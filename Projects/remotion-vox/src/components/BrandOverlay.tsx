// BrandOverlay.tsx — lớp nhận diện dán CỨNG mọi frame: logo (trên-phải) ·
// mascot (dưới-phải) · nút SUBSCRIBE animate (dưới-trái).
//
// Bản mẫu cùng ngách có đủ 3 thứ này ở 100% frame — mascot cáo 9 đuôi là thứ mắt
// nhìn vào đầu tiên ở góc phải. Khai ở ROOT project (`brand`), KHÔNG khai từng clip:
// khai từng clip thì một video 14 phút phải nhét thêm ~113 clip rác vào timeline.
//
// 🔴 MASCOT "CHUYỂN ĐỘNG" = đổi TƯ THẾ theo mốc giây + bob liên tục, KHÔNG phải video.
//    Cutout một clip video (rembg từng frame × 25.000 frame) là đường đắt và bẩn;
//    vài PNG tư thế nền magenta cắt bằng `cutout_sticker.py` thì sạch 9px và sắc nét.
// 🔴 Bob/nghiêng phải TIỀN ĐỊNH theo frame (không `random()`) — cùng bẫy đã dính ở
//    `papercut` (mép giấy rung mỗi frame).
// 🔴 GÓC DƯỚI-PHẢI CỦA KHUNG LÀ CỦA YOUTUBE (timestamp) — mascot đặt ở đó thì phải
//    NÂNG lên khỏi dải ~4% đáy, nếu không nó nằm dưới cái đồng hồ.

import React from 'react';
import {useCurrentFrame, useVideoConfig, interpolate, Img} from 'remotion';
import type {z} from 'zod';
import type {BrandSchema} from '../schema/project';
import {resolveAsset} from '../lib/resolveAsset';

type BrandT = z.infer<typeof BrandSchema>;

export const BrandOverlay: React.FC<{brand: BrandT; projectName: string}> = ({
  brand,
  projectName,
}) => {
  const frame = useCurrentFrame();
  const {width, height, fps} = useVideoConfig();
  const sec = frame / fps;

  // ── mascot: chọn tư thế theo mốc giây ──────────────────────────────────
  let mascotAsset = brand.mascot;
  if (brand.mascotPoses.length > 0) {
    const act = brand.mascotPoses
      .filter((p) => p.atSec <= sec)
      .sort((a, b) => a.atSec - b.atSec)
      .pop();
    if (act) mascotAsset = act.asset;
  }

  // bob: lên xuống 2,6% chiều cao mascot, chu kỳ 2,2s + nghiêng ±1,6°
  const bob = Math.sin((sec / 2.2) * Math.PI * 2);
  const tilt = Math.sin((sec / 3.1) * Math.PI * 2) * 1.6;

  // nút SUBSCRIBE: nhịp 4s — nằm im 3s, rồi nảy 2 cái + con trỏ chạm vào
  const cyc = sec % 4;
  const press = cyc > 3 ? Math.sin((cyc - 3) * Math.PI * 2) : 0;
  const btnScale = 1 + Math.max(0, press) * 0.12;
  const cursorX = interpolate(cyc, [2.6, 3.05], [26, 4], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const BOT = brand.bottomOffset;
  // 🔴 SUBSCRIBE có lề đáy RIÊNG: nó ở góc dưới-TRÁI nên chỉ phải tránh dải phụ đề, còn
  //    mascot ở góc dưới-PHẢI phải tránh timestamp của YouTube. Dùng chung một số thì hạ
  //    nút là hạ luôn mascot. `null` ⇒ giữ y nguyên hành vi cũ.
  const BOT_SUB = brand.subscribeBottom ?? BOT;

  return (
    <>
      {/* LOGO — góc TRÊN-PHẢI */}
      {brand.logo ? (
        <Img
          src={resolveAsset(projectName, brand.logo)}
          style={{
            position: 'absolute',
            right: Math.round(width * 0.012),
            top: Math.round(height * 0.015),
            height: brand.logoH,
            opacity: 0.95,
            filter: 'drop-shadow(0 2px 6px rgba(0,0,0,0.35))',
          }}
        />
      ) : null}

      {/* MASCOT VIDEO — góc DƯỚI-PHẢI. Ưu tiên hơn ảnh tĩnh khi có.
          🔴 File phải là **WebM VP9 có kênh alpha** (`mascot_chroma.py` xuất ra) — mp4 không
             mang được alpha, dán vào là ra một cái hộp đen ở góc màn.
          🔴 `Loop` phải nhận SỐ FRAME THẬT của clip, không phải số đoán: đoán ngắn thì clip
             bị cắt giữa động tác, đoán dài thì nó đứng hình chờ hết vòng. */}
      {brand.mascotVideo ? (
        <div
          style={{
            position: 'absolute',
            right: Math.round(width * 0.008),
            bottom: BOT + bob * (brand.mascotH * 0.02),
            height: brand.mascotH,
            transform: `rotate(${tilt * 0.5}deg)`,
            transformOrigin: '50% 100%',
            filter: 'drop-shadow(0 6px 12px rgba(0,0,0,0.35))',
          }}
        >
          <Img
            src={resolveAsset(
              projectName,
              // 🔴 PNG SEQUENCE, không phải WebM alpha. Build ffmpeg trên máy này KHÔNG
              //    ghi được alpha vào WebM (xuất ra yuv420p, im lặng) — đã thử vp9/vp8,
              //    -auto-alt-ref 0, bỏ despill; trích frame rgba đo thì alpha=255 hết.
              //    Sequence là đường không thể hỏng: mỗi frame một file RGBA riêng.
              // 🔴 `% N` để LOOP: N phải là SỐ FRAME THẬT (mascot_chroma.py in ra), và
              //    frame đánh số từ 1 (ffmpeg %04d bắt đầu ở 0001), nên +1.
              (mascotAsset || brand.mascotVideo).replace(
                '%04d',
                String((frame % Math.max(1, brand.mascotVideoFrames)) + 1).padStart(4, '0')
              )
            )}
            style={{height: brand.mascotH, width: 'auto'}}
          />
        </div>
      ) : null}

      {/* MASCOT ảnh tĩnh — đường lui khi chưa có clip alpha */}
      {!brand.mascotVideo && mascotAsset ? (
        <Img
          src={resolveAsset(projectName, mascotAsset)}
          style={{
            position: 'absolute',
            right: Math.round(width * 0.008),
            bottom: BOT + bob * (brand.mascotH * 0.026),
            height: brand.mascotH,
            transform: `rotate(${tilt}deg)`,
            transformOrigin: '50% 100%',
            filter: 'drop-shadow(0 6px 12px rgba(0,0,0,0.35))',
          }}
        />
      ) : null}

      {/* SUBSCRIBE — góc DƯỚI-TRÁI. Vẽ bằng DOM, không phải ảnh: sắc ở mọi khổ,
          và đổi chữ theo ngôn ngữ mà không phải gen lại asset. */}
      {brand.subscribe ? (
        <div
          style={{
            position: 'absolute',
            left: Math.round(width * 0.012),
            bottom: BOT_SUB,
            display: 'flex',
            alignItems: 'center',
            gap: 10,
            transform: `scale(${btnScale})`,
            transformOrigin: '0% 100%',
          }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 8,
              background: '#E12B2B',
              borderRadius: 11,
              padding: '8px 15px',
              border: '3px solid #FFFFFF',
              boxShadow: '0 4px 10px rgba(0,0,0,0.4)',
            }}
          >
            {/* nút play kiểu YouTube */}
            <svg width="34" height="24" viewBox="0 0 40 28">
              <rect width="40" height="28" rx="7" fill="#FFFFFF" />
              <path d="M16,8 L27,14 L16,20 Z" fill="#E12B2B" />
            </svg>
            <span
              style={{
                color: '#FFFFFF',
                fontWeight: 900,
                fontSize: 23,
                letterSpacing: '0.04em',
                fontFamily: 'Arial Black, sans-serif',
              }}
            >
              SUBSCRIBE
            </span>
          </div>
          {/* con trỏ chuột trượt tới rồi bấm */}
          <svg
            width="27"
            height="34"
            viewBox="0 0 30 38"
            style={{position: 'absolute', left: cursorX + 84, bottom: -18}}
          >
            <path
              d="M3,2 L3,28 L10,21 L15,33 L20,30 L15,19 L24,19 Z"
              fill="#FFFFFF"
              stroke="#111111"
              strokeWidth="2.4"
              strokeLinejoin="round"
            />
          </svg>
        </div>
      ) : null}
    </>
  );
};
