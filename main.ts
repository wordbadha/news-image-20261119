// THE WORLD TODAY — Thursday, 19 November 2026.
// Round-2 runner: copies the pre-rendered front page (entry.png) into
// the output directory and checks the copy is a whole, valid PNG of
// the size the rules allow. Standard library only; no network, no
// dependencies, nothing to install.

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const SOURCE = new URL("./entry.png", import.meta.url);
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const OUT_FILE = join(OUT_DIR, "entry.png");

const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const MAX_BYTES = 1048576;
const WANT_WIDTH = 1024;
const WANT_HEIGHT = 1024;

function fail(message: string): never {
  console.error(`error: ${message}`);
  process.exit(1);
}

function main(): void {
  mkdirSync(OUT_DIR, { recursive: true });
  copyFileSync(SOURCE, OUT_FILE);

  const data = readFileSync(OUT_FILE);

  if (data.length > MAX_BYTES) {
    fail(`entry.png is ${data.length} bytes, over the ${MAX_BYTES} byte limit`);
  }
  if (!data.subarray(0, 8).equals(PNG_SIGNATURE)) {
    fail("entry.png does not start with the PNG signature");
  }

  // IHDR is the first chunk: a 4-byte length, the letters IHDR, then
  // 13 bytes of header data holding the width and height.
  const ihdrLength = data.readUInt32BE(8);
  const ihdrType = data.toString("ascii", 12, 16);
  if (ihdrLength !== 13 || ihdrType !== "IHDR") {
    fail("entry.png has no IHDR chunk where one belongs");
  }
  const width = data.readUInt32BE(16);
  const height = data.readUInt32BE(20);
  if (width !== WANT_WIDTH || height !== WANT_HEIGHT) {
    fail(`entry.png is ${width}x${height}, expected ${WANT_WIDTH}x${WANT_HEIGHT}`);
  }

  // A whole PNG ends with an IEND chunk: length 0, the letters IEND,
  // and its CRC. Anything shorter is a truncated copy.
  const iendLength = data.readUInt32BE(data.length - 12);
  const iendType = data.toString("ascii", data.length - 8, data.length - 4);
  if (iendLength !== 0 || iendType !== "IEND") {
    fail("entry.png does not end with an IEND chunk");
  }

  const size = statSync(OUT_FILE).size;
  console.log(`wrote ${OUT_FILE} (${size} bytes, ${width}x${height} PNG)`);
}

main();
