# Figeage P1 des paramètres par trio (V2.3.1, 14/11/2026)

Programme World Twin, vague P1 : figer, pour chaque trio de la flotte
simulée, les paramètres opérationnels déterministes qui conditionnent les
runs — avant tout calibrage réel (monopole des FAT/SAT, Factory
Acceptance Test / Site Acceptance Test, sur machines réelles). Moteur :
`engine/parametres_trios.py`, sortie versionnée :
`data/parametres-trios.json`.

Étiquette : SYNTHÉTIQUE — registre de développement, jamais le registre
Merkle de production. Aucun paramètre calibré du VDE (Vignite Decision
Engine) : les coefficients réels vivent hors du dépôt (doctrine PI).

## Périmètre figé

| Population | Hubs | Trios |
| --- | --- | --- |
| Flotte généralisée (engine/flotte_monde.py) | 217 | 480 |
| Hubs pilotes P2 (engine/monde.py, dont ma-atlas 3 trios — raccord V2.3.1) | 7 | 9 |
| Total | 224 | 489 |

## Conventions figées par trio

- Équipe : 2 opérateurs tournants couvrent jusqu'à 5 trios (plafond figé
  du modèle IoT) — aucun hub ne dépasse 5 trios, donc une équipe par hub :
  224 équipes, 448 opérateurs (repère flotte : 217 équipes, 434
  opérateurs pour la part généralisée).
- MTBF (Mean Time Between Failures, temps moyen entre pannes) : 720
  heures — baseline figée V1.6, ILLUSTRATION non calibrée.
- MTTR (Mean Time To Repair, temps moyen de réparation) : 8 heures —
  même baseline ; les variantes M1/M2/M3 du Monte Carlo restent éteintes.
- Graines : graine déterministe du hub, et graine du trio par la
  convention P1 « graine_trio = graine_hub + indice − 1 » : le trio 1
  garde exactement la graine du hub (compatibilité arrière avec
  simulateur.simuler), les trios suivants la décalent d'un pas — deux
  trios d'un même hub ne produisent jamais des télémétries identiques.
- Fenêtre d'opération : union des fenêtres des biomasses du hub ;
  maintenance saisonnière : complément des douze mois. Statut de fenêtre :
  CONTINUE (12 mois actifs) ou SAISONNIÈRE. Résultat : 363 trios
  SAISONNIÈRE, 126 trios CONTINUE.

Témoins (reproduits à chaque verifier) : fr-rhone-trio-1 (graine du hub
P2 inchangée), ma-atlas-trio-3 (graines 6042 → 6044, fenêtre grignons
d'olive décembre-janvier-février, maintenance mars à novembre),
gen-maroc-1-trio-1 (fenêtre 1/2/5/6, graine 19942).

## Branchement des sources — vague P1

- FAOSTAT (base statistique de la FAO, Organisation des Nations unies
  pour l'alimentation et l'agriculture) : DÉJÀ BRANCHÉE. Les hubs
  généralisés héritent des gisements et des fenêtres du snapshot v18
  (engine/gisements-faostat-snapshot-v18.json, 959 séries, via
  flotte_monde.hubs_generalises()). Le figeage fige ce que la flotte
  consomme : rien n'est re-sourcé ici.
- GEOGLAM (Global Agricultural Geo-monitoring Initiative) : croisement
  P2.3 déjà livré pour les céréales AMIS (engine/geoglam.py, calendriers
  culturaux sous-nationaux, conditions de campagne). LIMITE DOCUMENTÉE :
  les calendriers AMIS ne sont pas téléchargeables, les cultures
  pérennes (vigne, olivier, noyer, yerba mate) sont hors périmètre
  GEOGLAM — les fenêtres candidates restent À SOURCER par curation
  manuelle, jamais ingérées dans le moteur avant sourcing complet
  (gisement, ratio, volumes).
- Open-Meteo : pointage multi-points des 219 hubs en UN appel
  (engine/build_carte.py --meteo-hubs), écrit dans le fichier versionné
  data/meteo-hubs-pointage.json (température, humidité, précipitation,
  vent par hub — données météo publiques, aucune donnée économique) ;
  le pointage figé est réinjecté dans chaque build de carte tant qu'il
  n'est pas rafraîchi ; le figeage lui-même n'en dépend pas.
- NASA FIRMS (Fire Information for Resource Management System de la
  National Aeronautics and Space Administration) : chaque hub
  généralisé enregistre sa zone GPS au moment de sa construction
  (firms.enregistrer_zone_gps, boîte ±1,0° latitude / ±1,5° longitude,
  convention firms_nrt.py). Le verifier contrôle que les 217 zones
  enregistrées correspondent exactement aux 217 hubs généralisés.

## Garde-fous du verifier

- Recomptages : 489 trios (480 + 9), 217 hubs généralisés, 7 pilotes,
  224 équipes, 448 opérateurs.
- Conventions : MTBF/MTTR/opérateurs sur chaque trio, formule des
  graines, fenêtre ∪ maintenance = 12 mois sans chevauchement, statut de
  fenêtre cohérent.
- Anti-fuite : data/parametres-trios.json ne contient aucun jeton
  économique ni secret (cout, prix, plan d'achat, marché externe, MAP_KEY…).
- Reproductibilité : le fichier versionné correspond octet par octet au
  figeage recalculé (build hors ligne déterministe).

## Lancement

```
python3 engine/parametres_trios.py sommaire        # totaux et témoins
python3 engine/parametres_trios.py generer        # écrit data/parametres-trios.json
python3 engine/parametres_trios.py verifier        # contrôles complets
python3 engine/parametres_trios.py table           # table des 489 trios
python3 engine/parametres_trios.py trio ma-atlas-trio-2   # fiche d'un trio
```
