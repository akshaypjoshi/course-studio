// Truth model for fig-01-engine-cycle and Ch 3 "Inside the engine". The chapter quotes these numbers;
// raptor.mjs draws and animates from them. Sources (checked October 2026):
//   thrust and chamber pressure: SpaceX statements reported on Wikipedia "SpaceX Raptor"
//     (230 tf consistently by Feb 2022; 300 bar main chamber pressure by Jul 2022)
//   dry mass: SpaceX, 3 Aug 2024 (Raptor 1 2,080 kg, Raptor 2 1,630 kg, Raptor 3 1,525 kg)
//   mixture ratio about 3.6 by mass; sea-level nozzle exit 1.3 m (SpaceX figures, 2018)
//   propellant flow about 650 kg/s (510 kg/s oxygen, 140 kg/s methane), as cited on Wikipedia
export const CHAMBER_BAR = 300;      // main chamber pressure, bar
export const SEA_LEVEL_TF = 230;     // sea-level thrust, tonnes-force
export const DRY_KG = 1630;          // engine dry mass, kg
export const MIXTURE = 3.6;          // oxygen : methane by mass
export const EXIT_M = 1.3;           // nozzle exit diameter, m
export const FLOW_KG_S = 650;        // total propellant flow, kg/s

const G0 = 9.80665, ATM = 101325;
export const thrustN = SEA_LEVEL_TF * 1000 * G0;                            // 2.26 MN
export const backTf = (ATM * Math.PI * (EXIT_M / 2) ** 2) / (1000 * G0);    // air pushing on the exit
export const vacuumTf = SEA_LEVEL_TF + backTf;                              // same engine, no air
export const thrustToWeight = (SEA_LEVEL_TF * 1000) / DRY_KG;
export const exhaustMs = thrustN / FLOW_KG_S;                               // effective exhaust speed
export const oxygenShare = MIXTURE / (1 + MIXTURE);
// thrust at a throttled chamber pressure: flow scales with pressure, minus the same back-pressure term
export const thrustAt = (bar) => vacuumTf * (bar / CHAMBER_BAR) - backTf;
