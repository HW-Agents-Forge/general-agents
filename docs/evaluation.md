# Évaluation : mesurer les économies de tokens

Sans mesure, déléguer peut coûter plus cher qu'agir directement. Chaque agent doit donc justifier son existence par des chiffres.

## Question posée

Pour une tâche donnée, la consommation totale (agent principal **plus** sous-agent) est-elle inférieure avec délégation, à qualité de réponse égale ?

## Protocole

1. Choisir un **scénario réel** (exemple : lancer la suite de tests d'un projet qui échoue et identifier la cause).
2. Exécuter deux fois, depuis le même état :
   - **Base** : l'agent principal fait tout lui-même.
   - **Délégation** : l'agent principal a accès à l'agent évalué et au skill `atomic-tasks`.
3. Relever, pour chaque exécution :
   - tokens d'entrée et de sortie de l'agent principal ;
   - tokens d'entrée et de sortie du ou des sous-agents ;
   - coût pondéré selon les tarifs des modèles utilisés ;
   - durée ;
   - qualité : la réponse est-elle correcte et suffisante ? (oui / partielle / non).
4. Répéter au moins 3 fois par scénario pour lisser la variance.

## Métriques

| Métrique | Calcul |
|---|---|
| Tokens totaux | principal + sous-agents |
| Coût pondéré | somme (tokens × tarif du modèle) |
| Gain de coût | 1 − coût délégation / coût base |
| Taux de qualité | part des exécutions jugées correctes |

## Seuils d'acceptation (proposés, à confirmer)

- Gain de coût médian ≥ 30 % sur les scénarios cibles de l'agent.
- Taux de qualité en délégation ≥ taux de la base.
- Aucun scénario cible où la délégation coûte plus cher.

Un agent sous le seuil est retravaillé (contrat de sortie, prompt) ou retiré du catalogue.

## Scénarios de départ

| Agent | Scénario |
|---|---|
| `run` | Tests ou build à sortie longue avec quelques erreurs réelles |
| `find` | Trouver tous les usages d'une API dans un dépôt de taille moyenne |
| `diff` | Résumer un changement de plusieurs dizaines de fichiers |
| `git` | Retrouver le commit introducteur d'une régression |
| `svn` | Équivalent sur un dépôt Subversion |

## Organisation

- Les scénarios, relevés et conclusions sont stockés dans `docs/evaluations/` (un fichier par agent et par date).
- La méthode de relevé des tokens dépend de l'outil ; elle est notée dans chaque fichier de résultats.
- Cette évaluation est manuelle au départ. Une automatisation n'est envisagée que si elle devient un frein.
