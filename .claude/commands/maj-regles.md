---
description: Intégrer les sources signalées par /veille, ou un document fourni
argument-hint: <faction ou « général »> [document fourni]
---

Intègre les sources de : $ARGUMENTS

Pars du rapport de `/veille` (lance-la s'il n'est pas dans la conversation). Traite les
sources « modifié » ou « absent du dépôt » de cette faction, et les sources générales
signalées (panneau « Rassembler les Armées », Règles de Base, Mises à jour des règles
universelles, appli Règles de Base) si aucune autre intégration ne les a encore prises en
charge. Traite aussi les unités de la collection qui n'ont pas de fiche dans
`datasheets.md` (achat, livraison), même si toutes les sources sont à jour : rédige leur
fiche selon l'étape 4, à partir des mêmes sources que les fiches existantes. Nommage des
bruts, en-tête des fichiers et messages de commit : `sources/procedures.md`, partie 6.

La commande s'exécute sur le Mac qui porte l'appli Warhammer 40,000. Mode d'emploi de
l'outil, recettes et marqueurs à traiter : `outils/appli/README.md`, à lire avant
l'étape 3.

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
   jour `regles/construction-armee.md`. La section 25 de l'appli (Règles de Base >
   25. Rassembler les Armées) la complète ; en cas de désaccord, le panneau du Munitorum
   l'emporte et l'écart est signalé.
4. **Texte des règles** : rédige `datasheets.md` (unités possédées uniquement : profils,
   armes, aptitudes, options d'équipement) et `detachements.md` (règle d'armée, puis
   **tous** les détachements de la faction : règle, optimisations, stratagèmes). Sources
   par ordre de priorité :
   1. **Appli Warhammer 40,000** (officielle) : les codex et suppléments listés dans le
      champ `appli` de la faction dans `sources/factions.json`. Fiches Techniques
      (unités possédées), Règles d'Armée, chaque détachement (règles et coût en PdD,
      Optimisations, Stratagèmes), Mises à Jour & Errata. Recettes et marqueurs ⚠ :
      `outils/appli/README.md`. Enregistre la sortie de `lire` de chaque page, précédée
      d'une ligne `== <chemin dans l'appli>`, dans un brut par faction
      (`sources/procedures.md`, partie 6). Les balises HTML de l'appli deviennent du
      Markdown. Un texte officiel resté en anglais dans l'appli (codex Tyranides) garde
      le renvoi `[O]` avec la mention « en anglais dans l'appli ».
   2. **Pack de Faction français**, pour ce que l'appli ne contient pas, et en
      recoupement de ses errata : télécharge le PDF indiqué par le rapport dans
      `sources/` et extrais-le avec `pdftotext -layout`. Si le Pack et l'appli se
      contredisent, retiens la version la plus récente et signale l'écart.
   3. **40k.app**, en secours seulement, quand l'appli reste inaccessible (« STOP » sans
      réponse de l'utilisateur) : `fetch` dans un onglet Chrome ouvert sur le site
      (`/factions/<id>/army-rules`, `/factions/<id>/detachments/<détachement>`,
      `/factions/<id>/units/<unité>`). Les détachements absents de la page de la faction
      sont sur les pages listées dans `app40k_complements` de `sources/factions.json`.
      L'outil JavaScript ne renvoie que 1 000 caractères : pour un gros volume, dépose le
      texte dans la page et lis-le avec l'outil de lecture de texte. Espace les
      requêtes : le site répond HTTP 429 au-delà d'un certain débit. Lis les tableaux
      cellule par cellule (une ligne par `<tr>`, cellules séparées par « | »), jamais par
      `innerText` de la page entière. Texte anglais marqué `[C]`. L'en-tête cite chaque
      page utilisée, pages complémentaires comprises.
   4. Un document fourni par l'utilisateur (extrait de codex) remplace le passage
      correspondant, marqué `[O]`.

   Noms d'unités, de détachements et d'optimisations : ceux du Munitorum. Dans un texte
   anglais (appli ou 40k.app), remplace-les par leur nom français, retrouvé par la
   colonne `_en` des fichiers TSV (sans tenir compte de la casse) ; sans correspondance :
   nom anglais entre guillemets, « terme français non trouvé ».

   **Mots-clés.** Chaque fiche porte trois lignes :
   - « Mots-clés de faction » : uniquement d'après une source officielle (ligne
     « Mots-clés de Faction » de la fiche de l'appli, bloc « MOTS-CLÉS DE FACTION » d'un
     Pack, document fourni). Sans source : « non donnés, à fournir », et ajoute le
     manque à « À récupérer » du `README.md`.
   - « Rôle » : LIGNE, TRANSPORT ASSIGNÉ, HÉROS ÉPIQUE, PERSONNAGE, ceux que porte la
     fiche, ou « aucun ». Ils servent aux limites de la construction d'armée.
   - « Mots-clés » : tous les autres.

   Chaque mot-clé prend son terme français officiel quand une source officielle française
   le donne : l'appli, `regles/rassembler-les-armees.txt` (LIGNE, TRANSPORT ASSIGNÉ,
   HÉROS ÉPIQUE, PERSONNAGE), l'extrait des Règles de Base dans `sources/`, les fiches du
   Pack de Faction français. Sinon : terme anglais entre guillemets, « terme français non
   trouvé ».

   Avant de passer à la suite, vérifie que chaque détachement de `<mfm>-detachements.tsv`
   et chaque unité de `collection/` ont leur section, et signale ce qui manque.
5. **Règles de Base, Mises à jour des règles universelles** : télécharge, extrais et
   mets à jour les passages utilisés dans `regles/construction-armee.md`. Les errata des
   Règles de Base de l'appli (Règles de Base > Mises à Jour & Errata) se reportent au
   même endroit. La lecture de la section 25 dans l'appli remplace les captures du
   21/09/2026 : retire l'entrée `doc:appli-s25:fr` de `sources/etat.json`.
6. Enregistre l'état des seules sources intégrées :
   `python3 -I outils/veille.py --appli --enregistrer <source> [<source>…]`, où
   `<source>` est un identifiant de source : `mfm:<mfm>:fr`, `pdf:pack:<id>:<langue>`,
   `appli:<id>:fr`, `appli:general:fr`, `c:40kapp:<app40k>`. Si 40k.app a servi de
   secours, ajoute `--navigateur <fichier>` : génère le JavaScript avec
   `python3 -I outils/veille.py --js`, exécute-le tel quel dans un onglet Chrome ouvert
   sur `https://www.40k.app/` et enregistre le JSON renvoyé dans ce fichier. Enregistre
   aussi les Packs de Faction qui n'ont rien à intégrer (absents, ou réduits aux
   Legends) : leur état est connu, la veille ne doit plus les signaler.
7. Régénère le tableau de fraîcheur (`python3 -I outils/veille.py --readme`), mets à
   jour « À récupérer » et « Points en suspens » du `README.md`, puis liste les fichiers
   de `listes/` qui citent une source modifiée : ils sont à revérifier. Un document
   fourni par l'utilisateur s'enregistre à la main dans `sources/etat.json`
   (`sources/procedures.md`, partie 6).
8. Propose les messages de commit, un par domaine.
