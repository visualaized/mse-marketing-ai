---
description: "Erstellt einen markenkonformen X-Post (Englisch, kurz und pointiert, max. 280 Zeichen) und übernimmt auf Wunsch Veröffentlichung/Planung über Upload-Post. Triggert bei 'X-Post erstellen', 'Tweet schreiben', 'Post für X/Twitter' oder wenn die Marketing-Zentrale den Kanal X auswählt."
disable-model-invocation: false
---

# Social Media — X (Twitter) — MSE Filterpressen GmbH

Dieser Baustein erzeugt einen fertigen X-Post für MSE Filterpressen und übergibt ihn nach kurzer
Freigabe an Upload-Post zur Veröffentlichung oder Planung.

## 1. Wann dieser Baustein läuft

- Der Nutzer will explizit einen X-Post (Tweet) erstellen lassen.
- Die Marketing-Zentrale hat im Rahmen eines Themas den Kanal X ausgewählt.
- Der Nutzer bittet um Post-Text oder direkte Veröffentlichung/Planung für X.

## 2. Pflichtschritt: Markenkern IMMER zuerst laden

Bevor du irgendeinen Text erzeugst, lies **in dieser Reihenfolge** (relativ zum aktuellen
Arbeitsverzeichnis, dem Marketing-Hub-Root des Kunden):

1. `CLAUDE.md` — kompaktes Master-Brand-Dokument.
2. `brand/brand-guidelines.md` — vollständiges Regelwerk, insbesondere Kapitel zu Tonalität und Kanälen.
3. `brand/color-palette.json` — maschinenlesbare, verbindliche Farbwerte (relevant für das begleitende
   Visual).

Diese drei Dateien sind die einzige verbindliche Quelle für Tonalität, Sprache, Claims und Do's/Don'ts.
**Erfinde niemals eigene Markenfakten, Zahlen oder Claims** — auch nicht, wenn sie plausibel klingen.
Fehlt eine Angabe, frage kurz nach, statt zu raten. Existieren diese Dateien nicht, stoppe und weise
darauf hin, dass Claude im Marketing-Hub-Ordner des Kunden gestartet werden muss.

## 3. Sprache & Tonalität — verbindlich, nicht verhandelbar

- **Immer Englisch.** X-Posts werden für MSE ausschließlich auf Englisch verfasst — unabhängig davon,
  in welcher Sprache das Thema angeliefert wurde.
- **Tonalität:** dasselbe professionelle, engineering-first Register wie LinkedIn, aber angepasst an
  X's kürzeres, schnelleres Format — kein aggressiver Sales-Ton, keine Ausrufezeichen-Kaskaden.
- Keine Wettbewerbernennung (Andritz, Aquachem, Diemme, Filox etc.) in nach außen gerichtetem Content.
- Korrekte Schreibweise: CellTRON® (internes Großgeschriebenes T beachten), CellTRON Xtreme,
  CellTRON Light, MSE Filterpressen®.

## 4. Post-Struktur

1. **Ein scharfer Hard-Statement-Hook** — die gesamte Kernaussage in einem Satz, direkt am Anfang.
2. **Optional eine kurze unterstützende Zeile** — nur falls sie echten Mehrwert liefert, nicht
   erzwingen.
3. **CTA/Link** — kurz, Verb + Outcome (siehe Abschnitt 6).

## 5. Längenvorgabe — strikt einhalten

- X-Limit: **280 Zeichen pro Post.**
- MSE-Posts bleiben bewusst knapp: Zielkorridor **ca. 200-260 Zeichen**, damit noch Platz für einen
  Link bleibt.
- Für einen längeren Gedanken ist ein **kurzer Thread aus 2-3 Posts** akzeptabel — aber der **erste
  Post muss für sich allein als Hook funktionieren** (darf nicht wie ein abgeschnittener Satz wirken).
- Vor der Auslieferung Zeichen zählen und im Zielkorridor bleiben — nicht auf Schätzung verlassen.

## 6. CTA-Stil

Immer Englisch, kurz, Verb + Outcome. Beispiele:

- "See how ↗"
- "Read the case ↗"
- "Explore the process ↗"

Direkt gefolgt vom Link (sofern vorhanden).

## 7. Hashtag-Strategie

X-Konvention: **1-3 Hashtags maximal**, weniger als auf Instagram. Beispiele:

`#Filtration` `#BatteryRecycling` `#ProcessEngineering`

Nicht das knappe Zeichenbudget mit Hashtags überladen — im Zweifel lieber weniger Hashtags und mehr
Substanz im Text.

## 8. Pflichtfrage: reine Bilder oder Text-/Info-Content (Mehrbild-Post)?

**Bevor ein Visual beschafft wird, immer zuerst fragen** (falls die `marketing-zentrale` das nicht
schon geklärt hat):

> "Soll der Post mit einem reinen Bild/Video arbeiten, oder sollen Headings, Text und CTA direkt in
> die Grafik eingebaut werden — z. B. als Mehrbild-Post?"

**Fall A — reine Bilder:** Weiter wie in Abschnitt 8a. **Fall B — Text-/Info-Content
(Mehrbild-Post):** Mehrere Bilder (X erlaubt bis zu 4 pro Post) mit eingebauter Headline/Kernaussage/
CTA — siehe Abschnitt 8b.

### 8a. Reine Bilder

- Das Visual muss aus dem `bild-video-generierung`-Skill stammen **oder** ein bereits vorhandenes,
  genehmigtes Asset aus `brand/product/`, `brand/generated-references/` oder `Outputs/` sein.
- Erzeuge selbst kein Bild in diesem Baustein — falls noch kein Visual vorliegt, rufe zuerst
  `bild-video-generierung` auf (Format i. d. R. 16:9 oder 1.91:1 Querformat für X).
- Orientiere dich am dokumentierten Social-Post-Bildkonvention aus den Brand Guidelines: häufig
  dunkler/anthrazitfarbener Hintergrund mit weißer Nudica-Typografie, großformatiges reales
  Industriefoto, blaues Bildzeichen als Akzent, getrackte graue Eyebrow-Label, Headline in Sentence
  Case.

### 8b. Mehrbild-Post mit Text/Headings/CTA (Fall B)

- **Immer perfekt auf die Kampagne abgestimmt** — dieselben Kernaussagen wie in Newsletter/Landing
  Page derselben Kampagne, kein isoliert erfundener Zusatzinhalt. Vorhandenes
  `Campaigns/<slug>/meta.json` als Kontext nutzen.
- **Erzeugung über `bild-video-generierung`, Abschnitt 8** (`scripts/compose_slide.py`) — jedes Bild
  mit **echter Nudica-Schrift und echtem Logo/Bildzeichen** (Pflicht). X erlaubt **maximal 4 Bilder**
  pro Post — bei diesem knappen Format reichen meist 2-3 Bilder. **Verbindliches Pixelmaß für X:**
  `1600x900` (16:9, Standardfall im Feed) oder `1200x1200` (1:1, falls ein quadratisches Set gewünscht
  ist):
  1. **Erstes Bild:** der Hard-Statement-Hook aus Abschnitt 4 als Headline im Bild.
  2. **Optional 1-2 weitere Bilder:** je eine kurze unterstützende Aussage.
  3. **Letztes Bild (falls ein CTA-Bild gewünscht ist):** kurze CTA-Pille.
  - Hintergrundbilder zuerst aus bereits genehmigten Kampagnen-Bildern beziehen (`Outputs/`,
    `brand/product/`), siehe `bild-video-generierung` Abschnitt 4.
  - **Nicht jedes Bild braucht ein Foto:** für eine reine Fakten-/Zahlen-Aussage oder ein Schaubild
    `compose_slide.py --bg-color` (statt `--background`) mit `--dark-text` verwenden statt ein Foto zu
    erzwingen.
  - **Alle Sonderzeichen (auch in deutschen Produktnamen/Zitaten) korrekt und nativ setzen, niemals
    ASCII-Ersatz** ("ue"/"ae"/"oe"/"ss") — auch nicht in Kommandozeilen-Aufrufen von `compose_slide.py`.
  - Alle Bilder als **eine Bild-Liste** an denselben Upload-Post-Aufruf übergeben, damit sie als ein
    Post mit mehreren Bildern veröffentlicht werden (nicht als separate Posts).
  - Der kurze Post-Text (Abschnitt 4/5) bleibt bestehen — die Bilder verstärken die Aussage, ersetzen
    den Text aber nicht; Zeichenlimit gilt weiterhin nur für den Text, nicht für Bildinhalte.

## 9. Ablauf: Generierung → Freigabe → Veröffentlichung/Planung

1. **Generierung:** Post-Text (inkl. optionalem Thread), Hashtags und CTA nach obigem Schema erstellen;
   Zeichenanzahl prüfen; passendes Visual referenzieren oder beschaffen.
2. **Freigabe:** Fertigen Post (vollständiger Text inkl. Zeichenanzahl + referenziertes Bild/Video) dem
   Nutzer zeigen und eine **kurze Go/No-Go-Bestätigung** einholen. Es gibt bewusst keinen komplexen
   Freigabeprozess — eine einfache Bestätigung genügt.
3. **Veröffentlichung/Planung:** Nach Freigabe fragen, ob **sofort veröffentlicht** oder auf ein
   bestimmtes **Datum/Uhrzeit geplant** werden soll. Dann die Upload-Post-MCP-Tools nutzen
   (`upload_photos`/`upload_video` für das Asset, ggf. `upload_text`, jeweils mit dem passenden
   Platform-Parameter für X — je nach Tool `x` oder `twitter`, im Zweifel das Enum des jeweiligen
   Upload-Post-Tools zur Laufzeit prüfen; Planung über die entsprechenden Scheduled-Post-Parameter bzw.
   `list_scheduled`/`edit_scheduled`/`cancel_scheduled` zur Verwaltung). Prüfe die exakten Tool-Namen und
   Parameter zur Laufzeit in der aktuellen Session (Installationen können variieren) — nicht blind eine
   feste Tool-ID annehmen.
4. Hinweis: Für Upload-Post fallen aktuell ca. 19 €/Monat an, die der Kunde selbst trägt
   (informativer Hinweis, nicht weiter vertiefen).

## 10. Ablage

Fertigen Post-Text (inkl. Zeichenanzahl), Hashtags, CTA und Referenz auf das verwendete Bild/Video
speichern unter `Outputs/<datum>-<thema>-x/` (z. B.
`Outputs/2026-07-01-celltron-xtreme-batterierecycling-x/`).

## 11. QA-Checkliste vor Auslieferung

- **Nutzer wurde gefragt, ob reine Bilder oder Text-/Info-Content (Mehrbild-Post) gewünscht sind** —
  nicht stillschweigend angenommen?
- Zeichenanzahl innerhalb des Limits (max. 280, Zielkorridor ca. 200-260)?
- Post vollständig auf Englisch?
- Erster Post eines etwaigen Threads funktioniert eigenständig als Hook?
- Keine Wettbewerbernennung?
- Korrekte Schreibweise CellTRON®/MSE Filterpressen®?
- Hashtags maximal 1-3, nicht überladen?
- CTA vorhanden, kurz, Verb + Outcome?
- Visual(s) stammen aus `bild-video-generierung`, `brand/product/`, `brand/generated-references/` oder
  `Outputs/`?
- **Bei Mehrbild-Post (Fall B):** maximal 4 Bilder, Format durchgängig `1600x900` oder `1200x1200`,
  jede Slide mit echter Nudica-Schrift und echtem Logo/Bildzeichen (über `compose_slide.py`), Inhalte
  stimmen mit der übrigen Kampagne überein, alle Bilder als **ein** Post übergeben?
- **Alle Sonderzeichen (ü/ä/ö/ß) korrekt und nativ gesetzt**, kein ASCII-Ersatz, auch nicht in
  deutschen Produktnamen/Zitaten innerhalb des sonst englischen Posts?
