// Figure fig-01-engine-cycle, built with the Anatomy engine.
// Contract with course-studio:
//   1. `node build.mjs` writes fig-01-engine-cycle.html (dark) and fig-01-engine-cycle-light.html (light).
//   2. `node build.mjs --audit` runs the same build; raptor.mjs audits every recorded solid and exits non-zero on a fault.
//   3. Numbers come from model.mjs, the same source the chapter quotes.
//   4. The card's `fig` is "Fig 1".
// The drawing itself is raptor.mjs (adapted from Anatomy's raptor-engine example); it builds one theme per run.
import { execFileSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
for (const flags of [[], ["--light"]]) {
  execFileSync(process.execPath, [join(HERE, "raptor.mjs"), ...flags], { stdio: "inherit", cwd: HERE });
}
