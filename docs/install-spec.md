# Spécification de `install`

`install` est un exécutable mince qui appelle `shuttle.cli.main()`. Le package s'utilise aussi avec `pip install -e .` (commande `shuttle`).

## Usage

```
install --target {vscode,copilot-cli,opencode} [--model AGENT=MODÈLE]... [--dry-run] [--yes] [--home PATH]
```

| Option | Effet |
|---|---|
| `--target` | **Obligatoire.** Un seul outil par exécution. Sans valeur par défaut ni `all` : l'absence de `--target` est une erreur d'usage (code 3). |
| `--model AGENT=MODÈLE` | Répétable. Fixe le modèle d'**un** agent pour cette exécution. Ne s'applique jamais à tous les agents. Un nom d'agent inconnu est une erreur d'usage. |
| `--dry-run` | Affiche chaque fichier qui serait créé ou mis à jour, sans rien écrire. |
| `--yes` | Ne pas demander de confirmation. |
| `--home PATH` | Racine de substitution du home (tests et essais). |

## Modèles et `models.toml`

`models.toml` est à la racine du dépôt, à côté de `agents/` et `skills/`. Il est copié avec le script d'un dépôt à l'autre.

```toml
name = "general-agents"     # identifie le dépôt dans la marque d'origine

[defaults]
small = "claude-haiku-5-5"  # modèle pour tier = small

[copilot-cli]
run = "claude-haiku-5-5"    # modèle d'un agent précis pour cet outil

[vscode]
[opencode]
```

Pour un agent et un outil donnés, le modèle est le premier trouvé parmi :
1. l'option `--model AGENT=MODÈLE` ;
2. la clé `AGENT` de la section de l'outil dans `models.toml` ;
3. la clé du `tier` de l'agent dans `[defaults]`.

Si aucun ne correspond, `install` échoue avec un message qui nomme l'agent et l'outil ; il ne choisit jamais un modèle au hasard. Un agent inconnu dans `models.toml` ou une section d'outil inconnue est signalé comme erreur de configuration (code 2).

`install` ne peut pas vérifier qu'un identifiant existe dans l'outil. Il contrôle seulement sa forme (caractères autorisés, non vide) ; le reste relève de l'utilisateur. `--dry-run` affiche le modèle retenu pour chaque agent.

## Marque d'origine

Tout fichier généré contient `managed-by: <name>`, où `<name>` est le champ `name` de `models.toml` (voir [targets.md](targets.md) pour la forme selon l'outil). C'est le **seul** critère par lequel `installer` considère qu'un fichier lui appartient.

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
| 2 | Source ou configuration invalide (agent, `models.toml`) |
| 3 | Erreur d'entrée/sortie ou d'usage |

## Choix retenus

- Aucune suppression par le script : ni `uninstall`, ni `--remove` (ADR 0004). L'utilisateur supprime à la main.
- Installation par **copie** transformée, pas par lien symbolique, car le contenu dépend de l'outil (ADR 0003).
