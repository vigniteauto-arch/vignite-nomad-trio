# Flotte généralisée World Twin — V1.6 (27/10/2026)

## Statut

V1.6 actée le 27/10/2026 (« go » de Manu Moineau) : figeage des paramètres
de maintenance et généralisation de la flotte simulée à l'ensemble des
points des atlas versionnés. Suite directe de la vague V1.5 (intégration
EMIT — Engineered Mineral Inventory Table, inventaire minéral spectral
de la NASA/JPL). Phase de référence inchangée : P0+1, pilote France v0,
graine déterministe 42. Étiquette **SYNTHÉTIQUE** — registre de
développement, jamais le registre Merkle de production.

## Figeage acté (27/10/2026)

| Paramètre | Valeur figée | Rôle |
| --- | --- | --- |
| MTBF (Mean Time Between Failures, temps moyen entre pannes) | 720 h | référence série historique |
| MTTR (Mean Time To Repair, temps moyen de réparation) | 8 h | référence série historique |
| Opérateurs | 2 tournants par équipe | doctrine IoT assistée |
| Plafond de couverture | 5 trios par équipe | 6e trio = seconde équipe |
| Rayon de mutualisation d'un hub | 300 km | ILLUSTRATION |

- La baseline 720 h / 8 h est conservée comme référence : toutes les
  séries P0+1 restent comparables d'une vague à l'autre.
- Les leviers M1, M2 et M3 ne sont pas imposés au run de référence :
  ce sont des variantes Monte Carlo, activables par knobs dans
  engine/simulateur.py (v0.5) et prédéfinies dans engine/monte_carlo.py.

### Variantes figées (Monte Carlo)

- M1 — MTTR en mélange : 80 % de pannes mineures à 4 h, 20 % de pannes
  majeures à 24 h, plus un délai de réponse de +2 h. Espérance :
  8 h de réparation + 2 h de délai. Simule un mix pièces/compétences
  réaliste plutôt qu'un MTTR uniforme.
- M2 — Commissioning : MTBF réduit à 240 h sur les 500 premières heures
  d'un trio neuf (jeunesse des pannes), puis retour à 720 h. À activer
  pour tout hub entrant en flotte.
- M3 — Staffing : MTTR × 1,5 quand le ratio opérateurs/trio franchit
  le plafond de couverture. Modélise la dérive de réparation quand une
  équipe est surchargée.

### Règle opérateurs (figée)

Deux opérateurs tournants couvrent jusqu'à cinq trios en doctrine IoT
assistée : présence 4 h/jour, alarmes, télémétrie Edge, intervention
détaillée sur appel. Le sixième trio d'un hub impose une seconde équipe.
La concurrence de pannes ne dimensionne rien : la probabilité que deux
trios d'une même équipe soient en panne simultanément reste inférieure
à 0,2 % à cinq trios. Le plafond tient au temps de déplacement, pas à
la probabilité de collision.

## Flotte généralisée

La couche engine/flotte_monde.py (V1.6) collecte les 151 points d'intrants
des trois atlas versionnés — v1.0 master (52), v1.1 pays (67), v1.2
vignobles (32) — exclut les 13 points déjà rattachés aux hubs de la flotte
P2 (hubs_flotte non vide), puis clusterise les 138 points restants en hubs
généralisés : un hub mutualise les points d'un même pays dans un rayon de
300 km (clustering glouton déterministe, tri par latitude/longitude).

Chaque hub reçoit : un identifiant gen-pays-N, une graine propre
(7142 + 100 × compteur), une flotte de trios et ses équipes. La capacité
d'un trio n'étant pas calibrée, le nombre de trios par hub suit une règle
ILLUSTRATION par densité de points : 1 trio pour 1 à 3 points, 2 pour 4 à
6, 3 pour 7 à 9, 4 pour 10 à 12, plafond 5. Les opérateurs suivent la
règle figée : 2 par équipe, une équipe pour 1 à 5 trios.

Composition obtenue (graines 1 à 10, Monte Carlo flotte) :
81 hubs généralisés sur 32 pays, 88 trios, 162 opérateurs, ratio 1,84
opérateur par trio. Disponibilité moyenne de la flotte : 99,7 % —
cohérente avec la baseline 98,9 % par trio permanent : les hubs à
fenêtre courte (saison unique) diluent les heures planifiées.

## Limites honnêtes

- Le dimensionnement des trios par hub est une règle ILLUSTRATION par
  densité de points : il n'est pas calibré par les gisements addressables.
  P3 (shadow mode réel, post-Nomad v1) le remplacera par les gisements.
- Les hubs généralisés n'ont pas de boîte FIRMS (Fire Information for
  Resource Management, détection thermique NASA) : les pain points
  retombent sur le repli synthétique du moteur de scénarios, propre et
  étiqueté comme tel. Aucune donnée externe n'est inventée.
- Les humidités par famille sont ILLUSTRATION, jamais mesurées.
- La mutualisation à 300 km est une hypothèse de démonstration, pas
  une logistique validée.

## Commandes

    python3 engine/flotte_monde.py sommaire        # composition + gardes
    python3 engine/flotte_monde.py flotte         # table hubs/trios/ops
    python3 engine/flotte_monde.py run [HUB]      # année SYNTHÉTIQUE
    python3 engine/flotte_monde.py monte-carlo 50 # Monte Carlo flotte

Sorties dans sorties/ (jamais versionnées) :
flotte-generale-composition.json, flotte-generale-run.json/.md,
flotte-generale-mc.json. Tout résultat porté en réunion ou devant
investisseur se dit « simulation » — jamais exploitation réelle.
