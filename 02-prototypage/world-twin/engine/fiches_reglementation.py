#!/usr/bin/env python3
"""Couche 1 — fiches pays réglementaires du Trio Nomad v1 (v0.6, 17/10/2026).

Cadre légal du brûlage des résidus agricoles pour les sept hubs, sourcé
et étiqueté. Chaque élément porte son étiquette :

- DONNÉES RÉELLES (texte légal ou source officielle) : disposition
  identifiée dans un texte légal ou un portail officiel, croisée ;
- À VÉRIFIER : non confirmé à la date de vérification (17/10/2026).

RÈGLES :
- Ces fiches décrivent le cadre réglementaire, pas une consultation
  juridique : valider par un conseil local avant tout engagement.
- La réglementation évolue : toute citation externe exige une
  re-vérification datée.
- Aucune valeur calibrée ; tout résultat de simulation reste
  étiqueté SYNTHÉTIQUE.

Lancement :

    python3 engine/fiches_reglementation.py            # sommaire console
    python3 engine/fiches_reglementation.py es-extremadura  # fiche d'un hub

Les identifiants de hubs sont exactement ceux de engine/monde.py ;
verifier_couverture() le contrôle au lancement.
"""

import sys

ETIQUETTE_REEL = "DONNÉES RÉELLES"
ETIQUETTE_A_VERIFIER = "À VÉRIFIER"

STATUTS_BRULAGE = {
    "fr-rhone": "interdit (dérogation préfectorale possible)",
    "ch-leman": "interdit en plein air (prescriptions cantonales)",
    "it-puglia": "encadré (autorisation régionale ; interdiction dans les zones à risque)",
    "es-extremadura": "interdit par principe (exceptions par ordre annuel)",
    "ar-cuyo": "encadré (autorisation obligatoire ; sanctions provinciales sévères)",
    "ar-misiones": "encadré (autorisation obligatoire ; régime provincial à vérifier)",
    "ma-atlas": "encadré (loi déchets ; cadre brûlage agricole à vérifier)",
}

FICHES_REGLEMENTATION = {
    "fr-rhone": {
        "pays": "France",
        "statut_brulage": STATUTS_BRULAGE["fr-rhone"],
        "cadre": [
            {"disposition": "Brûlage à l'air libre des biodéchets (dont déchets verts) interdit ; amende 750 euros ; dérogation individuelle du préfet possible",
             "reference": "Art. L.541-21-1 du code de l'environnement",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Base historique de l'interdiction : déchets verts assimilés aux déchets ménagers",
             "reference": "Circulaire du 18/11/2011 (Légifrance)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Sanctions pénales sur les déchets doublées (loi industrie verte)",
             "reference": "Loi 2023-973 du 23/10/2023 (art. L.541-46)",
             "etiquette": ETIQUETTE_REEL},
        ],
        "pain_point": "Paille de riz et sarments à valoriser hors brûlage ; feux réels FIRMS Camargue (11 détections le 17/10/2026).",
    },
    "ch-leman": {
        "pays": "Suisse",
        "statut_brulage": STATUTS_BRULAGE["ch-leman"],
        "cadre": [
            {"disposition": "Incinération de déchets en plein air interdite ; prescriptions cantonales possibles pour les feux en plein air",
             "reference": "Ordonnance sur la protection de l'air (OPair), art. 26a ; OFEV",
             "etiquette": ETIQUETTE_REEL},
        ],
        "pain_point": "Sarments vaudois (3 783 ha) à composter, broyer ou valoriser ; image environnementale de Lavaux (UNESCO).",
    },
    "it-puglia": {
        "pays": "Italie",
        "statut_brulage": STATUTS_BRULAGE["it-puglia"],
        "cadre": [
            {"disposition": "Paille, tontes et tailles exclues du régime déchets seulement si utilisées en agriculture/sylviculture ; combustion encadrée",
             "reference": "D.Lgs 152/2006, art. 185 (Codice dell'ambiente)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Prévention et lutte contre les incendies boisés et d'interface ; lignes directrices pour la combustion des chaumes et résidus végétaux",
             "reference": "Legge regionale Puglia 38/2016 ; lignes directrices 2018 ; DPR régional 2015 (interdiction absolue dans les zones à risque)",
             "etiquette": ETIQUETTE_REEL},
        ],
        "pain_point": "Grignonnage et brûlage de tailles de plus en plus contraints ; 4 feux réels FIRMS Puglia (17/10/2026).",
    },
    "es-extremadura": {
        "pays": "Espagne",
        "statut_brulage": STATUTS_BRULAGE["es-extremadura"],
        "cadre": [
            {"disposition": "La combustion de résidus végétaux agricoles ou sylvo-pastoraux n'est pas permise en règle générale",
             "reference": "Ley 7/2022 du 8 avril, art. 27.3 (déchets et sols contaminés)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Órdenes annuelles régulant les cas autorisés selon l'époque de danger d'incendie (Alto/Bajo)",
             "reference": "Junta de Extremadura, órdenes de 2024 et 2025 (DOE)",
             "etiquette": ETIQUETTE_REEL},
        ],
        "pain_point": "Plus de 300 000 ha d'oliveraie ; 2 feux réels FIRMS (17/10/2026) ; la loi de 2022 ferme la voie du feu.",
    },
    "ar-cuyo": {
        "pays": "Argentine (Mendoza)",
        "statut_brulage": STATUTS_BRULAGE["ar-cuyo"],
        "cadre": [
            {"disposition": "Toute élimination de végétation ou résidus par le feu (quema) requiert une autorisation, interruptible selon la météo",
             "reference": "Ley nationale 26.562, art. 4 à 6 (Infoleg)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Interdiction stricte hors zones autorisées ; amendes annoncées jusqu'à 58 millions de pesos ; contraventions avec arrestation en zone urbaine",
             "reference": "Gobierno de Mendoza (communiqués officiels) ; code des contraventions",
             "etiquette": ETIQUETTE_REEL},
        ],
        "pain_point": "Restes de taille de la vigne mendocine (145 393 ha) traditionnellement brûlés ; fenêtre juin-août, anti-saison parfaite.",
    },
    "ar-misiones": {
        "pays": "Argentine (Misiones)",
        "statut_brulage": STATUTS_BRULAGE["ar-misiones"],
        "cadre": [
            {"disposition": "Autorisation préalable obligatoire pour toute quema, résidus de yerba mate inclus",
             "reference": "Ley nationale 26.562 (applicable à tout le territoire)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Régime provincial spécifique de Misiones",
             "reference": "Non confirmé document par document à la date du 17/10/2026",
             "etiquette": ETIQUETTE_A_VERIFIER},
        ],
        "pain_point": "Environ 210 000 ha de yerba mate (87 % Misiones) ; bassin le plus pluvieux de la flotte ; 1 feu réel FIRMS (17/10/2026).",
    },
    "ma-atlas": {
        "pays": "Maroc (Meknès)",
        "statut_brulage": STATUTS_BRULAGE["ma-atlas"],
        "cadre": [
            {"disposition": "Déchets agricoles couverts par la loi sur la gestion des déchets ; élimination contrôlée requise",
             "reference": "Loi n° 28-00 relative à la gestion des déchets (SGG, 2006)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Cadre spécifique du brûlage agricole marocain (incendies, chaumes, oliveraies)",
             "reference": "À sourcer auprès du Haut-Commissariat aux eaux et forêts ; la référence « loi 62.25 » du plan initial n'a pas été retrouvée et est écartée",
             "etiquette": ETIQUETTE_A_VERIFIER},
        ],
        "pain_point": "Premier bassin oléicole du royaume (Meknès : 40 000 ha) ; 2 feux réels FIRMS Al-Atlas (17/10/2026).",
    },
}


def hubs_connus():
    return list(FICHES_REGLEMENTATION)


def statut_brulage(hub_id):
    if hub_id not in FICHES_REGLEMENTATION:
        return "Hub inconnu : %s. Hubs : %s" % (hub_id, ", ".join(FICHES_REGLEMENTATION))
    return STATUTS_BRULAGE[hub_id]


def verifier_couverture():
    """Contrôle que les fiches couvrent exactement les hubs de monde.py.

    Retourne None si le contrôle passe, sinon un message d'écart.
    Tolérant : si monde.py n'est pas importable, contrôle sauté.
    """
    try:
        import monde
    except ImportError:
        return None
    fiches = set(FICHES_REGLEMENTATION)
    moteur = set(monde.HUBS_MONDE)
    if fiches != moteur:
        manquants = sorted(moteur - fiches)
        en_trop = sorted(fiches - moteur)
        return "écart fiches/moteur — manquants: %s ; en trop: %s" % (
            ", ".join(manquants) or "aucun", ", ".join(en_trop) or "aucun")
    return None


def fiche_hub(hub_id):
    if hub_id not in FICHES_REGLEMENTATION:
        return "Hub inconnu : %s. Hubs : %s" % (hub_id, ", ".join(FICHES_REGLEMENTATION))
    f = FICHES_REGLEMENTATION[hub_id]
    lignes = []
    lignes.append("== %s — %s" % (hub_id, f["pays"]))
    lignes.append("  Statut brûlage : %s" % f["statut_brulage"])
    for c in f["cadre"]:
        lignes.append("  [%s] %s (référence : %s)" % (c["etiquette"], c["disposition"], c["reference"]))
    lignes.append("  Pain point : %s" % f["pain_point"])
    return "\n".join(lignes)


def sommaire():
    lignes = ["Fiches pays réglementaires — brûlage des résidus agricoles (v0.6, 17/10/2026)",
              "Vérification documentaire du 17/10/2026 ; à re-vérifier avant tout usage externe.",
              ""]
    for hub_id in FICHES_REGLEMENTATION:
        lignes.append(fiche_hub(hub_id))
        lignes.append("")
    return "\n".join(lignes) + "\n"


def main():
    ecart = verifier_couverture()
    if ecart:
        print("ATTENTION : %s" % ecart)
    if len(sys.argv) > 1:
        print(fiche_hub(sys.argv[1]))
    else:
        print(sommaire())
    return 0


if __name__ == "__main__":
    sys.exit(main())
