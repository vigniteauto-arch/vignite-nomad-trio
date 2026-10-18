# FIRMS historique multi-saison — cartographie pluriannuelle du brûlage (v0.8)

Vague P2.4 du plan World Twin : prolonger la couche FIRMS du jour (v0.3, détections NRT) par une cartographie PLURIANNUELLE — cinq saisons complètes, 2021 à 2025, dix bassins, deux hémisphères. La couche du jour dit où brûle aujourd'hui ; cette couche dit quand brûle toujours. C'est elle qui conditionne les fenêtres d'opération, les priorités de hub et le message « remplacement du brûlage ».

## 1. Méthode

- Source : NASA FIRMS, résumés annuels par pays (« Country Yearly Summary »), CSV publics téléchargeables SANS MAP_KEY (https://firms.modaps.eosdis.nasa.gov/country/ — liste des fichiers dans /data/country/yearly_summary_files.txt, constaté le 18/10/2026). Différence clé avec la couche v0.3 : aucun secret requis, aucune transaction API consommée.
- Capteur : VIIRS S-NPP 375 m (VNP14IMGTDL), série continue depuis 2012, meilleure détection des petits feux que MODIS 1 km. Alternatives paramétrables : viirs-jpss1 (NOAA-20, depuis 2018), modis (depuis 2000).
- Période : 2021-2025, cinq saisons complètes (fichiers 2025 consolidés le 10/10/2026).
- Filtres d'honnêteté :
  - sources statiques (type 1 : torchères, volcans) exclues ;
  - filtre de quasi-permanence : une cellule de 0,01 degré (environ 1 km) active au moins 9 mois sur 12 est une source FIXE (industrie, décharge), jamais un brûlage saisonnier — exclue et comptée à part. Sans ce filtre, la boîte camargue (corridor industrialo-portuaire de Fos-sur-Mer) affiche 16 868 détections « réparties » toute l'année ; avec le filtre, 1 893 détections réellement saisonnières ;
  - une détection de feu n'est pas une preuve de brûlage agricole : les tableaux ci-dessous sont DONNÉES RÉELLES (NASA FIRMS) ; l'attribution de cause est INFÉRENCE, croisée avec les calendriers culturaux (v0.7) et la réglementation (v0.6).
- Verdicts mensuels : RÉCURRENT (mois portant des détections dans au moins 80 % des saisons), OCCASIONNEL (au moins 40 %), RARE (une saison), ABSENT.
- Module : engine/firms_histo.py (stdlib uniquement, monde.py NON modifié — doctrine). Premier run : téléchargement d'environ 100 Mo (l'essentiel vient d'Argentine), mis en cache dans cache-firms-histo/ (jamais versionné).
- Vérification d'extraction : recompte indépendant (hors module) de l'agrégat Périgord/avril — 26 détections, comptes par année identiques au module (9/8/3/0/6).

## 2. Vue d'ensemble des dix bassins

Détections retenues après filtres, saisons 2021-2025 :

| Bassin | Pays | Détections | Exclues (quasi-perm.) | FRP MW | Mois dominants (part) |
| --- | --- | --- | --- | --- | --- |
| vallee-du-rhone | France | 285 | 59 | 1 570 | oct 17 %, août 17 %, avr 13 % |
| camargue | France | 1 893 | 14 975 | 19 640 | juil 15 %, mars 12 %, avr 12 %, oct 11 % |
| perigord | France | 59 | 0 | 220 | avr 44 %, août 19 %, oct 14 % |
| sud-ouest | France | 922 | 0 | 12 668 | juil 53 %, août 36 % (incendies 2022) |
| suisse-leman | Suisse | 56 | 53 | 122 | août 48 %, avr 16 %, mai 16 % |
| italie-puglia | Italie | 8 989 | 73 | 58 364 | juil 34 %, août 28 %, sept 16 % |
| espagne-extremadure | Espagne | 1 503 | 0 | 13 657 | oct 19 %, août 17 %, juil 16 % |
| argentine-cuyo | Argentine | 5 218 | 736 | 45 722 | août 21 %, sept 18 %, juil 13 %, oct 13 % |
| argentine-misiones | Argentine | 11 958 | 173 | 89 295 | août 24 %, juil 14 %, fév 11 % |
| maroc-atlas | Maroc | 831 | 163 | 18 485 | août 28 %, juil 15 %, oct 10 % |

Lecture immédiate : quatre bassins sur dix culminent en août — pour des raisons opposées. Été méditerranéen au nord (incendies, chaumes), hiver sec au sud (chaumes, renouvellements) : août est le mois où brûlent les deux hémisphères.

## 3. Saison par saison

### 3.1 vallee-du-rhone (France, 285 détections, FRP 1 570 MW)

| Mois | 2021 | 2022 | 2023 | 2024 | 2025 | Total | Part % | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 0 | 2 | 0 | 4 | 1,4 | OCCASIONNEL |
| 2 | 1 | 6 | 3 | 6 | 2 | 18 | 6,3 | RÉCURRENT |
| 3 | 4 | 18 | 5 | 3 | 2 | 32 | 11,2 | RÉCURRENT |
| 4 | 18 | 8 | 1 | 4 | 7 | 38 | 13,3 | RÉCURRENT |
| 5 | 0 | 5 | 4 | 4 | 4 | 17 | 6,0 | RÉCURRENT |
| 6 | 3 | 13 | 1 | 5 | 2 | 24 | 8,4 | RÉCURRENT |
| 7 | 5 | 12 | 1 | 4 | 4 | 26 | 9,1 | RÉCURRENT |
| 8 | 35 | 1 | 3 | 6 | 3 | 48 | 16,8 | RÉCURRENT |
| 9 | 4 | 4 | 0 | 3 | 6 | 17 | 6,0 | RÉCURRENT |
| 10 | 14 | 5 | 8 | 8 | 14 | 49 | 17,2 | RÉCURRENT |
| 11 | 1 | 1 | 0 | 0 | 6 | 8 | 2,8 | OCCASIONNEL |
| 12 | 2 | 0 | 0 | 2 | 0 | 4 | 1,4 | OCCASIONNEL |

Profil en deux bosses : printemps (février-avril, tailles et nettoyages) et octobre (vendanges, andains). Exception : août 2021 concentre à lui seul 666 MW (42 % du cumul du bassin) sur 35 détections — signature d'un événement estival, pas d'une habitude. Volume modeste : le brûlage y est encadré, pas éteint.

### 3.2 sud-ouest (France, 922 détections, FRP 12 668 MW)

| Mois | 2021 | 2022 | 2023 | 2024 | 2025 | Total | Part % | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 | 1 | 1 | 0,1 | RARE |
| 2 | 2 | 0 | 0 | 0 | 0 | 2 | 0,2 | RARE |
| 3 | 1 | 0 | 8 | 1 | 0 | 10 | 1,1 | OCCASIONNEL |
| 4 | 13 | 0 | 0 | 0 | 4 | 17 | 1,8 | OCCASIONNEL |
| 5 | 0 | 0 | 2 | 3 | 0 | 5 | 0,5 | OCCASIONNEL |
| 6 | 0 | 3 | 2 | 1 | 0 | 6 | 0,7 | OCCASIONNEL |
| 7 | 0 | 482 | 1 | 2 | 5 | 490 | 53,1 | RÉCURRENT |
| 8 | 0 | 297 | 16 | 16 | 7 | 336 | 36,4 | RÉCURRENT |
| 9 | 1 | 14 | 14 | 0 | 9 | 38 | 4,1 | RÉCURRENT |
| 10 | 3 | 2 | 4 | 2 | 6 | 17 | 1,8 | RÉCURRENT |
| 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0,0 | ABSENT |
| 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0,0 | ABSENT |

Signal dominé par l'événement, pas par l'habitude : juillet-août 2022 portent à eux seuls 85 % des détections de la période (779 sur 922), cohérent avec les grands incendies de Landiras (Gironde, juillet-août 2022) — INFÉRENCE. Le brûlage agricole de chaumes (octobre) est quant à lui quasi nul : 17 détections en cinq ans. Sur le maïs, le pain point français n'est pas le brûlage, c'est la ressource abandonnée — le pitch est l'approvisionnement, pas le sauvetage.

### 3.3 camargue (France, 1 893 détections, FRP 19 640 MW, 14 975 quasi-permanentes exclues)

| Mois | 2021 | 2022 | 2023 | 2024 | 2025 | Total | Part % | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 6 | 37 | 20 | 17 | 15 | 95 | 5,0 | RÉCURRENT |
| 2 | 13 | 46 | 46 | 39 | 23 | 167 | 8,8 | RÉCURRENT |
| 3 | 86 | 49 | 40 | 29 | 28 | 232 | 12,3 | RÉCURRENT |
| 4 | 98 | 32 | 38 | 28 | 31 | 227 | 12,0 | RÉCURRENT |
| 5 | 8 | 25 | 25 | 13 | 15 | 86 | 4,5 | RÉCURRENT |
| 6 | 15 | 42 | 9 | 15 | 65 | 146 | 7,7 | RÉCURRENT |
| 7 | 24 | 122 | 18 | 10 | 108 | 282 | 14,9 | RÉCURRENT |
| 8 | 68 | 15 | 46 | 39 | 27 | 195 | 10,3 | RÉCURRENT |
| 9 | 23 | 18 | 20 | 21 | 25 | 107 | 5,7 | RÉCURRENT |
| 10 | 64 | 31 | 28 | 23 | 69 | 215 | 11,4 | RÉCURRENT |
| 11 | 23 | 13 | 22 | 9 | 24 | 91 | 4,8 | RÉCURRENT |
| 12 | 7 | 6 | 9 | 26 | 2 | 50 | 2,6 | RÉCURRENT |

Un bassin actif toute l'année, à la fois sauvage (roselières, marais, été) et agricole : le signal rizicole d'octobre-novembre est présent CHAQUE année — 305 détections sur la fenêtre [10,11,12], 18,8 % du bassin. La couche v0.3 du jour (11 détections le 17/10/2026) était donc bien la fenêtre régulière, pas un accident. Attention : 25 cellules quasi-permanentes (Fos-sur-Mer) sont exclues — sans ce filtre, le brûlage agricole serait noyé sous l'industrie.

### 3.4 perigord (France, 59 détections, FRP 220 MW)

| Mois | 2021 | 2022 | 2023 | 2024 | 2025 | Total | Part % | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 2 | 0 | 2 | 3,4 | RARE |
| 2 | 0 | 0 | 1 | 0 | 0 | 1 | 1,7 | RARE |
| 3 | 1 | 1 | 1 | 0 | 1 | 4 | 6,8 | RÉCURRENT |
| 4 | 9 | 8 | 3 | 0 | 6 | 26 | 44,1 | RÉCURRENT |
| 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0,0 | ABSENT |
| 6 | 0 | 0 | 0 | 0 | 1 | 1 | 1,7 | RARE |
| 7 | 0 | 3 | 0 | 0 | 0 | 3 | 5,1 | RARE |
| 8 | 1 | 2 | 2 | 6 | 0 | 11 | 18,6 | RÉCURRENT |
| 9 | 0 | 1 | 0 | 0 | 0 | 1 | 1,7 | RARE |
| 10 | 3 | 1 | 2 | 0 | 2 | 8 | 13,6 | RÉCURRENT |
| 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0,0 | ABSENT |
| 12 | 0 | 0 | 0 | 2 | 0 | 2 | 3,4 | RARE |

Quasi-silence : douze détections par an en moyenne sur un bassin entier. L'interdiction française y est respectée ; les coques de noix ne brûlent pas, elles s'entassent ou partent en chauffage. Le pain point est la valorisation, pas le feu.

### 3.5 suisse-leman (Suisse, 56 détections, FRP 122 MW)

| Mois | 2021 | 2022 | 2023 | 2024 | 2025 | Total | Part % | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 | 1 | 1 | 1,8 | RARE |
| 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0,0 | ABSENT |
| 3 | 0 | 1 | 0 | 0 | 0 | 1 | 1,8 | RARE |
| 4 | 1 | 3 | 2 | 2 | 1 | 9 | 16,1 | RÉCURRENT |
| 5 | 2 | 2 | 1 | 1 | 3 | 9 | 16,1 | RÉCURRENT |
| 6 | 1 | 0 | 1 | 0 | 1 | 3 | 5,4 | OCCASIONNEL |
| 7 | 0 | 1 | 1 | 1 | 0 | 3 | 5,4 | OCCASIONNEL |
| 8 | 8 | 2 | 4 | 9 | 4 | 27 | 48,2 | RÉCURRENT |
| 9 | 0 | 1 | 0 | 1 | 1 | 3 | 5,4 | OCCASIONNEL |
| 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0,0 | ABSENT |
| 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0,0 | ABSENT |
| 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0,0 | ABSENT |

Le bassin le plus silencieux du monde : onze détections par an sur Lavaux, presque toutes estivales. L'OPair (art. 26a, interdiction de l'incinération en plein air, fiche v0.6) est appliquée. En Suisse, le trio Nomad ne vend pas la fin d'un brûlage ; il vend la valorisation de sarments et de marc qui, déjà, ne brûlent pas.

### 3.6 italie-puglia (Italie, 8 989 détections, FRP 58 364 MW)

| Mois | 2021 | 2022 | 2023 | 2024 | 2025 | Total | Part % | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 7 | 2 | 4 | 2 | 17 | 0,2 | RÉCURRENT |
| 2 | 9 | 14 | 4 | 12 | 4 | 43 | 0,5 | RÉCURRENT |
| 3 | 11 | 18 | 22 | 4 | 5 | 60 | 0,7 | RÉCURRENT |
| 4 | 10 | 5 | 11 | 18 | 10 | 54 | 0,6 | RÉCURRENT |
| 5 | 26 | 22 | 5 | 10 | 31 | 94 | 1,0 | RÉCURRENT |
| 6 | 243 | 185 | 31 | 121 | 287 | 867 | 9,6 | RÉCURRENT |
| 7 | 1120 | 601 | 550 | 166 | 611 | 3048 | 33,9 | RÉCURRENT |
| 8 | 863 | 134 | 798 | 243 | 515 | 2553 | 28,4 | RÉCURRENT |
| 9 | 422 | 116 | 414 | 117 | 353 | 1422 | 15,8 | RÉCURRENT |
| 10 | 89 | 104 | 361 | 67 | 116 | 737 | 8,2 | RÉCURRENT |
| 11 | 3 | 28 | 21 | 6 | 10 | 68 | 0,8 | RÉCURRENT |
| 12 | 7 | 1 | 8 | 3 | 7 | 26 | 0,3 | RÉCURRENT |

La bande juin-octobre concentre 95,9 % des détections : c'est la signature des chaumes de blé dur brûlés après la moisson de juin (fenêtre candidate paille-blé-dur À SOURCER du croisement GEOGLAM v0.7) plus les incendies d'été. À l'inverse, les fenêtres oléicoles [11,12,1] et viticoles [2,3] ne portent que 1 à 2 % du signal : les grignons ne brûlent pas (ils partent au moulin), les sarments brûlés sont trop petits ou trop brefs pour le pixel 375 m — mais le gisement, lui, existe. Le trio y a deux marchés : le remplacement du brûlage céréalier (visible de l'espace) et la valorisation oléicole (invisible de l'espace, chiffrée par l'atlas v0.5).

### 3.7 espagne-extremadure (Espagne, 1 503 détections, FRP 13 657 MW)

| Mois | 2021 | 2022 | 2023 | 2024 | 2025 | Total | Part % | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 21 | 2 | 1 | 17 | 42 | 2,8 | RÉCURRENT |
| 2 | 2 | 44 | 19 | 2 | 1 | 68 | 4,5 | RÉCURRENT |
| 3 | 68 | 9 | 8 | 6 | 6 | 97 | 6,5 | RÉCURRENT |
| 4 | 11 | 15 | 11 | 27 | 14 | 78 | 5,2 | RÉCURRENT |
| 5 | 9 | 22 | 5 | 11 | 8 | 55 | 3,7 | RÉCURRENT |
| 6 | 14 | 15 | 11 | 5 | 69 | 114 | 7,6 | RÉCURRENT |
| 7 | 36 | 10 | 25 | 9 | 157 | 237 | 15,8 | RÉCURRENT |
| 8 | 23 | 9 | 4 | 54 | 169 | 259 | 17,2 | RÉCURRENT |
| 9 | 20 | 29 | 5 | 33 | 47 | 134 | 8,9 | RÉCURRENT |
| 10 | 104 | 33 | 12 | 17 | 112 | 278 | 18,5 | RÉCURRENT |
| 11 | 47 | 7 | 12 | 25 | 16 | 107 | 7,1 | RÉCURRENT |
| 12 | 11 | 1 | 3 | 19 | 0 | 34 | 2,3 | RÉCURRENT |

Le seul bassin du monde Nord dont le premier mois est OCTOBRE (18,5 %) : époque de danger Bajo selon les órdenes annuelles de la Junta (fiche v0.6) — on brûle quand la loi desserre. Les deux fenêtres du moteur (grignons [11,12,1,2], sarments [3,4]) sont toutes deux alignées (16,7 % et 11,6 %). La Ley 7/2022 art. 27.3 interdit en principe ; la saisonalité montre l'application réelle.

### 3.8 argentine-cuyo (Argentine, 5 218 détections, FRP 45 722 MW)

| Mois | 2021 | 2022 | 2023 | 2024 | 2025 | Total | Part % | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 45 | 56 | 33 | 38 | 51 | 223 | 4,3 | RÉCURRENT |
| 2 | 13 | 29 | 33 | 28 | 24 | 127 | 2,4 | RÉCURRENT |
| 3 | 12 | 35 | 20 | 27 | 15 | 109 | 2,1 | RÉCURRENT |
| 4 | 43 | 50 | 30 | 35 | 27 | 185 | 3,5 | RÉCURRENT |
| 5 | 57 | 76 | 53 | 20 | 77 | 283 | 5,4 | RÉCURRENT |
| 6 | 50 | 97 | 103 | 38 | 93 | 381 | 7,3 | RÉCURRENT |
| 7 | 228 | 152 | 93 | 93 | 105 | 671 | 12,9 | RÉCURRENT |
| 8 | 270 | 276 | 129 | 148 | 269 | 1092 | 20,9 | RÉCURRENT |
| 9 | 189 | 326 | 108 | 209 | 99 | 931 | 17,8 | RÉCURRENT |
| 10 | 145 | 102 | 263 | 46 | 117 | 673 | 12,9 | RÉCURRENT |
| 11 | 43 | 87 | 88 | 30 | 73 | 321 | 6,2 | RÉCURRENT |
| 12 | 17 | 49 | 17 | 32 | 107 | 222 | 4,3 | RÉCURRENT |

Hémisphère Sud : le pic hivernal (août-septembre, 38,7 %) chevauche la fenêtre restos-poda [6,7,8] — 41,1 % des détections tombent dedans, le meilleur alignement du monde Nord ou Sud avec Misiones. Le régime de la Ley 26.562 (autorisation obligatoire, fiche v0.6) laisse passer un volume de feux massif : 870 à 1 335 détections par saison selon l'année (5 218 en cinq saisons) dans la boîte de Mendoza. Septembre-octobre (30,7 % à eux deux, HORS fenêtre) dessinent la fenêtre candidate des chaumes de blé post-moisson (candidate paille-blé [12,1] du croisement GEOGLAM — la phénologie dit récolte novembre-décembre, le feu parle en septembre-octobre : à sourcer avant toute ingestion).

### 3.9 argentine-misiones (Argentine, 11 958 détections, FRP 89 295 MW)

| Mois | 2021 | 2022 | 2023 | 2024 | 2025 | Total | Part % | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 58 | 424 | 76 | 62 | 113 | 733 | 6,1 | RÉCURRENT |
| 2 | 194 | 830 | 136 | 71 | 55 | 1286 | 10,8 | RÉCURRENT |
| 3 | 202 | 103 | 149 | 169 | 154 | 777 | 6,5 | RÉCURRENT |
| 4 | 289 | 118 | 146 | 122 | 124 | 799 | 6,7 | RÉCURRENT |
| 5 | 221 | 142 | 243 | 21 | 136 | 763 | 6,4 | RÉCURRENT |
| 6 | 59 | 50 | 250 | 377 | 7 | 743 | 6,2 | RÉCURRENT |
| 7 | 583 | 267 | 305 | 137 | 318 | 1610 | 13,5 | RÉCURRENT |
| 8 | 586 | 445 | 617 | 590 | 654 | 2892 | 24,2 | RÉCURRENT |
| 9 | 250 | 259 | 93 | 242 | 201 | 1045 | 8,7 | RÉCURRENT |
| 10 | 90 | 136 | 30 | 91 | 66 | 413 | 3,5 | RÉCURRENT |
| 11 | 91 | 189 | 25 | 49 | 82 | 436 | 3,6 | RÉCURRENT |
| 12 | 201 | 74 | 30 | 88 | 68 | 461 | 3,9 | RÉCURRENT |

Le bassin le plus brûlé du trio (12 000 détections, FRP cumulée 89 295 MW). L'hiver austral (juillet-septembre, 46,4 %) dépasse la fenêtre yerba [4,5,6,9,10,11] (35,1 %) : le pic d'août est la saison sèche — chaumes de tabac et de coton, renouvellements de parcels, feux de bord de pampa. Le cadre provincial reste À VÉRIFIER (fiche v0.6) ; le feu, lui, est vérifié cinq années sur cinq.

### 3.10 maroc-atlas (Maroc, 831 détections, FRP 18 485 MW)

| Mois | 2021 | 2022 | 2023 | 2024 | 2025 | Total | Part % | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 6 | 11 | 10 | 9 | 3 | 39 | 4,7 | RÉCURRENT |
| 2 | 3 | 8 | 6 | 4 | 2 | 23 | 2,8 | RÉCURRENT |
| 3 | 4 | 2 | 20 | 5 | 7 | 38 | 4,6 | RÉCURRENT |
| 4 | 5 | 7 | 5 | 11 | 6 | 34 | 4,1 | RÉCURRENT |
| 5 | 12 | 9 | 2 | 6 | 3 | 32 | 3,9 | RÉCURRENT |
| 6 | 24 | 10 | 14 | 15 | 6 | 69 | 8,3 | RÉCURRENT |
| 7 | 86 | 4 | 10 | 14 | 14 | 128 | 15,4 | RÉCURRENT |
| 8 | 16 | 182 | 7 | 16 | 15 | 236 | 28,4 | RÉCURRENT |
| 9 | 34 | 15 | 10 | 5 | 14 | 78 | 9,4 | RÉCURRENT |
| 10 | 32 | 14 | 19 | 4 | 15 | 84 | 10,1 | RÉCURRENT |
| 11 | 12 | 13 | 9 | 6 | 6 | 46 | 5,5 | RÉCURRENT |
| 12 | 13 | 1 | 6 | 4 | 0 | 24 | 2,9 | RÉCURRENT |

Le profil le plus « permanent » du monde Nord : tous les mois sont récurrents, mais l'été (juillet-août, 43,8 %, dont un pic 2022 cohérent avec la vague d'incendies marocains de l'été 2022 — INFÉRENCE) domine les chaumes céréaliers post-moisson (blé moissonné avril-juillet selon CM4EW, croisement v0.7). La fenêtre oléicole [12,1,2] est alignée mais modeste (10,3 %) : les grignons vont au masar, le brûlage visible est céréalier.

## 4. Croisement des fenêtres du moteur (monde.py, ILLUSTRATION d'origine)

| Hub / biomasse | Fenêtre | Verdict | Part dans la fenêtre |
| --- | --- | --- | --- |
| fr-rhone / sarments-vigne | [1,2,3,4] | FENÊTRE ALIGNÉE SUR UN BRÛLAGE RÉCURRENT | 32,3 % |
| fr-rhone / marc-raisin | [9,10,11] | FENÊTRE ALIGNÉE | 26,0 % |
| fr-rhone / mais-rdm | [10,11,12] | BRÛLAGE RÉCURRENT MAIS MARGINAL | 1,8 % |
| fr-rhone / paille-riz | [10,11,12] | FENÊTRE ALIGNÉE | 18,8 % |
| fr-rhone / coques-noix | [10,11,12,1,2] | CHEVAUCHEMENT PARTIEL | 22,0 % |
| ch-leman / sarments-vigne | [1,2,3] | BRÛLAGE FAIBLE | 3,6 % |
| ch-leman / marc-raisin | [10,11] | AUCUN BRÛLAGE DÉTECTÉ | 0,0 % |
| it-puglia / grignons-olive | [11,12,1] | BRÛLAGE RÉCURRENT MAIS MARGINAL | 1,2 % |
| it-puglia / sarments-vigne | [2,3] | BRÛLAGE RÉCURRENT MAIS MARGINAL | 1,1 % |
| es-extremadura / grignons-olive | [11,12,1,2] | FENÊTRE ALIGNÉE | 16,7 % |
| es-extremadura / sarments-vigne | [3,4] | FENÊTRE ALIGNÉE | 11,6 % |
| ar-cuyo / restos-poda | [6,7,8] | FENÊTRE ALIGNÉE | 41,1 % |
| ar-misiones / yerba-mate | [4,5,6,9,10,11] | FENÊTRE ALIGNÉE | 35,1 % |
| ma-atlas / grignons-olive | [12,1,2] | FENÊTRE ALIGNÉE | 10,3 % |

monde.py reste INCHANGÉ (doctrine : aucune ingestion sans sourcing complet). Les fenêtres candidates À SOURCER du croisement GEOGLAM v0.7 reçoivent ici leur première confirmation par le feu : Puglia [7,8,9] (le pic des chaumes de blé dur), Cuyo [9,10], Maroc [6,7,8]. Gisement, ratio et volumes restent à sourcer avant toute modification du moteur.

## 5. Convergences des trois couches (v0.6 réglementation, v0.7 GEOGLAM, v0.8 FIRMS historique)

- Partout où la loi interdit et est appliquée (Suisse OPair, France L.541-21-1 sur Périgord et le maïs landais), le feu disparaît des données : le pain point devient la valorisation, pas l'extinction.
- Partout où la loi encadre mais n'empêche pas (Argentine Ley 26.562, Estrémadure hors périodes de danger Alto, Puglia céréalière), le feu est visible de l'espace, chaque année, aux mêmes mois : la fenêtre commerciale du trio y est donc prévisible à l'échelle du mois.
- La phénologie (GEOGLAM) prédit la récolte ; FIRMS historique observe la conséquence ; la réglementation (v0.6) encadre le geste. Les trois couches convergent : le trio Nomad se positionne à l'intersection exacte.

## 6. Limites honnêtes

- Une détection de feu n'est pas une preuve de brûlage agricole : les incendies de végétation (Landiras 2022, été marocain 2022) polluent le signal — d'où le verdict « marginal » et la lecture croisée calendriers.
- Le pixel VIIRS (375 m) sous-détecte les feux petits et brefs : les sarments brûlés individuellement sont invisibles ; l'absence de signal ne prouve pas l'absence de brûlage (Suisse, Périgord : interdits ET sous-détectés).
- La FRP est une puissance radiative instantanée, pas une énergie brûlée : les comparaisons inter-bassins sont des ordres de grandeur.
- La boîte carrée n'est pas le bassin : agglomérations (Mendoza, Fès) et corridors industriels (Fos-sur-Mer) y vivent ; le filtre de quasi-permanence atténue, n'élimine pas.
- Cinq saisons ne couvrent pas les extrêmes rares — et 2022 en a justement apporté deux (Landiras, Maroc) : lire les moyennes ET les anomalies.
- Capteur unique (VIIRS S-NPP) : les saisons avant 2012 et la finesse MODIS restent accessibles par paramètre, non explorées ici.

## 7. Sources et reproductibilité

- NASA FIRMS (LANCE) — résumés annuels par pays, CSV : https://firms.modaps.eosdis.nasa.gov/country/ (fichiers viirs-snpp_2021-2025_{France,Switzerland,Italy,Spain,Argentina,Morocco}.csv, téléchargés le 18/10/2026, liste officielle /data/country/yearly_summary_files.txt, mise à jour 10/10/2026 pour l'année 2025).
- Produit VIIRS S-NPP 375 m : VNP14IMGTDL_NRT consolidé en traitement standard dans les archives (FIRMS remplace le NRT par le standard après 2-3 mois, jusqu'à 5 — constat pages officielles FIRMS, 18/10/2026).
- Commandes de reproductibilité : `python3 engine/firms_histo.py` (sommaire), `python3 engine/firms_histo.py camargue` (fiche), `python3 engine/firms_histo.py croisement` (croisement des fenêtres), options `--annees DEBUT FIN`, `--capteur`, `--sans-telechargement`.
- Étiquetage : détections et agrégats = DONNÉES RÉELLES (NASA FIRMS) ; attribution de cause = INFÉRENCE croisée (v0.6, v0.7) ; aucune valeur calibrée ; cache cache-firms-histo/ jamais versionné.
