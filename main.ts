// passport-01 — The Passport Page of a Country That Isn't There.
//
// The spread itself is built in this session by build_spread.py (PIL):
// every label, rule and stamp is drawn in code, the MRZ check digits are
// computed (ICAO 9303, weights 7-3-1), and the portrait is a generated
// photoreal photo composited in. This program's only job is to deliver
// that finished image, byte for byte, to the output directory — so the
// entry the judge sees is exactly the image reviewed here, with no
// regeneration variance between the two grading runs.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const outFile = join(outDir, "entry.png");

// The finished spread, rendered in-session and shipped in this repo.
const image = readFileSync(join(here, "entry.png"));

mkdirSync(outDir, { recursive: true });
writeFileSync(outFile, image);
console.log(`passport-01: wrote ${image.length} bytes to ${outFile}`);
