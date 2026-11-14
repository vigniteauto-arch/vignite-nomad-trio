# Sources de données monde — World Twin

Sources vérifiées gratuites le 17 octobre 2026. Branchement : Open-Meteo (ERA5, dix bassins monde) et NASA FIRMS (dix boîtes monde) sont branchées (17/10/2026, vague P2) ; FAOSTAT est branchée pour la France ; l'atlas des gisements multi-pays est livré en v0.5 (17/10/2026, atlas-gisements-monde.md et engine/atlas_gisements.py) avec des sources publiques additionnelles par hub ; les fiches pays réglementaires sont livrées en v0.6 (17/10/2026, fiches-pays-reglementation.md et engine/fiches_reglementation.py) ; le croisement GEOGLAM est livré en v0.7 (17/10/2026, croisement-geoglam.md et engine/geoglam.py) ; le FIRMS historique multi-saison est livré en v0.8 (18/10/2026, firms-historique.md et engine/firms_histo.py) ; l'extraction bulk FAOSTAT multi-pays est livrée en v0.9 (18/10/2026, gisements-faostat-bulk.md et engine/faostat_bulk.py) ; l'atlas des biomasses monde est livré en v1.0 (18/10/2026, atlas-biomasses-monde.md et engine/atlas_biomasses_monde.py) avec les 52 intrants du master placés sur le globe et une branche météo temps réelle Open-Meteo (52 points, cache horaire non versionné) ; l'atlas des biomasses locales par pays est livré en v1.1 (18/10/2026, atlas-biomasses-pays.md et engine/atlas_biomasses_pays.py) avec les 67 intrants locaux des 18 pays, productions ancrées sur le bulk FAOSTAT 2024 ; l'atlas des vignobles du monde est livré en v1.2 (18/10/2026, atlas-vignobles-monde.md et engine/atlas_vignobles_monde.py) avec les 32 intrants viticoles des 22 pays, productions et surfaces ancrées sur le bulk FAOSTAT 2024 (item Grapes) ; toute valeur non sourcée est ILLUSTRATION clairement étiquetée. Les gisements FAOSTAT des hubs généralisés sont livrés en v1.7 (31/10/2026, gisements-hubs-generalises.md et engine/gisements_hubs.py) avec 123 points sourcés sur 138 et le dimensionnement de la flotte par gisement réel. La matrice des abonnements satellites et l'extension mondiale de la veille sont livrées en V2.0 (06/11/2026, abonnements-satellites.md, 32 hubs, registre PROPOSÉ, rien activé côté services externes) puis màj en V2.1 (14/11/2026). La vague V2.3 (14/11/2026) branche le snapshot FAOSTAT v18 (959 séries), l'atlas CaO P2.9 (USGS MCS 2026, OWID) et le sourcing P3 (Global Energy Monitor) — sections dédiées ci-dessous.

## Sources

### FAOSTAT (Organisation des Nations unies pour l'alimentation et l'agriculture)

- Contenu : production agricole et résidus par pays, brûlage des résidus (méthode IPCC), ~245 pays, historique pluriannuel.
- Accès : libre, portail FAOSTAT et téléchargements en masse (bulk) ; la nouvelle API faostatservices.fao.org exige une clé — passer par le bulk, gratuit (constaté le 17/10/2026). Licence CC BY 4.0 (politique FAO d'open data licensing) ; le bulk normalisé « Production_Crops_Livestock_E » (environ 34 Mo, mise à jour du 31/12/2025) porte la série 1961-2024 (constaté le 18/10/2026).
- Statut : branchée pour la France depuis la v0.1 (17/10/2026) ; V0.9 (18/10/2026) : extraction bulk MULTI-PAYS branchée — six pays, six cultures, séries 2019-2024 mises en cache (cache-faostat-bulk/, jamais versionné), gisements nationaux documentaires dérivés, croisement avec les ancres régionales de l'atlas v0.5 (gisements-faostat-bulk.md et engine/faostat_bulk.py). V1.7 (31/10/2026) : gisements des hubs généralisés branchés — fenêtre 2020-2024, 33 pays, 599 séries Production et Area harvested (snapshot compact versionné engine/gisements-faostat-snapshot-v17.json, provenance md5), gisements par point et par hub, dimensionnement de la flotte (gisements-hubs-generalises.md et engine/gisements_hubs.py). V1.3 (31/10/2026) : atlas des biomasses d'Asie branché — 23 pays, 72 intrants, extrait du même bulk (pièges de nommage : items « Rice », « Maize (corn) », « Cassava, fresh », « Tea leaves », « Seed cotton, unginned », « Jute, raw or retted », pays « Türkiye », « Republic of Korea », « Lao People's Democratic Republic », « Iran (Islamic Republic of) », « Iraqi » non — « Iraq », « Syrian Arab Republic », « Russian Federation »), productions FAOSTAT 2024 étiquetées SOURCÉ (atlas-biomasses-asie.md et engine/atlas_biomasses_asie.py).
- Rôle : couche 1 — gisements par pays et biomasse, réglementation du brûlage.
- Limite : agrégation au niveau pays ; la maille régionale demande des extrapolations documentées ; le bulk écrase ses fichiers au fil des mises à jour (version datée dans le module) ; pièges de nommage documentés (pays en anglais, « Walnuts, in shell » avec virgule, « Maté leaves »).

### NASA FIRMS (Fire Information for Resource Management System)

- Contenu : feux actifs, points GPS horodatés, quasi temps réel et historique.
- Accès : API exigeant une MAP_KEY gratuite sur inscription (mise à jour du 17/10/2026 ; l'inscription prend environ cinq minutes ; l'API « area » couvre 1 à 5 jours par requête, date de départ paramétrable). Historique : résumés annuels par pays (« Country Yearly Summary »), CSV publics téléchargeables SANS clé — viirs-snpp depuis 2012, viirs-jpss1 depuis 2018, modis depuis 2000 (constaté le 18/10/2026).
- Statut : branchée et testée le 17/10/2026 — détections réelles intégrées au moteur de scénarios (pain points) et à la priorisation des hubs ; vague P2 : dix boîtes géographiques monde (une par bassin, Carré d'Or à Al-Atlas) ; MAP_KEY dans firms.env local, jamais versionné (motif *.env). V0.8 (18/10/2026) : couche historique multi-saison branchée — cinq saisons complètes 2021-2025, VIIRS S-NPP 375 m, filtre de quasi-permanence (sources fixes exclues), verdicts mensuels RÉCURRENT/OCCASIONNEL/RARE/ABSENT, croisement des fenêtres monde.py (firms-historique.md et engine/firms_histo.py).
- Rôle : couche 1 — pain point brûlage, ciblage des zones à épargner, priorisation des hubs, saisonnalité pluriannuelle des fenêtres.
- Limite : détection des feux, pas de leur cause ; croiser avec les calendriers culturaux (v0.7) et les statistiques nationales ; le pixel 375 m sous-détecte les feux petits et brefs (sarments) ; cache local d'un jour (API) et cache-firms-histo/ (résumés annuels, environ 100 Mo) pour préserver le quota de transactions.

### Open-Meteo

- Contenu : météo historique (réanalyse ERA5, 1940 à aujourd'hui) et prévisions, anywhere on Earth.
- Accès : API gratuite sans clé, fair use ~10 000 requêtes/jour.
- Statut : branchée le 17/10/2026 — agrégations mensuelles réelles versionnées dans cache-meteo/ ; vague P2 : dix bassins (France ×4, Suisse Léman, Italie Puglia, Espagne Estrémadure, Argentine Cuyo, Argentine Misiones, Maroc Al-Atlas) ; convention jours de pluie ≥ 0,2 mm, fenêtre 2025-10-01 → 2026-10-10 UTC. V1.0 (18/10/2026) : branche temps réel courante (current weather) branchée pour les 52 points de l'atlas des biomasses monde — un seul appel pour tous les points (listes lat/lon), variables température/humidité/précipitations/vent, cache local d'une heure dans cache-meteo-temps-reel/ (jamais versionné), pointage documentaire jamais une donnée de qualification.
- Rôle : couche 1 — fenêtres d'opération météo, humidité simulée, arrêts saisonniers.
- Limite : fair use ; prévoir une cache locale dès le multi-pays.

### GEOGLAM Crop Monitor

- Contenu : calendriers culturaux sous-nationaux (blé, maïs, riz, soja + cultures de sécurité alimentaire) et conditions de campagne mensuelles ; jeu de données Zenodo DOI 10.5281/zenodo.10949971 (V1.4 du 24/02/2026, licence CC-BY 4.0), couches de régions NASA Harvest/UMD (ArcGIS), bulletins Crop Monitor for AMIS et CM4EW.
- Accès : libre ; les calendriers AMIS proprement dits ne sont pas téléchargeables (« à venir » au 17/10/2026) — dates des pays AMIS sourcées par les bases publiques équivalentes (USDA, FAO GIEWS) et des sources locales croisées ; le portail IPAD de l'USDA a été fermé au public (constat 17/10/2026).
- Statut : branché en v0.7 (17/10/2026) — croisement-geoglam.md et engine/geoglam.py : calendriers machine des 7 hubs (Maroc décodé depuis les calendriers CM4EW), verdicts des fenêtres monde.py, fenêtres candidates À SOURCER ; conditions de campagne des bulletins AMIS n° 143 et CM4EW n° 120 (01/10/2026, conditions au 28/09/2026).
- Rôle : couche 1 — saisonnalité fine par région, validation des fenêtres du moteur.
- Limite : couverture inégale selon les pays (Suisse absente) ; pérennes (vigne, olivier, yerba mate) hors périmètre ; conditions de campagne à re-vérifier avant tout usage externe.

### Fiches pays (curation manuelle)

- Contenu : réglementation locale du brûlage, pain points, contraintes logistiques.
- Base : études LatAm et Al-Atlas déjà en amorce.
- Rôle : couche 1 — dimension réglementaire et commerciale.

### Sources publiques additionnelles — atlas gisements v0.5 (17/10/2026)

- Conseil Oléicole International (COI) : statistiques oléicoles mondiales par campagne (huile d'olive, olives de table).
- MAPA (Espagne) et Junta de Andalucía : prévisions et aforos de production oléicole espagnole (observable de croisement du rendement en huile, ~19 % en 2024/25).
- ISMEA/Agea et MASAF (Italie) : production italienne d'huile d'olive et d'olives de table.
- INYM (Argentine) : statistiques officielles de la yerba mate (surfaces, feuille verte, tissu productif).
- OFAG (Suisse) : surfaces viticoles suisses et vaudoises.
- Presse agricole vérifiée reprenant des données ministérielles (Agrimaroc, LesEco, Extremadura21, Misiones Plural, Clarín Rural) : chiffres régionaux et provinciaux.
- Littérature scientifique sur les résidus agricoles : ratios de génération grignons/sarments (ILLUSTRATION).
- Rôle : couche 1 — gisements contextuels par hub, atlas-gisements-monde.md et engine/atlas_gisements.py.
- Limite : l'oléiculture et la yerba mate alternent fortement ; chaque chiffre porte sa campagne ; maille régionale parfois extrapolée, toujours documentée.

## Plan de branchement P2+

1. FAOSTAT multi-pays : production et résidus des biomasses des hubs (Suisse, Italie, Espagne, Argentine, Maroc), même méthode que l'extraction France. FAIT en v0.5 (17/10/2026) sous forme d'atlas de données publiques sourcées par hub (atlas-gisements-monde.md) ; FAIT en v0.9 (18/10/2026) : extraction bulk FAOSTAT proprement dite — gisements-faostat-bulk.md et engine/faostat_bulk.py, six pays, six cultures, séries 2019-2024, gisements nationaux dérivés étiquetés, croisement avec l'atlas v0.5 (les quatre valeurs France v0.1 reproduites à l'identique, écarts régionaux documentés).
2. Croisement GEOGLAM : validation des fenêtres culturales des hubs, hémisphère Sud inclus. FAIT en v0.7 (17/10/2026) : croisement-geoglam.md et engine/geoglam.py — calendriers sous-nationaux des 7 hubs sourcés et étiquetés, fenêtres mais-rdm et paille-riz validées, fenêtres candidates pailles céréalières À SOURCER (gisement, ratio, volumes avant toute ingestion dans monde.py).
3. Fiches pays réglementaires : brûlage encadré, à sourcer document par document. FAIT en v0.6 (17/10/2026) : fiches-pays-reglementation.md et engine/fiches_reglementation.py — France L.541-21-1, Suisse OPair art. 26a, Italie D.Lgs 152/2006 + LR Puglia 38/2016, Espagne Ley 7/2022 art. 27.3, Argentine Ley 26.562, Maroc Loi 28-00 (la référence « loi 62.25 » du plan initial n'a pas été retrouvée et est écartée). Les textes légis sont publics : Légifrance/AIDA, Infoleg, SGG Maroc, DOE Estrémadure, bulletins officiels régionaux. RÉÉDITÉES en v2.0 (31/10/2026, vague V1.9) : chaque élément revérifié par croisement d'au moins deux sources dont la primaire — voir la section Fiches réglementation v2.0.
4. FIRMS historique : cartographie multi-saison des dix bassins, au-delà du jour courant. FAIT en v0.8 (18/10/2026) : firms-historique.md et engine/firms_histo.py — cinq saisons complètes 2021-2025 par résumés annuels par pays (sans MAP_KEY), VIIRS S-NPP 375 m par défaut (viirs-jpss1 et modis paramétrables), filtre de quasi-permanence des sources fixes, verdicts mensuels, croisement des fenêtres monde.py (monde.py inchangé, doctrine À SOURCER respectée).
5. Remplacement progressif des ILLUSTRATIONS du cahier pilote monde par les valeurs sourcées, avec traçabilité source et date.
6. Abonnements satellites et veille mondiale : matrice livrée en V2.0 (06/11/2026, abonnements-satellites.md). PROPOSÉ à décision de Manu : activation des alertes gratuites (FIRMS email, CAMS aérosols, GNW/MyGFW AOI, GDACS, vigilances nationales) sur les 32 hubs, abonnements CDSE OData PULL, puis prototype local de la couche hubs virtuels.

## Limites honnêtes

- Aucune source ne remplace la qualification machine : FAT/SAT sur acier réel uniquement.
- Les données agrégées au niveau pays masquent les réalités régionales : chaque extrapolation est documentée.
- Les volumes téléchargés vivent hors du dépôt (espace de travail chiffré) ; seules les spécifications et les agrégations non sensibles sont versionnées.

## Chaîne FRP → FRE → biomasse → émissions (V1.4, 22/10/2026)

Sources de la couche de conversion ajoutée en v1.4 :

- Wooster M. J., Roberts G., Perry G. L. W., Kaufman Y. J. (2005), « Retrieval
  of biomass combustion rates and totals from fire radiative power
  observations », J. Geophys. Res. 110, D24311, doi:10.1029/2005JD006318 —
  relation FRP/FRE/biomasse consommée, coefficient ≈ 0,368 kg de matière sèche
  par MJ.
- NOAA NESDIS (rapport technique FBCC) — coefficient de combustion FRE-biomasse
  mesuré de 0,368 à 0,453 kg/MJ selon les études (incertitude d'un facteur ~2).
- IPCC 2006 Guidelines Vol. 4 Ch. 2 Tab. 2.5 — facteurs d'émission des résidus
  agricoles (g par kg de matière sèche brûlée) : CO2 1 515, CH4 2,7, N2O 0,07,
  CO 92, NOx 2,5 ; GWP AR6 (CH4 27,0, N2O 273).
- Hall J., Argueta F., Giglio L. (2022), « Crop Residue Burning Emission
  Coefficients », Zenodo doi:10.5281/zenodo.7013656 (CC BY 4.0) — coefficients
  par culture (blé, riz, maïs, canne à sucre) pour l'affinage futur.

Statut : BRANCHÉE le 22/10/2026 (engine/fre_conversions.py nouveau ;
engine/firms_nrt.py et engine/firms.py mis à jour). Étiquette : ESTIMATION
DOCUMENTAIRE ILLUSTRATION. Usage : priorisation des hubs, argumentaire,
rapport World Ops — jamais le calibrage, jamais le registre Merkle de
production.

## Minéralogie des sols — NASA EMIT (V1.5, 27/10/2026)

- Contenu : identification minérale des surfaces affleurantes — argiles 1:1 (kaolinite) et 2:1 (smectite, illite, chlorite, vermiculite), carbonates (calcite, dolomite), sulfates (gypsum), oxydes de fer (hématite, goethite).
- Produits : EMIT L2B MIN « Estimated Mineral Identification and Band Depth and Uncertainty », maille 60 m (trois granules scènes versionnés) ; EMIT L3 ASA « Aggregated Mineral Spectral Abundance and Uncertainty », agrégation mondiale au demi-degré. EMIT — Earth Surface Mineral Dust Source Investigation, spectromètre imageur de la station spatiale internationale.
- Accès : données publiques NASA LP DAAC (Land Processes Distributed Active Archive Center) / Earthdata ; fichiers uploadés le 24/10/2026, déplacés de la racine du dépôt vers data/emit/ par la vague v1.5.
- Statut : BRANCHÉE le 27/10/2026 — engine/atlas_sols_emit.py (inventaire md5, réassemblage des .part dans cache-sols/ jamais versionné, extraction optionnelle via lecteur HDF5 local, rattachement aux dix bassins de la flotte) et atlas-sols-emit.md. Étiquette : SOURCÉ (fractions EMIT) / ILLUSTRATION (lectures agronomiques).
- Rôle : couche 1 — observable minéralogie par bassin, lecture documentaire des fiches intrants (rétention, CEC — Capacité d'Échange Cationique, dosage biochar indicatif).
- Limite : EMIT voit la surface affleurante, pas les sols couverts ni profonds ; trois scènes L2B ne couvrent pas le monde (le L3 ASA couvre au demi-degré) ; boîtes de bassin = approximation de région ; extraction .nc hors bibliothèque standard (h5py/netCDF4/xarray en local).

## Flotte généralisée (V1.6, 27/10/2026)

- Contenu : flotte mondiale simulée « as if in operation » dérivée des trois atlas versionnés (v1.0 master 52 intrants, v1.1 pays 67 intrants, v1.2 vignobles 32 intrants) : 151 points, dont 138 généralisés après exclusion des 13 points rattachés aux hubs de la flotte P2.
- Dérivation : clustering déterministe par pays, rayon de mutualisation 300 km (ILLUSTRATION) — 81 hubs généralisés sur 32 pays, 88 trios, 162 opérateurs. Règle opérateurs figée : 2 opérateurs tournants pour 5 trios maximum par hub, sixième trio = seconde équipe.
- Modules : engine/flotte_monde.py (sommaire | flotte | run [HUB] | monte-carlo [GRAINES]), flotte-monde.md ; simulateur v0.5 (knobs M1/M2/M3 éteints par défaut, baseline 720 h / 8 h strictement inchangée) et monte_carlo v0.5 (variantes M1-melange-80-4h-20-24h, M2-commissioning-240h-500h, M3-staffing-1-5x).
- Étiquette : SYNTHÉTIQUE — registre de développement, jamais le registre Merkle de production. Aucune donnée calibrée. Hubs généralisés sans boîte FIRMS (Fire Information for Resource Management) : repli synthétique du moteur de scénarios, étiqueté comme tel.
- Limites : dimensionnement des trios par densité de points ILLUSTRATION (capacité trio non calibrée), humidités par famille ILLUSTRATION, mutualisation à 300 km hypothèse de démonstration ; P3 (shadow mode réel, post-Nomad v1) remplacera par les gisements addressables.

## Gisements FAOSTAT des hubs généralisés (V1.7, 31/10/2026)

- Contenu : gisements en tonnes par an des 123 points d'atlas sourcés (sur 138 généralisés), par couple pays/item FAOSTAT, fourchettes [min, milieu, max] — gisement d'un hub = somme des milieux, dimensionnement des trios par paliers (moins de 0,5 Mt = 1 trio, 0,5-2 Mt = 2, 2-10 Mt = 3, 10-50 Mt = 4, 50 Mt et plus = 5, plafond figé de 5 trios par équipe) : 208 trios, 162 opérateurs.
- Base : bulk normalisé « Production_Crops_Livestock_E » (33 921 825 octets, md5 1a202c5674dce152f1134fa87b220b82, licence CC BY 4.0, attribution FAOSTAT), fenêtre 2020-2024, éléments Production et Area harvested, 33 pays — remplace la règle de densité de points de la V1.6 pour le dimensionnement des trios.
- Snapshot : engine/gisements-faostat-snapshot-v17.json (compact, versionné, 599 séries, provenance complète) pour le déterminisme — le bulk brut (environ 545 Mo extraits) vit dans cache-faostat-bulk/ hors du dépôt, procédure de régénération documentée dans gisements-hubs-generalises.md.
- Ratios : conventions ILLUSTRATION par famille issues des fiches d'atlas, recoupées fiche/FAOSTAT 2024 (92 reproductions contrôlées) — pailles de céréales × 0,8-1,2, balles de riz × 0,20, bagasse × 0,28, marc de raisin × 0,15, sarments 2 t/ha × surface, coques de noix × 0,30-0,70 selon espèce, table complète dans gisements-hubs-generalises.md.
- À SOURCER : 15 intrants sans équivalent FAOSTAT (forestier, minéral, marin, brassicole, sargasse, bambou, agave, liège, luzerne fourragère) — exclus du calcul numérique, aucune valeur inventée, trois hubs concernés en repli densité V1.6 étiqueté.
- Statut : BRANCHÉE le 31/10/2026 — engine/gisements_hubs.py (verifier, table), engine/flotte_monde.py v1.7 (sommaire, flotte, run, monte-carlo). Étiquette : SOURCÉ (séries FAOSTAT) / ILLUSTRATION (ratios de résidus).
- Rôle : couche 1 — gisements par point et par hub, dimensionnement de la flotte généralisée, base du rapport World Ops.
- Limite : gisements nationaux (proxy « brut national » documenté dans chaque fiche), décomposition régionale addressable À SOURCER (P3), ratios non calibrés, bases de masse hétérogènes assumées (sèche pour grains et pailles, humide pour bagasse, écorces, cerises de café, cabosses fraîches).

## Boîtes FIRMS des hubs généralisés (V1.8, 31/10/2026)

- Contenu : zone FIRMS par hub généralisé — boîte ±1.0° latitude / ±1.5° longitude autour du centre du cluster (81 hubs), même convention que les dix boîtes P2, enregistrée au runtime dans le registre de engine/firms.py par engine/flotte_monde.py v1.8.
- Capteur : VIIRS_NOAA20_NRT (Visible Infrared Imaging Radiometer Suite, satellite NOAA-20 — National Oceanic and Atmospheric Administration, Near Real Time), mission de référence après la cessation Suomi NPP du 01/11/2026.
- Activation : MAP_KEY gratuite (obtenue le 17/10/2026) lue depuis firms.env (jamais versionné, motif *.env) ou la variable FIRMS_MAP_KEY — en local pour les runs, dans le secret GitHub Actions pour le relevé quotidien CI. Sans clé : repli synthétique propre, workflow vert.
- Alignement : les tirages du moteur de scénarios (v0.6) sont identiques avec ou sans clé — les pain points réels n'altèrent que la narration (événements firms), jamais les lots, fautes ni disponibilité. La série historique Monte Carlo reste comparable.
- Quota : limite officielle 5 000 transactions par intervalle de 10 minutes — le circuit complet (relevé quotidien de 91 zones + runs du jour) consomme environ 91 requêtes par jour, marge massive.
- Statut : BRANCHÉE le 31/10/2026 — engine/firms.py v1.2 (registre de zones), engine/firms_nrt.py v1.2 (relevé 91 zones), engine/flotte_monde.py v1.8, engine/scenario.py v0.6. Étiquette : DONNÉES RÉELLES (NASA FIRMS) pour les événements, SYNTHÉTIQUE pour le run global.
- Rôle : couche 1 — pain points réels par hub (opportunité d'approvisionnement, ciblage, argument techfin), base de la section feux du rapport World Ops.
- Limite : cliché du jour (pas une climatologie par hub — les fenêtres historiques restent À L'ÉTUDE), feux de moins de 375 m sous-détectés, nuages et panaches masquants, incertitude d'un facteur environ 2 sur la biomasse dérivée, aucune attribution automatique d'un feu à une biomasse précise. Détail complet : firms-hubs.md.

## Fiches réglementation v2.0 des juridictions P2 (V1.9, 31/10/2026)

- Statut : réédition sourcée des fiches réglementaires du brûlage des résidus agricoles des 7 juridictions P2 (fr-rhone, ch-leman, it-puglia, es-extremadura, ar-cuyo, ar-misiones, ma-atlas) — remplace la v0.6 du 17/10/2026. BRANCHÉE le 31/10/2026 (fiches-pays-reglementation.md et engine/fiches_reglementation.py).
- Méthode : chaque élément juridique revérifié le 31/10/2026 par croisement d'au moins deux sources, dont la source officielle primaire chaque fois qu'elle était accessible. Étiquettes : DONNÉES RÉELLES (texte lu à la date indiquée) ou À VÉRIFIER (élément non confirmé).
- Découverte centrale : la Ley 26.562 argentine reste en vigueur mais se lit AVEC la Ley 26.815 de gestion du feu (modifiée par la Ley 27.591, autorité d'application confirmée par le Decreto 73/2026) — les deux lois ensemble, ce que la v0.6 omettait.
- Points comblés : Misiones par la Résolution 293/2020 (interdiction générale en milieu rural, exception agricole soumise à plan approuvé) et la Ley XVI n° 65. Maroc : constat d'absence de norme nationale dédiée (cadres généraux Loi 13-03 pollution de l'air et Loi 28-00 déchets, articles 10, 24 et 25).
- Actualisations : amendes Mendoza saison 2026 jusqu'à 70 millions de pesos argentins (140 000 unités fiscales (UF) à 500 pesos, annonce du 14/01/2026), Estrémadure órdenes 2026 (époques de danger Infoex), Italie article 182 alinéa 6-bis introduit en 2022 et ringrano Pouilles (délibération de la junte régionale (DGR) 1149/2018).
- Sources primaires : Légifrance (L.541-21-1 II, R.541-78), Fedlex (ordonnance sur la protection de l'air (OPair) article 26a), Normattiva (décret législatif 152/2006), Boletín Oficial del Estado (Ley 7/2022 article 27.3), Diario Oficial de Extremadura (órdenes 2026), Infoleg et Boletín Oficial argentin (Ley 26.562, Ley 26.815, Decreto 73/2026), Digesto de Misiones (Ley XVI n° 65), Secrétariat général du gouvernement marocain (Loi 28-00 consolidée).
- Détections : relevé Firms (Fire Information for Resource Management System) du 17/10/2026 conservé daté par juridiction (11 Camargue voisine, 4 Pouilles, 2 Estrémadure, 1 Misiones, 2 Atlas, aucune lémanique ni cuyenne au relevé du jour).
- Garde-fou : registre de travail, pas une consultation juridique — toute décision d'engagement opérationnel exige la validation par un conseil juridique local. Toute citation externe exige une re-vérification datée.

## Abonnements satellites et extension mondiale (V2.0, 06/11/2026)

- Statut : DOCUMENTÉ, non branché côté moteur (BOITES_BASSINS inchangé). Registre d'abonnements PROPOSÉ, aucune activation externe depuis le dépôt, aucune clé versionnée. Détail complet : abonnements-satellites.md et le canvas du 06/11/2026.
- Accès vérifiés le 06/11/2026 : alertes email par zone (FIRMS, CAMS Aerosol Alerts, MyGFW du GNW (Global Nature Watch), GDACS, vigilances nationales), abonnements de catalogue CDSE (Copernicus Data Space Ecosystem) OData PULL/PUSH (quotas 12 To/30 jours glissants), diffusion EUMETCast/GEONETCast (option sites isolés), polling API pour le reste (GPM IMERG, CHIRPS v3, ERA5-Land, SMAP L4_SM, ESA CCI v09.2, ASCAT, NISAR, BIOMASS, GEDI, WaPOR, Sentinel-2 L2A, Copernicus DEM, CAMS ADS, CAMS Radiation, GWIS FWI, CEMS, EFAS/GloFAS, EONET métadonnées).
- Extension mondiale : 23 hubs virtuels (32 hubs au total), boîtes ouest, sud, est, nord, mêmes conventions que BOITES_BASSINS. Étiquette : SOURCÉ (données publiques) / ILLUSTRATION (lectures agronomiques).
- Limites : couverture par latitude et alertes critiques dans abonnements-satellites.md (sections 7 et 11).
- Rôle : couche 1 élargie, veille feux, poussières, eau, sols, biomasse et alertes multi-aléas par hub, base des sections météo, feux et aérosols du rapport World Ops.

## Snapshot FAOSTAT v18 et mappings Asie (V2.3, 14/11/2026)

- Contenu : 959 séries Production et Area harvested, fenêtre 2020-2024, extraction par l'API smart-csv de la FAO (api.data.apps.fao.org, ressource sql_url du catalogue — le bulk forestry répond 403 depuis le bac à sable, contournement documenté) ; md5 du zip stable d'un run à l'autre, donc re-téléchargeable de façon déterministe.
- Résultat : +20 pays et +72 mappings Asie dans engine/gisements_hubs.py, repli densité pour les points non couverts (294 replis documentés, 15 intrants À SOURCER) ; flotte V2.3 : 517 points, 217 hubs, 140 pays, 480 trios, 434 opérateurs, 3 078 Mt/an (verifier OK, écart maximal 4,38 %).
- Statut : BRANCHÉ (snapshot versionné engine/gisements-faostat-snapshot-v18.json ; le v17 reste versionné pour la traçabilité).
- Rôle : couche 1 — dimensionnement de la flotte par gisement réel.

## Atlas CaO P2.9 — USGS, FAOSTAT bois, OWID (14/11/2026)

- Contenu : USGS Mineral Commodity Summaries 2026 (ciment en kt, fonte-acier en Mt, extraction positionnelle data/pdfpos.py), FAOSTAT bois rond 2024 (API smart-csv, article 1864, 139 pays), population 2023 Our World in Data (prorata USGS).
- Accès : libres et publics ; PDF USGS et CSV OWID hors dépôt (chemin WT_DATA_BRUTES pour data/gen_cao.py), snapshots dérivés versionnés dans data/ (rejouables, md5 stables).
- Statut : BRANCHÉ (engine/atlas_cao.py, sortie data/cao-hubs-public.json sans aucun coût ; sortie PRIVÉE locale jamais versionnée).
- Rôle : couche approvisionnement minéral du module Carb — capacité nationale proratisée vs besoin 582 t CO2/an par trio, statuts par hub. Détail : atlas-cao-hubs.md.

## Sourcing P3 — Global Energy Monitor (14/11/2026)

- Contenu : Global Cement and Concrete Tracker juillet 2025 (2 887 cimenteries retenues), Global Iron and Steel Tracker mars 2026 niveau usine (457 unités de hauts fourneau), Global Bioenergy Power Tracker v3 (DOI Zenodo 10.5281/zenodo.20843067, CC BY 4.0, 910 lignes bois) — tous libres et publics, versionnés dans data/ avec le lecteur stdlib data/xlslite.py.
- Statut : BRANCHÉ (engine/sourcing_p3.py, géomatch Haversine rayon 50 km étendu à 100 km, sorties data/sourcing-p3-public.json et data/p3-sites-snapshot.json sans aucun coût ; sortie PRIVÉE locale jamais versionnée).
- Limites : données GEM vivantes (écarts vs repères du 11/11 tracés dans verifier : paires +5,5 %, cimenteries +5,1 %, unités 457 vs 458) ; ruraux sans site à 100 km (91 hubs A_SOURCER).
- Rôle : couche approvisionnement local du module Carb — la contrainte est la concentration locale, pas le gisement mondial. Détail : sourcing-p3.md.

## Vague P1 — figeage des paramètres par trio et pointage météo des hubs (V2.3.1, 14/11/2026)

- Figeage (engine/parametres_trios.py, sortie versionnée data/parametres-trios.json) : 489 trios figés (480 généralisés + 9 pilotes P2 dont ma-atlas 3 trios), 224 équipes, 448 opérateurs tournants (2 par équipe, 5 trios maximum par équipe), MTBF (Mean Time Between Failures, temps moyen entre pannes) 720 h et MTTR (Mean Time To Repair, temps moyen de réparation) 8 h — baseline V1.6, ILLUSTRATION non calibrée, variantes M1/M2/M3 éteintes ; graine par trio (convention « graine_trio = graine_hub + indice − 1 », le trio 1 gardant la graine du hub) ; fenêtre d'opération, mois de maintenance et statut CONTINUE/SAISONNIÈRE. Aucun paramètre calibré du VDE.
- Statuts des sources : FAOSTAT BRANCHÉE (snapshot v18, cf. section V2.3) ; GEOGLAM CROISÉE pour les céréales AMIS, pérennes À SOURCER (curation manuelle — les calendriers AMIS ne sont pas téléchargeables, limite documentée) ; NASA FIRMS vérifié (217 zones GPS de hubs enregistrées = 217 hubs généralisés, firms.enregistrer_zone_gps via flotte_monde) ; Open-Meteo BRANCHÉ pour le pointage des hubs.
- Pointage météo des hubs : UN appel Open-Meteo multi-points rafraîchit les 219 hubs (engine/build_carte.py --meteo-hubs, fichier versionné data/meteo-hubs-pointage.json — données météo publiques, aucune donnée économique ; réinjection du pointage figé dans chaque build de carte, option --offline pour un build reproductible).
- Garde-fous : verifier du figeage (recomptages, conventions, zones FIRMS, anti-fuite, reprise octet par octet) ; contrôle du générateur de cartes (219 hubs couverts par les couches CaO/P3, pointage météo complet si présent). Détail : parametres-trios.md.

## Vague V2.4 — pérennes : ratios sourcés par la littérature (14/11/2026)

- Limite GEOGLAM (Global Agricultural Geo-monitoring Initiative) comblée : les calendriers AMIS (Agricultural Market Information System) ne couvrent que quatre céréales ; les cultures pérennes restent en curation manuelle. Le deepsearch « pérennes » du 14/11/2026 (47 sources, chaque ratio croisé d'au moins deux sources dont la primaire) fournit les ratios SOURCÉS appliqués aux atlas.
- Ratios SOURCÉS appliqués : sarments de vigne 1,5 à 2,9 t/ha/an, retenu 2 t/ha (BIVB — Bureau Interprofessionnel des Vins de Bourgogne, France ; Velázquez-Martí et al., Italie treillis) ; rameaux d'olivier 1,31 t/ha/an en taille annuelle, 3,02 t/ha en taille bisannuelle (Velázquez-Martí et al., Méditerranée) ; rafles de palmier (EFB — Empty Fruit Bunches) 0,22 fois les régimes, fourchette 0,20-0,28 (220-243 kg/t) ; coques de cacao 67-76 pour cent de la cabosse, retenu 3,0 fois les fèves en poids frais (planification littérature jusqu'à 10 fois) ; coques et parches de café robusta 0,20 fois le café marchand en voie sèche (fourchette 0,20-0,50 selon voie) ; pulpe de café 30-50 pour cent du fruit, soit environ 2,0 fois le café vert (fourchette 1,5-2,5) ; bourre de coco 0,35 fois la noix (FAO — Food and Agriculture Organization of the United Nations, Y3612E), coque 0,15 fois ; écales d'amande 52 pour cent et coques 33 pour cent du fruit frais, ratio global retenu 2,0 (fourchette 2,0-2,8, biomasse californienne 3,1 Mt 2017).
- Nouveaux intrants versionnés (atlas pays v1.1 V2.4) : EFB_PALMIER_MY (Sabah, rafles ≈ 22,0 Mt/an), EFB_PALMIER_CI (Grand-Lahou, ≈ 0,51 Mt/an), EFB_PALMIER_EC (Santo Domingo, ≈ 0,58 Mt/an), BOURRE_COCO_MY (Kudat, ≈ 0,24 Mt/an), PULPE_CAFE_MX (Tapachula, ≈ 0,39 Mt/an, fenêtre nov-févr). Le Viêt Nam n'a pas de jeton pulpe : la voie sèche robusta y est dominante, le jeton COQUE_CAFE_VN porte le flux.
- Essais biochar locaux : registre des partenariats candidats versé au dossier (essais-biochar-perennes.md — Toscane, Chianti Classico, Andalousie, Colombie, Ghana, Malaisie), doctrine : aucune sollicitation externe avant la clôture de la levée d'amorçage de 500 k€.
- Triangulation des organisations intergouvernementales : IOC (International Olive Council), OIV (International Organisation of Vine and Wine), ICCO (International Cocoa Organization), ICO (International Coffee Organization), complétée par GAEZ (Global Agro-Ecological Zoning, FAO et IIASA — International Institute for Applied Systems Analysis) v5 pour les surfaces pérennes.
- Impact flotte (vérifié au verifier) : 522 points d'atlas (+5), 217 hubs, 480 trios, 434 opérateurs inchangés ; les cinq nouveaux points fusionnent dans les clusters de leurs compagnons ; centres réactualisés de gen-cote-d-ivoire-2 et gen-equateur-1 (glissement de quelques dizaines de km, moyennes de cluster) ; figeage P1 régénéré (reprise octet par octet OK) ; sourcing P3 régénéré (médiane 75,9 → 76,3 km, écart 0,60 %, statuts inchangés) ; les cinq jetons sont À SOURCER dans gisements_hubs en attendant leurs séries au snapshot v19 (jamais de valeur inventée).
- Étiquette commune : ETQ_GISEMENT_SOURCÉ_LIT (« SOURCÉ (production FAOSTAT 2024) + ratio SOURCÉ (littérature, deepsearch pérennes 14/11/2026) ») appliquée aux seuls gisements concernés ; les marcs de raisin restent en ratio ILLUSTRATION (0,15 fois la vendange, à sourcer).

## Vague V2.5 — sites de transformation post-récolte (14/11/2026)

- Quatre attributs posés sur les 219 hubs sans toucher aux coordonnées ni aux figeages (aucun effet cascade, contrairement à la V2.4) : type de site dominant, coefficient de captabilité, profil énergétique et indice logistique. Question centrale : où sont les gisements AU SITE de transformation, pour ne pas aller chercher les biomasses aux champs.
- Deepsearch post-récolte du 14/11/2026 (canvas world-twin-transformation-post-recolte, ~47 sources croisées) : habitudes de transformation entre récolte et conditionnement, infrastructures (moulin de palmier à huile, rizerie, sucrerie, moulin d'olive, chai, bénéficio, décortiqueur, huller, distillerie, station de conditionnement, scierie), volumes et parcs d'usines par pays, méthodes et machines, besoins énergétiques, co-produits et résidus disponibles au site, routes et qualité d'accès.
- 24 familles de sites (engine/sites_transformation.py, premier motif matché gagne, dominante = captabilité la plus élevée) : captabilités ILLUSTRATION de 0,10 (gisement diffus AU_CHAMP, SARMENTS, CACAO en centre coopératif) à 0,95 (CHAI, BRASSERIE) ; 515 jetons couverts, familles dominantes AU_CHAMP=121, RIZ=48, MAIS=37, CANNE=33, NOIX_COQUES=25, PALMIER=18, etc.
- Profil énergétique SOURCÉ : AUTONOME (le site vend de l'énergie — moulin de palmier, rizerie de parboiling, sucrerie : chaudières biomasse + turbines, autofourniture documentée MPOB, CNP, UNICA) contre IMPORTATEUR (le site achète — chai, moulin d'olive, bénéficio, scierie). Fenêtre de fraîcheur par famille (< 24 h palmier, < 48 h canne, heures chais/beneficios, jours, continu, stockable).
- Logistique : LPI 2023 (Logistics Performance Index, Banque mondiale, 139 pays enquêtés, score 1 à 5) SOURCÉ pour 187 hubs ; 32 hubs À SOURCER (pays non enquêtés 2023 : 26 ISO absents de l'enquête, dont MAR, CIV, ECU, KEN, PAK, TUR — jamais de valeur inventée) ; RAI (Rural Access Index, indicateur 9.1.1 des ODD — Objectifs de Développement Durable) À SOURCER en vague suivante (extraction dédiée NASA SEDAC — Socio Economic Data and Applications Center).
- Documentation : sites-transformation.md ; cartes bi-modes régénérées (table « Site de transformation — V2.5 » dans la fiche hub des deux modes, anti-fuite étendu à la couche sites, verifier build_carte OK : 219 couches sites). Flotte INVARIANTE vérifiée : les cinq fichiers de données versionnés sont identiques octet par octet au bundle V2.4.

## Vague V2.6 — pérennes FAOSTAT, RAI sourcé, captabilités figées (14/11/2026)

- Jetons pérennes V2.4 activés avec les séries FAOSTAT du snapshot v18 (959 séries vérifiées à l'identique du bulk officiel md5 1a202c5674dce152f1134fa87b220b82, date interne 2025-12-23, aucun v19 requis) : cinq mappings inscrits dans engine/gisements_hubs.py — EFB_PALMIER_CI (0,20-0,28 × régimes, Côte d'Ivoire ≈ 2,3-2,8 Mt/an), EFB_PALMIER_MY (0,20-0,28, Malaisie), EFB_PALMIER_EC (0,20-0,28, Équateur), BOURRE_COCO_MY (0,30-0,40 × noix, SOURCÉ FAO Y3612E), PULPE_CAFE_MX (1,5-2,5 × café vert, deepsearch pérennes). Impact flotte vérifié : gen-malaisie-1 (Sabah, porte EFB_PALMIER_MY ≈ 22 Mt/an) passe à 4 trios ; 481 trios généralisés (480 → 481), 434 opérateurs inchangés, 217 hubs inchangés, 522 points d'atlas, points sourcés 200 (15 À SOURCER, avant 20), somme mondiale 3 101 Mt/an (avant 3 078) ; besoin CaO 279 942 t/an (481 × 582) ; figeage P1 régénéré (490 trios figés, reprise octet par octet OK) ; couches publiques sourcing P3 et atlas CaO régénérées.
- RAI (Rural Access Index, indicateur 9.1.1 des ODD — Objectifs de Développement Durable : part de la population rurale vivant à moins de 2 km d'une route praticable toute saison) SOURCÉ pour les 219 hubs (fin de l'à-trait V2.5) : jeu « Rural Access Index by Country (2022-2023) » du SDSN (Sustainable Development Solutions Network) SDG Transformation Center, d'après la méthodologie Banque mondiale, extrait le 14/11/2026 par l'API ArcGIS du hub (200 entités, 189 pays retenus, 199 valeurs 2023 valides, territoires contestés exclus, licence Creative Commons BY-NC-SA 4.0, usage interne avec attribution) ; les 140 pays de la flotte sont tous couverts — table RAI_2023 dans engine/sites_transformation.py, colonne RAI dans la table site des cartes, 219 SOURCÉ, 0 À SOURCER. Exemples : FRA 98, MAR 99, CIV 90, NER 65, ESP et ITA 100.
- Captabilités figées par famille avec étiquette SOURCÉ quand la littérature chiffre la fraction disponible au site (deepsearch post-récolte du 14/11/2026, canvas world-twin-transformation-post-recolte) : CACAO (0,20 — BioCycle/USAID environ 75 pour cent de la cabosse au champ, valeur sous la borne), VIGNE_MARC (0,95 — FranceAgriMer 93-99 pour cent des marcs en distillerie), OLIVE (0,85 — MDPI alperujo 80-85 pour cent du fruit), RIZ (0,90 — CNP balle 20 pour cent du paddy), CANNE (0,90 — UNICA autofourniture bagasse), PALMIER (0,90 — MPOB/PalmWatch, régimes entiers au moulin en moins de 24 h) ; les 18 autres familles restent ILLUSTRATION (aucune fraction chiffrée : la valeur ne sort pas du jugement d'ingénieur). Statut du hub = SOURCÉ seulement si toutes ses familles le sont : 32 hubs SOURCÉ, 187 ILLUSTRATION. Documentation : sites-transformation.md, table « Site de transformation — V2.6 » dans les cartes.
