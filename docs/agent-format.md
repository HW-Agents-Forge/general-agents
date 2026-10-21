# Format source neutre des agents

Chaque agent est un fichier Markdown dans `agents/`, composé d'un **frontmatter** et d'un **corps** (le prompt système).

## Exemple

```markdown
---
name: run
description: Exécute une commande longue (build, tests, scripts) et renvoie un verdict court avec les erreurs utiles. À utiliser quand la sortie brute serait volumineuse.
tier: small
tools: [shell]
max_output_lines: 40
---

Tu exécutes la commande demandée et tu résumes le résultat.
...
```

## Champs du frontmatter

| Champ | Obligatoire | Type | Description |
|---|---|---|---|
| `name` | oui | chaîne | Identifiant, minuscules, chiffres et tirets. Unique. Doit correspondre au nom du fichier. |
| `description` | oui | chaîne | Une à trois phrases. Indique **quand** l'agent principal doit l'invoquer. C'est ce texte que l'outil montre au modèle principal. |
| `tier` | oui | `small` | Niveau de modèle souhaité. Seule valeur admise : `small` (voir ADR 0006). Jamais un identifiant de modèle. |
| `tools` | oui | liste | Outils abstraits autorisés (voir ci-dessous). Liste vide interdite. |
| `max_output_lines` | non | entier | Taille maximale de la réponse, répétée dans le corps comme consigne. Défaut : 40. |

Toute clé inconnue est une erreur de validation.

## Outils abstraits

| Outil abstrait | Signification | Risque |
|---|---|---|
| `read` | Lire des fichiers | Faible |
| `search` | Rechercher par motif ou nom dans l'arborescence | Faible |
| `shell` | Exécuter des commandes | Élevé |

L'écriture de fichiers n'existe pas côté source : aucun agent du catalogue n'en a besoin (voir [vision.md](vision.md)). Chaque cible convertit ces outils en noms propres à la plateforme.

## Niveaux de modèle

| `tier` | Intention |
|---|---|
| `small` | Le plus petit modèle disponible dans l'outil cible. Seul niveau existant : aucun agent n'utilise de modèle plus grand. |

Conséquence pour la rédaction : les prompts doivent rester très courts et très directifs, avec un contrat de sortie rigide et au besoin un exemple de réponse. Une tâche qui exige du raisonnement délicat ne doit pas être confiée à un agent ; elle reste à l'agent principal.

La correspondance vers des identifiants réels est définie **dans chaque cible**, jamais dans les sources.

## Corps

Le corps est le prompt système. Structure recommandée :

1. **Rôle** en une phrase.
2. **Procédure** courte et ordonnée.
3. **Contrat de sortie** : format exact et taille maximale.
4. **Limites** : ce que l'agent ne doit pas faire.

Règles :
- Pas de références à un outil particulier (pas de noms d'outils de plateforme dans le corps).
- Le contrat de sortie est impératif et testable.
- Rester sous environ 60 lignes : le prompt système est payé à chaque appel.

## Marque d'origine

Les fichiers **générés** reçoivent la marque `managed-by: <name>`, où `<name>` est le champ `name` de `models.toml` dans leur frontmatter (ou un commentaire équivalent si l'outil n'accepte pas de clé libre). Elle n'apparaît pas dans les sources. Voir [install-spec.md](install-spec.md).

## Skills

Un skill est un dossier `skills/<nom>/SKILL.md` avec un frontmatter `name` et `description`, suivi d'un corps Markdown. Spécification du skill de ce projet : [skill-atomic-tasks.md](skill-atomic-tasks.md).
