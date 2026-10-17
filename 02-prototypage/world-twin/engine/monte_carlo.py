#!/usr/bin/env python3
"""Runner Monte Carlo World Twin — multi-graines et sensibilité (non calibré).

Exécute le simulateur sur de nombreuses graines, en variant MTBF et MTTR
pour éclairer les décisions de figeage. Les agrégats (et uniquement les
agrégats) sont écrits dans ../sorties/.

v0.4 (P2) : mode monde — la flotte entière (Carré d'Or, LatAm, Al-Atlas)
tourne à l'échelle du millier de runs. Les statistiques sont accumulées
grain par grain (mémoire constante), hub par hub.

Lancement :

    python3 monte_carlo.py                          # 200 + 50 graines, France
    python3 monte_carlo.py 1000 200                # milliers de runs, France
    python3 monte_carlo.py 1000 200 monde          # milliers de runs, monde
    python3 monte_carlo.py 1000 200 fr-rhone        # un hub précis

RÈGLES : étiquette SYNTHÉTIQUE — registre de développement ; aucune
valeur calibrée ; les sorties ne sont jamais versionnées (.gitignore).
"""

import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import simulateur
import monde

CONFIGS = {
    "baseline-720h-8h": (720.0, 8.0),
    "mtbf-500h":        (500.0, 8.0),
    "mtbf-1000h":       (1000.0, 8.0),
    "mttr-4h":          (720.0, 4.0),
    "mttr-12h":         (720.0, 12.0),
}

PAS_PROGRESSION = 100  # affiche une ligne tous les PAS runs


def _nouvel_accumulateur():
    return {"lots": [], "fautes": [], "dispo": [], "indispo": [], "lots_cumules": 0}


def run_config(nom, mtbf, mttr, nb_graines, hub_ids):
    """Runs multi-graines d'une config, agrégés hub par hub (mémoire constante).

    Le PRNG du simulateur et le cache FIRMS mémoire font que la première
    graine paie les requêtes réseau éventuelles, les suivantes tournent
    sur cache — aucune dérive de déterminisme.
    """
    simulateur.MTBF_HEURES = mtbf
    simulateur.MTTR_HEURES = mttr
    par_hub = {h: _nouvel_accumulateur() for h in hub_ids}
    for graine in range(1, nb_graines + 1):
        for hub_id in hub_ids:
            r = simulateur.simuler(hub_id, graine=graine)
            acc = par_hub[hub_id]
            acc["lots"].append(r["lots_total"])
            acc["fautes"].append(r["fautes_total"])
            acc["dispo"].append(r["disponibilite_pct"])
            acc["indispo"].append(r["heures_indisponibles"])
            acc["lots_cumules"] += r["lots_total"]
        if nb_graines >= PAS_PROGRESSION and graine % PAS_PROGRESSION == 0:
            print("   ... %d/%d graines" % (graine, nb_graines))
    hubs_stats = []
    for hub_id in hub_ids:
        acc = par_hub[hub_id]
        hub = monde.HUBS_MONDE[hub_id]
        hubs_stats.append({
            "hub": hub_id,
            "pays": hub["pays"],
            "lots_total_cumules": acc["lots_cumules"],
            "lots_par_run": {"min": min(acc["lots"]),
                              "moy": round(statistics.mean(acc["lots"]), 1),
                              "max": max(acc["lots"])},
            "fautes_par_run": {"min": min(acc["fautes"]),
                                "moy": round(statistics.mean(acc["fautes"]), 1),
                                "max": max(acc["fautes"])},
            "disponibilite_pct": {"min": min(acc["dispo"]),
                                   "moy": round(statistics.mean(acc["dispo"]), 1),
                                   "max": max(acc["dispo"])},
            "heures_indispo_moy": round(statistics.mean(acc["indispo"]), 1),
        })
    tous_lots = [v for h in hub_ids for v in par_hub[h]["lots"]]
    toutes_dispo = [v for h in hub_ids for v in par_hub[h]["dispo"]]
    return {
        "config": nom, "mtbf_h": mtbf, "mttr_h": mttr,
        "graines": nb_graines, "hubs_par_run": len(hub_ids),
        "lots_total_cumules": sum(par_hub[h]["lots_cumules"] for h in hub_ids),
        "lots_par_run_flotte": {"min": min(tous_lots),
                                 "moy": round(statistics.mean(tous_lots), 1),
                                 "max": max(tous_lots)},
        "disponibilite_flotte_pct": {"min": min(toutes_dispo),
                                      "moy": round(statistics.mean(toutes_dispo), 1),
                                      "max": max(toutes_dispo)},
        "par_hub": hubs_stats,
    }


def resoudre_hubs(arg):
    if arg is None or arg == "france":
        return ["fr-rhone"]
    if arg == "monde":
        return list(monde.HUBS_MONDE)
    if arg in monde.HUBS_MONDE:
        return [arg]
    print("ERREUR : mode/hub inconnu « %s ». Modes : france, monde ; ou un hub : %s"
          % (arg, ", ".join(monde.HUBS_MONDE)))
    sys.exit(1)


def main():
    graines_baseline = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    graines_variante = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    hub_ids = resoudre_hubs(sys.argv[3] if len(sys.argv) > 3 else "france")

    resultats = []
    for nom, (mtbf, mttr) in CONFIGS.items():
        nb = graines_baseline if nom == "baseline-720h-8h" else graines_variante
        resultats.append(run_config(nom, mtbf, mttr, nb, hub_ids))
        print(">> %-18s %3d graines x %d hubs — dispo flotte moy %.1f %%" % (
            nom, nb, len(hub_ids), resultats[-1]["disponibilite_flotte_pct"]["moy"]))

    total_runs = sum(c["graines"] * c["hubs_par_run"] for c in resultats)
    total_lots = sum(c["lots_total_cumules"] for c in resultats)
    charge = {
        "etiquette": "SYNTHÉTIQUE",
        "mode": "monde" if len(hub_ids) > 1 else hub_ids[0],
        "hubs": hub_ids,
        "total_runs_trio": total_runs,
        "total_lots_simules": total_lots,
        "configs": resultats,
    }
    dossier = os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "sorties"))
    os.makedirs(dossier, exist_ok=True)
    with open(os.path.join(dossier, "monte-carlo-agregats.json"), "w", encoding="utf-8") as f:
        json.dump(charge, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(">> %d runs trio — %.0f lots simulés — agrégats dans sorties/monte-carlo-agregats.json" % (
        total_runs, total_lots))
    return 0


if __name__ == "__main__":
    sys.exit(main())
