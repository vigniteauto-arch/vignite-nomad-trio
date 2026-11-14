# Adossement aux négociants dominants des filières — couche V2.9 (14/11/2026)

Couche `engine/partenaires_fileres.py` — pour chacun des 219 hubs de la
flotte World Twin, le négociant (ou l'écosystème) dominant de chaque
famille de co-produits présente, avec le véhicule d'adossement
recommandé. Objectif de Manu : s'adosser au dominant de chaque filière
pour soit des projets pilote, soit des LOI (Letter Of Intent, lettre
d'intention) ou des contrats d'offtake « à l'usine », soit des
franchises ou du licensing.

## Méthode

- Une ligne d'adossement par famille présente dans chaque hub :
  421 lignes au total, 24 familles couvertes.
- Résolution en cascade : entrée pays si la littérature, un classement
  public ou une structure filière documente le dominant du pays
  (63 entrées pays), sinon repli sur le négociant international de la
  filière (étiquette MONDIAL, proxy explicite), sinon écosystème
  documenté sans acteur unique (étiquette ILLUSTRATION).
- Sources croisées (publiques, vérifiées le 14/11/2026) : classements
  publics des négociants, sites et rapports officiels des groupes,
  presse filière, structures de filière (UNICA — União da Indústria de
  Cana-de-Açúcar, MPOB — Malaysian Palm Oil Board, PalmWatch, FNC —
  Federación Nacional de Cafeteros, California Walnut Board, Cocobod,
  Çaykur, ECX — bourse d'Éthiopie), précédents internes documentés
  (doctrine café Colombie, triptyque cacao, stratégie riz volume).

## Les trois véhicules d'adossement

- PILOTE : projet pilote avec l'écosystème de collecte, pour les
  gisements diffus (AU_CHAMP, SARGASSES, NOYAUX_FRUITS). Aucun acteur
  unique par nature : coopératives, organismes de collecte, puissance
  publique. Exemple : dépôts de biomasse du dispositif CRM indien
  (544 crore de roupies, CEEW — Council on Energy, Environment and
  Water) et FPO (Farmer Producer Organisations).
- LOI_USINE : LOI ou contrat d'offtake à l'usine, pour les gisements
  concentrés au site du dominant. Le co-produit sort de l'usine du
  dominant : la LOI capte le flux à la source. Exemple : bagasse des
  sucreries Raízen (alliance Cosan-Shell), marcs des distilleries
  Grap'Sud + UDM (fusion : premier groupe mondial de distilleries
  vinicoles, Vitisphere).
- FRANCHISE : franchise/licensing au dominant local, pour les pays hors
  périmètre direct (doctrine international : le partenaire local
  finance le matériel, Vignite perçoit des royalties). Le mode
  d'entrée est DIRECT pour les six pays du périmètre pilotes et
  filiales (France, Suisse, Italie, Espagne, Argentine, Maroc),
  LICENSING partout ailleurs ; en pays LICENSING, même une famille
  LOI_USINE passe par le véhicule franchise (le dominant local devient
  franchisé cible de la technologie).

## Table des dominants par famille (extraits)

| Famille | Monde (repli proxy) | Entrées pays SOURCÉES |
|---|---|---|
| CANNE | sucreries locales (co-produit capté à l'usine) | Raízen, Tereos, São Martinho (Brésil) ; Mitr Phol (Thaïlande) ; Balrampur Chini (Inde) ; Azcuba (Cuba) |
| RIZ | Olam Agri, Wilmar, LDC, COFCO | CP Intertrade (Thaïlande) ; Loc Troi (Viêt Nam) ; Olam Agri (Nigeria) |
| MAIS | ABCD (ADM, Bunge, Cargill, LDC) + COFCO | NIBULON (Ukraine) ; Axéréal, Terrena (France) ; Flour Mills of Nigeria |
| PALMIER | Wilmar, Musim Mas, GAR, Sime Darby, Cargill | Sime Darby + FGV (Malaisie) ; GAR + Musim Mas + Wilmar (Indonésie) ; Okomu + Presco (Nigeria) ; PalmCI/SIFCA (Côte d'Ivoire) |
| MANIOC | usines d'amidon et farineries | PCPL, Matna Foods, Psaltry, FMN Agro (Nigeria) ; groupes d'amidon de tapioca (Thaïlande) |
| VIGNE_MARC / SARMENTS | distilleries vinicoles | Grap'Sud + UDM (France) |
| CAFE | ECOM, Volcafé, LDC, Olam Agri, Suárez, Mercon | FNC + Cenicafé + Buencafé (Colombie) ; ECOM (Mexique) ; ECX + unions Oromia et Sidama (Éthiopie) |
| CACAO | Barry Callebaut, Cargill, OFI, Touton | acheteurs agréés + usines Cargill et Barry Callebaut (Côte d'Ivoire) ; LBC sous Cocobod (Ghana) ; Luker Cacao + Fedecacao (Colombie) |
| OLIVE | coopératives et mouliniers | Sovena (Portugal) ; stations de Sfax (Tunisie) ; Dcoop (Espagne) |
| AGRUMES | Cutrale + Citrosuco | duo brésilien (« un verre de jus sur trois dans le monde ») |
| THE | usines de thé | Çaykur (Turquie, monopole d'État) ; Forbes & Walker et brokers de Colombo (Sri Lanka) |
| COCO | décortiqueurs et usines de coprah | Franklin Baker, Peter Paul, Centennial (Philippines) |
| DATTIER | stations de conditionnement | Nouri & Cie, Nouran (Tunisie) |
| BIERE | AB InBev, Heineken, Castel | Kronenbourg (France) |
| AGAVE | Becle (José Cuervo), Herradura/Patrón | Becle (Mexique, n°1 mondial de tequila) |
| SARGASSES | — | SEMAR (Marine mexicaine, 156 063 t Quintana Roo saison 2026) + hôtellerie Riviera Maya + Carbonwave (IFC) (Mexique) |
| FORET_SCIERIE | groupes de scieries régionaux | West Fraser (Canada) ; Södra + Metsä (Suède) |
| NOIX_COQUES | hullers (modèle californien) | handlers de Californie (liste officielle California Walnut Board, États-Unis) |
| PECHE_COQUILLES | conserveries et criées | organisations de producteurs conchylicoles (France) |
| AU_CHAMP | AUCUN dominant par nature (gisement diffus) | coopératives et CUMA (France) ; dépôts CRM + FPO (Inde) |
| CAFE_PULPE | beneficios humides | ECOM et bénéficios du Chiapas (Mexique) ; centrales FNC (Colombie) |
| NOYAUX_FRUITS | stations de conditionnement | coopératives fruitières (France) |
| POMME | pressoirs cidricoles | coopératives cidricoles (France) ; pressoirs (Suisse) |

(Le module `python3 engine/partenaires_fileres.py table` imprime la
table complète des 219 hubs avec la famille dominante de chacun.)

## Statuts

- SOURCÉ : entrée pays documentée (63 entrées pays).
- MONDIAL (proxy) : repli sur le négociant international de la
  filière, explicite et distinct de SOURCÉ.
- ILLUSTRATION : écosystème documenté sans acteur unique (gisements
  diffus, filières fragmentées).

## Résultats du verifier (14/11/2026)

- 219 hubs couverts, 24 familles, 63 entrées pays SOURCÉES.
- 421 lignes d'adossement : 70 ancrées pays, 351 en repli mondial.
- Modes recommandés : 382 franchise/licensing, 25 LOI à l'usine,
  14 pilote (les entrées DIRECT portent les LOI à l'usine et les
  pilotes ; le reste de la flotte passe par la doctrine licensing).
- Sondages : gen-bresil-3 CANNE Raízen, gen-malaisie-1 PALMIER
  Sime Darby, gen-mexique-1 CAFE_PULPE ECOM, gen-mexique-3 AGAVE
  Cuervo, gen-mexique-4 SARGASSES SEMAR, gen-nigeria-1 RIZ Olam,
  fr-rhone VIGNE_MARC Grap'Sud.
- Anti-fuite : aucun jeton de coût dans les fiches et les couches.

## Intégration aux cartes

- Table « Adossement filière — V2.9 » dans la fiche hub des deux modes
  (public et privé) : une ligne par famille (acteur dominant, étiquette
  de statut, véhicule recommandé, ancre pays ou mondiale), ligne de
  mode d'entrée pays, rappel de doctrine.
- Bandeau de sources étendu : « adossement aux négociants dominants
  des filières V2.9 (pilote / LOI à l'usine / franchise-licensing,
  faits publics) ».
- Le verifier de build_carte contrôle les 219 fiches partenaires comme
  les couches CaO/P3/sites.

## Anti-fuite et doctrine

Faits publics uniquement (qui domine quelle filière, où, source
publique) et recommandations génériques de véhicule. Aucun contact
nominatif, aucun état de négociation versionné, aucun coût, aucune
valeur calibrée du VDE (Vignite Decision Engine). La prospection reste
hors dépôt : le World Twin désigne les cibles, il ne préjuge d'aucune
discussion en cours.
