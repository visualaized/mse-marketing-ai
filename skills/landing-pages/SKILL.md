---
description: "Erstellt eine eigenständige, markenkonforme Landing Page (HTML) zu einem Thema. Trigger: 'Landing Page erstellen/generieren zu [Thema]', 'Landingpage für Kampagne X', 'Themenseite bauen'."
disable-model-invocation: false
---

# Landing Pages — MSE Filterpressen GmbH

Dieser Baustein erzeugt aus einem Thema eine kompakte, responsive Landing Page als **eine einzige,
eigenständige HTML-Datei** im markenkonformen MSE-Design — inklusive passender Texte und der in der
Zentrale generierten bzw. bereits vorhandenen Bilder. Die fertige Datei ist direkt auf einem Webspace
einsetzbar. **Jede Landing Page enthält verbindlich einen DE/EN-Sprachumschalter oben rechts** (siehe
Abschnitt 5) — beide Sprachversionen liegen im selben HTML-Dokument, es wird **keine zweite Domain
oder Subdomain** benötigt.

## 1. Wann dieser Baustein läuft

- Der Nutzer möchte eine Landing Page zu einem Thema erstellen ("Landing Page zu CellTRON Xtreme
  bauen", "Landingpage für die Messe-Kampagne", "Themenseite für Batterierecycling").
- Wird häufig von der `marketing-zentrale` im Rahmen einer Kampagne aufgerufen, kann aber auch direkt
  angesprochen werden.

## 2. Benötigte Eingaben klären

Bevor Text oder HTML erzeugt werden, folgende Punkte klären (bereits von der `marketing-zentrale`
übergebene Angaben übernehmen, nur fehlende nachfragen):

1. **Thema** (Pflicht) — worum geht es inhaltlich (Produkt, Anwendungsfall, Kampagne, Messe etc.)?
2. **Zielgruppe/Anlass** — falls nicht eindeutig aus dem Thema ableitbar, kurz nachfragen (z. B.
   "Für welche Zielgruppe/welchen Anlass ist die Seite gedacht — z. B. eine bestimmte Branche,
   eine Messe, eine Ads-Kampagne?").
3. **Subdomain-Slot** (Pflicht) — direkt nachfragen:

   > "Soll die Seite Subdomain A oder Subdomain B ersetzen?"

   Dieser Baustein kennt die tatsächlichen Subdomain-Namen des Kunden nicht (das ist reine
   Infrastruktur-/DNS-Entscheidung des Kunden). Intern wird ausschließlich mit den Bezeichnern
   **"Slot A"** und **"Slot B"** gearbeitet — der Nutzer ordnet diese Bezeichner selbst seinen echten
   Subdomains zu (z. B. campaign1.mse-filterpressen.com / campaign2.mse-filterpressen.com). Der
   gewählte Slot wird im Ausgabe-Dateinamen und in den Kampagnen-Metadaten vermerkt (siehe Abschnitt 10),
   damit die bewusste Rotation der beiden Slots nachvollziehbar bleibt.
4. **Bildmaterial** — optional nachfragen: "Gibt es bereits ein freigegebenes Bild/Video aus der
   Bild-/Videogenerierung, oder soll jetzt eines erzeugt werden?" Falls nichts vorliegt, den Skill
   `bild-video-generierung` aufrufen (siehe Abschnitt 4).

## 3. Pflichtschritt: Markenkern zuerst laden

Bevor irgendein Text oder HTML erzeugt wird, in dieser Reihenfolge lesen (relativ zum aktuellen
Arbeitsverzeichnis, dem Marketing-Hub-Root des Kunden):

1. `CLAUDE.md` — kompaktes Master-Brand-Dokument.
2. `brand/brand-guidelines.md` — vollständiges Regelwerk (Typografie, Bildsprache, Do's & Don'ts).
3. `brand/color-palette.json` — verbindliche, maschinenlesbare Farbwerte.

Bei Widerspruch gewinnt `CLAUDE.md`. Erfinde niemals eigene Markenfakten, Zahlen, Claims oder
Farbwerte — fehlt eine Angabe, nachfragen statt raten. Existieren diese Dateien nicht, stoppen und den
Nutzer darauf hinweisen, dass im Marketing-Hub-Ordner des Kunden gearbeitet werden muss.

**Sprache:** Jede Landing Page wird **immer vollständig in beiden Sprachen** erstellt — Deutsch
(Sie-Ansprache, Standard-Fließtext-Sprache) **und** Englisch (die Sprache, in der MSE international
auftritt, z. B. auf LinkedIn) — nie nur eine Sprachversion. Welche Sprache beim Laden zuerst sichtbar
ist, entscheidet der Sprachumschalter (Default: Deutsch, siehe Abschnitt 5) — das ersetzt die frühere
Vorab-Entscheidung "Deutsch oder Englisch je nach Zielgruppe", da jetzt ohnehin immer beides vorliegt.

## 4. Struktur der Landing Page

Die Seite folgt dem MSE-Baukasten aus Modular-Block-Sections. Basis-Template:
`templates/landing-page-template.html` (Pfad relativ zum Skill-Verzeichnis `landing-pages/`).

| Abschnitt | Sektionstyp | Inhalt |
|---|---|---|
| **Hero** | Dark Hero | Großes reales Produktfoto **in voller Sichtbarkeit** im Hintergrund — **kein flächiges Grau-/Dunkel-Overlay** über dem Bild (die Bilder aus `bild-video-generierung` sind bereits dunkle Editorial-Aufnahmen mit bewusst reservierter Freifläche für die Headline, siehe dortiger Prompt-Aufbau). Große weiße, zentrierte Sentence-Case-Headline mit dezentem `text-shadow` für Lesbarkeit (statt Bild-Abdunkelung), kleine getrackte Grau-Eyebrow, "Scroll down"-Hinweis mit Pfeil. |
| **Problem/Kontext** | Light Content Section | Weißer Hintergrund, zentrierte Eyebrow → Anthrazit-Headline (Sentence case) → Body-Text. Formuliert das Prozessproblem des Kunden im Engineering-First-Ton (Problem zuerst, nicht das Produkt). |
| **Lösung/Produkt** | Split Layout | 50/50 Text (weiß) / Bild (Vollbild, real). Zeigt, wie MSE das Problem löst — technisch, konkret. |
| **Benefits/Features** | 3-Spalten-Cards | Hellgraue Karten, je ein technischer Vorteil/Spec mit kurzem Subhead + Text. |
| **CTA** | Website-.btn-Stil + Kontaktverweis | Pfeilkreis + Uppercase-Label (Verb + Outcome). Hat die Kampagne ein **Whitepaper** (Skill `whitepaper`): darunter eine Download-Zeile im Ghost-Stil mit Pfeilkreis (`data-de`/`data-en`-Label + `data-href-de`/`data-href-en` auf die PDF-URL[s], sprachpassend) — ergänzt den Haupt-CTA, ersetzt ihn nie. |
| **Footer** | site-footer (dunkel) | **Immer derselbe Footer wie die Website** (`class="site-footer relative block js-dark"`-Nachbau, siehe Abschnitt 9). |

Text-Fluss innerhalb jeder Sektion konsequent nach MSE-Muster: **Eyebrow → große Headline → kurze
Erklärung → technisches Wertversprechen → CTA** (sofern die Sektion einen CTA enthält).
**Verbindlich: Eine Headline steht NIEMALS ohne Eyebrow darüber** — jede Sektion mit Headline hat
einen Eyebrow-Platzhalter (`{{..._EYEBROW_DE}}`/`{{..._EYEBROW_EN}}`), auch Split- und CTA-Sektion.

### 4a. Typografie & Abstände — exakt im Website-Verhältnis (Kundenvorgabe, verbindlich)

Das Template setzt `html { font-size: 20px }` — dieselbe rem-Basis wie die Live-Website
(mse-filterpressen.com, Theme-CSS verifiziert 2026-07-02). Dadurch entsprechen alle rem-Werte 1:1
den Website-Proportionen. Nicht ändern und nicht auf px-Werte zurückbauen:

| Element | Spezifikation |
|---|---|
| Headline (h2, Standard) | `2.5rem`, `font-weight: bold`, `line-height: 1.2`, `letter-spacing: -0.02em`, `color: #0D0E11` |
| Hero-Headline (h1) | `4rem`, `font-weight: 900`, sonst wie h2 (Website `.alpha`); weiß auf dem dunklen Hero |
| Body | `15px`, `line-height: 1.4`, `font-weight: normal`, `color: #0D0E11` |
| Eyebrow (h5/.epsilon) | `1rem`, `line-height: 1.2`, `uppercase`, `letter-spacing: 0.05em`, `font-weight: 600`, `color: #5D6A77` |
| Container | `max-width: 80rem`, seitliches Padding `3rem` (Desktop) |
| Sektions-Padding | `6rem` vertikal (Desktop) |

Textfarbe ist `#0D0E11` (Website-Wert), nicht `#1B1B1B`; Eyebrow-Grau ist `#5D6A77`. Link-Hover im
Footer nutzt das Website-Blau `#3D96D2`.

Inhaltliche Leitplanken:
- Immer Sie-Ansprache.
- Kundenproblem zuerst, Produkt danach ("Wir lösen komplexe Filtrationsprobleme", nicht
  "Wir verkaufen Filterpressen").
- Keine erfundenen Statistiken, Studien oder Kundenzitate — nur was aus `CLAUDE.md`,
  `brand-guidelines.md` oder direkten Nutzerangaben stammt.
- Korrekte Schreibweise CellTRON® / MSE Filterpressen® (Markenzeichen bei erster Nennung).
- Keine Wettbewerber namentlich nennen.
- Keine Stockfotos/Cartoons/generische KI-Abstraktionen — nur reale Industriefotografie.

## 5. Sprachumschalter (DE/EN) — verbindlich, keine zweite Domain/Subdomain nötig

**Jede Landing Page hat oben rechts einen persistenten (`position: fixed`, bleibt beim Scrollen
sichtbar) Sprachumschalter** — ein kleiner, dezenter Chip im Brand-Design (Globus-Icon + "DE | EN",
Anthrazit-Halbtransparent-Hintergrund für Lesbarkeit auf jedem Untergrund), passend zum "Sprache/
Globus"-Element aus der rechten Kontakt-Rail der echten Website (`brand-guidelines.md` §7). Beide
Sprachversionen liegen **vollständig im selben HTML-Dokument** — der Umschalter tauscht per
JavaScript nur den sichtbaren Text aus, es wird nichts nachgeladen, es gibt **keine zweite Domain
oder Subdomain**.

**Technische Umsetzung (bereits vollständig im Template `landing-page-template.html` enthalten —
beim Ausfüllen nur die Platzhalter befüllen, nicht die Logik ändern):**

- Jedes übersetzbare Element trägt **zwei Attribute statt eines Platzhaltertexts**:
  `data-de="{{XYZ_DE}}"` und `data-en="{{XYZ_EN}}"`. Alle Content-Platzhalter aus Abschnitt 4 (Hero,
  Problem, Lösung, Features, CTA) existieren deshalb als Paar mit `_DE`/`_EN`-Suffix, z. B.
  `{{HERO_HEADLINE_DE}}` / `{{HERO_HEADLINE_EN}}`, `{{FEATURE_1_TITLE_DE}}` /
  `{{FEATURE_1_TITLE_EN}}` usw. — vollständige Liste im HTML-Kommentar/den Platzhaltern der
  Template-Datei. `{{HERO_IMAGE_URL}}`, `{{SOLUTION_IMAGE_URL}}`, `{{LOGO_URL}}`, `{{LOGO_ICON_URL}}`
  bleiben **einfach** (keine Sprachvarianten nötig, da Bilder sprachunabhängig sind).
- **Ausnahme — der CTA-Button hat auch eine sprachabhängige Ziel-URL:** `{{CTA_BUTTON_URL_DE}}` /
  `{{CTA_BUTTON_URL_EN}}` (nicht nur Label). Grund und genaue Regel siehe Abschnitt 5a
  (URL-Lokalisierung) direkt im Anschluss.
- `{{PAGE_TITLE_DE}}` / `{{PAGE_TITLE_EN}}` steuern den `<title>` sowohl initial als auch beim
  Umschalten (siehe Script am Seitenende).
- Ein kleines eingebettetes Vanilla-JS-Script (kein Framework, keine externe Datei) liest beim Klick
  auf "DE"/"EN" die passenden `data-de`/`data-en`-Attribute (Text) und `data-href-de`/`data-href-en`-
  Attribute (Links, z. B. der CTA-Button) aus und setzt sie per `textContent`/`setAttribute('href', …)`
  — merkt sich die Wahl in `localStorage` für den nächsten Besuch, Default ist Deutsch.
- Footer-Ausnahme: Firmierung, Adresse, Register-/USt-Angaben bleiben **identisch** in beiden
  Sprachen (Pflichtangaben ändern sich nicht durch Sprachwechsel) — nur die Rollenbezeichnung
  "Geschäftsführer" → "Managing Directors" wird übersetzt (siehe Abschnitt 9).

**Übersetzungsqualität:** Die englische Version ist **keine wörtliche/maschinelle Übersetzung**,
sondern eigenständig im MSE-Ton formuliert — gleiche Tonalität wie auf LinkedIn (sehr professionell,
technische Tiefe statt Marketing-Floskeln, CTA = Verb + Outcome), nicht 1:1 aus dem Deutschen
übersetzt. Etablierte zweisprachige Fachterminologie aus `CLAUDE.md`/`brand-guidelines.md` (z. B.
CellTRON-Linienbezeichnungen, Fachbegriffe aus der Terminologie-Tabelle) verwenden, keine eigene
Übersetzung erfinden, wo bereits eine offizielle existiert.

### 5a. URL-Lokalisierung: `{{CTA_BUTTON_URL_DE}}` / `{{CTA_BUTTON_URL_EN}}`

mse-filterpressen.com nutzt ein bestätigtes Muster für zweisprachige Seiten: die **deutsche Version
liegt auf dem Root-Pfad ohne Sprachpräfix**, die **englische Version liegt unter demselben Pfad mit
vorangestelltem `/en/`**. Bestätigtes Beispiel (CellTRON-Seite):

| Sprache | URL |
|---|---|
| Deutsch | `https://mse-filterpressen.com/celltron/` |
| Englisch | `https://mse-filterpressen.com/en/celltron/` |

- Verlinkt der CTA auf eine **bestehende Seite der Hauptwebsite**: `{{CTA_BUTTON_URL_DE}}` = Root-URL,
  `{{CTA_BUTTON_URL_EN}}` = dieselbe URL mit `/en/`-Präfix — aber **nur für Pfade, die der Nutzer
  bestätigt hat oder die bereits als Beispiel belegt sind**. Nicht blind für jede beliebige URL ein
  `/en/`-Pendant annehmen — im Zweifel kurz nachfragen: "Hat die Seite [URL] auch eine englische
  Version unter `/en/...`?"
- Verlinkt der CTA auf **diese Landing Page selbst** oder eine andere Landing Page mit eingebautem
  Sprachumschalter (z. B. ein "Zurück zur Übersicht"-Link): dieselbe URL für beide Sprachen verwenden
  — der Umschalter der Zielseite übernimmt die Sprachzuordnung selbst.
- Dieselbe Logik gilt spiegelbildlich im `newsletter-klaviyo`-Baustein für CTA-Links, die auf diese
  Landing Page zeigen — dort ist es ausführlicher dokumentiert, hier nur der Verweis darauf.

## 6. Technische Anforderungen an die HTML-Datei

- **Eine einzige, eigenständige HTML-Datei** — komplettes CSS in einem eingebetteten `<style>`-Block,
  kein Build-Schritt, kein Framework, keine externen CSS-/JS-Abhängigkeiten (außer optional
  Google Fonts/eine gehostete Nudica-`@font-face`-Datei, siehe unten). So kann die Datei direkt in
  jeden Webspace/jede Subdomain hochgeladen werden.
- **Responsive per reinem CSS**, Mobile-first mit Media-Query-Breakpoint um `768px` — muss auf
  Mobil- und Desktop-Breite gut funktionieren (siehe Template als Referenzimplementierung).
- **Schriftart — echtes Nudica ist Standard, nicht optional:** Das Template embedded Nudica als
  **Base64-Data-URI** direkt im `@font-face`-Block (`{{FONT_DATA_URI_REGULAR}}`/
  `{{FONT_DATA_URI_BOLD}}`) — dadurch bleibt die Seite eine einzige, eigenständige Datei (kein
  externes Hosting nötig) und zeigt trotzdem die echte Kundenschrift. Erzeuge die Data-URIs, indem du
  die echten Font-Dateien aus `brand/fonts/Nudica/Nudica Complete Desktop/Nudica-Regular.otf` und
  `Nudica-Bold.otf` per Base64 kodierst (z. B. `base64 -i "Nudica-Regular.otf"` im Bash-Tool) und als
  `data:font/opentype;base64,<...>` in die Platzhalter einsetzt. `font-family: 'Nudica', Arial,
  sans-serif` bleibt der CSS-Stack — `Arial` greift nur, falls die Base64-Einbettung aus irgendeinem
  Grund fehlschlägt, nicht als bewusster Standardfall wie bei E-Mail-Templates. **Niemals** die
  Font-Zeilen weglassen oder durch reinen System-Font ersetzen, ohne es zu versuchen.
- Sentence case für Display-Headlines (nie GROSSBUCHSTABEN), Eyebrows als kleine getrackte
  Großbuchstaben-Labels in Medium Grey (`#707070`).
- Farben ausschließlich aus `brand/color-palette.json`: Fast White `#FFFFFF` dominant, Light Grey
  `#F5F5F5` für Section-Hintergründe/Cards, MSE Blue `#3498DB` nur als Akzent (max. 10–15 %, nie
  Headline-/Flächenfarbe), Anthracite Black `#1B1B1B` für Dark-Hero/Akzentflächen + Fließtext auf
  hellem Grund, Medium Grey `#707070` für Eyebrows/dünne Trennlinien (`#E2E2E2`).

## 7. Logo: immer das echte Marken-Asset, nie Klartext

Das Template setzt das Logo an zwei Stellen ein — beide sind Pflicht, nicht optional:

- **`{{LOGO_ICON_URL}}`** — im dunklen Hero oben links (persistente Logo-Position laut
  `brand-guidelines.md` §7). Hier wird bewusst das **blaue 3-Streifen-Bildzeichen**
  (`brand/logo/MSE Favicon.png`) verwendet statt der vollen Wortmarke, weil dieses Icon auf jedem
  Hintergrund (hell wie dunkel) funktioniert — die volle Wortmarke ist dunkel/transparent und hätte
  auf dem dunklen Hero keinen Kontrast (kein freigegebenes Weiß-Logo-Asset vorhanden).
- **`{{LOGO_URL}}`** — die volle Wortmarke (`brand/logo/Logo_06.10.2020_ohne Hintergrund.png`) für
  helle Fl&auml;chen (der Footer ist inzwischen dunkel und kommt ohne Logo aus, siehe Abschnitt 9).

Beide Pfade müssen auf **gehostete, öffentlich erreichbare URLs** zeigen (gleiche Logik wie bei
Bildern, siehe Abschnitt 6/11) — niemals Klartext ("MSE Filterpressen" als Wort) als Ersatz einsetzen,
niemals das Logo selbst nachzeichnen oder neu generieren (CellTRON®/MSE® sind geschützte Marken).

## 8. Bilder: reale Assets verwenden, niemals Platzhalter-Stockfotos

Reihenfolge der Prüfung, bevor neu generiert wird:

1. Bereits im aktuellen Durchlauf von `bild-video-generierung` erzeugte und freigegebene Bilder.
2. `Outputs/` — frühere, bereits genehmigte Generierungen zum selben Thema/Produkt.
3. `brand/product/` — vorhandenes reales Produktfotografie-Material.

Erst wenn dort nichts Passendes vorliegt, den Skill `bild-video-generierung` aufrufen und ein neues
Hero-/Split-Bild im passenden Querformat generieren lassen (siehe dortige Formatvorgaben für
Landing-Page-Hero). Die finalen, extern erreichbaren Bild-URLs/-Pfade in `{{HERO_IMAGE_URL}}` und
`{{SOLUTION_IMAGE_URL}}` einsetzen — niemals generische Stockfoto- oder Cartoon-Platzhalter.

## 9. Footer — immer der Website-Footer (site-footer, dunkel)

**Kundenvorgabe, verbindlich:** Jede Landing Page trägt denselben Footer wie die Live-Website
(`class="site-footer relative block js-dark"`). Das Template enthält den Nachbau bereits —
Struktur und Inhalte (verifiziert gegen mse-filterpressen.com am 2026-07-02):

1. **Tagline-Block** oben, zentriert, groß/900 — **hinterlegt mit dem Original-Video**
   (Filterplatten-Animation, gehostet auf der Kundendomain:
   `https://mse-filterpressen.com/wp-content/uploads/2025/04/mse-filterpressen-filterplattenanimation.mp4`,
   absolut positioniert, `object-fit: contain`, muted/loop/autoplay/playsinline). Die Tagline hat
   **exakt die Zeilenumbrüche des Originals** (`.headline-row`-Blöcke, nicht per `data-de`/`data-en`
   umschaltbar, sondern über `html[lang]`-CSS):
   - DE: „Verstehen. Lösen." ⏎ „Vorantreiben. – Bereit," ⏎ „wenn du es bist."
   - EN: „Innovate." ⏎ „Solve. Accelerate." ⏎ „– Ready when you are."
   Darunter helle Trennlinie (`rgba(248,248,248,0.23)`).
2. **Vier Spalten**: „MSE Filterpressen" (Adresse), „Up To Date" (Social: LinkedIn, Instagram,
   YouTube — echte Profil-URLs), „Kontakt" (Telefon + `info@mse-filterpressen.de`), „Themen"
   (Karriere, Impressum, Datenschutz, Zertifizierungen, Fachpresse, FAQ — Links auf die
   Live-Website).
3. **Rechtliche Zeile** darunter (klein, hell auf Schwarz), exakt und vollständig:

```
MSE Filterpressen GmbH · Am Eisengraben 3 · 75196 Remchingen · Deutschland ·
Geschäftsführer: Giuseppe Rumé, Riccardo Valerio Rumé · Amtsgericht Mannheim HRB 502677 ·
USt-IdNr. DE 144200297.
```

Hintergrund `#000`, ALLE Texte weiß (rechtliche Zeile `#C9C9C9`), Link-Hover `#3D96D2`. **Keine
Faxnummer** (Kundenvorgabe: Fax wird nirgends genannt). Den Footer niemals durch einen hellen
Minimal-Footer ersetzen.

## 10. Ablage

Fertige Datei speichern unter:

```
Outputs/<datum>-<thema>-landingpage/index.html
```

Datum im Format `JJJJ-MM-TT`, Thema kurz und dateinamenfreundlich (Kleinbuchstaben, Bindestriche), z. B.
`Outputs/2026-07-01-celltron-xtreme-batterierecycling-landingpage/index.html`.

Ist diese Landing Page Teil einer verfolgten Kampagne, zusätzlich `Campaigns/<slug>/meta.json` gemäß
dem verbindlichen Schema aus dem Skill `kampagnen-dashboard` aktualisieren bzw. anlegen: Kanal
`"Landing Page"` in `kanaele` ergänzen und in `notiz` kurz den gewählten Subdomain-Slot vermerken
(z. B. `"Landing Page live auf Slot A"`). Das exakte `meta.json`-Schema (Felder, Enum-Werte für
`status` etc.) ist dort dokumentiert und wird hier nicht wiederholt — bei Unsicherheit dort nachlesen.

## 11. Wichtige Einschränkung: kein Upload durch diesen Baustein

**Dieser Skill hat keinen Zugriff auf den Webserver/FTP/Hosting des Kunden.** Er erzeugt ausschließlich
die fertige, einsatzbereite HTML-Datei. Das Hochladen der Datei auf den tatsächlichen Webspace/die
gewählte Subdomain ist ein **manueller Schritt durch den Kunden oder die Agentur** — dies dem Nutzer am
Ende jedes Durchlaufs klar mitteilen, inklusive Erinnerung an den gewählten Subdomain-Slot (Slot A/B),
damit die Zuordnung beim Hochladen stimmt.

## 12. QA-Checkliste vor Übergabe

- [ ] Markenfarben korrekt (Fast White/Light Grey dominant, Anthracite Black nur als Akzentfläche,
      MSE Blue max. 10–15 % und nur als Akzent, kein Grün/Rot außer Eco:LOGIC-Kontext).
- [ ] Typografie korrekt: `'Nudica', Arial, sans-serif`, Sentence-Case-Headlines, getrackte
      Großbuchstaben-Eyebrows in Medium Grey. **Echtes Nudica als Base64-`@font-face` eingebettet**
      (nicht stillschweigend beim Arial-Fallback belassen)?
- [ ] **Logo an beiden Stellen mit echten Assets befüllt** — `{{LOGO_ICON_URL}}` (Bildzeichen im
      Hero) und `{{LOGO_URL}}` (Wortmarke im Footer), kein Klartext-Ersatz?
- [ ] **Sprachumschalter oben rechts vorhanden, funktioniert und ist immer sichtbar** (`position:
      fixed`, bleibt beim Scrollen im Bild)? Beide Sprachen **vollständig** befüllt — kein
      `{{...}}`-Platzhalter oder leeres `data-de`/`data-en`-Attribut übrig geblieben (Stichprobe: im
      Browser einmal auf EN umschalten und die ganze Seite durchscrollen)?
- [ ] **Englische Version ist eigenständig im MSE-Ton formuliert**, keine wörtliche/maschinelle
      Übersetzung; etablierte zweisprachige Fachbegriffe aus `CLAUDE.md`/`brand-guidelines.md`
      verwendet?
- [ ] **CTA-Button-URL sprachpassend** (`{{CTA_BUTTON_URL_DE}}`/`{{CTA_BUTTON_URL_EN}}`) — DE zeigt
      auf die Root-URL, EN auf die `/en/`-Variante (bzw. dieselbe URL bei Verweis auf eine andere
      Seite mit eigenem Sprachumschalter) — im Browser durch Klick auf "EN" und Hover über den
      CTA-Button geprüft, nicht nur angenommen?
- [ ] Reale Industriefotografie verwendet — keine Stockfotos/Cartoons/generische KI-Abstraktionen.
- [ ] **Kein flächiges Grau-/Dunkel-Overlay über dem Hero-Bild** — Bild in voller Sichtbarkeit,
      Textlesbarkeit über `text-shadow` statt Bild-Abdunkelung gelöst?
- [ ] Responsive: Seite auf Mobil-Breite (~375px) geprüft/plausibel, Split- und 3-Spalten-Sektionen
      stapeln korrekt auf ein Spalten-Layout.
- [ ] CTA-Label = Verb + Outcome (kein reines "Mehr erfahren" ohne Kontext).
- [ ] Durchgehend korrekte Sie-Ansprache.
- [ ] Schreibweise CellTRON® / MSE Filterpressen® korrekt.
- [ ] Keine Wettbewerber namentlich genannt.
- [ ] **Typografie im Website-Verhältnis** (Abschnitt 4a): Headline 2.5rem bold `#0D0E11`, Body 15px
      lh 1.4, Eyebrow 1rem 600 `#5D6A77`, `html { font-size: 20px }` unverändert?
- [ ] **Keine Headline ohne Eyebrow** — jede Sektion mit Headline hat einen befüllten Eyebrow?
- [ ] **Website-Footer (site-footer, dunkel) vorhanden** — Tagline, vier Spalten, Themen-Links,
      rechtliche Zeile auf `#000` mit hellem Text (Abschnitt 9)? Keine Faxnummer?
- [ ] Keine erfundenen Statistiken, Studien oder Claims — alles auf `CLAUDE.md`/`brand-guidelines.md`
      bzw. Nutzerangaben rückführbar.
- [ ] Subdomain-Slot (A/B) mit dem Nutzer geklärt und in Dateiname/Notiz vermerkt.
- [ ] Nutzer wurde klar darauf hingewiesen, dass der Upload auf den Webspace ein manueller Schritt ist.
