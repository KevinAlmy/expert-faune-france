#!/usr/bin/env python3
"""Contrôle de reformulation : aucune valeur de la fiche ne reprend le texte d'une source.

Usage :
  python3 reformulation.py expert-faune-sortie/grenouille-rousse/fiche.json --source page.txt --url https://fr.wikipedia.org/wiki/...

`page.txt` est le texte de la page consultée (texte brut ou wikitexte), enregistré
pendant l'exécution. Seules les affirmations dont l'`url` vaut `--url` sont
contrôlées (toutes si `--url` est omis). Une affirmation échoue si elle partage
avec la source une suite d'au moins SEUIL mots identiques, accents, casse et
ponctuation ignorés. Code de sortie 1 en cas d'échec : la valeur doit être
réécrite (autres mots, autre construction), puis le contrôle relancé.

Bibliothèque standard seule.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

SEUIL = 6


def mots(texte: str) -> list[str]:
    sans_accents = "".join(c for c in unicodedata.normalize("NFD", texte) if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-z0-9]+", sans_accents.lower())


def ngrammes(liste: list[str], n: int) -> set[tuple[str, ...]]:
    return {tuple(liste[i : i + n]) for i in range(len(liste) - n + 1)}


def plus_longue_reprise(valeur: str, source: list[str], index: set[tuple[str, ...]]) -> str:
    """Plus longue suite de mots de `valeur` présente telle quelle dans la source (≥ SEUIL), sinon ''."""
    m = mots(valeur)
    meilleure: list[str] = []
    i = 0
    while i <= len(m) - SEUIL:
        if tuple(m[i : i + SEUIL]) in index:
            j = i + SEUIL
            texte_source = " " + " ".join(source) + " "
            while j < len(m) and f" {' '.join(m[i : j + 1])} " in texte_source:
                j += 1
            if j - i > len(meilleure):
                meilleure = m[i:j]
            i = j
        else:
            i += 1
    return " ".join(meilleure)


def affirmations(document: dict):
    """Parcourt toutes les affirmations de la fiche, avec leur chemin."""
    def parcourir(noeud, chemin):
        if isinstance(noeud, dict):
            if "valeur" in noeud and "source" in noeud:
                yield chemin, noeud
            for cle, enfant in noeud.items():
                yield from parcourir(enfant, f"{chemin}/{cle}")
        elif isinstance(noeud, list):
            for i, enfant in enumerate(noeud):
                yield from parcourir(enfant, f"{chemin}[{i}]")
    yield from parcourir(document, "")


def controler(document: dict, texte_source: str, url: str | None = None) -> list[dict]:
    source = mots(texte_source)
    index = ngrammes(source, SEUIL)
    echecs = []
    for chemin, a in affirmations(document):
        if url and a.get("url") != url:
            continue
        reprise = plus_longue_reprise(json.dumps(a["valeur"], ensure_ascii=False), source, index)
        if reprise:
            echecs.append({"chemin": chemin, "valeur": a["valeur"], "reprise": reprise})
    return echecs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("fiche", type=Path)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--url")
    args = parser.parse_args(argv)
    document = json.loads(args.fiche.read_text(encoding="utf-8"))
    echecs = controler(document, args.source.read_text(encoding="utf-8"), args.url)
    if not echecs:
        print(f"✔ aucune reprise de {SEUIL} mots ou plus depuis {args.source.name}")
        return 0
    print(f"✘ {len(echecs)} valeur(s) reprennent le texte de la source : à réécrire")
    for e in echecs:
        print(f"   - {e['chemin']} : « {e['reprise']} »")
    return 1


if __name__ == "__main__":
    sys.exit(main())
