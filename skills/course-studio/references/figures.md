# Figures: planning them and handing them to Anatomy

Every diagram in a course is an **Anatomy figure**: a detailed isometric machine whose working is the concept, in a framed card with a live readout. They are the course's signature, and each one is real work (Anatomy sizes a single-mechanism Figure at up to an hour). So this skill's job is to choose the few ideas that deserve one, brief them precisely, and fit them into the text.

Contents: 1. Which ideas get a figure · 2. Budget and time · 3. Writing the brief · 4. Building with Anatomy · 5. Parallel figures · 6. Fitting it into the chapter · 7. When Anatomy can't run

---

## 1. Which ideas get a figure

A figure earns its place when the insight is a **mechanism that moves**: something changes over time or under the learner's hand, and watching it change is how the idea clicks. Good candidates are the chapter's "aha":

- why binary search halves (the probe dropping between two stops)
- why a hash map is O(1) and when it isn't (the selector turning straight to a slot; a hook chain growing)
- why microtasks run before the next task (the clerk emptying the priority tray first)
- why adding a server moves only one arc of keys (a peg dropped onto a turntable)

Not figure material: definitions, lists, complexity tables, API surfaces, code walkthroughs, comparisons of options (use a table or `[!TRADEOFF]`), anything static. Don't draw boxes-and-arrows architecture with Anatomy — invent the machine (see `object-atlas.md`) or use prose plus a table.

## 2. Budget and time

| Output | Default figures | Size |
|---|---|---|
| Course plan | 0 built; one planned per chapter in `course.json` | — |
| Chapter | 1 signature figure | Anatomy **Figure** (one mechanism, 40–80 parts) |
| Long chapter (> 40 min) | 2 (ask before a 3rd) | Figure each; build in parallel where possible |
| Notes / cheat sheet | 0 new; reuse chapter figures by id | — |
| A dense object with several moving systems | only on request | Anatomy **Hero** |

Follow Anatomy's sizing rule exactly: name the size before starting; for a Figure don't quote a time (it often finishes well under an hour — keep the progress checks to yourself); for a Hero give its 2–4 hour estimate; never start an Epic without the user choosing it. In practice a chapter with one Figure took about half an hour end to end in testing.

## 3. Writing the brief

Scaffold with `python3 scripts/workspace.py figure <chapter-dir> <fig-id>` (or `chapter`, which does it for every planned figure). Name ids after the **concept**, not the object — `fig-01-hash-lookup`, not `fig-01-pigeonholes` — so changing the object later never means renaming across `course.json`, `chapter.md` and the folder. Fill every section of `figures/<id>/brief.md`:

- **The idea it must make obvious** — the insight sentence, written from the chapter's paragraph around `::figure`.
- **Truth** — the real model. For algorithms, the same algorithm as the chapter's code, with the same example input, so every number on the card matches the text. For systems, real numbers (latencies, rates, counts) you have verified. Write it as `figures/<id>/model.mjs` (a small pure module): `build.mjs` drives the readout and motion from it, and you can run it with `node -e` to produce the exact numbers the chapter quotes.
- **The object** — start from `object-atlas.md`; state what moves and what that motion means, and the one-to-one mapping. If the course already has figures, keep the course's visual family (atlas, "Reuse across a course").
- **Interaction & idle tour** — the beats the tour plays must be the moments the chapter text names ("watch the probe drop at 5, then 6").
- **Card text** — `Fig k` (its position in the chapter), a 2–4 word title, the hint, legend keys, a true caption.

A brief that leaves the object vague produces a vague figure. A brief whose numbers differ from the text produces a figure that contradicts the chapter. Both are the brief's fault.

## 4. Building with Anatomy

1. Make sure the workspace is wired: `python3 scripts/workspace.py init <courses-dir>` copies Anatomy's `kit/` and `scripts/` into `<courses-dir>/_anatomy/` (once; re-run to update). The figure's `build.mjs` stub already imports from there.
2. **Load the Anatomy skill** (invoke it by name, `anatomy`, or read its `SKILL.md`) and follow its workflow from step 1 — size, truth, object, parts list, world, geometry, painter's order, card, live behaviour, verify — with the brief as the spec. Open Anatomy's closest example before starting, as it instructs. Work inside `figures/<id>/`.
3. Keep course-studio's output contract (also written at the top of the stub):
   - `node build.mjs` writes **both** `<id>.html` (dark) and `<id>-light.html` (light) in the figure folder.
   - The card's `fig` is `Fig k`; `title`, `hint`, `readout`, `keys`, `caption` come from the brief.
   - `node build.mjs --audit` passes whenever the figure has pipes, cables or round parts.
4. Run Anatomy's own verification (its `capture.mjs`/`drive.mjs`/`lines.mjs` are in `_anatomy/scripts/`, its references in `_anatomy/references/`): desktop, 390 px phone, both themes, 4× close-ups, line ends at zero. Read every PNG.
   - Theme builds: Anatomy's examples build light with `--light`; course-studio's stub writes both themes in one `node build.mjs`. Point Anatomy's capture commands at `<id>.html` and `<id>-light.html` accordingly.
   - Anatomy's audit only proves what you record with `A.recorder`. Record every solid (moving ones included, at rest and at their extremes where the kit allows); anything you don't record — a shuttle, a stack of tiles — you must check by eye at 4× in its extreme poses.
   - Headless Chrome: set `CHROME_PATH` if Anatomy can't find a browser (e.g. Playwright's Chromium).

## 5. Parallel figures

When a chapter has 2+ figures, or a batch of chapters is requested, and the Agent tool is available: start one subagent per figure **as soon as its brief is written**, and keep writing the chapter text meanwhile. Prompt each with:

```
Build an Anatomy figure.
- Load the `anatomy` skill (or read its SKILL.md at <path>) and follow its workflow fully, including verification.
- Brief: <absolute path>/figures/<id>/brief.md — it is the spec; don't change the idea, numbers or card text without saying why.
- Work in <absolute path>/figures/<id>/. build.mjs is a stub that already imports the vendored kit from <courses>/_anatomy; keep its output contract:
  `node build.mjs` writes <id>.html and <id>-light.html next to it.
- Done when: both pages build, `--audit` passes if it has pipes/cables/round parts, Anatomy's verify steps pass, and you have read the screenshots.
- Reply with: the object you built and its mapping in 3 lines, any deviation from the brief, the paths, and anything unresolved.
```

When a subagent returns, check its deviation notes against the chapter text and fix whichever side is wrong.

## 6. Fitting it into the chapter

1. Rebuild the chapter (`build_chapter.py`) — the pending box becomes the live figure.
2. `check_pages.py` (default and `--mobile --dark`) — no clipped or failed figures, no errors.
3. Open the figure screenshots in the chapter context: does the figure's tour show what the paragraph before it promises? Does the readout use the chapter's vocabulary? Is the caption consistent with the text's numbers?
4. Update the paragraph after the figure to name what the learner just saw.

## 7. When Anatomy can't run

Anatomy needs Node 20.10+ and Chrome/Chromium for its checks. If they're missing, say so, keep the figure as a pending box with its complete brief (the chapter still builds and reads well), and tell the user the exact command to build it on their machine:

```
cd courses/<course>/chapters/<nn-slug>/figures/<id> && claude "/anatomy build this figure from brief.md"
```
