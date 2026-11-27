#!/usr/bin/env python3
"""Transforme une fiche ou une candidature JSON en page HTML lisible, autonome.

Usage : python3 rendre.py fiches/EFF-000001.json [-o EFF-000001.html]
Sans -o, la page est écrite à côté du JSON (même nom, extension .html).

Bibliothèque standard seule. Toute valeur lue est échappée : la page n'exécute
aucun contenu venu des sources. Elle n'ajoute rien à la fiche : elle la montre.
"""

from __future__ import annotations

import argparse
import json
import sys
from html import escape
from pathlib import Path

FAMILLES = {
    "reconnaissance": "Reconnaissance",
    "repartition": "Présence et répartition",
    "habitats": "Habitats",
    "alimentation": "Alimentation",
    "reproduction": "Reproduction",
    "developpement": "Développement et longévité",
    "comportements": "Comportements",
    "activite": "Activité et cycle annuel",
    "interactions": "Interactions écologiques",
    "conservation": "Conservation",
    "observation_respectueuse": "Observation respectueuse",
}
ETATS_CHAMP = {
    "documente": "Documenté",
    "corrobore": "Corroboré",
    "incertain": "Incertain",
    "contradictoire": "Contradictoire",
    "non_renseigne": "Non renseigné",
}
ETATS_RECHERCHE = {
    "non_recherche": "Non recherchée",
    "recherche_effectuee": "Recherche effectuée",
    "recherche_partielle": "Recherche partielle",
    "recherche_sans_resultat": "Sans résultat",
    "acces_indisponible": "Accès indisponible",
    "non_applicable": "Sans objet",
}
ETATS_ENTREE = {
    "fiche_complete": "Fiche complète",
    "fiche_partielle": "Fiche partielle",
    "fiche_minimale": "Fiche minimale",
    "candidate": "Candidature",
}

CSS = """
/* VOICE everyday: a naturalist's field plate, calm and exact
   IDEA a museum specimen label + field-guide plate, one row per family
   PICTURE coverage plate: one square per field, coloured by its state
   COLOUR white ground, pond-green #17614a field, ochre #c98a12 for gaps, rust for contradictions
   TYPE Archivo (display and text), italic only for the scientific name
   LAYOUT green band with name and key statuses; plate full width; families in two columns from 900px */
:root{color-scheme:light dark;--bg:light-dark(#ffffff,#0e1512);--ink:light-dark(#13201a,#e6efe9);--mute:light-dark(#4f5f57,#a3b5ab);--band:light-dark(#17614a,#123d31);--bandink:#f4fbf7;--doc:light-dark(#17614a,#4fbf92);--cor:light-dark(#0b3d2e,#9be3c3);--inc:light-dark(#c98a12,#e8b74a);--con:light-dark(#b23a1e,#f07a5a);--line:light-dark(#d5e0da,#2a3a32);--soft:light-dark(#eef5f1,#16211c)}
:root[data-theme=light]{color-scheme:light}:root[data-theme=dark]{color-scheme:dark}
*{box-sizing:border-box;min-width:0}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 Archivo,system-ui,sans-serif;overflow-x:clip}
a{color:inherit;text-underline-offset:2px}
.band{padding-block:clamp(24px,4vw,56px);padding-left:max(5vw,16px,env(safe-area-inset-left,0px));padding-right:max(5vw,16px,env(safe-area-inset-right,0px))}
.wrap{max-width:1240px;margin:0 auto}
.head{background:var(--band);color:var(--bandink);margin-top:calc(-1*env(safe-area-inset-top,0px));padding-top:calc(env(safe-area-inset-top,0px) + clamp(24px,4vw,56px))}
.head .wrap{display:grid;gap:24px}
@media(min-width:900px){.head .wrap{grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);align-items:end}}
h1{font-size:clamp(34px,5vw,52px);line-height:1.05;letter-spacing:-.02em;margin:0;font-style:italic;font-weight:700}
.auteur{white-space:nowrap;font-style:normal;font-weight:400;font-size:.5em;letter-spacing:0}
.vern{font-size:20px;margin:8px 0 0}
.classif{color:color-mix(in srgb,var(--bandink) 78%,transparent);margin:12px 0 0;font-size:15px}
.etiquette{border:1px solid color-mix(in srgb,var(--bandink) 40%,transparent);padding:16px 18px;display:grid;gap:10px;font-size:15px}
.etiquette div{display:flex;justify-content:space-between;gap:16px;border-bottom:1px solid color-mix(in srgb,var(--bandink) 20%,transparent);padding-bottom:8px}
.etiquette div:last-child{border:0;padding:0}
.etiquette b{font-weight:600;text-align:right}
h2{font-size:28px;line-height:1.1;letter-spacing:-.01em;margin:0 0 6px}
.lead{color:var(--mute);margin:0 0 20px;max-width:70ch}
.chiffres{display:grid;grid-template-columns:repeat(auto-fit,minmax(9em,1fr));gap:12px;margin-bottom:24px}
.chiffres div{border-top:3px solid var(--doc);padding-top:8px}
.chiffres strong{display:block;font-size:34px;line-height:1.1;font-variant-numeric:tabular-nums}
.chiffres span{color:var(--mute);font-size:14px}
.planche{display:grid;gap:2px;border-top:1px solid var(--line)}
.ligne{display:grid;grid-template-columns:minmax(0,15em) minmax(0,1fr) auto;gap:12px;align-items:center;padding:10px 0;border-bottom:1px solid var(--line)}
.ligne a{text-decoration:none;font-weight:600}
.cases{display:flex;flex-wrap:wrap;gap:4px}
.c{width:22px;height:22px;border:2px solid var(--doc)}
.c.documente{background:var(--doc)}
.c.corrobore{background:var(--cor);border-color:var(--cor)}
.c.incertain{border-color:var(--inc);background:repeating-linear-gradient(45deg,var(--inc) 0 3px,transparent 3px 7px)}
.c.contradictoire{background:var(--con);border-color:var(--con)}
.c.complement{background:var(--soft);border-color:var(--doc);box-shadow:inset 0 0 0 3px var(--bg),inset 0 0 0 11px var(--doc)}
.c.incertain.complement{box-shadow:none;border-color:var(--inc);background:repeating-linear-gradient(45deg,var(--inc) 0 3px,transparent 3px 7px)}
.c.non_renseigne{border-color:var(--inc);border-style:dashed;background:transparent}
.rech{font-size:14px;color:var(--mute);white-space:nowrap}
.legende{display:flex;flex-wrap:wrap;gap:8px 20px;margin-top:14px;font-size:14px;color:var(--mute)}
.legende span{display:inline-flex;align-items:center;gap:8px}
.legende .c{width:16px;height:16px}
@media(max-width:600px){.ligne{grid-template-columns:minmax(0,1fr) auto}.cases{grid-column:1/-1;order:3}}
.familles{display:grid;gap:20px}
@media(min-width:900px){.familles{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.fam{background:var(--soft);padding:20px;scroll-margin-top:16px}
.fam h3{font-size:21px;margin:0 0 4px}
.fam .just{color:var(--mute);font-size:14px;margin:0 0 12px}
.champ{border-top:1px solid var(--line);padding:10px 0}
.champ h4{margin:0;font-size:16px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.pastille{font-size:13px;font-weight:600;padding:1px 8px;border:1px solid currentColor;white-space:nowrap}
.p-documente,.p-corrobore{color:var(--doc)}
.p-incertain,.p-non_renseigne{color:var(--inc)}
.p-contradictoire{color:var(--con)}
.p-complement{color:var(--mute);border-style:dashed}
.champ ul{margin:6px 0 0;padding-left:20px}
.champ details{margin-top:6px;font-size:14px;color:var(--mute)}
.champ summary{cursor:pointer}
.aff{margin:8px 0 0;padding-left:12px;border-left:2px solid var(--line);overflow-wrap:anywhere}
.piste{font-size:14px;margin:10px 0 0}
.cols{display:grid;gap:28px}
@media(min-width:900px){.cols{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.cols ol,.cols ul{padding-left:20px;margin:0}
.cols li{margin-bottom:8px;overflow-wrap:anywhere}
.sm{font-size:14px;color:var(--mute)}
footer{border-top:1px solid var(--line);color:var(--mute);font-size:14px}
"""


def e(valeur) -> str:
    return escape("" if valeur is None else str(valeur), quote=True)


def lien(texte, url) -> str:
    if url and str(url).startswith(("https://", "http://")):
        return f'<a href="{e(url)}">{e(texte)}</a>'
    return e(texte)


MOTS = {
    "presence_sauvage_metropole": "Présence sauvage en métropole",
    "code_non_documente": "Code TAXREF non documenté",
    "etablie": "Établie", "indigene": "Indigène", "introduite": "Introduite", "indeterminee": "Indéterminée"}


def libelle(cle: str) -> str:
    return MOTS.get(cle, cle.replace("_", " ").capitalize())


def liste_valeurs(valeur) -> str:
    if valeur is None:
        return ""
    if isinstance(valeur, list):
        return "<ul>" + "".join(f"<li>{e(v)}</li>" for v in valeur) + "</ul>"
    if isinstance(valeur, dict):
        return "<ul>" + "".join(f"<li>{e(libelle(k))} : {e(v)}</li>" for k, v in valeur.items()) + "</ul>"
    return f"<ul><li>{e(valeur)}</li></ul>"


def affirmation(a: dict) -> str:
    contexte = " · ".join(e(a[k]) for k in ("territoire", "contexte", "stade_ou_saison", "population") if a.get(k))
    licence = a.get("reutilisation", {}).get("licence", "")
    return (
        f'<div class="aff"><div>{e(a.get("valeur"))}{(" " + e(a["unite"])) if a.get("unite") else ""}</div>'
        f'<div>Source : {lien(a.get("source"), a.get("url"))} ({e(a.get("date_ou_version"))})</div>'
        f'<div>Origine : {e(a.get("origine"))}{(" · " + contexte) if contexte else ""}</div>'
        f'<div>Licence : {e(licence)} · consulté le {e(a.get("consulte_le"))}</div>'
        f'{("<div>Diffusion : " + e(a["restriction_diffusion"]) + "</div>") if a.get("restriction_diffusion") else ""}</div>'
    )


def champ(nom: str, c: dict) -> str:
    etat = c.get("etat", "non_renseigne")
    affs = c.get("affirmations") or []
    complement = '<span class="pastille p-complement">Complément</span>' if c.get("niveau") == "complement" else ""
    ecartes = "".join(
        f'<div class="aff">Écarté : {e(x.get("valeur"))} ({e(x.get("source"))}) : {e(x.get("motif"))}</div>' for x in c.get("ecartes", [])
    )
    preuves = (
        f"<details><summary>{len(affs)} source{'s' if len(affs) > 1 else ''}</summary>"
        + "".join(affirmation(a) for a in affs)
        + ecartes
        + "</details>"
        if affs
        else ""
    )
    return (
        f'<div class="champ"><h4>{e(libelle(nom))}<span>{complement} <span class="pastille p-{e(etat)}">{e(ETATS_CHAMP.get(etat, etat))}</span></span></h4>'
        f"{liste_valeurs(c.get('valeur_synthese'))}{preuves}</div>"
    )


def page(titre: str, corps: str) -> str:
    return (
        '<!doctype html><html lang="fr"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="claude:viewport-fit-sides" content="cover">'
        f"<title>{e(titre)}</title>"
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,400;0,600;0,700;1,700&display=swap" rel="stylesheet">'
        f"<style>{CSS}</style></head><body>{corps}</body></html>"
    )


def pied(doc: dict) -> str:
    ex = doc.get("execution", {})
    return (
        f'<footer class="band"><div class="wrap">Fiche {e(doc.get("id"))} · produite le {e(ex.get("date"))} '
        f'par {e(ex.get("version_skill", "Expert faune de France"))} · requête « {e(ex.get("requete"))} ». '
        "Cette page montre le JSON tel quel : chaque valeur garde sa source, sa licence et son état.</div></footer>"
    )


def sources(doc: dict) -> str:
    ex = doc.get("execution", {})
    lues = "".join(
        f"<li>{lien(s.get('source'), s.get('url'))} <span class=sm>({e(s.get('version'))})</span></li>"
        if isinstance(s, dict) else f"<li>{e(s)}</li>"
        for s in ex.get("sources_consultees", [])
    )
    ko = "".join(
        f"<li>{e(s.get('source'))} <span class=sm>: {e(s.get('motif'))}</span></li>"
        for s in ex.get("indisponibilites", [])
    )
    return (
        '<section class="band" id="sources"><div class="wrap cols">'
        f"<div><h2>Sources lues</h2><ol>{lues or '<li>Aucune</li>'}</ol></div>"
        f"<div><h2>Sources non lues</h2><p class=lead>Déclarées telles quelles : rien n'y est attribué.</p><ul>{ko or '<li>Aucune</li>'}</ul></div>"
        "</div></section>"
    )


def rendre_fiche(d: dict) -> str:
    ident, pres = d["identite"], d["presence"]
    classif = ident.get("classification", {})
    chemin = " › ".join(e(classif[k]) for k in ("classe", "ordre", "famille") if classif.get(k))
    code = pres.get("code_source", {})
    conservation = d["familles"].get("conservation", {}).get("champs", {})
    lr_affs = conservation.get("liste_rouge_nationale", {}).get("affirmations") or [{}]
    lr_court = str(lr_affs[0].get("valeur") or "non renseignée").split(",")[0]
    if lr_affs[0].get("contexte"):
        lr_court += f" · {lr_affs[0]['contexte']}"
    prot = conservation.get("protection_nationale", {}).get("etat", "non_renseigne")

    lignes, total, docs, lacunes, compl = [], 0, 0, 0, 0
    for cle, nom in FAMILLES.items():
        fam = d["familles"].get(cle, {"recherche": "non_recherche", "champs": {}})
        cases = "".join(
            f'<span class="c {e(c.get("etat"))}{" complement" if c.get("niveau") == "complement" else ""}" title="{e(libelle(n))} : {e(ETATS_CHAMP.get(c.get("etat"), c.get("etat")))}"></span>'
            for n, c in fam["champs"].items()
        ) or '<span class="sm">aucun champ</span>'
        for c in fam["champs"].values():
            total += 1
            docs += c.get("etat") in ("documente", "corrobore")
            lacunes += c.get("etat") == "non_renseigne"
            compl += c.get("niveau") == "complement" and c.get("etat") in ("documente", "corrobore")
        lignes.append(
            f'<div class="ligne"><a href="#{e(cle)}">{e(nom)}</a><div class="cases">{cases}</div>'
            f'<span class="rech">{e(ETATS_RECHERCHE.get(fam["recherche"], fam["recherche"]))}</span></div>'
        )

    familles = []
    for cle, nom in FAMILLES.items():
        fam = d["familles"].get(cle)
        if not fam:
            continue
        just = f'<p class="just">{e(fam["justification"])}</p>' if fam.get("justification") else ""
        piste = f'<p class="piste"><b>Prochaine piste :</b> {e(fam["prochaine_piste"])}</p>' if fam.get("prochaine_piste") else ""
        familles.append(
            f'<article class="fam" id="{e(cle)}"><h3>{e(nom)}</h3>{just}'
            + "".join(champ(n, c) for n, c in fam["champs"].items())
            + f"{piste}</article>"
        )

    couv = d.get("couverture", {})
    reprise = "".join(f"<li>{e(p)}</li>" for p in couv.get("point_de_reprise", []))
    vern = ", ".join(ident.get("noms_vernaculaires", []))
    corps = (
        '<header class="band head"><div class="wrap"><div>'
        f'<h1>{e(ident["nom_retenu"])} <span class="auteur">{e(ident.get("auteur"))}{(", " + e(ident.get("annee"))) if ident.get("annee") else ""}</span></h1>'
        f'<p class="vern">{e(vern)}</p><p class="classif">{chemin}</p></div>'
        '<div class="etiquette">'
        f'<div><span>Présence en métropole</span><b>{e(libelle(pres.get("qualification", "")))}{(" · " + e(libelle(pres["origine"]))) if pres.get("origine") else ""}</b></div>'
        f'<div><span>{e(code.get("referentiel", "TAXREF"))}, colonne {e(code.get("colonne", "FR"))}</span><b>{e(code.get("code"))} · {e(code.get("signification"))}</b></div>'
        f'<div><span>Liste rouge France</span><b>{e(lr_court)}</b></div>'
        f'<div><span>Protection nationale</span><b>{e(ETATS_CHAMP.get(prot, prot))}</b></div>'
        f'<div><span>État de la fiche</span><b>{e(ETATS_ENTREE.get(d["etat"], d["etat"]))} · {e(d["id"])}</b></div>'
        "</div></div></header>"
        '<section class="band"><div class="wrap">'
        f"<h2>{docs} champs documentés sur {total}" + (f", dont {compl} par des sources de complément" if compl else "") + "</h2>"
        f'<p class="lead">Chaque case est un champ de la fiche. Passe du {e(couv.get("date"))} '
        f'{"terminée" if couv.get("passe_terminee") else "à reprendre : les manques sont listés plus bas et seront repris à la prochaine exécution"}.</p>'
        f'<div class="chiffres"><div><strong>{docs}</strong><span>champs documentés</span></div>'
        f"<div><strong>{lacunes}</strong><span>champs encore vides</span></div>"
        f'<div><strong>{len(d.get("execution", {}).get("sources_consultees", []))}</strong><span>sources lues</span></div>'
        f'<div><strong>{len(d.get("execution", {}).get("indisponibilites", []))}</strong><span>sources inaccessibles</span></div></div>'
        f'<div class="planche">{"".join(lignes)}</div>'
        '<div class="legende">'
        + "".join(f'<span><i class="c {k}"></i>{v}</span>' for k, v in ETATS_CHAMP.items())
        + '<span><i class="c documente complement"></i>Documenté par un complément (Wikipédia…)</span>'
        + "</div></div></section>"
        f'<section class="band" style="padding-top:0"><div class="wrap familles">{"".join(familles)}</div></section>'
        + (f'<section class="band" style="padding-top:0"><div class="wrap"><h2>Reprise prévue</h2><ul>{reprise}</ul></div></section>' if reprise else "")
        + sources(d)
        + pied(d)
    )
    return page(f"{ident['nom_retenu']} · fiche", corps)


def rendre_candidature(d: dict) -> str:
    taxon = d["taxon"]
    decl = "".join(f"<li>{e(x)}</li>" for x in d.get("reexamen", {}).get("declencheurs", []))
    consultees = "".join(f"<li>{e(x)}</li>" for x in d.get("sources_consultees", []))
    corps = (
        '<header class="band head"><div class="wrap"><div>'
        f'<h1>{e(taxon["nom"])} <span class="auteur">{e(taxon.get("auteur"))}</span></h1>'
        '<p class="vern">Candidature : pas de fiche pour l\'instant</p></div>'
        '<div class="etiquette">'
        f'<div><span>Preuve manquante</span><b>{e(libelle(d["preuve_manquante"]))}</b></div>'
        f'<div><span>Identité</span><b>{e(libelle(taxon.get("identite", "non précisée")))}</b></div>'
        f'<div><span>Identifiant</span><b>{e(d["id"])}</b></div>'
        "</div></div></header>"
        f'<section class="band"><div class="wrap cols"><div><h2>Motif</h2><p>{e(d["motif"])}</p></div>'
        f"<div><h2>Réexamen automatique si</h2><ul>{decl}</ul></div></div></section>"
        f'<section class="band" style="padding-top:0"><div class="wrap"><h2>Recherches faites</h2><ul>{consultees}</ul></div></section>'
        + sources(d)
        + pied(d)
    )
    return page(f"{taxon['nom']} · candidature", corps)


def rendre(document: dict) -> str:
    return rendre_candidature(document) if document.get("etat") == "candidate" else rendre_fiche(document)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("json", type=Path)
    parser.add_argument("-o", "--sortie", type=Path)
    args = parser.parse_args(argv)
    document = json.loads(args.json.read_text(encoding="utf-8"))
    sortie = args.sortie or args.json.with_suffix(".html")
    sortie.write_text(rendre(document), encoding="utf-8")
    print(f"✔ {sortie}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
