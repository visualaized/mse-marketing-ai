---
description: "Erstellt eine markenkonforme E-Mail-Signatur als fertigen HTML-Code für MSE Filterpressen — heller/transparenter Untergrund, dunkle Schrift/Icons, inkl. klickbarem Banner-Bild und Social-Icons. Fragt verbindlich zuerst den Verteilungsweg ab: manuell auf die Arbeitsplätze (einfache {{...}}-Platzhalter für Name, Abteilung usw.) oder CI-Sign-Format (automatische Verteilung via AD-Attribute). Trigger: 'E-Mail-Signatur erstellen/generieren'."
disable-model-invocation: false
---

# E-Mail-Signatur — MSE Filterpressen GmbH

Eigenständiger Baustein zur Erzeugung markenkonformer E-Mail-Signaturen. Auf Basis der Brand
Guidelines und eines vom Kunden vorgegebenen **Referenzlayouts** generiert die KI eine Signatur und
gibt diese als fertigen HTML-Code aus. Die Einbindung erfolgt entweder manuell direkt in die gängigen
E-Mail-Clients (dann mit einfachen Platzhaltern für die Personendaten) oder über das
Signatur-Management-Tool **CI Sign** (dann im CI-Sign-Platzhalterformat für automatische Verteilung)
— welcher der beiden Wege gilt, wird **immer zuerst abgefragt** (siehe Abschnitt 1).

## 0. Verbindliches Layout (Struktur nach Kundenreferenz, Farbgebung nach brand-guidelines.md §6)

Der Kunde hat den **strukturellen Aufbau** einer realen, bereits produktiv genutzten Signatur
vorgegeben (Screenshot, Signatur von R. Rumé). Wichtig — **klargestellt vom Kunden:** Der zunächst
dunkel wirkende Hintergrund in diesem Screenshot war **nur das Dark-Mode-Rendering des jeweiligen
Mail-Clients**, nicht das eigentliche Design. Das tatsächliche Layout ist:

- **Expliziter weißer Hintergrund** (`#FFFFFF`, gesetzt über `bgcolor="#FFFFFF"` **und**
  `background-color:#FFFFFF` inline), **dunkle (anthrazitfarbene, `#1B1B1B`) Schrift und Icons** —
  genau wie in der generischen Baseline aus `brand-guidelines.md` §6 beschrieben. **Niemals**
  `background-color:transparent` (oder gar keine Hintergrundfarbe) verwenden: Ohne einen explizit
  gesetzten hellen Hintergrund übernehmen viele Mail-Clients/Browser im Dark Mode einen eigenen
  dunklen Canvas — die anthrazitfarbene Schrift wird dann auf dunklem Grund fast unsichtbar. Genau
  das erzeugte den zunächst dunkel wirkenden Referenz-Screenshot des Kunden: keine bewusste
  Farbwahl, sondern eine fehlende explizite Hintergrundfarbe. **Niemals** einen tatsächlich
  dunklen/anthrazitfarbenen Signatur-Hintergrund bauen, auch wenn ein Referenz-Screenshot dunkel
  aussieht.

Die **Struktur** aus der Kundenreferenz bleibt jedoch verbindlich — nur eben in Hell/Dunkel-Schrift
statt Dunkel/Hell:

1. **Logo — Pflicht, nicht optional:** die echte Wortmarke aus `brand/logo/` (Standardfall:
   `Logo_06.10.2020_ohne Hintergrund.png`) oben in der Signatur, auf hellem Grund (korrekter
   Kontrast laut `brand-guidelines.md` §6). Niemals weglassen, niemals durch Klartext ersetzen,
   niemals selbst nachzeichnen/generieren (CellTRON®/MSE® sind geschützte Marken).
2. **Zweisprachige Grußzeile**: "Mit freundlichen Grüßen / Best regards".
3. **Name** fett, groß; darunter **zweisprachige Funktionsbezeichnung** (DE | EN), z. B. „Technische
   Geschäftsführung | Chief Technical Officer"; darunter Abteilung/Bereich | „MSE Filterpressen GmbH".
4. Dünne Trennlinie in **dunkler Farbe** (Anthrazit `#1B1B1B`) — **Trennstriche sind laut
   Kundenvorgabe NIEMALS blau** (gilt überall, nicht nur in der Signatur).
5. **Kontaktzeilen mit kleinem Icon** links (Telefon, E-Mail, Website, Standort) — jede Zeile mit Icon
   + klickbarem Link (`tel:`, `mailto:`, Website-Link); Icons **anthrazitfarben** (nicht weiß), im
   Material-Symbols-Outlined-Stil (siehe `brand-guidelines.md` §7 zur Icon-Sprache).
6. Zweite dünne, dezente graue Trennlinie (`#E0E0E0`).
7. **Phishing-/Sicherheitshinweis** in Rot, zwei Zeilen, englischsprachig (siehe Abschnitt 4).
8. **Klickbares Banner-Bild** in voller Signaturbreite, das auf die Website (oder eine
   Kampagnen-/Landingpage-URL) verlinkt.
9. **Social-Icons-Reihe** (kleine **anthrazitfarbene**, monochrome Icons, klickbar zu den jeweiligen
   Profilen).
10. **Rechtlicher Pflichtblock** (Firmierung ausgeschrieben „MSE Filterpressen Gesellschaft mit
    beschränkter Haftung", Geschäftsführung, Sitz, Registergericht, USt-IdNr.) in Medium Grey (`#707070`).
11. **Vertraulichkeitshinweis** (Standardtext, siehe Template), ebenfalls Medium Grey.
12. **„Think before you print"** mit kleinem grünem Blatt-Icon.

**Bewusste, dokumentierte Ausnahmen von den allgemeinen Farbregeln** (nur an dieser Stelle zulässig,
nicht auf andere Bausteine übertragbar):
- **Rot** im Phishing-/Sicherheitshinweis ist eine **Warnfarbe für einen Sicherheitshinweis**, keine
  dekorative Markenfarbe — deshalb hier zulässig, obwohl `brand-guidelines.md` Rot sonst ausschließt.
- **Grün** bei „Think before you print" ist ein **allgemein anerkanntes ökologisches Signalzeichen**
  im E-Mail-Fuß (keine Eco:LOGIC-Verwechslung, keine gestalterische Markenfarbe) — deshalb hier zulässig.

Beides bleibt auf genau diese zwei Stellen begrenzt; keine weiteren roten/grünen Elemente einführen.

## Wichtige Klarstellung zum Begriff "Thema"

Anders als bei den Content-Bausteinen (Newsletter, Social Posts etc.) ist mit "Thema" hier **kein**
Marketing-Thema gemeint. Dieser Skill erzeugt keine Kampagnen-Inhalte, sondern eine
Signatur(-Vorlage) für die Mitarbeitenden von MSE.

## Wann dieser Skill greift

- Der Nutzer möchte eine E-Mail-Signatur erstellen oder generieren lassen, z. B. "E-Mail-Signatur
  erstellen", "Signatur für Herrn Müller", "Signatur-Vorlage für alle Arbeitsplätze".
- Nicht zuständig für: Newsletter-Templates (`newsletter-brevo`), Social-Media-Grafiken, oder das
  Einrichten eines Signatur-Management-Systems selbst (siehe Abschnitt "Out of Scope").

## 1. Pflichtfrage zuerst: Verteilungsweg (manuell oder CI Sign)

**Bevor irgendetwas erzeugt wird, immer zuerst fragen**, wie die Signatur verteilt werden soll —
außer der Nutzer hat es im Briefing bereits eindeutig gesagt:

> "Soll die Signatur **manuell auf die Arbeitsplätze verteilt** werden (dann liefere ich sie mit
> einfachen Platzhaltern für Name, Abteilung usw.), oder im **CI-Sign-Format für die automatische
> Verteilung über CI Sign** (Platzhalter werden dann automatisch aus dem Active Directory befüllt)?"

Die Antwort bestimmt Template und Platzhalterformat:

**(a) Manuelle Verteilung** → Basis ist `templates/signatur-standard.html`. Die personenbezogenen
Felder bleiben als **einfache `{{...}}`-Platzhalter** im ausgelieferten HTML stehen — sie werden
später an jedem Arbeitsplatz (bzw. von der IT pro Mitarbeiter) von Hand ersetzt:

| Platzhalter | Bedeutung |
|---|---|
| `{{NAME}}` | Vollständiger Vor- und Nachname |
| `{{ROLE_DE}}` / `{{ROLE_EN}}` | Funktion/Rolle Deutsch / Englisch |
| `{{DEPARTMENT_DE}}` | Abteilung/Bereich |
| `{{PHONE}}` | Direkte Telefonnummer/Durchwahl |
| `{{EMAIL}}` | Persönliche E-Mail-Adresse |

Es werden dafür **keine Personendaten abgefragt** — die Vorlage ist bewusst personenneutral.
**Ausnahme:** Nennt der Nutzer ausdrücklich eine konkrete Person und wünscht eine fertig befüllte
Signatur, gelten die Pflichtangaben aus Abschnitt 1a und die Platzhalter werden direkt ersetzt.
Zusammen mit dem HTML immer eine kurze Ausfüll-Anleitung liefern (welcher Platzhalter = welches
Feld, Sonderzeichen als HTML-Entities einsetzen — siehe Abschnitt 4).

**(b) CI-Sign-Format (automatische Verteilung)** → Basis ist `templates/signatur-cisign.html` mit der
CI-Sign-Platzhaltersyntax (`@@attribut`/`##attribut`), die CI Sign automatisch aus dem
Active-Directory-Profil des jeweiligen Mitarbeiters befüllt — Details, Attributtabelle und
Einschränkungen in Abschnitt 5b. Auch hier werden keine Personendaten abgefragt.

In **beiden** Fällen bleiben die unternehmensweiten Platzhalter (Logo-, Icon-, Banner-URLs,
Social-Links) Teil des einen Rollouts und werden einmalig befüllt (siehe Abschnitt 4) — sie sind
nicht personenbezogen.

## 1a. Benötigte Eingaben (nur bei fertig befüllter Signatur für eine konkrete Person)

Nur relevant, wenn bei manueller Verteilung ausdrücklich eine **konkrete, namentlich benannte
Person** eingesetzt werden soll. Erforderlich (bei Fehlen kurz und direkt nachfragen — Namen niemals
raten oder annehmen):

- **Name** — vollständiger Vor- und Nachname der Person.
- **Funktion/Rolle** — auf Deutsch **und** Englisch (zweisprachig, wie im Referenzlayout), z. B.
  „Technische Geschäftsführung" / „Chief Technical Officer". Liefert der Nutzer nur eine Sprache,
  kurz nach der zweiten fragen bzw. eine sinnvolle Übersetzung vorschlagen und bestätigen lassen.
- **Direkte Telefonnummer/Durchwahl.**
- **Persönliche E-Mail-Adresse.**

Optional (gilt unabhängig vom Verteilungsweg auch für die Vorlagen-Varianten):

- **Abteilung/Bereich** (z. B. „Management", „Vertrieb International"). Fehlt sie bei einer konkreten
  Person, Zeile auf „MSE Filterpressen GmbH" kürzen (siehe Template-Kommentar); in der
  personenneutralen Vorlage bleibt `{{DEPARTMENT_DE}}` stehen.
- **Social-Profile**, die verlinkt werden sollen (LinkedIn/Instagram/X/Facebook) — nur die tatsächlich
  vorhandenen; nicht vorhandene Kanäle als ganze Spalte aus dem Template entfernen, keine toten Links.
- **Banner-Bild-Thema/-Anlass**, falls kein fertiges Bild vom Kunden vorliegt (siehe Abschnitt 2).

Beispiel für eine kurze Rückfrage, wenn Pflichtangaben fehlen:

> "Für die fertig befüllte Signatur brauche ich noch: vollständigen Namen, Funktion auf Deutsch und
> Englisch, Telefon-Durchwahl und die persönliche E-Mail-Adresse — magst du mir die kurz nennen?"

## 2. Banner-Bild: immer Foto + Headline + CTA in EINEM Bild — niemals ein bloßes Foto

Das Signatur-Banner ist **klickbar** (verlinkt auf `{{WEBSITE_URL}}` oder eine konkrete
Kampagnen-/Landingpage-URL), in **voller Signaturbreite** eingebunden — und **verbindlich immer aus
drei Elementen zusammengesetzt**, nicht nur ein rohes Foto:

1. **Hintergrundbild** (Foto/Visual, real oder generiert).
2. **Header/Headline** — eine kurze, markenkonforme Aussage im Bild selbst (z. B. Produktname +
   Kernaussage, wie „CellTRON Xtreme. Engineered for the toughest challenges.").
3. **CTA** — ein sichtbares Handlungselement im Bild (z. B. ein Pill-Button „CELLTRON XTREME
   ENTDECKEN ↗" im Ghost-/Solid-CTA-Stil aus `brand-guidelines.md` §7).

**Warum das ein einziges, fertig zusammengesetztes Bild sein muss statt HTML-Text über einem
Hintergrundbild:** E-Mail-HTML rendert Text-über-Bild-Layouts (`position:absolute`,
Hintergrundbilder auf `<td>`) über Outlook Desktop, Apple Mail, Gmail & Co. **nicht zuverlässig
identisch** — Outlook ignoriert `position:absolute` und `background-image` auf Tabellenzellen ohne
VML-Fallback häufig komplett. Die einzige across-alle-Clients bulletproof-Lösung ist ein **fertig
gerendertes, flaches Bild**, in dem Foto, Headline und CTA bereits verschmolzen sind.

**Wie das Banner erzeugt wird — zwei Wege, immer zuerst beim Nutzer erfragen, welcher gilt:**

1. **Kunde liefert ein fertiges Banner-Bild** (inkl. Header/CTA bereits im Bild): unverändert
   übernehmen, nur auf Plausibilität prüfen (Seitenverhältnis passend zur Signaturbreite).
2. **Banner wird selbst zusammengesetzt** (Standardfall, wenn kein fertiges Kundenbild vorliegt):
   a. Hintergrundbild beschaffen — Reihenfolge wie immer: bereits generierte/genehmigte Bilder aus
      `Outputs/`/`brand/product/` zuerst prüfen, sonst `bild-video-generierung` aufrufen (2K,
      Querformat, Motiv mit Freifläche für Text — siehe dortiger Prompt-Aufbau).
   b. Headline- und CTA-Text festlegen (kurz, markenkonform, aus bestätigten Fakten/Claims — nichts
      erfinden, siehe Abschnitt 3).
   c. **Text und CTA fest in das Bild einbrennen** — nicht per HTML-Overlay, sondern durch
      tatsächliches Kompositieren zu einem einzigen flachen Bild. Praktikabler Weg mit den in dieser
      Session verfügbaren Tools: ein kleines Python-Skript mit **Pillow** (`PIL.ImageDraw` +
      `PIL.ImageFont.truetype`), das die echte Nudica-Schriftdatei aus
      `brand/fonts/Nudica/Nudica Complete Desktop/Nudica-Bold.otf` lädt, Eyebrow/Headline in Weiß
      (mit dezentem Schlagschatten für Lesbarkeit, **kein** flächiges Overlay über dem ganzen Bild —
      siehe `landing-pages`-Konvention) sowie einen weißen CTA-Pill mit Pfeil-Kreis über das Foto
      zeichnet, und das Ergebnis als PNG speichert. Alternative: eine HTML/CSS-Komposition (Bild +
      `@font-face`-Nudica-Text + CTA) bauen und per Browser-Vorschau-Tool als Bild festhalten. In
      beiden Fällen ist das Resultat ein **einzelnes, fertiges PNG** — keine Live-HTML-Textebene im
      E-Mail-Code.

In beiden Fällen: das fertige (bereits Header+CTA enthaltende) Bild muss auf einer **stabil
gehosteten, öffentlich erreichbaren URL** liegen (kein Base64 — siehe Begründung in Abschnitt 3) und
wird in `{{BANNER_IMAGE_URL}}` eingesetzt; Klickziel in `{{BANNER_LINK_URL}}`.

### 2a. Responsives Banner — niemals ein festes `width`-Attribut auf dem `<img>`

**Verbindliche Regel, betrifft sowohl die gesamte Signatur-Tabelle als auch das Banner-Bild:** Auf
mobilen Geräten darf das Banner-Bild **nie über den sichtbaren Rand hinausragen/abgeschnitten
wirken**. Ursache eines bereits aufgetretenen Fehlers: Ein HTML-`width="..."`-Attribut auf einem
`<img>` (z. B. `width="592"`) wird von vielen mobilen Mail-Clients **wörtlich als feste Pixelbreite**
übernommen — auch dann, wenn die umgebende Tabellenzelle auf einem schmalen Bildschirm bereits auf
100 % geschrumpft ist. Das Bild bleibt dann bei seiner festen Pixelbreite und ragt über den
sichtbaren Rand hinaus: genau das erzeugt den „abgeschnitten"-Effekt.

**Deshalb gilt für Banner (und jedes andere große Bild in der Signatur) immer:**

1. **Kein `width="..."`-HTML-Attribut auf dem `<img>`** — ausschließlich CSS verwenden:
   `style="display:block; border:0; width:100%; max-width:592px; height:auto;"`. So übernimmt das
   Bild immer exakt die tatsächliche (fluide) Breite seiner Zelle, egal wie stark der Client die
   Tabelle auf dem jeweiligen Bildschirm skaliert.
2. **Die äußere Signatur-Tabelle selbst muss fluide sein**, nicht fest: `width="100%"` als
   HTML-Attribut **und** `style="width:100%; max-width:640px; ..."` — niemals `width="640"` als
   festes HTML-Attribut auf der äußeren Tabelle (derselbe Fehlermechanismus wie beim Bild, nur eine
   Ebene höher). Beide Templates (`signatur-standard.html`, `signatur-cisign.html`) sind bereits so
   aufgebaut — bei eigenen Anpassungen diese Struktur nicht auf feste Pixelbreiten zurückbauen.
3. Kleine Elemente (Logo 130px, Kontakt-Icons 18-24px) dürfen weiterhin ein festes `width`-Attribut
   behalten — sie sind so klein, dass sie auf keinem realistischen Bildschirm (auch nicht auf sehr
   schmalen Smartphones ab ca. 320px) über den Rand hinausragen können. Die Regel betrifft gezielt
   **große, breite Bilder** wie das Banner.
4. **Vor Auslieferung immer in einer schmalen Vorschau testen** (z. B. Browser-Vorschau-Tool auf
   ca. 375px Viewportbreite) — sichtbar prüfen, dass das Banner vollständig sichtbar bleibt und
   proportional mitschrumpft, nicht nur behaupten, dass es responsive sei.

### 2b. Grafiken für den Signatur-Anwendungsfall komprimieren (Pflicht, vor dem Hosten)

Die Signatur hängt an **jeder einzelnen ausgehenden E-Mail** — hier gelten die strengsten
Grenzwerte aller Bausteine. **Jede Grafik wird vor dem Hosten für diesen Anwendungsfall
optimiert** — niemals die 2K-Originale aus `bild-video-generierung` oder das komponierte
Banner-PNG in voller Auflösung direkt einbinden.

Verbindliche Vorgaben (Banner-Anzeigebreite max. 592 px):

| Grafik | Format | Abmessung (Export) | Zielgröße |
|---|---|---|---|
| Banner (Foto + Headline + CTA) | **JPEG, Qualität 70–80** (das komponierte PNG vor dem Hosten nach JPEG wandeln — Fotos als PNG sind um ein Vielfaches größer) | 1184 px Breite (2× 592 px für Retina) | ≤ 100 KB |
| Logo/Wortmarke | PNG (Transparenz), verlustfrei optimiert | 260 px Breite (2× 130 px) | ≤ 20 KB |
| Kontakt-/Blatt-Icons | PNG, verlustfrei optimiert | 36–48 px (2× Anzeigegröße) | ≤ 5 KB je Icon |
| Social-Icons | PNG, verlustfrei optimiert | 2× Anzeigegröße | ≤ 5 KB je Icon |

- **Gesamtgewicht aller Signatur-Grafiken: ≤ 150 KB** — liegt es darüber, zuerst die
  Banner-Qualität reduzieren.
- **Kein WebP/AVIF** — gleiche E-Mail-Client-Einschränkung wie beim Newsletter (Outlook Desktop).
- Praktische Umsetzung mit Bordmitteln (Pillow im Bash-Tool), sinngemäß:
  `python3 -c "from PIL import Image; im = Image.open('banner.png').convert('RGB'); im.thumbnail((1184, 10000)); im.save('banner.jpg', 'JPEG', quality=75, progressive=True, optimize=True)"`
- **Dateigröße nach dem Export prüfen** (`ls -la`) und erst dann hosten — nicht annehmen, dass die
  Grenzwerte eingehalten sind.

## 3. Markenkern zuerst laden (Pflicht)

Bevor Text oder HTML erzeugt werden, in dieser Reihenfolge lesen (relativ zum aktuellen
Arbeitsverzeichnis, dem CIDES-Root des Kunden):

1. `CLAUDE.md` — kompaktes Master-Brand-Dokument.
2. `brand/brand-guidelines.md`, insbesondere **§6 (Signaturen)** und **§7 (Icons)** — Details, die über
   das Referenzlayout in Abschnitt 0 hinausgehen (z. B. Logo-Schutzzone, Icon-Stil), gelten weiterhin.
3. `brand/color-palette.json` — verbindliche, maschinenlesbare Farbwerte.

Bei Widerspruch zwischen dieser Kurzfassung und den Original-Guidelines gewinnen `CLAUDE.md` bzw.
`brand-guidelines.md` — das gilt auch für die Farbgebung (heller/transparenter Untergrund, dunkle
Schrift/Icons). Die **Struktur** aus Abschnitt 0 (zweisprachige Rolle, Icon-Kontaktzeilen, Banner,
Social-Icons, Phishing-Hinweis, „Think before you print") ist die Vorgabe des Kunden und bleibt
verbindlich. Erfinde niemals eigene Farben, Claims oder Textbausteine (Phishing-Domain, Rechtsblock)
— nur die vom Kunden bestätigten Werte verwenden.

## 4. Template wiederverwenden

Nicht bei null anfangen: das Basis-Template liegt unter `templates/signatur-standard.html` (relativ
zum Verzeichnis dieses Skills). Es ist tabellenbasiert, vollständig inline gestylt (heller/
transparenter Untergrund, dunkle anthrazitfarbene Schrift und Icons) und enthält alle Platzhalter —
vollständige Liste im HTML-Kommentar am Kopf der Datei: `{{NAME}}`, `{{ROLE_DE}}`, `{{ROLE_EN}}`,
`{{DEPARTMENT_DE}}`, `{{PHONE}}`,
`{{EMAIL}}`, `{{WEBSITE_DISPLAY}}`, `{{WEBSITE_URL}}`, `{{ADDRESS}}`, `{{CORRECT_DOMAIN}}`,
`{{FAKE_DOMAIN_EXAMPLE}}`, `{{BANNER_IMAGE_URL}}`, `{{BANNER_ALT}}`, `{{BANNER_LINK_URL}}`, die vier
`{{SOCIAL_*_URL}}`/`{{SOCIAL_*_ICON_URL}}`-Paare sowie `{{ICON_PHONE_URL}}`, `{{ICON_EMAIL_URL}}`,
`{{ICON_WEB_URL}}`, `{{ICON_PIN_URL}}`, `{{ICON_LEAF_URL}}`.

Nicht vorhandene/gewünschte Elemente **vollständig entfernen** (ganze `<tr>`/`<td>`, keine leeren
Platzhalter oder toten Links stehen lassen) — v. a. bei Social-Icons: nur tatsächlich vorhandene
Kanäle behalten. **Verbindlich: im ausgelieferten HTML darf niemals sichtbarer Regieanweisungs-/
Hinweistext stehen** (z. B. "PLATZHALTER — ..." oder ähnliche Anweisungen an den Nutzer) — das
gehört, falls überhaupt nötig, in die Nachricht an den Nutzer außerhalb des HTML-Codes, niemals in
den gerenderten Signatur-Body selbst. Fehlen Angaben (z. B. Social-URLs), die betreffende Zeile/Spalte
sauber entfernen statt einen Hinweis dafür einzusetzen.

**Bewusste Ausnahme (Verteilungsweg "manuell", siehe Abschnitt 1):** Die personenbezogenen
`{{...}}`-Platzhalter (`{{NAME}}`, `{{ROLE_DE}}`, `{{ROLE_EN}}`, `{{DEPARTMENT_DE}}`, `{{PHONE}}`,
`{{EMAIL}}`) bleiben in der manuellen Vorlage **absichtlich stehen** — sie sind das Ausfüllformat
für die Arbeitsplätze und kein Verstoß gegen diese Regel. Beim CI-Sign-Format gilt dasselbe für die
`@@`/`##`-Attribute. Unternehmensweite Platzhalter (Logo/Icons/Banner/Social/Rechtsblock) müssen
dagegen in beiden Varianten vor Auslieferung real befüllt sein (bzw. mit explizitem Hinweis an den
Nutzer, siehe "Bildlogik" unten).

### Zeichencodierung: immer HTML-Entities für Sonderzeichen — niemals rohe UTF-8-Sonderzeichen

Die Signatur ist ein reines HTML-**Fragment** (kein `<head>`, kein `<meta charset>`), weil sie meist
direkt in das "Signatur bearbeiten"-Feld eines Mail-Clients eingefügt wird. Ohne eigene
Zeichensatz-Deklaration interpretieren manche Clients beim Einfügen rohe UTF-8-Sonderzeichen (ü, ö,
ä, ß, é …) fälschlich als Latin-1/Windows-1252 — sichtbares Symptom: „Grüßen" wird zu „GrÃ¼Ã&#65533;en".
Deshalb **für jeden Namen, jede Rolle und jeden sonstigen erzeugten Text mit deutschen Umlauten oder
Akzenten immer HTML-Entities verwenden**, nie das rohe Zeichen:

| Zeichen | Entity |
|---|---|
| ä / Ä | `&auml;` / `&Auml;` |
| ö / Ö | `&ouml;` / `&Ouml;` |
| ü / Ü | `&uuml;` / `&Uuml;` |
| ß | `&szlig;` |
| é / É | `&eacute;` / `&Eacute;` |
| „ / " (dt. Anführungszeichen) | `&bdquo;` / `&ldquo;` |

Das Template selbst hält sich bereits konsequent daran (z. B. „Gr&uuml;&szlig;en", „Rum&eacute;" in
den festen Textbausteinen) — beim Einsetzen von `{{NAME}}`, `{{ROLE_DE}}`, `{{DEPARTMENT_DE}}` etc.
genauso verfahren, auch wenn der Nutzer den Namen mit rohen Umlauten/Akzenten angibt.

### Bildlogik: kein Base64, sondern gehostete URLs

E-Mail-Clients (insbesondere Outlook Desktop, aber auch viele Web-Clients) blockieren oder entfernen
eingebettete Base64-Bilder standardmäßig oder zeigen sie inkonsistent an. Deshalb **nicht** Logo,
Icons oder Banner als Base64-Data-URI einbetten. Stattdessen:

- Alle Bild-Platzhalter (`{{BANNER_IMAGE_URL}}`, `{{ICON_*_URL}}`, `{{SOCIAL_*_ICON_URL}}`) müssen auf
  eine **stabile, öffentlich erreichbare URL** verweisen.
- Empfehlung an den Kunden: Icons/Banner auf eigenem Webspace hosten, idealerweise unter
  `mse-filterpressen.com` (z. B. `https://mse-filterpressen.com/assets/signatur/...`).
- Liegt noch keine echte URL vor, den Platzhalter sichtbar im ausgelieferten HTML stehen lassen und
  den Nutzer explizit darauf hinweisen, ihn vor dem produktiven Einsatz zu ersetzen.

## 5. Ausgabe: HTML-Code plus Einbindungs-Hinweise

Die Ausgabe richtet sich nach dem in Abschnitt 1 abgefragten Verteilungsweg. Dem Nutzer immer beides
liefern — den HTML-Quellcode als Code-Block **und** die passenden Einbindungs-Hinweise:

**(a) Manuelle Verteilung auf die Arbeitsplätze** (Outlook, Apple Mail, Gmail):
- HTML auf Basis von `signatur-standard.html`; personenbezogene Felder als einfache
  `{{...}}`-Platzhalter (siehe Abschnitt 1), unternehmensweite Platzhalter befüllt. Bei ausdrücklich
  gewünschter Einzelperson-Signatur: vollständig befüllt (Abschnitt 1a).
- Ausschließlich **inline Styles**, **kein externes Stylesheet**, **kein Flexbox/Grid** — nur
  tabellenbasiertes Layout, genau wie im Template umgesetzt (Outlook Desktop ist bei CSS
  erfahrungsgemäß am zickigsten).
- Einbindung: pro Arbeitsplatz die Platzhalter durch die echten Personendaten ersetzen (Umlaute als
  HTML-Entities, siehe Abschnitt 4), dann in den Signatur-Einstellungen des jeweiligen Clients die
  HTML-Quelle einfügen bzw. über "Signatur bearbeiten (HTML)" importieren. Die mitgelieferte kurze
  Ausfüll-Anleitung (Platzhalter → Feld) gehört immer dazu.

**(b) CI-Sign-Format für die automatische Verteilung über CI Sign:**
- HTML auf Basis von `signatur-cisign.html` mit der CI-Sign-Platzhaltersyntax (siehe Abschnitt 5b) —
  **niemals** das Standard-Template mit fest eingesetzten Personendaten oder `{{...}}`-Platzhaltern
  für diesen Weg verwenden, sonst zieht CI Sign die Werte nicht automatisch pro Mitarbeiter.
- **Wichtiger Hinweis (verbindlich, immer erwähnen):** Die Einrichtung eines externen
  Signatur-Management-Systems (z. B. CI Sign) ist **nicht Bestandteil dieses Angebots** und würde
  **gesondert beauftragt und abgerechnet**. Dieser Skill liefert ausschließlich das HTML.

## 5b. CI-Sign-Variante — Platzhalter für automatischen Personenbezug

Hat der Nutzer in der Pflichtfrage (Abschnitt 1) den **CI-Sign-Weg** gewählt, **immer**
`templates/signatur-cisign.html` als Basis verwenden statt `signatur-standard.html`. Der
einzige Unterschied: alle personenbezogenen Felder sind durch die CI-Sign-Platzhaltersyntax ersetzt,
sodass CI Sign die Werte automatisch aus dem Active-Directory-Profil des jeweiligen Mitarbeiters
zieht — es muss dann **nicht** pro Mitarbeiter eine eigene HTML-Datei erzeugt werden.

**CI-Sign-Syntax (recherchiert und bestätigt, siehe ci-solution.com-Dokumentation):**

| Syntax | Verhalten bei leerem Attribut |
|---|---|
| `@@attributName` | Nur der Platzhalter (inkl. eines direkt folgenden Leerzeichens) wird entfernt, der Rest der Zeile bleibt stehen. |
| `##attributName` | Die **gesamte Zeile**, in der der Platzhalter steht, wird entfernt. |

**Bestätigte AD-Attributnamen → Verwendung in der Signatur:**

| CI-Sign-Attribut | Bedeutung | Ersetzt in `signatur-standard.html` |
|---|---|---|
| `displayName` | Vollständiger Name | `{{NAME}}` |
| `title` | Funktion/Rolle (**nur eine Sprache**, AD kennt kein zweisprachiges Attribut) | `{{ROLE_DE}}`/`{{ROLE_EN}}` |
| `department` | Abteilung/Bereich | `{{DEPARTMENT_DE}}` |
| `telephoneNumber` | Direktdurchwahl | `{{PHONE}}` |
| `mobile` | Mobiltelefon (optional) | — (neue optionale Zeile) |
| ~~`facsimileTelephoneNumber`~~ | Fax — **NICHT verwenden**: Faxnummern werden laut Kundenvorgabe nirgends genannt (gilt für alle Bausteine) | — |
| `mail` | persönliche E-Mail-Adresse | `{{EMAIL}}` |
| `streetAdress` | Straße/Hausnummer (**exakt diese Schreibweise**, kein Tippfehler — offizielle CI-Sign-Attributbezeichnung) | Teil von `{{ADDRESS}}` |
| `postalCode` | PLZ | Teil von `{{ADDRESS}}` |
| `l` | Ort/Stadt | Teil von `{{ADDRESS}}` |
| `company` | Firma (i. d. R. statisch, da nur eine Firma) | — |

**Wichtige Einschränkungen, immer beachten:**

- **Keine Zweisprachigkeit für die Rolle**: `title` ist ein einzelnes AD-Attribut. Vor dem Rollout mit
  dem Kunden klären, ob (a) ein eigenes benutzerdefiniertes AD-Attribut für die englische Rolle
  angelegt wird (IT-seitig, außerhalb dieses Angebots) oder (b) nur die deutsche Rolle automatisch
  gezogen wird. Niemals eigenmächtig entscheiden oder die zweite Sprache stillschweigend weglassen,
  ohne den Nutzer darauf hinzuweisen.
- **Zeilen-Lösch-Verhalten vor Rollout verifizieren**: Ob `##` auf HTML-Ebene tatsächlich die gesamte
  `<tr>` entfernt oder nur die Textzeile innerhalb einer Zelle, hängt vom jeweiligen CI-Sign-
  Versionsstand ab. Vor dem unternehmensweiten Rollout **immer** einen Testexport mit einem Profil MIT
  und einem Profil OHNE optionales Attribut (z. B. ohne `mobile`) durchführen und das Ergebnis prüfen.
- **Unternehmensweite Platzhalter bleiben `{{...}}`**: Logo, Banner, Icons, Social-Links, Rechtsblock
  und Phishing-Domains sind nicht personenbezogen und werden weiterhin einmalig beim Rollout befüllt,
  nicht über CI-Sign-Attribute.
- Vollständige Platzhalterliste inkl. Kommentaren direkt im Kopf von `templates/signatur-cisign.html`.

## 6. Speicherort

Fertige Signatur speichern unter `Outputs/signaturen/`, Dateiname je nach Variante:

| Variante | Dateiname |
|---|---|
| Manuelle Vorlage (personenneutral, `{{...}}`-Platzhalter) | `signatur-vorlage-manuell.html` |
| CI-Sign-Format | `signatur-vorlage-cisign.html` |
| Fertig befüllt für eine konkrete Person | `<name-slug>.html` |

`<name-slug>` = Name der Person in Kleinbuchstaben, Leerzeichen durch Bindestriche ersetzt, ohne
Sonderzeichen/Umlaute ausschreiben (z. B. "Jürgen Müller" → `juergen-mueller.html`).

## 7. QA-Checkliste (vor Auslieferung prüfen)

- [ ] **Verteilungsweg abgefragt** (manuell vs. CI Sign, Abschnitt 1) — nicht angenommen — und das
      dazu passende Template/Platzhalterformat verwendet (manuell = `{{...}}`-Platzhalter bzw. auf
      Wunsch fertig befüllt; CI Sign = `@@`/`##`-Attribute)?
- [ ] Bei manueller Vorlage: alle fünf personenbezogenen Platzhalter (`{{NAME}}`, `{{ROLE_DE}}`,
      `{{ROLE_EN}}`, `{{DEPARTMENT_DE}}`, `{{PHONE}}`, `{{EMAIL}}`) unverändert vorhanden und eine
      kurze Ausfüll-Anleitung mitgeliefert?
- [ ] Hintergrund **explizit weiß** gesetzt (`bgcolor="#FFFFFF"` **und** `background-color:#FFFFFF`
      inline) — **niemals** `transparent` oder gar keine Hintergrundfarbe (sonst Dark-Mode-Risiko:
      Mail-Client/Browser legt einen eigenen dunklen Canvas darunter, anthrazitfarbene Schrift wird
      unsichtbar)? Durchgängig **anthrazitfarbene** (`#1B1B1B`) Schrift und Icons — nicht Weiß-auf-Dunkel?
- [ ] **{{LOGO_URL}} zeigt auf das echte Logo-Asset aus `brand/logo/`** — nicht weggelassen, kein
      Klartext-Ersatz, kein selbst nachgezeichnetes/generiertes Logo?
- [ ] **Trennlinie unter dem Namensblock in dunkler Farbe (`#1B1B1B`), NIEMALS blau** (Kundenvorgabe
      für Trennstriche überall)?
- [ ] **Keine Faxnummer** irgendwo in der Signatur (Kundenvorgabe: Fax wird nirgends genannt)?
- [ ] **Banner-Bild: heller Text hebt sich auch über hellen Bildbereichen ab** (weicher Schatten,
      macht `compose_slide.py` automatisch) — Sichtprüfung am fertigen Banner?
- [ ] Zweisprachige Grußzeile und zweisprachige Funktionsbezeichnung (DE | EN) vorhanden?
- [ ] Schriftart `'Nudica', Arial, sans-serif` (oder gleichwertiger Safe-Fallback-Stack) durchgängig?
- [ ] Alle vier Kontaktzeilen (Telefon, E-Mail, Website, Standort) mit Icon **und** funktionierendem
      Link (`tel:`, `mailto:`, Website-URL)?
- [ ] Phishing-Hinweis vorhanden, korrekte echte Domain, **keine erfundene** Fake-Domain (nur vom
      Kunden bestätigte Beispiele verwenden oder die Zeile generisch halten)?
- [ ] **Banner ist ein fertig komponiertes Bild aus Foto + Headline + CTA** (nicht nur ein rohes
      Foto), klickbar (auf Website/Kampagnen-URL verlinkt), in passender Auflösung/Seitenverhältnis?
- [ ] **Banner-`<img>` hat KEIN festes `width="..."`-HTML-Attribut**, nur CSS `width:100%;
      max-width:...px; height:auto;` — und die äußere Signatur-Tabelle ist fluide (`width="100%"`
      + `style="max-width:640px"`, nicht `width="640"` fest)? In einer schmalen Vorschau
      (~375px) getestet, dass das Banner vollständig sichtbar bleibt und nicht abgeschnitten wird
      (siehe Abschnitt 2a)?
- [ ] **Alle vier Kontakt-Icons und das Blatt-Icon sind echte `<img>`-Grafiken** (nicht Unicode-/
      Emoji-Zeichen als Text) und laden tatsächlich sichtbar — im Browser/Vorschau-Tool geprüft, nicht
      nur angenommen?
- [ ] **Kein sichtbarer Regieanweisungs-/Hinweistext im HTML-Body** (z. B. "PLATZHALTER — ...") —
      fehlende Angaben führen zum sauberen Entfernen der Zeile, nicht zu einem Hinweistext?
      (Personenbezogene `{{...}}`- bzw. `@@`/`##`-Platzhalter der jeweiligen Vorlagen-Variante sind
      die dokumentierte Ausnahme, siehe Abschnitt 4.)
- [ ] **Alle Sonderzeichen (ä/ö/ü/ß/é) als HTML-Entities gesetzt**, nicht als rohes UTF-8-Zeichen —
      Stichprobe: Vorschau im Browser zeigt korrekte Umlaute, keine "Ã¼"-artige Mojibake?
- [ ] Nur tatsächlich vorhandene Social-Kanäle verlinkt, keine toten/leeren Icon-Links?
- [ ] Rechtlicher Pflichtblock korrekt und vollständig (Firmierung ausgeschrieben, Geschäftsführung,
      Sitz, Registergericht HRB 502677, USt-IdNr. DE144200297)?
- [ ] Vertraulichkeitshinweis vorhanden (Standardtext aus Template)?
- [ ] „Think before you print" mit grünem Blatt-Icon vorhanden?
- [ ] Keine weiteren roten/grünen Elemente außerhalb der zwei dokumentierten Ausnahmen (Abschnitt 0)?
- [ ] HTML tabellenbasiert, ausschließlich Inline-Styles, kein externes Stylesheet, kein
      Flexbox/Grid — kompatibel mit Outlook Desktop, Apple Mail, Gmail?
- [ ] Alle Bild-Platzhalter nutzen gehostete URLs, **kein** eingebettetes Base64-Bild?
- [ ] **Grafiken für den Signatur-Anwendungsfall komprimiert** (Abschnitt 2b): Banner als JPEG
      ≤ 100 KB (1184 px), Logo ≤ 20 KB, Icons ≤ 5 KB je Stück, Gesamtgewicht ≤ 150 KB, kein
      WebP/AVIF — Dateigrößen tatsächlich geprüft, keine unkomprimierten Originale gehostet?
- [ ] Datei unter `Outputs/signaturen/` mit dem zur Variante passenden Dateinamen gespeichert
      (`signatur-vorlage-manuell.html` / `signatur-vorlage-cisign.html` / `<name-slug>.html`,
      siehe Abschnitt 6)?
- [ ] Bei CI-Sign-Rollout: `templates/signatur-cisign.html` (nicht `signatur-standard.html`) verwendet,
      korrekte `@@`/`##`-Syntax je Feld, Zweisprachigkeits-Einschränkung bei `title` mit dem Kunden
      geklärt, Zeilen-Lösch-Verhalten vor dem Rollout testexportiert (siehe Abschnitt 5b)?
