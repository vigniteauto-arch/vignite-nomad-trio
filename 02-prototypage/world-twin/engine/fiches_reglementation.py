#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""World Twin V1.9 — fiches pays réglementaires du brûlage, réédition v2.0 (31/10/2026).

Réédition sourcée des fiches réglementaires du brûlage des résidus agricoles
pour les sept juridictions P2 (fr-rhone, ch-leman, it-puglia, es-extremadura,
ar-cuyo, ar-misiones, ma-atlas). Elle remplace la v0.6 du 17/10/2026.

Chaque élément juridique a été revérifié le 31/10/2026 par croisement d'au
moins deux sources, dont la source officielle primaire chaque fois qu'elle
était accessible (Légifrance, Fedlex, Normattiva, Boletín Oficial del Estado,
Diario Oficial de Extremadura, Infoleg, Digesto de Misiones, Secrétariat
général du gouvernement marocain).

ÉTIQUETTES :
- DONNÉES RÉELLES : texte lu à la date indiquée sur la source primaire,
- À VÉRIFIER : élément non confirmé à la date de vérification.

DÉCOUVERTE CENTRALE DE LA V2.0 : la Ley 26.562 argentine reste en vigueur
mais se lit AVEC la Ley 26.815 de gestion du feu (modifiée par la Ley
27.591) — les deux lois ensemble. Le point À VÉRIFIER Misiones de la v0.6
est comblé par la Résolution 293/2020, celui du Maroc par le constat
d'absence de norme nationale dédiée (cadres généraux Loi 13-03 et Loi 28-00).

RÈGLES :
- Ces fiches décrivent le cadre réglementaire, pas une consultation
  juridique : valider par un conseil local avant tout engagement.
- La réglementation évolue : toute citation externe exige une
  re-vérification datée.
- Aucune valeur calibrée, tout résultat de simulation reste étiqueté
  SYNTHÉTIQUE. Doctrine PI : aucun paramètre du VDE n'est versionné.

Lancement :

    python3 engine/fiches_reglementation.py              # sommaire console
    python3 engine/fiches_reglementation.py ar-cuyo      # fiche d'une juridiction
    python3 engine/fiches_reglementation.py croisement   # gardes complètes

Les identifiants de hubs sont exactement ceux de engine/monde.py —
verifier_couverture() le contrôle au lancement, croisement() l'exige.
"""

import sys

ETIQUETTE_REEL = "DONNÉES RÉELLES"
ETIQUETTE_A_VERIFIER = "À VÉRIFIER"
DATE_VERIFICATION = "31/10/2026"
DATE_DETECTIONS = "17/10/2026"

STATUTS_BRULAGE = {
    "fr-rhone": "interdiction de principe, dérogation préfectorale exceptionnelle à objectif sanitaire",
    "ch-leman": "interdiction de principe, incinération admise uniquement en installation",
    "it-puglia": "encadré, tas limités à 3 m³ par hectare et par jour hors périodes de haut risque, chaumes soumis au régime du ringrano",
    "es-extremadura": "interdiction générale des résidus végétaux agricoles et forestiers, exceptions encadrées, verrou saisonnier",
    "ar-cuyo": "autorisation obligatoire à trois niveaux (fédéral, provincial, communal)",
    "ar-misiones": "interdiction générale en milieu rural, exceptions agricoles soumises à plan approuvé — régime le plus restrictif des sept",
    "ma-atlas": "aucune norme nationale dédiée identifiée, cadres généraux de la qualité de l'air et de la gestion des déchets",
}

TEXTES_PIVOTS = {
    "fr-rhone": "L.541-21-1",
    "ch-leman": "26a",
    "it-puglia": "6-bis",
    "es-extremadura": "27.3",
    "ar-cuyo": "26.815",
    "ar-misiones": "293/2020",
    "ma-atlas": "13-03",
}

FICHES_REGLEMENTATION = {
    "fr-rhone": {
        "juridiction": "France (département du Rhône)",
        "statut_brulage": STATUTS_BRULAGE["fr-rhone"],
        "cadre": [
            {"disposition": "Les biodéchets ne peuvent être éliminés par brûlage à l'air libre ni au moyen de matériels extérieurs (en vigueur depuis le 01/01/2021) — dérogation individuelle exceptionnelle du préfet aux seules fins d'éradication d'épiphytie ou d'élimination d'espèces végétales envahissantes — la mise à disposition d'équipements pour ce brûlage est interdite dans les mêmes conditions",
             "reference": "Code de l'environnement, article L.541-21-1 II (Légifrance, lu le 31/10/2026)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Base historique de l'interdiction, citée en doctrine",
             "reference": "Circulaire du 18/11/2011 (Légifrance)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Brûlage des chaumes et autres résidus de culture interdit sauf dérogation préfectorale à objectif sanitaire — réduction des aides de 3 % au premier constat puis 9 % en cas de récidive sur trois ans",
             "reference": "Condition de bonne condition agricole et environnementale numéro 3 (BCAE 3), fiche Telepac 2026 de la politique agricole commune (PAC), consultée le 31/10/2026",
             "etiquette": ETIQUETTE_REEL},
        ],
        "sanctions": "Contravention de 4e classe, 750 € au maximum, amende forfaitaire de 135 € (article R.541-78 du code de l'environnement). La loi 2023-973 du 23/10/2023 relative à l'industrie verte aurait doublé les sanctions du chapitre déchets (article L.541-46) — conservé de la v0.6, non re-vérifié sur Légifrance à la date de vérification.",
        "sanctions_etiquette": ETIQUETTE_A_VERIFIER,
        "procedure": "La dérogation est individuelle, exceptionnelle, délivrée par le préfet, limitée aux motifs sanitaires (épiphytie, espèces envahissantes). Aucune voie d'autorisation de routine n'existe pour les résidus de récolte.",
        "a_verifier": [
            "Loi 2023-973 industrie verte : re-vérifier le doublement des sanctions sur Légifrance avant toute citation externe.",
        ],
        "detections_firms": "Relevé du 17/10/2026 : 11 points chauds en Camargue voisine du hub — signal d'activité résiduelle réelle.",
        "angle_vignite": "Toute élimination par le feu est hors la loi en pratique courante : le gisement rhodanien est juridiquement verrouillé. La collecte et la valorisation sur site offrent la seule voie conforme, avec un argument de conformité immédiat auprès des coopératives et des négociants.",
        "sources": [
            "Légifrance (article L.541-21-1, lu le 31/10/2026)",
            "Portail national de l'information sur l'habitat (article R.541-78, consulté le 31/10/2026)",
            "Fiche Telepac 2026 des conditions de la politique agricole commune (PAC)",
        ],
    },
    "ch-leman": {
        "juridiction": "Suisse (canton de Vaud)",
        "statut_brulage": STATUTS_BRULAGE["ch-leman"],
        "cadre": [
            {"disposition": "L'incinération des déchets est admise uniquement dans des installations relevant du chiffre 7 de l'annexe 2, à l'exclusion des déchets visés au chiffre 11",
             "reference": "Ordonnance sur la protection de l'air (OPair), article 26a (recueil systématique RS 814.318.142.1, Fedlex, vérifié le 31/10/2026)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Encadrement de l'incinération en plein air",
             "reference": "Loi sur la protection de l'environnement (LPE), article 30c",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Dérogations communales étroites et motivées au cas par cas pour les rémanents forestiers (priorité à la valorisation matière)",
             "reference": "Instruction conjointe du Service des forêts, de la faune et de la nature (SFFN) et du Service de l'environnement et de l'énergie (SEVEN) du 20/11/2006, articles 30c LPE, 26a OPair et 15 du règlement d'application de la loi sur la gestion des déchets",
             "etiquette": ETIQUETTE_REEL},
        ],
        "sanctions": "Régime pénal de la loi sur la protection de l'environnement (LPE). Les modalités exactes d'amende pour le brûlage agricole en zone ouverte restent à vérifier auprès de l'autorité cantonale avant tout engagement.",
        "sanctions_etiquette": ETIQUETTE_A_VERIFIER,
        "procedure": "Aucune autorisation de brûlage de routine. La dérogation communale est l'exception motivée, avec priorité donnée à la valorisation matière.",
        "a_verifier": [
            "Modalités exactes d'amende du régime pénal de la LPE pour le brûlage agricole en zone ouverte (autorité cantonale).",
        ],
        "detections_firms": "Relevé du 17/10/2026 : aucun point chaud significatif au nord du Léman — cohérent avec le régime le plus contraignant des sept.",
        "angle_vignite": "L'ordonnance sur la protection de l'air (OPair) exige une installation : c'est précisément ce qu'est une unité Nomad. Le bassin lémanique est la juridiction où la conformité est la plus littéralement alignée sur le texte — le mode opératoire interdit est le feu ouvert, le mode proposé est un procédé en conteneur fermé.",
        "sources": [
            "Fedlex (ordonnance sur la protection de l'air, article 26a, consulté le 31/10/2026)",
            "JuriUp (mêmes références)",
            "Canton de Vaud (dérogations déchets verts, consulté le 31/10/2026)",
        ],
    },
    "it-puglia": {
        "juridiction": "Italie (région Pouilles)",
        "statut_brulage": STATUTS_BRULAGE["it-puglia"],
        "cadre": [
            {"disposition": "Ramassage et brûlage sur place des broussailles sèches, tontes et tailles autorisés en tas de 3 m³ maximum par hectare et par jour, en dehors des périodes de haut risque déclarées par la région, en vue du réusage comme fertilisant ou amendement",
             "reference": "Décret législatif 152/2006 (code de l'environnement italien), article 182, alinéa 6-bis, introduit en 2022 (Normattiva, consulté le 31/10/2026)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Exclusions du régime des déchets pour les matières dont l'usage agricole est démontré — voie ouverte à la valorisation sur place sans qualification de déchet",
             "reference": "Décret législatif 152/2006, article 185",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Brûlage des chaumes autorisé uniquement dans le cadre du ringrano (régénération des pailles) avec secondes récoltes sur surfaces irrigables, après communication préalable par formulaire certifié au maire et au Département régional de l'agriculture — sinon toujours interdit",
             "reference": "Loi régionale (LR) 38/2016 (Bulletin officiel de la région Poulies n° 143 du 14/12/2016) et délibération de la junte régionale (DGR) 1149 du 28/06/2018 (Bussola normativa, consulté le 31/10/2026)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Socle pénal national des incendies de forêt et d'interface",
             "reference": "Loi 353/2000",
             "etiquette": ETIQUETTE_REEL},
        ],
        "sanctions": "Régime de la loi 353/2000 en cas d'incendie, complété par les sanctions régionales de la loi régionale (LR) 38/2016. Montants exacts à vérifier selon la qualification (contravention administrative ou délit).",
        "sanctions_etiquette": ETIQUETTE_A_VERIFIER,
        "procedure": "Pour les tailles : tas de 3 m³ par hectare et par jour, hors alerte régionale de haut risque (informations météo quotidiennes du Centre fonctionnel décentralisé). Pour les chaumes : communication certifiée préalable au maire et au Département de l'agriculture, preuve du ringrano et de la seconde culture sur surface irrigable.",
        "a_verifier": [
            "Montants exacts des sanctions selon la qualification (contravention administrative ou délit).",
        ],
        "detections_firms": "Relevé du 17/10/2026 : 4 points chauds autour de Tarente et de Foggia — pratique résiduelle active, à traiter comme gisement adressable.",
        "angle_vignite": "Même le régime dit permissif exige une preuve de réusage agricole. Vignite inverse la logique : au lieu de prouver le brûlage utile, l'agriculteur vend la paille et gagne sans feu.",
        "sources": [
            "Normattiva (décret législatif 152/2006, article 182, alinéa 6-bis, consulté le 31/10/2026)",
            "Bulletin officiel de la région Poulies (loi régionale (LR) 38/2016, consulté le 31/10/2026)",
            "Bussola normativa (délibération de la junte régionale (DGR) 1149 du 28/06/2018, consulté le 31/10/2026)",
            "Centre fonctionnel décentralisé (informations météo quotidiennes de danger, relevées les 09/07/2026 et 10/08/2026)",
        ],
    },
    "es-extremadura": {
        "juridiction": "Espagne (Estrémadure)",
        "statut_brulage": STATUTS_BRULAGE["es-extremadura"],
        "cadre": [
            {"disposition": "En règle générale, la combustion de résidus végétaux issus du milieu agricole ou forestier n'est pas permise — exceptions liées à la directive (Union européenne) 2016/2284 (annexe III, partie 2, lettre C, considérant 22)",
             "reference": "Ley 7/2022 du 8 avril sur les déchets et les sols contaminés, article 27.3 (Boletín Oficial del Estado (BOE) du 09/04/2022, consulté le 31/10/2026)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Conditions de la notion de residuo vegetal de origen agrario",
             "reference": "Note interprétative du ministère de la Transition écologique (MITECO) du 26/01/2023",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Instructions d'application de l'article 27.3 sur le territoire régional",
             "reference": "Résolution du 30/12/2022 de la direction générale des situations d'urgence",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Époque de danger élevé du 01/06/2026 au 15/10/2026 avec régulation des usages du feu (plan de lutte contre les incendies de forêt d'Estrémadure, Infoex)",
             "reference": "Orden du 26/05/2026 (Diario Oficial de Extremadura (DOE) n° 100 du 27/05/2026)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Époque de danger faible en vigueur à la date de vérification, avec allègement encadré des usages du feu",
             "reference": "Orden du 09/10/2026 (Diario Oficial de Extremadura (DOE) du 15/10/2026)",
             "etiquette": ETIQUETTE_REEL},
        ],
        "sanctions": "Régime d'infractions de la Ley 7/2022 pour la partie déchets, et des órdenes saisonnières pour l'usage du feu en zone forestière, en particulier en époque de danger élevé. Montants à vérifier selon la qualification avant tout engagement.",
        "sanctions_etiquette": ETIQUETTE_A_VERIFIER,
        "procedure": "Aucune voie de brûlage agricole de routine : l'article 27.3 énonce une interdiction générale, les exceptions doivent être justifiées au regard de la directive (Union européenne) 2016/2284 et des instructions régionales de 2022.",
        "a_verifier": [
            "Montants des infractions selon la qualification (Ley 7/2022 et órdenes saisonnières Infoex).",
        ],
        "detections_firms": "Relevé du 17/10/2026 : 2 points chauds — pratique résiduelle malgré l'interdiction.",
        "angle_vignite": "L'Estrémadure combine une interdiction nationale de principe, une instruction régionale détaillée et un verrou saisonnier dur : c'est le cas d'école du marché adressable — de grandes surfaces de cultures permanentes et d'oliveraies dont les résidus ne peuvent plus être brûlés, sans filière de substitution structurée.",
        "sources": [
            "Boletín Oficial del Estado (BOE) (Ley 7/2022, consulté le 31/10/2026)",
            "Conseil de l'agriculture de la Junte d'Estrémadure (texte de l'article 27.3, consulté le 31/10/2026)",
            "Ministère de la Transition écologique (MITECO) (note du 26/01/2023, consultée le 31/10/2026)",
            "Diario Oficial de Extremadura (DOE) (órdenes des 26/05/2026 et 09/10/2026, consultés le 31/10/2026) et portail Infoex du gouvernement d'Estrémadure",
        ],
    },
    "ar-cuyo": {
        "juridiction": "Argentine (province de Mendoza)",
        "statut_brulage": STATUTS_BRULAGE["ar-cuyo"],
        "cadre": [
            {"disposition": "Définition de la quema (élimination de végétation ou de résidus par le feu en vue d'un usage productif du terrain, article 2), interdiction de toute quema sans autorisation de l'autorité locale (article 3), conditions et informations exigées (articles 4 à 6), normes provinciales complémentaires et sanctions supplétives — avertissement, amende pouvant atteindre 10 000 salaires de base de la catégorie initiale de l'administration publique nationale, suspension ou révocation (article 7), aucune exemption des normes forestières (article 8)",
             "reference": "Ley 26.562 (Boletín Oficial (BO) du 16/12/2009, Infoleg, consulté le 31/10/2026)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Système fédéral de gestion du feu, Service national de gestion du feu et Fonds national de gestion du feu en fiducie (contribution de 3 pour mille des primes d'assurance hors vie) — autorité d'application : ministère de la Sécurité de la Nation. La v0.6 citait la seule Ley 26.562 : la v2.0 corrige cette lacune, les deux lois se lisent ensemble",
             "reference": "Ley 26.815 de gestion du feu (Boletín Oficial (BO) du 16/01/2013, modifiée par la Ley 27.591 du 14/12/2020, Infoleg et Argentina.gob.ar, consultés le 31/10/2026) et Decreto 73/2026 (Boletín Oficial (BO) du 30/01/2026)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Interdit l'usage du feu en zones urbaines et rurales, sous réserve des autorisations du régime",
             "reference": "Ley 6.099 de Mendoza (Agrositio, consulté le 31/10/2026)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Procédure d'autorisation des brûlages prescrits de pâturages en zones de secano (travesías, peuplements d'Elionurus muticos, cortaderales)",
             "reference": "Résolution 1946/23 de la direction des ressources naturelles renouvelables (DRNR) du 20/09/2023 (Boletín Oficial (BO) de Mendoza du 02/10/2023, Ecofield, consulté le 31/10/2026)",
             "etiquette": ETIQUETTE_REEL},
        ],
        "sanctions": "Amendes saison 2026 du Plan provincial de gestion du feu pouvant atteindre 70 millions de pesos argentins (140 000 unités fiscales (UF) à 500 pesos argentins chacune, annonce du 14/01/2026, actualisant la valeur de 58 millions citée par la v0.6) — recouvrement par l'administration tributaire de Mendoza (ATM), surveillance satellitaire des anomalies thermiques et application Satellites on Fire.",
        "sanctions_etiquette": ETIQUETTE_REEL,
        "procedure": "Toute quema exige l'autorisation de l'autorité locale compétente, avec le dossier complet de l'article 4 de la Ley 26.562 (données du responsable et du titulaire, consentement, identification de la parcelle, objectif, techniques d'allumage et d'extinction, mesures de sécurité, date et heure), dans le respect du régime provincial de Mendoza. Les brûlages prescrits de pâturages suivent la procédure dédiée de la Résolution 1946/23.",
        "a_verifier": [
            "Périmètre exact des unités fiscales (UF) de Mendoza pour la conversion des amendes saison 2027.",
        ],
        "detections_firms": "Relevé du 17/10/2026 : aucune détection signalée sur la zone du hub au relevé du jour.",
        "angle_vignite": "Cuyo vit sous une triple contrainte (fédérale, provinciale, communale) avec une surveillance satellitaire active et des amendes 2026 en forte hausse. Le marché de proximité est double : les viticulteurs et producteurs qui ne peuvent plus brûler leurs sarments et résidus, et les gestionnaires de pâturages qui doivent aujourd'hui brûler à titre prescrit — la thermo-compression compacte et valorise sans feu. La Ley 26.562 exige des mesures d'extinction et de sécurité : l'unité Nomad supprime le besoin même du feu, donc l'essentiel du dossier d'autorisation.",
        "sources": [
            "Infoleg (Ley 26.562 et Ley 26.815, textes consultés le 31/10/2026)",
            "Boletín Oficial (BO) argentin (Ley 26.815, Decreto 73/2026)",
            "Portail Argentina.gob.ar (texte actualisé de la Ley 26.815) et Système argentin d'information juridique (SAIJ) (statut de vigueur)",
            "ArgentinaForestal (annonce du 14/01/2026 sur les amendes du plan provincial de gestion du feu de Mendoza), Agrositio (Ley 6.099), Ecofield (Résolution 1946/23)",
        ],
    },
    "ar-misiones": {
        "juridiction": "Argentine (province de Misiones)",
        "statut_brulage": STATUTS_BRULAGE["ar-misiones"],
        "cadre": [
            {"disposition": "Cadre fédéral : renvoi à la Ley 26.562 (présupposés minimaux du contrôle des brûlages) lue ensemble avec la Ley 26.815 de gestion du feu, modifiée par la Ley 27.591 du 14/12/2020",
             "reference": "Ley 26.562 et Ley 26.815 (Infoleg, consultés le 31/10/2026)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Plan provincial de gestion du feu, autorité d'application auprès du ministère de l'Écologie, Red de Alerta y Emergencia Provincial (RAEP, réseau d'alerte et d'urgence provincial) et fonds provincial de gestion du feu (FEPPCIFR)",
             "reference": "Ley XVI n° 65 (ancienne Ley 3.751 de l'an 2000, Digesto de Misiones et base FAOLEX de l'Organisation des Nations unies pour l'alimentation et l'agriculture (FAO), consultés le 31/10/2026)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Interdit toute quema en milieu rural sur l'ensemble du territoire de la province ainsi que tout usage du feu en milieu rural, à une exception près : la quema ouverte contrôlée de matériel végétal résiduel issu des récoltes, de la préparation du sol et du renouvellement des pâturages, aux conditions fixées par la résolution, avec renvoi exprès à l'article 140 de la Ley 26.815 — ce point comble le point À VÉRIFIER de la v0.6",
             "reference": "Résolution 293/2020 du 20/08/2020 du ministère de l'Écologie et des ressources naturelles renouvelables (texte officiel, consulté le 31/10/2026)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Le formulaire de demande et de plan de brûlage contrôlé exige une déclaration sur l'honneur de connaissance de la Ley 26.562, de la Ley 26.815, de la Ley XVI n° 65 et de la Résolution 293/2020, et rappelle que le plan soumis ne vaut pas autorisation tant qu'il n'est pas approuvé",
             "reference": "Solicitud - Plan de Quema Controlada, édition du ministère de l'Écologie de juillet 2026 (consultée le 31/10/2026)",
             "etiquette": ETIQUETTE_REEL},
        ],
        "sanctions": "Régime provincial du Plan provincial de gestion du feu, complété par les sanctions supplétives de l'article 7 de la Ley 26.562. Montants exacts à vérifier par voie locale.",
        "sanctions_etiquette": ETIQUETTE_A_VERIFIER,
        "procedure": "La procédure est une exception encadrée, non un droit : plan de brûlage contrôlé soumis, déclaration sur l'honneur des quatre textes, approbation préalable de l'autorité provinciale obligatoire.",
        "a_verifier": [
            "Montants exacts des sanctions du régime provincial (voie locale).",
        ],
        "detections_firms": "Relevé du 17/10/2026 : 1 point chaud — pratique résiduelle faible au regard du verrou législatif.",
        "angle_vignite": "Misiones applique le régime le plus restrictif des sept juridictions P2 et concentre la culture sur brûlis traditionnelle : la zone la plus sensible et le marché le plus net — l'interdiction existe, il ne manque que la filière de substitution. La sensibilité culturelle de la question du feu en zone rurale commande le même tact communicationnel qu'au Maroc.",
        "sources": [
            "Digesto de Misiones (Ley XVI n° 65, consulté le 31/10/2026)",
            "Ministère de l'Écologie de Misiones (formulaire de plan de brûlage contrôlé, édition de juillet 2026)",
            "Texte officiel de la Résolution 293/2020 et portail du Plan provincial de gestion du feu (consultés le 31/10/2026)",
            "Base FAOLEX de l'Organisation des Nations unies pour l'alimentation et l'agriculture (FAO) (statut de la Ley XVI n° 65)",
        ],
    },
    "ma-atlas": {
        "juridiction": "Maroc (région de l'Atlas)",
        "statut_brulage": STATUTS_BRULAGE["ma-atlas"],
        "cadre": [
            {"disposition": "Cadre général des émissions atmosphériques, le décret fixe les normes de qualité de l'air (modifié en 2024) — aucun de ces textes ne comporte de disposition dédiée au brûlage des résidus agricoles d'après les consultations du 31/10/2026",
             "reference": "Loi n° 13-03 relative à la lutte contre la pollution de l'air (dahir n° 1-03-61 du 12/05/2003, Bulletin officiel marocain n° 5118 du 19/06/2003) et décret n° 2-09-286 du 08/12/2009, modifié par le décret n° 2-23-244 du 07/03/2024 (ministère de la Transition énergétique et du Développement durable, JuriMaroc, consultés le 31/10/2026)",
             "etiquette": ETIQUETTE_REEL},
            {"disposition": "Titre III dédié aux déchets agricoles : dépôt dans les lieux d'élimination désignés par le plan directeur régional (article 24), réception contre redevance par le service communal (article 25), couverture des déchets agricoles par les plans directeurs régionaux (article 10) — la voie légale marocaine pour les résidus agricoles est le dépôt et la collecte organisés, non le brûlage, sans que celui-ci soit nommément interdit par un texte national identifié",
             "reference": "Loi n° 28-00 relative à la gestion des déchets (dahir n° 1-06-153 du 22/11/2006, Bulletin officiel marocain n° 5480 du 07/12/2006, texte consolidé vérifié le 31/10/2026, Secrétariat général du gouvernement marocain)",
             "etiquette": ETIQUETTE_REEL},
        ],
        "sanctions": "Sanctions des lois 13-03 et 28-00 pour les cadres généraux — montants et application au brûlage agricole à vérifier.",
        "sanctions_etiquette": ETIQUETTE_A_VERIFIER,
        "procedure": "Aucune procédure nationale d'autorisation de brûlage identifiée. La conformité s'apprécie au regard des lois 13-03 et 28-00 et du plan directeur régional des déchets.",
        "a_verifier": [
            "Absence de norme nationale dédiée au brûlage agricole : arrêtés du gouverneur, règlements régionaux et règles du Haut-Commissariat aux eaux et forêts non consultés — confirmer par un conseil local avant tout engagement opérationnel de la filiale Al-Atlas.",
        ],
        "detections_firms": "Relevé du 17/10/2026 : 2 points chauds sur la zone — pratique réelle de brûlis.",
        "angle_vignite": "Le vide relatif du droit marocain est un piège et une opportunité. Un piège, car l'absence d'interdiction explicite n'autorise rien : un brûlage de grande ampleur resterait exposé au regard de la Loi 13-03 et à un risque réputationnel fort pour un partenaire institutionnel. Une opportunité, car Vignite peut apporter la conformité par anticipation et se positionner en standard de la filière avant même que la norme n'existe — jamais couvrir un brûlage, toujours valoriser le procédé sans feu à l'air libre.",
        "sources": [
            "Ministère de la Transition énergétique et du Développement durable marocain (Loi 13-03, consultée le 31/10/2026)",
            "JuriMaroc (décret 2-09-286, consulté le 31/10/2026)",
            "Secrétariat général du gouvernement marocain (texte consolidé de la Loi 28-00 au 30/07/2025) et Bulletin officiel marocain",
            "Base de l'Unité d'évaluation environnementale du Programme des Nations unies pour l'environnement (UNEP) (cadre marocain des déchets, consultée le 31/10/2026)",
        ],
    },
}


def hubs_connus():
    return list(FICHES_REGLEMENTATION)


def statut_brulage(hub_id):
    if hub_id not in FICHES_REGLEMENTATION:
        return "Hub inconnu : %s. Hubs : %s" % (hub_id, ", ".join(FICHES_REGLEMENTATION))
    return STATUTS_BRULAGE[hub_id]


def verifier_couverture():
    """Contrôle que les fiches couvrent exactement les hubs de monde.py.

    Retourne None si le contrôle passe, sinon un message d'écart.
    Tolérant : si monde.py n'est pas importable, contrôle sauté.
    """
    try:
        import monde
    except ImportError:
        return None
    fiches = set(FICHES_REGLEMENTATION)
    moteur = set(monde.HUBS_MONDE)
    if fiches != moteur:
        manquants = sorted(moteur - fiches)
        en_trop = sorted(fiches - moteur)
        return "écart fiches/moteur — manquants: %s, en trop: %s" % (
            ", ".join(manquants) or "aucun", ", ".join(en_trop) or "aucun")
    return None


def fiche_hub(hub_id):
    if hub_id not in FICHES_REGLEMENTATION:
        return None
    f = FICHES_REGLEMENTATION[hub_id]
    lignes = []
    lignes.append("== %s — %s" % (hub_id, f["juridiction"]))
    lignes.append("Statut du brûlage des résidus agricoles : %s" % f["statut_brulage"])
    lignes.append("")
    lignes.append("Cadre (%s, chaque élément croisé d'au moins deux sources) :" % DATE_VERIFICATION)
    for c in f["cadre"]:
        lignes.append("  [%s] %s" % (c["etiquette"], c["disposition"]))
        lignes.append("        référence : %s" % c["reference"])
    lignes.append("")
    lignes.append("Sanctions [%s] : %s" % (f["sanctions_etiquette"], f["sanctions"]))
    lignes.append("Procédure : %s" % f["procedure"])
    if f["a_verifier"]:
        lignes.append("Points À VÉRIFIER :")
        for point in f["a_verifier"]:
            lignes.append("  - %s" % point)
    lignes.append("Détections Firms (Fire Information for Resource Management System) : %s" % f["detections_firms"])
    lignes.append("Angle Vignite : %s" % f["angle_vignite"])
    lignes.append("Sources croisées :")
    for source in f["sources"]:
        lignes.append("  - %s" % source)
    lignes.append("")
    lignes.append("Registre de travail, pas une consultation juridique : valider par un conseil local avant tout engagement.")
    return "\n".join(lignes)


def sommaire():
    lignes = ["Fiches pays réglementaires — brûlage des résidus agricoles (v2.0, 31/10/2026)",
              "Réédition sourcée de la v0.6 : chaque élément revérifié le 31/10/2026 par croisement d'au moins deux sources.",
              "Registre de travail, pas une consultation juridique — à re-vérifier avant tout usage externe.",
              ""]
    lignes.append("%-16s %-32s %s" % ("Hub", "Juridiction", "Statut du brûlage"))
    for hub_id in FICHES_REGLEMENTATION:
        f = FICHES_REGLEMENTATION[hub_id]
        lignes.append("%-16s %-32s %s" % (hub_id, f["juridiction"], f["statut_brulage"]))
    lignes.append("")
    lignes.append("Juridictions couvertes : %d — sommaire, fiche HUB, croisement." % len(FICHES_REGLEMENTATION))
    return "\n".join(lignes) + "\n"


def croisement():
    """Gardes complètes de la réédition v2.0. Retourne (texte, code)."""
    problemes = []
    lignes = ["Croisement fiches v2.0 — contrôles complets", ""]

    # garde 1 — couverture exacte des hubs de monde.py
    try:
        import monde
    except ImportError:
        problemes.append("monde.py introuvable : le croisement exige les hubs du moteur.")
        moteur = set()
    else:
        moteur = set(monde.HUBS_MONDE)
    fiches = set(FICHES_REGLEMENTATION)
    if moteur and fiches != moteur:
        manquants = sorted(moteur - fiches)
        en_trop = sorted(fiches - moteur)
        problemes.append("couverture moteur : manquants %s, en trop %s" % (
            ", ".join(manquants) or "aucun", ", ".join(en_trop) or "aucun"))
    lignes.append("Juridictions couvertes : %d" % len(FICHES_REGLEMENTATION))
    lignes.append("Couverture exacte des hubs de monde.py : %s" % ("OK" if not (moteur and fiches != moteur) else "ECART"))

    # garde 2 — structure obligatoire de chaque fiche
    manques_structure = []
    for hub_id, f in FICHES_REGLEMENTATION.items():
        if not f.get("juridiction"):
            manques_structure.append("%s (juridiction)" % hub_id)
        if len(f.get("cadre", [])) < 2:
            manques_structure.append("%s (cadre)" % hub_id)
        if not f.get("sanctions"):
            manques_structure.append("%s (sanctions)" % hub_id)
        if not f.get("procedure"):
            manques_structure.append("%s (procedure)" % hub_id)
        if len(f.get("sources", [])) < 2:
            manques_structure.append("%s (sources)" % hub_id)
        if not f.get("detections_firms"):
            manques_structure.append("%s (detections)" % hub_id)
        if not f.get("angle_vignite"):
            manques_structure.append("%s (angle)" % hub_id)
    if manques_structure:
        problemes.append("structure incomplète : %s" % ", ".join(manques_structure))
    lignes.append("Structure par fiche (juridiction, cadre, sanctions, procédure, sources, détections, angle) : %s"
                  % ("OK" if not manques_structure else "ECART"))

    # garde 3 — étiquettes licites et texte pivot présent
    etiquettes_licites = {ETIQUETTE_REEL, ETIQUETTE_A_VERIFIER}
    total_reel = 0
    total_verifier = 0
    pivots_manquants = []
    for hub_id, f in FICHES_REGLEMENTATION.items():
        references = " ".join(c["reference"] for c in f["cadre"])
        for c in f["cadre"]:
            if c["etiquette"] not in etiquettes_licites:
                problemes.append("étiquette illicite dans le cadre de %s : %s" % (hub_id, c["etiquette"]))
            if c["etiquette"] == ETIQUETTE_REEL:
                total_reel += 1
            else:
                total_verifier += 1
        if f["sanctions_etiquette"] not in etiquettes_licites:
            problemes.append("étiquette illicite pour les sanctions de %s" % hub_id)
        if f["sanctions_etiquette"] == ETIQUETTE_REEL:
            total_reel += 1
        else:
            total_verifier += 1
        if TEXTES_PIVOTS[hub_id] not in references:
            pivots_manquants.append("%s (pivot %s)" % (hub_id, TEXTES_PIVOTS[hub_id]))
    if pivots_manquants:
        problemes.append("texte pivot absent des références : %s" % ", ".join(pivots_manquants))
    lignes.append("Éléments de cadre étiquetés : %d — %d %s, %d %s"
                  % (total_reel + total_verifier, total_reel, ETIQUETTE_REEL, total_verifier, ETIQUETTE_A_VERIFIER))
    lignes.append("Textes pivots présents (L.541-21-1, OPair 26a, 6-bis, Ley 27.3, Ley 26.815, Résolution 293/2020, Loi 13-03) : %s"
                  % ("OK" if not pivots_manquants else "ECART"))

    # garde 4 — correctifs centraux de la v2.0 par rapport à la v0.6
    correctifs = []
    references_cuyo = " ".join(c["reference"] for c in FICHES_REGLEMENTATION["ar-cuyo"]["cadre"])
    references_misiones = " ".join(c["reference"] for c in FICHES_REGLEMENTATION["ar-misiones"]["cadre"])
    if "26.815" in references_cuyo:
        correctifs.append("Ley 26.815 lue avec la Ley 26.562 (ar-cuyo)")
    else:
        problemes.append("correctif central absent : la Ley 26.815 doit figurer dans les références de ar-cuyo")
    if "293/2020" in references_misiones:
        correctifs.append("Résolution 293/2020 de Misiones (point À VÉRIFIER de la v0.6 comblé)")
    else:
        problemes.append("correctif absent : la Résolution 293/2020 doit figurer dans les références de ar-misiones")
    sanctions_cuyo = FICHES_REGLEMENTATION["ar-cuyo"]["sanctions"]
    if "70 millions" in sanctions_cuyo:
        correctifs.append("amendes Mendoza 2026 actualisées à 70 millions de pesos argentins")
    else:
        problemes.append("amendes Mendoza 2026 non actualisées dans les sanctions de ar-cuyo")
    lignes.append("Correctifs v2.0 par rapport à la v0.6 :")
    for c in correctifs:
        lignes.append("  - %s" % c)

    lignes.append("")
    if problemes:
        lignes.append("PROBLÈMES DÉTECTÉS (%d) :" % len(problemes))
        lignes.extend("  - %s" % p for p in problemes)
        lignes.append("")
        lignes.append("CROISEMENT : ECHEC")
        return "\n".join(lignes), 1
    lignes.append("CROISEMENT : OK — toutes les gardes passent.")
    return "\n".join(lignes), 0


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    ecart = verifier_couverture()
    if ecart:
        print("ATTENTION : %s" % ecart)
    if not args:
        print(sommaire())
        return 0
    if args[0] == "croisement":
        texte, code = croisement()
        print(texte)
        return code
    texte = fiche_hub(args[0])
    if texte is None:
        print("Hub inconnu. Usage : sommaire | fiche HUB | croisement — hubs : %s"
              % ", ".join(FICHES_REGLEMENTATION))
        return 1
    print(texte)
    return 0


if __name__ == "__main__":
    sys.exit(main())
