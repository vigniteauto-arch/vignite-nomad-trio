#!/usr/bin/env python3
"""Couche 4/5 — Simulateur flotte World Twin (squelette non calibré).

Simule l'exploitation du trio Nomad v1 « comme si » il opérait déjà :
douze mois, pannes injectées, télémétrie SYNTHÉTIQUE au contrat Edge,
VDE en mode stub, rapports.

v0.4 (P2) : flotte MONDE — Carré d'Or (France, Suisse, Italie, Espagne),
LatAm (Argentine — Cuyo, Misiones), Al-Atlas (Maroc). Chaque hub vit
dans engine/monde.py, avec sa saisonnalité propre (hémisphère Sud
inclus) et sa graine déterministe. Le hub fr-rhone réplique
exactement le pilote France v0.3.

Lancement (bibliothèque standard uniquement, aucune dépendance) :

    python3 simulateur.py                 # monde : tous les hubs P2
    python3 simulateur.py fr-rhone        # un seul hub (compat v0.3)

Écrit dans ../sorties/ (ignoré par git, jamais versionné) :
    rapport-run.md / rapport-run.json       — synthèse du run (KPI par hub)
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
import firms
import monde

# ---------------------------------------------------------------------------
# Paramètres figés v0 (cahier pilote France — pilote-france-2027.md)
# ---------------------------------------------------------------------------

SEED = 42
ANNEE = 2027
OPERATEURS_PAR_TRIO = 2   # figé 17/10/2026 — modèle tournant : hub régional
                            # de 3 à 5 trios, éloignés de 1 h 30 à 2 h de route max
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
# VDE — stub non calibré (les coefficients réels vivent hors du dépôt)
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
# Simulation — générique par hub (engine/monde.py)
# ---------------------------------------------------------------------------

def simuler(hub_id="fr-rhone", graine=None):
    """Simule une année du trio d'un hub, de façon déterministe.

    hub_id : identifiant du hub dans monde.HUBS_MONDE.
    graine : graine du run ; par défaut, celle du hub.
    Le hub fr-rhone réplique exactement le pilote France v0.3.
    """
    hub = monde.HUBS_MONDE[hub_id]
    graine_run = graine if graine is not None else hub["graine"]
    trio_id = hub["trio_id"]
    pays = hub["pays"]
    region = hub["region"]
    maintenance = monde.mois_maintenance(hub)

    prng = scenario.Prng(graine_run)
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
        biomasses = monde.biomasses_du_mois(hub, mois)
        en_maintenance = mois in maintenance
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
                fiche = hub["biomasses"][biomasse]
                cellule = scenario.cellule(
                    pays, region, biomasse, mois, prng,
                    fiche=fiche, bassin=fiche["bassin"],
                )
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
                pp = cellule.get("pain_points", {})
                if pp.get("feux_actifs_detectes"):
                    evenements.append(
                        evenement(date, "firms", "brulage_actif_reel",
                                  "opportunite_approvisionnement + ciblage hub",
                                  "nb_feux=%d frp=%.1f MW ; source=%s" % (
                                      pp.get("nb_feux_reels", 0),
                                      pp.get("frp_total_mw", 0.0),
                                      pp.get("etiquette", "?")))
                    )
                meteo = cellule.get("meteo", {})
                if meteo.get("precipitations_mm", 0.0) > 60.0:
                    evenements.append(
                        evenement(date, "meteo", "mois_humide_surveillance",
                                  "lots maintenus sous surveillance humidite",
                                  "precip_mensuelles=%.1f mm ; source=%s" % (
                                      meteo["precipitations_mm"], meteo.get("etiquette", "?")))
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
        "trio": trio_id,
        "hub": hub_id,
        "pays": pays,
        "region": region,
        "annee": ANNEE,
        "graine": graine_run,
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


def _section_priorite_firms(lignes):
    """Section priorisation des bassins — brûlage actif réel si branché."""
    classement = firms.priorite_hubs()
    if classement:
        lignes.append("## Priorité des bassins — brûlage actif RÉEL (NASA FIRMS)")
        lignes.append("")
        lignes.append("| Bassin | Feux actifs (réel) | FRP total (MW) | Lecture |")
        lignes.append("| --- | --- | --- | --- |")
        for c in classement:
            lecture = "priorité haute" if c["nb_feux"] > 0 else "calme — fenêtre idéale pour valoriser sans urgence"
            lignes.append("| %s | %d | %.1f | %s |" % (
                c["bassin"], c["nb_feux"], c["frp_total_mw"], lecture))
        lignes.append("")
    else:
        lignes.append("## Priorité des bassins — brûlage actif")
        lignes.append("")
        lignes.append("Couche NASA FIRMS non branchée (pas de MAP_KEY locale) : ")
        lignes.append("repli sur les pain points SYNTHÉTIQUES du moteur de scénarios.")
        lignes.append("")


def rapport_run_markdown(runs):
    """Rapport markdown d'un run : un hub ou la flotte monde entière."""
    monde_complet = len(runs) > 1
    titre = "World Twin flotte monde %d" % runs[0]["annee"] if monde_complet \
        else "World Twin %s (%s) %d" % (runs[0]["hub"], runs[0]["pays"], runs[0]["annee"])
    lignes = []
    lignes.append("# Rapport de run — %s" % titre)
    lignes.append("")
    lignes.append("Étiquette : **%s** — registre de développement, valeurs non calibrées."
                  % runs[0]["etiquette_globale"])
    lignes.append("")

    lots_total = sum(r["lots_total"] for r in runs)
    fautes_total = sum(r["fautes_total"] for r in runs)
    evenements_total = sum(len(r["evenements"]) for r in runs)
    heures_indispo = sum(r["heures_indisponibles"] for r in runs)
    heures_dispo = sum(r["heures_disponibles"] for r in runs)
    dispo_globale = heures_dispo / (heures_dispo + heures_indispo) * 100.0

    lignes.append("## Synthèse")
    lignes.append("")
    lignes.append("- Hubs : %d. Trios : %d, %d opérateurs par trio (hypothèse v0)."
                  % (len(runs), len(runs), OPERATEURS_PAR_TRIO))
    lignes.append("- Lots simulés : %d. Fautes : %d. Événements : %d."
                  % (lots_total, fautes_total, evenements_total))
    lignes.append("- Disponibilité flotte : %.1f %% (disponible %.0f h, indisponible %.0f h)."
                  % (dispo_globale, heures_dispo, heures_indispo))
    lignes.append("")
    lignes.append("## KPI par hub")
    lignes.append("")
    lignes.append("| Hub | Pays | Région | Lots | Fautes | Disponibilité |")
    lignes.append("| --- | --- | --- | --- | --- | --- |")
    for r in runs:
        lignes.append("| %s | %s | %s | %d | %d | %.1f %% |" % (
            r["hub"], r["pays"], r["region"],
            r["lots_total"], r["fautes_total"], r["disponibilite_pct"]))
    lignes.append("")

    lignes.append("## Résumé mensuel (flotte, lots cumulés)")
    lignes.append("")
    lignes.append("| Mois | Lots | Fautes |")
    lignes.append("| --- | --- | --- |")
    for mois in range(1, 13):
        lots_mois = sum(m["lots"] for r in runs for m in r["resume_mensuel"] if m["mois"] == mois)
        fautes_mois = sum(m["fautes"] for r in runs for m in r["resume_mensuel"] if m["mois"] == mois)
        lignes.append("| %s | %d | %d |" % (MOIS_NOMS[mois - 1], lots_mois, fautes_mois))
    lignes.append("")

    _section_priorite_firms(lignes)

    lignes.append("## Journal fautes -> actions -> logs (extrait)")
    lignes.append("")
    lignes.append("| Horodatage | Hub | Module | Faute | Action | Log |")
    lignes.append("| --- | --- | --- | --- | --- | --- |")
    tous = []
    for r in runs:
        for e in r["evenements"]:
            tous.append((r["hub"], e))
    for hub, e in tous[:40]:
        lignes.append("| %s | %s | %s | %s | %s | %s |" % (
            e["timestamp"], hub, e["module"], e["faute"], e["action"], e["log"],
        ))
    if len(tous) > 40:
        lignes.append("")
        lignes.append("… et %d autres événements dans rapport-run.json." % (len(tous) - 40))
    lignes.append("")
    return "\n".join(lignes) + "\n"


def rapport_quotidien_exemple(runs):
    dernier_jour = []
    for r in runs:
        for e in r["evenements"][-5:]:
            dernier_jour.append((r["hub"], e))
    lignes = []
    lignes.append("# World Ops — rapport quotidien (exemple simulé)")
    lignes.append("")
    lignes.append("Étiquette : **%s**. Ce rapport est le gabarit de la tâche planifiée World Ops." % ETIQUETTE)
    lignes.append("")
    lignes.append("## État de la flotte")
    lignes.append("")
    for r in runs:
        lignes.append("- %s (%s, %s) : %d lots cumulés, disponibilité %.1f %%."
                      % (r["trio"], r["hub"], r["pays"], r["lots_total"], r["disponibilite_pct"]))
    lignes.append("")
    lignes.append("## Fautes -> actions -> logs (derniers événements)")
    lignes.append("")
    if dernier_jour:
        for hub, e in dernier_jour[-8:]:
            lignes.append("- %s — %s / %s : %s → %s (%s)" % (
                e["timestamp"], hub, e["module"], e["faute"], e["action"], e["log"]))
    else:
        lignes.append("- Aucune faute. Journée nominale.")
    lignes.append("")
    lignes.append("## Recommandations")
    lignes.append("")
    lignes.append("- Vérifier les fenêtres des biomasses actives du mois dans les cahiers pilotes.")
    lignes.append("- Confirmer les paramètres MTBF/MTTR avant le passage P3 (shadow mode réel).")
    lignes.append("- Rappel : toute donnée reste SYNTHÉTIQUE, registre de développement.")
    lignes.append("")
    return "\n".join(lignes) + "\n"


def main():
    argument = sys.argv[1] if len(sys.argv) > 1 else None
    if argument is None:
        hub_ids = list(monde.HUBS_MONDE)
    elif argument in monde.HUBS_MONDE:
        hub_ids = [argument]
    else:
        print("ERREUR : hub inconnu « %s ». Hubs disponibles : %s"
              % (argument, ", ".join(monde.HUBS_MONDE)))
        return 1

    runs = [simuler(hub_id) for hub_id in hub_ids]

    dossier_sorties = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sorties")
    dossier_sorties = os.path.normpath(dossier_sorties)
    os.makedirs(dossier_sorties, exist_ok=True)

    with open(os.path.join(dossier_sorties, "rapport-run.md"), "w", encoding="utf-8") as f:
        f.write(rapport_run_markdown(runs))

    runs_json = []
    telemetrie_globale = []
    for run in runs:
        run_json = dict(run)
        telemetrie_globale.extend(run["telemetrie"])
        del run_json["telemetrie"]
        runs_json.append(run_json)
    charge_json = {
        "etiquette_globale": ETIQUETTE,
        "mode": "monde" if len(runs) > 1 else runs[0]["hub"],
        "hubs": [r["hub"] for r in runs],
        "totaux": {
            "lots_total": sum(r["lots_total"] for r in runs),
            "fautes_total": sum(r["fautes_total"] for r in runs),
            "evenements_total": sum(len(r["evenements"]) for r in runs),
            "heures_indisponibles": round(sum(r["heures_indisponibles"] for r in runs), 1),
        },
        "runs": runs_json,
    }
    with open(os.path.join(dossier_sorties, "rapport-run.json"), "w", encoding="utf-8") as f:
        json.dump(charge_json, f, ensure_ascii=False, indent=2)
        f.write("\n")

    with open(os.path.join(dossier_sorties, "telemetrie-echantillon.json"), "w", encoding="utf-8") as f:
        json.dump(
            {"etiquette": ETIQUETTE, "contrat": "digital-twin/schemas/donnees-capteurs.schema.json",
             "enregistrements": telemetrie_globale[:120]},
            f, ensure_ascii=False, indent=2,
        )
        f.write("\n")

    with open(os.path.join(dossier_sorties, "rapport-quotidien-exemple.md"), "w", encoding="utf-8") as f:
        f.write(rapport_quotidien_exemple(runs))

    print(">> Run World Twin terminé (étiquette %s)" % ETIQUETTE)
    for r in runs:
        print(">> %-18s %-10s — %4d lots, %3d événements, dispo %.1f %%"
              % (r["trio"], r["pays"], r["lots_total"],
                 len(r["evenements"]), r["disponibilite_pct"]))
    print(">> Sorties : %s" % dossier_sorties)
    return 0


if __name__ == "__main__":
    sys.exit(main())
