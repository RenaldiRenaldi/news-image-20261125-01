import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
const out = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
// Resolve entry.png next to THIS script, not process.cwd():
// the grader runs `node /bot/main.ts` from an arbitrary cwd,
// so a cwd-relative path looks for entry.png in the wrong place (ENOENT, exit 1).
const here = dirname(fileURLToPath(import.meta.url));
mkdirSync(out, { recursive: true });
copyFileSync(join(here, "entry.png"), join(out, "entry.png"));
