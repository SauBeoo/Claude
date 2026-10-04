// AssetBin.tsx — per-project assets + shared SFX. Click adds a clip at the
// playhead on a fitting track; drop files to upload into assets/.

import React, {useEffect, useState} from 'react';
import type {Clip, Track} from '../../../../src/schema/project';
import {listAssets, uploadAsset} from '../api';
import {useProject} from '../store/useProject';

const isImg = (r: string) => /\.(png|jpe?g|webp)$/i.test(r);
const isAudio = (r: string) => /\.(wav|mp3|m4a|aac)$/i.test(r);
const isVideo = (r: string) => /\.(mp4|webm|mov)$/i.test(r);

let clipSeq = 0;
const newId = (p: string) => `${p}-${Date.now().toString(36)}-${clipSeq++}`;

export const AssetBin: React.FC = () => {
  const project = useProject((s) => s.project);
  const playhead = useProject((s) => s.playheadFrame);
  const addClip = useProject((s) => s.addClip);
  const addTrack = useProject((s) => s.addTrack);
  const [items, setItems] = useState<{ref: string; size: number}[]>([]);
  const [sfx, setSfx] = useState<{ref: string; size: number}[]>([]);
  const [busy, setBusy] = useState(false);

  const refresh = () => {
    if (!project) return;
    listAssets(project.meta.name)
      .then((r) => {
        setItems(r.assets);
        setSfx(r.sfx);
      })
      .catch(() => {});
  };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(refresh, [project?.meta.name]);

  if (!project) return <div className="assetbin empty">—</div>;

  const findOrMakeTrack = (type: Track['type'], name: string): Track => {
    const existing = project.tracks.find((t) => t.type === type && !t.locked);
    if (existing) return existing;
    const track: Track = {
      id: newId('trk'),
      name,
      type,
      muted: false,
      hidden: false,
      locked: false,
      clips: [],
    };
    addTrack(track);
    return track;
  };

  const addAsset = (ref: string) => {
    const from = Math.round(playhead);
    let clip: Clip;
    let track: Track;
    if (ref.startsWith('sfx/') || isAudio(ref)) {
      track = findOrMakeTrack('audio', 'Audio');
      clip = {
        id: newId('aud'), kind: 'audio', from,
        durationInFrames: ref.startsWith('sfx/') ? 60 : 150,
        asset: ref, volume: ref.startsWith('sfx/') ? 0.45 : 1, trimStartFrames: 0,
      };
    } else if (isVideo(ref)) {
      track = findOrMakeTrack('video', 'Footage');
      clip = {
        id: newId('vid'), kind: 'video', from, durationInFrames: 150,
        asset: ref, trimStartFrames: 0, fit: 'cover', layout: {},
        motion: 'none', volume: 0, fadeInFrames: 0, filter: {},
        wipeInFrames: 0, wipeDir: 'left', speed: 1, mirror: false,
        curlInFrames: 0, curlDir: 'br',
      };
    } else if (isImg(ref)) {
      track = findOrMakeTrack('sticker', 'Stickers');
      clip = {
        id: newId('stk'), kind: 'sticker', from, durationInFrames: 90,
        asset: ref,
        layout: {x: 660, y: 240, w: 600, rotation: 0, opacity: 1},
        entrance: {variant: 'pop', delayFrames: 0, params: {}},
        exit: null, idle: {amp: 5, phase: Math.random() * 6}, shadow: 'lg',
      };
    } else {
      return;
    }
    addClip(track.id, clip);
  };

  const onDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setBusy(true);
    try {
      for (const f of Array.from(e.dataTransfer.files)) {
        await uploadAsset(project.meta.name, f);
      }
      refresh();
    } finally {
      setBusy(false);
    }
  };

  return (
    <div
      className="assetbin"
      onDragOver={(e) => e.preventDefault()}
      onDrop={onDrop}
    >
      <div className="ab-head">Assets {busy ? '(đang tải…)' : ''}</div>
      <div className="ab-grid">
        {items.map((a) => (
          <div key={a.ref} className="ab-item" onClick={() => addAsset(a.ref)} title={a.ref}>
            {isImg(a.ref) ? (
              <img src={`/projects/${project.meta.name}/${a.ref}`} alt="" />
            ) : (
              <span className="ab-file">{a.ref.split('/').pop()}</span>
            )}
          </div>
        ))}
      </div>
      <div className="ab-head">SFX</div>
      <div className="ab-sfx">
        {sfx.map((a) => (
          <button key={a.ref} onClick={() => addAsset(a.ref)}>
            {a.ref.replace('sfx/', '').replace('.wav', '')}
          </button>
        ))}
      </div>
      <div className="ab-hint">Kéo file vào đây để thêm asset · click để đặt vào playhead</div>
    </div>
  );
};
