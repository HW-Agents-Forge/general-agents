# Stratégie de tests

Outil : `pytest`. Tests dans `tests/`, sans accès réseau ni écriture hors des répertoires temporaires (`tmp_path`).

## Niveaux

### Unitaires

| Module | À couvrir |
|---|---|
| `parser` | Frontmatter valide ; champ obligatoire manquant ; clé inconnue ; `name` différent du nom de fichier ; `tier` invalide ; `tools` vide ; corps vide |
| `model` | Construction et validation des dataclasses |
| `registry` | Découverte, ordre déterministe, doublons de noms |
| `targets/*` | Rendu d'un agent et d'un skill ; correspondance modèle et outils ; présence de la marque d'origine |

### Intégration (`installer`)

Dans un faux home temporaire :
- création des fichiers attendus ;
- idempotence (deuxième exécution sans changement) ;
- mise à jour d'un fichier marqué dont la source a changé ;
- **refus d'écraser** un fichier sans marque ;
- `--remove` ne supprime que les fichiers marqués et connus ;
- `--dry-run` n'écrit rien et annonce les mêmes actions que l'exécution réelle ;
- refus d'un chemin qui sort du home (y compris via lien symbolique) ;
- écriture atomique (pas de fichier partiel en cas d'erreur simulée).

### Bout en bout (`cli`)

- Codes de sortie pour chaque cas du tableau de [install-spec.md](install-spec.md).
- Sortie lisible pour `--dry-run`.

## Tests de référence (golden files)

Pour chaque cible, un fichier attendu par agent du catalogue est stocké dans `tests/golden/<outil>/`. Le test compare le rendu à ce fichier. Un changement volontaire de format se traduit par une mise à jour explicite du fichier de référence, revue en même temps que le code.

## Validation des sources du dépôt

Un test parcourt les vrais fichiers de `agents/` et `skills/` et vérifie qu'ils sont valides pour toutes les cibles. Cela empêche de livrer un agent mal formé.

## Qualité

- Couverture visée : ≥ 90 % sur `parser`, `installer` et `targets`.
- Les tests d'`installer` sont prioritaires : c'est là que se concentre le risque.
- Vérifications automatiques locales : tests, lint et typage (voir [conventions.md](conventions.md)).

## Non couvert par ces tests

La qualité réelle des réponses des sous-agents (dépend des modèles) relève de l'évaluation, pas des tests automatiques : voir [evaluation.md](evaluation.md).
