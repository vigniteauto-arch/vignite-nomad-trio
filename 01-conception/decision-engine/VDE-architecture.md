# Architecture du Vignite Decision Engine (VDE)

## Rôle

Le VDE orchestre les recettes par biomasse : sélection des paramètres procédés, orchestration des modules, journalisation des événements d'ingénierie et des lots.

## Modules (8)

Cadre de découpage, noms de travail :

1. acquisition — lecture capteurs, normalisation.
2. atlas — identification biomasse, sélection de recette.
3. recettes — exécution paramétrée des séquences.
4. thermique — supervision conversion.
5. pressage — supervision presse à vis.
6. finition — supervision presse, gravure, dépose.
7. journal — traçabilité des lots et événements.
8. supervision — alarmes, modes dégradés, interface opérateur.

## Contrats

Chaque module expose un contrat JSON Schema (voir 02-prototypage/digital-twin/schemas/ pour le format). Coordonnées d'échange en valeurs physiques, pas en indices internes.

## Limites

Les coefficients calibrés, seuils réels et gains sont hors dépôt. Ce document définit la structure uniquement.
