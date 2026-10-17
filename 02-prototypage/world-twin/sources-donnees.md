# Sources de données monde — World Twin

Sources vérifiées gratuites le 17 octobre 2026. Branchement : Open-Meteo (ERA5, dix bassins monde) et NASA FIRMS (dix boîtes monde) sont branchées (17/10/2026, vague P2) ; FAOSTAT est branchée pour la France ; l'atlas des gisements multi-pays est livré en v0.5 (17/10/2026, atlas-gisements-monde.md et engine/atlas_gisements.py) avec des sources publiques additionnelles par hub ; GEOGLAM reste planifiée ; toute valeur non sourcée est ILLUSTRATION clairement étiquetée.

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

- Contenu : calendriers culturaux et conditions de récolte sous-nationales.
- Accès : libre.
- Rôle : couche 1 — saisonnalité fine par région.
- Limite : couverture inégale selon les pays.

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
2. Croisement GEOGLAM : validation des fenêtres culturales des hubs, hémisphère Sud inclus.
3. Fiches pays réglementaires : brûlage encadré (Ley 26.562 argentine, interdictions locales Espagne/Italie, cadre Maroc loi 62.25), à sourcer document par document.
4. FIRMS historique : cartographie multi-saison des dix bassins, au-delà du jour courant.
5. Remplacement progressif des ILLUSTRATIONS du cahier pilote monde par les valeurs sourcées, avec traçabilité source et date.

## Limites honnêtes

- Aucune source ne remplace la qualification machine : FAT/SAT sur acier réel uniquement.
- Les données agrégées au niveau pays masquent les réalités régionales : chaque extrapolation est documentée.
- Les volumes téléchargés vivent hors du dépôt (espace de travail chiffré) ; seules les spécifications et les agrégations non sensibles sont versionnées.
