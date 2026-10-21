# general-agents

## Objectif

Créer des petits sous-agents, pour atomiser
des taches coûteuses en tokens. 
Ces sous-agents devront utiliser les plus
petits modèles possibles. 

J'ai pensé aux agents suivants :

- run
- read
- write
- list
- diff
- backup
- glob
- find
- git
- svn

> [!NOTE]
> Verifier qu'il n'y a pas de recouvrement. 

Pour que l'agent primaire sache comment et dans
quelles circonstances invoquer un sous agent,
il faut completer le skill atomic-tasks