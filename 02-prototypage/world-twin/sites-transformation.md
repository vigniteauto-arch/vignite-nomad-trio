# Sites de transformation post-récolte — couche V2.5 des hubs World Twin (14/11/2026)

Vague V2.5 : quatre attributs posés sur les 219 hubs (217 généralisés
+ fr-rhone + ma-atlas) SANS toucher aux coordonnées ni aux figeages — aucun
effet cascade, contrairement à la vague V2.4. Répond à la question
d'approvisionnement centrale : où sont les gisements AU SITE de
transformation, pour ne pas aller chercher les biomasses aux champs ?
Tout résultat est étiqueté SYNTHÉTIQUE ; devant un investisseur, on dit
« simulation », toujours. Aucune valeur calibrée, aucune clé, aucun coût
(doctrine PI, voir 00-gouvernance/GARDE_FOUS_PI.md).

## Les quatre attributs par hub

1. TYPE_SITE — le type de site de transformation dominant du cluster
   (moulin de palmier à huile, rizerie, sucrerie, moulin d'olive, chai,
   bénéficio, décortiqueur, huller, distillerie, station de conditionnement,
   parcelle agricole pour les gisements diffus).
2. CAPTABILITE — la fraction du gisement théorique disponible AU SITE de
   transformation (et non dispersée aux champs). ILLUSTRATION, dérivée du
   deepsearch post-récolte du 14/11/2026 (canvas
   world-twin-transformation-post-recolte, ~47 sources croisées), à figer
   par sourcing dédié.
3. ENERGIE_SITE — AUTONOME quand le site vend de l'énergie (moulin de
   palmier, rizerie de parboiling, sucrerie : chaudières biomasse +
   turbines, autofourniture documentée) contre IMPORTATEUR quand le site
   achète (chai, moulin d'olive, bénéficio, scierie). Lecture stratégique :
   un module Nomad se positionne différemment selon le sens du flux.
4. LOGISTIQUE — LPI 2023 (Logistics Performance Index, Banque mondiale,
   139 pays enquêtés, score 1 à 5) par pays du hub, SOURCÉ ; le RAI
   (Rural Access Index, indicateur 9.1.1 des ODD — Objectifs de
   Développement Durable) reste À SOURCER (vague suivante : les valeurs
   par pays demandent une extraction dédiée du jeu NASA SEDAC — Socio
   Economic Data and Applications Center).

## Méthode

- 24 familles de sites (FAMILLES_SITES) : chaque famille porte un type de
  site, une captabilité, un profil énergétique et une fenêtre de fraîcheur.
  L'ordre des familles EST une priorité : le premier motif qui matche gagne.
  La famille dominante du hub est celle de captabilité la plus élevée
  (égalité : ordre de la table).
- Le matcher couvre 515 jetons d'intrants (509 généralisés + 6 pilotes) ;
  les seuls non couverts sont les intrants de recherche (tours, pilotes) et
  les intrants déjà rattachés à d'autres couches.
- Captabilité du hub = moyenne des captabilités des familles présentes.
  Captabilité = ILLUSTRATION jusqu'au sourcing dédié.
- ENERGIE_SITE = AUTONOME dès qu'une famille AUTONOME est présente dans le
  cluster (moulin de palmier, rizerie, sucrerie).
- FENETRE_FRAICHEUR — la contrainte temporelle du site : « < 24 h »
  (rafles de palmier), « < 48 h » (canne), « heures » (chais, bénéficios),
  « jours », « continu » ou « stockable ».
- LPI_2023 : table complète des 139 pays enquêtés (ISO alpha-3 vers score),
  SOURCÉ Banque mondiale, republication intégrale NationsInquiry ; les
  pays non enquêtés 2023 (MAR, CIV, ECU, KEN, PAK, TUR, etc.) sont étiquetés
  À SOURCER — jamais de valeur inventée. PAYS_VERS_ISO : 140 pays de la
  flotte vers ISO alpha-3.

## Familles (24) : captabilités ILLUSTRATION et profils énergétiques

- Gisements diffus, la collecte est à organiser : AU_CHAMP (0,10, parcelle
  agricole), SARMENTS (0,10, rang de vigne, 2 t/ha/an figés en V2.4),
  CACAO (0,20, centre coopératif d'écabossage — environ 75 pour cent de la
  cabosse rejeté à la plantation, BioCycle/USAID), SARGASSES (0,30,
  échouage côtier).
- Sites de premier conditionnement : CAFE_PULPE (0,40, station de lavage),
  MAIS (0,40, silo séchoir), MANIOC (0,50, raperie sécherie), NOYAUX_FRUITS
  (0,50, station de conditionnement).
- Transformateurs intermédiaires : COCO (0,60, décortiqueur), DATTIER
  (0,60, station de conditionnement), THE (0,60, station de séchage),
  AGRUMES (0,70, usine de jus), CAFE (0,70, bénéficio sec), PECHE_COQUILLES
  (0,70, station de transformation), AGAVE (0,80, distillerie).
- Transformateurs concentrés, IMPORTATEURS : NOIX_COQUES (0,80,
  huller décortiqueur), OLIVE (0,85, moulin d'olive — alperujo 80-85 pour
  cent du fruit entrant au moulin à deux phases, MDPI), POMME (0,85,
  pressoir cidrerie), FORET_SCIERIE (0,90, scierie), VIGNE_MARC (0,95,
  chai — 93-99 pour cent des marcs français partent en distillerie,
  FranceAgriMer), BIERE (0,95, brasserie, drêches).
- Sites énergiquement AUTONOMES (le site vend de l'énergie) : RIZ (0,90,
  rizerie — balle de riz 20 pour cent du paddy, 13-15 MJ/kg, CNP), CANNE
  (0,90, sucrerie — bagasse, 389 unités UNICA Brésil 2025/26), PALMIER
  (0,90, moulin de palme — 449 moulins MPOB Malaisie dont 128 Sabah,
  1 471 PalmWatch Indonésie, 79 Colombie, 70 Thaïlande, 40 Équateur).

## Sources (toutes publiques, vérifiées le 14/11/2026)

- Banque mondiale, LPI 2023 (139 pays enquêtés, score 1 à 5 ;
  republication intégrale NationsInquiry datasets/logistics-performance).
- MPOB (Malaysian Palm Oil Board) : 449 moulins Malaisie, 128 Sabah.
- PalmWatch : 1 471 moulins Indonésie, 79 Colombie, 70 Thaïlande,
  40 Équateur.
- UNICA (União da Indústria de Cana-de-Açúcar) : 389 unités Brésil 2025/26.
- CNP (Carbon Negative Power) : balle de riz 20 pour cent du paddy,
  13-15 MJ/kg.
- FranceAgriMer : 93-99 pour cent des marcs français partent en distillerie.
- MDPI : alperujo 80-85 pour cent du fruit entrant au moulin à deux phases.
- BioCycle / USAID : environ 75 pour cent de la cabosse de cacao rejetée
  au champ.
- Détail des 47 sources croisées : canvas world-twin-transformation-
  post-recolte (deepsearch du 14/11/2026).

## Résultats (verifier : OK, 0 erreur)

- 219 hubs couverts, 515 jetons d'intrants rattachés à une famille, 24
  familles actives. Répartition des familles dominantes : AU_CHAMP=121,
  RIZ=48, MAIS=37, CANNE=33, NOIX_COQUES=25, SARMENTS=21, FORET_SCIERIE=17,
  MANIOC=18, CAFE=14, NOYAUX_FRUITS=14, VIGNE_MARC=15, PALMIER=18,
  AGRUMES=7, OLIVE=8, CACAO=9, THE=2, COCO=2, DATTIER=3, PECHE_COQUILLES=3,
  POMME=2, BIERE=1, AGAVE=1, SARGASSES=1, CAFE_PULPE=1.
- LPI 2023 : 187 hubs SOURCÉ, 32 À SOURCER (pays non enquêtés 2023 —
  26 ISO absents de l'enquête Banque mondiale).
- Flotte INVARIANTE : aucun figeage ni coordonnée touchés (contrôle du
  verifier ; les cinq fichiers de données versionnés sont inchangés au
  comparaison octet par octet avec le bundle V2.4).
- Sondages exacts : gen-cote-d-ivoire-2 = MOULIN_PALME, cap 0,55, AUTONOME
  (CACAO + PALMIER, LPI À SOURCER — Côte d'Ivoire non enquêtée 2023) ;
  fr-rhone = CHAI, cap 0,47, LPI 3,9 (France) ; ma-atlas = MOULIN_OLIVE,
  cap 0,85, IMPORTATEUR.

## Intégration aux cartes interactives

- engine/build_carte.py : la couche « sites » rejoint les couches CaO et P3
  (219 couches sites, une par hub) ; le verifier du générateur exige
  nb sites = nb P3 et des fiches non vides pour fr-rhone, ma-atlas,
  gen-cote-d-ivoire-2 ; l'anti-fuite du mode public s'étend à la couche.
- data/carte-monde-template.html : table « Site de transformation — V2.5 »
  dans la fiche hub (type de site, familles, captabilité ILLUSTRATION,
  énergie avec lecture stratégique AUTONOME = le site vend / IMPORTATEUR =
  le site achète, fenêtre de fraîcheur, LPI SOURCÉ ou À SOURCER,
  RAI À SOURCER) ; légende : « sites de transformation post-récolte V2.5
  (LPI 2023, Banque mondiale) ».
- Les deux modes (public et privé) portent la couche ; la carte publique
  ne contient aucun coût (verifier + grep du générateur).

## Lancement

    python3 engine/sites_transformation.py                # sommaire
    python3 engine/sites_transformation.py fiche gen-cote-d-ivoire-2
    python3 engine/sites_transformation.py verifier       # contrôles
    python3 engine/sites_transformation.py table          # table 219 hubs
    python3 engine/sites_transformation.py couches        # sortie couches

## Anti-fuite

- Aucun jeton cout/prix/plan_achat/eur_t/eur_an/marche_externe/deficit/€
  dans les couches sites (contrôlé au verifier).
- Captabilités ILLUSTRATION uniquement, LPI donnée publique SOURCÉE,
  RAI explicitement À SOURCER : jamais de valeur inventée.
- Télémétrie du registre DÉVELOPPEMENT, jamais le Merkle de production.
