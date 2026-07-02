#!/usr/bin/env python3
"""
build_whitepaper.py — MSE Filterpressen GmbH

Baut aus einer befüllten Whitepaper-HTML-Datei (Basis: templates/whitepaper-template.html)
das fertige, on-brand PDF:

1. Bettet die echten Nudica-Schriften (Regular/Medium/Bold) als Base64-Data-URIs ein —
   ersetzt die Platzhalter {{FONT_DATA_URI_REGULAR}} / {{FONT_DATA_URI_MEDIUM}} /
   {{FONT_DATA_URI_BOLD}}, falls noch vorhanden.
2. Rendert die HTML-Datei über Chrome/Chromium headless nach PDF
   (`--headless --print-to-pdf`, randlos — die Vorlage bringt ihre A4-Seitengeometrie
   selbst mit: @page size A4 / margin 0 + .page 210x297mm).

Aufruf:
  python3 build_whitepaper.py \
    --html "Outputs/2026-07-15-thema-whitepaper/whitepaper.html" \
    --font-dir "brand/fonts/Nudica/Nudica Complete Desktop" \
    --out "Outputs/2026-07-15-thema-whitepaper/whitepaper.pdf"

Findet Chrome automatisch (macOS/Windows/Linux, inkl. Edge als Chromium-Fallback).
Falls kein Chrome gefunden wird: die (bereits font-eingebettete) HTML-Datei im Browser
öffnen und über Datei -> Drucken -> "Als PDF sichern" exportieren (Ränder: Keine,
Hintergrundgrafiken: an) — ergibt dasselbe Dokument.

Nur Python-Standardbibliothek — kein pip install nötig.
"""

import argparse
import base64
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHROME_CANDIDATES = [
    # macOS
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    # Windows (unter python.exe direkt aufrufbar)
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    # Linux
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
]


def find_chrome():
    for name in ("google-chrome", "chromium", "chrome", "msedge"):
        path = shutil.which(name)
        if path:
            return path
    for cand in CHROME_CANDIDATES:
        if Path(cand).exists():
            return cand
    return None


def font_data_uri(path):
    return "data:font/opentype;base64," + base64.b64encode(Path(path).read_bytes()).decode()


def main():
    ap = argparse.ArgumentParser(description="Whitepaper-HTML -> on-brand PDF (Chrome headless).")
    ap.add_argument("--html", required=True, help="Befüllte Whitepaper-HTML-Datei.")
    ap.add_argument("--font-dir", required=True, help="Ordner mit Nudica-Regular/-Medium/-Bold.otf.")
    ap.add_argument("--out", required=True, help="Ausgabepfad des PDF.")
    args = ap.parse_args()

    html_path = Path(args.html)
    font_dir = Path(args.font_dir)
    out_path = Path(args.out)

    html = html_path.read_text(encoding="utf-8")

    replacements = {
        "{{FONT_DATA_URI_REGULAR}}": font_dir / "Nudica-Regular.otf",
        "{{FONT_DATA_URI_MEDIUM}}": font_dir / "Nudica-Medium.otf",
        "{{FONT_DATA_URI_BOLD}}": font_dir / "Nudica-Bold.otf",
    }
    changed = False
    for placeholder, font_file in replacements.items():
        if placeholder in html:
            if not font_file.exists():
                sys.exit(f"FEHLER: Font-Datei fehlt: {font_file}")
            html = html.replace(placeholder, font_data_uri(font_file))
            changed = True

    leftover = [p for p in ("{{",) if p in html]
    if leftover:
        # Nur warnen — bewusst kein Abbruch, damit man Zwischenstände rendern kann.
        print("WARNUNG: Es sind noch unbefüllte {{...}}-Platzhalter im HTML enthalten.")

    # Font-eingebettete Fassung neben das Original schreiben (dauerhafte, portable Quelle,
    # aus der jederzeit erneut gedruckt werden kann).
    embedded_path = html_path if not changed else html_path.with_suffix(".embedded.html")
    if changed:
        embedded_path.write_text(html, encoding="utf-8")
        print(f"Font-eingebettete HTML geschrieben: {embedded_path}")

    chrome = find_chrome()
    if not chrome:
        sys.exit(
            "Kein Chrome/Chromium/Edge gefunden. Alternative: die Datei\n"
            f"  {embedded_path}\n"
            "im Browser öffnen und über Drucken -> 'Als PDF sichern' exportieren\n"
            "(Ränder: Keine, Hintergrundgrafiken: an)."
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [
            chrome,
            "--headless=new",     # neuer Headless-Modus: terminiert zuverlässig nach dem Export
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={out_path.resolve()}",
            f"--user-data-dir={tmp}",
            embedded_path.resolve().as_uri(),
        ]
        try:
            # Timeout als Sicherheitsnetz: ältere Chrome-Versionen beenden den Prozess nach dem
            # PDF-Export teils nicht — das PDF liegt dann trotzdem vollständig auf der Platte.
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
            stderr = result.stderr
        except subprocess.TimeoutExpired as exc:
            stderr = (exc.stderr or b"").decode(errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        if not out_path.exists() or out_path.stat().st_size == 0:
            sys.exit(f"Chrome-PDF-Export fehlgeschlagen:\n{stderr[-2000:]}")

    print(f"Whitepaper-PDF geschrieben: {out_path}")


if __name__ == "__main__":
    main()
