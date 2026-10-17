# Architecture du trio Nomad v1

## Vue d'ensemble

Trois conteneurs 20' High Cube (6,06 × 2,44 × 2,90 m extérieurs), positionnés côte à côte pour optimiser les procédés :

- Buffer — réception, préparation et pressage de la biomasse.
- Stock — conversion thermique, cogénération, conditionnement du biochar.
- Ops — salle blanche de finition : presse de thermo-compression, bras de préhension, gravure laser, table de dépose.

## Doctrines d'intégration

- Toiture vide en configuration transport.
- En mode opérationnel, circulations (câbles, tuyauteries) admises sur les toitures.
- Sorties en façade affleurante uniquement (aucun équipement en toiture).
- Machines et flux intégralement internes aux conteneurs.

## Flux inter-modules (niveau conceptuel)

1. Biomasse → Buffer : trappe verrouillable en partie haute du petit côté (bord largeur), alimentation gravitaire vers silo d'autonomie.
2. Silo → trémie → pré-broyeur → presse à vis.
3. Bifurcation du cake pré-séché vers Stock (conversion) et Ops (finition).
4. Buffer : trois circuits de liquides (lixiviats, jus bruts, Jus Nobles) acheminés vers contenants dédiés, bacs IBC thermo-régulés.
5. Stock : pyrolyseur → CHP (boucle syngaz, autonomie énergétique du trio) → tunnel double paroi de refroidissement du biochar → bigbag.
6. Ops : presse, bras de préhension, gravure laser, table de dépose des produits finis, ambiance salle blanche.

## Interfaces

Voir interfaces-modules.md. Les détails calibrés des paramètres procédés sont hors dépôt (garde-fous PI).
