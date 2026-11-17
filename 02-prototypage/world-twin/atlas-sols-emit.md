# Atlas des sols — NASA EMIT (v1.7, 17/11/2026 au soir ; v1.6 : 17/11/2026 ; V1.5 : 27/10/2026)

Socle « Soil Sciences » de la couche 1 du World Twin : minéralogie des sols des bassins de la flotte par les données publiques NASA EMIT, pour la lecture agronomique des intrants (rétention d'eau, CEC — Capacité d'Échange Cationique, dosage biochar) et l'affinage documentaire de l'atlas des biomasses.

EMIT — Earth Surface Mineral Dust Source Investigation : spectromètre imageur embarqué sur la station spatiale internationale (ISS — International Space Station), 380-2500 nm, cartographie de la minéralogie des surfaces affleurantes.

## Produits et provenance (SOURCÉ)

- EMIT L2B MIN (EMITL2BMIN) : « Estimated Mineral Identification and Band Depth and Uncertainty », maille 60 m, scène par scène. Trois granules versionnés au dépôt, dossier `data/emit/` :
  - `EMIT_L2B_MIN_001_20230124T153032_2302410_038.nc` — scène du 24/01/2023 ;
  - `EMIT_L2B_MIN_001_20230804T113000_2321608_018.nc` — scène du 04/08/2023 ;
  - `EMIT_L2B_MIN_001_20240723T152209_2420510_006.nc` — scène du 23/07/2024 ;
  - cinq scènes L2B complètes (v1.7, vague Earthdata du 17/11/2026, compte nominatif NASA) : fichiers locaux dans `data/emit/`, hors Git en attendant la décision de versionnement, tailles et empreintes SHA-512 de référence NASA (fiches UMM du catalogue CMR) vérifiées à l'octet près :
    - `EMIT_L2B_MIN_001_20260724T144642_2620510_011.nc` — Périgord, 24/07/2026, 0 % de nuages ;
    - `EMIT_L2B_MIN_001_20260724T144630_2620510_010.nc` — Sud-Ouest, 24/07/2026, 0 % de nuages ;
    - `EMIT_L2B_MIN_001_20260728T131411_2620909_004.nc` — Léman suisse, 28/07/2026, 3 % de nuages ;
    - `EMIT_L2B_MIN_001_20250806T083943_2521806_009.nc` — Pouilles, 06/08/2025, 2 % de nuages ;
    - `EMIT_L2B_MIN_001_20260714T172731_2619512_016.nc` — Misiones, 14/07/2026, 2 % de nuages.
- EMIT L3 ASA (EMITL3ASA) : « Aggregated Mineral Spectral Abundance and Uncertainty », agrégation mondiale au demi-degré — la couche directement exploitable pour les dix bassins de la flotte. Un fichier versionné : `data/emit/EMIT_L3_ASA_002.zip`.
- Diffusion : NASA LP DAAC (Land Processes Distributed Active Archive Center), Earthdata, données publiques. Fichiers d'origine : uploads du 24/10/2026 (racine du dépôt), déplacés dans `data/emit/` par la vague v1.5.

## Règles absolues (inchangées)

- Données publiques NASA uniquement : aucun paramètre VDE (Vignite Decision Engine), aucune valeur calibrée, aucune clé.
- Les fractions minérales extraites sont SOURCÉES (NASA EMIT) ; toute lecture agronomique est ILLUSTRATION documentaire, jamais une prescription agronomique, jamais un calibrage.
- Les fichiers réassemblés, extractions et sorties du L3 vivent dans `cache-sols/`, jamais versionnés.
- La simulation éprouve la logique, jamais la physique. La qualification reste le monopole des FAT/SAT (Factory/Shop Acceptance Tests) sur machines réelles.

## Workflow machine (`engine/atlas_sols_emit.py`, bibliothèque standard)

1. `inventaire` — tailles, empreintes md5 et complétude des granules versionnés (parts et zip) ; pour les scènes complètes (v1.7), taille et empreinte SHA-512 confrontées à la référence NASA. Écrit `cache-sols/inventaire.json`.
2. `reassembler GRANULE` — concatène les `.partN` en `.nc` dans `cache-sols/` (jamais versionné). Cartouches : `2302410_038`, `2321608_018`, `2420510_006` ; les cinq scènes complètes n'ont rien à réassembler.
3. `extraire [SCÈNE|CARTOUCHE]` — empreinte géographique et variables des granules L2B : cartouches lues depuis `cache-sols/` (réassemblées), scènes complètes lues directement depuis `data/emit/` après contrôle de l'empreinte SHA-512 contre la référence NASA (v1.7). Requiert localement un lecteur HDF5 (`py -m pip install h5py`) ; sans lecteur, arrêt propre avec consigne — les autres modes restent disponibles. Correctif v1.7 : le parcours des groupes itérait sur les noms du fichier au lieu des objets (bug « 'str' object has no attribute 'keys' », constaté en atelier le 17/11/2026 sur les trois cartouches réassemblées, chemin jamais exercé avant).
4. `croiser` — rattachement des scènes L2B aux dix bassins de la flotte (mêmes boîtes géographiques que la couche FIRMS : approximation de la région, pas un cadastre). Écrit `cache-sols/croisement.json`.
5. `sommaire [BASSIN]` — sommaire de la couche sols, ou fiche d'un bassin.
6. `l3-bassins` — v1.6 : décompresse `EMIT_L3_ASA_002.zip` dans `cache-sols/` (jamais versionné), lit la grille mondiale au demi-degré et échantillonne les boîtes des dix bassins (moyenne des mailles valides, nodata exclues), dominant par minéral et rapport argiles 2:1 sur kaolinite par bassin. Écrit `cache-sols/l3-bassins.json`. Lecteur : h5py s'il est présent, sinon lecteur HDF5 minimal embarqué (bibliothèque standard, jeux contigus du L3 — les granules L2B à chunks compressés restent hors de sa portée) ; sans granule, repli sur la grille documentaire `GRILLE_L3_DOCUMENTAIRE` étiquetée ILLUSTRATION.

## Groupes minéraux et lecture agronomique (ILLUSTRATION)

| Minéral | Famille | CEC indicative | Lecture (ILLUSTRATION) |
| --- | --- | --- | --- |
| Kaolinite | argile 1:1 | faible (3-15 cmol+/kg) | faible rétention — le biochar y apporte le gain de rétention le plus visible |
| Smectite | argile 2:1 expansive | élevée (80-150 cmol+/kg) | vertisols — dosage prudent, viser la structure |
| Illite, muscovite | 2:1 | moyenne (20-40 cmol+/kg) | sols équilibrés — biochar en entretien |
| Chlorite | 2:1:1 | moyenne (10-40 cmol+/kg) | drainage variable |
| Vermiculite | 2:1 expansive | très élevée (100-150 cmol+/kg) | forte rétention — biochar en appoint |
| Calcite, dolomite | carbonates | — | sols calcaires, pH tamponné — le biochar n'y relève pas le pH |
| Gypsum | sulfate | — | risque de salinité et sodicité — drainage à surveiller avant amendment |
| Hématite, goethite | oxydes de fer | faible | sols rouges ou jaunes, sorption du phosphore, bonne agrégation |
| Quartz | oxyde | nulle | texture sableuse, drainage rapide |

Indice dérivé (ILLUSTRATION) : rapport argiles 2:1 sur kaolinite — un bassin smectitique rétient naturellement eau et cations quand un bassin kaolinitique en manque : la même tonne de biochar n'y fait pas le même travail, l'indice oriente la lecture documentaire des fiches intrants.

## Rôle dans l'architecture

- Couche 1 (données monde) : la minéralogie rejoint la météo (ERA5), le brûlage (FIRMS) et les calendriers (GEOGLAM) comme quatrième observable public par bassin — le mode `l3-bassins` en donne la lecture mondiale au demi-degré, sans attendre de nouvelles scènes L2B.
- Atlas des biomasses : la fiche intrant gagne une ligne « sol du bassin » (kaolinitique, smectitique, calcaire…) — étiquette SOURCÉ quand un granule couvre le bassin, ILLUSTRATION sinon.
- Soil Sciences : la base de connaissance « vignite-soil-sciences » reçoit les fiches bassins rédigées à partir du croisement L2B et de l'échantillonnage L3, avec la même étiquette.
- P3 (shadow mode réel) : la minéralogie réelle alimente le passage documentaire « sol ↔ recette » du Decision Engine — toujours hors calibrage avant qualification machine.

## Limites honnêtes

- Trois cartouches et cinq scènes complètes L2B ne couvrent pas le monde : seules les scènes recoupant les boîtes de la flotte sont rattachées, les autres restent en réserve documentaire (le L3 ASA, lui, couvre le monde au demi-degré). Les cinq scènes complètes sont des fichiers locaux hors Git : leur versionnement au dépôt (environ 193 Mo) reste une décision à part.
- EMIT voit la surface affleurante (sols nus, affleurements) : les cultures couvertes et les sols profonds échappent à la mesure — la lecture est un indice, pas un dosage.
- Nuages, panaches et ombres dégradent les scènes ; l'agrégation L3 lisse au demi-degré (environ 55 km) : maille fine à documenter avant tout usage externe.
- Le rattachement aux bassins réutilise les boîtes FIRMS : approximation de région, pas un cadastre — les boîtes voisines peuvent se chevaucher, une maille peut compter pour deux bassins.
- Extraction des granules L2B : chunks compressés, h5py requis en local (geste documenté) ; le lecteur HDF5 minimal embarqué (v1.6) ne lit que les jeux contigus du L3 ASA, en secours de h5py.

## Statut

Livrée le 27/10/2026 (v1.5) : granules déplacés dans `data/emit/`, module `engine/atlas_sols_emit.py`, ce document. Extraction L2B et croisement exécutés le 06/11/2026 côté poste local, traces consignées puis corrigées le 17/11/2026. v1.6 le 17/11/2026 : mode `l3-bassins` (L3 ASA échantillonné aux boîtes des dix bassins), lecteur HDF5 minimal embarqué, repli grille documentaire — validé sur oracle synthétique (banc HDF5), lecture réelle du granule à exécuter côté poste local. v1.7 le 17/11/2026 au soir : correctif du mode `extraire` (bug du parcours des groupes HDF5 constaté en atelier sur cartouches réassemblées) et extension aux cinq scènes L2B complètes de la vague Earthdata, empreintes SHA-512 NASA vérifiées — validé sur banc à leurre h5py fidèle au bug (scénarios nominal, absent, corrompu), lecteur embarqué et mode `l3-bassins` inchangés ligne à ligne. Étiquette : SOURCÉ (fractions EMIT) / ILLUSTRATION (lectures agronomiques). Usage : lecture documentaire, fiches atlas, data room sous NDA — jamais le calibrage, jamais le registre Merkle de production.
