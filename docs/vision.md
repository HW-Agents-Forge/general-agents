# Vision

## Problème

Les agents de code principaux consomment beaucoup de tokens sur des tâches dont ils n'ont besoin que de la conclusion : lire des logs de build, parcourir un dépôt, résumer un historique git. Ces tâches pourraient être confiées à un modèle plus petit et moins coûteux.

## Objectif

Fournir un ensemble de **petits sous-agents** qui condensent l'information, utilisent les **plus petits modèles possibles**, et sont **définis une seule fois** puis adaptés à plusieurs outils agentiques.

## Principes

1. **Condenser, pas seulement déléguer.** Un sous-agent n'a de valeur que s'il renvoie nettement moins que ce qu'il a consommé.
2. **Un seul format source.** Les agents sont décrits de façon neutre dans `agents/`. Le package `shuttle` les adapte à chaque outil.
3. **Sûr par défaut.** Lecture seule sauf nécessité. L'installation n'écrase jamais un fichier qui n'appartient pas au projet.
4. **Mesurable.** Chaque agent doit pouvoir être évalué par une comparaison de tokens avec et sans délégation (voir [evaluation.md](evaluation.md)).
5. **Sans dépendance à l'exécution.** Bibliothèque standard Python uniquement.

## Périmètre

- Agents : `run`, `find`, `diff`, `git`, `svn` (voir [agents-catalog.md](agents-catalog.md)).
- Skill `atomic-tasks` indiquant à l'agent principal quand et comment déléguer.
- Package Python `shuttle` et exécutable `install`.
- Outils cibles : VS Code, Copilot CLI, OpenCode.

## Hors périmètre

- Agents `read`, `list`, `glob` : redondants avec les outils natifs de l'agent principal.
- Agent `write` : l'agent principal doit déjà fournir tout le contenu, ce qui double le coût.
- `backup` : opération déterministe, relève d'un script et non d'un LLM.
- Script `uninstall` séparé : jugé risqué (voir [install-spec.md](install-spec.md) et ADR 0004).
- Orchestration multi-agents complexe, mémoire partagée entre sous-agents.

## Critères de succès

- Sur des cas réels, la délégation réduit la consommation totale de tokens de l'agent principal sans dégrader la qualité de la réponse.
- Ajouter un outil cible revient à ajouter un fichier.
- Ajouter un agent revient à ajouter un fichier Markdown.
- `install --dry-run` décrit exactement ce qui sera écrit.
