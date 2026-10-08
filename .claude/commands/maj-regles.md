---
description: Intégrer les sources signalées par /veille, ou un document fourni
argument-hint: <faction ou « général »> [document fourni]
---

Intègre les sources de : $ARGUMENTS

Pars du rapport de `/veille` (lance-la s'il n'est pas dans la conversation). Traite les
sources « modifié » ou « absent du dépôt » de cette faction, et les sources générales
signalées (panneau « Rassembler les Armées », Règles de Base, Mises à jour des règles
universelles) si aucune autre intégration ne les a encore prises en charge. Nommage des
bruts, en-tête des fichiers et messages de commit : `sources/procedures.md`, partie 4.

Les identifiants `<id>` sont ceux de `sources/factions.json`. Une ligne de `profil.md`
peut en regrouper plusieurs : « Space Marines / Dark Angels » se traite en une fois.

1. **Munitorum** : `python3 -I outils/veille.py --extraire <id> [<id>…]` écrit dans le
   dossier de la faction `<mfm>-points.tsv`, `-detachements.tsv`, `-attachements.tsv`
   (`<mfm>` : nom anglais du Munitorum, ex. `tyranids`), et
   `regles/rassembler-les-armees.txt`. Résume le `git diff` (écarts de points, unités
   ajoutées ou retirées) et signale les noms de `collection/` absents des fichiers TSV.
2. **Rassembler les Armées** : si `regles/rassembler-les-armees.txt` a changé, mets à
   jour `regles/construction-armee.md`. Ce panneau officiel l'emporte sur les captures
   de l'appli.
3. **Texte des règles** : rédige `datasheets.md` (unités possédées uniquement : profils,
   armes, aptitudes, options d'équipement) et `detachements.md` (règle d'armée, puis
   **tous** les détachements de la faction : règle, optimisations, stratagèmes). Sources
   par ordre de priorité :
   1. **Pack de Faction français**, s'il existe : télécharge le PDF indiqué par le
      rapport dans `sources/` et extrais-le avec `pdftotext -layout`. Un Pack peut
      compléter un codex sans le remplacer (il le dit en première page) : il ne contient
      alors qu'une partie des détachements et des fiches, et des errata.
   2. **40k.app** pour tout ce que le Pack ne contient pas : `fetch` dans un onglet
      Chrome ouvert sur le site (`/factions/<id>/army-rules`,
      `/factions/<id>/detachments/<détachement>`, `/factions/<id>/units/<unité>`).
      Texte anglais marqué `[C]`. Noms d'unités, de détachements et d'optimisations
      remplacés par leur nom français, retrouvé par la colonne `_en` des fichiers TSV
      (sans tenir compte de la casse) ; sans correspondance : nom anglais entre
      guillemets, « terme français non trouvé ». Si 40k.app contredit un erratum du
      Pack, le Pack l'emporte et l'écart est signalé.
   3. Un document fourni par l'utilisateur (codex, captures de l'appli) remplace le
      passage communautaire correspondant, marqué `[O]`.

   Avant de passer à la suite, vérifie que chaque détachement de `<mfm>-detachements.tsv`
   et chaque unité de `collection/` ont leur section, et signale ce qui manque.
4. **Règles de Base, Mises à jour des règles universelles** : télécharge, extrais et
   mets à jour les passages utilisés dans `regles/construction-armee.md`.
5. Enregistre l'état des seules sources intégrées :
   `python3 -I outils/veille.py --enregistrer <id> [<id>…]`, avec `--navigateur` si
   40k.app en fait partie (même procédure que `/veille`, étapes 1 et 2).
6. Mets à jour le tableau de fraîcheur du `README.md`, puis liste les fichiers de
   `listes/` qui citent une source modifiée : ils sont à revérifier.
7. Propose les messages de commit, un par domaine.
