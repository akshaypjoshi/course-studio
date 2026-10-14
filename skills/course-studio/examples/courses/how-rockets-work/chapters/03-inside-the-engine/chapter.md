---
title: Inside the engine
dek: A rocket engine is a pump problem. Raptor burns a little of each propellant just to drive its pumps, and throws nothing away.
chapter: 3
minutes: 30
level: Beginner
glyph: R2
outcomes:
  - Trace oxygen and methane through a full-flow staged-combustion engine, part by part
  - Explain why the pumps, not the fire, are the hard part of a rocket engine
  - Check an engine's spec sheet with thrust = propellant flow × exhaust speed
  - Say why the same engine pushes harder in space than at sea level
---

## The one idea

Burning propellant is easy. The hard part of a rocket engine is **getting about 650 kg of propellant every second into a chamber that is already at about 300 times atmospheric pressure**. That takes pumps, the pumps need tens of megawatts of power, and the only power on board is the propellant itself. How an engine powers its pumps is called its *cycle*, and it decides almost everything else about the engine.

This chapter takes apart SpaceX's Raptor 2, the methane and liquid-oxygen engine that powers Starship. Thirty-three of them fire at once on the Super Heavy booster, and six more on the ship. Raptor uses the most complete cycle there is, **full-flow staged combustion**: every kilogram of both propellants passes through a turbine on its way to the main chamber, and nothing is thrown overboard.

## Watch it work

The figure is Raptor 2 hanging upside down in a test stand, the way engines are fired on the ground: the load cell in the crosshead above it measures thrust, and the flame goes down into the cone in the deck.

Hover the engine and it comes apart, one numbered assembly at a time. Look for the two pumps: the **oxygen turbopump** (02) sits on the engine's axis under the gimbal, and the **methane turbopump** (08) hangs on the right. Each has a small chamber of its own fixed to it, a **preburner**. Then press Ignite and watch the readout: the engine chills down and vents first, then the **preburners light and the pumps spin up** while the chamber pressure is still low, and only then does the main chamber climb to **300 bar and 230 tf**.

::figure fig-01-engine-cycle

What you just saw is the whole cycle in order. The pumps had to be turning before the main chamber could burn at full pressure, and what turned them was gas made from the propellants they were pumping. When the readout said `Pc 300 bar · 230 tf`, everything leaving the engine was leaving through the nozzle.

## Why the pumps are the hard part

Gas only flows from high pressure to low. To push propellant into a chamber at 300 bar, the pumps must deliver it at an even higher pressure, to overcome the injector and the cooling passages on the way. Three hundred bar is the pressure about 3 km under the sea.

Raptor 2 swallows about 650 kg of propellant per second: about 510 kg of liquid oxygen and 140 kg of liquid methane, the 3.6 to 1 mixture by mass the engine runs at. Pumping that much liquid to that pressure takes tens of megawatts, about what a small power station makes, so each pump needs a serious turbine. The question every engine designer answers first is **where that turbine power comes from**:

- **Pressure-fed:** no pumps at all. The tanks themselves are pressurised. Simple, but the tanks must be thick and heavy, so chamber pressure stays low. Used for small thrusters.
- **Gas generator:** burn a little propellant in a small chamber, spin the turbine with it, and **dump the turbine's exhaust overboard**. SpaceX's Merlin, on Falcon 9, works this way. Simple and robust, but the dumped gas is propellant that never reaches the main chamber.
- **Staged combustion:** burn a little propellant in a *preburner*, spin the turbine, then **send the turbine exhaust into the main chamber** to finish burning. Nothing is wasted. Most staged-combustion engines have only one kind of preburner: the RD-180 runs oxygen-rich, while the Space Shuttle's RS-25 uses two fuel-rich preburners.
- **Full-flow staged combustion:** two preburners, one per propellant, so **all** the oxygen and **all** the methane pass through a turbine. Raptor is the first engine of this kind to fly.

> [!KEY]
> In a full-flow engine each propellant drives its own pump. Oxygen-rich gas spins the oxygen pump; methane-rich gas spins the methane pump. Then the two gases meet in the main chamber.

## Take it apart: the parts and the cycle

Here is what each assembly in the figure does. The numbers match the figure's legend.

| # | Assembly | Its job |
|---|---|---|
| 01 | Gimbal and thrust puck | Carries all 230 tf into the vehicle; two actuators tilt the engine to steer (Chapter 5) |
| 02 | Oxygen turbopump | Pumps liquid oxygen; its turbine is spun by oxygen-rich gas |
| 03 | Oxygen-rich preburner | Burns all the oxygen with a little methane to make hot, oxygen-rich gas |
| 04 | Oxygen duct and main valve | Carries oxygen from the pump to the preburner, and opens to start the engine |
| 05 | Engine controller and harness | The engine's computer: valves, sensors, the start and shutdown sequence |
| 06 | Injector and main chamber | Where the two hot gases meet and burn at 300 bar |
| 07 | Hot-gas manifold | Carries the methane-rich gas from its turbine across to the injector |
| 08 | Methane turbopump and fuel-rich preburner | Pumps liquid methane; its turbine is spun by methane-rich gas |
| 09 | Downcomer and main fuel valve | Sends methane down to cool the chamber and nozzle walls first |
| 10 | Plumbing | Ducts, sense lines and purge lines between everything else |
| 11 | Nozzle | Turns the chamber's pressure into speed; methane flows through its wall to keep it from melting |

Now follow each propellant through, in order.

**Oxygen.** Liquid oxygen enters the **oxygen turbopump** (02) and leaves at high pressure through the **oxygen duct** (04). All of it goes into the **oxygen-rich preburner** (03), where a small amount of methane is burned in it. That makes hot gas that is mostly oxygen: hot enough to drive a turbine, not hot enough to melt it. The gas spins the turbine on the oxygen pump's shaft, so **the oxygen powers its own pump**. Then it carries on into the injector.

**Methane.** Liquid methane enters the **methane turbopump** (08). Before it burns, it does a second job: the **downcomer** (09) sends it through channels in the walls of the nozzle and chamber, cooling them. Then all of it goes into the **fuel-rich preburner**, where a small amount of oxygen is burned in it, making hot, methane-rich gas that spins the methane pump's turbine. The **hot-gas manifold** (07) carries that gas across to the injector.

**The main chamber.** Both streams arrive at the **injector** (06) as hot gas, not liquid, so they mix fast and burn completely. On Raptor 2 the main chamber has **no igniter of its own**: the preburners have igniters, and the hot gases they send down light the main chamber. The burning gas reaches 300 bar, and the **nozzle** (11) turns that pressure into a jet leaving at about 3.5 km/s.

> [!INTUITION]
> Think of the preburners as the engine paying itself first. A small part of the propellant is burned early to make the power that pumps all of the propellant, and then that "spent" gas still goes on to make thrust.

## Why it's built this way

Every choice in Raptor's cycle buys something and costs something.

> [!TRADEOFF] Full flow vs a gas generator
> A gas-generator engine like Merlin is simpler and has a long, clean record, but it throws the turbine gas away and runs at much lower chamber pressure. Full flow sends every kilogram through the main chamber at 300 bar, which means more thrust from the same size engine. The price is complexity: two preburners, two turbines, two start-up sequences that must be timed to each other.

**Why two preburners help the turbines.** In a single-preburner engine one turbine is driven by a small fraction of the flow, so that gas has to be very hot to deliver the power. In a full-flow engine *all* the propellant passes through the turbines, so the same power comes from a much larger flow of cooler gas. Cooler turbines last longer, which matters for an engine meant to fly again and again. It also means oxygen and methane never meet inside a pump, so there's no need for the seal that other designs use to keep them apart.

**Why oxygen-rich gas is dangerous.** Hot, high-pressure oxygen will burn most metals. The oxygen-rich side of the engine needs special materials and coatings that survive it.

**Why methane.** Kerosene, Merlin's fuel, leaves soot in the engine when it burns fuel-rich. Methane burns much more cleanly, which suits a reusable engine and makes a fuel-rich preburner practical. SpaceX has also pointed out that methane can be made on Mars from carbon dioxide and water. Both propellants are stored *subcooled*, chilled close to their freezing points, which makes them denser so more fits in the tanks.

## The numbers, and what limits them

These are the figures the chapter and the figure use. They change as the engine is developed, so each has its date.

| Raptor 2 | Value | Source and date |
|---|---|---|
| Thrust at sea level | 230 tf (2.26 MN) | SpaceX, reached consistently by February 2022 |
| Main chamber pressure | 300 bar | SpaceX, July 2022 |
| Dry mass | 1,630 kg | SpaceX, August 2024 |
| Mixture ratio (oxygen : methane) | about 3.6 by mass | SpaceX figures as cited in public analyses |
| Propellant flow | about 650 kg/s | derived from published thrust and efficiency |
| Nozzle exit diameter | 1.3 m | SpaceX, 2018 |

You can check a spec sheet like this with three lines of arithmetic.

**Thrust = propellant flow × exhaust speed.** 230 tf is 230,000 × 9.81 ≈ 2.26 million newtons. Divide by 650 kg/s and you get about **3,470 m/s**: the effective speed of the jet. If a spec sheet's thrust, flow and exhaust speed don't multiply out, one of them is wrong.

**Thrust-to-weight.** 230,000 kg of push from a 1,630 kg engine is about **141 times its own weight**. A car engine can't lift itself at all.

**Why the same engine pushes harder in space.** At sea level the air presses on the nozzle's exit, the opening where the jet leaves, pushing back against the engine. The exit is 1.3 m across, an area of π × 0.65² ≈ 1.33 m², and air pressure is about 101,000 newtons per square metre, so the air pushes back with about 135,000 N, or **13.7 tf**. With no air, the same engine running the same way would make about **244 tf**. The figure's readout uses exactly this model.

> [!PITFALL] "Thrust is the flame pushing on the air"
> It isn't. The burning gas pushes on the inside of the chamber and nozzle, and that is what moves the rocket. The air only gets in the way: it pushes back on the exit, which is why thrust *rises* as the rocket climbs. A rocket works best in a vacuum.

What limits the numbers is heat and pressure. Higher chamber pressure means more thrust from the same engine, but every bar needs more pump power and puts more load on the walls, and every part in the hot-gas path has to survive temperatures that would melt it without cooling.

## Variants

- **Raptor Vacuum.** The same engine with a much larger nozzle, cooled the same way, used on the ship for flying in space. A larger exit lets the gas expand further and leave faster, but at sea level the air would push too hard on such a big exit, so the booster uses only sea-level engines.
- **Raptor 3.** A redesign with fewer external parts, many pipes and sensors moved inside the engine's castings. In August 2024 SpaceX reported 280 tf in ground testing at 350 bar, and a mass of 1,525 kg. In May 2026 SpaceX gave its nominal thrust as 250 tf. Expect these numbers to keep changing.
- **Other cycles flying today.** Falcon 9's Merlin (gas generator, kerosene); Blue Origin's BE-4 (staged combustion with a single oxygen-rich preburner, methane); the RS-25 (staged combustion with two fuel-rich preburners, hydrogen).

## How it fails

- **A pump that can't keep up.** If a turbopump loses speed, chamber pressure drops, and thrust drops faster than you'd guess. At half pressure the flow halves, but the air still pushes back with the same 13.7 tf, so thrust falls to about 108 tf, a bit under half.
- **Oxygen-rich fire.** A leak or a hot spot on the oxygen-rich side can start the engine's own metal burning. Shutting down fast and safely is part of the controller's job.
- **Start-up timing.** The two preburners must light and the two pumps spin up together. If one side runs ahead, the mixture in the main chamber is wrong at the moment it lights.

## Check yourself

> [!CHECK] A Raptor 2 makes 230 tf at sea level. Roughly what does the same engine make at the edge of space, running the same way?
> About 244 tf. With no air pushing back on the 1.3 m exit, it gains the 13.7 tf the atmosphere was taking away: 101,000 N/m² × 1.33 m² ≈ 135,000 N ≈ 13.7 tf.

> [!CHECK] Why does a full-flow engine need two turbines, where a gas-generator engine can drive both pumps from one?
> Because each propellant drives its own pump. All the oxygen goes through the oxygen-rich preburner and its turbine, and all the methane through the fuel-rich one. A gas generator burns a small side stream in one chamber and can put both pumps on one shaft, but then it throws that gas away.

> [!CHECK] A test runs the engine at 150 bar instead of 300. Is the thrust about 115 tf, or less? Why?
> Less: about 108 tf. Flow, and so the push inside the engine, scales with chamber pressure, giving about 122 tf. But the air's push-back on the exit doesn't shrink with it: 122 − 13.7 ≈ 108 tf.

> [!CHECK] The ship flies its Raptor Vacuum engines in space but the booster has none. What would go wrong with a vacuum nozzle on the booster at launch?
> At sea level the air would press on its much larger exit and the gas inside would be over-expanded, below the outside pressure, near the walls. That costs thrust and can let the flow separate from the nozzle wall and shake it. Big vacuum nozzles only pay off where there's no air.

> [!RECAP]
> - A rocket engine's hard part is **pumping**: about 650 kg/s into a chamber at 300 bar, powered only by the propellant.
> - **Full-flow staged combustion**: all the oxygen drives the oxygen pump via an oxygen-rich preburner, all the methane drives the methane pump via a fuel-rich one, and both hot gases finish burning in the main chamber. Nothing is dumped.
> - Raptor 2: **230 tf, 300 bar, 1,630 kg**, so thrust-to-weight is about 141 and the exhaust leaves at about 3.5 km/s.
> - The air pushes back on the nozzle exit (about 13.7 tf at sea level), so thrust **rises** as the rocket climbs.
