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
├─ Fournir un document (extrait de codex, capture de l'appli)
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
├─ Recevoir un colis Hachette
│     dis : « j'ai reçu le colis n° X »
│        → collection et calendrier mis à jour (collection/calendrier-hachette.md)
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
- **Chrome doit être ouvert** pour `/veille` et `/maj-regles` : 40k.app n'est lisible
  que par le navigateur. Sans lui, `/veille` signale que la vérification est incomplète.
- **Les règles de SM, DA et du codex Tyranides sont en anglais** (40k.app,
  communautaire) tant qu'aucun extrait officiel français n'est fourni. Les noms
  d'unités, de détachements et d'optimisations sont toujours les noms français
  officiels.
- **Ne jamais modifier à la main** les fichiers `*.tsv` de `regles/factions/` ni
  `sources/etat.json` : ils sont produits par `outils/veille.py`. Seules les entrées
  `doc:` des documents fournis s'ajoutent à la main, par `/maj-regles`.
