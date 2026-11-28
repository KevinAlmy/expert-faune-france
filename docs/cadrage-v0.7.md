# Expert faune de France — Note de cadrage

**Version 0.7, 28 novembre 2026.** Mise à jour du cadrage v0.6.

## 0. Changements de la v0.7 (ils prévalent sur le reste de la note)

1. **Le skill extrait, il ne stocke pas.** Il produit la fiche la plus complète possible et la remet à l'utilisateur. Il ne tient ni base de fiches, ni index, ni compteur, et ne relit jamais une fiche produite lors d'une exécution précédente. La conservation, le rapprochement avec les fiches déjà connues, le suivi des lacunes, le réexamen et la veille sont l'affaire de l'outil de l'utilisateur. Deux personnes qui utilisent le skill obtiennent chacune leurs propres fiches.
2. **Critères de l'utilisateur.** La demande peut porter des critères libres (thème à approfondir, territoire, usage commercial, nombre de photos, niveau de lecture). Ils orientent la recherche et la présentation sans assouplir les règles de preuve.
3. **Fiche fournie.** L'utilisateur peut fournir une fiche qu'il conserve, pour la faire vérifier ou enrichir ; le skill rend une nouvelle version sans rien garder.
4. **Identifiant déduit de l'espèce**, sans compteur : `EFF-TAXREF-<CD_REF>`, sinon `EFF-COL-<identifiant Catalogue of Life>`, sinon `EFF-NOM-<nom scientifique>`. La même espèce a toujours le même identifiant.
5. **Sources de complément.** Quand aucune source de référence ne renseigne un champ, des sources de complément (Wikipédia, sites naturalistes) peuvent le faire, marquées comme telles, jamais « corroborées », « incertaines » sans ouvrage cité, et toujours remplacées par une référence quand elle existe. Une politique de volume par site respecte le droit des bases de données.
6. **Reformulation intégrale obligatoire**, contrôlée automatiquement : aucune suite de six mots identiques à la page lue.
7. **Photos proposées.** Le skill propose des photos sous licence réutilisable (auteur connu, espèce vérifiée, contrôle visuel), jusqu'à trois par orientation (paysage, portrait), et en recommande une par orientation avec sa raison. Le choix et la validation des photos appartiennent à l'utilisateur ; le skill ne valide jamais une photo.

Les décisions du skill restent entièrement automatiques (principe 5). La validation humaine porte seulement sur ce que l'utilisateur choisit de garder et d'afficher dans son propre outil.

## 1. Principes directeurs

1. **Couverture d'abord.** Une fiche peut naître avec un nom scientifique, une identité établie et une présence sauvage étayée ; tous les autres champs s'enrichissent ensuite.
2. **Existence et présence sont deux faits distincts.** Qu'une espèce existe ne prouve pas qu'elle vit à l'état sauvage en France métropolitaine.
3. **Identité stable.** Chaque fiche porte un identifiant déduit de l'espèce (section 0), avec ses synonymes et ses identifiants externes, pour que l'outil de l'utilisateur la rapproche sans doublon de ce qu'il conserve déjà.
4. **Preuve par information.** Chaque information publiée remonte à une source d'origine datée, territorialisée et réutilisable dans les conditions de sa licence.
5. **Autonomie complète.** Le skill décide seul, selon des règles explicites. Quand les preuves ne suffisent pas, il s'abstient, garde les hypothèses sourcées dans la fiche et indique ce qui justifierait une nouvelle extraction. Chaque décision est expliquée.
6. **Indépendance.** Le skill ne dépend d'aucune application, d'aucune source unique et d'aucun choix de produit.

7. **Complétude progressive.** Toute demande de création d’une fiche déclenche une recherche dans toutes les familles pertinentes de la section 12.2. Chaque information disponible et suffisamment étayée est intégrée. Les lacunes sont décrites, avec les pistes pour une prochaine extraction.

## 2. Nom, périmètre et indépendance

- **Nom** : Expert faune de France.
- **Identifiant** : `expert-faune-france`.

**Périmètre.** Toute la faune sauvage de France métropolitaine, Corse comprise : milieux terrestres, eaux douces et milieux marins, dans le périmètre géographique documenté par le référentiel utilisé. Tous les groupes sont couverts au même titre : mammifères, oiseaux, reptiles, amphibiens, poissons, espèces sous-marines, insectes, arachnides, mollusques, crustacés et autres invertébrés, y compris les moins documentés. Une grenouille et un poisson qui partagent le même milieu ont tous deux leur place dans le catalogue.

**Utilisateurs.** Toute personne qui souhaite créer ses propres fiches sur cette faune, avec ses propres critères, ou faire vérifier et enrichir une fiche qu'elle conserve.

**Choix propres à chaque projet.** Un projet qui utilise le skill peut choisir les groupes, les qualifications de présence et les informations qu'il exploite. Ces choix vivent dans un **profil de projet** versionné, extérieur au socle (section 15). Ils ne modifient jamais le contenu du catalogue : ils déterminent seulement ce que le projet en exploite.

Le socle du skill ne contient ni marque, ni interface, ni modèle économique, ni préférence d'usage.

## 3. Mission

Extraire et vérifier la fiche la plus complète que permettent les connaissances accessibles et légalement réutilisables sur chaque animal de la faune sauvage métropolitaine. Rechercher systématiquement son identité, sa présence, sa biologie, sa reproduction, ses comportements, ses habitats, son cycle de vie, ses interactions écologiques, sa conservation et les conditions d’une observation respectueuse. Chaque information est reliée à ses preuves et à son contexte. La fiche est remise à l'utilisateur avec une description explicite des lacunes ; c'est lui qui la conserve et la fait progresser.

Le skill réalise une **validation documentaire argumentée** : chaque résultat indique ce qui est établi, ce qui reste incertain, ce qui est contradictoire et ce qui manque.

Il ne promet ni une connaissance exhaustive mémorisée, ni une connaissance instantanée des dernières publications. Il consulte les sources accessibles au moment de l'exécution, identifie leur version et rend compte, avec une date, de ce qu'il a réellement vérifié.

## 4. Composants

| Composant | Responsabilité |
|---|---|
| Skill | Méthode de recherche, choix des sources, règles de décision et de contrôle, formats de sortie. Ne conserve rien. |
| Base documentaire (chez l'utilisateur) | Fiches, candidatures, affirmations, références, versions, restrictions de diffusion et historique. Jamais dans le skill. |
| Validation éditoriale (chez l'utilisateur) | Choix des données affichées et validation des photos proposées. |
| Actualisation (chez l'utilisateur) | Relance du skill avec la fiche conservée, détection des changements, réexamen et application des décisions selon les règles de cette note. |

Le skill ne s'exécute pas seul en permanence : un agent ou un service disposant des outils nécessaires l'utilise à la demande ou depuis un traitement planifié. Chaque utilisateur branche ses propres données et outils.

## 5. Cas d'utilisation

**Dès la première version :**

- créer une fiche puis mener sa première passe complète d’enrichissement selon la section 9.6 ;
- enrichir automatiquement les thèmes incomplets d’une fiche existante ;
- produire dès la V1 des informations documentées sur l’observation respectueuse ;
- vérifier une fiche existante et produire une liste de corrections justifiées ;
- contrôler une modification précise avant son intégration ;
- résoudre un nom scientifique, un nom vernaculaire ou un synonyme vers une fiche ;
- vérifier des statuts en précisant territoire, population et date ;
- déterminer quelles informations, notamment de localisation, peuvent être diffusées ;
- revérifier une fiche ou une candidature fournie par l'utilisateur, par exemple après un nouvel export ;
- proposer des photos libres de droits, avec une recommandation par orientation.

**Plus tard :** réponses naturalistes à partir des données validées, aide à préparer une observation respectueuse, aide à l'identification d'un animal.

L'identification taxonomique d'un nom et l'identification d'un animal sur une image sont deux tâches différentes ; certaines déterminations demandent des critères non visibles sur une image.

## 6. Identité stable et prévention des doublons

### 6.1 Ce que porte chaque fiche

- un **identifiant déduit de l'espèce** (section 0), identique à chaque extraction de la même espèce ;
- le **nom retenu**, avec auteur et année lorsqu'ils sont disponibles ;
- les **anciens noms et synonymes**, avec auteur, année et source du rattachement ;
- les **identifiants externes** connus (TAXREF CD_NOM et CD_REF, Catalogue of Life, GBIF, référentiel spécialisé), chacun avec sa version ;
- l'**historique des rapprochements** : date, décision, motif et sources.

### 6.2 Contrôle avant toute création

Le skill ne conserve aucune fiche : la comparaison avec les fiches **et** candidatures existantes (nom retenu, synonymes, combinaison originale, auteur, année, identifiants externes) est faite par l'outil de l'utilisateur, à partir des informations que chaque fiche porte. Quand l'utilisateur fournit une fiche existante, le skill la compare lui-même. Les décisions du tableau suivant s'appliquent dans l'outil de l'utilisateur ; le skill les signale dans la fiche qu'il rend.

### 6.3 Décisions automatiques sur les noms

| Situation | Décision |
|---|---|
| Ancien nom rattaché sans ambiguïté à un seul taxon par le référentiel ou une source compétente | Enrichir la fiche existante : ajouter le synonyme et sa source. Aucune nouvelle fiche. |
| Même nom, auteurs différents (homonymie) | Ne rattacher que si l'auteur et l'année fournis lèvent l'ambiguïté. Sinon, s'abstenir : conserver les hypothèses sourcées et réexaminer à l'arrivée d'une nouvelle donnée. |
| Scission : une espèce divisée en plusieurs | Évaluer séparément l’identité et la présence sauvage métropolitaine de chaque espèce résultante. Créer les fiches qui remplissent les critères de la section 7 et conserver les autres comme candidatures. L'ancienne fiche devient un **concept historique** relié aux nouvelles fiches. Une donnée est réattribuée seulement si sa source permet de la départager (territoire, date, critères de détermination). Sinon, elle garde son attribution historique : elle n'est ni dupliquée ni affectée arbitrairement. |
| Fusion : plusieurs espèces réunies | La fiche du nom retenu est conservée. Les autres fiches deviennent des renvois vers elle, avec leur historique. Aucun identifiant n'est supprimé. |
| Nom retenu différent entre deux sources de référence | Conserver le nom du référentiel français utilisé. Documenter le nom concurrent comme hypothèse sourcée, jusqu'à son intégration éventuelle. |
| Espèce admise hors TAXREF, intégrée plus tard par TAXREF | Rattacher l'identifiant TAXREF à la fiche existante après contrôle des synonymes et du périmètre du taxon. Jamais de seconde fiche. |

## 7. Admission au catalogue

### 7.1 Deux faits à établir

Une espèce entre au catalogue lorsque deux faits sont suffisamment étayés :

1. son **identité** ;
2. sa **présence à l'état sauvage** en France métropolitaine, Corse comprise.

L'absence d'information sur l'alimentation, la reproduction, le statut de conservation ou tout autre champ n'empêche pas la création : ces champs restent « non renseignés ».

### 7.2 Fiche ou candidature

| Situation | Décision |
|---|---|
| Identité et présence sauvage étayées | **Créer la fiche**, avec le motif d'admission. |
| Identité établie, présence non étayée | **Conserver une candidature** : preuve manquante, motif, sources consultées. Réexamen automatique à l'arrivée de nouvelles données. |
| Identité ambiguë | **Candidature** avec les hypothèses sourcées. Aucune fiche tant que l'ambiguïté demeure. |

### 7.3 Qualifier la présence

Toute présence admise porte une qualification, pour que le lecteur sache ce qui est réellement attesté :

| Qualification | Admission | Signification |
|---|---|---|
| Établie, indigène | Oui | Présence sauvage régulière, d'origine naturelle. |
| Établie, introduite | Oui | Présence sauvage reproductrice issue d'une introduction. |
| Occasionnelle | Oui | Présence documentée mais irrégulière (erratique, migrateur rare). |
| Historique ou disparue | Oui, distinguée | Présence passée attestée, absente aujourd'hui selon la source. |
| Douteuse | Non : candidature | Présence signalée sans preuve suffisante. |
| Uniquement captive ou domestique | Non | Hors faune sauvage. |

### 7.4 Voie 1 : TAXREF

TAXREF est le premier référentiel consulté : nom retenu, synonymes, identifiants CD_NOM et CD_REF, version consultée.

Pour **chaque version** utilisée, le skill dispose d'une table de correspondance établie à partir de la documentation officielle de cette version :

| Élément à documenter | Contenu |
|---|---|
| Version et date de l'export | Numéro de version, date de publication, source du fichier. |
| Colonne territoriale | Colonne qui porte le statut pour la France métropolitaine, Corse comprise. |
| Codes de présence | Chaque code et sa signification, recopiés depuis la documentation de la version. |
| Décision associée | Qualification de la section 7.3 correspondant à chaque code. |

Règles :

- les espèces au rang espèce, au statut accepté et dont le code correspond à une qualification admise deviennent des fiches ;
- les taxons infraspécifiques sont conservés séparément et reliés à leur espèce ;
- un code absent de la table de correspondance donne une **candidature** avec le motif « code non documenté pour cette version » ;
- compter les lignes de TAXREF ne donne pas le nombre d'espèces : le fichier contient aussi d'autres rangs et des synonymes.

### 7.5 Voie 2 : admission hors TAXREF

Une espèce absente de TAXREF entre **immédiatement** au catalogue si une autre source compétente établit son identité et sa présence sauvage en métropole.

| Fait | Sources suffisantes seules | Sources insuffisantes seules |
|---|---|---|
| Identité | Description originale ; référentiel taxonomique du groupe ; Catalogue of Life. | Site généraliste, liste sans référence. |
| Présence sauvage en métropole | Description originale documentant un spécimen sauvage en métropole ; atlas ; publication avec spécimens ou observations localisés ; occurrence remontée jusqu'à son origine et vérifiée (ci-dessous). | Catalogue mondial ; répartition non sourcée ; occurrence d'agrégateur non remontée à son origine. |

Un seul document peut établir les deux faits : par exemple, une description originale qui documente un spécimen sauvage en Corse.

**Occurrence isolée sur un agrégateur (GBIF, OpenObs ou autre).** Le skill remonte au producteur, au spécimen ou à l'observation d'origine, puis vérifie :

- la localisation, comprise dans le territoire et cohérente avec sa précision déclarée ;
- le caractère sauvage (ni captivité, ni culture, ni élevage) ;
- la détermination, son auteur ou son niveau de validation chez le producteur ;
- la date ;
- l'indépendance vis-à-vis des autres preuves.

Si ces éléments sont établis, l'occurrence étaye la présence. Sinon, l'espèce reste candidate avec le motif précis.

**Motif d'admission.** Toute fiche admise hors TAXREF conserve la voie d'admission et les sources. Si une version ultérieure de TAXREF intègre l'espèce, la fiche lui est rapprochée (section 6.3).

### 7.6 Réexamen

Le skill ne garde rien : il indique dans chaque candidature et chaque fiche les événements qui justifieraient une nouvelle extraction. Les candidatures, les champs incertains et les hypothèses non rattachées sont réexaminés quand l'utilisateur relance le skill :

- à chaque nouvelle exécution qui les concerne ;
- à l'arrivée d'un nouvel export ou d'une nouvelle version de référentiel ;
- à l'apparition d'une nouvelle source pertinente.

## 8. Sources

### 8.1 Où chercher selon la question

| Question | Source à consulter en priorité | Remarque |
|---|---|---|
| Quel est le nom de l'espèce ? | Référentiel taxonomique : TAXREF, puis Catalogue of Life ou référentiel du groupe. | Un identifiant officiel n'a pas besoin d'être confirmé par d'autres sites. |
| Vit-elle à l'état sauvage en métropole ? | Statut biogéographique TAXREF, atlas, publication originale, occurrence remontée à son origine. | Un catalogue mondial ne suffit pas. |
| Est-elle protégée ? | Texte officiel en vigueur (Légifrance, EUR-Lex). | Ne jamais déduire la protection d'une catégorie de menace. |
| Risque-t-elle de disparaître ? | Évaluation Liste rouge datée et territorialisée. | Préciser territoire, population et date. |
| Biologie, comportement, milieux | Publication scientifique, atlas, synthèse spécialisée dont les références sont vérifiées. | Vérifier stade de vie, population, saison et unités. |
| Où la diffusion d'une localisation est-elle restreinte ? | Règle de diffusion du producteur de la donnée et règle territoriale applicable. | Une règle régionale ne vaut pas partout. |

### 8.2 Registre initial des sources

Chaque source reste candidate tant que sa disponibilité, ses conditions d'accès, sa licence et ses champs n'ont pas été vérifiés.

| Besoin | Sources | Usage |
|---|---|---|
| Identité | TAXREF (exports officiels, service web) ; Catalogue of Life via ChecklistBank ; référentiels spécialisés par groupe | Noms, synonymes, identifiants. |
| Statuts | BDC Statuts (PatriNat/INPN) ; référentiels de sensibilité | Index de statuts, avec remontée à leur source. |
| Menace | Comité français de l'UICN ; évaluations régionales officielles ; Liste rouge mondiale selon ses conditions | Catégories, dates, territoires, populations. |
| Droit | Légifrance, EUR-Lex, autorités compétentes | Régimes et textes en vigueur. |
| Occurrences et répartition | SINP, OpenObs, atlas nationaux et régionaux, GBIF | Présences datées et localisées, qualité, protocole, effort et précision. |
| Connaissance communale | Productions des Atlas de la biodiversité communale (ABC), rapports et jeux des producteurs locaux | Inventaires, habitats, cartographies et contexte territorial documenté. |
| Observations participatives | iNaturalist, directement ou via GBIF selon la donnée disponible | Occurrences et annotations pertinentes, après vérification de l’identité, de la qualité, des droits et de l’origine. |
| Biologie générale | INPN, OFB, muséums, programmes et atlas naturalistes | Synthèses et références de départ. |
| Groupes | Sociétés savantes et publications spécialisées (oiseaux, mammifères, reptiles et amphibiens, insectes, faune aquatique) | Connaissance par groupe. |
| Littérature | HAL, moteurs bibliographiques, sites des revues | Repérer puis lire les publications accessibles. |

Un titre, un DOI ou une notice ne suffisent pas à affirmer que le contenu d'un article a été vérifié.

### 8.3 Origine des preuves

Plusieurs portails peuvent diffuser un même jeu d'origine (par exemple INPN, BDC, UICN ou GBIF). Le skill enregistre **l'origine de la preuve**, pas seulement le site consulté. Deux sites qui reprennent la même étude comptent comme une seule origine. Une occurrence ne prouve ni l'abondance locale ni l'absence ailleurs.

### 8.4 Rôle des portails et nouvelles sources

TAXREF, INPN, OFB, SINP/OpenObs, UICN, GBIF, Catalogue of Life via ChecklistBank et la littérature figuraient déjà dans la v0.5. Les productions des ABC et iNaturalist sont ajoutées explicitement. Une source retenue dans le cadrage doit encore faire l’objet d’un contrôle d’accès avant son exploitation. Son inscription ne prouve aucune intégration technique.

- **OpenObs** donne accès aux observations et suivis diffusés par l’INPN. Le SINP organise la circulation des données. Conserver le producteur et le jeu d’origine pour documenter présence, dates, contexte et précision.
- **ABC** fournit une piste de recherche locale. Consulter les rapports, inventaires, cartographies et jeux associés au territoire. Le registre des projets sert à retrouver ces productions. Leur disponibilité, leur couverture taxonomique et leur ancienneté varient.
- **iNaturalist** constitue une source complémentaire. Contrôler le taxon, les éléments de détermination disponibles, le statut de qualité, la date, le caractère sauvage et la précision publique. Conserver séparément les droits des observations et des médias. Certaines observations sont aussi diffusées par GBIF, ce qui impose leur déduplication.
- **Catalogue of Life et ChecklistBank** sont reliés dans la chaîne d’accès aux données. Consigner le jeu et sa version pour éviter de compter deux accès au même contenu comme deux preuves.
- **Biologie et reproduction** nécessitent des synthèses spécialisées, atlas et publications adaptés au groupe. Les portails d’occurrences complètent ces connaissances dans leur contexte.

La liste des sources reste ouverte. Pour chaque thème, sélectionner la source compétente et poursuivre avec des ressources spécialisées lorsqu’elles apportent des informations supplémentaires. L’indisponibilité d’un portail déclenche la recherche d’une autre voie autorisée.

### 8.5 Observations, saisonnalité et recommandations

Avant une synthèse d’occurrences, contrôler identité, doublons, dates, coordonnées et précision, caractère sauvage, producteur et protocole. Utiliser les identifiants d’origine pour reconnaître les copies entre portails. En leur absence, conserver un indicateur de doublon probable et la règle appliquée, sans fusionner arbitrairement des observations distinctes.

Documenter l’emprise géographique, les années, le nombre d’observations exploitables et l’effort de prospection lorsqu’il est connu. Un pic de signalements décrit d’abord les données collectées. Toute interprétation en période d’activité, fréquence locale, tendance ou chance d’observation doit être étayée par une méthode et confrontée aux connaissances biologiques. L’absence de signalement reste qualifiée comme telle.

Les recommandations d’observation associent activité documentée, accessibilité autorisée du contexte et risque de dérangement. Les indices de reproduction sont interprétés à partir de comportements ou de stades documentés. Un simple signalement daté reste une preuve de présence. Toute recommandation conserve son territoire, sa période, ses preuves et ses limites.

## 9. Méthode de vérification par information

### 9.1 Résoudre l'identité

Rechercher le nom fourni, ses synonymes et les risques d'homonymie, puis appliquer la section 6. Tant qu'une ambiguïté demeure, ne jamais attribuer à une espèce les caractéristiques d'une autre.

### 9.2 Choisir la preuve adaptée

- Une source primaire compétente suffit pour le fait précis qu'elle établit, dans son périmètre et selon ses conditions de réutilisation.
- **Trois sources constituent un objectif de recherche, jamais un quota de publication.**
- Quand une donnée manque ou paraît fragile, rechercher d’abord deux sources complémentaires ciblées, puis poursuivre si une piste pertinente peut enrichir ou résoudre le champ. Ce premier effort de recherche ne fixe aucun plafond au nombre de sources.
- La recherche utilise le nom retenu et ses synonymes, en français et dans d'autres langues si utile : la littérature pertinente peut être internationale.

### 9.3 Examiner chaque affirmation

Pour chaque information publiée :

- enregistrer les sources qui la soutiennent et leur origine ;
- vérifier espèce, stade de vie, sexe, population, territoire, saison et unités ;
- distinguer observation ponctuelle, tendance, synthèse et recommandation ;
- comparer autorité, méthode, pertinence géographique et actualité ;
- rechercher corrections, rétractations et limites signalées lorsqu'elles sont accessibles ;
- séparer le fait de l'inférence et du conseil pratique.

Une source récente n'est pas automatiquement meilleure qu'une synthèse plus ancienne. La dernière évaluation officielle reste la dernière disponible, même ancienne.

### 9.4 Traiter les divergences

Aucun vote à la majorité. Le skill :

1. compare taxon, population, territoire, période et méthode : deux évaluations, l'une régionale, l'autre nationale, peuvent être exactes toutes les deux ;
2. identifie les dépendances entre sources et remonte à l'origine de chaque affirmation ;
3. compare méthode, date et autorité pertinente pour le champ ;
4. tranche si une source est clairement plus compétente pour ce fait, en enregistrant le motif ;
5. sinon, si le conflit persiste sur une même affirmation : conserve toutes les valeurs avec leurs références, marque le champ **contradictoire** et laisse la valeur de synthèse **indéterminée**. Les autres champs restent exploitables.

Une proposition scientifique de changement taxonomique est documentée comme hypothèse tant que le référentiel utilisé ne l'a pas intégrée.

### 9.5 Enrichir progressivement

Les champs établis sont publiés dès qu'ils sont disponibles. Une donnée manquante reste explicitement manquante. Une contradiction reste localisée au champ concerné. L'import des autres espèces se poursuit indépendamment.

Cette méthode s'inspire des principes d'évaluation critique des preuves ; elle ne constitue pas à elle seule une revue systématique ou une méta-analyse.

### 9.6 Procédure d’enrichissement complet

1. Résoudre l’identité, vérifier l’admission et publier les premiers champs établis.
2. Parcourir toutes les familles de la section 12.2. Déterminer les champs pertinents pour le groupe et rechercher les informations disponibles avec le nom retenu, ses synonymes et les termes spécialisés utiles.
3. Consulter les synthèses compétentes, puis approfondir les lacunes dans les publications originales et les ressources spécialisées. Utiliser les données locales et les occurrences lorsque la question le justifie.
4. Extraire des affirmations distinctes avec leur source, unité, plage de valeurs et contexte. Conserver les variations géographiques et biologiques. Chaque valeur propre à l’espèce doit disposer d’un support explicite.
5. Appliquer la vérification par champ, les décisions automatiques et les restrictions de diffusion. Publier progressivement les informations établies.
6. Produire une synthèse lisible, les données structurées, les références par champ et un bilan de couverture. Pour chaque lacune, conserver les recherches effectuées, leur résultat et la prochaine piste utile.
7. Terminer la passe lorsque chaque famille pertinente a été examinée et que les pistes prioritaires accessibles ont été traitées. Si une limite réelle de temps, d’accès ou de ressources interrompt le travail, indiquer les thèmes restants dans la fiche, comme pistes pour une prochaine extraction.

Pour une création en série, l'outil de l'utilisateur lance le skill espèce par espèce et conserve les résultats. Le travail sur une espèce peu documentée laisse progresser les autres. Toute information inconnue reste explicite. Aucune complétude absolue n’est déclarée.

## 10. Décisions automatiques

Le skill fonctionne sans aucune validation humaine. Chaque situation a une décision explicite et un motif enregistré.

| Situation | Décision automatique | Trace conservée |
|---|---|---|
| Espèce présente dans TAXREF avec un code admis | Créer la fiche, qualifier la présence. | Version, code, signification. |
| Espèce absente de TAXREF, identité et présence établies | Créer la fiche immédiatement. | Voie hors TAXREF, sources, faits établis par chacune. |
| Identité établie, présence non démontrée | Candidature. | Preuve manquante, motif, sources consultées. |
| Occurrence d'agrégateur non remontée à son origine | Ne pas l'utiliser comme preuve ; candidature si c'est la seule. | Motif. |
| Ancien nom sans ambiguïté | Enrichir la fiche existante. | Synonyme, source. |
| Homonymie ou rattachement ambigu | S'abstenir de rattacher ; conserver les hypothèses. | Hypothèses sourcées, critère manquant. |
| Scission | Admission vérifiée séparément pour chaque taxon résultant, concept historique conservé, réattribution seulement si départageable. | Version du référentiel, règle appliquée par donnée. |
| Fusion | Fiche retenue conservée, autres en renvoi. | Historique des identifiants. |
| Contradiction persistante | Champ contradictoire, synthèse indéterminée. | Toutes les valeurs et leurs références. |
| Correction d'une fiche existante | Appliquer si la nouvelle preuve est plus compétente pour ce champ ; sinon champ contradictoire. | Ancienne valeur, nouvelle valeur, preuve, motif. |
| Source indisponible | Conserver la dernière version connue. | Tentative datée, « consultation indisponible ». |
| Licence incompatible ou droits incertains | Conserver la référence et le lien, sans reprendre le contenu. | Licence constatée, usage refusé. |
| Localisation soumise à restriction ou dont la règle est incertaine | Diffuser au grain le plus protecteur applicable ; levée automatique dès que la source ou la règle l'autorise. | Règle appliquée, source de la restriction. |

## 11. Familles de statuts, conservées séparément

Aucune étiquette unique « sensible » ne résume ces enjeux.

| Dimension | Informations attendues | Règle |
|---|---|---|
| Taxonomie | Nom retenu, rang, synonymes, classification, identifiants internes et externes, versions | Source taxonomique identifiée et versionnée. |
| Présence | Territoire, qualification (section 7.3), code source et sa signification | Conserver le code et la version. |
| Risque de disparition | Catégorie de Liste rouge, territoire, population évaluée, date | Séparer évaluations mondiales, européennes, nationales et régionales. |
| Protection juridique | Texte, article ou annexe, champ géographique, période d'application, interdictions | Vérifier les textes officiels ; ne pas déduire la protection de la menace. |
| Sensibilité de diffusion | Règle nationale ou régionale, contexte, grain de diffusion autorisé, durée | Appliquer la règle à la donnée et au contexte ; préserver la restriction source. |
| Espèce exotique, caractère envahissant | Introduction, caractérisation écologique, classement réglementaire | Distinguer introduction, caractère envahissant et inscription réglementaire. |
| Autres réglementations | Chasse, pêche, capture, transport, commerce, CITES, directives | Chaque régime avec son territoire et sa validité ; aucune autorisation déduite d'un libellé. |
| Programmes de conservation | PNA, ZNIEFF, autres programmes | Nature exacte et périmètre du programme. |
| Précautions d'observation | Contexte biologique, risque de dérangement, conduite recommandée | Conseils documentés, distincts des statuts officiels. |

Les codes officiels des Listes rouges sont conservés tels quels (notamment EX, EW, CR, EN, VU, NT, LC, DD, NE et, dans les évaluations régionales, RE et NA). Un code absent n'équivaut pas à LC ; DD ou NE ne signifient pas absence de risque. Des catégories différentes selon le territoire ne sont pas une contradiction : seule la comparaison d'un même taxon, d'une même population, d'un même territoire et d'une même période peut en révéler une.

## 12. Fiche, traçabilité et états

### 12.1 Fiche minimale

Une fiche existe dès qu'elle contient : identifiant interne, nom retenu, identité sourcée, qualification de présence sourcée et motif d'admission. Tous les autres champs peuvent être « non renseignés ».

### 12.2 Blocs d'une fiche enrichie

| Famille à examiner | Informations recherchées selon leur pertinence pour le taxon |
|---|---|
| Identité | Noms scientifiques et vernaculaires, auteurs, rang, classification, synonymes, identifiants et versions. |
| Reconnaissance | Morphologie, dimensions et masse, variations selon sexe, âge et saison, stades, espèces proches, critères distinctifs et limites de détermination. |
| Présence et répartition | Aire documentée, présence métropolitaine et locale, indigénat ou introduction, statut historique ou occasionnel, résidente, migratrice ou hivernante selon les sources. |
| Habitats | Milieux, microhabitats, substrats, végétation associée, altitudes, profondeurs, conditions écologiques et usage saisonnier. |
| Alimentation | Régime, proies ou ressources, méthodes d’alimentation, variations selon âge, saison et milieu. |
| Reproduction | Maturité, calendrier territorialisé, parade, accouplement, lieux et supports décrits à un niveau compatible avec leur protection, ponte ou portée, incubation ou gestation, fréquence et soins parentaux. |
| Développement et longévité | Œuf, larve, métamorphose, croissance, émancipation, dispersion des jeunes, durée de vie et distinction entre données sauvages et captives. |
| Comportements | Sociabilité, territorialité, communication, vocalisations décrites, déplacements et comportements documentés. |
| Activité et cycle annuel | Activité journalière, présence saisonnière, migration, reproduction, mue, hibernation, diapause ou autres phases pertinentes. |
| Interactions écologiques | Prédateurs, proies, compétiteurs, parasites, mutualismes et rôle écologique lorsque documentés. |
| Conservation | Tendances étayées, menaces, évaluations territorialisées, protections, programmes et sensibilité de diffusion. |
| Observation respectueuse | Indices de présence, traces, sons décrits, conditions de détection documentées, confusions, limites, risques de dérangement et précautions contextualisées. |
| Traçabilité et couverture | Preuves par champ, dates, versions, états, droits, restrictions, historique, recherches effectuées et lacunes. |

Une période d'activité n'est pas automatiquement une période favorable à l'observation ; une période de reproduction appelle au contraire la plus grande prudence. Les déductions pratiques restent identifiées comme telles.

### 12.3 Trace de chaque information publiée

Pour chaque information : identifiant du champ, valeur, unité, taxon, **source d'origine**, **date ou version**, **territoire pertinent**, population, stade ou saison si utile, **état de vérification**, **conditions de réutilisation**, restriction de diffusion, date de consultation.

Chaque affirmation peut comporter plusieurs valeurs contextualisées. Les plages, unités, tailles d’échantillon et limites disponibles sont conservées. Une information générale sur un groupe est identifiée comme telle et ne remplit pas automatiquement un champ propre à une espèce. Des champs supplémentaires documentés peuvent compléter ces familles.

### 12.4 États

**Par champ** : documenté par la source de référence, corroboré, incertain, contradictoire, non renseigné. Aucun pourcentage de confiance n'est affiché sans méthode de calibration.

**Par entrée** : candidate, fiche minimale, fiche partielle, fiche documentée ; dans l'outil de l'utilisateur, concept historique (après scission) et renvoi (après fusion). L'état d'une fiche ne masque jamais un champ contradictoire ou une restriction.

**Par exécution** : sources effectivement consultées, version de chacune si connue, indisponibilités rencontrées.

**État de recherche, distinct de la fiabilité** — Pour chaque thème ou champ, enregistrer « non recherché », « recherche effectuée », « recherche partielle », « recherché sans résultat accessible » ou « accès indisponible ». Ajouter un motif pour les limites de réutilisation. Un champ non applicable au taxon porte une justification. La fiabilité conserve les états documenté, corroboré, incertain ou contradictoire.

**Bilan de couverture** — Fournir pour chaque famille les champs documentés, les lacunes, les thèmes à reprendre et la date de recherche. Un éventuel ratio de remplissage précise sa liste de champs applicables et mesure uniquement leur couverture. L’état « fiche documentée » exige une passe d’enrichissement terminée et un bilan des lacunes explicite.

Quatre dates restent distinctes : date de l'étude ou de l'évaluation, date de publication, date de collecte, date du dernier contrôle.

## 13. Droits, collecte et protection de la faune

### 13.1 Collecte autorisée

Ordre de préférence :

1. exports officiels et jeux ouverts ;
2. API et services documentés ;
3. consultation de pages ciblées ;
4. extraction automatisée seulement après contrôle des conditions applicables.

Chaque source automatisée a une **fiche d'accès** : propriétaire, licence et version, usages autorisés, conditions d'accès, éventuelle opposition à la fouille de textes et de données, fréquence et volume permis, restrictions de stockage, attribution exigée.

Un accès public, une citation, une politique d'indexation permissive ou une API ouverte ne suffisent pas à établir les droits de réutilisation. Droit d'auteur, droit des bases de données et données personnelles sont examinés séparément. Aucun contournement de connexion, de CAPTCHA, de paywall ou de restriction technique. Aucune collecte de données personnelles sans nécessité.

### 13.2 Licences par ressource

- **GBIF** : la licence est vérifiée **au niveau de chaque enregistrement exploité** ; un même jeu peut mêler plusieurs licences.
- **Listes rouges, BDC Statuts, textes, médias** : les conditions de la ressource précise sont vérifiées avant tout usage.
- **Droits incertains** : la référence bibliographique et le lien sont conservés, sans reprise du contenu.
- **Usage commercial** : un projet commercial déclare cet usage dans son profil ; les contenus incompatibles (par exemple sous clause « pas d'utilisation commerciale ») sont alors exclus de l'usage concerné.
- Les éléments sous accès restreint ne sont jamais transférés dans le dépôt public ni redistribués du seul fait qu'ils sont cités.

### 13.3 Localisations et respect de la faune

- Les restrictions de diffusion des localisations sont appliquées dans toutes les sorties : fiches, exports, cartes, réponses et métadonnées.
- Une précision masquée n'est jamais reconstituée en croisant plusieurs données, sources ou métadonnées d'images.
- Aucune indication exploitable vers des nids, gîtes, terriers ou rassemblements sensibles.
- Priorité à l'animal et à son milieu dans tous les conseils.
- Aucun conseil de poursuite, de manipulation, de déplacement d'un animal ou d'intrusion dans un site de reproduction.
- Aucune distance universelle, ni recommandation de repasse, d'appâtage ou de lumière artificielle, sans éléments spécifiques à l'espèce et au contexte.

Une licence choisie pour le skill ne remplace jamais les licences des données qu'il consulte.

## 14. Accès aux données et actualisation

### 14.1 Première version

- **Socle** : un export TAXREF **local, daté et versionné**, fourni au skill comme fichier.
- **Enrichissement dès la V1** : synthèses INPN/OFB, atlas, publications originales et ressources spécialisées, puis OpenObs/SINP, GBIF, productions des ABC et iNaturalist selon la question et les accès autorisés. Catalogue of Life via ChecklistBank complète l’identité.
- Un skill n'a pas d'accès réseau propre : il consulte ce que l'environnement qui l'exécute autorise.
- Chaque exécution indique les sources effectivement consultées, leur version si elle est connue et les indisponibilités rencontrées.
- Une panne temporaire n'est jamais une hypothèse permanente : elle n'efface aucune information déjà étayée et la consultation est retentée à l'exécution suivante. Une source indisponible n'est jamais présentée comme fraîchement consultée.

### 14.2 Réexamen

Dès la V1, le skill réexamine une fiche, une candidature ou un champ incertain que l'utilisateur lui fournit, par exemple après l'arrivée d'un nouvel export. Il ne réécrit pas systématiquement toutes les fiches : il cible les taxons et champs touchés par le changement.

### 14.3 Veille à terme

Objectif : une veille tous les quinze jours, ajoutée après la V1, **dans l'outil de l'utilisateur** (le skill ne s'exécute pas seul et ne garde rien).

- Le service mémorise une prochaine échéance espacée de quinze jours calendaires dans un fuseau horaire explicite. Une expression cron sur les jours du mois ne représente pas toujours quinze jours réguliers ; un contrôle quotidien peut lancer les travaux arrivés à échéance.
- Déroulement : lire versions et métadonnées des sources autorisées ; détecter les changements ; importer en zone de préparation ; identifier les taxons et champs touchés ; réexaminer en priorité les changements, les candidatures et les champs incertains ; produire les différences ; appliquer les décisions de la section 10 ; conserver versions, erreurs et résultats.
- Recherches bibliographiques ciblées par taxon et synonymes, avec une période de recouvrement pour les publications indexées tardivement.
- Journalisation, reprise, cache, limitation de débit, déduplication, exécutions sans effet doublon et retour arrière.

## 15. Dépôt et réutilisation

Dépôt Git open source indépendant : `expert-faune-france`.

**Licence proposée** : MIT pour le code et les instructions originales. Les données tierces conservent leurs propres licences.

Contenu du dépôt :

- `SKILL.md` : mission, déclenchement, procédure centrale ;
- méthode de vérification et règles de décision (sections 6 à 13) ;
- schéma JSON de la fiche, de la candidature et de la trace par information ;
- états possibles pour chaque champ et chaque entrée ;
- modèle de table de correspondance des codes TAXREF ;
- modèle de profil de projet ;
- cas de test avec leur résultat attendu ;
- scripts, seulement lorsqu'ils rendent un contrôle reproductible.

Le dépôt ne contient ni secret, ni données sous accès restreint, ni localisation sensible, ni copie non autorisée de contenus. L'import complet et l'hébergement des données restent extérieurs au skill.

**Profil de projet** (fichier de configuration, extérieur au socle) : groupes taxonomiques exploités, qualifications de présence exploitées, usage commercial ou non, règles de diffusion propres, textes d'affichage. Le catalogue reste identique quel que soit le profil.

## 16. Plus petite V1 utile

**Inclus** — Le dépôt de la section 15, un export TAXREF local versionné lorsque disponible, les autres voies d’admission, la procédure d’enrichissement complet, la matrice de couverture, les décisions automatiques et les cas de test ci-dessous. La V1 doit démontrer l’enrichissement biologique d’une fiche.

**Plus tard** : API publique, assistant conversationnel, médias (photos, sons), ordonnanceur de veille, pilote élargi à une trentaine de fiches une fois les comportements ci-dessous éprouvés.

### Cas de test et résultat attendu

| Cas | Résultat attendu |
|---|---|
| Espèce présente dans TAXREF avec un code admis | Fiche créée ; identifiants CD_NOM et CD_REF, version, code et qualification enregistrés. |
| Espèce décrite en Corse, absente de TAXREF, description originale avec spécimen sauvage | Fiche créée immédiatement, voie hors TAXREF ; identité et présence étayées par la même description ; rapprochement prévu avec une future version de TAXREF. |
| Espèce présente dans un catalogue mondial, présence française incertaine | Candidature ; identité établie ; motif « présence sauvage en métropole non démontrée » ; réexamen automatique. |
| Correction d'une fiche demandée sous un ancien nom | Rattachement au synonyme, fiche existante corrigée si la preuve est plus compétente ; aucune nouvelle fiche. |
| Scission ambiguë : ancienne observation impossible à départager | Chaque taxon résultant passe les critères d’admission séparément. L’observation garde son attribution historique. Un taxon sans présence métropolitaine étayée reste candidat. |
| Deux sites qui reprennent la même étude, contredits par une source indépendante | Une seule origine contre une ; comparaison du périmètre ; si le conflit persiste, champ contradictoire, synthèse indéterminée, autres champs exploitables. |
| Source indisponible | Dernière version connue conservée ; « consultation indisponible » daté ; aucune information effacée. |
| Licence restrictive (par exemple clause non commerciale dans un usage commercial) | Contenu non repris ; référence et lien conservés ; motif enregistré. |
| Localisation sensible | Diffusion au grain le plus protecteur ; aucune reconstitution par croisement. |
| Espèce aquatique (poisson ou espèce marine) | Admise dans le catalogue comme toute autre espèce. |
| Invertébré peu documenté | Fiche minimale admise ; champs non renseignés explicitement marqués. |

### Tests complémentaires d’enrichissement

| Cas | Résultat attendu |
|---|---|
| Espèce bien documentée | Toutes les familles pertinentes examinées. Biologie, reproduction, habitats, activité et observation renseignés lorsque les sources le permettent, avec preuves par champ. |
| Espèce peu documentée | Fiche disponible, lacunes et recherches explicites, pistes de reprise, aucune valeur biologique inventée. |
| Calendriers de reproduction différents selon les régions | Valeurs conservées avec territoire et période, sans moyenne nationale artificielle. |
| Observation visible dans OpenObs et GBIF, ou iNaturalist et GBIF | Origine retrouvée et preuve comptée une seule fois. |
| ABC avec uniquement une fiche de projet | Projet utilisé comme piste documentaire. Recherche du rapport ou du jeu d’inventaire avant toute affirmation sur les espèces. |
| Pic mensuel de signalements et effort inconnu | Répartition des signalements décrite avec limites. Aucune probabilité de rencontre déduite automatiquement. |
| Source supplémentaire après cinq références | Exploitée lorsqu’elle ajoute une information pertinente et réutilisable. |
| Valeur captive et valeur sauvage de longévité | Contextes conservés explicitement. |
| Passe interrompue | Thèmes restants indiqués dans la fiche ; l'utilisateur relance le skill en fournissant sa fiche, les acquis sont conservés sans doublon. |
| Information sur un groupe sans preuve propre à l’espèce | Contexte général identifié. Champ spécifique laissé non renseigné. |

## 17. Critères d'acceptation

- Aucune décision ne requiert de validation humaine ; chaque décision est expliquée par un motif enregistré.
- Aucune fiche créée à partir d'un nom ambigu ; aucun doublon après changement de nom, scission ou fusion.
- Existence et présence sauvage sont établies séparément.
- Chaque statut officiel porte sa source, son territoire et sa date ou version.
- Aucun arbitrage à la majorité ; une copie ou un agrégateur n'est pas une preuve indépendante.
- Une donnée manquante reste explicitement manquante.
- Une demande de fiche complète parcourt toutes les familles pertinentes et produit un bilan de couverture.
- La réussite d’une recherche taxonomique déclenche l’enrichissement biologique.
- Les champs non recherchés, sans résultat, inaccessibles et non applicables sont distingués.
- Le nombre de sources ne limite ni l’admission étayée ni l’enrichissement utile.
- Toute synthèse d’observations décrit ses données, sa méthode et ses limites.
- Une indisponibilité n'est pas une vérification réussie et n'efface rien.
- La date du dernier contrôle ne remplace pas la date de l'étude.
- Une modification est accompagnée de ses preuves et de son motif.
- Une restriction de diffusion s'applique à tous les canaux de sortie.
- Une source récente rétractée ou insuffisante ne remplace pas une référence établie.
- Une licence incompatible empêche l'usage concerné.
- Le skill et ses formats fonctionnent sans dépendre d'aucune application ni d'aucune source unique.
- Le skill ne conserve aucune fiche ni aucun fichier temporaire après l'exécution.
- Toute photo proposée a une licence réutilisable, un auteur crédité et un rattachement vérifié à l'espèce ; aucune n'est présentée comme validée par le skill.

## 18. Ordre de construction

1. Schéma JSON avec toutes les familles d’enrichissement, fiche, candidature, trace par information, états et bilan de couverture.
2. Table de correspondance des codes TAXREF pour la version utilisée.
3. Fiches d'accès des sources de la V1.
4. Rédaction du `SKILL.md` et des règles de décision.
5. Cas de test de la section 16, avec une fiche enrichie de bout en bout.
6. Publication du dépôt sous licence MIT.
7. Pilote élargi à une trentaine de fiches, tous groupes confondus.
8. Création en série et veille, dans l'outil de chaque utilisateur.
9. Assistant conversationnel.

## 19. Références

Références complémentaires consultées pour la mise à jour du 27 novembre 2026. Les conditions exactes sont contrôlées à nouveau avant chaque nouvel usage.

- OpenObs, accès INPN aux observations et suivis. https://www.data.gouv.fr/datasets/inpn-donnees-dobservation-et-de-suivi-sur-les-especes
- OFB, outils pour retrouver les productions des ABC. https://ofb.gouv.fr/mettre-en-oeuvre-un-projet-atlas-de-la-biodiversite-communale-abc-la-boite-a-outils
- Ministère de la Transition écologique, productions des ABC. https://www.ecologie.gouv.fr/politiques-publiques/atlas-biodiversite-communale
- iNaturalist, observations transmises à GBIF et distinction des licences des données et médias. https://inaturalist.freshdesk.com/en/support/solutions/articles/151000170346-which-inaturalist-observations-are-exported-for-gbif-and-how-often-does-this-export-happen-

Références conservées du cadrage précédent.

- TAXREF, référentiel taxonomique national (MNHN), jeu publié sur data.gouv.fr : https://www.data.gouv.fr/datasets/referentiel-taxonomique-taxref-1
- TAXREF, présentation et service web : https://taxref.mnhn.fr/taxref-web/
- PatriNat, téléchargement des référentiels liés à l'INPN : https://www.patrinat.fr/fr/page-temporaire-de-telechargement-des-referentiels-de-donnees-lies-linpn-7353
- BDC Statuts (PatriNat) : https://taxref.mnhn.fr/taxref-web/bdc
- Catalogue of Life, accès aux noms acceptés et synonymes : https://www.catalogueoflife.org/howto/access
- ChecklistBank, API : https://api.checklistbank.org/
- GBIF, accord d'utilisation des données : https://www.gbif.org/terms/data-user
- GBIF, licences proposées pour la publication de données : https://www.gbif.org/publishing-data
- GBIF, publication et métadonnées des médias : https://techdocs.gbif.org/en/data-publishing/multimedia-publishing
- Comité français de l'UICN, Liste rouge nationale : https://uicn.fr/especes/liste-rouge-france/
- Observatoire FAUNA, exemple de politique régionale de diffusion SINP : https://observatoire-fauna.fr/programmes/sinp/politique-de-diffusion
- HAL, API de recherche : https://api.hal.science/docs/search
- Collaboration for Environmental Evidence, lignes directrices : https://environmentalevidence.org/information-for-authors/guidelines-for-authors/
- OFB, 19 mars 2026, alerte sur certaines pratiques de photographie animalière : https://ofb.gouv.fr/sites/ofb-gouv-fr/files/2026-03/communique-de-presse-l-ofb-alerte-sur-les-derives-de-certains-photographes-animaliers_0.pdf
- LPO, manifeste pour une pratique éthique de la photographie de nature : https://www.lpo.fr/la-lpo-en-actions/education-a-l-environnement/ressources-pedagogiques/outils-pedagogiques/manifeste-pour-une-pratique-ethique-de-la-photographie-de-nature
- Code de la propriété intellectuelle, article L342-1 : https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006279247
- Code de la propriété intellectuelle, article L122-5-3 : https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044363192
- CNIL, collecte par moissonnage : https://www.cnil.fr/fr/focus-interet-legitime-collecte-par-moissonnage
- Skills dans Claude Code : https://code.claude.com/docs/en/skills
- Licences des dépôts GitHub : https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository

---

*Ce skill a été créé pour l’application Daffut. Nous le mettons à la disposition de toute personne souhaitant avoir accès à un expert en faune française.*
