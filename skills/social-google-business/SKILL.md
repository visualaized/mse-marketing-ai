---
description: "Erstellt markenkonforme, SEO-relevante Google-Business-Profile-Posts (Unternehmensprofil bei Google Suche/Maps) für MSE Filterpressen und veröffentlicht sie nach Freigabe über Upload-Post. Trigger: 'Google Business Post', 'Google Unternehmensprofil', 'GBP-Post', 'Google My Business' oder wenn CIDES den Kanal Google Business auswählt."
disable-model-invocation: false
---

# Social Media — Google Business Profile — MSE Filterpressen GmbH

Dieser Baustein erzeugt Beiträge für das **Google-Unternehmensprofil** (Google Business Profile,
sichtbar in Google Suche und Maps) und übergibt sie nach kurzer Freigabe an **Upload-Post** zur
Veröffentlichung — 100 % markenkonform und gezielt auf lokale Sichtbarkeit/SEO ausgelegt.

## 1. Wann dieser Baustein läuft

- Der Nutzer möchte einen Google-Business-Post erstellen/veröffentlichen.
- CIDES hat im Rahmen einer Kampagne den Kanal „Google Business" ausgewählt.

## 2. Pflichtschritt: Markenkern IMMER zuerst laden

`CLAUDE.md` → `brand/website-design-system.md` → `brand/brand-guidelines.md` +
`brand/color-palette.json` (relativ zum CIDES-Root). Keine erfundenen Fakten/Claims; korrekte
Schreibweisen (CellTRON®, MSE Filterpressen®); keine Wettbewerbernennung; kein Fax.

## 3. Sprache, Ton & Plattform-Eigenheiten

- **Immer Deutsch** (lokales Profil, Remchingen/DACH-Zielgruppe), Sie-Ansprache, professionell
  und direkt — GBP-Leser suchen konkret (Firma, Leistung, Standort), keine langen Storytelling-Bögen.
- **GBP ist ein Suchergebnis, kein Feed:** Die ersten ~80–100 Zeichen erscheinen in der Vorschau —
  Kernaussage + wichtigstes Keyword nach vorn.
- **Länge:** 150–300 Zeichen ideal (Maximum 1.500) — kompakt, ein Thema pro Post.
- **Keine Hashtags** (auf GBP funktionslos und unprofessionell), sparsame/keine Emojis.
- **Post-Typen:** Neuigkeit/Update (Standard), Angebot, Event — Typ passend zum Anlass wählen.

## 4. SEO-Regeln (verbindlich — GBP-Posts zahlen direkt auf lokale Suche ein)

1. **Leistungs-Keywords natürlich einbauen**, wie die Zielgruppe sucht: „Filterpresse",
   „Kammerfilterpresse", „Membranfilterpresse", „Fest-Flüssig-Trennung", „Filtration" + Anwendungs-
   begriffe (Batterierecycling, Spezialchemie …) — 1–2 Keywords pro Post, kein Keyword-Stuffing.
2. **Lokaler Bezug**, wo er natürlich passt: „aus Remchingen", „bei Pforzheim/Karlsruhe",
   „made in Germany" — GBP rankt lokal.
3. **CTA-Button setzen** (von GBP nativ unterstützt): „Mehr erfahren" mit sprachrichtiger
   Ziel-URL (Kampagnen-Landing-Page bzw. `mse-filterpressen.com/...`, DE = Root-Pfad) —
   Beitrags-Links sind für GBP-SEO wertvoll. Alternativ „Anrufen" bei Service-Themen.
4. **Bild ist Pflicht** (GBP-Posts ohne Bild performen deutlich schlechter): Querformat
   **1200×900 (4:3)** bevorzugt, min. 400×300 — aus der Kampagnen-Bildwelt (`Outputs/`,
   `brand/product/`) oder via `bild-video-generierung`; Text-Grafiken über `compose_slide.py`
   (echte Nudica, Logo-Ecken-Regel). Fotos wirken auf GBP oft stärker als Text-Slides.
5. **Konsistenz:** Firmierung/Adresse/Telefon exakt wie im Profil (NAP-Konsistenz) — niemals
   abweichende Schreibweisen der Firmendaten in Posts.
6. **Regelmäßigkeit schlägt Einzelaktion:** GBP-Posts veralten nach ~6 Monaten sichtbar —
   Kampagnenthemen eignen sich als Serie (z. B. je Themen-Tag ein GBP-Ableger).

## 5. Aufbau eines Posts

1. **Hook mit Keyword** (erste Zeile, ≤100 Zeichen): Kernaussage + Suchbegriff.
2. **1–3 kurze Sätze Substanz**: Nutzen/Fakt (nur Belegtes), ggf. lokaler Bezug.
3. **CTA-Hinweis im Text** (Verb + Outcome) — der klickbare CTA kommt als Button.

## 6. Ablauf: Generierung → Freigabe → Veröffentlichung

1. **Generierung:** Text nach Abschnitt 3–5, Bild referenzieren/beschaffen, CTA-URL festlegen
   (sprachrichtig, bevorzugt Kampagnen-Landing-Page).
2. **Freigabe:** Vollständige Vorschau (Text im Wortlaut, Bild, Post-Typ, CTA-Button + URL) und
   kurzes Go/No-Go einholen — **nichts ohne Zustimmung veröffentlichen**.
3. **Veröffentlichung via Upload-Post:** Google Business ist an Upload-Post angebunden —
   Ablauf: mit `get_google_business_locations` die verfügbaren Standorte abrufen, bei mehreren
   Standorten den Zielstandort vom Nutzer bestätigen lassen und per
   `select_google_business_location` setzen, dann den Post über das Upload-Tool mit
   Platform-Parameter `google_business` (Enum zur Laufzeit prüfen — Installationen können
   variieren) veröffentlichen oder terminieren (`list_scheduled`/`edit_scheduled` zur Verwaltung).
   **Verbindlich: Der Upload-Post-User für MSE heißt `mse`** — diesen Wert bei jedem
   `upload_*`-/Scheduling-/Standort-Aufruf als User-Parameter übergeben; niemals einen anderen User
   raten oder ungefragt aus `list_users` auswählen.
4. Hinweis wie bei den übrigen Social-Bausteinen: Upload-Post kostet aktuell ca. 19 €/Monat
   (trägt der Kunde; nur sachlich erwähnen, falls relevant).

## 7. Ablage & Kampagne

`Outputs/<datum>-<thema>-google-business/post.md` (Text, Post-Typ, CTA, Bild-Referenz,
Standort). Bei Kampagnenzugehörigkeit: `Campaigns/<slug>/meta.json` — Kanal `"Google Business"`
in `kanaele`, Post in `inhalte` registrieren.

## 8. QA-Checkliste vor Auslieferung

- [ ] Deutsch, Sie-Form, professionell; Kernaussage + Keyword in den ersten ~100 Zeichen?
- [ ] 150–300 Zeichen, EIN Thema, keine Hashtags, keine/kaum Emojis?
- [ ] 1–2 natürliche Leistungs-Keywords + lokaler Bezug (wo passend), kein Stuffing?
- [ ] Bild vorhanden (1200×900 bevorzugt), aus Bildwelt/`compose_slide.py`, markenkonform
      (echte Nudica, Logo-Ecken-Regel, Umlaute nativ)?
- [ ] CTA-Button gesetzt, URL sprachrichtig und erreichbar? NAP-Daten exakt wie im Profil?
- [ ] Keine unbelegten Claims, keine Wettbewerber, korrekte Schreibweisen?
- [ ] Zielstandort bestätigt (bei mehreren Locations)? **Go/No-Go vor Veröffentlichung
      eingeholt?**
