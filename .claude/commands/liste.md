---
description: Construire la liste d'armée d'un palier du plan de peinture
argument-hint: <faction> <format en points>
---

Construis la liste du palier correspondant à : $ARGUMENTS

`/liste` ne construit que des listes de palier (`peinture/plan.md`). Procédure :

0. Normalise les arguments, quelle que soit leur forme :
   - **faction** : compare sans tenir compte de la casse, des accents, des espaces ni des
     tirets aux champs `id`, `nom`, `mfm` et `app40k` de `sources/factions.json`, et
     accepte les abréviations courantes (« SM », « nids »). Retiens l'`id`. Si aucune
     faction ne correspond ou si plusieurs correspondent (« SM/DA », par exemple),
     demande avant de continuer.
   - **format** : garde le nombre de points seul (« 500 », « 500pts », « 500 points »
     donnent `500`). S'il ne figure pas dans le tableau de `regles/formats-maison.md`,
     arrête-toi et dis-le.
1. **Palier** : lis `peinture/plan.md` et `profil.md`. Trouve dans la séquence le palier
   dont la faction (ligne de `profil.md`, par exemple « Space Marines / Dark Angels »)
   et le format correspondent. S'il n'existe pas, arrête-toi et demande s'il faut
   l'ajouter au plan. Un palier de groupe se joue dans une seule faction : si
   l'argument ne précise pas laquelle, demande-la.
2. Lis `regles/construction-armee.md` et `regles/formats-maison.md` pour les limites du
   format.
3. Lis le fichier indiqué par le champ `collection` de la faction dans
   `sources/factions.json`.
4. Son `dossier` contient ses règles (`detachements.md`, `datasheets.md`) et ses
   fichiers `<mfm>-*.tsv` (points, détachements, attachements, options). Plusieurs
   factions peuvent partager un dossier (Space Marines et Dark Angels) : n'utilise que
   les fichiers TSV de la faction demandée.
5. **Fraîcheur** : si le rapport de `/veille` n'est pas dans la conversation, lance
   `python3 -I outils/veille.py --json` (sans Chrome) et lis le statut de chaque source
   utile, sans tenir compte du code de retour : `mfm:<mfm>:fr`, `pdf:pack:<id>:*`,
   `c:40kapp:<app40k>`, `mfm:rassembler:fr`, `pdf:regles-de-base:fr`,
   `pdf:maj-universelles:fr`.
   - Bloquent seulement « modifié », « absent du dépôt » et « erreur ». Bloquent aussi
     l'absence de `datasheets.md` ou `detachements.md`, ou d'une unité de la collection
     dans `datasheets.md`. Dans ces cas, arrête-toi et dis précisément ce qu'il te faut.
   - 40k.app non vérifié (aucune entrée `c:40kapp:*` sans Chrome) ne bloque pas : note-le
     dans « À vérifier » de la liste.
6. **Fichier** : `listes/palier-<NN>-<id>-<points>.md`, `NN` étant le numéro du palier
   dans `plan.md`, sur deux chiffres. Si un fichier `listes/palier-<NN>-*.md` existe,
   pars de lui et modifie-le, sans jamais l'écraser, en conservant « Retour de partie ».
   S'il porte une autre faction du groupe, demande avant de changer de faction.
7. Construis la liste en respectant les règles de `listes/CLAUDE.md`.
8. Enregistre-la et propose un message de commit.
