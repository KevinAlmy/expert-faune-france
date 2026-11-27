# Enrichissement complet

Cadrage v0.6, sections 8.5, 9.6 et 12. Toute création de fiche déclenche une passe complète sur toutes les familles pertinentes.

## Les familles à examiner

Clés JSON entre parenthèses (`familles` de `schemas/fiche.schema.json`).

| Famille | Informations recherchées, selon leur pertinence pour le taxon |
|---|---|
| Reconnaissance (`reconnaissance`) | Morphologie, dimensions et masse, variations selon sexe, âge et saison, stades, espèces proches, critères distinctifs, limites de détermination |
| Présence et répartition (`repartition`) | Aire documentée, présence métropolitaine et locale, indigénat ou introduction, statut historique ou occasionnel, résidente, migratrice ou hivernante |
| Habitats (`habitats`) | Milieux, microhabitats, substrats, végétation associée, altitudes, profondeurs, conditions écologiques, usage saisonnier |
| Alimentation (`alimentation`) | Régime, proies ou ressources, méthodes, variations selon âge, saison et milieu |
| Reproduction (`reproduction`) | Maturité, calendrier territorialisé, parade, accouplement, lieux et supports décrits à un niveau compatible avec leur protection, ponte ou portée, incubation ou gestation, fréquence, soins parentaux |
| Développement et longévité (`developpement`) | Œuf, larve, métamorphose, croissance, émancipation, dispersion, durée de vie, données sauvages et captives distinguées |
| Comportements (`comportements`) | Sociabilité, territorialité, communication, vocalisations décrites, déplacements |
| Activité et cycle annuel (`activite`) | Activité journalière, présence saisonnière, migration, mue, hibernation, diapause |
| Interactions écologiques (`interactions`) | Prédateurs, proies, compétiteurs, parasites, mutualismes, rôle écologique |
| Conservation (`conservation`) | Tendances étayées, menaces, évaluations territorialisées, protections, programmes, sensibilité de diffusion |
| Observation respectueuse (`observation_respectueuse`) | Indices de présence, traces, sons décrits, conditions de détection documentées, confusions, limites, risques de dérangement, précautions contextualisées |

L'identité, la traçabilité et la couverture sont portées par `identite`, chaque affirmation et `couverture`.

## Procédure (§9.6)

1. Identité résolue, admission vérifiée, fiche minimale écrite.
2. Pour chaque famille : déterminer les champs pertinents pour le groupe (une famille sans objet porte `non_applicable` et une justification) ; chercher avec le nom retenu, les synonymes et les termes spécialisés, en français et dans d'autres langues si utile.
3. Synthèses compétentes d'abord, puis publications originales et ressources spécialisées pour les lacunes ; données locales et occurrences quand la question le justifie.
4. Une affirmation distincte par valeur : source, origine, unité, plage, contexte (territoire, période, population, stade, sauvage ou captivité). Les variations géographiques et biologiques sont conservées.
5. État de chaque champ par `decider.py` ; restrictions de diffusion appliquées ; publication au fil de l'eau.
6. Rendre : synthèse lisible, données structurées, références par champ, bilan de couverture ; pour chaque lacune, les recherches faites, leur résultat et la prochaine piste.
7. Passe terminée quand chaque famille pertinente a été examinée et les pistes prioritaires accessibles traitées. Si une limite réelle (temps, accès) interrompt le travail : thèmes restants dans `couverture.point_de_reprise`, repris automatiquement à la prochaine exécution, sans doublon des acquis.

## Observations, saisonnalité et recommandations (§8.5)

Avant toute synthèse d'occurrences : contrôler identité, doublons (identifiants d'origine ; à défaut, indicateur de doublon probable sans fusion arbitraire), dates, coordonnées et précision, caractère sauvage, producteur, protocole. Documenter l'emprise, les années, le nombre d'observations exploitables et l'effort de prospection s'il est connu.

Un pic de signalements décrit d'abord les données collectées : aucune période d'activité, fréquence, tendance ou chance d'observation n'en est déduite sans méthode, confrontée aux connaissances biologiques. L'absence de signalement reste qualifiée comme telle. Un signalement daté prouve la présence, pas la reproduction : les indices de reproduction viennent de comportements ou de stades documentés.

Une recommandation d'observation associe activité documentée, accessibilité autorisée et risque de dérangement, et conserve son territoire, sa période, ses preuves et ses limites.

## Ce qui ne remplit jamais un champ

- une information générale sur le groupe ou la famille (à citer comme contexte) ;
- une valeur captive présentée comme sauvage ;
- une moyenne nationale fabriquée à partir de valeurs régionales ;
- une connaissance non sourcée.

Aucune complétude absolue n'est déclarée.
