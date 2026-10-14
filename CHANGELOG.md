# Changelog

## 0.5.0 (2026-10-14)

- **Second example: How Rockets Work, Ch 3 "Inside the engine".** A course for curious adults with six planned chapters and one written: how SpaceX's Raptor 2 drives its pumps (full-flow staged combustion), with real numbers dated and sourced in `model.mjs`, back-of-envelope checks, and a Hero figure adapted from Anatomy's Raptor 2 example that you can take apart and fire.
- Fixed: table-of-contents entries for headings with apostrophes showed `&rsquo;`; course pages showed an empty price pill when the price is `null`.
- Website: both chapters as demos (now under `/example/dsa/` and `/example/how-rockets-work/`, with redirects from the old Hashing URLs); the Raptor section now shows the chapter's own figure; the presets section is gone.
- Smoke test checks both example courses.

## 0.4.0 (2026-10-14)

- **Any subject, not just software.** The skill now covers engineering, science, the body, business and more. It adds must-haves for "how things work", natural sciences, business and humanities (writing.md §3), a "draw the real thing" rule for physical subjects, and a new atlas section with rocket engines, staging, orbits, the heart, gears, locks, tides and markets.
- Real-world facts must come from published sources (searched), with approximations marked and years given for anything that changes.
- Audience defaults now follow the subject; code languages apply only to programming courses. Added an example syllabus outside the presets (How Rockets Work).
- Website: a "Not just software" section with Anatomy's Raptor 2 engine running live.
- Evals: four new trigger cases and a rocket-engine chapter task.

- Website at [skills.akshayjoshi.dev/course-studio](https://skills.akshayjoshi.dev/course-studio/): a landing page with the hashing figure running live, and the demo course and chapter built by the skill's own scripts. Source in `site/`; CI builds it on every push.

## 0.3.1 (2026-10-14)

- Documentation follows the house style: no em dashes in the README, CHANGELOG, `SKILL.md`, references, templates or evals. CI now fails if one appears anywhere in the repository.
- README: describes the bundled Anatomy engine, the em dash checks, the `requirements.txt` path for plugin installs, and the repository layout.
- New `CONTRIBUTING.md`: how to test, the style rules, how to update the bundled Anatomy engine, and how to cut a release.

## 0.3.0 (2026-10-14)

- **No em dashes in generated content.** New writing rule covering chapters, notes, cheat sheets, `course.json` text, briefs and figure card text.
- `build_chapter.py` warns with line numbers (ignoring code); `check_pages.py` reports any em dash visible on a page or inside a figure as a PROBLEM.
- Markdown no longer converts `--`/`---` into dashes, and the pipeline itself no longer inserts any.

## 0.2.0 (2026-10-14)

- **Anatomy is bundled.** The figure engine (kit, scripts, references, examples) now ships inside the skill at `skills/course-studio/anatomy/`, pinned to upstream `e6600ff` (v1.1.0+). Installing `akshaypjoshi/course-studio` is all you need.
- Its guide is `anatomy/ANATOMY.md` (renamed from `SKILL.md` so it isn't installed as a second skill). Gallery publishing and the upstream test suite are left out.
- `workspace.py init` uses the bundled copy; `--anatomy <path>` or `ANATOMY_SKILL` still override it.
- `tools/update-anatomy.sh` re-vendors from upstream; `THIRD_PARTY_NOTICES.md` carries the MIT notice.

## 0.1.0 (2026-10-14)

First public release.

- Skill: plan courses, write chapters, notes and cheat sheets with Anatomy figures.
- Scripts: `workspace.py` (init/course/chapter/figure scaffolds), `build_chapter.py`, `build_course.py` (+ catalog), `check_pages.py`.
- Presets for DSA, System Design, JavaScript and Low-Level Design; any other subject works with a fallback palette.
- Worked example: DSA chapter 5 (Hashing) with its hash-sorter figure.
- Install via `npx skills add` or the Claude Code plugin marketplace.
- CI smoke test that rebuilds the example and checks pages on desktop, phone and dark.
