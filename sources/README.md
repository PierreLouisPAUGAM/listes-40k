# Sources brutes

- Documents bruts (PDF officiels, captures de l'appli, extraits de codex) et leur extrait
  texte. Les PDF et pages HTML sont exclus de git ; leur extrait `.txt` est versionné.
- `etat.json` : état de chaque source à sa dernière intégration (écrit par
  `outils/veille.py --enregistrer`).
- `factions.json` : correspondance entre les factions actives de `profil.md` et leurs
  identifiants dans chaque source.
- `procedures.md` : carte des sources, accès, nommage.

Ces fichiers ne sont pas lus systématiquement : ils servent quand une donnée doit être
vérifiée ou réextraite.
