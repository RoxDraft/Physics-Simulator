# Physics-Simulator
Simulate Focus On Application of Physics 1 Mechanics and Thermodynamics, 2 Electromagnetics and Wave with Modern Physics like Quantum Mechanics

- Mentors and Cowork: Gemini 3.8 flash / 4 Argon and Claude Opus 5.5
  
- University-level physics courses (Physics I and Physics II) are generally divided into the following main topics:

Physics I (Mechanics and Thermodynamics): Focuses on the study of motion, force, energy, and matter, such as kinematics, Newton's laws of motion, work and energy, momentum, rotation, gravity, fluid mechanics, and thermodynamics (heat and gases).

Physics II (Electromagnetic and Waves): Focuses on the study of electricity, magnetism, light, and modern physics such as static electricity, electric fields and electric potential, electric current and circuits, electromagnetism, magnetic induction, electromagnetic waves, and optics (wave optics and geometry).

Is quantum physics included? Generally, Physics II includes a short summary at the end (often called Modern Physics) that lays the groundwork for quantum physics, such as quantum theory of energy, the photoelectric effect, atomic spectra (e.g., Bohr's atomic model), and de Broglie's wave theory. However, it doesn't delve into deep quantum physics (such as the Schrödinger equation), which are usually studied separately in Modern Physics.

- Yes, it can definitely be simulated. Currently, industry and research widely apply Physics I and II in many areas, as follows:
Mechanics simulation (Physics I): Used in game and animation development to calculate gravity, collisions, and object motion (e.g., engines like PhysX or Box2D), as well as in automotive and aircraft design for crash testing and fluid dynamics (CFD).

Electromagnetic and wave simulation (Physics II): Used in the design and analysis of 5G/6G antennas, magnetic field simulation in electric motors for EVs, high-frequency electronic circuit design (PCB Layout), and light propagation simulation in 3D graphics (Ray Tracing).

Advanced research and industry: For example, the use of quantum computing and molecular structure simulation software in modern physics to develop materials science, medicine, or supercapacitors.

- It's one of the technologies that is currently transforming the IT world. It's called Quantum Computing, which uses principles from modern physics and quantum mechanics to process information.
The key principles that distinguish quantum computing from conventional computers are as follows:

Qubit: Instead of using regular bits, which are just 0s or 1s, quantum computers use qubits, which can exist in superposition states—i.e., both 0 and 1—simultaneously. This allows them to compute massive amounts of data simultaneously, a dramatic leap in speed compared to conventional computers.

Entanglement (Quantum Entanglement): A phenomenon where two qubits are mysteriously linked together, even when far apart, enabling extremely fast and efficient data transmission and processing.

Quantum Algorithms: Quantum-based programming or algorithms, such as Shor's Algorithm, can decrypt security codes (e.g., RSA) that would take a normal computer millions of years to calculate, in just a few minutes.

Currently, it is being applied to model complex chemical molecules for drug development, solving highly complex transportation and logistics routing problems, as well as financial analysis and cryptography.

---

## Simulators in this repo

Open `index.html` in a browser (or enable GitHub Pages: Settings → Pages → Deploy from branch `main`, folder `/`). No build step or install is needed.

| Folder | Simulator | Pages |
|---|---|---|
| [`ocean-waves/`](ocean-waves/index.html) | **Ocean Wave Simulator** — wind sea, swell, shoaling/breaking, tsunami and tide. Water-particle orbits, wave speed, period and power from the linear dispersion relation, plus how we use ocean waves (wave energy converters, coastlines, warning systems). | 2 |
| [`plate-tectonics/`](plate-tectonics/index.html) | **Plate Tectonics Lab** — world map of plate boundaries, M ≥ 7 earthquakes (USGS, 1965–2016) and active volcanoes (Smithsonian GVP), statistics by country, plate-boundary animations, seismic waves and epicentre location, early-warning time, response plans by magnitude, building resonance, seismic codes, and ground/satellite sensors. | 4 |
| [`camera-lab/`](camera-lab/index.html) | **Camera Lab** — six experiments: thin-lens ray diagram (phone camera, microscope, telescope), photon shot noise vs. light level and sensor size, multi-camera zoom and the ISP pipeline, stereo depth and Spatial Photo/Video, OIS vs. EIS stabilisation, and temperature / humidity / radiation effects. | 7 |
| [`mechanics-lab/`](mechanics-lab/index.html) | **Mechanics Lab** — a backhoe (tipping moments, ISO 10567 rated lift, slewing) and a container ship (buoyancy, GM, wind heel), plus sub-pages: **statics** (ladder friction, Pratt/Howe truss solver with buckling check), **dynamics** (stopping distance, crash impulse with crumple zone/seatbelt/airbag), **thermodynamics** (chip thermal resistance and throttling, room cooling load and AC refrigeration cycle), **fluids** (condo water pressure and zoning, pump vs. system curve in coolant loops) and the **swim start**. | 7 |
| [`beam-fea/`](beam-fea/index.html) | **Beam FEA** — a real 1-D finite element solver (40 Hermite beam elements, K·u = F) with von Mises / bending-stress colour maps, SFD/BMD, deflection limits and a textbook check. Presets: condo floor beam, factory crane runway, balcony, warehouse roof, timber footbridge. | 2 |
| [`circuit-lab/`](circuit-lab/index.html) | **Circuit Lab** — series/parallel circuit with animated current, a home distribution board (breakers tripping on overload or short circuit, earth leakage with/without earth wire and RCD, wire size, voltage drop, cost per hour), RC charging, and **from circuits to computers**: MOSFET switch, CMOS gates, a 4-bit adder, a D flip-flop register and a tiny fetch–decode–execute CPU. | 3 |
| [`chem-bio-lab/`](chem-bio-lab/index.html) | **Chem · Bio Lab** — collision-theory particle box with temperature, concentration, Ea and catalyst; an agent-based SEIR epidemic with masks, vaccination, distancing and isolation, plus data analysis (log-linear growth fit, doubling time, R0); and an SEIR ODE "flatten the curve" model. | 2 |
| [`quantum-lab/`](quantum-lab/index.html) | **Quantum Lab** — photoelectric effect (photon energy vs. work function, camera sensors, solar cells), quantum tunnelling (STM, gate-oxide leakage, flash memory), quantum dots and LED colour, a qubit on the Bloch sphere with H/X/Z/S/T gates and measurement statistics, and photonics: total internal reflection in fibre, attenuation and EDFA amplifiers, DWDM capacity. | 2 |
| [`space-lab/`](space-lab/index.html) | **Space Lab** — a hub page to choose the **Orbit Lab** simulation (launch, orbit raising, station-keeping with thruster exhaust, end of life over Point Nemo or to a graveyard orbit, re-entry heating and break-up down to the ground) or the **report** on the space industry (launch cost, launches per year, ISS vs Tiangong, propellants and RTGs, re-entry, Falcon 9 reuse, the Space Shuttle). Thai and English (`en/`). | 3 |
| [`synchrotron-lab/`](synchrotron-lab/index.html) | **Synchrotron Lab** — a hub page to choose the **synchrotron control room** simulation (ring size, energy lost to light per turn, RF cavity on/off, spectrum vs lasers, presets from Siam Photon to the LHC) or the **report** on how synchrotrons work and differ from lasers. Thai and English (`en/`). | 3 |

```
index.html            landing page linking every simulator
shared/dc-runtime.js  tiny runtime that renders the pages (no dependencies)
ocean-waves/          index.html, uses.html
camera-lab/           index.html, lens.html, sensor.html, fusion.html,
                      spatial.html, stabilize.html, environment.html
mechanics-lab/         index.html, statics.html, dynamics.html, thermo.html, fluids.html, swim.html, sources.html
circuit-lab/           index.html, computer.html, sources.html
beam-fea/ chem-bio-lab/ quantum-lab/   index.html, sources.html
space-lab/            index.html (choose), orbit-lab.html (simulation), report.html (document), img/
synchrotron-lab/      index.html (choose), simulation.html, report.html, img/
                      (standalone pages, not built from src/; their English hub pages are en/space-lab/ and en/synchrotron-lab/)
src/                  canvas sources (.dc.html) for every page
tools/build.sh        rebuilds all pages from src/ in Thai and English (home bar + language button)
tools/i18n/en.json    English text for every Thai string; the build stops if one is missing
en/                   English versions of every page (generated)
data/plate-tectonics/ open datasets → map data script, with provenance notes
tools/gen_sources.py  the Sources page of every simulator (open / restricted / estimated)
tools/dc2html.py      converts one canvas artboard into a page here
```

### How the pages work

Each page keeps its markup in a `<template id="dc-template">` with `{{holes}}`, `<sc-for>` loops and `<sc-if>` branches, and its physics in a `class Component extends DCLogic { renderVals() { … } }` script. `shared/dc-runtime.js` calls `renderVals()` whenever the state changes and patches the page in place, so sliders and animations update live.

After editing anything in `src/`, rebuild with:

```bash
bash tools/build.sh
```

To add a new simulator, put its `.dc.html` files in `src/<name>/` and add a block for it in `tools/build.sh`.

Every simulator has a **Sources** page listing which data is openly available, which exists but has restricted access, and which values are our own estimates.

The models are simplified for learning (thin lenses, linear wave theory, photon shot noise). Device figures are representative examples, not the specs of any particular model.
