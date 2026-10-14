<h1 align="center">Course Studio</h1>

<p align="center">
  An agent skill that plans and writes technical courses — syllabi, chapters, notes and cheat sheets —<br>
  with every diagram built as an interactive isometric figure by <a href="https://github.com/wheresryan22/anatomy">Anatomy</a>.
</p>

<p align="center">
  <a href="https://github.com/akshaypjoshi/course-studio/actions/workflows/ci.yml"><img src="https://github.com/akshaypjoshi/course-studio/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT license"></a>
  <a href="#install"><img src="https://img.shields.io/badge/install-npx_skills_add-1b1b19" alt="Install with npx"></a>
  <a href="#install"><img src="https://img.shields.io/badge/Claude_Code-plugin-D97757" alt="Claude Code plugin"></a>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/figure-dark.png">
    <img src=".github/assets/figure-light.png" width="720" alt="An isometric hash sorter: a dial computes k mod 8 and a shuttle on an overhead rail drops each key into one of eight trays. The card reads Fig 1, Hash sorter, key 15 → slot 7.">
  </picture>
</p>

Ask for *"the binary search chapter"* or *"notes on consistent hashing"* and you get a dense, verified chapter in Markdown, a signature figure whose working **is** the chapter's insight (a probe that halves a rack of gauge blocks, a turntable where a new peg captures one arc of keys), and a built page that has been checked in a headless browser on desktop, phone and dark mode.

## What it does

| You ask for | You get |
|---|---|
| a course, syllabus, curriculum | `course.json` (outcomes, prerequisites, chapters in dependency order, one planned figure each) + a course page and catalog |
| a chapter or lesson on X | `chapter.md` following a fixed teaching arc + its Anatomy figure + a built page |
| notes, an explainer, interview prep | `notes.md`, reusing a chapter figure where one fits |
| a cheat sheet / revision notes | `cheatsheet.md` — tables, patterns, one-liners, no new figures |
| a figure for an existing chapter | a brief, the Anatomy figure, and the rebuilt chapter |

What makes the output trustworthy:

- **Every code block is run**, every number verified, and the figure is driven by the same `model.mjs` as the chapter's worked example — so text, readout and caption agree.
- **Pages are checked**, not just generated: `check_pages.py` flags JS errors, clipped or unbuilt figures, broken links, sideways scroll and empty sections, and saves screenshots for review.
- **An object atlas** gives starting machines for ~90 concepts across DSA, System Design, JavaScript and Low-Level Design, plus a method for inventing one for anything else.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/chapter-dark.png">
    <img src=".github/assets/chapter-light.png" width="720" alt="The built Hashing chapter page: a peach hero card with the title, outcomes and a numbered table of contents.">
  </picture>
</p>

## Install

Course Studio needs the **Anatomy** skill for figures. Install both.

### With the skills CLI (`npx`)

```bash
npx skills add wheresryan22/anatomy -g -a claude-code
npx skills add akshaypjoshi/course-studio -g -a claude-code
```

Drop `-g` to install into the current project instead of globally, or swap `-a claude-code` for another agent the [skills CLI](https://github.com/vercel-labs/skills) supports.

### As a Claude Code plugin (`/plugin`)

Inside Claude Code:

```
/plugin marketplace add akshaypjoshi/course-studio
/plugin install course-studio@course-studio
```

Then install Anatomy (it ships as a skill, not a plugin): `npx skills add wheresryan22/anatomy -g -a claude-code`.

### Requirements

| | Needed for |
|---|---|
| Python 3.9+ with `markdown`, `pyyaml`, `pygments` | building pages |
| `playwright` + Chromium | `check_pages.py` |
| Node.js 20.10+ | building Anatomy figures |

```bash
pip install -r ~/.claude/skills/course-studio/requirements.txt   # path depends on how you installed
python3 -m playwright install chromium
```

Without Node or Chromium the skill still plans and writes; figures stay as dashed "pending" boxes showing their brief, and it tells you the command to build them later.

## Use it

Just ask, in any project:

```
Plan a System Design course, about 30 hours, for engineers preparing for senior interviews.
Write chapter 4 of the DSA course — binary search.
Notes on the JavaScript event loop, with a figure.
Cheat sheet for graph algorithms.
```

Work lands in `./courses/`:

```
courses/
  _anatomy/                     vendored Anatomy kit (pinned per workspace)
  catalog.html                  every course
  dsa/
    course.json                 card, outcomes, syllabus, planned figures
    chapters/05-hashing/
      chapter.md                source of truth (GFM/MDX-friendly)
      figures/fig-01-hash-sorter/{brief.md, model.mjs, build.mjs, *.html}
    dist/                       built pages: index.html, 05-hashing.html …
```

Built pages are self-contained HTML (figures embedded) apart from web fonts — open them, publish them, or feed `chapter.md` to your own platform: callouts use GitHub's `> [!NOTE]` syntax and figures are a single `::figure <id>` line a remark plugin can map to a component.

### Presets

The slugs `dsa`, `system-design`, `javascript-deeply` and `low-level-design` get a built-in colour identity and starting syllabus. Any other subject works the same way with a neutral palette, or set `accent`/`tint` (and dark variants) in `course.json`.

## The scripts

All in `skills/course-studio/scripts/`; the skill runs them for you.

| Script | Does |
|---|---|
| `workspace.py init <courses>` | vendors Anatomy's kit into `<courses>/_anatomy/` |
| `workspace.py course \| chapter \| figure …` | scaffolds `course.json`, `chapter.md` + briefs, a figure folder |
| `build_chapter.py <chapter.md>` | chapter / notes / cheat-sheet page with embedded figures |
| `build_course.py <course-dir>` / `<courses> --catalog` | course page with syllabus / catalog grid |
| `check_pages.py <dist> [--mobile] [--dark]` | headless checks + screenshots; exits 1 on any problem |

## Development

```bash
pip install -r skills/course-studio/requirements.txt && python3 -m playwright install chromium
tests/smoke.sh [path-to-anatomy]     # rebuilds the example course and checks every page
```

CI runs the same smoke test on every push. `evals/` holds trigger evals (prompts that should and shouldn't load the skill) and task evals with expectations, in the format used by Anthropic's `skill-creator`.

Repository layout: `skills/course-studio/` is the skill itself (what `npx skills add` installs); `.claude-plugin/` makes the repo a Claude Code plugin marketplace.

## Credits

Figures are drawn with [Anatomy](https://github.com/wheresryan22/anatomy) by wheresryan22 (MIT).

## License

[MIT](LICENSE)
