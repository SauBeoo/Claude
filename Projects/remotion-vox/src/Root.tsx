// Root.tsx — exactly ONE generic composition. Adding a video = adding a
// projects/<name>/project.json, NOT a new JSX file. defaultProps points at
// the demo so Studio opens something; render any project with:
//   npx remotion render VoxProject --props=projects/<name>/project.json out/<name>.mp4

import React from 'react';
import {Composition} from 'remotion';
import {VoxProject, calculateVoxMetadata} from './compositions/VoxProject';
import okuraDemo from '../projects/okura-demo/project.json';

export const Root: React.FC = () => (
  <Composition
    id="VoxProject"
    component={VoxProject}
    calculateMetadata={calculateVoxMetadata}
    // placeholders — calculateMetadata overrides from project.json
    durationInFrames={1}
    fps={30}
    width={1920}
    height={1080}
    defaultProps={okuraDemo as Record<string, unknown>}
  />
);
