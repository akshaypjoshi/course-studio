# Writing chapters and notes

Contents: 1. Kinds of output · 2. The chapter arc · 3. Per-course must-haves · 4. Writing rules · 5. Markdown conventions · 6. Notes and cheat sheets · 7. Self-review before building

---

## 1. Kinds of output

| Ask | `kind` | Length | Figures | Shape |
|---|---|---|---|---|
| "chapter on X", "lesson", "module" | `chapter` | 2,000–4,500 words, 25–45 min | 1 signature figure (2–3 for long chapters, on request) | full arc below |
| "notes on X", "explain X" | `notes` | 800–1,800 words | 0–1, prefer reusing a chapter figure | idea → mechanism → pitfalls → check |
| "cheat sheet", "revision notes", "quick reference" | `cheatsheet` | 1–2 screens | none new; link chapter figures | tables, patterns, complexity, one-liners |
| "interview prep for X" | `notes` | 1,000–2,000 words | 0–1 | patterns → canonical problems → what interviewers probe |

## 2. The chapter arc

Outline before writing. For every section write one sentence: *what the learner can do after it*. If two sections have the same sentence, merge them.

1. **Hook / the one idea**: the insight in one or two sentences, before any definition. A concrete situation where it matters.
2. **Watch it work**: the signature figure, placed where the idea first needs to be *seen*. The prose before it says what to watch; the prose after it names what they just saw.
3. **Why it works**: the invariant, proof sketch, or the rule from the spec. This is what separates the course from tutorials.
4. **Build it**: code (DSA, JS, LLD) or the design (SD), with the decisions explained line by line where they're non-obvious.
5. **Variants**: the 2–3 shapes the idea takes in practice and interviews.
6. **Cost & trade-offs**: complexity table (DSA), numbers and trade-offs (SD), performance/semantics (JS), extension cost (LLD).
7. **Pitfalls**: specific bugs, each with the line, the input that breaks it and the symptom.
8. **Check yourself**: 3–4 transfer questions with answers.
9. **Recap**: 3–5 bullets a learner could revise from.

The figure's idle tour, readout and caption must show exactly the moments the text refers to. Write the paragraph around `::figure` first, then the brief from it.

## 3. Per-course must-haves

**DSA**: invariant in one sentence · complexity table (best/avg/worst, space) · code in the course languages (default: Python first, then the others in tabs or a short "in C++ / Java / Go" block for the lines that differ) · edge cases (empty, one element, duplicates, overflow) · an "In the interview" callout naming the problem patterns this unlocks (with 3–5 classic problem names).

**System Design**: functional + non-functional requirements · back-of-envelope numbers shown as arithmetic · the architecture explained component by component · a `[!TRADEOFF]` for every design decision · failure modes and what degrades · "what I'd say in the interview" callout · real-world systems that do this (with what they actually do, verified).

**JavaScript, Deeply**: "predict the output" `[!CHECK]` *before* the explanation · the spec-level rule in plain words (cite the ECMAScript concept name, e.g. "Job Queue", "Environment Record") · how engines actually behave where it differs from the mental model · a pitfall with the real-code bug it causes.

**Low-Level Design**: requirements and assumptions · entities and responsibilities table · class relationships · the core methods in code · the pattern(s) used and why · "extending it" section: a new requirement and what changes · concurrency notes where it matters.

**Any other subject**: same arc; replace the must-haves with that field's equivalents (the core rule, the worked example, the common mistake, the transfer question).

## 4. Writing rules

- **Lead with the idea, not the definition.** "If the data is sorted, one comparison tells you which half to throw away" beats "Binary search is an algorithm that…".
- **Concrete before abstract.** Trace real numbers, then generalise. Every formula gets one worked number.
- **Explain why each step exists.** "lo = mid + 1 because a[mid] is already too small", not "update lo".
- **Name pitfalls precisely**: the line, the input, the symptom.
- **Density over padding.** No "In this chapter we will…", "Let's dive in", restated headings, or motivational filler. The audience is busy engineers and serious students; respect their time.
- **No em dashes (Unicode U+2014) anywhere in generated content**: chapters, notes, cheat sheets, `course.json` text, figure briefs and card text (title, hint, readout, keys, caption). Use a comma, a colon, parentheses or a new sentence instead. Don't fake one with ` - ` or `--` either. En dashes in number ranges (`25–45 min`) are fine. `build_chapter.py` warns with line numbers and `check_pages.py` reports any that reach a page.
- **One idea per paragraph**, 2–5 sentences. Bold only the phrase a skimmer must not miss, at most one per paragraph.
- **Correctness is non-negotiable.** Run every code block (write it to a scratch file and execute it with a few inputs). Verify complexity claims, numbers and real-world claims; search for anything about current systems or versions.
- **Point at the figure precisely.** "Watch the probe drop between blocks 4 and 7", not "see the diagram".
- **Consistent vocabulary** across the course: pick one term (e.g. "invariant", "search space") and keep it. Record course-wide terms in `course.json` → `"glossary"` when they recur.
- **Callouts are seasoning**: at most one per ~3 paragraphs.
- **Self-checks test transfer**, not recall: a variant, a "what breaks if…", a prediction.

## 5. Markdown conventions (what `build_chapter.py` understands)

```markdown
---
title: Binary Search
dek: Throw away half the problem on every comparison.
chapter: 4                # number, or a label like "Appendix"
kind: chapter             # chapter | notes | cheatsheet
minutes: 35
level: Beginner
glyph: BS                 # 2–3 letters for the hero; defaults to the course code
outcomes:
  - State the invariant and use it to avoid off-by-one bugs
---

## The one idea                       ← every ## is numbered and listed in the contents
Prose…

> [!INTUITION]                        ← also PITFALL, INTERVIEW, KEY, NOTE, TRADEOFF
> Body in Markdown.

> [!PITFALL] Integer overflow         ← text after the tag replaces the label

::figure fig-01-halving | Drag the probe; each drop halves the span.

> [!CHECK] Why `lo <= hi` and not `lo < hi`?
> Answer in Markdown.

> [!RECAP]
> - 3–5 bullets
```

- `::figure <id> | lead-in` must be on its own line. The figure folder is `figures/<id>/` next to `chapter.md`; if it isn't there, the builder looks in the other chapters of the course (so notes can reuse a chapter's figure). The lead-in is optional: the Anatomy card already has a title and caption.
- A figure that isn't built yet renders as a dashed "pending" box showing the first line of its `brief.md`, so the chapter can be reviewed before figures exist.
- Fenced code gets syntax highlighting (light and dark). Tables, footnote-free Markdown, and inline HTML work.
- Add `{.nonum}` after a heading (`## Appendix {.nonum}`) to leave it unnumbered.
- The same `chapter.md` is valid MDX/GFM input for a Next.js platform: callouts follow GitHub's `> [!NOTE]` syntax and `::figure` is a single directive line that a remark plugin can map to a `<Figure id>` component.

## 6. Notes and cheat sheets

- **Notes** follow a compressed arc: idea → mechanism (reuse a figure) → code/design → pitfalls → 2 checks. No hero-length intro.
- **Cheat sheets** are tables and patterns: "when you see X, reach for Y", complexity grid, templates (code skeletons), gotchas list. No prose paragraphs longer than two sentences. Link chapter pages for depth.
- Put notes under the course as `chapters/<nn-slug>/notes.md` (kind notes) or `notes/<slug>.md`; build with the same script.

## 7. Self-review before building

Read the draft as the learner:
1. Can each section's outcome sentence be ticked off?
2. Is there any paragraph you'd skim? Cut or compress it.
3. Does every code block run, and does the output in the text match? Are there zero em dashes?
4. Does the text around each figure name moments the figure actually shows?
5. Are the checks answerable from the chapter but not by copying a sentence?
