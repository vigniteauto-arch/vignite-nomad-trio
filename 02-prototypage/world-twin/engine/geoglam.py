#!/usr/bin/env python3
"""Couche P2.3 — croisement GEOGLAM du Trio Nomad v1 (v0.7, 17/10/2026).

Confronte les fenêtres d'opération du moteur (engine/monde.py, étiquetées
ILLUSTRATION) aux calendriers culturaux sous-nationaux réels et aux
conditions de campagne du mois. Chaque élément porte son étiquette :

- DONNÉES RÉELLES (source publique croisée, datée) ;
- HORS PÉRIMÈTRE GEOGLAM (culture pérenne ou pays absent des couches
  GEOGLAM : vigne, olivier, noyer, yerba mate, Suisse) ;
- À SOURCER (fenêtre candidate, jamais ingérée dans monde.py avant
  sourcing complet : gisement, ratio, volumes).

RÈGLES :
- GEOGLAM couvre les quatre céréales AMIS (blé, maïs, riz, soja) et
  les cultures de sécurité alimentaire du CM4EW — pas nos pérennes.
- Les calendriers AMIS ne sont pas téléchargeables (« à venir » au
  17/10/2026) : les dates des pays AMIS sont sourcées par les bases
  publiques équivalentes (USDA, FAO GIEWS), croisées avec des sources
  locales. Le portail IPAD de l'USDA a été fermé au public (17/10/2026).
- Conditions de campagne datées du 28/09/2026 (bulletins du 01/10/2026) :
  re-vérifier avant tout usage externe.
- Aucune valeur calibrée ; tout résultat de simulation reste
  étiqueté SYNTHÉTIQUE.

Lancement :

    python3 engine/geoglam.py                 # sommaire console
    python3 engine/geoglam.py es-extremadura  # fiche d'un hub
    python3 engine/geoglam.py croisement      # croisement machine complet

Les identifiants de hubs sont exactement ceux de engine/monde.py ;
verifier_couverture() le contrôle au lancement.
"""

import sys

ETIQUETTE_REEL = "DONNÉES RÉELLES"
ETIQUETTE_HORS_PERIMETRE = "HORS PÉRIMÈTRE GEOGLAM"
ETIQUETTE_A_SOURCER = "À SOURCER"

DATE_EXTRACTION = "17/10/2026"

# Calendriers culturaux sous-nationaux des hubs, sourcés et étiquetés.
# mois : 1 à 12. Sources vérifiées le 17/10/2026 (croisement-geoglam.md).
CALENDRIERS_GEOGLAM = {
    "fr-rhone": {
        "pays": "France",
        "region_geoglam": "France Northern/Southern (couches NASA Harvest/UMD)",
        "cultures": [
            {"culture": "maïs grain",
             "semis": [4, 5], "recolte": [10, 11, 12],
             "source": "Arvalis / La France Agricole — récolte prévue autour du 5-20 octobre, au plus tard fin octobre au niveau national, chantiers jusqu'en décembre selon l'année",
             "etiquette": ETIQUETTE_REEL},
            {"culture": "riz (Camargue)",
             "semis": [4, 5], "recolte": [9, 10],
             "source": "ABrideCamargue / Connexion France / Les Bains Gardians — moisson de la mi-septembre à la fin octobre, trois sources concordantes ; production camarguaise hors calendriers AMIS (mineure à l'échelle mondiale)",
             "etiquette": ETIQUETTE_REEL},
        ],
    },
    "ch-leman": {
        "pays": "Suisse",
        "region_geoglam": "absente des couches GEOGLAM et des deux bulletins",
        "cultures": [],
        "note": "Suisse absente des calendriers CM4EW et du bulletin AMIS ; à sourcer via OFAG/Agroscope si besoin.",
    },
    "it-puglia": {
        "pays": "Italie",
        "region_geoglam": "Italie (couche NASA Harvest/UMD)",
        "cultures": [
            {"culture": "blé dur (Tavoliere/Monti Dauni)",
             "semis": [11, 12], "recolte": [5, 6],
             "source": "Grano Italiano — semis « autour du 20 novembre et tout le mois de décembre » ; moisson débutée vers le 25 mai dans les zones arides, terminée fin juin sur les Monti Dauni",
             "etiquette": ETIQUETTE_REEL},
        ],
    },
    "es-extremadura": {
        "pays": "Espagne",
        "region_geoglam": "Espagne (couche NASA Harvest/UMD)",
        "cultures": [
            {"culture": "blé dur (Badajoz)",
             "semis": [10, 11, 12], "recolte": [6, 7],
             "source": "MAPA, calendrier de siembra y recolección 2014-2016, Badajoz — semis octobre-décembre (30/60/10 %), récolte juin-juillet (90/10 %)",
             "etiquette": ETIQUETTE_REEL},
            {"culture": "orge brassicole (Badajoz)",
             "semis": [10, 11], "recolte": [6, 7],
             "source": "MAPA, calendrier 2014-2016, Badajoz — semis octobre-novembre, récolte juin-juillet",
             "etiquette": ETIQUETTE_REEL},
            {"culture": "riz (bassin du Guadiana)",
             "semis": [4, 5], "recolte": [9, 10],
             "source": "MAPA, calendrier 2014-2016, Badajoz — índica/japónica 10/90 % au semis, récolte septembre-octobre 70/30 %",
             "etiquette": ETIQUETTE_REEL},
        ],
    },
    "ar-cuyo": {
        "pays": "Argentine (Mendoza)",
        "region_geoglam": "Argentine Western = Cuyo (12 régions NASA Harvest/UMD)",
        "cultures": [
            {"culture": "blé",
             "semis": [6, 7, 8], "recolte": [11, 12],
             "source": "Loneralj / Grain Brokers Australia — semis juin-août, récolte novembre-décembre, pic en décembre",
             "etiquette": ETIQUETTE_REEL},
            {"culture": "maïs",
             "semis": [9, 10, 11, 12, 1], "recolte": [3, 4, 5, 6, 7],
             "source": "GeoPard compilant l'USDA FAS — semis échelonnés septembre-janvier, récolte mars-juillet",
             "etiquette": ETIQUETTE_REEL},
        ],
    },
    "ar-misiones": {
        "pays": "Argentine (Misiones)",
        "region_geoglam": "Argentine Northeast = Misiones (12 régions NASA Harvest/UMD)",
        "cultures": [
            {"culture": "maïs",
             "semis": [9, 10, 11, 12, 1], "recolte": [3, 4, 5, 6, 7],
             "source": "GeoPard compilant l'USDA FAS — semis échelonnés septembre-janvier, récolte mars-juillet",
             "etiquette": ETIQUETTE_REEL},
        ],
    },
    "ma-atlas": {
        "pays": "Maroc (Meknès)",
        "region_geoglam": "Maroc Northern ou Central (6 régions CM4EW ; rattachement Meknès/Saïss à trancher)",
        "cultures": [
            {"culture": "blé tendre (région Northern)",
             "semis": [10], "recolte": [5, 6, 7],
             "source": "Calendriers CM4EW en machine (Zenodo DOI 10.5281/zenodo.10949971, CC-BY 4.0) — semis octobre, dormance, reprise végétative janvier, moisson à partir de mai, fin de saison juillet, hors saison août (double décodage concordant jours 289/1/121/182/213 et mois littéraux) ; région Central voisine : moisson dès avril",
             "etiquette": ETIQUETTE_REEL},
        ],
    },
}

# Conditions de campagne des bulletins Crop Monitor for AMIS n° 143 et
# CM4EW n° 120 (publiés le 01/10/2026, conditions au 28/09/2026).
CONDITIONS_CAMPAGNE = {
    "climat": "El Niño présent et se renforçant, très probablement très fort de septembre 2026 à janvier 2027, parmi les plus forts depuis 1950 ; IOD positif octobre-décembre 2026.",
    "ar-cuyo": "Blé argentin favorable au stade végétatif, surface semée en baisse ; outlook octobre-décembre : précipitations au-dessus de la moyenne et températures en dessous sur la principale région agricole.",
    "fr-rhone": "Maïs UE dégradé par des déficits de pluie persistants et de la chaleur en Europe de l'Ouest.",
    "ma-atlas": "MENA : préparation des sols du blé 2026/27 en cours, semis à partir d'octobre.",
}

# Verdicts du croisement pour les biomasses déjà présentes dans monde.py.
# monde.py reste INCHANGÉ : le croisement valide, il ne modifie pas le moteur.
VERDICTS_MOTEUR = {
    "fr-rhone": [
        {"biomasse": "mais-rdm", "fenetre": [10, 11, 12],
         "verdict": "VALIDÉE",
         "justification": "Les résidus suivent la moisson du maïs grain (récolte 5-20 octobre, chantiers jusqu'en décembre) — fenêtre conservée à l'identique dans monde.py."},
        {"biomasse": "paille-riz", "fenetre": [10, 11, 12],
         "verdict": "VALIDÉE",
         "justification": "Moisson du riz camarguais de la mi-septembre à la fin octobre (trois sources concordantes) ; riz camarguais hors des calendriers AMIS : sources locales, pas GEOGLAM."},
    ],
    "ar-cuyo": [
        {"biomasse": "restos-poda", "fenetre": [6, 7, 8],
         "verdict": "cohérence saisonnière VALIDÉE",
         "justification": "Taille d'hiver de la vigne mendocine, hors de la fenêtre de récolte du blé (novembre-décembre) : les deux calendriers ne se collisionnent pas."},
    ],
}

# Fenêtres candidates détectées par le croisement. Étiquette À SOURCER :
# jamais ingérées dans monde.py avant sourcing complet (gisement, ratio, volumes).
FENETRES_CANDIDATES = {
    "it-puglia": [
        {"biomasse_candidate": "paille-blé-dur", "fenetre": [6, 7],
         "justification": "Moisson du blé dur du ~25 mai à fin juin (Monti Dauni) ; aucune biomasse céréalière dans monde.py pour ce hub."},
    ],
    "es-extremadura": [
        {"biomasse_candidate": "paille-blé-dur", "fenetre": [7, 8],
         "justification": "Récolte du blé dur juin-juillet (90/10 %) ; la paille suit en juillet-août."},
        {"biomasse_candidate": "paille-orge", "fenetre": [7, 8],
         "justification": "Récolte de l'orge brassicole juin-juillet."},
        {"biomasse_candidate": "paille-riz-guadiana", "fenetre": [10, 11],
         "justification": "Récolte du riz du Guadiana septembre-octobre (70/30 %) ; la paille suit en octobre-novembre."},
    ],
    "ar-cuyo": [
        {"biomasse_candidate": "paille-blé", "fenetre": [12, 1],
         "justification": "Récolte du blé novembre-décembre, pic en décembre ; la paille suit en décembre-janvier."},
    ],
    "ar-misiones": [
        {"biomasse_candidate": "restos-de-maiz", "fenetre": [4, 5, 6, 7],
         "justification": "Récolte du maïs argentin mars-juillet ; les restes suivent la moisson."},
    ],
    "ma-atlas": [
        {"biomasse_candidate": "paille-blé", "fenetre": [5, 6, 7],
         "justification": "Moisson du blé à partir de mai (région Northern), dès avril en région Central — fourchette avril-juillet ; rattachement GEOGLAM de Meknès/Saïss à trancher."},
    ],
}

MOIS_ABR = {m: ["jan", "fév", "mar", "avr", "mai", "juin",
                "juil", "août", "sep", "oct", "nov", "déc"][m - 1] for m in range(1, 13)}


def mois_texte(mois):
    return " ".join(MOIS_ABR[m] for m in mois)


def hubs_connus():
    return list(CALENDRIERS_GEOGLAM)


def verifier_couverture():
    """Contrôle que le croisement couvre exactement les hubs de monde.py.

    Retourne None si le contrôle passe, sinon un message d'écart.
    Tolérant : si monde.py n'est pas importable, contrôle sauté.
    """
    try:
        import monde
    except ImportError:
        return None
    croisement = set(CALENDRIERS_GEOGLAM)
    moteur = set(monde.HUBS_MONDE)
    if croisement != moteur:
        manquants = sorted(moteur - croisement)
        en_trop = sorted(croisement - moteur)
        return "écart croisement/moteur — manquants: %s ; en trop: %s" % (
            ", ".join(manquants) or "aucun", ", ".join(en_trop) or "aucun")
    return None


def _fenetre_valide(mois):
    """Fenêtre valide : mois uniques dans 1-12, croissants avec au plus
    un wrap-around annuel (hémisphère Sud : ex. [9,10,11,12,1], [12,1])."""
    if not mois or len(set(mois)) != len(mois):
        return False
    if not all(1 <= m <= 12 for m in mois):
        return False
    descentes = sum(1 for i in range(len(mois) - 1) if mois[i + 1] < mois[i])
    return descentes <= 1


def verifier_coherence():
    """Contrôle interne des données du croisement.

    Retourne None si tout est cohérent, sinon un message d'écart :
    mois dans 1-12 (wrap-around annuel admis, hémisphère Sud),
    étiquettes connues, candidates sur des hubs connus.
    """
    etiquettes_valides = {ETIQUETTE_REEL, ETIQUETTE_HORS_PERIMETRE, ETIQUETTE_A_SOURCER}
    for hub_id, f in CALENDRIERS_GEOGLAM.items():
        for c in f["cultures"]:
            for champ in ("semis", "recolte"):
                if not _fenetre_valide(c.get(champ)):
                    return "%s/%s : %s invalide" % (hub_id, c["culture"], champ)
            if c["etiquette"] not in etiquettes_valides:
                return "%s/%s : étiquette inconnue %s" % (hub_id, c["culture"], c["etiquette"])
    for hub_id, candidates in FENETRES_CANDIDATES.items():
        if hub_id not in CALENDRIERS_GEOGLAM:
            return "candidat sur hub inconnu : %s" % hub_id
        for cand in candidates:
            if not _fenetre_valide(cand["fenetre"]):
                return "candidate %s/%s : fenêtre invalide" % (hub_id, cand["biomasse_candidate"])
    return None


def fiche_hub(hub_id):
    if hub_id not in CALENDRIERS_GEOGLAM:
        return "Hub inconnu : %s. Hubs : %s" % (hub_id, ", ".join(CALENDRIERS_GEOGLAM))
    f = CALENDRIERS_GEOGLAM[hub_id]
    lignes = []
    lignes.append("== %s — %s" % (hub_id, f["pays"]))
    lignes.append("  Région GEOGLAM : %s" % f["region_geoglam"])
    if f["cultures"]:
        for c in f["cultures"]:
            lignes.append("  [%s] %s — semis %s, récolte %s (source : %s)" % (
                c["etiquette"], c["culture"], mois_texte(c["semis"]),
                mois_texte(c["recolte"]), c["source"]))
    else:
        lignes.append("  [%s] aucune culture GEOGLAM pour ce hub" % ETIQUETTE_HORS_PERIMETRE)
        lignes.append("  Note : %s" % f.get("note", "pérennes hors périmètre GEOGLAM"))
    for v in VERDICTS_MOTEUR.get(hub_id, []):
        lignes.append("  Moteur : %s %s — %s (%s)" % (
            v["biomasse"], mois_texte(v["fenetre"]), v["verdict"], v["justification"]))
    for cand in FENETRES_CANDIDATES.get(hub_id, []):
        lignes.append("  Candidate [%s] : %s %s — %s" % (
            ETIQUETTE_A_SOURCER, cand["biomasse_candidate"],
            mois_texte(cand["fenetre"]), cand["justification"]))
    if hub_id in CONDITIONS_CAMPAGNE:
        lignes.append("  Campagne (28/09/2026) : %s" % CONDITIONS_CAMPAGNE[hub_id])
    return "\n".join(lignes)


def sommaire():
    lignes = ["Croisement GEOGLAM — calendriers culturaux des sept hubs (v0.7, 17/10/2026)",
              "Extraction et croisement du %s ; conditions de campagne du 28/09/2026 ; à re-vérifier avant tout usage externe." % DATE_EXTRACTION,
              "Climat : %s" % CONDITIONS_CAMPAGNE["climat"],
              ""]
    for hub_id in CALENDRIERS_GEOGLAM:
        lignes.append(fiche_hub(hub_id))
        lignes.append("")
    return "\n".join(lignes) + "\n"


def croisement_machine():
    """Synthèse machine : pour chaque hub, cultures GEOGLAM, biomasses du
    moteur (avec verdicts) et fenêtres candidates À SOURCER."""
    try:
        import monde
        moteur_charge = True
    except ImportError:
        moteur_charge = False
    lignes = ["Croisement machine GEOGLAM/moteur (v0.7)", ""]
    for hub_id in CALENDRIERS_GEOGLAM:
        f = CALENDRIERS_GEOGLAM[hub_id]
        lignes.append("%s (%s) — région : %s" % (hub_id, f["pays"], f["region_geoglam"]))
        for c in f["cultures"]:
            lignes.append("  GEOGLAM : %s — récolte %s [%s]" % (
                c["culture"], mois_texte(c["recolte"]), c["etiquette"]))
        if moteur_charge:
            for nom, fiche in monde.HUBS_MONDE[hub_id]["biomasses"].items():
                verdict = "HORS PÉRIMÈTRE GEOGLAM (pérenne ou non couvert)"
                for v in VERDICTS_MOTEUR.get(hub_id, []):
                    if v["biomasse"] == nom:
                        verdict = v["verdict"]
                lignes.append("  Moteur : %s %s — %s" % (nom, mois_texte(fiche["fenetre_operation"]), verdict))
        for cand in FENETRES_CANDIDATES.get(hub_id, []):
            lignes.append("  Candidate À SOURCER : %s %s" % (cand["biomasse_candidate"], mois_texte(cand["fenetre"])))
        lignes.append("")
    return "\n".join(lignes) + "\n"


def main():
    ecart = verifier_couverture()
    if ecart:
        print("ATTENTION : %s" % ecart)
    ecart2 = verifier_coherence()
    if ecart2:
        print("ATTENTION : %s" % ecart2)
    if len(sys.argv) > 1:
        if sys.argv[1] == "croisement":
            print(croisement_machine(), end="")
        else:
            print(fiche_hub(sys.argv[1]))
    else:
        print(sommaire(), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
