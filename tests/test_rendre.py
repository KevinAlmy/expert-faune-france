"""La page HTML montre la fiche sans rien exécuter de ce que contiennent les sources."""

import json
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "skills" / "fiche" / "scripts"))

from rendre import rendre  # noqa: E402

EXEMPLES = RACINE / "tests" / "exemples"


def test_fiche_et_candidature_se_rendent():
    for nom in ("fiche-minimale.json", "candidature.json"):
        html = rendre(json.loads((EXEMPLES / nom).read_text(encoding="utf-8")))
        assert html.startswith("<!doctype html>") and "</body></html>" in html


def test_valeur_venue_d_une_source_est_echappee():
    fiche = json.loads((EXEMPLES / "fiche-minimale.json").read_text(encoding="utf-8"))
    fiche["identite"]["nom_retenu"] = "<script>alert(1)</script>"
    html = rendre(fiche)
    assert "<script>alert" not in html and "&lt;script&gt;" in html


def test_lien_non_web_n_est_pas_un_lien():
    fiche = json.loads((EXEMPLES / "fiche-minimale.json").read_text(encoding="utf-8"))
    fiche["execution"]["sources_consultees"] = [{"source": "x", "url": "javascript:alert(1)"}]
    assert 'href="javascript' not in rendre(fiche)
