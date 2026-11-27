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

Quand les sources de référence ne renseignent pas un champ (accès refusé, lacune), le skill consulte ensuite des sources de complément, **pour ce champ seulement**. Chaque affirmation porte `niveau: "complement"` et `reference_citee` (vrai si la page cite un ouvrage pour cette valeur, qui devient l'`origine`). Un complément ne remplace jamais une source de référence, ne rend jamais un champ `corrobore`, et une valeur sans ouvrage cité reste `incertain` (voir `decisions.md`).

### Reformulation (obligatoire)

Les faits ne sont pas protégés par le droit d'auteur, le texte l'est. Toute valeur est donc **réécrite intégralement** (règle 6 de `SKILL.md`) et contrôlée par `scripts/reformulation.py` : aucune suite de 6 mots identiques à la page lue n'est acceptée.

### Volume : ce que chaque site permet

Reformuler protège contre le droit d'auteur, **pas** contre le droit des bases de données : en Europe, extraire une partie substantielle d'une base, ou en extraire de petites parties de façon répétée et systématique, est interdit sans autorisation (Code de la propriété intellectuelle, art. L342-1 et L342-2). D'où deux politiques :

- **usage systématique** : licence ouverte qui autorise la réutilisation, base comprise ; utilisable pour tout le catalogue en respectant les conditions (citation ; partage à l'identique pour CC BY-SA ; pas d'usage commercial pour NC) ;
- **usage ponctuel** : droits réservés ou conditions inconnues ; quelques champs d'une fiche quand rien d'autre n'existe, jamais en série, jamais par robot sur l'ensemble du site ; référence et lien toujours conservés.

| Source | Groupes | Langue | Licence constatée ou annoncée | Politique |
|---|---|---|---|---|
| Wikipédia (fr, puis en, de, es, it) : texte source `index.php?title=<Titre>&action=raw` | Tous | Multiples | CC BY-SA 4.0 | Systématique ; base dérivée en partage à l'identique si une part substantielle en vient ; requêtes lentes (limite de débit) |
| Wikidata (masse, longévité, taille… quand renseignées) | Tous | Données | CC0 | Systématique |
| Plazi (traitements taxonomiques) | Tous | en | CC0 | Systématique |
| Biodiversity Heritage Library (ouvrages anciens) | Tous | Multiples | Domaine public pour l'essentiel, à vérifier par ouvrage | Systématique pour le domaine public |
| Jeux de traits ouverts : AVONET (oiseaux), AmphiBIO (amphibiens), EltonTraits (régime, oiseaux et mammifères), PanTHERIA (mammifères) | Selon le jeu | Données | Ouvertes selon leur dépôt, à vérifier par jeu | Systématique si ouverte ; ce sont des sources de **référence** (publications scientifiques) |
| FishBase, SeaLifeBase | Poissons, faune marine | en | CC BY-NC | Systématique seulement sans usage commercial (profil-projet) |
| xeno-canto (sons) | Oiseaux, orthoptères, amphibiens, chauves-souris | Multiples | Licence par enregistrement (souvent CC BY-NC-SA) | Description des sons seulement ; selon la licence de chaque enregistrement |
| AmphibiaWeb | Amphibiens | en | À vérifier | Ponctuel ; vérification anti-robots non contournée |
| Animal Diversity Web (Université du Michigan) | Tous | en | Droits réservés | Ponctuel |
| The Reptile Database | Reptiles | en | Droits réservés | Ponctuel |
| Société herpétologique de France (lashf.org), SFEPM (mammifères), OPIE (insectes), LPO (oiseaux) | Selon la société | fr | Droits réservés, sauf mention contraire | Ponctuel |
| DORIS (FFESSM, faune subaquatique) | Faune marine et d'eau douce | fr | Droits réservés | Ponctuel |
| Oiseaux.net, Quel est cet animal ?, Lepinet, Galerie-insecte | Selon le site | fr | Droits réservés | Ponctuel |
| Encyclopedia of Life | Tous | en | Licence par élément | Selon chaque élément |

Exclus : contenus payants ou derrière un compte (Birds of the World…), réseaux sociaux, sites qui interdisent la collecte automatisée. Les licences ci-dessus sont à revérifier au premier usage de chaque site ; une licence incompatible avec le profil du projet écarte le contenu (référence conservée).

## Photos

But : deux belles photos par espèce, une en paysage et une en portrait (`scripts/photos.py`, étape 4 bis de `SKILL.md`).

| Source | Pourquoi | Licence | Identification de l'espèce |
|---|---|---|---|
| Wikimedia Commons : *Featured pictures*, *Valued images*, *Quality images* de la catégorie de l'espèce | Photos primées ou validées par des jurys (qualité technique, valeur d'illustration) | Par fichier : CC0, domaine public, CC BY, CC BY-SA le plus souvent | Catégorie Commons reliée à l'élément Wikidata vérifié par le nom scientifique |
| Wikidata, image principale (P18) | Image choisie pour représenter l'espèce | Celle du fichier Commons | Élément Wikidata vérifié par le nom scientifique |
| iNaturalist, observations « qualité recherche » classées par favoris | Grand choix, photos récentes, souvent en milieu naturel | Par photo ; seules CC0, CC BY, CC BY-SA (et NC sans usage commercial) sont demandées | Espèce validée par plusieurs observateurs |

Le contrôle visuel est obligatoire : les photos les plus appréciées ne sont pas toujours des portraits de l'animal (animal tenu en main, proie, cadrage lointain).

**Banques d'images (Unsplash, Pexels, Pixabay)** : non utilisées en V1.
- Les photos y sont souvent très belles et utilisables commercialement sans crédit obligatoire. Elles sont sous les licences propres à chaque site, pas sous Creative Commons. Ces licences interdisent notamment de constituer une collection qui concurrencerait le service.
- Mais l'espèce n'y est pas identifiée : les mots-clés disent « grenouille » ou « lézard », sans validation. Le risque d'une mauvaise espèce sur la fiche est élevé.
- Leur API demande une clé personnelle, et Unsplash impose d'afficher les images depuis ses serveurs.
- Elles pourront être ajoutées en dernier recours, avec le contrôle visuel et une mention « identification non vérifiée ».



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
