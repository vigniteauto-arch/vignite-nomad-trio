# World Twin — la flotte mondiale en simulation

Programme World Twin : faire tourner le trio Nomad v1 « comme si » il opérait déjà partout dans le monde — toutes biomasses par pays et région, couplé à la saisonnalité des récoltes, aux pain points locaux (brûlage, réglementation), à la météo et aux points GPS — afin de nourrir le VDE de milliers de lots simulés et de produire le rapport quotidien World Ops, avant même que le premier acier ne soit commandé.

Statut : P2 — flotte monde (Carré d'Or, LatAm, Al-Atlas : 7 hubs, 2 hémisphères). Squelette non calibré, déterministe. Couches réelles branchées : météo ERA5 (10 bassins) et brûlage NASA FIRMS (10 boîtes), le 17/10/2026. V0.5 (17/10/2026) : atlas des gisements mondiaux en données publiques sourcées (les 7 hubs) et lecture des résultats Monte Carlo. V0.6 (17/10/2026) : fiches pays réglementaires — cadre légal du brûlage des résidus pour les 7 hubs. V0.7 (17/10/2026) : croisement GEOGLAM — calendriers culturaux sous-nationaux réels des 7 hubs confrontés aux fenêtres du moteur, conditions de campagne des bulletins AMIS n° 143 et CM4EW n° 120 (28/09/2026, El Niño très fort). V0.8 (18/10/2026) : FIRMS historique multi-saison — cinq saisons complètes de détections réelles (2021-2025) par bassin, filtre des sources fixes, verdicts mensuels, croisement des fenêtres du moteur. V0.9 (18/10/2026) : extraction bulk FAOSTAT multi-pays — productions et surfaces nationales réelles (six pays, six cultures, 2019-2024), gisements documentaires dérivés, croisement avec l'atlas v0.5. V1.0 (18/10/2026) : atlas des biomasses monde — les 52 intrants du master placés sur le globe (familles, points GPS, volumes, saisonnalité, techniques, réglementation, météo temps réelle). V1.1 (18/10/2026) : atlas des biomasses locales par pays — 18 pays, 67 intrants sourcés FAOSTAT bulk 2024 (productions réelles, ratios résidus ILLUSTRATION), points GPS par bassin de production, fenêtres saisonnières, techniques, réglementation par pays (cinq postes), 2 points rattachés aux hubs de la flotte (Meknès, Lavaux). V1.2 (18/10/2026) : atlas des vignobles du monde — 22 pays viticoles, 32 intrants (22 points de sarments de taille, 10 points de marcs de pressurage) sourcés FAOSTAT bulk 2024 (productions et surfaces réelles, ratios ILLUSTRATION), points GPS par grande région viticole, fenêtres saisonnières des deux hémisphères (double régime tropical documenté), techniques, réglementation par pays (cinq postes), 2 points rattachés aux hubs de la flotte (Mendoza — ar-cuyo, Extrémadure — es-extremadura).

## Règles absolues

- Tout résultat est étiqueté SYNTHÉTIQUE. Devant un investisseur, on dit simulation, toujours.
- Aucune valeur calibrée, clé ou secret dans ce dossier. Les paramètres réels vivent hors du dépôt.
- La télémétrie synthétique circule sur le registre de DÉVELOPPEMENT, jamais sur le registre Merkle de production.
- La simulation éprouve la logique, jamais la physique. La qualification reste le monopole des FAT/SAT sur machines réelles.

## Architecture en cinq couches

| Couche | Rôle | Sources (gratuites, vérifiées 17/10/2026) |
| --- | --- | --- |
| 1 — Données monde | gisements, saisonnalité, brûlage, réglementation, météo | FAOSTAT, NASA FIRMS, Open-Meteo (ERA5), GEOGLAM Crop Monitor, fiches pays |
| 2 — Atlas des biomasses | grammaire des recettes par biomasse | Atlas V6 (hors dépôt pour les valeurs calibrées) |
| 3 — Moteur de scénarios | cellule (pays, région, biomasse, mois) → charge, humidité, fenêtre | engine/scenario.py |
| 4 — Simulateur flotte | trios, opérateurs, MTBF/MTTR, pannes injectées, modes dégradés | engine/simulateur.py |
| 5 — Cloud « as if in operation » | télémétrie SYNTHÉTIQUE au contrat Edge, VDE stub, rapports | sorties/ (non versionnées) |

## Contenu du dossier

- README.md — cette spécification.
- pilote-france-2027.md — cahier du pilote France : cinq biomasses, douze mois, paramètres figés v0.
- pilote-monde-2027.md — cahier P2 : les sept hubs de la flotte monde, saisonnalité hémisphère Sud incluse, données réelles branchées.
- sources-donnees.md — sources de données monde, accès, limites, plan de branchement.
- atlas-gisements-monde.md — atlas des gisements mondiaux des 7 hubs : données publiques sourcées et étiquetées (v0.5), méthode, ratios de conversion.
- fiches-pays-reglementation.md — fiches pays réglementaires (v0.6) : cadre légal du brûlage des résidus pour les 7 hubs, sanctions, pain points, sources légales croisées.
- croisement-geoglam.md — croisement GEOGLAM (v0.7) : calendriers culturaux sous-nationaux réels des 7 hubs, verdicts des fenêtres du moteur, fenêtres candidates étiquetées À SOURCER.
- firms-historique.md — FIRMS historique multi-saison (v0.8) : cinq saisons complètes de détections NASA FIRMS réelles par bassin (2021-2025), filtre des sources fixes, verdicts mensuels, croisement des fenêtres du moteur.
- gisements-faostat-bulk.md — gisements FAOSTAT bulk multi-pays (v0.9) : séries nationales de production et de surfaces (six pays, six cultures, 2019-2024), gisements documentaires dérivés, croisement avec les ancres régionales de l'atlas v0.5.
- atlas-biomasses-monde.md — atlas des biomasses monde (v1.0) : les 52 intrants du master placés sur le globe — familles, points GPS (hub existant ou point candidat), gisements étiquetés SOURCÉ/ILLUSTRATION, fenêtres saisonnières, techniques culturales, réglementation par intrant (brûlage, enfouissement, traitement, coûts, main-d'œuvre), synthèse réglementaire par pays, météo temps réelle.
- engine/atlas_biomasses_monde.py — atlas machine des biomasses monde : 52 fiches placées (GPS, volumes, calendriers, réglementation), contrôles de couverture contre monde.py et de cohérence des bassins ERA5, pointage météo temps réel Open-Meteo en un appel pour les 52 points (cache local d'une heure, jamais versionné).
- atlas-biomasses-pays.md — atlas des biomasses locales par pays (v1.1) : 18 pays, 67 intrants locaux majeurs — productions nationales FAOSTAT 2024 étiquetées SOURCÉ (deux volumes À SOURCER : luzerne saoudienne, liège portugais), ratios résidus ILLUSTRATION, points GPS par bassin de production, fenêtres saisonnières, techniques culturales, réglementation par pays (brûlage, enfouissement, traitement, coûts, main-d'œuvre), fiches pays complètes.
- engine/atlas_biomasses_pays.py — atlas machine des biomasses locales par pays : 67 fiches placées (GPS, volumes, calendriers, réglementation), croisement de cohérence contre le master v1.0 (familles, jetons, hubs flotte), fiche d'un intrant ou d'un pays ; aucun paramètre VDE versionné.
- atlas-vignobles-monde.md — atlas des vignobles du monde (v1.2) : 22 pays viticoles, 32 intrants (22 sarments de taille, 10 marcs de pressurage) — productions et surfaces nationales FAOSTAT 2024 étiquetées SOURCÉ, ratios résidus ILLUSTRATION (2 t/ha de sarments, 15 % de la vendange en marc), points GPS par grande région viticole, fenêtres saisonnières des deux hémisphères, techniques culturales, réglementation par pays (brûlage, enfouissement, traitement, coûts, main-d'œuvre), fiches pays complètes, coupe de périmètre documentée (pays non retenus, candidats v1.3).
- engine/atlas_vignobles_monde.py — atlas machine des vignobles du monde : 32 fiches placées (GPS, volumes, calendriers, réglementation), croisement de cohérence contre le master v1.0 et l'atlas v1.1 (familles, jetons, hubs flotte, cohérence hémisphérique des fenêtres), fiche d'un intrant ou d'un pays ; aucun paramètre VDE versionné.
- engine/monde.py — grammaire mondiale des hubs (P2) : pays, régions, biomasses, fenêtres, graines ; maintenance déduite des fenêtres.
- engine/scenario.py — couche 3 : scénarios déterministes non calibrés ; lecture optionnelle du cache météo ERA5 réel ; fiche/bassin optionnels pour les hubs monde.
- engine/simulateur.py — couche 4 : simulateur de flotte monde et générateur de rapports (KPI par hub, priorisation mondiale FIRMS) ; fr-rhone réplique exactement v0.3.
- engine/monte_carlo.py — runs multi-graines et sensibilité (figeage), mode monde à l'échelle du millier de runs, agrégats par hub, mémoire constante.
- engine/firms.py — couche 1 : client NASA FIRMS (stdlib uniquement). Avec une MAP_KEY locale, les pain points deviennent des feux RÉELS ; sans clé, repli synthétique ILLUSTRATION.
- engine/firms.env.example — modèle commenté du fichier de configuration local de la clé FIRMS (firms.env, jamais versionné).
- engine/atlas_gisements.py — atlas machine des gisements mondiaux : constantes étiquetées par hub (v0.5), contrôle de couverture contre monde.py.
- engine/lecture_resultats.py — lecture des résultats Monte Carlo (v0.5) : classement des hubs par disponibilité, sensibilité au figeage, synthèse du dernier run ; écrit sorties/lecture-resultats.md et .json.
- engine/fiches_reglementation.py — fiches pays réglementaires machine (v0.6) : statut du brûlage et références légales par hub, contrôle de couverture contre monde.py.
- engine/geoglam.py — croisement GEOGLAM machine (v0.7) : calendriers culturaux par hub étiquetés, conditions de campagne, fenêtres candidates, contrôles de couverture et de cohérence contre monde.py.
- engine/firms_histo.py — couche FIRMS historique machine (v0.8) : téléchargement et cache des résumés annuels par pays (sans MAP_KEY), agrégats mensuels pluriannuels par bassin, filtre de quasi-permanence, croisement des fenêtres monde.py (monde.py inchangé).
- engine/faostat_bulk.py — extraction FAOSTAT bulk machine (v0.9) : téléchargement du bulk normalisé (sans clé, licence CC BY 4.0), séries nationales par hub, gisements documentaires dérivés, croisement avec l'atlas v0.5 (monde.py inchangé).
- cache-meteo/agregats-mensuels.json — agrégations mensuelles RÉELLES Open-Meteo ERA5 des dix bassins (4 pilote + 6 monde, données publiques, versionnées).
- sorties/ — rapports et télémétrie générés (ignorés par git, jamais versionnés).

## Lancement

```
python3 engine/simulateur.py                 # flotte monde : 7 hubs (P2)
python3 engine/simulateur.py fr-rhone        # un hub seul (réplique v0.3)
```

Configuration optionnelle de la couche brûlage réelle : copier `engine/firms.env.example` en `firms.env` à la racine du dossier world-twin, y coller la MAP_KEY FIRMS (gratuite, inscription sur la NASA, environ cinq minutes). Le fichier `firms.env` est exclu du dépôt (motif `*.env`) ; la clé vit uniquement en local. Sans clé, le simulateur fonctionne en repli synthétique sans erreur.

Aucune dépendance : bibliothèque standard uniquement, graine déterministe. Monte Carlo : `python3 engine/monte_carlo.py [graines_baseline] [graines_par_variante] [france|monde|hub]` — le mode `monde` tourne à l'échelle du millier de runs (agrégats par hub, mémoire constante, progression affichée). Atlas gisements : `python3 engine/atlas_gisements.py [hub]` (sommaire ou fiche d'un hub). Croisement GEOGLAM : `python3 engine/geoglam.py [hub|croisement]` (sommaire, fiche d'un hub ou croisement machine complet). FIRMS historique : `python3 engine/firms_histo.py [bassin|hub|croisement] [--annees DEBUT FIN] [--capteur viirs-snpp|viirs-jpss1|modis]` (sommaire, fiche, ou croisement des fenêtres ; premier run : téléchargement d'environ 100 Mo, mis en cache dans cache-firms-histo/). FAOSTAT bulk : `python3 engine/faostat_bulk.py [hub|croisement] [--annees DEBUT FIN]` (sommaire, fiche d'un hub ou croisement avec l'atlas v0.5 ; premier run : téléchargement d'environ 34 Mo, mis en cache dans cache-faostat-bulk/). Atlas des biomasses monde : `python3 engine/atlas_biomasses_monde.py [TOKEN|croisement|meteo [TOKEN]]` (sommaire des 52 intrants, fiche d'un intrant, croisement de couverture, pointage météo temps réel ; réseau requis pour `meteo` uniquement). Atlas des biomasses locales par pays : `python3 engine/atlas_biomasses_pays.py [TOKEN|pays NOM|croisement]` (sommaire des 67 intrants, fiche d'un intrant, fiche d'un pays, croisement de cohérence contre le master v1.0). Atlas des vignobles du monde : `python3 engine/atlas_vignobles_monde.py [TOKEN|pays NOM|croisement]` (sommaire des 32 intrants, fiche d'un intrant, fiche d'un pays, croisement de cohérence contre le master v1.0 et l'atlas v1.1). Lecture des résultats : `python3 engine/lecture_resultats.py` — à lancer après un Monte Carlo (erreur propre sinon). Un run complet écrit dans sorties/ :

- rapport-run.md et rapport-run.json — synthèse du run : lots, fautes, actions, logs, disponibilité ;
- telemetrie-echantillon.json — télémétrie SYNTHÉTIQUE au contrat du digital twin ;
- rapport-quotidien-exemple.md — base du rapport quotidien World Ops.

## Phases

- P0 : spécification, cahier pilote France, paramètres figés. Terminé le 17/10/2026 (figeage : 2 opérateurs tournants par hub, MTBF 720 h, MTTR 8 h).
- P1 (nov-déc 2026) : 900 runs Monte Carlo réalisés (403 200 lots) ; météo ERA5 réelle branchée ; couche brûlage NASA FIRMS réelle branchée (17/10/2026) ; FAOSTAT extrait ; rapport quotidien planifié.
- P2 (démarrée le 17/10/2026) : multi-pays — Carré d'Or (Suisse, Italie, Espagne), LatAm (Argentine : Cuyo, Misiones), Al-Atlas (Maroc) ; 7 hubs, 2 hémisphères ; ERA5 réelle sur 10 bassins ; FIRMS sur 10 boîtes ; Monte Carlo monde à l'échelle du millier de runs ; KPI pays/région dans le rapport. V0.5 (17/10/2026) : atlas des gisements mondiaux multi-pays livré (données publiques sourcées, FAOSTAT/COI/MAPA/INYM/OFAG), lecture des résultats Monte Carlo. V0.6 (17/10/2026) : fiches pays réglementaires livrées (cadre légal du brûlage, 7 hubs). V0.7 (17/10/2026) : croisement GEOGLAM livré (calendriers culturaux sous-nationaux, fenêtres moteur validées, fenêtres candidates À SOURCER). V0.8 (18/10/2026) : FIRMS historique multi-saison livré (cinq saisons réelles 2021-2025, dix bassins, filtre des sources fixes, croisement des fenêtres). V0.9 (18/10/2026) : extraction bulk FAOSTAT multi-pays livrée (six pays, six cultures, séries 2019-2024, gisements documentaires dérivés, croisement avec l'atlas v0.5). V1.0 (18/10/2026) : atlas des biomasses monde livré (52 intrants placés, couverture monde.py contrôlée, réglementation étiquetée, météo temps réelle branchée). V1.1 (18/10/2026) : atlas des biomasses locales par pays livré (18 pays, 67 intrants FAOSTAT 2024, deux points rattachés aux hubs existants Meknès et Lavaux, croisement de cohérence contre le master v1.0). V1.2 (18/10/2026) : atlas des vignobles du monde livré (22 pays viticoles, 32 intrants FAOSTAT 2024, deux points rattachés aux hubs existants Mendoza et Extrémadure, croisement de cohérence contre le master v1.0 et l'atlas v1.1).
- P3 (post-Nomad v1) : shadow mode réel, replay des campagnes réelles, calibrage edge-first.

## V1.4 — chaîne FRP → FRE → biomasse → émissions (22/10/2026)

La couche brûlage FIRMS passe du comptage à l'énergie : chaque relevé quotidien
(engine/firms_nrt.py) alimente engine/fre_conversions.py, qui convertit le FRP
total des détections (MW) en énergie radiative extrapolée sur la journée (FRE,
MJ), en biomasse sèche consommée (coefficient 0,368 kg/MJ, Wooster et al.
2005, fourchette 0,368-0,453) et en émissions estimées (facteurs IPCC 2006
Vol. 4 Tab. 2.5, résidus agricoles ; GWP AR6). La priorisation des hubs
(engine/firms.py) trie désormais par FRP total décroissant avant le nombre de
détections : l'énergie l'emporte sur le comptage — dix petits feux de
ratissement ne pèsent plus un chantier de chaumes.

Lancement :

    python3 engine/fre_conversions.py chaine 18,1        # chaîne d'un FRP relevé (MW)
    python3 engine/fre_conversions.py chaine 18,1 7       # sur 7 jours
    python3 engine/fre_conversions.py exemple             # cas d'école Camargue 17/10

Le relevé quotidien (sorties-firms-nrt/, jamais versionné) ajoute les colonnes
fre_mj, biomasse_t, co2_t, ch4_t, n2o_t, co2e_nonco2_t et une section « chaîne »
dans resume.md, base de la section feux du rapport World Ops.

DOCTRINE : toutes les valeurs dérivées sont des ESTIMATIONS DOCUMENTAIRES
ILLUSTRATION — jamais calibrées, jamais une donnée de qualification, jamais
sur le registre Merkle de production. Limites honnêtes : extrapolation à
combustion constante entre passages (~2/jour), incertitude d'un facteur ~2 sur
la biomasse (NOAA), feux < 375 m sous-détectés, nuages et panaches masquants.
