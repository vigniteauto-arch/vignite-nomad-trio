# Sites de transformation post-récolte — couche V2.8 des hubs World Twin (14/11/2026)

Vagues V2.5 à V2.8 : quatre attributs posés sur les 219 hubs (217
généralisés + fr-rhone + ma-atlas). La couche ne touche ni aux coordonnées
ni aux figeages : aucun effet cascade, contrairement à la vague V2.4.
Répond à la question d'approvisionnement centrale : où sont les gisements
AU SITE de transformation, pour ne pas aller chercher les biomasses aux
champs ? Tout résultat est étiqueté SYNTHÉTIQUE ; devant un investisseur,
on dit « simulation », toujours. Aucune valeur calibrée, aucune clé, aucun
coût (doctrine PI, voir 00-gouvernance/GARDE_FOUS_PI.md).

La vague V2.8 « suite des À SOURCER » attaque les deux dettes laissées par la V2.7 :
cinq familles de sites passent SOURCÉ (AU_CHAMP, SARMENTS, MANIOC,
DATTIER, PECHE_COQUILLES), soit 17 familles SOURCÉ sur 24, et les trois
pays jamais enquêtés par le LPI (Belize, Soudan du Sud, Suriname)
reçoivent un proxy régional explicite, étiqueté RÉGIONAL et distinct de
SOURCÉ : le À SOURCER tombe à zéro sans qu'aucune valeur soit inventée.

## Les quatre attributs par hub

1. TYPE_SITE — le type de site de transformation dominant du cluster
   (moulin de palmier à huile, rizerie, sucrerie, moulin d'olive, chai,
   bénéficio, décortiqueur, huller, distillerie, station de conditionnement,
   parcelle agricole pour les gisements diffus).
2. CAPTABILITE — la fraction du gisement théorique disponible AU SITE de
   transformation (et non dispersée aux champs). Étiquetée par famille
   depuis la V2.6 : SOURCÉ quand la littérature chiffre la fraction au
   site, ILLUSTRATION ailleurs. V2.6 : six familles SOURCÉ (CACAO,
   VIGNE_MARC, OLIVE, RIZ, CANNE, PALMIER), V2.7 : six de plus (BIERE,
   POMME, AGRUMES, AGAVE, FORET_SCIERIE, NOIX_COQUES), V2.8 : cinq de
   plus (AU_CHAMP 0,35, SARMENTS 0,55, MANIOC 0,50, DATTIER 0,60,
   PECHE_COQUILLES 0,70), soit 17 familles SOURCÉ sur 24. Un hub n'est
   SOURCÉ que si toutes ses familles le sont (verifier : 156 hubs SOURCÉ,
   63 ILLUSTRATION, contre 45/174 en V2.7). La captabilité est un attribut
   de la couche sites : aucun gisement, aucun figeage ne bouge.
3. ENERGIE_SITE — AUTONOME quand le site vend de l'énergie (moulin de
   palmier, rizerie de parboiling, sucrerie : chaudières biomasse +
   turbines, autofourniture documentée) contre IMPORTATEUR quand le site
   achète (chai, moulin d'olive, bénéficio, scierie). Lecture stratégique :
   un module Nomad se positionne différemment selon le sens du flux.
4. LOGISTIQUE — LPI (Logistics Performance Index, Banque mondiale, score
   1 à 5) disponible pour les 219 hubs : 216 hubs SOURCÉ (187 en LPI 2023,
   139 pays enquêtés, republication intégrale NationsInquiry ; 25 en LPI
   2018, 3 en LPI 2016 — Éthiopie, Mozambique, Tanzanie ; 1 en LPI 2014 —
   Azerbaïdjan, via l'indicateur LP.LPI.OVRL.XQ de l'API open data Banque
   mondiale depuis la V2.7) et depuis la V2.8 trois hubs RÉGIONAL :
   Belize 2,69 et Suriname 2,69 (moyenne simple des 24 pays enquêtés de
   la région Amérique latine et Caraïbes), Soudan du Sud 2,54 (moyenne
   simple des 26 pays enquêtés de la région Afrique subsaharienne), score
   2023, méthode « simple averages » des agrégats du jeu Data360 WB_LPI.
   Le statut RÉGIONAL est distinct de SOURCÉ : c'est un proxy documenté,
   pas une enquête. RAI 2023 (Rural Access Index, indicateur 9.1.1 des
   ODD — Objectifs de Développement Durable : part de la population
   rurale vivant à moins de 2 km d'une route praticable toute saison)
   SOURCÉ pour les 219 hubs depuis la V2.6 (jeu SDSN SDG Transformation
   Center « Rural Access Index by Country (2022-2023) », 189 pays,
   d'après la méthodologie Banque mondiale ; les 140 pays de la flotte
   sont tous couverts). Plus aucun À SOURCER en LPI : zéro, sans valeur
   inventée.

## Méthode

- 24 familles de sites (FAMILLES_SITES) : chaque famille porte un type de
  site, une captabilité, un profil énergétique, une fenêtre de fraîcheur
  et un statut SOURCÉ ou ILLUSTRATION (depuis la V2.6). L'ordre des
  familles EST une priorité : le premier motif qui matche gagne. La
  famille dominante du hub est celle de captabilité la plus élevée
  (égalité : ordre de la table).
- Le matcher couvre 515 jetons d'intrants (509 généralisés + 6 pilotes) ;
  les seuls non couverts sont les intrants de recherche (tours, pilotes)
  et les intrants déjà rattachés à d'autres couches.
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
  récent, édition portée à la fiche) : Maroc 2,54 et Côte d'Ivoire 3,08
  en 2018, Tanzanie 2,99 en 2016, Azerbaïdjan 2,45 en 2014, etc.
- LPI_MOYENNES_REGIONALES (V2.8) : table des 3 pays jamais enquêtés à
  aucune édition (Belize BLZ, Suriname SUR, Soudan du Sud SSD), vers
  (score proxy, nombre de pays enquêtés de la région, région Banque
  mondiale). Proxy = moyenne simple des scores LPI 2023 des pays
  enquêtés de la même région Banque mondiale, méthode identique aux
  « simple averages » des agrégats du jeu Data360 WB_LPI (fiche dataset
  documentée). Le proxy porte l'étiquette RÉGIONAL, le champ lpi_proxy
  vaut vrai, le détail (région, nombre de pays) suit la fiche : jamais
  confondu avec un score enquêté.
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

Familles SOURCÉ, V2.8 (sourcing du 14/11/2026, suite des À SOURCER) :

- AU_CHAMP (0,35, parcelle agricole, gisement diffus — taux de retrait
  soutenable chiffré par la méta-analyse Resources, Conservation and
  Recycling 2025 : 45 pour cent pour le riz, 19 pour cent pour le blé,
  42 pour cent pour le maïs ; 33-50 pour cent selon les États membres de
  l'UE, Union européenne (France 50 pour cent, Hongrie 33 pour cent) ;
  fraction collectable au regroupement retenue 0,35. C'est la famille
  diffuse dominante de la flotte (121 hubs) : sa captabilité passe de
  0,10 à 0,35 dans la couche sites, sans toucher au moindre gisement.
- SARMENTS (0,55, rang de vigne — 2 t/ha/an figés en V2.4 (BIVB France,
  Velázquez-Martí Italie) ; collecte mécanisée chiffrée : pertes de
  collecte 36,2-46,2 pour cent selon les prototypes, donc 54-64 pour
  cent récupérable (Biomass and Bioenergy, octobre 2018) ; récolte
  éprouvée par Spinelli, Magagnotti, Nati, Biosystems Engineering
  105(3), 2010 ; retenu 0,55, contre 0,10 en ILLUSTRATION.
- MANIOC (0,50, raperie sécherie — pelage manuel ≈ 22 pour cent de la
  racine fraîche (ILRI, International Livestock Research Institute,
  « Turning Waste to Wealth », Springer 2022), garri ≈ 70 pour cent du
  manioc nigérian transformé hors exploitation aux centres villageois ;
  la valeur 0,50 de l'ingénieur devient SOURCÉ.
- DATTIER (0,60, station de conditionnement — rejets de triage et noyaux
  = 10-15 pour cent de la production à la station (revue MDPI Applied
  Sciences 13(22):12315, 2023 ; conditionnement tunisien centralisé,
  capacité 59 kt) ; la valeur 0,60 devient SOURCÉ.
- PECHE_COQUILLES (0,70, station de transformation — coquilles = 56
  pour cent des déchets de conserverie et ≈ 27 pour cent de la tonne
  vivante rejetée en co-produits aux plants industriels (revue Waste
  Management & Research 2022, d'après Iribarren et al. 2010, Galice) ;
  la valeur 0,70 devient SOURCÉ.

Familles ILLUSTRATION (7 restantes, tentatives V2.8 documentées et
infructueuses, à figer par sourcing dédié) :

- SARGASSES (0,30, échouage côtier — 156 063 t collectées au Quintana
  Roo par la Marine mexicaine, saison 2026, record documenté, mais
  aucune part chiffrée du gisement échoué : gisement aléatoire, valeur
  d'ingénieur).
- CAFE_PULPE (0,40, station de lavage — pulpe 44,6 pour cent de la
  masse de cerise au moulin humide (Rotta, UC Davis 2020), 29 pour cent
  du café éthiopien lavé en station (CABI 2020) ; part du café mexicain
  passant au bénéficio humide À SOURCER, tentative V2.8 infructueuse ;
  hub porteur : gen-mexique-1).
- MAIS (0,40, silo séchoir — collecte intégrée à la moisson chiffrée
  (pertes ≈ 31 pour cent, MDPI Energies 13(5):1265 2020) mais part
  centralisée au silo non chiffrée, tentative V2.8 infructueuse).
- NOYAUX_FRUITS (0,50, station de conditionnement — composition chiffrée
  par les revues de valorisation, mais part des fruits passant en
  station À SOURCER, tentative V2.8 infructueuse).
- COCO (0,60, décortiqueur — l'enquête Philippines 1 200 fermes,
  13 provinces (IJERD, International Journal of Environment and Rural
  Development, 2018) documente la dispersion à la ferme, part
  centralisée À SOURCER, tentative V2.8 infructueuse).
- THE (0,60, station de séchage — résidus de manufacture concentrés en
  station (revues Springer 2025, JECE 2025) mais fraction de la
  production non chiffrée, tentative V2.8 infructueuse).
- CAFE (0,70, bénéficio sec — coques au moulin central de décorticage,
  souvent brûlées dans les séchoirs ; aucune part centralisée chiffrée,
  tentative V2.8 infructueuse).

## Ratio de marc SOURCÉ (V2.7, moteur des gisements)

Les 12 mappings MARC_RAISIN du moteur gisements_hubs.py passent du ratio
ILLUSTRATION (0,15 ; 0,15 ; 0,25) de la doctrine v1.2 au ratio SOURCÉ
(0,15 ; 0,20 ; 0,30) : le marc représente 15 à 30 pour cent de la
vendange (MDPI Foods 14(24):4246 2025 : 10-30 pour cent de la masse de
raisin traitée ; MDPI Fermentation 11(2):57 2025 : 15-30 pour cent du
poids total des raisins traités ; retenu 0,20). Impact vérifié :
gisements des 14 hubs porteurs de marc en hausse de 9 à 33 pour cent en
milieu de fourchette, AUCUN palier de trio ne change (figeage P1 régénéré
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
- Banque mondiale, agrégats régionaux du jeu Data360 WB_LPI (V2.8) :
  moyennes simples des scores LPI 2023 des pays enquêtés, méthode
  « simple averages » documentée par la fiche dataset ; calculs
  vérifiés sur le jeu officiel LPI_2023 (139 pays) : Amérique latine
  et Caraïbes 2,69 (24 pays), Afrique subsaharienne 2,54 (26 pays,
  Soudan inclus). Proxys appliqués aux 3 hubs jamais enquêtés.
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
- V2.8 — Resources, Conservation and Recycling (Elsevier, 2025) :
  méta-analyse des taux de retrait soutenable des résidus de culture
  (45 pour cent riz, 19 pour cent blé, 42 pour cent maïs).
- V2.8 — Biomass and Bioenergy (Elsevier, octobre 2018) : pertes de
  collecte mécanisée des sarments 36,2-46,2 pour cent selon prototypes ;
  et Biosystems Engineering 105(3) (2010), Spinelli, Magagnotti, Nati.
- V2.8 — ILRI (International Livestock Research Institute), « Turning
  Waste to Wealth » (Springer, 2022) : pelage du manioc ≈ 22 pour cent
  de la racine fraîche.
- V2.8 — MDPI Applied Sciences 13(22):12315 (2023) : rejets de triage et
  noyaux de dattes 10-15 pour cent de la production, à la station.
- V2.8 — Waste Management & Research (2022), d'après Iribarren et al.
  2010 (Galice) : coquilles 56 pour cent des déchets de conserverie,
  ≈ 27 pour cent de la tonne vivante aux plants industriels.
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
  3 hubs RÉGIONAL (Belize 2,69 et Suriname 2,69, Amérique latine et
  Caraïbes ; Soudan du Sud 2,54, Afrique subsaharienne), 0 À SOURCER.
- RAI 2023 : 219 hubs SOURCÉ, 0 À SOURCER (les 140 pays de la flotte sont
  tous présents dans le jeu SDSN, millésime 2023).
- Captabilités : 156 hubs SOURCÉ (toutes les familles du hub chiffrées,
  soit 17 familles SOURCÉ combinées), 63 ILLUSTRATION.
- Flotte : le module ne touche ni figeages ni coordonnées ; la captabilité
  est un attribut de couche. Figeage reprise octet par octet IDENTIQUE
  (md5 d30c8ba6e939b27cb27f451b21bca57a), somme mondiale inchangée
  3 103 Mt/an, voir les verifiers dédiés.
- Sondages exacts : gen-cote-d-ivoire-2 = MOULIN_PALME, cap 0,55 SOURCÉ,
  AUTONOME (CACAO + PALMIER, LPI 3,08 édition 2018, RAI 90 pour cent) ;
  fr-rhone = CHAI, cap 0,47 ILLUSTRATION, LPI 3,9 édition 2023, RAI 98
  pour cent (France) ; ma-atlas = MOULIN_OLIVE, cap 0,85 SOURCÉ,
  IMPORTATEUR, LPI 2,54 édition 2018, RAI 99 pour cent (Maroc) ;
  gen-belize-1 = RIZERIE, cap 0,90 SOURCÉ (RIZ + CANNE), LPI 2,69
  RÉGIONAL (proxy Amérique latine et Caraïbes, 24 pays), jamais enquêté ;
  gen-soudan-du-sud-1 = parcelle agricole, cap 0,35 SOURCÉ (AU_CHAMP),
  LPI 2,54 RÉGIONAL (proxy Afrique subsaharienne, 26 pays) ;
  gen-espagne-2 = CHAI, cap 0,88, LPI 3,9, RAI 100 pour cent.

## Intégration aux cartes interactives

- engine/build_carte.py : la couche « sites » rejoint les couches CaO et P3
  (219 couches sites, une par hub) ; le verifier du générateur exige
  nb sites = nb P3 et des fiches non vides pour fr-rhone, ma-atlas,
  gen-cote-d-ivoire-2 ; l'anti-fuite du mode public s'étend à la couche.
- data/carte-monde-template.html : table « Site de transformation — V2.8 »
  dans la fiche hub (type de site, familles, captabilité avec statut
  SOURCÉ ou ILLUSTRATION, énergie avec lecture stratégique AUTONOME = le
  site vend / IMPORTATEUR = le site achète, fenêtre de fraîcheur, LPI
  avec édition portée à la fiche et étiquette RÉGIONAL dédiée pour les
  proxys — le détail « moyenne simple des N pays enquêtés de la région,
  jamais enquêté » suit le score, RAI 2023 SOURCÉ en pour cent) ; légende :
  « sites de transformation post-récolte V2.8 (LPI Banque mondiale 2023
  ou édition la plus récente, moyenne régionale en proxy pour les pays
  jamais enquêtés, RAI 2023 SDSN, indicateur ODD 9.1.1) ».
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
  dans les couches sites, y compris le champ lpi_detail des proxys
  (contrôlé au verifier).
- Captabilités étiquetées SOURCÉ ou ILLUSTRATION par famille, LPI et RAI
  données publiques SOURCÉES, proxys régionaux étiquetés RÉGIONAL :
  jamais de valeur inventée.
- Télémétrie du registre DÉVELOPPEMENT, jamais le Merkle de production.
