// "Sum up 17 November's world news in one image": this program copies the
// poster (entry.png, drawn by tools/make-image.py) to the output directory.
// Node 22, standard library only.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(
  new URL('./entry.png', import.meta.url),
  join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'),
);
