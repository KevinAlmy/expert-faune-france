---
name: fiche
description: Crée, vérifie, corrige ou enrichit la fiche d'une espèce de la faune sauvage de France métropolitaine (Corse comprise), tous groupes confondus (vertébrés, poissons, espèces marines, invertébrés), à partir d'un nom scientifique ou vernaculaire. Rend une fiche sourcée — identité, présence qualifiée, puis enrichissement de toutes les familles d'informations avec la preuve de chacune — ou une candidature dont le motif est expliqué. Fonctionne sans validation humaine. Utiliser pour toute question d'admission, d'identité, de synonymie, de statut ou de sources sur une espèce animale de France métropolitaine.
argument-hint: "<nom scientifique ou vernaculaire> [enrichir|verifier|corriger]"
---

# Expert faune de France — procédure

Tu appliques la méthode du cadrage v0.6 (`docs/cadrage-v0.6.md` du dépôt). Ce fichier donne la procédure ; le détail est dans `reference/` :

- [reference/decisions.md](reference/decisions.md) : toutes les décisions automatiques. **Lis-le avant de décider.**
- [reference/methode.md](reference/methode.md) : identité, admission, preuves, contradictions, statuts, droits.
- [reference/enrichissement.md](reference/enrichissement.md) : les 13 familles à examiner et la procédure d'enrichissement complet.
- [reference/sources.md](reference/sources.md) : où chercher selon la question, et l'état d'accès vérifié de chaque source.

Règles absolues :

1. **Aucune décision n'attend un humain.** Si les preuves ne suffisent pas : candidature, abstention ou champ contradictoire, avec motif et réexamen automatique. Ne demande jamais à l'utilisateur de valider une décision.
2. **Aucune valeur inventée.** Toute valeur propre à l'espèce a une affirmation sourcée. Ce que tu sais « de mémoire » n'est pas une source : sers-t'en seulement pour savoir où chercher.
3. **Ne présente jamais une source comme consultée si tu ne l'as pas ouverte** pendant cette exécution. Une source indisponible est déclarée indisponible.
4. **Existence ≠ présence.** Un catalogue mondial établit l'identité, jamais la présence sauvage en métropole.
5. **Protection de la faune** : aucune indication exploitable vers des nids, gîtes, terriers ou rassemblements sensibles ; grain de localisation le plus protecteur ; aucune reconstitution par croisement.
6. **Reformulation intégrale, obligatoire, sans exception.** Tu reprends des faits, jamais un texte. Chaque valeur est réécrite avec tes propres mots et une autre construction de phrase : ni copie, ni copie légèrement modifiée, ni traduction mot à mot. Seuls restent tels quels les noms, les nombres, les unités et les intitulés officiels courts (catégorie de liste rouge, article d'un texte). Après chaque page lue, enregistre son texte dans un fichier temporaire et lance `python3 "${CLAUDE_SKILL_DIR}/scripts/reformulation.py" fiches/<id>.json --source <fichier> --url <url>` : tant qu'il signale une reprise, réécris la valeur.
7. **Chaque information garde sa source.** L'ouvrage d'origine va dans `origine`, la page lue dans `source` et `url`, avec la licence et la date. La page HTML en tire une section « Sources » numérotée en fin de fiche.

## Entrée

`$ARGUMENTS` : un nom (scientifique ou vernaculaire), suivi éventuellement de `enrichir`, `verifier` ou `corriger`. Sans mot-clé : création ou mise à jour, puis enrichissement complet.

## Étape 0 — Préparer

1. **Export TAXREF local.** Cherche, dans cet ordre : la variable d'environnement `EXPERT_FAUNE_TAXREF` (dossier contenant `TAXREFvNN.txt`), `./data/taxref/v18/`, `~/.expert-faune-france/taxref/v18/`. S'il est absent, télécharge-le si le réseau le permet, en vérifiant l'empreinte :
   - adresse et empreinte SHA-256 : `${CLAUDE_SKILL_DIR}/config/taxref-v18.json` (champ `export`) ;
   - décompresse au moins `TAXREFv18.txt` et `habitats_note.csv` dans `~/.expert-faune-france/taxref/v18/`.
   Si le téléchargement est impossible, continue par la voie hors TAXREF et déclare TAXREF indisponible dans le rapport.
2. **Base documentaire.** Les fiches sont rangées dans `./fiches/` (ou `EXPERT_FAUNE_FICHES`). `fiches/index.json` associe chaque identifiant interne à ses noms, synonymes et identifiants externes. Crée-les s'ils n'existent pas.
3. **Profil de projet.** Si `./profil-projet.json` existe, applique-le à la sortie seulement (usage commercial, grain de localisation). Il ne change jamais le contenu du catalogue.

## Étape 1 — Résoudre l'identité

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/taxref.py" cherche --export "<dossier TAXREF>" --nom "<nom>"
```

Le script rend les taxons correspondants (nom retenu, synonyme ou nom vernaculaire), le CD_REF, l'auteur, les synonymes, l'habitat, le code de la colonne `FR` (France hexagonale et Corse) et la décision associée par la table officielle de correspondance.

- Un seul taxon au rang espèce : identité établie par TAXREF.
- Plusieurs (`"ambigu": true`) : applique [decisions.md](reference/decisions.md), section « Noms » (homonymie, vernaculaire partagé). Ne rattache jamais au hasard.
- Aucun : cherche l'identité dans le Catalogue of Life (ChecklistBank) ou un référentiel du groupe, puis la présence par la voie hors TAXREF (méthode §7.5).

Avant toute création, compare avec `fiches/index.json` (noms, synonymes, CD_REF). Un nom déjà connu enrichit la fiche existante : jamais de doublon.

## Étape 2 — Décider l'admission

Constitue un **dossier de preuves** (format des fichiers de `tests/cas/` du dépôt) puis applique les règles :

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/decider.py" dossier.json
```

Le script est la version exécutable de [decisions.md](reference/decisions.md) ; ses résultats sont testés. Il rend `creer_fiche`, `candidature`, `enrichir`, `exclusion`, `abstention`, `scission` ou `fusion`, avec le motif.

- `candidature` : écris `fiches/<id>.json` au format `schemas/candidature.schema.json` (motif, preuve manquante, sources consultées, déclencheurs de réexamen) et arrête l'enrichissement.
- `exclusion` : n'écris pas de fiche ; explique le motif (par exemple code M : domestique).
- `creer_fiche` ou `enrichir` : passe à l'étape 3.

## Étape 3 — Fiche minimale

Écris immédiatement la fiche minimale (`schemas/fiche.schema.json`) : identifiant interne (`EFF-` suivi du prochain numéro de l'index, jamais réutilisé), nom retenu, identité sourcée, présence qualifiée et sourcée (référentiel, colonne, code, signification), motif d'admission, familles à « non recherché ». Elle est publiable dès cet instant.

## Étape 4 — Enrichissement complet

Suis [reference/enrichissement.md](reference/enrichissement.md) : parcours **toutes** les familles pertinentes, des synthèses compétentes vers les publications originales et les ressources spécialisées. Pour chaque information :

- une affirmation au format `schemas/affirmation.schema.json` (source, **origine**, date ou version, territoire, contexte, licence, date de consultation) ;
- l'état du champ par `decider.py` (contexte distinct ≠ contradiction ; deux copies = une origine ; licence et portée de groupe filtrées) ;
- l'état de recherche de la famille : `recherche_effectuee`, `recherche_partielle`, `recherche_sans_resultat`, `acces_indisponible` ou `non_applicable` (avec justification).

**Compléter les champs restés vides.** Quand les sources de référence sont épuisées ou inaccessibles, cherche chaque champ vide dans les sources de complément (Wikipédia en français puis en anglais, autres sites listés dans [reference/sources.md](reference/sources.md)) : lis le texte source de la page (`action=raw`) pour voir l'ouvrage cité derrière chaque valeur. Marque l'affirmation `niveau: "complement"`, mets l'ouvrage cité en `origine` et `reference_citee: false` s'il n'y en a pas. Applique la règle 6 (reformulation contrôlée par `reformulation.py`). Respecte la politique de volume de chaque site (`sources.md`) : un site « usage ponctuel » ne sert que pour quelques champs, jamais de façon systématique. Un complément ne remplace jamais une source de référence.

Écris la fiche au fur et à mesure : une passe interrompue garde ses acquis et note un `point_de_reprise`.

## Étape 5 — Vérifier et rendre

1. Valide : `python3 "${CLAUDE_SKILL_DIR}/scripts/valider.py" fiches/<id>.json`. Corrige jusqu'à `✔`.
2. Mets à jour `fiches/index.json` (noms, synonymes, identifiants externes, historique).
3. Produis la page lisible : `python3 "${CLAUDE_SKILL_DIR}/scripts/rendre.py" fiches/<id>.json` (écrit `fiches/<id>.html`, à ouvrir dans un navigateur).
4. Réponds à l'utilisateur, en français :
   - **en tête** : sources réellement consultées (avec version) et indisponibilités ;
   - la décision et son motif ;
   - une synthèse lisible par famille : ce qui est établi, incertain, contradictoire, manquant ;
   - le bilan de couverture et les prochaines pistes ;
   - les chemins du fichier JSON et de la page HTML produits.

Ne déclare jamais une fiche complète : l'état `fiche_documentee` exige une passe terminée et un bilan explicite des lacunes.
