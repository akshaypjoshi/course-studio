# Figure brief: {{id}}

<!-- First non-heading line is shown in the chapter while the figure is pending. Keep it one sentence. -->
{{concept}}

- **Course / chapter / position:** <course> · Ch <n> · Fig <k> of the chapter
- **Size:** {{size}} (Figure = one mechanism, 40–80 parts; Hero only when asked)
- **Reader:** what they already know when they reach this figure (the paragraph before it)

## The idea it must make obvious
One sentence a learner could say after playing with it. Not the topic — the insight.

## Truth (the model)
The real numbers and behaviour the figure must obey. Every readout, motion and caption number comes from this model.
Write it as `model.mjs` in this folder (a small pure module); `build.mjs` imports it, and the chapter's numbers are produced by running it.
- inputs:
- state:
- rule(s), as code or formula:
- concrete values to show (sizes, counts, thresholds):

## The object
{{object}}

- **What moves, and what that motion means:** one sentence.
- **Mapping:** concept part → physical part, one line each (every concept part must have a physical part, and vice versa).
- **The one lit part** (what the reader watches):

## Interaction
- **Pointer:** what hover/drag does.
- **Keyboard:** arrows / space / home / end.
- **Idle tour:** the loop it plays when nobody touches it (3–5 beats, each a moment the chapter text refers to).
- **Readout:** the live value, with units, e.g. `lo 3 · hi 6 · mid 4`.

## Card text
- **Fig:** Fig <k>
- **Title:** 2–4 words
- **Hint:** e.g. "Drag the carriage ← →"
- **Legend keys:** 1–3 (`lit`, `raised`, `dotted`, …) and what each stands for
- **Caption:** 1–2 true sentences with the real numbers

## How the chapter uses it
The sentences around `::figure {{id}}` that point at it ("watch the fifth pin…"). The figure must show exactly those moments.

## Done when
- `node build.mjs` writes `{{id}}.html` and `{{id}}-light.html`; `--audit` passes if it has pipes, cables or round parts.
- Anatomy's verify steps pass (desktop, 390 px phone, both themes, 4× close-ups).
- A learner who only plays with the figure can state "The idea it must make obvious".
