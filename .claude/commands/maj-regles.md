---
description: Intégrer les sources signalées par /veille, ou un document fourni
argument-hint: <faction ou « général »> [document fourni]
---

Intègre les sources de : $ARGUMENTS

Pars du rapport de `/veille` (lance-la s'il n'est pas dans la conversation) et ne
traite que les sources « modifié » ou « absent du dépôt » concernées. Nommage des bruts,
en-tête des fichiers et messages de commit : `sources/procedures.md`, partie 4.

1. **Munitorum** : `python3 -I outils/veille.py --extraire <id>` écrit dans le dossier
   de la faction `<id>-points.tsv`, `-detachements.tsv`, `-attachements.tsv`, et
   `regles/rassembler-les-armees.txt`. Résume le `git diff` (écarts de points, unités
   ajoutées ou retirées) et signale les noms de `collection/` absents des fichiers TSV.
2. **Rassembler les Armées** : si `regles/rassembler-les-armees.txt` a changé, mets à
   jour `regles/construction-armee.md`. Ce panneau officiel l'emporte sur les captures
   de l'appli.
3. **Pack de Faction français** : télécharge le PDF indiqué par le rapport dans
   `sources/`, extrais-le avec `pdftotext -layout`, puis rédige `datasheets.md` (unités
   possédées uniquement) et `detachements.md` (règle d'armée, puis **tous** les
   détachements de la faction : règle, optimisations, stratagèmes).
4. **Faction sans Pack de Faction français** : récupère les mêmes contenus sur 40k.app
   par `fetch`, dans un onglet Chrome ouvert sur le site (`/factions/<id>/army-rules`,
   `/factions/<id>/detachments/<détachement>`, `/factions/<id>/units/<unité>`).
   - Texte des règles en anglais, marqué `[C]`.
   - Noms d'unités, de détachements et d'optimisations remplacés par leur nom français,
     retrouvé par la colonne `_en` des fichiers TSV (comparaison sans tenir compte de la
     casse). Sans correspondance : nom anglais entre guillemets, « terme français non
     trouvé ».
   - Un document fourni par l'utilisateur (codex, captures de l'appli) remplace le
     passage communautaire correspondant, marqué `[O]`.
5. **Règles de Base, Mises à jour des règles universelles** : télécharge, extrais et
   mets à jour les passages utilisés dans `regles/construction-armee.md`.
6. Enregistre l'état des seules sources intégrées :
   `python3 -I outils/veille.py --enregistrer <id> [<id>…]`, avec `--navigateur` si
   40k.app en fait partie (même procédure que `/veille`, étapes 1 et 2).
7. Mets à jour le tableau de fraîcheur du `README.md`, puis liste les fichiers de
   `listes/` qui citent une source modifiée : ils sont à revérifier.
8. Propose les messages de commit, un par domaine.
