# Conventions de contribution

## Branches

- main : état de référence, toujours cohérent.
- feat/<module>-<sujet> : travaux en cours.
- doc/<sujet> : documentation seule.

## Messages de commit

Format : [phase] type(scope) : description courte, impératif.

Phases : infra, conception, prototypage, assemblage, tests, operation.
Types : feat, fix, doc, chore.

Exemple : [prototypage] feat(merkle) : ajout vérification de preuve pour feuille isolée.

## Nommage des fichiers

- Markdown en kebab-case : plan-assemblage.md.
- Schémas JSON : kebab-case + suffixe .schema.json.
- Numérotation des répertoires conservée (00-06).

## Langue

Documentation en français. Code et identifiants en anglais, commentaires en français acceptés.

## Revue

Tout commit vers main passe par une auto-revue PI (voir GARDE_FOUS_PI.md).
