"""Prototype de registre Merkle — démonstration pédagogique.

Implémentation démo : arbre de Merkle binaire, preuve d'inclusion,
vérification par un tiers. Aucune mécanique de production.
"""
import hashlib


def _hash(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def _hash_pair(left: bytes, right: bytes) -> bytes:
    return _hash(left + right)


def build_merkle_tree(leaves):
    """Construit un arbre de Merkle à partir d'une liste d'événements (str)."""
    if not leaves:
        raise ValueError("aucune feuille fournie")
    level = [_hash(leaf.encode("utf-8")) for leaf in leaves]
    tree = [level]
    while len(level) > 1:
        if len(level) % 2 == 1:
            level = level + [level[-1]]  # duplication de la dernière feuille
        level = [_hash_pair(level[i], level[i + 1]) for i in range(0, len(level), 2)]
        tree.append(level)
    return tree


def merkle_root(tree):
    return tree[-1][0]


def merkle_proof(tree, index):
    """Construit la preuve d'inclusion pour la feuille d'index donné."""
    proof = []
    for level in tree[:-1]:
        if index % 2 == 0:
            sibling = level[index + 1] if index + 1 < len(level) else level[index]
            proof.append((sibling, "right"))
        else:
            proof.append((level[index - 1], "left"))
        index //= 2
    return proof


def verify_proof(leaf, proof, root):
    """Vérifie une preuve d'inclusion côté tiers (vérification indépendante)."""
    current = _hash(leaf.encode("utf-8"))
    for sibling, side in proof:
        current = _hash_pair(current, sibling) if side == "right" else _hash_pair(sibling, current)
    return current == root


def demo():
    evenements = [
        "lot-0001: reception biomasse",
        "lot-0001: pre-broyage termine",
        "lot-0001: pressage termine",
        "lot-0001: controle qualite conforme",
    ]
    tree = build_merkle_tree(evenements)
    root = merkle_root(tree)
    print("racine (hex):", root.hex())

    index = 2
    proof = merkle_proof(tree, index)
    ok = verify_proof(evenements[index], proof, root)
    print("verification inclusion evenement", index, ":", "OK" if ok else "ECHEC")

    # altération : un tiers vérifie avec une feuille falsifiée
    falsifie = verify_proof("lot-0001: pressage modifie", proof, root)
    print("verification feuille falsifiee :", "OK" if falsifie else "ECHEC (attendu)")


if __name__ == "__main__":
    demo()
