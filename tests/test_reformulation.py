"""Reformulation obligatoire : une reprise de texte est détectée, une vraie réécriture passe."""

import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "skills" / "fiche" / "scripts"))

from reformulation import controler  # noqa: E402
from rendre import references  # noqa: E402

SOURCE = "La femelle pond de 700 à 4500 œufs en amas gélatineux, déposés sur le fond ou flottant à la surface d'eaux peu profondes."
URL = "https://fr.wikipedia.org/wiki/Exemple"


def fiche(valeur, url=URL):
    return {"familles": {"reproduction": {"champs": {"ponte": {"affirmations": [
        {"valeur": valeur, "source": "Wikipédia", "url": url, "origine": "Ouvrage A"}]}}}}}


def test_copie_detectee_meme_sans_accents_ni_majuscules():
    echecs = controler(fiche("Elle pond de 700 a 4500 OEUFS en amas gelatineux, deposes sur le fond"), SOURCE, URL)
    assert len(echecs) == 1 and "amas gelatineux" in echecs[0]["reprise"]


def test_reformulation_acceptee():
    assert controler(fiche("Ponte de 700 à 4 500 œufs réunis en une masse de gelée"), SOURCE, URL) == []


def test_seules_les_affirmations_de_la_page_sont_controlees():
    assert controler(fiche(SOURCE, url="https://autre.example"), SOURCE, URL) == []


def test_bibliographie_une_entree_par_origine():
    doc = fiche("x")
    doc["familles"]["reproduction"]["champs"]["autre"] = {"affirmations": [
        {"valeur": "y", "source": "Wikipédia EN", "url": "https://en.wikipedia.org/wiki/E", "origine": "Ouvrage A"},
        {"valeur": "z", "source": "GBIF", "url": "https://api.gbif.org", "origine": "GBIF"}]}
    refs = references(doc)
    assert [r["origine"] for r in refs] == ["Ouvrage A", "GBIF"]
    assert len(refs[0]["acces"]) == 2 and refs[1]["numero"] == 2
