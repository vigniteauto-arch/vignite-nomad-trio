#!/usr/bin/env python3
"""Couche V2.9 « adossement aux négociants dominants » des filières.

Pour chaque hub, la couche identifie le négociant dominant de chaque
famille de co-produits présente (entrée pays SOURCÉ quand la littérature
ou les classements publics documentent un dominant, repli MONDIAL sur
le négociant international de la filière, ILLUSTRATION pour les
gisements diffus sans acteur unique), puis recommande l'adossement :

- PILOTE : projet pilote avec l'écosystème de collecte (gisement
  diffus) ;
- LOI_USINE : LOI/contrat d'offtake à l'usine, sur les co-produits du
  site du dominant (gisement concentré au site) ;
- FRANCHISE : franchise/licensing au dominant local (pays hors
  périmètre direct de Vignite, doctrine international : le partenaire
  finance le matériel, Vignite perçoit des royalties).

Doctrine PI : cette couche ne contient QUE des faits publics (qui
domine quelle filière, où) et des recommandations génériques de mode.
Aucun contact nominatif, aucun état de négociation, aucun coût, aucune
valeur calibrée. Télémétrie du registre DÉVELOPPEMENT.

Sources croisées (publiques, vérifiées le 14/11/2026) : classements
publics des négociants (AGRI.markets, Report Prime, Financely), sites
officiels des groupes (Raízen, Mitr Phol, CP Intertrade, Loc Troi,
Balrampur Chini, Dcoop, Sovena, McLeod Russel, Becle/José Cuervo,
Franklin Baker, FGV, West Fraser), presse filière (Vitisphere pour
la fusion UDM-Grap'Sud, IFC pour Carbonwave), structures filières
(UNICA, MPOB, PalmWatch, FNC/Cenicafé, California Walnut Board,
Cocobod, Çaykur, Forbes & Walker), précédents internes documentés
(colombie-cafe-analyse-deploiement, cacao-equateur-colombie-perou,
riz-monde-strategie-volume, 2026-11-09-plan-loi-priorite-n1).
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sites_transformation

JETONS_INTERDITS = ("cout", "prix", "plan_achat", "eur_t", "eur_an",
                    "marche_externe", "deficit", "€")

# ------------------------------------------------------------------ tables

# Angle d'adossement par famille : PILOTE pour les gisements diffus,
# LOI_USINE pour les gisements concentrés au site d'un dominant.
ANGLE_FILIERE = {
    "AU_CHAMP": "PILOTE",
    "SARGASSES": "PILOTE",
    "NOYAUX_FRUITS": "PILOTE",
}

# Pays du périmètre direct (pilotes P2 + filiales) : adossement direct,
# ailleurs la doctrine international impose la franchise/licensing.
PAYS_DIRECTS = {
    "France": "hub pilote fr-rhone (Carré d'Or)",
    "Suisse": "hub pilote ch-leman (Carré d'Or)",
    "Italie": "hub pilote it-puglia (Vignite Italia)",
    "Espagne": "hub pilote es-extremadura (Carré d'Or)",
    "Argentine": "hubs pilotes ar-cuyo, ar-misiones (Vignite LatAm)",
    "Maroc": "hub pilote ma-atlas (Vignite Al-Atlas)",
}

# Négociant dominant par famille : (monde, pays).
# Chaque entrée pays : (acteur, statut, note, source).
NEGOCIANTS = {
    "PALMIER": {
        "monde": ("Wilmar, Musim Mas, GAR (Golden Agri-Resources), "
                  "Sime Darby, Cargill",
                  "négociants-meuniers internationaux du palmier à huile "
                  "(parcs MPOB 449 moulins Malaisie, PalmWatch 1 471 "
                  "Indonésie)", "classements publics (AGRI.markets, "
                  "Locality Partners)"),
        "pays": {
            "Malaisie": ("Sime Darby + FGV (Felda Global Ventures), "
                         "meuniers agréés MPOB", "SOURCÉ",
                         "premiers producteurs-meuniers du pays",
                         "FGV Holdings, classements publics"),
            "Indonésie": ("GAR (Sinar Mas) + Musim Mas + Wilmar, "
                          "meuniers PalmWatch", "SOURCÉ",
                          "premiers groupes intégrés du pays",
                          "CNBC Indonesia (10 producteurs 2025), "
                          "PalmWatch"),
            "Nigeria": ("Okomu + Presco, plus grands producteurs-meuniers "
                        "domestiques", "SOURCÉ",
                        "premiers planteurs-meuniers du Nigeria",
                        "rapports annuels Okomu, Presco"),
            "Côte d'Ivoire": ("PalmCI (groupe SIFCA), premier "
                              "meunier ivoirien", "SOURCÉ",
                              "premier groupe oléicole du pays",
                              "SIFCA, rapports publics"),
        },
    },
    "RIZ": {
        "monde": ("Olam Agri, Wilmar, LDC (Louis Dreyfus Company), COFCO",
                  "négociants internationaux du riz, rizeries "
                  "industrielles locales", "classements publics des "
                  "négociants de riz (Report Prime, AGRI.markets)"),
        "pays": {
            "Thaïlande": ("CP Intertrade (groupe CP), premier exportateur "
                          "thaï", "SOURCÉ",
                          "premier exportateur de riz du pays",
                          "CP Thairice, PM Award"),
            "Viêt Nam": ("Loc Troi, premier producteur-négociant rizicole",
                         "SOURCÉ", "leader rizicole du Viêt Nam",
                         "Ministère du commerce (GoGlobal VN)"),
            "Nigeria": ("Olam Agri, premier investisseur de la filière "
                        "riz locale", "SOURCÉ",
                        "dominant de l'intégration riz Nigeria",
                        "doctrine interne riz monde, rapports Olam"),
        },
    },
    "CANNE": {
        "monde": ("sucreries du pays (pas de négociant mondial de la "
                  "bagasse : co-produit capté à l'usine)",
                  "meuniers sucriers locaux, parcs UNICA et équivalents",
                  "doctrine sites V2.5 : le co-produit est au site"),
        "pays": {
            "Brésil": ("Raízen (alliance Cosan-Shell), Tereos, "
                       "São Martinho", "SOURCÉ",
                       "premiers transformeurs de canne du Brésil "
                       "(parc UNICA 389 unités)", "Raízen, UNICA, "
                       "presse filière"),
            "Thaïlande": ("Mitr Phol, premier sucrier du pays", "SOURCÉ",
                          "premier groupe sucrier familial thaï",
                          "Mitr Phol Group"),
            "Inde": ("Balrampur Chini, premier sucrier coté", "SOURCÉ",
                     "premier groupe privé indien", "BCML"),
            "Mexique": ("ingénios du groupe Tres Valles et équivalents",
                        "SOURCÉ", "grands moulins de la canne mexicaine",
                        "presse filière mexicaine"),
            "Cuba": ("Azcuba (étatique), tous les centrales", "SOURCÉ",
                     "monopole d'État de la filière", "Azcuba"),
        },
    },
    "MAIS": {
        "monde": ("ABCD (ADM, Bunge, Cargill, LDC) + COFCO",
                  "négociants en céréales, silos et collecte",
                  "classements publics des négociants de céréales "
                  "(AGRI.markets, Financely)"),
        "pays": {
            "Ukraine": ("NIBULON + exportateurs céréaliers, silos "
                        "portuaires", "SOURCÉ",
                        "premier exportateur céréalier du pays", "NIBULON"),
            "France": ("coopératives céréalières (Axéréal, Terrena) et "
                       "collecteurs agréés", "SOURCÉ",
                       "la collecte française est coopérative",
                       "FranceAgriMer, coopératives"),
            "Nigeria": ("Flour Mills of Nigeria, premier intégrateur "
                        "céréalier", "SOURCÉ",
                        "premier meunier du pays", "FMN"),
        },
    },
    "AU_CHAMP": {
        "monde": ("AUCUN négociant dominant par nature (gisement diffus) : "
                  "coopératives, organismes de collecte, agrégateurs",
                  "écosystème de collecte des résidus de culture",
                  "méta-analyse des taux de retrait (Resources, "
                  "Conservation and Recycling 2025) : 45 % riz, 19 % blé, "
                  "42 % maïs ; collecte à organiser, jamais un seul acteur"),
        "pays": {
            "France": ("coopératives et CUMA, organisme de collecte "
                       "paille-menue-paille", "ILLUSTRATION",
                       "collecte coopérative, pas d'acteur unique",
                       "Coop de France"),
            "Inde": ("dépôts de biomasse du dispositif CRM (544 crore de "
                     "roupies) et FPO", "SOURCÉ",
                     "chaîne d'appro ex-situ paille de riz, subventionnée",
                     "CEEW, PIB gouvernement indien"),
            "Chine": ("entreprises de collecte de paille, usines de "
                      "biomasse", "ILLUSTRATION",
                      "collecte centralisée en croissance, paysage "
                      "fragmenté", "presse chinoise biomasse"),
        },
    },
    "SARMENTS": {
        "monde": ("distilleries vinicoles et prestataires de taille au "
                  "rang", "écosystème distilleries-tailleur",
                  "post-récolte V2.5 : France 93-99 % des marcs en "
                  "distillerie"),
        "pays": {
            "France": ("Grap'Sud + UDM (fusion : premier groupe mondial "
                       "de distilleries vinicoles), BIVB pour la taille",
                       "SOURCÉ", "leader de la collecte des marcs et "
                       "sarments", "Vitisphere (fusion UDM-Grap'Sud), BIVB"),
        },
    },
    "VIGNE_MARC": {
        "monde": ("distilleries vinicoles et coopératives viticoles",
                  "écosystème distilleries (FranceAgriMer : 93-99 % des "
                  "marcs partent en distillerie)", "FranceAgriMer"),
        "pays": {
            "France": ("Grap'Sud + UDM, premier groupe mondial de "
                       "distilleries vinicoles", "SOURCÉ",
                       "dominant de la distillation des marcs",
                       "Vitisphere (fusion), FranceAgriMer"),
            "Espagne": ("coopératives et distilleries régionales",
                        "ILLUSTRATION", "paysage coopératif fragmenté",
                        "presse filière espagnole"),
            "Italie": ("grappole/distillerie de borlande régionales",
                       "ILLUSTRATION", "paysage fragmenté",
                       "presse filière italienne"),
        },
    },
    "FORET_SCIERIE": {
        "monde": ("groupes de scieries régionaux (filière fragmentée)",
                  "sciage : résidus 46 % de la grume à la scierie "
                  "(FAO appendice VI)", "FAO T0269E"),
        "pays": {
            "Canada": ("West Fraser, premier producteur de bois d'œuvre "
                       "d'Amérique du Nord", "SOURCÉ",
                       "premier groupe de scieries du pays", "West Fraser"),
            "Suède": ("Södra + Metsä, groupes coopératifs et privés du "
                      "sciage nordique", "SOURCÉ",
                      "grands scieurs nordiques", "Södra, Metsä"),
            "France": ("scieries du Jura et des massifs, coopératives "
                       "forestières", "ILLUSTRATION",
                       "filière française fragmentée mais organisée",
                       "CNPF, presse filière"),
        },
    },
    "MANIOC": {
        "monde": ("usines d'amidon, farineries et garrieries locales",
                  "transformateurs du manioc (garri ≈ 70 % du manioc "
                  "nigérian transformé hors exploitation, ILRI 2022)",
                  "ILRI Turning Waste to Wealth (Springer 2022)"),
        "pays": {
            "Nigeria": ("PCPL (Premium Cassava Products), Matna Foods, "
                        "Psaltry, FMN Agro", "SOURCÉ",
                        "premiers transformateurs industriels du manioc "
                        "nigérian", "sites officiels PCPL, Matna, FMN"),
            "Thaïlande": ("groupes d'amidon de tapioca (premier "
                          "exportateur mondial)", "SOURCÉ",
                          "premier complexe mondial de l'amidon de "
                          "manioc", "Thai Tapioca Trade Association"),
            "Brésil": ("farinheiras et fecularias de la ceinture "
                       "cassavicole", "ILLUSTRATION",
                       "paysage fragmenté des casas de farinha",
                       "presse filière brésilienne"),
        },
    },
    "CAFE": {
        "monde": ("ECOM, Volcafé (Neumann Kaffee Gruppe), LDC, "
                  "Olam Agri, Suárez, Mercon",
                  "négociants internationaux du café", "classements "
                  "publics des négociants (Financely, Daily Coffee "
                  "News 2026)"),
        "pays": {
            "Colombie": ("FNC (Federación Nacional de Cafeteros) + "
                         "Cenicafé + Buencafé", "SOURCÉ",
                         "la FNC fédère la filière ; doctrine interne "
                         "déployée (LOI Cenicafé prête, trios en sortie "
                         "de ligne Ecomill/coopératives, Buencafé "
                         "Chinchiná flagship)", "FNC/Cenicafé, doctrine "
                         "interne colombie-cafe-analyse-deploiement"),
            "Mexique": ("ECOM et exportateurs du Chiapas (bénéficios "
                        "humides et secs)", "SOURCÉ",
                        "premier négociant présent au Mexique",
                        "ECOM, presse filière"),
            "Éthiopie": ("ECX (bourse d'Éthiopie) + unions de "
                         "coopératives (Oromia, Sidama)", "SOURCÉ",
                         "canaux officiels de commercialisation",
                         "ECX, unions"),
        },
    },
    "CAFE_PULPE": {
        "monde": ("stations de lavage (bénéficios humides)",
                  "pulpe 44,6 % de la cerise au moulin humide (Rotta, "
                  "UC Davis 2020) ; 29 % du café éthiopien lavé en "
                  "station (CABI 2020)", "Rotta UC Davis 2020, CABI 2020"),
        "pays": {
            "Mexique": ("ECOM et bénéficios humides du Chiapas (hub "
                        "porteur gen-mexique-1)", "SOURCÉ",
                        "la voie humide se concentre dans les "
                        "bénéficios exportateurs", "ECOM, tentative "
                        "V2.8 : part À SOURCER"),
            "Colombie": ("centrales de transformation FNC/Cenicafé "
                         "(doctrine interne : trios en sortie de "
                         "centrale)", "SOURCÉ",
                         "les centrales fédèrent le lavage",
                         "FNC/Cenicafé"),
        },
    },
    "CACAO": {
        "monde": ("Barry Callebaut, Cargill, OFI (Olam Food "
                  "Ingredients), Touton",
                  "meuniers du cacao (les trois premiers transforment "
                  "la majorité mondiale)", "classements publics des "
                  "broyeurs"),
        "pays": {
            "Côte d'Ivoire": ("acheteurs agréés + usines Cargill, Barry "
                              "Callebaut (Yopougon)", "SOURCÉ",
                              "première origine mondiale, meuniers "
                              "installés", "CCC (Conseil Café-Cacao), "
                              "rapports publics"),
            "Ghana": ("LBC (Licensed Buying Companies) sous Cocobod "
                      "+ Cargill, Barry Callebaut", "SOURCÉ",
                      "filière étatique (Cocobod)", "Cocobod"),
            "Colombie": ("Luker Cacao (Nutresa) + Fedecacao", "SOURCÉ",
                         "Luker capte la majorité des coques de fève "
                         "(CBS) ; doctrine interne triptyque café-cacao Colombie",
                         "Fedecacao, Luker, analyse interne cacao"),
            "Nigeria": ("exportateurs agréés (plusieurs centaines), "
                        "oléine évasive", "ILLUSTRATION",
                        "filière privée fragmentée", "presse filière"),
        },
    },
    "OLIVE": {
        "monde": ("coopératives et mouliniers oléicoles",
                  "alperujo 80-85 % du fruit au moulin à deux phases "
                  "(MDPI), filière coopérative", "MDPI (alperujo)"),
        "pays": {
            "Portugal": ("Sovena, premier embouteilleur mondial d'huile "
                         "d'olive", "SOURCÉ",
                         "leader portugais intégré", "Sovena"),
            "Tunisie": ("stations d'extraction de Sfax et conditionneurs "
                        "(CHO et équivalents)", "SOURCÉ",
                        "le broyage se concentre dans les huileries de "
                        "Sfax", "presse filière tunisienne"),
            "Maroc": ("coopératives oléicoles (crushers régionaux) + "
                      "intégrateurs nationaux", "ILLUSTRATION",
                      "filière en structuration (Vignite Al-Atlas)",
                      "ONIGA, coopératives"),
            "Espagne": ("Dcoop, première coopérative oléicole mondiale",
                        "SOURCÉ", "leader andalou", "Dcoop"),
        },
    },
    "AGRUMES": {
        "monde": ("Cutrale + Citrosuco (Brésil), usines de jus concentré "
                  "locales", "un verre de jus d'orange sur trois dans le "
                  "monde vient de Cutrale", "presse brésilienne "
                  "(FoodBiz, Click)"),
        "pays": {
            "Brésil": ("Cutrale + Citrosuco, duo dominant du concentré",
                       "SOURCÉ", "le duo capte la majorité des exportations "
                       "brésiliennes de jus", "FoodBiz, presse"),
            "Espagne": ("coopératives agrumicoles (Anecoop, et "
                        "équivalents)", "ILLUSTRATION",
                        "filière coopérative du jus espagnol", "Anecoop"),
            "Israël": ("canaux d'exportation Jaffa (Pri-Or, coopératifs)",
                       "ILLUSTRATION", "brand Jaffa fédéré",
                       "presse filière israélienne"),
        },
    },
    "PECHE_COQUILLES": {
        "monde": ("conserveries et criées",
                  "coquilles 56 % des déchets de conserverie, ≈ 27 % de "
                  "la tonne vivante aux plants industriels (Waste "
                  "Management & Research 2022)", "WMR 2022, Iribarren "
                  "2010"),
        "pays": {
            "France": ("conserveries et organisations de producteurs "
                       "conchylicoles (moules de bouchot)", "SOURCÉ",
                       "filière conchylicole française organisée",
                       "CNPMEM (comité national conchyliculture)"),
        },
    },
    "POMME": {
        "monde": ("pressoirs cidricoles et usines de jus",
                  "marc de pomme 25-30 % du fruit au pressoir "
                  "(MDPI Antioxidants 2026)", "MDPI Antioxidants "
                  "15(4):429 2026"),
        "pays": {
            "France": ("coopératives cidricoles normandes et bretonnes",
                       "ILLUSTRATION", "filière cidricole coopérative",
                       "IFPC (institut français des productions "
                       "cidricoles)"),
            "Suisse": ("pressoirs et coopératives fruitières suisses",
                       "ILLUSTRATION", "filière fruitière suisse "
                       "coopérative", "presse cantonale"),
        },
    },
    "THE": {
        "monde": ("usines/manufactures de thé (feuilles, tiges, poussière "
                  "concentrées en station)", "résidus de manufacture "
                  "concentrés (revues Springer 2025)", "Springer 2025, "
                  "JECE 2025"),
        "pays": {
            "Turquie": ("Çaykur, monopole d'État du thé turc", "SOURCÉ",
                        "dominant de la manufacture du pays",
                        "Çaykur"),
            "Sri Lanka": ("brokers de Colombo (Forbes & Walker, et "
                          "équivalents) + estates", "SOURCÉ",
                          "les brokers fédèrent les ventes aux enchères",
                          "Ceylon Chamber, Forbes & Walker"),
        },
    },
    "COCO": {
        "monde": ("décortiqueurs et usines de coprah/desiccated",
                  "bourre 0,35 × noix (FAO Y3612E)", "FAO Y3612E"),
        "pays": {
            "Philippines": ("Franklin Baker, Peter Paul, Centennial "
                            "(desiccated)", "SOURCÉ",
                            "majors historiques du desiccated coconut",
                            "Franklin Baker (site officiel), FoodChain "
                            "Magazine"),
            "Malaisie": ("transformateurs locaux (KLK Oleo, et "
                         "équivalents)", "ILLUSTRATION",
                         "filière oléagineuse intégrée", "KLK, presse"),
        },
    },
    "DATTIER": {
        "monde": ("stations de conditionnement des palmeraies",
                  "rejets de triage et noyaux 10-15 % de la production "
                  "à la station (MDPI Applied Sciences 2023) ; "
                  "conditionnement tunisien centralisé 59 kt",
                  "MDPI Applied Sciences 13(22):12315 2023"),
        "pays": {
            "Arabie Saoudite": ("négociants des marchés centraux de "
                                "dattes et conditionneurs nationaux",
                                "ILLUSTRATION",
                                "marchés centraux (pas d'acteur unique "
                                "documenté)", "presse filière"),
            "Irak": ("exportateurs de Barhi (Basra)", "ILLUSTRATION",
                     "filière en reconstruction", "presse filière"),
            "Iran": ("exportateurs de Mazafati (Kerman)", "ILLUSTRATION",
                     "filière exportatrice fragmentée", "presse filière"),
            "Tunisie": ("conditionneurs de Deglet Nour (Nouri & Cie, "
                        "Nouran, et équivalents)", "SOURCÉ",
                        "le conditionnement est centralisé et "
                        "exportateur", "Nouri & Cie, Nouran (sites "
                        "officiels)"),
        },
    },
    "BIERE": {
        "monde": ("AB InBev (n°1 mondial), Heineken, Castel, Asahi",
                  "drêches ≈ 85 % des résidus solides de brasserie "
                  "(MDPI Sustainability 2026)", "MDPI Sustainability "
                  "18(5):2464 2026"),
        "pays": {
            "France": ("Kronenbourg (groupe Carlsberg), Heineken, "
                       "Castel", "SOURCÉ",
                       "premier brasseur du marché français",
                       "Kronenbourg, BIWA (brasseurs)"),
        },
    },
    "AGAVE": {
        "monde": ("Becle (José Cuervo, n°1 mondial de tequila), "
                  "Herradura/Patrón (Brown-Forman, Suntory)",
                  "bagasse ≈ 40 % du poids humide à la distillerie "
                  "(MDPI Fermentation 2026)", "MDPI Fermentation "
                  "12(2):79 2026, Cuervo (présentations investisseurs)"),
        "pays": {
            "Mexique": ("Becle (José Cuervo), Herradura (Casa "
                        "Herradura), Patrón", "SOURCÉ",
                        "premier groupe tequilier mondial",
                        "Becle IR, classements publics"),
        },
    },
    "SARGASSES": {
        "monde": ("Marine mexicaine (SEMAR : barrages et collecte, "
                  "156 063 t Quintana Roo saison 2026), hôtellerie de "
                  "la Riviera Maya, start-ups de transformation "
                  "(Carbonwave, financé par l'IFC)",
                  "gisement aléatoire, aucune part chiffrée du gisement "
                  "échoué : gisement à organiser avec la puissance "
                  "publique", "SEMAR (collecte officielle), IFC "
                  "(Carbonwave)"),
        "pays": {
            "Mexique": ("SEMAR + hôtellerie Riviera Maya + Carbonwave",
                        "SOURCÉ",
                        "l'État conduit la collecte, les hôtels financent, "
                        "les start-ups transforment", "SEMAR, IFC"),
        },
    },
    "NOYAUX_FRUITS": {
        "monde": ("stations de conditionnement et coopératives fruitières",
                  "composition chiffrée mais part centralisée À SOURCER "
                  "(tentative V2.8 infructueuse)", "revues de "
                  "valorisation (tentative V2.8)"),
        "pays": {
            "France": ("coopératives fruitières (elles-mêmes adossées "
                       "aux stations de conditionnement)", "ILLUSTRATION",
                       "collecte coopérative", "presse filière"),
        },
    },
    "NOIX_COQUES": {
        "monde": ("hullers et décortiqueurs (modèle coopératif "
                  "californien)",
                  "coques et brou aux unités centralisées (Biomass "
                  "Conversion and Biorefinery 2023)", "BCBR 2023"),
        "pays": {
            "États-Unis": ("handlers de Californie (liste officielle "
                           "California Walnut Board)", "SOURCÉ",
                           "la liste publique des handlers documente la "
                           "concentration", "California Walnut Board "
                           "(handler list)"),
            "Chili": ("exportateurs chilians de noix (ChileNut et "
                      "membres)", "ILLUSTRATION",
                      "filière exportatrice organisée", "ChileNut"),
            "Italie": ("centres de transformation Sorrento/Piemonte",
                       "ILLUSTRATION", "filières régionales", "presse"),
            "France": ("coopératives noix du Dauphiné", "ILLUSTRATION",
                       "filière AOP coopérative", "presse filière"),
        },
    },
}

# ------------------------------------------------------------------ logique


def angle_filiere(famille):
    """Angle d'adossement de la famille : PILOTE ou LOI_USINE."""
    return ANGLE_FILIERE.get(famille, "LOI_USINE")


def entree_pays(pays):
    """Mode d'entrée : DIRECT (périmètre pilotes/filiales) ou LICENSING."""
    return ("DIRECT", PAYS_DIRECTS.get(pays, "doctrine international : "
            "licensing/JV, le partenaire finance le matériel")) \
        if pays in PAYS_DIRECTS else \
        ("LICENSING", "doctrine international : licensing/JV, le "
         "partenaire local finance le matériel, Vignite perçoit des "
         "royalties")


def _entree_famille(famille, pays):
    """Résout le dominant de la famille pour le pays donné."""
    bloc = NEGOCIANTS[famille]
    if pays in bloc["pays"]:
        acteur, statut, note, source = bloc["pays"][pays]
        portee = "PAYS"
    else:
        acteur, note, source = bloc["monde"]
        if famille in ANGLE_FILIERE:
            # familles diffuses (PILOTE) : écosystème documenté, pas de
            # dominant mondial unique
            statut = "ILLUSTRATION (écosystème documenté, pas d'acteur " \
                     "unique)"
        else:
            statut = "MONDIAL (proxy : négociant international de la " \
                     "filière)"
        portee = "MONDE"
    return {
        "famille": famille,
        "acteur": acteur,
        "portee": portee,
        "statut": statut,
        "note": note,
        "source": source,
    }


def fiche_hub(hid):
    """Fiche d'adossement d'un hub : une ligne par famille présente."""
    f = sites_transformation.fiche_hub(hid)
    if f is None:
        return None
    lignes = []
    for famille in f["familles"].split("+"):
        e = _entree_famille(famille, f["pays"])
        angle = angle_filiere(famille)
        portee_entree, note_entree = entree_pays(f["pays"])
        if portee_entree == "LICENSING":
            mode = "FRANCHISE"
        else:
            mode = angle
        e.update({
            "angle": angle,
            "entree": portee_entree,
            "mode": mode,
        })
        lignes.append(e)
    return {
        "hub": hid,
        "pays": f["pays"],
        "entree": lignes[0]["entree"] if lignes else "DIRECT",
        "entree_note": entree_pays(f["pays"])[1],
        "familles_partenaires": lignes,
        "etiquette": ("SYNTHÉTIQUE — négociants dominants par faits "
                      "publics, adossement recommandé, aucun contact, "
                      "aucun coût, aucun état de négociation"),
    }


def couches():
    """Couche compacte des 219 hubs pour les cartes interactives."""
    resultat = {}
    for hid in sorted(sites_transformation.hubs_avec_jetons()):
        f = fiche_hub(hid)
        if f is None:
            continue
        resultat[hid] = {
            "pays": f["pays"],
            "entree": f["entree"],
            "familles": [{
                "famille": e["famille"],
                "acteur": e["acteur"],
                "portee": e["portee"],
                "statut": e["statut"],
                "mode": e["mode"],
            } for e in f["familles_partenaires"]],
        }
    return resultat


def sommaire():
    lignes = [
        "World Twin v2.9 — adossement aux négociants dominants",
        "=====================================================",
        "",
        "Par famille de co-produits et par pays : le négociant (ou ",
        "l'écosystème) dominant de la filière, l'angle d'adossement et ",
        "le mode d'entrée. Trois véhicules : PILOTE (gisement diffus), ",
        "LOI_USINE (offtake à l'usine du dominant), FRANCHISE ",
        "(licensing au dominant local hors périmètre direct).",
        "",
        "Familles couvertes : %d" % len(NEGOCIANTS),
    ]
    entrees = sites_transformation.hubs_avec_jetons()
    total_pays = 0
    for famille in sorted(NEGOCIANTS):
        nb_pays = len(NEGOCIANTS[famille]["pays"])
        total_pays += nb_pays
        lignes.append("- %-15s entrées pays : %d" % (famille, nb_pays))
    lignes.append("")
    lignes.append("Hubs couverts : %d — entrées pays directes : %d "
                  "(%s)" % (len(entrees), len(PAYS_DIRECTS),
                            ", ".join(sorted(PAYS_DIRECTS))))
    stats = {"PAYS": 0, "MONDE": 0}
    modes = {"PILOTE": 0, "LOI_USINE": 0, "FRANCHISE": 0}
    for hid in entrees:
        f = fiche_hub(hid)
        for e in f["familles_partenaires"]:
            stats[e["portee"]] = stats.get(e["portee"], 0) + 1
            modes[e["mode"]] = modes.get(e["mode"], 0) + 1
    lignes.append("Lignes d'adossement : %d dont %d ancrées pays "
                  "(SOURCÉ/ILLUSTRATION documenté) et %d en repli "
                  "mondial (proxy)"
                  % (stats["PAYS"] + stats["MONDE"], stats["PAYS"],
                     stats["MONDE"]))
    lignes.append("Modes recommandés : %d LOI à l'usine, %d pilote, "
                  "%d franchise/licensing"
                  % (modes["LOI_USINE"], modes["PILOTE"],
                     modes["FRANCHISE"]))
    lignes.append("")
    lignes.append("Commandes : sommaire | fiche HUB | verifier | table")
    return "\n".join(lignes)


def verifier():
    """Contrôles : couverture, cohérence, anti-fuite."""
    erreurs = []
    familles_flotte = set()
    entrees = sites_transformation.hubs_avec_jetons()
    if len(entrees) != 219:
        erreurs.append("hubs attendus : 219, trouvés : %d" % len(entrees))
    for hid, (pays, jetons) in sorted(entrees.items()):
        f = fiche_hub(hid)
        if f is None:
            erreurs.append("hub sans fiche d'adossement : %s" % hid)
            continue
        if f["pays"] != pays:
            erreurs.append("pays incohérent : %s" % hid)
        for e in f["familles_partenaires"]:
            familles_flotte.add(e["famille"])
            if not e["acteur"]:
                erreurs.append("acteur vide : %s/%s" % (hid, e["famille"]))
            if e["mode"] not in ("PILOTE", "LOI_USINE", "FRANCHISE"):
                erreurs.append("mode inconnu : %s/%s -> %s"
                              % (hid, e["famille"], e["mode"]))
            if e["entree"] not in ("DIRECT", "LICENSING"):
                erreurs.append("entrée inconnue : %s/%s -> %s"
                              % (hid, e["famille"], e["entree"]))
    manquantes = familles_flotte - set(NEGOCIANTS)
    if manquantes:
        erreurs.append("familles sans table négociants : %s"
                       % ", ".join(sorted(manquantes)))
    # anti-fuite : aucun jeton de coût dans les fiches et couches
    charges = json.dumps(couches(), ensure_ascii=False)
    for interdit in JETONS_INTERDITS:
        if interdit in charges:
            erreurs.append("fuite potentielle : jeton « %s »" % interdit)
    # sondages
    sondages = {
        "gen-bresil-3": ("CANNE", "Raízen"),
        "gen-malaisie-1": ("PALMIER", "Sime Darby"),
        "gen-mexique-1": ("CAFE_PULPE", "ECOM"),
        "gen-mexique-3": ("AGAVE", "Cuervo"),
        "gen-mexique-4": ("SARGASSES", "SEMAR"),
        "fr-rhone": ("VIGNE_MARC", "Grap'Sud"),
        "gen-nigeria-1": ("RIZ", "Olam"),
    }
    for hid, (famille, marque) in sondages.items():
        f = fiche_hub(hid)
        if f is None:
            continue
        ligne = next((e for e in f["familles_partenaires"]
                      if e["famille"] == famille), None)
        if ligne is None:
            erreurs.append("sondage sans famille : %s/%s"
                           % (hid, famille))
        elif marque not in ligne["acteur"]:
            erreurs.append("sondage inattendu : %s/%s -> %s"
                           % (hid, famille, ligne["acteur"]))
    if not erreurs:
        print(json.dumps({"verdict": "ok",
                          "hubs": len(entrees),
                          "familles": len(NEGOCIANTS),
                          "entrees_pays_sourced": total_entrees_pays()},
                         ensure_ascii=False, indent=2))
    print("VERDICT : %s (%d erreur(s))"
          % ("OK" if not erreurs else "KO", len(erreurs)))
    for e in erreurs:
        print(" -", e)
    return len(erreurs)


def total_entrees_pays():
    return sum(len(b["pays"]) for b in NEGOCIANTS.values())


def table():
    """Table des 219 hubs : dominant et mode par famille dominante."""
    lignes = []
    for hid in sorted(sites_transformation.hubs_avec_jetons()):
        f = fiche_hub(hid)
        fam_dom = sites_transformation.fiche_hub(hid)["famille_dominante"]
        e = next((x for x in f["familles_partenaires"]
                  if x["famille"] == fam_dom), None)
        if e:
            lignes.append("%-22s %-16s %-14s %-40s %-10s %s"
                          % (hid, f["pays"][:16], fam_dom,
                             e["acteur"][:40], e["mode"],
                             e["portee"]))
    return "\n".join(lignes)


def main():
    args = sys.argv[1:]
    if not args or args[0] == "sommaire":
        print(sommaire())
    elif args[0] == "fiche" and len(args) > 1:
        print(json.dumps(fiche_hub(args[1]), ensure_ascii=False, indent=2))
    elif args[0] == "verifier":
        sys.exit(1 if verifier() else 0)
    elif args[0] == "table":
        print(table())
    elif args[0] == "couches":
        print(json.dumps(couches(), ensure_ascii=False, indent=2))
    else:
        print("attendu : sommaire | fiche HUB | verifier | table | couches")
        sys.exit(1)


if __name__ == "__main__":
    main()
