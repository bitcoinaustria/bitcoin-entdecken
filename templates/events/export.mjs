import { spawnSync } from "node:child_process";
import fs from "node:fs/promises";
import { statSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { PNG } from "pngjs";
import QRCode from "qrcode";
import { chromium } from "playwright";

const root = path.dirname(fileURLToPath(import.meta.url));
const src = path.join(root, "src");
const eventsDir = path.join(src, "events");
const layoutsDir = path.join(src, "layouts");
const exportsDir = path.join(root, "exports");
const sizes = {
  a3: ["841.92pt", "1191.12pt"],
  a5: ["420pt", "594.96pt"],
  bauzaun: ["3400mm", "1650mm"],
};
const minimumRasterPpi = { a3: 100, a5: 300, bauzaun: 20 };

function fail(message) {
  throw new Error(message);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function formatTime(value, eventId) {
  const match = value.match(/^([01]\d|2[0-3]):([0-5]\d)$/);
  if (!match) fail(`${eventId}: Uhrzeit muss HH:MM sein`);
  const hour = String(Number(match[1]));
  return match[2] === "00" ? hour : `${hour}:${match[2]}`;
}

function computedEvent(event) {
  const result = { ...event };
  if (event.date) {
    const [, year, month, day] = event.date.match(/^(\d{4})-(\d{2})-(\d{2})$/) || [];
    if (!day) fail(`${event.id}: date muss YYYY-MM-DD sein`);
    result.dateShort = `${day}.${month}.`;
    if (result.dateShort.includes(year)) fail(`${event.id}: Kurzdatum enthält fälschlich das Jahr`);
  }
  if (event.start || event.end) {
    if (!event.start || !event.end) fail(`${event.id}: Start- und Endzeit müssen gemeinsam gesetzt sein`);
    result.timeRange = `${formatTime(event.start, event.id)}–${formatTime(event.end, event.id)} Uhr`;
  }
  result.dateAndTime = result.dateShort && result.timeRange
    ? `${result.dateShort} // ${result.timeRange}`
    : "";
  result.postalCity = [event.postalCode, event.city].filter(Boolean).join(" ");
  result.venueAndCity = [event.venue, event.city].filter(Boolean).join(" · ");
  return result;
}

function resolveTemplateValue(object, key) {
  return key.split(".").reduce((value, part) => value?.[part], object);
}

function fillTemplate(template, values, sourceName) {
  return template.replace(/{{\s*([\w.]+)\s*}}/g, (_, key) => {
    const value = resolveTemplateValue(values, key);
    if (value === undefined || value === null || value === "") {
      fail(`${sourceName}: Wert für {{${key}}} fehlt`);
    }
    return key === "qrDataUrl" || key === "baseUrl" ? String(value) : escapeHtml(value);
  });
}

async function readEvents() {
  const names = (await fs.readdir(eventsDir)).filter((name) => name.endsWith(".json") && !name.endsWith(".entwurf.json"));
  const events = [];
  for (const name of names) {
    const event = JSON.parse(await fs.readFile(path.join(eventsDir, name), "utf8"));
    if (!event.id || !Array.isArray(event.outputs)) fail(`${name}: id oder outputs fehlt`);
    for (const output of event.outputs) {
      if (!output.file || output.file !== path.basename(output.file)) fail(`${name}: unsicherer Ausgabename`);
      if (!output.from && (!output.layout || !Array.isArray(output.pages))) fail(`${name}: Layout oder Seiten fehlen`);
      if (output.size && !sizes[output.size]) fail(`${name}: unbekannte Größe ${output.size}`);
    }
    events.push(computedEvent(event));
  }
  return events;
}

async function renderSource(event, output) {
  const file = path.join(layoutsDir, output.layout);
  const template = await fs.readFile(file, "utf8");
  const qrSvg = await QRCode.toString(event.registrationUrl, { type: "svg", margin: 1, errorCorrectionLevel: "M" });
  const qrDataUrl = `data:image/svg+xml;base64,${Buffer.from(qrSvg).toString("base64")}`;
  return fillTemplate(template, {
    event,
    qrDataUrl,
    baseUrl: pathToFileURL(`${layoutsDir}${path.sep}`).href,
  }, output.layout);
}

function browserPath() {
  const candidates = [
    process.env.BROWSER_PATH,
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  ].filter(Boolean);
  return candidates.find((candidate) => requireFile(candidate));
}

function requireFile(file) {
  try {
    return Boolean(file && statSync(file).isFile());
  } catch {
    return false;
  }
}

async function preparePage(browser, event, output) {
  const temporaryDirectory = await fs.mkdtemp(path.join(os.tmpdir(), "bitcoin-entdecken-event-"));
  const temporaryHtml = path.join(temporaryDirectory, "render.html");
  await fs.writeFile(temporaryHtml, await renderSource(event, output));
  const page = await browser.newPage({ viewport: { width: 1400, height: 1800 } });
  await page.goto(pathToFileURL(temporaryHtml).href, { waitUntil: "networkidle" });
  const geometry = await page.evaluate(async (ids) => {
    document.querySelectorAll(".page").forEach((element) => {
      if (!ids.includes(element.dataset.layout)) element.remove();
    });
    await document.fonts.ready;
    if (!document.fonts.check("16px Poppins")) throw new Error("Poppins wurde nicht geladen");
    return [...document.querySelectorAll(".page")].map((element) => ({
      ...element.getBoundingClientRect().toJSON(),
      backgroundColor: getComputedStyle(element).backgroundColor,
    }));
  }, output.pages);
  if (geometry.length !== output.pages.length || geometry.some(({ width, height }) => !width || !height)) {
    fail(`${output.layout}: ausgewählte Seiten haben keine gültige Geometrie`);
  }
  return { page, temporaryDirectory, backgrounds: geometry.map(({ backgroundColor }) => backgroundColor) };
}

function runCheckedCommand(command, args, errorHint) {
  const result = spawnSync(command, args, { encoding: "utf8" });
  if (result.status !== 0) fail(`${errorHint}\n${result.stderr || result.stdout}`);
  return result.stdout;
}

async function checkFullBleed(pdf, scratch, backgrounds, dpi = "150") {
  runCheckedCommand("pdftoppm", ["-f", "1", "-l", String(backgrounds.length), "-png", "-r", dpi, pdf, scratch], "Poppler (pdftoppm) fehlt oder konnte das PDF nicht prüfen");
  const files = backgrounds.map((_, index) => `${scratch}-${index + 1}.png`);
  let issue;
  try {
    for (const [index, file] of files.entries()) {
      if (backgrounds[index] === "rgb(255, 255, 255)") continue;
      const png = PNG.sync.read(await fs.readFile(file));
      let white = 0;
      const isWhite = (offset) => png.data[offset] > 245 && png.data[offset + 1] > 245 && png.data[offset + 2] > 245;
      for (let x = 0; x < png.width; x += 1) {
        if (isWhite(x * 4)) white += 1;
        if (isWhite(((png.height - 1) * png.width + x) * 4)) white += 1;
      }
      for (let y = 0; y < png.height; y += 1) {
        if (isWhite((y * png.width) * 4)) white += 1;
        if (isWhite((y * png.width + png.width - 1) * 4)) white += 1;
      }
      if (white) issue = `${path.basename(pdf)}, Seite ${index + 1}: ${white} weiße Pixel am Außenrand`;
    }
  } finally {
    await Promise.all(files.map((file) => fs.rm(file, { force: true })));
  }
  if (issue) fail(issue);
}

function checkRasterResolution(pdf, minimumPpi) {
  const rows = runCheckedCommand("pdfimages", ["-list", pdf], "Poppler (pdfimages) fehlt oder konnte das PDF nicht prüfen")
    .split("\n")
    .map((line) => line.trim().split(/\s+/))
    .filter((columns) => columns[2] === "image");
  const low = rows.filter((columns) => Number(columns[12]) < minimumPpi || Number(columns[13]) < minimumPpi);
  if (low.length) fail(`${path.basename(pdf)}: Rasterbild unter ${minimumPpi} PPI (${low.map((columns) => `${columns[12]}×${columns[13]}`).join(", ")})`);
}

async function exportEvent(browser, event) {
  const target = path.join(exportsDir, event.id);
  const scratch = path.join(target, ".qa");
  await fs.mkdir(target, { recursive: true });
  const expectedFiles = new Set(event.outputs.map(({ file }) => file));
  for (const entry of await fs.readdir(target, { withFileTypes: true })) {
    if (entry.isFile() && !expectedFiles.has(entry.name)) await fs.rm(path.join(target, entry.name));
  }
  for (const output of event.outputs) {
    const destination = path.join(target, output.file);
    if (output.type === "png300") {
      const sourcePdf = path.join(target, output.from);
      const prefix = destination.replace(/\.png$/i, "");
      runCheckedCommand("pdftoppm", ["-png", "-r", "300", "-singlefile", sourcePdf, prefix], "Poppler (pdftoppm) fehlt oder konnte das PNG nicht erzeugen");
      continue;
    }
    const { page, temporaryDirectory, backgrounds } = await preparePage(browser, event, output);
    if (output.type === "jpeg") {
      const design = page.locator(`[data-layout="${output.pages[0]}"]`);
      await design.screenshot({ path: destination, type: "jpeg", quality: 96 });
    } else if (output.type === "pdf") {
      const [width, height] = sizes[output.size];
      await page.addStyleTag({ content: `@page { size: ${width} ${height}; margin: 0; }` });
      await page.emulateMedia({ media: "print" });
      await page.pdf({ path: destination, printBackground: true, preferCSSPageSize: true, margin: { top: "0", right: "0", bottom: "0", left: "0" } });
      const info = runCheckedCommand("pdfinfo", [destination], "Poppler (pdfinfo) fehlt oder konnte das PDF nicht prüfen");
      if (!info.includes(`Pages:           ${output.pages.length}`)) fail(`${output.file}: falsche Seitenzahl`);
      await checkFullBleed(destination, scratch, backgrounds, output.size === "bauzaun" ? "10" : "150");
      checkRasterResolution(destination, minimumRasterPpi[output.size]);
    } else {
      fail(`${event.id}: unbekannter Ausgabetyp ${output.type}`);
    }
    await page.close();
    await fs.rm(temporaryDirectory, { recursive: true });
  }
}

const events = await readEvents();
if (process.argv.includes("--check")) {
  if (computedEvent({ id: "Zeitprüfung", start: "17:30", end: "19:45" }).timeRange !== "17:30–19:45 Uhr") fail("Interne Zeitformatierung ist fehlerhaft");
  for (const event of events) {
    for (const output of event.outputs.filter((item) => item.layout)) {
      await renderSource(event, output);
    }
  }
  console.log(`${events.length} Eventdatensätze und ${events.flatMap((event) => event.outputs).length} Ausgaben geprüft.`);
  process.exit(0);
}

const requested = process.argv.slice(2).find((argument) => argument !== "--");
if (!requested) fail(`Event-ID fehlt. Verfügbar: ${events.map((event) => event.id).join(", ")}`);
const selected = requested === "--all" ? events : events.filter((event) => event.id === requested);
if (!selected.length) fail(`Unbekannte Event-ID: ${requested}`);
const executablePath = browserPath();
const browser = await chromium.launch({ headless: true, ...(executablePath ? { executablePath } : {}) });
try {
  for (const event of selected) await exportEvent(browser, event);
} finally {
  await browser.close();
}
