# Skill `atomic-tasks`

Fichier cible : `skills/atomic-tasks/SKILL.md`.

## Rôle

Indiquer à l'agent principal **quand** déléguer à un sous-agent du catalogue et **comment** le faire, pour que la délégation reste rentable.

## Principe de décision

Déléguer si la sortie brute attendue est volumineuse **et** que seule une conclusion est utile. Ne pas déléguer si l'agent principal a besoin du contenu exact pour la suite, ou si l'opération est triviale.

## Table de décision (contenu à reprendre dans le skill)

| Situation | Décision |
|---|---|
| Lancer une commande à sortie longue ou durable (simulation, build, régression) | Déléguer à `run`, en lui donnant la commande exacte en `csh` |
| Chercher où une notion apparaît dans un gros dépôt | Déléguer à `find` |
| Lire un petit fichier, ou quelques lignes précises | Ne pas déléguer, lire directement |
| Écrire ou modifier un fichier | Ne pas déléguer |
| Comprendre l'ampleur d'un changement entre deux révisions | Déléguer à `diff` |
| Retrouver l'auteur ou l'origine d'un changement | Déléguer à `git` ou `svn` |
| Commande courte dont la sortie tient en quelques lignes | Ne pas déléguer |

## Consignes d'invocation

Pour chaque délégation, l'agent principal doit :
1. Formuler une **question précise** (« quels tests échouent et pourquoi ? »), pas une instruction vague.
2. Fournir le **contexte minimal** : chemin, commande, références. Pour `run`, la commande exacte, écrite pour `csh` ; `run` ne l'interprète pas.
3. Préciser le **format attendu** si différent du contrat par défaut.
4. Ne **pas** recopier de gros contenus dans le prompt.

## Après la réponse

- Faire confiance au verdict, mais vérifier avant toute action irréversible.
- Si la réponse signale `tronqué: oui` ou des incertitudes, relancer avec une question plus ciblée plutôt que de relire le contenu brut.
- Ne pas relancer un sous-agent sur la même question sans nouvelle information.

## Structure du fichier

```markdown
---
name: atomic-tasks
description: Quand et comment déléguer des tâches volumineuses (exécution, recherche, diff, historique) à de petits sous-agents. À consulter avant de lancer une commande à sortie longue ou une recherche large.
---

# Quand déléguer
...
# Table de décision
...
# Comment formuler la demande
...
# Après la réponse
...
```

## Contraintes

- Rester court : le skill est chargé dans le contexte de l'agent principal ; chaque ligne a un coût.
- Citer les agents par leur nom du catalogue, jamais par un nom d'outil de plateforme.
- À mettre à jour à chaque ajout ou changement de frontière d'agent (voir [agents-catalog.md](agents-catalog.md)).
