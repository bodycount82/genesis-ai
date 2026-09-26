#!/usr/bin/env node
// Genesis AI trailer renderer.
//
// Steps trailer.html frame by frame in headless Chromium (deterministic: every
// frame is renderFrame(i / fps), nothing is captured in real time), pipes the
// frames into ffmpeg, then muxes the synthesized score from music.mjs.
//
//   node render.mjs                     # 1920x1080 → out/genesis-ai-trailer-1080p.mp4
//   node render.mjs --vertical          # 1080x1920 → out/genesis-ai-trailer-vertical.mp4
//   node render.mjs --still 3,8.5,20    # PNG stills → out/stills/
//   options: --workers 3  --from 10 --to 20  --silent  --crf 18
//
// ffmpeg is taken from $FFMPEG, else from PATH.

import { chromium } from "playwright";
import { spawn, spawnSync } from "node:child_process";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");           // repo root, so the page can reach ../assets/brand
const args = process.argv.slice(2);
const flag = (name) => args.includes("--" + name);
const opt = (name, dflt) => { const i = args.indexOf("--" + name); return i >= 0 ? args[i + 1] : dflt; };

const vertical = flag("vertical");
const FPS = 30;
const DURATION = 45;
const crf = opt("crf", "18");
const workers = Math.max(1, parseInt(opt("workers", "3"), 10));
const ffmpegBin = process.env.FFMPEG || "ffmpeg";
const outDir = path.join(here, "out");
const tmpDir = path.join(here, ".render");
fs.mkdirSync(outDir, { recursive: true });
fs.mkdirSync(tmpDir, { recursive: true });

const W = vertical ? 1080 : 1920, H = vertical ? 1920 : 1080;
const outFile = path.join(outDir, opt("out", vertical ? "genesis-ai-trailer-vertical.mp4" : "genesis-ai-trailer-1080p.mp4"));

/* --- tiny static server (textures and fonts need http, not file://) --- */
const types = { ".html": "text/html", ".js": "text/javascript", ".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp", ".woff2": "font/woff2", ".css": "text/css" };
const server = http.createServer((req, res) => {
  const p = path.normalize(path.join(root, decodeURIComponent(new URL(req.url, "http://x").pathname)));
  if (!p.startsWith(root)) { res.writeHead(403); return res.end(); }
  fs.readFile(p, (err, buf) => {
    if (err) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { "content-type": types[path.extname(p)] || "application/octet-stream" });
    res.end(buf);
  });
});
await new Promise((r) => server.listen(0, "127.0.0.1", r));
const pageUrl = `http://127.0.0.1:${server.address().port}/video/trailer.html${vertical ? "?format=vertical" : ""}`;

async function openPage() {
  const browser = await chromium.launch({
    args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--disable-gpu-vsync", "--font-render-hinting=none", "--force-color-profile=srgb"],
  });
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  page.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") console.log("[page]", m.text()); });
  page.on("pageerror", (e) => console.log("[page error]", e.message));
  await page.goto(pageUrl);
  await page.evaluate(() => window.trailerReady);
  return { browser, page };
}

async function frameAt(page, t, type = "png") {
  await page.evaluate((tt) => window.renderFrame(tt), t);
  return page.screenshot({ type, clip: { x: 0, y: 0, width: W, height: H }, animations: "allow", caret: "initial" });
}

function run(cmd, argv) {
  const r = spawnSync(cmd, argv, { stdio: "inherit" });
  if (r.status !== 0) throw new Error(`${cmd} failed (${r.status})`);
}

/* --- stills --- */
if (opt("still")) {
  const dir = path.join(outDir, "stills");
  fs.mkdirSync(dir, { recursive: true });
  const { browser, page } = await openPage();
  for (const s of opt("still").split(",")) {
    const t = parseFloat(s);
    const buf = await frameAt(page, t);
    const f = path.join(dir, `${vertical ? "v" : "h"}-${t.toFixed(2)}.png`);
    fs.writeFileSync(f, buf);
    console.log(f);
  }
  await browser.close();
  server.close();
  process.exit(0);
}

/* --- frames → segments → final mp4 --- */
const from = Math.round(parseFloat(opt("from", "0")) * FPS);
const to = Math.round(parseFloat(opt("to", String(DURATION))) * FPS);
const total = to - from;
const per = Math.ceil(total / workers);
const t0 = Date.now();
let done = 0;

async function renderSegment(k) {
  const a = from + k * per, b = Math.min(to, a + per);
  if (a >= b) return null;
  const seg = path.join(tmpDir, `${vertical ? "v" : "h"}-seg-${k}.mkv`);
  const ff = spawn(ffmpegBin, ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "png", "-i", "-",
    "-vf", "scale=out_color_matrix=bt709:out_range=tv", "-c:v", "libx264", "-preset", "veryfast", "-crf", "8", "-pix_fmt", "yuv444p",
    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", seg], { stdio: ["pipe", "inherit", "inherit"] });
  const closed = new Promise((res, rej) => ff.on("close", (c) => (c === 0 ? res() : rej(new Error("ffmpeg segment " + k + " failed")))));
  const { browser, page } = await openPage();
  for (let i = a; i < b; i++) {
    const buf = await frameAt(page, i / FPS);
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
    done++;
    if (done % 30 === 0) {
      const el = (Date.now() - t0) / 1000;
      process.stdout.write(`\r${done}/${total} frames · ${(el / done * 1000).toFixed(0)} ms/frame · eta ${((total - done) * el / done / 60).toFixed(1)} min   `);
    }
  }
  ff.stdin.end();
  await closed;
  await browser.close();
  return seg;
}

const segs = (await Promise.all(Array.from({ length: workers }, (_, k) => renderSegment(k)))).filter(Boolean);
server.close();
console.log(`\nframes done in ${((Date.now() - t0) / 60000).toFixed(1)} min`);

const list = path.join(tmpDir, "segments.txt");
fs.writeFileSync(list, segs.map((s) => `file '${s.replace(/'/g, "'\\''")}'`).join("\n"));

const music = path.join(here, "out", "genesis-ai-score.wav");
const withAudio = !flag("silent") && fs.existsSync(music);
if (!flag("silent") && !withAudio) console.log("no out/genesis-ai-score.wav — run `node music.mjs` first; exporting silent");

const enc = ["-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", list];
if (withAudio) enc.push("-ss", String(from / FPS), "-i", music);
enc.push("-map", "0:v:0");
if (withAudio) enc.push("-map", "1:a:0", "-c:a", "aac", "-b:a", "192k", "-shortest");
enc.push("-c:v", "libx264", "-preset", "slow", "-crf", crf, "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", vertical ? "4.2" : "4.1",
  "-r", String(FPS), "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart", outFile);
run(ffmpegBin, enc);
segs.forEach((s) => fs.rmSync(s, { force: true }));
const mb = fs.statSync(outFile).size / 1048576;
console.log(`${outFile} · ${mb.toFixed(1)} MB${mb > 90 ? "  (!) over 90 MB — raise --crf" : ""}`);
