// CaptionLayer.tsx — burned-in captions. Two modes:
//   - words[] present  -> karaoke word-by-word highlight (CapCut-style)
//   - lines[] only     -> per-line subtitle
// Styles are presets matching the channel pipeline (sub_style values).
// The UPLOADED subs.srt is generated separately (tools/export_srt.py) and
// stays clean — this layer is burn-only.

import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import type {z} from 'zod';
import type {CaptionsSchema, ThemeSchema} from '../schema/project';

type Captions = z.infer<typeof CaptionsSchema>;
type Theme = z.infer<typeof ThemeSchema>;

type StylePreset = {
  container: React.CSSProperties;
  text: React.CSSProperties;
  activeWord: React.CSSProperties;
};

const PRESETS: Record<string, StylePreset> = {
  // chữ trần viền đen — chuẩn toàn hệ thống (audience-45plus §3.1)
  outline: {
    container: {},
    text: {
      color: '#fff',
      WebkitTextStroke: '8px #000',
      paintOrder: 'stroke fill',
      textShadow: '0 3px 10px rgba(0,0,0,0.45)',
    },
    activeWord: {color: '#FFE01B'},
  },
  // hộp đen mờ (kiểu CapCut mặc định)
  box: {
    container: {
      background: 'rgba(0,0,0,0.72)',
      borderRadius: 14,
      padding: '10px 28px',
    },
    text: {color: '#fff'},
    activeWord: {color: '#FFE01B'},
  },
  // karaoke đậm: từ active phóng nhẹ + đổi màu
  karaoke: {
    container: {},
    text: {
      color: '#fff',
      WebkitTextStroke: '9px #111',
      paintOrder: 'stroke fill',
    },
    activeWord: {color: '#FFD700'},
  },
};

export const CaptionLayer: React.FC<{captions: Captions; theme: Theme}> = ({
  captions,
  theme,
}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const nowMs = (frame / fps) * 1000;

  const preset = PRESETS[captions.style] ?? PRESETS.outline;
  const line = captions.lines.find(
    (l) => nowMs >= l.startMs && nowMs < l.endMs,
  );
  if (!line) return null;

  const lineIndex = captions.lines.indexOf(line);
  const words = captions.words.filter((w) => w.lineIndex === lineIndex);
  const fontSize = captions.fontSize * (height / 1080);

  return (
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        bottom: height * 0.055,
        display: 'flex',
        justifyContent: 'center',
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          maxWidth: width * 0.86,
          textAlign: 'center',
          fontFamily: theme.fontFamily,
          fontWeight: 900,
          fontSize,
          lineHeight: 1.3,
          ...preset.container,
        }}
      >
        {words.length > 0 ? (
          words.map((w, i) => {
            const active = nowMs >= w.startMs && nowMs < w.endMs;
            const past = nowMs >= w.endMs;
            return (
              <span
                key={i}
                style={{
                  ...preset.text,
                  ...(active ? preset.activeWord : null),
                  ...(active ? {transform: 'scale(1.08)'} : null),
                  display: 'inline-block',
                  opacity: past || active ? 1 : 0.92,
                  whiteSpace: 'pre',
                }}
              >
                {w.text}
              </span>
            );
          })
        ) : (
          <span style={preset.text}>{line.text}</span>
        )}
      </div>
    </div>
  );
};
