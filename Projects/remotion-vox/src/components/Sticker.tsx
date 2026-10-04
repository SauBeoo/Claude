// Sticker.tsx — positioned cutout PNG with entrance/exit from the registry,
// continuous idle bob, and paper drop-shadow. Replaces Cutout+SupportElement.

import React from 'react';
import {Img, useCurrentFrame, useVideoConfig} from 'remotion';
import type {z} from 'zod';
import type {StickerClipSchema} from '../schema/project';
import {resolveAsset} from '../lib/resolveAsset';
import {resolveEntrance, resolveExit} from '../effects/entrances';

type StickerClip = z.infer<typeof StickerClipSchema>;

const SHADOWS: Record<string, string | undefined> = {
  lg: 'drop-shadow(10px 14px 0 rgba(0,0,0,0.22))',
  sm: 'drop-shadow(6px 8px 0 rgba(0,0,0,0.20))',
  none: undefined,
};

const idle = (frame: number, phase: number, amp: number) => ({
  y: Math.sin(frame / 13 + phase) * amp,
  rot: Math.sin(frame / 19 + phase * 1.7) * (amp >= 5 ? 0.8 : 1.0),
});

const EXIT_FRAMES = 18; // exit animation window at the tail of the clip

export const Sticker: React.FC<{
  clip: StickerClip;
  projectName: string;
}> = ({clip, projectName}) => {
  const frame = useCurrentFrame(); // clip-local (Sequence resets it)
  const {fps} = useVideoConfig();

  const t = frame - clip.entrance.delayFrames;
  if (t < 0) return null;

  const enter = resolveEntrance(clip.entrance.variant)({
    frame: t,
    fps,
    params: clip.entrance.params,
  });

  let exitStyle: ReturnType<typeof Object.assign> | null = null;
  if (clip.exit) {
    const exitStart = clip.durationInFrames - EXIT_FRAMES;
    if (frame >= exitStart) {
      exitStyle = resolveExit(clip.exit.variant)({
        frame: frame - exitStart,
        fps,
        params: clip.exit.params,
      });
    }
  }

  const bob = idle(frame, clip.idle.phase, clip.idle.amp);
  const {x, y, w, rotation, opacity} = clip.layout;

  const transforms = [
    enter.transform !== 'none' ? enter.transform : '',
    exitStyle && exitStyle.transform !== 'none' ? exitStyle.transform : '',
    `translateY(${bob.y}px)`,
    `rotate(${rotation + bob.rot}deg)`,
  ]
    .filter(Boolean)
    .join(' ');

  const alpha =
    (enter.opacity ?? 1) * (exitStyle?.opacity ?? 1) * opacity;

  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        width: w,
        perspective: 1200,
      }}
    >
      <Img
        src={resolveAsset(projectName, clip.asset)}
        style={{
          width: '100%',
          opacity: alpha,
          transform: transforms,
          transformOrigin: enter.transformOrigin,
          filter:
            [enter.filter, SHADOWS[clip.shadow]].filter(Boolean).join(' ') ||
            undefined,
        }}
      />
    </div>
  );
};
