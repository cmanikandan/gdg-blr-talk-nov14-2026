#!/usr/bin/env node
/**
 * Cinema-Grade 1080p 30fps Demo Video Recorder using Chromium CDP + FFmpeg.
 *
 * - Injects all 4 REAL live API traces (`demos/traces/demo{1..4}_trace.json`) into `demos/studio.html?record=1`
 * - Renders 1920x1080 @ 30fps crisp H.264 MP4 videos + high-res PNG posters
 * - Muxes REAL Gemini 3.8 HD Voice WAV tracks (`gemini-3.8-flash-tts`) synced to the exact millisecond in Demo 3!
 */
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { setTimeout as delay } from 'node:timers/promises';

const ROOT = '/home/antigravity/cmanikandan/gdg-blr-talk-nov14-2026';
const HTML_URL = `file://${ROOT}/demos/studio.html?record=1`;
const TRACES_DIR = `${ROOT}/demos/traces`;
const OUT_DIR = `${ROOT}/assets/videos`;
const TMP_DIR = `/tmp/demo_frames_${Date.now()}`;

const FPS = 30;
const PORT = 9334;

function loadTraces() {
  const traces = {};
  for (const [k, f] of [
    ['demo1', 'demo1_trace.json'],
    ['demo2', 'demo2_trace.json'],
    ['demo3', 'demo3_trace.json'],
    ['demo4', 'demo4_trace.json'],
    ['demo5', 'demo5_trace.json'],
  ]) {
    const p = path.join(TRACES_DIR, f);
    if (fs.existsSync(p)) {
      traces[k] = JSON.parse(fs.readFileSync(p, 'utf8'));
    }
  }
  return traces;
}

async function waitForCDP() {
  for (let i = 0; i < 45; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${PORT}/json/list`);
      const targets = await res.json();
      const page = targets.find((t) => t.type === 'page');
      if (page && page.webSocketDebuggerUrl) return page.webSocketDebuggerUrl;
    } catch {}
    await delay(200);
  }
  throw new Error('Timed out waiting for Chromium CDP endpoint');
}

class CDPSession {
  constructor(wsUrl) {
    this.ws = new WebSocket(wsUrl);
    this.nextId = 1;
    this.pending = new Map();
  }
  async connect() {
    await new Promise((resolve, reject) => {
      this.ws.addEventListener('open', resolve, { once: true });
      this.ws.addEventListener('error', reject, { once: true });
    });
    this.ws.addEventListener('message', (ev) => {
      const msg = JSON.parse(ev.data.toString());
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        if (msg.error) reject(new Error(JSON.stringify(msg.error)));
        else resolve(msg.result);
      }
    });
  }
  send(method, params = {}) {
    const id = this.nextId++;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }
  close() {
    this.ws.close();
  }
}

function buildDemo3AudioMix(demo3Trace, outWavPath) {
  const turns = demo3Trace.voice_turns || [];
  if (turns.length < 3) return null;
  const d1 = turns[0].duration_sec;
  const d2 = turns[1].duration_sec;
  const t1Ms = 200;
  const t2Ms = Math.round((0.2 + d1 + 0.35) * 1000);
  const t3Ms = Math.round((0.2 + d1 + 0.35 + d2 + 0.35) * 1000);

  const filterComplex =
    `[0:a]adelay=${t1Ms}|${t1Ms}[a0];` +
    `[1:a]adelay=${t2Ms}|${t2Ms}[a1];` +
    `[2:a]adelay=${t3Ms}|${t3Ms}[a2];` +
    `[a0][a1][a2]amix=inputs=3:duration=longest:normalize=0,volume=1.0[aout]`;

  execFileSync(
    'ffmpeg',
    [
      '-y',
      '-i', turns[0].wav_path,
      '-i', turns[1].wav_path,
      '-i', turns[2].wav_path,
      '-filter_complex', filterComplex,
      '-map', '[aout]',
      '-ar', '48000',
      '-ac', '2',
      outWavPath,
    ],
    { stdio: 'ignore' }
  );
  return outWavPath;
}

async function main() {
  const traces = loadTraces();
  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.mkdirSync(TMP_DIR, { recursive: true });

  const vt = traces.demo3.voice_turns || [];
  const demo3Dur = vt.length >= 3
    ? Math.ceil((0.2 + vt[0].duration_sec + 0.35 + vt[1].duration_sec + 0.35 + vt[2].duration_sec + 1.4) * 10) / 10
    : 30.0;

  const onlyArg = process.argv.find(a => a.startsWith('--only='));
  const onlyId = onlyArg ? Number(onlyArg.split('=')[1]) : null;
  const SCENES = [
    { id: 1, name: 'demo1_antigravity_swarm_kickoff', duration: 13.5, posterAt: 12.2, hasAudio: false },
    { id: 2, name: 'demo2_decisions_api_arena', duration: 15.0, posterAt: 13.8, hasAudio: false },
    { id: 3, name: 'demo3_live38_voice_multicloud_adk', duration: demo3Dur, posterAt: Math.max(12, demo3Dur - 4.0), hasAudio: true },
    { id: 4, name: 'demo4_review_shipped_pr', duration: 13.5, posterAt: 12.4, hasAudio: false },
    { id: 5, name: 'demo5_code_modernization', duration: 14.0, posterAt: 12.6, hasAudio: false },
  ].filter(s => !onlyId || s.id === onlyId);

  console.log(`Launching headless Chromium 1920x1080 @ ${FPS}fps...`);
  const chrome = spawn(
    '/usr/bin/chromium',
    [
      '--headless',
      '--no-sandbox',
      '--disable-gpu',
      '--disable-dev-shm-usage',
      `--remote-debugging-port=${PORT}`,
      '--window-size=1920,1080',
      'about:blank',
    ],
    { stdio: 'ignore' }
  );

  try {
    const wsUrl = await waitForCDP();
    const cdp = new CDPSession(wsUrl);
    await cdp.connect();

    await cdp.send('Page.enable');
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width: 1920,
      height: 1080,
      deviceScaleFactor: 1,
      mobile: false,
    });

    await cdp.send('Page.navigate', { url: HTML_URL });
    await delay(900);

    // Inject real captured traces directly into page memory
    const tracesJson = JSON.stringify(traces);
    await cdp.send('Runtime.evaluate', {
      expression: `window.__INJECTED_TRACES__ = ${tracesJson}; TRACES = window.__INJECTED_TRACES__; true;`,
    });

    for (const scene of SCENES) {
      const sceneFrameDir = path.join(TMP_DIR, scene.name);
      fs.mkdirSync(sceneFrameDir, { recursive: true });
      const totalFrames = Math.round(scene.duration * FPS);
      console.log(`Recording Scene ${scene.id} (${scene.name}): ${totalFrames} frames (${scene.duration}s @ ${FPS}fps)...`);

      for (let f = 0; f < totalFrames; f++) {
        const t = f / FPS;
        await cdp.send('Runtime.evaluate', {
          expression: `window.renderDemoAt(${scene.id}, ${t.toFixed(3)})`,
        });
        const shot = await cdp.send('Page.captureScreenshot', { format: 'jpeg', quality: 93 });
        const framePath = path.join(sceneFrameDir, `frame_${String(f).padStart(4, '0')}.jpg`);
        fs.writeFileSync(framePath, Buffer.from(shot.data, 'base64'));
      }

      // High-res PNG poster frame at climax timestamp
      await cdp.send('Runtime.evaluate', {
        expression: `window.renderDemoAt(${scene.id}, ${scene.posterAt.toFixed(3)})`,
      });
      const posterShot = await cdp.send('Page.captureScreenshot', { format: 'png' });
      const posterPath = path.join(OUT_DIR, `${scene.name}_poster.png`);
      fs.writeFileSync(posterPath, Buffer.from(posterShot.data, 'base64'));

      const mp4Path = path.join(OUT_DIR, `${scene.name}.mp4`);
      if (scene.hasAudio) {
        const mixWav = path.join(TMP_DIR, 'demo3_mix.wav');
        const audioPath = buildDemo3AudioMix(traces.demo3, mixWav);
        execFileSync(
          'ffmpeg',
          [
            '-y',
            '-framerate', String(FPS),
            '-i', path.join(sceneFrameDir, 'frame_%04d.jpg'),
            '-i', audioPath,
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '19',
            '-pix_fmt', 'yuv420p',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-shortest',
            '-movflags', '+faststart',
            mp4Path,
          ],
          { stdio: 'ignore' }
        );
      } else {
        execFileSync(
          'ffmpeg',
          [
            '-y',
            '-framerate', String(FPS),
            '-i', path.join(sceneFrameDir, 'frame_%04d.jpg'),
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '19',
            '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart',
            mp4Path,
          ],
          { stdio: 'ignore' }
        );
      }

      const sizeKB = Math.round(fs.statSync(mp4Path).size / 1024);
      console.log(`  ✔ Saved ${mp4Path} (${sizeKB} KB${scene.hasAudio ? ' + REAL Gemini 3.8 HD Audio!' : ''}) + poster PNG`);
    }

    cdp.close();
  } finally {
    chrome.kill('SIGKILL');
    fs.rmSync(TMP_DIR, { recursive: true, force: true });
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
