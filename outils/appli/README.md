# Pilotage de l'appli Warhammer 40,000

`appli` lit le texte officiel de l'appli Warhammer 40,000 (version iPad, « WH 40K »,
installée sur le Mac) par l'accessibilité de macOS. Il permet de récupérer sans
l'utilisateur ce qui venait jusqu'ici de 40k.app ou de captures fournies :

- fiches des unités : profils, armes, aptitudes, options d'équipement, composition,
  mots-clés et mots-clés de faction ;
- règle d'armée et détachements : règle, coût en PdD, optimisations et leur coût,
  stratagèmes ;
- Règles de Base (dont la section 25 « Rassembler les Armées ») ;
- errata (« Mises à Jour & Errata » de chaque codex, datées) et version des données de
  l'appli (onglet Profil).

Les points, PdD et coûts restent ceux de l'Inventaire du Munitorum (`outils/veille.py`).

Outil mis au point le 22 et le 23/10/2026, sur l'appli v2.8.1, données v995.

## Préparation

Compiler (le binaire n'est pas versionné) :

```sh
swiftc -O outils/appli/appli.swift -o outils/appli/appli
```

Puis, avant toute session :

```sh
outils/appli/appli verifier
```

`verifier` contrôle et répare ce qui peut l'être, puis répond `PRÊT`, ou `STOP` suivi de
l'action que seul l'utilisateur peut faire (code de sortie 5) :

| Contrôle | Réparé par `verifier` |
|---|---|
| Autorisations d'accessibilité et d'enregistrement de l'écran du terminal | non : Réglages macOS |
| Mac verrouillé, écran en veille | non : déverrouillage (à distance depuis l'iPhone) |
| `caffeinate -d` (empêche la veille, sans quoi le Mac se verrouille) | oui, lancé pour 2 h |
| Appli fermée ou bloquée | oui, lancée ou relancée |
| Écran d'accueil (abonnement) | oui, « Continuer avec la version gratuite » |
| Taille de la fenêtre | oui : 1 024 de large, pleine hauteur de son écran |
| Compte Warhammer connecté | non : identifiants |

Une session dure plus de 2 h : relancer `verifier`, qui relance `caffeinate`.

Captures : `lire` et `capture` écrivent dans `$APPLI_CAPTURES`, sinon dans un dossier
temporaire. Dans une conversation, pointer `APPLI_CAPTURES` vers le dossier de travail de
la session.

## Commandes

| Commande | Rôle |
|---|---|
| `verifier` | préparation et contrôle, à lancer en premier |
| `accueil` | retour à la racine de Référence, depuis n'importe quel état |
| `appuyer LIBELLÉ [N]` | ouvre une entrée (N-ième occurrence du libellé, 1 par défaut) |
| `atteindre LIBELLÉ` | descend jusqu'à une entrée pas encore chargée et l'amène à l'écran |
| `retour` | bouton retour (son nom change selon la page) |
| `remplir TEXTE` | saisit une recherche (après `appuyer "Recherche de Référence : Bouton"`) |
| `fermer` | ferme un menu « Ajouter aux Favoris » ou la recherche |
| `descendre`, `monter` | défilement d'environ une fenêtre ; code 3 au bout de la page |
| `deplier` | ouvre toutes les rubriques de la page |
| `lire` | toute la page, de haut en bas, une ligne par rangée affichée |
| `ecran` | ce qui est à l'écran |
| `capture FICHIER` | image de la fenêtre seule |
| `etat` | fenêtre, premier plan, et si l'appli répond |
| `relancer` | arrête et relance l'appli, passe l'écran d'accueil |
| `arbre`, `action`, `cliquer`, `reveiller`, `placer` | diagnostic et secours |

`TRACE=1` affiche le détail des opérations sur la sortie d'erreur.

Les libellés sont exacts, accents et apostrophes typographiques compris : les relever
avec `ecran` plutôt que les taper de mémoire.

## Plan de l'appli

```
Référence (racine)
├── Règles de Base → 01. … 25. Rassembler les Armées, Mises à Jour des Règles
│   Universelles, FAQ, Mises à Jour & Errata → sections dépliables
├── <Faction> (ex. Space Marines, Tyranides, Dark Angels, Ultramarines…)
│   ├── Codex: <faction>  ou  Supplément de Codex: <Chapitre>  ou  Codex Supplement: …
│   │   ├── Fiches Techniques → fiches
│   │   ├── Règles d'Armée
│   │   ├── Mises à Jour & Errata (date « Dernière Mise à Jour »)
│   │   └── DÉTACHEMENTS → <détachement> → règles (coût en PdD), Optimisations, Stratagèmes
│   ├── Imperial Armour, Legends, Patrouille…
Profil → « Version des Données »
```

Les détachements de Chapitre des Space Marines sont dans « Supplément de Codex:
<Chapitre> » (Ultramarines, Imperial Fists…), à la racine de Référence.

## Recettes

Après chaque navigation, contrôler la page avec `ecran | head -3` avant d'enchaîner : une
commande lancée sur la mauvaise page lit la mauvaise chose sans erreur.

**Fiche d'une unité**

```sh
A=outils/appli/appli
$A accueil
$A appuyer "Recherche de Référence : Bouton"
$A remplir "Escouade Eliminator"
$A ecran | head -3                                  # libellé exact du résultat
$A appuyer "Escouade Eliminator, Codex: Space Marines"
$A deplier
$A lire
```

Une fiche se lit en 20 à 30 s.

**Détachement**

```sh
$A accueil
$A atteindre "Space Marines" && $A appuyer "Space Marines"
$A appuyer "Codex: Space Marines"
$A atteindre "Force Opérationnelle Gladius" && $A appuyer "Force Opérationnelle Gladius"
$A deplier; $A lire                                  # règles, coût en PdD
$A appuyer "Optimisations"; $A deplier; $A lire; $A retour
$A appuyer "Stratagèmes"; $A deplier; $A lire
```

**Section des Règles de Base, règles d'armée, errata** : même principe (`atteindre`,
`appuyer`, `deplier`, `lire`).

**Liste longue** : `lire` sur la page de la liste. L'index de toutes les fiches (recherche
au champ vide, plus de 1 100 entrées) prend plusieurs minutes : passer par la recherche.

## Lecture de la sortie de `lire`

- Une ligne par rangée affichée ; les éléments d'une même rangée sont séparés par « | ».
  Un élément peut contenir plusieurs lignes de texte (une arme et toutes ses
  caractéristiques, par exemple).
- Armes : « Armes de Tir - <arme>. » puis « Portée : … », « Attaques : … », etc., puis
  « Aptitudes d'Arme. <APTITUDE> - Button. ».
- Points : tableau « Nom de Figurine | Compte | Points », lu rangée par rangée (le
  nombre de points occupe sa propre ligne quand il couvre plusieurs rangées).
- Rubriques en menu (règles, optimisations, stratagèmes) : « <nom>, <coût>, Déplié » puis
  leur texte.
- Stratagèmes : les libellés Quand / Cible / Effet ne sont pas exposés. L'ordre est fixe :
  nom du détachement, moment, cible, effet.
- Texte des règles : balises HTML de l'appli (`<b>`, `<k>` pour un mot-clé, `<u>`,
  `<ul><li>`, `<nest>` pour une aptitude imbriquée), à convertir à la rédaction.
- « Historique Replié : Bouton… » : texte d'ambiance, sans intérêt.

Marqueurs à traiter :

| Marqueur | Signification | Action |
|---|---|---|
| `⚠ PV non exposés … capture <chemin>` | le résumé des caractéristiques de l'appli est faux (« %wounds@ ») | lire les PV sur l'image indiquée |
| `⚠ armes à profils … arme parente probable : <nom> ; captures : <chemin>` | l'appli expose « Frag » au lieu de « Lance-missiles Ballistus - Frag » | vérifier le nom sur l'image |
| `⚠ raccord incertain entre deux écrans` | deux écrans successifs n'ont pas pu être raccordés | vérifier le passage sur `capture` |

## Règles d'usage

- Lancer `verifier` en premier, et le relancer après toute erreur inattendue.
- Ne jamais appuyer sur : « Supprimer mon Compte », « Déconnexion », « Abonnez-vous
  maintenant », « Ajouter aux Favoris ». Ne pas utiliser l'onglet « F. D'ARMÉE » (une
  seule feuille d'armée en version gratuite).
- Ne pas piloter le Finder ni une autre appli par AppleScript : macOS ouvre une demande
  d'autorisation qui bloque l'appli jusqu'à ce que l'utilisateur réponde.
- `deplier` sur les rubriques en menu, `lire` sur ces pages et la descente dans une liste
  plus haute que la fenêtre utilisent la souris : l'appli passe au premier plan et le
  curseur bouge. Prévenir l'utilisateur de ne pas se servir du Mac pendant la session.
  Tout le reste fonctionne avec l'appli en arrière-plan.

## Limites

- Le Codex Tyranides est en anglais dans l'appli (texte officiel non traduit). Des
  passages restent en anglais côté Space Marines (listes de meneurs, FAQ, index de
  recherche).
- Le coût en PdD n'est pas exposé dans la liste des détachements : il figure dans la page
  du détachement.
- Rubriques de fiche : les titres ne sont pas exposés (le contenu reste reconnaissable).
- Pages testées : 7 fiches (infanterie, véhicule, personnages, armes à profils, une fiche
  tyranide), les listes de Référence et l'index, les codex Space Marines et Tyranides, les
  suppléments Dark Angels et Ultramarines, un détachement complet, les règles d'armée, les
  errata, la section 25.03 et le Profil. Une autre structure de page peut exister : une
  sortie incohérente se vérifie sur `capture`.

## Pièges de l'appli neutralisés par l'outil

Pour qui modifie `appli.swift` :

- Les actions d'accessibilité `AXScrollUpByPage` et `AXScrollDownByPage` bloquent l'appli
  sur certains éléments (100 % du processeur, plus de réponse) : l'outil les refuse et
  fait défiler en amenant à l'écran l'élément chargé le plus haut ou le plus bas, ou à la
  molette dans les listes.
- L'appui d'accessibilité sur une rubrique en menu ouvre « Ajouter aux Favoris » : ces
  rubriques s'ouvrent au clic souris, et leur libellé finit par « Replier » (fermée) ou
  « Déplié » (ouverte).
- Les titres de rubrique de fiche s'appellent tous « Déplié » quel que soit leur état :
  une rubrique est jugée repliée quand le titre suivant la touche. Certaines lignes
  (« Endommagé ») ressemblent à des titres sans se déplier : elles sont repérées et
  ignorées.
- Seul le contenu autour de l'écran existe dans l'arbre d'accessibilité, et les titres de
  menu restent collés en haut pendant le défilement : `lire` raccorde les écrans par leur
  recouvrement, pas par leur position.
- La recherche est un calque quand le champ contient du texte, une page quand il est vide.
- L'appli mêle espaces et espaces insécables dans les noms.
- `NSRunningApplication.activate` est refusé à un outil en ligne de commande : le passage
  au premier plan se fait par `open -a`.
- L'appli possède des fenêtres invisibles : la capture vise celle qui s'appelle « WH 40K ».

## Dépannage

| Symptôme | Cause probable | Remède |
|---|---|---|
| « l'appli ne répond pas à l'accessibilité » (code 4) | appli bloquée, ou fenêtre système par-dessus | `relancer`, puis `verifier` ; si ça persiste, l'utilisateur regarde l'écran du Mac |
| « introuvable : <libellé> » | entrée pas encore chargée, libellé inexact, mauvaise page | `ecran`, puis `atteindre` |
| « pas de bouton retour » | page racine, ou recherche ouverte | `accueil` |
| « refusé : l'appli n'est pas au premier plan » | une fenêtre système garde le premier plan | l'utilisateur regarde l'écran du Mac |
| `STOP` de `verifier` | action de l'utilisateur nécessaire | transmettre le message tel quel |
