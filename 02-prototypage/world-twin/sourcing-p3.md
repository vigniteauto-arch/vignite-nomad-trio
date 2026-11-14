# Sourcing P3 — sites industriels réels au rayon des hubs World Twin (14/11/2026)

Couche P3 de la flotte V2.3 : pour chaque hub généralisé, les sites
industriels RÉELS capables de livrer des réactifs alcalins (poussière de
fours à ciment, laitier, cendres de bois) sont géomatchés en GPS et la
capacité du rayon est confrontée au besoin du module Carb (582 t CO2/an par
trio). Tout résultat est étiqueté SYNTHÉTIQUE ; devant un investisseur, on
dit « simulation », toujours. Aucune valeur calibrée, aucune clé (doctrine
PI, voir 00-gouvernance/GARDE_FOUS_PI.md).

## Sources (publiques, Global Energy Monitor)

- `data/GEM_GCCT.xlsx` — Global Cement and Concrete Tracker (juillet 2025) :
  2 887 cimenteries retenues (statuts operating / construction /
  operating pre-retirement, capacité ciment > 0, GPS ; le statut
  pre-retirement est REQUIS, sinon la médiane au site le plus proche passe
  de 75,9 à 76,4 km).
- `data/GEM_GIST-plant.xlsx` — Global Iron and Steel Tracker (mars 2026,
  données au niveau usine) : 457 unités de hauts fourneau retenues
  (statuts idem, ttpa > 0, position d'usine ; 409 usines ; écart documenté
  par rapport au repère 458 : données GEM vivantes).
- `data/GEM_GBPT.xlsx` — Global Bioenergy Power Tracker (v3, DOI Zenodo
  10.5281/zenodo.20843067, CC BY 4.0) : 910 lignes bois retenues
  (wood + operating + GPS).
- `data/xlslite.py` — lecteur XLSX minimal (stdlib uniquement, aucune
  dépendance).

## Doctrine (calibrée le 14/11/2026)

- Géomatch Haversine : rayon 50 km, extension à 100 km si le besoin n'est
  pas couvert à 50 km.
- Seuils P3 (DISTINCTS des seuils CaO P2.9) : AUTONOME ≥ 1,0 ;
  COUVERT 0,8-1,0 ; PARTIEL 0,3-0,8 ; A_SOURCER < 0,3 ou sans site.
- Besoin = trios × 582 t CO2/an. Facteur bois 12 500 t/an/MW
  (ILLUSTRATION).
- 165 alias de pays GEM vers ISO 3166-1 alpha-3 (21 alias remarquables
  documentés dans le code).
- Coûts (merit order + déficit marché) : PRIVÉS, jamais versionnés
  (`data/sourcing-p3.json` exclu par .gitignore).

## Résultats (verifier : OK, écarts tracés)

- Statuts : 118 AUTONOME, 2 COUVERT, 6 PARTIEL, 91 A_SOURCER (ruraux sans
  site à 100 km).
- Paires hub-site : 362 (repère du 11/11 : 343, +5,5 % — comptage
  lignes/unités + données GEM vivantes) ; cimenteries retenues : 270
  (repère 257, +5,1 %) ; aciéries : 13 ; unités bois : 79.
- Médiane du site le plus proche : 75,9 km. Capacité CO2 des sites :
  1 373 190 t/an (écart +0,07 %). Médiane des ratios des hubs matchés :
  5,95 (repère 6,0).
- Insight : la contrainte est la concentration locale, pas le gisement
  mondial (P2.9 ratio ~124×).
- Témoin fr-rhone : AUTONOME, ratio 6,57, 2 sites, site le plus proche
  9,1 km. Témoin ma-atlas (raccord V2.3.1, centre 33,89 / −5,55) :
  AUTONOME au rayon de 50 km, ratio 5,47, 2 cimenteries (Meknès 5,5 km,
  Aïn Chkef 40,4 km).

## Lancement

```
python3 engine/sourcing_p3.py generer         # snapshot sites + hubs (+ PRIVÉ local)
python3 engine/sourcing_p3.py sommaire        # synthèse mondiale
python3 engine/sourcing_p3.py verifier        # contrôles croisés et écarts tracés
python3 engine/sourcing_p3.py table           # table des hubs
python3 engine/sourcing_p3.py pays France     # fiche d'un pays
```

## Anti-fuite

`data/sourcing-p3.json` contient les coûts et plans d'achat : jamais
versionné, jamais publié. `data/sourcing-p3-public.json` et
`data/p3-sites-snapshot.json` sont versionnables (zéro coût, greps
anti-fuite : cout / € / prix / plan_achat / eur_t / eur_an / marche_externe
/ deficit). La carte en mode public ne charge que la version publique.
