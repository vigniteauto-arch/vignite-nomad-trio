# Sources de données monde — World Twin

Sources vérifiées gratuites le 17 octobre 2026. Branchement : Open-Meteo (ERA5, dix bassins monde) et NASA FIRMS (dix boîtes monde) sont branchées (17/10/2026, vague P2) ; FAOSTAT est branchée pour la France ; l'atlas des gisements multi-pays est livré en v0.5 (17/10/2026, atlas-gisements-monde.md et engine/atlas_gisements.py) avec des sources publiques additionnelles par hub ; les fiches pays réglementaires sont livrées en v0.6 (17/10/2026, fiches-pays-reglementation.md et engine/fiches_reglementation.py) ; le croisement GEOGLAM est livré en v0.7 (17/10/2026, croisement-geoglam.md et engine/geoglam.py) ; le FIRMS historique multi-saison est livré en v0.8 (18/10/2026, firms-historique.md et engine/firms_histo.py) ; l'extraction bulk FAOSTAT multi-pays est livrée en v0.9 (18/10/2026, gisements-faostat-bulk.md et engine/faostat_bulk.py) ; l'atlas des biomasses monde est livré en v1.0 (18/10/2026, atlas-biomasses-monde.md et engine/atlas_biomasses_monde.py) avec les 52 intrants du master placés sur le globe et une branche météo temps réelle Open-Meteo (52 points, cache horaire non versionné) ; l'atlas des biomasses locales par pays est livré en v1.1 (18/10/2026, atlas-biomasses-pays.md et engine/atlas_biomasses_pays.py) avec les 67 intrants locaux des 18 pays, productions ancrées sur le bulk FAOSTAT 2024 ; l'atlas des vignobles du monde est livré en v1.2 (18/10/2026, atlas-vignobles-monde.md et engine/atlas_vignobles_monde.py) avec les 32 intrants viticoles des 22 pays, productions et surfaces ancrées sur le bulk FAOSTAT 2024 (item Grapes) ; toute valeur non sourcée est ILLUSTRATION clairement étiquetée.

## Sources

### FAOSTAT (Organisation des Nations unies pour l'alimentation et l'agriculture)

- Contenu : production agricole et résidus par pays, brûlage des résidus (méthode IPCC), ~245 pays, historique pluriannuel.
- Accès : libre, portail FAOSTAT et téléchargements en masse (bulk) ; la nouvelle API faostatservices.fao.org exige une clé — passer par le bulk, gratuit (constaté le 17/10/2026). Licence CC BY 4.0 (politique FAO d'open data licensing) ; le bulk normalisé « Production_Crops_Livestock_E » (environ 34 Mo, mise à jour du 31/12/2025) porte la série 1961-2024 (constaté le 18/10/2026).
- Statut : branchée pour la France depuis la v0.1 (17/10/2026) ; V0.9 (18/10/2026) : extraction bulk MULTI-PAYS branchée — six pays, six cultures, séries 2019-2024 mises en cache (cache-faostat-bulk/, jamais versionné), gisements nationaux documentaires dérivés, croisement avec les ancres régionales de l'atlas v0.5 (gisements-faostat-bulk.md et engine/faostat_bulk.py).
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
3. Fiches pays réglementaires : brûlage encadré, à sourcer document par document. FAIT en v0.6 (17/10/2026) : fiches-pays-reglementation.md et engine/fiches_reglementation.py — France L.541-21-1, Suisse OPair art. 26a, Italie D.Lgs 152/2006 + LR Puglia 38/2016, Espagne Ley 7/2022 art. 27.3, Argentine Ley 26.562, Maroc Loi 28-00 (la référence « loi 62.25 » du plan initial n'a pas été retrouvée et est écartée). Les textes légis sont publics : Légifrance/AIDA, Infoleg, SGG Maroc, DOE Estrémadure, bulletins officiels régionaux.
4. FIRMS historique : cartographie multi-saison des dix bassins, au-delà du jour courant. FAIT en v0.8 (18/10/2026) : firms-historique.md et engine/firms_histo.py — cinq saisons complètes 2021-2025 par résumés annuels par pays (sans MAP_KEY), VIIRS S-NPP 375 m par défaut (viirs-jpss1 et modis paramétrables), filtre de quasi-permanence des sources fixes, verdicts mensuels, croisement des fenêtres monde.py (monde.py inchangé, doctrine À SOURCER respectée).
5. Remplacement progressif des ILLUSTRATIONS du cahier pilote monde par les valeurs sourcées, avec traçabilité source et date.

## Limites honnêtes

- Aucune source ne remplace la qualification machine : FAT/SAT sur acier réel uniquement.
- Les données agrégées au niveau pays masquent les réalités régionales : chaque extrapolation est documentée.
- Les volumes téléchargés vivent hors du dépôt (espace de travail chiffré) ; seules les spécifications et les agrégations non sensibles sont versionnées.
