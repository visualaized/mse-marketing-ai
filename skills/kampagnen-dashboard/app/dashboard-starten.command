#!/bin/bash
# MSE Kampagnen-Dashboard — Doppelklick-Starter für macOS
# Startet den lokalen Dashboard-Server (node server.mjs) und öffnet den Browser.
# Voraussetzung: Node.js ist installiert (nodejs.org). Fenster offen lassen,
# solange das Dashboard genutzt wird; Beenden mit Ctrl+C.

cd "$(dirname "$0")"

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js wurde nicht gefunden. Bitte von https://nodejs.org installieren"
  echo "und diesen Starter danach erneut ausführen."
  read -r -p "Enter zum Schließen…"
  exit 1
fi

( sleep 1 && open "http://localhost:8787" ) &
node server.mjs
