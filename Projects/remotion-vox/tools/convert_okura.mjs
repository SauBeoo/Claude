// convert_okura.mjs — one-off: convert the old OkuraDemo SEGMENTS (hardcoded
// JSX data) into projects/okura-demo/project.json. Also serves as the
// reference for how collage scenes map onto the track model.
// Run: node tools/convert_okura.mjs

import {mkdirSync, writeFileSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const TOTAL = 497;

// verbatim from src/OkuraDemo.jsx (studio-injected garbage transforms dropped)
const SEGMENTS = [
  {
    from: 0, duration: 111, tag: 'オクラ', tagColor: '#FFE01B',
    splash: ['#7CB518', '#4EC3E0'],
    punch: {text: 'くたくたにゆでて…', appearAt: 50},
    hero: {src: 'el_okra.png', variant: 'rise', w: 900, x: 480, y: 170},
    supports: [
      {src: 'el_pot.png', w: 460, x: 1400, y: 520, delay: 16},
      {src: 'el_glass.png', w: 260, x: 150, y: 620, delay: 26},
    ],
    sfx: [
      {name: 'whoosh', at: 0, volume: 0.45},
      {name: 'pop', at: 6, volume: 0.4},
      {name: 'paper', at: 16, volume: 0.35},
      {name: 'click', at: 50, volume: 0.45},
    ],
  },
  {
    from: 111, duration: 92, tag: '刻む', tagColor: '#4EC3E0',
    splash: ['#4EC3E0', '#FFE01B'],
    punch: {text: 'それから、刻む。', appearAt: 55},
    hero: {src: 'el_sliced.png', variant: 'grow', w: 1150, x: 380, y: 190},
    supports: [
      {src: 'el_glass.png', w: 250, x: 130, y: 560, delay: 12},
      {src: 'el_knife.png', w: 230, x: 1560, y: 420, delay: 24},
    ],
    sfx: [
      {name: 'paper', at: 0, volume: 0.4},
      {name: 'pop', at: 6, volume: 0.4},
      {name: 'swipe', at: 24, volume: 0.45},
      {name: 'click', at: 55, volume: 0.45},
    ],
  },
  {
    from: 203, duration: 99, tag: '長年', tagColor: '#FF8C42',
    splash: ['#FF8C42', '#B8B8D1'],
    punch: {text: 'ずっと、そのやり方で。', appearAt: 42},
    hero: {src: 'el_senior.png', variant: 'flip', w: 1200, x: 360, y: 150},
    supports: [{src: 'el_clock.png', w: 420, x: 1440, y: 560, delay: 14}],
    sfx: [
      {name: 'whoosh', at: 0, volume: 0.4},
      {name: 'pop', at: 6, volume: 0.4},
      {name: 'paper', at: 14, volume: 0.35},
      {name: 'click', at: 42, volume: 0.4},
    ],
  },
  {
    from: 302, duration: 98, tag: '宝物', tagColor: '#2EC46F',
    splash: ['#2EC46F', '#FFE01B'],
    punch: {text: 'いちばんの宝物', appearAt: 50},
    hero: {src: 'el_gem.png', variant: 'punch', w: 1000, x: 430, y: 230},
    supports: [
      {src: 'el_okra.png', w: 340, x: 140, y: 580, delay: 12},
      {src: 'el_magnify.png', w: 300, x: 1500, y: 480, delay: 24},
    ],
    sfx: [
      {name: 'riser', at: 0, volume: 0.4},
      {name: 'thud', at: 10, volume: 0.5},
      {name: 'pop', at: 6, volume: 0.35},
      {name: 'coin', at: 50, volume: 0.45},
    ],
  },
  {
    from: 400, duration: 97, tag: '？', tagColor: '#FF5E5B',
    splash: ['#FF5E5B', '#4EC3E0'],
    punch: {text: '捨てているかも。', appearAt: 45},
    hero: {src: 'el_sink.png', variant: 'wobble', w: 1250, x: 340, y: 260},
    supports: [
      {src: 'el_pot.png', w: 340, x: 120, y: 560, delay: 12},
      {src: 'el_glass.png', w: 220, x: 1580, y: 620, delay: 22},
    ],
    sfx: [
      {name: 'boing', at: 0, volume: 0.5},
      {name: 'pop', at: 6, volume: 0.35},
      {name: 'paper', at: 12, volume: 0.35},
      {name: 'drop', at: 45, volume: 0.5},
    ],
  },
];

const layout = (x, y, w, rotation = 0) => ({x, y, w, rotation, opacity: 1});

const tracks = {
  background: {id: 'trk-bg', name: 'Background', type: 'background', clips: []},
  hero: {id: 'trk-hero', name: 'Hero', type: 'sticker', clips: []},
  sup1: {id: 'trk-sup1', name: 'Support 1', type: 'sticker', clips: []},
  sup2: {id: 'trk-sup2', name: 'Support 2', type: 'sticker', clips: []},
  tag: {id: 'trk-tag', name: 'Tag', type: 'text', clips: []},
  punch: {id: 'trk-punch', name: 'Punch', type: 'text', clips: []},
  voice: {id: 'trk-voice', name: 'Voice', type: 'audio', clips: []},
  sfx: {id: 'trk-sfx', name: 'SFX', type: 'audio', clips: []},
};

const sceneMarkers = [];

SEGMENTS.forEach((seg, i) => {
  const n = i + 1;
  const F = seg.from;
  const D = seg.duration;
  sceneMarkers.push({id: `scene-${n}`, atFrame: F, label: seg.tag});

  tracks.background.clips.push({
    id: `bg-${n}`, kind: 'background', from: F, durationInFrames: D,
    paper: 'assets/paper.jpg', tint: '#F2EDE4', tintOpacity: 0.55,
    grid: true, dots: true, splash: seg.splash,
  });

  tracks.hero.clips.push({
    id: `hero-${n}`, kind: 'sticker', from: F, durationInFrames: D,
    asset: `assets/${seg.hero.src}`,
    layout: layout(seg.hero.x, seg.hero.y, seg.hero.w),
    entrance: {variant: seg.hero.variant, delayFrames: 0, params: {}},
    exit: null, idle: {amp: 6, phase: 0}, shadow: 'lg',
  });

  seg.supports.forEach((sp, j) => {
    const lane = j === 0 ? tracks.sup1 : tracks.sup2;
    lane.clips.push({
      id: `sup-${n}-${j + 1}`, kind: 'sticker',
      from: F + sp.delay, durationInFrames: D - sp.delay,
      asset: `assets/${sp.src}`,
      layout: layout(sp.x, sp.y, sp.w, j % 2 ? 4 : -5),
      entrance: {variant: 'pop', delayFrames: 0, params: {}},
      exit: null, idle: {amp: 4, phase: 2.1 * (j + 1)}, shadow: 'sm',
    });
  });

  tracks.tag.clips.push({
    id: `tag-${n}`, kind: 'text', from: F + 4, durationInFrames: D - 4,
    content: seg.tag, preset: 'tag', color: seg.tagColor,
    animation: seg.hero.variant === 'flip' ? 'pop-swing' : 'pop',
    animationParams: {damping: 11, stiffness: 180, restDeg: -2},
    layout: {}, fontSize: null,
  });

  tracks.punch.clips.push({
    id: `punch-${n}`, kind: 'text',
    from: F + seg.punch.appearAt, durationInFrames: D - seg.punch.appearAt,
    content: seg.punch.text, preset: 'punch', color: '#FFE01B',
    animation: 'pop', animationParams: {restDeg: -1.5},
    layout: {}, fontSize: null,
  });

  seg.sfx.forEach((f, k) => {
    tracks.sfx.clips.push({
      id: `sfx-${n}-${k + 1}`, kind: 'audio',
      from: F + f.at, durationInFrames: Math.min(60, TOTAL - (F + f.at)),
      asset: `sfx/${f.name}.wav`, volume: f.volume, trimStartFrames: 0,
    });
  });
});

tracks.voice.clips.push({
  id: 'voice-1', kind: 'audio', from: 0, durationInFrames: TOTAL,
  asset: 'assets/audio.mp3', volume: 1, trimStartFrames: 0,
});

const now = new Date().toISOString();
const project = {
  version: 1,
  meta: {
    name: 'okura-demo', channel: null, templateRef: null,
    fps: 30, width: 1920, height: 1080, createdAt: now, modifiedAt: now,
  },
  timeline: {durationInFrames: TOTAL},
  sceneMarkers,
  tracks: [
    tracks.background, tracks.hero, tracks.sup1, tracks.sup2,
    tracks.tag, tracks.punch, tracks.voice, tracks.sfx,
  ],
  captions: {
    source: 'none', style: 'outline', enabled: true, fontSize: 44,
    lines: [], words: [],
  },
  theme: {
    palette: {bgTop: '#2A3A58', bgBottom: '#182236', accent: '#FFD700'},
    fontFamily: '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
    canvasColor: '#F2EDE4',
  },
};

const outDir = join(ROOT, 'projects', 'okura-demo');
mkdirSync(outDir, {recursive: true});
writeFileSync(
  join(outDir, 'project.json'),
  JSON.stringify(project, null, 2),
  'utf8',
);
console.log(
  `OK projects/okura-demo/project.json — ${Object.values(tracks).reduce((a, t) => a + t.clips.length, 0)} clips / ${sceneMarkers.length} scenes`,
);
