#!/usr/bin/env node
/**
 * Headless 1080p Demo Video Recorder using Chromium CDP + FFmpeg (Zero external npm deps!)
 * Captures all 4 keynote demos from `demos/live_demo_studio.html` into crisp H.264 MP4s + PNG posters.
 */
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { setTimeout as delay } from 'node:timers/promises';

const ROOT = '/home/antigravity/cmanikandan/gdg-blr-talk-nov14-2026';
const HTML_URL = `file://${ROOT}/demos/live_demo_studio.html?record=1`;
const OUT_DIR = `${ROOT}/assets/videos`;
const TMP_DIR = `/tmp/demo_frames_${Date.now()}`;

const SCENES = [
  { id: 1, name: 'demo1_antigravity_swarm_kickoff', duration: 11.0, posterAt: 9.2 },
  { id: 2, name: 'demo2_decisions_api_167ms', duration: 10.0, posterAt: 8.5 },
  { id: 3, name: 'demo3_live38_voice_multicloud_adk', duration: 12.5, posterAt: 10.8 },
  { id: 4, name: 'demo4_review_shipped_pr', duration: 10.0, posterAt: 8.5 },
];

const FPS = 15;
const PORT = 9333;

async function waitForCDP() {
  for (let i = 0; i < 40; i++) {
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

async function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.mkdirSync(TMP_DIR, { recursive: true });

  console.log('Launching headless Chromium 1920x1080...');
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
    await delay(1000);

    for (const scene of SCENES) {
      const sceneFrameDir = path.join(TMP_DIR, scene.name);
      fs.mkdirSync(sceneFrameDir, { recursive: true });
      const totalFrames = Math.round(scene.duration * FPS);
      console.log(`Recording Scene ${scene.id} (${scene.name}): ${totalFrames} frames @ ${FPS}fps...`);

      for (let f = 0; f < totalFrames; f++) {
        const t = f / FPS;
        await cdp.send('Runtime.evaluate', {
          expression: `window.renderDemoAt(${scene.id}, ${t.toFixed(3)})`,
        });
        const shot = await cdp.send('Page.captureScreenshot', { format: 'jpeg', quality: 92 });
        const framePath = path.join(sceneFrameDir, `frame_${String(f).padStart(4, '0')}.jpg`);
        fs.writeFileSync(framePath, Buffer.from(shot.data, 'base64'));
      }

      // Capture high-res PNG poster frame at climax timestamp
      await cdp.send('Runtime.evaluate', {
        expression: `window.renderDemoAt(${scene.id}, ${scene.posterAt})`,
      });
      const posterShot = await cdp.send('Page.captureScreenshot', { format: 'png' });
      const posterPath = path.join(OUT_DIR, `${scene.name}_poster.png`);
      fs.writeFileSync(posterPath, Buffer.from(posterShot.data, 'base64'));

      // Encode H.264 MP4 compatible with all browsers, QuickTime, PowerPoint, and Google Drive/Slides
      const mp4Path = path.join(OUT_DIR, `${scene.name}.mp4`);
      execFileSync('ffmpeg', [
        '-y',
        '-framerate', String(FPS),
        '-i', path.join(sceneFrameDir, 'frame_%04d.jpg'),
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '20',
        '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart',
        mp4Path,
      ], { stdio: 'ignore' });

      const sizeKB = Math.round(fs.statSync(mp4Path).size / 1024);
      console.log(`  ✔ Saved ${mp4Path} (${sizeKB} KB) + poster PNG`);
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
