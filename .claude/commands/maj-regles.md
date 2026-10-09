---
description: Intégrer les sources signalées par /veille, ou un document fourni
argument-hint: <faction ou « général »> [document fourni]
---

Intègre les sources de : $ARGUMENTS

Pars du rapport de `/veille` (lance-la s'il n'est pas dans la conversation). Traite les
sources « modifié » ou « absent du dépôt » de cette faction, et les sources générales
signalées (panneau « Rassembler les Armées », Règles de Base, Mises à jour des règles
universelles) si aucune autre intégration ne les a encore prises en charge. Nommage des
bruts, en-tête des fichiers et messages de commit : `sources/procedures.md`, partie 6.

Les identifiants `<id>` sont ceux de `sources/factions.json`. Une ligne de `profil.md`
peut en regrouper plusieurs : « Space Marines / Dark Angels » se traite en une fois.

1. **Munitorum** : `python3 -I outils/veille.py --extraire <id> [<id>…]` écrit dans le
   dossier de la faction `<mfm>-points.tsv`, `-detachements.tsv`, `-attachements.tsv`,
   `-options.tsv` (surcoûts d'équipement) (`<mfm>` : nom anglais du Munitorum, ex.
   `tyranids`), et
   `regles/rassembler-les-armees.txt`. Résume le `git diff` (écarts de points, unités
   ajoutées ou retirées) et reprends les avertissements du script.
2. **Collection** : compare le fichier indiqué par le champ `collection` de la faction
   dans `sources/factions.json` et `peinture/plan.md` aux fichiers
   TSV et relève les noms d'unités différents du nom officiel, les unités absentes du
   Munitorum et toute affirmation contredite par les nouvelles données. Propose les
   corrections et ne les applique qu'avec l'accord de l'utilisateur.
3. **Rassembler les Armées** : si `regles/rassembler-les-armees.txt` a changé, mets à
   jour `regles/construction-armee.md`. Ce panneau officiel l'emporte sur les captures
   de l'appli.
4. **Texte des règles** : rédige `datasheets.md` (unités possédées uniquement : profils,
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
      Les détachements absents de la page de la faction sont sur les pages listées dans
      `app40k_complements` de `sources/factions.json`. L'outil JavaScript ne renvoie que
      1 000 caractères : pour un gros volume, dépose le texte dans la page et lis-le
      avec l'outil de lecture de texte. Espace les requêtes : le site répond HTTP 429
      au-delà d'un certain débit. Lis les tableaux cellule par cellule (une ligne par
      `<tr>`, cellules séparées par « | »), jamais par `innerText` de la page entière.
      Texte anglais marqué `[C]`. L'en-tête cite chaque page utilisée, pages
      complémentaires comprises. Noms d'unités, de détachements et d'optimisations
      remplacés par leur nom français, retrouvé par la colonne `_en` des fichiers TSV
      (sans tenir compte de la casse) ; sans correspondance : nom anglais entre
      guillemets, « terme français non trouvé ». Si 40k.app contredit un erratum du
      Pack, le Pack l'emporte et l'écart est signalé.
   3. Un document fourni par l'utilisateur (codex, captures de l'appli) remplace le
      passage communautaire correspondant, marqué `[O]`.

   **Mots-clés.** Sur 40k.app, le bloc « KEYWORDS » d'une fiche mêle le rôle de l'unité
   (BATTLELINE, DEDICATED TRANSPORT, CHARACTER, EPIC HERO…) aux autres mots-clés, et ne
   donne aucun mot-clé de faction. Chaque fiche porte trois lignes :
   - « Mots-clés de faction » : uniquement d'après une source officielle (bloc « MOTS-CLÉS
     DE FACTION » des fiches du Pack, document fourni). Sans source : « non donnés par
     40k.app, à fournir », et ajoute le manque à « À récupérer » du `README.md`.
   - « Rôle » : LIGNE, TRANSPORT ASSIGNÉ, HÉROS ÉPIQUE, PERSONNAGE, ceux que porte la
     fiche, ou « aucun ». Ils servent aux limites de la construction d'armée.
   - « Mots-clés » : tous les autres.

   Chaque mot-clé prend son terme français officiel quand une source officielle française
   le donne : `regles/rassembler-les-armees.txt` (LIGNE, TRANSPORT ASSIGNÉ, HÉROS
   ÉPIQUE, PERSONNAGE), l'extrait des Règles de Base dans `sources/`, les fiches du Pack
   de Faction français. Sinon : terme anglais entre guillemets, « terme français non
   trouvé ».

   Avant de passer à la suite, vérifie que chaque détachement de `<mfm>-detachements.tsv`
   et chaque unité de `collection/` ont leur section, et signale ce qui manque.
5. **Règles de Base, Mises à jour des règles universelles** : télécharge, extrais et
   mets à jour les passages utilisés dans `regles/construction-armee.md`.
6. Enregistre l'état des seules sources intégrées :
   `python3 -I outils/veille.py --enregistrer <id> [<id>…]`, avec `--navigateur` si
   40k.app en fait partie (même procédure que `/veille`, étapes 1 et 2). Enregistre
   aussi les Packs de Faction qui n'ont rien à intégrer (absents, ou réduits aux
   Legends) : leur état est connu, la veille ne doit plus les signaler.
7. Régénère le tableau de fraîcheur (`python3 -I outils/veille.py --readme`), mets à
   jour « À récupérer » et « Points en suspens » du `README.md`, puis liste les fichiers
   de `listes/` qui citent une source modifiée : ils sont à revérifier. Un document
   fourni par l'utilisateur s'enregistre à la main dans `sources/etat.json`
   (`sources/procedures.md`, partie 6).
8. Propose les messages de commit, un par domaine.
