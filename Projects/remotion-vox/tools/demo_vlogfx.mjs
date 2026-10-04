// demo_vlogfx.mjs — build projects/vlogfx-demo/project.json
// Recreates the CapCut "VLOG nâng cao" reel formula (Edit Không Khó,
// fb reel 2298976200877685): beat-synced cuts + landmark-cutout whip
// transition (tách nền vật mốc) + linear-mask wipe (mặt nạ tuyến tính)
// + zoom-punch speed-ramp hits. 12s @ 30fps, 120bpm => beat = 15 frames.

import {mkdirSync, writeFileSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const FPS = 30;
const TOTAL = 360; // 12s
const BEAT = 15; // 120bpm

const footage = (id, asset, from, dur, extra = {}) => ({
  id, kind: 'video', from, durationInFrames: dur, asset,
  trimStartFrames: 0, fit: 'cover', layout: {}, motion: 'none',
  volume: 0, fadeInFrames: 0, wipeInFrames: 0, wipeDir: 'left', filter: {},
  ...extra,
});

const sfx = (id, name, from, volume = 0.45) => ({
  id, kind: 'audio', from, durationInFrames: Math.min(60, TOTAL - from),
  asset: `sfx/${name}.wav`, volume, trimStartFrames: 0,
});

const tag = (id, content, from, dur, color, extra = {}) => ({
  id, kind: 'text', from, durationInFrames: dur, content,
  preset: 'tag', color, animation: 'pop',
  animationParams: {damping: 11, stiffness: 180, restDeg: -2},
  layout: {}, fontSize: null, ...extra,
});

const tracks = [
  {
    id: 'trk-scenes', name: 'Scenes', type: 'video',
    muted: false, hidden: false, locked: false,
    clips: [
      // scene A (Tokyo B&W) — beat cuts với zoom-punch mỗi nhịp
      footage('a1', 'assets/scene_a.jpg', 0, 2 * BEAT, {motion: 'zoom-punch'}),
      footage('a2', 'assets/scene_a.jpg', 2 * BEAT, 2 * BEAT, {
        motion: 'zoom-punch', filter: {saturate: 1.5, contrast: 1.1},
      }),
      footage('a3', 'assets/scene_a.jpg', 4 * BEAT, 3 * BEAT, {motion: 'pan'}),
      // scene B (HK neon) — vào đúng lúc cutout che giữa màn (beat 7)
      footage('b1', 'assets/scene_b.jpg', 7 * BEAT, 2 * BEAT, {motion: 'zoom-punch'}),
      // +12 frame đè qua đoạn wipe của C để khe wipe lộ cảnh B, không lộ nền đen
      footage('b2', 'assets/scene_b.jpg', 9 * BEAT, 6 * BEAT + 12, {motion: 'pan'}),
      // scene C (desert sign) — mặt nạ tuyến tính wipe vào (beat 15)
      footage('c1', 'assets/scene_c.jpg', 15 * BEAT, TOTAL - 15 * BEAT, {
        motion: 'pan', wipeInFrames: 12, wipeDir: 'left',
        filter: {saturate: 1.2},
      }),
    ],
  },
  {
    id: 'trk-cutout', name: 'Landmark', type: 'sticker',
    muted: false, hidden: false, locked: false,
    clips: [
      // vật mốc: cột đèn whip vào trước cú đổi cảnh 1 beat, whip ra sau đó
      {
        id: 'light-1', kind: 'sticker',
        from: 6 * BEAT, durationInFrames: 4 * BEAT,
        asset: 'assets/el_light.png',
        layout: {x: 690, y: 120, w: 540, rotation: 0, opacity: 1},
        entrance: {variant: 'whip', delayFrames: 0, params: {}},
        exit: {variant: 'whip-out', delayFrames: 0, params: {}},
        idle: {amp: 4, phase: 0}, shadow: 'lg',
      },
    ],
  },
  {
    id: 'trk-text', name: 'Text', type: 'text',
    muted: false, hidden: false, locked: false,
    clips: [
      tag('t1', 'VLOG FX', 4, 7 * BEAT - 4, '#FFE01B'),
      tag('t2', '街 NEON', 7 * BEAT + 4, 8 * BEAT - 4, '#4EC3E0'),
      tag('t3', '砂漠 ROAD', 15 * BEAT + 4, TOTAL - 15 * BEAT - 4, '#FF8C42'),
      {
        id: 'credit', kind: 'text', from: 16 * BEAT,
        durationInFrames: TOTAL - 16 * BEAT,
        content: 'remotion-vox demo', preset: 'punch', color: '#FFE01B',
        animation: 'slide-in', animationParams: {},
        layout: {}, fontSize: 44,
      },
    ],
  },
  {
    id: 'trk-music', name: 'Beat', type: 'audio',
    muted: false, hidden: false, locked: false,
    clips: [{
      id: 'beat-1', kind: 'audio', from: 0, durationInFrames: TOTAL,
      asset: 'assets/beat.wav', volume: 0.5, trimStartFrames: 0,
    }],
  },
  {
    id: 'trk-sfx', name: 'SFX', type: 'audio',
    muted: false, hidden: false, locked: false,
    clips: [
      sfx('s1', 'pop', 4, 0.4),
      sfx('s2', 'whoosh', 6 * BEAT, 0.55), // whip in
      sfx('s3', 'thud', 7 * BEAT, 0.5), // đổi cảnh sau lưng vật mốc
      sfx('s4', 'swipe', 9 * BEAT - 18, 0.5), // whip out
      sfx('s5', 'riser', 14 * BEAT, 0.45), // build trước wipe
      sfx('s6', 'shatter', 15 * BEAT, 0.4), // wipe hit
    ],
  },
];

const now = new Date().toISOString();
const project = {
  version: 1,
  meta: {
    name: 'vlogfx-demo', channel: null, templateRef: null,
    fps: FPS, width: 1920, height: 1080, createdAt: now, modifiedAt: now,
  },
  timeline: {durationInFrames: TOTAL},
  sceneMarkers: [
    {id: 'm1', atFrame: 0, label: 'A tokyo'},
    {id: 'm2', atFrame: 6 * BEAT, label: 'whip vật mốc'},
    {id: 'm3', atFrame: 7 * BEAT, label: 'B neon'},
    {id: 'm4', atFrame: 15 * BEAT, label: 'C wipe'},
  ],
  tracks,
  captions: {source: 'none', style: 'outline', enabled: false, fontSize: 44, lines: [], words: []},
  theme: {
    palette: {bgTop: '#101216', bgBottom: '#101216', accent: '#FFE01B'},
    fontFamily: '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
    canvasColor: '#0B0C10',
  },
};

const dir = join(ROOT, 'projects', 'vlogfx-demo');
mkdirSync(dir, {recursive: true});
writeFileSync(join(dir, 'project.json'), JSON.stringify(project, null, 2), 'utf8');
console.log('OK projects/vlogfx-demo/project.json — 12s, 24 beat, 3 scene + whip + wipe');
