#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""World Twin v1.7 — Atlas des biomasses : Afrique complète.

Extension régionale de la lignée d'atlas (monde v1.0, pays v1.1, vignobles
v1.2, Asie v1.3) : pour les pays non encore couverts de cette région, les
biomasses LOCALES majeures sont placées sur le globe — région, point GPS
(Global Positioning System, approximation de bassin, jamais un cadastre),
type, volume, fenêtre saisonnière, techniques culturales — avec, par pays,
une synthèse réglementaire à cinq postes, tous À VÉRIFIER.

136 intrants, productions SOURCÉES (FAOSTAT QCL 2024 via Commodity
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
    python3 engine/atlas_afrique.py                # sommaire par pays
    python3 engine/atlas_afrique.py TOKEN          # fiche d'un intrant
    python3 engine/atlas_afrique.py croisement     # contrôles complets
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
PAYS_AFRIQUE = {
    "Algérie": {
        "nom_fao": "Algeria",
        "portrait": "bassin Hauts Plateaux céréaliers (Sétif-Constantine) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "NOYAU_DATTE_DZ",
                "famille": "Coques & noyaux",
                "nom_fr": "Noyaux et rachis de dattes",
                "region": "Hauts Plateaux céréaliers (Sétif-Constantine)",
                "lat": 36.5,
                "lon": 3.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "noyaux, rachis et écarts de tri des dattes",
                "production": "dattes : 1 337 301 t (FAOSTAT QCL 2024)",
                "ratio": "noyaux et rachis ≈ 0,12 × dattes (ILLUSTRATION)",
                "gisement": "≈ 160 476 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8,
                    9,
                    10
                ],
                "fenetre_note": "récolte de juillet à octobre, point sous garde",
                "techniques": "tri en station de conditionnement"
            },
            {
                "token": "PAILLE_BLE_DZ",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "Hauts Plateaux céréaliers (Sétif-Constantine)",
                "lat": 36.5,
                "lon": 3.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 3 000 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 3,6 Mt/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    6,
                    7,
                    8
                ],
                "fenetre_note": "récolte de juin à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes, fourrage prioritaire"
            },
            {
                "token": "PAILLE_ORGE_DZ",
                "famille": "Céréales",
                "nom_fr": "Paille d'orge",
                "region": "Hauts Plateaux céréaliers (Sétif-Constantine)",
                "lat": 36.5,
                "lon": 3.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'orge, chaumes et glumes",
                "production": "orge : 1 200 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 1,2 Mt/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            },
            {
                "token": "GRIGNONS_OLIVE_DZ",
                "famille": "Coques & noyaux",
                "nom_fr": "Grignons d'olive",
                "region": "Hauts Plateaux céréaliers (Sétif-Constantine)",
                "lat": 36.5,
                "lon": 3.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "grignons, noyaux et margines d'olives à huile",
                "production": "huile d'olive : 81 300 t (FAOSTAT QCL 2023)",
                "ratio": "grignons ≈ 1,75 × huile (olives ≈ 5 × huile, grignons ≈ 0,35 × olives) (ILLUSTRATION)",
                "gisement": "≈ 142 275 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2023) + ratio ILLUSTRATION",
                "fenetre": [
                    10,
                    11,
                    12
                ],
                "fenetre_note": "récolte de octobre à décembre, point sous garde",
                "techniques": "récolte, trituration en huilerie"
            },
            {
                "token": "MARC_AGRUME_DZ",
                "famille": "Cultures pérennes",
                "nom_fr": "Marc d'agrumes",
                "region": "Hauts Plateaux céréaliers (Sétif-Constantine)",
                "lat": 36.5,
                "lon": 3.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "écorces, pépins et marc d'oranges après pressage",
                "production": "oranges : 1 294 262 t (FAOSTAT QCL 2024)",
                "ratio": "écorces et marc ≈ 0,50 × fruit (ILLUSTRATION)",
                "gisement": "≈ 647 131 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    11,
                    12,
                    1,
                    2
                ],
                "fenetre_note": "récolte de novembre à février, point sous garde",
                "techniques": "récolte, pressage en juserie"
            },
            {
                "token": "MARC_RAISIN_DZ",
                "famille": "Cultures pérennes",
                "nom_fr": "Marc de raisin de table",
                "region": "Hauts Plateaux céréaliers (Sétif-Constantine)",
                "lat": 36.5,
                "lon": 3.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "rafles, pépons et marc de raisin de table frais",
                "production": "raisin : 605 260 t (FAOSTAT QCL 2024)",
                "ratio": "marc ≈ 0,25 × raisin (ILLUSTRATION)",
                "gisement": "≈ 151 315 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10
                ],
                "fenetre_note": "récolte de septembre à octobre, point sous garde",
                "techniques": "récolte en frais, écarts de table"
            }
        ]
    },
    "Tunisie": {
        "nom_fao": "Tunisia",
        "portrait": "bassin vallée de la Medjerda — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "NOYAU_DATTE_TN",
                "famille": "Coques & noyaux",
                "nom_fr": "Noyaux et rachis de dattes",
                "region": "vallée de la Medjerda",
                "lat": 36.3,
                "lon": 9.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "noyaux, rachis et écarts de tri des dattes",
                "production": "dattes : 400 219 t (FAOSTAT QCL 2024)",
                "ratio": "noyaux et rachis ≈ 0,12 × dattes (ILLUSTRATION)",
                "gisement": "≈ 48 026 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8,
                    9,
                    10
                ],
                "fenetre_note": "récolte de juillet à octobre, point sous garde",
                "techniques": "tri en station de conditionnement"
            },
            {
                "token": "GRIGNONS_OLIVE_TN",
                "famille": "Coques & noyaux",
                "nom_fr": "Grignons d'olive",
                "region": "vallée de la Medjerda",
                "lat": 36.3,
                "lon": 9.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "grignons, noyaux et margines d'olives à huile",
                "production": "huile d'olive : 210 000 t (FAOSTAT QCL 2023)",
                "ratio": "grignons ≈ 1,75 × huile (olives ≈ 5 × huile, grignons ≈ 0,35 × olives) (ILLUSTRATION)",
                "gisement": "≈ 367 500 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2023) + ratio ILLUSTRATION",
                "fenetre": [
                    10,
                    11,
                    12
                ],
                "fenetre_note": "récolte de octobre à décembre, point sous garde",
                "techniques": "récolte, trituration en huilerie"
            },
            {
                "token": "PAILLE_BLE_TN",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "vallée de la Medjerda",
                "lat": 36.3,
                "lon": 9.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 1 150 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 1,4 Mt/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    6,
                    7,
                    8
                ],
                "fenetre_note": "récolte de juin à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes, fourrage prioritaire"
            },
            {
                "token": "PAILLE_ORGE_TN",
                "famille": "Céréales",
                "nom_fr": "Paille d'orge",
                "region": "vallée de la Medjerda",
                "lat": 36.3,
                "lon": 9.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'orge, chaumes et glumes",
                "production": "orge : 550 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 550 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            },
            {
                "token": "MARC_AGRUME_TN",
                "famille": "Cultures pérennes",
                "nom_fr": "Marc d'agrumes",
                "region": "vallée de la Medjerda",
                "lat": 36.3,
                "lon": 9.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "écorces, pépins et marc d'oranges après pressage",
                "production": "oranges : 416 897 t (FAOSTAT QCL 2024)",
                "ratio": "écorces et marc ≈ 0,50 × fruit (ILLUSTRATION)",
                "gisement": "≈ 208 449 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
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
    "Libye": {
        "nom_fao": "Libya",
        "portrait": "bassin côte de Tripolitaine et oasis du Fezzan — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "NOYAU_DATTE_LY",
                "famille": "Coques & noyaux",
                "nom_fr": "Noyaux et rachis de dattes",
                "region": "côte de Tripolitaine et oasis du Fezzan",
                "lat": 28.0,
                "lon": 17.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "noyaux, rachis et écarts de tri des dattes",
                "production": "dattes : 187 039 t (FAOSTAT QCL 2024)",
                "ratio": "noyaux et rachis ≈ 0,12 × dattes (ILLUSTRATION)",
                "gisement": "≈ 22 445 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8,
                    9,
                    10
                ],
                "fenetre_note": "récolte de juillet à octobre, point sous garde",
                "techniques": "tri en station de conditionnement"
            },
            {
                "token": "PAILLE_BLE_LY",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "côte de Tripolitaine et oasis du Fezzan",
                "lat": 28.0,
                "lon": 17.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 200 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 240 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    6,
                    7,
                    8
                ],
                "fenetre_note": "récolte de juin à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes, fourrage prioritaire"
            },
            {
                "token": "PAILLE_ORGE_LY",
                "famille": "Céréales",
                "nom_fr": "Paille d'orge",
                "region": "côte de Tripolitaine et oasis du Fezzan",
                "lat": 28.0,
                "lon": 17.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'orge, chaumes et glumes",
                "production": "orge : 100 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 100 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            },
            {
                "token": "GRIGNONS_OLIVE_LY",
                "famille": "Coques & noyaux",
                "nom_fr": "Grignons d'olive",
                "region": "côte de Tripolitaine et oasis du Fezzan",
                "lat": 28.0,
                "lon": 17.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "grignons, noyaux et margines d'olives à huile",
                "production": "huile d'olive : 16 000 t (FAOSTAT QCL 2023)",
                "ratio": "grignons ≈ 1,75 × huile (olives ≈ 5 × huile, grignons ≈ 0,35 × olives) (ILLUSTRATION)",
                "gisement": "≈ 28 000 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2023) + ratio ILLUSTRATION",
                "fenetre": [
                    10,
                    11,
                    12
                ],
                "fenetre_note": "récolte de octobre à décembre, point sous garde",
                "techniques": "récolte, trituration en huilerie"
            }
        ]
    },
    "Mauritanie": {
        "nom_fao": "Mauritania",
        "portrait": "bassin vallée du Sénégal (Nouakchott-Rosso) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_SORGHO_MR",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "vallée du Sénégal (Nouakchott-Rosso)",
                "lat": 19.5,
                "lon": -10.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 70 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 105 000 t/an",
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
                "token": "PAILLE_MIL_MR",
                "famille": "Céréales",
                "nom_fr": "Paille de mil",
                "region": "vallée du Sénégal (Nouakchott-Rosso)",
                "lat": 19.5,
                "lon": -10.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de mil",
                "production": "mil : 3 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 4 500 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle, gerbes au champ"
            },
            {
                "token": "BALLE_RIZ_MR",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "vallée du Sénégal (Nouakchott-Rosso)",
                "lat": 19.5,
                "lon": -10.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz blanchi : 276 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 80 040 t/an",
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
    "Sénégal": {
        "nom_fao": "Senegal",
        "portrait": "bassin bassin arachidier (Kaolack-Fatick) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_MIL_SN",
                "famille": "Céréales",
                "nom_fr": "Paille de mil",
                "region": "bassin arachidier (Kaolack-Fatick)",
                "lat": 14.7,
                "lon": -15.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de mil",
                "production": "mil : 1 100 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 1,6 Mt/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle, gerbes au champ"
            },
            {
                "token": "PAILLE_SORGHO_SN",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "bassin arachidier (Kaolack-Fatick)",
                "lat": 14.7,
                "lon": -15.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 445 000 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 667 500 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle ou mécanisée, fanage au champ"
            },
            {
                "token": "COQUE_ARACHIDE_SN",
                "famille": "Coques & noyaux",
                "nom_fr": "Coques d'arachide",
                "region": "bassin arachidier (Kaolack-Fatick)",
                "lat": 14.7,
                "lon": -15.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "coques d'arachides après décorticage",
                "production": "arachides en coque : 1 681 953 t (FAOSTAT QCL 2024)",
                "ratio": "coques ≈ 0,30 × arachides en coque (ILLUSTRATION)",
                "gisement": "≈ 504 586 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "arrachage, séchage, décorticage mécanique"
            },
            {
                "token": "BALLE_RIZ_SN",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "bassin arachidier (Kaolack-Fatick)",
                "lat": 14.7,
                "lon": -15.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz blanchi : 1 020 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 295 800 t/an",
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
    "Mali": {
        "nom_fao": "Mali",
        "portrait": "bassin delta intérieur du Niger (Ségou-Mopti) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_MIL_ML",
                "famille": "Céréales",
                "nom_fr": "Paille de mil",
                "region": "delta intérieur du Niger (Ségou-Mopti)",
                "lat": 17.5,
                "lon": -3.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de mil",
                "production": "mil : 1 800 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 2,7 Mt/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle, gerbes au champ"
            },
            {
                "token": "PAILLE_SORGHO_ML",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "delta intérieur du Niger (Ségou-Mopti)",
                "lat": 17.5,
                "lon": -3.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 1 640 848 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 2,5 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle ou mécanisée, fanage au champ"
            },
            {
                "token": "BALLE_RIZ_ML",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "delta intérieur du Niger (Ségou-Mopti)",
                "lat": 17.5,
                "lon": -3.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz blanchi : 2 020 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 585 800 t/an",
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
                "token": "COQUE_ARACHIDE_ML",
                "famille": "Coques & noyaux",
                "nom_fr": "Coques d'arachide",
                "region": "delta intérieur du Niger (Ségou-Mopti)",
                "lat": 17.5,
                "lon": -3.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "coques d'arachides après décorticage",
                "production": "arachides en coque : 497 436 t (FAOSTAT QCL 2024)",
                "ratio": "coques ≈ 0,30 × arachides en coque (ILLUSTRATION)",
                "gisement": "≈ 149 231 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "arrachage, séchage, décorticage mécanique"
            }
        ]
    },
    "Burkina Faso": {
        "nom_fao": "Burkina Faso",
        "portrait": "bassin plateau central (Ouagadougou-Koudougou) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_MIL_BF",
                "famille": "Céréales",
                "nom_fr": "Paille de mil",
                "region": "plateau central (Ouagadougou-Koudougou)",
                "lat": 12.8,
                "lon": -1.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de mil",
                "production": "mil : 1 000 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 1,5 Mt/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle, gerbes au champ"
            },
            {
                "token": "PAILLE_SORGHO_BF",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "plateau central (Ouagadougou-Koudougou)",
                "lat": 12.8,
                "lon": -1.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 1 900 000 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 2,9 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle ou mécanisée, fanage au champ"
            },
            {
                "token": "RESIDUS_MAIS_BF",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "plateau central (Ouagadougou-Koudougou)",
                "lat": 12.8,
                "lon": -1.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 1 850 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 462 500 t/an",
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
                "token": "COQUE_ARACHIDE_BF",
                "famille": "Coques & noyaux",
                "nom_fr": "Coques d'arachide",
                "region": "plateau central (Ouagadougou-Koudougou)",
                "lat": 12.8,
                "lon": -1.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "coques d'arachides après décorticage",
                "production": "arachides en coque : 611 271 t (FAOSTAT QCL 2024)",
                "ratio": "coques ≈ 0,30 × arachides en coque (ILLUSTRATION)",
                "gisement": "≈ 183 381 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "arrachage, séchage, décorticage mécanique"
            }
        ]
    },
    "Niger": {
        "nom_fao": "Niger",
        "portrait": "bassin régions de Tahoua et Dosso — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_MIL_NE",
                "famille": "Céréales",
                "nom_fr": "Paille de mil",
                "region": "régions de Tahoua et Dosso",
                "lat": 17.0,
                "lon": 8.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de mil",
                "production": "mil : 3 400 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 5,1 Mt/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle, gerbes au champ"
            },
            {
                "token": "PAILLE_SORGHO_NE",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "régions de Tahoua et Dosso",
                "lat": 17.0,
                "lon": 8.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 1 907 733 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 2,9 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle ou mécanisée, fanage au champ"
            },
            {
                "token": "COQUE_ARACHIDE_NE",
                "famille": "Coques & noyaux",
                "nom_fr": "Coques d'arachide",
                "region": "régions de Tahoua et Dosso",
                "lat": 17.0,
                "lon": 8.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "coques d'arachides après décorticage",
                "production": "arachides en coque : 676 651 t (FAOSTAT QCL 2024)",
                "ratio": "coques ≈ 0,30 × arachides en coque (ILLUSTRATION)",
                "gisement": "≈ 202 995 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "arrachage, séchage, décorticage mécanique"
            }
        ]
    },
    "Tchad": {
        "nom_fao": "Chad",
        "portrait": "bassin bassin du Chari-Logone (Moundou) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_SORGHO_TD",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "bassin du Chari-Logone (Moundou)",
                "lat": 15.0,
                "lon": 18.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 720 086 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 1,1 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle ou mécanisée, fanage au champ"
            },
            {
                "token": "PAILLE_MIL_TD",
                "famille": "Céréales",
                "nom_fr": "Paille de mil",
                "region": "bassin du Chari-Logone (Moundou)",
                "lat": 15.0,
                "lon": 18.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de mil",
                "production": "mil : 700 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 1,1 Mt/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle, gerbes au champ"
            },
            {
                "token": "COQUE_ARACHIDE_TD",
                "famille": "Coques & noyaux",
                "nom_fr": "Coques d'arachide",
                "region": "bassin du Chari-Logone (Moundou)",
                "lat": 15.0,
                "lon": 18.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "coques d'arachides après décorticage",
                "production": "arachides en coque : 692 960 t (FAOSTAT QCL 2024)",
                "ratio": "coques ≈ 0,30 × arachides en coque (ILLUSTRATION)",
                "gisement": "≈ 207 888 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "arrachage, séchage, décorticage mécanique"
            },
            {
                "token": "TIGE_COTON_TD",
                "famille": "Céréales",
                "nom_fr": "Tiges de coton",
                "region": "bassin du Chari-Logone (Moundou)",
                "lat": 15.0,
                "lon": 18.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et racines de cotonnier arrachées après récolte",
                "production": "coton brut (fibres) : 35 924 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "tiges ≈ 3 × coton brut (ILLUSTRATION)",
                "gisement": "≈ 107 773 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11,
                    12
                ],
                "fenetre_note": "récolte de septembre à décembre, point sous garde",
                "techniques": "récolte mécanique ou manuelle, arrachage des tiges"
            }
        ]
    },
    "Nigeria": {
        "nom_fao": "Nigeria",
        "portrait": "bassin ceinture maïs et manioc du Middle Belt — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "ECORCES_MANIOC_NG",
                "famille": "Tropical",
                "nom_fr": "Écorces de manioc",
                "region": "ceinture maïs et manioc du Middle Belt",
                "lat": 9.0,
                "lon": 8.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "écorces et déchets de racines de manioc",
                "production": "manioc (racines fraîches) : 62 624 946 t (FAOSTAT QCL 2024)",
                "ratio": "écorces ≈ 0,15 × racines fraîches (ILLUSTRATION)",
                "gisement": "≈ 9,4 Mt/an",
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
                "techniques": "arrachage manuel ou mécanique, décorticage"
            },
            {
                "token": "RESIDUS_MAIS_NG",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "ceinture maïs et manioc du Middle Belt",
                "lat": 9.0,
                "lon": 8.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 11 164 000 t (FAOSTAT QCL 2024)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 2,8 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte en ensilage ou grain, andains au champ"
            },
            {
                "token": "PAILLE_MIL_NG",
                "famille": "Céréales",
                "nom_fr": "Paille de mil",
                "region": "ceinture maïs et manioc du Middle Belt",
                "lat": 9.0,
                "lon": 8.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de mil",
                "production": "mil : 1 700 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 2,5 Mt/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle, gerbes au champ"
            },
            {
                "token": "PAILLE_SORGHO_NG",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "ceinture maïs et manioc du Middle Belt",
                "lat": 9.0,
                "lon": 8.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 6 500 000 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 9,8 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle ou mécanisée, fanage au champ"
            },
            {
                "token": "CABOSSE_CACAO_NG",
                "famille": "Coques & noyaux",
                "nom_fr": "Cabosse de cacao",
                "region": "ceinture maïs et manioc du Middle Belt",
                "lat": 9.0,
                "lon": 8.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "cabosses fendues et mucilage de cacao",
                "production": "fèves de cacao sèches : 350 000 t (FAOSTAT QCL 2024)",
                "ratio": "cabosse ≈ 8 × fèves sèches (ILLUSTRATION)",
                "gisement": "≈ 2,8 Mt/an",
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
                "token": "RAFLES_PALMIER_NG",
                "famille": "Tropical",
                "nom_fr": "Rafles de palmier à huile",
                "region": "ceinture maïs et manioc du Middle Belt",
                "lat": 9.0,
                "lon": 8.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "rafles vides et efflorescences du palmier à huile",
                "production": "régimes de palmier à huile : 11 517 078 t (FAOSTAT QCL 2024)",
                "ratio": "rafles ≈ 0,22 × régimes (ILLUSTRATION)",
                "gisement": "≈ 2,5 Mt/an",
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
                "token": "TIGE_COTON_NG",
                "famille": "Céréales",
                "nom_fr": "Tiges de coton",
                "region": "ceinture maïs et manioc du Middle Belt",
                "lat": 9.0,
                "lon": 8.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et racines de cotonnier arrachées après récolte",
                "production": "coton égrené : 99 200 t (FAOSTAT QCL 2023)",
                "ratio": "tiges ≈ 3 × coton brut (ILLUSTRATION)",
                "gisement": "≈ 297 600 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2023) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11,
                    12
                ],
                "fenetre_note": "récolte de septembre à décembre, point sous garde",
                "techniques": "récolte mécanique ou manuelle, arrachage des tiges"
            },
            {
                "token": "COQUE_ARACHIDE_NG",
                "famille": "Coques & noyaux",
                "nom_fr": "Coques d'arachide",
                "region": "ceinture maïs et manioc du Middle Belt",
                "lat": 9.0,
                "lon": 8.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "coques d'arachides après décorticage",
                "production": "arachides en coque : 4 300 000 t (FAOSTAT QCL 2024)",
                "ratio": "coques ≈ 0,30 × arachides en coque (ILLUSTRATION)",
                "gisement": "≈ 1,3 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "arrachage, séchage, décorticage mécanique"
            },
            {
                "token": "BALLE_RIZ_NG",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "ceinture maïs et manioc du Middle Belt",
                "lat": 9.0,
                "lon": 8.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz paddy : 9 129 900 t (FAOSTAT QCL 2024)",
                "ratio": "balle ≈ 0,20 × riz paddy (ILLUSTRATION)",
                "gisement": "≈ 1,8 Mt/an",
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
                "token": "BAGASSE_CANNE_NG",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "ceinture maïs et manioc du Middle Belt",
                "lat": 9.0,
                "lon": 8.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "sucre de canne centrifuge : 80 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 24 000 t/an",
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
            }
        ]
    },
    "Ghana": {
        "nom_fao": "Ghana",
        "portrait": "bassin bassin cacaoyer du Sud-Ouest (Kumasi) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "CABOSSE_CACAO_GH",
                "famille": "Coques & noyaux",
                "nom_fr": "Cabosse de cacao",
                "region": "bassin cacaoyer du Sud-Ouest (Kumasi)",
                "lat": 7.9,
                "lon": -1.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "cabosses fendues et mucilage de cacao",
                "production": "fèves de cacao sèches : 530 000 t (FAOSTAT QCL 2024)",
                "ratio": "cabosse ≈ 8 × fèves sèches (ILLUSTRATION)",
                "gisement": "≈ 4,2 Mt/an",
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
                "token": "ECORCES_MANIOC_GH",
                "famille": "Tropical",
                "nom_fr": "Écorces de manioc",
                "region": "bassin cacaoyer du Sud-Ouest (Kumasi)",
                "lat": 7.9,
                "lon": -1.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "écorces et déchets de racines de manioc",
                "production": "manioc (racines fraîches) : 27 917 781 t (FAOSTAT QCL 2024)",
                "ratio": "écorces ≈ 0,15 × racines fraîches (ILLUSTRATION)",
                "gisement": "≈ 4,2 Mt/an",
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
                "techniques": "arrachage manuel ou mécanique, décorticage"
            },
            {
                "token": "RESIDUS_MAIS_GH",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "bassin cacaoyer du Sud-Ouest (Kumasi)",
                "lat": 7.9,
                "lon": -1.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 2 600 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 650 000 t/an",
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
                "token": "RAFLES_PALMIER_GH",
                "famille": "Tropical",
                "nom_fr": "Rafles de palmier à huile",
                "region": "bassin cacaoyer du Sud-Ouest (Kumasi)",
                "lat": 7.9,
                "lon": -1.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "rafles vides et efflorescences du palmier à huile",
                "production": "régimes de palmier à huile : 3 210 394 t (FAOSTAT QCL 2024)",
                "ratio": "rafles ≈ 0,22 × régimes (ILLUSTRATION)",
                "gisement": "≈ 706 287 t/an",
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
    "Bénin": {
        "nom_fao": "Benin",
        "portrait": "bassin plateau d'Abomey et Borgou — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "ECORCES_MANIOC_BJ",
                "famille": "Tropical",
                "nom_fr": "Écorces de manioc",
                "region": "plateau d'Abomey et Borgou",
                "lat": 9.8,
                "lon": 2.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "écorces et déchets de racines de manioc",
                "production": "manioc (racines fraîches) : 4 448 391 t (FAOSTAT QCL 2024)",
                "ratio": "écorces ≈ 0,15 × racines fraîches (ILLUSTRATION)",
                "gisement": "≈ 667 259 t/an",
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
                "techniques": "arrachage manuel ou mécanique, décorticage"
            },
            {
                "token": "RESIDUS_MAIS_BJ",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "plateau d'Abomey et Borgou",
                "lat": 9.8,
                "lon": 2.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 1 600 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 400 000 t/an",
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
                "token": "TIGE_COTON_BJ",
                "famille": "Céréales",
                "nom_fr": "Tiges de coton",
                "region": "plateau d'Abomey et Borgou",
                "lat": 9.8,
                "lon": 2.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et racines de cotonnier arrachées après récolte",
                "production": "coton égrené : 219 130 t (FAOSTAT QCL 2023)",
                "ratio": "tiges ≈ 3 × coton brut (ILLUSTRATION)",
                "gisement": "≈ 657 391 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2023) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11,
                    12
                ],
                "fenetre_note": "récolte de septembre à décembre, point sous garde",
                "techniques": "récolte mécanique ou manuelle, arrachage des tiges"
            },
            {
                "token": "RAFLES_PALMIER_BJ",
                "famille": "Tropical",
                "nom_fr": "Rafles de palmier à huile",
                "region": "plateau d'Abomey et Borgou",
                "lat": 9.8,
                "lon": 2.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "rafles vides et efflorescences du palmier à huile",
                "production": "régimes de palmier à huile : 755 057 t (FAOSTAT QCL 2024)",
                "ratio": "rafles ≈ 0,22 × régimes (ILLUSTRATION)",
                "gisement": "≈ 166 113 t/an",
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
                "token": "COQUE_ARACHIDE_BJ",
                "famille": "Coques & noyaux",
                "nom_fr": "Coques d'arachide",
                "region": "plateau d'Abomey et Borgou",
                "lat": 9.8,
                "lon": 2.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "coques d'arachides après décorticage",
                "production": "arachides décortiquées : 175 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "coques ≈ 0,42 × arachides décortiquées (ILLUSTRATION)",
                "gisement": "≈ 73 500 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "arrachage, séchage, décorticage mécanique"
            }
        ]
    },
    "Togo": {
        "nom_fao": "Togo",
        "portrait": "bassin plateau central (Kara-Sokodé) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "RESIDUS_MAIS_TG",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "plateau central (Kara-Sokodé)",
                "lat": 8.7,
                "lon": 0.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 1 000 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 250 000 t/an",
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
                "token": "TIGE_COTON_TG",
                "famille": "Céréales",
                "nom_fr": "Tiges de coton",
                "region": "plateau central (Kara-Sokodé)",
                "lat": 8.7,
                "lon": 0.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et racines de cotonnier arrachées après récolte",
                "production": "coton brut (fibres) : 28 304 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "tiges ≈ 3 × coton brut (ILLUSTRATION)",
                "gisement": "≈ 84 912 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11,
                    12
                ],
                "fenetre_note": "récolte de septembre à décembre, point sous garde",
                "techniques": "récolte mécanique ou manuelle, arrachage des tiges"
            },
            {
                "token": "PAILLE_MIL_TG",
                "famille": "Céréales",
                "nom_fr": "Paille de mil",
                "region": "plateau central (Kara-Sokodé)",
                "lat": 8.7,
                "lon": 0.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de mil",
                "production": "mil : 30 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 45 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle, gerbes au champ"
            }
        ]
    },
    "Cameroun": {
        "nom_fao": "Cameroon",
        "portrait": "bassin Ouest forestier et Littoral (Douala) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "ECORCES_MANIOC_CM",
                "famille": "Tropical",
                "nom_fr": "Écorces de manioc",
                "region": "Ouest forestier et Littoral (Douala)",
                "lat": 5.5,
                "lon": 12.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "écorces et déchets de racines de manioc",
                "production": "manioc (racines fraîches) : 6 658 483 t (FAOSTAT QCL 2024)",
                "ratio": "écorces ≈ 0,15 × racines fraîches (ILLUSTRATION)",
                "gisement": "≈ 998 772 t/an",
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
                "techniques": "arrachage manuel ou mécanique, décorticage"
            },
            {
                "token": "CABOSSE_CACAO_CM",
                "famille": "Coques & noyaux",
                "nom_fr": "Cabosse de cacao",
                "region": "Ouest forestier et Littoral (Douala)",
                "lat": 5.5,
                "lon": 12.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "cabosses fendues et mucilage de cacao",
                "production": "fèves de cacao sèches : 320 000 t (FAOSTAT QCL 2024)",
                "ratio": "cabosse ≈ 8 × fèves sèches (ILLUSTRATION)",
                "gisement": "≈ 2,6 Mt/an",
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
                "token": "RESIDUS_MAIS_CM",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "Ouest forestier et Littoral (Douala)",
                "lat": 5.5,
                "lon": 12.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 2 200 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 550 000 t/an",
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
                "token": "RAFLES_PALMIER_CM",
                "famille": "Tropical",
                "nom_fr": "Rafles de palmier à huile",
                "region": "Ouest forestier et Littoral (Douala)",
                "lat": 5.5,
                "lon": 12.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "rafles vides et efflorescences du palmier à huile",
                "production": "régimes de palmier à huile : 2 947 380 t (FAOSTAT QCL 2024)",
                "ratio": "rafles ≈ 0,22 × régimes (ILLUSTRATION)",
                "gisement": "≈ 648 424 t/an",
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
    "Gabon": {
        "nom_fao": "Gabon",
        "portrait": "bassin Estuaire et forêts du Haut-Ogooué — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "RAFLES_PALMIER_GA",
                "famille": "Tropical",
                "nom_fr": "Rafles de palmier à huile",
                "region": "Estuaire et forêts du Haut-Ogooué",
                "lat": -0.5,
                "lon": 11.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "rafles vides et efflorescences du palmier à huile",
                "production": "régimes de palmier à huile : 607 941 t (FAOSTAT QCL 2024)",
                "ratio": "rafles ≈ 0,22 × régimes (ILLUSTRATION)",
                "gisement": "≈ 133 747 t/an",
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
                "token": "BAGASSE_CANNE_GA",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "Estuaire et forêts du Haut-Ogooué",
                "lat": -0.5,
                "lon": 11.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "sucre de canne centrifuge : 30 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 9 000 t/an",
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
            }
        ]
    },
    "Congo": {
        "nom_fao": "Congo, Rep.",
        "portrait": "bassin bassin du Niari (Brazzaville-Pointe-Noire) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "BAGASSE_CANNE_CG",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "bassin du Niari (Brazzaville-Pointe-Noire)",
                "lat": -1.0,
                "lon": 15.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "sucre de canne centrifuge : 70 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 21 000 t/an",
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
            }
        ]
    },
    "RDC": {
        "nom_fao": "Congo, The Democratic Republic Of The",
        "portrait": "bassin bassin du Kasaï et Haut-Katanga — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "ECORCES_MANIOC_CD",
                "famille": "Tropical",
                "nom_fr": "Écorces de manioc",
                "region": "bassin du Kasaï et Haut-Katanga",
                "lat": -2.5,
                "lon": 23.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "écorces et déchets de racines de manioc",
                "production": "manioc (racines fraîches) : 46 558 022 t (FAOSTAT QCL 2024)",
                "ratio": "écorces ≈ 0,15 × racines fraîches (ILLUSTRATION)",
                "gisement": "≈ 7,0 Mt/an",
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
                "techniques": "arrachage manuel ou mécanique, décorticage"
            },
            {
                "token": "RESIDUS_MAIS_CD",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "bassin du Kasaï et Haut-Katanga",
                "lat": -2.5,
                "lon": 23.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 2 250 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 562 500 t/an",
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
                "token": "RAFLES_PALMIER_CD",
                "famille": "Tropical",
                "nom_fr": "Rafles de palmier à huile",
                "region": "bassin du Kasaï et Haut-Katanga",
                "lat": -2.5,
                "lon": 23.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "rafles vides et efflorescences du palmier à huile",
                "production": "régimes de palmier à huile : 1 953 210 t (FAOSTAT QCL 2024)",
                "ratio": "rafles ≈ 0,22 × régimes (ILLUSTRATION)",
                "gisement": "≈ 429 706 t/an",
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
                "token": "COQUE_ARACHIDE_CD",
                "famille": "Coques & noyaux",
                "nom_fr": "Coques d'arachide",
                "region": "bassin du Kasaï et Haut-Katanga",
                "lat": -2.5,
                "lon": 23.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "coques d'arachides après décorticage",
                "production": "arachides en coque : 508 245 t (FAOSTAT QCL 2024)",
                "ratio": "coques ≈ 0,30 × arachides en coque (ILLUSTRATION)",
                "gisement": "≈ 152 474 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    4,
                    5
                ],
                "fenetre_note": "récolte de avril à mai, point sous garde",
                "techniques": "arrachage, séchage, décorticage mécanique"
            }
        ]
    },
    "Angola": {
        "nom_fao": "Angola",
        "portrait": "bassin plateau central (Huambo-Bié) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "ECORCES_MANIOC_AO",
                "famille": "Tropical",
                "nom_fr": "Écorces de manioc",
                "region": "plateau central (Huambo-Bié)",
                "lat": -12.5,
                "lon": 17.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "écorces et déchets de racines de manioc",
                "production": "manioc (racines fraîches) : 11 930 569 t (FAOSTAT QCL 2024)",
                "ratio": "écorces ≈ 0,15 × racines fraîches (ILLUSTRATION)",
                "gisement": "≈ 1,8 Mt/an",
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
                "techniques": "arrachage manuel ou mécanique, décorticage"
            },
            {
                "token": "RESIDUS_MAIS_AO",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "plateau central (Huambo-Bié)",
                "lat": -12.5,
                "lon": 17.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 2 950 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 737 500 t/an",
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
                "token": "BAGASSE_CANNE_AO",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "plateau central (Huambo-Bié)",
                "lat": -12.5,
                "lon": 17.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "sucre de canne centrifuge : 120 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 36 000 t/an",
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
                "token": "PAILLE_MIL_AO",
                "famille": "Céréales",
                "nom_fr": "Paille de mil",
                "region": "plateau central (Huambo-Bié)",
                "lat": -12.5,
                "lon": 17.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de mil",
                "production": "mil : 35 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 52 500 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    3,
                    4,
                    5
                ],
                "fenetre_note": "récolte de mars à mai, point sous garde",
                "techniques": "récolte manuelle, gerbes au champ"
            }
        ]
    },
    "Botswana": {
        "nom_fao": "Botswana",
        "portrait": "bassin veld du Sud-Est (Gaborone-Francistown) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_SORGHO_BW",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "veld du Sud-Est (Gaborone-Francistown)",
                "lat": -22.5,
                "lon": 24.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 5 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 7 500 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    3,
                    4,
                    5
                ],
                "fenetre_note": "récolte de mars à mai, point sous garde",
                "techniques": "récolte manuelle ou mécanisée, fanage au champ"
            },
            {
                "token": "PAILLE_MIL_BW",
                "famille": "Céréales",
                "nom_fr": "Paille de mil",
                "region": "veld du Sud-Est (Gaborone-Francistown)",
                "lat": -22.5,
                "lon": 24.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de mil",
                "production": "mil : 3 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 4 500 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    3,
                    4,
                    5
                ],
                "fenetre_note": "récolte de mars à mai, point sous garde",
                "techniques": "récolte manuelle, gerbes au champ"
            }
        ]
    },
    "Zimbabwe": {
        "nom_fao": "Zimbabwe",
        "portrait": "bassin Highveld céréalier (Harare-Bulawayo) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "RESIDUS_MAIS_ZW",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "Highveld céréalier (Harare-Bulawayo)",
                "lat": -19.0,
                "lon": 29.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 635 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 158 750 t/an",
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
                "token": "TIGE_COTON_ZW",
                "famille": "Céréales",
                "nom_fr": "Tiges de coton",
                "region": "Highveld céréalier (Harare-Bulawayo)",
                "lat": -19.0,
                "lon": 29.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et racines de cotonnier arrachées après récolte",
                "production": "coton brut (fibres) : 46 810 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "tiges ≈ 3 × coton brut (ILLUSTRATION)",
                "gisement": "≈ 140 431 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    3,
                    4,
                    5,
                    6
                ],
                "fenetre_note": "récolte de mars à juin, point sous garde",
                "techniques": "récolte mécanique ou manuelle, arrachage des tiges"
            },
            {
                "token": "PAILLE_SORGHO_ZW",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "Highveld céréalier (Harare-Bulawayo)",
                "lat": -19.0,
                "lon": 29.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 82 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 123 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    3,
                    4,
                    5
                ],
                "fenetre_note": "récolte de mars à mai, point sous garde",
                "techniques": "récolte manuelle ou mécanisée, fanage au champ"
            },
            {
                "token": "COQUE_ARACHIDE_ZW",
                "famille": "Coques & noyaux",
                "nom_fr": "Coques d'arachide",
                "region": "Highveld céréalier (Harare-Bulawayo)",
                "lat": -19.0,
                "lon": 29.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "coques d'arachides après décorticage",
                "production": "arachides décortiquées : 130 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "coques ≈ 0,42 × arachides décortiquées (ILLUSTRATION)",
                "gisement": "≈ 54 600 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    4,
                    5
                ],
                "fenetre_note": "récolte de avril à mai, point sous garde",
                "techniques": "arrachage, séchage, décorticage mécanique"
            }
        ]
    },
    "Zambie": {
        "nom_fao": "Zambia",
        "portrait": "bassin ceinture de maïs du plateau central (Lusaka) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "RESIDUS_MAIS_ZM",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "ceinture de maïs du plateau central (Lusaka)",
                "lat": -14.5,
                "lon": 27.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 1 510 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 377 500 t/an",
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
                "token": "ECORCES_MANIOC_ZM",
                "famille": "Tropical",
                "nom_fr": "Écorces de manioc",
                "region": "ceinture de maïs du plateau central (Lusaka)",
                "lat": -14.5,
                "lon": 27.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "écorces et déchets de racines de manioc",
                "production": "manioc (racines fraîches) : 3 127 778 t (FAOSTAT QCL 2024)",
                "ratio": "écorces ≈ 0,15 × racines fraîches (ILLUSTRATION)",
                "gisement": "≈ 469 167 t/an",
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
                "techniques": "arrachage manuel ou mécanique, décorticage"
            },
            {
                "token": "COQUE_ARACHIDE_ZM",
                "famille": "Coques & noyaux",
                "nom_fr": "Coques d'arachide",
                "region": "ceinture de maïs du plateau central (Lusaka)",
                "lat": -14.5,
                "lon": 27.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "coques d'arachides après décorticage",
                "production": "arachides décortiquées : 175 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "coques ≈ 0,42 × arachides décortiquées (ILLUSTRATION)",
                "gisement": "≈ 73 500 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    4,
                    5
                ],
                "fenetre_note": "récolte de avril à mai, point sous garde",
                "techniques": "arrachage, séchage, décorticage mécanique"
            },
            {
                "token": "PAILLE_SORGHO_ZM",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "ceinture de maïs du plateau central (Lusaka)",
                "lat": -14.5,
                "lon": 27.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 3 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 4 500 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    3,
                    4,
                    5
                ],
                "fenetre_note": "récolte de mars à mai, point sous garde",
                "techniques": "récolte manuelle ou mécanisée, fanage au champ"
            }
        ]
    },
    "Malawi": {
        "nom_fao": "Malawi",
        "portrait": "bassin vallée du Shire et Blantyre — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "ECORCES_MANIOC_MW",
                "famille": "Tropical",
                "nom_fr": "Écorces de manioc",
                "region": "vallée du Shire et Blantyre",
                "lat": -13.5,
                "lon": 34.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "écorces et déchets de racines de manioc",
                "production": "manioc (racines fraîches) : 6 278 880 t (FAOSTAT QCL 2024)",
                "ratio": "écorces ≈ 0,15 × racines fraîches (ILLUSTRATION)",
                "gisement": "≈ 941 832 t/an",
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
                "techniques": "arrachage manuel ou mécanique, décorticage"
            },
            {
                "token": "RESIDUS_MAIS_MW",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "vallée du Shire et Blantyre",
                "lat": -13.5,
                "lon": 34.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 2 900 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 725 000 t/an",
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
                "token": "COQUE_ARACHIDE_MW",
                "famille": "Coques & noyaux",
                "nom_fr": "Coques d'arachide",
                "region": "vallée du Shire et Blantyre",
                "lat": -13.5,
                "lon": 34.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "coques d'arachides après décorticage",
                "production": "arachides en coque : 350 000 t (FAOSTAT QCL 2024)",
                "ratio": "coques ≈ 0,30 × arachides en coque (ILLUSTRATION)",
                "gisement": "≈ 105 000 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    4,
                    5
                ],
                "fenetre_note": "récolte de avril à mai, point sous garde",
                "techniques": "arrachage, séchage, décorticage mécanique"
            }
        ]
    },
    "Mozambique": {
        "nom_fao": "Mozambique",
        "portrait": "bassin corridor de la Beira (Manica-Sofala) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "ECORCES_MANIOC_MZ",
                "famille": "Tropical",
                "nom_fr": "Écorces de manioc",
                "region": "corridor de la Beira (Manica-Sofala)",
                "lat": -17.5,
                "lon": 35.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "écorces et déchets de racines de manioc",
                "production": "manioc (racines fraîches) : 8 522 790 t (FAOSTAT QCL 2024)",
                "ratio": "écorces ≈ 0,15 × racines fraîches (ILLUSTRATION)",
                "gisement": "≈ 1,3 Mt/an",
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
                "techniques": "arrachage manuel ou mécanique, décorticage"
            },
            {
                "token": "BAGASSE_CANNE_MZ",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "corridor de la Beira (Manica-Sofala)",
                "lat": -17.5,
                "lon": 35.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "sucre de canne centrifuge : 455 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 136 500 t/an",
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
                "token": "RESIDUS_MAIS_MZ",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "corridor de la Beira (Manica-Sofala)",
                "lat": -17.5,
                "lon": 35.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 1 400 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 350 000 t/an",
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
                "token": "COQUE_ARACHIDE_MZ",
                "famille": "Coques & noyaux",
                "nom_fr": "Coques d'arachide",
                "region": "corridor de la Beira (Manica-Sofala)",
                "lat": -17.5,
                "lon": 35.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "coques d'arachides après décorticage",
                "production": "arachides décortiquées : 130 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "coques ≈ 0,42 × arachides décortiquées (ILLUSTRATION)",
                "gisement": "≈ 54 600 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    4,
                    5
                ],
                "fenetre_note": "récolte de avril à mai, point sous garde",
                "techniques": "arrachage, séchage, décorticage mécanique"
            }
        ]
    },
    "Tanzanie": {
        "nom_fao": "Tanzania, United Republic Of",
        "portrait": "bassin ceinture maïs du Sud (Mbeya-Iringa) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "ECORCES_MANIOC_TZ",
                "famille": "Tropical",
                "nom_fr": "Écorces de manioc",
                "region": "ceinture maïs du Sud (Mbeya-Iringa)",
                "lat": -6.5,
                "lon": 34.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "écorces et déchets de racines de manioc",
                "production": "manioc (racines fraîches) : 10 532 000 t (FAOSTAT QCL 2024)",
                "ratio": "écorces ≈ 0,15 × racines fraîches (ILLUSTRATION)",
                "gisement": "≈ 1,6 Mt/an",
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
                "techniques": "arrachage manuel ou mécanique, décorticage"
            },
            {
                "token": "RESIDUS_MAIS_TZ",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "ceinture maïs du Sud (Mbeya-Iringa)",
                "lat": -6.5,
                "lon": 34.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 10 084 000 t (FAOSTAT QCL 2024)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 2,5 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    2,
                    3,
                    4
                ],
                "fenetre_note": "récolte de février à avril, point sous garde",
                "techniques": "récolte en ensilage ou grain, andains au champ"
            },
            {
                "token": "BALLE_RIZ_TZ",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "ceinture maïs du Sud (Mbeya-Iringa)",
                "lat": -6.5,
                "lon": 34.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz paddy : 4 052 141 t (FAOSTAT QCL 2024)",
                "ratio": "balle ≈ 0,20 × riz paddy (ILLUSTRATION)",
                "gisement": "≈ 810 428 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    3,
                    4,
                    5
                ],
                "fenetre_note": "récolte de mars à mai, point sous garde",
                "techniques": "moisson, décorticage en rizerie"
            },
            {
                "token": "BAGASSE_CANNE_TZ",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "ceinture maïs du Sud (Mbeya-Iringa)",
                "lat": -6.5,
                "lon": 34.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "sucre de canne centrifuge : 385 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 115 500 t/an",
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
            }
        ]
    },
    "Ouganda": {
        "nom_fao": "Uganda",
        "portrait": "bassin bassin du lac Victoria (Jinja-Kampala) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "RESIDUS_MAIS_UG",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "bassin du lac Victoria (Jinja-Kampala)",
                "lat": 1.3,
                "lon": 32.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 5 000 000 t (FAOSTAT QCL 2024)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 1,2 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte en ensilage ou grain, andains au champ"
            },
            {
                "token": "BAGASSE_CANNE_UG",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "bassin du lac Victoria (Jinja-Kampala)",
                "lat": 1.3,
                "lon": 32.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "sucre de canne centrifuge : 500 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 150 000 t/an",
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
                "token": "BALLE_RIZ_UG",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "bassin du lac Victoria (Jinja-Kampala)",
                "lat": 1.3,
                "lon": 32.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz blanchi : 237 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 68 730 t/an",
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
                "token": "PARCHE_CAFE_UG",
                "famille": "Tropical",
                "nom_fr": "Parche et pulpe de café",
                "region": "bassin du lac Victoria (Jinja-Kampala)",
                "lat": 1.3,
                "lon": 32.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "parche, pulpe et mucilage de cerises de café",
                "production": "café vert : 402 000 t (FAOSTAT QCL 2024)",
                "ratio": "parche et pulpe ≈ 0,45 × café vert (ILLUSTRATION)",
                "gisement": "≈ 180 900 t/an",
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
            }
        ]
    },
    "Kenya": {
        "nom_fao": "Kenya",
        "portrait": "bassin highlands de l'Ouest (Nakuru-Eldoret) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "PARCHE_CAFE_KE",
                "famille": "Tropical",
                "nom_fr": "Parche et pulpe de café",
                "region": "highlands de l'Ouest (Nakuru-Eldoret)",
                "lat": 0.3,
                "lon": 37.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "parche, pulpe et mucilage de cerises de café",
                "production": "café vert : 49 500 t (FAOSTAT QCL 2024)",
                "ratio": "parche et pulpe ≈ 0,45 × café vert (ILLUSTRATION)",
                "gisement": "≈ 22 275 t/an",
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
                "token": "BAGASSE_CANNE_KE",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "highlands de l'Ouest (Nakuru-Eldoret)",
                "lat": 0.3,
                "lon": 37.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "canne à sucre : 9 365 300 t (FAOSTAT QCL 2024)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 2,8 Mt/an",
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
                "token": "RESIDUS_MAIS_KE",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "highlands de l'Ouest (Nakuru-Eldoret)",
                "lat": 0.3,
                "lon": 37.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 4 000 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 1,0 Mt/an",
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
                "token": "BALLE_RIZ_KE",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "highlands de l'Ouest (Nakuru-Eldoret)",
                "lat": 0.3,
                "lon": 37.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz blanchi : 180 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 52 200 t/an",
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
    "Rwanda": {
        "nom_fao": "Rwanda",
        "portrait": "bassin plateau central (Kigali-Butare) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "RESIDUS_MAIS_RW",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "plateau central (Kigali-Butare)",
                "lat": -1.9,
                "lon": 29.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 450 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 112 500 t/an",
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
                "token": "BALLE_RIZ_RW",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "plateau central (Kigali-Butare)",
                "lat": -1.9,
                "lon": 29.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz paddy : 135 075 t (tableau Wikipédia (FAOSTAT, année de l'article))",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 27 015 t/an",
                "etiquette_gisement": "SOURCÉ (production tableau Wikipédia (FAOSTAT, année de l'article)) + ratio ILLUSTRATION",
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
    "Éthiopie": {
        "nom_fao": "Ethiopia",
        "portrait": "bassin highlands éthiopiens (Bahre Dar-Gondar) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_SORGHO_ET",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "highlands éthiopiens (Bahre Dar-Gondar)",
                "lat": 9.0,
                "lon": 39.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 4 100 000 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 6,2 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle ou mécanisée, fanage au champ"
            },
            {
                "token": "PAILLE_MIL_ET",
                "famille": "Céréales",
                "nom_fr": "Paille de mil",
                "region": "highlands éthiopiens (Bahre Dar-Gondar)",
                "lat": 9.0,
                "lon": 39.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de mil",
                "production": "mil : 1 125 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 1,7 Mt/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle, gerbes au champ"
            },
            {
                "token": "RESIDUS_MAIS_ET",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "highlands éthiopiens (Bahre Dar-Gondar)",
                "lat": 9.0,
                "lon": 39.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 11 701 131 t (FAOSTAT QCL 2024)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 2,9 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte en ensilage ou grain, andains au champ"
            },
            {
                "token": "PARCHE_CAFE_ET",
                "famille": "Tropical",
                "nom_fr": "Parche et pulpe de café",
                "region": "highlands éthiopiens (Bahre Dar-Gondar)",
                "lat": 9.0,
                "lon": 39.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "parche, pulpe et mucilage de cerises de café",
                "production": "café vert : 575 696 t (FAOSTAT QCL 2024)",
                "ratio": "parche et pulpe ≈ 0,45 × café vert (ILLUSTRATION)",
                "gisement": "≈ 259 063 t/an",
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
                "token": "PAILLE_BLE_ET",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "highlands éthiopiens (Bahre Dar-Gondar)",
                "lat": 9.0,
                "lon": 39.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 6 185 341 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 7,4 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    6,
                    7,
                    8
                ],
                "fenetre_note": "récolte de juin à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes, fourrage prioritaire"
            }
        ]
    },
    "Somalie": {
        "nom_fao": "Somalia",
        "portrait": "bassin vallées du Juba et du Shebelle — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_SORGHO_SO",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "vallées du Juba et du Shebelle",
                "lat": 6.0,
                "lon": 45.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 100 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 150 000 t/an",
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
                "token": "RESIDUS_MAIS_SO",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "vallées du Juba et du Shebelle",
                "lat": 6.0,
                "lon": 45.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 75 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 18 750 t/an",
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
    "Soudan": {
        "nom_fao": "Sudan",
        "portrait": "bassin plaine de Gezira — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_SORGHO_SD",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "plaine de Gezira",
                "lat": 15.5,
                "lon": 32.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 5 393 620 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 8,1 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle ou mécanisée, fanage au champ"
            },
            {
                "token": "PAILLE_MIL_SD",
                "famille": "Céréales",
                "nom_fr": "Paille de mil",
                "region": "plaine de Gezira",
                "lat": 15.5,
                "lon": 32.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de mil",
                "production": "mil : 1 000 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 1,5 Mt/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle, gerbes au champ"
            },
            {
                "token": "NOYAU_DATTE_SD",
                "famille": "Coques & noyaux",
                "nom_fr": "Noyaux et rachis de dattes",
                "region": "plaine de Gezira",
                "lat": 15.5,
                "lon": 32.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "noyaux, rachis et écarts de tri des dattes",
                "production": "dattes : 443 134 t (FAOSTAT QCL 2024)",
                "ratio": "noyaux et rachis ≈ 0,12 × dattes (ILLUSTRATION)",
                "gisement": "≈ 53 176 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8,
                    9,
                    10
                ],
                "fenetre_note": "récolte de juillet à octobre, point sous garde",
                "techniques": "tri en station de conditionnement"
            },
            {
                "token": "COQUE_ARACHIDE_SD",
                "famille": "Coques & noyaux",
                "nom_fr": "Coques d'arachide",
                "region": "plaine de Gezira",
                "lat": 15.5,
                "lon": 32.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "coques d'arachides après décorticage",
                "production": "arachides en coque : 1 683 800 t (FAOSTAT QCL 2024)",
                "ratio": "coques ≈ 0,30 × arachides en coque (ILLUSTRATION)",
                "gisement": "≈ 505 140 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "arrachage, séchage, décorticage mécanique"
            },
            {
                "token": "PAILLE_BLE_SD",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "plaine de Gezira",
                "lat": 15.5,
                "lon": 32.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 400 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 480 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    6,
                    7,
                    8
                ],
                "fenetre_note": "récolte de juin à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes, fourrage prioritaire"
            }
        ]
    },
    "Madagascar": {
        "nom_fao": "Madagascar",
        "portrait": "bassin hauts plateaux rizicoles (Antananarivo-Antsirabe) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "BALLE_RIZ_MG",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "hauts plateaux rizicoles (Antananarivo-Antsirabe)",
                "lat": -18.9,
                "lon": 46.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz paddy : 4 970 000 t (FAOSTAT QCL 2024)",
                "ratio": "balle ≈ 0,20 × riz paddy (ILLUSTRATION)",
                "gisement": "≈ 994 000 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    3,
                    4,
                    5
                ],
                "fenetre_note": "récolte de mars à mai, point sous garde",
                "techniques": "moisson, décorticage en rizerie"
            },
            {
                "token": "ECORCES_MANIOC_MG",
                "famille": "Tropical",
                "nom_fr": "Écorces de manioc",
                "region": "hauts plateaux rizicoles (Antananarivo-Antsirabe)",
                "lat": -18.9,
                "lon": 46.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "écorces et déchets de racines de manioc",
                "production": "manioc (racines fraîches) : 2 573 531 t (FAOSTAT QCL 2024)",
                "ratio": "écorces ≈ 0,15 × racines fraîches (ILLUSTRATION)",
                "gisement": "≈ 386 030 t/an",
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
                "techniques": "arrachage manuel ou mécanique, décorticage"
            },
            {
                "token": "BAGASSE_CANNE_MG",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "hauts plateaux rizicoles (Antananarivo-Antsirabe)",
                "lat": -18.9,
                "lon": 46.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "sucre de canne centrifuge : 90 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 27 000 t/an",
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
                "token": "PARCHE_CAFE_MG",
                "famille": "Tropical",
                "nom_fr": "Parche et pulpe de café",
                "region": "hauts plateaux rizicoles (Antananarivo-Antsirabe)",
                "lat": -18.9,
                "lon": 46.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "parche, pulpe et mucilage de cerises de café",
                "production": "café vert : 49 561 t (FAOSTAT QCL 2024)",
                "ratio": "parche et pulpe ≈ 0,45 × café vert (ILLUSTRATION)",
                "gisement": "≈ 22 303 t/an",
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
            }
        ]
    },
    "Maurice": {
        "nom_fao": "Mauritius",
        "portrait": "bassin plaine du Nord de l'île — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "BAGASSE_CANNE_MU",
                "famille": "Tropical",
                "nom_fr": "Bagasse de canne à sucre",
                "region": "plaine du Nord de l'île",
                "lat": -20.2,
                "lon": 57.55,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "bagasse, paille de canne et écume de sucrerie",
                "production": "sucre de canne centrifuge : 245 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "bagasse ≈ 0,30 × canne à sucre (ILLUSTRATION)",
                "gisement": "≈ 73 500 t/an",
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
            }
        ]
    },
    "Guinée": {
        "nom_fao": "Guinea",
        "portrait": "bassin Fouta-Djalon et Basse-Côte — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "BALLE_RIZ_GN",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "Fouta-Djalon et Basse-Côte",
                "lat": 10.5,
                "lon": -11.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz paddy : 3 680 000 t (FAOSTAT QCL 2024)",
                "ratio": "balle ≈ 0,20 × riz paddy (ILLUSTRATION)",
                "gisement": "≈ 736 000 t/an",
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
                "token": "ECORCES_MANIOC_GN",
                "famille": "Tropical",
                "nom_fr": "Écorces de manioc",
                "region": "Fouta-Djalon et Basse-Côte",
                "lat": 10.5,
                "lon": -11.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "écorces et déchets de racines de manioc",
                "production": "manioc (racines fraîches) : 3 080 966 t (FAOSTAT QCL 2024)",
                "ratio": "écorces ≈ 0,15 × racines fraîches (ILLUSTRATION)",
                "gisement": "≈ 462 145 t/an",
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
                "techniques": "arrachage manuel ou mécanique, décorticage"
            },
            {
                "token": "RESIDUS_MAIS_GN",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "Fouta-Djalon et Basse-Côte",
                "lat": 10.5,
                "lon": -11.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 850 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 212 500 t/an",
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
                "token": "RAFLES_PALMIER_GN",
                "famille": "Tropical",
                "nom_fr": "Rafles de palmier à huile",
                "region": "Fouta-Djalon et Basse-Côte",
                "lat": 10.5,
                "lon": -11.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "rafles vides et efflorescences du palmier à huile",
                "production": "régimes de palmier à huile : 891 909 t (FAOSTAT QCL 2024)",
                "ratio": "rafles ≈ 0,22 × régimes (ILLUSTRATION)",
                "gisement": "≈ 196 220 t/an",
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
    "Sierra Leone": {
        "nom_fao": "Sierra Leone",
        "portrait": "bassin province du Nord (Makeni-Freetown) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "BALLE_RIZ_SL",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "province du Nord (Makeni-Freetown)",
                "lat": 8.7,
                "lon": -11.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz blanchi : 975 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 282 750 t/an",
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
                "token": "ECORCES_MANIOC_SL",
                "famille": "Tropical",
                "nom_fr": "Écorces de manioc",
                "region": "province du Nord (Makeni-Freetown)",
                "lat": 8.7,
                "lon": -11.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "écorces et déchets de racines de manioc",
                "production": "manioc (racines fraîches) : 2 855 436 t (FAOSTAT QCL 2024)",
                "ratio": "écorces ≈ 0,15 × racines fraîches (ILLUSTRATION)",
                "gisement": "≈ 428 315 t/an",
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
                "techniques": "arrachage manuel ou mécanique, décorticage"
            }
        ]
    },
    "Liberia": {
        "nom_fao": "Liberia",
        "portrait": "bassin comtés de Bong et Nimba — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "BALLE_RIZ_LR",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "comtés de Bong et Nimba",
                "lat": 6.8,
                "lon": -9.5,
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
            },
            {
                "token": "RAFLES_PALMIER_LR",
                "famille": "Tropical",
                "nom_fr": "Rafles de palmier à huile",
                "region": "comtés de Bong et Nimba",
                "lat": 6.8,
                "lon": -9.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "rafles vides et efflorescences du palmier à huile",
                "production": "huile de palme : 45 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "rafles ≈ 1,1 × huile (0,22 × régimes, régimes ≈ 5 × huile) (ILLUSTRATION)",
                "gisement": "≈ 49 500 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
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
    "Guinée-Bissau": {
        "nom_fao": "Guinea-Bissau",
        "portrait": "bassin régions de Biombo et Oio — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "BALLE_RIZ_GW",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "régions de Biombo et Oio",
                "lat": 12.0,
                "lon": -15.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz blanchi : 138 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 40 020 t/an",
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
    "Gambie": {
        "nom_fao": "Gambia, The",
        "portrait": "bassin bassin arachidier de Banjul — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "BALLE_RIZ_GM",
                "famille": "Céréales",
                "nom_fr": "Balle de riz",
                "region": "bassin arachidier de Banjul",
                "lat": 13.45,
                "lon": -16.6,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "balle de riz (coque), coproduit du décorticage",
                "production": "riz paddy : 44 597 t (tableau Wikipédia (FAOSTAT, année de l'article))",
                "ratio": "balle ≈ 0,29 × riz blanchi (0,20 × paddy, paddy ≈ 1,45 × blanchi) (ILLUSTRATION)",
                "gisement": "≈ 8 919 t/an",
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
    },
    "Burundi": {
        "nom_fao": "Burundi",
        "portrait": "bassin plateau central (Bujumbura-Gitega) — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "ECORCES_MANIOC_BI",
                "famille": "Tropical",
                "nom_fr": "Écorces de manioc",
                "region": "plateau central (Bujumbura-Gitega)",
                "lat": -3.3,
                "lon": 29.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "écorces et déchets de racines de manioc",
                "production": "manioc (racines fraîches) : 2 675 784 t (FAOSTAT QCL 2024)",
                "ratio": "écorces ≈ 0,15 × racines fraîches (ILLUSTRATION)",
                "gisement": "≈ 401 368 t/an",
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
                "techniques": "arrachage manuel ou mécanique, décorticage"
            },
            {
                "token": "RESIDUS_MAIS_BI",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "plateau central (Bujumbura-Gitega)",
                "lat": -3.3,
                "lon": 29.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 280 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 70 000 t/an",
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
                "token": "PAILLE_SORGHO_BI",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "plateau central (Bujumbura-Gitega)",
                "lat": -3.3,
                "lon": 29.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 30 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 45 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    3,
                    4,
                    5
                ],
                "fenetre_note": "récolte de mars à mai, point sous garde",
                "techniques": "récolte manuelle ou mécanisée, fanage au champ"
            }
        ]
    },
    "Soudan du Sud": {
        "nom_fao": "South Sudan",
        "portrait": "bassin Équatoria et Bahr el Ghazal — profil agricole à compléter (v1.7)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.7)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_SORGHO_SS",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "Équatoria et Bahr el Ghazal",
                "lat": 7.5,
                "lon": 31.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 960 000 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 1,4 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte manuelle ou mécanisée, fanage au champ"
            }
        ]
    }
}


def _index():
    idx = {}
    for pays, fiche in PAYS_AFRIQUE.items():
        for intrant in fiche["intrants"]:
            idx[intrant["token"]] = (pays, intrant)
    return idx


INDEX = _index()


def verifier_couverture():
    return set(INDEX) & (set(_master.ATLAS_BIOMASSES_MONDE) | set(_p11.INDEX)
                         | set(_v12.INDEX) | set(_v13.INDEX))


def sommaire():
    lignes = ["Atlas Afrique complète (v1.7) — %d pays, %d intrants" % (len(PAYS_AFRIQUE), len(INDEX))]
    for pays in sorted(PAYS_AFRIQUE, key=lambda p: p.lower()):
        lignes.append("  %s — %d intrant(s)" % (pays, len(PAYS_AFRIQUE[pays]["intrants"])))
    return "\n".join(lignes)


def fiche_token(token):
    if token not in INDEX:
        return None
    pays, intrant = INDEX[token]
    return {"pays": pays, "intrant": intrant}


def croisement():
    lignes = ["Pays couverts : %d" % len(PAYS_AFRIQUE)]
    lignes.append("Intrants : %d (attendu 136)" % len(INDEX))
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
