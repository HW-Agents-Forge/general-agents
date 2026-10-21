# 0003. Installation par copie transformée

- Statut : acceptée
- Date : 2026-10-21

## Contexte

Les agents installés dans le home pourraient être des liens symboliques vers le dépôt, ou des fichiers générés.

## Décision

Copie de fichiers **générés** par la cible, portant une marque d'origine.

## Conséquences

- Nécessaire car le contenu dépend de l'outil (le lien symbolique ne peut pas transformer).
- Une modification du dépôt n'est visible qu'après relance de `install` (idempotent, voir [install-spec.md](../install-spec.md)).
- La marque d'origine permet de distinguer les fichiers gérés des fichiers personnels.
