"""Couche P2 — grammaire mondiale des hubs World Twin (squelette non calibré).

Définit la flotte mondiale simulée « as if in operation » : Carré d'Or
(France, Suisse, Italie, Espagne), LatAm (Argentine — Cuyo et Misiones),
Al-Atlas (Maroc). Chaque hub porte ses biomasses, leur saisonnalité
(hémisphère Sud inclus) et sa graine déterministe.

RÈGLES :
- Aucune valeur calibrée : charges, humidités et fenêtres sont
  ILLUSTRATION, à sourcer FAOSTAT / GEOGLAM / fiches pays en P2+.
- Les mois de maintenance saisonnière sont DÉDUITS des fenêtres :
  un mois sans biomasse active est un mois de maintenance.
- Le hub fr-rhone réplique exactement le pilote France v0.3 (mêmes
  biomasses, même graine) — la compatibilité arrière est un test.
- Tout résultat reste étiqueté SYNTHÉTIQUE, registre de développement.
"""

HUBS_MONDE = {
    "fr-rhone": {
        "pays": "France",
        "region": "pilote-v0 (Vallée du Rhône, Camargue, Sud-Ouest, Périgord)",
        "trio_id": "fr-hub01-trio-1",
        "graine": 42,
        "biomasses": {
            "sarments-vigne": {
                "bassin": "vallee-du-rhone",
                "fenetre_operation": [1, 2, 3, 4],
                "charge_mois": {1: "haute", 2: "haute", 3: "moyenne", 4: "fin"},
                "humidite_pct": (35.0, 55.0),
            },
            "marc-raisin": {
                "bassin": "vallee-du-rhone",
                "fenetre_operation": [9, 10, 11],
                "charge_mois": {9: "haute", 10: "moyenne", 11: "fin"},
                "humidite_pct": (55.0, 75.0),
            },
            "mais-rdm": {
                "bassin": "sud-ouest",
                "fenetre_operation": [10, 11, 12],
                "charge_mois": {10: "haute", 11: "moyenne", 12: "fin"},
                "humidite_pct": (15.0, 35.0),
            },
            "paille-riz": {
                "bassin": "camargue",
                "fenetre_operation": [10, 11, 12],
                "charge_mois": {10: "haute", 11: "moyenne", 12: "fin"},
                "humidite_pct": (12.0, 28.0),
            },
            "coques-noix": {
                "bassin": "perigord",
                "fenetre_operation": [10, 11, 12, 1, 2],
                "charge_mois": {10: "haute", 11: "moyenne", 12: "moyenne", 1: "fin", 2: "fin"},
                "humidite_pct": (10.0, 22.0),
            },
        },
    },
    "ch-leman": {
        "pays": "Suisse",
        "region": "Lavaux-Léman (Carré d'Or)",
        "trio_id": "ch-leman-trio-1",
        "graine": 1042,
        "biomasses": {
            "sarments-vigne": {
                "bassin": "suisse-leman",
                "fenetre_operation": [1, 2, 3],
                "charge_mois": {1: "haute", 2: "moyenne", 3: "fin"},
                "humidite_pct": (35.0, 55.0),
            },
            "marc-raisin": {
                "bassin": "suisse-leman",
                "fenetre_operation": [10, 11],
                "charge_mois": {10: "haute", 11: "fin"},
                "humidite_pct": (55.0, 75.0),
            },
        },
    },
    "it-puglia": {
        "pays": "Italie",
        "region": "Puglia-Tavoliere (Foggia)",
        "trio_id": "it-puglia-trio-1",
        "graine": 2042,
        "biomasses": {
            "grignons-olive": {
                "bassin": "italie-puglia",
                "fenetre_operation": [11, 12, 1],
                "charge_mois": {11: "haute", 12: "moyenne", 1: "fin"},
                "humidite_pct": (35.0, 60.0),
            },
            "sarments-vigne": {
                "bassin": "italie-puglia",
                "fenetre_operation": [2, 3],
                "charge_mois": {2: "haute", 3: "fin"},
                "humidite_pct": (35.0, 55.0),
            },
        },
    },
    "es-extremadura": {
        "pays": "Espagne",
        "region": "Estrémadure",
        "trio_id": "es-extremadura-trio-1",
        "graine": 3042,
        "biomasses": {
            "grignons-olive": {
                "bassin": "espagne-extremadure",
                "fenetre_operation": [11, 12, 1, 2],
                "charge_mois": {11: "haute", 12: "haute", 1: "moyenne", 2: "fin"},
                "humidite_pct": (35.0, 60.0),
            },
            "sarments-vigne": {
                "bassin": "espagne-extremadure",
                "fenetre_operation": [3, 4],
                "charge_mois": {3: "haute", 4: "fin"},
                "humidite_pct": (35.0, 55.0),
            },
        },
    },
    "ar-cuyo": {
        "pays": "Argentine",
        "region": "Cuyo-Mendoza (LatAm — hémisphère Sud)",
        "trio_id": "ar-cuyo-trio-1",
        "graine": 4042,
        "biomasses": {
            "restos-poda": {
                "bassin": "argentine-cuyo",
                "fenetre_operation": [6, 7, 8],
                "charge_mois": {6: "haute", 7: "moyenne", 8: "fin"},
                "humidite_pct": (30.0, 55.0),
            },
        },
    },
    "ar-misiones": {
        "pays": "Argentine",
        "region": "Misiones (LatAm — hémisphère Sud)",
        "trio_id": "ar-misiones-trio-1",
        "graine": 5042,
        "biomasses": {
            "yerba-mate": {
                "bassin": "argentine-misiones",
                "fenetre_operation": [4, 5, 6, 9, 10, 11],
                "charge_mois": {4: "moyenne", 5: "haute", 6: "haute",
                                 9: "haute", 10: "moyenne", 11: "fin"},
                "humidite_pct": (20.0, 40.0),
            },
        },
    },
    "ma-atlas": {
        "pays": "Maroc",
        "region": "Al-Atlas (Meknès)",
        "trio_id": "ma-atlas-trio-1",
        "graine": 6042,
        "biomasses": {
            "grignons-olive": {
                "bassin": "maroc-atlas",
                "fenetre_operation": [12, 1, 2],
                "charge_mois": {12: "haute", 1: "haute", 2: "fin"},
                "humidite_pct": (35.0, 60.0),
            },
        },
    },
}


def mois_maintenance(hub):
    """Mois de maintenance saisonnière : mois sans biomasse active.

    Pour le hub France, cette déduction redonne exactement (5, 6, 7, 8)
    du pilote v0.3 — compatibilité arrière par construction.
    """
    actifs = set()
    for fiche in hub["biomasses"].values():
        actifs.update(fiche["fenetre_operation"])
    return tuple(m for m in range(1, 13) if m not in actifs)


def biomasses_du_mois(hub, mois):
    """Biomasses du hub dont la fenêtre couvre ce mois (ordre stable)."""
    return [
        nom for nom, fiche in hub["biomasses"].items()
        if mois in fiche["fenetre_operation"]
    ]


def bassins_des_hubs():
    """Tous les bassins du monde, sans doublon, ordre stable."""
    vus = []
    for hub in HUBS_MONDE.values():
        for fiche in hub["biomasses"].values():
            b = fiche["bassin"]
            if b not in vus:
                vus.append(b)
    return vus
