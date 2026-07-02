---
description: "Erstellt markenkonforme Newsletter für MSE Filterpressen und legt sie als Draft-Kampagne in Klaviyo an. Trigger: 'Newsletter erstellen', 'Klaviyo-Kampagne', 'Kampagnen-Mail', 'Mailing zu Thema X', 'Newsletter versenden vorbereiten'."
disable-model-invocation: false
---

# Newsletter (Klaviyo) — MSE Filterpressen GmbH

Dieser Baustein erzeugt aus einem Thema einen fertigen, markenkonformen HTML-Newsletter und legt ihn
in Klaviyo als **Draft-Kampagne** an (Template + Kampagne + Zuordnung). Er wird in der Regel von der
`marketing-zentrale` aufgerufen, kann aber auch direkt angesprochen werden.

## Wann dieser Skill greift

- Der Nutzer möchte einen Newsletter, ein Mailing oder eine E-Mail-Kampagne zu einem Thema erstellen.
- Der Nutzer sagt z. B. "Newsletter zu CellTRON Xtreme", "Klaviyo-Kampagne aufsetzen", "Mailing für
  die Messe", "Newsletter-Entwurf für nächste Woche".
- Nicht zuständig für: einmalige Transaktions-E-Mails, SMS/WhatsApp-Kampagnen, Kontakt-Migration
  (dafür `newsletter-migration`).

## 0. Markenkern zuerst laden (Pflicht)

Bevor irgendein Text oder HTML erzeugt wird, in dieser Reihenfolge lesen (relativ zum aktuellen
Arbeitsverzeichnis, dem Marketing-Hub-Root des Kunden):

1. `CLAUDE.md` — kompaktes Master-Brand-Dokument.
2. `brand/brand-guidelines.md` — vollständiges Regelwerk (Typografie, Bildsprache, Do's & Don'ts).
3. `brand/color-palette.json` — verbindliche, maschinenlesbare Farbwerte.

Bei Widerspruch gewinnt `CLAUDE.md`. Erfinde niemals eigene Claims, Zahlen oder Farbwerte — fehlt eine
Angabe, nachfragen statt raten. Existieren diese Dateien nicht, stoppen und den Nutzer darauf
hinweisen, dass im Marketing-Hub-Ordner des Kunden gearbeitet werden muss.

## 1. Immer zweisprachig — Deutsch UND Englisch, keine Sprachauswahl mehr nötig

**Jeder Newsletter wird verbindlich in beiden Sprachen erstellt** — eine deutsche Version (Sie-
Ansprache) **und** eine eigenständig im MSE-Ton formulierte englische Version (keine wörtliche/
maschinelle Übersetzung, siehe `landing-pages`-Konvention für dieselbe Regel). Es gibt keine
Vorab-Sprachwahl mehr — der komplette Pipeline-Durchlauf (Text → Bilder → Template →
Klaviyo-Draft → Segment-Versand als Entwurf) läuft **einmal pro Sprache**, mit zwei eigenständigen
Templates/Kampagnen/Ausgabeordnern, nie einer gemischt-sprachigen Datei.

Jede Sprachversion bekommt außerdem ihre **eigene, sprachpassende CTA-Ziel-URL** (siehe Abschnitt
1a) und wird als eigener Draft an das **entsprechende Klaviyo-Segment** dieser Sprache gerichtet
(siehe Abschnitt 1b) — beide Sprachversionen sind vollständig eigenständige Kampagnen, nicht nur
zwei Textvarianten derselben Kampagne.

### 1a. URL-Lokalisierung: CTA verlinkt immer auf die sprachpassende Landing-Page-Variante

mse-filterpressen.com nutzt ein bestätigtes Muster für zweisprachige Seiten: die **deutsche Version
liegt auf dem Root-Pfad ohne Sprachpräfix**, die **englische Version liegt unter demselben Pfad mit
vorangestelltem `/en/`**. Bestätigtes Beispiel (CellTRON-Seite):

| Sprache | URL |
|---|---|
| Deutsch | `https://mse-filterpressen.com/celltron/` |
| Englisch | `https://mse-filterpressen.com/en/celltron/` |

Beim Setzen von `{{CTA_URL}}`:
- **Deutsche Newsletter-Version** → CTA verlinkt auf die deutsche (Root-)URL.
- **Englische Newsletter-Version** → CTA verlinkt auf dieselbe Seite mit `/en/`-Präfix.
- Ist die Ziel-Landing-Page ein Ergebnis des `landing-pages`-Bausteins **derselben Kampagne**: dort
  liegt ohnehin nur eine Datei mit eingebautem DE/EN-Umschalter vor (kein separater Pfad pro Sprache)
  — in diesem Fall für beide Newsletter-Sprachversionen dieselbe URL verwenden; der Umschalter auf
  der Landing Page selbst übernimmt die Sprachzuordnung.
- Verlinkt der Newsletter stattdessen auf eine **bestehende Seite der Hauptwebsite** (wie im
  CellTRON-Beispiel): das `/en/`-Präfix-Muster anwenden — aber **nur für Pfade, die der Nutzer
  bestätigt hat oder die bereits als Beispiel belegt sind**. Nicht blind für jede beliebige URL ein
  `/en/`-Pendant annehmen, ohne dass dessen Existenz plausibel/bestätigt ist — im Zweifel kurz
  nachfragen: "Hat die Seite [URL] auch eine englische Version unter `/en/...`?"

### 1b. Klaviyo-Segmente: DE- und EN-Version an das jeweils richtige Segment senden

Jede Sprachversion wird als Draft-Kampagne an ein **eigenes Klaviyo-Segment** dieser Sprache
gerichtet (z. B. ein Segment für deutschsprachige und eines für englischsprachige Kontakte). Da ein
falsch zugeordnetes Segment dazu führen kann, dass Kontakte E-Mails in der falschen Sprache
bekommen, **niemals blind raten**:

1. Verfügbare Segmente über die Klaviyo-MCP-Tools abrufen (sinngemäß `get_segments` — Tool-Name zur
   Laufzeit lokalisieren, siehe Abschnitt 2/Schritt 6).
2. Anhand des Namens ein Segment für Deutsch (z. B. "DE", "Deutsch", "German") und eines für Englisch
   (z. B. "EN", "English") identifizieren.
3. **Ist die Zuordnung nicht eindeutig** (z. B. keine sprachlich benannten Segmente vorhanden, oder
   mehrere infrage kommende Segmente): dem Nutzer die gefundene Segment-Liste zeigen und **explizit
   nachfragen**, welches Segment für welche Sprachversion verwendet werden soll — nicht raten oder
   ein Segment "wahrscheinlich passend" auswählen.
4. Die einmal bestätigte Zuordnung (Segment-ID/-Name je Sprache) in der Kampagnen-Notiz/Ablage
   (Abschnitt 2/Schritt 7) vermerken, damit sie bei künftigen Newslettern wiederverwendet werden kann,
   ohne erneut nachzufragen — bis der Nutzer etwas anderes angibt.

## 2. Pipeline: Thema → fertiger Draft in Klaviyo

### Schritt 1 — Thema entgegennehmen
Thema, Anlass und Kernbotschaft kurz erfassen (i. d. R. bereits von der `marketing-zentrale`
übergeben).

### Schritt 2 — Text erzeugen
Folgende Textbausteine in Sie-Ansprache und im MSE-Content-Flow (BIG HEADLINE → kurze Erklärung →
technisches Wertversprechen → CTA) erzeugen:

- **Betreff** (`{{SUBJECT}}`) — kurz, konkret, kein Clickbait, keine unbelegten Superlative.
- **Preheader** (`{{PREHEADER}}`) — ergänzt den Betreff, keine Wiederholung.
- **Eyebrow** (`{{EYEBROW}}`) — kurzes, getracktes Label in Kleinbuchstaben-Konzept aber Großschreibung
  gemäß Brand (z. B. "PRODUKT-UPDATE", "CASE STUDY").
- **Headline** (`{{HEADLINE}}`) — Satzform (Sentence case), kein AUSSCHLIESSLICH GROSS.
- **Body-Text** (`{{BODY_TEXT}}`) — kurze Sätze, harte Fakten, technische Präzision, keine Filler-Wörter.
- **CTA-Label** (`{{CTA_LABEL}}`) — immer Verb + Outcome (z. B. "Filtrationssystem konfigurieren",
  "Mit unseren Experten sprechen" / EN: "Configure Your Filtration System", "Connect with Our Experts").
- **CTA-Ziel-URL** (`{{CTA_URL}}`) — **immer sprachpassend** setzen (siehe Abschnitt 1a: deutsche
  Version verlinkt auf die deutsche/Root-URL, englische Version auf die `/en/`-Variante, außer die
  Zielseite ist eine `landing-pages`-Seite mit eingebautem Sprachumschalter — dann für beide
  Newsletter-Sprachversionen dieselbe URL verwenden). Vom Nutzer/Kampagnenkontext übernehmen, sonst
  Platzhalter lassen und nachfragen.

Alle Aussagen ausschließlich auf Basis von `CLAUDE.md` / `brand-guidelines.md` bzw. vom Nutzer
gelieferten Fakten. Keine erfundenen Zahlen, Studien oder Kundenaussagen.

### Schritt 3 — Bilder beschaffen
Bilder nicht neu erzeugen, wenn bereits passendes Material existiert. Reihenfolge der Prüfung:

1. Bereits im aktuellen Durchlauf von `bild-video-generierung` erzeugte und freigegebene Bilder.
2. `Outputs/` — frühere, bereits genehmigte Generierungen zum selben Thema/Produkt.
3. `brand/product/` — vorhandenes Produktfotografie-Material.

Erst wenn dort nichts Passendes vorliegt, den Skill `bild-video-generierung` für eine Neu-Generierung
aufrufen. Bildsprache immer: echte Industriefotografie (Filterpressen, Anlagen, technische Details) —
niemals Stockfotos, Cartoons oder generische KI-Abstraktionen.

### Schritt 3b — Logo und Schrift: immer die echten Marken-Assets verwenden

**{{LOGO_URL}} ist Pflicht, kein optionales Extra.** Verwende immer das echte, freigegebene Logo aus
`brand/logo/` (Standardfall: `Logo_06.10.2020_ohne Hintergrund.png`) als gehostete URL — niemals
Klartext ("MSE Filterpressen" als Wort) anstelle des Logos einsetzen, niemals das Logo selbst
nachzeichnen/neu generieren (CellTRON®/MSE® sind geschützte Marken). Der Header-Bereich des Templates
ist bewusst **Light Grey** hinterlegt, weil das vorhandene Logo-Asset dunkel/transparent ist und auf
einem hellen Untergrund den nötigen Kontrast hat (siehe `brand-guidelines.md` §6, "Standard"-Nutzung) —
niemals auf einen dunklen/anthrazitfarbenen Header-Hintergrund wechseln, dafür existiert kein
freigegebenes Weiß-Logo-Asset.

**Optionale Nudica-Einbindung:** Beide Templates enthalten einen auskommentierten `@font-face`-Block
für `{{FONT_URL_REGULAR}}`/`{{FONT_URL_BOLD}}`. Aktivieren, **wenn** die echten Nudica-Dateien aus
`brand/fonts/Nudica/` an einer stabilen, öffentlich erreichbaren URL gehostet werden (z. B. auf
mse-filterpressen.com) — dann zeigen Apple Mail, iOS Mail und viele Webmailer echtes Nudica. Ist keine
gehostete Font-URL vorhanden, den Block auskommentiert lassen: Der `'Nudica', Arial, sans-serif`-Stack
fällt dann kontrolliert auf Arial zurück. Das ist eine bekannte, branchenübliche Einschränkung von
HTML-E-Mail (u. a. Outlook Desktop ignoriert `@font-face` grundsätzlich) — **kein** Zeichen dafür, dass
die Marke ignoriert wird, sondern eine bewusste, dokumentierte Fallback-Entscheidung.

### Schritt 4 — In HTML-Template einsetzen
Eines der beiden Starter-Templates dieses Skills als Basis nehmen (Pfade relativ zum Skill-Verzeichnis
`newsletter-klaviyo/`):

- `templates/newsletter-standard.html` — allgemeines Ankündigungs-/Themen-Mailing.
- `templates/newsletter-produkt.html` — produkt-/technologie-fokussiertes Mailing mit Spec-Raster
  (z. B. für CellTRON-Spezifikationen) und Bild-Split-Layout.

Alle `{{PLATZHALTER}}` im gewählten Template durch die in Schritt 2/3 erzeugten Inhalte ersetzen.
Beim Produkt-Template zusätzlich `{{SPEC_ROWS}}` durch generierte Label/Value-Zeilen ersetzen (siehe
Kommentar im Template für das erwartete HTML-Fragment). Bild-Platzhalter (`{{HEADER_IMAGE_URL}}` etc.)
durch finale, gehostete Bild-URLs ersetzen (z. B. aus Klaviyo-Bildbibliothek oder Outputs-Ablage,
sobald ein extern erreichbarer Link vorliegt).

### Schritt 5 — Qualitätssicherung (siehe Checkliste unten)
Vor dem Anlegen in Klaviyo den fertigen HTML-Inhalt gegen die Checkliste in Abschnitt 4 prüfen.

### Schritt 6 — Klaviyo MCP: Template, Kampagne, Zuordnung
Die Klaviyo-MCP-Tools sind in der aktuellen Session unter session-spezifischen Serverpräfixen
verfügbar (das Präfix ändert sich je nach Installation). Vor der Nutzung die passenden Tools per
Tool-Suche lokalisieren, z. B. mit Suchbegriffen wie `"klaviyo campaign template"`,
`"create email template"` oder `"assign template campaign message"` — niemals ein festes
Server-Präfix fest verdrahten.

Konzeptioneller Ablauf (Tool-Namen sinngemäß, je nach Session ggf. leicht abweichend) — **einmal pro
Sprachversion durchlaufen**:

1. **E-Mail-Template anlegen** (sinngemäß `create_email_template`) mit dem fertigen, QA-geprüften
   HTML aus Schritt 4/5 der jeweiligen Sprachversion.
2. **Passendes Segment bestimmen** (sinngemäß `get_segments`, siehe Abschnitt 1b) — DE-Version an das
   deutschsprachige Segment, EN-Version an das englischsprachige Segment. Bei Unklarheit den Nutzer
   fragen statt zu raten.
3. **Kampagne anlegen** (sinngemäß `create_campaign`) mit Betreff, Preheader und dem in Schritt 2
   bestimmten Segment als Zielgruppe.
4. **Template der Kampagnen-Message zuordnen** (sinngemäß `assign_template_to_campaign_message`).

**Wichtige Regel — niemals automatisch versenden:** Das Ergebnis dieses Ablaufs ist ausschließlich
eine **Draft-Kampagne** in Klaviyo. Es wird zu keinem Zeitpunkt ein Versand-, Schedule- oder
"Send now"-Tool aufgerufen. Der Versand erfolgt ausschließlich manuell durch einen Menschen nach
Prüfung im Klaviyo-Interface.

### Schritt 7 — Ablage
Eine Kopie des finalen HTML sowie eine kurze Meta-Notiz speichern unter:

```
Outputs/<datum>-<thema>-newsletter-<sprache>/
  newsletter.html
  meta.txt   (Thema, Sprache, Betreff, CTA-URL, verwendetes Klaviyo-Segment (ID/Name),
              Klaviyo-Kampagnen-ID/-Name, Erstellungsdatum, Status: Draft)
```

Datum im Format `JJJJ-MM-TT`, Thema kurz und dateinamenfreundlich (Kleinbuchstaben, Bindestriche),
Sprache als `de` bzw. `en` — **immer beide Ordner anlegen**, da jeder Newsletter zweisprachig läuft.

## 3. Hinweis: Sending Domain, DNS und API-Key-Verwaltung (nicht Teil dieses Laufs)

Die dedizierte Sending Domain, DNS-Konfiguration (SPF/DKIM/DMARC) sowie die sichere Verwaltung des
Klaviyo-API-Keys sind **einmalige Onboarding-Aufgaben**, kein Bestandteil des Pro-Newsletter-Ablaufs.
Diese Einrichtung erfolgt separat beim Setup der Anbindung; die Zugangsdaten liegen konzeptionell in
der MCP-/Umgebungskonfiguration der Session (nicht in diesem Skill oder in Projektdateien). Dieser
Skill geht davon aus, dass die Anbindung bereits funktionsfähig ist. Gibt es Hinweise auf
Zustellbarkeitsprobleme oder fehlende Autorisierung, den Nutzer darauf hinweisen, dass dies ein
Onboarding-/Infrastruktur-Thema ist, statt es hier zu lösen.

## 4. QA-Checkliste vor Abschluss (Draft erst dann als "fertig" markieren)

- [ ] Farben im HTML korrekt: Fast White dominant, MSE Blue `#3498DB` nur als Akzent (CTA/Link,
      max. 10–15 % der Fläche), Anthracite Black `#1B1B1B` nur als Akzent-Band/-Box, kein
      vollflächiges Schwarz, kein Grün/Rot außer bei Eco:LOGIC-Inhalten.
- [ ] Typografie: `font-family: 'Nudica', Arial, sans-serif` für Headline und Body, Headline in
      Sentence case (nicht GROSSBUCHSTABEN), Eyebrow als kleine, getrackte Großbuchstaben-Zeile in
      Medium Grey. Falls eine gehostete Nudica-Font-URL vorliegt: `@font-face`-Block aktiviert?
- [ ] **{{LOGO_URL}} zeigt auf das echte Logo-Asset aus `brand/logo/`** — kein Klartext-Ersatz, kein
      selbst nachgezeichnetes/generiertes Logo, Header-Hintergrund bleibt Light Grey (Kontrastgrund
      für das dunkle Logo)?
- [ ] **Beide Sprachversionen (DE + EN) vollständig erstellt** — nicht nur eine, außer der Nutzer hat
      ausdrücklich nach nur einer Sprache verlangt?
- [ ] Anrede korrekt: durchgehend "Sie"-Form (bzw. formelles Englisch bei EN-Version). Englische
      Version eigenständig im MSE-Ton formuliert, keine wörtliche/maschinelle Übersetzung?
- [ ] Sprache korrekt und konsistent (keine Sprachmischung innerhalb einer Version).
- [ ] **CTA-URL sprachpassend** — DE-Version verlinkt auf die deutsche/Root-URL, EN-Version auf die
      `/en/`-Variante (bzw. dieselbe URL, falls Ziel eine `landing-pages`-Seite mit eingebautem
      Sprachumschalter ist)?
- [ ] **Jede Sprachversion wurde an das dafür bestätigte Klaviyo-Segment gerichtet** — Zuordnung mit
      dem Nutzer abgeglichen, nicht geraten?
- [ ] CTA-Label = Verb + Outcome, kein reines "Mehr erfahren" ohne Kontext.
- [ ] Gesetzlicher Footer vollständig und unverändert vorhanden (siehe Template), inkl.
      `{{ unsubscribe_link }}`.
- [ ] Schreibweise CellTRON® / MSE® korrekt (Markenzeichen an der ersten Nennung).
- [ ] Keine Wettbewerber namentlich genannt.
- [ ] Keine erfundenen Zahlen, Studien, Kundenzitate oder unbelegten Claims — alles auf
      `CLAUDE.md`/`brand-guidelines.md` bzw. Nutzerangaben rückführbar.
- [ ] Bildsprache: echte Industriefotografie, keine Stockfotos/Cartoons/generische KI-Abstraktion.
- [ ] Klaviyo-Kampagne liegt als **Draft** vor — kein Versand-/Schedule-Tool wurde aufgerufen.
