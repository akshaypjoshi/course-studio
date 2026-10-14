# Designing a course

Contents: 1. Inputs · 2. From outcomes to chapters · 3. course.json · 4. Starting syllabi for the preset courses · 5. Delivering the plan

---

## 1. Inputs

Read what the user gave and fill the rest with sensible defaults stated in one line. Ask only when a wrong guess wastes the whole plan (e.g. "System Design" for interview prep vs for a team building real systems: the chapter list differs a lot).

| Field | Default when not given |
|---|---|
| Audience | Working engineers and final-year students preparing for product-company interviews |
| Level | As on the course card (presets: DSA Beginner → Advanced; others Intermediate) |
| Hours | As on the card; a chapter ≈ 35–50 min reading + practice |
| Languages | DSA: C++ / Python / JavaScript / Go; JS course: JavaScript; LLD: Java-style pseudocode plus TypeScript |
| Price, status | **Never invent prices.** Keep what the user stated or what's already in `course.json`; otherwise `null`. |

Search before writing when the course depends on the current landscape (interview formats, current tooling, versions of runtimes, real systems' architectures). Course structure itself doesn't need search.

## 2. From outcomes to chapters

1. **Outcomes first**: 5–8 things the learner can *do* at the end ("design a rate limiter and defend its trade-offs"). Every chapter must serve at least one.
2. **Prerequisites**: what you assume; link to the course that teaches it if it's in the same catalog.
3. **Chapters in dependency order**: nothing used before it's taught. Spiral where useful (a chapter can revisit an earlier idea at a deeper level; say so in its summary).
4. **Size each chapter** to one sitting (25–45 min reading). A chapter with two "aha"s is two chapters.
5. **Plan one signature figure per chapter**: the concept it makes obvious and a starting object from `object-atlas.md`. Keep one visual family per course.
6. **Topics**: 3–8 tags per chapter (they show on the syllabus).
7. Check the total against the hours on the card; adjust chapter count, not chapter depth.

## 3. course.json

The single source of truth for the course card, the course page and the chapter scaffolds. Fields map to the platform's course card (`code` → the big letters, `tagline` → card text, `level · hours · languages` → the mono spec line, `status`, `price`).

```json
{
  "slug": "dsa",                     // folder name; known slugs get the course colours automatically:
                                     // dsa, system-design, javascript-deeply, low-level-design
  "code": "DSA",                     // 2–3 letters on the card and hero
  "title": "Data Structures & Algorithms",
  "tagline": "From arrays to DP. Learn it visually, then prove it with practice.",
  "level": "Beginner → Advanced", "hours": 40, "languages": ["C++", "Python", "JavaScript", "Go"],
  "status": "available",             // available | coming_soon
  "price": 3499, "currency": "INR", "order": 1,
  "accent": "#D04A28", "tint": "#F4E1D8", "accentDark": "#F06A45", "tintDark": "#3A2219",   // optional overrides
  "audience": "...", "prerequisites": ["..."], "outcomes": ["..."],
  "glossary": {"invariant": "a statement true before and after every loop iteration"},
  "chapters": [
    { "n": 4, "slug": "binary-search", "title": "Binary Search",
      "summary": "One comparison against a sorted midpoint discards half the candidates.",
      "minutes": 35, "outcomes": ["..."], "topics": ["invariant", "lower bound", "search on answer"],
      "figures": [{ "id": "fig-01-halving", "concept": "each probe halves the span",
                    "object": "rack of sorted gauge blocks with two sliding stops and a drop probe", "size": "Figure" }],
      "status": "planned" }          // planned | drafted | figures-pending | published
  ]
}
```

Folder layout:

```
courses/
  _anatomy/                 vendored Anatomy kit (workspace.py init)
  catalog.html              all courses (build_course.py courses --catalog)
  dsa/
    course.json
    chapters/04-binary-search/
      chapter.md
      figures/fig-01-halving/{brief.md, model.mjs, build.mjs, fig-01-halving.html, fig-01-halving-light.html}
    dist/                   built pages: index.html (course page), 04-binary-search.html, …
```

New course colours: add `accent`/`tint` (and dark variants). Pick a hue distinct from the existing four, with the tint at ~12% of the accent on the paper colour.

## 4. Starting syllabi for the preset courses

The four built-in presets (these slugs get their colours automatically). Starting points matched to the card counts. Adapt to what the user wants; they're not fixed.

**DSA (12 chapters, 40 hrs)**: 1 Complexity & how to think about cost · 2 Arrays, strings & prefix sums · 3 Two pointers & sliding window · 4 Binary search (incl. on the answer) · 5 Hashing · 6 Stacks, queues & monotonic stacks · 7 Linked lists · 8 Recursion & backtracking · 9 Trees & BSTs · 10 Heaps & greedy · 11 Graphs (BFS, DFS, shortest paths, topo sort, union-find) · 12 Dynamic programming.

**System Design (5 chapters, 30 hrs)**: 1 Foundations: requirements, estimation, latency numbers, the interview framework · 2 Scaling reads & writes: load balancing, caching, CDNs, replication, sharding, consistent hashing · 3 Data: SQL vs NoSQL, indexes, B-trees & LSM, consistency, quorums, transactions · 4 Async & reliability: queues, logs, idempotency, rate limiting, circuit breakers, back-pressure · 5 Case studies: URL shortener, feed, chat, rate limiter service, payment flow.

**JavaScript, Deeply (4 chapters, 18 hrs)**: 1 Execution: contexts, hoisting, TDZ, scope chain, closures, `this` · 2 Objects: prototypes, classes, references vs values, property descriptors, hidden classes · 3 Async: event loop, tasks vs microtasks, promises, async/await, generators · 4 Memory & performance: garbage collection, leaks, debounce/throttle, modules & bundling.

**Low-Level Design (3 chapters, 22 hrs)**: 1 Object modelling & SOLID: entities, responsibilities, relationships, dependency inversion · 2 Design patterns that come up in machine-coding rounds: strategy, observer, factory, builder, state, command, decorator, adapter, chain of responsibility, singleton (with when *not* to) · 3 Machine-coding walkthroughs: parking lot, elevator, LRU cache, rate limiter, splitwise, with concurrency.

## 5. Delivering the plan

1. Write `course.json` (and `workspace.py init` if the workspace is new).
2. `python3 scripts/build_course.py courses/<slug>` → the course page with the syllabus and planned figures; `--catalog` for all courses.
3. Show the user the syllabus page and the figure plan, and offer to write chapter 1 (or the chapter they care about most). Don't build every chapter unasked: each chapter with its figure is a real piece of work.
