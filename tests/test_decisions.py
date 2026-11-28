"""Chaque cas de tests/cas/ : le dossier de preuves donne le résultat attendu.

Le résultat attendu est comparé comme un sous-ensemble : chaque clé attendue
doit exister avec la même valeur ; les listes sont comparées élément par élément.
"""

import json
import sys
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "skills" / "fiche" / "scripts"))

from decider import decider  # noqa: E402

CAS = sorted((RACINE / "tests" / "cas").glob("*.json"))


def contient(obtenu, attendu, chemin="racine"):
    if isinstance(attendu, dict):
        assert isinstance(obtenu, dict), f"{chemin} : objet attendu, obtenu {obtenu!r}"
        for cle, valeur in attendu.items():
            assert cle in obtenu, f"{chemin}.{cle} absent de {list(obtenu)}"
            contient(obtenu[cle], valeur, f"{chemin}.{cle}")
    elif isinstance(attendu, list):
        assert isinstance(obtenu, list) and len(obtenu) == len(attendu), f"{chemin} : {obtenu!r} au lieu de {attendu!r}"
        for i, (o, a) in enumerate(zip(obtenu, attendu)):
            contient(o, a, f"{chemin}[{i}]")
    else:
        assert obtenu == attendu, f"{chemin} : {obtenu!r} au lieu de {attendu!r}"


@pytest.mark.parametrize("fichier", CAS, ids=[c.stem for c in CAS])
def test_cas(fichier):
    cas = json.loads(fichier.read_text(encoding="utf-8"))
    contient(decider(cas["dossier"]), cas["attendu"])


def test_aucune_decision_n_attend_un_humain():
    """Toute sortie est une décision ; aucun état « en attente de validation »."""
    interdit = {"validation_humaine", "en_attente_validation", "revue_manuelle"}
    for fichier in CAS:
        sortie = json.dumps(decider(json.loads(fichier.read_text(encoding="utf-8"))["dossier"]))
        assert not any(mot in sortie for mot in interdit), fichier.name


def test_scission_un_seul_taxon_admis_et_aucune_duplication():
    cas = json.loads((RACINE / "tests/cas/12-scission-presence-partielle.json").read_text(encoding="utf-8"))
    sortie = decider(cas["dossier"])["admission"]
    fiches = [r["taxon"] for r in sortie["resultants"] if r["decision"] == "creer_fiche"]
    assert fiches == ["A1"]
    attributions = [d["attribution"] for d in sortie["donnees_historiques"]]
    assert attributions == ["EFF-A", "EFF-A"], "observations ni dupliquées ni réaffectées"
