#!/usr/bin/env node
/**
 * server.mjs
 *
 * Lokaler Server für das Kampagnen-Dashboard — statischer Dateiserver PLUS kleine
 * Planungs-API, mit der der Kunde direkt im Dashboard neue Kampagnen PLANEN kann
 * (Status "geplant" mit Veröffentlichungsdatum, Kanälen und Notizen).
 *
 * Endpunkte:
 *   GET  /                       Dashboard (index.html, styles.css, …)
 *   GET  /campaigns-index.json   Kampagnenliste — wird bei jedem Aufruf LIVE aus
 *                                Campaigns/<slug>/meta.json generiert (nie veraltet);
 *                                zusätzlich wird die statische campaigns-index.json
 *                                aktualisiert, damit auch rein statisches Hosting
 *                                (z. B. Showcase-Kopie) einen brauchbaren Stand hat.
 *   GET  /api/ping               Feature-Detection für die Oberfläche: antwortet nur
 *                                dieser Server (statisches Hosting → 404) — daran
 *                                erkennt index.html, ob das Planungsformular gezeigt wird.
 *   POST /api/campaigns          Neue GEPLANTE Kampagne anlegen. JSON-Body:
 *                                { thema, kanaele: [...], zeitraum_start: "YYYY-MM-DD",
 *                                  zeitraum_ende?, notiz?, verantwortlich? }
 *                                Schreibt Campaigns/<slug>/meta.json mit status "geplant".
 *   PUT  /api/campaigns/<slug>   GEPLANTE Kampagne bearbeiten (gleicher Body wie POST).
 *                                Nur für Einträge mit status "geplant" erlaubt — laufende/
 *                                abgeschlossene Kampagnen werden über die Bausteine gepflegt.
 *   DELETE /api/campaigns/<slug> GEPLANTE Kampagne löschen (nur status "geplant").
 *   GET  /hub/<pfad>             Liest Dateien aus dem Marketing-Hub-Root (eine Ebene über dem
 *                                App-Ordner) NUR lesend aus — damit die Inhalte-Links der
 *                                Kampagnen (meta.json-Feld "inhalte", Pfade relativ zum Hub-Root
 *                                wie "Outputs/...") direkt im Browser geöffnet werden können.
 *
 * Campaigns-Ordner: standardmäßig "../Campaigns" relativ zu diesem Skript — das entspricht
 * der Standard-Ablage im Marketing Hub (Kampagnen-Dashboard/ und Campaigns/ liegen beide im
 * Hub-Root). Abweichender Pfad über die Umgebungsvariable CAMPAIGNS_DIR.
 *
 * Aufruf:
 *   node server.mjs            (Port 8787, oder PORT-Umgebungsvariable)
 *   node server.mjs 3000       (Port als erstes CLI-Argument)
 *
 * Nur eingebaute Module (http/fs/path) — kein Express, kein npm install nötig.
 */

import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT_DIR = __dirname;
const CAMPAIGNS_DIR = process.env.CAMPAIGNS_DIR
  ? path.resolve(process.cwd(), process.env.CAMPAIGNS_DIR)
  : path.resolve(__dirname, "../Campaigns");
// Marketing-Hub-Root (für den lesenden /hub/-Mount der Inhalte-Links): eine Ebene über dem
// App-Ordner — dieselbe Ablage-Konvention wie bei CAMPAIGNS_DIR. Override via HUB_DIR.
const HUB_DIR = process.env.HUB_DIR
  ? path.resolve(process.cwd(), process.env.HUB_DIR)
  : path.resolve(__dirname, "..");

const PORT = Number(process.argv[2]) || Number(process.env.PORT) || 8787;

const VALID_KANAELE = [
  "Bild/Video",
  "Instagram",
  "LinkedIn",
  "X",
  "Newsletter-DE",
  "Newsletter-EN",
  "Landing Page",
  "E-Mail-Signatur",
  "Whitepaper",
];

const CONTENT_TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".md": "text/plain; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
  ".otf": "font/otf",
  ".ico": "image/x-icon",
};

function contentTypeFor(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return CONTENT_TYPES[ext] || "application/octet-stream";
}

function safeResolve(requestUrl) {
  const urlPath = decodeURIComponent(requestUrl.split("?")[0]);
  const relativePath = urlPath === "/" ? "/index.html" : urlPath;
  const resolved = path.join(ROOT_DIR, path.normalize(relativePath));
  if (!resolved.startsWith(ROOT_DIR)) {
    return null;
  }
  return resolved;
}

/* ------------------------------------------------------------------ *
 *  Kampagnen-Index: live aus Campaigns/<slug>/meta.json generieren
 * ------------------------------------------------------------------ */

function buildIndex() {
  if (!fs.existsSync(CAMPAIGNS_DIR)) {
    return [];
  }
  const entries = [];
  for (const dirent of fs.readdirSync(CAMPAIGNS_DIR, { withFileTypes: true })) {
    if (!dirent.isDirectory()) continue;
    const metaPath = path.join(CAMPAIGNS_DIR, dirent.name, "meta.json");
    if (!fs.existsSync(metaPath)) continue;
    try {
      const meta = JSON.parse(fs.readFileSync(metaPath, "utf-8"));
      meta.slug = dirent.name;
      entries.push(meta);
    } catch (err) {
      console.warn("Überspringe ungültige meta.json in " + dirent.name + ": " + err.message);
    }
  }
  entries.sort((a, b) => String(b.zeitraum_start || "").localeCompare(String(a.zeitraum_start || "")));
  return entries;
}

function writeStaticIndex(index) {
  // Statische Kopie neben index.html aktualisieren, damit auch ein rein statisches
  // Hosting (ohne diesen Server) einen aktuellen Stand ausliefert.
  try {
    fs.writeFileSync(path.join(ROOT_DIR, "campaigns-index.json"), JSON.stringify(index, null, 2) + "\n", "utf-8");
  } catch (err) {
    console.warn("Konnte statische campaigns-index.json nicht schreiben: " + err.message);
  }
}

/* ------------------------------------------------------------------ *
 *  Planungs-API
 * ------------------------------------------------------------------ */

function slugify(value) {
  return String(value)
    .toLowerCase()
    .replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 60) || "kampagne";
}

function sendJson(res, statusCode, payload) {
  res.writeHead(statusCode, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(payload));
}

function validatePlanPayload(body) {
  const errors = [];
  if (!body || typeof body !== "object") {
    return ["Ungültiger Request-Body."];
  }
  if (!body.thema || !String(body.thema).trim()) {
    errors.push("Feld 'thema' ist Pflicht.");
  }
  if (!Array.isArray(body.kanaele) || body.kanaele.length === 0) {
    errors.push("Feld 'kanaele' ist Pflicht (mindestens ein Kanal).");
  } else {
    for (const k of body.kanaele) {
      if (!VALID_KANAELE.includes(k)) {
        errors.push("Unbekannter Kanal: " + k);
      }
    }
  }
  if (!body.zeitraum_start || !/^\d{4}-\d{2}-\d{2}$/.test(String(body.zeitraum_start))) {
    errors.push("Feld 'zeitraum_start' (geplantes Veröffentlichungsdatum) ist Pflicht im Format YYYY-MM-DD.");
  }
  if (body.zeitraum_ende && !/^\d{4}-\d{2}-\d{2}$/.test(String(body.zeitraum_ende))) {
    errors.push("Feld 'zeitraum_ende' muss das Format YYYY-MM-DD haben.");
  }
  return errors;
}

function readBody(req, callback) {
  let raw = "";
  req.on("data", (chunk) => {
    raw += chunk;
    if (raw.length > 64 * 1024) {
      req.destroy();
    }
  });
  req.on("end", () => callback(raw));
}

function buildMetaFromPayload(body, existingMeta) {
  const meta = {
    thema: String(body.thema).trim(),
    kanaele: body.kanaele,
    status: "geplant",
    zeitraum_start: String(body.zeitraum_start),
  };
  if (body.zeitraum_ende) meta.zeitraum_ende = String(body.zeitraum_ende);
  if (body.verantwortlich && String(body.verantwortlich).trim()) meta.verantwortlich = String(body.verantwortlich).trim();
  if (body.notiz && String(body.notiz).trim()) meta.notiz = String(body.notiz).trim();
  // Felder erhalten, die das Formular nicht kennt (z. B. inhalte, falls schon vorhanden)
  if (existingMeta && Array.isArray(existingMeta.inhalte)) meta.inhalte = existingMeta.inhalte;
  meta.quelle = (existingMeta && existingMeta.quelle) || "dashboard-planung";
  return meta;
}

function handleCreateCampaign(req, res) {
  readBody(req, (raw) => {
    let body;
    try {
      body = JSON.parse(raw);
    } catch {
      return sendJson(res, 400, { ok: false, errors: ["Body ist kein gültiges JSON."] });
    }

    const errors = validatePlanPayload(body);
    if (errors.length) {
      return sendJson(res, 400, { ok: false, errors });
    }

    const baseSlug = slugify(body.thema);
    let slug = baseSlug;
    let counter = 2;
    while (fs.existsSync(path.join(CAMPAIGNS_DIR, slug))) {
      slug = baseSlug + "-" + counter++;
    }

    const meta = buildMetaFromPayload(body, null);

    try {
      fs.mkdirSync(path.join(CAMPAIGNS_DIR, slug), { recursive: true });
      fs.writeFileSync(
        path.join(CAMPAIGNS_DIR, slug, "meta.json"),
        JSON.stringify(meta, null, 2) + "\n",
        "utf-8",
      );
    } catch (err) {
      return sendJson(res, 500, { ok: false, errors: ["Konnte meta.json nicht schreiben: " + err.message] });
    }

    writeStaticIndex(buildIndex());
    sendJson(res, 201, { ok: true, slug, meta });
  });
}

function loadPlannedMeta(slug) {
  // Nur saubere Slugs akzeptieren (kein Traversal), nur existierende geplante Kampagnen liefern.
  if (!/^[a-z0-9-]+$/.test(slug)) return { error: [400, "Ungültiger Kampagnen-Slug."] };
  const metaPath = path.join(CAMPAIGNS_DIR, slug, "meta.json");
  if (!fs.existsSync(metaPath)) return { error: [404, "Kampagne nicht gefunden: " + slug] };
  let meta;
  try {
    meta = JSON.parse(fs.readFileSync(metaPath, "utf-8"));
  } catch {
    return { error: [500, "meta.json ist nicht lesbar/kein gültiges JSON."] };
  }
  if (meta.status !== "geplant") {
    return { error: [409, "Nur Kampagnen mit Status 'geplant' können über das Dashboard bearbeitet oder gelöscht werden."] };
  }
  return { meta, metaPath };
}

function handleUpdateCampaign(req, res, slug) {
  const loaded = loadPlannedMeta(slug);
  if (loaded.error) return sendJson(res, loaded.error[0], { ok: false, errors: [loaded.error[1]] });

  readBody(req, (raw) => {
    let body;
    try {
      body = JSON.parse(raw);
    } catch {
      return sendJson(res, 400, { ok: false, errors: ["Body ist kein gültiges JSON."] });
    }

    const errors = validatePlanPayload(body);
    if (errors.length) {
      return sendJson(res, 400, { ok: false, errors });
    }

    const meta = buildMetaFromPayload(body, loaded.meta);
    try {
      fs.writeFileSync(loaded.metaPath, JSON.stringify(meta, null, 2) + "\n", "utf-8");
    } catch (err) {
      return sendJson(res, 500, { ok: false, errors: ["Konnte meta.json nicht schreiben: " + err.message] });
    }

    writeStaticIndex(buildIndex());
    sendJson(res, 200, { ok: true, slug, meta });
  });
}

function handleDeleteCampaign(res, slug) {
  const loaded = loadPlannedMeta(slug);
  if (loaded.error) return sendJson(res, loaded.error[0], { ok: false, errors: [loaded.error[1]] });

  try {
    fs.rmSync(path.join(CAMPAIGNS_DIR, slug), { recursive: true });
  } catch (err) {
    return sendJson(res, 500, { ok: false, errors: ["Konnte Kampagnen-Ordner nicht löschen: " + err.message] });
  }

  writeStaticIndex(buildIndex());
  sendJson(res, 200, { ok: true, slug });
}

/* ------------------------------------------------------------------ *
 *  HTTP-Server
 * ------------------------------------------------------------------ */

const server = http.createServer((req, res) => {
  const urlPath = (req.url || "/").split("?")[0];

  if (urlPath === "/api/ping") {
    return sendJson(res, 200, { ok: true, planning: true });
  }

  if (urlPath === "/api/campaigns" && req.method === "POST") {
    return handleCreateCampaign(req, res);
  }

  const slugMatch = urlPath.match(/^\/api\/campaigns\/([^/]+)$/);
  if (slugMatch) {
    const slug = decodeURIComponent(slugMatch[1]);
    if (req.method === "PUT") return handleUpdateCampaign(req, res, slug);
    if (req.method === "DELETE") return handleDeleteCampaign(res, slug);
    return sendJson(res, 405, { ok: false, errors: ["Methode nicht erlaubt."] });
  }

  if (urlPath === "/campaigns-index.json") {
    const index = buildIndex();
    writeStaticIndex(index);
    return sendJson(res, 200, index);
  }

  // Lesender Hub-Mount für Kampagnen-Inhalte (meta.json-Feld "inhalte"):
  // /hub/Outputs/... -> <HUB_DIR>/Outputs/... — nur GET, mit Traversal-Schutz.
  if (urlPath.startsWith("/hub/") && req.method === "GET") {
    const rel = decodeURIComponent(urlPath.slice("/hub/".length));
    const resolved = path.join(HUB_DIR, path.normalize(rel));
    if (!resolved.startsWith(HUB_DIR)) {
      res.writeHead(403, { "Content-Type": "text/plain; charset=utf-8" });
      res.end("403 Verboten");
      return;
    }
    return fs.readFile(resolved, (err, data) => {
      if (err) {
        res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
        res.end("404 Nicht gefunden: " + req.url);
        return;
      }
      res.writeHead(200, { "Content-Type": contentTypeFor(resolved) });
      res.end(data);
    });
  }

  const filePath = safeResolve(req.url || "/");
  if (!filePath) {
    res.writeHead(403, { "Content-Type": "text/plain; charset=utf-8" });
    res.end("403 Verboten");
    return;
  }

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
      res.end("404 Nicht gefunden: " + req.url);
      return;
    }
    res.writeHead(200, { "Content-Type": contentTypeFor(filePath) });
    res.end(data);
  });
});

server.listen(PORT, () => {
  console.log("Kampagnen-Dashboard läuft auf: http://localhost:" + PORT);
  console.log("Ausgelieferter Ordner: " + ROOT_DIR);
  console.log("Campaigns-Ordner:      " + CAMPAIGNS_DIR);
  console.log("Beenden mit Strg+C.");
});
