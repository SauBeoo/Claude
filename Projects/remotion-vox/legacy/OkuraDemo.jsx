// OkuraDemo.jsx — demo 16.5s cho skill vox-collage-video.
// Nguồn audio: 16.5s đầu video health 09 (オクラ血糖値), timestamps từ subs.srt.
// 5 scene = 5 block srt, 5 entrance variant khác nhau (wobble lấy từ
// references/animation-variants.md của skill).

import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

export const OKURA_CANVAS = {width: 1920, height: 1080};
export const OKURA_TOTAL_FRAMES = 497; // 16.547s * 30fps

// ---------------------------------------------------------------------------
// SEGMENTS — ranh giới scene = ranh giới block subs.srt (frame = giây * 30)
// ---------------------------------------------------------------------------
const SEGMENTS = [
  {
    // 00.000-03.691 「オクラを、鍋のお湯でくたくたにゆでて、」
    from: 0,
    duration: 111,
    tag: 'オクラ',
    tagColor: '#FFE01B',
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
    // 03.691-06.752 「冷たい水にさらして、それから刻む。」
    from: 111,
    duration: 92,
    tag: '刻む',
    tagColor: '#4EC3E0',
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
    // 06.752-10.061 「——長年、そうしてこられた方。」
    from: 203,
    duration: 99,
    tag: '長年',
    tagColor: '#FF8C42',
    splash: ['#FF8C42', '#B8B8D1'],
    punch: {text: 'ずっと、そのやり方で。', appearAt: 42},
    hero: {src: 'el_senior.png', variant: 'flip', w: 1200, x: 360, y: 150},
    supports: [
      {src: 'el_clock.png', w: 420, x: 1440, y: 560, delay: 14},
    ],
    sfx: [
      {name: 'whoosh', at: 0, volume: 0.4},
      {name: 'pop', at: 6, volume: 0.4},
      {name: 'paper', at: 14, volume: 0.35},
      {name: 'click', at: 42, volume: 0.4},
    ],
  },
  {
    // 10.061-13.336 「じつはそれ、オクラのいちばんの宝物を、」
    from: 302,
    duration: 98,
    tag: '宝物',
    tagColor: '#2EC46F',
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
    // 13.336-16.547 「お湯と流しに、捨てているかもしれません。」
    from: 400,
    duration: 97,
    tag: '？',
    tagColor: '#FF5E5B',
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

// --------------------------- helpers ---------------------------------------

const Sfx = ({name, at, volume = 0.4}) => (
  <Sequence from={at} durationInFrames={60}>
    <Audio src={staticFile(`sfx/${name}.wav`)} volume={volume} />
  </Sequence>
);

const idle = (frame, phase = 0, amp = 5) => ({
  y: Math.sin(frame / 13 + phase) * amp,
  rot: Math.sin(frame / 19 + phase * 1.7) * 0.8,
});

// --------------------------- nền -------------------------------------------

const GridBackground = ({splash}) => (
  <AbsoluteFill>
    <Img
      src={staticFile('paper.jpg')}
      style={{width: '100%', height: '100%', objectFit: 'cover', opacity: 0.9}}
    />
    <AbsoluteFill style={{backgroundColor: '#F2EDE4', opacity: 0.55}} />
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <defs>
        <pattern id="grid" width="72" height="72" patternUnits="userSpaceOnUse">
          <path d="M72 0H0V72" fill="none" stroke="#1a1a1a" strokeOpacity="0.10" strokeWidth="1.5" />
        </pattern>
        <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">
          <circle cx="4" cy="4" r="3.2" fill="#1a1a1a" fillOpacity="0.16" />
        </pattern>
      </defs>
      <rect width="1920" height="1080" fill="url(#grid)" />
      <rect x="1500" y="60" width="360" height="260" fill="url(#dots)" opacity="0.7" />
      <rect x="60" y="780" width="300" height="230" fill="url(#dots)" opacity="0.5" />
    </svg>
    <div style={{position: 'absolute', left: -180, top: -220, width: 760, height: 760, borderRadius: '50%', background: splash[0], opacity: 0.30, filter: 'blur(70px)'}} />
    <div style={{position: 'absolute', right: -160, bottom: -260, width: 820, height: 820, borderRadius: '50%', background: splash[1], opacity: 0.26, filter: 'blur(80px)'}} />
  </AbsoluteFill>
);

// --------------------------- chữ --------------------------------------------

const TitleTag = ({text, color, variant}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: frame - 4, fps, config: {damping: 11, stiffness: 180}});
  const rot = variant === 'flip' ? interpolate(s, [0, 1], [12, -2]) : -2;
  return (
    <div
      style={{
        position: 'absolute', left: 90, top: 70,
        transform: `scale(${s}) rotate(${rot}deg)`,
        transformOrigin: 'left center',
        background: color, color: '#111', padding: '14px 34px',
        fontFamily: '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
        fontSize: 74, fontWeight: 900,
        boxShadow: '6px 8px 0 rgba(0,0,0,0.28)',
      }}
    >
      {text}
    </div>
  );
};

const PunchPhrase = ({text, appearAt}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (frame < appearAt) return null;
  const s = spring({frame: frame - appearAt, fps, config: {damping: 13, stiffness: 200}});
  return (
    <div
      style={{
        position: 'absolute', left: 90, bottom: 110, maxWidth: 980,
        transform: `scale(${s}) rotate(-1.5deg)`, transformOrigin: 'left bottom',
        background: '#111', color: '#FFE01B', padding: '18px 30px',
        fontFamily: '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
        fontSize: 56, fontWeight: 900, lineHeight: 1.15,
        boxShadow: '8px 10px 0 rgba(0,0,0,0.25)',
      }}
    >
      {text}
    </div>
  );
};

// --------------------------- cutouts ----------------------------------------

const Cutout = ({src, variant, w, x, y}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 12, stiffness: 130}});
  const bob = idle(frame, 0, 6);

  let enter = '';
  if (variant === 'rise') {
    enter = `translateY(${interpolate(s, [0, 1], [420, 0])}px)`;
  } else if (variant === 'grow') {
    enter = `scale(${interpolate(s, [0, 1], [0.25, 1])})`;
  } else if (variant === 'punch') {
    const sp = spring({frame, fps, config: {damping: 8, stiffness: 220}});
    enter = `scale(${interpolate(sp, [0, 1], [1.7, 1])})`;
  } else if (variant === 'flip') {
    enter = `rotateY(${interpolate(s, [0, 1], [85, 0])}deg)`;
  } else if (variant === 'wobble') {
    // wobble-drop từ references/animation-variants.md: rơi spring damping thấp
    // (tự nảy) + rotate sin tắt dần
    const sp = spring({frame, fps, config: {damping: 6.5, stiffness: 160}});
    const wob = Math.sin(frame / 2.2) * 14 * Math.exp(-frame / 12);
    enter = `translateY(${interpolate(sp, [0, 1], [-500, 0])}px) rotate(${wob}deg)`;
  }

  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, perspective: 1200}}>
      <Img
        src={staticFile(src)}
        style={{
          width: '100%',
          opacity: interpolate(s, [0, 0.25], [0, 1], {extrapolateRight: 'clamp'}),
          transform: `${enter} translateY(${bob.y}px) rotate(${bob.rot}deg)`,
          filter: 'drop-shadow(10px 14px 0 rgba(0,0,0,0.22))',
          translate: "6.9px -46.4px",
          rotate: "-1.2deg"
        }}
      />
    </div>
  );
};

const SupportElement = ({src, w, x, y, delay, index}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (frame < delay) return null;
  const s = spring({frame: frame - delay, fps, config: {damping: 10, stiffness: 190}});
  const bob = idle(frame, 2.1 * (index + 1), 4);
  const tilt = index % 2 ? 4 : -5;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w}}>
      <Img
        src={staticFile(src)}
        style={{
          width: '100%',
          transform: `scale(${s}) rotate(${tilt + bob.rot}deg) translateY(${bob.y}px)`,
          filter: 'drop-shadow(6px 8px 0 rgba(0,0,0,0.20))',
          translate: "-15.4px 8.7px",
          scale: 0.924,
          rotate: "10.4deg"
        }}
        from={-1} />
    </div>
  );
};

// --------------------------- scene + root -----------------------------------

const Scene = ({seg}) => (
  <AbsoluteFill>
    <GridBackground splash={seg.splash} />
    <Cutout {...seg.hero} />
    {seg.supports.map((sp, i) => (
      <SupportElement key={i} index={i} {...sp} />
    ))}
    <TitleTag text={seg.tag} color={seg.tagColor} variant={seg.hero.variant} />
    <PunchPhrase {...seg.punch} />
    {seg.sfx.map((f, i) => (
      <Sfx key={i} {...f} />
    ))}
  </AbsoluteFill>
);

export const OkuraDemo = () => (
  <AbsoluteFill style={{backgroundColor: '#F2EDE4'}}>
    <Audio src={staticFile('audio.mp3')} />
    {SEGMENTS.map((seg, i) => (
      <Sequence key={i} from={seg.from} durationInFrames={seg.duration}>
        <Scene seg={seg} />
      </Sequence>
    ))}
  </AbsoluteFill>
);
