# Gisements FAOSTAT des hubs généralisés (V1.7, 31/10/2026)

Couche P2.9 du programme World Twin. Étiquette SYNTHÉTIQUE : la flotte est une simulation « as if in operation », jamais une exploitation réelle. Devant un investisseur, on dit simulation, toujours.

## Résumé

La règle ILLUSTRATION de dimensionnement par densité de points (V1.6, 27/10/2026) est remplacée par un dimensionnement fondé sur les gisements réels FAOSTAT (Organisation des Nations unies pour l'alimentation et l'agriculture) : chaque point d'intrant reçoit un gisement en tonnes par an calculé depuis les séries nationales bulk, chaque hub dimensionne ses trios sur la somme des gisements de ses points.

- Flotte : 88 trios (V1.6) → 208 trios (V1.7), 162 opérateurs (inchangés, ratio 0,78 opérateur par trio), 81 hubs sur 32 pays, plafond figé de 5 trios par équipe d'opérateurs.
- Couverture : 138 points d'atlas généralisés, dont 123 sourcés FAOSTAT et 15 étiquetés À SOURCER (exclus du calcul numérique, aucune valeur inventée).
- Somme mondiale des gisements sourcés : 2 543 Mt/an (proxy national, la décomposition régionale addressable reste À SOURCER en P3).
- Modules : engine/gisements_hubs.py (gisements par point, contrôles croisés, couverture) et engine/flotte_monde.py v1.7 (dimensionnement par paliers de gisement). Snapshot versionné : engine/gisements-faostat-snapshot-v17.json.

## Méthode

### Base FAOSTAT

Bulk normalisé « Production_Crops_Livestock_E_All_Data_(Normalized).zip », URL https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_(Normalized).zip, 33 921 825 octets, md5 1a202c5674dce152f1134fa87b220b82, date interne FAO 2025-12-23, licence CC BY 4.0, attribution FAOSTAT. Série 1961-2024 : la fenêtre retenue est 2020-2024 (cinq années, min-moyenne-max par couple pays/item). Éléments : Production (tonnes) et Area harvested (hectares). Pays : 33.

Pièges de nommage bulk documentés (noms anglais) : « China, mainland », « Türkiye », « Viet Nam », « United States of America », « Republic of Moldova », « Côte d'Ivoire » (avec accents), « Groundnuts, excluding shelled », « Seed cotton, unginned », « Maize (corn) », « Soya beans », et l'item de riz s'appelle « Rice » (pas « Rice, paddy »).

### Gisement d'un point

Gisement = base FAOSTAT de la fenêtre (min, moyenne, max de l'élément du couple pays/item) multipliée par un ratio de résidu ILLUSTRATION (min, milieu, max) issu des fiches d'atlas v1.0, v1.1 et v1.2. Chaque point porte sa fourchette [min, milieu, max] et l'étiquette SOURCÉ (FAOSTAT 2020-2024) + ratio ILLUSTRATION. Bases de masse hétérogènes assumées : sèche pour les grains et les pailles, humide pour la bagasse, les écorces, les cerises de café et les cabosses fraîches.

### Gisement d'un hub et paliers de trios

Le gisement d'un hub est la somme des milieux de fourchette de ses points sourcés. Le nombre de trios suit des paliers sur ce gisement (règle ILLUSTRATION, plafond figé) :

| Gisement du hub (t/an) | Trios |
| --- | --- |
| moins de 0,5 Mt | 1 |
| de 0,5 à 2 Mt | 2 |
| de 2 à 10 Mt | 3 |
| de 10 à 50 Mt | 4 |
| 50 Mt et plus | 5 |

Un hub dont aucun point n'est sourcé (par exemple un point unique sargasse) reste en repli densité V1.6, propre et étiqueté. La règle opérateurs figée en P0 est inchangée : 2 opérateurs tournants pour 5 trios maximum, sixième trio = seconde équipe — aucun hub ne dépasse 5 trios, les 162 opérateurs de V1.6 sont conservés.

### Snapshot versionné

engine/gisements-faostat-snapshot-v17.json : 599 séries (uniquement les couples pays/item nécessaires aux gisements et aux contrôles croisés), 33 556 octets, triées, provenance complète (URL, taille, md5, licence, fenêtre). Versionné pour le déterminisme : un run hors ligne, sans réseau, reproduit la flotte à l'identique. Le bulk brut (environ 545 Mo extraits) et le cache filtré (faostat-33pays-2020-2024.json, 36 386 lignes) ne sont jamais versionnés — doctrine cache-faostat-bulk/.

## Conventions de ratios par famille (ILLUSTRATION)

Chaque ratio (min/milieu/max) a été recoupé entre la fiche d'atlas d'origine et FAOSTAT 2024 : 92 reproductions de fiches contrôlées à l'identique par le vérifieur.

| Résidu | Item FAOSTAT | Élément | Ratio (min/milieu/max) | Points |
| --- | --- | --- | --- | --- |
| Paille de blé | Wheat | Production | 0,8/1,0/1,2 × | 12 |
| Paille d'orge | Barley | Production | 0,8/0,9/1,0 × | 3 |
| Paille et tige de maïs | Maize (corn) | Production | 0,8/1,0/1,2 × | 5 |
| Paille de soja | Soya beans | Production | 0,8/1,0/1,2 × | 2 |
| Paille de riz | Rice | Production | 1,0/1,2/1,4 × | 6 |
| Balle de riz | Rice | Production | 0,18/0,20/0,22 × | 7 |
| Balle d'avoine | Oats | Production | 0,20/0,25/0,30 × | 1 |
| Paille de colza | Rape or colza seed | Production | 1,0/1,5/2,0 × | 2 |
| Tige de moutarde (Inde) | Rape or colza seed | Production | 1,2/1,5/1,8 × | 1 |
| Tige de tournesol | Sunflower seed | Production | 1,0/1,5/2,0 × | 2 |
| Paille de lin (anas) | Flax, raw or retted | Production | 0,40/0,50/0,60 × | 1 |
| Chènevotte | True hemp, raw or retted | Production | 0,50/0,55/0,60 × | 1 |
| Bagasse | Sugar cane | Production | 0,25/0,28/0,30 × | 6 |
| Paille de canne | Sugar cane | Production | 0,10/0,125/0,15 × | 1 |
| Sarments de vigne | Grapes | Area harvested | 1,5/2,0/3,0 t/ha | 20 |
| Marc de raisin | Grapes | Production | 0,15/0,15/0,25 × | 12 |
| Grignon d'olive | Olives | Production | 0,35/0,40/0,45 × | 1 |
| Marc de pomme | Apples | Production | 0,15/0,20/0,25 × | 2 |
| Rafle de maïs | Maize (corn) | Production | 0,12/0,15/0,18 × | 1 |
| Drèche de brasserie | Beer of barley, malted | Production | 0,15/0,20/0,25 × (20 kg/hl, 1 t ≈ 10 hl) | 1 |
| Écorce d'orange | Oranges | Production | 0,22/0,25/0,28 × | 3 |
| Noyau d'abricot | Apricots | Production | 0,06/0,08/0,10 × | 1 |
| Noyau de pêche | Peaches and nectarines | Production | 0,06/0,08/0,10 × | 1 |
| Noyau de cerise | Cherries | Production | 0,08/0,10/0,12 × | 1 |
| Noyau d'avocat | Avocados | Production | 0,15/0,20/0,25 × | 1 |
| Noyau de datte | Dates | Production | 0,10/0,125/0,15 × | 1 |
| Rachis de palmier dattier | Dates | Area harvested | 2,0/2,5/3,0 t/ha | 1 |
| Déchet de dattier | Dates | Area harvested | 2,0/4,0/6,0 t/ha | 1 |
| Coque d'amande | Almonds, in shell | Production | 1,8/2,0/2,2 × | 2 |
| Coque de noisette | Hazelnuts, in shell | Production | 0,45/0,475/0,50 × | 1 |
| Coque de cajou | Cashew nuts, in shell | Production | 0,65/0,70/0,75 × | 2 |
| Coque et balle d'arachide | Groundnuts, excluding shelled | Production | 0,25/0,30/0,35 × | 2 |
| Coque de cacao | Cocoa beans | Production | 0,65/0,70/0,75 × | 1 |
| Cabosse de cacao | Cocoa beans | Production | 8,0/10,0/12,0 × (fiche) | 1 |
| Coque de noix de coco | Coconuts, in shell | Production | 0,35/0,40/0,45 × | 1 |
| Fibre de coco | Coconuts, in shell | Production | 0,25/0,30/0,35 × | 1 |
| Fibre de palmier à huile | Oil palm fruit | Production | 0,10/0,12/0,14 × et 0,22/0,25/0,28 × (Côte d'Ivoire) | 3 |
| Raffle de palmier à huile | Oil palm fruit | Production | 0,20/0,22/0,25 × | 1 |
| Coque de café | Coffee, green | Production | 0,18/0,20/0,22 × | 2 |
| Marc de café | Coffee, green | Production | 2,1/2,25/2,4 × (chaîne cerise fraîche documentée) | 1 |
| Graine de papaye | Papayas | Production | 0,10/0,125/0,15 × | 1 |
| Feuille d'ananas | Pineapples | Area harvested | 3,0/4,5/6,0 t/ha | 1 |
| Tige de bananier | Bananas | Area harvested | 30/40/50 t/ha | 1 |
| Écorce de banane | Bananas | Production | 0,25/0,30/0,35 × | 1 |
| Tige de coton | Seed cotton, unginned | Area harvested | 2,0/2,5/3,0 t/ha | 1 |
| Tige de sorgho | Sorghum | Area harvested | 3,0/4,5/6,0 t/ha | 1 |
| Noix macadamia, pacane, pistache | Other nuts…n.e.c. | Production | 0,45/0,50/0,55 × (pacane, pistache) et 0,60/0,65/0,70 × (macadamia) | 3 |

## Les 15 intrants À SOURCER

Sans équivalent FAOSTAT (forestier, minéral, marin, brassicole, sargasse, bambou, agave, liège, luzerne fourragère) : AIGUILLE_PIN, BRISURE_LIEGE_PT (Portugal), CARAPACE_CRABE, COPEAU_HETRE, COQUILLE_HUITRE, COQUILLE_MOULE, COQUILLE_ST_JACQUES, ECORCE_EUCALYPTUS, ECORCE_PIN, FANE_LUZERNE_SA (Arabie Saoudite), RESIDU_AGAVE (Mexique), SARGASSE (Mexique), SCIURE_CHENE, SCIURE_PIN, TIGE_BAMBOU (Chine).

Ces points sont exclus du calcul numérique : aucune valeur n'est jamais inventée. Trois hubs ne portent que des points À SOURCER et restent au repli densité V1.6, étiquetés comme tel : gen-arabie-saoudite-3 (fane de luzerne), gen-chine-2 (tige de bambou), gen-mexique-4 (sargasse). Le compteur « points à sourcer » figure dans la composition de chaque hub (voir sorties du sommaire).

## Corrections de sourcing

Trois fiches v1.0 surestimaient leur gisement. Le numérique suit désormais FAOSTAT, la fiche reste référence qualitative :

- Balle d'avoine France : la fiche citait 2 à 3 Mt/an, le calcul FAOSTAT (production d'avoine 2020-2024 de 0,30 à 0,48 Mt × ratio 0,20-0,30) donne 0,06 à 0,14 Mt/an.
- Drèche de brasserie France : la fiche citait 1,5 à 2 Mt/an, le calcul (bière d'orge malté 2020-2024 × 20 kg/hl) donne environ 0,43 Mt/an au milieu de fourchette.
- Marc de pomme France : proxy pommes FAOSTAT (1,6 à 2,0 Mt/an de pommes × ratio 0,15-0,25), gisement 0,24 à 0,49 Mt/an.

## Résultats

Composition V1.7 de la flotte généralisée :

- 208 trios (88 en V1.6), 162 opérateurs (inchangés, ratio 0,78 par trio), 81 hubs sur 32 pays.
- Distribution des hubs par nombre de trios : 30 hubs à 1 trio, 10 à 2, 17 à 3, 13 à 4, 11 à 5.
- Écarts V1.6 → V1.7 : 30 hubs inchangés, 1 hub en baisse (gen-france-1, 2 → 1 trios, gisement 176-660 kt), 12 à +1, 15 à +2, 13 à +3, 10 à +4.
- Somme mondiale des gisements sourcés : 2 543 Mt/an (proxy national).
- Monte Carlo de contrôle (3 graines) : disponibilité de flotte 99,7 %, simulation complète en environ 2 secondes — le simulateur reste fonctionnel pour les pipelines CI (Continuous Integration) GitHub Actions.

Table comparatif complète (les gisements sont des fourchettes ILLUSTRATION sur base FAOSTAT sourcée, proxy national) :

| Hub | Pays | Points | Trios v1.6 | Trios v1.7 | Opérateurs | Gisement (t/an, ILLUSTRATION) |
| --- | --- | --- | --- | --- | --- | --- |
| gen-afrique-du-sud-1 | Afrique du Sud | 2 | 1 | 2 | 2 | 437 kt à 866 kt |
| gen-allemagne-1 | Allemagne | 2 | 1 | 1 | 2 | 310 kt à 611 kt |
| gen-arabie-saoudite-1 | Arabie Saoudite | 1 | 1 | 1 | 2 | 305 kt à 773 kt |
| gen-arabie-saoudite-2 | Arabie Saoudite | 3 | 1 | 2 | 2 | 903 kt à 3.4 Mt |
| gen-arabie-saoudite-3 | Arabie Saoudite | 1 | 1 | 1 | 2 | À SOURCER |
| gen-argentine-1 | Argentine | 1 | 1 | 4 | 2 | 10 Mt à 27 Mt |
| gen-argentine-2 | Argentine | 2 | 1 | 4 | 2 | 23 Mt à 69 Mt |
| gen-argentine-3 | Argentine | 1 | 1 | 5 | 2 | 33 Mt à 73 Mt |
| gen-argentine-4 | Argentine | 1 | 1 | 1 | 2 | 218 kt à 560 kt |
| gen-australie-1 | Australie | 1 | 1 | 1 | 2 | 195 kt à 584 kt |
| gen-australie-2 | Australie | 1 | 1 | 1 | 2 | 221 kt à 557 kt |
| gen-australie-3 | Australie | 1 | 1 | 4 | 2 | 4.8 Mt à 18 Mt |
| gen-australie-4 | Australie | 1 | 1 | 4 | 2 | 22 Mt à 49 Mt |
| gen-australie-5 | Australie | 1 | 1 | 4 | 2 | 8.8 Mt à 15 Mt |
| gen-australie-6 | Australie | 1 | 1 | 3 | 2 | 7.2 Mt à 9.8 Mt |
| gen-australie-7 | Australie | 1 | 1 | 1 | 2 | 25.8 kt à 42 kt |
| gen-bresil-1 | Brésil | 1 | 1 | 3 | 2 | 1.9 Mt à 2.6 Mt |
| gen-bresil-2 | Brésil | 1 | 1 | 5 | 2 | 71 Mt à 1.6e+02 Mt |
| gen-bresil-3 | Brésil | 3 | 1 | 5 | 2 | 2.5e+02 Mt à 3.6e+02 Mt |
| gen-bresil-4 | Brésil | 1 | 1 | 1 | 2 | 114 kt à 189 kt |
| gen-bresil-5 | Brésil | 1 | 1 | 5 | 2 | 97 Mt à 1.8e+02 Mt |
| gen-bresil-6 | Brésil | 1 | 1 | 1 | 2 | 111 kt à 253 kt |
| gen-chili-1 | Chili | 2 | 1 | 2 | 2 | 615 kt à 1.3 Mt |
| gen-chine-1 | Chine | 1 | 1 | 5 | 2 | 2.1e+02 Mt à 3e+02 Mt |
| gen-chine-2 | Chine | 1 | 1 | 1 | 2 | À SOURCER |
| gen-chine-3 | Chine | 1 | 1 | 5 | 2 | 1.1e+02 Mt à 1.7e+02 Mt |
| gen-chine-4 | Chine | 1 | 1 | 3 | 2 | 4.5 Mt à 6.9 Mt |
| gen-chine-5 | Chine | 1 | 1 | 3 | 2 | 2.1 Mt à 4.2 Mt |
| gen-chine-6 | Chine | 1 | 1 | 2 | 2 | 1.1 Mt à 2.3 Mt |
| gen-chine-7 | Chine | 1 | 1 | 5 | 2 | 2.1e+02 Mt à 3.5e+02 Mt |
| gen-cote-d-ivoire-1 | Côte d'Ivoire | 1 | 1 | 3 | 2 | 1.5 Mt à 3.3 Mt |
| gen-cote-d-ivoire-2 | Côte d'Ivoire | 3 | 1 | 4 | 2 | 16 Mt à 31 Mt |
| gen-cote-d-ivoire-3 | Côte d'Ivoire | 1 | 1 | 2 | 2 | 552 kt à 919 kt |
| gen-espagne-1 | Espagne | 1 | 1 | 1 | 2 | 60.1 kt à 163 kt |
| gen-espagne-2 | Espagne | 3 | 1 | 3 | 2 | 1.8 Mt à 3.6 Mt |
| gen-espagne-3 | Espagne | 1 | 1 | 3 | 2 | 3.2 Mt à 10 Mt |
| gen-espagne-4 | Espagne | 1 | 1 | 3 | 2 | 3 Mt à 11 Mt |
| gen-france-1 | France | 5 | 2 | 1 | 2 | 176 kt à 660 kt |
| gen-france-2 | France | 5 | 2 | 3 | 2 | 1.5 Mt à 4.1 Mt (+4 à sourcer) |
| gen-france-3 | France | 9 | 3 | 4 | 2 | 25 Mt à 54 Mt (+4 à sourcer) |
| gen-france-4 | France | 1 | 1 | 1 | 2 | 324 kt à 562 kt |
| gen-france-5 | France | 2 | 1 | 1 | 2 | 60.5 kt à 144 kt (+1 à sourcer) |
| gen-grece-1 | Grèce | 1 | 1 | 1 | 2 | 84.6 kt à 207 kt |
| gen-grece-2 | Grèce | 1 | 1 | 1 | 2 | 119 kt à 313 kt |
| gen-georgie-1 | Géorgie | 1 | 1 | 1 | 2 | 70.5 kt à 149 kt |
| gen-inde-1 | Inde | 1 | 1 | 1 | 2 | 225 kt à 539 kt |
| gen-inde-2 | Inde | 1 | 1 | 3 | 2 | 2.5 Mt à 4.2 Mt |
| gen-inde-3 | Inde | 2 | 1 | 5 | 2 | 97 Mt à 1.6e+02 Mt |
| gen-inde-4 | Inde | 2 | 1 | 5 | 2 | 2.1e+02 Mt à 3.5e+02 Mt |
| gen-iran-1 | Iran | 1 | 1 | 1 | 2 | 166 kt à 438 kt |
| gen-italie-1 | Italie | 1 | 1 | 1 | 2 | 1.84 kt à 2.44 kt |
| gen-italie-2 | Italie | 1 | 1 | 3 | 2 | 5 Mt à 8.8 Mt |
| gen-italie-3 | Italie | 3 | 1 | 2 | 2 | 824 kt à 1.6 Mt |
| gen-italie-4 | Italie | 1 | 1 | 2 | 2 | 1 Mt à 2.1 Mt |
| gen-malaisie-1 | Malaisie | 1 | 1 | 4 | 2 | 18 Mt à 25 Mt |
| gen-malaisie-2 | Malaisie | 2 | 1 | 4 | 2 | 9.3 Mt à 14 Mt |
| gen-malaisie-3 | Malaisie | 1 | 1 | 3 | 2 | 2.1 Mt à 3.4 Mt |
| gen-maroc-1 | Maroc | 3 | 1 | 3 | 2 | 2.5 Mt à 12 Mt |
| gen-mexique-1 | Mexique | 1 | 1 | 1 | 2 | 31.4 kt à 42.9 kt |
| gen-mexique-2 | Mexique | 2 | 1 | 4 | 2 | 14 Mt à 18 Mt |
| gen-mexique-3 | Mexique | 3 | 1 | 4 | 2 | 20 Mt à 34 Mt (+1 à sourcer) |
| gen-mexique-4 | Mexique | 1 | 1 | 1 | 2 | À SOURCER |
| gen-moldavie-1 | Moldavie | 1 | 1 | 1 | 2 | 109 kt à 342 kt |
| gen-nouvelle-zelande-1 | Nouvelle-Zélande | 1 | 1 | 1 | 2 | 51.9 kt à 113 kt |
| gen-philippines-1 | Philippines | 2 | 1 | 3 | 2 | 5 Mt à 7.3 Mt |
| gen-philippines-2 | Philippines | 2 | 1 | 3 | 2 | 4.9 Mt à 8.3 Mt |
| gen-philippines-3 | Philippines | 2 | 1 | 4 | 2 | 23 Mt à 32 Mt |
| gen-portugal-1 | Portugal | 6 | 2 | 2 | 2 | 673 kt à 1.5 Mt (+2 à sourcer) |
| gen-perou-1 | Pérou | 1 | 1 | 1 | 2 | 52.7 kt à 114 kt |
| gen-roumanie-1 | Roumanie | 1 | 1 | 1 | 2 | 240 kt à 497 kt |
| gen-russie-1 | Russie | 1 | 1 | 1 | 2 | 109 kt à 253 kt |
| gen-suisse-1 | Suisse | 2 | 1 | 1 | 2 | 274 kt à 694 kt |
| gen-turquie-1 | Turquie | 1 | 1 | 2 | 2 | 558 kt à 1.2 Mt |
| gen-viet-nam-1 | Viêt Nam | 5 | 2 | 5 | 2 | 50 Mt à 71 Mt |
| gen-egypte-1 | Égypte | 1 | 1 | 1 | 2 | 116 kt à 240 kt |
| gen-equateur-1 | Équateur | 4 | 2 | 3 | 2 | 6.8 Mt à 13 Mt |
| gen-etats-unis-1 | États-Unis | 1 | 1 | 1 | 2 | 61.4 kt à 85.8 kt |
| gen-etats-unis-2 | États-Unis | 1 | 1 | 2 | 2 | 1.3 Mt à 2.3 Mt |
| gen-etats-unis-3 | États-Unis | 3 | 1 | 3 | 2 | 4.4 Mt à 7.7 Mt |
| gen-etats-unis-4 | États-Unis | 1 | 1 | 4 | 2 | 36 Mt à 64 Mt |
| gen-etats-unis-5 | États-Unis | 1 | 1 | 5 | 2 | 2.8e+02 Mt à 4.7e+02 Mt |

Total : 88 trios v1.6 → 208 trios v1.7, 162 opérateurs (inchangés), 81 hubs sur 32 pays.

## Garde-fous

- Étiquette SYNTHÉTIQUE sur toute la flotte simulée — registre de DÉVELOPPEMENT, jamais le registre Merkle de production. Devant un investisseur, on dit simulation, toujours.
- Aucune valeur calibrée, aucun paramètre VDE (Vignite Decision Engine), aucune clé, aucun secret (doctrine PI, voir 00-gouvernance/GARDE_FOUS_PI.md).
- Les ratios de résidus restent ILLUSTRATION et non calibrants. Les gisements sont nationaux : la convention « brut national » est documentée dans chaque fiche d'origine, la décomposition régionale addressable reste À SOURCER (P3).
- Les points sans équivalent FAOSTAT ne reçoivent jamais de valeur inventée : étiquette À SOURCER, exclusion du numérique.
- La simulation éprouve la logique, jamais la physique : la qualification reste le monopole des FAT/SAT (Factory Acceptance Test / Site Acceptance Test) sur machines réelles.

## Régénération du snapshot

Le snapshot engine/gisements-faostat-snapshot-v17.json est versionné : la régénération n'est nécessaire que si FAOSTAT met à jour son bulk. Procédure :

1. Télécharger le bulk normalisé (URL en tête de ce document) et vérifier taille 33 921 825 octets et md5 1a202c5674dce152f1134fa87b220b82. Si le md5 change, la série FAOSTAT a bougé : re-dériver, dater et documenter la nouvelle référence, mettre à jour la provenance du snapshot et les constantes CONTROLES_DOCTRINE du module.
2. Extraire dans cache-faostat-bulk/ (jamais versionné, doctrine en vigueur).
3. Filtrer sur les 33 pays du référentiel, les éléments Production et Area harvested, la fenêtre 2020-2024 (cache de travail local, jamais versionné).
4. Reconstituer le snapshot : les seules séries des couples pays/item référencés par MAPPINGS et par CONTROLES_DOCTRINE (599 séries à date), triées, avec la provenance complète (URL, taille, md5, licence, fenêtre, dates).
5. Contrôler : python3 engine/gisements_hubs.py verifier — VERDICT OK exigé (contrôles doctrine 2024, reproductions des fiches, couverture des 138 points).
6. Re-valider la flotte : python3 engine/flotte_monde.py sommaire puis monte-carlo — toute variation de composition (208 trios à date) doit être comprise et re-documentée avant poussée.

## Validations effectuées (31/10/2026)

- Vérifieur engine/gisements_hubs.py : VERDICT OK — 11 contrôles doctrine FAOSTAT 2024 (tolérance 2 %), 92 reproductions de fiches à l'identique, couverture des 138 points généralisés (123 sourcés, 15 À SOURCER, aucun manquant, aucun pays erroné).
- engine/flotte_monde.py v1.7 : py_compile OK, double run déterministe à l'identique (graines figées), run complet en environ 2 secondes, monte-carlo 3 graines (disponibilité 99,7 %).
- Octet-identité : les deux fichiers de spécification patchés (README.md, sources-donnees.md) ont été reconstruits et vérifiés contre le SHA de blob GitHub du dépôt avant patch — aucune régression involontaire du texte historique.

## Lancement

    python3 engine/gisements_hubs.py verifier     # contrôles croisés et couverture
    python3 engine/gisements_hubs.py table TOKEN  # fiche de gisement d'un point
    python3 engine/flotte_monde.py sommaire      # composition de la flotte V1.7
    python3 engine/flotte_monde.py flotte         # table des 81 hubs
    python3 engine/flotte_monde.py run HUB        # run d'un hub seul
    python3 engine/flotte_monde.py monte-carlo N  # runs multi-graines

Bibliothèque standard uniquement, aucune dépendance, graine déterministe. Le snapshot versionné garantit un run hors ligne sans réseau.
