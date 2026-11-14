#!/usr/bin/env python3
"""Couche P2.9 — atlas CaO : réactifs minéraux de captation, par hub.

Calcule, pour chaque hub de la flotte généralisée (217 hubs, 480 trios)
plus les hubs pilotes fr-rhone (1 trio) et ma-atlas (3 trios, Al-Atlas,
raccord V2.3.1, vitrine P2, hors totaux), la capacité locale en oxyde de
calcium (CaO) minéral disponible pour la captation, le besoin par trio
et le plan d'approvisionnement.

Chaîne documentaire, DONNÉES PUBLIQUES SOURCÉES :
- CKD (poussières de four à ciment, Cement Kiln Dust) : production et
  capacité clinker USGS MCS 2026 (kt), ratio 3 % de la production,
  50 % disponibles, 21,6 % de CaO utile ;
- laitier de haut fourneau : acier brut USGS MCS 2026 (Mt), 15 % de
  laitier, 30 % non valorisés, 25,0 % de CaO utile ;
- cendres de biomasse : bois rond industriel FAOSTAT 2024 (m³), densité
  0,65 t/m³, 2 % de cendres, 50 % récupérables, 13,0 % de CaO utile ;
- population 2023 Our World in Data : prorata des lignes « Autres
  pays » USGS vers chaque pays non listé (dénominateurs publics du
  snapshot cao-population-snapshot.json).

Les lignes « Autres pays » USGS sont ventILÉes au prorata de la
population : chaque pays non listé reçoit une part documentée, jamais
une valeur calibrée (doctrine PI, 00-gouvernance/GARDE_FOUS_PI.md).

Coûts PRIVÉS ILLUSTRATION (jamais publiés, jamais devant des
investisseurs) : prix de départ, proxy de distance et transport par
réactif, prix du marché externe pour le déficit. Le fichier public
cao-hubs-public.json ne contient AUCUN coût (contrôle anti-fuite du
verifier).

Étiquette de simulation : SYNTHÉTIQUE — registre de développement,
jamais le registre Merkle de production.

Commandes : generer | sommaire | verifier | table | pays [PAYS]
"""
import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(ICI), "data")

# --------------------------------------------------------------------------
# Constantes figées (doctrine P2.9, validée par Manu le 11/11/2026)
# --------------------------------------------------------------------------

RATIO_CKD = 0.03                    # CKD ≈ 3 % de la production clinker
PART_CKD_DISPONIBLE = 0.50          # 50 % captés/disponibles
FACTEUR_CKD = 0.216                 # t CO2 fixables par t de CKD

RATIO_LAITIER = 0.15                # laitier ≈ 15 % de l'acier brut
PART_LAITIER_NON_VALORISE = 0.30    # 30 % non valorisés (accessibles)
FACTEUR_LAITIER = 0.250             # t CO2 par t de laitier

DENSITE_BOIS = 0.65                 # t de bois par m³
PART_CENDRES = 0.02                 # 2 % de cendres à la combustion
PART_CENDRES_RECUPERABLES = 0.50    # 50 % récupérables
FACTEUR_CENDRES = 0.130             # t CO2 par t de cendres

STOECHIOMETRIE_CAO = 1.274          # t CaO par t CO2 (CaCO3 → CaO + CO2)
BESOIN_PAR_TRIO = 582.0             # t CO2 à fixer par trio et par an

SEUIL_AUTONOME = 1.2                # capacité/besoin
SEUIL_COUVERT = 0.8
SEUIL_PARTIEL = 0.3

# Coûts PRIVÉS ILLUSTRATION — jamais versionnés, jamais publiés.
PRIX_DEPART = {"ckd": 5.0, "laitier": 15.0, "cendres": 3.0}   # €/t
DISTANCE_PROXY = {"ckd": 65.0, "laitier": 85.0, "cendres": 40.0}  # km
TRANSPORT = 0.10                    # €/t/km
PRIX_MARCHE_EXTERNE = 90.0          # €/t CO2 (achat déficitaire)

ETIQUETTE = "SOURCÉ (USGS MCS 2026, FAOSTAT, OWID) + ratios ILLUSTRATION"
ETIQUETTE_SIMULATION = "SYNTHÉTIQUE"

# --------------------------------------------------------------------------
# Chargement des snapshots (données publiques, versionnées dans data/)
# --------------------------------------------------------------------------


def _charger(nom):
    with open(os.path.join(DATA, nom), encoding="utf-8") as f:
        return json.load(f)


_MEMO_PAYS = None
_MEMO_HUBS = None


def _referentiel():
    global _MEMO_PAYS
    if _MEMO_PAYS is None:
        _MEMO_PAYS = _charger("cao-pays-referentiel.json")["pays"]
    return _MEMO_PAYS


def capacites_nationales():
    """Par pays de la flotte : tonnes/an de CKD, laitier, cendres, capacité.

    Les pays listés USGS prennent leur ligne directe ; les autres
    reçoivent une part prorata population des lignes « Autres pays ».
    """
    referentiel = _referentiel()
    bois = _charger("cao-bois-faostat-snapshot.json")["pays"]
    population = _charger("cao-population-snapshot.json")
    industrie = _charger("cao-industrie-snapshot.json")

    bases = population["bases_prorata_usgs"]
    base_ciment = bases["ciment"]["base_non_listee"]
    base_acier = bases["acier"]["base_non_listee"]
    ciment_listes = industrie["ciment_kt"]["pays"]
    ciment_autres = industrie["ciment_kt"]["autres"][1]      # prod 2025, kt
    acier_listes = industrie["acier_mt"]["pays"]
    acier_autres = industrie["acier_mt"]["autres"][3]       # acier 2025e, Mt

    sortie = {}
    for pays, ref in referentiel.items():
        pop = population["pays"][ref["iso3"]]
        if pays in ciment_listes:
            ckd_t = (ciment_listes[pays][1] * 1000.0
                     * RATIO_CKD * PART_CKD_DISPONIBLE)
            note_ckd = "production USGS 2025 du pays"
        else:
            ckd_t = (ciment_autres * 1000.0
                     * RATIO_CKD * PART_CKD_DISPONIBLE
                     * pop / base_ciment)
            note_ckd = "part prorata population des « Autres pays » USGS"
        if pays in acier_listes:
            laitier_t = (acier_listes[pays][3] * 1.0e6
                         * RATIO_LAITIER * PART_LAITIER_NON_VALORISE)
            note_laitier = "acier brut USGS 2025e du pays"
        else:
            laitier_t = (acier_autres * 1.0e6
                         * RATIO_LAITIER * PART_LAITIER_NON_VALORISE
                         * pop / base_acier)
            note_laitier = ("part prorata population des « Autres pays »"
                            " USGS")
        cendres_t = (bois.get(pays, 0.0) * DENSITE_BOIS
                     * PART_CENDRES * PART_CENDRES_RECUPERABLES)
        capacite = (ckd_t * FACTEUR_CKD + laitier_t * FACTEUR_LAITIER
                    + cendres_t * FACTEUR_CENDRES)
        sortie[pays] = {
            "iso3": ref["iso3"], "population": pop,
            "ckd_t_an": ckd_t, "laitier_t_an": laitier_t,
            "cendres_t_an": cendres_t, "capacite_t_an": capacite,
            "notes": {"ckd": note_ckd, "laitier": note_laitier,
                      "cendres": "bois rond industriel FAOSTAT 2024"
                                 + ("" if bois.get(pays) else
                                    " — pays absent du bulk bois, "
                                    "capacité nulle documentée")},
        }
    return sortie


def _trios_par_hub():
    """Hubs généralisés (trios par hub) + hubs pilotes fr-rhone, ma-atlas."""
    import flotte_monde
    import monde
    hubs = {}
    for hid, h in flotte_monde.hubs_generalises()[0].items():
        hubs[hid] = {"pays": h["pays"],
                     "trios": h["_meta"]["trios"],
                     "hub_pilote": False}
    pilote = monde.HUBS_MONDE.get("fr-rhone")
    if pilote is not None:
        hubs["fr-rhone"] = {"pays": pilote["pays"], "trios": 1,
                            "hub_pilote": True}
    atlas = monde.HUBS_MONDE.get("ma-atlas")
    if atlas is not None:
        # Raccord V2.3.1 : 3 trios P2 Al-Atlas (MA-HUB-TRIO-1…3,
        # convention data/carte-monde.json). Le prorata national Maroc
        # passe de 3 à 6 trios au dénominateur : la capacité de
        # gen-maroc-1 est divisée par deux (ratio 37,30 → 18,65) sans
        # changer son statut AUTONOME — écart documenté au verifier.
        hubs["ma-atlas"] = {"pays": atlas["pays"], "trios": 3,
                            "hub_pilote": True}
    return hubs


def _cout_unitaire(reactif):
    """€ par tonne de CO2 fixée via ce réactif (PRIVÉ ILLUSTRATION)."""
    reactif_par_t_co2 = STOECHIOMETRIE_CAO / {
        "ckd": FACTEUR_CKD, "laitier": FACTEUR_LAITIER,
        "cendres": FACTEUR_CENDRES}[reactif]
    return reactif_par_t_co2 * (PRIX_DEPART[reactif]
                                + TRANSPORT * DISTANCE_PROXY[reactif])


def hubs_cao():
    """Détail CaO par hub : besoin, capacité par type, plan, coût, statut."""
    global _MEMO_HUBS
    if _MEMO_HUBS is not None:
        return _MEMO_HUBS
    nationales = capacites_nationales()
    hubs = _trios_par_hub()
    trios_pays = {}
    for h in hubs.values():
        trios_pays[h["pays"]] = trios_pays.get(h["pays"], 0) + h["trios"]

    detail = {}
    for hid, h in hubs.items():
        pays, trios = h["pays"], h["trios"]
        nat = nationales[pays]
        part = trios / trios_pays[pays]
        besoin = trios * BESOIN_PAR_TRIO
        caps_reactif = {"ckd": nat["ckd_t_an"] * part,
                        "laitier": nat["laitier_t_an"] * part,
                        "cendres": nat["cendres_t_an"] * part}
        facteurs = {"ckd": FACTEUR_CKD, "laitier": FACTEUR_LAITIER,
                    "cendres": FACTEUR_CENDRES}
        caps = {r: caps_reactif[r] * facteurs[r] for r in caps_reactif}
        capacite = sum(caps.values())
        # Merit order : CKD, cendres, laitier, puis marché externe.
        plan, reste = {}, besoin
        for reactif in ("ckd", "cendres", "laitier"):
            utilise = min(caps[reactif], reste)
            if utilise > 0:
                plan[reactif] = utilise
                reste -= utilise
        if reste > 0:
            plan["marche_externe"] = reste
        cout = sum(plan[r] * (_cout_unitaire(r)
                              if r != "marche_externe"
                              else PRIX_MARCHE_EXTERNE)
                   for r in plan)
        ratio = capacite / besoin if besoin else 0.0
        statut = ("AUTONOME" if ratio >= SEUIL_AUTONOME
                 else "COUVERT" if ratio >= SEUIL_COUVERT
                 else "PARTIEL" if ratio >= SEUIL_PARTIEL
                 else "A_SOURCER")
        detail[hid] = {
            "hub": hid, "pays": pays, "trios": trios,
            "hub_pilote": h["hub_pilote"],
            "besoin_t_an": besoin,
            "capacite_t_an": capacite,
            "capacite_ckd_t_an": caps["ckd"],
            "capacite_laitier_t_an": caps["laitier"],
            "capacite_cendres_t_an": caps["cendres"],
            "ratio": ratio, "statut": statut,
            "plan_achat_t_an": plan,
            "cout_eur_an": cout,
            "cout_eur_t": cout / besoin if besoin else 0.0,
            "etiquette": ETIQUETTE,
            "etiquette_simulation": ETIQUETTE_SIMULATION,
        }
    _MEMO_HUBS = detail
    return detail


def _totaux(detail):
    """Statistiques de référence : hubs généralisés SEULES (hors pilote)."""
    gen = [d for d in detail.values() if not d["hub_pilote"]]
    trios = sum(d["trios"] for d in gen)
    besoin = sum(d["besoin_t_an"] for d in gen)
    capacite = sum(d["capacite_t_an"] for d in gen)
    cout = sum(d["cout_eur_an"] for d in gen)
    statuts = {}
    for d in gen:
        statuts[d["statut"]] = statuts.get(d["statut"], 0) + 1
    return {"hubs": len(gen), "trios": trios,
            "besoin_t_an": besoin, "capacite_t_an": capacite,
            "cout_eur_an": cout,
            "cout_eur_t": cout / besoin if besoin else 0.0,
            "cout_eur_par_trio": cout / trios if trios else 0.0,
            "statuts": statuts}


# --------------------------------------------------------------------------
# Commandes
# --------------------------------------------------------------------------


def generer():
    """Écrit cao-hubs.json (PRIVÉ, jamais versionné) et la version publique."""
    detail = hubs_cao()
    totaux = _totaux(detail)
    prov = ("Réactifs minéraux par hub — chaîne documentaire publique "
            "(USGS MCS 2026, FAOSTAT bois 2024, OWID population 2023). "
            "Fichier PRIVÉ : coûts ILLUSTRATION et plans d'achat, "
            "JAMAIS versionnés (doctrine PI).")

    prive = {
        "provenance": {"date": "2026-11-14", "note": prov,
                       "etiquette": ETIQUETTE,
                       "etiquette_simulation": ETIQUETTE_SIMULATION,
                       "confidentialite": "PRIVÉ — jamais versionné"},
        "totaux_hubs_generalises": totaux,
        "hubs": detail,
    }
    chemin_prive = os.path.join(DATA, "cao-hubs.json")
    with open(chemin_prive, "w", encoding="utf-8") as f:
        json.dump(prive, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")

    # Version publique : ZÉRO coût, ZÉRO plan d'achat.
    public = {
        "provenance": {
            "date": "2026-11-14",
            "note": ("Réactifs minéraux par hub — chaîne documentaire "
                     "publique (USGS MCS 2026, FAOSTAT bois 2024, OWID "
                     "population 2023). Capacités et besoins par hub, "
                     "sans AUCUNE donnée économique privée. Versionné."),
            "etiquette": ETIQUETTE,
            "etiquette_simulation": ETIQUETTE_SIMULATION,
        },
        "totaux_hubs_generalises": {
            "hubs": totaux["hubs"], "trios": totaux["trios"],
            "besoin_t_an": round(totaux["besoin_t_an"], 1),
            "capacite_mt_co2_an": round(totaux["capacite_t_an"] / 1.0e6, 2),
            "statuts": totaux["statuts"],
        },
        "hubs": {},
    }
    for hid, d in detail.items():
        public["hubs"][hid] = {
            "pays": d["pays"], "trios": d["trios"],
            "hub_pilote": d["hub_pilote"],
            "besoin_t_an": d["besoin_t_an"],
            "capacite_t_an": round(d["capacite_t_an"] / 10.0) * 10.0,
            "ratio": round(d["ratio"], 2),
            "statut": d["statut"],
            "etiquette_simulation": ETIQUETTE_SIMULATION,
        }
    chemin_public = os.path.join(DATA, "cao-hubs-public.json")
    with open(chemin_public, "w", encoding="utf-8") as f:
        json.dump(public, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print("écrit : data/cao-hubs.json (PRIVÉ, jamais versionné)")
    print("écrit : data/cao-hubs-public.json (versionnable, zéro coût)")
    return 0


def sommaire():
    detail = hubs_cao()
    t = _totaux(detail)
    pilote = detail.get("fr-rhone")
    lignes = [
        "Atlas CaO World Twin (P2.9) — étiquette %s"
        % ETIQUETTE_SIMULATION,
        "",
        "- Hubs généralisés : %d (%d trios) ; hubs pilotes fr-rhone "
        "(1 trio) et ma-atlas (3 trios, Al-Atlas) : vitrine P2, "
        "hors totaux" % (t["hubs"], t["trios"]),
        "- Capacité mondiale (réactifs CaO) : %.1f Mt CO2/an"
        % (t["capacite_t_an"] / 1.0e6),
        "- Besoin : %.1f kt CO2/an (%.0f t par trio)"
        % (t["besoin_t_an"] / 1.0e3, BESOIN_PAR_TRIO),
        "- Coût privé ILLUSTRATION : %.1f M€/an = %.0f €/t = %.1f k€/trio "
        "(jamais publié)" % (t["cout_eur_an"] / 1.0e6, t["cout_eur_t"],
                             t["cout_eur_par_trio"] / 1.0e3),
        "- Statuts : %s" % " / ".join(
            "%d %s" % (t["statuts"].get(s, 0), s)
            for s in ("AUTONOME", "COUVERT", "PARTIEL", "A_SOURCER")),
        "- Chaîne : CKD (cimenteries USGS 2025), laitier (acier brut "
        "USGS 2025e), cendres (bois FAOSTAT 2024) — SOURCÉ public, "
        "ratios ILLUSTRATION",
    ]
    if pilote:
        lignes.append("- Témoin pilote fr-rhone : besoin %.0f t/an, "
                      "capacité %.0f t/an, statut %s"
                      % (pilote["besoin_t_an"], pilote["capacite_t_an"],
                         pilote["statut"]))
    atlas = detail.get("ma-atlas")
    if atlas:
        lignes.append("- Témoin pilote ma-atlas : besoin %.0f t/an, "
                      "capacité %.0f t/an, statut %s (prorata Maroc "
                      "partagé avec gen-maroc-1)"
                      % (atlas["besoin_t_an"], atlas["capacite_t_an"],
                         atlas["statut"]))
    lignes += [
        "",
        "Commandes : generer | sommaire | verifier | table | pays [PAYS]",
    ]
    return "\n".join(lignes) + "\n"


def _statut(ratio):
    return ("AUTONOME" if ratio >= SEUIL_AUTONOME
            else "COUVERT" if ratio >= SEUIL_COUVERT
            else "PARTIEL" if ratio >= SEUIL_PARTIEL else "A_SOURCER")


def verifier():
    """Contrôles : recomptages, témoins, statuts, anti-fuite, étiquettes."""
    rapports = []
    detail = hubs_cao()
    t = _totaux(detail)
    nationales = capacites_nationales()

    # 1. Recomptage du besoin et des statuts.
    assert t["trios"] == 481, t["trios"]
    assert abs(t["besoin_t_an"] - 481 * BESOIN_PAR_TRIO) < 1e-6
    rapports.append("besoin recompté : %d trios × %.0f t = %.1f kt/an OK"
                    % (t["trios"], BESOIN_PAR_TRIO,
                       t["besoin_t_an"] / 1.0e3))
    for hid, d in detail.items():
        attendu = _statut(d["ratio"])
        assert d["statut"] == attendu, (hid, d["statut"], attendu)
    rapports.append("statuts vs seuils %.1f/%.1f/%.1f : OK"
                    % (SEUIL_AUTONOME, SEUIL_COUVERT, SEUIL_PARTIEL))

    # 2. Capacité mondiale dans la plage doctrine.
    mt = t["capacite_t_an"] / 1.0e6
    assert 25.0 <= mt <= 45.0, mt
    rapports.append("capacité mondiale %.1f Mt CO2/an ∈ [25, 45] : OK" % mt)

    # 3. Cinq hubs témoins (prorata national exact).
    trios_pays = {}
    for d in detail.values():
        trios_pays[d["pays"]] = trios_pays.get(d["pays"], 0) + d["trios"]
    for hid in ("fr-rhone", "ma-atlas", "gen-maroc-1",
                "gen-belize-1", "gen-maurice-1", "gen-chine-1"):
        d = detail[hid]
        nat = nationales[d["pays"]]
        part = d["trios"] / trios_pays[d["pays"]]
        attendu = nat["capacite_t_an"] * part
        assert abs(d["capacite_t_an"] - attendu) < 1e-6, hid
        assert abs(d["besoin_t_an"] - d["trios"] * BESOIN_PAR_TRIO) < 1e-9
        rapports.append("témoin %-13s %s : %d trio(s), besoin %.0f t/an, "
                        "ratio %.2f, %s OK"
                        % (hid, d["pays"], d["trios"], d["besoin_t_an"],
                           d["ratio"], d["statut"]))
    assert detail["fr-rhone"]["hub_pilote"] is True
    assert detail["ma-atlas"]["hub_pilote"] is True
    rapports.append("hubs pilotes fr-rhone et ma-atlas hors totaux : OK")
    rapports.append("raccord ma-atlas (V2.3.1) : prorata Maroc 3 → 6 "
                    "trios, gen-maroc-1 ratio 37,30 → %.2f — statut "
                    "AUTONOME inchangé, écart documenté"
                    % detail["gen-maroc-1"]["ratio"])

    # 4. Anti-fuite : le fichier public ne contient AUCUN coût.
    chemin_public = os.path.join(DATA, "cao-hubs-public.json")
    if os.path.exists(chemin_public):
        with open(chemin_public, encoding="utf-8") as f:
            texte = f.read()
        for token in ("cout", "€", "prix", "plan_achat", "eur_t",
                      "eur_an", "marche_externe"):
            assert token not in texte, ("fuite : %s" % token)
        rapports.append("anti-fuite cao-hubs-public.json : "
                        "aucun coût, aucun plan d'achat : OK")
        # Étiquettes.
        for ch in (texte,):
            assert ETIQUETTE_SIMULATION in ch
    chemin_prive = os.path.join(DATA, "cao-hubs.json")
    if os.path.exists(chemin_prive):
        with open(chemin_prive, encoding="utf-8") as f:
            texte = f.read()
        assert ETIQUETTE_SIMULATION in texte
        rapports.append("étiquette %s présente (privé et public) : OK"
                        % ETIQUETTE_SIMULATION)

    rapports.append("VERDICT : OK (%d hubs généralisés + 2 pilotes, "
                    "%d AUTONOME)" % (t["hubs"], t["statuts"].get(
                        "AUTONOME", 0)))
    return rapports


def table():
    detail = hubs_cao()
    lignes = ["| Hub | Pays | Trios | Besoin (t/an) | Capacité (t/an) | "
              "Ratio | Statut |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    for hid in sorted(detail):
        d = detail[hid]
        lignes.append("| %s%s | %s | %d | %.0f | %.0f | %.2f | %s |" % (
            hid, " *" if d["hub_pilote"] else "", d["pays"], d["trios"],
            d["besoin_t_an"], d["capacite_t_an"], d["ratio"], d["statut"]))
    lignes.append("")
    lignes.append("* hub pilote, hors totaux.")
    return "\n".join(lignes) + "\n"


def pays_detail(nom_pays):
    nationales = capacites_nationales()
    if nom_pays not in nationales:
        return "Pays inconnu « %s » (voir data/cao-pays-referentiel.json)" \
            % nom_pays
    nat = nationales[nom_pays]
    detail = {hid: d for hid, d in hubs_cao().items()
              if d["pays"] == nom_pays}
    trios = sum(d["trios"] for d in detail.values())
    lignes = [
        "Pays : %s (%s, %d habitants 2023) — étiquette %s"
        % (nom_pays, nat["iso3"], nat["population"], ETIQUETTE),
        "",
        "- CKD : %.0f t/an (%s)" % (nat["ckd_t_an"], nat["notes"]["ckd"]),
        "- Laitier : %.0f t/an (%s)" % (nat["laitier_t_an"],
                                        nat["notes"]["laitier"]),
        "- Cendres : %.0f t/an (%s)" % (nat["cendres_t_an"],
                                        nat["notes"]["cendres"]),
        "- Capacité CaO : %.0f t CO2/an ; hubs : %d (%d trio(s))"
        % (nat["capacite_t_an"], len(detail), trios),
    ]
    for hid in sorted(detail):
        d = detail[hid]
        lignes.append("  - %s : besoin %.0f t/an, ratio %.2f, %s"
                      % (hid, d["besoin_t_an"], d["ratio"], d["statut"]))
    return "\n".join(lignes) + "\n"


def main():
    arguments = sys.argv[1:]
    if not arguments or arguments[0] == "sommaire":
        print(sommaire())
        return 0
    if arguments[0] == "generer":
        return generer()
    if arguments[0] == "verifier":
        for ligne in verifier():
            print(ligne)
        return 0
    if arguments[0] == "table":
        print(table())
        return 0
    if arguments[0] == "pays" and len(arguments) > 1:
        print(pays_detail(arguments[1]))
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
