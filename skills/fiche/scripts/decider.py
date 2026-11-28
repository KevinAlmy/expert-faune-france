#!/usr/bin/env python3
"""Règles de décision automatiques du skill (cadrage v0.7, sections 6, 7, 9 et 10).

Ce module est la version exécutable de reference/decisions.md. Il ne cherche
rien : il reçoit un « dossier de preuves » (JSON) déjà constitué et rend la
décision, son motif et la trace à conserver. Il n'existe aucune décision qui
attende une validation humaine : quand les preuves manquent, la décision est
une abstention motivée (candidature, champ contradictoire, rattachement
suspendu) avec réexamen automatique.

Usage : python3 decider.py dossier.json   (ou lecture sur l'entrée standard)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Section 7.5 : ce qui suffit seul pour chaque fait.
IDENTITE_SUFFISANTE = {"taxref", "description_originale", "referentiel_groupe", "catalogue_of_life"}
PRESENCE_SUFFISANTE = {
    "taxref",
    "description_originale_specimen_metropole",
    "atlas",
    "publication_localisee",
    "occurrence_verifiee",
}
# Section 7.3 : qualifications et admission.
QUALIF_ADMISES = {"etablie", "occasionnelle", "historique"}
QUALIF_CANDIDATES = {"douteuse"}
QUALIF_EXCLUES = {"captive_ou_domestique", "absente", "erreur"}


def _origines(preuves: list[dict]) -> set[str]:
    """Deux copies d'une même étude = une seule origine (section 8.3)."""
    return {p.get("origine") or p.get("source") for p in preuves}


def _faits_identite(dossier: dict) -> tuple[str, list[dict]]:
    identite = dossier.get("identite", {})
    if identite.get("ambigue"):
        return "ambigue", identite.get("hypotheses", [])
    preuves = [p for p in identite.get("preuves", []) if p.get("type") in IDENTITE_SUFFISANTE]
    return ("etablie" if preuves else "non_etablie"), preuves


def _faits_presence(dossier: dict) -> tuple[str, str | None, list[dict], str]:
    """Rend (état, qualification, preuves retenues, motif)."""
    presence = dossier.get("presence", {})
    taxref = presence.get("taxref")
    if taxref:
        decision = taxref.get("decision")
        if decision == "fiche":
            preuve = {**taxref, "type": "taxref", "origine": f"TAXREF v{taxref.get('version')}"}
            if "origine" in taxref:
                preuve["origine_biogeographique"] = taxref["origine"]
            return "etablie", taxref.get("qualification"), [preuve], (
                f"TAXREF v{taxref.get('version')} : code {taxref.get('code')} ({taxref.get('signification')})"
            )
        if decision == "exclusion":
            return "exclue", None, [], taxref.get("motif", "exclue par TAXREF")
        if decision == "candidature" and not presence.get("preuves"):
            return "non_etablie", None, [], taxref.get("motif", "présence non démontrée")

    preuves = presence.get("preuves", [])
    retenues = [p for p in preuves if p.get("type") in PRESENCE_SUFFISANTE]
    ecartees = [p for p in preuves if p.get("type") not in PRESENCE_SUFFISANTE]
    if retenues:
        qualification = presence.get("qualification", "etablie")
        if qualification in QUALIF_EXCLUES:
            return "exclue", None, [], f"présence qualifiée « {qualification} » : hors faune sauvage"
        if qualification in QUALIF_CANDIDATES:
            return "non_etablie", None, retenues, "présence douteuse"
        return "etablie", qualification, retenues, "présence sauvage en métropole étayée par " + ", ".join(
            sorted({p["type"] for p in retenues})
        )
    raisons = sorted({p.get("type", "inconnue") for p in ecartees})
    motif = "présence sauvage en métropole non démontrée"
    if raisons:
        motif += " (preuves insuffisantes seules : " + ", ".join(raisons) + ")"
    return "non_etablie", None, [], motif


def decider_admission(dossier: dict) -> dict:
    """Section 7.2 et 10 : fiche, candidature, exclusion ou enrichissement."""
    noms = dossier.get("noms", {})
    situation = noms.get("situation", "nouveau")

    if situation in ("homonymie_non_resolue", "vernaculaire_partage"):
        motif = (
            "homonymie : auteur et année ne lèvent pas l'ambiguïté"
            if situation == "homonymie_non_resolue"
            else "nom vernaculaire partagé par plusieurs espèces"
        )
        return {
            "decision": "abstention",
            "action": "aucun_rattachement",
            "motif": motif,
            "hypotheses": noms.get("hypotheses", []),
            "reexamen": True,
        }
    if situation == "synonyme_sans_ambiguite":
        return {
            "decision": "enrichir",
            "fiche_id": noms["fiche_existante"],
            "ajout_synonyme": noms.get("nom_fourni"),
            "motif": f"ancien nom rattaché sans ambiguïté par {noms.get('source', 'le référentiel')}",
        }
    if situation == "fusion":
        return decider_fusion(noms)
    if situation == "scission":
        return decider_scission(dossier)

    identite, preuves_id = _faits_identite(dossier)
    if identite == "ambigue":
        return {
            "decision": "candidature",
            "motif": "identité ambiguë",
            "hypotheses": preuves_id,
            "reexamen": True,
        }
    if identite == "non_etablie":
        return {"decision": "candidature", "motif": "identité non établie", "reexamen": True}

    presence, qualification, preuves_pr, motif = _faits_presence(dossier)
    if presence == "exclue":
        return {"decision": "exclusion", "motif": motif}
    if presence == "non_etablie":
        return {
            "decision": "candidature",
            "motif": motif,
            "preuve_manquante": "presence_sauvage_metropole",
            "reexamen": True,
        }
    voie = "taxref" if any(p.get("type") == "taxref" for p in preuves_pr) else "hors_taxref"
    resultat = {
        "decision": "creer_fiche",
        "voie": voie,
        "qualification": qualification,
        "motif": motif,
        "preuves": {"identite": sorted(_origines(preuves_id)), "presence": sorted(_origines(preuves_pr))},
    }
    if voie == "hors_taxref":
        resultat["rapprochement_taxref_prevu"] = True
    return resultat


def decider_scission(dossier: dict) -> dict:
    """Section 6.3 : admission évaluée séparément pour chaque taxon résultant."""
    scission = dossier["noms"]["scission"]
    resultants = []
    for taxon in scission["resultants"]:
        decision = decider_admission({"identite": taxon.get("identite", {}), "presence": taxon.get("presence", {})})
        resultants.append({"taxon": taxon["taxon"], **decision})
    donnees = []
    for donnee in scission.get("donnees_historiques", []):
        if donnee.get("departageable") and donnee.get("vers"):
            donnees.append({"id": donnee["id"], "attribution": donnee["vers"], "motif": donnee.get("critere", "départageable")})
        else:
            donnees.append({
                "id": donnee["id"],
                "attribution": scission["concept_historique"],
                "motif": "impossible à départager : attribution historique conservée",
            })
    return {
        "decision": "scission",
        "concept_historique": {
            "fiche_id": scission["concept_historique"],
            "etat": "concept_historique",
            "relie_a": [t["taxon"] for t in scission["resultants"]],
        },
        "resultants": resultants,
        "donnees_historiques": donnees,
        "motif": f"scission selon {scission.get('referentiel', 'le référentiel')}",
    }


def decider_fusion(noms: dict) -> dict:
    fusion = noms["fusion"]
    return {
        "decision": "fusion",
        "fiche_conservee": fusion["retenue"],
        "renvois": [{"fiche_id": f, "etat": "renvoi", "vers": fusion["retenue"]} for f in fusion["fusionnees"]],
        "motif": f"fusion selon {fusion.get('referentiel', 'le référentiel')} ; aucun identifiant supprimé",
    }


def decider_champ(champ: dict, profil: dict | None = None) -> dict:
    """Sections 9.4, 12.3, 13 : état d'un champ à partir de ses affirmations."""
    profil = profil or {}
    affirmations = champ.get("affirmations", [])

    if champ.get("source_indisponible"):
        precedente = champ.get("valeur_precedente")
        return {
            "etat": precedente["etat"] if precedente else "non_renseigne",
            "valeur": precedente["valeur"] if precedente else None,
            "recherche": "acces_indisponible",
            "motif": "consultation indisponible ; dernière version connue conservée",
        }

    retenues, refusees = [], []
    for a in affirmations:
        if a.get("portee") == "groupe":
            refusees.append({**a, "refus": "information générale sur le groupe, pas propre à l'espèce"})
        elif profil.get("usage_commercial") and "NC" in str(a.get("licence", "")).upper():
            refusees.append({**a, "refus": "licence non commerciale incompatible avec l'usage déclaré"})
        elif a.get("droits") == "incertains":
            refusees.append({**a, "refus": "droits incertains : référence et lien conservés, contenu non repris"})
        else:
            retenues.append(a)

    # Sources de complément (encyclopédies collaboratives, sites de vulgarisation) :
    # elles ne servent qu'à combler un champ qu'aucune source de référence ne renseigne.
    references = [a for a in retenues if a.get("niveau", "reference") == "reference"]
    complements = [a for a in retenues if a.get("niveau") == "complement"]
    if references:
        retenues = references
        refusees += [{**a, "refus": "complément non utilisé : une source de référence renseigne ce champ"} for a in complements]
    elif complements:
        return _champ_complement(complements, refusees)

    if not retenues:
        return {
            "etat": "non_renseigne",
            "valeur": None,
            "recherche": "recherche_effectuee" if affirmations else champ.get("recherche", "non_recherche"),
            "references_conservees": refusees,
        }

    # Contextes distincts (territoire, période, population, captivité) : plusieurs valeurs, pas un conflit.
    contextes: dict[tuple, list[dict]] = {}
    for a in retenues:
        cle = (a.get("territoire"), a.get("periode"), a.get("population"), a.get("contexte"))
        contextes.setdefault(cle, []).append(a)

    valeurs, contradictoire = [], False
    for cle, groupe in contextes.items():
        distinctes = {json.dumps(a["valeur"], sort_keys=True) for a in groupe}
        origines = _origines(groupe)
        if len(distinctes) > 1:
            plus_competente = [a for a in groupe if a.get("plus_competente")]
            if len(plus_competente) == 1:
                valeurs.append({"contexte": cle, "valeur": plus_competente[0]["valeur"], "motif": "source plus compétente pour ce fait"})
                continue
            contradictoire = True
            valeurs.append({"contexte": cle, "valeur": None, "valeurs_en_conflit": [a["valeur"] for a in groupe]})
        else:
            valeurs.append({"contexte": cle, "valeur": groupe[0]["valeur"], "origines": sorted(origines)})

    if contradictoire:
        return {"etat": "contradictoire", "valeur_synthese": None, "valeurs": valeurs, "references_conservees": refusees}
    # Corroboré seulement si chaque contexte a au moins deux origines indépendantes :
    # deux valeurs dans deux contextes différents ne se confirment pas l'une l'autre.
    par_contexte = [len(_origines(groupe)) for groupe in contextes.values()]
    etat = "corrobore" if min(par_contexte) >= 2 else "documente"
    return {
        "etat": etat,
        "valeurs": valeurs,
        "origines_independantes": min(par_contexte),
        "references_conservees": refusees,
    }


def _champ_complement(complements: list[dict], refusees: list[dict]) -> dict:
    """Champ renseigné uniquement par des compléments : jamais corroboré. Dans chaque contexte,
    les compléments qui citent un ouvrage priment ; le champ est incertain si un contexte n'a
    aucune valeur référencée ou si les valeurs référencées divergent."""
    contextes: dict[tuple, list[dict]] = {}
    for a in complements:
        cle = (a.get("territoire"), a.get("periode"), a.get("population"), a.get("contexte"))
        contextes.setdefault(cle, []).append(a)
    valeurs, etat = [], "documente"
    for cle, groupe in contextes.items():
        cites = [a for a in groupe if a.get("reference_citee", True)]
        if cites:
            refusees += [{**a, "refus": "complément sans référence, écarté au profit d'un complément référencé"} for a in groupe if a not in cites]
            groupe = cites
        else:
            etat = "incertain"
        distinctes = {json.dumps(a["valeur"], sort_keys=True) for a in groupe}
        if len(distinctes) > 1:
            etat = "incertain"
        valeurs.append({"contexte": cle, "valeurs": [a["valeur"] for a in groupe], "origines": sorted(_origines(groupe))})
    return {
        "etat": etat,
        "niveau": "complement",
        "valeurs": valeurs,
        "motif": "aucune source de référence ; valeur issue d'une source de complément, à remplacer dès qu'une référence la renseigne",
        "references_conservees": refusees,
    }


LICENCES_LIBRES = {"cc0", "pd", "cc-by", "cc-by-sa"}
LICENCES_NC = {"cc-by-nc", "cc-by-nc-sa"}
TAILLE_MIN_PHOTO = 640


def decider_photo(photo: dict, profil: dict | None = None) -> dict:
    """Une photo n'est retenue que si sa licence permet de l'afficher, de la redimensionner
    et de la recadrer, si son auteur est connu (crédit obligatoire) et si elle est assez grande."""
    profil = profil or {}
    licence = (photo.get("licence") or "inconnue").lower()
    cote = max(photo.get("largeur") or 0, photo.get("hauteur") or 0)
    if "nd" in licence.split("-"):
        return {"admise": False, "motif": "licence sans modification (ND) : recadrage et redimensionnement interdits"}
    if licence in LICENCES_NC:
        if profil.get("usage_commercial"):
            return {"admise": False, "motif": "licence non commerciale incompatible avec l'usage déclaré"}
    elif licence not in LICENCES_LIBRES:
        return {"admise": False, "motif": f"licence « {licence} » non réutilisable ou inconnue"}
    if licence not in {"cc0", "pd"} and not photo.get("auteur"):
        return {"admise": False, "motif": "auteur inconnu : le crédit exigé par la licence est impossible"}
    if cote and cote < TAILLE_MIN_PHOTO:
        return {"admise": False, "motif": f"image trop petite ({cote} px, minimum {TAILLE_MIN_PHOTO})"}
    if not photo.get("identite_verifiee"):
        return {"admise": False, "motif": "rattachement de la photo à l'espèce non vérifié"}
    restriction = "usage non commercial seulement" if licence in LICENCES_NC else None
    return {"admise": True, "motif": "licence réutilisable, auteur connu, espèce vérifiée", **({"restriction": restriction} if restriction else {})}


def decider_photos(photos: list[dict], profil: dict | None = None) -> dict:
    """Garde l'ordre de priorité des sources ; la première photo admise est proposée comme
    recommandée. Le skill ne valide jamais une photo : la validation appartient à l'utilisateur."""
    resultats = [{**p, **decider_photo(p, profil)} for p in photos]
    admises = [r for r in resultats if r["admise"]]
    return {
        "recommandee": admises[0].get("id") if admises else None,
        "admises": [r.get("id") for r in admises],
        "refusees": [{"id": r.get("id"), "motif": r["motif"]} for r in resultats if not r["admise"]],
    }


def decider_localisation(localisation: dict) -> dict:
    """Section 13.3 : grain le plus protecteur ; jamais de reconstitution."""
    grains = localisation.get("grains_autorises", [])
    ordre = ["masquee", "departement", "maille_10km", "commune", "maille_1km", "precise"]
    if localisation.get("regle_incertaine") or not grains:
        return {"grain": "masquee" if not grains else grains[0], "motif": "règle incertaine : grain le plus protecteur"}
    grain = min(grains, key=ordre.index)
    return {"grain": grain, "motif": f"restriction de {localisation.get('source_restriction', 'la source')}", "croisement_interdit": True}


def decider(dossier: dict) -> dict:
    """Point d'entrée : un dossier peut contenir l'admission et/ou des champs."""
    sortie: dict = {}
    if "identite" in dossier or "noms" in dossier or "presence" in dossier:
        sortie["admission"] = decider_admission(dossier)
    if "champs" in dossier:
        sortie["champs"] = {nom: decider_champ(c, dossier.get("profil")) for nom, c in dossier["champs"].items()}
    if "photos" in dossier:
        sortie["photos"] = decider_photos(dossier["photos"], dossier.get("profil"))
    if "localisation" in dossier:
        sortie["localisation"] = decider_localisation(dossier["localisation"])
    return sortie


def main(argv: list[str]) -> int:
    texte = Path(argv[1]).read_text(encoding="utf-8") if len(argv) > 1 else sys.stdin.read()
    json.dump(decider(json.loads(texte)), sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
