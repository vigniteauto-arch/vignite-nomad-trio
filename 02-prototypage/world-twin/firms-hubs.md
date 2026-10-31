# Boîtes FIRMS des hubs généralisés — V1.8 (31/10/2026)

## Statut

V1.8 actée le 31/10/2026 sur « go » de Manu Moineau : chaque hub généralisé de
la flotte (81 hubs, 32 pays) possède désormais sa zone NASA FIRMS (Fire
Information for Resource Management System). Avec la MAP_KEY locale, les pain
points par hub passent du repli synthétique aux feux actifs RÉELS du jour.
Suite directe de la vague V1.7 (gisements FAOSTAT des hubs généralisés —
Food and Agriculture Organization of the United Nations, fenêtre 2020-2024,
208 trios).

## Ce que la clé active

La MAP_KEY est gratuite (firms.modaps.eosdis.nasa.gov/api/map_key/) et déjà
obtenue le 17/10/2026. Elle vit dans deux endroits, jamais dans le dépôt :

- en local : le fichier firms.env à la racine du dossier world-twin (copier
  engine/firms.env.example, coller la clé, le motif *.env du .gitignore
  l'exclut du dépôt) ou la variable d'environnement FIRMS_MAP_KEY —
- en intégration continue : le secret FIRMS_MAP_KEY du workflow FIRMS NRT
  quotidien (Continuous Integration, GitHub Actions).

Trois circuits deviennent réels avec la clé :

1. Le moteur de scénarios (engine/scenario.py) : pour chaque cellule simulée
   sur un hub, les pain points deviennent les détections réelles du jour sur
   la zone du hub — étiquette DONNÉES RÉELLES (NASA FIRMS). Sans clé : repli
   synthétique déterministe, étiquette SYNTHÉTIQUE, inchangé.
2. Le relevé quotidien (engine/firms_nrt.py) : 91 zones — 10 bassins P2 et
   81 hubs généralisés — une requête API par zone et par jour.
3. La priorisation (engine/firms.py, priorite_hubs) : classement des zones
   par FRP (Fire Radiative Power, mégawatts) décroissant.

## Méthode

- Capteur : VIIRS_NOAA20_NRT (Visible Infrared Imaging Radiometer Suite,
  satellite NOAA-20 — National Oceanic and Atmospheric Administration,
  Near Real Time). La NASA (National Aeronautics and Space Administration)
  cesse la livraison Suomi NPP le 01/11/2026 : NOAA-20 est la mission de
  référence qui poursuit la série.
- Boîte de requête : ±1.0° latitude / ±1.5° longitude autour du centre du
  cluster du hub (même convention que les dix bassins P2). Le centre et la
  boîte sont calculés par engine/flotte_monde.py v1.8 et enregistrés au
  runtime dans le registre de engine/firms.py.
- Cache : une seule requête réseau par zone et par jour de run, mémoïsée en
  mémoire et écrite dans cache-firms/ (jamais versionné).
- Chaîne FRP → FRE → biomasse → émissions (engine/fre_conversions.py,
  v1.4) : FRE extrapolée sur 24 h, biomasse via le coefficient 0,368 kg/MJ
  (Wooster et al. 2005), émissions via les facteurs IPCC 2006 Vol. 4 Tab. 2.5
  (résidus agricoles — Intergovernmental Panel on Climate Change), GWP AR6.
  Toutes les valeurs dérivées restent des ESTIMATIONS DOCUMENTAIRES
  ILLUSTRATION.
- Limite officielle de l'API FIRMS : 5 000 transactions par intervalle de
  10 minutes. Le circuit complet consomme 91 requêtes par jour (1,8 % du
  quota par intervalle), marge massive.

## Alignement des tirages — comparabilité stricte clé / sans clé (scenario v0.6)

Le générateur pseudo-aléatoire du moteur tire DEUX valeurs par cellule pour
les pain points, AVANT le branchement FIRMS, dans le même ordre dans les deux
chemins. Conséquence : le flux pseudo-aléatoire est strictement identique
avec ou sans clé — les lots, les fautes et la disponibilité ne bougent JAMAIS.
Les pain points réels n'altèrent que la narration (événements firms du run).
La série historique Monte Carlo (disponibilité flotte 99,7 %) reste
rigoureusement comparable. Sans cet alignement, activer la clé aurait
décalé le flux et fait diverger les chiffres figés : c'est le correctif clé
de la vague V1.8.

## Étiquettes et doctrine

- Un run complet reste étiqueté SYNTHÉTIQUE (registre de développement,
  jamais le registre Merkle de production) : les pain points FIRMS y
  apparaissent comme des événements ponctuels étiquetés DONNÉES RÉELLES
  (NASA FIRMS), données brutes du domaine public.
- Devant un investisseur : la flotte reste une simulation, les feux sont
  réels. On ne mélange jamais les deux registres dans une phrase.
- La MAP_KEY est un secret : jamais versionnée, jamais dans la base de
  connaissance, jamais partagée. Le relevé quotidien et les caches ne sont
  jamais versionnés.
- La détection ne qualifie rien : feux de moins de 375 m sous-détectés,
  nuages et panaches masquants, incertitude d'un facteur environ 2 sur la
  biomasse dérivée. La qualification reste le monopole des FAT/SAT sur
  machines réelles (Factory Acceptance Test / Site Acceptance Test).

## Lancement

    python3 engine/flotte_monde.py sommaire        # composition, ligne pain points V1.8
    python3 engine/flotte_monde.py run gen-bresil-1 # un hub — événements firms réels avec clé
    python3 engine/firms_nrt.py                     # relevé des 91 zones (sorties-firms-nrt/)

Sans firms.env ni FIRMS_MAP_KEY : tous les circuits retombent proprement sur
le repli synthétique, le workflow reste vert, l'écart est visible dans le
résumé quotidien.

## Ce que la V1.8 ne fait pas (reliquats assumés)

- Les fenêtres FIRMS historiques par hub (saisonnalité pluriannuelle du
  brûlage par zone, sur le modèle de firms_histo.py) restent À L'ÉTUDE — le
  relevé V1.8 est un cliché du jour, pas une climatologie.
- La dimension réglementaire du brûlage par pays reste celle des fiches
  réglementation (v0.6), étiquetée À VÉRIFIER pour plusieurs juridictions.
- L'attribution d'un feu à une biomasse précise (chaumes contre défriche)
  n'est pas automatisée : la lecture World Ops reste humaine.
