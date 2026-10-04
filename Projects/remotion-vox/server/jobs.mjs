// jobs.mjs — background job runner (renders, python importers).
// Each job: jobs/<id>/log.txt + EXITCODE file when done (workspace rule
// render-background.md: log file is the evidence, never stdout of a chat turn).

import {spawn} from 'node:child_process';
import {createWriteStream, existsSync, mkdirSync, readFileSync, readdirSync} from 'node:fs';
import {join} from 'node:path';
import {fileURLToPath} from 'node:url';

const JOBS_DIR = fileURLToPath(new URL('../jobs/', import.meta.url));

const jobs = new Map(); // id -> {id, kind, cmd, startedAt, pid, done, exitCode}

const newId = (kind) =>
  `${kind}-${new Date().toISOString().slice(0, 19).replace(/[:T]/g, '')}-${Math.random().toString(36).slice(2, 6)}`;

export const startJob = (kind, command, args, opts = {}) => {
  const id = newId(kind);
  const dir = join(JOBS_DIR, id);
  mkdirSync(dir, {recursive: true});
  const logPath = join(dir, 'log.txt');
  const log = createWriteStream(logPath, {flags: 'a'});
  log.write(`# ${kind}\n# ${command} ${args.join(' ')}\n\n`);

  const child = spawn(command, args, {
    cwd: opts.cwd,
    shell: false,
    windowsHide: true,
    env: {...process.env, PYTHONUNBUFFERED: '1', PYTHONIOENCODING: 'utf-8'},
  });
  const job = {
    id,
    kind,
    startedAt: Date.now(),
    pid: child.pid,
    done: false,
    exitCode: null,
    meta: opts.meta ?? {},
  };
  jobs.set(id, job);

  child.stdout.on('data', (d) => log.write(d));
  child.stderr.on('data', (d) => log.write(d));
  child.on('close', (code) => {
    job.done = true;
    job.exitCode = code;
    log.write(`\nEXITCODE=${code}\n`);
    log.end();
    try {
      // sidecar file so the evidence survives the server process
      createWriteStream(join(dir, 'EXITCODE')).end(String(code));
    } catch {}
    if (opts.onDone) opts.onDone(code);
  });
  child.on('error', (err) => {
    job.done = true;
    job.exitCode = -1;
    log.write(`\nSPAWN ERROR: ${err.message}\nEXITCODE=-1\n`);
    log.end();
  });
  return job;
};

export const getJob = (id) => {
  const job = jobs.get(id);
  const dir = join(JOBS_DIR, id);
  const logPath = join(dir, 'log.txt');
  let logTail = '';
  if (existsSync(logPath)) {
    const txt = readFileSync(logPath, 'utf8');
    logTail = txt.length > 4000 ? txt.slice(-4000) : txt;
  }
  if (job) return {...job, logTail};
  // job from a previous server run — reconstruct from disk
  if (existsSync(dir)) {
    const exitPath = join(dir, 'EXITCODE');
    const exitCode = existsSync(exitPath)
      ? Number(readFileSync(exitPath, 'utf8').trim())
      : null;
    return {id, kind: id.split('-')[0], done: exitCode != null, exitCode, logTail};
  }
  return null;
};

export const listJobs = () => {
  const live = [...jobs.values()].map(({id, kind, startedAt, done, exitCode, meta}) => ({
    id, kind, startedAt, done, exitCode, meta,
  }));
  const onDisk = existsSync(JOBS_DIR)
    ? readdirSync(JOBS_DIR).filter((d) => !jobs.has(d)).map((id) => ({id, kind: id.split('-')[0], done: true}))
    : [];
  return [...live, ...onDisk].slice(-50);
};
