---
description: "Erstellt markenkonforme PDF-Whitepaper (informative Themen-PDFs) für MSE Filterpressen — inkl. on-brand Schaubildern/Diagrammen, PDF-Erzeugung über Chrome headless und Verlinkung aus Newsletter/Landing Page. Trigger: 'Whitepaper erstellen', 'PDF zu [Thema]', 'Leitfaden als PDF' oder wenn die CIDES-Zentrale den Kanal Whitepaper auswählt."
disable-model-invocation: false
---

# Whitepaper (PDF) — MSE Filterpressen GmbH

Eigenständiger Baustein für **informative PDF-Whitepaper** zu einem Fachthema (z. B. „Filtration im
Batterierecycling", „Restfeuchte-Optimierung in der Spezialchemie") — perfekt on-brand, als
Download-Asset für Kampagnen: verlinkt im Newsletter und/oder auf der Landing Page.

## 1. Wann dieser Baustein läuft

- Der Nutzer möchte ein Whitepaper/Themen-PDF/einen PDF-Leitfaden erstellen.
- Die CIDES-Zentrale hat im Rahmen einer Kampagne den Kanal „Whitepaper" ausgewählt.

## 2. Pflichtschritt: Markenkern IMMER zuerst laden

Vor jeder Inhalts- oder Gestaltungsarbeit lesen (relativ zum CIDES-Root):

1. `CLAUDE.md` — Master-Brand-Dokument.
2. `brand/website-design-system.md` — **verbindliche Gestaltungsgrundlage** (Farben, Typo-Skala,
   Formen, Abstände) — das Whitepaper-Template setzt genau dieses System in Print um.
3. `brand/brand-guidelines.md` + `brand/color-palette.json`.

Keine erfundenen Fakten, Zahlen, Studien oder Quellen — Whitepaper leben von Glaubwürdigkeit.
Jede Zahl stammt aus `CLAUDE.md`/`brand-guidelines.md`/`brand/design-examples/` (Kataloge,
Fachbeiträge) oder direkten Nutzerangaben; im Zweifel nachfragen statt raten.

## 3. Sprache, Ton, Inhaltsaufbau

- **Sprache:** Deutsch (Standard) — auf Wunsch zusätzlich eine eigenständige EN-Fassung (eigene
  Datei, eigenständig formuliert, keine wörtliche Übersetzung). Sie-Ansprache, Engineering-first:
  Problem → technischer Kontext → Lösung → Nutzen. Kein Sales-Sprech; das Whitepaper informiert,
  der CTA am Ende verkauft.
- **Typischer Aufbau** (4–8 Seiten): Titelseite → Einführung/Problemstellung → 2–4 Fachkapitel
  (mit Key-Facts, Diagrammen, Tabellen, Infoboxen) → Fazit → Schlussseite mit CTA + Kontakt.
- **Jede Section: Eyebrow → Headline → Body** (nie Headline ohne Eyebrow), Sentence case,
  großzügiger Weißraum (max. ~2 Sections pro Seite).
- Korrekte Schreibweisen (CellTRON®, MSE Filterpressen®), keine Wettbewerbernennung, kein Fax.

## 4. Template verwenden: `templates/whitepaper-template.html`

Nicht bei null anfangen — das Template (Pfad relativ zu diesem Skill-Verzeichnis) ist eine
A4-Druckvorlage, die das Website-Design-System 1:1 in Print übersetzt:

- **Seitengeometrie:** `@page A4/margin 0`, jede `.page` = exakt 210×297 mm.
- **Typo im Website-Verhältnis** (Eyebrow : Headline : Body = 0.4 : 1 : 0.3): Eyebrow 9pt/600/
  uppercase/`#5D6A77`, H1 26pt / H2 17pt bold ls -0.02em `#0D0E11`, Body 10pt/1.5.
- **Titelseite HELL** (Produktfoto als Bild-Block oben, Titel auf Weiß darunter,
  „Whitepaper"-Badge auf dem Foto, Bildzeichen in der Ecke), **Schlussseite HELL**
  (CTA-Pfeilkreis-Zeile + Kontakt + Rechtsblock) — Druckregel, siehe Abschnitt 5a.
- **Elemente:** Infobox (`#F8F8F8`, eckig), Key-Facts-3er-Raster, helle Statement-Box mit
  dunklem Akzentbalken, Datentabelle (hairline-Linien), Bild mit Caption, Diagramm-Stile für
  alle Formen (Abschnitt 5).
- **Bildzeichen-Regel:** auf jeder Seite in der Ecke (`corner-logo`) — nie frei im Raum.
- Seitenfooter mit Kurztitel + Seitenzahl (beim Befüllen fortlaufend pflegen).

Alle `{{PLATZHALTER}}` befüllen; nicht benötigte Element-Blöcke komplett entfernen, benötigte
Seiten durch Duplizieren der `.page`-Blöcke ergänzen. **Kein sichtbarer Platzhaltertext im
fertigen Dokument.** Bilder: reale Assets aus `Outputs/`/`brand/product/` (Kampagnen-Bildwelt
wiederverwenden), Pfade relativ oder absolut — sie werden ins PDF eingebacken.

## 5. Schaubilder, Graphen, Diagramme — 100 % on brand (verbindlich)

Diagramme werden als **Inline-SVG direkt im HTML** gebaut. Das Template liefert fertige
CSS-Klassen und Muster (aktiv: Balkendiagramm; auskommentiert: Linien- und Tortendiagramm).
Der Skill kann **jede benötigte Form** abbilden — die Wahl richtet sich nach den Daten:

| Datentyp | Passende Form |
|---|---|
| Kategorien vergleichen | Balken vertikal (`bar-*`), bei langen Labels horizontal |
| Verlauf über Zeit | Liniendiagramm (`line-primary`, 2. Reihe gestrichelt `line-secondary`, dezente Fläche `area-primary`) |
| Anteile am Ganzen | **Tortendiagramm** (`pie-1..3`, `pie-rest`) ODER gestapelte Balken — Torte flach, weiße Fugen, max. 4–5 Segmente, Beschriftung außen, Sammelrest immer `pie-rest` (`#D9DCDF`), niemals 3D/Explode/Donut-Deko |
| Zusammensetzung über Kategorien | Gestapelte Balken (`bar-primary`/`-secondary`/`-rest`) |
| Exakte Werte/Spezifikationen | Datentabelle (`table.data`) |
| Einzelne Kennzahlen | Key-Facts-Raster (`.facts`) |
| Abläufe/Prozesse | Prozess-Schaubild: eckige Kästen (`#F8F8F8` oder Outline 0.6pt `#0D0E11`), schlichte Pfeillinien `#0D0E11` |

Verbindliche Gestaltungsregeln für ALLE Formen:

- **Farben AUSSCHLIESSLICH:** `#0D0E11` (Primär), `#5D6A77` (Sekundär), `#3D96D2` (genau EIN
  hervorgehobener Wert/Segment — sparsam, wie der Blau-Akzent der Website), `#D9DCDF`/`#F8F8F8`
  (weitere Anteile, Flächen, Gitter). Keine anderen Farben, kein Grün/Rot/Gelb, keine Verläufe,
  keine Schatten, kein 3D.
- **Beschriftung ZURÜCKHALTEND (Kundenvorgabe):** Labels/Werte im Druck ca. **6–7pt** — immer
  kleiner als der Body-Text, nie dominanter als der Inhalt. Die Template-Klassen (`chart-label`,
  `chart-value`) sind auf die Standard-Chartbreite (130mm) kalibriert; bei eigenem `viewBox`
  die px-Werte so umrechnen, dass im Druck 6–7pt herauskommen. Nudica über die Klassen —
  niemals Default-SVG-Schrift, niemals fette Riesen-Labels.
- **Werte ehrlich:** Achsen bei 0 beginnen lassen (oder Abweichung ausweisen), Quellenzeile
  unter jedem Diagramm (`.small`).
- Komplexe fotorealistische Visuals kommen weiterhin aus `bild-video-generierung` — dieser
  Abschnitt gilt für vektorbasierte Informationsgrafiken.

### 5a. Druckregel: keine dunklen Vollflächen (verbindlich)

Whitepaper werden **ausgedruckt** — deshalb enthält das PDF **keine großflächig dunklen
Seitenhintergründe**: Titelseite und Schlussseite sind hell (das Cover-Foto ist ein Bild-Block im
oberen Seitenbereich, der Titel steht auf Weiß), die Statement-Box ist Light Grey mit dunklem
Akzentbalken statt Flächen-Schwarz. Dunkle Farbe nur in kleinen Elementen (Balken, Linien,
Textfarbe). Beim Befüllen niemals dunkle Vollflächen-Seiten zurückbauen.

## 6. PDF erzeugen: `scripts/build_whitepaper.py`

```bash
python3 <skill-dir>/scripts/build_whitepaper.py \
  --html "Outputs/<datum>-<thema>-whitepaper/whitepaper.html" \
  --font-dir "brand/fonts/Nudica/Nudica Complete Desktop" \
  --out "Outputs/<datum>-<thema>-whitepaper/whitepaper.pdf"
```

Das Skript bettet die echten Nudica-Fonts (Regular/Medium/Bold) als Base64 ein und rendert über
**Chrome/Chromium/Edge headless** (`--print-to-pdf`, randlos) — pixelgenau identisch zur
HTML-Vorlage. Findet es keinen Browser, gibt es die font-eingebettete HTML-Datei aus, die manuell
über Drucken → „Als PDF sichern" (Ränder: Keine, Hintergrundgrafiken: an) exportiert wird.
**Das fertige PDF immer visuell prüfen** (jede Seite: Schnittkanten, Umbrüche, Diagramme, Fonts).

## 7. Ablage & Kampagnen-Anbindung

```
Outputs/<datum>-<thema>-whitepaper/
  whitepaper.html            ← befüllte Quelle (weiter editierbar)
  whitepaper.embedded.html   ← font-eingebettete Fassung (entsteht beim Build)
  whitepaper.pdf             ← finales Dokument
```

Teil einer Kampagne? Dann verbindlich:
- `Campaigns/<slug>/meta.json`: Kanal `"Whitepaper"` in `kanaele` ergänzen und das PDF im
  `inhalte`-Feld registrieren (`{"label": "Whitepaper (PDF)", "pfad": "Outputs/..."}`).
- **Hosting für den Download:** Das PDF muss auf eine öffentlich erreichbare URL des Kunden
  (Upload ist manueller Schritt, wie bei Landing Pages — Nutzer explizit darauf hinweisen).

## 8. Verlinkung: Newsletter & Landing Page

Das Whitepaper ist das Download-Asset der Kampagne — genau dafür verlinken:

- **Newsletter (`newsletter-klaviyo`):** Download-Link als **sekundärer Ghost-CTA** unter dem
  Haupt-CTA (gleicher Ghost-Stil wie der Haupt-CTA des Templates, Label z. B.
  „Whitepaper herunterladen (PDF)" — Verb + Outcome). In BEIDEN Sprachversionen; verlinkt die
  jeweils sprachpassende PDF-Fassung (existiert nur DE, in der EN-Version kennzeichnen:
  „Download whitepaper (PDF, German)").
- **Landing Page (`landing-pages`):** Download-Zeile in der CTA-Sektion unter dem Haupt-Button —
  Ghost-Stil mit Pfeilkreis, `data-de`/`data-en`-Label + `data-href-de`/`data-href-en` auf die
  PDF-URL(s). Das Whitepaper ersetzt nie den Haupt-CTA, es ergänzt ihn.

## 9. QA-Checkliste vor Auslieferung

- [ ] Markenkern + `website-design-system.md` gelesen; Farben NUR `#0D0E11`/`#5D6A77`/`#F8F8F8`/
      `#3D96D2` (sparsam)/Weiß; Trennlinien dunkel/neutral, nie blau?
- [ ] Jede Section mit Eyebrow über der Headline; Typo-Verhältnisse des Templates unverändert?
- [ ] Bildzeichen auf jeder Seite in der Ecke — nie frei im Raum?
- [ ] Alle Diagramme/Schaubilder nach Abschnitt 5 (passende Form je Datentyp, Brand-Farben,
      Nudica-Beschriftung ZURÜCKHALTEND ~6–7pt, Quellenzeile; Torten flach mit weißen Fugen)?
- [ ] **Keine dunklen Vollflächen-Seiten** (Titel-/Schlussseite hell, Statement-Box hell) —
      Druckregel Abschnitt 5a eingehalten?
- [ ] Keine erfundenen Zahlen/Quellen; alle Fakten rückführbar; Umlaute nativ korrekt?
- [ ] Kein Fax; Rechtsblock auf der Schlussseite korrekt; kein sichtbarer Platzhaltertext?
- [ ] **Kein `text-shadow` irgendwo in der Vorlage** — Chrome rastert geblurte text-shadows beim
      PDF-Export als eckige dunkle Kästen hinter den Textzeilen (bekannter Bug). Lesbarkeit auf
      der Titelseite kommt ausschließlich vom `cover__scrim`-Verlauf (ein einziger linearer
      Gradient ohne Zwischenstops — Zwischenstops erzeugen sichtbare Banding-Kanten im PDF)?
- [ ] Cover-Foto geprüft: unteres Drittel ruhig genug für Titel/Subtitle (harte Hell-Dunkel-Kanten
      im Motiv liegen idealerweise oberhalb des Textbereichs)?
- [ ] PDF über `build_whitepaper.py` erzeugt und **jede Seite visuell geprüft** (Fonts echt,
      Umbrüche sauber, nichts abgeschnitten)?
- [ ] Bei Kampagne: `meta.json` (`kanaele` + `inhalte`) aktualisiert; Newsletter-/Landing-Page-
      Verlinkung gesetzt (sprachpassend); Nutzer auf manuellen PDF-Upload hingewiesen?
