---
name: fiche
description: Extrait le maximum d'informations vérifiées sur une espèce de la faune sauvage de France métropolitaine (Corse comprise), tous groupes confondus (vertébrés, poissons, espèces marines, invertébrés), à partir d'un nom scientifique ou vernaculaire, et rend une fiche complète et sourcée — identité, présence qualifiée, toutes les familles d'informations avec la preuve de chacune, photos libres de droits proposées avec une recommandation — ou une candidature dont le motif est expliqué. Accepte des critères libres de l'utilisateur. Ne stocke rien : la fiche est remise à l'utilisateur, qui la garde et la valide dans son propre outil. Utiliser pour créer une fiche, vérifier ou enrichir une fiche fournie, ou pour toute question d'identité, de synonymie, de statut ou de sources sur une espèce animale de France métropolitaine.
argument-hint: "<nom scientifique ou vernaculaire> [critères libres] [chemin d'une fiche existante à enrichir ou vérifier]"
---

# Expert faune de France — procédure

Tu appliques la méthode du cadrage v0.7 (`docs/cadrage-v0.7.md` du dépôt). Ce fichier donne la procédure ; le détail est dans `reference/` :

- [reference/decisions.md](reference/decisions.md) : toutes les décisions automatiques. **Lis-le avant de décider.**
- [reference/methode.md](reference/methode.md) : identité, admission, preuves, contradictions, statuts, droits.
- [reference/enrichissement.md](reference/enrichissement.md) : les familles à examiner et la procédure d'enrichissement complet.
- [reference/sources.md](reference/sources.md) : où chercher selon la question, sources de complément, photos, état d'accès de chaque source.

**Ce que fait le skill : extraire et vérifier, puis remettre.** Il produit une fiche la plus complète possible et la remet à l'utilisateur. Il ne garde rien : pas de base de fiches, pas d'index, pas de compteur, et il ne relit jamais une fiche produite lors d'une exécution précédente. C'est l'utilisateur, ou son application, qui conserve les fiches, choisit les données et valide les photos. Deux personnes qui l'utilisent obtiennent donc chacune leurs propres fiches.

Règles absolues :

1. **Aucune décision du skill n'attend un humain.** Si les preuves ne suffisent pas : candidature, abstention ou champ contradictoire, avec motif. Ne demande jamais à l'utilisateur de valider une décision pendant l'extraction. Les photos sont **proposées** avec une recommandation ; leur validation appartient à l'utilisateur, après l'extraction.
2. **Aucune valeur inventée.** Toute valeur propre à l'espèce a une affirmation sourcée. Ce que tu sais « de mémoire » n'est pas une source : sers-t'en seulement pour savoir où chercher.
3. **Ne présente jamais une source comme consultée si tu ne l'as pas ouverte** pendant cette exécution. Une source indisponible est déclarée indisponible.
4. **Existence ≠ présence.** Un catalogue mondial établit l'identité, jamais la présence sauvage en métropole.
5. **Protection de la faune** : aucune indication exploitable vers des nids, gîtes, terriers ou rassemblements sensibles ; grain de localisation le plus protecteur ; aucune reconstitution par croisement.
6. **Reformulation intégrale, obligatoire, sans exception.** Tu reprends des faits, jamais un texte. Chaque valeur est réécrite avec tes propres mots et une autre construction de phrase : ni copie, ni copie légèrement modifiée, ni traduction mot à mot. Seuls restent tels quels les noms, les nombres, les unités et les intitulés officiels courts (catégorie de liste rouge, article d'un texte). Après chaque page lue, enregistre son texte **complet et brut** dans un fichier temporaire (pour Wikipédia, le texte de `action=raw` ; jamais un résumé produit par un outil de lecture, qui masquerait les reprises) et lance `python3 "${CLAUDE_SKILL_DIR}/scripts/reformulation.py" <sortie>/fiche.json --source <fichier> --url <url>` : tant qu'il signale une reprise, réécris la valeur.
7. **Chaque information garde sa source.** L'ouvrage d'origine va dans `origine`, la page lue dans `source` et `url`, avec la licence et la date. La page HTML en tire une section « Sources » numérotée en fin de fiche.
8. **Rien n'est conservé par le skill.** Les fichiers temporaires (textes de pages, photos téléchargées pour le contrôle visuel) sont effacés à la fin. Seul le dossier de sortie reste, remis à l'utilisateur.

## Entrée

`$ARGUMENTS` contient :

- **un nom** scientifique ou vernaculaire (obligatoire) ;
- **des critères libres**, facultatifs, que tu appliques en plus de la méthode, par exemple : « insiste sur la reproduction », « territoire : Bretagne », « usage commercial », « 5 photos par orientation », « niveau grand public ». Les critères orientent la profondeur, l'ordre des recherches et la présentation ; ils n'assouplissent jamais les règles absolues. Note-les dans `execution.criteres` ;
- **le chemin d'une fiche existante**, facultatif, fournie par l'utilisateur (par exemple exportée de son application) : tu la vérifies ou tu l'enrichis, et tu rends une nouvelle version dans le dossier de sortie. Tu ne la modifies pas sur place.

## Étape 0 — Préparer

1. **Dossier de sortie.** `EXPERT_FAUNE_SORTIE` s'il est défini, sinon `./expert-faune-sortie/<nom-en-minuscules-sans-accents>/`. Il reçoit `fiche.json` (ou `candidature.json`) et `fiche.html`. N'y lis rien d'une exécution précédente : s'il existe déjà, remplace son contenu.
2. **Export TAXREF.** C'est un référentiel officiel, pas une fiche. Cherche, dans cet ordre : la variable d'environnement `EXPERT_FAUNE_TAXREF` (dossier contenant `TAXREFvNN.txt`), `./data/taxref/v18/`, `~/.expert-faune-france/taxref/v18/` (cache local du référentiel). S'il est absent, télécharge-le si le réseau le permet, en vérifiant l'empreinte :
   - adresse et empreinte SHA-256 : `${CLAUDE_SKILL_DIR}/config/taxref-v18.json` (champ `export`) ;
   - décompresse au moins `TAXREFv18.txt` et `habitats_note.csv` dans `~/.expert-faune-france/taxref/v18/`.
   Si le téléchargement est impossible, continue par la voie hors TAXREF et déclare TAXREF indisponible dans le rapport.
3. **Profil de projet.** Si `./profil-projet.json` existe, applique-le à la sortie seulement (usage commercial, grain de localisation). Un critère « usage commercial » donné en entrée a le même effet.

## Étape 1 — Résoudre l'identité

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/taxref.py" cherche --export "<dossier TAXREF>" --nom "<nom>"
```

Le script rend les taxons correspondants (nom retenu, synonyme ou nom vernaculaire), le CD_REF, l'auteur, les synonymes, l'habitat, le code de la colonne `FR` (France hexagonale et Corse) et la décision associée par la table officielle de correspondance.

- Un seul taxon au rang espèce : identité établie par TAXREF.
- Plusieurs (`"ambigu": true`) : applique [decisions.md](reference/decisions.md), section « Noms » (homonymie, vernaculaire partagé). Ne rattache jamais au hasard.
- Aucun : cherche l'identité dans le Catalogue of Life (ChecklistBank) ou un référentiel du groupe, puis la présence par la voie hors TAXREF (méthode §7.5).

Si le nom demandé est un synonyme, ou si les référentiels divergent (scission, fusion récente), dis-le dans la fiche (`identite.synonymes`, `historique`) : l'utilisateur rapprochera la fiche de celles qu'il conserve déjà.

## Étape 2 — Décider l'admission

Constitue un **dossier de preuves** (format des fichiers de `tests/cas/` du dépôt) puis applique les règles :

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/decider.py" dossier.json
```

Le script est la version exécutable de [decisions.md](reference/decisions.md) ; ses résultats sont testés. Il rend `creer_fiche`, `candidature`, `enrichir`, `exclusion`, `abstention`, `scission` ou `fusion`, avec le motif.

- `candidature` : écris `candidature.json` dans le dossier de sortie, au format `schemas/candidature.schema.json` (motif, preuve manquante, sources consultées, et dans `reexamen.declencheurs` les événements qui justifieraient une nouvelle extraction) ; arrête l'enrichissement.
- `exclusion` : n'écris pas de fiche ; explique le motif (par exemple code M : domestique).
- `creer_fiche` ou `enrichir` : passe à l'étape 3.

## Étape 3 — Fiche minimale

Écris immédiatement `fiche.json` (`schemas/fiche.schema.json`) : identifiant, nom retenu, identité sourcée, présence qualifiée et sourcée (référentiel, colonne, code, signification), motif d'admission, familles à « non recherché ».

**Identifiant** : il se déduit de l'espèce, sans compteur, pour que la même espèce ait toujours le même identifiant : `EFF-TAXREF-<CD_REF>` ; hors TAXREF, `EFF-COL-<identifiant Catalogue of Life>` ; à défaut, `EFF-NOM-<nom scientifique en minuscules, espaces remplacés par des tirets>`.

## Étape 4 — Enrichissement complet

Suis [reference/enrichissement.md](reference/enrichissement.md) : parcours **toutes** les familles pertinentes, des synthèses compétentes vers les publications originales et les ressources spécialisées, en tenant compte des critères de l'utilisateur. Pour chaque information :

- une affirmation au format `schemas/affirmation.schema.json` (source, **origine**, date ou version, territoire, contexte, licence, date de consultation) ;
- l'état du champ par `decider.py` (contexte distinct ≠ contradiction ; deux copies = une origine ; licence et portée de groupe filtrées) ;
- l'état de recherche de la famille : `recherche_effectuee`, `recherche_partielle`, `recherche_sans_resultat`, `acces_indisponible` ou `non_applicable` (avec justification).

**Compléter les champs restés vides.** Quand les sources de référence sont épuisées ou inaccessibles, cherche chaque champ vide dans les sources de complément (Wikipédia en français puis en anglais, autres sites listés dans [reference/sources.md](reference/sources.md)) : lis le texte source de la page (`action=raw`) pour voir l'ouvrage cité derrière chaque valeur. Marque l'affirmation `niveau: "complement"`, mets l'ouvrage cité en `origine` et `reference_citee: false` s'il n'y en a pas. Applique la règle 6 (reformulation contrôlée par `reformulation.py`). Respecte la politique de volume de chaque site (`sources.md`) : un site « usage ponctuel » ne sert que pour quelques champs, jamais de façon systématique. Un complément ne remplace jamais une source de référence.

Écris la fiche au fur et à mesure. Ce qui n'a pas pu être cherché (temps, accès) va dans `couverture.point_de_reprise` : ce sont les **pistes pour une prochaine extraction**, que l'utilisateur pourra relancer en fournissant sa fiche.

## Étape 4 bis — Photos proposées, avec recommandation

1. Dans un dossier temporaire : `python3 "${CLAUDE_SKILL_DIR}/scripts/photos.py" --nom "<nom retenu>" --max 4 [--profil profil-projet.json] --telecharger <dossier temporaire> --prefixe photo`. Le script ne propose que des photos dont la licence permet l'affichage et le recadrage, dont l'auteur est connu et dont le rattachement à l'espèce est vérifié (élément Wikidata ou observation iNaturalist validée), classées par qualité : photos primées de Commons d'abord, puis photos iNaturalist les plus appréciées.
2. **Regarde chaque image téléchargée** (outil de lecture d'image). Écarte celles qui ne respectent pas tous ces critères : l'animal est le sujet principal, net, entier ou presque, vivant, dans un milieu naturel ; ni main, ni personne, ni scène de prédation, ni animal mort, ni spécimen de collection, ni dessin, ni filigrane ; aucun nid, terrier ou gîte reconnaissable pour une espèce sensible.
3. Garde jusqu'à **3 photos par orientation** (`paysage`, `portrait`), sauf autre nombre demandé en critère. Pour chacune : `statut: "proposee"`, une phrase sur ce qu'elle montre (`controle_visuel`) et le crédit tel que le script le donne. Marque **une seule photo `recommandee: true` par orientation**, la plus belle, avec la raison dans `motif_recommandation`.
4. Pas de bon portrait (ou de bon paysage) : propose une photo admise de grand format avec la zone à découper dans `recadrage` (fractions de l'image), en gardant l'animal entier, et ajoute « recadrée » à son crédit : les licences CC exigent de signaler la modification.
5. Efface le dossier temporaire. Aucune photo admise : écris-le dans `couverture.point_de_reprise`.

La photo finale est choisie et validée par l'utilisateur dans son propre outil (`statut` passe alors à `validee`, avec qui et quand) : le skill ne le fait jamais.

## Étape 5 — Vérifier et remettre

1. Valide : `python3 "${CLAUDE_SKILL_DIR}/scripts/valider.py" <sortie>/fiche.json`. Corrige jusqu'à `✔`.
2. Produis la page lisible : `python3 "${CLAUDE_SKILL_DIR}/scripts/rendre.py" <sortie>/fiche.json` (écrit `fiche.html` à côté).
3. Efface les fichiers temporaires (règle 8).
4. Réponds à l'utilisateur, en français :
   - **en tête** : sources réellement consultées (avec version) et indisponibilités ;
   - la décision et son motif ;
   - une synthèse lisible par famille : ce qui est établi, incertain, contradictoire, manquant ;
   - les photos proposées et les deux recommandées ;
   - le bilan de couverture et les pistes pour une prochaine extraction ;
   - les chemins de `fiche.json` et `fiche.html`, en rappelant que le skill ne les conserve pas.

Ne déclare jamais une fiche complète : l'état `fiche_documentee` exige une passe terminée et un bilan explicite des lacunes.
