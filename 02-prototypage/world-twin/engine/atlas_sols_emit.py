"""Atlas des sols — NASA EMIT (V1.5, 27/10/2026).

Réassemble, inventorie et extrait les granules NASA EMIT du dossier
data/emit/, puis les rattache aux dix bassins de la flotte P2 et en
donne la lecture agronomique (argiles 1:1 vs 2:1, carbonates, oxydes
de fer, gypsum) — socle « Soil Sciences » de la couche 1.

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
VDE (Vignite Decision Engine), aucune clé, aucun secret.

DÉPENDANCES : bibliothèque standard pour tout, sauf l'extraction des
fichiers .nc (NetCDF-4 / HDF5) qui requiert localement h5py, netCDF4
ou xarray (au choix). Sans lecteur : modes inventaire/reassembler/
sommaire fonctionnent, extraire s'arrête proprement avec la consigne
d'installation.

LANCEMENT :
    python3 engine/atlas_sols_emit.py inventaire
    python3 engine/atlas_sols_emit.py reassembler [GRANULE]
    python3 engine/atlas_sols_emit.py extraire [GRANULE]
    python3 engine/atlas_sols_emit.py croiser
    python3 engine/atlas_sols_emit.py sommaire [BASSIN]
"""

import hashlib
import json
import os
import sys

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
}
GRANULE_L3 = {"fichier": "EMIT_L3_ASA_002.zip",
              "produit": "EMITL3ASA V002 — agrégation mondiale 0,5 degré"}

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


def inventaire():
    """Tailles, empreintes md5 et complétude des granules versionnés."""
    print("Inventaire NASA EMIT — dossier data/emit/ (V1.5)\n")
    if not os.path.isdir(DOSSIER_EMIT):
        print("  dossier data/emit/ introuvable — lancer la vague v1.5 (déplacement des .part)")
        return 1
    lignes = []
    for cart, meta in sorted(GRANULES_L2B.items()):
        print("L2B MIN %s — scène %s" % (cart, meta["scene"]))
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

    L2B MIN : bornes lat/lon de la scène + fractions par groupe minéral.
    Sans cartouche : le sommaire de chaque granule réassemblé.
    Écrit cache-sols/extraire-*.json, jamais versionné.
    """
    module, nom_lecteur = _lecteur()
    if module is None:
        print("aucun lecteur NetCDF-4/HDF5 disponible")
        print("installer au choix : pip install h5py  (ou netCDF4, ou xarray)")
        print("les modes inventaire/reassembler/sommaire restent disponibles")
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
        chemin = os.path.join(DOSSIER_CACHE, meta["fichier"])
        if not os.path.exists(chemin):
            print("%s : absent de cache-sols/ — lancer d'abord : "
                  "python3 engine/atlas_sols_emit.py reassembler %s" % (cart, cart))
            continue
        donnees = {"cartouche": cart, "scene": meta["scene"],
                   "etiquette": ETIQUETTE}
        with h5py.File(chemin, "r") as f:
            donnees["variables"] = sorted(f.keys())
            for groupe in f:
                donnees.setdefault("groupes", {})[groupe.name] = sorted(groupe.keys())
            donnees["bornes"] = _bornes_h5py(f)
        resultats.append(donnees)
        print("extrait : %s (scène %s) — variables : %d" % (
            cart, meta["scene"], len(donnees["variables"])))
    _ecrire_cache("extraire.json", resultats)
    return 0


def _bornes_h5py(f):
    bornes = {}
    for nom in ("lat", "lon", "latitude", "longitude"):
        if nom in f:
            jeu = f[nom][:]
            try:
                borne_min, borne_max = float(jeu.min()), float(jeu.max())
                bornes[nom] = [round(borne_min, 4), round(borne_max, 4)]
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
        return 0
    print("Atlas des sols — NASA EMIT (V1.5, 27/10/2026)\n")
    print("Granules L2B MIN versionnés : %d (cartouches %s)" % (
        len(GRANULES_L2B), ", ".join(sorted(GRANULES_L2B))))
    print("Granule L3 ASA : %s (agrégation mondiale 0,5 degré)" % GRANULE_L3["fichier"])
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
             "sommaire": lambda: sommaire(argument)}
    if mode not in table:
        print("mode inconnu : %s — modes : %s" % (mode, ", ".join(table)))
        return 1
    return table[mode]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
