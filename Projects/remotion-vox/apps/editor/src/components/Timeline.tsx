// Timeline.tsx — CapCut-style multitrack timeline.
// Drag = move clip; edge handles = trim; snap to scene markers, neighbour
// clip edges and the playhead. Ctrl+wheel zooms. History snapshots only on
// pointer-up (pauseHistory/resumeHistory).

import React, {useCallback, useMemo, useRef} from 'react';
import type {Clip, Track} from '../../../../src/schema/project';
import {
  pauseHistory,
  resumeHistory,
  useProject,
} from '../store/useProject';

const LABEL_W = 148;
const ROW_H = 40;
const SNAP_PX = 7;

const KIND_COLORS: Record<string, string> = {
  background: '#3e5a52',
  sticker: '#4a6fa5',
  text: '#8a6d3b',
  video: '#5b4a8a',
  audio: '#3d7a4f',
};

type DragState = {
  mode: 'move' | 'trim-l' | 'trim-r';
  trackId: string;
  clipId: string;
  startX: number;
  origFrom: number;
  origDur: number;
  origTrim: number;
  origProject: NonNullable<ReturnType<typeof useProject.getState>['project']>;
  moved: boolean;
};

export const Timeline: React.FC<{
  onSeek: (frame: number) => void;
}> = ({onSeek}) => {
  const project = useProject((s) => s.project);
  const selection = useProject((s) => s.selection);
  const playhead = useProject((s) => s.playheadFrame);
  const pxf = useProject((s) => s.pxPerFrame);
  const setPxPerFrame = useProject((s) => s.setPxPerFrame);
  const select = useProject((s) => s.select);
  const updateClip = useProject((s) => s.updateClip);
  const drag = useRef<DragState | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  const snapPoints = useMemo(() => {
    if (!project) return [] as number[];
    const pts = new Set<number>([0, project.timeline.durationInFrames, playhead]);
    for (const m of project.sceneMarkers) pts.add(m.atFrame);
    for (const t of project.tracks)
      for (const c of t.clips) {
        pts.add(c.from);
        pts.add(c.from + c.durationInFrames);
      }
    return [...pts];
  }, [project, playhead]);

  const snap = useCallback(
    (frame: number, excludeClip?: string) => {
      let best = frame;
      let bestDist = SNAP_PX / pxf;
      for (const p of snapPoints) {
        const d = Math.abs(p - frame);
        if (d < bestDist) {
          best = p;
          bestDist = d;
        }
      }
      return Math.max(0, Math.round(best));
    },
    [snapPoints, pxf],
  );

  const onClipPointerDown = (
    e: React.PointerEvent,
    track: Track,
    clip: Clip,
    mode: DragState['mode'],
  ) => {
    if (track.locked) return;
    e.stopPropagation();
    try {
      (e.target as HTMLElement).setPointerCapture(e.pointerId);
    } catch {
      // synthetic pointer events (automation) may carry an invalid pointerId
    }
    select({trackId: track.id, clipId: clip.id});
    const origProject = useProject.getState().project;
    if (!origProject) return;
    pauseHistory();
    drag.current = {
      mode,
      trackId: track.id,
      clipId: clip.id,
      startX: e.clientX,
      origFrom: clip.from,
      origDur: clip.durationInFrames,
      origTrim: (clip as {trimStartFrames?: number}).trimStartFrames ?? 0,
      origProject,
      moved: false,
    };
  };

  const onPointerMove = (e: React.PointerEvent) => {
    const d = drag.current;
    if (!d) return;
    d.moved = true;
    const df = (e.clientX - d.startX) / pxf;
    if (d.mode === 'move') {
      const from = snap(d.origFrom + df, d.clipId);
      updateClip(d.trackId, d.clipId, {from});
    } else if (d.mode === 'trim-r') {
      const end = snap(d.origFrom + d.origDur + df, d.clipId);
      updateClip(d.trackId, d.clipId, {
        durationInFrames: Math.max(1, end - d.origFrom),
      });
    } else {
      const from = Math.min(snap(d.origFrom + df, d.clipId), d.origFrom + d.origDur - 1);
      const delta = from - d.origFrom;
      const patch: Partial<Clip> & {trimStartFrames?: number} = {
        from,
        durationInFrames: d.origDur - delta,
      };
      // media clips keep their content anchored while trimming the head
      patch.trimStartFrames = Math.max(0, d.origTrim + delta);
      updateClip(d.trackId, d.clipId, patch as Partial<Clip>);
    }
  };

  const endDrag = () => {
    const d = drag.current;
    if (!d) return;
    drag.current = null;
    const finalProject = useProject.getState().project;
    if (d.moved && finalProject) {
      // zundo pushes the PRE-set state on the next recorded set — so: revert
      // silently to the gesture-start project, resume recording, then apply
      // the final state. Undo now lands exactly on the pre-drag state.
      useProject.setState({project: d.origProject});
      resumeHistory();
      useProject.setState({project: finalProject, dirty: true});
    } else {
      resumeHistory();
    }
  };

  const onLaneWheel = (e: React.WheelEvent) => {
    if (e.ctrlKey) {
      e.preventDefault();
      setPxPerFrame(pxf * (e.deltaY < 0 ? 1.2 : 1 / 1.2));
    }
  };

  if (!project) return <div className="timeline empty">Chưa mở project</div>;

  const total = project.timeline.durationInFrames;
  const fps = project.meta.fps;
  const laneW = Math.max(600, total * pxf + 200);

  const seekFromEvent = (e: React.MouseEvent) => {
    const rect = scrollRef.current!.getBoundingClientRect();
    const x = e.clientX - rect.left + scrollRef.current!.scrollLeft - LABEL_W;
    const f = Math.max(0, Math.min(total, Math.round(x / pxf)));
    onSeek(f);
  };

  return (
    <div className="timeline" onPointerMove={onPointerMove} onPointerUp={endDrag}>
      <div className="tl-scroll" ref={scrollRef} onWheel={onLaneWheel}>
        <div style={{width: LABEL_W + laneW, position: 'relative'}}>
          {/* ruler */}
          <div className="tl-ruler" onMouseDown={seekFromEvent}>
            <div style={{width: LABEL_W, flexShrink: 0}} className="tl-label" />
            <div style={{position: 'relative', width: laneW, height: '100%'}}>
              {Array.from({length: Math.ceil(total / fps) + 1}, (_, s) => (
                <div key={s} className="tl-tick" style={{left: s * fps * pxf}}>
                  {s}s
                </div>
              ))}
              {project.sceneMarkers.map((m) => (
                <div
                  key={m.id}
                  className="tl-marker"
                  style={{left: m.atFrame * pxf}}
                  title={m.label}
                />
              ))}
            </div>
          </div>

          {/* tracks */}
          {project.tracks.map((track) => (
            <div key={track.id} className="tl-row" style={{height: ROW_H}}>
              <div className="tl-label" style={{width: LABEL_W}}>
                <span className={track.hidden ? 'dim' : ''}>{track.name}</span>
                <span className="tl-type">{track.type}</span>
              </div>
              <div
                className="tl-lane"
                style={{width: laneW}}
                onMouseDown={(e) => {
                  if (e.target === e.currentTarget) seekFromEvent(e);
                }}
              >
                {track.clips.map((clip, ci) => {
                  const sel =
                    selection?.trackId === track.id && selection?.clipId === clip.id;
                  const overlapNudge =
                    track.type === 'audio' && ci % 2 === 1 ? 6 : 0;
                  return (
                    <div
                      key={clip.id}
                      className={`tl-clip ${sel ? 'sel' : ''}`}
                      style={{
                        left: clip.from * pxf,
                        width: Math.max(3, clip.durationInFrames * pxf),
                        top: 3 + overlapNudge,
                        height: ROW_H - 8 - overlapNudge,
                        background: KIND_COLORS[clip.kind] ?? '#555',
                      }}
                      onPointerDown={(e) => onClipPointerDown(e, track, clip, 'move')}
                    >
                      <div
                        className="tl-handle l"
                        onPointerDown={(e) => onClipPointerDown(e, track, clip, 'trim-l')}
                      />
                      <span className="tl-clip-label">
                        {clip.kind === 'text'
                          ? (clip as {content?: string}).content
                          : ((clip as {asset?: string}).asset ?? clip.kind)
                              .split('/')
                              .pop()}
                      </span>
                      <div
                        className="tl-handle r"
                        onPointerDown={(e) => onClipPointerDown(e, track, clip, 'trim-r')}
                      />
                    </div>
                  );
                })}
              </div>
            </div>
          ))}

          {/* playhead */}
          <div
            className="tl-playhead"
            style={{left: LABEL_W + playhead * pxf}}
          />
        </div>
      </div>
      <div className="tl-zoom">
        <button onClick={() => setPxPerFrame(pxf / 1.4)}>−</button>
        <span>{pxf.toFixed(1)} px/f</span>
        <button onClick={() => setPxPerFrame(pxf * 1.4)}>+</button>
      </div>
    </div>
  );
};
