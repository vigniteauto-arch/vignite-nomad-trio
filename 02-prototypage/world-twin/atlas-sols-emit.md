# Atlas des sols — NASA EMIT (V1.5, 27/10/2026)

Socle « Soil Sciences » de la couche 1 du World Twin : minéralogie des sols des bassins de la flotte par les données publiques NASA EMIT, pour la lecture agronomique des intrants (rétention d'eau, CEC — Capacité d'Échange Cationique, dosage biochar) et l'affinage documentaire de l'atlas des biomasses.

EMIT — Earth Surface Mineral Dust Source Investigation : spectromètre imageur embarqué sur la station spatiale internationale (ISS — International Space Station), 380-2500 nm, cartographie de la minéralogie des surfaces affleurantes.

## Produits et provenance (SOURCÉ)

- EMIT L2B MIN (EMITL2BMIN) : « Estimated Mineral Identification and Band Depth and Uncertainty », maille 60 m, scène par scène. Trois granules versionnés au dépôt, dossier `data/emit/` :
  - `EMIT_L2B_MIN_001_20230124T153032_2302410_038.nc` — scène du 24/01/2023 ;
  - `EMIT_L2B_MIN_001_20230804T113000_2321608_018.nc` — scène du 04/08/2023 ;
  - `EMIT_L2B_MIN_001_20240723T152209_2420510_006.nc` — scène du 23/07/2024.
- EMIT L3 ASA (EMITL3ASA) : « Aggregated Mineral Spectral Abundance and Uncertainty », agrégation mondiale au demi-degré — la couche directement exploitable pour les dix bassins de la flotte. Un fichier versionné : `data/emit/EMIT_L3_ASA_002.zip`.
- Diffusion : NASA LP DAAC (Land Processes Distributed Active Archive Center), Earthdata, données publiques. Fichiers d'origine : uploads du 24/10/2026 (racine du dépôt), déplacés dans `data/emit/` par la vague v1.5.

## Règles absolues (inchangées)

- Données publiques NASA uniquement : aucun paramètre VDE (Vignite Decision Engine), aucune valeur calibrée, aucune clé.
- Les fractions minérales extraites sont SOURCÉES (NASA EMIT) ; toute lecture agronomique est ILLUSTRATION documentaire, jamais une prescription agronomique, jamais un calibrage.
- Les fichiers réassemblés et extractions vivent dans `cache-sols/`, jamais versionnés.
- La simulation éprouve la logique, jamais la physique. La qualification reste le monopole des FAT/SAT (Factory/Shop Acceptance Tests) sur machines réelles.

## Workflow machine (`engine/atlas_sols_emit.py`, bibliothèque standard)

1. `inventaire` — tailles, empreintes md5 et complétude des granules versionnés (parts et zip). Écrit `cache-sols/inventaire.json`.
2. `reassembler CARTOUCHE` — concatène les `.partN` en `.nc` dans `cache-sols/` (jamais versionné). Cartouches : `2302410_038`, `2321608_018`, `2420510_006`.
3. `extraire [CARTOUCHE]` — empreinte géographique et variables des granules réassemblés. Requiert localement un lecteur NetCDF-4/HDF5 (`pip install h5py`, ou netCDF4, ou xarray) ; sans lecteur, arrêt propre avec consigne — les autres modes restent disponibles.
4. `croiser` — rattachement des scènes aux dix bassins de la flotte (mêmes boîtes géographiques que la couche FIRMS : approximation de la région, pas un cadastre). Écrit `cache-sols/croisement.json`.
5. `sommaire [BASSIN]` — sommaire de la couche sols, ou fiche d'un bassin.

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

- Couche 1 (données monde) : la minéralogie rejoint la météo (ERA5), le brûlage (FIRMS) et les calendriers (GEOGLAM) comme quatrième observable public par bassin.
- Atlas des biomasses : la fiche intrant gagne une ligne « sol du bassin » (kaolinitique, smectitique, calcaire…) — étiquette SOURCÉ quand le granule couvre le bassin, ILLUSTRATION sinon.
- Soil Sciences : la base de connaissance « vignite-soil-sciences » reçoit les fiches bassins rédigées à partir du croisement, avec la même étiquette.
- P3 (shadow mode réel) : la minéralogie réelle alimente le passage documentaire « sol ↔ recette » du Decision Engine — toujours hors calibrage avant qualification machine.

## Limites honnêtes

- Trois scènes L2B ne couvrent pas le monde : seules les scènes recoupant les boîtes de la flotte sont rattachées, les autres restent en réserve documentaire (le L3 ASA, lui, couvre le monde au demi-degré).
- EMIT voit la surface affleurante (sols nus, affleurements) : les cultures couvertes et les sols profonds échappent à la mesure — la lecture est un indice, pas un dosage.
- Nuages, panaches et ombres dégradent les scènes ; l'agrégation L3 lisse au demi-degré (environ 55 km) : maille fine à documenter avant tout usage externe.
- Le rattachement aux bassins réutilise les boîtes FIRMS : approximation de région, pas un cadastre.
- Extraction des `.nc` : lecture hors bibliothèque standard (h5py/netCDF4/xarray) — la vague versionne le module et les données, l'extraction reste un geste local documenté.

## Statut

Livrée le 27/10/2026 (v1.5) : granules déplacés dans `data/emit/`, module `engine/atlas_sols_emit.py`, ce document. Extraction et croisement restent à exécuter en local (lecteur HDF5) ; les fiches bassins suivront la première extraction couronnée de succès. Étiquette : SOURCÉ (fractions EMIT) / ILLUSTRATION (lectures agronomiques). Usage : lecture documentaire, fiches atlas, data room sous NDA — jamais le calibrage, jamais le registre Merkle de production.
