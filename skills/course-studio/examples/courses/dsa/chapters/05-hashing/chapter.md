---
title: Hashing
dek: A hash function turns a key into a slot number, so lookup is one jump, until collisions pile up.
chapter: 5
minutes: 40
level: Beginner → Advanced
glyph: "#"
outcomes:
  - Explain why a hash map lookup is O(1) on average and what the average assumes
  - Implement separate chaining and linear probing, including deletion with tombstones
  - Use the load factor to decide when to resize, and show why doubling is amortised O(1)
  - Recognise the inputs that make a hash map O(n) and what languages do about it
---

## The one idea

An array finds element `i` in one step because `i` *is* the address. A hash map gives any key that power: a **hash function turns the key into an array index**, so looking up `"user:4471"` costs the same as looking up `a[3]`. Everything else in this chapter is about the one thing that can go wrong: two keys asking for the same index.

You already use this every day. Counting word frequencies, de-duplicating IDs, caching results, "have I seen this node before?" in a graph search: each is a hash map turning an O(n) scan into an O(1) jump. Interviewers know it too, and their follow-up is almost always the same: *is it really O(1)? When isn't it?*

## Watch it work

Take a table of `m = 8` slots and the simplest hash function for integers, `h(k) = k mod 8`. Key 10 goes to slot 2, key 22 to slot 6, key 31 to slot 7. Then comes key 15: `15 mod 8 = 7`, the slot 31 already holds. That is a **collision**, and the table has to keep both keys in slot 7.

In the figure, the dial computes `k mod 8` and the shuttle carries each key to its tray. Watch the shuttle: it never stops at the trays it passes; it goes straight to the one the dial names. Watch 15 land on top of 31 in tray 7, then stay for the second key set.

::figure fig-01-hash-sorter

With the first set, 10, 22, 31, 4, 15, the longest stack was 2: finding 15 means jumping to tray 7 and comparing two keys. The second set, 8, 16, 24, 32, 40, has the same number of keys in the same eight trays, a load of 5/8 both times, yet every key landed in tray 0 and built a stack of 5. Each is a multiple of 8, so `k mod 8` is 0 for all of them. **The hash map was exactly as fast as its longest stack.**

## Why it works: the hash function and the average

A hash function has two jobs. It must be **deterministic** (the same key always gives the same index, or you could never find what you stored), and it should **spread keys evenly** over the slots. The first job is a rule you can't break. The second is a hope you can only make likely.

The O(1) claim rests on that hope, stated precisely as *simple uniform hashing*: each key is equally likely to land in any of the `m` slots, independently of the others. Under it, `n` keys in `m` slots give an expected stack length of

> α = n / m, the **load factor**.

With 5 keys in 8 slots, α = 0.625: an average slot holds 0.625 keys, and a lookup for a missing key compares, on average, 0.625 keys after the jump. Keep α below a constant (say 0.75) and the expected cost of every operation is O(1 + α) = O(1). That's the whole proof. Notice what it is *not*: it is not a guarantee for every input. The second key set shows a single bad input pushing one lookup to 5 comparisons, and n bad keys push it to n.

Real hash functions for integers and strings mix every bit of the key into every bit of the result, so that keys which differ slightly (16 and 24, or `"ab"` and `"ba"`) land far apart. Plain `k mod m` doesn't: it only looks at the low bits when `m` is a power of two, which is exactly why the multiples of 8 all collided. Two standard defences:

- **Mix before you reduce.** Python's `dict` perturbs its probe sequence with the high bits of the hash; Java's `HashMap` XORs the high 16 bits of `hashCode()` into the low 16 before masking.
- **Use a prime `m`** when the hash itself is weak. libstdc++'s `std::unordered_map` picks prime bucket counts: `reserve(1000)` gives 1,031 buckets.

> [!INTUITION]
> A hash function is a promise about *typical* keys. The average-case O(1) is a statement about those keys, and an adversary who knows your hash function can choose keys that aren't typical.

## Build it: separate chaining

The figure's trays are **separate chaining**: each slot holds a small list (a chain), and colliding keys share that list. Lookup is "jump, then walk one short chain".

```python
class ChainedMap:
    def __init__(self, m=8):
        self.buckets = [[] for _ in range(m)]
        self.n = 0

    def _bucket(self, key):
        return self.buckets[hash(key) % len(self.buckets)]

    def get(self, key, default=None):
        for k, v in self._bucket(key):          # walk one chain only
            if k == key:
                return v
        return default

    def put(self, key, value):
        b = self._bucket(key)
        for i, (k, _) in enumerate(b):
            if k == key:                        # existing key: overwrite, n unchanged
                b[i] = (key, value)
                return
        b.append((key, value))
        self.n += 1
        if self.n / len(self.buckets) > 0.75:   # load factor check
            self._resize(2 * len(self.buckets))

    def remove(self, key):
        b = self._bucket(key)
        for i, (k, _) in enumerate(b):
            if k == key:
                b.pop(i)
                self.n -= 1
                return True
        return False

    def _resize(self, m):
        old = self.buckets
        self.buckets = [[] for _ in range(m)]
        for chain in old:
            for k, v in chain:                  # every key moves: its slot depends on m
                self.buckets[hash(k) % m].append((k, v))
```

The decisions that matter:

- **`put` searches before appending.** A map stores each key once; without the search, `put(15, "a")` then `put(15, "b")` leaves two entries and `get` returns whichever comes first.
- **`n` changes only on a real insert or removal**, because it drives the load-factor check.
- **`_resize` rehashes every key** rather than copying buckets: a key's slot is `hash(k) % m`, and `m` just changed.

In CPython, `hash(n) == n` for small integers, so inserting the figure's keys reproduces it exactly: chain lengths `[0, 0, 1, 0, 1, 0, 1, 2]` for the first set and `[5, 0, 0, 0, 0, 0, 0, 0]` for the second, both at load 0.625.

Every course language ships a production hash map; use it, and know its one sharp edge:

```cpp
std::unordered_map<int, int> seen;
seen.reserve(1000);                        // size once: no rehash while filling
seen[15] = 225;
if (seen.find(99) == seen.end()) { ... }   // seen[99] would INSERT a 0
```

```javascript
const seen = new Map();                    // not {}: object keys become strings
seen.set(15, 225);
seen.get(99);                              // undefined
```

```go
seen := make(map[int]int, 1000)            // size hint
v, ok := seen[99]                          // 0, false: check ok, not v
```

## Open addressing: no lists at all

**Open addressing** stores keys directly in the array. On a collision you *probe* other slots in a fixed order until you find a free one. The simplest order is **linear probing**: try `h`, then `h+1`, `h+2`, … wrapping around. In a 16-slot table, `31 mod 16 = 15`, and 15 also hashes to 15, so 15 probes on to slot 0.

```python
EMPTY, TOMB = object(), object()

class ProbingMap:
    def __init__(self, m=8):
        self.keys = [EMPTY] * m
        self.vals = [None] * m
        self.n = 0          # live keys
        self.used = 0       # live keys + tombstones (what slows probes down)

    def _probe(self, key):
        m = len(self.keys)
        i = hash(key) % m
        while True:
            yield i
            i = (i + 1) % m                     # linear probing: try the next slot

    def get(self, key, default=None):
        for i in self._probe(key):
            k = self.keys[i]
            if k is EMPTY:                      # a never-used slot ends the search
                return default
            if k is not TOMB and k == key:      # a tombstone does NOT end it
                return self.vals[i]

    def put(self, key, value):
        if (self.used + 1) / len(self.keys) > 0.5:
            grow = self.n + 1 > len(self.keys) // 4
            self._resize(2 * len(self.keys) if grow else len(self.keys))
        first_tomb = None
        for i in self._probe(key):
            k = self.keys[i]
            if k is EMPTY:
                if first_tomb is not None:      # reuse the earliest tombstone on the path
                    i = first_tomb
                else:
                    self.used += 1
                self.keys[i], self.vals[i] = key, value
                self.n += 1
                return
            if k is TOMB:
                if first_tomb is None:
                    first_tomb = i
            elif k == key:
                self.vals[i] = value
                return

    def remove(self, key):
        for i in self._probe(key):
            k = self.keys[i]
            if k is EMPTY:
                return False
            if k is not TOMB and k == key:
                self.keys[i], self.vals[i] = TOMB, None   # keep the probe path intact
                self.n -= 1
                return True

    def _resize(self, m):
        live = [(k, v) for k, v in zip(self.keys, self.vals) if k is not EMPTY and k is not TOMB]
        self.keys, self.vals, self.n, self.used = [EMPTY] * m, [None] * m, 0, 0
        for k, v in live:
            self.put(k, v)
```

The invariant that makes it correct: **if key `k` is in the table, every slot on its probe path from `h(k)` up to `k` is non-empty.** `get` relies on it: it stops at the first EMPTY slot because the invariant says `k` can't be beyond it.

That is why deletion needs a **tombstone**. Delete 31 by writing EMPTY into slot 15, and `get(15)` starts at slot 15, sees EMPTY, and reports 15 missing, although it sits one slot further on. Running both versions confirms it: with the tombstone, `get(15)` returns 15; with the naive delete, it returns `None`.

Tombstones have a cost: they still lengthen probe paths. That is why the code counts `used` (live keys plus tombstones) for the load check, and why a resize that drops tombstones may keep the same size (`grow` is false when most of the used slots are dead).

> [!TRADEOFF] Chaining or open addressing?
> **Chaining** tolerates α near or above 1, deletes simply, and keeps pointers to entries stable across inserts; each entry pays for a node, and walking a list is cache-unfriendly. **Open addressing** keeps everything in one array (fast, cache-friendly, no per-entry allocation) but must stay well below full, needs tombstones, and is sensitive to clustering. CPython's `dict` and Go's `map` (Swiss tables since Go 1.24) use open addressing; Java's `HashMap` and C++'s `std::unordered_map` use chaining.

## Load factor and resizing

Both designs slow down as α grows, but open addressing slows much faster. Under uniform hashing, linear probing needs about ½·(1 + 1/(1 − α)²) probes for an unsuccessful search: **2.5 probes at α = 0.5, 8.5 at α = 0.75, 50.5 at α = 0.9.** Chaining needs about 1 + α: 1.5, 1.75 and 1.9 at those loads. That gap is why open-addressing tables resize earlier: CPython's `dict` grows at two-thirds full, while `std::unordered_map` defaults to `max_load_factor() == 1.0`.

Resizing is O(n): every key is rehashed into the new array. So why is `put` still O(1)? Because the table **doubles**. Starting at `m = 8` with a 0.75 threshold, 1,000 inserts trigger resizes at n = 7, 13, 25, 49, 97, 193, 385 and 769, moving 7 + 13 + … + 769 = **1,538 keys in total, about 1.5 moves per insert**. In general the moves form a geometric series that sums to less than 2n, so the *amortised* cost per insert is O(1), even though one unlucky insert pays O(n).

> [!PITFALL] Growing by a constant
> Grow by `m + 100` instead of `2m` and the series is no longer geometric: n inserts trigger about n/75 resizes of average size n/2, which is O(n²/150) moves in total, so each insert costs O(n) amortised. The constant only hides it until n is large.

When you know the size up front, skip the resizes entirely: `reserve(n)` in C++, `make(map[K]V, n)` in Go. That also removes the latency spike of one giant rehash in the middle of a request.

## When a hash map is NOT O(1)

| Operation | Average | Worst | Why the worst happens |
|---|---|---|---|
| `get` / `contains` | O(1) | O(n) | every key in one chain or one probe cluster |
| `put` | O(1) amortised | O(n) | a resize, or a long chain/cluster |
| `remove` | O(1) | O(n) | same as `get` |
| iterate all | O(n + m) | O(n + m) | must visit empty slots too |
| space | O(n + m) | O(n + m) | m stays within a constant factor of n |

The worst case arrives in four concrete ways:

1. **A weak hash meets patterned keys.** The figure's second set: multiples of 8 under `k mod 8`. Real versions: IDs that are all multiples of 1,024, timestamps rounded to the second, pointers aligned to 16 bytes.
2. **A custom hash that ignores most of the key.** A `__hash__` that returns `len(self.name)` puts every 5-letter name in one bucket.
3. **An adversary chooses the keys.** If attackers know your hash function, they can send thousands of colliding keys (say, as JSON fields or query parameters) and make each insert O(n), so n inserts cost O(n²). With every key forced to one hash value, building a CPython `dict` of 1,000 keys took 40 ms on our test machine, 2,000 took 147 ms and 4,000 took 678 ms, each doubling roughly 4× slower, against well under 1 ms for ordinary integer keys.
4. **Expensive hashing or comparison.** Hashing a 1 MB string is O(1 MB). "O(1)" counts operations on keys, not the cost of each one; for long keys the real cost is O(key length).

What languages do about attack (3): **randomise the hash per process**, so attackers can't precompute collisions. Python seeds `str` and `bytes` hashing with SipHash-1-3 and a random key at startup (`PYTHONHASHSEED` fixes it for reproducible tests); Go randomises its map hash seed; Java 8+ keeps chaining but turns a bucket into a balanced tree once its chain reaches 8 entries (and the table has at least 64 buckets), capping a bad bucket at O(log n).

> [!PITFALL] Mutating a key after inserting it
> Store a list-like or mutable object as a key, change one of its fields, and its hash changes: the entry still sits in the old slot, so `get` jumps to the new slot and misses it. Python forbids `list` keys for this reason. In Java and C++ it compiles and silently loses entries. Use immutable keys: tuples, strings, frozen records.

> [!INTERVIEW]
> Hashing unlocks the "have I seen it?" family: **Two Sum** (store `target − x`), **Longest Substring Without Repeating Characters** (last index of each char), **Group Anagrams** (sorted string or letter counts as key), **Subarray Sum Equals K** (prefix sum counts), **LRU Cache** (hash map + doubly linked list). When you claim O(1), add "expected, assuming a good hash", and be ready for "what's the worst case?": O(n) per operation, and why.

## Edge cases and pitfalls

- **Empty table.** `get` on an empty open-addressing table must hit EMPTY at once. A table that is *full* of tombstones and live keys has no EMPTY slot, and `get` for a missing key loops forever. Resizing on `used` (not `n`) prevents it.
- **Negative keys.** In Python `-3 % 8 == 5`, but in C++, Java, JavaScript and Go `-3 % 8 == -3`, a negative index. Use `(h % m + m) % m`, or mask with `h & (m - 1)` when `m` is a power of two.
- **Overwriting vs inserting.** `put` of an existing key must not increment `n`, or the table resizes early and `len()` lies.
- **Equality and hash must agree.** If `a == b` then `hash(a) == hash(b)`. Override one without the other and equal keys land in different slots.
- **C++ `operator[]` inserts.** `if (seen[x])` adds `x` with value 0 when it's missing. Use `find` or `count` (or `contains` in C++20).
- **JavaScript `{}` coerces keys to strings.** `o[1]` and `o["1"]` are the same entry; a `Map` keeps them apart.

## Check yourself

> [!CHECK] A table of 8 buckets uses `h(k) = k mod 8`. You insert 3, 11, 19, 27. What's the longest chain, and which single change to `m` spreads them out?
> All four are 3 mod 8, so one chain of 4. Any `m` that doesn't divide 8 breaks the pattern; with a prime such as `m = 7` they land in slots 3, 4, 5, 6. The real fix is a hash that mixes the bits before reducing, so the choice of `m` stops mattering.

> [!CHECK] In the linear-probing table, you remove a key by writing EMPTY and then *immediately* shift the next keys back one slot. Is that enough to stay correct?
> Not in general. A key further on may belong to an earlier home slot and be needed where it is, or belong to a slot after the hole and must not move before its home. The correct "backward-shift deletion" moves a later key into the hole only when its home slot is at or before the hole (cyclically). That is exactly the probe-path invariant again. Tombstones avoid the analysis at the price of longer probes.

> [!CHECK] A service stores session IDs in a hash map that doubles at α = 0.75. Most of the day, p99 latency is 2 ms, but a few requests a day take 300 ms. What's a likely cause, and two fixes?
> A resize: one insert rehashes millions of keys at once. Fixes: pre-size the table (`reserve` / capacity hint) to the expected peak, or use an incrementally resizing map that moves a few buckets per operation (Redis does this for its dictionaries). Amortised O(1) is a statement about totals, not about each request.

> [!CHECK] Why does an attacker need to know your hash function to make a hash map O(n), and why doesn't Java's treeification need randomisation to cap the damage?
> To collide, keys must share a hash value (or slot), which requires predicting the function; a random per-process seed removes that. Treeification doesn't stop collisions, it changes what a collision costs: a bucket of n colliding keys becomes a balanced tree, so lookups cost O(log n) instead of O(n), whatever the attacker does.

> [!RECAP]
> - A hash function turns a key into an index, so lookup is one jump plus a scan of one short chain or probe run.
> - O(1) is the **expected** cost under a good hash and a bounded load factor α = n/m; the worst case is O(n).
> - Chaining keeps a list per slot; open addressing probes the array and needs tombstones to delete.
> - Doubling on a load threshold makes resizing amortised O(1): 1,000 inserts move about 1,500 keys.
> - Weak hashes on patterned keys, adversarial keys, mutable keys and expensive keys are how the O(1) breaks.
