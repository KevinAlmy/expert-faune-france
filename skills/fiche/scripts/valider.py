#!/usr/bin/env python3
"""Valide une fiche ou une candidature contre les schémas du skill.

Usage : python3 valider.py sortie.json [autre.json ...]
Le type est déduit du champ « etat » (candidate → candidature, sinon fiche).
Nécessite le paquet jsonschema ; sans lui, seuls les champs obligatoires sont contrôlés.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCHEMAS = Path(__file__).resolve().parent.parent / "schemas"


def charger(nom: str) -> dict:
    return json.loads((SCHEMAS / nom).read_text(encoding="utf-8"))


def schema_pour(document: dict) -> str:
    return "candidature.schema.json" if document.get("etat") == "candidate" else "fiche.schema.json"


def erreurs(document: dict) -> list[str]:
    nom = schema_pour(document)
    schema = charger(nom)
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
    except ImportError:
        manquants = [c for c in schema.get("required", []) if c not in document]
        return [f"champ obligatoire absent : {c}" for c in manquants]
    ressources = [
        (f"{charger(f.name)['$id']}", Resource.from_contents(charger(f.name)))
        for f in SCHEMAS.glob("*.schema.json")
    ]
    ressources += [(f.name, Resource.from_contents(charger(f.name))) for f in SCHEMAS.glob("*.schema.json")]
    registre = Registry().with_resources(ressources)
    validateur = Draft202012Validator(schema, registry=registre)
    return [
        f"{'/'.join(str(p) for p in e.absolute_path) or '(racine)'} : {e.message}"
        for e in sorted(validateur.iter_errors(document), key=lambda e: list(e.absolute_path))
    ]


def main(chemins: list[str]) -> int:
    code = 0
    for chemin in chemins:
        document = json.loads(Path(chemin).read_text(encoding="utf-8"))
        liste = erreurs(document)
        if liste:
            code = 1
            print(f"✘ {chemin} ({schema_pour(document)})")
            for e in liste:
                print(f"   - {e}")
        else:
            print(f"✔ {chemin} ({schema_pour(document)})")
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
