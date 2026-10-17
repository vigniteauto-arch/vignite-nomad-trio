# Runbook — modes dégradés (cadre)

## Principe

Un mode dégradé maintient la sécurité des personnes et l'intégrité des lots, au prix de cadence ou de fonctionnalité réduite. Jamais de contournement des protections.

## Scénarios (trame)

1. Perte du CHP → trio sur source externe temporaire, arrêt des étapes énergivores, conservation des lots en cours.
2. Défaut presse à vis (Buffer) → by-pass du lot en cours vers stockage tampon, arrêt de l'amont.
3. Défaut pyrolyseur (Stock) → arrêt du gisement, maintien Buffer et Ops en attente contrôlée.
4. Défaut salle blanche (Ops) → produits semi-finis maintenus en zone contrôlée, pas de finition tant que l'ambiance n'est pas rétablie.
5. Défaut acquisition capteurs → exécution stoppée sur le module concerné ; jamais d'exécution aveugle.

## Journalisation

Chaque passage en mode dégradé : événement horodaté, cause, actions, retour au nominal. Alimente le registre et la revue d'amélioration hebdomadaire.

## Statut

Cadre v0 — scénarios à tester sur maquette avant opération.
