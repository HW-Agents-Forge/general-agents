# Points ouverts

## Bloquants avant le jalon 1

| # | Question | Impact |
|---|---|---|
| 1 | Quel outil cible en premier (VS Code, Copilot CLI, OpenCode) ? | Détermine la première cible à écrire et à vérifier |
| 2 | ~~Quel est le plus petit modèle (`small`) ?~~ **Réponse : Haiku 5.5** (`claude-haiku-5-5`). Reste à confirmer son identifiant exact dans chaque outil cible | Table de correspondance de la cible |
| 3 | Valeur par défaut de `--target` : un outil, ou `all` ? | Comportement de `install` |

## À trancher pendant le développement

| # | Question | Pistes |
|---|---|---|
| 4 | Fusionner `git` et `svn` en un agent `vcs` ? | Un seul agent détecte le dépôt (moins de recouvrement, un seul prompt) contre deux agents spécialisés (prompts plus ciblés) |
| 5 | Parseur de frontmatter maison (sous-ensemble YAML) ou PyYAML ? | Maison : zéro dépendance mais périmètre à borner. PyYAML : simple mais dépendance |
| 6 | Rendre `--remove` disponible ou s'en passer ? | Voir [install-spec.md](install-spec.md) ; reste désactivable sans conséquence sur le reste |
| 7 | `run` : liste blanche de commandes ou confirmation de l'agent principal ? | Sécurité contre souplesse |
| 8 | Python minimal : 3.10 convient-il à tous vos environnements ? | Syntaxe et typage utilisables |
| 9 | Seuils d'acceptation de l'évaluation (30 % de gain) | À ajuster après les premières mesures |

## À vérifier dans les documentations officielles

- Formats d'agents, emplacements et noms d'outils de chaque cible (voir [targets.md](targets.md)).
- Support de `SKILL.md` et emplacement des skills dans chaque outil.
- Possibilité de clé libre dans le frontmatter pour la marque d'origine.
- Moyen de relever la consommation de tokens du principal et des sous-agents dans chaque outil.
