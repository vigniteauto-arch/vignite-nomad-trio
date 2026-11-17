"""Atlas des sols — NASA EMIT (v1.8, 17/11/2026 ; v1.7 : 17/11/2026 ; v1.6 : 17/11/2026 ; V1.5 : 27/10/2026).

Réassemble, inventorie et extrait les granules NASA EMIT du dossier
data/emit/, puis les rattache aux dix bassins de la flotte P2 et en
donne la lecture agronomique (argiles 1:1 vs 2:1, carbonates, oxydes
de fer, gypsum) — socle « Soil Sciences » de la couche 1.

v1.6 (17/11/2026) : nouveau mode « l3-bassins » — échantillonnage du
L3 ASA (Aggregated Mineral Spectral Abundance) aux boîtes des dix
bassins directement dans le module, avec lecteur HDF5 (Hierarchical
Data Format version 5) minimal EMBARQUÉ en bibliothèque standard
(superblock v0/v2, en-têtes d'objets v2 « OHDR », messages v2, balayage
heuristique des liens denses, jeux de données CONTIGUS uniquement —
les onze couches minérales du L3 ASA sont contiguës, fait établi lors
de l'extraction locale du 06/11/2026). Le lecteur externe h5py/netCDF4/
xarray reste préféré s'il est présent ; le lecteur embarqué est le
repli sans installation. Les scènes L2B (jeux chunkés en arbre B v1)
restent hors du lecteur embarqué : extraire continue d'exiger h5py.

v1.7 (17/11/2026, au soir) : correctif du mode extraire — le parcours
des groupes itérait sur les NOMS du fichier au lieu des objets (bug
« 'str' object has no attribute 'keys' », constaté en atelier par Manu
sur les trois cartouches réassemblées : ce chemin n'avait jamais été
exercé avant le 17/11/2026) ; et extension aux scènes L2B COMPLÈTES :
cinq fichiers .nc entiers de la vague Earthdata du 17/11/2026
(Périgord, Sud-Ouest, Léman suisse, Pouilles, Misiones) posés dans
data/emit/ sans fragments, référencés par taille et empreinte SHA-512
(Secure Hash Algorithm 512 bits) du catalogue NASA (fiches UMM du CMR
— Common Metadata Repository), vérifiées à l'inventaire et contrôlées
à l'extraction. Les cartouches en fragments restent inchangées.

v1.8 (17/11/2026, dans la nuit) : trois correctifs de parcours constatés
en atelier après la poussée v1.7 (inventaire et extraire verts, croiser
et l3-bassins en échec — même famille que le bug v1.7 : des chemins
jamais exercés sur des fichiers réels). (1) croiser : les bornes lat/lon
étaient cherchées à la RACINE du fichier alors qu'EMIT les loge dans le
groupe « location » — d'où « scène hors périmètre » pour les huit
scènes ; la recherche est désormais récursive sur tout le fichier (1D
ou 2D, valeur de remplissage −9999 exclue). (2) l3-bassins :
l'heuristique de grille ne gardait que les 400 premières valeurs de
chaque axe (les « 400 longitudes » de l'atelier) et élisait « samples »
(rempli de zéros) comme longitude ; les axes sont désormais pris par
leur nom (« lat » : 220 latitudes de 55,0 à −54,5°, « lon » : 690
longitudes de −165,0 à 179,5°, pas 0,5° — faits établis le 17/11/2026
sur le granule réel), et l'heuristique de repli garde les listes
complètes en écartant les axes constants. (3) le lecteur HDF5 embarqué
refusait les en-têtes « OHDR » version 2 (version 1 exigée), confondait
les identifiants de messages et lisait dimensions et tailles aux
mauvais décalages : il n'avait jamais lu un seul fichier réel ; il est
réparé et validé sur le L3 ASA réel (33 couches minérales contiguës
220 x 690, classe 1 du message de disposition : adresse + taille en
octets).

PRODUITS (données publiques NASA, LP DAAC — Land Processes
Distributed Active Archive Center) :
- EMIT L2B MIN (EMITL2BMIN) : « Estimated Mineral Identification and
  Band Depth and Uncertainty », maille 60 m, scène par scène —
  identification minérale des surfaces affleurantes.
- EMIT L3 ASA (EMITL3ASA) : « Aggregated Mineral Spectral Abundance
  and Uncertainty », agrégation mondiale au demi-degré — la couche
  directement exploitable pour les bassins de la flotte.

ÉTIQUETTES (doctrine World Twin) : toute fraction extraite est SOURCÉE
(NASA EMIT) ; toute lecture agronomique (CEC — Capacité d'Échange
Cationique, dosage biochar) est ILLUSTRATION documentaire, jamais une
donnée calibrée, jamais une prescription.

DOCTRINE PI : données publiques NASA uniquement ; aucun paramètre du
VDE (Vignite Decision Engine), aucune clé, aucun secret. Les sorties
vivent dans cache-sols/, jamais versionnées.

LANCEMENT :
    python3 engine/atlas_sols_emit.py inventaire
    python3 engine/atlas_sols_emit.py reassembler [GRANULE]
    python3 engine/atlas_sols_emit.py extraire [SCÈNE|GRANULE] (h5py requis)
    python3 engine/atlas_sols_emit.py croiser
    python3 engine/atlas_sols_emit.py l3-bassins             (v1.6)
    python3 engine/atlas_sols_emit.py sommaire [BASSIN]
"""

import hashlib
import json
import os
import struct
import sys
import zipfile

DOSSIER = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."))
DOSSIER_EMIT = os.path.join(DOSSIER, "data", "emit")
DOSSIER_CACHE = os.path.join(DOSSIER, "cache-sols")

# ---------------------------------------------------------------------------
# Granules EMIT versionnés au dépôt (uploads du 24/10/2026, déplacés ici par
# la vague v1.5). Dates de scène lues dans le nom, cartouches au format
# EMIT_L2B_MIN_001_AAAAMMJJThhmmss_oorbit_ooo.nc découpé en .partN.
# ---------------------------------------------------------------------------
GRANULES_L2B = {
    "2302410_038": {"fichier": "EMIT_L2B_MIN_001_20230124T153032_2302410_038.nc",
                    "scene": "2023-01-24", "parts": 3},
    "2321608_018": {"fichier": "EMIT_L2B_MIN_001_20230804T113000_2321608_018.nc",
                    "scene": "2023-08-04", "parts": 3},
    "2420510_006": {"fichier": "EMIT_L2B_MIN_001_20240723T152209_2420510_006.nc",
                    "scene": "2024-07-23", "parts": 3},
    # Scènes L2B COMPLÈTES de la vague Earthdata du 17/11/2026 (v1.7) :
    # fichiers .nc entiers dans data/emit/, aucun fragment. Tailles et
    # empreintes SHA-512 de référence NASA (fiches UMM du catalogue CMR),
    # fichiers téléchargés vérifiés à l'octet près le 17/11/2026 au soir.
    "2620510_011": {"fichier": "EMIT_L2B_MIN_001_20260724T144642_2620510_011.nc",
                    "scene": "2026-07-24", "parts": 0, "octets": 40763540,
                    "sha512": "abed11ca244b023f46a4762463a5701114aa61d427842c862c4f495e6067b83cf995ea44920403cb8d77f9263e6295d9a82f9dc805f33940b603e27af8875036"},
    "2620510_010": {"fichier": "EMIT_L2B_MIN_001_20260724T144630_2620510_010.nc",
                    "scene": "2026-07-24", "parts": 0, "octets": 39685163,
                    "sha512": "248f41fac0c0089bb26453902121140da5331d0cf957fa82a66b1dfa99631c4943ad491a44385c5fadc536b59acd1a8fe42bd1841a7ae19515f20d353985aa6e"},
    "2620909_004": {"fichier": "EMIT_L2B_MIN_001_20260728T131411_2620909_004.nc",
                    "scene": "2026-07-28", "parts": 0, "octets": 40262971,
                    "sha512": "c228b19c42bb27241c27aec157c225d6a70a52df905c778dcf67a3a0f646a5b3d7adf56635477736276421e7e65f44f949aec4f0925f11d9d04d03331b5d7853"},
    "2521806_009": {"fichier": "EMIT_L2B_MIN_001_20250806T083943_2521806_009.nc",
                    "scene": "2025-08-06", "parts": 0, "octets": 41537754,
                    "sha512": "f0a7c9642307d9f297ea3d7406e27ac15d762f059c6657ae66bc441288a00a1914b1e5db06ecda217d5ca813b6289ac4874a8447943fa8973cad728e7a86e0d6"},
    "2619512_016": {"fichier": "EMIT_L2B_MIN_001_20260714T172731_2619512_016.nc",
                    "scene": "2026-07-14", "parts": 0, "octets": 39796339,
                    "sha512": "f32919d4f2cbff126e32bc8baceeb0546ecf54a179e9803c958013b51c5d9b580fa68ce40d5789cb74bf9f264a945a2ba969b8b4d7e56fa78a51ae7b14ce65be"},
}
GRANULE_L3 = {"fichier": "EMIT_L3_ASA_002.zip",
              "nc_interne": "EMIT_L3_ASA_002.nc",
              "produit": "EMITL3ASA V002 — agrégation mondiale 0,5 degré"}

# Grille documentaire du L3 ASA, consignée le 06/11/2026 lors de la
# première extraction locale (superblock v2 lu dans le granule réel) :
# latitude 220 valeurs de −54,5° à +55,0° (pas 0,5°), longitude 690
# valeurs de −165,0° à +179,5°. Utilisée UNIQUEMENT si le lecteur ne
# retrouve pas les jeux 1D de coordonnées dans le fichier (repli).
GRILLE_L3_DOCUMENTAIRE = {
    "lat": [-54.5 + 0.5 * i for i in range(220)],
    "lon": [-165.0 + 0.5 * i for i in range(690)],
}
NODATA_L3 = -9999.0

# ---------------------------------------------------------------------------
# Bassins de la flotte P2 — mêmes boîtes géographiques que la couche FIRMS
# (engine/firms.py, v0.4) : (ouest, sud, est, nord). Approximation de la
# région, pas un cadastre (limite honnête inchangée).
# ---------------------------------------------------------------------------
BOITES_BASSINS = {
    "vallee-du-rhone": (4.40, 43.90, 5.30, 44.50),
    "camargue": (3.50, 43.20, 5.50, 44.30),
    "perigord": (0.20, 44.70, 1.20, 45.30),
    "sud-ouest": (-1.00, 43.60, 0.00, 44.50),
    "suisse-leman": (6.40, 46.30, 7.20, 46.75),
    "italie-puglia": (15.30, 40.70, 16.60, 41.70),
    "espagne-extremadure": (-6.60, 38.70, -5.00, 39.60),
    "argentine-cuyo": (-69.60, -34.20, -67.40, -32.50),
    "argentine-misiones": (-55.80, -27.80, -54.30, -26.40),
    "maroc-atlas": (-6.20, 32.90, -4.60, 34.20),
}

# ---------------------------------------------------------------------------
# Groupes minéraux EMIT et lecture agronomique (science des sols publique).
# La colonne « lecture » est ILLUSTRATION documentaire, jamais calibrée.
# ---------------------------------------------------------------------------
MINERAUX_LECTURE = {
    "kaolinite": {"famille": "argile 1:1", "cec": "faible (3-15 cmol+/kg)",
                  "lecture": "sols à faible rétention, drainage rapide — le biochar y apporte le gain de rétention le plus visible (ILLUSTRATION)"},
    "smectite": {"famille": "argile 2:1 expansive", "cec": "élevée (80-150 cmol+/kg)",
                 "lecture": "vertisols, forte rétention d'eau, risque de compaction — dosage biochar prudent, viser la structure (ILLUSTRATION)"},
    "illite": {"famille": "argile 2:1 non expansive", "cec": "moyenne (20-40 cmol+/kg)",
               "lecture": "sols équilibrés, rétention correcte — biochar en entretien (ILLUSTRATION)"},
    "muscovite": {"famille": "mica 2:1", "cec": "moyenne", "lecture": "compagne de l'illite (ILLUSTRATION)"},
    "chlorite": {"famille": "argile 2:1:1", "cec": "moyenne (10-40 cmol+/kg)",
                 "lecture": "sols de roches ferromagnésiennes, drainage variable (ILLUSTRATION)"},
    "vermiculite": {"famille": "argile 2:1 expansive", "cec": "très élevée (100-150 cmol+/kg)",
                     "lecture": "forte rétention, sensible au potassium — biochar en appoint (ILLUSTRATION)"},
    "calcite": {"famille": "carbonate", "cec": "—",
                "lecture": "sols calcaires, pH tamponné, phosphore lessivé par le calcium — le biochar n'y relève pas le pH, inutile de surdoser (ILLUSTRATION)"},
    "dolomite": {"famille": "carbonate double", "cec": "—",
                 "lecture": "calcaire dolomitique, magnésium disponible (ILLUSTRATION)"},
    "gypsum": {"famille": "sulfate", "cec": "—",
               "lecture": "risque de salinité et sodicité, drainage à surveiller avant toute amendment (ILLUSTRATION)"},
    "hematite": {"famille": "oxyde de fer", "cec": "faible",
                 "lecture": "sols rouges, forte sorption du phosphore, bonne agrégation (ILLUSTRATION)"},
    "goethite": {"famille": "oxyde de fer", "cec": "faible",
                 "lecture": "sols jaunes-bruns, sorption P et agrégation — bonne assise pour biochar de structure (ILLUSTRATION)"},
    "quartz": {"famille": "oxyde", "cec": "nulle",
               "lecture": "texture sableuse, drainage rapide (ILLUSTRATION)"},
}

ETIQUETTE = "SOURCÉ (NASA EMIT — données publiques LP DAAC)"


def _md5(chemin):
    h = hashlib.md5()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def _sha512(chemin):
    h = hashlib.sha512()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


# ===========================================================================
# Lecteur HDF5 minimal — bibliothèque standard (v1.6)
# ===========================================================================
# Porté du lecteur h5mini.py écrit le 06/11/2026 pour l'extraction locale
# (faits de format consignés ce jour-là sur les granules réels du dépôt,
# fichiers écrits par netCDF 4.7.4 / HDF5 1.12.0) : superblock v0 (L2B) et
# v2 (L3), en-têtes d'objets racine v2 « OHDR » (fanions 0x0d : champ de
# taille de chunk sur 2 octets), messages v2 type(1) + taille(2) + fanions(1)
# + ordre de création(2) sans remplissage, chunks de continuation « OCHK ».
# LIMITES HONNÊTES : jeux de données CONTIGUS uniquement (les onze couches
# minérales du L3 ASA sont contiguës — fait établi le 06/11/2026) ; les
# scènes L2B chunkées (arbre B v1 « TREE », filtres deflate/shuffle) restent
# du ressort de h5py. Les liens denses (tas fractal FRHP) sont résolus par
# balayage heuristique : un nom n'est retenu que si les 8 octets qui le
# suivent pointent sur une signature « OHDR » valide — l'adresse fait foi.
#
# v1.8 (17/11/2026, nuit) : lecteur RÉPARÉ — il exigeait la version 1 des
# en-têtes OHDR (les fichiers réels écrivent la version 2), cherchait
# l'espace de données sous 0x11, le type sous 0x0B et la disposition sous
# 0x03 (identifiants réels : 0x01, 0x03, 0x08), et lisait la taille du
# type à l'octet 8 (elle vit à l'octet 4) et les dimensions v2 à l'octet
# 8 (elles vivent à l'octet 4 ; v1 : octet 8). Le v1.6 n'avait donc
# jamais lu un seul fichier réel. Validé sur le L3 ASA réel du dépôt.
# ===========================================================================


class ErreurLecteur(Exception):
    pass


class LecteurHDF5Minimal(object):
    """Lecteur HDF5 minimal : jeux contigus, retour {nom: dict}."""

    SIG_OHDR = b"OHDR"
    SIG_OCHK = b"OCHK"
    NOM_VALIDES = set(
        b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_/.-")

    def __init__(self, chemin):
        with open(chemin, "rb") as f:
            self.donnees = f.read()
        self.taille = len(self.donnees)
        self.taille_off = 8
        self.taille_len = 8

    # -- primitives ---------------------------------------------------------
    def _u(self, pos, n):
        return int.from_bytes(self.donnees[pos:pos + n], "little")

    def _superblock(self):
        """Localise le superblock, relève version et tailles d'adresses."""
        for pos in range(0, min(4096, self.taille), 512):
            if self.donnees[pos:pos + 8] == b"\x89HDF\r\n\x1a\n":
                version = self.donnees[pos + 8]
                if version == 0:
                    self.taille_off = self.donnees[pos + 13]
                    self.taille_len = self.donnees[pos + 14]
                elif version in (2, 3):
                    self.taille_off = self.donnees[pos + 9]
                    self.taille_len = self.donnees[pos + 10]
                return version
        raise ErreurLecteur("signature HDF5 introuvable — fichier corrompu ?")

    def _messages_ohdr(self, addr):
        """Messages d'un en-tête d'objet v2 (suivis jusqu'à « OCHK »)."""
        if self.donnees[addr:addr + 4] != self.SIG_OHDR:
            raise ErreurLecteur("signature OHDR absente à %d" % addr)
        if self.donnees[addr + 4] != 2:
            raise ErreurLecteur("version OHDR inattendue : %d (attendu : 2 — "
                                "v1.8 : les fichiers EMIT réels écrivent la "
                                "version 2)" % self.donnees[addr + 4])
        fanions = self.donnees[addr + 5]
        # v1.8 : la largeur du champ « taille du chunk 0 » se lit dans les
        # bits 0-1 des fanions (0 : 1 octet, 1 : 2, 2 : 4, 3 : 8 — préfixe
        # d'en-tête v2). Le v1.6 testait le bit 2 et lisait toujours
        # 2 octets : de la chance sur nos fichiers (fanions 0x0d), pas de
        # la spécification.
        largeur = (1, 2, 4, 8)[fanions & 0x03]
        pos = addr + 6
        taille_chunk0 = self._u(pos, largeur)
        if not taille_chunk0:
            raise ErreurLecteur("taille de chunk nulle à %d" % addr)
        fin = pos + largeur + taille_chunk0
        return self._messages_a_partir_de(pos + largeur, fin,
                                          bool(fanions & 0x08))

    def _messages_a_partir_de(self, debut, fin, avec_ordre):
        """Messages v2 : type(1) + taille(2) + fanions(1) + ordre(2 si suivi)."""
        messages = []
        pos = debut
        while pos + 4 <= fin and pos + 4 <= self.taille:
            mtype = self.donnees[pos]
            if mtype == 0x00:
                break
            mtaille = self._u(pos + 1, 2)
            pos += 4
            if avec_ordre:
                pos += 2
            if mtype == 0x10 and mtaille >= 16:
                addr = self._u(pos, 8)
                longueur = self._u(pos + 8, 8)
                sous = addr + 4 if self.donnees[addr:addr + 4] == self.SIG_OCHK else addr
                if 0 < addr < self.taille:
                    messages.extend(self._messages_a_partir_de(
                        sous, min(sous + longueur, self.taille), avec_ordre))
            else:
                messages.append((mtype, self.donnees[pos:pos + mtaille]))
            pos += mtaille
        return messages

    # -- messages utiles ----------------------------------------------------
    def _dataspace(self, corps):
        """v1.8 : dimensions v1 à l'octet 8, v2 à l'octet 4 (spécification)."""
        version = corps[0]
        ndims = corps[1]
        pos = 8 if version < 2 else 4
        dims = []
        for _ in range(ndims):
            dims.append(int.from_bytes(corps[pos:pos + 8], "little"))
            pos += 8
        return dims

    def _datatype(self, corps):
        """v1.8 : version dans le quartet HAUT, classe dans le BAS ;
        taille de l'élément à l'octet 4 (le v1.6 lisait la classe dans
        le mauvais quartet et la taille à l'octet 8)."""
        classe = corps[0] & 0x0F
        if classe not in (0, 1):
            return None
        taille = int.from_bytes(corps[4:8], "little")
        gros_boutisme = bool(corps[1] & 0x01)
        return (classe, taille, gros_boutisme)

    def _layout_contigu(self, corps):
        if len(corps) < 2 or corps[0] != 3 or corps[1] != 1:
            return None
        addr = int.from_bytes(corps[2:10], "little")
        taille = int.from_bytes(corps[10:18], "little")
        return addr, taille

    def _dataset_depuis_ohdr(self, addr):
        """Retourne la description d'un jeu contigu, sinon None."""
        try:
            messages = self._messages_ohdr(addr)
        except ErreurLecteur:
            return None
        dims, dtype, layout = None, None, None
        for mtype, corps in messages:
            # v1.8 : identifiants réels — espace de données 0x01 (le v1.6
            # cherchait 0x11, la table de symboles), type de données 0x03
            # (cherché sous 0x0B, les filtres) et disposition 0x08
            # (cherchée sous 0x03) : aucun fichier réel n'était lisible.
            if mtype == 0x01 and dims is None:
                dims = self._dataspace(corps)
            elif mtype == 0x03 and dtype is None:
                dtype = self._datatype(corps)
            elif mtype == 0x08 and layout is None:
                layout = self._layout_contigu(corps)
        if dtype is None or not (dims and layout):
            return None
        classe, taille_elem, gros_boutisme = dtype
        if classe not in (0, 1):
            return None
        addr_donnees, octets = layout
        if len(dims) not in (1, 2) or taille_elem not in (4, 8):
            return None
        if addr_donnees + octets > self.taille:
            return None
        return {"dims": dims, "taille_elem": taille_elem,
                "gros_boutisme": gros_boutisme,
                "octets": octets, "adresse": addr_donnees}

    # -- résolution heuristique des noms ------------------------------------
    def _est_nom(self, octet):
        return bool(octet) and octet[0] in self.NOM_VALIDES

    def _noms_vers_ohdr(self):
        """Balayage : nom ASCII complet suivi d'une adresse pointant sur OHDR.

        Seuls les DÉBUTS de séquence sont retenus (l'octet précédent n'est
        pas un caractère de nom) : sans cette garde, toute sous-chaîne d'un
        nom (« aolinite » dans « Kaolinite ») créerait un alias parasite.
        L'adresse fait foi : le nom n'est accepté que si les 8 octets qui
        le suivent pointent sur une signature « OHDR » version 2 valide.
        """
        donnees = self.donnees
        vus = set()
        addr = -1
        while True:
            addr = donnees.find(self.SIG_OHDR, addr + 1)
            if addr < 0 or addr + 7 > self.taille:
                break
            if donnees[addr + 4] == 2 and donnees[addr + 5] <= 0x3f:
                vus.add(addr)
        resultat = {}
        i, n = 0, self.taille
        while i < n:
            if self._est_nom(donnees[i:i + 1]) and (
                    i == 0 or not self._est_nom(donnees[i - 1:i])):
                fin = i
                while fin < n and self._est_nom(donnees[fin:fin + 1]):
                    fin += 1
                if fin - i >= 3:
                    # l'octet de poids faible de l'adresse peut être un
                    # caractère de nom (334 = 0x4E = « N ») : la séquence
                    # peut donc engloutir le début de l'adresse — tester
                    # toutes les coupes, la plus longue d'abord
                    for coupe in range(fin, i + 2, -1):
                        if coupe + 8 > n:
                            continue
                        cible = int.from_bytes(donnees[coupe:coupe + 8], "little")
                        if cible in vus:
                            nom = donnees[i:coupe].decode("ascii", "replace")
                            resultat.setdefault(nom, cible)
                            break
                i = fin
            else:
                i += 1
        return resultat

    # -- API ----------------------------------------------------------------
    def jeux_contigus(self):
        """{nom: {dims, valeurs float, ...}} pour les jeux numériques 1D/2D."""
        self._superblock()
        noms = self._noms_vers_ohdr()
        jeux = {}
        for nom, addr in sorted(noms.items()):
            info = self._dataset_depuis_ohdr(addr)
            if info is None:
                continue
            n = 1
            for d in info["dims"]:
                n *= d
            if n * info["taille_elem"] > info["octets"]:
                continue
            brut = self.donnees[info["adresse"]:info["adresse"] + n * info["taille_elem"]]
            if info["taille_elem"] == 4:
                fmt = ">%df" if info["gros_boutisme"] else "<%df"
                valeurs = list(struct.unpack(fmt % n, brut))
            else:
                fmt = ">%dd" if info["gros_boutisme"] else "<%dd"
                valeurs = list(struct.unpack(fmt % n, brut))
            jeux[nom] = {"dims": info["dims"], "valeurs": valeurs,
                         "adresse": info["adresse"], "octets": info["octets"]}
        if not jeux:
            raise ErreurLecteur(
                "aucun jeu contigu résolu — le lecteur embarqué ne couvre pas "
                "ce fichier ; installer h5py (pip install h5py) et relancer")
        return jeux


# ===========================================================================
# Mode l3-bassins (v1.6)
# ===========================================================================

def _jeux_h5py(chemin):
    """Collecte les jeux numériques via h5py : {nom: {dims, valeurs}}."""
    import h5py
    jeux = {}

    def visiter(nom, objet):
        if isinstance(objet, h5py.Dataset) and objet.dtype.kind == "f":
            dims = list(objet.shape)
            if len(dims) in (1, 2):
                jeux[nom.rsplit("/", 1)[-1]] = {
                    "dims": dims, "valeurs": objet[:].astype("f8").ravel().tolist()}

    with h5py.File(chemin, "r") as f:
        f.visititems(visiter)
    return jeux


def _decompresser_l3():
    """Décompresse le zip L3 dans cache-sols/ (jamais versionné)."""
    chemin_zip = os.path.join(DOSSIER_EMIT, GRANULE_L3["fichier"])
    if not os.path.exists(chemin_zip):
        print("zip L3 ASA introuvable : data/emit/%s" % GRANULE_L3["fichier"])
        return None
    os.makedirs(DOSSIER_CACHE, exist_ok=True)
    cible = os.path.join(DOSSIER_CACHE, GRANULE_L3["nc_interne"])
    with zipfile.ZipFile(chemin_zip) as z:
        membres = [m for m in z.namelist() if m.endswith(".nc")]
        if not membres:
            print("aucun .nc dans le zip L3 ASA")
            return None
        with z.open(membres[0]) as source, open(cible, "wb") as sortie:
            sortie.write(source.read())
    print("L3 ASA décompressé : cache-sols/%s — %d octets, md5 %s" % (
        GRANULE_L3["nc_interne"], os.path.getsize(cible), _md5(cible)))
    print("la décompression vit dans cache-sols/, jamais versionné")
    return cible


def _grille_l3(jeux):
    """Axes de la grille L3 lus par leur nom, repli heuristique corrigé (v1.8).

    Le v1.6 ne gardait que les 400 premières valeurs de chaque axe (d'où
    les « 400 longitudes » de l'atelier) et élit « samples » (jeu rempli
    de zéros) comme longitude. Sur le granule réel : « lat » = 220
    latitudes (55,0 à −54,5°, pas −0,5°), « lon » = 690 longitudes
    (−165,0 à 179,5°, pas 0,5°). Le repli heuristique garde désormais
    les listes complètes et écarte les axes constants.
    """
    lat = lon = None
    for nom, info in jeux.items():
        if len(info["dims"]) != 1 or info["dims"][0] < 50:
            continue
        vals = list(info["valeurs"])
        if len(vals) < 2 or vals[0] == vals[-1]:
            continue
        if nom == "lat" and lat is None:
            lat = (nom, vals)
        elif nom == "lon" and lon is None:
            lon = (nom, vals)
    if lat is not None and lon is not None:
        return {"lat": lat[1], "lon": lon[1],
                "source": "lue dans le granule par nom (jeux 1D %s, %s — "
                          "correctif v1.8)" % (lat[0], lon[0])}
    candidats = {"lat": [], "lon": []}
    for nom, info in jeux.items():
        if len(info["dims"]) != 1 or info["dims"][0] < 50:
            continue
        vals = list(info["valeurs"])
        if len(vals) < 2 or vals[0] == vals[-1]:
            continue
        if -90.0 <= min(vals) and max(vals) <= 90.0:
            candidats["lat"].append((info["dims"][0], nom, vals))
        if -180.0 <= min(vals) and max(vals) <= 180.0:
            candidats["lon"].append((info["dims"][0], nom, vals))
    if candidats["lat"] and candidats["lon"]:
        lat = sorted(candidats["lat"])[0]
        lon = sorted(candidats["lon"], reverse=True)[0]
        if lat[0] >= lon[0]:
            lat, lon = lon, lat
        return {"lat": lat[2], "lon": lon[2],
                "source": "repli heuristique v1.8, listes complètes "
                          "(jeux 1D %s, %s)" % (lat[1], lon[1])}
    return {"lat": GRILLE_L3_DOCUMENTAIRE["lat"],
            "lon": GRILLE_L3_DOCUMENTAIRE["lon"],
            "source": "repli documentaire consigné le 06/11/2026 "
                      "(jeux 1D de coordonnées non résolus par le lecteur)"}


def l3_bassins():
    """Échantillonne le L3 ASA aux boîtes des dix bassins (v1.6, corrigé v1.8).

    Décompresse data/emit/EMIT_L3_ASA_002.zip dans cache-sols/, lit le
    .nc avec h5py si présent, sinon avec le lecteur HDF5 minimal embarqué
    (jeux contigus uniquement — les couches L3 le sont). Calcule par
    bassin et par couche la moyenne des mailles valides (nodata −9999
    exclu). Écrit cache-sols/l3-bassins.json, jamais versionné.
    """
    chemin = _decompresser_l3()
    if chemin is None:
        return 1
    module, nom_lecteur = _lecteur()
    jeux = None
    provenance = None
    if module is not None and nom_lecteur == "h5py":
        jeux = _jeux_h5py(chemin)
        provenance = "lecteur h5py externe"
    if not jeux:
        try:
            jeux = LecteurHDF5Minimal(chemin).jeux_contigus()
            provenance = "lecteur HDF5 minimal embarqué (bibliothèque standard)"
        except ErreurLecteur as e:
            print("lecteur embarqué : %s" % e)
            print("consigne : pip install h5py  puis relancer l3-bassins")
            return 1
    print("lecture : %s — %d jeux résolus" % (provenance, len(jeux)))

    grille = _grille_l3(jeux)
    lat, lon = grille["lat"], grille["lon"]
    print("grille : %d latitudes, %d longitudes — %s" % (
        len(lat), len(lon), grille["source"]))

    couches = {}
    for nom, info in jeux.items():
        if len(info["dims"]) == 2 and info["dims"] == [len(lat), len(lon)]:
            couches[nom] = info["valeurs"]
    if not couches:
        print("aucune couche 2D %d x %d résolue — STOP, voir grille" % (
            len(lat), len(lon)))
        return 1
    print("couches minérales 2D résolues : %d — %s" % (
        len(couches), ", ".join(sorted(couches))))

    resultat = {"produit": GRANULE_L3["produit"],
                "lecteur": provenance, "grille": {
                    "lat": [round(v, 4) for v in (lat[0], lat[-1])],
                    "lon": [round(v, 4) for v in (lon[0], lon[-1])],
                    "source": grille["source"]},
                "bassins": {}, "etiquette": ETIQUETTE}
    print("\n%s" % ("-" * 72))
    for bassin, (o, s, e, n) in BOITES_BASSINS.items():
        idx_lat = [i for i, v in enumerate(lat) if s <= v <= n]
        idx_lon = [j for j, v in enumerate(lon) if o <= v <= e]
        total = len(idx_lat) * len(idx_lon)
        compte = {"bassin": bassin,
                  "boite": "(O %s, S %s, E %s, N %s)" % (o, s, e, n),
                  "mailles_total": total, "couches": {}}
        dominantes = []
        for nom, valeurs in couches.items():
            somme, valides = 0.0, 0
            for i in idx_lat:
                base = i * len(lon)
                for j in idx_lon:
                    v = valeurs[base + j]
                    if v != NODATA_L3 and v > -1000.0:
                        somme += v
                        valides += 1
            if valides:
                moyenne = somme / valides
                compte["couches"][nom] = {"moyenne": round(moyenne, 4),
                                          "mailles_valides": valides}
                dominantes.append((moyenne, nom, valides))
        dominantes.sort(reverse=True)
        compte["dominantes"] = [{"couche": nom, "moyenne": round(moyenne, 4),
                                 "mailles_valides": valides}
                                for moyenne, nom, valides in dominantes[:3]]
        resultat["bassins"][bassin] = compte
        couverture = "COUVERT (%d/%d mailles)" % (
            dominantes[0][2], total) if dominantes else "HORS COUVERTURE (0/%d)" % total
        print("%s — %s" % (bassin, couverture))
        for moyenne, nom, valides in dominantes[:3]:
            print("    %-14s %8.4f  (%d mailles valides)" % (nom, moyenne, valides))
    print("-" * 72)
    print("\nÉtiquette : %s — fractions SOURCÉES, lecture agronomique "
          "toujours ILLUSTRATION" % ETIQUETTE)
    print("sortie : cache-sols/l3-bassins.json (jamais versionné)")
    _ecrire_cache("l3-bassins.json", resultat)
    return 0


# ===========================================================================
# Modes v1.5 (inchangés)
# ===========================================================================

def inventaire():
    """Tailles, empreintes md5 et complétude des granules versionnés."""
    print("Inventaire NASA EMIT — dossier data/emit/ (v1.8)\n")
    if not os.path.isdir(DOSSIER_EMIT):
        print("  dossier data/emit/ introuvable — lancer la vague v1.5 (déplacement des .part)")
        return 1
    lignes = []
    for cart, meta in sorted(GRANULES_L2B.items()):
        print("L2B MIN %s — scène %s" % (cart, meta["scene"]))
        if meta["parts"] == 0:
            nom = meta["fichier"]
            chemin = os.path.join(DOSSIER_EMIT, nom)
            if os.path.exists(chemin):
                taille = os.path.getsize(chemin)
                conforme = (taille == meta["octets"]
                            and _sha512(chemin) == meta["sha512"])
                print("  %-46s %9d octets  SHA-512 %s" % (
                    nom, taille, "CONFORME (référence NASA)" if conforme
                    else "NON CONFORME — retélécharger la scène"))
                lignes.append({"part": nom, "octets": taille,
                               "scene_complete": True,
                               "conforme_nasa": conforme})
            else:
                print("  %-46s ABSENT (scène complète attendue dans data/emit/)" % nom)
                lignes.append({"part": nom, "octets": None,
                               "scene_complete": True})
            print()
            continue
        for i in range(meta["parts"]):
            nom = meta["fichier"] + ".part%d" % i
            chemin = os.path.join(DOSSIER_EMIT, nom)
            if os.path.exists(chemin):
                taille = os.path.getsize(chemin)
                print("  %-46s %9d octets  md5 %s" % (nom, taille, _md5(chemin)))
                lignes.append({"part": nom, "octets": taille})
            else:
                print("  %-46s ABSENT" % nom)
                lignes.append({"part": nom, "octets": None})
        print()
    chemin_zip = os.path.join(DOSSIER_EMIT, GRANULE_L3["fichier"])
    print("L3 ASA — %s" % GRANULE_L3["produit"])
    if os.path.exists(chemin_zip):
        print("  %-46s %9d octets  md5 %s" % (
            GRANULE_L3["fichier"], os.path.getsize(chemin_zip), _md5(chemin_zip)))
        lignes.append({"part": GRANULE_L3["fichier"],
                       "octets": os.path.getsize(chemin_zip)})
    else:
        print("  %s ABSENT" % GRANULE_L3["fichier"])
        lignes.append({"part": GRANULE_L3["fichier"], "octets": None})
    print("\nÉtiquette : %s" % ETIQUETTE)
    _ecrire_cache("inventaire.json", lignes)
    return 0


def reassembler(cartouche=None):
    """Concatène les .partN en .nc dans cache-sols/ (jamais versionné)."""
    if cartouche is None:
        print("reassembler GRANULE — cartouche requis parmi : %s" %
              ", ".join(GRANULES_L2B))
        return 1
    if cartouche not in GRANULES_L2B:
        print("cartouche inconnu : %s" % cartouche)
        return 1
    meta = GRANULES_L2B[cartouche]
    if meta["parts"] == 0:
        print("scène complète — rien à réassembler : %s" % meta["fichier"])
        print("extraire %s la lit directement depuis data/emit/ (v1.7)" % cartouche)
        return 0
    os.makedirs(DOSSIER_CACHE, exist_ok=True)
    sortie = os.path.join(DOSSIER_CACHE, meta["fichier"])
    total = 0
    with open(sortie, "wb") as f:
        for i in range(meta["parts"]):
            nom = meta["fichier"] + ".part%d" % i
            chemin = os.path.join(DOSSIER_EMIT, nom)
            if not os.path.exists(chemin):
                print("partie manquante : %s" % nom)
                return 1
            with open(chemin, "rb") as p:
                bloc = p.read(1 << 20)
                while bloc:
                    f.write(bloc)
                    total += len(bloc)
                    bloc = p.read(1 << 20)
    print("réassemblé : cache-sols/%s — %d octets, md5 %s" % (
        meta["fichier"], total, _md5(sortie)))
    print("le réassemblage vit dans cache-sols/, jamais versionné")
    return 0


def _lecteur():
    """Retourne un module lecteur NetCDF-4/HDF5 disponible, sinon None."""
    for nom in ("h5py", "netCDF4", "xarray"):
        try:
            return __import__(nom), nom
        except ImportError:
            continue
    return None, None


def extraire(cartouche=None):
    """Extrait l'empreinte géographique et les fractions minérales.

    L2B MIN : bornes lat/lon de la scène + variables par groupe minéral.
    Sans argument : chaque granule connu — cartouches réassemblées dans
    cache-sols/ et scènes complètes de data/emit/ (v1.7).
    Écrit cache-sols/extraire-*.json, jamais versionné.
    """
    module, nom_lecteur = _lecteur()
    if module is None:
        print("aucun lecteur NetCDF-4/HDF5 disponible")
        print("installer au choix : pip install h5py  (ou netCDF4, ou xarray)")
        print("les modes inventaire/reassembler/l3-bassins/sommaire restent "
             "disponibles (l3-bassins embarque son propre lecteur contigu)")
        return 1
    if nom_lecteur == "h5py":
        return _extraire_h5py(cartouche)
    print("lecteur %s détecté — l'extraction est implémentée pour h5py, "
          "le plus léger des trois ; installer h5py (pip install h5py)" % nom_lecteur)
    return 1


def _extraire_h5py(cartouche):
    import h5py
    cibles = [cartouche] if cartouche else list(GRANULES_L2B)
    resultats = []
    for cart in cibles:
        meta = GRANULES_L2B[cart]
        complet = meta["parts"] == 0
        dossier = DOSSIER_EMIT if complet else DOSSIER_CACHE
        chemin = os.path.join(dossier, meta["fichier"])
        if not os.path.exists(chemin):
            if complet:
                print("%s : absent de data/emit/ — scène complète attendue "
                      "(vague Earthdata du 17/11/2026)" % cart)
            else:
                print("%s : absent de cache-sols/ — lancer d'abord : "
                      "python3 engine/atlas_sols_emit.py reassembler %s" % (cart, cart))
            continue
        if complet and _sha512(chemin) != meta["sha512"]:
            print("%s : empreinte SHA-512 NON CONFORME à la référence NASA "
                  "— retélécharger la scène, rien n'est extrait" % cart)
            continue
        donnees = {"cartouche": cart, "scene": meta["scene"],
                   "etiquette": ETIQUETTE,
                   "provenance": ("data/emit/ (scène complète, v1.7)" if complet
                                  else "cache-sols/ (cartouche réassemblée)")}
        with h5py.File(chemin, "r") as f:
            donnees["variables"] = sorted(f.keys())
            groupes = {}
            for nom_groupe in f:
                objet = f[nom_groupe]
                if isinstance(objet, h5py.Group):
                    groupes["/" + nom_groupe] = sorted(objet.keys())
            donnees["groupes"] = groupes
            donnees["bornes"] = _bornes_h5py(f)
        resultats.append(donnees)
        print("extrait : %s (scène %s) — variables : %d" % (
            cart, meta["scene"], len(donnees["variables"])))
    _ecrire_cache("extraire.json", resultats)
    return 0


def _bornes_h5py(f):
    """Bornes lat/lon récursives (v1.8).

    EMIT loge les coordonnées des scènes L2B dans le groupe « location »,
    jamais à la racine : le v1.6 ne cherchait qu'à la racine, donc
    « scène hors périmètre » pour tout. La recherche parcourt désormais
    tout le fichier (1D ou 2D), en excluant la valeur de remplissage.
    """
    bornes = {}

    def visiter(nom, objet):
        base = nom.rsplit("/", 1)[-1].lower()
        if base not in ("lat", "latitude", "lon", "longitude"):
            return
        try:
            jeu = objet[:]
            if hasattr(jeu, "ravel"):
                valeurs = [float(v) for v in jeu.ravel()]
            else:
                valeurs = [float(v) for v in jeu]
            valeurs = [v for v in valeurs
                       if v != NODATA_L3 and -1000.0 < v < 1000.0]
            if not valeurs:
                return
            cle = "lat" if base in ("lat", "latitude") else "lon"
            if cle not in bornes:
                bornes[cle] = [round(min(valeurs), 4),
                               round(max(valeurs), 4)]
        except Exception:
            pass

    try:
        f.visititems(visiter)
    except Exception:
        pass
    return bornes


def croiser():
    """Rattache les extractions aux dix bassins de la flotte.

    Un granule L2B dont l'empreinte recouvre une boîte de bassin y est
    rattaché (approximation de la région, pas un cadastre). Produit
    cache-sols/croisement.json, base des fiches de atlas-sols-emit.md.
    """
    chemin = os.path.join(DOSSIER_CACHE, "extraire.json")
    if not os.path.exists(chemin):
        print("aucune extraction — lancer d'abord : "
              "python3 engine/atlas_sols_emit.py extraire")
        return 1
    with open(chemin, encoding="utf-8") as f:
        extractions = json.load(f)
    croisement = []
    for ext in extractions:
        bornes = ext.get("bornes") or {}
        rattachements = []
        for bassin, (o, s, e, n) in BOITES_BASSINS.items():
            lat = bornes.get("lat") or bornes.get("latitude")
            lon = bornes.get("lon") or bornes.get("longitude")
            if not lat or not lon:
                continue
            if lat[0] < n and lat[1] > s and lon[0] < e and lon[1] > o:
                rattachements.append(bassin)
        croisement.append({"cartouche": ext["cartouche"],
                           "scene": ext["scene"],
                           "bassins": rattachements,
                           "hors_bassins_flotte": not rattachements,
                           "etiquette": ETIQUETTE})
        print("%s (scène %s) -> %s" % (
            ext["cartouche"], ext["scene"],
            ", ".join(rattachements) or "aucun bassin de la flotte (scène hors périmètre)"))
    _ecrire_cache("croisement.json", croisement)
    print("\nÉtiquette : %s — rattachement géographique SOURCÉ, "
          "lecture agronomique toujours ILLUSTRATION" % ETIQUETTE)
    return 0


def sommaire(bassin=None):
    """Sommaire de la couche sols : bassins, granules, lectures."""
    if bassin and bassin not in BOITES_BASSINS:
        print("bassin inconnu : %s — bassins : %s" % (
            bassin, ", ".join(BOITES_BASSINS)))
        return 1
    if bassin:
        o, s, e, n = BOITES_BASSINS[bassin]
        print("Bassin %s — boîte (O %s, S %s, E %s, N %s) [ILLUSTRATION géographique]" % (
            bassin, o, s, e, n))
        chemin = os.path.join(DOSSIER_CACHE, "croisement.json")
        if os.path.exists(chemin):
            with open(chemin, encoding="utf-8") as f:
                for ligne in json.load(f):
                    if bassin in ligne["bassins"]:
                        print("  granule EMIT %s (scène %s) — %s" % (
                            ligne["cartouche"], ligne["scene"], ligne["etiquette"]))
        chemin_l3 = os.path.join(DOSSIER_CACHE, "l3-bassins.json")
        if os.path.exists(chemin_l3):
            with open(chemin_l3, encoding="utf-8") as f:
                compte = json.load(f)["bassins"][bassin]
                if compte["dominantes"]:
                    print("  L3 ASA : COUVERT — dominantes %s" % ", ".join(
                        "%s %.4f" % (d["couche"], d["moyenne"])
                        for d in compte["dominantes"]))
                else:
                    print("  L3 ASA : HORS COUVERTURE (végétation ou limite du capteur)")
        return 0
    print("Atlas des sols — NASA EMIT (v1.8, 17/11/2026 ; v1.7 : 17/11/2026 ; "
          "v1.6 : 17/11/2026 ; V1.5 : 27/10/2026)\n")
    cartouches = sorted(c for c, m in GRANULES_L2B.items() if m["parts"] > 0)
    completes = sorted(c for c, m in GRANULES_L2B.items() if m["parts"] == 0)
    print("Granules L2B MIN : %d — cartouches en fragments : %d (%s) ; "
          "scènes complètes : %d (%s)" % (
              len(GRANULES_L2B), len(cartouches), ", ".join(cartouches),
              len(completes), ", ".join(completes)))
    print("Granule L3 ASA : %s (agrégation mondiale 0,5 degré)" % GRANULE_L3["fichier"])
    print("Mode « l3-bassins » (v1.6, corrigé v1.8 : axes de grille lus par "
          "nom, lecteur HDF5 réparé) : échantillonnage du L3 aux dix "
          "boîtes, lecteur embarqué en bibliothèque standard "
          "(jeux contigus, h5py préféré s'il est présent)")
    print("Bassins de la flotte : %d" % len(BOITES_BASSINS))
    print("\nGroupes minéraux et lecture agronomique (ILLUSTRATION) :")
    for minerai, info in MINERAUX_LECTURE.items():
        print("  %-12s %-22s CEC %-22s %s" % (
            minerai, info["famille"], info["cec"], info["lecture"][:60]))
    print("\nRègles absolues : données publiques NASA uniquement, aucun paramètre "
          "VDE versionné, lecture agronomique jamais une prescription — "
          "la qualification reste le monopole des FAT/SAT sur machines réelles.")
    return 0


def _ecrire_cache(nom, donnees):
    os.makedirs(DOSSIER_CACHE, exist_ok=True)
    chemin = os.path.join(DOSSIER_CACHE, nom)
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=1)
        f.write("\n")


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    mode, argument = argv[1], (argv[2] if len(argv) > 2 else None)
    table = {"inventaire": lambda: inventaire(),
             "reassembler": lambda: reassembler(argument),
             "extraire": lambda: extraire(argument),
             "croiser": lambda: croiser(),
             "l3-bassins": lambda: l3_bassins(),
             "sommaire": lambda: sommaire(argument)}
    if mode not in table:
        print("mode inconnu : %s — modes : %s" % (mode, ", ".join(table)))
        return 1
    return table[mode]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
