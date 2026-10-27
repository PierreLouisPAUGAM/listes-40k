#!/usr/bin/env python3
"""Veille des sources de règles et de points pour les factions actives.

Mode par défaut : détection. Compare l'état en ligne des sources officielles à
l'état enregistré dans sources/etat.json et affiche un rapport. N'écrit rien.

  --extraire [ID] écrit points, détachements et attachements des factions
                  (toutes les actives si aucun ID) dans regles/factions/
  --enregistrer [ID…]  écrit l'état constaté dans etat.json, pour les sources dont
                  l'identifiant commence par l'un des ID (toutes si aucun)
  --js            affiche le JavaScript à exécuter dans Chrome pour 40k.app
                  (site bloqué en accès direct), pour toutes les factions actives
  --navigateur F  ajoute au rapport le résultat de ce JavaScript, enregistré dans F
                  (40k.app ne sert plus qu'en secours de l'appli)
  --appli         interroge l'appli Warhammer 40,000 du Mac (outils/appli/appli) : dates
                  de mise à jour des codex de chaque faction et des Règles de Base
  --readme        régénère le tableau de fraîcheur de README.md depuis etat.json
                  (sans accès réseau)
  --json          rapport au format JSON
  --langue en     lit le Munitorum en anglais (tests)
  --url ID=URL    remplace l'adresse du Munitorum d'une faction (tests, archives)
  --etat CHEMIN   utilise un autre fichier d'état (tests)

Codes de retour : 0 tout est à jour, 1 au moins un changement ou appli non vérifiée,
2 erreur d'accès.
Python standard uniquement ; l'appli est lue par l'outil Swift outils/appli/appli.
"""

import argparse
import datetime
import gzip
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
PROFIL = RACINE / "profil.md"
FACTIONS = RACINE / "sources" / "factions.json"
ETAT = RACINE / "sources" / "etat.json"
RASSEMBLER = RACINE / "regles" / "rassembler-les-armees.txt"
README = RACINE / "README.md"
MARQUES = ("<!-- fraicheur:debut -->", "<!-- fraicheur:fin -->")
CONSTRUCTION = "regles/construction-armee.md"
APPLI = RACINE / "outils" / "appli" / "appli"
APPLI_SOURCE = RACINE / "outils" / "appli" / "appli.swift"
# Pages de l'appli communes à toutes les factions (chemins depuis la racine de Référence).
APPLI_GENERAL = ["Règles de Base"]
MOIS = {m: i for i, m in enumerate(("janvier", "février", "mars", "avril", "mai", "juin", "juillet",
                                     "août", "septembre", "octobre", "novembre", "décembre"), 1)}

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
    detachements = sum(1 for b in mfm_structure(page).values() if b["type"] == "detachement")
    return page, {
        "id": f"mfm:{faction['mfm']}:{langue}",
        "libelle": f"Munitorum {faction['nom']} ({langue})",
        "type": "officielle",
        "url": url,
        "version": version,
        "empreinte": hashlib.sha256("\n".join(contenu).encode()).hexdigest(),
        "detail": f"{sum(1 for l in contenu if l.endswith(' pts'))} coûts, "
                  f"{detachements} détachements",
        "detachements": detachements,
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


def entree_pdf(ident, libelle, doc, note="", qualificatif=""):
    # L'empreinte « absent » est conservée : seule la version affichée est explicite.
    if doc is None:
        return {"id": ident, "libelle": libelle, "type": "officielle", "url": None,
                "version": "aucun pack (codex ou appli)", "empreinte": "absent", "detail": note}
    return {"id": ident, "libelle": libelle, "type": "officielle",
            "url": ASSETS + doc["fichier"], "version": f"{qualificatif}MAJ {doc['maj']}",
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
        note, qualificatif = "", ""
        if pack_en and "legends" in pack_en["titre"].lower():
            qualificatif = "Legends seulement, "
        elif pack_en:
            note = "pack en anglais seulement"
        entrees.append(entree_pdf(f"pdf:pack:{faction['id']}:en",
                                  f"Pack de Faction {faction['nom']} (en)", pack_en, note,
                                  qualificatif))
    return entrees


# ------------------------------------------------------ extraction structurée

UUID = re.compile(r"^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$")
CLASSE_BLOC = "flex flex-col space-y-1 m-1 print:break-inside-avoid-page"
ROLES = {"/leader.svg": "meneur", "/support.svg": "appui"}
ICONE_OPTIONS = "/cog.svg"  # rubrique « OPTIONS D'ÉQUIPEMENT » : surcoût par équipement


class Arbre:
    """Accès à l'arbre de composants d'une page du Munitorum."""

    def __init__(self, page):
        self.lignes = rsc_lignes(page)
        self.cache = {}

    def resoudre(self, n):
        if isinstance(n, str) and n.startswith("$L") and n[2:] in self.lignes:
            if n not in self.cache:
                self.cache[n] = json.loads(self.lignes[n[2:]])
            return self.cache[n]
        return n

    @staticmethod
    def element(n):
        return isinstance(n, list) and len(n) == 4 and n[0] == "$" and isinstance(n[3], dict)

    def enfants(self, n):
        n = self.resoudre(n)
        c = self.resoudre(n[3].get("children")) if self.element(n) else n
        if self.element(c):
            return [c]
        return [self.resoudre(x) for x in c] if isinstance(c, list) else []

    def texte(self, n):
        n = self.resoudre(n)
        if isinstance(n, str):
            return "" if n.startswith("$") else n
        if self.element(n):
            return self.texte(n[3].get("children"))
        if isinstance(n, list):
            return "".join(self.texte(c) for c in n)
        return ""

    def parcourir(self, n, visiteur):
        """Appelle visiteur sur chaque élément ; s'il renvoie False, n'entre pas dedans."""
        n = self.resoudre(n)
        if self.element(n):
            if visiteur(n) is not False:
                self.parcourir(n[3].get("children"), visiteur)
        elif isinstance(n, list):
            for c in n:
                self.parcourir(c, visiteur)

    def blocs(self):
        """Blocs d'unité et de détachement, indexés par leur identifiant."""
        trouves = {}

        def visiteur(n):
            if (n[1] == "div" and isinstance(n[2], str) and UUID.match(n[2])
                    and n[3].get("className") == CLASSE_BLOC):
                trouves.setdefault(n[2], n)
                return False

        for ligne in self.lignes.values():
            try:
                self.parcourir(json.loads(ligne), visiteur)
            except ValueError:
                continue
        return trouves


def nettoyer(texte):
    return re.sub(r"\s+", " ", re.sub(r"[▲▼]\s*(\([+-]?\d+\)\s*)?", "", texte)).strip()


def palier(intitule):
    """« DE LA 1RE À LA 2E, VOS UNITÉS COÛTENT » → 1-2 ; « VOTRE UNITÉ COÛTE » → toutes."""
    nombres = re.findall(r"\d+", intitule)
    if len(nombres) >= 2:
        return f"{nombres[0]}-{nombres[1]}"
    if nombres:
        suivantes = "+" in intitule or "SUIVANT" in intitule.upper()
        return nombres[0] + ("+" if suivantes else "")
    return "toutes"


def attachements(arbre, bloc):
    """Rôles de meneur ou d'appui : icône du rôle, puis liste des gardes du corps."""
    trouves = []

    def visiteur(n):
        enfants = arbre.enfants(n)
        if len(enfants) < 2:
            return
        icones = []
        arbre.parcourir(enfants[0], lambda e: icones.append(e[3].get("src")))
        role = next((ROLES[s] for s in icones if s in ROLES), None)
        if role:
            noms = [nettoyer(x) for x in arbre.texte(enfants[1]).split(",")]
            trouves.append((role, [x for x in noms if x]))
            return False

    arbre.parcourir(bloc[3].get("children"), visiteur)
    return trouves


def options(arbre, bloc):
    """Surcoûts d'équipement, indexés par l'identifiant de leur ligne."""
    trouves = []

    def visiteur(n):
        enfants = arbre.enfants(n)
        if len(enfants) < 2:
            return
        icones = []
        arbre.parcourir(enfants[0], lambda e: icones.append(e[3].get("src")))
        if ICONE_OPTIONS not in icones:
            return

        def ligne(e):
            if e[1] == "li":
                morceaux = [nettoyer(arbre.texte(x)) for x in arbre.enfants(e)]
                morceaux = [m for m in morceaux if m]
                if len(morceaux) >= 2:
                    trouves.append({"id": e[2], "option": morceaux[0], "points": morceaux[-1]})
                return False

        for c in enfants[1:]:
            arbre.parcourir(c, ligne)
        return False

    arbre.parcourir(bloc[3].get("children"), visiteur)
    return trouves


def lire_bloc(arbre, bloc):
    enfants = arbre.enfants(bloc)
    entete = enfants[0] if enfants else None
    spans = []
    arbre.parcourir(entete, lambda e: spans.append(arbre.texte(e)) if e[1] == "span" else None)
    nom = nettoyer(spans[0] if spans else arbre.texte(entete))
    pdd = next((m.group(1) for s in spans for m in [re.fullmatch(r"(\d+)\s*(PDD|DP)", s.strip())] if m), None)

    if pdd is not None:
        dispositions, optimisations = [], []

        def visiteur(n):
            style = n[3].get("style") or {}
            if "backgroundColor" in style:
                dispositions.append(nettoyer(arbre.texte(n)))
                return False
            if isinstance(n[2], str) and UUID.match(n[2]) and n[1] in ("div", "$1") and n is not bloc:
                valeurs = []
                arbre.parcourir(n, lambda e: valeurs.append(arbre.texte(e)) if e[1] == "span" else None)
                valeurs = [nettoyer(v) for v in valeurs if nettoyer(v)]
                if len(valeurs) >= 2 and valeurs[1].endswith("pts"):
                    optimisations.append({"id": n[2], "nom": valeurs[0], "cout": valeurs[1],
                                          "attachements": attachements(arbre, n)})
                    return False

        arbre.parcourir(entete, lambda e: None)
        for c in enfants[1:]:
            arbre.parcourir(c, visiteur)
        return {"type": "detachement", "nom": nom, "pdd": pdd,
                "dispositions": dispositions, "optimisations": optimisations}

    couts = []

    def visiteur(n):
        enfants_n = arbre.enfants(n)
        listes = [e for e in enfants_n if arbre.element(e) and e[1] == "ul"]
        if listes and arbre.element(enfants_n[0]) and enfants_n[0][1] == "div":
            intitule = nettoyer(arbre.texte(enfants_n[0]))
            for li in arbre.enfants(listes[0]):
                morceaux = [nettoyer(arbre.texte(x)) for x in arbre.enfants(li)]
                morceaux = [m for m in morceaux if m]
                if len(morceaux) >= 2:
                    couts.append({"palier": palier(intitule), "effectif": morceaux[0],
                                  "points": morceaux[-1]})
            return False

    for c in enfants[1:]:
        arbre.parcourir(c, visiteur)
    return {"type": "unite", "nom": nom, "couts": couts, "attachements": attachements(arbre, bloc),
            "options": options(arbre, bloc)}


def mfm_structure(page):
    arbre = Arbre(page)
    return {cle: lire_bloc(arbre, bloc) for cle, bloc in arbre.blocs().items()}


def ecrire_tsv(chemin, entetes, lignes):
    contenu = ["\t".join(entetes)] + ["\t".join(str(c) for c in l) for l in lignes]
    chemin.write_text("\n".join(contenu) + "\n", encoding="utf-8")


def nombre(points):
    return int(re.sub(r"\D", "", points)) if re.search(r"\d", points) else points


def extraire(faction, page_fr=None):
    """Écrit les fichiers <faction>-points, -detachements et -attachements.tsv."""
    fr = mfm_structure(page_fr or telecharger(MFM.format(langue="fr", faction=faction["mfm"])))
    en = mfm_structure(telecharger(MFM.format(langue="en", faction=faction["mfm"])))
    manquants = sorted(set(fr) ^ set(en))
    if manquants:
        raise ErreurAcces(f"blocs sans équivalent entre /fr et /en : {len(manquants)}")
    nom_en = {}
    for cle, bloc in fr.items():
        nom_en[bloc["nom"]] = en[cle]["nom"]

    dossier = RACINE / faction["dossier"]
    dossier.mkdir(parents=True, exist_ok=True)
    prefixe = faction["mfm"]
    unites = sorted((b for b in fr.items() if b[1]["type"] == "unite"), key=lambda b: b[1]["nom"])
    detachements = sorted((b for b in fr.items() if b[1]["type"] == "detachement"),
                          key=lambda b: b[1]["nom"])

    points = []
    for cle, u in unites:
        for c in u["couts"]:
            points.append((u["nom"], en[cle]["nom"], c["palier"], c["effectif"], nombre(c["points"])))
    lignes_opt = []
    for cle, u in unites:
        opt_en = {o["id"]: o["option"] for o in en[cle]["options"]}
        for o in u["options"]:
            lignes_opt.append((u["nom"], en[cle]["nom"], o["option"], opt_en.get(o["id"], ""),
                               nombre(o["points"])))
    attache = []
    for cle, u in unites:
        for role, gardes in u["attachements"]:
            for g in gardes:
                attache.append((u["nom"], en[cle]["nom"], role, g, nom_en.get(g, "")))
    lignes_det = []
    for cle, d in detachements:
        opt_en = {o["id"]: o["nom"] for o in en[cle]["optimisations"]}
        for o in d["optimisations"] or [{"id": None, "nom": "", "cout": "", "attachements": []}]:
            lignes_det.append((d["nom"], en[cle]["nom"], d["pdd"], ", ".join(d["dispositions"]),
                               o["nom"], opt_en.get(o["id"], ""), nombre(o["cout"])))
            for role, gardes in o["attachements"]:
                for g in gardes:
                    attache.append((o["nom"], opt_en.get(o["id"], ""), role, g, nom_en.get(g, "")))

    # Deux noms d'unités collés : virgule manquante dans la source officielle.
    anomalies = sorted({g for *_, g, _ in attache if g not in nom_en and any(
        g[:i].strip() in nom_en and g[i:].strip() in nom_en for i in range(1, len(g)))})

    fichiers = {
        f"{prefixe}-points.tsv": (("unite", "unite_en", "palier", "effectif", "points"), points),
        f"{prefixe}-detachements.tsv": (("detachement", "detachement_en", "pdd", "dispositions",
                                         "optimisation", "optimisation_en", "cout"), lignes_det),
        f"{prefixe}-attachements.tsv": (("unite", "unite_en", "role", "gardes_du_corps",
                                         "gardes_du_corps_en"), attache),
        f"{prefixe}-options.tsv": (("unite", "unite_en", "option", "option_en", "points"),
                                   lignes_opt),
    }
    for nom, (entetes, lignes) in fichiers.items():
        ecrire_tsv(dossier / nom, entetes, lignes)
    return [str((dossier / n).relative_to(RACINE)) for n in fichiers], \
        {"unites": len(unites), "couts": len(points), "detachements": len(detachements),
         "attachements": len(attache), "options": len(lignes_opt), "anomalies": anomalies}


# ---------------------------------------------------- sources via le navigateur

# 40k.app bloque les accès directs (protection Vercel) : ce code s'exécute dans un
# onglet Chrome ouvert sur https://www.40k.app/. Il sert à toutes les factions : un Pack
# de Faction peut compléter un codex sans le remplacer, et le texte du codex n'a pas
# d'autre source automatisable. Les détachements absents de la page d'une faction
# (détachements de Chapitre des Space Marines) sont sur les pages app40k_complements de
# factions.json. Il ne couvre que l'index des
# datasheets (avec les points), les détachements et les mises à jour : une
# correction du seul texte d'une règle n'y apparaît pas.
JS_40KAPP = """await (async () => {
  const factions = %s;
  const texte = async (u) => {
    await new Promise((ok) => setTimeout(ok, 300));  // 40k.app limite le débit (HTTP 429)
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
      const textes = [index, detachements, maj];
      const slugs = new Set();
      const relever = (doc, b) => [...doc.querySelectorAll("a")].map((a) => a.getAttribute("href"))
        .filter((h) => h && h.startsWith(b + "/detachments/")).forEach((h) => slugs.add(h.split("/").pop()));
      relever(det, base);
      for (const c of f.complements) {
        const [doc, t] = await texte("/factions/" + c + "/detachments");
        textes.push(t);
        relever(doc, "/factions/" + c);
      }
      sortie.push({id: "c:40kapp:" + f.app40k, libelle: "40k.app " + f.nom + " (en)",
        type: "communautaire", url: "https://www.40k.app" + base, version: "sans version",
        empreinte: await sha(textes.join("\\n")), detail: slugs.size + " détachements",
        detachements: slugs.size});
    } catch (e) {
      sortie.push({id: "c:40kapp:" + f.app40k, libelle: "40k.app " + f.nom + " (en)",
        erreur: String(e)});
    }
  }
  return JSON.stringify(sortie);
})()"""


# ------------------------------------------------------------------- BSData

# ------------------------------------------------------------------------ appli

def date_appli(texte):
    """« 14 octobre 2026 » → « 14/10/2026 » ; texte inchangé s'il n'a pas cette forme."""
    m = re.fullmatch(r"(\d{1,2}) (\w+) (\d{4})", texte or "")
    if not m or m.group(2).lower() not in MOIS:
        return texte
    return f"{int(m.group(1)):02d}/{MOIS[m.group(2).lower()]:02d}/{m.group(3)}"


def verifier_appli(factions):
    """Une source par faction (codex et suppléments listés dans le champ « appli » de
    factions.json) et une pour les Règles de Base. Empreinte : date « Dernière Mise à
    Jour » de chaque page, ou version des données pour une page qui n'en a pas.
    Renvoie (entrées, avertissements) ; aucune entrée si l'appli n'est pas joignable."""
    if not APPLI.exists() or APPLI.stat().st_mtime < APPLI_SOURCE.stat().st_mtime:
        r = subprocess.run(["swiftc", "-O", str(APPLI_SOURCE), "-o", str(APPLI)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            return [], [f"appli non vérifiée : compilation de l'outil impossible ({r.stderr.strip()[:200]})"]
    r = subprocess.run([str(APPLI), "verifier"], capture_output=True, text=True)
    if r.returncode != 0:
        stop = next((l for l in r.stdout.splitlines() if l.startswith("STOP")), r.stderr.strip())
        return [], [f"appli non vérifiée : {stop}"]
    groupes = [(f"appli:{f['id']}:fr", f"Appli Warhammer 40,000, {f['nom']} (fr)", f.get("appli", []))
               for f in factions]
    groupes.append(("appli:general:fr", "Appli Warhammer 40,000, Règles de Base (fr)", APPLI_GENERAL))
    chemins = [c for _, _, liste in groupes for c in liste]
    r = subprocess.run([str(APPLI), "dates", *chemins], capture_output=True, text=True)
    if r.returncode != 0:
        return [], [f"appli non vérifiée : {r.stderr.strip() or 'commande dates en échec'}"]
    releve = json.loads(r.stdout)
    donnees, dates = releve.get("donnees") or "inconnue", releve["dates"]
    entrees, avertissements = [], []
    for ident, libelle, liste in groupes:
        if not liste:
            avertissements.append(f"{libelle} : aucun chemin dans le champ « appli » de factions.json")
            continue
        erreurs = [c for c in liste if isinstance(dates.get(c), dict)]
        if erreurs:
            entrees.append({"id": ident, "libelle": libelle,
                            "erreur": f"page introuvable dans l'appli : {', '.join(erreurs)}"})
            continue
        empreinte = "|".join(f"{c}={dates[c] or 'données ' + donnees}" for c in liste)
        datees = sorted({date_appli(dates[c]) for c in liste if dates[c]})
        version = f"données {donnees}" + (f", MAJ {', '.join(datees)}" if datees else "")
        entrees.append({"id": ident, "libelle": libelle, "type": "officielle", "url": None,
                        "version": version, "empreinte": empreinte})
    return entrees, avertissements


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


def derives_par_defaut(e, factions):
    """Fichiers du dépôt alimentés par une source, quand l'intégration ne les précise pas."""
    if e["id"].startswith("mfm:rassembler"):
        return [str(RASSEMBLER.relative_to(RACINE)), CONSTRUCTION]
    if e["id"].startswith(("pdf:regles-de-base", "pdf:maj-universelles", "appli:general")):
        return [CONSTRUCTION]
    for f in factions:
        if e["id"] == f"mfm:{f['mfm']}:fr":
            return [f"{f['dossier']}/{f['mfm']}-{n}.tsv"
                    for n in ("points", "detachements", "attachements", "options")]
        if e["id"].startswith((f"pdf:pack:{f['id']}:", f"c:40kapp:{f['app40k']}", f"appli:{f['id']}:")):
            return [f"{f['dossier']}/datasheets.md", f"{f['dossier']}/detachements.md"]
    return []


def enregistrer(entrees, chemin, etat, filtres, factions, derives=None):
    aujourdhui = datetime.date.today().isoformat()
    for e in entrees:
        if "erreur" in e or (filtres and not e["id"].startswith(tuple(filtres))):
            continue
        ancien = etat.get(e["id"], {})
        etat[e["id"]] = {
            "libelle": e["libelle"], "type": e["type"], "url": e["url"],
            "version": e["version"], "empreinte": e["empreinte"],
            "consulte_le": aujourdhui,
            "derives": (derives or {}).get(e["id"]) or ancien.get("derives")
                       or derives_par_defaut(e, factions),
        }
    chemin.write_text(json.dumps({"sources": dict(sorted(etat.items()))},
                                 ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def tableau_readme(etat):
    """Tableau de fraîcheur du README. Les entrées « doc: » sont des documents fournis
    par l'utilisateur (captures, extraits de codex) : enregistrées à la main, jamais
    comparées en ligne."""
    ordre = {"officielle": 0, "fournie": 1, "communautaire": 2}
    lignes = ["Généré par `python3 -I outils/veille.py --readme` depuis `sources/etat.json`. "
              "Pour savoir si une source a changé depuis son intégration : `/veille`.", "",
              "| Source | Type | Version | Alimente | Intégrée le |", "|---|---|---|---|---|"]
    for cle, s in sorted(etat.items(), key=lambda kv: (ordre.get(kv[1]["type"], 3), kv[1]["libelle"])):
        alimente = ", ".join(f"`{Path(d).name}`" for d in s.get("derives", [])) or "—"
        date = datetime.date.fromisoformat(s["consulte_le"]).strftime("%d/%m/%Y")
        lignes.append(f"| {s['libelle']} | {s['type']} | {s['version']} | {alimente} | {date} |")
    return "\n".join(lignes)


def ecrire_readme(etat):
    texte = README.read_text(encoding="utf-8")
    debut, fin = MARQUES
    if debut not in texte or fin not in texte:
        raise SystemExit(f"Marqueurs {debut} et {fin} absents de README.md")
    avant, reste = texte.split(debut, 1)
    _, apres = reste.split(fin, 1)
    README.write_text(f"{avant}{debut}\n{tableau_readme(etat)}\n{fin}{apres}", encoding="utf-8")


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
    p.add_argument("--enregistrer", nargs="*", metavar="ID")
    p.add_argument("--js", action="store_true")
    p.add_argument("--extraire", nargs="*", metavar="ID")
    p.add_argument("--navigateur", type=Path, metavar="FICHIER")
    p.add_argument("--appli", action="store_true")
    p.add_argument("--readme", action="store_true")
    p.add_argument("--json", action="store_true")
    p.add_argument("--langue", default="fr")
    p.add_argument("--url", action="append", default=[], metavar="ID=URL")
    p.add_argument("--etat", type=Path, default=ETAT)
    args = p.parse_args()

    urls = dict(u.split("=", 1) for u in args.url)
    factions = [f for _, f in correspondances(factions_actives())]
    etat = json.loads(args.etat.read_text(encoding="utf-8"))["sources"] if args.etat.exists() else {}
    if args.readme:
        ecrire_readme(etat)
        print("Tableau de fraîcheur de README.md régénéré.")
        return 0

    entrees, infos, avertissements = [], [], []
    rassembler, pages = None, {}
    for f in factions:
        try:
            page, entree = verifier_mfm(f, args.langue, urls.get(f["mfm"]))
            pages[f["id"]] = page
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

    if args.js:
        print(JS_40KAPP % json.dumps([{"app40k": f["app40k"], "nom": f["nom"],
                                        "complements": f.get("app40k_complements", [])}
                                       for f in factions], ensure_ascii=False))
        return 0
    if args.navigateur:
        navigateur = json.loads(args.navigateur.read_text(encoding="utf-8"))
        entrees += navigateur
        # 40k.app doit couvrir tous les détachements du Munitorum.
        for f in factions:
            mfm = next((e for e in entrees if e["id"] == f"mfm:{f['mfm']}:{args.langue}"), {})
            nav = next((e for e in navigateur if e["id"] == f"c:40kapp:{f['app40k']}"), {})
            if "detachements" in mfm and "detachements" in nav and mfm["detachements"] != nav["detachements"]:
                avertissements.append(
                    f"40k.app {f['nom']} : {nav['detachements']} détachements, contre "
                    f"{mfm['detachements']} au Munitorum (compléter app40k_complements)")
    appli_verifiee = False
    if args.appli:
        e, a = verifier_appli(factions)
        entrees += e
        avertissements += a
        appli_verifiee = bool(e)
    else:
        avertissements.append("appli non vérifiée : relancer avec --appli (Mac déverrouillé, "
                              "appli connectée)")
    try:
        infos += pr_bsdata()
    except ErreurAcces as e:
        avertissements.append(f"PR BSData non consultées : {e}")
    if not shutil.which("pdftotext"):
        avertissements.append("pdftotext absent : l'intégration des PDF sera impossible "
                              "(brew install poppler)")

    derives = {}
    if args.extraire is not None:
        if args.langue != "fr" or urls:
            raise SystemExit("--extraire ne s'utilise qu'avec le Munitorum français en ligne")
        for f in factions:
            if args.extraire and f["id"] not in args.extraire and f["mfm"] not in args.extraire:
                continue
            try:
                fichiers, compte = extraire(f, pages.get(f["id"]))
            except ErreurAcces as e:
                avertissements.append(f"extraction {f['nom']} impossible : {e}")
                continue
            derives[f"mfm:{f['mfm']}:fr"] = fichiers
            infos.append(f"extrait {f['nom']} : {compte['unites']} unités, {compte['couts']} coûts, "
                         f"{compte['detachements']} détachements, {compte['attachements']} "
                         f"attachements, {compte['options']} options → {', '.join(fichiers)}")
            for g in compte["anomalies"]:
                avertissements.append(f"{f['nom']} : garde du corps « {g} » inconnu, virgule "
                                      "probablement manquante dans le Munitorum (recopié tel quel)")

        if rassembler:
            page = next(iter(pages.values()))
            RASSEMBLER.write_text("\n".join(mfm_rassembler(page)) + "\n", encoding="utf-8")
            fichier = str(RASSEMBLER.relative_to(RACINE))
            derives[rassembler["id"]] = [fichier, CONSTRUCTION]
            infos.append(f"extrait Rassembler les Armées → {fichier}")

    comparer(entrees, etat)
    if args.enregistrer is not None:
        enregistrer(entrees, args.etat, etat, args.enregistrer, factions, derives)
        avertissements.append(f"état enregistré dans {args.etat}")
        detectees = [e["id"] for e in entrees if "erreur" not in e]
        for filtre in args.enregistrer:
            if not any(i.startswith(filtre) for i in detectees):
                avertissements.append(f"--enregistrer : aucune source ne commence par « {filtre} »")

    if args.json:
        print(json.dumps({"sources": entrees, "informations": infos,
                          "avertissements": avertissements}, ensure_ascii=False, indent=2))
    else:
        rapport_texte(entrees, infos, avertissements)

    if any(e["statut"] == "erreur" for e in entrees):
        return 2
    # Sans le relevé de l'appli, rien ne permet d'affirmer que le texte des règles est à jour.
    complet = appli_verifiee
    return 0 if complet and all(e["statut"] == "à jour" for e in entrees) else 1


if __name__ == "__main__":
    sys.exit(main())
