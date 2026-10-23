# Sources : carte, accès, nommage

Constats du 08/10/2026, appli Warhammer 40,000 ajoutée le 23/10/2026. Les règles d'usage sont dans `sources/CLAUDE.md`. La
vérification et l'intégration passent par `/veille` et `/maj-regles`, qui s'appuient sur
`outils/veille.py` et `outils/appli/` : ce document ne décrit que ce que ces outils ne
disent pas.

## 1. Outils

| Outil | Rôle | Limites |
|---|---|---|
| `outils/veille.py` | Détection (Munitorum, panneau « Rassembler les Armées », API des téléchargements, appli avec `--appli`, PR BSData), `--extraire`, `--enregistrer`, `--readme`, `--js` | Python standard ; l'appli passe par `outils/appli/appli` |
| `outils/appli/appli` | Lecture de l'appli Warhammer 40,000 installée sur le Mac (mode d'emploi : `outils/appli/README.md`) | Mac déverrouillé, compte connecté ; la souris bouge sur certaines pages |
| Chrome (Claude in Chrome) | 40k.app (secours de l'appli), articles Warhammer Community, boutique | Seul accès à ces sites |
| `pdftotext` (poppler, installé par Homebrew le 08/10/2026) | Texte des PDF officiels | Mise en page approximative : relire les tableaux |
| WebFetch | Repérage | Le contenu passe par un modèle de résumé : inutilisable pour transcrire |
| Recherche web | Repérage | Remonte des PDF de la 10e édition : vérifier l'édition avant usage |

Accès impossibles : les codex papier. Leur contenu ne peut venir que de l'utilisateur
(extraits).

## 2. Carte des sources

| Information | Source retenue | Type | Langue | Accès |
|---|---|---|---|---|
| Points, paliers, PdD, noms et coûts des optimisations, meneurs et appuis, surcoûts d'équipement | Inventaire du Munitorum, `mfm.warhammer-community.com/fr/<faction>` | officielle | FR | Script |
| Construction d'armée | Panneau « Rassembler les Armées » du Munitorum ; appli, section 25, en complément | officielle | FR | Script ; `outils/appli` |
| Règles de Base, Mises à jour des règles universelles | PDF de l'API des téléchargements | officielle | FR | Script, puis `pdftotext` |
| Règles de faction contenues dans un Pack de Faction | Pack de Faction PDF | officielle | FR quand il existe | Script, puis `pdftotext` |
| Règles de faction (fiches, règle d'armée, détachements, errata) | Appli Warhammer 40,000 (codex et suppléments listés dans le champ `appli` de `factions.json`) | officielle | FR (codex Tyranides : EN) | `outils/appli` |
| Règles de faction absentes de l'appli | Pack de Faction PDF | officielle | FR quand il existe | Script, puis `pdftotext` |
| Règles de faction, en secours quand l'appli est inaccessible | 40k.app | communautaire | EN | Chrome |
| Contenu des boîtes | Boutique `warhammer.com/fr-FR/shop/<produit>` | officielle | FR | Chrome |
| Annonces (codex, équilibrage, précommandes) | `warhammer-community.com/fr-fr/` | officielle | FR | Chrome |

Situation des factions actives :

- **Space Marines** : codex sorti le 03/10/2026, aucun Pack de Faction.
- **Dark Angels** : règles dans l'appli. Le Pack de Faction anglais v1.3 (30/09/2026)
  ne contient plus que les unités Legends et renvoie à l'appli.
- **Tyranides** : codex, complété par le Pack de Faction français v1.2 (26/08/2026) :
  4 détachements, 3 fiches, errata.

Un Pack de Faction peut compléter un codex sans le remplacer (il le dit en première
page). Quand une faction reçoit son codex ou une mise à jour dans l'appli, son Pack
disparaît ou se réduit aux Legends.

## 3. Détails par source

### Inventaire du Munitorum

- Site Next.js. Les coûts arrivent dans des blocs masqués en fin de page ; le panneau
  « Rassembler les Armées » et la structure (unités, détachements) sont dans les données
  de la page, pas dans le HTML affiché. Le script les lit ; `curl` seul ne montre que les
  noms.
- Les pages `/fr` et `/en` d'une faction partagent les identifiants de leurs blocs :
  c'est la correspondance officielle entre noms anglais et français (colonnes `_en` des
  fichiers TSV).
- Langues : `/en`, `/fr`, `/de`, `/es`, `/it`, `/ja`, `/ko`, `/zh`. `/fr-fr` renvoie une
  erreur 500. Identifiants de faction : slugs anglais (`space-marines`, `tyranids`…).
- La page affiche une version (« v1.5 ») mais aucune date. La v1.5 du 30/09/2026 a été
  modifiée entre le 02/10 et le 05/10/2026 sans changer de numéro : seule l'empreinte du
  contenu fait foi.
- La version française garde des résidus non traduits (« Power of the Hive Mind »,
  « Chameleonic ») et des fautes de la source (virgule manquante dans les gardes du corps
  de Marneus Calgar en v1.5, corrigée en v1.6) : recopiés tels quels, signalés.

### API des téléchargements de Warhammer Community

La page Téléchargements charge sa liste par une requête que l'on peut appeler
directement (paramètre trouvé dans le code JavaScript public du site) :

```sh
curl -s -A 'Mozilla/5.0' -H 'Content-Type: application/json' \
  -X POST https://www.warhammer-community.com/api/search/downloads/ \
  -d '{"index":"downloads_v2","searchTerm":"","gameSystem":"warhammer-40000","language":"french"}' \
  | jq -r '.hits[] | [.title, .id.last_updated, ("https://assets.warhammer-community.com/" + .id.file)] | @tsv'
```

- `language` : `french` ou `english`. Seule `last_updated` fait foi, pas le préfixe date
  des noms de fichiers.
- La page `/fr-fr/downloads/` répond « cette page n'existe pas », mais les PDF français
  sont dans l'API.
- Si la requête cesse de fonctionner, relire les requêtes réseau de la page
  Téléchargements dans Chrome.

### Appli Warhammer 40,000

- Version iPad (« WH 40K ») installée sur le Mac, compte de l'utilisateur, version gratuite
  (suffisante pour la Référence). Lue par `outils/appli/appli` ; plan de l'appli,
  recettes et limites : `outils/appli/README.md`.
- Contenu : codex et suppléments à jour de leurs errata (Space Marines, Dark Angels,
  suppléments de Chapitre, Tyranides), Règles de Base avec la section 25, en français
  sauf le codex Tyranides (anglais au 23/10/2026).
- Datation : « Version des Données » (onglet Profil, v995 au 23/10/2026) et « Dernière
  Mise à Jour » de la page Mises à Jour & Errata des codex et des Règles de Base. Les
  suppléments n'en ont pas : leur empreinte suit la version des données.
- `/veille` les relève par `outils/veille.py --appli` (champ `appli` de `factions.json`
  pour les chemins des codex de chaque faction).

### 40k.app (secours de l'appli)

- Mainteneur et origine des données non indiqués (page de soutien et serveur Discord,
  aucun nom). Points et détachements concordent avec le Munitorum au 08/10/2026.
- Protection Vercel : `curl` reçoit HTTP 429. Dans Chrome, `fetch` depuis un onglet ouvert
  sur le site lit toutes les pages, en espaçant les requêtes.
- Pages : `/factions/<id>`, `/army-rules`, `/detachments/<détachement>`,
  `/units/<unité>`, `/updates` (écarts avec la publication précédente).
- Les détachements de Chapitre des Space Marines sont sur les pages des Chapitres
  (`app40k_complements` de `factions.json`). Le site n'y reproduit pas la restriction au
  Chapitre : la vérifier avant de proposer ces détachements.
- L'outil JavaScript de Chrome ne renvoie que 1 000 caractères : déposer le texte dans la
  page et le lire avec l'outil de lecture de texte.

### BSData `wh40k-11e-mfm`

Collecte automatique du Munitorum. Chaque changement détecté arrive d'abord en PR
ouverte (branche `mfm/auto-update`) avant fusion : le script liste ces PR pour expliquer
un changement, sans s'y fier.

## 4. Sources écartées ou non évaluées

| Source | Statut au 08/10/2026 |
|---|---|
| Wahapedia | Écartée : encore « Faction Pack v1.2 » pour les Space Marines, cinq jours après le codex |
| BSData `wh40k-11e` (catalogues) | Intégration du codex SM non déterminée |
| New Recruit | Non testé |
| ALN 40K (`40k.armylistnetwork.com`) | En français, origine des données non indiquée, listes publiques lisibles sans connexion. Non évalué |
| Goonhammer | Redirige vers `tabletopbattles.com`, raison non vérifiée |
| Bell of Lost Souls, Spikey Bits | Actualités et rumeurs, fiabilité moyenne |

## 5. Termes français

Ordre de recherche d'un terme de jeu :

1. Inventaire du Munitorum `/fr/<faction>` (unités, détachements, optimisations, équipements) ;
2. appli Warhammer 40,000 (armes, aptitudes, mots-clés, règles) ;
3. Pack de Faction et Règles de Base en PDF français ;
4. boutique `warhammer.com/fr-FR` (noms de boîtes et de figurines) ;
5. articles Warhammer Community FR ;
6. documents fournis (extraits de codex).

Sans résultat : nom anglais entre guillemets, « terme français non trouvé ».

## 6. Documents bruts et en-têtes

### Emplacement et nommage

Bruts dans `sources/`, à plat :

```
<document>_<portée>_<version>_<langue>_<AAAA-MM-JJ>.<ext>
```

- `document` : `regles-de-base`, `regles-universelles`, `faction-pack`, `codex`,
  `appli`, `appli-s25`, `boite`…
- `portée` : faction ou produit, en minuscules avec tirets (`tyranides`, `general`).
- `version` : la version officielle quand le document en affiche une (`v1.2`), sinon
  `maj` suivi de la date officielle de mise à jour (`maj2026-08-26`), sinon `sv`. Appli :
  version des données (`donnees-v995`).
- `langue` : `fr` ou `en`. Date finale : date de récupération, suffixe `-01`, `-02` pour
  plusieurs captures du même jour.
- Une source communautaire est préfixée par `communautaire_`.

Les PDF et pages HTML sont exclus de git (`.gitignore`) : on peut les retélécharger.
Leur extrait texte par `pdftotext` est versionné à côté, avec le même nom en `.txt`. Les
captures fournies par l'utilisateur sont versionnées.

Appli : un brut texte par faction, `appli_<id>_donnees-<version>_<langue>_<date>.txt`,
versionné. Il réunit la sortie de `outils/appli/appli lire` de chaque page lue, précédée
d'une ligne `== <chemin dans l'appli>`. Les captures produites par l'outil (PV, armes à
profils) ne sont pas versionnées : leur contenu passe dans les fichiers dérivés.

### Document fourni par l'utilisateur

Ajouter à la main une entrée `doc:<document>:<langue>` dans `sources/etat.json`, de type
`fournie`, avec sa version, sa date et les fichiers qu'il alimente. Le script ne la
compare pas en ligne, mais `--readme` l'affiche.

### En-tête des fichiers dérivés

En tête de tout fichier de `regles/`, `collection/` ou `listes/` alimenté par une source :

```markdown
> **Source** : Inventaire du Munitorum, Tyranides — officielle
> **URL** : https://mfm.warhammer-community.com/fr/tyranids
> **Version** : v1.5
> **Consultée le** : 08/10/2026
> **Brut** : regles/factions/tyranides/tyranids-points.tsv
```

- Un bloc par source. Toutes les pages utilisées sont citées, pages complémentaires
  comprises.
- Source communautaire : `— communautaire, à recouper avec <source officielle>`.
- Une ligne ou une section issue d'une autre source que celle de l'en-tête porte un
  renvoi `[C]` (communautaire) ou `[O]` (officielle), expliqué en tête de fichier.
- Une information absente s'écrit « non trouvé au JJ/MM/AAAA », jamais par déduction.

### Messages de commit

- Bruts et état : `sources: …`. Points : `points: <faction> Munitorum v1.5`. Texte des
  règles : `regles: …`. Collection : `collection: …`.
