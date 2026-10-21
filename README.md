# general-agents

## Objectifs

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

pour gerer l'installation, deux scripts:

- install : permet d'ajouter les agents dans le home
- uninstall : permet de retirer les agents du home

Etant donné que j'utilise plusieurs outils agentiques,
au lieu de developper des agents pour un seul outil,
ajouter uniquement la description dans les fichiers sources 
et utilise un script shuttle pour adapter a l'outil 

- VS Code
- Copilot CLI 
- OpenCode