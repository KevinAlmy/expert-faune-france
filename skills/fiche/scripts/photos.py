#!/usr/bin/env python3
"""Cherche des photos sous licence libre pour une espèce, avec leur crédit.

Usage :
  python3 photos.py --nom "Rana temporaria" [--profil profil-projet.json]
                    [--max 3] [--telecharger <dossier temporaire> --prefixe photo]

But : deux belles photos par espèce, une en paysage et une en portrait.
Sources, classées par qualité :
  1. Wikimedia Commons, catégorie de l'espèce (reliée à son élément Wikidata,
     vérifié par le nom scientifique P225) : Featured pictures, Valued images,
     Quality images (photos primées par des jurys), puis image Wikidata ;
  2. iNaturalist : observations de « qualité recherche » (espèce validée par la
     communauté), classées par nombre de favoris.
Le script propose jusqu'à --max candidates par orientation ; la plus belle de
chaque orientation est choisie en regardant les images (étape du skill).

Chaque photo porte sa licence, son auteur et un texte de crédit prêt à afficher.
La décision (retenue ou refusée, et pourquoi) applique `decider.decider_photos`.
Les coordonnées de prise de vue ne sont jamais conservées.

Sortie : JSON sur la sortie standard. Bibliothèque standard seule.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from decider import decider_photos  # noqa: E402

AGENT = "expert-faune-france/0.1 (https://github.com/KevinAlmy/expert-faune-france)"
PAUSE = 1.0  # secondes entre deux requêtes vers un même service

LIBELLES = {
    "cc0": ("CC0 (domaine public volontaire)", "https://creativecommons.org/publicdomain/zero/1.0/"),
    "pd": ("Domaine public", None),
    "cc-by": ("CC BY", "https://creativecommons.org/licenses/by/{v}/"),
    "cc-by-sa": ("CC BY-SA", "https://creativecommons.org/licenses/by-sa/{v}/"),
    "cc-by-nc": ("CC BY-NC", "https://creativecommons.org/licenses/by-nc/{v}/"),
    "cc-by-nc-sa": ("CC BY-NC-SA", "https://creativecommons.org/licenses/by-nc-sa/{v}/"),
    "cc-by-nd": ("CC BY-ND", "https://creativecommons.org/licenses/by-nd/{v}/"),
    "cc-by-nc-nd": ("CC BY-NC-ND", "https://creativecommons.org/licenses/by-nc-nd/{v}/"),
}


def lire(url: str, json_attendu: bool = True):
    requete = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(requete, timeout=30) as reponse:
        corps = reponse.read().decode("utf-8", errors="replace")
    time.sleep(PAUSE)
    return json.loads(corps) if json_attendu else corps


# ---------------------------------------------------------------- licences

def normaliser_licence(texte: str) -> tuple[str, str]:
    """« CC BY-SA 4.0 », « cc-by-sa-4.0 », « CC-zero », « PD-self » → (code, version)."""
    t = (texte or "").strip().lower().replace("_", "-").replace(" ", "-")
    if not t:
        return "inconnue", ""
    if t in {"cc0", "cc-zero", "cc0-1.0", "cc-0"} or t.startswith(("cc-zero", "cc0")):
        return "cc0", "1.0"
    if t.startswith(("pd", "public-domain", "domaine-public")):
        return "pd", ""
    m = re.match(r"(?:cc-)?(by(?:-nc)?(?:-sa|-nd)?)(?:-(\d(?:\.\d)?))?", t.removeprefix("cc-"))
    if m and t.startswith(("cc-by", "by")):
        return "cc-" + m.group(1), m.group(2) or ""
    if "gfdl" in t:
        return "gfdl", ""
    if t in {"arr", "all-rights-reserved", "copyright"}:
        return "arr", ""
    return "inconnue", ""


def meilleure_licence(modeles: list[str]) -> tuple[str, str]:
    """Une image sous plusieurs licences au choix : on retient la plus permissive."""
    ordre = ["cc0", "pd", "cc-by", "cc-by-sa", "cc-by-nc", "cc-by-nc-sa", "cc-by-nd", "cc-by-nc-nd", "gfdl", "arr", "inconnue"]
    trouvees = [normaliser_licence(m) for m in modeles]
    trouvees = [t for t in trouvees if t[0] != "inconnue"] or [("inconnue", "")]
    return min(trouvees, key=lambda t: ordre.index(t[0]))


def nettoyer_auteur(texte: str) -> str:
    """Retire le balisage wiki ou HTML d'un nom d'auteur."""
    t = re.sub(r"<[^>]+>", "", html.unescape(texte or ""))
    m = re.match(r"No machine-readable author provided\.\s*(.+?)\s+assumed", t)
    if m:  # texte automatique de Commons : l'auteur présumé est le déposant
        t = m.group(1)
    t = t.replace("'''", "").replace("''", "")
    t = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", t)  # [[User:X|Nom]] → Nom
    t = re.sub(r"\[https?://\S+\s+([^\]]+)\]", r"\1", t)  # [url Nom] → Nom
    t = re.sub(r"\{\{[^}]*\}\}", "", t)
    return re.sub(r"\s+", " ", t).strip(" .;,")


def licence_depuis_wikitexte(wikitexte: str) -> tuple[tuple[str, str], str]:
    """Licence et auteur d'une page de fichier Commons, lus dans son texte source."""
    modeles = re.findall(r"\{\{\s*([^|}]+)", wikitexte)
    candidats = []
    for m in modeles:
        nom = m.strip()
        if nom.lower() == "self":
            continue
        candidats.append(nom)
    for bloc in re.findall(r"\{\{\s*self\s*\|([^}]*)\}\}", wikitexte, flags=re.I):
        candidats += [x.strip() for x in bloc.split("|") if "=" not in x]
    licence = meilleure_licence([c for c in candidats if re.match(r"(?i)(cc|pd|gfdl|public)", c)])
    auteur = ""
    m = re.search(r"\|\s*(?:author|auteur)\s*=\s*(.+)", wikitexte, flags=re.I)
    if m:
        auteur = nettoyer_auteur(m.group(1))
    return licence, auteur


# ---------------------------------------------------------------- Wikimedia Commons

def element_wikidata(nom: str) -> tuple[str, dict] | None:
    """Élément Wikidata de l'espèce, trouvé par sa page Wikispecies, vérifié par P225."""
    titre = urllib.parse.quote(nom.replace(" ", "_"))
    try:
        donnees = lire(f"https://www.wikidata.org/wiki/Special:EntityData/Special:ItemByTitle/specieswiki/{titre}.json")
    except (urllib.error.URLError, json.JSONDecodeError):
        try:
            requete = urllib.request.Request(
                f"https://www.wikidata.org/wiki/Special:ItemByTitle/specieswiki/{titre}", headers={"User-Agent": AGENT}
            )
            with urllib.request.urlopen(requete, timeout=30) as r:
                qid = r.geturl().rsplit("/", 1)[-1]
            donnees = lire(f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json")
        except (urllib.error.URLError, json.JSONDecodeError, ValueError):
            return None
    for qid, entite in donnees.get("entities", {}).items():
        noms = [c["mainsnak"].get("datavalue", {}).get("value") for c in entite.get("claims", {}).get("P225", [])]
        if nom in noms:
            return qid, entite
    return None


def url_miniature_commons(fichier: str, largeur: int = 1280) -> str:
    """Adresse directe d'une miniature Commons (chemin calculé, sans redirection)."""
    nom = fichier.replace(" ", "_")
    h = hashlib.md5(nom.encode("utf-8")).hexdigest()
    nom_url = urllib.parse.quote(nom)
    return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{nom_url}/{largeur}px-{nom_url}"


def infos_commons(fichier: str) -> dict:
    """Licence, auteur et dimensions d'un fichier Commons (API, sinon texte source)."""
    titre = urllib.parse.quote("File:" + fichier.replace(" ", "_"))
    page = f"https://commons.wikimedia.org/wiki/{titre}"
    image = url_miniature_commons(fichier)
    infos = {"url_page": page, "url_image": image}
    try:
        api = lire(
            "https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo"
            f"&iiprop=extmetadata|size&titles={titre}"
        )
        ii = next(iter(api["query"]["pages"].values()))["imageinfo"][0]
        meta = ii.get("extmetadata", {})
        code, version = normaliser_licence(meta.get("LicenseShortName", {}).get("value", ""))
        infos.update(
            licence=code, version=version, auteur=nettoyer_auteur(meta.get("Artist", {}).get("value", "")),
            largeur=ii.get("width"), hauteur=ii.get("height"), lecture="API Commons",
        )
        return infos
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, StopIteration):
        pass
    try:
        texte = lire(f"https://commons.wikimedia.org/w/index.php?title={titre}&action=raw", json_attendu=False)
    except urllib.error.URLError as erreur:
        infos.update(licence="inconnue", version="", auteur="", lecture=f"page illisible : {erreur}")
        return infos
    (code, version), auteur = licence_depuis_wikitexte(texte)
    infos.update(licence=code, version=version, auteur=auteur, lecture="texte source de la page (API limitée)")
    return infos


def recherche_commons(requete: str, limite: int = 8) -> list[str]:
    """Fichiers Commons trouvés par le moteur de recherche (page de recherche, pas l'API)."""
    url = (
        "https://commons.wikimedia.org/w/index.php?ns6=1&fulltext=1&limit=20&search="
        + urllib.parse.quote(requete)
    )
    try:
        page = lire(url, json_attendu=False)
    except urllib.error.URLError:
        return []
    vus: list[str] = []
    for titre in re.findall(r'title="File:([^"]+)"', page):
        titre = html.unescape(titre)
        if titre not in vus and titre.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff")):
            vus.append(titre)
    return vus[:limite]


LABELS_COMMONS = [
    ("Assessments", 4.0, "Featured picture de Commons (sélection des meilleures photos)"),
    ("VI", 3.5, "Valued image de Commons (meilleure illustration de l'espèce)"),
    ("QualityImage", 3.0, "Quality image de Commons (qualité technique validée)"),
]


def photos_commons(nom: str) -> list[dict]:
    trouve = element_wikidata(nom)
    if not trouve:
        return []
    qid, entite = trouve
    revendications = entite.get("claims", {})
    categorie = next(
        (c["mainsnak"]["datavalue"]["value"] for c in revendications.get("P373", []) if c["mainsnak"].get("datavalue")),
        nom,
    )
    candidats: dict[str, tuple[float, str]] = {}
    for modele, rang, label in LABELS_COMMONS:
        for fichier in recherche_commons(f'incategory:"{categorie.replace(" ", "_")}" hastemplate:"{modele}"', 6):
            candidats.setdefault(fichier, (rang, label))
    for c in revendications.get("P18", []):
        fichier = c["mainsnak"].get("datavalue", {}).get("value")
        if fichier:
            candidats.setdefault(fichier, (2.0, "image principale de l'élément Wikidata"))
    photos = []
    for fichier, (rang, label) in list(candidats.items())[:12]:
        infos = infos_commons(fichier)
        if not infos.get("largeur"):
            infos.update(dimensions_distantes(infos["url_image"]) or {})
        photos.append({
            "id": f"commons:{fichier}",
            "source": "Wikimedia Commons",
            "titre": fichier,
            **infos,
            "rang_qualite": rang,
            "qualite": label,
            "identite_verifiee": True,
            "verification": f"fichier de la catégorie Commons « {categorie} », reliée à l'élément Wikidata {qid} "
            f"dont le nom scientifique (P225) est « {nom} »",
        })
    return photos


def dimensions_jpeg(donnees: bytes) -> tuple[int, int] | None:
    """Largeur et hauteur lues dans l'en-tête d'un JPEG (segment SOF)."""
    i = 2
    while i + 9 < len(donnees):
        if donnees[i] != 0xFF:
            i += 1
            continue
        marqueur = donnees[i + 1]
        longueur = int.from_bytes(donnees[i + 2 : i + 4], "big")
        if marqueur in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            hauteur = int.from_bytes(donnees[i + 5 : i + 7], "big")
            largeur = int.from_bytes(donnees[i + 7 : i + 9], "big")
            return largeur, hauteur
        i += 2 + longueur
    return None


def dimensions_distantes(url: str) -> dict | None:
    """Dimensions d'une image en ne lisant que le début du fichier."""
    requete = urllib.request.Request(url, headers={"User-Agent": AGENT, "Range": "bytes=0-131071"})
    try:
        with urllib.request.urlopen(requete, timeout=30) as r:
            dims = dimensions_jpeg(r.read())
    except (urllib.error.URLError, OSError):
        return None
    time.sleep(PAUSE / 2)
    return {"largeur_miniature": dims[0], "hauteur_miniature": dims[1]} if dims else None


# ---------------------------------------------------------------- iNaturalist

def auteur_inaturalist(photo: dict, observation: dict) -> str:
    """Nom à créditer : celui de l'attribution, sinon celui de l'observateur
    (une photo CC0 porte seulement « no rights reserved »)."""
    texte = re.sub(r"^\(c\)\s*|,?\s*(some|no|all) rights reserved.*$", "", photo.get("attribution") or "", flags=re.I)
    nom = nettoyer_auteur(photo.get("attribution_name") or texte)
    if not nom:
        utilisateur = observation.get("user") or {}
        nom = utilisateur.get("name") or utilisateur.get("login") or ""
    return nom


def photos_inaturalist(nom: str, profil: dict | None = None) -> list[dict]:
    """Photos des observations de « qualité recherche » (espèce validée par la communauté),
    classées par nombre de favoris, sous licence réutilisable."""
    licences = ["cc0", "cc-by", "cc-by-sa"]
    if profil and profil.get("usage_commercial") is False:
        licences += ["cc-by-nc", "cc-by-nc-sa"]
    try:
        recherche = lire(
            "https://api.inaturalist.org/v1/observations?quality_grade=research&order_by=votes&per_page=15"
            f"&photo_license={','.join(licences)}&taxon_name=" + urllib.parse.quote(nom)
        )
    except (urllib.error.URLError, json.JSONDecodeError):
        return []
    photos = []
    for obs in recherche.get("results", []):
        taxon = obs.get("taxon") or {}
        if taxon.get("name") != nom or taxon.get("rank") != "species" or not obs.get("photos"):
            continue
        p = obs["photos"][0]
        if (p.get("license_code") or "") not in licences:
            continue
        code, version = normaliser_licence(p.get("license_code"))
        dims = p.get("original_dimensions") or {}
        favoris = obs.get("faves_count") or 0
        photos.append({
            "id": f"inaturalist:{p.get('id')}",
            "source": "iNaturalist",
            "titre": f"Photo iNaturalist {p.get('id')}",
            "url_page": f"https://www.inaturalist.org/photos/{p.get('id')}",
            "url_image": (p.get("url") or "").replace("/square.", "/large."),
            "licence": code,
            "version": version or "4.0",
            "auteur": auteur_inaturalist(p, obs),
            "largeur": dims.get("width"),
            "hauteur": dims.get("height"),
            "lecture": "API iNaturalist",
            "rang_qualite": 1.0 + min(favoris, 20) / 5,
            "qualite": f"observation iNaturalist classée par votes ({favoris} favoris)",
            "identite_verifiee": True,
            "verification": f"observation iNaturalist {obs.get('id')} de qualité recherche : espèce « {nom} » validée par la communauté",
        })
    return photos


# ---------------------------------------------------------------- assemblage

def orientation(photo: dict) -> str:
    l = photo.get("largeur") or photo.get("largeur_miniature") or 0
    h = photo.get("hauteur") or photo.get("hauteur_miniature") or 0
    if not l or not h:
        return "inconnue"
    rapport = l / h
    return "paysage" if rapport >= 1.2 else "portrait" if rapport <= 0.9 else "carre"


def score(photo: dict) -> float:
    cote = max(photo.get("largeur") or 0, photo.get("hauteur") or 0, photo.get("largeur_miniature") or 0)
    return photo.get("rang_qualite", 1.0) + min(cote, 4000) / 4000


def credit(photo: dict) -> tuple[str, str, str | None]:
    libelle, url = LIBELLES.get(photo["licence"], (photo["licence"], None))
    version = photo.get("version") or ""
    if url and "{v}" in url:
        url = url.format(v=version or "4.0")
        libelle = f"{libelle} {version}".strip()
    auteur = photo.get("auteur") or "auteur inconnu"
    texte = f"Photo : {auteur}, {libelle}, via {photo['source']}"
    return libelle, url, texte


def fiche_photo(photo: dict) -> dict:
    libelle, url_licence, texte = credit(photo)
    return {
        "source": photo["source"],
        "url_page": photo["url_page"],
        "url_image": photo["url_image"],
        "titre": photo["titre"],
        "auteur": photo.get("auteur") or None,
        "licence": photo["licence"],
        "licence_libelle": libelle,
        "licence_url": url_licence,
        "largeur": photo.get("largeur") or photo.get("largeur_miniature"),
        "hauteur": photo.get("hauteur") or photo.get("hauteur_miniature"),
        "orientation_origine": orientation(photo),
        "statut": "proposee",
        "qualite": photo.get("qualite"),
        "credit": texte,
        "verification": photo["verification"],
        "consulte_le": dt.date.today().isoformat(),
        **({"restriction": "usage non commercial seulement"} if photo["licence"] in {"cc-by-nc", "cc-by-nc-sa"} else {}),
    }


def chercher(nom: str, profil: dict | None = None, par_orientation: int = 3) -> dict:
    """Candidates classées par qualité, puis réparties en paysage et portrait.
    Le choix final (la plus belle de chaque orientation) se fait en regardant les images."""
    candidates = sorted(photos_commons(nom) + photos_inaturalist(nom, profil), key=score, reverse=True)
    for c in candidates:
        c["orientation"] = orientation(c)
    decision = decider_photos(candidates, profil)
    par_id = {c["id"]: c for c in candidates}
    resultat: dict = {"nom": nom, "paysage": [], "portrait": [], "carre": []}
    for ident in decision["admises"]:
        c = par_id[ident]
        groupe = resultat.get(c["orientation"])
        if groupe is not None and len(groupe) < par_orientation:
            groupe.append(fiche_photo(c))
    resultat["refusees"] = decision["refusees"]
    resultat["sources_interrogees"] = [
        "Wikimedia Commons (Featured, Valued et Quality images de la catégorie de l'espèce ; image Wikidata)",
        "iNaturalist (observations de qualité recherche classées par votes)",
    ]
    return resultat


def telecharger(photos: list[dict], dossier: Path, prefixe: str) -> None:
    dossier.mkdir(parents=True, exist_ok=True)
    for i, photo in enumerate(photos, 1):
        chemin = dossier / f"{prefixe}-{photo['orientation_origine']}-{i}.jpg"
        requete = urllib.request.Request(photo["url_image"], headers={"User-Agent": AGENT})
        for essai in range(3):
            try:
                with urllib.request.urlopen(requete, timeout=60) as r:
                    chemin.write_bytes(r.read())
                photo["fichier_local"] = str(chemin)
                photo.pop("telechargement", None)
                break
            except urllib.error.HTTPError as erreur:
                photo["telechargement"] = f"échec : HTTP {erreur.code}"
                if erreur.code != 429:
                    break
                time.sleep(10 * (essai + 1))  # serveur saturé ou trop sollicité : on ralentit
            except (urllib.error.URLError, OSError) as erreur:
                photo["telechargement"] = f"échec : {erreur}"
                break
        time.sleep(PAUSE * 3)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--nom", required=True, help="nom scientifique retenu")
    parser.add_argument("--profil", type=Path)
    parser.add_argument("--max", type=int, default=3, help="candidates par orientation")
    parser.add_argument("--telecharger", type=Path)
    parser.add_argument("--prefixe", default="photo")
    args = parser.parse_args(argv)
    profil = json.loads(args.profil.read_text(encoding="utf-8")) if args.profil and args.profil.exists() else None
    resultat = chercher(args.nom, profil, args.max)
    if args.telecharger:
        telecharger(resultat["paysage"] + resultat["portrait"] + resultat["carre"], args.telecharger, args.prefixe)
    json.dump(resultat, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
