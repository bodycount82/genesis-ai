#!/usr/bin/env node
// Genesis AI — extended-cut score ("vastness"). Synthesized from scratch: no samples, no third-party
// audio, free to use. Writes out/genesis-ai-score-extended.wav (48 kHz stereo, 16-bit, 98 s).
//
// Cue sheet (extended-cut seconds):
//   0–13    a sub drone and a quiet organ out of silence; a swell and a deep bloom as the sun breaks (6.5)
//   13–67   five feature lines, 10.8 s each: organ progression i–VI–III–VII–(iv–V) in D minor over a
//           clock-like bell pulse (0.9 s); strings enter on line 2, a heartbeat on line 3, and it all
//           builds through line 5 into a timpani roll
//   67–82   the showcase: the peak — full organ, strings, double-time pulse — then easing off
//   82–98   the end card: resolve to D major, bells, a long tail into silence

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const SR = 48000, DUR = 98, N = SR * DUR;
const dryL = new Float32Array(N), dryR = new Float32Array(N);      // little or no reverb
const wetL = new Float32Array(N), wetR = new Float32Array(N);      // reverb send
const strL = new Float32Array(N), strR = new Float32Array(N);      // strings bus (filtered, then sent)

/* ---- helpers ---- */
let seed = 20260926;
const rand = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
const clamp01 = (x) => (x < 0 ? 0 : x > 1 ? 1 : x);
const smooth = (x) => { x = clamp01(x); return x * x * (3 - 2 * x); };
const ramp = (t, a, b) => clamp01((t - a) / (b - a));
const TABLE = 8192, SINE = new Float32Array(TABLE + 1);
for (let i = 0; i <= TABLE; i++) SINE[i] = Math.sin((i / TABLE) * Math.PI * 2);
const sin = (ph) => { const x = (ph - Math.floor(ph)) * TABLE, i = x | 0; return SINE[i] + (SINE[i + 1] - SINE[i]) * (x - i); };
const NOTE = { C: 0, "C#": 1, Db: 1, D: 2, "D#": 3, Eb: 3, E: 4, F: 5, "F#": 6, Gb: 6, G: 7, "G#": 8, Ab: 8, A: 9, "A#": 10, Bb: 10, B: 11 };
const hz = (s) => { const m = s.match(/^([A-G][#b]?)(-?\d)$/); return 440 * Math.pow(2, (12 * (parseInt(m[2], 10) + 1) + NOTE[m[1]] - 69) / 12); };
const panG = (p) => [Math.cos(p * Math.PI / 2), Math.sin(p * Math.PI / 2)];

/* ---- the intensity curve everything follows ---- */
const KEYS = [[0, 0.12], [6.0, 0.3], [9, 0.34], [13, 0.3], [23.8, 0.4], [34.6, 0.5], [45.4, 0.62], [56.2, 0.76], [64.5, 0.92], [67, 1.0], [75, 1.0], [80.5, 0.72], [82, 0.62], [92, 0.55], [98, 0.4]];
function intensity(t) {
  for (let i = 1; i < KEYS.length; i++) if (t <= KEYS[i][0]) { const a = KEYS[i - 1], b = KEYS[i]; return a[1] + (b[1] - a[1]) * smooth((t - a[0]) / (b[0] - a[0])); }
  return KEYS[KEYS.length - 1][1];
}
const master = (t) => smooth(ramp(t, 0, 2.5)) * (1 - smooth(ramp(t, 93.5, 98)));
// per-sample lookups (every oscillator reads these)
const IA = new Float32Array(N), MA = new Float32Array(N);
for (let i = 0; i < N; i++) { IA[i] = intensity(i / SR); MA[i] = master(i / SR); }

/* ---- sections / harmony ---- */
const CH = [
  // start, end, organ voicing, string voicing, pulse figure (bells, octave 4–6)
  [0, 13.6, ["D2", "A2", "D3", "F3", "A3", "E4"], [], []],
  [13, 24.4, ["D2", "A2", "D3", "F3", "A3", "D4"], ["D3", "A3", "F4"], ["A4", "D5", "F5", "E5", "D5", "A4", "D5", "F5", "A5", "F5", "E5", "D5"]],
  [23.8, 35.2, ["Bb1", "F2", "D3", "F3", "A3", "D4"], ["D3", "F3", "Bb3", "D4"], ["F4", "Bb4", "D5", "C5", "Bb4", "F4", "Bb4", "D5", "F5", "D5", "C5", "A4"]],
  [34.6, 46.0, ["F1", "C2", "A2", "C3", "E3", "A3", "C4"], ["C3", "A3", "C4", "E4"], ["A4", "C5", "E5", "F5", "E5", "C5", "A4", "C5", "E5", "G5", "E5", "C5"]],
  [45.4, 56.8, ["C2", "G2", "E3", "G3", "D4", "E4"], ["E3", "G3", "C4", "E4", "G4"], ["G4", "C5", "D5", "E5", "G5", "E5", "D5", "C5", "E5", "G5", "C6", "G5"]],
  [56.2, 62.2, ["G1", "D2", "Bb2", "D3", "G3", "Bb3", "D4"], ["D3", "G3", "Bb3", "D4", "G4"], ["G4", "Bb4", "D5", "G5", "D5", "Bb4"]],
  [61.6, 64.9, ["A1", "E2", "A2", "D3", "E3", "A3", "D4"], ["E3", "A3", "D4", "E4", "A4"], ["A4", "D5", "E5", "A5"]],
  [64.3, 67.8, ["A1", "E2", "A2", "C#3", "E3", "A3", "C#4", "E4"], ["E3", "A3", "C#4", "E4", "A4"], ["A4", "C#5", "E5"]],
  [67, 75.2, ["D1", "D2", "A2", "D3", "F3", "A3", "D4", "F4"], ["D3", "A3", "D4", "F4", "A4", "D5"], ["D5", "F5", "A5", "D6", "A5", "F5", "E5", "F5", "A5", "D6", "E6", "D6"]],
  [74.5, 82.8, ["Bb0", "Bb1", "F2", "D3", "F3", "Bb3", "D4", "F4"], ["D3", "F3", "Bb3", "D4", "F4", "Bb4"], ["F5", "Bb5", "D6", "C6", "Bb5", "F5", "D5", "F5", "Bb5", "C6", "D6", "F6"]],
  [82, 98, ["D1", "D2", "A2", "D3", "F#3", "A3", "E4", "F#4"], ["D3", "A3", "D4", "F#4", "A4"], []],
];

/* ---- organ: additive drawbars (16', 8', 4', 2 2/3', 2', 1 3/5', 1 1/3', 1') ---- */
const DRAW = [[0.5, 0.55], [1, 1.0], [2, 0.62], [3, 0.3], [4, 0.36], [5, 0.12], [6, 0.14], [8, 0.16]];
function organ(a, b, notes, fadeIn, fadeOut) {
  const s0 = Math.max(0, Math.floor(a * SR)), s1 = Math.min(N, Math.ceil((b + fadeOut) * SR));
  for (const name of notes) {
    const f0 = hz(name);
    const pan = 0.5 + (rand() - 0.5) * 0.5;
    const [gl, gr] = panG(pan);
    for (const [mult, amp0] of DRAW) {
      const f = f0 * mult;
      if (f < 26 || f > 6000) continue;
      const bright = mult <= 2;                  // upper drawbars open with intensity
      for (const det of [-1.2, 1.2]) {           // gentle celeste
        let ph = rand();
        const inc = f * Math.pow(2, det / 1200) / SR;
        const trem = 4.8 + rand() * 0.8, tremP = rand();
        for (let i = s0; i < s1; i++) {
          const t = i / SR;
          const env = smooth((t - a) / fadeIn) * (1 - smooth((t - b) / fadeOut));
          if (env <= 0) { ph += inc; continue; }
          const I = IA[i];
          const g = amp0 * (bright ? 1 : 0.25 + 0.95 * I) * (f0 < 70 ? 1.1 : 1) * 0.02 * (0.55 + 0.6 * I);
          const v = sin(ph) * g * env * (1 + 0.012 * sin(tremP + t * trem)) * MA[i];
          wetL[i] += v * gl * 0.9; wetR[i] += v * gr * 0.9;
          dryL[i] += v * gl * 0.35; dryR[i] += v * gr * 0.35;
          ph += inc;
        }
      }
    }
  }
}

/* ---- strings: band-limited saw ensemble into a filtered bus ---- */
function blep(t, dt) {
  if (t < dt) { t /= dt; return t + t - t * t - 1; }
  if (t > 1 - dt) { t = (t - 1) / dt; return t * t + t + t + 1; }
  return 0;
}
function strings(a, b, notes, fadeIn, fadeOut, level) {
  const s0 = Math.max(0, Math.floor(a * SR)), s1 = Math.min(N, Math.ceil((b + fadeOut) * SR));
  for (const name of notes) {
    const f0 = hz(name);
    for (let v = 0; v < 5; v++) {
      const cents = (v - 2) * 5 + (rand() - 0.5) * 3;
      const [gl, gr] = panG(0.12 + 0.76 * (v / 4) + (rand() - 0.5) * 0.1);
      let ph = rand();
      const vibF = 4.6 + rand() * 0.9, vibP = rand();
      for (let i = s0; i < s1; i++) {
        const t = i / SR;
        const env = smooth((t - a) / fadeIn) * (1 - smooth((t - b) / fadeOut));
        const vib = 1 + 0.0022 * sin(vibP + t * vibF) * smooth((t - a) / 2);
        const inc = f0 * Math.pow(2, cents / 1200) * vib / SR;
        if (env > 0) {
          const saw = 2 * ph - 1 - blep(ph, inc);
          const I = IA[i];
          const g = 0.0075 * level * env * (0.2 + 0.8 * I) * MA[i];
          strL[i] += saw * g * gl; strR[i] += saw * g * gr;
        }
        ph += inc; if (ph >= 1) ph -= 1;
      }
    }
  }
}

/* ---- bells for the pulse (soft mallet: fundamental + inharmonic partials) ---- */
function bell(t0, f, gain, pan, decay = 2.4) {
  const s0 = Math.floor(t0 * SR), s1 = Math.min(N, s0 + Math.floor(decay * 3 * SR));
  const [gl, gr] = panG(pan);
  const P = [[1, 1, decay], [2.0, 0.22, decay * 0.4], [2.76, 0.08, decay * 0.22], [5.4, 0.035, decay * 0.1]];
  for (let i = s0; i < s1; i++) {
    const t = (i - s0) / SR;
    let v = 0;
    for (const [m, a, d] of P) v += sin(f * m * t) * a * Math.exp(-t / d);
    v *= (1 - Math.exp(-t / 0.004)) * gain * MA[i];
    dryL[i] += v * gl * 0.55; dryR[i] += v * gr * 0.55;
    wetL[i] += v * gl * 0.7; wetR[i] += v * gr * 0.7;
  }
}

/* ---- percussion and swells ---- */
function thump(t0, gain, f1 = 62, f2 = 42, decay = 0.45) {
  const s0 = Math.floor(t0 * SR), s1 = Math.min(N, s0 + Math.floor(decay * 6 * SR));
  let ph = 0, lp = 0, lp2 = 0;
  for (let i = s0; i < s1; i++) {
    const t = (i - s0) / SR;
    ph += (f2 + (f1 - f2) * Math.exp(-t / 0.06)) / SR;
    lp += 0.03 * ((rand() * 2 - 1) - lp); lp2 += 0.03 * (lp - lp2);
    const v = (sin(ph) * Math.exp(-t / decay) + lp2 * 1.2 * Math.exp(-t / 0.03)) * gain * (1 - Math.exp(-t / 0.006));
    dryL[i] += v; dryR[i] += v; wetL[i] += v * 0.35; wetR[i] += v * 0.35;
  }
}
function boom(t0, gain) {
  thump(t0, gain, 70, 31, 2.6);
  // a low rumble of filtered noise under it
  const s0 = Math.floor(t0 * SR), s1 = Math.min(N, s0 + Math.floor(5 * SR));
  let a = 0, b = 0;
  for (let i = s0; i < s1; i++) {
    const t = (i - s0) / SR;
    a += 0.012 * ((rand() * 2 - 1) - a); b += 0.012 * (a - b);
    const v = b * 4.5 * gain * Math.exp(-t / 1.6) * (1 - Math.exp(-t / 0.01));
    dryL[i] += v; dryR[i] += v * 0.96; wetL[i] += v * 0.6; wetR[i] += v * 0.6;
  }
}
function swell(tEnd, len, gain) {                // reverse-cymbal style airy rise into a hit
  let lp = 0, lp2 = 0, lq = 0, lq2 = 0;
  const s0 = Math.max(0, Math.floor((tEnd - len) * SR)), s1 = Math.floor(tEnd * SR);
  for (let i = s0; i < s1; i++) {
    const u = (i - s0) / (s1 - s0);
    const c = 1 - Math.exp(-2 * Math.PI * (300 + 6500 * u * u) / SR);
    lp += c * ((rand() * 2 - 1) - lp); lp2 += c * (lp - lp2);
    lq += c * ((rand() * 2 - 1) - lq); lq2 += c * (lq - lq2);
    const env = Math.pow(u, 3) * gain * (1 - smooth((u - 0.985) / 0.015));
    wetL[i] += lp2 * env; wetR[i] += lq2 * env;
    dryL[i] += lp2 * env * 0.3; dryR[i] += lq2 * env * 0.3;
  }
}
function drone(a, b) {                            // the floor of space: D1 + D2 with a slow breath
  const s0 = Math.floor(a * SR), s1 = Math.min(N, Math.floor(b * SR));
  let p1 = 0, p2 = 0, p3 = 0;
  for (let i = s0; i < s1; i++) {
    const t = i / SR;
    const env = smooth((t - a) / 6) * (1 - smooth((t - (b - 8)) / 8));
    const breath = 0.82 + 0.18 * sin(t * 0.07);
    const I = IA[i];
    const v = (sin(p1) * 0.9 + sin(p2) * 0.35 + sin(p3) * 0.12) * env * breath * (0.05 + 0.05 * I) * MA[i];
    dryL[i] += v; dryR[i] += v; wetL[i] += v * 0.25; wetR[i] += v * 0.25;
    p1 += hz("D1") / SR; p2 += hz("D2") * 1.0008 / SR; p3 += hz("A2") / SR;
  }
}
function shimmer(a, b, notes, gain) {             // faint high partials that drift in and out — distance
  for (const name of notes) {
    const f = hz(name), [gl, gr] = panG(0.2 + rand() * 0.6), lfo = 0.03 + rand() * 0.05, lp = rand();
    const s0 = Math.floor(a * SR), s1 = Math.min(N, Math.floor(b * SR));
    for (let i = s0; i < s1; i++) {
      const t = i / SR;
      const env = smooth((t - a) / 5) * (1 - smooth((t - (b - 5)) / 5)) * Math.pow(0.5 + 0.5 * sin(lp + t * lfo), 2);
      const v = sin(f * t) * env * gain * MA[i];
      wetL[i] += v * gl; wetR[i] += v * gr;
    }
  }
}

/* ---- the score ---- */
drone(0, 98);
shimmer(0, 30, ["A5", "D6", "E6"], 0.006);
shimmer(80, 98, ["F#5", "A5", "E6"], 0.007);

CH.forEach(([a, b, org, str], k) => {
  const fadeIn = k === 0 ? 5.5 : 1.4, fadeOut = k === CH.length - 1 ? 1 : 1.8;
  organ(a, b, org, fadeIn, fadeOut);
  if (str.length) strings(a + (k === 1 ? 2 : 0), b, str, k === 1 ? 5 : 1.6, fadeOut, k === 1 ? 0.35 : k === 2 ? 0.7 : 1.0);
});

// the pulse: 0.9 s grid from 13 s; double time at the peak; none under the end card
const PULSE = 0.9;
CH.forEach(([a, b, , , fig], k) => {
  if (!fig.length) return;
  const peak = a >= 67 && a < 82;
  const step = peak ? PULSE / 2 : PULSE;
  const start = k === 1 ? 13 : a;
  const end = Math.min(k + 1 < CH.length ? CH[k + 1][0] : b, 81.2);
  for (let t = start, j = 0; t < end - 0.01; t += step, j++) {
    const I = intensity(t);
    const accent = j % (peak ? 8 : 4) === 0 ? 1 : 0.72;
    const g = 0.085 * (0.45 + 0.75 * I) * accent * (peak ? 0.8 : 1) * (1 - smooth(ramp(t, 79, 81.2)));
    bell(t, hz(fig[j % fig.length]), g, 0.3 + 0.4 * ((j * 5) % 8) / 7, peak ? 1.4 : 2.4);
  }
});

// heartbeat from line 3, quickening at the end of line 5, then a roll into the peak
for (let t = 34.6; t < 63.4; t += 1.8) thump(t, 0.07 + 0.16 * ramp(t, 34.6, 63), 58, 40, 0.5), thump(t + 0.32, (0.04 + 0.1 * ramp(t, 34.6, 63)), 55, 40, 0.4);
{
  let t = 63.5, gap = 0.42;
  while (t < 66.9) { thump(t, 0.1 + 0.2 * ramp(t, 63.5, 66.9), 80, 55, 0.3); t += gap; gap = Math.max(0.085, gap * 0.9); }
}
for (let t = 67; t < 79; t += 1.8) thump(t, 0.2, 60, 40, 0.55);

// hits
swell(6.5, 4.0, 0.12); boom(6.5, 0.5);
boom(13, 0.2);
swell(67, 4.5, 0.16); boom(67, 0.85);
boom(74.5, 0.4);
swell(82, 3.0, 0.08); boom(82, 0.38);

// end card: the answer, in bells
[[83.2, "A4"], [84.6, "D5"], [86.2, "F#5"], [88.0, "A5"], [90.5, "E5"], [92.6, "D5"]].forEach(([t, n], i) => bell(t, hz(n), 0.11, 0.3 + 0.08 * i, 3.2));

/* ---- strings bus: time-varying low-pass (opens with intensity), then into the mix ---- */
{
  let l1 = 0, l2 = 0, r1 = 0, r2 = 0;
  for (let i = 0; i < N; i++) {
    const t = i / SR;
    const cut = 500 + 3800 * Math.pow(IA[i], 1.4);
    const c = 1 - Math.exp(-2 * Math.PI * cut / SR);
    l1 += c * (strL[i] - l1); l2 += c * (l1 - l2);
    r1 += c * (strR[i] - r1); r2 += c * (r1 - r2);
    dryL[i] += l2 * 0.5; dryR[i] += r2 * 0.5;
    wetL[i] += l2 * 0.8; wetR[i] += r2 * 0.8;
  }
}

/* ---- hall: 8-line feedback delay network, RT60 ≈ 6 s, damped highs, 45 ms pre-delay ---- */
function hall(inL, inR, rt60) {
  const lens = [1733, 2111, 2539, 2917, 3389, 3761, 4217, 4643].map((d) => Math.round(d * SR / 44100));
  const bufs = lens.map((d) => new Float32Array(d)), idx = new Array(8).fill(0);
  const gains = lens.map((d) => Math.pow(10, -3 * d / (rt60 * SR)));
  const damp = new Float32Array(8);
  const pre = Math.round(0.045 * SR);
  const outL = new Float32Array(N), outR = new Float32Array(N);
  const y = new Float32Array(8);
  for (let i = 0; i < N; i++) {
    const xl = i >= pre ? inL[i - pre] : 0, xr = i >= pre ? inR[i - pre] : 0;
    for (let k = 0; k < 8; k++) {
      const v = bufs[k][idx[k]];
      damp[k] = v * 0.62 + damp[k] * 0.38;       // absorb highs each pass
      y[k] = damp[k];
    }
    // 8x8 Hadamard mix (normalised)
    const a0 = y[0] + y[1], a1 = y[0] - y[1], a2 = y[2] + y[3], a3 = y[2] - y[3], a4 = y[4] + y[5], a5 = y[4] - y[5], a6 = y[6] + y[7], a7 = y[6] - y[7];
    const b0 = a0 + a2, b1 = a1 + a3, b2 = a0 - a2, b3 = a1 - a3, b4 = a4 + a6, b5 = a5 + a7, b6 = a4 - a6, b7 = a5 - a7;
    const m = [b0 + b4, b1 + b5, b2 + b6, b3 + b7, b0 - b4, b1 - b5, b2 - b6, b3 - b7];
    for (let k = 0; k < 8; k++) {
      const inp = k < 4 ? xl : xr;
      bufs[k][idx[k]] = m[k] * 0.35355339 * gains[k] + inp;
      if (++idx[k] >= lens[k]) idx[k] = 0;
    }
    outL[i] = (y[0] + y[2] + y[4] + y[6]) * 0.25;
    outR[i] = (y[1] + y[3] + y[5] + y[7]) * 0.25;
  }
  return [outL, outR];
}
const [revL, revR] = hall(wetL, wetR, 6.2);

/* ---- mix → gentle glue → normalise to −1 dBFS → 16-bit ---- */
const outL = new Float32Array(N), outR = new Float32Array(N);
let peak = 0, env = 0;
for (let i = 0; i < N; i++) {
  let l = dryL[i] + revL[i] * 1.6, r = dryR[i] + revR[i] * 1.6;
  // slow peak follower + soft knee, so the climax gets loud without the quiet opening vanishing
  const lvl = Math.max(Math.abs(l), Math.abs(r));
  env = lvl > env ? env + (lvl - env) * 0.002 : env + (lvl - env) * 0.00004;
  const g = env > 0.35 ? Math.pow(0.35 / env, 0.45) : 1;
  l = Math.tanh(l * g * 1.25); r = Math.tanh(r * g * 1.25);
  outL[i] = l; outR[i] = r;
  peak = Math.max(peak, Math.abs(l), Math.abs(r));
}
const norm = Math.pow(10, -1 / 20) / (peak || 1);
const buf = Buffer.alloc(44 + N * 4);
buf.write("RIFF", 0); buf.writeUInt32LE(36 + N * 4, 4); buf.write("WAVE", 8);
buf.write("fmt ", 12); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(2, 22);
buf.writeUInt32LE(SR, 24); buf.writeUInt32LE(SR * 4, 28); buf.writeUInt16LE(4, 32); buf.writeUInt16LE(16, 34);
buf.write("data", 36); buf.writeUInt32LE(N * 4, 40);
for (let i = 0; i < N; i++) {
  const d = (rand() - rand()) / 32768;
  buf.writeInt16LE(Math.max(-32768, Math.min(32767, Math.round((outL[i] * norm + d) * 32767))), 44 + i * 4);
  buf.writeInt16LE(Math.max(-32768, Math.min(32767, Math.round((outR[i] * norm + d) * 32767))), 46 + i * 4);
}
const out = path.join(here, "out", "genesis-ai-score-extended.wav");
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, buf);
console.log(`${out} · ${(buf.length / 1048576).toFixed(1)} MB`);
