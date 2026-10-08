#!/usr/bin/env python3
"""Veille des sources de règles et de points pour les factions actives.

Mode par défaut : détection. Compare l'état en ligne des sources officielles à
l'état enregistré dans sources/etat.json et affiche un rapport. N'écrit rien.

  --enregistrer   écrit l'état constaté dans etat.json (après une intégration)
  --json          rapport au format JSON
  --langue en     lit le Munitorum en anglais (tests)
  --url ID=URL    remplace l'adresse du Munitorum d'une faction (tests, archives)
  --etat CHEMIN   utilise un autre fichier d'état (tests)

Codes de retour : 0 tout est à jour, 1 au moins un changement, 2 erreur d'accès.
Python standard uniquement, aucun navigateur.
"""

import argparse
import datetime
import gzip
import hashlib
import html
import json
import re
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
PROFIL = RACINE / "profil.md"
FACTIONS = RACINE / "sources" / "factions.json"
ETAT = RACINE / "sources" / "etat.json"

MFM = "https://mfm.warhammer-community.com/{langue}/{faction}"
API_TELECHARGEMENTS = "https://www.warhammer-community.com/api/search/downloads/"
ASSETS = "https://assets.warhammer-community.com/"
BSDATA_PR = "https://api.github.com/repos/BSData/wh40k-11e-mfm/pulls?state=open"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

# Documents communs à toutes les factions, repérés par le nom de leur fichier.
DOCUMENTS_GENERAUX = {
    "regles-de-base": ("core_rules", "Règles de Base"),
    "maj-universelles": ("universal_rules_updates", "Mises à jour des règles universelles"),
}


class ErreurAcces(Exception):
    pass


# ---------------------------------------------------------------- accès réseau

def telecharger(url, donnees=None, entetes=None):
    entetes = dict(entetes or {})
    entetes.setdefault("User-Agent", UA)
    requete = urllib.request.Request(url, data=donnees, headers=entetes)
    try:
        with urllib.request.urlopen(requete, timeout=60) as reponse:
            corps = reponse.read()
    except (urllib.error.URLError, TimeoutError) as e:
        raise ErreurAcces(f"{url} : {e}") from e
    if corps[:2] == b"\x1f\x8b":  # les archives web.archive.org arrivent compressées
        corps = gzip.decompress(corps)
    return corps.decode("utf-8")


# ----------------------------------------------------------- factions actives

def factions_actives():
    """Noms des lignes « Active » du tableau des factions de profil.md."""
    noms = []
    for ligne in PROFIL.read_text(encoding="utf-8").splitlines():
        cellules = [c.strip() for c in ligne.strip().strip("|").split("|")]
        if len(cellules) >= 2 and cellules[1] == "Active":
            noms.append(cellules[0])
    return noms


def correspondances(noms):
    table = json.loads(FACTIONS.read_text(encoding="utf-8"))
    manquantes = [n for n in noms if n not in table]
    if manquantes:
        raise SystemExit(
            "Faction active sans correspondance dans sources/factions.json : "
            + ", ".join(manquantes))
    return [(nom, f) for nom in noms for f in table[nom]]


# ------------------------------------------------------- Inventaire du Munitorum

def mfm_texte(page):
    """Texte de la page, valeurs différées comprises, une ligne par élément.

    Next.js envoie les coûts dans des blocs masqués <div hidden id="S:x"> placés
    en fin de page ; chaque <template id="P:x"> marque leur emplacement.
    """
    blocs = dict(re.findall(
        r'<div hidden id="S:([0-9a-f]+)">(.*?)</div><script>\$RS\("S:\1"',
        page, flags=re.S))
    for _ in range(5):
        suivante = re.sub(r'<template id="P:([0-9a-f]+)"></template>',
                          lambda m: blocs.get(m.group(1), ""), page)
        if suivante == page:
            break
        page = suivante
    page = re.sub(r'<div hidden id="S:([0-9a-f]+)">.*?</div><script>\$RS\("S:\1"',
                  "<script>", page, flags=re.S)
    page = re.sub(r"<script.*?</script>", "", page, flags=re.S)
    # Drapeaux « MIS À JOUR », « BODYGUARD UNITS UPDATED »… : relatifs à la
    # version précédente, ils ne font pas partie du contenu.
    page = re.sub(r'<div class="m-0 px-1 py-0\.5[^"]*"><span>[^<]*</span></div>', "", page)
    texte = html.unescape(re.sub(r"<[^>]+>", "\n", page))
    return [l.strip() for l in texte.split("\n") if l.strip()]


def mfm_contenu(lignes):
    """Version et contenu normalisé : détachements, optimisations, unités, coûts."""
    version = next((l for l in lignes if re.fullmatch(r"v\d+\.\d+", l)), None)
    if version is None or "FACTIONS" not in lignes:
        raise ErreurAcces("structure de page inattendue (version ou repère FACTIONS absent)")
    contenu = []
    for l in lignes[lignes.index("FACTIONS") + 1:]:
        l = re.sub(r"^[▲▼]\s*(\([+-]?\d+\)\s*)?", "", l)  # écart avec la version précédente
        if l:
            contenu.append(l)
    return version, contenu


def verifier_mfm(faction, langue, url=None):
    url = url or MFM.format(langue=langue, faction=faction["mfm"])
    version, contenu = mfm_contenu(mfm_texte(telecharger(url)))
    return {
        "id": f"mfm:{faction['mfm']}:{langue}",
        "libelle": f"Munitorum {faction['nom']} ({langue})",
        "type": "officielle",
        "url": url,
        "version": version,
        "empreinte": hashlib.sha256("\n".join(contenu).encode()).hexdigest(),
        "detail": f"{sum(1 for l in contenu if l.endswith(' pts'))} coûts",
    }


# ---------------------------------------------------- API des téléchargements

def documents(langue):
    corps = json.dumps({"index": "downloads_v2", "searchTerm": "",
                        "gameSystem": "warhammer-40000", "language": langue}).encode()
    reponse = json.loads(telecharger(API_TELECHARGEMENTS, corps,
                                     {"Content-Type": "application/json"}))
    return [{"titre": h["title"], "maj": h["id"]["last_updated"], "fichier": h["id"]["file"]}
            for h in reponse["hits"]]


def entree_pdf(ident, libelle, doc, note=""):
    if doc is None:
        return {"id": ident, "libelle": libelle, "type": "officielle", "url": None,
                "version": "absent", "empreinte": "absent", "detail": note}
    return {"id": ident, "libelle": libelle, "type": "officielle",
            "url": ASSETS + doc["fichier"], "version": f"MAJ {doc['maj']}",
            "empreinte": f"{doc['maj']}|{doc['fichier']}", "detail": note}


def chercher(docs, motif):
    return next((d for d in docs if re.search(motif, d["fichier"])), None)


def verifier_pdf(factions):
    fr, en = documents("french"), documents("english")
    entrees = [entree_pdf(f"pdf:{nom}:fr", f"{titre} (fr)", chercher(fr, motif))
               for nom, (motif, titre) in DOCUMENTS_GENERAUX.items()]
    for faction in factions:
        motif = "faction_pack_" + re.sub(r"[-_]", "[-_]", faction["pack"]) + r"\b"
        pack_fr = chercher(fr, motif)
        if pack_fr:
            entrees.append(entree_pdf(f"pdf:pack:{faction['id']}:fr",
                                      f"Pack de Faction {faction['nom']} (fr)", pack_fr))
            continue
        # Sans pack français, le texte officiel est passé dans un codex ou l'appli.
        pack_en = chercher(en, motif)
        if pack_en and "legends" in pack_en["titre"].lower():
            note = "pack réduit aux Legends : règles dans le codex ou l'appli"
        elif pack_en:
            note = "pack en anglais seulement"
        else:
            note = "aucun pack : règles dans le codex ou l'appli"
        entrees.append(entree_pdf(f"pdf:pack:{faction['id']}:en",
                                  f"Pack de Faction {faction['nom']} (en)", pack_en, note))
    return entrees


# ------------------------------------------------------------------- BSData

def pr_bsdata():
    """PR ouvertes de mise à jour des points (information, non enregistrée)."""
    prs = json.loads(telecharger(BSDATA_PR, entetes={"Accept": "application/vnd.github+json"}))
    return [f"PR n° {p['number']} ({p['updated_at'][:10]}) : {p['title']}"
            for p in prs if "MFM" in p["title"]]


# --------------------------------------------------------------- comparaison

def comparer(entrees, etat):
    for e in entrees:
        if "erreur" in e:
            e["statut"] = "erreur"
            continue
        ancien = etat.get(e["id"])
        if ancien is None:
            e["statut"] = "absent du dépôt"
        elif ancien["empreinte"] == e["empreinte"]:
            e["statut"] = "à jour"
        else:
            e["statut"] = "modifié"
            consulte = datetime.date.fromisoformat(ancien["consulte_le"]).strftime("%d/%m/%Y")
            e["enregistre"] = f"{ancien['version']}, consulté le {consulte}"
    return entrees


def enregistrer(entrees, chemin, etat):
    aujourdhui = datetime.date.today().isoformat()
    for e in entrees:
        if "erreur" in e:
            continue
        ancien = etat.get(e["id"], {})
        etat[e["id"]] = {
            "libelle": e["libelle"], "type": e["type"], "url": e["url"],
            "version": e["version"], "empreinte": e["empreinte"],
            "consulte_le": aujourdhui, "derives": ancien.get("derives", []),
        }
    chemin.write_text(json.dumps({"sources": dict(sorted(etat.items()))},
                                 ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rapport_texte(entrees, infos, avertissements):
    largeur = max(len(e["libelle"]) for e in entrees)
    print(f"Veille du {datetime.date.today().strftime('%d/%m/%Y')}\n")
    for e in entrees:
        if e["statut"] == "erreur":
            print(f"  {e['libelle']:<{largeur}}  ERREUR  {e['erreur']}")
            continue
        ligne = f"  {e['libelle']:<{largeur}}  {e['statut']:<15} {e['version']}"
        if e.get("detail"):
            ligne += f" ; {e['detail']}"
        if e.get("enregistre"):
            ligne += f" (dépôt : {e['enregistre']})"
        print(ligne)
    for titre, lignes in (("Informations", infos), ("Avertissements", avertissements)):
        if lignes:
            print(f"\n{titre} :")
            for l in lignes:
                print(f"  - {l}")


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--enregistrer", action="store_true")
    p.add_argument("--json", action="store_true")
    p.add_argument("--langue", default="fr")
    p.add_argument("--url", action="append", default=[], metavar="ID=URL")
    p.add_argument("--etat", type=Path, default=ETAT)
    args = p.parse_args()

    urls = dict(u.split("=", 1) for u in args.url)
    factions = [f for _, f in correspondances(factions_actives())]
    etat = json.loads(args.etat.read_text(encoding="utf-8"))["sources"] if args.etat.exists() else {}

    entrees, infos, avertissements = [], [], []
    for f in factions:
        try:
            entrees.append(verifier_mfm(f, args.langue, urls.get(f["mfm"])))
        except ErreurAcces as e:
            entrees.append({"id": f"mfm:{f['mfm']}:{args.langue}",
                            "libelle": f"Munitorum {f['nom']} ({args.langue})", "erreur": str(e)})
    try:
        entrees += verifier_pdf(factions)
    except (ErreurAcces, KeyError, ValueError) as e:
        entrees.append({"id": "pdf", "libelle": "API des téléchargements", "erreur": str(e)})
    try:
        infos += pr_bsdata()
    except ErreurAcces as e:
        avertissements.append(f"PR BSData non consultées : {e}")
    if not shutil.which("pdftotext"):
        avertissements.append("pdftotext absent : l'intégration des PDF sera impossible "
                              "(brew install poppler)")

    comparer(entrees, etat)
    if args.enregistrer:
        enregistrer(entrees, args.etat, etat)
        avertissements.append(f"état enregistré dans {args.etat}")

    if args.json:
        print(json.dumps({"sources": entrees, "informations": infos,
                          "avertissements": avertissements}, ensure_ascii=False, indent=2))
    else:
        rapport_texte(entrees, infos, avertissements)

    if any(e["statut"] == "erreur" for e in entrees):
        return 2
    return 0 if all(e["statut"] == "à jour" for e in entrees) else 1


if __name__ == "__main__":
    sys.exit(main())
