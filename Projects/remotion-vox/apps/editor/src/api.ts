// api.ts — thin fetch wrapper for the local server.

import type {Project} from '../../../src/schema/project';

const j = async <T>(r: Response): Promise<T> => {
  if (!r.ok) throw new Error((await r.json().catch(() => ({})))?.error ?? r.statusText);
  return r.json() as Promise<T>;
};

export const listProjects = () =>
  fetch('/api/projects').then((r) => j<{name: string; modifiedMs: number}[]>(r));

export const loadProject = (name: string) =>
  fetch(`/api/projects/${name}`).then((r) => j<unknown>(r));

export const saveProject = (project: Project) =>
  fetch(`/api/projects/${project.meta.name}`, {
    method: 'PUT',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(project),
  }).then((r) => j<{ok: boolean}>(r));

export const listAssets = (name: string) =>
  fetch(`/api/assets/${name}`).then((r) =>
    j<{assets: {ref: string; size: number}[]; sfx: {ref: string; size: number}[]}>(r),
  );

export const uploadAsset = async (name: string, file: File) => {
  const r = await fetch(
    `/api/assets/${name}?filename=${encodeURIComponent(file.name)}`,
    {method: 'POST', body: file},
  );
  return j<{ok: boolean; ref: string}>(r);
};

export const startRender = (project: Project) =>
  fetch('/api/render', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({project}),
  }).then((r) =>
    j<{jobId?: string; cached?: boolean; blocked?: boolean; missing?: string[]; outPath?: string}>(r),
  );

export const getJob = (id: string) =>
  fetch(`/api/jobs/${id}`).then((r) =>
    j<{id: string; done: boolean; exitCode: number | null; logTail: string}>(r),
  );

export type Template = {
  name: string;
  displayName: string;
  theme: Project['theme'];
  captions: {style: string; fontSize: number};
  entranceRotation: string[];
};

export const listTemplates = () =>
  fetch('/api/templates').then((r) => j<Template[]>(r));

export const runImport = (tool: string, args: string[]) =>
  fetch('/api/import', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({tool, args}),
  }).then((r) => j<{jobId: string}>(r));
