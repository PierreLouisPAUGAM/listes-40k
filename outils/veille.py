#!/usr/bin/env python3
"""Veille des sources de règles et de points pour les factions actives.

Mode par défaut : détection. Compare l'état en ligne des sources officielles à
l'état enregistré dans sources/etat.json et affiche un rapport. N'écrit rien.

  --enregistrer   écrit l'état constaté dans etat.json (après une intégration)
  --js            affiche le JavaScript à exécuter dans Chrome pour les sources
                  communautaires (sites bloqués en accès direct)
  --navigateur F  ajoute au rapport le résultat de ce JavaScript, enregistré dans F
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


def rsc_lignes(page):
    """Lignes « id:json » des données que Next.js insère dans la page."""
    flux = "".join(json.loads('"' + m + '"') for m in re.findall(
        r'self\.__next_f\.push\(\[1,"((?:[^"\\]|\\.)*)"\]\)', page))
    lignes = {}
    for l in flux.split("\n"):
        m = re.match(r"([0-9a-f]+):(.*)", l)
        if m:
            lignes[m.group(1)] = m.group(2)
    return lignes


BLOCS = {"div", "p", "li", "ul", "ol", "table", "thead", "tbody", "tr",
         "h1", "h2", "h3", "h4", "h5", "h6"}


def rsc_texte(noeud, lignes, sortie):
    """Texte d'un arbre de composants : une ligne par paragraphe, cellules séparées par « | »."""
    def resoudre(n):
        if isinstance(n, str) and n.startswith("$L") and n[2:] in lignes:
            return json.loads(lignes[n[2:]])
        return n

    def element(n):
        return isinstance(n, list) and len(n) == 4 and n[0] == "$" and isinstance(n[3], dict)

    def plat(n):
        n = resoudre(n)
        if isinstance(n, str):
            return "" if n.startswith("$") else n
        if element(n):
            if n[1] == "tr":
                enfants = n[3].get("children") or []
                enfants = enfants if isinstance(enfants, list) and not element(enfants) else [enfants]
                return " | ".join(plat(c).strip() for c in enfants)
            return plat(n[3].get("children"))
        if isinstance(n, list):
            return "".join(plat(c) for c in n)
        return ""

    def contient_bloc(n):
        n = resoudre(n)
        if element(n):
            return n[1] in BLOCS or contient_bloc(n[3].get("children"))
        return isinstance(n, list) and any(contient_bloc(c) for c in n)

    def ajouter(texte):
        texte = re.sub(r"\s+", " ", texte).strip()
        if texte:
            sortie.append(texte)

    noeud = resoudre(noeud)
    if element(noeud) and noeud[1] != "tr" and contient_bloc(noeud[3].get("children")):
        rsc_texte(noeud[3].get("children"), lignes, sortie)
    elif isinstance(noeud, list) and not element(noeud):
        # Texte et éléments en ligne qui se suivent forment un seul paragraphe.
        tampon = ""
        for c in map(resoudre, noeud):
            if element(c) and c[1] == "br":
                ajouter(tampon)
                tampon = ""
            elif contient_bloc(c):
                ajouter(tampon)
                tampon = ""
                rsc_texte(c, lignes, sortie)
            else:
                tampon += plat(c)
        ajouter(tampon)
    else:
        ajouter(plat(noeud))
    return sortie


def mfm_rassembler(page):
    """Panneau « Rassembler les Armées » : présent dans les données de la page, pas
    dans le HTML affiché. Ses titres sont les seuls éléments de classe text-lg."""
    lignes = rsc_lignes(page)
    ligne = next((v for v in lignes.values() if '"className":"text-lg"' in v), None)
    if ligne is None:
        raise ErreurAcces("panneau « Rassembler les Armées » introuvable")
    return rsc_texte(json.loads(ligne), lignes, [])


def verifier_mfm(faction, langue, url=None):
    url = url or MFM.format(langue=langue, faction=faction["mfm"])
    page = telecharger(url)
    version, contenu = mfm_contenu(mfm_texte(page))
    return page, {
        "id": f"mfm:{faction['mfm']}:{langue}",
        "libelle": f"Munitorum {faction['nom']} ({langue})",
        "type": "officielle",
        "url": url,
        "version": version,
        "empreinte": hashlib.sha256("\n".join(contenu).encode()).hexdigest(),
        "detail": f"{sum(1 for l in contenu if l.endswith(' pts'))} coûts",
    }


def verifier_rassembler(page, langue, url):
    contenu = mfm_rassembler(page)
    return {
        "id": f"mfm:rassembler:{langue}",
        "libelle": f"Rassembler les Armées ({langue})",
        "type": "officielle",
        "url": url,
        "version": "sans version",
        "empreinte": hashlib.sha256("\n".join(contenu).encode()).hexdigest(),
        "detail": f"{len(contenu)} paragraphes",
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


# ---------------------------------------------------- sources via le navigateur

# 40k.app bloque les accès directs (protection Vercel) : ce code s'exécute dans un
# onglet Chrome ouvert sur https://www.40k.app/. Il ne couvre que l'index des
# datasheets (avec les points), les détachements et les mises à jour : une
# correction du seul texte d'une règle n'y apparaît pas.
JS_40KAPP = """await (async () => {
  const factions = %s;
  const texte = async (u) => {
    const r = await fetch(u);
    if (!r.ok) throw new Error(u + " : HTTP " + r.status);
    const d = new DOMParser().parseFromString(await r.text(), "text/html");
    d.querySelectorAll("script,style").forEach((e) => e.remove());
    return [d, (d.querySelector("main") || d.body).innerText.replace(/\\s+/g, " ").trim()];
  };
  const sha = async (t) => [...new Uint8Array(await crypto.subtle.digest("SHA-256",
    new TextEncoder().encode(t)))].map((b) => b.toString(16).padStart(2, "0")).join("");
  const sortie = [];
  for (const f of factions) {
    const base = "/factions/" + f.app40k;
    try {
      const [, index] = await texte(base);
      const [det, detachements] = await texte(base + "/detachments");
      const [, maj] = await texte(base + "/updates");
      const n = new Set([...det.querySelectorAll("a")].map((a) => a.getAttribute("href"))
        .filter((h) => h && h.startsWith(base + "/detachments/"))).size;
      sortie.push({id: "c:40kapp:" + f.app40k, libelle: "40k.app " + f.nom + " (en)",
        type: "communautaire", url: "https://www.40k.app" + base, version: "sans version",
        empreinte: await sha([index, detachements, maj].join("\\n")), detail: n + " détachements"});
    } catch (e) {
      sortie.push({id: "c:40kapp:" + f.app40k, libelle: "40k.app " + f.nom + " (en)",
        erreur: String(e)});
    }
  }
  return JSON.stringify(sortie);
})()"""


def sans_pack_francais(factions, entrees):
    ids = {e["id"] for e in entrees}
    return [f for f in factions if f"pdf:pack:{f['id']}:fr" not in ids]


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
    p.add_argument("--js", action="store_true")
    p.add_argument("--navigateur", type=Path, metavar="FICHIER")
    p.add_argument("--json", action="store_true")
    p.add_argument("--langue", default="fr")
    p.add_argument("--url", action="append", default=[], metavar="ID=URL")
    p.add_argument("--etat", type=Path, default=ETAT)
    args = p.parse_args()

    urls = dict(u.split("=", 1) for u in args.url)
    factions = [f for _, f in correspondances(factions_actives())]
    etat = json.loads(args.etat.read_text(encoding="utf-8"))["sources"] if args.etat.exists() else {}

    entrees, infos, avertissements = [], [], []
    rassembler = None
    for f in factions:
        try:
            page, entree = verifier_mfm(f, args.langue, urls.get(f["mfm"]))
            entrees.append(entree)
            if rassembler is None:
                rassembler = verifier_rassembler(page, args.langue, entree["url"])
        except ErreurAcces as e:
            entrees.append({"id": f"mfm:{f['mfm']}:{args.langue}",
                            "libelle": f"Munitorum {f['nom']} ({args.langue})", "erreur": str(e)})
    if rassembler:
        entrees.append(rassembler)
    try:
        entrees += verifier_pdf(factions)
    except (ErreurAcces, KeyError, ValueError) as e:
        entrees.append({"id": "pdf", "libelle": "API des téléchargements", "erreur": str(e)})

    communautaires = sans_pack_francais(factions, entrees)
    if args.js:
        print(JS_40KAPP % json.dumps([{"app40k": f["app40k"], "nom": f["nom"]}
                                       for f in communautaires], ensure_ascii=False))
        return 0
    if args.navigateur:
        entrees += json.loads(args.navigateur.read_text(encoding="utf-8"))
    elif communautaires:
        avertissements.append("40k.app non vérifié (" + ", ".join(f["nom"] for f in communautaires)
                              + ") : lancer --js dans Chrome puis --navigateur")
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
