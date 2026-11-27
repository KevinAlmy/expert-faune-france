# Méthode de vérification

Résumé opérationnel du cadrage v0.6 (sections 6 à 9, 11 et 13). En cas de doute, le cadrage complet fait foi : `docs/cadrage-v0.6.md`.

## Identité stable (§6)

Chaque fiche porte un identifiant interne `EFF-…`, attribué à la création, jamais réutilisé, indépendant des noms et des identifiants externes. Elle conserve le nom retenu (auteur, année), les anciens noms et synonymes avec leur source, les identifiants externes avec leur version (TAXREF CD_NOM et CD_REF, Catalogue of Life, GBIF) et l'historique des rapprochements (date, décision, motif, sources).

Avant toute création : comparer aux fiches **et** aux candidatures existantes par nom retenu, synonymes, combinaison originale, auteur, année et identifiants externes.

## Admission (§7)

Deux faits distincts : **identité** et **présence à l'état sauvage** en France métropolitaine, Corse comprise. Tous les autres champs peuvent rester « non renseignés ».

Voie 1, TAXREF : espèces au rang ES, nom accepté (CD_NOM = CD_REF), code de la colonne `FR` admis par la table de correspondance de la version. Les taxons infraspécifiques sont conservés séparément et reliés à leur espèce.

Voie 2, hors TAXREF : admission immédiate si une source compétente établit identité et présence (voir `decisions.md`). Une même description originale peut établir les deux faits. Une occurrence d'agrégateur (GBIF, OpenObs, iNaturalist) n'étaye la présence qu'après remontée au producteur, au spécimen ou à l'observation d'origine, et vérification de la localisation, du caractère sauvage, de la détermination, de la date et de l'indépendance.

Réexamen automatique des candidatures, champs incertains et hypothèses : à chaque exécution qui les concerne, à chaque nouvel export ou nouvelle version de référentiel, à chaque nouvelle source pertinente.

## Preuves (§8.3, §9)

- Une source primaire compétente suffit pour le fait précis qu'elle établit.
- Trois sources : objectif de recherche, jamais quota. Pour une donnée manquante ou fragile, chercher d'abord deux sources complémentaires ciblées, puis poursuivre tant qu'une piste peut enrichir ou résoudre le champ. Aucun plafond.
- Enregistrer **l'origine** de la preuve, pas seulement le site : deux sites qui reprennent la même étude, ou un même jeu diffusé par INPN, GBIF et OpenObs, comptent pour une seule origine.
- Pour chaque affirmation : espèce, stade, sexe, population, territoire, saison, unités ; observation ponctuelle, tendance, synthèse ou recommandation ; autorité, méthode, pertinence géographique, actualité ; corrections et rétractations ; fait, inférence et conseil séparés.
- Une source récente n'est pas automatiquement meilleure. La dernière évaluation officielle reste la dernière disponible, même ancienne.
- Un titre, un DOI ou une notice ne prouvent pas que le contenu a été vérifié : il faut l'avoir lu.

## Divergences (§9.4)

Aucun vote. Comparer taxon, population, territoire, période et méthode ; identifier les dépendances ; remonter à l'origine ; trancher si une source est clairement plus compétente (motif enregistré) ; sinon champ `contradictoire`, synthèse indéterminée, toutes les valeurs conservées. Une évaluation régionale et une nationale différentes peuvent être exactes toutes deux. Une proposition taxonomique non intégrée au référentiel reste une hypothèse documentée.

## Statuts, conservés séparément (§11)

Aucune étiquette unique « sensible ». Distinguer : taxonomie ; présence (qualification, code, signification) ; **risque de disparition** (Liste rouge : catégorie, territoire, population, date ; codes officiels conservés tels quels ; un code absent n'est pas LC ; DD et NE ne signifient pas absence de risque) ; **protection juridique** (texte officiel en vigueur, article ou annexe, champ géographique ; jamais déduite de la menace) ; **sensibilité de diffusion** (règle du producteur et règle territoriale) ; caractère exotique ou envahissant (introduction, caractérisation écologique, inscription réglementaire, distinctes) ; autres réglementations (chasse, pêche, commerce, CITES) ; programmes de conservation ; précautions d'observation (conseils documentés, distincts des statuts).

## Droits et collecte (§13)

Ordre : exports officiels et jeux ouverts ; API documentées ; pages ciblées ; extraction automatisée seulement après contrôle des conditions. Jamais de contournement de connexion, de CAPTCHA, de paywall ni de protection anti-robots. Aucune donnée personnelle sans nécessité.

- GBIF : licence vérifiée **par enregistrement** (un même jeu mêle CC0, CC BY et CC BY-NC).
- iNaturalist : droits des observations et des médias distincts.
- Listes rouges, BDC Statuts, textes, médias : conditions de la ressource précise.
- Droits incertains : référence et lien conservés, contenu non repris.
- Usage commercial déclaré dans le profil : contenus NC exclus de cet usage.
- Rien sous accès restreint n'est versé dans un dépôt public.

## Localisations et respect de la faune (§13.3)

Restrictions appliquées à toutes les sorties ; aucune reconstitution d'une précision masquée ; aucune indication exploitable vers nids, gîtes, terriers ou rassemblements sensibles ; priorité à l'animal ; aucun conseil de poursuite, manipulation, déplacement ou intrusion ; aucune distance universelle, repasse, appâtage ou lumière artificielle sans éléments propres à l'espèce et au contexte. Une période de reproduction appelle la plus grande prudence, pas une recommandation d'observation.
