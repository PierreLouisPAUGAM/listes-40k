---
description: Construire une liste d'armée pour une faction et un format donnés
argument-hint: <faction> <format en points>
---

Construis une liste d'armée pour : $ARGUMENTS

Procédure :

1. Lis `regles/construction-armee.md` et `regles/formats-maison.md` pour les limites du
   format demandé.
2. Lis le fichier de collection de la faction dans `collection/`.
3. Trouve la faction dans `sources/factions.json` : son `dossier` contient ses règles
   (`detachements.md`, `datasheets.md`) et ses fichiers `<mfm>-*.tsv` (points,
   détachements, attachements, options). Plusieurs factions peuvent partager un dossier
   (Space Marines et Dark Angels) : n'utilise que les fichiers TSV de la faction demandée.
4. Si le rapport de `/veille` n'est pas dans la conversation, lance
   `python3 -I outils/veille.py` (sans Chrome). **Si une source de la faction est
   modifiée ou absente du dépôt, ou si les points ou les fiches manquent, arrête-toi et
   dis précisément ce qu'il te faut.** Ne construis jamais une liste à partir de ta
   mémoire.
5. Construis la liste en respectant les règles de `listes/CLAUDE.md`.
6. Enregistre-la dans `listes/<faction>-<format>-<AAAA-MM>.md` et propose un message de
   commit.
