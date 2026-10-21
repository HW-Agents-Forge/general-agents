# Feuille de route

Principe : valider tôt, sur un seul agent et un seul outil, avant de généraliser.

## Jalon 0 : préparation

- [ ] Répondre aux points bloquants de [open-questions.md](open-questions.md) (outil prioritaire, modèles `small`).
- [ ] Vérifier le format de l'outil prioritaire dans sa documentation officielle et remplir [targets.md](targets.md).
- [ ] `pyproject.toml`, squelette `src/shuttle/`, `tests/`, outils de lint et de typage.

## Jalon 1 : tranche verticale minimale

Objectif : `agents/run.md` installé de bout en bout pour **un** outil.

- [ ] `model.py` et `errors.py`.
- [ ] `parser.py` avec tests.
- [ ] `registry.py`.
- [ ] Première cible dans `targets/`.
- [ ] `installer.py` avec toutes les règles de sécurité et leurs tests.
- [ ] `cli.py` et exécutable `install` (`--dry-run` inclus).
- [ ] Agent `run` rédigé.

Critère de sortie : `install --dry-run` puis `install` produisent le bon fichier dans un home de test ; l'agent est utilisable dans l'outil.

## Jalon 2 : première évaluation

- [ ] Évaluer `run` selon [evaluation.md](evaluation.md) sur au moins un scénario réel.
- [ ] Décider : on poursuit, on ajuste le prompt, ou on revoit l'approche.

Ce jalon conditionne la suite : si le gain n'est pas démontré, on revoit le catalogue avant d'investir davantage.

## Jalon 3 : catalogue complet

- [ ] Agents `find`, `diff`, `git`, `svn` (ou `vcs`, selon décision).
- [ ] Skill `atomic-tasks`.
- [ ] Évaluation de chaque agent.

## Jalon 4 : multi-outils

- [ ] Cibles restantes (VS Code, Copilot CLI, OpenCode), une à la fois, chacune précédée de la vérification de son format.
- [ ] Tests de référence par cible.
- [ ] Installation des skills selon les emplacements de chaque outil.

## Jalon 5 : finition

- [ ] `--remove` avec confirmation, limité aux fichiers marqués.
- [ ] README du dépôt mis à jour (usage, installation).
- [ ] Revue de sécurité de `installer`.

## Hors feuille de route (à reconsidérer plus tard)

- Agents supplémentaires, selon besoin mesuré.
- Automatisation de l'évaluation.
- Publication du package.
