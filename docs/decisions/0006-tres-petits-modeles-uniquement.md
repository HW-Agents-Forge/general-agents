# 0006. Uniquement de très petits modèles

- Statut : acceptée (amendée par l'ADR 0007)
- Date : 2026-10-21

## Contexte

La première version du format prévoyait deux niveaux, `small` et `medium`. Le but du projet est de réduire le coût en tokens ; un modèle intermédiaire réduit cet avantage.

## Décision

Tous les agents utilisent le plus petit modèle disponible dans l'outil cible. Le niveau `medium` est supprimé : `tier` n'accepte que `small`.

## Conséquences

- Prompts très courts et directifs, contrats de sortie rigides, exemples de réponse si nécessaire ([agent-format.md](../agent-format.md)).
- Les tâches qui demandent du raisonnement délicat ne sont pas déléguées : elles restent à l'agent principal, et le skill `atomic-tasks` doit le dire.
- Les agents les plus exposés (`diff` pour juger l'intention d'un changement, `git`/`svn` pour remonter à une cause) peuvent produire des réponses moins fiables. Ils doivent privilégier les faits (lignes, révisions, auteurs) plutôt que l'interprétation, et l'évaluation ([evaluation.md](../evaluation.md)) doit vérifier la qualité de façon explicite.
- Si un agent échoue durablement à atteindre la qualité avec le plus petit modèle, il est retiré du catalogue ou son rôle est réduit, et non basculé sur un modèle plus grand sans nouvelle décision.

## Amendement (ADR 0007)

`tier` reste limité à `small`, mais l'identifiant de modèle n'est plus imposé : il vient de `models.toml` et peut être remplacé agent par agent. La règle « petits modèles seulement » devient la valeur par défaut, sous la responsabilité de l'utilisateur.
