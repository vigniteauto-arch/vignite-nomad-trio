# Consolidation Al-Atlas (Maroc) — World Twin V2.3 (14/11/2026)

Consolidation de toutes les couches World Twin pour la zone Maroc de la
filiale Vignite Al-Atlas, établie par la vague V2.3 du 14/11/2026 puis
complétée par le raccord V2.3.1 (mêmes date et doctrine : le bassin
pilote ma-atlas est désormais raccordé aux couches CaO P2.9 et sourcing
P3, cf. sections 2 et 3). Préparé, rien poussé sans double-clic de Manu
Moineau. Toute la flotte décrite est simulée : étiquette SYNTHÉTIQUE,
registre de DÉVELOPPEMENT, jamais le registre Merkle de production.
Devant investisseurs : toujours dire « simulation », jamais exploitation
réelle. Aucune valeur calibrée, aucune clé, aucun jeton dans ce fichier
(doctrine PI, 00-gouvernance/GARDE_FOUS_PI.md).

## 1. Flotte simulée Maroc (4 trios SYNTHÉTIQUES)

| Hub | Région | Biomasses | Fenêtre | Trios |
|---|---|---|---|---|
| ma-atlas (P2) | Al-Atlas (Meknès) | grignons d'olive | décembre-février | 3 |
| gen-maroc-1 (V2.3) | Chaouia (centre 33,47 / −6,06, entre Casablanca et Settat) | paille de blé, paille d'orge, sarments de vigne | selon atlas v1.3 | 3 |

- ma-atlas : bassin P2 du cahier pilote, trio ma-atlas-trio-1, graine
  6042, humidité des grignons 35 à 60 %. Raccord V2.3.1 : le hub porte
  3 trios P2 (MA-HUB-TRIO-1 à 3, convention data/carte-monde.json),
  figés dans data/parametres-trios.json (graines 6042 à 6044).
- gen-maroc-1 : hub généralisé de la flotte V2.3 (engine/flotte_monde.py),
  3 points atlas, gisement 2,5 à 12,0 Mt/an (moyenne 5,1 Mt/an),
  étiqueté SOURCÉ (FAOSTAT 2020-2024, snapshot v18) + ratios
  ILLUSTRATION.

## 2. Socle minéral CaO (P2.9, data/cao-hubs-public.json)

- Raccord V2.3.1 : ma-atlas rejoint la couche comme hub pilote (3 trios,
  besoin 1 746 t CO2/an). Le prorata national Maroc passe de 3 à 6 trios
  au dénominateur : capacité proratisée 32 560 t/an pour chaque hub
  marocain, ratio 18,65, AUTONOME.
- gen-maroc-1 : besoin 1 746 t CO2/an (3 trios × 582), capacité
  proratisée 32 560 t/an après raccord (65 120 t/an de réactifs
  nationaux pour tout le Maroc) — ratio 18,65 AUTONOME, écart V2.3 →
  V2.3.1 (37,3 → 18,65) documenté dans le verifier : le statut ne
  change pas, seule la part nationale par trio bouge.
- Chaîne documentaire : USGS Mineral Commodity Summaries 2026 (ciment,
  fonte/acier), FAOSTAT bois rond 2024 (Maroc 6 504 769 m³/an, témoin
  exact du snapshot), population 2023 Our World in Data, ratios
  ILLUSTRATION (poussière de fours à ciment, laitier, cendres).
- Coûts et plans d'achat : PRIVÉS, jamais versionnés
  (data/cao-hubs.json, local uniquement).

## 3. Sourcing réel P3 (data/sourcing-p3-public.json)

- Raccord V2.3.1 — ma-atlas (centre 33,89 / −5,55, convention
  data/carte-monde.json) : AUTONOME au rayon standard de 50 km ; deux
  cimenteries retenues (Global Cement and Concrete Tracker, Global
  Energy Monitor, données publiques) : cimenterie de Meknès à 5,5 km
  (capacité 5 670 t CO2/an) et Aïn Chkef à 40,4 km (3 888 t CO2/an) ;
  ratio 5,47 ; aucune aciérie à haut fourneau ni unité bois dans le
  rayon. Le bassin pilote est assis sur la cimenterie de Meknès même.
- gen-maroc-1 : AUTONOME au rayon étendu de 100 km ; deux cimenteries
  retenues à 71,6 et 94,7 km ; site le plus proche 71,6 km ; aucune
  aciérie à haut fourneau ni unité bois dans le rayon.
- Réactif dominant pour le Maroc : poussière de fours à ciment (CKD,
  Cement Kiln Dust).
- Coûts : PRIVÉS, jamais versionnés (data/sourcing-p3.json, local).

## 4. Cadre réglementaire (fiches_reglementation.py, consulté le
31/10/2026)

- Loi n° 13-03 relative à la lutte contre la pollution de l'air (dahir
  n° 1-03-61 du 12/05/2003, Bulletin officiel n° 5118) ; décret
  n° 2-09-286 du 08/12/2009 modifié par le décret n° 2-23-244 du
  07/03/2023 (ministère de la Transition énergétique et du Développement
  durable).
- Loi n° 28-00 relative à la gestion des déchets (dahir n° 1-06-153 du
  22/11/2006, Bulletin officiel n° 5480).
- Constat : aucune norme nationale dédiée au brûlage agricole, aucune
  procédure d'autorisation identifiée ; la conformité s'apprécie au
  regard des lois 13-03 et 28-00 et du plan directeur régional des
  déchets.
- Angle Vignite : le vide relatif est un piège et une opportunité ;
  conformité par anticipation, positionnement en standard de filière ;
  jamais couvrir un brûlage, toujours valoriser le procédé sans feu à
  l'air libre.

## 5. Abonnements et veille (registre-abonnements V2.1)

- CAMS (Copernicus Atmosphere Monitoring Service) Aerosol Alerts,
  abonnement Dust Haouz ACTIF (boîte 30,44 à 33,20 / −10,63 à −5,76,
  paramètre od550dust).
- NASA FIRMS (Fire Information for Resource Management System) API sur
  la zone maroc-atlas (MAP_KEY locale, jamais versionnée).
- WaPOR v3 (Afrique et Proche-Orient, sans jeton) ; EMIT L3 ASA scène
  2420510_006 (Atlas) ; DMN Maroc (vigilance.ma) ; GDACS en filet
  mondial.
- La vague V2.3 n'a activé AUCUN nouvel abonnement externe.

## 6. Économie simulée

Aucune donnée économique dans ce dépôt (doctrine PI). Le compte de
résultat simulé (P&L) des hubs marocains vit dans les fichiers PRIVÉS
locaux correspondants (cao-hubs.json, sourcing-p3.json), jamais
versionnés. Toute communication : simulation SYNTHÉTIQUE.

## 7. Actions proposées (à décision de Manu)

1. FAIT (V2.3.1, 14/11/2026) : le bassin pilote ma-atlas (Meknès) est
   raccordé aux couches CaO P2.9 (ratio 18,65 AUTONOME) et sourcing P3
   (AUTONOME, cimenterie de Meknès à 5,5 km) ; il est figé dans
   data/parametres-trios.json (3 trios, graines 6042 à 6044).
2. Croiser avec la stratégie de la filiale Vignite Al-Atlas (base de
   connaissance, réserve de nom Fahm/Fahima) pour les partenaires
   institutionnels.
3. Aucune sollicitation externe sans validation explicite : priorité de
   l'entreprise, levée d'amorçage 500 k€.
