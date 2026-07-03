# mse-marketing-ai — KI-Marketing-Zentrale für MSE Filterpressen GmbH

Claude-Code-Plugin mit allen Bausteinen aus der Auftragsbestätigung `AB202606-1000`. Das Plugin
enthält **keine** Marken-/Brand-Daten selbst — es liest diese zur Laufzeit aus dem **Marketing Hub**
des Kunden (Grundbaustein, separat aufgesetzt: `CLAUDE.md`, `brand/`, `Outputs/`, `Campaigns/`). Das
Plugin muss deshalb immer mit dem Marketing-Hub-Ordner als Arbeitsverzeichnis genutzt werden.

## Enthaltene Bausteine (Skills)

| Skill | Pos. im Angebot | Zweck |
|---|---|---|
| `marketing-zentrale` | 1 (Grundbaustein-Logik) | Zentrale Steuerlogik: Thema → Rückfragen → Auslösen der passenden Bausteine |
| `bild-video-generierung` | 2 | KI-Bilder (2K, nach `nano-banana-prompt`-Struktur) & KI-Videos via Higgsfield |
| `newsletter-klaviyo` | 3 | Thema → Text & Bilder → HTML-Newsletter → Klaviyo-Draft-Campaign |
| `newsletter-migration` | 4 (Add-on) | Einmalige Kontakt-Migration Brevo → Klaviyo inkl. DSGVO-Prüfung |
| `social-instagram` | 5 | Instagram-Posts (Deutsch, lockerer-professionell) + Upload-Post |
| `social-linkedin` | 5 | LinkedIn-Posts (Englisch, sehr professionell/Thought-Leadership) + Upload-Post |
| `social-x` | 5 | X-Posts (Englisch, kurz/prägnant) + Upload-Post |
| `kampagnen-dashboard` | 6 | Statisches Kampagnen-Dashboard für die Geschäftsführung |
| `email-signatur` | 7 | Markenkonforme HTML-E-Mail-Signaturen |
| `landing-pages` | 8 | Responsive Single-File-HTML-Landingpages für 2 Wechsel-Subdomains |

Dokumentation/Schulung/Abnahme (Pos. 9) ist keine Skill-Datei, sondern dieser README + eine Live-Schulung.

## Voraussetzung: Marketing Hub

Dieses Plugin erwartet im **Arbeitsverzeichnis** (nicht im Plugin-Ordner selbst) die Struktur des
Marketing-Hub-Grundbausteins:

```
<Marketing-Hub-Root>/
  CLAUDE.md                     # Master-Brand-Dokument (immer zuerst gelesen)
  brand/
    brand-guidelines.md
    color-palette.json
    logo/, elements/, fonts/, product/
  Outputs/                      # fertige Ergebnisse
  Campaigns/                    # Kampagnen-Ordner (meta.json je Kampagne, siehe kampagnen-dashboard-Skill)
```

Ohne diese Dateien lehnen die Skills die Erzeugung von Inhalten ab (siehe jeweilige SKILL.md, Abschnitt
"Pflichtschritt: Markenkern immer zuerst laden") — es wird nichts "blind" generiert.

## Installation beim Kunden (pro Arbeitsplatz/Client)

1. Marketing-Hub-Ordner auf dem zentralen Server/Share des Kunden bereitstellen (einmalig, Grundbaustein).
2. Auf jedem Arbeitsplatz, der mit Claude Code arbeiten soll:
   - Repository dieses Plugins klonen bzw. aktualisieren (z. B. `git clone <repo-url>`).
   - In Claude Code: `/plugin marketplace add <owner>/<repo>` (oder lokal: `claude --plugin-dir "<Pfad zu diesem Ordner>"` für Tests).
   - Danach: `/plugin install mse-marketing-ai`.
   - Claude Code **im Marketing-Hub-Ordner** starten (dort liegt `CLAUDE.md`) — nicht im Plugin-Ordner.
3. Benötigte MCP-Zugänge/API-Keys gemäß Auftragsbestätigung einrichten: Klaviyo, Higgsfield, Upload-Post,
   Claude (Anthropic) und — nur für die einmalige Kontakt-Migration — Brevo.

Dieser Schritt ("Client-Anbindung": Verlinkung zum Brand Hub + Installation der Plugins/Skills pro
Arbeitsplatz) ist laut Auftragsbestätigung aufwandsbezogen abzurechnen und nicht Teil dieser Pauschalen.

## Remote-Updates

Die Versionierung erfolgt über `version` in `.claude-plugin/plugin.json` (aktuell `1.0.0`):

- Neue Version im Repo taggen/pushen → Version in `plugin.json` erhöhen (SemVer).
- Kunde/Client: `/plugin update mse-marketing-ai` (bzw. automatisches Update, falls in den
  Claude-Code-Einstellungen aktiviert) holt die neue Version.
- Da alle Marken-/Kundendaten **außerhalb** des Plugins im Marketing Hub liegen, betreffen Updates nie
  Kundendaten — nur Skill-Logik, Templates und Dashboard-Code.

## Bearbeitungs-Hinweis (für visualaized/pebro)

Bei Änderungen an Skills: Versionsnummer in `.claude-plugin/plugin.json` erhöhen und Changelog-Eintrag
unten ergänzen, damit Remote-Updates beim Kunden nachvollziehbar bleiben.

## Changelog

- **1.13.1** (2026-07-02) — Fix Whitepaper-Titelseite: **`text-shadow` wird von Chrome beim
  PDF-Export als eckige dunkle Kästen hinter den Textzeilen gerastert** (bekannter
  `--print-to-pdf`-Bug). Schatten aus der Druckvorlage entfernt; Lesbarkeit der Titelseite kommt
  jetzt von einem `cover__scrim`-Verlauf (EIN linearer Gradient ohne Zwischenstops —
  Zwischenstops erzeugen im PDF sichtbare Banding-Kanten). Regel „kein text-shadow in
  Druckvorlagen" + Cover-Foto-Check in der QA verankert; Demo-PDF neu gebaut und abgenommen.
- **1.13.0** (2026-07-02) — **Neuer Baustein: PDF-Whitepaper** (Skill `whitepaper`):
  1. **A4-Druckvorlage** (`templates/whitepaper-template.html`) nach dem Website-Design-System:
     dunkle Titelseite mit Cover-Foto + „Whitepaper"-Badge, Sections mit Eyebrow→Headline→Body im
     Website-Typo-Verhältnis, Infoboxen/Key-Facts/Statement-Box/Datentabellen, dunkle
     CTA-Schlussseite mit Pfeilkreis, Bildzeichen auf jeder Seite in der Ecke, kein Fax.
  2. **On-brand Diagramm-System**: Schaubilder/Graphen als Inline-SVG mit verbindlichen Regeln
     (nur Markenfarben, ein Blau-Akzent, eckige Balken, hairline-Gitter, Nudica-Beschriftung,
     keine Torten-Diagramme, Quellenzeile) — fertige CSS-Klassen + Balkendiagramm-Muster im
     Template.
  3. **PDF-Erzeugung** über `scripts/build_whitepaper.py`: bettet echte Nudica-Fonts ein und
     rendert via Chrome/Edge headless (`--print-to-pdf`, Timeout-Sicherheitsnetz); Fallback
     Browser-Druckdialog dokumentiert. End-to-End getestet (4-seitiges CellTRON-Demo-PDF).
  4. **Kampagnen-Integration**: „Whitepaper" als Kanal in der Kanalauswahl der Zentrale und im
     Kampagnen-Dashboard (Planungsformular + Server-Validierung); Download-Verlinkung als
     sekundärer Ghost-CTA im Newsletter (beide Sprachen, sprachpassend) und als Download-Zeile
     in der Landing-Page-CTA-Sektion dokumentiert; PDF wird im `inhalte`-Feld der Kampagne
     registriert.
- **1.12.0** (2026-07-02) — Grafik-Kompositionen (compose_slide.py) exakt on Brand:
  1. **Bildzeichen-Platzierungsregel (Kundenvorgabe):** Das Favicon-Bildzeichen steht nie mehr
     frei im Raum — neue Option `--logo-pos tl|tr|bl|br|headline` (vier Bildecken mit
     einheitlichem, an der kürzeren Kante bemessenem Eckabstand, oder mit Abstand direkt über
     dem Headline-Block); Regel in `brand/website-design-system.md` §3 und der zentralen QA
     verankert. Behebt das frei schwebende Logo auf flachen Bannern.
  2. **Schriftgrößen/-gewichte im Website-Verhältnis:** Eyebrow : Headline : Body jetzt
     0.4 : 1 : 0.3 wie die Website (statt Body fast in Headline-Größe); Headline deutlich größer
     (width/13), Eyebrow in **Nudica-Medium** (Website-Gewicht 600 statt Bold), Body Regular.
  3. **CTA im echten Website-Stil auch in Grafiken:** Pfeilkreis (1px currentColor) + Uppercase-
     Bold-Label statt der bisherigen weißen Pille.
  4. Signatur-Banner und Instagram-Carousel-Demo mit allen Fixes neu erzeugt.
- **1.11.0** (2026-07-02) — **Vollständiges Website-Design-System extrahiert und als verbindliche
  CI-Grundlage verankert** (Theme-CSS + Seiten-HTML von mse-filterpressen.com komplett ausgewertet):
  1. **Neues Brand-Dokument `brand/website-design-system.md`** im Marketing Hub: verifizierte
     Farben, komplette Typo-Skala (1rem=20px, alpha–zeta), Formen/Elemente (eckig, 2rem-Pfeilkreis,
     quadratische Karussell-Dots, Reveal-Animationssprache), Layout/Abstände (Container 80rem/3rem,
     6rem-Rhythmus, Breakpoints), Sektions-Baukasten (alle block--Typen) und Footer-Spezifikation.
     In `CLAUDE.md`, `color-palette.json` und `marketing-zentrale` (Pflichtlektüre, Schritt 0)
     verankert. Bei Widerspruch zu älteren Dokumenten gewinnt das Design-System.
  2. **Farbpalette korrigiert auf echte Website-Werte:** Text/Dunkel `#0D0E11` (statt `#1B1B1B`),
     Sekundär-Grau `#5D6A77`, Hellgrau `#F8F8F8` (statt `#F5F5F5`), Blau `#3D96D2` (statt
     `#3498DB`), Footer `#000` — in Templates und `compose_slide.py` durchgezogen.
  3. **Landing-Page-Footer wie Original:** Tagline jetzt mit dem Original-Hintergrund-Video
     (Filterplatten-Animation, gehostet auf der Kundendomain) und den EXAKTEN Zeilenumbrüchen der
     Website (DE „Verstehen. Lösen." / „Vorantreiben. – Bereit," / „wenn du es bist.", EN analog).
  4. **CTA im echten Website-Stil:** keine Pille mehr — transparenter uppercase-Button mit
     2rem-Pfeilkreis (1px currentColor) und Hover in `#3D96D2`, wie `.btn` der Website.
- **1.10.0** (2026-07-02) — **Design-Angleichung an die Live-Website** (Kundenvorgaben, Stil aus
  mse-filterpressen.com/Theme-CSS extrahiert und verifiziert):
  1. **Typografie-Verhältnisse wie Website** in Landing-Page- und Newsletter-Templates:
     Headline 2.5rem/bold/`#0D0E11`/lh 1.2/ls -0.02em (Hero 4rem/900), Body 15px/lh 1.4/`#0D0E11`,
     Eyebrow 1rem/600/uppercase/ls 0.05em/`#5D6A77`; Landing Page mit Website-rem-Basis
     (`html{font-size:20px}`), Container 80rem/3rem, Sektions-Padding 6rem. **Nie eine Headline
     ohne Eyebrow** (neue Eyebrow-Slots in Split- und CTA-Sektion, Pflichtregel in allen Skills).
  2. **Landing Pages: Website-Footer** — Nachbau des `site-footer js-dark` (schwarz, Tagline
     „Verstehen. Lösen. Vorantreiben. …", vier Spalten mit echten Social-/Themen-Links,
     rechtliche Zeile, Hover-Blau `#3D96D2`).
  3. **Newsletter: Footer-Bild + nahtloser Rechtsfooter** — `brand/elements/MSE Newsletter
     Footer.png` immer in voller Breite über dem rechtlichen Footer; dieser nahtlos darunter auf
     `#000000` mit hellem Text (neuer Platzhalter `{{FOOTER_IMAGE_URL}}`).
  4. **Keine Faxnummer mehr, nirgends** (aus Templates/Doku entfernt, als Verbotsregel verankert);
     **Trennstriche immer dunkel, nie blau** (Signatur-Templates umgestellt).
  5. **`compose_slide.py`: leichter, weicher Schatten** hinter hellem Text auf Foto-Hintergründen
     (Gaussian-Blur, kein harter Umriss) — helle Schrift hebt sich jetzt auch auf hellen
     Bildbereichen ab; Signatur-Banner neu erzeugt.
- **1.9.0** (2026-07-02) — Kampagnen-Dashboard: Inhalte-Anzeige + Bearbeiten/Löschen + Datenbereinigung:
  1. **Generierte Inhalte pro Kampagne sichtbar:** neues optionales `meta.json`-Feld
     `inhalte: [{label, pfad}]` — das Dashboard zeigt pro Kampagne eine ausklappbare Link-Liste
     („n Inhalte anzeigen"); die Dateien werden über einen neuen lesenden `/hub/`-Mount von
     `server.mjs` ausgeliefert (Traversal-geschützt, nur GET). Verbindliche neue Regel in der
     `marketing-zentrale`: Jeder fertige Output MUSS im `inhalte`-Feld registriert werden.
  2. **Geplante Kampagnen bearbeiten/löschen:** neue Endpunkte `PUT`/`DELETE
     /api/campaigns/<slug>` + Bearbeiten-/Löschen-Buttons in der Kampagnenzeile (Formular
     vorbefüllt, Löschen mit Bestätigungsdialog). Serverseitig strikt auf Status „geplant"
     beschränkt (409 sonst) — laufende Kampagnen sind über die Oberfläche unantastbar.
  3. **Agentur-Name entfernt:** „visualaized / pebro GmbH" aus allen kundensichtbaren
     Kampagnendaten und dem Showcase entfernt; neue verbindliche Regel: `verantwortlich` ist immer
     eine kundeninterne Angabe (Standard „Marketing-Team"), nie ein Dienstleistername.
- **1.8.0** (2026-07-02) — **Kampagnen-Dashboard wird Planungstool + Planungsabgleich in der Zentrale:**
  1. **Planungsformular im Dashboard** („+ Kampagne planen"): Thema/Beschreibung, geplantes
     Veröffentlichungsdatum, Kanal-Checkboxen und Notizen — schreibt über die neue Mini-API in
     `server.mjs` (`POST /api/campaigns`) eine reguläre `Campaigns/<slug>/meta.json` mit
     `status: "geplant"` und `quelle: "dashboard-planung"`. Formular erscheint nur bei laufendem
     Server (Feature-Detection `GET /api/ping`); bei statischem Hosting bleibt das Dashboard reine
     Lese-Übersicht.
  2. **Live-Index:** `campaigns-index.json` wird von `server.mjs` bei jedem Abruf frisch aus den
     `meta.json`-Dateien generiert — der manuelle `generate-index.mjs`-Schritt entfällt bei
     laufendem Server (bleibt als Fallback für statisches Hosting).
  3. **Planungsabgleich in der `marketing-zentrale`** (neuer Schritt 1a, Pflicht): Beim Start einer
     Kampagne über Claude wird `Campaigns/` nach passenden geplanten Kampagnen durchsucht; bei
     bestätigtem Treffer werden Beschreibung, Kanäle, Zeitraum und Notizen übernommen (Kanalfrage
     entfällt, nur noch Bestätigung), der bestehende Ordner weiterverwendet und der Status auf
     „in Arbeit" gesetzt — kein Duplikat, keine doppelte Abfrage.
  4. Dashboard-App jetzt **self-contained** (Logo + Nudica-Fonts als lokale Kopien im App-Ordner) —
     behebt still fehlschlagende `../brand/...`-Pfade unter dem Standalone-Server.
- **1.7.0** (2026-07-02) — **Verbindliche Kanalauswahl per Multiple Choice zum Kampagnenstart.**
  Die `marketing-zentrale` fragt jetzt zu Beginn JEDER Kampagne per Mehrfachauswahl (interaktives
  Auswahl-Tool, kein Freitext), welche Kanäle bespielt werden sollen: Instagram, LinkedIn, X,
  Newsletter (automatisch DE+EN), Landing Page, E-Mail-Signatur. Die Auswahl wandert 1:1 in das
  `kanaele`-Feld der Kampagnen-`meta.json` und steuert Dashboard und Folge-Bausteine. Dabei
  bereinigt: die veraltete Newsletter-Sprachfrage ("Deutsch / Englisch / beide") aus Schritt 2
  entfernt — Newsletter sind seit 1.5.0 immer zweisprachig, eine Sprachabfrage widersprach dem.
- **1.6.2** (2026-07-02) — Zwei Fixes nach Kundenfeedback:
  1. **`compose_slide.py`: CTA-Button wurde bei flachen Formaten unten abgeschnitten.** Ursache: der
     Textblock startete fix bei 62 % der Bildhöhe und lief nach unten aus dem Bild (v. a. beim
     Signatur-Banner 1184×420). Behoben: die Gesamthöhe des Blocks (Eyebrow + Headline + Body + CTA)
     wird jetzt vorab gemessen und der Block bei Bedarf nach oben verschoben (Bottom-Anchor mit
     Sicherheitsabstand) — der CTA passt immer vollständig ins Bild. Signatur-Banner neu erzeugt.
  2. **Blatt-Icon** (`brand/elements/icons/icon-leaf.png`) neu gezeichnet — die vorherige Grafik war
     nicht als Blatt erkennbar; jetzt klassische Blattform mit Mittelrippe und Stiel in Grün.
- **1.6.1** (2026-07-01) — Fix: **Signatur-Banner wurde auf mobilen Geräten abgeschnitten.** Ursache:
  ein festes `width="..."`-HTML-Attribut auf dem Banner-`<img>` sowie auf der äußeren Signatur-Tabelle
  wurde von mobilen Mail-Clients wörtlich als Pixelbreite übernommen, auch wenn die Zelle bereits
  geschrumpft war — das Bild ragte über den Rand hinaus. Behoben durch eine durchgängig fluide Struktur
  (Tabelle `width="100%"` + `max-width:640px`, Bild nur noch `width:100%; max-width:592px; height:auto`
  über CSS, kein HTML-`width`-Attribut mehr) in `signatur-standard.html`, `signatur-cisign.html` und dem
  ausgelieferten Demo-Beispiel. Neue verbindliche Regel inkl. Begründung in SKILL.md Abschnitt 2a
  verankert, QA-Checkliste ergänzt (Test in ~375px-Vorschau vor Auslieferung).
- **1.6.0** (2026-07-01) — Feinschliff auf explizites Kundenfeedback zu Font/Umlaut-Treue und CI Sign:
  1. **`compose_slide.py`: harter Schlagschatten/Umriss um Text entfernt.** Die bisherige
     Per-Buchstaben-Duplikat-Technik (Schwarz versetzt + Weiß darüber) erzeugte einen sichtbaren
     dunklen Rand/Halo, der wie eine falsche Schriftart wirkte. Ersetzt durch einen weichen, nur auf
     die Textzone begrenzten Verlaufs-Scrim (`apply_text_scrim()`) — Text bleibt lesbar, ohne
     Schatten-/Umriss-Artefakt, echte Nudica-Typografie bleibt klar erkennbar. Alle Demo-Assets
     (Signatur-Banner, Instagram-Carousel-Slides) mit der reparierten Version neu erzeugt.
  2. **Umlaute (ü/ä/ö/ß) jetzt durchgängig korrekt** in allen Beispiel-Skripten, Slide-Inhalten und
     SKILL.md-Dokumentationen — vorherige ASCII-Ersatzschreibweisen ("ue"/"ae"/"oe"/"ss") entfernt und
     durch die echten Zeichen ersetzt (die Nudica-Schrift enthält alle deutschen Sonderzeichen
     vollständig; das war ein reiner Eingabefehler, kein Font-Problem). Neue verbindliche
     Umlaut-Regel in allen drei Social-Media-Skills (Instagram/LinkedIn/X) verankert.
  3. **E-Mail-Signatur: neue CI-Sign-Variante** (`email-signatur/templates/signatur-cisign.html`) mit
     recherchierten CI-Sign-Platzhaltern (`@@`/`##`-Syntax, echte Active-Directory-Attributnamen wie
     `displayName`, `title`, `telephoneNumber`, `mail`, `streetAdress`, `postalCode`, `l`) für den
     automatischen Personenbezug beim Signatur-Rollout — dokumentiert inkl. Einschränkungen
     (einsprachiges `title`-Attribut, Zeilen-Lösch-Verhalten vor Rollout testen) in SKILL.md
     Abschnitt 5b.
  4. **Social-Media-Skills:** verbindliche, plattformexakte Pixelmaße für Text-/Carousel-Slides
     festgeschrieben (Instagram `1080x1350`/`1080x1080`, LinkedIn `1200x1200`/`1200x628`, X
     `1600x900`/`1200x1200`) sowie die neue `compose_slide.py --bg-color`-Option für reine
     Schaubild-/Fakten-Slides dokumentiert (nicht jede Slide braucht ein Foto).
- **1.5.0** (2026-07-01) — Drei neue verbindliche Anforderungen umgesetzt:
  1. **Social Media (Instagram/LinkedIn/X): Pflichtfrage "reine Bilder oder Text-/Info-Content?"**
     Bei Text-/Info-Content wird ein Carousel (Instagram) bzw. Mehrbild-Post (LinkedIn/X) erzeugt,
     bei dem Headline/Body/CTA fest in die Bilder eingebrannt sind — immer mit echter Nudica-Schrift
     und echtem Logo. Neues wiederverwendbares Werkzeug: `bild-video-generierung/scripts/
     compose_slide.py` (Pillow-basiert, produziert markenkonforme Einzel-Slides).
  2. **Newsletter: immer zweisprachig (DE+EN)**, keine Sprachauswahl mehr — jede Version geht als
     eigener Klaviyo-Draft an das dafür bestätigte Segment (Segment-Zuordnung wird mit dem Nutzer
     abgeglichen, nie geraten). CTAs verlinken sprachpassend.
  3. **URL-Lokalisierung dokumentiert und verdrahtet:** bestätigtes Muster für mse-filterpressen.com
     — Deutsch = Root-Pfad, Englisch = `/en/`-Präfix (Beispiel: `.../celltron/` vs.
     `.../en/celltron/`). Newsletter-CTAs und Landing-Page-CTA-Button (jetzt mit `_DE`/`_EN`-URL-Paar,
     wechselt live beim Sprachumschalter) wenden dieses Muster an; Konvention zusätzlich in der
     Marketing-Hub-`CLAUDE.md` festgehalten.
- **1.4.0** (2026-07-01) — `landing-pages`: **verbindlicher DE/EN-Sprachumschalter** oben rechts
  (Globus-Icon + "DE | EN", `position: fixed`, Brand-Design) — beide Sprachversionen liegen im selben
  HTML-Dokument, es wird **keine zweite Domain/Subdomain** benötigt. Alle Content-Platzhalter jetzt als
  `_DE`/`_EN`-Paare (`data-de`/`data-en`-Attribute + kleines Vanilla-JS zum Umschalten, merkt sich die
  Wahl in `localStorage`). Beim Bau entdeckter und behobener Bug: Titel wurden ursprünglich in ein
  einfach gequotetes JS-String-Literal eingesetzt — ein Apostroph im Text (z. B. "MSE's ...") hätte das
  Literal vorzeitig beendet und das gesamte Umschalt-Script per SyntaxError lahmgelegt; Titel werden
  jetzt wie der übrige Content aus HTML-Attributen gelesen (unempfindlich gegenüber Apostrophen).
- **1.3.0** (2026-07-01) — `email-signatur`: vier Korrekturen aus Kundenfeedback:
  1. **Banner ist jetzt immer Foto + Headline + CTA in einem Bild**, nie mehr ein bloßes Foto —
     begründet mit der fehlenden Zuverlässigkeit von Text-über-Bild-HTML in E-Mail-Clients; Skill
     dokumentiert den Kompositions-Workflow (Pillow + echte Nudica-Schriftdatei oder HTML+Screenshot).
  2. **Zeichencodierung behoben** — Template nutzte rohe UTF-8-Sonderzeichen (ü/ö/ä/ß/é), was beim
     Einfügen in manche Mail-Clients zu Mojibake führte ("GrÃ¼Ã&#65533;en"); jetzt durchgängig
     HTML-Entities, neue Skill-Regel dazu ergänzt.
  3. **Kontakt-Icons sind jetzt echte Bild-Assets** (`brand/elements/icons/`) statt Unicode-/
     Emoji-Zeichen als Textersatz.
  4. **Kein sichtbarer Platzhaltertext mehr im HTML-Body** — fehlende Angaben (z. B. Social-Links)
     führen zum sauberen Entfernen der Zeile statt zu einer sichtbaren Regieanweisung.
- **1.2.1** (2026-07-01) — `landing-pages`: generelles Grau-/Dunkel-Overlay über dem Hero-Bild entfernt
  (Bild jetzt in voller Sichtbarkeit); Textlesbarkeit von Headline/Eyebrow stattdessen über
  `text-shadow` gelöst statt über eine Abdunkelung des gesamten Bilds.
- **1.2.0** (2026-07-01) — Zwei Korrekturen aus Kundenfeedback:
  1. `bild-video-generierung`: Prompt-Regelwerk um eine explizite Anweisung ergänzt, Nameplates/Logos
     auf Maschinen als **flache, aufgeklebte Folie** darzustellen (nicht erhaben/3D) — Beispiel-Prompt
     entsprechend nachgeschärft.
  2. **Logo & Nudica-Schrift waren nur als Fallback vorgesehen, nicht durchgängig genutzt** — behoben in
     allen betroffenen Templates: `newsletter-klaviyo` (Header jetzt Light Grey mit echtem
     `{{LOGO_URL}}` statt Klartext/Anthrazit-Band), `landing-pages` (Logo-Leiste im Hero + Wortmarke im
     Footer ergänzt, echte Nudica-Schrift jetzt als Base64-`@font-face` eingebettet statt nur
     Arial-Fallback), `email-signatur` (Logo-Zeile ergänzt, war zuvor komplett entfernt),
     `kampagnen-dashboard` (Bildzeichen im Header ergänzt, `@font-face`-Pfade/Format korrigiert — zeigten
     zuvor auf nicht existierende `.woff`-Dateien). QA-Checklisten und die zentrale
     `marketing-zentrale`-Checkliste um verbindliche Logo-/Font-Prüfpunkte erweitert.
- **1.1.2** (2026-07-01) — `email-signatur`: Root-Cause-Fix für den Dark-Mode-Bug — Hintergrund war
  `background-color:transparent` statt explizit weiß gesetzt, wodurch Mail-Clients/Browser im Dark
  Mode einen eigenen dunklen Canvas einsetzten und die anthrazitfarbene Schrift unsichtbar wurde.
  Jetzt `bgcolor="#FFFFFF"` + `background-color:#FFFFFF` explizit im Template; per Live-Preview mit
  erzwungenem Dark-Mode-Rendering verifiziert.
- **1.1.1** (2026-07-01) — `email-signatur`: Korrektur — der dunkle Hintergrund im Kunden-Referenz-
  Screenshot war nur Dark-Mode-Rendering des Mail-Clients. Template/Skill zurück auf hellen/
  transparenten Untergrund mit dunkler (anthrazitfarbener) Schrift und Icons umgestellt; Struktur
  (zweisprachige Rolle, Icon-Kontaktzeilen, Banner, Social-Icons, Phishing-Hinweis, „Think before you
  print") bleibt unverändert erhalten.
- **1.1.0** (2026-07-01) — `bild-video-generierung`: Prompt-Aufbau verbindlich nach der 6-Layer-Struktur
  des `nano-banana-prompt`-Skills, Generierung immer in 2K. `email-signatur`: Template und Skill auf das
  vom Kunden vorgegebene reale Referenzlayout umgestellt (dunkler Hintergrund, zweisprachige Rolle,
  Icon-Kontaktzeilen, klickbares Banner-Bild, Social-Icons, Phishing-Hinweis, „Think before you print").
- **1.0.0** (2026-07-01) — Initiales Release: alle 9 Bausteine aus AB202606-1000 umgesetzt.
