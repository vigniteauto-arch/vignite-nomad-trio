#!/usr/bin/env python3
"""Couche P1 — figeage des paramètres opérationnels par trio (V2.3.1).

Fige, pour chaque trio de la flotte World Twin — les 481 trios des 217
hubs généralisés (engine/flotte_monde.py) et les 9 trios des 7 hubs
pilotes P2 (engine/monde.py, dont ma-atlas qui porte 3 trios,
convention data/carte-monde.json, raccord V2.3.1) — les paramètres
opérationnels déterministes :

  - 2 opérateurs tournants par équipe, une équipe couvrant jusqu'à
    5 trios (plafond figé du modèle IoT, flotte_monde.py) ;
  - MTBF (Mean Time Between Failures, temps moyen entre pannes)
    720 heures et MTTR (Mean Time To Repair, temps moyen de
    réparation) 8 heures — baseline figée V1.6, ILLUSTRATION non
    calibrée, variantes M1/M2/M3 éteintes ;
  - graine déterministe du hub et graine du trio (convention P1 :
    graine_trio = graine_hub + indice de trio - 1 ; le trio 1 garde
    exactement la graine du hub, compatibilité arrière avec
    simulateur.simuler) ;
  - fenêtre d'opération (union des fenêtres des biomasses du hub),
    mois de maintenance saisonnière (complément) et statut de fenêtre
    (CONTINUE si douze mois actifs, SAISONNIÈRE sinon) ;
  - pays, hub, équipe, étiquette SYNTHÉTIQUE.

Branchement des sources, vague P1 :
  - FAOSTAT (base statistique de l'Organisation des Nations unies pour
    l'alimentation et l'agriculture, FAO) : DÉJÀ BRANCHÉE — les hubs
    généralisés héritent des gisements et fenêtres du snapshot v18
    (data/gisements-faostat-snapshot-v18.json via flotte_monde.py) ;
  - GEOGLAM (Global Agricultural Geo-monitoring Initiative) : croisée
    au moteur P2.3 (engine/geoglam.py) pour les céréales AMIS ; les
    fenêtres candidates des cultures pérennes restent À SOURCER
    (curation manuelle, jamais ingérées avant sourcing complet) ;
  - Open-Meteo : pointage multi-points des hubs par
    engine/build_carte.py --meteo-hubs (fichier versionné
    data/meteo-hubs-pointage.json) ; le figeage n'en dépend pas ;
  - NASA FIRMS (Fire Information for Resource Management System de la
    National Aeronautics and Space Administration) : chaque hub
    généralisé enregistre sa zone GPS au moment de sa construction
    (firms.enregistrer_zone_gps, boîte ±1,0° latitude / ±1,5°
    longitude) — contrôlé au verifier.

AUCUN paramètre calibré du VDE (Vignite Decision Engine) : les
paramètres figés ici sont des conventions de simulation ILLUSTRATION,
jamais les coefficients réels (doctrine PI, hors du dépôt).

Étiquette de simulation : SYNTHÉTIQUE — registre de développement,
jamais le registre Merkle de production.

Sortie versionnée : data/parametres-trios.json — aucune donnée
économique, aucun secret (contrôle anti-fuite du verifier).

Commandes : generer | sommaire | verifier | table | trio [ID]
"""
import json
import math
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)

import flotte_monde                                    # noqa: E402 (engine/)
import monde                                           # noqa: E402 (engine/)
import simulateur                                      # noqa: E402 (engine/)
import firms                                           # noqa: E402 (engine/)

DATA = os.path.join(os.path.dirname(ICI), "data")

ETIQUETTE_SIMULATION = "SYNTHÉTIQUE"
ETIQUETTE = ("CONVENTIONS FIGÉES (vague P1) — ILLUSTRATION, aucun "
             "paramètre calibré du VDE")
TRIOS_PAR_EQUIPE = 5        # plafond figé de couverture d'une équipe
TRIOS_ATLAS = 3             # ma-atlas : 3 trios P2 (convention
                            # data/carte-monde.json, raccord V2.3.1)

JETONS_FUITE = ["cout", "€", "prix", "plan_achat", "eur_t", "eur_an",
                "marche_externe", "deficit", "map_key", "secret"]


# --------------------------------------------------------------------------
# Figeage
# --------------------------------------------------------------------------

def _fenetre_hub(hub):
    """Fenêtre d'opération du hub : union des fenêtres des biomasses."""
    actifs = set()
    for fiche in hub["biomasses"].values():
        actifs.update(fiche["fenetre_operation"])
    return sorted(actifs)


def _trios_du_hub(hid, hub, nb_trios, pilote):
    """Enregistrements figés des trios d'un hub (ordre déterministe)."""
    fenetre = _fenetre_hub(hub)
    maintenance = [m for m in range(1, 13) if m not in fenetre]
    statut_fenetre = "CONTINUE" if len(fenetre) == 12 else "SAISONNIÈRE"
    records = []
    for indice in range(1, nb_trios + 1):
        records.append({
            "trio": "%s-trio-%d" % (hid, indice),
            "hub": hid,
            "pays": hub["pays"],
            "region": hub["region"],
            "hub_pilote": pilote,
            "equipe": (indice - 1) // TRIOS_PAR_EQUIPE + 1,
            "operateurs_equipe": flotte_monde.EQUIPE_OPERATEURS,
            "graine_hub": hub["graine"],
            "graine_trio": hub["graine"] + indice - 1,
            "mtbf_h": simulateur.MTBF_HEURES,
            "mttr_h": simulateur.MTTR_HEURES,
            "fenetre_operation_mois": fenetre,
            "maintenance_mois": maintenance,
            "statut_fenetre": statut_fenetre,
            "etiquette": ETIQUETTE,
            "etiquette_simulation": ETIQUETTE_SIMULATION,
        })
    return records


def trios_figes():
    """Tous les trios figés de la flotte (ordre déterministe)."""
    gen, _, _ = flotte_monde.hubs_generalises()
    records = []
    for hid in sorted(gen):
        records.extend(_trios_du_hub(
            hid, gen[hid], gen[hid]["_meta"]["trios"], False))
    for hid in sorted(monde.HUBS_MONDE):
        nb = TRIOS_ATLAS if hid == "ma-atlas" else 1
        records.extend(_trios_du_hub(hid, monde.HUBS_MONDE[hid], nb, True))
    return records


def totaux(records):
    """Totaux de référence (généralisés et pilotes séparés)."""
    par_hub = {}
    for r in records:
        par_hub.setdefault(r["hub"], {"trios": 0, "pilote": r["hub_pilote"],
                                      "pays": r["pays"]})
        par_hub[r["hub"]]["trios"] += 1
    equipes = {}
    for r in records:
        equipes[(r["hub"], r["equipe"])] = True
    return {
        "hubs": len(par_hub),
        "hubs_generalises": sum(1 for h in par_hub.values()
                               if not h["pilote"]),
        "hubs_pilotes": sum(1 for h in par_hub.values() if h["pilote"]),
        "trios": len(records),
        "trios_generalises": sum(1 for r in records if not r["hub_pilote"]),
        "trios_pilotes": sum(1 for r in records if r["hub_pilote"]),
        "equipes": len(equipes),
        "operateurs": flotte_monde.EQUIPE_OPERATEURS * len(equipes),
        "mtbf_h": simulateur.MTBF_HEURES,
        "mttr_h": simulateur.MTTR_HEURES,
        "statuts_fenetre": {
            s: sum(1 for r in records if r["statut_fenetre"] == s)
            for s in ("CONTINUE", "SAISONNIÈRE")},
    }


def _charge():
    return {
        "provenance": {
            "date": "2026-11-14",
            "note": ("Paramètres opérationnels figés par trio — vague P1. "
                     "Conventions de simulation ILLUSTRATION, déterministes "
                     "(MTBF/MTTR baseline V1.6, 2 opérateurs tournants par "
                     "équipe de 5 trios max, graines par trio). Aucun "
                     "paramètre calibré du VDE. Versionné dans data/."),
            "etiquette": ETIQUETTE,
            "etiquette_simulation": ETIQUETTE_SIMULATION,
            "sources": {
                "faostat": ("branchée — snapshot v18 via "
                            "flotte_monde.hubs_generalises()"),
                "geoglam": ("croisée P2.3 céréales (engine/geoglam.py) ; "
                            "pérennes À SOURCER, curation manuelle"),
                "open_meteo": ("pointage multi-points via build_carte.py "
                               "--meteo-hubs, fichier "
                               "data/meteo-hubs-pointage.json"),
                "nasa_firms": ("zones GPS des hubs enregistrées via "
                               "firms.enregistrer_zone_gps (boîte "
                               "±1,0°/±1,5°)"),
            },
        },
        "totaux": totaux(trios_figes()),
        "trios": {r["trio"]: r for r in trios_figes()},
    }


# --------------------------------------------------------------------------
# Commandes
# --------------------------------------------------------------------------

def generer():
    """Écrit data/parametres-trios.json (versionné, sans secret)."""
    charge = _charge()
    chemin = os.path.join(DATA, "parametres-trios.json")
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(charge, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    t = charge["totaux"]
    print("écrit : data/parametres-trios.json (versionnable, %d trios — "
          "%d généralisés + %d pilotes)" % (t["trios"],
                                            t["trios_generalises"],
                                            t["trios_pilotes"]))
    print("figeage : MTBF %g h, MTTR %g h, %d opérateurs tournants par "
          "équipe de %d trios max" % (t["mtbf_h"], t["mttr_h"],
                                      flotte_monde.EQUIPE_OPERATEURS,
                                      TRIOS_PAR_EQUIPE))
    return 0


def sommaire():
    charge = _charge()
    t = charge["totaux"]
    print("Figeage P1 par trio — étiquette %s" % ETIQUETTE_SIMULATION)
    print("- Hubs : %d (%d généralisés + %d pilotes P2)"
          % (t["hubs"], t["hubs_generalises"], t["hubs_pilotes"]))
    print("- Trios : %d (%d généralisés + %d pilotes, ma-atlas 3 trios)"
          % (t["trios"], t["trios_generalises"], t["trios_pilotes"]))
    print("- Équipes : %d — opérateurs tournants : %d (%d par équipe, "
          "%d trios max par équipe)"
          % (t["equipes"], t["operateurs"], flotte_monde.EQUIPE_OPERATEURS,
             TRIOS_PAR_EQUIPE))
    print("- MTBF %g h, MTTR %g h (baseline V1.6, ILLUSTRATION)"
          % (t["mtbf_h"], t["mttr_h"]))
    print("- Fenêtres : %d SAISONNIÈRE, %d CONTINUE"
          % (t["statuts_fenetre"]["SAISONNIÈRE"],
             t["statuts_fenetre"]["CONTINUE"]))
    for exemple in ("fr-rhone-trio-1", "ma-atlas-trio-3", "gen-maroc-1-trio-1"):
        r = charge["trios"].get(exemple)
        if r:
            print("- Témoin %-20s %s — graine %d, équipe %d, fenêtre %s"
                  % (exemple, r["pays"], r["graine_trio"], r["equipe"],
                     "/".join(str(m) for m in r["fenetre_operation_mois"])))
    print("Commandes : generer | sommaire | verifier | table | trio [ID]")
    return 0


def verifier():
    """Contrôles : recomptages, conventions, FIRMS, anti-fuite, reprise."""
    erreurs = []

    def controle(ok, message):
        print("  %-4s %s" % ("OK" if ok else "ERREUR", message))
        if not ok:
            erreurs.append(message)

    print("— Contrôles figeage P1 —")
    charge = _charge()
    trios = charge["trios"]
    t = charge["totaux"]
    controle(len(trios) == 490, "490 trios (481 généralisés + 9 pilotes)")
    controle(t["trios_generalises"] == 481, "481 trios généralisés (V2.6 : +1 à gen-malaisie-1, EFB_PALMIER_MY)")
    controle(t["hubs_generalises"] == 217, "217 hubs généralisés")
    controle(t["hubs_pilotes"] == 7, "7 hubs pilotes P2")
    controle(t["trios_pilotes"] == 9, "9 trios pilotes (ma-atlas 3 trios)")
    controle(t["equipes"] == 217 + 7
             and t["operateurs"] == flotte_monde.EQUIPE_OPERATEURS
             * (217 + 7),
             "équipes %d, opérateurs %d (une équipe par hub : aucun hub ne "
             "dépasse %d trios)" % (t["equipes"], t["operateurs"],
                                    TRIOS_PAR_EQUIPE))
    controle(t["equipes"] - 7 == 217,
             "repère flotte : 217 équipes généralisées (434 opérateurs)")

    print("— Conventions par trio —")
    ok_params = all(r["mtbf_h"] == simulateur.MTBF_HEURES
                    and r["mttr_h"] == simulateur.MTTR_HEURES
                    and r["operateurs_equipe"] == flotte_monde.EQUIPE_OPERATEURS
                    for r in trios.values())
    controle(ok_params, "MTBF %g h, MTTR %g h, %d opérateurs sur chaque "
             "trio" % (simulateur.MTBF_HEURES, simulateur.MTTR_HEURES,
                       flotte_monde.EQUIPE_OPERATEURS))
    ok_graines = all(
        r["graine_trio"] == r["graine_hub"] + int(r["trio"].rsplit("-", 1)[1])
        - 1 for r in trios.values())
    controle(ok_graines, "graine_trio = graine_hub + indice − 1 sur chaque "
             "trio (trio 1 = graine du hub, compatibilité simulateur)")
    ok_fenetres = True
    for r in trios.values():
        union = set(r["fenetre_operation_mois"]) | set(r["maintenance_mois"])
        inter = set(r["fenetre_operation_mois"]) & set(r["maintenance_mois"])
        if union != set(range(1, 13)) or inter:
            ok_fenetres = False
            break
    controle(ok_fenetres, "fenêtre ∪ maintenance = 12 mois, sans "
             "chevauchement, sur chaque trio")
    controle(all(r["statut_fenetre"] == ("CONTINUE"
                 if len(r["fenetre_operation_mois"]) == 12 else "SAISONNIÈRE")
                 for r in trios.values()),
             "statut de fenêtre cohérent (CONTINUE ↔ 12 mois actifs)")
    pilote = trios.get("fr-rhone-trio-1")
    controle(pilote is not None
             and pilote["graine_trio"] == monde.HUBS_MONDE["fr-rhone"]["graine"],
             "témoin fr-rhone-trio-1 : graine du hub P2 inchangée")
    atlas = trios.get("ma-atlas-trio-3")
    controle(atlas is not None and atlas["graine_hub"] == 6042
             and atlas["graine_trio"] == 6044,
             "témoin ma-atlas-trio-3 : graines 6042 → 6044 (raccord V2.3.1)")
    controle(trios["ma-atlas-trio-1"]["fenetre_operation_mois"]
             == [1, 2, 12]
             and trios["ma-atlas-trio-1"]["maintenance_mois"]
             == [3, 4, 5, 6, 7, 8, 9, 10, 11],
             "témoin ma-atlas : fenêtre grignons d'olive décembre-janvier-"
             "février (triée [1, 2, 12]), maintenance mars à novembre")

    print("— Branchement des sources (vague P1) —")
    zones = sorted(firms.REGISTRE_ZONES)
    gen_ids = sorted({r["hub"] for r in trios.values()
                      if not r["hub_pilote"]})
    controle(zones == gen_ids,
             "NASA FIRMS : %d zones GPS enregistrées = hubs généralisés "
             "(firms.enregistrer_zone_gps via flotte_monde)" % len(zones))
    controle("faostat" in charge["provenance"]["sources"]
             and "geoglam" in charge["provenance"]["sources"]
             and "open_meteo" in charge["provenance"]["sources"]
             and "nasa_firms" in charge["provenance"]["sources"],
             "provenance : quatre sources documentées (FAOSTAT branchée, "
             "GEOGLAM curation manuelle, Open-Meteo pointage, NASA FIRMS "
             "zones)")

    print("— Anti-fuite et reproductibilité —")
    chemin = os.path.join(DATA, "parametres-trios.json")
    if os.path.exists(chemin):
        texte = open(chemin, encoding="utf-8").read()
        fuites = [j for j in JETONS_FUITE if j in texte]
        controle(not fuites, "parametres-trios.json sans jeton interdit "
                 "(%s)" % ", ".join(fuites) if fuites else "aucun")
        attendu = json.dumps(charge, ensure_ascii=False, indent=1,
                            sort_keys=True) + "\n"
        controle(texte == attendu, "reprise octet par octet : le fichier "
                 "versionné correspond au figeage courant")
    else:
        controle(False, "parametres-trios.json absent — lancer generer")
    controle(ETIQUETTE_SIMULATION in json.dumps(charge, ensure_ascii=False),
             "étiquette SYNTHÉTIQUE présente")

    if erreurs:
        print("\nVERDICT : %d erreur(s)." % len(erreurs))
        for e in erreurs:
            print("  - %s" % e)
        return 1
    print("\nVERDICT : OK (490 trios figés, sources P1 documentées).")
    return 0


def table():
    charge = _charge()
    records = sorted(charge["trios"].values(),
                     key=lambda r: (r["hub_pilote"], r["hub"], r["trio"]))
    print("%-26s %-13s %-11s %6s %6s %12s"
          % ("trio", "pays", "fenêtre", "équ.", "graine", "statut"))
    for r in records:
        print("%-26s %-13s %-11s %6d %6d %12s"
              % (r["trio"], r["pays"][:13],
                 "/".join(str(m) for m in r["fenetre_operation_mois"]),
                 r["equipe"], r["graine_trio"], r["statut_fenetre"]))


def trio_detail(ident):
    charge = _charge()
    r = charge["trios"].get(ident)
    if r is None:
        print("Trio inconnu « %s » (voir data/parametres-trios.json)." % ident)
        return 1
    print("Trio : %s" % r["trio"])
    print("Hub : %s%s — %s (%s)" % (r["hub"],
                                    " (pilote P2)" if r["hub_pilote"] else "",
                                    r["region"], r["pays"]))
    print("Équipe %d — %d opérateurs tournants"
          % (r["equipe"], r["operateurs_equipe"]))
    print("Graine hub %d — graine trio %d" % (r["graine_hub"],
                                             r["graine_trio"]))
    print("MTBF %g h, MTTR %g h" % (r["mtbf_h"], r["mttr_h"]))
    print("Fenêtre d'opération : %s — maintenance : %s (%s)"
          % ("/".join(str(m) for m in r["fenetre_operation_mois"]),
             "/".join(str(m) for m in r["maintenance_mois"]),
             r["statut_fenetre"]))
    print("Étiquette : %s" % r["etiquette"])
    return 0


def main():
    arguments = sys.argv[1:]
    if not arguments or arguments[0] == "sommaire":
        return sommaire()
    if arguments[0] == "generer":
        return generer()
    if arguments[0] == "verifier":
        return verifier()
    if arguments[0] == "table":
        table()
        return 0
    if arguments[0] == "trio" and len(arguments) > 1:
        return trio_detail(arguments[1])
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
