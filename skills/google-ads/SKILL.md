---
description: "Erstellt und verwaltet markenkonforme Google-Ads-Kampagnen/-Anzeigen für MSE Filterpressen über die Pipeboard-Anbindung (pipeboard.co) — mit striktem Freigabe-Gate: NICHTS wird ohne ausdrückliche Zustimmung veröffentlicht oder geändert. Trigger: 'Google Ads', 'Suchanzeigen', 'Anzeigenkampagne', 'SEA' oder wenn CIDES den Kanal Google Ads auswählt."
disable-model-invocation: false
---

# Google Ads — MSE Filterpressen GmbH (Anbindung: Pipeboard)

Eigenständiger Baustein für **Google-Ads-Suchkampagnen**: Kampagnenstruktur, Keywords und
markenkonforme Anzeigentexte erstellen, bestehende Kampagnen analysieren und — ausschließlich
nach ausdrücklicher Freigabe — Änderungen über die **Pipeboard-Anbindung** (pipeboard.co, MCP)
in das Google-Ads-Konto des Kunden übertragen.

## 0. OBERSTE REGEL: Nichts ohne ausdrückliche Zustimmung (nicht verhandelbar)

**Es wird NIEMALS etwas ohne die ausdrückliche, fallbezogene Zustimmung des Nutzers
veröffentlicht oder geändert.** Das gilt für JEDE schreibende Aktion im Google-Ads-Konto:

- Kampagnen/Anzeigengruppen/Anzeigen **erstellen, aktivieren, pausieren, beenden, löschen**
- **Budgets und Gebote** anlegen oder ändern (auch minimale Beträge)
- **Keywords** (auch negative) hinzufügen/entfernen/ändern
- Targeting, Zeitpläne, Erweiterungen (Sitelinks, Callouts, Snippets), Conversion-Einstellungen

Verbindlicher Ablauf vor JEDER schreibenden Aktion:

1. **Vollständige Vorschau zeigen** — exakt das, was übertragen würde: alle Anzeigentexte im
   Wortlaut, Keywords mit Match-Types, Budget-/Gebotsbeträge mit Währung, Zielseiten-URLs,
   Laufzeit/Status. Keine Zusammenfassung, keine Auslassung.
2. **Explizit fragen** („Soll ich das so in das Google-Ads-Konto übertragen? Die Kampagne wird
   dabei [pausiert angelegt / live geschaltet / geändert].") und auf eine **eindeutige,
   fallbezogene Zustimmung warten**. Eine frühere Zustimmung, eine allgemeine Erlaubnis
   („mach ruhig") oder Schweigen gilt NICHT — jede Aktion braucht ihr eigenes Ja.
3. Neue Kampagnen werden — auch nach Freigabe — standardmäßig **PAUSIERT** angelegt; die
   Live-Schaltung ist eine eigene, erneut freizugebende Aktion. Ausnahme nur, wenn der Nutzer
   ausdrücklich „direkt live" verlangt.
4. Nach der Übertragung: **exakt berichten, was ausgeführt wurde** (IDs, Status) — und was nicht.

Analyse/Lesen (Kampagnen, Berichte, Suchbegriffe abrufen) ist ohne Freigabe erlaubt — alles, was
den Kontozustand verändert, nicht. Bei Unsicherheit, ob eine Aktion schreibend ist: als schreibend
behandeln.

## 1. Wann dieser Baustein läuft

- Der Nutzer möchte Google-Ads-Anzeigen/-Kampagnen erstellen, prüfen oder ändern.
- CIDES hat im Rahmen einer Kampagne den Kanal „Google Ads" ausgewählt.

## 2. Pflichtschritt: Markenkern IMMER zuerst laden

Vor jedem Text: `CLAUDE.md`, `brand/website-design-system.md` (Sprachgefühl/CTA-Stil),
`brand/brand-guidelines.md`. Es gelten alle Markenregeln — auch im Anzeigenformat:

- **Sprache:** Deutsch (Standard; EN nur auf Wunsch für internationale Kampagnen).
- **Ton:** Engineering-first, präzise, keine Superlative ohne Beleg, keine Ausrufezeichen-Ketten
  (Google lehnt „!" in Headlines ohnehin ab), kein Clickbait.
- **Korrekte Schreibweisen:** CellTRON, CellTRON Xtreme, MSE Filterpressen (®-Zeichen sind in
  Google-Ads-Anzeigen unüblich/platzraubend — weglassen erlaubt, Schreibweise bleibt exakt).
- **CTA = Verb + Outcome** („Filtrationslösung konfigurieren", „CellTRON Xtreme entdecken").
- **Keine Wettbewerbernamen** — weder im Anzeigentext noch als gebuchte Brand-Keywords
  (kein Brand-Bidding auf Andritz, Diemme etc.).
- **Keine erfundenen Zahlen/Claims** — nur belegte Aussagen aus den Markendokumenten
  (z. B. „Bis zu 30 % weniger Restfeuchte" ist belegt).
- **Ziel-URLs sprachrichtig** nach der URL-Konvention (DE = Root, EN = `/en/`-Präfix) — bevorzugt
  auf die passende Kampagnen-Landing-Page (`landing-pages`).

## 3. Format-Regeln (Responsive Search Ads)

- **Headlines:** max. **30 Zeichen**, 8–12 Varianten liefern (Mischung: Marke/Produkt, Nutzen,
  belegte Zahl, CTA); Zeichenzahl VOR der Vorschau nachzählen, nicht schätzen.
- **Descriptions:** max. **90 Zeichen**, 3–4 Varianten (Nutzen + Beleg + CTA).
- **Pfade (Display-URL):** 2 × max. 15 Zeichen, klein, thematisch (`/celltron`, `/filtration`).
- Sinnvolle Erweiterungen vorschlagen (Sitelinks auf echte Seiten, Callouts mit belegten
  Fakten) — Übertragung nur mit Freigabe wie alles andere.
- **Keywords:** eng am Suchverhalten der Zielgruppe (Process Engineers, Einkauf):
  Produkt-/Lösungsbegriffe („Filterpresse kaufen", „Kammerfilterpresse", „Filterpresse
  Batterierecycling"), Match-Types bewusst wählen (Phrase/Exact bevorzugt, Broad nur begründet),
  Vorschlagsliste negativer Keywords mitliefern (z. B. „gebraucht", „hobby", Fremdbranchen).

## 4. Pipeboard-Anbindung (MCP)

Die Verbindung zum Google-Ads-Konto läuft über **Pipeboard (pipeboard.co)** als MCP-Server —
der Kunde verbindet Pipeboard einmalig mit seinem Google-Ads-Konto, Claude nutzt die
bereitgestellten MCP-Tools.

- **Tool-Namen und Parameter zur Laufzeit prüfen** (ToolSearch/Tool-Liste der Session) — nicht
  blind feste Tool-IDs annehmen; Pipeboard stellt typischerweise Tools zum Auflisten von
  Konten/Kampagnen, Abrufen von Berichten und Erstellen/Ändern von Kampagnen/Anzeigen bereit.
- Ist **kein Pipeboard-MCP verbunden**: nicht improvisieren — den Nutzer bitten, den
  Pipeboard-Connector zu verbinden (pipeboard.co, dort Google-Ads-Konto autorisieren). Bis dahin
  können Texte/Struktur vollständig vorbereitet und als Entwurf in `Outputs/` abgelegt werden.
- **Mehrere Konten/Kunden im Pipeboard-Zugang:** IMMER zuerst das Zielkonto anzeigen und
  bestätigen lassen, bevor irgendetwas geschrieben wird.

## 5. Arbeitsablauf

1. **Briefing klären:** Ziel (Leads/Bekanntheit), Produkt/Thema, Zielregion, Sprache,
   Monatsbudget-Rahmen (nur vom Nutzer — niemals ein Budget annehmen), Ziel-URL.
2. **Entwurf erstellen:** Kampagnenstruktur (Kampagne → Anzeigengruppen nach Themen-Clustern),
   Keywords + negative Keywords, RSA-Texte nach Abschnitt 2/3.
3. **Ablage:** Entwurf unter `Outputs/<datum>-<thema>-google-ads/entwurf.md` speichern; bei
   Kampagnenzugehörigkeit `Campaigns/<slug>/meta.json` aktualisieren (Kanal `"Google Ads"`,
   Entwurf in `inhalte` registrieren).
4. **Freigabe-Gate nach Abschnitt 0** — erst dann Übertragung via Pipeboard (Standard: pausiert).
5. **Bericht:** was genau angelegt/geändert wurde, mit dem Hinweis, dass die Live-Schaltung ein
   separater, freizugebender Schritt ist.

## 6. QA-Checkliste vor der Freigabe-Vorschau

- [ ] Alle Headlines ≤ 30, Descriptions ≤ 90 Zeichen (nachgezählt)?
- [ ] Ton/Schreibweisen markenkonform, CTA = Verb + Outcome, keine unbelegten Claims?
- [ ] Keine Wettbewerbernamen in Texten oder Keywords?
- [ ] Ziel-URLs sprachrichtig und erreichbar (Landing Page live)?
- [ ] Negative-Keyword-Liste beigelegt? Match-Types begründet?
- [ ] Budget/Gebote stammen ausdrücklich vom Nutzer?
- [ ] Vorschau vollständig (jeder Text im Wortlaut, jede Zahl) und Zielkonto bestätigt?
- [ ] **Keine schreibende Aktion ohne fallbezogenes, ausdrückliches Ja** — neue Kampagnen
      pausiert angelegt?
