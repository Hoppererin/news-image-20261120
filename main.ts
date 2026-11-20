// news-image-20261120 — "The World Today": one image summing up Friday 20 November 2026.
// The image (entry.png, 1024x1024) is rendered in this repo by render.py
// (PIL + DejaVu, deterministic — re-running it writes byte-identical bytes);
// this program only copies it to /output/entry.png. Node 22, standard library
// only, no network, no randomness, no timestamps. It never deletes /output:
// the grader mounts /output, so removing it would fail the run.
// Run locally: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
console.log(`wrote ${join(outDir, "entry.png")}`);
