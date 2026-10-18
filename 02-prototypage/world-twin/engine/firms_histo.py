#!/usr/bin/env python3
"""Couche P2.4 — FIRMS historique multi-saison du Trio Nomad v1 (v0.8).

Cartographie pluriannuelle du brûlage dans les dix bassins : résumés
annuels par pays de NASA FIRMS (CSV publics, sans MAP_KEY), filtrés par
les boîtes de engine/firms.py, agrégés par mois sur cinq saisons.

DONNÉES :
- NASA FIRMS « Country Yearly Summary », domaine public, un CSV par
  capteur, pays et année — https://firms.modaps.eosdis.nasa.gov/country/
  (fichiers listés dans /data/country/yearly_summary_files.txt, constaté
  le 18/10/2026 ; aucun secret requis, contrairement à l'API du jour).
- Capteur par défaut : VIIRS S-NPP 375 m (série continue depuis 2012,
  meilleure détection des petits feux agricoles que MODIS 1 km).
- Les fichiers téléchargés sont mis en cache local (cache-firms-histo/,
  jamais versionné) ; seules les agrégations par bassin sont manipulées.

RÈGLES :
- Une détection de feu n'est pas une preuve de brûlage agricole : le
  profil saisonnier multi-saison croise la cause probable avec les
  calendriers culturaux (v0.7) et la réglementation (v0.6). Le verdict
  de cause reste une INFÉRENCE, toujours étiquetée.
- Les sources statiques (type 1 : torchères, volcans) sont exclues des
  verdicts et comptées à part — un bassin pétrolier ne doit pas être
  lu comme un bassin de brûlage.
- Aucune valeur calibrée ; aucune clé ; monde.py n'est PAS modifié —
  les mois de brûlage récurrent hors fenêtres sont étiquetés
  À SOURCER (gisement, ratio, volumes avant toute ingestion).

Lancement :

    python3 engine/firms_histo.py                 # sommaire des dix bassins
    python3 engine/firms_histo.py camargue        # fiche d'un bassin
    python3 engine/firms_histo.py fr-rhone        # fiche d'un hub (ses bassins)
    python3 engine/firms_histo.py croisement       # croisement des fenêtres monde.py

Options : --annees DEBUT FIN (défaut 2021-2025, cinq saisons complètes),
--capteur viirs-snpp|viirs-jpss1|modis (défaut viirs-snpp),
--sans-telechargement (cache local uniquement).

Premier run : téléchargement d'environ 100 Mo (six pays, cinq saisons,
VIIRS S-NPP — l'essentiel vient d'Argentine) ; les runs suivants lisent
le cache. verifier_couverture() contrôle les bassins au lancement.
"""

import csv
import os
import sys
import urllib.request

# Le module vit dans engine/ ; les voisins (firms, monde) aussi.
try:
    import firms
    import monde
except ImportError:  # exécution depuis la racine world-twin
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
    import firms
    import monde

DOSSIER = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."))
DOSSIER_CACHE = os.path.join(DOSSIER, "cache-firms-histo")
URL_BASE = "https://firms.modaps.eosdis.nasa.gov/data/country/"

ETIQUETTE = "DONNÉES RÉELLES (NASA FIRMS)"
ETIQUETTE_INFERENCE = "INFÉRENCE (cause probable, à croiser)"
ETIQUETTE_A_SOURCER = "À SOURCER"

ANNEES_DEFAUT = (2021, 2022, 2023, 2024, 2025)
CAPTEUR_DEFAUT = "viirs-snpp"
DATE_EXTRACTION = "18/10/2026"

# Capteurs disponibles dans les résumés annuels par pays (constaté le
# 18/10/2026) ; premiere_annee = première saison complète disponible.
CAPTEURS = {
    "viirs-snpp": {
        "produit": "VIIRS S-NPP 375 m (VNP14IMGTDL)",
        "premiere_annee": 2012,
    },
    "viirs-jpss1": {
        "produit": "VIIRS NOAA-20 / JPSS-1 375 m (VJ114IMGTDL)",
        "premiere_annee": 2018,
    },
    "modis": {
        "produit": "MODIS C6.1 Terra/Aqua 1 km (MCD14DL)",
        "premiere_annee": 2000,
    },
}

# Pays des résumés annuels FIRMS couvrant chaque bassin (noms exacts des
# fichiers : viirs-snpp_2025_Switzerland.csv, etc.).
PAYS_PAR_BASSIN = {
    "vallee-du-rhone": "France",
    "camargue": "France",
    "perigord": "France",
    "sud-ouest": "France",
    "suisse-leman": "Switzerland",
    "italie-puglia": "Italy",
    "espagne-extremadure": "Spain",
    "argentine-cuyo": "Argentina",
    "argentine-misiones": "Argentina",
    "maroc-atlas": "Morocco",
}

# Seuils de récurrence (proportion d'années de la période où le mois
# porte au moins une détection) — ILLUSTRATION de lecture, documentée.
SEUIL_RECURRENT = 0.80   # présent dans au moins 80 % des saisons
SEUIL_OCCASIONNEL = 0.40  # présent dans au moins 40 % des saisons

# Filtre de quasi-permanence : une cellule de 0,01 degré (environ 1 km)
# portant des détections au moins SEUIL_MOIS_PERMANENCE mois sur 12 est
# une source FIXE (torchière industrielle, décharge, volcan) — jamais
# un brûlage agricole saisonnier. Ces détections sont exclues des
# verdicts et comptées à part (« sources quasi-permanentes »). Sans
# ce filtre, la boîte camargue (corridor de Fos-sur-Mer) et les
# agglomérations (Mendoza, Fès) écrasent le signal saisonnier.
SEUIL_MOIS_PERMANENCE = 9

_memoire = {}


def verifier_couverture():
    """Contrôle que chaque bassin a son pays et que monde.py est couvert.

    Retourne la liste des problèmes (vide = OK).
    """
    problemes = []
    for bassin in firms.BOITES_BASSINS:
        if bassin not in PAYS_PAR_BASSIN:
            problemes.append("bassin sans pays : %s" % bassin)
    for hub_id, hub in monde.HUBS_MONDE.items():
        for biomasse, fiche in hub["biomasses"].items():
            b = fiche["bassin"]
            if b not in PAYS_PAR_BASSIN:
                problemes.append(
                    "hub %s, biomasse %s : bassin non couvert %s"
                    % (hub_id, biomasse, b))
    return problemes


def fichier_cache(annee, pays, capteur):
    return os.path.join(
        DOSSIER_CACHE, "%s_%d_%s.csv" % (capteur, annee, pays))


def telecharger(annee, pays, capteur):
    """Télécharge (ou reprend du cache) le résumé annuel d'un pays.

    Retourne le chemin du fichier, ou None en cas d'échec.
    """
    chemin = fichier_cache(annee, pays, capteur)
    if os.path.exists(chemin) and os.path.getsize(chemin) > 0:
        return chemin
    url = URL_BASE + "%s_%d_%s.csv" % (capteur, annee, pays)
    os.makedirs(DOSSIER_CACHE, exist_ok=True)
    try:
        with urllib.request.urlopen(url, timeout=180) as reponse:
            donnees = reponse.read()
    except Exception:
        return None
    texte = donnees.decode("utf-8", errors="replace")
    if not texte.startswith("latitude"):
        return None  # page d'erreur ou fichier absent
    with open(chemin, "w", encoding="utf-8", newline="\n") as f:
        f.write(texte)
    return chemin


def _iter_points(chemin, boite):
    """Itère les détections d'un CSV FIRMS dans une boîte (ouest, sud, est, nord).

    Rend (annee, mois, frp, type, lat, lon) ; type converti en entier si
    possible. Les positions servent au filtre de quasi-permanence.
    """
    ouest, sud, est, nord = boite
    with open(chemin, encoding="utf-8") as f:
        for ligne in csv.DictReader(f):
            try:
                lat = float(ligne["latitude"])
                lon = float(ligne["longitude"])
            except (KeyError, ValueError):
                continue
            if not (sud <= lat <= nord and ouest <= lon <= est):
                continue
            date = (ligne.get("acq_date") or "")[:10]
            morceaux = date.split("-")
            if len(morceaux) != 3:
                continue
            annee, mois = int(morceaux[0]), int(morceaux[1])
            frp_brut = (ligne.get("frp") or "").strip()
            try:
                frp = float(frp_brut)
            except ValueError:
                frp = 0.0
            type_brut = (ligne.get("type") or "").strip()
            try:
                type_feu = int(type_brut)
            except ValueError:
                type_feu = None
            yield annee, mois, frp, type_feu, lat, lon


def saisonnalite(bassin, annees=ANNEES_DEFAUT, capteur=CAPTEUR_DEFAUT,
                 telechargement=True):
    """Agrégat pluriannuel du brûlage d'un bassin, étiqueté RÉEL.

    Retourne None si les fichiers restent inaccessibles (réseau coupé
    et cache absent). Structure :

    {bassin, source, capteur, annees, pays,
     mois: {1..12: {nb, frp_mw, nb_par_annee, nb_statiques, verdict}},
     total, frp_mw, total_statiques, nb_quasi_permanentes,
     cellules_quasi_permanentes, mois_recurrents}
    """
    cle_memoire = (bassin, tuple(annees), capteur)
    if cle_memoire in _memoire:
        return _memoire[cle_memoire]
    if bassin not in firms.BOITES_BASSINS:
        return None
    pays = PAYS_PAR_BASSIN[bassin]
    boite = firms.BOITES_BASSINS[bassin]
    nb_saisons = len(annees)
    mois = {m: {"nb": 0, "frp_mw": 0.0, "nb_par_annee": {},
                "nb_statiques": 0} for m in range(1, 13)}
    # Passe 1 : collecte en mémoire (détections dans la boîte seulement).
    points = []
    dispo = 0
    for annee in annees:
        if telechargement:
            chemin = telecharger(annee, pays, capteur)
        else:
            chemin = fichier_cache(annee, pays, capteur)
            if not (chemin and os.path.exists(chemin)):
                chemin = None
        if not chemin:
            continue
        dispo += 1
        for an_date, m, frp, type_feu, lat, lon in _iter_points(chemin, boite):
            if an_date != annee:
                continue  # garde-fou : le fichier est bien annuel
            if type_feu == 1:
                mois[m]["nb_statiques"] += 1
                continue
            cellule = (int(lat // 0.01), int(lon // 0.01))
            points.append((an_date, m, frp, cellule))
    if dispo == 0:
        return None
    # Passe 2 : filtre de quasi-permanence — une cellule de 0,01 degré
    # (environ 1 km) active au moins SEUIL_MOIS_PERMANENCE mois sur 12
    # est une source FIXE (torchière, décharge, industrie), jamais un
    # brûlage agricole saisonnier.
    mois_par_cellule = {}
    for _, m, _, cellule in points:
        mois_par_cellule.setdefault(cellule, set()).add(m)
    quasi_permanentes = {
        cellule for cellule, mois_vus in mois_par_cellule.items()
        if len(mois_vus) >= SEUIL_MOIS_PERMANENCE}
    nb_quasi_permanentes = 0
    for an_date, m, frp, cellule in points:
        if cellule in quasi_permanentes:
            nb_quasi_permanentes += 1
            continue
        case = mois[m]
        case["nb"] += 1
        case["frp_mw"] += frp
        case["nb_par_annee"][an_date] = case["nb_par_annee"].get(an_date, 0) + 1
    total = sum(case["nb"] for case in mois.values())
    total_statiques = sum(case["nb_statiques"] for case in mois.values())
    mois_recurrents = []
    for m, case in mois.items():
        annees_touchees = len(case["nb_par_annee"])
        if total == 0 and total_statiques == 0:
            case["verdict"] = "ABSENT"
            continue
        proportion = annees_touchees / float(nb_saisons)
        if proportion >= SEUIL_RECURRENT:
            case["verdict"] = "RÉCURRENT"
            mois_recurrents.append(m)
        elif proportion >= SEUIL_OCCASIONNEL:
            case["verdict"] = "OCCASIONNEL"
        elif annees_touchees >= 1:
            case["verdict"] = "RARE"
        else:
            case["verdict"] = "ABSENT"
    resultat = {
        "bassin": bassin,
        "pays": pays,
        "source": "NASA FIRMS — %s, résumés annuels par pays" % capteur,
        "etiquette": ETIQUETTE,
        "capteur": capteur,
        "annees": list(annees),
        "saisons_disponibles": dispo,
        "mois": mois,
        "total": total,
        "frp_mw": round(sum(case["frp_mw"] for case in mois.values()), 1),
        "total_statiques": total_statiques,
        "nb_quasi_permanentes": nb_quasi_permanentes,
        "cellules_quasi_permanentes": len(quasi_permanentes),
        "mois_recurrents": mois_recurrents,
    }
    _memoire[cle_memoire] = resultat
    return resultat


def _bassins_du_hub(hub_id):
    """Bassins d'un hub monde.py, ordre stable, sans doublon."""
    if hub_id not in monde.HUBS_MONDE:
        return None
    vus = []
    for fiche in monde.HUBS_MONDE[hub_id]["biomasses"].values():
        b = fiche["bassin"]
        if b not in vus:
            vus.append(b)
    return vus


def croisement(annees=ANNEES_DEFAUT, capteur=CAPTEUR_DEFAUT):
    """Croise le brûlage pluriannuel réel avec les fenêtres monde.py.

    Pour chaque biomasse de chaque hub : verdict de la fenêtre et mois
    de brûlage récurrent HORS fenêtre (étiquetés À SOURCER — jamais
    ingérés dans monde.py sans sourcing complet).
    """
    lignes = []
    for hub_id, hub in monde.HUBS_MONDE.items():
        for biomasse, fiche in hub["biomasses"].items():
            bassin = fiche["bassin"]
            agg = saisonnalite(bassin, annees, capteur)
            if agg is None:
                lignes.append({
                    "hub": hub_id, "biomasse": biomasse, "bassin": bassin,
                    "fenetre": list(fiche["fenetre_operation"]),
                    "verdict": "DONNÉES INDISPONIBLES (réseau/cache absent)",
                    "mois_hors_fenetre": [],
                })
                continue
            fenetre = list(fiche["fenetre_operation"])
            verdicts_fenetre = {m: agg["mois"][m]["verdict"] for m in fenetre}
            recurrents_dans = [m for m in fenetre
                               if verdicts_fenetre[m] == "RÉCURRENT"]
            recurrents_hors = [m for m in agg["mois_recurrents"]
                              if m not in fenetre]
            # Part des détections du bassin tombant dans la fenêtre :
            # un mois peut être RÉCURRENT en présence et négligeable en
            # volume (feux d'ordure ponctuels) — le verdict doit le dire.
            part_fenetre_pct = 0.0
            if agg["total"]:
                nb_fenetre = sum(agg["mois"][m]["nb"] for m in fenetre)
                part_fenetre_pct = round(100.0 * nb_fenetre / agg["total"], 1)
            moitie = max(1, len(fenetre) // 2)
            if recurrents_dans and len(recurrents_dans) >= moitie \
                    and part_fenetre_pct >= 10.0:
                verdict = "FENÊTRE ALIGNÉE SUR UN BRÛLAGE RÉCURRENT"
            elif recurrents_dans and len(recurrents_dans) >= moitie:
                verdict = ("BRÛLAGE RÉCURRENT MAIS MARGINAL DANS LA FENÊTRE "
                           "(%.1f %% des détections du bassin)" % part_fenetre_pct)
            elif recurrents_dans:
                verdict = "CHEVAUCHEMENT PARTIEL (brûlage récurrent sur un bord de fenêtre)"
            elif any(v in ("OCCASIONNEL", "RARE") for v in verdicts_fenetre.values()):
                verdict = "BRÛLAGE FAIBLE DANS LA FENÊTRE"
            else:
                verdict = "AUCUN BRÛLAGE DÉTECTÉ DANS LA FENÊTRE"
            lignes.append({
                "hub": hub_id,
                "biomasse": biomasse,
                "bassin": bassin,
                "fenetre": fenetre,
                "verdicts_mois": verdicts_fenetre,
                "part_fenetre_pct": part_fenetre_pct,
                "verdict": verdict,
                "mois_hors_fenetre": recurrents_hors,
                "etiquette_hors_fenetre": (
                    ETIQUETTE_A_SOURCER if recurrents_hors else None),
            })
    return lignes


def _barres(nb, maxi):
    """Barre ASCII proportionnelle pour la console (lecture rapide)."""
    if maxi <= 0:
        return ""
    longueur = int(round(28.0 * nb / maxi))
    return "#" * longueur


def afficher_sommaire(annees, capteur):
    print("FIRMS historique multi-saison — sommaire des dix bassins")
    print("Source : %s — %s" % (ETIQUETTE, CAPTEURS[capteur]["produit"]))
    print("Saisons : %d-%d (%d saisons complètes), extrait le %s"
          % (annees[0], annees[-1], len(annees), DATE_EXTRACTION))
    print()
    resultats = {}
    for bassin in firms.BOITES_BASSINS:
        resultats[bassin] = saisonnalite(bassin, annees, capteur)
    # Échelle commune : le mois le plus chargé de tous les bassins.
    maxi = max(
        (r["mois"][m]["nb"] for r in resultats.values() if r
         for m in range(1, 13)), default=0)
    for bassin, agg in resultats.items():
        if agg is None:
            print("%-22s DONNÉES INDISPONIBLES" % bassin)
            continue
        top = sorted(agg["mois_recurrents"])
        print("%-22s %6d détections  FRP %8.1f MW  récurrents : %s%s"
              % (bassin, agg["total"], agg["frp_mw"],
                 " ".join("%d" % m for m in top) if top else "—",
                 ("  (exclues : %d quasi-permanentes)"
                  % agg["nb_quasi_permanentes"])
                 if agg["nb_quasi_permanentes"] else ""))
        ligne_barres = " " * 22
        for m in range(1, 13):
            ligne_barres += "%2d %-28s" % (m, _barres(agg["mois"][m]["nb"], maxi))
        print(ligne_barres)


def afficher_fiche_bassin(bassin, agg):
    annees = agg["annees"]
    print("=" * 72)
    print("Bassin : %s (%s)" % (bassin, agg["pays"]))
    print("Source : %s — %s" % (agg["etiquette"], CAPTEURS[agg["capteur"]]["produit"]))
    print("Saisons : %s (%d disponibles) — détections retenues : %d "
          "(exclues : %d sources statiques, %d quasi-permanentes sur %d cellules fixes)"
          % ("-".join(str(a) for a in (annees[0], annees[-1])),
             agg["saisons_disponibles"], agg["total"], agg["total_statiques"],
             agg["nb_quasi_permanentes"], agg["cellules_quasi_permanentes"]))
    print("FRP cumulée : %.1f MW" % agg["frp_mw"])
    print()
    entete = "mois | " + " | ".join("%d" % a for a in annees)
    print(entete + " |  total |  part % |   FRP MW | verdict")
    print("-" * len(entete))
    for m in range(1, 13):
        case = agg["mois"][m]
        cases = " | ".join(
            "%5d" % case["nb_par_annee"].get(a, 0) for a in annees)
        part = (100.0 * case["nb"] / agg["total"]) if agg["total"] else 0.0
        print("%4d | %s | %6d | %6.1f | %7.1f | %s"
              % (m, cases, case["nb"], part, case["frp_mw"], case["verdict"]))
    recurrents = " ".join(str(m) for m in agg["mois_recurrents"])
    print()
    print("Mois de brûlage récurrent : %s"
          % (recurrents if recurrents else "aucun"))
    print("Lecture : %s — une détection n'est pas une preuve de"
          " brûlage agricole." % ETIQUETTE_INFERENCE)


def afficher_fiche(cible, annees, capteur):
    if cible in firms.BOITES_BASSINS:
        agg = saisonnalite(cible, annees, capteur)
        if agg is None:
            print("DONNÉES INDISPONIBLES pour %s (réseau/cache absent)." % cible)
            return 1
        afficher_fiche_bassin(cible, agg)
        return 0
    bassins = _bassins_du_hub(cible)
    if bassins is None:
        print("Cible inconnue : %s (bassin de engine/firms.py ou hub de"
              " engine/monde.py attendu)." % cible)
        return 1
    for i, bassin in enumerate(bassins):
        if i:
            print()
        agg = saisonnalite(bassin, annees, capteur)
        if agg is None:
            print("Bassin %s : DONNÉES INDISPONIBLES" % bassin)
            continue
        afficher_fiche_bassin(bassin, agg)
    return 0


def afficher_croisement(annees, capteur):
    print("Croisement FIRMS historique × fenêtres engine/monde.py")
    print("Source : %s — saisons %d-%d — %s"
          % (ETIQUETTE, annees[0], annees[-1],
             CAPTEURS[capteur]["produit"]))
    print()
    for ligne in croisement(annees, capteur):
        print("%s / %s (bassin %s)" % (ligne["hub"], ligne["biomasse"],
                                       ligne["bassin"]))
        print("  fenêtre %s -> %s"
              % (ligne["fenetre"], ligne["verdict"]))
        if ligne.get("verdicts_mois"):
            detail = ", ".join(
                "%d: %s" % (m, v) for m, v in ligne["verdicts_mois"].items())
            print("  par mois : %s" % detail)
        if ligne.get("part_fenetre_pct") is not None:
            print("  part des détections dans la fenêtre : %.1f %%"
                  % ligne["part_fenetre_pct"])
        if ligne["mois_hors_fenetre"]:
            print("  brûlage récurrent HORS fenêtre : %s — %s"
                  % (ligne["mois_hors_fenetre"], ETIQUETTE_A_SOURCER))
        print()


def main(argv):
    problemes = verifier_couverture()
    if problemes:
        print("ERREUR DE COUVERTURE :")
        for p in problemes:
            print(" - %s" % p)
        return 1
    annees = list(ANNEES_DEFAUT)
    capteur = CAPTEUR_DEFAUT
    telechargement = True
    cible = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--annees" and i + 2 < len(argv):
            annees = list(range(int(argv[i + 1]), int(argv[i + 2]) + 1))
            i += 3
            continue
        if a == "--capteur" and i + 1 < len(argv):
            capteur = argv[i + 1]
            i += 2
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
    if capteur not in CAPTEURS:
        print("Capteur inconnu : %s (attendus : %s)"
              % (capteur, ", ".join(CAPTEURS)))
        return 1
    if annees[0] < CAPTEURS[capteur]["premiere_annee"]:
        print("Année %d antérieure à la couverture du capteur %s (%d)."
              % (annees[0], capteur, CAPTEURS[capteur]["premiere_annee"]))
        return 1
    if cible == "croisement":
        afficher_croisement(annees, capteur)
        return 0
    if cible is None:
        afficher_sommaire(annees, capteur)
        return 0
    return afficher_fiche(cible, annees, capteur)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
