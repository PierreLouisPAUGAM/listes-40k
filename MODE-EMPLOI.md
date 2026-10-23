# Mode d'emploi

Une session = une intention. Trouve la tienne, tape ce qui est indiqué. Les commandes
proposent leurs modifications et leurs messages de commit ; rien n'est commité sans ton
accord.

Identifiants de faction : `space-marines`, `dark-angels`, `tyranides`
(`sources/factions.json`).

```
Que veux-tu faire ?
│
├─ Savoir si les données sont à jour
│     /veille
│        ├─ « tout est à jour » (code 0) ........ rien à faire
│        └─ sources modifiées ou absentes ........ /maj-regles <faction>
│
├─ Intégrer une mise à jour (codex, équilibrage, nouveau Munitorum)
│     /veille
│     /maj-regles <faction>          (space-marines traite aussi les Dark Angels)
│        → points, détachements, fiches et état des sources mis à jour
│        → propose les corrections de collection/ et peinture/plan.md : à valider
│
├─ Fournir un document (extrait de codex)
│     dépose-le dans sources/ ou joins-le à la conversation
│     /maj-regles <faction> <document>
│        → remplace le texte communautaire [C] par le texte officiel [O]
│
├─ Construire la liste d'un palier du plan de peinture
│     /veille                        (les données doivent être à jour)
│     /liste <faction> <points>      (un palier de peinture/plan.md)
│        → conversation : analyse, axes, discussion, brouillon chiffré
│        → listes/palier-<NN>-<faction>-<points>.md, écrit après ton accord
│
├─ Enregistrer une session de peinture
│     /session <durée> <unité> <de X % à Y %>
│        → historique, collection, vitesse par type de figurine, palier en cours
│
├─ Recevoir des figurines (achat ou colis Hachette)
│     dis : « j'ai acheté … » ou « j'ai reçu le colis n° X »
│        → collection mise à jour (et calendrier pour un colis Hachette)
│     /maj-regles <faction>          (fiches des nouvelles unités)
│
├─ Activer une nouvelle faction
│     dis : « active la faction X »
│        → profil.md (statut Active) et sources/factions.json complétés
│     /veille
│     /maj-regles <faction>
│
└─ Faire le point
      /etat
         → palier en cours, figurines par statut, prochaine unité à peindre
```

## Bon à savoir

- **Une conversation par tâche lourde.** Une intégration (`/maj-regles`) remplit vite
  le contexte : lance-la dans un chat neuf.
- **`/veille` et `/maj-regles` lisent l'appli Warhammer 40,000 du Mac** : à lancer sur
  ce Mac, déverrouillé, appli connectée, sans s'en servir pendant ce temps (la souris
  bouge sur certaines pages). Si quelque chose bloque, la commande s'arrête sur un
  message « STOP » qui dit quoi faire. Chrome ne sert plus qu'au secours 40k.app et aux
  annonces de Warhammer Community.
- **Les règles du codex Tyranides sont en anglais dans l'appli** (texte officiel). Les
  noms d'unités, de détachements et d'optimisations sont toujours les noms français
  officiels.
- **Ne jamais modifier à la main** les fichiers `*.tsv` de `regles/factions/` ni
  `sources/etat.json` : ils sont produits par `outils/veille.py`. Seules les entrées
  `doc:` des documents fournis s'ajoutent à la main, par `/maj-regles`.
