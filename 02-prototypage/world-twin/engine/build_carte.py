#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère sorties-cartes/carte-world-twin-{public,prive}.html — cartes World Twin.

Sources versionnées :
  data/carte-pays-110m.json       — 177 pays (projection équirectangulaire 960x480)
  data/carte-monde.json           — hubs pilotes, vignobles, locaux, FIRMS, météo, pointage
  data/carte-monde-template.html  — gabarit HTML (jetons __COUNTRIES__ __DATA__ __POINTAGE__ __MODE__ __MODECLASS__)
  data/cao-hubs-public.json       — couche CaO P2.9 publique (statuts, ratios, besoins, capacités)
  data/sourcing-p3-public.json   — couche sourcing P3 publique (statuts, distances, sites retenus)
  data/p3-sites-snapshot.json     — sites industriels Global Energy Monitor (GPS, type)
  engine/sourcing_p3.py hubs()    — positions des 217 hubs généralisés + hubs pilotes (recalcul déterministe)

--mode public : AUCUNE donnée de coût — les fichiers PRIVÉS (cao-hubs.json,
                sourcing-p3.json) ne sont même pas ouverts.
--mode prive  : ajoute les coûts ILLUSTRATION des fichiers PRIVÉS
                (jamais versionnés) ; sortie à usage interne exclusif,
                jamais dans le dépôt (sorties-cartes/ est ignoré par git).

Par défaut : un seul appel Open-Meteo multi-points rafraîchit la météo des 13 clés.
--offline : conserve le pointage figé des données versionnées (build reproductible).
--meteo-hubs : UN appel Open-Meteo multi-points rafraîchit le pointage météo des
               219 hubs (généralisés + pilotes) et l'écrit dans le fichier VERSIONNÉ
               data/meteo-hubs-pointage.json (données météo publiques, aucune donnée
               économique) ; le pointage figé est réinjecté dans chaque build tant
               qu'il n'est pas rafraîchi. Jamais combiné avec --offline.
Contrôles : 177 pays, chaque hub présent dans le HTML, aucun jeton résiduel,
            219 hubs couverts par les couches CaO/P3 (217 généralisés
            + 2 pilotes), et en mode public :
            aucun « cout », « € », « eur_t » ni « eur_an » dans les données injectées.
"""
import argparse
import datetime
import json
import os
import sys
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
OUT = os.path.join(BASE, "sorties-cartes")

MODES = {
    "public": ("pub", "MODE PUBLIC — AUCUN COÛT VERSIONNÉ", "cao-hubs-public.json", "sourcing-p3-public.json"),
    "prive": ("pri", "MODE PRIVÉ — COÛTS ILLUSTRATION · USAGE INTERNE", "cao-hubs.json", "sourcing-p3.json"),
}


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
    url = ( "https://api.open-meteo.com/v1/forecast?latitude=%s&longitude=%s"
           "&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
           % (lats, lons) )
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


def maj_meteo_hubs(monde, hubgps):
    """Pointage Open-Meteo des hubs : UN appel multi-points, fichier versionné.

    Écrit data/meteo-hubs-pointage.json (température, humidité,
    précipitation, vent par hub — données météo publiques, AUCUNE donnée
    économique) puis l'injecte dans monde["meteo_hubs"].
    """
    cles = sorted(hubgps)
    lats = ",".join(str(hubgps[k][0]) for k in cles)
    lons = ",".join(str(hubgps[k][1]) for k in cles)
    url = ("https://api.open-meteo.com/v1/forecast?latitude=%s&longitude=%s"
           "&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
           % (lats, lons))
    rep = None
    for tentative in (1, 2):        # un réessai : poignée de main TLS parfois lente
        try:
            with urllib.request.urlopen(url, timeout=90) as reponse:
                rep = json.load(reponse)
            break
        except Exception:
            if tentative == 2:
                raise
    if isinstance(rep, dict):
        rep = [rep]
    if len(rep) != len(cles):
        raise RuntimeError("réponse Open-Meteo incohérente (%d points)"
                           % len(rep))
    maintenant = datetime.datetime.now(datetime.timezone.utc)
    horodatage = maintenant.strftime("%d/%m/%Y %H:%M UTC")
    pointage = {
        "provenance": {
            "note": ("Pointage météo des hubs World Twin (Open-Meteo, "
                     "réel — vague P1). Données météo publiques, aucune "
                     "donnée économique. Versionné dans data/."),
            "etiquette_simulation": "SYNTHÉTIQUE",
        },
        "pointage": horodatage + " (Open-Meteo, réel)",
        "hubs": {},
    }
    for cle, entree in zip(cles, rep):
        actuel = entree["current"]
        pointage["hubs"][cle] = {
            "t": round(float(actuel["temperature_2m"]), 1),
            "h": int(round(float(actuel["relative_humidity_2m"]))),
            "p": round(float(actuel["precipitation"]), 1),
            "v": round(float(actuel["wind_speed_10m"]), 1),
            "heure": horodatage,
        }
    with open(os.path.join(DATA, "meteo-hubs-pointage.json"), "w",
              encoding="utf-8") as f:
        json.dump(pointage, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    monde["meteo_hubs"] = pointage
    return len(pointage["hubs"])


def construire_couches(mode):
    """Couches CaO P2.9 + sourcing P3 + sites + positions des hubs (recalcul déterministe)."""
    _, _, cao_f, p3_f = MODES[mode]
    with open(os.path.join(DATA, cao_f), encoding="utf-8") as f:
        cao = json.load(f)
    with open(os.path.join(DATA, p3_f), encoding="utf-8") as f:
        p3 = json.load(f)
    with open(os.path.join(DATA, "p3-sites-snapshot.json"), encoding="utf-8") as f:
        sites = json.load(f)

    sys.path.insert(0, os.path.join(BASE, "engine"))
    import sourcing_p3                                   # noqa: E402 (engine/)
    gps = sourcing_p3.hubs()
    hubgps = {hid: [round(h["lat"], 2), round(h["lon"], 2)] for hid, h in gps.items()}

    # V2.5 : sites de transformation post-récolte (type de site, captabilité,
    # énergie du site, LPI 2023 par pays) — 219 fiches, aucune coordonnée.
    import sites_transformation                          # noqa: E402 (engine/)
    couches_sites = sites_transformation.couches()

    prive = mode == "prive"
    couches_cao = {}
    for hid, h in cao["hubs"].items():
        entree = {
            "pays": h["pays"], "trios": h["trios"], "statut": h["statut"],
            "ratio": round(h["ratio"], 2),
            "besoin_t_an": h["besoin_t_an"],
            "capacite_t_an": round(h["capacite_t_an"]),
        }
        if prive:
            entree["cout_eur_an"] = round(h.get("cout_eur_an", 0.0))
            entree["cout_eur_t"] = round(h.get("cout_eur_t", 0.0), 1)
        couches_cao[hid] = entree

    couches_p3 = {}
    for hid, h in p3["hubs"].items():
        retenus = h.get("sites_retenus") or []
        entree = {
            "pays": h["pays"], "statut": h["statut"],
            "ratio": round(h["ratio"], 2),
            "distance_site_proche_km": round(h["distance_site_proche_km"], 1),
            "rayon_km": h["rayon_km"],
            "nb_sites": len(retenus),
            "capacite_rayon_t_an": round(h["capacite_rayon_t_an"]),
        }
        if prive:
            entree["cout_eur_an"] = round(h.get("cout_eur_an", 0.0))
            entree["cout_eur_t"] = round(h.get("cout_eur_t", 0.0), 1)
            deficit = h.get("deficit_marche_t_an") or 0.0
            if deficit:
                entree["deficit_marche_t_an"] = round(deficit)
        couches_p3[hid] = entree

    p3sites = [{"lat": s["lat"], "lon": s["lon"], "type": s["type"]}
               for s in sites["sites"].values()]
    return hubgps, couches_cao, couches_p3, p3sites, couches_sites


def verifier(pays, monde, html, mode, data_json):
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
    for jeton in ("__COUNTRIES__", "__DATA__", "__POINTAGE__", "__MODE__", "__MODECLASS__"):
        if jeton in html:
            raise RuntimeError("jeton résiduel : %s" % jeton)
    nb_cao = len(monde.get("cao", {}))
    nb_p3 = len(monde.get("p3", {}))
    if nb_cao != 219 or nb_p3 != 219:
        raise RuntimeError("couches CaO/P3 incomplètes : %d/%d hubs (attendu 219/219)"
                           % (nb_cao, nb_p3))
    for hid in ("fr-rhone", "ma-atlas", "gen-maroc-1"):
        if hid not in monde.get("hubgps", {}):
            raise RuntimeError("hub sans GPS recalculé : %s" % hid)
        if hid not in html:
            raise RuntimeError("hub généralisé absent du HTML généré : %s" % hid)
    if "p3sites" not in monde or not monde["p3sites"]:
        raise RuntimeError("couche sites P3 vide")
    nb_sites = len(monde.get("sites", {}))
    if nb_sites != nb_p3:
        raise RuntimeError("couche sites de transformation incomplète : %d fiches "
                           "(attendu %d, comme CaO/P3)" % (nb_sites, nb_p3))
    for hid in ("fr-rhone", "ma-atlas", "gen-cote-d-ivoire-2"):
        fiche = monde.get("sites", {}).get(hid)
        if not fiche or not fiche.get("type_site"):
            raise RuntimeError("fiche site absente ou vide : %s" % hid)
    mh = monde.get("meteo_hubs")
    if mh is not None:
        nb_mh = len(mh.get("hubs", {}))
        if nb_mh != len(monde.get("hubgps", {})):
            raise RuntimeError("pointage météo hubs incomplet : %d hubs "
                               "pointés / %d attendus"
                               % (nb_mh, len(monde.get("hubgps", {}))))
    if mode == "public":
        couches_json = json.dumps({"cao": monde.get("cao", {}), "p3": monde.get("p3", {}),
                                   "sites": monde.get("sites", {})},
                                  ensure_ascii=False, separators=(",", ":"))
        for indice in ("cout", "€", "eur_t", "eur_an"):
            if indice in couches_json:
                raise RuntimeError("fuite de coût en mode public (couches CaO/P3) : indice « %s »" % indice)


def main():
    analyse = argparse.ArgumentParser(description="Générateur des cartes World Twin (HTML autonome)")
    analyse.add_argument("--mode", choices=sorted(MODES), default="public",
                         help="public : aucune donnée de coût ; prive : coûts ILLUSTRATION (usage interne)")
    analyse.add_argument("--offline", action="store_true",
                         help="météo figée des données versionnées (aucun appel réseau)")
    analyse.add_argument("--meteo-hubs", action="store_true",
                         help="rafraîchit le pointage météo des 219 hubs (UN appel "
                              "Open-Meteo multi-points, fichier versionné "
                              "data/meteo-hubs-pointage.json)")
    args = analyse.parse_args()
    classe, libelle, _, _ = MODES[args.mode]
    pays, monde, gabarit = charger()
    hubgps, couches_cao, couches_p3, p3sites, couches_sites = construire_couches(args.mode)
    monde["hubgps"] = hubgps
    monde["cao"] = couches_cao
    monde["p3"] = couches_p3
    monde["p3sites"] = p3sites
    monde["sites"] = couches_sites
    monde["mode"] = args.mode
    chemin_meteo_hubs = os.path.join(DATA, "meteo-hubs-pointage.json")
    if args.meteo_hubs and not args.offline:
        try:
            nb = maj_meteo_hubs(monde, hubgps)
            print("pointage météo hubs rafraîchi : data/meteo-hubs-pointage.json "
                  "(%d hubs, %s)" % (nb, monde["meteo_hubs"]["pointage"]))
        except Exception as exc:
            print("pointage météo hubs indisponible (%s) — pointage figé "
                  "conservé" % exc)
    if "meteo_hubs" not in monde and os.path.exists(chemin_meteo_hubs):
        with open(chemin_meteo_hubs, encoding="utf-8") as f:
            monde["meteo_hubs"] = json.load(f)
    if not args.offline:
        try:
            maj_meteo_live(monde)
        except Exception as exc:
            print("météo live indisponible (%s) — pointage figé conservé" % exc)
    os.makedirs(OUT, exist_ok=True)
    data_json = json.dumps(monde, ensure_ascii=False, separators=(",", ":"))
    html = gabarit.replace("__COUNTRIES__", json.dumps(pays, ensure_ascii=False, separators=(",", ":")))
    html = html.replace("__DATA__", data_json)
    html = html.replace("__POINTAGE__", "le " + monde["pointage"].split(" (")[0])
    html = html.replace("__MODECLASS__", classe)
    html = html.replace("__MODE__", libelle)
    verifier(pays, monde, html, args.mode, data_json)
    cible = os.path.join(OUT, "carte-world-twin-%s.html" % args.mode)
    with open(cible, "w", encoding="utf-8") as f:
        f.write(html)
    print("carte générée : %s (%d octets, mode %s, pointage %s)"
          % (cible, os.path.getsize(cible), args.mode, monde["pointage"]))


if __name__ == "__main__":
    main()
