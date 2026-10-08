---
description: Vérifier que les données des factions actives sont présentes et à jour
---

Vérifie les sources des factions actives, sans rien écrire dans le dépôt.

1. Génère le JavaScript des sources communautaires dans ton répertoire temporaire :
   `python3 -I outils/veille.py --js > <temp>/veille.js`.
   Il ne couvre que les factions sans Pack de Faction français.
2. Si ce fichier contient des factions, ouvre un nouvel onglet Chrome sur
   `https://www.40k.app/`, exécute son contenu tel quel avec l'outil JavaScript, ferme
   l'onglet et enregistre le JSON renvoyé dans `<temp>/veille-navigateur.json`.
   Si Chrome est indisponible, passe à l'étape 3 sans `--navigateur` : le rapport
   signalera 40k.app comme non vérifié.
3. Lance `python3 -I outils/veille.py --navigateur <temp>/veille-navigateur.json`.
4. Rends compte selon le code de retour :
   - **0** : tout est à jour. Affiche le tableau, rien de plus.
   - **1** : pour chaque source modifiée ou absente du dépôt, indique les fichiers qui en
     dépendent (champ `derives` de `sources/etat.json`, listes de `listes/` qui citent
     cette source). Explique le changement : résumé de la PR BSData listée en
     information pour le Munitorum, annonce sur Warhammer Community FR (via Chrome)
     pour une source officielle. Propose `/maj-regles <faction>`.
   - **2** : erreur d'accès. Réessaie une fois, puis applique la règle d'accès de
     `sources/procedures.md` avant de conclure.

Ne lance jamais `--enregistrer` : il est réservé à `/maj-regles`, après intégration.
