#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Relevé quotidien FIRMS VIIRS NOAA-20 NRT sur les 10 bassins World Twin.

Capteur : VIIRS_NOAA20_NRT (satellite NOAA-20). Correctif du 19/10/2026 :
la NASA FIRMS cesse la livraison Suomi NPP le 01/11/2026, NOAA-20 est la
mission de référence qui poursuit la série VIIRS (page /api/area/ FIRMS).

Écrit sorties-firms-nrt/firms-nrt.csv et resume.md (jamais versionnés).
API : firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/VIIRS_NOAA20_NRT/{W},{S},{E},{N}/1/{date}
Boîte : ±1.0° latitude / ±1.5° longitude autour du GPS du bassin.
Sans FIRMS_MAP_KEY (ou en cas d'échec API) : repli propre — zéros étiquetés
SYNTHÉTIQUE, le workflow reste vert et l'écart est visible dans le résumé.

V1.4 (22/10/2026) : chaque relevé alimente la chaîne FRP → FRE → biomasse →
émissions (engine/fre_conversions.py) — FRE extrapolée sur la journée,
biomasse via le coefficient 0,368 kg/MJ (Wooster et al. 2005), émissions via
les facteurs IPCC 2006 Vol. 4 Tab. 2.5 (résidus agricoles). Toutes les
valeurs dérivées sont des ESTIMATIONS DOCUMENTAIRES ILLUSTRATION : jamais
calibrées, jamais une donnée de qualification, jamais sur le registre Merkle
de production.
"""
import csv
import datetime
import io
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fre_conversions

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "sorties-firms-nrt")

BASSINS = [
    ("vallée-du-rhone", 44.5, 4.8),
    ("camargue", 43.6, 4.5),
    ("périgord", 45.0, 0.8),
    ("sud-ouest", 44.2, -0.7),
    ("suisse-leman", 46.4, 6.5),
    ("italie-puglia", 41.5, 15.5),
    ("espagne-extremadure", 38.9, -6.5),
    ("argentine-cuyo", -33.0, -68.5),
    ("argentine-misiones", -27.5, -55.5),
    ("maroc-atlas", 33.8, -5.3),
]


def relever(cle_api, lat, lon, date_utc):
    ouest = "%.4f" % (lon - 1.5)
    sud = "%.4f" % (lat - 1.0)
    est = "%.4f" % (lon + 1.5)
    nord = "%.4f" % (lat + 1.0)
    url = ("https://firms.modaps.eosdis.nasa.gov/api/area/csv/%s/VIIRS_NOAA20_NRT/"
           "%s,%s,%s,%s/1/%s" % (cle_api, ouest, sud, est, nord, date_utc))
    with urllib.request.urlopen(url, timeout=30) as reponse:
        texte = reponse.read().decode("utf-8")
    lignes = list(csv.DictReader(io.StringIO(texte)))
    frp = 0.0
    for ligne in lignes:
        try:
            frp += float(ligne.get("frp") or 0.0)
        except (TypeError, ValueError):
            pass
    return len(lignes), round(frp, 1)


def fr(n):
    return ("%s" % n).replace(".", ",")


def main():
    os.makedirs(OUT, exist_ok=True)
    cle_api = os.environ.get("FIRMS_MAP_KEY", "").strip()
    maintenant = datetime.datetime.now(datetime.timezone.utc)
    date_utc = maintenant.strftime("%Y-%m-%d")
    lignes = []
    for bassin, lat, lon in BASSINS:
        if cle_api:
            try:
                detections, frp = relever(cle_api, lat, lon, date_utc)
                lignes.append((bassin, lat, lon, detections, frp, "RÉEL (FIRMS NOAA-20 NRT)"))
                continue
            except Exception as exc:
                print("échec API %s : %s — repli SYNTHÉTIQUE" % (bassin, exc))
        lignes.append((bassin, lat, lon, 0, 0.0,
                       "SYNTHÉTIQUE (sans clé)" if not cle_api else "SYNTHÉTIQUE (échec API)"))
    with open(os.path.join(OUT, "firms-nrt.csv"), "w", encoding="utf-8", newline="") as f:
        ecrivain = csv.writer(f)
        ecrivain.writerow(["bassin", "latitude", "longitude", "detections", "frp_mw",
                           "fre_mj", "biomasse_t", "co2_t", "ch4_t", "n2o_t",
                           "co2e_nonco2_t", "source", "date_utc"])
        for bassin, lat, lon, det, frp, src in lignes:
            chaine = fre_conversions.chaine(frp, 24.0)
            ecrivain.writerow([bassin, lat, lon, det, frp,
                               chaine["fre_mj"], chaine["biomasse_t"],
                               chaine["emissions"]["co2"], chaine["emissions"]["ch4"],
                               chaine["emissions"]["n2o"], chaine["emissions"]["co2e_nonco2_t"],
                               src, date_utc])
    total_det = sum(l[3] for l in lignes)
    total_frp = round(sum(l[4] for l in lignes), 1)
    reels = sum(1 for l in lignes if l[5].startswith("RÉEL"))
    resume = []
    resume.append("# Relevé FIRMS VIIRS NOAA-20 NRT — %s" % maintenant.strftime("%d/%m/%Y %H:%M UTC"))
    resume.append("")
    resume.append("10 bassins World Twin (boîte ±1.0° lat / ±1.5° lon autour du GPS du bassin), "
                  "source VIIRS_NOAA20_NRT (NOAA-20), journée %s." % date_utc)
    resume.append("")
    resume.append("| bassin | détections | FRP (MW) | FRE 24 h (MJ) | biomasse (t MS) | CO2e non-CO2 (t) | source |")
    resume.append("| --- | --- | --- | --- | --- | --- | --- |")
    tot_fre = 0.0
    tot_bio = 0.0
    tot_co2e = 0.0
    for bassin, lat, lon, det, frp, src in lignes:
        chaine = fre_conversions.chaine(frp, 24.0)
        tot_fre += chaine["fre_mj"]
        tot_bio += chaine["biomasse_t"]
        tot_co2e += chaine["emissions"]["co2e_nonco2_t"]
        resume.append("| %s | %d | %s | %s | %s | %s | %s |" % (
            bassin, det, fr(frp), fr(round(chaine["fre_mj"])), fr(round(chaine["biomasse_t"], 1)),
            fr(round(chaine["emissions"]["co2e_nonco2_t"], 2)), src))
    resume.append("")
    resume.append("Total : %d détections, %s MW — %d/10 bassins en données réelles." % (total_det, fr(total_frp), reels))
    resume.append("")
    resume.append("## Chaîne FRP → FRE → biomasse → émissions (v1.4, ESTIMATIONS ILLUSTRATION)")
    resume.append("")
    resume.append("FRE extrapolée sur 24 h : %s MJ — biomasse sèche consommée estimée : %s t "
                  "(fourchette coeff 0,368–0,453 kg/MJ) — CO2e non-CO2 émis : %s t équivalent."
                  % (fr(round(tot_fre)), fr(round(tot_bio)), fr(round(tot_co2e, 1))))
    resume.append("Lecture World Ops : la biomasse partie en fumée ce jour sur les dix bassins est "
                  "autant de matière première perdue pour les trios — l'équivalent CO2 est l'argument "
                  "techfin de la conversion en biochar. Valeurs ILLUSTRATION, jamais calibrées.")
    resume.append("")
    resume.append("Méthode : FRP × 86 400 s = FRE (extrapolation à combustion constante, ~2 passages/jour) ; "
                  "× 0,368 kg/MJ = biomasse (Wooster et al. 2005) ; facteurs IPCC 2006 Vol. 4 Tab. 2.5 "
                  "(résidus agricoles) ; GWP AR6 (CH4 27,0, N2O 273). Limites : incertitude ~ facteur 2, "
                  "feux < 375 m sous-détectés, nuages et panaches masquent.")
    resume.append("")
    if reels < len(BASSINS):
        resume.append("REPLI : %d bassin(s) SYNTHÉTIQUE — créer le secret FIRMS_MAP_KEY "
                      "(Settings > Secrets and variables > Actions > New repository secret). "
                      "Clé gratuite : firms.modaps.eosdis.nasa.gov/api/map_key/"
                      % (len(BASSINS) - reels))
    resume.append("")
    resume.append("Doctrine : données brutes NASA, relevé jamais versionné, diffusion interne uniquement.")
    with open(os.path.join(OUT, "resume.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(resume) + "\n")
    print("relevé FIRMS NOAA-20 écrit : %s (%d/10 bassins réels)" % (OUT, reels))


if __name__ == "__main__":
    main()

