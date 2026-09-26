# Genesis AI — cinematic trailer

A 45-second, 1920×1080 / 30 fps trailer for YouTube, plus a 1080×1920 vertical cut for Shorts.
Everything is generated from source in this folder: a three.js scene and HTML titles, rendered
frame by frame in headless Chromium and encoded with ffmpeg. Nothing is screen-recorded, so every
render is identical.

| File | What it is |
| --- | --- |
| `out/genesis-ai-trailer-1080p.mp4` | Main trailer, H.264 High, yuv420p, CRF 18, AAC 192k |
| `out/genesis-ai-trailer-vertical.mp4` | Shorts cut, 1080×1920, same timeline |
| `out/genesis-ai-score.wav` | The music on its own (synthesized, see below) |
| `trailer.html` | The whole film: planet, camera moves, titles, showcase, end card |
| `render.mjs` | Frame-stepping renderer → ffmpeg |
| `music.mjs` | Synthesizes the score |
| `shots/` | App screenshots used in the showcase (swap these) |
| `vendor/` | three.js r160, NASA Blue/Black Marble textures (from three-globe), OFL fonts |

## Timeline

| Time | Shot |
| --- | --- |
| 0–6 s | Black → the planet's night side fades in; the camera pushes in and the sun breaks the limb |
| 6–11 s | The Genesis AI glyph and wordmark resolve over the horizon: *Most AIs store. Genesis remembers.* |
| 11–30 s | One continuous orbit under five lines (≈3.8 s each): Local & private · Memory (a gold wave spreads from the Slovenia origin) · Missions · Work · Autonomy (arcs to the world) · Browser Bridge · Android |
| 30–38 s | Showcase: desktop window and two phones, slow parallax — *It's already awake.* |
| 38–45 s | End card over a new sunrise: Genesis AI · Free download · Windows · Android · Browser Bridge · https://bodycount82.github.io/genesis-ai/ |

All wording comes from the site (`index`, `local-private`, `memory`, `modes`, `desktop-control`).
Colours are the palette in `assets/style.css` (void black, ivory, gold); the logo is
`assets/brand/icon-512.png` with its purple tile keyed out at render time.

## Render

Needs Node 18+ and ffmpeg (with libx264) on `PATH`, or pointed to with `FFMPEG=/path/to/ffmpeg`.

```bash
cd video
npm install                 # installs Playwright
npx playwright install chromium   # once, if you don't already have Playwright's Chromium

npm run render              # score + 1080p   → out/genesis-ai-trailer-1080p.mp4
npm run render:vertical     # score + Shorts  → out/genesis-ai-trailer-vertical.mp4
```

Which is the same as `node music.mjs && node render.mjs [--vertical]`. Rendering uses software
WebGL (SwiftShader), so it takes a while — about 10–20 min for the full film on a 4-core machine.
Useful options:

```bash
node render.mjs --still 3,8.5,20      # PNG stills into out/stills/ (fast way to check a change)
node render.mjs --workers 4           # parallel browser workers (default 3)
node render.mjs --from 30 --to 38     # render only part of the timeline
node render.mjs --silent              # no music track
node render.mjs --crf 20              # smaller file (keep MP4s under GitHub's 100 MB limit)
```

To look at it interactively, serve the repo root (`npx serve ..` from `video/`) and open
`/video/trailer.html?play` (real-time loop), `?t=21.5` (one frame) or add `&format=vertical`.

## Swapping in new screenshots

The showcase (30–38 s) loads three files from `shots/`:

| File | Frame | Best size |
| --- | --- | --- |
| `shots/desktop-1.png` | Desktop window (front, left) | 16:10 or 16:9, e.g. 1600×960 or larger |
| `shots/phone-1.png` | Front phone | 9:19.5 portrait, e.g. 720×1560 |
| `shots/phone-2.png` | Rear phone | same as phone-1 |

They currently hold the real screens from `assets/showcase/` (desktop chat, Android chat, Android
calendar). Replace any of them with a new PNG of the same name, then run `npm run render` again.
Images are scaled to cover the frame and anchored to the top, so a screenshot with a different
aspect ratio is cropped at the bottom rather than distorted. A missing file just shows an empty
dark frame.

To change the words, edit the `.beat`, `#logo`, `#showcase` and `#end` blocks in `trailer.html`;
the timing for each block is in `renderFrame()` in the same file.

## Music

`music.mjs` synthesizes the score from sine oscillators (a detuned pad in D, a bell arpeggio with one
chord per feature beat, noise risers and sub "blooms" on the cuts, a Schroeder reverb), mastered to
about −14 LUFS. It uses no samples or third-party audio, so it is free to use on YouTube with no
Content ID claims. To publish without it, render with `--silent` and add music in YouTube Studio.
