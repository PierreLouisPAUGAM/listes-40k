# Conventions des listes

Un fichier par liste, nommé `<faction>-<format>-<AAAA-MM>.md`
(ex. `sm-750-2026-12.md`). Les variantes d'une même liste se suivent dans le même fichier
via l'historique git, pas en multipliant les fichiers.

## Modèle

```
# <Nom> — <faction> — <format> pts

- Source des points :
- Détachement(s) et coût en PdD :
- Seigneur de Guerre :

| Unité | Effectif | Attachements | Points |
|---|---|---|---|

Total : X / Y points — Z PdD sur N — O optimisations sur P
Peint : …
Manquant : …
Retour de partie :
```

## Règles

- Détailler le calcul : points ligne par ligne, total, PdD, optimisations.
- Respecter les limites du format (`regles/formats-maison.md`).
- Un appui **doit** être attaché, un meneur non ; une unité ne reçoit qu'un meneur et
  qu'un appui.
- Toujours désigner le Seigneur de Guerre.
- Indiquer ce qui est peint, ce qui est monté, ce qui serait à acheter.
- Citer la version des points utilisée : une liste sans source de points n'est pas valide.
