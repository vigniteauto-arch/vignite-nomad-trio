# Croisement GEOGLAM — calendiers culturaux des sept hubs (v0.7, 17/10/2026)

Le croisement GEOGLAM confronte les fenêtres d'opération du moteur (engine/monde.py, étiquetées ILLUSTRATION) aux calendiers culturaux sous-nationaux réels et aux conditions de campagne du mois. Conditions de campagne au 28/09/2026 (bulletins du 01/10/2026) : re-vérifier avant tout usage externe.

## Sources et méthode

- Calendiers sous-nationaux CM4EW : jeu GEOGLAM publié sur Zenodo (DOI 10.5281/zenodo.10949971 ; V1.3 du 09/07/2025, V1.4 du 24/02/2026, licence CC-BY 4.0), extrait le 17/10/2026 en machine via la couche Africa GeoPortal (mois de phase). DONNÉES RÉELLES.
- Régions GEOGLAM : couches officielles NASA Harvest/UMD (ArcGIS) interrogées le 17/10/2026 — France Northern/Southern, Italie, Espagne, Argentine douze régions (dont Western = Cuyo, Northeast = Misiones), Maroc six régions (dont Northern), Suisse absente. DONNÉES RÉELLES.
- Bulletins : Crop Monitor for AMIS n° 143 et Crop Monitor for Early Warning n° 120, publiés le 01/10/2026, conditions au 28/09/2026. DONNÉES RÉELLES.
- Calendiers AMIS : le téléchargement officiel est annoncé « à venir » au 17/10/2026 ; conformément à la méthode GEOGLAM documentée (base USDA Major World Crop Areas, FAO GIEWS), les dates des pays AMIS sont sourcées par les bases publiques équivalentes, croisées. Le portail IPAD de l'USDA a été fermé au public (constat 17/10/2026).
- Sources locales croisées : Arvalis et La France Agricole (maïs grain France) ; ABrideCamargue, Connexion France et Les Bains Gardians (riz Camargue, trois sources concordantes) ; Grano Italiano (blé dur Puglia) ; MAPA, calendrier de siembra y recolección 2014-2016, Badajoz (Estrémadure) ; Loneralj et Grain Brokers Australia (blé argentin) ; GeoPard compilant l'USDA FAS (maïs argentin).

## Verdicts par hub

### fr-rhone — France (GEOGLAM AMIS : Northern / Southern France)

- Maïs grain : semis avril-mai ; récolte du maïs grain prévue autour du 5-20 octobre (Arvalis), au plus tard fin octobre au niveau national, chantiers jusqu'en décembre selon l'année (Arvalis 2026, La France Agricole). Verdict : fenêtre mais-rdm [10-12] VALIDÉE — les résidus suivent la moisson ; fenêtre conservée à l'identique dans monde.py.
- Riz (Camargue) : moisson de la mi-septembre à la fin octobre (trois sources concordantes). Verdict : fenêtre paille-riz [10-12] VALIDÉE. Le riz camarguais est hors des calendiers AMIS (production mineure à l'échelle mondiale) : sources locales, pas GEOGLAM.
- Condition de campagne (AMIS n° 143) : déficits de pluie persistants et chaleur qui continuent de dégrader le maïs en Europe de l'Ouest et une partie de l'Europe centrale.
- Hors périmètre GEOGLAM : vigne (sarments, marc), noyer (coques) — cultures pérennes ; calendriers inchangés (atlas v0.5).

### ch-leman — Suisse (absente des couches GEOGLAM)

- La Suisse ne figure ni dans les régions AMIS ni dans les pays CM4EW (requête du 17/10/2026 sur les couches officielles) : pas de calendrier GEOGLAM pour ce hub.
- Hors périmètre : vigne (Lavaux). Calendriers céréaliers suisses (froment, maïs) À VÉRIFIER (OFAG, Agroscope) si un besoin apparaît.

### it-puglia — Italie (GEOGLAM AMIS : Italie, une seule région)

- Blé dur : semis « autour du 20 novembre et tout le mois de décembre » (Grano Italiano) ; moisson débutée vers le 25 mai dans les zones arides, terminée fin juin sur les Monti Dauni. Verdict : aucune biomasse céréalière dans monde.py pour ce hub — fenêtre candidate paille de blé dur [6-7], À SOURCER (gisement, ratio, volumes).
- Condition de campagne (AMIS n° 143) : maïs UE dégradé par la sécheresse en Europe de l'Ouest ; le semis du blé dur pugliese (novembre-décembre) dépend des pluies d'automne.
- Hors périmètre : olivier (grignons), vigne (sarments) — fenêtres v0.5 inchangées.

### es-extremadura — Espagne (GEOGLAM AMIS : Espagne, une seule région)

- Blé dur (Badajoz, calendrier MAPA 2014-2016) : semis réparti octobre-décembre (30/60/10 %), récolte juin-juillet (90/10 %). Verdict : fenêtre candidate paille de blé dur [7-8], À SOURCER.
- Orge brassicole (Badajoz) : semis octobre-novembre, récolte juin-juillet — fenêtre candidate [7-8], À SOURCER.
- Riz (Badajoz, índica et japónica) : semis avril-mai, récolte septembre-octobre (70/30 %) — fenêtre candidate paille de riz du Guadiana [10-11], À SOURCER.
- Prévisions deux semaines (AMIS n° 143) : risque de précipitations sous la moyenne sur le nord-ouest de l'Espagne.
- Hors périmètre : olivier (grignons), vigne (sarments) — fenêtres v0.5 inchangées.

### ar-cuyo — Argentine, Cuyo-Mendoza (GEOGLAM AMIS : Western Argentina)

- Blé : semis juin-août (automne-hiver austral), récolte novembre-décembre (Loneralj ; Grain Brokers Australia : pic en décembre, jusqu'à fin janvier au sud). Condition (AMIS n° 143) : blé favorable, principalement au stade végétatif, surface semée en baisse ; outlook précipitations au-dessus de la moyenne et températures en dessous pour octobre-décembre.
- Verdict : restos-poda [6-8] = taille d'hiver de la vigne mendocine — cohérence saisonnière VALIDÉE (hors fenêtre de récolte du blé) ; fenêtre candidate paille de blé [12-1], À SOURCER. Le trio Cuyo peut enchaîner deux calendriers : paille de blé (nov-déc) puis taille de vigne (juin-août).
- Hors périmètre : vigne (restes de poda) — pérenne ; fenêtre v0.5 inchangée.

### ar-misiones — Argentine, Misiones (GEOGLAM AMIS : Northeast Argentina)

- Maïs (Argentine) : semis échelonnés septembre-janvier, récolte mars-juillet (GeoPard compilant l'USDA FAS). Verdict : fenêtre candidate restos de maïz [4-7], À SOURCER.
- El Niño (AMIS n° 143) : présent et se renforçant, très probablement très fort de septembre 2026 à janvier 2027, parmi les plus forts depuis 1950 ; IOD positif octobre-décembre — outlook humide sur la grande région agricole argentine : vigilance sur les chantiers de récolte.
- Hors périmètre : yerba mate (pérenne, zafra INYM v0.5) — fenêtre inchangée.

### ma-atlas — Maroc, Al-Atlas/Meknès (GEOGLAM CM4EW : Morocco Northern)

- Blé tendre (calendrier GEOGLAM CM4EW, extraction machine du 17/10/2026, région Northern) : semis octobre, reprise végétative janvier (après dormance hivernale), moisson à partir de mai, fin de saison en juillet, hors saison en août. Double décodage concordant du même enregistrement : champs jours-de-l'année (289/1/121/182/213) et champs littéraux (October/January/May/July/August). Région Central voisine : moisson à partir d'avril, fin en juin — Meknès/Saïss : rattachement Northern ou Central à trancher, fourchette de moisson avril-juillet.
- Condition de campagne (CM4EW n° 120, Moyen-Orient et Afrique du Nord) : préparation des sols de la saison blé 2026/27 en cours, semis à partir d'octobre — la fenêtre d'ouverture est en cours.
- Verdict : fenêtre candidate paille de blé [5-7], À SOURCER. La moisson du blé (avril-juillet) précède la campagne oléicole (nov-fév) : deux calendriers superposés sans collision.
- Hors périmètre : olivier (grignons) — fenêtre v0.5 inchangée.

## Lecture stratégique transversale

Partout, un second calendrier agricole s'ajoute au premier : la récolte d'une culture annuelle précède ou chevauche la fenêtre d'un résidu pérenne. Le trio peut vivre sur les deux — à Cuyo, la paille de blé (novembre-décembre) précède la taille de la vigne (juin-août) ; au Maroc, la paille de blé (avril-juillet) précède la campagne oléicole (novembre-février) ; en Estrémadure, la paille de riz du Guadiana (octobre) prolonge la fenêtre des grignons. Le croisement des détections FIRMS du 17/10/2026 est cohérent : Camargue en pleine moisson du riz, Puglia et Estrémadure en pré-plantation des céréales d'hiver, Al-Atlas à l'ouverture du semis 2026/27. GEOGLAM donne la phénologie, FIRMS la conséquence, la réglementation (v0.6) l'interdit — les trois couches convergent vers la même conclusion : le feu est un crime agricole, le trio est l'alibi productif.

## Écarts documentés et garde-fous

- Cultures pérennes (vigne, olivier, noyer, yerba mate) : hors périmètre GEOGLAM, qui ne couvre que les céréales et légumineuses majeures ; les calendriers pérennes restent ceux de l'atlas v0.5.
- Suisse : absente des deux bulletins GEOGLAM — écart à combler par sources fédérales si besoin.
- Calendiers AMIS non téléchargeables (« à venir ») ; portail IPAD USDA fermé au public (17/10/2026) — les dates AMIS passent par les bases publiques croisées.
- Toute fenêtre candidate reste une hypothèse : gisement, ratio et volumes à sourcer avant toute entrée dans monde.py. Aucune valeur calibrée ; tout résultat de simulation reste étiqueté SYNTHÉTIQUE.
