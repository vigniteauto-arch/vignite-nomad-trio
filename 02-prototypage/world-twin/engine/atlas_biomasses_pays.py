#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""World Twin v1.1 — Atlas des biomasses locales par pays.

Déclinaison nationale de l'atlas des biomasses monde (v1.0) : pour chacun des
dix-huit pays couverts (les dix-sept pays de l'atlas v1.0 plus la Suisse et le
Maroc, qui ferment les sept hubs de la flotte), les biomasses LOCALES majeures
sont placées sur le globe — région, point GPS (approximation de région, jamais
un cadastre), type, volume, fenêtre saisonnière, techniques culturales, récolte
et transformation — avec, par pays, une synthèse réglementaire à cinq postes
(brûlage, enfouissement, traitement, coûts pour l'agriculture, main-d'œuvre).

Doctrine PI : ce module n'embarque AUCUN des six paramètres du VDE (Vignite
Decision Engine) et aucune valeur calibrée. Seules des données publiques sont
versionnées : géographie, productions nationales FAOSTAT (Food and Agriculture
Organization of the United Nations), ratios documentaires, calendriers,
réglementation. Les productions sont SOURCÉES (bulk FAOSTAT 2024) ; les ratios
résidus sont ILLUSTRATION ; la réglementation est DONNÉES RÉELLES pour les
juridictions hub couvertes par les fiches v0.6 et À VÉRIFIER pour les autres.

Bibliothèque standard uniquement, déterministe, aucune dépendance réseau.
Usage :
    python3 engine/atlas_biomasses_pays.py                  # sommaire par pays
    python3 engine/atlas_biomasses_pays.py PAILLE_RIZ_VN   # fiche d'un intrant
    python3 engine/atlas_biomasses_pays.py pays "Viet Nam"  # fiche d un pays
    python3 engine/atlas_biomasses_pays.py croisement       # contrôles complets
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import atlas_biomasses_monde as _master  # noqa: E402  (autorité : familles et hubs)

ETIQUETTE_SOURCÉ = "SOURCÉ"
ETIQUETTE_ILLUSTRATION = "ILLUSTRATION"
ETIQUETTE_REEL = "DONNÉES RÉELLES"
ETIQUETTE_A_VERIFIER = "À VÉRIFIER"
ETIQUETTE_A_SOURCER = "À SOURCER"

SOURCE_PRODUCTION = ("production FAOSTAT bulk Production_Crops_Livestock_E, "
                     "valeurs 2024 (mise à jour du 31/12/2025)")
ETQ_GISEMENT_SOURCÉ = "SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION"

MOIS_COURTS = _master.MOIS_COURTS

# ---------------------------------------------------------------------------
# Registre pays : fiche pays (synthèse réglementaire à cinq postes) + intrants.
# Chaque intrant : token unique (suffixe pays), famille du master, région réelle
# de production, GPS approximatif, volume ancré sur la production FAOSTAT 2024,
# fenêtre saisonnière (mois), note, techniques.
# ---------------------------------------------------------------------------

PAYS_BIOMASSES = {

"Arabie Saoudite": {
    "nom_fao": "Saudi Arabia",
    "portrait": "agriculture intensive irriguée (pivots) : dattes, blé déphasé, luzerne fourragère ; les deux intrants du master (déchet dattier, noyau de datte) sont complétés par la paille de blé, les fanes de luzerne et les palmes de taille du palmier dattier.",
    "reglementation": {
        "brulage": ("le brûlage à l'air libre des déchets agricoles est restreint par les prescriptions municipales et la réglementation sur la qualité de l'air (sable, zones urbaines)", ETIQUETTE_A_VERIFIER, "règles municipales, à sourcer"),
        "enfouissement": ("les palmes et résidus de taille sont déchiquetés et épandus au verger (mulching) ; le brûlage des palmes est documenté localement mais de moins en moins admis", ETIQUETTE_A_VERIFIER, "pratiques oasisiennes, à sourcer"),
        "traitement": ("les centres de conditionnement de dattes concentrent les déchets de tri ; la luzerne alimente les élevages ; l'élevage est en croissance (déchets de fermes)", ETIQUETTE_A_VERIFIER, "filière dattière, à sourcer"),
        "cout_agriculture": ("le coût dominant est l'eau (irrigation pivot) ; la collecte des résidus est en marge des opérations", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("main-d'œuvre agricole majoritairement expatriée dans les grandes fermes ; taille des palmiers manuelle", ETIQUETTE_A_VERIFIER, "à sourcer"),
    },
    "intrants": [
        {
            "token": "PAILLE_BLE_SA", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Buraidah (Al-Qassim, pivot céréalier)", "lat": 26.33, "lon": 43.97,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé dur/tenace, récolte déphasée par pivot irrigué",
            "production": "blé : 820 392 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 0,8 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [3, 4, 5], "fenetre_note": "moisson de mars à mai (campagne décalée)",
            "techniques": "irrigation pivot, moisson motorisée, pressage balles rondes",
        },
        {
            "token": "FANE_LUZERNE_SA", "famille": "Cultures pérennes", "nom_fr": "Fanes et refus de luzerne",
            "region": "Sakaka (Al-Jouf, ceinture fourragère)", "lat": 29.90, "lon": 40.20,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "fanes, feuilles perdues au fanage et refus de criblage de luzerne",
            "production": "pas d'entrée luzerne dans le bulk FAOSTAT — volume national À SOURCER (fermes à pivot)", "ratio": "fanes/refus ≈ 10-15 % du tonnage fané",
            "gisement": "à documenter : bassin fourrager de Al-Jouf/Al-Qassim", "etiquette_gisement": ETIQUETTE_A_SOURCER,
            "fenetre": [3, 4, 5, 6, 7, 8, 9, 10, 11],
            "fenetre_note": "coupes successives de mars à novembre, fanage continu",
            "techniques": "fauche-fanage mécanisé, balles cylindriques, criblage en ferme",
        },
        {
            "token": "RACHIS_PALMIER_SA", "famille": "Tropical", "nom_fr": "Palmes et rachis de palmier dattier",
            "region": "Al-Ahsa (oasis dattière majeure)", "lat": 25.38, "lon": 49.64,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "palmes et rachis issus de la taille annuelle du palmier dattier (avec les déchets du conditionnement déjà placés : DECHET_DATTIER, NOYAU_DATTE)",
            "production": "dattes : 1 927 556 t (2024, FAOSTAT) — l'ancrage palmes est un ratio par hectare", "ratio": "palmes ≈ 2-3 t/ha/an (taille)",
            "gisement": "palmes ≈ plusieurs centaines de milliers de t/an (ILLUSTRATION, à borner par le verger national)",
            "etiquette_gisement": "SOURCÉ (dattes FAOSTAT 2024) + ratio ILLUSTRATION",
            "fenetre": [3, 4, 5], "fenetre_note": "taille printanière des palmiers ; élagage continu possible",
            "techniques": "taille manuelle (machette), déchiquetage/broyage au verger",
        },
    ],
},

"Argentine": {
    "nom_fao": "Argentina",
    "portrait": "géant céréalier de l'hémisphère Sud : soja, maïs, blé, tournesol ; l'intrant du master (résidu de yerba, hub ar-misiones) est complété par les pailles de la Pampa et du Cuyo — le hub ar-cuyo (restos de poda) reste l'ancre régionale.",
    "reglementation": {
        "brulage": ("la Ley 26.562 (2008) encadre les brûlages agricoles : plan de gestion obligatoire, interdiction de fait dans plusieurs provinces ; Mendoza applique des amendes lourdes", ETIQUETTE_REEL, "Ley 26.562 + amendes Mendoza (fiche v0.6)"),
        "enfouissement": ("le semis direct est généralisé : la paille reste au sol par défaut (couverture, humidité)", ETIQUETTE_REEL, "pratique dominante documentée (fiche v0.6)"),
        "traitement": ("balers au sud de Buenos Aires (filière paille d'export), broyage de soja ; aucune filière résidu structurée hors paille", ETIQUETTE_A_VERIFIER, "filière paille, à sourcer"),
        "cout_agriculture": ("la paille a une valeur agronomique (semis direct) ; sa collecte est un service facturé au contraire du brûlage", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("récolte 100 % motorisée (moissonneuses 12-15 m) ; labour en régression", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "PAILLE_BLE_AR", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Tres Arroyos (sud de Buenos Aires, bassin bléier)", "lat": -38.34, "lon": -60.26,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé, chaumes et glumes",
            "production": "blé : 18 510 280 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 18,5 Mt/an (part récoltable partielle)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [12, 1], "fenetre_note": "moisson décembre-janvier (hémisphère Sud)",
            "techniques": "moisson motorisée, balers d'export au sud (filière paille balles)",
        },
        {
            "token": "PAILLE_MAIS_AR", "famille": "Céréales", "nom_fr": "Paille de maïs",
            "region": "Río Cuarto (Córdoba, cœur maïsicole)", "lat": -33.12, "lon": -64.35,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille et cannes de maïs (stover)",
            "production": "maïs : 57 494 500 t (2024, FAOSTAT)", "ratio": "stover ≈ 1,0 × grain",
            "gisement": "stover ≈ 57 Mt/an brut (récoltable très partielle, semis direct)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [3, 4, 5, 6], "fenetre_note": "récolte mars-juin",
            "techniques": "moisson à égrainage, broyage des cannes au champ, semis direct",
        },
        {
            "token": "PAILLE_SOJA_AR", "famille": "Céréales", "nom_fr": "Paille de soja",
            "region": "Rosario (Santa Fe, cœur sojero)", "lat": -32.95, "lon": -60.66,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille et fines de soja",
            "production": "soja : 48 213 207 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 48 Mt/an brut (récoltable faible)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [3, 4, 5], "fenetre_note": "récolte mars-mai",
            "techniques": "moisson motorisée, paille hachée et épandue par défaut",
        },
        {
            "token": "TIGE_TOURNESOL_AR", "famille": "Céréales", "nom_fr": "Tiges de tournesol",
            "region": "Pergamino (nord de Buenos Aires, bassin oléagineux)", "lat": -33.89, "lon": -60.94,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges et capitules secs de tournesol",
            "production": "graines de tournesol : 3 895 156 t (2024, FAOSTAT)", "ratio": "tiges ≈ 1,5 × grain",
            "gisement": "tiges ≈ 5,8 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [2, 3], "fenetre_note": "récolte février-mars",
            "techniques": "moisson motorisée, tiges broyées au champ",
        },
    ],
},

"Australie": {
    "nom_fao": "Australia",
    "portrait": "bassin céréalier de l'hémisphère Sud (blé, orge, colza) et sucrier du Queensland ; l'intrant du master (coque de macadamia, Mareeba) est complété par les pailles de l'Ouest et la bagasse de canne.",
    "reglementation": {
        "brulage": ("le brûlage de paille est encadré par les agences d'État (EPA) : permis, périodes d'interdiction saisonnière, restrictions en saison de feux", ETIQUETTE_A_VERIFIER, "règles EPA d'État, à sourcer"),
        "enfouissement": ("rétention des chaumes (stubble retention) recommandée pour l'humidité du sol ; le semis direct domine l'Ouest australien", ETIQUETTE_A_VERIFIER, "pratique dominante, à sourcer"),
        "traitement": ("filière de balles de paille d'export vers l'Asie ; bagasse en cogénération dans les sucreries du Queensland", ETIQUETTE_A_VERIFIER, "filières paille/bagasse, à sourcer"),
        "cout_agriculture": ("la paille est parfois vendue au contrat (export) ; sinon brûlée ou retenue selon les saisons", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("récolte 100 % motorisée, swathing et grosses balles ; main-d'œuvre saisonnière en moisson", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "PAILLE_BLE_AU", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Merredin (Wheatbelt, Australie-Occidentale)", "lat": -31.48, "lon": 118.28,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé, chaumes",
            "production": "blé : 34 110 000 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 34 Mt/an brut (récoltable partielle, rétention conseillée)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [11, 12], "fenetre_note": "moisson novembre-décembre (hémisphère Sud)",
            "techniques": "moisson motorisée, balles carrées/cylindriques, rétention des chaumes",
        },
        {
            "token": "PAILLE_ORGE_AU", "famille": "Céréales", "nom_fr": "Paille d'orge",
            "region": "Tamworth (Nouvelle-Galles du Sud, ceinture d'orge de brasserie)", "lat": -31.09, "lon": 150.93,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille d'orge",
            "production": "orge : 13 265 000 t (2024, FAOSTAT)", "ratio": "paille ≈ 0,9 × grain",
            "gisement": "paille ≈ 12 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [11, 12], "fenetre_note": "moisson novembre-décembre",
            "techniques": "moisson motorisée, paille de brasserie valorisée en litière",
        },
        {
            "token": "BAGASSE_CANNE_AU", "famille": "Tropical", "nom_fr": "Bagasse de canne à sucre",
            "region": "Mackay (Queensland, bassin sucrier central)", "lat": -21.14, "lon": 149.19,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "bagasse de broyage de canne (fibre pressée)",
            "production": "canne à sucre : 29 855 156 t (2024, FAOSTAT)", "ratio": "bagasse ≈ 0,28 × canne",
            "gisement": "bagasse ≈ 8,4 Mt/an (humide), concentrée en sucreries", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6, 7, 8, 9, 10, 11], "fenetre_note": "campagne de broyage juin-novembre",
            "techniques": "récolte mécanisée (canne entière), broyage en sucrerie, cogénération bagasse établie",
        },
        {
            "token": "PAILLE_COLZA_AU", "famille": "Céréales", "nom_fr": "Paille de colza (canola)",
            "region": "Esperance (Australie-Occidentale, bassin canola)", "lat": -33.87, "lon": 121.89,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de colza",
            "production": "colza : 6 396 000 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,5 × grain",
            "gisement": "paille ≈ 9,6 Mt/an brut", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [11, 12], "fenetre_note": "moisson novembre-décembre",
            "techniques": "moisson motorisée, swathing localement, paille hachée",
        },
    ],
},

"Brésil": {
    "nom_fao": "Brazil",
    "portrait": "premier producteur mondial de canne, soja, orange et de maïs de contre-saison ; les intrants du master (bagasse de canne, graine de papaye) sont complétés par la paille de canne, la paille de maïs et de soja, la balle de riz du sud et les écorces d'agrumes du parc paulista.",
    "reglementation": {
        "brulage": ("la Ley 11.241/2002 fixe l'éradication progressive du brûlage pré-récolte de la canne ; São Paulo (Lei estadual) l'a rendu marginal — récolte verte généralisée", ETIQUETTE_A_VERIFIER, "Lei 11.241/2002 + protocole agro-environnemental, à re-vérifier"),
        "enfouissement": ("la paille de canne et les résidus de soja/maïs restent au sol par défaut (semis direct pauliste) ; la paille de canne est partiellement collectée pour les chaudières", ETIQUETTE_A_VERIFIER, "système plantio direto, à sourcer"),
        "traitement": ("bagasse et paille de canne alimentent les chaudières et l'éthanol de seconde génération ; rizeries valorisent la balle ; l'agro-industrie des jus concentre les écorces", ETIQUETTE_A_VERIFIER, "filières sucrière et de jus, à sourcer"),
        "cout_agriculture": ("la paille de canne est vendue aux usines (contrat) ; la collecte de stover de maïs/soja reste marginale", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("récolte motorisée (canne) et moissons de grande capacité ; le coupeur manuel a été remplacé par la mécanisation", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "PAILLE_CANNE_BR", "famille": "Tropical", "nom_fr": "Paille de canne (trash)",
            "region": "Ribeirão Preto (São Paulo, cœur sucrier)", "lat": -21.18, "lon": -47.81,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "feuillage et sommets secs de canne récoltée verte (paille)",
            "production": "canne à sucre : 759 662 482 t (2024, FAOSTAT)", "ratio": "paille ≈ 0,10-0,15 × canne",
            "gisement": "paille ≈ 76-114 Mt/an (fraction collectée croissante pour les chaudières)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [5, 6, 7, 8, 9, 10, 11], "fenetre_note": "campagne de récolte mai-novembre",
            "techniques": "récolte verte mécanisée sans brûlage, balayage/râteau de paille, chaudières en usine",
        },
        {
            "token": "PAILLE_MAIS_BR", "famille": "Céréales", "nom_fr": "Paille de maïs",
            "region": "Cascavel (Paraná, maïs de contre-saison)", "lat": -24.96, "lon": -53.74,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille et cannes de maïs (safrinha et plein champ)",
            "production": "maïs : 114 953 303 t (2024, FAOSTAT)", "ratio": "stover ≈ 1,0 × grain",
            "gisement": "stover ≈ 115 Mt/an brut (récoltable très partielle, semis direct)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [2, 3, 7, 8, 9], "fenetre_note": "récoltes de juin-septembre (plein champ) et janvier-mars (safrinha)",
            "techniques": "moisson à épis, broyage des cannes, semis direct sur couverture",
        },
        {
            "token": "BALLE_RIZ_BR", "famille": "Céréales", "nom_fr": "Balle de riz",
            "region": "Pelotas (Rio Grande do Sul, riziculture irriguée)", "lat": -31.72, "lon": -52.34,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "balle (enveloppe) de riz usiné",
            "production": "riz : 10 671 490 t (2024, FAOSTAT)", "ratio": "balle ≈ 0,20 × riz usiné",
            "gisement": "balle ≈ 2,1 Mt/an, concentrée en rizeries", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [2, 3, 4], "fenetre_note": "moisson janvier-avril, usinage continu ensuite",
            "techniques": "récolte motorisée, séchage et usinage en rizeries coopératives",
        },
        {
            "token": "PAILLE_SOJA_BR", "famille": "Céréales", "nom_fr": "Paille de soja",
            "region": "Sorriso (Mato Grosso, front pionnier sojero)", "lat": -12.55, "lon": -55.72,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille et fines de soja",
            "production": "soja : 144 473 768 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 144 Mt/an brut (récoltable très faible, semis direct)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3], "fenetre_note": "récolte janvier-mars",
            "techniques": "moisson motorisée, paille hachée-épandue, double culture maïs-soja",
        },
        {
            "token": "ECORCE_ORANGE_BR", "famille": "Cultures pérennes", "nom_fr": "Écorces d'orange (industrie du jus)",
            "region": "Matão (São Paulo, bassin des usines de jus)", "lat": -21.60, "lon": -48.37,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "écorces, pulpes et membraises d'orange pressée (humides)",
            "production": "oranges : 15 688 409 t (2024, FAOSTAT)", "ratio": "résidu humide ≈ 0,25 × fruits pressés",
            "gisement": "écorces/pulpe ≈ 3,9 Mt/an humides, concentrées en usines de jus", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6, 7, 11, 12, 1], "fenetre_note": "campagne de presse principal (juin-décembre selon variétés)",
            "techniques": "vergers industriels irrigués, pressoirs concentrés, valorisation en alimentation animale (pellets) et digestats",
        },
    ],
},

"Chine": {
    "nom_fao": "China",
    "portrait": "premier producteur mondial de riz, blé et maïs ; l'intrant du master (tige de bambou, Zhejiang) est complété par la paille de riz du Hunan, la paille de maïs de la Mandchourie, la paille de blé de la plaine du Nord et les coques d'arachide du Shandong.",
    "reglementation": {
        "brulage": ("le brûlage à l'air libre de la paille est interdit par la loi sur la prévention de la pollution atmosphérique ; surveillance satellitaire des points chauds et amendes provinciales", ETIQUETTE_A_VERIFIER, "loi pollution atmosphérique + règles provinciales, à sourcer"),
        "enfouissement": ("la politique de retour au sol (秸秆还田) est subventionnée dans les grandes provinces céréalières ; incorporation mécanisée dominante", ETIQUETTE_A_VERIFIER, "politique de subvention, à sourcer"),
        "traitement": ("filières biomasse en croissance : centrales à paille, granulés, éthanol cellulosique pilote ; coques d'arachide valorisées en combustible", ETIQUETTE_A_VERIFIER, "filière biomasse, à sourcer"),
        "cout_agriculture": ("la collecte de paille est organisée en dépôts de village ; le retour au sol reste la voie la moins chère", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("récolte motorisée en progression (moissonneuses de service), séchage sur aire", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "PAILLE_RIZ_CN", "famille": "Céréales", "nom_fr": "Paille de riz",
            "region": "Changsha (Hunan, double riziculture)", "lat": 28.23, "lon": 112.94,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de riz (canne et feuilles)",
            "production": "riz : 209 173 000 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × paddy",
            "gisement": "paille ≈ 251 Mt/an brut national (ILLUSTRATION au prorata du bassin)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [7, 8, 9, 10], "fenetre_note": "récoltes du riz précoce (juillet) et tardif (octobre)",
            "techniques": "moissonneuse-batteuse de service, séchage en coopérative, incorporation au sol",
        },
        {
            "token": "PAILLE_MAIS_CN", "famille": "Céréales", "nom_fr": "Paille de maïs",
            "region": "Harbin (Heilongjiang, ceinture dorée du maïs)", "lat": 45.80, "lon": 126.53,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille et cannes de maïs",
            "production": "maïs : 295 140 069 t (2024, FAOSTAT)", "ratio": "stover ≈ 1,0 × grain",
            "gisement": "stover ≈ 295 Mt/an brut national (récoltable partielle)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10], "fenetre_note": "récolte septembre-octobre avant les gelées",
            "techniques": "moisson motorisée, balles cylindriques, dépôts de village",
        },
        {
            "token": "COQUE_ARACHIDE_CN", "famille": "Coques & noyaux", "nom_fr": "Coques d'arachide",
            "region": "Yantai (Shandong, bassin arachidier)", "lat": 37.54, "lon": 121.39,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "coques (gousses) d'arachide décortiquée",
            "production": "arachide : 19 651 100 t (2024, FAOSTAT)", "ratio": "coque ≈ 0,30 × arachide en gousse",
            "gisement": "coques ≈ 5,9 Mt/an, concentrées en décortiqueuses", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [8, 9], "fenetre_note": "arrachage et séchage août-septembre",
            "techniques": "arrachage motorisé, séchage au champ, décorticage en huileries",
        },
        {
            "token": "PAILLE_BLE_CN", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Zhengzhou (Henan, grenier à blé du Nord)", "lat": 34.75, "lon": 113.63,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé",
            "production": "blé : 140 105 000 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 140 Mt/an brut national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6, 7], "fenetre_note": "moisson juin-juillet",
            "techniques": "moisson motorisée, fenêtre courte riz-blé au Sud, incorporation dominante",
        },
    ],
},

"Côte d'Ivoire": {
    "nom_fao": "Côte d'Ivoire",
    "portrait": "premier producteur mondial de cacao, grand bassin palmier à huile et hévéa, cajou en hausse ; l'intrant du master (cabosse de cacao, Daloa) est complété par les coques de cacao des unités de transformation, les fibres de palmier, la paille de riz et les coques de cajou du Nord.",
    "reglementation": {
        "brulage": ("les feux de brousse sont prohibés par le code forestier et les arrêtés annuels anti-feux ; la pratique de préparation de parcelle se maintient en saison sèche", ETIQUETTE_A_VERIFIER, "code forestier + arrêtés anti-feux, à sourcer"),
        "enfouissement": ("les coques de cacao sont épandues au verger comme amendement (pratique courante) ; les régimes vides (raffles) sont mulchés", ETIQUETTE_A_VERIFIER, "pratiques verger/plantation, à sourcer"),
        "traitement": ("compostage coopératif et granulés de coques de cacao en développement ; fibres de palmiste en chaudière d'huilerie", ETIQUETTE_A_VERIFIER, "initiatives de transformation, à sourcer"),
        "cout_agriculture": ("l'écabossage (fèves) est à la charge des coopératives ; la logistique des coques n'existe pas encore à grande échelle", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("écabossage manuel à la machette au verger ; petites unités de transformation en zone de production", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "COQUE_CACAO_CI", "famille": "Coques & noyaux", "nom_fr": "Coques de cacao (transformation)",
            "region": "Soubré (Sud-Comoé, ancre industrielle cacaoyère)", "lat": 5.78, "lon": -6.60,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "coques de fèves décortiquées (flux des unités de transformation, distinct de la cabosse au verger)",
            "production": "fèves de cacao : 1 890 442 t (2024, FAOSTAT)", "ratio": "coque ≈ 0,70 × fèves",
            "gisement": "coques ≈ 1,3 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11, 12, 1, 2, 3], "fenetre_note": "campagne principale octobre-mars (petite récolte en mai-août)",
            "techniques": "écabossage au verger, fermentation en bacs, séchage solaire, décorticage en usine",
        },
        {
            "token": "FIBRE_PALMIER_CI", "famille": "Tropical", "nom_fr": "Fibres et coques de palmier à huile",
            "region": "Grand-Lahou (ceinture palmicoïde du Sud)", "lat": 5.25, "lon": -5.02,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "fibres de presse et coques de palmiste des huileries",
            "production": "régimes de palmier : 2 298 984 t (2024, FAOSTAT)", "ratio": "fibres ≈ 0,12 × régime ; coques ≈ 0,13 × régime",
            "gisement": "fibres + coques ≈ 0,57 Mt/an, concentrées en huileries", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "fenetre_note": "production permanente (régimes toute l'année)",
            "techniques": "plantations villageoises et agro-industrielles, stérilisation/pressage en huilerie, chaudières fibres",
        },
        {
            "token": "PAILLE_RIZ_CI", "famille": "Céréales", "nom_fr": "Paille de riz",
            "region": "Gagnoa (bassin rizicole de l'Ouest)", "lat": -6.13, "lon": -5.98,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de riz",
            "production": "riz : 2 381 129 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × paddy",
            "gisement": "paille ≈ 2,9 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11, 12], "fenetre_note": "récolte principale octobre-décembre",
            "techniques": "récolte manuelle puis motorisée en croissance, battage villageois",
        },
        {
            "token": "COQUE_CAJOU_CI", "famille": "Coques & noyaux", "nom_fr": "Coques de cajou (noix de cajou)",
            "region": "Korhogo (bassin cajou du Nord)", "lat": 9.46, "lon": -5.63,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "coques de noix de cajou (contenant du liquide de coque, CNSL, corrosif — précaution au procédé)",
            "production": "cajou en coque : 944 673 t (2024, FAOSTAT)", "ratio": "coque ≈ 0,70 × noix brute",
            "gisement": "coques ≈ 0,66 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [2, 3, 4, 5], "fenetre_note": "récolte février-avril, décorticage en saison sèche",
            "techniques": "ramassage manuel, séchage solaire, unités chinoises/marocaines de décorticage en montée",
        },
    ],
},

"Équateur": {
    "nom_fao": "Ecuador",
    "portrait": "premier exportateur mondial de bananes, palmerie et riziculture de la Côte ; l'intrant du master (tige de bananier, Machala) est complété par les fibres de palmier, la bagasse de canne et la balle de riz.",
    "reglementation": {
        "brulage": ("la réglementation de qualité de l'air et les ordonnances provinciales restreignent le brûlage au champ ; pratique résiduelle sur canne et riz", ETIQUETTE_A_VERIFIER, "normes qualité de l'air, à sourcer"),
        "enfouissement": ("incorporation des pailles de riz dans les parcelles ; les raflés de palmier sont mulchées au verger", ETIQUETTE_A_VERIFIER, "pratiques de plantation, à sourcer"),
        "traitement": ("palmeries modernes valorisent fibres et coques en chaudière ; sucreries (bagasse) et rizeries (balle) établies", ETIQUETTE_A_VERIFIER, "filières locales, à sourcer"),
        "cout_agriculture": ("la collecte est à charge des usines (balle, bagasse) ou laissée au champ (paille)", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("récolte de la banane manuelle (câbles), riz motorisé en croissance", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "FIBRE_PALMIER_EC", "famille": "Tropical", "nom_fr": "Fibres de palmier à huile",
            "region": "Santo Domingo (bassin palmicole de l'Ouest)", "lat": -0.25, "lon": -79.15,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "fibres de presse et coques de palmiste des extracteurs",
            "production": "régimes de palmier : 2 651 973 t (2024, FAOSTAT)", "ratio": "fibres ≈ 0,12 × régime",
            "gisement": "fibres ≈ 0,32 Mt/an, concentrées en extracteurs", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "fenetre_note": "production permanente",
            "techniques": "plantations agro-industrielles, extracteurs concentrés, chaudières fibres",
        },
        {
            "token": "BAGASSE_CANNE_EC", "famille": "Tropical", "nom_fr": "Bagasse de canne à sucre",
            "region": "Milagro (Guayas, bassin sucrier côtier)", "lat": -2.13, "lon": -79.59,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "bagasse de broyage de canne",
            "production": "canne à sucre : 6 378 738 t (2024, FAOSTAT)", "ratio": "bagasse ≈ 0,28 × canne",
            "gisement": "bagasse ≈ 1,8 Mt/an humide, en sucreries", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [8, 9, 10, 11, 12], "fenetre_note": "campagne de broyage août-décembre",
            "techniques": "récolte manuelle/mécanisée, broyage en sucreries, cogénération partielle",
        },
        {
            "token": "BALLE_RIZ_EC", "famille": "Céréales", "nom_fr": "Balle de riz",
            "region": "Babahoyo (Los Ríos, riziculture de la Côte)", "lat": -1.80, "lon": -79.47,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "balle de riz usiné",
            "production": "riz : 1 560 200 t (2024, FAOSTAT)", "ratio": "balle ≈ 0,20 × riz usiné",
            "gisement": "balle ≈ 0,31 Mt/an, en rizeries", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11], "fenetre_note": "récolte principale octobre-novembre",
            "techniques": "récolte motorisée, séchage/usinage en rizeries de la Côte",
        },
    ],
},

"Espagne": {
    "nom_fao": "Spain",
    "portrait": "bassin oléicole mondial (hub es-extremadura ancré par NOYAU_OLIVE et la fiche v0.6) ; les intrants du master (coque d'amande, noyau d'olive) sont complétés par les pailles de Castille et d'Aragon, les écorces d'agrumes valenciennes et la balle de riz des marismas.",
    "reglementation": {
        "brulage": ("l'incinération de résidus végétaux au champ est interdite par la Ley 7/2022 (art. 27.3) ; dérogations phytosanitaires exceptionnelles des communautés autonomes", ETIQUETTE_REEL, "Ley 7/2022 art. 27.3 (fiche v0.6)"),
        "enfouissement": ("l'enfouissement de la paille est la pratique dominante (semis direct en progression en Castille)", ETIQUETTE_A_VERIFIER, "pratique dominante, à sourcer"),
        "traitement": ("marché de la paille établi (balles, litières, papeterie) ; industries de jus concentrées ; rizeries des marismas", ETIQUETTE_A_VERIFIER, "filières, à sourcer"),
        "cout_agriculture": ("la paille se vend au champ (courtiers) ; le coût de pressage est répercuté sur l'acheteur", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("moisson motorisée, presses à balles, courtiers de paille", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "PAILLE_BLE_ES", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Valladolid (Tierra de Campos, grenier castillan)", "lat": 41.65, "lon": -4.72,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé tendre et dur",
            "production": "blé : 7 147 930 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 7,1 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6, 7], "fenetre_note": "moisson juin-juillet",
            "techniques": "moisson motorisée, balles rondes, marché de courtage local",
        },
        {
            "token": "PAILLE_ORGE_ES", "famille": "Céréales", "nom_fr": "Paille d'orge",
            "region": "Zaragoza (vallée de l'Ebre, ceinture d'orge)", "lat": 41.65, "lon": -0.89,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille d'orge",
            "production": "orge : 7 440 970 t (2024, FAOSTAT)", "ratio": "paille ≈ 0,9 × grain",
            "gisement": "paille ≈ 6,7 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [5, 6, 7], "fenetre_note": "moisson mai-juillet selon altitudes",
            "techniques": "moisson motorisée, balles pour litières et ration animale",
        },
        {
            "token": "ECORCE_ORANGE_ES", "famille": "Cultures pérennes", "nom_fr": "Écorces d'orange (industrie du jus)",
            "region": "Valence (huerta des agrumes)", "lat": 39.47, "lon": -0.38,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "écorces et pulpes d'agrumes pressés",
            "production": "oranges : 2 904 940 t (2024, FAOSTAT)", "ratio": "résidu humide ≈ 0,25 × fruits pressés",
            "gisement": "écorces ≈ 0,73 Mt/an humides, en usines de jus", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11, 12, 1, 2, 3], "fenetre_note": "campagne d'agrumes octobre-mars",
            "techniques": "vergers irrigués, usines de jus concentré, valorisation en alimentation animale",
        },
        {
            "token": "BALLE_RIZ_ES", "famille": "Céréales", "nom_fr": "Balle de riz",
            "region": "Séville (marismas du Guadalquivir)", "lat": 36.95, "lon": -6.15,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "balle de riz usiné",
            "production": "riz : 605 820 t (2024, FAOSTAT)", "ratio": "balle ≈ 0,20 × riz usiné",
            "gisement": "balle ≈ 0,12 Mt/an, en rizeries andalouses", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10], "fenetre_note": "récolte septembre-octobre",
            "techniques": "riziculture inondée, moisson motorisée, séchage coopératif",
        },
    ],
},

"États-Unis": {
    "nom_fao": "United States of America",
    "portrait": "premier maïsicol du monde, blé des Grandes Plaines, riz de l'Arkansas et amande californienne ; l'intrant du master (coque de pacane, Géorgie) est complété par le stover de maïs de l'Iowa, la paille de blé du Kansas, les coques d'amande de la vallée Centrale et la balle de riz de l'Arkansas.",
    "reglementation": {
        "brulage": ("le brûlage agricole est régi par les règles des districts de qualité de l'air de chaque État (ex. SJVAPCD en Californie) : permis, plafonds, jours d'interdiction", ETIQUETTE_A_VERIFIER, "règles d'État (districts air), à sourcer"),
        "enfouissement": ("la rétention d'une part du stover de maïs (30-60 %) est recommandée pour le carbone du sol ; le no-till s'étend sur les Plaines", ETIQUETTE_A_VERIFIER, "pratiques de conservation, à sourcer"),
        "traitement": ("coques d'amande valorisées en litière laitière et combustible (marché spot établi) ; balle de riz en litière ; stover pilier de l'éthanol cellulosique", ETIQUETTE_A_VERIFIER, "filières, à sourcer"),
        "cout_agriculture": ("les hullers californiens facturent le traitement des coques ; la paille se vend à la tonne balles", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("récolte 100 % motorisée ; opérateurs saisonniers ; hullers/shellers centraux", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "PAILLE_MAIS_US", "famille": "Céréales", "nom_fr": "Paille de maïs (corn stover)",
            "region": "Ames (Iowa, ceinture de maïs)", "lat": 42.03, "lon": -93.62,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille, cannes et spathes de maïs",
            "production": "maïs : 377 632 690 t (2024, FAOSTAT)", "ratio": "stover ≈ 1,0 × grain",
            "gisement": "stover ≈ 378 Mt/an brut national (récoltable très partielle, rétention au sol requise)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11], "fenetre_note": "récolte septembre-novembre",
            "techniques": "moisson à épis, râteau-andainage des cannes, balles ; chaîne éthanol cellulosique pilote",
        },
        {
            "token": "PAILLE_BLE_US", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Salina (Kansas, blé d'hiver)", "lat": 38.84, "lon": -97.61,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé d'hiver",
            "production": "blé : 53 650 020 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 54 Mt/an brut national (récoltable partielle)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6, 7], "fenetre_note": "moisson juin-juillet",
            "techniques": "moisson motorisée, balles grosses cylindriques, pâturage d'hiver des chaumes",
        },
        {
            "token": "COQUE_AMANDE_US", "famille": "Coques & noyaux", "nom_fr": "Coques et écales d'amande",
            "region": "Modesto (vallée Centrale de Californie, monde de l'amande)", "lat": 37.63, "lon": -121.00,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "coques (hull) et écales (shell) des hullers/shellers",
            "production": "amandes en coque : 2 000 340 t (2024, FAOSTAT)", "ratio": "coques+écales ≈ 2,0 × amande décortiquée",
            "gisement": "coques+écales ≈ 4 Mt/an, concentrées en hullers", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [8, 9, 10], "fenetre_note": "récolte août-octobre, décorticage continu ensuite",
            "techniques": "secoueuses mécaniques, hullers/shellers centraux, marché litière/combustible établi",
        },
        {
            "token": "BALLE_RIZ_US", "famille": "Céréales", "nom_fr": "Balle de riz",
            "region": "Stuttgart (Arkansas, ceinture du riz)", "lat": 34.56, "lon": -91.55,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "balle de riz usiné",
            "production": "riz : 10 075 780 t (2024, FAOSTAT)", "ratio": "balle ≈ 0,20 × riz usiné",
            "gisement": "balle ≈ 2,0 Mt/an, en rizeries", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10], "fenetre_note": "récolte septembre-octobre",
            "techniques": "riziculture irriguée, moisson motorisée, séchage/usinage en réseau coopératif",
        },
    ],
},

"Inde": {
    "nom_fao": "India",
    "portrait": "premier producteur mondial de riz, blé, moutarde et arachide de la zone ; l'intrant du master (tige de coton, Pendjab) est complété par la paille de riz (épicentre mondial du brûlage), la paille de blé, les tiges de moutarde et les coques d'arachide.",
    "reglementation": {
        "brulage": ("le brûlage de la paille de riz au Pendjab et Haryana est restreint par les ordonnances des commissions (tribunaux) et la PPCB (Pollution Control Board du Pendjab) ; amendes, campagnes de dissuasion, subventions aux machines (Happy Seeder)", ETIQUETTE_A_VERIFIER, "ordonnances CAAP + PPCB, à re-vérifier (fiche v1.0)"),
        "enfouissement": ("le semis direct dans la paille (Happy Seeder, super seeder) est subventionné ; adoption partielle sous pression de la fenêtre riz-blé", ETIQUETTE_A_VERIFIER, "programmes in-situ, à sourcer"),
        "traitement": ("filières ex-situ en croissance : co-combustion dans les centrales thermiques (biomasse co-firing), balle de riz en composites/papier, granulés", ETIQUETTE_A_VERIFIER, "programmes de co-firing, à sourcer"),
        "cout_agriculture": ("la fenêtre courte riz-blé rend le brûlage le moins cher ; la collecte balles se développe via des entrepreneurs de machinerie", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("récolte combinée répandue au Pendjab (andains sur 20-30 cm), arrachage du coton manuel en recul", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "PAILLE_RIZ_IN", "famille": "Céréales", "nom_fr": "Paille de riz (parali)",
            "region": "Ludhiana (Pendjab, épicentre du brûlage de paille)", "lat": 30.90, "lon": 75.85,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de riz et chaumes de récolte combinée",
            "production": "riz : 217 867 864 t (2024, FAOSTAT, national)", "ratio": "paille ≈ 1,2 × paddy",
            "gisement": "paille ≈ 261 Mt/an brut national ; le point Pendjab porte le pain point brûlage (fenêtre de 20 jours entre riz et blé)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11], "fenetre_note": "récolte septembre-novembre, brûlage/collecte en octobre-novembre",
            "techniques": "moissonneuse-batteuse (andains), Happy Seeder/subvention, andainage-balles en croissance",
        },
        {
            "token": "PAILLE_BLE_IN", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Meerut (Uttar Pradesh occidental, plaine du Gange)", "lat": 28.98, "lon": 77.71,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé",
            "production": "blé : 113 292 368 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 113 Mt/an brut national (fourrage dominant, collecte très valorisée)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [3, 4], "fenetre_note": "moisson mars-avril",
            "techniques": "moisson combinée, balles pour fourrage/papier, marché de paille établi",
        },
        {
            "token": "TIGE_MOUTARDE_IN", "famille": "Céréales", "nom_fr": "Tiges de moutarde (sarson)",
            "region": "Jaipur (Rajasthan, ceinture de la moutarde)", "lat": 26.91, "lon": 75.79,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges et siliques vides de moutarde",
            "production": "moutarde/colza : 13 259 142 t (2024, FAOSTAT)", "ratio": "tiges ≈ 1,5 × grain",
            "gisement": "tiges ≈ 19,9 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [2, 3, 4], "fenetre_note": "récolte février-avril",
            "techniques": "récolte manuelle puis batteuse, tiges séchées en meules (combustible domestique traditionnel)",
        },
        {
            "token": "BALLE_ARACHIDE_IN", "famille": "Coques & noyaux", "nom_fr": "Coques d'arachide",
            "region": "Junagadh (Gujarat, Saurashtra arachidier)", "lat": 21.52, "lon": 70.46,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "coques (gousses) d'arachide décortiquée",
            "production": "arachide : 11 945 539 t (2024, FAOSTAT)", "ratio": "coque ≈ 0,30 × arachide en gousse",
            "gisement": "coques ≈ 3,6 Mt/an, en décortiqueuses et huileries", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [8, 9, 10], "fenetre_note": "arrachage en fin de mousson (kharif)",
            "techniques": "arrachage motorisé, séchage au champ, décorticage en usines de bord de mer",
        },
    ],
},

"Italie": {
    "nom_fao": "Italy",
    "portrait": "vergers et vignes du Carré d'Or (hub it-puglia ancré par RAMEAU_OLIVIER et la fiche v0.6) ; les intrants du master sont complétés par la paille du blé dur des Pouilles, la rafle de maïs de la plaine du Pô, la balle de riz de Vercelli et le marc de raisin vénitien.",
    "reglementation": {
        "brulage": ("la combustion des résidus agricoles est interdite (D.Lgs 152/2006, art. 185) ; les Pouilles réglementent strictement le brûlage des chaumes (LR 38/2016)", ETIQUETTE_REEL, "D.Lgs 152/2006 art. 185 + LR Puglia 38/2016 (fiche v0.6)"),
        "enfouissement": ("l'incorporation de la paille de blé dur est documentée dans les Pouilles (alternative encadrée au brûlage)", ETIQUETTE_A_VERIFIER, "pratiques documentées, à sourcer"),
        "traitement": ("rizeries de Vercelli (balle), distilleries et caves (marc), marchés de paille locaux", ETIQUETTE_A_VERIFIER, "filières, à sourcer"),
        "cout_agriculture": ("la paille de blé dur se vend (litières, papeterie) ; le ramassage est opéré par des tiers", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("moisson motorisée, presses à balles ; vendanges partiellement manuelles en coteaux", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "PAILLE_BLE_IT", "famille": "Céréales", "nom_fr": "Paille de blé dur",
            "region": "Foggia (Tavoliere des Pouilles, cœur du blé dur)", "lat": 41.46, "lon": 15.70,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé dur",
            "production": "blé (toutes catégories, cœur blé dur) : 6 213 210 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 6,2 Mt/an (Tavoliere : première région de blé dur)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6, 7], "fenetre_note": "moisson juin-juillet",
            "techniques": "moisson motorisée, balles rondes, fenêtre croisée avec le brûlage encadré des Pouilles",
        },
        {
            "token": "RAFLE_MAIS_IT", "famille": "Céréales", "nom_fr": "Rafle de maïs",
            "region": "Piacenza (plaine du Pô, maïs fourrager)", "lat": 45.05, "lon": 9.69,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "rafles (épis dégranés) de maïs",
            "production": "maïs : 4 940 530 t (2024, FAOSTAT)", "ratio": "rafle ≈ 0,15 × grain",
            "gisement": "rafles ≈ 0,74 Mt/an, en silos de maïs Granario", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10], "fenetre_note": "récolte septembre-octobre",
            "techniques": "moisson à épis, séchage en cribles (grandes unités de séchage bergamasques), rafles en litière",
        },
        {
            "token": "BALLE_RIZ_IT", "famille": "Céréales", "nom_fr": "Balle de riz",
            "region": "Vercelli (baraggia, riziculture du Pô)", "lat": 45.32, "lon": 8.42,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "balle de riz usiné",
            "production": "riz : 1 448 760 t (2024, FAOSTAT)", "ratio": "balle ≈ 0,20 × riz usiné",
            "gisement": "balle ≈ 0,29 Mt/an, en rizeries", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10], "fenetre_note": "récolte septembre-octobre",
            "techniques": "riziculture inondée, moisson motorisée, séchage/usinage des rizeries piémontaises",
        },
        {
            "token": "MARC_RAISIN_IT", "famille": "Cultures pérennes", "nom_fr": "Marc de raisin",
            "region": "Trévise (Vénétie, prosecco)", "lat": 45.67, "lon": 12.24,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "marc et rafles de raisin vinifiés (distinct de l'ancre française du même type)",
            "production": "raisins : 7 637 640 t (2024, FAOSTAT)", "ratio": "marc ≈ 0,15 × raisin",
            "gisement": "marc ≈ 1,1 Mt/an, en caves", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10], "fenetre_note": "vendanges septembre-octobre",
            "techniques": "vendanges manuelles/motorisées, distillation du marc encadrée, caves concentrées",
        },
    ],
},

"Malaisie": {
    "nom_fao": "Malaysia",
    "portrait": "deuxième producteur mondial d'huile de palme ; l'intrant du master (rafflé de palmier, Johor) est complété par les fibres de presse de Sabah, les coques de noix de coco et la paille de riz de Kedah.",
    "reglementation": {
        "brulage": ("le brûlage des plantations est interdit (politique de zéro brûlage depuis les épisodes de brume transfrontalière)", ETIQUETTE_A_VERIFIER, "interdiction zéro brûlage, à sourcer"),
        "enfouissement": ("les régimes vides (raffles) sont mulchés au verger — pratique industrielle dominante", ETIQUETTE_A_VERIFIER, "pratique de plantation, à sourcer"),
        "traitement": ("fibres et coques alimentent les chaudières des moulins (biomasse électricité, compostage industriel EFB)", ETIQUETTE_A_VERIFIER, "filières moulin, à sourcer"),
        "cout_agriculture": ("les moulins concentrent gratuitement les résidus (fibres, coques, EFB) — point de collecte idéal", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("récolte de régime manuelle au long (ciseaux à manche)", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "FIBRE_PALMIER_MY", "famille": "Tropical", "nom_fr": "Fibres de palmier à huile",
            "region": "Sandakan (Sabah, frontière palmicole de l'Est)", "lat": 5.84, "lon": 118.11,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "fibres de presse (mesocarpe) et coques de palmiste des moulins",
            "production": "régimes de palmier : 100 163 525 t (2024, FAOSTAT)", "ratio": "fibres ≈ 0,12 × régime",
            "gisement": "fibres ≈ 12 Mt/an (coques ≈ 13 Mt/an en sus), concentrées en moulins", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "fenetre_note": "production permanente des régimes",
            "techniques": "plantations industrielles, moulins concentrent fibres/coques, chaudières biomasse",
        },
        {
            "token": "COQUE_COCO_MY", "famille": "Coques & noyaux", "nom_fr": "Coques de noix de coco",
            "region": "Kudat (Sabah, cocoteraies du Nord)", "lat": 6.89, "lon": 116.85,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "coques (endocarpe) de noix de coco déshuskées",
            "production": "noix de coco : 673 553 t (2024, FAOSTAT)", "ratio": "coque ≈ 0,40 × noix",
            "gisement": "coques ≈ 0,27 Mt/an, en déshuskeurs/coprah", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "fenetre_note": "récolte permanente",
            "techniques": "récolte manuelle, déshuskage en points de coprah, charbon de coque traditionnel",
        },
        {
            "token": "PAILLE_RIZ_MY", "famille": "Céréales", "nom_fr": "Paille de riz",
            "region": "Alor Setar (Kedah, rizière du Nord)", "lat": 6.11, "lon": 100.37,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de riz",
            "production": "riz : 2 102 960 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × paddy",
            "gisement": "paille ≈ 2,5 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [8, 9, 10], "fenetre_note": "récolte principale août-octobre (saison principale)",
            "techniques": "moisson mécanisée de service (compagnies de moisson), brûlage résiduel en recul",
        },
    ],
},

"Maroc": {
    "nom_fao": "Morocco",
    "portrait": "hub Al-Atlas (Meknès) de la flotte ; l'oléiculture marocaine et les céréales du Chaouia complètent le maillage — premier point pays rattaché au hub ma-atlas (grignons d'olive à Meknès même).",
    "reglementation": {
        "brulage": ("le brûlage des résidus au champ est réglementé dans le cadre de la gestion des déchets et des arrêtés du ministère de l'agriculture (interdictions en période de vent)", ETIQUETTE_REEL, "Loi 28-00 + arrêtés (fiche v0.6)"),
        "enfouissement": ("le semis direct progresse (programmes de conservation) ; la paille reste majoritairement pâturée ou collectée pour l'élevage", ETIQUETTE_A_VERIFIER, "pratiques céréalières, à sourcer"),
        "traitement": ("huileries concentrées à Meknès et Fès (grignons), paille valorisée en élevage (litière/fourrage)", ETIQUETTE_A_VERIFIER, "filière oléicole, à sourcer"),
        "cout_agriculture": ("la paille a une valeur fourragère élevée (équarrissage du marché) ; les grignons sont vendus par les huileries (maâouns)", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("moisson motorisée en progression, orangeries et oliveraies de main-d'œuvre saisonnière", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "GRIGNON_OLIVE_MA", "famille": "Cultures pérennes", "nom_fr": "Grignons d'olive",
            "region": "Meknès (Saïss, huileries du hub Al-Atlas)", "lat": 33.90, "lon": -5.55,
            "type_point": "hub existant", "hubs_flotte": {"ma-atlas": "grignons-olive"},
            "type_biomasse": "grignons (résidu de pressage) des huileries du Saïss — premier rattachement pays au hub ma-atlas",
            "production": "olives : 1 079 873 t (2024, FAOSTAT)", "ratio": "grignons ≈ 0,40 × olives triturées",
            "gisement": "grignons ≈ 0,43 Mt/an, concentrés en huileries (maâouns)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11, 12], "fenetre_note": "trituration octobre-février, pic novembre-décembre",
            "techniques": "oliveraies du Saïss, trituration en huileries modernes (2 phases : grignons humides)",
        },
        {
            "token": "PAILLE_BLE_MA", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Settat (Chaouia, plaines céréalières)", "lat": 32.99, "lon": -7.62,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé tendre/dur",
            "production": "blé : 2 441 670 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 2,4 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [5, 6], "fenetre_note": "moisson mai-juin",
            "techniques": "moisson motorisée, balles pour litière/fourrage (marché d'élevage)",
        },
        {
            "token": "PAILLE_ORGE_MA", "famille": "Céréales", "nom_fr": "Paille d'orge",
            "region": "El Hajeb (Moyen Atlas, orge de bour)", "lat": 33.62, "lon": -5.37,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille d'orge de bour (pluvial)",
            "production": "orge : 659 225 t (2024, FAOSTAT)", "ratio": "paille ≈ 0,9 × grain",
            "gisement": "paille ≈ 0,59 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [5, 6], "fenetre_note": "moisson mai-juin",
            "techniques": "moisson motorisée en bour, balles destinées à l'élevage ovin",
        },
    ],
},

"Mexique": {
    "nom_fao": "Mexico",
    "portrait": "bassin de l'agave (master), du maïs natal et de la canne ; les intrants du master (résidu d'agave, noyau d'avocat, sargasse) sont complétés par la bagasse de canne de Veracruz, la paille de maïs du Bajío, les écorces d'orange et les coques de café du Chiapas.",
    "reglementation": {
        "brulage": ("la LGPGIR (loi générale de prévention et gestion intégrale des résidus) classe les résidus agricoles ; les lois d'État restreignent le brûlage ; la pratique de quema persiste localement sur la canne", ETIQUETTE_A_VERIFIER, "LGPGIR + lois d'État, à sourcer (fiche v1.0)"),
        "enfouissement": ("la couverture de sol en agriculture de conservation (residuos como cobertura) progresse sur le maïs", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "traitement": ("ingenios (bagasse en cogénération/papier), usines de jus d'orange (écorces), beneficios de café (pulpes et coques)", ETIQUETTE_A_VERIFIER, "filières, à sourcer"),
        "cout_agriculture": ("la bagasse est absorbée par les ingenios ; la paille de maïs pâture ou se collecte en balles localement", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("récolte de maïs mécanisée sur l'irrigué, manuelle sur le pluvial ; coupe de canne manuelle persistante", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "BAGASSE_CANNE_MX", "famille": "Tropical", "nom_fr": "Bagasse de canne à sucre",
            "region": "Córdoba (Veracruz, bassin sucrier du Golfe)", "lat": 18.90, "lon": -96.93,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "bagasse de broyage de canne",
            "production": "canne à sucre : 53 051 361 t (2024, FAOSTAT)", "ratio": "bagasse ≈ 0,28 × canne",
            "gisement": "bagasse ≈ 14,9 Mt/an humide, en ingenios", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [12, 1, 2, 3, 4, 5], "fenetre_note": "campagne de broyage décembre-mai (zafra)",
            "techniques": "coupe mixte manuelle/mécanisée, ingenios concentrés, cogénération partielle",
        },
        {
            "token": "PAILLE_MAIS_MX", "famille": "Céréales", "nom_fr": "Paille de maïs",
            "region": "Irapuato (Guanajuato, Bajío maïsicole)", "lat": 20.67, "lon": -101.35,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille et cannes de maïs criollo",
            "production": "maïs : 24 326 508 t (2024, FAOSTAT)", "ratio": "stover ≈ 1,0 × grain",
            "gisement": "stover ≈ 24 Mt/an brut (récoltable partielle, pâturage traditionnel)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11], "fenetre_note": "récolte d'automne (octobre-novembre)",
            "techniques": "récolte mixte, ensilage fourrager partiel, agriculture de conservation en progression",
        },
        {
            "token": "ECORCE_ORANGE_MX", "famille": "Cultures pérennes", "nom_fr": "Écorces d'orange (industrie du jus)",
            "region": "Martínez de la Torre (Veracruz, bassin des agrumes)", "lat": 20.07, "lon": -97.14,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "écorces et pulpes d'orange pressée",
            "production": "oranges : 4 836 052 t (2024, FAOSTAT)", "ratio": "résidu humide ≈ 0,25 × fruits pressés",
            "gisement": "écorces ≈ 1,2 Mt/an humides, en usines de jus", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11, 12, 1], "fenetre_note": "campagne d'agrumes octobre-janvier",
            "techniques": "vergers de piémont, usines de jus concentré, valorisation en alimentation animale",
        },
        {
            "token": "COQUE_CAFE_MX", "famille": "Tropical", "nom_fr": "Coques et parches de café",
            "region": "Tapachula (Chiapas, ceinture du café)", "lat": 14.91, "lon": -92.26,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "coques (pergamino) et pulpes des beneficios humides",
            "production": "café vert : 194 470 t (2024, FAOSTAT)", "ratio": "coque+parche ≈ 0,20 × café marchand",
            "gisement": "coques/parches ≈ 39 kt/an, en beneficios", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [11, 12, 1, 2], "fenetre_note": "récolte novembre-mars",
            "techniques": "petits producteurs, beneficios humides de village, compostage des pulpes traditionnel",
        },
    ],
},

"Philippines": {
    "nom_fao": "Philippines",
    "portrait": "archipel rizicole et cocotier ; les intrants du master (feuille d'ananas, fibre de coco) sont complétés par la paille et la balle de riz de Central Luzon, la bagasse de Negros et les écorces de banane de Mindanao.",
    "reglementation": {
        "brulage": ("la RA 9003 (Ecological Solid Waste Management Act) et les ordonnances locales restreignent le brûlage à l'air libre ; les chaumes de riz brûlent malgré tout en fin de campagne", ETIQUETTE_A_VERIFIER, "RA 9003 + ordinances locales, à re-vérifier (fiche v1.0)"),
        "enfouissement": ("l'incorporation des chaumes est encouragée par le département de l'Agriculture ; adoption lente", ETIQUETTE_A_VERIFIER, "programmes DA, à sourcer"),
        "traitement": ("balle de riz : combustible des moulins et litière ; bagasse en centrales sucrières de Negros ; écorces de banane en alimentation animale", ETIQUETTE_A_VERIFIER, "filières locales, à sourcer"),
        "cout_agriculture": ("la récolte est à la charge du producteur (moissonneuses de service) ; la balle est gratuite au moulin", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("récolte manuelle/mécanisée mixte, séchage sur routes et aires", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "PAILLE_RIZ_PH", "famille": "Céréales", "nom_fr": "Paille de riz",
            "region": "Cabanatuan (Central Luzon, grenier à riz)", "lat": 15.51, "lon": 120.97,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de riz",
            "production": "riz : 19 087 135 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × paddy",
            "gisement": "paille ≈ 22,9 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [4, 10, 11, 12], "fenetre_note": "campagne principale octobre-décembre, seconde en avril",
            "techniques": "récolte mécanisée de service, andains le long des digues, incorporation en progression",
        },
        {
            "token": "BALLE_RIZ_PH", "famille": "Céréales", "nom_fr": "Balle de riz",
            "region": "Muñoz (Nueva Ecija, rizeries de Central Luzon)", "lat": 15.73, "lon": 120.90,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "balle de riz usiné",
            "production": "riz : 19 087 135 t (2024, FAOSTAT)", "ratio": "balle ≈ 0,20 × riz usiné",
            "gisement": "balle ≈ 3,8 Mt/an, en rizeries", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [4, 10, 11, 12], "fenetre_note": "usinage après chaque campagne",
            "techniques": "séchage/usinage en moulins, balle en combustible de chaudière des rizeries mêmes",
        },
        {
            "token": "BAGASSE_CANNE_PH", "famille": "Tropical", "nom_fr": "Bagasse de canne à sucre",
            "region": "Bacolod (Negros Occidental, capitale sucrière)", "lat": 10.67, "lon": 123.01,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "bagasse de broyage de canne",
            "production": "canne à sucre : 18 694 653 t (2024, FAOSTAT)", "ratio": "bagasse ≈ 0,28 × canne",
            "gisement": "bagasse ≈ 5,2 Mt/an humide, en sucreries", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [11, 12, 1, 2, 3], "fenetre_note": "campagne de broyage novembre-mai",
            "techniques": "récolte manuelle traditionnelle, sucreries concentrées, cogénération établie",
        },
        {
            "token": "ECORCE_BANANE_PH", "famille": "Tropical", "nom_fr": "Écorces de banane (stations de fruits)",
            "region": "Tagum (Davao del Norte, bassin bananier)", "lat": 7.45, "lon": 125.81,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "écorces et rejets de calibrage des stations de conditionnement",
            "production": "bananes : 5 641 129 t (2024, FAOSTAT)", "ratio": "écorces ≈ 0,30 × régime",
            "gisement": "écorces ≈ 1,7 Mt/an, en stations", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "fenetre_note": "récolte hebdomadaire permanente",
            "techniques": "plantations d'exportation, câbles et stations de conditionnement, alimentation animale locale",
        },
    ],
},

"Portugal": {
    "nom_fao": "Portugal",
    "portrait": "bassin oléicole du Nord et subéricole de l'Alentejo ; l'intrant du master (écorce d'eucalyptus) est complété par les grignons d'olive de Trás-os-Montes, la paille de l'Alentejo et les brisures de liège de la filière de Coruche.",
    "reglementation": {
        "brulage": ("le brûlage des résidus agricoles est encadré par la réglementation des feux et les périodes d'interdiction estivale", ETIQUETTE_A_VERIFIER, "règles de feux, à sourcer"),
        "enfouissement": ("pailles pâturées ou incorporées dans l'agriculture mixte de l'Alentejo", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "traitement": ("huileries (grignons — orujo), filière liège : granulés et brisures recyclées depuis longtemps", ETIQUETTE_A_VERIFIER, "filières, à sourcer"),
        "cout_agriculture": ("les grignons se vendent en sacs (maâouns agricoles) ; le liège est acheté au kg à la levée", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("moisson en coopératives, levée du liège hautement qualifiée (strippers)", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "GRIGNON_OLIVE_PT", "famille": "Cultures pérennes", "nom_fr": "Grignons d'olive",
            "region": "Mirandela (Trás-os-Montes, oliveraies traditionnelles)", "lat": 41.49, "lon": -7.18,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "grignons (résidu de pressage) des lagares",
            "production": "olives : 1 340 820 t (2024, FAOSTAT)", "ratio": "grignons ≈ 0,40 × olives triturées",
            "gisement": "grignons ≈ 0,54 Mt/an, en lagares", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11, 12], "fenetre_note": "trituration octobre-janvier",
            "techniques": "oliveraies traditionnelles et modernes, lagares coopératifs, séchage des grignons",
        },
        {
            "token": "PAILLE_BLE_PT", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Évora (Alentejo, plaines céréalières)", "lat": 38.57, "lon": -7.91,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé (campagne modeste, ancrée sur la production nationale réelle)",
            "production": "blé : 81 350 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 81 kt/an (l'Alentejo porte l'essentiel)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6], "fenetre_note": "moisson de juin",
            "techniques": "moisson en coopératives, balles pour litières équines et bovines",
        },
        {
            "token": "BRISURE_LIEGE_PT", "famille": "Forestier", "nom_fr": "Brisures de liège",
            "region": "Coruche (vallée du Tage, subéraies du Sud)", "lat": 38.95, "lon": -8.20,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "brisures, poussières et refus de l'industrie du liège (premier producteur mondial)",
            "production": "pas d'entrée liège dans le bulk FAOSTAT — volume national À SOURCER", "ratio": "brisures/refus ≈ 20-25 % du liège transformé",
            "gisement": "à borner : production portugaise de liège estimée à 150-200 kt/an (ILLUSTRATION)", "etiquette_gisement": ETIQUETTE_A_SOURCER,
            "fenetre": [5, 6, 7], "fenetre_note": "levée du liège (safra) de mai à juillet",
            "techniques": "levée manuelle (strippers), industries de transformation (Amora, Coruche), granulés de liège établis",
        },
    ],
},

"Suisse": {
    "nom_fao": "Switzerland",
    "portrait": "hub Léman (Lavaux) de la flotte ; premier point pays rattaché au hub ch-leman (marc de raisin à Cully même), complété par la paille du Seeland et le marc de pomme thurgovien.",
    "reglementation": {
        "brulage": ("le brûlage des déchets végétaux au champ est interdit par l'ordonnance sur la protection de l'air (OPair), dérogations cantonales rares", ETIQUETTE_REEL, "OPair art. 26a (fiche v0.6)"),
        "enfouissement": ("les sarments et pailles sont broyés et laissés au sol par défaut (pratique viticole et céréalière)", ETIQUETTE_A_VERIFIER, "pratiques, à sourcer"),
        "traitement": ("caves (marc de raisin, distillation encadrée), jus de pommes (cidreries)", ETIQUETTE_A_VERIFIER, "filières, à sourcer"),
        "cout_agriculture": ("récolte motorisée sur de petites surfaces ; le marc part à la distillerie dans un circuit réglementé", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("vendanges largement manuelles en coteaux (UNESCO Lavaux)", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "MARC_RAISIN_CH", "famille": "Cultures pérennes", "nom_fr": "Marc de raisin",
            "region": "Cully (Lavaux, terrasses du hub Léman)", "lat": 46.49, "lon": 6.72,
            "type_point": "hub existant", "hubs_flotte": {"ch-leman": "marc-raisin"},
            "type_biomasse": "marc et rafles de raisin vinifiés — premier rattachement pays au hub ch-leman",
            "production": "raisins : 95 600 t (2024, FAOSTAT)", "ratio": "marc ≈ 0,15 × raisin",
            "gisement": "marc ≈ 14 kt/an, en caves du Léman", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10], "fenetre_note": "vendanges septembre-octobre",
            "techniques": "vendanges manuelles des terrasses, caves de village, distillation réglementée du marc",
        },
        {
            "token": "PAILLE_BLE_CH", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Seeland (plateau de Berne/Fribourg)", "lat": 47.05, "lon": 7.05,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé (campagne nationale modeste, ancrée sur la production réelle)",
            "production": "blé : 311 807 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 0,31 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [7, 8], "fenetre_note": "moisson juillet-août",
            "techniques": "moisson motorisée, balles pour litière (filière équine et avicole suisse)",
        },
        {
            "token": "MARC_POMME_CH", "famille": "Cultures pérennes", "nom_fr": "Marc de pomme (cidreries)",
            "region": "Thurgau (vergers cidricoles de Suisse orientale)", "lat": 47.55, "lon": 9.05,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "marc de pommes pressées (must)",
            "production": "pommes : 213 926 t (2024, FAOSTAT)", "ratio": "marc ≈ 0,20 × pommes",
            "gisement": "marc ≈ 43 kt/an, en cidreries et jus", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10], "fenetre_note": "campagne de pressage septembre-novembre",
            "techniques": "vergers haute-tige, pressoirs coopératifs (must), marc en alimentation animale",
        },
    ],
},

"Viêt Nam": {
    "nom_fao": "Viet Nam",
    "portrait": "deuxième exportateur mondial de riz, capitale du robusta ; l'intrant du master (marc de café) est complété par la paille de riz du Mékong (trois campagnes), la bagasse du Sud-Est, la coque de café des torréfacteurs et la coque de cajou de Bình Phước.",
    "reglementation": {
        "brulage": ("le brûlage des résidus agricoles est découragé par la réglementation de gestion des déchets (décret sur la gestion des déchets agricoles) ; la pratique de la paille de riz se maintient", ETIQUETTE_A_VERIFIER, "réglementation des déchets agricoles, à sourcer"),
        "enfouissement": ("incorporation et compostage partiel de la paille ; retour au sol favorisé dans les bassins intensifs", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "traitement": ("la balle de riz alimente les briqueteries (combustible dominant) ; bagasse en sucreries ; coques de cajou en développement", ETIQUETTE_A_VERIFIER, "filières, à sourcer"),
        "cout_agriculture": ("la moisson mécanisée se vend à la saison ; la paille est souvent donnée contre le ramassage", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("moisson motorisée en forte progression dans le Delta, séchage sur routes", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "PAILLE_RIZ_VN", "famille": "Céréales", "nom_fr": "Paille de riz",
            "region": "Cần Thơ (Delta du Mékong, riz du monde)", "lat": 10.03, "lon": 105.78,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de riz (trois campagnes annuelles)",
            "production": "riz : 43 450 449 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × paddy",
            "gisement": "paille ≈ 52 Mt/an brut (Delta du Mékong : majorité nationale)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "fenetre_note": "trois campagnes continues dans le Delta (fenêtre permanente)",
            "techniques": "moisson-battage motorisée de service, paille en andains, enlèvement par bateaux-barges",
        },
        {
            "token": "BAGASSE_CANNE_VN", "famille": "Tropical", "nom_fr": "Bagasse de canne à sucre",
            "region": "Củ Chi (périphérie de Hô-Chi-Minh-Ville, ceinture sucrière du Sud-Est)", "lat": 11.05, "lon": 106.50,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "bagasse de broyage de canne",
            "production": "canne à sucre : 11 843 772 t (2024, FAOSTAT)", "ratio": "bagasse ≈ 0,28 × canne",
            "gisement": "bagasse ≈ 3,3 Mt/an humide, en sucreries", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11, 12, 1, 2, 3], "fenetre_note": "campagne de broyage octobre-mars",
            "techniques": "récolte manuelle/mécanisée, sucreries du Sud-Est, chaudières bagasse",
        },
        {
            "token": "COQUE_CAFE_VN", "famille": "Tropical", "nom_fr": "Coques et parches de café",
            "region": "Đắk Lắk (Tay Nguyen, ancre des hauts plateaux — distinct du marc déjà placé)", "lat": 12.78, "lon": 108.22,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "coques (parche/pergamino) du café décortiqué après séchage",
            "production": "café vert : 2 015 289 t (2024, FAOSTAT)", "ratio": "coque+parche ≈ 0,20 × café marchand",
            "gisement": "coques/parches ≈ 0,40 Mt/an, en stations de décorticage", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11, 12, 1, 2], "fenetre_note": "récolte octobre-janvier, usinage sec ensuite",
            "techniques": "récolte manuelle, séchage solaire/ mécanique, décorticage en stations, coques en combustible de séchoirs",
        },
        {
            "token": "COQUE_CAJOU_VN", "famille": "Coques & noyaux", "nom_fr": "Coques de cajou (noix de cajou)",
            "region": "Bình Phước (capitale vietnamienne du cajou)", "lat": 11.75, "lon": 106.90,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "coques de noix de cajou (contenant du liquide de coque, CNSL, corrosif — précaution au procédé)",
            "production": "cajou en coque : 306 185 t (2024, FAOSTAT, production nationale)", "ratio": "coque ≈ 0,70 × noix brute",
            "gisement": "coques ≈ 0,21 Mt/an (l'importation de noix brutes africaines double le flux des usines)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [2, 3, 4, 5], "fenetre_note": "campagne de transformation février-juin",
            "techniques": "décorticage mécanique en usines, vapeur de coques en chaudières (CNSL valorisé)",
        },
    ],
},
}

# ---------------------------------------------------------------------------
# Index et contrôles
# ---------------------------------------------------------------------------

def _index():
    """(pays, intrant) pour chaque token."""
    idx = {}
    for pays, fiche in PAYS_BIOMASSES.items():
        for intrant in fiche["intrants"]:
            idx[intrant["token"]] = (pays, intrant)
    return idx

INDEX = _index()


def _verifier_structure(problemes):
    idx = {}
    for pays, fiche in PAYS_BIOMASSES.items():
        for cle in ("nom_fao", "portrait", "reglementation", "intrants"):
            if cle not in fiche:
                problemes.append("pays %s : champ manquant %s" % (pays, cle))
        if len(fiche.get("intrants", [])) < 3:
            problemes.append("pays %s : moins de 3 intrants" % pays)
        for cle in _master.CLEFS_REGLEMENTATION:
            if cle not in fiche["reglementation"]:
                problemes.append("pays %s : poste de réglementation manquant %s" % (pays, cle))
        for intrant in fiche["intrants"]:
            tok = intrant.get("token")
            if not tok:
                problemes.append("pays %s : intrant sans token" % pays)
                continue
            if tok in idx:
                problemes.append("token dupliqué : %s" % tok)
            idx[tok] = (pays, intrant)
            for cle in ("famille", "nom_fr", "region", "lat", "lon", "type_point",
                        "type_biomasse", "production", "ratio", "gisement",
                        "etiquette_gisement", "fenetre", "fenetre_note", "techniques"):
                if cle not in intrant:
                    problemes.append("%s : champ manquant %s" % (tok, cle))
            lat, lon = intrant.get("lat"), intrant.get("lon")
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                problemes.append("%s : GPS hors bornes %s, %s" % (tok, lat, lon))
            for mois in intrant.get("fenetre", []):
                if not 1 <= mois <= 12:
                    problemes.append("%s : mois hors bornes %s" % (tok, mois))
    return idx


def verifier_couverture():
    """Contrôles complets : structure, alignement master, hubs, familles."""
    problemes = []
    idx = _verifier_structure(problemes)

    familles_master = {f["famille"] for f in _master.ATLAS_BIOMASSES_MONDE.values()}
    tokens_master = set(_master.ATLAS_BIOMASSES_MONDE.keys())
    hubs_master = set()
    for f in _master.ATLAS_BIOMASSES_MONDE.values():
        for hub in (f.get("hubs_flotte") or {}):
            hubs_master.add(hub)

    for tok, (pays, intrant) in sorted(idx.items()):
        if intrant["famille"] not in familles_master:
            problemes.append("%s : famille hors master %s" % (tok, intrant["famille"]))
        if tok in tokens_master:
            problemes.append("token en collision avec le master : %s" % tok)
        if intrant["type_point"] not in ("hub existant", "point candidat"):
            problemes.append("%s : type_point inconnu %s" % (tok, intrant["type_point"]))
        for hub in (intrant.get("hubs_flotte") or {}):
            if hub not in hubs_master:
                problemes.append("%s : hub inconnu %s" % (tok, hub))
        if intrant["type_point"] == "hub existant" and not intrant.get("hubs_flotte"):
            problemes.append("%s : point hub sans rattachement hubs_flotte" % tok)

    return problemes


def sommaire():
    lignes = ["Atlas des biomasses locales par pays — World Twin v1.1",
              " Productions FAOSTAT 2024 SOURCÉES ; ratios résidus ILLUSTRATION ;",
              " points GPS approximations de région ; doctrine PI (aucun paramètre VDE).", ""]
    total = 0
    for pays in sorted(PAYS_BIOMASSES, key=lambda p: p.lower()):
        fiche = PAYS_BIOMASSES[pays]
        lignes.append("%s (%s) — %d intrants" % (pays, fiche["nom_fao"], len(fiche["intrants"])))
        for intrant in fiche["intrants"]:
            lignes.append("  %-18s %-16s %-28s %s" % (
                intrant["token"], intrant["famille"], intrant["nom_fr"],
                " / ".join(MOIS_COURTS[m] for m in intrant["fenetre"])))
        total += len(fiche["intrants"])
        lignes.append("")
    lignes.insert(3, " Pays : %d — intrants : %d" % (len(PAYS_BIOMASSES), total))
    return "\n".join(lignes)


def fiche_token(token):
    if token not in INDEX:
        return None
    pays, intrant = INDEX[token]
    fiche_pays = PAYS_BIOMASSES[pays]
    lignes = ["%s — %s" % (intrant["token"], intrant["nom_fr"]), ""]
    lignes.append("Pays : %s (%s)" % (pays, fiche_pays["nom_fao"]))
    lignes.append("Famille : %s" % intrant["famille"])
    lignes.append("Localisation : %s — GPS %.2f, %.2f, approximation de région. Point : %s%s" % (
        intrant["region"], intrant["lat"], intrant["lon"], intrant["type_point"],
        " (rattaché : %s)" % ", ".join(intrant["hubs_flotte"]) if intrant.get("hubs_flotte") else ""))
    lignes.append("Type de biomasse : %s" % intrant["type_biomasse"])
    lignes.append("Volumes : %s [%s]" % (intrant["production"], SOURCE_PRODUCTION))
    lignes.append("Ratio résidu : %s" % intrant["ratio"])
    lignes.append("Gisement : %s [%s]" % (intrant["gisement"], intrant["etiquette_gisement"]))
    lignes.append("Fenêtre saisonnière : %s — %s" % (
        ", ".join(MOIS_COURTS[m] for m in intrant["fenetre"]), intrant["fenetre_note"]))
    lignes.append("Techniques : %s" % intrant["techniques"])
    lignes.append("")
    lignes.append("Réglementation %s (synthèse pays) :" % pays)
    for cle in _master.CLEFS_REGLEMENTATION:
        texte, etiquette, ref = fiche_pays["reglementation"][cle]
        lignes.append("  %s [%s] : %s (réf. %s)" % (cle, etiquette, texte, ref))
    return "\n".join(lignes)


def fiche_pays(nom):
    cible = None
    for pays in PAYS_BIOMASSES:
        if nom.lower() in (pays.lower(), PAYS_BIOMASSES[pays]["nom_fao"].lower()) or nom.lower() == pays.lower():
            cible = pays
            break
    if cible is None:
        return None
    fiche = PAYS_BIOMASSES[cible]
    lignes = ["%s (%s) — atlas des biomasses locales" % (cible, fiche["nom_fao"]), ""]
    lignes.append("Portrait : %s" % fiche["portrait"])
    lignes.append("")
    lignes.append("Réglementation (synthèse à cinq postes) :")
    for cle in _master.CLEFS_REGLEMENTATION:
        texte, etiquette, ref = fiche["reglementation"][cle]
        lignes.append("  %s [%s] : %s (réf. %s)" % (cle, etiquette, texte, ref))
    lignes.append("")
    lignes.append("Intrants (%d) :" % len(fiche["intrants"]))
    for intrant in fiche["intrants"]:
        lignes.append("  %-18s %-16s %s" % (intrant["token"], intrant["famille"], intrant["nom_fr"]))
        lignes.append("    %s — GPS %.2f, %.2f [%s]" % (intrant["region"], intrant["lat"], intrant["lon"], intrant["type_point"]))
        lignes.append("    %s" % intrant["gisement"])
        lignes.append("    fenêtre : %s (%s)" % (
            ", ".join(MOIS_COURTS[m] for m in intrant["fenetre"]), intrant["fenetre_note"]))
    return "\n".join(lignes)


def croisement():
    problemes = verifier_couverture()
    lignes = ["Croisement v1.1 — contrôles complets", ""]
    lignes.append("Pays couverts : %d" % len(PAYS_BIOMASSES))
    lignes.append("Intrants pays : %d (master v1.0 : %d)" % (len(INDEX), len(_master.ATLAS_BIOMASSES_MONDE)))
    familles_pays = {i["famille"] for (_, i) in INDEX.values()}
    familles_master = {f["famille"] for f in _master.ATLAS_BIOMASSES_MONDE.values()}
    lignes.append("Familles pays ⊆ familles master : %s" % ("OK" if familles_pays <= familles_master else "ECART"))
    lignes.append("Familles représentées : %s" % ", ".join(sorted(familles_pays)))
    collision = set(INDEX) & set(_master.ATLAS_BIOMASSES_MONDE)
    lignes.append("Collision de tokens avec le master : %s" % ("AUCUNE" if not collision else ", ".join(sorted(collision))))
    hubs_points = [(tok, p, i["hubs_flotte"]) for tok, (p, i) in sorted(INDEX.items()) if i["type_point"] == "hub existant"]
    lignes.append("Points rattachés à un hub existant : %d — %s" % (len(hubs_points),
                  ", ".join("%s→%s" % (tok, ",".join(sorted(hubs))) for tok, _, hubs in hubs_points)))
    if problemes:
        lignes.append("")
        lignes.append("PROBLÈMES DÉTECTÉS (%d) :" % len(problemes))
        lignes.extend("  - %s" % p for p in problemes)
        lignes.append("")
        lignes.append("CROISEMENT : ECHEC")
        return "\n".join(lignes), 1
    lignes.append("")
    lignes.append("CROISEMENT : OK — toutes les gardes passent.")
    return "\n".join(lignes), 0


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print(sommaire())
        return 0
    if args[0] == "croisement":
        texte, code = croisement()
        print(texte)
        return code
    if args[0] == "pays" and len(args) >= 2:
        texte = fiche_pays(" ".join(args[1:]))
        if texte is None:
            print("Pays inconnu. Pays disponibles : %s" % ", ".join(sorted(PAYS_BIOMASSES)))
            return 1
        print(texte)
        return 0
    texte = fiche_token(args[0])
    if texte is None:
        print("Jeton inconnu. Usage : sommaire | fiche TOKEN | pays NOM | croisement")
        return 1
    print(texte)
    return 0


if __name__ == "__main__":
    sys.exit(main())
