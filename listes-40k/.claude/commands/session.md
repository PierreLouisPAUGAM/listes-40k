---
description: Enregistrer une session de peinture et recalculer la vitesse
argument-hint: <durée> <unité> <de X% à Y%>
---

Enregistre cette session de peinture : $ARGUMENTS

Procédure :

1. Ajoute une ligne à `peinture/historique.csv` au format décrit dans `peinture/README.md`.
   Demande les informations manquantes plutôt que de les deviner.
2. Mets à jour le fichier de collection concerné : statut, avancement, socles, vernis.
3. Recalcule le temps moyen par figurine, séparément par type, à partir de l'ensemble du
   CSV. Précise la taille de l'échantillon et rappelle que l'estimation est provisoire
   tant qu'il est faible.
4. Indique où en est le palier en cours dans `peinture/plan.md`.
5. Propose un message de commit.
