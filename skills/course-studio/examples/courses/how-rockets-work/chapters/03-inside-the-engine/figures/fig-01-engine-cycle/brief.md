# Figure brief: fig-01-engine-cycle

<!-- First non-heading line is shown in the chapter while the figure is pending. Keep it one sentence. -->
SpaceX's Raptor 2 hangs in a test stand; hover to take it apart part by part, then fire it and watch the preburners light before the main chamber reaches 300 bar and 230 tf.

- **Course / chapter / position:** How Rockets Work · Ch 3 · Fig 1 of the chapter
- **Size:** Hero (a dense real machine with several moving systems: 11 assemblies, plumbing, harness, a shader plume). Adapted from Anatomy's bundled `examples/raptor-engine`, so the drawing exists; the work is wiring it to this chapter's model and words.
- **Reader:** knows thrust is mass thrown backwards (Ch 1) and that most of a rocket is propellant (Ch 2); has just read that the hard part of an engine is pumping about 650 kg of propellant per second into a chamber at 300 bar.

## The idea it must make obvious
Each propellant drives its own pump on the way to the chamber: all the oxygen passes through an oxygen-rich preburner that spins the oxygen pump, all the methane through a fuel-rich preburner that spins the methane pump, and the two hot gases meet in the main chamber. Nothing is thrown overboard.

## Truth (the model)
`model.mjs`, shared with the chapter. Sources in its header (checked October 2026).
- Raptor 2: 230 tf at sea level, 300 bar main chamber pressure, 1,630 kg dry, mixture ratio about 3.6 by mass, 1.3 m nozzle exit, about 650 kg/s of propellant.
- Derived: back-pressure on the exit at sea level 13.7 tf, so about 244 tf with no air; thrust-to-weight about 141; effective exhaust speed about 3.5 km/s; thrust at 150 bar about 108 tf.
- Start sequence the readout follows: chill-down and venting → spin-up, preburners lit (chamber pressure rising from about 13% of full) → main stage, `Pc 300 bar · 230 tf` → shutdown and purge.

## The object
The engine itself, hung from a vertical test stand: a deck with a flame cone and deluge ring, two columns, a crosshead with a load cell and two gimbal actuators. Below the gimbal: oxygen turbopump, oxygen-rich preburner, injector and main chamber, bell nozzle with its cooling manifold. On the right: methane turbopump and fuel-rich preburner, joined by the hot-gas manifold and a downcomer; ducts, sense lines and the controller's harness.

- **What moves, and what that motion means:** parts lift away one by one (01 to 11, top of the engine down) = every assembly a propellant passes through, shown separately; on Ignite, the plume grows as chamber pressure rises = thrust follows pressure.
- **Mapping:** each numbered part in the legend (01 to 11) is one real assembly with its real job; the readout's bar and tf are the chamber pressure and the load cell's thrust.
- **The one lit part:** the part under the pointer (its name and job show in the readout).

## Interaction
- **Pointer:** hover the engine to take it apart; hover a legend part to light it.
- **Keyboard:** arrow keys take it apart part by part; I or the Ignite button fires it; Escape puts it back together.
- **Idle tour:** takes the engine apart in legend order, then closes it up and fires it.
- **Readout:** idle `1,630 kg · cold`; a lit part shows its job, e.g. `main chamber · 300 bar · no igniter`; burning shows `spin-up · preburners lit · … bar`, then `Pc 300 bar · 230 tf`.

## Card text
- **Fig:** Fig 1
- **Title:** Raptor 2 · test stand
- **Hint:** Hover the engine to take it apart
- **Legend keys:** the 11 numbered assemblies (01 Gimbal and thrust puck … 11 Nozzle)
- **Caption:** Raptor 2 is SpaceX's full-flow staged-combustion engine: liquid oxygen and methane at a mixture ratio of 3.6, 300 bar in the main chamber, 230 tf at sea level, 1,630 kg dry. Every drop of oxygen passes through an oxygen-rich preburner that spins the oxygen pump, and every drop of methane through a fuel-rich preburner that spins the methane pump; the two hot gases meet in the main chamber, which has no igniter of its own. The load cell above the gimbal reads the thrust while it burns.

## How the chapter uses it
Before: "Hover the engine and it comes apart, one numbered assembly at a time. Then press Ignite and watch the readout: the preburners light first, and only then does the chamber climb to 300 bar." After: "The two pumps are spun by gas made from the propellants they pump. Nothing left the engine except through the nozzle."

## Done when
- `node build.mjs` writes `fig-01-engine-cycle.html` and `fig-01-engine-cycle-light.html`; the audit inside the build passes.
- Desktop, 390 px phone, both themes checked in the chapter.
- A learner who only plays with the figure can say which gas spins which pump.
