# 0005. Bibliothèque standard uniquement à l'exécution

- Statut : proposée
- Date : 2026-10-21

## Contexte

`install` est destiné à être lancé directement depuis un dépôt cloné, sur des machines variées, sans environnement virtuel préparé.

## Décision

Aucune dépendance d'exécution. Le frontmatter est lu par un parseur maison limité à un sous-ensemble de YAML (clés simples, listes courtes). Les dépendances de développement (`pytest`, `ruff`, `mypy`) restent autorisées.

## Conséquences

- Démarrage immédiat, pas d'installation préalable.
- Le sous-ensemble de YAML accepté doit être borné et documenté dans [agent-format.md](../agent-format.md) ; tout le reste est rejeté avec une erreur claire.
- Réversible : si le parseur devient un fardeau, passer à PyYAML demande une nouvelle décision (voir question 5 de [open-questions.md](../open-questions.md)).
