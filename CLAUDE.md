# Expert faune de France — consignes pour Claude Code

- Méthode de référence : `docs/cadrage-v0.7.md`. Procédure du skill : `skills/fiche/SKILL.md`.
- Toute modification d'une règle de décision : mettre à jour `skills/fiche/reference/decisions.md`, `skills/fiche/scripts/decider.py` et un cas dans `tests/cas/`, puis `python3 -m pytest tests`.
- Avant une pull request : `python3 -m pytest tests` et `claude plugin validate .` doivent réussir.
- Aucune décision du skill ne demande de validation humaine. Le skill ne stocke rien : il extrait et remet la fiche ; la conservation et la validation des photos se font chez l'utilisateur.
- Le dépôt ne contient ni l'export TAXREF (`data/`), ni les sorties d'essai (`expert-faune-sortie/`, `fiches/`), ni secret, ni donnée sous accès restreint.
- Les contributions passent par pull request et sont fusionnées par le mainteneur.
