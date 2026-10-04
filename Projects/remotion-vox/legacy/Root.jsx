import React from 'react';
import {Composition} from 'remotion';
import {OkuraDemo, OKURA_CANVAS, OKURA_TOTAL_FRAMES} from './OkuraDemo';

export const Root = () => {
  return (
    <>
      <Composition
        id="OkuraDemo"
        component={OkuraDemo}
        durationInFrames={OKURA_TOTAL_FRAMES}
        fps={30}
        width={OKURA_CANVAS.width}
        height={OKURA_CANVAS.height}
      />
    </>
  );
};
