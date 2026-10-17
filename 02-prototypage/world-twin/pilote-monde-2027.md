# World Twin — cahier pilote monde 2027 (P2)

Carré d'Or, LatAm, Al-Atlas : le trio Nomad v1 « as if in operation » sur trois continents et deux hémisphères, dans le même simulateur que le pilote France. Ce cahier fixe la grammaire des hubs P2 ; toute valeur y est ILLUSTRATION, non calibrée, en attente de sourçage FAOSTAT / GEOGLAM / fiches pays.

Statut : v0.4 — poussé le 17/10/2026 (P2 démarrée trente mois avant la feuille de route P2 du README).

## Règles absolues (inchangées)

- Tout résultat est étiqueté SYNTHÉTIQUE. Devant un investisseur, on dit simulation, toujours.
- Aucune valeur calibrée, clé ou secret dans ce dossier.
- La simulation éprouve la logique, jamais la physique. La qualification reste le monopole des FAT/SAT sur machines réelles.

## Les sept hubs de la flotte P2

| Hub | Pays | Région | Trios | Biomasses (fenêtres) | Bassins données |
| --- | --- | --- | --- | --- | --- |
| fr-rhone | France | pilote v0 (Rhône, Camargue, Sud-Ouest, Périgord) | 1 | sarments-vigne (jan-avr), marc-raisin (sept-nov), mais-rdm (oct-déc), paille-riz (oct-déc), coques-noix (oct-févr) | 4 bassins pilote |
| ch-leman | Suisse | Lavaux-Léman (Carré d'Or) | 1 | sarments-vigne (jan-mars), marc-raisin (oct-nov) | suisse-leman |
| it-puglia | Italie | Puglia-Tavoliere (Foggia) | 1 | grignons-olive (nov-janv), sarments-vigne (févr-mars) | italie-puglia |
| es-extremadura | Espagne | Estrémadure | 1 | grignons-olive (nov-févr), sarments-vigne (mars-avr) | espagne-extremadure |
| ar-cuyo | Argentine | Cuyo-Mendoza (LatAm) | 1 | restos-poda (juin-août) — hémisphère Sud : la taille d'hiver austral | argentine-cuyo |
| ar-misiones | Argentine | Misiones (LatAm) | 1 | yerba-mate (avr-juin, sept-nov) — hémisphère Sud | argentine-misiones |
| ma-atlas | Maroc | Al-Atlas (Meknès) | 1 | grignons-olive (déc-févr) | maroc-atlas |

Paramètres de flotte identiques au figeage v0.2 : 2 opérateurs tournants par trio (hub régional de 3 à 5 trios), MTBF 720 h, MTTR 8 h, 2 lots/jour, mois de 28 jours.

## Saisonnalité et hémisphère Sud

- Les mois de maintenance saisonnière sont DÉDUITS des fenêtres : un mois sans biomasse active est un mois de maintenance. Pour fr-rhone, la déduction redonne exactement mai-août, le figeage du pilote — la compatibilité arrière est un test, pas une coïncidence.
- Hémisphère Sud : ar-cuyo (taille de vigne en hiver austral, juin-août) et ar-misiones (yerba maté, récoltes d'automne et de printemps austral) prouvent que la grammaire suit le calendrier du gisement, pas celui du simulateur.
- Graines déterministes : fr-rhone 42 (pilote inchangé), puis 1042, 2042, 3042, 4042, 5042, 6042 — convention lisible, un run se reproduit à l'identique.

## Données réelles branchées (17/10/2026)

- Météo : Open-Meteo ERA5, agrégations mensuelles réelles des dix bassins (janv. Mendoza 25,7 °C contre 2,6 °C au Léman : l'hiver austral est dedans). Cache versionné : cache-meteo/agregats-mensuels.json ; convention jours de pluie ≥ 0,2 mm sur la fenêtre 2025-10-01 → 2026-10-10 UTC.
- Feux : NASA FIRMS, dix boîtes géographiques (une par bassin). Avec une MAP_KEY locale : pain points réels par hub, priorisation mondiale des bassins par brûlage actif du jour. Sans clé : repli synthétique déterministe, aucune erreur.
- Hors périmètre du jour : gisements FAOSTAT multi-pays (à extraire comme pour la France), réglementation du brûlage par pays (Ley 26.562 argentine, interdictions locales), fiches pays commerciales — toutes restent ILLUSTRATION jusqu'à sourçage documenté.

## Lancement

```
python3 engine/simulateur.py                # flotte monde (7 hubs, 2 016 lots)
python3 engine/simulateur.py fr-rhone        # un hub seul (réplique v0.3)
python3 engine/monte_carlo.py 1000 200 monde # milliers de runs, agrégats par hub
```

## Limites honnêtes

- Les charges, humidités et gisements des hubs non français sont ILLUSTRATION ; seule la saisonnalité (fenêtres) et la météo (ERA5) sont sourcées.
- Un trio par hub en P2 ; le modèle tournant 3-5 trios par hub est simulé en monte_carlo, pas en run simple.
- La géographie des bassins (boîtes FIRMS, points ERA5) est une approximation de la région, pas un cadastre.
