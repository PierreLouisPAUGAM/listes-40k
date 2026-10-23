// Pilotage de l'appli Warhammer 40,000 (« WH 40K », processus w40) par l'accessibilité macOS.
// Mode d'emploi, pièges et limites : README.md du même dossier.
//
// Avant tout
//   verifier                     contrôle et prépare le Mac et l'appli ; « PRÊT » ou « STOP » + action à faire
// Navigation
//   etat                         fenêtre, premier plan, et si l'appli répond
//   placer X Y L H               déplace et redimensionne la fenêtre
//   remplir TEXTE                remplit le champ de recherche (ouvert par la loupe)
//   appuyer LIBELLÉ [N]          appui d'accessibilité sur la N-ième occurrence (1 par défaut)
//   retour                       bouton retour de la barre (son nom varie)
//   fermer                       ferme le menu « Ajouter aux Favoris » ou la recherche
//   accueil                      ramène à la racine de Référence depuis n'importe quel état
//   atteindre LIBELLÉ            descend jusqu'à l'entrée et l'amène à l'écran (listes longues)
//   descendre / monter           défilement d'environ une fenêtre (code 3 au bout de la page)
// Lecture
//   deplier                      déplie toutes les rubriques de la page
//   lire                         toute la page, de haut en bas, une ligne par rangée affichée ;
//                                captures automatiques (PV non exposés, armes à profils) dans
//                                $APPLI_CAPTURES ou un dossier temporaire, chemins dans la sortie
//   ecran                        ce qui est à l'écran, dans l'ordre de lecture
//   capture FICHIER              capture de la fenêtre seule (PNG)
// Secours et diagnostic
//   relancer                     arrête et relance l'appli, passe l'écran d'accueil
//   reveiller                    interroge l'écran point par point (éléments non exposés)
//   cliquer LIBELLÉ [N]          clic souris au centre d'un élément visible
//   action NOM LIBELLÉ [N]       action d'accessibilité brute (AXPress, AXScrollToVisible…)
//   arbre                        arbre d'accessibilité : rôle, texte, cadre
//
// La souris (clic, molette) exige le premier plan : l'outil met l'appli devant et refuse
// d'agir s'il n'y parvient pas. Tout le reste fonctionne avec l'appli en arrière-plan.
// TRACE=1 dans l'environnement affiche le détail des opérations sur la sortie d'erreur.

import AppKit
import ApplicationServices

func sortir(_ message: String, code: Int32 = 1) -> Never {
    FileHandle.standardError.write((message + "\n").data(using: .utf8)!)
    exit(code)
}

let traceActive = ProcessInfo.processInfo.environment["TRACE"] != nil
func trace(_ m: String) { if traceActive { FileHandle.standardError.write(("· " + m + "\n").data(using: .utf8)!) } }

func trouverAppli() -> NSRunningApplication? {
    NSWorkspace.shared.runningApplications.first { $0.executableURL?.lastPathComponent == "w40" }
}

let cheminAppli = "/Applications/WH 40K.app"

func lancer(_ chemin: String, _ arguments: [String], attendre: Bool = true) {
    let p = Process()
    p.executableURL = URL(fileURLWithPath: chemin)
    p.arguments = arguments
    // Un processus laissé en marche (caffeinate) ne doit pas garder la sortie de l'outil ouverte.
    if !attendre { p.standardOutput = FileHandle.nullDevice; p.standardError = FileHandle.nullDevice }
    try? p.run()
    if attendre { p.waitUntilExit() }
}

// Vrai si l'appli répond à l'accessibilité (une appli bloquée renvoie « impossible de terminer »).
func repond(_ a: NSRunningApplication) -> Bool {
    var v: CFTypeRef?
    return AXUIElementCopyAttributeValue(AXUIElementCreateApplication(a.processIdentifier),
                                         kAXWindowsAttribute as CFString, &v) != .cannotComplete
}

// Arrête l'appli si elle tourne, la relance et passe l'écran d'accueil (« Continuer avec la
// version gratuite », qui ne touche pas à l'abonnement). Renvoie un compte rendu.
func relancerAppli() -> String {
    if let a = trouverAppli() {
        kill(a.processIdentifier, SIGTERM)
        for _ in 0..<50 where trouverAppli() != nil { usleep(200_000) }
        if let a = trouverAppli() { kill(a.processIdentifier, SIGKILL); usleep(1_000_000) }
    }
    lancer("/usr/bin/open", ["-a", cheminAppli])
    for _ in 0..<40 {
        usleep(500_000)
        guard let a = trouverAppli() else { continue }
        var v: CFTypeRef?
        guard AXUIElementCopyAttributeValue(AXUIElementCreateApplication(a.processIdentifier),
                                            kAXWindowsAttribute as CFString, &v) == .success,
              let f = (v as? [AXUIElement])?.first else { continue }
        var pile = [f]
        while let e = pile.popLast() {
            var d: CFTypeRef?
            AXUIElementCopyAttributeValue(e, kAXDescriptionAttribute as CFString, &d)
            if (d as? String) == "CONTINUER AVEC LA VERSION GRATUITE" {
                AXUIElementPerformAction(e, kAXPressAction as CFString)
                usleep(1_500_000)
                return "relancée, écran d'accueil passé"
            }
            var c: CFTypeRef?
            AXUIElementCopyAttributeValue(e, kAXChildrenAttribute as CFString, &c)
            pile += (c as? [AXUIElement]) ?? []
        }
    }
    return "relancée (écran d'accueil non rencontré)"
}

let args = Array(CommandLine.arguments.dropFirst())
guard let commande = args.first else { sortir("commande manquante (voir l'en-tête de appli.swift)") }

// Contrôles qui précèdent tout accès à l'appli : `verifier` les rapporte un par un et s'arrête
// sur le premier qui demande une action de l'utilisateur.
if commande == "verifier" {
    func ok(_ m: String) { print("ok   \(m)") }
    func bloque(_ m: String) -> Never { print("STOP \(m)"); exit(5) }
    if !AXIsProcessTrusted() {
        bloque("le terminal n'a pas l'autorisation d'accessibilité (Réglages > Confidentialité > Accessibilité)")
    }
    ok("autorisation d'accessibilité")
    if !CGPreflightScreenCaptureAccess() {
        bloque("le terminal n'a pas l'autorisation d'enregistrement de l'écran (Réglages > Confidentialité)")
    }
    ok("autorisation d'enregistrement de l'écran")
    let session = CGSessionCopyCurrentDictionary() as? [String: Any] ?? [:]
    if (session["CGSSessionScreenIsLocked"] as? Bool) == true {
        bloque("le Mac est verrouillé : le déverrouiller (à distance depuis l'iPhone)")
    }
    if CGDisplayIsAsleep(CGMainDisplayID()) != 0 {
        bloque("l'écran est en veille : le réveiller")
    }
    ok("session déverrouillée, écran allumé")
    // Veille : caffeinate pour 2 h s'il ne tourne pas déjà.
    let pg = Process(), tuyau = Pipe()
    // Seul un caffeinate avec -d empêche la veille de l'écran ; d'autres programmes en lancent sans.
    pg.executableURL = URL(fileURLWithPath: "/usr/bin/pgrep"); pg.arguments = ["-f", "caffeinate -d"]
    pg.standardOutput = tuyau; try? pg.run(); pg.waitUntilExit()
    if pg.terminationStatus == 0 { ok("caffeinate déjà actif") }
    else { lancer("/usr/bin/caffeinate", ["-d", "-i", "-t", "7200"], attendre: false); ok("caffeinate lancé pour 2 h") }
    if trouverAppli() == nil {
        lancer("/usr/bin/open", ["-a", cheminAppli]); sleep(8)
        guard trouverAppli() != nil else { bloque("l'appli ne se lance pas (« \(cheminAppli) » absente ?)") }
        ok("appli lancée")
    }
    if !repond(trouverAppli()!) {
        print("…    l'appli ne répond pas : \(relancerAppli())")
        if !repond(trouverAppli()!) {
            bloque("l'appli ne répond toujours pas : fenêtre système probable par-dessus (autorisation macOS) ; regarder l'écran du Mac")
        }
    }
    ok("l'appli répond")
}

if commande == "relancer" { print(relancerAppli()); exit(0) }

guard AXIsProcessTrusted() else { sortir("accessibilité non autorisée pour ce terminal") }
guard let appli = trouverAppli() else { sortir("appli non lancée") }
let racine = AXUIElementCreateApplication(appli.processIdentifier)

func attribut<T>(_ e: AXUIElement, _ nom: String) -> T? {
    var v: CFTypeRef?
    guard AXUIElementCopyAttributeValue(e, nom as CFString, &v) == .success else { return nil }
    return v as? T
}

func cadre(_ e: AXUIElement) -> CGRect? {
    var p: CFTypeRef?, t: CFTypeRef?
    guard AXUIElementCopyAttributeValue(e, kAXPositionAttribute as CFString, &p) == .success,
          AXUIElementCopyAttributeValue(e, kAXSizeAttribute as CFString, &t) == .success,
          let p, let t, CFGetTypeID(p) == AXValueGetTypeID(), CFGetTypeID(t) == AXValueGetTypeID()
    else { return nil }
    var point = CGPoint.zero, taille = CGSize.zero
    // Certains éléments ont des coordonnées non numériques : on les ignore.
    guard AXValueGetValue(p as! AXValue, .cgPoint, &point),
          AXValueGetValue(t as! AXValue, .cgSize, &taille),
          point.x.isFinite, point.y.isFinite, taille.width.isFinite, taille.height.isFinite
    else { return nil }
    return CGRect(origin: point, size: taille)
}

func libelle(_ e: AXUIElement) -> String {
    if let v: String = attribut(e, kAXValueAttribute), !v.isEmpty { return v }
    if let d: String = attribut(e, kAXDescriptionAttribute), !d.isEmpty { return d }
    if let t: String = attribut(e, kAXTitleAttribute), !t.isEmpty { return t }
    return ""
}

func fenetre() -> AXUIElement {
    var v: CFTypeRef?
    let r = AXUIElementCopyAttributeValue(racine, kAXWindowsAttribute as CFString, &v)
    if r == .cannotComplete { sortir("l'appli ne répond pas à l'accessibilité (bloquée ?) : lancer « relancer »", code: 4) }
    guard let f = (v as? [AXUIElement])?.first else { sortir("aucune fenêtre (écran d'accueil ou fenêtre fermée ?)") }
    return f
}

struct Noeud { let element: AXUIElement; let profondeur: Int; let role: String; let texte: String }

func parcourir(_ e: AXUIElement, _ profondeur: Int, _ acc: inout [Noeud]) {
    let role: String = attribut(e, kAXRoleAttribute) ?? "?"
    acc.append(Noeud(element: e, profondeur: profondeur, role: role, texte: libelle(e)))
    for enfant in (attribut(e, kAXChildrenAttribute) as [AXUIElement]?) ?? [] {
        parcourir(enfant, profondeur + 1, &acc)
    }
}

func noeuds() -> [Noeud] { var acc: [Noeud] = []; parcourir(fenetre(), 0, &acc); return acc }

func trouver(_ cible: String, _ rang: Int) -> AXUIElement {
    let candidats = noeuds().filter { $0.texte == cible }
    guard candidats.count >= rang else { sortir("introuvable : \(cible) (\(candidats.count) occurrence(s))") }
    return candidats[rang - 1].element
}

func auPremierPlan() {
    // NSRunningApplication.activate est refusé à un outil en ligne de commande : on passe par open.
    let p = Process()
    p.executableURL = URL(fileURLWithPath: "/usr/bin/open")
    p.arguments = ["-a", appli.bundleURL!.path]
    try? p.run(); p.waitUntilExit()
    for _ in 0..<10 {
        if NSWorkspace.shared.frontmostApplication?.processIdentifier == appli.processIdentifier { return }
        usleep(100_000)
    }
    sortir("refusé : l'appli n'est pas au premier plan")
}

func souris(_ type: CGEventType, _ point: CGPoint) {
    CGEvent(mouseEventSource: nil, mouseType: type, mouseCursorPosition: point, mouseButton: .left)?.post(tap: .cghidEventTap)
}

func molette(_ pixels: Int32) {
    auPremierPlan()
    let cf = cadre(fenetre())!
    souris(.mouseMoved, CGPoint(x: cf.midX, y: cf.midY))
    CGEvent(scrollWheelEvent2Source: nil, units: .pixel, wheelCount: 1, wheel1: pixels, wheel2: 0, wheel3: 0)?.post(tap: .cghidEventTap)
}

// Clic souris au centre d'un élément, seulement si le point est dans la zone de contenu de la
// fenêtre (sous la barre de navigation). Renvoie faux si l'élément est hors zone.
func cliquerElement(_ e: AXUIElement) -> Bool {
    auPremierPlan()
    guard let c = cadre(e), let cf = cadre(fenetre()) else { return false }
    let zone = CGRect(x: cf.minX, y: cf.minY + 130, width: cf.width, height: cf.height - 140)
    let centre = CGPoint(x: c.midX, y: c.midY)
    guard zone.contains(centre) else { return false }
    souris(.mouseMoved, centre); usleep(100_000)
    souris(.leftMouseDown, centre); usleep(50_000)
    souris(.leftMouseUp, centre)
    return true
}

func identifiantFenetre() -> Int {
    // L'appli possède d'autres fenêtres invisibles : on vise celle qui porte le titre « WH 40K ».
    let liste = CGWindowListCopyWindowInfo(.optionAll, kCGNullWindowID) as? [[String: Any]] ?? []
    for w in liste where (w[kCGWindowOwnerPID as String] as? Int32) == appli.processIdentifier
        && (w[kCGWindowName as String] as? String) == "WH 40K" {
        if let n = w[kCGWindowNumber as String] as? Int { return n }
    }
    sortir("identifiant de fenêtre introuvable")
}

// Captures produites par `lire` : dossier $APPLI_CAPTURES, sinon un dossier temporaire.
let dossierCaptures: String = {
    let d = ProcessInfo.processInfo.environment["APPLI_CAPTURES"] ?? (NSTemporaryDirectory() + "appli-captures")
    try? FileManager.default.createDirectory(atPath: d, withIntermediateDirectories: true)
    return d
}()
var numeroCapture = 0
func capturer(_ zone: CGRect?, _ nom: String) -> String {
    numeroCapture += 1
    let horodatage = Int(Date().timeIntervalSince1970)
    let chemin = "\(dossierCaptures)/\(horodatage)-\(numeroCapture)-\(nom).png"
    var arguments = ["-x", "-o"]
    if let z = zone { arguments.append("-R\(Int(z.minX)),\(Int(z.minY)),\(Int(z.width)),\(Int(z.height))") }
    else { arguments.append("-l\(identifiantFenetre())") }
    lancer("/usr/sbin/screencapture", arguments + [chemin])
    return chemin
}

// Éléments de la barre de navigation et de la fenêtre, jamais pris pour du contenu.
let libellesBarre: Set<String> = ["Précédent", "Overflow", "Effacer le texte", "WH 40K"]
func estBarre(_ n: Noeud) -> Bool {
    libellesBarre.contains(n.texte) || n.texte.hasPrefix("Recherche de Référence")
        || n.role == "AXRadioButton" || (n.role == "AXButton" && n.texte.isEmpty)
}

// Défilement. AXScrollUpByPage / AXScrollDownByPage bloquent l'appli sur certains éléments
// (constaté le 22/10/2026) : on ne s'en sert jamais. On amène à l'écran l'élément chargé le
// plus haut (ou le plus bas) ; l'appli garde un peu de contenu hors de la fenêtre, la page
// avance donc d'à peu près une hauteur de fenêtre. Dans une liste, rien n'est chargé hors de
// la fenêtre : on passe alors à la molette (premier plan). Renvoie vrai si la page a bougé.
func amener(versLeHaut: Bool) -> Bool {
    let cf = cadre(fenetre())!
    let types: Set<String> = ["AXStaticText", "AXGenericElement", "AXHeading", "AXImage", "AXButton"]
    let charges = noeuds().compactMap { n -> (Noeud, CGRect)? in
        guard types.contains(n.role), !estBarre(n), let c = cadre(n.element) else { return nil }
        if abs(c.minY - cf.minY) < 20 { return nil }                     // barre de titre
        if n.role == "AXHeading" && n.texte != "Déplié" { return nil }   // titre fixe de la barre
        return (n, c)
    }
    guard let cible = versLeHaut ? charges.min(by: { $0.1.minY < $1.1.minY })
                                 : charges.max(by: { $0.1.maxY < $1.1.maxY }) else { return false }
    trace("AXScrollToVisible sur « \(cible.0.texte.prefix(30)) » à \(Int(cible.1.minY))")
    AXUIElementPerformAction(cible.0.element, "AXScrollToVisible" as CFString)
    usleep(500_000)
    if abs((cadre(cible.0.element)?.minY ?? cible.1.minY) - cible.1.minY) > 1 { return true }
    let avant = cadre(cible.0.element)?.minY ?? cible.1.minY
    molette(Int32(cf.height * 0.8) * (versLeHaut ? 1 : -1))
    usleep(700_000)
    let apres = cadre(cible.0.element)?.minY
    trace("molette : élément de \(Int(avant)) à \(apres.map { String(Int($0)) } ?? "disparu")")
    return apres.map { abs($0 - avant) > 1 } ?? true
}

// Ramène à la racine de Référence depuis n'importe quel état : menu ouvert (on l'annule),
// recherche en calque quand le champ contient du texte (on la ferme), page de recherche ou
// page profonde (on revient), puis onglet Référence.
func allerAccueil() -> Bool {
    let cf = cadre(fenetre())!
    for _ in 0..<15 {
        let tous = noeuds()
        if let item = tous.first(where: { $0.role == "AXMenuItem" }) {
            AXUIElementPerformAction(item.element, kAXCancelAction as CFString); usleep(800_000); continue
        }
        if let champ = tous.first(where: { $0.role == "AXTextField" }), !champ.texte.isEmpty,
           champ.texte != "Commencez la Saisie..." {
            AXUIElementPerformAction(champ.element, kAXCancelAction as CFString); usleep(1_000_000); continue
        }
        if let b = tous.first(where: { n in n.role == "AXButton" && !n.texte.isEmpty
            && (cadre(n.element).map { $0.minX < cf.minX + 40 && $0.minY < cf.minY + 80 } ?? false) }) {
            AXUIElementPerformAction(b.element, kAXPressAction as CFString); usleep(1_200_000); continue
        }
        if let onglet = tous.first(where: { $0.role == "AXRadioButton" && $0.texte == "RÉFÉRENCE" }) {
            AXUIElementPerformAction(onglet.element, kAXPressAction as CFString); usleep(800_000)
        }
        return true
    }
    return false
}

// Rangées affichées dans la fenêtre : éléments triés par position, regroupés par ligne (4 px).
func lignesEcran() -> [String] {
    let cf = cadre(fenetre())!
    let roles: Set<String> = ["AXStaticText", "AXHeading", "AXButton", "AXGenericElement", "AXPopUpButton"]
    let vis = noeuds().compactMap { n -> (Noeud, CGRect)? in
        guard roles.contains(n.role), !n.texte.isEmpty, n.texte != "Déplié", !estBarre(n),
              let c = cadre(n.element), c.minY > cf.minY + 120, c.minY < cf.maxY else { return nil }
        if n.role == "AXHeading" && c.minY < cf.minY + 130 { return nil }   // titre de la barre
        return (n, c)
    }.sorted { abs($0.1.minY - $1.1.minY) > 4 ? $0.1.minY < $1.1.minY : $0.1.minX < $1.1.minX }
    var lignes: [String] = [], courante: [String] = [], y = -CGFloat.infinity
    for (n, c) in vis {
        var t = n.texte
        // Résumé de caractéristiques faux : l'appli n'expose pas les cases, les PV se lisent sur capture.
        if t.contains("%wounds@") { t = "⚠ PV non exposés par l'appli : les lire sur une capture | " + t }
        if c.minY - y > 4, !courante.isEmpty { lignes.append(courante.joined(separator: " | ")); courante = [] }
        if courante.isEmpty { y = c.minY }
        if courante.last != t { courante.append(t) }
    }
    if !courante.isEmpty { lignes.append(courante.joined(separator: " | ")) }
    return lignes
}

switch commande {
case "verifier":
    // Suite des contrôles (la partie qui précède l'accès à l'appli est en tête de fichier).
    func ok(_ m: String) { print("ok   \(m)") }
    func bloque(_ m: String) -> Never { print("STOP \(m)"); exit(5) }
    if noeuds().contains(where: { $0.texte == "CONTINUER AVEC LA VERSION GRATUITE" }) {
        AXUIElementPerformAction(trouver("CONTINUER AVEC LA VERSION GRATUITE", 1), kAXPressAction as CFString)
        sleep(2); ok("écran d'accueil passé (version gratuite)")
    }
    // Fenêtre : pleine hauteur de son écran, 1 024 de large (la colonne de contenu est fixe).
    let f = fenetre(), cf = cadre(f)!
    let principal = NSScreen.screens[0].frame.height
    let ecranFenetre = NSScreen.screens.first { s in
        let v = s.frame
        let haut = principal - v.maxY
        return CGRect(x: v.minX, y: haut, width: v.width, height: v.height).contains(CGPoint(x: cf.midX, y: cf.midY))
    } ?? NSScreen.screens[0]
    let v = ecranFenetre.visibleFrame
    var p = CGPoint(x: v.minX + (v.width - 1024) / 2, y: principal - v.maxY), t = CGSize(width: 1024, height: v.height)
    if abs(cf.height - v.height) > 40 || abs(cf.width - 1024) > 2 {
        AXUIElementSetAttributeValue(f, kAXPositionAttribute as CFString, AXValueCreate(.cgPoint, &p)!)
        AXUIElementSetAttributeValue(f, kAXSizeAttribute as CFString, AXValueCreate(.cgSize, &t)!)
        usleep(500_000)
    }
    let cf2 = cadre(fenetre())!
    ok("fenêtre \(Int(cf2.width))x\(Int(cf2.height))")
    // Compte : l'onglet Profil affiche « Déconnexion » quand on est connecté.
    guard allerAccueil() else { bloque("navigation impossible jusqu'à la racine de Référence") }
    guard let profil = noeuds().first(where: { $0.role == "AXRadioButton" && $0.texte == "PROFIL" })
    else { bloque("onglet Profil introuvable : structure de l'appli inattendue") }
    AXUIElementPerformAction(profil.element, kAXPressAction as CFString); sleep(2)
    let page = noeuds()
    let connecte = page.contains { $0.texte == "Déconnexion" }
    let version = page.first { $0.texte.hasPrefix("Version des Données") }?.texte ?? "version des données non lue"
    _ = allerAccueil()
    if !connecte { bloque("compte Warhammer déconnecté : se reconnecter dans l'appli (identifiants)") }
    ok("compte connecté ; \(version)")
    print("PRÊT")

case "etat":
    let c = cadre(fenetre())!
    let devant = NSWorkspace.shared.frontmostApplication?.processIdentifier == appli.processIdentifier
    print("fenêtre \(Int(c.minX)),\(Int(c.minY)) \(Int(c.width))x\(Int(c.height)) ; premier plan \(devant ? "oui" : "non") ; répond")

case "placer":
    guard args.count == 5, let x = Double(args[1]), let y = Double(args[2]),
          let l = Double(args[3]), let h = Double(args[4]) else { sortir("usage : placer X Y L H") }
    var p = CGPoint(x: x, y: y), t = CGSize(width: l, height: h)
    let f = fenetre()
    AXUIElementSetAttributeValue(f, kAXPositionAttribute as CFString, AXValueCreate(.cgPoint, &p)!)
    AXUIElementSetAttributeValue(f, kAXSizeAttribute as CFString, AXValueCreate(.cgSize, &t)!)
    let c = cadre(f)!
    print("fenêtre \(Int(c.minX)),\(Int(c.minY)) \(Int(c.width))x\(Int(c.height))")

case "remplir":
    guard args.count == 2 else { sortir("usage : remplir TEXTE") }
    guard let champ = noeuds().first(where: { $0.role == "AXTextField" })
    else { sortir("aucun champ de saisie : ouvrir d'abord la recherche (appuyer « Recherche de Référence : Bouton »)") }
    let r = AXUIElementSetAttributeValue(champ.element, kAXValueAttribute as CFString, args[1] as CFString)
    print(r == .success ? "rempli : \(args[1])" : "échec du remplissage (\(r.rawValue))")

case "appuyer":
    guard args.count >= 2 else { sortir("usage : appuyer LIBELLÉ [N]") }
    let e = trouver(args[1], args.count > 2 ? Int(args[2]) ?? 1 : 1)
    if (attribut(e, kAXRoleAttribute) as String?) == "AXPopUpButton" && args[1] != "Overflow" {
        sortir("refusé : un appui sur un menu déroulant ouvre « Ajouter aux Favoris » ; utiliser deplier")
    }
    let r = AXUIElementPerformAction(e, kAXPressAction as CFString)
    print(r == .success ? "appuyé : \(args[1])" : "échec de l'appui (\(r.rawValue)) : \(args[1])")

case "retour":
    // Le bouton retour porte le nom de la page parente : on le repère à sa place, en haut à gauche.
    let cf = cadre(fenetre())!
    guard let b = noeuds().first(where: { n in n.role == "AXButton" && !n.texte.isEmpty
        && (cadre(n.element).map { $0.minX < cf.minX + 40 && $0.minY < cf.minY + 80 } ?? false) })
    else { sortir("pas de bouton retour (page racine, ou recherche ouverte : « fermer »)") }
    AXUIElementPerformAction(b.element, kAXPressAction as CFString)
    print("retour (\(b.texte))")

case "fermer":
    // AXCancel referme le menu des favoris, ou la recherche, sans clavier.
    let tous = noeuds()
    if let item = tous.first(where: { $0.role == "AXMenuItem" }) {
        AXUIElementPerformAction(item.element, kAXCancelAction as CFString); print("menu fermé")
    } else if let champ = tous.first(where: { $0.role == "AXTextField" }) {
        AXUIElementPerformAction(champ.element, kAXCancelAction as CFString); print("recherche fermée")
    } else { print("rien à fermer") }

case "accueil":
    if allerAccueil() { print("accueil : racine de Référence") } else { sortir("accueil : racine non atteinte après 15 étapes") }

case "atteindre":
    // Descend jusqu'à ce que l'élément soit chargé, puis l'amène à l'écran. Les listes ne
    // chargent que ce qui est autour de la fenêtre : un libellé introuvable peut être plus bas.
    guard args.count == 2 else { sortir("usage : atteindre LIBELLÉ") }
    var immobile = 0
    for _ in 0..<60 {
        if let n = noeuds().first(where: { $0.texte == args[1] }) {
            AXUIElementPerformAction(n.element, "AXScrollToVisible" as CFString)
            print("atteint : \(args[1])"); exit(0)
        }
        immobile = amener(versLeHaut: false) ? 0 : immobile + 1
        if immobile >= 2 { break }
    }
    sortir("introuvable jusqu'en bas de la page : \(args[1])")

case "descendre", "monter":
    if amener(versLeHaut: commande == "monter") { print("\(commande) : ok") } else { print("\(commande) : bout de page"); exit(3) }

case "deplier":
    // Rien à faire sur une page sans rubriques (liste, index) : on ne la parcourt pas.
    guard noeuds().contains(where: { ($0.role == "AXHeading" && $0.texte == "Déplié")
        || ($0.role == "AXPopUpButton" && ($0.texte.hasSuffix("Replier") || $0.texte.hasSuffix("Déplié"))) })
    else { print("aucune rubrique sur cette page"); exit(0) }
    // 1) Rubriques en menu déroulant (règles, optimisations, stratagèmes, Règles de Base) : leur
    //    libellé finit par « Replier » quand elles sont fermées et « Déplié » quand elles sont
    //    ouvertes. Elles ne s'ouvrent qu'au clic souris (l'appui ouvre le menu des favoris).
    var clics = 0, bloque = 0
    for _ in 0..<80 where clics < 60 {
        let fermees = noeuds().filter { $0.role == "AXPopUpButton" && $0.texte.hasSuffix("Replier") }
            .compactMap { n in cadre(n.element).map { (n, $0) } }.sorted { $0.1.minY < $1.1.minY }
        if let f = fermees.first {
            if !cliquerElement(f.0.element) {
                AXUIElementPerformAction(f.0.element, "AXScrollToVisible" as CFString); usleep(400_000)
                if !cliquerElement(f.0.element) { bloque += 1; if bloque > 3 { break }; continue }
            }
            trace("clic sur « \(f.0.texte) »"); clics += 1; bloque = 0; usleep(700_000); continue
        }
        if !amener(versLeHaut: false) { break }
    }
    if clics > 0 { print("menus dépliés : \(clics)") }

    // 2) Rubriques de fiche : les titres s'appellent tous « Déplié » quel que soit leur état, et
    //    ceux qui sont loin de l'écran n'existent pas dans l'arbre. On n'appuie que sur preuve
    //    qu'une rubrique est repliée : le titre suivant la touche directement. Le dernier titre
    //    n'a pas de suivant : en bas de page, on l'appuie une fois s'il n'est suivi de rien.
    func titres() -> [(Noeud, CGRect)] {
        noeuds().filter { $0.role == "AXHeading" && $0.texte == "Déplié" }
            .compactMap { n in cadre(n.element).map { (n, $0) } }.sorted { $0.1.minY < $1.1.minY }
    }
    func suivant(_ t: AXUIElement) -> CGFloat? {
        let y = cadre(t)?.minY ?? 0
        return titres().first { $0.1.minY > y + 1 }?.1.minY
    }
    var appuis = 0, immobile = 0
    var inertes: [AXUIElement] = []
    for _ in 0..<80 where appuis < 30 {
        let ts = titres()
        if let i = ts.indices.dropLast().first(where: { i in
            ts[i + 1].1.minY - ts[i].1.maxY < 3 && !inertes.contains { CFEqual($0, ts[i].0.element) } }) {
            let titre = ts[i].0.element
            AXUIElementPerformAction(titre, "AXScrollToVisible" as CFString); usleep(300_000)
            let hauteurAvant = cadre(titre)?.height, suivantAvant = suivant(titre)
            AXUIElementPerformAction(titre, kAXPressAction as CFString); usleep(700_000)
            // Certaines lignes (« Endommagé ») sont exposées comme des titres mais ne se déplient
            // pas : si l'appui ne change rien, on ne les touche plus.
            if let a = suivantAvant, let b = suivant(titre), abs(a - b) < 2, cadre(titre)?.height == hauteurAvant {
                trace("titre inerte, ignoré"); inertes.append(titre); continue
            }
            trace("rubrique dépliée"); appuis += 1; continue
        }
        immobile = amener(versLeHaut: false) ? 0 : immobile + 1
        if immobile >= 2 {
            let contenu: Set<String> = ["AXStaticText", "AXGenericElement", "AXButton"]
            if let d = titres().last, !noeuds().contains(where: { n in
                contenu.contains(n.role) && !n.texte.isEmpty && (cadre(n.element).map { $0.minY >= d.1.maxY - 1 } ?? false) }) {
                trace("dernière rubrique dépliée")
                AXUIElementPerformAction(d.0.element, kAXPressAction as CFString); usleep(700_000)
                appuis += 1
            }
            break
        }
    }
    if appuis > 0 || clics == 0 { print("rubriques dépliées : \(appuis)") }

case "lire":
    // Remonte en haut, puis descend écran par écran. Deux écrans successifs se chevauchent : on
    // les raccorde par leur plus long recouvrement (les positions « dans la page » ne sont pas
    // fiables, le repère change quand la page grandit).
    let cf = cadre(fenetre())!
    for _ in 0..<40 { if !amener(versLeHaut: true) { break } }
    // Les titres en menu déroulant restent collés en haut pendant le défilement : il n'y a plus
    // d'élément au-dessus à amener. On finit à la molette (ces pages exigent déjà la souris).
    if noeuds().contains(where: { $0.role == "AXPopUpButton" && $0.texte != "Overflow" }) {
        for _ in 0..<30 {
            let premier = noeuds().first { $0.role == "AXPopUpButton" && $0.texte != "Overflow" }
            let avant = premier.flatMap { cadre($0.element)?.minY }
            molette(Int32(cf.height)); usleep(400_000)
            if let a = avant, let b = premier.flatMap({ cadre($0.element)?.minY }), abs(a - b) < 1 { break }
        }
    }
    var acc: [String] = [], immobile = 0
    var capturePV: String?, capturesProfils: [String] = []
    for _ in 0..<80 {
        // Résumé de caractéristiques faux : on capture la ligne de caractéristiques dès qu'elle
        // est entièrement visible. Arme à profils : on capture l'écran qui montre sa note.
        let tous = noeuds()
        if capturePV == nil, let n = tous.first(where: { $0.texte.contains("%wounds@") }),
           let c = cadre(n.element), c.minY > cf.minY + 120, c.maxY < cf.maxY {
            capturePV = capturer(c.insetBy(dx: 0, dy: -4), "caracteristiques")
        }
        if capturesProfils.isEmpty, tous.contains(where: { $0.texte.hasPrefix("Avant de choisir des cibles pour cette arme") }) {
            capturesProfils.append(capturer(nil, "armes"))
        }
        let ecran = lignesEcran()
        // Plus long recouvrement entre la fin de ce qui est lu et un bloc de l'écran, où qu'il
        // commence : la page avance parfois de peu, et un titre de menu peut rester collé en haut.
        // On exige au moins trois lignes communes : des lignes isolées (« Historique », nom du
        // détachement) se répètent d'une rubrique à l'autre. Un recouvrement plus court suffit
        // s'il est long (une arme tient en un seul élément) et n'apparaît qu'une fois.
        func recouvrementSur(_ acc: [String], _ k: Int) -> Bool {
            guard k > 0 else { return false }
            let bloc = Array(acc.suffix(k))
            guard bloc.joined().count >= 60 else { return false }
            let occurrences = (0...(acc.count - k)).filter { Array(acc[$0..<($0 + k)]) == bloc }.count
            return occurrences == 1
        }
        var meilleur: (j: Int, k: Int) = (0, 0)
        for j in 0...ecran.count {
            var k = min(acc.count, ecran.count - j)
            while k > 0 && Array(acc.suffix(k)) != Array(ecran[j..<(j + k)]) { k -= 1 }
            if k > meilleur.k { meilleur = (j, k) }
        }
        let minimum = min(3, ecran.count)
        trace("écran de \(ecran.count) lignes ; recouvrement \(meilleur.k) à partir de \(meilleur.j) ; fin lue : « \(acc.last?.prefix(40) ?? "") » ; début écran : « \(ecran.first?.prefix(40) ?? "") »")
        if traceActive { for l in ecran { trace("   | \(l.prefix(60))") } }
        if acc.isEmpty {
            acc = ecran
        } else if meilleur.k >= minimum && minimum > 0 || recouvrementSur(acc, meilleur.k) {
            // Titre collé en tête d'écran : on ne l'ajoute que s'il n'a pas encore été lu.
            acc += ecran[..<meilleur.j].filter { !acc.contains($0) }
            acc += ecran[(meilleur.j + meilleur.k)...]
        } else if !ecran.isEmpty {
            acc.append("⚠ raccord incertain entre deux écrans : vérifier sur capture")
            acc += ecran
        }
        immobile = amener(versLeHaut: false) ? 0 : immobile + 1
        if immobile >= 2 { break }
    }
    // PV : on remplace l'avertissement par le chemin de la capture.
    if let c = capturePV {
        acc = acc.map { $0.replacingOccurrences(of: "les lire sur une capture", with: "les lire sur la capture \(c)") }
    }
    // Armes à profils : l'appli expose « Armes de Tir - Frag. » sans le nom de l'arme. On repère
    // les noms d'armes absents de l'équipement et des options, et on propose comme arme parente
    // les équipements qui n'ont pas de ligne d'arme à leur nom.
    func nomArme(_ l: String) -> String? {
        for prefixe in ["Armes de Tir -", "Armes de Mêlée -"] where l.hasPrefix(prefixe) {
            var n = String(l.dropFirst(prefixe.count)).trimmingCharacters(in: .whitespaces)
            if let fin = n.firstIndex(of: "\n") { n = String(n[..<fin]) }
            while n.hasSuffix(".") { n.removeLast() }
            return n.trimmingCharacters(in: .whitespaces)
        }
        return nil
    }
    let armes = acc.compactMap(nomArme)
    // Sources des noms d'équipement : ce qui suit « équipée de : », et les lignes d'options.
    var lignesEquipement: [String] = []
    for l in acc {
        let espaces = l.replacingOccurrences(of: "\u{202F}", with: " ").replacingOccurrences(of: "\u{00A0}", with: " ")
        for sous in espaces.components(separatedBy: "\n") {
            // L'espace avant les deux-points est souvent insécable.
            if let r = sous.range(of: "équipée de[\\s\u{00A0}\u{202F}]*:", options: .regularExpression) {
                lignesEquipement.append(String(sous[r.upperBound...]))
            }
            else if sous.hasPrefix("■") || sous.hasPrefix("▫") { lignesEquipement.append(sous) }
        }
    }
    var equipements: [String] = []
    for l in lignesEquipement {
        let morceaux = l.components(separatedBy: CharacterSet(charactersIn: ";:"))
        for m in morceaux {
            guard let r = m.range(of: #"(?:^|\s|par )1 ([^;.\n]+)"#, options: .regularExpression) else { continue }
            var nom = String(m[r]).replacingOccurrences(of: "par ", with: "").trimmingCharacters(in: .whitespaces)
            if nom.hasPrefix("1 ") { nom.removeFirst(2) }
            nom = nom.trimmingCharacters(in: .whitespacesAndNewlines)
            if !nom.isEmpty && !equipements.contains(nom) { equipements.append(nom) }
        }
    }
    // Comparaison insensible à la casse et aux espaces insécables, que l'appli mêle aux espaces.
    func norme(_ t: String) -> String {
        t.replacingOccurrences(of: "\u{202F}", with: " ").replacingOccurrences(of: "\u{00A0}", with: " ")
            .split(separator: " ").joined(separator: " ").lowercased()
    }
    let connus = Set(equipements.map(norme))
    let profils = armes.filter { !connus.contains(norme($0)) }
    if !equipements.isEmpty && !profils.isEmpty {
        let armesMin = Set(armes.map(norme))
        let parents = equipements.filter { !armesMin.contains(norme($0)) }
        acc.append("⚠ armes à profils, nom de l'arme non exposé par l'appli : \(profils.joined(separator: ", "))"
            + " ; arme parente probable : \(parents.isEmpty ? "non déduite" : parents.joined(separator: " ou "))"
            + (capturesProfils.isEmpty ? " ; vérifier sur capture" : " ; captures : \(capturesProfils.joined(separator: ", "))"))
    }
    print(acc.joined(separator: "\n"))

case "ecran":
    print(lignesEcran().joined(separator: "\n"))

case "capture":
    guard args.count == 2 else { sortir("usage : capture FICHIER") }
    let p = Process()
    p.executableURL = URL(fileURLWithPath: "/usr/sbin/screencapture")
    p.arguments = ["-x", "-o", "-l\(identifiantFenetre())", args[1]]
    try! p.run(); p.waitUntilExit()
    print(p.terminationStatus == 0 ? "capture : \(args[1])" : "échec de la capture")

case "reveiller":
    // Certains éléments n'apparaissent dans l'arbre qu'après une interrogation à leur position ;
    // ils y restent ensuite. Constaté une fois (tableau des points de l'Infiltrator).
    let cf = cadre(fenetre())!
    var n = 0
    for y in stride(from: cf.minY + 130, to: cf.maxY, by: 20) {
        for x in stride(from: cf.midX - 240, to: cf.midX + 240, by: 40) {
            var e: AXUIElement?
            _ = AXUIElementCopyElementAtPosition(racine, Float(x), Float(y), &e); n += 1
        }
    }
    print("\(n) points interrogés")

case "cliquer":
    guard args.count >= 2 else { sortir("usage : cliquer LIBELLÉ [N]") }
    let e = trouver(args[1], args.count > 2 ? Int(args[2]) ?? 1 : 1)
    if cliquerElement(e) { print("cliqué : \(args[1])") } else { sortir("hors zone : \(args[1]) (amener à l'écran d'abord)", code: 2) }

case "action":
    guard args.count >= 3 else { sortir("usage : action NOM LIBELLÉ [N]") }
    if args[1] == "AXScrollUpByPage" || args[1] == "AXScrollDownByPage" { sortir("refusé : cette action peut bloquer l'appli") }
    let e = trouver(args[2], args.count > 3 ? Int(args[3]) ?? 1 : 1)
    let r = AXUIElementPerformAction(e, args[1] as CFString)
    print(r == .success ? "\(args[1]) : \(args[2])" : "échec de \(args[1]) (\(r.rawValue)) : \(args[2])")

case "arbre":
    for n in noeuds() {
        let c = cadre(n.element).map { "\(Int($0.minX)),\(Int($0.minY)) \(Int($0.width))x\(Int($0.height))" } ?? "-"
        print(String(repeating: " ", count: n.profondeur) + "\(n.role) | \(n.texte) | \(c)")
    }

default:
    sortir("commande inconnue : \(commande)")
}
