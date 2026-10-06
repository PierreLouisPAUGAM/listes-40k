# Peinture

## `historique.csv`

Une ligne par session. Colonnes :

| Colonne | Contenu |
|---|---|
| `date` | AAAA-MM-JJ |
| `duree_h` | durée en heures, décimale (ex. 2.5) |
| `faction` | SM, TYR, … |
| `unite` | nom français officiel de l'unité |
| `type` | fantassin, personnage, grosse_figurine |
| `nb_figurines` | nombre de figurines travaillées |
| `etape_debut` / `etape_fin` | % d'avancement, ou `socles`, `vernis`, `montage`, `sous-couche` |
| `commentaire` | libre, facultatif |

Exemple : `2026-10-08,3,SM,Escouade Infernus,fantassin,10,90,100,finition des détails`

## Calcul de la vitesse

Temps moyen par figurine, calculé **séparément** pour les fantassins, les personnages et
les grosses figurines. Tant que l'échantillon est faible, toute estimation de durée doit
être présentée comme provisoire. Aucune vitesse ne doit être supposée a priori.

## Disponibilité

Référence : 6 h par semaine en deux sessions, variable selon les semaines. La
disponibilité prévue se note au fil de l'eau dans la conversation, le réalisé dans le CSV.
