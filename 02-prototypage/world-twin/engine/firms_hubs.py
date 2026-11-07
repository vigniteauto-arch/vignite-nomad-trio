#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Couche FIRMS des hubs généralisés — boîtes des 81 hubs (V1.7, 31/10/2026).

Jusqu'à la V1.6, seuls les 10 bassins P2 portaient une boîte FIRMS
(engine/firms.py, BOITES_BASSINS) : les hubs généralisés de la flotte
étoffée retombaient sur le repli synthétique. La V1.7 donne à chacun
des 81 hubs sa boîte de surveillance, dérivée de son centre GPS —
exactement la même géométrie que le relevé quotidien : ±1.0° latitude /
±1.5° longitude autour du centre du cluster (firms_nrt.py).

COUVERTURE — 91 ZONES :
- 10 bassins P2 (BOITES_BASSINS, inchangés) ;
- 81 hubs généralisés (centres des clusters V1.6, déterministes) ;
- aucune clé, aucune requête réseau ici : ce module ne fait que
  CONSTRUIRE et VÉRIFIER les boîtes.

RÈGLES :
- Les centres sont ceux du clustering V1.6 (déterministes : mêmes
  atlas, mêmes clusters, mêmes boîtes — reproductible au degré près).
- La géométrie de boîte est ILLUSTRATION, comme celle des bassins :
  elle cadre la zone de pain point du hub, pas son gisement complet.
- Des boîtes voisines peuvent se CHEVAUCHER (deux hubs mutualisés à
  moins de ~250 km) : une même détection peut alors compter dans les
  deux zones. Doctrine : le relevé mesure l'intensité du pain point
  PAR ZONE, jamais un total mondial sans double compte.
- Aucune valeur calibrée, aucun paramètre VDE, aucune clé (doctrine PI).

Lancement (bibliothèque standard uniquement) :

    python3 firms_hubs.py sommaire     # composition des 91 zones
    python3 firms_hubs.py fiche ZONE   # boîte d'une zone (bassin ou hub)
    python3 firms_hubs.py croiser      # gardes de couverture et cohérence
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import firms
import flotte_monde

DEMI_LAT = 1.0    # ±1.0° latitude — même géométrie que firms_nrt.py
DEMI_LON = 1.5     # ±1.5° longitude — même géométrie que firms_nrt.py

_memoire_zones = None
_memoire_boites = None


def boites_hubs():
    """Boîtes des 81 hubs généralisés : {hub_id: {lat, lon, pays, boite}}.

    La boite est (ouest, sud, est, nord), même convention que
    firms.BOITES_BASSINS. Centres issus du clustering V1.6 —
    déterministes, jamais saisis à la main.
    """
    global _memoire_boites
    if _memoire_boites is not None:
        return _memoire_boites
    hubs, _, _ = flotte_monde.hubs_generalises()
    boites = {}
    for hid, hub in hubs.items():
        lat, lon = hub["_meta"]["centre"]
        boites[hid] = {
            "pays": hub["pays"],
            "lat": lat,
            "lon": lon,
            "boite": (round(lon - DEMI_LON, 2), round(lat - DEMI_LAT, 2),
                      round(lon + DEMI_LON, 2), round(lat + DEMI_LAT, 2)),
            "type": "hub généralisé",
        }
    _memoire_boites = boites
    return boites


def zones_firms():
    """Les 91 zones de surveillance : 10 bassins P2 + 81 hubs.

    Retourne {zone: fiche} où fiche porte pays, lat, lon, boite
    (ouest, sud, est, nord), type (« bassin P2 » ou « hub généralisé »).
    Les bassins P2 gardent leurs centres historiques de firms_nrt.py
    (GPS de référence des bassins, inchangés depuis la V1.4).
    """
    global _memoire_zones
    if _memoire_zones is not None:
        return _memoire_zones
    centres_bassins = {
        # GPS de référence des bassins P2 (firms_nrt.py, V1.4 — inchangés).
        "vallee-du-rhone":       (44.5, 4.8),
        "camargue":              (43.6, 4.5),
        "perigord":              (45.0, 0.8),
        "sud-ouest":             (44.2, -0.7),
        "suisse-leman":          (46.4, 6.5),
        "italie-puglia":         (41.5, 15.5),
        "espagne-extremadure":   (38.9, -6.5),
        "argentine-cuyo":        (-33.0, -68.5),
        "argentine-misiones":    (-27.5, -55.5),
        "maroc-atlas":           (33.8, -5.3),
    }
    zones = {}
    for bassin, boite in firms.BOITES_BASSINS.items():
        lat, lon = centres_bassins[bassin]
        zones[bassin] = {
            "pays": "bassin P2",
            "lat": lat,
            "lon": lon,
            "boite": boite,
            "type": "bassin P2",
        }
    for hid, fiche in boites_hubs().items():
        zones[hid] = fiche
    _memoire_zones = zones
    return zones


# ---------------------------------------------------------------------------
# Gardes de cohérence
# ---------------------------------------------------------------------------

def verifier():
    """Gardes : 91 zones exactement, unicité, boîtes valides, couverture.

    Un écart est une ATTENTION affichée — jamais une valeur cachée.
    """
    ecarts = []
    zones = zones_firms()
    if len(zones) != len(firms.BOITES_BASSINS) + len(boites_hubs()):
        ecarts.append("zones %d != bassins %d + hubs %d"
                      % (len(zones), len(firms.BOITES_BASSINS),
                         len(boites_hubs())))
    for zone, fiche in zones.items():
        ouest, sud, est, nord = fiche["boite"]
        if not (-180.0 <= ouest < est <= 180.0):
            ecarts.append("longitude invalide : %s" % zone)
        if not (-90.0 <= sud < nord <= 90.0):
            ecarts.append("latitude invalide : %s" % zone)
        if not -90.0 <= fiche["lat"] <= 90.0 or not -180.0 <= fiche["lon"] <= 180.0:
            ecarts.append("centre GPS hors monde : %s" % zone)
    # couverture : chaque hub de la flotte a sa zone, chaque zone hub
    # correspond à un hub de la flotte.
    hubs, _, _ = flotte_monde.hubs_generalises()
    for hid in hubs:
        if hid not in zones:
            ecarts.append("hub sans boîte : %s" % hid)
    for zone in zones:
        if zone not in firms.BOITES_BASSINS and zone not in hubs:
            ecarts.append("zone sans hub ni bassin : %s" % zone)
    return ecarts


def sommaire():
    zones = zones_firms()
    hubs = boites_hubs()
    pays = sorted({f["pays"] for f in hubs.values()})
    lignes = [
        "Boîtes FIRMS des hubs World Twin (V1.7) — %d zones de surveillance" % len(zones),
        "",
        "- Bassins P2 : %d (boîtes inchangées, firms.py)" % len(firms.BOITES_BASSINS),
        "- Hubs généralisés : %d sur %d pays (centres V1.6, géométrie ±1.0° lat / ±1.5° lon)"
        % (len(hubs), len(pays)),
        "- Total : %d zones — %d requêtes FIRMS par relevé quotidien "
        "(limite NASA : 5 000 transactions / 10 min, consommation : 91/jour)"
        % (len(zones), len(zones)),
        "- Déterminisme : boîtes dérivées des clusters V1.6, jamais saisies à la main",
        "",
        "Commandes : sommaire | fiche ZONE | croiser",
    ]
    return "\n".join(lignes) + "\n"


def fiche(zone):
    zones = zones_firms()
    if zone not in zones:
        print("ERREUR : zone inconnue « %s ». Zones : %s"
              % (zone, ", ".join(sorted(zones))))
        return 1
    f = zones[zone]
    ouest, sud, est, nord = f["boite"]
    print("Zone : %s (%s)" % (zone, f["type"]))
    print("Centre GPS : %.2f / %.2f — pays : %s" % (f["lat"], f["lon"], f["pays"]))
    print("Boîte (ouest, sud, est, nord) : %s, %s, %s, %s"
          % (ouest, sud, est, nord))
    print("Format API FIRMS : %s,%s,%s,%s" % (ouest, sud, est, nord))
    return 0


def main():
    arguments = sys.argv[1:]
    if not arguments or arguments[0] == "sommaire":
        for ecart in verifier():
            print("ATTENTION : %s" % ecart)
        print(sommaire())
        return 0
    if arguments[0] == "fiche":
        return fiche(arguments[1]) if len(arguments) > 1 else 1
    if arguments[0] == "croiser":
        ecarts = verifier()
        if ecarts:
            for ecart in ecarts:
                print("ATTENTION : %s" % ecart)
            return 1
        zones = zones_firms()
        print("Croisement OK : %d zones (%d bassins P2 + %d hubs), "
              "couverture flotte complète, boîtes valides."
              % (len(zones), len(firms.BOITES_BASSINS),
                 len(zones) - len(firms.BOITES_BASSINS)))
        return 0
    print("Commande inconnue : %s (sommaire | fiche ZONE | croiser)" % arguments[0])
    return 1


if __name__ == "__main__":
    sys.exit(main())
