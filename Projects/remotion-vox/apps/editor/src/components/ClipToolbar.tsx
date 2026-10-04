// ClipToolbar.tsx — CapCut-style insert bar above the timeline: drop a new
// Text / Tag / Punch / Background / BGM clip at the playhead. Sticker/footage
// clips are added from the AssetBin (click an asset).

import React, {useRef} from 'react';
import type {Clip} from '../../../../src/schema/project';
import {uploadAsset} from '../api';
import {useProject} from '../store/useProject';

let seq = 0;
const newId = (p: string) => `${p}-${Date.now().toString(36)}-${seq++}`;

export const ClipToolbar: React.FC = () => {
  const project = useProject((s) => s.project);
  const playhead = useProject((s) => s.playheadFrame);
  const addClip = useProject((s) => s.addClip);
  const ensureTrack = useProject((s) => s.ensureTrack);
  const bgmInput = useRef<HTMLInputElement>(null);

  if (!project) return null;
  const from = Math.round(playhead);
  const total = project.timeline.durationInFrames;
  const defDur = Math.max(30, Math.min(150, total - from));

  const addText = (preset: 'plain' | 'tag' | 'punch') => {
    const track = ensureTrack('text', 'Text');
    if (!track) return;
    const contents = {plain: 'テキスト', tag: 'タグ', punch: 'パンチライン'};
    const clip: Clip = {
      id: newId('txt'),
      kind: 'text',
      from,
      durationInFrames: defDur,
      content: contents[preset],
      preset,
      color: '#FFE01B',
      animation: 'pop',
      animationParams: {},
      layout: preset === 'plain' ? {x: 660, y: 480} : {},
      fontSize: null,
    };
    addClip(track.id, clip);
  };

  const addBackground = () => {
    const track = ensureTrack('background', 'Background');
    if (!track) return;
    const clip: Clip = {
      id: newId('bg'),
      kind: 'background',
      from,
      durationInFrames: defDur,
      paper: null,
      tint: '#F2EDE4',
      tintOpacity: 0.55,
      grid: true,
      dots: true,
      splash: ['#7CB518', '#4EC3E0'],
    };
    addClip(track.id, clip);
  };

  const addBgm = async (file: File) => {
    const {ref} = await uploadAsset(project.meta.name, file);
    const track = ensureTrack('audio', 'BGM');
    if (!track) return;
    const clip: Clip = {
      id: newId('bgm'),
      kind: 'audio',
      from: 0,
      durationInFrames: total,
      asset: ref,
      // −40dB (luật BGM toàn hệ thống) = gain 0.01
      volume: 0.01,
      trimStartFrames: 0,
    };
    addClip(track.id, clip);
  };

  return (
    <div className="clip-toolbar">
      <span className="ct-label">➕ tại playhead:</span>
      <button onClick={() => addText('plain')}>T Text</button>
      <button onClick={() => addText('tag')}>🏷 Tag</button>
      <button onClick={() => addText('punch')}>💬 Punch</button>
      <button onClick={addBackground}>🎨 Nền</button>
      <button onClick={() => bgmInput.current?.click()}>🎵 BGM</button>
      <input
        ref={bgmInput}
        type="file"
        accept="audio/*"
        style={{display: 'none'}}
        onChange={(e) => {
          const f = e.target.files?.[0];
          if (f) addBgm(f);
          e.target.value = '';
        }}
      />
      <span className="ct-hint">ảnh/clip/SFX → click bên Assets</span>
    </div>
  );
};
