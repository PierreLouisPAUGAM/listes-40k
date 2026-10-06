# Projet « Listes 40k »

Construire des listes d'armée Warhammer 40,000 (11e édition) à partir des figurines
possédées, et en déduire un ordre de peinture. Le projet gère le **quoi** et le **quand**
peindre, jamais le **comment** (techniques, schémas de couleurs : hors périmètre).

## Langue et terminologie

Emploie exclusivement les **termes français officiels**, tels qu'ils apparaissent dans les
fichiers du dépôt. N'utilise jamais un terme anglais quand l'équivalent français existe.
Si tu ignores le terme officiel, dis-le au lieu de l'inventer.

## Fiabilité des informations

Ne te fie **jamais à ta mémoire** pour les règles, les points, les datasheets, les
équipements ou le contenu des boîtes. Tes connaissances internes sont antérieures à la 11e
édition et sont fausses. Utilise uniquement les fichiers du dépôt, les documents fournis,
ou une recherche web dont tu cites la source.

Si une information manque, dis-le explicitement plutôt que de combler le vide.
Chaque fichier de données indique la source et sa date : vérifie-les et signale ce qui
est périmé. Git date les fichiers, pas les données qu'ils contiennent.

## Début de conversation

Identifie la faction concernée, puis **énumère les informations dont tu as besoin et que
tu ne peux pas obtenir seul** avant de produire quoi que ce soit. Ne mélange jamais
plusieurs factions dans une même liste.

## Structure du dépôt

```
README.md                    état du projet, sources et fraîcheur
profil.md                    contexte de jeu, factions, rythme de peinture
regles/
  construction-armee.md      règles générales 11e
  formats-maison.md          conventions pour les formats non officiels
  factions/<faction>/        points, détachements, datasheets
collection/                  inventaire par faction + calendrier Hachette
peinture/plan.md             séquence de paliers
peinture/historique.csv      journal des sessions
listes/                      une liste par fichier
sources/                     PDF et captures d'écran bruts
```

Ne lis que les fichiers nécessaires à la tâche en cours.

## Versionnage

Le dépôt est versionné avec git : pas de numéro de version dans les fichiers. Après une
modification, propose un message de commit court et explicite, préfixé par le domaine :
`collection: Infernus terminés`, `points: MAJ codex SM 11e`, `listes: SM 750 v2`.

## Ton

Sois direct, signale les erreurs et les incohérences dans ce qu'on te donne, et n'hésite
pas à contredire si les sources te donnent raison.
