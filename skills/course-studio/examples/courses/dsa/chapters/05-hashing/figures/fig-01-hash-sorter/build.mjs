// Figure fig-01-hash-sorter, built with the Anatomy skill.
//
// Contract with course-studio:
//   1. Imports the kit from the vendored copy: ../../../../../_anatomy/kit/iso-kit.mjs
//   2. `node build.mjs` writes BOTH themes next to this file: fig-01-hash-sorter.html (dark), -light.html (light)
//   3. `node build.mjs --audit` runs Anatomy's audit (the figure has round parts: posts, feet, dial).
//   4. The card's `fig` is "Fig 1".
//
// The object: a gantry tray sorter. A hash dial (8 stops) shows k % 8, a shuttle on an overhead beam
// carries one key tile straight to that tray and drops it; tiles that collide stack in one tray.
import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as k from "../../../../../_anatomy/kit/iso-kit.mjs";
import * as A from "../../../../../_anatomy/kit/audit.mjs";
import { kitScript } from "../../../../../_anatomy/scripts/inline-kit.mjs";
import { M, SETS, STATES, readoutAt } from "./model.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const ID = "fig-01-hash-sorter";
const WIDTH = 600;
const HEIGHT = 380;

// ---- world (units ≈ px), z up ----
const PLATE = { x: -160, y: -58, w: 328, d: 116, r: 8 };
const PLATE_H = 12, FOOT_H = 5;
const PITCH = 27;
const TX = (i) => -54 + PITCH * i; // tray centres: -54 … 135
const BED = { x: -70, y: -22, w: 221, d: 44, r: 2 };
const BED_H = 3;
const TRAY = { w: 24, d: 34, wall: 1.6, h: 6 }; // walls z 3 … 9: stacks rise above them
const FLOOR_TOP = BED_H + 2;
const WALL_TOP = BED_H + TRAY.h;
const TILE = { w: 17, d: 24, h: 5, gap: 0.5 };
const tileZ = (n) => FLOOR_TOP + n * (TILE.h + TILE.gap);
const BEAM_Y = -40, BEAM_Z = 76, BEAM_TOP = 84;
const POSTS = [-92, 156];
const HOME = -84;
const HEAD_BOTTOM = 80;
const CARRY = 48; // tile bottom while travelling
const GRIP_H = 2.4;
const DIAL = [-120, 24], DIAL_R = 17, DIAL_Z = 22, DIAL_H = 7, DIAL_TOP = DIAL_Z + DIAL_H;

const P = k.fitProjection(
  [...k.boxCorners(PLATE, -PLATE_H - FOOT_H, 0), [POSTS[0], BEAM_Y - 8, BEAM_TOP + 12], [POSTS[1] + 8, BEAM_Y, BEAM_TOP + 4]],
  WIDTH, HEIGHT, { pad: 26, azimuth: 58 },
);

const at = (p) => k.iso(p, P);
const S = (paths, style) => k.solidSvg(paths, style);
const L = (d, style) => k.lineSvg(d, style);
const D = (pts, style) => k.dotsSvg(pts, style);
const byDepth = (pts) => [...pts].sort((a, b) => k.depthOf([a[0], a[1], 0], P) - k.depthOf([b[0], b[1], 0], P));

// ---- recorder: every static part is an item with its true shape, in drawing order ----
const R = A.recorder(P);
let order = 0;
const put = (name, svg, shapes) => R.put({ name, key: order++, svg, shapes: shapes.map((s) => R.solid(s)) });

function base() {
  for (const [x, y] of byDepth(k.corners(PLATE, 22))) {
    put("stand.foot", S(k.cylinder(x, y, 7, -PLATE_H - FOOT_H, 1.6, P, 28), { tone: "lo" }) + S(k.cylinder(x, y, 5.4, -PLATE_H - FOOT_H + 1.6, FOOT_H - 1.6, P, 28), { tone: "mid" }),
      [A.cylinder(x, y, 7, -PLATE_H - FOOT_H, 1.6, { name: "stand.foot", ground: true }), A.cylinder(x, y, 5.4, -PLATE_H - FOOT_H + 1.6, FOOT_H - 1.6, { name: "stand.foot.post", ground: true })]);
  }
  const screws = k.corners(PLATE, 10);
  put("stand.plate",
    S(k.slabOf(PLATE, -PLATE_H, PLATE_H, P, 8, 1.6), { tone: "mid" }) +
    L(k.planOutline(k.insetPlan(PLATE, 5), 0, P), { tone: "lo" }) +
    L(screws.map(([x, y]) => k.ring(x, y, 2.2, 0, P, 16)).join(""), { tone: "lo" }) +
    D(screws.map(([x, y]) => at([x, y, 0])), { size: 0.5 }),
    [A.slab(PLATE, -PLATE_H, PLATE_H, { name: "stand.plate", ground: true })]);
  // slot ruler: a major tick under every tray centre, the zero mark under tray 0
  const strip = { x: -66, y: 27, w: 213, d: 7, r: 1 };
  const t = k.topTicks(-63, 144, 9, 3, strip.y + 0.8, 0.6, [2, 3.6], P);
  put("ruler",
    S(k.slabOf(strip, 0, 0.6, P, 3), { tone: "lo", crease: "none" }) + L(t.minor, { tone: "lo" }) + L(t.major, { tone: "mid" }) +
    L(k.lineOnTop([TX(0), strip.y + 0.8], [TX(0), strip.y + 5.4], 0.6, P), { tone: "hi" }) +
    D([at([strip.x + 1.8, strip.y + 3.5, 0.6]), at([strip.x + strip.w - 1.8, strip.y + 3.5, 0.6])], { size: 0.45 }),
    [A.slab(strip, 0, 0.6, { name: "ruler" }, 3)]);
  // label plate with rule lines (they stand for printed text)
  const lp = { x: 98, y: 40, w: 46, d: 11, r: 1.2 };
  put("label",
    S(k.slabOf(lp, 0, 0.8, P, 4), { tone: "mid" }) + L(k.planOutline(k.insetPlan(lp, 1.6), 0.8, P), { tone: "faint" }) +
    L([[lp.x + 6, lp.y + 3.6, 30], [lp.x + 6, lp.y + 5.6, 22], [lp.x + 6, lp.y + 7.6, 26]].map(([x, y, w]) => k.lineOnTop([x, y], [x + w, y], 0.8, P)).join(""), { tone: "lo", free: true }) +
    D([at([lp.x + 3, lp.y + lp.d / 2, 0.8]), at([lp.x + lp.w - 3, lp.y + lp.d / 2, 0.8])], { size: 0.45 }),
    [A.slab(lp, 0, 0.8, { name: "label" }, 4)]);
  // tray bed with screws at its corners
  put("bed",
    S(k.slabOf(BED, 0, BED_H, P, 3, 0.5), { tone: "mid" }) +
    D([BED.x + 4, BED.x + BED.w - 4].flatMap((x) => [at([x, BED.y + 4, BED_H]), at([x, BED.y + BED.d - 4, BED_H])]), { size: 0.45 }),
    [A.slab(BED, 0, BED_H, { name: "bed" }, 3)]);
}

function post(x) {
  const y = BEAM_Y;
  put("post",
    S(k.cylinder(x, y, 7.5, 0, 3, P, 32), { tone: "mid" }) +
    S(k.cylinder(x, y, 4.2, 3, BEAM_Z - 7, P, 28), { tone: "mid", crease: "none" }) +
    L([26, 52].map((z) => k.sideArc(x, y, 4.2, z, P, 16)).join(""), { tone: "faint" }) +
    S(k.cylinder(x, y, 5.6, BEAM_Z - 4, 4, P, 28), { tone: "mid" }),
    [A.cylinder(x, y, 7.5, 0, 3, { name: "post.foot" }), A.cylinder(x, y, 4.2, 3, BEAM_Z - 7, { name: "post" }), A.cylinder(x, y, 5.6, BEAM_Z - 4, 4, { name: "post.cap" })]);
}

function beam() {
  const plan = { x: -100, y: BEAM_Y - 5, w: 264, d: 10, r: 1.5 };
  const stops = [-100, 159].map((x) => ({ x, y: BEAM_Y - 6, w: 5, d: 12, r: 1 }));
  put("beam",
    S(k.slabOf(plan, BEAM_Z, BEAM_TOP - BEAM_Z, P, 3, 0.5), { tone: "mid", inner: L(k.sideSeam(plan, BEAM_Z + 4, P, 3), { tone: "faint" }) }) +
    stops.map((s) => S(k.slabOf(s, BEAM_TOP, 5, P, 2, 0.4), { tone: "mid" }) + D([at([s.x + 2.5, BEAM_Y - 3, BEAM_TOP + 5]), at([s.x + 2.5, BEAM_Y + 3, BEAM_TOP + 5])], { size: 0.45 })).join("") +
    D(POSTS.map((x) => at([x, BEAM_Y, BEAM_TOP])), { size: 0.5 }),
    [A.slab(plan, BEAM_Z, BEAM_TOP - BEAM_Z, { name: "beam" }, 3), ...stops.map((s) => A.slab(s, BEAM_TOP, 5, { name: "beam.stop" }, 2))]);
}

// One tray: floor, far walls, [stack], [in-flight slot], near walls. Five tiles are pre-built per tray and shown per state.
function tile(cx, z) {
  const plan = { x: cx - TILE.w / 2, y: -TILE.d / 2, w: TILE.w, d: TILE.d, r: 1.2 };
  return S(k.slabOf(plan, z, TILE.h, P, 3, 0.4), { tone: "hi", crease: "lo" });
}
function trays() {
  const order = [...Array(M).keys()].sort((a, b) => k.depthOf([TX(a), 0, 0], P) - k.depthOf([TX(b), 0, 0], P));
  for (const i of order) {
    const cx = TX(i), w = TRAY.wall, x0 = cx - TRAY.w / 2, y0 = -TRAY.d / 2;
    const floor = { x: x0 + w, y: y0 + w, w: TRAY.w - 2 * w, d: TRAY.d - 2 * w, r: 0.6 };
    const back = { x: x0, y: y0, w: TRAY.w, d: w, r: 0.5 };
    const left = { x: x0, y: y0 + w, w, d: TRAY.d - 2 * w, r: 0.3 };
    const right = { x: x0 + TRAY.w - w, y: y0 + w, w, d: TRAY.d - 2 * w, r: 0.3 };
    const front = { x: x0, y: y0 + TRAY.d - w, w: TRAY.w, d: w, r: 0.5 };
    const wall = (p) => S(k.slabOf(p, BED_H, TRAY.h, P, 2, 0), { tone: "mid" });
    const stack = Array.from({ length: 5 }, (_, n) => `<g data-tile="${i}-${n}" style="display:none">${tile(cx, tileZ(n))}</g>`).join("");
    const rivets = D([at([x0 + 3, y0 + TRAY.d, WALL_TOP - 2]), at([x0 + TRAY.w - 3, y0 + TRAY.d, WALL_TOP - 2])], { size: 0.4 });
    put(`tray.${i}`,
      S(k.slabOf(floor, BED_H, 2, P, 2), { tone: "lo" }) + L(k.planOutline(k.insetPlan(floor, 2.5), FLOOR_TOP, P, 2), { tone: "faint" }) +
      wall(back) + wall(left) + `<g data-stack="${i}">${stack}</g><g data-slot="${i}"></g>` + wall(right) + wall(front) + rivets,
      [A.slab(floor, BED_H, 2, { name: "tray.floor" }, 2), ...[back, left, right, front].map((p) => A.slab(p, BED_H, TRAY.h, { name: "tray.wall" }, 2))]);
  }
}

function needleAt(slot) {
  const a = (slot / M) * Math.PI * 2, [x, y] = DIAL;
  return k.lineOnTop([x - Math.sin(a) * 3.4, y + Math.cos(a) * 3.4], [x + Math.sin(a) * (DIAL_R - 4), y - Math.cos(a) * (DIAL_R - 4)], DIAL_TOP + 0.2, P);
}
function dial() {
  const [x, y] = DIAL;
  const ticks = k.radialTicks(x, y, DIAL_R - 3, 40, 5, DIAL_TOP, [1.3, 3], P);
  put("dial",
    S(k.cylinder(x, y, 10, 0, 3, P, 32), { tone: "mid" }) +
    S(k.cylinder(x, y, 5, 3, DIAL_Z - 3, P, 24), { tone: "mid", crease: "none" }) +
    L(k.sideArc(x, y, 5, 12, P, 16), { tone: "faint" }) +
    S(k.cylinder(x, y, DIAL_R, DIAL_Z, DIAL_H, P, 64, 0.8), { tone: "hi", crease: "lo" }) +
    L(k.knurl(x, y, DIAL_R, DIAL_TOP - 3, DIAL_TOP, 84, P, 0.3), { tone: "lo" }) +
    L(k.sideArc(x, y, DIAL_R, DIAL_TOP - 3, P, 40), { tone: "faint" }) +
    L(k.ring(x, y, DIAL_R - 2.2, DIAL_TOP, P, 64), { tone: "lo" }) +
    L(ticks.minor, { tone: "lo" }) + L(ticks.major, { tone: "mid" }) +
    k.faceTextSvg(k.topMatrix([x, y + 8.5], DIAL_TOP, P, "x"), "k mod 8", { size: 2.6, tone: "lo", anchor: "middle" }) +
    `<path data-part="needle" class="iso-line" data-tone="lit" data-free="start" d="${needleAt(0)}" style="stroke-width:1.1"/>` +
    L(k.ring(x, y, 1.6, DIAL_TOP, P, 16), { tone: "mid" }) + D([at([x, y, DIAL_TOP])], { size: 0.5 }),
    [A.cylinder(x, y, 10, 0, 3, { name: "dial.foot" }), A.cylinder(x, y, 5, 3, DIAL_Z - 3, { name: "dial.post" }), A.cylinder(x, y, DIAL_R, DIAL_Z, DIAL_H, { name: "dial" })]);
}

// ---- moving parts, built once at x = 0 and moved with translateAlong ----
function shuttle() {
  const body = { x: -11, y: BEAM_Y - 8, w: 22, d: 16, r: 2 };
  const arm = { x: -4, y: BEAM_Y + 8, w: 8, d: 36, r: 1.5 };
  return [
    S(k.slabOf(body, BEAM_TOP, 10, P, 3, 0.5), { tone: "mid" }),
    D([[-7, BEAM_Y - 5], [7, BEAM_Y - 5], [-7, BEAM_Y + 5], [7, BEAM_Y + 5]].map(([x, y]) => at([x, y, BEAM_TOP + 10])), { size: 0.45 }),
    S(k.slabOf(arm, BEAM_TOP + 3, 4, P, 2, 0.4), { tone: "mid" }),
    S(k.cylinder(0, 0, 4.6, HEAD_BOTTOM, BEAM_TOP + 7 - HEAD_BOTTOM, P, 28), { tone: "mid" }),
    L(k.sideArc(0, 0, 4.6, HEAD_BOTTOM + 3, P, 16), { tone: "faint" }),
    S(k.cylinder(0, 0, 2.2, BEAM_TOP + 7, 2.2, P, 20), { tone: "mid" }),
    L(k.knurl(0, 0, 2.2, BEAM_TOP + 7, BEAM_TOP + 9.2, 14, P), { tone: "lo" }),
  ].join("");
}

base();
dial();
post(POSTS[0]);
post(POSTS[1]);
beam();
trays();

A.settle(R, P);
R.items.sort((a, b) => a.key - b.key);
const art = `<path class="iso-halo" d="${k.haloOf(PLATE, -PLATE_H - FOOT_H, PLATE_H, P)}"/>` + R.items.map((it) => it.svg).join("");
A.auditOrExit(R, P);

// Live page numbers: every one comes from the model or the geometry above.
const LIVE_CONST = { P, M, SETS, STATES, TX: [...Array(M).keys()].map(TX), HOME, CARRY, HEAD_BOTTOM, GRIP_H, TILE, FLOOR_TOP, WALL_TOP, DIAL, DIAL_R, DIAL_TOP, READOUTS: STATES.map(readoutAt) };

const live = `
const C = ${JSON.stringify(LIVE_CONST)};
const P = C.P;
const stage = document.querySelector(".iso-stage");
const svg = stage.querySelector("svg");
const readout = document.querySelector("[data-readout]");
const top = svg.querySelector('[data-part="top"]');
const shuttleEl = svg.querySelector('[data-part="shuttle"]');
const flight = svg.querySelector('[data-part="flight"]');
const lift = flight.querySelector('[data-part="lift"]');
const rodEl = flight.querySelector('[data-part="rod"]');
const heldTile = flight.querySelector('[data-part="tile"]');
const needle = svg.querySelector('[data-part="needle"]');
const still = matchMedia("(prefers-reduced-motion: reduce)");
const tiles = (i, n) => svg.querySelector('[data-tile="' + i + '-' + n + '"]');
const slotOf = (key) => key % C.M;
const tileZ = (n) => C.FLOOR_TOP + n * (C.TILE.h + C.TILE.gap);
const ease = (t) => t <= 0 ? 0 : t >= 1 ? 1 : t * t * (3 - 2 * t);
const span = (p, a, b) => ease((p - a) / (b - a));
const STEP = 3.0;                 // seconds per insert when stepping one at a time
const HOLD = [1.4, 0.4, 0.4, 0.4, 0.6, 2.8, 1.0, 0.4, 0.4, 0.4, 0.4, 3.2]; // pause after reaching each state

let shown = 0, target = 0, phase = -1, speed = 1, needleAt = 0, needleFrom = 0, x = C.HOME;
let touring = !still.matches, hold = HOLD[0], visible = false, frame = 0, last = 0, idleTimer = 0;

function chainsAt(s) { const c = Array.from({ length: C.M }, () => []); C.SETS[s.set].slice(0, s.n).forEach((key) => c[slotOf(key)].push(key)); return c; }
function showTable(s) {
  const c = chainsAt(s);
  for (let i = 0; i < C.M; i++) for (let n = 0; n < 5; n++) tiles(i, n).style.display = n < c[i].length ? "" : "none";
}
let rodLen = -1;
function setLift(z) {
  // z is the bottom of the carried tile; the drop rod runs from the head down to the gripper
  lift.setAttribute("transform", translateAlong(P, [0, 0, z - C.CARRY]));
  const len = Math.round((C.HEAD_BOTTOM - (z + C.TILE.h + C.GRIP_H)) * 4) / 4;
  if (len !== rodLen) { rodLen = len; rodEl.innerHTML = solidSvg(cylinder(0, 0, 1.1, C.HEAD_BOTTOM - len, len, P, 16), { tone: "mid", crease: "none" }); }
}
function parentTo(el) { if (flight.parentNode !== el) el.appendChild(flight); }
function needleTo(slot) {
  const a = slot / C.M * Math.PI * 2, [x, y] = C.DIAL, r = C.DIAL_R - 4;
  needle.setAttribute("d", lineOnTop([x - Math.sin(a) * 3.4, y + Math.cos(a) * 3.4], [x + Math.sin(a) * r, y - Math.cos(a) * r], C.DIAL_TOP + 0.2, P));
}
function say(text) { if (readout.textContent !== text) readout.textContent = text; }
function describe() {
  stage.setAttribute("aria-valuenow", String(shown));
  stage.setAttribute("aria-valuetext", C.READOUTS[shown]);
}

// One insert, phase 0..1: dial turns 0–.18 · shuttle runs .18–.52 · tile drops .52–.70 · released .72 · grip rises .72–.84 · returns .84–1
function draw() {
  let carrying = false, z = C.CARRY;
  if (phase >= 0) {
    const s = C.STATES[shown + 1], key = C.SETS[s.set][s.n - 1], slot = slotOf(key);
    const below = chainsAt(C.STATES[shown])[slot].length;
    const bottom = tileZ(below);
    needleAt = needleFrom + (slot - needleFrom) * span(phase, 0, 0.18);
    x = C.HOME + (C.TX[slot] - C.HOME) * span(phase, 0.18, 0.52) + (C.HOME - C.TX[slot]) * span(phase, 0.84, 1);
    carrying = phase < 0.72;
    z = carrying ? C.CARRY + (bottom - C.CARRY) * span(phase, 0.52, 0.70) : bottom + (C.CARRY - bottom) * span(phase, 0.72, 0.84);
    // while the tile is inside the tray it is drawn in the tray's slot, between the far and near walls
    const low = z < C.WALL_TOP + 2 && phase > 0.5 && phase < 0.86;
    parentTo(low ? svg.querySelector('[data-slot="' + slot + '"]') : top);
    tiles(slot, below).style.display = carrying ? "none" : "";
    say(phase < 0.18 ? "key " + key + " · hashing" : carrying ? "key " + key + " → slot " + slot : C.READOUTS[shown + 1]);
  } else {
    parentTo(top);
    say(C.READOUTS[shown]);
  }
  heldTile.style.display = carrying ? "" : "none";
  needleTo(needleAt);
  shuttleEl.setAttribute("transform", translateAlong(P, [x, 0, 0]));
  flight.setAttribute("transform", translateAlong(P, [x, 0, 0]));
  setLift(z);
}

// Start the next step toward target. Going back, or into an empty set, is a jump (the table is cleared).
function begin() {
  while (target !== shown && (target < shown || C.STATES[shown + 1].n === 0)) {
    shown = target < shown ? target : shown + 1;
    x = C.HOME; showTable(C.STATES[shown]); describe();
  }
  if (target === shown) { phase = -1; return; }
  phase = 0; needleFrom = needleAt;
  speed = Math.min(4, Math.max(1, target - shown));
}
function finish() { shown += 1; phase = -1; showTable(C.STATES[shown]); describe(); }

function tick(now) {
  const dt = last ? Math.min((now - last) / 1000, 1 / 30) : 1 / 60;
  last = now;
  if (phase < 0 && touring) {
    hold -= dt;
    if (hold <= 0) { target = (shown + 1) % C.STATES.length; hold = HOLD[target]; }
  }
  if (phase < 0) begin();
  if (phase >= 0) {
    phase = still.matches ? 1 : phase + dt * speed / STEP;
    if (phase >= 1) { finish(); x = C.HOME; begin(); }
  }
  draw();
  const settled = !touring && phase < 0 && shown === target;
  frame = visible && !settled ? requestAnimationFrame(tick) : 0;
}
const run = () => { if (!frame && visible) { last = 0; frame = requestAnimationFrame(tick); } };
const steer = (next) => {
  touring = false;
  target = Math.max(0, Math.min(C.STATES.length - 1, next));
  clearTimeout(idleTimer);
  idleTimer = setTimeout(() => { touring = !still.matches; hold = HOLD[shown]; run(); }, 3600);
  run();
};
new IntersectionObserver((entries) => { visible = entries[entries.length - 1].isIntersecting; if (visible) run(); }, { rootMargin: "120px 0px" }).observe(stage);
stage.addEventListener("pointermove", (event) => {
  const box = svg.getBoundingClientRect();
  const share = Math.min(1, Math.max(0, ((event.clientX - box.left) / box.width - 0.1) / 0.8));
  const want = Math.round(share * (C.STATES.length - 1));
  if (want !== target) steer(want);
});
stage.addEventListener("keydown", (event) => {
  let to = null;
  if (event.key === "ArrowRight" || event.key === "ArrowUp") to = target + 1;
  if (event.key === "ArrowLeft" || event.key === "ArrowDown") to = target - 1;
  if (event.key === "Home") to = 0;
  if (event.key === "End") to = C.STATES.length - 1;
  if (to === null) return;
  event.preventDefault();
  steer(to);
});
if (still.matches) touring = false;
showTable(C.STATES[0]); describe(); draw();
`;

const held = (() => {
  const plan = { x: -TILE.w / 2, y: -TILE.d / 2, w: TILE.w, d: TILE.d, r: 1.2 };
  const grip = { x: -6, y: -7, w: 12, d: 14, r: 1.5 };
  return `<g data-part="lift"><g data-part="tile">${S(k.slabOf(plan, CARRY, TILE.h, P, 3, 0.4), { tone: "hi", lit: true })}</g>` +
    S(k.slabOf(grip, CARRY + TILE.h, GRIP_H, P, 2, 0.3), { tone: "mid" }) +
    D([at([-4, 0, CARRY + TILE.h + GRIP_H]), at([4, 0, CARRY + TILE.h + GRIP_H])], { size: 0.4 }) + `</g>`;
})();

function build(theme) {
  const figure = k.figureSvg({
    width: WIDTH,
    height: HEIGHT,
    label: "A gantry tray sorter on a bench. A hash dial with eight stops shows each key mod 8; a shuttle on an overhead beam carries the key as a tile straight to that tray and drops it. Keys 10, 22, 31, 4 and 15 land in trays 2, 6, 7, 4 and 7, so tray 7 holds a stack of two. Keys 8, 16, 24, 32 and 40 all land in tray 0 and stack five high.",
    body: [
      art,
      `<g data-part="top"><g data-part="flight" transform="${k.translateAlong(P, [HOME, 0, 0])}"><g data-part="rod"></g>${held}</g></g>`,
      `<g data-part="shuttle" transform="${k.translateAlong(P, [HOME, 0, 0])}">${shuttle()}</g>`,
    ],
  });
  const plate = k.plateHtml({
    fig: "Fig 1",
    title: "Hash sorter",
    hint: "Hover or ← → to insert",
    readout: readoutAt(STATES[0]),
    keys: [
      { mark: "lit", label: "The key being inserted" },
      { mark: "raised", label: "Keys already stored; a stack is one chain" },
    ],
    caption: "The dial computes k mod 8 and the shuttle drops each key straight into that tray. Keys 10, 22, 31, 4, 15 leave a longest chain of 2; keys 8, 16, 24, 32, 40 all land in tray 0 and build a chain of 5 at the same load, 5/8.",
    body: `<div class="iso-stage" tabindex="0" role="slider" aria-label="Hash sorter: arrow keys insert the next key or step back; Home empties the table, End inserts both key sets" aria-valuemin="0" aria-valuemax="${STATES.length - 1}" aria-valuenow="0">${figure}</div>`,
  });
  const name = theme === "light" ? `${ID}-light.html` : `${ID}.html`;
  writeFileSync(join(HERE, name), k.pageHtml({ title: "Hash sorter", theme, body: plate, script: kitScript() + live }));
  console.log("wrote", name);
}

build("dark");
build("light");
