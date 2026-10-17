#!/usr/bin/env python3
"""Couche 1 — atlas des gisements mondiaux du Trio Nomad v1 (v0.5, 17/10/2026).

Données PUBLIQUES, sourcées et étiquetées, croisant FAOSTAT, le Conseil
Oléicole International, le MAPA espagnol, la Junta de Andalucía, l'ISMEA,
l'INYM argentin, l'OFAG suisse et la presse agricole spécialisée.
Chaque chiffre porte son étiquette :

- DONNÉES RÉELLES (source, campagne) : statistique publique croisée,
  citée avec sa source et sa campagne ;
- ILLUSTRATION : ratio de littérature ou produit dérivé indicatif,
  JAMAIS utilisé pour calibrer le moteur.

RÈGLES :
- Aucune valeur calibrée dans ce dépôt ; les estimations business
  (volumes adressables, prix) restent hors du dépôt (doctrine PI).
- Les chiffres publics ci-dessous sont des ordres de grandeur, à
  re-vérifier avant tout usage externe (l'oléiculture alterne
  fortement d'une campagne à l'autre : toujours citer la campagne).
- Tout ce qui sort du simulateur reste étiqueté SYNTHÉTIQUE.

Lancement :

    python3 engine/atlas_gisements.py          # sommaire console
    python3 engine/atlas_gisements.py it-puglia  # fiche d'un hub

Les identifiants de hubs sont exactement ceux de engine/monde.py ;
verifier_couverture() le contrôle au lancement.
"""

import sys

ETIQUETTE_REEL = "DONNÉES RÉELLES"
ETIQUETTE_ILLUSTRATION = "ILLUSTRATION"

SOURCES = {
    "FAOSTAT": "FAO, division statistique (bulk public)",
    "COI": "Conseil Oléicole International (internationaloliveoil.org)",
    "MAPA": "Ministerio de Agricultura, Pesca y Alimentación (Espagne)",
    "JUNTA": "Junta de Andalucía, aforo de producción de olivar",
    "ISMEA": "Istituto di Servizi per il Mercato Agricolo Alimentare (Italie)",
    "MASAF": "Ministero dell'Agricoltura, della Sovranità Alimentare e delle Foreste (Italie)",
    "INYM": "Instituto Nacional de la Yerba Mate (Argentine)",
    "OFAG": "Office fédéral de l'agriculture (Suisse)",
    "AGRI": "presse agricole vérifiée (agrimaroc.ma, extremadura21.com, misionesplural.net, leseco.ma — chiffres repris de sources ministérielles)",
    "LITTERATURE": "littérature scientifique sur les résidus agricoles (ratios ILLUSTRATION)",
}

RATIOS_ILLUSTRATION = [
    {
        "nom": "grignons d'olive",
        "ratio": "0,4 à 0,6 tonne de grignons bruts par tonne d'olives triturées",
        "etiquette": ETIQUETTE_ILLUSTRATION,
        "source": "LITTERATURE",
    },
    {
        "nom": "sarments de vigne",
        "ratio": "1 à 3 tonnes de matière sèche par hectare et par an (1 à 5 selon cépage et conduite)",
        "etiquette": ETIQUETTE_ILLUSTRATION,
        "source": "LITTERATURE",
    },
    {
        "nom": "rendement huile d'olive",
        "ratio": "15 à 20 % du poids d'olives ; cohérent avec l'observable réel andalou 2024/25 (4,45 Mt d'olives de mouture -> 852 943 t d'huile, soit environ 19 %)",
        "etiquette": ETIQUETTE_ILLUSTRATION,
        "source": "LITTERATURE + JUNTA (croisement)",
    },
]

GISEMENTS_MONDE = {
    "fr-rhone": {
        "pays": "France",
        "region": "Vallée du Rhône, Camargue, Sud-Ouest, Périgord",
        "hemisphere": "Nord",
        "faits": [
            {"biomasse": "raisin",
             "indicateur": "production nationale de raisin",
             "valeur": "4,7 à 6,2 Mt/an",
             "etiquette": ETIQUETTE_REEL,
             "source": "FAOSTAT, extraction v0.1 (17/10/2026)"},
            {"biomasse": "mais-rdm",
             "indicateur": "production nationale de maïs",
             "valeur": "14,7 Mt/an",
             "etiquette": ETIQUETTE_REEL,
             "source": "FAOSTAT, extraction v0.1 (17/10/2026)"},
            {"biomasse": "paille-riz",
             "indicateur": "production nationale de riz paddy",
             "valeur": "72 kt/an",
             "etiquette": ETIQUETTE_REEL,
             "source": "FAOSTAT, extraction v0.1 (17/10/2026)"},
            {"biomasse": "coques-noix",
             "indicateur": "production nationale de noix",
             "valeur": "27,7 kt/an",
             "etiquette": ETIQUETTE_REEL,
             "source": "FAOSTAT, extraction v0.1 (17/10/2026)"},
        ],
        "notes": "Hub pilote — le détail complet vit dans pilote-france-2027.md. Le potentiel national business reste hors dépôt (doctrine PI).",
    },
    "ch-leman": {
        "pays": "Suisse",
        "region": "Lavaux-Léman",
        "hemisphere": "Nord",
        "faits": [
            {"biomasse": "sarments-vigne",
             "indicateur": "surface viticole suisse totale",
             "valeur": "14 793 ha (2015, environ 15 000 ha)",
             "etiquette": ETIQUETTE_REEL,
             "source": "OFAG, repris par la viticulture helvétique"},
            {"biomasse": "sarments-vigne",
             "indicateur": "surface du canton de Vaud",
             "valeur": "3 783 ha — environ un quart de la production suisse de vin",
             "etiquette": ETIQUETTE_REEL,
             "source": "OFAG / vignoble vaudois"},
            {"biomasse": "sarments-vigne",
             "indicateur": "potentiel sarments du canton de Vaud (ratio littérature x surface publique)",
             "valeur": "environ 3,8 à 11,3 kt MS/an",
             "etiquette": ETIQUETTE_ILLUSTRATION,
             "source": "LITTERATURE x OFAG (produit dérivé)"},
        ],
        "notes": "Lavaux : terrasses viticoles classées au patrimoine mondial de l'UNESCO (2007), AOC Lavaux. Le bassin FIRMS et ERA5 suisse-leman couvre le Léman vaudois.",
    },
    "it-puglia": {
        "pays": "Italie",
        "region": "Puglia-Tavoliere (Foggia)",
        "hemisphere": "Nord",
        "faits": [
            {"biomasse": "grignons-olive",
             "indicateur": "production italienne d'huile d'olive",
             "valeur": "241 kt (2022, -27 %) ; l'Italie est le 2e producteur mondial derrière l'Espagne (854 kt, 2023)",
             "etiquette": ETIQUETTE_REEL,
             "source": "ISMEA/Agea 2023 ; COI/FAOSTAT 2023"},
            {"biomasse": "grignons-olive",
             "indicateur": "part de la Puglia dans la production italienne d'huile",
             "valeur": "environ 40 %",
             "etiquette": ETIQUETTE_REEL,
             "source": "convergent : analyses sectorielles oléicoles italiennes"},
            {"biomasse": "grignons-olive",
             "indicateur": "production italienne d'olives de table",
             "valeur": "80 à 90 kt/an",
             "etiquette": ETIQUETTE_REEL,
             "source": "MASAF"},
        ],
        "notes": "Alternance biennale forte : toujours citer la campagne. La crise Xylella a réduit le verger apulien ; le secteur replante des variétés résistantes. Le grignonnage (torréfaction des grignons, Pain Point régional) est un gisement à part entière.",
    },
    "es-extremadura": {
        "pays": "Espagne",
        "region": "Estrémadure",
        "hemisphere": "Nord",
        "faits": [
            {"biomasse": "grignons-olive",
             "indicateur": "production espagnole d'huile d'olive",
             "valeur": "765,3 kt prévus (2023/24), campagne finale autour de 850-900 kt ; 1er producteur mondial",
             "etiquette": ETIQUETTE_REEL,
             "source": "MAPA 2023 ; COI/secteur"},
            {"biomasse": "grignons-olive",
             "indicateur": "surface d'oliveraie d'Estrémadure",
             "valeur": "plus de 300 000 ha, environ 14 % de la surface oléicole nationale",
             "etiquette": ETIQUETTE_REEL,
             "source": "AGRI 2025 (données sectorielles extrêmègnes)"},
            {"biomasse": "grignons-olive",
             "indicateur": "olives de table en Estrémadure",
             "valeur": "75 956 ha en propre + 71 434 ha à double aptitude (verdeur/mouture)",
             "etiquette": ETIQUETTE_REEL,
             "source": "Cooperativas Agro-Alimentarias d'Estrémadure"},
            {"biomasse": "grignons-olive",
             "indicateur": "rendements oléicoles intensifs récents",
             "valeur": "10 000 à 12 000 kg d'olives par hectare",
             "etiquette": ETIQUETTE_REEL,
             "source": "AGRI 2025"},
        ],
        "notes": "Observable réel de croisement : Andalousie 2024/25, 4,45 Mt d'olives de mouture -> 852 943 t d'huile (Junta de Andalucía), soit environ 19 % de rendement — cohérent avec le ratio ILLUSTRATION 15-20 %.",
    },
    "ar-cuyo": {
        "pays": "Argentine",
        "region": "Cuyo-Mendoza",
        "hemisphere": "Sud",
        "faits": [
            {"biomasse": "restos-poda",
             "indicateur": "surface de vigne à Mendoza",
             "valeur": "145 393 ha (2024)",
             "etiquette": ETIQUETTE_REEL,
             "source": "recensement provincial 2024 (analyse sectorielle) ; convergent : 146 000-150 000 ha"},
            {"biomasse": "restos-poda",
             "indicateur": "part de Mendoza dans le vignoble argentin",
             "valeur": "70 à 75 % des surfaces et de la production de vin",
             "etiquette": ETIQUETTE_REEL,
             "source": "convergent : plusieurs analyses viticoles argentines"},
            {"biomasse": "restos-poda",
             "indicateur": "potentiel sarments Mendoza (ratio littérature x surface publique)",
             "valeur": "environ 145 à 436 kt MS/an",
             "etiquette": ETIQUETTE_ILLUSTRATION,
             "source": "LITTERATURE x recensement 2024 (produit dérivé)"},
        ],
        "notes": "Fenêtre de taille hivernale : juin-août (hémisphère Sud) — quand la France taille, Mendoza récolte ; quand la France récolte, Mendoza taille. Le monde ne s'arrête jamais.",
    },
    "ar-misiones": {
        "pays": "Argentine",
        "region": "Misiones",
        "hemisphere": "Sud",
        "faits": [
            {"biomasse": "yerba-mate",
             "indicateur": "surface nationale cultivée",
             "valeur": "environ 210 000 ha (87 % Misiones, 13 % Corrientes)",
             "etiquette": ETIQUETTE_REEL,
             "source": "INYM (données officielles)"},
            {"biomasse": "yerba-mate",
             "indicateur": "production nationale de feuille verte",
             "valeur": "703 312 t (2011) -> 812 995 t (2020) ; environ 880 000 t/an récemment",
             "etiquette": ETIQUETTE_REEL,
             "source": "INYM, statistiques décennales et mensuelles"},
            {"biomasse": "yerba-mate",
             "indicateur": "tissu productif",
             "valeur": "environ 12 700 producteurs et 15 000 tareferos",
             "etiquette": ETIQUETTE_REEL,
             "source": "INYM"},
        ],
        "notes": "Nuance réelle (zafra 2025) : Corrientes, avec moins de 15 % de la surface, a dépassé Misiones en feuille verte en début de campagne — la répartition régionale évolue, à suivre année par année.",
    },
    "ma-atlas": {
        "pays": "Maroc",
        "region": "Al-Atlas (Meknès)",
        "hemisphere": "Nord",
        "faits": [
            {"biomasse": "grignons-olive",
             "indicateur": "production nationale d'olives",
             "valeur": "1,968 Mt (2021/22) ; 1,086 Mt (2022/23) ; environ 1,072 Mt (2023/24)",
             "etiquette": ETIQUETTE_REEL,
             "source": "ministère de l'Agriculture marocain, repris par la presse économique"},
            {"biomasse": "grignons-olive",
             "indicateur": "surface de la région Fès-Meknès",
             "valeur": "320 000 ha, plus de 32 % de la surface oléicole nationale (dont 40 000 ha à Meknès)",
             "etiquette": ETIQUETTE_REEL,
             "source": "AGRI (données du ministère de l'Agriculture)"},
            {"biomasse": "grignons-olive",
             "indicateur": "production oléicole de la région Fès-Meknès",
             "valeur": "déjà dépassé 1 Mt (2017/18 : 1 027 573 t)",
             "etiquette": ETIQUETTE_REEL,
             "source": "direction régionale de l'Agriculture, presse économique"},
        ],
        "notes": "Forte fluctuation interannuelle (déficit hydrique 2022-2024) : toujours citer la campagne. La région Fès-Meknès est le premier bassin oléicole du royaume.",
    },
}


def hubs_connus():
    return list(GISEMENTS_MONDE)


def verifier_couverture():
    """Contrôle que les hubs de l'atlas sont exactement ceux de monde.py.

    Retourne None si le contrôle passe, sinon un message d'écart.
    Tolérant : si monde.py n'est pas importable (exécution isolée),
    le contrôle est sauté sans erreur.
    """
    try:
        import monde
    except ImportError:
        return None
    atlas = set(GISEMENTS_MONDE)
    moteur = set(monde.HUBS_MONDE)
    if atlas != moteur:
        manquants = sorted(moteur - atlas)
        en_trop = sorted(atlas - moteur)
        return "écart atlas/moteur — manquants: %s ; en trop: %s" % (
            ", ".join(manquants) or "aucun", ", ".join(en_trop) or "aucun")
    return None


def fiche_hub(hub_id):
    if hub_id not in GISEMENTS_MONDE:
        return "Hub inconnu : %s. Hubs : %s" % (hub_id, ", ".join(GISEMENTS_MONDE))
    h = GISEMENTS_MONDE[hub_id]
    lignes = []
    lignes.append("== %s — %s (%s, hémisphère %s)" % (hub_id, h["region"], h["pays"], h["hemisphere"]))
    for fait in h["faits"]:
        lignes.append("  [%s] %s : %s (source : %s)" % (
            fait["etiquette"], fait["indicateur"], fait["valeur"], fait["source"]))
    if h.get("notes"):
        lignes.append("  Notes : %s" % h["notes"])
    return "\n".join(lignes)


def sommaire():
    lignes = ["Atlas des gisements mondiaux — Trio Nomad v1 (v0.5, 17/10/2026)"]
    lignes.append("Données publiques, sourcées, étiquetées. Aucune valeur calibrée (doctrine PI).")
    lignes.append("")
    for hub_id in GISEMENTS_MONDE:
        lignes.append(fiche_hub(hub_id))
        lignes.append("")
    lignes.append("Ratios de conversion (ILLUSTRATION, littérature) :")
    for r in RATIOS_ILLUSTRATION:
        lignes.append("  - %s : %s" % (r["nom"], r["ratio"]))
    return "\n".join(lignes) + "\n"


def main():
    ecart = verifier_couverture()
    if ecart:
        print("ATTENTION : %s" % ecart)
    if len(sys.argv) > 1:
        print(fiche_hub(sys.argv[1]))
    else:
        print(sommaire())
    return 0


if __name__ == "__main__":
    sys.exit(main())
