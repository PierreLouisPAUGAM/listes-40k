# Space Marines / Dark Angels — règles d'armée et détachements

> **Source** : Inventaire du Munitorum, Space Marines — officielle
> **URL** : https://mfm.warhammer-community.com/fr/space-marines
> **Version** : v1.5
> **Consultée le** : 08/10/2026
> **Brut** : regles/factions/space-marines/space-marines-detachements.tsv (PdD, dispositions, noms et coûts des optimisations)

> **Source** : Inventaire du Munitorum, Dark Angels — officielle
> **URL** : https://mfm.warhammer-community.com/fr/dark-angels
> **Version** : v1.5
> **Consultée le** : 08/10/2026
> **Brut** : regles/factions/space-marines/dark-angels-detachements.tsv

> **Source** : 40k.app, Space Marines et Dark Angels (en) — communautaire, à recouper avec le codex Space Marines ou l'appli
> **URL** : https://www.40k.app/factions/space-marines/army-rules, https://www.40k.app/factions/dark-angels/army-rules, https://www.40k.app/factions/space-marines/detachments/<détachement>, https://www.40k.app/factions/dark-angels/detachments/<détachement>, et les pages complémentaires https://www.40k.app/factions/<chapitre>/detachments/<détachement> pour imperial-fists, iron-hands, raven-guard, salamanders, ultramarines, white-scars
> **Version** : sans version
> **Consultée le** : 08/10/2026
> **Brut** : aucun (pages lues dans Chrome)

Aucun Pack de Faction ne couvre ces deux factions : le Pack Space Marines n'existe pas et
le Pack Dark Angels du 30/09/2026 ne contient plus que les unités Legends. Le texte des
règles vient donc entièrement de 40k.app, en anglais, avec le renvoi **[C]**. Le texte
français n'existe que dans le codex Space Marines et l'appli ; il remplacera ces passages
quand il sera fourni (renvoi **[O]**).

Noms des détachements et des optimisations : Inventaire du Munitorum. Les noms des règles
de détachement, des stratagèmes et des aptitudes ne figurent dans aucune source française
accessible : ils restent en anglais entre guillemets, terme français non trouvé au
08/10/2026. Les mots-clés sont laissés en anglais, en capitales, comme sur 40k.app.

Colonne « Phase » : catégorie affichée par 40k.app ; le type de stratagème (Battle Tactic,
Strategic Ploy…) n'y figure pas. PC : chiffre affiché par le site après chaque
stratagème. Les effets sont recopiés en anglais, condensés quand 40k.app les découpe en
listes.

Les 16 détachements communs ont les mêmes PdD, dispositions, optimisations et coûts dans
les deux Inventaires (comparaison des fichiers TSV le 08/10/2026), et le même texte sur
les pages 40k.app Space Marines et Dark Angels (le texte n'a été relu que sur la page
Space Marines).

Les Mises à jour des règles universelles (`regles/construction-armee.md`) s'appliquent
en plus.

## Règle d'armée [C]

Pages `space-marines/army-rules` et `dark-angels/army-rules`. Les deux factions partagent
les quatre premières règles ; les Dark Angels ajoutent la Ravenwing et la Deathwing.

### "Combat Doctrines"

At the start of your Command phase, you can select one combat doctrine listed below. If
you do, that combat doctrine is active for friendly ADEPTUS ASTARTES units with this
ability until the start of your next Command phase.

- **"Assault Doctrine"** : when this unit is selected to make an advance move, that
  advance move does not prevent this unit from being eligible to declare a charge.
- **"Devastator Doctrine"** : this unit's ranged attacks have [ASSAULT].
- **"Tactical Doctrine"** : when this unit is selected to make a fall-back move, that
  fall-back move does not prevent this unit from being eligible to shoot and eligible to
  declare a charge.

Unless otherwise stated, you can only select each combat doctrine once per battle, and
only one combat doctrine can be active for each unit. If a rule makes a combat doctrine
active for a unit, any combat doctrine previously active for that unit is no longer
active for that unit.

### "Transhuman Strategist"

At the start of the battle round, if a model with this ability is your WARLORD, gain 1CP.

### "Librarius"

ADEPTUS ASTARTES PSYKER units with this ability have a psyker level of 1 or higher,
specified in that unit's abilities. Each psychic ability has a psychic level of 1 or
higher, specified in that ability's name. In a battle round, a friendly ADEPTUS ASTARTES
PSYKER unit can use a number of psychic abilities whose total psychic level does not
exceed that unit's psyker level. Example: a psyker level 3 unit could use three psychic
level 1 abilities, or one level 1 and one level 2, or one level 3.

### "Special Move Types"

- **"Shock Disembark Move"**. When eligible: as stated in the rule allowing this move
  type, if your unit is embarked within a TRANSPORT model that is on the battlefield and
  did not embark within that TRANSPORT this phase. Effect: your unit is set up as
  described in Set Up (Core Rules, 03.02). While moving: set up each model wholly within
  the set-up distance of that TRANSPORT. After moving: your unit is not eligible to
  declare a charge until the end of the turn.
- **"Assault Disembark Move"**. When eligible: as stated in the rule allowing this move
  type, if your unit is embarked within a TRANSPORT model that is on the battlefield, did
  not embark within that TRANSPORT this phase, and that TRANSPORT has not made an
  advance/fall-back move this phase. Set-up distance: 3". Effect: your unit is set up as
  described in Set Up (Core Rules, 03.02). While moving: set up each model wholly within
  the set-up distance of that TRANSPORT.

La page s'arrête là pour l'« Assault Disembark Move » : aucune clause « After moving »,
contrairement au « Shock Disembark Move ». Lacune de 40k.app ou absence réelle : à
vérifier dans le codex.

### "The Ravenwing" — Dark Angels uniquement

The following friendly ADEPTUS ASTARTES units have RAVENWING: MOUNTED units; VEHICLE FLY
units.

### "The Deathwing" — Dark Angels uniquement

The following friendly ADEPTUS ASTARTES units have DEATHWING: TERMINATOR units;
Doyen Gardelame, Escouade de Vétérans Gardelames, Escouade de Vétérans d'Appui and
Escouade de Vétérans d'Avant-garde à Réacteurs Dorsaux units; Land Raider, Land Raider
Crusader, Land Raider Redeemer, Repulsor and Repulsor Executioner units; DREADNOUGHT
units.

La page Dark Angels répète ensuite « Combat Doctrines » et « Transhuman Strategist » à
l'identique.

## Récapitulatif

| Détachement | PdD | Dispositions de force | Accessible à |
|---|---|---|---|
| Appui de la Deathwatch | 1 | Perturbation | SM et DA |
| Champions Cuirassés | 1 | Atouts Prioritaires | SM et DA |
| Confrérie Devastator | 1 | Éliminez l'Adversaire | SM et DA |
| Confrérie d'Assaut | 1 | Prendre et Tenir | SM et DA |
| Confrérie Tactique | 1 | Atouts Prioritaires | SM et DA |
| Fer de Lance Déluge d'Acier | 1 | Éliminez l'Adversaire | SM et DA |
| Force Briseuse de Ligne Gravis | 1 | Prendre et Tenir | SM et DA |
| Force de Choc Phobos | 1 | Perturbation | SM et DA |
| Force de Siège Gravis | 1 | Prendre et Tenir | SM et DA |
| Force d'Assaut Terminator | 1 | Atouts Prioritaires | SM et DA |
| Force d'Attaque Tacticus | 1 | Prendre et Tenir | SM et DA |
| Force Furtive Phobos | 1 | Perturbation | SM et DA |
| Force Opérationnelle Ceste | 1 | Reconnaissance | SM et DA |
| Force Opérationnelle Lance de l'Orage | 1 | Reconnaissance | SM et DA |
| Force Tacticus Tempête de Feu | 1 | Atouts Prioritaires | SM et DA |
| Force Opérationnelle du Cercle Intérieur | 1 | Atouts Prioritaires | DA uniquement |
| Poursuite de Sombrevol | 1 | Reconnaissance | DA uniquement |
| Colère du Roc | 2 | Prendre et Tenir | DA uniquement |
| Chercheurs du Père de la Forge | 2 | Atouts Prioritaires | SM, Salamanders |
| Colère de Medusa | 2 | Éliminez l'Adversaire | SM, Iron Hands |
| Force Opérationnelle de Pointe de Lance | 2 | Reconnaissance | SM, White Scars |
| Sentinelles de Céramite | 2 | Prendre et Tenir | SM, Imperial Fists |
| Serre des Ombres | 2 | Perturbation | SM, Raven Guard |
| Force Opérationnelle Gladius | 3 | Prendre et Tenir, Atouts Prioritaires | SM et DA |
| Lame d'Ultramar | 3 | Prendre et Tenir, Atouts Prioritaires | SM, Ultramarines |

« SM, <Chapitre> » : détachement listé par 40k.app sur la page du Chapitre et non sur la
page Space Marines ; l'Inventaire du Munitorum Space Marines le liste sans mention de
Chapitre. La restriction écrite figure sur les pages 40k.app de Sentinelles de Céramite,
Chercheurs du Père de la Forge et Force Opérationnelle de Pointe de Lance (et des trois
détachements Dark Angels), pas sur celles de Colère de Medusa, Serre des Ombres et Lame
d'Ultramar.

Les détachements à 3 PdD sont inaccessibles en Incursion d'après le panneau « Rassembler
les Armées » (voir la contradiction signalée dans `regles/construction-armee.md`).

Le Munitorum anglais écrit « Nightforged Battery (Upgarde) » : coquille de la source.

---

## Confrérie d'Assaut [C]

1 PdD · Prendre et Tenir · page 40k.app : `space-marines/detachments/assault-brethren`

### Règle : "Assault Mastery"

You can select the assault doctrine one additional time per battle.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Assaut Furieux (Amélioration) | 10 pts | ADEPTUS ASTARTES INFANTRY unit only. This unit's melee attacks have [SUSTAINED HITS 1: non-MONSTER/VEHICLE]. |
| Glaive de l'Imperium | 20 pts | ADEPTUS ASTARTES model only. This model has the following weapon: Imperium's Sword, mêlée, A 6, CC 2+, F 7, PA -3, D 3. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Gene-wrought Might" | Fight | 1 | Fight phase, when a friendly ADEPTUS ASTARTES unit is selected to fight | That unit | Melee attacks have [LANCE]; or, if the assault doctrine is active for your unit, [LANCE] and +1 AP. |
| "Armour of Contempt" | Shooting & Fight | 1 | Opponent's Shooting phase or the Fight phase, when an enemy unit targets a friendly ADEPTUS ASTARTES unit | That unit | Attacks that target your unit have -1 AP until that enemy unit has attacked. |
| "Duty in Death" | Fight | 1 | Fight phase, when an enemy unit targets a friendly ADEPTUS ASTARTES unit | That unit | When a model in your unit is destroyed, if your unit has not been selected to fight this phase, roll one D6 (+1 if the assault doctrine is active for your unit): on a 4+, do not remove it; it is removed when your unit has fought or at the end of the phase, whichever comes first. |

## Appui de la Deathwatch [C]

1 PdD · Perturbation · page 40k.app : `space-marines/detachments/deathwatch-support`

### Règle : "Mission Tactics"

Friendly KILL TEAM units with this ability have the following abilities:

- **Furor Tactics** : if the devastator doctrine is active for your unit, your unit's attacks have [SUSTAINED HITS 1].
- **Malleus Tactics** : if the tactical doctrine is active for your unit, your unit's attacks have [LETHAL HITS].
- **Purgatus Tactics** : if the assault doctrine is active for your unit, your unit's attacks that target an enemy unit within 9" of this unit have [PRECISION].

**"Deathwatch Allies"** : you can include DEATHWATCH units in your army, even though they do not have the same Chapter faction keyword as other units in your army. The combined points value of such units cannot exceed 500 points. When mustering your army, unless otherwise stated, you cannot select a DEATHWATCH model to be your WARLORD. In addition, KILL TEAM units can only contain enhancements taken from this detachment. This is an exception to the Space Marine Chapters Army Rules (pg156).

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Balise Angelis | 25 pts | ADEPTUS ASTARTES model only. If this unit is a KILL TEAM unit, it has Deep Strike, and when you target it with the Rapid Ingress Stratagem, that use is -1CP. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Blackstar Extraction" | Fight | 1 | End of your opponent's Fight phase | One friendly unengaged KILL TEAM unit | Place your unit in strategic reserves. |
| "Kraken Rounds" | Shooting | 1 | Your Shooting phase, when a KILL TEAM unit is selected to shoot | That unit | Ranged attacks have +6" range and +1 S. |
| "Dragonfire Rounds" | Shooting | 1 | Your Shooting phase, when a KILL TEAM unit is selected to shoot | That unit | Ranged attacks can re-roll Wound rolls of 1 and have [IGNORES COVER]. |
| "Hellfire Rounds" | Shooting | 1 | Your Shooting phase, when a KILL TEAM unit is selected to shoot | That unit | Ranged attacks (excluding [DEVASTATING WOUNDS] attacks) have [ANTI-non-VEHICLE 4+]. |

## Confrérie Devastator [C]

1 PdD · Éliminez l'Adversaire · page 40k.app : `space-marines/detachments/devastator-brethren`

### Règle : "Devastator Mastery"

You can select the devastator doctrine one additional time per battle.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Honneur Vigilant | 20 pts | ADEPTUS ASTARTES model only. This unit's ranged attacks have [LETHAL HITS]. If the devastator doctrine is active for this unit, it can re-roll advance rolls. |
| Armes à Feu de Facture Magistrale | 15 pts | ADEPTUS ASTARTES INFANTRY/MOUNTED model only. This model's ranged attacks (excluding [PSYCHIC] attacks) have +1 A, S, AP and D. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Armour of Contempt" | Shooting & Fight | 1 | Opponent's Shooting phase or the Fight phase, when an enemy unit targets a friendly ADEPTUS ASTARTES unit | That unit | Attacks that target your unit have -1 AP until that enemy unit has attacked. |
| "Storm of Fire" | Shooting | 1 | Your Shooting phase, when a friendly ADEPTUS ASTARTES unit is selected to shoot | That unit | Ranged attacks have [IGNORES COVER]; or, if the devastator doctrine is active for your unit, [IGNORES COVER] and +1 AP. |
| "Hail of Vengeance" | Shooting | 2 | Opponent's Shooting phase, when an enemy unit has shot, if those attacks destroyed a model in a friendly ADEPTUS ASTARTES unit | That unit | Your unit shoots using normal shooting, but can only target that enemy unit. |

## Force Opérationnelle Ceste [C]

1 PdD · Reconnaissance · page 40k.app : `space-marines/detachments/gauntlet-task-force`

### Règle : "Combined Deployment"

In your Shooting phase, when a friendly ADEPTUS ASTARTES TRANSPORT unit has shot, you can select one enemy unit hit by those attacks. That enemy unit is assailed until the end of the turn. While a unit is assailed, when an ADEPTUS ASTARTES unit that disembarked this turn targets that unit, those attacks have [SUSTAINED HITS 1].

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Liaison de Classe Damoclès | 15 pts | CAPTAIN model only. In your Movement phase, if this unit is embarked within a TRANSPORT unit, you can select one friendly ADEPTUS ASTARTES INFANTRY unit within 6" of that TRANSPORT and one combat doctrine: that doctrine is active for that INFANTRY unit. |
| Offensive Briseuse de Ligne | 20 pts | ADEPTUS ASTARTES INFANTRY model only. If this unit disembarked this turn, it can re-roll charge rolls, and enemy units cannot target it with snap shooting attacks. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Storm and Secure" | Movement | 1 | End of your Movement phase | One friendly ADEPTUS ASTARTES TRANSPORT unit that has an ADEPTUS ASTARTES BATTLELINE unit embarked within it | Select one objective your unit is controlling: that objective is secured. |
| "Aggressive Disembarkation" | Any | 1 | Any phase, when a friendly ADEPTUS ASTARTES unit embarked within a TRANSPORT is selected to move | That unit | While making that move, each model can be set up within the set-up distance of that TRANSPORT, instead of wholly within it. |
| "Duty is Never Done" | Fight | 1 | End of the Fight phase | One friendly unengaged ADEPTUS ASTARTES INFANTRY unit that was eligible to fight this phase, is wholly within 6" of a friendly TRANSPORT unit and is eligible to embark within it | Your unit embarks within that TRANSPORT unit. |

## Force Opérationnelle Gladius [C]

3 PdD · Prendre et Tenir, Atouts Prioritaires · page 40k.app : `space-marines/detachments/gladius-task-force`

### Règle : "Codex Discipline"

You can select one combat doctrine one additional time per battle.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Adepte du Codex | 20 pts | CAPTAIN model only. The tactical doctrine is active for this unit in addition to any other combat doctrine. |
| Armure d'Artificier | 15 pts | ADEPTUS ASTARTES model only. This model has 2+ Sv and Feel No Pain 5+. |
| Lauriers du Triomphe | 20 pts | ADEPTUS ASTARTES model only. This model's melee attacks have +1 S and AP; or, if the assault doctrine is active for this unit, +2 S and AP. |
| Étendard de l'Empereur Ascendant | 25 pts | ANCIENT model only. This model has +1 OC and Ld, Feel No Pain 5+, and the ability "Ancient Exhortation" (once per battle, per army): when this unit is selected to fight, its melee attacks have +1 A until the end of the phase. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Armour of Contempt" | Shooting & Fight | 1 | Opponent's Shooting phase or the Fight phase, when an enemy unit targets a friendly ADEPTUS ASTARTES unit | That unit | Attacks that target your unit have -1 AP until that enemy unit has attacked. |
| "Adaptive Strategy" | Command | 1 | Your Command phase | One friendly ADEPTUS ASTARTES unit | Select one combat doctrine: it is active for your unit until the start of your next Command phase. |
| "A Worthy Death" | Fight | 1 | Fight phase, when an enemy unit targets a friendly ADEPTUS ASTARTES unit | That unit | When a model in your unit is destroyed, if your unit has not been selected to fight this phase, roll one D6: on a 4+, do not remove it; it is removed when your unit has fought or at the end of the phase, whichever comes first. |
| "Responsive Tactics" | Movement | 1 | Opponent's Movement phase, when an enemy unit ends a move within 8" of a friendly unengaged ADEPTUS ASTARTES INFANTRY/MOUNTED unit | That unit | Your unit can make a normal move of up to D6". |
| "Storm of Devastation" | Shooting | 1 | Your Shooting phase, when a friendly ADEPTUS ASTARTES unit is selected to shoot | That unit | Ranged attacks have [IGNORES COVER]. |
| "Might of Angels" | Fight | 1 | Fight phase, when a friendly ADEPTUS ASTARTES unit is selected to fight | That unit | Melee attacks have [LANCE]. |

## Force Briseuse de Ligne Gravis [C]

1 PdD · Prendre et Tenir · page 40k.app : `space-marines/detachments/gravis-linebreaker-force`

### Règle : "Walking Fortress"

In a turn a friendly GRAVIS unit made a normal move, that unit's ranged attacks do not have [HEAVY] and have +1 to Hit rolls.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Robustesse Inaltérable | 20 pts | GRAVIS model only. Attacks that target this unit with a S greater than this unit's T have -1 to Wound rolls. |
| Avance Implacable | 20 pts | GRAVIS model only. This unit has Scouts 5". |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Purgation Push" | Shooting | 1 | Your Shooting phase, when a friendly GRAVIS unit has shot | That unit | If unengaged, your unit can make a normal move of up to 5" and must end it within range of an objective. It is then not eligible to declare a charge or embark within a TRANSPORT until the end of the turn. |
| "Armoured Impact" | Charge | 1 | Your Charge phase, when a friendly GRAVIS unit ends a charge move | That unit | Select one enemy unit engaged with your unit; roll one D6 per model of your unit engaged with it: each 3+ inflicts 1 mortal wound. |
| "Annihilating Force" | Shooting & Fight | 1 | Your Shooting phase or the Fight phase, when a friendly GRAVIS unit is selected to attack | That unit | Attacks have [LETHAL HITS]. |

## Force de Siège Gravis [C]

1 PdD · Prendre et Tenir · page 40k.app : `space-marines/detachments/gravis-siege-force`

### Règle : "Indomitable Defence"

While a friendly GRAVIS unit is within range of an objective, attacks that target that unit with a S greater than that unit's T have -1 to Wound rolls.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Conquérants Inamovibles (Amélioration) | 15 pts | GRAVIS unit only. This unit has +1 OC. |
| Gantelet Narthecis | 20 pts | APOTHECARY BIOLOGIS model only. In your Command phase, this unit heals D3+1 wounds. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Annihilating Force" | Shooting & Fight | 1 | Your Shooting phase or the Fight phase, when a friendly GRAVIS unit is selected to attack | That unit | Attacks have [LETHAL HITS]. |
| "Suppression Volleys" | Shooting | 1 | Your Shooting phase, when a friendly GRAVIS unit has shot | That unit | Select one enemy unit hit by those attacks: it makes a battle-shock roll, with -1. |
| "Stand Unyielding" | Movement | 1 | End of your Movement phase | One friendly GRAVIS unit | Select one objective your unit is controlling: that objective is secured. |

## Champions Cuirassés [C]

1 PdD · Atouts Prioritaires · page 40k.app : `space-marines/detachments/ironclad-champions`

### Règle : "Enduring Vengeance"

Friendly ADEPTUS ASTARTES DREADNOUGHT units can re-roll Hit rolls of 1.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Sarcophage d'Artificier (Amélioration) | 40 pts | DREADNOUGHT unit only. Attacks that target this unit have -1 D. |
| Champion Vénérable (Aura) (Amélioration) | 30 pts | DREADNOUGHT unit only. While a friendly ADEPTUS ASTARTES INFANTRY/MOUNTED unit is within 6" of this unit, that unit's attacks can re-roll Hit rolls of 1. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Adamantine Terror" | Fight | 1 | Start of the Fight phase | One friendly DREADNOUGHT unit | Each enemy unit engaged with your unit makes a battle-shock roll, with -1. |
| "Mercy is Weakness" | Shooting & Fight | 1 | Your Shooting phase or the Fight phase, when a friendly DREADNOUGHT unit is selected to attack | That unit | Attacks have [LETHAL HITS], or [SUSTAINED HITS 1]. |
| "Unstoppable Advance" | Movement & Charge | 1 | Your Movement/Charge phase, when a friendly DREADNOUGHT unit is selected to move or declares a charge | That unit | Your unit has Mobile. |

40k.app écrit « Upstoppable Advance » : coquille corrigée en « Unstoppable Advance ».

## Fer de Lance Déluge d'Acier [C]

1 PdD · Éliminez l'Adversaire · page 40k.app : `space-marines/detachments/ironstorm-spearhead`

### Règle : "Ironstorm Auto-targeters"

Ranged attacks of friendly ADEPTUS ASTARTES VEHICLE units (excluding WALKER units) can re-roll one Hit roll and one Wound roll.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Honneurs d'Artilleur (Amélioration) | 15 pts | ADEPTUS ASTARTES VEHICLE unit only (excluding DEDICATED TRANSPORT/FLY/WALKER units). This unit's ranged attacks have [HEAVY]. |
| Esprit de la Machine Redoutable (Amélioration) | 25 pts | ADEPTUS ASTARTES VEHICLE unit only (excluding DEDICATED TRANSPORT/FLY/WALKER units). This unit has 5+ InSv and, at the end of your Command phase, heals 1 wound. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Might of the Machine Spirit" | Command | 1 | Your Command phase | One friendly ADEPTUS ASTARTES VEHICLE unit (excluding DEDICATED TRANSPORT/FLY/WALKER units) | Until the start of your next Command phase, your unit can ignore modifiers to its M, BS, Hit rolls and Wound rolls. |
| "Layered Ceramite" | Any | 1 | Any phase, when a friendly ADEPTUS ASTARTES VEHICLE unit suffers a mortal wound | That unit | Feel No Pain 5+ against mortal wounds. |
| "Headhunter Doctrine" | Shooting | 1 | Your Shooting phase, when a friendly ADEPTUS ASTARTES VEHICLE unit (excluding DEDICATED TRANSPORT/FLY/WALKER units) is selected to shoot | That unit | Ranged attacks have [LETHAL HITS: MONSTER/VEHICLE]. |

## Force Furtive Phobos [C]

1 PdD · Perturbation · page 40k.app : `space-marines/detachments/phobos-shadow-force`

### Règle : "Shadow Masters"

When a friendly PHOBOS or SCOUT SQUAD unit has shot, either those attacks do not prevent that unit from being hidden, or that unit can make a normal move of up to D6" (it is then not eligible to declare a charge until the end of the turn).

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Exécution et Redéploiement | 25 pts | PHOBOS model only. In your Shooting phase, after this unit has shot, if unengaged, it can make a normal move of up to 6"; it is then not eligible to declare a charge until the end of the turn. |
| Omni-auspex Venator | 15 pts | PHOBOS model only. This unit's attacks that target a hidden unit can re-roll Wound rolls of 1; or, if the assault doctrine is active for this unit, Wound rolls of 1 and 2. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Mortis Snares" | Movement | 1 | End of your Movement phase | One friendly unengaged PHOBOS/SCOUT SQUAD unit | If your unit is controlling an objective, that objective is snared. When an enemy unit ends a move within range of a snared objective, roll one D6: on a 2+, it suffers D6 mortal wounds; the objective is then no longer snared. |
| "Tactical Withdrawal" | Fight | 1 | End of your opponent's Fight phase | One friendly unengaged PHOBOS/SCOUT SQUAD unit | Place your unit in strategic reserves. |
| "Strike from the Shadows" | Shooting & Fight | 1 | Your Shooting phase or the Fight phase, when a friendly hidden PHOBOS unit is selected to attack | That unit | Attacks have +1 S and [LETHAL HITS]. |

## Force de Choc Phobos [C]

1 PdD · Perturbation · page 40k.app : `space-marines/detachments/phobos-shock-force`

### Règle : "Vanguard Ambushers"

At the end of your Movement phase, if a friendly PHOBOS unit is hidden, that unit's attacks can re-roll Wound rolls of 1 until the end of the turn.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Sceau de Dissimulation | 15 pts | PHOBOS model only. Enemy units cannot target this unit with snap shooting attacks. |
| Omni-auspex Venator | 15 pts | PHOBOS model only. This unit's attacks that target a hidden unit can re-roll Wound rolls of 1; or, if the assault doctrine is active for this unit, Wound rolls of 1-2. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Umbral Evasion" | Shooting | 1 | Opponent's Shooting phase, when an enemy unit targets a friendly PHOBOS unit | That unit | Ranged attacks that target your unit have -1 to Hit rolls. |
| "Strike from the Shadows" | Shooting & Fight | 1 | Your Shooting phase or the Fight phase, when a friendly hidden PHOBOS unit is selected to attack | That unit | Attacks have +1 S and [LETHAL HITS]. |
| "Transhuman Reactions" | Movement | 1 | Opponent's Movement phase, when an enemy unit ends a move within 8" of a friendly unengaged PHOBOS unit | That unit | Your unit can make a normal move of up to D6"; or, if the tactical doctrine is active for your unit, up to 6". |

## Force Opérationnelle Lance de l'Orage [C]

1 PdD · Reconnaissance · page 40k.app : `space-marines/detachments/stormlance-task-force`

### Règle : "Lightning-fast Strike"

Friendly ADEPTUS ASTARTES MOUNTED/SPEEDER units have +2" M.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Autels-auspex de Triangulation (Amélioration) | 10 pts | ADEPTUS ASTARTES SPEEDER unit only. At the start of your Shooting phase, select one visible enemy unit within 12" of this unit: it is spotted. While a unit is spotted, it has +3" detection range. |
| Moteurs Surgonflés (Amélioration) | 10 pts | ADEPTUS ASTARTES MOUNTED unit only. This unit can re-roll advance rolls. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Hurtling Targets" | Shooting | 1 | Opponent's Shooting phase, when an enemy unit targets a friendly ADEPTUS ASTARTES MOUNTED/SPEEDER unit | That unit | Ranged attacks that target your unit have -1 to Hit rolls. |
| "Wind-Swift Evasion" | Fight | 1 | End of the Fight phase | One friendly ADEPTUS ASTARTES MOUNTED unit that was eligible to fight this phase | If unengaged, your unit can make a normal move; if engaged, it can make a fall-back move. |
| "Sudden Onslaught" | Movement | 1 | Your Movement phase, when a friendly ADEPTUS ASTARTES MOUNTED/SPEEDER unit is selected to make an advance move | That unit | Your unit can change its advance rolls to a 6. |

## Confrérie Tactique [C]

1 PdD · Atouts Prioritaires · page 40k.app : `space-marines/detachments/tactical-brethren`

### Règle : "Tactical Mastery"

You can select the tactical doctrine one additional time per battle.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Lauriers de la Vigilance | 10 pts | ADEPTUS ASTARTES model only. (Once per battle round, per army) When you use the Fire Overwatch/Heroic Intervention Stratagem on a friendly ADEPTUS ASTARTES BATTLELINE unit within 12" of this model, that use is -1CP. |
| Sagacité Tactique | 15 pts | CAPTAIN model only. The tactical doctrine is active for this unit in addition to any other combat doctrine. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Armour of Contempt" | Shooting & Fight | 1 | Opponent's Shooting phase or the Fight phase, when an enemy unit targets a friendly ADEPTUS ASTARTES unit | That unit | Attacks that target your unit have -1 AP until that enemy unit has attacked. |
| "Masterful Tactics" | Movement | 1 | Opponent's Movement phase, when an enemy unit ends a move within 8" of a friendly unengaged ADEPTUS ASTARTES INFANTRY/MOUNTED unit | That unit | Your unit can make a normal move of up to D6"; or, if the tactical doctrine is active for your unit, up to 6". |
| "Domination Fire" | Shooting | 1 | Your Shooting phase, when a friendly ADEPTUS ASTARTES unit has shot | That unit | Select one enemy unit hit by those attacks: it is suppressed until the start of your next turn (its attacks have -1 to Hit rolls). |

## Force d'Attaque Tacticus [C]

1 PdD · Prendre et Tenir · page 40k.app : `space-marines/detachments/tacticus-attack-force`

### Règle : "Wrath of the Chapter"

Friendly TACTICUS units can re-roll advance rolls.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Parangon Martial | 10 pts | TACTICUS model only. This unit's attacks can re-roll one Hit roll and one Wound roll. |
| Champion d'Avant-garde | 15 pts | TACTICUS model only. This unit has Scouts 6". |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Transhuman Swiftness" | Fight | 1 | Fight phase, when an enemy unit has fought | One friendly TACTICUS unit within range of an objective and eligible to fight | Your unit has Fights First and must be the next unit you select to fight. |
| "Tactical Focus" | Fight | 1 | Fight phase, when a friendly TACTICUS unit is selected to make a consolidation move | That unit | Your unit can move up to D3+3" when making that consolidation move. |
| "Relentless Assault" | Shooting & Fight | 1 | Your Shooting phase or the Fight phase, when a friendly TACTICUS unit is selected to attack | That unit | Attacks have [SUSTAINED HITS 1: non-MONSTER/VEHICLE], or [LETHAL HITS: MONSTER/VEHICLE]. |

## Force Tacticus Tempête de Feu [C]

1 PdD · Atouts Prioritaires · page 40k.app : `space-marines/detachments/tacticus-firestorm-force`

### Règle : "Codex Fire-patterns"

Friendly TACTICUS units' [RAPID FIRE] attacks benefit from [RAPID FIRE] when targeting units up to that attack's maximum range.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Cyberfamilier | 15 pts | TACTICUS model only. When both players have deployed their armies, you can redeploy up to three friendly ADEPTUS ASTARTES INFANTRY units, including into strategic reserves regardless of how many units are already there. |
| Trempé dans les Combats (Aura) | 10 pts | TACTICUS model only. Friendly ADEPTUS ASTARTES units within 6" of this model can re-roll leadership rolls. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Point-blank Brutality" | Shooting | 1 | Your Shooting phase, when a friendly engaged TACTICUS unit is selected to shoot | That unit | Ranged attacks (excluding [BLAST] attacks) have [CLOSE-QUARTERS] and [IGNORES COVER]. |
| "For the Emperor!" | Command | 1 | Command phase | One friendly TACTICUS unit within range of an objective | Your unit has +1 OC until the end of the turn. |
| "Relentless Assault" | Shooting & Fight | 1 | Your Shooting phase or the Fight phase, when a friendly TACTICUS unit is selected to attack | That unit | Attacks have [SUSTAINED HITS 1: non-MONSTER/VEHICLE], or [LETHAL HITS: MONSTER/VEHICLE]. |

## Force d'Assaut Terminator [C]

1 PdD · Atouts Prioritaires · page 40k.app : `space-marines/detachments/terminator-storm-force`

### Règle : "Death Blow"

Friendly ADEPTUS ASTARTES TERMINATOR units have +1 to charge rolls.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Champion de la Première Compagnie | 20 pts | ADEPTUS ASTARTES TERMINATOR model only. This unit's melee attacks have [LETHAL HITS]. |
| Reliquaire Corporeum | 25 pts | ADEPTUS ASTARTES TERMINATOR model only. In your first Movement phase, this unit can make an ingress move. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Tactical Dreadnought Fortitude" | Shooting & Fight | 2 | Opponent's Shooting phase or the Fight phase, when an enemy unit targets a friendly ADEPTUS ASTARTES TERMINATOR unit | That unit | Attacks that target your unit have -1 D until that enemy unit has attacked. |
| "Gunship Extraction" | Fight | 1 | End of your opponent's Fight phase | One friendly unengaged ADEPTUS ASTARTES TERMINATOR unit | Place your unit in strategic reserves. |
| "Merciless Veterans" | Shooting | 1 | Your Shooting phase, when a friendly ADEPTUS ASTARTES TERMINATOR unit is selected to shoot | That unit | Ranged attacks have [LETHAL HITS] and [SUSTAINED HITS 1]. |

## Poursuite de Sombrevol [C] — Dark Angels uniquement

1 PdD · Reconnaissance · page 40k.app : `dark-angels/detachments/darkflight-pursuit`

### Règle : "Black-winged Vigilance"

Friendly RAVENWING FLY units' ranged attacks have [IGNORES COVER].

Restrictions : your army can include DARK ANGELS units, but it cannot include any ADEPTUS ASTARTES units drawn from any other Chapter.

Friendly OUTRIDER SQUAD units have BATTLELINE.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Batterie Noctiforgée (Amélioration) | 10 pts | LAND SPEEDER VENGEANCE unit only. This unit can re-roll rolls to determine the A of a weapon, and Hazard rolls. |
| Turbines Ténébreuses (Amélioration) | 15 pts | RAVENWING FLY/MOUNTED unit only. In your first Movement phase, this unit can make an ingress move. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Skyborne Surveillance" | Shooting | 1 | Your Shooting phase, when a friendly RAVENWING FLY unit has shot | That unit | Visible enemy units within 6" of your unit have +3" detection range. |
| "We Are Vengeance" | Shooting | 1 | Opponent's Shooting phase, when an enemy unit that targeted a friendly unengaged RAVENWING FLY unit has shot | That unit | Your unit can make a normal move of up to D3+3". |
| "Wings of Shadow" | Shooting | 1 | Opponent's Shooting phase, when an enemy unit targets a friendly RAVENWING FLY/MOUNTED unit | That unit | Your unit has Stealth. |

## Force Opérationnelle du Cercle Intérieur [C] — Dark Angels uniquement

1 PdD · Atouts Prioritaires · page 40k.app : `dark-angels/detachments/inner-circle-task-force`

### Règle : "Vowed Target"

In your Command phase, you can select one objective: it is your vowed objective until your next Command phase. Attacks of friendly DEATHWING INFANTRY units that target an enemy unit within range of your vowed objective have +1 to Wound rolls.

Restrictions : your army can include DARK ANGELS units, but it cannot include any ADEPTUS ASTARTES units drawn from any other Chapter.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Champion de la Deathwing | 20 pts | DEATHWING model only. This unit's attacks that target an enemy unit within range of your vowed objective have [SUSTAINED HITS 1]. |
| Volonté Singulière | 20 pts | DEATHWING model only. When this unit is selected to make a consolidation move, it can move up to D3+3". |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Relic Teleportarium" | Movement | 1 | Your Movement phase, when a friendly DEATHWING unit with Deep Strike is selected to make an ingress move | That unit | Your unit can be set up more than 6" horizontally from all enemy units (instead of more than 8"); it is not eligible to declare a charge until the end of the turn. |
| "Duty Unto Death" | Fight | 1 | Fight phase, when an enemy unit targets a friendly DEATHWING unit | That unit | When a model in your unit is destroyed, if your unit has not been selected to fight this phase, roll one D6 (+1 if your unit is engaged with an enemy unit within range of your vowed objective): on a 4+, do not remove it; it is removed when your unit has fought or at the end of the phase, whichever comes first. |
| "Wrath of the Lion" | Charge | 1 | Your Charge phase, when a friendly DEATHWING unit ends a charge move | That unit | Select one enemy unit engaged with your unit; roll one D6 per model of your unit engaged with it: each 3+ inflicts 1 mortal wound (maximum 6). |

## Colère du Roc [C] — Dark Angels uniquement

2 PdD · Prendre et Tenir · page 40k.app : `dark-angels/detachments/wrath-of-the-rock`

### Règle : "Dutiful Tenacity"

Attacks that target friendly ADEPTUS ASTARTES INFANTRY/MOUNTED units with a S greater than that unit's T have -1 to Wound rolls.

Restrictions : your army can include DARK ANGELS units, but it cannot include any ADEPTUS ASTARTES units drawn from any other Chapter.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Armes Antiques | 20 pts | ADEPTUS ASTARTES model only. This model's melee attacks have +2 S and +1 AP. |
| Assaut Deathwing | 15 pts | DEATHWING model with Deep Strike only. In your first Movement phase, this unit can make an ingress move. |
| Seigneur de la Ravenwing | 15 pts | RAVENWING model only. This unit can re-roll charge rolls. |
| Trempé dans les Combats (Aura) | 10 pts | ADEPTUS ASTARTES model only. Friendly ADEPTUS ASTARTES units within 6" of this model can re-roll leadership rolls. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "In Sacrifice, Victory" | Any | 1 | Any phase, when a friendly DEATHWING/RAVENWING unit within range of an objective is destroyed | That unit, even though it is destroyed | Select one objective that no enemy units (excluding AIRCRAFT) are within range of, or that your unit was controlling at the end of the previous phase: that objective is secured. |
| "Lion's Will" | Command | 1 | Command phase | One friendly ADEPTUS ASTARTES unit within range of an objective | Your unit has +1 OC until the end of the turn. |
| "Inescapable Justice" | Fight | 1 | Fight phase, when a friendly ADEPTUS ASTARTES unit is selected to fight | That unit | Melee attacks have [PRECISION]. |
| "Tactical Mastery" | Command | 1 | Your Command phase | One friendly DEATHWING/RAVENWING unit | Select one combat doctrine: it is active for your unit until the start of your next Command phase. |
| "Knights of Iron" | Movement & Charge | 1 | Your Movement/Charge phase, when a friendly RAVENWING unit is selected to move or declares a charge | That unit | Your unit has Mobile. |
| "Relics of the Dark Age" | Shooting | 1 | Your Shooting phase, when a friendly ADEPTUS ASTARTES INFANTRY/MOUNTED unit is selected to shoot | That unit | Ranged attacks have +2 S. |

40k.app affiche le mot-clé TERMINATOR à côté de ce détachement, sans règle associée sur la page.

## Sentinelles de Céramite [C] — Imperial Fists uniquement

2 PdD · Prendre et Tenir · page 40k.app : `imperial-fists/detachments/ceramite-sentinels`

### Règle : "Adaptive Defence"

- While a friendly ADEPTUS ASTARTES unit is within a terrain area, that unit's attacks can re-roll Wound rolls of 1.
- Friendly ADEPTUS ASTARTES units are entrenched while all of the following apply: the unit is within a terrain area, it was not set up this turn, and no model in it moved more than 3" this turn.
- Friendly DARNATH LYSANDER/TOR GARADON units have the ability "Defensive Mastery": at the start of each phase, this unit is entrenched, regardless of the conditions above.

Restrictions : your army can include IMPERIAL FISTS units, but it cannot include any ADEPTUS ASTARTES units drawn from any other Chapter.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Omnivox Castellum | 10 pts | ADEPTUS ASTARTES unit only. When this unit makes an advance/fall-back move, that move does not prevent it from being eligible to start an action. |
| Maîtrise Défensive | 10 pts | ADEPTUS ASTARTES model only. When both players have deployed their armies, you can redeploy up to three friendly ADEPTUS ASTARTES INFANTRY units, including into strategic reserves regardless of how many units are already there. |
| Honneur Inoxydable | 10 pts | GRAVIS model only. (Once per battle, per army) At the end of a phase in which this model is destroyed, roll one D6: on a 2+, set it back up as close as possible to where it was destroyed, unengaged, with 3 wounds remaining. |
| Liaison par Crâne-espion | 10 pts | ADEPTUS ASTARTES unit only. This unit's ranged weapons have [IGNORES COVER]. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Unyielding Might" | Command | 1 | Command phase | One friendly ADEPTUS ASTARTES unit within range of an objective | Your unit has +1 OC until the end of the turn. |
| "Stand to the End" | Shooting & Fight | 1 | Opponent's Shooting phase or the Fight phase, when an enemy unit targets a friendly ADEPTUS ASTARTES unit (excluding MONSTER/VEHICLE units) | That unit | Attacks with a S greater than your unit's T have -1 to Wound rolls; or, if your unit is entrenched, all attacks that target it have -1 to Wound rolls. |
| "Augmented Targeting" | Shooting & Fight | 1 | Your Shooting phase or the Fight phase, when a friendly ADEPTUS ASTARTES unit is selected to attack | That unit | Attacks have [LETHAL HITS], or [SUSTAINED HITS 1]; if entrenched, both. |
| "Establish Supremacy" | Fight | 1 | Fight phase, when a friendly entrenched ADEPTUS ASTARTES INFANTRY unit is selected to make a consolidation move | That unit | You can select the objective consolidation mode regardless of that move's Before Moving restrictions (designer's note: your unit can thus move out of engagement range, provided it meets the conditions of that mode). |
| "Priority Strike" | Shooting & Fight | 1 | Your Shooting phase or the Fight phase, when a friendly ADEPTUS ASTARTES INFANTRY/MOUNTED unit is selected to attack | That unit | Attacks that target a MONSTER/VEHICLE unit have +1 to Wound rolls. |
| "Evasive Repositioning" | Shooting | 1 | Opponent's Shooting phase, when an enemy unit has shot | One friendly unengaged ADEPTUS ASTARTES INFANTRY/MOUNTED unit that lost a wound as a result of those attacks | Your unit can make a normal move of up to D6" (D3+3" if entrenched); it cannot embark within a TRANSPORT until the end of the turn. |

Le nom français de l'optimisation « Maîtrise Défensive » est aussi le nom anglais de l'aptitude de Lysander et Garadon (« Defensive Mastery ») : deux règles distinctes.

## Colère de Medusa [C] — Iron Hands

2 PdD · Éliminez l'Adversaire · page 40k.app : `iron-hands/detachments/medusas-wrath`

### Règle : "Armoured Wrath"

Each time a friendly ADEPTUS ASTARTES unit is selected to shoot or to fight, when resolving those attacks:

- if that unit is within 6" of a friendly CAANOK VAR/RÉVÉREND DE FER FEIRROS unit, you can re-roll one Hit roll, one Wound roll and one Damage roll;
- otherwise, you can re-roll one Hit roll, or one Wound roll, or one Damage roll.

40k.app ne reproduit pas, sur cette page, de restriction de Chapitre ; elle figure sur les autres détachements de Chapitre. Non trouvé au 08/10/2026 pour celui-ci.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Adepte de l'Omnimessie | 25 pts | TECHMARINE model only. (Once per battle round, per army) When an enemy unit targets a friendly ADEPTUS ASTARTES VEHICLE unit within 6" of this unit, that VEHICLE unit has Feel No Pain 5+ until that enemy unit has attacked. |
| Maître de la Guerre Mécanisée | 25 pts | ADEPTUS ASTARTES model only. In your Movement phase, select one visible friendly ADEPTUS ASTARTES VEHICLE unit within 6" of this model and the devastator or tactical doctrine: that doctrine is active for that VEHICLE unit until the start of your next Command phase. |
| Toile Augure de Ciblage | 30 pts | TECHMARINE model only. In your Movement phase, at the start or end of this unit's move, select one friendly ADEPTUS ASTARTES VEHICLE model within 3": its attacks have [LETHAL HITS] until the start of your next Command phase. |
| La Chair est Faible | 15 pts | ADEPTUS ASTARTES model only. This model has +1 T and Feel No Pain 5+. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Unbowed Conviction" | Command | 1 | Your Command phase | One friendly ADEPTUS ASTARTES unit below Starting Strength | Until the start of your next Command phase, your unit can ignore modifiers to its BS, WS, Hit rolls and Wound rolls. |
| "Spirits of Iron" | Any | 1 | Any phase, when a friendly ADEPTUS ASTARTES unit suffers a mortal wound | That unit | Feel No Pain 5+ against mortal wounds. |
| "Vengeful Animus" | Any | 1 | Any phase, when a friendly ADEPTUS ASTARTES VEHICLE unit is destroyed, before rolling for Deadly Demise | That unit | Change any Deadly Demise rolls for this unit to an unmodified 6. |
| "Methodical Brutality" | Shooting & Fight | 1 | Your Shooting phase or the Fight phase, when a friendly ADEPTUS ASTARTES unit is selected to attack | That unit | Attacks have [SUSTAINED HITS 1]; if your unit is a VEHICLE, they also have +1 to Wound rolls. |
| "Ancient Fury" | Command | 1 | Your Command phase | One friendly ADEPTUS ASTARTES DREADNOUGHT unit | Until the start of your next Command phase: +1" M, +1 T, +1 Ld, +1 OC and +1 to Hit rolls. |
| "Power of the Machine Spirit" | Shooting | 1 | Opponent's Shooting phase, when an enemy unit that targeted a friendly unengaged ADEPTUS ASTARTES VEHICLE unit has shot | That unit | Your unit shoots using snap shooting (normal shooting if at half-strength or below), and can only target that enemy unit. |

40k.app écrit « Cannok Var » ; l'Inventaire du Munitorum écrit CAANOK VAR.

## Serre des Ombres [C] — Raven Guard

2 PdD · Perturbation · page 40k.app : `raven-guard/detachments/shadowmark-talon`

### Règle : "Shadow Tactics"

Friendly ADEPTUS ASTARTES units have Stealth. Friendly PHOBOS/SCOUT SQUAD units have -3" detection range. Friendly AETHON SHAAN units have the ability "Unparalleled Tactician": (once per battle round, per army) when you use the "Into Darkness" Stratagem, that use is -1CP.

Restriction de Chapitre : non reproduite sur la page 40k.app, non trouvée au 08/10/2026.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Suaire de l'Aile Noire | 25 pts | ADEPTUS ASTARTES INFANTRY model only. This unit has Infiltrators. |
| Couronne des Murmures | 30 pts | PHOBOS model only. Each enemy unit (excluding MONSTER/VEHICLE units) engaged with this unit cannot be targeted by its controlling player's Stratagems. |
| Instincts du Chasseur | 25 pts | ADEPTUS ASTARTES model only. In your first Movement phase, this unit can make an ingress move. |
| Rapace de l'Ombre | 15 pts | ADEPTUS ASTARTES INFANTRY model only. This model has Fights First and Lone Operative. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Into Darkness" | Fight | 1 | End of your opponent's Fight phase | One unengaged ADEPTUS ASTARTES INFANTRY unit | Place your unit in strategic reserves. |
| "Raptorial Vigilance" | Movement | 1 | Opponent's Movement phase, when an enemy unit ends a move within 8" of a friendly unengaged ADEPTUS ASTARTES INFANTRY unit | That unit | Your unit can make a normal move of up to D6"; or, if it is a PHOBOS/SCOUT SQUAD unit, up to 6". |
| "Murderous Fusillade" | Shooting | 1 | Your Shooting phase, when a friendly ADEPTUS ASTARTES INFANTRY unit that made an ingress move this turn is selected to shoot | That unit | Ranged attacks have +1 BS and +1 AP. |
| "Suppressed Weapons" | Shooting | 1 | Your Shooting phase, when a friendly ADEPTUS ASTARTES INFANTRY unit has shot | That unit | Those attacks do not prevent your unit from being hidden. |
| "Feint and Thrust" | Command | 1 | Your Command phase | One friendly ADEPTUS ASTARTES INFANTRY unit | The tactical doctrine is active for your unit in addition to any other combat doctrine, until the start of your next Command phase. |
| "Lay Low the Tyrants" | Fight | 1 | Fight phase, when a friendly ADEPTUS ASTARTES INFANTRY unit is selected to fight | That unit | Melee attacks have [PRECISION]. |

## Chercheurs du Père de la Forge [C] — Salamanders uniquement

2 PdD · Atouts Prioritaires · page 40k.app : `salamanders/detachments/forgefathers-seekers`

### Règle : "Vulkan's Quest"

- You can select the devastator doctrine one additional time per battle.
- Friendly ADEPTUS ASTARTES units' ranged attacks that target a unit within 12" have +1 S.
- If your army includes a VULKAN HE'STAN unit, friendly ESCOUADE INFERNUS units have the following: when selected to make an advance/fall-back move, that move does not prevent them from being eligible to start an action; when they start an action, that action does not prevent them from being eligible to shoot.

Restrictions : your army can include SALAMANDERS units, but it cannot include any ADEPTUS ASTARTES units drawn from any other Chapter.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Cape Adamantine | 20 pts | ADEPTUS ASTARTES model only. Attacks allocated to this model have -1 D. |
| Forgés par la Bataille | 25 pts | ADEPTUS ASTARTES model only. This unit can ignore modifiers to BS, WS and Hit rolls. |
| Immolator | 20 pts | ADEPTUS ASTARTES model only. This unit's [TORRENT] weapons have +1 A. |
| Artisan Aguerri | 25 pts | ADEPTUS ASTARTES model only. This model's melee attacks have +1 S and +1 D. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Blazing Earth" | Charge | 1 | Start of your opponent's Charge phase | One friendly unengaged ADEPTUS ASTARTES unit equipped with one or more TORRENT/MELTA weapons | Select one visible enemy unit within 12" of your unit: it has -1 to charge rolls. |
| "Wrath and Ruin" | Command | 1 | Your Command phase | One friendly ADEPTUS ASTARTES INFANTRY unit | The assault or tactical doctrine is active for your unit until the start of your next Command phase. |
| "Forged in Fire" | Shooting | 1 | Your Shooting phase, when a friendly engaged ADEPTUS ASTARTES unit is selected to shoot | That unit | Your unit's TORRENT weapons do not have [BLAST], have [CLOSE-QUARTERS] and +1 A. |
| "Immolation Protocols" | Shooting | 1 | Your Shooting phase, when a friendly ADEPTUS ASTARTES INFANTRY unit is selected to attack | That unit | Ranged [TORRENT] attacks have +1 AP. |
| "Crucible of Battle" | Shooting & Fight | 1 | Your Shooting phase or the Fight phase, when a friendly ADEPTUS ASTARTES INFANTRY unit is selected to attack an enemy unit within 6" | That unit | Attacks can re-roll Hit rolls of 1 and Wound rolls of 1. |
| "Burning Vengeance" | Shooting | 1 | Opponent's Shooting phase, when an enemy unit has shot a friendly ADEPTUS ASTARTES TRANSPORT unit | One friendly ADEPTUS ASTARTES unit embarked within that TRANSPORT | Your unit can make a disembark move and shoot using normal shooting, but can only target that enemy unit. |

## Lame d'Ultramar [C] — Ultramarines

3 PdD · Prendre et Tenir, Atouts Prioritaires · page 40k.app : `ultramarines/detachments/blade-of-ultramar`

### Règle : "Mastered Doctrines"

If your army includes a MARNEUS CALGAR unit, you can select the assault, devastator and tactical doctrines each one additional time per battle.

Restriction de Chapitre : non reproduite sur la page 40k.app, non trouvée au 08/10/2026.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Armure d'Antoninus | 15 pts | ADEPTUS ASTARTES model only. This model has 2+ Sv and Feel No Pain 5+. |
| Serment de Macragge | 20 pts | ADEPTUS ASTARTES model only. This model's melee attacks have +1 S and AP; or, if the assault doctrine is active for this unit, +2 S and AP. |
| Érudit du Codex | 20 pts | CAPTAIN model only. The tactical doctrine is active for this unit in addition to any other combat doctrine. |
| Vétéran de Béhémoth | 20 pts | ADEPTUS ASTARTES model only. This unit's ranged attacks have [SUSTAINED HITS 1]. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Armour of Contempt" | Shooting & Fight | 1 | Opponent's Shooting phase or the Fight phase, when an enemy unit targets a friendly ADEPTUS ASTARTES unit | That unit | Attacks that target your unit have -1 AP until that enemy unit has attacked. |
| "Exemplary Vigilance" | Shooting | 1 | Your Shooting phase, when a friendly ADEPTUS ASTARTES unit is selected to shoot | That unit | Ranged attacks have [IGNORES COVER]. |
| "Ultramarian Adaptivity" | Command | 1 | Your Command phase | One friendly ADEPTUS ASTARTES unit | Select one combat doctrine: it is active for your unit until the start of your next Command phase. |
| "Courage and Honour!" | Fight | 1 | Fight phase, when a friendly ADEPTUS ASTARTES unit is selected to fight | That unit | Melee attacks have [LANCE]. |
| "Practical Tactics" | Movement | 1 | Opponent's Movement phase, when an enemy unit ends a move within 8" of a friendly unengaged ADEPTUS ASTARTES INFANTRY/MOUNTED unit | That unit | Your unit can make a normal move of up to D3+3". |
| "Tactical Foresight" | Shooting & Fight | 1 | Opponent's Shooting phase or the Fight phase, when an enemy unit targets a friendly ADEPTUS ASTARTES unit | That unit | Attacks with a S greater than your unit's T have -1 to Wound rolls. |

## Force Opérationnelle de Pointe de Lance [C] — White Scars uniquement

2 PdD · Reconnaissance · page 40k.app : `white-scars/detachments/spearpoint-task-force`

### Règle : "Storm-swift Onslaught"

- You can select the assault or tactical doctrine one additional time per battle.
- Friendly ADEPTUS ASTARTES MOUNTED/SPEEDER units have +1 to advance rolls.
- Friendly SUBODEN KHAN units have the ability "Wrath of the First Khan": at the end of the Fight phase, if this unit was eligible to fight this phase, it can make a normal move if unengaged, or a fall-back move if engaged.

Restrictions : your army can include WHITE SCARS units, but it cannot include any ADEPTUS ASTARTES units drawn from any other Chapter.

### Optimisations

| Optimisation | Coût | Effet |
|---|---|---|
| Maître de Chasse Chogorien | 20 pts | ADEPTUS ASTARTES MOUNTED/SPEEDER unit only. When this unit is selected to make an ingress move, treat the current battle round number as one higher than it actually is. |
| Œil du Chasseur | 25 pts | ADEPTUS ASTARTES model only. This unit's ranged attacks have [IGNORES COVER] and [SUSTAINED HITS 1]. |
| Parangon de Pointe de Lance | 25 pts | ADEPTUS ASTARTES model only. This model's melee attacks have +1 S and AP; or, if this unit made a charge move this turn, +2 S and AP. |
| Sagesse des Devins d'Orage | 15 pts | ADEPTUS ASTARTES model only. This unit can re-roll advance rolls. |

### Stratagèmes

| Stratagème | Phase | PC | Quand | Cible | Effet |
|---|---|---|---|---|---|
| "Evasive Manoeuvres" | Shooting | 1 | Opponent's Shooting phase, when an enemy unit targets a friendly ADEPTUS ASTARTES MOUNTED/SPEEDER unit | That unit | Ranged attacks that target your unit have -1 to Wound rolls. |
| "Mobile Lethality" | Movement | 1 | Your Movement phase, when a friendly ADEPTUS ASTARTES unit is selected to make an advance/fall-back move | That unit | That fall-back move does not prevent your unit from being eligible to shoot, and its ranged attacks have [ASSAULT]. |
| "Flawless Riders" | Movement & Charge | 1 | Your Movement/Charge phase, when a friendly ADEPTUS ASTARTES MOUNTED unit is selected to move or declares a charge | That unit | Your unit has Mobile. |
| "Spear Thrust and Sabre Swing" | Fight | 1 | Fight phase, when a friendly ADEPTUS ASTARTES unit is selected to fight | That unit | Melee attacks have [LETHAL HITS], or [LANCE]; if your unit is MOUNTED, both. |
| "Withdraw and Regroup" | Fight | 1 | End of your opponent's Fight phase | One friendly unengaged ADEPTUS ASTARTES MOUNTED/SPEEDER unit | Place your unit in strategic reserves. |
| "Hunter's Instincts" | Movement | 1 | Opponent's Movement phase, when an enemy unit ends a move within 8" of a friendly unengaged ADEPTUS ASTARTES INFANTRY/MOUNTED/SPEEDER unit | That unit | Your unit can make a normal move of up to D3+3". |

