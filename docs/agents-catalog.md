# Catalogue des agents

Critère d'entrée : l'agent **condense** une sortie volumineuse en une réponse courte. Les agents qui n'apportent que de l'indirection sont exclus (voir [vision.md](vision.md)).

Tous les agents sont en `tier: small` au départ. Ils ne modifient jamais de fichier.

## Vue d'ensemble

| Agent | Outils | Entrée type | Sortie |
|---|---|---|---|
| `run` | `shell` | Une commande et ce qu'on veut savoir | Verdict, code de sortie, erreurs utiles |
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
| « Lance les tests / le build et dis-moi ce qui échoue » | `run` |

Règles de départage :
- `diff` compare du contenu. `git` et `svn` interrogent l'historique et l'état d'un dépôt. Si une comparaison porte sur deux révisions, `diff` la fait ; si elle cherche **qui** ou **pourquoi**, c'est `git` ou `svn`.
- `find` n'exécute pas de commande arbitraire, `run` ne fait pas de recherche dans le code.
- Question ouverte : fusionner `git` et `svn` en un agent `vcs` (voir [open-questions.md](open-questions.md)).

## Contrats de sortie

Chaque réponse tient dans `max_output_lines` lignes, sans préambule ni conclusion bavarde.

### `run`

```
verdict: ok | échec | partiel
code_sortie: <entier>
durée: <approximative>
points_clés:
- <erreur ou avertissement utile, une ligne>
extrait: |
  <au plus quelques lignes de sortie brute décisives>
tronqué: oui | non
```

Consignes : ne jamais renvoyer le journal complet ; dédupliquer les erreurs répétées ; indiquer `tronqué: oui` si l'analyse a été limitée.
Limites : refuser les commandes destructives (suppression récursive, écriture hors du dépôt, accès réseau non demandé) et demander confirmation à l'agent principal.

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
