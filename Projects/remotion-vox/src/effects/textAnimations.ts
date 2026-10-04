// textAnimations.ts — registry for text-clip entrances (tag chips, punch boxes).

import {interpolate, spring} from 'remotion';
import type {EntranceCtx, EntranceStyle} from './entrances';

type TextAnimFn = (ctx: EntranceCtx) => EntranceStyle;

const num = (v: unknown, fallback: number): number =>
  typeof v === 'number' && Number.isFinite(v) ? v : fallback;

export const TEXT_ANIMATIONS: Record<string, TextAnimFn> = {
  none: () => ({transform: 'none', opacity: 1}),

  // scale-in with a resting tilt (TitleTag / PunchPhrase behaviour)
  pop: ({frame, fps, params}) => {
    const s = spring({
      frame,
      fps,
      config: {
        damping: num(params.damping, 13),
        stiffness: num(params.stiffness, 200),
      },
    });
    const rest = num(params.restDeg, -2);
    return {transform: `scale(${s}) rotate(${rest}deg)`};
  },

  // tag entrance when the hero flips: swings from +12deg to rest
  'pop-swing': ({frame, fps, params}) => {
    const s = spring({frame, fps, config: {damping: 11, stiffness: 180}});
    const rest = num(params.restDeg, -2);
    const rot = interpolate(s, [0, 1], [12, rest]);
    return {transform: `scale(${s}) rotate(${rot}deg)`};
  },

  // slide in from the left, slight overshoot
  'slide-in': ({frame, fps, params}) => {
    const s = spring({frame, fps, config: {damping: 12, stiffness: 160}});
    const rest = num(params.restDeg, -1.5);
    return {
      transform: `translateX(${interpolate(s, [0, 1], [-260, 0])}px) rotate(${rest}deg)`,
      opacity: interpolate(s, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'}),
    };
  },

  // drop from above and settle
  drop: ({frame, fps, params}) => {
    const s = spring({frame, fps, config: {damping: 9, stiffness: 170}});
    const rest = num(params.restDeg, -1.5);
    return {
      transform: `translateY(${interpolate(s, [0, 1], [-180, 0])}px) rotate(${rest}deg)`,
      opacity: interpolate(s, [0, 0.25], [0, 1], {extrapolateRight: 'clamp'}),
    };
  },
};

export const resolveTextAnimation = (name: string): TextAnimFn =>
  TEXT_ANIMATIONS[name] ?? TEXT_ANIMATIONS.pop;

export const TEXT_ANIMATION_NAMES = Object.keys(TEXT_ANIMATIONS);
