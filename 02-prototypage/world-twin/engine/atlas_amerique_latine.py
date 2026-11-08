#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""World Twin v1.8 — Atlas des biomasses : Amérique latine et centrale restante.

Extension régionale de la lignée d'atlas (monde v1.0, pays v1.1, vignobles
v1.2, Asie v1.3) : pour les pays non encore couverts de cette région, les
biomasses LOCALES majeures sont placées sur le globe — région, point GPS
(Global Positioning System, approximation de bassin, jamais un cadastre),
type, volume, fenêtre saisonnière, techniques culturales — avec, par pays,
une synthèse réglementaire à cinq postes, tous À VÉRIFIER.

66 intrants, productions SOURCÉES (FAOSTAT QCL 2024 via Commodity
Origins CC BY 4.0, IndexMundi/USDA PS&D relevé 03/2026, tableaux Wikipédia,
Nordic Forest Statistics 2026, Luke, Statistique Canada) et ratios
résidus ILLUSTRATION selon la convention figée v1.3.

Les nouveaux jetons restent HORS de MAPPINGS (gisements_hubs.py) : repli
densité v1.6 à l'exécution, comme l'atlas Asie v1.3 — extension du snapshot
v18 inscrite en action P3.

Doctrine PI (propriété intellectuelle) : ce module n'embarque AUCUN des six
paramètres du VDE (Vignite Decision Engine) et aucune valeur calibrée.
Seules des données publiques sont versionnées. Étiquette SYNTHÉTIQUE au
registre de développement uniquement.

Bibliothèque standard uniquement, déterministe, aucune dépendance réseau.
Usage :
    python3 engine/atlas_amerique_latine.py                # sommaire par pays
    python3 engine/atlas_amerique_latine.py TOKEN          # fiche d'un intrant
    python3 engine/atlas_amerique_latine.py croisement     # contrôles complets
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import atlas_biomasses_monde as _master   # noqa: E402
import atlas_biomasses_pays as _p11        # noqa: E402
import atlas_vignobles_monde as _v12       # noqa: E402
import atlas_biomasses_asie as _v13        # noqa: E402

ETIQUETTE_A_VERIFIER = "À VÉRIFIER"
CEINTURE_TROPICALE = 23.5
PAYS_AMERIQUE_LATINE = {
    "Colombie": {
        "nom_fao": "Colombia",
        "portrait": "bassin vallée du Cauca et piémont des Llanos — profil agricole à compléter (v1.8)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ]
        },
        "intrants": [
            {
                "token": "PARCHE_CAFE_CO",
                "famille": "Tropical",
                "nom_fr": "Parche et pulpe de café",
                "region": "vallée du Cauca et piémont des Llanos",
                "lat": 4.0,
                "lon": -73.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "parche, pulpe et mucilage de cerises de café",
                "production": "café vert : 839 847 t (FAOSTAT QCL 2024)",
                "ratio": "parche et pulpe ≈ 0,45 × café vert (ILLUSTRATION)",
                "gisement": "≈ 377 931 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    10,
                    11,
                    12,
                    1,
                    2
                ],
                "fenetre_note": "récolte de octobre à février, point sous garde",
                "techniques": "dépulpage humide ou sec en station"
            },
            {
                "token": "BAGASSE_CANNE_CO",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "vallée du Cauca et piémont des Llanos",
                "lat": 4.0,
                "lon": -73.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "canne à sucre : 31 856 922 t (FAOSTAT QCL 2024)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 9,6 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de avril à novembre, point sous garde",
                "techniques": "coupe mécanique, pressage en sucrerie"
            },
            {
                "token": "RAFLES_PALMIER_CO",
                "famille": "Tropical",
                "nom_fr": "Rafles de palmier à huile",
                "region": "vallée du Cauca et piémont des Llanos",
                "lat": 4.0,
                "lon": -73.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "rafles vides et efflorescences du palmier à huile",
                "production": "régimes de palmier à huile : 7 824 756 t (FAOSTAT QCL 2024)",
                "ratio": "rafles ≈ 0,22 × régimes (ILLUSTRATION)",
                "gisement": "≈ 1,7 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12
                ],
                "fenetre_note": "récolte ou activité continue sur l'année, point sous garde",
                "techniques": "égrappage en huilerie, régimes toute l'année"
            },
            {
                "token": "RESIDUS_MAIS_CO",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "vallée du Cauca et piémont des Llanos",
                "lat": 4.0,
                "lon": -73.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 1 500 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 375 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte en ensilage ou grain, andains au champ"
            },
            {
                "token": "BALLE_RIZ_CO",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "vallée du Cauca et piémont des Llanos",
                "lat": 4.0,
                "lon": -73.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz paddy : 2 823 000 t (FAOSTAT QCL 2024)",
                "ratio": "balle ≈ 0,20 × riz paddy (ILLUSTRATION)",
                "gisement": "≈ 564 600 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "moisson, décorticage en rizerie"
            },
            {
                "token": "CABOSSE_CACAO_CO",
                "famille": "Coques & noyaux",
                "nom_fr": "Cabosse de cacao",
                "region": "vallée du Cauca et piémont des Llanos",
                "lat": 4.0,
                "lon": -73.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "cabosses fendues et mucilage de cacao",
                "production": "fèves de cacao sèches : 67 678 t (FAOSTAT QCL 2024)",
                "ratio": "cabosse ≈ 8 × fèves sèches (ILLUSTRATION)",
                "gisement": "≈ 541 424 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    10,
                    11,
                    12,
                    1,
                    2,
                    3
                ],
                "fenetre_note": "récolte de octobre à mars, point sous garde",
                "techniques": "cabossage manuel, fermentation des fèves"
            }
        ]
    },
    "Venezuela": {
        "nom_fao": "Venezuela, RB",
        "portrait": "bassin Llanos centraux et État de Portuguesa — profil agricole à compléter (v1.8)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ]
        },
        "intrants": [
            {
                "token": "BALLE_RIZ_VE",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "Llanos centraux et État de Portuguesa",
                "lat": 7.5,
                "lon": -66.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz paddy : 478 473 t (tableau Wikipédia (FAOSTAT, année de l'article))",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 95 695 t/an",
                "etiquette_gisement": "SOURCÉ (production tableau Wikipédia (FAOSTAT, année de l'article)) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "moisson, décorticage en rizerie"
            },
            {
                "token": "CABOSSE_CACAO_VE",
                "famille": "Coques & noyaux",
                "nom_fr": "Cabosse de cacao",
                "region": "Llanos centraux et État de Portuguesa",
                "lat": 7.5,
                "lon": -66.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "cabosses fendues et mucilage de cacao",
                "production": "fèves de cacao sèches : 29 383 t (FAOSTAT QCL 2024)",
                "ratio": "cabosse ≈ 8 × fèves sèches (ILLUSTRATION)",
                "gisement": "≈ 235 066 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    10,
                    11,
                    12,
                    1,
                    2,
                    3
                ],
                "fenetre_note": "récolte de octobre à mars, point sous garde",
                "techniques": "cabossage manuel, fermentation des fèves"
            }
        ]
    },
    "Bolivie": {
        "nom_fao": "Bolivia",
        "portrait": "bassin plaines de Santa Cruz et Beni — profil agricole à compléter (v1.8)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_SOJA_BO",
                "famille": "Céréales",
                "nom_fr": "Résidus de soja",
                "region": "plaines de Santa Cruz et Beni",
                "lat": -17.5,
                "lon": -64.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, gousses et pailles de soja",
                "production": "soja (graines) : 3 216 440 t (FAOSTAT QCL 2024)",
                "ratio": "résidus ≈ 2,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 8,0 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    3,
                    4,
                    5
                ],
                "fenetre_note": "récolte de mars à mai, point sous garde",
                "techniques": "récolte au moissonneur-batteur, andains"
            },
            {
                "token": "RESIDUS_MAIS_BO",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "plaines de Santa Cruz et Beni",
                "lat": -17.5,
                "lon": -64.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 1 100 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 275 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    2,
                    3,
                    4
                ],
                "fenetre_note": "récolte de février à avril, point sous garde",
                "techniques": "récolte en ensilage ou grain, andains au champ"
            },
            {
                "token": "PAILLE_SORGHO_BO",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "plaines de Santa Cruz et Beni",
                "lat": -17.5,
                "lon": -64.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 1 771 085 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 2,7 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    3,
                    4,
                    5
                ],
                "fenetre_note": "récolte de mars à mai, point sous garde",
                "techniques": "récolte manuelle ou mécanisée, fanage au champ"
            },
            {
                "token": "BAGASSE_CANNE_BO",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "plaines de Santa Cruz et Beni",
                "lat": -17.5,
                "lon": -64.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "canne à sucre : 11 447 542 t (FAOSTAT QCL 2024)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 3,4 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de avril à novembre, point sous garde",
                "techniques": "coupe mécanique, pressage en sucrerie"
            },
            {
                "token": "BALLE_RIZ_BO",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "plaines de Santa Cruz et Beni",
                "lat": -17.5,
                "lon": -64.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz blanchi : 405 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 117 450 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    3,
                    4,
                    5
                ],
                "fenetre_note": "récolte de mars à mai, point sous garde",
                "techniques": "moisson, décorticage en rizerie"
            }
        ]
    },
    "Paraguay": {
        "nom_fao": "Paraguay",
        "portrait": "bassin région orientale (Ciudad del Este) — profil agricole à compléter (v1.8)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_SOJA_PY",
                "famille": "Céréales",
                "nom_fr": "Résidus de soja",
                "region": "région orientale (Ciudad del Este)",
                "lat": -23.5,
                "lon": -58.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, gousses et pailles de soja",
                "production": "soja (graines) : 11 100 256 t (FAOSTAT QCL 2024)",
                "ratio": "résidus ≈ 2,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 27,8 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    3,
                    4,
                    5
                ],
                "fenetre_note": "récolte de mars à mai, point sous garde",
                "techniques": "récolte au moissonneur-batteur, andains"
            },
            {
                "token": "RESIDUS_MAIS_PY",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "région orientale (Ciudad del Este)",
                "lat": -23.5,
                "lon": -58.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 5 200 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 1,3 Mt/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    2,
                    3,
                    4
                ],
                "fenetre_note": "récolte de février à avril, point sous garde",
                "techniques": "récolte en ensilage ou grain, andains au champ"
            },
            {
                "token": "PAILLE_BLE_PY",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "région orientale (Ciudad del Este)",
                "lat": -23.5,
                "lon": -58.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 1 300 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 1,6 Mt/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    11,
                    12,
                    1
                ],
                "fenetre_note": "récolte de novembre à janvier, point sous garde",
                "techniques": "moisson motorisée, balles rondes, fourrage prioritaire"
            },
            {
                "token": "TIGE_TOURNESOL_PY",
                "famille": "Céréales",
                "nom_fr": "Tiges de tournesol",
                "region": "région orientale (Ciudad del Este)",
                "lat": -23.5,
                "lon": -58.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et capitules de tournesol",
                "production": "tournesol (graines) : 40 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "tiges ≈ 2 × graines (ILLUSTRATION)",
                "gisement": "≈ 80 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    2,
                    3,
                    4
                ],
                "fenetre_note": "récolte de février à avril, point sous garde",
                "techniques": "récolte des capitules, broyage des tiges"
            },
            {
                "token": "TIGE_COTON_PY",
                "famille": "Céréales",
                "nom_fr": "Tiges de coton",
                "region": "région orientale (Ciudad del Este)",
                "lat": -23.5,
                "lon": -58.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et racines de cotonnier arrachées après récolte",
                "production": "coton brut (fibres) : 54 431 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "tiges ≈ 3 × coton brut (ILLUSTRATION)",
                "gisement": "≈ 163 292 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    3,
                    4,
                    5,
                    6
                ],
                "fenetre_note": "récolte de mars à juin, point sous garde",
                "techniques": "récolte mécanique ou manuelle, arrachage des tiges"
            }
        ]
    },
    "Uruguay": {
        "nom_fao": "Uruguay",
        "portrait": "bassin littoral céréalier (Paysandú-Salto) — profil agricole à compléter (v1.8)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_SOJA_UY",
                "famille": "Céréales",
                "nom_fr": "Résidus de soja",
                "region": "littoral céréalier (Paysandú-Salto)",
                "lat": -32.8,
                "lon": -56.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, gousses et pailles de soja",
                "production": "soja (graines) : 3 065 000 t (FAOSTAT QCL 2024)",
                "ratio": "résidus ≈ 2,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 7,7 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    3,
                    4,
                    5
                ],
                "fenetre_note": "récolte de mars à mai, point sous garde",
                "techniques": "récolte au moissonneur-batteur, andains"
            },
            {
                "token": "PAILLE_BLE_UY",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "littoral céréalier (Paysandú-Salto)",
                "lat": -32.8,
                "lon": -56.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 1 300 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 1,6 Mt/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    11,
                    12,
                    1
                ],
                "fenetre_note": "récolte de novembre à janvier, point sous garde",
                "techniques": "moisson motorisée, balles rondes, fourrage prioritaire"
            },
            {
                "token": "RESIDUS_MAIS_UY",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "littoral céréalier (Paysandú-Salto)",
                "lat": -32.8,
                "lon": -56.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 1 000 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 250 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    2,
                    3,
                    4
                ],
                "fenetre_note": "récolte de février à avril, point sous garde",
                "techniques": "récolte en ensilage ou grain, andains au champ"
            },
            {
                "token": "TIGE_TOURNESOL_UY",
                "famille": "Céréales",
                "nom_fr": "Tiges de tournesol",
                "region": "littoral céréalier (Paysandú-Salto)",
                "lat": -32.8,
                "lon": -56.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et capitules de tournesol",
                "production": "tournesol (graines) : 10 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "tiges ≈ 2 × graines (ILLUSTRATION)",
                "gisement": "≈ 20 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    2,
                    3,
                    4
                ],
                "fenetre_note": "récolte de février à avril, point sous garde",
                "techniques": "récolte des capitules, broyage des tiges"
            },
            {
                "token": "BALLE_RIZ_UY",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "littoral céréalier (Paysandú-Salto)",
                "lat": -32.8,
                "lon": -56.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz blanchi : 1 050 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 304 500 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    3,
                    4,
                    5
                ],
                "fenetre_note": "récolte de mars à mai, point sous garde",
                "techniques": "moisson, décorticage en rizerie"
            }
        ]
    },
    "Guyana": {
        "nom_fao": "Guyana",
        "portrait": "bassin côte de Demerara — profil agricole à compléter (v1.8)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ]
        },
        "intrants": [
            {
                "token": "BAGASSE_CANNE_GY",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "côte de Demerara",
                "lat": 5.0,
                "lon": -58.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "sucre de canne centrifuge : 65 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 19 500 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de avril à novembre, point sous garde",
                "techniques": "coupe mécanique, pressage en sucrerie"
            },
            {
                "token": "BALLE_RIZ_GY",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "côte de Demerara",
                "lat": 5.0,
                "lon": -58.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz blanchi : 720 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 208 800 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "moisson, décorticage en rizerie"
            }
        ]
    },
    "Suriname": {
        "nom_fao": "Suriname",
        "portrait": "bassin district de Commewijne — profil agricole à compléter (v1.8)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ]
        },
        "intrants": [
            {
                "token": "BALLE_RIZ_SR",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "district de Commewijne",
                "lat": 4.5,
                "lon": -55.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz blanchi : 170 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 49 300 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "moisson, décorticage en rizerie"
            }
        ]
    },
    "Panama": {
        "nom_fao": "Panama",
        "portrait": "bassin provinces de Chiriquí et Veraguas — profil agricole à compléter (v1.8)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ]
        },
        "intrants": [
            {
                "token": "BAGASSE_CANNE_PA",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "provinces de Chiriquí et Veraguas",
                "lat": 8.5,
                "lon": -80.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "sucre de canne centrifuge : 160 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 48 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de avril à novembre, point sous garde",
                "techniques": "coupe mécanique, pressage en sucrerie"
            },
            {
                "token": "BALLE_RIZ_PA",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "provinces de Chiriquí et Veraguas",
                "lat": 8.5,
                "lon": -80.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz blanchi : 230 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 66 700 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "moisson, décorticage en rizerie"
            },
            {
                "token": "RESIDUS_MAIS_PA",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "provinces de Chiriquí et Veraguas",
                "lat": 8.5,
                "lon": -80.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 125 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 31 250 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte en ensilage ou grain, andains au champ"
            }
        ]
    },
    "Costa Rica": {
        "nom_fao": "Costa Rica",
        "portrait": "bassin vallée centrale (Alajuela-San José) — profil agricole à compléter (v1.8)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ]
        },
        "intrants": [
            {
                "token": "BAGASSE_CANNE_CR",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "vallée centrale (Alajuela-San José)",
                "lat": 9.8,
                "lon": -84.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "sucre de canne centrifuge : 430 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 129 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de avril à novembre, point sous garde",
                "techniques": "coupe mécanique, pressage en sucrerie"
            },
            {
                "token": "RAFLES_PALMIER_CR",
                "famille": "Tropical",
                "nom_fr": "Rafles de palmier à huile",
                "region": "vallée centrale (Alajuela-San José)",
                "lat": 9.8,
                "lon": -84.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "rafles vides et efflorescences du palmier à huile",
                "production": "régimes de palmier à huile : 1 225 774 t (FAOSTAT QCL 2024)",
                "ratio": "rafles ≈ 0,22 × régimes (ILLUSTRATION)",
                "gisement": "≈ 269 670 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12
                ],
                "fenetre_note": "récolte ou activité continue sur l'année, point sous garde",
                "techniques": "égrappage en huilerie, régimes toute l'année"
            },
            {
                "token": "PARCHE_CAFE_CR",
                "famille": "Tropical",
                "nom_fr": "Parche et pulpe de café",
                "region": "vallée centrale (Alajuela-San José)",
                "lat": 9.8,
                "lon": -84.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "parche, pulpe et mucilage de cerises de café",
                "production": "café vert : 62 154 t (FAOSTAT QCL 2024)",
                "ratio": "parche et pulpe ≈ 0,45 × café vert (ILLUSTRATION)",
                "gisement": "≈ 27 969 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    10,
                    11,
                    12,
                    1,
                    2
                ],
                "fenetre_note": "récolte de octobre à février, point sous garde",
                "techniques": "dépulpage humide ou sec en station"
            },
            {
                "token": "BALLE_RIZ_CR",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "vallée centrale (Alajuela-San José)",
                "lat": 9.8,
                "lon": -84.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz blanchi : 33 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 9 570 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "moisson, décorticage en rizerie"
            },
            {
                "token": "MARC_AGRUME_CR",
                "famille": "Cultures pérennes",
                "nom_fr": "Marc d'agrumes",
                "region": "vallée centrale (Alajuela-San José)",
                "lat": 9.8,
                "lon": -84.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "écorces, pépins et marc d'oranges après pressage",
                "production": "oranges : 250 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "écorces et marc ≈ 0,50 × fruit (ILLUSTRATION)",
                "gisement": "≈ 125 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    11,
                    12,
                    1,
                    2
                ],
                "fenetre_note": "récolte de novembre à février, point sous garde",
                "techniques": "récolte, pressage en juserie"
            }
        ]
    },
    "Nicaragua": {
        "nom_fao": "Nicaragua",
        "portrait": "bassin départements de Chinandega et León — profil agricole à compléter (v1.8)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ]
        },
        "intrants": [
            {
                "token": "BAGASSE_CANNE_NI",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "départements de Chinandega et León",
                "lat": 12.8,
                "lon": -85.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "sucre de canne centrifuge : 760 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 228 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de avril à novembre, point sous garde",
                "techniques": "coupe mécanique, pressage en sucrerie"
            },
            {
                "token": "PAILLE_SORGHO_NI",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "départements de Chinandega et León",
                "lat": 12.8,
                "lon": -85.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 27 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 40 500 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle ou mécanisée, fanage au champ"
            },
            {
                "token": "RESIDUS_MAIS_NI",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "départements de Chinandega et León",
                "lat": 12.8,
                "lon": -85.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 372 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 93 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte en ensilage ou grain, andains au champ"
            },
            {
                "token": "COQUE_ARACHIDE_NI",
                "famille": "Coques & noyaux",
                "nom_fr": "Coques d'arachide",
                "region": "départements de Chinandega et León",
                "lat": 12.8,
                "lon": -85.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "coques d'arachides après décorticage",
                "production": "arachides décortiquées : 215 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "coques ≈ 0,42 × arachides décortiquées (ILLUSTRATION)",
                "gisement": "≈ 90 300 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "arrachage, séchage, décorticage mécanique"
            },
            {
                "token": "BALLE_RIZ_NI",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "départements de Chinandega et León",
                "lat": 12.8,
                "lon": -85.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz blanchi : 286 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 82 940 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "moisson, décorticage en rizerie"
            }
        ]
    },
    "Honduras": {
        "nom_fao": "Honduras",
        "portrait": "bassin vallée du Sula (San Pedro Sula) — profil agricole à compléter (v1.8)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ]
        },
        "intrants": [
            {
                "token": "PARCHE_CAFE_HN",
                "famille": "Tropical",
                "nom_fr": "Parche et pulpe de café",
                "region": "vallée du Sula (San Pedro Sula)",
                "lat": 14.8,
                "lon": -86.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "parche, pulpe et mucilage de cerises de café",
                "production": "café vert : 324 015 t (FAOSTAT QCL 2024)",
                "ratio": "parche et pulpe ≈ 0,45 × café vert (ILLUSTRATION)",
                "gisement": "≈ 145 807 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    10,
                    11,
                    12,
                    1,
                    2
                ],
                "fenetre_note": "récolte de octobre à février, point sous garde",
                "techniques": "dépulpage humide ou sec en station"
            },
            {
                "token": "BAGASSE_CANNE_HN",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "vallée du Sula (San Pedro Sula)",
                "lat": 14.8,
                "lon": -86.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "sucre de canne centrifuge : 548 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 164 400 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de avril à novembre, point sous garde",
                "techniques": "coupe mécanique, pressage en sucrerie"
            },
            {
                "token": "RESIDUS_MAIS_HN",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "vallée du Sula (San Pedro Sula)",
                "lat": 14.8,
                "lon": -86.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 500 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 125 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte en ensilage ou grain, andains au champ"
            },
            {
                "token": "BALLE_RIZ_HN",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "vallée du Sula (San Pedro Sula)",
                "lat": 14.8,
                "lon": -86.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz blanchi : 50 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 14 500 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "moisson, décorticage en rizerie"
            }
        ]
    },
    "Guatemala": {
        "nom_fao": "Guatemala",
        "portrait": "bassin basses terres du Nord (Petén-Alta Verapaz) — profil agricole à compléter (v1.8)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ]
        },
        "intrants": [
            {
                "token": "BAGASSE_CANNE_GT",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "basses terres du Nord (Petén-Alta Verapaz)",
                "lat": 15.5,
                "lon": -90.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "canne à sucre : 22 907 870 t (FAOSTAT QCL 2024)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 6,9 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de avril à novembre, point sous garde",
                "techniques": "coupe mécanique, pressage en sucrerie"
            },
            {
                "token": "PARCHE_CAFE_GT",
                "famille": "Tropical",
                "nom_fr": "Parche et pulpe de café",
                "region": "basses terres du Nord (Petén-Alta Verapaz)",
                "lat": 15.5,
                "lon": -90.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "parche, pulpe et mucilage de cerises de café",
                "production": "café vert : 224 860 t (FAOSTAT QCL 2024)",
                "ratio": "parche et pulpe ≈ 0,45 × café vert (ILLUSTRATION)",
                "gisement": "≈ 101 187 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    10,
                    11,
                    12,
                    1,
                    2
                ],
                "fenetre_note": "récolte de octobre à février, point sous garde",
                "techniques": "dépulpage humide ou sec en station"
            },
            {
                "token": "PAILLE_SORGHO_GT",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "basses terres du Nord (Petén-Alta Verapaz)",
                "lat": 15.5,
                "lon": -90.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 35 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 52 500 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle ou mécanisée, fanage au champ"
            },
            {
                "token": "RESIDUS_MAIS_GT",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "basses terres du Nord (Petén-Alta Verapaz)",
                "lat": 15.5,
                "lon": -90.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 1 625 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 406 250 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte en ensilage ou grain, andains au champ"
            },
            {
                "token": "RAFLES_PALMIER_GT",
                "famille": "Tropical",
                "nom_fr": "Rafles de palmier à huile",
                "region": "basses terres du Nord (Petén-Alta Verapaz)",
                "lat": 15.5,
                "lon": -90.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "rafles vides et efflorescences du palmier à huile",
                "production": "régimes de palmier à huile : 4 175 082 t (FAOSTAT QCL 2024)",
                "ratio": "rafles ≈ 0,22 × régimes (ILLUSTRATION)",
                "gisement": "≈ 918 518 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12
                ],
                "fenetre_note": "récolte ou activité continue sur l'année, point sous garde",
                "techniques": "égrappage en huilerie, régimes toute l'année"
            }
        ]
    },
    "El Salvador": {
        "nom_fao": "El Salvador",
        "portrait": "bassin départements de La Libertad et Usulután — profil agricole à compléter (v1.8)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ]
        },
        "intrants": [
            {
                "token": "BAGASSE_CANNE_SV",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "départements de La Libertad et Usulután",
                "lat": 13.8,
                "lon": -88.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "canne à sucre : 7 310 908 t (FAOSTAT QCL 2024)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 2,2 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de avril à novembre, point sous garde",
                "techniques": "coupe mécanique, pressage en sucrerie"
            },
            {
                "token": "PARCHE_CAFE_SV",
                "famille": "Tropical",
                "nom_fr": "Parche et pulpe de café",
                "region": "départements de La Libertad et Usulután",
                "lat": 13.8,
                "lon": -88.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "parche, pulpe et mucilage de cerises de café",
                "production": "café vert : 30 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "parche et pulpe ≈ 0,45 × café vert (ILLUSTRATION)",
                "gisement": "≈ 13 500 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    10,
                    11,
                    12,
                    1,
                    2
                ],
                "fenetre_note": "récolte de octobre à février, point sous garde",
                "techniques": "dépulpage humide ou sec en station"
            },
            {
                "token": "PAILLE_SORGHO_SV",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "départements de La Libertad et Usulután",
                "lat": 13.8,
                "lon": -88.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 90 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 135 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle ou mécanisée, fanage au champ"
            },
            {
                "token": "RESIDUS_MAIS_SV",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "départements de La Libertad et Usulután",
                "lat": 13.8,
                "lon": -88.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 810 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 202 500 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte en ensilage ou grain, andains au champ"
            }
        ]
    },
    "Cuba": {
        "nom_fao": "Cuba",
        "portrait": "bassin provinces de Camagüey et Ciego de Ávila — profil agricole à compléter (v1.8)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ]
        },
        "intrants": [
            {
                "token": "BAGASSE_CANNE_CU",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "provinces de Camagüey et Ciego de Ávila",
                "lat": 21.8,
                "lon": -79.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "canne à sucre : 9 050 600 t (FAOSTAT QCL 2024)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 2,7 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de avril à novembre, point sous garde",
                "techniques": "coupe mécanique, pressage en sucrerie"
            },
            {
                "token": "BALLE_RIZ_CU",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "provinces de Camagüey et Ciego de Ávila",
                "lat": 21.8,
                "lon": -79.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz blanchi : 153 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 44 370 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "moisson, décorticage en rizerie"
            },
            {
                "token": "RESIDUS_MAIS_CU",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "provinces de Camagüey et Ciego de Ávila",
                "lat": 21.8,
                "lon": -79.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 220 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 55 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte en ensilage ou grain, andains au champ"
            }
        ]
    },
    "Jamaïque": {
        "nom_fao": "Jamaica",
        "portrait": "bassin plaine de la Middlesex (Spanish Town) — profil agricole à compléter (v1.8)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ]
        },
        "intrants": [
            {
                "token": "BAGASSE_CANNE_JM",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "plaine de la Middlesex (Spanish Town)",
                "lat": 18.1,
                "lon": -77.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "sucre de canne centrifuge : 34 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 10 200 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de avril à novembre, point sous garde",
                "techniques": "coupe mécanique, pressage en sucrerie"
            },
            {
                "token": "PARCHE_CAFE_JM",
                "famille": "Tropical",
                "nom_fr": "Parche et pulpe de café",
                "region": "plaine de la Middlesex (Spanish Town)",
                "lat": 18.1,
                "lon": -77.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "parche, pulpe et mucilage de cerises de café",
                "production": "café vert : 1 200 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "parche et pulpe ≈ 0,45 × café vert (ILLUSTRATION)",
                "gisement": "≈ 540 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    10,
                    11,
                    12,
                    1,
                    2
                ],
                "fenetre_note": "récolte de octobre à février, point sous garde",
                "techniques": "dépulpage humide ou sec en station"
            },
            {
                "token": "CABOSSE_CACAO_JM",
                "famille": "Coques & noyaux",
                "nom_fr": "Cabosse de cacao",
                "region": "plaine de la Middlesex (Spanish Town)",
                "lat": 18.1,
                "lon": -77.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "cabosses fendues et mucilage de cacao",
                "production": "fèves de cacao sèches : 201 t (tableau Wikipédia (FAOSTAT, année de l'article))",
                "ratio": "cabosse ≈ 8 × fèves sèches (ILLUSTRATION)",
                "gisement": "≈ 1 608 t/an",
                "etiquette_gisement": "SOURCÉ (production tableau Wikipédia (FAOSTAT, année de l'article)) + ratio ILLUSTRATION",
                "fenetre": [
                    10,
                    11,
                    12,
                    1,
                    2,
                    3
                ],
                "fenetre_note": "récolte de octobre à mars, point sous garde",
                "techniques": "cabossage manuel, fermentation des fèves"
            }
        ]
    },
    "Haïti": {
        "nom_fao": "Haiti",
        "portrait": "bassin plaine de l'Artibonite (Gonaïves) — profil agricole à compléter (v1.8)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ]
        },
        "intrants": [
            {
                "token": "BALLE_RIZ_HT",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "plaine de l'Artibonite (Gonaïves)",
                "lat": 19.0,
                "lon": -72.4,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz blanchi : 52 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 15 080 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "moisson, décorticage en rizerie"
            }
        ]
    },
    "Rép. dominicaine": {
        "nom_fao": "Dominican Republic",
        "portrait": "bassin vallée du Cibao (Santiago-La Vega) — profil agricole à compléter (v1.8)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ]
        },
        "intrants": [
            {
                "token": "BAGASSE_CANNE_DO",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "vallée du Cibao (Santiago-La Vega)",
                "lat": 19.3,
                "lon": -70.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "sucre de canne centrifuge : 520 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 156 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de avril à novembre, point sous garde",
                "techniques": "coupe mécanique, pressage en sucrerie"
            },
            {
                "token": "BALLE_RIZ_DO",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "vallée du Cibao (Santiago-La Vega)",
                "lat": 19.3,
                "lon": -70.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz blanchi : 680 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 197 200 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "moisson, décorticage en rizerie"
            },
            {
                "token": "CABOSSE_CACAO_DO",
                "famille": "Coques & noyaux",
                "nom_fr": "Cabosse de cacao",
                "region": "vallée du Cibao (Santiago-La Vega)",
                "lat": 19.3,
                "lon": -70.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "cabosses fendues et mucilage de cacao",
                "production": "fèves de cacao sèches : 57 461 t (FAOSTAT QCL 2024)",
                "ratio": "cabosse ≈ 8 × fèves sèches (ILLUSTRATION)",
                "gisement": "≈ 459 688 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    10,
                    11,
                    12,
                    1,
                    2,
                    3
                ],
                "fenetre_note": "récolte de octobre à mars, point sous garde",
                "techniques": "cabossage manuel, fermentation des fèves"
            },
            {
                "token": "PARCHE_CAFE_DO",
                "famille": "Tropical",
                "nom_fr": "Parche et pulpe de café",
                "region": "vallée du Cibao (Santiago-La Vega)",
                "lat": 19.3,
                "lon": -70.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "parche, pulpe et mucilage de cerises de café",
                "production": "café vert : 7 500 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "parche et pulpe ≈ 0,45 × café vert (ILLUSTRATION)",
                "gisement": "≈ 3 375 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    10,
                    11,
                    12,
                    1,
                    2
                ],
                "fenetre_note": "récolte de octobre à février, point sous garde",
                "techniques": "dépulpage humide ou sec en station"
            }
        ]
    },
    "Trinité-et-Tobago": {
        "nom_fao": "Trinidad and Tobago",
        "portrait": "bassin comté de Caroni, île de Trinidad — profil agricole à compléter (v1.8)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ]
        },
        "intrants": [
            {
                "token": "CABOSSE_CACAO_TT",
                "famille": "Coques & noyaux",
                "nom_fr": "Cabosse de cacao",
                "region": "comté de Caroni, île de Trinidad",
                "lat": 10.5,
                "lon": -61.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "cabosses fendues et mucilage de cacao",
                "production": "fèves de cacao sèches : 231 t (tableau Wikipédia (FAOSTAT, année de l'article))",
                "ratio": "cabosse ≈ 8 × fèves sèches (ILLUSTRATION)",
                "gisement": "≈ 1 848 t/an",
                "etiquette_gisement": "SOURCÉ (production tableau Wikipédia (FAOSTAT, année de l'article)) + ratio ILLUSTRATION",
                "fenetre": [
                    10,
                    11,
                    12,
                    1,
                    2,
                    3
                ],
                "fenetre_note": "récolte de octobre à mars, point sous garde",
                "techniques": "cabossage manuel, fermentation des fèves"
            }
        ]
    },
    "Belize": {
        "nom_fao": "Belize",
        "portrait": "bassin districts de Corozal et Orange Walk — profil agricole à compléter (v1.8)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.8)"
            ]
        },
        "intrants": [
            {
                "token": "BAGASSE_CANNE_BZ",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "districts de Corozal et Orange Walk",
                "lat": 17.2,
                "lon": -88.6,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "sucre de canne centrifuge : 200 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 60 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de avril à novembre, point sous garde",
                "techniques": "coupe mécanique, pressage en sucrerie"
            },
            {
                "token": "BALLE_RIZ_BZ",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "districts de Corozal et Orange Walk",
                "lat": 17.2,
                "lon": -88.6,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz paddy : 15 364 t (tableau Wikipédia (FAOSTAT, année de l'article))",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 3 073 t/an",
                "etiquette_gisement": "SOURCÉ (production tableau Wikipédia (FAOSTAT, année de l'article)) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "moisson, décorticage en rizerie"
            }
        ]
    }
}


def _index():
    idx = {}
    for pays, fiche in PAYS_AMERIQUE_LATINE.items():
        for intrant in fiche["intrants"]:
            idx[intrant["token"]] = (pays, intrant)
    return idx


INDEX = _index()


def verifier_couverture():
    return set(INDEX) & (set(_master.ATLAS_BIOMASSES_MONDE) | set(_p11.INDEX)
                         | set(_v12.INDEX) | set(_v13.INDEX))


def sommaire():
    lignes = ["Atlas Amérique latine et centrale restante (v1.8) — %d pays, %d intrants" % (len(PAYS_AMERIQUE_LATINE), len(INDEX))]
    for pays in sorted(PAYS_AMERIQUE_LATINE, key=lambda p: p.lower()):
        lignes.append("  %s — %d intrant(s)" % (pays, len(PAYS_AMERIQUE_LATINE[pays]["intrants"])))
    return "\n".join(lignes)


def fiche_token(token):
    if token not in INDEX:
        return None
    pays, intrant = INDEX[token]
    return {"pays": pays, "intrant": intrant}


def croisement():
    lignes = ["Pays couverts : %d" % len(PAYS_AMERIQUE_LATINE)]
    lignes.append("Intrants : %d (attendu 66)" % len(INDEX))
    lignes.append("Collisions de jetons avec v1.0-v1.3 : %d" % len(verifier_couverture()))
    familles = sorted({i["famille"] for (_, i) in INDEX.values()})
    lignes.append("Familles : %s" % ", ".join(familles))
    hors = [t for t, (_, i) in INDEX.items() if not (0 <= i["lat"] <= 90 and -180 <= i["lon"] <= 180)]
    lignes.append("Coordonnées hors globe : %d" % len(hors))
    return "\n".join(lignes)


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] == "sommaire":
        print(sommaire())
    elif args[0] == "croisement":
        print(croisement())
    else:
        f = fiche_token(args[0])
        print(json.dumps(f, ensure_ascii=False, indent=2) if f else "jeton inconnu : %s" % args[0])


if __name__ == "__main__":
    main()
