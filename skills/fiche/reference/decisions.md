# Décisions automatiques

Cadrage v0.6, sections 6.3, 7, 9.4, 10 et 13. Version exécutable : `scripts/decider.py`, testée par `tests/cas/`. Aucune décision ne requiert de validation humaine : chaque situation a une décision et un motif enregistré.

## Admission

| Situation | Décision | Trace |
|---|---|---|
| Espèce dans TAXREF, code admis (table `config/taxref-vNN.json`) | `creer_fiche`, qualification du code | Version, colonne, code, signification |
| Absente de TAXREF, identité **et** présence établies par des sources suffisantes | `creer_fiche` immédiate, voie `hors_taxref`, rapprochement TAXREF prévu | Voie, sources, faits établis par chacune |
| Identité établie, présence non démontrée | `candidature` (`preuve_manquante: presence_sauvage_metropole`) | Motif, sources consultées, réexamen |
| Identité ambiguë | `candidature` avec hypothèses sourcées | Hypothèses, critère manquant |
| Code TAXREF D (douteux) ou G (ADNe seul) | `candidature` | Code et signification |
| Code M, Q, A, X ou aucun code | `exclusion` motivée (pas de fiche) | Code et signification |
| Code absent de la table de correspondance | `candidature`, motif « code non documenté pour cette version » | Code, version |
| Occurrence d'agrégateur non remontée à son origine | Pas une preuve ; `candidature` si c'est la seule | Motif |

**Suffisant seul pour l'identité** : TAXREF, description originale, référentiel taxonomique du groupe, Catalogue of Life.
**Suffisant seul pour la présence** : TAXREF (code admis), description originale documentant un spécimen sauvage en métropole, atlas, publication avec spécimens ou observations localisés, occurrence remontée à son origine et vérifiée (localisation, caractère sauvage, détermination, date, indépendance).
**Insuffisant seul** : catalogue mondial, répartition non sourcée, site généraliste, occurrence non remontée.

## Codes TAXREF v18 (colonne FR : France hexagonale et Corse)

| Code | Signification officielle | Décision | Qualification |
|---|---|---|---|
| P | Présent (indigène ou indéterminé) | fiche | établie, indigène |
| E | Endémique | fiche | établie, indigène |
| S | Subendémique | fiche | établie, indigène |
| C | Cryptogène | fiche | établie, origine indéterminée |
| I | Introduit | fiche | établie, introduite |
| J | Introduit envahissant | fiche | établie, introduite, envahissante |
| B | Occasionnel | fiche | occasionnelle |
| W | Disparu | fiche | historique |
| Y | Introduit éteint | fiche | historique (introduite) |
| Z | Endémique éteint | fiche | historique (indigène) |
| D | Douteux | candidature | — |
| G | ADNe uniquement | candidature | — |
| M | Introduit non établi (domestique, échappé) | exclusion | hors faune sauvage établie |
| Q | Mentionné par erreur | exclusion | — |
| A | Absent | exclusion | — |
| X | Éteint (globalement) | exclusion | — |
| (vide) | Aucun statut pour le territoire | exclusion | — |

Source des significations : `statuts_note.csv` et `TAXREFv18.pdf`, dans l'archive officielle (empreinte dans `config/taxref-v18.json`).

## Noms

| Situation | Décision |
|---|---|
| Ancien nom rattaché sans ambiguïté à un seul taxon | `enrichir` la fiche existante : ajout du synonyme et de sa source |
| Homonymie (même nom, auteurs différents) non levée par auteur et année | `abstention` : aucun rattachement, hypothèses conservées, réexamen |
| Nom vernaculaire partagé par plusieurs espèces | `abstention` : lister les espèces candidates, ne rien rattacher |
| Scission | Admission évaluée **séparément** pour chaque taxon résultant ; ancienne fiche → `concept_historique` relié aux nouvelles ; donnée réattribuée seulement si sa source permet de la départager, sinon attribution historique conservée (ni dupliquée, ni affectée arbitrairement) |
| Fusion | Fiche du nom retenu conservée ; autres fiches → `renvoi` ; aucun identifiant supprimé |
| Nom retenu différent entre deux référentiels | Nom du référentiel français conservé ; l'autre documenté comme hypothèse |
| Espèce admise hors TAXREF, intégrée plus tard | Rattacher l'identifiant TAXREF à la fiche existante ; jamais de seconde fiche |

## Champs

| Situation | Décision |
|---|---|
| Valeurs différentes dans des contextes différents (territoire, période, population, sauvage/captivité) | Toutes conservées avec leur contexte ; pas de moyenne ; pas une contradiction |
| Même contexte, valeurs différentes, une source clairement plus compétente | Valeur de la source la plus compétente, motif enregistré |
| Même contexte, conflit persistant | `contradictoire`, synthèse indéterminée, toutes les valeurs et références conservées ; autres champs exploitables |
| Deux portails ou sites reprenant la même étude | Une seule origine |
| `corrobore` | Au moins deux origines indépendantes **dans chaque contexte** ; sinon `documente` |
| Information générale sur le groupe | Identifiée comme telle ; ne remplit pas le champ propre à l'espèce |
| Licence incompatible (par exemple NC dans un usage commercial) ou droits incertains | Contenu non repris ; référence et lien conservés ; motif |
| Correction d'un champ existant | Appliquée si la nouvelle preuve est plus compétente ; sinon `contradictoire` |
| Source indisponible | Dernière version connue conservée ; « consultation indisponible » daté ; rien n'est effacé |
| Champ renseigné par une source de référence et par un complément | La référence seule ; le complément est écarté (motif enregistré), même s'il diverge |
| Champ renseigné seulement par des compléments citant leur ouvrage | `documente`, marqué `niveau: complement` ; jamais `corrobore` ; remplacé dès qu'une référence le renseigne |
| Complément sans référence citée, ou compléments divergents dans un même contexte | `incertain`, marqué `niveau: complement` |

## Photos

| Situation | Décision |
|---|---|
| Licence CC0, domaine public, CC BY, CC BY-SA | Admise si l'auteur est connu (sauf CC0 et domaine public) |
| Licence CC BY-NC ou CC BY-NC-SA | Refusée si le profil déclare un usage commercial ; sinon admise avec la restriction « usage non commercial » |
| Licence ND (pas de modification), droits réservés, licence inconnue, GFDL seule | Refusée : recadrer ou redimensionner serait interdit, ou la réutilisation n'est pas autorisée |
| Auteur inconnu | Refusée : le crédit exigé par la licence est impossible |
| Plus grand côté inférieur à 640 px | Refusée |
| Rattachement à l'espèce non vérifié (nom scientifique de l'élément Wikidata ou du taxon iNaturalist différent du nom retenu) | Refusée |
| Plusieurs photos admises | Ordre de priorité des sources ; la première est la photo principale |
| Aucune photo admise | Pas une erreur : la fiche le dit et la recherche est reprise à la prochaine exécution |

## Localisation

| Situation | Décision |
|---|---|
| Restriction connue | Grain le plus protecteur parmi les grains autorisés |
| Règle incertaine | Grain le plus protecteur ; levée automatique dès que la règle l'autorise |
| Toujours | Aucune reconstitution par croisement de données, de sources ou de métadonnées d'images |
