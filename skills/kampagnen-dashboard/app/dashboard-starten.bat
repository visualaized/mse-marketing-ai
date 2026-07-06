@echo off
rem MSE Kampagnen-Dashboard — Doppelklick-Starter fuer Windows
rem Startet den lokalen Dashboard-Server (node server.mjs) und oeffnet den Browser.
rem Voraussetzung: Node.js ist installiert (nodejs.org). Fenster offen lassen,
rem solange das Dashboard genutzt wird; Beenden mit Strg+C oder Fenster schliessen.

cd /d "%~dp0"

where node >nul 2>nul
if errorlevel 1 (
  echo Node.js wurde nicht gefunden. Bitte von https://nodejs.org installieren
  echo und diesen Starter danach erneut ausfuehren.
  pause
  exit /b 1
)

start "" "http://localhost:8787"
node server.mjs
pause
