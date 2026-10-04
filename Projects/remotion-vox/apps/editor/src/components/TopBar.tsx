// TopBar.tsx — project picker, save, undo/redo, render with job progress.

import React, {useEffect, useRef, useState} from 'react';
import {
  getJob, listProjects, listTemplates, loadProject, saveProject, startRender,
  type Template,
} from '../api';
import {redo, undo, useProject} from '../store/useProject';
import {NewProject} from './NewProject';

export const TopBar: React.FC = () => {
  const project = useProject((s) => s.project);
  const dirty = useProject((s) => s.dirty);
  const load = useProject((s) => s.loadProject);
  const markSaved = useProject((s) => s.markSaved);
  const [names, setNames] = useState<string[]>([]);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [showNew, setShowNew] = useState(false);
  const [renderState, setRenderState] = useState<string>('');
  const pollRef = useRef<number>(0);

  const refreshList = () =>
    listProjects().then((l) => setNames(l.map((p) => p.name))).catch(() => {});

  useEffect(() => {
    refreshList();
    listTemplates().then(setTemplates).catch(() => {});
  }, []);

  const applyTemplate = (name: string) => {
    const t = templates.find((x) => x.name === name);
    const p = useProject.getState().project;
    if (!t || !p) return;
    useProject.setState({
      project: {
        ...p,
        meta: {...p.meta, templateRef: t.name, channel: t.name},
        theme: t.theme,
        captions: {...p.captions, style: t.captions.style, fontSize: t.captions.fontSize},
      },
      dirty: true,
    });
  };

  const open = async (name: string) => {
    if (!name) return;
    const raw = await loadProject(name);
    load(raw);
  };

  const save = async () => {
    if (!project) return;
    await saveProject(project);
    markSaved();
  };

  // autosave: debounce 2s after any dirty change
  useEffect(() => {
    if (!dirty || !project) return;
    const t = window.setTimeout(save, 2000);
    return () => window.clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dirty, project]);

  const render = async () => {
    if (!project) return;
    await save();
    const r = await startRender(project);
    if (r.blocked) {
      setRenderState(`🔴 thiếu asset: ${r.missing?.join(', ')}`);
      return;
    }
    if (r.cached) {
      setRenderState(`✅ cache: ${r.outPath}`);
      return;
    }
    setRenderState('⏳ render…');
    const poll = async () => {
      const job = await getJob(r.jobId!);
      const m = job.logTail.match(/Rendered (\d+)\/(\d+)/g);
      const last = m?.[m.length - 1];
      if (job.done) {
        setRenderState(
          job.exitCode === 0 ? `✅ xong: ${r.outPath}` : `🔴 lỗi (exit ${job.exitCode}) — xem jobs/${job.id}/log.txt`,
        );
        return;
      }
      setRenderState(`⏳ ${last ?? 'render…'}`);
      pollRef.current = window.setTimeout(poll, 1500);
    };
    poll();
  };

  useEffect(() => () => window.clearTimeout(pollRef.current), []);

  // keyboard: Ctrl+Z / Ctrl+Y / Ctrl+S
  useEffect(() => {
    const h = (e: KeyboardEvent) => {
      if (!e.ctrlKey) return;
      const k = e.key.toLowerCase();
      if (k === 'z') {
        e.preventDefault();
        undo();
      } else if (k === 'y') {
        e.preventDefault();
        redo();
      } else if (k === 's') {
        e.preventDefault();
        save();
      }
    };
    window.addEventListener('keydown', h);
    return () => window.removeEventListener('keydown', h);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [project]);

  return (
    <div className="topbar">
      <strong className="brand">remotion-vox</strong>
      <button onClick={() => setShowNew(true)}>➕ Mới</button>
      <select value={project?.meta.name ?? ''} onChange={(e) => open(e.target.value)}>
        <option value="">— mở project —</option>
        {names.map((n) => (
          <option key={n} value={n}>
            {n}
          </option>
        ))}
      </select>
      <select
        value={project?.meta.templateRef ?? ''}
        onChange={(e) => applyTemplate(e.target.value)}
        disabled={!project}
        title="Áp template kênh (palette + caption style)"
      >
        <option value="">— template —</option>
        {templates.map((t) => (
          <option key={t.name} value={t.name}>
            {t.name}
          </option>
        ))}
      </select>
      <button onClick={save} disabled={!project}>
        Lưu{dirty ? ' •' : ''}
      </button>
      <button onClick={() => undo()} disabled={!project}>↩ Undo</button>
      <button onClick={() => redo()} disabled={!project}>↪ Redo</button>
      <button className="primary" onClick={render} disabled={!project}>
        🎬 Render
      </button>
      <span className="render-state">{renderState}</span>
      {showNew ? (
        <NewProject
          onClose={() => setShowNew(false)}
          onCreated={async (name) => {
            setShowNew(false);
            await refreshList();
            await open(name);
          }}
        />
      ) : null}
    </div>
  );
};
