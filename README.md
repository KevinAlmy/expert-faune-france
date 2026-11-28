# Expert faune de France

Un skill Claude Code qui **extrait et vérifie le maximum d'informations sur un animal de la faune sauvage de France métropolitaine** (Corse comprise) et vous **remet une fiche complète et sourcée** : mammifères, oiseaux, reptiles, amphibiens, poissons, espèces marines, insectes et autres invertébrés.

Vous lui demandez un animal, avec vos critères si vous le souhaitez ; il cherche, vérifie et vous rend la fiche. **Il ne garde rien** : vous conservez vos fiches dans votre propre outil, vous choisissez les informations que vous gardez et vous validez les photos. Deux personnes qui l'utilisent obtiennent donc chacune leurs propres fiches.

- **Identité et présence d'abord.** Une fiche naît dès que l'identité de l'espèce et sa présence à l'état sauvage sont étayées. Sinon, le skill rend une candidature, avec le motif et la preuve manquante.
- **Une preuve par information.** Chaque information remonte à sa source d'origine, datée, territorialisée, avec ses conditions de réutilisation ; une section « Sources » numérotée termine chaque fiche.
- **Le plus complet possible.** Reconnaissance, répartition, habitats, alimentation, reproduction, développement, comportements, activité, interactions, conservation, observation respectueuse. Sources de référence d'abord, puis sources de complément (Wikipédia…) pour les champs restés vides, toujours marquées comme telles ; textes toujours reformulés.
- **Photos libres de droits proposées.** Jusqu'à trois par orientation (paysage, portrait), sous licence réutilisable, avec le crédit prêt à afficher ; une recommandée par orientation. Vous choisissez et validez.
- **Entièrement automatique pendant l'extraction.** Chaque décision est expliquée ; quand les preuves manquent, le skill le dit et indique ce qui justifierait une nouvelle extraction.

Méthode complète : [docs/cadrage-v0.7.md](docs/cadrage-v0.7.md).

## Installation

Dans Claude Code (terminal ou application de bureau, version 2.1.275 ou ultérieure) :

```
/plugin install expert-faune-france --marketplace KevinAlmy/expert-faune-france
```

Ou en deux étapes :

```
/plugin marketplace add KevinAlmy/expert-faune-france
/plugin install expert-faune-france@faune-france
```

Vérification : `/plugin`, onglet **Installed**, affiche `expert-faune-france` activé.

> Les sessions cloud (claude.ai/code) ne chargent pas les plugins installés sur votre ordinateur. Pour les utiliser là, ouvrez une session sur ce dépôt : le skill y est disponible.

## Utilisation

```
/expert-faune-france:fiche Grenouille rousse
/expert-faune-france:fiche Hérisson d'Europe, insiste sur l'alimentation et l'hibernation, usage commercial
/expert-faune-france:fiche Brochet, territoire : Bretagne, 5 photos par orientation
/expert-faune-france:fiche Rana temporaria, vérifie et enrichis ma fiche ./mes-fiches/grenouille-rousse.json
```

Le skill écrit dans `./expert-faune-sortie/<animal>/` :
- `fiche.json` : la fiche structurée (format : [`skills/fiche/schemas/`](skills/fiche/schemas/)), à importer dans votre outil ;
- `fiche.html` : la même fiche, lisible dans un navigateur, avec les photos proposées et les sources.

Il répond aussi par une synthèse : sources consultées, décision et motif, informations par famille, photos recommandées, lacunes et pistes pour une prochaine extraction. Il efface ensuite ses fichiers temporaires : rien d'autre n'est conservé.

Exemples réels : [`docs/exemples/`](docs/exemples/) et [`docs/essais-10/`](docs/essais-10/).

## Données

Le skill s'appuie sur l'**export officiel TAXREF** (MNHN, Licence Ouverte 2.0), non inclus dans ce dépôt. Il le télécharge lui-même si le réseau le permet et vérifie son empreinte (voir [`skills/fiche/config/taxref-v18.json`](skills/fiche/config/taxref-v18.json)). Vous pouvez aussi le placer vous-même :

1. téléchargez `TAXREF_v18_2025.zip` depuis la page de téléchargement de PatriNat ;
2. décompressez `TAXREFv18.txt` et `habitats_note.csv` dans `~/.expert-faune-france/taxref/v18/` (ou indiquez le dossier dans la variable `EXPERT_FAUNE_TAXREF`).

Les autres sources (Catalogue of Life, GBIF, littérature…) sont consultées selon l'accès réseau de votre environnement. Chaque exécution indique celles qui ont réellement été consultées.

Quand les sources de référence ne suffisent pas, le skill complète les champs vides avec des **sources de complément** (Wikipédia et sites naturalistes), marquées comme telles. Les textes sont **toujours reformulés** (contrôle automatique) ; seuls les faits sont repris, avec leur source. La liste des sites et ce que chacun permet à grande échelle sont dans [`skills/fiche/reference/sources.md`](skills/fiche/reference/sources.md).

## Afficher les sources dans une application

**Photos.** Chaque photo proposée porte `statut: "proposee"` ; votre outil la passe à `validee` ou `refusee` (champ `validation` : par qui, quand). N'affichez que des photos validées, avec leur `credit`.

Chaque information d'une fiche porte son ouvrage d'origine (`origine`), la page lue (`source`, `url`), la licence et la date. La page HTML en tire une section « Sources » numérotée ; une application peut faire de même avec la fonction `references()` de `skills/fiche/scripts/rendre.py`, ou en regroupant les affirmations par `origine`. Citer ces sources est une condition des licences ouvertes (CC BY, CC BY-SA).

## Contenu du dépôt

| Chemin | Rôle |
|---|---|
| `skills/fiche/SKILL.md` | Procédure du skill |
| `skills/fiche/reference/` | Décisions automatiques, méthode, enrichissement, sources |
| `skills/fiche/schemas/` | Schémas JSON : fiche, candidature, affirmation, états, rapport d'exécution |
| `skills/fiche/config/` | Table des codes TAXREF v18, exemple de profil de projet |
| `skills/fiche/scripts/` | Recherche TAXREF, règles de décision exécutables, photos libres de droits, validation, contrôle de reformulation, page HTML |
| `tests/` | Cas de test avec résultat attendu |
| `docs/` | Cadrage de la méthode, exemples et essai sur 10 espèces |

## Contribuer

Les contributions sont bienvenues par pull request : voir [CONTRIBUTING.md](CONTRIBUTING.md). Chaque contribution est relue avant fusion.

## Licence

Code et instructions : [MIT](LICENSE). Les données consultées gardent leurs propres licences : voir [NOTICE.md](NOTICE.md).

---

*Ce skill a été créé pour l’application Daffut. Nous le mettons à la disposition de toute personne souhaitant avoir accès à un expert en faune française.*
