# Listes 40k

Dépôt de travail pour la construction de listes Warhammer 40,000 (11e édition) et la
planification de la peinture.

Pour savoir quoi lancer selon ce que tu veux faire : `MODE-EMPLOI.md`.

## État au 08/10/2026

- **Factions actives** : Space Marines / Dark Angels, Tyranides.
- **Factions à venir** : 7 factions livrées par abonnement Hachette entre fin 2026 et
  mars 2028 (voir `collection/calendrier-hachette.md`).
- **Figurines possédées** : 149 (102 Space Marines / Dark Angels, 47 Tyranides).
- **Peint** : 0 unité terminée.
- **Vitesse de peinture** : inconnue, à calculer dès que `peinture/historique.csv`
  contiendra quelques semaines de données.

## Fraîcheur des sources

<!-- fraicheur:debut -->
Généré par `python3 -I outils/veille.py --readme` depuis `sources/etat.json`. Pour savoir si une source a changé depuis son intégration : `/veille`.

| Source | Type | Version | Alimente | Intégrée le |
|---|---|---|---|---|
| Appli Warhammer 40,000, Dark Angels (fr) | officielle | données v995 | `datasheets.md`, `detachements.md` | 23/10/2026 |
| Appli Warhammer 40,000, Règles de Base (fr) | officielle | données v995, MAJ 14/10/2026 | `construction-armee.md` | 23/10/2026 |
| Appli Warhammer 40,000, Space Marines (fr) | officielle | données v995, MAJ 14/10/2026 | `datasheets.md`, `detachements.md` | 23/10/2026 |
| Mises à jour des règles universelles (fr) | officielle | MAJ 26/08/2026 | `construction-armee.md` | 08/10/2026 |
| Munitorum Dark Angels (fr) | officielle | v1.6 | `dark-angels-points.tsv`, `dark-angels-detachements.tsv`, `dark-angels-attachements.tsv`, `dark-angels-options.tsv` | 23/10/2026 |
| Munitorum Space Marines (fr) | officielle | v1.6 | `space-marines-points.tsv`, `space-marines-detachements.tsv`, `space-marines-attachements.tsv`, `space-marines-options.tsv` | 23/10/2026 |
| Munitorum Tyranides (fr) | officielle | v1.5 | `tyranids-points.tsv`, `tyranids-detachements.tsv`, `tyranids-attachements.tsv`, `tyranids-options.tsv` | 08/10/2026 |
| Pack de Faction Dark Angels (en) | officielle | Legends seulement, MAJ 30/09/2026 | `datasheets.md`, `detachements.md` | 09/10/2026 |
| Pack de Faction Space Marines (en) | officielle | aucun pack (codex ou appli) | `datasheets.md`, `detachements.md` | 09/10/2026 |
| Pack de Faction Tyranides (fr) | officielle | MAJ 26/08/2026 | `datasheets.md`, `detachements.md` | 09/10/2026 |
| Rassembler les Armées (fr) | officielle | sans version | `rassembler-les-armees.txt`, `construction-armee.md` | 08/10/2026 |
| Règles de Base (fr) | officielle | MAJ 01/06/2026 | `construction-armee.md` | 08/10/2026 |
| 40k.app Tyranides (en) | communautaire | sans version | `datasheets.md`, `detachements.md` | 09/10/2026 |
<!-- fraicheur:fin -->

## À récupérer

- Codex Tyranides ou captures de l'appli : texte français des fiches et des 6 détachements
  absents du Pack (en anglais communautaire pour l'instant).
- Tyranides : mots-clés de faction des 10 unités possédées, absents de 40k.app et du
  Pack (fiches du codex ou de l'appli).
- Dark Angels : texte français de l'aptitude d'équipement « Watcher in the Dark »
  (Chevaliers et Escouade Terminator de la Deathwing), en anglais dans l'appli au
  23/10/2026. Seul le codex papier peut le donner (extrait à fournir si besoin).

## Points en suspens

- Escouade Suppressor : absente de l'Inventaire du Munitorum v1.6 SM et DA et des fiches
  de l'appli au 23/10/2026. La page « Substituts Légendaires » de l'appli indique
  « Escouade Suppressor : Escouade Inceptor », sans expliquer l'usage de ces substituts.
  Reste hors plan.
- SM/DA, appli : pas de paragraphe « Restrictions » pour la Colère de Medusa, la Serre des
  Ombres et la Lame d'Ultramar (contrairement aux autres détachements de Chapitre) ;
  optimisation Maîtrise Défensive (Sentinelles de Céramite) au même texte que
  Cyberfamilier, probablement erroné ; mouvement de débarquement d'assaut sans clause
  « après le mouvement ». Détail : `regles/factions/space-marines/detachements.md`.
- SM/DA : « Règles d'Armée des Chapitres Space Marines (p. 156) », citées par l'Appui de
  la Deathwatch, absentes de la page Règles d'Armée de l'appli.
- Étiquette « Unique : … » des détachements (DOCTRINES, GRAVIS, IRONSTORM, PHOBOS,
  TACTICUS, TERMINATOR) : affichée par l'appli, expliquée nulle part dans les sources lues.
- Incursion et détachement à 3 PdD : la section 25.04 de l'appli porte une note « ** »
  orpheline qui l'autorise s'il est le seul détachement ; le panneau du Munitorum ne la
  contient pas et l'emporte (`regles/construction-armee.md`).
- Mouvements de débarquement d'assaut (18.06) et de choc (18.07) : cités par les Mises à
  jour des règles universelles, absents des Règles de Base du 01/06/2026 ; définis pour
  les Space Marines dans leurs Règles d'Armée (Types de Mouvement Spécial).
- Lion El'Jonson : l'aptitude Primarque de la Première Légion parle de « deux
  aptitudes », la rubrique de l'appli en liste trois.
- Tyranides, Situation Insurmontable (Essaim Inépuisable) : l'erratum français du Pack
  v1.2 vise les unités « d'ESSAIM INÉPUISABLE », 40k.app les ENDLESS MULTITUDE
  (MULTITUDE INFINIE). Erreur probable de traduction, à trancher par l'appli ou le codex.

## Procédures de recherche

Carte des sources, accès et nommage : `sources/procedures.md`. Vérification et
intégration : `/veille`, puis `/maj-regles <faction>`.
