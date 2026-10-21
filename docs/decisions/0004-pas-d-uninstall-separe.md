# 0004. Aucune suppression par le script

- Statut : acceptée (remplace la version initiale, qui prévoyait `--remove`)
- Date : 2026-10-21

## Contexte

Un script qui supprime des fichiers dans le home est risqué : une erreur de chemin ou de filtre peut détruire des fichiers n'appartenant pas au projet. Une première version de cette décision acceptait un `--remove` limité aux fichiers marqués.

## Décision

Le script ne supprime **aucun** fichier : pas de `uninstall`, pas de `--remove`, et `installer` n'expose aucune opération de suppression. Pour retirer un agent, l'utilisateur supprime le fichier à la main.

## Conséquences

- Risque de destruction supprimé à la source ; la marque d'origine ne sert plus qu'à décider si un fichier peut être mis à jour (voir [install-spec.md](../install-spec.md)).
- Un agent retiré des sources reste installé jusqu'à suppression manuelle ; `install` ne le signale pas.
- Moins de code et de tests dans `installer` ([testing.md](../testing.md)).
