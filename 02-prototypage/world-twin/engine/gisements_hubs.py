#!/usr/bin/env python3
"""Couche P2.8 — gisements FAOSTAT par point, dimensionnement des hubs (v1.7, 31/10/2026).

Remplace la règle ILLUSTRATION de dimensionnement par densité de points
(v1.6) par un dimensionnement fondé sur les gisements réels FAOSTAT
(bulk Production_Crops_Livestock_E, licence CC BY 4.0, attribution FAO).

MÉTHODE :
- Chaque point d'intrant des atlas versionnés (v1.0, v1.1, v1.2) reçoit un
  gisement en tonnes par an, fourchette [min, milieu, max], calculé comme :
  base FAOSTAT (min, moyenne, max de la fenêtre 2020-2024 de l'élément
  Production ou Area harvested du couple pays/item) multipliée par un ratio
  de résidu ILLUSTRATION (min, milieu, max) issu des fiches d'atlas.
- Les valeurs FAOSTAT proviennent du snapshot versionné
  gisements-faostat-snapshot-v17.json (régénérable, voir le document
  gisements-hubs-generalises.md). Le bulk brut (545 Mo) ne jamais être
  versionné : doctrine cache-faostat-bulk/.
- Les points sans équivalent FAOSTAT (forestier, minéral, marin,
  brassicole, sargasse, bambou, agave à tequila, liège, luzerne) restent
  étiquetés À SOURCER et sont exclus du calcul numérique : aucune valeur
  n'est jamais inventée.
- Le gisement d'un hub est la somme des milieux de fourchette de ses
  points sourcés. Le nombre de trios suit des paliers sur ce gisement
  (règle ILLUSTRATION, plafond figé de 5 trios par équipe d'opérateurs).

GARDE-FOUS :
- Étiquette SYNTHÉTIQUE pour toute la flotte simulée — registre de
  développement, jamais le registre Merkle de production.
- Aucune valeur calibrée, aucun paramètre VDE, aucune clé (doctrine PI).
- Les ratios de résidus restent ILLUSTRATION et non calibrants. Les
  gisements sont nationaux : la décomposition régionale addressable
  reste À SOURCER (P3), le proxy national est documenté dans chaque
  fiche d'origine (« brut national »).
- Bases de masse hétérogènes assumées : sèche pour les grains et pailles,
  humide pour bagasse, écorces, cerises de café, cabosses fraîches.

Lancement (bibliothèque standard uniquement) :

    python3 gisements_hubs.py verifier     # contrôles croisés et couverture
    python3 gisements_hubs.py table        # table des gisements par token
"""

import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

FENETRE = (2020, 2024)
SNAPSHOT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "gisements-faostat-snapshot-v17.json")

# Paliers de dimensionnement ILLUSTRATION : gisement du hub en t/an.
# 1 à 5 trios, plafond figé de 5 trios par équipe d'opérateurs.
SEUILS_TRIO = (500.0e3, 2.0e6, 10.0e6, 50.0e6)

# Noms de pays des atlas (français) vers noms FAOSTAT bulk (anglais).
# Pièges bulk documentés : « China, mainland », « Türkiye »,
# « United States of America », « Republic of Moldova », « Viet Nam ».
PAYS_FAOSTAT = {
    "Afrique du Sud": "South Africa",
    "Allemagne": "Germany",
    "Arabie Saoudite": "Saudi Arabia",
    "Argentine": "Argentina",
    "Australie": "Australia",
    "Brésil": "Brazil",
    "Chili": "Chile",
    "Chine": "China, mainland",
    "Côte d'Ivoire": "Côte d'Ivoire",
    "Égypte": "Egypt",
    "Équateur": "Ecuador",
    "Espagne": "Spain",
    "États-Unis": "United States of America",
    "France": "France",
    "Géorgie": "Georgia",
    "Grèce": "Greece",
    "Inde": "India",
    "Iran": "Iran (Islamic Republic of)",
    "Italie": "Italy",
    "Malaisie": "Malaysia",
    "Maroc": "Morocco",
    "Mexique": "Mexico",
    "Moldavie": "Republic of Moldova",
    "Nouvelle-Zélande": "New Zealand",
    "Pérou": "Peru",
    "Philippines": "Philippines",
    "Portugal": "Portugal",
    "Roumanie": "Romania",
    "Russie": "Russian Federation",
    "Suisse": "Switzerland",
    "Turquie": "Türkiye",
    "Viêt Nam": "Viet Nam",
}

# Ratio de résidu (min, milieu, max) appliqué à la base FAOSTAT.
# Conventions calibrées sur les fiches v1.1/v1.2 (SOURCÉ FAOSTAT 2024)
# puis étendues aux fiches v1.0 : chaque milieu reproduit la valeur
# SOURCÉ de sa fiche d'origine. Élément « Production » en tonnes sauf
# mention, « Area harvested » en hectares pour les ratios en t/ha.
AUTRE_NOIX = ("Other nuts (excluding wild edible nuts and groundnuts),"
              " in shell, n.e.c.")

MAPPINGS = {
    # --- Arabie Saoudite ---
    "PAILLE_BLE_SA": {"pays": "Arabie Saoudite", "item": "Wheat",
                      "element": "Production", "ratio": (0.8, 1.0, 1.2)},
    "RACHIS_PALMIER_SA": {"pays": "Arabie Saoudite", "item": "Dates",
                          "element": "Area harvested",
                          "ratio": (2.0, 2.5, 3.0),
                          "note": "rachis de dattier figé v1.3, en t/ha"},
    "NOYAU_DATTE": {"pays": "Arabie Saoudite", "item": "Dates",
                    "element": "Production",
                    "ratio": (0.10, 0.125, 0.15),
                    "note": "noyau ≈ 10 à 15 % de la datte (fiche v1.0)"},
    "DECHET_DATTIER": {"pays": "Arabie Saoudite", "item": "Dates",
                       "element": "Area harvested",
                       "ratio": (2.0, 4.0, 6.0),
                       "note": "élagage 20 à 40 kg/arbre × 100 à 150"
                               " arbres/ha, chaîne ILLUSTRATION en t/ha"},
    # --- Argentine ---
    "PAILLE_BLE_AR": {"pays": "Argentine", "item": "Wheat",
                      "element": "Production", "ratio": (0.8, 1.0, 1.2)},
    "PAILLE_MAIS_AR": {"pays": "Argentine", "item": "Maize (corn)",
                       "element": "Production", "ratio": (0.8, 1.0, 1.2)},
    "PAILLE_SOJA_AR": {"pays": "Argentine", "item": "Soya beans",
                       "element": "Production", "ratio": (0.8, 1.0, 1.2)},
    "TIGE_TOURNESOL_AR": {"pays": "Argentine", "item": "Sunflower seed",
                          "element": "Production", "ratio": (1.0, 1.5, 2.0)},
    # --- Australie ---
    "BAGASSE_CANNE_AU": {"pays": "Australie", "item": "Sugar cane",
                         "element": "Production", "ratio": (0.25, 0.28, 0.30),
                         "note": "humide"},
    "PAILLE_BLE_AU": {"pays": "Australie", "item": "Wheat",
                      "element": "Production", "ratio": (0.8, 1.0, 1.2)},
    "PAILLE_COLZA_AU": {"pays": "Australie", "item": "Rape or colza seed",
                        "element": "Production", "ratio": (1.0, 1.5, 2.0)},
    "PAILLE_ORGE_AU": {"pays": "Australie", "item": "Barley",
                       "element": "Production", "ratio": (0.8, 0.9, 1.0)},
    "COQUE_MACADAMIA": {"pays": "Australie", "item": AUTRE_NOIX,
                        "element": "Production", "ratio": (0.60, 0.65, 0.70),
                        "note": "proxy « Other nuts » ≈ macadamia australien,"
                                " coque ≈ 60 à 70 % de la masse en coque"},
    # --- Brésil ---
    "BALLE_RIZ_BR": {"pays": "Brésil", "item": "Rice",
                     "element": "Production", "ratio": (0.18, 0.20, 0.22)},
    "ECORCE_ORANGE_BR": {"pays": "Brésil", "item": "Oranges",
                         "element": "Production", "ratio": (0.22, 0.25, 0.28),
                         "note": "humide"},
    "PAILLE_CANNE_BR": {"pays": "Brésil", "item": "Sugar cane",
                         "element": "Production",
                         "ratio": (0.10, 0.125, 0.15),
                         "note": "pointes et feuilles, brut"},
    "PAILLE_MAIS_BR": {"pays": "Brésil", "item": "Maize (corn)",
                       "element": "Production", "ratio": (0.8, 1.0, 1.2)},
    "PAILLE_SOJA_BR": {"pays": "Brésil", "item": "Soya beans",
                       "element": "Production", "ratio": (0.8, 1.0, 1.2)},
    "BAGASSE_CANNE": {"pays": "Brésil", "item": "Sugar cane",
                      "element": "Production", "ratio": (0.25, 0.28, 0.30),
                      "note": "fiche v1.0, même convention que v1.1, humide"},
    "GRAINE_PAPAYE": {"pays": "Brésil", "item": "Papayas",
                      "element": "Production", "ratio": (0.10, 0.125, 0.15),
                      "note": "graines ≈ 10 à 15 % du fruit (fiche v1.0),"
                              " addendum À MESURER du master"},
    # --- Chili ---
    # --- Chine ---
    "COQUE_ARACHIDE_CN": {"pays": "Chine", "item": "Groundnuts, excluding shelled",
                          "element": "Production", "ratio": (0.25, 0.30, 0.35)},
    "PAILLE_BLE_CN": {"pays": "Chine", "item": "Wheat",
                      "element": "Production", "ratio": (0.8, 1.0, 1.2)},
    "PAILLE_MAIS_CN": {"pays": "Chine", "item": "Maize (corn)",
                       "element": "Production", "ratio": (0.8, 1.0, 1.2)},
    "PAILLE_RIZ_CN": {"pays": "Chine", "item": "Rice",
                      "element": "Production", "ratio": (1.0, 1.2, 1.4)},
    # --- Côte d'Ivoire ---
    "COQUE_CACAO_CI": {"pays": "Côte d'Ivoire", "item": "Cocoa beans",
                       "element": "Production", "ratio": (0.65, 0.70, 0.75)},
    "COQUE_CAJOU_CI": {"pays": "Côte d'Ivoire", "item": "Cashew nuts, in shell",
                       "element": "Production", "ratio": (0.65, 0.70, 0.75)},
    "FIBRE_PALMIER_CI": {"pays": "Côte d'Ivoire", "item": "Oil palm fruit",
                         "element": "Production", "ratio": (0.22, 0.25, 0.28),
                         "note": "fibres et coques selon la fiche v1.1"},
    "PAILLE_RIZ_CI": {"pays": "Côte d'Ivoire", "item": "Rice",
                      "element": "Production", "ratio": (1.0, 1.2, 1.4)},
    "CABOSSE_CACAO": {"pays": "Côte d'Ivoire", "item": "Cocoa beans",
                      "element": "Production", "ratio": (8.0, 10.0, 12.0),
                      "note": "cabosses ≈ 10 fois les fèves en matière"
                              " fraîche (fiche v1.0), base humide"},
    # --- Espagne ---
    "BALLE_RIZ_ES": {"pays": "Espagne", "item": "Rice",
                     "element": "Production", "ratio": (0.18, 0.20, 0.22)},
    "ECORCE_ORANGE_ES": {"pays": "Espagne", "item": "Oranges",
                         "element": "Production", "ratio": (0.22, 0.25, 0.28)},
    "PAILLE_BLE_ES": {"pays": "Espagne", "item": "Wheat",
                      "element": "Production", "ratio": (0.8, 1.0, 1.2)},
    "PAILLE_ORGE_ES": {"pays": "Espagne", "item": "Barley",
                       "element": "Production", "ratio": (0.8, 0.9, 1.0)},
    "COQUE_AMANDE": {"pays": "Espagne", "item": "Almonds, in shell",
                     "element": "Production", "ratio": (1.8, 2.0, 2.2),
                     "note": "convention v1.1 amande : coques et écales"
                             " ≈ 2 fois l'amande FAOSTAT"},
    # --- France (master v1.0) ---
    "BALLE_AVOINE": {"pays": "France", "item": "Oats",
                     "element": "Production", "ratio": (0.20, 0.25, 0.30),
                     "note": "balle ≈ 20 à 30 % du grain (fiche v1.0)."
                             " Correction de sourcing : la fiche citait"
                             " 2 à 3 Mt d'avoine, FAOSTAT donne 0,3 à 0,5 Mt"},
    "BALLE_RIZ": {"pays": "France", "item": "Rice",
                  "element": "Production", "ratio": (0.18, 0.20, 0.22),
                  "note": "paddy 71 960 t en 2024, cohérent avec la fiche"
                          " SOURCÉ v0.9"},
    "CHENEVOTTE": {"pays": "France", "item": "True hemp, raw or retted",
                   "element": "Production", "ratio": (0.50, 0.55, 0.60),
                   "note": "chènevotte ≈ 50 à 60 % de la tige défibrée"
                           " (fiche v1.0)"},
    "DRECHE_BIERE": {"pays": "France", "item": "Beer of barley, malted",
                     "element": "Production", "ratio": (0.15, 0.20, 0.25),
                     "note": "20 kg/hl brassé (fiche v1.0), 1 t ≈ 10 hl,"
                             " base humide. Correction de sourcing : la"
                             " fiche citait 1,5 à 2 Mt, le calcul donne"
                             " ≈ 0,43 Mt"},
    "MARC_POMME": {"pays": "France", "item": "Apples",
                   "element": "Production", "ratio": (0.15, 0.20, 0.25),
                   "note": "marc ≈ 20 à 25 % du pressurage (fiche v1.0),"
                           " proxy pommes FAOSTAT"},
    "NOYAU_ABRICOT": {"pays": "France", "item": "Apricots",
                      "element": "Production", "ratio": (0.06, 0.08, 0.10)},
    "NOYAU_CERISE": {"pays": "France", "item": "Cherries",
                     "element": "Production", "ratio": (0.08, 0.10, 0.12)},
    "NOYAU_PECHE": {"pays": "France", "item": "Peaches and nectarines",
                    "element": "Production", "ratio": (0.06, 0.08, 0.10)},
    "PAILLE_BLE": {"pays": "France", "item": "Wheat",
                   "element": "Production", "ratio": (0.8, 1.0, 1.2),
                   "note": "paille ≈ 0,8 à 1,2 fois le grain (fiche v1.0)"},
    "PAILLE_LIN": {"pays": "France", "item": "Flax, raw or retted",
                   "element": "Production", "ratio": (0.40, 0.50, 0.60),
                   "note": "anas ≈ 50 % de la paille teillée (fiche v1.0),"
                           " base paille de lin FAOSTAT"},
    "TIGE_COLZA": {"pays": "France", "item": "Rape or colza seed",
                   "element": "Production", "ratio": (1.0, 1.5, 2.0),
                   "note": "famille harmonisée sur la convention v1.1"},
    "TIGE_SORGHO": {"pays": "France", "item": "Sorghum",
                    "element": "Area harvested", "ratio": (3.0, 4.5, 6.0),
                    "note": "tiges ≈ 3 à 6 t/ha (fiche v1.0)"},
    "TIGE_TOURNESOL": {"pays": "France", "item": "Sunflower seed",
                       "element": "Production", "ratio": (1.0, 1.5, 2.0),
                       "note": "famille harmonisée sur la convention v1.1"},
    # --- Inde ---
    "BALLE_ARACHIDE_IN": {"pays": "Inde", "item": "Groundnuts, excluding shelled",
                          "element": "Production", "ratio": (0.25, 0.30, 0.35)},
    "PAILLE_BLE_IN": {"pays": "Inde", "item": "Wheat",
                      "element": "Production", "ratio": (0.8, 1.0, 1.2)},
    "PAILLE_RIZ_IN": {"pays": "Inde", "item": "Rice",
                      "element": "Production", "ratio": (1.0, 1.2, 1.4)},
    "TIGE_MOUTARDE_IN": {"pays": "Inde", "item": "Rape or colza seed",
                         "element": "Production", "ratio": (1.2, 1.5, 1.8),
                         "note": "moutarde indienne rapportée sous colza"
                                 " dans FAOSTAT (vérifié : 13,3 Mt × 1,5"
                                 " ≈ 19,9 Mt de la fiche)"},
    "TIGE_COTON": {"pays": "Inde", "item": "Seed cotton, unginned",
                   "element": "Area harvested", "ratio": (2.0, 2.5, 3.0),
                   "note": "tiges ≈ 2 à 3 t/ha (fiche v1.0), proxy national"
                           " documenté (le point citait le Pendjab)"},
    # --- Italie ---
    "BALLE_RIZ_IT": {"pays": "Italie", "item": "Rice",
                     "element": "Production", "ratio": (0.18, 0.20, 0.22)},
    "PAILLE_BLE_IT": {"pays": "Italie", "item": "Wheat",
                      "element": "Production", "ratio": (0.8, 1.0, 1.2)},
    "RAFLE_MAIS_IT": {"pays": "Italie", "item": "Maize (corn)",
                      "element": "Production", "ratio": (0.12, 0.15, 0.18)},
    "COQUE_NOISETTE": {"pays": "Italie", "item": "Hazelnuts, in shell",
                       "element": "Production", "ratio": (0.45, 0.475, 0.50)},
    "COQUE_PISTACHE": {"pays": "Italie", "item": AUTRE_NOIX,
                       "element": "Production", "ratio": (0.45, 0.50, 0.55),
                       "note": "proxy « Other nuts » ≈ pistaches de Bronte,"
                               " alternance bisannuelle documentée (fiche v1.0)"},
    # --- Malaisie ---
    "COQUE_COCO_MY": {"pays": "Malaisie", "item": "Coconuts, in shell",
                      "element": "Production", "ratio": (0.35, 0.40, 0.45)},
    "FIBRE_PALMIER_MY": {"pays": "Malaisie", "item": "Oil palm fruit",
                         "element": "Production", "ratio": (0.10, 0.12, 0.14),
                         "note": "fibres seules (coques en sus selon fiche)"},
    "PAILLE_RIZ_MY": {"pays": "Malaisie", "item": "Rice",
                      "element": "Production", "ratio": (1.0, 1.2, 1.4)},
    "RAFFLE_PALMIER": {"pays": "Malaisie", "item": "Oil palm fruit",
                       "element": "Production", "ratio": (0.20, 0.22, 0.25),
                       "note": "rafles (EFB) figé v1.3 : 0,22 × régimes"},
    # --- Maroc ---
    "PAILLE_BLE_MA": {"pays": "Maroc", "item": "Wheat",
                      "element": "Production", "ratio": (0.8, 1.0, 1.2)},
    "PAILLE_ORGE_MA": {"pays": "Maroc", "item": "Barley",
                       "element": "Production", "ratio": (0.8, 0.9, 1.0)},
    # --- Mexique ---
    "BAGASSE_CANNE_MX": {"pays": "Mexique", "item": "Sugar cane",
                         "element": "Production", "ratio": (0.25, 0.28, 0.30)},
    "COQUE_CAFE_MX": {"pays": "Mexique", "item": "Coffee, green",
                      "element": "Production", "ratio": (0.18, 0.20, 0.22)},
    "ECORCE_ORANGE_MX": {"pays": "Mexique", "item": "Oranges",
                         "element": "Production", "ratio": (0.22, 0.25, 0.28)},
    "PAILLE_MAIS_MX": {"pays": "Mexique", "item": "Maize (corn)",
                       "element": "Production", "ratio": (0.8, 1.0, 1.2)},
    "NOYAU_AVOCAT": {"pays": "Mexique", "item": "Avocados",
                     "element": "Production", "ratio": (0.15, 0.20, 0.25),
                     "note": "noyau ≈ 15 à 25 % de la masse (fiche v1.0)"},
    # --- Philippines ---
    "BAGASSE_CANNE_PH": {"pays": "Philippines", "item": "Sugar cane",
                         "element": "Production", "ratio": (0.25, 0.28, 0.30)},
    "BALLE_RIZ_PH": {"pays": "Philippines", "item": "Rice",
                     "element": "Production", "ratio": (0.18, 0.20, 0.22)},
    "ECORCE_BANANE_PH": {"pays": "Philippines", "item": "Bananas",
                         "element": "Production", "ratio": (0.25, 0.30, 0.35)},
    "PAILLE_RIZ_PH": {"pays": "Philippines", "item": "Rice",
                      "element": "Production", "ratio": (1.0, 1.2, 1.4)},
    "FEUILLE_ANANAS": {"pays": "Philippines", "item": "Pineapples",
                       "element": "Area harvested", "ratio": (3.0, 4.5, 6.0),
                       "note": "feuilles ≈ 3 à 6 t/ha/cycle en matière"
                               " sèche (fiche v1.0)"},
    "FIBRE_COCO": {"pays": "Philippines", "item": "Coconuts, in shell",
                   "element": "Production", "ratio": (0.25, 0.30, 0.35),
                   "note": "balle ≈ 25 à 35 % du fruit (fiche v1.0)"},
    # --- Portugal ---
    "GRIGNON_OLIVE_PT": {"pays": "Portugal", "item": "Olives",
                         "element": "Production", "ratio": (0.35, 0.40, 0.45)},
    "PAILLE_BLE_PT": {"pays": "Portugal", "item": "Wheat",
                      "element": "Production", "ratio": (0.8, 1.0, 1.2)},
    # --- Suisse ---
    "PAILLE_BLE_CH": {"pays": "Suisse", "item": "Wheat",
                      "element": "Production", "ratio": (0.8, 1.0, 1.2)},
    "MARC_POMME_CH": {"pays": "Suisse", "item": "Apples",
                      "element": "Production", "ratio": (0.15, 0.20, 0.25)},
    # --- Viêt Nam ---
    "BAGASSE_CANNE_VN": {"pays": "Viêt Nam", "item": "Sugar cane",
                         "element": "Production", "ratio": (0.25, 0.28, 0.30)},
    "COQUE_CAFE_VN": {"pays": "Viêt Nam", "item": "Coffee, green",
                      "element": "Production", "ratio": (0.18, 0.20, 0.22)},
    "COQUE_CAJOU_VN": {"pays": "Viêt Nam", "item": "Cashew nuts, in shell",
                       "element": "Production", "ratio": (0.65, 0.70, 0.75),
                       "note": "production domestique (la fiche note que"
                               " l'importation de noix brutes double le"
                               " flux des usines)"},
    "PAILLE_RIZ_VN": {"pays": "Viêt Nam", "item": "Rice",
                      "element": "Production", "ratio": (1.0, 1.2, 1.4)},
    "MARC_CAFE": {"pays": "Viêt Nam", "item": "Coffee, green",
                  "element": "Production", "ratio": (2.10, 2.25, 2.40),
                  "note": "pulpe ≈ 40 à 45 % de la cerise fraîche (fiche"
                          " v1.0) et cerise fraîche ≈ 5,2 × café vert"
                          " (ILLUSTRATION), base humide"},
    # --- Équateur ---
    "BAGASSE_CANNE_EC": {"pays": "Équateur", "item": "Sugar cane",
                         "element": "Production", "ratio": (0.25, 0.28, 0.30)},
    "BALLE_RIZ_EC": {"pays": "Équateur", "item": "Rice",
                     "element": "Production", "ratio": (0.18, 0.20, 0.22)},
    "FIBRE_PALMIER_EC": {"pays": "Équateur", "item": "Oil palm fruit",
                         "element": "Production", "ratio": (0.10, 0.12, 0.14)},
    "TIGE_BANANIER": {"pays": "Équateur", "item": "Bananas",
                      "element": "Area harvested", "ratio": (30.0, 40.0, 50.0),
                      "note": "pseudotroncs ≈ 30 à 50 t/ha/an en matière"
                              " fraîche (fiche v1.0)"},
    # --- États-Unis ---
    "BALLE_RIZ_US": {"pays": "États-Unis", "item": "Rice",
                     "element": "Production", "ratio": (0.18, 0.20, 0.22)},
    "COQUE_AMANDE_US": {"pays": "États-Unis", "item": "Almonds, in shell",
                        "element": "Production", "ratio": (1.8, 2.0, 2.2)},
    "PAILLE_BLE_US": {"pays": "États-Unis", "item": "Wheat",
                      "element": "Production", "ratio": (0.8, 1.0, 1.2)},
    "PAILLE_MAIS_US": {"pays": "États-Unis", "item": "Maize (corn)",
                       "element": "Production", "ratio": (0.8, 1.0, 1.2)},
    "COQUE_PECAN": {"pays": "États-Unis", "item": AUTRE_NOIX,
                    "element": "Production", "ratio": (0.45, 0.50, 0.55),
                    "note": "proxy « Other nuts » ≈ pacanes, proxy national"
                            " documenté (la fiche citait la Géorgie)"},
}

# Familles v1.2 (viticoles) : marc et sarments par pays.
for _pays, _suffixe in [("Afrique du Sud", "ZA"), ("Allemagne", "DE"),
                        ("Argentine", "AR"), ("Australie", "AU"),
                        ("Brésil", "BR"), ("Chili", "CL"), ("Chine", "CN"),
                        ("Espagne", "ES"), ("Grèce", "GR"), ("Italie", "IT"),
                        ("Portugal", "PT"), ("États-Unis", "US")]:
    MAPPINGS["MARC_RAISIN_" + _suffixe] = {
        "pays": _pays, "item": "Grapes", "element": "Production",
        "ratio": (0.15, 0.15, 0.25),
        "note": "marc ≈ 15 à 25 % de la vendange (doctrine v1.2)"}
for _pays, _suffixe in [("Afrique du Sud", "ZA"), ("Allemagne", "DE"),
                        ("Australie", "AU"), ("Brésil", "BR"),
                        ("Chili", "CL"), ("Chine", "CN"),
                        ("Géorgie", "GE"), ("Grèce", "GR"), ("Inde", "IN"),
                        ("Iran", "IR"), ("Maroc", "MA"),
                        ("Moldavie", "MD"), ("Nouvelle-Zélande", "NZ"),
                        ("Portugal", "PT"), ("Pérou", "PE"),
                        ("Roumanie", "RO"), ("Russie", "RU"),
                        ("Turquie", "TR"), ("Égypte", "EG"),
                        ("États-Unis", "US")]:
    MAPPINGS["SARMENT_VIGNE_" + _suffixe] = {
        "pays": _pays, "item": "Grapes", "element": "Area harvested",
        "ratio": (1.5, 2.0, 3.0),
        "note": "sarments ≈ 2 t/ha, fourchette doctrine 1,5 à 3 (v1.2)"}

# Contrôles croisés doctrine du 18/10 (valeurs FAOSTAT 2024 documentées
# dans la base de connaissance). Ces combos doivent figurer dans le
# snapshot même si aucun token ne les référence directement.
CONTROLES_DOCTRINE = [
    ("Spain", "Wheat", "Production", 7147930),
    ("China, mainland", "Wheat", "Production", 140105000),
    ("China, mainland", "Maize (corn)", "Production", 295140069),
    ("China, mainland", "Rice", "Production", 209173000),
    ("India", "Rice", "Production", 217867864),
    ("South Africa", "Grapes", "Production", 1870973),
    ("South Africa", "Grapes", "Area harvested", 103955),
    ("Georgia", "Grapes", "Production", 320700),
    ("Georgia", "Grapes", "Area harvested", 49570),
    ("Republic of Moldova", "Grapes", "Production", 396400),
    ("Republic of Moldova", "Grapes", "Area harvested", 72601),
]

# Points sans équivalent FAOSTAT : jamais de valeur inventée.
A_SOURCER = {
    "FANE_LUZERNE_SA": "aucun item fourrager FAOSTAT pour l'Arabie"
                       " Saoudite, bassin de Al-Jouf/Al-Qassim à documenter"
                       " (fiche v1.1)",
    "BRISURE_LIEGE_PT": "liège hors périmètre FAOSTAT, production"
                        " portugaise à borner (fiche v1.1)",
    "TIGE_BAMBOU": "bamboueraie forestière hors FAOSTAT (Anji), à sourcer"
                   " auprès des données forestières",
    "AIGUILLE_PIN": "litière sylvicole hors FAOSTAT, à sourcer littérature",
    "CARAPACE_CRABE": "filière crustacés hors FAOSTAT, à sourcer DPMA",
    "COPEAU_HETRE": "filière bois hors FAOSTAT, à sourcer",
    "COQUILLE_HUITRE": "filière conchylicole hors FAOSTAT, à sourcer"
                       " CNC/DPMA",
    "COQUILLE_MOULE": "filière conchylicole hors FAOSTAT, à sourcer"
                      " CNC/DPMA",
    "COQUILLE_ST_JACQUES": "débarquements hors FAOSTAT, à sourcer DPMA",
    "ECORCE_PIN": "filière bois hors FAOSTAT, massif landais à sourcer",
    "SCIURE_CHENE": "filière bois hors FAOSTAT, à sourcer CNPF",
    "SCIURE_PIN": "filière bois hors FAOSTAT, à sourcer CNPF",
    "RESIDU_AGAVE": "agave à tequila hors FAOSTAT (l'item « Agave"
                     " fibres » couvre sisal et henequen, pas la piña),"
                     " à sourcer CRT",
    "SARGASSE": "influx marin hors FAOSTAT, à sourcer Red de Monitoreo"
                " de Sargazo",
    "ECORCE_EUCALYPTUS": "filière bois papetier hors FAOSTAT, à sourcer"
                          " CELPA/ICNF",
}

_MEMO_SNAPSHOT = None


def charger_snapshot():
    """Charge le snapshot FAOSTAT versionné (déterministe, en cache)."""
    global _MEMO_SNAPSHOT
    if _MEMO_SNAPSHOT is None:
        with open(SNAPSHOT, encoding="utf-8") as _f:
            _MEMO_SNAPSHOT = json.load(_f)
    return _MEMO_SNAPSHOT


def base_fenetre(pays_bulk, item, element):
    """Min, moyenne et max de l'élément sur la fenêtre 2020-2024."""
    valeurs = []
    for _annee in range(FENETRE[0], FENETRE[1] + 1):
        _valeur = charger_snapshot()["series"].get(
            "%s|%s|%s|%d" % (pays_bulk, item, element, _annee))
        if _valeur is not None:
            valeurs.append(_valeur)
    if not valeurs:
        return None
    return (min(valeurs), statistics.mean(valeurs), max(valeurs))


def gisement_token(token):
    """Gisement fourchette d'un token, ou None si À SOURCER.

    Retourne un dictionnaire avec min, moy, max en tonnes par an,
    la base FAOSTAT de la fenêtre, l'item, l'élément et l'étiquette.
    """
    mapping = MAPPINGS.get(token)
    if mapping is None:
        return None
    pays_bulk = PAYS_FAOSTAT[mapping["pays"]]
    base = base_fenetre(pays_bulk, mapping["item"], mapping["element"])
    if base is None:
        return None
    r_min, r_mid, r_max = mapping["ratio"]
    return {
        "token": token,
        "pays": mapping["pays"],
        "item": mapping["item"],
        "element": mapping["element"],
        "base": {"min": base[0], "moy": base[1], "max": base[2]},
        "min": base[0] * r_min,
        "moy": base[1] * r_mid,
        "max": base[2] * r_max,
        "ratio": mapping["ratio"],
        "note": mapping.get("note", ""),
        "etiquette": "SOURCÉ (FAOSTAT 2020-2024) + ratio ILLUSTRATION",
    }


def gisement_cluster(tokens):
    """Somme des gisements d'un cluster de points (t/an).

    Les tokens À SOURCER sont listés sans valeur. Retourne None si le
    cluster n'a aucun point sourcé (repli densité v1.6 côté appelant).
    """
    total = {"min": 0.0, "moy": 0.0, "max": 0.0,
             "sources": [], "a_sourcer": []}
    for token in tokens:
        gisement = gisement_token(token)
        if gisement is None:
            total["a_sourcer"].append(token)
        else:
            total["min"] += gisement["min"]
            total["moy"] += gisement["moy"]
            total["max"] += gisement["max"]
            total["sources"].append(token)
    if not total["sources"]:
        return None
    return total


def trios_du_gisement(gisement, trios_max):
    """Paliers ILLUSTRATION : 1 à 5 trios selon le gisement du hub.

    Seuils en tonnes par an : 0,5 / 2 / 10 / 50 Mt. Le plafond figé de
    couverture d'une équipe d'opérateurs est appliqué par l'appelant.
    """
    if gisement is None or gisement["moy"] <= 0:
        return None
    palier = 1
    for seuil in SEUILS_TRIO:
        if gisement["moy"] >= seuil:
            palier += 1
    return min(palier, trios_max)


def verifier():
    """Contrôles croisés : doctrine 2024, reproduction des fiches, couverture."""
    import flotte_monde

    rapport = {"controles_doctrine": [], "reproductions_fiches": [],
               "couverture": {}, "erreurs": []}

    controles_doctrine = CONTROLES_DOCTRINE
    for pays, item, element, attendu in controles_doctrine:
        obtenu = charger_snapshot()["series"].get(
            "%s|%s|%s|2024" % (pays, item, element))
        ecart = None if obtenu is None else abs(obtenu - attendu) / attendu
        ok = ecart is not None and ecart <= 0.02
        rapport["controles_doctrine"].append({
            "pays": pays, "item": item, "element": element,
            "attendu": attendu, "obtenu": obtenu,
            "ecart_pct": None if ecart is None else round(ecart * 100, 3),
            "ok": ok})
        if not ok:
            rapport["erreurs"].append("doctrine : %s %s" % (pays, item))

    # Reproduction des valeurs SOURCÉ des fiches v1.1 et v1.2 (2024).
    fiches = {
        "PAILLE_BLE_SA": 0.8e6, "PAILLE_BLE_AR": 18.5e6,
        "PAILLE_MAIS_AR": 57e6, "PAILLE_SOJA_AR": 48e6,
        "TIGE_TOURNESOL_AR": 5.8e6, "BAGASSE_CANNE_AU": 8.4e6,
        "PAILLE_BLE_AU": 34e6, "PAILLE_COLZA_AU": 9.6e6,
        "PAILLE_ORGE_AU": 12e6, "BALLE_RIZ_BR": 2.1e6,
        "ECORCE_ORANGE_BR": 3.9e6, "PAILLE_CANNE_BR": 95e6,
        "PAILLE_MAIS_BR": 115e6, "PAILLE_SOJA_BR": 144e6,
        "COQUE_ARACHIDE_CN": 5.9e6, "PAILLE_BLE_CN": 140e6,
        "PAILLE_MAIS_CN": 295e6, "PAILLE_RIZ_CN": 251e6,
        "COQUE_CACAO_CI": 1.3e6, "COQUE_CAJOU_CI": 0.66e6,
        "FIBRE_PALMIER_CI": 0.57e6, "PAILLE_RIZ_CI": 2.9e6,
        "BALLE_RIZ_ES": 0.12e6, "ECORCE_ORANGE_ES": 0.73e6,
        "PAILLE_BLE_ES": 7.1e6, "PAILLE_ORGE_ES": 6.7e6,
        "BALLE_ARACHIDE_IN": 3.6e6, "PAILLE_BLE_IN": 113e6,
        "PAILLE_RIZ_IN": 261e6, "TIGE_MOUTARDE_IN": 19.9e6,
        "BALLE_RIZ_IT": 0.29e6, "MARC_RAISIN_IT": 1.1e6,
        "PAILLE_BLE_IT": 6.2e6, "RAFLE_MAIS_IT": 0.74e6,
        "COQUE_COCO_MY": 0.27e6, "FIBRE_PALMIER_MY": 12e6,
        "PAILLE_RIZ_MY": 2.5e6, "PAILLE_BLE_MA": 2.4e6,
        "PAILLE_ORGE_MA": 0.59e6, "BAGASSE_CANNE_MX": 14.9e6,
        "COQUE_CAFE_MX": 0.039e6, "ECORCE_ORANGE_MX": 1.2e6,
        "PAILLE_MAIS_MX": 24e6, "BAGASSE_CANNE_PH": 5.2e6,
        "BALLE_RIZ_PH": 3.8e6, "ECORCE_BANANE_PH": 1.7e6,
        "PAILLE_RIZ_PH": 22.9e6, "GRIGNON_OLIVE_PT": 0.54e6,
        "PAILLE_BLE_PT": 0.081e6, "PAILLE_BLE_CH": 0.31e6,
        "MARC_POMME_CH": 0.043e6, "BAGASSE_CANNE_VN": 3.3e6,
        "COQUE_CAFE_VN": 0.40e6, "COQUE_CAJOU_VN": 0.21e6,
        "PAILLE_RIZ_VN": 52e6, "BAGASSE_CANNE_EC": 1.8e6,
        "BALLE_RIZ_EC": 0.31e6, "FIBRE_PALMIER_EC": 0.32e6,
        "BALLE_RIZ_US": 2.0e6, "COQUE_AMANDE_US": 4e6,
        "PAILLE_BLE_US": 54e6, "PAILLE_MAIS_US": 378e6,
        "MARC_RAISIN_ZA": 0.281e6, "SARMENT_VIGNE_ZA": 0.208e6,
        "MARC_RAISIN_DE": 0.159e6, "SARMENT_VIGNE_DE": 0.203e6,
        "MARC_RAISIN_AR": 0.288e6, "MARC_RAISIN_AU": 0.242e6,
        "SARMENT_VIGNE_AU": 0.271e6, "SARMENT_VIGNE_BR": 0.169e6,
        "MARC_RAISIN_CL": 0.368e6, "SARMENT_VIGNE_CL": 0.333e6,
        "MARC_RAISIN_CN": 2.5e6, "SARMENT_VIGNE_CN": 1.5e6,
        "MARC_RAISIN_ES": 0.808e6, "MARC_RAISIN_GR": 0.117e6,
        "SARMENT_VIGNE_GR": 0.167e6, "SARMENT_VIGNE_GE": 0.099e6,
        "SARMENT_VIGNE_IN": 0.359e6, "SARMENT_VIGNE_IR": 0.239e6,
        "SARMENT_VIGNE_MA": 0.080e6, "SARMENT_VIGNE_MD": 0.145e6,
        "SARMENT_VIGNE_NZ": 0.075e6, "MARC_RAISIN_PT": 0.138e6,
        "SARMENT_VIGNE_PT": 0.346e6, "SARMENT_VIGNE_PE": 0.074e6,
        "SARMENT_VIGNE_RO": 0.324e6, "SARMENT_VIGNE_RU": 0.153e6,
        "SARMENT_VIGNE_TR": 0.745e6, "SARMENT_VIGNE_EG": 0.160e6,
        "MARC_RAISIN_US": 0.735e6, "SARMENT_VIGNE_US": 0.747e6,
    }
    for token, fiche in sorted(fiches.items()):
        gisement = gisement_token(token)
        if gisement is None:
            rapport["reproductions_fiches"].append({
                "token": token, "fiche": fiche, "obtenu": None,
                "ecart_pct": None, "ok": False})
            rapport["erreurs"].append("fiche sans gisement : %s" % token)
            continue
        obtenu = _reproduction_2024(token, gisement)
        ecart = abs(obtenu - fiche) / fiche if fiche else 0.0
        ok = ecart <= 0.15
        rapport["reproductions_fiches"].append({
            "token": token, "fiche": fiche, "obtenu": round(obtenu, 1),
            "ecart_pct": round(ecart * 100, 2), "ok": ok})
        if not ok:
            rapport["erreurs"].append("reproduction : %s (écart %.1f %%)"
                                      % (token, ecart * 100))

    # Couverture exhaustive des points des atlas versionnés.
    points, exclus = flotte_monde._collecte_points()
    manquants, a_sourcer, pays_errones = [], [], []
    for point in points:
        token = point["token"]
        if token in MAPPINGS:
            if MAPPINGS[token]["pays"] != point["pays"]:
                pays_errones.append((token, point["pays"]))
        elif token in A_SOURCER:
            a_sourcer.append(token)
        else:
            manquants.append(token)
    rapport["couverture"] = {
        "points": len(points), "exclus_p2": len(exclus),
        "mappes": len(points) - len(manquants) - len(a_sourcer),
        "a_sourcer": sorted(set(a_sourcer)),
        "manquants": sorted(set(manquants)),
        "pays_errones": pays_errones,
    }
    if manquants or pays_errones:
        rapport["erreurs"].append("couverture incomplète : %s %s"
                                  % (manquants, pays_errones))
    rapport["ok"] = not rapport["erreurs"]
    return rapport


def _reproduction_2024(token, gisement):
    """Recalcule la valeur fiche : base FAOSTAT 2024 × ratio milieu."""
    pays_bulk = PAYS_FAOSTAT[gisement["pays"]]
    valeur = charger_snapshot()["series"].get(
        "%s|%s|%s|2024" % (pays_bulk, gisement["item"], gisement["element"]))
    if valeur is None:
        return 0.0
    return valeur * gisement["ratio"][1]


def _table():
    lignes = []
    for token in sorted(MAPPINGS):
        gisement = gisement_token(token)
        if gisement is None:
            lignes.append("%-22s BASE ABSENTE" % token)
            continue
        lignes.append("%-22s %-14s %-26s %12.0f %12.0f %12.0f t/an"
                      % (token, gisement["pays"], gisement["item"],
                         gisement["min"], gisement["moy"], gisement["max"]))
    for token in sorted(A_SOURCER):
        lignes.append("%-22s À SOURCER : %s" % (token, A_SOURCER[token]))
    return "\n".join(lignes)


def main():
    if len(sys.argv) < 2 or sys.argv[1] == "verifier":
        rapport = verifier()
        ok = rapport.pop("ok")
        print(json.dumps(rapport, ensure_ascii=False, indent=1))
        print("VERDICT : %s (%d erreur(s))"
              % ("OK" if ok else "ÉCHEC", len(rapport["erreurs"])))
        return 0 if ok else 1
    if sys.argv[1] == "table":
        print(_table())
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
