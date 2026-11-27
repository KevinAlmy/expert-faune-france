# Sources

Cadrage v0.6, section 8. Un skill n'a pas d'accès réseau propre : il consulte ce que l'environnement qui l'exécute autorise. Chaque exécution déclare les sources réellement consultées et les indisponibilités.

## Où chercher selon la question

| Question | Source prioritaire | Remarque |
|---|---|---|
| Nom de l'espèce | TAXREF (export local), puis Catalogue of Life (ChecklistBank) ou référentiel du groupe | Un identifiant officiel n'a pas besoin d'être confirmé ailleurs |
| Présence sauvage en métropole | Colonne `FR` de TAXREF, atlas, publication originale, occurrence remontée à son origine | Un catalogue mondial ne suffit pas |
| Protection juridique | Texte officiel en vigueur (Légifrance, EUR-Lex) | Jamais déduite de la menace |
| Risque de disparition | Évaluation Liste rouge datée et territorialisée | Territoire, population, date |
| Biologie, comportement, milieux | Publication scientifique, atlas, synthèse spécialisée aux références vérifiées | Stade, population, saison, unités |
| Restriction de diffusion d'une localisation | Règle du producteur et règle territoriale | Une règle régionale ne vaut pas partout |

## Sources de complément

Quand les sources de référence ne renseignent pas un champ (accès refusé, lacune), le skill consulte ensuite des sources de complément, **pour ce champ seulement** :

| Source | Accès | Licence | Usage |
|---|---|---|---|
| Wikipédia (français, puis anglais et langues de l'aire) | `https://fr.wikipedia.org/w/index.php?title=<Titre>&action=raw` (texte source avec ses références) | CC BY-SA 4.0 | Faits reformulés, jamais de texte recopié ; l'origine est l'ouvrage cité par la page, la source est la page avec sa date de consultation |
| AmphibiaWeb, sites de sociétés savantes, fiches pédagogiques d'organismes publics | Sites des éditeurs | Selon le site | Idem ; une page protégée par une vérification anti-robots n'est pas contournée |

Règles : chaque affirmation porte `niveau: "complement"` et `reference_citee` (vrai si la page cite un ouvrage pour cette valeur). Un complément ne remplace jamais une source de référence, ne rend jamais un champ `corrobore`, et une valeur sans référence citée reste `incertain` (voir `decisions.md`). Les compléments sont affichés comme tels dans la fiche et la page HTML.

## Fiches d'accès (V1)

État constaté lors de la construction du skill (27/11/2026). À revérifier à chaque usage.

| Source | Accès | Licence | État constaté |
|---|---|---|---|
| TAXREF v18, export officiel | `https://assets.patrinat.fr/files/referentiel/TAXREF_v18_2025.zip` (empreinte dans `config/taxref-v18.json`) | Licence Ouverte 2.0 (Etalab) | Téléchargé et vérifié |
| TAXREF, service web (`taxref.mnhn.fr/api`) | API documentée | Licence Ouverte 2.0 | Refuse les accès automatisés (protection anti-robots) : ne pas contourner ; utiliser l'export |
| Catalogue of Life via ChecklistBank | `https://api.checklistbank.org/` (jeu `3LR`) | CC BY 4.0 | Accessible ; version 2026-11-11 constatée |
| GBIF (occurrences, noms) | `https://api.gbif.org/v1/` | Par enregistrement : CC0, CC BY, CC BY-NC | Accessible ; licence à lire sur chaque enregistrement |
| GBIF, copie de TAXREF (jeu `0e61f8fe-7d25-4f81-ada7-d970bbb2c6d6`) | API GBIF | CC BY 4.0 | Ancienne (03/2025), **sans statut de présence** : identité seulement |
| INPN, OpenObs, BDC Statuts | Sites et exports PatriNat | Selon la ressource | Hors ligne fin novembre 2026 (incident de sécurité signalé par le mainteneur) ; BDC disponible en export sur la page PatriNat (licence à vérifier avant usage) |
| Listes rouges (UICN France, régionales, mondiale) | Sites des évaluateurs | À vérifier par ressource | Non vérifié : conditions de réutilisation à contrôler avant reprise |
| iNaturalist | Directement ou via GBIF | Observations et médias sous licences distinctes | Non vérifié directement ; via GBIF, dédupliquer par identifiant d'origine |
| Atlas de la biodiversité communale (ABC) | Rapports et jeux des producteurs | Selon le producteur | Piste documentaire : une fiche de projet ne prouve rien sur une espèce |
| Littérature (HAL, revues) | API HAL, sites des revues | Selon l'éditeur | Lire le contenu avant toute affirmation |

## Origine des preuves

Plusieurs portails diffusent les mêmes jeux (INPN, BDC, UICN, GBIF, OpenObs, iNaturalist). Enregistrer le producteur et le jeu d'origine, et les identifiants d'origine des observations, pour ne compter chaque preuve qu'une fois. Le Catalogue of Life et ChecklistBank sont deux accès au même contenu : consigner le jeu et sa version.

Une indisponibilité déclenche la recherche d'une autre voie autorisée ; elle n'efface rien de ce qui était déjà étayé.
