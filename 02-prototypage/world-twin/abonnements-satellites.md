# Abonnements satellites et veille mondiale : World Twin (V2.0, 06/11/2026)

Demande de Manu Moineau (06/11/2026) : examiner toutes les possibilités d'abonnement aux satellites et à leurs données utiles, croisées et enregistrées pour le World Twin, puis extension à toutes les régions du monde, comme si les Trio Nomad étaient en opération en Afrique, en Asie, dans le Pacifique, aux États-Unis, au Canada, en Europe du Nord et de l'Est et au Moyen-Orient. Livrable de référence : le canvas « World Twin : abonnements satellites, données utiles, croisements et enregistrement (06/11/2026) » (notes de sources complètes avec URL exactes et crédibilité sur 5). Ce fichier en est la version dépôt.

DOCTRINE (inchangée) : données publiques étiquetées SOURCÉ, toute simulation étiquetée SYNTHÉTIQUE (« simulation » devant les investisseurs), toute lecture agronomique ILLUSTRATION. Aucune valeur calibrée, aucune clé, aucun jeton dans ce dossier (la MAP_KEY FIRMS, les clés ADS (Atmosphere Data Store), CDS (Climate Data Store), CDSE (Copernicus Data Space Ecosystem), les jetons Earthdata et l'EKU (EUMETSAT Key Unit) vivent uniquement en local, motif *.env). Caches (cache-sols/, cache-meteo-temps-reel/, cache-firms-histo/, cache-faostat-bulk/ et autres cache-*/) jamais versionnés. Télémétrie SYNTHÉTIQUE sur le registre de DÉVELOPPEMENT uniquement, jamais le registre Merkle de production.

## 1. Sources déjà branchées (couche 1 actuelle au 06/11/2026)

- NASA FIRMS (Fire Information for Resource Management System) via API (Application Programming Interface) : MAP_KEY locale (firms.env, jamais versionnée), capteurs VIIRS (Visible Infrared Imaging Radiometer Suite) NOAA-20 et NOAA-21 NRT (Near Real Time) plus MODIS (Moderate Resolution Imaging Spectroradiometer), 91 zones (10 bassins P2 + 81 hubs généralisés v1.8), repli synthétique sans clé. Suomi NPP retiré le 01/11/2026.
- Open-Meteo (réanalyse ERA5 de l'ECMWF, European Centre for Medium-Range Weather Forecasts) : agrégats mensuels réels versionnés dans cache-meteo/agregats-mensuels.json (10 bassins), branche temps réel pour les 52 points de l'atlas v1.0 (cache horaire non versionné).
- FAOSTAT (Organisation des Nations unies pour l'alimentation et l'agriculture) bulk : snapshot v1.7 versionné (engine/gisements-faostat-snapshot-v17.json), 599 séries, fenêtre 2020-2024, licence CC BY 4.0.
- GEOGLAM Crop Monitor : calendriers sous-nationaux, bulletins AMIS (Agricultural Market Information System) et CM4EW.
- NASA EMIT (Earth Surface Mineral Dust Source Investigation) : granules L2B MIN et L3 ASA dans data/emit/, extraction locale (lecteur HDF5 (Hierarchical Data Format version 5) maison, bibliothèque standard uniquement), 5/10 bassins couverts en L3 ASA au 06/11/2026, scènes 2302410_038 (Cuyo) et 2420510_006 (Atlas).
- CAMS (Copernicus Atmosphere Monitoring Service) Aerosol Alerts : deux abonnements actifs par email (Dust Cuyo, boîte −36,37 à −28,52 / −70,66 à −66,93, épisode prévu 06-07/11/2026 niveau ≥ 1, et Dust Haouz, boîte 30,44 à 33,20 / −10,63 à −5,76, épisode 26-28/10/2026 passé), paramètre od550dust, six fils Gmail étiquetés Vignite/International.
- SoilGrids et Natural Earth (cartes dans data/).

## 2. Quatre mécanismes d'abonnement retenus (gratuits ou coût nul au démarrage)

1. Alertes email par zone : FIRMS Fire Alert Subscription, CAMS Aerosol Alerts, MyGFW (My Global Forest Watch, portail du GNW, Global Nature Watch, ex GFW, Global Forest Watch) avec AOI (Area of Interest) sauvegardée, GDACS (Global Disaster Alert and Coordination System), vigilances météorologiques nationales, bulletins GEOGLAM/AMIS.
2. Abonnements de catalogue CDSE (Copernicus Data Space Ecosystem) OData (Open Data Protocol) PULL/PUSH sur Sentinel-1, Sentinel-2 L2A (Level-2A), Sentinel-3, Sentinel-5P, avec filtres bbox par boîte. Quotas constatés : 12 To/30 jours glissants, 4 connexions, 20 Mo/s. Nouveau catalogue STAC (SpatioTemporal Asset Catalog) SFEOS en service depuis le 16/10/2026.
3. Diffusion multicast par satellite : EUMETCast Europe (plus de 4 000 stations), EUMETCast Terrestrial (NREN, National Research and Education Network, requis), GEONETCast Americas, CMACast. Option pour les sites Nomad isolés (réception indépendante d'Internet). L'EKU n'est jamais versionnée.
4. Polling API (Application Programming Interface) pour le reste : SMAP (Soil Moisture Active Passive) L4_SM, ESA (European Space Agency) CCI (Climate Change Initiative) Soil Moisture v09.2 sans compte via le CEDA, GPM (Global Precipitation Measurement) IMERG (Integrated Multi-satellitE Retrievals for GPM) Early, CHIRPS (Climate Hazards Group InfraRed Precipitation with Station data) v3, ARC2, GSMaP_NOW, GWIS (Global Wildfire Information System) FWI (Fire Weather Index), CAMS ADS, CAMS Radiation via SoDa, WaPOR (Water Productivity through Open access of Remotely sensed data) v3 sans jeton, Sentinel-2 L2A via Sentinel Hub, Planetary Computer STAC, Copernicus DEM (Digital Elevation Model) GLO-30, BIOMASS L2A, GEDI (Global Ecosystem Dynamics Investigation) L4B, NISAR (NASA-ISRO SAR, Synthetic Aperture Radar) bande L, EnMAP, PRISMA, EONET (métadonnées seulement), CEMS (Copernicus Emergency Management Service) Rapid Mapping API publique, EFAS/GloFAS.

## 3. Matrice des sources candidates par famille (détails et URL dans le canvas)

- Feux, danger d'incendie, émissions : FIRMS NRT + alertes email, GWIS FWI, alertes GNW feux (VIIRS 375 m) et changement forestier (GLAD-L, GLAD-S2, RADD, DIST-ALERT), GFAS (Global Fire Assimilation System).
- Eau : précipitations GPM IMERG V07B Early (latence 4 h, maille 0,1°, 30 min, toutes latitudes), CHIRPS v3 (0,05°, 60°S-60°N, la v2 s'arrête après décembre 2026), CMORPH (CPC (Climate Prediction Center) de la NOAA (National Oceanic and Atmospheric Administration), 8 km, 30 min, 60°S-60°N), GSMaP_NOW (JAXA, Japan Aerospace Exploration Agency), ARC2 (Maroc), ERA5-Land (9 km horaire, mondial depuis 1950, eau volumique du sol niveaux 1 à 4, via le CDS, licence CC BY), humidité du sol SMAP L4_SM (±85,044°), ESA CCI v09.2 (jusqu'au 31/12/2024, sans compte), ASCAT (Advanced Scatterometer) via EUMETSAT (European Organisation for the Exploitation of Meteorological Satellites) H SAF, NISAR L3 humidité du sol 200 m (400 m au Sahara), inondations Sentinel-1 GRD (Ground Range Detected) + NISAR.
- Sols, végétation, biomasse : EMIT L3 ASA (±55°), SoilGrids, Sentinel-2 L2A (NDVI, sols nus, dégâts, 56°S-82,8°N), Landsat 8/9 USGS (United States Geological Survey) + HLS (Harmonized Landsat Sentinel-2) v2.0 (mondial sauf Antarctique depuis avril 2013), BIOMASS (56°S-75°N mais exclut opérationnellement l'Amérique du Nord et l'Europe), GEDI L4B (±51,6°), WaPOR v3 (Afrique et Proche-Orient uniquement, boîte longitude −30 à 65 et latitude −40 à 45), EnMAP (DLR, Deutsches Zentrum für Luft- und Raumfahrt), PRISMA (ASI, Agence spatiale italienne, portail en maintenance au 06/11/2026).
- Atmosphère, aérosols, qualité de l'air, rayonnement : CAMS ADS (Europe 0,1°, global environ 0,4°, changement de CGU le 05/10/2026 et mesures anti-abus le 22/10/2026 à surveiller), prévisions globales CAMS, CAMS Radiation / HelioClim-3 via SoDa (gratuit avec inscription, 100 requêtes/jour), Sentinel-5P TROPOMI (NO2, O3, aérosols), SMOS.
- Imagerie, altitude, occupation du sol : Sentinel-2 L2A, Landsat, Copernicus DEM GLO-30, WorldCover, PRISMA/EnMAP hyperspectral sur demande.
- Alertes multi-aléas et diffusion : GDACS, EONET (métadonnées, erreurs HTTP 500 constatées en avril 2026), CEMS Rapid Mapping, EFAS/GloFAS, vigilances nationales (section 8), WMO (World Meteorological Organization) WIS 2.0 (WMO Information System), Meteoalarm.

## 4. Croisements proposés par bassin (couche par couche)

Pour chaque bassin/hub, le World Twin croise : (1) minéraux de surface EMIT L3 ASA quand couvert, (2) poussières CAMS od550dust, (3) feux actifs FIRMS + alertes email FIRMS + alertes GNW, (4) danger d'incendie GWIS FWI, (5) précipitations IMERG Early + CHIRPS v3 (+ ARC2 Maroc, GSMaP_NOW), (6) humidité du sol SMAP L4_SM + ESA CCI v09.2 + ASCAT + NISAR, (7) imagerie Sentinel-2 L2A, (8) SAR (Synthetic Aperture Radar) NISAR + Sentinel-1 (inondations, humidité), (9) biomasse BIOMASS L2A + GEDI L4B (+ WaPOR Afrique et Proche-Orient), (10) altitude Copernicus DEM GLO-30 + WorldCover, (11) qualité de l'air CAMS ADS (Europe), (12) rayonnement CAMS Radiation, (13) alertes officielles nationales + GDACS + EONET. Croisement déjà observé : les alertes poussières CAMS (Cuyo, Haouz) et les scènes EMIT retenues (2302410_038 Cuyo, 2420510_006 Atlas) pointent les mêmes régions sources de poussières minérales.

## 5. Protocole d'enregistrement

Caches locaux jamais versionnés (motifs cache-*/ et *.env), empreintes md5/SHA-256 et horodatage UTC consignés, aucune clé ni jeton consigné, étiquettes SOURCÉ/SYNTHÉTIQUE/ILLUSTRATION systématiques, registre d'abonnements tenu (section 10) avec service, zone, paramètre, canal, étiquette, dernier contrôle, le dernier passage World Ops reste horodaté dans ops-horodatage.md par le run, pas à la main.

## 6. Extension mondiale : 23 hubs virtuels (32 hubs au total)

Hypothèse de travail (demande Manu du 06/11/2026) : comme si des unités Trio Nomad étaient en opération dans chaque zone. Boîtes ouest, sud, est, nord, même convention que BOITES_BASSINS (engine/atlas_sols_emit.py, inchangé, 10 bassins). Données publiques SOURCÉ uniquement, lectures agronomiques ILLUSTRATION.

| Hub virtuel | Zone | Boîte (ouest, sud, est, nord) |
|---|---|---|
| sahel-ouest | Afrique de l'Ouest | −18, 8, 8, 20 |
| afrique-est | Afrique de l'Est | 30, −12, 43, 6 |
| afrique-centrale | Afrique centrale | 9, −14, 28, 4 |
| afrique-australe | Afrique australe | 16, −35, 33, −22 |
| egypte-nil | Égypte et Nil | 24, 21, 36, 32 |
| golfe-arabique | golfe Persique | 44, 12, 60, 30 |
| levant | Levant | 34, 29, 44, 37 |
| turquie-anatolie | Turquie | 26, 36, 45, 42 |
| inde-asie-du-sud | Asie du Sud | 68, 6, 89, 36 |
| asie-sud-est | Asie du Sud-Est | 95, −11, 141, 8 |
| asie-est | Asie de l'Est | 100, 20, 145, 46 |
| asie-centrale | Asie centrale | 48, 36, 80, 56 |
| oceanie-australie | Australie | 112, −44, 154, −10 |
| nouvelle-zelande-pacifique | Pacifique sud-ouest | 160, −48, 180, −25 |
| bresil-sudeste | Brésil sud-est | −55, −30, −35, −5 |
| usa-midwest | États-Unis, Midwest | −102, 35, −78, 49 |
| usa-ouest | États-Unis, Ouest | −125, 30, −104, 49 |
| usa-sud | États-Unis, Sud | −106, 25, −74, 37 |
| canada-prairies | Canada, Prairies | −120, 49, −90, 60 |
| canada-est | Canada, Est | −95, 42, −55, 56 |
| europe-nord | Europe du Nord | 4, 54, 32, 71 |
| europe-est | Europe de l'Est | 14, 41, 41, 60 |
| iles-britanniques | îles britanniques | −10, 49, 2, 60 |

## 7. Couverture des sources par latitude (vérifiée le 06/11/2026)

- Mondial, tous les hubs : FIRMS, GWIS, GNW, CAMS alertes et prévisions globales, GDACS, Sentinel-1/3/5P, SMAP ±85,044°, ESA CCI, ASCAT, ERA5/ERA5-Land, NISAR bande L (produit L3 humidité du sol 200 m mondial), GPM IMERG V07B (toutes latitudes sauf quelques boîtes polaires), Landsat + HLS v2.0 (sauf Antarctique).
- Sentinel-2 L2A : 56°S à 82,8°N, tous les hubs couverts (nord maximal des boîtes : 71°N).
- CHIRPS v3, CMORPH, GSMaP : 60°S à 60°N seulement, repli ERA5-Land au-delà (hubs europe-nord et canada-prairies).
- GEDI ±51,6° et EMIT ±55° : europe-nord et canada partiellement hors, repli biomasse Landsat ORNL DAAC (Oak Ridge National Laboratory Distributed Active Archive Center).
- BIOMASS : 56°S à 75°N mais Amérique du Nord et Europe EXCLUES (coordination avec les radars du Département de la Défense des États-Unis), donc pas de BIOMASS pour les hubs États-Unis, Canada, Europe.
- WaPOR v3 : Afrique et Proche-Orient uniquement (8 hubs sur 32).
- NISAR : regard à gauche uniquement, trou au pôle Arctique, bande S (ISRO, Indian Space Research Organisation) Inde et sites de calibration seulement.

## 8. Imagerie géostationnaire et services météo nationaux ouverts, par région

| Région | Satellite géostationnaire et accès gratuit | Service météo national ouvert |
|---|---|---|
| Europe, Afrique, Moyen-Orient, océan Indien | Meteosat MSG (Meteosat Second Generation) 0°, 45,5°E, 9,5°E et MTG-I1 (Meteosat Third Generation) 0° depuis le 16/06/2025, imageur FCI (Flexible Combined Imager) disque 10 min 16 canaux, imageur d'éclairs LI (Lightning Imager) 83 % du disque, via EUMETCast et Data Store | Météo-France Vigilance + APIC (georisques.gouv.fr), AEMET (RSS/Atom au format CAP, Common Alerting Protocol), DWD (Deutscher Wetterdienst) opendata.dwd.de (CAP + MOSMIX sans clé), MeteoSwiss, DMN Maroc (vigilance.ma), Meteoalarm |
| Amériques | GOES-19 (Geostationary Operational Environmental Satellite, Est 75,2°W depuis le 04/04/2025) et GOES-18 (Ouest), buckets Amazon S3 (Simple Storage Service) publics noaa-goes16/17/18/19 en accès --no-sign-request, GLM (Geostationary Lightning Mapper) sur Planetary Computer | NWS (National Weather Service) api.weather.gov sans clé (en-tête User-Agent avec contact obligatoire, alertes CAP), USGS api.waterdata.usgs.gov (clé gratuite, ancien service keyless retiré au premier trimestre 2027), ECCC (Environment and Climate Change Canada) dd.weather.gc.ca (CAP, AMQP (Advanced Message Queuing Protocol), WMS (Web Map Service) ALERTS, GEM en GRIB2 (GRIB édition 2)) |
| Asie-Pacifique | Himawari-8/9 (140,7°E) via le portail P-Tree de la JAXA (compte demandé, temps réel 5 à 20 min, usage commercial autorisé depuis le 01/02/2026, redistribution des brutes interdite), portail JMA (Japan Meteorological Agency) ds.data.jma.go.jp | JMA, BOM (Bureau of Meteorology) Australie Water Data Online (gratuit, CC BY) |
| Russie, Asie centrale, Europe de l'Est, Pacifique ouest | Elektro-L (76°E, 14,5°W, 165,8°E), imageur MSU-GS 1 km visible 4 km infrarouge, disque 15 à 30 min, HRIT/LRIT (High Rate Information Transmission / Low Rate Information Transmission), portail WMO OSCAR (space.oscar.wmo.int) | Roshydromet, WMO WIS 2.0 filet mondial |
| Mondial (filet de sécurité) | GDACS, EONET, WIS 2.0 | tous les services ci-dessus |

## 9. Nouveaux abonnements proposés pour les 23 hubs virtuels (statut PROPOSÉ, rien activé)

- FIRMS : alerte email par boîte de hub (23 boîtes), VIIRS NOAA-20/NOAA-21 + MODIS, NRT, pièces jointes CSV (Comma-Separated Values) ou KML (Keyhole Markup Language) optionnelles.
- CAMS Aerosol Alerts : boîtes « poussières » pour les 6 hubs exposés (sahel-ouest, egypte-nil, golfe-arabique, asie-centrale, afrique-australe, oceanie-australie).
- GNW/MyGFW : une AOI par hub (23 AOI), notifications email feux et changement forestier.
- CDSE : abonnements OData PULL avec filtres bbox sur les 23 boîtes, collections Sentinel-1 GRD, Sentinel-2 L2A, Sentinel-3, Sentinel-5P.
- Alertes nationales : api.weather.gov (3 hubs États-Unis), dd.weather.gc.ca (2 hubs Canada), opendata.dwd.de (Europe centrale), AEMET, Météo-France/APIC, MeteoSwiss, BOM (Australie), DMN Maroc, plus GDACS en global.
- Option terrain : EUMETCast Terrestrial ou GEONETCast Americas pour une station Nomad isolée, GOES via AWS (Amazon Web Services) pour les Amériques.

Aucune sollicitation externe n'a été faite depuis ce dépôt : l'activation de ces abonnements (création de comptes, de clés, d'AOI) reste à la décision de Manu Moineau.

## 10. Registre d'abonnements (proposé)

| Service | Zone | Paramètre | Canal | Étiquette | Dernier contrôle | Statut |
|---|---|---|---|---|---|---|
| FIRMS API | 91 zones (10 bassins + 81 hubs) | feux actifs VIIRS/MODIS NRT | API + firms.env local | DONNÉES RÉELLES | 06/11/2026 | ACTIF |
| CAMS Aerosol Alerts | Dust Cuyo, Dust Haouz | od550dust, seuil ≥ 1 | email | SOURCÉ | 06/11/2026 (épisode 06-07/11 prévu) | ACTIF |
| Open-Meteo ERA5 | 10 bassins + 52 points | météo mensuelle + temps réel | API sans clé | SOURCÉ | 06/11/2026 | ACTIF |
| FIRMS email | 32 hubs | alertes feux par zone | email | SOURCÉ | à activer | PROPOSÉ |
| CAMS poussières | 6 hubs exposés + 8 bassins restants | od550dust | email | SOURCÉ | à activer | PROPOSÉ |
| MyGFW/GNW | 32 hubs | AOI, alertes feux + changement forestier | email | SOURCÉ | à activer | PROPOSÉ |
| CDSE OData | 32 boîtes | Sentinel-1/2/3/5P | PULL catalogue | SOURCÉ | à activer | PROPOSÉ |
| Alertes nationales | hubs concernés | CAP, vigilances | API/RSS/AMQP | SOURCÉ | à activer | PROPOSÉ |
| GDACS | mondial | multi-aléas | email/web | SOURCÉ | à activer | PROPOSÉ |

## 11. Alertes critiques

- Aucune clé ni jeton dans le dépôt (voir doctrine).
- BIOMASS exclut l'Amérique du Nord et l'Europe : ne pas la retenir pour les hubs États-Unis, Canada, Europe.
- Au-delà de 60°N : repli ERA5-Land pour précipitations et humidité du sol.
- CHIRPS v2 s'arrête après décembre 2026 : migrer vers la v3.
- WaPOR réservé à l'Afrique et au Proche-Orient.
- NISAR : trou au pôle Arctique, compléter par Sentinel-1.
- Himawari : redistribution des données brutes interdite.
- USGS : migrer vers api.waterdata.usgs.gov avant le retrait du service keyless (premier trimestre 2027).
- EONET fournit des métadonnées, pas des mesures.
- PRISMA : portail en maintenance au 06/11/2026.
- CAMS ADS : changement de CGU (05/10/2026) et mesures anti-abus (22/10/2026), incident du 23/10/2026 : à surveiller pour un usage automatisé.
- Télémétrie SYNTHÉTIQUE, registre de DÉVELOPPEMENT uniquement.

## 12. Sources clés vérifiées le 06/11/2026 (sélection, liste complète dans le canvas)

- FIRMS alerts : https://firms.modaps.eosdis.nasa.gov/alerts/
- CDSE subscriptions et quotas : https://documentation.dataspace.copernicus.eu/APIs/Subscriptions.html et https://documentation.dataspace.copernicus.eu/Quotas.html
- GPM IMERG : https://gpm.nasa.gov/data/directory
- ERA5-Land (CDS) : https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land
- CHIRPS v3 : https://chc.ucsb.edu/data/chirps et https://cgiar-climate-data-hub.github.io/catalog/chirps-v3-daily/
- ESA CCI Soil Moisture v09.2 (CEDA) : https://admin.climate.esa.int/
- SMAP L4_SM : https://earthdata.nasa.gov/data/catalog/nsidc-cprd-spl4smlm-008
- NISAR : https://science.nasa.gov/mission/nisar/mission-overview/ et https://asf.alaska.edu/ (ASF, Alaska Satellite Facility)
- BIOMASS (ESA) : https://www.esa.int/ (données ouvertes depuis le 26/01/2026)
- GEDI L4B : https://daac.ornl.gov/ (DOI 10.3334/ORNLDAAC/2299)
- WaPOR v3 : https://data.apps.fao.org/wapor/ (API sans jeton)
- Sentinel-2 : https://sentiwiki.copernicus.eu/web/s2-mission
- HLS v2.0 : https://www.usgs.gov/ (publication 70266349)
- EUMETSAT Meteosat : https://user.eumetsat.int/data/satellites/
- GOES (AWS) : https://registry.opendata.aws/noaa-goes/
- Himawari P-Tree : https://www.eorc.jaxa.jp/ptree/
- NWS API : https://www.weather.gov/documentation/services-web-api
- USGS water : https://www.usgs.gov/tools/usgs-water-data-apis
- ECCC open data : https://dd.weather.gc.ca/ et https://github.com/ECCC-MSC/open-data
- DWD opendata : https://opendata.dwd.de/
- BOM : https://www.bom.gov.au/waterdata/
- GDACS : https://www.gdacs.org/
- GNW/MyGFW : https://www.globalnaturewatch.org/

## 13. Gouvernance et prochaine vague

Rite « je prépare, tu pousses » : cette vague V2.0 pousse la documentation uniquement, avec validation explicite de Manu Moineau (06/11/2026). Aucun module moteur modifié (BOITES_BASSINS inchangé, 10 bassins), aucun abonnement externe activé, aucune clé créée, ops-horodatage.md inchangé (mis à jour par le run World Ops). Prochaine vague proposée (à décision de Manu) : activation des alertes gratuites (FIRMS email, CAMS, GNW, GDACS, vigilances nationales) sur les 32 hubs, abonnements CDSE OData PULL, puis prototype local de la couche « hubs virtuels » (caches non versionnés) avec les replis documentés (ERA5-Land au-delà de 60°N, Landsat/GEDI pour la biomasse aux hautes latitudes et en Amérique du Nord, WaPOR Afrique et Proche-Orient uniquement).
