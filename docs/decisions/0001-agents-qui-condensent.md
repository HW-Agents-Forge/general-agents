# 0001. Ne garder que les agents qui condensent

- Statut : acceptée
- Date : 2026-10-21

## Contexte

La liste initiale contenait `run`, `read`, `write`, `list`, `diff`, `backup`, `glob`, `find`, `git`, `svn`. Déléguer a un coût fixe (prompt système, contexte transmis, aller-retour).

## Décision

Un agent n'est retenu que s'il condense une sortie volumineuse en une réponse courte. Sont retenus : `run`, `find`, `diff`, `git`, `svn`. Sont écartés :
- `read`, `list`, `glob` : redondants avec les outils natifs de l'agent principal ;
- `write` : le contenu à écrire doit déjà être fourni par l'agent principal, donc coût doublé ;
- `backup` : opération déterministe, relève d'un script.

## Conséquences

- Catalogue plus petit et plus cohérent, avec des frontières nettes (voir [agents-catalog.md](../agents-catalog.md)).
- Chaque agent doit prouver son gain par une mesure ([evaluation.md](../evaluation.md)).
- Aucun agent n'écrit de fichier.
