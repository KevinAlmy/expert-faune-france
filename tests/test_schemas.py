"""Les exemples respectent les schémas ; un document incomplet est rejeté."""

import copy
import json
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "skills" / "fiche" / "scripts"))

from valider import erreurs  # noqa: E402

EXEMPLES = RACINE / "tests" / "exemples"


def charger(nom):
    return json.loads((EXEMPLES / nom).read_text(encoding="utf-8"))


def test_fiche_minimale_valide():
    assert erreurs(charger("fiche-minimale.json")) == []


def test_candidature_valide():
    assert erreurs(charger("candidature.json")) == []


def test_fiche_sans_preuve_de_presence_rejetee():
    fiche = copy.deepcopy(charger("fiche-minimale.json"))
    fiche["presence"]["preuves"] = []
    assert erreurs(fiche)


def test_fiche_sans_famille_rejetee():
    fiche = copy.deepcopy(charger("fiche-minimale.json"))
    del fiche["familles"]["reproduction"]
    assert erreurs(fiche)


def test_etat_inconnu_rejete():
    fiche = copy.deepcopy(charger("fiche-minimale.json"))
    fiche["familles"]["habitats"]["recherche"] = "a_valider_par_un_humain"
    assert erreurs(fiche)


def test_affirmation_sans_origine_rejetee():
    fiche = copy.deepcopy(charger("fiche-minimale.json"))
    del fiche["identite"]["preuves"][0]["origine"]
    assert erreurs(fiche)
