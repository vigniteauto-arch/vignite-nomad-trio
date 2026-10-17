# Sources de données monde — World Twin

Sources vérifiées gratuites le 17 octobre 2026. Leur branchement est planifié en P1 ; en P0, le simulateur fonctionne sur hypothèses ILLUSTRATION clairement étiquetées.

## Sources

### FAOSTAT (Organisation des Nations unies pour l'alimentation et l'agriculture)

- Contenu : production agricole et résidus par pays, brûlage des résidus (méthode IPCC), ~245 pays, historique pluriannuel.
- Accès : libre, portail FAOSTAT et téléchargements en masse (bulk) ; la nouvelle API faostatservices.fao.org exige une clé — passer par le bulk, gratuit (constaté le 17/10/2026).
- Rôle : couche 1 — gisements par pays et biomasse, réglementation du brûlage.
- Limite : agrégation au niveau pays ; la maille régionale demande des extrapolations documentées.

### NASA FIRMS (Fire Information for Resource Management System)

- Contenu : feux actifs, points GPS horodatés, quasi temps réel et historique.
- Accès : API exigeant une MAP_KEY gratuite sur inscription (mise à jour du 17/10/2026 ; l'inscription prend environ cinq minutes).
- Rôle : couche 1 — pain point brûlage, ciblage des zones à épargner, priorisation des hubs.
- Limite : détection des feux, pas de leur cause ; croiser avec les statistiques nationales.

### Open-Meteo

- Contenu : météo historique (réanalyse ERA5, 1940 à aujourd'hui) et prévisions, anywhere on Earth.
- Accès : API gratuite sans clé, fair use ~10 000 requêtes/jour.
- Statut : branchée le 17/10/2026 — agrégations mensuelles réelles des quatre bassins pilotes versionnées dans cache-meteo/.
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

## Plan de branchement P1

1. Téléchargement FAOSTAT France : production et résidus des cinq biomasses du pilote.
2. Croisement GEOGLAM : validation des fenêtres culturales du cahier pilote.
3. Cache Open-Meteo : historique météo 2020-2026 des bassins pilotes.
4. FIRMS : cartographie des feux sur les bassins pilotes, dernière saison.
5. Remplacement des ILLUSTRATIONS du cahier pilote par les valeurs sourcées, avec traçabilité source et date.

## Limites honnêtes

- Aucune source ne remplace la qualification machine : FAT/SAT sur acier réel uniquement.
- Les données agrégées au niveau pays masquent les réalités régionales : chaque extrapolation est documentée.
- Les volumes téléchargés vivent hors du dépôt (espace de travail chiffré) ; seules les spécifications et les agrégations non sensibles sont versionnées.
