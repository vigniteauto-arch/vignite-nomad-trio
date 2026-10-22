#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""World Twin v1.4 — chaîne FRP → FRE → biomasse → émissions.

Convertit la puissance radiative des feux détectés par NASA FIRMS (Fire
Radiative Power, MW) en estimations documentaires de biomasse consommée
et d'émissions associées — par bassin, région ou pays.

MÉTHODE (sources publiques, citées dans chaque constante) :
- FRP → FRE : la puissance radiative intégrée sur une durée d'observation
  donne l'énergie radiative du feu (FRE, MJ), proportionnelle à la masse
  de biomasse consommée (Wooster et al. 2005, J. Geophys. Res. 110,
  D24311, doi:10.1029/2005JD006318).
- FRE → biomasse : coefficient de combustion 0,368 kg de matière sèche
  par MJ (fourchette mesurée 0,368–0,453 kg/MJ selon les études, NOAA
  NESDIS Technical Memorandum — l'incertitude est d'un facteur ~2).
- Biomasse → émissions : facteurs d'émission IPCC 2006 Vol. 4 Tab. 2.5
  (résidus agricoles, g par kg de matière sèche brûlée) ; GWP AR6
  (CH4 = 27,0 ; N2O = 273) pour l'équivalent CO2 non-CO2.

RÈGLES :
- ÉTIQUETTE : toute valeur produite est une ESTIMATION DOCUMENTAIRE
  ILLUSTRATION — jamais une donnée de qualification, jamais calibrée.
- USAGE : priorisation des hubs, argumentaire, rapport World Ops.
  JAMAIS : calibrage du procédé, registre Merkle de production.
- Le satellite polaire observe chaque zone ~2 fois par jour : la FRE
  entre deux passages est EXTRAPOLÉE (hypothèse de combustion constante
  sur la journée), pas observée. Les feux < 375 m de côté sont
  sous-détectés ; nuages et panaches masquent les détections.

Lancement :

    python3 engine/fre_conversions.py chaine 18,1          # chaîne pour 18,1 MW
    python3 engine/fre_conversions.py chaine 18,1 7        # sur 7 jours
    python3 engine/fre_conversions.py exemple              # cas d'école documenté
"""

import json
import sys

# ---------------------------------------------------------------------------
# Constantes sourcées (toutes publiques)
# ---------------------------------------------------------------------------

# Coefficient FRE → biomasse (kg de matière sèche par MJ).
# Wooster et al. 2005 ; fourchette 0,368–0,453 (NOAA NESDIS, FBCC).
COEFF_FRE_BIOMASSE_KG_PAR_MJ = 0.368
COEFF_FRE_BIOMASSE_MIN = 0.368
COEFF_FRE_BIOMASSE_MAX = 0.453

# Passages du satellite polaire par jour sur une même zone (jour + nuit).
# Hypothèse d'extrapolation documentaire : le FRP relevé au passage est
# supposé représenter la puissance moyenne sur la demi-journée.
PASSAGES_PAR_JOUR = 2
SECONDES_PAR_JOUR = 86400

# Facteurs d'émission des résidus agricoles (g par kg de matière sèche
# brûlée) — IPCC 2006 Vol. 4 Ch. 2 Tab. 2.5, colonne « Agricultural residues ».
FACTEURS_EMISSION_G_PAR_KG = {
    "co2": 1515.0,   # dioxyde de carbone (biogénique : rapporté, nettoyé par repousse)
    "ch4": 2.7,      # méthane
    "n2o": 0.07,     # protoxyde d'azote
    "co": 92.0,      # monoxyde de carbone (polluant air, pas de GWP)
    "nox": 2.5,      # oxydes d'azote (polluant air, pas de GWP)
}

# Pouvoirs de réchauffement global (GWP-100, IPCC AR6).
GWP_CH4 = 27.0
GWP_N2O = 273.0

ETIQUETTE = "ESTIMATION DOCUMENTAIRE ILLUSTRATION (chaîne FRP→FRE→IPCC, non calibrée)"


# ---------------------------------------------------------------------------
# Chaîne de conversion
# ---------------------------------------------------------------------------

def fre_extrapolee_mj(frp_total_mw, heures=24.0):
    """Énergie radiative extrapolée (MJ) : puissance × durée.

    Le FRP total relevé au passage (MW) est extrapolé sur la durée demandée
    avec l'hypothèse documentaire de combustion constante. 1 MW × 1 s = 1 MJ.
    """
    return float(frp_total_mw) * float(heures) * 3600.0


def biomasse_consommee_t(fre_mj, coeff=None):
    """Biomasse sèche consommée (tonnes) depuis la FRE (MJ)."""
    c = COEFF_FRE_BIOMASSE_KG_PAR_MJ if coeff is None else coeff
    return fre_mj * c / 1000.0


def emissions(biomasse_t):
    """Émissions (tonnes de chaque gaz) pour une biomasse brûlée (t MS).

    Retourne un dict étiqueté. Le CO2 biogénique est rapporté pour
    information ; l'impact inventorié d'un brûlage agricole est porté
    par le méthane et le protoxyde d'azote (IPCC 2006).
    """
    kg = biomasse_t * 1000.0
    sorties = {gaz: facteur * kg / 1e6 for gaz, facteur in FACTEURS_EMISSION_G_PAR_KG.items()}
    sorties["co2e_nonco2_t"] = (
        sorties["ch4"] * GWP_CH4 + sorties["n2o"] * GWP_N2O
    )
    return sorties


def chaine(frp_total_mw, heures=24.0):
    """Chaîne complète : FRP (MW) → FRE (MJ) → biomasse (t) → émissions (t).

    Toutes les valeurs sont des ESTIMATIONS DOCUMENTAIRES ILLUSTRATION.
    """
    fre = fre_extrapolee_mj(frp_total_mw, heures)
    biomasse = biomasse_consommee_t(fre)
    fourchette = (biomasse_consommee_t(fre, COEFF_FRE_BIOMASSE_MIN),
                  biomasse_consommee_t(fre, COEFF_FRE_BIOMASSE_MAX))
    return {
        "frp_total_mw": round(float(frp_total_mw), 2),
        "duree_h": heures,
        "fre_mj": round(fre, 0),
        "fre_gj": round(fre / 1000.0, 1),
        "biomasse_t": round(biomasse, 1),
        "biomasse_fourchette_t": (round(fourchette[0], 1), round(fourchette[1], 1)),
        "co2_t": round(0.0, 1),
        "emissions": {g: round(v, 3) for g, v in emissions(biomasse).items()},
        "etiquette": ETIQUETTE,
    }


# ---------------------------------------------------------------------------
# Interface console
# ---------------------------------------------------------------------------

def _rendre_chaine(c):
    lignes = [
        "Chaîne FRP → FRE → biomasse → émissions — ESTIMATION ILLUSTRATION",
        "",
        "FRP total relevé    : %s MW sur %s h" % (c["frp_total_mw"], c["duree_h"]),
        "FRE extrapolée      : %s MJ (%s GJ)" % (fmt(c["fre_mj"]), fmt(c["fre_gj"])),
        "Biomasse consommée  : %s t MS (fourchette %s – %s t, coeff 0,368–0,453 kg/MJ)"
        % (fmt(c["biomasse_t"]), fmt(c["biomasse_fourchette_t"][0]), fmt(c["biomasse_fourchette_t"][1])),
        "",
        "Émissions (IPCC 2006 Vol. 4 Tab. 2.5, résidus agricoles) :",
        "  CO2 biogénique    : %s t (rapporté, la repousse le réabsorbe)" % fmt(c["emissions"]["co2"]),
        "  CH4               : %s t" % fmt(c["emissions"]["ch4"]),
        "  N2O               : %s t" % fmt(c["emissions"]["n2o"]),
        "  CO                : %s t (polluant air, sans GWP)" % fmt(c["emissions"]["co"]),
        "  CO2e non-CO2      : %s t équivalent CO2 (GWP AR6)" % fmt(c["emissions"]["co2e_nonco2_t"]),
        "",
        "Usage : priorisation des hubs, argumentaire, rapport World Ops.",
        "JAMAIS : calibrage du procédé, registre Merkle de production.",
        "Extrapolation : combustion constante entre passages (%d/jour), incertitude ~ facteur 2."
        % PASSAGES_PAR_JOUR,
    ]
    return "\n".join(lignes) + "\n"


def fmt(n):
    return ("{:,.1f}".format(float(n) if n is not None else 0.0)
            .replace(",", " ").replace(".", ","))


def main():
    arguments = sys.argv[1:]
    if not arguments or arguments[0] in ("sommaire", "aide"):
        print(__doc__)
        return 0
    if arguments[0] == "exemple":
        print("# Cas d'école documenté : 11 feux, 18,1 MW relevés en Camargue le 17/10/2026")
        print(_rendre_chaine(chaine(18.1, 24.0)))
        return 0
    if arguments[0] == "chaine":
        if len(arguments) < 2:
            print("Usage : chaine FRP_MW [HEURES]")
            return 1
        heures = float(arguments[2]) if len(arguments) > 2 else 24.0
        try:
            frp = float(arguments[1].replace(",", "."))
        except ValueError:
            print("FRP invalide : %s" % arguments[1])
            return 1
        print(_rendre_chaine(chaine(frp, heures)))
        return 0
    if arguments[0] == "json":
        heures = float(arguments[2].replace(",", ".")) if len(arguments) > 2 else 24.0
        frp = float(arguments[1].replace(",", "."))
        print(json.dumps(chaine(frp, heures), ensure_ascii=False, indent=1))
        return 0
    print("Commande inconnue : %s (sommaire | chaine FRP [HEURES] | exemple | json FRP [HEURES])"
          % arguments[0])
    return 1


if __name__ == "__main__":
    sys.exit(main())
