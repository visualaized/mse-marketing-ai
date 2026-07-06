---
description: "Kontakt-Import und -Pflege in Brevo (ERP-/Excel-Kundenlisten → Bereinigung, DSGVO-Prüfung, Import als Brevo-Kontakte inkl. Anrede/Titel/Vorname/Nachname). Nur auf ausdrücklichen Wunsch des Nutzers auslösen (\"Kontakte importieren\", \"Kundenliste nach Brevo\", \"Kontakte übertragen/aktualisieren\") — kein Standardschritt des Themen-zu-Output-Ablaufs der CIDES-Zentrale."
disable-model-invocation: false
---

# Newsletter – Kontakt-Import & -Pflege (Add-on): Kundenliste → Brevo

Dieser Skill ist ein **einmaliges (bzw. seltenes) Import-/Pflege-Add-on** und **kein** Teil des
normalen CIDES-Zentrale-Ablaufs ("Thema → Output"). Er wird **niemals automatisch** von der
`marketing-zentrale` ausgelöst, sondern ausschließlich dann, wenn der Nutzer explizit danach fragt
(z. B. "Kundenliste nach Brevo importieren", "Kontakte aktualisieren", "neue ERP-Kontakte
übertragen"). Wenn du unsicher bist, ob der Nutzer wirklich einen vollständigen Import will, frage
kurz nach, bevor du beginnst.

> **Plattform-Hinweis:** Newsletter-System des Kunden ist seit Juli 2026 **Brevo** (Kundenentscheid).
> Die frühere Fassung dieses Skills beschrieb eine Migration Brevo → Klaviyo — diese Richtung ist
> hinfällig. Ziel aller Importe ist jetzt Brevo; Klaviyo wird nicht mehr befüllt.

Dieser Vorgang fasst **echte personenbezogene Kundendaten** an. Arbeite jeden Schritt bewusst,
nachvollziehbar und ohne Abkürzungen ab. Im Zweifel: anhalten und den Nutzer fragen, statt zu raten.

## 0. Preflight-Checks (immer zuerst)

Bevor irgendein Daten-Schritt beginnt:

1. **Brevo-Zugang prüfen.** Suche nach den Brevo-MCP-Tools in dieser Session (z. B. via Tool-Suche
   nach Stichworten wie "Brevo", "contact_import_export", "contacts_get_contacts", "attributes",
   "lists"). Sind sie nicht verfügbar oder schlägt ein Testaufruf fehl, stoppe und weise den Nutzer
   darauf hin, dass der Brevo-Zugang zuerst eingerichtet/autorisiert werden muss.
2. **Quelldatei klären.** Der Import basiert auf einer vom Nutzer bereitgestellten Kundenliste
   (typischerweise ein bereinigter ERP-/Excel-Export, z. B. `MSE_Kundenliste_Brevo_bereinigt.xlsx`).
   Liegt keine Datei vor, bitte aktiv darum — erfinde keine Kontaktdaten und nimm keine Platzhalter an.
3. **Umfang klären.** Frage den Nutzer ausdrücklich:
   - Handelt es sich um einen **vollständigen Erstimport** (alle Kontakte) oder um einen
     **inkrementellen Lauf** (nur neue/geänderte Kontakte seit dem letzten Import)?
   - Bei inkrementellem Lauf: gibt es einen Referenzpunkt (Datum des letzten Laufs, letzter
     Import-Report in `Outputs/`)? Falls ja, nutze diesen als Filterkriterium.
   - In **welche Brevo-Liste(n)** sollen die Kontakte (Standard: sprachgetrennte Listen DE/EN, siehe
     Schritt 3)?
4. **Risikohinweis geben.** Weise den Nutzer aktiv darauf hin, dass dieser Vorgang reale
   Kundenkontakte betrifft (Namen, E-Mails, Opt-in-Status) und daher bewusst und nicht "nebenbei"
   ausgeführt werden sollte. Schlage bei der ersten Ausführung einen **Dry-Run** vor: nur Einlesen und
   Datenaufbereitung durchführen, Ergebnis (Anzahl, Auffälligkeiten, Ausschlüsse) dem Nutzer zeigen und
   den eigentlichen Import in Brevo erst nach ausdrücklicher Freigabe starten.

## Schritt 1 — Quelldaten einlesen

Ziel: vollständige, strukturierte Erfassung der Quelldatei.

**Bekanntes Spaltenschema der bereinigten MSE-Kundenliste** (Stand Juli 2026 — bei abweichenden
Dateien das tatsächliche Schema erst prüfen, nicht blind annehmen):

| Spalte | Inhalt / Besonderheiten |
|---|---|
| Landkz, Land | Ländercode/-name (gemischt Deutsch/Englisch, z. B. "Deutschland", "Sweden") |
| Postleitzahl, Ort | Adressdaten |
| Kundennummer | ERP-Kundennummer (Verknüpfungsschlüssel) |
| Firma | Firmenname |
| **Anrede** | `Herr`, `Frau` (deutschsprachig) bzw. `Mr.`, `Ms.` (englischsprachig); teils leer |
| **Titel** | meist leer; sonst z. B. `Dr.`, `Dr.-Ing.`, `Dipl.-Ing.`, `Ing.` |
| **Vorname**, **Name** | Vor-/Nachname (Spalte "Name" = Nachname) |
| Funktion, Abteilung | Rolle des Ansprechpartners (oft leer) |
| EMAIL | E-Mail-Adresse (Pflichtfeld für den Import) |
| Branche | Branchenzuordnung (z. B. "Chemie & Pharma", "Wasser- & Abwasseraufbereitung") |

Die Felder **Anrede, Titel, Vorname, Name** sind die Grundlage für die persönliche Anrede in allen
Newslettern (siehe `newsletter-brevo` Abschnitt 1c) — sie müssen vollständig und unverfälscht als
Brevo-Kontaktattribute ankommen.

Zusätzlich bei jedem Lauf: **bestehende Brevo-Attribute abrufen** (sinngemäß
`attributes_get_attributes`), um das Mapping Quellspalte → Brevo-Attribut festzulegen. Fehlende
Attribute vor dem Import anlegen (sinngemäß `attributes_create_attribute`) — Namenskonvention
GROSSBUCHSTABEN (z. B. `ANREDE`, `TITEL`, `VORNAME`, `NACHNAME`, `FIRMA`, `KUNDENNUMMER`,
`BRANCHE`, `LAND`). Das final verwendete Mapping im Report dokumentieren.

## Schritt 2 — Datenbereinigung

Führe folgende Schritte nachvollziehbar durch und dokumentiere auffällige Fälle statt sie
stillschweigend zu entscheiden:

1. **Deduplizierung**
   - Schlüssel: E-Mail-Adresse, **case-insensitive** und **getrimmt** (führende/nachfolgende
     Leerzeichen entfernt) vergleichen.
   - Bei mehreren Datensätzen mit derselben E-Mail-Adresse: zu einem Kontakt zusammenführen (siehe
     Merge-Logik unten), nicht einfach den ersten oder letzten Treffer behalten.

2. **Normalisierung**
   - Namen: konsistente Groß-/Kleinschreibung (z. B. "Max Mustermann" statt "max MUSTERMANN").
   - Anrede: nur die vier bekannten Werte `Herr`/`Frau`/`Mr.`/`Ms.` oder leer — abweichende
     Schreibweisen (z. B. "Herrn", "Mister") auf den Standardwert normalisieren; nicht eindeutig
     zuordenbare Werte im Report vermerken statt zu raten.
   - Land/Sprache: konsistente Codes/Bezeichnungen (z. B. ISO-Ländercode, einheitliche Sprachkürzel).

3. **Validierung**
   - Einfache Formatprüfung der E-Mail-Adresse (enthält `@`, gültige Domain-Struktur).
   - Kontakte ohne gültige E-Mail-Adresse werden **nicht** importiert (siehe "Never"-Liste unten) und
     landen im Report unter "ausgeschlossen: keine gültige E-Mail".

4. **Merge-Logik bei Dubletten zwischen Quelldatei und bestehendem Brevo-Bestand**
   Wenn derselbe Kontakt (per E-Mail bzw. Kundennummer) in der Quelldatei **und** bereits in Brevo
   existiert, gilt als sinnvoller **Standard-Präzedenzfall**:
   - **Quelldatei (ERP) gewinnt** bei Firmen-/Rollen-/Stammdaten (Firma, Branche, Kundennummer,
     Anrede/Titel/Namen, Funktion).
   - **Brevo gewinnt** bei Engagement- und Opt-in-Historie (Abo-Status, Blacklist-Flags,
     Listenzugehörigkeiten, Interaktionsdaten) — diese werden niemals aus der Quelldatei überschrieben.
   - Widersprüchliche Werte, die sich nicht eindeutig nach dieser Regel auflösen lassen (z. B.
     unterschiedliche Namen zur selben E-Mail-Adresse), werden **nicht automatisch entschieden**,
     sondern im Import-Report unter "Konflikte – manuelle Prüfung erforderlich" aufgelistet.

## Schritt 3 — Sprachzuordnung (DE/EN-Listen)

Die Newsletter laufen zweisprachig (siehe `newsletter-brevo` Abschnitt 1) — deshalb werden Kontakte
beim Import einer sprachpassenden Brevo-Liste zugeordnet:

- Anrede `Herr`/`Frau` → deutschsprachige Liste.
- Anrede `Mr.`/`Ms.` → englischsprachige Liste.
- Anrede leer → anhand des Landes plausibilisieren (D-A-CH → DE, sonst EN); nicht eindeutige Fälle
  im Report unter "Sprachzuordnung unklar" aufführen und dem Nutzer zur Entscheidung vorlegen.

Existieren noch keine sprachgetrennten Listen in Brevo (sinngemäß `lists_get_lists` prüfen), die
Ziel-Listen mit dem Nutzer abstimmen und ggf. anlegen (sinngemäß `lists_create_list`) — niemals
stillschweigend in eine beliebige bestehende Liste importieren.

## Schritt 4 — DSGVO-/GDPR-Prüfung

Dies ist der wichtigste Schritt und darf nicht übersprungen oder verkürzt werden:

- **Nur Kontakte mit nachvollziehbarer Rechtsgrundlage importieren.** Kläre mit dem Nutzer, auf
  welcher Grundlage die Liste beruht (bestehende Kundenbeziehung/Einwilligung) und dokumentiere die
  Antwort im Report.
- **In Brevo bereits abgemeldete oder blockierte Kontakte respektieren:** Ein Kontakt, der in Brevo
  als abgemeldet/blacklisted geführt wird, wird durch den Import **niemals** wieder auf "abonniert"
  gesetzt — auch wenn er in der Quelldatei steht.
- **Unklare Fälle → ausschließen oder zur manuellen Prüfung markieren**, niemals automatisch als
  "vermutlich okay" importieren.
- **Herkunft dokumentieren.** Quelle und Importdatum als Attribut mitgeben (z. B.
  `IMPORT_QUELLE`, `IMPORT_DATUM`), damit die Herkunft jedes Kontakts nachweisbar bleibt.
- **Im Zweifel: nicht importieren.** Es ist immer die sicherere Wahl, einen Kontakt zur manuellen
  Prüfung auszuschließen, als eine Rechtsgrundlage anzunehmen, die nicht eindeutig belegt ist.

## Schritt 5 — Import nach Brevo

Nutze die verfügbaren Brevo-MCP-Tools generisch (Tool-Suche nach Stichworten wie "Brevo import
contacts", "Brevo create contact", "Brevo lists", "Brevo attributes" — exakte Namen sind
sessionabhängig):

1. **Kontakte importieren/aktualisieren** (bevorzugt als Bulk-Import, sinngemäß
   `contact_import_export_import_contacts` bzw. `update_batch_contacts`; einzelne Nachzügler
   sinngemäß `contacts_create_contact`/`contacts_update_contact`) für jeden bereinigten,
   DSGVO-geprüften Kontakt.
2. **Attribute vollständig mitgeben**, insbesondere `ANREDE`, `TITEL`, `VORNAME`, `NACHNAME` (bzw.
   die in Schritt 1 verifizierten Attributnamen) sowie `FIRMA`, `KUNDENNUMMER`, `BRANCHE`, `LAND`,
   `IMPORT_QUELLE`, `IMPORT_DATUM` — die Anrede-Felder sind Pflicht, weil jeder Newsletter darauf
   personalisiert (siehe `newsletter-brevo` Abschnitt 1c).
3. **Listenzuordnung gemäß Schritt 3** (DE-/EN-Liste) im Import mitgeben bzw. nachziehen (sinngemäß
   `lists_add_contact_to_list`).
4. Arbeite in überschaubaren Batches und protokolliere Fehler pro Batch (z. B. ungültiges Format,
   API-Fehler), statt bei einem Fehler den gesamten Import abzubrechen, ohne den Fortschritt
   festzuhalten. Bei asynchronen Import-Jobs den Job-Status abfragen (sinngemäß
   `processes_get_process`), bevor Erfolg gemeldet wird.

## Schritt 6 — Verifikation & Report

1. Erstelle einen kurzen, klar strukturierten Import-Report mit mindestens folgenden Kennzahlen:
   - Anzahl Datensätze in der Quelldatei
   - Anzahl nach Deduplizierung
   - Anzahl ausgeschlossen wegen fehlender/ungültiger E-Mail-Adresse
   - Anzahl ausgeschlossen/markiert nach DSGVO-Prüfung (inkl. respektierter Abmeldungen)
   - Anzahl Konflikte zur manuellen Prüfung (Merge-Logik, Sprachzuordnung)
   - Anzahl erfolgreich importierter/aktualisierter Kontakte (Brevo), aufgeschlüsselt nach DE-/EN-Liste
   - Anzahl Fehler beim Import (mit kurzer Fehlerbeschreibung)
   - Verwendetes Attribut-Mapping (Quellspalte → Brevo-Attribut)
2. Speichere den Report unter `Outputs/<datum>-kontakt-import/import-report.md`
   (Datum im Format `YYYY-MM-DD`, z. B. `Outputs/2026-07-06-kontakt-import/import-report.md`).
3. Empfehle dem Nutzer ausdrücklich einen **Stichproben-Check** (z. B. 5–10 zufällige Kontakte in
   Brevo gegen die Quelldatei abgleichen — insbesondere Anrede/Titel/Nachname, da die
   Newsletter-Personalisierung darauf aufbaut), bevor der nächste Newsletter an die importierten
   Listen gerichtet wird.

## Was dieser Skill NIEMALS tun darf

- **Niemals** Kontakte in Brevo löschen oder abmelden (unsubscriben) — dieser Skill legt an und
  aktualisiert, er entfernt nichts.
- **Niemals** einen in Brevo abgemeldeten/blockierten Kontakt durch den Import wieder aktivieren.
- **Niemals** eine Rechtsgrundlage/Einwilligung raten oder annehmen, wenn sie nicht eindeutig belegt
  ist — im Zweifel ausschließen bzw. zur manuellen Prüfung markieren.
- **Niemals** Kontakte ohne mindestens eine gültige E-Mail-Adresse importieren.
- **Niemals** bestehende Brevo-Kontaktdaten still überschreiben, ohne die klare, dem Nutzer
  kommunizierte Präzedenzregel anzuwenden (siehe Merge-Logik in Schritt 2) — Konflikte werden
  gemeldet, nicht stillschweigend aufgelöst.
- **Niemals** diesen Skill automatisch im Rahmen des normalen "Thema → Output"-Ablaufs auslösen — nur
  auf expliziten Wunsch des Nutzers.
