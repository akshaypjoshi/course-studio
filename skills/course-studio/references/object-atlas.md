# Object atlas: concept → machine

Anatomy's hardest step is "invent the object": a real, recognisable machine whose working *is* the concept. This atlas gives a starting object for the concepts that recur across the four preset courses (DSA, System Design, JavaScript, LLD). Use it as a head start, not a menu: check the mapping is one-to-one for *this* chapter's point, and change the object if the chapter's insight is a different one.

Each row: **concept** · **object** · **what moves = what it means** · **readout** (the live number on the card).

Contents: How to invent one · DSA · System Design · JavaScript, Deeply · Low-Level Design · Real machines, science and everyday systems · Reuse across a course

---

## How to invent one (for anything not listed)

1. Write the insight as a *mechanism* sentence: "X happens because Y forces Z." (Binary search: "half the candidates are discarded because one comparison against a sorted midpoint rules out a side.")
2. List the moving parts of the mechanism: the thing that changes, the thing that decides, the thing that is counted.
3. Find a workshop, lab, post-office, railway, kitchen or factory machine that has those same three parts. Prefer machines with **rails, carriages, gates, dials, springs, levers, trays, chutes**: they move legibly in isometric.
4. Check one-to-one: every concept part has a physical part and every physical part means something. Extra parts are structure (base, frame, screws), not new meaning.
5. Pick the one **lit** part: the thing whose motion *is* the insight.
6. Pick the **readout**: the number the chapter keeps talking about (comparisons, latency, load, depth).

Reject an object when: the reader must be told what it is (too abstract), it needs labels to work, the motion contradicts the concept (a queue drawn as something that serves from the back), or the concept's key number can't be read off the object.

## DSA

| Concept | Object | Moves = means | Readout |
|---|---|---|---|
| Array indexing, address arithmetic | Printer's type case: a tray of equal compartments under a pointer carriage on a ruled rail | Carriage jumps straight to compartment i (no walking) = O(1) random access; rail ticks = base + i·size | `i 6 · addr 0x18` |
| Prefix sums | Measuring tape laid along a row of blocks of different lengths | Sliding two calipers to any two tape marks reads a segment sum by subtraction | `sum[2..5] = 31` |
| Two pointers | Bench vise with two jaws closing on a row of sorted weights | Left jaw steps right if total is light, right jaw steps left if heavy | `L 1 · R 6 · sum 13` |
| Sliding window | Film strip advancing under a fixed-width viewing gate on a light table | Strip advances one frame; gate adds the new frame, drops the old | `window sum 18 · best 21` |
| Binary search | Rack of sorted gauge blocks with two sliding end stops (lo, hi) and a probe that drops at the midpoint | Probe reads mid; one stop jumps past it; span halves | `lo 4 · hi 7 · mid 5 · 3 probes` |
| Insertion sort | Library book trolley: the new book slides left until it meets a shorter one | Each slide = one shift | `shifts 7` |
| Merge sort | Two sorted conveyors meeting at a zipper gate that drops the smaller tray first | Gate picks min of two heads | `merged 6/10` |
| Quick sort / partition | Coin sorter with a pivot gate diverting smaller left, larger right | Gate setting = pivot; chutes = partitions | `pivot 42 · L 5 · R 4` |
| Stack | Spring-loaded plate dispenser (cafeteria) | Push compresses spring; only the top plate is reachable | `depth 4` |
| Queue / deque | Tray conveyor with a loading end and an unloading end (deque: gates at both ends) | Trays enter one end, leave the other in order | `front A · size 3` |
| Monotonic stack | Plate dispenser with a sizing gate: a bigger plate ejects every smaller one above | Ejected plates are answered ("next greater") | `answered 3` |
| Linked list | Railway wagons joined by couplers on a siding | Insert = uncouple, roll a wagon in, recouple two couplers; no wagon moves | `len 5 · couplers changed 2` |
| Hash map | Bench tray sorter: a hash dial with m stops beside a row of m trays on a slot ruler, and a gantry shuttle that carries each key tile | Dial needle = `h(k) mod m`; the shuttle passes over other trays without stopping (O(1)); a tray's stack height = chain length = comparisons | `key 15 → slot 7 · chain 2 · α 5/8` |
| Open addressing / probing | Same sorter with a stepping pawl: an occupied tray pushes the shuttle one tray on | Probe sequence = pawl steps; clusters = runs of full trays | `probes 3 · α 6/8` |
| Resizing / rehash | Same sorter with a second, twice-as-long tray rail and the shuttle moving every tile across | Doubling moves every key once; amortised O(1) | `m 8 → 16 · moved 6` |
| Heap / priority queue | Pegboard binary tree of cups with swap levers between parent and child | Inserted ball swaps upward while lighter than its parent | `swaps 2 · height 3` |
| BST | Coin ramp with a left/right flap at each junction (smaller goes left) | A coin's path is the search; depth = flaps passed | `depth 3` |
| Balanced trees (AVL / rotations) | Mobile of balance beams that re-hangs itself when one side tips | A rotation re-hangs three beams | `balance −2 → 0` |
| Trie | Railway switchyard: each letter throws a switch; words end at buffers with a flag | Typing a prefix routes the train; shared track = shared prefix | `nodes 14 · words 5` |
| Graph BFS | Pegboard of nodes joined by tubes; dye spreads one hop per tick from the source | Rings of equal colour = equal distance | `tick 2 · reached 6/9` |
| Graph DFS / backtracking | Maze with a thread spool on the explorer (Ariadne's thread) | Advancing unspools; dead end rewinds to the last junction = stack pop | `depth 4 · backtracks 2` |
| Dijkstra | Water manifold of pipes of different lengths with an arrival flag at each junction | First water to arrive at a junction fixes its distance | `dist(F) 11` |
| Topological sort | Assembly jig where a part's slot unlocks only when its prerequisites are seated | Indegree pins drop to zero → slot opens | `ready 2 · done 4/7` |
| Union-Find | Keyrings on hooks; union hangs one ring on another; path compression rehangs directly on the master | Find = follow rings to the hook | `sets 3 · hops 1` |
| Recursion / call stack | Freight lift descending floors, carrying a return value back up | Each floor = a frame; base case = ground floor | `depth 4 · returning 6` |
| Dynamic programming | Grid stamping machine filling a pegboard table; each stamp reads two neighbours first | Fill order = dependency order | `cell [3][4] = 7` |
| Memoization | Card catalog: each drawer filled once, re-reads pull the card | Second visit = no work | `calls 9 · hits 5` |
| Greedy (intervals) | Booking board with slot pegs on a timeline rail; the earliest-finishing peg locks first | Picks never revisited | `booked 4` |
| Big-O growth | Three machines on one bench processing the same tray stack at n, n log n, n² rates, tachometers on each | Doubling n doubles, ~doubles, quadruples the dial | `n 64 · ops 64 / 384 / 4096` |
| Bit manipulation | Row of DIP switches with a sliding mask template | Template shows AND/OR/XOR as which switches flip | `x 1011 · mask 0110` |

## System Design

| Concept | Object | Moves = means | Readout |
|---|---|---|---|
| Latency numbers | Relay race on one bench: L1 drawer, RAM shelf, SSD cabinet, network cart across the room | Distance travelled = time | `SSD 100 µs` |
| Load balancing | Water manifold with a rotary distributor arm feeding N turbines (round-robin) or pressure valves (least-connections) | Arm position / valve opening = routing policy | `A 34% · B 33% · C 33%` |
| Caching / cache key | Pin-tumbler lock: when every pin matches, the plug turns and nothing is redrawn | Matching pins = cache hit | `hit rate 92%` |
| Cache hierarchy / cache-aside | Workbench tool tray (cache) beside a warehouse rack (DB) with a retrieval cart | Miss sends the cart; result lands on the tray too | `miss → 40 ms · hit → 1 ms` |
| CDN / edge | Regional depots fed by one central warehouse; trucks only run on a depot miss | Depot stock = cached objects | `origin load 8%` |
| Consistent hashing | Turntable with server pegs on the rim and key balls that roll clockwise to the next peg | Adding a peg captures one arc only | `moved 1/6 keys` |
| Sharding / partitioning | Coin sorter routing by denomination (the shard key) into tubes | Bad key = one tube overflows (hot shard) | `max shard 41%` |
| Replication / lag | Pantograph copying a writer's stroke to two boards through a belt with slack | Belt slack = replication lag | `lag 120 ms` |
| Leader election / consensus | Single-line railway token machine: only the token holder may enter (write) | Token transfer = new leader term | `term 3 · leader B` |
| Quorum (R + W > N) | Panel of N lamps; a write lights W, a read checks R; overlap guaranteed when R + W > N | Overlapping lamps = seeing the latest write | `N 5 · W 3 · R 3` |
| Message queue / log (Kafka) | Tray conveyor (partition) with numbered trays and each consumer group's bookmark slider on a rail | Consumers advance their own bookmark | `offset A 41 · B 37` |
| Pub/sub fan-out | Pneumatic tube station delivering one capsule to several outlets | One publish, many deliveries | `fan-out 4` |
| Rate limiter (token bucket) | Hopper filling with tokens at a fixed rate; requests take a token through a gate; spillway caps capacity | Empty hopper = 429 | `tokens 3/10 · +2/s` |
| Circuit breaker | Real breaker with trip coil, trip counter and a reset timer | Trips after k failures, half-open probe after timeout | `state open · retry 8 s` |
| Back-pressure | Pipes with a pressure gauge and a relief valve before a slow pump | Valve opens when the consumer can't keep up | `pressure 0.8 bar` |
| B-tree / index | Card catalog cabinet: drawer labels route by range; leaves linked by a rail | Lookup = 3 drawer pulls | `pages read 3` |
| LSM tree | Inbox tray (memtable) flushing to sorted boxes on shelves, compactor merging boxes | Compaction = merge | `levels 3 · write amp 4×` |
| Bloom filter | Pegboard where k hammers punch holes; a check lowers k pins | All pins drop = "maybe"; any blocked = "definitely not" | `fp rate 1.2%` |
| Idempotency keys | Ticket punch that refuses an already-punched ticket | Second punch = no-op | `dup blocked` |
| Two-phase commit / saga | Railway interlocking frame: all levers set before the signal clears (2PC); or a ratchet with a release per step (saga, compensation) | Lever states = votes | `prepared 3/3` |

## JavaScript, Deeply

| Concept | Object | Moves = means | Readout |
|---|---|---|---|
| Event loop | Mailroom with one clerk desk (call stack), a priority tray emptied fully first (microtasks), a conveyor of envelopes (task queue), kitchen timers on a shelf (Web APIs) | Clerk only takes from the conveyor when desk and tray are empty | `log: A D C B` |
| Call stack & execution contexts | Stack of clipboards on a spike; each holds a function's local sheet | Return pulls the top clipboard | `depth 3` |
| Hoisting & TDZ | Stage with props pre-placed under covers; a cover lifts only when the script reaches that line | Touching a covered prop = ReferenceError | `x: in TDZ` |
| Scope chain | Nested glass display cases; a lookup walks outward through case doors | First case holding the name wins | `found in outer` |
| Closures | A tool on a lanyard with a key fob (its captured environment) that stays attached after the workshop (outer frame) is dismantled | The fob keeps the variables alive | `count 3 · frames gone 1` |
| `this` binding | Universal remote that controls whatever device it is pointed at (the call site) | `bind` = taping the remote to one device | `this → button` |
| Prototype chain | Stack of filing drawers; a lookup drops down drawer by drawer until a card is found or it hits the floor (null) | Shadowing = a card in an upper drawer | `hops 2 · found on Animal.prototype` |
| References vs values | Coat check: variables hold tickets, the heap holds coats; copying a ticket ≠ copying the coat | Mutate through either ticket | `same coat: true` |
| Garbage collection (mark & sweep) | Crane rig: hooks from roots lift everything reachable; what falls goes to the scrap bin | Unreachable = collected | `freed 3 objects` |
| Promises | Coat-check ticket that later lights "ready" or "lost" | State changes once | `fulfilled · 42` |
| async/await | Ticket machine where the clerk parks a job at `await` and serves the next customer | Resume = microtask | `suspended 1` |
| Generators / iterators | Music box with a crank that stops after each note (yield) | Each crank turn = `next()` | `note 3/8` |
| Debounce / throttle | Door with a dashpot closer (debounce) vs a turnstile with a metronome (throttle) | Bursts collapse to one / to a steady rate | `calls 1 / 12` |
| Hidden classes / inline caches | Stamping molds: objects pressed from the same mold share a shape plate | Adding a property in a different order = a new mold | `shapes 2` |
| Module loading / bundling | Parts warehouse with a picking cart following an import manifest | Tree shaking = parts never picked | `bundle 41 kB` |

## Low-Level Design

| Concept | Object | Moves = means | Readout |
|---|---|---|---|
| Encapsulation | Sealed instrument case with only knobs exposed | Internal gears move only through knobs | `invariants held` |
| Strategy | Drill chuck with interchangeable bits | Swapping a bit changes behaviour, not the drill | `strategy: hourly` |
| Observer | Old house bell board: one pull rings several bells on wires | Subscribe = attach a wire | `notified 3` |
| Factory / abstract factory | Stamping press with swappable dies | Same press, different product | `made: Truck` |
| Builder | Assembly jig with optional stations a part passes through | Each station = a builder step | `steps 4/6` |
| Singleton | Key cabinet with exactly one hook and a checkout card | Second request gets the same key | `instances 1` |
| Adapter | Travel plug adapter between a socket and a foreign plug | Interface translation, no rewiring | `fits: true` |
| Decorator | Camera with screw-on lens filters stacked in front | Each filter wraps the previous | `layers 3` |
| Composite | Power-strip tree: strips plugged into strips | Treat a strip like a single device | `devices 7` |
| Command (+ undo) | Kitchen ticket rail with a spike for completed tickets | Undo = pull the top ticket back off the spike | `history 5` |
| Chain of responsibility | Coin validator: gates in series, each accepts or passes on | First gate that handles it stops the coin | `handled by gate 2` |
| State pattern / state machines | Vending machine with a rotary mode cam / washing-machine program dial | Events turn the cam; each position allows different actions | `state: has-coin` |
| Dependency inversion | Wall socket plate: appliances depend on the socket shape, not the wiring behind | Swap the wiring, appliances unchanged | `coupling: interface` |
| Producer–consumer / bounded buffer | Bakery cooling rack with N slots between a baker and a packer | Full rack blocks the baker; empty blocks the packer | `rack 4/6` |
| Mutex / locks | Single-line railway token (or a one-key restroom) | Only the holder enters the critical section | `holder T2 · waiting 1` |
| Deadlock | Two railway sidings each holding the token the other train needs | Circular wait made visible | `cycle: yes` |
| Parking lot (machine-coding) | Model parking garage: ticket machine, floors, spot sensors, exit gate | Ticket = object lifecycle | `free 12/40` |
| Elevator system | Glass elevator shaft model with call buttons and a dispatcher drum | Scheduling = drum order | `car 1 → 7` |
| LRU cache (design) | Shelf with a push-rod: used items slide to the front, the back item drops into a bin | Eviction = falling off the back | `size 4/4 · evicted C` |

## Real machines, science and everyday systems

For a physical subject the object is usually **the thing itself**, cut away or taken apart so the working parts show. For an abstract one (money, markets, an ecosystem), invent a machine as above. Check every number against a published source before it goes on the card.

| Concept | Object | Moves = means | Readout |
|---|---|---|---|
| Rocket engine (how thrust is made) | The engine on a test stand, as in Anatomy's `examples/raptor-engine/` | Propellants flow through turbopumps into the chamber; the plume leaves the nozzle; an exploded view separates the parts | `Pc 300 bar · 230 tf` (Raptor 2, SpaceX figures) |
| Staging | A two-stage stack on a launch mount | Booster burns, separates and falls away; the upper stage lights and carries on lighter | `stage 2 lit · booster away` |
| Rocket equation (why most of a rocket is fuel) | A stack of propellant tanks on a scale beside a small payload | Each tank drained adds a fixed step of speed; the payload stays tiny | `Δv 9.4 km/s · 94% propellant` |
| Orbit (falling and missing) | Newton's cannon on a mountain on a small globe | Faster shots land further round until one never lands | `v 7.8 km/s · orbit` |
| Four-stroke engine | One cylinder cut away: piston, crank, two valves, spark plug | Intake, compression, power, exhaust in turn; valves open on cue | `stroke 3/4 · power` |
| Gears, torque | A gear train on a bench with a hand crank and a lifted weight | Small gear turns fast, big gear turns slow and lifts more | `ratio 4:1 · torque ×4` |
| Pin-tumbler lock | The lock cut away with a key going in | Each cut lifts its pin stack to the shear line; the plug turns only when all align | `pins 5/5 at shear line` |
| Refrigerator / heat pump | Compressor, condenser coil, expansion valve, evaporator on a frame | Refrigerant loops, hot on one side, cold on the other | `inside 4 °C · coil 40 °C` |
| Electric motor | A cutaway motor: rotor, magnets, commutator, brushes | The commutator flips the current each half turn so the rotor keeps turning | `rpm 3,000 · 0.5 A` |
| Heart | A four-chamber pump with valves, cut away | Chambers squeeze in sequence; valves snap shut to stop backflow | `72 bpm · 70 ml/beat` |
| Lungs, breathing | A bell jar with a rubber diaphragm and two balloons | Pulling the diaphragm down lowers pressure; the balloons fill | `inhale · tidal 500 ml` |
| Waves, interference | A ripple tank with two dippers, as in Anatomy's `examples/ripple-tank/` | Two sources make bright and dark bands where waves add and cancel | `λ 2 cm · 2 sources` |
| Tides | A small globe and moon on a turntable with a water shell | The water bulges towards and away from the moon as the globe turns | `high tide · 12 h 25 m` |
| Supply and demand | A balance with a price slider between buyers' and sellers' trays | Raising the price moves units from the buyers' tray to the sellers' | `price 4.00 · 120 sold` |
| Compound interest | A coin press that adds a slice to every coin in the stack each year | The stack grows faster each year because the slices also earn | `5% · year 10 · 1.63× the start` |
| Printing press (history) | A Gutenberg-style screw press with a type bed and a paper frame | Ink, press, lift: one sheet per pull | `sheets 240/h` |

Rows with real-world numbers are starting points: confirm each number for the exact model, year and conditions the chapter discusses before using it.

## Reuse across a course

- Keep **one visual family per course** so figures feel like a set: DSA lives on a workbench of rails, gauges and trays; SD in a utility room of pipes, valves and conveyors; JS in a mailroom/office; LLD in a model workshop of small machines. Anatomy's "consistent scale across a set" applies.
- A later chapter may **extend an earlier figure** (the hash tray sorter gains a second, longer tray rail for resizing). Reuse its model module and parts; it reads as progression.
- A notes page or cheat sheet **reuses** chapter figures by id instead of drawing new ones.
