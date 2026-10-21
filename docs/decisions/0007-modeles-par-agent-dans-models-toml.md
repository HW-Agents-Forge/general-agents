# 0007. Modèles par agent dans models.toml, script copié

- Statut : acceptée
- Date : 2026-10-21

## Contexte

Les identifiants de modèles dépendent de l'outil et du plan Copilot de l'utilisateur. Le script sera copié tel quel dans d'autres dépôts, avec d'autres agents.

## Décision

- Le modèle est choisi à l'installation, **agent par agent**, jamais en bloc.
- Il vient, par ordre de priorité, de `--model AGENT=MODÈLE`, de la section de l'outil dans `models.toml`, puis de `[defaults]` selon le `tier`.
- `models.toml` est à la racine du dépôt et porte le champ `name`, utilisé dans la marque d'origine `managed-by: <name>`.
- Le script est copié d'un dépôt à l'autre : pas de paramètre `--source`, pas de publication du package. Python ≥ 3.11.
- Aucun modèle n'est jamais choisi par défaut en l'absence de configuration : l'erreur est explicite.

## Conséquences

- Les cibles ne contiennent plus d'identifiants de modèles ; elles gardent leur table de noms d'outils.
- L'identifiant n'est pas vérifié auprès de l'outil (aucun moyen fiable hors ligne) ; seule sa forme l'est.
- Chaque copie du script a son propre `name`, ce qui évite de confondre les fichiers de deux dépôts qui écrivent dans le même home.
