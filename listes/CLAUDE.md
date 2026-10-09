# Conventions des listes

Une liste par palier de `peinture/plan.md`, nommée `palier-<NN>-<id>-<points>.md`, où
`<NN>` est le numéro du palier sur deux chiffres et `<id>` l'identifiant de la faction
dans `sources/factions.json` (ex. `palier-03-space-marines-750.md`). Les variantes d'une
même liste se suivent dans le même fichier via l'historique git, pas en multipliant les
fichiers.

## Modèle

```
# Palier n° N — <Nom> — <faction> — <points> pts

- Source des points :
- Détachement(s) et coût en PdD :
- Seigneur de Guerre :
- Axe retenu : <axe>, ce que la liste apprend de l'armée
- Palier précédent : <fichier>, unités retirées : …

| Unité | Effectif | Attachements | Points | Statut |
|---|---|---|---|---|

Total : X / Y points — Z PdD sur N — O optimisations sur P

Découpages possibles : <découpage> — <contrainte éventuelle>

Ordre de peinture :
1. <unité> — <justification>

Manquant : …
À vérifier : …
Retour de partie :
```

## Règles

- Une conversation dédiée **par faction**, alimentée par les données les plus récentes.
- Une liste ne contient qu'une faction. Un palier de groupe (« Space Marines / Dark
  Angels ») se joue dans une seule des factions du groupe.
- La liste est la **cible** du palier : elle se construit avec toute la collection, pas
  seulement le peint. Une unité peinte n'est pas obligée d'y entrer.
- **Montée en puissance progressive** (`profil.md`) : partir de la liste du palier
  précédent du même groupe et la compléter, pour qu'aucune figurine peinte ne soit
  perdue d'un palier à l'autre. Toute unité retirée est signalée, avec la raison. Si le
  palier précédent a été joué dans une autre faction du groupe, signaler ses unités qui
  ne sont pas jouables dans la nouvelle.
- Une escouade de 10 figurines peut être alignée à 5.
- **Découpages possibles** : le tableau donne un découpage de référence. La ligne
  « Découpages possibles » ne liste que des répartitions des mêmes figurines en escouades
  (10 ou 5 + 5, attachement des personnages) qui laissent inchangés les figurines, les
  points et les optimisations, et qui respectent les limites du format. Une variante qui
  change le contenu de la liste passe par l'historique git. Ligne omise s'il n'y en a
  aucun.
- S'approcher au maximum du total **sans le dépasser**. Si l'écart résiduel est
  volontaire, pour préserver la cohérence de la liste, le signaler explicitement.
- Respecter les règles de construction (`regles/construction-armee.md`) et les limites
  du format (`regles/formats-maison.md`) : PdD, optimisations, exemplaires.
- Détailler le calcul : points ligne par ligne, total, PdD, optimisations.
- Citer la version des points utilisée : une liste sans source de points n'est pas valide.
- Colonne Statut : celui de la collection (`collection/CLAUDE.md`), avec l'avancement de
  la peinture. Indiquer sous « Manquant » ce qui serait à acheter.
- **Ordre de peinture** : toutes les unités non terminées de la liste, dans l'ordre où
  les peindre, chacune justifiée par son avancement actuel, le montage nécessaire et les
  priorités de `peinture/plan.md`.
- Le palier est **atteint** quand toutes les unités de sa liste sont terminées au sens
  de `collection/CLAUDE.md`.
