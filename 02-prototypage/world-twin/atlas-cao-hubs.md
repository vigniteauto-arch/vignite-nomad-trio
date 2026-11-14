# Atlas des gisements de CaO des hubs World Twin — couche P2.9 (14/11/2026)

Socle minéral de la flotte V2.3 : pour chaque hub généralisé, la capacité
nationale en réactifs alcalins carbonatables (poussière de fours à ciment
CKD, laitier de haut fourneau, cendres de bois-énergie) confrontée au besoin
du module Carb (582 t CO2/an par trio). Tout résultat est étiqueté
SYNTHÉTIQUE ; devant un investisseur, on dit « simulation », toujours.
Aucune valeur calibrée du VDE, aucune clé, aucun secret (doctrine PI,
voir 00-gouvernance/GARDE_FOUS_PI.md).

## Chaîne de données (publics, SOURCÉ + ratios ILLUSTRATION)

1. `data/gen_cao.py` régénère les quatre snapshots versionnés (rejouable,
   stdlib uniquement, md5 stables d'un run à l'autre) :
   - `data/cao-pays-referentiel.json` — 140 pays de la flotte, nom français
     vers ISO 3166-1 alpha-3 et bulk FAOSTAT (Organisation des Nations unies
     pour l'alimentation et l'agriculture) ;
   - `data/cao-bois-faostat-snapshot.json` — bois rond 2024 par pays (API
     smart-csv FAO, article 1864), 139 pays (Nicaragua absent du bulk,
     documenté) ;
   - `data/cao-population-snapshot.json` — population 2023 par ISO 3166-1
     alpha-3 (Our World in Data), bases de prorata USGS (14 pays ciment,
     11 pays acier) ;
   - `data/cao-industrie-snapshot.json` — tables USGS (United States
     Geological Survey) Mineral Commodity Summaries 2026, ciment (kt) et
     fonte-acier (Mt), extraites positionnellement (data/pdfpos.py).
   Données brutes (PDF USGS, population OWID, bois FAO) : hors dépôt,
   chemin par défaut `../../data` ou variable `WT_DATA_BRUTES`.
2. `engine/atlas_cao.py` déroule la doctrine P2.9 : prorata USGS par
   population pour chaque pays de la flotte, conversion en potentiel CO2
   par réactif (ratios ILLUSTRATION : CKD, laitier, cendres de bois-énergie),
   besoin = trios × 582 t CO2/an, statuts AUTONOME (ratio ≥ 1,2) /
   COUVERT (0,8-1,2) / PARTIEL (0,3-0,8) / A_SOURCER (< 0,3).
3. Sorties versionnées : `data/cao-hubs-public.json` (statuts, ratios,
   besoins, capacités — AUCUN coût). Sortie PRIVÉE `data/cao-hubs.json`
   (coûts, plans d'achat) : JAMAIS versionnée, exclue par .gitignore.

## Résultats (verifier : OK)

- 217 hubs généralisés (480 trios), plus les hubs pilotes fr-rhone
  (1 trio) et ma-atlas (3 trios, Al-Atlas — raccord V2.3.1), témoins
  hors totaux.
- Capacité mondiale de réactifs : 34,8 Mt CO2/an ; besoin de la flotte :
  279,4 kt CO2/an — la contrainte n'est pas le gisement mondial (~124×)
  mais la concentration locale, traitée par la couche P3.
- Statuts : 217 AUTONOME. Écart documenté par rapport au repère du
  11/11/2026 (215 AUTONOME / 1 COUVERT / 1 PARTIEL) : le bois régénéré du
  snapshot FAOSTAT v18 fait passer gen-belize-1 à un ratio de 1,30 — écart
  tracé dans verifier, pas une anomalie.
- Écart V2.3 → V2.3.1 documenté : le raccord de ma-atlas fait passer le
  prorata national Maroc de 3 à 6 trios — gen-maroc-1 passe d'un ratio
  de 37,3 à 18,65, statut AUTONOME inchangé (tracé dans verifier).
- Témoin fr-rhone : besoin 582 t/an, capacité 11 402 t/an, AUTONOME.
  Témoin ma-atlas : besoin 1 746 t/an (3 trios), capacité 32 560 t/an,
  ratio 18,65, AUTONOME.
- Coûts (ILLUSTRATION, PRIVÉS, jamais dans le dépôt) : voir la sortie
  locale de `engine/atlas_cao.py sommaire`.

## Lancement

```
python3 data/gen_cao.py                        # régénère les 4 snapshots
python3 engine/atlas_cao.py generer            # écrit cao-hubs-public.json (+ PRIVÉ local)
python3 engine/atlas_cao.py verifier           # contrôles croisés et écarts tracés
python3 engine/atlas_cao.py sommaire            # synthèse
python3 engine/atlas_cao.py table              # table des hubs
python3 engine/atlas_cao.py pays France        # fiche d'un pays
```

## Anti-fuite

`data/cao-hubs.json` contient les coûts et plans d'achat : jamais versionné
(motif .gitignore), jamais publié, jamais dans une carte en mode public
(`engine/build_carte.py --mode public` ne l'ouvre même pas et vérifie
l'absence de tout indice de coût dans les couches injectées).
