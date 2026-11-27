# Journal des versions

## 0.1.0 — à publier

Première version (V1 du cadrage v0.6).

- Skill `fiche` : création, vérification, correction et enrichissement d'une fiche, entièrement automatiques.
- Export TAXREF v18 local : recherche par nom retenu, synonyme ou nom vernaculaire ; table officielle des codes de la colonne `FR` (France hexagonale et Corse) et décision associée.
- Règles de décision exécutables (`scripts/decider.py`) et 21 cas de test, dont la scission avec présence établie pour un seul taxon résultant.
- Sources de complément (Wikipédia et sites de même nature) : elles comblent seulement les champs qu'aucune source de référence ne renseigne, sont marquées comme telles, ne rendent jamais un champ « corroboré », et une valeur sans ouvrage cité reste « incertaine » (cas de test 22 à 24).
- Reformulation intégrale obligatoire, contrôlée par `scripts/reformulation.py` (aucune suite de 6 mots identiques à la page lue) ; liste des sites de complément avec, pour chacun, la politique de volume (usage systématique ou ponctuel) au regard du droit des bases de données.
- Section « Sources » numérotée en fin de page HTML ; appels [n] sur chaque champ ; fonction `references()` réutilisable.
- Essai sur 10 espèces de groupes différents (`docs/essais-10/`) : 82 % des champs documentés, dont 28 % par des compléments ; rapport et vérifications indépendantes.
- Le contrôle de reformulation porte sur le texte complet et brut de la page, jamais sur un résumé (reprises manquées lors de l'essai).
- Photos : deux photos par espèce (paysage et portrait) sous licence réutilisable, avec crédit prêt à afficher ; sources classées par qualité (photos primées de Wikimedia Commons, puis observations iNaturalist les plus appréciées) ; rattachement à l'espèce vérifié ; contrôle visuel obligatoire ; recadrage indiqué quand aucune photo de la bonne orientation ne convient (`scripts/photos.py`, règles et cas de test 25 à 27).
- Page HTML lisible de chaque fiche ou candidature (`scripts/rendre.py`), valeurs échappées, liens limités au web.
- Exemples réels produits par le skill de bout en bout : fiche Grenouille rousse (`docs/exemples/grenouille-rousse-EFF-000001.json`) et candidature Grenouille des bois, absente de France (`docs/exemples/grenouille-des-bois-EFF-000002.json`), avec leurs pages HTML.
- Correction : l'origine d'une preuve TAXREF n'est plus écrasée par l'origine biogéographique (relevé par le premier essai).
- Schémas JSON : fiche (11 familles d'enrichissement, bilan de couverture), candidature, affirmation, états, rapport d'exécution.
- Plugin et marketplace Claude Code.

Précisions de mise en œuvre par rapport au cadrage :

- Le code TAXREF C (cryptogène) est admis avec la qualification « établie » et l'origine « indéterminée », la section 7.3 du cadrage ne prévoyant pas d'origine inconnue.
- Le code G (ADN environnemental seulement) donne une candidature ; le code M (introduit non établi, domestique) une exclusion motivée.
- Un champ n'est « corroboré » que si chaque contexte (territoire, période, population, sauvage ou captivité) a au moins deux origines indépendantes.
