---
description: "Kontakt-Migration von Brevo nach Klaviyo (Export, Bereinigung, DSGVO-Prüfung, Import). Nur auf ausdrücklichen Wunsch des Nutzers auslösen (\"Kontakte migrieren\", \"Brevo zu Klaviyo\", \"Kontakte übertragen\") — kein Standardschritt des Themen-zu-Output-Ablaufs der CIDES-Zentrale."
disable-model-invocation: false
---

# Newsletter – Kontakt-Migration (Add-on): Brevo → Klaviyo

Dieser Skill ist ein **einmaliges (bzw. seltenes) Migrations-Add-on** und **kein** Teil des normalen
CIDES-Zentrale-Ablaufs ("Thema → Output"). Er wird **niemals automatisch** von der
`marketing-zentrale` ausgelöst, sondern ausschließlich dann, wenn der Nutzer explizit danach fragt
(z. B. "Kontakte von Brevo zu Klaviyo migrieren", "Kontakt-Migration starten", "unsere Newsletter-Liste
übertragen"). Wenn du unsicher bist, ob der Nutzer wirklich eine vollständige Migration will, frage
kurz nach, bevor du beginnst.

Diese Migration fasst **echte personenbezogene Kundendaten** an. Arbeite jeden Schritt bewusst,
nachvollziehbar und ohne Abkürzungen ab. Im Zweifel: anhalten und den Nutzer fragen, statt zu raten.

## 0. Preflight-Checks (immer zuerst)

Bevor irgendein Daten-Schritt beginnt:

1. **Brevo-Zugang prüfen.** Suche nach den Brevo-MCP-Tools in dieser Session (z. B. via Tool-Suche
   nach Stichworten wie "Brevo", "contact_import_export", "contacts_get_contacts", "segments",
   "lists"). Sind sie nicht verfügbar oder schlägt ein Testaufruf fehl, stoppe und weise den Nutzer
   darauf hin, dass der Brevo-Zugang zuerst eingerichtet/autorisiert werden muss.
2. **Klaviyo-Zugang prüfen.** Analog: suche die Klaviyo-MCP-Tools (z. B. "get_lists", "create_profile",
   "get_bulk_import_profiles_job", "subscribe_profile_to_marketing"). Fehlen sie, stoppe und weise
   entsprechend hin.
3. **Umfang klären.** Frage den Nutzer ausdrücklich:
   - Handelt es sich um eine **vollständige Erstmigration** (alle Kontakte, alle Listen/Segmente) oder
     um eine **inkrementelle/wiederholte Migration** (nur neue/geänderte Kontakte seit dem letzten Lauf)?
   - Bei inkrementeller Migration: gibt es einen Referenzpunkt (Datum des letzten Laufs, letzten
     Migrationsreport in `Outputs/`)? Falls ja, nutze diesen als Filterkriterium beim Export.
4. **Risikohinweis geben.** Weise den Nutzer aktiv darauf hin, dass dieser Vorgang reale
   Kundenkontakte betrifft (Namen, E-Mails, Opt-in-Historie) und daher bewusst und nicht "nebenbei"
   ausgeführt werden sollte. Schlage bei der ersten Ausführung einen **Dry-Run** vor: nur Export und
   Datenaufbereitung durchführen, Ergebnis (Anzahl, Auffälligkeiten, Ausschlüsse) dem Nutzer zeigen und
   den eigentlichen Import in Klaviyo erst nach ausdrücklicher Freigabe starten.
5. **ERP-Daten ankündigen.** Erkläre dem Nutzer, dass für die Anreicherung mit ERP-Daten (z. B.
   Kundennummer, Branche, Firmendaten) eine Export-Datei (i. d. R. CSV) aus dem ERP-System benötigt
   wird, da hierfür kein MCP-Tool zur Verfügung steht — siehe Schritt 1b.

## Schritt 1 — Export aus Brevo

Ziel: vollständiger, strukturierter Export aller relevanten Kontaktdaten.

**1a. Brevo-Export (via Brevo-MCP-Tools)**

Nutze die verfügbaren Brevo-MCP-Tools konzeptionell wie folgt (exakte Toolnamen können je nach Session
variieren — suche generisch danach, z. B. per Tool-Suche nach "Brevo contacts", "Brevo segments",
"Brevo attributes", "Brevo export"):

- **Listen abrufen** (Funktionen rund um Listen/Ordner), um zu verstehen, welche Listen existieren und
  welche migriert werden sollen.
- **Segmente abrufen** (Funktionen rund um Segmente), um Segmentzugehörigkeiten später als
  Custom-Property oder Tag in Klaviyo abbilden zu können.
- **Attribute/Felder abrufen** (Funktionen rund um Kontakt-Attribute), um zu wissen, welche
  Custom-Felder in Brevo gepflegt sind (z. B. Branche, Sprache, Opt-in-Datum).
- **Kontakte abrufen bzw. Exportauftrag anstoßen** (Funktionen zum Auflisten von Kontakten je Liste
  sowie zum Anfordern eines vollständigen Kontakt-Exports), um je Kontakt mindestens folgende Felder zu
  sichern:
  - E-Mail-Adresse (Pflichtfeld)
  - Vor-/Nachname, Firma, Telefonnummer (falls vorhanden)
  - Listen-/Segmentzugehörigkeiten
  - Tags
  - **Opt-in-/Consent-Status** (z. B. "subscribed", "unsubscribed", "blacklisted", Double-Opt-in-Flag)
  - Opt-in-Quelle und -Datum, sofern in Brevo als Attribut gepflegt

Bei inkrementeller Migration: filtere nach Änderungsdatum bzw. nutze die Ergebnisse des letzten
Migrationsreports als Ausschlussliste für bereits migrierte Kontakte.

**1b. ERP-Daten (manueller Input)**

Da für das ERP-System kein MCP-Tool zur Verfügung steht, ist dies ein manueller Schritt:

- Bitte den Nutzer aktiv um eine ERP-Export-Datei (typischerweise CSV, ggf. Excel), die mindestens
  E-Mail-Adresse oder eine eindeutige Kundennummer als Verknüpfungsschlüssel enthält, plus relevante
  Felder wie Firma, Branche, Kundennummer, Ansprechpartner-Rolle.
- Sobald die Datei bereitgestellt wurde, lies sie mit den `Read`- bzw. `Glob`-Tools ein (Pfad ggf. im
  `Outputs/`- oder einem vom Nutzer genannten Ordner suchen).
- Falls keine ERP-Datei vorliegt: frage nach, ob die Migration ohne ERP-Anreicherung durchgeführt
  werden soll, oder warte auf die Datei — erfinde keine ERP-Daten und nimm keine Platzhalter an.

## Schritt 2 — Datenbereinigung

Führe folgende Schritte nachvollziehbar durch und dokumentiere auffällige Fälle statt sie stillschweigend zu entscheiden:

1. **Deduplizierung**
   - Schlüssel: E-Mail-Adresse, **case-insensitive** und **getrimmt** (führende/nachfolgende
     Leerzeichen entfernt) vergleichen.
   - Bei mehreren Datensätzen mit derselben E-Mail-Adresse: zu einem Kontakt zusammenführen (siehe
     Merge-Logik unten), nicht einfach den ersten oder letzten Treffer behalten.

2. **Normalisierung**
   - Namen: konsistente Groß-/Kleinschreibung (z. B. "Max Mustermann" statt "max MUSTERMANN").
   - Telefonnummern: einheitliches Format (z. B. E.164-ähnlich mit Ländervorwahl, `+49...`), soweit
     aus den Rohdaten ableitbar; wenn das Format nicht eindeutig interpretierbar ist, Originalwert
     unverändert übernehmen und im Report als "nicht normalisiert" vermerken statt zu raten.
   - Land/Sprache: konsistente Codes/Bezeichnungen (z. B. ISO-Ländercode, einheitliche Sprachkürzel).

3. **Validierung**
   - Einfache Formatprüfung der E-Mail-Adresse (enthält `@`, gültige Domain-Struktur).
   - Kontakte ohne gültige E-Mail-Adresse werden **nicht** importiert (siehe "Never"-Liste unten) und
     landen im Report unter "ausgeschlossen: keine gültige E-Mail".

4. **Merge-Logik bei Dubletten zwischen Brevo und ERP**
   Wenn derselbe Kontakt (per E-Mail bzw. Kundennummer) in Brevo **und** im ERP-Export vorkommt, gilt
   als sinnvoller **Standard-Präzedenzfall**:
   - **ERP gewinnt** bei Firmen-/Rollen-/Stammdaten (Firma, Branche, Kundennummer, Ansprechpartner-Rolle).
   - **Brevo gewinnt** bei Engagement- und Opt-in-Historie (Opt-in-Status, Opt-in-Datum, Tags,
     Segment-/Listenzugehörigkeit, Interaktionsdaten).
   - Widersprüchliche Werte, die sich nicht eindeutig nach dieser Regel auflösen lassen (z. B.
     unterschiedliche Namen zur selben E-Mail-Adresse), werden **nicht automatisch entschieden**,
     sondern im Migrationsreport unter "Konflikte – manuelle Prüfung erforderlich" aufgelistet.

## Schritt 3 — DSGVO-/GDPR-Prüfung

Dies ist der wichtigste Schritt und darf nicht übersprungen oder verkürzt werden:

- **Nur Kontakte mit eindeutigem, nachvollziehbarem Opt-in migrieren.** Ein Kontakt gilt nur dann als
  migrierbar, wenn der Consent-Status aus Brevo klar "aktiv/subscribed" bzw. eindeutig dokumentiert
  Double-Opt-in-bestätigt ist.
- **Unklare oder fehlende Einwilligung → ausschließen oder zur manuellen Prüfung markieren**, niemals
  automatisch als "vermutlich okay" migrieren. Das gilt insbesondere für:
  - Kontakte ohne erkennbares Opt-in-Datum/-Quelle,
  - Kontakte mit widerrufenem Opt-in (unsubscribed, blacklisted),
  - Kontakte, die nur über eine ERP-Beziehung existieren, aber nie einem Newsletter zugestimmt haben.
- **Opt-in-Quelle und -Zeitpunkt dokumentieren.** Wo in Brevo vorhanden, als Custom Property in Klaviyo
  mitgeben (z. B. `optin_quelle`, `optin_datum`), damit die Einwilligung auch nach der Migration
  nachweisbar bleibt.
- **Im Zweifel: nicht migrieren.** Es ist immer die sicherere Wahl, einen Kontakt zur manuellen Prüfung
  auszuschließen, als eine Einwilligung anzunehmen, die nicht eindeutig belegt ist.

## Schritt 4 — Import nach Klaviyo

Nutze die verfügbaren Klaviyo-MCP-Tools generisch (Tool-Suche nach Stichworten wie "Klaviyo profile",
"Klaviyo import", "Klaviyo list", "Klaviyo subscribe" — exakte Namen sind sessionabhängig):

1. **Profile anlegen/aktualisieren** (Funktionen zum Erstellen bzw. Aktualisieren von Profilen, ggf.
   im Rahmen eines Bulk-Import-Jobs) für jeden bereinigten, DSGVO-konformen Kontakt.
2. **Custom Properties mitgeben**, u. a.:
   - `segmentname` bzw. `brevo_segmente` (aus Brevo-Segmenten/Tags)
   - `erp_kundennummer` (aus ERP-Daten)
   - `branche` (aus ERP-Daten, falls vorhanden)
   - `optin_quelle`, `optin_datum` (aus Brevo, siehe Schritt 3)
3. **Listen-/Segmentzugehörigkeit sinnvoll abbilden.** Klaviyo-Listen sind strukturell anders als
   Brevo-Listen/Segmente (Klaviyo trennt stärker zwischen statischen Listen und dynamischen Segmenten
   auf Basis von Profil-Properties). Gehe pragmatisch vor:
   - Feste Brevo-Listen → nach Möglichkeit als Klaviyo-Liste anlegen/zuordnen (Listen-Tools nutzen).
   - Brevo-Tags/dynamische Segmente → eher als Profil-Property/Tag übernehmen, aus der in Klaviyo bei
     Bedarf ein neues Segment gebaut werden kann, statt krampfhaft 1:1 auf Klaviyo-Listen zu mappen.
4. **Marketing-Abo (Subscribe) nur bei valider Einwilligung.** Rufe die Funktion zum Abonnieren für
   Marketing-Kommunikation **ausschließlich** für Kontakte auf, die die DSGVO-Prüfung in Schritt 3
   bestanden haben. Kontakte ohne validen Opt-in werden zwar ggf. als Profil angelegt (falls vom Nutzer
   gewünscht, z. B. für reine Stammdatenhaltung), aber **nicht** für Marketing abonniert.
5. Arbeite in überschaubaren Batches und protokolliere Fehler pro Batch (z. B. ungültiges Format,
   API-Fehler), statt bei einem Fehler den gesamten Import abzubrechen, ohne den Fortschritt festzuhalten.

## Schritt 5 — Verifikation & Report

1. Erstelle einen kurzen, klar strukturierten Migrationsreport mit mindestens folgenden Kennzahlen:
   - Anzahl exportierter Kontakte (Brevo)
   - Anzahl nach Deduplizierung
   - Anzahl ausgeschlossen wegen fehlender/unklarer Einwilligung (DSGVO)
   - Anzahl ausgeschlossen wegen fehlender/ungültiger E-Mail-Adresse
   - Anzahl Konflikte zur manuellen Prüfung (Merge-Logik)
   - Anzahl erfolgreich importierter Profile (Klaviyo)
   - Anzahl Fehler beim Import (mit kurzer Fehlerbeschreibung)
2. Speichere den Report unter `Outputs/<datum>-kontakt-migration/migration-report.md`
   (Datum im Format `YYYY-MM-DD`, z. B. `Outputs/2026-07-01-kontakt-migration/migration-report.md`).
3. Empfehle dem Nutzer ausdrücklich einen **Stichproben-Check** (z. B. 5–10 zufällige Kontakte in
   Klaviyo gegen Brevo abgleichen), bevor Brevo als System für Newsletter-Versand als "abgelöst"
   betrachtet wird. Weise darauf hin, dass Brevo bis zur Bestätigung durch den Nutzer die
   Quelle der Wahrheit bleibt.

## Was dieser Skill NIEMALS tun darf

- **Niemals** Kontakte in Brevo automatisch löschen oder abmelden (unsubscriben) — Brevo bleibt
  unverändert, dieser Skill ist rein lesend gegenüber Brevo.
- **Niemals** einen Opt-in-/Consent-Status raten oder annehmen, wenn er nicht eindeutig aus den Daten
  hervorgeht — im Zweifel ausschließen bzw. zur manuellen Prüfung markieren.
- **Niemals** Kontakte ohne mindestens eine gültige E-Mail-Adresse importieren.
- **Niemals** bestehende Klaviyo-Profildaten still überschreiben, ohne eine klare, dem Nutzer
  kommunizierte Präzedenzregel anzuwenden (siehe Merge-Logik in Schritt 2) — Konflikte werden
  gemeldet, nicht stillschweigend aufgelöst.
- **Niemals** diesen Skill automatisch im Rahmen des normalen "Thema → Output"-Ablaufs auslösen — nur
  auf expliziten Wunsch des Nutzers.
