# Sites de transformation post-récolte — couche V2.7 des hubs World Twin (14/11/2026)

Vagues V2.5, V2.6 puis V2.7 : quatre attributs posés sur les 219 hubs (217
généralisés + fr-rhone + ma-atlas). La couche ne touche ni aux coordonnées
ni aux figeages : aucun effet cascade, contrairement à la vague V2.4.
Répond à la question d'approvisionnement centrale : où sont les gisements
AU SITE de transformation, pour ne pas aller chercher les biomasses aux
champs ? Tout résultat est étiqueté SYNTHÉTIQUE ; devant un investisseur,
on dit « simulation », toujours. Aucune valeur calibrée, aucune clé, aucun
coût (doctrine PI, voir 00-gouvernance/GARDE_FOUS_PI.md).

La vague V2.7 « consolidation du sourçage » ajoute trois choses : le ratio
de marc de raisin devient SOURCÉ dans le moteur de gisements (15 à 30 pour
cent de la vendange, retenu 0,20 — MDPI Foods 14(24):4246 2025 et MDPI
Fermentation 11(2):57 2025), six familles de sites passent SOURCÉ, et les
pays non enquêtés par le LPI 2023 récupèrent leur édition la plus récente
(Banque mondiale, indicateur LP.LPI.OVRL.XQ, API open data).

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
   ILLUSTRATION ailleurs. V2.7 : six familles supplémentaires passent
   SOURCÉ (BIERE, POMME, AGRUMES, AGAVE, FORET_SCIERIE, NOIX_COQUES),
   soit 12 familles SOURCÉ sur 24. Un hub n'est SOURCÉ que si toutes ses
   familles le sont (verifier : 45 hubs SOURCÉ, 174 ILLUSTRATION).
3. ENERGIE_SITE — AUTONOME quand le site vend de l'énergie (moulin de
   palmier, rizerie de parboiling, sucrerie : chaudières biomasse +
   turbines, autofourniture documentée) contre IMPORTATEUR quand le site
   achète (chai, moulin d'olive, bénéficio, scierie). Lecture stratégique :
   un module Nomad se positionne différemment selon le sens du flux.
4. LOGISTIQUE — LPI (Logistics Performance Index, Banque mondiale, score
   1 à 5) SOURCÉ pour 216 hubs : 187 en LPI 2023 (139 pays enquêtés,
   republication intégrale NationsInquiry) et 29 en édition antérieure
   (V2.7 : indicateur LP.LPI.OVRL.XQ de l'API open data Banque mondiale,
   25 hubs en LPI 2018, 3 en LPI 2016 — Éthiopie, Mozambique, Tanzanie —,
   1 en LPI 2014 — Azerbaïdjan). RAI 2023 (Rural Access Index,
   indicateur 9.1.1 des ODD — Objectifs de Développement Durable : part de
   la population rurale vivant à moins de 2 km d'une route praticable
   toute saison) SOURCÉ pour les 219 hubs depuis la V2.6 (jeu SDSN SDG
   Transformation Center « Rural Access Index by Country (2022-2023) »,
   189 pays, d'après la méthodologie Banque mondiale ; les 140 pays de la
   flotte sont tous couverts). Seuls Belize, le Soudan du Sud et le
   Suriname restent À SOURCER en LPI : jamais enquêtés à aucune édition,
   aucune valeur inventée.

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
  SOURCÉ Banque mondiale, republication intégrale NationsInquiry.
- LPI_EDITIONS_ANTERIEURES (V2.7) : table des 23 pays de la flotte non
  enquêtés en 2023 mais enquêtés à une édition précédente (score le plus
  récent, édition portée à la fiche) : Maroc 2,54 et Côte d'Ivoire 3,08 en
  2018, Tanzanie 2,99 en 2016, Azerbaïdjan 2,45 en 2014, etc. Les pays
  jamais enquêtés (Belize, Soudan du Sud, Suriname) restent À SOURCER —
  jamais de valeur inventée.
- RAI_2023 : table des 189 pays du jeu SDSN (ISO alpha-3 vers pourcentage
  de la population rurale à moins de 2 km d'une route toute saison,
  millésime 2023) extraite le 14/11/2026 par l'API ArcGIS du hub SDSN SDG
  Transformation Center (200 entités, 199 valeurs valides, territoires
  contestés exclus, licence Creative Commons BY-NC-SA 4.0, usage interne
  avec attribution). Aucune valeur inventée : un pays absent serait
  étiqueté À SOURCER. PAYS_VERS_ISO : 140 pays de la flotte vers ISO
  alpha-3.

## Familles (24) : captabilités, statuts et profils énergétiques

Familles SOURCÉ, V2.6 (la littérature chiffre la fraction disponible au
site) :

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

Familles SOURCÉ, V2.7 (sourcing du 14/11/2026) :

- BIERE (0,95, brasserie — drêches ≈ 85 pour cent des résidus solides de
  brasserie, générées à la brasserie, MDPI Sustainability 18(5):2464
  2026).
- POMME (0,85, pressoir cidrerie — marc de pomme 25-30 pour cent de la
  masse du fruit frais, généré au pressoir industriel, MDPI Antioxidants
  15(4):429 2026).
- AGRUMES (0,90, usine de jus — résidus de pressage 50-60 pour cent de la
  masse du fruit, générés à l'usine de jus concentré, MDPI Sustainability
  15(21):15225 2023).
- AGAVE (0,90, distillerie — bagasse ≈ 40 pour cent du poids humide de
  l'agave cuit, générée à la distillerie, MDPI Fermentation 12(2):79
  2026).
- FORET_SCIERIE (0,95, scierie — résidus de sciage 46 pour cent du volume
  de la grume (délignures 34 pour cent + sciure 12 pour cent), générés à
  la scierie, FAO appendice VI « Generation of wood residues », rapport
  T0269E).
- NOIX_COQUES (0,80, huller décortiqueur — coques et brou de noix,
  sous-produits des unités de transformation centralisées, Biomass
  Conversion and Biorefinery 2023 ; modèle coopératif de la Central
  Valley californienne).

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
  CAFE (0,70, bénéficio sec), PECHE_COQUILLES (0,70, station de
  transformation).

## Ratio de marc SOURCÉ (V2.7, moteur des gisements)

Les 12 mappings MARC_RAISIN du moteur gisements_hubs.py passent du ratio
ILLUSTRATION (0,15 ; 0,15 ; 0,25) de la doctrine v1.2 au ratio SOURCÉ
(0,15 ; 0,20 ; 0,30) : le marc représente 15 à 30 pour cent de la
vendange (MDPI Foods 14(24):4246 2025 : 10-30 pour cent de la masse de
raisin traitée ; MDPI Fermentation 11(2):57 2025 : 15-30 pour cent du
poids total des raisins traités ; retenu 0,20). Impact vérifié :
gisements des 14 hubs porteurs de marc en hausse de 9 à 33 pour cent en
milieu de fourchette (par exemple Italie 1,17 → 1,57 Mt/an, Espagne
0,87 → 1,16 Mt/an), AUCUN palier de trio ne change (figeage P1 régénéré
puis reprise octet par octet IDENTIQUE : md5 d30c8ba6e939b27cb27f451b21bca57a),
somme mondiale portée à environ 3 103 Mt/an. Les fiches de l'atlas
vignobles v1.2 (atlas-vignobles-monde.md, hors bundle) gardent leurs
valeurs historiques à 0,15 : le moteur V2.7 fait autorité.

## Sources (toutes publiques, vérifiées le 14/11/2026)

- Banque mondiale, LPI 2023 (139 pays enquêtés, score 1 à 5 ;
  republication intégrale NationsInquiry datasets/logistics-performance).
- Banque mondiale, LPI éditions antérieures (V2.7) : indicateur
  LP.LPI.OVRL.XQ, API open data api.worldbank.org, extrait le 14/11/2026 ;
  23 pays de la flotte récupèrent leur score le plus récent (19 pays en
  2018, Éthiopie Mozambique Tanzanie en 2016, Azerbaïdjan en 2014).
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
- V2.7 — MDPI Sustainability 18(5):2464 (2026) : drêches de brasserie
  ≈ 85 pour cent des résidus solides, générées à la brasserie.
- V2.7 — MDPI Antioxidants 15(4):429 (2026) : marc de pomme 25-30 pour
  cent de la masse du fruit frais, au pressoir industriel.
- V2.7 — MDPI Sustainability 15(21):15225 (2023) : résidus d'orangerie
  50-60 pour cent de la masse du fruit, à l'usine de jus.
- V2.7 — MDPI Fermentation 12(2):79 (2026) : bagasse d'agave ≈ 40 pour
  cent du poids humide, à la distillerie.
- V2.7 — FAO, appendice VI « Generation of wood residues » (rapport
  T0269E) : résidus de sciage 46 pour cent du volume de la grume, à la
  scierie.
- V2.7 — Biomass Conversion and Biorefinery (Springer, 2023) : coques et
  brou de noix, sous-produits des unités de transformation.
- V2.7 — MDPI Foods 14(24):4246 (2025) et MDPI Fermentation 11(2):57
  (2025) : marc de raisin 15-30 pour cent de la vendange (deux sources
  croisées, retenu 0,20).
- Détail des 47 sources croisées de la V2.5 : canvas
  world-twin-transformation-post-recolte (deepsearch du 14/11/2026).

## Résultats (verifier : OK, 0 erreur)

- 219 hubs couverts, 515 jetons d'intrants rattachés à une famille, 24
  familles actives. Jetons par famille : AU_CHAMP=121, RIZ=48, MAIS=37,
  CANNE=33, NOIX_COQUES=25, SARMENTS=21, FORET_SCIERIE=17, MANIOC=18,
  PALMIER=18, CAFE=14, NOYAUX_FRUITS=14, VIGNE_MARC=15, CACAO=9, OLIVE=8,
  AGRUMES=7, PECHE_COQUILLES=3, POMME=2, THE=2, COCO=2, DATTIER=3,
  BIERE=1, AGAVE=1, SARGASSES=1, CAFE_PULPE=1.
- LPI : 216 hubs SOURCÉ (187 en LPI 2023 ; 25 en LPI 2018 ; 3 en LPI 2016
  — Éthiopie, Mozambique, Tanzanie ; 1 en LPI 2014 — Azerbaïdjan),
  3 hubs À SOURCER (Belize, Soudan du Sud, Suriname : jamais enquêtés à
  aucune édition).
- RAI 2023 : 219 hubs SOURCÉ, 0 À SOURCER (les 140 pays de la flotte sont
  tous présents dans le jeu SDSN, millésime 2023).
- Captabilités : 45 hubs SOURCÉ (toutes les familles du hub chiffrées,
  soit 12 familles SOURCÉ combinées), 174 hubs ILLUSTRATION.
- Flotte : le module ne touche ni figeages ni coordonnées ; le ratio marc
  V2.7 est absorbé sans palier (figeage reprise octet par octet
  IDENTIQUE), voir les verifiers dédiés.
- Sondages exacts : gen-cote-d-ivoire-2 = MOULIN_PALME, cap 0,55 SOURCÉ,
  AUTONOME (CACAO + PALMIER, LPI 3,08 édition 2018, RAI 90 pour cent) ;
  fr-rhone = CHAI, cap 0,47 ILLUSTRATION, LPI 3,9 édition 2023, RAI 98
  pour cent (France) ; ma-atlas = MOULIN_OLIVE, cap 0,85 SOURCÉ,
  IMPORTATEUR, LPI 2,54 édition 2018, RAI 99 pour cent (Maroc) ;
  gen-malaisie-1 = MOULIN_PALME, cap 0,90 SOURCÉ, AUTONOME, LPI 3,6
  édition 2023, RAI 98 pour cent ; gen-espagne-2 = CHAI, cap 0,88, LPI 3,9,
  RAI 100 pour cent.

## Intégration aux cartes interactives

- engine/build_carte.py : la couche « sites » rejoint les couches CaO et P3
  (219 couches sites, une par hub) ; le verifier du générateur exige
  nb sites = nb P3 et des fiches non vides pour fr-rhone, ma-atlas,
  gen-cote-d-ivoire-2 ; l'anti-fuite du mode public s'étend à la couche.
- data/carte-monde-template.html : table « Site de transformation — V2.7 »
  dans la fiche hub (type de site, familles, captabilité avec statut
  SOURCÉ ou ILLUSTRATION, énergie avec lecture stratégique AUTONOME = le
  site vend / IMPORTATEUR = le site achète, fenêtre de fraîcheur, LPI
  avec édition portée à la fiche, RAI 2023 SOURCÉ en pour cent) ; légende :
  « sites de transformation post-récolte V2.7 (LPI Banque mondiale 2023
  ou édition la plus récente, RAI 2023 SDSN, indicateur ODD 9.1.1) ».
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
