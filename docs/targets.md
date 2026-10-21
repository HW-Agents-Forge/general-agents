# Outils cibles

> **À VÉRIFIER.** Les formats ci-dessous sont des hypothèses de travail. Avant d'écrire chaque cible, confronter ce document à la documentation officielle de l'outil et noter la date de vérification dans la colonne prévue. Les tests de rendu servent ensuite de référence.

## Informations à établir pour chaque outil

| Information | VS Code | Copilot CLI | OpenCode |
|---|---|---|---|
| Emplacement des agents (niveau utilisateur) | À vérifier | À vérifier | À vérifier |
| Extension et nom de fichier | À vérifier | À vérifier | À vérifier |
| Clés du frontmatter (nom, description, outils, modèle) | À vérifier | À vérifier | À vérifier |
| Identifiant du plus petit modèle (`small`) | À vérifier | À vérifier | À vérifier |
| Noms des outils pour `read`, `search`, `shell` | À vérifier | À vérifier | À vérifier |
| Mode sous-agent (invocable par l'agent principal) | À vérifier | À vérifier | À vérifier |
| Emplacement des skills et support de `SKILL.md` | À vérifier | À vérifier | À vérifier |
| Accepte une clé libre pour la marque d'origine | À vérifier | À vérifier | À vérifier |
| Date de vérification | — | — | — |

## Table de correspondance attendue

Chaque cible exprime ces correspondances dans son module.

| Abstrait | Cible concrète |
|---|---|
| `tier: small` | Identifiant du plus petit modèle de l'outil (jamais dans les sources) |
| `tools: [read]` | Nom(s) d'outil de lecture de la plateforme |
| `tools: [search]` | Nom(s) d'outil de recherche |
| `tools: [shell]` | Nom(s) d'outil d'exécution |

## Gestion de la marque d'origine

Si l'outil tolère une clé libre dans le frontmatter, utiliser `managed-by: <name>` (`name` lu dans `models.toml`). Sinon, ajouter un commentaire de première ligne dans le corps. La détection par `installer` doit fonctionner dans les deux cas (voir [install-spec.md](install-spec.md)).

## Ajouter un outil

1. Remplir la colonne correspondante ci-dessus à partir de la documentation officielle.
2. Créer `src/shuttle/targets/<outil>.py` implémentant `Target`.
3. Enregistrer la cible dans le registre des cibles.
4. Ajouter les tests de rendu (voir [testing.md](testing.md)).
5. Mettre à jour ce document avec la date de vérification.
