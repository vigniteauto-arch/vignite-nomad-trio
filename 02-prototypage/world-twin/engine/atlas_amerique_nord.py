#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""World Twin v1.5 — Atlas des biomasses : Amérique du Nord (Canada).

Extension régionale de la lignée d'atlas (monde v1.0, pays v1.1, vignobles
v1.2, Asie v1.3) : pour les pays non encore couverts de cette région, les
biomasses LOCALES majeures sont placées sur le globe — région, point GPS
(Global Positioning System, approximation de bassin, jamais un cadastre),
type, volume, fenêtre saisonnière, techniques culturales — avec, par pays,
une synthèse réglementaire à cinq postes, tous À VÉRIFIER.

7 intrants, productions SOURCÉES (FAOSTAT QCL 2024 via Commodity
Origins CC BY 4.0, IndexMundi/USDA PS&D relevé 03/2026, tableaux Wikipédia,
Nordic Forest Statistics 2026, Luke, Statistique Canada) et ratios
résidus ILLUSTRATION selon la convention figée v1.3.

Les nouveaux jetons restent HORS de MAPPINGS (gisements_hubs.py) : repli
densité v1.6 à l'exécution, comme l'atlas Asie v1.3 — extension du snapshot
v18 inscrite en action P3.

Doctrine PI (propriété intellectuelle) : ce module n'embarque AUCUN des six
paramètres du VDE (Vignite Decision Engine) et aucune valeur calibrée.
Seules des données publiques sont versionnées. Étiquette SYNTHÉTIQUE au
registre de développement uniquement.

Bibliothèque standard uniquement, déterministe, aucune dépendance réseau.
Usage :
    python3 engine/atlas_amerique_nord.py                # sommaire par pays
    python3 engine/atlas_amerique_nord.py TOKEN          # fiche d'un intrant
    python3 engine/atlas_amerique_nord.py croisement     # contrôles complets
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import atlas_biomasses_monde as _master   # noqa: E402
import atlas_biomasses_pays as _p11        # noqa: E402
import atlas_vignobles_monde as _v12       # noqa: E402
import atlas_biomasses_asie as _v13        # noqa: E402

ETIQUETTE_A_VERIFIER = "À VÉRIFIER"
CEINTURE_TROPICALE = 23.5
PAYS_AMERIQUE_NORD = {
    "Canada": {
        "nom_fao": "Canada",
        "portrait": "bassin ceinture de blé des Prairies (Saskatchewan) — profil agricole à compléter (v1.5)",
        "reglementation": {
            "brulage": [
                "pratique locale non documentée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.5)"
            ],
            "enfouissement": [
                "retour au sol partiel, profil à sourcer",
                "À VÉRIFIER",
                "à sourcer (v1.5)"
            ],
            "traitement": [
                "aucune filière de valorisation structurée identifiée à ce jour",
                "À VÉRIFIER",
                "à sourcer (v1.5)"
            ],
            "cout_agriculture": [
                "coût de collecte à borner localement",
                "À VÉRIFIER",
                "à sourcer (v1.5)"
            ],
            "main_oeuvre": [
                "main-d'œuvre rurale disponible, saisonnalité des récoltes",
                "À VÉRIFIER",
                "à sourcer (v1.5)"
            ]
        },
        "intrants": [
            {
                "token": "SCIURE_RESINEUX_CA",
                "famille": "Forestier",
                "nom_fr": "Sciure, copeaux et écorces de scierie",
                "region": "scieries du Nord-Ouest de l'Ontario (Kenora)",
                "lat": 49.3,
                "lon": -94.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "sciure, copeaux et écorces de résineux de scierie",
                "production": "abattages de bois rond industriels : 130 Mm³ (Statistique Canada 2024 : 47,9 Mm³ de sciages résineux, × 2,7 m³ de grume par m³ scié (ratio ILLUSTRATION))",
                "ratio": "sciure, copeaux et écorces ≈ 28 % du volume de grume usinée × 0,7 t/m³ (ILLUSTRATION)",
                "gisement": "≈ 25,5 Mt/an",
                "etiquette_gisement": "SOURCÉ (abattages Statistique Canada 2024 : 47,9 Mm³ de sciages résineux, × 2,7 m³ de grume par m³ scié (ratio ILLUSTRATION)) + ratio ILLUSTRATION",
                "fenetre": [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12
                ],
                "fenetre_note": "activité de scierie continue sur l'année, point sous garde",
                "techniques": "sciage de grumes résineuses, écorceuse, rabotage"
            },
            {
                "token": "PAILLE_BLE_CA",
                "famille": "Céréales",
                "nom_fr": "Paille de blé",
                "region": "ceinture de blé des Prairies (Saskatchewan)",
                "lat": 50.5,
                "lon": -104.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille de blé, chaumes et glumes",
                "production": "blé : 35 938 839 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,2 × grain (ILLUSTRATION)",
                "gisement": "≈ 43,1 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    6,
                    7,
                    8
                ],
                "fenetre_note": "récolte de juin à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes, fourrage prioritaire"
            },
            {
                "token": "PAILLE_ORGE_CA",
                "famille": "Céréales",
                "nom_fr": "Paille d'orge",
                "region": "ceinture de blé des Prairies (Saskatchewan)",
                "lat": 50.5,
                "lon": -104.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'orge, chaumes et glumes",
                "production": "orge : 8 143 897 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 8,1 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            },
            {
                "token": "PAILLE_AVOINE_CA",
                "famille": "Céréales",
                "nom_fr": "Paille d'avoine",
                "region": "ceinture de blé des Prairies (Saskatchewan)",
                "lat": 50.5,
                "lon": -104.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "paille d'avoine, chaumes et glumes",
                "production": "avoine : 3 357 551 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 1,0 × grain (ILLUSTRATION)",
                "gisement": "≈ 3,4 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8,
                    9
                ],
                "fenetre_note": "récolte de juillet à septembre, point sous garde",
                "techniques": "moisson motorisée, balles rondes"
            },
            {
                "token": "RESIDUS_COLZA_CA",
                "famille": "Céréales",
                "nom_fr": "Résidus de colza",
                "region": "ceinture de blé des Prairies (Saskatchewan)",
                "lat": 50.5,
                "lon": -104.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "pailles et cosses de colza",
                "production": "colza (graines) : 19 239 463 t (FAOSTAT QCL 2024)",
                "ratio": "paille ≈ 2,5 × graines (ILLUSTRATION)",
                "gisement": "≈ 48,1 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    7,
                    8
                ],
                "fenetre_note": "récolte de juillet à août, point sous garde",
                "techniques": "moisson, battage, andains de cosses"
            },
            {
                "token": "RESIDUS_MAIS_CA",
                "famille": "Céréales",
                "nom_fr": "Résidus de maïs",
                "region": "ceinture de blé des Prairies (Saskatchewan)",
                "lat": 50.5,
                "lon": -104.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, cannes et rafles de maïs",
                "production": "maïs : 15 344 938 t (FAOSTAT QCL 2024)",
                "ratio": "résidus ≈ 0,25 × grain (convention v1.3) (ILLUSTRATION)",
                "gisement": "≈ 3,8 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte en ensilage ou grain, andains au champ"
            },
            {
                "token": "PAILLE_SOJA_CA",
                "famille": "Céréales",
                "nom_fr": "Résidus de soja",
                "region": "ceinture de blé des Prairies (Saskatchewan)",
                "lat": 50.5,
                "lon": -104.0,
                "type_point": "point candidat",
                "hubs_flotte": {},
                "type_biomasse": "tiges, gousses et pailles de soja",
                "production": "soja (graines) : 7 568 013 t (FAOSTAT QCL 2024)",
                "ratio": "résidus ≈ 2,5 × grain (ILLUSTRATION)",
                "gisement": "≈ 18,9 Mt/an",
                "etiquette_gisement": "SOURCÉ (production FAOSTAT QCL 2024) + ratio ILLUSTRATION",
                "fenetre": [
                    9,
                    10,
                    11
                ],
                "fenetre_note": "récolte de septembre à novembre, point sous garde",
                "techniques": "récolte au moissonneur-batteur, andains"
            }
        ]
    }
}


def _index():
    idx = {}
    for pays, fiche in PAYS_AMERIQUE_NORD.items():
        for intrant in fiche["intrants"]:
            idx[intrant["token"]] = (pays, intrant)
    return idx


INDEX = _index()


def verifier_couverture():
    return set(INDEX) & (set(_master.ATLAS_BIOMASSES_MONDE) | set(_p11.INDEX)
                         | set(_v12.INDEX) | set(_v13.INDEX))


def sommaire():
    lignes = ["Atlas Amérique du Nord (Canada) (v1.5) — %d pays, %d intrants" % (len(PAYS_AMERIQUE_NORD), len(INDEX))]
    for pays in sorted(PAYS_AMERIQUE_NORD, key=lambda p: p.lower()):
        lignes.append("  %s — %d intrant(s)" % (pays, len(PAYS_AMERIQUE_NORD[pays]["intrants"])))
    return "\n".join(lignes)


def fiche_token(token):
    if token not in INDEX:
        return None
    pays, intrant = INDEX[token]
    return {"pays": pays, "intrant": intrant}


def croisement():
    lignes = ["Pays couverts : %d" % len(PAYS_AMERIQUE_NORD)]
    lignes.append("Intrants : %d (attendu 7)" % len(INDEX))
    lignes.append("Collisions de jetons avec v1.0-v1.3 : %d" % len(verifier_couverture()))
    familles = sorted({i["famille"] for (_, i) in INDEX.values()})
    lignes.append("Familles : %s" % ", ".join(familles))
    hors = [t for t, (_, i) in INDEX.items() if not (0 <= i["lat"] <= 90 and -180 <= i["lon"] <= 180)]
    lignes.append("Coordonnées hors globe : %d" % len(hors))
    return "\n".join(lignes)


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] == "sommaire":
        print(sommaire())
    elif args[0] == "croisement":
        print(croisement())
    else:
        f = fiche_token(args[0])
        print(json.dumps(f, ensure_ascii=False, indent=2) if f else "jeton inconnu : %s" % args[0])


if __name__ == "__main__":
    main()
