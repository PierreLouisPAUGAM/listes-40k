---
description: Vérifier que les données des factions actives sont présentes et à jour
---

Vérifie les sources des factions actives, sans rien écrire dans le dépôt. La commande
s'exécute sur le Mac qui porte l'appli Warhammer 40,000 (`outils/appli/README.md`).

1. Préviens l'utilisateur que l'appli va être pilotée pendant environ trois minutes (la
   souris peut bouger), puis lance `python3 -I outils/veille.py --appli`.
2. Rends compte selon le code de retour :
   - **0** : tout est à jour. Affiche le tableau, rien de plus.
   - **1** : si l'appli n'a pas pu être vérifiée, dis-le en premier et transmets tel quel
     le message « STOP » : il nomme l'action que seul l'utilisateur peut faire
     (déverrouiller le Mac, se reconnecter…). Pour chaque source modifiée ou absente du
     dépôt, indique les fichiers qui en dépendent (champ `derives` de
     `sources/etat.json`, listes de `listes/` qui citent cette source). Explique le
     changement : résumé de la PR BSData listée en information pour le Munitorum,
     annonce sur Warhammer Community FR (via Chrome) pour une source officielle.
     Propose `/maj-regles <faction>`.
   - **2** : erreur d'accès. Réessaie une fois, puis applique la règle d'accès de
     `sources/procedures.md` avant de conclure.

40k.app n'est plus vérifié : il ne sert qu'en secours de l'appli, dans `/maj-regles`.

Ne lance jamais `--enregistrer` : il est réservé à `/maj-regles`, après intégration.
