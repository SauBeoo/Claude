// entrances.ts — entrance-variant registry for sticker/cutout clips.
// Each variant maps (local frame, fps, params) -> partial CSS the Sticker
// component merges into its style. Lifted from OkuraDemo.jsx + the six
// documented variants in vox-collage-video/references/animation-variants.md.
// Rules carried over: always spring()-driven; supports use 'pop'; never
// repeat a variant on two consecutive scenes (enforced by importers, not here).

import {interpolate, spring} from 'remotion';

export type EntranceCtx = {
  frame: number; // clip-local frame, already past delayFrames
  fps: number;
  params: Record<string, unknown>;
};

export type EntranceStyle = {
  transform: string;
  opacity?: number;
  filter?: string;
  transformOrigin?: string;
};

type EntranceFn = (ctx: EntranceCtx) => EntranceStyle;

const num = (v: unknown, fallback: number): number =>
  typeof v === 'number' && Number.isFinite(v) ? v : fallback;

const fadeIn = (s: number) =>
  interpolate(s, [0, 0.25], [0, 1], {extrapolateRight: 'clamp'});

export const ENTRANCES: Record<string, EntranceFn> = {
  none: () => ({transform: 'none', opacity: 1}),

  // slide up from below
  rise: ({frame, fps, params}) => {
    const s = spring({frame, fps, config: {damping: 12, stiffness: 130}});
    const dist = num(params.distance, 420);
    return {
      transform: `translateY(${interpolate(s, [0, 1], [dist, 0])}px)`,
      opacity: fadeIn(s),
    };
  },

  // scale up from small
  grow: ({frame, fps, params}) => {
    const s = spring({frame, fps, config: {damping: 12, stiffness: 130}});
    const from = num(params.from, 0.25);
    return {
      transform: `scale(${interpolate(s, [0, 1], [from, 1])})`,
      opacity: fadeIn(s),
    };
  },

  // slam down from oversized
  punch: ({frame, fps, params}) => {
    const sp = spring({frame, fps, config: {damping: 8, stiffness: 220}});
    const from = num(params.from, 1.7);
    return {
      transform: `scale(${interpolate(sp, [0, 1], [from, 1])})`,
      opacity: fadeIn(sp),
    };
  },

  // 3D flip in around Y
  flip: ({frame, fps, params}) => {
    const s = spring({frame, fps, config: {damping: 12, stiffness: 130}});
    const deg = num(params.fromDeg, 85);
    return {
      transform: `rotateY(${interpolate(s, [0, 1], [deg, 0])}deg)`,
      opacity: fadeIn(s),
    };
  },

  // wobble-drop: low-damping fall + decaying sine rotate
  wobble: ({frame, fps}) => {
    const sp = spring({frame, fps, config: {damping: 6.5, stiffness: 160}});
    const wob = Math.sin(frame / 2.2) * 14 * Math.exp(-frame / 12);
    return {
      transform: `translateY(${interpolate(sp, [0, 1], [-500, 0])}px) rotate(${wob}deg)`,
      opacity: fadeIn(sp),
    };
  },

  // simple scale-pop (default for support elements)
  pop: ({frame, fps}) => {
    const s = spring({frame, fps, config: {damping: 10, stiffness: 190}});
    return {transform: `scale(${s})`, opacity: fadeIn(s)};
  },

  // peel off the page: rotateX from -70deg, hinge at top center
  peel: ({frame, fps, params}) => {
    const s = spring({frame, fps, config: {damping: 14, stiffness: 120}});
    const deg = num(params.fromDeg, -70);
    return {
      transform: `rotateX(${interpolate(s, [0, 1], [deg, 0])}deg)`,
      transformOrigin: 'top center',
      opacity: fadeIn(s),
    };
  },

  // one spring drives scale + 540deg rotation + slide (max once per video)
  spiral: ({frame, fps, params}) => {
    const s = spring({frame, fps, config: {damping: 15, stiffness: 90}});
    const turns = num(params.deg, 540);
    return {
      transform: [
        `translateX(${interpolate(s, [0, 1], [-360, 0])}px)`,
        `rotate(${interpolate(s, [0, 1], [turns, 0])}deg)`,
        `scale(${interpolate(s, [0, 1], [0.1, 1])})`,
      ].join(' '),
      opacity: fadeIn(s),
    };
  },

  // whip: fly in horizontally with motion blur (landmark-cutout transition,
  // kiểu "tách nền vật mốc" của CapCut VLOG edits)
  whip: ({frame, fps, params}) => {
    const s = spring({frame, fps, config: {damping: 16, stiffness: 190}});
    const fromX = num(params.fromX, -1700);
    const x = interpolate(s, [0, 1], [fromX, 0]);
    const speedBlur = Math.min(28, Math.abs(fromX) * (1 - s) * 0.02);
    return {
      transform: `translateX(${x}px) rotate(${interpolate(s, [0, 1], [num(params.fromDeg, -14), 0])}deg)`,
      filter: speedBlur > 1 ? `blur(${speedBlur.toFixed(1)}px)` : undefined,
      opacity: fadeIn(s),
    };
  },

  // zoom-through: from huge + blurred to crisp
  'zoom-through': ({frame, fps, params}) => {
    const s = spring({frame, fps, config: {damping: 13, stiffness: 110}});
    const from = num(params.from, 3.5);
    const blur = interpolate(s, [0, 1], [14, 0]);
    return {
      transform: `scale(${interpolate(s, [0, 1], [from, 1])})`,
      filter: blur > 0.3 ? `blur(${blur}px)` : undefined,
      opacity: fadeIn(s),
    };
  },
};

// exits reuse the same shape but run backwards near clip end (P4 wires the UI)
export const EXITS: Record<string, EntranceFn> = {
  fade: ({frame, fps}) => {
    const s = spring({frame, fps, config: {damping: 14, stiffness: 120}});
    return {transform: 'none', opacity: 1 - s};
  },
  sink: ({frame, fps}) => {
    const s = spring({frame, fps, config: {damping: 12, stiffness: 130}});
    return {
      transform: `translateY(${interpolate(s, [0, 1], [0, 420])}px)`,
      opacity: 1 - s,
    };
  },
  shrink: ({frame, fps}) => {
    const s = spring({frame, fps, config: {damping: 12, stiffness: 150}});
    return {transform: `scale(${1 - s})`, opacity: 1 - s};
  },
  // whip out to the right with motion blur (pairs with entrance 'whip')
  'whip-out': ({frame, fps}) => {
    const s = spring({frame, fps, config: {damping: 16, stiffness: 190}});
    const x = interpolate(s, [0, 1], [0, 1700]);
    const speedBlur = Math.min(28, s * (1 - s) * 90);
    return {
      transform: `translateX(${x}px) rotate(${s * 12}deg)`,
      filter: speedBlur > 1 ? `blur(${speedBlur.toFixed(1)}px)` : undefined,
      opacity: 1 - s * 0.4,
    };
  },
};

export const resolveEntrance = (variant: string): EntranceFn =>
  ENTRANCES[variant] ?? ENTRANCES.rise;

export const resolveExit = (variant: string): EntranceFn =>
  EXITS[variant] ?? EXITS.fade;

export const ENTRANCE_NAMES = Object.keys(ENTRANCES);
export const EXIT_NAMES = Object.keys(EXITS);
