# Sources de données monde — World Twin

Sources vérifiées gratuites le 17 octobre 2026. Branchement : Open-Meteo (ERA5, dix bassins monde) et NASA FIRMS (dix boîtes monde) sont branchées (17/10/2026, vague P2) ; FAOSTAT est branchée pour la France ; l'atlas des gisements multi-pays est livré en v0.5 (17/10/2026, atlas-gisements-monde.md et engine/atlas_gisements.py) avec des sources publiques additionnelles par hub ; les fiches pays réglementaires sont livrées en v0.6 (17/10/2026, fiches-pays-reglementation.md et engine/fiches_reglementation.py) ; le croisement GEOGLAM est livré en v0.7 (17/10/2026, croisement-geoglam.md et engine/geoglam.py) ; toute valeur non sourcée est ILLUSTRATION clairement étiquetée.

## Sources

### FAOSTAT (Organisation des Nations unies pour l'alimentation et l'agriculture)

- Contenu : production agricole et résidus par pays, brûlage des résidus (méthode IPCC), ~245 pays, historique pluriannuel.
- Accès : libre, portail FAOSTAT et téléchargements en masse (bulk) ; la nouvelle API faostatservices.fao.org exige une clé — passer par le bulk, gratuit (constaté le 17/10/2026).
- Rôle : couche 1 — gisements par pays et biomasse, réglementation du brûlage.
- Limite : agrégation au niveau pays ; la maille régionale demande des extrapolations documentées.

### NASA FIRMS (Fire Information for Resource Management System)

- Contenu : feux actifs, points GPS horodatés, quasi temps réel et historique.
- Accès : API exigeant une MAP_KEY gratuite sur inscription (mise à jour du 17/10/2026 ; l'inscription prend environ cinq minutes).
- Statut : branchée et testée le 17/10/2026 — détections réelles intégrées au moteur de scénarios (pain points) et à la priorisation des hubs ; vague P2 : dix boîtes géographiques monde (une par bassin, Carré d'Or à Al-Atlas) ; MAP_KEY dans firms.env local, jamais versionné (motif *.env).
- Rôle : couche 1 — pain point brûlage, ciblage des zones à épargner, priorisation des hubs.
- Limite : détection des feux, pas de leur cause ; croiser avec les statistiques nationales ; cache local d'un jour pour préserver le quota de transactions API.

### Open-Meteo

- Contenu : météo historique (réanalyse ERA5, 1940 à aujourd'hui) et prévisions, anywhere on Earth.
- Accès : API gratuite sans clé, fair use ~10 000 requêtes/jour.
- Statut : branchée le 17/10/2026 — agrégations mensuelles réelles versionnées dans cache-meteo/ ; vague P2 : dix bassins (France ×4, Suisse Léman, Italie Puglia, Espagne Estrémadure, Argentine Cuyo, Argentine Misiones, Maroc Al-Atlas) ; convention jours de pluie ≥ 0,2 mm, fenêtre 2025-10-01 → 2026-10-10 UTC.
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

1. FAOSTAT multi-pays : production et résidus des biomasses des hubs (Suisse, Italie, Espagne, Argentine, Maroc), même méthode que l'extraction France. FAIT en v0.5 (17/10/2026) sous forme d'atlas de données publiques sourcées par hub (atlas-gisements-monde.md) ; l'extraction bulk FAOSTAT proprement dite reste à faire pour affiner.
2. Croisement GEOGLAM : validation des fenêtres culturales des hubs, hémisphère Sud inclus. FAIT en v0.7 (17/10/2026) : croisement-geoglam.md et engine/geoglam.py — calendriers sous-nationaux des 7 hubs sourcés et étiquetés, fenêtres mais-rdm et paille-riz validées, fenêtres candidates pailles céréalières À SOURCER (gisement, ratio, volumes avant toute ingestion dans monde.py).
3. Fiches pays réglementaires : brûlage encadré, à sourcer document par document. FAIT en v0.6 (17/10/2026) : fiches-pays-reglementation.md et engine/fiches_reglementation.py — France L.541-21-1, Suisse OPair art. 26a, Italie D.Lgs 152/2006 + LR Puglia 38/2016, Espagne Ley 7/2022 art. 27.3, Argentine Ley 26.562, Maroc Loi 28-00 (la référence « loi 62.25 » du plan initial n'a pas été retrouvée et est écartée). Les textes légis sont publics : Légifrance/AIDA, Infoleg, SGG Maroc, DOE Estrémadure, bulletins officiels régionaux.
4. FIRMS historique : cartographie multi-saison des dix bassins, au-delà du jour courant.
5. Remplacement progressif des ILLUSTRATIONS du cahier pilote monde par les valeurs sourcées, avec traçabilité source et date.

## Limites honnêtes

- Aucune source ne remplace la qualification machine : FAT/SAT sur acier réel uniquement.
- Les données agrégées au niveau pays masquent les réalités régionales : chaque extrapolation est documentée.
- Les volumes téléchargés vivent hors du dépôt (espace de travail chiffré) ; seules les spécifications et les agrégations non sensibles sont versionnées.
