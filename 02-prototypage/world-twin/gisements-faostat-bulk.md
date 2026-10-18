# Gisements FAOSTAT bulk multi-pays — productions et surfaces réelles des sept hubs (v0.9)

Vague P2.5 du plan World Twin : l'atlas v0.5 documentait les gisements par hub à partir de sources publiques croisées ; cette vague branche l'extraction bulk FAOSTAT proprement dite — les séries nationales officielles, six cultures, six pays, 2019-2024 — et les confronte aux ancres régionales de l'atlas. La maille nationale encadre ; la maille régionale décide : chaque part régionale reste étiquetée À SOURCER tant qu'elle n'a pas son sourcing complet (gisement, ratio, volumes). C'est la dernière vague de P2.

## 1. Méthode

- Source : FAOSTAT, domaine « Production : Crops and livestock products », fichier normalisé en masse (bulk) — https://bulks-faostat.fao.org/production/Production_Crops_Livestock_E_All_Data_(Normalized).zip — sans clé, contrairement à l'API faostatservices.fao.org. Licence : CC BY 4.0 (politique FAO d'open data licensing pour les bases statistiques) — diffusion permise avec attribution.
- Version : mise à jour FAO du 31/12/2025, série 1961-2024 ; ZIP d'environ 34 Mo, CSV interne d'environ 545 Mo. L'extrait filtré (six pays, six cultures, deux éléments, historique complet : 3 712 lignes) est mis en cache dans cache-faostat-bulk/ (jamais versionné) ; les options --annees filtrent ensuite en mémoire, sans nouveau téléchargement.
- Extraction : le 18/10/2026 ; éléments retenus : Area harvested (ha) et Production (t).
- Pièges de filtrage constatés et documentés :
  - le bulk nomme les pays en ANGLAIS (Switzerland, Italy, Spain, Argentina, Morocco) alors que monde.py les nomme en français — la traduction est explicite dans engine/faostat_bulk.py, un pays non mappé lève une erreur de couverture, jamais un zéro silencieux ;
  - l'item noix s'écrit « Walnuts, in shell » (virgule) dans le CSV du bulk mais « Walnuts; in shell » (point-virgule) dans le fichier des codes — incohérence FAOSTAT source d'un piège de filtrage ;
  - la yerba mate s'appelle « Maté leaves » (code 671).
- Vérification d'extraction : les quatre valeurs France de l'extraction v0.1 (17/10/2026, même bulk) sont reproduites À L'IDENTIQUE — raisin 4 747 450 t, maïs 14 670 620 t, riz paddy 71 960 t, noix 27 710 t (écart 0,0 %, voir croisement).
- Module : engine/faostat_bulk.py (stdlib uniquement, monde.py NON modifié — doctrine). Les gisements dérivés sont des REPÈRES DOCUMENTAIRES : les ratios de conversion sont étiquetés SOURCÉ ou ILLUSTRATION à l'identique de la v0.1 et de l'atlas v0.5, jamais des calibrages du moteur.
- Couverture contrôlée au lancement : chaque hub, pays et biomasse de monde.py doit avoir sa culture FAOSTAT et au moins une valeur sur la fenêtre demandée.

## 2. Vue d'ensemble 2024 — six pays, six cultures

| Pays | Raisin t | Vigne ha | Maïs t | Olives t | Riz t | Noix t | Maté t |
| --- | --- | --- | --- | --- | --- | --- | --- |
| France | 4 747 450 | 741 330 | 14 670 620 | 28 200 | 71 960 | 27 710 | — |
| Suisse | 95 600 | 14 484 | 156 750 | — | — | — | — |
| Italie | 7 637 640 | 715 790 | 4 940 530 | 2 299 660 | 1 448 760 | — | — |
| Espagne | 5 387 270 | 903 980 | 3 500 060 | 8 310 250 | 605 820 | — | — |
| Argentine | 1 918 974 | 199 946 | 57 494 500 | 347 381 | 1 264 770 | — | 986 738 |
| Maroc | 339 673 | 40 032 | 73 227 | 1 079 874 | 6 006 | — | — |

Toutes ces valeurs sont DONNÉES RÉELLES (FAOSTAT bulk, licence CC BY 4.0), campagne 2024, dernier millésime du bulk. Les cultures hors périmètre des hubs (maïs suisse ou espagnol, olives françaises) figurent dans l'extrait mais n'alimentent aucun gisement de hub.

## 3. Séries par hub (2019-2024)

### 3.1 fr-rhone — France (sarments, marc, rafles de maïs, paille de riz, coques de noix)

| Élément | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
| --- | --- | --- | --- | --- | --- | --- |
| Vigne ha | 755 470 | 759 590 | 757 830 | 757 550 | 753 340 | 741 330 |
| Raisin t | 5 489 650 | 5 857 870 | 5 073 590 | 6 199 950 | 6 205 260 | 4 747 450 |
| Maïs ha | 1 506 100 | 1 730 030 | 1 549 470 | 1 456 090 | 1 314 680 | 1 593 920 |
| Maïs t | 12 845 020 | 13 726 410 | 15 358 290 | 10 877 190 | 12 834 600 | 14 670 620 |
| Riz ha | 15 100 | 14 320 | 12 030 | 11 760 | 12 120 | 13 480 |
| Riz t | 82 570 | 75 460 | 62 340 | 64 480 | 68 270 | 71 960 |
| Noix ha | 25 880 | 27 180 | 26 850 | 26 900 | 26 870 | 26 830 |
| Noix t | 34 950 | 38 060 | 37 740 | 49 680 | 31 380 | 27 710 |

Lecture : le millésime 2024 est une année de gel pour la vigne (−23,5 % de raisin vs 2023) — l'extraction v0.1 avait déjà retenu la fourchette plutôt que le seul 2024 pour les sarments. Le maïs rebondit (+14,3 %) après la sécheresse 2022. En 1961, la vigne française couvrait 1 418 000 ha : elle a fondu de moitié en soixante ans — le gisement de sarments suit la surface, pas le rendement.

### 3.2 ch-leman — Suisse (sarments, marc)

| Élément | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
| --- | --- | --- | --- | --- | --- | --- |
| Vigne ha | 14 704 | 14 696 | 14 629 | 14 606 | 14 569 | 14 484 |
| Raisin t | 124 061 | 105 739 | 77 290 | 125 681 | 127 853 | 95 600 |

Lecture : 2021 est une année de gel (raisin −38 % vs 2019) ; la surface est d'une stabilité remarquable (±1,5 % sur six ans). L'ancre OFAG de l'atlas v0.5 (14 793 ha) concorde avec FAOSTAT à 2,1 % près — deux institutions, une même vigne.

### 3.3 it-puglia — Italie (grignons, sarments)

| Élément | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
| --- | --- | --- | --- | --- | --- | --- |
| Olivier ha | 1 139 470 | 1 145 520 | 1 129 000 | 1 076 520 | 1 080 060 | 1 083 010 |
| Olives t | 2 194 110 | 2 207 150 | 2 270 630 | 2 160 400 | 2 397 880 | 2 299 660 |
| Vigne ha | 697 910 | 703 900 | 702 670 | 709 890 | 713 350 | 715 790 |
| Raisin t | 7 900 120 | 8 222 360 | 8 149 400 | 8 437 970 | 6 668 830 | 7 637 640 |

Lecture : l'oléiculture italienne alterne autour de 2,2-2,4 Mt ; le rendement huile implicite de l'ancre ISMEA (241 kt d'huile en 2022) ressort à 11,2 % des olives FAOSTAT — bas de la fourchette 15-20 %, cohérent avec les olives de table et une année basse.

### 3.4 es-extremadura — Espagne (grignons, sarments)

| Élément | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
| --- | --- | --- | --- | --- | --- | --- |
| Olivier ha | 2 601 900 | 2 623 720 | 2 623 290 | 2 635 280 | 2 651 110 | 2 645 680 |
| Olives t | 5 965 080 | 8 137 810 | 8 256 550 | 3 940 070 | 5 101 010 | 8 310 250 |
| Vigne ha | 936 890 | 931 630 | 929 390 | 922 920 | 913 000 | 903 980 |
| Raisin t | 5 745 450 | 6 817 770 | 6 086 920 | 5 902 040 | 4 822 760 | 5 387 270 |

Lecture : l'Espagne est la première oliveraie du monde et elle alterne du simple au double (8,26 Mt en 2021, 3,94 Mt en 2022, −52 % ; 8,31 Mt en 2024). Le rendement huile implicite de l'ancre MAPA (765,3 kt prévus 2023/24) ressort à 15,0 % des olives 2023 — bas de fourchette, l'année 2023 étant elle-même un creux. Une ressource qui varie du simple au double appelle une logique de flotte mobile, pas d'usine fixe.

### 3.5 ar-cuyo — Argentine (restes de taille)

| Élément | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
| --- | --- | --- | --- | --- | --- | --- |
| Vigne ha | 215 169 | 214 798 | 211 099 | 207 047 | 204 847 | 199 946 |
| Raisin t | 2 519 886 | 2 055 746 | 2 241 420 | 1 936 803 | 1 455 312 | 1 918 974 |

Lecture : le vignoble argentin descend doucement (−7,1 % de surface en six ans) ; 2023 est un point bas de production (1 455 312 t, gel) et 2024 reste 24 % sous le niveau de 2019. L'ancre INV Mendoza (145 393 ha en 2024) ressort à 72,7 % de la surface nationale FAOSTAT — exactement la fourchette 70-75 % de l'atlas v0.5.

### 3.6 ar-misiones — Argentine (yerba mate)

| Élément | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
| --- | --- | --- | --- | --- | --- | --- |
| Maté ha | 172 650 | 177 530 | 192 436 (I) | 209 277 | 222 169 | 230 256 |
| Maté t | 837 054 | 813 454 | 807 184 (I) | 829 237 | 774 168 | 986 738 |

Lecture : la yerba mate pousse partout — +33 % de surface en six ans, production record 2024 (986 738 t, flag FAOSTAT « I » = imputée sur 2021 uniquement). Les ancres INYM de l'atlas (≈ 210 kha plantés, ≈ 880 kt de feuille verte ~2020) concordent : écart 9,6 % sur la surface, 12,1 % sur la production (croissance réelle entre-temps).

### 3.7 ma-atlas — Maroc (grignons)

| Élément | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
| --- | --- | --- | --- | --- | --- | --- |
| Olivier ha | 1 073 493 | 1 068 895 | 1 104 083 | 1 201 308 | 1 160 032 | 1 238 815 |
| Olives t | 1 912 238 | 1 409 266 | 1 590 504 | 1 968 111 | 988 044 | 1 079 874 |

Lecture : le verger marocain s'étend (+15,4 % de surface en six ans — plantation), mais la production alterne du simple au double (1,97 Mt en 2022, 0,99 Mt en 2023, −50 %) : alternance bisannuelle et sécheresse. Les ancres de l'atlas sont identiques à FAOSTAT pour 2021/22 (1,968 Mt, écart 0,0 %) et à 0,7 % pour 2023/24 ; l'oliveraie Fès-Meknès (320 kha) ressort à 25,8 % de la surface nationale FAOSTAT 2024 — l'atlas disait « plus de 32 % » sur la base du verger national d'alors (environ 1 Mha) : l'écart mesure la croissance du verger national, pas une contradiction.

## 4. Croisement avec l'atlas v0.5

Chaque ancre régionale de l'atlas est confrontée arithmétiquement à la série nationale FAOSTAT (le module engine/faostat_bulk.py croisement tranche les verdicts, jamais à l'œil) :

| Hub | Ancre atlas v0.5 | Valeur atlas | FAOSTAT | Verdict |
| --- | --- | --- | --- | --- |
| fr-rhone | Raisin 2024 (extraction v0.1) | 4 747 450 t | 4 747 450 t | IDENTIQUE (écart 0,0 %) |
| fr-rhone | Maïs grain 2024 (extraction v0.1) | 14 670 620 t | 14 670 620 t | IDENTIQUE (écart 0,0 %) |
| fr-rhone | Riz paddy 2024 (extraction v0.1) | 71 960 t | 71 960 t | IDENTIQUE (écart 0,0 %) |
| fr-rhone | Noix 2024 (extraction v0.1) | 27 710 t | 27 710 t | IDENTIQUE (écart 0,0 %) |
| ch-leman | Vigne suisse OFAG | 14 793 ha | 14 484 ha (2024) | CONCORDANT (écart 2,1 %) |
| it-puglia | Huile Italie 2022 ISMEA/Agea | 241 000 t | rendement implicite 11,2 % | COHÉRENT (fourchette 8-25 %) |
| es-extremadura | Huile prévue 2023/24 MAPA | 765 300 t | rendement implicite 15,0 % | COHÉRENT (fourchette 8-25 %) |
| es-extremadura | Oliveraie Estrémadure | > 300 000 ha | 11,3 % du national | PART RÉGIONALE CONFIRMÉE |
| ar-cuyo | Vignes Mendoza 2024 INV | 145 393 ha | 72,7 % du national | PART RÉGIONALE CONFIRMÉE (70-75 % atlas) |
| ar-misiones | Yerba plantée INYM | 210 000 ha | 230 256 ha (2024) | CONCORDANT (écart 9,6 %) |
| ar-misiones | Feuille verte INYM ~2020 | 880 000 t | 986 738 t (2024) | CONCORDANT EN ORDRE DE GRANDEUR (écart 12,1 %) |
| ma-atlas | Olives 2021/22 | 1 968 111 t | 1 968 111 t (2022) | IDENTIQUE (écart 0,0 %) |
| ma-atlas | Olives 2023/24 | 1 072 000 t | 1 079 874 t (2024) | CONCORDANT (écart 0,7 %) |
| ma-atlas | Oliveraie Fès-Meknès | 320 000 ha | 25,8 % du national 2024 | PART RÉGIONALE COHÉRENTE (verger national en croissance) |

Lecture : l'extraction bulk v0.9 REVALIDE la totalité de l'extraction France v0.1 et confirme chaque ancre régionale de l'atlas — aucune contradiction, deux écarts documentés (rendement huile bas en année creuse, verger marocain en croissance). L'atlas garde la maille régionale ; FAOSTAT apporte la maille nationale et la profondeur historique : les deux couches se tiennent.

## 5. Gisements nationaux dérivés (campagne 2024)

Ratios documentaires à l'identique de la v0.1 et de l'atlas v0.5 — jamais des calibrages. La maille est NATIONALE : chaque part régionale reste À SOURCER.

| Hub | Biomasse | Base 2024 | Gisement dérivé t/an | Ratio |
| --- | --- | --- | --- | --- |
| fr-rhone | sarments-vigne | 741 330 ha | 593 064 → 815 463 | 0,8-1,1 t/ha/an — SOURCÉ |
| fr-rhone | marc-raisin | 4 747 450 t | 474 745 → 1 424 235 | 10-30 % vendange — SOURCÉ |
| fr-rhone | mais-rdm (rafles) | 14 670 620 t | 2 200 593 → 2 934 124 | 15-20 % du grain — ILLUSTRATION |
| fr-rhone | paille-riz | 71 960 t | 71 960 → 107 940 | 1,0-1,5 × paddy — ILLUSTRATION |
| fr-rhone | coques-noix | 27 710 t | 13 855 → 18 012 | 50-65 % en coques — ILLUSTRATION |
| ch-leman | sarments-vigne | 14 484 ha | 11 587 → 15 932 | 0,8-1,1 t/ha/an — SOURCÉ |
| ch-leman | marc-raisin | 95 600 t | 9 560 → 28 680 | 10-30 % vendange — SOURCÉ |
| it-puglia | grignons-olive | 2 299 660 t | 919 864 → 1 379 796 | 0,4-0,6 t/t triturée — ILLUSTRATION |
| it-puglia | sarments-vigne | 715 790 ha | 572 632 → 787 369 | 0,8-1,1 t/ha/an — SOURCÉ |
| es-extremadura | grignons-olive | 8 310 250 t | 3 324 100 → 4 986 150 | 0,4-0,6 t/t triturée — ILLUSTRATION |
| es-extremadura | sarments-vigne | 903 980 ha | 723 184 → 994 378 | 0,8-1,1 t/ha/an — SOURCÉ |
| ar-cuyo | restos-poda | 199 946 ha × 70-75 % | 111 970 → 164 955 | 0,8-1,1 t/ha/an — SOURCÉ ; part Mendoza 70-75 % — ILLUSTRATION |
| ar-misiones | yerba-mate | 986 738 t | 986 738 | GISSEMENT DIRECT (la feuille est la biomasse) |
| ma-atlas | grignons-olive | 1 079 874 t | 431 950 → 647 924 | 0,4-0,6 t/t triturée — ILLUSTRATION |

Lecture : sur les seules bases nationales 2024, le gisement documentaire cumulé des quatorze lignes atteint 10,4 à 15,3 Mt/an — dominé par l'oléiculture ibérique (grignons d'Estrémadure : 3,3-5,0 Mt à lui seul) et les rafles de maïs françaises (2,2-2,9 Mt). Hypothèses documentées : olives triturées ≈ production (olives de table non soustraites) ; maille nationale, parts régionales À SOURCER.

## 6. Limites honnêtes

- La maille FAOSTAT est NATIONALE : Puglia, Estrémadure, Mendoza, Misiones, Fès-Meknès et les bassins français ne se déduisent PAS d'une moyenne nationale — chaque part régionale exige son sourcing propre avant toute ingestion dans monde.py (doctrine À SOURCER).
- Les campagnes oléicoles alternent (Espagne et Maroc : du simple au double) : un gisement dérivé sur le seul 2024 est un millésime, pas une moyenne ; la série 2019-2024 est dans le module pour encadrer.
- Les gisements dérivés reposent sur des ratios documentaires (SOURCÉ pour les sarments et le marc, ILLUSTRATION pour grignons, rafles, paille, coques) : ils encadrent des ordres de grandeur, ils ne qualifient rien — la qualification reste le monopole des FAT/SAT.
- Flags FAOSTAT : « A » (donnée officielle) domine ; la yerba mate 2021 est imputée (« I ») ; certaines années espagnoles ou argentines peuvent être révisées par la FAO.
- Le bulk est écrasé par la FAO sous le même nom au fil des mises à jour : la version utilisée ici (mise à jour du 31/12/2025, extraite le 18/10/2026) est datée dans le module pour reproductibilité.
- Les volumes téléchargés (ZIP, CSV) vivent hors du dépôt (cache-faostat-bulk/, motif du .gitignore) ; seules les séries agrégées et étiquetées sont versionnées.

## 7. Reproductibilité

```
python3 engine/faostat_bulk.py                 # sommaire des sept hubs
python3 engine/faostat_bulk.py fr-rhone        # fiche d'un hub (séries 2019-2024)
python3 engine/faostat_bulk.py croisement       # croisement avec l'atlas v0.5
python3 engine/faostat_bulk.py --annees 2000 2004   # fenêtre arbitraire (cache)
python3 engine/faostat_bulk.py --sans-telechargement  # cache local uniquement
```

Premier run : téléchargement d'environ 34 Mo. monde.py n'est ni lu pour calibration ni modifié ; les gisements dérivés restent des repères documentaires étiquetés.
