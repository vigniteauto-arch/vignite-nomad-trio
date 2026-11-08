#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""World Twin v1.4 — Atlas des biomasses : Europe du Nord et scieries.

Extension régionale de la lignée d'atlas (monde v1.0, pays v1.1, vignobles
v1.2, Asie v1.3) : pour les pays non encore couverts de cette région, les
biomasses LOCALES majeures sont placées sur le globe — région, point GPS
(Global Positioning System, approximation de bassin, jamais un cadastre),
type, volume, fenêtre saisonnière, techniques culturales — avec, par pays,
une synthèse réglementaire à cinq postes, tous À VÉRIFIER.

64 intrants, productions SOURCÉES (FAOSTAT QCL 2024 via Commodity
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
    python3 engine/atlas_europe_nord.py                # sommaire par pays
    python3 engine/atlas_europe_nord.py TOKEN          # fiche d'un intrant
    python3 engine/atlas_europe_nord.py croisement     # contrôles complets
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
PAYS_EUROPE_NORD = {
    "Suède": {
        "nom_fao": "Sweden",
        "portrait": "bassin plaines céréalières du Sud (Skåne-Uppland) — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "SCIURE_RESINEUX_SE",
                "famille": "Forestier",
                "nom_fr": "Sciure, copeaux et écorces de scierie",
                "region": "scieries du Norrland (Sundsvall-Timrå)",
                "lat": 62.5,
                "lon": 17.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "sciure, copeaux et écorces de résineux de scierie",
                "production": "abattages de bois rond industriels : 72 Mm³ (Nordic Forest Statistics 2026 : 140 Mm³ abattus en 2024 dans les pays nordiques)",
                "ratio": "sciure, copeaux et écorces ≈ 28 % du volume de grume usinée × 0,7 t/m³ (ILLUSTRATION)",
                "gisement": "≈ 14,1 Mt/an",
                "etiquette_gisement": "SOURCÉ (abattages Nordic Forest Statistics 2026 : 140 Mm³ abattus en 2024 dans les pays nordiques) + ratio ILLUSTRATION",
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
                "fenetre_note": "activité de scierie continue sur l'année, point sous garde",
                "techniques": "sciage de grumes résineuses, écorceuse, rabotage"
            },
            {
                "token": "PAILLE_BLE_SE",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "plaines céréalières du Sud (Skåne-Uppland)",
                "lat": 59.8,
                "lon": 15.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 2 300 000 t (FAOSTAT 2024 (tableau Wikipédia))",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 2,8 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT 2024 (tableau Wikipédia)) + ratio ILLUSTRATION",
                "fenetre": [
                    6,
                    7,
                    8
                ],
                "fenetre_note": "récolte de juin à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes, fourrage prioritaire"
            },
            {
                "token": "PAILLE_ORGE_SE",
                "famille": "Céréales",
                "nom_fr": "Paille d'orge",
                "region": "plaines céréalières du Sud (Skåne-Uppland)",
                "lat": 59.8,
                "lon": 15.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'orge, chaumes et glumes",
                "production": "orge : 1 263 900 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 1,3 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            },
            {
                "token": "RESIDUS_COLZA_SE",
                "famille": "Céréales",
                "nom_fr": "Résidus de colza",
                "region": "plaines céréalières du Sud (Skåne-Uppland)",
                "lat": 59.8,
                "lon": 15.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "pailles et cosses de colza",
                "production": "colza (graines) : 283 600 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 2,5 × graines (ILLUSTRATION)",
                "gisement": "≈ 709 000 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson, battage, andains de cosses"
            }
        ]
    },
    "Finlande": {
        "nom_fao": "Finland",
        "portrait": "bassin bassin céréalier de l'Ostrobotnie du Sud — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "SCIURE_RESINEUX_FI",
                "famille": "Forestier",
                "nom_fr": "Sciure, copeaux et écorces de scierie",
                "region": "scieries de l'Ouest (Vaasa-Seinäjoki)",
                "lat": 63.6,
                "lon": 23.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "sciure, copeaux et écorces de résineux de scierie",
                "production": "abattages de bois rond industriels : 63 Mm³ (Luke 2025 : 74,3 Mm³ abattus en Finlande en 2025, dont ~85 % industriels)",
                "ratio": "sciure, copeaux et écorces ≈ 28 % du volume de grume usinée × 0,7 t/m³ (ILLUSTRATION)",
                "gisement": "≈ 12,3 Mt/an",
                "etiquette_gisement": "SOURCÉ (abattages Luke 2025 : 74,3 Mm³ abattus en Finlande en 2025, dont ~85 % industriels) + ratio ILLUSTRATION",
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
                "fenetre_note": "activité de scierie continue sur l'année, point sous garde",
                "techniques": "sciage de grumes résineuses, écorceuse, rabotage"
            },
            {
                "token": "PAILLE_ORGE_FI",
                "famille": "Céréales",
                "nom_fr": "Paille d'orge",
                "region": "bassin céréalier de l'Ostrobotnie du Sud",
                "lat": 61.8,
                "lon": 25.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'orge, chaumes et glumes",
                "production": "orge : 1 178 950 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 1,2 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            },
            {
                "token": "PAILLE_AVOINE_FI",
                "famille": "Céréales",
                "nom_fr": "Paille d'avoine",
                "region": "bassin céréalier de l'Ostrobotnie du Sud",
                "lat": 61.8,
                "lon": 25.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'avoine, chaumes et glumes",
                "production": "avoine : 1 221 540 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 1,2 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8,
                    9
                ],
                "fenetre_note": "récolte de juillet à septembre, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            }
        ]
    },
    "Norvège": {
        "nom_fao": "Norway",
        "portrait": "bassin céréales du Trøndelag — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "SCIURE_RESINEUX_NO",
                "famille": "Forestier",
                "nom_fr": "Sciure, copeaux et écorces de scierie",
                "region": "scieries du Viken (Est de la Norvège)",
                "lat": 60.0,
                "lon": 10.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "sciure, copeaux et écorces de résineux de scierie",
                "production": "abattages de bois rond industriels : 12 Mm³ (Nordic Forest Statistics 2026)",
                "ratio": "sciure, copeaux et écorces ≈ 28 % du volume de grume usinée × 0,7 t/m³ (ILLUSTRATION)",
                "gisement": "≈ 2,4 Mt/an",
                "etiquette_gisement": "SOURCÉ (abattages Nordic Forest Statistics 2026) + ratio ILLUSTRATION",
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
                "fenetre_note": "activité de scierie continue sur l'année, point sous garde",
                "techniques": "sciage de grumes résineuses, écorceuse, rabotage"
            },
            {
                "token": "PAILLE_ORGE_NO",
                "famille": "Céréales",
                "nom_fr": "Paille d'orge",
                "region": "céréales du Trøndelag",
                "lat": 60.8,
                "lon": 9.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'orge, chaumes et glumes",
                "production": "orge : 600 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 600 000 t/an",
                "etiquette_gisement": "SOURCÉ (production campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            },
            {
                "token": "PAILLE_AVOINE_NO",
                "famille": "Céréales",
                "nom_fr": "Paille d'avoine",
                "region": "céréales du Trøndelag",
                "lat": 60.8,
                "lon": 9.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'avoine, chaumes et glumes",
                "production": "avoine : 283 000 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 283 000 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8,
                    9
                ],
                "fenetre_note": "récolte de juillet à septembre, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            },
            {
                "token": "PAILLE_BLE_NO",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "céréales du Trøndelag",
                "lat": 60.8,
                "lon": 9.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 420 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 504 000 t/an",
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
    "Danemark": {
        "nom_fao": "Denmark",
        "portrait": "bassin Jutland céréalier — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_BLE_DK",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "Jutland céréalier",
                "lat": 56.2,
                "lon": 9.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 5 900 000 t (FAOSTAT 2024 (tableau Wikipédia))",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 7,1 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT 2024 (tableau Wikipédia)) + ratio ILLUSTRATION",
                "fenetre": [
                    6,
                    7,
                    8
                ],
                "fenetre_note": "récolte de juin à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes, fourrage prioritaire"
            },
            {
                "token": "PAILLE_ORGE_DK",
                "famille": "Céréales",
                "nom_fr": "Paille d'orge",
                "region": "Jutland céréalier",
                "lat": 56.2,
                "lon": 9.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'orge, chaumes et glumes",
                "production": "orge : 3 141 150 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 3,1 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            },
            {
                "token": "RESIDUS_COLZA_DK",
                "famille": "Céréales",
                "nom_fr": "Résidus de colza",
                "region": "Jutland céréalier",
                "lat": 56.2,
                "lon": 9.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "pailles et cosses de colza",
                "production": "colza (graines) : 696 900 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 2,5 × graines (ILLUSTRATION)",
                "gisement": "≈ 1,7 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson, battage, andains de cosses"
            }
        ]
    },
    "Estonie": {
        "nom_fao": "Estonia",
        "portrait": "bassin plaines de l'Ouest (Harju-Tartu) — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "SCIURE_RESINEUX_EE",
                "famille": "Forestier",
                "nom_fr": "Sciure, copeaux et écorces de scierie",
                "region": "scieries du Sud (Tartu)",
                "lat": 58.9,
                "lon": 24.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "sciure, copeaux et écorces de résineux de scierie",
                "production": "abattages de bois rond industriels : 3.5 Mm³ (FAOSTAT 2024 (bois rond))",
                "ratio": "sciure, copeaux et écorces ≈ 28 % du volume de grume usinée × 0,7 t/m³ (ILLUSTRATION)",
                "gisement": "≈ 686 000 t/an",
                "etiquette_gisement": "SOURCÉ (abattages FAOSTAT 2024 (bois rond)) + ratio ILLUSTRATION",
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
                "fenetre_note": "activité de scierie continue sur l'année, point sous garde",
                "techniques": "sciage de grumes résineuses, écorceuse, rabotage"
            },
            {
                "token": "PAILLE_ORGE_EE",
                "famille": "Céréales",
                "nom_fr": "Paille d'orge",
                "region": "plaines de l'Ouest (Harju-Tartu)",
                "lat": 58.7,
                "lon": 25.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'orge, chaumes et glumes",
                "production": "orge : 488 820 t (tableau Wikipédia (FAOSTAT, année de l'article))",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 488 820 t/an",
                "etiquette_gisement": "SOURCÉ (production tableau Wikipédia (FAOSTAT, année de l'article)) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            }
        ]
    },
    "Lettonie": {
        "nom_fao": "Latvia",
        "portrait": "bassin Zemgale céréalière (Jelgava) — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "SCIURE_RESINEUX_LV",
                "famille": "Forestier",
                "nom_fr": "Sciure, copeaux et écorces de scierie",
                "region": "scieries de Liepāja",
                "lat": 56.8,
                "lon": 26.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "sciure, copeaux et écorces de résineux de scierie",
                "production": "abattages de bois rond industriels : 4 Mm³ (FAOSTAT 2024 (bois rond))",
                "ratio": "sciure, copeaux et écorces ≈ 28 % du volume de grume usinée × 0,7 t/m³ (ILLUSTRATION)",
                "gisement": "≈ 784 000 t/an",
                "etiquette_gisement": "SOURCÉ (abattages FAOSTAT 2024 (bois rond)) + ratio ILLUSTRATION",
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
                "fenetre_note": "activité de scierie continue sur l'année, point sous garde",
                "techniques": "sciage de grumes résineuses, écorceuse, rabotage"
            },
            {
                "token": "PAILLE_BLE_LV",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "Zemgale céréalière (Jelgava)",
                "lat": 56.9,
                "lon": 24.6,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 1 000 000 t (FAOSTAT 2024 (tableau Wikipédia))",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 1,2 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT 2024 (tableau Wikipédia)) + ratio ILLUSTRATION",
                "fenetre": [
                    6,
                    7,
                    8
                ],
                "fenetre_note": "récolte de juin à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes, fourrage prioritaire"
            },
            {
                "token": "PAILLE_ORGE_LV",
                "famille": "Céréales",
                "nom_fr": "Paille d'orge",
                "region": "Zemgale céréalière (Jelgava)",
                "lat": 56.9,
                "lon": 24.6,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'orge, chaumes et glumes",
                "production": "orge : 281 600 t (tableau Wikipédia (FAOSTAT, année de l'article))",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 281 600 t/an",
                "etiquette_gisement": "SOURCÉ (production tableau Wikipédia (FAOSTAT, année de l'article)) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            }
        ]
    },
    "Lituanie": {
        "nom_fao": "Lithuania",
        "portrait": "bassin Suvalkija céréalière (Marijampolė) — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "SCIURE_RESINEUX_LT",
                "famille": "Forestier",
                "nom_fr": "Sciure, copeaux et écorces de scierie",
                "region": "scieries de Klaipėda",
                "lat": 55.3,
                "lon": 24.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "sciure, copeaux et écorces de résineux de scierie",
                "production": "abattages de bois rond industriels : 4.5 Mm³ (FAOSTAT 2024 (bois rond))",
                "ratio": "sciure, copeaux et écorces ≈ 28 % du volume de grume usinée × 0,7 t/m³ (ILLUSTRATION)",
                "gisement": "≈ 882 000 t/an",
                "etiquette_gisement": "SOURCÉ (abattages FAOSTAT 2024 (bois rond)) + ratio ILLUSTRATION",
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
                "fenetre_note": "activité de scierie continue sur l'année, point sous garde",
                "techniques": "sciage de grumes résineuses, écorceuse, rabotage"
            },
            {
                "token": "PAILLE_BLE_LT",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "Suvalkija céréalière (Marijampolė)",
                "lat": 55.5,
                "lon": 23.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 2 100 000 t (FAOSTAT 2024 (tableau Wikipédia))",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 2,5 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT 2024 (tableau Wikipédia)) + ratio ILLUSTRATION",
                "fenetre": [
                    6,
                    7,
                    8
                ],
                "fenetre_note": "récolte de juin à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes, fourrage prioritaire"
            },
            {
                "token": "RESIDUS_COLZA_LT",
                "famille": "Céréales",
                "nom_fr": "Résidus de colza",
                "region": "Suvalkija céréalière (Marijampolė)",
                "lat": 55.5,
                "lon": 23.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "pailles et cosses de colza",
                "production": "colza (graines) : 868 000 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 2,5 × graines (ILLUSTRATION)",
                "gisement": "≈ 2,2 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson, battage, andains de cosses"
            },
            {
                "token": "PAILLE_ORGE_LT",
                "famille": "Céréales",
                "nom_fr": "Paille d'orge",
                "region": "Suvalkija céréalière (Marijampolė)",
                "lat": 55.5,
                "lon": 23.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'orge, chaumes et glumes",
                "production": "orge : 522 000 t (tableau Wikipédia (FAOSTAT, année de l'article))",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 522 000 t/an",
                "etiquette_gisement": "SOURCÉ (production tableau Wikipédia (FAOSTAT, année de l'article)) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            }
        ]
    },
    "Pologne": {
        "nom_fao": "Poland",
        "portrait": "bassin grande plaine centrale (Mazovie) — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "SCIURE_RESINEUX_PL",
                "famille": "Forestier",
                "nom_fr": "Sciure, copeaux et écorces de scierie",
                "region": "scieries de Poméranie (Gdańsk)",
                "lat": 53.6,
                "lon": 18.6,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "sciure, copeaux et écorces de résineux de scierie",
                "production": "abattages de bois rond industriels : 42 Mm³ (FAOSTAT 2024 (bois rond))",
                "ratio": "sciure, copeaux et écorces ≈ 28 % du volume de grume usinée × 0,7 t/m³ (ILLUSTRATION)",
                "gisement": "≈ 8,2 Mt/an",
                "etiquette_gisement": "SOURCÉ (abattages FAOSTAT 2024 (bois rond)) + ratio ILLUSTRATION",
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
                "fenetre_note": "activité de scierie continue sur l'année, point sous garde",
                "techniques": "sciage de grumes résineuses, écorceuse, rabotage"
            },
            {
                "token": "PAILLE_BLE_PL",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "grande plaine centrale (Mazovie)",
                "lat": 52.2,
                "lon": 19.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 12 183 620 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 14,6 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    6,
                    7,
                    8
                ],
                "fenetre_note": "récolte de juin à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes, fourrage prioritaire"
            },
            {
                "token": "RESIDUS_COLZA_PL",
                "famille": "Céréales",
                "nom_fr": "Résidus de colza",
                "region": "grande plaine centrale (Mazovie)",
                "lat": 52.2,
                "lon": 19.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "pailles et cosses de colza",
                "production": "colza (graines) : 3 124 180 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 2,5 × graines (ILLUSTRATION)",
                "gisement": "≈ 7,8 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson, battage, andains de cosses"
            },
            {
                "token": "RESIDUS_MAIS_PL",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "grande plaine centrale (Mazovie)",
                "lat": 52.2,
                "lon": 19.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 9 223 230 t (FAOSTAT QCL 2024)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 2,3 Mt/an",
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
                "token": "PAILLE_ORGE_PL",
                "famille": "Céréales",
                "nom_fr": "Paille d'orge",
                "region": "grande plaine centrale (Mazovie)",
                "lat": 52.2,
                "lon": 19.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'orge, chaumes et glumes",
                "production": "orge : 2 960 050 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 3,0 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            }
        ]
    },
    "Irlande": {
        "nom_fao": "Ireland",
        "portrait": "bassin bassin céréalier du Sud-Est (Meath-Wexford) — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_ORGE_IE",
                "famille": "Céréales",
                "nom_fr": "Paille d'orge",
                "region": "bassin céréalier du Sud-Est (Meath-Wexford)",
                "lat": 53.3,
                "lon": -8.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'orge, chaumes et glumes",
                "production": "orge : 1 282 050 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 1,3 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            },
            {
                "token": "PAILLE_AVOINE_IE",
                "famille": "Céréales",
                "nom_fr": "Paille d'avoine",
                "region": "bassin céréalier du Sud-Est (Meath-Wexford)",
                "lat": 53.3,
                "lon": -8.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'avoine, chaumes et glumes",
                "production": "avoine : 226 020 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 226 020 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8,
                    9
                ],
                "fenetre_note": "récolte de juillet à septembre, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            }
        ]
    },
    "Royaume-Uni": {
        "nom_fao": "United Kingdom",
        "portrait": "bassin East Anglia céréalière — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "SCIURE_RESINEUX_GB",
                "famille": "Forestier",
                "nom_fr": "Sciure, copeaux et écorces de scierie",
                "region": "scieries d'Écosse (Inverness)",
                "lat": 57.2,
                "lon": -3.8,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "sciure, copeaux et écorces de résineux de scierie",
                "production": "abattages de bois rond industriels : 10 Mm³ (FAOSTAT 2024 (bois rond))",
                "ratio": "sciure, copeaux et écorces ≈ 28 % du volume de grume usinée × 0,7 t/m³ (ILLUSTRATION)",
                "gisement": "≈ 2,0 Mt/an",
                "etiquette_gisement": "SOURCÉ (abattages FAOSTAT 2024 (bois rond)) + ratio ILLUSTRATION",
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
                "fenetre_note": "activité de scierie continue sur l'année, point sous garde",
                "techniques": "sciage de grumes résineuses, écorceuse, rabotage"
            },
            {
                "token": "PAILLE_BLE_GB",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "East Anglia céréalière",
                "lat": 52.8,
                "lon": -1.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 11 146 000 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 13,4 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    6,
                    7,
                    8
                ],
                "fenetre_note": "récolte de juin à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes, fourrage prioritaire"
            },
            {
                "token": "PAILLE_ORGE_GB",
                "famille": "Céréales",
                "nom_fr": "Paille d'orge",
                "region": "East Anglia céréalière",
                "lat": 52.8,
                "lon": -1.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'orge, chaumes et glumes",
                "production": "orge : 7 091 000 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 7,1 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            },
            {
                "token": "RESIDUS_COLZA_GB",
                "famille": "Céréales",
                "nom_fr": "Résidus de colza",
                "region": "East Anglia céréalière",
                "lat": 52.8,
                "lon": -1.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "pailles et cosses de colza",
                "production": "colza (graines) : 823 605 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 2,5 × graines (ILLUSTRATION)",
                "gisement": "≈ 2,1 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson, battage, andains de cosses"
            },
            {
                "token": "PAILLE_AVOINE_GB",
                "famille": "Céréales",
                "nom_fr": "Paille d'avoine",
                "region": "East Anglia céréalière",
                "lat": 52.8,
                "lon": -1.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'avoine, chaumes et glumes",
                "production": "avoine : 986 000 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 986 000 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8,
                    9
                ],
                "fenetre_note": "récolte de juillet à septembre, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            }
        ]
    },
    "Pays-Bas": {
        "nom_fao": "Netherlands",
        "portrait": "bassin polders céréaliers de Flevoland — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_ORGE_NL",
                "famille": "Céréales",
                "nom_fr": "Paille d'orge",
                "region": "polders céréaliers de Flevoland",
                "lat": 52.2,
                "lon": 5.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'orge, chaumes et glumes",
                "production": "orge : 283 230 t (tableau Wikipédia (FAOSTAT, année de l'article))",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 283 230 t/an",
                "etiquette_gisement": "SOURCÉ (production tableau Wikipédia (FAOSTAT, année de l'article)) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            }
        ]
    },
    "Belgique": {
        "nom_fao": "Belgium",
        "portrait": "bassin limon céréalier de Hesbaye — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_ORGE_BE",
                "famille": "Céréales",
                "nom_fr": "Paille d'orge",
                "region": "limon céréalier de Hesbaye",
                "lat": 50.6,
                "lon": 4.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'orge, chaumes et glumes",
                "production": "orge : 373 000 t (tableau Wikipédia (FAOSTAT, année de l'article))",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 373 000 t/an",
                "etiquette_gisement": "SOURCÉ (production tableau Wikipédia (FAOSTAT, année de l'article)) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            }
        ]
    },
    "Tchéquie": {
        "nom_fao": "Czechia",
        "portrait": "bassin plaine de Haná (Olomouc) — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "SCIURE_RESINEUX_CZ",
                "famille": "Forestier",
                "nom_fr": "Sciure, copeaux et écorces de scierie",
                "region": "scieries de Moravie (Olomouc)",
                "lat": 49.2,
                "lon": 17.7,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "sciure, copeaux et écorces de résineux de scierie",
                "production": "abattages de bois rond industriels : 20 Mm³ (FAOSTAT 2024 (bois rond))",
                "ratio": "sciure, copeaux et écorces ≈ 28 % du volume de grume usinée × 0,7 t/m³ (ILLUSTRATION)",
                "gisement": "≈ 3,9 Mt/an",
                "etiquette_gisement": "SOURCÉ (abattages FAOSTAT 2024 (bois rond)) + ratio ILLUSTRATION",
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
                "fenetre_note": "activité de scierie continue sur l'année, point sous garde",
                "techniques": "sciage de grumes résineuses, écorceuse, rabotage"
            },
            {
                "token": "PAILLE_BLE_CZ",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "plaine de Haná (Olomouc)",
                "lat": 49.8,
                "lon": 15.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 4 400 000 t (FAOSTAT 2024 (tableau Wikipédia))",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 5,3 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT 2024 (tableau Wikipédia)) + ratio ILLUSTRATION",
                "fenetre": [
                    6,
                    7,
                    8
                ],
                "fenetre_note": "récolte de juin à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes, fourrage prioritaire"
            },
            {
                "token": "PAILLE_ORGE_CZ",
                "famille": "Céréales",
                "nom_fr": "Paille d'orge",
                "region": "plaine de Haná (Olomouc)",
                "lat": 49.8,
                "lon": 15.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'orge, chaumes et glumes",
                "production": "orge : 1 671 530 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 1,7 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            },
            {
                "token": "RESIDUS_COLZA_CZ",
                "famille": "Céréales",
                "nom_fr": "Résidus de colza",
                "region": "plaine de Haná (Olomouc)",
                "lat": 49.8,
                "lon": 15.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "pailles et cosses de colza",
                "production": "colza (graines) : 946 890 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 2,5 × graines (ILLUSTRATION)",
                "gisement": "≈ 2,4 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson, battage, andains de cosses"
            }
        ]
    },
    "Autriche": {
        "nom_fao": "Austria",
        "portrait": "bassin Weinviertel et Basse-Autriche céréalière — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "SCIURE_RESINEUX_AT",
                "famille": "Forestier",
                "nom_fr": "Sciure, copeaux et écorces de scierie",
                "region": "scieries de Styrie (Graz)",
                "lat": 47.5,
                "lon": 15.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "sciure, copeaux et écorces de résineux de scierie",
                "production": "abattages de bois rond industriels : 18 Mm³ (FAOSTAT 2024 (bois rond))",
                "ratio": "sciure, copeaux et écorces ≈ 28 % du volume de grume usinée × 0,7 t/m³ (ILLUSTRATION)",
                "gisement": "≈ 3,5 Mt/an",
                "etiquette_gisement": "SOURCÉ (abattages FAOSTAT 2024 (bois rond)) + ratio ILLUSTRATION",
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
                "fenetre_note": "activité de scierie continue sur l'année, point sous garde",
                "techniques": "sciage de grumes résineuses, écorceuse, rabotage"
            },
            {
                "token": "PAILLE_ORGE_AT",
                "famille": "Céréales",
                "nom_fr": "Paille d'orge",
                "region": "Weinviertel et Basse-Autriche céréalière",
                "lat": 47.7,
                "lon": 14.2,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'orge, chaumes et glumes",
                "production": "orge : 767 120 t (tableau Wikipédia (FAOSTAT, année de l'article))",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 767 120 t/an",
                "etiquette_gisement": "SOURCÉ (production tableau Wikipédia (FAOSTAT, année de l'article)) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            }
        ]
    },
    "Ukraine": {
        "nom_fao": "Ukraine",
        "portrait": "bassin ceinture noire centrale (Tcherkassy-Vinnytsia) — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "SCIURE_RESINEUX_UA",
                "famille": "Forestier",
                "nom_fr": "Sciure, copeaux et écorces de scierie",
                "region": "scieries des Carpates (Ivano-Frankivsk)",
                "lat": 48.6,
                "lon": 24.7,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "sciure, copeaux et écorces de résineux de scierie",
                "production": "abattages de bois rond industriels : 15 Mm³ (FAOSTAT 2024 (bois rond))",
                "ratio": "sciure, copeaux et écorces ≈ 28 % du volume de grume usinée × 0,7 t/m³ (ILLUSTRATION)",
                "gisement": "≈ 2,9 Mt/an",
                "etiquette_gisement": "SOURCÉ (abattages FAOSTAT 2024 (bois rond)) + ratio ILLUSTRATION",
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
                "fenetre_note": "activité de scierie continue sur l'année, point sous garde",
                "techniques": "sciage de grumes résineuses, écorceuse, rabotage"
            },
            {
                "token": "PAILLE_BLE_UA",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "ceinture noire centrale (Tcherkassy-Vinnytsia)",
                "lat": 49.5,
                "lon": 31.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 22 441 110 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 26,9 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    6,
                    7,
                    8
                ],
                "fenetre_note": "récolte de juin à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes, fourrage prioritaire"
            },
            {
                "token": "RESIDUS_MAIS_UA",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "ceinture noire centrale (Tcherkassy-Vinnytsia)",
                "lat": 49.5,
                "lon": 31.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 26 863 740 t (FAOSTAT QCL 2024)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 6,7 Mt/an",
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
                "token": "TIGE_TOURNESOL_UA",
                "famille": "Céréales",
                "nom_fr": "Tiges de tournesol",
                "region": "ceinture noire centrale (Tcherkassy-Vinnytsia)",
                "lat": 49.5,
                "lon": 31.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et capitules de tournesol",
                "production": "tournesol (graines) : 10 955 940 t (FAOSTAT QCL 2024)",
                "ratio": "tiges ≈ 2 × graines (ILLUSTRATION)",
                "gisement": "≈ 21,9 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    8,
                    9,
                    10
                ],
                "fenetre_note": "récolte de août à octobre, point sous garde",
                "techniques": "récolte des capitules, broyage des tiges"
            },
            {
                "token": "RESIDUS_COLZA_UA",
                "famille": "Céréales",
                "nom_fr": "Résidus de colza",
                "region": "ceinture noire centrale (Tcherkassy-Vinnytsia)",
                "lat": 49.5,
                "lon": 31.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "pailles et cosses de colza",
                "production": "colza (graines) : 3 591 300 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 2,5 × graines (ILLUSTRATION)",
                "gisement": "≈ 9,0 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson, battage, andains de cosses"
            }
        ]
    },
    "Biélorussie": {
        "nom_fao": "Belarus",
        "portrait": "bassin plaine centrale (Minsk-Gomel) — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "SCIURE_RESINEUX_BY",
                "famille": "Forestier",
                "nom_fr": "Sciure, copeaux et écorces de scierie",
                "region": "scieries de la Bérézina (Barysaw)",
                "lat": 53.0,
                "lon": 27.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "sciure, copeaux et écorces de résineux de scierie",
                "production": "abattages de bois rond industriels : 12 Mm³ (FAOSTAT 2024 (bois rond))",
                "ratio": "sciure, copeaux et écorces ≈ 28 % du volume de grume usinée × 0,7 t/m³ (ILLUSTRATION)",
                "gisement": "≈ 2,4 Mt/an",
                "etiquette_gisement": "SOURCÉ (abattages FAOSTAT 2024 (bois rond)) + ratio ILLUSTRATION",
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
                "fenetre_note": "activité de scierie continue sur l'année, point sous garde",
                "techniques": "sciage de grumes résineuses, écorceuse, rabotage"
            },
            {
                "token": "PAILLE_BLE_BY",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "plaine centrale (Minsk-Gomel)",
                "lat": 53.5,
                "lon": 28.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 2 600 000 t (campagne 2025-2026, IndexMundi/USDA PS&D, relevé 03/2026)",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 3,1 Mt/an",
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
                "token": "PAILLE_ORGE_BY",
                "famille": "Céréales",
                "nom_fr": "Paille d'orge",
                "region": "plaine centrale (Minsk-Gomel)",
                "lat": 53.5,
                "lon": 28.0,
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
                "token": "PAILLE_AVOINE_BY",
                "famille": "Céréales",
                "nom_fr": "Paille d'avoine",
                "region": "plaine centrale (Minsk-Gomel)",
                "lat": 53.5,
                "lon": 28.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'avoine, chaumes et glumes",
                "production": "avoine : 320 000 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 320 000 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8,
                    9
                ],
                "fenetre_note": "récolte de juillet à septembre, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            }
        ]
    },
    "Slovaquie": {
        "nom_fao": "Slovakia",
        "portrait": "bassin plaine du Sud (Podunajsko) — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "SCIURE_RESINEUX_SK",
                "famille": "Forestier",
                "nom_fr": "Sciure, copeaux et écorces de scierie",
                "region": "scieries des Tatras (Poprad)",
                "lat": 49.0,
                "lon": 21.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "sciure, copeaux et écorces de résineux de scierie",
                "production": "abattages de bois rond industriels : 9 Mm³ (FAOSTAT 2024 (bois rond))",
                "ratio": "sciure, copeaux et écorces ≈ 28 % du volume de grume usinée × 0,7 t/m³ (ILLUSTRATION)",
                "gisement": "≈ 1,8 Mt/an",
                "etiquette_gisement": "SOURCÉ (abattages FAOSTAT 2024 (bois rond)) + ratio ILLUSTRATION",
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
                "fenetre_note": "activité de scierie continue sur l'année, point sous garde",
                "techniques": "sciage de grumes résineuses, écorceuse, rabotage"
            },
            {
                "token": "PAILLE_BLE_SK",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "plaine du Sud (Podunajsko)",
                "lat": 48.7,
                "lon": 19.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 1 500 000 t (FAOSTAT 2024 (tableau Wikipédia))",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 1,8 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT 2024 (tableau Wikipédia)) + ratio ILLUSTRATION",
                "fenetre": [
                    6,
                    7,
                    8
                ],
                "fenetre_note": "récolte de juin à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes, fourrage prioritaire"
            },
            {
                "token": "RESIDUS_COLZA_SK",
                "famille": "Céréales",
                "nom_fr": "Résidus de colza",
                "region": "plaine du Sud (Podunajsko)",
                "lat": 48.7,
                "lon": 19.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "pailles et cosses de colza",
                "production": "colza (graines) : 393 540 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 2,5 × graines (ILLUSTRATION)",
                "gisement": "≈ 983 850 t/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson, battage, andains de cosses"
            }
        ]
    },
    "Hongrie": {
        "nom_fao": "Hungary",
        "portrait": "bassin Grande Plaine de l'Alföld (Szeged) — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "RESIDUS_MAIS_HU",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "Grande Plaine de l'Alföld (Szeged)",
                "lat": 47.2,
                "lon": 19.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 5 297 730 t (FAOSTAT QCL 2024)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 1,3 Mt/an",
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
                "token": "PAILLE_BLE_HU",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "Grande Plaine de l'Alföld (Szeged)",
                "lat": 47.2,
                "lon": 19.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 5 272 960 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 6,3 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    6,
                    7,
                    8
                ],
                "fenetre_note": "récolte de juin à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes, fourrage prioritaire"
            },
            {
                "token": "TIGE_TOURNESOL_HU",
                "famille": "Céréales",
                "nom_fr": "Tiges de tournesol",
                "region": "Grande Plaine de l'Alföld (Szeged)",
                "lat": 47.2,
                "lon": 19.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et capitules de tournesol",
                "production": "tournesol (graines) : 1 798 950 t (FAOSTAT QCL 2024)",
                "ratio": "tiges ≈ 2 × graines (ILLUSTRATION)",
                "gisement": "≈ 3,6 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    8,
                    9,
                    10
                ],
                "fenetre_note": "récolte de août à octobre, point sous garde",
                "techniques": "récolte des capitules, broyage des tiges"
            },
            {
                "token": "RESIDUS_COLZA_HU",
                "famille": "Céréales",
                "nom_fr": "Résidus de colza",
                "region": "Grande Plaine de l'Alföld (Szeged)",
                "lat": 47.2,
                "lon": 19.5,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "pailles et cosses de colza",
                "production": "colza (graines) : 450 360 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 2,5 × graines (ILLUSTRATION)",
                "gisement": "≈ 1,1 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson, battage, andains de cosses"
            }
        ]
    },
    "Bulgarie": {
        "nom_fao": "Bulgaria",
        "portrait": "bassin plaine de Thrace (Plovdiv) — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "PAILLE_BLE_BG",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "plaine de Thrace (Plovdiv)",
                "lat": 42.8,
                "lon": 25.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 7 085 140 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 8,5 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    6,
                    7,
                    8
                ],
                "fenetre_note": "récolte de juin à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes, fourrage prioritaire"
            },
            {
                "token": "TIGE_TOURNESOL_BG",
                "famille": "Céréales",
                "nom_fr": "Tiges de tournesol",
                "region": "plaine de Thrace (Plovdiv)",
                "lat": 42.8,
                "lon": 25.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et capitules de tournesol",
                "production": "tournesol (graines) : 1 644 740 t (FAOSTAT QCL 2024)",
                "ratio": "tiges ≈ 2 × graines (ILLUSTRATION)",
                "gisement": "≈ 3,3 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    8,
                    9,
                    10
                ],
                "fenetre_note": "récolte de août à octobre, point sous garde",
                "techniques": "récolte des capitules, broyage des tiges"
            }
        ]
    },
    "Serbie": {
        "nom_fao": "Serbia",
        "portrait": "bassin Vojvodine céréalière (Novi Sad) — profil agricole à compléter (v1.4)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.4)"
            ]
        },
        "intrants": [
            {
                "token": "RESIDUS_MAIS_RS",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "Vojvodine céréalière (Novi Sad)",
                "lat": 44.3,
                "lon": 20.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 5 107 309 t (FAOSTAT QCL 2024)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 1,3 Mt/an",
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
                "token": "PAILLE_BLE_RS",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "Vojvodine céréalière (Novi Sad)",
                "lat": 44.3,
                "lon": 20.3,
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
                "token": "TIGE_TOURNESOL_RS",
                "famille": "Céréales",
                "nom_fr": "Tiges de tournesol",
                "region": "Vojvodine céréalière (Novi Sad)",
                "lat": 44.3,
                "lon": 20.3,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges et capitules de tournesol",
                "production": "tournesol (graines) : 622 512 t (FAOSTAT QCL 2024)",
                "ratio": "tiges ≈ 2 × graines (ILLUSTRATION)",
                "gisement": "≈ 1,2 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    8,
                    9,
                    10
                ],
                "fenetre_note": "récolte de août à octobre, point sous garde",
                "techniques": "récolte des capitules, broyage des tiges"
            }
        ]
    }
}


def _index():
    idx = {}
    for pays, fiche in PAYS_EUROPE_NORD.items():
        for intrant in fiche["intrants"]:
            idx[intrant["token"]] = (pays, intrant)
    return idx


INDEX = _index()


def verifier_couverture():
    return set(INDEX) & (set(_master.ATLAS_BIOMASSES_MONDE) | set(_p11.INDEX)
                         | set(_v12.INDEX) | set(_v13.INDEX))


def sommaire():
    lignes = ["Atlas Europe du Nord et scieries (v1.4) — %d pays, %d intrants" % (len(PAYS_EUROPE_NORD), len(INDEX))]
    for pays in sorted(PAYS_EUROPE_NORD, key=lambda p: p.lower()):
        lignes.append("  %s — %d intrant(s)" % (pays, len(PAYS_EUROPE_NORD[pays]["intrants"])))
    return "\n".join(lignes)


def fiche_token(token):
    if token not in INDEX:
        return None
    pays, intrant = INDEX[token]
    return {"pays": pays, "intrant": intrant}


def croisement():
    lignes = ["Pays couverts : %d" % len(PAYS_EUROPE_NORD)]
    lignes.append("Intrants : %d (attendu 64)" % len(INDEX))
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
