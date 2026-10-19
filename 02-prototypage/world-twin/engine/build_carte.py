#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère sorties-cartes/carte-world-twin.html — carte publique World Twin.

Sources versionnées :
  data/carte-pays-110m.json      — 177 pays (projection équirectangulaire 960x480)
  data/carte-monde.json          — hubs, vignobles, locaux, FIRMS, météo, pointage
  data/carte-monde-template.html — gabarit HTML (jetons __COUNTRIES__ __DATA__ __POINTAGE__)

Par défaut : un seul appel Open-Meteo multi-points rafraîchit la météo des 13 clés.
--offline : conserve le pointage figé des données versionnées (build reproductible).
Contrôles : 177 pays, chaque hub présent dans le HTML, aucun jeton résiduel.
"""
import argparse
import datetime
import json
import os
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
OUT = os.path.join(BASE, "sorties-cartes")


def charger():
    with open(os.path.join(DATA, "carte-pays-110m.json"), encoding="utf-8") as f:
        pays = json.load(f)
    with open(os.path.join(DATA, "carte-monde.json"), encoding="utf-8") as f:
        monde = json.load(f)
    with open(os.path.join(DATA, "carte-monde-template.html"), encoding="utf-8") as f:
        gabarit = f.read()
    return pays, monde, gabarit


def cle_gps(monde):
    """Résolution GPS des clés météo : hubs par id, vignobles/locaux par iso, US_MARC -> US."""
    cles = {}
    for h in monde.get("hubs", []):
        cles[h["id"]] = h["gps"]
    for v in monde.get("vin", []):
        cles.setdefault(v["iso"], v["gps"])
    for l in monde.get("loc", []):
        cles.setdefault(l["iso"], l["gps"])
    if "US_MARC" not in cles:
        cles["US_MARC"] = cles.get("US", [37.64, -120.99])
    return cles


def maj_meteo_live(monde):
    cles = list(monde["meteo"].keys())
    cg = cle_gps(monde)
    manquantes = [k for k in cles if k not in cg]
    if manquantes:
        raise RuntimeError("clés météo sans GPS : %s" % ", ".join(manquantes))
    lats = ",".join(str(cg[k][0]) for k in cles)
    lons = ",".join(str(cg[k][1]) for k in cles)
    url = ("https://api.open-meteo.com/v1/forecast?latitude=%s&longitude=%s"
           "&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
           % (lats, lons))
    with urllib.request.urlopen(url, timeout=25) as reponse:
        rep = json.load(reponse)
    if isinstance(rep, dict):
        rep = [rep]
    if len(rep) != len(cles):
        raise RuntimeError("réponse Open-Meteo incohérente (%d points)" % len(rep))
    maintenant = datetime.datetime.now(datetime.timezone.utc)
    horodatage = maintenant.strftime("%d/%m/%Y %H:%M UTC")
    for cle, entree in zip(cles, rep):
        actuel = entree["current"]
        monde["meteo"][cle] = {
            "t": round(float(actuel["temperature_2m"]), 1),
            "h": int(round(float(actuel["relative_humidity_2m"]))),
            "p": round(float(actuel["precipitation"]), 1),
            "v": round(float(actuel["wind_speed_10m"]), 1),
            "heure": horodatage,
        }
    monde["pointage"] = horodatage + " (Open-Meteo, réel)"


def verifier(pays, monde, html):
    if len(pays) != 177:
        raise RuntimeError("carte-pays-110m.json : %d pays (attendu 177)" % len(pays))
    ids = [h["id"] for h in monde.get("hubs", [])]
    attendus = ["fr-rhone", "ch-leman", "it-puglia", "es-extremadura",
                "ar-cuyo", "ar-misiones", "ma-atlas"]
    for ident in attendus:
        if ident not in ids:
            raise RuntimeError("hub absent des données : %s" % ident)
        if ident not in html:
            raise RuntimeError("hub absent du HTML généré : %s" % ident)
    for jeton in ("__COUNTRIES__", "__DATA__", "__POINTAGE__"):
        if jeton in html:
            raise RuntimeError("jeton résiduel : %s" % jeton)


def main():
    analyse = argparse.ArgumentParser(description="Générateur de la carte World Twin (HTML autonome)")
    analyse.add_argument("--offline", action="store_true",
                         help="météo figée des données versionnées (aucun appel réseau)")
    args = analyse.parse_args()
    pays, monde, gabarit = charger()
    if not args.offline:
        try:
            maj_meteo_live(monde)
        except Exception as exc:
            print("météo live indisponible (%s) — pointage figé conservé" % exc)
    os.makedirs(OUT, exist_ok=True)
    html = gabarit.replace("__COUNTRIES__", json.dumps(pays, ensure_ascii=False, separators=(",", ":")))
    html = html.replace("__DATA__", json.dumps(monde, ensure_ascii=False, separators=(",", ":")))
    html = html.replace("__POINTAGE__", "le " + monde["pointage"].split(" (")[0])
    verifier(pays, monde, html)
    cible = os.path.join(OUT, "carte-world-twin.html")
    with open(cible, "w", encoding="utf-8") as f:
        f.write(html)
    print("carte générée : %s (%d octets, pointage %s)" % (cible, os.path.getsize(cible), monde["pointage"]))


if __name__ == "__main__":
    main()
