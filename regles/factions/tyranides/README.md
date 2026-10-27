# Tyranides — règles et points

**Alimenté le 26/10/2026** à partir de l'Inventaire du Munitorum v1.6, de l'appli
Warhammer 40,000 (données v995, codex en anglais) et du Pack de Faction Tyranides v1.3
(14/10/2026). Sources et dates détaillées en
tête de chaque fichier ; état des sources dans `sources/etat.json`.

- `tyranids-points.tsv` — coûts des unités (Munitorum), avec noms français et anglais.
- `tyranids-detachements.tsv` — détachements, PdD, dispositions de force, optimisations
  et leurs coûts (Munitorum).
- `tyranids-attachements.tsv` — meneurs et unités de gardes du corps (Munitorum).
- `tyranids-options.tsv` — surcoûts d'équipement (Munitorum).
- `detachements.md` — règle d'armée et les 10 détachements : règles, optimisations,
  stratagèmes.
- `datasheets.md` — uniquement les unités possédées (voir `collection/tyranides.md`) :
  profils, armes, aptitudes, options d'équipement.

Les quatre fichiers TSV sont produits par `python3 -I outils/veille.py --extraire
tyranides` : ne pas les modifier à la main.
