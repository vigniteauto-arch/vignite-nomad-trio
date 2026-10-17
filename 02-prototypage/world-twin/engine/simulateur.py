#!/usr/bin/env python3
"""Couche 4/5 — Simulateur flotte World Twin (squelette non calibré).

Simule l'exploitation du trio Nomad v1 « comme si » il opérait déjà :
douze mois, cinq biomasses, pannes injectées, télémétrie SYNTHÉTIQUE
au contrat Edge, VDE en mode stub, rapports.

Lancement (bibliothèque standard uniquement, aucune dépendance) :

    python3 simulateur.py

Écrit dans ../sorties/ (ignoré par git, jamais versionné) :
    rapport-run.md / rapport-run.json       — synthèse du run
    telemetrie-echantillon.json             — télémétrie SYNTHÉTIQUE
    rapport-quotidien-exemple.md            — base du rapport World Ops

RÈGLES :
- Valeurs ILLUSTRATION non calibrées ; les paramètres réels vivent hors dépôt.
- Registre de DÉVELOPPEMENT, jamais le registre Merkle de production.
- Tout résultat est étiqueté SYNTHÉTIQUE.
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import scenario

# ---------------------------------------------------------------------------
# Paramètres figés v0 (cahier pilote France — pilote-france-2027.md)
# ---------------------------------------------------------------------------

SEED = 42
ANNEE = 2027
TRIO_ID = "fr-hub01-trio-1"
PAYS = "France"
REGION = "pilote-v0"
OPERATEURS_PAR_TRIO = 3   # hypothèse v0 à figer
MTBF_HEURES = 720.0       # ILLUSTRATION, non calibré
MTTR_HEURES = 8.0         # ILLUSTRATION, non calibré
LOTS_PAR_JOUR = 2         # ILLUSTRATION
CAPTEURS_PAR_MODULE = 3   # jouet : la vraie nomenclature vit hors dépôt

ETIQUETTE = "SYNTHÉTIQUE"

# Catalogue capteurs ILLUSTRATION (non calibré) : id, grandeur, unité, bornes.
CATALOGUE_CAPTEURS = {
    "buffer": [
        ("buf-hum-01", "humidite_entree", "%", (10.0, 80.0)),
        ("buf-niv-01", "niveau_silo", "%", (10.0, 100.0)),
        ("tmp-buf-01", "temperature_trappe", "C", (5.0, 40.0)),
    ],
    "stock": [
        ("stk-tmp-01", "temperature_pyrolyse", "C", (300.0, 650.0)),
        ("stk-gaz-01", "debit_syngaz", "m3/h", (50.0, 400.0)),
        ("stk-press-01", "pression_circuit", "kPa", (95.0, 110.0)),
    ],
    "ops": [
        ("ops-press-01", "pression_presse", "MPa", (5.0, 25.0)),
        ("ops-vis-01", "vitesse_vis", "rpm", (5.0, 40.0)),
        ("tmp-ops-01", "temperature_salle", "C", (18.0, 28.0)),
    ],
}


# ---------------------------------------------------------------------------
# VDE — stub non calibré (les coefficients réels vivent hors dépôt)
# ---------------------------------------------------------------------------

def vde_decider(biomasse, humidite_pct, prng):
    """Décision de recette simulée : interlocks + recette + mode.

    Stub : la grammaire des recettes réelle et les coefficients calibrés
    vivent hors du dépôt. Ici, logique de démonstration uniquement.
    """
    interlocks = []
    if humidite_pct > 65.0:
        interlocks.append("humidite_haute_pretraitement")
    if humidite_pct < 12.0:
        interlocks.append("humidite_basse_gestion_poussieres")
    recette = "recette-" + biomasse + "-v0"
    mode = "degrade" if interlocks else "nominal"
    lots_prevus = prng.entier(1, 3)
    return {
        "recette": recette,
        "mode": mode,
        "interlocks": interlocks,
        "lots_prevus": lots_prevus,
        "etiquette": ETIQUETTE,
    }


# ---------------------------------------------------------------------------
# Télémétrie — contrat Edge (digital-twin/schemas/donnees-capteurs.schema.json)
# ---------------------------------------------------------------------------

def telemetrie_module(module, lot_id, horodatage, prng, qualite="nominal"):
    catalogue = CATALOGUE_CAPTEURS[module]
    capteurs = []
    for id_capteur, grandeur, unite, (bas, haut) in catalogue:
        valeur = round(prng.intervalle(bas, haut), 1)
        capteurs.append(
            {
                "id_capteur": id_capteur,
                "grandeur": grandeur,
                "valeur": valeur,
                "unite": unite,
                "qualite": qualite,
            }
        )
    return {
        "module": module,
        "lot_id": lot_id,
        "timestamp": horodatage,
        "capteurs": capteurs,
    }


# ---------------------------------------------------------------------------
# Simulation
# ---------------------------------------------------------------------------

def simuler():
    prng = scenario.Prng(SEED)
    evenements = []          # faute -> action -> log
    telemetrie = []
    resume_mensuel = []
    lots_total = 0
    heures_disponibles = 0.0
    heures_indisponibles = 0.0
    etat = "operationnel"   # operationnel | en_panne | maintenance_saisonniere
    fin_panne = None

    debut_annee = datetime(ANNEE, 1, 1, tzinfo=timezone.utc)

    for mois in range(1, 13):
        biomasses = scenario.biomasses_du_mois(mois)
        en_maintenance = mois in scenario.MOIS_MAINTENANCE
        lots_mois = 0
        fautes_mois = 0

        for jour in range(1, 29):  # mois simulé de 28 jours (v0)
            date = debut_annee.replace(month=mois, day=jour)

            if en_maintenance:
                if etat == "operationnel":
                    evenements.append(evenement(date, "trio", "entree_maintenance_saisonniere",
                                                "bascule_mode_maintenance",
                                                "mode=maintenance ; calibrages internes hors dépôt"))
                etat = "maintenance_saisonniere"
                heures_disponibles += 0.0
                continue

            # Pannes : hazard déterministe sur MTBF/MTTR (ILLUSTRATION).
            if etat == "operationnel" and prng.uniforme() < (24.0 / MTBF_HEURES):
                fautes_mois += 1
                module = prng.entier(0, 2)
                nom_module = ("buffer", "stock", "ops")[module]
                panne = PANNES_ILLUSTRATION[prng.entier(0, len(PANNES_ILLUSTRATION) - 1)]
                duree = round(MTTR_HEURES * prng.intervalle(0.5, 1.5), 1)
                etat = "en_panne"
                fin_panne = date + timedelta(hours=duree)
                evenements.append(
                    evenement(date, nom_module, panne,
                              "arret_module + intervention_simulee_MTTR",
                              "ticket_mttr_ouvert ; duree_h=%.1f" % duree)
                )
                heures_indisponibles += duree

            if etat == "en_panne":
                if date.replace(hour=23) >= fin_panne:
                    etat = "operationnel"
                    evenements.append(evenement(date, "trio", "fin_panne",
                                                "retour_operationnel",
                                                "ticket_mttr_ferme"))
                else:
                    continue

            # Journée opérationnelle : lots, scénario, VDE, télémétrie.
            for indice_lot in range(LOTS_PAR_JOUR):
                if not biomasses:
                    break
                biomasse = biomasses[indice_lot % len(biomasses)]
                cellule = scenario.cellule(PAYS, REGION, biomasse, mois, prng)
                decision = vde_decider(biomasse, cellule["humidite_pct"], prng)
                horodatage = date.replace(hour=6 + 6 * indice_lot).isoformat().replace("+00:00", "Z")
                lot_id = "lot-%04d-%s" % (lots_total + 1, biomasse)
                lots_total += 1
                lots_mois += 1
                qualite = "degrade" if decision["mode"] == "degrade" else "nominal"
                for module in ("buffer", "stock", "ops"):
                    telemetrie.append(
                        telemetrie_module(module, lot_id, horodatage, prng, qualite)
                    )
                if decision["interlocks"]:
                    evenements.append(
                        evenement(date, "vde", "interlocks=" + ",".join(decision["interlocks"]),
                                  "recette=" + decision["recette"] + " mode=" + decision["mode"],
                                  "lot=" + lot_id)
                    )
            heures_disponibles += 24.0

        resume_mensuel.append(
            {
                "mois": mois,
                "biomasses": list(biomasses),
                "lots": lots_mois,
                "fautes": fautes_mois,
                "etat": "maintenance" if en_maintenance else "operation",
                "etiquette": ETIQUETTE,
            }
        )

    disponibilite = heures_disponibles / (heures_disponibles + heures_indisponibles)
    return {
        "trio": TRIO_ID,
        "annee": ANNEE,
        "graine": SEED,
        "lots_total": lots_total,
        "fautes_total": len([e for e in evenements if e["faute"].startswith(("panne", "capteur", "vis", "press", "sur"))]),
        "evenements": evenements,
        "resume_mensuel": resume_mensuel,
        "heures_disponibles": round(heures_disponibles, 1),
        "heures_indisponibles": round(heures_indisponibles, 1),
        "disponibilite_pct": round(disponibilite * 100.0, 1),
        "telemetrie": telemetrie,
        "etiquette_globale": ETIQUETTE,
    }


PANNES_ILLUSTRATION = [
    "panne_vis_alimentation",
    "capteur_temperature_hors_plage",
    "pression_hydrolique_insuffisante",
    "sur_chauffe_bearings_presse",
]


def evenement(date, module, faute, action, log):
    return {
        "timestamp": date.isoformat().replace("+00:00", "Z"),
        "module": module,
        "faute": faute,
        "action": action,
        "log": log,
        "etiquette": ETIQUETTE,
    }


# ---------------------------------------------------------------------------
# Rapports
# ---------------------------------------------------------------------------

MOIS_NOMS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
             "août", "septembre", "octobre", "novembre", "décembre"]


def rapport_run_markdown(run):
    lignes = []
    lignes.append("# Rapport de run — World Twin pilote France %d" % run["annee"])
    lignes.append("")
    lignes.append("Étiquette : **%s** — registre de développement, valeurs non calibrées." % run["etiquette_globale"])
    lignes.append("")
    lignes.append("## Synthèse")
    lignes.append("")
    lignes.append("- Trio : %s, %d opérateurs (hypothèse v0)." % (run["trio"], OPERATEURS_PAR_TRIO))
    lignes.append("- Graine : %d — run reproductible à l'identique." % run["graine"])
    lignes.append("- Lots simulés : %d. Fautes : %d." % (run["lots_total"], run["fautes_total"]))
    lignes.append("- Disponibilité : %.1f %% (disponible %.0f h, indisponible %.0f h)."
                  % (run["disponibilite_pct"], run["heures_disponibles"], run["heures_indisponibles"]))
    lignes.append("")
    lignes.append("## Résumé mensuel")
    lignes.append("")
    lignes.append("| Mois | Biomasses actives | Lots | Fautes | État |")
    lignes.append("| --- | --- | --- | --- | --- |")
    for m in run["resume_mensuel"]:
        lignes.append("| %s | %s | %d | %d | %s |" % (
            MOIS_NOMS[m["mois"] - 1],
            ", ".join(m["biomasses"]) or "—",
            m["lots"], m["fautes"], m["etat"],
        ))
    lignes.append("")
    lignes.append("## Journal fautes -> actions -> logs (extrait)")
    lignes.append("")
    lignes.append("| Horodatage | Module | Faute | Action | Log |")
    lignes.append("| --- | --- | --- | --- | --- |")
    for e in run["evenements"][:40]:
        lignes.append("| %s | %s | %s | %s | %s |" % (
            e["timestamp"], e["module"], e["faute"], e["action"], e["log"],
        ))
    if len(run["evenements"]) > 40:
        lignes.append("")
        lignes.append("… et %d autres événements dans rapport-run.json." % (len(run["evenements"]) - 40))
    lignes.append("")
    return "\n".join(lignes) + "\n"


def rapport_quotidien_exemple(run):
    dernier_jour = run["evenements"][-5:] if run["evenements"] else []
    lignes = []
    lignes.append("# World Ops — rapport quotidien (exemple simulé)")
    lignes.append("")
    lignes.append("Étiquette : **%s**. Ce rapport est le gabarit de la tâche planifiée World Ops." % ETIQUETTE)
    lignes.append("")
    lignes.append("## État de la flotte")
    lignes.append("")
    lignes.append("- %s : operationnel, %d lots cumulés." % (run["trio"], run["lots_total"]))
    lignes.append("- Disponibilité cumulée : %.1f %%." % run["disponibilite_pct"])
    lignes.append("")
    lignes.append("## Fautes -> actions -> logs (derniers événements)")
    lignes.append("")
    if dernier_jour:
        for e in dernier_jour:
            lignes.append("- %s — %s : %s → %s (%s)" % (
                e["timestamp"], e["module"], e["faute"], e["action"], e["log"]))
    else:
        lignes.append("- Aucune faute. Journée nominale.")
    lignes.append("")
    lignes.append("## Recommandations")
    lignes.append("")
    lignes.append("- Vérifier la fenêtre de la biomasse active du mois dans le cahier pilote.")
    lignes.append("- Confirmer les paramètres MTBF/MTTR avant le passage P2.")
    lignes.append("- Rappel : toute donnée reste SYNTHÉTIQUE, registre de développement.")
    lignes.append("")
    return "\n".join(lignes) + "\n"


def main():
    run = simuler()
    dossier_sorties = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sorties")
    dossier_sorties = os.path.normpath(dossier_sorties)
    os.makedirs(dossier_sorties, exist_ok=True)

    with open(os.path.join(dossier_sorties, "rapport-run.md"), "w", encoding="utf-8") as f:
        f.write(rapport_run_markdown(run))

    run_json = dict(run)
    telemetrie_echantillon = run["telemetrie"][:120]
    del run_json["telemetrie"]
    with open(os.path.join(dossier_sorties, "rapport-run.json"), "w", encoding="utf-8") as f:
        json.dump(run_json, f, ensure_ascii=False, indent=2)
        f.write("\n")

    with open(os.path.join(dossier_sorties, "telemetrie-echantillon.json"), "w", encoding="utf-8") as f:
        json.dump(
            {"etiquette": ETIQUETTE, "contrat": "digital-twin/schemas/donnees-capteurs.schema.json",
             "enregistrements": telemetrie_echantillon},
            f, ensure_ascii=False, indent=2,
        )
        f.write("\n")

    with open(os.path.join(dossier_sorties, "rapport-quotidien-exemple.md"), "w", encoding="utf-8") as f:
        f.write(rapport_quotidien_exemple(run))

    print(">> Run World Twin terminé (étiquette %s)" % ETIQUETTE)
    print(">> Trio %s — %d lots, %d événements, disponibilité %.1f %%"
          % (run["trio"], run["lots_total"], len(run["evenements"]), run["disponibilite_pct"]))
    print(">> Sorties : %s" % dossier_sorties)
    return 0


if __name__ == "__main__":
    sys.exit(main())
