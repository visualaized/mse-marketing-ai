---
description: "Erstellt/aktualisiert das Kampagnen-Dashboard (Übersicht + Kampagnenplanung) und die zugehörige meta.json; Trigger: Dashboard aufsetzen/aktualisieren, Kampagnenübersicht, Kampagne planen, neue Kampagne anlegen."
disable-model-invocation: false
---

# Kampagnen-Dashboard — MSE Marketing-Zentrale

## 1. Zweck

Das Kampagnen-Dashboard hat **zwei Aufgaben**:

1. **Übersicht** für die Geschäftsführung: Thema, Kanal, Status und Zeitraum aller laufenden und
   geplanten Kampagnen auf einen Blick.
2. **Planungstool**: Der Kunde kann direkt im Dashboard neue Kampagnen **einplanen** — mit Thema/
   Beschreibung, geplantem Veröffentlichungsdatum, Kanal-Auswahl (Checkboxen) und Notizen. Ein so
   angelegter Eintrag erhält den Status `"geplant"` und landet als ganz normale
   `Campaigns/<slug>/meta.json` im Marketing Hub. Wenn später über Claude eine Kampagne gestartet
   wird, gleicht die `marketing-zentrale` das Briefing gegen diese geplanten Kampagnen ab und
   übernimmt deren Daten (siehe Abschnitt 5).

Zusätzlich zeigt das Dashboard pro Kampagne die **generierten Inhalte** an (ausklappbare Liste mit
Links zu Bildern, Newslettern, Landing Page etc. — siehe `inhalte`-Feld in Abschnitt 2), und
**geplante** Kampagnen lassen sich über die Oberfläche **bearbeiten und löschen** (Abschnitt 4).

Bewusst **nicht** Teil dieses Bausteins:
- **Keine Freigabe-/Genehmigungsworkflows.** Das Dashboard zeigt Status an, es steuert ihn nicht.
  Auch das Planungsformular ist reine Datenerfassung, kein Genehmigungsschritt.
- **Kein Bearbeiten/Löschen von Kampagnen, die über den Status `"geplant"` hinaus sind** —
  Bearbeiten/Löschen über die Oberfläche gilt ausschließlich für geplante Kampagnen (der Server
  weist alles andere mit HTTP 409 ab). Laufende/veröffentlichte/abgeschlossene Kampagnen werden
  weiterhin über die `meta.json`-Dateien gepflegt (vom Nutzer selbst oder automatisch durch andere
  Bausteine).
- **Kein Login/Zugriffsschutz.** Falls der Kunde den Zugriff auf das Dashboard einschränken möchte,
  ist das Aufgabe seiner bestehenden Server-/Netzwerk-Infrastruktur (z. B. Basic-Auth in Apache/Nginx,
  VPN, internes Netz) — nicht Teil dieses Bausteins.

Das Dashboard ist fest im System verankert (kein separater Buchungsschritt, keine Subscription).
Die Oberfläche ist HTML/CSS/Vanilla-JS ohne Datenbank und ohne Build-Schritt; für die
Planungsfunktion läuft der mitgelieferte Mini-Server `server.mjs` (nur Node-Bordmittel), der die
`meta.json`-Dateien schreibt. Ohne diesen Server (rein statisches Hosting) blendet die Oberfläche
das Planungsformular automatisch aus und bleibt reine Lese-Übersicht.

## 2. Das Datenmodell: `Campaigns/<kampagnen-slug>/meta.json`

Dieser Skill ist die **verbindliche Quelle** (Single Source of Truth) für das `meta.json`-Schema.
Alle anderen Bausteine (Marketing-Zentrale, Newsletter, Social-Media-Skills, Landing-Pages etc.)
müssen sich beim Anlegen/Aktualisieren einer kampagnenbezogenen `meta.json` an dieses Schema halten.

Jede Kampagne lebt in einem eigenen Ordner:

```
Campaigns/
  <kampagnen-slug>/
    meta.json
```

Der `<kampagnen-slug>` ist ein kurzer, URL-sicherer Bezeichner in Kleinbuchstaben mit Bindestrichen,
z. B. `celltron-xtreme-batterierecycling-2026-q3`.

### Felder in `meta.json`

| Feld | Typ | Pflicht | Beschreibung |
|---|---|---|---|
| `thema` | string | ja | Kurzer, sprechender Kampagnentitel, z. B. `"CellTRON Xtreme im Batterierecycling"`. |
| `kanaele` | string[] | ja | Liste der bespielten Kanäle, z. B. `["Newsletter-DE", "LinkedIn", "Instagram"]`. Freie Strings, aber bitte konsistente Schreibweise verwenden (siehe Beispiele unten). |
| `status` | string (Enum) | ja | Einer von exakt vier Werten (siehe Enum unten). |
| `zeitraum_start` | string (ISO-Datum, `YYYY-MM-DD`) | ja | Beginn der Kampagne. |
| `zeitraum_ende` | string (ISO-Datum, `YYYY-MM-DD`) | optional | Ende der Kampagne, falls bekannt/geplant. Fehlt das Feld, gilt die Kampagne als laufend ohne festes Enddatum. |
| `verantwortlich` | string | optional | Name/Kürzel der verantwortlichen Person **beim Kunden** (Standard: `"Marketing-Team"`). **Niemals** den Namen eines externen Dienstleisters/einer Agentur eintragen — das Dashboard ist eine kundeninterne Ansicht. |
| `notiz` | string | optional | Kurze freie Notiz, z. B. Anlass, Zielgruppe, Kernbotschaft oder nächster Schritt. |
| `quelle` | string | optional | Herkunftsmarker. `"dashboard-planung"` = vom Kunden über das Planungsformular angelegt (wichtig für den Planungsabgleich der `marketing-zentrale`, siehe Abschnitt 5). Von Bausteinen automatisch angelegte Kampagnen lassen das Feld weg. |
| `inhalte` | Array<{`label`, `pfad`}> | optional | **Generierte Inhalte der Kampagne** — das Dashboard zeigt sie als ausklappbare Link-Liste in der Kampagnenzeile. `label` = sprechender Anzeigename (z. B. `"Newsletter (DE)"`), `pfad` = Pfad **relativ zum Marketing-Hub-Root** (z. B. `"Outputs/2026-07-01-celltron-launch-newsletter-de/newsletter.html"`). Ausgeliefert werden die Dateien über den lesenden `/hub/`-Mount von `server.mjs`. **Jeder Baustein, der einen Kampagnen-Output fertigstellt, MUSS ihn hier registrieren** (Eintrag anhängen, nichts überschreiben). |

### Enum `status` (genau diese vier Werte, exakt so geschrieben)

- `"geplant"` — Kampagne ist definiert, aber noch nicht gestartet.
- `"in Arbeit"` — Inhalte werden aktuell produziert/bearbeitet.
- `"veröffentlicht"` — mindestens ein Kanal ist live, Kampagne läuft.
- `"abgeschlossen"` — Kampagne ist beendet.

Andere Statuswerte sind nicht vorgesehen. Das Dashboard stellt diese vier Zustände über abgestufte
Grau-/Anthrazit-/Blau-Töne dar (gefüllt, umrandet, blass) — **niemals** über Rot/Grün/Gelb-Ampelfarben,
da Grün/Rot markenseitig für Eco:LOGIC reserviert bzw. verboten sind.

### Beispiel

Eine vollständig ausgefüllte Beispieldatei liegt unter
`skills/kampagnen-dashboard/app/example-campaign-meta.json`. Sie enthält zusätzlich ein
`"_comment"`-Feld, das erklärt, dass es sich um eine Vorlage handelt (reines JSON kennt keine
Kommentare). **Dieses `_comment`-Feld gehört nicht in echte Kampagnen-`meta.json`-Dateien** — beim
Kopieren als Vorlage entfernen. Die Beispieldatei wird von der Dashboard-App selbst nicht gelesen,
sie dient nur als Kopiervorlage und lebendige Schema-Dokumentation.

Kurzform zum Anlegen einer neuen Kampagne von Hand:

```json
{
  "thema": "Messe-Rückblick Achema 2026",
  "kanaele": ["LinkedIn", "Newsletter-DE"],
  "status": "in Arbeit",
  "zeitraum_start": "2026-07-10",
  "zeitraum_ende": "2026-07-25",
  "verantwortlich": "Marketing-Team",
  "notiz": "Nachbericht + Foto-Highlights"
}
```

Diese Datei kommt nach `Campaigns/messe-rueckblick-achema-2026/meta.json`.

## 3. Einrichtung beim Kunden (einmalig pro Marketing-Hub)

1. Den kompletten Ordner `skills/kampagnen-dashboard/app/` aus dem Plugin in die Marketing-Hub-Root
   des Kunden kopieren, z. B. nach `Kampagnen-Dashboard/` (oder an den Ort, von dem der bestehende
   Webserver des Kunden statische Dateien ausliefert).
2. Sicherstellen, dass `Campaigns/` (mit den `meta.json`-Dateien der einzelnen Kampagnen) über einen
   relativen Pfad von `Kampagnen-Dashboard/` aus erreichbar ist — standardmäßig `../Campaigns/`, da
   beide Ordner direkt unter der Marketing-Hub-Root liegen.
3. **Logo und Nudica-Schrift sind Pflicht, nicht optional** — und liegen als **lokale Kopien im
   App-Ordner selbst** (`logo.png` sowie `fonts/Nudica-Regular.otf` + `fonts/Nudica-Bold.otf`),
   damit die App self-contained ist: `server.mjs` liefert ausschließlich den App-Ordner aus und
   blockiert `../`-Pfade (Directory-Traversal-Schutz) — Verweise auf `../brand/...` würden dort
   still (ohne Fehlermeldung im UI) auf Arial/kein Logo zurückfallen. Beim Deployment daher
   `brand/logo/MSE Favicon.png` als `logo.png` und die beiden OTF-Dateien aus
   `brand/fonts/Nudica/Nudica Complete Desktop/` nach `fonts/` in den App-Ordner kopieren. Nach dem
   Kopieren kurz im Browser prüfen, ob Logo und Schriftbild tatsächlich erscheinen.
4. Den Server starten bzw. in die bestehende Webserver-Konfiguration einbinden (siehe 3.3). Für die
   Planungsfunktion muss `server.mjs` laufen; `Campaigns/` wird standardmäßig unter `../Campaigns`
   relativ zum App-Ordner erwartet (abweichender Pfad über die Umgebungsvariable `CAMPAIGNS_DIR`).

### 3.1 Wie das Dashboard die Kampagnendaten liest

Der Browser kann aus Sicherheits-/Einfachheitsgründen nicht einfach ein ganzes Verzeichnis
(`Campaigns/*/meta.json`) auflisten. Dafür gibt es drei Wege — **Option A0 ist der empfohlene
Standardweg**, sobald `server.mjs` ohnehin läuft:

**Option A0 (Standard mit `server.mjs`): Live-Generierung — nie veraltet**

Läuft der mitgelieferte `server.mjs`, wird `campaigns-index.json` bei **jedem Abruf live** aus den
`Campaigns/<slug>/meta.json`-Dateien generiert — kein manueller Regenerier-Schritt nötig, die
Anzeige ist immer aktuell. Zusätzlich schreibt der Server bei jedem Abruf und nach jeder über das
Planungsformular angelegten Kampagne die statische `campaigns-index.json` neben `index.html`
aktuell, sodass auch eine statisch gehostete Kopie (z. B. Showcase) einen brauchbaren Stand hat.

**Option A (Fallback ohne Server): `generate-index.mjs` — kleines Node-Skript**

`app/generate-index.mjs` durchsucht `Campaigns/`, liest alle `meta.json`-Dateien ein und schreibt sie
gesammelt, sortiert nach `zeitraum_start` (absteigend, neueste zuerst), in eine einzige Datei
`campaigns-index.json` direkt neben `index.html`. Die Webseite selbst lädt nur noch diese eine Datei
per `fetch()` — kein Verzeichnis-Listing, kein Backend nötig.

Aufruf (aus dem `app/`-Ordner heraus, oder mit expliziten Pfaden):

```bash
node generate-index.mjs
# oder explizit:
node generate-index.mjs ../Campaigns ./campaigns-index.json
```

Dieses Skript ist nur noch für **rein statisches Hosting** relevant (ohne laufenden `server.mjs`):
dort muss es erneut ausgeführt werden, sobald sich eine Kampagne ändert. Mit laufendem `server.mjs`
(Option A0) entfällt der Schritt komplett.

**Option B: Serverseitige Auflistung/API**

Falls der Webserver des Kunden bereits eine dynamische Komponente hat (z. B. PHP, ein bestehendes
Backend) und Verzeichnis-Listing oder eine kleine API bereitstellen kann, lässt sich `index.html` auch
so anpassen, dass sie diese Quelle statt `campaigns-index.json` abfragt. Das ist **nicht der
Standardfall** für dieses Baustein — nur sinnvoll, wenn der Kunde eine solche Infrastruktur ohnehin
schon betreibt. Im Regelfall bei Option A bleiben.

### 3.2 Kampagne hinzufügen/aktualisieren (laufender Betrieb)

Wenn die Marketing-Zentrale oder ein anderer Baustein (Newsletter, Social-Media, Landing-Page) einen
kampagnenbezogenen Output fertigstellt:

1. `Campaigns/<kampagnen-slug>/meta.json` anlegen (neue Kampagne) oder aktualisieren (bestehende
   Kampagne, z. B. Status von `"geplant"` auf `"in Arbeit"` setzen) — gemäß Schema aus Abschnitt 2.
2. Läuft `server.mjs`, ist nichts weiter nötig (Live-Index, Option A0). Nur bei rein statischem
   Hosting zusätzlich `node generate-index.mjs` erneut ausführen.

Das ist der komplette Workflow — keine weiteren Schritte, keine Freigabe, keine Benachrichtigung.

### 3.3 Hosting

Das Dashboard ist eine statische Seite (HTML/CSS/Vanilla-JS), daher pragmatisch und leicht zu hosten:

- **Produktiv-Empfehlung:** über den vorhandenen Webserver des Kunden (Apache/Nginx) als statischer
  Ordner ausliefern — einfach `app/` (bzw. den umbenannten `Kampagnen-Dashboard/`-Ordner) in das
  bestehende Webroot-Verzeichnis legen oder per Alias/VirtualHost einbinden.
- **Lokal/Test:** `node server.mjs` im `app/`-Ordner startet einen minimalen, abhängigkeitsfreien
  statischen Dateiserver (Standardport `8787`, override per `PORT`-Umgebungsvariable oder erstem
  CLI-Argument, z. B. `node server.mjs 3000`). Die Konsole zeigt beim Start die aufzurufende URL an.
- Ein Öffnen direkt über `file://` funktioniert für einen ersten Eindruck der Optik, **aber**
  `fetch()` von `campaigns-index.json` wird von den meisten Browsern über `file://` aus
  Sicherheitsgründen blockiert. Für echten Gebrauch daher immer über `node server.mjs` oder den
  Webserver des Kunden aufrufen — die Seite zeigt in diesem Fall selbst einen Hinweis an.

Dieses Baustein ist bewusst als **leichtgewichtiges Deliverable** skopiert — keine SaaS-Plattform,
kein Datenbank-Backend, kein npm-Install-Schritt beim Kunden nötig. Alles läuft mit purem `node`
(nur eingebaute Module: `fs`, `path`, `http`, `url`).

## 4. Planungsfunktion: Kampagnen direkt im Dashboard einplanen

Die Oberfläche zeigt (nur bei laufendem `server.mjs`, Feature-Detection über `GET /api/ping`) einen
Button **„+ Kampagne planen"**. Das Formular erfasst:

- **Thema / Beschreibung** (Pflicht)
- **Geplantes Veröffentlichungsdatum** (Pflicht, wird `zeitraum_start`) + optionales Enddatum
- **Geplante Kanäle** als Checkboxen (Pflicht, mind. einer): Instagram, LinkedIn, X, Newsletter-DE,
  Newsletter-EN, Landing Page, E-Mail-Signatur, Bild/Video
- **Notizen** (optional — Anlass, Zielgruppe, Kernbotschaft, Besonderheiten)

Beim Absenden ruft die Oberfläche `POST /api/campaigns` auf; `server.mjs` validiert, erzeugt einen
ASCII-sicheren Slug aus dem Thema (Umlaute → ae/oe/ue/ss, bei Kollision Suffix `-2`, `-3`, …) und
schreibt `Campaigns/<slug>/meta.json` mit `status: "geplant"` und `quelle: "dashboard-planung"`.
Die Liste aktualisiert sich sofort (Live-Index). Der **Inhalt** der `meta.json` behält echte
Umlaute — nur der Ordnername ist ASCII.

**Bearbeiten & Löschen geplanter Kampagnen:** In der Zeile jeder Kampagne mit Status `"geplant"`
erscheinen (nur bei laufendem Server) die Buttons **Bearbeiten** und **Löschen**. Bearbeiten öffnet
das Planungsformular vorbefüllt (Speichern per `PUT`); Löschen fragt per Bestätigungsdialog nach
und entfernt den kompletten `Campaigns/<slug>/`-Ordner. Beides ist **serverseitig auf Status
`"geplant"` beschränkt** (HTTP 409 sonst) — laufende oder abgeschlossene Kampagnen können über die
Oberfläche weder geändert noch gelöscht werden. Beim Bearbeiten bleiben Felder erhalten, die das
Formular nicht kennt (z. B. bereits registrierte `inhalte`).

**Generierte Inhalte anzeigen:** Enthält eine `meta.json` das `inhalte`-Feld (Abschnitt 2), zeigt
die Kampagnenzeile eine ausklappbare Liste („n Inhalte anzeigen") — jeder Eintrag öffnet die Datei
über den lesenden `/hub/`-Mount in einem neuen Tab (Bilder, Newsletter-HTML, Landing Page,
Markdown-Posts etc.).

**API-Referenz (`server.mjs`):**

| Endpunkt | Zweck |
|---|---|
| `GET /api/ping` | Feature-Detection: antwortet nur der Server (`{ok, planning: true}`); bei statischem Hosting 404 → Formular/Buttons bleiben versteckt. |
| `POST /api/campaigns` | Neue geplante Kampagne. Body: `{thema, kanaele[], zeitraum_start, zeitraum_ende?, notiz?, verantwortlich?}`. Antwort `201` mit `{ok, slug, meta}`. |
| `PUT /api/campaigns/<slug>` | Geplante Kampagne bearbeiten (gleicher Body wie POST; nur Status `"geplant"`, sonst 409). Vorhandene `inhalte`/`quelle` bleiben erhalten. |
| `DELETE /api/campaigns/<slug>` | Geplante Kampagne löschen (nur Status `"geplant"`, sonst 409). Entfernt den Kampagnen-Ordner. |
| `PATCH /api/campaigns/<slug>/termin` | Kalender-Drag&Drop: `{zeitraum_start}` verschieben (nur `"geplant"`); `zeitraum_ende` wandert um dieselbe Differenz mit. |
| `GET /api/ideen` | Ideen-Sammlung + Themen-Tage (legt `Campaigns/ideen.json` mit Standard-Themen-Tagen an, falls fehlend). |
| `POST /api/ideen` | Eigene Idee/Notiz erfassen: `{titel, beschreibung?, themen_tag?}` → `status:"offen"`, `quelle:"kunde"`. |
| `PATCH /api/ideen/<id>` | Idee aktualisieren (`status` offen/akzeptiert/abgelehnt/umgesetzt, `titel`, `beschreibung`, `themen_tag`). |
| `DELETE /api/ideen/<id>` | Idee löschen. |
| `GET /campaigns-index.json` | Live generierter Kampagnen-Index (inkl. `slug` je Eintrag). |
| `GET /hub/<pfad>` | Lesender Zugriff auf Dateien im Marketing-Hub-Root (für die Inhalte-Links; Traversal-geschützt, nur GET). Hub-Root = eine Ebene über dem App-Ordner, Override via `HUB_DIR`. |

## 4a. Ideen-Sammlung & KI-Themenvorschläge (`Campaigns/ideen.json`)

Das Dashboard ist auch **Ideen-Zentrale**: eine dritte Ansicht („Ideen") sammelt Themenideen für
künftige Kampagnen — vom Kunden selbst erfasst oder **von Claude vorgeschlagen**.

**Datenmodell (`Campaigns/ideen.json`):**

```json
{
  "hinweis": "Themen-Tage sind Orientierung, nicht fix — Abweichungen sind ausdrücklich erlaubt.",
  "themen_tage": [
    { "tag": "Dienstag",   "fokus": "Tech / Produkt / Engineering" },
    { "tag": "Donnerstag", "fokus": "Branchenbezug / Use Case / Kundenprojekt" },
    { "tag": "Freitag",    "fokus": "Menschliches, Marke, Team" }
  ],
  "ideen": [
    {
      "id": "idee-<eindeutig>",
      "titel": "…", "beschreibung": "…",
      "themen_tag": "Dienstag — Tech / Produkt / Engineering",
      "status": "offen", "quelle": "claude", "erfasst_am": "YYYY-MM-DD"
    }
  ]
}
```

- `status`: `offen` → `akzeptiert` | `abgelehnt`; `akzeptiert` → `umgesetzt` (sobald daraus eine
  Kampagne entstanden ist). `quelle`: `"claude"` (KI-Vorschlag) oder `"kunde"` (selbst erfasst).
- Die Datei liegt bewusst als **Datei** in `Campaigns/` (der Kampagnen-Scanner liest nur Ordner).
  `server.mjs` legt sie mit den Standard-Themen-Tagen an, falls sie fehlt.

**Dashboard-Funktionen (Ideen-Ansicht):** Themen-Tage-Karten mit Hinweis „Orientierung, nicht
fix"; offene Vorschläge mit **Akzeptieren/Ablehnen**; akzeptierte Ideen mit **„Als Kampagne
einplanen"** (öffnet das Planungsformular vorbefüllt mit Titel + Beschreibung); eigenes Formular
„+ Idee / Notiz erfassen"; abgelehnte Ideen reaktivieren oder löschen. Der Ideen-Tab zeigt eine
Badge mit der Zahl offener Vorschläge.

**Pflicht-Verhalten für Claude beim Vorschlagen von Themenideen** (Trigger: „Schlag mir
Themenideen vor", „Ideen für nächste Woche/den Content-Plan" o. ä.):

1. Markenkern laden (Themenfelder, Zielgruppen, laufende Kampagnen aus `Campaigns/` als Kontext —
   keine Dubletten zu vorhandenen Ideen/Kampagnen vorschlagen).
2. Vorschläge **entlang der `themen_tage`** aus `ideen.json` entwickeln (typisch 3–6 Stück, gern
   je Themen-Tag mindestens einer). Die Themen-Tage sind **Orientierung, nicht fix** — ein starker
   Vorschlag außerhalb des Rasters ist erlaubt und wird dann ohne `themen_tag` bzw. mit passender
   Begründung in der Beschreibung eingetragen.
3. Jede Idee als Eintrag mit `status: "offen"`, `quelle: "claude"`, eindeutiger `id`
   (`idee-<timestamp/slug>`), kurzem `titel` (Kampagnen-tauglich) und 1–2 Sätzen `beschreibung`
   (Kerngedanke, ggf. Kanal-Idee) **oben in das `ideen`-Array von `Campaigns/ideen.json`
   schreiben** — vorhandene Einträge und `themen_tage` unverändert lassen.
4. Dem Nutzer kurz melden, dass die Vorschläge im Dashboard (Ideen-Tab) zum
   Akzeptieren/Ablehnen bereitliegen. **Niemals selbst akzeptieren/ablehnen** — das entscheidet
   der Kunde im Dashboard.

## 4b. Kalender-Ansicht

Zweite Ansicht „Kalender": Monatsraster (Mo–So, Navigation ‹ ›), Kampagnen erscheinen als Chip an
ihrem `zeitraum_start` (Statusfarben wie die Badges). **Klick auf einen Chip** öffnet das
Detail-Modal (Status, Zeitraum, Kanäle, Verantwortlich/Notiz, klickbare Inhalte-Links, bei
geplanten Kampagnen ein Bearbeiten-Shortcut). **Geplante Kampagnen** lassen sich **per Drag &
Drop** auf einen anderen Tag ziehen — das ruft `PATCH /api/campaigns/<slug>/termin` auf,
verschiebt `zeitraum_start` und wandert ein vorhandenes `zeitraum_ende` um dieselbe Differenz mit
(Dauer bleibt erhalten). Kampagnen mit anderem Status sind im Kalender nur lesend. Die Spalten
Di/Do/Fr tragen die Themen-Tage-Fokusse als dezente Orientierung.

## 5. Planungsabgleich durch die Marketing-Zentrale (Pflicht-Verhalten)

Geplante Kampagnen sind der **Auftakt für die spätere Umsetzung über Claude**: Startet der Nutzer
über die `marketing-zentrale` eine neue Kampagne, MUSS diese zuerst `Campaigns/*/meta.json` nach
Einträgen mit `status: "geplant"` durchsuchen und prüfen, ob das Briefing einer geplanten Kampagne
entspricht (Themen-Ähnlichkeit; `quelle: "dashboard-planung"` ist ein starkes Signal). Bei Treffer
werden Thema/Beschreibung, geplante Kanäle, Zeitraum und Notizen übernommen — Details und
Bestätigungslogik im `marketing-zentrale`-Skill (Schritt 1a). Dieser Baustein liefert dafür nur das
Datenmodell; die Abgleichslogik lebt in der Zentrale.

## 6. Kurz-Checkliste für dieses Baustein

- [ ] `Campaigns/<slug>/meta.json` folgt exakt dem Schema aus Abschnitt 2 (insbesondere die vier
      exakten `status`-Werte).
- [ ] Mit `server.mjs`: Live-Index aktiv (nichts zu tun). Ohne Server (statisches Hosting): nach
      jeder Änderung an einer `meta.json` `generate-index.mjs` erneut ausgeführt.
- [ ] Keine Status-Farben in Rot/Grün/Gelb — nur Grau/Anthrazit/Blau-Abstufungen.
- [ ] Logo (`logo.png`) und echte Nudica-Schrift (`fonts/*.otf`) liegen als lokale Kopien im
      App-Ordner und laden tatsächlich sichtbar im Browser (geprüft, nicht nur angenommen)?
- [ ] Planungsformular erscheint bei laufendem `server.mjs` und verschwindet bei statischem Hosting
      (Feature-Detection funktioniert)?
- [ ] Testweise eingeplante Kampagne erscheint sofort in der Liste UND als
      `Campaigns/<slug>/meta.json` auf der Platte?
- [ ] Bearbeiten/Löschen funktioniert für geplante Kampagnen — und wird für Kampagnen mit anderem
      Status serverseitig abgewiesen (409)?
- [ ] Generierte Outputs der Kampagne im `inhalte`-Feld registriert, Links öffnen über `/hub/`
      tatsächlich die Dateien?
- [ ] `verantwortlich` enthält eine kundeninterne Angabe (Standard „Marketing-Team"), **niemals**
      den Namen eines externen Dienstleisters/einer Agentur?
- [ ] Keine Freigabe-Buttons, keine Login-Maske, kein Bearbeiten/Löschen für Kampagnen jenseits von
      Status „geplant" in der Weboberfläche ergänzt — das widerspricht dem Scope dieses Bausteins.
