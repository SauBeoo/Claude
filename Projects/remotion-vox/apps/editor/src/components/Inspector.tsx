// Inspector.tsx — edit the selected clip's fields by kind.

import React from 'react';
import type {Clip} from '../../../../src/schema/project';
import {ENTRANCE_NAMES} from '../../../../src/effects/entrances';
import {TEXT_ANIMATION_NAMES} from '../../../../src/effects/textAnimations';
import {useProject} from '../store/useProject';

const Num: React.FC<{
  label: string;
  value: number | undefined | null;
  onChange: (v: number) => void;
  step?: number;
}> = ({label, value, onChange, step = 1}) => (
  <label className="insp-field">
    <span>{label}</span>
    <input
      type="number"
      step={step}
      value={value ?? ''}
      onChange={(e) => onChange(Number(e.target.value))}
    />
  </label>
);

const Txt: React.FC<{
  label: string;
  value: string;
  onChange: (v: string) => void;
}> = ({label, value, onChange}) => (
  <label className="insp-field">
    <span>{label}</span>
    <input type="text" value={value} onChange={(e) => onChange(e.target.value)} />
  </label>
);

const Sel: React.FC<{
  label: string;
  value: string;
  options: string[];
  onChange: (v: string) => void;
}> = ({label, value, options, onChange}) => (
  <label className="insp-field">
    <span>{label}</span>
    <select value={value} onChange={(e) => onChange(e.target.value)}>
      {options.map((o) => (
        <option key={o} value={o}>
          {o}
        </option>
      ))}
    </select>
  </label>
);

const CAPTION_STYLES = ['outline', 'box', 'karaoke'];

// shown when no clip is selected — project-level settings (captions...)
const ProjectPanel: React.FC = () => {
  const project = useProject((s) => s.project);
  const updateCaptions = useProject((s) => s.updateCaptions);
  if (!project) return <div className="inspector empty">Chưa mở project</div>;
  const c = project.captions;
  return (
    <div className="inspector">
      <div className="insp-title">Project · phụ đề</div>
      <label className="insp-field">
        <span>bật phụ đề</span>
        <input
          type="checkbox"
          checked={c.enabled}
          onChange={(e) => updateCaptions({enabled: e.target.checked})}
        />
      </label>
      <Sel
        label="style"
        value={c.style}
        options={CAPTION_STYLES}
        onChange={(v) => updateCaptions({style: v})}
      />
      <Num
        label="font size"
        value={c.fontSize}
        onChange={(v) => updateCaptions({fontSize: Math.max(10, v)})}
      />
      <div className="insp-note">
        {c.lines.length} dòng · {c.words.length} từ karaoke
        {c.words.length === 0 && c.lines.length > 0
          ? ' — chạy vv_word_timing.py để có karaoke'
          : ''}
      </div>
      <div className="insp-note">Chọn 1 clip trên timeline để sửa clip.</div>
    </div>
  );
};

export const Inspector: React.FC = () => {
  const project = useProject((s) => s.project);
  const selection = useProject((s) => s.selection);
  const updateClip = useProject((s) => s.updateClip);
  const deleteClip = useProject((s) => s.deleteClip);

  if (!project || !selection) {
    return <ProjectPanel />;
  }
  const track = project.tracks.find((t) => t.id === selection.trackId);
  const clip = track?.clips.find((c) => c.id === selection.clipId);
  if (!track || !clip) return <div className="inspector empty">—</div>;

  const up = (patch: Partial<Clip>) => updateClip(track.id, clip.id, patch);
  const upLayout = (key: string, v: number) =>
    up({layout: {...(clip as {layout?: object}).layout, [key]: v}} as Partial<Clip>);

  return (
    <div className="inspector">
      <div className="insp-title">
        {clip.kind} · <code>{clip.id}</code>
        <button className="danger" onClick={() => deleteClip(track.id, clip.id)}>
          Xoá
        </button>
      </div>

      <Num label="from (frame)" value={clip.from} onChange={(v) => up({from: Math.max(0, Math.round(v))})} />
      <Num
        label="duration (frames)"
        value={clip.durationInFrames}
        onChange={(v) => up({durationInFrames: Math.max(1, Math.round(v))})}
      />

      {clip.kind === 'sticker' && (
        <>
          <Num label="x" value={clip.layout.x} onChange={(v) => upLayout('x', v)} />
          <Num label="y" value={clip.layout.y} onChange={(v) => upLayout('y', v)} />
          <Num label="w" value={clip.layout.w} onChange={(v) => upLayout('w', v)} />
          <Num label="xoay (°)" value={clip.layout.rotation} onChange={(v) => upLayout('rotation', v)} step={0.5} />
          <Num label="opacity" value={clip.layout.opacity} onChange={(v) => upLayout('opacity', v)} step={0.05} />
          <Sel
            label="entrance"
            value={clip.entrance.variant}
            options={ENTRANCE_NAMES}
            onChange={(v) => up({entrance: {...clip.entrance, variant: v}})}
          />
          <Sel
            label="shadow"
            value={clip.shadow}
            options={['lg', 'sm', 'none']}
            onChange={(v) => up({shadow: v as 'lg' | 'sm' | 'none'})}
          />
          <Num
            label="idle amp"
            value={clip.idle.amp}
            onChange={(v) => up({idle: {...clip.idle, amp: v}})}
          />
        </>
      )}

      {clip.kind === 'text' && (
        <>
          <Txt label="nội dung" value={clip.content} onChange={(v) => up({content: v})} />
          <Sel
            label="preset"
            value={clip.preset}
            options={['tag', 'punch', 'plain']}
            onChange={(v) => up({preset: v as 'tag' | 'punch' | 'plain'})}
          />
          <Txt label="màu" value={clip.color} onChange={(v) => up({color: v})} />
          <Sel
            label="animation"
            value={clip.animation}
            options={TEXT_ANIMATION_NAMES}
            onChange={(v) => up({animation: v})}
          />
          <Num
            label="font size"
            value={clip.fontSize}
            onChange={(v) => up({fontSize: v || null})}
          />
          <Num label="x" value={clip.layout.x} onChange={(v) => upLayout('x', v)} />
          <Num label="y" value={clip.layout.y} onChange={(v) => upLayout('y', v)} />
        </>
      )}

      {clip.kind === 'audio' && (
        <>
          <Num label="volume" value={clip.volume} onChange={(v) => up({volume: Math.max(0, v)})} step={0.05} />
          <Num
            label="trim đầu (frames)"
            value={clip.trimStartFrames}
            onChange={(v) => up({trimStartFrames: Math.max(0, Math.round(v))})}
          />
        </>
      )}

      {clip.kind === 'video' && (
        <>
          <Sel
            label="fit"
            value={clip.fit}
            options={['cover', 'contain']}
            onChange={(v) => up({fit: v as 'cover' | 'contain'})}
          />
          <Sel
            label="motion"
            value={clip.motion}
            options={['none', 'pan']}
            onChange={(v) => up({motion: v as 'none' | 'pan'})}
          />
          <Num label="volume" value={clip.volume} onChange={(v) => up({volume: Math.max(0, v)})} step={0.05} />
          <Num
            label="dissolve (frames)"
            value={clip.fadeInFrames}
            onChange={(v) => up({fadeInFrames: Math.max(0, Math.round(v))})}
          />
          <div className="insp-title" style={{marginTop: 8}}>Filter màu</div>
          {(
            [
              ['brightness', 'sáng', 1],
              ['contrast', 'tương phản', 1],
              ['saturate', 'bão hoà', 1],
              ['grayscale', 'đen trắng', 0],
              ['sepia', 'sepia', 0],
              ['blur', 'blur (px)', 0],
            ] as const
          ).map(([key, label, neutral]) => (
            <Num
              key={key}
              label={label}
              value={clip.filter?.[key] ?? neutral}
              step={key === 'blur' ? 1 : 0.05}
              onChange={(v) =>
                up({filter: {...clip.filter, [key]: v}} as Partial<Clip>)
              }
            />
          ))}
        </>
      )}

      {clip.kind === 'background' && (
        <>
          <Txt label="tint" value={clip.tint} onChange={(v) => up({tint: v})} />
          <Num
            label="tint opacity"
            value={clip.tintOpacity}
            onChange={(v) => up({tintOpacity: Math.min(1, Math.max(0, v))})}
            step={0.05}
          />
          <Txt
            label="splash 1"
            value={clip.splash?.[0] ?? ''}
            onChange={(v) => up({splash: [v, clip.splash?.[1] ?? '#ffffff']})}
          />
          <Txt
            label="splash 2"
            value={clip.splash?.[1] ?? ''}
            onChange={(v) => up({splash: [clip.splash?.[0] ?? '#ffffff', v]})}
          />
        </>
      )}
    </div>
  );
};
