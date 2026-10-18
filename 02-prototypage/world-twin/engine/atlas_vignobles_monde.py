#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""World Twin v1.2 — Atlas des vignobles du monde.

Déclinaison viticole des atlas v1.0 (52 intrants du master) et v1.1 (67 intrants
locaux par pays) : les vignobles majeurs du monde sont placés sur le globe —
région, point GPS (approximation de région, jamais un cadastre), volume, surface,
fenêtre saisonnière, techniques — pour vingt-deux pays viticoles hors France,
Italie et Suisse (déjà couverts par le master v1.0 et l'atlas v1.1). Deux intrants
selon les bassins : les sarments de taille (partout) et le marc de pressurage (dix
grands bassins vinicoles), avec, par pays, une synthèse réglementaire à cinq
postes (brûlage, enfouissement, traitement, coûts pour l'agriculture, main-d'œuvre).

Doctrine PI : ce module n'embarque AUCUN des six paramètres du VDE (Vignite
Decision Engine) et aucune valeur calibrée. Seules des données publiques sont
versionnées : géographie, productions et surfaces nationales FAOSTAT (Food and
Agriculture Organization of the United Nations), ratios documentaires, calendriers,
réglementation. Les productions et surfaces sont SOURCÉES (bulk FAOSTAT 2024,
item Grapes) ; les ratios résidus sont ILLUSTRATION ; la réglementation est
DONNÉES RÉELLES pour les juridictions hub couvertes par les fiches v0.6 et
À VÉRIFIER pour les autres.

Bibliothèque standard uniquement, déterministe, aucune dépendance réseau.
Usage :
    python3 engine/atlas_vignobles_monde.py                    # sommaire par pays
    python3 engine/atlas_vignobles_monde.py SARMENT_VIGNE_AR  # fiche d'un intrant
    python3 engine/atlas_vignobles_monde.py pays Argentine     # fiche d un pays
    python3 engine/atlas_vignobles_monde.py croisement         # contrôles complets
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import atlas_biomasses_monde as _master  # noqa: E402  (autorité : familles et hubs)
import atlas_biomasses_pays as _pays_v11  # noqa: E402  (autorité : jetons v1.1)

ETIQUETTE_SOURCÉ = "SOURCÉ"
ETIQUETTE_ILLUSTRATION = "ILLUSTRATION"
ETIQUETTE_REEL = "DONNÉES RÉELLES"
ETIQUETTE_A_VERIFIER = "À VÉRIFIER"
ETIQUETTE_A_SOURCER = "À SOURCER"

SOURCE_PRODUCTION = ("productions et surfaces FAOSTAT bulk Production_Crops_Livestock_E, "
                     "item Grapes, valeurs 2024 (mise à jour du 31/12/2025)")
ETQ_GISEMENT_SOURCÉ = "SOURCÉ (production et surface FAOSTAT 2024) + ratio ILLUSTRATION"

MOIS_COURTS = _master.MOIS_COURTS

# ---------------------------------------------------------------------------
# Registre des vignobles : fiche pays (portrait, synthèse réglementaire à cinq
# postes) + intrants. Deux types de points : SARMENT_VIGNE_XX partout (résidu de
# taille ligneux) et MARC_RAISIN_XX pour les dix grands bassins vinicoles (résidu
# de pressurage). Les productions et surfaces sont nationales (FAOSTAT 2024) ; les
# points GPS sont des approximations de région ; les gisements résidus sont
# arithmétiquement dérivés des ratios ILLUSTRATION (2 t/ha de sarments, 15 % de
# la vendange en marc). Deux points sont rattachés à des hubs existants :
# SARMENT_VIGNE_AR (Mendoza, ar-cuyo) et SARMENT_VIGNE_ES (Extremadura,
# es-extremadura).
# ---------------------------------------------------------------------------

VIGNOBLES_MONDE = {

"Afrique du Sud": {
    "nom_fao": "South Africa",
    "portrait": "vignoble du Cap-Occidental (Boland, Stellenbosch, Swartland) sous climat méditerranéen et vent du sud-est (Cape doctor) ; export de vin au long cours ; pinotage emblématique.",
    "reglementation": {
        "brulage": ("les feux agricoles sont encadrés par la loi sur les feux de veld et de forêt (saisons de feu, permis) et les règles régionales de qualité de l'air", ETIQUETTE_A_VERIFIER, "National Veld and Forest Fire Act + règles régionales, à sourcer"),
        "enfouissement": ("broyage au rang standard ; couvre-sol vivant entre les rangs (semis de moutarde, avoine)", ETIQUETTE_A_VERIFIER, "pratique de cave, à sourcer"),
        "traitement": ("coopératives de chais du Boland (compostage, eaux de cave) ; distillation localisée ; pas de filière sarments structurée", ETIQUETTE_A_VERIFIER, "filière vinicole, à sourcer"),
        "cout_agriculture": ("la taille est un coût obligatoire du vignoble ; la mécanisation de la taille progresse", ETIQUETTE_A_VERIFIER, "à sourcer par exploitation"),
        "main_oeuvre": ("taille manuelle dominante ; vendanges mécanisées en plaine, main-d'œuvre saisonnière rurale", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_ZA", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Stellenbosch (Boland, province du Cap-Occidental)", "lat": -33.93, "lon": 18.86,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 1 870 973 t ; vigne : 103 955 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 208 kt/an sur le vignoble national du Cap", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6, 7, 8], "fenetre_note": "taille d'hiver australe : juin-août",
            "techniques": "taille en Guyot ou échalas sur treillis, broyage au rang ; vendanges mécaniques en plaine",
        },
        {
            "token": "MARC_RAISIN_ZA", "famille": "Cultures pérennes", "nom_fr": "Marc de raisin",
            "region": "Paarl (Berg river, Cap-Occidental)", "lat": -33.73, "lon": 18.98,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu humide de pressurage (peaux, pépins, pulpes)",
            "production": "raisins : 1 870 973 t ; vigne : 103 955 ha (2024, FAOSTAT)", "ratio": "marc ≈ 0,15 × vendange (fourchette 0,15-0,25)",
            "gisement": "marc ≈ 281 kt/an, en chais du Cap (vendange à dominante vinicole)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [2, 3, 4], "fenetre_note": "vendanges australes : février-avril",
            "techniques": "pressurage des coopératives du Boland ; compostage de cave établi",
        },
    ],
},

"Allemagne": {
    "nom_fao": "Germany",
    "portrait": "vignobles rhénans de coteaux sur schistes et marnes : Moselle, Rheingau, Rheinhessen (le plus grand) ; riesling dominant ; vendanges tardives d'octobre-novembre ; coteaux entièrement manuels.",
    "reglementation": {
        "brulage": ("le brûlage des résidus verts au champ est restreint par les règlements des Länder ; dérogations phytosanitaires locales exceptionnelles", ETIQUETTE_A_VERIFIER, "règles des Länder, à sourcer"),
        "enfouissement": ("broyage au rang sur les parcelles mécanisables ; les coteaux escarpés se broient sous le rang", ETIQUETTE_A_VERIFIER, "pratique standard, à sourcer"),
        "traitement": ("la distillation des sous-produits de cave est une tradition réglementée (eau-de-vie de marc) ; compostage de cave courant", ETIQUETTE_A_VERIFIER, "réglementation viticole allemande, à sourcer"),
        "cout_agriculture": ("la taille manuelle des coteaux est coûteuse (pentes) ; le broyage au rang est le moindre coût", ETIQUETTE_ILLUSTRATION, "ordre de grandeur"),
        "main_oeuvre": ("coteaux de Moselle entièrement manuels ; plaines de Rheinhessen mécanisées", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_DE", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Bernkastel-Kues (Moselle, coteaux de schiste)", "lat": 49.92, "lon": 7.06,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 1 059 770 t ; vigne : 101 560 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 203 kt/an sur le vignoble national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [2, 3], "fenetre_note": "taille d'hiver sur coteaux : février-mars (gel tardif)",
            "techniques": "taille manuelle sur coteaux de schiste, Guyot double ; relevage printanier",
        },
        {
            "token": "MARC_RAISIN_DE", "famille": "Cultures pérennes", "nom_fr": "Marc de raisin",
            "region": "Ingelheim (Rheinhessen, plaines rhénanes)", "lat": 49.99, "lon": 8.06,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu humide de pressurage (peaux, pépins, pulpes)",
            "production": "raisins : 1 059 770 t ; vigne : 101 560 ha (2024, FAOSTAT)", "ratio": "marc ≈ 0,15 × vendange (fourchette 0,15-0,25)",
            "gisement": "marc ≈ 159 kt/an, en chais (vendange presque entièrement vinicole)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10, 11], "fenetre_note": "vendanges tardives : septembre-novembre",
            "techniques": "pressurage des caves de Rheinhessen ; distillation réglementée des sous-produits",
        },
    ],
},

"Argentine": {
    "nom_fao": "Argentina",
    "portrait": "vignoble de Cuyo (Mendoza : 70 % de la surface ; San Juan) accroché aux contreforts andins, irrigation par aqueducs de fonte (malbec emblématique) ; Salta pour les vignobles d'extrême altitude ; hub ar-cuyo de la flotte (restos-poda).",
    "reglementation": {
        "brulage": ("la Ley 26.562 (2008) encadre les brûlages agricoles : plan de gestion obligatoire, interdiction de fait dans plusieurs provinces ; Mendoza applique des amendes lourdes", ETIQUETTE_REEL, "Ley 26.562 + amendes Mendoza (fiche v0.6)"),
        "enfouissement": ("le broyage-enfouissement au rang est la pratique documentée ; le sarment reste au vignoble", ETIQUETTE_A_VERIFIER, "pratique dominante, à sourcer"),
        "traitement": ("chais du Gran Mendoza ; distillation artisanale ; aucune filière sarments structurée", ETIQUETTE_A_VERIFIER, "filière vinicole, à sourcer"),
        "cout_agriculture": ("la taille est un coût obligatoire du vignoble ; le broyage au rang est le moindre coût", ETIQUETTE_A_VERIFIER, "à sourcer par exploitation"),
        "main_oeuvre": ("taille manuelle qualifiée, main-d'œuvre saisonnière (zafra) régionale et chilienne", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_AR", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Luján de Cuyo (Mendoza, oasis du rio Mendoza — hub ar-cuyo)", "lat": -33.04, "lon": -68.87,
            "type_point": "hub existant", "hubs_flotte": {"ar-cuyo": "restos-poda"},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 1 918 974 t ; vigne : 199 946 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 400 kt/an, bassin andin de Cuyo", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6, 7, 8], "fenetre_note": "taille d'hiver australe : juin-août (hub ar-cuyo, restos-poda)",
            "techniques": "taille en Guyot sur ceps conduits bas, conduite traditionnelle en parral dans les oasis ; broyage au rang",
        },
        {
            "token": "MARC_RAISIN_AR", "famille": "Cultures pérennes", "nom_fr": "Marc de raisin",
            "region": "Maipú (Gran Mendoza, chais de l'oasis)", "lat": -32.93, "lon": -68.77,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu humide de pressurage (peaux, pépins, pulpes)",
            "production": "raisins : 1 918 974 t ; vigne : 199 946 ha (2024, FAOSTAT)", "ratio": "marc ≈ 0,15 × vendange (fourchette 0,15-0,25)",
            "gisement": "marc ≈ 288 kt/an, en chais du Cuyo (vendange à dominante vinicole)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [2, 3, 4], "fenetre_note": "vendanges australes : février-avril (maturité andine précoce)",
            "techniques": "pressurage des chais du Gran Mendoza ; marcs parfois distillés localement",
        },
    ],
},

"Australie": {
    "nom_fao": "Australia",
    "portrait": "vignobles de l'Australie-Méridionale (Barossa, McLaren Vale), du Sunraysia irrigué (Murray Darling) et du sud-est ; vendanges australes de février à avril ; récolte mécanique dominante ; export vers le Royaume-Uni et l'Asie.",
    "reglementation": {
        "brulage": ("les feux agricoles relèvent des permis de feu des comtés en saison à risque ; le brûlage au champ est rare", ETIQUETTE_A_VERIFIER, "règles des comtés et des États, à sourcer"),
        "enfouissement": ("broyage au rang standard, mulch entre les rangs ; pratique universelle", ETIQUETTE_A_VERIFIER, "pratique standard, à sourcer"),
        "traitement": ("grandes wineries de la Barossa et du Sunraysia ; quelques essais de pellets de sarments ; compostage de cave établi", ETIQUETTE_A_VERIFIER, "filière vinicole, à sourcer"),
        "cout_agriculture": ("taille mécanisée dominante sur les vignobles plats irrigués ; le broyage au rang est le moindre coût", ETIQUETTE_A_VERIFIER, "à sourcer par exploitation"),
        "main_oeuvre": ("vendanges nocturnes mécaniques dominantes ; taille en partie sous-traitée", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_AU", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Tanunda (Barossa valley, Australie-Méridionale)", "lat": -34.53, "lon": 138.80,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 1 613 640 t ; vigne : 135 264 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 271 kt/an sur le vignoble national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6, 7, 8], "fenetre_note": "taille d'hiver australe : juin-août",
            "techniques": "taille mécanisée sur vignobles plats, broyage au rang ; vendanges nocturnes mécaniques",
        },
        {
            "token": "MARC_RAISIN_AU", "famille": "Cultures pérennes", "nom_fr": "Marc de raisin",
            "region": "Mildura (Sunraysia, Murray Darling)", "lat": -34.19, "lon": 142.16,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu humide de pressurage (peaux, pépins, pulpes)",
            "production": "raisins : 1 613 640 t ; vigne : 135 264 ha (2024, FAOSTAT)", "ratio": "marc ≈ 0,15 × vendange (fourchette 0,15-0,25)",
            "gisement": "marc ≈ 242 kt/an, en chais et usines de raisin sec du Sunraysia", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [2, 3, 4], "fenetre_note": "vendanges australes : février-avril",
            "techniques": "crush du Sunraysia et de la Barossa ; marcs des grandes wineries et des usines de raisin sec",
        },
    ],
},

"Brésil": {
    "nom_fao": "Brazil",
    "portrait": "deux vignobles en un : la Serra Gaúcha (Rio Grande do Sul) pour le vin, vendange méridionale de février-mars ; la vallée du São Francisco (Pernambouc, Bahia) pour le raisin de table, deux à trois vendanges par an à 9° de latitude sud.",
    "reglementation": {
        "brulage": ("les lois des États sur la qualité de l'air encadrent les brûlages agricoles ; pratique résiduelle dans les petites propriétés", ETIQUETTE_A_VERIFIER, "lois des États, à sourcer"),
        "enfouissement": ("broyage au rang courant ; les sarments servent aussi de combustible domestique dans la Serra Gaúcha", ETIQUETTE_A_VERIFIER, "pratique locale, à sourcer"),
        "traitement": ("caves de la Serra Gaúcha et usines de jus de la vallée du São Francisco ; pas de filière sarments structurée", ETIQUETTE_A_VERIFIER, "filière vinicole, à sourcer"),
        "cout_agriculture": ("le double régime de taille (vallée tropicale) double le coût cultural ; la collecte reste marginale", ETIQUETTE_A_VERIFIER, "à sourcer par exploitation"),
        "main_oeuvre": ("vendanges manuelles dans la Serra Gaúcha ; mécanisées dans la vallée tropicale", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_BR", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Petrolina (vallée du São Francisco, Pernambouc)", "lat": -9.39, "lon": -40.50,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 1 820 104 t ; vigne : 84 380 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 169 kt/an sur le vignoble national (les deux bassins confondus)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [5, 6], "fenetre_note": "taille d'inter-saison : mai-juin, entre deux cycles (vignoble tropical)",
            "techniques": "tailles de relance entre cycles (double régime tropical) sur pergolas ; broyage au rang",
        },
    ],
},

"Chili": {
    "nom_fao": "Chile",
    "portrait": "vignoble andin de 1 400 km irrigué par la fonte des Andes, de l'Elqui au Maule ; exportateur majeur de vin et de raisin de table ; carménère emblématique ; vendanges australes de février à avril.",
    "reglementation": {
        "brulage": ("les brûlages agricoles demandent une autorisation des directions régionales de santé ; périodes d'interdiction saisonnières", ETIQUETTE_A_VERIFIER, "règles régionales, à sourcer"),
        "enfouissement": ("broyage au rang dominant sur les vignobles mécanisés de la vallée centrale", ETIQUETTE_A_VERIFIER, "pratique standard, à sourcer"),
        "traitement": ("chais et piscoeras ; distillation de marcs localisée ; pas de filière sarments structurée", ETIQUETTE_A_VERIFIER, "filière vinicole, à sourcer"),
        "cout_agriculture": ("la taille mécanisée domine en plaine ; le broyage au rang est le moindre coût", ETIQUETTE_A_VERIFIER, "à sourcer par exploitation"),
        "main_oeuvre": ("vendanges mécanisées dans la vallée centrale ; taille manuelle sur les coteaux", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_CL", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Rancagua (vallée centrale, région d'O'Higgins)", "lat": -34.17, "lon": -70.69,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 2 453 897 t ; vigne : 166 457 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 333 kt/an sur le vignoble national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6, 7, 8], "fenetre_note": "taille d'hiver australe : juin-août",
            "techniques": "taille manuelle sur coteaux et mécanisée en plaine ; broyage au rang, vendanges mécaniques nocturnes",
        },
        {
            "token": "MARC_RAISIN_CL", "famille": "Cultures pérennes", "nom_fr": "Marc de raisin",
            "region": "Santa Cruz (vallée de Colchagua)", "lat": -34.39, "lon": -71.61,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu humide de pressurage (peaux, pépins, pulpes)",
            "production": "raisins : 2 453 897 t ; vigne : 166 457 ha (2024, FAOSTAT)", "ratio": "marc ≈ 0,15 × vendange (fourchette 0,15-0,25)",
            "gisement": "marc ≈ 368 kt/an, en chais et piscoeras (part pressée réelle inférieure : le raisin de table n'est pas pressé)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [2, 3, 4], "fenetre_note": "vendanges australes : février-avril",
            "techniques": "pressurage des chais de Colchagua ; distillation de pisco en aval",
        },
    ],
},

"Chine": {
    "nom_fao": "China, mainland",
    "portrait": "premier producteur mondial de raisins (16,8 Mt devant l'Italie et la France) : le Xinjiang concentre la moitié de la surface (raisin de table, de sec et vin), le Ningxia porte la viticulture fine au pied de l'Helan ; marché domestique du vin en recomposition.",
    "reglementation": {
        "brulage": ("le brûlage des résidus est restreint par les réglementations provinciales de qualité de l'air ; les campagnes hivernales anti-smog durcissent les contrôles", ETIQUETTE_A_VERIFIER, "règles provinciales, à sourcer"),
        "enfouissement": ("broyage au rang courant ; les ceps du Xinjiang sont buttés et enterrés contre le gel (buttage mécanisé)", ETIQUETTE_A_VERIFIER, "pratique oasisienne, à sourcer"),
        "traitement": ("quelques chaînes de broyage-compostage près des vignobles de vin ; marché du combustible de sarments anecdotique", ETIQUETTE_A_VERIFIER, "filière émergente, à sourcer"),
        "cout_agriculture": ("main-d'œuvre de taille abondante ; la collecte des sarments reste marginale faute de filière", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("taille manuelle dominante sur les petits vignobles ; mécanisation sur les domaines industrialisés", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_CN", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Turpan (Xinjiang, ceinture oasienne sous le niveau de la mer)", "lat": 42.95, "lon": 89.19,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 16 821 674 t ; vigne : 770 850 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 1,5 Mt/an sur le vignoble national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [3, 4], "fenetre_note": "taille au relevage des ceps hivernés sous terre : mars-avril",
            "techniques": "taille au relevage des ceps hivernés sous terre (Xinjiang), palissage sur espalier ; broyage au rang sur les domaines du Ningxia",
        },
        {
            "token": "MARC_RAISIN_CN", "famille": "Cultures pérennes", "nom_fr": "Marc de raisin",
            "region": "Yinchuan (Ningxia, vignoble au pied de l'Helan)", "lat": 38.47, "lon": 106.23,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu humide de pressurage (peaux, pépins, pulpes)",
            "production": "raisins : 16 821 674 t ; vigne : 770 850 ha (2024, FAOSTAT)", "ratio": "marc ≈ 0,15 × vendange (fourchette 0,15-0,25)",
            "gisement": "marc ≈ 2,5 Mt/an, si toute la vendange était pressée (part vinicole réelle plus faible : table et raisin sec dominants)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [8, 9, 10], "fenetre_note": "vendanges du Ningxia : août-octobre",
            "techniques": "vinification moderne des domaines du Ningxia ; marcs sortant des chais de pied de l'Helan",
        },
    ],
},

"Espagne": {
    "nom_fao": "Spain",
    "portrait": "premier vignoble mondial en surface (904 000 ha) ; la Mancha porte la moitié, l'Extremadura du hub es-extremadura double oliviers et vignes ; Rioja et Ribera del Duero portent l'export ; gobelet sec historique dans l'intérieur.",
    "reglementation": {
        "brulage": ("l'incinération de résidus végétaux au champ est interdite par la Ley 7/2022 (art. 27.3) ; dérogations phytosanitaires exceptionnelles des communautés autonomes", ETIQUETTE_REEL, "Ley 7/2022 art. 27.3 (fiche v0.6)"),
        "enfouissement": ("broyage-enfouissement au rang préconisé et majoritaire dans les appellations", ETIQUETTE_A_VERIFIER, "pratique dominante, à sourcer"),
        "traitement": ("distilleries et lignes de traitement des chais ; les coopératives de la Mancha mutualisent les marcs", ETIQUETTE_A_VERIFIER, "filière vinicole, à sourcer"),
        "cout_agriculture": ("la taille est un coût obligatoire du vignoble ; le broyage au rang est le moindre coût", ETIQUETTE_A_VERIFIER, "à sourcer par exploitation"),
        "main_oeuvre": ("taille manuelle sur les vignes vieilles en gobelet ; machines à tailler sur les vignobles de plaine", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_ES", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Badajoz (Extremadura, bassin du Guadiana — hub es-extremadura)", "lat": 38.88, "lon": -6.97,
            "type_point": "hub existant", "hubs_flotte": {"es-extremadura": "sarments-vigne"},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 5 387 270 t ; vigne : 903 980 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 1,8 Mt/an sur le vignoble national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3], "fenetre_note": "taille d'hiver : janvier-mars",
            "techniques": "taille en gobelet ou en espalier (cordon), mécanisée dans les vignes de plaine ; broyage au rang dominant",
        },
        {
            "token": "MARC_RAISIN_ES", "famille": "Cultures pérennes", "nom_fr": "Marc de raisin",
            "region": "Almagro (La Mancha, Castille-La Manche)", "lat": 38.89, "lon": -3.71,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu humide de pressurage (peaux, pépins, pulpes)",
            "production": "raisins : 5 387 270 t ; vigne : 903 980 ha (2024, FAOSTAT)", "ratio": "marc ≈ 0,15 × vendange (fourchette 0,15-0,25)",
            "gisement": "marc ≈ 808 kt/an, en chais (vendange à dominante vinicole)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [8, 9, 10], "fenetre_note": "vendanges de la Mancha (précoces) et de Rioja : août-octobre",
            "techniques": "pressurage des bodegas de la Mancha et de Rioja ; coopératives mutualisent les marcs",
        },
    ],
},

"Grèce": {
    "nom_fao": "Greece",
    "portrait": "vignoble méditerranéen millénaire : Péloponnèse (Nemea), Crète, Macédoine et îles (panier kouloura de Santorin) ; raisin de table et corinthe sèche majoritaires ; distillation traditionnelle de tsipouro.",
    "reglementation": {
        "brulage": ("les permis communaux de brûlage sont encadrés ; la pratique est en régression", ETIQUETTE_A_VERIFIER, "règles communales, à sourcer"),
        "enfouissement": ("broyage au rang courant sur le continent ; terrasses et îles broyées sous le rang", ETIQUETTE_A_VERIFIER, "pratique standard, à sourcer"),
        "traitement": ("coopératives et usines de raisin sec (corinthe) concentrent les déchets de tri ; distillation de tsipouro traditionnelle", ETIQUETTE_A_VERIFIER, "filières vinicoles, à sourcer"),
        "cout_agriculture": ("la taille manuelle des formes traditionnelles (kouloura) coûteuse ; le vignoble de plaine se mécanise", ETIQUETTE_A_VERIFIER, "à sourcer par exploitation"),
        "main_oeuvre": ("taille manuelle des formes traditionnelles ; vendanges manuelles sur les îles", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_GR", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Nemea (Péloponnèse, Argolide)", "lat": 37.81, "lon": 22.66,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 777 210 t ; vigne : 83 560 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 167 kt/an sur le vignoble national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2], "fenetre_note": "taille d'hiver : janvier-février",
            "techniques": "taille manuelle des formes traditionnelles (gobelet, panier kouloura de Santorin)",
        },
        {
            "token": "MARC_RAISIN_GR", "famille": "Cultures pérennes", "nom_fr": "Marc de raisin",
            "region": "Héraklion (Crète, chais et usines de raisin sec)", "lat": 35.34, "lon": 25.13,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu humide de pressurage (peaux, pépins, pulpes)",
            "production": "raisins : 777 210 t ; vigne : 83 560 ha (2024, FAOSTAT)", "ratio": "marc ≈ 0,15 × vendange (fourchette 0,15-0,25)",
            "gisement": "marc ≈ 117 kt/an, en chais et usines de raisin sec (part vinicole réelle plus faible)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [8, 9, 10], "fenetre_note": "vendanges de table et de chai : août-octobre",
            "techniques": "pressurage des coopératives et usines de raisin sec ; distillation de tsipouro traditionnelle",
        },
    ],
},

"Géorgie": {
    "nom_fao": "Georgia",
    "portrait": "berceau de la viniculture (huit mille ans de continuité) : la Kahétie concentre la moitié du vignoble, fermentation en qvevri (jarre de terre cuite) inscrite au patrimoine immatériel ; vendanges communautaires (rtveli) de septembre-octobre.",
    "reglementation": {
        "brulage": ("le brûlage des résidus est restreint par les règles environnementales ; pratique résiduelle", ETIQUETTE_A_VERIFIER, "règles nationales, à sourcer"),
        "enfouissement": ("broyage au rang ; les sarments servent aussi de combustible domestique dans les campagnes de Kahétie", ETIQUETTE_A_VERIFIER, "pratique locale, à sourcer"),
        "traitement": ("les marani (celliers familiaux) concentrent les marcs ; distillation traditionnelle (tchatcha)", ETIQUETTE_A_VERIFIER, "tradition vinicole, à sourcer"),
        "cout_agriculture": ("la taille manuelle domine sur les coteaux de l'Alazani ; coût cultural maîtrisé par la main-d'œuvre familiale", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("vendanges communautaires (rtveli) manuelles ; qvevri entretenus en famille", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_GE", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Telavi (Kahétie, vallée de l'Alazani)", "lat": 41.92, "lon": 45.48,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 320 700 t ; vigne : 49 570 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 99 kt/an sur le vignoble national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3], "fenetre_note": "taille d'hiver : janvier-mars",
            "techniques": "taille manuelle des coteaux de l'Alazani, ceps conduits bas ; sarments souvent conservés comme tuteurs et bois de chauffe",
        },
    ],
},

"Inde": {
    "nom_fao": "India",
    "portrait": "quatrième production mondiale, presque entièrement raisin de table (Nashik, Maharashtra, au cœur de la ceinture) ; double régime de taille (fondation et relance) pour les vendanges décalées ; exports de contre-saison vers l'Europe et le Golfe.",
    "reglementation": {
        "brulage": ("le brûlage des résidus est restreint par les réglementations des États sur la qualité de l'air ; pratique résiduelle", ETIQUETTE_A_VERIFIER, "règles des États, à sourcer"),
        "enfouissement": ("les sarments servent de combustible domestique ou de tuteurs ; le broyage au rang progresse", ETIQUETTE_A_VERIFIER, "pratique locale, à sourcer"),
        "traitement": ("filière non structurée ; quelques essais de granulés près de Nashik ; stations de conditionnement d'exportation", ETIQUETTE_A_VERIFIER, "filière émergente, à sourcer"),
        "cout_agriculture": ("main-d'œuvre abondante ; la collecte vaut surtout comme bois de chauffe", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("taille manuelle dominante ; vendanges manuelles escaladées", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_IN", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Nashik (Maharashtra, ceinture de la vigne)", "lat": 19.99, "lon": 73.79,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 3 904 287 t ; vigne : 179 629 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 359 kt/an sur le vignoble national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [4, 10], "fenetre_note": "double régime : fondation (octobre), relance (avril)",
            "techniques": "taille fondation (octobre) et relance (avril) sur pergolas en Y ; vendanges manuelles escaladées",
        },
    ],
},

"Iran": {
    "nom_fao": "Iran (Islamic Republic of)",
    "portrait": "vignoble ancien du nord-ouest et du centre (Urmia, Takestan) : raisin de table et de sec dominants, pergolas de cour ; pas de vinification (production fruitière et fermentée hors alcool).",
    "reglementation": {
        "brulage": ("restrictions administratives sur le brûlage des résidus ; pratique résiduelle", ETIQUETTE_A_VERIFIER, "règles nationales, à sourcer"),
        "enfouissement": ("le sarment est le bois de chauffe des campagnes (pergolas de Takestan) ; broyage au rang marginal", ETIQUETTE_A_VERIFIER, "pratique locale, à sourcer"),
        "traitement": ("filière non structurée ; le séchage du raisin (kismis) concentre les déchets de tri", ETIQUETTE_A_VERIFIER, "filière de séchage, à sourcer"),
        "cout_agriculture": ("la collecte vaut comme combustible domestique ; pas de filière payante", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("taille manuelle généralisée ; pergolas de cour entretenues en famille", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_IR", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Takestan (Qazvin, bassin viticole historique)", "lat": 36.07, "lon": 49.69,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 1 566 663 t ; vigne : 119 275 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 239 kt/an sur le vignoble national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3], "fenetre_note": "taille d'hiver : janvier-mars",
            "techniques": "taille manuelle des pergolas ; raisin de table et séchage en adobes",
        },
    ],
},

"Maroc": {
    "nom_fao": "Morocco",
    "portrait": "vignoble reconstitué du Saïss et de l'Oriental (hub Al-Atlas à Meknès) : Guerrouane près de Meknès, Berkane ; carignan et cinsault historiques, cépages internationaux en montée ; vendanges précoces d'août à octobre.",
    "reglementation": {
        "brulage": ("le brûlage des résidus au champ est réglementé dans le cadre de la gestion des déchets et des arrêtés du ministère de l'agriculture (interdictions en période de vent)", ETIQUETTE_REEL, "Loi 28-00 + arrêtés (fiche v0.6)"),
        "enfouissement": ("broyage au rang ; les sarments servent de combustible domestique dans les campagnes du Saïss", ETIQUETTE_A_VERIFIER, "pratique locale, à sourcer"),
        "traitement": ("caves de Meknès et de l'Oriental ; pas de filière sarments structurée", ETIQUETTE_A_VERIFIER, "filière vinicole, à sourcer"),
        "cout_agriculture": ("la taille est un coût obligatoire du vignoble ; la collecte des sarments n'a pas de filière", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("taille manuelle dominante ; vendanges manuelles et précoces (août)", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_MA", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Guerrouane (côteaux du Saïss, à l'est de Meknès)", "lat": 33.80, "lon": -5.20,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 339 673 t ; vigne : 40 032 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 80 kt/an sur le vignoble national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2], "fenetre_note": "taille d'hiver : janvier-février",
            "techniques": "taille en gobelet bas, vendanges précoces (août) ; broyage au rang ou combustible domestique",
        },
    ],
},

"Moldavie": {
    "nom_fao": "Republic of Moldova",
    "portrait": "le vignoble par habitant le plus dense du continent : plaines entre Prut et Dniestr (Codru), caves et tunnels de Cricova ; vin et divin (brandy) ; vendanges de septembre-octobre.",
    "reglementation": {
        "brulage": ("restrictions réglementaires sur le brûlage ; le sarment sert surtout de combustible domestique", ETIQUETTE_A_VERIFIER, "règles nationales, à sourcer"),
        "enfouissement": ("broyage au rang courant sur les vignobles de plaine", ETIQUETTE_A_VERIFIER, "pratique standard, à sourcer"),
        "traitement": ("caves et tunnels de Cricova concentrent les marcs ; distillation traditionnelle (divin)", ETIQUETTE_A_VERIFIER, "filière vinicole, à sourcer"),
        "cout_agriculture": ("vignoble mécanisable, coûts culturels bas ; la taille reste manuelle sur les petites exploitations", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("vendanges manuelles dominantes ; main-d'œuvre rurale abondante", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_MD", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Cricova (banlieue de Chișinău, Codru)", "lat": 47.16, "lon": 28.86,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 396 400 t ; vigne : 72 601 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 145 kt/an sur le vignoble national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [2, 3], "fenetre_note": "taille d'hiver : février-mars",
            "techniques": "taille manuelle mécanisable sur plaines ; vendanges manuelles dominantes",
        },
    ],
},

"Nouvelle-Zélande": {
    "nom_fao": "New Zealand",
    "portrait": "sauvignon blanc de Marlborough (les trois quarts du volume, île du Sud) ; vendanges de mars-avril ; viticulture de précision mécanisée ; Hawke's Bay pour les rouges.",
    "reglementation": {
        "brulage": ("les règles régionales de l'air (Marlborough) découragent le brûlage au champ ; permis requis", ETIQUETTE_A_VERIFIER, "règles régionales, à sourcer"),
        "enfouissement": ("broyage au rang universellement pratiqué (rang larges, vignes mécanisables)", ETIQUETTE_A_VERIFIER, "pratique universelle, à sourcer"),
        "traitement": ("les chais de Marlborough mutualisent compost et eaux de cave ; pas de filière sarments", ETIQUETTE_A_VERIFIER, "filière vinicole, à sourcer"),
        "cout_agriculture": ("la taille mécanisée progresse ; la main-d'œuvre saisonnière est coûteuse (schemes de visa reconnus)", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("vendanges mécaniques nocturnes dominantes ; taille en partie manuelle sous contrat", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_NZ", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Blenheim (Marlborough, île du Sud)", "lat": -41.51, "lon": 173.96,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 395 000 t ; vigne : 37 627 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 75 kt/an sur le vignoble national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6, 7, 8], "fenetre_note": "taille d'hiver australe : juin-août",
            "techniques": "taille mécanisée en progression sur rangs larges, broyage au rang universel",
        },
    ],
},

"Portugal": {
    "nom_fao": "Portugal",
    "portrait": "vignoble atlantique et douroien : Douro (porto, terrasses de schiste), Vinho Verde au nord-ouest, Alentejo dans le sud plat ; 250 cépages autochtones ; vendanges de septembre-octobre.",
    "reglementation": {
        "brulage": ("le brûlage des résidus agricoles est encadré par les municipalités ; pratique rare en viticulture", ETIQUETTE_A_VERIFIER, "règles municipales, à sourcer"),
        "enfouissement": ("broyage au rang dominant ; sur les terrasses du Douro le broyage reste sous le rang", ETIQUETTE_A_VERIFIER, "pratique standard, à sourcer"),
        "traitement": ("les chais du porto (Vila Nova de Gaia) concentrent les marcs ; distillation réglementée pour les eaux-de-vie", ETIQUETTE_A_VERIFIER, "filière du porto, à sourcer"),
        "cout_agriculture": ("la taille manuelle des terrasses est coûteuse ; les plaines de l'Alentejo se mécanisent", ETIQUETTE_A_VERIFIER, "à sourcer par exploitation"),
        "main_oeuvre": ("terrasses manuelles ; plaines de l'Alentejo mécanisées", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_PT", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Peso da Régua (Douro, terrasses du fleuve)", "lat": 41.16, "lon": -7.79,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 917 890 t ; vigne : 173 210 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 346 kt/an sur le vignoble national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3], "fenetre_note": "taille d'hiver : janvier-mars",
            "techniques": "taille manuelle des terrasses douro étiennes (socalcos), Guyot en plaine ; broyage au rang",
        },
        {
            "token": "MARC_RAISIN_PT", "famille": "Cultures pérennes", "nom_fr": "Marc de raisin",
            "region": "Vila Nova de Gaia (chais du porto)", "lat": 41.13, "lon": -8.62,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu humide de pressurage (peaux, pépins, pulpes)",
            "production": "raisins : 917 890 t ; vigne : 173 210 ha (2024, FAOSTAT)", "ratio": "marc ≈ 0,15 × vendange (fourchette 0,15-0,25)",
            "gisement": "marc ≈ 138 kt/an, en chais et lagares du Douro", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10], "fenetre_note": "vendanges du Douro : septembre-octobre",
            "techniques": "lagares et chais du Douro ; marcs distillés pour les eaux-de-vie (réglementation du porto)",
        },
    ],
},

"Pérou": {
    "nom_fao": "Peru",
    "portrait": "vignobles désertiques d'Ica et de la côte sud, irrigués par les aquifères andins : raisin de table d'exportation (contre-saison nord-américaine) et pisco ; cycles continus, pic de vendange en février-mars.",
    "reglementation": {
        "brulage": ("décrets contre les brûlages (qualité de l'air de la côte) ; pratique rare dans les oasis", ETIQUETTE_A_VERIFIER, "règles régionales, à sourcer"),
        "enfouissement": ("broyage au rang courant dans les vignes industrielles d'Ica", ETIQUETTE_A_VERIFIER, "pratique standard, à sourcer"),
        "traitement": ("caves de pisco et stations d'exportation de raisin de table ; pas de filière sarments", ETIQUETTE_A_VERIFIER, "filières locales, à sourcer"),
        "cout_agriculture": ("la taille est intégrée au calendrier à cycles continus ; coût cultural maîtrisé", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("main-d'œuvre locale abondante ; vendanges manuelles sélectives", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_PE", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Ica (oasis du désert côtier, Huacachina)", "lat": -14.07, "lon": -75.73,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 948 131 t ; vigne : 36 811 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 74 kt/an sur le vignoble national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [6, 7], "fenetre_note": "taille d'hiver austral courte : juin-juillet (cycles continus)",
            "techniques": "taille au calendrier des cycles continus, pergolas de plaine désertique irriguée au goutte-à-goutte",
        },
    ],
},

"Roumanie": {
    "nom_fao": "Romania",
    "portrait": "un des premiers vignobles de l'Union européenne en surface (162 000 ha) : Dealul Mare (subcarpates), Moldavie roumaine, Transylvanie ; cépages autochtones (fetească) ; vendanges de septembre-octobre.",
    "reglementation": {
        "brulage": ("le brûlage des résidus est restreint par la réglementation environnementale ; pratique persistante dans les petites exploitations", ETIQUETTE_A_VERIFIER, "règles nationales, à sourcer"),
        "enfouissement": ("broyage au rang dominant sur les coteaux et les plaines", ETIQUETTE_A_VERIFIER, "pratique standard, à sourcer"),
        "traitement": ("caves de Dealul Mare et de Moldavie ; distillation traditionnelle (vinars)", ETIQUETTE_A_VERIFIER, "filière vinicole, à sourcer"),
        "cout_agriculture": ("la taille manuelle domine ; coût cultural maîtrisé par la main-d'œuvre locale", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("vendanges manuelles des coteaux ; main-d'œuvre saisonnière locale", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_RO", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Buzău (Dealul Mare, subcarpates de courbure)", "lat": 45.15, "lon": 26.83,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 704 160 t ; vigne : 161 930 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 324 kt/an sur le vignoble national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [2, 3], "fenetre_note": "taille d'hiver : février-mars",
            "techniques": "taille manuelle en Guyot sur coteaux ; vendanges manuelles de proximité",
        },
    ],
},

"Russie": {
    "nom_fao": "Russian Federation",
    "portrait": "vignobles du Kouban (Krasnodar, mer Noire) et du Daghestan ; surfaces en progression depuis les années 2010 ; cépages résistants au froid ; vendanges de septembre-octobre.",
    "reglementation": {
        "brulage": ("règlements régionaux (Krasnodar) sur les brûlages ; pratique résiduelle", ETIQUETTE_A_VERIFIER, "règles régionales, à sourcer"),
        "enfouissement": ("broyage au rang ; la protection hivernale des ceps (buttage) mobilise le sol plutôt que le résidu", ETIQUETTE_A_VERIFIER, "pratique locale, à sourcer"),
        "traitement": ("filière locale naissante ; quelques distilleries de marcs", ETIQUETTE_A_VERIFIER, "filière émergente, à sourcer"),
        "cout_agriculture": ("la taille manuelle domine ; la saison courte concentre les opérations", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("vendanges en partie manuelles ; saison courte, équipements en progression", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_RU", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Krasnodar (Kouban, littoral de la mer Noire)", "lat": 45.04, "lon": 38.98,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 823 136 t ; vigne : 76 587 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 153 kt/an sur le vignoble national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [3, 4], "fenetre_note": "taille de printemps : mars-avril (gelées hivernales)",
            "techniques": "taille manuelle printanière, ceps protégés par buttage hivernal",
        },
    ],
},

"Turquie": {
    "nom_fao": "Türkiye",
    "portrait": "cinquième producteur mondial, premier producteur de raisin sec (sultane de Smyrne) : Égée intérieure (Manisa) pour le sec, Thrace et Cappadoce pour le vin ; vignes en gobelet bas conduites en sec.",
    "reglementation": {
        "brulage": ("arrêtés provinciaux contre le brûlage des résidus ; pratique persistante dans les vignobles secs", ETIQUETTE_A_VERIFIER, "arrêtés provinciaux, à sourcer"),
        "enfouissement": ("le sarment sert de combustible domestique dominant dans les campagnes anatoliennes ; broyage au rang marginal", ETIQUETTE_A_VERIFIER, "pratique locale, à sourcer"),
        "traitement": ("pas de filière structurée ; les coopératives de raisin sec concentrent les déchets de tri", ETIQUETTE_A_VERIFIER, "filière du sec, à sourcer"),
        "cout_agriculture": ("la vigne en gobelet bas se taille à la serpe ; coût cultural faible", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("taille manuelle généralisée (serpe), vendanges manuelles", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_TR", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Manisa (Égée intérieure, bassin du sultanine)", "lat": 38.62, "lon": 27.43,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 3 468 000 t ; vigne : 372 285 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 745 kt/an sur le vignoble national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [12, 1, 2], "fenetre_note": "taille d'hiver : décembre-février",
            "techniques": "gobelets bas taillés à la serpe, vignobles secs non irrigués ; le sarment sert de bois de chauffe",
        },
    ],
},

"Égypte": {
    "nom_fao": "Egypt",
    "portrait": "vignoble irrigué du delta et des terres nouvelles (Noubariya) : raisin de table exporté vers l'Europe en contre-saison, vendanges précoces (mai-juin) par forçage cultural ; vin discret.",
    "reglementation": {
        "brulage": ("le brûlage des résidus est restreint par la réglementation sur la pollution de l'air ; interdictions en période de vent", ETIQUETTE_A_VERIFIER, "règles de qualité de l'air, à sourcer"),
        "enfouissement": ("les sarments servent de combustible domestique dominant dans les campagnes ; broyage au rang marginal", ETIQUETTE_A_VERIFIER, "pratique locale, à sourcer"),
        "traitement": ("filière non structurée ; les stations de conditionnement d'exportation concentrent les déchets de tri", ETIQUETTE_A_VERIFIER, "filière d'exportation, à sourcer"),
        "cout_agriculture": ("main-d'œuvre abondante ; la taille est manuelle et intégrée aux opérations", ETIQUETTE_A_VERIFIER, "à sourcer"),
        "main_oeuvre": ("taille et vendanges manuelles ; main-d'œuvre agricole rurale abondante", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_EG", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Noubariya (Béhéira, terres nouvelles du delta)", "lat": 30.68, "lon": 30.32,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 1 696 018 t ; vigne : 80 078 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 160 kt/an sur le vignoble national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [11, 12], "fenetre_note": "taille de novembre-décembre pour la vendange de printemps (forçage)",
            "techniques": "taille manuelle sur pergolas, irrigation au goutte-à-goutte ; forçage de la précocité pour l'export",
        },
    ],
},

"États-Unis": {
    "nom_fao": "United States of America",
    "portrait": "quatrième production mondiale, dominée par la Californie (vallée centrale : vin, raisin de table et de sec) ; Washington, Oregon et l'État de New York complètent la carte ; viticulture industrialisée de précision.",
    "reglementation": {
        "brulage": ("les districts californiens de gestion de la qualité de l'air encadrent les brûlages agricoles (permis, jours alloués, saisons d'interdiction)", ETIQUETTE_A_VERIFIER, "règles des districts de qualité de l'air, à sourcer"),
        "enfouissement": ("broyage au rang standard entre les vignes mécanisées", ETIQUETTE_A_VERIFIER, "pratique standard, à sourcer"),
        "traitement": ("compostage de chais développé dans la Napa Valley ; distillation marginale ; quelques essais de valorisation énergétique", ETIQUETTE_A_VERIFIER, "filière vinicole, à sourcer"),
        "cout_agriculture": ("la taille mécanisée réduit le coût ; l'andainage optionnel reste marginal", ETIQUETTE_A_VERIFIER, "à sourcer par exploitation"),
        "main_oeuvre": ("taille en partie mécanisée ; vendanges mécaniques nocturnes pour le vin de milieu de gamme", ETIQUETTE_ILLUSTRATION, "constat documentaire"),
    },
    "intrants": [
        {
            "token": "SARMENT_VIGNE_US", "famille": "Cultures pérennes", "nom_fr": "Sarments de vigne (taille)",
            "region": "Modesto (vallée centrale de Californie)", "lat": 37.64, "lon": -120.99,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu de taille ligneux sec (sarments)",
            "production": "raisins : 4 902 250 t ; vigne : 373 529 ha (2024, FAOSTAT)", "ratio": "sarments ≈ 1,5 à 3 t/ha/an (retenu : 2 t/ha)",
            "gisement": "sarments ≈ 747 kt/an sur le vignoble national", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [1, 2, 3], "fenetre_note": "taille d'hiver : janvier-mars",
            "techniques": "taille mécanisée avec pré-ébourgeonnage sur les vignes californiennes ; broyage au rang standard",
        },
        {
            "token": "MARC_RAISIN_US", "famille": "Cultures pérennes", "nom_fr": "Marc de raisin",
            "region": "Napa (comté de Napa, Californie du Nord)", "lat": 38.50, "lon": -122.42,
            "type_point": "point candidat", "hubs_flotte": {},
            "type_biomasse": "résidu humide de pressurage (peaux, pépins, pulpes)",
            "production": "raisins : 4 902 250 t ; vigne : 373 529 ha (2024, FAOSTAT)", "ratio": "marc ≈ 0,15 × vendange (fourchette 0,15-0,25)",
            "gisement": "marc ≈ 735 kt/an, en chais et usines (la part pressée exclut le raisin de table et de sec)", "etiquette_gisement": ETQ_GISEMENT_SOURCÉ,
            "fenetre": [9, 10], "fenetre_note": "crush californien : septembre-octobre",
            "techniques": "crush californien de grande capacité ; marcs des wineries de la vallée centrale et de Napa",
        },
    ],
},

}

def _index():
    """(pays, intrant) pour chaque token."""
    idx = {}
    for pays, fiche in VIGNOBLES_MONDE.items():
        for intrant in fiche["intrants"]:
            idx[intrant["token"]] = (pays, intrant)
    return idx

INDEX = _index()


def _verifier_structure(problemes):
    idx = {}
    for pays, fiche in VIGNOBLES_MONDE.items():
        for cle in ("nom_fao", "portrait", "reglementation", "intrants"):
            if cle not in fiche:
                problemes.append("pays %s : champ manquant %s" % (pays, cle))
        if len(fiche.get("intrants", [])) < 1:
            problemes.append("pays %s : aucun intrant" % pays)
        for cle in _master.CLEFS_REGLEMENTATION:
            if cle not in fiche["reglementation"]:
                problemes.append("pays %s : poste de réglementation manquant %s" % (pays, cle))
        sarments = [i["token"] for i in fiche.get("intrants", []) if i["token"].startswith("SARMENT_VIGNE_")]
        marcs = [i["token"] for i in fiche.get("intrants", []) if i["token"].startswith("MARC_RAISIN_")]
        if len(sarments) != 1:
            problemes.append("pays %s : %d point sarments (attendu : 1)" % (pays, len(sarments)))
        if len(marcs) > 1:
            problemes.append("pays %s : %d points marc (attendu : 0 ou 1)" % (pays, len(marcs)))
        for intrant in fiche["intrants"]:
            tok = intrant.get("token")
            if not tok:
                problemes.append("pays %s : intrant sans token" % pays)
                continue
            if tok in idx:
                problemes.append("token dupliqué : %s" % tok)
            idx[tok] = (pays, intrant)
            for cle in ("famille", "nom_fr", "region", "lat", "lon", "type_point",
                        "type_biomasse", "production", "ratio", "gisement",
                        "etiquette_gisement", "fenetre", "fenetre_note", "techniques"):
                if cle not in intrant:
                    problemes.append("%s : champ manquant %s" % (tok, cle))
            lat, lon = intrant.get("lat"), intrant.get("lon")
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                problemes.append("%s : GPS hors bornes %s, %s" % (tok, lat, lon))
            for mois in intrant.get("fenetre", []):
                if not 1 <= mois <= 12:
                    problemes.append("%s : mois hors bornes %s" % (tok, mois))
            # Cohérence hémisphérique (hors ceinture tropicale, double régime) :
            # hémisphère Sud : taille en mai-septembre, vendange en janvier-mai ;
            # hémisphère Nord : taille d'octobre à avril, vendange de juillet à novembre.
            if abs(lat) > 23.5:
                if lat < 0:
                    attendus = {5, 6, 7, 8, 9} if tok.startswith("SARMENT_VIGNE_") else {1, 2, 3, 4, 5}
                else:
                    attendus = {10, 11, 12, 1, 2, 3, 4} if tok.startswith("SARMENT_VIGNE_") else {7, 8, 9, 10, 11}
                for mois in intrant.get("fenetre", []):
                    if mois not in attendus:
                        problemes.append("%s : mois %d incohérent avec la latitude %.2f" % (tok, mois, lat))
    return idx


def verifier_couverture():
    """Contrôles complets : structure, alignement master v1.0 et atlas v1.1, hubs."""
    problemes = []
    idx = _verifier_structure(problemes)

    familles_master = {f["famille"] for f in _master.ATLAS_BIOMASSES_MONDE.values()}
    tokens_master = set(_master.ATLAS_BIOMASSES_MONDE.keys())
    tokens_v11 = set(_pays_v11.INDEX.keys())
    hubs_master = set()
    for f in _master.ATLAS_BIOMASSES_MONDE.values():
        for hub in (f.get("hubs_flotte") or {}):
            hubs_master.add(hub)

    for tok, (pays, intrant) in sorted(idx.items()):
        if intrant["famille"] not in familles_master:
            problemes.append("%s : famille hors master %s" % (tok, intrant["famille"]))
        if tok in tokens_master:
            problemes.append("token en collision avec le master v1.0 : %s" % tok)
        if tok in tokens_v11:
            problemes.append("token en collision avec l'atlas v1.1 : %s" % tok)
        if intrant["type_point"] not in ("hub existant", "point candidat"):
            problemes.append("%s : type_point inconnu %s" % (tok, intrant["type_point"]))
        for hub in (intrant.get("hubs_flotte") or {}):
            if hub not in hubs_master:
                problemes.append("%s : hub inconnu %s" % (tok, hub))
        if intrant["type_point"] == "hub existant" and not intrant.get("hubs_flotte"):
            problemes.append("%s : point hub sans rattachement hubs_flotte" % tok)

    return problemes


def sommaire():
    lignes = ["Atlas des vignobles du monde — World Twin v1.2",
              " Productions et surfaces FAOSTAT 2024 SOURCÉES ; ratios résidus ILLUSTRATION ;",
              " points GPS approximations de région ; doctrine PI (aucun paramètre VDE).", ""]
    total = 0
    for pays in sorted(VIGNOBLES_MONDE, key=lambda p: p.lower()):
        fiche = VIGNOBLES_MONDE[pays]
        lignes.append("%s (%s) — %d intrants" % (pays, fiche["nom_fao"], len(fiche["intrants"])))
        for intrant in fiche["intrants"]:
            lignes.append("  %-18s %-16s %-28s %s" % (
                intrant["token"], intrant["famille"], intrant["nom_fr"],
                " / ".join(MOIS_COURTS[m] for m in intrant["fenetre"])))
        total += len(fiche["intrants"])
        lignes.append("")
    lignes.insert(3, " Pays : %d — intrants : %d" % (len(VIGNOBLES_MONDE), total))
    return "\n".join(lignes)


def fiche_token(token):
    if token not in INDEX:
        return None
    pays, intrant = INDEX[token]
    fiche_pays = VIGNOBLES_MONDE[pays]
    lignes = ["%s — %s" % (intrant["token"], intrant["nom_fr"]), ""]
    lignes.append("Pays : %s (%s)" % (pays, fiche_pays["nom_fao"]))
    lignes.append("Famille : %s" % intrant["famille"])
    lignes.append("Localisation : %s — GPS %.2f, %.2f, approximation de région. Point : %s%s" % (
        intrant["region"], intrant["lat"], intrant["lon"], intrant["type_point"],
        " (rattaché : %s)" % ", ".join(intrant["hubs_flotte"]) if intrant.get("hubs_flotte") else ""))
    lignes.append("Type de biomasse : %s" % intrant["type_biomasse"])
    lignes.append("Volumes : %s [%s]" % (intrant["production"], SOURCE_PRODUCTION))
    lignes.append("Ratio résidu : %s" % intrant["ratio"])
    lignes.append("Gisement : %s [%s]" % (intrant["gisement"], intrant["etiquette_gisement"]))
    lignes.append("Fenêtre saisonnière : %s — %s" % (
        ", ".join(MOIS_COURTS[m] for m in intrant["fenetre"]), intrant["fenetre_note"]))
    lignes.append("Techniques : %s" % intrant["techniques"])
    lignes.append("")
    lignes.append("Réglementation %s (synthèse pays) :" % pays)
    for cle in _master.CLEFS_REGLEMENTATION:
        texte, etiquette, ref = fiche_pays["reglementation"][cle]
        lignes.append("  %s [%s] : %s (réf. %s)" % (cle, etiquette, texte, ref))
    return "\n".join(lignes)


def fiche_pays(nom):
    cible = None
    for pays in VIGNOBLES_MONDE:
        if nom.lower() in (pays.lower(), VIGNOBLES_MONDE[pays]["nom_fao"].lower()) or nom.lower() == pays.lower():
            cible = pays
            break
    if cible is None:
        return None
    fiche = VIGNOBLES_MONDE[cible]
    lignes = ["%s (%s) — atlas des vignobles du monde" % (cible, fiche["nom_fao"]), ""]
    lignes.append("Portrait : %s" % fiche["portrait"])
    lignes.append("")
    lignes.append("Réglementation (synthèse à cinq postes) :")
    for cle in _master.CLEFS_REGLEMENTATION:
        texte, etiquette, ref = fiche["reglementation"][cle]
        lignes.append("  %s [%s] : %s (réf. %s)" % (cle, etiquette, texte, ref))
    lignes.append("")
    lignes.append("Intrants (%d) :" % len(fiche["intrants"]))
    for intrant in fiche["intrants"]:
        lignes.append("  %-18s %-16s %s" % (intrant["token"], intrant["famille"], intrant["nom_fr"]))
        lignes.append("    %s — GPS %.2f, %.2f [%s]" % (intrant["region"], intrant["lat"], intrant["lon"], intrant["type_point"]))
        lignes.append("    %s" % intrant["gisement"])
        lignes.append("    fenêtre : %s (%s)" % (
            ", ".join(MOIS_COURTS[m] for m in intrant["fenetre"]), intrant["fenetre_note"]))
    return "\n".join(lignes)


def croisement():
    problemes = verifier_couverture()
    lignes = ["Croisement v1.2 — contrôles complets", ""]
    lignes.append("Pays viticoles couverts : %d" % len(VIGNOBLES_MONDE))
    lignes.append("Intrants vignobles : %d (master v1.0 : %d ; atlas v1.1 : %d)" % (
        len(INDEX), len(_master.ATLAS_BIOMASSES_MONDE), len(_pays_v11.INDEX)))
    familles_v12 = {i["famille"] for (_, i) in INDEX.values()}
    familles_master = {f["famille"] for f in _master.ATLAS_BIOMASSES_MONDE.values()}
    lignes.append("Familles v1.2 ⊆ familles master : %s" % ("OK" if familles_v12 <= familles_master else "ECART"))
    lignes.append("Familles représentées : %s" % ", ".join(sorted(familles_v12)))
    collision_m = set(INDEX) & set(_master.ATLAS_BIOMASSES_MONDE)
    collision_11 = set(INDEX) & set(_pays_v11.INDEX)
    lignes.append("Collision de tokens avec le master v1.0 : %s" % ("AUCUNE" if not collision_m else ", ".join(sorted(collision_m))))
    lignes.append("Collision de tokens avec l'atlas v1.1 : %s" % ("AUCUNE" if not collision_11 else ", ".join(sorted(collision_11))))
    sarments = sum(1 for i in INDEX.values() if i[1]["token"].startswith("SARMENT_VIGNE_"))
    marcs = sum(1 for i in INDEX.values() if i[1]["token"].startswith("MARC_RAISIN_"))
    lignes.append("Points sarments : %d — points marcs : %d" % (sarments, marcs))
    hubs_points = [(tok, p, i["hubs_flotte"]) for tok, (p, i) in sorted(INDEX.items()) if i["type_point"] == "hub existant"]
    lignes.append("Points rattachés à un hub existant : %d — %s" % (len(hubs_points),
                  ", ".join("%s→%s" % (tok, ",".join(sorted(hubs))) for tok, _, hubs in hubs_points)))
    if problemes:
        lignes.append("")
        lignes.append("PROBLÈMES DÉTECTÉS (%d) :" % len(problemes))
        lignes.extend("  - %s" % p for p in problemes)
        lignes.append("")
        lignes.append("CROISEMENT : ECHEC")
        return "\n".join(lignes), 1
    lignes.append("")
    lignes.append("CROISEMENT : OK — toutes les gardes passent.")
    return "\n".join(lignes), 0


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print(sommaire())
        return 0
    if args[0] == "croisement":
        texte, code = croisement()
        print(texte)
        return code
    if args[0] == "pays" and len(args) >= 2:
        texte = fiche_pays(" ".join(args[1:]))
        if texte is None:
            print("Pays inconnu. Pays disponibles : %s" % ", ".join(sorted(VIGNOBLES_MONDE)))
            return 1
        print(texte)
        return 0
    texte = fiche_token(args[0])
    if texte is None:
        print("Jeton inconnu. Usage : sommaire | fiche TOKEN | pays NOM | croisement")
        return 1
    print(texte)
    return 0


if __name__ == "__main__":
    sys.exit(main())
