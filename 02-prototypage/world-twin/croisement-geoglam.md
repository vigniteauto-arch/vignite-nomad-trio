# Croisement GEOGLAM — calendriers culturaux des sept hubs (v0.7, 17/10/2026)

Le croisement GEOGLAM confronte les fenêtres d'opération du moteur (engine/monde.py, étiquetées ILLUSTRATION) aux calendriers culturaux sous-nationaux réels et aux conditions de campagne du mois. Conditions de campagne au 28/09/2026 (bulletins du 01/10/2026) : re-vérifier avant tout usage externe.

## Sources et méthode

- Calendriers sous-nationaux CM4EW : jeu GEOGLAM publié sur Zenodo (DOI 10.5281/zenodo.10949971 ; V1.3 du 09/07/2025, V1.4 du 24/02/2026, licence CC-BY 4.0), extrait le 17/10/2026 en machine via la couche Africa GeoPortal (mois de phase). DONNÉES RÉELLES.
- Régions GEOGLAM : couches officielles NASA Harvest/UMD (ArcGIS) interrogées le 17/10/2026 — France Northern/Southern, Italie, Espagne, Argentine douze régions (dont Western = Cuyo, Northeast = Misiones), Maroc six régions (dont Northern), Suisse absente. DONNÉES RÉELLES.
- Bulletins : Crop Monitor for AMIS n° 143 et Crop Monitor for Early Warning n° 120, publiés le 01/10/2026, conditions au 28/09/2026. DONNÉES RÉELLES.
- Calendriers AMIS : le téléchargement officiel est annoncé « à venir » au 17/10/2026 ; conformément à la méthode GEOGLAM documentée (base USDA Major World Crop Areas, FAO GIEWS), les dates des pays AMIS sont sourcées par les bases publiques équivalentes, croisées. Le portail IPAD de l'USDA a été fermé au public (constat 17/10/2026).
- Sources locales croisées : Arvalis et La France Agricole (maïs grain France) ; ABrideCamargue, Connexion France et Les Bains Gardians (riz Camargue, trois sources concordantes) ; Grano Italiano (blé dur Puglia) ; MAPA, calendrier de siembra y recolección 2014-2016, Badajoz (Estrémadure) ; Loneralj et Grain Brokers Australia (blé argentin) ; GeoPard compilant l'USDA FAS (maïs argentin).

## Verdicts par hub

### fr-rhone — France (GEOGLAM : France Northern/Southern)

- Maïs grain : semis avril-mai ; récolte du maïs grain prévue autour du 5-20 octobre (Arvalis), au plus tard fin octobre au niveau national, chantiers jusqu'en décembre selon l'année (Arvalis 2026, La France Agricole). Verdict : fenêtre mais-rdm [10-12] VALIDÉE — les résidus suivent la moisson ; fenêtre conservée à l'identique dans monde.py.
- Riz (Camargue) : moisson de la mi-septembre à la fin octobre (trois sources concordantes). Verdict : fenêtre paille-riz [10-12] VALIDÉE. Le riz camarguais est hors des calendriers AMIS (production mineure à l'échelle mondiale) : sources locales, pas GEOGLAM.
- Campagne (28/09/2026) : maïs UE dégradé par des déficits de pluie persistants et de la chaleur en Europe de l'Ouest.

### ch-leman — Suisse (absente des couches GEOGLAM)

- Suisse absente des calendriers CM4EW et du bulletin AMIS. Verdict : HORS PÉRIMÈTRE GEOGLAM — à sourcer via OFAG/Agroscope si besoin. Les pérennes du hub (sarments, marc) restent régies par l'atlas v0.5 et le cahier pilote.

### it-puglia — Italie (GEOGLAM : Italie)

- Blé dur : semis « autour du 20 novembre et tout le mois de décembre » (Grano Italiano) ; moisson débutée vers le 25 mai dans les zones arides, terminée fin juin sur les Monti Dauni. Verdict : aucune biomasse céréalière dans monde.py pour ce hub — fenêtre candidate paille de blé dur [6-7], À SOURCER (gisement, ratio, volumes).

### es-extremadura — Espagne (GEOGLAM : Espagne)

- Blé dur (Badajoz, calendrier MAPA 2014-2016) : semis réparti octobre-décembre (30/60/10 %), récolte juin-juillet (90/10 %). Verdict : fenêtre candidate paille de blé dur [7-8], À SOURCER.
- Orge brassicole : semis octobre-novembre, récolte juin-juillet. Verdict : fenêtre candidate paille d'orge [7-8], À SOURCER.
- Riz (bassin du Guadiana) : semis avril-mai (índica/japónica 10/90 %), récolte septembre-octobre (70/30 %). Verdict : fenêtre candidate paille de riz [10-11], À SOURCER.

### ar-cuyo — Argentine, Mendoza (GEOGLAM : Western = Cuyo)

- Blé : semis juin-août, récolte novembre-décembre, pic en décembre (Loneralj, Grain Brokers Australia). Maïs : semis échelonnés septembre-janvier, récolte mars-juillet (GeoPard compilant l'USDA FAS).
- Verdict : restos-poda [6-8] = taille d'hiver de la vigne mendocine — cohérence saisonnière VALIDÉE (hors fenêtre de récolte du blé) ; fenêtre candidate paille de blé [12-1], À SOURCER. Le trio Cuyo peut enchaîner deux calendriers : paille de blé (nov-déc) puis taille de vigne (juin-août).
- Campagne (28/09/2026) : blé argentin favorable au stade végétatif, surface semée en baisse ; outlook octobre-décembre : précipitations au-dessus de la moyenne et températures en dessous sur la principale région agricole.

### ar-misiones — Argentine, Misiones (GEOGLAM : Northeast = Misiones)

- Maïs (Argentine) : semis échelonnés septembre-janvier, récolte mars-juillet (GeoPard compilant l'USDA FAS). Verdict : fenêtre candidate restos de maïz [4-7], À SOURCER.
- La yerba mate, pérenne, reste hors périmètre GEOGLAM — calendrier de l'atlas v0.5 inchangé (fenêtre moteur [4-6, 9-11], zafra).

### ma-atlas — Maroc, Meknès (GEOGLAM : Northern ou Central, à trancher)

- Blé tendre (région Northern, calendriers CM4EW en machine) : semis octobre, dormance hivernale, reprise végétative janvier, moisson à partir de mai, fin de saison juillet, hors saison août ; région Central voisine : moisson dès avril.
- Verdict : fenêtre candidate paille de blé [5-7], À SOURCER. La moisson du blé (avril-juillet) précède la campagne oléicole (nov-fév) : deux calendriers superposés sans collision.
- Campagne (28/09/2026) : MENA — préparation des sols du blé 2026/27 en cours, semis à partir d'octobre.

## Écarts documentés

- Pérennes (vigne, olivier, noyer, yerba mate) : hors périmètre GEOGLAM (quatre céréales AMIS + cultures de sécurité alimentaire CM4EW). Les calendriers de l'atlas v0.5 restent la référence pour ces biomasses.
- Suisse : absente des couches GEOGLAM et des deux bulletins.
- Meknès/Saïss : rattachement GEOGLAM Northern ou Central à trancher ; fourchette de moisson avril-juillet.
- Fenêtres candidates : jamais ingérées dans monde.py avant sourcing complet (gisement, ratio, volumes) — doctrine PI inchangée.

## Lecture stratégique

Partout, un second calendrier agricole s'ajoute au premier : la récolte d'une culture annuelle précède ou chevauche la fenêtre d'un résidu pérenne (Cuyo : paille de blé nov.-déc. puis taille de vigne juin-août ; Maroc : paille de blé avril-juillet puis campagne oléicole nov.-fév.). Les détections FIRMS du 17/10/2026 tombent toutes dans des fenêtres phénologiques actives (Camargue en moisson de riz, Puglia/Estrémadure en pré-plantation céréalière, Al-Atlas à l'ouverture du semis 2026/27) : GEOGLAM donne la phénologie, FIRMS la conséquence, la réglementation v0.6 l'interdit. Les trois couches convergent.
