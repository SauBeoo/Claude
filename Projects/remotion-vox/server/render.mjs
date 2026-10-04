// render.mjs — render queue with content-aware cache.
// Cache key = sha1(canonical project JSON) + (path,size,mtimeMs) of every
// referenced asset — NEVER existence-only (workspace rule §2.5).

import {createHash} from 'node:crypto';
import {existsSync, mkdirSync, readFileSync, statSync, writeFileSync} from 'node:fs';
import {join} from 'node:path';
import {startJob} from './jobs.mjs';

export const makeRenderModule = (ROOT) => {
  const CACHE_PATH = join(ROOT, 'out', '.render_cache.json');

  const assetDiskPath = (projectName, ref) =>
    ref.startsWith('sfx/') || ref.startsWith('shared/')
      ? join(ROOT, 'public', ref)
      : join(ROOT, 'public', 'projects', projectName, ref);

  const collectAssetRefs = (project) => {
    const refs = new Set();
    for (const track of project.tracks ?? []) {
      for (const clip of track.clips ?? []) {
        if (clip.asset) refs.add(clip.asset);
        if (clip.paper) refs.add(clip.paper);
      }
    }
    return [...refs];
  };

  const renderKey = (project) => {
    const h = createHash('sha1');
    h.update(JSON.stringify(project));
    for (const ref of collectAssetRefs(project).sort()) {
      const p = assetDiskPath(project.meta.name, ref);
      if (existsSync(p)) {
        const st = statSync(p);
        h.update(`${ref}:${st.size}:${Math.round(st.mtimeMs)}`);
      } else {
        h.update(`${ref}:MISSING`);
      }
    }
    return h.digest('hex');
  };

  const readCache = () => {
    try {
      return JSON.parse(readFileSync(CACHE_PATH, 'utf8'));
    } catch {
      return {};
    }
  };

  const startRender = (project) => {
    const name = project.meta.name;
    const missing = collectAssetRefs(project).filter(
      (ref) => !existsSync(assetDiskPath(name, ref)),
    );
    if (missing.length > 0) {
      // đủ asset mới được render (workspace rule render-background §1.5)
      return {blocked: true, missing};
    }

    const key = renderKey(project);
    const outPath = join(ROOT, 'out', `${name}.mp4`);
    const cache = readCache();
    if (cache[name] === key && existsSync(outPath)) {
      return {cached: true, outPath: `out/${name}.mp4`};
    }

    mkdirSync(join(ROOT, 'out'), {recursive: true});
    const propsPath = join(ROOT, 'out', `.${name}.props.json`);
    writeFileSync(propsPath, JSON.stringify(project), 'utf8');

    // Node >=21 blocks spawning .cmd with shell:false -> go through cmd.exe
    const isWin = process.platform === 'win32';
    const cmd = isWin ? 'cmd.exe' : 'npx';
    const baseArgs = [
      'remotion', 'render', 'VoxProject',
      `--props=${propsPath}`,
      outPath,
      '--overwrite',
    ];
    const args = isWin ? ['/d', '/s', '/c', 'npx', ...baseArgs] : baseArgs;
    const job = startJob(
      'render',
      cmd,
      args,
      {
        cwd: ROOT,
        meta: {project: name, out: `out/${name}.mp4`},
        onDone: (code) => {
          if (code === 0) {
            const c = readCache();
            c[name] = key;
            writeFileSync(CACHE_PATH, JSON.stringify(c, null, 2), 'utf8');
          }
        },
      },
    );
    return {jobId: job.id, outPath: `out/${name}.mp4`};
  };

  return {startRender};
};
