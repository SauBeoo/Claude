// Footage.tsx — full-bleed or boxed media: mp4 clip OR still image.
// Stills can slow-pan (ease) — mirrors the pipeline's --motion behaviour.

import React from 'react';
import {
  Img,
  OffthreadVideo,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import type {z} from 'zod';
import type {FootageClipSchema} from '../schema/project';
import {isVideoAsset, resolveAsset} from '../lib/resolveAsset';

type FootageClip = z.infer<typeof FootageClipSchema>;

export const Footage: React.FC<{clip: FootageClip; projectName: string}> = ({
  clip,
  projectName,
}) => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const src = resolveAsset(projectName, clip.asset);

  const fadeIn =
    clip.fadeInFrames > 0
      ? interpolate(frame, [0, clip.fadeInFrames], [0, 1], {
          extrapolateRight: 'clamp',
        })
      : 1;

  const f = clip.filter ?? {};
  const cssFilter =
    [
      f.brightness != null && f.brightness !== 1 ? `brightness(${f.brightness})` : '',
      f.contrast != null && f.contrast !== 1 ? `contrast(${f.contrast})` : '',
      f.saturate != null && f.saturate !== 1 ? `saturate(${f.saturate})` : '',
      f.grayscale ? `grayscale(${f.grayscale})` : '',
      f.sepia ? `sepia(${f.sepia})` : '',
      f.blur ? `blur(${f.blur}px)` : '',
    ]
      .filter(Boolean)
      .join(' ') || undefined;

  // linear-mask wipe reveal (mặt nạ tuyến tính)
  let clipPath: string | undefined;
  if (clip.wipeInFrames > 0 && frame < clip.wipeInFrames) {
    const p = interpolate(frame, [0, clip.wipeInFrames], [100, 0], {
      easing: (t) => 1 - Math.pow(1 - t, 3),
    });
    const insets = {
      left: `inset(0 ${p}% 0 0)`,
      right: `inset(0 0 0 ${p}%)`,
      up: `inset(${p}% 0 0 0)`,
      down: `inset(0 0 ${p}% 0)`,
    } as const;
    clipPath = insets[clip.wipeDir];
  }

  // ── LẬT TRANG (curl reveal) ────────────────────────────────────────────────
  // Clip mới hiện dần theo một đường CHÉO quét qua khung, kèm dải sáng ở mép và
  // bóng đổ mềm — đọc ra như một trang giấy đang được lật sang.
  //
  // ⚠️⚠️ ĐÂY LÀ XẤP XỈ 2D, KHÔNG PHẢI LẬT TRANG THẬT. Lật trang thật (như bản mẫu
  //    nenkin video 22 tham chiếu) cần **warp 3D** — mặt giấy phải cong, mặt sau
  //    phải thấy được, bóng phải bẻ theo độ cong. Cái đó cần WebGL/canvas shader,
  //    CSS không làm nổi. Ở khổ 1920 và tốc độ 0,6–0,9s thì mắt đọc ra "trang lật",
  //    nhưng **đừng hứa với ai là giống y bản mẫu** — soi từng frame sẽ thấy mép
  //    thẳng chứ không cong.
  // 🔴 `clipPath` chỉ nhận MỘT giá trị, nên curl và wipe KHÔNG dùng chung được.
  //    Khai cả hai trên một clip thì curl thắng (nó cụ thể hơn), và builder phải
  //    coi đó là lỗi cấu hình chứ không phải tính năng.
  let curlRim: React.CSSProperties | undefined;
  if (clip.curlInFrames > 0 && frame < clip.curlInFrames) {
    const t = interpolate(frame, [0, clip.curlInFrames], [0, 1], {
      easing: (x) => 1 - Math.pow(1 - x, 3),
    });
    // đường chéo quét: p đi từ -40 -> 140 (phần trăm) để mép ra hẳn ngoài khung
    const p = -40 + t * 180;
    // hai điểm của đường chéo, lệch 40% để đường nghiêng ~22 độ
    const a = p;
    const b = p + 40;
    const polys = {
      br: `polygon(0% 0%, ${b}% 0%, ${a}% 100%, 0% 100%)`,
      bl: `polygon(${100 - b}% 0%, 100% 0%, 100% 100%, ${100 - a}% 100%)`,
      tr: `polygon(0% 0%, 100% 0%, 100% ${a}%, 0% ${b}%)`,
      tl: `polygon(0% ${100 - b}%, 100% ${100 - a}%, 100% 100%, 0% 100%)`,
    } as const;
    clipPath = polys[clip.curlDir];
    // dải sáng + bóng chạy DỌC theo mép vừa quét qua
    const ang = clip.curlDir === 'br' || clip.curlDir === 'bl' ? 102 : 12;
    curlRim = {
      position: 'absolute',
      inset: 0,
      pointerEvents: 'none',
      background:
        `linear-gradient(${ang}deg, rgba(0,0,0,0) ` +
        `${Math.max(0, a - 6)}%, rgba(255,255,255,0.55) ${a}%, ` +
        `rgba(255,255,255,0.10) ${a + 3}%, rgba(0,0,0,0.28) ${a + 7}%, ` +
        `rgba(0,0,0,0) ${a + 16}%)`,
      clipPath,
    };
  }

  const boxed = clip.layout.x != null || clip.layout.w != null;
  const box: React.CSSProperties = boxed
    ? {
        position: 'absolute',
        left: clip.layout.x ?? 0,
        top: clip.layout.y ?? 0,
        width: clip.layout.w ?? width,
        height: clip.layout.h,
        opacity: (clip.layout.opacity ?? 1) * fadeIn,
        transform: clip.layout.rotation
          ? `rotate(${clip.layout.rotation}deg)`
          : undefined,
        overflow: 'hidden',
        clipPath,
        borderRadius: clip.frame?.radius,
        border: clip.frame?.border ? `${clip.frame.border}px solid ${clip.frame.borderColor}` : undefined,
        boxShadow: clip.frame?.shadow ?? undefined,
      }
    : {
        position: 'absolute',
        inset: 0,
        opacity: (clip.layout.opacity ?? 1) * fadeIn,
        overflow: 'hidden',
        clipPath,
      };

  if (isVideoAsset(clip.asset)) {
    return (
      <div style={box}>
        <OffthreadVideo
          src={src}
          startFrom={clip.trimStartFrames}
          volume={clip.volume}
          playbackRate={clip.speed}
          style={{
            width: '100%',
            height: '100%',
            objectFit: clip.fit,
            filter: cssFilter,
            transform: clip.mirror ? 'scaleX(-1)' : undefined,
          }}
        />
        {curlRim ? <div style={curlRim} /> : null}
      </div>
    );
  }

  // still image; optional motion
  let transform: string | undefined;
  if (clip.motion === 'pan') {
    // slow ease pan (zoom 1.0 -> 1.08 drifting)
    const p = interpolate(frame, [0, clip.durationInFrames], [0, 1], {
      extrapolateRight: 'clamp',
      easing: (t) => 1 - Math.pow(1 - t, 2),
    });
    const zoom = 1.02 + 0.06 * p;
    const dx = -12 * p;
    transform = `scale(${zoom}) translateX(${dx}px)`;
  } else if (clip.motion === 'zoom-punch') {
    // speed-ramp hit: slam from 1.28 -> 1.0 in ~8 frames, then hold
    const p = interpolate(frame, [0, 8], [0, 1], {
      extrapolateRight: 'clamp',
      easing: (t) => 1 - Math.pow(1 - t, 3),
    });
    transform = `scale(${1.28 - 0.28 * p})`;
  }

  return (
    <div style={box}>
      <Img
        src={src}
        style={{
          width: '100%',
          height: boxed ? clip.layout.h ?? undefined : '100%',
          objectFit: clip.fit,
          transform:
            [transform, clip.mirror ? 'scaleX(-1)' : '']
              .filter(Boolean)
              .join(' ') || undefined,
          filter: cssFilter,
        }}
      />
    </div>
  );
};
