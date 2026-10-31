#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""World Twin v1.3 — Atlas des biomasses d'Asie.

Extension asiatique de la lignée d'atlas (monde v1.0, pays v1.1, vignobles
v1.2) : pour vingt-trois pays d'Asie non encore couverts, les biomasses
LOCALES majeures sont placées sur le globe — région, point GPS
(Global Positioning System, approximation de région, jamais un cadastre),
type, volume, fenêtre saisonnière, techniques culturales — avec, par pays,
une synthèse réglementaire à cinq postes, tous À VÉRIFIER (aucun de ces
pays n'est couvert par les fiches v0.6 des sept hubs).

Soixante-douze intrants, productions SOURCÉES (bulk FAOSTAT 2024, base
statistique de l'Organisation des Nations unies pour l'alimentation et
l'agriculture) et ratios résidus ILLUSTRATION, selon la convention figée
v1.3 : familles Céréales et Tropical uniquement.

Conventions de ratios figées v1.3 (ILLUSTRATION, à borner localement) :
- balle de riz : 0,20 × riz paddy
- bagasse de canne : 0,30 × canne à sucre
- rafles de palmier : 0,22 × régimes
- écorces de manioc : 0,15 × racines fraîches
- paille de blé : 1,2 × grain
- paille d'orge : 1,0 × grain
- paille d'avoine : 1,0 × grain
- résidus de maïs : 0,25 × grain
- tiges de coton : 3 × coton brut non égrené
- tiges de tournesol : 2 × graines
- tiges de jute : 1,8 × fibre
- résidus de théier : 0,6 t/ha/an (tailles)
- palmes de dattier : 2,5 t/ha/an (taille)

Pièges de nommage FAOSTAT consignés : les items s'appellent « Rice »,
« Maize (corn) », « Cassava, fresh », « Tea leaves », « Seed cotton,
unginned », « Jute, raw or retted » et « Dates », les pays « Türkiye »,
« Republic of Korea », « Lao People's Democratic Republic », « Iran
(Islamic Republic of) », « Syrian Arab Republic », « Iraq » et
« Russian Federation ».

Deux gardes nouvelles :
- REGLES_SAISON : par préfixe de jeton, mois autorisés pour la fenêtre des
  points HORS ceinture tropicale (|lat| > 23,5), les points tropicaux étant
  exemptés (production continue)
- BBOX_ASIE : boîte englobante par pays, chaque point doit y rester
  (pièges consignés : Panjakent à la longitude 67,32, Chelyabinsk à la
  longitude 61,40).

Doctrine PI (propriété intellectuelle) : ce module n'embarque AUCUN des six
paramètres du VDE (Vignite Decision Engine) et aucune valeur calibrée.
Seules des données publiques sont versionnées. Étiquette SYNTHÉTIQUE au
registre de développement uniquement.

Bibliothèque standard uniquement, déterministe, aucune dépendance réseau
hors la commande meteo (Open-Meteo, gratuite sans clé).
Usage :
    python3 engine/atlas_biomasses_asie.py                  # sommaire par pays
    python3 engine/atlas_biomasses_asie.py BALLE_RIZ_TH     # fiche d'un intrant
    python3 engine/atlas_biomasses_asie.py pays "Corée du Sud"  # fiche d un pays
    python3 engine/atlas_biomasses_asie.py croisement       # contrôles complets
    python3 engine/atlas_biomasses_asie.py meteo [TOKEN]    # pointage temps réel

Exemples :
    python3 engine/atlas_biomasses_asie.py pays Turquie     # les 8 intrants turcs
    python3 engine/atlas_biomasses_asie.py croisement      # les 72 intrants sous gardes
Réglementation : synthèse à cinq postes par pays, tous À VÉRIFIER.
"""

import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import atlas_biomasses_monde as _master  # noqa: E402  (autorité : familles, hubs, réglementation)
import atlas_biomasses_pays as _pays_v11  # noqa: E402  (autorité : jetons de l'atlas v1.1)
import atlas_vignobles_monde as _vignobles_v12  # noqa: E402  (autorité : jetons des vignobles v1.2)

ETIQUETTE_SOURCÉ = "SOURCÉ"
ETIQUETTE_ILLUSTRATION = "ILLUSTRATION"
ETIQUETTE_REEL = "DONNÉES RÉELLES"
ETIQUETTE_A_VERIFIER = "À VÉRIFIER"

SOURCE_PRODUCTION = ("production FAOSTAT bulk Production_Crops_Livestock_E, "
                     "valeurs 2024 (mise à jour du 31/12/2025)")
ETQ_GISEMENT_SOURCÉ = "SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION"

MOIS_COURTS = _master.MOIS_COURTS

# ---------------------------------------------------------------------------
# Règles saisonnières par préfixe de jeton : mois autorisés pour la fenêtre
# des points HORS ceinture tropicale (|lat| > 23,5). Les points tropicaux
# sont exemptés : production continue, la garde ne s'applique pas.
# ---------------------------------------------------------------------------

REGLES_SAISON = {
    "PAILLE_BLE": [3, 4, 5, 6, 7, 8, 9, 10, 11],
    "PAILLE_ORGE": [3, 4, 5, 6, 7, 8, 9, 10, 11],
    "PAILLE_AVOINE": [7, 8, 9],
    "PAILLE_MAIS": [8, 9, 10, 11, 12],
    "BALLE_RIZ": [1, 2, 3, 4, 5, 9, 10, 11, 12],
    "BAGASSE_CANNE": [10, 11, 12, 1, 2, 3, 4, 5, 6],
    "TIGE_COTON": [9, 10, 11, 12, 1],
    "TIGE_TOURNESOL": [8, 9, 10, 11],
    "TIGE_JUTE": [6, 7, 8, 9],
    "RACHIS_DATTIER": [3, 4, 5],
    "RESIDU_THE": [4, 5, 6, 7, 8, 9, 10, 11],
    "EFB_PALMIER": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "ECORCE_MANIOC": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
}

CEINTURE_TROPICALE = 23.5

# ---------------------------------------------------------------------------
# Boîtes englobantes par pays (latitude min, latitude max, longitude min,
# longitude max). Chaque point d'intrant doit rester dans la boîte de son
# pays : garde anti-coquille GPS. Piège consigné : Panjakent (Tadjikistan)
# est à la longitude 67,32, la boîte tadjike commence donc à 67.
# ---------------------------------------------------------------------------

BBOX_ASIE = {
    "Afghanistan": (29.0, 39.0, 60.0, 75.0),
    "Azerbaïdjan": (38.0, 42.0, 44.0, 51.0),
    "Bangladesh": (20.0, 27.0, 88.0, 93.0),
    "Cambodge": (10.0, 15.0, 102.0, 108.0),
    "Corée du Sud": (33.0, 39.0, 126.0, 130.0),
    "Indonésie": (-9.0, 6.0, 95.0, 141.0),
    "Iran": (25.0, 40.0, 44.0, 64.0),
    "Irak": (29.0, 38.0, 38.0, 49.0),
    "Japon": (30.0, 46.0, 128.0, 146.0),
    "Kazakhstan": (40.0, 56.0, 46.0, 88.0),
    "Kirghizistan": (39.0, 43.0, 69.0, 81.0),
    "Laos": (13.0, 23.0, 100.0, 108.0),
    "Myanmar": (9.0, 29.0, 92.0, 102.0),
    "Népal": (26.0, 31.0, 80.0, 89.0),
    "Ouzbékistan": (37.0, 46.0, 55.0, 74.0),
    "Pakistan": (23.0, 37.0, 60.0, 78.0),
    "Russie": (41.0, 60.0, 37.0, 65.0),
    "Sri Lanka": (5.0, 10.0, 79.0, 82.0),
    "Syrie": (32.0, 37.0, 35.0, 42.0),
    "Tadjikistan": (36.0, 41.0, 67.0, 76.0),
    "Thaïlande": (5.0, 21.0, 97.0, 106.0),
    "Turkménistan": (35.0, 43.0, 52.0, 67.0),
    "Turquie": (35.0, 43.0, 25.0, 45.0),
}

# ---------------------------------------------------------------------------
# Registre des 23 pays d'Asie : fiche pays (portrait, synthèse réglementaire
# à cinq postes, tous À VÉRIFIER car aucun de ces pays n'est couvert par les
# fiches v0.6 des hubs) + intrants. Chaque intrant : token unique (suffixe
# pays), famille, région réelle de production, GPS approximatif, volume ancré
# sur la production FAOSTAT 2024, fenêtre saisonnière, note, techniques.
# ---------------------------------------------------------------------------

PAYS_ASIE = {

# Afghanistan — 3 intrants
"Afghanistan": {
    "nom_fao": "Afghanistan",
    "portrait": "bassins irrigués de l'Ouest et du Nord : blé dominant (Herat, Kunduz), riz et coton des vallées du Nord — agriculture de piémonts et d'oasis.",
    "reglementation": {
        "brulage": ("le brûlage des résidus est pratiqué au nettoyage de printemps et au renouvellement des vergers, sans cadre national identifié à ce jour", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("les résidus servent d'abord de fourrage et de combustible domestique avant tout retour au sol", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("aucune filière de valorisation structurée identifiée à ce jour, l'économie des résidus reste domestique", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte est manuelle, le coût dominant est la main-d'œuvre familiale", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("petites structures familiales, mécanisation localisée dans les bassins irrigués", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "PAILLE_BLE_AF", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Herat (bassin céréalier de l'Ouest)", "lat": 34.34, "lon": 62.21,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé, chaumes et glumes",
            "production": "blé : 5 200 000 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × grain",
            "gisement": "paille ≈ 6,2 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [5, 6, 7], "fenetre_note": "moisson de mai à juillet, point sous garde",
            "techniques": "moisson motorisée ou manuelle, balles rondes, fourrage dominant",
        },
        {
            "token": "BALLE_RIZ_AF", "famille": "Céréales", "nom_fr": "Balle de riz",
            "region": "Kunduz (rizière du Nord)", "lat": 36.72, "lon": 68.86,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "balle de riz (coque), coproduit du décorticage",
            "production": "riz paddy : 654 000 t (2024, FAOSTAT)", "ratio": "balle ≈ 0,20 × riz paddy",
            "gisement": "balle ≈ 130 800 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11], "fenetre_note": "moisson d'octobre à novembre, point sous garde",
            "techniques": "moisson manuelle, décorticage villageois",
        },
        {
            "token": "TIGE_COTON_AF", "famille": "Céréales", "nom_fr": "Tiges de coton",
            "region": "Taloqan (Takhar, coton du Nord)", "lat": 36.70, "lon": 69.53,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges et racines de cotonnier arrachées après récolte",
            "production": "coton brut : 120 508 t (2024, FAOSTAT)", "ratio": "tiges ≈ 3 × coton brut non égrené",
            "gisement": "tiges de coton ≈ 361 524 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [11, 12], "fenetre_note": "récolte de novembre à décembre, point sous garde",
            "techniques": "récolte manuelle, andains au champ",
        },
    ],
},

# Azerbaïdjan — 3 intrants
"Azerbaïdjan": {
    "nom_fao": "Azerbaijan",
    "portrait": "ceinture céréalière et cotonnière du bas-Kura (Ganja, Barda), orge de piémont (Qazax) — agriculture post-soviétique irriguée.",
    "reglementation": {
        "brulage": ("le brûlage des chaumes est documenté localement, l'encadrement national reste à sourcer", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("la paille est largement récupérée comme fourrage et litière, retour au sol en partage", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("aucune filière de valorisation énergétique identifiée à ce jour", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte est mécanisée dans les grandes fermes, artisanale ailleurs", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("main-d'œuvre rurale disponible, saisonnalité forte des récoltes", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "TIGE_COTON_AZ", "famille": "Céréales", "nom_fr": "Tiges de coton",
            "region": "Barda (coton du bas-Kura)", "lat": 40.39, "lon": 47.13,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges et racines de cotonnier arrachées après récolte",
            "production": "coton brut : 237 651 t (2024, FAOSTAT)", "ratio": "tiges ≈ 3 × coton brut non égrené",
            "gisement": "tiges de coton ≈ 712 953 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11], "fenetre_note": "récolte d'octobre à novembre, point sous garde",
            "techniques": "récolte mécanique, arrachage des tiges",
        },
        {
            "token": "PAILLE_BLE_AZ", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Ganja (bassin céréalier de l'Ouest)", "lat": 40.68, "lon": 46.36,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé, chaumes et glumes",
            "production": "blé : 1 901 046 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × grain",
            "gisement": "paille ≈ 2,3 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6, 7], "fenetre_note": "moisson de juin à juillet, point sous garde",
            "techniques": "moisson motorisée, balles rondes, fourrage",
        },
        {
            "token": "PAILLE_ORGE_AZ", "famille": "Céréales", "nom_fr": "Paille d'orge",
            "region": "Qazax (piémonts du Nord-Ouest)", "lat": 41.10, "lon": 45.36,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille d'orge, chaumes et barbes",
            "production": "orge : 1 067 119 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 1,1 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [5, 6], "fenetre_note": "moisson de mai à juin, point sous garde",
            "techniques": "moisson motorisée, balles rondes, fourrage",
        },
    ],
},

# Bangladesh — 4 intrants
"Bangladesh": {
    "nom_fao": "Bangladesh",
    "portrait": "delta du Gange et du Brahmapoutre : riz omniprésent (60 Mt), jute du Faridpur (fibre historique), maïs fourrager en expansion, blé d'hiver.",
    "reglementation": {
        "brulage": ("le brûlage des balles de riz et des tiges est pratiqué malgré les interdictions locales signalées, cadre national à sourcer", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("la paille de riz est incorporée au sol ou sert de fourrage, la balle alimente les briqueteries", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("la balle de riz alimente déjà des chaudières informelles, aucun réseau structuré identifié à ce jour", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la main-d'œuvre est abondante, la collecte manuelle domine hors zones mécanisées", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("petites parcelles, récolte en grande partie manuelle", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "TIGE_JUTE_BD", "famille": "Céréales", "nom_fr": "Tiges de jute",
            "region": "Faridpur (bassin jutier du delta)", "lat": 23.60, "lon": 89.83,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges de jute après défibrage (moelle résiduelle)",
            "production": "jute : 2 086 101 t (2024, FAOSTAT)", "ratio": "tiges ≈ 1,8 × fibre",
            "gisement": "tiges de jute ≈ 3,8 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [7, 8, 9], "fenetre_note": "arrachage de juillet à septembre, point sous garde",
            "techniques": "rouissage traditionnel, défibrage manuel ou mécanique",
        },
        {
            "token": "BALLE_RIZ_BD", "famille": "Céréales", "nom_fr": "Balle de riz",
            "region": "Mymensingh (rizière du Bengale)", "lat": 24.75, "lon": 90.40,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "balle de riz (coque), coproduit du décorticage",
            "production": "riz paddy : 60 570 453 t (2024, FAOSTAT)", "ratio": "balle ≈ 0,20 × riz paddy",
            "gisement": "balle ≈ 12,1 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [11, 12, 1, 2, 3, 4], "fenetre_note": "moissons d'amon et de boro, point sous garde",
            "techniques": "moisson manuelle ou motorisée, décorticage en rizerie",
        },
        {
            "token": "PAILLE_MAIS_BD", "famille": "Céréales", "nom_fr": "Résidus de maïs",
            "region": "Rangpur (bassin maïsier du Nord)", "lat": 25.75, "lon": 89.25,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges, spathes et rafles de maïs",
            "production": "maïs : 4 592 508 t (2024, FAOSTAT)", "ratio": "résidus ≈ 0,25 × grain",
            "gisement": "résidus de maïs ≈ 1,1 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11], "fenetre_note": "récolte d'octobre à novembre, point sous garde",
            "techniques": "récolte des épis, séchage, tiges au champ",
        },
        {
            "token": "PAILLE_BLE_BD", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Dinajpur (bassin céréalier du Nord)", "lat": 25.62, "lon": 88.64,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé, chaumes et glumes",
            "production": "blé : 1 172 242 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × grain",
            "gisement": "paille ≈ 1,4 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [3, 4], "fenetre_note": "moisson de mars à avril (blé d'hiver), point sous garde",
            "techniques": "moisson motorisée, balles rondes, fourrage dominant",
        },
    ],
},

# Cambodge — 2 intrants
"Cambodge": {
    "nom_fao": "Cambodia",
    "portrait": "riz du Tonlé Sap et du Battambang (14 Mt), manioc de Kampong Cham en forte croissance — agriculture de plaine tropicale.",
    "reglementation": {
        "brulage": ("le brûlage des résidus de riz est courant en saison sèche, encadrement à sourcer", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("la paille est broutée par le bétail ou brûlée, le labour de couverture progresse", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("la balle de riz alimente quelques unités de cogénération, filière émergente", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte est manuelle, le transport fluvial structure les coûts", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("main-d'œuvre rurale abondante, moissons en grande partie manuelles", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "BALLE_RIZ_KH", "famille": "Céréales", "nom_fr": "Balle de riz",
            "region": "Battambang (bassin du Tonlé Sap)", "lat": 13.10, "lon": 103.20,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "balle de riz (coque), coproduit du décorticage",
            "production": "riz paddy : 14 200 000 t (2024, FAOSTAT)", "ratio": "balle ≈ 0,20 × riz paddy",
            "gisement": "balle ≈ 2,8 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [11, 12, 1, 2, 3], "fenetre_note": "moisson de novembre à mars, point tropical exempté",
            "techniques": "moisson manuelle ou motorisée, décorticage villageois",
        },
        {
            "token": "ECORCE_MANIOC_KH", "famille": "Tropical", "nom_fr": "Écorces de manioc",
            "region": "Kampong Cham (bassin manioc de l'Est)", "lat": 12.00, "lon": 105.46,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "écorces et épluchures de manioc",
            "production": "manioc : 14 261 306 t (2024, FAOSTAT)", "ratio": "écorces ≈ 0,15 × racines",
            "gisement": "écorces ≈ 2,1 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "fenetre_note": "récolte continue, point tropical exempté",
            "techniques": "récolte manuelle, épluchage en amidonnerie",
        },
    ],
},

# Corée du Sud — 2 intrants
"Corée du Sud": {
    "nom_fao": "Republic of Korea",
    "portrait": "riziculture de Jeolla (Jeonju, Iksan), orge d'hiver en succession — montagnes boisées, surfaces agricoles restreintes et mécanisées.",
    "reglementation": {
        "brulage": ("le brûlage des résidus est réglementé au niveau national et restreint par les collectivités, texte à sourcer", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("l'incorporation de la paille au sol est encouragée après les récoltes de riz", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("des filières de valorisation de la paille et de la balle existent (litière, combustible rural)", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la mécanisation est totale, la collecte est un service contractuel", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("vieillissement de la main-d'œuvre agricole, recours aux saisonniers", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "BALLE_RIZ_KR", "famille": "Céréales", "nom_fr": "Balle de riz",
            "region": "Jeonju (Jeolla, rizière du Sud-Ouest)", "lat": 35.82, "lon": 127.15,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "balle de riz (coque), coproduit du décorticage",
            "production": "riz paddy : 4 783 114 t (2024, FAOSTAT)", "ratio": "balle ≈ 0,20 × riz paddy",
            "gisement": "balle ≈ 956 623 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11], "fenetre_note": "moisson d'octobre à novembre, point sous garde",
            "techniques": "moisson motorisée, séchage, décorticage en rizerie",
        },
        {
            "token": "PAILLE_ORGE_KR", "famille": "Céréales", "nom_fr": "Paille d'orge",
            "region": "Iksan (Jeolla, orge d'hiver)", "lat": 35.94, "lon": 126.95,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille d'orge, chaumes et barbes",
            "production": "orge : 47 730 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 47 730 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [5, 6], "fenetre_note": "moisson de mai à juin (orge d'hiver), point sous garde",
            "techniques": "moisson motorisée, balles rondes, fourrage",
        },
    ],
},

# Indonésie — 5 intrants
"Indonésie": {
    "nom_fao": "Indonesia",
    "portrait": "archipel : premier producteur mondial de palmier à huile (Riau, 243 Mt de régimes), riz de Java (53 Mt), canne de Lampung, manioc de Grobogan — production continue tropicale.",
    "reglementation": {
        "brulage": ("le brûlage est restreint par la réglementation sur les feux de végétation, pratiques résiduelles documentées à Sumatra et Bornéo", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("les rafles de palmier sont épandues en inter-rangs de plantation, pratique standard des huileries", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("les huileries valorisent déjà une part des rafles (compost, combustible de chaudière), marché concurrentiel", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la logistique insulaire domine les coûts de collecte", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("plantations structurées pour le palmier, riziculture familiale à Java", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "EFB_PALMIER_ID", "famille": "Tropical", "nom_fr": "Rafles de palmier à huile",
            "region": "Riau (bassin palmier de Sumatra)", "lat": 0.53, "lon": 101.44,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "rafles de régimes de palmier à huile",
            "production": "régimes de palmier : 243 000 000 t (2024, FAOSTAT)", "ratio": "rafles ≈ 0,22 × régimes",
            "gisement": "rafles ≈ 53,5 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "fenetre_note": "régimes toute l'année, point tropical exempté",
            "techniques": "récolte des régimes, stérilisation et pressage en huilerie",
        },
        {
            "token": "BALLE_RIZ_ID", "famille": "Céréales", "nom_fr": "Balle de riz",
            "region": "Karawang (rizière de Java Ouest)", "lat": -6.30, "lon": 107.32,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "balle de riz (coque), coproduit du décorticage",
            "production": "riz paddy : 53 142 727 t (2024, FAOSTAT)", "ratio": "balle ≈ 0,20 × riz paddy",
            "gisement": "balle ≈ 10,6 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "fenetre_note": "trois campagnes de riz par an, point tropical exempté",
            "techniques": "moisson motorisée, usinage, décorticage en rizerie",
        },
        {
            "token": "BAGASSE_CANNE_ID", "famille": "Tropical", "nom_fr": "Bagasse de canne",
            "region": "Lampung (bassin sucrier du Sud)", "lat": -5.40, "lon": 105.33,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "bagasse de canne à sucre, coproduit du broyage",
            "production": "canne à sucre : 32 000 000 t (2024, FAOSTAT)", "ratio": "bagasse ≈ 0,30 × canne",
            "gisement": "bagasse ≈ 9,6 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [5, 6, 7, 8, 9, 10, 11, 12], "fenetre_note": "campagne de broyage de mai à décembre, point tropical exempté",
            "techniques": "récolte manuelle ou mécanique, broyage en sucrerie",
        },
        {
            "token": "ECORCE_MANIOC_ID", "famille": "Tropical", "nom_fr": "Écorces de manioc",
            "region": "Grobogan (bassin manioc de Java Centre)", "lat": -7.08, "lon": 110.82,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "écorces et épluchures de manioc",
            "production": "manioc : 15 624 038 t (2024, FAOSTAT)", "ratio": "écorces ≈ 0,15 × racines",
            "gisement": "écorces ≈ 2,3 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "fenetre_note": "récolte continue, point tropical exempté",
            "techniques": "récolte manuelle, épluchage en unités de transformation",
        },
        {
            "token": "PAILLE_MAIS_ID", "famille": "Céréales", "nom_fr": "Résidus de maïs",
            "region": "Jember (Java Est)", "lat": -8.20, "lon": 113.70,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges, spathes et rafles de maïs",
            "production": "maïs : 15 138 912 t (2024, FAOSTAT)", "ratio": "résidus ≈ 0,25 × grain",
            "gisement": "résidus de maïs ≈ 3,8 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "fenetre_note": "double campagne de maïs, point tropical exempté",
            "techniques": "récolte des grains, broyage des tiges au champ",
        },
    ],
},

# Iran — 4 intrants
"Iran": {
    "nom_fao": "Iran (Islamic Republic of)",
    "portrait": "blé de Gorgan et de la Caspienne (16,75 Mt), orge du Khorassan, riz du Guilan, dattes de la ceinture des oasis (Kerman, Bam).",
    "reglementation": {
        "brulage": ("le brûlage des résidus est restreint par la réglementation environnementale, application variable à sourcer", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("la paille sert de fourrage dominant dans l'élevage ovin, retour au sol en partage", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("aucune filière de valorisation structurée identifiée à ce jour", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte est mécanisée dans les grands bassins céréaliers", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("mécanisation céréalière avancée, taille des palmiers manuelle", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "PAILLE_BLE_IR", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Gorgan (bassin de la Caspienne)", "lat": 36.84, "lon": 54.44,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé, chaumes et glumes",
            "production": "blé : 16 750 000 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × grain",
            "gisement": "paille ≈ 20,1 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [5, 6, 7], "fenetre_note": "moisson de mai à juillet, point sous garde",
            "techniques": "moisson motorisée, balles rondes, fourrage dominant",
        },
        {
            "token": "PAILLE_ORGE_IR", "famille": "Céréales", "nom_fr": "Paille d'orge",
            "region": "Mashhad (Khorassan)", "lat": 36.30, "lon": 59.60,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille d'orge, chaumes et barbes",
            "production": "orge : 4 000 000 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 4 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [5, 6], "fenetre_note": "moisson de mai à juin, point sous garde",
            "techniques": "moisson motorisée, pâturage des chaumes courant",
        },
        {
            "token": "BALLE_RIZ_IR", "famille": "Céréales", "nom_fr": "Balle de riz",
            "region": "Rasht (Guilan, rizière caspienne)", "lat": 37.28, "lon": 49.58,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "balle de riz (coque), coproduit du décorticage",
            "production": "riz paddy : 3 478 820 t (2024, FAOSTAT)", "ratio": "balle ≈ 0,20 × riz paddy",
            "gisement": "balle ≈ 695 764 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10], "fenetre_note": "moisson de septembre à octobre, point sous garde",
            "techniques": "moisson motorisée, décorticage villageois",
        },
        {
            "token": "RACHIS_DATTIER_IR", "famille": "Tropical", "nom_fr": "Palmes et rachis de palmier dattier",
            "region": "Bam (Kerman, ceinture des oasis)", "lat": 29.11, "lon": 58.37,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "palmes et rachis issus de la taille du palmier dattier",
            "production": "dattes : 1 182 144 t — surface 135 540 ha (2024, FAOSTAT), l'ancrage palmes et rachis est un ratio par hectare", "ratio": "palmes ≈ 2,5 t/ha/an (taille)",
            "gisement": "palmes et rachis ≈ 339 000 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [3, 4, 5], "fenetre_note": "taille printanière des palmiers, point sous garde",
            "techniques": "taille manuelle, déchiquetage au verger",
        },
    ],
},

# Irak — 2 intrants
"Irak": {
    "nom_fao": "Iraq",
    "portrait": "dattiers historiques de Basra (surface 256 758 ha), blé de la Djéziré et de Diyala — agriculture irriguée mésopotamienne.",
    "reglementation": {
        "brulage": ("le brûlage des palmes et chaumes est documenté, encadrement national à sourcer", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("les palmes servent d'ombrage, de litière et de combustible domestique", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("aucune filière de valorisation structurée identifiée à ce jour, les vergers dattiers concentrent les tailles", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte des palmes est manuelle au verger", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("taille et récolte des dattiers manuelles, savoir-faire oasien", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "RACHIS_DATTIER_IQ", "famille": "Tropical", "nom_fr": "Palmes et rachis de palmier dattier",
            "region": "Basra (vergers dattiers du Chatt al-Arab)", "lat": 30.51, "lon": 47.78,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "palmes et rachis issus de la taille du palmier dattier",
            "production": "dattes : 587 190 t — surface 256 758 ha (2024, FAOSTAT), l'ancrage palmes et rachis est un ratio par hectare", "ratio": "palmes ≈ 2,5 t/ha/an (taille)",
            "gisement": "palmes et rachis ≈ 642 000 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [3, 4, 5], "fenetre_note": "taille printanière des palmiers, point sous garde",
            "techniques": "taille manuelle (machette), déchiquetage au verger",
        },
        {
            "token": "PAILLE_BLE_IQ", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Diyala (bassin céréalier de l'Est)", "lat": 33.75, "lon": 44.52,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé, chaumes et glumes",
            "production": "blé : 5 234 171 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × grain",
            "gisement": "paille ≈ 6,3 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [4, 5], "fenetre_note": "moisson d'avril à mai, point sous garde",
            "techniques": "moisson motorisée, balles rondes, pâturage des chaumes",
        },
    ],
},

# Japon — 2 intrants
"Japon": {
    "nom_fao": "Japan",
    "portrait": "riz de Niigata (10,1 Mt), blé de Hokkaido — petites structures, mécanisation fine, calendriers culturaux précis.",
    "reglementation": {
        "brulage": ("le brûlage de la paille de riz est réglementé et en recul, interdictions préfectorales documentées", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("l'incorporation précoce de la paille au sol est la pratique encouragée", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("la paille alimente litière, fourrage et matériaux, la balle des rizeries est partiellement valorisée", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte est mécanisée et contractuelle, coût élevé de la main-d'œuvre", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("vieillissement marqué, coopératives structurées (nokyo)", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "BALLE_RIZ_JP", "famille": "Céréales", "nom_fr": "Balle de riz",
            "region": "Niigata (plaine du Shinano)", "lat": 37.92, "lon": 139.05,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "balle de riz (coque), coproduit du décorticage",
            "production": "riz paddy : 10 142 000 t (2024, FAOSTAT)", "ratio": "balle ≈ 0,20 × riz paddy",
            "gisement": "balle ≈ 2 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10, 11], "fenetre_note": "moisson de septembre à novembre, point sous garde",
            "techniques": "moisson motorisée, séchage, décorticage en rizerie",
        },
        {
            "token": "PAILLE_BLE_JP", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Obihiro (Tokachi, Hokkaido)", "lat": 42.92, "lon": 143.20,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé, chaumes et glumes",
            "production": "blé : 1 029 000 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × grain",
            "gisement": "paille ≈ 1,2 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [7, 8], "fenetre_note": "moisson de juillet à août, point sous garde",
            "techniques": "moisson motorisée, pressage en balles, fourrage d'hiver",
        },
    ],
},

# Kazakhstan — 4 intrants
"Kazakhstan": {
    "nom_fao": "Kazakhstan",
    "portrait": "steppe céréalière du Nord (blé d'export 18,6 Mt, Akmola, Kostanay), orge, tournesol du Petropavl, coton du Turkestan — grandes cultures de latitudes hautes.",
    "reglementation": {
        "brulage": ("le brûlage des chaumes est restreint par la réglementation sur les steppes, application à sourcer", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("le semis direct et la conservation des sols progressent, la paille reste majoritairement au sol", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("aucune filière de valorisation structurée identifiée à ce jour", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte est mécanisée à grande échelle, distances de transport élevées", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("fermes de très grande taille, main-d'œuvre saisonnière localisée", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "PAILLE_BLE_KZ", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Kokshetau (Akmola, steppe céréalière)", "lat": 53.29, "lon": 69.42,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé, chaumes et glumes",
            "production": "blé : 18 576 694 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × grain",
            "gisement": "paille ≈ 22,3 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [8, 9], "fenetre_note": "moisson d'août à septembre, point sous garde",
            "techniques": "moisson motorisée, balles rondes, export de paille possible",
        },
        {
            "token": "PAILLE_ORGE_KZ", "famille": "Céréales", "nom_fr": "Paille d'orge",
            "region": "Kostanay (steppe du Nord)", "lat": 53.22, "lon": 63.62,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille d'orge, chaumes et barbes",
            "production": "orge : 3 839 684 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 3,8 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [8, 9], "fenetre_note": "moisson d'août à septembre, point sous garde",
            "techniques": "moisson motorisée, balles rondes",
        },
        {
            "token": "TIGE_TOURNESOL_KZ", "famille": "Céréales", "nom_fr": "Tiges de tournesol",
            "region": "Petropavl (Kazakhstan du Nord)", "lat": 54.87, "lon": 69.18,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges et calathides de tournesol",
            "production": "tournesol : 1 834 397 t (2024, FAOSTAT)", "ratio": "tiges ≈ 2 × graines",
            "gisement": "tiges de tournesol ≈ 3,7 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10], "fenetre_note": "récolte de septembre à octobre, point sous garde",
            "techniques": "moisson motorisée, broyage des tiges",
        },
        {
            "token": "TIGE_COTON_KZ", "famille": "Céréales", "nom_fr": "Tiges de coton",
            "region": "Turkestan (oasis cotonnière du Sud)", "lat": 43.29, "lon": 68.25,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges et racines de cotonnier arrachées après récolte",
            "production": "coton brut : 301 661 t (2024, FAOSTAT)", "ratio": "tiges ≈ 3 × coton brut non égrené",
            "gisement": "tiges de coton ≈ 904 984 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11], "fenetre_note": "récolte d'octobre à novembre, point sous garde",
            "techniques": "récolte mécanique, arrachage des tiges",
        },
    ],
},

# Kirghizistan — 3 intrants
"Kirghizistan": {
    "nom_fao": "Kyrgyzstan",
    "portrait": "vallées de Tchouï et de Talas (blé, orge), coton de Djalal-Abad — agriculture de montagne et de piémonts.",
    "reglementation": {
        "brulage": ("le brûlage des résidus est pratiqué au printemps, encadrement à sourcer", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("la paille sert de fourrage d'hiver dominant pour l'élevage", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("aucune filière de valorisation structurée identifiée à ce jour", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte est artisanale, le coût dominant est le fourrage", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("fermes familiales, élevage et grandes cultures en partage", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "TIGE_COTON_KG", "famille": "Céréales", "nom_fr": "Tiges de coton",
            "region": "Jalal-Abad (vallée de Ferghana kirghize)", "lat": 40.93, "lon": 72.78,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges et racines de cotonnier arrachées après récolte",
            "production": "coton brut : 46 338 t (2024, FAOSTAT)", "ratio": "tiges ≈ 3 × coton brut non égrené",
            "gisement": "tiges de coton ≈ 139 014 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11], "fenetre_note": "récolte d'octobre à novembre, point sous garde",
            "techniques": "récolte manuelle, andains au champ",
        },
        {
            "token": "PAILLE_BLE_KG", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Chuy (vallée de Bichkek)", "lat": 42.87, "lon": 74.59,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé, chaumes et glumes",
            "production": "blé : 664 830 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × grain",
            "gisement": "paille ≈ 797 796 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [7, 8], "fenetre_note": "moisson de juillet à août, point sous garde",
            "techniques": "moisson motorisée, balles rondes, fourrage d'hiver",
        },
        {
            "token": "PAILLE_ORGE_KG", "famille": "Céréales", "nom_fr": "Paille d'orge",
            "region": "Talas (vallée du Nord-Ouest)", "lat": 42.52, "lon": 72.24,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille d'orge, chaumes et barbes",
            "production": "orge : 611 050 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 611 050 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6, 7], "fenetre_note": "moisson de juin à juillet, point sous garde",
            "techniques": "moisson motorisée, balles rondes, fourrage",
        },
    ],
},

# Laos — 2 intrants
"Laos": {
    "nom_fao": "Lao People's Democratic Republic",
    "portrait": "riz du Mékong (Savannakhet, 3,8 Mt), manioc des plateaux en croissance — agriculture tropicale de vallées.",
    "reglementation": {
        "brulage": ("le brûlage des résidus de riz est courant en saison sèche, encadrement à sourcer", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("la paille sert de fourrage et de paillage, le feu de nettoyage persiste", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("aucune filière de valorisation structurée identifiée à ce jour", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte est manuelle, l'éloignement des plateaux structure les coûts", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("riziculture familiale, récolte manuelle dominante", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "BALLE_RIZ_LA", "famille": "Céréales", "nom_fr": "Balle de riz",
            "region": "Savannakhet (bassin du Mékong)", "lat": 16.60, "lon": 104.75,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "balle de riz (coque), coproduit du décorticage",
            "production": "riz paddy : 3 750 740 t (2024, FAOSTAT)", "ratio": "balle ≈ 0,20 × riz paddy",
            "gisement": "balle ≈ 750 148 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [11, 12, 1, 2, 3], "fenetre_note": "moisson de novembre à mars, point tropical exempté",
            "techniques": "moisson manuelle ou motorisée, décorticage villageois",
        },
        {
            "token": "ECORCE_MANIOC_LA", "famille": "Tropical", "nom_fr": "Écorces de manioc",
            "region": "Vientiane (plaines du Mékong)", "lat": 18.20, "lon": 102.80,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "écorces et épluchures de manioc",
            "production": "manioc : 7 402 000 t (2024, FAOSTAT)", "ratio": "écorces ≈ 0,15 × racines",
            "gisement": "écorces ≈ 1,1 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "fenetre_note": "récolte continue, point tropical exempté",
            "techniques": "récolte manuelle, épluchage en amidonnerie",
        },
    ],
},

# Myanmar — 3 intrants
"Myanmar": {
    "nom_fao": "Myanmar",
    "portrait": "delta de l'Ayeyarwady (riz 27,7 Mt, Bogale), maïs des états Shan (Taunggyi), canne de la Chindwin (Monywa) — grenier tropical sous-équipé.",
    "reglementation": {
        "brulage": ("le brûlage des résidus de riz est courant en saison sèche, encadrement à sourcer", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("la paille reste au sol ou sert de fourrage, le labour de couverture domine", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("aucune filière de valorisation structurée identifiée à ce jour", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte est manuelle, l'infrastructure de transformation est limitée", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("main-d'œuvre rurale abondante, moissons manuelles dominantes", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "BALLE_RIZ_MM", "famille": "Céréales", "nom_fr": "Balle de riz",
            "region": "Bogale (delta de l'Ayeyarwady)", "lat": 16.30, "lon": 95.10,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "balle de riz (coque), coproduit du décorticage",
            "production": "riz paddy : 27 650 000 t (2024, FAOSTAT)", "ratio": "balle ≈ 0,20 × riz paddy",
            "gisement": "balle ≈ 5,5 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [11, 12, 1, 2, 3, 4], "fenetre_note": "moisson de novembre à avril, point tropical exempté",
            "techniques": "moisson manuelle ou motorisée, décorticage en rizerie",
        },
        {
            "token": "PAILLE_MAIS_MM", "famille": "Céréales", "nom_fr": "Résidus de maïs",
            "region": "Taunggyi (plateaux des états Shan)", "lat": 20.78, "lon": 97.04,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges, spathes et rafles de maïs",
            "production": "maïs : 2 050 000 t (2024, FAOSTAT)", "ratio": "résidus ≈ 0,25 × grain",
            "gisement": "résidus de maïs ≈ 512 500 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [8, 9, 10], "fenetre_note": "récolte d'août à octobre, point tropical exempté",
            "techniques": "récolte des épis, tiges broyées ou broutées au champ",
        },
        {
            "token": "BAGASSE_CANNE_MM", "famille": "Tropical", "nom_fr": "Bagasse de canne",
            "region": "Monywa (vallée de la Chindwin)", "lat": 22.00, "lon": 95.13,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "bagasse de canne à sucre, coproduit du broyage",
            "production": "canne à sucre : 11 997 881 t (2024, FAOSTAT)", "ratio": "bagasse ≈ 0,30 × canne",
            "gisement": "bagasse ≈ 3,6 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [11, 12, 1, 2, 3], "fenetre_note": "campagne de broyage de novembre à mars, point tropical exempté",
            "techniques": "coupe manuelle, broyage en sucrerie",
        },
    ],
},

# Népal — 3 intrants
"Népal": {
    "nom_fao": "Nepal",
    "portrait": "Terai (riz de Chitwan 6 Mt, blé de Rupandehi) et collines (maïs de Dang) — agriculture de plaine et de versants.",
    "reglementation": {
        "brulage": ("le brûlage des résidus de blé avant la mousson est documenté, encadrement à sourcer", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("la paille sert de fourrage dominant (buffle, bovin), retour au sol en partage", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("aucune filière de valorisation structurée identifiée à ce jour", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte est manuelle, le fourrage valorise la paille", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("petites parcelles, exode rural et main-d'œuvre féminine dominante", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "BALLE_RIZ_NP", "famille": "Céréales", "nom_fr": "Balle de riz",
            "region": "Chitwan (Terai central)", "lat": 27.53, "lon": 84.35,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "balle de riz (coque), coproduit du décorticage",
            "production": "riz paddy : 5 955 500 t (2024, FAOSTAT)", "ratio": "balle ≈ 0,20 × riz paddy",
            "gisement": "balle ≈ 1,2 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11, 12], "fenetre_note": "moisson d'octobre à décembre, point sous garde",
            "techniques": "moisson manuelle ou motorisée, décorticage villageois",
        },
        {
            "token": "PAILLE_MAIS_NP", "famille": "Céréales", "nom_fr": "Résidus de maïs",
            "region": "Dang (vallées du mid-West)", "lat": 28.10, "lon": 82.30,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges, spathes et rafles de maïs",
            "production": "maïs : 3 193 869 t (2024, FAOSTAT)", "ratio": "résidus ≈ 0,25 × grain",
            "gisement": "résidus de maïs ≈ 798 467 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10, 11], "fenetre_note": "récolte de septembre à novembre, point sous garde",
            "techniques": "récolte des épis, séchage sur les toits, tiges au champ",
        },
        {
            "token": "PAILLE_BLE_NP", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Rupandehi (Terai ouest)", "lat": 27.52, "lon": 83.28,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé, chaumes et glumes",
            "production": "blé : 2 035 559 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × grain",
            "gisement": "paille ≈ 2,4 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [3, 4, 5], "fenetre_note": "moisson de mars à mai, point sous garde",
            "techniques": "moisson motorisée, balles rondes, fourrage dominant",
        },
    ],
},

# Ouzbékistan — 2 intrants
"Ouzbékistan": {
    "nom_fao": "Uzbekistan",
    "portrait": "vallée de Ferghana et Samarcande : coton historique (2,9 Mt non égrené), blé d'autosuffisance (6,7 Mt) — oasis irriguées.",
    "reglementation": {
        "brulage": ("le brûlage des tiges de coton et des chaumes est restreint par décret, application à sourcer", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("les tiges de coton sont retournées au sol sur ordonnancement étatique", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("aucune filière de valorisation structurée identifiée à ce jour", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte est organisée par les clusters cotonniers étatiques", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("récolte du coton en partie manuelle, salariat de campagne", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "TIGE_COTON_UZ", "famille": "Céréales", "nom_fr": "Tiges de coton",
            "region": "Ferghana (vallée cotonnière)", "lat": 40.38, "lon": 71.78,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges et racines de cotonnier arrachées après récolte",
            "production": "coton brut : 2 938 089 t (2024, FAOSTAT)", "ratio": "tiges ≈ 3 × coton brut non égrené",
            "gisement": "tiges de coton ≈ 8,8 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11], "fenetre_note": "récolte d'octobre à novembre, point sous garde",
            "techniques": "récolte manuelle ou mécanique, andains au champ",
        },
        {
            "token": "PAILLE_BLE_UZ", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Samarcande (oasis céréalière)", "lat": 39.65, "lon": 66.96,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé, chaumes et glumes",
            "production": "blé : 6 729 357 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × grain",
            "gisement": "paille ≈ 8,1 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6, 7], "fenetre_note": "moisson de juin à juillet, point sous garde",
            "techniques": "moisson motorisée, balles rondes, fourrage",
        },
    ],
},

# Pakistan — 3 intrants
"Pakistan": {
    "nom_fao": "Pakistan",
    "portrait": "Pendjab céréalier (blé 31,8 Mt, coton de Multan 3,5 Mt), canne du Sindh (Matiari, 84 Mt) — irrigation du bassin de l'Indus.",
    "reglementation": {
        "brulage": ("le brûlage des résidus de canne et de coton est courant, encadrement provincial à sourcer", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("la paille de blé sert de fourrage dominant, la balle de riz alimente les briqueteries", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("les sucreries valorisent déjà la bagasse en chaudière, marché concurrentiel", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte est semi-mécanisée, le coût du transport domine", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("récolte de la canne manuelle, saisonnalité forte du salariat", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "TIGE_COTON_PK", "famille": "Céréales", "nom_fr": "Tiges de coton",
            "region": "Multan (ceinture cotonnière du Pendjab)", "lat": 30.20, "lon": 71.47,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges et racines de cotonnier arrachées après récolte",
            "production": "coton brut : 3 500 618 t (2024, FAOSTAT)", "ratio": "tiges ≈ 3 × coton brut non égrené",
            "gisement": "tiges de coton ≈ 10,5 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [11, 12, 1], "fenetre_note": "récolte d'octobre à février, point sous garde",
            "techniques": "arrachage post-récolte, andains au champ",
        },
        {
            "token": "BAGASSE_CANNE_PK", "famille": "Tropical", "nom_fr": "Bagasse de canne",
            "region": "Matiari (bassin sucrier du Sindh)", "lat": 25.60, "lon": 68.45,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "bagasse de canne à sucre, coproduit du broyage",
            "production": "canne à sucre : 84 235 451 t (2024, FAOSTAT)", "ratio": "bagasse ≈ 0,30 × canne",
            "gisement": "bagasse ≈ 25,3 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [11, 12, 1, 2, 3], "fenetre_note": "campagne sucrière de novembre à mars, point sous garde",
            "techniques": "récolte manuelle, broyage en sucrerie",
        },
        {
            "token": "PAILLE_BLE_PK", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Sahiwal (bassin céréalier du Pendjab)", "lat": 30.67, "lon": 73.11,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé, chaumes et glumes",
            "production": "blé : 31 814 444 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × grain",
            "gisement": "paille ≈ 38,2 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [4, 5], "fenetre_note": "moisson d'avril à mai, point sous garde",
            "techniques": "moisson motorisée, pressage en balles rondes, andainage",
        },
    ],
},

# Russie — 5 intrants
"Russie": {
    "nom_fao": "Russian Federation",
    "portrait": "Kouban et Volga : blé (82,6 Mt, Krasnodar, Saratov), orge (16,7 Mt), avoine de l'Oural (Kurgan), tournesol de Volgograd (17,2 Mt), maïs du Kouban — la steppe au sud du 50e parallèle.",
    "reglementation": {
        "brulage": ("le brûlage des chaumes et des tiges de tournesol est restreint par décret régional, application variable à sourcer", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("la paille reste majoritairement au sol en grandes cultures extensives", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("la paille alimente quelques usines de pellet, filière marginale identifiée", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte est mécanisée, les distances de ramassage sont le coût dominant", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("fermes de très grande taille, mécanisation totale", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "PAILLE_BLE_RU", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Krasnodar (Kouban)", "lat": 45.04, "lon": 38.98,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé, chaumes et glumes",
            "production": "blé : 82 588 000 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × grain",
            "gisement": "paille ≈ 99,1 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [7, 8], "fenetre_note": "moisson de juillet à août, point sous garde",
            "techniques": "moisson motorisée, balles rondes, export de paille possible",
        },
        {
            "token": "PAILLE_ORGE_RU", "famille": "Céréales", "nom_fr": "Paille d'orge",
            "region": "Saratov (bassin de la Volga)", "lat": 51.57, "lon": 46.03,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille d'orge, chaumes et barbes",
            "production": "orge : 16 667 000 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 16,7 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [7, 8], "fenetre_note": "moisson de juillet à août, point sous garde",
            "techniques": "moisson motorisée, paille laissée au sol en sec",
        },
        {
            "token": "PAILLE_AVOINE_RU", "famille": "Céréales", "nom_fr": "Paille d'avoine",
            "region": "Chelyabinsk (Oural)", "lat": 55.16, "lon": 61.40,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille d'avoine, chaumes et panicules",
            "production": "avoine : 3 000 000 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 3 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [8, 9], "fenetre_note": "moisson d'août à septembre, point sous garde",
            "techniques": "moisson motorisée, fourrage d'hiver ou paillage",
        },
        {
            "token": "TIGE_TOURNESOL_RU", "famille": "Céréales", "nom_fr": "Tiges de tournesol",
            "region": "Volgograd (bassin tournesolier)", "lat": 48.71, "lon": 44.51,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges et calathides de tournesol",
            "production": "tournesol : 17 200 000 t (2024, FAOSTAT)", "ratio": "tiges ≈ 2 × graines",
            "gisement": "tiges de tournesol ≈ 34,4 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10], "fenetre_note": "récolte de septembre à octobre, point sous garde",
            "techniques": "moisson motorisée, broyage des tiges",
        },
        {
            "token": "PAILLE_MAIS_RU", "famille": "Céréales", "nom_fr": "Résidus de maïs",
            "region": "Tikhoretsk (Kouban, maïs du Sud)", "lat": 45.61, "lon": 40.13,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges, spathes et rafles de maïs",
            "production": "maïs : 13 954 000 t (2024, FAOSTAT)", "ratio": "résidus ≈ 0,25 × grain",
            "gisement": "résidus de maïs ≈ 3,5 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10, 11], "fenetre_note": "récolte de septembre à novembre, point sous garde",
            "techniques": "récolte des grains, ensilage ou broyage des tiges",
        },
    ],
},

# Sri Lanka — 2 intrants
"Sri Lanka": {
    "nom_fao": "Sri Lanka",
    "portrait": "thé des hauts plateaux (Kandy, surface 268 829 ha), riz de Polonnaruwa — plantation et riziculture tropicales.",
    "reglementation": {
        "brulage": ("le brûlage est restreint par la réglementation environnementale, pratiques résiduelles documentées", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("les tailles de théier sont épandues en inter-rangs, la paille de riz sert de paillage", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("les usines de thé sèchent déjà une part des résidus (bois de taille), marché local", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte est manuelle sur les plantations, mécanisée en riziculture", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("cueillette manuelle du thé, main-d'œuvre de plantation structurée", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "RESIDU_THE_LK", "famille": "Tropical", "nom_fr": "Résidus de théier",
            "region": "Kandy (hauts plateaux théicoles)", "lat": 7.29, "lon": 80.64,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidus de taille et de cueillette du théier",
            "production": "thé (feuilles) : 1 514 024 t — surface 268 829 ha (2024, FAOSTAT), l'ancrage résidus de théier est un ratio par hectare", "ratio": "résidus ≈ 0,6 t/ha/an (tailles)",
            "gisement": "résidus de théier ≈ 161 000 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "fenetre_note": "cueillette toute l'année (quatre saisons de thé), point tropical exempté",
            "techniques": "cueillette manuelle, tailles de formation et de régénération",
        },
        {
            "token": "BALLE_RIZ_LK", "famille": "Céréales", "nom_fr": "Balle de riz",
            "region": "Polonnaruwa (rizière du Mahaweli)", "lat": 7.93, "lon": 81.02,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "balle de riz (coque), coproduit du décorticage",
            "production": "riz paddy : 4 698 453 t (2024, FAOSTAT)", "ratio": "balle ≈ 0,20 × riz paddy",
            "gisement": "balle ≈ 939 691 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [3, 4, 8, 9], "fenetre_note": "double campagne de riz (yala et maha), point tropical exempté",
            "techniques": "moisson motorisée, décorticage en rizerie",
        },
    ],
},

# Syrie — 2 intrants
"Syrie": {
    "nom_fao": "Syrian Arab Republic",
    "portrait": "blé et orge du Croissant fertile (Djéziré de Hasakah, Alep 1,6 Mt d'orge) — pluvial et irrigué du Nord-Est.",
    "reglementation": {
        "brulage": ("le brûlage des chaumes est pratiqué, encadrement à sourcer", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("la paille sert de fourrage dominant, le pâturage des chaumes est courant", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("aucune filière de valorisation structurée identifiée à ce jour", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte est semi-mécanisée, la sécheresse structure les coûts", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("grandes fermes mécanisées dans la Djéziré, petites structures ailleurs", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "PAILLE_BLE_SY", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Hasakah (Djéziré, blé du Nord-Est)", "lat": 36.51, "lon": 40.75,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé, chaumes et glumes",
            "production": "blé : 2 431 225 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × grain",
            "gisement": "paille ≈ 2,9 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [5, 6], "fenetre_note": "moisson de mai à juin, point sous garde",
            "techniques": "moisson motorisée, balles rondes, fourrage dominant",
        },
        {
            "token": "PAILLE_ORGE_SY", "famille": "Céréales", "nom_fr": "Paille d'orge",
            "region": "Alep (bassin orge de l'Ouest)", "lat": 36.20, "lon": 37.16,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille d'orge, chaumes et barbes",
            "production": "orge : 1 572 020 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 1,6 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [4, 5], "fenetre_note": "moisson d'avril à mai, point sous garde",
            "techniques": "moisson motorisée, pâturage des chaumes courant",
        },
    ],
},

# Tadjikistan — 2 intrants
"Tadjikistan": {
    "nom_fao": "Tajikistan",
    "portrait": "coton de la vallée de Sughd (Panjakent, 253 kt), blé des vallées (Hissor) — agriculture de montagne irriguée.",
    "reglementation": {
        "brulage": ("le brûlage des tiges de coton est restreint, application à sourcer", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("les tiges de coton sont retournées au sol ou servent de combustible domestique", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("aucune filière de valorisation structurée identifiée à ce jour", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte est manuelle, le combustible d'hiver valorise les tiges", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("récolte du coton en partie manuelle, ouvrages collectifs de campagne", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "TIGE_COTON_TJ", "famille": "Céréales", "nom_fr": "Tiges de coton",
            "region": "Panjakent (vallée de Sughd)", "lat": 39.51, "lon": 67.32,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges et racines de cotonnier arrachées après récolte",
            "production": "coton brut : 253 182 t (2024, FAOSTAT)", "ratio": "tiges ≈ 3 × coton brut non égrené",
            "gisement": "tiges de coton ≈ 759 546 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11], "fenetre_note": "récolte d'octobre à novembre, point sous garde",
            "techniques": "récolte manuelle, andains au champ",
        },
        {
            "token": "PAILLE_BLE_TJ", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Hisor (vallée de Douchanbé)", "lat": 38.53, "lon": 68.79,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé, chaumes et glumes",
            "production": "blé : 880 734 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × grain",
            "gisement": "paille ≈ 1,1 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6, 7], "fenetre_note": "moisson de juin à juillet, point sous garde",
            "techniques": "moisson motorisée, balles rondes, fourrage",
        },
    ],
},

# Thaïlande — 4 intrants
"Thaïlande": {
    "nom_fao": "Thailand",
    "portrait": "riz de la Chao Phraya (Chainat, 33,6 Mt), manioc de l'Isan (Khorat, 28,6 Mt), canne du Khon Kaen (82,4 Mt), palmier du Sud (Krabi) — grenier tropical exportateur.",
    "reglementation": {
        "brulage": ("le brûlage des résidus de canne avant récolte est interdit mais documenté, contrôles en renforcement à sourcer", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("la paille de riz est en partie broyée et incorporée, le feu persiste en zones d'élevage", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("les sucreries valorisent la bagasse en chaudière, la balle de riz alimente des centrales et des fermes avicoles", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte est semi-mécanisée, le coût de la coupe manuelle de canne domine", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("coupe de canne manuelle salariée, riziculture mécanisée en plaine", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "BALLE_RIZ_TH", "famille": "Céréales", "nom_fr": "Balle de riz",
            "region": "Chainat (bassin de la Chao Phraya)", "lat": 15.20, "lon": 100.10,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "balle de riz (coque), coproduit du décorticage",
            "production": "riz paddy : 33 551 337 t (2024, FAOSTAT)", "ratio": "balle ≈ 0,20 × riz paddy",
            "gisement": "balle ≈ 6,7 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [11, 12, 1, 2, 3, 4], "fenetre_note": "grande récolte de novembre à avril, point tropical exempté",
            "techniques": "moisson motorisée, usinage, décorticage en rizerie",
        },
        {
            "token": "ECORCE_MANIOC_TH", "famille": "Tropical", "nom_fr": "Écorces de manioc",
            "region": "Nakhon Ratchasima (bassin manioc de l'Isan)", "lat": 14.97, "lon": 102.10,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "écorces et épluchures de manioc",
            "production": "manioc : 28 624 312 t (2024, FAOSTAT)", "ratio": "écorces ≈ 0,15 × racines",
            "gisement": "écorces ≈ 4,3 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "fenetre_note": "récolte continue, point tropical exempté",
            "techniques": "récolte manuelle, épluchage en amidonnerie",
        },
        {
            "token": "BAGASSE_CANNE_TH", "famille": "Tropical", "nom_fr": "Bagasse de canne",
            "region": "Khon Kaen (bassin sucrier du Nord-Est)", "lat": 16.43, "lon": 102.83,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "bagasse de canne à sucre, coproduit du broyage",
            "production": "canne à sucre : 82 435 400 t (2024, FAOSTAT)", "ratio": "bagasse ≈ 0,30 × canne",
            "gisement": "bagasse ≈ 24,7 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [11, 12, 1, 2, 3], "fenetre_note": "campagne de broyage de novembre à mars, point tropical exempté",
            "techniques": "coupe manuelle ou mécanique, broyage en sucrerie",
        },
        {
            "token": "EFB_PALMIER_TH", "famille": "Tropical", "nom_fr": "Rafles de palmier à huile",
            "region": "Krabi (bassin palmier du Sud)", "lat": 8.11, "lon": 98.90,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "rafles de régimes de palmier à huile",
            "production": "régimes de palmier : 18 606 769 t (2024, FAOSTAT)", "ratio": "rafles ≈ 0,22 × régimes",
            "gisement": "rafles ≈ 4,1 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "fenetre_note": "régimes toute l'année, point tropical exempté",
            "techniques": "récolte des régimes, stérilisation et pressage en huilerie",
        },
    ],
},

# Turkménistan — 2 intrants
"Turkménistan": {
    "nom_fao": "Turkmenistan",
    "portrait": "coton de Mary (600 kt) et blé de Dachogouz (1,3 Mt) — oasis irriguées du Karakoum, ordonnancement étatique.",
    "reglementation": {
        "brulage": ("le brûlage des tiges de coton est restreint par ordonnance, application à sourcer", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("les tiges sont retournées au sol sur directive des exploitations d'État", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("aucune filière de valorisation structurée identifiée à ce jour", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte est organisée par les exploitations d'État", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("récolte du coton en partie manuelle, campagnes organisées", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "TIGE_COTON_TM", "famille": "Céréales", "nom_fr": "Tiges de coton",
            "region": "Mary (oasis cotonnière du Karakoum)", "lat": 37.61, "lon": 61.83,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges et racines de cotonnier arrachées après récolte",
            "production": "coton brut : 600 238 t (2024, FAOSTAT)", "ratio": "tiges ≈ 3 × coton brut non égrené",
            "gisement": "tiges de coton ≈ 1,8 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11], "fenetre_note": "récolte d'octobre à novembre, point sous garde",
            "techniques": "récolte manuelle ou mécanique, andains au champ",
        },
        {
            "token": "PAILLE_BLE_TM", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Dashoguz (oasis céréalière du Nord)", "lat": 41.43, "lon": 59.91,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé, chaumes et glumes",
            "production": "blé : 1 330 000 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × grain",
            "gisement": "paille ≈ 1,6 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6, 7], "fenetre_note": "moisson de juin à juillet, point sous garde",
            "techniques": "moisson motorisée, balles rondes, fourrage",
        },
    ],
},

# Turquie — 8 intrants
"Turquie": {
    "nom_fao": "Türkiye",
    "portrait": "blé de Konya (20,8 Mt), orge d'Ankara (8,1 Mt), maïs de Çukurova (8,1 Mt), coton de Şanlıurfa (2,2 Mt), tournesol de Thrace (Edirne), thé de Rize (1,4 Mt) — agricultures méditerranéennes et anatoliennes.",
    "reglementation": {
        "brulage": ("le brûlage des résidus est restreint par la réglementation turque sur l'environnement, pratiques variables selon les provinces", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "enfouissement": ("la paille sert de fourrage et de litière, l'incorporation au sol progresse", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "traitement": ("la paille alimente des unités de cogénération documentées, la balle de riz des rizeries de Thrace", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "cout_agriculture": ("la collecte est mécanisée et contractuelle dans les grands bassins", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
        "main_oeuvre": ("mécanisation céréalière avancée, cueillette du thé manuelle", ETIQUETTE_A_VERIFIER, "à sourcer (v1.3)"),
    },
    "intrants": [
        {
            "token": "PAILLE_BLE_TR", "famille": "Céréales", "nom_fr": "Paille de blé",
            "region": "Konya (steppe céréalière anatolienne)", "lat": 37.87, "lon": 32.49,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille de blé, chaumes et glumes",
            "production": "blé : 20 800 000 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,2 × grain",
            "gisement": "paille ≈ 25 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6, 7], "fenetre_note": "moisson de juin à juillet, point sous garde",
            "techniques": "moisson motorisée, pressage en balles rondes, andainage",
        },
        {
            "token": "PAILLE_ORGE_TR", "famille": "Céréales", "nom_fr": "Paille d'orge",
            "region": "Ankara (bassin orge d anatolien)", "lat": 39.93, "lon": 32.86,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille d'orge, chaumes et barbes",
            "production": "orge : 8 100 000 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 8,1 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6, 7], "fenetre_note": "moisson de juin à juillet, point sous garde",
            "techniques": "moisson motorisée, balles rondes, fourrage",
        },
        {
            "token": "PAILLE_AVOINE_TR", "famille": "Céréales", "nom_fr": "Paille d'avoine",
            "region": "Çorum (Haute Anatolie)", "lat": 40.65, "lon": 34.95,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "paille d'avoine, chaumes et panicules",
            "production": "avoine : 390 000 t (2024, FAOSTAT)", "ratio": "paille ≈ 1,0 × grain",
            "gisement": "paille ≈ 390 000 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [7, 8], "fenetre_note": "moisson de juillet à août, point sous garde",
            "techniques": "moisson motorisée, balles rondes, fourrage",
        },
        {
            "token": "PAILLE_MAIS_TR", "famille": "Céréales", "nom_fr": "Résidus de maïs",
            "region": "Adana (Çukurova, delta du Seyhan)", "lat": 37.00, "lon": 35.32,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges, spathes et rafles de maïs",
            "production": "maïs : 8 100 000 t (2024, FAOSTAT)", "ratio": "résidus ≈ 0,25 × grain",
            "gisement": "résidus de maïs ≈ 2 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10, 11], "fenetre_note": "récolte de septembre à novembre, point sous garde",
            "techniques": "récolte des grains, ensilage des tiges ou broyage au champ",
        },
        {
            "token": "BALLE_RIZ_TR", "famille": "Céréales", "nom_fr": "Balle de riz",
            "region": "Edirne (Thrace rizicole)", "lat": 41.68, "lon": 26.56,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "balle de riz (coque), coproduit du décorticage",
            "production": "riz paddy : 1 019 000 t (2024, FAOSTAT)", "ratio": "balle ≈ 0,20 × riz paddy",
            "gisement": "balle ≈ 203 800 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10], "fenetre_note": "moisson de septembre à octobre, point sous garde",
            "techniques": "moisson motorisée, décorticage en rizerie de Thrace",
        },
        {
            "token": "TIGE_COTON_TR", "famille": "Céréales", "nom_fr": "Tiges de coton",
            "region": "Şanlıurfa (bassin cotonnier du Sud-Est)", "lat": 37.16, "lon": 38.92,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges et racines de cotonnier arrachées après récolte",
            "production": "coton brut : 2 243 000 t (2024, FAOSTAT)", "ratio": "tiges ≈ 3 × coton brut non égrené",
            "gisement": "tiges de coton ≈ 6,7 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [10, 11, 12], "fenetre_note": "récolte d'octobre à décembre, point sous garde",
            "techniques": "récolte mécanique, arrachage des tiges post-récolte",
        },
        {
            "token": "TIGE_TOURNESOL_TR", "famille": "Céréales", "nom_fr": "Tiges de tournesol",
            "region": "Edirne (tournesol de Thrace)", "lat": 41.72, "lon": 26.61,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "tiges et calathides de tournesol",
            "production": "tournesol : 2 195 000 t (2024, FAOSTAT)", "ratio": "tiges ≈ 2 × graines",
            "gisement": "tiges de tournesol ≈ 4,4 Mt/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10], "fenetre_note": "récolte de septembre à octobre, point sous garde",
            "techniques": "moisson motorisée, broyage des tiges",
        },
        {
            "token": "RESIDU_THE_TR", "famille": "Tropical", "nom_fr": "Résidus de théier",
            "region": "Rize (côte de la mer Noire théicole)", "lat": 41.02, "lon": 40.52,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidus de taille et de cueillette du théier",
            "production": "thé (feuilles) : 1 414 000 t — surface 81 010 ha (2024, FAOSTAT), l'ancrage résidus de théier est un ratio par hectare", "ratio": "résidus ≈ 0,6 t/ha/an (tailles)",
            "gisement": "résidus de théier ≈ 49 000 t/an", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [5, 6, 7, 8, 9, 10], "fenetre_note": "cueillette et tailles de mai à octobre, point sous garde",
            "techniques": "cueillette manuelle, tailles de formation, séchage en usine",
        },
    ],
},

}

POSTES_REGLEMENTATION = _master.CLEFS_REGLEMENTATION



# ---------------------------------------------------------------------------
# Index et contrôles de structure
# ---------------------------------------------------------------------------

def _index():
    idx = {}
    for pays, fiche in PAYS_ASIE.items():
        for intrant in fiche["intrants"]:
            idx[intrant["token"]] = (pays, intrant)
    return idx


INDEX = _index()


def _verifier_structure(problemes):
    idx = {}
    for pays, fiche in PAYS_ASIE.items():
        for cle in ("nom_fao", "portrait", "reglementation", "intrants"):
            if cle not in fiche:
                problemes.append("pays %s : champ manquant %s" % (pays, cle))
        if len(fiche.get("intrants", [])) < 2:
            problemes.append("pays %s : moins de 2 intrants" % pays)
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
    """Contrôles complets : structure, alignement master et atlas, saisons, boîtes."""
    problemes = []
    idx = _verifier_structure(problemes)

    familles_master = {f["famille"] for f in _master.ATLAS_BIOMASSES_MONDE.values()}
    tokens_master = set(_master.ATLAS_BIOMASSES_MONDE)
    tokens_v11 = set(_pays_v11.INDEX)
    tokens_v12 = set(_vignobles_v12.INDEX)

    tropicaux = 0
    sous_garde = 0
    for tok, (pays, intrant) in sorted(idx.items()):
        if intrant["famille"] not in familles_master:
            problemes.append("%s : famille hors master %s" % (tok, intrant["famille"]))
        if tok in tokens_master:
            problemes.append("token en collision avec le master : %s" % tok)
        if tok in tokens_v11:
            problemes.append("token en collision avec l'atlas v1.1 : %s" % tok)
        if tok in tokens_v12:
            problemes.append("token en collision avec l'atlas v1.2 : %s" % tok)
        prefixe = tok[:tok.rindex("_")]
        if abs(intrant["lat"]) <= CEINTURE_TROPICALE:
            tropicaux += 1
        else:
            sous_garde += 1
            if prefixe not in REGLES_SAISON:
                problemes.append("%s : préfixe sans règle saisonnière %s" % (tok, prefixe))
            else:
                hors = [m for m in intrant["fenetre"] if m not in REGLES_SAISON[prefixe]]
                if hors:
                    problemes.append("%s : fenêtre hors règle %s : %s" % (tok, prefixe, hors))
        boite = BBOX_ASIE.get(pays)
        if boite is None:
            problemes.append("%s : pays sans boîte englobante %s" % (tok, pays))
        elif not (boite[0] <= intrant["lat"] <= boite[1]
                  and boite[2] <= intrant["lon"] <= boite[3]):
            problemes.append("%s : GPS hors boîte %s (%s, %s)"
                             % (tok, pays, intrant["lat"], intrant["lon"]))
    if tropicaux + sous_garde != len(idx):
        problemes.append("comptage saisonnier incohérent")
    return problemes


# ---------------------------------------------------------------------------
# Sommaire et fiches
# ---------------------------------------------------------------------------

def sommaire():
    lignes = ["Atlas des biomasses d'Asie — World Twin v1.3",
              " Productions FAOSTAT 2024 SOURCÉES, ratios résidus ILLUSTRATION,",
              " points GPS approximations de région, doctrine PI (aucun paramètre VDE).", ""]
    total = 0
    for pays in sorted(PAYS_ASIE, key=lambda p: p.lower()):
        fiche = PAYS_ASIE[pays]
        lignes.append("%s (%s) — %d intrants" % (pays, fiche["nom_fao"], len(fiche["intrants"])))
        for intrant in fiche["intrants"]:
            lignes.append("  %-18s %-16s %-30s %s" % (
                intrant["token"], intrant["famille"], intrant["nom_fr"],
                " / ".join(MOIS_COURTS[m] for m in intrant["fenetre"])))
        total += len(fiche["intrants"])
        lignes.append("")
    lignes.insert(3, " Pays : %d — intrants : %d" % (len(PAYS_ASIE), total))
    return "\n".join(lignes)


def fiche_token(token):
    if token not in INDEX:
        return None
    pays, intrant = INDEX[token]
    fiche_pays = PAYS_ASIE[pays]
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
    prefixe = token[:token.rindex("_")]
    if abs(intrant["lat"]) <= CEINTURE_TROPICALE:
        garde = "point tropical exempté (production continue)"
    elif prefixe in REGLES_SAISON:
        garde = "point sous garde, mois autorisés : %s" % " ".join(
            str(m) for m in REGLES_SAISON[prefixe])
    else:
        garde = "préfixe sans règle"
    lignes.append("Fenêtre saisonnière : %s — %s (%s)" % (
        ", ".join(MOIS_COURTS[m] for m in intrant["fenetre"]), intrant["fenetre_note"], garde))
    lignes.append("Techniques : %s" % intrant["techniques"])
    lignes.append("")
    lignes.append("Réglementation %s (synthèse pays, À VÉRIFIER) :" % pays)
    for cle in _master.CLEFS_REGLEMENTATION:
        texte, etiquette, ref = fiche_pays["reglementation"][cle]
        lignes.append("  %s [%s] : %s (réf. %s)" % (cle, etiquette, texte, ref))
    return "\n".join(lignes)


def fiche_pays(nom):
    cible = None
    for pays in PAYS_ASIE:
        if nom.lower() in (pays.lower(), PAYS_ASIE[pays]["nom_fao"].lower()) or nom.lower() == pays.lower():
            cible = pays
            break
    if cible is None:
        return None
    fiche = PAYS_ASIE[cible]
    lignes = ["%s (%s) — atlas des biomasses d'Asie" % (cible, fiche["nom_fao"]), ""]
    lignes.append("Portrait : %s" % fiche["portrait"])
    lignes.append("")
    lignes.append("Réglementation (synthèse à cinq postes, À VÉRIFIER) :")
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
    lignes = ["Croisement v1.3 — contrôles complets", ""]
    lignes.append("Pays couverts : %d" % len(PAYS_ASIE))
    lignes.append("Intrants pays : %d (master v1.0 : %d, atlas v1.1 : %d, vignobles v1.2 : %d)"
                  % (len(INDEX), len(_master.ATLAS_BIOMASSES_MONDE), len(_pays_v11.INDEX),
                     len(_vignobles_v12.INDEX)))
    familles_pays = {i["famille"] for (_, i) in INDEX.values()}
    familles_master = {f["famille"] for f in _master.ATLAS_BIOMASSES_MONDE.values()}
    lignes.append("Familles pays ⊆ familles master : %s"
                  % ("OK" if familles_pays <= familles_master else "ECART"))
    lignes.append("Familles représentées : %s" % ", ".join(sorted(familles_pays)))
    collisions_m = set(INDEX) & set(_master.ATLAS_BIOMASSES_MONDE)
    collisions_11 = set(INDEX) & set(_pays_v11.INDEX)
    collisions_12 = set(INDEX) & set(_vignobles_v12.INDEX)
    lignes.append("Collision de tokens avec le master v1.0 : %s"
                  % ("AUCUNE" if not collisions_m else ", ".join(sorted(collisions_m))))
    lignes.append("Collision de tokens avec l'atlas v1.1 : %s"
                  % ("AUCUNE" if not collisions_11 else ", ".join(sorted(collisions_11))))
    lignes.append("Collision de tokens avec l'atlas v1.2 : %s"
                  % ("AUCUNE" if not collisions_12 else ", ".join(sorted(collisions_12))))
    tropicaux = [t for t, (_, i) in INDEX.items() if abs(i["lat"]) <= CEINTURE_TROPICALE]
    sous_garde = [t for t, (_, i) in INDEX.items() if abs(i["lat"]) > CEINTURE_TROPICALE]
    lignes.append("Garde saisonnière : %d points sous garde, %d points tropicaux exemptés"
                  % (len(sous_garde), len(tropicaux)))
    lignes.append("Boîtes englobantes : %d pays, %d points contrôlés" % (len(BBOX_ASIE), len(INDEX)))
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


# ---------------------------------------------------------------------------
# Météo temps réel (Open-Meteo, cache jamais versionné)
# ---------------------------------------------------------------------------

VARIABLES_METEO = ("temperature_2m", "relative_humidity_2m", "precipitation",
                   "wind_speed_10m")
TTL_POINTAGE_S = 3600


def _chemin_cache_meteo_temps_reel():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "cache-meteo-temps-reel")


def _pointage_en_cache(tokens):
    """Retourne un pointage horodaté s'il existe et est frais, sinon None."""
    dossier = _chemin_cache_meteo_temps_reel()
    if not os.path.isdir(dossier):
        return None
    attendus = set(tokens)
    for nom in sorted(os.listdir(dossier), reverse=True):
        if not nom.startswith("pointage-") or not nom.endswith(".json"):
            continue
        chemin = os.path.join(dossier, nom)
        try:
            age = max(0, int(__import__("time").time() - os.path.getmtime(chemin)))
        except OSError:
            continue
        if age > TTL_POINTAGE_S:
            continue
        try:
            with open(chemin, "r", encoding="utf-8") as fh:
                contenu = json.load(fh)
        except (OSError, ValueError):
            continue
        if attendus.issubset(set(contenu.get("points", {}))):
            return contenu
    return None


def pointage_meteo(tokens=None):
    """Pointage météo temps réel Open-Meteo pour un ou tous les intrants.

    Un seul appel API pour tous les points (listes lat/lon en virgule),
    mise en cache horaire dans cache-meteo-temps-reel/ (jamais versionné).
    """
    if tokens is None:
        tokens = list(INDEX)
    for token in tokens:
        if token not in INDEX:
            raise SystemExit("Intrant inconnu : %s. Intrants : %s"
                             % (token, ", ".join(sorted(INDEX))))
    cache = _pointage_en_cache(tokens)
    if cache is not None:
        return cache
    latitudes = ",".join("%.4f" % INDEX[t][1]["lat"] for t in tokens)
    longitudes = ",".join("%.4f" % INDEX[t][1]["lon"] for t in tokens)
    url = ("https://api.open-meteo.com/v1/forecast"
           "?latitude=%s&longitude=%s&current=%s&timezone=UTC"
           % (latitudes, longitudes, ",".join(VARIABLES_METEO)))
    try:
        with urllib.request.urlopen(url, timeout=30) as reponse:
            brut = json.loads(reponse.read().decode("utf-8"))
    except (OSError, ValueError) as erreur:
        raise SystemExit("Pointage météo indisponible (réseau : %s). "
                         "Le module reste utilisable hors ligne." % erreur)
    points = {}
    for index, token in enumerate(tokens):
        if isinstance(brut, list):
            courant = brut[index].get("current", {})
        else:
            courant = brut.get("current", {})
        points[token] = {clef: courant.get(clef) for clef in VARIABLES_METEO}
        points[token]["heure_utc"] = courant.get("time")
    contenu = {"etiquette": "POINTAGE TEMPS RÉEL (Open-Meteo current, non versionné)",
               "source": "api.open-meteo.com, gratuite sans clé",
               "points": points}
    dossier = _chemin_cache_meteo_temps_reel()
    try:
        os.makedirs(dossier, exist_ok=True)
        horodatage = __import__("time").strftime("%Y%m%dT%H", __import__("time").gmtime())
        with open(os.path.join(dossier, "pointage-%s.json" % horodatage),
                  "w", encoding="utf-8") as fh:
            json.dump(contenu, fh, ensure_ascii=False, indent=1, sort_keys=True)
    except OSError:
        pass  # cache best effort : le pointage reste affiché
    return contenu


def rendre_pointage(contenu):
    lignes = ["Pointage météo temps réel — %d point(s) (Open-Meteo, cache local d'une heure)"
              % len(contenu["points"]),
              "Étiquette : %s — jamais une donnée de qualification." % contenu["etiquette"],
              ""]
    lignes.append("%-20s %-30s %8s %8s %8s %8s" % ("intranT", "pays", "T°C", "HR%", "mm", "km/h"))
    for token in sorted(contenu["points"]):
        pays, f = INDEX[token]
        m = contenu["points"][token]
        lignes.append("%-20s %-30s %8s %8s %8s %8s" % (
            token, pays, m.get("temperature_2m"), m.get("relative_humidity_2m"),
            m.get("precipitation"), m.get("wind_speed_10m")))
    return "\n".join(lignes) + "\n"


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print(sommaire())
        return 0
    if args[0] == "croisement":
        texte, code = croisement()
        print(texte)
        return code
    if args[0] == "meteo":
        tokens = args[1:] or None
        contenu = pointage_meteo(tokens)
        print(rendre_pointage(contenu))
        return 0
    if args[0] == "pays" and len(args) >= 2:
        texte = fiche_pays(" ".join(args[1:]))
        if texte is None:
            print("Pays inconnu. Pays disponibles : %s" % ", ".join(sorted(PAYS_ASIE)))
            return 1
        print(texte)
        return 0
    texte = fiche_token(args[0])
    if texte is None:
        print("Jeton inconnu. Usage : sommaire | fiche TOKEN | pays NOM | croisement | meteo [TOKEN]")
        return 1
    print(texte)
    return 0


if __name__ == "__main__":
    sys.exit(main())

