# Atlas des biomasses d'Asie — World Twin v1.3

Vague du 31/10/2026 (régénération). Vingt-trois pays d'Asie non encore couverts, soixante-douze intrants placés — productions ancrées sur le bulk FAOSTAT 2024 (base statistique de l'Organisation des Nations unies pour l'alimentation et l'agriculture, licence CC BY 4.0), ratios résidus ILLUSTRATION, fenêtres saisonnières sous garde, réglementation à cinq postes À VÉRIFIER. Étiquette SYNTHÉTIQUE au registre de développement uniquement.

## Doctrine et étiquettes

- Ce document n'embarque aucun des six paramètres du VDE (Vignite Decision Engine) et aucune valeur calibrée.
- Productions nationales : SOURCÉ (bulk FAOSTAT 2024).
- Ratios de résidus : ILLUSTRATION (conventions figées, à borner localement).
- Réglementation : À VÉRIFIER (aucun de ces vingt-trois pays n'est couvert par les fiches v0.6 des sept hubs).
- Points GPS (Global Positioning System) : approximations de région, jamais un cadastre.

## Méthode

- Base : bulk normalisé « Production_Crops_Livestock_E » (33 921 825 octets, md5 1a202c5674dce152f1134fa87b220b82), éléments Production et Area harvested, année 2024, licence CC BY 4.0, attribution FAOSTAT.
- Les productions affichées sont les valeurs nationales 2024 du bulk, sans recalage.
- Gisements documentaires = production × ratio ILLUSTRATION, conventions listées dans le module.
- Les fenêtres saisonnières sont ILLUSTRATION, mises sous garde par préfixe de jeton.
- Périmètre figé v1.3 : familles Céréales et Tropical uniquement — la famille Coques et noyaux n'existe pas dans le master v1.0, d'où l'écart historique de 79 contre 72 intrants tracé à la conception.
- Croisement de cohérence contre le master v1.0 et les atlas v1.1 et v1.2 : familles, collisions de jetons, gardes saisonnières, boîtes englobantes.

## Pièges de nommage FAOSTAT (consignés)

Items (le bulk écrase ses libellés, chaque extraction doit re-vérifier) :
- « Rice » — pas de suffixe paddy
- « Maize (corn) »
- « Cassava, fresh »
- « Tea leaves »
- « Seed cotton, unginned »
- « Jute, raw or retted »
- « Dates »
Pays :
- « Türkiye » — avec tréma
- « Republic of Korea »
- « Lao People's Democratic Republic »
- « Iran (Islamic Republic of) »
- « Syrian Arab Republic »
- « Iraq » — sans i final
- « Russian Federation »
Le pivot pays « China, mainland » est hors du périmètre v1.3 (Chine déjà couverte par la v1.1).

## Gardes nouvelles de la v1.3

- REGLES_SAISON : par préfixe de jeton, mois autorisés pour la fenêtre des points hors ceinture tropicale (latitude absolue supérieure à 23,5). Cinquante-quatre points sont sous garde, dix-huit points tropicaux sont exemptés (production continue).
- BBOX_ASIE : boîte englobante par pays (latitude et longitude minimales et maximales), chaque point doit y rester — garde anti-coquille GPS (Global Positioning System). Pièges consignés : Panjakent (Tadjikistan) est à la longitude 67,32, la boîte tadjike commence donc à 67 — Chelyabinsk (Russie) est à la longitude 61,40, dans la boîte russe bornée à 65.

Règles saisonnières par préfixe (mois autorisés, hors ceinture tropicale) :

| Préfixe | Mois autorisés |
| --- | --- |
| PAILLE_BLE | 3, 4, 5, 6, 7, 8, 9, 10, 11  |
| PAILLE_ORGE | 3, 4, 5, 6, 7, 8, 9, 10, 11  |
| PAILLE_AVOINE | 7, 8, 9  |
| PAILLE_MAIS | 8, 9, 10, 11, 12  |
| BALLE_RIZ | 1, 2, 3, 4, 5, 9, 10, 11, 12  |
| BAGASSE_CANNE | 10, 11, 12, 1, 2, 3, 4, 5, 6  |
| TIGE_COTON | 9, 10, 11, 12, 1  |
| TIGE_TOURNESOL | 8, 9, 10, 11  |
| TIGE_JUTE | 6, 7, 8, 9  |
| RACHIS_DATTIER | 3, 4, 5  |
| RESIDU_THE | 4, 5, 6, 7, 8, 9, 10, 11  |
| EFB_PALMIER | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 production continue (tropical) |
| ECORCE_MANIOC | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 production continue (tropical) |

## Synthèse des 23 pays

| Pays | Nom FAOSTAT | Intrants | Point emblématique | Gisement majeur |
| --- | --- | --- | --- | --- |
| Afghanistan | Afghanistan | 3 | Herat (bassin céréalier de l'Ouest) | paille ≈ 6,2 Mt/an |
| Azerbaïdjan | Azerbaijan | 3 | Barda (coton du bas-Kura) | paille ≈ 2,3 Mt/an |
| Bangladesh | Bangladesh | 4 | Faridpur (bassin jutier du delta) | balle ≈ 12,1 Mt/an |
| Cambodge | Cambodia | 2 | Battambang (bassin du Tonlé Sap) | balle ≈ 2,8 Mt/an |
| Corée du Sud | Republic of Korea | 2 | Jeonju (Jeolla, rizière du Sud-Ouest) | balle ≈ 956 623 t/an |
| Indonésie | Indonesia | 5 | Riau (bassin palmier de Sumatra) | rafles ≈ 53,5 Mt/an |
| Iran | Iran (Islamic Republic of) | 4 | Gorgan (bassin de la Caspienne) | paille ≈ 20,1 Mt/an |
| Irak | Iraq | 2 | Basra (vergers dattiers du Chatt al-Arab) | paille ≈ 6,3 Mt/an |
| Japon | Japan | 2 | Niigata (plaine du Shinano) | balle ≈ 2 Mt/an |
| Kazakhstan | Kazakhstan | 4 | Kokshetau (Akmola, steppe céréalière) | paille ≈ 22,3 Mt/an |
| Kirghizistan | Kyrgyzstan | 3 | Jalal-Abad (vallée de Ferghana kirghize) | paille ≈ 797 796 t/an |
| Laos | Lao People's Democratic Republic | 2 | Savannakhet (bassin du Mékong) | écorces ≈ 1,1 Mt/an |
| Myanmar | Myanmar | 3 | Bogale (delta de l'Ayeyarwady) | balle ≈ 5,5 Mt/an |
| Népal | Nepal | 3 | Chitwan (Terai central) | paille ≈ 2,4 Mt/an |
| Ouzbékistan | Uzbekistan | 2 | Ferghana (vallée cotonnière) | tiges de coton ≈ 8,8 Mt/an |
| Pakistan | Pakistan | 3 | Multan (ceinture cotonnière du Pendjab) | paille ≈ 38,2 Mt/an |
| Russie | Russian Federation | 5 | Krasnodar (Kouban) | paille ≈ 99,1 Mt/an |
| Sri Lanka | Sri Lanka | 2 | Kandy (hauts plateaux théicoles) | balle ≈ 939 691 t/an |
| Syrie | Syrian Arab Republic | 2 | Hasakah (Djéziré, blé du Nord-Est) | paille ≈ 2,9 Mt/an |
| Tadjikistan | Tajikistan | 2 | Panjakent (vallée de Sughd) | paille ≈ 1,1 Mt/an |
| Thaïlande | Thailand | 4 | Chainat (bassin de la Chao Phraya) | bagasse ≈ 24,7 Mt/an |
| Turkménistan | Turkmenistan | 2 | Mary (oasis cotonnière du Karakoum) | tiges de coton ≈ 1,8 Mt/an |
| Turquie | Türkiye | 8 | Konya (steppe céréalière anatolienne) | paille ≈ 25 Mt/an |

## Les 72 intrants

| Jeton | Famille | Région | GPS (Global Positioning System) | Fenêtre | Gisement |
| --- | --- | --- | --- | --- | --- |
| EFB_PALMIER_ID | Tropical | Riau (bassin palmier de Sumatra) | 0.53, 101.44 | janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc | rafles ≈ 53,5 Mt/an |
| BALLE_RIZ_ID | Céréales | Karawang (rizière de Java Ouest) | -6.30, 107.32 | janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc | balle ≈ 10,6 Mt/an |
| BAGASSE_CANNE_ID | Tropical | Lampung (bassin sucrier du Sud) | -5.40, 105.33 | mai-juin-juil-août-sept-oct-nov-déc | bagasse ≈ 9,6 Mt/an |
| ECORCE_MANIOC_ID | Tropical | Grobogan (bassin manioc de Java Centre) | -7.08, 110.82 | janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc | écorces ≈ 2,3 Mt/an |
| PAILLE_MAIS_ID | Céréales | Jember (Java Est) | -8.20, 113.70 | janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc | résidus de maïs ≈ 3,8 Mt/an |
| TIGE_COTON_PK | Céréales | Multan (ceinture cotonnière du Pendjab) | 30.20, 71.47 | nov-déc-janv | tiges de coton ≈ 10,5 Mt/an |
| BAGASSE_CANNE_PK | Tropical | Matiari (bassin sucrier du Sindh) | 25.60, 68.45 | nov-déc-janv-févr-mars | bagasse ≈ 25,3 Mt/an |
| PAILLE_BLE_PK | Céréales | Sahiwal (bassin céréalier du Pendjab) | 30.67, 73.11 | avr-mai | paille ≈ 38,2 Mt/an |
| BALLE_RIZ_TH | Céréales | Chainat (bassin de la Chao Phraya) | 15.20, 100.10 | nov-déc-janv-févr-mars-avr | balle ≈ 6,7 Mt/an |
| ECORCE_MANIOC_TH | Tropical | Nakhon Ratchasima (bassin manioc de l'Isan) | 14.97, 102.10 | janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc | écorces ≈ 4,3 Mt/an |
| BAGASSE_CANNE_TH | Tropical | Khon Kaen (bassin sucrier du Nord-Est) | 16.43, 102.83 | nov-déc-janv-févr-mars | bagasse ≈ 24,7 Mt/an |
| EFB_PALMIER_TH | Tropical | Krabi (bassin palmier du Sud) | 8.11, 98.90 | janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc | rafles ≈ 4,1 Mt/an |
| BALLE_RIZ_MM | Céréales | Bogale (delta de l'Ayeyarwady) | 16.30, 95.10 | nov-déc-janv-févr-mars-avr | balle ≈ 5,5 Mt/an |
| PAILLE_MAIS_MM | Céréales | Taunggyi (plateaux des états Shan) | 20.78, 97.04 | août-sept-oct | résidus de maïs ≈ 512 500 t/an |
| BAGASSE_CANNE_MM | Tropical | Monywa (vallée de la Chindwin) | 22.00, 95.13 | nov-déc-janv-févr-mars | bagasse ≈ 3,6 Mt/an |
| TIGE_JUTE_BD | Céréales | Faridpur (bassin jutier du delta) | 23.60, 89.83 | juil-août-sept | tiges de jute ≈ 3,8 Mt/an |
| BALLE_RIZ_BD | Céréales | Mymensingh (rizière du Bengale) | 24.75, 90.40 | nov-déc-janv-févr-mars-avr | balle ≈ 12,1 Mt/an |
| PAILLE_MAIS_BD | Céréales | Rangpur (bassin maïsier du Nord) | 25.75, 89.25 | oct-nov | résidus de maïs ≈ 1,1 Mt/an |
| PAILLE_BLE_BD | Céréales | Dinajpur (bassin céréalier du Nord) | 25.62, 88.64 | mars-avr | paille ≈ 1,4 Mt/an |
| BALLE_RIZ_NP | Céréales | Chitwan (Terai central) | 27.53, 84.35 | oct-nov-déc | balle ≈ 1,2 Mt/an |
| PAILLE_MAIS_NP | Céréales | Dang (vallées du mid-West) | 28.10, 82.30 | sept-oct-nov | résidus de maïs ≈ 798 467 t/an |
| PAILLE_BLE_NP | Céréales | Rupandehi (Terai ouest) | 27.52, 83.28 | mars-avr-mai | paille ≈ 2,4 Mt/an |
| RESIDU_THE_LK | Tropical | Kandy (hauts plateaux théicoles) | 7.29, 80.64 | janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc | résidus de théier ≈ 161 000 t/an |
| BALLE_RIZ_LK | Céréales | Polonnaruwa (rizière du Mahaweli) | 7.93, 81.02 | mars-avr-août-sept | balle ≈ 939 691 t/an |
| BALLE_RIZ_KH | Céréales | Battambang (bassin du Tonlé Sap) | 13.10, 103.20 | nov-déc-janv-févr-mars | balle ≈ 2,8 Mt/an |
| ECORCE_MANIOC_KH | Tropical | Kampong Cham (bassin manioc de l'Est) | 12.00, 105.46 | janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc | écorces ≈ 2,1 Mt/an |
| BALLE_RIZ_LA | Céréales | Savannakhet (bassin du Mékong) | 16.60, 104.75 | nov-déc-janv-févr-mars | balle ≈ 750 148 t/an |
| ECORCE_MANIOC_LA | Tropical | Vientiane (plaines du Mékong) | 18.20, 102.80 | janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc | écorces ≈ 1,1 Mt/an |
| BALLE_RIZ_JP | Céréales | Niigata (plaine du Shinano) | 37.92, 139.05 | sept-oct-nov | balle ≈ 2 Mt/an |
| PAILLE_BLE_JP | Céréales | Obihiro (Tokachi, Hokkaido) | 42.92, 143.20 | juil-août | paille ≈ 1,2 Mt/an |
| BALLE_RIZ_KR | Céréales | Jeonju (Jeolla, rizière du Sud-Ouest) | 35.82, 127.15 | oct-nov | balle ≈ 956 623 t/an |
| PAILLE_ORGE_KR | Céréales | Iksan (Jeolla, orge d'hiver) | 35.94, 126.95 | mai-juin | paille ≈ 47 730 t/an |
| PAILLE_BLE_KZ | Céréales | Kokshetau (Akmola, steppe céréalière) | 53.29, 69.42 | août-sept | paille ≈ 22,3 Mt/an |
| PAILLE_ORGE_KZ | Céréales | Kostanay (steppe du Nord) | 53.22, 63.62 | août-sept | paille ≈ 3,8 Mt/an |
| TIGE_TOURNESOL_KZ | Céréales | Petropavl (Kazakhstan du Nord) | 54.87, 69.18 | sept-oct | tiges de tournesol ≈ 3,7 Mt/an |
| TIGE_COTON_KZ | Céréales | Turkestan (oasis cotonnière du Sud) | 43.29, 68.25 | oct-nov | tiges de coton ≈ 904 984 t/an |
| TIGE_COTON_UZ | Céréales | Ferghana (vallée cotonnière) | 40.38, 71.78 | oct-nov | tiges de coton ≈ 8,8 Mt/an |
| PAILLE_BLE_UZ | Céréales | Samarcande (oasis céréalière) | 39.65, 66.96 | juin-juil | paille ≈ 8,1 Mt/an |
| TIGE_COTON_TM | Céréales | Mary (oasis cotonnière du Karakoum) | 37.61, 61.83 | oct-nov | tiges de coton ≈ 1,8 Mt/an |
| PAILLE_BLE_TM | Céréales | Dashoguz (oasis céréalière du Nord) | 41.43, 59.91 | juin-juil | paille ≈ 1,6 Mt/an |
| TIGE_COTON_TJ | Céréales | Panjakent (vallée de Sughd) | 39.51, 67.32 | oct-nov | tiges de coton ≈ 759 546 t/an |
| PAILLE_BLE_TJ | Céréales | Hisor (vallée de Douchanbé) | 38.53, 68.79 | juin-juil | paille ≈ 1,1 Mt/an |
| TIGE_COTON_KG | Céréales | Jalal-Abad (vallée de Ferghana kirghize) | 40.93, 72.78 | oct-nov | tiges de coton ≈ 139 014 t/an |
| PAILLE_BLE_KG | Céréales | Chuy (vallée de Bichkek) | 42.87, 74.59 | juil-août | paille ≈ 797 796 t/an |
| PAILLE_ORGE_KG | Céréales | Talas (vallée du Nord-Ouest) | 42.52, 72.24 | juin-juil | paille ≈ 611 050 t/an |
| TIGE_COTON_AZ | Céréales | Barda (coton du bas-Kura) | 40.39, 47.13 | oct-nov | tiges de coton ≈ 712 953 t/an |
| PAILLE_BLE_AZ | Céréales | Ganja (bassin céréalier de l'Ouest) | 40.68, 46.36 | juin-juil | paille ≈ 2,3 Mt/an |
| PAILLE_ORGE_AZ | Céréales | Qazax (piémonts du Nord-Ouest) | 41.10, 45.36 | mai-juin | paille ≈ 1,1 Mt/an |
| PAILLE_BLE_AF | Céréales | Herat (bassin céréalier de l'Ouest) | 34.34, 62.21 | mai-juin-juil | paille ≈ 6,2 Mt/an |
| BALLE_RIZ_AF | Céréales | Kunduz (rizière du Nord) | 36.72, 68.86 | oct-nov | balle ≈ 130 800 t/an |
| TIGE_COTON_AF | Céréales | Taloqan (Takhar, coton du Nord) | 36.70, 69.53 | nov-déc | tiges de coton ≈ 361 524 t/an |
| RACHIS_DATTIER_IQ | Tropical | Basra (vergers dattiers du Chatt al-Arab) | 30.51, 47.78 | mars-avr-mai | palmes et rachis ≈ 642 000 t/an |
| PAILLE_BLE_IQ | Céréales | Diyala (bassin céréalier de l'Est) | 33.75, 44.52 | avr-mai | paille ≈ 6,3 Mt/an |
| PAILLE_BLE_SY | Céréales | Hasakah (Djéziré, blé du Nord-Est) | 36.51, 40.75 | mai-juin | paille ≈ 2,9 Mt/an |
| PAILLE_ORGE_SY | Céréales | Alep (bassin orge de l'Ouest) | 36.20, 37.16 | avr-mai | paille ≈ 1,6 Mt/an |
| PAILLE_BLE_TR | Céréales | Konya (steppe céréalière anatolienne) | 37.87, 32.49 | juin-juil | paille ≈ 25 Mt/an |
| PAILLE_ORGE_TR | Céréales | Ankara (bassin orge d anatolien) | 39.93, 32.86 | juin-juil | paille ≈ 8,1 Mt/an |
| PAILLE_AVOINE_TR | Céréales | Çorum (Haute Anatolie) | 40.65, 34.95 | juil-août | paille ≈ 390 000 t/an |
| PAILLE_MAIS_TR | Céréales | Adana (Çukurova, delta du Seyhan) | 37.00, 35.32 | sept-oct-nov | résidus de maïs ≈ 2 Mt/an |
| BALLE_RIZ_TR | Céréales | Edirne (Thrace rizicole) | 41.68, 26.56 | sept-oct | balle ≈ 203 800 t/an |
| TIGE_COTON_TR | Céréales | Şanlıurfa (bassin cotonnier du Sud-Est) | 37.16, 38.92 | oct-nov-déc | tiges de coton ≈ 6,7 Mt/an |
| TIGE_TOURNESOL_TR | Céréales | Edirne (tournesol de Thrace) | 41.72, 26.61 | sept-oct | tiges de tournesol ≈ 4,4 Mt/an |
| RESIDU_THE_TR | Tropical | Rize (côte de la mer Noire théicole) | 41.02, 40.52 | mai-juin-juil-août-sept-oct | résidus de théier ≈ 49 000 t/an |
| PAILLE_BLE_IR | Céréales | Gorgan (bassin de la Caspienne) | 36.84, 54.44 | mai-juin-juil | paille ≈ 20,1 Mt/an |
| PAILLE_ORGE_IR | Céréales | Mashhad (Khorassan) | 36.30, 59.60 | mai-juin | paille ≈ 4 Mt/an |
| BALLE_RIZ_IR | Céréales | Rasht (Guilan, rizière caspienne) | 37.28, 49.58 | sept-oct | balle ≈ 695 764 t/an |
| RACHIS_DATTIER_IR | Tropical | Bam (Kerman, ceinture des oasis) | 29.11, 58.37 | mars-avr-mai | palmes et rachis ≈ 339 000 t/an |
| PAILLE_BLE_RU | Céréales | Krasnodar (Kouban) | 45.04, 38.98 | juil-août | paille ≈ 99,1 Mt/an |
| PAILLE_ORGE_RU | Céréales | Saratov (bassin de la Volga) | 51.57, 46.03 | juil-août | paille ≈ 16,7 Mt/an |
| PAILLE_AVOINE_RU | Céréales | Chelyabinsk (Oural) | 55.16, 61.40 | août-sept | paille ≈ 3 Mt/an |
| TIGE_TOURNESOL_RU | Céréales | Volgograd (bassin tournesolier) | 48.71, 44.51 | sept-oct | tiges de tournesol ≈ 34,4 Mt/an |
| PAILLE_MAIS_RU | Céréales | Tikhoretsk (Kouban, maïs du Sud) | 45.61, 40.13 | sept-oct-nov | résidus de maïs ≈ 3,5 Mt/an |

## Fiches pays

### Afghanistan (Afghanistan) — 3 intrants

Portrait : bassins irrigués de l'Ouest et du Nord : blé dominant (Herat, Kunduz), riz et coton des vallées du Nord — agriculture de piémonts et d'oasis.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des résidus est pratiqué au nettoyage de printemps et au renouvellement des vergers, sans cadre national identifié à ce jour (À VÉRIFIER, à sourcer).
- enfouissement : les résidus servent d'abord de fourrage et de combustible domestique avant tout retour au sol (À VÉRIFIER, à sourcer).
- traitement : aucune filière de valorisation structurée identifiée à ce jour, l'économie des résidus reste domestique (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte est manuelle, le coût dominant est la main-d'œuvre familiale (À VÉRIFIER, à sourcer).
- main_oeuvre : petites structures familiales, mécanisation localisée dans les bassins irrigués (À VÉRIFIER, à sourcer).

#### PAILLE_BLE_AF — Paille de blé
- Région : Herat (bassin céréalier de l'Ouest) — GPS (Global Positioning System) 34.34, 62.21, approximation de région.
- Production : blé : 5 200 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,2 × grain [ILLUSTRATION].
- Gisement : paille ≈ 6,2 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : mai-juin-juil — moisson de mai à juillet, point sous garde.
- Techniques : moisson motorisée ou manuelle, balles rondes, fourrage dominant.

#### BALLE_RIZ_AF — Balle de riz
- Région : Kunduz (rizière du Nord) — GPS (Global Positioning System) 36.72, 68.86, approximation de région.
- Production : riz paddy : 654 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : balle ≈ 0,20 × riz paddy [ILLUSTRATION].
- Gisement : balle ≈ 130 800 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : oct-nov — moisson d'octobre à novembre, point sous garde.
- Techniques : moisson manuelle, décorticage villageois.

#### TIGE_COTON_AF — Tiges de coton
- Région : Taloqan (Takhar, coton du Nord) — GPS (Global Positioning System) 36.70, 69.53, approximation de région.
- Production : coton brut : 120 508 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : tiges ≈ 3 × coton brut non égrené [ILLUSTRATION].
- Gisement : tiges de coton ≈ 361 524 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : nov-déc — récolte de novembre à décembre, point sous garde.
- Techniques : récolte manuelle, andains au champ.

### Azerbaïdjan (Azerbaijan) — 3 intrants

Portrait : ceinture céréalière et cotonnière du bas-Kura (Ganja, Barda), orge de piémont (Qazax) — agriculture post-soviétique irriguée.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des chaumes est documenté localement, l'encadrement national reste à sourcer (À VÉRIFIER, à sourcer).
- enfouissement : la paille est largement récupérée comme fourrage et litière, retour au sol en partage (À VÉRIFIER, à sourcer).
- traitement : aucune filière de valorisation énergétique identifiée à ce jour (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte est mécanisée dans les grandes fermes, artisanale ailleurs (À VÉRIFIER, à sourcer).
- main_oeuvre : main-d'œuvre rurale disponible, saisonnalité forte des récoltes (À VÉRIFIER, à sourcer).

#### TIGE_COTON_AZ — Tiges de coton
- Région : Barda (coton du bas-Kura) — GPS (Global Positioning System) 40.39, 47.13, approximation de région.
- Production : coton brut : 237 651 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : tiges ≈ 3 × coton brut non égrené [ILLUSTRATION].
- Gisement : tiges de coton ≈ 712 953 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : oct-nov — récolte d'octobre à novembre, point sous garde.
- Techniques : récolte mécanique, arrachage des tiges.

#### PAILLE_BLE_AZ — Paille de blé
- Région : Ganja (bassin céréalier de l'Ouest) — GPS (Global Positioning System) 40.68, 46.36, approximation de région.
- Production : blé : 1 901 046 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,2 × grain [ILLUSTRATION].
- Gisement : paille ≈ 2,3 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : juin-juil — moisson de juin à juillet, point sous garde.
- Techniques : moisson motorisée, balles rondes, fourrage.

#### PAILLE_ORGE_AZ — Paille d'orge
- Région : Qazax (piémonts du Nord-Ouest) — GPS (Global Positioning System) 41.10, 45.36, approximation de région.
- Production : orge : 1 067 119 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,0 × grain [ILLUSTRATION].
- Gisement : paille ≈ 1,1 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : mai-juin — moisson de mai à juin, point sous garde.
- Techniques : moisson motorisée, balles rondes, fourrage.

### Bangladesh (Bangladesh) — 4 intrants

Portrait : delta du Gange et du Brahmapoutre : riz omniprésent (60 Mt), jute du Faridpur (fibre historique), maïs fourrager en expansion, blé d'hiver.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des balles de riz et des tiges est pratiqué malgré les interdictions locales signalées, cadre national à sourcer (À VÉRIFIER, à sourcer).
- enfouissement : la paille de riz est incorporée au sol ou sert de fourrage, la balle alimente les briqueteries (À VÉRIFIER, à sourcer).
- traitement : la balle de riz alimente déjà des chaudières informelles, aucun réseau structuré identifié à ce jour (À VÉRIFIER, à sourcer).
- cout_agriculture : la main-d'œuvre est abondante, la collecte manuelle domine hors zones mécanisées (À VÉRIFIER, à sourcer).
- main_oeuvre : petites parcelles, récolte en grande partie manuelle (À VÉRIFIER, à sourcer).

#### TIGE_JUTE_BD — Tiges de jute
- Région : Faridpur (bassin jutier du delta) — GPS (Global Positioning System) 23.60, 89.83, approximation de région.
- Production : jute : 2 086 101 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : tiges ≈ 1,8 × fibre [ILLUSTRATION].
- Gisement : tiges de jute ≈ 3,8 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : juil-août-sept — arrachage de juillet à septembre, point sous garde.
- Techniques : rouissage traditionnel, défibrage manuel ou mécanique.

#### BALLE_RIZ_BD — Balle de riz
- Région : Mymensingh (rizière du Bengale) — GPS (Global Positioning System) 24.75, 90.40, approximation de région.
- Production : riz paddy : 60 570 453 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : balle ≈ 0,20 × riz paddy [ILLUSTRATION].
- Gisement : balle ≈ 12,1 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : nov-déc-janv-févr-mars-avr — moissons d'amon et de boro, point sous garde.
- Techniques : moisson manuelle ou motorisée, décorticage en rizerie.

#### PAILLE_MAIS_BD — Résidus de maïs
- Région : Rangpur (bassin maïsier du Nord) — GPS (Global Positioning System) 25.75, 89.25, approximation de région.
- Production : maïs : 4 592 508 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : résidus ≈ 0,25 × grain [ILLUSTRATION].
- Gisement : résidus de maïs ≈ 1,1 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : oct-nov — récolte d'octobre à novembre, point sous garde.
- Techniques : récolte des épis, séchage, tiges au champ.

#### PAILLE_BLE_BD — Paille de blé
- Région : Dinajpur (bassin céréalier du Nord) — GPS (Global Positioning System) 25.62, 88.64, approximation de région.
- Production : blé : 1 172 242 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,2 × grain [ILLUSTRATION].
- Gisement : paille ≈ 1,4 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : mars-avr — moisson de mars à avril (blé d'hiver), point sous garde.
- Techniques : moisson motorisée, balles rondes, fourrage dominant.

### Cambodge (Cambodia) — 2 intrants

Portrait : riz du Tonlé Sap et du Battambang (14 Mt), manioc de Kampong Cham en forte croissance — agriculture de plaine tropicale.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des résidus de riz est courant en saison sèche, encadrement à sourcer (À VÉRIFIER, à sourcer).
- enfouissement : la paille est broutée par le bétail ou brûlée, le labour de couverture progresse (À VÉRIFIER, à sourcer).
- traitement : la balle de riz alimente quelques unités de cogénération, filière émergente (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte est manuelle, le transport fluvial structure les coûts (À VÉRIFIER, à sourcer).
- main_oeuvre : main-d'œuvre rurale abondante, moissons en grande partie manuelles (À VÉRIFIER, à sourcer).

#### BALLE_RIZ_KH — Balle de riz
- Région : Battambang (bassin du Tonlé Sap) — GPS (Global Positioning System) 13.10, 103.20, approximation de région.
- Production : riz paddy : 14 200 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : balle ≈ 0,20 × riz paddy [ILLUSTRATION].
- Gisement : balle ≈ 2,8 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : nov-déc-janv-févr-mars — moisson de novembre à mars, point tropical exempté.
- Techniques : moisson manuelle ou motorisée, décorticage villageois.

#### ECORCE_MANIOC_KH — Écorces de manioc
- Région : Kampong Cham (bassin manioc de l'Est) — GPS (Global Positioning System) 12.00, 105.46, approximation de région.
- Production : manioc : 14 261 306 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : écorces ≈ 0,15 × racines [ILLUSTRATION].
- Gisement : écorces ≈ 2,1 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc — récolte continue, point tropical exempté.
- Techniques : récolte manuelle, épluchage en amidonnerie.

### Corée du Sud (Republic of Korea) — 2 intrants

Portrait : riziculture de Jeolla (Jeonju, Iksan), orge d'hiver en succession — montagnes boisées, surfaces agricoles restreintes et mécanisées.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des résidus est réglementé au niveau national et restreint par les collectivités, texte à sourcer (À VÉRIFIER, à sourcer).
- enfouissement : l'incorporation de la paille au sol est encouragée après les récoltes de riz (À VÉRIFIER, à sourcer).
- traitement : des filières de valorisation de la paille et de la balle existent (litière, combustible rural) (À VÉRIFIER, à sourcer).
- cout_agriculture : la mécanisation est totale, la collecte est un service contractuel (À VÉRIFIER, à sourcer).
- main_oeuvre : vieillissement de la main-d'œuvre agricole, recours aux saisonniers (À VÉRIFIER, à sourcer).

#### BALLE_RIZ_KR — Balle de riz
- Région : Jeonju (Jeolla, rizière du Sud-Ouest) — GPS (Global Positioning System) 35.82, 127.15, approximation de région.
- Production : riz paddy : 4 783 114 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : balle ≈ 0,20 × riz paddy [ILLUSTRATION].
- Gisement : balle ≈ 956 623 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : oct-nov — moisson d'octobre à novembre, point sous garde.
- Techniques : moisson motorisée, séchage, décorticage en rizerie.

#### PAILLE_ORGE_KR — Paille d'orge
- Région : Iksan (Jeolla, orge d'hiver) — GPS (Global Positioning System) 35.94, 126.95, approximation de région.
- Production : orge : 47 730 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,0 × grain [ILLUSTRATION].
- Gisement : paille ≈ 47 730 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : mai-juin — moisson de mai à juin (orge d'hiver), point sous garde.
- Techniques : moisson motorisée, balles rondes, fourrage.

### Indonésie (Indonesia) — 5 intrants

Portrait : archipel : premier producteur mondial de palmier à huile (Riau, 243 Mt de régimes), riz de Java (53 Mt), canne de Lampung, manioc de Grobogan — production continue tropicale.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage est restreint par la réglementation sur les feux de végétation, pratiques résiduelles documentées à Sumatra et Bornéo (À VÉRIFIER, à sourcer).
- enfouissement : les rafles de palmier sont épandues en inter-rangs de plantation, pratique standard des huileries (À VÉRIFIER, à sourcer).
- traitement : les huileries valorisent déjà une part des rafles (compost, combustible de chaudière), marché concurrentiel (À VÉRIFIER, à sourcer).
- cout_agriculture : la logistique insulaire domine les coûts de collecte (À VÉRIFIER, à sourcer).
- main_oeuvre : plantations structurées pour le palmier, riziculture familiale à Java (À VÉRIFIER, à sourcer).

#### EFB_PALMIER_ID — Rafles de palmier à huile
- Région : Riau (bassin palmier de Sumatra) — GPS (Global Positioning System) 0.53, 101.44, approximation de région.
- Production : régimes de palmier : 243 000 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : rafles ≈ 0,22 × régimes [ILLUSTRATION].
- Gisement : rafles ≈ 53,5 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc — régimes toute l'année, point tropical exempté.
- Techniques : récolte des régimes, stérilisation et pressage en huilerie.

#### BALLE_RIZ_ID — Balle de riz
- Région : Karawang (rizière de Java Ouest) — GPS (Global Positioning System) -6.30, 107.32, approximation de région.
- Production : riz paddy : 53 142 727 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : balle ≈ 0,20 × riz paddy [ILLUSTRATION].
- Gisement : balle ≈ 10,6 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc — trois campagnes de riz par an, point tropical exempté.
- Techniques : moisson motorisée, usinage, décorticage en rizerie.

#### BAGASSE_CANNE_ID — Bagasse de canne
- Région : Lampung (bassin sucrier du Sud) — GPS (Global Positioning System) -5.40, 105.33, approximation de région.
- Production : canne à sucre : 32 000 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : bagasse ≈ 0,30 × canne [ILLUSTRATION].
- Gisement : bagasse ≈ 9,6 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : mai-juin-juil-août-sept-oct-nov-déc — campagne de broyage de mai à décembre, point tropical exempté.
- Techniques : récolte manuelle ou mécanique, broyage en sucrerie.

#### ECORCE_MANIOC_ID — Écorces de manioc
- Région : Grobogan (bassin manioc de Java Centre) — GPS (Global Positioning System) -7.08, 110.82, approximation de région.
- Production : manioc : 15 624 038 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : écorces ≈ 0,15 × racines [ILLUSTRATION].
- Gisement : écorces ≈ 2,3 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc — récolte continue, point tropical exempté.
- Techniques : récolte manuelle, épluchage en unités de transformation.

#### PAILLE_MAIS_ID — Résidus de maïs
- Région : Jember (Java Est) — GPS (Global Positioning System) -8.20, 113.70, approximation de région.
- Production : maïs : 15 138 912 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : résidus ≈ 0,25 × grain [ILLUSTRATION].
- Gisement : résidus de maïs ≈ 3,8 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc — double campagne de maïs, point tropical exempté.
- Techniques : récolte des grains, broyage des tiges au champ.

### Iran (Iran (Islamic Republic of)) — 4 intrants

Portrait : blé de Gorgan et de la Caspienne (16,75 Mt), orge du Khorassan, riz du Guilan, dattes de la ceinture des oasis (Kerman, Bam).

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des résidus est restreint par la réglementation environnementale, application variable à sourcer (À VÉRIFIER, à sourcer).
- enfouissement : la paille sert de fourrage dominant dans l'élevage ovin, retour au sol en partage (À VÉRIFIER, à sourcer).
- traitement : aucune filière de valorisation structurée identifiée à ce jour (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte est mécanisée dans les grands bassins céréaliers (À VÉRIFIER, à sourcer).
- main_oeuvre : mécanisation céréalière avancée, taille des palmiers manuelle (À VÉRIFIER, à sourcer).

#### PAILLE_BLE_IR — Paille de blé
- Région : Gorgan (bassin de la Caspienne) — GPS (Global Positioning System) 36.84, 54.44, approximation de région.
- Production : blé : 16 750 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,2 × grain [ILLUSTRATION].
- Gisement : paille ≈ 20,1 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : mai-juin-juil — moisson de mai à juillet, point sous garde.
- Techniques : moisson motorisée, balles rondes, fourrage dominant.

#### PAILLE_ORGE_IR — Paille d'orge
- Région : Mashhad (Khorassan) — GPS (Global Positioning System) 36.30, 59.60, approximation de région.
- Production : orge : 4 000 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,0 × grain [ILLUSTRATION].
- Gisement : paille ≈ 4 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : mai-juin — moisson de mai à juin, point sous garde.
- Techniques : moisson motorisée, pâturage des chaumes courant.

#### BALLE_RIZ_IR — Balle de riz
- Région : Rasht (Guilan, rizière caspienne) — GPS (Global Positioning System) 37.28, 49.58, approximation de région.
- Production : riz paddy : 3 478 820 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : balle ≈ 0,20 × riz paddy [ILLUSTRATION].
- Gisement : balle ≈ 695 764 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : sept-oct — moisson de septembre à octobre, point sous garde.
- Techniques : moisson motorisée, décorticage villageois.

#### RACHIS_DATTIER_IR — Palmes et rachis de palmier dattier
- Région : Bam (Kerman, ceinture des oasis) — GPS (Global Positioning System) 29.11, 58.37, approximation de région.
- Production : dattes : 1 182 144 t — surface 135 540 ha (2024, FAOSTAT), l'ancrage palmes et rachis est un ratio par hectare [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : palmes ≈ 2,5 t/ha/an (taille) [ILLUSTRATION].
- Gisement : palmes et rachis ≈ 339 000 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : mars-avr-mai — taille printanière des palmiers, point sous garde.
- Techniques : taille manuelle, déchiquetage au verger.

### Irak (Iraq) — 2 intrants

Portrait : dattiers historiques de Basra (surface 256 758 ha), blé de la Djéziré et de Diyala — agriculture irriguée mésopotamienne.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des palmes et chaumes est documenté, encadrement national à sourcer (À VÉRIFIER, à sourcer).
- enfouissement : les palmes servent d'ombrage, de litière et de combustible domestique (À VÉRIFIER, à sourcer).
- traitement : aucune filière de valorisation structurée identifiée à ce jour, les vergers dattiers concentrent les tailles (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte des palmes est manuelle au verger (À VÉRIFIER, à sourcer).
- main_oeuvre : taille et récolte des dattiers manuelles, savoir-faire oasien (À VÉRIFIER, à sourcer).

#### RACHIS_DATTIER_IQ — Palmes et rachis de palmier dattier
- Région : Basra (vergers dattiers du Chatt al-Arab) — GPS (Global Positioning System) 30.51, 47.78, approximation de région.
- Production : dattes : 587 190 t — surface 256 758 ha (2024, FAOSTAT), l'ancrage palmes et rachis est un ratio par hectare [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : palmes ≈ 2,5 t/ha/an (taille) [ILLUSTRATION].
- Gisement : palmes et rachis ≈ 642 000 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : mars-avr-mai — taille printanière des palmiers, point sous garde.
- Techniques : taille manuelle (machette), déchiquetage au verger.

#### PAILLE_BLE_IQ — Paille de blé
- Région : Diyala (bassin céréalier de l'Est) — GPS (Global Positioning System) 33.75, 44.52, approximation de région.
- Production : blé : 5 234 171 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,2 × grain [ILLUSTRATION].
- Gisement : paille ≈ 6,3 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : avr-mai — moisson d'avril à mai, point sous garde.
- Techniques : moisson motorisée, balles rondes, pâturage des chaumes.

### Japon (Japan) — 2 intrants

Portrait : riz de Niigata (10,1 Mt), blé de Hokkaido — petites structures, mécanisation fine, calendriers culturaux précis.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage de la paille de riz est réglementé et en recul, interdictions préfectorales documentées (À VÉRIFIER, à sourcer).
- enfouissement : l'incorporation précoce de la paille au sol est la pratique encouragée (À VÉRIFIER, à sourcer).
- traitement : la paille alimente litière, fourrage et matériaux, la balle des rizeries est partiellement valorisée (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte est mécanisée et contractuelle, coût élevé de la main-d'œuvre (À VÉRIFIER, à sourcer).
- main_oeuvre : vieillissement marqué, coopératives structurées (nokyo) (À VÉRIFIER, à sourcer).

#### BALLE_RIZ_JP — Balle de riz
- Région : Niigata (plaine du Shinano) — GPS (Global Positioning System) 37.92, 139.05, approximation de région.
- Production : riz paddy : 10 142 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : balle ≈ 0,20 × riz paddy [ILLUSTRATION].
- Gisement : balle ≈ 2 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : sept-oct-nov — moisson de septembre à novembre, point sous garde.
- Techniques : moisson motorisée, séchage, décorticage en rizerie.

#### PAILLE_BLE_JP — Paille de blé
- Région : Obihiro (Tokachi, Hokkaido) — GPS (Global Positioning System) 42.92, 143.20, approximation de région.
- Production : blé : 1 029 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,2 × grain [ILLUSTRATION].
- Gisement : paille ≈ 1,2 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : juil-août — moisson de juillet à août, point sous garde.
- Techniques : moisson motorisée, pressage en balles, fourrage d'hiver.

### Kazakhstan (Kazakhstan) — 4 intrants

Portrait : steppe céréalière du Nord (blé d'export 18,6 Mt, Akmola, Kostanay), orge, tournesol du Petropavl, coton du Turkestan — grandes cultures de latitudes hautes.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des chaumes est restreint par la réglementation sur les steppes, application à sourcer (À VÉRIFIER, à sourcer).
- enfouissement : le semis direct et la conservation des sols progressent, la paille reste majoritairement au sol (À VÉRIFIER, à sourcer).
- traitement : aucune filière de valorisation structurée identifiée à ce jour (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte est mécanisée à grande échelle, distances de transport élevées (À VÉRIFIER, à sourcer).
- main_oeuvre : fermes de très grande taille, main-d'œuvre saisonnière localisée (À VÉRIFIER, à sourcer).

#### PAILLE_BLE_KZ — Paille de blé
- Région : Kokshetau (Akmola, steppe céréalière) — GPS (Global Positioning System) 53.29, 69.42, approximation de région.
- Production : blé : 18 576 694 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,2 × grain [ILLUSTRATION].
- Gisement : paille ≈ 22,3 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : août-sept — moisson d'août à septembre, point sous garde.
- Techniques : moisson motorisée, balles rondes, export de paille possible.

#### PAILLE_ORGE_KZ — Paille d'orge
- Région : Kostanay (steppe du Nord) — GPS (Global Positioning System) 53.22, 63.62, approximation de région.
- Production : orge : 3 839 684 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,0 × grain [ILLUSTRATION].
- Gisement : paille ≈ 3,8 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : août-sept — moisson d'août à septembre, point sous garde.
- Techniques : moisson motorisée, balles rondes.

#### TIGE_TOURNESOL_KZ — Tiges de tournesol
- Région : Petropavl (Kazakhstan du Nord) — GPS (Global Positioning System) 54.87, 69.18, approximation de région.
- Production : tournesol : 1 834 397 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : tiges ≈ 2 × graines [ILLUSTRATION].
- Gisement : tiges de tournesol ≈ 3,7 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : sept-oct — récolte de septembre à octobre, point sous garde.
- Techniques : moisson motorisée, broyage des tiges.

#### TIGE_COTON_KZ — Tiges de coton
- Région : Turkestan (oasis cotonnière du Sud) — GPS (Global Positioning System) 43.29, 68.25, approximation de région.
- Production : coton brut : 301 661 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : tiges ≈ 3 × coton brut non égrené [ILLUSTRATION].
- Gisement : tiges de coton ≈ 904 984 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : oct-nov — récolte d'octobre à novembre, point sous garde.
- Techniques : récolte mécanique, arrachage des tiges.

### Kirghizistan (Kyrgyzstan) — 3 intrants

Portrait : vallées de Tchouï et de Talas (blé, orge), coton de Djalal-Abad — agriculture de montagne et de piémonts.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des résidus est pratiqué au printemps, encadrement à sourcer (À VÉRIFIER, à sourcer).
- enfouissement : la paille sert de fourrage d'hiver dominant pour l'élevage (À VÉRIFIER, à sourcer).
- traitement : aucune filière de valorisation structurée identifiée à ce jour (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte est artisanale, le coût dominant est le fourrage (À VÉRIFIER, à sourcer).
- main_oeuvre : fermes familiales, élevage et grandes cultures en partage (À VÉRIFIER, à sourcer).

#### TIGE_COTON_KG — Tiges de coton
- Région : Jalal-Abad (vallée de Ferghana kirghize) — GPS (Global Positioning System) 40.93, 72.78, approximation de région.
- Production : coton brut : 46 338 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : tiges ≈ 3 × coton brut non égrené [ILLUSTRATION].
- Gisement : tiges de coton ≈ 139 014 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : oct-nov — récolte d'octobre à novembre, point sous garde.
- Techniques : récolte manuelle, andains au champ.

#### PAILLE_BLE_KG — Paille de blé
- Région : Chuy (vallée de Bichkek) — GPS (Global Positioning System) 42.87, 74.59, approximation de région.
- Production : blé : 664 830 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,2 × grain [ILLUSTRATION].
- Gisement : paille ≈ 797 796 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : juil-août — moisson de juillet à août, point sous garde.
- Techniques : moisson motorisée, balles rondes, fourrage d'hiver.

#### PAILLE_ORGE_KG — Paille d'orge
- Région : Talas (vallée du Nord-Ouest) — GPS (Global Positioning System) 42.52, 72.24, approximation de région.
- Production : orge : 611 050 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,0 × grain [ILLUSTRATION].
- Gisement : paille ≈ 611 050 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : juin-juil — moisson de juin à juillet, point sous garde.
- Techniques : moisson motorisée, balles rondes, fourrage.

### Laos (Lao People's Democratic Republic) — 2 intrants

Portrait : riz du Mékong (Savannakhet, 3,8 Mt), manioc des plateaux en croissance — agriculture tropicale de vallées.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des résidus de riz est courant en saison sèche, encadrement à sourcer (À VÉRIFIER, à sourcer).
- enfouissement : la paille sert de fourrage et de paillage, le feu de nettoyage persiste (À VÉRIFIER, à sourcer).
- traitement : aucune filière de valorisation structurée identifiée à ce jour (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte est manuelle, l'éloignement des plateaux structure les coûts (À VÉRIFIER, à sourcer).
- main_oeuvre : riziculture familiale, récolte manuelle dominante (À VÉRIFIER, à sourcer).

#### BALLE_RIZ_LA — Balle de riz
- Région : Savannakhet (bassin du Mékong) — GPS (Global Positioning System) 16.60, 104.75, approximation de région.
- Production : riz paddy : 3 750 740 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : balle ≈ 0,20 × riz paddy [ILLUSTRATION].
- Gisement : balle ≈ 750 148 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : nov-déc-janv-févr-mars — moisson de novembre à mars, point tropical exempté.
- Techniques : moisson manuelle ou motorisée, décorticage villageois.

#### ECORCE_MANIOC_LA — Écorces de manioc
- Région : Vientiane (plaines du Mékong) — GPS (Global Positioning System) 18.20, 102.80, approximation de région.
- Production : manioc : 7 402 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : écorces ≈ 0,15 × racines [ILLUSTRATION].
- Gisement : écorces ≈ 1,1 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc — récolte continue, point tropical exempté.
- Techniques : récolte manuelle, épluchage en amidonnerie.

### Myanmar (Myanmar) — 3 intrants

Portrait : delta de l'Ayeyarwady (riz 27,7 Mt, Bogale), maïs des états Shan (Taunggyi), canne de la Chindwin (Monywa) — grenier tropical sous-équipé.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des résidus de riz est courant en saison sèche, encadrement à sourcer (À VÉRIFIER, à sourcer).
- enfouissement : la paille reste au sol ou sert de fourrage, le labour de couverture domine (À VÉRIFIER, à sourcer).
- traitement : aucune filière de valorisation structurée identifiée à ce jour (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte est manuelle, l'infrastructure de transformation est limitée (À VÉRIFIER, à sourcer).
- main_oeuvre : main-d'œuvre rurale abondante, moissons manuelles dominantes (À VÉRIFIER, à sourcer).

#### BALLE_RIZ_MM — Balle de riz
- Région : Bogale (delta de l'Ayeyarwady) — GPS (Global Positioning System) 16.30, 95.10, approximation de région.
- Production : riz paddy : 27 650 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : balle ≈ 0,20 × riz paddy [ILLUSTRATION].
- Gisement : balle ≈ 5,5 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : nov-déc-janv-févr-mars-avr — moisson de novembre à avril, point tropical exempté.
- Techniques : moisson manuelle ou motorisée, décorticage en rizerie.

#### PAILLE_MAIS_MM — Résidus de maïs
- Région : Taunggyi (plateaux des états Shan) — GPS (Global Positioning System) 20.78, 97.04, approximation de région.
- Production : maïs : 2 050 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : résidus ≈ 0,25 × grain [ILLUSTRATION].
- Gisement : résidus de maïs ≈ 512 500 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : août-sept-oct — récolte d'août à octobre, point tropical exempté.
- Techniques : récolte des épis, tiges broyées ou broutées au champ.

#### BAGASSE_CANNE_MM — Bagasse de canne
- Région : Monywa (vallée de la Chindwin) — GPS (Global Positioning System) 22.00, 95.13, approximation de région.
- Production : canne à sucre : 11 997 881 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : bagasse ≈ 0,30 × canne [ILLUSTRATION].
- Gisement : bagasse ≈ 3,6 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : nov-déc-janv-févr-mars — campagne de broyage de novembre à mars, point tropical exempté.
- Techniques : coupe manuelle, broyage en sucrerie.

### Népal (Nepal) — 3 intrants

Portrait : Terai (riz de Chitwan 6 Mt, blé de Rupandehi) et collines (maïs de Dang) — agriculture de plaine et de versants.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des résidus de blé avant la mousson est documenté, encadrement à sourcer (À VÉRIFIER, à sourcer).
- enfouissement : la paille sert de fourrage dominant (buffle, bovin), retour au sol en partage (À VÉRIFIER, à sourcer).
- traitement : aucune filière de valorisation structurée identifiée à ce jour (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte est manuelle, le fourrage valorise la paille (À VÉRIFIER, à sourcer).
- main_oeuvre : petites parcelles, exode rural et main-d'œuvre féminine dominante (À VÉRIFIER, à sourcer).

#### BALLE_RIZ_NP — Balle de riz
- Région : Chitwan (Terai central) — GPS (Global Positioning System) 27.53, 84.35, approximation de région.
- Production : riz paddy : 5 955 500 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : balle ≈ 0,20 × riz paddy [ILLUSTRATION].
- Gisement : balle ≈ 1,2 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : oct-nov-déc — moisson d'octobre à décembre, point sous garde.
- Techniques : moisson manuelle ou motorisée, décorticage villageois.

#### PAILLE_MAIS_NP — Résidus de maïs
- Région : Dang (vallées du mid-West) — GPS (Global Positioning System) 28.10, 82.30, approximation de région.
- Production : maïs : 3 193 869 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : résidus ≈ 0,25 × grain [ILLUSTRATION].
- Gisement : résidus de maïs ≈ 798 467 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : sept-oct-nov — récolte de septembre à novembre, point sous garde.
- Techniques : récolte des épis, séchage sur les toits, tiges au champ.

#### PAILLE_BLE_NP — Paille de blé
- Région : Rupandehi (Terai ouest) — GPS (Global Positioning System) 27.52, 83.28, approximation de région.
- Production : blé : 2 035 559 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,2 × grain [ILLUSTRATION].
- Gisement : paille ≈ 2,4 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : mars-avr-mai — moisson de mars à mai, point sous garde.
- Techniques : moisson motorisée, balles rondes, fourrage dominant.

### Ouzbékistan (Uzbekistan) — 2 intrants

Portrait : vallée de Ferghana et Samarcande : coton historique (2,9 Mt non égrené), blé d'autosuffisance (6,7 Mt) — oasis irriguées.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des tiges de coton et des chaumes est restreint par décret, application à sourcer (À VÉRIFIER, à sourcer).
- enfouissement : les tiges de coton sont retournées au sol sur ordonnancement étatique (À VÉRIFIER, à sourcer).
- traitement : aucune filière de valorisation structurée identifiée à ce jour (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte est organisée par les clusters cotonniers étatiques (À VÉRIFIER, à sourcer).
- main_oeuvre : récolte du coton en partie manuelle, salariat de campagne (À VÉRIFIER, à sourcer).

#### TIGE_COTON_UZ — Tiges de coton
- Région : Ferghana (vallée cotonnière) — GPS (Global Positioning System) 40.38, 71.78, approximation de région.
- Production : coton brut : 2 938 089 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : tiges ≈ 3 × coton brut non égrené [ILLUSTRATION].
- Gisement : tiges de coton ≈ 8,8 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : oct-nov — récolte d'octobre à novembre, point sous garde.
- Techniques : récolte manuelle ou mécanique, andains au champ.

#### PAILLE_BLE_UZ — Paille de blé
- Région : Samarcande (oasis céréalière) — GPS (Global Positioning System) 39.65, 66.96, approximation de région.
- Production : blé : 6 729 357 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,2 × grain [ILLUSTRATION].
- Gisement : paille ≈ 8,1 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : juin-juil — moisson de juin à juillet, point sous garde.
- Techniques : moisson motorisée, balles rondes, fourrage.

### Pakistan (Pakistan) — 3 intrants

Portrait : Pendjab céréalier (blé 31,8 Mt, coton de Multan 3,5 Mt), canne du Sindh (Matiari, 84 Mt) — irrigation du bassin de l'Indus.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des résidus de canne et de coton est courant, encadrement provincial à sourcer (À VÉRIFIER, à sourcer).
- enfouissement : la paille de blé sert de fourrage dominant, la balle de riz alimente les briqueteries (À VÉRIFIER, à sourcer).
- traitement : les sucreries valorisent déjà la bagasse en chaudière, marché concurrentiel (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte est semi-mécanisée, le coût du transport domine (À VÉRIFIER, à sourcer).
- main_oeuvre : récolte de la canne manuelle, saisonnalité forte du salariat (À VÉRIFIER, à sourcer).

#### TIGE_COTON_PK — Tiges de coton
- Région : Multan (ceinture cotonnière du Pendjab) — GPS (Global Positioning System) 30.20, 71.47, approximation de région.
- Production : coton brut : 3 500 618 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : tiges ≈ 3 × coton brut non égrené [ILLUSTRATION].
- Gisement : tiges de coton ≈ 10,5 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : nov-déc-janv — récolte d'octobre à février, point sous garde.
- Techniques : arrachage post-récolte, andains au champ.

#### BAGASSE_CANNE_PK — Bagasse de canne
- Région : Matiari (bassin sucrier du Sindh) — GPS (Global Positioning System) 25.60, 68.45, approximation de région.
- Production : canne à sucre : 84 235 451 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : bagasse ≈ 0,30 × canne [ILLUSTRATION].
- Gisement : bagasse ≈ 25,3 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : nov-déc-janv-févr-mars — campagne sucrière de novembre à mars, point sous garde.
- Techniques : récolte manuelle, broyage en sucrerie.

#### PAILLE_BLE_PK — Paille de blé
- Région : Sahiwal (bassin céréalier du Pendjab) — GPS (Global Positioning System) 30.67, 73.11, approximation de région.
- Production : blé : 31 814 444 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,2 × grain [ILLUSTRATION].
- Gisement : paille ≈ 38,2 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : avr-mai — moisson d'avril à mai, point sous garde.
- Techniques : moisson motorisée, pressage en balles rondes, andainage.

### Russie (Russian Federation) — 5 intrants

Portrait : Kouban et Volga : blé (82,6 Mt, Krasnodar, Saratov), orge (16,7 Mt), avoine de l'Oural (Kurgan), tournesol de Volgograd (17,2 Mt), maïs du Kouban — la steppe au sud du 50e parallèle.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des chaumes et des tiges de tournesol est restreint par décret régional, application variable à sourcer (À VÉRIFIER, à sourcer).
- enfouissement : la paille reste majoritairement au sol en grandes cultures extensives (À VÉRIFIER, à sourcer).
- traitement : la paille alimente quelques usines de pellet, filière marginale identifiée (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte est mécanisée, les distances de ramassage sont le coût dominant (À VÉRIFIER, à sourcer).
- main_oeuvre : fermes de très grande taille, mécanisation totale (À VÉRIFIER, à sourcer).

#### PAILLE_BLE_RU — Paille de blé
- Région : Krasnodar (Kouban) — GPS (Global Positioning System) 45.04, 38.98, approximation de région.
- Production : blé : 82 588 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,2 × grain [ILLUSTRATION].
- Gisement : paille ≈ 99,1 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : juil-août — moisson de juillet à août, point sous garde.
- Techniques : moisson motorisée, balles rondes, export de paille possible.

#### PAILLE_ORGE_RU — Paille d'orge
- Région : Saratov (bassin de la Volga) — GPS (Global Positioning System) 51.57, 46.03, approximation de région.
- Production : orge : 16 667 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,0 × grain [ILLUSTRATION].
- Gisement : paille ≈ 16,7 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : juil-août — moisson de juillet à août, point sous garde.
- Techniques : moisson motorisée, paille laissée au sol en sec.

#### PAILLE_AVOINE_RU — Paille d'avoine
- Région : Chelyabinsk (Oural) — GPS (Global Positioning System) 55.16, 61.40, approximation de région.
- Production : avoine : 3 000 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,0 × grain [ILLUSTRATION].
- Gisement : paille ≈ 3 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : août-sept — moisson d'août à septembre, point sous garde.
- Techniques : moisson motorisée, fourrage d'hiver ou paillage.

#### TIGE_TOURNESOL_RU — Tiges de tournesol
- Région : Volgograd (bassin tournesolier) — GPS (Global Positioning System) 48.71, 44.51, approximation de région.
- Production : tournesol : 17 200 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : tiges ≈ 2 × graines [ILLUSTRATION].
- Gisement : tiges de tournesol ≈ 34,4 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : sept-oct — récolte de septembre à octobre, point sous garde.
- Techniques : moisson motorisée, broyage des tiges.

#### PAILLE_MAIS_RU — Résidus de maïs
- Région : Tikhoretsk (Kouban, maïs du Sud) — GPS (Global Positioning System) 45.61, 40.13, approximation de région.
- Production : maïs : 13 954 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : résidus ≈ 0,25 × grain [ILLUSTRATION].
- Gisement : résidus de maïs ≈ 3,5 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : sept-oct-nov — récolte de septembre à novembre, point sous garde.
- Techniques : récolte des grains, ensilage ou broyage des tiges.

### Sri Lanka (Sri Lanka) — 2 intrants

Portrait : thé des hauts plateaux (Kandy, surface 268 829 ha), riz de Polonnaruwa — plantation et riziculture tropicales.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage est restreint par la réglementation environnementale, pratiques résiduelles documentées (À VÉRIFIER, à sourcer).
- enfouissement : les tailles de théier sont épandues en inter-rangs, la paille de riz sert de paillage (À VÉRIFIER, à sourcer).
- traitement : les usines de thé sèchent déjà une part des résidus (bois de taille), marché local (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte est manuelle sur les plantations, mécanisée en riziculture (À VÉRIFIER, à sourcer).
- main_oeuvre : cueillette manuelle du thé, main-d'œuvre de plantation structurée (À VÉRIFIER, à sourcer).

#### RESIDU_THE_LK — Résidus de théier
- Région : Kandy (hauts plateaux théicoles) — GPS (Global Positioning System) 7.29, 80.64, approximation de région.
- Production : thé (feuilles) : 1 514 024 t — surface 268 829 ha (2024, FAOSTAT), l'ancrage résidus de théier est un ratio par hectare [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : résidus ≈ 0,6 t/ha/an (tailles) [ILLUSTRATION].
- Gisement : résidus de théier ≈ 161 000 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc — cueillette toute l'année (quatre saisons de thé), point tropical exempté.
- Techniques : cueillette manuelle, tailles de formation et de régénération.

#### BALLE_RIZ_LK — Balle de riz
- Région : Polonnaruwa (rizière du Mahaweli) — GPS (Global Positioning System) 7.93, 81.02, approximation de région.
- Production : riz paddy : 4 698 453 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : balle ≈ 0,20 × riz paddy [ILLUSTRATION].
- Gisement : balle ≈ 939 691 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : mars-avr-août-sept — double campagne de riz (yala et maha), point tropical exempté.
- Techniques : moisson motorisée, décorticage en rizerie.

### Syrie (Syrian Arab Republic) — 2 intrants

Portrait : blé et orge du Croissant fertile (Djéziré de Hasakah, Alep 1,6 Mt d'orge) — pluvial et irrigué du Nord-Est.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des chaumes est pratiqué, encadrement à sourcer (À VÉRIFIER, à sourcer).
- enfouissement : la paille sert de fourrage dominant, le pâturage des chaumes est courant (À VÉRIFIER, à sourcer).
- traitement : aucune filière de valorisation structurée identifiée à ce jour (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte est semi-mécanisée, la sécheresse structure les coûts (À VÉRIFIER, à sourcer).
- main_oeuvre : grandes fermes mécanisées dans la Djéziré, petites structures ailleurs (À VÉRIFIER, à sourcer).

#### PAILLE_BLE_SY — Paille de blé
- Région : Hasakah (Djéziré, blé du Nord-Est) — GPS (Global Positioning System) 36.51, 40.75, approximation de région.
- Production : blé : 2 431 225 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,2 × grain [ILLUSTRATION].
- Gisement : paille ≈ 2,9 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : mai-juin — moisson de mai à juin, point sous garde.
- Techniques : moisson motorisée, balles rondes, fourrage dominant.

#### PAILLE_ORGE_SY — Paille d'orge
- Région : Alep (bassin orge de l'Ouest) — GPS (Global Positioning System) 36.20, 37.16, approximation de région.
- Production : orge : 1 572 020 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,0 × grain [ILLUSTRATION].
- Gisement : paille ≈ 1,6 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : avr-mai — moisson d'avril à mai, point sous garde.
- Techniques : moisson motorisée, pâturage des chaumes courant.

### Tadjikistan (Tajikistan) — 2 intrants

Portrait : coton de la vallée de Sughd (Panjakent, 253 kt), blé des vallées (Hissor) — agriculture de montagne irriguée.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des tiges de coton est restreint, application à sourcer (À VÉRIFIER, à sourcer).
- enfouissement : les tiges de coton sont retournées au sol ou servent de combustible domestique (À VÉRIFIER, à sourcer).
- traitement : aucune filière de valorisation structurée identifiée à ce jour (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte est manuelle, le combustible d'hiver valorise les tiges (À VÉRIFIER, à sourcer).
- main_oeuvre : récolte du coton en partie manuelle, ouvrages collectifs de campagne (À VÉRIFIER, à sourcer).

#### TIGE_COTON_TJ — Tiges de coton
- Région : Panjakent (vallée de Sughd) — GPS (Global Positioning System) 39.51, 67.32, approximation de région.
- Production : coton brut : 253 182 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : tiges ≈ 3 × coton brut non égrené [ILLUSTRATION].
- Gisement : tiges de coton ≈ 759 546 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : oct-nov — récolte d'octobre à novembre, point sous garde.
- Techniques : récolte manuelle, andains au champ.

#### PAILLE_BLE_TJ — Paille de blé
- Région : Hisor (vallée de Douchanbé) — GPS (Global Positioning System) 38.53, 68.79, approximation de région.
- Production : blé : 880 734 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,2 × grain [ILLUSTRATION].
- Gisement : paille ≈ 1,1 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : juin-juil — moisson de juin à juillet, point sous garde.
- Techniques : moisson motorisée, balles rondes, fourrage.

### Thaïlande (Thailand) — 4 intrants

Portrait : riz de la Chao Phraya (Chainat, 33,6 Mt), manioc de l'Isan (Khorat, 28,6 Mt), canne du Khon Kaen (82,4 Mt), palmier du Sud (Krabi) — grenier tropical exportateur.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des résidus de canne avant récolte est interdit mais documenté, contrôles en renforcement à sourcer (À VÉRIFIER, à sourcer).
- enfouissement : la paille de riz est en partie broyée et incorporée, le feu persiste en zones d'élevage (À VÉRIFIER, à sourcer).
- traitement : les sucreries valorisent la bagasse en chaudière, la balle de riz alimente des centrales et des fermes avicoles (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte est semi-mécanisée, le coût de la coupe manuelle de canne domine (À VÉRIFIER, à sourcer).
- main_oeuvre : coupe de canne manuelle salariée, riziculture mécanisée en plaine (À VÉRIFIER, à sourcer).

#### BALLE_RIZ_TH — Balle de riz
- Région : Chainat (bassin de la Chao Phraya) — GPS (Global Positioning System) 15.20, 100.10, approximation de région.
- Production : riz paddy : 33 551 337 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : balle ≈ 0,20 × riz paddy [ILLUSTRATION].
- Gisement : balle ≈ 6,7 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : nov-déc-janv-févr-mars-avr — grande récolte de novembre à avril, point tropical exempté.
- Techniques : moisson motorisée, usinage, décorticage en rizerie.

#### ECORCE_MANIOC_TH — Écorces de manioc
- Région : Nakhon Ratchasima (bassin manioc de l'Isan) — GPS (Global Positioning System) 14.97, 102.10, approximation de région.
- Production : manioc : 28 624 312 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : écorces ≈ 0,15 × racines [ILLUSTRATION].
- Gisement : écorces ≈ 4,3 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc — récolte continue, point tropical exempté.
- Techniques : récolte manuelle, épluchage en amidonnerie.

#### BAGASSE_CANNE_TH — Bagasse de canne
- Région : Khon Kaen (bassin sucrier du Nord-Est) — GPS (Global Positioning System) 16.43, 102.83, approximation de région.
- Production : canne à sucre : 82 435 400 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : bagasse ≈ 0,30 × canne [ILLUSTRATION].
- Gisement : bagasse ≈ 24,7 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : nov-déc-janv-févr-mars — campagne de broyage de novembre à mars, point tropical exempté.
- Techniques : coupe manuelle ou mécanique, broyage en sucrerie.

#### EFB_PALMIER_TH — Rafles de palmier à huile
- Région : Krabi (bassin palmier du Sud) — GPS (Global Positioning System) 8.11, 98.90, approximation de région.
- Production : régimes de palmier : 18 606 769 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : rafles ≈ 0,22 × régimes [ILLUSTRATION].
- Gisement : rafles ≈ 4,1 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc — régimes toute l'année, point tropical exempté.
- Techniques : récolte des régimes, stérilisation et pressage en huilerie.

### Turkménistan (Turkmenistan) — 2 intrants

Portrait : coton de Mary (600 kt) et blé de Dachogouz (1,3 Mt) — oasis irriguées du Karakoum, ordonnancement étatique.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des tiges de coton est restreint par ordonnance, application à sourcer (À VÉRIFIER, à sourcer).
- enfouissement : les tiges sont retournées au sol sur directive des exploitations d'État (À VÉRIFIER, à sourcer).
- traitement : aucune filière de valorisation structurée identifiée à ce jour (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte est organisée par les exploitations d'État (À VÉRIFIER, à sourcer).
- main_oeuvre : récolte du coton en partie manuelle, campagnes organisées (À VÉRIFIER, à sourcer).

#### TIGE_COTON_TM — Tiges de coton
- Région : Mary (oasis cotonnière du Karakoum) — GPS (Global Positioning System) 37.61, 61.83, approximation de région.
- Production : coton brut : 600 238 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : tiges ≈ 3 × coton brut non égrené [ILLUSTRATION].
- Gisement : tiges de coton ≈ 1,8 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : oct-nov — récolte d'octobre à novembre, point sous garde.
- Techniques : récolte manuelle ou mécanique, andains au champ.

#### PAILLE_BLE_TM — Paille de blé
- Région : Dashoguz (oasis céréalière du Nord) — GPS (Global Positioning System) 41.43, 59.91, approximation de région.
- Production : blé : 1 330 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,2 × grain [ILLUSTRATION].
- Gisement : paille ≈ 1,6 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : juin-juil — moisson de juin à juillet, point sous garde.
- Techniques : moisson motorisée, balles rondes, fourrage.

### Turquie (Türkiye) — 8 intrants

Portrait : blé de Konya (20,8 Mt), orge d'Ankara (8,1 Mt), maïs de Çukurova (8,1 Mt), coton de Şanlıurfa (2,2 Mt), tournesol de Thrace (Edirne), thé de Rize (1,4 Mt) — agricultures méditerranéennes et anatoliennes.

Réglementation (cinq postes, tous À VÉRIFIER) :
- brulage : le brûlage des résidus est restreint par la réglementation turque sur l'environnement, pratiques variables selon les provinces (À VÉRIFIER, à sourcer).
- enfouissement : la paille sert de fourrage et de litière, l'incorporation au sol progresse (À VÉRIFIER, à sourcer).
- traitement : la paille alimente des unités de cogénération documentées, la balle de riz des rizeries de Thrace (À VÉRIFIER, à sourcer).
- cout_agriculture : la collecte est mécanisée et contractuelle dans les grands bassins (À VÉRIFIER, à sourcer).
- main_oeuvre : mécanisation céréalière avancée, cueillette du thé manuelle (À VÉRIFIER, à sourcer).

#### PAILLE_BLE_TR — Paille de blé
- Région : Konya (steppe céréalière anatolienne) — GPS (Global Positioning System) 37.87, 32.49, approximation de région.
- Production : blé : 20 800 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,2 × grain [ILLUSTRATION].
- Gisement : paille ≈ 25 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : juin-juil — moisson de juin à juillet, point sous garde.
- Techniques : moisson motorisée, pressage en balles rondes, andainage.

#### PAILLE_ORGE_TR — Paille d'orge
- Région : Ankara (bassin orge d anatolien) — GPS (Global Positioning System) 39.93, 32.86, approximation de région.
- Production : orge : 8 100 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,0 × grain [ILLUSTRATION].
- Gisement : paille ≈ 8,1 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : juin-juil — moisson de juin à juillet, point sous garde.
- Techniques : moisson motorisée, balles rondes, fourrage.

#### PAILLE_AVOINE_TR — Paille d'avoine
- Région : Çorum (Haute Anatolie) — GPS (Global Positioning System) 40.65, 34.95, approximation de région.
- Production : avoine : 390 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : paille ≈ 1,0 × grain [ILLUSTRATION].
- Gisement : paille ≈ 390 000 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : juil-août — moisson de juillet à août, point sous garde.
- Techniques : moisson motorisée, balles rondes, fourrage.

#### PAILLE_MAIS_TR — Résidus de maïs
- Région : Adana (Çukurova, delta du Seyhan) — GPS (Global Positioning System) 37.00, 35.32, approximation de région.
- Production : maïs : 8 100 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : résidus ≈ 0,25 × grain [ILLUSTRATION].
- Gisement : résidus de maïs ≈ 2 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : sept-oct-nov — récolte de septembre à novembre, point sous garde.
- Techniques : récolte des grains, ensilage des tiges ou broyage au champ.

#### BALLE_RIZ_TR — Balle de riz
- Région : Edirne (Thrace rizicole) — GPS (Global Positioning System) 41.68, 26.56, approximation de région.
- Production : riz paddy : 1 019 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : balle ≈ 0,20 × riz paddy [ILLUSTRATION].
- Gisement : balle ≈ 203 800 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : sept-oct — moisson de septembre à octobre, point sous garde.
- Techniques : moisson motorisée, décorticage en rizerie de Thrace.

#### TIGE_COTON_TR — Tiges de coton
- Région : Şanlıurfa (bassin cotonnier du Sud-Est) — GPS (Global Positioning System) 37.16, 38.92, approximation de région.
- Production : coton brut : 2 243 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : tiges ≈ 3 × coton brut non égrené [ILLUSTRATION].
- Gisement : tiges de coton ≈ 6,7 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : oct-nov-déc — récolte d'octobre à décembre, point sous garde.
- Techniques : récolte mécanique, arrachage des tiges post-récolte.

#### TIGE_TOURNESOL_TR — Tiges de tournesol
- Région : Edirne (tournesol de Thrace) — GPS (Global Positioning System) 41.72, 26.61, approximation de région.
- Production : tournesol : 2 195 000 t (2024, FAOSTAT) [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : tiges ≈ 2 × graines [ILLUSTRATION].
- Gisement : tiges de tournesol ≈ 4,4 Mt/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : sept-oct — récolte de septembre à octobre, point sous garde.
- Techniques : moisson motorisée, broyage des tiges.

#### RESIDU_THE_TR — Résidus de théier
- Région : Rize (côte de la mer Noire théicole) — GPS (Global Positioning System) 41.02, 40.52, approximation de région.
- Production : thé (feuilles) : 1 414 000 t — surface 81 010 ha (2024, FAOSTAT), l'ancrage résidus de théier est un ratio par hectare [SOURCÉ, bulk FAOSTAT 2024].
- Ratio : résidus ≈ 0,6 t/ha/an (tailles) [ILLUSTRATION].
- Gisement : résidus de théier ≈ 49 000 t/an [SOURCÉ (production FAOSTAT 2024) + ratio ILLUSTRATION].
- Fenêtre : mai-juin-juil-août-sept-oct — cueillette et tailles de mai à octobre, point sous garde.
- Techniques : cueillette manuelle, tailles de formation, séchage en usine.

## Coupe de périmètre

Non retenus (dix-huit pays) :
- Brunei : surface agricole négligeable.
- Singapour : ville-État, pas de gisement agricole.
- Timor-Leste : pas de série bulk exploitable.
- Maldives : surface agricole négligeable.
- Bhoutan : montagne boisée, pas de série bulk exploitable.
- Mongolie : élevage extensif hors périmètre cultures.
- Corée du Nord : pas de série bulk exploitable.
- Arménie : petits bassins, noyau viticole déjà traité.
- Oman : gisement dattier déjà couvert par l'Irak et l'Iran.
- Émirats arabes unis : gisement dattier déjà couvert.
- Qatar : surface agricole négligeable.
- Koweït : surface agricole négligeable.
- Bahreïn : surface agricole négligeable.
- Yémen : série bulk lacunaire, gisement dattier déjà couvert.
- Jordanie : petits bassins, pas d'intrant majeur dégagé.
- Israël : agriculture intensive, pas d'intrant majeur dégagé.
- Liban : surface agricole négligeable.
- Territoires palestiniens : surface agricole négligeable.

Déjà couverts (sept pays) :
- Chine : atlas v1.0 et v1.1.
- Inde : atlas v1.0 et v1.1.
- Malaisie : atlas v1.0 et v1.1.
- Philippines : atlas v1.0 et v1.1.
- Viêt Nam : atlas v1.0 et v1.1.
- Arabie saoudite : atlas v1.0 et v1.1.
- Géorgie : atlas v1.2 (vignobles).

## Limites honnêtes

- La bagasse est déjà valorisée en chaudières par les sucreries thaïlandaises et pakistanaises : le gisement affiché est brut, la part réellement disponible est plus faible.
- Les productions nationales ne sont pas régionales : l'ancrage GPS (Global Positioning System) est une approximation de bassin.
- Les ratios ILLUSTRATION doivent être bornés localement avant tout dimensionnement.
- La réglementation à cinq postes est À VÉRIFIER avant tout engagement, validation par un conseil local requise.
- L'écart historique de 79 contre 72 intrants est tracé : la famille Coques et noyaux n'existe pas dans le master v1.0.

## Reproductibilité

- Module : python3 engine/atlas_biomasses_asie.py (sommaire, fiche TOKEN, pays NOM, croisement, meteo [TOKEN]).
- Le croisement contrôle familles, collisions v1.0, v1.1 et v1.2, gardes saisonnières (54 points sous garde, 18 tropicaux exemptés) et boîtes englobantes.
- Le bulk FAOSTAT vit dans cache-faostat-bulk/ hors du dépôt, procédure de régénération documentée dans gisements-hubs-generalises.md.
- Aucune dépendance réseau hors la commande meteo (Open-Meteo, gratuite sans clé, cache local d'une heure jamais versionné).

