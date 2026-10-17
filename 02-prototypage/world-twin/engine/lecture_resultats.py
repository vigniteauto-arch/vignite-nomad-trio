#!/usr/bin/env python3
"""Lecture des résultats Monte Carlo — World Twin (v0.5, 17/10/2026).

Consomme les agrégats produits par monte_carlo.py
(sorties/monte-carlo-agregats.json) et, s'il est présent, le rapport du
dernier run (sorties/rapport-run.json), puis produit une analyse lisible :

- classement des hubs par disponibilité (config figée baseline) ;
- sensibilité MTBF/MTTR contre la config figée, en deltas de points
  de disponibilité et de lots par run flotte ;
- synthèse du dernier run si disponible.

Écrit sorties/lecture-resultats.md et sorties/lecture-resultats.json.

RÈGLES : étiquette SYNTHÉTIQUE — les sorties ne sont jamais versionnées ;
lecture passive : aucune écriture en dehors de sorties/ ; aucune valeur
calibrée. La lecture éclaire le figeage, elle ne le remplace pas : la
qualification reste le monopole des FAT/SAT sur machines réelles.

Lancement :

    python3 engine/lecture_resultats.py
"""

import json
import os
import sys

ETIQUETTE = "SYNTHÉTIQUE"


def dossier_sorties():
    chemin = os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "sorties"))
    return chemin


def charger_json(chemin):
    with open(chemin, "r", encoding="utf-8") as f:
        return json.load(f)


def trouver_baseline(configs):
    """Config figée : baseline-720h-8h, sinon la première config."""
    for c in configs:
        if c["config"].startswith("baseline"):
            return c
    return configs[0] if configs else None


def delta(valeur, reference):
    return round(valeur - reference, 1)


def analyser_config(config, baseline):
    dispo = config["disponibilite_flotte_pct"]["moy"]
    lots = config["lots_par_run_flotte"]["moy"]
    entree = {
        "config": config["config"],
        "mtbf_h": config["mtbf_h"],
        "mttr_h": config["mttr_h"],
        "graines": config["graines"],
        "dispo_flotte_pct_moy": dispo,
        "lots_par_run_flotte_moy": lots,
        "lots_total_cumules": config["lots_total_cumules"],
    }
    if baseline is not None:
        entree["delta_dispo_vs_baseline_pts"] = delta(
            dispo, baseline["disponibilite_flotte_pct"]["moy"])
        entree["delta_lots_vs_baseline"] = delta(
            lots, baseline["lots_par_run_flotte"]["moy"])
    return entree


def classement_hubs(baseline):
    hubs = baseline["par_hub"] if baseline else []
    classe = sorted(hubs, key=lambda h: h["disponibilite_pct"]["moy"], reverse=True)
    lignes = []
    for rang, h in enumerate(classe, 1):
        lignes.append({
            "rang": rang,
            "hub": h["hub"],
            "pays": h["pays"],
            "dispo_pct_moy": h["disponibilite_pct"]["moy"],
            "dispo_pct_min": h["disponibilite_pct"]["min"],
            "lots_par_run_moy": h["lots_par_run"]["moy"],
            "fautes_par_run_moy": h["fautes_par_run"]["moy"],
            "heures_indispo_moy": h["heures_indispo_moy"],
        })
    return lignes


def sensibilité(configs, baseline):
    """Deltas des variantes MTBF/MTTR contre la config figée."""
    variants = []
    if baseline is None:
        return variants
    ref = (baseline["mtbf_h"], baseline["mttr_h"])
    for c in configs:
        if c["config"] == baseline["config"]:
            continue
        sens = ""
        if c["mttr_h"] == ref[1] and c["mtbf_h"] != ref[0]:
            sens = "MTBF %s -> %s h" % (ref[0], c["mtbf_h"])
        elif c["mtbf_h"] == ref[0] and c["mttr_h"] != ref[1]:
            sens = "MTTR %s -> %s h" % (ref[1], c["mttr_h"])
        variants.append({
            "config": c["config"],
            "levier": sens or "%s/%s -> %s/%s" % (ref[0], ref[1], c["mtbf_h"], c["mttr_h"]),
            "delta_dispo_pts": delta(c["disponibilite_flotte_pct"]["moy"],
                                     baseline["disponibilite_flotte_pct"]["moy"]),
            "delta_lots_par_run": delta(c["lots_par_run_flotte"]["moy"],
                                        baseline["lots_par_run_flotte"]["moy"]),
        })
    return variants


def analyser_dernier_run(chemin_run):
    """Synthèse courte du dernier run simulateur, si le rapport existe."""
    if not os.path.exists(chemin_run):
        return None
    try:
        run = charger_json(chemin_run)
    except (ValueError, OSError):
        return None
    hubs = []
    for r in run.get("runs", []):
        hubs.append({
            "hub": r["hub"],
            "pays": r["pays"],
            "lots_total": r["lots_total"],
            "fautes_total": r["fautes_total"],
            "disponibilite_pct": r["disponibilite_pct"],
        })
    return {
        "mode": run.get("mode"),
        "hubs": run.get("hubs", []),
        "totaux": run.get("totaux", {}),
        "par_hub": hubs,
    }


def rendre_markdown(analyse):
    lignes = []
    lignes.append("# Lecture des résultats — World Twin (v0.5)")
    lignes.append("")
    lignes.append("Étiquette : %s. Lecture des agrégats Monte Carlo — "
                  "les sorties ne sont jamais versionnées." % ETIQUETTE)
    lignes.append("")
    lignes.append("## Vue d'ensemble")
    lignes.append("")
    lignes.append("- Mode : %s — hubs : %s" % (analyse["mode"], ", ".join(analyse["hubs"])))
    lignes.append("- %d runs trio, %d lots simulés au total." % (
        analyse["total_runs_trio"], analyse["total_lots_simules"]))
    if analyse["baseline"]:
        lignes.append("- Config figée : %s (MTBF %s h, MTTR %s h) — dispo flotte moy %.1f %%." % (
            analyse["baseline"]["config"], analyse["baseline"]["mtbf_h"],
            analyse["baseline"]["mttr_h"],
            analyse["baseline"]["disponibilite_flotte_pct"]["moy"]))
    lignes.append("")
    lignes.append("## Classement des hubs (config figée)")
    lignes.append("")
    lignes.append("| Rang | Hub | Pays | Dispo moy % | Dispo min % | Lots/run | Fautes/run |")
    lignes.append("| --- | --- | --- | --- | --- | --- | --- |")
    for h in analyse["classement"]:
        lignes.append("| %d | %s | %s | %.1f | %.1f | %.1f | %.1f |" % (
            h["rang"], h["hub"], h["pays"], h["dispo_pct_moy"],
            h["dispo_pct_min"], h["lots_par_run_moy"], h["fautes_par_run_moy"]))
    lignes.append("")
    if analyse["classement"]:
        plus_faible = analyse["classement"][-1]
        lignes.append("Point d'attention : %s ferme la marche (%.1f %% de dispo moyenne ; "
                      "%.1f h d'indispo moyennes par run) — à surveiller en priorité World Ops." % (
                          plus_faible["hub"], plus_faible["dispo_pct_moy"],
                          plus_faible.get("heures_indispo_moy", 0.0)))
        lignes.append("")
    lignes.append("## Sensibilité au figeage (deltas contre la config figée)")
    lignes.append("")
    lignes.append("| Config | Levier | Delta dispo (pts) | Delta lots/run |")
    lignes.append("| --- | --- | --- | --- |")
    for v in analyse["sensibilite"]:
        lignes.append("| %s | %s | %+.1f | %+.1f |" % (
            v["config"], v["levier"], v["delta_dispo_pts"], v["delta_lots_par_run"]))
    lignes.append("")
    lignes.append("Lecture : un delta de disponibilité faible entre MTBF 500 h et 1000 h "
                  "signale un figeage robuste ; un delta important signale un paramètre "
                  "décisif à sécuriser avant la qualification. Ces écarts éclairent la "
                  "décision de figeage, ils ne la remplacent pas.")
    lignes.append("")
    if analyse["dernier_run"]:
        dr = analyse["dernier_run"]
        lignes.append("## Dernier run simulateur (si présent)")
        lignes.append("")
        lignes.append("- Mode : %s — %d hubs." % (dr["mode"], len(dr["hubs"])))
        totaux = dr["totaux"]
        if totaux:
            lignes.append("- Totaux : %d lots, %d fautes, %d événements, %.1f h d'indispo." % (
                totaux.get("lots_total", 0), totaux.get("fautes_total", 0),
                totaux.get("evenements_total", 0), totaux.get("heures_indisponibles", 0.0)))
        for h in dr["par_hub"]:
            lignes.append("- %s (%s) : %d lots, %d fautes, dispo %.1f %%." % (
                h["hub"], h["pays"], h["lots_total"], h["fautes_total"], h["disponibilite_pct"]))
        lignes.append("")
    lignes.append("Rappel : simulation SYNTHÉTIQUE, registre de développement ; "
                  "la qualification reste le monopole des FAT/SAT sur machines réelles.")
    lignes.append("")
    return "\n".join(lignes)


def main():
    sorties = dossier_sorties()
    chemin_mc = os.path.join(sorties, "monte-carlo-agregats.json")
    chemin_run = os.path.join(sorties, "rapport-run.json")
    if not os.path.exists(chemin_mc):
        print("ERREUR : %s introuvable. Lance d'abord : "
              "python3 engine/monte_carlo.py [graines] [variantes] [france|monde|hub]" % chemin_mc)
        return 1
    charge = charger_json(chemin_mc)
    configs = charge.get("configs", [])
    baseline = trouver_baseline(configs)
    analyse = {
        "etiquette": ETIQUETTE,
        "mode": charge.get("mode"),
        "hubs": charge.get("hubs", []),
        "total_runs_trio": charge.get("total_runs_trio", 0),
        "total_lots_simules": charge.get("total_lots_simules", 0),
        "baseline": baseline,
        "configs": [analyser_config(c, baseline) for c in configs],
        "classement": classement_hubs(baseline),
        "sensibilite": sensibilité(configs, baseline),
        "dernier_run": analyser_dernier_run(chemin_run),
    }
    with open(os.path.join(sorties, "lecture-resultats.json"), "w", encoding="utf-8") as f:
        json.dump(analyse, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(os.path.join(sorties, "lecture-resultats.md"), "w", encoding="utf-8") as f:
        f.write(rendre_markdown(analyse))
    print(">> Lecture écrite : sorties/lecture-resultats.md et sorties/lecture-resultats.json")
    if analyse["classement"]:
        meilleur = analyse["classement"][0]
        plus_faible = analyse["classement"][-1]
        print(">> Meilleure dispo : %s (%.1f %%) — plus faible : %s (%.1f %%)" % (
            meilleur["hub"], meilleur["dispo_pct_moy"],
            plus_faible["hub"], plus_faible["dispo_pct_moy"]))
    for v in analyse["sensibilite"]:
        print(">> %-18s %+.1f pts de dispo (%s)" % (
            v["config"], v["delta_dispo_pts"], v["levier"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
