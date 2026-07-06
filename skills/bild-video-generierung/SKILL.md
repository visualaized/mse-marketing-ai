---
description: "Erzeugt markenkonforme Bilder und Videos mit Higgsfield (immer in 2K, Prompt-Aufbau nach der 6-Layer-Struktur des nano-banana-prompt-Skills) für jeden anderen Baustein (Newsletter, Social Media, Landing Page, Kampagnen). Triggert bei 'Bild generieren', 'Video generieren', 'Visual erstellen', 'Higgsfield', oder wenn ein anderer Baustein ein Visual für Social Media, Newsletter oder Landing Page benötigt."
disable-model-invocation: false
---

# Bild- & Videogenerierung — MSE Filterpressen GmbH

Dieser Baustein generiert markenkonforme Bilder und Videos auf Basis der MSE Brand Guidelines.
Bildgenerierung erfolgt über Higgsfield; Videogenerierung baut auf den generierten (oder bestehenden,
genehmigten) Bildern auf — ebenfalls über Higgsfield, per Image-to-Video. Dieser Baustein liefert die
passenden Visuals für alle anderen Bausteine (Newsletter, Social Media, Landing Pages, Kampagnen).

## 1. Wann dieser Baustein läuft

- Der Nutzer will explizit ein Bild oder Video generieren lassen.
- Ein anderer Baustein (Newsletter, Social-Media-Post, Landing Page, Kampagne) benötigt ein Visual und
  ruft diesen Skill auf, um es zu beschaffen.
- Gilt gleichermaßen für **Bildgenerierung** und **Videogenerierung** — Video setzt immer auf einem
  (neu generierten oder bereits vorhandenen) Bild auf.

## 2. Pflichtschritt: Markenkern IMMER zuerst laden

Bevor du irgendeinen Prompt baust, lies **in dieser Reihenfolge** (relativ zum aktuellen
Arbeitsverzeichnis, dem CIDES-Root des Kunden):

1. `CLAUDE.md` — kompaktes Master-Brand-Dokument.
2. `brand/brand-guidelines.md` — vollständiges Regelwerk, insbesondere Kapitel zur Bildsprache.
3. `brand/color-palette.json` — maschinenlesbare, verbindliche Farbwerte.

Diese drei Dateien sind die einzige verbindliche Quelle für Farben, Bildsprache und Do's/Don'ts.
**Erfinde niemals eigene Markenfakten, Farbwerte oder Stilregeln** — auch nicht, wenn sie plausibel
klingen. Fehlt eine Angabe, frage kurz nach, statt zu raten. Existieren diese Dateien nicht, stoppe und
weise darauf hin, dass Claude im CIDES-Ordner des Kunden gestartet werden muss.

## 3. Markenkonformen Higgsfield-Bild-Prompt aufbauen

**Verbindlich: jeder Bild-Prompt folgt der 6-Layer-Struktur des `nano-banana-prompt`-Skills**
(Concept → Subject → Colors & Materials → Composition → Lighting & Mood → Camera & Lens). Rufe für
den Prompt-Aufbau den Skill `nano-banana-prompt` auf (bzw. wende dessen Regelwerk direkt an, falls der
Skill in der Session nicht auslösbar ist) und befülle die 6 Layer mit den MSE-spezifischen Vorgaben aus
diesem Abschnitt. Nutze **niemals** eine improvisierte Freitext-Prompt-Struktur ohne die 6 Layer.

Kernregeln aus `nano-banana-prompt`, verbindlich für alle MSE-Bilder:
- **Realismus-Anker zu Beginn**, z. B. *"Ultra-photorealistic image, indistinguishable from a
  professional photo shoot, shot on professional full-frame camera, no AI artifacts, no painterly
  rendering..."*
- **Qualitäts-Verstärkung am Ende**, z. B. *"...hyperrealistic rendering with maximum detail in
  materials and surfaces. No digital artifacts. No AI aesthetic. Photographic truth."*
- Fließtext-Prosa, keine Stichpunkte im finalen Prompt; Ziel **250–450 Wörter** — mehr Detail pro
  Layer verringert den kreativen Interpretationsspielraum des Modells und erhöht die Markenkonsistenz.
- Layer 3 (Colors & Materials): niemals generische Farbnamen — immer Farbton + Unterton + Temperatur +
  Sättigung angeben (z. B. "anthracite black with a cool, near-neutral undertone, low reflectivity,
  matte industrial coating" statt nur "black"); jede Materialoberfläche (Stahl, lackierte Flächen,
  Beton, Glas) mit Lichtverhalten/Haptik beschreiben.
- Falls ausnahmsweise **Menschen** im Bild vorkommen (z. B. Ingenieurteam in Produktionsumgebung): die
  Pflicht-Detailtiefe des `nano-banana-prompt`-Skills für Haut und Haare vollständig einhalten (siehe
  dortiges Regelwerk) — MSE zeigt reale Menschen in Arbeitskleidung/PSA, niemals Business-Stockfoto-Posen.
- Produkt-Referenzbilder (z. B. vorhandenes Foto einer CellTRON aus `brand/product/`) werden als
  **Hard Reference** eingebunden, nicht im Prompt-Text beschrieben: *"Use the uploaded reference image
  as the exact reference. Reproduce the machine 1:1 — do not alter shape, proportions, labeling, or
  finish."*

Bild-Prompts werden **auf Englisch** verfasst (Bildmodelle reagieren zuverlässiger auf Englisch), auch
wenn Rückfragen an den Nutzer auf Deutsch erfolgen.

### MSE-spezifische Vorgaben je Layer (Input für den 6-Layer-Prompt)

**Subjekt (Pflicht):**
- Reale industrielle Filterpressen-Anlagen, -Komponenten oder -Umgebungen: Filterpressen im Betrieb,
  Filterplatten, Rohrleitungen, Ventile, industrielle Automatisierung, Sensorik, Ingenieurteams in
  Produktionsumgebungen.
- Wo passend: konkrete Produktnamen korrekt schreiben (CellTRON, CellTRON Xtreme, CellTRON Light,
  MSE Filterpressen) — nur wenn der Kontext das rechtfertigt und keine falschen technischen Details
  erfunden werden.

**Komposition:**
- Saubere, minimalistische Industrieästhetik, viel Weißraum bzw. großzügige, ruhige Bildflächen.
- Präzise, technische Detailaufnahmen sind erwünscht (Nahaufnahmen von Platten, Ventilen, Mechanik).
- Blaues 3-Streifen-Bildzeichen (`brand/logo/MSE Favicon.png`) nur als **sehr zurückhaltender Akzent**
  einsetzen, nie als große Fläche — das Bestandsasset wiederverwenden, nicht neu nachbauen.

**Licht & Farbe:**
- Fast White / Light Grey als dominante Töne, Anthracite Black nur für Akzentflächen/-bänder (keine
  vollflächigen Schwarzflächen).
- MSE Blue (#3498DB) ausschließlich als sehr gezielter Akzent (max. 10–15 % der Fläche) — niemals
  große blaue Flächen, Hintergründe oder dominante Farbgebung.
- Kein Grün/Rot, außer es geht ausdrücklich um die Eco:LOGIC-Sub-Marke (eigenes grünes Globus-Icon).
- Realistische, zurückhaltende industrielle Beleuchtung (z. B. Hallenlicht, technisches Kunstlicht,
  gedämpftes dramatisches Licht bei Hero-Shots) — kein knalliges, übersättigtes "KI-Look"-Licht.

**Explizit ausschließen (immer im Prompt als Negativ-Hinweise formulieren):**
- Kein Stockfoto-Look (lächelnde Business-Menschen, Handshakes, generische Büro-Szenen).
- Keine Cartoon-/Illustrationsstile.
- Keine grellen Neonfarben, kein übersättigtes, generisch-buntes "AI-Look"-Bild.
- Kein Grün/Rot außer Eco:LOGIC-Kontext.
- Keine großflächigen blauen Hintergründe/Flächen.
- Keine erfundene Retro-/Sci-Fi-/Fantasy-Ästhetik — MSE ist präzises, reales Industrial Engineering.

### Beispiel-Prompts

Die folgenden drei Beispiele zeigen die inhaltlichen MSE-Vorgaben je Layer in Kurzform. Baue daraus für
jede tatsächliche Generierung den vollständigen, fließenden 250–450-Wörter-Prompt nach
`nano-banana-prompt` auf (Realismus-Anker → Concept → Subject → Colors & Materials → Composition →
Lighting & Mood → Camera & Lens → Qualitäts-Verstärkung) — die Kurzbeispiele hier sind Ausgangsmaterial,
kein finales Prompt-Format.

**1. CellTRON Xtreme in einer Batterierecycling-Anlage:**
```
Photorealistic industrial photography of a large industrial filter press (CellTRON Xtreme type)
installed inside a modern battery-recycling plant. Wide shot showing the full press with stacked
filter plates, surrounded by pipework, valves, and industrial automation sensors. Clean, minimal
industrial environment, polished concrete floor, tall factory windows letting in natural daylight,
lots of negative space. Color palette dominated by white, light grey, and anthracite black surfaces;
a single thin MSE blue accent line or small blue indicator light as the only spot of color. No people
smiling at camera, no stock-photo staging, no neon colors, no cartoon or illustration style, no
oversaturated "AI-generated" look. Sharp technical detail, realistic industrial lighting, engineering
documentation quality.
```

**2. Technische Detailaufnahme einer Filterplatte:**
```
Extreme close-up, photorealistic technical detail shot of a single filter press plate, showing the
precise machined surface, drainage grooves, and steel clamping mechanism. Shallow depth of field,
soft industrial studio lighting, neutral grey and anthracite black background. Subtle cool highlights
suggesting MSE blue as a minimal accent on one edge or bolt detail only — no large blue surfaces.
Ultra-sharp macro focus on engineering precision, dust-free clean industrial surface. No text overlays,
no illustration style, no neon or saturated colors, no green or red tones.
```

**3. Dunkler Hero-Shot mit blauem Bildzeichen-Akzent:**
```
Cinematic, photorealistic hero shot of an industrial filter press standing in a dim, moody factory
hall at dusk, silhouette-style lighting from above. Dominant tones are anthracite black and dark grey,
with a single deliberate MSE blue accent light or thin blue line tracing an edge of the machine —
blue must remain a small, precise highlight, never a dominant color or background wash. Composition
leaves large areas of negative space for text overlay. Realistic industrial photography aesthetic,
no cartoon style, no neon colors, no stock-photo people, no green or red tones, no oversaturated
"AI-generated" look. Engineering-grade, premium, quiet confidence.
```

## 4. Referenz-Assets zuerst prüfen

Bevor du komplett neu generierst:

1. Prüfe `brand/product/` — echte vorhandene Fotos/Videos realer MSE-Anlagen. Diese sind die
   verlässlichste Referenzquelle für Bildmodelle (reale Industriefotografie, kein Stockmaterial).
2. Prüfe `Outputs/` (frühere Kampagnenordner) auf bereits genehmigte, frühere Higgsfield-Generierungen
   zum gleichen oder einem ähnlichen Thema.
3. Existiert ein passendes Referenzbild: **bevorzugt Image-to-Image-Varianten oder Upscaling auf Basis
   dieser Referenz erzeugen**, statt komplett neu von einem leeren Prompt zu starten. Das erhält
   visuelle Konsistenz über Zeit und Kampagnen hinweg.
4. Existiert keine passende Referenz: neu generieren, aber den fertigen, genehmigten Output danach als
   neue Referenz ablegen (siehe Abschnitt 6), damit zukünftige Generierungen darauf aufbauen können.

## 5. Higgsfield-MCP-Tools aufrufen

Die Higgsfield-MCP-Tools sind in jeder Session unter einem session-spezifischen Server-Präfix
eingebunden (z. B. `mcp__<server-id>__generate_image`, `generate_video`, `models_explore`,
`upscale_image`, `outpaint_image`, `reframe`, `remove_background`, `motion_control`,
`media_upload_widget`). Die genaue Tool-ID unterscheidet sich je nach Installation — **suche die
verfügbaren Higgsfield-Bild-/Video-Generierungs-Tools in der aktuellen Session** (z. B. per Tool-Suche
nach Namen wie `generate_image`, `generate_video`, `models_explore`) und nutze sie generisch; hardcode
keine feste Tool-ID.

- Ist unklar, welches Higgsfield-Modell für den Anwendungsfall am besten passt, rufe zuerst das
  Modell-Empfehlungs-Tool auf (z. B. `models_explore` mit `action: recommend`), bevor du generierst.
- Für Bearbeitungen an einem bestehenden Asset (statt komplett neu zu generieren) das passende
  dedizierte Tool verwenden statt erneuter Vollgenerierung: Upscaling/Auflösung erhöhen, Outpainting/
  Bildausschnitt erweitern, Reframe für neues Seitenverhältnis, Hintergrund entfernen, Motion Control
  für Bewegungsvorgaben.

### Auflösung: immer 2K

**Verbindlich: jedes Bild wird in 2K generiert** (Higgsfield/Nano Banana Pro unterstützt 2K als
Ausgabequalität — diese Auflösung ist der Standard für alle MSE-Bild-Generierungen, unabhängig vom
Zielkanal). Stelle beim Aufruf des Higgsfield-Bild-Tools den 2K-Auflösungsparameter (bzw. das
entsprechende Qualitäts-/Resolution-Preset des jeweiligen Modells) explizit ein — generiere niemals in
einer niedrigeren Standardauflösung "auf gut Glück". Muss ein Kanal ein kleineres Format ausspielen
(z. B. ein Instagram-Thumbnail), wird das fertige 2K-Bild passend zugeschnitten/skaliert — nicht direkt
in niedriger Auflösung erzeugt.

### Seitenverhältnis je Kanal

| Kanal/Zweck | Format |
|---|---|
| Instagram Feed-Post | 1:1 (quadratisch) oder 4:5 (Hochformat) |
| LinkedIn / X | 16:9 oder 1.91:1 (Querformat) |
| Newsletter-Header | i. d. R. breites Querformat (z. B. 16:9 oder ähnlich, passend zum Klaviyo-Template) |
| Landing-Page-Hero | Querformat, hohe Auflösung (Desktop-Hero-Breite, i. d. R. 16:9 oder breiter) |

Frage den Nutzer bzw. den aufrufenden Baustein nach dem Zielkanal, falls nicht bereits bekannt, und
wähle das Seitenverhältnis entsprechend — die Auflösung bleibt in jedem Fall 2K.

## 6. Freigabe & Ablage

1. Nach der Generierung: Ergebnis dem Nutzer zur kurzen **Go/No-Go-Freigabe** vorlegen (kein komplexer
   Freigabeprozess — eine kurze Bestätigung reicht).
2. Freigegebene Bilder/Videos ablegen unter `Outputs/<datum>-<thema>/` (z. B. `Outputs/2026-07-01-celltron-xtreme-batterierecycling/`).
3. Besonders wiederverwendbare, markenkonforme Ergebnisse **zusätzlich** kopieren nach
   `brand/generated-references/` — ein dediziertes Unterverzeichnis für KI-generierte Referenzbilder,
   getrennt von den echten Produktfotos in `brand/product/`. Existiert dieser Ordner noch nicht, beim
   ersten Anlass anlegen und dem Nutzer kurz erklären, wofür er dient: Er sammelt bereits genehmigte
   Generierungen als Referenzbasis für zukünftige Image-to-Image-Generierungen, damit Markenkonsistenz
   über Zeit und Kampagnen hinweg zunimmt statt bei jeder Generierung neu bei null zu beginnen.

## 7. Videogenerierung

Sobald ein genehmigtes Basisbild vorliegt (frisch generiert oder aus `brand/product/` /
`brand/generated-references/`), damit über Higgsfield kurze, markenkonforme Bewegtbild-Inhalte für
Social Media und weitere Kanäle erzeugen (Image-to-Video bzw. Motion Control).

**Prompt-Charakter für Video:** ruhig, präzise, zurückhaltend — passend zum Markencharakter:
- Dezente Kamerafahrten (langsamer Pan, leichter Zoom, ruhige Parallaxe).
- Realistische Maschinenbewegung (Filterplatten schließen/öffnen, Fördertechnik läuft, Ventile
  betätigen sich, Dampf/Flüssigkeit in Rohrleitungen).
- Keine überstilisierten Effekte, keine schnellen Schnitte, keine Glitch-/Sci-Fi-Effekte, keine
  übertriebene Kameradynamik.
- Ziel: ruhiges, souveränes "Premium Industrial Engineering"-Gefühl, keine Social-Media-Hektik.

Auch hier zuerst passendes Higgsfield-Video-Tool in der Session lokalisieren (z. B. `generate_video`,
`motion_control`, `reframe` für Seitenverhältnis-Anpassung) statt feste Tool-IDs anzunehmen. Nach
Generierung gilt derselbe Freigabe- und Ablage-Schritt wie unter Abschnitt 6.

## 8. Text-Slides / Carousel-Grafiken komponieren (Foto + Headline + CTA in einem Bild)

Für Social-Media-Content mit Text/Infos (Instagram-Carousel, LinkedIn-/X-Mehrbild-Post — siehe
`social-instagram`/`social-linkedin`/`social-x`) und für den E-Mail-Signatur-Banner braucht es
**fertig komponierte Bilder**, bei denen Foto, Headline, ggf. Body-Text und CTA **in einem einzigen
flachen Bild** verschmolzen sind — nicht Text live per HTML/CSS über ein Bild gelegt. Grund: solche
Assets werden oft in Kontexten eingebettet (E-Mail, Social-Media-Plattform-Uploads), die
zuverlässiges Text-über-Bild-Rendering nicht garantieren; ein fertiges Bild sieht dagegen überall
exakt gleich aus.

**Werkzeug: `scripts/compose_slide.py`** (Pfad relativ zu diesem Skill-Verzeichnis,
`bild-video-generierung/scripts/compose_slide.py`) — ein fertiges, getestetes Python-Skript (nur
Pillow, bereits in dieser Umgebung installiert), das genau das macht: echte Nudica-Schriftdatei
laden, Foto auf Zielformat zuschneiden (`object-fit: cover`-Logik), Eyebrow/Headline/Body mit
dezentem Text-Scrim plus — bei hellem Text auf Foto — einem leichten, WEICHEN Schatten hinter den
Buchstaben (Kundenvorgabe: helle Schrift auf hellen Bildbereichen muss sich abheben; kein harter
Umriss, kein flächiges Overlay, siehe `landing-pages`-Konvention). Schriftgrößen im
**Website-Verhältnis** (Eyebrow : Headline : Body = 0.4 : 1 : 0.3, Eyebrow in Nudica-Medium wie
das 600er-Gewicht der Website), CTA im **Website-.btn-Stil** (Pfeilkreis + Uppercase-Label, keine
Pille). **Bildzeichen-Platzierung:** nie frei im Raum — `--logo-pos tl|tr|bl|br` (Bildecke mit
einheitlichem Eckabstand, Standard `tl`) oder `--logo-pos headline` (mit Abstand direkt über dem
Headline-Block); Details in `brand/website-design-system.md` §3. Optional eine
CTA-Pille sowie eine Fortschrittsanzeige ("2/5") zeichnen, echtes Logo/Bildzeichen einbetten, als
PNG speichern. **Dieses Skript verwenden, nicht selbst neu erfinden** — bei Bedarf Parameter
anpassen, aber die Kernlogik (echte Fonts, echtes Logo, kein Overlay) beibehalten.

Aufruf-Beispiel (ein Aufruf pro Slide):

```bash
python3 "<Pfad-zum-Plugin>/skills/bild-video-generierung/scripts/compose_slide.py" \
  --background "Outputs/2026-07-01-celltron-launch/celltron-hero-vollansicht.png" \
  --font-dir "brand/fonts/Nudica/Nudica Complete Desktop" \
  --logo "brand/logo/MSE Favicon.png" \
  --eyebrow "PRODUKTNEUHEIT — CELLTRON SERIE" \
  --headline "CellTRON Xtreme." \
  --body "Vollständig eingehaust. Gasdicht. Für die anspruchsvollsten Medien." \
  --index "1/4" \
  --width 1080 --height 1350 \
  --out "Outputs/2026-07-01-celltron-launch/carousel/slide-1.png"
```

- `--width`/`--height`: an den Zielkanal anpassen — Instagram-Carousel i. d. R. `1080x1350` (4:5)
  oder `1080x1080` (1:1); LinkedIn-/X-Mehrbild-Post i. d. R. `1200x1200` (1:1) oder `1200x628`
  (~1.91:1). Auflösung bleibt hochwertig (mind. 1080 px Kante), unabhängig vom Kanal.
- `--headline`/`--body`/`--eyebrow`: kurze, markenkonforme Aussagen — Content-Fluss wie überall bei
  MSE (Headline → kurze Erklärung → Wertversprechen), keine erfundenen Fakten.
- `--cta`: nur auf der **letzten Slide** eines Carousels sinnvoll setzen (Verb + Outcome, z. B.
  "CellTRON Xtreme entdecken").
- `--index`: fortlaufende Kennzeichnung "1/4", "2/4" usw. — hilft Nutzer:innen beim Swipen, optional
  aber empfohlen bei Carousels mit mehr als 2 Slides.
- `--logo`: **immer setzen**, wenn ein Logo/Bildzeichen zur Verfügung steht (Markenpflicht, siehe
  `marketing-zentrale`-QA-Checkliste) — `brand/logo/MSE Favicon.png` (blaues Bildzeichen, funktioniert
  auf jedem Hintergrund) ist der Standardfall für kleine Eck-Platzierungen.
- Hintergrundbild (`--background`) kommt wie immer zuerst aus bereits generierten/genehmigten
  Bildern (`Outputs/`, `brand/product/`), erst dann neu über Higgsfield generieren (siehe
  Abschnitt 4). Für ein Carousel können mehrere Slides dasselbe oder verschiedene Hintergrundbilder
  nutzen (z. B. Vollansicht + 2 Detailaufnahmen + Vollansicht für CTA-Slide).

Jede fertige Slide durchläuft dieselbe Freigabe & Ablage wie unter Abschnitt 6 beschrieben.

## 9. Hinweis zu Modell-Updates bei Higgsfield

Higgsfield aktualisiert seine zugrundeliegenden Bild-/Videomodelle regelmäßig. Das kann dazu führen,
dass ein zuvor gut funktionierender Prompt nach einem Modell-Update leicht abweichende Ergebnisse
liefert (z. B. andere Bildstimmung, Detailgrad oder Farbnuancen). Das ist normales, zu erwartendes
Verhalten bei KI-Bildmodellen — kein Fehler im Baustein. Gelegentliches Nachjustieren von Prompts nach
größeren Modell-Updates ist ein separat abzurechnender Wartungsschritt gemäß Leistungsvereinbarung,
kein dauerhaftes Pixel-genaues Konsistenzversprechen. Weise den Nutzer bei Bedarf sachlich darauf hin,
statt permanente 1:1-Konsistenz zu versprechen.

## 10. QA-Checkliste vor Auslieferung

Vor jeder Übergabe eines Bildes oder Videos an einen anderen Baustein oder den Nutzer prüfen:

- Prompt wurde nach der 6-Layer-Struktur von `nano-banana-prompt` aufgebaut (Realismus-Anker,
  250–450 Wörter Fließtext, Qualitäts-Verstärkung am Ende) — keine improvisierte Kurzform verwendet?
- Bild wurde in **2K** generiert?
- Markenfarben eingehalten (Weiß/Hellgrau dominant, Anthrazit nur als Akzentfläche, MSE Blue max.
  10–15 % und nur als gezielter Akzent, kein Grün/Rot außer Eco:LOGIC)?
- Keine verbotene Bildsprache (kein Stockfoto-Look, keine Cartoons, keine lächelnden Business-Stock-
  Menschen, kein generischer "KI-Look", keine Neonfarben)?
- Korrektes Seitenverhältnis/Auflösung für den vorgesehenen Kanal (Instagram 1:1/4:5, LinkedIn/X 16:9
  oder 1.91:1, Newsletter-Header, Landing-Page-Hero)?
- Wirkt das Ergebnis wie reale, hochwertige Industriefotografie/-videografie — nicht wie generisches,
  offensichtlich künstlich wirkendes Bildmaterial?
- CellTRON®/MSE®-Schreibweisen korrekt, falls im Bild Text/Branding sichtbar ist?
- Wurde vor der Neugenerierung geprüft, ob eine passende Referenz in `brand/product/` oder
  `brand/generated-references/` bereits existiert?
