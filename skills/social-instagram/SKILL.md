---
description: "Erstellt einen markenkonformen Instagram-Post (Caption + Hashtags + CTA, immer Deutsch) und übernimmt auf Wunsch Veröffentlichung/Planung über Upload-Post. Triggert bei 'Instagram-Post erstellen', 'Post für Instagram', 'IG-Caption schreiben' oder wenn die Marketing-Zentrale den Kanal Instagram auswählt."
disable-model-invocation: false
---

# Social Media — Instagram — MSE Filterpressen GmbH

Dieser Baustein erzeugt einen fertigen Instagram-Post (Caption, Hashtags, CTA) für MSE Filterpressen
und übergibt ihn nach kurzer Freigabe an Upload-Post zur Veröffentlichung oder Planung.

## 1. Wann dieser Baustein läuft

- Der Nutzer will explizit einen Instagram-Post erstellen lassen.
- Die Marketing-Zentrale hat im Rahmen eines Themas den Kanal Instagram ausgewählt.
- Der Nutzer bittet um Caption-Text, Hashtags oder direkte Veröffentlichung/Planung für Instagram.

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

- **Immer Deutsch.** Instagram-Posts werden für MSE ausschließlich auf Deutsch verfasst — unabhängig
  davon, in welcher Sprache das Thema angeliefert wurde.
- **Tonalität: "etwas lockerer, aber weiterhin professionell."** Instagram ist zugänglicher und
  bildgetriebener als LinkedIn, bleibt aber premium Engineering — niemals Consumer-Sound, niemals
  platt verkäuferisch, keine Ausrufezeichen-Kaskaden, keine generischen Hashtag-Floskeln.
- **Anrede:** "Sie" für kundengerichteten Content (Standardfall). "Du" ausschließlich bei
  Recruiting-Content (Stellenanzeigen, Karriere-Posts) — im Zweifel beim Nutzer nachfragen, welcher Fall
  vorliegt.
- Englische Claims/Taglines (z. B. "Beyond Filtration", "The Future of Filtration", "Engineered for
  Excellence") dürfen als stilistischer Akzent auch in einem deutschen Post verwendet werden — ganze
  Captions bleiben aber Deutsch.
- Keine Wettbewerbernennung (Andritz, Aquachem, Diemme, Filox etc.) in nach außen gerichtetem Content.
- Korrekte Schreibweise: CellTRON® (internes Großgeschriebenes T beachten), CellTRON Xtreme,
  CellTRON Light, MSE Filterpressen®.

## 4. Caption-Struktur

Jede Instagram-Caption folgt dem Aufbau:

1. **Hook-Zeile** — eine harte, prägnante Aussage direkt am Anfang (entspricht der großen Headline im
   Content-Flow-Muster: BIG HEADLINE → kurze Erklärung → Nutzen/technischer Mehrwert → CTA).
2. **Kurzer Fließtext** — 3-6 kurze Sätze/Zeilen, die die Aussage einordnen und den technischen/
   praktischen Nutzen greifbar machen. Kurze Sätze, keine Füllwörter, keine unbelegten Superlative.
3. **CTA** — Verb + Outcome, siehe Abschnitt 6.
4. **Hashtag-Block** — abgesetzt am Ende (siehe Abschnitt 5).

## 5. Länge & Lesbarkeit

- Die **ersten ca. 125-150 Zeichen** sind in der Feed-Vorschau sichtbar, bevor Instagram "…mehr
  anzeigen" einblendet — die Hook-Zeile muss also innerhalb dieses Fensters die Kernaussage
  transportieren.
- Instagram erlaubt bis zu ca. 2.200 Zeichen — MSE-Posts bleiben aber bewusst **knapp und scannbar**:
  insgesamt etwa **3-6 kurze Sätze/Zeilen** vor dem CTA, keine langen Textblöcke.
- Zeilenumbrüche nutzen, um die Caption optisch in kurze, gut lesbare Häppchen zu gliedern (kein
  Fließtext-Block).

## 6. CTA-Stil

Verb + Outcome, wie im Markenkern definiert — auf Instagram darf der CTA auf Deutsch formuliert werden,
da der gesamte Post Deutsch ist. Beispiele:

- "Jetzt Anwendungsbereiche entdecken ↗"
- "Mehr zur CellTRON Xtreme erfahren ↗"
- "Filtrationslösung konfigurieren ↗"

Kein generisches "Mehr erfahren" ohne konkreten Outcome, kein reiner Produktverkaufston.

## 7. Hashtag-Strategie

- **Ca. 5-10 relevante Hashtags**, kein Hashtag-Spam.
- Mischung aus:
  - **Marken-Hashtags:** `#MSEFilterpressen` `#Filtration` `#Filterpresse` `#CellTRON`
  - **Themen-/Branchen-Hashtags**, passend zum konkreten Thema: `#Batterierecycling`
    `#Hydrometallurgie` `#Verfahrenstechnik` `#Industrietechnik` `#Prozesstechnik`
    `#Fest-Flüssig-Trennung`
- Hashtags immer inhaltlich zum Thema passend wählen, nicht pauschal dieselbe Liste kopieren.

## 8. Pflichtfrage: reine Bilder oder Text-/Info-Content (Carousel)?

**Bevor ein Visual beschafft wird, immer zuerst fragen** (falls die `marketing-zentrale` das nicht
schon geklärt hat):

> "Soll der Post mit einem reinen Bild/Video arbeiten, oder sollen Headings, Text und CTA direkt in
> die Grafik eingebaut werden — z. B. als Carousel mit mehreren Slides?"

**Fall A — reine Bilder:** Weiter wie in Abschnitt 8a beschrieben (ein Bild/Video, Text nur in der
Caption).

**Fall B — Text-/Info-Content (Carousel):** Ein mehrteiliges Instagram-Carousel erzeugen, bei dem
Headline, kurze Kernaussagen und CTA **direkt in die Bilder eingebaut** sind (nicht nur in der
Caption) — siehe Abschnitt 8b.

### 8a. Reine Bilder

- Das Visual muss aus dem `bild-video-generierung`-Skill stammen **oder** ein bereits vorhandenes,
  genehmigtes Asset aus `brand/product/`, `brand/generated-references/` oder `Outputs/` sein.
- Erzeuge selbst kein Bild in diesem Baustein — falls noch kein Visual vorliegt, rufe zuerst
  `bild-video-generierung` auf (Format i. d. R. 1:1 quadratisch oder 4:5 Hochformat für den Feed).
- Orientiere dich am dokumentierten Social-Post-Bildkonvention aus den Brand Guidelines: häufig
  dunkler/anthrazitfarbener Hintergrund mit weißer Nudica-Typografie, großformatiges reales
  Industriefoto, blaues Bildzeichen als Akzent, getrackte graue Eyebrow-Label (z. B.
  "BEYOND FILTRATION"), Headline in Sentence Case.

### 8b. Carousel mit Text/Headings/CTA (Fall B)

- **Immer perfekt auf die Kampagne abgestimmt:** Die Slide-Inhalte (Headline, Kernaussagen, CTA)
  müssen zur selben Botschaft passen wie die übrigen Bausteine derselben Kampagne (Newsletter,
  Landing Page) — dieselben Kernfakten, keine widersprüchlichen oder frei erfundenen Zusatzaussagen.
  Existiert bereits ein `Campaigns/<slug>/meta.json` für dieses Thema, dessen Inhalt/Notizen als
  Kontext heranziehen statt den Post isoliert neu zu erfinden.
- **Erzeugung über `bild-video-generierung`, Abschnitt 8** (`scripts/compose_slide.py`) — dieser Skill
  liefert für jede Slide ein fertiges, flaches Bild mit **echter Nudica-Schrift und echtem Logo/
  Bildzeichen** (nicht optional, siehe dortige Vorgaben). **Verbindliches Pixelmaß für Instagram:**
  `1080x1350` (4:5, Standardfall für Feed-Carousel, maximale vertikale Fläche in der App) oder
  `1080x1080` (1:1, wenn ein quadratisches Raster gewünscht ist) — niemals andere Seitenverhältnisse
  für Instagram-Carousels verwenden, da Instagram sie sonst zuschneidet. Typisch 3-6 Slides:
  1. **Cover-Slide:** Eyebrow + Hook-Headline (die stärkste Aussage der Kampagne).
  2. **1-2 Value-Slides:** je eine kurze Kernaussage/ein Vorteil (Headline + 1 kurzer Body-Satz),
     analog zu den Feature-Aussagen aus der Landing Page/dem Newsletter derselben Kampagne.
  3. **Optional weitere Detail-Slide(s):** technische Details, Anwendungsfall, o. ä.
  4. **CTA-Slide (letzte Slide):** kurze Abschluss-Headline + CTA-Pille (Verb + Outcome, siehe
     Abschnitt 6) — `--index` auf jeder Slide setzen (z. B. "1/4"…"4/4") als Swipe-Orientierung.
  - Hintergrundbilder je Slide: bereits genehmigte Kampagnen-Bilder aus `Outputs/`/`brand/product/`
    zuerst prüfen (siehe `bild-video-generierung` Abschnitt 4), pro Slide gern unterschiedliche
    Perspektiven/Ausschnitte desselben Produkts verwenden, damit das Carousel visuell variiert wirkt.
  - **Nicht jede Slide braucht ein Foto:** Für Schaubilder, Zahlen/Fakten-Slides oder reine
    Aussage-Slides `compose_slide.py --bg-color` (statt `--background`) mit `--dark-text` verwenden —
    liefert eine saubere, markenkonforme Flächenfarbe (z. B. Light Grey `#F5F5F5` oder Fast White) statt
    eines Fotos. Auch hier gilt: immer echte Nudica-Schrift, nie ein Foto erzwingen, wo ein reines
    Text-/Diagramm-Slide klarer wirkt. Ein Foto nur einsetzen, wenn es inhaltlich etwas zeigt (Produkt,
    Anwendung) — nicht als reine Dekoration auf jeder Slide.
  - **Umlaute immer korrekt, niemals ASCII-Ersatz:** ü/ä/ö/ß in jedem Slide-Text exakt so eingeben wie
    geschrieben (z. B. "Für", "Vollständig", "Maßgeschneiderte") — niemals "ue"/"ae"/"oe"/"ss" als
    Ersatz verwenden, auch nicht in Kommandozeilen-Aufrufen von `compose_slide.py`. Die Nudica-Schrift
    enthält alle deutschen Sonderzeichen vollständig; ASCII-Ersatz ist ausschließlich ein
    Autoren-/Eingabefehler, kein technisches Font-Problem.
  - Alle fertigen Slide-PNGs werden gemeinsam als **ein Carousel-Post** an Upload-Post übergeben
    (mehrere Bildpfade in einem `upload_photos`-Aufruf bzw. dem für Carousels vorgesehenen
    Parameter — exakten Parameter-Namen zur Laufzeit prüfen, siehe Abschnitt 9).
  - Die Caption bleibt trotzdem vollständig (Hook, Fließtext, CTA, Hashtags wie gewohnt) — die
    Slide-Texte wiederholen die Kernaussagen visuell, ersetzen die Caption aber nicht.

## 9. Ablauf: Generierung → Freigabe → Veröffentlichung/Planung

1. **Generierung:** Caption, Hashtags und CTA nach obigem Schema erstellen; passendes Visual referenzieren
   oder beschaffen.
2. **Freigabe:** Fertigen Post (vollständige Caption-Vorschau + referenziertes Bild/Video) dem Nutzer
   zeigen und eine **kurze Go/No-Go-Bestätigung** einholen. Es gibt bewusst keinen komplexen
   Freigabeprozess — eine einfache Bestätigung genügt.
3. **Veröffentlichung/Planung:** Nach Freigabe fragen, ob **sofort veröffentlicht** oder auf ein
   bestimmtes **Datum/Uhrzeit geplant** werden soll. Dann die Upload-Post-MCP-Tools nutzen
   (`upload_photos`/`upload_video` für das Asset, ggf. `upload_text`, jeweils mit Platform-Parameter
   `instagram`; Planung über die entsprechenden Scheduled-Post-Parameter bzw. `list_scheduled`/
   `edit_scheduled`/`cancel_scheduled` zur Verwaltung). **Bei einem Carousel (Fall B) alle Slide-Bilder
   gemeinsam als eine Bild-Liste an denselben `upload_photos`-Aufruf übergeben**, damit Instagram sie
   als ein einziges Mehrbild-Carousel veröffentlicht, nicht als mehrere Einzelposts — Parameter-Name
   für Mehrfachbilder zur Laufzeit prüfen (Installationen können variieren). Prüfe generell die exakten
   Tool-Namen und Parameter zur Laufzeit in der aktuellen Session — nicht blind eine feste Tool-ID
   annehmen.
4. Hinweis (einmalig, informativ): Für Upload-Post fallen aktuell **ca. 19 €/Monat** an, die der Kunde
   selbst trägt. Nicht weiter thematisieren, nur sachlich erwähnen falls relevant.

## 10. Ablage

Fertige Caption, Hashtags, CTA und Referenz auf das verwendete Bild/Video speichern unter
`Outputs/<datum>-<thema>-instagram/` (z. B. `Outputs/2026-07-01-celltron-xtreme-batterierecycling-instagram/`).

## 11. QA-Checkliste vor Auslieferung

- **Nutzer wurde gefragt, ob reine Bilder oder Text-/Info-Content (Carousel) gewünscht sind** — nicht
  stillschweigend angenommen?
- Post vollständig auf Deutsch?
- Richtige Anrede: "Sie" bei kundengerichtetem Content, "Du" nur bei Recruiting-Content?
- Keine Wettbewerbernennung?
- Korrekte Schreibweise CellTRON®/MSE Filterpressen®?
- Hashtags thematisch relevant, ca. 5-10 Stück, kein Spam?
- CTA-Stil = Verb + Outcome?
- Visual(s) stammen aus `bild-video-generierung`, `brand/product/`, `brand/generated-references/` oder
  `Outputs/` — kein neu erfundenes/nicht markenkonformes Bild?
- **Bei Carousel (Fall B):** jede Slide nutzt echte Nudica-Schrift und echtes Logo/Bildzeichen (über
  `compose_slide.py`, nicht selbstgebaut), Format durchgängig `1080x1350` oder `1080x1080`, Inhalte
  stimmen mit der übrigen Kampagne überein (Newsletter/Landing Page derselben Kampagne), alle Slides
  wurden als **ein** Carousel-Post übergeben (nicht als mehrere Einzelposts)?
- **Alle Umlaute (ü/ä/ö/ß) korrekt und nativ gesetzt** — in Caption UND in jedem Slide-Text — kein
  ASCII-Ersatz ("ue"/"ae"/"oe"/"ss") an irgendeiner Stelle?
- Caption knapp und scannbar (3-6 kurze Sätze/Zeilen), Hook in den ersten ca. 125-150 Zeichen erkennbar?
