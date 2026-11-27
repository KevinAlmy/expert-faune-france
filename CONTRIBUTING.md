# Contribuer

Merci de votre intérêt pour Expert faune de France.

## Comment proposer une modification

1. Créez une copie du dépôt (**Fork**), puis une branche.
2. Faites votre modification et, si elle touche une règle, ajoutez ou adaptez un cas dans `tests/cas/` avec le résultat attendu.
3. Lancez les tests : `pip install pytest jsonschema` puis `python3 -m pytest tests`.
4. Ouvrez une **pull request** en expliquant le changement et, pour toute règle naturaliste, la source qui la justifie.

Chaque pull request est relue par le mainteneur avant fusion. Les tests automatiques doivent être verts.

## Règles de fond

- La méthode de référence est [docs/cadrage-v0.6.md](docs/cadrage-v0.6.md). Une modification de méthode le met à jour et note la décision dans `CHANGELOG.md`.
- Une règle de décision du skill n'attend jamais une validation humaine : quand les preuves manquent, elle s'abstient avec un motif.
- Aucune valeur sans source. Aucune donnée sous accès restreint, aucune localisation sensible, aucune copie de contenu non autorisée dans le dépôt.
- Le socle reste indépendant de toute application : les choix propres à un projet vont dans un profil de projet.

## Licence des contributions

En proposant une contribution, vous acceptez qu'elle soit publiée sous la licence MIT du dépôt.
