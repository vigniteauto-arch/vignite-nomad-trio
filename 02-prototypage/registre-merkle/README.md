# Prototype de registre Merkle (mode démo)

## Objectif

Démontrer la mécanique : lot d'événements → arbre de Merkle → racine publiée → preuve d'inclusion vérifiable par un tiers.

## Contenu

- merkle_prototype.py : implémentation pédagogique autonome (stdlib uniquement), arbre binaire, preuve d'inclusion, vérification.

## Périmètre démo

- Hachage SHA-256, structure en mémoire, jeux d'essais simples.
- Publication simulée de la racine.

## Hors périmètre

Toute clé, tout système de production, tout encodage propriétaire. Ce prototype sert la conversation technique et la démonstration ; il ne reflète pas la mécanique réelle, volontairement non versionnée.

## Utilisation

python merkle_prototype.py
