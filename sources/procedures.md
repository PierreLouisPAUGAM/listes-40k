# Sources d'information : accès, rapatriement, veille

Cartographie établie le 06/10/2026. Chaque constat d'accès a été testé ce jour-là ; les
résultats peuvent changer sans préavis. Revérifier un accès avant de déclarer une source
inaccessible.

## 1. Capacités disponibles

| Capacité | Disponible | Vérification du 06/10/2026 |
|---|---|---|
| Requêtes HTTP brutes (`curl`, `wget`) | Oui | `curl 8.5.0` exécuté sur une quinzaine d'URL, codes retour consignés en partie 2 |
| Récupération web résumée (WebFetch) | Oui, avec réserve | Testé sur `mfm.warhammer-community.com/fr/dark-angels` : répond. Le contenu passe par un modèle de résumé : **inutilisable pour transcrire des points ou des profils**, à réserver au repérage |
| Recherche web (WebSearch) | Oui | Plusieurs recherches effectuées. Résultats orientés vers l'anglais, et remontent souvent des PDF **périmés** de la 10e édition (voir 2.1) |
| Pilotage de Chrome (Claude in Chrome) | Oui | Onglet ouvert, navigation, exécution de JavaScript, lecture de texte, capture d'écran. Indispensable pour les pages rendues en JavaScript (Téléchargements de Warhammer Community, panneau « Rassembler les Armées » du Munitorum, boutique warhammer.com) |
| Connecteurs MCP | Chrome et Claude Docs uniquement | Aucun connecteur lié au jeu (pas d'accès à l'appli Warhammer 40,000) |
| Exécution de scripts | Oui | `python3` (sans `pip`, modules tiers absents sauf `requests`), `node`/`npm`, `jq`, `git` |
| Lecture de PDF | Oui | `pdftotext`, `pdfinfo`, `pdftoppm` (poppler) présents ; lecture directe des PDF par l'outil de lecture de fichiers |
| Lecture d'images (captures de l'appli) | Oui, par lecture visuelle | Pas d'OCR installé (`tesseract`, `ocrmypdf` absents). Les captures sont lues visuellement, une par une : fiable pour un texte net, à relire pour les chiffres |
| Conversion de formats | Limitée | Pas de `pandoc`, `libreoffice` ni ImageMagick. PDF → texte et PDF → image possibles via poppler |
| API GitHub | Oui, sans authentification | `api.github.com` répond (quota anonyme limité) |

**Règle d'accès** : quand une page est inaccessible ou vide par `curl` ou WebFetch,
réessayer avec Chrome avant de conclure. Un échec ne se consigne qu'après cet essai.

Limites constatées :

- **Appli Warhammer 40,000** : aucun accès. Elle demande un compte et, pour une partie du
  contenu, un abonnement. Je ne crée pas de compte et ne saisis pas d'identifiants.
- **Codex papier** : aucun accès. Seul l'utilisateur peut en fournir des extraits.
- **Protections anti-robot** : `warhammer.com` renvoie une réponse vide (code 202) en
  `curl`, mais s'affiche normalement dans Chrome. `www.39k.pro` et
  `www.warhammer-forum.com` n'ont pas répondu (délai dépassé). Aucune tentative de
  contournement.

## 2. Cartographie des sources

Légende : **O** = officielle, **C** = communautaire. « Seul » = je peux l'atteindre sans
aide ; « À fournir » = l'utilisateur doit déposer le document.

### 2.1 Règles de base 11e en français

| Source | Type | FR | Format | Mise à jour | Accès |
|---|---|---|---|---|---|
| PDF « Règles de Base », Warhammer Community | O | Oui | PDF | Rare | **Seul**, via l'API des téléchargements (2.9). Version française « mise à jour le 01/06/2026 » : `fre_01-06_warhammer40k_new40k_core_rules-ooyuallyp9-s4aczdfbm2.pdf` |
| Wahapedia, `wahapedia.ru/wh40k11ed/the-rules/core-rules/` | C | Non | HTML | Suit les publications | Seul (`curl` 200) |

Constats :

- La page française `/fr-fr/downloads/` renvoie « Désolé, cette page n'existe pas ».
  Les PDF français sont pourtant publiés : on les obtient par l'API décrite en 2.9.
- Le PDF français 11e déjà utilisé par le projet est daté du 05/06/2026 ; l'API indique
  une mise à jour au 01/06/2026. Écart non expliqué : comparer les deux fichiers avant
  de remplacer celui du projet.
- La recherche web remonte
  `assets.warhammer-community.com/warhammer40000_core&key_corerules_fre_24.09-o8xvsjfbj1.pdf` :
  en-tête `Last-Modified` du 25/09/2024, donc **10e édition, à ne pas utiliser**. Même
  piège pour `warhammer40000_indexes_faqs&errata-fre_16.10.pdf` (23/10/2024).
### 2.2 Construction d'armée (« Rassembler les Armées »)

| Source | Type | FR | Format | Accès |
|---|---|---|---|---|
| Appli Warhammer 40,000, section 25 | O | Oui | Appli | **À fournir** (captures) |
| Inventaire du Munitorum, panneau « Rassembler les Armées » (toute page faction, ex. `mfm.warhammer-community.com/fr/tyranids`) | O | Oui | HTML rendu en JavaScript | **Seul, via Chrome** (panneau dépliable). Absent du HTML récupéré par `curl` |

Le panneau du Munitorum (environ 5 800 caractères le 06/10/2026) couvre : Commencer sa
feuille d'armée, Choisir une faction d'armée, Choisir le format de la bataille (tableau
Incursion / Force de Frappe), Remplir votre feuille d'armée, Choisir des détachements,
Choisir des unités, Attacher les unités de meneur et d'appui, Choisir des optimisations.
**Non vérifié** : s'il reprend l'intégralité de la section 25 de l'appli ou un résumé.
Le comparer une fois avec `regles/construction-armee.md` avant de s'y fier seul.

### 2.3 Inventaire du Munitorum (points)

| Source | Type | FR | Format | Mise à jour | Accès |
|---|---|---|---|---|---|
| `mfm.warhammer-community.com/fr/<faction>` | O | Oui | HTML rendu côté serveur | À chaque mise à jour d'équilibrage ou sortie de codex | **Seul, par `curl`** |
| Page Téléchargements 40k, `warhammer-community.com/en-gb/downloads/warhammer-40000/` (carte « Munitorum Field Manual ») | O | Non | Page JS | Affiche la date de mise à jour | Seul, via Chrome : « Updated 30/09/2026 » le 06/10/2026 |
| BSData `wh40k-11e-mfm` (`github.com/BSData/wh40k-11e-mfm`) | C | Non | YAML par faction + journal des modifications | Collecte quotidienne automatique | Seul (`curl`, API GitHub) |

**Revérification du blocage signalé le 21/09/2026 : le blocage n'est plus constaté.**
Le 06/10/2026, `curl` avec un en-tête de navigateur courant obtient un code 200 et le
contenu complet sur `/fr`, `/fr/tyranids`, `/fr/space-marines`, `/fr/dark-angels`
(site Next.js hébergé chez Vercel, pages pré-rendues). WebFetch obtient aussi la page.
Les causes possibles du blocage antérieur (en-tête, adresse, protection retirée) ne sont
pas connues.

Détails utiles :

- Langues : `/en`, `/fr`, `/de`, `/es`, `/it`, `/ja`, `/ko`, `/zh`. Attention :
  `/fr-fr` renvoie une erreur 500.
- Identifiants de faction (slugs anglais, identiques dans toutes les langues) :
  `space-marines`, `dark-angels`, `tyranids`, etc. La liste complète figure en tête de
  `mfm.warhammer-community.com/en`.
- La page affiche la **version** (« v1.5 ») mais **aucune date**. La date se lit sur la
  page Téléchargements (carte Munitorum) ou dans le journal BSData.
- Les mentions « MIS À JOUR » et « DISPOSITION(S) DES FORCES MODIFIÉE(S) » signalent ce
  qui a changé depuis la version précédente.
- Les unités Legends et le texte de bienvenue ne sont visibles qu'avec JavaScript
  (interrupteur « Montrer les unités Legends »).
- La version française contient des résidus non traduits (ex. optimisations tyranides
  « Power of the Hive Mind », « Chameleonic » le 06/10/2026). Les signaler, ne pas les
  traduire soi-même.

État constaté le 06/10/2026 : version **v1.5** pour Space Marines, Dark Angels et
Tyranides. Selon BSData, v1.5 a paru le **30/09/2026**, avec des changements massifs
côté Space Marines (69 unités retirées, 5 ajoutées, 14 détachements ajoutés), ce qui
laisse penser qu'elle intègre déjà le codex Space Marines. **À confirmer** par
l'annonce officielle.

### 2.4 Datasheets, détachements, optimisations, stratagèmes

Les noms, coûts en PdD et coûts des optimisations sont dans l'Inventaire du Munitorum
FR (2.3). Le texte des règles (profils, aptitudes, règles de détachement, effets des
optimisations, stratagèmes) se trouve dans les sources suivantes.

| Source | Type | FR | Format | Accès |
|---|---|---|---|---|
| Packs de Faction PDF (API, 2.9) | O | **Oui** | PDF | **Seul.** Le 06/10/2026 : 22 Packs de Faction en français. « Pack de Faction: Tyranids » mis à jour le 26/08/2026. Aucun Pack de Faction Space Marines ni Dark Angels (remplacés par le codex) ; il reste « Dark Angels legends » en anglais seulement |
| Codex Space Marines (papier, sorti le 03/10/2026) | O | Oui (`codex-space-marines-2026-fre` en boutique) | Livre | **À fournir** (photos ou saisie) |
| Appli Warhammer 40,000 | O | Oui | Appli | **À fournir** (captures). Seul support de la mise à jour numérique Dark Angels selon la presse communautaire (Bell of Lost Souls), non confirmé par une source officielle |
| Wahapedia, `wahapedia.ru/wh40k11ed/factions/<faction>/` | C | Non | HTML | Seul (`curl` 200 ; la racine `/wh40k11ed/` renvoie 403, pas les sous-pages). Contenu complet : datasheets, règles de détachement, optimisations, stratagèmes |
| BSData `wh40k-11e` (`github.com/BSData/wh40k-11e`) | C | Non | Catalogues JSON par faction | Seul. Commits quotidiens (dernier le 05/10/2026). Intégration du codex SM non déterminée : les métadonnées du catalogue ne citent que l'Index de 2023 |
| New Recruit, `newrecruit.eu` | C | Non vérifié | Application web | Page d'accueil accessible ; contenu non testé |

Fraîcheur de Wahapedia au 06/10/2026 :

- Tyranides : « Faction Pack 11 — v1.2 — August 2026 », cohérent avec le Pack de Faction
  officiel du 26/08/2026.
- Space Marines et Dark Angels : encore « Faction Pack 11 — v1.2 », alors que le codex
  est sorti le 03/10/2026. **Périmé** pour ces factions tant que ce tableau n'a pas changé.

Wahapedia indique sa source dans un tableau « Book / Kind / Edition / Version / Last
update » en tête de chaque faction : toujours le relever.

### 2.5 Ce qui n'existe en français que dans le codex ou l'appli

Pour les Space Marines et les Dark Angels, depuis le codex : le texte français des
datasheets, des règles de détachement et des stratagèmes. Les sources communautaires
donnent un équivalent anglais, mais aucune n'est encore à jour du codex au 06/10/2026.

### 2.6 Équilibrage, errata, FAQ

| Source | Type | FR | Accès |
|---|---|---|---|
| Articles Warhammer Community FR (ex. « Mise à Jour d'Équilibrage : l'Astartes Renforcé », 30/09/2026) | O | Oui | Seul, via Chrome (texte rendu en JS ; `curl` ne récupère que le menu) |
| « Mises à jour des règles universelles » (API, 2.9) | O | Oui | Seul. Mis à jour le 26/08/2026 |
| Wahapedia (FAQ et errata intégrés aux pages) | C | Non | Seul |

### 2.7 Contenu des boîtes

| Source | Type | FR | Accès |
|---|---|---|---|
| Boutique `warhammer.com/fr-FR/shop/<produit>` | O | Oui | **Seul, via Chrome uniquement** (`curl` : réponse vide). Ex. « Patrouille : Couvain d'Assaut Tyranide » : 18 figurines, composition décrite en français |
| Articles « que contient la boîte » de Warhammer Community FR | O | Oui | Seul, via Chrome |
| Détaillants (ex. `philibertnet.com`) | C | Oui | Seul (`curl` 200). Moins fiable que la boutique officielle |

### 2.8 Actualités (codex, éditions, retraits d'unités)

| Source | Type | FR | Accès |
|---|---|---|---|
| Warhammer Community FR, `warhammer-community.com/fr-fr/` | O | Oui | Seul : accueil en `curl`, articles via Chrome. Pas de flux RSS (`/feed` : 403) |
| Boutique `warhammer.com/fr-FR/shop/warhammer-40000/pre-order` | O | Oui | Seul, via Chrome |
| Reddit r/WarhammerCompetitive (`/.rss`) | C | Non | Seul (`curl` 200) |
| Goonhammer | C | Non | `goonhammer.com` redirige (301) vers `tabletopbattles.com` le 06/10/2026 ; raison non vérifiée |
| Bell of Lost Souls, Spikey Bits | C | Non | Vus en résultats de recherche ; fiabilité moyenne (sites d'actualité et de rumeurs) |

### 2.9 API des téléchargements de Warhammer Community

La page Téléchargements charge sa liste par une requête que le site fait lui-même. On
peut l'appeler directement, sans navigateur. Elle donne, pour chaque document : titre
(en français pour la langue `french`), date de création, date de dernière mise à jour,
taille et nom du fichier PDF.

```sh
curl -s -A 'Mozilla/5.0' -H 'Content-Type: application/json' \
  -X POST https://www.warhammer-community.com/api/search/downloads/ \
  -d '{"index":"downloads_v2","searchTerm":"","gameSystem":"warhammer-40000","language":"french"}' \
  | jq -r '.hits[] | [.title, .id.last_updated, .id.file_size,
      ("https://assets.warhammer-community.com/" + .id.file)] | @tsv'
```

- `language` : `french` ou `english` (37 documents en anglais, 27 en français le
  06/10/2026). La carte Munitorum n'y figure pas : c'est un lien vers le site, pas un PDF.
- Le paramètre a été trouvé dans le code JavaScript public du site. Si la requête cesse
  de fonctionner, ouvrir la page Téléchargements dans Chrome et relire ses requêtes
  réseau.
- Les PDF français portent le préfixe `fre_` ; le préfixe date (`30-09_`) est absent de
  certains noms. Seule `last_updated` fait foi.

## 3. Sources communautaires retenues

| Source | Maintenance | Délai après publication | Réputation | FR | Retour au terme officiel FR |
|---|---|---|---|---|---|
| **BSData `wh40k-11e-mfm`** | Collecte automatique quotidienne du site officiel, validée par schéma et tests ; PR par changement | 1 jour (v1.5 publiée le 30/09, intégrée le 30/09–01/10) | Organisation BSData, qui fournit les données de BattleScribe ; New Recruit s'en sert aussi (non vérifié directement) | Non | Les identifiants (`slug`) et l'ordre des entrées sont ceux du site officiel : aligner avec la page `/fr/<faction>` correspondante |
| **Wahapedia** | Financé par dons et abonnements (liens Patreon et Boosty sur l'accueil) ; équipe non identifiée ; couvre les éditions 8 à 11 | Variable : pas encore à jour du codex SM trois jours après sa sortie | Très citée par les sites anglophones (ex. Spikey Bits) ; réputation non évaluée au-delà | Non (aucun sélecteur de langue) | Retrouver chaque nom dans le Munitorum FR ; pour les règles, dans le codex ou l'appli FR |
| **BSData `wh40k-11e`** | Bénévoles, correctifs liés à des tickets, commits quotidiens | Quelques jours à quelques semaines | Données utilisées par New Recruit | Non | Comme ci-dessus |

Règles d'usage :

- Une donnée issue d'une source communautaire porte la mention **communautaire** dans le
  fichier où elle est consignée (voir partie 4), pour être recoupée plus tard.
- En cas de contradiction, la source officielle l'emporte, et la contradiction est
  signalée dans le fichier et à l'utilisateur.
- **Aucune traduction maison** d'un terme de jeu. Ordre de recherche du terme français :
  1. Inventaire du Munitorum `/fr/<faction>` (unités, détachements, optimisations) ;
  2. boutique `warhammer.com/fr-FR` (noms de boîtes et de figurines) ;
  3. articles Warhammer Community FR ;
  4. Packs de Faction et Règles de Base en PDF français ;
  5. documents fournis (codex, captures de l'appli).
  Si aucun ne donne le terme, garder le nom anglais entre guillemets avec la mention
  « terme français non trouvé ».

## 4. Rapatriement dans le dépôt

### 4.1 Emplacement des documents bruts

Tout document brut va dans `sources/`, à plat. Un document brut est conservé tel que
récupéré : PDF, capture, page HTML enregistrée, ou texte extrait par script s'il ne
s'agit que d'une transcription mécanique.

### 4.2 Nommage

```
<document>_<portée>_<version>_<langue>_<AAAA-MM-JJ>.<ext>
```

- `document` : `regles-de-base`, `munitorum`, `faction-pack`, `codex`, `appli-s25`,
  `equilibrage`, `boite`…
- `portée` : faction ou produit, en minuscules avec tirets (`tyranides`,
  `space-marines`, `general`).
- `version` : version officielle (`v1.5`) ; à défaut, `maj` suivi de la date officielle
  de mise à jour (`maj2026-09-30`) ; à défaut, `sv` (sans version).
- `langue` : `fr` ou `en`.
- Date finale : **date de récupération**. Plusieurs captures d'un même jour prennent un
  suffixe `-01`, `-02`.
- Une source communautaire est préfixée par `communautaire_`.

Exemples : `munitorum_tyranides_v1.5_fr_2026-10-06.html`,
`appli-s25_general_sv_fr_2026-09-21-01.png`,
`communautaire_wahapedia_space-marines_fp-v1.2_en_2026-10-06.html`.

### 4.3 En-tête des fichiers de données dérivés

En tête de tout fichier de `regles/`, `collection/` ou `listes/` alimenté par une source :

```markdown
> **Source** : Inventaire du Munitorum, Tyranides — officielle
> **URL** : https://mfm.warhammer-community.com/fr/tyranids
> **Version** : v1.5, publiée le 30/09/2026
> **Consultée le** : 06/10/2026
> **Brut** : sources/munitorum_tyranides_v1.5_fr_2026-10-06.html
```

- Plusieurs sources : un bloc par source.
- Une source communautaire : `— communautaire, à recouper avec <source officielle>`.
- Une ligne ou une cellule issue d'une source différente de l'en-tête porte un renvoi
  `[C]` (communautaire) ou `[O]` (officielle), expliqué en tête de fichier.
- Une information non trouvée s'écrit « non trouvé au JJ/MM/AAAA », jamais par déduction.

### 4.4 Tableau de fraîcheur du README

À chaque intégration, mettre à jour la ligne correspondante de « Fraîcheur des sources »
dans `README.md` : nom de la source, version et date officielle, usage dans le projet,
état (`À jour` au JJ/MM/AAAA, ou `PÉRIMÉ` depuis telle publication). Une ligne par
source, pas d'historique dans ce tableau (git le garde). Mettre aussi à jour « À
récupérer » et « Procédures de recherche » si l'accès a changé.

### 4.5 Messages de commit

- Dépôt d'un brut seul : `sources: Munitorum Tyranides v1.5 (FR)`.
- Données dérivées : préfixe du domaine (`points:`, `regles:`, `collection:`), avec la
  version source : `points: Tyranides Munitorum v1.5`.
- Procédures et cartographie : `sources: procédures d'accès et de veille`.

## 5. Veille à la demande

À lancer avant de construire une liste et à chaque annonce de mise à jour.

1. **Version du Munitorum** (officielle, sans navigateur) :
   ```sh
   for f in space-marines dark-angels tyranids; do
     printf '%s ' "$f"
     curl -s -A 'Mozilla/5.0' "https://mfm.warhammer-community.com/fr/$f" \
       | grep -oE '>v[0-9]+\.[0-9]+<' | head -1
   done
   ```
   Comparer avec la version du tableau de fraîcheur. Si elle a changé, chercher les
   mentions « MIS À JOUR » sur la page.
2. **Date et contenu des changements** : `DATA-CHANGELOG.md` de BSData
   `wh40k-11e-mfm` (communautaire, à recouper) liste chaque version avec sa date et les
   écarts de points par faction.
3. **Documents PDF** : requête de la partie 2.9 en `french`. Comparer la colonne
   `last_updated` des Règles de Base, des Packs de Faction concernés et des « Mises à
   jour des règles universelles » avec le tableau de fraîcheur. La date de la carte
   Munitorum se lit sur la page Téléchargements, via Chrome.
4. **Annonces** : accueil de Warhammer Community FR (articles d'équilibrage, codex,
   précommandes) et page Précommandes de la boutique FR.
5. **Wahapedia** (si utilisé) : tableau « Version / Last update » de la faction, pour
   savoir si le site a intégré la dernière publication.

Résultat :

- Rien n'a changé : noter « vérifié le JJ/MM/AAAA » dans la colonne État du tableau de
  fraîcheur.
- Une source a changé : marquer la ligne `PÉRIMÉ depuis <publication>`, ajouter la
  récupération à « À récupérer », lister les fichiers de `regles/` et les listes de
  `listes/` qui en dépendent, puis lancer `/maj-regles` si l'utilisateur le demande.
