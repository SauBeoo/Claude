// App.tsx — layout: TopBar / AssetBin | Player | Inspector / Timeline.

import React, {useRef} from 'react';
import type {PlayerRef} from '@remotion/player';
import {AssetBin} from './components/AssetBin';
import {ClipToolbar} from './components/ClipToolbar';
import {Inspector} from './components/Inspector';
import {PlayerPanel} from './components/PlayerPanel';
import {Timeline} from './components/Timeline';
import {TopBar} from './components/TopBar';
import {useProject} from './store/useProject';

export const App: React.FC = () => {
  const playerRef = useRef<PlayerRef | null>(null);
  const setPlayhead = useProject((s) => s.setPlayhead);

  const seek = (frame: number) => {
    setPlayhead(frame);
    playerRef.current?.seekTo(frame);
  };

  return (
    <div className="app">
      <TopBar />
      <div className="main">
        <AssetBin />
        <PlayerPanel playerRef={playerRef} />
        <Inspector />
      </div>
      <ClipToolbar />
      <Timeline onSeek={seek} />
    </div>
  );
};
