#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""World Twin v2.8 — Sites de transformation post-récolte : gisements au site.

Quatre attributs posés sur les 219 hubs (217 généralisés + 2 pilotes) SANS
toucher aux coordonnées ni aux figeages (aucun effet cascade, contrairement à
la vague V2.4) :

1. TYPE_SITE — le type de site de transformation dominant du cluster
   (moulin de palmier à huile, rizerie, sucrerie, moulin d'olive, chai,
   bénéficio, décortiqueur, huller, distillerie, station de conditionnement,
   parcelle agricole pour les gisements diffus).
2. CAPTABILITE — la fraction du gisement théorique disponible AU SITE de
   transformation (et non dispersée aux champs). Étiquetée par famille
   (V2.6) : SOURCÉ quand la littérature chiffre la fraction au site
   (FranceAgriMer marcs 93-99 %, MDPI alperujo 80-85 % du fruit, CNP balle
   20 % du paddy, BioCycle/USAID cabosse ~75 % au champ, parcs MPOB,
   PalmWatch, UNICA), ILLUSTRATION ailleurs ; un hub n'est SOURCÉ que si
   toutes ses familles le sont. V2.7 : six familles supplémentaires passent
   SOURCÉ (drêches de brasserie ~85 % des résidus à la brasserie, marc de
   pomme 25-30 % du fruit au pressoir, résidus d'agrumes 50-60 % du fruit à
   l'usine de jus, bagasse d'agave ~40 % du poids humide à la distillerie,
   résidus de sciage 46 % du volume de grume à la scierie, coques aux
   hullers et décortiqueurs). V2.8 : cinq familles de plus passent
   SOURCÉ (retrait des pailles 19-45 % selon culture, collecte des
   sarments 54-64 %, pelures de manioc ~22 % de la racine, rejets
   et noyaux de dattes 10-15 % de la production en station,
   coquilles 56 % des déchets de conserverie aux plants).
3. ENERGIE_SITE — AUTONOME quand le site vend de l'énergie (moulin de
   palmier, rizerie de parboiling, sucrerie : chaudières biomasse +
   turbines, autofourniture documentée) contre IMPORTATEUR quand le site
   achète (chai, moulin d'olive, bénéficio, scierie). Un module Nomad se
   positionne différemment selon le sens du flux.
4. LOGISTIQUE — LPI 2023 (Logistics Performance Index, Banque mondiale,
   139 pays enquêtés, score 1 à 5) et RAI 2023 (Rural Access Index,
   indicateur 9.1.1 des ODD — Objectifs de Développement Durable : part de
   la population rurale à moins de 2 km d'une route toute saison), tous
   deux SOURCÉS par pays du hub (V2.6 : RAI extrait du jeu SDSN SDG
   Transformation Center « Rural Access Index by Country (2022-2023) »,
   189 pays, d'après la méthodologie Banque mondiale). V2.7 : les 23 pays
   non enquêtés en 2023 mais enquêtés à une édition antérieure récupèrent
   leur score le plus récent (indicateur LP.LPI.OVRL.XQ, API open data
   Banque mondiale, édition portée à la fiche) ; seuls Belize, Soudan du
   Sud et Suriname (jamais enquêtés à aucune édition) reçoivent en
   V2.8 un proxy RÉGIONAL : moyenne simple des scores LPI 2023 des
   pays enquêtés de leur région Banque mondiale (méthode « simple
   averages » des agrégats du jeu Data360 WB_LPI), statut RÉGIONAL
   distinct de SOURCÉ : plus aucun À SOURCER.

Doctrine : tout est étiqueté SYNTHÉTIQUE, aucune valeur calibrée, aucune
clé, aucun coût. Les captabilités portent leur statut SOURCÉ ou
ILLUSTRATION par famille, les LPI et RAI sont des données publiques
SOURCÉES. Jamais le registre Merkle de production.

Sources (toutes publiques, vérifiées le 14/11/2026) :
- Banque mondiale, LPI 2023 (139 pays, republication intégrale NationsInquiry).
- SDSN SDG Transformation Center, RAI 2022-2023 (189 pays, indicateur ODD
  9.1.1, licence Creative Commons BY-NC-SA 4.0, usage interne).
- MPOB (Malaysian Palm Oil Board) : 449 moulins Malaisie, 128 Sabah.
- PalmWatch : 1 471 moulins Indonésie, 79 Colombie, 70 Thaïlande, 40 Équateur.
- UNICA (União da Indústria de Cana-de-Açúcar) : 389 unités Brésil 2025/26.
- CNP (Carbon Negative Power) : balle de riz 20 % du paddy, 13-15 MJ/kg.
- FranceAgriMer : 93-99 % des marcs français partent en distillerie.
- MDPI : alperujo 80-85 % du fruit entrant au moulin à deux phases.
- BioCycle / USAID : environ 75 % de la cabosse de cacao rejetée au champ.
- V2.7 — Banque mondiale, LPI éditions antérieures (indicateur
  LP.LPI.OVRL.XQ, API open data api.worldbank.org, extrait 14/11/2026) :
  23 pays de la flotte récupèrent leur score le plus récent (19 pays en
  2018, Éthiopie Mozambique Tanzanie en 2016, Azerbaïdjan en 2014).
- V2.7 — MDPI Sustainability 18(5):2464 (2026) : drêches ≈ 85 % des
  résidus solides de brasserie, générées à la brasserie.
- V2.7 — MDPI Antioxidants 15(4):429 (2026) : marc de pomme 25-30 % de la
  masse du fruit frais, généré au pressoir industriel.
- V2.7 — MDPI Sustainability 15(21):15225 (2023) : résidus d'orangerie
  50-60 % de la masse du fruit, à l'usine de jus concentré.
- V2.7 — MDPI Fermentation 12(2):79 (2026) : bagasse d'agave ≈ 40 % du
  poids humide de l'agave cuit, à la distillerie.
- V2.7 — FAO, appendice VI « Generation of wood residues » (rapport
  T0269E) : résidus de sciage 46 % du volume de la grume, à la scierie.
- V2.7 — Biomass Conversion and Biorefinery (Springer, 2023) : coques et
  brou de noix, sous-produits des unités de transformation.
- V2.7 — MDPI Foods 14(24):4246 (2025) et MDPI Fermentation 11(2):57
  (2025) : marc de raisin 15-30 % de la vendange (ratio sourcé dans
  gisements_hubs.py, retenu 0,20).
- V2.8 — Resources, Conservation and Recycling (2025) : taux de
  retrait raisonnable des pailles 45 % riz, 19 % blé, 42 % maïs
  (méta-analyse Chine) ; potentiels pailles UE : 33-50 % selon
  État membre (France 50 %, Hongrie 33 %).
- V2.8 — Biomass and Bioenergy (octobre 2018) : prototypes de
  collecte des sarments, pertes 36,2-46,2 % (54-64 % récupéré) ;
  Biosystems Engineering 105(3) (2010) : récolte des sarments
  pour l'énergie (Spinelli, Magagnotti, Nati).
- V2.8 — ILRI, Turning Waste to Wealth (Springer, 2022) : pelage
  manuel du manioc ≈ 22 % de la racine fraîche, aux centres de
  transformation villageois.
- V2.8 — MDPI Applied Sciences 13(22):12315 (2023) : rejets de
  triage et noyaux de dattes = 10-15 % de la production, aux
  stations de conditionnement.
- V2.8 — Waste Management & Research (2022) : revue des co-produits
  industriels de la moule (coquilles = 56 % des déchets de
  conserverie, ~ 27 % du tonne vivante rejeté, Galice, d'après
  Iribarren et al. 2010).
- V2.8 — Banque mondiale, jeu Data360 WB_LPI : agrégats régionaux
  en moyennes simples (méthode du proxy des 3 jamais enquêtés,
  calcul du 14/11/2026 sur le jeu officiel LP.LPI.OVRL.XQ).

Lancement :

    python3 engine/sites_transformation.py                # sommaire
    python3 engine/sites_transformation.py fiche gen-cote-d-ivoire-2
    python3 engine/sites_transformation.py verifier       # contrôles complets
    python3 engine/sites_transformation.py table          # table des 219 hubs
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Familles de sites : (famille, type_site, captabilite, energie_site,
#                     fenetre_fraicheur, motifs, note sourcée)
# L'ordre EST une priorité : le premier motif qui matche gagne, la famille
# dominante du hub est celle de captabilité la plus élevée (égalité : ordre).
# ---------------------------------------------------------------------------
FAMILLES_SITES = [
    ("AU_CHAMP", "parcelle agricole (gisement diffus)", 0.35, "IMPORTATEUR",
     "stockable",
     ["PAILLE_", "TIGE_", "FEUILLE_ANANAS", "FANE_LUZERNE", "BANANE",
      "BALLE_AVOINE", "RESIDUS_COLZA"],
     "pailles, tiges et feuilles au champ : taux de retrait"
     " soutenable 45 % riz, 19 % blé, 42 % maïs (méta-analyse"
     " Resources, Conservation and Recycling 2025), 33-50 % selon"
     " États membres UE (France 50 %, Hongrie 33 %) : fraction"
     " collectable retenue 0,35 (SOURCES V2.8)",
     "SOURCÉ"),
    ("SARMENTS", "AU_CHAMP (rang de vigne)", 0.55, "IMPORTATEUR",
     "saison de taille",
     ["SARMENT_VIGNE", "VINE_SHOOTS", "GRAPE_STALKS"],
     "sarments au rang, 2 t/ha/an figés en V2.4 (BIVB France,"
     " Velázquez-Martí Italie) ; collecte mécanisée : pertes"
     " 36,2-46,2 % selon prototypes, donc 54-64 % récupérable"
     " (Biomass and Bioenergy 2018 ; récolte éprouvée Spinelli,"
     " Magagnotti, Nati, Biosystems Engineering 2010) : retenu"
     " 0,55 (SOURCES V2.8)",
     "SOURCÉ"),
    ("CACAO", "CENTRE_COLLECTE_COOP (écabossage)", 0.20, "IMPORTATEUR",
     "heures",
["CABOSSE_CACAO", "COQUE_CACAO"],
     "environ 75 % de la cabosse rejeté à la plantation (BioCycle/USAID)," 
     "écabossage fermier : le seul point de regroupement est le centre" 
     "coopératif d'achat",
     "SOURCÉ"),
    ("SARGASSES", "ECHECHAGE_COTE", 0.30, "IMPORTATEUR",
     "saisonnier",
["SARGASSE"],
     "échouages atlantiques, ramassage côtier (Marine mexicaine :"
     " 156 063 t collectées au Quintana Roo, saison 2026, record)"
     " mais aucune part chiffrée du gisement échoué dans la"
     " littérature : gisement aléatoire, valeur d'ingénieur",
     "ILLUSTRATION"),
    ("CAFE_PULPE", "STATION_LAVAGE", 0.40, "IMPORTATEUR",
     "heures",
["PULPE_CAFE"],
     "pulpe au bénéficio humide : 44,6 % de la masse de cerise au"
     " moulin humide (Rotta, UC Davis 2020), 29 % du café éthiopien"
     " lavé en station (CABI 2020) ; part du café mexicain passant"
     " au bénéficio humedo À SOURCER (tentative V2.8 infructueuse)",
     "ILLUSTRATION"),
    ("MAIS", "SILO_SECHOIR", 0.40, "IMPORTATEUR",
     "stockable",
["RESIDUS_MAIS", "RAFLE_MAIS"],
     "rafles et résidus aux silos et séchoirs, gisement semi-diffus ;"
     " collecte intégrée à la moisson chiffrée (pertes ~31 %, MDPI"
     " Energies 13(5):1265 2020) mais part centralisée au silo non"
     " chiffrée (tentative V2.8) : reste ILLUSTRATION",
     "ILLUSTRATION"),
    ("MANIOC", "RAPERIE_SECHERIE", 0.50, "IMPORTATEUR",
     "jours",
["MANIOC"],
     "écorces au raspage et au séchage : pelage manuel ≈ 22 % de la"
     " racine fraîche (ILRI, Turning Waste to Wealth, Springer"
     " 2022), garri ≈ 70 % du manioc nigérian transformé hors"
     " exploitation aux centres villageois : retenu 0,50"
     " (SOURCES V2.8)",
     "SOURCÉ"),
    ("NOYAUX_FRUITS", "STATION_CONDITIONNEMENT", 0.50, "IMPORTATEUR",
     "stockable",
["NOYAU_", "GRAINE_PAPAYE"],
     "noyaux de fruits (abricot, pêche, cerise, avocat) aux stations de"
     " conditionnement ; composition chiffrée (revues de"
     " valorisation) mais part des fruits passant en station À"
     " SOURCER (tentative V2.8 infructueuse)",
     "ILLUSTRATION"),
    ("COCO", "DECORTIQUEUR_COCO", 0.60, "IMPORTATEUR",
     "stockable",
["BOURRE_COCO", "COQUE_COCO", "FIBRE_COCO"],
     "bourre et poussière au décorticage, coprah séché au village"
     " (Philippines, Indonésie, Inde) ; l'enquête Philippines"
     " 1 200 fermes, 13 provinces (IJERD 2018) documente la"
     " dispersion à la ferme, part centralisée À SOURCER"
     " (tentative V2.8 infructueuse)",
     "ILLUSTRATION"),
    ("DATTIER", "STATION_CONDITIONNEMENT", 0.60, "IMPORTATEUR",
     "stockable",
["NOYAU_DATTE", "RACHIS_DATTIER", "DECHET_DATTIER"],
     "noyaux et grappes aux stations de conditionnement des palmeraies"
     " (Ziz, Draa, Souf) : rejets de triage et noyaux = 10-15 %"
     " de la production à la station (revue MDPI Applied Sciences"
     " 13(22):12315 2023 ; conditionnement tunisien centralisé,"
     " capacité 59 kt) : retenu 0,60 (SOURCES V2.8)",
     "SOURCÉ"),
    ("THE", "STATION_SECHAGE_THE", 0.60, "IMPORTATEUR",
     "heures",
["RESIDU_THE"],
     "résidus de manufacture (feuilles, tiges, poussière) concentrés"
     " en station (revues Springer 2025, JECE 2025) mais fraction"
     " de la production non chiffrée (tentative V2.8) : reste"
     " ILLUSTRATION",
     "ILLUSTRATION"),
    ("AGAVE", "DISTILLERIE_AGAVE", 0.90, "IMPORTATEUR",
     "stockable",
["RESIDU_AGAVE"],
     "bagasse = environ 40 % du poids humide de l'agave cuit, générée à"
     " la distillerie (MDPI Fermentation 12(2):79 2026), vinasses et"
     " valorisation biogaz émergente au Jalisco",
     "SOURCÉ"),
    ("PECHE_COQUILLES", "STATION_TRANSFORM_PECHE", 0.70, "IMPORTATEUR",
     "heures",
["COQUILLE_", "CARAPACE_CRABE"],
     "coquilles (huître, moule, coquille Saint-Jacques) et carapaces aux"
     " criées et stations : coquilles = 56 % des déchets de"
     " conserverie et ~ 27 % du tonne vivante rejeté en co-produits"
     " aux plants industriels (revue Waste Management & Research"
     " 2022, d'après Iribarren et al. 2010, Galice) : retenu 0,70"
     " (SOURCES V2.8)",
     "SOURCÉ"),
    ("AGRUMES", "USINE_JUS_AGRUMES", 0.90, "IMPORTATEUR",
     "heures",
["MARC_AGRUME", "ECORCE_ORANGE", "MARC_CITRON"],
     "résidus de pressage = 50 à 60 % de la masse du fruit, générés à"
     " l'usine de jus concentré (São Paulo, Floride, Veracruz) (MDPI"
     " Sustainability 15(21):15225 2023)",
     "SOURCÉ"),
    ("CAFE", "BENEFICIO_SEC", 0.70, "IMPORTATEUR",
     "stockable",
["PARCHE_CAFE", "COQUE_CAFE", "MARC_CAFE"],
     "coques au moulin central de décorticage (rebenefício), souvent"
     " brûlées dans les séchoirs ; aucune part centralisée"
     " chiffrée (tentative V2.8 infructueuse) : fraction réelle À"
     " SOURCER",
     "ILLUSTRATION"),
    ("NOIX_COQUES", "HULLER_DECORTIQUEUR", 0.80, "IMPORTATEUR",
     "stockable",
     ["COQUE_AMANDE", "COQUE_MACADAMIA", "COQUE_NOIX", "COQUE_NOISETTE", 
      "COQUE_PISTACHE", "COQUE_PECAN", "COQUE_CAJOU", "COQUE_ARACHIDE", 
"BALLE_ARACHIDE"],
     "coques = sous-produit des hullers et décortiqueurs centralisés"
     " (revue coques et brou de noix, Biomass Conversion and Biorefinery"
     " 2023 ; modèle coopératif de la Central Valley californienne)",
     "SOURCÉ"),
    ("FORET_SCIERIE", "SCIERIE", 0.95, "IMPORTATEUR",
     "continu",
     ["SCIURE_", "ECORCE_PIN", "AIGUILLE_PIN", "COPEAU_HETRE", 
"CHENEVOTTE", "ECORCE_EUCALYPTUS", "BRISURE_LIEGE"],
     "résidus de sciage = 46 % du volume de la grume (délignures et"
     " délignures de sciage 34 % + sciure 12 %), générés à la scierie et à"
     " l'usine de liège (FAO, appendice VI « Generation of wood residues »,"
     " rapport T0269E)",
     "SOURCÉ"),
    ("VIGNE_MARC", "CHAI", 0.95, "IMPORTATEUR",
     "heures (vendange)",
["MARC_RAISIN", "GRAPE_POMACE"],
     "93 à 99 % des marcs français partent en distillerie (FranceAgriMer) :" 
     "gisement très concentré au chai, fenêtre de vendange courte",
     "SOURCÉ"),
    ("BIERE", "BRASSERIE", 0.95, "IMPORTATEUR",
     "continu",
["DRECHE_BIERE"],
     "drêches = environ 85 % des résidus solides de brasserie, générées à"
     " la brasserie (MDPI Sustainability 18(5):2464 2026), flux continu"
     " urbain, forte teneur en eau",
     "SOURCÉ"),
    ("POMME", "PRESSOIR_CIDRERIE", 0.85, "IMPORTATEUR",
     "heures (pressoir)",
["MARC_POMME"],
     "marc de pomme = 25 à 30 % de la masse du fruit frais, généré au"
     " pressoir industriel jus et cidrerie (MDPI Antioxidants"
     " 15(4):429 2026), fenêtre septembre-novembre",
     "SOURCÉ"),
    ("OLIVE", "MOULIN_OLIVE", 0.85, "IMPORTATEUR",
     "jours",
["GRIGNONS_OLIVE", "GRIGNON_OLIVE", "NOYAU_OLIVE", "POMACE_OLIVE"],
     "extraction à deux phases : l'alperujo (80 à 85 % du poids du fruit," 
     "60-70 % d'humidité) reste au moulin (MDPI) ; orujillo partiellement" 
     "brûlé sur place",
     "SOURCÉ"),
    ("RIZ", "RIZERIE", 0.90, "AUTONOME",
     "stockable",
["BALLE_RIZ"],
     "balle = 20 % du paddy, 13-15 MJ/kg, humidité 10 %, disponible au" 
     "point d'usinage ; le parboiling s'autofournit en vapeur (CNP)",
     "SOURCÉ"),
    ("CANNE", "SUCRERIE", 0.90, "AUTONOME",
     "< 48 h",
["BAGASSE_CANNE"],
     "la bagasse autofournit vapeur et électricité, l'excédent part en" 
     "bioélectricité (UNICA : 389 unités Brésil 2025/26) : co-produit le" 
     "plus disputé de la chaîne",
     "SOURCÉ"),
    ("PALMIER", "MOULIN_PALME", 0.90, "AUTONOME",
     "< 24 h",
     ["EFB_PALMIER", "FIBRE_PALMIER", "RAFLES_PALMIER", "RAFLE_PALMIER",
"RAFFLE_PALMIER", "RACHIS_PALMIER"],
     "la totalité des régimes entre au moulin en moins de 24 h (acides gras" 
     "libres) ; fibres et coques autofournissent l'énergie (MPOB : 449" 
     "moulins Malaisie, 128 Sabah ; PalmWatch : 1 471 Indonésie), l'EFB" 
     "humide (60-65 %) reste le co-produit en excès",
     "SOURCÉ"),
]

# ---------------------------------------------------------------------------
# LPI 2023 — Logistics Performance Index, Banque mondiale (SOURCÉ).
# 139 pays enquêtés, score 1 à 5. Les pays du hub non enquêtés en 2023
# restent À SOURCER : aucune valeur inventée.
# ---------------------------------------------------------------------------
LPI_2023 = {
    "SGP": 4.3, "FIN": 4.2, "DNK": 4.1, "DEU": 4.1, "NLD": 4.1, "CHE": 4.1,
    "AUT": 4.0, "BEL": 4.0, "CAN": 4.0, "HKG": 4.0, "SWE": 4.0, "ARE": 4.0,
    "FRA": 3.9, "JPN": 3.9, "ESP": 3.9, "TWN": 3.9, "KOR": 3.8, "USA": 3.8,
    "AUS": 3.7, "CHN": 3.7, "GRC": 3.7, "ITA": 3.7, "NOR": 3.7, "ZAF": 3.7,
    "GBR": 3.7, "EST": 3.6, "ISL": 3.6, "IRL": 3.6, "ISR": 3.6, "LUX": 3.6,
    "MYS": 3.6, "NZL": 3.6, "POL": 3.6, "BHR": 3.5, "LVA": 3.5, "QAT": 3.5,
    "THA": 3.5, "IND": 3.4, "LTU": 3.4, "PRT": 3.4, "SAU": 3.4, "TUR": 3.4,
    "HRV": 3.3, "CZE": 3.3, "MLT": 3.3, "OMN": 3.3, "PHL": 3.3, "SVK": 3.3,
    "SVN": 3.3, "VNM": 3.3, "BRA": 3.2, "BGR": 3.2, "CYP": 3.2, "HUN": 3.2,
    "KWT": 3.2, "ROU": 3.2, "BWA": 3.1, "EGY": 3.1, "MKD": 3.1, "PAN": 3.1,
    "BIH": 3.0, "CHL": 3.0, "IDN": 3.0, "PER": 3.0, "URY": 3.0, "ATG": 2.9,
    "BEN": 2.9, "COL": 2.9, "CRI": 2.9, "HND": 2.9, "MEX": 2.9, "NAM": 2.9,
    "ARG": 2.8, "MNE": 2.8, "RWA": 2.8, "SRB": 2.8, "SLB": 2.8, "LKA": 2.8,
    "BHS": 2.7, "BLR": 2.7, "DJI": 2.7, "SLV": 2.7, "GEO": 2.7, "KAZ": 2.7,
    "PNG": 2.7, "PRY": 2.7, "UKR": 2.7, "BGD": 2.6, "DOM": 2.6, "GTM": 2.6,
    "GNB": 2.6, "MLI": 2.6, "NGA": 2.6, "COG": 2.6, "RUS": 2.6, "UZB": 2.6,
    "ALB": 2.5, "DZA": 2.5, "ARM": 2.5, "BTN": 2.5, "CAF": 2.5, "COD": 2.5,
    "GHA": 2.5, "GRD": 2.5, "GIN": 2.5, "JAM": 2.5, "MUS": 2.5, "MDA": 2.5,
    "MNG": 2.5, "NIC": 2.5, "TJK": 2.5, "TGO": 2.5, "TTO": 2.5, "ZWE": 2.5,
    "BOL": 2.4, "KHM": 2.4, "GAB": 2.4, "GUY": 2.4, "IRQ": 2.4, "LAO": 2.4,
    "LBR": 2.4, "SDN": 2.4, "BFA": 2.3, "FJI": 2.3, "GMB": 2.3, "IRN": 2.3,
    "KGZ": 2.3, "MDG": 2.3, "MRT": 2.3, "SYR": 2.3, "VEN": 2.3, "CUB": 2.2,
    "YEM": 2.2, "AGO": 2.1, "CMR": 2.1, "HTI": 2.1, "SOM": 2.0, "AFG": 1.9,
    "LBY": 1.9,
}


# ---------------------------------------------------------------------------
# LPI éditions antérieures (V2.7) — Logistics Performance Index, Banque
# mondiale, indicateur LP.LPI.OVRL.XQ de l'API open data. Les 23 pays de
# la flotte non enquêtés en 2023 mais enquêtés à une édition précédente
# récupèrent leur score le plus récent, avec l'édition portée à la fiche.
# SOURCÉ : API Banque mondiale (api.worldbank.org), extrait le 14/11/2026.
# Restent À SOURCER : Belize, Soudan du Sud, Suriname (jamais enquêtés,
# aucune édition) : aucune valeur inventée.
# ---------------------------------------------------------------------------
LPI_EDITIONS_ANTERIEURES = {
    "AZE": (2014, 2.45), "BDI": (2018, 2.06), "CIV": (2018, 3.08),
    "ECU": (2018, 2.88), "ETH": (2016, 2.38), "JOR": (2018, 2.69),
    "KEN": (2018, 2.81), "LBN": (2018, 2.72), "MAR": (2018, 2.54),
    "MMR": (2018, 2.30), "MOZ": (2016, 2.68), "MWI": (2018, 2.59),
    "NER": (2018, 2.07), "NPL": (2018, 2.51), "PAK": (2018, 2.42),
    "SEN": (2018, 2.25), "SLE": (2018, 2.08), "TCD": (2018, 2.42),
    "TKM": (2018, 2.41), "TUN": (2018, 2.57), "TZA": (2016, 2.99),
"UGA": (2018, 2.58), "ZMB": (2018, 2.53),
}

# ---------------------------------------------------------------------------
# LPI proxys régionaux (V2.8) — Belize, Soudan du Sud et Suriname n'ont
# été enquêtés à AUCUNE édition (2007-2023, vérifié sur l'indicateur
# LP.LPI.OVRL.XQ) : aucune valeur inventée, à la place un proxy
# RÉGIONAL documenté = moyenne SIMPLE des scores LPI 2023 des pays
# enquêtés de leur région au sens Banque mondiale (méthode « simple
# averages » des agrégats du jeu Data360 WB_LPI). Calcul du 14/11/2026
# sur le jeu officiel : Amérique latine et Caraïbes 2,69 (24 pays
# enquêtés), Afrique subsaharienne 2,54 (26 pays enquêtés). Statut
# RÉGIONAL, jamais SOURCÉ : l'honnêteté doctrinale tient au mot.
# ---------------------------------------------------------------------------
LPI_MOYENNES_REGIONALES = {
    "BLZ": (2.69, 24, "Amérique latine et Caraïbes"),
    "SSD": (2.54, 26, "Afrique subsaharienne"),
    "SUR": (2.69, 24, "Amérique latine et Caraïbes"),
}


# ---------------------------------------------------------------------------
# RAI 2023 — Rural Access Index, indicateur 9.1.1 des ODD (Objectifs de
# Développement Durable) : part de la population rurale vivant à moins de
# 2 km d'une route praticable toute saison, en pourcentage. SOURCÉ :
# SDSN (Sustainable Development Solutions Network) SDG Transformation
# Center, jeu « Rural Access Index by Country (2022-2023) », d'après la
# méthodologie Banque mondiale (GRIP, Global Road Inventory Project),
# licence Creative Commons BY-NC-SA 4.0 (usage interne, attribution).
# Extrait le 14/11/2026 par l'API ArcGIS du hub SDSN (200 entités, 199
# valeurs 2023 valides, territoires contestés exclus). Aucune valeur
# inventée : les pays absents de l'enquête resteraient À SOURCER.
# ---------------------------------------------------------------------------
RAI_2023 = {
    "AFG": 57, "AGO": 74, "ALB": 100, "AND": 100, "ARE": 96, "ARG": 93, "ARM": 85, "ATG": 100, "AUS": 100, "AUT": 100,
    "AZE": 55, "BDI": 67, "BEL": 100, "BEN": 79, "BFA": 63, "BGD": 98, "BGR": 100, "BHR": 100, "BHS": 95, "BIH": 100,
    "BLR": 100, "BLZ": 90, "BOL": 88, "BRA": 97, "BRB": 98, "BRN": 100, "BTN": 90, "BWA": 83, "CAF": 51, "CAN": 100,
    "CHE": 100, "CHL": 96, "CHN": 89, "CIV": 90, "CMR": 77, "COD": 53, "COG": 41, "COL": 85, "COM": 70, "CPV": 100,
    "CRI": 99, "CUB": 92, "CYP": 100, "CZE": 100, "DEU": 100, "DJI": 79, "DMA": 99, "DNK": 99, "DOM": 97, "DZA": 90,
    "ECU": 94, "EGY": 96, "ERI": 47, "ESH": 61, "ESP": 100, "EST": 100, "ETH": 63, "FIN": 100, "FJI": 97, "FRA": 98,
    "FSM": 72, "GAB": 67, "GBR": 100, "GEO": 75, "GHA": 93, "GIN": 71, "GMB": 86, "GNB": 73, "GNQ": 85, "GRC": 100,
    "GRD": 100, "GTM": 97, "GUY": 81, "HND": 95, "HRV": 100, "HTI": 80, "HUN": 100, "IDN": 92, "IND": 99, "IRL": 100,
    "IRN": 80, "IRQ": 84, "ISL": 92, "ISR": 100, "ITA": 100, "JAM": 100, "JOR": 96, "JPN": 100, "KAZ": 72, "KEN": 87,
    "KGZ": 78, "KHM": 95, "KNA": 100, "KOR": 100, "KWT": 86, "LAO": 95, "LBN": 100, "LBR": 58, "LBY": 79, "LCA": 100,
    "LIE": 100, "LKA": 100, "LSO": 77, "LTU": 100, "LUX": 100, "LVA": 100, "MAR": 99, "MDA": 100, "MDG": 49, "MDV": 94,
    "MEX": 99, "MHL": 86, "MKD": 99, "MLI": 72, "MLT": 100, "MMR": 84, "MNE": 99, "MNG": 76, "MOZ": 56, "MRT": 57,
    "MUS": 100, "MWI": 72, "MYS": 98, "NER": 65, "NGA": 91, "NIC": 88, "NLD": 100, "NOR": 97, "NPL": 81, "NZL": 100,
    "OMN": 85, "PAK": 88, "PAN": 91, "PER": 84, "PHL": 98, "PLW": 99, "PNG": 43, "POL": 100, "PRK": 76, "PRT": 100,
    "PRY": 98, "QAT": 100, "ROU": 100, "RUS": 95, "RWA": 79, "SAU": 67, "SDN": 56, "SEN": 89, "SGP": 98, "SLB": 55,
    "SLE": 72, "SLV": 99, "SMR": 95, "SOM": 64, "SRB": 96, "SSD": 27, "STP": 74, "SUR": 82, "SVK": 100, "SVN": 100,
    "SWE": 100, "SWZ": 99, "SYC": 100, "SYR": 85, "TCD": 43, "TGO": 78, "THA": 98, "TJK": 80, "TKM": 63, "TLS": 82,
    "TON": 100, "TTO": 98, "TUN": 98, "TUR": 98, "TZA": 74, "UGA": 76, "UKR": 100, "URY": 100, "USA": 100, "UZB": 89,
    "VCT": 95, "VEN": 78, "VNM": 98, "VUT": 66, "WSM": 92, "YEM": 65, "ZAF": 99, "ZMB": 68, "ZWE": 76,
}
# Pays des hubs (noms français de la flotte) vers ISO 3166-1 alpha-3.
PAYS_VERS_ISO = {
    "Afghanistan": "AFG", "Afrique du Sud": "ZAF", "Algérie": "DZA",
    "Allemagne": "DEU", "Angola": "AGO", "Arabie Saoudite": "SAU",
    "Argentine": "ARG", "Australie": "AUS", "Autriche": "AUT",
    "Azerbaïdjan": "AZE", "Bangladesh": "BGD", "Belgique": "BEL",
    "Belize": "BLZ", "Biélorussie": "BLR", "Bolivie": "BOL",
    "Botswana": "BWA", "Brésil": "BRA", "Bulgarie": "BGR",
    "Burkina Faso": "BFA", "Burundi": "BDI", "Bénin": "BEN",
    "Cambodge": "KHM", "Cameroun": "CMR", "Canada": "CAN", "Chili": "CHL",
    "Chine": "CHN", "Chypre": "CYP", "Colombie": "COL", "Congo": "COG",
    "Corée du Sud": "KOR", "Costa Rica": "CRI", "Cuba": "CUB",
    "Côte d'Ivoire": "CIV", "Danemark": "DNK", "El Salvador": "SLV",
    "Espagne": "ESP", "Estonie": "EST", "Finlande": "FIN", "France": "FRA",
    "Gabon": "GAB", "Gambie": "GMB", "Ghana": "GHA", "Grèce": "GRC",
    "Guatemala": "GTM", "Guinée": "GIN", "Guinée-Bissau": "GNB",
    "Guyana": "GUY", "Géorgie": "GEO", "Haïti": "HTI", "Honduras": "HND",
    "Hongrie": "HUN", "Inde": "IND", "Indonésie": "IDN", "Irak": "IRQ",
    "Iran": "IRN", "Irlande": "IRL", "Israël": "ISR", "Italie": "ITA",
    "Jamaïque": "JAM", "Japon": "JPN", "Jordanie": "JOR",
    "Kazakhstan": "KAZ", "Kenya": "KEN", "Kirghizistan": "KGZ",
    "Koweït": "KWT", "Laos": "LAO", "Lettonie": "LVA", "Liban": "LBN",
    "Liberia": "LBR", "Libye": "LBY", "Lituanie": "LTU",
    "Madagascar": "MDG", "Malaisie": "MYS", "Malawi": "MWI", "Mali": "MLI",
    "Maroc": "MAR", "Maurice": "MUS", "Mauritanie": "MRT", "Mexique": "MEX",
    "Moldavie": "MDA", "Mozambique": "MOZ", "Myanmar": "MMR",
    "Nicaragua": "NIC", "Niger": "NER", "Nigeria": "NGA",
    "Norvège": "NOR", "Nouvelle-Zélande": "NZL", "Népal": "NPL",
    "Oman": "OMN", "Ouganda": "UGA", "Ouzbékistan": "UZB",
    "Pakistan": "PAK", "Panama": "PAN", "Paraguay": "PRY",
    "Pays-Bas": "NLD", "Philippines": "PHL", "Pologne": "POL",
    "Portugal": "PRT", "Pérou": "PER", "Qatar": "QAT", "RDC": "COD",
    "Roumanie": "ROU", "Royaume-Uni": "GBR", "Russie": "RUS",
    "Rwanda": "RWA", "Rép. dominicaine": "DOM", "Serbie": "SRB",
    "Sierra Leone": "SLE", "Slovaquie": "SVK", "Somalie": "SOM",
    "Soudan": "SDN", "Soudan du Sud": "SSD", "Sri Lanka": "LKA",
    "Suisse": "CHE", "Suriname": "SUR", "Suède": "SWE", "Syrie": "SYR",
    "Sénégal": "SEN", "Tadjikistan": "TJK", "Tanzanie": "TZA",
    "Tchad": "TCD", "Tchéquie": "CZE", "Thaïlande": "THA", "Togo": "TGO",
    "Trinité-et-Tobago": "TTO", "Tunisie": "TUN", "Turkménistan": "TKM",
    "Turquie": "TUR", "Ukraine": "UKR", "Uruguay": "URY",
    "Venezuela": "VEN", "Viêt Nam": "VNM", "Yémen": "YEM", "Zambie": "ZMB",
    "Zimbabwe": "ZWE", "Égypte": "EGY",
    "Émirats arabes unis": "ARE", "Équateur": "ECU", "États-Unis": "USA",
    "Éthiopie": "ETH",
}

# Jetons des deux hubs pilotes (convention data/carte-monde.json)
JETONS_PILOTES = {
    "fr-rhone": ["SARMENT_VIGNE_FR", "MARC_RAISIN_FR", "RAFLE_MAIS_FR",
                 "PAILLE_RIZ_FR", "COQUE_NOIX_FR"],
    "ma-atlas": ["GRIGNONS_OLIVE_MA"],
}

_MEMO_FAMILLE = {}
_MEMO_HUBS = None


def famille_du_token(token):
    """Première famille dont un motif matche le jeton (ordre = priorité)."""
    if token in _MEMO_FAMILLE:
        return _MEMO_FAMILLE[token]
    resultat = None
    for (famille, _type, _cap, _ener, _fen, motifs, _note, _stat) in \
            FAMILLES_SITES:
        if any(m in token for m in motifs):
            resultat = famille
            break
    _MEMO_FAMILLE[token] = resultat
    return resultat


def _fiche_famille(famille):
    for f in FAMILLES_SITES:
        if f[0] == famille:
            return f
    return None


def hubs_avec_jetons():
    """{hub: (pays, [jetons])} — 217 généralisés + 2 pilotes."""
    global _MEMO_HUBS
    if _MEMO_HUBS is not None:
        return _MEMO_HUBS
    import sourcing_p3  # noqa: E402 (engine/)
    import flotte_monde  # noqa: E402 (engine/)
    gen, _, _ = flotte_monde.hubs_generalises()
    resultat = {}
    for hid, h in sourcing_p3.hubs().items():
        if h.get("hub_pilote"):
            jetons = list(JETONS_PILOTES.get(hid, []))
        else:
            jetons = list(gen[hid]["_meta"]["clusters"])
        resultat[hid] = (h["pays"], jetons)
    _MEMO_HUBS = resultat
    return resultat


def fiche_hub(hid):
    """Attributs de site d'un hub : type, familles, captabilité, énergie,
    fenêtre, LPI. Aucune coordonnée, aucun coût."""
    entrees = hubs_avec_jetons()
    if hid not in entrees:
        return None
    pays, jetons = entrees[hid]
    familles = {}
    jetons_sans_famille = []
    for t in jetons:
        f = famille_du_token(t)
        if f is None:
            jetons_sans_famille.append(t)
        else:
            familles.setdefault(f, 0)
            familles[f] += 1
    if jetons_sans_famille:
        raise RuntimeError(
            "jetons sans famille de site (%s) : %s — compléter FAMILLES_SITES"
            % (hid, ", ".join(jetons_sans_famille)))
    iso = PAYS_VERS_ISO.get(pays)
    lpi = LPI_2023.get(iso) if iso else None
    lpi_edition = 2023 if lpi is not None else None
    if lpi is None and iso in LPI_EDITIONS_ANTERIEURES:
        lpi_edition, lpi = LPI_EDITIONS_ANTERIEURES[iso]
    lpi_proxy = False
    nb_enquetes, region_lpi = None, None
    if lpi is None and iso in LPI_MOYENNES_REGIONALES:
        lpi, nb_enquetes, region_lpi = LPI_MOYENNES_REGIONALES[iso]
        lpi_edition = 2023
        lpi_proxy = True
    rai = RAI_2023.get(iso) if iso else None
    # famille dominante : captabilité la plus élevée, égalité par ordre
    ordre = {f[0]: i for i, f in enumerate(FAMILLES_SITES)}
    dominant = max(sorted(familles), key=lambda f: (
        _fiche_famille(f)[2], -ordre[f]))
    fd = _fiche_famille(dominant)
    captabilite = round(sum(
        _fiche_famille(f)[2] * n for f, n in familles.items()
    ) / sum(familles.values()), 2)
    energie = ("AUTONOME"
               if any(_fiche_famille(f)[3] == "AUTONOME" for f in familles)
               else "IMPORTATEUR")
    cap_sourcee = all(_fiche_famille(f)[7] == "SOURCÉ" for f in familles)
    return {
        "hub": hid,
        "pays": pays,
        "iso": iso,
        "type_site": fd[1],
        "famille_dominante": dominant,
        "familles": "+".join(sorted(familles, key=lambda f: ordre[f])),
        "nb_jetons": len(jetons),
        "captabilite": captabilite,
        "energie_site": energie,
        "fenetre_fraicheur": fd[4],
        "lpi_2023": lpi,
        "lpi_edition": lpi_edition,
        "lpi_statut": ("RÉGIONAL (proxy : moyenne simple des %d pays"
                       " enquêtés de la région %s, jamais enquêté)"
                       % (nb_enquetes, region_lpi)
                       if lpi_proxy
                       else ("SOURCÉ (Banque mondiale, LPI %d)"
                             % lpi_edition
                             if lpi is not None
                             else "A_SOURCER (jamais enquêté,"
                                  " aucune édition du LPI)")),
        "lpi_proxy": lpi_proxy,
        "rai_2023": rai,
        "rai_statut": ("SOURCÉ (SDSN SDG Transformation Center, indicateur "
                       "ODD 9.1.1, d'après Banque mondiale)" if rai is not None
                       else "A_SOURCER (pays absent du jeu 2022-2023)"),
        "captabilite_statut": ("SOURCÉ (toutes les familles du hub sont "
                               "chiffrées par la littérature)" if cap_sourcee
                               else "ILLUSTRATION (au moins une famille non "
                               "chiffrée par la littérature)"),
        "etiquette": ("SYNTHÉTIQUE — captabilités par famille SOURCÉ/"
                      "ILLUSTRATION, LPI et RAI SOURCÉS"),
    }


def couches():
    """Couche compacte des 219 hubs pour les cartes interactives."""
    resultat = {}
    for hid in sorted(hubs_avec_jetons()):
        f = fiche_hub(hid)
        resultat[hid] = {
            "pays": f["pays"],
            "type_site": f["type_site"],
            "familles": f["familles"],
            "captabilite": f["captabilite"],
            "energie_site": f["energie_site"],
            "fenetre": f["fenetre_fraicheur"],
            "lpi": f["lpi_2023"],
            "lpi_edition": f["lpi_edition"],
            "lpi_proxy": f["lpi_proxy"],
            "rai": f["rai_2023"],
            "cap_statut": f["captabilite_statut"].split(" (")[0],
        }
        # V2.8 : les 3 hubs jamais enquêtés portent le détail du proxy
        # régional (moyenne simple des pays enquêtés de la région).
        if f["lpi_proxy"]:
            resultat[hid]["lpi_detail"] = f["lpi_statut"]
    return resultat


def sommaire():
    lignes = [
        "World Twin v2.8 — sites de transformation post-récolte",
        "=====================================================",
        "",
        "Quatre attributs sur 219 hubs (217 généralisés + 2 pilotes),",
        "aucune coordonnée modifiée, aucun figeage touché :",
        "",
        "1. TYPE_SITE — site de transformation dominant du cluster ;",
        "2. CAPTABILITE — fraction du gisement disponible au site",
        "   (statut SOURCÉ ou ILLUSTRATION par famille) ;",
        "3. ENERGIE_SITE — AUTONOME (le site vend) contre IMPORTATEUR ;",
        "4. LOGISTIQUE — LPI (édition 2023 ou la plus récente",
        "   disponible, proxy régional pour les 3 jamais enquêtés)",
        "   et RAI 2023 SOURCÉS (Banque mondiale, SDSN ; indicateur",
        "   ODD 9.1.1 pour le RAI).",
        "",
        "Familles de sites : %d" % len(FAMILLES_SITES),
    ]
    for (famille, type_site, cap, ener, _fen, motifs, _note, statut) in \
            FAMILLES_SITES:
        lignes.append("- %-15s %-28s cap. %.2f %-11s [%d motif(s)] %s"
                      % (famille, type_site, cap, ener, len(motifs), statut))
    entrees = hubs_avec_jetons()
    lignes.append("")
    lignes.append("Hubs : %d — pays couverts : %d"
                  % (len(entrees), len({p for p, _ in entrees.values()})))
    avec_lpi = sum(1 for hid in entrees
                   if fiche_hub(hid)["lpi_2023"] is not None)
    avec_proxy = sum(1 for hid in entrees
                     if fiche_hub(hid)["lpi_proxy"])
    lignes.append("LPI disponible : %d hubs SOURCÉ, %d RÉGIONAL"
                  " (proxy), %d À SOURCER"
                  % (avec_lpi - avec_proxy, avec_proxy,
                     len(entrees) - avec_lpi))
    avec_rai = sum(1 for hid in entrees
                   if fiche_hub(hid)["rai_2023"] is not None)
    lignes.append("RAI 2023 disponible : %d hubs SOURCÉ, %d À SOURCER "
                  "(SDSN, indicateur ODD 9.1.1)"
                  % (avec_rai, len(entrees) - avec_rai))
    caps = sum(1 for hid in entrees
               if fiche_hub(hid)["captabilite_statut"].startswith("SOURCÉ"))
    lignes.append("Captabilités : %d hubs SOURCÉ (toutes familles chiffrées), "
                  "%d ILLUSTRATION" % (caps, len(entrees) - caps))
    lignes.append("")
    lignes.append("Commandes : sommaire | fiche HUB | verifier | table")
    return "\n".join(lignes)


def verifier():
    """Contrôles : couverture des jetons, bornes, LPI, anti-fuite."""
    erreurs = []
    entrees = hubs_avec_jetons()
    if len(entrees) != 219:
        erreurs.append("hubs attendus : 219, trouvés : %d" % len(entrees))
    jetons_vus = set()
    familles_hubs = {}
    for hid, (pays, jetons) in sorted(entrees.items()):
        f = fiche_hub(hid)
        if f is None:
            erreurs.append("hub sans fiche : %s" % hid)
            continue
        jetons_vus.update(jetons)
        for fam in f["familles"].split("+"):
            familles_hubs.setdefault(fam, 0)
            familles_hubs[fam] += 1
        if not (0.0 <= f["captabilite"] <= 1.0):
            erreurs.append("captabilité hors bornes : %s" % hid)
        if f["iso"] is None:
            erreurs.append("pays sans ISO : %s (%s)" % (hid, pays))
        if f["energie_site"] not in ("AUTONOME", "IMPORTATEUR"):
            erreurs.append("énergie inconnue : %s" % hid)
        if not f["type_site"] or not f["familles"]:
            erreurs.append("attributs vides : %s" % hid)
    sans_famille = sorted(t for t in jetons_vus if famille_du_token(t) is None)
    if sans_famille:
        erreurs.append("jetons sans famille : %s" % ", ".join(sans_famille))
    pilotes = sorted(h for h, (_, j) in entrees.items() if not j)
    if pilotes:
        erreurs.append("hubs sans jetons : %s" % ", ".join(pilotes))
    # anti-fuite : ce module ne doit porter aucun jeton économique
    for interdit in ("cout", "prix", "plan_achat", "eur_t", "eur_an",
                     "marche_externe", "deficit", "€"):
        if interdit in json.dumps(couches()):
            erreurs.append("fuite de jeton économique : %s" % interdit)
    stats_lpi = {}
    stats_rai = {}
    stats_cap = {}
    stats_lpi_editions = {}
    for hid, (pays, _j) in entrees.items():
        f = fiche_hub(hid)
        stats_lpi[f["lpi_statut"].split(" (")[0]] = \
            stats_lpi.get(f["lpi_statut"].split(" (")[0], 0) + 1
        stats_rai[f["rai_statut"].split(" (")[0]] = \
            stats_rai.get(f["rai_statut"].split(" (")[0], 0) + 1
        stats_cap[f["captabilite_statut"].split(" (")[0]] = \
            stats_cap.get(f["captabilite_statut"].split(" (")[0], 0) + 1
        if f["lpi_edition"] is not None:
            stats_lpi_editions[f["lpi_edition"]] = \
                stats_lpi_editions.get(f["lpi_edition"], 0) + 1
    lignes = [
        "VERIFICATEUR SITES V2.8",
        "hubs : %d (attendu 219)" % len(entrees),
        "jetons couverts : %d — familles actives : %s"
        % (len(jetons_vus), ", ".join(
            "%s=%d" % kv for kv in sorted(familles_hubs.items()))),
        "LPI : %s (éditions enquêtées : %s)" % (
            ", ".join("%s=%d" % kv for kv in sorted(stats_lpi.items())),
            ", ".join("LPI %s=%d" % kv
                      for kv in sorted(stats_lpi_editions.items()))),
        "RAI 2023 : %s" % ", ".join("%s=%d" % kv
                                    for kv in sorted(stats_rai.items())),
        "captabilités : %s" % ", ".join("%s=%d" % kv
                                       for kv in sorted(stats_cap.items())),
        "flotte : module sans effet sur figeages et coordonnées (proxys",
        "régionaux LPI V2.8 et captabilités V2.8 : aucun gisement ne",
        "bouge, voir les verifiers dédiés)",
        "VERDICT : %s (%d erreur(s))"
        % ("OK" if not erreurs else "ÉCHEC", len(erreurs)),
    ]
    if erreurs:
        lignes.extend("  - %s" % e for e in erreurs)
    return "\n".join(lignes)


def table():
    lignes = ["%-24s %-14s %-28s %6s %-11s %6s %s"
              % ("hub", "pays", "type de site", "cap.", "énergie", "LPI",
                 "RAI 2023")]
    for hid in sorted(hubs_avec_jetons()):
        f = fiche_hub(hid)
        lignes.append("%-24s %-14s %-28s %6.2f %-11s %6s %s"
                      % (hid, f["pays"][:14], f["type_site"][:28],
                         f["captabilite"], f["energie_site"],
                         f["lpi_2023"] if f["lpi_2023"] else "-",
                         "%s %%" % f["rai_2023"]
                         if f["rai_2023"] is not None else "A_SOURCER"))
    return "\n".join(lignes)


def main():
    args = list(sys.argv[1:])
    if not args or args[0] == "sommaire":
        print(sommaire())
    elif args[0] == "verifier":
        print(verifier())
    elif args[0] == "table":
        print(table())
    elif args[0] == "fiche" and len(args) > 1:
        f = fiche_hub(args[1])
        print(json.dumps(f, ensure_ascii=False, indent=2) if f
              else "hub inconnu : %s" % args[1])
    elif args[0] == "couches":
        print(json.dumps(couches(), ensure_ascii=False, indent=2))
    else:
        print("commande inconnue : %s" % " ".join(args))
        print("attendu : sommaire | fiche HUB | verifier | table | couches")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
