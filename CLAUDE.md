# Expert faune de France — consignes pour Claude Code

- Méthode de référence : `docs/cadrage-v0.6.md`. Procédure du skill : `skills/fiche/SKILL.md`.
- Toute modification d'une règle de décision : mettre à jour `skills/fiche/reference/decisions.md`, `skills/fiche/scripts/decider.py` et un cas dans `tests/cas/`, puis `python3 -m pytest tests`.
- Avant une pull request : `python3 -m pytest tests` et `claude plugin validate .` doivent réussir.
- Aucune décision du skill ne demande de validation humaine.
- Le dépôt ne contient ni l'export TAXREF (`data/`), ni les fiches d'essai (`fiches/`), ni secret, ni donnée sous accès restreint.
- Les contributions passent par pull request et sont fusionnées par le mainteneur.
