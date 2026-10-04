// demo_vlogfx2.mjs — vlogfx2-demo: bản dựng lại ĐÚNG công thức intro reel
// fb/2298976200877685 (Edit Không Khó), lần này bằng VIDEO THẬT, khung dọc 9:16:
//   ① beat-cut + ĐỔI TỐC ĐỘ (speed 2.0 → 0.5 → 1.0) trên footage người qua đường
//   ② TÁCH NỀN VẬT MỐC: đèn giao thông + doodle mèo vẽ tay + số đếm ngược trong ô đèn
//   ③ MẶT NẠ GƯƠNG: tram lật gương rồi lật lại
//   ④ MẶT NẠ TUYẾN TÍNH: split 3 dải ngang, mỗi dải wipe vào lệch 1 beat
//   + sticker con vịt + tag chữ, tất cả rơi đúng beat 120bpm.
// 12s @ 30fps, 1080x1920. Chạy: node tools/demo_vlogfx2.mjs

import {mkdirSync, writeFileSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const FPS = 30;
const TOTAL = 360;
const B = 15; // 1 beat @120bpm

const video = (id, asset, from, dur, extra = {}) => ({
  id, kind: 'video', from, durationInFrames: dur, asset,
  trimStartFrames: 0, fit: 'cover', layout: {}, motion: 'none',
  speed: 1, mirror: false, volume: 0,
  fadeInFrames: 0, wipeInFrames: 0, wipeDir: 'left', filter: {},
  ...extra,
});

const sticker = (id, asset, from, dur, layout, extra = {}) => ({
  id, kind: 'sticker', from, durationInFrames: dur, asset,
  layout: {rotation: 0, opacity: 1, ...layout},
  entrance: {variant: 'pop', delayFrames: 0, params: {}},
  exit: null, idle: {amp: 5, phase: 0}, shadow: 'lg',
  ...extra,
});

const text = (id, content, from, dur, extra = {}) => ({
  id, kind: 'text', from, durationInFrames: dur, content,
  preset: 'tag', color: '#FFE01B', animation: 'pop',
  animationParams: {damping: 11, stiffness: 180, restDeg: -2},
  layout: {}, fontSize: null, ...extra,
});

const sfx = (id, name, from, volume = 0.45) => ({
  id, kind: 'audio', from, durationInFrames: Math.min(60, TOTAL - from),
  asset: `sfx/${name}.wav`, volume, trimStartFrames: 0,
});

const BAND_H = 600; // split 3 dải: 20/660/1300, khe đen 40px

const tracks = [
  {
    id: 'trk-video', name: 'Footage', type: 'video',
    muted: false, hidden: false, locked: false,
    clips: [
      // ① beat-cut + đổi tốc độ (crosswalk)
      video('v-a1', 'assets/clip_cross.mp4', 0, 2 * B, {speed: 2}),
      video('v-a2', 'assets/clip_cross.mp4', 2 * B, B, {
        speed: 0.5, trimStartFrames: 120, filter: {saturate: 1.3},
      }),
      video('v-a3', 'assets/clip_cross.mp4', 3 * B, B, {speed: 1, trimStartFrames: 200}),
      // ② vật mốc: đèn giao thông (doodle + đếm ngược đè bằng track trên)
      video('v-b', 'assets/clip_light.mp4', 4 * B, 6 * B, {fadeInFrames: 6}),
      // ③ mặt nạ gương: tram lật gương → lật lại
      video('v-c1', 'assets/clip_tram.mp4', 10 * B, 3 * B, {
        mirror: true, wipeInFrames: 10, wipeDir: 'right',
      }),
      video('v-c2', 'assets/clip_tram.mp4', 13 * B, 2 * B, {
        mirror: false, trimStartFrames: 45,
      }),
      // ⑤ kết: crosswalk tua nhanh
      video('v-e', 'assets/clip_cross.mp4', 21 * B, TOTAL - 21 * B, {
        speed: 2, trimStartFrames: 30, fadeInFrames: 8,
      }),
    ],
  },
  {
    id: 'trk-bands', name: 'Split bands', type: 'video',
    muted: false, hidden: false, locked: false,
    clips: [
      // ④ mặt nạ tuyến tính: 3 dải ngang vào lệch 1 beat
      video('band-1', 'assets/clip_tram.mp4', 15 * B, 6 * B, {
        layout: {x: 0, y: 20, w: 1080, h: BAND_H},
        wipeInFrames: 10, wipeDir: 'left', trimStartFrames: 60,
      }),
      video('band-2', 'assets/clip_light.mp4', 16 * B, 5 * B, {
        layout: {x: 0, y: 660, w: 1080, h: BAND_H},
        wipeInFrames: 10, wipeDir: 'right', trimStartFrames: 90,
      }),
      video('band-3', 'assets/clip_cross.mp4', 17 * B, 4 * B, {
        layout: {x: 0, y: 1300, w: 1080, h: BAND_H},
        wipeInFrames: 10, wipeDir: 'left', trimStartFrames: 150,
      }),
    ],
  },
  {
    id: 'trk-sticker', name: 'Stickers', type: 'sticker',
    muted: false, hidden: false, locked: false,
    clips: [
      // vịt ở intro (góc dưới trái, như reel)
      sticker('duck-1', 'assets/el_duck.png', 6, 4 * B - 6,
        {x: 40, y: 1440, w: 330}, {idle: {amp: 6, phase: 1}}),
      // doodle mèo dán lên đèn giao thông
      sticker('cat-1', 'assets/doodle_cat.png', 5 * B, 5 * B,
        {x: 620, y: 430, w: 230},
        {entrance: {variant: 'grow', delayFrames: 0, params: {}}, shadow: 'none',
         idle: {amp: 2, phase: 0}}),
      // vịt quay lại giữa split
      sticker('duck-2', 'assets/el_duck.png', 18 * B, 3 * B,
        {x: 700, y: 900, w: 300},
        {entrance: {variant: 'wobble', delayFrames: 0, params: {}}}),
    ],
  },
  {
    id: 'trk-text', name: 'Text', type: 'text',
    muted: false, hidden: false, locked: false,
    clips: [
      text('t-intro', '今日はコレ', 4, 4 * B - 4, {
        layout: {x: 70, y: 150}, fontSize: 86,
      }),
      // đếm ngược trong ô đèn — mỗi số 1 beat, plain đỏ to
      text('cnt-3', '3', 6 * B, B, {
        preset: 'plain', color: '#FF3B30', animation: 'pop',
        layout: {x: 500, y: 470}, fontSize: 150,
      }),
      text('cnt-2', '2', 7 * B, B, {
        preset: 'plain', color: '#FF9500', animation: 'pop',
        layout: {x: 500, y: 470}, fontSize: 150,
      }),
      text('cnt-1', '1', 8 * B, B, {
        preset: 'plain', color: '#2EC46F', animation: 'pop',
        layout: {x: 500, y: 470}, fontSize: 150,
      }),
      text('t-mirror', 'MIRROR', 10 * B + 4, 5 * B - 4, {
        color: '#4EC3E0', layout: {x: 70, y: 150}, fontSize: 80,
      }),
      text('t-split', '3 MÀN', 15 * B + 4, 6 * B - 4, {
        color: '#FF8C42', layout: {x: 70, y: 40}, fontSize: 72,
      }),
      {
        id: 't-end', kind: 'text', from: 21 * B + 6,
        durationInFrames: TOTAL - 21 * B - 6,
        content: 'EDIT xong 🎬', preset: 'punch', color: '#FFE01B',
        animation: 'pop', animationParams: {restDeg: -1.5},
        layout: {x: 90, y: 1650}, fontSize: 72,
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
      sfx('s-pop1', 'pop', 6, 0.4),
      sfx('s-whoosh1', 'whoosh', 4 * B, 0.5),
      sfx('s-c3', 'click', 6 * B, 0.5),
      sfx('s-c2', 'click', 7 * B, 0.5),
      sfx('s-c1', 'coin', 8 * B, 0.5),
      sfx('s-mirror', 'swipe', 10 * B, 0.5),
      sfx('s-flip', 'thud', 13 * B, 0.5),
      sfx('s-b1', 'paper', 15 * B, 0.45),
      sfx('s-b2', 'paper', 16 * B, 0.45),
      sfx('s-b3', 'paper', 17 * B, 0.45),
      sfx('s-end', 'riser', 20 * B, 0.45),
    ],
  },
];

const now = new Date().toISOString();
const project = {
  version: 1,
  meta: {
    name: 'vlogfx2-demo', channel: null, templateRef: null,
    fps: FPS, width: 1080, height: 1920, createdAt: now, modifiedAt: now,
  },
  timeline: {durationInFrames: TOTAL},
  sceneMarkers: [
    {id: 'm1', atFrame: 0, label: '① beat-cut + speed'},
    {id: 'm2', atFrame: 4 * B, label: '② vật mốc + doodle'},
    {id: 'm3', atFrame: 10 * B, label: '③ gương'},
    {id: 'm4', atFrame: 15 * B, label: '④ split 3 dải'},
    {id: 'm5', atFrame: 21 * B, label: 'kết'},
  ],
  tracks,
  captions: {source: 'none', style: 'outline', enabled: false, fontSize: 44, lines: [], words: []},
  theme: {
    palette: {bgTop: '#0B0C10', bgBottom: '#0B0C10', accent: '#FFE01B'},
    fontFamily: '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
    canvasColor: '#000000',
  },
};

const dir = join(ROOT, 'projects', 'vlogfx2-demo');
mkdirSync(dir, {recursive: true});
writeFileSync(join(dir, 'project.json'), JSON.stringify(project, null, 2), 'utf8');
console.log('OK projects/vlogfx2-demo/project.json — 9:16, 12s, 4 hiệu ứng reel');
