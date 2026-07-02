---
description: "Erstellt einen markenkonformen LinkedIn-Post (Thought-Leadership-Text auf Englisch + Hashtags + CTA) und übernimmt auf Wunsch Veröffentlichung/Planung über Upload-Post. Triggert bei 'LinkedIn-Post erstellen', 'Post für LinkedIn' oder wenn die Marketing-Zentrale den Kanal LinkedIn auswählt."
disable-model-invocation: false
---

# Social Media — LinkedIn — MSE Filterpressen GmbH

Dieser Baustein erzeugt einen fertigen LinkedIn-Post für MSE Filterpressen und übergibt ihn nach kurzer
Freigabe an Upload-Post zur Veröffentlichung oder Planung.

## 1. Wann dieser Baustein läuft

- Der Nutzer will explizit einen LinkedIn-Post erstellen lassen.
- Die Marketing-Zentrale hat im Rahmen eines Themas den Kanal LinkedIn ausgewählt.
- Der Nutzer bittet um Post-Text, Hashtags oder direkte Veröffentlichung/Planung für LinkedIn.

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

- **Immer Englisch.** LinkedIn-Posts werden für MSE ausschließlich auf Englisch verfasst — unabhängig
  davon, in welcher Sprache das Thema angeliefert wurde.
- **Tonalität: "sehr professionell" — Thought-Leadership-Register.** Technische Tiefe steht vor
  Produktwerbung. Zielgruppe: internationale technische/kaufmännische Entscheider (Process Engineers,
  Plant Engineers, Procurement, C-Level) sowie Fachmedien/Multiplikatoren.
- Inhaltlich bevorzugte Themenfelder: Battery Recycling, Hydrometallurgy, anspruchsvolle
  Filtration/Specialty Chemicals — wo das Thema es hergibt, diese Tiefe suchen statt oberflächlicher
  Produktwerbung.
- Kurze, klare Sätze; harte Fakten statt Superlative; kein Marketing-Sprech, keine generischen
  Branchenfloskeln.
- Keine Wettbewerbernennung (Andritz, Aquachem, Diemme, Filox etc.) in nach außen gerichtetem Content.
- Korrekte Schreibweise: CellTRON® (internes Großgeschriebenes T beachten), CellTRON Xtreme,
  CellTRON Light, MSE Filterpressen®.

## 4. Post-Struktur

1. **Starke Opening-Hook-Zeile** — eine harte Aussage/ein Fakt, der sofort Aufmerksamkeit verdient
   (entspricht der BIG-HEADLINE-Logik des Markenkerns).
2. **Kurzer Fließtext mit technischer Substanz** — macht einen echten inhaltlichen Punkt, keine reine
   Werbebotschaft. Kurze Absätze von 1-3 Zeilen für Lesbarkeit.
3. **Optionale Bullet-Liste** mit 2-4 technischen Vorteilen/Fakten — nur wenn es dem Thema dient, nicht
   erzwingen.
4. **CTA** — Verb + Outcome, siehe Abschnitt 6.
5. **Hashtag-Block** am Ende (siehe Abschnitt 7).

## 5. Länge & Format

- Richtwert: **ca. 900-1.300 Zeichen / ca. 100-200 Wörter.** LinkedIn belohnt zwar längere,
  durchdachte Posts, aber der MSE-Stil bevorzugt Präzision vor Länge.
- Für echte Thought-Leadership-/technische Deep-Dive-Themen darf der Post **länger** ausfallen, wenn der
  Inhalt es rechtfertigt — nie künstlich strecken, nur um Länge zu erreichen.
- Kurze Absätze (1-3 Zeilen), großzügige Zeilenumbrüche für Scanbarkeit — keine langen Textblöcke.

## 6. CTA-Stil

Immer Englisch, Verb + Outcome. Beispiele:

- "Explore how CellTRON Xtreme performs in battery recycling ↗"
- "See the engineering behind the process ↗"
- "Connect with our process engineers ↗"

Kein reiner Produktverkaufston, kein "Learn more" ohne konkreten Outcome.

## 7. Hashtag-Strategie

LinkedIn-Konvention: **3-5 fokussierte Hashtags** am Ende, keine Hashtag-Häufung. Beispiele je nach
Thema:

`#FiltrationTechnology` `#BatteryRecycling` `#Hydrometallurgy` `#ProcessEngineering`
`#IndustrialEngineering`

Immer passend zum konkreten Thema auswählen, nicht pauschal dieselbe Liste kopieren.

## 8. Pflichtfrage: reine Bilder oder Text-/Info-Content (Mehrbild-Post)?

**Bevor ein Visual beschafft wird, immer zuerst fragen** (falls die `marketing-zentrale` das nicht
schon geklärt hat):

> "Soll der Post mit einem reinen Bild/Video arbeiten, oder sollen Headings, Text und CTA direkt in
> die Grafik eingebaut werden — z. B. als Mehrbild-Post mit mehreren Slides?"

**Fall A — reine Bilder:** Weiter wie in Abschnitt 8a. **Fall B — Text-/Info-Content
(Mehrbild-Post):** Ein mehrteiliger LinkedIn-Post mit mehreren Bildern, in die Headline, Kernaussagen
und CTA eingebaut sind — siehe Abschnitt 8b.

### 8a. Reine Bilder

- Das Visual muss aus dem `bild-video-generierung`-Skill stammen **oder** ein bereits vorhandenes,
  genehmigtes Asset aus `brand/product/`, `brand/generated-references/` oder `Outputs/` sein.
- Erzeuge selbst kein Bild in diesem Baustein — falls noch kein Visual vorliegt, rufe zuerst
  `bild-video-generierung` auf (Format i. d. R. 16:9 oder 1.91:1 Querformat für LinkedIn).
- Orientiere dich am dokumentierten Social-Post-Bildkonvention aus den Brand Guidelines: häufig
  dunkler/anthrazitfarbener Hintergrund mit weißer Nudica-Typografie, großformatiges reales
  Industriefoto, blaues Bildzeichen als Akzent, getrackte graue Eyebrow-Label, Headline in Sentence
  Case.

### 8b. Mehrbild-Post mit Text/Headings/CTA (Fall B)

- **Immer perfekt auf die Kampagne abgestimmt** — dieselben Kernaussagen wie in Newsletter/Landing
  Page derselben Kampagne, keine widersprüchlichen oder frei erfundenen Zusatzaussagen. Ein
  vorhandenes `Campaigns/<slug>/meta.json` als Kontext nutzen statt isoliert neu zu texten.
- **Erzeugung über `bild-video-generierung`, Abschnitt 8** (`scripts/compose_slide.py`) — jede Slide
  mit **echter Nudica-Schrift und echtem Logo/Bildzeichen** (Pflicht, nicht optional). **Verbindliches
  Pixelmaß für LinkedIn:** `1200x1200` (1:1, empfohlen für Mehrbild-Posts, da LinkedIn sie im Feed
  einheitlich beschneidet) oder `1200x628` (~1.91:1, wenn ein breiteres Format gewünscht ist), Text auf
  jeder Slide in Englisch (Ausnahme: geschützte deutsche Produktbezeichnungen bleiben unverändert):
  1. **Erstes Bild:** Hook-Headline (die stärkste, substanzstärkste Aussage — Thought-Leadership-Ton).
  2. **1-2 mittlere Bilder:** je eine technische Kernaussage/ein Fakt (Headline + 1 kurzer Satz).
  3. **Letztes Bild:** CTA-Slide mit kurzer Abschluss-Headline + CTA-Pille (Englisch, Verb + Outcome).
  - Hintergrundbilder je Slide zuerst aus bereits genehmigten Kampagnen-Bildern (`Outputs/`,
    `brand/product/`) beziehen, siehe `bild-video-generierung` Abschnitt 4.
  - **Nicht jedes Bild braucht ein Foto:** für Fakten-/Zahlen-Slides oder ein technisches Schaubild
    `compose_slide.py --bg-color` (statt `--background`) mit `--dark-text` verwenden — liefert eine
    saubere Flächenfarbe (z. B. Light Grey `#F5F5F5`) statt eines erzwungenen Fotos. Ein Foto nur
    einsetzen, wo es inhaltlich etwas zeigt.
  - **Alle Sonderzeichen (auch in deutschen Produktnamen/Zitaten, z. B. ü/ä/ö/ß) korrekt und nativ
    setzen, niemals ASCII-Ersatz** ("ue"/"ae"/"oe"/"ss") — auch nicht in Kommandozeilen-Aufrufen von
    `compose_slide.py`.
  - Alle Slide-Bilder als **eine Bild-Liste** an denselben Upload-Post-Aufruf übergeben, damit
    LinkedIn sie als einen Mehrbild-Post veröffentlicht (nicht als separate Einzelposts) — Parameter
    zur Laufzeit prüfen, siehe Abschnitt 9.
  - Der Post-Text (Abschnitt 4) bleibt vollständig bestehen — die Slides verstärken die Aussage
    visuell, ersetzen den Text aber nicht.

## 9. Ablauf: Generierung → Freigabe → Veröffentlichung/Planung

1. **Generierung:** Post-Text, Bullet-Liste (optional), Hashtags und CTA nach obigem Schema erstellen;
   passendes Visual referenzieren oder beschaffen.
2. **Freigabe:** Fertigen Post (vollständiger Text + referenziertes Bild/Video) dem Nutzer zeigen und
   eine **kurze Go/No-Go-Bestätigung** einholen. Es gibt bewusst keinen komplexen Freigabeprozess — eine
   einfache Bestätigung genügt.
3. **Veröffentlichung/Planung:** Nach Freigabe fragen, ob **sofort veröffentlicht** oder auf ein
   bestimmtes **Datum/Uhrzeit geplant** werden soll. Dann die Upload-Post-MCP-Tools nutzen
   (`upload_photos`/`upload_video` für das Asset, ggf. `upload_text`, jeweils mit Platform-Parameter
   `linkedin`; Planung über die entsprechenden Scheduled-Post-Parameter bzw. `list_scheduled`/
   `edit_scheduled`/`cancel_scheduled` zur Verwaltung). **Bei einem Mehrbild-Post (Fall B) alle
   Slide-Bilder gemeinsam als eine Bild-Liste übergeben**, damit sie als ein Post veröffentlicht
   werden. Prüfe die exakten Tool-Namen und Parameter zur Laufzeit in der aktuellen Session
   (Installationen können variieren) — nicht blind eine feste Tool-ID annehmen.
4. Hinweis: Für Upload-Post fallen aktuell ca. 19 €/Monat an, die der Kunde selbst trägt
   (informativer Hinweis, nicht weiter vertiefen).

## 10. Ablage

Fertigen Post-Text, Hashtags, CTA und Referenz auf das verwendete Bild/Video speichern unter
`Outputs/<datum>-<thema>-linkedin/` (z. B. `Outputs/2026-07-01-celltron-xtreme-batterierecycling-linkedin/`).

## 11. QA-Checkliste vor Auslieferung

- **Nutzer wurde gefragt, ob reine Bilder oder Text-/Info-Content (Mehrbild-Post) gewünscht sind** —
  nicht stillschweigend angenommen?
- Post vollständig auf Englisch?
- Professionelles Thought-Leadership-Register durchgehend eingehalten (kein Consumer-/Sales-Ton)?
- Technische Substanz/Glaubwürdigkeit statt reiner Marketing-Floskeln?
- Keine Wettbewerbernennung?
- Korrekte Schreibweise CellTRON®/MSE Filterpressen®?
- Hashtags fokussiert, 3-5 Stück, thematisch passend?
- CTA-Stil = Verb + Outcome, auf Englisch?
- Visual(s) stammen aus `bild-video-generierung`, `brand/product/`, `brand/generated-references/` oder
  `Outputs/`?
- **Bei Mehrbild-Post (Fall B):** jede Slide nutzt echte Nudica-Schrift und echtes Logo/Bildzeichen
  (über `compose_slide.py`), Format durchgängig `1200x1200` oder `1200x628`, Inhalte stimmen mit der
  übrigen Kampagne überein, alle Bilder wurden als **ein** Post übergeben?
- **Alle Sonderzeichen (ü/ä/ö/ß) korrekt und nativ gesetzt**, kein ASCII-Ersatz, auch nicht in
  deutschen Produktnamen/Zitaten innerhalb des sonst englischen Posts?
