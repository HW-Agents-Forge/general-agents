# 0004. Pas de script uninstall séparé

- Statut : acceptée
- Date : 2026-10-21

## Contexte

Un script qui supprime des fichiers dans le home est risqué : une erreur de chemin ou de filtre peut détruire des fichiers n'appartenant pas au projet.

## Décision

Pas de script `uninstall`. Le retrait est une option de `install` (`--remove`), qui :
- ne supprime que les fichiers portant la marque d'origine **et** correspondant à un agent ou skill connu du dépôt ;
- demande confirmation (sauf `--yes`) ;
- dispose d'un `--dry-run`.

La disponibilité de `--remove` reste révisable (voir [open-questions.md](../open-questions.md)) : l'écarter ne remet pas en cause le reste.

## Conséquences

- Surface de risque réduite et concentrée dans `installer`, testée en priorité ([testing.md](../testing.md)).
- Pas de second point d'entrée à maintenir.
