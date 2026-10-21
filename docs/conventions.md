# Conventions

## Langue

- Documentation et prompts d'agents : français, sauf si un outil impose l'anglais pour un champ précis.
- Code (identifiants, docstrings, messages d'erreur développeur) : anglais.
- Messages affichés à l'utilisateur de `install` : français.

## Python

- Version minimale : 3.11 (`tomllib` pour lire `models.toml`).
- Bibliothèque standard uniquement à l'exécution. Dépendances de développement autorisées : `pytest`, un outil de lint/format (`ruff`), un vérificateur de types (`mypy`).
- Annotations de types partout dans `src/`.
- Dataclasses figées (`frozen=True`) pour le modèle de données.
- Pas d'état global. Les chemins et le home sont passés en paramètre.
- Les erreurs métier lèvent des exceptions de `errors.py`, jamais de `sys.exit` hors de `cli`.
- Fonctions courtes ; un module, une responsabilité (voir [architecture.md](architecture.md)).

## Écriture disque

Toute écriture passe par `installer`. Aucun autre module n'ouvre un fichier en écriture.

## Agents et skills

- Nom d'agent : minuscules, chiffres, tirets ; identique au nom de fichier.
- Description : indique **quand** utiliser l'agent.
- Corps court, contrat de sortie explicite (voir [agent-format.md](agent-format.md)).
- Tout changement de frontière entre agents met à jour le catalogue et le skill `atomic-tasks`.

## Git

- Branches : `feature/<sujet>`, `fix/<sujet>`, `docs/<sujet>`.
- Commits à l'impératif, une idée par commit, message court en première ligne.
- Un changement de format de sortie d'une cible inclut la mise à jour des fichiers de référence de test.

## Revue

Une modification est prête à être fusionnée si :
- les tests, le lint et le typage passent ;
- la documentation concernée est à jour ;
- aucune règle de sécurité de [install-spec.md](install-spec.md) n'est affaiblie sans ADR.

## Décisions

Toute décision structurante (format, sécurité, dépendance, périmètre) est consignée dans `docs/decisions/` selon le modèle de [decisions/README.md](decisions/README.md).
