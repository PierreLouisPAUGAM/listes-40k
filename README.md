# Listes 40k

Dépôt de travail pour la construction de listes Warhammer 40,000 (11e édition) et la
planification de la peinture.

## État au 08/10/2026

- **Factions actives** : Space Marines / Dark Angels, Tyranides.
- **Factions à venir** : 7 factions livrées par abonnement Hachette entre fin 2026 et
  mars 2028 (voir `collection/calendrier-hachette.md`).
- **Figurines possédées** : 147 (100 Space Marines / Dark Angels, 47 Tyranides).
- **Peint** : 0 unité terminée.
- **Vitesse de peinture** : inconnue, à calculer dès que `peinture/historique.csv`
  contiendra quelques semaines de données.

## Fraîcheur des sources

<!-- fraicheur:debut -->
Généré par `python3 -I outils/veille.py --readme` depuis `sources/etat.json`. Pour savoir si une source a changé depuis son intégration : `/veille`.

| Source | Type | Version | Alimente | Intégrée le |
|---|---|---|---|---|
| Mises à jour des règles universelles (fr) | officielle | MAJ 26/08/2026 | `construction-armee.md` | 08/10/2026 |
| Munitorum Dark Angels (fr) | officielle | v1.5 | `dark-angels-points.tsv`, `dark-angels-detachements.tsv`, `dark-angels-attachements.tsv`, `dark-angels-options.tsv` | 08/10/2026 |
| Munitorum Space Marines (fr) | officielle | v1.5 | `space-marines-points.tsv`, `space-marines-detachements.tsv`, `space-marines-attachements.tsv`, `space-marines-options.tsv` | 08/10/2026 |
| Munitorum Tyranides (fr) | officielle | v1.5 | `tyranids-points.tsv`, `tyranids-detachements.tsv`, `tyranids-attachements.tsv`, `tyranids-options.tsv` | 08/10/2026 |
| Pack de Faction Dark Angels (en) | officielle | MAJ 30/09/2026 | `datasheets.md`, `detachements.md` | 08/10/2026 |
| Pack de Faction Space Marines (en) | officielle | absent | `datasheets.md`, `detachements.md` | 08/10/2026 |
| Pack de Faction Tyranides (fr) | officielle | MAJ 26/08/2026 | `datasheets.md`, `detachements.md` | 08/10/2026 |
| Rassembler les Armées (fr) | officielle | sans version | `rassembler-les-armees.txt`, `construction-armee.md` | 08/10/2026 |
| Règles de Base (fr) | officielle | MAJ 01/06/2026 | `construction-armee.md` | 08/10/2026 |
| Appli Warhammer 40,000, section 25 (captures) | fournie | captures du 21/09/2026 | `construction-armee.md` | 21/09/2026 |
| 40k.app Dark Angels (en) | communautaire | sans version | `datasheets.md`, `detachements.md` | 08/10/2026 |
| 40k.app Space Marines (en) | communautaire | sans version | `datasheets.md`, `detachements.md` | 08/10/2026 |
| 40k.app Tyranides (en) | communautaire | sans version | `datasheets.md`, `detachements.md` | 08/10/2026 |
<!-- fraicheur:fin -->

## À récupérer

- Codex Space Marines 11e (sorti le 03/10/2026) : texte français des règles d'armée,
  détachements et datasheets (en anglais communautaire pour l'instant). À fournir.
- Mise à jour numérique Dark Angels, qui remplace l'ancien supplément : texte français
  des 3 détachements et des fiches Dark Angels. À fournir (captures de l'appli).
- Codex Tyranides ou captures de l'appli : texte français des fiches et des 6 détachements
  absents du Pack (en anglais communautaire pour l'instant).
- Capture de l'appli, section 25.03 : trancher le détachement à 3 PdD en Incursion.

## Points en suspens

- Escouade Suppressor : absente de l'Inventaire du Munitorum v1.5 SM et DA et de
  40k.app au 08/10/2026. Reste hors plan.

## Procédures de recherche

Carte des sources, accès et nommage : `sources/procedures.md`. Vérification et
intégration : `/veille`, puis `/maj-regles <faction>`.
