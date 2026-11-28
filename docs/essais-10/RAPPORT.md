# Expert faune de France : sources de complément et essai sur 10 espèces

Rapport du 27 novembre 2026, à soumettre pour avis critique. Il décrit ce qui a été ajouté au skill « Expert faune de France » (skill Claude Code qui produit des fiches d'espèces animales sourcées pour la France métropolitaine), puis les résultats d'un essai sur 10 espèces. Les fichiers produits sont dans le dépôt `KevinAlmy/expert-faune-france`, dossier `docs/essais-10/`.

## 1. Point de départ

La version 0.1.0 du skill ne consultait que des **sources de référence** : TAXREF v18 (export officiel, Licence Ouverte), Catalogue of Life, GBIF, BDC Statuts et rapportage Directive Habitats (PatriNat), listes rouges (UICN), littérature scientifique.

Un premier essai (Grenouille rousse) avait renseigné 29 champs sur 44. Les lacunes étaient la morphologie, les dimensions, le calendrier de reproduction, la taille de ponte, l'alimentation et le statut en Corse. Deux causes :
- l'INPN et OpenObs sont hors ligne, à la suite d'un incident de sécurité signalé par le porteur du projet ;
- l'environnement d'exécution bloquait la plupart des autres sites.

## 2. Ce qui a été ajouté au skill

### 2.1 Sources de complément, en second rang

Quand aucune source de référence ne renseigne un champ, et **pour ce champ seulement**, le skill consulte des sources de complément : Wikipédia (français puis anglais et autres langues) et des sites naturalistes.

Règles exécutables (`scripts/decider.py`, cas de test 22 à 24) :

| Situation | Résultat |
|---|---|
| Une source de référence renseigne le champ | Elle seule compte ; le complément est écarté, même s'il diverge (motif enregistré) |
| Seulement des compléments qui citent un ouvrage | `documente`, marqué `niveau: complement` ; jamais `corrobore` |
| Complément sans ouvrage cité, ou compléments divergents | `incertain`, marqué `niveau: complement` |
| Une référence devient disponible plus tard | Elle remplace le complément |

Chaque affirmation de complément enregistre :
- la page lue (`source`, `url`) ;
- l'ouvrage cité par cette page pour cette valeur (`origine`) ;
- `reference_citee` (vrai ou faux) ;
- la licence et la date de consultation.

Pour voir l'ouvrage cité derrière chaque phrase, Wikipédia est lue en texte source (`action=raw`).

### 2.2 Reformulation intégrale, obligatoire et contrôlée

Règle absolue n° 6 du skill : il reprend des faits, jamais un texte. Chaque valeur est réécrite avec d'autres mots et une autre construction : pas de copie, pas de copie légèrement modifiée, pas de traduction mot à mot. Seuls restent tels quels les noms, les nombres, les unités et les intitulés officiels courts.

Le contrôle est automatique : `scripts/reformulation.py` compare chaque valeur au texte brut de la page lue. Il refuse toute suite d'au moins 6 mots identiques, sans tenir compte des accents, de la casse ni de la ponctuation. Tant qu'il signale une reprise, la valeur doit être réécrite.

### 2.3 Politique de volume par site

La reformulation répond au droit d'auteur, mais pas au droit *sui generis* des bases de données (CPI, art. L342-1 et L342-2). Celui-ci interdit l'extraction d'une partie substantielle, ou l'extraction répétée et systématique de petites parties. Chaque site est donc classé :

- **Usage systématique**, sous licence ouverte : Wikipédia (CC BY-SA 4.0), Wikidata (CC0), Plazi (CC0), Biodiversity Heritage Library (domaine public pour l'essentiel), et les jeux de traits ouverts (AVONET, AmphiBIO, EltonTraits, PanTHERIA ; licence à vérifier par jeu).
- **Usage systématique sans usage commercial** : FishBase et SeaLifeBase (CC BY-NC), xeno-canto (licence par enregistrement).
- **Usage ponctuel**, droits réservés : quelques champs quand rien d'autre n'existe, jamais en série.
  - AmphibiaWeb, Animal Diversity Web, The Reptile Database ;
  - sociétés savantes (SHF, SFEPM, OPIE, LPO), DORIS ;
  - Oiseaux.net, Quel est cet animal ?, Lepinet.
- **Exclus** : sites payants, réseaux sociaux, sites qui interdisent la collecte automatisée. Les protections anti-robots ne sont jamais contournées.

### 2.4 Citation des sources

Chaque champ porte des appels numérotés vers une section « Sources » en fin de fiche. Cette section a une entrée par ouvrage d'origine et indique par quelle page il a été lu, sous quelle licence, à quelle date. Une fonction réutilisable (`references()`) permet à une application d'afficher la même section.

### 2.5 Position juridique retenue, à vérifier

- **Les faits ne sont pas protégés** par le droit d'auteur ; le texte l'est. D'où la reformulation obligatoire.
- **Wikipédia autorise la réutilisation**, y compris commerciale, sous deux conditions : citer, et partager à l'identique. Si une part substantielle d'une base de fiches vient de Wikipédia, cette base (pas l'application ni son code) doit être diffusée sous CC BY-SA 4.0. La licence 4.0 couvre aussi le droit des bases de données.
- **Les sites à droits réservés** ne peuvent pas être exploités en série, même avec reformulation (droit des bases de données).
- **Aucun avis juridique professionnel** n'a été demandé à ce stade.

## 3. Protocole de l'essai

- **10 espèces de groupes différents** : 2 mammifères, 1 oiseau, 1 reptile, 1 amphibien, 1 poisson, 2 insectes, 1 mollusque, 1 crustacé.
- **Exécution** : la commande réelle du skill (`/expert-faune-france:fiche <nom>`) en mode non interactif, 3 espèces à la fois, sans aucune intervention humaine.
- **Réseau** : environnement cloud dont la liste d'hôtes autorisés comprend Wikipédia, Wikidata, GBIF, ChecklistBank, PatriNat, UICN France, HAL, OpenAlex, Persée, iNaturalist, BHL, SHF, AmphibiaWeb et Légifrance.
  - INPN et OpenObs étaient hors ligne.
  - Légifrance a refusé les accès automatisés.
  - AmphibiaWeb a imposé une vérification anti-robots, non contournée.
- **Interruption** : 8 exécutions ont été coupées par une limite d'utilisation du service, puis relancées. Le skill a repris les fiches commencées à partir de leur point de reprise.
- **Vérifications indépendantes après coup** :
  - validation de chaque fiche contre les schémas JSON ;
  - recalcul de l'état de chaque champ par les règles du skill ;
  - nouveau contrôle de reformulation contre le texte brut des pages Wikipédia citées.

## 4. Résultats

### 4.1 Par espèce

Colonnes : champs examinés ; documentés par une référence ; documentés par un complément ; incertains ; vides ; part de Wikipédia parmi les affirmations ; durée (dernière exécution seulement).

| Espèce | Champs | Référence | Complément | Incertains | Vides | Wikipédia | Durée |
|---|---|---|---|---|---|---|---|
| Hérisson d'Europe (*Erinaceus europaeus*) | 81 | 63 (78 %) | 13 (16 %) | 5 | 0 | 19 % | 11 min |
| Pipistrelle commune (*Pipistrellus pipistrellus*) | 47 | 41 (87 %) | 1 (2 %) | 2 | 3 | 6 % | 5 min |
| Mésange charbonnière (*Parus major*) | 51 | 6 (12 %) | 44 (86 %) | 0 | 1 | 78 % | 7 min |
| Lézard des murailles (*Podarcis muralis*) | 45 | 10 (22 %) | 30 (67 %) | 4 | 1 | 75 % | 11 min |
| Salamandre tachetée (*Salamandra salamandra*) | 68 | 38 (56 %) | 10 (15 %) | 20 | 0 | 39 % | 10 min |
| Brochet (*Esox lucius*) | 65 | 39 (60 %) | 15 (23 %) | 10 | 1 | 42 % | 9 min |
| Lucane cerf-volant (*Lucanus cervus*) | 69 | 52 (75 %) | 10 (14 %) | 5 | 2 | 23 % | 11 min |
| Machaon (*Papilio machaon*) | 49 | 19 (39 %) | 18 (37 %) | 6 | 6 | 55 % | 7 min |
| Escargot de Bourgogne (*Helix pomatia*) | 60 | 24 (40 %) | 12 (20 %) | 10 | 14 | 40 % | 9 min |
| Écrevisse à pattes blanches (*Austropotamobius pallipes*) | 45 | 25 (56 %) | 7 (16 %) | 13 | 0 | 39 % | 10 min |

Les 10 fiches sont valides et ont l'état « fiche partielle » : le skill ne déclare jamais une fiche complète sans bilan explicite des lacunes.

Le Lucane a aussi produit une **candidature** pour *Lucanus capra*. Le Catalogue of Life et une publication de 2026 séparent les populations du sud de la France en une espèce distincte, que TAXREF v18 ne reconnaît pas encore. Faute de preuve de présence au sens du skill, aucune fiche n'est créée ; un réexamen est prévu à la sortie de TAXREF v19.

### 4.2 Ensemble des 10 fiches (580 champs)

| État du champ | Nombre | Part |
|---|---|---|
| Documenté par une source de référence | 317 | 54,7 % |
| Documenté par une source de complément | 160 | 27,6 % |
| Incertain ou contradictoire | 75 | 12,9 % |
| Non renseigné | 28 | 4,8 % |

Sans les compléments, environ 55 % des champs auraient été documentés au lieu de 82 % : les 160 champs complétés seraient restés vides ou incertains.

### 4.3 Sites utilisés (741 affirmations)

| Famille de sources | Affirmations | Part |
|---|---|---|
| Wikipédia (français et anglais) | 287 | 38,7 % |
| Littérature scientifique (articles, HAL, OpenAlex, DOI) | 172 | 23,2 % |
| GBIF (noms et occurrences) | 107 | 14,4 % |
| PatriNat / TAXREF (référentiel, BDC Statuts, Directive Habitats, sensibilité) | 96 | 13,0 % |
| UICN (listes rouges) | 37 | 5,0 % |
| Textes juridiques | 14 | 1,9 % |
| Autres sites | 14 | 1,9 % |
| Catalogue of Life | 10 | 1,3 % |
| Wikidata | 4 | 0,5 % |

Au total, 61 % des affirmations viennent de sources de référence et 39 % de compléments. Parmi les 289 affirmations de complément, 194 (67 %) s'appuient sur un ouvrage cité par la page ; les 95 autres n'en ont pas, et ne peuvent pas rendre un champ « documenté » à elles seules.

### 4.4 Contrôles indépendants

- **Schémas** : 11 fichiers valides sur 11.
- **Règles de décision** : 552 champs recalculés, aucun écart avec l'état écrit dans les fiches.
- **Reformulation** : 285 affirmations comparées au texte brut des 19 pages Wikipédia citées. Une seule fiche, le Lucane, contient des reprises : 3 courtes suites de 6 à 7 mots, par exemple « la femelle peut pincer jusqu'au sang ». Le skill avait pourtant déclaré n'en trouver aucune, sans doute parce qu'il a comparé avec un résumé de la page et non avec son texte brut. La consigne a été corrigée : le contrôle doit porter sur le texte complet et brut.

### 4.5 Exemples de compléments

- **Mésange charbonnière, plumage** : coiffe et gorge noires, grandes joues blanches, dos vert olive, ventre jaune barré de noir. L'origine citée par Wikipédia est Svensson et al. (2015), *Le guide ornitho*.
- **Mésange charbonnière, nourriture des poussins** : chenilles et araignées en forêt de feuillus ; larves de tenthrèdes et chenilles processionnaires en forêt de résineux. L'origine citée est Gosler et al. (2020), *Birds of the World*.
- **Brochet, proies occasionnelles** (écrevisses, amphibiens, canetons, rongeurs) : sans référence dans Wikipédia, donc enregistré comme tel.
- **Escargot de Bourgogne, taille de ponte** : 40 à 65 œufs. L'origine est AnimalBase (Université de Göttingen).

## 5. Limites constatées

1. **Les ouvrages cités par Wikipédia n'ont pas été lus.** L'origine enregistrée est celle que la page attribue. Une erreur de citation sur Wikipédia passerait inaperçue, et le skill ne peut pas détecter une information circulaire (citogenèse).
2. **La part de Wikipédia varie beaucoup d'une espèce à l'autre**, de 6 % (Pipistrelle) à 78 % (Mésange). Pour la Mésange, 44 champs sur 51 viennent de compléments, alors que des sources de référence existent sûrement (atlas des oiseaux nicheurs, *Birds of the World*, littérature). Le skill a pu se tourner trop vite vers les compléments quand les références étaient difficiles d'accès.
3. **Les pourcentages comptent des affirmations**, pas l'importance des informations. Un statut de protection pèse autant qu'une couleur de plumage.
4. **Un seul passage par espèce**, dans un environnement au réseau restreint, avec les principales bases françaises (INPN, OpenObs) hors ligne. Les résultats seraient différents sur un poste avec un accès complet.
5. **Le contrôle de reformulation ne détecte que les reprises littérales** d'au moins 6 mots. Il ne détecte pas une paraphrase trop proche, ni une traduction mot à mot depuis l'anglais.
6. **Une seule exécution du skill**, une fois sur 10 fiches, a mal appliqué son propre contrôle (point 4.4).

## 6. Questions posées

Merci de répondre point par point, de façon critique et argumentée, en distinguant ce qui est établi de ce qui est une opinion.

1. **Est-ce légal ?** Utiliser Wikipédia et les sites listés au 2.3 pour compléter un catalogue d'environ 65 000 fiches d'espèces, en reformulant intégralement et en citant les sources, en vue d'une application mobile qui pourrait devenir commerciale.
   - Droit d'auteur français et européen.
   - Droit *sui generis* des bases de données, y compris pour Wikipédia et pour les sites à droits réservés.
   - Portée exacte de la clause de partage à l'identique de CC BY-SA 4.0 pour une base de fiches reformulées, et ce qu'elle imposerait à l'application.
   - Conditions d'utilisation des sites et des API (limites de débit, robots).
   - Les règles du 2.3 sont-elles suffisantes ? Que faudrait-il changer ?
2. **Est-ce que cela améliore la qualité des données ?**
   - Le gain de couverture (55 % → 82 % des champs documentés) vaut-il le risque d'erreurs venant de sources secondaires ?
   - Les garde-fous du 2.1 suffisent-ils : priorité aux références, jamais « corroboré », « incertain » sans ouvrage cité, marquage visible ?
   - Faudrait-il exiger de lire l'ouvrage cité avant de considérer un complément comme « documenté » ?
3. **Est-ce mieux de compléter ainsi ?** Ou faut-il plutôt laisser les champs vides, chercher d'autres sources de référence, ou procéder autrement ?
   - Quelles sources ouvertes ou de référence manquent, en français comme en anglais, par groupe (oiseaux, mammifères, reptiles, amphibiens, poissons, insectes, mollusques, crustacés) ?
   - Comment éviter qu'une espèce comme la Mésange soit documentée surtout par Wikipédia ?
   - Quelles règles ajouter au skill, et quels tests ?
