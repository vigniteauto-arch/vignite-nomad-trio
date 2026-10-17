# World Twin — la flotte mondiale en simulation

Programme World Twin : faire tourner le trio Nomad v1 « comme si » il opérait déjà partout dans le monde — toutes biomasses par pays et région, couplé à la saisonnalité des récoltes, aux pain points locaux (brûlage, réglementation), à la météo et aux points GPS — afin de nourrir le VDE de milliers de lots simulés et de produire le rapport quotidien World Ops, avant même que le premier acier ne soit commandé.

Statut : P2 — flotte monde (Carré d'Or, LatAm, Al-Atlas : 7 hubs, 2 hémisphères). Squelette non calibré, déterministe. Couches réelles branchées : météo ERA5 (10 bassins) et brûlage NASA FIRMS (10 boîtes), le 17/10/2026.

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
- engine/monde.py — grammaire mondiale des hubs (P2) : pays, régions, biomasses, fenêtres, graines ; maintenance déduite des fenêtres.
- engine/scenario.py — couche 3 : scénarios déterministes non calibrés ; lecture optionnelle du cache météo ERA5 réel ; fiche/bassin optionnels pour les hubs monde.
- engine/simulateur.py — couche 4 : simulateur de flotte monde et générateur de rapports (KPI par hub, priorisation mondiale FIRMS) ; fr-rhone réplique exactement v0.3.
- engine/monte_carlo.py — runs multi-graines et sensibilité (figeage), mode monde à l'échelle du millier de runs, agrégats par hub, mémoire constante.
- engine/firms.py — couche 1 : client NASA FIRMS (stdlib uniquement). Avec une MAP_KEY locale, les pain points deviennent des feux RÉELS ; sans clé, repli synthétique ILLUSTRATION.
- engine/firms.env.example — modèle commenté du fichier de configuration local de la clé FIRMS (firms.env, jamais versionné).
- cache-meteo/agregats-mensuels.json — agrégations mensuelles RÉELLES Open-Meteo ERA5 des dix bassins (4 pilote + 6 monde, données publiques, versionnées).
- sorties/ — rapports et télémétrie générés (ignorés par git, jamais versionnés).

## Lancement

```
python3 engine/simulateur.py                 # flotte monde : 7 hubs (P2)
python3 engine/simulateur.py fr-rhone        # un hub seul (réplique v0.3)
```

Configuration optionnelle de la couche brûlage réelle : copier `engine/firms.env.example` en `firms.env` à la racine du dossier world-twin, y coller la MAP_KEY FIRMS (gratuite, inscription sur la NASA, environ cinq minutes). Le fichier `firms.env` est exclu du dépôt (motif `*.env`) ; la clé vit uniquement en local. Sans clé, le simulateur fonctionne en repli synthétique sans erreur.

Aucune dépendance : bibliothèque standard uniquement, graine déterministe. Monte Carlo : `python3 engine/monte_carlo.py [graines_baseline] [graines_par_variante] [france|monde|hub]` — le mode `monde` tourne à l'échelle du millier de runs (agrégats par hub, mémoire constante, progression affichée). Un run complet écrit dans sorties/ :

- rapport-run.md et rapport-run.json — synthèse du run : lots, fautes, actions, logs, disponibilité ;
- telemetrie-echantillon.json — télémétrie SYNTHÉTIQUE au contrat du digital twin ;
- rapport-quotidien-exemple.md — base du rapport quotidien World Ops.

## Phases

- P0 : spécification, cahier pilote France, paramètres figés. Terminé le 17/10/2026 (figeage : 2 opérateurs tournants par hub, MTBF 720 h, MTTR 8 h).
- P1 (nov-déc 2026) : 900 runs Monte Carlo réalisés (403 200 lots) ; météo ERA5 réelle branchée ; couche brûlage NASA FIRMS réelle branchée (17/10/2026) ; FAOSTAT extrait ; rapport quotidien planifié.
- P2 (démarrée le 17/10/2026) : multi-pays — Carré d'Or (Suisse, Italie, Espagne), LatAm (Argentine : Cuyo, Misiones), Al-Atlas (Maroc) ; 7 hubs, 2 hémisphères ; ERA5 réelle sur 10 bassins ; FIRMS sur 10 boîtes ; Monte Carlo monde à l'échelle du millier de runs ; KPI pays/région dans le rapport. Reste : FAOSTAT multi-pays, fiches pays réglementaires.
- P3 (post-Nomad v1) : shadow mode réel, replay des campagnes réelles, calibrage edge-first.
