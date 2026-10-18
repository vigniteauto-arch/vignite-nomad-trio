#!/usr/bin/env python3
"""Couche 1 — atlas des biomasses monde du Trio Nomad v1 (v1.0, 18/10/2026).

Les 52 intrants du master privé (50 du dataset VDE + 2 addendums à mesurer)
placés sur le globe : famille, identités FR/EN, pays, région, point GPS de
positionnement (hub existant ou point candidat), type de biomasse, gisement
indicatif étiqueté, fenêtre saisonnière, techniques culturales et de
récolte/transformation, réglementation (brûlage, enfouissement, traitement,
coût pour l'agriculture, main-d'œuvre), rattachement aux bassins ERA5 de la
flotte et pointage météo temps réel optionnel.

RÈGLES :
- PROPRIÉTÉ INTELLECTUELLE : aucune valeur calibrée du master ne vit ici.
  Les six paramètres du VDE (lignine, cellulose, Tg, humidité maximale,
  alpha de diffusion, friction) restent dans l'atlas privé scellé.
  Ce module ne porte que des données publiques : géographie, volumes,
  calendriers, réglementation, météo.
- Chaque gisement porte une étiquette SOURCÉ (vérifiable, source citée)
  ou ILLUSTRATION (ordre de grandeur documentaire, à sourcer avant usage).
- Chaque élément réglementaire porte DONNÉES RÉELLES (texte identifié ;
  pays des 7 hubs couverts par les fiches v0.6) ou À VÉRIFIER (nouvelles
  juridictions : connaissance générale, re-vérification obligatoire).
- Les points GPS sont des approximations de région de positionnement
  (pas un cadastre) : à affiner avant tout ancrage terrain.
- La météo temps réelle vit dans cache-meteo-temps-reel/ (jamais versionné).

Lancement :

    python3 engine/atlas_biomasses_monde.py               # sommaire console
    python3 engine/atlas_biomasses_monde.py COQUE_NOIX    # fiche d'un intrant
    python3 engine/atlas_biomasses_monde.py croisement    # couverture flotte
    python3 engine/atlas_biomasses_monde.py meteo         # pointage temps réel
    python3 engine/atlas_biomasses_monde.py meteo COQUE_NOIX  # un point seul

verifier_couverture() contrôle au lancement que les 14 paires
(hub, biomasse) de engine/monde.py sont toutes rattachées à un intrant.
"""

import json
import os
import sys
import urllib.request

ETIQUETTE_SOURCÉ = "SOURCÉ"
ETIQUETTE_ILLUSTRATION = "ILLUSTRATION"
ETIQUETTE_REEL = "DONNÉES RÉELLES"
ETIQUETTE_A_VERIFIER = "À VÉRIFIER"

# Addendums du 10/10/2026, caractérisation à faire avant ingestion VDE.
STATUTS_A_MESURER = ("RESIDU_YERBA_MATE", "GRAINE_PAPAYE")

# Rattachements agronomiques documentés (le master privé reste l'autorité) :
# MARC_POMME est placé en Cultures pérennes (résidu d'un verger pérenne),
# TIGE_BAMBOU en Tropical ; ces deux rattachements sont documentés ici.

ATLAS_BIOMASSES_MONDE = {

    # ------------------------------------------------------------------
    # Cultures pérennes (4 du master + MARC_POMME, rattachement documenté)
    # ------------------------------------------------------------------

    "MARC_RAISIN": {
        "famille": "Cultures pérennes",
        "nom_fr": "Marc de raisin",
        "nom_en": "GRAPE_POMACE",
        "pays": "France",
        "region": "Vallée du Rhône (pilote v0)",
        "lat": 44.84,
        "lon": 4.85,
        "type_point": "hub existant",
        "hubs_flotte": {"fr-rhone": "marc-raisin", "ch-leman": "marc-raisin"},
        "bassin_era5": "vallee-du-rhone",
        "type_biomasse": "résidu humide de pressurage (peaux, pépins, pulpes)",
        "gisement": "France : 4 747 450 t de raisin récoltées en 2024 (FAOSTAT, extraction v0.9) ; marc ≈ 15 à 25 % de la vendange (ratio)",
        "etiquette_gisement": "SOURCÉ (FAOSTAT v0.9) ; ratio ILLUSTRATION",
        "fenetre": [9, 10, 11],
        "fenetre_note": "vendanges ; sur le hub suisse ch-leman la fenêtre moteur est [10, 11]",
        "techniques": "viticulture conduite en gobelet ou pergola ; vendanges manuelles et mécaniques ; pressurage au chai, le marc sort humide",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("compostage ou épandage des marcs, encadrés par les plans de gestion vinicoles", ETIQUETTE_A_VERIFIER, "pratique standard, à sourcer DGAL"),
            "traitement": ("distillation des marcs (bouilleurs de cru) ou méthanisation, filières historiques réglementées", ETIQUETTE_REEL, "filière française réglementée"),
            "cout_agriculture": ("évacuation du marc parfois facturée à la cave (ordre de grandeur : 0 à 30 €/t), non obligatoire", ETIQUETTE_ILLUSTRATION, "à sourcer par cave"),
            "main_oeuvre": ("aucune main-d'œuvre dédiée : le marc suit les vendanges", ETIQUETTE_A_VERIFIER, "ordre de grandeur"),
        },
    },

    "SARMENT_VIGNE": {
        "famille": "Cultures pérennes",
        "nom_fr": "Sarments de vigne (taille)",
        "nom_en": "VINE_SHOOTS",
        "pays": "France",
        "region": "Vallée du Rhône (pilote v0)",
        "lat": 44.84,
        "lon": 4.85,
        "type_point": "hub existant",
        "hubs_flotte": {"fr-rhone": "sarments-vigne", "ch-leman": "sarments-vigne",
                        "it-puglia": "sarments-vigne", "es-extremadura": "sarments-vigne",
                        "ar-cuyo": "restos-poda"},
        "bassin_era5": "vallee-du-rhone",
        "type_biomasse": "résidu de taille ligneux sec",
        "gisement": "ordre de grandeur : 1,5 à 3 t/ha/an de sarments ; France : 4 747 450 t de raisin 2024 (FAOSTAT v0.9) ; Mendoza : 145 393 ha de vigne (atlas v0.5)",
        "etiquette_gisement": "SOURCÉ (FAOSTAT v0.5/v0.9) ; rendement ILLUSTRATION",
        "fenetre": [1, 2, 3, 4],
        "fenetre_note": "taille d'hiver ; hémisphère Sud : fenêtre anti-saison juin-août sur ar-cuyo [6, 7, 8]",
        "techniques": "taille manuelle ou mécanique, broyage au rang ou andainage ; le sarment sec sort à la taille",
        "reglementation": {
            "brulage": ("interdit à l'air libre en France, dérogation préfectorale rare ; encadré en Argentine (autorisation obligatoire)", ETIQUETTE_REEL, "Art. L.541-21-1 (France) ; Ley 26.562 (Argentine) — fiches v0.6"),
            "enfouissement": ("broyage-enfouissement au rang préconisé et pratiqué (chaque pays du hub a sa pratique documentée)", ETIQUETTE_A_VERIFIER, "pratique standard, à sourcer par bassin"),
            "traitement": ("broyage, compostage ou valorisation énergétique ; le brûlage est fermé en France et contraint ailleurs", ETIQUETTE_REEL, "fiches v0.6 (7 hubs)"),
            "cout_agriculture": ("la taille est un coût obligatoire du vignoble ; la gestion du sarment est un surcoût sans valorisation (0 à 60 €/ha, ordre)", ETIQUETTE_ILLUSTRATION, "à sourcer par exploitation"),
            "main_oeuvre": ("la taille mobilise 60 à 100 heures de main-d'œuvre par hectare et par an (ordre de grandeur)", ETIQUETTE_ILLUSTRATION, "littérature viticole"),
        },
    },

    "RAFFLE_RAISIN": {
        "famille": "Cultures pérennes",
        "nom_fr": "Rafles de raisin",
        "nom_en": "GRAPE_STALKS",
        "pays": "France",
        "region": "Vallée du Rhône (pilote v0)",
        "lat": 44.84,
        "lon": 4.85,
        "type_point": "hub existant",
        "hubs_flotte": {"fr-rhone": None},
        "bassin_era5": "vallee-du-rhone",
        "type_biomasse": "squelette de la grappe, résidu humide de pressurage ou de vinification",
        "gisement": "rafles ≈ 3 à 5 % de la vendange ; France : 4 747 450 t de raisin 2024 (FAOSTAT v0.9)",
        "etiquette_gisement": "SOURCÉ (FAOSTAT v0.9) ; ratio ILLUSTRATION",
        "fenetre": [9, 10],
        "fenetre_note": "érafilage à la réception de la vendange, pour les vinifications sans macération carbonique",
        "techniques": "érafleuse-fouloir au chai ; rafles sortant humides, souvent compostées",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("compostage de cave le plus courant", ETIQUETTE_A_VERIFIER, "pratique standard, à sourcer"),
            "traitement": ("compostage ou méthanisation ; volume modeste mais régulier", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("négligeable en entrée : la rafle sort avec la vendange", ETIQUETTE_ILLUSTRATION, "ordre de grandeur"),
            "main_oeuvre": ("aucune main-d'œuvre dédiée : l'érafleur est déjà dans la chaîne", ETIQUETTE_ILLUSTRATION, "ordre de grandeur"),
        },
    },

    "RAMEAU_OLIVIER": {
        "famille": "Cultures pérennes",
        "nom_fr": "Rameaux d'olivier (taille)",
        "nom_en": "OLIVE_BRANCHES",
        "pays": "Italie",
        "region": "Puglia — Tavoliere (Foggia)",
        "lat": 41.12,
        "lon": 16.50,
        "type_point": "hub existant",
        "hubs_flotte": {"it-puglia": None},
        "bassin_era5": "italie-puglia",
        "type_biomasse": "résidu de taille ligneux",
        "gisement": "ordre de grandeur : 1 à 2,5 t/ha/an de bois de taille ; oliveraies puglieses de l'ordre de 370 000 ha (à sourcer)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer FAOSTAT/COI régional)",
        "fenetre": [2, 3, 4],
        "fenetre_note": "taille après récolte, février-avril",
        "techniques": "oléiculture traditionnelle ou intensive ; taille manuelle et mécanique, broyage inter-rang le plus courant",
        "reglementation": {
            "brulage": ("encadré : autorisation régionale requise, interdiction dans les zones à risque incendie", ETIQUETTE_REEL, "LR Puglia 38/2016 ; D.Lgs 152/2006 art. 185 (fiche v0.6)"),
            "enfouissement": ("broyage et enfouissement au rang préconisés", ETIQUETTE_A_VERIFIER, "pratique standard, à sourcer"),
            "traitement": ("broyage, valorisation énergétique ou distillation ; la combustion est de plus en plus contrainte", ETIQUETTE_REEL, "fiche v0.6 it-puglia"),
            "cout_agriculture": ("la taille est un coût obligatoire de l'oliveraie ; la gestion du bois de taille est un surcoût sans valorisation", ETIQUETTE_ILLUSTRATION, "à sourcer par exploitation"),
            "main_oeuvre": ("la taille mobilise 20 à 50 heures/ha et par an selon la densité (ordre de grandeur)", ETIQUETTE_ILLUSTRATION, "littérature oléicole"),
        },
    },

    # ------------------------------------------------------------------
    # Coques & noyaux (11 du master)
    # ------------------------------------------------------------------

    "NOYAU_OLIVE": {
        "famille": "Coques & noyaux",
        "nom_fr": "Noyau d'olive (grignons)",
        "nom_en": "OLIVE_PIT",
        "pays": "Espagne",
        "region": "Estrémadure (Badajoz)",
        "lat": 38.87,
        "lon": -6.97,
        "type_point": "hub existant",
        "hubs_flotte": {"it-puglia": "grignons-olive", "es-extremadura": "grignons-olive",
                        "ma-atlas": "grignons-olive"},
        "bassin_era5": "espagne-extremadure",
        "type_biomasse": "noyau et grignons d'olive, résidu oléicole dur",
        "gisement": "Espagne ≈ 1,4 million de t d'huile d'olive par campagne (COI, atlas v0.5) ; grignons ≈ 4 fois la masse d'huile (ratio) ; plus de 300 000 ha d'oliveraie en Estrémadure (fiche v0.6)",
        "etiquette_gisement": "SOURCÉ (COI/fiche v0.6) ; ratio ILLUSTRATION",
        "fenetre": [11, 12, 1, 2],
        "fenetre_note": "campagne oléicole ; fenêtres moteur [11, 12, 1] en Puglia et [12, 1, 2] à Meknès",
        "techniques": "récolte par vibrateurs ou peignes, trituration sous 24 à 48 heures ; les grignons sortent du moulin après extraction à deux phases",
        "reglementation": {
            "brulage": ("interdit par principe, exceptions par ordre annuel selon le danger d'incendie", ETIQUETTE_REEL, "Ley 7/2022 art. 27.3 ; órdenes DOE (fiche v0.6)"),
            "enfouissement": ("les grignons sont plutôt épandus ou valorisés (combustible, amendement)", ETIQUETTE_A_VERIFIER, "pratique à sourcer par moulin"),
            "traitement": ("grignonnage industriel courant : séparation noyau/pulpe, combustible ou amendement", ETIQUETTE_A_VERIFIER, "filière espagnole, à sourcer"),
            "cout_agriculture": ("le moulin assume l'évacuation des grignons ; l'agriculteur reçoit parfois un dédommagement", ETIQUETTE_ILLUSTRATION, "à sourcer par moulin"),
            "main_oeuvre": ("aucune main-d'œuvre dédiée : les grignons suivent l'huilerie", ETIQUETTE_ILLUSTRATION, "ordre de grandeur"),
        },
    },

    "COQUE_NOIX": {
        "famille": "Coques & noyaux",
        "nom_fr": "Coques de noix",
        "nom_en": "WALNUT_SHELL",
        "pays": "France",
        "region": "Périgord (pôle nucicole historique)",
        "lat": 44.90,
        "lon": 0.70,
        "type_point": "hub existant",
        "hubs_flotte": {"fr-rhone": "coques-noix"},
        "bassin_era5": "perigord",
        "type_biomasse": "coque dure, résidu de décorticage",
        "gisement": "France : 27 710 t de noix (avec coque) en 2024 (FAOSTAT v0.9) ; coque ≈ 50 % de la masse (ratio)",
        "etiquette_gisement": "SOURCÉ (FAOSTAT v0.9) ; ratio ILLUSTRATION",
        "fenetre": [10, 11, 12, 1, 2],
        "fenetre_note": "récolte octobre-novembre puis décorticage étalé jusqu'à février (fenêtre moteur fr-rhone)",
        "techniques": "nuciculture en vergers ; récolte mécanique (secoueuses), séchage, décorticage en atelier",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("non pertinent : la coque sort de l'atelier de décorticage", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("granulés et litières à base de coque existent ; valorisation énergétique locale courante", ETIQUETTE_A_VERIFIER, "filière nucicole, à sourcer"),
            "cout_agriculture": ("l'atelier facture ou assume le décorticage ; la coque est un sous-produit à valeur faible", ETIQUETTE_ILLUSTRATION, "à sourcer par atelier"),
            "main_oeuvre": ("décorticage mécanique : quelques heures par lot (ordre de grandeur)", ETIQUETTE_ILLUSTRATION, "à sourcer"),
        },
    },

    "COQUE_AMANDE": {
        "famille": "Coques & noyaux",
        "nom_fr": "Coques d'amande",
        "nom_en": "ALMOND_SHELL",
        "pays": "Espagne",
        "region": "Alicante (bassin amandier méditerranéen)",
        "lat": 38.35,
        "lon": -0.65,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "coque dure, résidu de décorticage",
        "gisement": "Espagne premier producteur européen d'amandes ; coque ≈ 40 à 60 % de la masse récoltée (ratios littérature)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer FAOSTAT/MAPA régional)",
        "fenetre": [8, 9, 10],
        "fenetre_note": "récolte août-octobre selon variétés et irrigation",
        "techniques": "amandiers irrigués ou secs ; récolte mécanisée (secoueuses), décorticage en atelier coopératif",
        "reglementation": {
            "brulage": ("interdit par principe, exceptions par ordre annuel selon le danger d'incendie", ETIQUETTE_REEL, "Ley 7/2022 art. 27.3 (cadre national espagnol, fiche v0.6)"),
            "enfouissement": ("non pertinent : la coque sort de l'atelier", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("combustible d'atelier et litière : valorisations locales établies", ETIQUETTE_A_VERIFIER, "filière espagnole, à sourcer"),
            "cout_agriculture": ("la coque est traditionnellement cédée au décortiqueur ; l'agriculteur touche parfois un petit dédommagement", ETIQUETTE_ILLUSTRATION, "à sourcer par coopérative"),
            "main_oeuvre": ("décorticage mécanique continu en campagne", ETIQUETTE_ILLUSTRATION, "à sourcer"),
        },
    },

    "COQUE_PISTACHE": {
        "famille": "Coques & noyaux",
        "nom_fr": "Coques de pistache",
        "nom_en": "PISTACHIO_SHELL",
        "pays": "Italie",
        "region": "Bronte (Sicile, pistachietto de l'Etna)",
        "lat": 37.79,
        "lon": 14.99,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "coque ligneuse, résidu de décorticage",
        "gisement": "Bronte : de l'ordre de 3 000 à 4 000 t de pistaches brutes les années paires (alternance bisannuelle, à sourcer)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer Consortium Bronte)",
        "fenetre": [9, 10],
        "fenetre_note": "récolte septembre-octobre, années alternées",
        "techniques": "pistachiers sur lave de l'Etna ; récolte manuelle par ételonnage, séchage et décorticage",
        "reglementation": {
            "brulage": ("les résidus agricoles restent exclus du régime déchets seulement si valorisés ; combustion encadrée", ETIQUETTE_REEL, "D.Lgs 152/2006 art. 185 (cadre italien, fiche v0.6)"),
            "enfouissement": ("non pertinent pour la coque d'atelier", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("valorisations locales à documenter (combustible,artisanat)", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("le décorticage est à la charge du producteur ou du transformateur local", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("récolte manuelle : poste dominant, plusieurs dizaines d'heures/ha (ordre de grandeur)", ETIQUETTE_ILLUSTRATION, "littérature pistachière"),
        },
    },

    "COQUE_NOISETTE": {
        "famille": "Coques & noyaux",
        "nom_fr": "Coques de noisette",
        "nom_en": "HAZELNUT_SHELL",
        "pays": "Italie",
        "region": "Piémont (Cuneo)",
        "lat": 44.38,
        "lon": 7.55,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "coque dure, résidu de décorticage",
        "gisement": "Italie deuxième producteur mondial, Varese-Langa : de l'ordre de 100 000 t/an de noisettes en coque (à sourcer) ; coque ≈ 45 à 50 % de la masse",
        "etiquette_gisement": "ILLUSTRATION (à sourcer FAOSTAT)",
        "fenetre": [8, 9, 10],
        "fenetre_note": "récolte août-octobre, décorticage en campagne",
        "techniques": "noisetiers en vergers conduits en gobelet ; récolte mécanisée à terre, séchage, calibrage, décorticage",
        "reglementation": {
            "brulage": ("les résidus agricoles restent hors régime déchets seulement si valorisés ; combustion encadrée", ETIQUETTE_REEL, "D.Lgs 152/2006 art. 185 (cadre italien, fiche v0.6)"),
            "enfouissement": ("non pertinent pour la coque d'atelier", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("combustible et litière : débouchés locaux établis à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("la coopérative assume le décorticage ; la coque est un sous-produit cédé", ETIQUETTE_A_VERIFIER, "à sourcer par coopérative"),
            "main_oeuvre": ("décorticage mécanique continu en campagne", ETIQUETTE_ILLUSTRATION, "à sourcer"),
        },
    },

    "NOYAU_CERISE": {
        "famille": "Coques & noyaux",
        "nom_fr": "Noyaux de cerise",
        "nom_en": "CHERRY_PIT",
        "pays": "France",
        "region": "Provence (bassin cerisier du Midi)",
        "lat": 44.00,
        "lon": 5.00,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "noyau dur, résidu de conserverie ou de distillation",
        "gisement": "noyau ≈ 8 à 12 % de la masse de cerise ; production française de l'ordre de 30 000 à 40 000 t/an (à sourcer)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer FAOSTAT/agrestes)",
        "fenetre": [6, 7],
        "fenetre_note": "récolte juin-juillet, conserveries en campagne",
        "techniques": "cerisaies ; récolte manuelle ou mécanique ; les noyaux sortent des conserveries et des distilleries",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("non pertinent : le noyau sort de la conserverie", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("débouchés existants (charge de chaudière, anneaux de massage, artisanat) à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("la conserverie assume le dénoyautage ; le noyau est un déchet de process à évacuer", ETIQUETTE_A_VERIFIER, "à sourcer par conserverie"),
            "main_oeuvre": ("dénoyautage mécanique en ligne", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "NOYAU_PECHE": {
        "famille": "Coques & noyaux",
        "nom_fr": "Noyaux de pêche",
        "nom_en": "PEACH_PIT",
        "pays": "France",
        "region": "Roussillon / Gard (bassins pêchers du Sud)",
        "lat": 43.84,
        "lon": 4.36,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "noyau dur, résidu de conserverie",
        "gisement": "noyau ≈ 6 à 10 % de la masse de pêche ; production française de l'ordre de 200 000 t/an (à sourcer)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer FAOSTAT/agrestes)",
        "fenetre": [6, 7, 8],
        "fenetre_note": "récolte juin à septembre selon variétés",
        "techniques": "vergers irrigués ; récolte manuelle en cagettes ; dénoyautage en conserverie",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("non pertinent : le noyau sort de la conserverie", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("combustible et charbon actif : pistes à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("la conserverie assume le dénoyautage et l'évacuation", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("dénoyautage mécanique en ligne", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "NOYAU_ABRICOT": {
        "famille": "Coques & noyaux",
        "nom_fr": "Noyaux d'abricot",
        "nom_en": "APRICOT_PIT",
        "pays": "France",
        "region": "Roussillon (premier bassin abricotier français)",
        "lat": 42.70,
        "lon": 2.90,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "noyau dur, résidu de conserverie",
        "gisement": "Roussillon ≈ 80 % de la production française d'abricots (ordre) ; noyau ≈ 6 à 10 % de la masse",
        "etiquette_gisement": "ILLUSTRATION (à sourcer FAOSTAT/agrestes)",
        "fenetre": [6, 7],
        "fenetre_note": "récolte juin-juillet, conserveries en campagne",
        "techniques": "vergers irrigués ; récolte manuelle ; dénoyautage en conserverie (amandes utilisées en confiserie, coques en résidu)",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("non pertinent : le noyau sort de la conserverie", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("charbon actif et combustible : filières à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("la conserverie assume le dénoyautage et l'évacuation", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("dénoyautage mécanique en ligne", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "COQUE_MACADAMIA": {
        "famille": "Coques & noyaux",
        "nom_fr": "Coques de macadamia",
        "nom_en": "MACADAMIA_SHELL",
        "pays": "Australie",
        "region": "Queensland (Mareeba)",
        "lat": -16.99,
        "lon": 145.42,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "coque très dure, résidu de décorticage",
        "gisement": "coque ≈ 60 à 70 % de la masse récoltée ; Australie de l'ordre de 50 000 t de noyaux/an (à sourcer)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer AMS)",
        "fenetre": [3, 4, 5, 6, 7, 8, 9, 10],
        "fenetre_note": "récolte étalée mars-octobre (chute naturelle)",
        "techniques": "vergers irrigués ; récolte par ramassage au sol, décorticage mécanique en usine",
        "reglementation": {
            "brulage": ("le brûlage des coques est courant en usine mais encadré par la réglementation australienne de l'air", ETIQUETTE_A_VERIFIER, "cadre état Queensland, à sourcer"),
            "enfouissement": ("non pertinent : la coque sort de l'usine", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("combustible d'usine établi (séchage des noix) : pratique industrielle à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("l'usine assume le décorticage ; la coque est un sous-produit valorisé en interne", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("décorticage mécanique continu", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "COQUE_PECAN": {
        "famille": "Coques & noyaux",
        "nom_fr": "Coques de pacane",
        "nom_en": "PECAN_SHELL",
        "pays": "États-Unis",
        "region": "Géorgie (Albany, premier bassin pacanier)",
        "lat": 31.58,
        "lon": -84.13,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "coque dure, résidu de décorticage",
        "gisement": "Géorgie de l'ordre de 60 à 70 millions de kg de pacanes/an (à sourcer USDA) ; coque ≈ 45 à 55 % de la masse",
        "etiquette_gisement": "ILLUSTRATION (à sourcer USDA NASS)",
        "fenetre": [10, 11, 12],
        "fenetre_note": "récolte octobre-décembre (secouage mécanique)",
        "techniques": "vergers irrigués ; secoueuses, ramassage, séchage, décorticage en usine",
        "reglementation": {
            "brulage": ("pratiqué localement mais de plus en plus contraint par les règles d'air de l'État", ETIQUETTE_A_VERIFIER, "règles GADNR/EPD, à sourcer"),
            "enfouissement": ("non pertinent : la coque sort de l'usine", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("mulch, litière et combustible : débouchés établis à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("l'usine assume le décorticage ; la coque est cédée à bas prix", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("décorticage mécanique continu en campagne", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "NOYAU_AVOCAT": {
        "famille": "Coques & noyaux",
        "nom_fr": "Noyaux d'avocat",
        "nom_en": "AVOCADO_PIT",
        "pays": "Mexique",
        "region": "Michoacán (Uruapan, premier bassin avocatier mondial)",
        "lat": 19.41,
        "lon": -102.06,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "noyau dur, résidu des emballeurs (packings)",
        "gisement": "Michoacán ≈ 2 millions de t d'avocats/an (ordre, premier producteur mondial) ; noyau ≈ 15 à 25 % de la masse",
        "etiquette_gisement": "ILLUSTRATION (à sourcer SIAP/FAOSTAT)",
        "fenetre": [10, 11, 12, 1, 2],
        "fenetre_note": "campagne principale octobre-février (export)",
        "techniques": "vergers en collines ; récolte manuelle, calibrage et emballage dans les packings, noyaux triés avec les sous-produits",
        "reglementation": {
            "brulage": ("le brûlage des résidus de packing existe mais le cadre fédéral des déchets s'applique", ETIQUETTE_A_VERIFIER, "LGPGIR (loi générale prévention gestion intégrale résidus), à sourcer"),
            "enfouissement": ("enfouissement des résidus organiques dans les vergers, pratiqué", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "traitement": ("compostage industriel en développement dans les packings", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("le packing assume l'évacuation des sous-produits (obligation sanitaire et environnementale croissante)", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("récolte et tri très manuels : poste dominant (ordre de grandeur, centaines d'heures/ha/an)", ETIQUETTE_ILLUSTRATION, "littérature avocatière"),
        },
    },

    # ------------------------------------------------------------------
    # Céréales et grandes cultures (10 du master)
    # ------------------------------------------------------------------

    "PAILLE_BLE": {
        "famille": "Céréales",
        "nom_fr": "Paille de blé",
        "nom_en": "WHEAT_STRAW",
        "pays": "France",
        "region": "Beauce (grenier à blé)",
        "lat": 48.44,
        "lon": 1.49,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "paille de céréale, résidu de moisson",
        "gisement": "France : blé de l'ordre de 30 millions de t/an (FAOSTAT-sourçable via le pipeline v0.9) ; paille ≈ 0,8 à 1,2 fois le grain (ratio)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer FAOSTAT v0.9)",
        "fenetre": [7, 8],
        "fenetre_note": "moisson juillet-août",
        "techniques": "culture de blé tendre et dur ; moissonneuse-batteuse, pressage des ballots au champ ou broyage-enfouissement",
        "reglementation": {
            "brulage": ("brûlage des chaumes interdit à l'air libre (biodéchets), dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("broyage-enfouissement pratiqué pour la fertilité, partiellement valorisé en litière et paillage", ETIQUETTE_A_VERIFIER, "pratique standard, à sourcer chambre d'agriculture"),
            "traitement": ("litière animale, méthanisation, paillage : filières établies, la valorisation thermo-chimique reste marginale", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("le pressage et l'andainage coûtent sans recette certaine (ordre : 20 à 40 €/t pressée)", ETIQUETTE_ILLUSTRATION, "à sourcer par exploitation"),
            "main_oeuvre": ("quelques dizaines de minutes/ha en presse à grosse balle (ordre de grandeur)", ETIQUETTE_ILLUSTRATION, "littérature céréalière"),
        },
    },

    "PAILLE_RIZ": {
        "famille": "Céréales",
        "nom_fr": "Paille de riz",
        "nom_en": "RICE_STRAW",
        "pays": "France",
        "region": "Camargue (rizicultures du delta)",
        "lat": 43.70,
        "lon": 4.30,
        "type_point": "hub existant",
        "hubs_flotte": {"fr-rhone": "paille-riz"},
        "bassin_era5": "camargue",
        "type_biomasse": "paille de riz, résidu de récolte, salifère",
        "gisement": "France : 71 960 t de riz paddy en 2024 (FAOSTAT v0.9) ; paille ≈ 0,7 à 1,2 fois le paddy (ratio)",
        "etiquette_gisement": "SOURCÉ (FAOSTAT v0.9) ; ratio ILLUSTRATION",
        "fenetre": [10, 11, 12],
        "fenetre_note": "récolte octobre-novembre, fenêtre moteur [10, 11, 12] (pain point historique : le brûlage camarguais)",
        "techniques": "riziculture inondée, moissonneuse-batteuse ; la paille reste au champ, broyée, enfouie ou brûlée",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare ; le brûlage camarguais persiste en dérogation encadrée", ETIQUETTE_REEL, "Art. L.541-21-1 ; feux réels FIRMS Camargue (fiches v0.6)"),
            "enfouissement": ("broyage-enfouissement pratiqué mais difficile (litière saline, sol asphyxié)", ETIQUETTE_A_VERIFIER, "pratique à sourcer"),
            "traitement": ("litière, méthanisation, valorisation énergétique : pistes à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("l'évacuation de la paille conditionne la préparation de la campagne suivante : contrainte forte et datée", ETIQUETTE_REEL, "contrainte agronomique, fiche pilote v0"),
            "main_oeuvre": ("une à deux passes de broyeur ou d'andaineur par hectare (ordre de grandeur)", ETIQUETTE_ILLUSTRATION, "à sourcer"),
        },
    },

    "RAFLE_MAIS": {
        "famille": "Céréales",
        "nom_fr": "Rafles de maïs",
        "nom_en": "MAIZE_COB",
        "pays": "France",
        "region": "Sud-Ouest / Aquitaine (bassin maïsiculture)",
        "lat": 43.89,
        "lon": -0.50,
        "type_point": "hub existant",
        "hubs_flotte": {"fr-rhone": "mais-rdm"},
        "bassin_era5": "sud-ouest",
        "type_biomasse": "rafle (épi dépouillé), résidu de récolte du maïs",
        "gisement": "France : 14 670 620 t de maïs grain en 2024 (FAOSTAT v0.9) ; rafle ≈ 15 % de l'épi (ratio)",
        "etiquette_gisement": "SOURCÉ (FAOSTAT v0.9) ; ratio ILLUSTRATION",
        "fenetre": [10, 11, 12],
        "fenetre_note": "récolte octobre-décembre, fenêtre moteur [10, 11, 12]",
        "techniques": "maïsiculture irriguée ; moissonneuse-batteuse, séchage en coopérative, rafles séparées au tri",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("broyage-enfouissement des cannes et rafles pratiqué pour la fertilité", ETIQUETTE_A_VERIFIER, "pratique standard, à sourcer"),
            "traitement": ("litière, lit de volaille, combustible : débouchés locaux à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("le tri coopératif assume la séparation ; la rafle est un sous-produit à faible valeur", ETIQUETTE_ILLUSTRATION, "à sourcer par coopérative"),
            "main_oeuvre": ("aucune main-d'œuvre dédiée : la rafle suit le flux de séchage", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "TIGE_TOURNESOL": {
        "famille": "Céréales",
        "nom_fr": "Tiges de tournesol",
        "nom_en": "SUNFLOWER_STALK",
        "pays": "France",
        "region": "Poitou (bassin tournesol non irrigué)",
        "lat": 46.58,
        "lon": 0.34,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "tige sèche creuse, résidu de récolte",
        "gisement": "France : tournesol de l'ordre de 1,3 à 1,7 million de t/an (à sourcer) ; tiges ≈ 2 à 3 t/ha (ratio)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer FAOSTAT/agrestes)",
        "fenetre": [9, 10],
        "fenetre_note": "récolte septembre-octobre",
        "techniques": "culture de printemps ; moisson à maturité, tiges broyées ou laissées debout puis enfouies",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("broyage-enfouissement pratiqué pour la fertilité", ETIQUETTE_A_VERIFIER, "pratique standard, à sourcer"),
            "traitement": ("valorisation marginale ; la paille de tournesol reste surtout enfouie", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("une passe de broyeur par hectare entre deux cultures (ordre : 15 à 30 €/ha)", ETIQUETTE_ILLUSTRATION, "à sourcer"),
            "main_oeuvre": ("demi-heure à une heure/ha de broyage (ordre de grandeur)", ETIQUETTE_ILLUSTRATION, "littérature"),
        },
    },

    "TIGE_COLZA": {
        "famille": "Céréales",
        "nom_fr": "Pailles de colza",
        "nom_en": "RAPE_STALK",
        "pays": "France",
        "region": "Beauce / Orléanais (bassin colza)",
        "lat": 47.90,
        "lon": 1.90,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "paille de colza, résidu de récolte",
        "gisement": "France : colza de l'ordre de 3 à 4 millions de t/an (à sourcer) ; paille ≈ 2 à 4 t/ha (ratio)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer FAOSTAT/agrestes)",
        "fenetre": [7, 8],
        "fenetre_note": "moisson juillet-août",
        "techniques": "culture d'hiver ; moissonneuse-batteuse, paille pressée pour litière ou enfouie",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("broyage-enfouissement pratiqué pour la fertilité", ETIQUETTE_A_VERIFIER, "pratique standard, à sourcer"),
            "traitement": ("litière animale établie ; méthanisation en développement", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("pressage ou broyage à la charge de l'exploitant (ordre : 20 à 40 €/t pressée)", ETIQUETTE_ILLUSTRATION, "à sourcer"),
            "main_oeuvre": ("quelques dizaines de minutes/ha en presse (ordre de grandeur)", ETIQUETTE_ILLUSTRATION, "littérature"),
        },
    },

    "CHENEVOTTE": {
        "famille": "Céréales",
        "nom_fr": "Chènevotte de chanvre",
        "nom_en": "HEMP_HURD",
        "pays": "France",
        "region": "Champagne (Aube, premier bassin chanvre)",
        "lat": 48.19,
        "lon": 4.71,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "moelle ligneuse défibrée du chanvre",
        "gisement": "France : chanvre industriel de l'ordre de 10 000 à 15 000 ha/an (à sourcer) ; chènevotte ≈ 50 à 60 % de la tige défibrée",
        "etiquette_gisement": "ILLUSTRATION (à sourcer InterChanvre)",
        "fenetre": [9, 10],
        "fenetre_note": "récolte septembre-octobre, défibrage ensuite",
        "techniques": "semis dense, récolte à l'automne, rouissage au champ, teillage en usine : fibre d'un côté, chènevotte de l'autre",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("non pertinent : la chènevotte sort du teillage", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("litière animale (couchage cheval) : débouché établi", ETIQUETTE_A_VERIFIER, "filière chanvre française, à sourcer"),
            "cout_agriculture": ("l'usine de teillage assume le sous-produit ; la chènevotte est cédée ou stockée", ETIQUETTE_A_VERIFIER, "à sourcer par usine"),
            "main_oeuvre": ("teillage mécanique continu", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "PAILLE_LIN": {
        "famille": "Céréales",
        "nom_fr": "Paille de lin",
        "nom_en": "FLAX_STRAW",
        "pays": "France",
        "region": "Normandie (bassin lin teillé)",
        "lat": 49.85,
        "lon": 0.85,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "paille de lin, résidu du teillage (anas de lin)",
        "gisement": "France : lin fibre de l'ordre de 60 000 à 100 000 ha/an, premier producteur mondial (à sourcer) ; anas ≈ 50 % de la paille teillée",
        "etiquette_gisement": "ILLUSTRATION (à sourcer CIPALIN)",
        "fenetre": [7, 8, 9],
        "fenetre_note": "arrachage juillet-août, rouissage, teillage automne-hiver",
        "techniques": "arrachage, rouissage au champ, rentrée en balles, teillage : fibre longue, lin à papier et anas en sous-produits",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("non pertinent : l'anas sort du teillage", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("panneaux, litière, plaquettes : débouchés établis", ETIQUETTE_A_VERIFIER, "filière linière, à sourcer"),
            "cout_agriculture": ("le teilleur assume l'anas ; cédé à bas prix à l'industrie panneautière", ETIQUETTE_A_VERIFIER, "à sourcer par teillage"),
            "main_oeuvre": ("teillage mécanique continu en campagne", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "TIGE_SORGHO": {
        "famille": "Céréales",
        "nom_fr": "Tiges de sorgho",
        "nom_en": "SORGHUM_STALK",
        "pays": "France",
        "region": "Sud-Ouest / Midi toulousain",
        "lat": 43.60,
        "lon": 1.44,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "tige sèche, résidu de récolte",
        "gisement": "France : sorgho de l'ordre de 30 000 à 50 000 ha/an (à sourcer) ; tiges ≈ 3 à 6 t/ha (ratio)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer agrestes)",
        "fenetre": [9, 10],
        "fenetre_note": "récolte septembre-octobre",
        "techniques": "culture de printemps non irriguée ou irriguée ; moisson, tiges broyées ou pâturées",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("broyage-enfouissement pratiqué pour la fertilité", ETIQUETTE_A_VERIFIER, "pratique standard, à sourcer"),
            "traitement": ("litière et fourrage résiduel : valorisations locales à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("une passe de broyeur par hectare (ordre : 15 à 30 €/ha)", ETIQUETTE_ILLUSTRATION, "à sourcer"),
            "main_oeuvre": ("demi-heure à une heure/ha de broyage (ordre de grandeur)", ETIQUETTE_ILLUSTRATION, "littérature"),
        },
    },

    "BALLE_AVOINE": {
        "famille": "Céréales",
        "nom_fr": "Balles d'avoine",
        "nom_en": "OAT_HUSK",
        "pays": "France",
        "region": "Bretagne (bassin avoine fourragère)",
        "lat": 48.47,
        "lon": -2.50,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "balle (enveloppe du grain), résidu de décortication",
        "gisement": "France : avoine de l'ordre de 2 à 3 millions de t/an (à sourcer) ; balle ≈ 20 à 30 % du grain décortiqué",
        "etiquette_gisement": "ILLUSTRATION (à sourcer FAOSTAT)",
        "fenetre": [8, 9],
        "fenetre_note": "moisson août-septembre, décortication ensuite",
        "techniques": "culture d'hiver ou de printemps ; moisson, décortication en atelier ou coopérative",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("non pertinent : la balle sort de l'atelier", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("litière animale établie ; valorisation énergétique marginale", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("l'atelier assume le sous-produit ; la balle est cédée en litière", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("décortication mécanique continue", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "TIGE_COTON": {
        "famille": "Céréales",
        "nom_fr": "Racines et tiges de coton (surge)",
        "nom_en": "COTTON_STALK",
        "pays": "Inde",
        "region": "Pendjab (Ludhiana, rotations coton-riz)",
        "lat": 30.90,
        "lon": 75.86,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "tige ligneuse arrachée après récolte du coton",
        "gisement": "Pendjab : coton de l'ordre de 300 000 à 500 000 ha/an (à sourcer) ; tiges ≈ 2 à 3 t/ha (ratio)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer PAU/ministère indien)",
        "fenetre": [10, 11, 12],
        "fenetre_note": "arrachage des plants octobre-décembre, avant le semis du blé",
        "techniques": "culture de mousson (kharif) ; récolte du kapok manuelle, plants arrachés à la main ou à la charrue",
        "reglementation": {
            "brulage": ("le brûlage des tiges et racines est restreint mais reste pratiqué ; la crise régionale du brûlage (pailles de riz) sert de précédent réglementaire", ETIQUETTE_A_VERIFIER, "directions CAAP 2019 (tribunal de Delhi) ; amendes PCA/PPCB — à re-vérifier"),
            "enfouissement": ("l'enfouissement des tiges est encouragé par les programmes agricoles (promotion du semis direct)", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "traitement": ("valorisation énergétique marginale aujourd'hui ; gisement massif à l'échelle du Pendjab", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("l'arrachage est un coût obligatoire entre deux cultures (monoculture interdite : le blé suit)", ETIQUETTE_A_VERIFIER, "rotation documentée, à re-vérifier"),
            "main_oeuvre": ("l'arrachage est manuel et coûteux : plusieurs dizaines d'heures/ha (ordre de grandeur)", ETIQUETTE_ILLUSTRATION, "littérature agronomique indienne"),
        },
    },

    # ------------------------------------------------------------------
    # Tropical (12 du master + 2 addendums à mesurer)
    # ------------------------------------------------------------------

    "BAGASSE_CANNE": {
        "famille": "Tropical",
        "nom_fr": "Bagasse de canne à sucre",
        "nom_en": "SUGARCANE_BAGASSE",
        "pays": "Brésil",
        "region": "São Paulo (Ribeirão Preto, cœur sucrier)",
        "lat": -21.18,
        "lon": -47.81,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "fibres de canne après broyage (gisement massif, humide)",
        "gisement": "monde : plus de 1,8 milliard de t/an de bagasse (atlas V3, ordre) ; Brésil ≈ la moitié de la canne mondiale",
        "etiquette_gisement": "ILLUSTRATION (à sourcer FAOSTAT/UNICA)",
        "fenetre": [5, 6, 7, 8, 9, 10, 11],
        "fenetre_note": "safra mai-novembre (broyage quotidien des usines)",
        "techniques": "récolte mécanisée croissante sans brûlage pré-récolte ; broyage à l'usine, bagasse déjà partiellement valorisée en chaudière",
        "reglementation": {
            "brulage": ("fin programmée du brûlage pré-récolte dans l'État de São Paulo (échéances selon la pente)", ETIQUETTE_A_VERIFIER, "Lei estadual 11.241/2002, à re-vérifier"),
            "enfouissement": ("la paille (trash) laissée au champ est de plus en plus maintenue en paillage", ETIQUETTE_A_VERIFIER, "pratique à sourcer"),
            "traitement": ("la bagasse alimente déjà les chaudières sucrières : co-génération établie, surplus disponible", ETIQUETTE_A_VERIFIER, "filière UNICA, à sourcer"),
            "cout_agriculture": ("l'usine assume la logistique ; la bagasse excédentaire est un sous-produit quasi gratuit à la porte de l'usine", ETIQUETTE_ILLUSTRATION, "à sourcer par usine"),
            "main_oeuvre": ("flux continu à la porte de l'usine : aucun andainage agricole nécessaire (cas d'école logistique)", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "BALLE_RIZ": {
        "famille": "Tropical",
        "nom_fr": "Balles de riz (balle blanche)",
        "nom_en": "RICE_HUSK",
        "pays": "France",
        "region": "Camargue (rizicultures du delta, rizeries locales)",
        "lat": 43.70,
        "lon": 4.30,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": "camargue",
        "type_biomasse": "enveloppe du paddy, résidu de rizerie, abrasive",
        "gisement": "France : 71 960 t de riz paddy 2024 (FAOSTAT v0.9) ; balle ≈ 20 % du paddy (ratio)",
        "etiquette_gisement": "SOURCÉ (FAOSTAT v0.9) ; ratio ILLUSTRATION",
        "fenetre": [10, 11, 12],
        "fenetre_note": "usinage après récolte, flux continu de la rizerie",
        "techniques": "riziculture, séchage puis décorticage en rizerie ; la balle sort en vrac du premier passage",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("non pertinent : la balle sort de la rizerie", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("litière et combustible de rizerie : débouchés locaux à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("la rizerie assume le sous-produit ; la balle est un débit de process continu", ETIQUETTE_A_VERIFIER, "à sourcer par rizerie"),
            "main_oeuvre": ("aucune main-d'œuvre dédiée : flux mécanique continu", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "DECHET_DATTIER": {
        "famille": "Tropical",
        "nom_fr": "Résidus de dattier (palmes d'élagage)",
        "nom_en": "DATE_PALM_RESIDUE",
        "pays": "Arabie Saoudite",
        "region": "Al-Qassim (oasis dattière)",
        "lat": 26.33,
        "lon": 43.97,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "palmes et stipes d'élagage, ligneux fibreux",
        "gisement": "Arabie : dattes de l'ordre de 1,5 million de t/an (à sourcer) ; résidus d'élagage ≈ 20 à 40 kg/arbre/an (ratio)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer FAOSTAT/GSCA)",
        "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "fenetre_note": "élagage continu, pics printemps et automne",
        "techniques": "palmeraies datte ; émondage manuel des palmes sèches, mise en andains ou brûlage traditionnel",
        "reglementation": {
            "brulage": ("le brûlage des palmes reste courant ; le cadre environnemental national le contraint progressivement", ETIQUETTE_A_VERIFIER, "centre national de conformité environnementale, à sourcer"),
            "enfouissement": ("non pratiqué : matériau ligneux volumineux, plutôt broyé en paillage", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "traitement": ("broyage en paillage ou valorisation énergétique : pistes à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("l'émondage est un coût obligatoire du dattier (sanitaire) ; l'évacuation des palmes est un surcoût", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("émondage manuel à la scie d'élagage : plusieurs heures par arbre et par an (ordre de grandeur)", ETIQUETTE_ILLUSTRATION, "littérature phœnicicole"),
        },
    },

    "NOYAU_DATTE": {
        "famille": "Tropical",
        "nom_fr": "Noyaux de datte",
        "nom_en": "DATE_PIT",
        "pays": "Arabie Saoudite",
        "region": "Al-Qassim (unités de conditionnement)",
        "lat": 26.33,
        "lon": 43.97,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "noyau dur, résidu des unités de conditionnement",
        "gisement": "noyau ≈ 10 à 15 % de la datte ; Arabie ≈ 1,5 million de t de dattes/an (à sourcer)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer FAOSTAT)",
        "fenetre": [8, 9, 10],
        "fenetre_note": "campagne de récolte des dattes août-octobre (khalal à tamr)",
        "techniques": "récolte par régimes, conditionnement et tri dans les unités ; les noyaux sortent des lignes de calibrage et de dénoyautage",
        "reglementation": {
            "brulage": ("non pertinent au champ : noyau d'atelier", ETIQUETTE_ILLUSTRATION, "constat"),
            "enfouissement": ("non pertinent : noyau d'atelier", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("farine de noyau (aliment bétail) existante ; valorisation énergétique à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("l'unité de conditionnement assume le dénoyautage ; le noyau est un débit de process", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("dénoyautage mécanique en ligne", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "RAFFLE_PALMIER": {
        "famille": "Tropical",
        "nom_fr": "Rafles de régime de palmier à huile",
        "nom_en": "PALM_RACHIS",
        "pays": "Malaisie",
        "region": "Johor (bassin huile de palme)",
        "lat": 1.94,
        "lon": 102.90,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "rachis de régime, résidu d'usine (empty fruit bunch)",
        "gisement": "Malaisie : de l'ordre de 100 millions de t/an de résidus palmier tous flux (à sourcer) ; rafles ≈ 20 à 25 t/ha/an (ratio)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer MPOB)",
        "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "fenetre_note": "production continue, pics lors des replantations",
        "techniques": "récolte des régimes toute l'année ; l'usine sépare fruits et rafles (stérilisation, égrappage) ; compostage partiel",
        "reglementation": {
            "brulage": ("le brûlage des résidus de replantation est restreint (lutte contre la brume transfrontière)", ETIQUETTE_A_VERIFIER, "accord ASEAN sur la brume transfrontière ; licences MPOB — à re-vérifier"),
            "enfouissement": ("compostage et épandage en plantation pratiqués", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "traitement": ("combustible de chaudière d'usine et compost : filières établies à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("l'usine assume le flux ; la rafle est un débit de process quasi gratuit à la porte", ETIQUETTE_ILLUSTRATION, "à sourcer par usine"),
            "main_oeuvre": ("flux continu à la porte de l'usine (cas d'école logistique, comme la bagasse)", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "TIGE_BANANIER": {
        "famille": "Tropical",
        "nom_fr": "Pseudotroncs de bananier",
        "nom_en": "BANANA_PSEUDOSTEM",
        "pays": "Équateur",
        "region": "Machala (premier bassin bananier d'exportation)",
        "lat": -3.26,
        "lon": -79.96,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "pseudotronc très humide, rejet de la récolte",
        "gisement": "pseudotroncs ≈ 30 à 50 t/ha/an de matière fraîche (ratio) ; Équateur : premier exportateur mondial de bananes",
        "etiquette_gisement": "ILLUSTRATION (à sourcer FAOSTAT/CNB)",
        "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "fenetre_note": "récolte continue, rejets hebdomadaires",
        "techniques": "plantations mestizas ; coupe des régimes, pseudotroncs abattus et laissés au rang ou hachés (fertilisation)",
        "reglementation": {
            "brulage": ("peu pratiqué : matériau humide ; le brûlage agricole est néanmoins encadré par la loi de gestion environnementale", ETIQUETTE_A_VERIFIER, "Ley de Gestión Ambiental (Équateur), à sourcer"),
            "enfouissement": ("hachage-enfouissement au rang, pratique dominante documentée", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "traitement": ("valorisations (fibres, compost) marginales à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("l'abattage du pseudotronc est un geste cultural obligatoire (cycle de rejets)", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("geste manuel à chaque passage de récolte (ordre : minutes/planche)", ETIQUETTE_ILLUSTRATION, "littérature bananière"),
        },
    },

    "FEUILLE_ANANAS": {
        "famille": "Tropical",
        "nom_fr": "Feuilles d'ananas (résidus de récolte)",
        "nom_en": "PINEAPPLE_LEAF",
        "pays": "Philippines",
        "region": "Cebu (zone ananas traditionnelle)",
        "lat": 10.31,
        "lon": 123.90,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "feuille longue fibreuse, résidu de récolte",
        "gisement": "feuilles ≈ 3 à 6 t/ha/cycle en matière sèche (ratio) ; Philippines : bassin ananas et fibre piña établi",
        "etiquette_gisement": "ILLUSTRATION (à sourcer DA-Philippines)",
        "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "fenetre_note": "récolte étalée toute l'année (cycles de 18 à 24 mois par parcelle)",
        "techniques": "culture en dams, récolte manuelle des fruits, feuilles coupées ou laissées au champ (décomposition lente)",
        "reglementation": {
            "brulage": ("le brûlage des feuilles d'ananas après récolte est courant mais contraint par la loi sur les déchets solides", ETIQUETTE_A_VERIFIER, "RA 9003 (Ecological Solid Waste Management Act), à sourcer"),
            "enfouissement": ("l'enfouissement des feuilles est encouragé pour la fertilité", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "traitement": ("la fibre piña (textile) valorise une part minime ; le gisement reste massivement au champ", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("le nettoyage de la parcelle après récolte est un coût obligatoire du cycle (replantation)", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("nettoyage manuel à la machette : plusieurs dizaines d'heures/ha (ordre de grandeur)", ETIQUETTE_ILLUSTRATION, "littérature"),
        },
    },

    "CABOSSE_CACAO": {
        "famille": "Tropical",
        "nom_fr": "Cabosses de cacao (coques vides)",
        "nom_en": "CACAO_POD",
        "pays": "Côte d'Ivoire",
        "region": "Daloa (premier bassin cacaoyer mondial)",
        "lat": 6.88,
        "lon": -6.45,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "coque de cabosse, résidu d'écabossage au champ",
        "gisement": "Côte d'Ivoire ≈ 2 millions de t de fèves/an, premier producteur mondial (à sourcer) ; cabosses ≈ 10 fois la masse des fèves en matière fraîche (ratio)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer FAOSTAT/CCC)",
        "fenetre": [1, 2, 3, 5, 6, 7, 10, 11, 12],
        "fenetre_note": "deux campagnes (octobre-mars, mai-août), écabossage au champ le jour de la cueillette",
        "techniques": "cacaoyères villageoises ; cueillette, écabossage manuel au champ, fermentation des fèves, les coques restent au pied des arbres",
        "reglementation": {
            "brulage": ("le brûlage des coques est pratiqué ponctuellement ; le cadre des déchets agricoles est à re-vérifier", ETIQUETTE_A_VERIFIER, "code de l'environnement ivoirien, à sourcer"),
            "enfouissement": ("les coques sont épandues au pied des cacaoyers (compostage de fait)", ETIQUETTE_A_VERIFIER, "pratique à sourcer"),
            "traitement": ("valorisation marginale (compost, biochar artisanal) à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("l'écabossage est un geste obligatoire de la récolte ; aucun surcoût dédié", ETIQUETTE_ILLUSTRATION, "constat"),
            "main_oeuvre": ("écabossage manuel au machette : minutes par cabosse, poste dominant à la récolte", ETIQUETTE_ILLUSTRATION, "littérature cacaoyère"),
        },
    },

    "FIBRE_COCO": {
        "famille": "Tropical",
        "nom_fr": "Balle de coco (fibre et poussière)",
        "nom_en": "COCO_COIR",
        "pays": "Philippines",
        "region": "Davao (bassin coco)",
        "lat": 7.19,
        "lon": 125.46,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "balle (épicarpe et mésocarpe), résidu de décortication",
        "gisement": "balle ≈ 25 à 35 % du fruit ; Philippines : noix de coco de l'ordre de 14 millions de t/an (à sourcer)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer PCA/FAOSTAT)",
        "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "fenetre_note": "récolte continue (cycle par arbre de 45 à 60 jours)",
        "techniques": "cocoteraies ; récolte des noix, décorticage en usine de fibre (coir) : fibre, poussière (coco peat) et résidus",
        "reglementation": {
            "brulage": ("le brûlage des balles et bourres est restreint par la loi sur les déchets solides", ETIQUETTE_A_VERIFIER, "RA 9003 (Philippines), à sourcer"),
            "enfouissement": ("la poussière de coco est valorisée en substrat : filière établie", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "traitement": ("filière coir établie (géotextiles, substrats) : part valorisée, gisement résiduel à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("l'usine de décorticage assume la balle ; le coprah reste le produit principal", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("récolte manuelle par gaffe : geste continu (ordre : minutes par arbre)", ETIQUETTE_ILLUSTRATION, "littérature"),
        },
    },

    "MARC_CAFE": {
        "famille": "Tropical",
        "nom_fr": "Marc de café (pulpe et mucilage)",
        "nom_en": "SPENT_COFFEE_GROUNDS",
        "pays": "Viêt Nam",
        "region": "Tay Nguyen (Buôn Ma Thuột, capitale du robusta)",
        "lat": 12.67,
        "lon": 108.06,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "pulpe et mucilage de la voie humide, résidu très humide",
        "gisement": "Viêt Nam ≈ 1,7 million de t de café/an, deuxième producteur mondial (à sourcer) ; pulpe ≈ 40 à 45 % de la cerise fraîche (ratio)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer FAOSTAT/VICofa)",
        "fenetre": [11, 12, 1, 2],
        "fenetre_note": "récolte du café novembre-février (sèche après)",
        "techniques": "caféiers robusta sur les hauts plateaux ; dépulpage en voie humide à la ferme ou au collecteur, séchage des parchment",
        "reglementation": {
            "brulage": ("le brûlage des pulpes est ponctuel ; la réglementation des déchets de dépulpage se durcit (déversements dans les rivières interdits)", ETIQUETTE_A_VERIFIER, "réglementation vietnamienne des déchets, à sourcer"),
            "enfouissement": ("compostage des pulpes pratiqué de façon croissante", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "traitement": ("compost et biogaz : pistes à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("le dépulpage est un geste obligatoire de la voie humide ; la pulpe est un débit de process", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("dépulpage mécanique à la ferme, manuel au tri", ETIQUETTE_ILLUSTRATION, "littérature caféière"),
        },
    },

    "RESIDU_AGAVE": {
        "famille": "Tropical",
        "nom_fr": "Bagasse d'agave (residuos de la jima)",
        "nom_en": "AGAVE_RESIDUE",
        "pays": "Mexique",
        "region": "Jalisco (Tequila, bassin de l'agave bleu)",
        "lat": 20.90,
        "lon": -103.84,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "fibres de piña cuite après distillation",
        "gisement": "Jalisco : agaves de l'ordre de 1 à 2 millions de t/an pour la tequila (à sourcer) ; bagasse ≈ 30 à 40 % de la piña cuite (ratio)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer CRT/FAOSTAT)",
        "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "fenetre_note": "jima (récolte) et distillation étalées sur l'année",
        "techniques": "agaves bleus mûris 6 à 8 ans ; jima manuelle (coa), cuisson des piñas, broyage, fermentation et distillation dans les tequileras",
        "reglementation": {
            "brulage": ("la bagasse d'agave est souvent brûlée ou abandonnée ; le cadre fédéral des résidus s'applique", ETIQUETTE_A_VERIFIER, "LGPGIR (Mexique), à sourcer"),
            "enfouissement": ("abandon en andains non réglementé constaté historiquement", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "traitement": ("compostage et valorisation énergétique en développement à documenter", ETIQUETTE_A_VERIFIER, "à sourcer CRT"),
            "cout_agriculture": ("la distillerie assume le flux ; la bagasse est un débit de process à la porte (cas d'école logistique)", ETIQUETTE_ILLUSTRATION, "à sourcer par tequilera"),
            "main_oeuvre": ("la jima est très manuelle (jimadores) : poste dominant (ordre : minutes par piña)", ETIQUETTE_ILLUSTRATION, "littérature agavère"),
        },
    },

    "TIGE_BAMBOU": {
        "famille": "Tropical",
        "nom_fr": "Débris de bambou (coupes)",
        "nom_en": "BAMBOO_CULM",
        "pays": "Chine",
        "region": "Anji (Zhejiang, capitale du bambou)",
        "lat": 30.68,
        "lon": 119.68,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "débris de coupe et vieilles chaumes, ligneux à croissance rapide",
        "gisement": "débris d'exploitation ≈ 20 à 30 % de la coupe (ratio) ; Anji : de l'ordre de 60 000 ha de bambouseraies (à sourcer)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer Anji/FAO)",
        "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "fenetre_note": "campagnes de coupe échelonnées (chaumes mûrs et dépérissants)",
        "techniques": "bambouseraies de moso ; coupe sélective des chaumes mûrs, débit en usines de planches et panifications",
        "reglementation": {
            "brulage": ("le brûlage des débris de coupe est interdit ou restreint localement (pollution de l'air, feux de forêt)", ETIQUETTE_A_VERIFIER, "règles locales du Zhejiang, à sourcer"),
            "enfouissement": ("les débris sont souvent laissés en litière de bambouseraie (mulch)", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "traitement": ("filière de transformation du bambou établie ; les débris restent sous-valorisés", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("la coupe est obligatoire (santé du massif) ; les débris sont un débit de coupe", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("coupe manuelle à la scie : heures par quartier de coupe (ordre de grandeur)", ETIQUETTE_ILLUSTRATION, "littérature sylvicole"),
        },
    },

    "RESIDU_YERBA_MATE": {
        "famille": "Tropical",
        "nom_fr": "Résidus de yerba mate (palos y palada)",
        "nom_en": "YERBA_MATE_RESIDUE",
        "pays": "Argentine",
        "region": "Misiones (cœur yerbatiero)",
        "lat": -27.45,
        "lon": -54.95,
        "type_point": "hub existant",
        "hubs_flotte": {"ar-misiones": "yerba-mate"},
        "bassin_era5": "argentine-misiones",
        "type_biomasse": "tiges et feuilles de taille, résidus de séchage (barbacuá)",
        "gisement": "Argentine : 986 738 t de feu verte en 2024 (INYM) ; environ 210 000 ha de yerba mate, 87 % à Misiones (fiche v0.6)",
        "etiquette_gisement": "SOURCÉ (INYM / fiche v0.6)",
        "fenetre": [4, 5, 6, 9, 10, 11],
        "fenetre_note": "fenêtre moteur exacte de monde.py (mois moyens et fins de campagne, hémisphère Sud)",
        "techniques": "plantations sous ombre ou plein soleil ; taille et récolte manuelles, séchage en séchoirs à bandes, les palos sortent du tri des moulins",
        "reglementation": {
            "brulage": ("autorisation préalable obligatoire pour toute quema, résidus de yerba mate inclus", ETIQUETTE_REEL, "Ley nationale 26.562 (fiche v0.6)"),
            "enfouissement": ("les palos et palada sont plutôt compostés ou laissés au champ", ETIQUETTE_A_VERIFIER, "pratique à sourcer INYM"),
            "traitement": ("compost et combustible de séchoir : pistes à documenter", ETIQUETTE_A_VERIFIER, "à sourcer par secadero"),
            "cout_agriculture": ("la taille est un coût obligatoire du yerbal ; les résidus sont un débit de séchoir", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("récolte manuelle dominante (tareferos) : très laborieuse (ordre : centaines d'heures/ha/an)", ETIQUETTE_ILLUSTRATION, "littérature yerbatière"),
        },
    },

    "GRAINE_PAPAYE": {
        "famille": "Tropical",
        "nom_fr": "Graines de papaye",
        "nom_en": "PAPAYA_SEEDS",
        "pays": "Brésil",
        "region": "Espírito Santo (bassin mamão)",
        "lat": -20.30,
        "lon": -40.34,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "graines et résidus de conserverie de papaye",
        "gisement": "graines ≈ 10 à 15 % du fruit ; Brésil : papaye de l'ordre de 1 million de t/an, premier producteur mondial (à sourcer)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer FAOSTAT/IBGE)",
        "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "fenetre_note": "production continue (culture pérenne de cycle court)",
        "techniques": "plantations irriguées, récolte manuelle continue, conserveries et juiceries en flux",
        "reglementation": {
            "brulage": ("non pertinent : résidu d'usine", ETIQUETTE_ILLUSTRATION, "constat"),
            "enfouissement": ("non pertinent : résidu d'usine", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("valorisations marginales à documenter (compost, extraits)", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("l'usine assume l'évacuation des graines et peaux (obligation de gestion des résidus)", ETIQUETTE_A_VERIFIER, "loi 12.305/2010 (PNRS Brésil), à sourcer"),
            "main_oeuvre": ("récolte manuelle continue (poste dominant)", ETIQUETTE_ILLUSTRATION, "littérature"),
        },
    },

    # ------------------------------------------------------------------
    # Forestier (6 du master + MARC_POMME, rattachement agronomique documenté)
    # ------------------------------------------------------------------

    "SCIURE_PIN": {
        "famille": "Forestier",
        "nom_fr": "Sciure de pin",
        "nom_en": "PINE_SAWDUST",
        "pays": "France",
        "region": "Landes de Gascogne (massif pin maritime)",
        "lat": 44.40,
        "lon": -0.80,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "sciure de scierie, résidu sec",
        "gisement": "sciure ≈ 5 à 10 % du bois entrant en scierie (ratio) ; massif landais ≈ 1 million de ha de pin maritime (à sourcer)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer CNPF/filière bois)",
        "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "fenetre_note": "flux continu des scieries",
        "techniques": "sylviculture de pin maritime, exploitations et scieries locales ; la sciure est aspirée au poste de débit",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare ; le brûlage des déchets de scierie est fermé", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("non pertinent : résidu d'atelier", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("panneaux et litière établis ; valorisation énergétique des chaudières bois", ETIQUETTE_A_VERIFIER, "filière bois française, à sourcer"),
            "cout_agriculture": ("hors agriculture : la scierie cède ou assume la sciure selon les débouchés", ETIQUETTE_A_VERIFIER, "à sourcer par scierie"),
            "main_oeuvre": ("aucune main-d'œuvre dédiée : flux mécanique continu", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "SCIURE_CHENE": {
        "famille": "Forestier",
        "nom_fr": "Sciure de chêne",
        "nom_en": "OAK_SAWDUST",
        "pays": "France",
        "region": "France nord (scieries de chêne)",
        "lat": 48.00,
        "lon": 2.00,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "sciure de scierie, résidu sec",
        "gisement": "sciure ≈ 5 à 10 % du bois entrant en scierie (ratio) ; le chêne est la première essence de feuillu française",
        "etiquette_gisement": "ILLUSTRATION (à sourcer filière bois)",
        "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "fenetre_note": "flux continu des scieries",
        "techniques": "exploitations feuillues, merrains de tonnellerie, scieries de chêne",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("non pertinent : résidu d'atelier", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("panneaux et combustible : débouchés établis", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("hors agriculture : la scierie cède ou assume la sciure", ETIQUETTE_A_VERIFIER, "à sourcer par scierie"),
            "main_oeuvre": ("aucune main-d'œuvre dédiée : flux mécanique continu", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "ECORCE_PIN": {
        "famille": "Forestier",
        "nom_fr": "Écorces de pin",
        "nom_en": "PINE_BARK",
        "pays": "France",
        "region": "Landes de Gascogne",
        "lat": 44.40,
        "lon": -0.80,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "écorce de grume, résidu d'exploitation",
        "gisement": "écorce ≈ 10 à 15 % de la grume (ratio) ; massif landais ≈ 1 million de ha de pin maritime (à sourcer)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer filière bois)",
        "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "fenetre_note": "flux continu des scieries (déroguage)",
        "techniques": "exploitations de pin maritime ; déroguage en scierie, écorce en vrac",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("paillage forestier pratiqué", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "traitement": ("paillage horticole établi ; combustible possible", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("hors agriculture : la scierie assume l'écorce", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("aucune main-d'œuvre dédiée : flux mécanique continu", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "ECORCE_EUCALYPTUS": {
        "famille": "Forestier",
        "nom_fr": "Écorces d'eucalyptus",
        "nom_en": "EUCALYPTUS_BARK",
        "pays": "Portugal",
        "region": "Centre du Portugal (bassin papetier eucalyptus)",
        "lat": 39.50,
        "lon": -8.20,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "écorce de grume, résidu d'exploitation",
        "gisement": "écorce ≈ 10 à 15 % de la grume (ratio) ; le Portugal est un grand bassin d'eucalyptus papetier (à sourcer)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer CELPA/ICNF)",
        "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "fenetre_note": "flux continu des usines papetières",
        "techniques": "plantations d'eucalyptus à rotation courte, débardage et déroguage en usine",
        "reglementation": {
            "brulage": ("le brûlage des résidus forestiers est très encadré au Portugal (période critique anti-incendie)", ETIQUETTE_A_VERIFIER, "ICNF / période crítica, à re-vérifier"),
            "enfouissement": ("non pertinent : résidu d'usine", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("combustible de chaudière d'usine papetière établi", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("hors agriculture : l'usine assume l'écorce", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("aucune main-d'œuvre dédiée : flux mécanique continu", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "COPEAU_HETRE": {
        "famille": "Forestier",
        "nom_fr": "Copeaux de hêtre",
        "nom_en": "BEECH_SHAVINGS",
        "pays": "France",
        "region": "France nord (scieries et menuiseries)",
        "lat": 48.00,
        "lon": 2.00,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "copeaux de déroulage et rabotage, résidu sec",
        "gisement": "copeaux ≈ 5 à 10 % du bois entrant (ratio)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer filière bois)",
        "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "fenetre_note": "flux continu des ateliers",
        "techniques": "exploitations feuillues ; déroulage (placage), rabotage en menuiserie, copeaux aspirés",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("non pertinent : résidu d'atelier", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("litière et panneaux : débouchés établis", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("hors agriculture : l'atelier assume les copeaux", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("aucune main-d'œuvre dédiée : flux mécanique continu", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "AIGUILLE_PIN": {
        "famille": "Forestier",
        "nom_fr": "Aiguilles de pin (litière)",
        "nom_en": "PINE_NEEDLES",
        "pays": "France",
        "region": "Landes de Gascogne",
        "lat": 44.40,
        "lon": -0.80,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "litière d'aiguilles, récolte éventuelle en sous-bois",
        "gisement": "litière ≈ 1 à 3 t/ha/an d'aiguilles et débris fins (ratio)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer littérature sylvicole)",
        "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "fenetre_note": "chute continue, récolte éventuelle hors périodes de risque incendie",
        "techniques": "sous-bois de pin maritime ; récolte éventuelle andains/pare-feux (débroussaillage, broyage)",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare ; les pare-feux sont entretenus par débroussaillage, pas par le feu", ETIQUETTE_REEL, "Art. L.541-21-1 ; obligations de débroussaillage (fiche v0.6)"),
            "enfouissement": ("la litière reste au sol par défaut (fertilité forestière)", ETIQUETTE_A_VERIFIER, "pratique à sourcer"),
            "traitement": ("récolte marginale à documenter (paillage)", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("hors agriculture : coût de débroussaillage assumé par les communes et forestiers", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("débroussaillage mécanique (broyeur à marteaux)", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "MARC_POMME": {
        "famille": "Cultures pérennes",
        "nom_fr": "Marc de pomme (cidrerie)",
        "nom_en": "APPLE_POMACE",
        "pays": "France",
        "region": "Normandie (bassin cidricole)",
        "lat": 49.29,
        "lon": 0.20,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "marc de pomme, résidu humide de pressurage",
        "gisement": "France : pommes à cidre de l'ordre de 1,5 à 2 millions de t/an (à sourcer) ; marc ≈ 20 à 25 % du pressurage",
        "etiquette_gisement": "ILLUSTRATION (à sourcer FNPP/INAO)",
        "fenetre": [10, 11, 12],
        "fenetre_note": "campagne cidricole octobre-décembre",
        "techniques": "vergers hautes tiges, récolte mécanisée au ramasseur, lavage, broyage et pressurage en cidrerie",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("épandage des marcs sous conditions (plan de gestion)", ETIQUETTE_A_VERIFIER, "à sourcer DGAL"),
            "traitement": ("distillation des marcs et cidres (bouilleurs de cru) : filière historique", ETIQUETTE_REEL, "filière française réglementée"),
            "cout_agriculture": ("la cidrerie assume le marc ; épandage ou distillation selon les débouchés", ETIQUETTE_A_VERIFIER, "à sourcer par cidrerie"),
            "main_oeuvre": ("aucune main-d'œuvre dédiée : le marc suit le pressurage", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    # ------------------------------------------------------------------
    # Brassicole (1)
    # ------------------------------------------------------------------

    "DRECHE_BIERE": {
        "famille": "Brassicole",
        "nom_fr": "Drèche de brasserie (orge malté)",
        "nom_en": "BREWERS_SPENT_GRAIN",
        "pays": "France",
        "region": "France (brasseries régionales ; deck cervecerías argentin en réserve)",
        "lat": 48.20,
        "lon": 7.50,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "drèche humide (enveloppes de grain et résidus d'amidon)",
        "gisement": "drèche ≈ 20 kg par hectolitre brassé (ratio) ; France : de l'ordre de 1,5 à 2 millions de t/an de drèche fraîche (à sourcer)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer Brasseurs de France)",
        "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "fenetre_note": "brassage continu, flux quotidien à la porte de la brasserie",
        "techniques": "empâtage et filtration du moût ; la drèche sort humide de la cuve filtre, en flux continu",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("épandage agricole sous conditions (matières de catégorie 3 pour les brasseries)", ETIQUETTE_A_VERIFIER, "cadre sanitaire, à sourcer"),
            "traitement": ("alimentation bovine établie (drèche fraîche) ; séchage et valorisations en développement", ETIQUETTE_A_VERIFIER, "à sourcer par brasserie"),
            "cout_agriculture": ("la brasserie assume l'évacuation ; les éleveurs enlèvent souvent gratuitement (litière/affouragement)", ETIQUETTE_ILLUSTRATION, "à sourcer"),
            "main_oeuvre": ("aucune main-d'œuvre dédiée : flux mécanique quotidien", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    # ------------------------------------------------------------------
    # Marin (1)
    # ------------------------------------------------------------------

    "SARGASSE": {
        "famille": "Marin",
        "nom_fr": "Sargasses échouées (brown tide)",
        "nom_en": "SARGASSUM",
        "pays": "Mexique",
        "region": "Caraïbes / Riviera Maya (cancún)",
        "lat": 20.50,
        "lon": -86.90,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "algue brune échouée, gisement côtier massif",
        "gisement": "influx Caraïbes : des millions de t/an échouées (ordres de grandeur publics, à sourcer)",
        "etiquette_gisement": "ILLUSTRATION (à sourcer Red de Monitoreo de Sargazo)",
        "fenetre": [4, 5, 6, 7, 8, 9, 10],
        "fenetre_note": "saison des sargasses avril-octobre (pics mai-août)",
        "techniques": "ramassage mécanisé sur les plages (ceintures, barrages en mer), stockage et ensachage",
        "reglementation": {
            "brulage": ("le brûlage des sargasses est proscrit (toxicité, règlements locaux)", ETIQUETTE_A_VERIFIER, "règlements municipaux Quintana Roo, à sourcer"),
            "enfouissement": ("l'enfouissement sauvage historique est en cours d'interdiction ; centres de valorisation en développement", ETIQUETTE_A_VERIFIER, "à sourcer SEMARNAT"),
            "traitement": ("ramassage quasi obligatoire sur les littoraux touristiques (prescriptions fédérales et hôtelières)", ETIQUETTE_A_VERIFIER, "protocoles Fondo NATIVA/SEMA, à sourcer"),
            "cout_agriculture": ("hors agriculture : le ramassage coûte aux communes et hôtels (ordre : dizaines de millions de dollars/an dans la Caraïbe)", ETIQUETTE_ILLUSTRATION, "rapports publics, à sourcer"),
            "main_oeuvre": ("ramassage mécanisé, équipes municipales permanentes en saison (ordre de grandeur)", ETIQUETTE_ILLUSTRATION, "rapports publics, à sourcer"),
        },
    },

    # ------------------------------------------------------------------
    # Minéral (4)
    # ------------------------------------------------------------------

    "COQUILLE_HUITRE": {
        "famille": "Minéral",
        "nom_fr": "Coquilles d'huître",
        "nom_en": "OYSTER_SHELL",
        "pays": "France",
        "region": "Marennes-Oléron (bassin ostréicole)",
        "lat": 45.90,
        "lon": -1.10,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "coquille calcaire, résidu de capture et de tri",
        "gisement": "France : huîtres de l'ordre de 100 000 à 150 000 t/an (à sourcer) ; coquille ≈ 80 à 90 % de la masse",
        "etiquette_gisement": "ILLUSTRATION (à sourcer CNC/DPMA)",
        "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "fenetre_note": "capture toute l'année, tri continu (peaks fêtes de fin d'année)",
        "techniques": "parcs d'élevage sur tables, capture au crible, affinage en claires ; les coquilles sont broyées pour le captage",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("réemploi ostréicole : le captage et le cheminement des parcs consomment une part du gisement", ETIQUETTE_A_VERIFIER, "pratique à sourcer"),
            "traitement": ("amendement calcaire agricole et routier : débouchés établis", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("hors agriculture : la filière assume la coquille (collecte et broyage)", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("tri manuel et mécanique au dépôt (ordre de grandeur)", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "COQUILLE_MOULE": {
        "famille": "Minéral",
        "nom_fr": "Coquilles de moule",
        "nom_en": "MUSSEL_SHELL",
        "pays": "France",
        "region": "Bouchot de la baie du Mont-Saint-Michel",
        "lat": 48.60,
        "lon": -1.50,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "coquille calcaire, résidu de conserverie et de criblage",
        "gisement": "France : moules de l'ordre de 75 000 à 90 000 t/an (à sourcer) ; coquille ≈ 40 à 60 % de la masse",
        "etiquette_gisement": "ILLUSTRATION (à sourcer CNC/DPMA)",
        "fenetre": [6, 7, 8, 9, 10, 11, 12, 1],
        "fenetre_note": "récolte juin-janvier (hors repos biologique printanier)",
        "techniques": "bouchots sur pieux, récolte mécanisée, criblage ; coquilles en rejet de tri",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("amendement calcaire des côtes : débouché établi", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "traitement": ("broyage en amendement et charge minérale : pistes à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("hors agriculture : la filière assume le rejet de tri", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("criblage mécanique continu", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "COQUILLE_ST_JACQUES": {
        "famille": "Minéral",
        "nom_fr": "Coquilles Saint-Jacques",
        "nom_en": "SCALLOP_SHELL",
        "pays": "France",
        "region": "Normandie / baie de Seine (coquillière principale)",
        "lat": 49.50,
        "lon": 0.10,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "coquille calcaire, résidu de criée et de mareyage",
        "gisement": "France : coquilles de l'ordre de 20 000 à 30 000 t/an débarquées (à sourcer) ; coquille ≈ 60 à 70 % de la masse",
        "etiquette_gisement": "ILLUSTRATION (à sourcer DPMA)",
        "fenetre": [11, 12, 1, 2],
        "fenetre_note": "coquillière ouverte hors reproduction (novembre-avril dans les criées)",
        "techniques": "dragues à coquilles, tri à bord (rejets), criée et mareyage en port",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("amendement calcaire et valorisation locale (empierrements ostréicoles)", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "traitement": ("broyage minéral à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("hors agriculture : le mareyage assume le rejet", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("rejets de tri mécaniques en criée", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },

    "CARAPACE_CRABE": {
        "famille": "Minéral",
        "nom_fr": "Carapaces de crabe (tourteaux)",
        "nom_en": "CRAB_SHELL",
        "pays": "France",
        "region": "Bretagne nord (criées de la Manche)",
        "lat": 48.50,
        "lon": -2.50,
        "type_point": "point candidat",
        "hubs_flotte": {},
        "bassin_era5": None,
        "type_biomasse": "carapace chitino-calcaire, résidu de conserverie et de criée",
        "gisement": "France : tourteaux de l'ordre de 10 000 à 50 000 t/an (à sourcer) ; carapace ≈ 50 à 60 % de la masse crabe",
        "etiquette_gisement": "ILLUSTRATION (à sourcer DPMA/filière crustacés)",
        "fenetre": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "fenetre_note": "débarquements étalés, conserveries en flux",
        "techniques": "casiers et filets, débarquement en criée, cuisson et écrémage en conserverie (carapaces en rejet)",
        "reglementation": {
            "brulage": ("interdit à l'air libre, dérogation préfectorale rare", ETIQUETTE_REEL, "Art. L.541-21-1 code de l'environnement (fiche v0.6)"),
            "enfouissement": ("non pertinent : résidu d'usine", ETIQUETTE_ILLUSTRATION, "constat"),
            "traitement": ("chitosane et amendement : filières établies à documenter", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "cout_agriculture": ("hors agriculture : la conserverie assume le rejet", ETIQUETTE_A_VERIFIER, "à sourcer"),
            "main_oeuvre": ("écrémage mécanique, tri manuel résiduel (ordre de grandeur)", ETIQUETTE_ILLUSTRATION, "constat"),
        },
    },
}


# ----------------------------------------------------------------------
# Contrôles de cohérence
# ----------------------------------------------------------------------

CLEFS_REGLEMENTATION = ("brulage", "enfouissement", "traitement",
                        "cout_agriculture", "main_oeuvre")


def familles():
    """Familles dans l'ordre stable de l'atlas."""
    vues = []
    for fiche in ATLAS_BIOMASSES_MONDE.values():
        if fiche["famille"] not in vues:
            vues.append(fiche["famille"])
    return vues


def tokens_de_la_famille(famille):
    return [t for t, f in ATLAS_BIOMASSES_MONDE.items()
            if f["famille"] == famille]


def paires_flotte():
    """Les paires (hub, biomasse moteur) rattachées à un intrant."""
    paires = []
    for token, fiche in ATLAS_BIOMASSES_MONDE.items():
        for hub, biomasse in fiche.get("hubs_flotte", {}).items():
            if biomasse is not None:
                paires.append((token, hub, biomasse))
    return paires


def verifier_couverture():
    """Contrôle que l'atlas couvre exactement la flotte de monde.py.

    Retourne None si le contrôle passe, sinon un message d'écart.
    Tolérant : si monde.py n'est pas importable, contrôle sauté.
    """
    try:
        import monde
    except ImportError:
        return None
    paires_moteur = set()
    for hub, fiche_hub in monde.HUBS_MONDE.items():
        for biomasse in fiche_hub["biomasses"]:
            paires_moteur.add((hub, biomasse))
    paires_atlas = set()
    for token, fiche in ATLAS_BIOMASSES_MONDE.items():
        for hub, biomasse in fiche.get("hubs_flotte", {}).items():
            if biomasse is not None:
                paires_atlas.add((hub, biomasse))
    if paires_moteur != paires_atlas:
        manquants = sorted(paires_moteur - paires_atlas)
        en_trop = sorted(paires_atlas - paires_moteur)
        return ("écart atlas/moteur — manquants: %s ; en trop: %s" % (
            ", ".join("%s/%s" % p for p in manquants) or "aucun",
            ", ".join("%s/%s" % p for p in en_trop) or "aucun"))
    return None


def verifier_coherence_interne():
    """Contrôles internes : GPS plausibles, réglementation complète."""
    ecarts = []
    for token, fiche in ATLAS_BIOMASSES_MONDE.items():
        if not (-90.0 <= fiche["lat"] <= 90.0 and -180.0 <= fiche["lon"] <= 180.0):
            ecarts.append("%s : GPS hors bornes" % token)
        if fiche["lat"] == 0.0 and fiche["lon"] == 0.0:
            ecarts.append("%s : GPS nul" % token)
        for clef in CLEFS_REGLEMENTATION:
            if clef not in fiche["reglementation"]:
                ecarts.append("%s : réglementation incomplète (%s)" % (token, clef))
        if not fiche["fenetre"]:
            ecarts.append("%s : fenêtre vide" % token)
    return ecarts or None


def verifier_bassins():
    """Contrôle que les bassins ERA5 rattachés existent dans le cache météo."""
    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "cache-meteo", "agregats-mensuels.json")
    if not os.path.exists(chemin):
        return None
    try:
        with open(chemin, "r", encoding="utf-8") as fh:
            donnees = json.load(fh)
    except (OSError, ValueError):
        return None
    connus = set(donnees.get("bassins", {}))
    rattachements = {f["bassin_era5"] for f in ATLAS_BIOMASSES_MONDE.values()
                     if f["bassin_era5"] is not None}
    inconnus = sorted(rattachements - connus)
    if inconnus:
        return "bassins ERA5 inconnus du cache météo : %s" % ", ".join(inconnus)
    return None


# ----------------------------------------------------------------------
# Rendus console
# ----------------------------------------------------------------------

MOIS_COURTS = {1: "janv", 2: "févr", 3: "mars", 4: "avr", 5: "mai", 6: "juin",
               7: "juil", 8: "août", 9: "sept", 10: "oct", 11: "nov", 12: "déc"}


def _fenetre_texte(mois):
    return "-".join(MOIS_COURTS[m] for m in mois)


def fiche_token(token):
    if token not in ATLAS_BIOMASSES_MONDE:
        return ("Intrant inconnu : %s. Intrants : %s"
                % (token, ", ".join(ATLAS_BIOMASSES_MONDE)))
    f = ATLAS_BIOMASSES_MONDE[token]
    lignes = []
    lignes.append("== %s — %s / %s" % (token, f["nom_fr"], f["nom_en"]))
    lignes.append("  Famille : %s%s" % (
        f["famille"],
        " (statut À MESURER)" if token in STATUTS_A_MESURER else ""))
    lignes.append("  Localisation : %s, %s (GPS %.2f, %.2f — approximation de région, pas un cadastre)"
                  % (f["region"], f["pays"], f["lat"], f["lon"]))
    lignes.append("  Point : %s" % f["type_point"])
    if f["hubs_flotte"]:
        liens = ["%s → %s" % (h, b) for h, b in f["hubs_flotte"].items() if b]
        lignes.append("  Flotte monde.py : %s" % ", ".join(liens))
    else:
        lignes.append("  Flotte monde.py : intrant non encore simulé (point candidat)")
    lignes.append("  Bassin ERA5 : %s" % (f["bassin_era5"] or "aucun (candidat P3)"))
    lignes.append("  Type : %s" % f["type_biomasse"])
    lignes.append("  Gisement [%s] : %s" % (f["etiquette_gisement"], f["gisement"]))
    lignes.append("  Fenêtre : %s (%s)" % (_fenetre_texte(f["fenetre"]), f["fenetre_note"]))
    lignes.append("  Techniques : %s" % f["techniques"])
    lignes.append("  Réglementation :")
    for clef in CLEFS_REGLEMENTATION:
        texte, etiquette, reference = f["reglementation"][clef]
        lignes.append("    %-15s [%s] %s (référence : %s)"
                      % (clef + " :", etiquette, texte, reference))
    return "\n".join(lignes)


def sommaire():
    lignes = ["Atlas des biomasses monde — %d intrants (v1.0, 18/10/2026)"
              % len(ATLAS_BIOMASSES_MONDE),
              "Master privé : identités publiques uniquement ; aucune valeur calibrée VDE.",
              ""]
    for famille in familles():
        tokens = tokens_de_la_famille(famille)
        lignes.append("[%s] %d intrants" % (famille, len(tokens)))
        for token in tokens:
            f = ATLAS_BIOMASSES_MONDE[token]
            marqueur = " (À MESURER)" if token in STATUTS_A_MESURER else ""
            lignes.append("  %-20s %-28s %s, %s [%s]%s"
                          % (token, f["nom_fr"], f["region"], f["pays"],
                             f["type_point"], marqueur))
        lignes.append("")
    lignes.append("Lancement : fiche d'un intrant (python3 engine/atlas_biomasses_monde.py TOKEN),")
    lignes.append("croisement de couverture (croisement), pointage météo temps réel (meteo [TOKEN]).")
    return "\n".join(lignes) + "\n"


def croisement():
    lignes = ["Croisement atlas biomasses / flotte monde (v1.0, 18/10/2026)", ""]
    ecart = verifier_couverture()
    lignes.append("Couverture monde.py : %s" % ("OK — toutes les paires (hub, biomasse) rattachées"
                                               if ecart is None else "ÉCART : %s" % ecart))
    ecarts_internes = verifier_coherence_interne()
    lignes.append("Cohérence interne : %s" % ("OK" if ecarts_internes is None
                                              else "ÉCARTS : %s" % "; ".join(ecarts_internes)))
    ecart_bassins = verifier_bassins()
    lignes.append("Bassins ERA5 rattachés : %s" % ("OK (vérifiés contre le cache météo versionné)"
                                                   if ecart_bassins is None else "ÉCART : %s" % ecart_bassins))
    lignes.append("")
    lignes.append("Paires (hub, biomasse moteur) rattachées :")
    for token, hub, biomasse in paires_flotte():
        lignes.append("  %-20s %-15s %s" % (token, hub, biomasse))
    lignes.append("")
    lignes.append("Familles :")
    for famille in familles():
        lignes.append("  %-22s %d intrants" % (famille, len(tokens_de_la_famille(famille))))
    lignes.append("")
    lignes.append("Intrants statut À MESURER (addendum du 10/10/2026) : %s"
                  % ", ".join(t for t in ATLAS_BIOMASSES_MONDE if t in STATUTS_A_MESURER))
    lignes.append("Points hub existant : %d ; points candidats : %d" % (
        sum(1 for f in ATLAS_BIOMASSES_MONDE.values() if f["type_point"].startswith("hub")),
        sum(1 for f in ATLAS_BIOMASSES_MONDE.values() if f["type_point"].startswith("point"))))
    return "\n".join(lignes) + "\n"


# ----------------------------------------------------------------------
# Météo temps réel (Open-Meteo, cache jamais versionné)
# ----------------------------------------------------------------------

VARIABLES_METEO = ("temperature_2m", "relative_humidity_2m", "precipitation",
                   "wind_speed_10m")
TTL_POINTAGE_S = 3600


def _chemin_cache_meteo_temps_reel():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "cache-meteo-temps-reel")


def _pointage_en_cache(tokens):
    """Retourne un pointage horodaté s'il existe et est frais, sinon None."""
    dossier = _chemin_cache_meteo_temps_reel()
    if not os.path.isdir(dossier):
        return None
    attendus = set(tokens)
    for nom in sorted(os.listdir(dossier), reverse=True):
        if not nom.startswith("pointage-") or not nom.endswith(".json"):
            continue
        chemin = os.path.join(dossier, nom)
        try:
            age = max(0, int(__import__("time").time() - os.path.getmtime(chemin)))
        except OSError:
            continue
        if age > TTL_POINTAGE_S:
            continue
        try:
            with open(chemin, "r", encoding="utf-8") as fh:
                contenu = json.load(fh)
        except (OSError, ValueError):
            continue
        if attendus.issubset(set(contenu.get("points", {}))):
            return contenu
    return None


def pointage_meteo(tokens=None):
    """Pointage météo temps réel Open-Meteo pour un ou tous les intrants.

    Un seul appel API pour tous les points (listes lat/lon en virgules),
    mise en cache horaire dans cache-meteo-temps-reel/ (jamais versionné).
    """
    if tokens is None:
        tokens = list(ATLAS_BIOMASSES_MONDE)
    for token in tokens:
        if token not in ATLAS_BIOMASSES_MONDE:
            raise SystemExit("Intrant inconnu : %s. Intrants : %s"
                             % (token, ", ".join(ATLAS_BIOMASSES_MONDE)))
    cache = _pointage_en_cache(tokens)
    if cache is not None:
        return cache
    latitudes = ",".join("%.4f" % ATLAS_BIOMASSES_MONDE[t]["lat"] for t in tokens)
    longitudes = ",".join("%.4f" % ATLAS_BIOMASSES_MONDE[t]["lon"] for t in tokens)
    url = ("https://api.open-meteo.com/v1/forecast"
           "?latitude=%s&longitude=%s&current=%s&timezone=UTC"
           % (latitudes, longitudes, ",".join(VARIABLES_METEO)))
    try:
        with urllib.request.urlopen(url, timeout=30) as reponse:
            brut = json.loads(reponse.read().decode("utf-8"))
    except (OSError, ValueError) as erreur:
        raise SystemExit("Pointage météo indisponible (réseau : %s). "
                         "Le module reste utilisable hors ligne." % erreur)
    points = {}
    for index, token in enumerate(tokens):
        if isinstance(brut, list):
            courant = brut[index].get("current", {})
        else:
            courant = brut.get("current", {})
        points[token] = {clef: courant.get(clef) for clef in VARIABLES_METEO}
        points[token]["heure_utc"] = courant.get("time")
    contenu = {"etiquette": "POINTAGE TEMPS RÉEL (Open-Meteo current, non versionné)",
               "source": "api.open-meteo.com, gratuite sans clé",
               "points": points}
    dossier = _chemin_cache_meteo_temps_reel()
    try:
        os.makedirs(dossier, exist_ok=True)
        horodatage = __import__("time").strftime("%Y%m%dT%H", __import__("time").gmtime())
        with open(os.path.join(dossier, "pointage-%s.json" % horodatage),
                  "w", encoding="utf-8") as fh:
            json.dump(contenu, fh, ensure_ascii=False, indent=1, sort_keys=True)
    except OSError:
        pass  # cache best effort : le pointage reste affiché
    return contenu


def rendre_pointage(contenu):
    lignes = ["Pointage météo temps réel — %d point(s) (Open-Meteo, cache local d'une heure)"
              % len(contenu["points"]),
              "Étiquette : %s — jamais une donnée de qualification." % contenu["etiquette"],
              ""]
    lignes.append("%-20s %-28s %8s %8s %8s %8s" % ("intranT", "localisation", "T°C", "HR%", "mm", "km/h"))
    for token in ATLAS_BIOMASSES_MONDE:
        if token not in contenu["points"]:
            continue
        f = ATLAS_BIOMASSES_MONDE[token]
        m = contenu["points"][token]
        lignes.append("%-20s %-28s %8s %8s %8s %8s" % (
            token, f["pays"], m.get("temperature_2m"), m.get("relative_humidity_2m"),
            m.get("precipitation"), m.get("wind_speed_10m")))
    return "\n".join(lignes) + "\n"


def main():
    ecarts = verifier_coherence_interne()
    if ecarts:
        print("ATTENTION : %s" % "; ".join(ecarts))
    ecart = verifier_couverture()
    if ecart:
        print("ATTENTION : %s" % ecart)
    arguments = sys.argv[1:]
    if not arguments:
        print(sommaire())
    elif arguments[0] == "croisement":
        print(croisement())
    elif arguments[0] == "meteo":
        tokens = arguments[1:] or None
        contenu = pointage_meteo(tokens)
        print(rendre_pointage(contenu))
    else:
        for token in arguments:
            print(fiche_token(token))
    return 0


if __name__ == "__main__":
    sys.exit(main())
