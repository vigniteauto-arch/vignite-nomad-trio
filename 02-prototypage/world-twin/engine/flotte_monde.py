#!/usr/bin/env python3
"""Couche P2.7 — flotte généralisée « as if in operation » (V1.8, 31/10/2026).

Fait tourner le trio Nomad v1 en simulation sur TOUS les points des
atlas versionnés (v1.0 : 52 intrants du master, v1.1 : 67 intrants
locaux par pays, v1.2 : 32 intrants viticoles) : les points candidats
sont clusterés en hubs généralisés par pays et par proximité
géographique, chaque hub reçoit sa flotte de trios et ses équipes
d'opérateurs selon le figeage acté du 27/10/2026, puis le simulateur
v0.5 y fait tourner une année SYNTHÉTIQUE.

Figeage acté (27/10/2026, « go » de Manu) :
- MTBF 720 h, MTTR 8 h (baseline inchangée, série historique comparable) ;
- M1 : MTTR en mélange 80 % mineur 4 h / 20 % majeur 24 h + délai de
  réponse +2 h — variante Monte Carlo ;
- M2 : commissioning MTBF 240 h sur les 500 premières heures d'un trio
  neuf — variante Monte Carlo ;
- M3 : MTTR × 1,5 quand le ratio opérateurs/trio franchit le plafond —
  variante Monte Carlo ;
- OPÉRATEURS : 2 opérateurs tournants couvrent jusqu'à 5 trios par hub
  (doctrine IoT assistée — présence 4 h/jour, alarmes, télémétrie Edge) ;
  le sixième trio impose une seconde équipe. La concurrence de pannes
  ne dimensionne rien (P(>=2 trios en panne) < 0,2 % à n=5).

RÈGLES :
- Étiquette SYNTHÉTIQUE — registre de développement, jamais production.
- Aucune valeur calibrée, aucun paramètre VDE, aucune clé (doctrine PI).
- V1.8 (31/10/2026) — pain points réels par hub : chaque hub enregistre
  sa zone GPS (boîte ±1.0° latitude / ±1.5° longitude autour du centre
  du cluster) dans le registre de engine/firms.py au moment de sa
  construction. Avec une MAP_KEY locale (firms.env ou FIRMS_MAP_KEY),
  les pain points du hub deviennent des feux RÉELS NASA FIRMS du jour.
  Sans clé : repli synthétique propre, inchangé. Les tirages du moteur
  sont alignés (scenario v0.6) : les KPI restent identiques avec ou
  sans clé.
- Les gisements, réglementations et volumes restent ceux des atlas, avec
  leurs étiquettes SOURCÉ / ILLUSTRATION / À VÉRIFIER d'origine.
- La capacité d'un trio n'est PAS calibrée : depuis la v1.7, le
  dimensionnement des flottes (trios par hub) suit le gisement FAOSTAT
  du mix d'intrants du hub (couche gisements_hubs, fenêtre 2020-2024,
  somme des milieux de fourchette des points sourcés) par paliers
  ILLUSTRATION. La part récoltable et la décomposition régionale
  addressable restent À SOURCER (P3) : le proxy national est documenté
  dans chaque fiche d'atlas (« brut national »).

Lancement (bibliothèque standard uniquement) :

    python3 flotte_monde.py sommaire            # composition de la flotte
    python3 flotte_monde.py flotte              # table des hubs, trios, ops
    python3 flotte_monde.py run                 # une année simulée, tous hubs
    python3 flotte_monde.py run gen-bresil-1    # un hub généralisé précis
    python3 flotte_monde.py monte-carlo 50       # 50 graines sur tous les hubs

Sorties dans ../sorties/ (jamais versionnées) :
    flotte-generale-composition.json — composition (hubs, trios, ops)
    flotte-generale-run.json / .md  — run d'une année (KPI par hub)
    flotte-generale-mc.json         — agrégats Monte Carlo
"""

import json
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import atlas_biomasses_monde
import atlas_biomasses_pays
import atlas_vignobles_monde
import firms
import gisements_hubs
import monde
import simulateur

ETIQUETTE = "SYNTHÉTIQUE"
RAYON_CLUSTER_KM = 300.0   # ILLUSTRATION : rayon de mutualisation d'un hub
TRIOS_MAX_PAR_HUB = 5      # figé : plafond de couverture d'une équipe
EQUIPE_OPERATEURS = 2      # figé : 2 opérateurs tournants par équipe

# Humidités ILLUSTRATION par famille (jamais calibrées).
HUMIDITES_FAMILLES = {
    "Céréales": (10.0, 28.0),
    "Cultures pérennes": (30.0, 55.0),
    "Racines & tubercules": (15.0, 40.0),
    "Maraîcher": (40.0, 70.0),
    "Oléagineux": (8.0, 20.0),
    "Légumineuses": (12.0, 30.0),
}
HUMIDITE_DEFAUT = (20.0, 50.0)


# ---------------------------------------------------------------------------
# Collecte des points des atlas versionnés
# ---------------------------------------------------------------------------

def _collecte_points():
    """Tous les points d'intrants des atlas v1.0/v1.1/v1.2.

    Les points rattachés aux 7 hubs de la flotte P2 (hubs_flotte non
    vide) sont exclus : ils tournent déjà dans le simulateur monde.
    """
    points = []
    exclus = []

    def ajouter(fiche, source):
        if not isinstance(fiche, dict) or "lat" not in fiche or "lon" not in fiche:
            return
        point = {
            "token": fiche.get("token"),
            "pays": fiche.get("pays") or fiche.get("pays_courant"),
            "region": fiche.get("region", ""),
            "lat": float(fiche["lat"]),
            "lon": float(fiche["lon"]),
            "famille": fiche.get("famille", ""),
            "nom_fr": fiche.get("nom_fr", ""),
            "fenetre": list(fiche.get("fenetre", [])),
            "gisement": fiche.get("gisement", ""),
            "etiquette_gisement": fiche.get("etiquette_gisement", ""),
            "source_atlas": source,
        }
        if point["token"] is None or not point["pays"] or not point["fenetre"]:
            return
        (exclus if fiche.get("hubs_flotte") else points).append(point)

    # v1.0 — master (52 intrants, fiches à clé token)
    for token, fiche in atlas_biomasses_monde.ATLAS_BIOMASSES_MONDE.items():
        copie = dict(fiche)
        copie["token"] = token
        ajouter(copie, "v1.0")
    # v1.1 — atlas pays (67 intrants, listes « intrants » par pays)
    for pays, bloc in atlas_biomasses_pays.PAYS_BIOMASSES.items():
        for fiche in bloc.get("intrants", []):
            copie = dict(fiche)
            copie["pays"] = pays
            ajouter(copie, "v1.1")
    # v1.2 — atlas vignobles (32 intrants, listes « intrants » par pays)
    for pays, bloc in atlas_vignobles_monde.VIGNOBLES_MONDE.items():
        for fiche in bloc.get("intrants", []):
            copie = dict(fiche)
            copie["pays"] = pays
            ajouter(copie, "v1.2")
    return points, exclus


# ---------------------------------------------------------------------------
# Clustering géographique déterministe (par pays, rayon de mutualisation)
# ---------------------------------------------------------------------------

def _distance_km(lat1, lon1, lat2, lon2):
    """Distance équirectangulaire (km) — suffisante pour du clustering."""
    lat_moy = math.radians((lat1 + lat2) / 2.0)
    dx = (lon2 - lon1) * 111.32 * math.cos(lat_moy)
    dy = (lat2 - lat1) * 110.57
    return math.sqrt(dx * dx + dy * dy)


def _clusters_du_pays(points):
    """Cluster greedy déterministe : un hub mutualise un rayon de 300 km."""
    tries = sorted(points, key=lambda p: (round(p["lat"], 4), round(p["lon"], 4)))
    clusters = []
    for point in tries:
        place = False
        for cluster in clusters:
            centre_lat = sum(p["lat"] for p in cluster) / len(cluster)
            centre_lon = sum(p["lon"] for p in cluster) / len(cluster)
            if _distance_km(point["lat"], point["lon"], centre_lat, centre_lon) <= RAYON_CLUSTER_KM:
                cluster.append(point)
                place = True
                break
        if not place:
            clusters.append([point])
    return clusters


def _slug(texte):
    """Slug déterministe d'un nom de pays (accents et espaces)."""
    correspondances = str.maketrans(
        "àáâäèéêëìíîïòóôöùúûüçñ",
        "aaaaeeeeiiiioooouuuucn")
    propre = texte.lower().translate(correspondances)
    garde = "".join(c if (c.isalnum() or c == "-") else "-" for c in propre)
    while "--" in garde:
        garde = garde.replace("--", "-")
    return garde.strip("-")


def _humidite_famille(famille):
    return HUMIDITES_FAMILLES.get(famille, HUMIDITE_DEFAUT)


def _charge_mois(fenetre):
    """Charge dérivée de la fenêtre : première haute, dernière fin."""
    charge = {}
    for rang, mois in enumerate(fenetre):
        if len(fenetre) == 1:
            charge[mois] = "haute"
        elif rang == 0:
            charge[mois] = "haute"
        elif rang == len(fenetre) - 1:
            charge[mois] = "fin"
        else:
            charge[mois] = "moyenne"
    return charge


def _trios_du_cluster(gisement, nb_points):
    """Flotte d'un hub — v1.7 : paliers sur le gisement FAOSTAT du hub.

    Gisement (somme des milieux de fourchette des points sourcés, en
    tonnes par an) : moins de 0,5 Mt : 1 trio. 0,5 à 2 : 2. 2 à 10 : 3.
    10 à 50 : 4. 50 et plus : 5. Seuils ILLUSTRATION, plafond figé de
    couverture d'une équipe d'opérateurs. Repli sur la règle de densité
    v1.6 si le hub n'a aucun point sourcé FAOSTAT (jamais de valeur
    inventée).
    """
    trios = gisements_hubs.trios_du_gisement(gisement, TRIOS_MAX_PAR_HUB)
    if trios is None:
        return min(TRIOS_MAX_PAR_HUB, 1 + (nb_points - 1) // 3)
    return trios


def _resume_gisement(gisement):
    """Résumé arrondi du gisement d'un hub pour les sorties JSON."""
    if gisement is None:
        return None
    return {
        "min_t_an": round(gisement["min"], 1),
        "moy_t_an": round(gisement["moy"], 1),
        "max_t_an": round(gisement["max"], 1),
        "points_sources": len(gisement["sources"]),
        "points_a_sourcer": len(gisement["a_sourcer"]),
        "etiquette": "SOURCÉ (FAOSTAT 2020-2024) + ratios ILLUSTRATION",
    }


def hubs_generalises():
    """Construit les hubs généralisés au format monde.HUBS_MONDE."""
    points, exclus = _collecte_points()
    par_pays = {}
    for point in points:
        par_pays.setdefault(point["pays"], []).append(point)
    hubs = {}
    compteur = 0
    for pays in sorted(par_pays):
        slug_pays = _slug(pays)
        for indice, cluster in enumerate(_clusters_du_pays(par_pays[pays]), start=1):
            compteur += 1
            hub_id = "gen-%s-%d" % (slug_pays, indice)
            biomasses = {}
            for point in cluster:
                biomasses[point["token"].lower()] = {
                    "bassin": hub_id,  # zone GPS enregistrée dans firms (V1.8)
                    "fenetre_operation": list(point["fenetre"]),
                    "charge_mois": _charge_mois(point["fenetre"]),
                    "humidite_pct": _humidite_famille(point["famille"]),
                }
            gisement = gisements_hubs.gisement_cluster(
                [p["token"] for p in cluster])
            trios = _trios_du_cluster(gisement, len(cluster))
            lat_centre = round(sum(p["lat"] for p in cluster) / len(cluster), 2)
            lon_centre = round(sum(p["lon"] for p in cluster) / len(cluster), 2)
            # V1.8 : le hub enregistre sa zone GPS — pain points FIRMS réels
            # avec une MAP_KEY locale, repli synthétique sinon.
            firms.enregistrer_zone_gps(hub_id, lat_centre, lon_centre)
            hubs[hub_id] = {
                "pays": pays,
                "region": "hub généralisé (%d points, centre %s/%s) — %s"
                          % (len(cluster), lat_centre, lon_centre,
                             ", ".join(sorted({p["region"] for p in cluster}))[:120]),
                "trio_id": "%s-trio-1" % hub_id,
                "graine": 7142 + 100 * compteur,  # convention lisible, sans collision P2
                "biomasses": biomasses,
                "_meta": {
                    "points": len(cluster),
                    "trios": trios,
                    "operateurs": EQUIPE_OPERATEURS * ((trios + TRIOS_MAX_PAR_HUB - 1)
                                                      // TRIOS_MAX_PAR_HUB),
                    "clusters": [p["token"] for p in cluster],
                    "sources_atlas": sorted({p["source_atlas"] for p in cluster}),
                    "gisement": _resume_gisement(gisement),
                    "lat_centre": lat_centre,
                    "lon_centre": lon_centre,
                    "etiquette": ETIQUETTE,
                },
            }
    return hubs, points, exclus


def composition():
    hubs, points, exclus = hubs_generalises()
    trios = sum(h["_meta"]["trios"] for h in hubs.values())
    operateurs = sum(h["_meta"]["operateurs"] for h in hubs.values())
    points_sources = sum(h["_meta"]["gisement"]["points_sources"]
                         for h in hubs.values()
                         if h["_meta"]["gisement"])
    points_a_sourcer = sum(h["_meta"]["gisement"]["points_a_sourcer"]
                           for h in hubs.values()
                           if h["_meta"]["gisement"])
    points_a_sourcer += sum(h["_meta"]["points"] for h in hubs.values()
                            if not h["_meta"]["gisement"])
    gisement_mondial = sum(h["_meta"]["gisement"]["moy_t_an"]
                           for h in hubs.values()
                           if h["_meta"]["gisement"])
    return {
        "etiquette": ETIQUETTE,
        "points_atlas": len(points) + len(exclus),
        "points_rattaches_flotte_p2": len(exclus),
        "points_generalises": len(points),
        "hubs_generalises": len(hubs),
        "pays": len({h["pays"] for h in hubs.values()}),
        "trios": trios,
        "operateurs": operateurs,
        "ratio_operateurs_par_trio": round(operateurs / trios, 2) if trios else 0.0,
        "gisements": {
            "fenetre": list(gisements_hubs.FENETRE),
            "points_sources": points_sources,
            "points_a_sourcer": points_a_sourcer,
            "somme_mondiale_t_an": round(gisement_mondial, 1),
            "seuils_trios_t": [int(s) for s in gisements_hubs.SEUILS_TRIO],
            "etiquette": "SOURCÉ (FAOSTAT 2020-2024) + ratios ILLUSTRATION, "
                         "proxys nationaux (décomposition régionale P3)",
        },
        "figeage": {
            "mtbf_h": simulateur.MTBF_HEURES,
            "mttr_h": simulateur.MTTR_HEURES,
            "operateurs_par_equipe": EQUIPE_OPERATEURS,
            "plafond_trios_par_equipe": TRIOS_MAX_PAR_HUB,
            "rayon_cluster_km": RAYON_CLUSTER_KM,
            "regle_trios": "v1.7 : paliers sur gisement FAOSTAT (fenêtre "
                           "2020-2024), repli densité v1.6 si hub sans "
                           "point sourcé",
            "note": "2 opérateurs couvrent jusqu'à 5 trios (doctrine IoT) ; "
                    "6e trio = seconde équipe ; M1/M2/M3 = variantes Monte Carlo",
        },
        "par_hub": [
            {"hub": hid, "pays": h["pays"], "points": h["_meta"]["points"],
             "trios": h["_meta"]["trios"], "operateurs": h["_meta"]["operateurs"],
             "graine": h["graine"]}
            for hid, h in hubs.items()
        ],
    }


# ---------------------------------------------------------------------------
# Simulation — réutilisation du simulateur v0.5 (injection runtime)
# ---------------------------------------------------------------------------

def _injecter(hubs):
    """Injecte les hubs généralisés dans monde.HUBS_MONDE (runtime)."""
    for hid, hub in hubs.items():
        copie = {k: v for k, v in hub.items() if k != "_meta"}
        monde.HUBS_MONDE[hid] = copie
    return [hid for hid in hubs]


def run(hub_id=None):
    """Une année simulée SYNTHÉTIQUE sur les hubs généralisés (ou un seul)."""
    hubs, _, _ = hubs_generalises()
    ids = _injecter(hubs)
    if hub_id is not None:
        if hub_id not in ids:
            print("ERREUR : hub généralisé inconnu « %s ». Hubs : %s"
                  % (hub_id, ", ".join(ids)))
            return 1
        ids = [hub_id]
    simulateur.MELANGE_MTTR = None
    simulateur.DELAI_REPONSE_H = 0.0
    simulateur.FACTEUR_STAFFING = 1.0
    simulateur.MTBF_COMMISSIONING_H = None
    simulateur.HEURES_COMMISSIONING = 0.0
    runs = [simulateur.simuler(hid) for hid in ids]
    comp = composition()

    dossier = os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "sorties"))
    os.makedirs(dossier, exist_ok=True)
    with open(os.path.join(dossier, "flotte-generale-run.json"), "w",
              encoding="utf-8") as f:
        json.dump({"etiquette": ETIQUETTE, "composition": comp,
                   "runs": [{k: v for k, v in r.items() if k != "telemetrie"}
                            for r in runs]},
                  f, ensure_ascii=False, indent=2)
        f.write("\n")

    lignes = ["# Flotte généralisée — run annuel SYNTHÉTIQUE", "",
              "Étiquette : **%s** — registre de développement, valeurs non calibrées." % ETIQUETTE,
              "Figeage : MTBF %g h, MTTR %g h, 2 opérateurs pour %d trios max." % (
                  simulateur.MTBF_HEURES, simulateur.MTTR_HEURES, TRIOS_MAX_PAR_HUB), "",
              "| Hub | Pays | Points | Trios | Ops | Lots | Fautes | Dispo |",
              "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r, hid in zip(runs, ids):
        meta = hubs[hid]["_meta"]
        lignes.append("| %s | %s | %d | %d | %d | %d | %d | %.1f %% |" % (
            hid, r["pays"], meta["points"], meta["trios"], meta["operateurs"],
            r["lots_total"], r["fautes_total"], r["disponibilite_pct"]))
    lignes.append("")
    with open(os.path.join(dossier, "flotte-generale-run.md"), "w",
              encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")

    print(">> flotte généralisée : %d hubs, %d trios, %d opérateurs — étiquette %s"
          % (len(ids), comp["trios"], comp["operateurs"], ETIQUETTE))
    for r in runs:
        print(">> %-22s %-14s — %4d lots, %2d fautes, dispo %.1f %%"
              % (r["hub"], r["pays"], r["lots_total"], r["fautes_total"],
                 r["disponibilite_pct"]))
    print(">> Sorties : %s" % dossier)
    return 0


def monte_carlo(nb_graines=50):
    """Monte Carlo léger sur la flotte généralisée (graines 1..N)."""
    hubs, _, _ = hubs_generalises()
    ids = _injecter(hubs)
    simulateur.MELANGE_MTTR = None
    simulateur.DELAI_REPONSE_H = 0.0
    simulateur.FACTEUR_STAFFING = 1.0
    simulateur.MTBF_COMMISSIONING_H = None
    simulateur.HEURES_COMMISSIONING = 0.0
    par_hub = {hid: {"dispo": [], "lots": [], "fautes": []} for hid in ids}
    for graine in range(1, nb_graines + 1):
        for hid in ids:
            r = simulateur.simuler(hid, graine=graine)
            par_hub[hid]["dispo"].append(r["disponibilite_pct"])
            par_hub[hid]["lots"].append(r["lots_total"])
            par_hub[hid]["fautes"].append(r["fautes_total"])
    stats = {
        "etiquette": ETIQUETTE,
        "graines": nb_graines,
        "hubs": len(ids),
        "runs_trio": nb_graines * len(ids),
        "lots_simules": sum(sum(v["lots"]) for v in par_hub.values()),
        "disponibilite_flotte_pct_moy": round(
            statistics.mean([d for v in par_hub.values() for d in v["dispo"]]), 1),
        "par_hub": {
            hid: {
                "dispo_moy": round(statistics.mean(v["dispo"]), 1),
                "dispo_min": min(v["dispo"]),
                "fautes_moy": round(statistics.mean(v["fautes"]), 1),
            } for hid, v in par_hub.items()
        },
    }
    dossier = os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "sorties"))
    os.makedirs(dossier, exist_ok=True)
    with open(os.path.join(dossier, "flotte-generale-mc.json"), "w",
              encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(">> %d runs trio — dispo flotte moy %.1f %% — agrégats dans "
          "sorties/flotte-generale-mc.json"
          % (stats["runs_trio"], stats["disponibilite_flotte_pct_moy"]))
    return 0


# ---------------------------------------------------------------------------
# Gardes de cohérence
# ---------------------------------------------------------------------------

def verifier():
    """Gardes : fenêtres valides, doublons, points rattachés exclus."""
    ecarts = []
    hubs, points, exclus = hubs_generalises()
    vus = set()
    for hid, hub in hubs.items():
        if not hub["biomasses"]:
            ecarts.append("%s sans biomasse" % hid)
        for nom, fiche in hub["biomasses"].items():
            if nom in vus:
                ecarts.append("biomasse dupliquée : %s" % nom)
            vus.add(nom)
            for mois in fiche["fenetre_operation"]:
                if not 1 <= mois <= 12:
                    ecarts.append("mois hors calendrier : %s dans %s" % (mois, nom))
    if len(vus) != len(points):
        ecarts.append("points collectés %d != biomasses %d" % (len(points), len(vus)))
    for hid, hub in hubs.items():
        for nom in hub["biomasses"]:
            if monde.mois_maintenance(hub) == tuple(range(1, 13)):
                ecarts.append("%s : aucune fenêtre active (année entière en maintenance)" % hid)
                break
    return ecarts


def sommaire():
    comp = composition()
    lignes = [
        "Flotte généralisée World Twin (V1.8) — étiquette %s" % ETIQUETTE,
        "",
        "- Points d'atlas : %d (rattachés flotte P2 : %d, généralisés : %d)"
        % (comp["points_atlas"], comp["points_rattaches_flotte_p2"],
           comp["points_generalises"]),
        "- Hubs généralisés : %d sur %d pays" % (comp["hubs_generalises"], comp["pays"]),
        "- Trios : %d — opérateurs : %d (ratio %.2f par trio)"
        % (comp["trios"], comp["operateurs"], comp["ratio_operateurs_par_trio"]),
        "- Dimensionnement v1.7 : gisement FAOSTAT %d-%d, points sourcés %d, "
        "À SOURCER %d, somme mondiale %.0f Mt/an (proxy national, P3 pour "
        "l'addressable)" % (comp["gisements"]["fenetre"][0],
                            comp["gisements"]["fenetre"][1],
                            comp["gisements"]["points_sources"],
                            comp["gisements"]["points_a_sourcer"],
                            comp["gisements"]["somme_mondiale_t_an"] / 1.0e6),
        "- Figeage : MTBF %g h, MTTR %g h, 2 opérateurs pour %d trios max, "
        "6e trio = seconde équipe" % (simulateur.MTBF_HEURES,
                                      simulateur.MTTR_HEURES,
                                      TRIOS_MAX_PAR_HUB),
        "- Variantes M1/M2/M3 : voir monte_carlo.py (V1.6)",
        "- Pain points V1.8 : zone GPS enregistrée par hub (boîte ±1.0° lat / "
        "±1.5° lon) — feux RÉELS NASA FIRMS avec une MAP_KEY locale, repli "
        "synthétique sinon, KPI identiques dans les deux cas",
        "",
        "Commandes : sommaire | flotte | run [HUB] | monte-carlo [GRAINES]",
    ]
    return "\n".join(lignes) + "\n"


def _formate_tonnes(valeur):
    """Formate une masse annuelle en t, kt ou Mt (lisibilité des tables)."""
    if valeur >= 1.0e6:
        return "%.2g Mt" % (valeur / 1.0e6)
    if valeur >= 1.0e3:
        return "%.3g kt" % (valeur / 1.0e3)
    return "%.3g t" % valeur


def table_flotte():
    hubs, _, _ = hubs_generalises()
    lignes = ["| Hub | Pays | Points | Trios | Ops | Graine | Gisement (t/an) |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    for hid, h in hubs.items():
        m = h["_meta"]
        if m["gisement"]:
            gisement = "%s à %s" % (_formate_tonnes(m["gisement"]["min_t_an"]),
                                    _formate_tonnes(m["gisement"]["max_t_an"]))
            if m["gisement"]["points_a_sourcer"]:
                gisement += " (+%d à sourcer)" % m["gisement"]["points_a_sourcer"]
        else:
            gisement = "À SOURCER"
        lignes.append("| %s | %s | %d | %d | %d | %d | %s |" % (
            hid, h["pays"], m["points"], m["trios"], m["operateurs"],
            h["graine"], gisement))
    return "\n".join(lignes) + "\n"


def main():
    arguments = sys.argv[1:]
    if not arguments or arguments[0] == "sommaire":
        for ecart in verifier():
            print("ATTENTION : %s" % ecart)
        print(sommaire())
        return 0
    if arguments[0] == "flotte":
        print(table_flotte())
        return 0
    if arguments[0] == "run":
        return run(arguments[1] if len(arguments) > 1 else None)
    if arguments[0] == "monte-carlo":
        graines = int(arguments[1]) if len(arguments) > 1 else 50
        return monte_carlo(graines)
    print("Commande inconnue : %s (sommaire | flotte | run [HUB] | monte-carlo [GRAINES])"
          % arguments[0])
    return 1


if __name__ == "__main__":
    sys.exit(main())
