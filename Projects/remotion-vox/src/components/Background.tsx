// Background.tsx — paper texture + tint + grid/dot patterns + splash blobs.
// Ported from OkuraDemo GridBackground, now driven by a background clip.

import React from 'react';
import {AbsoluteFill, Img, useVideoConfig} from 'remotion';
import type {z} from 'zod';
import type {BackgroundClipSchema} from '../schema/project';
import {resolveAsset} from '../lib/resolveAsset';

type BackgroundClip = z.infer<typeof BackgroundClipSchema>;

export const Background: React.FC<{
  clip: BackgroundClip;
  projectName: string;
}> = ({clip, projectName}) => {
  const {width, height} = useVideoConfig();
  return (
    <AbsoluteFill>
      {clip.paper ? (
        <Img
          src={resolveAsset(projectName, clip.paper)}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            opacity: 0.9,
          }}
        />
      ) : null}
      <AbsoluteFill
        style={{backgroundColor: clip.tint, opacity: clip.tintOpacity}}
      />
      {clip.grid || clip.dots ? (
        <svg width={width} height={height} style={{position: 'absolute'}}>
          <defs>
            <pattern
              id="rv-grid"
              width="72"
              height="72"
              patternUnits="userSpaceOnUse"
            >
              <path
                d="M72 0H0V72"
                fill="none"
                stroke="#1a1a1a"
                strokeOpacity="0.10"
                strokeWidth="1.5"
              />
            </pattern>
            <pattern
              id="rv-dots"
              width="26"
              height="26"
              patternUnits="userSpaceOnUse"
            >
              <circle cx="4" cy="4" r="3.2" fill="#1a1a1a" fillOpacity="0.16" />
            </pattern>
          </defs>
          {clip.grid ? (
            <rect width={width} height={height} fill="url(#rv-grid)" />
          ) : null}
          {clip.dots ? (
            <>
              <rect
                x={width - 420}
                y={60}
                width={360}
                height={260}
                fill="url(#rv-dots)"
                opacity={0.7}
              />
              <rect
                x={60}
                y={height - 300}
                width={300}
                height={230}
                fill="url(#rv-dots)"
                opacity={0.5}
              />
            </>
          ) : null}
        </svg>
      ) : null}
      {clip.splash ? (
        <>
          <div
            style={{
              position: 'absolute',
              left: -180,
              top: -220,
              width: 760,
              height: 760,
              borderRadius: '50%',
              background: clip.splash[0],
              opacity: 0.3,
              filter: 'blur(70px)',
            }}
          />
          <div
            style={{
              position: 'absolute',
              right: -160,
              bottom: -260,
              width: 820,
              height: 820,
              borderRadius: '50%',
              background: clip.splash[1],
              opacity: 0.26,
              filter: 'blur(80px)',
            }}
          />
        </>
      ) : null}
    </AbsoluteFill>
  );
};
