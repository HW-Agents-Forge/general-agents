# Catalogue des agents

Critère d'entrée : l'agent **condense** une sortie volumineuse en une réponse courte. Les agents qui n'apportent que de l'indirection sont exclus (voir [vision.md](vision.md)).

Tous les agents sont en `tier: small` au départ. Aucun n'écrit de fichier de lui-même ; les effets de `run` sont uniquement ceux de la commande fournie par l'agent parent.

## Vue d'ensemble

| Agent | Outils | Entrée type | Sortie |
|---|---|---|---|
| `run` | `shell` | La commande exacte à lancer (syntaxe csh) et ce qu'on veut savoir | Rapport : verdict, code de sortie, points clés |
| `find` | `search`, `read` | Une question sur le dépôt | Chemins et extraits pertinents |
| `diff` | `shell`, `read` | Deux références ou fichiers à comparer | Résumé structuré des changements |
| `git` | `shell` | Une question sur l'historique ou l'état | Réponse digérée |
| `svn` | `shell` | Une question sur l'historique ou l'état | Réponse digérée |

## Frontières (anti-recouvrement)

| Question | Agent |
|---|---|
| « Où est défini X ? Quels fichiers parlent de Y ? » | `find` |
| « Que dit ce gros fichier à propos de Z ? » | `find` |
| « Qu'est-ce qui a changé entre A et B ? » | `diff` |
| « Qui a modifié cette ligne ? Quand ce bug est-il apparu ? » | `git` / `svn` |
| « Quel est l'état de la copie de travail ? » | `git` / `svn` |
| « Lance exactement cette commande, surveille-la et dis-moi ce qui échoue » | `run` |

Règles de départage :
- `diff` compare du contenu. `git` et `svn` interrogent l'historique et l'état d'un dépôt. Si une comparaison porte sur deux révisions, `diff` la fait ; si elle cherche **qui** ou **pourquoi**, c'est `git` ou `svn`.
- `find` n'exécute pas de commande, `run` n'exécute que la commande reçue et ne cherche pas dans le code.
- Question ouverte : fusionner `git` et `svn` en un agent `vcs` (voir [open-questions.md](open-questions.md)).

## Contrats de sortie

Chaque réponse tient dans `max_output_lines` lignes, sans préambule ni conclusion bavarde.

### `run`

Rôle : exécuter dans le terminal la commande **exacte** fournie par l'agent parent, la surveiller pendant son exécution et rendre un rapport. Le shell est `csh`.

Responsabilités :
- L'agent parent fournit la commande complète, déjà écrite pour `csh`. `run` ne la réécrit pas, ne la complète pas, n'ajoute ni option ni redirection de sa propre initiative.
- `run` ne lance **aucune autre commande** que celle reçue (pas de commande d'investigation, pas de relance). Il peut en revanche lire la sortie du terminal et le fichier de log désigné par l'agent parent.
- Il surveille la progression (sortie produite, fin du processus, code de sortie) et rend son rapport à la fin, ou en cas de blocage.
- Il ne diagnostique pas au-delà de ce que la sortie montre : l'analyse et la décision suivante reviennent à l'agent parent.

```
commande: <commande reçue, recopiée telle quelle>
statut: terminé | échec | bloqué | interrompu
code_sortie: <entier, ou « inconnu » si non terminé>
durée: <approximative>
points_clés:
- <erreur ou avertissement utile, une ligne>
extrait: |
  <au plus quelques lignes de sortie brute décisives>
tronqué: oui | non
```

Consignes : ne jamais renvoyer le journal complet ; dédupliquer les erreurs répétées ; `bloqué` si le processus attend une entrée ou ne produit plus rien au-delà du délai prévu, avec la dernière ligne vue ; indiquer `tronqué: oui` si l'analyse a été limitée.
Limites : exécuter la commande telle quelle (la responsabilité de son contenu est à l'agent parent) ; si aucune commande exacte n'est fournie, ne rien lancer et le dire.

### `find`

```
résultats:
- chemin:ligne — <pourquoi pertinent, une ligne>
réponse: <réponse directe à la question, 1 à 3 phrases>
incertitudes: <ce qui n'a pas pu être confirmé>
```

Consignes : classer par pertinence, plafonner le nombre de résultats, citer des lignes vérifiées et non supposées.

### `diff`

```
fichiers_modifiés: <nombre>
résumé: <2 à 4 phrases sur l'intention des changements>
détail:
- chemin — <nature du changement>
risques: <points d'attention, ou « aucun repéré »>
```

### `git` et `svn`

```
réponse: <réponse directe>
preuves:
- <révision ou commit> — <auteur>, <date> — <pourquoi pertinent>
état: <propre | modifié | conflit> (si demandé)
```

Consignes : commandes en lecture seule uniquement (`log`, `blame`/`annotate`, `status`, `show`, `diff`) ; jamais de commit, reset, checkout ou merge.

## Ajouter un agent

Un nouvel agent est accepté s'il :
1. condense réellement une sortie (le gain doit être mesuré selon [evaluation.md](evaluation.md)) ;
2. a une frontière claire avec les agents existants ;
3. a un contrat de sortie court et vérifiable ;
4. demande le minimum d'outils.
