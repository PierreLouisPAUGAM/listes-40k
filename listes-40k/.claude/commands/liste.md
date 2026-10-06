---
description: Construire une liste d'armée pour une faction et un format donnés
argument-hint: <faction> <format en points>
---

Construis une liste d'armée pour : $ARGUMENTS

Procédure :

1. Lis `regles/construction-armee.md` et `regles/formats-maison.md` pour les limites du
   format demandé.
2. Lis le fichier de collection de la faction dans `collection/`.
3. Lis les règles et points de la faction dans `regles/factions/<faction>/`.
4. **Si les points ou les datasheets manquent, ou si leur source est antérieure à la
   dernière mise à jour connue, arrête-toi et dis précisément ce qu'il te faut.**
   Ne construis jamais une liste à partir de ta mémoire.
5. Construis la liste en respectant les règles de `listes/CLAUDE.md`.
6. Enregistre-la dans `listes/<faction>-<format>-<AAAA-MM>.md` et propose un message de
   commit.
