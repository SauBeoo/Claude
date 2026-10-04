// YawaText.tsx — preset chữ cho kênh yawa (人生哲学の夜話): êm, chậm, chữ 明朝.
// Khán giả 50–70 NGHE nhiều hơn nhìn ⇒ chữ hiện dần như mực thấm, không pop/bật.
//
//   yawa-chapter : card chương toàn khung. content = "その四\n<tiêu đề>"
//                  số chương vàng mờ dần → gạch vàng tự kẻ → tiêu đề hiện từng chữ.
//   yawa-reveal  : câu chốt mục trên tấm giấy kem. content = các dòng tách "\n",
//                  animationParams.times = giây bắt đầu từng dòng (khớp giọng đọc).
//   yawa-chip    : chip tiến độ góc trên-trái ("その四 ／ 七"), mờ, đứng yên.
//   yawa-keyword : một cụm chữ trên dải giấy kem ở nửa trên khung, fade + trôi lên rất nhẹ.
//
// 🔴 Góc dưới-phải để trống (timestamp YouTube) · dải đáy là của phụ đề.

import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import type {z} from 'zod';
import type {TextClipSchema} from '../schema/project';
import {YAWA_SERIF, ensureYawaFont} from '../lib/yawaFont';

type TextClipT = z.infer<typeof TextClipSchema>;

const GOLD = '#F0C46E';
const CREAM = '#F6EEDE';
const INK = '#3A2E24';
const NAVY_TOP = '#282C4E';
const NAVY_BOT = '#16182E';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

/** Tách dòng dài ở dấu 、 gần giữa nhất (chữ Nhật không có khoảng trắng để wrap). */
const splitLong = (line: string, maxChars: number): string[] => {
  if (line.length <= maxChars) return [line];
  const cuts = [...line].map((c, i) => (c === '、' || c === '」' ? i + 1 : -1)).filter((i) => i > 0 && i < line.length);
  if (!cuts.length) return [line.slice(0, maxChars), ...splitLong(line.slice(maxChars), maxChars)];
  const mid = line.length / 2;
  const cut = cuts.reduce((a, b) => (Math.abs(b - mid) < Math.abs(a - mid) ? b : a));
  return [...splitLong(line.slice(0, cut), maxChars), ...splitLong(line.slice(cut), maxChars)];
};

/** Một dòng chữ hiện TỪNG KÝ TỰ: mỗi chữ fade + nhích lên `rise` px trong `each` frame. */
const InkLine: React.FC<{
  text: string;
  frame: number;
  start: number;
  stagger: number;
  each?: number;
  rise?: number;
  style: React.CSSProperties;
}> = ({text, frame, start, stagger, each = 14, rise = 7, style}) => (
  <div style={{whiteSpace: 'nowrap', ...style}}>
    {[...text].map((ch, i) => {
      const t0 = start + i * stagger;
      const p = interpolate(frame, [t0, t0 + each], [0, 1], clamp);
      return (
        <span
          key={i}
          style={{
            display: 'inline-block',
            opacity: p,
            transform: `translateY(${(1 - p) * rise}px)`,
            filter: `blur(${(1 - p) * 2.2}px)`,
          }}
        >
          {ch}
        </span>
      );
    })}
  </div>
);

export const YawaText: React.FC<{clip: TextClipT}> = ({clip}) => {
  ensureYawaFont();
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const dur = clip.durationInFrames;
  const outFade = interpolate(frame, [dur - 12, dur], [1, 0], clamp);
  const lines = clip.content.split('\n');

  // ── CARD CHƯƠNG ──────────────────────────────────────────────────────────
  if (clip.preset === 'yawa-chapter') {
    const [num, ...rest] = lines;
    const size = clip.fontSize ?? 76;
    const maxChars = Math.floor((width * 0.8) / size);
    const title = rest.flatMap((l) => splitLong(l, maxChars));
    const numP = interpolate(frame, [0, 22], [0, 1], clamp);
    const rule = interpolate(frame, [14, 46], [0, 1], clamp);
    const t0 = 34;
    const stagger = Math.max(1.6, Math.min(3, 60 / Math.max(1, title.join('').length)));
    let k = 0;
    // scrim (0..1, tuy chon — kinishinai 2026-10-02): nen navy BAN TRONG SUOT de anh that ben duoi lo ra
    // (user: "background nen xanh thay bang nen that"). Khong truyen = nen navy dac nhu cu (yawa khong doi).
    const scrim = clip.animationParams?.scrim as number | undefined;
    const fadeIn = (clip.animationParams?.fadeIn as number | undefined) ?? 12;
    const bg =
      scrim == null
        ? `linear-gradient(180deg, ${NAVY_TOP} 0%, ${NAVY_BOT} 100%)`
        : `linear-gradient(180deg, rgba(40,44,78,${scrim}) 0%, rgba(22,24,46,${Math.min(1, scrim + 0.12)}) 100%)`;
    return (
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: bg,
          fontFamily: YAWA_SERIF,
          textShadow: scrim == null ? undefined : '0 2px 14px rgba(0,0,0,0.55)',
          opacity: outFade * interpolate(frame, [0, fadeIn], [0, 1], clamp), // dissolve vào như renderer cũ
        }}
      >
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            top: height * 0.24,
            textAlign: 'center',
            color: GOLD,
            fontSize: size * 0.62,
            fontWeight: 600,
            letterSpacing: '0.18em',
            opacity: numP,
            transform: `translateY(${(1 - numP) * 10}px)`,
          }}
        >
          {num}
        </div>
        <div
          style={{
            position: 'absolute',
            left: width / 2 - 110 * rule,
            width: 220 * rule,
            top: height * 0.24 + size * 0.95,
            height: 3,
            background: GOLD,
            opacity: 0.85,
          }}
        />
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            top: height * 0.24 + size * 1.55,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: size * 0.38,
          }}
        >
          {title.map((l, i) => {
            const s = t0 + k * stagger;
            k += l.length;
            return (
              <InkLine
                key={i}
                text={l}
                frame={frame}
                start={s}
                stagger={stagger}
                style={{color: '#FFFFFF', fontSize: size, fontWeight: 500, letterSpacing: '0.06em'}}
              />
            );
          })}
        </div>
      </div>
    );
  }

  // ── CÂU CHỐT TRÊN GIẤY KEM ──────────────────────────────────────────────
  if (clip.preset === 'yawa-reveal') {
    const size = clip.fontSize ?? 62;
    const times = (clip.animationParams.times as number[] | undefined) ?? [];
    const maxChars = Math.floor(1240 / (size * 1.04));
    const panelIn = interpolate(frame, [0, 16], [0, 1], clamp);
    const rows: {text: string; start: number}[] = [];
    lines.forEach((l, li) => {
      const st = Math.round((times[li] ?? li * 2.5) * fps) + 10;
      splitLong(l, maxChars).forEach((part, pi) => {
        const prev = rows[rows.length - 1];
        rows.push({text: part, start: pi === 0 ? st : prev.start + prev.text.length * 2.2});
      });
    });
    return (
      <div style={{position: 'absolute', inset: 0, opacity: outFade, fontFamily: YAWA_SERIF}}>
        <div
          style={{
            position: 'absolute',
            left: width / 2 - 720,
            width: 1440,
            top: height * 0.42 - (rows.length * size * 1.7) / 2 - 70,
            padding: '70px 0',
            background: `${CREAM}EB`,
            borderRadius: 6,
            boxShadow: '0 18px 50px rgba(0,0,0,0.35), inset 0 0 0 1px rgba(90,70,50,0.18)',
            opacity: panelIn,
            transform: `translateY(${(1 - panelIn) * 12}px)`,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: size * 0.7,
          }}
        >
          {rows.map((r, i) => (
            <InkLine
              key={i}
              text={r.text}
              frame={frame}
              start={r.start}
              stagger={2.2}
              style={{color: INK, fontSize: size, fontWeight: 600, letterSpacing: '0.04em'}}
            />
          ))}
        </div>
      </div>
    );
  }

  // ── CHIP TIẾN ĐỘ GÓC TRÊN-TRÁI ──────────────────────────────────────────
  if (clip.preset === 'yawa-chip') {
    const p = interpolate(frame, [0, 20], [0, 1], clamp) * interpolate(frame, [dur - 20, dur], [1, 0], clamp);
    return (
      <div
        style={{
          position: 'absolute',
          left: clip.layout.x ?? 56,
          top: clip.layout.y ?? 44,
          padding: '10px 26px 12px',
          borderRadius: 40,
          background: 'rgba(22,24,46,0.55)',
          border: `1px solid ${GOLD}88`,
          color: CREAM,
          fontFamily: YAWA_SERIF,
          fontWeight: 600,
          fontSize: clip.fontSize ?? 34,
          letterSpacing: '0.12em',
          opacity: p * (clip.layout.opacity ?? 0.85),
        }}
      >
        {lines[0]}
      </div>
    );
  }

  // ── TỪ KHOÁ TRÊN DẢI GIẤY ───────────────────────────────────────────────
  if (clip.preset === 'yawa-keyword') {
    const size = clip.fontSize ?? 58;
    const p = interpolate(frame, [0, 24], [0, 1], clamp);
    const drift = interpolate(frame, [0, dur], [0, -10], clamp);
    return (
      <div
        style={{
          position: 'absolute',
          left: clip.layout.x ?? 140,
          top: (clip.layout.y ?? 150) + drift,
          padding: `${size * 0.32}px ${size * 0.7}px`,
          background: `${CREAM}E6`,
          color: INK,
          fontFamily: YAWA_SERIF,
          fontWeight: 600,
          fontSize: size,
          letterSpacing: '0.06em',
          boxShadow: '0 10px 30px rgba(0,0,0,0.30)',
          borderLeft: `6px solid ${GOLD}`,
          opacity: p * outFade,
          whiteSpace: 'nowrap',
        }}
      >
        <InkLine text={lines[0]} frame={frame} start={6} stagger={2.4} style={{}} />
      </div>
    );
  }

  // ── THẺ 古典: nền navy như card chương, câu cổ hiện chậm từng chữ, nguồn vàng hiện sau ──
  // content = "dòng1／dòng2／dòng3\n— nguồn"  (dấu ／ = chỗ xuống dòng do make_cards chốt)
  if (clip.preset === 'yawa-quote') {
    const size = clip.fontSize ?? 64;
    const rows = lines[0].split('／').map((r) => r.trim()).filter(Boolean);
    const src = lines[1] ?? '';
    const stagger = Math.max(1.8, Math.min(3.2, (dur * 0.55) / Math.max(1, rows.join('').length)));
    const total = rows.join('').length * stagger;
    const srcP = interpolate(frame, [14 + total + 6, 14 + total + 30], [0, 1], clamp);
    let k = 0;
    return (
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: `linear-gradient(180deg, ${NAVY_TOP} 0%, ${NAVY_BOT} 100%)`,
          fontFamily: YAWA_SERIF,
          opacity: outFade * interpolate(frame, [0, 12], [0, 1], clamp),
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          paddingBottom: height * 0.12,
          gap: size * 0.45,
        }}
      >
        {rows.map((r, i) => {
          const st = 14 + k * stagger;
          k += r.length;
          return (
            <InkLine key={i} text={r} frame={frame} start={st} stagger={stagger} each={18}
              style={{color: '#FFFFFF', fontSize: size, fontWeight: 500, letterSpacing: '0.08em'}} />
          );
        })}
        <div style={{marginTop: size * 0.5, color: GOLD, fontSize: size * 0.48, fontWeight: 500,
          letterSpacing: '0.1em', opacity: srcP}}>{src}</div>
      </div>
    );
  }

  // ── THẺ THƯ: giấy kem có dòng kẻ trên nền be, chữ hiện như đang viết ──
  // content = các dòng thư tách "\n"; animationParams.shown = số dòng ĐÃ hiện sẵn
  // (thẻ thư nối tiếp: thẻ sau giữ nguyên phần thẻ trước rồi viết tiếp).
  if (clip.preset === 'yawa-letter') {
    const size = clip.fontSize ?? 54;
    const shown = (clip.animationParams.shown as number | undefined) ?? 0;
    const maxChars = Math.floor(1240 / (size * 1.02));
    const rows: {text: string; pre: boolean}[] = [];
    lines.forEach((l, li) => splitLong(l, maxChars).forEach((t) => rows.push({text: t, pre: li < shown})));
    const fresh = rows.filter((r) => !r.pre).map((r) => r.text).join('').length;
    const stagger = Math.max(1.6, Math.min(3, (dur * 0.6) / Math.max(1, fresh)));
    const lineH = size * 1.9;
    let k = 0;
    return (
      <div style={{position: 'absolute', inset: 0, background: '#D6C8B0', fontFamily: YAWA_SERIF,
        // thẻ nối tiếp (shown>0) không dissolve vào, thẻ bị nối (holdOut) không tắt dần — trang thư đứng liền
        opacity: (clip.animationParams.holdOut ? 1 : outFade) * (shown > 0 ? 1 : interpolate(frame, [0, 12], [0, 1], clamp))}}>
        <div
          style={{
            position: 'absolute',
            left: width / 2 - 720,
            width: 1440,
            // mép trên CỐ ĐỊNH (không căn giữa theo số dòng): thẻ thư nối tiếp viết thêm dòng
            // thì trang giấy đứng yên, chỉ mọc dài xuống — căn giữa làm trang nhảy lên khi đổi thẻ
            top: shown > 0 || clip.animationParams.holdOut ? 130 : height * 0.44 - (rows.length * lineH) / 2 - 60,
            padding: '60px 0',
            background: '#F5EEE0',
            boxShadow: '0 16px 40px rgba(60,40,20,0.28)',
            backgroundImage: `repeating-linear-gradient(180deg, transparent 0, transparent ${lineH - 2}px, rgba(160,120,90,0.28) ${lineH - 2}px, rgba(160,120,90,0.28) ${lineH}px)`,
            backgroundPosition: '0 60px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          {rows.map((r, i) => {
            const st = r.pre ? -999 : 10 + k * stagger;
            if (!r.pre) k += r.text.length;
            return (
              <div key={i} style={{height: lineH, display: 'flex', alignItems: 'center'}}>
                <InkLine text={r.text} frame={frame} start={st} stagger={stagger} each={16}
                  style={{color: INK, fontSize: size, fontWeight: 500, letterSpacing: '0.05em'}} />
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  return null;
};
