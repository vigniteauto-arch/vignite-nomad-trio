#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""World Twin v1.6 — Atlas des biomasses : Moyen-Orient complet.

Extension régionale de la lignée d'atlas (monde v1.0, pays v1.1, vignobles
v1.2, Asie v1.3) : pour les pays non encore couverts de cette région, les
biomasses LOCALES majeures sont placées sur le globe — région, point GPS
(Global Positioning System, approximation de bassin, jamais un cadastre),
type, volume, fenêtre saisonnière, techniques culturales — avec, par pays,
une synthèse réglementaire à cinq postes, tous À VÉRIFIER.

21 intrants, productions SOURCÉES (FAOSTAT QCL 2024 via Commodity
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
    python3 engine/atlas_moyen_orient.py                # sommaire par pays
    python3 engine/atlas_moyen_orient.py TOKEN          # fiche d'un intrant
    python3 engine/atlas_moyen_orient.py croisement     # contrôles complets
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
PAYS_MOYEN_ORIENT = {
    "Émirats arabes unis": {
        "nom_fao": "United Arab Emirates",
        "portrait": "bassin oasis d'Al-Aïn et fermes irriguées de Liwa — profil agricole à compléter (v1.6)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ]
        },
        "intrants": [
            {
                "token": "NOYAU_DATTE_AE",
                "famille": "Coques & noyaux",
                "nom_fr": "Noyaux et rachis de dattes",
                "region": "oasis d'Al-Aïn et fermes irriguées de Liwa",
                "lat": 24.3,
                "lon": 54.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "noyaux, rachis et écarts de tri des dattes",
                "production": "dattes : 333 632 t (FAOSTAT QCL 2024)",
                "ratio": "noyaux et rachis ≈ 0,12 × dattes (ILLUSTRATION)",
                "gisement": "≈ 40 036 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8,
                    9,
                    10
                ],
                "fenetre_note": "récolte de juillet à octobre, point sous garde",
                "techniques": "tri en station de conditionnement"
            }
        ]
    },
    "Qatar": {
        "nom_fao": "Qatar",
        "portrait": "bassin fermes du Nord (Al Khor) — profil agricole à compléter (v1.6)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ]
        },
        "intrants": [
            {
                "token": "NOYAU_DATTE_QA",
                "famille": "Coques & noyaux",
                "nom_fr": "Noyaux et rachis de dattes",
                "region": "fermes du Nord (Al Khor)",
                "lat": 25.3,
                "lon": 51.2,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "noyaux, rachis et écarts de tri des dattes",
                "production": "dattes : 35 318 t (FAOSTAT QCL 2024)",
                "ratio": "noyaux et rachis ≈ 0,12 × dattes (ILLUSTRATION)",
                "gisement": "≈ 4 238 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8,
                    9,
                    10
                ],
                "fenetre_note": "récolte de juillet à octobre, point sous garde",
                "techniques": "tri en station de conditionnement"
            }
        ]
    },
    "Koweït": {
        "nom_fao": "Kuwait",
        "portrait": "bassin fermes d'Abdali — profil agricole à compléter (v1.6)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ]
        },
        "intrants": [
            {
                "token": "NOYAU_DATTE_KW",
                "famille": "Coques & noyaux",
                "nom_fr": "Noyaux et rachis de dattes",
                "region": "fermes d'Abdali",
                "lat": 29.3,
                "lon": 47.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "noyaux, rachis et écarts de tri des dattes",
                "production": "dattes : 102 213 t (FAOSTAT QCL 2024)",
                "ratio": "noyaux et rachis ≈ 0,12 × dattes (ILLUSTRATION)",
                "gisement": "≈ 12 266 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8,
                    9,
                    10
                ],
                "fenetre_note": "récolte de juillet à octobre, point sous garde",
                "techniques": "tri en station de conditionnement"
            }
        ]
    },
    "Oman": {
        "nom_fao": "Oman",
        "portrait": "bassin Batinah et oasis de l'intérieur (Nizwa) — profil agricole à compléter (v1.6)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ]
        },
        "intrants": [
            {
                "token": "NOYAU_DATTE_OM",
                "famille": "Coques & noyaux",
                "nom_fr": "Noyaux et rachis de dattes",
                "region": "Batinah et oasis de l'intérieur (Nizwa)",
                "lat": 21.5,
                "lon": 57.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "noyaux, rachis et écarts de tri des dattes",
                "production": "dattes : 400 655 t (FAOSTAT QCL 2024)",
                "ratio": "noyaux et rachis ≈ 0,12 × dattes (ILLUSTRATION)",
                "gisement": "≈ 48 079 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8,
                    9,
                    10
                ],
                "fenetre_note": "récolte de juillet à octobre, point sous garde",
                "techniques": "tri en station de conditionnement"
            }
        ]
    },
    "Yémen": {
        "nom_fao": "Yemen, Rep.",
        "portrait": "bassin wadi Hadramawt et hauts plateaux — profil agricole à compléter (v1.6)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_SORGHO_YE",
                "famille": "Céréales",
                "nom_fr": "Paille de sorgho",
                "region": "wadi Hadramawt et hauts plateaux",
                "lat": 15.8,
                "lon": 47.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de sorgho",
                "production": "sorgho : 350 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 525 000 t/an",
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
                "token": "PAILLE_MIL_YE",
                "famille": "Céréales",
                "nom_fr": "Paille de mil",
                "region": "wadi Hadramawt et hauts plateaux",
                "lat": 15.8,
                "lon": 47.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et pailles de mil",
                "production": "mil : 60 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 90 000 t/an",
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
                "token": "PAILLE_BLE_YE",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "wadi Hadramawt et hauts plateaux",
                "lat": 15.8,
                "lon": 47.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 110 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 132 000 t/an",
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
                "token": "PARCHE_CAFE_YE",
                "famille": "Tropical",
                "nom_fr": "Parche et pulpe de café",
                "region": "wadi Hadramawt et hauts plateaux",
                "lat": 15.8,
                "lon": 47.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "parche, pulpe et mucilage de cerises de café",
                "production": "café vert : 30 291 t (tableau Wikipédia (FAOSTAT, année de l'article))",
                "ratio": "parche et pulpe ≈ 0,45 × café vert (ILLUSTRATION)",
                "gisement": "≈ 13 631 t/an",
                "etiquette_gisement": "SOURCÉ (production tableau Wikipédia (FAOSTAT, année de l'article)) + ratio ILLUSTRATION",
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
    "Liban": {
        "nom_fao": "Lebanon",
        "portrait": "bassin plaine de la Bekaa — profil agricole à compléter (v1.6)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_BLE_LB",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "plaine de la Bekaa",
                "lat": 33.9,
                "lon": 35.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 140 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 168 000 t/an",
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
                "token": "GRIGNONS_OLIVE_LB",
                "famille": "Coques & noyaux",
                "nom_fr": "Grignons d'olive",
                "region": "plaine de la Bekaa",
                "lat": 33.9,
                "lon": 35.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "grignons, noyaux et margines d'olives à huile",
                "production": "huile d'olive : 17 300 t (FAOSTAT QCL 2023)",
                "ratio": "grignons ≈ 1,75 × huile (olives ≈ 5 × huile, grignons ≈ 0,35 × olives) (ILLUSTRATION)",
                "gisement": "≈ 30 275 t/an",
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
                "token": "MARC_RAISIN_LB",
                "famille": "Cultures pérennes",
                "nom_fr": "Marc de raisin de table",
                "region": "plaine de la Bekaa",
                "lat": 33.9,
                "lon": 35.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "rafles, pépons et marc de raisin de table frais",
                "production": "raisin : 56 006 t (FAOSTAT 2024 (tableau Wikipédia))",
                "ratio": "marc ≈ 0,25 × raisin (ILLUSTRATION)",
                "gisement": "≈ 14 002 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT 2024 (tableau Wikipédia)) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10
                ],
                "fenetre_note": "récolte de septembre à octobre, point sous garde",
                "techniques": "récolte en frais, écarts de table"
            }
        ]
    },
    "Israël": {
        "nom_fao": "Israel",
        "portrait": "bassin plaine côtière et Néguev irrigué — profil agricole à compléter (v1.6)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_BLE_IL",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "plaine côtière et Néguev irrigué",
                "lat": 31.3,
                "lon": 34.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 120 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 144 000 t/an",
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
                "token": "TIGE_COTON_IL",
                "famille": "Céréales",
                "nom_fr": "Tiges de coton",
                "region": "plaine côtière et Néguev irrigué",
                "lat": 31.3,
                "lon": 34.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et racines de cotonnier arrachées après récolte",
                "production": "coton brut (fibres) : 8 709 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "tiges ≈ 3 × coton brut (ILLUSTRATION)",
                "gisement": "≈ 26 127 t/an",
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
                "token": "MARC_AGRUME_IL",
                "famille": "Cultures pérennes",
                "nom_fr": "Marc d'agrumes",
                "region": "plaine côtière et Néguev irrigué",
                "lat": 31.3,
                "lon": 34.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "écorces, pépins et marc d'oranges après pressage",
                "production": "oranges : 95 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "écorces et marc ≈ 0,50 × fruit (ILLUSTRATION)",
                "gisement": "≈ 47 500 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
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
                "token": "MARC_CITRON_IL",
                "famille": "Cultures pérennes",
                "nom_fr": "Marc de citrons et limes",
                "region": "plaine côtière et Néguev irrigué",
                "lat": 31.3,
                "lon": 34.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "écorces, pépins et marc de citrons et limes",
                "production": "citrons et limes : 62 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "écorces et marc ≈ 0,50 × fruit (ILLUSTRATION)",
                "gisement": "≈ 31 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    6,
                    7,
                    8,
                    9
                ],
                "fenetre_note": "récolte de juin à septembre, point sous garde",
                "techniques": "récolte, pressage, huilerie d'essence"
            },
            {
                "token": "NOYAU_DATTE_IL",
                "famille": "Coques & noyaux",
                "nom_fr": "Noyaux et rachis de dattes",
                "region": "plaine côtière et Néguev irrigué",
                "lat": 31.3,
                "lon": 34.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "noyaux, rachis et écarts de tri des dattes",
                "production": "dattes : 80 000 t (FAOSTAT QCL 2024)",
                "ratio": "noyaux et rachis ≈ 0,12 × dattes (ILLUSTRATION)",
                "gisement": "≈ 9 600 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8,
                    9,
                    10
                ],
                "fenetre_note": "récolte de juillet à octobre, point sous garde",
                "techniques": "tri en station de conditionnement"
            }
        ]
    },
    "Jordanie": {
        "nom_fao": "Jordan",
        "portrait": "bassin vallée du Jourdain (Zor) — profil agricole à compléter (v1.6)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ]
        },
        "intrants": [
            {
                "token": "GRIGNONS_OLIVE_JO",
                "famille": "Coques & noyaux",
                "nom_fr": "Grignons d'olive",
                "region": "vallée du Jourdain (Zor)",
                "lat": 31.3,
                "lon": 36.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "grignons, noyaux et margines d'olives à huile",
                "production": "huile d'olive : 25 028 t (FAOSTAT QCL 2023)",
                "ratio": "grignons ≈ 1,75 × huile (olives ≈ 5 × huile, grignons ≈ 0,35 × olives) (ILLUSTRATION)",
                "gisement": "≈ 43 799 t/an",
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
                "token": "NOYAU_DATTE_JO",
                "famille": "Coques & noyaux",
                "nom_fr": "Noyaux et rachis de dattes",
                "region": "vallée du Jourdain (Zor)",
                "lat": 31.3,
                "lon": 36.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "noyaux, rachis et écarts de tri des dattes",
                "production": "dattes : 32 618 t (FAOSTAT QCL 2024)",
                "ratio": "noyaux et rachis ≈ 0,12 × dattes (ILLUSTRATION)",
                "gisement": "≈ 3 914 t/an",
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
                "token": "PAILLE_BLE_JO",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "vallée du Jourdain (Zor)",
                "lat": 31.3,
                "lon": 36.9,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 32 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 38 400 t/an",
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
    "Chypre": {
        "nom_fao": "Cyprus",
        "portrait": "bassin plaine de la Mesaorie (Nicosie) — profil agricole à compléter (v1.6)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.6)"
            ]
        },
        "intrants": [
            {
                "token": "GRIGNONS_OLIVE_CY",
                "famille": "Coques & noyaux",
                "nom_fr": "Grignons d'olive",
                "region": "plaine de la Mesaorie (Nicosie)",
                "lat": 35.0,
                "lon": 33.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "grignons, noyaux et margines d'olives à huile",
                "production": "huile d'olive : 5 700 t (FAOSTAT QCL 2023)",
                "ratio": "grignons ≈ 1,75 × huile (olives ≈ 5 × huile, grignons ≈ 0,35 × olives) (ILLUSTRATION)",
                "gisement": "≈ 9 975 t/an",
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
                "token": "MARC_RAISIN_CY",
                "famille": "Cultures pérennes",
                "nom_fr": "Marc de raisin de table",
                "region": "plaine de la Mesaorie (Nicosie)",
                "lat": 35.0,
                "lon": 33.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "rafles, pépons et marc de raisin de table frais",
                "production": "raisin : 21 890 t (FAOSTAT 2024 (tableau Wikipédia))",
                "ratio": "marc ≈ 0,25 × raisin (ILLUSTRATION)",
                "gisement": "≈ 5 472 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT 2024 (tableau Wikipédia)) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10
                ],
                "fenetre_note": "récolte de septembre à octobre, point sous garde",
                "techniques": "récolte en frais, écarts de table"
            }
        ]
    }
}


def _index():
    idx = {}
    for pays, fiche in PAYS_MOYEN_ORIENT.items():
        for intrant in fiche["intrants"]:
            idx[intrant["token"]] = (pays, intrant)
    return idx


INDEX = _index()


def verifier_couverture():
    return set(INDEX) & (set(_master.ATLAS_BIOMASSES_MONDE) | set(_p11.INDEX)
                         | set(_v12.INDEX) | set(_v13.INDEX))


def sommaire():
    lignes = ["Atlas Moyen-Orient complet (v1.6) — %d pays, %d intrants" % (len(PAYS_MOYEN_ORIENT), len(INDEX))]
    for pays in sorted(PAYS_MOYEN_ORIENT, key=lambda p: p.lower()):
        lignes.append("  %s — %d intrant(s)" % (pays, len(PAYS_MOYEN_ORIENT[pays]["intrants"])))
    return "\n".join(lignes)


def fiche_token(token):
    if token not in INDEX:
        return None
    pays, intrant = INDEX[token]
    return {"pays": pays, "intrant": intrant}


def croisement():
    lignes = ["Pays couverts : %d" % len(PAYS_MOYEN_ORIENT)]
    lignes.append("Intrants : %d (attendu 21)" % len(INDEX))
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
