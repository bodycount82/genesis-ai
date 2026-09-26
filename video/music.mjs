#!/usr/bin/env node
// Genesis AI trailer score — synthesized from scratch (no samples, no third-party audio), so it is
// free to use anywhere. Writes out/genesis-ai-score.wav (48 kHz, stereo, 16-bit, 45 s).
//
// A slow pad in D that swells with the sunrise, a sub "bloom" as the logo resolves (6.4 s), a soft
// bell arpeggio under the five feature beats (11–30 s, one chord per beat), a lift into the
// showcase and a resolve on the end card.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const SR = 48000, DUR = 45, N = SR * DUR;
const L = new Float32Array(N), R = new Float32Array(N);

/* ---- helpers ---- */
let seed = 1337;
const rand = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
const clamp01 = (x) => (x < 0 ? 0 : x > 1 ? 1 : x);
const smooth = (x) => { x = clamp01(x); return x * x * (3 - 2 * x); };
const ramp = (t, a, b) => clamp01((t - a) / (b - a));
const midi = (m) => 440 * Math.pow(2, (m - 69) / 12);
const TABLE = 8192, SINE = new Float32Array(TABLE + 1);
for (let i = 0; i <= TABLE; i++) SINE[i] = Math.sin((i / TABLE) * Math.PI * 2);
const sinLU = (ph) => { const x = (ph - Math.floor(ph)) * TABLE, i = x | 0; return SINE[i] + (SINE[i + 1] - SINE[i]) * (x - i); };

// note names → midi
const NOTE = { C: 0, "C#": 1, D: 2, "D#": 3, E: 4, F: 5, "F#": 6, G: 7, "G#": 8, A: 9, "A#": 10, B: 11 };
const n = (s) => { const m = s.match(/^([A-G]#?)(-?\d)$/); return 12 * (parseInt(m[2], 10) + 1) + NOTE[m[1]]; };

/* ---- pad: detuned additive voices, one chord per section, raised-cosine crossfades ---- */
const chords = [
  // [start, end, notes, level]
  [0.0, 11.4, ["D2", "A2", "E3", "A3", "D4", "F#4"], 1.0],   // Dsus2 → D: the sunrise
  [11.0, 15.0, ["B1", "F#2", "D3", "A3", "C#4", "F#4"], 0.9], // Bm9      · local & private
  [14.8, 18.8, ["G1", "D2", "B2", "F#3", "A3", "D4"], 0.9],   // Gmaj9    · memory
  [18.6, 22.6, ["D2", "A2", "F#3", "C#4", "E4", "A4"], 0.9],  // Dmaj9    · missions
  [22.4, 26.4, ["A1", "E2", "C#3", "E3", "B3", "E4"], 0.9],   // Aadd9    · browser
  [26.2, 30.4, ["B1", "F#2", "D3", "F#3", "A3", "E4"], 0.9],  // Bm11     · android
  [30.0, 34.2, ["G1", "D2", "A2", "D3", "B3", "E4"], 0.95],   // Gadd9    · showcase
  [34.0, 38.4, ["A1", "E2", "D3", "E3", "A3", "D4"], 1.0],    // Asus4    · lift
  [38.0, 45.0, ["D2", "A2", "D3", "F#3", "A3", "E4", "A4"], 1.1], // Dadd9 · end card
];
const padGain = (t) => {
  const inA = smooth(ramp(t, 0.2, 5.5)) * (0.55 + 0.45 * smooth(ramp(t, 4.5, 7.0)));
  return inA * (1 - smooth(ramp(t, 43.6, 45.0)));
};
for (const [a, b, notes, level] of chords) {
  const fadeIn = a === 0 ? 0.01 : 0.9, fadeOut = b >= 45 ? 0.01 : 1.1;
  const s0 = Math.max(0, Math.floor((a - 0.3) * SR)), s1 = Math.min(N, Math.ceil((b + fadeOut) * SR));
  for (const name of notes) {
    const f0 = midi(n(name));
    const low = f0 < 90;
    const partials = low ? 4 : 6;
    for (let k = 1; k <= partials; k++) {
      const amp = (0.055 / Math.pow(k, 1.6)) * (low ? 1.2 : 1.0) * level;
      for (const cents of [-6, 0, 5.5]) {
        const f = f0 * k * Math.pow(2, cents / 1200);
        if (f > 5000) continue;
        const pan = 0.5 + (cents / 12) * 0.8 + (rand() - 0.5) * 0.2;
        const gl = Math.cos(pan * Math.PI / 2), gr = Math.sin(pan * Math.PI / 2);
        let ph = rand();
        const inc = f / SR;
        const lfoF = 0.05 + rand() * 0.12, lfoP = rand();
        for (let i = s0; i < s1; i++) {
          const t = i / SR;
          const env = (0.5 - 0.5 * Math.cos(Math.PI * clamp01((t - a + 0.3) / (fadeIn + 0.3)))) *
                      (0.5 + 0.5 * Math.cos(Math.PI * clamp01((t - b) / fadeOut)));
          const shimmer = 0.75 + 0.25 * sinLU(lfoP + t * lfoF);
          // upper partials bloom with the sunrise and the end card
          const bright = k === 1 ? 1 : 0.35 + 0.65 * Math.max(smooth(ramp(t, 4.0, 8.0)) * (1 - 0.4 * smooth(ramp(t, 10.5, 12))), smooth(ramp(t, 37.5, 40)));
          const v = sinLU(ph) * amp * env * shimmer * bright * padGain(t);
          L[i] += v * gl; R[i] += v * gr;
          ph += inc;
        }
      }
    }
  }
}

/* ---- bell arpeggio under the beats and the showcase ---- */
const arps = [
  [11.0, ["F#4", "B4", "C#5", "D5", "F#5", "D5", "C#5", "B4"]],
  [14.8, ["D4", "G4", "A4", "B4", "D5", "B4", "A4", "F#4"]],
  [18.6, ["F#4", "A4", "C#5", "E5", "F#5", "E5", "C#5", "A4"]],
  [22.4, ["E4", "A4", "B4", "C#5", "E5", "C#5", "B4", "A4"]],
  [26.2, ["F#4", "B4", "D5", "E5", "F#5", "E5", "D5", "B4"]],
  [30.0, ["D4", "G4", "A4", "B4", "D5", "E5", "D5", "B4"]],
  [34.0, ["E4", "A4", "D5", "E5", "A5", "E5", "D5", "A4"]],
];
const STEP = 3.8 / 8;
function bell(t0, name, gain, pan) {
  const f = midi(n(name));
  const s0 = Math.floor(t0 * SR), s1 = Math.min(N, s0 + Math.floor(3.2 * SR));
  const gl = Math.cos(pan * Math.PI / 2), gr = Math.sin(pan * Math.PI / 2);
  for (let i = s0; i < s1; i++) {
    const t = (i - s0) / SR;
    const env = (1 - Math.exp(-t / 0.006)) * Math.exp(-t / 0.9);
    const v = (sinLU(f * t) + 0.18 * sinLU(2.0 * f * t) * Math.exp(-t / 0.25) + 0.06 * sinLU(3.01 * f * t) * Math.exp(-t / 0.12)) * env * gain;
    L[i] += v * gl; R[i] += v * gr;
  }
}
for (const [start, pattern] of arps) {
  const span = start >= 34 ? 4.0 : 3.8;
  const count = Math.round(span / STEP);
  for (let j = 0; j < count; j++) {
    const t = start + j * STEP;
    const into = smooth(ramp(t, 11.0, 13.5)) * (1 - 0.35 * smooth(ramp(t, 30, 31))) * (1 - smooth(ramp(t, 37.2, 38.0)));
    const accent = j % 4 === 0 ? 1.0 : 0.72;
    bell(t, pattern[j % pattern.length], 0.05 * into * accent, 0.3 + 0.4 * ((j * 3) % 8) / 7);
  }
}
// the end card: three slow bells resolving to D
[[38.2, "A4"], [39.2, "D5"], [40.4, "F#5"], [41.9, "A5"]].forEach(([t, name], i) => bell(t, name, 0.045, 0.35 + 0.1 * i));

/* ---- rises and sub blooms on the cuts ---- */
function rise(tEnd, len, gain) {
  let lp = 0, lp2 = 0;
  const s0 = Math.max(0, Math.floor((tEnd - len) * SR)), s1 = Math.floor(tEnd * SR);
  for (let i = s0; i < s1; i++) {
    const u = (i - s0) / (s1 - s0);
    const cutoff = 200 + 5000 * u * u;
    const a = 1 - Math.exp(-2 * Math.PI * cutoff / SR);
    const w = rand() * 2 - 1;
    lp += a * (w - lp); lp2 += a * (lp - lp2);
    const env = Math.pow(u, 2.4) * gain * (1 - smooth((u - 0.97) / 0.03));
    L[i] += lp2 * env; R[i] += (lp2 * 0.9 + (rand() - 0.5) * 0.02) * env;
  }
}
function bloom(t0, gain, fStart = 55, fEnd = 38) {
  const s0 = Math.floor(t0 * SR), s1 = Math.min(N, s0 + Math.floor(4.5 * SR));
  let ph = 0;
  for (let i = s0; i < s1; i++) {
    const t = (i - s0) / SR;
    const f = fEnd + (fStart - fEnd) * Math.exp(-t / 0.35);
    ph += f / SR;
    const env = (1 - Math.exp(-t / 0.02)) * Math.exp(-t / 1.4);
    const v = (sinLU(ph) + 0.25 * sinLU(ph * 2)) * env * gain;
    L[i] += v; R[i] += v;
  }
}
rise(6.4, 3.2, 0.10); bloom(6.4, 0.34);
rise(11.0, 1.6, 0.05); bloom(11.0, 0.16, 60, 44);
rise(30.0, 1.8, 0.06); bloom(30.0, 0.18, 60, 44);
rise(38.0, 2.4, 0.09); bloom(38.0, 0.30);

/* ---- stereo Schroeder reverb (4 combs + 2 allpasses per side) ---- */
function reverb(inp, combs, aps, fb, damp) {
  const out = new Float32Array(N);
  for (const d of combs) {
    const buf = new Float32Array(d); let idx = 0, filt = 0;
    for (let i = 0; i < N; i++) {
      const y = buf[idx];
      filt = y * (1 - damp) + filt * damp;
      buf[idx] = inp[i] + filt * fb;
      out[i] += y;
      if (++idx >= d) idx = 0;
    }
  }
  for (const d of aps) {
    const buf = new Float32Array(d); let idx = 0;
    for (let i = 0; i < N; i++) {
      const b = buf[idx], x = out[i];
      const y = -x + b; buf[idx] = x + b * 0.5; out[i] = y;
      if (++idx >= d) idx = 0;
    }
  }
  return out;
}
const s = SR / 44100;
const wetL = reverb(L, [1557, 1617, 1491, 1422].map((d) => Math.round(d * s * 1.9)), [225, 556].map((d) => Math.round(d * s)), 0.86, 0.35);
const wetR = reverb(R, [1617 + 23, 1557 + 23, 1422 + 23, 1491 + 23].map((d) => Math.round(d * s * 1.9)), [248, 579].map((d) => Math.round(d * s)), 0.86, 0.35);

/* ---- mix, gentle saturation, normalise to −1 dBFS, fade tail ---- */
const mixL = new Float32Array(N), mixR = new Float32Array(N);
let peak = 0;
for (let i = 0; i < N; i++) {
  const t = i / SR;
  const fade = smooth(ramp(t, 0, 0.3)) * (1 - smooth(ramp(t, 44.0, 45.0)));
  const l = Math.tanh((L[i] * 0.72 + wetL[i] * 0.09) * 1.4) * fade;
  const r = Math.tanh((R[i] * 0.72 + wetR[i] * 0.09) * 1.4) * fade;
  mixL[i] = l; mixR[i] = r;
  peak = Math.max(peak, Math.abs(l), Math.abs(r));
}
const g = Math.pow(10, -1 / 20) / (peak || 1);

const buf = Buffer.alloc(44 + N * 4);
buf.write("RIFF", 0); buf.writeUInt32LE(36 + N * 4, 4); buf.write("WAVE", 8);
buf.write("fmt ", 12); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(2, 22);
buf.writeUInt32LE(SR, 24); buf.writeUInt32LE(SR * 4, 28); buf.writeUInt16LE(4, 32); buf.writeUInt16LE(16, 34);
buf.write("data", 36); buf.writeUInt32LE(N * 4, 40);
for (let i = 0; i < N; i++) {
  // TPDF dither
  const d = (rand() - rand()) / 32768;
  buf.writeInt16LE(Math.max(-32768, Math.min(32767, Math.round((mixL[i] * g + d) * 32767))), 44 + i * 4);
  buf.writeInt16LE(Math.max(-32768, Math.min(32767, Math.round((mixR[i] * g + d) * 32767))), 46 + i * 4);
}
const out = path.join(here, "out", "genesis-ai-score.wav");
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, buf);
console.log(`${out} · ${(buf.length / 1048576).toFixed(1)} MB · peak gain ${(20 * Math.log10(g)).toFixed(1)} dB`);
