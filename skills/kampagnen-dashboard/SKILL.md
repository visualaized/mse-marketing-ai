---
description: "Erstellt/aktualisiert das Kampagnen-Dashboard (Übersicht + Kampagnenplanung) und die zugehörige meta.json; Trigger: Dashboard aufsetzen/aktualisieren, Kampagnenübersicht, Kampagne planen, neue Kampagne anlegen."
disable-model-invocation: false
---

# Kampagnen-Dashboard — CIDES — MSE Marketing-Zentrale

## 1. Zweck

Das Kampagnen-Dashboard hat **zwei Aufgaben**:

1. **Übersicht** für die Geschäftsführung: Thema, Kanal, Status und Zeitraum aller laufenden und
   geplanten Kampagnen auf einen Blick.
2. **Planungstool**: Der Kunde kann direkt im Dashboard neue Kampagnen **einplanen** — mit Thema/
   Beschreibung, geplantem Veröffentlichungsdatum, Kanal-Auswahl (Checkboxen) und Notizen. Ein so
   angelegter Eintrag erhält den Status `"geplant"` und landet als ganz normale
   `Campaigns/<slug>/meta.json` im CIDES. Wenn später über Claude eine Kampagne gestartet
   wird, gleicht die `marketing-zentrale` das Briefing gegen diese geplanten Kampagnen ab und
   übernimmt deren Daten (siehe Abschnitt 5).

Zusätzlich zeigt das Dashboard pro Kampagne die **generierten Inhalte** an (ausklappbare Liste mit
Links zu Bildern, Newslettern, Landing Page etc. — siehe `inhalte`-Feld in Abschnitt 2), markiert
Kanal-Badges mit einem **✓-Haken**, sobald für den Kanal ein Inhalt registriert ist (Abschnitt 4c),
und **alle** Kampagnen lassen sich über die Oberfläche **bearbeiten und löschen** (Abschnitt 4).

Bewusst **nicht** Teil dieses Bausteins:
- **Keine Freigabe-/Genehmigungsworkflows.** Das Dashboard zeigt Status an, es steuert ihn nicht.
  Auch das Planungsformular ist reine Datenerfassung, kein Genehmigungsschritt.
- **Keine Inhalts-Erstellung.** Bearbeiten im Dashboard ändert nur die Kampagnen-Metadaten
  (Thema, Kanäle, Status, Zeitraum, Notiz) — die eigentlichen Inhalte entstehen weiterhin über die
  Bausteine der CIDES-Zentrale und werden dort im `inhalte`-Feld registriert.
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
Alle anderen Bausteine (CIDES-Zentrale, Newsletter, Social-Media-Skills, Landing-Pages etc.)
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
| `inhalte` | Array<{`label`, `pfad`}> | optional | **Generierte Inhalte der Kampagne** — das Dashboard zeigt sie als ausklappbare Link-Liste in der Kampagnenzeile. `label` = sprechender Anzeigename (z. B. `"Newsletter (DE)"`), `pfad` = Pfad **relativ zum CIDES-Root** (z. B. `"Outputs/2026-07-01-celltron-launch-newsletter-de/newsletter.html"`). Ausgeliefert werden die Dateien über den lesenden `/hub/`-Mount von `server.mjs`. **Jeder Baustein, der einen Kampagnen-Output fertigstellt, MUSS ihn hier registrieren** (Eintrag anhängen, nichts überschreiben). |

### Enum `status` (genau diese fünf Werte, exakt so geschrieben)

Der Lebenszyklus macht dem Team auf einen Blick klar, wie weit eine Kampagne ist:

- `"geplant"` — Kampagne ist nur definiert (Thema, Kanäle, Zeitraum), noch keine Inhalte erstellt.
- `"in Arbeit"` — Inhalte werden aktuell produziert/bearbeitet; die ✓-Haken an den Kanal-Badges
  (Abschnitt 4c) zeigen den Fortschritt pro Kanal.
- `"eingeplant"` — **alle** erforderlichen Inhalte sind erstellt UND die Veröffentlichungen sind
  terminiert (Posts geplant/gescheduled, Newsletter-Entwurf steht, Termine fixiert). Die Kampagne
  wartet nur noch auf ihren Start.
- `"veröffentlicht"` — mindestens ein Kanal ist live, Kampagne läuft.
- `"abgeschlossen"` — Kampagne ist beendet (manuell über den Button **Abschließen** in der
  Kampagnenzeile oder über die Status-Auswahl im Bearbeiten-Formular).

Andere Statuswerte sind nicht vorgesehen. Das Dashboard stellt diese fünf Zustände über abgestufte
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

1. Den kompletten Ordner `skills/kampagnen-dashboard/app/` aus dem Plugin in die CIDES-Root
   des Kunden kopieren, z. B. nach `Kampagnen-Dashboard/` (oder an den Ort, von dem der bestehende
   Webserver des Kunden statische Dateien ausliefert).
2. Sicherstellen, dass `Campaigns/` (mit den `meta.json`-Dateien der einzelnen Kampagnen) über einen
   relativen Pfad von `Kampagnen-Dashboard/` aus erreichbar ist — standardmäßig `../Campaigns/`, da
   beide Ordner direkt unter der CIDES-Root liegen.
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

Wenn die CIDES-Zentrale oder ein anderer Baustein (Newsletter, Social-Media, Landing-Page) einen
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
- **Doppelklick-Starter (kein Terminal nötig):** `dashboard-starten.bat` (Windows) bzw.
  `dashboard-starten.command` (macOS) im App-Ordner — startet den Server und öffnet den Browser
  automatisch. Der Server ist plattformunabhängig (reines Node.js, alle Pfade über das
  `path`-Modul); einzige Voraussetzung auf jedem System ist ein installiertes Node.js
  (nodejs.org). Windows-Hinweis: Beim ersten Start ggf. die Windows-Firewall-Nachfrage für
  Node.js mit „Zulassen" bestätigen (rein lokaler Zugriff auf localhost).
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

**Bearbeiten & Löschen:** In der Zeile **jeder** Kampagne erscheinen (nur bei laufendem Server)
die Buttons **Bearbeiten** und **Löschen** — unabhängig vom Status. Bearbeiten öffnet das
Planungsformular vorbefüllt inklusive Status-Auswahl (geplant / in Arbeit / eingeplant /
veröffentlicht / abgeschlossen; Speichern per `PUT`). Zusätzlich trägt jede noch nicht
abgeschlossene Kampagne den Button **Abschließen** — er setzt den Status nach Bestätigungsdialog
per `PATCH /api/campaigns/<slug>/status` direkt auf `"abgeschlossen"`, ohne dass das Formular
geöffnet werden muss. Löschen fragt per Bestätigungsdialog nach und entfernt den
kompletten `Campaigns/<slug>/`-Ordner (bereits generierte Dateien unter `Outputs/` bleiben
unberührt). Beim Bearbeiten bleiben Felder erhalten, die das Formular nicht kennt (z. B. bereits
registrierte `inhalte` und `quelle`).

**Generierte Inhalte anzeigen:** Enthält eine `meta.json` das `inhalte`-Feld (Abschnitt 2), zeigt
die Kampagnenzeile eine ausklappbare Liste („n Inhalte anzeigen") — jeder Eintrag öffnet die Datei
über den lesenden `/hub/`-Mount in einem neuen Tab (Bilder, Newsletter-HTML, Landing Page,
Markdown-Posts etc.).

**API-Referenz (`server.mjs`):**

| Endpunkt | Zweck |
|---|---|
| `GET /api/ping` | Feature-Detection: antwortet nur der Server (`{ok, planning: true}`); bei statischem Hosting 404 → Formular/Buttons bleiben versteckt. |
| `POST /api/campaigns` | Neue geplante Kampagne. Body: `{thema, kanaele[], zeitraum_start, zeitraum_ende?, notiz?, verantwortlich?}`. Antwort `201` mit `{ok, slug, meta}`. |
| `PUT /api/campaigns/<slug>` | Kampagne bearbeiten (gleicher Body wie POST + optional `status`; alle Statuswerte erlaubt). Vorhandene `inhalte`/`quelle` bleiben erhalten. |
| `DELETE /api/campaigns/<slug>` | Kampagne löschen (alle Statuswerte; die Oberfläche fragt vorher per Dialog nach). Entfernt den Kampagnen-Ordner. |
| `PATCH /api/campaigns/<slug>/status` | Nur den Status umstellen: `{status}` (einer der fünf gültigen Werte). Genutzt von der Schnellaktion **Abschließen**. |
| `PATCH /api/campaigns/<slug>/termin` | Kalender-Drag&Drop: `{zeitraum_start}` verschieben (alle Statuswerte); `zeitraum_ende` wandert um dieselbe Differenz mit. |
| `GET /api/ideen` | Ideen-Sammlung + Themen-Tage (legt `Campaigns/ideen.json` mit Standard-Themen-Tagen an, falls fehlend). |
| `POST /api/ideen` | Eigene Idee/Notiz erfassen: `{titel, beschreibung?, themen_tag?}` → `status:"offen"`, `quelle:"kunde"`. |
| `PATCH /api/ideen/<id>` | Idee aktualisieren (`status` offen/akzeptiert/abgelehnt/umgesetzt, `titel`, `beschreibung`, `themen_tag`). |
| `DELETE /api/ideen/<id>` | Idee löschen. |
| `GET /campaigns-index.json` | Live generierter Kampagnen-Index (inkl. `slug` je Eintrag). |
| `GET /hub/<pfad>` | Lesender Zugriff auf Dateien im CIDES-Root (für die Inhalte-Links; Traversal-geschützt, nur GET). Hub-Root = eine Ebene über dem App-Ordner, Override via `HUB_DIR`. |

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
      "status": "offen", "quelle": "claude", "erfasst_am": "YYYY-MM-DD",
      "quellen": [ { "titel": "Kurztitel der Fundstelle", "url": "https://…" } ]
    }
  ]
}
```

`quellen` ist optional (v. a. bei KI-Vorschlägen aus der Online-Recherche, siehe unten) — das
Dashboard zeigt die Fundstellen als kleine Linkliste unter der Idee an.

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
2. **Online-Recherche (Pflicht):** Vor dem Formulieren aktiv recherchieren, was die Branche
   AKTUELL beschäftigt — per Websuche (WebSearch/WebFetch bzw. verfügbare Browser-Tools), nicht
   nur aus dem eigenen Wissen:
   - **Suchfelder:** Filtration/Fest-Flüssig-Trennung, Batterierecycling & Batteriezellproduktion,
     Hydrometallurgie, Spezialchemie/Pharma, Verfahrenstechnik allgemein — plus aktuelle Anlässe
     (Messen wie ACHEMA/POWTECH, Regulatorik wie EU-Batterieverordnung, Rohstoff-/Energiethemen).
   - **Quellentypen:** Google/News-Suche, LinkedIn (Fachbeiträge/Diskussionen der Branche),
     Branchenmagazine und Fachportale (z. B. PROCESS, CHEManager, cav/Chemie Technik, Recycling
     Magazin, Filtration + Separation) sowie Verbands-/Messemeldungen.
   - **Aktualität vor Allgemeinplätzen:** bevorzugt Themen mit konkretem, datierbarem Aufhänger
     aus den letzten Wochen/Monaten. Nichts erfinden — wird zu einem Suchfeld nichts Aktuelles
     gefunden, den Vorschlag ohne fingierten Anlass formulieren oder weglassen.
3. Vorschläge **entlang der `themen_tage`** aus `ideen.json` entwickeln (typisch 3–6 Stück, gern
   je Themen-Tag mindestens einer) und dabei die Recherche-Funde einarbeiten: Der aktuelle
   Branchen-Aufhänger gehört in die `beschreibung` („Aufhänger: …"), die Fundstellen als
   `quellen`-Einträge (`{titel, url}`) an die Idee. Die Themen-Tage sind **Orientierung, nicht
   fix** — ein starker Vorschlag außerhalb des Rasters ist erlaubt und wird dann ohne
   `themen_tag` bzw. mit passender Begründung in der Beschreibung eingetragen.
4. Jede Idee als Eintrag mit `status: "offen"`, `quelle: "claude"`, eindeutiger `id`
   (`idee-<timestamp/slug>`), kurzem `titel` (Kampagnen-tauglich), 1–2 Sätzen `beschreibung`
   (Kerngedanke + Aufhänger, ggf. Kanal-Idee) und ggf. `quellen` **oben in das `ideen`-Array von
   `Campaigns/ideen.json` schreiben** — vorhandene Einträge und `themen_tage` unverändert lassen.
5. Dem Nutzer kurz melden, dass die Vorschläge im Dashboard (Ideen-Tab) zum
   Akzeptieren/Ablehnen bereitliegen — mit einem Satz, welche aktuellen Branchenthemen die
   Recherche ergeben hat. **Niemals selbst akzeptieren/ablehnen** — das entscheidet der Kunde
   im Dashboard.

## 4b. Kalender-Ansicht

Zweite Ansicht „Kalender": Monatsraster (Mo–So, Navigation ‹ ›), Kampagnen erscheinen als Chip an
ihrem `zeitraum_start` (Statusfarben wie die Badges). **Klick auf einen Chip** öffnet das
Detail-Modal (Status, Zeitraum, Kanäle mit ✓-Haken, Verantwortlich/Notiz, klickbare
Inhalte-Links, Bearbeiten-Shortcut). **Alle Kampagnen** lassen sich **per Drag & Drop** auf einen
anderen Tag ziehen — das ruft `PATCH /api/campaigns/<slug>/termin` auf, verschiebt
`zeitraum_start` und wandert ein vorhandenes `zeitraum_ende` um dieselbe Differenz mit (Dauer
bleibt erhalten). Die Spalten Di/Do/Fr tragen die Themen-Tage-Fokusse als dezente Orientierung.

## 4c. Erledigt-Haken an Kanal-Badges

Das Dashboard erkennt automatisch, für welche Kanäle einer Kampagne bereits Inhalte vorliegen, und
setzt einen kleinen **✓-Haken** in das jeweilige Kanal-Badge (Liste UND Detail-Modal, Tooltip
„Inhalt vorhanden"). Grundlage sind ausschließlich die in `meta.json` unter `inhalte` registrierten
Einträge: pro Kanal wird per Muster gegen `label + pfad` jedes Eintrags geprüft. Die Muster (Datei
`index.html`, Objekt `KANAL_MATCHER`):

| Kanal | erkennt (label oder pfad enthält) |
|---|---|
| Bild/Video | „bild", „video", „hero", „detail", „foto" |
| Instagram / LinkedIn / Whitepaper | Kanalname |
| X | „x-post" oder Pfadsegment `…-x/` |
| Newsletter-DE / -EN | „newsletter" + „(DE)"/„-de" bzw. „(EN)"/„-en" |
| Landing Page | „landing" |
| E-Mail-Signatur | „signatur" |
| Google Business / Google Ads | „google business" / „google ads" (auch mit `-`) |

**Konsequenz für alle Bausteine:** Beim Registrieren von Outputs im `inhalte`-Feld MUSS das `label`
mit dem Kanalnamen beginnen bzw. ihn enthalten (z. B. „Instagram-Carousel (Slide 1)",
„Newsletter (DE)", „Google-Ads-Entwurf") — sonst bleibt der Haken aus. Ein Haken bedeutet „mindestens
ein Inhalt vorhanden", nicht „vollständig freigegeben/veröffentlicht".

## 5. Planungsabgleich durch die CIDES-Zentrale (Pflicht-Verhalten)

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
- [ ] Bearbeiten/Löschen funktioniert für Kampagnen **jedes** Status (Buttons in jeder Zeile,
      Status-Auswahl im Formular, Löschen mit Bestätigungsdialog)?
- [ ] Button **Abschließen** erscheint bei allen nicht abgeschlossenen Kampagnen und setzt den
      Status nach Bestätigung auf `"abgeschlossen"`?
- [ ] Kanal-Badges zeigen ✓-Haken für Kanäle mit registrierten `inhalte`-Einträgen (Labels führen
      den Kanalnamen)?
- [ ] Generierte Outputs der Kampagne im `inhalte`-Feld registriert, Links öffnen über `/hub/`
      tatsächlich die Dateien?
- [ ] `verantwortlich` enthält eine kundeninterne Angabe (Standard „Marketing-Team"), **niemals**
      den Namen eines externen Dienstleisters/einer Agentur?
- [ ] Keine Freigabe-Buttons und keine Login-Maske in der Weboberfläche ergänzt — das widerspricht
      dem Scope dieses Bausteins.
