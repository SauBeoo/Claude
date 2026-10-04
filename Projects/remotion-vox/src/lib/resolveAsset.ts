// resolveAsset.ts — asset refs in project.json are RELATIVE and namespaced.
//   "assets/el_okra.png"  -> public/projects/<name>/assets/el_okra.png
//   "sfx/pop.wav"         -> public/sfx/pop.wav            (shared library)
//   "shared/foo.png"      -> public/shared/foo.png         (shared library)
// staticFile() resolves identically in Player preview (Vite publicDir points
// at the repo public/) and in `npx remotion render`.

import {staticFile} from 'remotion';

const SHARED_PREFIXES = ['sfx/', 'shared/'];

export const resolveAsset = (projectName: string, ref: string): string => {
  if (SHARED_PREFIXES.some((p) => ref.startsWith(p))) {
    return staticFile(ref);
  }
  return staticFile(`projects/${projectName}/${ref}`);
};

export const isVideoAsset = (ref: string): boolean =>
  /\.(mp4|webm|mov|mkv)$/i.test(ref);
