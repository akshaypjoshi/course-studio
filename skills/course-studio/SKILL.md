---
name: course-studio
description: Plan and write technical courses, chapters, lessons, notes and cheat sheets — with every diagram built as an interactive isometric figure by the Anatomy skill — and build them into styled, self-checking HTML pages. Ships presets for Data Structures & Algorithms, System Design, JavaScript and Low-Level Design, and works for any technical subject. Use whenever the user asks to create or outline a course, a syllabus or curriculum, a chapter or lesson, notes, revision notes, a cheat sheet, interview-prep material, or "explain X visually for the course", even if they only name a topic like "binary search chapter" or "notes on consistent hashing".
license: MIT
compatibility: Bundles the Anatomy figure engine (MIT). Needs Python 3.9+ with markdown, pyyaml, pygments (playwright + Chromium for checks), and Node.js 20.10+ for figures.
---

# Course Studio

Course Studio writes the teaching; **Anatomy draws the figures** — its engine is bundled in `anatomy/` (kit, scripts, references, examples; guide in `anatomy/ANATOMY.md`), so nothing else needs installing. A course here is a `course.json` (the card, outcomes and syllabus), chapters written in Markdown, and for each chapter one signature Anatomy figure — a detailed isometric machine whose working *is* the chapter's insight (a gauge rack whose probe halves the span, a turntable where a new peg captures one arc of keys). The build scripts turn it into course-catalog pages: warm paper, heavy grotesk titles, mono metadata, one accent per course, light and dark.

## Setup (once per machine)

- **Anatomy** is bundled in `anatomy/`; `workspace.py init` copies it into each workspace. Figures need Node.js 20.10+ (and Chrome/Chromium for checks); without them, plan and write anyway — figures stay as pending boxes with complete briefs (figures.md §7).
- **Python packages**: `pip install -r requirements.txt` from this skill's folder (markdown, pyyaml, pygments; playwright for checks, then `playwright install chromium`). The scripts print the exact missing package if one is absent.

## Files

- `scripts/workspace.py` — `init` (vendor Anatomy's kit into the workspace), `course`, `chapter`, `figure` scaffolds.
- `scripts/build_chapter.py <chapter.md>` — chapter/notes page with embedded figures (pending figures show their brief).
- `scripts/build_course.py <course-dir>` — course page with syllabus; `<courses-dir> --catalog` for the course grid.
- `scripts/check_pages.py <dist-dir> [shots] [--mobile] [--dark]` — headless check + screenshots.
- `references/course-design.md` — outcomes → chapters, `course.json`, folder layout, starting syllabi for the four preset courses.
- `references/writing.md` — the chapter arc, per-course must-haves, writing rules, the Markdown conventions, notes and cheat sheets.
- `references/figures.md` — which ideas get a figure, time budget, the brief, building with Anatomy, parallel figures, integration.
- `references/object-atlas.md` — concept → machine starting points for ~90 DSA / SD / JS / LLD concepts, and how to invent one.
- `anatomy/` — the bundled Anatomy engine: `ANATOMY.md` (its workflow), `kit/`, `scripts/` (capture, drive, lines checks), `references/`, `examples/`. Pinned version in `anatomy/VERSION`.
- `assets/templates/` — `course.json`, `brief.md`, `build.mjs` (figure stub wired to the vendored kit).
- `examples/courses/dsa/` — a finished, verified chapter (Ch 5 Hashing) in the real layout: `course.json`, `chapter.md`, and its Anatomy figure's `brief.md`, `model.mjs` and `build.mjs`. Read it before writing your first chapter to calibrate depth, tone and how text and figure point at each other. To rebuild it, copy `examples/courses/` into a workspace and run `workspace.py init` on it.

## Decide the scope first

| The user asks for | You produce | Read |
|---|---|---|
| a course, syllabus, curriculum, "plan the X course" | `course.json` + course page (+ catalog) with a figure planned per chapter; offer to write chapter 1 | course-design.md |
| a chapter / lesson / module on X | `chapter.md` + its signature figure(s) + built page | writing.md, figures.md, object-atlas.md |
| notes, an explainer, interview prep on X | `notes.md` (kind `notes`), reusing an existing figure where one fits | writing.md §6 |
| a cheat sheet / revision notes | `cheatsheet.md` (kind `cheatsheet`), no new figures | writing.md §6 |
| a figure for an existing chapter | brief + Anatomy figure + rebuilt chapter | figures.md |

If the request names a course that already has a `course.json`, read it first: the chapter must fit its sequence, vocabulary (`glossary`), languages and visual family. Look for the workspace (a folder with `courses/` or `course.json`) in the user's project before creating a new one; default location is `./courses/`.

Say the scope in one line before starting — e.g. "Writing Ch 4 with one Anatomy figure (Figure size)." Follow Anatomy's sizing rule on time: don't quote a time for Figure-size work; give Anatomy's estimate only for a Hero, and never start an Epic unasked. Figures are real work, so a whole course is planned at once but written chapter by chapter unless the user asks for a batch.

## Workflow for a chapter (the main path)

1. **Context.** Read `course.json` (or create it from `assets/templates/course.json` via `workspace.py course`). Run `workspace.py init <courses>` once per workspace so figures can import the kit. Then `workspace.py chapter <course-dir> <n>` scaffolds `chapter.md` and a brief per planned figure.
2. **Outline.** Write the section list with one outcome sentence each (writing.md §2) and the course's must-haves (§3). Identify the single insight that most needs to be *seen moving* — that's the signature figure (figures.md §1). Pick its object from the atlas or invent one with the atlas's method.
3. **Brief the figure early.** Write the paragraph that surrounds `::figure`, then fill `figures/<id>/brief.md` from it — insight, truth model with the chapter's exact example numbers, object and mapping, interaction and tour beats, card text (figures.md §3).
4. **Build the figure with Anatomy.** Put the truth model in `figures/<id>/model.mjs` so the figure and the chapter's numbers share one source. Read `anatomy/ANATOMY.md` (in this skill's folder) and follow its workflow in `figures/<id>/` with the brief as the spec, keeping the output contract (`<id>.html` + `<id>-light.html` from one `node build.mjs`). With the Agent tool available, hand each figure to a subagent as soon as its brief exists and write the chapter meanwhile (figures.md §5); without it, build the figure first, then write.
5. **Write the chapter** in `chapter.md` following the arc and rules. Run every code block in a scratch file; verify every number and real-world claim.
6. **Build and check.** `build_chapter.py chapter.md` → `check_pages.py` on `dist/` (default, and `--mobile --dark`). Read the screenshots: the page, then each figure in context. Fix until the only PROBLEM lines are figures you've deliberately left pending.
7. **Reconcile text and figure.** The text must name moments the figure shows, with the same numbers and words. Update `course.json` (`status`, final figure ids/objects), rebuild the course page.
8. **Deliver** (below).

## Workflow for a course plan

Follow course-design.md: outcomes → prerequisites → chapters in dependency order, sized to the card's hours → per chapter: summary, outcomes, topics, one planned figure (concept + object) → `course.json` → `build_course.py` (+ `--catalog`) → check → show the syllabus and offer the first chapter. Never invent prices; keep `null` unless given.

## Delivering

- In the user's project: write into their `courses/` tree; they get `dist/*.html` to open, and `chapter.md` + figure folders as the source of truth for their platform.
- In claude.ai: publish the built chapter or course page as an artifact (it's self-contained: figures are embedded), and send the `courses/<slug>` folder as a zip when they'll import it into their platform.
- For the user's own Next.js platform: `chapter.md` is GFM/MDX-friendly (`> [!PITFALL]` callouts, a one-line `::figure <id>` directive), and Anatomy figures can also be built through Anatomy's React path (its `references/react.md`) if they'd rather render figures natively than embed the HTML.

End with one line on what was made, what's pending (e.g. a figure still building), and the natural next chapter.

## Quality bar

- The chapter teaches one insight so well that the self-checks are easy *after* reading and hard before.
- The figure is an Anatomy figure that passes Anatomy's own verification — not a diagram of boxes. It shows exactly the moments the text refers to, with the same numbers.
- Nothing is padded; every code block has been run; every number is true.
- Pages pass `check_pages.py` on desktop, phone and dark.
