# Cahier pilote France — World Twin v0 (2027)

Pilote de simulation « as if in operation » : un trio Nomad v1 simulé en France sur douze mois, cinq biomasses, graine déterministe. Version du 17 octobre 2026.

## 1. Objet et règles du jeu

Le pilote prouve la chaîne complète en simulation : données monde → scénario → flotte → télémétrie → VDE → rapport quotidien. Il ne prouve pas la physique — la qualification reste le monopole des FAT/SAT sur machines réelles.

Règles inviolables :

- Toute donnée produite est étiquetée SYNTHÉTIQUE.
- Aucune valeur calibrée : les hypothèses chiffrées sont des ILLUSTRATIONS à remplacer par les sources FAOSTAT, FIRMS, Open-Meteo et GEOGLAM au branchement P1.
- La télémétrie circule sur le registre de DÉVELOPPEMENT, jamais sur le registre Merkle de production.
- Reproductibilité totale : une graine, un run identique.

## 2. Paramètres figés v0

| Paramètre | Valeur | Statut |
| --- | --- | --- |
| Graine déterministe | 42 | figé |
| Année simulée | 2027 | figé |
| Trios simulés | 1 — FR-HUB-01-TRIO-1 | figé (P2 : multi-trios) |
| Opérateurs par trio | 2, tournants sur le hub régional (3 à 5 trios, 1 h 30 à 2 h de route) | figé le 17/10/2026 |
| MTBF (temps moyen entre pannes) | 720 heures | ILLUSTRATION, figé par décision du 17/10 |
| MTTR (temps moyen de réparation) | 8 heures | ILLUSTRATION, figé — couvre le temps de route inter-trios |
| Durée d'un lot simulé | 6 heures | ILLUSTRATION, non calibré |
| Horaire simulé | 2 lots par jour ouvré | ILLUSTRATION |

## 3. Les cinq biomasses du pilote

Fenêtres de récolte et d'opération en France — ILLUSTRATION v0, calendriers à croiser avec GEOGLAM Crop Monitor et FAOSTAT.

| Biomasse | Bassin v0 | Récolte (ILLUSTRATION) | Fenêtre d'opération simulée |
| --- | --- | --- | --- |
| Sarments de vigne | Vallée du Rhône | taille janvier à mars | janvier à avril |
| Marc de raisin | Vallée du Rhône | vendanges septembre à octobre | septembre à novembre |
| Rafles et cannes de maïs | Sud-Ouest | septembre à octobre | octobre à décembre |
| Paille de riz | Camargue | septembre à octobre | octobre à décembre |
| Coques de noix | Périgord | septembre à octobre | octobre à février |

## 4. Calendrier saisonnier simulé (charge par mois, ILLUSTRATION)

| Mois | Sarments | Marc | Maïs | Riz | Noix | Charge trio |
| --- | --- | --- | --- | --- | --- | --- |
| Janvier | haute | — | — | — | — | moyenne |
| Février | haute | — | — | — | — | moyenne |
| Mars | moyenne | — | — | — | — | moyenne |
| Avril | fin | — | — | — | — | basse |
| Mai | — | — | — | — | — | maintenance |
| Juin | — | — | — | — | — | maintenance |
| Juillet | — | — | — | — | — | maintenance |
| Août | — | — | — | — | — | maintenance |
| Septembre | — | haute | — | — | — | haute |
| Octobre | — | moyenne | haute | haute | haute | pic |
| Novembre | — | fin | moyenne | moyenne | moyenne | haute |
| Décembre | — | — | fin | fin | moyenne | moyenne |

Mois de mai à août : arrêt saisonnier simulé, maintenance préventive et calibrages (en interne, hors dépôt).

## 5. Télémétrie et VDE

- La télémétrie synthétique respecte le contrat JSON du digital twin (02-prototypage/digital-twin/schemas/donnees-capteurs.schema.json) : modules buffer, stock, ops ; capteurs avec grandeur, valeur, unité, qualité.
- Le VDE est exécuté en mode stub non calibré : sélection de recette depuis la grammaire des recettes, interlocks, hiérarchie syngaz, modes dégradés. Les coefficients calibrés vivent hors du dépôt.
- Chaque faute simulée déclenche la chaîne faute → action → log, collectée dans le rapport.

## 6. Sorties attendues du pilote

1. Rapport de run (markdown + JSON) : douze mois, lots, fautes, actions, logs, disponibilité.
2. Échantillon de télémétrie SYNTHÉTIQUE au contrat Edge.
3. Exemple de rapport quotidien World Ops (base du rapport quotidien planifié).

## 7. Hypothèses v0 à sourcer

- Quantités de gisement par biomasse et bassin : ILLUSTRATION, à remplacer par FAOSTAT (production et résidus, méthode IPCC).
- Fenêtres culturales : à croiser avec GEOGLAM Crop Monitor.
- Météo : synthétique en v0 ; branchement Open-Meteo (ERA5 historique) en P1.
- Pain points brûlage et réglementation : à documenter par fiche pays.

## 8. Critères de passage vers P2

- Le simulateur tourne de bout en bout sans erreur, déterministe, sur douze mois.
- Au moins cent simulations de lots accumulées au registre de développement.
- Paramètres opérateurs, MTBF et MTTR figés par décision.
- Rapport quotidien jugé exploitable pendant deux semaines consécutives.
