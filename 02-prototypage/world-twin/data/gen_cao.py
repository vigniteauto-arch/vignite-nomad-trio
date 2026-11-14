#!/usr/bin/env python3
"""Génère les quatre snapshots CaO (P2.9) dans world-twin/data/.

1. cao-pays-referentiel.json : 140 pays de la flotte, français → iso3 +
   bulk FAOSTAT (données publiques, versionnables).
2. cao-bois-faostat-snapshot.json : m³ de bois 2024 par pays (API
   smart-csv FAO, item 1864), 139 pays (Nicaragua absent du bulk,
   documenté).
3. cao-population-snapshot.json : habitants 2023 par iso3 (Our World
   in Data), monde + bases de prorata USGS (14 pays ciment, 11 acier).
4. cao-industrie-snapshot.json : tables USGS MCS 2026 ciment (kt) et
   fer-acier (Mt) extraites positionnellement (data/pdfpos.py).

Rejouable, stdlib uniquement, aucune donnée calibrée (doctrine PI).
"""
import csv
import json
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))        # .../world-twin/data
WT = os.path.dirname(ICI)                                # .../world-twin
DATA = ICI                                               # snapshots versionnés ici
# Données brutes publiques (PDF USGS MCS 2026, population OWID, bois FAO) :
# hors dépôt ; chemin par défaut adapté au bac à sable, sinon variable
# d'environnement WT_DATA_BRUTES.
DATA_BRUTES = os.environ.get(
    "WT_DATA_BRUTES",
    os.path.join(os.path.dirname(WT), "..", "..", "data"))
sys.path.insert(0, DATA)

import pdfpos  # noqa: E402

# --------------------------------------------------------------------------
# Référentiel : 140 pays de la flotte, français → (iso3, bulk FAOSTAT)
# --------------------------------------------------------------------------

REFERENTIEL = {
    "Afghanistan": ("AFG", "Afghanistan"),
    "Afrique du Sud": ("ZAF", "South Africa"),
    "Algérie": ("DZA", "Algeria"),
    "Allemagne": ("DEU", "Germany"),
    "Angola": ("AGO", "Angola"),
    "Arabie Saoudite": ("SAU", "Saudi Arabia"),
    "Argentine": ("ARG", "Argentina"),
    "Australie": ("AUS", "Australia"),
    "Autriche": ("AUT", "Austria"),
    "Azerbaïdjan": ("AZE", "Azerbaijan"),
    "Bangladesh": ("BGD", "Bangladesh"),
    "Belgique": ("BEL", "Belgium"),
    "Belize": ("BLZ", "Belize"),
    "Biélorussie": ("BLR", "Belarus"),
    "Bolivie": ("BOL", "Bolivia (Plurinational State of)"),
    "Botswana": ("BWA", "Botswana"),
    "Brésil": ("BRA", "Brazil"),
    "Bulgarie": ("BGR", "Bulgaria"),
    "Burkina Faso": ("BFA", "Burkina Faso"),
    "Burundi": ("BDI", "Burundi"),
    "Bénin": ("BEN", "Benin"),
    "Cambodge": ("KHM", "Cambodia"),
    "Cameroun": ("CMR", "Cameroon"),
    "Canada": ("CAN", "Canada"),
    "Chili": ("CHL", "Chile"),
    "Chine": ("CHN", "China, mainland"),
    "Chypre": ("CYP", "Cyprus"),
    "Colombie": ("COL", "Colombia"),
    "Congo": ("COG", "Congo"),
    "Corée du Sud": ("KOR", "Republic of Korea"),
    "Costa Rica": ("CRI", "Costa Rica"),
    "Cuba": ("CUB", "Cuba"),
    "Côte d'Ivoire": ("CIV", "Côte d'Ivoire"),
    "Danemark": ("DNK", "Denmark"),
    "El Salvador": ("SLV", "El Salvador"),
    "Espagne": ("ESP", "Spain"),
    "Estonie": ("EST", "Estonia"),
    "Finlande": ("FIN", "Finland"),
    "France": ("FRA", "France"),
    "Gabon": ("GAB", "Gabon"),
    "Gambie": ("GMB", "Gambia"),
    "Ghana": ("GHA", "Ghana"),
    "Grèce": ("GRC", "Greece"),
    "Guatemala": ("GTM", "Guatemala"),
    "Guinée": ("GIN", "Guinea"),
    "Guinée-Bissau": ("GNB", "Guinea-Bissau"),
    "Guyana": ("GUY", "Guyana"),
    "Géorgie": ("GEO", "Georgia"),
    "Haïti": ("HTI", "Haiti"),
    "Honduras": ("HND", "Honduras"),
    "Hongrie": ("HUN", "Hungary"),
    "Inde": ("IND", "India"),
    "Indonésie": ("IDN", "Indonesia"),
    "Irak": ("IRQ", "Iraq"),
    "Iran": ("IRN", "Iran (Islamic Republic of)"),
    "Irlande": ("IRL", "Ireland"),
    "Israël": ("ISR", "Israel"),
    "Italie": ("ITA", "Italy"),
    "Jamaïque": ("JAM", "Jamaica"),
    "Japon": ("JPN", "Japan"),
    "Jordanie": ("JOR", "Jordan"),
    "Kazakhstan": ("KAZ", "Kazakhstan"),
    "Kenya": ("KEN", "Kenya"),
    "Kirghizistan": ("KGZ", "Kyrgyzstan"),
    "Koweït": ("KWT", "Kuwait"),
    "Laos": ("LAO", "Lao People's Democratic Republic"),
    "Lettonie": ("LVA", "Latvia"),
    "Liban": ("LBN", "Lebanon"),
    "Liberia": ("LBR", "Liberia"),
    "Libye": ("LBY", "Libya"),
    "Lituanie": ("LTU", "Lithuania"),
    "Madagascar": ("MDG", "Madagascar"),
    "Malaisie": ("MYS", "Malaysia"),
    "Malawi": ("MWI", "Malawi"),
    "Mali": ("MLI", "Mali"),
    "Maroc": ("MAR", "Morocco"),
    "Maurice": ("MUS", "Mauritius"),
    "Mauritanie": ("MRT", "Mauritania"),
    "Mexique": ("MEX", "Mexico"),
    "Moldavie": ("MDA", "Republic of Moldova"),
    "Mozambique": ("MOZ", "Mozambique"),
    "Myanmar": ("MMR", "Myanmar"),
    "Nicaragua": ("NIC", "Nicaragua"),
    "Niger": ("NER", "Niger"),
    "Nigeria": ("NGA", "Nigeria"),
    "Norvège": ("NOR", "Norway"),
    "Nouvelle-Zélande": ("NZL", "New Zealand"),
    "Népal": ("NPL", "Nepal"),
    "Oman": ("OMN", "Oman"),
    "Ouganda": ("UGA", "Uganda"),
    "Ouzbékistan": ("UZB", "Uzbekistan"),
    "Pakistan": ("PAK", "Pakistan"),
    "Panama": ("PAN", "Panama"),
    "Paraguay": ("PRY", "Paraguay"),
    "Pays-Bas": ("NLD", "Netherlands (Kingdom of the)"),
    "Philippines": ("PHL", "Philippines"),
    "Pologne": ("POL", "Poland"),
    "Portugal": ("PRT", "Portugal"),
    "Pérou": ("PER", "Peru"),
    "Qatar": ("QAT", "Qatar"),
    "RDC": ("COD", "Democratic Republic of the Congo"),
    "Roumanie": ("ROU", "Romania"),
    "Royaume-Uni": ("GBR", "United Kingdom of Great Britain and Northern Ireland"),
    "Russie": ("RUS", "Russian Federation"),
    "Rwanda": ("RWA", "Rwanda"),
    "Rép. dominicaine": ("DOM", "Dominican Republic"),
    "Serbie": ("SRB", "Serbia"),
    "Sierra Leone": ("SLE", "Sierra Leone"),
    "Slovaquie": ("SVK", "Slovakia"),
    "Somalie": ("SOM", "Somalia"),
    "Soudan": ("SDN", "Sudan"),
    "Soudan du Sud": ("SSD", "South Sudan"),
    "Sri Lanka": ("LKA", "Sri Lanka"),
    "Suisse": ("CHE", "Switzerland"),
    "Suriname": ("SUR", "Suriname"),
    "Suède": ("SWE", "Sweden"),
    "Syrie": ("SYR", "Syrian Arab Republic"),
    "Sénégal": ("SEN", "Senegal"),
    "Tadjikistan": ("TJK", "Tajikistan"),
    "Tanzanie": ("TZA", "United Republic of Tanzania"),
    "Tchad": ("TCD", "Chad"),
    "Tchéquie": ("CZE", "Czechia"),
    "Thaïlande": ("THA", "Thailand"),
    "Togo": ("TGO", "Togo"),
    "Trinité-et-Tobago": ("TTO", "Trinidad and Tobago"),
    "Tunisie": ("TUN", "Tunisia"),
    "Turkménistan": ("TKM", "Turkmenistan"),
    "Turquie": ("TUR", "Türkiye"),
    "Ukraine": ("UKR", "Ukraine"),
    "Uruguay": ("URY", "Uruguay"),
    "Venezuela": ("VEN", "Venezuela (Bolivarian Republic of)"),
    "Viêt Nam": ("VNM", "Viet Nam"),
    "Yémen": ("YEM", "Yemen"),
    "Zambie": ("ZMB", "Zambia"),
    "Zimbabwe": ("ZWE", "Zimbabwe"),
    "Égypte": ("EGY", "Egypt"),
    "Émirats arabes unis": ("ARE", "United Arab Emirates"),
    "Équateur": ("ECU", "Ecuador"),
    "États-Unis": ("USA", "United States of America"),
    "Éthiopie": ("ETH", "Ethiopia"),
}

CIMENT_USGS_FR = {
    "United States (includes Puerto Rico)": "États-Unis",
    "Brazil": "Brésil", "China": "Chine", "Egypt": "Égypte",
    "India": "Inde", "Indonesia": "Indonésie", "Iran": "Iran",
    "Japan": "Japon", "Korea, Republic of": "Corée du Sud",
    "Mexico": "Mexique", "Russia": "Russie",
    "Saudi Arabia": "Arabie Saoudite", "Turkey": "Turquie",
    "Vietnam": "Viêt Nam",
}
ACIER_USGS_FR = {
    "United States": "États-Unis", "Brazil": "Brésil", "China": "Chine",
    "Germany": "Allemagne", "India": "Inde", "Iran": "Iran",
    "Japan": "Japon", "Korea, Republic of": "Corée du Sud",
    "Russia": "Russie", "Turkey": "Turquie", "Vietnam": "Viêt Nam",
}

NOMS_CIMENT = ["United States (includes Puerto Rico)", "Brazil", "China",
               "Egypt", "India", "Indonesia", "Iran", "Japan",
               "Korea, Republic of", "Mexico", "Russia", "Saudi Arabia",
               "Turkey", "Vietnam", "Other countries (rounded)",
               "World total (rounded)"]
NOMS_ACIER = ["United States", "Brazil", "China", "Germany", "India",
              "Iran", "Japan", "Korea, Republic of", "Russia", "Turkey",
              "Vietnam", "Other countries", "World total (rounded)"]

CIMENT_ISO3 = ["USA", "BRA", "CHN", "EGY", "IND", "IDN", "IRN", "JPN",
               "KOR", "MEX", "RUS", "SAU", "TUR", "VNM"]
ACIER_ISO3 = ["USA", "BRA", "CHN", "DEU", "IND", "IRN", "JPN", "KOR",
              "RUS", "TUR", "VNM"]


def _ecrire(nom, objet):
    chemin = os.path.join(DATA, nom)
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(objet, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print("écrit :", nom, os.path.getsize(chemin), "octets")


def _nombre(texte):
    return float(texte.replace(",", ""))


def extraire_table(chemin_pdf, colonnes, noms):
    """Extrait la table USGS : noms → [valeur par colonne].

    N'enregistre une ligne que si toutes les cellules sont numériques :
    le texte courant des colonnes voisines peut commencer par un nom de
    pays (« Turkey, 32 % ; Canada, 20 %... ») sans porter de valeurs.
    """
    numerique = re.compile(r"^[\d,\.]+$")
    sortie = {}
    for ligne in pdfpos.par_lignes(chemin_pdf, tolerance=0.05):
        texte = "".join(t for x, t in sorted(ligne["fragments"])).strip()
        for nom_usgs in noms:
            if texte.startswith(nom_usgs) and nom_usgs not in sortie:
                cellules = [pdfpos.cellule(ligne, c) for c in colonnes]
                if all(cellules) and all(numerique.match(c)
                                         for c in cellules):
                    sortie[nom_usgs] = [_nombre(c) for c in cellules]
    manquants = [n for n in noms if n not in sortie]
    assert not manquants, manquants
    return sortie


def main():
    assert len(REFERENTIEL) == 140, len(REFERENTIEL)

    # 1. Référentiel pays.
    _ecrire("cao-pays-referentiel.json", {
        "provenance": {
            "date_extraction": "2026-11-14",
            "note": "Référentiel des 140 pays de la flotte généralisée : "
                    "nom français, code ISO 3166-1 alpha-3, nom bulk "
                    "FAOSTAT. Données publiques, versionnable.",
            "source": "ISO 3166-1 alpha-3 ; noms FAOSTAT ; flotte_monde",
        },
        "pays": {p: {"iso3": i, "faostat": b}
                 for p, (i, b) in REFERENTIEL.items()},
    })

    # 2. Bois FAOSTAT 2024.
    with open(os.path.join(DATA_BRUTES, "bois-faostat-2024.json"),
              encoding="utf-8") as f:
        bois_monde = json.load(f)
    bois, absents = {}, []
    for pays, (_iso3, bulk) in ((p, REFERENTIEL[p]) for p in REFERENTIEL):
        if bulk in bois_monde:
            bois[pays] = bois_monde[bulk]
        else:
            absents.append(pays)
    assert absents == ["Nicaragua"], absents
    assert bois["France"] == 24109400.0, bois["France"]
    assert bois["Maroc"] == 6504769.0, bois["Maroc"]
    assert bois["Chine"] == 145660573.0, bois["Chine"]
    _ecrire("cao-bois-faostat-snapshot.json", {
        "provenance": {
            "annee": 2024,
            "date_extraction": "2026-11-14",
            "item": "Roundwood, industriel (FAOSTAT item 1864)",
            "note": "Mètres cubes par an, valeurs publiques FAOSTAT "
                    "(API smart-csv data.apps.fao.org), versionnables. "
                    "Le Nicaragua est absent du bulk bois 2024 "
                    "(documenté : capacité cendres nulle pour ce pays).",
            "source": "FAOSTAT, api.data.apps.fao.org (item 1864)",
            "controles": {"Chine": 145660573, "France": 24109400,
                          "Maroc": 6504769},
        },
        "unite": "m3/an",
        "pays": bois,
    })

    # 3. Population 2023.
    population = {}
    monde = None
    with open(os.path.join(DATA_BRUTES, "population.csv"),
              encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["year"] != "2023":
                continue
            code = row["code"]
            if row["entity"] == "World" and code == "OWID_WRL":
                monde = int(row["population_historical"])
            elif code:
                population[code] = int(row["population_historical"])
    assert monde is not None and 8.0e9 < monde < 8.2e9, monde
    iso3 = {p: i for p, (i, _b) in REFERENTIEL.items()}
    manquants = [p for p in REFERENTIEL if iso3[p] not in population]
    assert not manquants, manquants
    pays_pop = {REFERENTIEL[p][0]: population[REFERENTIEL[p][0]]
                for p in REFERENTIEL}
    # Bases de prorata USGS : population MONDIALE NON LISTÉE (le
    # dénominateur des parts des pays absents des tables USGS).
    somme_ciment = sum(population[i] for i in CIMENT_ISO3)
    somme_acier = sum(population[i] for i in ACIER_ISO3)
    base_ciment = monde - somme_ciment
    base_acier = monde - somme_acier
    assert 4.4e9 < somme_ciment < 4.7e9, somme_ciment
    assert 3.4e9 < base_ciment < 3.7e9, base_ciment
    assert 4.0e9 < somme_acier < 4.2e9, somme_acier
    assert 3.9e9 < base_acier < 4.1e9, base_acier
    _ecrire("cao-population-snapshot.json", {
        "provenance": {
            "annee": 2023,
            "date_extraction": "2026-11-14",
            "note": "Habitants 2023 par code ISO 3166-1 alpha-3, Our "
                    "World in Data (population_historical). Données "
                    "publiques, versionnables. Les bases de prorata "
                    "USGS sont les populations MONDIALES NON LISTÉES "
                    "(monde moins les pays listés) : elles servent de "
                    "dénominateur pour ventiler les lignes « Autres "
                    "pays » des tables USGS vers chaque pays non "
                    "listé.",
            "source": "Our World in Data, population_historical",
        },
        "monde": monde,
        "pays": pays_pop,
        "bases_prorata_usgs": {
            "ciment": {"iso3_listes": CIMENT_ISO3,
                       "somme_population_listee": somme_ciment,
                       "base_non_listee": base_ciment},
            "acier": {"iso3_listes": ACIER_ISO3,
                      "somme_population_listee": somme_acier,
                      "base_non_listee": base_acier},
        },
    })

    # 4. Industrie USGS MCS 2026 (parseur positionnel).
    ciment = extraire_table(
        os.path.join(DATA_BRUTES, "mcs2026-cement.pdf"),
        [(225, 262), (298, 340), (415, 452), (488, 528)],
        NOMS_CIMENT)
    acier = extraire_table(
        os.path.join(DATA_BRUTES, "mcs2026-iron-steel.pdf"),
        [(250, 280), (300, 335), (410, 448), (475, 505)],
        NOMS_ACIER)
    autres_ciment = ciment.pop("Other countries (rounded)")
    monde_ciment = ciment.pop("World total (rounded)")
    autres_acier = acier.pop("Other countries")
    monde_acier = acier.pop("World total (rounded)")

    # Asserts doctrine (USGS MCS 2026, février 2026).
    assert monde_ciment == [3.9e6, 3.8e6, 3.8e6, 3.8e6], monde_ciment
    assert autres_ciment == [8.6e5, 8.6e5, 6.5e5, 6.5e5], autres_ciment
    assert ciment["China"][1] == 1.7e6, ciment["China"]
    assert monde_acier == [1280, 1300, 1880, 1900], monde_acier
    assert autres_acier == [78, 93, 269, 280], autres_acier
    assert acier["China"] == [852, 830, 1010, 980], acier["China"]
    assert 1250 <= monde_acier[0] <= 1350, monde_acier[0]
    somme_ciment = sum(v[1] for v in ciment.values()) + autres_ciment[1]
    assert abs(somme_ciment - monde_ciment[1]) / monde_ciment[1] <= 0.03
    somme_acier = sum(v[3] for v in acier.values()) + autres_acier[3]
    assert abs(somme_acier - monde_acier[3]) / monde_acier[3] <= 0.03

    _ecrire("cao-industrie-snapshot.json", {
        "provenance": {
            "date_extraction": "2026-11-14",
            "note": "Tables USGS Mineral Commodity Summaries 2026 "
                    "(février 2026) extraites positionnellement "
                    "(data/pdfpos.py). Ciment en milliers de tonnes : "
                    "production 2024, production 2025 (estimée), "
                    "capacité clinker 2024, capacité clinker 2025 "
                    "(estimée). Fer et acier en millions de tonnes : "
                    "fonte 2024, fonte 2025e, acier brut 2024, acier "
                    "brut 2025e. Données publiques, versionnables.",
            "source": "USGS, Mineral Commodity Summaries 2026 "
                      "(Cement ; Iron and Steel)",
        },
        "ciment_kt": {
            "pays": {CIMENT_USGS_FR[k]: v for k, v in ciment.items()},
            "autres": autres_ciment,
            "monde": monde_ciment,
        },
        "acier_mt": {
            "pays": {ACIER_USGS_FR[k]: v for k, v in acier.items()},
            "autres": autres_acier,
            "monde": monde_acier,
        },
    })
    print("asserts doctrine : OK")


if __name__ == "__main__":
    main()
