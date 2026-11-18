// "Sum up 17 November's world news in one image": this program copies the
// poster (entry.png, drawn by tools/make-image.py) to the output directory.
// Node 22, standard library only. It creates the output directory itself,
// so no `mkdir -p` is needed before running it:
//
//   MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });

copyFileSync(
  new URL('./entry.png', import.meta.url),
  join(outDir, 'entry.png'),
);
