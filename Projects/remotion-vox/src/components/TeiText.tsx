// TeiText.tsx — preset chữ cho kênh teinengo (定年後のこころ研究室), khán giả 60+.
// User chốt 2026-10-01: "chữ chạy từng chữ / từng câu · có mũi tên thì mũi tên hiện dần ·
// NÓI ĐẾN ĐÂU HIỂN THỊ ĐẾN ĐÓ · chữ có nền phải MỀM, không thô".
//
//   tei-label  : nhãn VỆT BÚT LÔNG (sumi) + chữ 明朝 trắng (user chọn kiểu 5, 2026-10-01; viên thuốc bo
//                tròn bị chê "nhìn như button"). Vệt bút quét trái->phải 14 frame rồi chữ mới hiện.
//                color = màu vệt. Hình vệt tiền định theo nội dung (hash) — không random mỗi frame.
//   tei-reveal : khối chữ hiện THEO LỜI ĐỌC. Builder tính mốc từ mora VOICEVOX rồi truyền vào
//                animationParams.lines = [[run, run, …], …] (mỗi phần tử = một dòng), với
//                  run = {t: "九時", a: 1.20, b: 1.62, hot?: true}  → chữ hiện LẦN LƯỢT từ a tới b (giây,
//                        tính từ đầu clip), mỗi ký tự mờ dần vào trong 5 frame.
//                  run = {arrow: true, a: 1.62, b: 2.10}          → mũi tên tự vẽ từ trái sang phải.
//                animationParams.box = true → đặt khối trên tấm nền mờ bo góc (mềm, không viền cứng).
//                color = màu nhấn cho run có hot.
//
// 🔴 Không nảy, không bay: tệp 60+ (bài học nenkin v26 MAD 9,97). Chỉ opacity + nhích 6px.

import React from 'react';
import {continueRender, delayRender, Easing, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {z} from 'zod';
import type {TextClipSchema} from '../schema/project';

type TextClipT = z.infer<typeof TextClipSchema>;
type Run = {t?: string; a: number; b: number; hot?: boolean; arrow?: boolean};

const SANS = '"Yu Gothic", "YuGothic", "Meiryo", sans-serif';
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const CHAR_FADE = 5; // frames

const useClipFade = (fadeOut = 10): number => {
  const f = useCurrentFrame();
  const {durationInFrames: d} = useVideoConfig();
  return interpolate(f, [d - fadeOut, d], [1, 0], clamp);
};

const shade = (hex: string, k: number): string => {
  const m = /^#([0-9a-fA-F]{6})$/.exec(hex.trim());
  if (!m) return hex;
  const n = parseInt(m[1], 16);
  const c = [(n >> 16) & 255, (n >> 8) & 255, n & 255].map((v) =>
    Math.max(0, Math.min(255, Math.round(k >= 1 ? v + (255 - v) * (k - 1) : v * k)))
  );
  return `rgb(${c[0]},${c[1]},${c[2]})`;
};

// ── font 明朝 cho nhãn: Noto Serif JP variable (OFL), chặn render tới khi nạp xong ──
const TEI_SERIF = '"TeiSerif", "Yu Mincho", "YuMincho", serif';
let fontStarted = false;
const ensureTeiFont = (): void => {
  if (fontStarted || typeof document === 'undefined') return;
  fontStarted = true;
  const h = delayRender('load TeiSerif');
  const face = new FontFace('TeiSerif', `url(${staticFile('shared/fonts/NotoSerifJP-VF.ttf')})`, {weight: '200 900'});
  face
    .load()
    .then((ff) => {
      document.fonts.add(ff);
      continueRender(h);
    })
    .catch((err) => {
      console.error('TeiSerif load failed', err);
      continueRender(h);
    });
};

// hash tiền định → số giả ngẫu nhiên ổn định theo (nội dung, chỉ số)
const hrand = (seed: string, i: number): number => {
  let x = 2166136261;
  for (const ch of seed + ':' + i) x = Math.imul(x ^ ch.charCodeAt(0), 16777619);
  return ((x >>> 0) % 10000) / 10000;
};

const Label: React.FC<{clip: TextClipT}> = ({clip}) => {
  ensureTeiFont();
  const f = useCurrentFrame();
  const out = useClipFade();
  const size = clip.fontSize ?? 62;
  const ink = (clip.animationParams?.ink as string) ?? '#FFFFFF';
  const chars = Array.from(clip.content).length;
  const textW = chars * size * 1.02;
  const padX = size * 0.8;
  const W = textW + padX * 2;
  const Hh = size * 1.32;
  const seed = clip.content + clip.color;
  // mép trên/dưới răng cưa nhẹ, hai đầu vát xiên như nét cọ
  const N = 34;
  const top: string[] = [];
  const bot: string[] = [];
  for (let i = 0; i <= N; i++) {
    const x = size * 0.35 + ((W - size * 0.55) * i) / N;
    top.push(`${x.toFixed(1)},${(size * 0.12 + (hrand(seed, i) - 0.5) * size * 0.1).toFixed(1)}`);
    const xb = W - size * 0.3 - ((W - size * 0.5) * i) / N;
    bot.push(`${xb.toFixed(1)},${(Hh - size * 0.1 + (hrand(seed, 100 + i) - 0.5) * size * 0.1).toFixed(1)}`);
  }
  const pts = [
    `${size * 0.05},${Hh * 0.42}`,
    ...top,
    `${W},${Hh * 0.3}`,
    `${W - size * 0.12},${Hh * 0.62}`,
    ...bot,
    `${size * 0.12},${Hh * 0.8}`,
  ].join(' ');
  // vệt khô của cọ: vài dải ngang mờ hơn
  const streaks = Array.from({length: 7}, (_, k) => ({
    y: Hh * (0.12 + 0.12 * k + (hrand(seed, 300 + k) - 0.5) * 0.05),
    h: Hh * (0.02 + hrand(seed, 400 + k) * 0.035),
    x0: W * hrand(seed, 500 + k) * 0.35,
    w: W * (0.35 + hrand(seed, 600 + k) * 0.6),
  }));
  const sweep = interpolate(f, [0, 14], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const textOp = interpolate(f, [8, 18], [0, 1], clamp) * out;
  const id = `tb_${Math.round(hrand(seed, 999) * 1e6)}`;
  const boxW = clip.layout.w;
  return (
    <div
      style={{
        position: 'absolute',
        left: clip.layout.x ?? 90,
        top: clip.layout.y ?? 60,
        width: boxW,
        display: 'flex',
        justifyContent: boxW ? 'center' : undefined,
        opacity: out,
      }}
    >
      <div style={{position: 'relative', width: W, height: Hh}}>
        <svg width={W} height={Hh} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
          <defs>
            <filter id={`${id}_r`} x="-5%" y="-20%" width="110%" height="140%">
              <feTurbulence type="fractalNoise" baseFrequency="0.035 0.6" numOctaves="2" seed={Math.round(hrand(seed, 7) * 90)} />
              <feDisplacementMap in="SourceGraphic" scale={size * 0.09} />
            </filter>
            <clipPath id={`${id}_c`}>
              <rect x={0} y={-20} width={W * sweep + 2} height={Hh + 40} />
            </clipPath>
            <mask id={`${id}_m`}>
              <rect x={0} y={0} width={W} height={Hh} fill="white" />
              {streaks.map((s, k) => (
                <rect key={k} x={s.x0} y={s.y} width={s.w} height={s.h} fill="black" opacity={0.28} />
              ))}
            </mask>
          </defs>
          <g clipPath={`url(#${id}_c)`} filter={`url(#${id}_r)`}>
            <polygon points={pts} fill={clip.color} opacity={0.88} mask={`url(#${id}_m)`} />
          </g>
        </svg>
        <div
          style={{
            position: 'absolute',
            left: 0,
            top: 0,
            width: W,
            height: Hh,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontFamily: TEI_SERIF,
            fontWeight: 800,
            fontSize: size,
            color: ink,
            letterSpacing: '0.02em',
            whiteSpace: 'nowrap',
            opacity: textOp,
            textShadow: '0 3px 8px rgba(0,0,0,0.35)',
          }}
        >
          {clip.content}
        </div>
      </div>
    </div>
  );
};

const Arrow: React.FC<{p: number; size: number; color: string}> = ({p, size, color}) => {
  const w = size * 1.5;
  const h = size * 0.7;
  const len = w - size * 0.25;
  return (
    <svg width={w} height={h} style={{margin: `0 ${size * 0.18}px`, overflow: 'visible'}}>
      <line
        x1={size * 0.05}
        y1={h / 2}
        x2={size * 0.05 + len * p}
        y2={h / 2}
        stroke={color}
        strokeWidth={size * 0.11}
        strokeLinecap="round"
        style={{filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.45))'}}
      />
      {p > 0.85 && (
        <polyline
          points={`${size * 0.05 + len - size * 0.32},${h / 2 - size * 0.26} ${size * 0.05 + len},${h / 2} ${
            size * 0.05 + len - size * 0.32
          },${h / 2 + size * 0.26}`}
          fill="none"
          stroke={color}
          strokeWidth={size * 0.11}
          strokeLinecap="round"
          strokeLinejoin="round"
          opacity={interpolate(p, [0.85, 1], [0, 1], clamp)}
          style={{filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.45))'}}
        />
      )}
    </svg>
  );
};

const Reveal: React.FC<{clip: TextClipT}> = ({clip}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const out = useClipFade();
  const size = clip.fontSize ?? 76;
  const lines = (clip.animationParams?.lines as Run[][]) ?? [[{t: clip.content, a: 0, b: 0.6}]];
  const box = Boolean(clip.animationParams?.box);
  const ink = (clip.animationParams?.ink as string) ?? '#FFFFFF';
  const first = Math.min(...lines.flat().map((r) => r.a));
  const boxOp = interpolate(f, [first * fps - 6, first * fps + 6], [0, 1], clamp);

  const glyphStyle = (hot: boolean, op: number, dy: number): React.CSSProperties => ({
    display: 'inline-block',
    opacity: op,
    transform: `translateY(${dy}px)`,
    color: hot ? clip.color : ink,
    fontSize: size,
    fontWeight: 800,
    // viền MỀM: mảnh + bóng mờ, không phải viền đen dày 14px của telop
    WebkitTextStrokeWidth: box ? 0 : `${Math.max(3, Math.round(size * 0.06))}px`,
    WebkitTextStrokeColor: 'rgba(20,16,12,0.85)',
    paintOrder: 'stroke fill',
    textShadow: '0 3px 10px rgba(0,0,0,0.45)',
  });

  return (
    <div
      style={{
        position: 'absolute',
        left: clip.layout.x ?? 90,
        top: clip.layout.y ?? 80,
        opacity: out,
        fontFamily: SANS,
        lineHeight: 1.25,
      }}
    >
      {box && (
        <div
          style={{
            position: 'absolute',
            inset: `${-size * 0.32}px ${-size * 0.5}px`,
            borderRadius: size * 0.42,
            background: 'rgba(24,22,20,0.42)',
            backdropFilter: 'blur(10px)',
            boxShadow: '0 12px 36px rgba(0,0,0,0.25)',
            opacity: boxOp,
          }}
        />
      )}
      <div style={{position: 'relative'}}>
        {lines.map((runs, li) => (
          <div key={li} style={{display: 'flex', alignItems: 'center', whiteSpace: 'nowrap'}}>
            {runs.map((r, ri) => {
              if (r.arrow) {
                const p = interpolate(f, [r.a * fps, Math.max(r.a * fps + 1, r.b * fps)], [0, 1], clamp);
                return <Arrow key={ri} p={p} size={size} color={ink} />;
              }
              const chars = Array.from(r.t ?? '');
              const step = chars.length > 1 ? ((r.b - r.a) * fps) / chars.length : 0;
              return (
                <span key={ri}>
                  {chars.map((ch, ci) => {
                    const s = r.a * fps + ci * step;
                    const op = interpolate(f, [s, s + CHAR_FADE], [0, 1], clamp);
                    const dy = interpolate(f, [s, s + CHAR_FADE], [6, 0], clamp);
                    return (
                      <span key={ci} style={glyphStyle(Boolean(r.hot), op, dy)}>
                        {ch}
                      </span>
                    );
                  })}
                </span>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
};

export const TeiText: React.FC<{clip: TextClipT}> = ({clip}) => {
  if (clip.preset === 'tei-label') return <Label clip={clip} />;
  return <Reveal clip={clip} />;
};
