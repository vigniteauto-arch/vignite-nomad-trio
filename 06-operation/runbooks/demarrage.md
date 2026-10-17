# Runbook — démarrage du trio (cadre)

## Préconditions

- Inspection visuelle des trois conteneurs et des passerelles de services.
- Vérification des contenants vides et des protections.
- Journal de lot ouvert dans le VDE.

## Séquence (à valider en FAT/SAT)

1. Ops : mise en ambiance salle blanche, contrôle des pressions.
2. Stock : montée en température du pyrolyseur, mise en service CHP.
3. Buffer : contrôle silo, trémie, circuits de liquides vides.
4. Boucle énergétique confirmée : autonomie du trio vérifiée.
5. Premier lot : recette sélectionnée dans l'atlas, exécution supervisée.
6. Contrôle de sortie de premier lot, journalisation.

## Critères d'arrêt

Tout écart hors bornes de sécurité → arrêt séquence, passage en mode dégradé (voir mode-degrade.md), journalisation de l'événement.

## Statut

Cadre v0 — validation terrain requise avant tout usage réel.
