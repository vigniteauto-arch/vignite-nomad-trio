#!/usr/bin/env python3
"""Couche P2.5 — extraction bulk FAOSTAT multi-pays du Trio Nomad v1 (v0.9).

Séries nationales de production et de surfaces des cultures des sept
hubs (raisin, maïs, riz paddy, noix, olives, feuilles de maté) pour
les six pays de la flotte monde (France, Suisse, Italie, Espagne,
Argentine, Maroc), extraites du bulk officiel FAOSTAT.

DONNÉES :
- FAOSTAT, domaine « Production : Crops and livestock products »,
  fichier normalisé en masse (bulk) — bulks-faostat.fao.org — sans
  clé, contrairement à l'API faostatservices.fao.org. Licence :
  CC BY 4.0 (politique FAO d'open data licensing pour les bases
  statistiques) — diffusion permise avec attribution.
- Version téléchargée : mise à jour FAO du 31/12/2025 (constaté le
  18/10/2026), série 1961-2024 ; le ZIP fait environ 34 Mo et le CSV
  interne environ 545 Mo (le filtre ne garde que nos pays et items).
- Le ZIP et l'extrait filtré sont mis en cache local (cache-faostat-
  bulk/, jamais versionné) ; seules les séries par hub sont manipulées.

RÈGLES :
- monde.py n'est PAS modifié : les gisements nationaux sont des
  REPÈRES documentaires ; toute ingestion d'un gisement régional dans
  monde.py exige son sourcing complet (gisement, ratio, volumes).
- Les ratios de conversion en gisement sont étiquetés SOURCÉ ou
  ILLUSTRATION, à l'identique de l'extraction France v0.1 et de
  l'atlas v0.5 ; ce ne sont jamais des calibrages du moteur.
- La maille FAOSTAT est NATIONALE : les parts régionales restent
  étiquetées À SOURCER quand aucune source régionale croisée n'existe
  (atlas v0.5) — le national encadre, la région décide.

Lancement :

    python3 engine/faostat_bulk.py                 # sommaire des sept hubs
    python3 engine/faostat_bulk.py fr-rhone        # fiche d'un hub
    python3 engine/faostat_bulk.py croisement       # croisement atlas v0.5

Options : --annees DEBUT FIN (défaut 2019-2024, six campagnes),
--sans-telechargement (cache local uniquement).

Premier run : téléchargement d'environ 34 Mo ; les runs suivants
lisent le cache. verifier_couverture() contrôle les hubs, pays et
biomasses de monde.py au lancement.
"""

import csv
import os
import sys
import urllib.request
import zipfile

# Le module vit dans engine/ ; les voisins (monde) aussi.
try:
    import monde
except ImportError:  # exécution depuis la racine world-twin
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import monde

DOSSIER = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."))
DOSSIER_CACHE = os.path.join(DOSSIER, "cache-faostat-bulk")

URL_BULK = ("https://bulks-faostat.fao.org/production/"
            "Production_Crops_Livestock_E_All_Data_(Normalized).zip")
MEMBRE_CSV = "Production_Crops_Livestock_E_All_Data_(Normalized).csv"

ETIQUETTE = "DONNÉES RÉELLES (FAOSTAT bulk, licence CC BY 4.0)"
ETIQUETTE_ILLUSTRATION = "ILLUSTRATION (ratio documentaire, jamais un calibrage)"
ETIQUETTE_A_SOURCER = "À SOURCER"
DATE_EXTRACTION = "18/10/2026"
VERSION_BULK = "mise à jour FAO du 31/12/2025"

ANNEES_DEFAUT = (2019, 2020, 2021, 2022, 2023, 2024)
ELEMENTS = ("Area harvested", "Production")

# monde.py nomme les pays en français ; le bulk FAOSTAT les nomme en
# anglais (seul « France » coïncide) — la traduction est explicite,
# jamais implicite : un pays non mappé lève une erreur de couverture.
PAYS_FAOSTAT = {
    "France": "France",
    "Suisse": "Switzerland",
    "Italie": "Italy",
    "Espagne": "Spain",
    "Argentine": "Argentina",
    "Maroc": "Morocco",
}

# Culture FAOSTAT portée par chaque biomasse de monde.py. « Walnuts, in
# shell » porte une virgule dans le CSV du bulk (le fichier des codes
# écrit « Walnuts; in shell » — incohérence FAOSTAT constatée le
# 18/10/2026, source d'un piège de filtrage documenté ici).
CULTURES_BIOMASSES = {
    "sarments-vigne": "Grapes",
    "marc-raisin": "Grapes",
    "restos-poda": "Grapes",
    "mais-rdm": "Maize (corn)",
    "paille-riz": "Rice",
    "coques-noix": "Walnuts, in shell",
    "grignons-olive": "Olives",
    "yerba-mate": "Maté leaves",
}

# Ratios de conversion en gisement (documentaires, étiquetés). Chaque
# entrée : base (élément FAOSTAT lu), facteur (min, max) appliqué à la
# dernière année demandée, étiquette de sourcing. À l'identique de
# l'extraction France v0.1 (17/10/2026) et de l'atlas v0.5.
RATIOS_GISEMENTS = {
    "sarments-vigne": {
        "libelle": "sarments de vigne",
        "base": "Area harvested",
        "facteur": (0.8, 1.1),        # t MS/ha/an
        "etiquette": "SOURCÉ (LIFE 3.0 ≈ 0,8 t/ha/an ; méta-analyse ≈ 1,08 t/ha)",
    },
    "restos-poda": {
        "libelle": "restes de taille de vigne",
        "base": "Area harvested",
        "facteur": (0.8, 1.1),        # t MS/ha/an — même ratio sarments
        "part_region": (0.70, 0.75),  # part Mendoza du vignoble argentin
        "etiquette": ("SOURCÉ pour le ratio ; part Mendoza ILLUSTRATION "
                      "(atlas v0.5 : Mendoza 70-75 % du vignoble argentin)"),
    },
    "marc-raisin": {
        "libelle": "marc de raisin",
        "base": "Production",
        "facteur": (0.10, 0.30),     # part de la vendange
        "etiquette": "SOURCÉ (revues grape pomace : 10-30 % de la vendange)",
    },
    "mais-rdm": {
        "libelle": "rafles de maïs",
        "base": "Production",
        "facteur": (0.15, 0.20),     # rafles en part du grain
        "etiquette": ("rafles ILLUSTRATION (15-20 % du grain ; stover "
                      "total ≈ masse du grain, SOURCÉ MSU Extension)"),
    },
    "paille-riz": {
        "libelle": "paille de riz",
        "base": "Production",
        "facteur": (1.0, 1.5),       # × paddy
        "etiquette": "ILLUSTRATION (paille = 1,0-1,5 × paddy)",
    },
    "coques-noix": {
        "libelle": "coques de noix",
        "base": "Production",
        "facteur": (0.50, 0.65),     # part de la masse en coques
        "etiquette": "ILLUSTRATION (coques = 50-65 % de la masse en coques)",
    },
    "grignons-olive": {
        "libelle": "grignons d'olive",
        "base": "Production",
        "facteur": (0.4, 0.6),       # t/t olives triturées
        "etiquette": ("ILLUSTRATION (grignons = 0,4-0,6 t/t triturée, "
                      "atlas v0.5 ; hypothèse : olives triturées ≈ "
                      "production, olives de table non soustraites)"),
    },
    "yerba-mate": {
        "libelle": "feuille de yerba mate",
        "base": "Production",
        "facteur": (1.0, 1.0),       # la feuille EST la biomasse
        "etiquette": ("GISSEMENT DIRECT (la feuille de maté est la "
                      "biomasse du hub, pas un résidu)"),
    },
}

# Ancres de croisement avec l'atlas v0.5 (données publiques étiquetées,
# hub par hub). Chaque ancre : (libellé, valeur, unité, source, clef).
# clef = "surface:CULTURE:ANNEE" (compare à Area harvested),
# "production:CULTURE:ANNEE" (compare à Production),
# "part-surface:CULTURE:ANNEE" (part régionale de la surface nationale),
# "ratio-huile:Olives:ANNEE" (rendement huile implicite, l'atlas donnant
# l'huile et FAOSTAT les olives — métriques différentes, arithmétique
# quand même).
ANCRES_ATLAS = {
    "fr-rhone": [
        ("Raisin 2024 — extraction France v0.1, même bulk",
         4747450, "t", "FAOSTAT bulk (v0.1, 17/10/2026)",
         "production:Grapes:2024"),
        ("Maïs grain 2024 — extraction France v0.1",
         14670620, "t", "FAOSTAT bulk (v0.1, 17/10/2026)",
         "production:Maize (corn):2024"),
        ("Riz paddy 2024 — extraction France v0.1",
         71960, "t", "FAOSTAT bulk (v0.1, 17/10/2026)",
         "production:Rice:2024"),
        ("Noix en coques 2024 — extraction France v0.1",
         27710, "t", "FAOSTAT bulk (v0.1, 17/10/2026)",
         "production:Walnuts, in shell:2024"),
    ],
    "ch-leman": [
        ("Surfaces viticoles suisses (OFAG, atlas v0.5)",
         14793, "ha", "OFAG (atlas v0.5)", "surface:Grapes:2024"),
    ],
    "it-puglia": [
        ("Huile d'olive Italie 2022 (ISMEA/Agea, atlas v0.5)",
         241000, "t", "ISMEA/Agea (atlas v0.5)", "ratio-huile:Olives:2022"),
    ],
    "es-extremadura": [
        ("Huile d'olive prévue Espagne 2023/24 (MAPA, atlas v0.5)",
         765300, "t", "MAPA (atlas v0.5)", "ratio-huile:Olives:2023"),
        ("Oliveraie Estrémadure > 300 kha (atlas v0.5)",
         300000, "ha", "atlas v0.5 (DOE/MAPA)", "part-surface:Olives:2024"),
    ],
    "ar-cuyo": [
        ("Vignes Mendoza 2024 (atlas v0.5, INV)",
         145393, "ha", "INV Mendoza (atlas v0.5)",
         "part-surface:Grapes:2024"),
    ],
    "ar-misiones": [
        ("Yerba mate plantée INYM ≈ 210 kha (atlas v0.5, 87 % Misiones)",
         210000, "ha", "INYM (atlas v0.5)", "surface:Maté leaves:2024"),
        ("Feuille verte yerba ≈ 880 kt/an (INYM ~2020, atlas v0.5)",
         880000, "t", "INYM (atlas v0.5)", "production:Maté leaves:2024"),
    ],
    "ma-atlas": [
        ("Olives Maroc 2021/22 ≈ 1,968 Mt (atlas v0.5)",
         1968111, "t", "MAPM/FAOSTAT (atlas v0.5)",
         "production:Olives:2022"),
        ("Olives Maroc 2023/24 ≈ 1,072 Mt (atlas v0.5)",
         1072000, "t", "MAPM (atlas v0.5)", "production:Olives:2024"),
        ("Oliveraie Fès-Meknès 320 kha > 32 % national (atlas v0.5)",
         320000, "ha", "MAPM (atlas v0.5)", "part-surface:Olives:2024"),
    ],
}


def pays_des_hubs():
    """Les six pays des hubs de monde.py, sans doublon, ordre stable."""
    vus = []
    for hub in monde.HUBS_MONDE.values():
        if hub["pays"] not in vus:
            vus.append(hub["pays"])
    return vus


def cultures_des_hubs():
    """Les cultures FAOSTAT couvertes par les biomasses de monde.py."""
    vus = []
    for culture in CULTURES_BIOMASSES.values():
        if culture not in vus:
            vus.append(culture)
    return vus


def telecharger_et_extraire():
    """Télécharge le bulk (si besoin) et écrit l'extrait filtré en cache.

    L'extrait garde TOUT l'historique (1961-2024) de nos six pays, six
    cultures et deux éléments : les options --annees filtrent ensuite
    en mémoire, sans nouveau téléchargement.
    """
    os.makedirs(DOSSIER_CACHE, exist_ok=True)
    chemin_zip = os.path.join(DOSSIER_CACHE, "bulk.zip")
    chemin_extrait = os.path.join(DOSSIER_CACHE, "extrait-hubs.csv")
    if not os.path.exists(chemin_zip):
        print(">> Téléchargement du bulk FAOSTAT (environ 34 Mo)...")
        urllib.request.urlretrieve(URL_BULK, chemin_zip)
    pays = set(PAYS_FAOSTAT.values())
    cultures = set(cultures_des_hubs())
    elements = set(ELEMENTS)
    lignes = 0
    with zipfile.ZipFile(chemin_zip) as archive:
        with archive.open(MEMBRE_CSV) as brut:
            lecteur = csv.reader(
                (ligne.decode("utf-8") for ligne in brut))
            entetes = next(lecteur)
            with open(chemin_extrait, "w", encoding="utf-8",
                      newline="") as sortie:
                ecrivain = csv.writer(sortie)
                ecrivain.writerow(entetes)
                for ligne in lecteur:
                    if (ligne[2] in pays and ligne[5] in cultures
                            and ligne[7] in elements):
                        ecrivain.writerow(ligne)
                        lignes += 1
    print(">> Extrait : %d lignes (6 pays, 6 cultures, 2 éléments, "
          "historique complet)." % lignes)
    return chemin_extrait


def charger_donnees(annees):
    """Lit le cache (téléchargé si autorisé) et filtre les années.

    Retour : donnees[pays_faostat][culture][(element, annee)] = (valeur,
    unité, flag) — les clefs de premier niveau sont les noms FAOSTAT.
    Lève FileNotFoundError si le cache est absent et que le
    téléchargement est refusé (--sans-telechargement).
    """
    chemin_extrait = os.path.join(DOSSIER_CACHE, "extrait-hubs.csv")
    if not os.path.exists(chemin_extrait):
        raise FileNotFoundError(
            "cache absent : lancez sans --sans-telechargement "
            "(premier run : téléchargement d'environ 34 Mo)")
    donnees = {}
    debut, fin = min(annees), max(annees)
    with open(chemin_extrait, encoding="utf-8") as f:
        lecteur = csv.reader(f)
        next(lecteur)  # entêtes
        for ligne in lecteur:
            pays, culture = ligne[2], ligne[5]
            element, annee = ligne[7], int(ligne[9])
            if not (debut <= annee <= fin):
                continue
            if ligne[11] == "":  # valeur manquante (flag M)
                continue
            donnees.setdefault(pays, {}).setdefault(culture, {})[
                (element, annee)] = (float(ligne[11]), ligne[10], ligne[12])
    return donnees


def biomasses_du_hub(hub_id):
    """Biomasses de monde.py pour un hub, ordre stable."""
    return list(monde.HUBS_MONDE[hub_id]["biomasses"].keys())


def valeur(donnees, pays, culture, element, annee):
    """Valeur FAOSTAT ou None ; les trous sont explicites, jamais comblés.

    « pays » est le nom français de monde.py, traduit ici vers le nom
    FAOSTAT ; un pays non mappé est une erreur de couverture, jamais un
    zéro silencieux.
    """
    if pays not in PAYS_FAOSTAT:
        raise KeyError("pays non mappé vers FAOSTAT : %s" % pays)
    fiche = donnees.get(PAYS_FAOSTAT[pays], {}).get(culture, {})
    entree = fiche.get((element, annee))
    return entree[0] if entree else None


def gisement_derive(donnees, hub_id, biomasse, annee):
    """Gisement documentaire d'une biomasse sur la dernière année.

    Retour : dict(libelle, base, valeur_base, unite_base, min_t, max_t,
    etiquettes) ou None si la donnée de base manque. Les ratios sont
    documentaires ; « restos-poda » applique en sus la part Mendoza.
    """
    hub = monde.HUBS_MONDE[hub_id]
    pays = hub["pays"]
    culture = CULTURES_BIOMASSES[biomasse]
    ratio = RATIOS_GISEMENTS[biomasse]
    base = valeur(donnees, pays, culture, ratio["base"], annee)
    if base is None:
        return None
    mini = base * ratio["facteur"][0]
    maxi = base * ratio["facteur"][1]
    etiquettes = [ratio["etiquette"]]
    part = ratio.get("part_region")
    if part is not None:
        mini *= part[0]
        maxi *= part[1]
        etiquettes.append(
            "part régionale × %.0f-%.0f %% (ILLUSTRATION, atlas v0.5)"
            % (part[0] * 100, part[1] * 100))
    etiquettes.append("maille NATIONALE — la part régionale de %s reste "
                      "%s (atlas v0.5 pour les ancres régionales)"
                      % (hub["region"], ETIQUETTE_A_SOURCER))
    return {
        "libelle": ratio["libelle"],
        "base": ratio["base"],
        "valeur_base": base,
        "min_t": mini,
        "max_t": maxi,
        "etiquettes": etiquettes,
        "culture": culture,
    }


def afficher_sommaire(donnees, annees):
    """Tableau national par hub : cultures, dernière année, tendance."""
    print("=" * 72)
    print("FAOSTAT BULK MULTI-PAYS — SOMMAIRE DES SEPT HUBS (%s)" % ETIQUETTE)
    print("Bulk %s, extrait le %s ; années %d-%d." % (
        VERSION_BULK, DATE_EXTRACTION, min(annees), max(annees)))
    print("=" * 72)
    for hub_id, hub in monde.HUBS_MONDE.items():
        pays = hub["pays"]
        print("\n%s — %s (%s)" % (hub_id, hub["region"], pays))
        for biomasse in biomasses_du_hub(hub_id):
            culture = CULTURES_BIOMASSES[biomasse]
            prod = [valeur(donnees, pays, culture, "Production", a)
                    for a in annees]
            surf = [valeur(donnees, pays, culture, "Area harvested", a)
                    for a in annees]
            if prod[-1] is None and surf[-1] is None:
                print("  %-14s %-18s AUCUNE DONNÉE — %s"
                      % (biomasse, culture, ETIQUETTE_A_SOURCER))
                continue
            ligne = "  %-14s %-18s" % (biomasse, culture)
            if prod[-1] is not None:
                ligne += " prod %s: %s t" % (annees[-1], _fmt(prod[-1]))
            if surf[-1] is not None:
                ligne += " | surf: %s ha" % _fmt(surf[-1])
            connu = [p for p in prod if p is not None]
            if len(connu) >= 2:
                ligne += " | 5 ans: %s → %s t" % (
                    _fmt(connu[0]), _fmt(connu[-1]))
            print(ligne)
    print("\nMaille NATIONALE partout : les parts régionales (Lavaux, "
          "Puglia, Estrémadure, Cuyo, Misiones, Fès-Meknès) restent "
          "%s — voir croisement." % ETIQUETTE_A_SOURCER)


def afficher_fiche(hub_id, donnees, annees):
    """Fiche d'un hub : séries complètes + gisements dérivés documentés."""
    if hub_id not in monde.HUBS_MONDE:
        print("Hub inconnu : %s (attendus : %s)"
              % (hub_id, ", ".join(monde.HUBS_MONDE)))
        return 1
    hub = monde.HUBS_MONDE[hub_id]
    pays = hub["pays"]
    print("=" * 72)
    print("FICHE %s — %s (%s)" % (hub_id, hub["region"], pays))
    print("%s ; bulk %s, extrait le %s." % (
        ETIQUETTE, VERSION_BULK, DATE_EXTRACTION))
    print("=" * 72)
    for biomasse in biomasses_du_hub(hub_id):
        culture = CULTURES_BIOMASSES[biomasse]
        print("\n%s (culture FAOSTAT : %s)" % (biomasse, culture))
        for element in ELEMENTS:
            serie = [valeur(donnees, pays, culture, element, a)
                     for a in annees]
            if all(v is None for v in serie):
                continue
            print("  %-15s" % element, end="")
            for a, v in zip(annees, serie):
                print(" %s:%s" % (a, _fmt(v) if v is not None else "—"),
                      end="")
            print()
        gisement = gisement_derive(donnees, hub_id, biomasse, annees[-1])
        if gisement is not None:
            print("  gisement dérivé (%s %d) : %s : %s → %s t/an"
                  % (gisement["base"], annees[-1], gisement["libelle"],
                     _fmt(gisement["min_t"]), _fmt(gisement["max_t"])))
            for etiquette in gisement["etiquettes"]:
                print("    - %s" % etiquette)
        else:
            print("  gisement non dérivable : donnée de base absente — %s"
                  % ETIQUETTE_A_SOURCER)
    print()
    return 0


def _verdict(ecart_pct):
    if ecart_pct is None:
        return "NON COMPARABLE DIRECTEMENT"
    if ecart_pct <= 2.0:
        return "IDENTIQUE (écart ≤ 2 %)"
    if ecart_pct <= 10.0:
        return "CONCORDANT (écart ≤ 10 %)"
    if ecart_pct <= 25.0:
        return "CONCORDANT EN ORDRE DE GRANDEUR (écart ≤ 25 %)"
    return "ÉCART DOCUMENTÉ (> 25 %)"


def afficher_croisement(donnees, annees):
    """Croise les séries FAOSTAT avec les ancres régionales de l'atlas v0.5.

    Pour chaque hub : chaque ancre est confrontée à la série nationale ;
    les verdicts d'écart sont tranchés arithmétiquement (part, rendement
    implicite ou delta), jamais à l'œil.
    """
    print("=" * 72)
    print("CROISEMENT FAOSTAT BULK × ATLAS V0.5 (ancres régionales sourcées)")
    print("%s ; bulk %s, extrait le %s ; années %d-%d." % (
        ETIQUETTE, VERSION_BULK, DATE_EXTRACTION,
        min(annees), max(annees)))
    print("=" * 72)
    for hub_id, hub in monde.HUBS_MONDE.items():
        pays = hub["pays"]
        print("\n%s — %s (%s)" % (hub_id, hub["region"], pays))
        for libelle, valeur_ancre, unite, source, clef in ANCRES_ATLAS[
                hub_id]:
            print("  ancre : %s" % libelle)
            print("    atlas v0.5 : %s %s (%s)" % (
                _fmt(valeur_ancre), unite, source))
            morceaux = clef.split(":")
            element = morceaux[0]
            culture, annee = morceaux[1], int(morceaux[2])
            if element in ("surface", "production"):
                elem = ("Area harvested" if element == "surface"
                        else "Production")
                national = valeur(donnees, pays, culture, elem, annee)
                if national is None:
                    print("    FAOSTAT %d : donnée absente — %s"
                          % (annee, ETIQUETTE_A_SOURCER))
                    continue
                ecart = abs(valeur_ancre - national) / valeur_ancre * 100
                print("    FAOSTAT %d (%s, %s) : %s %s" % (
                    annee, culture, elem, _fmt(national),
                    "ha" if elem == "Area harvested" else "t"))
                print("    verdict : %s (écart %.1f %%)" % (
                    _verdict(ecart), ecart))
            elif element == "part-surface":
                national = valeur(donnees, pays, culture,
                                  "Area harvested", annee)
                if national is None:
                    print("    FAOSTAT %d : surface absente — %s"
                          % (annee, ETIQUETTE_A_SOURCER))
                    continue
                part = valeur_ancre / national * 100
                print("    FAOSTAT %d (%s) : %s ha nationaux ; part "
                      "régionale de l'ancre : %.1f %%" % (
                          annee, culture, _fmt(national), part))
                if part >= 100:
                    print("    verdict : incohérent — à revoir (%s)"
                          % ETIQUETTE_A_SOURCER)
                else:
                    print("    verdict : part régionale cohérente avec "
                          "l'atlas (ordre de grandeur confirmé)")
            elif element == "ratio-huile":
                national = valeur(donnees, pays, culture,
                                  "Production", annee)
                if national is None:
                    print("    FAOSTAT %d : production d'olives absente "
                          "— %s" % (annee, ETIQUETTE_A_SOURCER))
                    continue
                rendement = valeur_ancre / national * 100
                print("    FAOSTAT %d : %s t d'olives ; rendement huile "
                      "implicite : %.1f %%" % (
                          annee, _fmt(national), rendement))
                if 8.0 <= rendement <= 25.0:
                    print("    verdict : COHÉRENT (rendement 8-25 % "
                          "attendu ; olives de table et années basses "
                          "minorant le ratio national)")
                else:
                    print("    verdict : ÉCART DOCUMENTÉ (rendement "
                          "hors fourchette 8-25 %) — %s"
                          % ETIQUETTE_A_SOURCER)
        # gisements nationaux dérivés du hub, dernière année
        print("  gisements nationaux dérivés (%d) :" % annees[-1])
        for biomasse in biomasses_du_hub(hub_id):
            gisement = gisement_derive(donnees, hub_id, biomasse,
                                       annees[-1])
            if gisement is None:
                print("    %-14s donnée de base absente — %s"
                      % (biomasse, ETIQUETTE_A_SOURCER))
                continue
            print("    %-14s %s : %s → %s t/an" % (
                biomasse, gisement["libelle"],
                _fmt(gisement["min_t"]), _fmt(gisement["max_t"])))
    print("\nmonde.py INCHANGÉ : les gisements ci-dessus sont des repères "
          "documentaires ; toute ingestion d'une valeur dans les fenêtres "
          "exige son sourcing complet (gisement, ratio, volumes).")
    return 0


def _fmt(valeur_num):
    """Format franc lisible : séparateur de milliers, sans décimales."""
    return "{:,.0f}".format(valeur_num).replace(",", " ")


def verifier_couverture():
    """Contrôle que chaque hub, pays et biomasse de monde.py est couvert.

    Retourne la liste des problèmes (vide = couverture complète) :
    pays absent de l'extraction, culture sans donnée sur la fenêtre,
    biomasse sans culture connue.
    """
    problemes = []
    for hub_id, hub in monde.HUBS_MONDE.items():
        for biomasse in hub["biomasses"]:
            if biomasse not in CULTURES_BIOMASSES:
                problemes.append(
                    "biomasse %s (hub %s) sans culture FAOSTAT connue"
                    % (biomasse, hub_id))
    return problemes


def main(argv):
    problemes = verifier_couverture()
    if problemes:
        print("ERREUR DE COUVERTURE :")
        for p in problemes:
            print(" - %s" % p)
        return 1
    annees = list(ANNEES_DEFAUT)
    telechargement = True
    cible = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--annees" and i + 2 < len(argv):
            annees = list(range(int(argv[i + 1]), int(argv[i + 2]) + 1))
            i += 3
            continue
        if a == "--sans-telechargement":
            telechargement = False
            i += 1
            continue
        if a == "croisement":
            cible = "croisement"
            i += 1
            continue
        if cible is None:
            cible = a
        i += 1
    try:
        if telechargement and not os.path.exists(
                os.path.join(DOSSIER_CACHE, "extrait-hubs.csv")):
            telecharger_et_extraire()
        donnees = charger_donnees(annees)
    except FileNotFoundError as erreur:
        print("ERREUR : %s" % erreur)
        return 1
    # couverture réelle des données : chaque pays × culture doit avoir
    # au moins une valeur sur la fenêtre demandée
    for hub_id, hub in monde.HUBS_MONDE.items():
        for biomasse in hub["biomasses"]:
            culture = CULTURES_BIOMASSES[biomasse]
            presente = any(
                valeur(donnees, hub["pays"], culture, element, a) is not None
                for element in ELEMENTS for a in annees)
            if not presente:
                print("ERREUR DE COUVERTURE : %s / %s (%s) sans donnée "
                      "sur %d-%d." % (hub_id, biomasse, culture,
                                     annees[0], annees[-1]))
                return 1
    if cible == "croisement":
        return afficher_croisement(donnees, annees)
    if cible is None:
        afficher_sommaire(donnees, annees)
        return 0
    return afficher_fiche(cible, donnees, annees)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
