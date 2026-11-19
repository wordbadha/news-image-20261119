// news-image-20261119 — entrypoint (Node 22).
// Runs the Pillow renderer and drops the finished front page at
// <output-dir>/entry.png. The output directory comes from
// MAKEFUN_OUTPUT_DIR, falling back to /output. The renderer is fully
// deterministic, so two runs write identical bytes.

import { spawnSync } from "node:child_process";
import { existsSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// A PNG is 8 signature bytes, then a 25-byte IHDR chunk: length (4),
// type "IHDR" (4), width (4, big-endian), height (4), and the rest.
const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);

function checkPng(path: string): void {
  const buf = readFileSync(path);
  if (buf.length < 33 || !buf.subarray(0, 8).equals(PNG_SIGNATURE)) {
    throw new Error(`${path} is not a PNG file`);
  }
  if (buf.toString("ascii", 12, 16) !== "IHDR") {
    throw new Error(`${path} has no IHDR chunk where one belongs`);
  }
  const width = buf.readUInt32BE(16);
  const height = buf.readUInt32BE(20);
  if (width !== 1024 || height !== 1024) {
    throw new Error(
      `${path} is ${width}x${height}, expected 1024x1024`,
    );
  }
  if (buf.length > 1048576) {
    throw new Error(`${path} is ${buf.length} bytes, over the 1 MiB limit`);
  }
}

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const script = join(here, "build", "gen_image.py");

const run = spawnSync("python3", [script, outDir], { stdio: "inherit" });
if (run.error) {
  console.error(`failed to start python3: ${run.error.message}`);
  process.exit(1);
}
if (run.status !== 0) {
  console.error(`gen_image.py exited with status ${run.status}`);
  process.exit(run.status ?? 1);
}

const entry = join(outDir, "entry.png");
if (!existsSync(entry)) {
  console.error(`expected output missing: ${entry}`);
  process.exit(1);
}
try {
  checkPng(entry);
} catch (err) {
  console.error(`output failed validation: ${(err as Error).message}`);
  process.exit(1);
}
const { size } = statSync(entry);
console.log(`entry.png ready: ${size} bytes at ${entry}`);
