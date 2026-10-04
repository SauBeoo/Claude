// PlayerPanel.tsx — realtime preview via @remotion/player bound to the store.
// No write-back: the Player just re-renders whenever project state changes.

import React, {useEffect, useRef} from 'react';
import {Player, type PlayerRef} from '@remotion/player';
import {VoxProject} from '../../../../src/compositions/VoxProject';
import {useProject} from '../store/useProject';

export const PlayerPanel: React.FC<{playerRef: React.RefObject<PlayerRef | null>}> = ({
  playerRef,
}) => {
  const project = useProject((s) => s.project);
  const setPlayhead = useProject((s) => s.setPlayhead);
  const raf = useRef<number>(0);

  // keep the timeline playhead in sync while playing
  useEffect(() => {
    const tick = () => {
      const p = playerRef.current;
      if (p) {
        const f = p.getCurrentFrame();
        if (f != null && f !== useProject.getState().playheadFrame) setPlayhead(f);
      }
      raf.current = requestAnimationFrame(tick);
    };
    raf.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf.current);
  }, [playerRef, setPlayhead]);

  if (!project) return <div className="player-panel empty">—</div>;

  return (
    <div className="player-panel">
      <Player
        ref={playerRef as React.RefObject<PlayerRef>}
        component={VoxProject}
        inputProps={project as unknown as Record<string, unknown>}
        durationInFrames={project.timeline.durationInFrames}
        fps={project.meta.fps}
        compositionWidth={project.meta.width}
        compositionHeight={project.meta.height}
        style={{width: '100%', height: '100%'}}
        controls
        loop
        // mặc định 5 — project beat-edit có nhạc + SFX chồng dày là vượt
        // ngay, Player crash màn đen (bắt được 2026-08-16 ở vlog-auto)
        numberOfSharedAudioTags={32}
        acknowledgeRemotionLicense
      />
    </div>
  );
};
