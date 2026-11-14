#!/usr/bin/env python3
"""pdfpos.py — extraction positionnelle de texte PDF, stdlib uniquement.

Usage : fragments(chemin) → [(x, y, texte)] ; lignes_texte(chemin) →
dict y → liste (x, texte) triée par x ; par_lignes(chemin) → liste de
dicts {y, fragments:[(x, texte)]} triés par y décroissant.

Machine minimale : BT/ET, Tf, Tc/Tw, Tz, TL, Tm, Td/TD/T*, Tj/TJ, ',
q/Q/cm (pile explicite des matrices). Chaînes (...) avec escapes,
tableaux TJ [(frag) k (frag)...]. Les polices à CMap (codes de glyphes)
ne sont PAS décodées : ce parseur cible les PDF à encodage simple
(USGS MCS 2026). Aucune dépendance, aucune écriture disque.
"""
import re
import zlib


# --------------------------------------------------------------------------
# Streams
# --------------------------------------------------------------------------

def _streams(brut):
    """Décompresse tous les flux FlateDecode d'un PDF (octets)."""
    sortie = []
    for m in re.finditer(rb"stream\r\n|\r?\nstream\r?\n", brut):
        debut = m.end()
        fin = brut.find(b"endstream", debut)
        if fin < 0:
            break
        morceau = brut[debut:fin]
        if morceau.endswith(b"\r\n"):
            morceau = morceau[:-2]
        elif morceau.endswith(b"\n") or morceau.endswith(b"\r"):
            morceau = morceau[:-1]
        try:
            sortie.append(zlib.decompress(morceau))
        except zlib.error:
            try:
                sortie.append(zlib.decompressobj().decompress(morceau))
            except zlib.error:
                continue
    return sortie


# --------------------------------------------------------------------------
# Matrices 3x2 (a b c d e f) : lignes, colonnes, produit
# --------------------------------------------------------------------------

def _mul(m1, m2):
    """Produit m1 × m2 (m2 appliquée en premier)."""
    a1, b1, c1, d1, e1, f1 = m1
    a2, b2, c2, d2, e2, f2 = m2
    return (a1 * a2 + b1 * c2, a1 * b2 + b1 * d2,
            c1 * a2 + d1 * c2, c1 * b2 + d1 * d2,
            e1 * a2 + f1 * c2 + e2, e1 * b2 + f1 * d2 + f2)


def _translation(m, tx, ty):
    return _mul(m, (1, 0, 0, 1, tx, ty))


def _point(m):
    """Origine (x, y) que la matrice donne au point (0, 0)."""
    return m[4], m[5]


# --------------------------------------------------------------------------
# Décodage des chaînes PDF
# --------------------------------------------------------------------------

def _lire_chaine(data, i):
    """data[i] == b'(' : lit la chaîne avec escapes. Retourne (texte, j)."""
    sortie = bytearray()
    profondeur = 1
    i += 1
    while i < len(data) and profondeur:
        c = data[i]
        if c == 0x5C:  # backslash
            if i + 1 >= len(data):
                break
            n = data[i + 1]
            if n in (0x6E,):  # \n
                sortie.append(0x0A)
                i += 2
            elif n == 0x72:  # \r
                sortie.append(0x0D)
                i += 2
            elif n == 0x74:  # \t
                sortie.append(0x09)
                i += 2
            elif n == 0x62:  # \b
                sortie.append(0x08)
                i += 2
            elif n == 0x66:  # \f
                sortie.append(0x0C)
                i += 2
            elif n in (0x28, 0x29, 0x5C):  # \( \) \\
                sortie.append(n)
                i += 2
            elif 0x30 <= n <= 0x37:  # \ooo octal (1 à 3 chiffres)
                j = i + 2
                octal = bytearray()
                while j < len(data) and len(octal) < 3 \
                        and 0x30 <= data[j] <= 0x37:
                    octal.append(data[j])
                    j += 1
                sortie.append(int(octal.decode("ascii"), 8) & 0xFF)
                i = j
            else:
                i += 2
            continue
        if c == 0x28:  # (
            profondeur += 1
            sortie.append(c)
        elif c == 0x29:  # )
            profondeur -= 1
            if profondeur == 0:
                i += 1
                break
            sortie.append(c)
        else:
            sortie.append(c)
        i += 1
    return bytes(sortie), i


def _hex_chaine(data, i):
    """data[i] == b'<' (chaîne hexadécimale <...>). Retourne (texte, j)."""
    j = data.find(b">", i)
    if j < 0:
        return b"", len(data)
    hexa = re.sub(rb"\s", b"", data[i + 1:j])
    if len(hexa) % 2:
        hexa += b"0"
    try:
        return bytes.fromhex(hexa.decode("ascii")), j + 1
    except ValueError:
        return b"", j + 1


# --------------------------------------------------------------------------
# Tokenisation et machine de rendu
# --------------------------------------------------------------------------

def _nombres(data, i):
    """Lit un ou deux nombres PDF depuis i. Retourne (valeurs, j)."""
    valeurs = []
    while len(valeurs) < 2:
        m = re.match(rb"[ \t]*(\-?\d*\.?\d+)", data[i:])
        if not m:
            break
        valeurs.append(float(m.group(1)))
        i += m.end()
    return valeurs, i


def _rendu(data):
    """Machine à opérateurs sur un flux de contenu. → [(x, y, texte)]."""
    fragments = []
    i, n = 0, len(data)
    pile_ctm = []
    ctm = (1, 0, 0, 1, 0, 0)
    tm = (1, 0, 0, 1, 0, 0)
    tlm = tm
    tl = 0.0
    tf_taille = 1.0
    dans_bt = False
    operandes = []

    while i < n:
        c = data[i:i + 1]
        if c in b" \t\r\n%":
            if c == b"%":
                j = data.find(b"\n", i)
                i = n if j < 0 else j + 1
                continue
            i += 1
            continue
        if c == b"(":
            texte, i = _lire_chaine(data, i)
            operandes.append(("s", texte))
            continue
        if c == b"<" and data[i:i + 2] != b"<<":
            texte, i = _hex_chaine(data, i)
            operandes.append(("s", texte))
            continue
        if c == b"[":
            operandes.append(("[", None))
            i += 1
            continue
        if c == b"]":
            operandes.append(("]", None))
            i += 1
            continue
        if c == b"{":
            j = data.find(b"}", i)
            i = n if j < 0 else j + 1
            continue
        m = re.match(rb"/[A-Za-z0-9_\+#\-\.]+|[\-+]?\d*\.?\d+", data[i:])
        if m:
            jeton = m.group(0)
            i += m.end()
            if jeton.startswith(b"/"):
                operandes.append(("name", jeton[1:]))
            else:
                operandes.append(("n", float(jeton)))
            continue
        # Opérateur : lettres
        m = re.match(rb"[A-Za-z'\"*]+", data[i:])
        if not m:
            i += 1
            continue
        op = m.group(0)
        i += m.end()

        if op == b"q":
            pile_ctm.append(ctm)
        elif op == b"Q":
            ctm = pile_ctm.pop() if pile_ctm else (1, 0, 0, 1, 0, 0)
        elif op == b"cm" and len(operandes) >= 6:
            nums = [v for t, v in operandes if t == "n"][-6:]
            if len(nums) == 6:
                ctm = _mul(tuple(nums), ctm)
        elif op == b"BT":
            dans_bt = True
            tm = (1, 0, 0, 1, 0, 0)
            tlm = tm
        elif op == b"ET":
            dans_bt = False
        elif op == b"Tf":
            nums = [v for t, v in operandes if t == "n"]
            if nums:
                tf_taille = nums[-1]
        elif op == b"TL" and operandes:
            nums = [v for t, v in operandes if t == "n"]
            if nums:
                tl = nums[-1]
        elif op == b"Tm" and dans_bt:
            nums = [v for t, v in operandes if t == "n"][-6:]
            if len(nums) == 6:
                tm = tlm = tuple(nums)
        elif op == b"Td" and dans_bt:
            nums = [v for t, v in operandes if t == "n"][-2:]
            if len(nums) == 2:
                tlm = _translation(tlm, nums[0], nums[1])
                tm = tlm
        elif op == b"TD" and dans_bt:
            nums = [v for t, v in operandes if t == "n"][-2:]
            if len(nums) == 2:
                tl = -nums[1]
                tlm = _translation(tlm, nums[0], nums[1])
                tm = tlm
        elif op == b"T*" and dans_bt:
            tlm = _translation(tlm, 0, -tl)
            tm = tlm
        elif op == b"Tj" and dans_bt:
            for t, v in operandes:
                if t == "s" and v:
                    x, y = _point(_mul(tm, ctm))
                    fragments.append((x, y, v.decode("latin-1")))
                    tm = _translation(tm, _largeur(v, tf_taille), 0)
        elif op == b"TJ" and dans_bt:
            profondeur_tab = 0
            for t, v in operandes:
                if t == "[":
                    profondeur_tab += 1
                    continue
                if t == "]":
                    profondeur_tab -= 1
                    continue
                if t == "n":
                    tm = _translation(tm, -v * tf_taille / 1000.0, 0)
                elif t == "s" and v:
                    x, y = _point(_mul(tm, ctm))
                    fragments.append((x, y, v.decode("latin-1")))
                    tm = _translation(tm, _largeur(v, tf_taille), 0)
            # TJ réinitialise la matrice texte à Tlm (fin de chaîne)
            tm = tlm
        elif op == b"'" and dans_bt:
            tlm = _translation(tlm, 0, -tl)
            tm = tlm
            for t, v in operandes:
                if t == "s" and v:
                    x, y = _point(_mul(tm, ctm))
                    fragments.append((x, y, v.decode("latin-1")))
        operandes = []
    return fragments


def _largeur(texte, taille):
    """Avance horizontale approximative (0.5 em par caractère)."""
    return 0.5 * taille * len(texte)


# --------------------------------------------------------------------------
# API publique
# --------------------------------------------------------------------------

def fragments(chemin):
    """Tous les fragments (x, y, texte) d'un PDF, tous flux confondus."""
    with open(chemin, "rb") as f:
        brut = f.read()
    sortie = []
    for data in _streams(brut):
        if b"BT" not in data:
            continue
        sortie.extend(_rendu(data))
    return sortie


def par_lignes(chemin, tolerance=2.0):
    """Grouppe les fragments par ligne (y ± tolérance, y PDF décroissant)."""
    frags = fragments(chemin)
    lignes = []
    for x, y, texte in sorted(frags, key=lambda f: (-f[1], f[0])):
        if lignes and abs(lignes[-1]["y"] - y) <= tolerance:
            lignes[-1]["fragments"].append((x, texte))
        else:
            lignes.append({"y": y, "fragments": [(x, texte)]})
    return lignes


def texte_ligne(ligne):
    """Assemble les fragments d'une ligne en ignorant les chevauchements."""
    morceaux = []
    for x, texte in sorted(ligne["fragments"]):
        morceaux.append(texte)
    return " ".join(morceaux).strip()


def cellule(ligne, intervalle):
    """Concatène les fragments dont x ∈ intervalle (début du fragment)."""
    bas, haut = intervalle
    morceaux = [t for x, t in sorted(ligne["fragments"]) if bas <= x < haut]
    return "".join(morceaux).strip()


if __name__ == "__main__":
    import sys
    for ligne in par_lignes(sys.argv[1]):
        t = texte_ligne(ligne)
        if t:
            print("%7.1f | %s" % (ligne["y"], t[:150]))
