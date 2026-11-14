#!/usr/bin/env python3
"""xlslite.py — lecteur XLSX en FLUX, stdlib uniquement.

NE JAMAIS charger un classeur entier en mémoire : le Global Bioenergy
Power Plant Tracker (16 Mo de XML) tuait le bac à sable. Ici :
- xml.etree.ElementTree.iterparse avec clear() par ligne ;
- sharedStrings.xml lu en flux (liste de chaînes, jamais l'arbre) ;
- un générateur de lignes par feuille : yield dicts {en-tête: valeur}.

Usage :
    feuilles(chemin) → liste des noms de feuilles
    lire_feuille(chemin, nom_ou_indice) → générateur de dicts, la
        première ligne de la feuille sert d'en-têtes
"""
import re
import xml.etree.ElementTree as ET
import zipfile

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
NS_REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
NS_OFF = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def _colonne(reference):
    """'BC12' → index de colonne (0 = A)."""
    lettres = re.match(r"([A-Z]+)", reference)
    if not lettres:
        return 0
    n = 0
    for c in lettres.group(1):
        n = n * 26 + (ord(c) - 64)
    return n - 1


def _cartes_feuilles(zf):
    """[(nom, chemin_dans_le_zip)] depuis workbook.xml et ses relations."""
    with zf.open("xl/workbook.xml") as f:
        racine = ET.parse(f).getroot()
    correspondances = {}
    for feuille in racine.iter(NS + "sheet"):
        nom = feuille.get("name")
        rid = feuille.get(NS_REL + "id")
        correspondances[rid] = nom
    with zf.open("xl/_rels/workbook.xml.rels") as f:
        racine = ET.parse(f).getroot()
    chemins = {}
    for rel in racine.iter(NS_OFF + "Relationship"):
        if rel.get("Id") in correspondances:
            cible = rel.get("Target")
            if not cible.startswith("xl/"):
                cible = "xl/" + cible.lstrip("/")
            chemins[correspondances[rel.get("Id")]] = cible
    return [(correspondances[rid], chemins[correspondances[rid]])
            for rid in correspondances
            if correspondances[rid] in chemins]


def _chaines_partagees(zf, chemin="xl/sharedStrings.xml"):
    """Liste des chaînes partagées, lues en flux.

    Ne charge jamais l'arbre : à chaque fin de <si>, on concatène le
    texte de ses fragments (texte simple ou riche <r><t>) puis on
    libère l'élément.
    """
    if chemin not in zf.namelist():
        return []
    sortie = []
    fragments = []
    with zf.open(chemin) as f:
        for _evenement, element in ET.iterparse(f, events=("end",)):
            if element.tag == NS + "t":
                if element.text:
                    fragments.append(element.text)
            elif element.tag == NS + "si":
                sortie.append("".join(fragments))
                fragments = []
            element.clear()
    return sortie


def feuilles(chemin):
    """Noms des feuilles du classeur."""
    with zipfile.ZipFile(chemin) as zf:
        return [nom for nom, _c in _cartes_feuilles(zf)]


def lire_feuille(chemin, nom_ou_indice):
    """Générateur de lignes dicts (en-têtes = première ligne).

    nom_ou_indice : nom exact OU indice base 0 de la feuille.
    """
    with zipfile.ZipFile(chemin) as zf:
        cartes = _cartes_feuilles(zf)
        if isinstance(nom_ou_indice, int):
            nom, chemin_feuille = cartes[nom_ou_indice]
        else:
            carte = {n: c for n, c in cartes}
            nom = nom_ou_indice
            chemin_feuille = carte[nom]
        chaines = _chaines_partagees(zf)

        ligne_courante = {}
        en_tetes = None
        index = 0

        with zf.open(chemin_feuille) as f:
            for _evenement, element in ET.iterparse(f, events=("end",)):
                if element.tag != NS + "row":
                    # On ne clear QUE le row (voir ci-dessous) : les
                    # cellules doivent survivre jusqu'à la fin de ligne.
                    continue
                valeurs = {}
                for cellule in element.findall(NS + "c"):
                    ref = cellule.get("r") or ""
                    idx = _colonne(ref)
                    type_ = cellule.get("t")
                    brut = None
                    v = cellule.find(NS + "v")
                    if v is not None and v.text is not None:
                        brut = v.text
                    elif type_ == "inlineStr":
                        t = cellule.find(NS + "is/" + NS + "t")
                        if t is not None:
                            brut = t.text
                    if brut is None:
                        continue
                    if type_ == "s":
                        texte = chaines[int(brut)]
                    elif type_ == "b":
                        texte = "VRAI" if brut == "1" else "FAUX"
                    else:
                        texte = brut
                    valeurs[idx] = texte
                element.clear()

                index += 1
                if en_tetes is None:
                    if not valeurs:
                        continue
                    taille = max(valeurs) + 1
                    en_tetes = [valeurs.get(i, "") for i in range(taille)]
                    continue
                ligne = {}
                for i, tete in enumerate(en_tetes):
                    if i in valeurs and valeurs[i] != "":
                        ligne[tete] = valeurs[i]
                yield ligne


if __name__ == "__main__":
    import sys
    chemin = sys.argv[1]
    print("feuilles :", feuilles(chemin))
    for i, ligne in zip(range(3), lire_feuille(chemin, 0)):
        print(ligne)
