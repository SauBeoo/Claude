// useProject.ts — editor state. zustand + zundo temporal (undo/redo).
// The project object here is ALWAYS a parsed, valid Project — mutations go
// through produce-style copies; history snapshots only the project.

import {create} from 'zustand';
import {temporal} from 'zundo';
import type {Clip, Project, Track} from '../../../../src/schema/project';
import {parseProject} from '../../../../src/schema/project';

export type Selection = {trackId: string; clipId: string} | null;

type EditorState = {
  project: Project | null;
  selection: Selection;
  playheadFrame: number;
  dirty: boolean;
  pxPerFrame: number;

  loadProject: (raw: unknown) => void;
  select: (sel: Selection) => void;
  setPlayhead: (f: number) => void;
  setPxPerFrame: (v: number) => void;
  markSaved: () => void;

  updateClip: (trackId: string, clipId: string, patch: Partial<Clip>) => void;
  deleteClip: (trackId: string, clipId: string) => void;
  addClip: (trackId: string, clip: Clip) => void;
  addTrack: (track: Track) => void;
  ensureTrack: (type: Track['type'], name: string) => Track | null;
  setDuration: (frames: number) => void;
  updateCaptions: (patch: Partial<Project['captions']>) => void;
};

const touch = (p: Project): Project => ({...p});

export const useProject = create<EditorState>()(
  temporal(
    (set, get) => ({
      project: null,
      selection: null,
      playheadFrame: 0,
      dirty: false,
      pxPerFrame: 2,

      loadProject: (raw) =>
        set({project: parseProject(raw), selection: null, playheadFrame: 0, dirty: false}),
      select: (selection) => set({selection}),
      setPlayhead: (playheadFrame) => set({playheadFrame}),
      setPxPerFrame: (pxPerFrame) =>
        set({pxPerFrame: Math.min(12, Math.max(0.3, pxPerFrame))}),
      markSaved: () => set({dirty: false}),

      updateClip: (trackId, clipId, patch) => {
        const p = get().project;
        if (!p) return;
        set({
          project: touch({
            ...p,
            tracks: p.tracks.map((t) =>
              t.id !== trackId
                ? t
                : {
                    ...t,
                    clips: t.clips.map((c) =>
                      c.id === clipId ? ({...c, ...patch} as Clip) : c,
                    ),
                  },
            ),
          }),
          dirty: true,
        });
      },

      deleteClip: (trackId, clipId) => {
        const p = get().project;
        if (!p) return;
        set({
          project: touch({
            ...p,
            tracks: p.tracks.map((t) =>
              t.id !== trackId
                ? t
                : {...t, clips: t.clips.filter((c) => c.id !== clipId)},
            ),
          }),
          selection: null,
          dirty: true,
        });
      },

      addClip: (trackId, clip) => {
        const p = get().project;
        if (!p) return;
        set({
          project: touch({
            ...p,
            tracks: p.tracks.map((t) =>
              t.id !== trackId ? t : {...t, clips: [...t.clips, clip]},
            ),
          }),
          selection: {trackId, clipId: clip.id},
          dirty: true,
        });
      },

      addTrack: (track) => {
        const p = get().project;
        if (!p) return;
        set({project: touch({...p, tracks: [...p.tracks, track]}), dirty: true});
      },

      ensureTrack: (type, name) => {
        const p = get().project;
        if (!p) return null;
        const existing = p.tracks.find((t) => t.type === type && !t.locked);
        if (existing) return existing;
        const track: Track = {
          id: `trk-${type}-${Date.now().toString(36)}`,
          name,
          type,
          muted: false,
          hidden: false,
          locked: false,
          clips: [],
        };
        set({project: touch({...p, tracks: [...p.tracks, track]}), dirty: true});
        return track;
      },

      updateCaptions: (patch) => {
        const p = get().project;
        if (!p) return;
        set({
          project: touch({...p, captions: {...p.captions, ...patch}}),
          dirty: true,
        });
      },

      setDuration: (frames) => {
        const p = get().project;
        if (!p) return;
        set({
          project: touch({
            ...p,
            timeline: {...p.timeline, durationInFrames: Math.max(1, Math.round(frames))},
          }),
          dirty: true,
        });
      },
    }),
    {
      partialize: (s) => ({project: s.project}),
      equality: (a, b) => a.project === b.project,
      limit: 200,
    },
  ),
);

export const undo = () => useProject.temporal.getState().undo();
export const redo = () => useProject.temporal.getState().redo();

// pause/resume history grouping while dragging (snapshot only on pointer-up)
export const pauseHistory = () => useProject.temporal.getState().pause();
export const resumeHistory = () => useProject.temporal.getState().resume();
