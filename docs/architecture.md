# Architecture

## Arborescence cible

```
general-agents/
├── agents/                     # descriptions neutres, un .md par agent
├── skills/
│   └── atomic-tasks/SKILL.md
├── install                     # exécutable mince : appelle shuttle.cli.main()
├── models.toml                 # nom du dépôt et modèles par outil et par agent
├── pyproject.toml
├── src/shuttle/
│   ├── __init__.py
│   ├── cli.py                  # arguments, dispatch, codes de sortie
│   ├── model.py                # dataclasses : Agent, Skill, ModelTier, ToolSet
│   ├── config.py               # lecture de models.toml, résolution du modèle par agent
│   ├── parser.py               # lecture du frontmatter + corps
│   ├── registry.py             # découverte des agents et skills
│   ├── targets/
│   │   ├── base.py             # interface Target
│   │   ├── vscode.py
│   │   ├── copilot_cli.py
│   │   └── opencode.py
│   ├── installer.py            # seul module qui écrit sur disque
│   └── errors.py
├── tests/
└── docs/
```

## Flux de données

```
agents/*.md ──► parser ──► model.Agent ──► Target.render ──► installer ──► fichiers du home
skills/*/    ──► parser ──► model.Skill ──┘
```

0. `config` lit `models.toml` à la racine du dépôt.
1. `registry` parcourt `agents/` et `skills/`.
2. `parser` valide chaque source et produit des objets typés (`Agent`, `Skill`). Toute erreur de source est détectée ici.
3. Chaque `Target` transforme un objet typé et le modèle résolu en contenu de fichier propre à l'outil et indique son emplacement d'installation.
4. `installer` écrit (ou simule l'écriture). C'est le seul module qui touche au disque.

## Responsabilités

| Module | Responsabilité | Ne fait pas |
|---|---|---|
| `parser` | Valider et typer les sources | Connaître les outils cibles |
| `config` | Lire `models.toml`, résoudre le modèle de chaque agent pour un outil | Écrire sur disque |
| `model` | Représenter agents, skills, niveaux de modèle, jeux d'outils | Faire des entrées/sorties |
| `targets/*` | Rendu et chemins propres à un outil, tables de correspondance | Écrire sur disque |
| `installer` | Écriture, dry-run, marque d'origine (aucune suppression) | Connaître le format d'un outil |
| `cli` | Interface utilisateur, codes de sortie | Logique métier |

## Interface `Target`

```python
class Target(Protocol):
    name: str
    def agent_path(self, agent: Agent) -> Path: ...
    def skill_path(self, skill: Skill) -> Path: ...
    def render_agent(self, agent: Agent, model: str) -> str: ...
    def render_skill(self, skill: Skill) -> str: ...
```

Chaque cible porte sa table de correspondance des outils abstraits vers les noms d'outils de la plateforme. Les identifiants de modèles ne sont plus dans les cibles : ils viennent de `models.toml` (voir [install-spec.md](install-spec.md)).

## Contraintes

- Python ≥ 3.11 (pour `tomllib`), bibliothèque standard uniquement à l'exécution.
- Sorties déterministes : à entrée identique, contenu généré identique (utile aux tests et aux mises à jour).
- Aucune écriture hors des chemins fournis par les cibles.
- Les erreurs sont typées (`errors.py`) et transformées en messages clairs et codes de sortie par `cli`.
