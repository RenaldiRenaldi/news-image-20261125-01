import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
const out = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
// Resolve the bundled image from this module's directory, regardless of caller cwd.
const scriptDirectory = dirname(fileURLToPath(import.meta.url));
mkdirSync(out, { recursive: true });
copyFileSync(join(scriptDirectory, "entry.png"), join(out, "entry.png"));
