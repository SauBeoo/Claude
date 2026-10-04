// yawaFont.ts — nạp Noto Serif JP (OFL) cho preset yawa-* trước khi render frame.
// Không nạp kịp thì Chromium vẽ bằng font fallback ở vài frame đầu => chữ "nhảy font".
// Nên chặn render bằng delayRender cho tới khi FontFace load xong.

import {continueRender, delayRender, staticFile} from 'remotion';

export const YAWA_SERIF = '"YawaSerif", "Yu Mincho", "YuMincho", serif';

let started = false;

export const ensureYawaFont = (): void => {
  if (started || typeof document === 'undefined') return;
  started = true;
  const handle = delayRender('load YawaSerif');
  const faces = [
    new FontFace('YawaSerif', `url(${staticFile('shared/fonts/NotoSerifJP-Medium.otf')})`, {weight: '500'}),
    new FontFace('YawaSerif', `url(${staticFile('shared/fonts/NotoSerifJP-SemiBold.otf')})`, {weight: '600'}),
  ];
  Promise.all(faces.map((f) => f.load()))
    .then((loaded) => {
      loaded.forEach((f) => document.fonts.add(f));
      continueRender(handle);
    })
    .catch((err) => {
      console.error('YawaSerif load failed', err);
      continueRender(handle);
    });
};
