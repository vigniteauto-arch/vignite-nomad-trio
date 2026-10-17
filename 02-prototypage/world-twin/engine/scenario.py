"""Couche 3 — Moteur de scénarios World Twin (squelette non calibré).

Génère de façon déterministe les paramètres d'une cellule
(pays, région, biomasse, mois) : gisement, saisonnalité, météo
synthétique, pain points locaux (brûlage, réglementation).

RÈGLES :
- Aucune valeur calibrée : tout est ILLUSTRATION jusqu'au branchement
  des sources FAOSTAT / FIRMS / Open-Meteo / GEOGLAM (P1).
- Déterminisme complet : la graine suffit à reproduire un run.
- Sorties étiquetées SYNTHÉTIQUE — registre de développement,
  jamais le registre de production.
"""

# Générateur pseudo-aléatoire déterministe (LCG 32 bits, Numerical Recipes).
# Suffisant pour la simulation de charge ; remplacé par un vrai flux
# de données monde en P1.


class Prng:
    """Générateur déterministe minimal, reproductible par graine."""

    def __init__(self, graine):
        self._etat = graine & 0xFFFFFFFF

    def suivant(self):
        self._etat = (1664525 * self._etat + 1013904223) & 0xFFFFFFFF
        return self._etat

    def uniforme(self):
        return self.suivant() / 4294967296.0

    def intervalle(self, bas, haut):
        return bas + (haut - bas) * self.uniforme()

    def entier(self, bas, haut):
        return bas + self.suivant() % (haut - bas + 1)


# ---------------------------------------------------------------------------
# Pilote France v0 — cinq biomasses (ILLUSTRATION, à sourcer FAOSTAT/GEOGLAM)
# ---------------------------------------------------------------------------

BIOMASSES_PILOTE = {
    "sarments-vigne": {
        "bassin": "vallee-du-rhone",
        "fenetre_operation": [1, 2, 3, 4],   # janvier à avril
        "charge_mois": {1: "haute", 2: "haute", 3: "moyenne", 4: "fin"},
        "humidite_pct": (35.0, 55.0),  # ILLUSTRATION, non calibré
    },
    "marc-raisin": {
        "bassin": "vallee-du-rhone",
        "fenetre_operation": [9, 10, 11],  # septembre à novembre
        "charge_mois": {9: "haute", 10: "moyenne", 11: "fin"},
        "humidite_pct": (55.0, 75.0),
    },
    "mais-rdm": {
        "bassin": "sud-ouest",
        "fenetre_operation": [10, 11, 12],  # octobre à décembre
        "charge_mois": {10: "haute", 11: "moyenne", 12: "fin"},
        "humidite_pct": (15.0, 35.0),
    },
    "paille-riz": {
        "bassin": "camargue",
        "fenetre_operation": [10, 11, 12],  # octobre à décembre
        "charge_mois": {10: "haute", 11: "moyenne", 12: "fin"},
        "humidite_pct": (12.0, 28.0),
    },
    "coques-noix": {
        "bassin": "perigord",
        "fenetre_operation": [10, 11, 12, 1, 2],  # octobre à février
        "charge_mois": {10: "haute", 11: "moyenne", 12: "moyenne", 1: "fin", 2: "fin"},
        "humidite_pct": (10.0, 22.0),
    },
}

# Mois d'arrêt saisonnier : maintenance préventive simulée.
MOIS_MAINTENANCE = (5, 6, 7, 8)

# Coefficients de charge ILLUSTRATION (non calibrés).
FACTEUR_CHARGE = {"haute": 1.0, "moyenne": 0.6, "fin": 0.25}


def biomasses_du_mois(mois):
    """Biomasses dont la fenêtre d'opération couvre ce mois."""
    if mois in MOIS_MAINTENANCE:
        return []
    return [
        nom
        for nom, fiche in BIOMASSES_PILOTE.items()
        if mois in fiche["fenetre_operation"]
    ]


def gisement_illustration(biomasse, mois, prng):
    """Gisement simulé en tonnes pour le mois — ILLUSTRATION, non calibré.

    À remplacer en P1 par FAOSTAT (production et résidus, méthode IPCC).
    """
    charge = BIOMASSES_PILOTE[biomasse]["charge_mois"].get(mois, "moyenne")
    facteur = FACTEUR_CHARGE.get(charge, 0.5)
    return round(60.0 * facteur * prng.intervalle(0.8, 1.2), 1)


def meteo_synthetique(mois, jour, prng):
    """Météo synthétique — ILLUSTRATION.

    À remplacer en P1 par Open-Meteo (réanalyse ERA5 historique).
    """
    temperature_c = round(prng.intervalle(2.0, 26.0), 1)
    humidite_air_pct = round(prng.intervalle(45.0, 95.0), 1)
    pluie_mm = round(prng.uniforme() * (8.0 if mois in (1, 2, 3, 10, 11, 12) else 3.0), 1)
    return {
        "temperature_c": temperature_c,
        "humidite_air_pct": humidite_air_pct,
        "pluie_mm": pluie_mm,
        "etiquette": "SYNTHÉTIQUE",
    }


def pain_points(biomasse, mois, prng):
    """Pain points locaux simulés — ILLUSTRATION.

    À remplacer en P1 par NASA FIRMS (feux actifs GPS) et fiches pays
    (réglementation du brûlage).
    """
    feux_actifs_detectes = prng.uniforme() < 0.25
    brulage_reglemente = prng.uniforme() < 0.5
    return {
        "feux_actifs_detectes": feux_actifs_detectes,
        "brulage_reglemente": brulage_reglemente,
        "etiquette": "SYNTHÉTIQUE",
    }


def cellule(pays, region, biomasse, mois, prng):
    """Assemble les paramètres d'une cellule (pays, région, biomasse, mois)."""
    return {
        "pays": pays,
        "region": region,
        "biomasse": biomasse,
        "mois": mois,
        "gisement_t": gisement_illustration(biomasse, mois, prng),
        "humidite_pct": round(
            prng.intervalle(*BIOMASSES_PILOTE[biomasse]["humidite_pct"]), 1
        ),
        "etiquette": "SYNTHÉTIQUE",
    }
