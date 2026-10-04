// VoxProject.tsx — THE generic composition. Renders any project.json.
// Track array order = z-order (first = bottom). Every clip is a Sequence.

import React from 'react';
import {AbsoluteFill, Audio, Sequence} from 'remotion';
import type {CalculateMetadataFunction} from 'remotion';
import type {Clip, Project, Track} from '../schema/project';
import {parseProject} from '../schema/project';
import {resolveAsset} from '../lib/resolveAsset';
import {Background} from '../components/Background';
import {Sticker} from '../components/Sticker';
import {TextClip} from '../components/TextClip';
import {Footage} from '../components/Footage';
import {CaptionLayer} from '../components/CaptionLayer';
import {FxLayer} from '../components/FxLayer';
import {BrandOverlay} from '../components/BrandOverlay';

// Props ARE the raw project.json content — so `--props=projects/<x>/project.json`
// feeds the composition directly. Validated in calculateMetadata + at render.
export type VoxProjectProps = Record<string, unknown>;

const ClipView: React.FC<{clip: Clip; project: Project; muted: boolean}> = ({
  clip,
  project,
  muted,
}) => {
  const name = project.meta.name;
  switch (clip.kind) {
    case 'background':
      return <Background clip={clip} projectName={name} />;
    case 'sticker':
      return <Sticker clip={clip} projectName={name} />;
    case 'text':
      return <TextClip clip={clip} theme={project.theme} />;
    case 'video':
      return <Footage clip={clip} projectName={name} />;
    case 'fx':
      return <FxLayer clip={clip} />;
    case 'audio':
      return muted ? null : (
        <Audio
          src={resolveAsset(name, clip.asset)}
          volume={clip.volume}
          startFrom={clip.trimStartFrames || undefined}
        />
      );
    default:
      return null;
  }
};

const TrackView: React.FC<{track: Track; project: Project}> = ({
  track,
  project,
}) => {
  if (track.hidden) return null;
  return (
    <>
      {track.clips.map((clip) => (
        <Sequence
          key={clip.id}
          from={clip.from}
          durationInFrames={clip.durationInFrames}
        >
          <ClipView clip={clip} project={project} muted={track.muted} />
        </Sequence>
      ))}
    </>
  );
};

export const VoxProject: React.FC<VoxProjectProps> = (props) => {
  const p = parseProject(props);
  return (
    <AbsoluteFill style={{backgroundColor: p.theme.canvasColor}}>
      {p.tracks.map((track) => (
        <TrackView key={track.id} track={track} project={p} />
      ))}
      {p.brand ? <BrandOverlay brand={p.brand} projectName={p.meta.name} /> : null}
      {p.captions.enabled && p.captions.lines.length > 0 ? (
        <CaptionLayer captions={p.captions} theme={p.theme} />
      ) : null}
    </AbsoluteFill>
  );
};

export const calculateVoxMetadata: CalculateMetadataFunction<
  VoxProjectProps
> = ({props}) => {
  const p = parseProject(props);
  return {
    durationInFrames: p.timeline.durationInFrames,
    fps: p.meta.fps,
    width: p.meta.width,
    height: p.meta.height,
    props,
  };
};
