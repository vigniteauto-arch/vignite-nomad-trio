# Atlas des biomasses monde — World Twin (v1.0)

Vague v1.0 du programme World Twin (18/10/2026) : les 52 intrants de l'atlas des biomasses — les 50 du dataset du VDE (Vignite Decision Engine, moteur de décision) et les deux addendums à mesurer (yerba mate, papaye) — placés sur le globe. Chaque intrant porte : sa famille, ses identités FR et EN (anglais), son pays et sa région, un point GPS (Global Positioning System) de positionnement (hub existant de la flotte ou point candidat), son type de biomasse, un gisement indicatif étiqueté, sa fenêtre saisonnière, ses techniques culturales et de récolte/transformation, sa réglementation associée (brûlage, enfouissement, traitement, coût pour l'agriculture, main-d'œuvre) et son rattachement éventuel à un bassin ERA5 (European Reanalysis v5, réanalyse météorologique) de la flotte. Un pointage météo temps réel est disponible en ligne de commande pour les 52 points.

Ce dossier prolonge la chaîne documentaire du World Twin : atlas des gisements (v0.5), fiches pays réglementaires (v0.6), croisement GEOGLAM (Group on Earth Observations Global Agricultural Monitoring, v0.7), FIRMS historique (Fire Information for Resource Management System, v0.8), gisements FAOSTAT bulk (Organisation des Nations unies pour l'alimentation et l'agriculture, v0.9).

## Doctrine de propriété intellectuelle

Aucune valeur calibrée de l'atlas privé ne vit dans ce dossier. Les six paramètres du VDE — lignine, cellulose, Tg (glass transition temperature, température de transition vitreuse), humidité maximale, alpha de diffusion, friction — restent dans l'atlas privé scellé, hors du dépôt. Le présent atlas ne versionne que des données publiques : géographie, volumes, calendriers, réglementation, météo. Les identités des intrants (noms FR et EN) sont publiques ; leurs caractérisations ne le sont pas.

## Méthode et étiquettes

- Gisements : chaque chiffre porte une étiquette SOURCÉ (vérifiable, source citée : FAOSTAT v0.9, INYM — Instituto Nacional de la Yerba Mate, COI — Conseil Oléicole International, fiches v0.6) ou ILLUSTRATION (ordre de grandeur documentaire, ratios de littérature, à sourcer avant tout usage). Les ratios de conversion (part de coque dans la noix, part de marc dans la vendange) sont ILLUSTRATION.
- Réglementation : chaque élément porte DONNÉES RÉELLES (texte légal ou source officielle identifiée — les pays des 7 hubs sont couverts par les fiches v0.6) ou À VÉRIFIER (nouvelles juridictions : connaissance générale, référence nommée mais non confirmée document par document ; re-vérification obligatoire avant tout usage externe).
- Points GPS : approximations de région de positionnement (un trio Nomad se positionnerait dans cette région), pas un cadastre. À affiner avant tout ancrage terrain.
- Familles : issues du nettoyage du 29/09/2026 (Cultures pérennes 4, Coques et noyaux 11, Céréales 10, Tropical 12, Forestier 7, Brassicole 1, Marin 1, Minéral 4) plus les deux addendums. Deux rattachements agronomiques documentés s'écartent de la lettre du master : MARC_POMME placé en Cultures pérennes (résidu d'un verger pérenne) et TIGE_BAMBOU en Tropical. Le master privé reste l'autorité sur ces rattachements.
- Fenêtres saisonnières : pour les biomasses simulées par la flotte, la fenêtre reprend exactement celle de `engine/monde.py` ; pour les points candidats, la fenêtre décrit la campagne culturale réelle (hémisphère Sud inclus).
- Deux intrants portent le statut À MESURER (addendum du 10/10/2026) : RESIDU_YERBA_MATE et GRAINE_PAPAYE — caractérisation à faire avant ingestion VDE.

## Vue d'ensemble par famille
| Famille | Intrants | Jetons |
| --- | --- | --- |
| Cultures pérennes | 5 | MARC_RAISIN, SARMENT_VIGNE, RAFFLE_RAISIN, RAMEAU_OLIVIER, MARC_POMME |
| Coques & noyaux | 11 | NOYAU_OLIVE, COQUE_NOIX, COQUE_AMANDE, COQUE_PISTACHE, COQUE_NOISETTE, NOYAU_CERISE, NOYAU_PECHE, NOYAU_ABRICOT, COQUE_MACADAMIA, COQUE_PECAN, NOYAU_AVOCAT |
| Céréales | 10 | PAILLE_BLE, PAILLE_RIZ, RAFLE_MAIS, TIGE_TOURNESOL, TIGE_COLZA, CHENEVOTTE, PAILLE_LIN, TIGE_SORGHO, BALLE_AVOINE, TIGE_COTON |
| Tropical | 14 | BAGASSE_CANNE, BALLE_RIZ, DECHET_DATTIER, NOYAU_DATTE, RAFFLE_PALMIER, TIGE_BANANIER, FEUILLE_ANANAS, CABOSSE_CACAO, FIBRE_COCO, MARC_CAFE, RESIDU_AGAVE, TIGE_BAMBOU, RESIDU_YERBA_MATE, GRAINE_PAPAYE |
| Forestier | 6 | SCIURE_PIN, SCIURE_CHENE, ECORCE_PIN, ECORCE_EUCALYPTUS, COPEAU_HETRE, AIGUILLE_PIN |
| Brassicole | 1 | DRECHE_BIERE |
| Marin | 1 | SARGASSE |
| Minéral | 4 | COQUILLE_HUITRE, COQUILLE_MOULE, COQUILLE_ST_JACQUES, CARAPACE_CRABE |
| Total | 52 | |

## Couverture de la flotte monde

Le contrôle machine `croisement` vérifie que les 14 paires (hub, biomasse moteur) de `engine/monde.py` sont toutes rattachées à un intrant de l'atlas :

| Jeton atlas | Hub | Biomasse moteur |
| --- | --- | --- |
| MARC_RAISIN | fr-rhone | marc-raisin |
| MARC_RAISIN | ch-leman | marc-raisin |
| SARMENT_VIGNE | fr-rhone | sarments-vigne |
| SARMENT_VIGNE | ch-leman | sarments-vigne |
| SARMENT_VIGNE | it-puglia | sarments-vigne |
| SARMENT_VIGNE | es-extremadura | sarments-vigne |
| SARMENT_VIGNE | ar-cuyo | restos-poda |
| NOYAU_OLIVE | it-puglia | grignons-olive |
| NOYAU_OLIVE | es-extremadura | grignons-olive |
| NOYAU_OLIVE | ma-atlas | grignons-olive |
| COQUE_NOIX | fr-rhone | coques-noix |
| PAILLE_RIZ | fr-rhone | paille-riz |
| RAFLE_MAIS | fr-rhone | mais-rdm |
| RESIDU_YERBA_MATE | ar-misiones | yerba-mate |

## Les 52 fiches

### MARC_RAISIN — Marc de raisin / GRAPE_POMACE
- Famille : Cultures pérennes.
- Localisation : Vallée du Rhône (pilote v0), France — GPS (Global Positioning System) 44.84, 4.85, approximation de région, pas un cadastre. Point : hub existant.
- Flotte monde.py : >fr-rhone→ marc-raisin< (fr-rhone), >ch-leman→ marc-raisin< (ch-leman).
- Bassin ERA5 (European Reanalysis v5) : vallee-du-rhone.
- Type de biomasse : résidu humide de pressurage (peaux, pépins, pulpes).
- Gisement [SOURCÉ (FAOSTAT v0.9) ; ratio ILLUSTRATION] : France : 4 747 450 t de raisin récoltées en 2024 (FAOSTAT, extraction v0.9) ; marc ≈ 15 à 25 % de la vendange (ratio).
- Fenêtre saisonnière : sept-oct-nov (vendanges ; sur le hub suisse ch-leman la fenêtre moteur est [10, 11]).
- Techniques culturales, récolte, transformation : viticulture conduite en gobelet ou pergola ; vendanges manuelles et mécaniques ; pressurage au chai, le marc sort humide.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [À VÉRIFIER] : compostage ou épandage des marcs, encadrés par les plans de gestion vinicoles (référence : pratique standard, à sourcer DGAL).
- Traitement [DONNÉES RÉELLES] : distillation des marcs (bouilleurs de cru) ou méthanisation, filières historiques réglementées (référence : filière française réglementée).
- Coût pour l'agriculture [ILLUSTRATION] : évacuation du marc parfois facturée à la cave (ordre de grandeur : 0 à 30 €/t), non obligatoire (référence : à sourcer par cave).
- Main-d'œuvre [À VÉRIFIER] : aucune main-d'œuvre dédiée : le marc suit les vendanges (référence : ordre de grandeur).

### SARMENT_VIGNE — Sarments de vigne (taille) / VINE_SHOOTS
- Famille : Cultures pérennes.
- Localisation : Vallée du Rhône (pilote v0), France — GPS (Global Positioning System) 44.84, 4.85, approximation de région, pas un cadastre. Point : hub existant.
- Flotte monde.py : >fr-rhone→ sarments-vigne< (fr-rhone), >ch-leman→ sarments-vigne< (ch-leman), >it-puglia→ sarments-vigne< (it-puglia), >es-extremadura→ sarments-vigne< (es-extremadura), >ar-cuyo→ restos-poda< (ar-cuyo).
- Bassin ERA5 (European Reanalysis v5) : vallee-du-rhone.
- Type de biomasse : résidu de taille ligneux sec.
- Gisement [SOURCÉ (FAOSTAT v0.5/v0.9) ; rendement ILLUSTRATION] : ordre de grandeur : 1,5 à 3 t/ha/an de sarments ; France : 4 747 450 t de raisin 2024 (FAOSTAT v0.9) ; Mendoza : 145 393 ha de vigne (atlas v0.5).
- Fenêtre saisonnière : janv-févr-mars-avr (taille d'hiver ; hémisphère Sud : fenêtre anti-saison juin-août sur ar-cuyo [6, 7, 8]).
- Techniques culturales, récolte, transformation : taille manuelle ou mécanique, broyage au rang ou andainage ; le sarment sec sort à la taille.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre en France, dérogation préfectorale rare ; encadré en Argentine (autorisation obligatoire) (référence : Art. L.541-21-1 (France) ; Ley 26.562 (Argentine) — fiches v0.6).
- Enfouissement [À VÉRIFIER] : broyage-enfouissement au rang préconisé et pratiqué (chaque pays du hub a sa pratique documentée) (référence : pratique standard, à sourcer par bassin).
- Traitement [DONNÉES RÉELLES] : broyage, compostage ou valorisation énergétique ; le brûlage est fermé en France et contraint ailleurs (référence : fiches v0.6 (7 hubs)).
- Coût pour l'agriculture [ILLUSTRATION] : la taille est un coût obligatoire du vignoble ; la gestion du sarment est un surcoût sans valorisation (0 à 60 €/ha, ordre) (référence : à sourcer par exploitation).
- Main-d'œuvre [ILLUSTRATION] : la taille mobilise 60 à 100 heures de main-d'œuvre par hectare et par an (ordre de grandeur) (référence : littérature viticole).

### RAFFLE_RAISIN — Rafles de raisin / GRAPE_STALKS
- Famille : Cultures pérennes.
- Localisation : Vallée du Rhône (pilote v0), France — GPS (Global Positioning System) 44.84, 4.85, approximation de région, pas un cadastre. Point : hub existant.
- Flotte monde.py : .
- Bassin ERA5 (European Reanalysis v5) : vallee-du-rhone.
- Type de biomasse : squelette de la grappe, résidu humide de pressurage ou de vinification.
- Gisement [SOURCÉ (FAOSTAT v0.9) ; ratio ILLUSTRATION] : rafles ≈ 3 à 5 % de la vendange ; France : 4 747 450 t de raisin 2024 (FAOSTAT v0.9).
- Fenêtre saisonnière : sept-oct (érafilage à la réception de la vendange, pour les vinifications sans macération carbonique).
- Techniques culturales, récolte, transformation : érafleuse-fouloir au chai ; rafles sortant humides, souvent compostées.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [À VÉRIFIER] : compostage de cave le plus courant (référence : pratique standard, à sourcer).
- Traitement [À VÉRIFIER] : compostage ou méthanisation ; volume modeste mais régulier (référence : à sourcer).
- Coût pour l'agriculture [ILLUSTRATION] : négligeable en entrée : la rafle sort avec la vendange (référence : ordre de grandeur).
- Main-d'œuvre [ILLUSTRATION] : aucune main-d'œuvre dédiée : l'érafleur est déjà dans la chaîne (référence : ordre de grandeur).

### RAMEAU_OLIVIER — Rameaux d'olivier (taille) / OLIVE_BRANCHES
- Famille : Cultures pérennes.
- Localisation : Puglia — Tavoliere (Foggia), Italie — GPS (Global Positioning System) 41.12, 16.50, approximation de région, pas un cadastre. Point : hub existant.
- Flotte monde.py : .
- Bassin ERA5 (European Reanalysis v5) : italie-puglia.
- Type de biomasse : résidu de taille ligneux.
- Gisement [ILLUSTRATION (à sourcer FAOSTAT/COI régional)] : ordre de grandeur : 1 à 2,5 t/ha/an de bois de taille ; oliveraies puglieses de l'ordre de 370 000 ha (à sourcer).
- Fenêtre saisonnière : févr-mars-avr (taille après récolte, février-avril).
- Techniques culturales, récolte, transformation : oléiculture traditionnelle ou intensive ; taille manuelle et mécanique, broyage inter-rang le plus courant.
- Brûlage [DONNÉES RÉELLES] : encadré : autorisation régionale requise, interdiction dans les zones à risque incendie (référence : LR Puglia 38/2016 ; D.Lgs 152/2006 art. 185 (fiche v0.6)).
- Enfouissement [À VÉRIFIER] : broyage et enfouissement au rang préconisés (référence : pratique standard, à sourcer).
- Traitement [DONNÉES RÉELLES] : broyage, valorisation énergétique ou distillation ; la combustion est de plus en plus contrainte (référence : fiche v0.6 it-puglia).
- Coût pour l'agriculture [ILLUSTRATION] : la taille est un coût obligatoire de l'oliveraie ; la gestion du bois de taille est un surcoût sans valorisation (référence : à sourcer par exploitation).
- Main-d'œuvre [ILLUSTRATION] : la taille mobilise 20 à 50 heures/ha et par an selon la densité (ordre de grandeur) (référence : littérature oléicole).

### NOYAU_OLIVE — Noyau d'olive (grignons) / OLIVE_PIT
- Famille : Coques & noyaux.
- Localisation : Estrémadure (Badajoz), Espagne — GPS (Global Positioning System) 38.87, -6.97, approximation de région, pas un cadastre. Point : hub existant.
- Flotte monde.py : >it-puglia→ grignons-olive< (it-puglia), >es-extremadura→ grignons-olive< (es-extremadura), >ma-atlas→ grignons-olive< (ma-atlas).
- Bassin ERA5 (European Reanalysis v5) : espagne-extremadure.
- Type de biomasse : noyau et grignons d'olive, résidu oléicole dur.
- Gisement [SOURCÉ (COI/fiche v0.6) ; ratio ILLUSTRATION] : Espagne ≈ 1,4 million de t d'huile d'olive par campagne (COI, atlas v0.5) ; grignons ≈ 4 fois la masse d'huile (ratio) ; plus de 300 000 ha d'oliveraie en Estrémadure (fiche v0.6).
- Fenêtre saisonnière : nov-déc-janv-févr (campagne oléicole ; fenêtres moteur [11, 12, 1] en Puglia et [12, 1, 2] à Meknès).
- Techniques culturales, récolte, transformation : récolte par vibrateurs ou peignes, trituration sous 24 à 48 heures ; les grignons sortent du moulin après extraction à deux phases.
- Brûlage [DONNÉES RÉELLES] : interdit par principe, exceptions par ordre annuel selon le danger d'incendie (référence : Ley 7/2022 art. 27.3 ; órdenes DOE (fiche v0.6)).
- Enfouissement [À VÉRIFIER] : les grignons sont plutôt épandus ou valorisés (combustible, amendement) (référence : pratique à sourcer par moulin).
- Traitement [À VÉRIFIER] : grignonnage industriel courant : séparation noyau/pulpe, combustible ou amendement (référence : filière espagnole, à sourcer).
- Coût pour l'agriculture [ILLUSTRATION] : le moulin assume l'évacuation des grignons ; l'agriculteur reçoit parfois un dédommagement (référence : à sourcer par moulin).
- Main-d'œuvre [ILLUSTRATION] : aucune main-d'œuvre dédiée : les grignons suivent l'huilerie (référence : ordre de grandeur).

### COQUE_NOIX — Coques de noix / WALNUT_SHELL
- Famille : Coques & noyaux.
- Localisation : Périgord (pôle nucicole historique), France — GPS (Global Positioning System) 44.90, 0.70, approximation de région, pas un cadastre. Point : hub existant.
- Flotte monde.py : >fr-rhone→ coques-noix< (fr-rhone).
- Bassin ERA5 (European Reanalysis v5) : perigord.
- Type de biomasse : coque dure, résidu de décorticage.
- Gisement [SOURCÉ (FAOSTAT v0.9) ; ratio ILLUSTRATION] : France : 27 710 t de noix (avec coque) en 2024 (FAOSTAT v0.9) ; coque ≈ 50 % de la masse (ratio).
- Fenêtre saisonnière : oct-nov-déc-janv-févr (récolte octobre-novembre puis décorticage étalé jusqu'à février (fenêtre moteur fr-rhone)).
- Techniques culturales, récolte, transformation : nuciculture en vergers ; récolte mécanique (secoueuses), séchage, décorticage en atelier.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [ILLUSTRATION] : non pertinent : la coque sort de l'atelier de décorticage (référence : constat).
- Traitement [À VÉRIFIER] : granulés et litières à base de coque existent ; valorisation énergétique locale courante (référence : filière nucicole, à sourcer).
- Coût pour l'agriculture [ILLUSTRATION] : l'atelier facture ou assume le décorticage ; la coque est un sous-produit à valeur faible (référence : à sourcer par atelier).
- Main-d'œuvre [ILLUSTRATION] : décorticage mécanique : quelques heures par lot (ordre de grandeur) (référence : à sourcer).

### COQUE_AMANDE — Coques d'amande / ALMOND_SHELL
- Famille : Coques & noyaux.
- Localisation : Alicante (bassin amandier méditerranéen), Espagne — GPS (Global Positioning System) 38.35, -0.65, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : coque dure, résidu de décorticage.
- Gisement [ILLUSTRATION (à sourcer FAOSTAT/MAPA régional)] : Espagne premier producteur européen d'amandes ; coque ≈ 40 à 60 % de la masse récoltée (ratios littérature).
- Fenêtre saisonnière : août-sept-oct (récolte août-octobre selon variétés et irrigation).
- Techniques culturales, récolte, transformation : amandiers irrigués ou secs ; récolte mécanisée (secoueuses), décorticage en atelier coopératif.
- Brûlage [DONNÉES RÉELLES] : interdit par principe, exceptions par ordre annuel selon le danger d'incendie (référence : Ley 7/2022 art. 27.3 (cadre national espagnol, fiche v0.6)).
- Enfouissement [ILLUSTRATION] : non pertinent : la coque sort de l'atelier (référence : constat).
- Traitement [À VÉRIFIER] : combustible d'atelier et litière : valorisations locales établies (référence : filière espagnole, à sourcer).
- Coût pour l'agriculture [ILLUSTRATION] : la coque est traditionnellement cédée au décortiqueur ; l'agriculteur touche parfois un petit dédommagement (référence : à sourcer par coopérative).
- Main-d'œuvre [ILLUSTRATION] : décorticage mécanique continu en campagne (référence : à sourcer).

### COQUE_PISTACHE — Coques de pistache / PISTACHIO_SHELL
- Famille : Coques & noyaux.
- Localisation : Bronte (Sicile, pistachietto de l'Etna), Italie — GPS (Global Positioning System) 37.79, 14.99, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : coque ligneuse, résidu de décorticage.
- Gisement [ILLUSTRATION (à sourcer Consortium Bronte)] : Bronte : de l'ordre de 3 000 à 4 000 t de pistaches brutes les années paires (alternance bisannuelle, à sourcer).
- Fenêtre saisonnière : sept-oct (récolte septembre-octobre, années alternées).
- Techniques culturales, récolte, transformation : pistachiers sur lave de l'Etna ; récolte manuelle par ételonnage, séchage et décorticage.
- Brûlage [DONNÉES RÉELLES] : les résidus agricoles restent exclus du régime déchets seulement si valorisés ; combustion encadrée (référence : D.Lgs 152/2006 art. 185 (cadre italien, fiche v0.6)).
- Enfouissement [ILLUSTRATION] : non pertinent pour la coque d'atelier (référence : constat).
- Traitement [À VÉRIFIER] : valorisations locales à documenter (combustible,artisanat) (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : le décorticage est à la charge du producteur ou du transformateur local (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : récolte manuelle : poste dominant, plusieurs dizaines d'heures/ha (ordre de grandeur) (référence : littérature pistachière).

### COQUE_NOISETTE — Coques de noisette / HAZELNUT_SHELL
- Famille : Coques & noyaux.
- Localisation : Piémont (Cuneo), Italie — GPS (Global Positioning System) 44.38, 7.55, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : coque dure, résidu de décorticage.
- Gisement [ILLUSTRATION (à sourcer FAOSTAT)] : Italie deuxième producteur mondial, Varese-Langa : de l'ordre de 100 000 t/an de noisettes en coque (à sourcer) ; coque ≈ 45 à 50 % de la masse.
- Fenêtre saisonnière : août-sept-oct (récolte août-octobre, décorticage en campagne).
- Techniques culturales, récolte, transformation : noisetiers en vergers conduits en gobelet ; récolte mécanisée à terre, séchage, calibrage, décorticage.
- Brûlage [DONNÉES RÉELLES] : les résidus agricoles restent hors régime déchets seulement si valorisés ; combustion encadrée (référence : D.Lgs 152/2006 art. 185 (cadre italien, fiche v0.6)).
- Enfouissement [ILLUSTRATION] : non pertinent pour la coque d'atelier (référence : constat).
- Traitement [À VÉRIFIER] : combustible et litière : débouchés locaux établis à documenter (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : la coopérative assume le décorticage ; la coque est un sous-produit cédé (référence : à sourcer par coopérative).
- Main-d'œuvre [ILLUSTRATION] : décorticage mécanique continu en campagne (référence : à sourcer).

### NOYAU_CERISE — Noyaux de cerise / CHERRY_PIT
- Famille : Coques & noyaux.
- Localisation : Provence (bassin cerisier du Midi), France — GPS (Global Positioning System) 44.00, 5.00, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : noyau dur, résidu de conserverie ou de distillation.
- Gisement [ILLUSTRATION (à sourcer FAOSTAT/agrestes)] : noyau ≈ 8 à 12 % de la masse de cerise ; production française de l'ordre de 30 000 à 40 000 t/an (à sourcer).
- Fenêtre saisonnière : juin-juil (récolte juin-juillet, conserveries en campagne).
- Techniques culturales, récolte, transformation : cerisaies ; récolte manuelle ou mécanique ; les noyaux sortent des conserveries et des distilleries.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [ILLUSTRATION] : non pertinent : le noyau sort de la conserverie (référence : constat).
- Traitement [À VÉRIFIER] : débouchés existants (charge de chaudière, anneaux de massage, artisanat) à documenter (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : la conserverie assume le dénoyautage ; le noyau est un déchet de process à évacuer (référence : à sourcer par conserverie).
- Main-d'œuvre [ILLUSTRATION] : dénoyautage mécanique en ligne (référence : constat).

### NOYAU_PECHE — Noyaux de pêche / PEACH_PIT
- Famille : Coques & noyaux.
- Localisation : Roussillon / Gard (bassins pêchers du Sud), France — GPS (Global Positioning System) 43.84, 4.36, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : noyau dur, résidu de conserverie.
- Gisement [ILLUSTRATION (à sourcer FAOSTAT/agrestes)] : noyau ≈ 6 à 10 % de la masse de pêche ; production française de l'ordre de 200 000 t/an (à sourcer).
- Fenêtre saisonnière : juin-juil-août (récolte juin à septembre selon variétés).
- Techniques culturales, récolte, transformation : vergers irrigués ; récolte manuelle en cagettes ; dénoyautage en conserverie.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [ILLUSTRATION] : non pertinent : le noyau sort de la conserverie (référence : constat).
- Traitement [À VÉRIFIER] : combustible et charbon actif : pistes à documenter (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : la conserverie assume le dénoyautage et l'évacuation (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : dénoyautage mécanique en ligne (référence : constat).

### NOYAU_ABRICOT — Noyaux d'abricot / APRICOT_PIT
- Famille : Coques & noyaux.
- Localisation : Roussillon (premier bassin abricotier français), France — GPS (Global Positioning System) 42.70, 2.90, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : noyau dur, résidu de conserverie.
- Gisement [ILLUSTRATION (à sourcer FAOSTAT/agrestes)] : Roussillon ≈ 80 % de la production française d'abricots (ordre) ; noyau ≈ 6 à 10 % de la masse.
- Fenêtre saisonnière : juin-juil (récolte juin-juillet, conserveries en campagne).
- Techniques culturales, récolte, transformation : vergers irrigués ; récolte manuelle ; dénoyautage en conserverie (amandes utilisées en confiserie, coques en résidu).
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [ILLUSTRATION] : non pertinent : le noyau sort de la conserverie (référence : constat).
- Traitement [À VÉRIFIER] : charbon actif et combustible : filières à documenter (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : la conserverie assume le dénoyautage et l'évacuation (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : dénoyautage mécanique en ligne (référence : constat).

### COQUE_MACADAMIA — Coques de macadamia / MACADAMIA_SHELL
- Famille : Coques & noyaux.
- Localisation : Queensland (Mareeba), Australie — GPS (Global Positioning System) -16.99, 145.42, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : coque très dure, résidu de décorticage.
- Gisement [ILLUSTRATION (à sourcer AMS)] : coque ≈ 60 à 70 % de la masse récoltée ; Australie de l'ordre de 50 000 t de noyaux/an (à sourcer).
- Fenêtre saisonnière : mars-avr-mai-juin-juil-août-sept-oct (récolte étalée mars-octobre (chute naturelle)).
- Techniques culturales, récolte, transformation : vergers irrigués ; récolte par ramassage au sol, décorticage mécanique en usine.
- Brûlage [À VÉRIFIER] : le brûlage des coques est courant en usine mais encadré par la réglementation australienne de l'air (référence : cadre état Queensland, à sourcer).
- Enfouissement [ILLUSTRATION] : non pertinent : la coque sort de l'usine (référence : constat).
- Traitement [À VÉRIFIER] : combustible d'usine établi (séchage des noix) : pratique industrielle à documenter (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : l'usine assume le décorticage ; la coque est un sous-produit valorisé en interne (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : décorticage mécanique continu (référence : constat).

### COQUE_PECAN — Coques de pacane / PECAN_SHELL
- Famille : Coques & noyaux.
- Localisation : Géorgie (Albany, premier bassin pacanier), États-Unis — GPS (Global Positioning System) 31.58, -84.13, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : coque dure, résidu de décorticage.
- Gisement [ILLUSTRATION (à sourcer USDA NASS)] : Géorgie de l'ordre de 60 à 70 millions de kg de pacanes/an (à sourcer USDA) ; coque ≈ 45 à 55 % de la masse.
- Fenêtre saisonnière : oct-nov-déc (récolte octobre-décembre (secouage mécanique)).
- Techniques culturales, récolte, transformation : vergers irrigués ; secoueuses, ramassage, séchage, décorticage en usine.
- Brûlage [À VÉRIFIER] : pratiqué localement mais de plus en plus contraint par les règles d'air de l'État (référence : règles GADNR/EPD, à sourcer).
- Enfouissement [ILLUSTRATION] : non pertinent : la coque sort de l'usine (référence : constat).
- Traitement [À VÉRIFIER] : mulch, litière et combustible : débouchés établis à documenter (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : l'usine assume le décorticage ; la coque est cédée à bas prix (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : décorticage mécanique continu en campagne (référence : constat).

### NOYAU_AVOCAT — Noyaux d'avocat / AVOCADO_PIT
- Famille : Coques & noyaux.
- Localisation : Michoacán (Uruapan, premier bassin avocatier mondial), Mexique — GPS (Global Positioning System) 19.41, -102.06, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : noyau dur, résidu des emballeurs (packings).
- Gisement [ILLUSTRATION (à sourcer SIAP/FAOSTAT)] : Michoacán ≈ 2 millions de t d'avocats/an (ordre, premier producteur mondial) ; noyau ≈ 15 à 25 % de la masse.
- Fenêtre saisonnière : oct-nov-déc-janv-févr (campagne principale octobre-février (export)).
- Techniques culturales, récolte, transformation : vergers en collines ; récolte manuelle, calibrage et emballage dans les packings, noyaux triés avec les sous-produits.
- Brûlage [À VÉRIFIER] : le brûlage des résidus de packing existe mais le cadre fédéral des déchets s'applique (référence : LGPGIR (loi générale prévention gestion intégrale résidus), à sourcer).
- Enfouissement [À VÉRIFIER] : enfouissement des résidus organiques dans les vergers, pratiqué (référence : à sourcer).
- Traitement [À VÉRIFIER] : compostage industriel en développement dans les packings (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : le packing assume l'évacuation des sous-produits (obligation sanitaire et environnementale croissante) (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : récolte et tri très manuels : poste dominant (ordre de grandeur, centaines d'heures/ha/an) (référence : littérature avocatière).

### PAILLE_BLE — Paille de blé / WHEAT_STRAW
- Famille : Céréales.
- Localisation : Beauce (grenier à blé), France — GPS (Global Positioning System) 48.44, 1.49, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : paille de céréale, résidu de moisson.
- Gisement [ILLUSTRATION (à sourcer FAOSTAT v0.9)] : France : blé de l'ordre de 30 millions de t/an (FAOSTAT-sourçable via le pipeline v0.9) ; paille ≈ 0,8 à 1,2 fois le grain (ratio).
- Fenêtre saisonnière : juil-août (moisson juillet-août).
- Techniques culturales, récolte, transformation : culture de blé tendre et dur ; moissonneuse-batteuse, pressage des ballots au champ ou broyage-enfouissement.
- Brûlage [DONNÉES RÉELLES] : brûlage des chaumes interdit à l'air libre (biodéchets), dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [À VÉRIFIER] : broyage-enfouissement pratiqué pour la fertilité, partiellement valorisé en litière et paillage (référence : pratique standard, à sourcer chambre d'agriculture).
- Traitement [À VÉRIFIER] : litière animale, méthanisation, paillage : filières établies, la valorisation thermo-chimique reste marginale (référence : à sourcer).
- Coût pour l'agriculture [ILLUSTRATION] : le pressage et l'andainage coûtent sans recette certaine (ordre : 20 à 40 €/t pressée) (référence : à sourcer par exploitation).
- Main-d'œuvre [ILLUSTRATION] : quelques dizaines de minutes/ha en presse à grosse balle (ordre de grandeur) (référence : littérature céréalière).

### PAILLE_RIZ — Paille de riz / RICE_STRAW
- Famille : Céréales.
- Localisation : Camargue (rizicultures du delta), France — GPS (Global Positioning System) 43.70, 4.30, approximation de région, pas un cadastre. Point : hub existant.
- Flotte monde.py : >fr-rhone→ paille-riz< (fr-rhone).
- Bassin ERA5 (European Reanalysis v5) : camargue.
- Type de biomasse : paille de riz, résidu de récolte, salifère.
- Gisement [SOURCÉ (FAOSTAT v0.9) ; ratio ILLUSTRATION] : France : 71 960 t de riz paddy en 2024 (FAOSTAT v0.9) ; paille ≈ 0,7 à 1,2 fois le paddy (ratio).
- Fenêtre saisonnière : oct-nov-déc (récolte octobre-novembre, fenêtre moteur [10, 11, 12] (pain point historique : le brûlage camarguais)).
- Techniques culturales, récolte, transformation : riziculture inondée, moissonneuse-batteuse ; la paille reste au champ, broyée, enfouie ou brûlée.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare ; le brûlage camarguais persiste en dérogation encadrée (référence : Art. L.541-21-1 ; feux réels FIRMS Camargue (fiches v0.6)).
- Enfouissement [À VÉRIFIER] : broyage-enfouissement pratiqué mais difficile (litière saline, sol asphyxié) (référence : pratique à sourcer).
- Traitement [À VÉRIFIER] : litière, méthanisation, valorisation énergétique : pistes à documenter (référence : à sourcer).
- Coût pour l'agriculture [DONNÉES RÉELLES] : l'évacuation de la paille conditionne la préparation de la campagne suivante : contrainte forte et datée (référence : contrainte agronomique, fiche pilote v0).
- Main-d'œuvre [ILLUSTRATION] : une à deux passes de broyeur ou d'andaineur par hectare (ordre de grandeur) (référence : à sourcer).

### RAFLE_MAIS — Rafles de maïs / MAIZE_COB
- Famille : Céréales.
- Localisation : Sud-Ouest / Aquitaine (bassin maïsiculture), France — GPS (Global Positioning System) 43.89, -0.50, approximation de région, pas un cadastre. Point : hub existant.
- Flotte monde.py : >fr-rhone→ mais-rdm< (fr-rhone).
- Bassin ERA5 (European Reanalysis v5) : sud-ouest.
- Type de biomasse : rafle (épi dépouillé), résidu de récolte du maïs.
- Gisement [SOURCÉ (FAOSTAT v0.9) ; ratio ILLUSTRATION] : France : 14 670 620 t de maïs grain en 2024 (FAOSTAT v0.9) ; rafle ≈ 15 % de l'épi (ratio).
- Fenêtre saisonnière : oct-nov-déc (récolte octobre-décembre, fenêtre moteur [10, 11, 12]).
- Techniques culturales, récolte, transformation : maïsiculture irriguée ; moissonneuse-batteuse, séchage en coopérative, rafles séparées au tri.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [À VÉRIFIER] : broyage-enfouissement des cannes et rafles pratiqué pour la fertilité (référence : pratique standard, à sourcer).
- Traitement [À VÉRIFIER] : litière, lit de volaille, combustible : débouchés locaux à documenter (référence : à sourcer).
- Coût pour l'agriculture [ILLUSTRATION] : le tri coopératif assume la séparation ; la rafle est un sous-produit à faible valeur (référence : à sourcer par coopérative).
- Main-d'œuvre [ILLUSTRATION] : aucune main-d'œuvre dédiée : la rafle suit le flux de séchage (référence : constat).

### TIGE_TOURNESOL — Tiges de tournesol / SUNFLOWER_STALK
- Famille : Céréales.
- Localisation : Poitou (bassin tournesol non irrigué), France — GPS (Global Positioning System) 46.58, 0.34, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : tige sèche creuse, résidu de récolte.
- Gisement [ILLUSTRATION (à sourcer FAOSTAT/agrestes)] : France : tournesol de l'ordre de 1,3 à 1,7 million de t/an (à sourcer) ; tiges ≈ 2 à 3 t/ha (ratio).
- Fenêtre saisonnière : sept-oct (récolte septembre-octobre).
- Techniques culturales, récolte, transformation : culture de printemps ; moisson à maturité, tiges broyées ou laissées debout puis enfouies.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [À VÉRIFIER] : broyage-enfouissement pratiqué pour la fertilité (référence : pratique standard, à sourcer).
- Traitement [À VÉRIFIER] : valorisation marginale ; la paille de tournesol reste surtout enfouie (référence : à sourcer).
- Coût pour l'agriculture [ILLUSTRATION] : une passe de broyeur par hectare entre deux cultures (ordre : 15 à 30 €/ha) (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : demi-heure à une heure/ha de broyage (ordre de grandeur) (référence : littérature).

### TIGE_COLZA — Pailles de colza / RAPE_STALK
- Famille : Céréales.
- Localisation : Beauce / Orléanais (bassin colza), France — GPS (Global Positioning System) 47.90, 1.90, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : paille de colza, résidu de récolte.
- Gisement [ILLUSTRATION (à sourcer FAOSTAT/agrestes)] : France : colza de l'ordre de 3 à 4 millions de t/an (à sourcer) ; paille ≈ 2 à 4 t/ha (ratio).
- Fenêtre saisonnière : juil-août (moisson juillet-août).
- Techniques culturales, récolte, transformation : culture d'hiver ; moissonneuse-batteuse, paille pressée pour litière ou enfouie.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [À VÉRIFIER] : broyage-enfouissement pratiqué pour la fertilité (référence : pratique standard, à sourcer).
- Traitement [À VÉRIFIER] : litière animale établie ; méthanisation en développement (référence : à sourcer).
- Coût pour l'agriculture [ILLUSTRATION] : pressage ou broyage à la charge de l'exploitant (ordre : 20 à 40 €/t pressée) (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : quelques dizaines de minutes/ha en presse (ordre de grandeur) (référence : littérature).

### CHENEVOTTE — Chènevotte de chanvre / HEMP_HURD
- Famille : Céréales.
- Localisation : Champagne (Aube, premier bassin chanvre), France — GPS (Global Positioning System) 48.19, 4.71, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : moelle ligneuse défibrée du chanvre.
- Gisement [ILLUSTRATION (à sourcer InterChanvre)] : France : chanvre industriel de l'ordre de 10 000 à 15 000 ha/an (à sourcer) ; chènevotte ≈ 50 à 60 % de la tige défibrée.
- Fenêtre saisonnière : sept-oct (récolte septembre-octobre, défibrage ensuite).
- Techniques culturales, récolte, transformation : semis dense, récolte à l'automne, rouissage au champ, teillage en usine : fibre d'un côté, chènevotte de l'autre.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [ILLUSTRATION] : non pertinent : la chènevotte sort du teillage (référence : constat).
- Traitement [À VÉRIFIER] : litière animale (couchage cheval) : débouché établi (référence : filière chanvre française, à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : l'usine de teillage assume le sous-produit ; la chènevotte est cédée ou stockée (référence : à sourcer par usine).
- Main-d'œuvre [ILLUSTRATION] : teillage mécanique continu (référence : constat).

### PAILLE_LIN — Paille de lin / FLAX_STRAW
- Famille : Céréales.
- Localisation : Normandie (bassin lin teillé), France — GPS (Global Positioning System) 49.85, 0.85, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : paille de lin, résidu du teillage (anas de lin).
- Gisement [ILLUSTRATION (à sourcer CIPALIN)] : France : lin fibre de l'ordre de 60 000 à 100 000 ha/an, premier producteur mondial (à sourcer) ; anas ≈ 50 % de la paille teillée.
- Fenêtre saisonnière : juil-août-sept (arrachage juillet-août, rouissage, teillage automne-hiver).
- Techniques culturales, récolte, transformation : arrachage, rouissage au champ, rentrée en balles, teillage : fibre longue, lin à papier et anas en sous-produits.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [ILLUSTRATION] : non pertinent : l'anas sort du teillage (référence : constat).
- Traitement [À VÉRIFIER] : panneaux, litière, plaquettes : débouchés établis (référence : filière linière, à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : le teilleur assume l'anas ; cédé à bas prix à l'industrie panneautière (référence : à sourcer par teillage).
- Main-d'œuvre [ILLUSTRATION] : teillage mécanique continu en campagne (référence : constat).

### TIGE_SORGHO — Tiges de sorgho / SORGHUM_STALK
- Famille : Céréales.
- Localisation : Sud-Ouest / Midi toulousain, France — GPS (Global Positioning System) 43.60, 1.44, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : tige sèche, résidu de récolte.
- Gisement [ILLUSTRATION (à sourcer agrestes)] : France : sorgho de l'ordre de 30 000 à 50 000 ha/an (à sourcer) ; tiges ≈ 3 à 6 t/ha (ratio).
- Fenêtre saisonnière : sept-oct (récolte septembre-octobre).
- Techniques culturales, récolte, transformation : culture de printemps non irriguée ou irriguée ; moisson, tiges broyées ou pâturées.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [À VÉRIFIER] : broyage-enfouissement pratiqué pour la fertilité (référence : pratique standard, à sourcer).
- Traitement [À VÉRIFIER] : litière et fourrage résiduel : valorisations locales à documenter (référence : à sourcer).
- Coût pour l'agriculture [ILLUSTRATION] : une passe de broyeur par hectare (ordre : 15 à 30 €/ha) (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : demi-heure à une heure/ha de broyage (ordre de grandeur) (référence : littérature).

### BALLE_AVOINE — Balles d'avoine / OAT_HUSK
- Famille : Céréales.
- Localisation : Bretagne (bassin avoine fourragère), France — GPS (Global Positioning System) 48.47, -2.50, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : balle (enveloppe du grain), résidu de décortication.
- Gisement [ILLUSTRATION (à sourcer FAOSTAT)] : France : avoine de l'ordre de 2 à 3 millions de t/an (à sourcer) ; balle ≈ 20 à 30 % du grain décortiqué.
- Fenêtre saisonnière : août-sept (moisson août-septembre, décortication ensuite).
- Techniques culturales, récolte, transformation : culture d'hiver ou de printemps ; moisson, décortication en atelier ou coopérative.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [ILLUSTRATION] : non pertinent : la balle sort de l'atelier (référence : constat).
- Traitement [À VÉRIFIER] : litière animale établie ; valorisation énergétique marginale (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : l'atelier assume le sous-produit ; la balle est cédée en litière (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : décortication mécanique continue (référence : constat).

### TIGE_COTON — Racines et tiges de coton (surge) / COTTON_STALK
- Famille : Céréales.
- Localisation : Pendjab (Ludhiana, rotations coton-riz), Inde — GPS (Global Positioning System) 30.90, 75.86, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : tige ligneuse arrachée après récolte du coton.
- Gisement [ILLUSTRATION (à sourcer PAU/ministère indien)] : Pendjab : coton de l'ordre de 300 000 à 500 000 ha/an (à sourcer) ; tiges ≈ 2 à 3 t/ha (ratio).
- Fenêtre saisonnière : oct-nov-déc (arrachage des plants octobre-décembre, avant le semis du blé).
- Techniques culturales, récolte, transformation : culture de mousson (kharif) ; récolte du kapok manuelle, plants arrachés à la main ou à la charrue.
- Brûlage [À VÉRIFIER] : le brûlage des tiges et racines est restreint mais reste pratiqué ; la crise régionale du brûlage (pailles de riz) sert de précédent réglementaire (référence : directions CAAP 2019 (tribunal de Delhi) ; amendes PCA/PPCB — à re-vérifier).
- Enfouissement [À VÉRIFIER] : l'enfouissement des tiges est encouragé par les programmes agricoles (promotion du semis direct) (référence : à sourcer).
- Traitement [À VÉRIFIER] : valorisation énergétique marginale aujourd'hui ; gisement massif à l'échelle du Pendjab (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : l'arrachage est un coût obligatoire entre deux cultures (monoculture interdite : le blé suit) (référence : rotation documentée, à re-vérifier).
- Main-d'œuvre [ILLUSTRATION] : l'arrachage est manuel et coûteux : plusieurs dizaines d'heures/ha (ordre de grandeur) (référence : littérature agronomique indienne).

### BAGASSE_CANNE — Bagasse de canne à sucre / SUGARCANE_BAGASSE
- Famille : Tropical.
- Localisation : São Paulo (Ribeirão Preto, cœur sucrier), Brésil — GPS (Global Positioning System) -21.18, -47.81, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : fibres de canne après broyage (gisement massif, humide).
- Gisement [ILLUSTRATION (à sourcer FAOSTAT/UNICA)] : monde : plus de 1,8 milliard de t/an de bagasse (atlas V3, ordre) ; Brésil ≈ la moitié de la canne mondiale.
- Fenêtre saisonnière : mai-juin-juil-août-sept-oct-nov (safra mai-novembre (broyage quotidien des usines)).
- Techniques culturales, récolte, transformation : récolte mécanisée croissante sans brûlage pré-récolte ; broyage à l'usine, bagasse déjà partiellement valorisée en chaudière.
- Brûlage [À VÉRIFIER] : fin programmée du brûlage pré-récolte dans l'État de São Paulo (échéances selon la pente) (référence : Lei estadual 11.241/2002, à re-vérifier).
- Enfouissement [À VÉRIFIER] : la paille (trash) laissée au champ est de plus en plus maintenue en paillage (référence : pratique à sourcer).
- Traitement [À VÉRIFIER] : la bagasse alimente déjà les chaudières sucrières : co-génération établie, surplus disponible (référence : filière UNICA, à sourcer).
- Coût pour l'agriculture [ILLUSTRATION] : l'usine assume la logistique ; la bagasse excédentaire est un sous-produit quasi gratuit à la porte de l'usine (référence : à sourcer par usine).
- Main-d'œuvre [ILLUSTRATION] : flux continu à la porte de l'usine : aucun andainage agricole nécessaire (cas d'école logistique) (référence : constat).

### BALLE_RIZ — Balles de riz (balle blanche) / RICE_HUSK
- Famille : Tropical.
- Localisation : Camargue (rizicultures du delta, rizeries locales), France — GPS (Global Positioning System) 43.70, 4.30, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : camargue.
- Type de biomasse : enveloppe du paddy, résidu de rizerie, abrasive.
- Gisement [SOURCÉ (FAOSTAT v0.9) ; ratio ILLUSTRATION] : France : 71 960 t de riz paddy 2024 (FAOSTAT v0.9) ; balle ≈ 20 % du paddy (ratio).
- Fenêtre saisonnière : oct-nov-déc (usinage après récolte, flux continu de la rizerie).
- Techniques culturales, récolte, transformation : riziculture, séchage puis décorticage en rizerie ; la balle sort en vrac du premier passage.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [ILLUSTRATION] : non pertinent : la balle sort de la rizerie (référence : constat).
- Traitement [À VÉRIFIER] : litière et combustible de rizerie : débouchés locaux à documenter (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : la rizerie assume le sous-produit ; la balle est un débit de process continu (référence : à sourcer par rizerie).
- Main-d'œuvre [ILLUSTRATION] : aucune main-d'œuvre dédiée : flux mécanique continu (référence : constat).

### DECHET_DATTIER — Résidus de dattier (palmes d'élagage) / DATE_PALM_RESIDUE
- Famille : Tropical.
- Localisation : Al-Qassim (oasis dattière), Arabie Saoudite — GPS (Global Positioning System) 26.33, 43.97, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : palmes et stipes d'élagage, ligneux fibreux.
- Gisement [ILLUSTRATION (à sourcer FAOSTAT/GSCA)] : Arabie : dattes de l'ordre de 1,5 million de t/an (à sourcer) ; résidus d'élagage ≈ 20 à 40 kg/arbre/an (ratio).
- Fenêtre saisonnière : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc (élagage continu, pics printemps et automne).
- Techniques culturales, récolte, transformation : palmeraies datte ; émondage manuel des palmes sèches, mise en andains ou brûlage traditionnel.
- Brûlage [À VÉRIFIER] : le brûlage des palmes reste courant ; le cadre environnemental national le contraint progressivement (référence : centre national de conformité environnementale, à sourcer).
- Enfouissement [À VÉRIFIER] : non pratiqué : matériau ligneux volumineux, plutôt broyé en paillage (référence : à sourcer).
- Traitement [À VÉRIFIER] : broyage en paillage ou valorisation énergétique : pistes à documenter (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : l'émondage est un coût obligatoire du dattier (sanitaire) ; l'évacuation des palmes est un surcoût (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : émondage manuel à la scie d'élagage : plusieurs heures par arbre et par an (ordre de grandeur) (référence : littérature phœnicicole).

### NOYAU_DATTE — Noyaux de datte / DATE_PIT
- Famille : Tropical.
- Localisation : Al-Qassim (unités de conditionnement), Arabie Saoudite — GPS (Global Positioning System) 26.33, 43.97, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : noyau dur, résidu des unités de conditionnement.
- Gisement [ILLUSTRATION (à sourcer FAOSTAT)] : noyau ≈ 10 à 15 % de la datte ; Arabie ≈ 1,5 million de t de dattes/an (à sourcer).
- Fenêtre saisonnière : août-sept-oct (campagne de récolte des dattes août-octobre (khalal à tamr)).
- Techniques culturales, récolte, transformation : récolte par régimes, conditionnement et tri dans les unités ; les noyaux sortent des lignes de calibrage et de dénoyautage.
- Brûlage [ILLUSTRATION] : non pertinent au champ : noyau d'atelier (référence : constat).
- Enfouissement [ILLUSTRATION] : non pertinent : noyau d'atelier (référence : constat).
- Traitement [À VÉRIFIER] : farine de noyau (aliment bétail) existante ; valorisation énergétique à documenter (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : l'unité de conditionnement assume le dénoyautage ; le noyau est un débit de process (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : dénoyautage mécanique en ligne (référence : constat).

### RAFFLE_PALMIER — Rafles de régime de palmier à huile / PALM_RACHIS
- Famille : Tropical.
- Localisation : Johor (bassin huile de palme), Malaisie — GPS (Global Positioning System) 1.94, 102.90, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : rachis de régime, résidu d'usine (empty fruit bunch).
- Gisement [ILLUSTRATION (à sourcer MPOB)] : Malaisie : de l'ordre de 100 millions de t/an de résidus palmier tous flux (à sourcer) ; rafles ≈ 20 à 25 t/ha/an (ratio).
- Fenêtre saisonnière : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc (production continue, pics lors des replantations).
- Techniques culturales, récolte, transformation : récolte des régimes toute l'année ; l'usine sépare fruits et rafles (stérilisation, égrappage) ; compostage partiel.
- Brûlage [À VÉRIFIER] : le brûlage des résidus de replantation est restreint (lutte contre la brume transfrontière) (référence : accord ASEAN sur la brume transfrontière ; licences MPOB — à re-vérifier).
- Enfouissement [À VÉRIFIER] : compostage et épandage en plantation pratiqués (référence : à sourcer).
- Traitement [À VÉRIFIER] : combustible de chaudière d'usine et compost : filières établies à documenter (référence : à sourcer).
- Coût pour l'agriculture [ILLUSTRATION] : l'usine assume le flux ; la rafle est un débit de process quasi gratuit à la porte (référence : à sourcer par usine).
- Main-d'œuvre [ILLUSTRATION] : flux continu à la porte de l'usine (cas d'école logistique, comme la bagasse) (référence : constat).

### TIGE_BANANIER — Pseudotroncs de bananier / BANANA_PSEUDOSTEM
- Famille : Tropical.
- Localisation : Machala (premier bassin bananier d'exportation), Équateur — GPS (Global Positioning System) -3.26, -79.96, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : pseudotronc très humide, rejet de la récolte.
- Gisement [ILLUSTRATION (à sourcer FAOSTAT/CNB)] : pseudotroncs ≈ 30 à 50 t/ha/an de matière fraîche (ratio) ; Équateur : premier exportateur mondial de bananes.
- Fenêtre saisonnière : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc (récolte continue, rejets hebdomadaires).
- Techniques culturales, récolte, transformation : plantations mestizas ; coupe des régimes, pseudotroncs abattus et laissés au rang ou hachés (fertilisation).
- Brûlage [À VÉRIFIER] : peu pratiqué : matériau humide ; le brûlage agricole est néanmoins encadré par la loi de gestion environnementale (référence : Ley de Gestión Ambiental (Équateur), à sourcer).
- Enfouissement [À VÉRIFIER] : hachage-enfouissement au rang, pratique dominante documentée (référence : à sourcer).
- Traitement [À VÉRIFIER] : valorisations (fibres, compost) marginales à documenter (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : l'abattage du pseudotronc est un geste cultural obligatoire (cycle de rejets) (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : geste manuel à chaque passage de récolte (ordre : minutes/planche) (référence : littérature bananière).

### FEUILLE_ANANAS — Feuilles d'ananas (résidus de récolte) / PINEAPPLE_LEAF
- Famille : Tropical.
- Localisation : Cebu (zone ananas traditionnelle), Philippines — GPS (Global Positioning System) 10.31, 123.90, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : feuille longue fibreuse, résidu de récolte.
- Gisement [ILLUSTRATION (à sourcer DA-Philippines)] : feuilles ≈ 3 à 6 t/ha/cycle en matière sèche (ratio) ; Philippines : bassin ananas et fibre piña établi.
- Fenêtre saisonnière : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc (récolte étalée toute l'année (cycles de 18 à 24 mois par parcelle)).
- Techniques culturales, récolte, transformation : culture en dams, récolte manuelle des fruits, feuilles coupées ou laissées au champ (décomposition lente).
- Brûlage [À VÉRIFIER] : le brûlage des feuilles d'ananas après récolte est courant mais contraint par la loi sur les déchets solides (référence : RA 9003 (Ecological Solid Waste Management Act), à sourcer).
- Enfouissement [À VÉRIFIER] : l'enfouissement des feuilles est encouragé pour la fertilité (référence : à sourcer).
- Traitement [À VÉRIFIER] : la fibre piña (textile) valorise une part minime ; le gisement reste massivement au champ (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : le nettoyage de la parcelle après récolte est un coût obligatoire du cycle (replantation) (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : nettoyage manuel à la machette : plusieurs dizaines d'heures/ha (ordre de grandeur) (référence : littérature).

### CABOSSE_CACAO — Cabosses de cacao (coques vides) / CACAO_POD
- Famille : Tropical.
- Localisation : Daloa (premier bassin cacaoyer mondial), Côte d'Ivoire — GPS (Global Positioning System) 6.88, -6.45, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : coque de cabosse, résidu d'écabossage au champ.
- Gisement [ILLUSTRATION (à sourcer FAOSTAT/CCC)] : Côte d'Ivoire ≈ 2 millions de t de fèves/an, premier producteur mondial (à sourcer) ; cabosses ≈ 10 fois la masse des fèves en matière fraîche (ratio).
- Fenêtre saisonnière : janv-févr-mars-mai-juin-juil-oct-nov-déc (deux campagnes (octobre-mars, mai-août), écabossage au champ le jour de la cueillette).
- Techniques culturales, récolte, transformation : cacaoyères villageoises ; cueillette, écabossage manuel au champ, fermentation des fèves, les coques restent au pied des arbres.
- Brûlage [À VÉRIFIER] : le brûlage des coques est pratiqué ponctuellement ; le cadre des déchets agricoles est à re-vérifier (référence : code de l'environnement ivoirien, à sourcer).
- Enfouissement [À VÉRIFIER] : les coques sont épandues au pied des cacaoyers (compostage de fait) (référence : pratique à sourcer).
- Traitement [À VÉRIFIER] : valorisation marginale (compost, biochar artisanal) à documenter (référence : à sourcer).
- Coût pour l'agriculture [ILLUSTRATION] : l'écabossage est un geste obligatoire de la récolte ; aucun surcoût dédié (référence : constat).
- Main-d'œuvre [ILLUSTRATION] : écabossage manuel au machette : minutes par cabosse, poste dominant à la récolte (référence : littérature cacaoyère).

### FIBRE_COCO — Balle de coco (fibre et poussière) / COCO_COIR
- Famille : Tropical.
- Localisation : Davao (bassin coco), Philippines — GPS (Global Positioning System) 7.19, 125.46, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : balle (épicarpe et mésocarpe), résidu de décortication.
- Gisement [ILLUSTRATION (à sourcer PCA/FAOSTAT)] : balle ≈ 25 à 35 % du fruit ; Philippines : noix de coco de l'ordre de 14 millions de t/an (à sourcer).
- Fenêtre saisonnière : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc (récolte continue (cycle par arbre de 45 à 60 jours)).
- Techniques culturales, récolte, transformation : cocoteraies ; récolte des noix, décorticage en usine de fibre (coir) : fibre, poussière (coco peat) et résidus.
- Brûlage [À VÉRIFIER] : le brûlage des balles et bourres est restreint par la loi sur les déchets solides (référence : RA 9003 (Philippines), à sourcer).
- Enfouissement [À VÉRIFIER] : la poussière de coco est valorisée en substrat : filière établie (référence : à sourcer).
- Traitement [À VÉRIFIER] : filière coir établie (géotextiles, substrats) : part valorisée, gisement résiduel à documenter (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : l'usine de décorticage assume la balle ; le coprah reste le produit principal (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : récolte manuelle par gaffe : geste continu (ordre : minutes par arbre) (référence : littérature).

### MARC_CAFE — Marc de café (pulpe et mucilage) / SPENT_COFFEE_GROUNDS
- Famille : Tropical.
- Localisation : Tay Nguyen (Buôn Ma Thuột, capitale du robusta), Viêt Nam — GPS (Global Positioning System) 12.67, 108.06, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : pulpe et mucilage de la voie humide, résidu très humide.
- Gisement [ILLUSTRATION (à sourcer FAOSTAT/VICofa)] : Viêt Nam ≈ 1,7 million de t de café/an, deuxième producteur mondial (à sourcer) ; pulpe ≈ 40 à 45 % de la cerise fraîche (ratio).
- Fenêtre saisonnière : nov-déc-janv-févr (récolte du café novembre-février (sèche après)).
- Techniques culturales, récolte, transformation : caféiers robusta sur les hauts plateaux ; dépulpage en voie humide à la ferme ou au collecteur, séchage des parchment.
- Brûlage [À VÉRIFIER] : le brûlage des pulpes est ponctuel ; la réglementation des déchets de dépulpage se durcit (déversements dans les rivières interdits) (référence : réglementation vietnamienne des déchets, à sourcer).
- Enfouissement [À VÉRIFIER] : compostage des pulpes pratiqué de façon croissante (référence : à sourcer).
- Traitement [À VÉRIFIER] : compost et biogaz : pistes à documenter (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : le dépulpage est un geste obligatoire de la voie humide ; la pulpe est un débit de process (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : dépulpage mécanique à la ferme, manuel au tri (référence : littérature caféière).

### RESIDU_AGAVE — Bagasse d'agave (residuos de la jima) / AGAVE_RESIDUE
- Famille : Tropical.
- Localisation : Jalisco (Tequila, bassin de l'agave bleu), Mexique — GPS (Global Positioning System) 20.90, -103.84, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : fibres de piña cuite après distillation.
- Gisement [ILLUSTRATION (à sourcer CRT/FAOSTAT)] : Jalisco : agaves de l'ordre de 1 à 2 millions de t/an pour la tequila (à sourcer) ; bagasse ≈ 30 à 40 % de la piña cuite (ratio).
- Fenêtre saisonnière : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc (jima (récolte) et distillation étalées sur l'année).
- Techniques culturales, récolte, transformation : agaves bleus mûris 6 à 8 ans ; jima manuelle (coa), cuisson des piñas, broyage, fermentation et distillation dans les tequileras.
- Brûlage [À VÉRIFIER] : la bagasse d'agave est souvent brûlée ou abandonnée ; le cadre fédéral des résidus s'applique (référence : LGPGIR (Mexique), à sourcer).
- Enfouissement [À VÉRIFIER] : abandon en andains non réglementé constaté historiquement (référence : à sourcer).
- Traitement [À VÉRIFIER] : compostage et valorisation énergétique en développement à documenter (référence : à sourcer CRT).
- Coût pour l'agriculture [ILLUSTRATION] : la distillerie assume le flux ; la bagasse est un débit de process à la porte (cas d'école logistique) (référence : à sourcer par tequilera).
- Main-d'œuvre [ILLUSTRATION] : la jima est très manuelle (jimadores) : poste dominant (ordre : minutes par piña) (référence : littérature agavère).

### TIGE_BAMBOU — Débris de bambou (coupes) / BAMBOO_CULM
- Famille : Tropical.
- Localisation : Anji (Zhejiang, capitale du bambou), Chine — GPS (Global Positioning System) 30.68, 119.68, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : débris de coupe et vieilles chaumes, ligneux à croissance rapide.
- Gisement [ILLUSTRATION (à sourcer Anji/FAO)] : débris d'exploitation ≈ 20 à 30 % de la coupe (ratio) ; Anji : de l'ordre de 60 000 ha de bambouseraies (à sourcer).
- Fenêtre saisonnière : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc (campagnes de coupe échelonnées (chaumes mûrs et dépérissants)).
- Techniques culturales, récolte, transformation : bambouseraies de moso ; coupe sélective des chaumes mûrs, débit en usines de planches et panifications.
- Brûlage [À VÉRIFIER] : le brûlage des débris de coupe est interdit ou restreint localement (pollution de l'air, feux de forêt) (référence : règles locales du Zhejiang, à sourcer).
- Enfouissement [À VÉRIFIER] : les débris sont souvent laissés en litière de bambouseraie (mulch) (référence : à sourcer).
- Traitement [À VÉRIFIER] : filière de transformation du bambou établie ; les débris restent sous-valorisés (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : la coupe est obligatoire (santé du massif) ; les débris sont un débit de coupe (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : coupe manuelle à la scie : heures par quartier de coupe (ordre de grandeur) (référence : littérature sylvicole).

### RESIDU_YERBA_MATE — Résidus de yerba mate (palos y palada) / YERBA_MATE_RESIDUE
- Famille : Tropical — statut À MESURER (addendum du 10/10/2026).
- Localisation : Misiones (cœur yerbatiero), Argentine — GPS (Global Positioning System) -27.45, -54.95, approximation de région, pas un cadastre. Point : hub existant.
- Flotte monde.py : >ar-misiones→ yerba-mate< (ar-misiones).
- Bassin ERA5 (European Reanalysis v5) : argentine-misiones.
- Type de biomasse : tiges et feuilles de taille, résidus de séchage (barbacuá).
- Gisement [SOURCÉ (INYM / fiche v0.6)] : Argentine : 986 738 t de feu verte en 2024 (INYM) ; environ 210 000 ha de yerba mate, 87 % à Misiones (fiche v0.6).
- Fenêtre saisonnière : avr-mai-juin-sept-oct-nov (fenêtre moteur exacte de monde.py (mois moyens et fins de campagne, hémisphère Sud)).
- Techniques culturales, récolte, transformation : plantations sous ombre ou plein soleil ; taille et récolte manuelles, séchage en séchoirs à bandes, les palos sortent du tri des moulins.
- Brûlage [DONNÉES RÉELLES] : autorisation préalable obligatoire pour toute quema, résidus de yerba mate inclus (référence : Ley nationale 26.562 (fiche v0.6)).
- Enfouissement [À VÉRIFIER] : les palos et palada sont plutôt compostés ou laissés au champ (référence : pratique à sourcer INYM).
- Traitement [À VÉRIFIER] : compost et combustible de séchoir : pistes à documenter (référence : à sourcer par secadero).
- Coût pour l'agriculture [À VÉRIFIER] : la taille est un coût obligatoire du yerbal ; les résidus sont un débit de séchoir (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : récolte manuelle dominante (tareferos) : très laborieuse (ordre : centaines d'heures/ha/an) (référence : littérature yerbatière).

### GRAINE_PAPAYE — Graines de papaye / PAPAYA_SEEDS
- Famille : Tropical — statut À MESURER (addendum du 10/10/2026).
- Localisation : Espírito Santo (bassin mamão), Brésil — GPS (Global Positioning System) -20.30, -40.34, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : graines et résidus de conserverie de papaye.
- Gisement [ILLUSTRATION (à sourcer FAOSTAT/IBGE)] : graines ≈ 10 à 15 % du fruit ; Brésil : papaye de l'ordre de 1 million de t/an, premier producteur mondial (à sourcer).
- Fenêtre saisonnière : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc (production continue (culture pérenne de cycle court)).
- Techniques culturales, récolte, transformation : plantations irriguées, récolte manuelle continue, conserveries et juiceries en flux.
- Brûlage [ILLUSTRATION] : non pertinent : résidu d'usine (référence : constat).
- Enfouissement [ILLUSTRATION] : non pertinent : résidu d'usine (référence : constat).
- Traitement [À VÉRIFIER] : valorisations marginales à documenter (compost, extraits) (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : l'usine assume l'évacuation des graines et peaux (obligation de gestion des résidus) (référence : loi 12.305/2010 (PNRS Brésil), à sourcer).
- Main-d'œuvre [ILLUSTRATION] : récolte manuelle continue (poste dominant) (référence : littérature).

### SCIURE_PIN — Sciure de pin / PINE_SAWDUST
- Famille : Forestier.
- Localisation : Landes de Gascogne (massif pin maritime), France — GPS (Global Positioning System) 44.40, -0.80, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : sciure de scierie, résidu sec.
- Gisement [ILLUSTRATION (à sourcer CNPF/filière bois)] : sciure ≈ 5 à 10 % du bois entrant en scierie (ratio) ; massif landais ≈ 1 million de ha de pin maritime (à sourcer).
- Fenêtre saisonnière : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc (flux continu des scieries).
- Techniques culturales, récolte, transformation : sylviculture de pin maritime, exploitations et scieries locales ; la sciure est aspirée au poste de débit.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare ; le brûlage des déchets de scierie est fermé (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [ILLUSTRATION] : non pertinent : résidu d'atelier (référence : constat).
- Traitement [À VÉRIFIER] : panneaux et litière établis ; valorisation énergétique des chaudières bois (référence : filière bois française, à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : hors agriculture : la scierie cède ou assume la sciure selon les débouchés (référence : à sourcer par scierie).
- Main-d'œuvre [ILLUSTRATION] : aucune main-d'œuvre dédiée : flux mécanique continu (référence : constat).

### SCIURE_CHENE — Sciure de chêne / OAK_SAWDUST
- Famille : Forestier.
- Localisation : France nord (scieries de chêne), France — GPS (Global Positioning System) 48.00, 2.00, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : sciure de scierie, résidu sec.
- Gisement [ILLUSTRATION (à sourcer filière bois)] : sciure ≈ 5 à 10 % du bois entrant en scierie (ratio) ; le chêne est la première essence de feuillu française.
- Fenêtre saisonnière : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc (flux continu des scieries).
- Techniques culturales, récolte, transformation : exploitations feuillues, merrains de tonnellerie, scieries de chêne.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [ILLUSTRATION] : non pertinent : résidu d'atelier (référence : constat).
- Traitement [À VÉRIFIER] : panneaux et combustible : débouchés établis (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : hors agriculture : la scierie cède ou assume la sciure (référence : à sourcer par scierie).
- Main-d'œuvre [ILLUSTRATION] : aucune main-d'œuvre dédiée : flux mécanique continu (référence : constat).

### ECORCE_PIN — Écorces de pin / PINE_BARK
- Famille : Forestier.
- Localisation : Landes de Gascogne, France — GPS (Global Positioning System) 44.40, -0.80, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : écorce de grume, résidu d'exploitation.
- Gisement [ILLUSTRATION (à sourcer filière bois)] : écorce ≈ 10 à 15 % de la grume (ratio) ; massif landais ≈ 1 million de ha de pin maritime (à sourcer).
- Fenêtre saisonnière : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc (flux continu des scieries (déroguage)).
- Techniques culturales, récolte, transformation : exploitations de pin maritime ; déroguage en scierie, écorce en vrac.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [À VÉRIFIER] : paillage forestier pratiqué (référence : à sourcer).
- Traitement [À VÉRIFIER] : paillage horticole établi ; combustible possible (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : hors agriculture : la scierie assume l'écorce (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : aucune main-d'œuvre dédiée : flux mécanique continu (référence : constat).

### ECORCE_EUCALYPTUS — Écorces d'eucalyptus / EUCALYPTUS_BARK
- Famille : Forestier.
- Localisation : Centre du Portugal (bassin papetier eucalyptus), Portugal — GPS (Global Positioning System) 39.50, -8.20, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : écorce de grume, résidu d'exploitation.
- Gisement [ILLUSTRATION (à sourcer CELPA/ICNF)] : écorce ≈ 10 à 15 % de la grume (ratio) ; le Portugal est un grand bassin d'eucalyptus papetier (à sourcer).
- Fenêtre saisonnière : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc (flux continu des usines papetières).
- Techniques culturales, récolte, transformation : plantations d'eucalyptus à rotation courte, débardage et déroguage en usine.
- Brûlage [À VÉRIFIER] : le brûlage des résidus forestiers est très encadré au Portugal (période critique anti-incendie) (référence : ICNF / période crítica, à re-vérifier).
- Enfouissement [ILLUSTRATION] : non pertinent : résidu d'usine (référence : constat).
- Traitement [À VÉRIFIER] : combustible de chaudière d'usine papetière établi (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : hors agriculture : l'usine assume l'écorce (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : aucune main-d'œuvre dédiée : flux mécanique continu (référence : constat).

### COPEAU_HETRE — Copeaux de hêtre / BEECH_SHAVINGS
- Famille : Forestier.
- Localisation : France nord (scieries et menuiseries), France — GPS (Global Positioning System) 48.00, 2.00, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : copeaux de déroulage et rabotage, résidu sec.
- Gisement [ILLUSTRATION (à sourcer filière bois)] : copeaux ≈ 5 à 10 % du bois entrant (ratio).
- Fenêtre saisonnière : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc (flux continu des ateliers).
- Techniques culturales, récolte, transformation : exploitations feuillues ; déroulage (placage), rabotage en menuiserie, copeaux aspirés.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [ILLUSTRATION] : non pertinent : résidu d'atelier (référence : constat).
- Traitement [À VÉRIFIER] : litière et panneaux : débouchés établis (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : hors agriculture : l'atelier assume les copeaux (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : aucune main-d'œuvre dédiée : flux mécanique continu (référence : constat).

### AIGUILLE_PIN — Aiguilles de pin (litière) / PINE_NEEDLES
- Famille : Forestier.
- Localisation : Landes de Gascogne, France — GPS (Global Positioning System) 44.40, -0.80, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : litière d'aiguilles, récolte éventuelle en sous-bois.
- Gisement [ILLUSTRATION (à sourcer littérature sylvicole)] : litière ≈ 1 à 3 t/ha/an d'aiguilles et débris fins (ratio).
- Fenêtre saisonnière : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc (chute continue, récolte éventuelle hors périodes de risque incendie).
- Techniques culturales, récolte, transformation : sous-bois de pin maritime ; récolte éventuelle andains/pare-feux (débroussaillage, broyage).
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare ; les pare-feux sont entretenus par débroussaillage, pas par le feu (référence : Art. L.541-21-1 ; obligations de débroussaillage (fiche v0.6)).
- Enfouissement [À VÉRIFIER] : la litière reste au sol par défaut (fertilité forestière) (référence : pratique à sourcer).
- Traitement [À VÉRIFIER] : récolte marginale à documenter (paillage) (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : hors agriculture : coût de débroussaillage assumé par les communes et forestiers (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : débroussaillage mécanique (broyeur à marteaux) (référence : constat).

### MARC_POMME — Marc de pomme (cidrerie) / APPLE_POMACE
- Famille : Cultures pérennes.
- Localisation : Normandie (bassin cidricole), France — GPS (Global Positioning System) 49.29, 0.20, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : marc de pomme, résidu humide de pressurage.
- Gisement [ILLUSTRATION (à sourcer FNPP/INAO)] : France : pommes à cidre de l'ordre de 1,5 à 2 millions de t/an (à sourcer) ; marc ≈ 20 à 25 % du pressurage.
- Fenêtre saisonnière : oct-nov-déc (campagne cidricole octobre-décembre).
- Techniques culturales, récolte, transformation : vergers hautes tiges, récolte mécanisée au ramasseur, lavage, broyage et pressurage en cidrerie.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [À VÉRIFIER] : épandage des marcs sous conditions (plan de gestion) (référence : à sourcer DGAL).
- Traitement [DONNÉES RÉELLES] : distillation des marcs et cidres (bouilleurs de cru) : filière historique (référence : filière française réglementée).
- Coût pour l'agriculture [À VÉRIFIER] : la cidrerie assume le marc ; épandage ou distillation selon les débouchés (référence : à sourcer par cidrerie).
- Main-d'œuvre [ILLUSTRATION] : aucune main-d'œuvre dédiée : le marc suit le pressurage (référence : constat).

### DRECHE_BIERE — Drèche de brasserie (orge malté) / BREWERS_SPENT_GRAIN
- Famille : Brassicole.
- Localisation : France (brasseries régionales ; deck cervecerías argentin en réserve), France — GPS (Global Positioning System) 48.20, 7.50, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : drèche humide (enveloppes de grain et résidus d'amidon).
- Gisement [ILLUSTRATION (à sourcer Brasseurs de France)] : drèche ≈ 20 kg par hectolitre brassé (ratio) ; France : de l'ordre de 1,5 à 2 millions de t/an de drèche fraîche (à sourcer).
- Fenêtre saisonnière : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc (brassage continu, flux quotidien à la porte de la brasserie).
- Techniques culturales, récolte, transformation : empâtage et filtration du moût ; la drèche sort humide de la cuve filtre, en flux continu.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [À VÉRIFIER] : épandage agricole sous conditions (matières de catégorie 3 pour les brasseries) (référence : cadre sanitaire, à sourcer).
- Traitement [À VÉRIFIER] : alimentation bovine établie (drèche fraîche) ; séchage et valorisations en développement (référence : à sourcer par brasserie).
- Coût pour l'agriculture [ILLUSTRATION] : la brasserie assume l'évacuation ; les éleveurs enlèvent souvent gratuitement (litière/affouragement) (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : aucune main-d'œuvre dédiée : flux mécanique quotidien (référence : constat).

### SARGASSE — Sargasses échouées (brown tide) / SARGASSUM
- Famille : Marin.
- Localisation : Caraïbes / Riviera Maya (cancún), Mexique — GPS (Global Positioning System) 20.50, -86.90, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : algue brune échouée, gisement côtier massif.
- Gisement [ILLUSTRATION (à sourcer Red de Monitoreo de Sargazo)] : influx Caraïbes : des millions de t/an échouées (ordres de grandeur publics, à sourcer).
- Fenêtre saisonnière : avr-mai-juin-juil-août-sept-oct (saison des sargasses avril-octobre (pics mai-août)).
- Techniques culturales, récolte, transformation : ramassage mécanisé sur les plages (ceintures, barrages en mer), stockage et ensachage.
- Brûlage [À VÉRIFIER] : le brûlage des sargasses est proscrit (toxicité, règlements locaux) (référence : règlements municipaux Quintana Roo, à sourcer).
- Enfouissement [À VÉRIFIER] : l'enfouissement sauvage historique est en cours d'interdiction ; centres de valorisation en développement (référence : à sourcer SEMARNAT).
- Traitement [À VÉRIFIER] : ramassage quasi obligatoire sur les littoraux touristiques (prescriptions fédérales et hôtelières) (référence : protocoles Fondo NATIVA/SEMA, à sourcer).
- Coût pour l'agriculture [ILLUSTRATION] : hors agriculture : le ramassage coûte aux communes et hôtels (ordre : dizaines de millions de dollars/an dans la Caraïbe) (référence : rapports publics, à sourcer).
- Main-d'œuvre [ILLUSTRATION] : ramassage mécanisé, équipes municipales permanentes en saison (ordre de grandeur) (référence : rapports publics, à sourcer).

### COQUILLE_HUITRE — Coquilles d'huître / OYSTER_SHELL
- Famille : Minéral.
- Localisation : Marennes-Oléron (bassin ostréicole), France — GPS (Global Positioning System) 45.90, -1.10, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : coquille calcaire, résidu de capture et de tri.
- Gisement [ILLUSTRATION (à sourcer CNC/DPMA)] : France : huîtres de l'ordre de 100 000 à 150 000 t/an (à sourcer) ; coquille ≈ 80 à 90 % de la masse.
- Fenêtre saisonnière : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc (capture toute l'année, tri continu (peaks fêtes de fin d'année)).
- Techniques culturales, récolte, transformation : parcs d'élevage sur tables, capture au crible, affinage en claires ; les coquilles sont broyées pour le captage.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [À VÉRIFIER] : réemploi ostréicole : le captage et le cheminement des parcs consomment une part du gisement (référence : pratique à sourcer).
- Traitement [À VÉRIFIER] : amendement calcaire agricole et routier : débouchés établis (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : hors agriculture : la filière assume la coquille (collecte et broyage) (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : tri manuel et mécanique au dépôt (ordre de grandeur) (référence : constat).

### COQUILLE_MOULE — Coquilles de moule / MUSSEL_SHELL
- Famille : Minéral.
- Localisation : Bouchot de la baie du Mont-Saint-Michel, France — GPS (Global Positioning System) 48.60, -1.50, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : coquille calcaire, résidu de conserverie et de criblage.
- Gisement [ILLUSTRATION (à sourcer CNC/DPMA)] : France : moules de l'ordre de 75 000 à 90 000 t/an (à sourcer) ; coquille ≈ 40 à 60 % de la masse.
- Fenêtre saisonnière : juin-juil-août-sept-oct-nov-déc-janv (récolte juin-janvier (hors repos biologique printanier)).
- Techniques culturales, récolte, transformation : bouchots sur pieux, récolte mécanisée, criblage ; coquilles en rejet de tri.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [À VÉRIFIER] : amendement calcaire des côtes : débouché établi (référence : à sourcer).
- Traitement [À VÉRIFIER] : broyage en amendement et charge minérale : pistes à documenter (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : hors agriculture : la filière assume le rejet de tri (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : criblage mécanique continu (référence : constat).

### COQUILLE_ST_JACQUES — Coquilles Saint-Jacques / SCALLOP_SHELL
- Famille : Minéral.
- Localisation : Normandie / baie de Seine (coquillière principale), France — GPS (Global Positioning System) 49.50, 0.10, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : coquille calcaire, résidu de criée et de mareyage.
- Gisement [ILLUSTRATION (à sourcer DPMA)] : France : coquilles de l'ordre de 20 000 à 30 000 t/an débarquées (à sourcer) ; coquille ≈ 60 à 70 % de la masse.
- Fenêtre saisonnière : nov-déc-janv-févr (coquillière ouverte hors reproduction (novembre-avril dans les criées)).
- Techniques culturales, récolte, transformation : dragues à coquilles, tri à bord (rejets), criée et mareyage en port.
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [À VÉRIFIER] : amendement calcaire et valorisation locale (empierrements ostréicoles) (référence : à sourcer).
- Traitement [À VÉRIFIER] : broyage minéral à documenter (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : hors agriculture : le mareyage assume le rejet (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : rejets de tri mécaniques en criée (référence : constat).

### CARAPACE_CRABE — Carapaces de crabe (tourteaux) / CRAB_SHELL
- Famille : Minéral.
- Localisation : Bretagne nord (criées de la Manche), France — GPS (Global Positioning System) 48.50, -2.50, approximation de région, pas un cadastre. Point : point candidat.
- Flotte monde.py : intrant non encore simulé (point candidat).
- Bassin ERA5 (European Reanalysis v5) : aucun (candidat P3).
- Type de biomasse : carapace chitino-calcaire, résidu de conserverie et de criée.
- Gisement [ILLUSTRATION (à sourcer DPMA/filière crustacés)] : France : tourteaux de l'ordre de 10 000 à 50 000 t/an (à sourcer) ; carapace ≈ 50 à 60 % de la masse crabe.
- Fenêtre saisonnière : janv-févr-mars-avr-mai-juin-juil-août-sept-oct-nov-déc (débarquements étalés, conserveries en flux).
- Techniques culturales, récolte, transformation : casiers et filets, débarquement en criée, cuisson et écrémage en conserverie (carapaces en rejet).
- Brûlage [DONNÉES RÉELLES] : interdit à l'air libre, dérogation préfectorale rare (référence : Art. L.541-21-1 code de l'environnement (fiche v0.6)).
- Enfouissement [ILLUSTRATION] : non pertinent : résidu d'usine (référence : constat).
- Traitement [À VÉRIFIER] : chitosane et amendement : filières établies à documenter (référence : à sourcer).
- Coût pour l'agriculture [À VÉRIFIER] : hors agriculture : la conserverie assume le rejet (référence : à sourcer).
- Main-d'œuvre [ILLUSTRATION] : écrémage mécanique, tri manuel résiduel (ordre de grandeur) (référence : constat).


## Réglementation par pays — synthèse

Pays des 7 hubs (étiquette DONNÉES RÉELLES, fiches v0.6 du 17/10/2026) :

- France : brûlage à l'air libre interdit (art. L.541-21-1 code de l'environnement ; amende 750 euros ; dérogation préfectorale rare ; sanctions doublées loi 2023-973).
- Suisse : incinération en plein air interdite (OPair — Ordonnance sur la protection de l'air, art. 26a ; prescriptions cantonales).
- Italie : résidus hors régime déchets seulement si valorisés en agriculture (D.Lgs 152/2006 art. 185) ; combustion encadrée (LR Puglia 38/2016, interdiction dans les zones à risque).
- Espagne : combustion non permise par principe (Ley 7/2022 art. 27.3) ; exceptions par ordres annuels selon le danger d'incendie (DOE).
- Argentine : toute quema requiert une autorisation (Ley nationale 26.562) ; amendes provinciales sévères à Mendoza.
- Maroc : déchets agricoles couverts par la loi 28-00 ; cadre spécifique du brûlage à sourcer.

Nouvelles juridictions (étiquette À VÉRIFIER, références nommées à confirmer) :

- Brésil (São Paulo) : fin programmée du brûlage pré-récolte de canne (Lei estadual 11.241/2002) ; PNRS (Política Nacional de Resíduos Sólidos, loi 12.305/2010) pour les résidus d'usine.
- Inde (Pendjab) : brûlage des résidus restreint (directions CAAP 2019 du tribunal de Delhi, amendes PPCB — Punjab Pollution Control Board) ; précédent de la crise des pailles de riz.
- Malaisie / Indonésie : brûlage de replantation palmier restreint (accord ASEAN — Association of Southeast Asian Nations — sur la brume transfrontière, licences MPOB).
- Arabie Saoudite : brûlage des palmes courant, cadre national en durcissement (centre national de conformité environnementale).
- Mexique : LGPGIR (Ley General de Prevención y Gestión Integral de Residuos) pour agave, avocat, sargasses ; ramassage quasi obligatoire sur les littoraux touristiques.
- Philippines : RA 9003 (Ecological Solid Waste Management Act) pour les résidus d'ananas et de coco.
- Côte d'Ivoire, Équateur, Viêt Nam, Chine (Anji), Portugal (période critique anti-incendie ICNF — Instituto da Conservação da Natureza e das Florestas), Australie, États-Unis : cadres généraux cités par intrant, tous À VÉRIFIER.

Ces éléments décrivent un contexte réglementaire, pas une consultation juridique : valider par un conseil local avant tout engagement. La réglementation évolue : toute citation externe exige une re-vérification datée.

## Météo temps réelle

Branche v1.0 : Open-Meteo (API current weather, gratuite sans clé) interrogable pour les 52 points en un seul appel (listes latitude/longitude en virgules ; variables : température à 2 m, humidité relative à 2 m, précipitations, vent à 10 m ; fuseau UTC — Coordinated Universal Time). Le pointage est mis en cache une heure dans `cache-meteo-temps-reel/` (jamais versionné, exclu par .gitignore). Ce pointage est un outil de pilotage documentaire, jamais une donnée de qualification. Exemple de pointage réel du 18/10/2026 (17h30 UTC) : Vallée du Rhône 10,5 °C / 81 % ; Badajoz 20,5 °C / 63 % ; Mareeba (Australie) 17,4 °C / 99 % ; Ludhiana (Pendjab) vent 11 km/h ; Ribeirão Preto (Brésil) saison sèche. Les 10 bassins ERA5 de la flotte restent couverts par les agrégations mensuelles réelles versionnées (`cache-meteo/agregats-mensuels.json`).

## Reproductibilité

```
python3 engine/atlas_biomasses_monde.py               # sommaire des 52 intrants
python3 engine/atlas_biomasses_monde.py COQUE_NOIX   # fiche d'un intrant
python3 engine/atlas_biomasses_monde.py croisement    # couverture monde.py + familles
python3 engine/atlas_biomasses_monde.py meteo        # pointage temps réel des 52 points
python3 engine/atlas_biomasses_monde.py meteo COQUE_NOIX  # un point seul
```

Bibliothèque standard uniquement, déterministe (les sorties sommaire/fiche/croisement sont reproductibles à l'octet près) ; seule la branche météo dépend du réseau et échoue proprement hors ligne.

## Limites honnêtes

- Les points GPS sont des approximations de région : ils situent un gisement, pas une parcelle.
- Les gisements ILLUSTRATION sont des ordres de grandeur : sourcer (FAOSTAT, statistiques nationales) avant tout usage externe.
- La réglementation des nouvelles juridictions est À VÉRIFIER : aucune décision d'implantation ne s'appuie sur ces fiches sans re-vérification locale.
- L'atlas ne remplace ni la qualification machine (FAT/SAT — Factory Acceptance Test / Site Acceptance Test — sur acier réel), ni le calibrage des six paramètres VDE, qui vit hors du dépôt.
- La météo temps réelle est un pointage documentaire : la simulation World Twin reste SYNTHÉTIQUE, registre de développement.
