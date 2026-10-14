# Figure brief: fig-01-hash-sorter

<!-- First non-heading line is shown in the chapter while the figure is pending. Keep it one sentence. -->
A hash dial turns each key into a tray number and a shuttle drops it straight there; keys that collide stack in the same tray, and a bad key set stacks them all in one.

- **Course / chapter / position:** DSA · Ch 5 · Fig 1 of the chapter
- **Size:** Figure (one mechanism, 40–80 parts, ≤ 1 hour)
- **Reader:** knows arrays give O(1) access by index; has just read that `h(k) = k mod m` turns a key into an index, and that two keys can share an index.

## The idea it must make obvious
A hash map is fast because the key is turned straight into a slot number (no walking past other slots); it stays fast only while each slot holds a short chain, and keys that all hash to one slot turn it back into a list.

## Truth (the model)
- inputs: two key sets, inserted one key at a time into an empty table.
  - set A (typical): 10, 22, 31, 4, 15
  - set B (adversarial): 8, 16, 24, 32, 40
- state: m = 8 trays (slots 0–7); chains as lists; n keys stored.
- rule: `slot = k % 8`; a new key is appended to the chain in its slot (separate chaining); chain length = keys compared when looking up the newest key in that slot; load α = n / m.
- concrete values:
  - A: 10→2, 22→6, 31→7, 4→4, 15→7 (collides with 31; chain at slot 7 = 2). Longest chain 2, α = 5/8.
  - B: 8, 16, 24, 32, 40 → all slot 0; chain grows 1…5. α = 5/8 again, longest chain 5.

## The object
A gantry tray sorter on a bench: a base plate carrying a row of eight trays over a slot ruler (0–7), an overhead rail on two end posts with a shuttle that carries one key tile on a drop rod, and a face-up hash dial (8 stops) at the left whose needle points at the slot number.

- **What moves, and what that motion means:** the dial needle swings to `k % 8` and the shuttle runs straight to that tray and drops the tile = computing the index and jumping to it; tiles stack in a tray = the chain grows.
- **Mapping:**
  - key → the tile carried by the shuttle (one tile per key)
  - hash function `k % 8` → the hash dial with 8 stops; needle on the slot
  - bucket array of size 8 → the eight trays on the ruler 0–7
  - chain in a bucket → the stack of tiles in one tray; stack height = chain length = comparisons to find the newest key
  - "jump straight to the slot" → the shuttle passes over the other trays without stopping
  - load factor → readout `α n/8`
- **The one lit part:** the tile being inserted.

## Interaction
- **Pointer:** hover across the card scrubs through the 12 states (A empty → A 5 keys → B empty → B 5 keys).
- **Keyboard:** → next insert, ← back, Home = empty, End = all of set B.
- **Idle tour:** (1) insert 10, 22, 31, 4 into separate trays; (2) 15 lands on 31 in tray 7: first collision, stack of 2; (3) table clears and set B starts; (4) 8, 16, 24, 32, 40 all go to tray 0 and the stack grows to five while seven trays stay empty.
- **Readout:** `key 15 → slot 7 · chain 2 · α 5/8`; empty table: `empty · α 0/8`.

## Card text
- **Fig:** Fig 1
- **Title:** Hash sorter
- **Hint:** Hover or ← → to insert
- **Legend keys:** `lit` the key being inserted · `raised` keys already stored (a stack is one chain)
- **Caption:** The dial computes k mod 8 and the shuttle drops each key straight into that tray. Keys 10, 22, 31, 4, 15 leave a longest chain of 2; keys 8, 16, 24, 32, 40 all land in tray 0 and build a chain of 5 at the same load, 5/8.

## How the chapter uses it
Before: "Watch the shuttle: it never stops at the trays it passes. Watch 15 land on top of 31 in tray 7, then stay for the second key set." After: "With the first set the longest chain was 2. With the second, the same load of 5/8 produced a chain of 5: every key is a multiple of 8, so k mod 8 is 0 for all of them."

## Done when
- `node build.mjs` writes `fig-01-hash-sorter.html` and `fig-01-hash-sorter-light.html`; `--audit` passes if it has pipes, cables or round parts.
- Anatomy's verify steps pass (desktop, 390 px phone, both themes, 4× close-ups).
- A learner who only plays with the figure can state "The idea it must make obvious".
