#!/usr/bin/env python3
"""Recherche d'un taxon dans un export TAXREF local (bibliothèque standard seule).

Usage :
  python3 taxref.py cherche --export DOSSIER --nom "Rana temporaria"
  python3 taxref.py cherche --export DOSSIER --nom "Grenouille rousse"
  python3 taxref.py compte  --export DOSSIER

DOSSIER contient TAXREFvNN.txt (et, facultatif, habitats_note.csv). La table de
correspondance des codes est lue dans ../config/taxref-vNN.json.

Sortie : JSON sur la sortie standard. Le script ne décide rien d'autre que ce
que TAXREF dit ; la décision (fiche, candidature, exclusion) applique la table
de correspondance, documentée et versionnée.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
csv.field_size_limit(10**9)


def normaliser(texte: str) -> str:
    """Minuscules, sans accents, sans ponctuation superflue."""
    sans_accents = "".join(
        c for c in unicodedata.normalize("NFD", texte) if unicodedata.category(c) != "Mn"
    )
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s-]", " ", sans_accents.lower())).strip()


def trouver_export(dossier: Path) -> tuple[Path, str]:
    fichiers = sorted(dossier.glob("TAXREFv*.txt"))
    if not fichiers:
        raise SystemExit(f"Aucun fichier TAXREFvNN.txt dans {dossier}")
    fichier = fichiers[-1]
    version = re.search(r"TAXREFv(\d+)", fichier.name).group(1)  # type: ignore[union-attr]
    return fichier, version


def charger_config(version: str) -> dict:
    chemin = CONFIG_DIR / f"taxref-v{version}.json"
    if not chemin.exists():
        raise SystemExit(
            f"Table de correspondance absente : {chemin.name}. "
            "Toute espèce de cette version resterait candidate (« code non documenté »)."
        )
    return json.loads(chemin.read_text(encoding="utf-8"))


def libelles_habitats(dossier: Path) -> dict[str, str]:
    chemin = dossier / "habitats_note.csv"
    if not chemin.exists():
        return {}
    brut = chemin.read_bytes()
    try:
        texte = brut.decode("utf-8")
    except UnicodeDecodeError:
        texte = brut.decode("cp1252")
    return {
        ligne["HABITAT"]: ligne["LB_HABITAT"]
        for ligne in csv.DictReader(texte.splitlines(), delimiter=";")
    }


def lignes(fichier: Path):
    with fichier.open(encoding="utf-8", newline="") as flux:
        yield from csv.DictReader(flux, delimiter="\t")


def decision_code(config: dict, code: str) -> dict:
    regle = config["codes"].get(code)
    if regle is None:
        return {
            "decision": "candidature",
            "motif": f"code « {code} » non documenté pour la version {config['version']}",
        }
    return regle


def chercher(dossier: Path, requete: str) -> dict:
    fichier, version = trouver_export(dossier)
    config = charger_config(version)
    habitats = libelles_habitats(dossier)
    cible = normaliser(requete)

    animaux: dict[str, dict] = {}
    correspondances: dict[str, set[str]] = {}
    for ligne in lignes(fichier):
        if ligne["REGNE"] != "Animalia":
            continue
        cd_ref = ligne["CD_REF"]
        if ligne["CD_NOM"] == cd_ref:
            animaux.setdefault(cd_ref, {})["accepte"] = ligne
        animaux.setdefault(cd_ref, {}).setdefault("synonymes", [])
        if ligne["CD_NOM"] != cd_ref:
            animaux[cd_ref]["synonymes"].append(ligne)

        if normaliser(ligne["LB_NOM"]) == cible or normaliser(ligne["NOM_COMPLET"]) == cible:
            type_ = "nom_retenu" if ligne["CD_NOM"] == cd_ref else "synonyme"
            correspondances.setdefault(cd_ref, set()).add(type_)
        elif ligne["CD_NOM"] == cd_ref and ligne["NOM_VERN"]:
            noms = [normaliser(n) for n in re.split(r",", re.sub(r"\(.*?\)", "", ligne["NOM_VERN"]))]
            if cible in noms:
                correspondances.setdefault(cd_ref, set()).add("vernaculaire")

    resultats = []
    for cd_ref, types in correspondances.items():
        entree = animaux.get(cd_ref, {})
        accepte = entree.get("accepte")
        if accepte is None:
            continue
        code = accepte["FR"]
        regle = decision_code(config, code)
        resultats.append(
            {
                "correspondance": sorted(types),
                "cd_ref": cd_ref,
                "nom_retenu": accepte["LB_NOM"],
                "auteur": accepte["LB_AUTEUR"],
                "nom_complet": accepte["NOM_COMPLET"],
                "rang": accepte["RANG"],
                "classification": {
                    k.lower(): accepte[k] for k in ("PHYLUM", "CLASSE", "ORDRE", "FAMILLE")
                },
                "groupes_inpn": [accepte[k] for k in ("GROUP1_INPN", "GROUP2_INPN", "GROUP3_INPN") if accepte[k]],
                "noms_vernaculaires": accepte["NOM_VERN"],
                "habitat": {"code": accepte["HABITAT"], "libelle": habitats.get(accepte["HABITAT"], "")},
                "statut_fr": {
                    "colonne": config["documentation"]["colonne_territoriale"],
                    "code": code,
                    "signification": regle.get("signification", ""),
                },
                "decision_taxref": regle,
                "synonymes": [
                    {"cd_nom": s["CD_NOM"], "nom": s["LB_NOM"], "auteur": s["LB_AUTEUR"]}
                    for s in entree.get("synonymes", [])
                ][:50],
                "url": accepte["URL"],
            }
        )

    especes = [r for r in resultats if r["rang"] == "ES"]
    return {
        "requete": requete,
        "taxref": {"version": version, "fichier": fichier.name, "sha256": config["export"]["sha256"]},
        "nombre_taxons": len(resultats),
        "ambigu": len({r["cd_ref"] for r in especes}) > 1,
        "resultats": resultats,
    }


def compter(dossier: Path) -> dict:
    fichier, version = trouver_export(dossier)
    config = charger_config(version)
    filtre = config["filtre_especes"]
    par_code: dict[str, int] = {}
    for ligne in lignes(fichier):
        if ligne["REGNE"] != filtre["regne"] or ligne["RANG"] != filtre["rang"]:
            continue
        if ligne["CD_NOM"] != ligne["CD_REF"]:
            continue
        par_code[ligne["FR"]] = par_code.get(ligne["FR"], 0) + 1
    decisions: dict[str, int] = {}
    for code, n in par_code.items():
        d = decision_code(config, code)["decision"]
        decisions[d] = decisions.get(d, 0) + n
    return {"version": version, "par_code": par_code, "par_decision": decisions}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="commande", required=True)
    p_cherche = sub.add_parser("cherche")
    p_cherche.add_argument("--export", required=True, type=Path)
    p_cherche.add_argument("--nom", required=True)
    p_compte = sub.add_parser("compte")
    p_compte.add_argument("--export", required=True, type=Path)
    args = parser.parse_args(argv)
    resultat = chercher(args.export, args.nom) if args.commande == "cherche" else compter(args.export)
    json.dump(resultat, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
