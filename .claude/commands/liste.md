---
description: Construire, en discussion, la liste d'armée d'un palier du plan de peinture
argument-hint: <faction> <format en points>
---

Construis avec l'utilisateur la liste du palier correspondant à : $ARGUMENTS

`/liste` ne construit que des listes de palier (`peinture/plan.md`). C'est une
conversation : tu analyses, tu présentes la situation et des axes, la liste se construit
dans l'échange. Le fichier n'est écrit qu'après accord explicite.

## 1. Analyse silencieuse

Ne rends compte de cette phase que si une donnée bloque : arrête-toi alors et dis
précisément ce qu'il te faut.

1. Normalise les arguments, quelle que soit leur forme :
   - **faction** : compare sans tenir compte de la casse, des accents, des espaces ni des
     tirets aux champs `id`, `nom`, `mfm` et `app40k` de `sources/factions.json`, et
     accepte les abréviations courantes (« SM », « nids »). Retiens l'`id`. Si aucune
     faction ne correspond ou si plusieurs correspondent (« SM/DA », par exemple),
     demande avant de continuer.
   - **format** : garde le nombre de points seul (« 500 », « 500pts », « 500 points »
     donnent `500`). S'il ne figure pas dans le tableau de `regles/formats-maison.md`,
     arrête-toi et dis-le.
2. **Palier** : lis `peinture/plan.md` et `profil.md`. Trouve dans la séquence le palier
   dont la faction (ligne de `profil.md`, par exemple « Space Marines / Dark Angels »)
   et le format correspondent. S'il n'existe pas, arrête-toi et demande s'il faut
   l'ajouter au plan. Un palier de groupe se joue dans une seule faction : si
   l'argument ne précise pas laquelle, demande-la.
3. Lis `regles/construction-armee.md` et `regles/formats-maison.md` pour les limites du
   format.
4. Lis le fichier indiqué par le champ `collection` de la faction dans
   `sources/factions.json`.
5. Son `dossier` contient ses règles (`detachements.md`, `datasheets.md`) et ses
   fichiers `<mfm>-*.tsv` (points, détachements, attachements, options). Plusieurs
   factions peuvent partager un dossier (Space Marines et Dark Angels) : n'utilise que
   les fichiers TSV de la faction demandée.
6. **Fraîcheur** : si le rapport de `/veille` n'est pas dans la conversation, lance
   `python3 -I outils/veille.py --json` (sans Chrome) et lis le statut de chaque source
   utile, sans tenir compte du code de retour : `mfm:<mfm>:fr`, `pdf:pack:<id>:*`,
   `c:40kapp:<app40k>`, `mfm:rassembler:fr`, `pdf:regles-de-base:fr`,
   `pdf:maj-universelles:fr`.
   - Bloquent seulement « modifié », « absent du dépôt » et « erreur ». Bloquent aussi
     l'absence de `datasheets.md` ou `detachements.md`, ou d'une unité de la collection
     dans `datasheets.md`.
   - 40k.app non vérifié (aucune entrée `c:40kapp:*` sans Chrome) ne bloque pas : note-le
     dans « À vérifier » de la liste.
7. **Fichier** : `listes/palier-<NN>-<id>-<points>.md`, `NN` étant le numéro du palier
   dans `plan.md`, sur deux chiffres. Si un fichier `listes/palier-<NN>-*.md` existe,
   la discussion part de lui. S'il porte une autre faction du groupe, demande avant de
   changer de faction. Lis aussi la liste du palier précédent du même groupe.

## 2. Premier retour

Présente, puis arrête-toi et attends la réponse :

- **État de la faction** : unités peintes, en peinture, montées, en grappes ; ce que le
  palier précédent impose de garder. Seules ses figurines sont imposées : donne leur coût
  hors optimisations et la marge qui en découle. Optimisations et détachements se
  rechoisissent à chaque palier.
- **Rappel des règles** : règle d'armée ; détachements accessibles au format, avec leur
  coût en PdD, leurs dispositions de force et leur idée générale ; limites du format.
- **Règles utiles dans ce cas précis** : associations meneur / gardes du corps possibles
  avec la collection, optimisations pertinentes pour les personnages possédés,
  interactions notables entre unités, aptitudes, équipements et règles de détachement,
  pièges et restrictions (détachements de Chapitre, par exemple).
- **Trois axes de construction**, davantage si d'autres s'imposent clairement. Pour
  chacun : idée de jeu, ce qu'il apprend de l'armée, détachement(s), unités clés, points
  forts et faiblesses, effort de peinture (figurines à finir, à monter, à acheter),
  points des figurines et des optimisations séparés, en disant si l'axe garde, change
  ou abandonne les optimisations du palier précédent, cohérence avec le palier précédent et les suivants. Chaque axe respecte les objectifs
  de `profil.md` (apprendre l'armée ; progression : peu de mécaniques nouvelles, pas de
  personnage d'élite trop tôt). Un axe qui s'en écarte le dit et explique pourquoi.

## 3. Discussion

L'utilisateur choisit, mélange ou questionne les axes. Chaque affirmation de règle
renvoie au fichier et à la section ; ce qui repose sur un texte [C] ou sur une donnée
manquante (mots-clés de faction, par exemple) est signalé comme incertain.

## 4. Brouillon

Quand l'axe est arrêté, présente la liste chiffrée selon le modèle et les
règles de `listes/CLAUDE.md` (tableau, total, PdD, optimisations) et l'ordre de peinture, puis
arrête-toi pour les ajustements.

## 5. Écriture

Seulement après accord explicite : enregistre la liste, sans jamais écraser un fichier
existant (modifie-le en conservant « Retour de partie »), puis propose un message de
commit.
