---
description: Intégrer une nouvelle source de règles ou de points
argument-hint: <faction> <nature du document>
---

Intègre cette source : $ARGUMENTS

Procédure :

1. Lis le document fourni (dans `sources/` ou joint à la conversation).
2. Extrais uniquement ce qui concerne les unités possédées, listées dans `collection/`.
3. Écris ou mets à jour les fichiers de `regles/factions/<faction>/`, en indiquant en
   tête la source et sa date.
4. Mets à jour le tableau de fraîcheur des sources dans `README.md`.
5. Signale ce qui a changé par rapport aux données précédentes, et quelles listes
   existantes de `listes/` sont à revérifier.
6. Propose un message de commit.
