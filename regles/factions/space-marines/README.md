# Space Marines / Dark Angels — règles et points

**Alimenté le 23/10/2026** à partir de l'Inventaire du Munitorum v1.6 (Space Marines et
Dark Angels, fichiers TSV) et de l'appli Warhammer 40,000 (`datasheets.md`,
`detachements.md`, texte officiel français). Aucun Pack de Faction n'apporte de règles.
Sources et dates détaillées en tête de chaque fichier ; état des sources dans
`sources/etat.json`.

- `space-marines-points.tsv`, `dark-angels-points.tsv` — coûts des unités (Munitorum),
  avec noms français et anglais.
- `space-marines-detachements.tsv`, `dark-angels-detachements.tsv` — détachements, PdD,
  dispositions de force, optimisations et leurs coûts (Munitorum).
- `space-marines-attachements.tsv`, `dark-angels-attachements.tsv` — meneurs, appuis et
  unités de gardes du corps (Munitorum).
- `space-marines-options.tsv`, `dark-angels-options.tsv` — surcoûts d'équipement
  (Munitorum).
- `detachements.md` — règles d'armée et les 25 détachements (16 communs dont l'Appui de
  la Deathwatch, 6 de Chapitre côté Space Marines, 3 propres aux Dark Angels) : règles,
  optimisations, stratagèmes.
- `datasheets.md` — uniquement les unités possédées (voir `collection/space-marines.md`) :
  profils, armes, aptitudes, options d'équipement.

Les huit fichiers TSV sont produits par `python3 -I outils/veille.py --extraire
space-marines dark-angels` : ne pas les modifier à la main.
