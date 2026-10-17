#!/usr/bin/env python3
"""Couche 1 — croisement GEOGLAM : calendiers culturaux des 7 hubs (v0.7, 17/10/2026).

Confronte les fenêtres d'opération du moteur (engine/monde.py, étiquetées
ILLUSTRATION) aux calendiers culturaux sous-nationaux GEOGLAM et aux
conditions de campagne des bulletins Crop Monitor for AMIS n° 143 et
CM4EW n° 120 (publiés le 01/10/2026, conditions au 28/09/2026).

Étiquettes :

- DONNÉES RÉELLES : calendrier ou condition issu d'une source citée,
  extraite et croisée le 17/10/2026 ;
- HORS PÉRIMÈTRE : culture pérenne ou pays non couvert par GEOGLAM ;
- À SOURCER : fenêtre candidate, hypothèse à sourcer (gisement, ratio,
  volumes) avant toute entrée dans monde.py.

RÈGLES :
- GEOGLAM ne couvre pas les cultures pérennes (vigne, olivier, noyer,
  yerba mate) : leurs calendriers restent ceux de l'atlas v0.5.
- Les conditions de campagne datent du 28/09/2026 : re-vérifier avant
  tout usage externe.
- Aucune valeur calibrée ; tout résultat de simulation reste
  étiqueté SYNTHÉTIQUE.

Lancement :

    python3 engine/geoglam.py              # sommaire console
    python3 engine/geoglam.py ar-cuyo      # fiche d'un hub

Les identifiants de hubs sont exactement ceux de engine/monde.py ;
verifier_couverture() le contrôle au lancement.
"""

import sys

ETIQUETTE_REEL = "DONNÉES RÉELLES"
ETIQUETTE_HORS_PERIMETRE = "HORS PÉRIMÈTRE"
ETIQUETTE_A_SOURCER = "À SOURCER"
ETIQUETTE_A_VERIFIER = "À VÉRIFIER"

CROISEMENT_GEOGLAM = {
    "fr-rhone": {
        "pays": "France",
        "region_geoglam": "AMIS — Northern / Southern France (vérifiée sur les couches GEOGLAM le 17/10/2026)",
        "calendriers": [
            {"culture": "maïs grain",
             "semis": "avril-mai",
             "recolte": "octobre (5-20 oct. en prévision Arvalis), au plus tard fin octobre, chantiers jusqu'en décembre selon l'année",
             "source": "Arvalis ; La France Agricole",
             "etiquette": ETIQUETTE_REEL,
             "verdict": "fenêtre mais-rdm [10, 11, 12] VALIDÉE — conservée à l'identique dans monde.py"},
            {"culture": "riz (Camargue)",
             "semis": "printemps (hors calendiers AMIS, production mineure)",
             "recolte": "mi-septembre à fin octobre",
             "source": "ABrideCamargue ; Connexion France ; Les Bains Gardians (trois sources concordantes)",
             "etiquette": ETIQUETTE_REEL,
             "verdict": "fenêtre paille-riz [10, 11, 12] VALIDÉE — conservée à l'identique"},
        ],
        "condition_campagne": "AMIS n° 143 (28/09/2026) : déficits de pluie persistants et chaleur dégradent le maïs en Europe de l'Ouest et une partie de l'Europe centrale",
        "hors_perimetre": ["vigne (sarments, marc)", "noyer (coques)"],
        "candidates": [],
    },
    "ch-leman": {
        "pays": "Suisse",
        "region_geoglam": "absente des couches GEOGLAM — ni AMIS ni CM4EW (requête du 17/10/2026)",
        "calendriers": [
            {"culture": "céréales suisses (froment, maïs)",
             "semis": "-",
             "recolte": "-",
             "source": "OFAG, Agroscope — à sourcer si un besoin apparaît",
             "etiquette": ETIQUETTE_A_VERIFIER,
             "verdict": "aucun calendrier GEOGLAM pour ce hub"},
        ],
        "condition_campagne": "non couverte par les bulletins GEOGLAM",
        "hors_perimetre": ["vigne (Lavaux)"],
        "candidates": [],
    },
    "it-puglia": {
        "pays": "Italie",
        "region_geoglam": "AMIS — Italie (une seule région)",
        "calendriers": [
            {"culture": "blé dur",
             "semis": "vers le 20 novembre puis tout décembre",
             "recolte": "de fin mai (vers le 25) à fin juin (Monti Dauni)",
             "source": "Grano Italiano",
             "etiquette": ETIQUETTE_REEL,
             "verdict": "aucune biomasse céréalière dans monde.py pour ce hub"},
        ],
        "condition_campagne": "AMIS n° 143 (28/09/2026) : maïs UE dégradé par la sécheresse en Europe de l'Ouest ; semis du blé dur pugliese tributaire des pluies d'automne",
        "hors_perimetre": ["olivier (grignons)", "vigne (sarments)"],
        "candidates": [
            {"biomasse": "paille-blé-dur", "fenetre": [6, 7],
             "justification": "résidus post-moisson (fin mai-fin juin)",
             "etiquette": ETIQUETTE_A_SOURCER},
        ],
    },
    "es-extremadura": {
        "pays": "Espagne",
        "region_geoglam": "AMIS — Espagne (une seule région)",
        "calendriers": [
            {"culture": "blé dur (Badajoz)",
             "semis": "octobre-décembre (30/60/10 %)",
             "recolte": "juin-juillet (90/10 %)",
             "source": "MAPA, calendario de siembra y recolección 2014-2016",
             "etiquette": ETIQUETTE_REEL,
             "verdict": "aucune biomasse céréalière dans monde.py pour ce hub"},
            {"culture": "orge brassicole (Badajoz)",
             "semis": "octobre-novembre (40/60 %)",
             "recolte": "juin-juillet",
             "source": "MAPA, calendario de siembra y recolección 2014-2016",
             "etiquette": ETIQUETTE_REEL,
             "verdict": "candidate"},
            {"culture": "riz índica et japónica (Badajoz)",
             "semis": "avril-mai (10/90 %)",
             "recolte": "septembre-octobre (70/30 %)",
             "source": "MAPA, calendario de siembra y recolección 2014-2016",
             "etiquette": ETIQUETTE_REEL,
             "verdict": "candidate"},
        ],
        "condition_campagne": "AMIS n° 143 (28/09/2026) : risque de précipitations sous la moyenne sur le nord-ouest de l'Espagne (prévisions deux semaines)",
        "hors_perimetre": ["olivier (grignons)", "vigne (sarments)"],
        "candidates": [
            {"biomasse": "paille-blé-dur", "fenetre": [7, 8],
             "justification": "résidus post-récolte juin-juillet",
             "etiquette": ETIQUETTE_A_SOURCER},
            {"biomasse": "paille-orge", "fenetre": [7, 8],
             "justification": "orge brassicole récoltée juin-juillet (90 % en juillet)",
             "etiquette": ETIQUETTE_A_SOURCER},
            {"biomasse": "paille-riz-guadiana", "fenetre": [10, 11],
             "justification": "riz du Guadiana récolté septembre-octobre",
             "etiquette": ETIQUETTE_A_SOURCER},
        ],
    },
    "ar-cuyo": {
        "pays": "Argentine (Mendoza)",
        "region_geoglam": "AMIS — Western Argentina (une des 12 régions argentines)",
        "calendriers": [
            {"culture": "blé",
             "semis": "juin-août (automne-hiver austral)",
             "recolte": "novembre-décembre (pic en décembre, jusqu'à fin janvier au sud)",
             "source": "Loneralj ; Grain Brokers Australia",
             "etiquette": ETIQUETTE_REEL,
             "verdict": "fenêtre restos-poda [6, 7, 8] : cohérence saisonnière VALIDÉE (taille d'hiver, hors récolte du blé)"},
        ],
        "condition_campagne": "AMIS n° 143 (28/09/2026) : blé argentin favorable, stade principalement végétatif, surface semée en baisse ; outlook précipitations au-dessus de la moyenne et températures en dessous (octobre-décembre) ; El Niño très fort (sept. 2026-janv. 2027)",
        "hors_perimetre": ["vigne (restos de poda)"],
        "candidates": [
            {"biomasse": "paille-blé", "fenetre": [12, 1],
             "justification": "résidus post-récolte du blé (novembre-décembre), enchaînés sur la taille de vigne (juin-août)",
             "etiquette": ETIQUETTE_A_SOURCER},
        ],
    },
    "ar-misiones": {
        "pays": "Argentine (Misiones)",
        "region_geoglam": "AMIS — Northeast Argentina",
        "calendriers": [
            {"culture": "maïs (Argentine)",
             "semis": "septembre-janvier (semis échelonnés)",
             "recolte": "mars-juillet",
             "source": "GeoPard compilant l'USDA FAS",
             "etiquette": ETIQUETTE_REEL,
             "verdict": "aucune culture annuelle dans monde.py pour ce hub"},
        ],
        "condition_campagne": "AMIS n° 143 (28/09/2026) : El Niño présent et se renforçant, très probablement très fort de sept. 2026 à janv. 2027, parmi les plus forts depuis 1950 ; IOD positif oct.-déc. — outlook humide sur la grande région agricole argentine",
        "hors_perimetre": ["yerba mate (pérenne, zafra INYM — atlas v0.5)"],
        "candidates": [
            {"biomasse": "restos-de-maiz", "fenetre": [4, 5, 6, 7],
             "justification": "résidus post-récolte (mars-juillet)",
             "etiquette": ETIQUETTE_A_SOURCER},
        ],
    },
    "ma-atlas": {
        "pays": "Maroc (Meknès)",
        "region_geoglam": "CM4EW — Morocco Northern (une des 6 régions marocaines)",
        "calendriers": [
            {"culture": "blé tendre (winter wheat, région Northern)",
             "semis": "octobre",
             "recolte": "à partir de mai, fin de saison en juillet (région Central voisine : dès avril, fin en juin)",
             "source": "GEOGLAM CM4EW Sub-National Crop Calendars (Zenodo 10.5281/zenodo.10949971), extraction machine du 17/10/2026 — double décodage concordant jours-de-l'année (289/1/121/182/213) et mois littéraux (October/January/May/July/August)",
             "etiquette": ETIQUETTE_REEL,
             "verdict": "aucune culture annuelle dans monde.py pour ce hub"},
        ],
        "condition_campagne": "CM4EW n° 120 (28/09/2026, Moyen-Orient et Afrique du Nord) : préparation des sols de la saison blé 2026/27 en cours, semis à partir d'octobre — fenêtre d'ouverture en cours",
        "hors_perimetre": ["olivier (grignons)"],
        "candidates": [
            {"biomasse": "paille-blé", "fenetre": [5, 6, 7],
             "justification": "résidus post-moisson (fourchette avril-juillet selon rattachement Northern/Central)",
             "etiquette": ETIQUETTE_A_SOURCER},
        ],
    },
}


def hubs_connus():
    return list(CROISEMENT_GEOGLAM)


def fenetres_candidates(hub_id):
    if hub_id not in CROISEMENT_GEOGLAM:
        return []
    return list(CROISEMENT_GEOGLAM[hub_id]["candidates"])


def verifier_couverture():
    """Contrôle que le croisement couvre exactement les hubs de monde.py.

    Retourne None si le contrôle passe, sinon un message d'écart.
    Tolérant : si monde.py n'est pas importable, contrôle sauté.
    """
    try:
        import monde
    except ImportError:
        return None
    croises = set(CROISEMENT_GEOGLAM)
    moteur = set(monde.HUBS_MONDE)
    if croises != moteur:
        manquants = sorted(moteur - croises)
        en_trop = sorted(croises - moteur)
        return "écart croisement/moteur — manquants: %s ; en trop: %s" % (
            ", ".join(manquants) or "aucun", ", ".join(en_trop) or "aucun")
    return None


def verifier_coherence():
    """Contrôle interne : chaque fenêtre candidate est une liste de mois 1-12."""
    for hub_id, fiche in CROISEMENT_GEOGLAM.items():
        for c in fiche["candidates"]:
            if not c["fenetre"] or not all(1 <= m <= 12 for m in c["fenetre"]):
                return "fenêtre candidate invalide : %s / %s" % (hub_id, c["biomasse"])
    return None


def fiche_hub(hub_id):
    if hub_id not in CROISEMENT_GEOGLAM:
        return "Hub inconnu : %s. Hubs : %s" % (hub_id, ", ".join(CROISEMENT_GEOGLAM))
    f = CROISEMENT_GEOGLAM[hub_id]
    lignes = []
    lignes.append("== %s — %s" % (hub_id, f["pays"]))
    lignes.append("  Région GEOGLAM : %s" % f["region_geoglam"])
    for c in f["calendriers"]:
        lignes.append("  [%s] %s : semis %s ; récolte %s (source : %s)" % (
            c["etiquette"], c["culture"], c["semis"], c["recolte"], c["source"]))
        lignes.append("    Verdict : %s" % c["verdict"])
    lignes.append("  Condition de campagne : %s" % f["condition_campagne"])
    for h in f["hors_perimetre"]:
        lignes.append("  [%s] %s" % (ETIQUETTE_HORS_PERIMETRE, h))
    for c in f["candidates"]:
        lignes.append("  [%s] candidate %s %s — %s" % (
            c["etiquette"], c["biomasse"], c["fenetre"], c["justification"]))
    return "\n".join(lignes)


def sommaire():
    lignes = ["Croisement GEOGLAM — calendiers culturaux des 7 hubs (v0.7, 17/10/2026)",
              "Conditions de campagne au 28/09/2026 (bulletins AMIS n° 143 et CM4EW n° 120) ; à re-vérifier avant tout usage externe.",
              ""]
    for hub_id in CROISEMENT_GEOGLAM:
        lignes.append(fiche_hub(hub_id))
        lignes.append("")
    return "\n".join(lignes) + "\n"


def main():
    ecart = verifier_couverture()
    if ecart:
        print("ATTENTION : %s" % ecart)
    ecart = verifier_coherence()
    if ecart:
        print("ATTENTION : %s" % ecart)
    if len(sys.argv) > 1:
        print(fiche_hub(sys.argv[1]))
    else:
        print(sommaire())
    return 0


if __name__ == "__main__":
    sys.exit(main())
