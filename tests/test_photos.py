"""Photos : lecture des licences, crédit, orientation, dimensions (sans réseau)."""

import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "skills" / "fiche" / "scripts"))

from photos import credit, dimensions_jpeg, licence_depuis_wikitexte, normaliser_licence, orientation, url_miniature_commons  # noqa: E402

WIKITEXTE = """== {{int:filedesc}} ==
{{Information
| Description = Grenouille
| Author      = [https://www.flickr.com/people/x Frank Vassen] from Brussels
}}
=={{int:license-header}}==
{{self|cc-by-sa-4.0|GFDL}}
"""


def test_licences_normalisees():
    assert normaliser_licence("CC BY-SA 4.0") == ("cc-by-sa", "4.0")
    assert normaliser_licence("cc-by-2.0") == ("cc-by", "2.0")
    assert normaliser_licence("CC0") == ("cc0", "1.0")
    assert normaliser_licence("Public domain") == ("pd", "")
    assert normaliser_licence("cc-by-nc-nd") == ("cc-by-nc-nd", "")
    assert normaliser_licence("GFDL") == ("gfdl", "")
    assert normaliser_licence("") == ("inconnue", "")


def test_licence_et_auteur_lus_dans_le_texte_source_commons():
    (code, version), auteur = licence_depuis_wikitexte(WIKITEXTE)
    assert (code, version) == ("cc-by-sa", "4.0"), "double licence : la plus permissive réutilisable"
    assert auteur.startswith("Frank Vassen")


def test_credit_complet():
    libelle, url, texte = credit({"licence": "cc-by-sa", "version": "4.0", "auteur": "A. Martin", "source": "Wikimedia Commons"})
    assert libelle == "CC BY-SA 4.0" and url == "https://creativecommons.org/licenses/by-sa/4.0/"
    assert texte == "Photo : A. Martin, CC BY-SA 4.0, via Wikimedia Commons"


def test_orientation():
    assert orientation({"largeur": 3000, "hauteur": 2000}) == "paysage"
    assert orientation({"largeur": 1365, "hauteur": 2048}) == "portrait"
    assert orientation({"largeur": 2000, "hauteur": 1900}) == "carre"
    assert orientation({}) == "inconnue"


def test_dimensions_lues_dans_l_entete_jpeg():
    sof = b"\xff\xd8" + b"\xff\xe0\x00\x04\x00\x00" + b"\xff\xc0\x00\x11\x08" + (720).to_bytes(2, "big") + (1280).to_bytes(2, "big") + b"\x03" + b"\x00" * 9
    assert dimensions_jpeg(sof) == (1280, 720)


def test_adresse_miniature_commons():
    url = url_miniature_commons("Common frog.jpg")
    assert url.startswith("https://upload.wikimedia.org/wikipedia/commons/thumb/")
    assert url.endswith("/1280px-Common_frog.jpg")


def test_auteurs_nettoyes():
    from photos import auteur_inaturalist, nettoyer_auteur
    assert nettoyer_auteur("'''Dark'''one") == "Darkone"
    assert nettoyer_auteur("No machine-readable author provided. Esv assumed (based on copyright claims).") == "Esv"
    assert auteur_inaturalist({"attribution": "no rights reserved"}, {"user": {"login": "jdupont", "name": ""}}) == "jdupont"
    assert auteur_inaturalist({"attribution": "(c) Marie Curie, some rights reserved (CC BY)"}, {}) == "Marie Curie"
