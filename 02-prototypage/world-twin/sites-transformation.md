# Sites de transformation post-récolte — couche V2.6 des hubs World Twin (14/11/2026)

Vagues V2.5 puis V2.6 : quatre attributs posés sur les 219 hubs (217
généralisés + fr-rhone + ma-atlas). La couche ne touche ni aux coordonnées
ni aux figeages : aucun effet cascade, contrairement à la vague V2.4.
Répond à la question d'approvisionnement centrale : où sont les gisements
AU SITE de transformation, pour ne pas aller chercher les biomasses aux
champs ? Tout résultat est étiqueté SYNTHÉTIQUE ; devant un investisseur,
on dit « simulation », toujours. Aucune valeur calibrée, aucune clé, aucun
coût (doctrine PI, voir 00-gouvernance/GARDE_FOUS_PI.md).

## Les quatre attributs par hub

1. TYPE_SITE — le type de site de transformation dominant du cluster
   (moulin de palmier à huile, rizerie, sucrerie, moulin d'olive, chai,
   bénéficio, décortiqueur, huller, distillerie, station de conditionnement,
   parcelle agricole pour les gisements diffus).
2. CAPTABILITE — la fraction du gisement théorique disponible AU SITE de
   transformation (et non dispersée aux champs). Étiquetée par famille
   depuis la V2.6 : SOURCÉ quand la littérature chiffre la fraction au
   site (FranceAgriMer marcs 93-99 pour cent, MDPI alperujo 80-85 pour cent
   du fruit, CNP balle 20 pour cent du paddy, BioCycle/USAID cabosse
   environ 75 pour cent au champ, parcs MPOB, PalmWatch, UNICA),
   ILLUSTRATION ailleurs. Un hub n'est SOURCÉ que si toutes ses familles
   le sont (verifier : 32 hubs SOURCÉ, 187 ILLUSTRATION).
3. ENERGIE_SITE — AUTONOME quand le site vend de l'énergie (moulin de
   palmier, rizerie de parboiling, sucrerie : chaudières biomasse +
   turbines, autofourniture documentée) contre IMPORTATEUR quand le site
   achète (chai, moulin d'olive, bénéficio, scierie). Lecture stratégique :
   un module Nomad se positionne différemment selon le sens du flux.
4. LOGISTIQUE — LPI 2023 (Logistics Performance Index, Banque mondiale,
   139 pays enquêtés, score 1 à 5) SOURCÉ pour 187 hubs ; RAI 2023
   (Rural Access Index, indicateur 9.1.1 des ODD — Objectifs de
   Développement Durable : part de la population rurale vivant à moins de
   2 km d'une route praticable toute saison) SOURCÉ pour les 219 hubs
   depuis la V2.6 (jeu SDSN SDG Transformation Center « Rural Access Index
   by Country (2022-2023) », 189 pays, d'après la méthodologie Banque
   mondiale ; les 140 pays de la flotte sont tous couverts).

## Méthode

- 24 familles de sites (FAMILLES_SITES) : chaque famille porte un type de
  site, une captabilité, un profil énergétique, une fenêtre de fraîcheur
  et depuis la V2.6 un statut SOURCÉ ou ILLUSTRATION. L'ordre des familles
  EST une priorité : le premier motif qui matche gagne. La famille
  dominante du hub est celle de captabilité la plus élevée
  (égalité : ordre de la table).
- Le matcher couvre 515 jetons d'intrants (509 généralisés + 6 pilotes) ;
  les seuls non couverts sont les intrants de recherche (tours, pilotes) et
  les intrants déjà rattachés à d'autres couches.
- Captabilité du hub = moyenne des captabilités des familles présentes ;
  statut du hub = SOURCÉ seulement si toutes les familles présentes sont
  SOURCÉ, sinon ILLUSTRATION (honnêteté : une seule famille non chiffrée
  suffit à retirer le statut).
- ENERGIE_SITE = AUTONOME dès qu'une famille AUTONOME est présente dans le
  cluster (moulin de palmier, rizerie, sucrerie).
- FENETRE_FRAICHEUR — la contrainte temporelle du site : « < 24 h »
  (rafles de palmier), « < 48 h » (canne), « heures » (chais, bénéficios),
  « jours », « continu » ou « stockable ».
- LPI_2023 : table complète des 139 pays enquêtés (ISO alpha-3 vers score),
  SOURCÉ Banque mondiale, republication intégrale NationsInquiry ; les
  pays non enquêtés 2023 (MAR, CIV, ECU, KEN, PAK, TUR, etc.) sont étiquetés
  À SOURCER — jamais de valeur inventée.
- RAI_2023 : table des 189 pays du jeu SDSN (ISO alpha-3 vers pourcentage
  de la population rurale à moins de 2 km d'une route toute saison,
  millésime 2023) extraite le 14/11/2026 par l'API ArcGIS du hub SDSN SDG
  Transformation Center (200 entités, 199 valeurs valides, territoires
  contestés exclus, licence Creative Commons BY-NC-SA 4.0, usage interne
  avec attribution). Aucune valeur inventée : un pays absent serait
  étiqueté À SOURCER. PAYS_VERS_ISO : 140 pays de la flotte vers ISO
  alpha-3.

## Familles (24) : captabilités, statuts et profils énergétiques

Familles SOURCÉ (la littérature chiffre la fraction disponible au site) :

- CACAO (0,20, centre coopératif d'écabossage — environ 75 pour cent de
  la cabosse rejeté à la plantation, BioCycle/USAID : au plus 25 pour
  cent atteignable au point de regroupement, valeur retenue sous la
  borne).
- VIGNE_MARC (0,95, chai — 93-99 pour cent des marcs français partent en
  distillerie, FranceAgriMer).
- OLIVE (0,85, moulin d'olive — alperujo 80-85 pour cent du fruit entrant
  au moulin à deux phases, MDPI).
- RIZ (0,90, rizerie — balle de riz 20 pour cent du paddy, 13-15 MJ/kg,
  CNP).
- CANNE (0,90, sucrerie — bagasse autofournit vapeur et électricité,
  389 unités UNICA Brésil 2025/26).
- PALMIER (0,90, moulin de palme — la totalité des régimes entre au moulin
  en moins de 24 h, 449 moulins MPOB Malaisie dont 128 Sabah, 1 471
  PalmWatch Indonésie).

Familles ILLUSTRATION (jugement d'ingénieur, fraction non chiffrée par la
littérature, à figer par sourcing dédié) :

- Gisements diffus, la collecte est à organiser : AU_CHAMP (0,10, parcelle
  agricole), SARMENTS (0,10, rang de vigne, 2 t/ha/an figés en V2.4),
  SARGASSES (0,30, échouage côtier).
- Sites de premier conditionnement : CAFE_PULPE (0,40, station de lavage),
  MAIS (0,40, silo séchoir), MANIOC (0,50, raperie sécherie), NOYAUX_FRUITS
  (0,50, station de conditionnement).
- Transformateurs intermédiaires : COCO (0,60, décortiqueur), DATTIER
  (0,60, station de conditionnement), THE (0,60, station de séchage),
  AGRUMES (0,70, usine de jus), CAFE (0,70, bénéficio sec), PECHE_COQUILLES
  (0,70, station de transformation), AGAVE (0,80, distillerie).
- Transformateurs concentrés, IMPORTATEURS : NOIX_COQUES (0,80,
  huller décortiqueur), POMME (0,85, pressoir cidrerie),
  FORET_SCIERIE (0,90, scierie), BIERE (0,95, brasserie, drêches).

## Sources (toutes publiques, vérifiées le 14/11/2026)

- Banque mondiale, LPI 2023 (139 pays enquêtés, score 1 à 5 ;
  republication intégrale NationsInquiry datasets/logistics-performance).
- SDSN (Sustainable Development Solutions Network) SDG Transformation
  Center, « Rural Access Index by Country (2022-2023) » : RAI par pays,
  indicateur 9.1.1 des ODD, d'après la méthodologie Banque mondiale,
  licence Creative Commons BY-NC-SA 4.0 (usage interne, attribution).
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
- RAI 2023 : 219 hubs SOURCÉ, 0 À SOURCER (les 140 pays de la flotte sont
  tous présents dans le jeu SDSN, millésime 2023).
- Captabilités : 32 hubs SOURCÉ (toutes les familles du hub chiffrées,
  clusters CACAO, VIGNE_MARC, OLIVE, RIZ, CANNE, PALMIER purs ou
  combinés), 187 hubs ILLUSTRATION.
- Flotte : le module ne touche ni figeages ni coordonnées (le trio
  supplémentaire de gen-malaisie-1 vient de la vague V2.6 FAOSTAT, voir
  les verifiers dédiés).
- Sondages exacts : gen-cote-d'ivoire-2 = MOULIN_PALME, cap 0,55 SOURCÉ,
  AUTONOME (CACAO + PALMIER, LPI À SOURCER — Côte d'Ivoire non enquêtée
  2023, RAI 90 pour cent) ; fr-rhone = CHAI, cap 0,47 ILLUSTRATION,
  LPI 3,9, RAI 98 pour cent (France) ; ma-atlas = MOULIN_OLIVE, cap 0,85
  SOURCÉ, IMPORTATEUR, LPI À SOURCER, RAI 99 pour cent (Maroc) ;
  gen-malaisie-1 = MOULIN_PALME, cap 0,90 SOURCÉ, AUTONOME, LPI 3,6,
  RAI 98 pour cent.

## Intégration aux cartes interactives

- engine/build_carte.py : la couche « sites » rejoint les couches CaO et P3
  (219 couches sites, une par hub) ; le verifier du générateur exige
  nb sites = nb P3 et des fiches non vides pour fr-rhone, ma-atlas,
  gen-cote-d-ivoire-2 ; l'anti-fuite du mode public s'étend à la couche.
- data/carte-monde-template.html : table « Site de transformation — V2.6 »
  dans la fiche hub (type de site, familles, captabilité avec statut
  SOURCÉ ou ILLUSTRATION, énergie avec lecture stratégique AUTONOME = le
  site vend / IMPORTATEUR = le site achète, fenêtre de fraîcheur, LPI
  SOURCÉ ou À SOURCER, RAI 2023 SOURCÉ en pour cent) ; légende :
  « sites de transformation post-récolte V2.6 (LPI 2023 Banque mondiale,
  RAI 2023 SDSN, indicateur ODD 9.1.1) ».
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
- Captabilités étiquetées SOURCÉ ou ILLUSTRATION par famille, LPI et RAI
  données publiques SOURCÉES : jamais de valeur inventée.
- Télémétrie du registre DÉVELOPPEMENT, jamais le Merkle de production.
