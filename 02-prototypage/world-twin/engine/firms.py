"""Couche 1 — NASA FIRMS : feux actifs réels et priorisation des hubs.

Récupère les détections de feux actifs (VIIRS NOAA-20, Near Real Time)
par bassin pilote, via l'API FIRMS. Met en cache les résultats pour la
journée (une seule requête réseau par bassin et par jour de run).

CLÉ (RÈGLES) :
- La MAP_KEY est un SECRET : jamais versionnée, jamais dans le dépôt.
- Elle est lue depuis la variable d'environnement FIRMS_MAP_KEY, ou
  depuis le fichier local `firms.env` à la racine du dossier world-twin
  (exclu du dépôt par le motif *.env du .gitignore). Voir
  firms.env.example.
- Sans clé : repli — le moteur de scénarios utilise ses pain points
  synthétiques déterministes (aucune panne).

V1.8 (31/10/2026) — hubs généralisés : chaque hub de la flotte
généralisée (engine/flotte_monde.py) enregistre sa zone GPS au moment
de sa construction (boîte ±1.0° latitude / ±1.5° longitude autour du
centre du cluster, même convention que firms_nrt.py). Avec une clé,
ses pain points deviennent des feux RÉELS. Limite officielle de l'API
FIRMS : 5 000 transactions par intervalle de 10 minutes — le circuit
complet (10 bassins P2 + 81 hubs) consomme 91 requêtes par jour.

DONNÉES : NASA FIRMS, domaine public, agrégations par bassin. Les
détails bruts sont mis en cache local (cache-firms/, jamais versionné) ;
seules les agrégations non sensibles sont manipulées.
"""

import csv
import io
import json
import os
import urllib.request
from datetime import datetime, timezone

DOSSIER = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."))
CHEMIN_CLE = os.path.join(DOSSIER, "firms.env")
DOSSIER_CACHE = os.path.join(DOSSIER, "cache-firms")
API = "https://firms.modaps.eosdis.nasa.gov/api/area/csv/{cle}/VIIRS_NOAA20_NRT/{boite}/{jours}"

# Boîtes géographiques des bassins pilotes et du monde P2 (ouest, sud, est, nord).
BOITES_BASSINS = {
    # Pilote France (v0.3)
    "vallee-du-rhone": (4.40, 43.90, 5.30, 44.50),
    "camargue":        (3.50, 43.20, 5.50, 44.30),
    "perigord":        (0.20, 44.70, 1.20, 45.30),
    "sud-ouest":       (-1.00, 43.60, 0.00, 44.50),
    # Carré d'Or, LatAm, Al-Atlas (P2)
    "suisse-leman":       (6.40, 46.30, 7.20, 46.75),
    "italie-puglia":      (15.30, 40.70, 16.60, 41.70),
    "espagne-extremadure": (-6.60, 38.70, -5.00, 39.60),
    "argentine-cuyo":     (-69.60, -34.20, -67.40, -32.50),
    "argentine-misiones": (-55.80, -27.80, -54.30, -26.40),
    "maroc-atlas":        (-6.20, 32.90, -4.60, 34.20),
}

# Zones des hubs généralisés, enregistrées au runtime par
# engine/flotte_monde.py (boîte GPS autour du centre du cluster).
REGISTRE_ZONES = {}


def enregistrer_zone(nom, boite):
    """Enregistre la boîte (ouest, sud, est, nord) d'une zone nommée."""
    REGISTRE_ZONES[nom] = tuple(float(v) for v in boite)


def enregistrer_zone_gps(nom, lat, lon, demi_lat=1.0, demi_lon=1.5):
    """Enregistre une zone par point GPS — même convention que firms_nrt."""
    enregistrer_zone(nom, (lon - demi_lon, lat - demi_lat,
                           lon + demi_lon, lat + demi_lat))


_memoire = {}


def cle_disponible():
    """Retourne la MAP_KEY si elle est disponible, sinon None."""
    cle = os.environ.get("FIRMS_MAP_KEY", "").strip()
    if cle:
        return cle
    try:
        with open(CHEMIN_CLE, encoding="utf-8") as f:
            for ligne in f:
                ligne = ligne.strip()
                if ligne and not ligne.startswith("#"):
                    return ligne
    except OSError:
        pass
    return None


def _lire_cache(bassin, jour):
    chemin = os.path.join(DOSSIER_CACHE, "%s-%s.json" % (bassin, jour))
    try:
        with open(chemin, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def _ecrire_cache(bassin, jour, donnees):
    os.makedirs(DOSSIER_CACHE, exist_ok=True)
    chemin = os.path.join(DOSSIER_CACHE, "%s-%s.json" % (bassin, jour))
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=1)
        f.write("\n")


def feux_bassin(bassin, jours=1, aujourdhui=None):
    """Agrégat des feux actifs d'un bassin : nombre, FRP total et max.

    Retourne None si la clé est absente ou si la requête échoue
    (repli synthétique côté moteur). Sinon un dict étiqueté
    DONNÉES RÉELLES.
    """
    cle = cle_disponible()
    if not cle:
        return None
    jour = aujourdhui or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    memo = _memoire.get((bassin, jour, jours))
    if memo is not None:
        return memo
    zone = BOITES_BASSINS.get(bassin) or REGISTRE_ZONES.get(bassin)
    if zone is None:
        return None
    resultat = _lire_cache(bassin, jour)
    if resultat is None:
        boite = ",".join("%g" % v for v in zone)
        url = API.format(cle=cle, boite=boite, jours=jours)
        try:
            with urllib.request.urlopen(url, timeout=25) as reponse:
                texte = reponse.read().decode("utf-8")
        except Exception:
            return None
        lignes = list(csv.DictReader(io.StringIO(texte)))
        frp = [float(l["frp"]) for l in lignes if l.get("frp")]
        resultat = {
            "bassin": bassin,
            "source": "NASA FIRMS — VIIRS_NOAA20_NRT",
            "jours": jours,
            "nb_feux": len(lignes),
            "frp_total_mw": round(sum(frp), 2),
            "frp_max_mw": round(max(frp), 2) if frp else 0.0,
            "etiquette": "DONNÉES RÉELLES (NASA FIRMS)",
        }
        _ecrire_cache(bassin, jour, resultat)
    _memoire[(bassin, jour, jours)] = resultat
    return resultat


def priorite_hubs(bassins=None, jours=1):
    """Classement des bassins par brûlage actif réel, décroissant.

    Base de la priorisation des hubs : plus un bassin brûle, plus un
    trio y est prioritaire (pain point vif, opportunité d'approvision-
    nement et de message écologique).

    V1.4 — pondération par l'énergie : le classement trie d'abord par
    FRP total (MW, l'énergie rayonnée, proportionnelle à la biomasse
    consommée — Wooster et al. 2005), puis par nombre de détections.
    Dix petits feux de ratissement ne pèsent plus un chantier de
    chaumes : l'énergie l'emporte sur le comptage.
    Sans clé ou sans données : liste vide — le repli est synthétique.
    """
    classement = []
    for bassin in (bassins or BOITES_BASSINS):
        donnees = feux_bassin(bassin, jours=jours)
        if donnees:
            classement.append(donnees)
    classement.sort(key=lambda d: (-d["frp_total_mw"], -d["nb_feux"], d["bassin"]))
    return classement

