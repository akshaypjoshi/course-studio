// Figure {{id}} — built with the Anatomy skill.
//
// Contract with course-studio (keep these, replace everything else by following Anatomy's ANATOMY.md
// and its closest example: {{ANATOMY}}/examples/dial-indicator/build.mjs is vendored; the others are
// listed in {{ANATOMY}}/SOURCE.txt):
//   1. Import the kit from the vendored copy: {{ANATOMY}}/kit/iso-kit.mjs
//   2. `node build.mjs` writes BOTH themes next to this file (Anatomy's examples use a `--light`
//      flag instead; here one run makes both, so point Anatomy's capture commands at each file):
//        {{id}}.html        (dark)
//        {{id}}-light.html  (light)
//      build_chapter.py embeds whichever matches the reader's theme.
//   3. `node build.mjs --audit` runs Anatomy's audit when the figure has pipes, cables or round parts.
//   4. The card's `fig` is "Fig n", n = this figure's position in the chapter (see brief.md).
//
import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as k from "{{ANATOMY}}/kit/iso-kit.mjs";
import { kitScript } from "{{ANATOMY}}/scripts/inline-kit.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const ID = "{{id}}";
const WIDTH = 600;
const HEIGHT = 380;

// ---- the model lives in ./model.mjs: every number the figure AND the chapter show comes from it ----
// import { step, initial } from "./model.mjs";

function build(theme) {
  // ---- geometry, painter's order, card: see Anatomy's ANATOMY.md workflow steps 4-8 ----
  const P = k.fitProjection([[-100, -60, 0], [100, 60, 80]], WIDTH, HEIGHT, { pad: 30, azimuth: 45 });
  const art = ""; // solids, lines, dots, wires
  const svg = k.figureSvg({ width: WIDTH, height: HEIGHT, label: "TODO: what the object is and what it shows", body: art });
  const body = k.plateHtml({
    fig: "Fig 1",
    title: "TODO",
    hint: "TODO: the interaction",
    readout: "TODO: live value",
    keys: [],
    caption: "TODO: a true caption with the real numbers",
    body: `<div class="iso-stage" tabindex="0">${svg}</div>`,
  });
  const live = ""; // the live loop (Anatomy references/motion.md)
  const name = theme === "light" ? `${ID}-light.html` : `${ID}.html`;
  writeFileSync(join(HERE, name), k.pageHtml({ title: ID, theme, body, script: kitScript() + live }));
  console.log("wrote", name);
  void P;
}

build("dark");
build("light");
