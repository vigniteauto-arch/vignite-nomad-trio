# Interfaces inter-modules — cadre à figer

Objectif : figer les interfaces Buffer ↔ Stock ↔ Ops pour permettre le travail en parallèle sans réunion de synchronisation permanente.

## Principe

Chaque interface est définie par un contrat : point de connexion physique, support transporté, plage nominale (à définir en conception détaillée, valeurs non calibrées ici), mode de verrouillage, conditions d'erreur.

## Interfaces à documenter

1. Buffer → Stock : transfert cake pré-séché. Support : convoyage interne. Points : entrée trémie Stock.
2. Buffer → Ops : transfert cake pré-séché. Support : même convoyage, aiguillage.
3. Stock → Buffer/Ops : alimentation électrique et thermique CHP.
4. Stock → sortie biochar : bigbag, quai de dépose.
5. Ops → sortie produits finis : table de dépose, quai.
6. Buffer → évacuation contenants (lixiviats, jus bruts, Jus Nobles).

## Statut

En cours de définition. Ticket associé : figer les interfaces avant commande ferme des équipements longs.
