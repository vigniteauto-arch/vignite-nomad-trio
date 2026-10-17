#!/usr/bin/env python3
"""Runner Monte Carlo World Twin — multi-graines et sensibilité (non calibré).

Exécute le simulateur du pilote France sur de nombreuses graines, en
variant MTBF et MTTR pour éclairer les décisions de figeage. Les
agrégats (et uniquement les agrégats) sont écrits dans ../sorties/.

Lancement :

    python3 monte_carlo.py            # par défaut : 200 graines baseline + variantes
    python3 monte_carlo.py 500 100    # graines baseline, graines par variante

RÈGLES : étiquette SYNTHÉTIQUE — registre de développement ; aucune
valeur calibrée ; les sorties ne sont jamais versionnées (.gitignore).
"""

import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import simulateur

CONFIGS = {
    "baseline-720h-8h": (720.0, 8.0),
    "mtbf-500h":        (500.0, 8.0),
    "mtbf-1000h":       (1000.0, 8.0),
    "mttr-4h":          (720.0, 4.0),
    "mttr-12h":         (720.0, 12.0),
}


def run_config(nom, mtbf, mttr, nb_graines):
    simulateur.MTBF_HEURES = mtbf
    simulateur.MTTR_HEURES = mttr
    lots, fautes, dispo, indispo = [], [], [], []
    for graine in range(1, nb_graines + 1):
        simulateur.SEED = graine
        r = simulateur.simuler()
        lots.append(r["lots_total"])
        fautes.append(r["fautes_total"])
        dispo.append(r["disponibilite_pct"])
        indispo.append(r["heures_indisponibles"])
    return {
        "config": nom, "mtbf_h": mtbf, "mttr_h": mttr, "graines": nb_graines,
        "lots_total_cumules": sum(lots),
        "lots_par_run": {"min": min(lots), "moy": round(statistics.mean(lots), 1), "max": max(lots)},
        "fautes_par_run": {"min": min(fautes), "moy": round(statistics.mean(fautes), 1), "max": max(fautes)},
        "disponibilite_pct": {"min": min(dispo), "moy": round(statistics.mean(dispo), 1), "max": max(dispo)},
        "heures_indispo_moy": round(statistics.mean(indispo), 1),
    }


def main():
    graines_baseline = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    graines_variante = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    resultats = []
    for nom, (mtbf, mttr) in CONFIGS.items():
        nb = graines_baseline if nom == "baseline-720h-8h" else graines_variante
        resultats.append(run_config(nom, mtbf, mttr, nb))
        print(">> %-18s %3d graines — dispo moy %.1f %%" % (
            nom, nb, resultats[-1]["disponibilite_pct"]["moy"]))
    charge = {
        "etiquette": "SYNTHÉTIQUE",
        "total_runs": sum(c["graines"] for c in resultats),
        "total_lots_simules": sum(c["lots_total_cumules"] for c in resultats),
        "configs": resultats,
    }
    dossier = os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "sorties"))
    os.makedirs(dossier, exist_ok=True)
    with open(os.path.join(dossier, "monte-carlo-agregats.json"), "w", encoding="utf-8") as f:
        json.dump(charge, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(">> %d runs — %d lots simulés — agrégats dans sorties/monte-carlo-agregats.json" % (
        charge["total_runs"], charge["total_lots_simules"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
