// index.mjs — local editor backend. 127.0.0.1 only, no auth (solo desktop app).
//   GET  /api/projects                 list projects
//   GET  /api/projects/:name           read project.json
//   PUT  /api/projects/:name           save (atomic tmp->rename, keeps .bak)
//   GET  /api/assets/:name             list per-project assets + shared sfx
//   POST /api/assets/:name?filename=x  upload raw body into assets/
//   POST /api/render                   {name} -> background render job
//   POST /api/import                   {tool, args[]} -> python importer job
//   GET  /api/jobs /api/jobs/:id       job status + log tail

import express from 'express';
import {
  copyFileSync, existsSync, mkdirSync, readFileSync, readdirSync,
  renameSync, statSync, writeFileSync,
} from 'node:fs';
import {join, normalize} from 'node:path';
import {fileURLToPath} from 'node:url';
import {getJob, listJobs, startJob} from './jobs.mjs';
import {makeRenderModule} from './render.mjs';

const ROOT = fileURLToPath(new URL('..', import.meta.url));
const PROJECTS = join(ROOT, 'projects');
const PUBLIC = join(ROOT, 'public');
const {startRender} = makeRenderModule(ROOT);

const app = express();
app.use(express.json({limit: '50mb'}));

const safeName = (name) => {
  if (!/^[A-Za-z0-9._-]+$/.test(name)) throw new Error('bad name');
  return name;
};

// ---------------- projects ----------------

app.get('/api/projects', (_req, res) => {
  const out = [];
  if (existsSync(PROJECTS)) {
    for (const d of readdirSync(PROJECTS)) {
      const p = join(PROJECTS, d, 'project.json');
      if (existsSync(p)) {
        const st = statSync(p);
        out.push({name: d, modifiedMs: st.mtimeMs});
      }
    }
  }
  res.json(out.sort((a, b) => b.modifiedMs - a.modifiedMs));
});

app.get('/api/projects/:name', (req, res) => {
  try {
    const p = join(PROJECTS, safeName(req.params.name), 'project.json');
    if (!existsSync(p)) return res.status(404).json({error: 'not found'});
    res.type('json').send(readFileSync(p, 'utf8'));
  } catch (e) {
    res.status(400).json({error: String(e.message)});
  }
});

app.put('/api/projects/:name', (req, res) => {
  try {
    const name = safeName(req.params.name);
    const body = req.body;
    if (!body || body.version !== 1 || body?.meta?.name !== name) {
      return res.status(400).json({error: 'body must be a v1 project whose meta.name matches the URL'});
    }
    body.meta.modifiedAt = new Date().toISOString();
    const dir = join(PROJECTS, name);
    mkdirSync(dir, {recursive: true});
    const target = join(dir, 'project.json');
    if (existsSync(target)) copyFileSync(target, join(dir, 'project.json.bak'));
    const tmp = join(dir, 'project.json.tmp');
    writeFileSync(tmp, JSON.stringify(body, null, 2), 'utf8');
    renameSync(tmp, target); // atomic on same volume
    res.json({ok: true, modifiedAt: body.meta.modifiedAt});
  } catch (e) {
    res.status(400).json({error: String(e.message)});
  }
});

// ---------------- assets ----------------

app.get('/api/assets/:name', (req, res) => {
  try {
    const name = safeName(req.params.name);
    const dir = join(PUBLIC, 'projects', name, 'assets');
    const assets = existsSync(dir)
      ? readdirSync(dir)
          .filter((f) => !f.startsWith('.'))
          .map((f) => ({ref: `assets/${f}`, size: statSync(join(dir, f)).size}))
      : [];
    const sfxDir = join(PUBLIC, 'sfx');
    const sfx = existsSync(sfxDir)
      ? readdirSync(sfxDir)
          .filter((f) => f.endsWith('.wav'))
          .map((f) => ({ref: `sfx/${f}`, size: statSync(join(sfxDir, f)).size}))
      : [];
    res.json({assets, sfx});
  } catch (e) {
    res.status(400).json({error: String(e.message)});
  }
});

app.post(
  '/api/assets/:name',
  express.raw({type: '*/*', limit: '500mb'}),
  (req, res) => {
    try {
      const name = safeName(req.params.name);
      const filename = String(req.query.filename ?? '');
      if (!/^[^\\/:*?"<>|]+$/.test(filename) || filename.startsWith('.')) {
        return res.status(400).json({error: 'bad filename'});
      }
      const dir = join(PUBLIC, 'projects', name, 'assets');
      mkdirSync(dir, {recursive: true});
      const target = normalize(join(dir, filename));
      if (!target.startsWith(dir)) return res.status(400).json({error: 'path escape'});
      writeFileSync(target, req.body);
      res.json({ok: true, ref: `assets/${filename}`});
    } catch (e) {
      res.status(400).json({error: String(e.message)});
    }
  },
);

// ---------------- render + import jobs ----------------

app.post('/api/render', (req, res) => {
  try {
    const project = req.body?.project;
    if (!project?.meta?.name) return res.status(400).json({error: 'need {project}'});
    safeName(project.meta.name);
    res.json(startRender(project));
  } catch (e) {
    res.status(400).json({error: String(e.message)});
  }
});

const IMPORT_TOOLS = new Set([
  'import_pipeline.py',
  'auto_collage.py',
  'import_caption_job.py',
  'vv_word_timing.py',
  'export_srt.py',
  'auto_vlog.py',
]);

app.post('/api/import', (req, res) => {
  try {
    const {tool, args = []} = req.body ?? {};
    if (!IMPORT_TOOLS.has(tool)) return res.status(400).json({error: 'unknown tool'});
    if (!Array.isArray(args) || args.some((a) => typeof a !== 'string')) {
      return res.status(400).json({error: 'args must be string[]'});
    }
    const py = process.platform === 'win32' ? 'py' : 'python3';
    const pyArgs =
      process.platform === 'win32'
        ? ['-3', join(ROOT, 'tools', tool), ...args]
        : [join(ROOT, 'tools', tool), ...args];
    const job = startJob('import', py, pyArgs, {cwd: ROOT, meta: {tool}});
    res.json({jobId: job.id});
  } catch (e) {
    res.status(400).json({error: String(e.message)});
  }
});

app.get('/api/templates', (_req, res) => {
  const dir = join(ROOT, 'templates');
  if (!existsSync(dir)) return res.json([]);
  const out = readdirSync(dir)
    .filter((f) => f.endsWith('.json'))
    .map((f) => JSON.parse(readFileSync(join(dir, f), 'utf8')));
  res.json(out);
});

app.get('/api/jobs', (_req, res) => res.json(listJobs()));
app.get('/api/jobs/:id', (req, res) => {
  const job = getJob(req.params.id);
  if (!job) return res.status(404).json({error: 'not found'});
  res.json(job);
});

const PORT = 7788;
app.listen(PORT, '127.0.0.1', () => {
  console.log(`remotion-vox server: http://127.0.0.1:${PORT}`);
});
