# 0002. Format source neutre et package shuttle

- Statut : acceptée
- Date : 2026-10-21

## Contexte

Plusieurs outils agentiques sont utilisés (VS Code, Copilot CLI, OpenCode), avec des formats, emplacements, noms d'outils et identifiants de modèles différents.

## Décision

- Les agents sont décrits une seule fois, de façon neutre, dans `agents/` (niveaux de modèle et outils abstraits).
- Un vrai package Python, `shuttle`, adapte ces sources à chaque outil. L'exécutable `install` n'en est que le point d'entrée.
- Une classe de cible par outil, derrière une interface commune.

## Conséquences

- Ajouter un outil = ajouter un module de cible.
- Les correspondances (modèles, outils) sont isolées dans les cibles et peuvent évoluer sans toucher aux sources.
- Le projet a une structure de package (tests, typage, lint) plutôt que celle d'un script.
