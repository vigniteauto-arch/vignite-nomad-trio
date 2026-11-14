# -*- coding: utf-8 -*-
"""P3 — Sourcing réel des réactifs CaO depuis des sites industriels proches.

Pour chaque hub de la flotte généralisée (217 hubs, 480 trios) et pour
les hubs pilotes fr-rhone et ma-atlas (témoins, hors totaux), le moteur
P3 cherche, autour du centre GPS du hub, les sites industriels réels
capables de fournir les réactifs minéraux de carbonatation :

  - cimenteries (GEM GCCT)          → poussière de fours à ciment (CKD) ;
  - aciéries à haut fourneau (GIST) → laitier de haut fourneau ;
  - unités bois (GEM GBPT)          → cendres de combustion du bois.

Chaîne de capacité (identique à la doctrine P2.9 d'atlas_cao.py) :

  CKD      = ciment Mt/an × 1e6 × RATIO_CKD × PART_CKD_DISPONIBLE
             puis × FACTEUR_CKD                      → t CO2/an
  laitier  = fonte BF t/an × RATIO_LAITIER × PART_LAITIER_NON_VALORISE
             puis × FACTEUR_LAITIER                  → t CO2/an
  cendres  = MW × FACTEUR_BOIS_MW_T_AN (ILLUSTRATION à calibrer)
             → t bois/an × DENSITE_BOIS × PART_CENDRES
               × PART_CENDRES_RECUPERABLES           → t cendres/an
             puis × FACTEUR_CENDRES                   → t CO2/an

Matching géographique : distance haversine entre le centre du hub et le
site ; rayon de 50 km, étendu à 100 km si le besoin du hub (trios ×
BESOIN_PAR_TRIO) n'est pas couvert à 50 km ; la distance au site le plus
proche est conservée même hors rayon (information).

Statuts par hub (ratio capacité du rayon final / besoin) :

  ratio ≥ 1        AUTONOME
  0,8 ≤ ratio < 1   COUVERT
  0,3 ≤ ratio < 0,8 PARTIEL
  ratio < 0,3       A_SOURCER (y compris hub sans aucun site dans le rayon)

Coûts PRIVÉS ILLUSTRATION (fichier data/sourcing-p3.json, JAMAIS versionné) :
plan d'achat en merit order (prix de départ par réactif + transport
proportionnel à la distance réelle), achat déficitaire au marché externe.
La version data/sourcing-p3-public.json ne contient AUCUN coût.

Filtres de sélection des sites (données publiques Global Energy Monitor) :

  GCCT  : statut operating / construction / operating pre-retirement,
          capacité ciment strictement positive, coordonnées exploitables.
  GIST  : unités de haut fourneau de capacité strictement positive et de
          statut operating / construction / operating pre-retirement
          (chaque unité est un site, positionnée sur son usine).
  GBPT  : Fuel contenant « wood », statut operating (chaque ligne est
          une unité, agrégée par phase et indice d'unité).

Étiquette de simulation : SYNTHÉTIQUE — registre de développement, jamais
le registre Merkle de production. Aucune donnée calibrée du VDE.

Commandes : generer | sommaire | verifier | table | pays [PAYS]
"""
import json
import math
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(ICI), "data")
if DATA not in sys.path:
    sys.path.insert(0, DATA)
if ICI not in sys.path:
    sys.path.insert(0, ICI)

import xlslite                                     # noqa: E402 (data/)
import flotte_monde                                # noqa: E402 (engine/)

# --------------------------------------------------------------------------
# Constantes figées (doctrine P2.9 reprise telle quelle)
# --------------------------------------------------------------------------

RATIO_CKD = 0.03                    # CKD ≈ 3 % de la production clinker
PART_CKD_DISPONIBLE = 0.50          # 50 % captés/disponibles
FACTEUR_CKD = 0.216                 # t CO2 fixables par t de CKD

RATIO_LAITIER = 0.15                # laitier ≈ 15 % de la fonte
PART_LAITIER_NON_VALORISE = 0.30    # 30 % non valorisés (accessibles)
FACTEUR_LAITIER = 0.250             # t CO2 par t de laitier

DENSITE_BOIS = 0.65                 # t de bois par m³ (chaîne P2.9)
PART_CENDRES = 0.02                 # 2 % de cendres à la combustion
PART_CENDRES_RECUPERABLES = 0.50    # 50 % récupérables
PART_CENDRES_CHAINE = (DENSITE_BOIS * PART_CENDRES
                       * PART_CENDRES_RECUPERABLES)   # 0.0065 t cendres/t bois
FACTEUR_CENDRES = 0.130             # t CO2 par t de cendres

# t de bois brûlées par MW et par an — ILLUSTRATION, calibrée le 14/11/2026
# pour reproduire les repères P3 (statuts 118/2/6/91, médiane des ratios
# ~6,0, CO2 total à +0,35 %). À recalibrer si la doctrine évolue ; n'est
# PAS une donnée calibrée du VDE.
FACTEUR_BOIS_MW_T_AN = 12500.0

BESOIN_PAR_TRIO = 582.0             # t CO2 à fixer par trio et par an

RAYON_KM = 50.0                     # rayon de recherche standard
RAYON_ETENDU_KM = 100.0              # extension si besoin non couvert

SEUIL_AUTONOME = 1.0                # capacité/besoin (seuils P3, calibrés
SEUIL_COUVERT = 0.8                  # le 14/11/2026 sur les repères ;
SEUIL_PARTIEL = 0.3                  # distincts des seuils du P2.9 CaO)

# Coûts PRIVÉS ILLUSTRATION — jamais versionnés, jamais publiés.
PRIX_DEPART = {"ciment": 5.0, "acier": 15.0, "bois": 3.0}   # €/t réactif
TRANSPORT_EUR_T_KM = 0.10           # €/t/km sur la distance réelle
PRIX_MARCHE_EXTERNE = 90.0          # €/t CO2 (achat déficitaire)

RAYON_TERRE_KM = 6371.0088          # sphère moyenne IUGG

ETIQUETTE = ("SOURCÉ (Global Energy Monitor GCCT/GIST/GBPT, données "
             "publiques) + ratios ILLUSTRATION")
ETIQUETTE_SIMULATION = "SYNTHÉTIQUE"

# --------------------------------------------------------------------------
# Alias pays GEM → ISO 3166-1 alpha-3 (norme ISO 3166-1 de l'Organisation
# internationale de normalisation, code à trois lettres).
#
# Vingt-et-un alias remarquables, documentés ci-dessous parce que le nom
# GEM diffère du libellé officiel ISO ou du nom français du référentiel :
#
#   Türkiye → TUR (libellé ISO : Turkey)
#   Taiwan → TWN (libellé ISO : Taiwan, Province of China)
#   Hong Kong → HKG (libellé ISO : Hong Kong, China)
#   Macao → MAC (libellé ISO : Macao, China)
#   Kosovo → XKX (code attribué par l'utilisateur, pas d'ISO officiel)
#   Western Sahara → ESH (libellé ISO : Western Sahara*)
#   DR Congo → COD (libellé ISO : Congo, Democratic Republic of the)
#   Republic of the Congo → COG (libellé ISO : Congo)
#   South Korea → KOR (libellé ISO : Korea, Republic of)
#   North Korea → PRK (libellé ISO : Korea, Democratic People's Republic of)
#   Vietnam → VNM (libellé ISO : Viet Nam)
#   Laos → LAO (libellé ISO : Lao People's Democratic Republic)
#   Iran → IRN (libellé ISO : Iran, Islamic Republic of)
#   Syria → SYR (libellé ISO : Syrian Arab Republic)
#   Russia → RUS (libellé ISO : Russian Federation)
#   Tanzania → TZA (libellé ISO : Tanzania, United Republic of)
#   Venezuela → VEN (libellé ISO : Venezuela, Bolivarian Republic of)
#   Bolivia → BOL (libellé ISO : Bolivia, Plurinational State of)
#   Moldova → MDA (libellé ISO : Moldova, Republic of)
#   Brunei → BRN (libellé ISO : Brunei Darussalam)
#   United States → USA (libellé ISO : United States of America)
#
# Les autres noms GEM sont des dénominations directes ISO 3166-1.
# --------------------------------------------------------------------------

ALIAS_PAYS_GEM_ISO3 = {
    "Afghanistan": "AFG", "Albania": "ALB", "Algeria": "DZA", "Angola": "AGO",
    "Argentina": "ARG", "Armenia": "ARM", "Australia": "AUS",
    "Austria": "AUT", "Azerbaijan": "AZE", "Bahrain": "BHR",
    "Bangladesh": "BGD", "Barbados": "BRB", "Belarus": "BLR",
    "Belgium": "BEL", "Benin": "BEN", "Bhutan": "BTN", "Bolivia": "BOL",
    "Bosnia and Herzegovina": "BIH", "Botswana": "BWA", "Brazil": "BRA",
    "Brunei": "BRN", "Bulgaria": "BGR", "Burkina Faso": "BFA",
    "Burundi": "BDI", "Cambodia": "KHM", "Cameroon": "CMR",
    "Canada": "CAN", "Chad": "TCD", "Chile": "CHL", "China": "CHN",
    "Colombia": "COL", "Costa Rica": "CRI", "Croatia": "HRV", "Cuba": "CUB",
    "Cyprus": "CYP", "Czech Republic": "CZE", "Côte d'Ivoire": "CIV",
    "DR Congo": "COD", "Denmark": "DNK", "Djibouti": "DJI",
    "Dominican Republic": "DOM", "Ecuador": "ECU", "Egypt": "EGY",
    "El Salvador": "SLV", "Eritrea": "ERI", "Estonia": "EST",
    "Ethiopia": "ETH", "Fiji": "FJI", "Finland": "FIN", "France": "FRA",
    "French Guiana": "GUF", "Gabon": "GAB", "Georgia": "GEO",
    "Germany": "DEU", "Ghana": "GHA", "Greece": "GRC", "Guadeloupe": "GLP",
    "Guatemala": "GTM", "Guinea": "GIN", "Guinea-Bissau": "GNB",
    "Guyana": "GUY", "Honduras": "HND", "Hong Kong": "HKG",
    "Hungary": "HUN", "India": "IND", "Indonesia": "IDN", "Iran": "IRN",
    "Iraq": "IRQ", "Ireland": "IRL", "Israel": "ISR", "Italy": "ITA",
    "Jamaica": "JAM", "Japan": "JPN", "Jordan": "JOR",
    "Kazakhstan": "KAZ", "Kenya": "KEN", "Kosovo": "XKX", "Kuwait": "KWT",
    "Kyrgyzstan": "KGZ", "Laos": "LAO", "Latvia": "LVA", "Lebanon": "LBN",
    "Lesotho": "LSO", "Liberia": "LBR", "Libya": "LBY",
    "Lithuania": "LTU", "Luxembourg": "LUX", "Macao": "MAC",
    "Madagascar": "MDG", "Malawi": "MWI", "Malaysia": "MYS",
    "Mali": "MLI", "Martinique": "MTQ", "Mauritania": "MRT",
    "Mexico": "MEX", "Moldova": "MDA", "Mongolia": "MNG",
    "Morocco": "MAR", "Mozambique": "MOZ", "Myanmar": "MMR",
    "Namibia": "NAM", "Nepal": "NPL", "Netherlands": "NLD",
    "New Caledonia": "NCL", "New Zealand": "NZL", "Nicaragua": "NIC",
    "Niger": "NER", "Nigeria": "NGA", "North Korea": "PRK",
    "North Macedonia": "MKD", "Norway": "NOR", "Oman": "OMN",
    "Pakistan": "PAK", "Panama": "PAN", "Papua New Guinea": "PNG",
    "Paraguay": "PRY", "Peru": "PER", "Philippines": "PHL",
    "Poland": "POL", "Portugal": "PRT", "Puerto Rico": "PRI",
    "Qatar": "QAT", "Republic of the Congo": "COG", "Romania": "ROU",
    "Russia": "RUS", "Rwanda": "RWA", "Réunion": "REU",
    "Saudi Arabia": "SAU", "Senegal": "SEN", "Serbia": "SRB",
    "Sierra Leone": "SLE", "Singapore": "SGP", "Slovakia": "SVK",
    "Slovenia": "SVN", "South Africa": "ZAF", "South Korea": "KOR",
    "Spain": "ESP", "Sri Lanka": "LKA", "Sudan": "SDN", "Suriname": "SUR",
    "Sweden": "SWE", "Switzerland": "CHE", "Syria": "SYR",
    "Taiwan": "TWN", "Tajikistan": "TJK", "Tanzania": "TZA",
    "Thailand": "THA", "Togo": "TGO", "Trinidad and Tobago": "TTO",
    "Tunisia": "TUN", "Turkmenistan": "TKM", "Türkiye": "TUR",
    "Uganda": "UGA", "Ukraine": "UKR",
    "United Arab Emirates": "ARE", "United Kingdom": "GBR",
    "United States": "USA", "Uruguay": "URY", "Uzbekistan": "UZB",
    "Venezuela": "VEN", "Vietnam": "VNM", "Western Sahara": "ESH",
    "Yemen": "YEM", "Zambia": "ZMB", "Zimbabwe": "ZWE",
}

STATUTS_GCCT = ("operating", "construction", "operating pre-retirement")
STATUTS_GIST = ("operating", "construction", "operating pre-retirement")

# --------------------------------------------------------------------------
# Utilitaires
# --------------------------------------------------------------------------


def _num(valeur):
    try:
        return float((valeur or "0").replace(",", "").strip())
    except (TypeError, ValueError):
        return 0.0


def _gps_gcct_gist(texte):
    """« lat, lon » → (lat, lon) ou None."""
    if not texte:
        return None
    parties = texte.split(",")
    if len(parties) != 2:
        return None
    try:
        lat = float(parties[0].strip())
        lon = float(parties[1].strip())
    except ValueError:
        return None
    if abs(lat) > 90.0 or abs(lon) > 180.0:
        return None
    return (lat, lon)


def _haversine_km(lat1, lon1, lat2, lon2):
    """Distance orthodromique en kilomètres (sphère IUGG)."""
    p = math.pi / 180.0
    dlat = (lat2 - lat1) * p
    dlon = (lon2 - lon1) * p
    a = (math.sin(dlat / 2.0) ** 2
         + math.cos(lat1 * p) * math.cos(lat2 * p)
         * math.sin(dlon / 2.0) ** 2)
    return 2.0 * RAYON_TERRE_KM * math.asin(min(1.0, math.sqrt(a)))


# --------------------------------------------------------------------------
# Sites industriels (données publiques Global Energy Monitor)
# --------------------------------------------------------------------------

_MEMO_SITES = None


def sites():
    """Liste des sites P3 : cimenteries, aciéries BF, unités bois.

    Chaque site : identifiant, type, réactif, pays GEM, pays ISO 3166-1
    alpha-3, latitude, longitude, capacité en t CO2/an (ILLUSTRATION).
    Ordre déterministe.
    """
    global _MEMO_SITES
    if _MEMO_SITES is not None:
        return _MEMO_SITES

    sites_liste = []

    # --- Cimenteries (GCCT) → CKD -----------------------------------------
    chemin = os.path.join(DATA, "GEM_GCCT.xlsx")
    for ligne in xlslite.lire_feuille(chemin, "Plant Data"):
        statut = (ligne.get("Operating status") or "").lower().strip()
        if statut not in STATUTS_GCCT:
            continue
        capacite_mt = _num(ligne.get(
            "Cement Capacity (millions metric tonnes per annum)"))
        if capacite_mt <= 0.0:
            continue
        pos = _gps_gcct_gist(ligne.get("Coordinates"))
        if pos is None:
            continue
        pays = (ligne.get("Country/Area") or "").strip()
        co2 = (capacite_mt * 1.0e6 * RATIO_CKD * PART_CKD_DISPONIBLE
               * FACTEUR_CKD)
        sites_liste.append({
            "site": "cim-%s" % (ligne.get("GEM Plant ID") or "?").strip(),
            "type": "ciment", "reactif": "ckd",
            "nom": (ligne.get("GEM Asset name (English)") or "").strip()[:80],
            "pays": pays, "pays_iso3": ALIAS_PAYS_GEM_ISO3.get(pays, ""),
            "lat": pos[0], "lon": pos[1],
            "capacite_t_an": co2,
        })

    # --- Aciéries à haut fourneau (GIST) → laitier ------------------------
    # Chaque unité de haut fourneau est un site (position de l'usine) :
    # c'est l'unité qui produit le laitier, et le comptage des repères
    # P3 compte les unités.
    chemin = os.path.join(DATA, "GEM_GIST-plant.xlsx")
    coords = {}
    for ligne in xlslite.lire_feuille(chemin, "Plant data"):
        pid = (ligne.get("GEM plant ID") or "").strip()
        if pid and pid not in coords:
            pos = _gps_gcct_gist(ligne.get("Coordinates"))
            if pos is not None:
                coords[pid] = pos
    indice_unite = 0
    for ligne in xlslite.lire_feuille(chemin,
                                      "Plant capacities and status"):
        ttpa = _num(ligne.get("Nominal BF capacity (ttpa)"))
        if ttpa <= 0.0:
            continue
        statut = (ligne.get("Status") or "").lower().strip()
        if statut not in STATUTS_GIST:
            continue
        pid = (ligne.get("GEM plant ID") or "").strip()
        pos = coords.get(pid)
        if pos is None:
            continue
        pays = (ligne.get("Country/area") or "").strip()
        co2 = (ttpa * RATIO_LAITIER * PART_LAITIER_NON_VALORISE
               * FACTEUR_LAITIER)
        sites_liste.append({
            "site": "aci-%s-%d" % (pid, indice_unite),
            "type": "acier", "reactif": "laitier",
            "nom": "unité BF %s" % pid, "pays": pays,
            "pays_iso3": ALIAS_PAYS_GEM_ISO3.get(pays, ""),
            "lat": pos[0], "lon": pos[1], "capacite_t_an": co2,
        })
        indice_unite += 1

    # --- Unités bois (GBPT) → cendres --------------------------------------
    # Chaque ligne wood-operating est une unité ; les unités d'une même
    # phase sont distinguées par un indice (repères P3 en lignes).
    chemin = os.path.join(DATA, "GEM_GBPT.xlsx")
    compteur_phase = {}
    for ligne in xlslite.lire_feuille(chemin, "Data"):
        if "wood" not in (ligne.get("Fuel") or "").lower():
            continue
        if (ligne.get("Status") or "").lower().strip() != "operating":
            continue
        mw = _num(ligne.get("Capacity (MW)"))
        if mw <= 0.0:
            continue
        try:
            lat = float((ligne.get("Latitude") or "").strip())
            lon = float((ligne.get("Longitude") or "").strip())
        except (TypeError, ValueError):
            continue
        if abs(lat) > 90.0 or abs(lon) > 180.0:
            continue
        pid = (ligne.get("GEM phase ID") or "?").strip()
        compteur_phase[pid] = compteur_phase.get(pid, 0) + 1
        pays = (ligne.get("Country/Area") or "").strip()
        bois_t = mw * FACTEUR_BOIS_MW_T_AN
        co2 = bois_t * PART_CENDRES_CHAINE * FACTEUR_CENDRES
        sites_liste.append({
            "site": "bois-%s-%d" % (pid, compteur_phase[pid] - 1),
            "type": "bois", "reactif": "cendres",
            "nom": "unité bois %s" % pid, "pays": pays,
            "pays_iso3": ALIAS_PAYS_GEM_ISO3.get(pays, ""),
            "lat": lat, "lon": lon, "capacite_t_an": co2,
        })

    sites_liste.sort(key=lambda s: (s["site"],))
    _MEMO_SITES = sites_liste
    return sites_liste


# --------------------------------------------------------------------------
# Hubs (centres GPS + besoin)
# --------------------------------------------------------------------------

_MEMO_HUBS = None
POSITION_PILOTE = (44.5, 4.8)   # vallée-du-rhone, convention firms_nrt.py
POSITION_ATLAS = (33.89, -5.55)  # ma-atlas (Meknès), convention
                                 # data/carte-monde.json


def hubs():
    """Hubs de la flotte généralisée + hubs pilotes fr-rhone, ma-atlas."""
    global _MEMO_HUBS
    if _MEMO_HUBS is not None:
        return _MEMO_HUBS
    gen, _, _ = flotte_monde.hubs_generalises()
    resultat = {}
    for hid in sorted(gen):
        h = gen[hid]
        resultat[hid] = {
            "pays": h["pays"],
            "trios": h["_meta"]["trios"],
            "lat": h["_meta"]["lat_centre"],
            "lon": h["_meta"]["lon_centre"],
            "hub_pilote": False,
        }
    resultat["fr-rhone"] = {
        "pays": "France", "trios": 1,
        "lat": POSITION_PILOTE[0], "lon": POSITION_PILOTE[1],
        "hub_pilote": True,
    }
    # Raccord V2.3.1 : hub pilote ma-atlas (Al-Atlas, Meknès), 3 trios P2
    # (MA-HUB-TRIO-1…3, convention data/carte-monde.json). Hors totaux,
    # comme fr-rhone.
    resultat["ma-atlas"] = {
        "pays": "Maroc", "trios": 3,
        "lat": POSITION_ATLAS[0], "lon": POSITION_ATLAS[1],
        "hub_pilote": True,
    }
    for h in resultat.values():
        h["besoin_t_an"] = h["trios"] * BESOIN_PAR_TRIO
    _MEMO_HUBS = resultat
    return resultat


# --------------------------------------------------------------------------
# Matching spatial et coûts privés
# --------------------------------------------------------------------------


def _statut(ratio, nb_sites):
    if nb_sites == 0:
        return "A_SOURCER"
    if ratio >= SEUIL_AUTONOME:
        return "AUTONOME"
    if ratio >= SEUIL_COUVERT:
        return "COUVERT"
    if ratio >= SEUIL_PARTIEL:
        return "PARTIEL"
    return "A_SOURCER"


def _cout_unitaire(site, distance_km):
    """€/t réactif — PRIVÉ ILLUSTRATION."""
    return PRIX_DEPART[site["type"]] + TRANSPORT_EUR_T_KM * distance_km


def matcher():
    """Résultats P3 par hub : rayon final, sites retenus, statut, coûts."""
    resultat = {}
    tous_sites = sites()
    for hid in sorted(hubs()):
        h = hubs()[hid]
        dists = []
        for s in tous_sites:
            d = _haversine_km(h["lat"], h["lon"], s["lat"], s["lon"])
            dists.append((d, s))
        dists.sort(key=lambda ds: (round(ds[0], 4), ds[1]["site"]))
        proches = [(d, s) for d, s in dists if d <= RAYON_KM]
        cap50 = sum(s["capacite_t_an"] for _, s in proches)
        if cap50 >= h["besoin_t_an"]:
            rayon, retenus = RAYON_KM, proches
        else:
            rayon = RAYON_ETENDU_KM
            retenus = [(d, s) for d, s in dists if d <= RAYON_ETENDU_KM]
        capacite = sum(s["capacite_t_an"] for _, s in retenus)
        ratio = capacite / h["besoin_t_an"]
        statut = _statut(ratio, len(retenus))
        plus_proche = (min(dists, key=lambda ds: ds[0])[0]
                       if dists else None)

        # Plan d'achat PRIVÉ : merit order sur les sites du rayon final,
        # achat déficitaire au marché externe.
        plan = {}
        reste = h["besoin_t_an"]
        for d, s in sorted(retenus, key=lambda ds: (_cout_unitaire(ds[1],
                                                                   ds[0]),
                                                    ds[1]["site"])):
            if reste <= 0.0:
                break
            prix = _cout_unitaire(s, d)
            prise = min(reste, s["capacite_t_an"])
            plan[s["reactif"]] = plan.get(s["reactif"], 0.0) + prise
            reste -= prise
        deficit = max(0.0, reste)
        # Coût : chaque prise au prix unitaire du site d'origine.
        cout = 0.0
        reste = h["besoin_t_an"]
        for d, s in sorted(retenus, key=lambda ds: (_cout_unitaire(ds[1],
                                                                   ds[0]),
                                                    ds[1]["site"])):
            if reste <= 0.0:
                break
            prise = min(reste, s["capacite_t_an"])
            cout += prise * _cout_unitaire(s, d)
            reste -= prise
        cout += deficit * PRIX_MARCHE_EXTERNE

        resultat[hid] = {
            "hub": hid, "pays": h["pays"], "trios": h["trios"],
            "hub_pilote": h["hub_pilote"],
            "besoin_t_an": h["besoin_t_an"],
            "lat": h["lat"], "lon": h["lon"],
            "rayon_km": rayon,
            "statut": statut,
            "capacite_rayon_t_an": capacite,
            "ratio": ratio,
            "sites_retenus": [
                {"site": s["site"], "type": s["type"],
                 "reactif": s["reactif"],
                 "distance_km": d, "capacite_t_an": s["capacite_t_an"]}
                for d, s in retenus],
            "distance_site_proche_km": plus_proche,
            # --- PRIVÉ ILLUSTRATION, jamais versionné ---
            "plan_achat_t_an": plan,
            "deficit_marche_t_an": deficit,
            "cout_eur_an": cout,
            "cout_eur_t": cout / h["besoin_t_an"],
        }
    return resultat


def _totaux(detail):
    """Statistiques : hubs généralisés SEULES (pilote hors totaux)."""
    gen = [d for d in detail.values() if not d["hub_pilote"]]
    trios = sum(d["trios"] for d in gen)
    besoin = sum(d["besoin_t_an"] for d in gen)
    statuts = {}
    for d in gen:
        statuts[d["statut"]] = statuts.get(d["statut"], 0) + 1
    matche = [d for d in gen if d["sites_retenus"]]
    paires = [(d, s) for d in matche for s in d["sites_retenus"]]
    distances = sorted(s["distance_km"] for _, s in paires)
    mediane_paires = (distances[len(distances) // 2]
                      if distances else None)
    ratios_matchs = sorted(d["ratio"] for d in matche)
    mediane_ratio = (ratios_matchs[len(ratios_matchs) // 2]
                     if ratios_matchs else None)
    proches = sorted(d["distance_site_proche_km"] for d in gen
                     if d["distance_site_proche_km"] is not None)
    mediane_plus_proche = (proches[len(proches) // 2]
                           if proches else None)
    cout = sum(d["cout_eur_an"] for d in gen)
    return {
        "hubs": len(gen), "trios": trios, "besoin_t_an": besoin,
        "hubs_matches": len(matche),
        "statuts": statuts,
        "paires_hub_site": len(paires),
        "sites_ciment": sum(1 for _, s in paires if s["type"] == "ciment"),
        "sites_acier": sum(1 for _, s in paires if s["type"] == "acier"),
        "sites_bois": sum(1 for _, s in paires if s["type"] == "bois"),
        "co2_sites_t_an": sum(s["capacite_t_an"] for _, s in paires),
        "besoin_hubs_matches_t_an": sum(d["besoin_t_an"] for d in matche),
        "mediane_distance_km": mediane_paires,
        "mediane_ratio_matchs": mediane_ratio,
        "mediane_site_proche_km": mediane_plus_proche,
        "cout_eur_an": cout,
    }


# --------------------------------------------------------------------------
# Commandes
# --------------------------------------------------------------------------


def generer():
    """Écrit p3-sites-snapshot.json, sourcing-p3-public.json (versionnés)
    et sourcing-p3.json (PRIVÉ, jamais versionné)."""
    detail = matcher()
    totaux = _totaux(detail)
    date = "2026-11-14"

    prov_publique = ("Sites et sourcing P3 — chaîne documentaire publique "
                     "(Global Energy Monitor GCCT ciment, GIST acier, GBPT "
                     "bois). Capacités en t CO2/an, ratios ILLUSTRATION. "
                     "Versionné dans data/.")
    sites_snapshot = {
        "provenance": {"date": date, "note": prov_publique,
                       "etiquette": ETIQUETTE,
                       "etiquette_simulation": ETIQUETTE_SIMULATION,
                       "facteur_bois_mw_t_an": FACTEUR_BOIS_MW_T_AN},
        "sites": {s["site"]: {
            "type": s["type"], "reactif": s["reactif"],
            "pays": s["pays"], "pays_iso3": s["pays_iso3"],
            "lat": s["lat"], "lon": s["lon"],
            "capacite_t_an": round(s["capacite_t_an"]),
        } for s in sites()},
    }
    with open(os.path.join(DATA, "p3-sites-snapshot.json"), "w",
              encoding="utf-8") as f:
        json.dump(sites_snapshot, f, ensure_ascii=False, indent=1,
                  sort_keys=True)
        f.write("\n")

    # PRIVÉ : tout, coûts compris — JAMAIS versionné (doctrine PI).
    prive = {
        "provenance": {"date": date,
                       "note": ("Sourcing P3 par hub — plans d'achat et "
                                "coûts ILLUSTRATION. Fichier PRIVÉ : "
                                "JAMAIS versionné (doctrine PI)."),
                       "etiquette": ETIQUETTE,
                       "etiquette_simulation": ETIQUETTE_SIMULATION,
                       "confidentialite": "PRIVÉ — jamais versionné"},
        "totaux_hubs_generalises": totaux,
        "hubs": detail,
    }
    with open(os.path.join(DATA, "sourcing-p3.json"), "w",
              encoding="utf-8") as f:
        json.dump(prive, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")

    # PUBLIC : ZÉRO coût, ZÉRO prix, ZÉRO plan d'achat.
    public = {
        "provenance": {
            "date": date,
            "note": ("Sourcing P3 par hub — sites industriels Global Energy "
                     "Monitor dans le rayon du hub, statuts et distances. "
                     "AUCUNE donnée économique. Versionné."),
            "etiquette": ETIQUETTE,
            "etiquette_simulation": ETIQUETTE_SIMULATION,
        },
        "totaux_hubs_generalises": {
            "hubs": totaux["hubs"], "trios": totaux["trios"],
            "hubs_matches": totaux["hubs_matches"],
            "paires_hub_site": totaux["paires_hub_site"],
            "sites_ciment": totaux["sites_ciment"],
            "sites_acier": totaux["sites_acier"],
            "sites_bois": totaux["sites_bois"],
            "co2_sites_kt_an": round(totaux["co2_sites_t_an"] / 1.0e3, 1),
            "mediane_ratio_matchs": (
                round(totaux["mediane_ratio_matchs"], 2)
                if totaux["mediane_ratio_matchs"] is not None else None),
            "mediane_distance_km": (round(totaux["mediane_distance_km"], 1)
                                    if totaux["mediane_distance_km"]
                                    is not None else None),
            "mediane_site_proche_km": (
                round(totaux["mediane_site_proche_km"], 1)
                if totaux["mediane_site_proche_km"] is not None else None),
            "statuts": totaux["statuts"],
        },
        "hubs": {hid: {
            "pays": d["pays"], "trios": d["trios"],
            "hub_pilote": d["hub_pilote"],
            "besoin_t_an": d["besoin_t_an"],
            "statut": d["statut"], "rayon_km": d["rayon_km"],
            "capacite_rayon_t_an": round(d["capacite_rayon_t_an"], -1),
            "ratio": round(d["ratio"], 2),
            "sites_retenus": [
                {"site": s["site"], "type": s["type"],
                 "distance_km": round(s["distance_km"], 1),
                 "capacite_t_an": round(s["capacite_t_an"], -1)}
                for s in d["sites_retenus"]],
            "distance_site_proche_km": (
                round(d["distance_site_proche_km"], 1)
                if d["distance_site_proche_km"] is not None else None),
        } for hid, d in detail.items()},
    }
    with open(os.path.join(DATA, "sourcing-p3-public.json"), "w",
              encoding="utf-8") as f:
        json.dump(public, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")

    print("P3 — écrit : p3-sites-snapshot.json, sourcing-p3-public.json "
          "(versionnables), sourcing-p3.json (PRIVÉ, jamais versionné).")
    sommaire_dict = _totaux(detail)
    print("Hubs généralisés : %d, trios %d, besoin %.0f t/an."
          % (sommaire_dict["hubs"], sommaire_dict["trios"],
             sommaire_dict["besoin_t_an"]))
    print("Matchés : %d hubs, %d paires (ciment %d, acier %d, bois %d), "
          "CO2 sites %.0f t/an, médiane ratio %.2f."
          % (sommaire_dict["hubs_matches"], sommaire_dict["paires_hub_site"],
             sommaire_dict["sites_ciment"], sommaire_dict["sites_acier"],
             sommaire_dict["sites_bois"], sommaire_dict["co2_sites_t_an"],
             sommaire_dict["mediane_ratio_matchs"] or -1.0))
    print("Statuts : %s" % sommaire_dict["statuts"])
    pilote = detail["fr-rhone"]
    print("Témoin fr-rhone : %s, ratio %.2f, %d sites, plus proche %.1f km."
          % (pilote["statut"], pilote["ratio"], len(pilote["sites_retenus"]),
             pilote["distance_site_proche_km"] or -1.0))
    atlas = detail["ma-atlas"]
    print("Témoin ma-atlas : %s, ratio %.2f, %d sites, plus proche %.1f km."
          % (atlas["statut"], atlas["ratio"], len(atlas["sites_retenus"]),
             atlas["distance_site_proche_km"] or -1.0))


def sommaire():
    d = _totaux(matcher())
    print("Hubs généralisés : %d (trios %d, besoin %.0f t CO2/an)"
          % (d["hubs"], d["trios"], d["besoin_t_an"]))
    print("Hubs avec sites dans le rayon : %d / %d"
          % (d["hubs_matches"], d["hubs"]))
    print("Paires hub-site : %d (cimenteries %d, aciéries BF %d, bois %d)"
          % (d["paires_hub_site"], d["sites_ciment"], d["sites_acier"],
             d["sites_bois"]))
    print("Capacité des sites du rayon : %.0f t CO2/an"
          % d["co2_sites_t_an"])
    print("Médiane des ratios des hubs matchés : %.2f"
          % (d["mediane_ratio_matchs"] or -1.0))
    print("Médiane des distances hub-site : %.1f km"
          % (d["mediane_distance_km"] or -1.0))
    print("Médiane des distances au site le plus proche (217 hubs) : "
          "%.1f km" % (d["mediane_site_proche_km"] or -1.0))
    print("Statuts : %s" % d["statuts"])
    pilote = matcher()["fr-rhone"]
    print("Témoin fr-rhone : %s (ratio %.2f, %d sites, proche %.1f km)"
          % (pilote["statut"], pilote["ratio"],
             len(pilote["sites_retenus"]),
             pilote["distance_site_proche_km"] or -1.0))
    atlas = matcher()["ma-atlas"]
    print("Témoin ma-atlas : %s (ratio %.2f, %d sites, proche %.1f km)"
          % (atlas["statut"], atlas["ratio"],
             len(atlas["sites_retenus"]),
             atlas["distance_site_proche_km"] or -1.0))


def table():
    d = matcher()
    entete = ("%-26s %-11s %5s %5s %6s %5s %8s"
              % ("hub", "statut", "rayon", "sites", "ratio",
                 "trios", "km_proche"))
    print(entete)
    for hid in sorted(d):
        if d[hid]["hub_pilote"]:
            continue
        print("%-26s %-11s %5.0f %5d %6.2f %5d %8.1f"
              % (hid, d[hid]["statut"], d[hid]["rayon_km"],
                 len(d[hid]["sites_retenus"]), d[hid]["ratio"],
                 d[hid]["trios"],
                 d[hid]["distance_site_proche_km"] or -1.0))


def pays(nom):
    d = matcher()
    lignes = [h for h in sorted(d)
              if d[h]["pays"].lower() == nom.lower()]
    for hid in lignes:
        print("%-26s %-11s trio %d — %d sites, ratio %.2f"
              % (hid, d[hid]["statut"], d[hid]["trios"],
                 len(d[hid]["sites_retenus"]), d[hid]["ratio"]))
    if not lignes:
        print("Aucun hub pour le pays « %s »." % nom)


# --------------------------------------------------------------------------
# verifier — doctrine, anti-fuite, reproduction des repères P3
# --------------------------------------------------------------------------

REPÈRES = [
    # (libellé, valeur_repère, tolérance_relative) — repères établis le
    # 14/11/2026 sur le même jeu GEM (md5 vérifié). Les tolérances
    # élargies (paires, cimenteries) couvrent l'écart documenté dans
    # ETAT.md : comptage en lignes/unités vs comptage agrégé, données
    # Global Energy Monitor vivantes (écart déjà constaté : 457 unités
    # BF au lieu de 458).
    ("paires hub-site <100 km", 343, 0.08),
    ("cimenteries matchées", 257, 0.08),
    ("aciéries BF matchées", 13, 0.05),
    ("unités bois matchées", 78, 0.05),
    ("CO2 sites (t/an)", 1372187.0, 0.01),
    ("médiane ratios matchés", 6.0, 0.02),
    ("hubs AUTONOME", 118, 0.02),
    ("hubs COUVERT", 2, 0.5),
    ("hubs PARTIEL", 6, 0.2),
    ("hubs A_SOURCER", 91, 0.02),
    ("médiane site le plus proche (km)", 75.9, 0.01),
]

JETONS_FUITE = ["cout", "€", "prix", "plan_achat", "eur_t", "eur_an",
                "marche_externe", "deficit"]


def verifier():
    detail = matcher()
    totaux = _totaux(detail)
    erreurs = []

    def controle(ok, message):
        print("  %-4s %s" % ("OK" if ok else "ERREUR", message))
        if not ok:
            erreurs.append(message)

    print("— Contrôles doctrine P3 —")
    controle(len(detail) == 219, "219 hubs (217 généralisés + 2 pilotes)")
    gen = [d for d in detail.values() if not d["hub_pilote"]]
    controle(len(gen) == 217, "217 hubs généralisés, pilotes hors totaux")
    controle(sum(d["trios"] for d in gen) == 480, "480 trios généralisés")
    controle(abs(sum(d["besoin_t_an"] for d in gen) - 279360.0) < 1e-6,
             "besoin total 279 360 t/an (480 × 582)")
    controle(detail["fr-rhone"]["hub_pilote"],
             "fr-rhone marqué hub_pilote, hors totaux")
    controle(detail["ma-atlas"]["hub_pilote"],
             "ma-atlas marqué hub_pilote, hors totaux")
    atlas = detail["ma-atlas"]
    controle(atlas["statut"] == "AUTONOME",
             "témoin ma-atlas : AUTONOME (raccord V2.3.1)")
    controle(atlas["rayon_km"] == 50.0
             and len(atlas["sites_retenus"]) == 2
             and all(s["type"] == "ciment" for s in atlas["sites_retenus"]),
             "témoin ma-atlas : 2 cimenteries dans le rayon de 50 km")
    controle(abs(atlas["ratio"] - 5.47) < 0.02,
             "témoin ma-atlas : ratio 5,47 (obtenu %.2f)" % atlas["ratio"])
    controle(atlas["distance_site_proche_km"] is not None
             and abs(atlas["distance_site_proche_km"] - 5.5) < 0.1,
             "témoin ma-atlas : site le plus proche 5,5 km (Meknès)")
    sites_liste = sites()
    controle(len(sites_liste) == 2887 + 457 + 910,
             "sites filtrés : 2 887 cimenteries + 457 unités BF "
             "(409 usines) + 910 unités bois = %d"
             % len(sites_liste))
    iso3_manquants = [s["site"] for s in sites_liste
                      if not s["pays_iso3"]]
    controle(not iso3_manquants,
             "alias pays GEM→ISO 3166-1 alpha-3 renseignés pour tous "
             "les sites (%d manquants)" % len(iso3_manquants))
    controle(all(d["rayon_km"] in (50.0, 100.0) for d in detail.values()),
             "rayons finaux en {50, 100} km")
    controle(all(d["distance_site_proche_km"] is None
                 or d["distance_site_proche_km"] >= 0.0
                 for d in detail.values()),
             "distance au site le plus proche conservée (même hors rayon)")

    print("— Anti-fuite (fichiers publics) —")
    for nom in ("sourcing-p3-public.json", "p3-sites-snapshot.json"):
        chemin = os.path.join(DATA, nom)
        if not os.path.exists(chemin):
            controle(False, "%s absent — lancer generer" % nom)
            continue
        texte = open(chemin, encoding="utf-8").read().lower()
        fuites = [t for t in JETONS_FUITE if t in texte]
        controle(not fuites, "%s sans jeton économique (%s)"
                 % (nom, ", ".join(fuites) or "aucun"))
    chemin_prive = os.path.join(DATA, "sourcing-p3.json")
    controle(os.path.exists(chemin_prive),
             "sourcing-p3.json (PRIVÉ) présent")

    print("— Repères P3 (calibration du 14/11/2026) —")
    valeurs = {
        "paires hub-site <100 km": totaux["paires_hub_site"],
        "cimenteries matchées": totaux["sites_ciment"],
        "aciéries BF matchées": totaux["sites_acier"],
        "unités bois matchées": totaux["sites_bois"],
        "CO2 sites (t/an)": totaux["co2_sites_t_an"],
        "médiane ratios matchés": (totaux["mediane_ratio_matchs"]
                                   or 0.0),
        "hubs AUTONOME": totaux["statuts"].get("AUTONOME", 0),
        "hubs COUVERT": totaux["statuts"].get("COUVERT", 0),
        "hubs PARTIEL": totaux["statuts"].get("PARTIEL", 0),
        "hubs A_SOURCER": totaux["statuts"].get("A_SOURCER", 0),
        "médiane site le plus proche (km)": (
            totaux["mediane_site_proche_km"] or 0.0),
    }
    for libelle, repere, tol in REPÈRES:
        v = valeurs[libelle]
        ecart = abs(v - repere) / max(abs(repere), 1e-9)
        ok = ecart <= tol
        print("  %-4s %-28s obtenu %.4s, repère %s (écart %.2f %%)"
              % ("OK" if ok else "ÉCART", libelle, v, repere,
                 100.0 * ecart))
        if not ok:
            erreurs.append("repère %s" % libelle)

    print("— Coûts privés ILLUSTRATION (jamais versionnés) —")
    cout_gen = sum(d["cout_eur_an"] for d in gen)
    cout_local = sum(d["cout_eur_an"] - d["deficit_marche_t_an"]
                     * PRIX_MARCHE_EXTERNE for d in gen)
    deficit = sum(d["deficit_marche_t_an"] for d in gen)
    print("  Achats sites : %.2f M€/an ; déficit marché externe : "
          "%.0f t/an ; total %.2f M€/an"
          % (cout_local / 1.0e6, deficit, cout_gen / 1.0e6))
    print("  Repère ~8,40 M€/an : ÉCART DOCUMENTÉ dans ETAT.md "
          "(formule du plan d'achat — merit order local + déficit au "
          "marché externe pour tous les hubs, y compris A_SOURCER).")
    pilote = detail["fr-rhone"]
    print("  Témoin fr-rhone : %.0f €/an, %s"
          % (pilote["cout_eur_an"], pilote["statut"]))
    atlas = detail["ma-atlas"]
    print("  Témoin ma-atlas : %.0f €/an, %s"
          % (atlas["cout_eur_an"], atlas["statut"]))

    if erreurs:
        print("\nVERDICT : %d erreur(s)." % len(erreurs))
        for e in erreurs:
            print("  - %s" % e)
        return 1
    print("\nVERDICT : OK.")
    return 0


if __name__ == "__main__":
    commande = sys.argv[1] if len(sys.argv) > 1 else "sommaire"
    if commande == "generer":
        generer()
    elif commande == "sommaire":
        sommaire()
    elif commande == "verifier":
        sys.exit(verifier())
    elif commande == "table":
        table()
    elif commande == "pays":
        if len(sys.argv) < 3:
            print("Usage : pays [PAYS]")
        else:
            pays(sys.argv[2])
    else:
        print("Commandes : generer | sommaire | verifier | table | "
              "pays [PAYS]")
