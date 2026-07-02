#!/usr/bin/env node
/**
 * generate-index.mjs
 *
 * Durchsucht den Campaigns/-Ordner des Kunden, liest alle Campaigns/<slug>/meta.json,
 * validiert minimal und schreibt das Ergebnis gesammelt (sortiert nach zeitraum_start,
 * absteigend) als campaigns-index.json, die die Dashboard-Weboberfläche (index.html) per
 * fetch() lädt.
 *
 * Aufruf:
 *   node generate-index.mjs [<Campaigns-Ordner>] [<Ausgabedatei>]
 *
 * Ohne Argumente:
 *   - Campaigns-Ordner: ../../../Campaigns (relativ zu diesem Skript)
 *   - Ausgabedatei:     ./campaigns-index.json (neben diesem Skript)
 *
 * Keine externen Abhängigkeiten — läuft mit jedem halbwegs aktuellen Node.js
 * ausschließlich über die eingebauten Module fs/path/url.
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const REQUIRED_FIELDS = ["thema", "kanaele", "status", "zeitraum_start"];
const VALID_STATUS = ["geplant", "in Arbeit", "veröffentlicht", "abgeschlossen"];

function resolveArgs(argv) {
  const campaignsDirArg = argv[2];
  const outputPathArg = argv[3];

  const campaignsDir = campaignsDirArg
    ? path.resolve(process.cwd(), campaignsDirArg)
    : path.resolve(__dirname, "../../../Campaigns");

  const outputPath = outputPathArg
    ? path.resolve(process.cwd(), outputPathArg)
    : path.resolve(__dirname, "campaigns-index.json");

  return { campaignsDir, outputPath };
}

function warn(message) {
  process.stderr.write("[generate-index] Warnung: " + message + "\n");
}

function validateMeta(meta, slug) {
  for (const field of REQUIRED_FIELDS) {
    if (meta[field] === undefined || meta[field] === null || meta[field] === "") {
      warn(`"${slug}/meta.json" fehlt Pflichtfeld "${field}" — wird übersprungen.`);
      return false;
    }
  }

  if (!Array.isArray(meta.kanaele)) {
    warn(`"${slug}/meta.json" hat "kanaele", das kein Array ist — wird übersprungen.`);
    return false;
  }

  if (!VALID_STATUS.includes(meta.status)) {
    warn(
      `"${slug}/meta.json" hat einen unbekannten status "${meta.status}" ` +
        `(erlaubt: ${VALID_STATUS.join(", ")}) — wird übersprungen.`
    );
    return false;
  }

  return true;
}

function readCampaigns(campaignsDir) {
  if (!fs.existsSync(campaignsDir)) {
    warn(`Campaigns-Ordner "${campaignsDir}" existiert nicht. Erzeuge leeren Index.`);
    return [];
  }

  let entries;
  try {
    entries = fs.readdirSync(campaignsDir, { withFileTypes: true });
  } catch (err) {
    warn(`Campaigns-Ordner "${campaignsDir}" konnte nicht gelesen werden: ${err.message}`);
    return [];
  }

  const campaigns = [];

  for (const entry of entries) {
    if (!entry.isDirectory()) continue;

    const slug = entry.name;
    const metaPath = path.join(campaignsDir, slug, "meta.json");

    if (!fs.existsSync(metaPath)) {
      warn(`"${slug}/" enthält keine meta.json — wird übersprungen.`);
      continue;
    }

    let raw;
    try {
      raw = fs.readFileSync(metaPath, "utf8");
    } catch (err) {
      warn(`"${slug}/meta.json" konnte nicht gelesen werden: ${err.message}`);
      continue;
    }

    let meta;
    try {
      meta = JSON.parse(raw);
    } catch (err) {
      warn(`"${slug}/meta.json" enthält kein gültiges JSON: ${err.message}`);
      continue;
    }

    if (!validateMeta(meta, slug)) {
      continue;
    }

    campaigns.push({ slug, ...meta });
  }

  campaigns.sort((a, b) => {
    if (a.zeitraum_start < b.zeitraum_start) return 1;
    if (a.zeitraum_start > b.zeitraum_start) return -1;
    return 0;
  });

  return campaigns;
}

function main() {
  const { campaignsDir, outputPath } = resolveArgs(process.argv);

  const campaigns = readCampaigns(campaignsDir);

  fs.writeFileSync(outputPath, JSON.stringify(campaigns, null, 2) + "\n", "utf8");

  process.stdout.write(
    `[generate-index] ${campaigns.length} Kampagne(n) aus "${campaignsDir}" ` +
      `nach "${outputPath}" geschrieben.\n`
  );
}

main();
