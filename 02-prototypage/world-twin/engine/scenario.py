"""Couche 3 — Moteur de scénarios World Twin (squelette non calibré).

Génère de façon déterministe les paramètres d'une cellule
(pays, région, biomasse, mois) : gisement, saisonnalité, météo
synthétique, pain points locaux (brûlage, réglementation).

RÈGLES :
- Aucune valeur calibrée : tout est ILLUSTRATION jusqu'au branchement
  des sources FAOSTAT / FIRMS / GEOGLAM (P2).
- v0.2 : si cache-meteo/agregats-mensuels.json est présent, la météo
  vient du RÉEL (Open-Meteo ERA5, agrégations mensuelles) ; sinon
  repli synthétique déterministe.
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


import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import firms

CHEMIN_CACHE = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "cache-meteo", "agregats-mensuels.json"
))

_cache_meteo = None


def _charger_cache_meteo():
    """Charge le cache ERA5 (agregats mensuels) si présent, sinon {}."""
    global _cache_meteo
    if _cache_meteo is None:
        try:
            with open(CHEMIN_CACHE, encoding="utf-8") as f:
                _cache_meteo = json.load(f).get("bassins", {})
        except Exception:
            _cache_meteo = {}
    return _cache_meteo


def meteo_du_bassin(bassin, mois, prng):
    """Météo du bassin pour le mois : RÉELLE si cache ERA5 présent, sinon synthétique."""
    cache = _charger_cache_meteo()
    entrees = [
        v for cle, v in cache.get(bassin, {}).items()
        if int(cle[-2:]) == mois
    ]
    if entrees:
        return {
            "temperature_moy_c": round(sum(e["temperature_moy_c"] for e in entrees) / len(entrees), 1),
            "humidite_moy_pct": round(sum(e["humidite_moy_pct"] for e in entrees) / len(entrees), 1),
            "precipitations_mm": round(sum(e["precipitations_mm"] for e in entrees) / len(entrees), 1),
            "etiquette": "DONNÉES RÉELLES (Open-Meteo ERA5)",
        }
    return meteo_synthetique(mois, 1, prng)


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


def gisement_illustration(biomasse, mois, prng, fiche=None):
    """Gisement simulé en tonnes pour le mois — ILLUSTRATION, non calibré.

    À remplacer en P1 par FAOSTAT (production et résidus, méthode IPCC).
    v0.4 : fiche optionnelle (hubs du monde — engine/monde.py) ; défaut
    = pilote France.
    """
    if fiche is None:
        fiche = BIOMASSES_PILOTE[biomasse]
    charge = fiche["charge_mois"].get(mois, "moyenne")
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


def pain_points(biomasse, mois, prng, bassin=None):
    """Pain points locaux : feux actifs RÉELS si FIRMS est branchée.

    v0.3 : avec une MAP_KEY locale (firms.env), les feux actifs viennent
    de NASA FIRMS (VIIRS NOAA-20, NRT) — DONNÉES RÉELLES du jour.
    Sans clé : repli synthétique déterministe (ILLUSTRATION).
    v0.4 : bassin optionnel (hubs du monde — engine/monde.py) ; défaut
    = pilote France. La dimension réglementaire du brûlage reste
    ILLUSTRATION (fiches pays à sourcer).
    v0.6 (V1.8, 31/10/2026) : les deux tirages du générateur sont
    effectués AVANT le branchement FIRMS, dans le même ordre dans les
    deux chemins — le flux pseudo-aléatoire reste strictement identique
    avec ou sans MAP_KEY. Les pain points réels n'altèrent que la
    narration (événements firms du run), jamais les lots, fautes ni
    disponibilité : la série historique reste comparable.
    """
    if bassin is None:
        bassin = BIOMASSES_PILOTE[biomasse]["bassin"]
    tirage_feux = prng.uniforme()
    tirage_brulage = prng.uniforme()
    feux = firms.feux_bassin(bassin)
    if feux is not None:
        return {
            "feux_actifs_detectes": feux["nb_feux"] > 0,
            "nb_feux_reels": feux["nb_feux"],
            "frp_total_mw": feux["frp_total_mw"],
            "brulage_reglemente": tirage_brulage < 0.5,
            "etiquette": "DONNÉES RÉELLES (NASA FIRMS)",
        }
    return {
        "feux_actifs_detectes": tirage_feux < 0.25,
        "brulage_reglemente": tirage_brulage < 0.5,
        "etiquette": "SYNTHÉTIQUE",
    }


def cellule(pays, region, biomasse, mois, prng, fiche=None, bassin=None):
    """Assemble les paramètres d'une cellule (pays, région, biomasse, mois).

    v0.4 : fiche et bassin optionnels (hubs du monde — engine/monde.py) ;
    par défaut, le pilote France (BIOMASSES_PILOTE). L'ordre des
    tirages déterministes est inchangé — compatibilité v0.3.
    """
    if fiche is None:
        fiche = BIOMASSES_PILOTE[biomasse]
    if bassin is None:
        bassin = fiche["bassin"]
    return {
        "pays": pays,
        "region": region,
        "biomasse": biomasse,
        "mois": mois,
        "gisement_t": gisement_illustration(biomasse, mois, prng, fiche),
        "humidite_pct": round(
            prng.intervalle(*fiche["humidite_pct"]), 1
        ),
        "meteo": meteo_du_bassin(bassin, mois, prng),
        "pain_points": pain_points(biomasse, mois, prng, bassin),
        "etiquette": "SYNTHÉTIQUE",
    }
