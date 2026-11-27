# Expert faune de France

Un skill Claude Code qui crée, vérifie, corrige et enrichit des **fiches sourcées sur la faune sauvage de France métropolitaine, Corse comprise** : mammifères, oiseaux, reptiles, amphibiens, poissons, espèces marines, insectes et autres invertébrés.

- **Identité et présence d'abord.** Une fiche naît dès que l'identité de l'espèce et sa présence à l'état sauvage sont étayées. Sinon, l'espèce reste candidate, avec le motif et la preuve manquante.
- **Une preuve par information.** Chaque information remonte à sa source d'origine, datée, territorialisée, avec ses conditions de réutilisation.
- **Enrichissement complet.** Reconnaissance, répartition, habitats, alimentation, reproduction, développement, comportements, activité, interactions, conservation, observation respectueuse ; les lacunes restent explicites.
- **Entièrement automatique.** Chaque décision est expliquée ; quand les preuves manquent, le skill s'abstient et réexamine plus tard.

Méthode complète : [docs/cadrage-v0.6.md](docs/cadrage-v0.6.md).

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
/expert-faune-france:fiche Rana temporaria enrichir
/expert-faune-france:fiche Salmo trutta verifier
```

Le skill rend une fiche JSON dans `./fiches/` (format : [`skills/fiche/schemas/`](skills/fiche/schemas/)) et une synthèse lisible : sources consultées, décision et motif, informations par famille, lacunes et prochaines pistes.

## Données

Le skill s'appuie sur l'**export officiel TAXREF** (MNHN, Licence Ouverte 2.0), non inclus dans ce dépôt. Il le télécharge lui-même si le réseau le permet et vérifie son empreinte (voir [`skills/fiche/config/taxref-v18.json`](skills/fiche/config/taxref-v18.json)). Vous pouvez aussi le placer vous-même :

1. téléchargez `TAXREF_v18_2025.zip` depuis la page de téléchargement de PatriNat ;
2. décompressez `TAXREFv18.txt` et `habitats_note.csv` dans `~/.expert-faune-france/taxref/v18/` (ou indiquez le dossier dans la variable `EXPERT_FAUNE_TAXREF`).

Les autres sources (Catalogue of Life, GBIF, littérature…) sont consultées selon l'accès réseau de votre environnement. Chaque exécution indique celles qui ont réellement été consultées.

## Contenu du dépôt

| Chemin | Rôle |
|---|---|
| `skills/fiche/SKILL.md` | Procédure du skill |
| `skills/fiche/reference/` | Décisions automatiques, méthode, enrichissement, sources |
| `skills/fiche/schemas/` | Schémas JSON : fiche, candidature, affirmation, états, rapport d'exécution |
| `skills/fiche/config/` | Table des codes TAXREF v18, exemple de profil de projet |
| `skills/fiche/scripts/` | Recherche TAXREF, règles de décision exécutables, validation |
| `tests/` | Cas de test avec résultat attendu |
| `docs/` | Cadrage de la méthode |

## Contribuer

Les contributions sont bienvenues par pull request : voir [CONTRIBUTING.md](CONTRIBUTING.md). Chaque contribution est relue avant fusion.

## Licence

Code et instructions : [MIT](LICENSE). Les données consultées gardent leurs propres licences : voir [NOTICE.md](NOTICE.md).

---

*Ce skill a été créé pour l’application Daffut. Nous le mettons à la disposition de toute personne souhaitant avoir accès à un expert en faune française.*
