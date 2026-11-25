// news-image-20261124 entry (Node 22, standard library only).
// The image is entry.png beside this file; the program copies it to the
// output directory, then proves the copy is byte-identical by hashing it
// and reads the image size straight out of the PNG header.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR?.trim() || '/output';
const targetPath = join(outDir, 'entry.png');

const bytes = readFileSync(sourcePath);
// Fail loudly on a corrupt source instead of handing the gate a bad file:
// a whole PNG starts with its 8-byte signature, then the IHDR chunk.
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (bytes.length < 33 || !bytes.subarray(0, 8).equals(PNG_SIGNATURE)
    || bytes.toString('ascii', 12, 16) !== 'IHDR') {
  throw new Error('entry.png is not a whole PNG file');
}
if (!existsSync(outDir)) mkdirSync(outDir, { recursive: true });
writeFileSync(targetPath, bytes);

const roundTrip = readFileSync(targetPath);
const digest = (buf: Buffer) => createHash('sha256').update(buf).digest('hex');
if (digest(roundTrip) !== digest(bytes)) {
  throw new Error('entry.png copy failed the byte-for-byte check');
}

const width = roundTrip.readUInt32BE(16);
const height = roundTrip.readUInt32BE(20);
console.log(`wrote ${targetPath} (${width}x${height}, ${bytes.length} bytes, sha256 ${digest(bytes).slice(0, 16)}…)`);
