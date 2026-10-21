# Spécification de `install`

`install` est un exécutable mince qui appelle `shuttle.cli.main()`. Le package s'utilise aussi avec `pip install -e .` (commande `shuttle`).

## Usage

```
install --target {vscode,copilot-cli,opencode} [--dry-run] [--yes] [--home PATH]
```

| Option | Effet |
|---|---|
| `--target` | **Obligatoire.** Un seul outil par exécution. Sans valeur par défaut ni `all` : l'absence de `--target` est une erreur d'usage (code 3). |
| `--dry-run` | Affiche chaque fichier qui serait créé ou mis à jour, sans rien écrire. |
| `--yes` | Ne pas demander de confirmation. |
| `--home PATH` | Racine de substitution du home (tests et essais). |

## Marque d'origine

Tout fichier généré contient `managed-by: general-agents` (voir [targets.md](targets.md) pour la forme selon l'outil). C'est le **seul** critère par lequel `installer` considère qu'un fichier lui appartient.

## Règles de sécurité

1. **Ne jamais écraser un fichier sans marque.** Si la destination existe sans marque, l'opération échoue pour ce fichier avec un message explicite.
2. **Ne jamais supprimer aucun fichier.** `installer` n'expose aucune opération de suppression. Un agent retiré des sources reste installé jusqu'à ce que l'utilisateur le supprime à la main.
3. **Écrire uniquement dans les chemins retournés par les cibles**, résolus sous la racine du home. Refuser tout chemin qui en sortirait (y compris via lien symbolique).
4. **Dry-run fidèle** : mêmes chemins et mêmes décisions que l'exécution réelle, sans effet de bord.
5. **Écriture atomique** : écrire dans un fichier temporaire du même dossier, puis renommer.
6. **Idempotence** : relancer `install` sans changement de source ne modifie rien.

## Actions possibles par fichier

| État de la destination | Action |
|---|---|
| Absente | Créer |
| Présente, marquée, contenu identique | Aucune |
| Présente, marquée, contenu différent | Mettre à jour |
| Présente, sans marque | Refuser, signaler |

## Sortie

Un résumé par fichier (`créé`, `mis à jour`, `inchangé`, `refusé`), puis un total.

## Codes de sortie

| Code | Signification |
|---|---|
| 0 | Succès |
| 1 | Au moins un fichier refusé |
| 2 | Source invalide (erreur de validation) |
| 3 | Erreur d'entrée/sortie ou d'usage |

## Choix retenus

- Aucune suppression par le script : ni `uninstall`, ni `--remove` (ADR 0004). L'utilisateur supprime à la main.
- Installation par **copie** transformée, pas par lien symbolique, car le contenu dépend de l'outil (ADR 0003).
