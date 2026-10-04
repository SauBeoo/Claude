// FxLayer.tsx — lớp trang trí "hoa lá cành": đồng xu bay · sparkle · mũi tên
// phát sáng · 集中線 · quầng sáng · confetti.
//
// VÌ SAO CÓ FILE NÀY (đọc trước khi sửa):
// Bản mẫu cùng ngách BAKE mấy thứ này vào chính ảnh AI. Mình không làm được thế:
// footage của mình là **video AI (Veo)**, mà Veo không đặt được mũi tên đúng chỗ và
// không viết được chữ. Nên lớp này do Remotion vẽ — và đó lại là cái LỢI: xu bay
// THẬT (mẫu chỉ có xu đứng yên trong ảnh tĩnh), sửa được mà không phải gen lại.
//
// 🔴 LUẬT SỐ MỘT: MỌI thứ "ngẫu nhiên" phải TIỀN ĐỊNH theo (seed, index).
//    Remotion render từng frame trong một tiến trình độc lập ⇒ `Math.random()` cho
//    mỗi frame một giá trị khác ⇒ hạt nhảy loạn xạ. Đây là đúng cái bẫy đã dính ở
//    `papercut` (mép giấy rung mỗi frame) — xem CLAUDE.md nenkin §②.
//
// 🔴 LUẬT SỐ HAI: hạt phải chạy theo `frame`, KHÔNG theo `Date.now()` / animation CSS.
//    CSS animation không đồng bộ với timeline render, ra video giật.

import React from 'react';
import {useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import type {z} from 'zod';
import type {FxClipSchema} from '../schema/project';

type FxT = z.infer<typeof FxClipSchema>;

// PRNG tiền định: cùng (seed, i, salt) luôn ra cùng số trong [0,1).
// Dùng phép nhân số nguyên 32-bit của Knuth — rẻ và phân bố đủ đều cho hạt trang trí.
const rnd = (seed: number, i: number, salt: number): number => {
  let h = (seed * 374761393 + i * 668265263 + salt * 2654435761) >>> 0;
  h = (h ^ (h >>> 13)) >>> 0;
  h = (h * 1274126177) >>> 0;
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
};

export const FxLayer: React.FC<{clip: FxT}> = ({clip}) => {
  const frame = useCurrentFrame();
  const {width, height, fps} = useVideoConfig();
  const dur = clip.durationInFrames;

  // fade vào/ra để lớp không bật-tắt phần phật — tệp 45+ rất phạt cái đó
  const fade =
    interpolate(frame, [0, Math.max(1, clip.fadeInFrames)], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    }) *
    interpolate(frame, [dur - Math.max(1, clip.fadeOutFrames), dur], [1, 0], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });

  const box: React.CSSProperties = {
    position: 'absolute',
    left: `${clip.area.x}%`,
    top: `${clip.area.y}%`,
    width: `${clip.area.w}%`,
    height: `${clip.area.h}%`,
    pointerEvents: 'none',
    opacity: fade * clip.opacity,
    overflow: 'visible',
  };

  const AW = (width * clip.area.w) / 100;
  const AH = (height * clip.area.h) / 100;

  // ── ĐỒNG XU VÀNG BAY ─────────────────────────────────────────────────────
  // Mẫu có xu vàng rải quanh khung nhưng ĐỨNG YÊN (nó là ảnh tĩnh). Ở đây xu
  // trôi lên + xoay quanh trục dọc (scaleX dao động = mặt xu nghiêng đi).
  if (clip.variant === 'coins') {
    return (
      <div style={box}>
        {Array.from({length: clip.density}).map((_, i) => {
          const x = rnd(clip.seed, i, 1) * AW;
          const size = AH * (0.075 + rnd(clip.seed, i, 2) * 0.065);
          const speed = 0.35 + rnd(clip.seed, i, 3) * 0.5; // vòng đời/giây
          const phase = rnd(clip.seed, i, 4);
          // t chạy 0→1 lặp lại: xu đi từ dưới đáy vùng lên quá đỉnh rồi quay lại
          const t = ((frame / fps) * speed * 0.35 + phase) % 1;
          const y = AH * 1.05 - t * AH * 1.25;
          // lắc ngang nhẹ theo sin để không rơi thẳng đơ như hạt mưa
          const sway = Math.sin((t + phase) * Math.PI * 2 * 1.5) * AW * 0.03;
          // mặt xu nghiêng: scaleX chạy quanh vòng tròn -> xu "xoay"
          const spin = Math.cos(((frame / fps) * (1.1 + phase) + phase) * Math.PI * 2);
          const flat = Math.max(0.12, Math.abs(spin));
          // mờ dần ở hai đầu vòng đời để không thấy xu "chớp" hiện/biến
          const lifeFade = Math.min(1, t / 0.12, (1 - t) / 0.15);
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: x + sway,
                top: y,
                width: size,
                height: size,
                opacity: lifeFade * (0.55 + rnd(clip.seed, i, 5) * 0.45),
                transform: `scaleX(${flat})`,
              }}
            >
              <svg viewBox="0 0 100 100" width="100%" height="100%">
                <defs>
                  <radialGradient id={`cg${clip.id}${i}`} cx="35%" cy="30%">
                    <stop offset="0%" stopColor="#FFF6C9" />
                    <stop offset="45%" stopColor={clip.color} />
                    <stop offset="100%" stopColor="#B87A0E" />
                  </radialGradient>
                </defs>
                <circle cx="50" cy="50" r="48" fill={`url(#cg${clip.id}${i})`} />
                <circle
                  cx="50"
                  cy="50"
                  r="38"
                  fill="none"
                  stroke="#FFF0B0"
                  strokeWidth="5"
                  opacity="0.75"
                />
                {/* đốm sáng lệch tâm = cảm giác kim loại, không phải cái đĩa phẳng */}
                <ellipse cx="35" cy="30" rx="14" ry="9" fill="#FFFDF0" opacity="0.8" />
              </svg>
            </div>
          );
        })}
      </div>
    );
  }

  // ── SPARKLE: sao 4 cánh lấp lánh ─────────────────────────────────────────
  if (clip.variant === 'sparkle') {
    return (
      <div style={box}>
        {Array.from({length: clip.density}).map((_, i) => {
          const x = rnd(clip.seed, i, 11) * AW;
          const y = rnd(clip.seed, i, 12) * AH;
          const size = AH * (0.03 + rnd(clip.seed, i, 13) * 0.06);
          const per = 0.9 + rnd(clip.seed, i, 14) * 1.4; // chu kỳ nháy (giây)
          const ph = rnd(clip.seed, i, 15);
          // nháy: dùng luỹ thừa 3 để đa số thời gian sao MỜ, chỉ loé lên ngắn —
          // nháy đều nhau thì ra "đèn nhấp nháy", không ra "lấp lánh"
          const k = Math.pow(
            Math.max(0, Math.sin(((frame / fps) / per + ph) * Math.PI * 2)),
            3
          );
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: x - size / 2,
                top: y - size / 2,
                width: size,
                height: size,
                opacity: k,
                transform: `rotate(${rnd(clip.seed, i, 16) * 90}deg) scale(${0.6 + k * 0.6})`,
              }}
            >
              <svg viewBox="-50 -50 100 100" width="100%" height="100%">
                {/* hình sao 4 cánh vẽ bằng 4 đường cong lõm — không dùng ngôi sao 5 cánh */}
                <path
                  d="M0,-50 Q6,-6 50,0 Q6,6 0,50 Q-6,6 -50,0 Q-6,-6 0,-50 Z"
                  fill={clip.color}
                />
                <circle cx="0" cy="0" r="7" fill="#FFFFFF" opacity="0.9" />
              </svg>
            </div>
          );
        })}
      </div>
    );
  }

  // ── MŨI TÊN LỚN PHÁT SÁNG (đỏ → vàng) ────────────────────────────────────
  // Bản mẫu khung 240s: mũi tên đỏ-vàng cong vút lên, có glow, chiếm ~nửa khung.
  // Ở đây nó ĐƯỢC VẼ RA (stroke-dashoffset) trong ~0,8s rồi đứng — chuyển động
  // "đang tăng lên" mạnh hơn hẳn một mũi tên đứng sẵn.
  if (clip.variant === 'arrow') {
    const draw = interpolate(frame, [0, Math.round(fps * 0.8)], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
      easing: (x) => 1 - Math.pow(1 - x, 3),
    });
    const rot =
      clip.dir === 'up' ? -90 : clip.dir === 'right' ? 0 : clip.dir === 'down' ? 90 : -38;
    const L = 620; // chiều dài đường cong trong hệ toạ độ viewBox
    return (
      <div style={{...box, transform: `rotate(${rot}deg)`, transformOrigin: '50% 50%'}}>
        <svg viewBox="0 0 500 300" width="100%" height="100%" style={{overflow: 'visible'}}>
          <defs>
            <linearGradient id={`ag${clip.id}`} x1="0" y1="1" x2="1" y2="0">
              <stop offset="0%" stopColor="#D6202A" />
              <stop offset="55%" stopColor="#FF6A2B" />
              <stop offset="100%" stopColor={clip.color} />
            </linearGradient>
            <filter id={`af${clip.id}`} x="-40%" y="-40%" width="180%" height="180%">
              <feGaussianBlur stdDeviation="10" result="b" />
              <feMerge>
                <feMergeNode in="b" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>
          <g filter={`url(#af${clip.id})`}>
            <path
              d="M40,265 C170,250 300,190 420,55"
              fill="none"
              stroke={`url(#ag${clip.id})`}
              strokeWidth="46"
              strokeLinecap="round"
              strokeDasharray={L}
              strokeDashoffset={L * (1 - draw)}
            />
            {/* đầu mũi tên chỉ hiện khi thân đã vẽ gần xong */}
            <path
              d="M420,55 L352,86 L404,116 Z"
              fill={clip.color}
              opacity={interpolate(draw, [0.8, 1], [0, 1], {extrapolateLeft: 'clamp'})}
              transform="translate(18,-14) rotate(-4 420 55) scale(1.55) translate(-152,-20)"
            />
          </g>
        </svg>
      </div>
    );
  }

  // ── 集中線 / tia hội tụ ───────────────────────────────────────────────────
  // 🔴 Bản đầu vẽ tia bề rộng tới 2,2 đơn viewBox và opacity 0,7 ⇒ ra "tia mặt trời"
  //    to bản che gần hết khung (bắt ở still demo scene 「片方は返金」). 集中線 thật là
  //    NÉT MẢNH, dày ở RÌA và thon về tâm, và có VÙNG TRỐNG ở giữa cho chủ thể.
  //    Ba thứ sửa: bề rộng ÷3 · fade dần vào tâm bằng gradient · lỗ trống giữa rộng gấp đôi.
  if (clip.variant === 'rays') {
    const spin = (frame / fps) * 3;
    return (
      <div style={box}>
        <svg viewBox="-50 -50 100 100" width="100%" height="100%">
          <defs>
            <radialGradient id={`rg${clip.id}`}>
              {/* trong suốt ở tâm -> đặc ở rìa: chủ thể giữa khung không bị phủ */}
              <stop offset="30%" stopColor={clip.color} stopOpacity="0" />
              <stop offset="62%" stopColor={clip.color} stopOpacity="0.42" />
              <stop offset="100%" stopColor={clip.color} stopOpacity="0.82" />
            </radialGradient>
            <mask id={`rm${clip.id}`}>
              <g transform={`rotate(${spin})`}>
                {Array.from({length: clip.density}).map((_, i) => {
                  const a = (360 / clip.density) * i;
                  const w = 0.28 + rnd(clip.seed, i, 21) * 0.72;
                  const r0 = 30 + rnd(clip.seed, i, 22) * 9;
                  return (
                    <path
                      key={i}
                      d={`M0,-${r0} L-${w},-78 L${w},-78 Z`}
                      fill="#FFFFFF"
                      transform={`rotate(${a})`}
                    />
                  );
                })}
              </g>
            </mask>
          </defs>
          <rect
            x="-78" y="-78" width="156" height="156"
            fill={`url(#rg${clip.id})`}
            mask={`url(#rm${clip.id})`}
          />
        </svg>
      </div>
    );
  }

  // ── QUẦNG SÁNG ───────────────────────────────────────────────────────────
  if (clip.variant === 'glow') {
    // thở nhẹ: 6% biên độ, chu kỳ 2,4s — đủ để mắt thấy sống mà không nhấp nháy
    const pulse = 1 + Math.sin((frame / fps / 2.4) * Math.PI * 2) * 0.06;
    return (
      <div style={box}>
        <div
          style={{
            position: 'absolute',
            inset: 0,
            transform: `scale(${pulse})`,
            background: `radial-gradient(circle at 50% 50%, ${clip.color}CC 0%, ${clip.color}55 32%, ${clip.color}00 68%)`,
          }}
        />
      </div>
    );
  }

  // ── VIGNETTE CẢNH BÁO: quầng màu ở RÌA khung, thở theo nhịp ──────────────
  // 🔴 Vì sao ở RÌA chứ không phủ toàn khung: phủ đều thì mặt người ngả màu và
  //    trông như lỗi cân bằng trắng — đúng cái làm clip Veo task_005 thành kỳ quặc
  //    (Veo tô đỏ thẳng lên bàn tay). Rìa thì mắt đọc là "đèn cảnh báo trong phòng",
  //    da người giữ nguyên màu thật.
  // 🔴 Nhịp thở phải CHẬM (~1,4s) và biên độ vừa. Nháy nhanh = đèn hỏng, và tệp 45+
  //    rất phạt thứ nhấp nháy gấp (`audience-45plus.md` §2).
  if (clip.variant === 'vignette') {
    const pulse = 0.55 + 0.45 * Math.abs(Math.sin((frame / fps / 1.4) * Math.PI));
    return (
      <div style={box}>
        <div
          style={{
            position: 'absolute',
            inset: 0,
            opacity: pulse,
            background:
              `radial-gradient(ellipse 78% 72% at 50% 50%, ${clip.color}00 55%, ` +
              `${clip.color}55 82%, ${clip.color}AA 100%)`,
            mixBlendMode: 'multiply',
          }}
        />
      </div>
    );
  }

  // ── DẤU ✗ ĐỎ ĐẬP XUỐNG rồi rung tắt dần ──────────────────────────────────
  // Đóng vai "cái này KHÔNG được / hết hạn". Vẽ bằng SVG nên nét luôn sắc — và
  // đây là thứ Veo LÀM ĐƯỢC (clip 03/06 ra dấu ✗ đỏ ổn) nhưng ta vẫn tự vẽ, vì
  // tự vẽ thì đúng nhịp lời và sửa được mà không gen lại clip.
  if (clip.variant === 'stampx') {
    const t = frame / fps;
    // đập: 0 -> 0,22s phóng từ 2,6x về 1,0 (ease-out mạnh) rồi rung tắt dần
    const hit = Math.min(1, t / 0.22);
    const sc = 2.6 - 1.6 * (1 - Math.pow(1 - hit, 4));
    const ring = t > 0.22 ? Math.exp(-(t - 0.22) * 7) * Math.sin((t - 0.22) * 46) * 3.2 : 0;
    return (
      <div style={box}>
        <div
          style={{
            position: 'absolute',
            inset: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transform: `scale(${sc}) rotate(${-9 + ring}deg)`,
          }}
        >
          <svg viewBox="0 0 100 100" style={{width: '38%', height: '38%', overflow: 'visible'}}>
            <defs>
              <filter id={`sx${clip.id}`} x="-30%" y="-30%" width="160%" height="160%">
                <feDropShadow dx="0" dy="3" stdDeviation="4" floodOpacity="0.45" />
              </filter>
            </defs>
            <g filter={`url(#sx${clip.id})`} stroke={clip.color} strokeWidth="17"
               strokeLinecap="round" fill="none">
              <path d="M16,16 L84,84" />
              <path d="M84,16 L16,84" />
            </g>
          </svg>
        </div>
      </div>
    );
  }

  // ── CONFETTI ─────────────────────────────────────────────────────────────
  if (clip.variant === 'confetti') {
    const PAL = [clip.color, '#FF5B6E', '#4FC3F7', '#8BE28B', '#FFFFFF'];
    return (
      <div style={box}>
        {Array.from({length: clip.density}).map((_, i) => {
          const x = rnd(clip.seed, i, 31) * AW;
          const w = AH * (0.026 + rnd(clip.seed, i, 32) * 0.022); // to gap ~1,8x bản đầu
          const speed = 0.22 + rnd(clip.seed, i, 33) * 0.3;
          const ph = rnd(clip.seed, i, 34);
          const t = ((frame / fps) * speed + ph) % 1;
          const y = -AH * 0.1 + t * AH * 1.2;
          const sway = Math.sin((t + ph) * Math.PI * 2 * 2.2) * AW * 0.04;
          const flip = Math.cos(((frame / fps) * (1.6 + ph) + ph) * Math.PI * 2);
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: x + sway,
                top: y,
                width: w,
                height: w * 1.8,
                background: PAL[i % PAL.length],
                opacity: Math.min(1, t / 0.1, (1 - t) / 0.12),
                transform: `rotate(${rnd(clip.seed, i, 35) * 180}deg) scaleY(${Math.max(0.15, Math.abs(flip))})`,
                borderRadius: 2,
              }}
            />
          );
        })}
      </div>
    );
  }

  // ── yawa (2026-10-01): ba lớp ÊM — không thở, không nháy ──────────────────
  // Bài học showa: "êm = ÍT thứ động + động CHẬM". Mọi thứ dưới đây ≤0,3 opacity
  // và tốc độ ~10 px/s để không làm khung "bơi".
  if (clip.variant === 'dust') {
    return (
      <div style={box}>
        {Array.from({length: clip.density}).map((_, i) => {
          const big = rnd(clip.seed, i, 41) < 0.25;            // 1/4 là bokeh to, mờ hơn
          const r = big ? 14 + rnd(clip.seed, i, 42) * 18 : 2 + rnd(clip.seed, i, 43) * 3.5;
          const speed = 6 + rnd(clip.seed, i, 44) * 8;          // px/s đi lên
          const x0 = rnd(clip.seed, i, 45) * AW;
          const y0 = rnd(clip.seed, i, 46) * (AH + 80);
          const tsec = frame / fps;
          const y = (((y0 - tsec * speed) % (AH + 80)) + AH + 80) % (AH + 80) - 40;
          const sway = Math.sin(tsec * (0.25 + rnd(clip.seed, i, 47) * 0.2) * Math.PI * 2 + i) * 10;
          const tw = 0.6 + 0.4 * Math.sin(tsec * (0.3 + rnd(clip.seed, i, 48) * 0.3) * Math.PI * 2 + i * 1.7);
          const a = (big ? 0.10 : 0.32) * tw;
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: x0 + sway - r,
                top: y - r,
                width: r * 2,
                height: r * 2,
                borderRadius: '50%',
                background: `radial-gradient(circle, ${clip.color}FF 0%, ${clip.color}88 40%, ${clip.color}00 72%)`,
                opacity: a,
                filter: big ? 'blur(3px)' : undefined,
              }}
            />
          );
        })}
      </div>
    );
  }

  if (clip.variant === 'vignette-soft') {
    return (
      <div style={box}>
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background:
              `radial-gradient(ellipse 80% 75% at 50% 48%, ${clip.color}00 58%, ` +
              `${clip.color}66 88%, ${clip.color}AA 100%)`,
          }}
        />
      </div>
    );
  }

  if (clip.variant === 'grain') {
    // seed đổi mỗi 2 frame (15 lần/s) — đổi mỗi frame thì hạt "sôi", tệp 45+ thấy rối mắt
    const sd = (Math.floor(frame / 2) * 7919 + clip.seed) % 997;
    return (
      <div style={box}>
        <svg width="100%" height="100%" style={{position: 'absolute', inset: 0, mixBlendMode: 'overlay'}}>
          <filter id={`yg${clip.seed}`}>
            <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={sd} stitchTiles="stitch" />
            <feColorMatrix type="saturate" values="0" />
          </filter>
          <rect width="100%" height="100%" filter={`url(#yg${clip.seed})`} />
        </svg>
      </div>
    );
  }

  return null;
};
