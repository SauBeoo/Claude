// KinText.tsx — preset chữ cho kênh kinishinai (他人の目を気にしない心理学), khán giả 60+.
// Khuôn từ video mẫu ku8qF5wrFxg (介護保険料): chip chương góc trên-trái, ô chữ từ khoá bên trái,
// dòng 出典 nhỏ, thẻ số hiện dần. CHỈ fade (12 frame), không bay/nảy — bài học nenkin v26
// (Remotion nhiều động → MAD 9,97, mẫu thắng 1,06–4,28).
//
//   kin-chip    : content = "その一\n「すみません」" — nhãn navy + tiêu đề trên nền trắng, góc trên-trái.
//   kin-callout : content = 1–2 dòng — hộp trắng + vạch đồng bên trái; CÙNG kiểu ô chữ đã bake trong
//                 clip người dẫn (youtube-jp-kinishinai/tools/host_insert_01.py::callout).
//   kin-source  : content = "出典：…" — chữ nhỏ trên viên thuốc trắng mờ, trái, trên dải phụ đề.
//   kin-stat    : thẻ số. content = "dòng trên\nTRƯỚC|SAU\ndòng dưới"; animationParams.times = giây
//                 (tính từ đầu clip) bật [dòng trên, TRƯỚC, mũi tên+SAU, dòng dưới]. Nền = chính nền
//                 thẻ PIL của kênh (public/shared/kinishinai/card_bg.png) ⇒ đè khít thẻ cũ.
//
// 🔴 Mọi thứ nằm trên y < 790 (phụ đề 2 dòng cháy sẵn bắt đầu y≈796) · góc dưới-phải để trống.

import React from 'react';
import {Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {z} from 'zod';
import type {TextClipSchema} from '../schema/project';

type TextClipT = z.infer<typeof TextClipSchema>;

const SANS = '"Yu Gothic", "YuGothic", "Meiryo", sans-serif';
const INK = '#243048';
const BLUE = '#427CB0';
const BRONZE = '#B07834';
const GREY = '#5A6170';
const SUB_TOP = 790;
const FADE = 12;
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

const useFade = (): number => {
  const f = useCurrentFrame();
  const {durationInFrames: d} = useVideoConfig();
  return Math.min(interpolate(f, [0, FADE], [0, 1], clamp), interpolate(f, [d - FADE, d], [1, 0], clamp));
};

const Chip: React.FC<{clip: TextClipT}> = ({clip}) => {
  const op = useFade();
  const [label = '', title = ''] = clip.content.split('\n');
  const size = clip.fontSize ?? 34;
  return (
    <div style={{position: 'absolute', left: clip.layout.x ?? 36, top: clip.layout.y ?? 28, opacity: op,
      display: 'flex', alignItems: 'stretch', fontFamily: SANS, fontWeight: 700,
      boxShadow: '0 3px 10px rgba(0,0,0,0.18)', borderRadius: 10, overflow: 'hidden'}}>
      <div style={{background: INK, color: '#FFFFFF', fontSize: size * 0.8, padding: `${size * 0.28}px ${size * 0.5}px`,
        display: 'flex', alignItems: 'center'}}>{label}</div>
      <div style={{background: 'rgba(255,255,255,0.94)', color: INK, fontSize: size,
        padding: `${size * 0.22}px ${size * 0.6}px`, display: 'flex', alignItems: 'center'}}>{title}</div>
    </div>
  );
};

const Callout: React.FC<{clip: TextClipT}> = ({clip}) => {
  const op = useFade();
  const lines = clip.content.split('\n');
  const size = clip.fontSize ?? 64;
  return (
    <div style={{position: 'absolute', left: clip.layout.x ?? 96, top: clip.layout.y ?? 300, opacity: op,
      background: 'rgba(255,255,255,0.93)', borderRadius: 22, padding: `${size * 0.47}px ${size * 0.75}px`,
      paddingLeft: size * 0.75 + 10, boxShadow: '6px 8px 0 rgba(0,0,0,0.12)', fontFamily: SANS,
      fontWeight: 700, color: INK, fontSize: size, lineHeight: 1.35, maxWidth: clip.layout.w ?? 820}}>
      <div style={{position: 'absolute', left: 0, top: 18, bottom: 18, width: 10, background: BRONZE}} />
      {lines.map((l, i) => <div key={i} style={{whiteSpace: 'nowrap'}}>{l}</div>)}
    </div>
  );
};

const Source: React.FC<{clip: TextClipT}> = ({clip}) => {
  const op = useFade();
  const size = clip.fontSize ?? 24;
  return (
    <div style={{position: 'absolute', left: clip.layout.x ?? 96, top: clip.layout.y ?? SUB_TOP - 66, opacity: op,
      background: 'rgba(255,255,255,0.82)', borderRadius: 999, padding: `${size * 0.3}px ${size * 0.8}px`,
      fontFamily: SANS, fontWeight: 700, fontSize: size, color: GREY, whiteSpace: 'nowrap'}}>{clip.content}</div>
  );
};

const Stat: React.FC<{clip: TextClipT}> = ({clip}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const op = useFade();
  const [top = '', pair = '', bottom = ''] = clip.content.split('\n');
  const [before = '', after = ''] = pair.split('|');
  const ts = ((clip.animationParams.times as number[] | undefined) ?? [0.2, 0.9, 2.0, 3.0]).map((s) => s * fps);
  const show = (k: number) => interpolate(f, [ts[k], ts[k] + FADE], [0, 1], clamp);
  const arrow = interpolate(f, [ts[2], ts[2] + 18], [0, 1], clamp);
  const hero = clip.fontSize ?? 150;
  return (
    <div style={{position: 'absolute', inset: 0, opacity: op}}>
      {/* nen the cua kenh, chi tren dai phu de — phu de chay san ben duoi van thay */}
      <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: SUB_TOP, overflow: 'hidden'}}>
        <Img src={staticFile('shared/kinishinai/card_bg.png')} style={{width: 1920, height: 1080}} />
      </div>
      <div style={{position: 'absolute', left: 160, width: 1600, top: 150, textAlign: 'center', fontFamily: SANS,
        fontWeight: 700, fontSize: 62, color: INK, opacity: show(0)}}>{top}</div>
      <div style={{position: 'absolute', left: 160, width: 1600, top: 300, display: 'flex', justifyContent: 'center',
        alignItems: 'center', gap: 56, fontFamily: SANS, fontWeight: 800}}>
        <span style={{fontSize: hero * 0.78, color: GREY, opacity: show(1)}}>{before}</span>
        <svg width={170} height={80} style={{opacity: arrow > 0 ? 1 : 0}}>
          <line x1={8} y1={40} x2={8 + 130 * arrow} y2={40} stroke={BLUE} strokeWidth={12} strokeLinecap="round" />
          {arrow > 0.95 ? <polygon points="132,12 166,40 132,68" fill={BLUE} /> : null}
        </svg>
        <span style={{fontSize: hero, color: BLUE, opacity: show(2),
          borderBottom: `10px solid ${BRONZE}`, paddingBottom: 6}}>{after}</span>
      </div>
      <div style={{position: 'absolute', left: 160, width: 1600, top: 560, textAlign: 'center', fontFamily: SANS,
        fontWeight: 700, fontSize: 54, color: INK, opacity: show(3)}}>{bottom}</div>
    </div>
  );
};

export const KinText: React.FC<{clip: TextClipT}> = ({clip}) => {
  switch (clip.preset) {
    case 'kin-chip':
      return <Chip clip={clip} />;
    case 'kin-callout':
      return <Callout clip={clip} />;
    case 'kin-source':
      return <Source clip={clip} />;
    case 'kin-stat':
      return <Stat clip={clip} />;
    default:
      return null;
  }
};
