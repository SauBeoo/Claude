// example-scene.jsx — template scene Vox-collage cho Remotion.
// CÁCH DÙNG: copy thành src/<VideoName>.jsx trong Remotion project, đổi tên
// component + 2 hằng export (EXAMPLE_* -> <VIDEONAME>_*), điền SEGMENTS bằng
// dữ liệu thật từ bước 2-5 của SKILL.md, đăng ký trong src/Root.jsx.
//
// Quy ước asset (đều nằm trong public/ của Remotion project):
//   audio.mp3            — narration
//   paper.jpg            — ảnh texture giấy làm nền (tải 1 lần / video)
//   el_*.png             — cutout đã qua process_cutout.py
//   sfx/*.wav            — output của generate_sfx.py

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

export const EXAMPLE_CANVAS = {width: 1920, height: 1080};
// = ceil(độ dài audio * 30). Đặt đúng theo audio thật.
export const EXAMPLE_TOTAL_FRAMES = 450;

const FPS = 30;

// ---------------------------------------------------------------------------
// SEGMENTS — mỗi phần tử là MỘT scene, ranh giới lấy từ segment của
// Whisper/subs.srt (KHÔNG chia đều máy móc). Mọi frame trong scene đều LOCAL
// (tính từ đầu scene); `from` là frame toàn cục scene bắt đầu.
//
// Luật khi điền:
//  - variant: không để 2 scene LIÊN TIẾP trùng nhau. 4 cái code sẵn ở đây:
//    'rise' | 'grow' | 'punch' | 'flip'. Muốn thêm (shatter/peel/unfold/
//    spiral/wobble-drop/zoom-through) đọc references/animation-variants.md.
//  - punch.appearAt = round(word.start * 30) - from  (bám đúng TỪ trong câu,
//    KHÔNG phải caption bar chạy chữ).
//  - supports: 2-4 cái, delay so le để chúng pop lần lượt; nội dung phải
//    "đúng câu" chứ không trang trí chung chung.
//  - sfx: đặt tại đúng beat (hero vào, tag pop ~frame 6, punch appearAt,
//    delay của từng support) — đừng dồn hết vào frame 0.
// ---------------------------------------------------------------------------
const SEGMENTS = [
  {
    from: 0,
    duration: 110,
    tag: '2007',
    tagColor: '#FFE01B',
    splash: ['#FF6B5E', '#4EC3E0'],
    punch: {text: 'THE TURNING POINT', appearAt: 38},
    hero: {src: 'el_phone.png', variant: 'rise', w: 1320, x: 300, y: 140},
    supports: [
      {src: 'el_globe.png', w: 380, x: 1450, y: 560, delay: 14},
      {src: 'el_chart.png', w: 420, x: 120, y: 620, delay: 24},
    ],
    sfx: [
      {name: 'whoosh', at: 0, volume: 0.45},
      {name: 'pop', at: 6, volume: 0.4},
      {name: 'paper', at: 14, volume: 0.35},
      {name: 'coin', at: 38, volume: 0.4},
    ],
  },
  // ...thêm scene, from = from + duration của scene trước
];

// --------------------------- helpers ---------------------------------------

// SFX một phát tại frame `at` (local trong scene nhờ lồng trong Sequence cha)
const Sfx = ({name, at, volume = 0.4}) => (
  <Sequence from={at} durationInFrames={60}>
    <Audio src={staticFile(`sfx/${name}.wav`)} volume={volume} />
  </Sequence>
);

// Idle motion — lắc/bồng bềnh biên độ nhỏ chạy LIÊN TỤC sau khi entrance
// xong. Thiếu cái này cutout nhìn như ảnh chết. `phase` lệch nhau giữa các
// element để chúng không bao giờ bồng bềnh đồng bộ.
const idle = (frame, phase = 0, amp = 5) => ({
  y: Math.sin(frame / 13 + phase) * amp,
  rot: Math.sin(frame / 19 + phase * 1.7) * 0.8,
});

// --------------------------- nền -------------------------------------------

const GridBackground = ({splash}) => (
  <AbsoluteFill>
    {/* ảnh giấy thật + tint — chất hơn hẳn màu CSS phẳng */}
    <Img
      src={staticFile('paper.jpg')}
      style={{width: '100%', height: '100%', objectFit: 'cover', opacity: 0.9}}
    />
    <AbsoluteFill style={{backgroundColor: '#F2EDE4', opacity: 0.55}} />
    {/* lưới graph-paper */}
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
      {/* 2 cụm halftone dots ở góc */}
      <rect x="1500" y="60" width="360" height="260" fill="url(#dots)" opacity="0.7" />
      <rect x="60" y="780" width="300" height="230" fill="url(#dots)" opacity="0.5" />
    </svg>
    {/* 2 blob màu mềm — màu đổi theo scene */}
    <div style={{position: 'absolute', left: -180, top: -220, width: 760, height: 760, borderRadius: '50%', background: splash[0], opacity: 0.30, filter: 'blur(70px)'}} />
    <div style={{position: 'absolute', right: -160, bottom: -260, width: 820, height: 820, borderRadius: '50%', background: splash[1], opacity: 0.26, filter: 'blur(80px)'}} />
  </AbsoluteFill>
);

// --------------------------- chữ --------------------------------------------

// Chip highlighter cố định cả scene (năm / con số / "?")
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
        fontFamily: 'Arial Black, sans-serif', fontSize: 74, fontWeight: 900,
        boxShadow: '6px 8px 0 rgba(0,0,0,0.28)',
      }}
    >
      {text}
    </div>
  );
};

// MỘT pull-quote / scene, hiện đúng lúc từ đó được đọc.
// ⛔ Đừng biến cái này lại thành caption bar chạy từng chữ dưới đáy —
// đó chính là lỗi "basic" mà bản draft đầu tiên dính.
const PunchPhrase = ({text, appearAt}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (frame < appearAt) return null;
  const s = spring({frame: frame - appearAt, fps, config: {damping: 13, stiffness: 200}});
  return (
    <div
      style={{
        position: 'absolute', left: 90, bottom: 110, maxWidth: 900,
        transform: `scale(${s}) rotate(-1.5deg)`, transformOrigin: 'left bottom',
        background: '#111', color: '#FFE01B', padding: '18px 30px',
        fontFamily: 'Arial Black, sans-serif', fontSize: 56, fontWeight: 900,
        lineHeight: 1.15, boxShadow: '8px 10px 0 rgba(0,0,0,0.25)',
      }}
    >
      {text}
    </div>
  );
};

// --------------------------- cutouts ----------------------------------------

// Hero — box ~1300-1350px trong khung 1920. Mỗi scene một entrance KHÁC nhau.
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
    // đập vào quá đà rồi nảy về — spring damping thấp tự lo phần overshoot
    const sp = spring({frame, fps, config: {damping: 8, stiffness: 220}});
    enter = `scale(${interpolate(sp, [0, 1], [1.7, 1])})`;
  } else if (variant === 'flip') {
    enter = `rotateY(${interpolate(s, [0, 1], [85, 0])}deg)`;
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
        }}
      />
    </div>
  );
};

// Support — 2-4 cái/scene, delay so le, phase idle lệch nhau
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
        }}
      />
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

export const ExampleCollage = () => (
  <AbsoluteFill style={{backgroundColor: '#F2EDE4'}}>
    <Audio src={staticFile('audio.mp3')} />
    {SEGMENTS.map((seg, i) => (
      <Sequence key={i} from={seg.from} durationInFrames={seg.duration}>
        <Scene seg={seg} />
      </Sequence>
    ))}
  </AbsoluteFill>
);
