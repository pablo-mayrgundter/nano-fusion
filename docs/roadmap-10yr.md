# NanoFusion 10-year development plan, 2027–2036

From physics modelling to proof-of-concept fabrication to mass fabrication of nano-fusion batteries.
Read with [`physics-baseline.md`](physics-baseline.md) (the targets) and
[`literature-review.md`](literature-review.md) (the evidence).

## Premise and honest framing

- **Given:** near-future atomic-level synthesis, so that a reaction site, its optical antenna, its
  photon source and its collector can be built to atomic specification.
- **Flagship hypothesis (Track B):** a synthetic crystal whose reaction sites are driven out of
  equilibrium by on-board photon sources can reach fusion rates useful for a battery.
- **Status of that hypothesis:** unproven and far from current evidence. Confirmed lattice effects are
  large in relative terms and useless in absolute terms; no nuclear effect of low-intensity light has
  been confirmed.
- **Therefore the plan is built around gates, not around the hypothesis being true.** The first three
  years are designed to find out cheaply. Every phase has a product or a publishable result that
  survives a "no."

My rough odds, to be revised as data arrives: a confirmed structure- or light-controlled change of a
nuclear rate by ≥ 2× at Gate 1, perhaps 1 in 5 (structure alone is likelier than light). Net electrical
energy from a nano-cell by 2036, well under 1 in 100. A sellable chip-scale particle source and a
world-class designed-lattice nuclear metrology platform, better than even.

## Four tracks on one platform

All four share the fabrication stack, the CAD model and the simulator, so work is not wasted on a pivot.

| Track | Idea | Physics status | Role |
|---|---|---|---|
| **B** Driven coherent lattice | Designed hydride/deuteride sites pumped by on-chip light via plasmons (electrons) or resonant phonons (lattice) | Needs new or unconfirmed physics | Flagship; decided at Gate 1 |
| **A** Screened lattice + nano-accelerator | keV–100 keV ions from field-ionisation nanostructures into a channeling, high-screening lattice | Known physics; gain capped by F ≈ 10⁻³–10⁻² | Metrology backbone and first product |
| **D** Electron-free nano-collider | Bare ions recirculating in atomically precise electrostatic traps at 1–10 V/nm | Known physics, unbuilt; Rider limit is the question | Hedge with the only known-physics path to F ≥ 1 |
| **C** Muon-catalysed nano-cell | The 2014 concept: geometry to defeat alpha sticking | Known physics; muon cost is the wall | Watch; revisit if muon sources improve |

## Atomic-fabrication capability levels

The plan is indexed to capability, not to a vendor. Each phase names what it needs and what it uses if
the capability is late.

| Level | Capability | Status |
|---|---|---|
| APM-0 | 2D, UHV, scanning-probe; ≤ 10⁴ placed atoms; few chemistries | Today (HDL, P-in-Si, C₂ mechanosynthesis) |
| APM-1 | 2.5D, ≤ 10⁶ atoms, C/Si/B/N/H/D plus one metal; 10²–10⁴ parallel tips | Site scale |
| APM-2 | 3D heterostructures, ~10⁹ atoms (a 250 nm cube) | Pixel scale |
| APM-3 | 10¹²–10¹⁵ atoms (a 50 µm tile) | Tile scale |
| APM-4 | ≥ 10²² atoms/day per line (~0.2 g/day of diamond) | Product scale |

Two rules keep the plan from depending on APM-4:

1. **Spend atomic precision only on the site.** A site needs ~10³–10⁴ precisely placed atoms. Antenna,
   waveguides, collectors and wiring are 10 nm-class conventional nanofabrication.
2. **Make the site a molecule where possible.** Chemistry already produces 10²⁰ atomically identical
   objects per batch. Endohedral cages (D₂@C₆₀ has been made by organic synthesis), atom-precise metal
   clusters and hydride cluster compounds are the route to volume. Positional assembly is for
   prototypes and for what chemistry cannot make.

## Program metrics

| Metric | Meaning | Today | Battery needs |
|---|---|---|---|
| N_γ | photons spent per fusion event | 3 × 10⁶ (NIF), 5 × 10¹¹ (nanowires), ∞ (lattice) | ≤ 10⁵ |
| Λ | fusion rate per fuel pair at a site, s⁻¹ | ~10⁻⁶⁴ (D₂) | ≥ 10⁻¹⁵ volumetric; far higher if only hot spots are active |
| F-leverage | σ/Sₑ improvement over bulk cold fuel | × 2 (channeling) | × 72 (D-T), × 520 (p-¹¹B) |
| Q_site, Q_tile, Q_cell | energy out / energy in at each scale | ≤ 10⁻² | ≥ 1, then ≥ 3 with capture losses |
| n/W | neutrons per second per watt | 8.5 × 10¹¹ (D-D) | ≤ ~10⁴ for an unshielded consumer product (to be set with regulators) |

---

## Phase 0 — 2027: physics baseline, simulator v0, experiment design

**Needs:** no fabrication. 3–5 people, compute, ~$1–2 M (estimate).

Work:

1. **Simulator v0** (architecture in `design-notes.md` §7). Reproduce six published results before
   predicting anything new:
   - B1 bare cross sections and thick-target yields (done, `sim/baseline.py`);
   - B2 screening energies by host metal (Raiola, Kasagi, Huke) from time-dependent DFT;
   - B3 the 15 % electrochemical-loading effect (Thunderbird);
   - B4 the sub-keV plateau (Karahadian et al.) — or a quantified statement of what conventional
     physics cannot reproduce;
   - B5 the × 2 channeling anisotropy in Pd/D (Lebedev);
   - B6 NASA LCF neutron spectra and the Missouri tritium null.
2. **Requirements document:** for each track and fuel, the enhancement required per site, with error
   bars, generated from the simulator rather than typed in.
3. **Decide the Rider question for Track D** at 10–100 nm with 1–10 V/nm electrodes: a paper-study
   go/no-go.
4. **Design experiments E1–E6** to the level of count-rate budgets and systematics lists; secure beam
   time and partners (candidates: LBNL/UC Davis, UBC, Szczecin, NASA Glenn, Lebedev-type channeling
   expertise).
5. **CAD data model v0** and the NF-cell v0 parametric spec (started: `design/nf-cell-v0.yaml`).
6. Full-text reading queue from the literature review.

**Gate 0 (Dec 2027).** Pass if the simulator reproduces at least four of B1–B6 within stated
uncertainty and at least one experiment predicts a ≥ 10σ-detectable effect under the flagship
hypothesis and a clean null under conventional physics. If no experiment can discriminate, stop and
redesign before spending on hardware.

## Phase 1 — 2028–2029: discriminating experiments on engineered lattices

**Needs:** APM-0 plus bridging processes (MBE, ALD, ion implantation, e-beam and He-ion lithography,
HDL). 10–15 people, $5–10 M/yr (estimate), mostly beam time and detectors.

| # | Experiment | Tests | Decisive because |
|---|---|---|---|
| **E1** | D⁺ beam (1–20 keV) on PdD plasmonic nanoantenna arrays with a chopped laser; lock-in on charged-product yield | Light-driven transient screening (the Google/UMD patent claim) | Differential measurement: beam, target and geometry identical, only the light changes. ~1 % yield modulation should be detectable in about a day at 5 keV and 1 mA (estimate, to be budgeted properly) |
| **E2** | Uₑ and the sub-keV plateau versus designed defect density: epitaxial single-crystal, nanocrystalline and vacancy-engineered PdD, TiD₂, ErD₃ | Whether defects and loading cause the 2026 plateau | First experiment where the defect population is an input, not an unknown |
| **E3** | Two-laser THz difference-frequency drive of PdD at 8.3, 15.3, 20.4 THz, with neutron, charged-particle, gamma, ⁴He and calorimetric diagnostics; blinded frequency schedule | The Letts-Cravens-Hagelstein claim | Never replicated with nuclear diagnostics; cheap; a clean null is publishable |
| **E4** | σ/Sₑ leverage in designed channels and superlattices at 20–700 keV | How far channeling and flux peaking go beyond × 2 | Sets the ceiling for Track A |
| **E5** | Branching-ratio spectroscopy below 5 keV, including e⁺e⁻ pairs | Czerski threshold resonance | A neutron-poor D-D channel would change the product fuel |
| **E6** | Cage sites: D₂@C₆₀ and metallic fulleride crystals under Raman/THz pumping; neutron scattering for the D-D distribution | Simulator validation on an atom-exact driven site | Null expected; it calibrates the nuclear-quantum-dynamics code on a system with no unknown defects |

Alongside: build the event-resolved detector tile (diamond or SiC, one channel per ~100 µm pixel),
because every later phase depends on counting single MeV particles from a known site.

**Product off-ramp P1:** chip-scale D-D neutron/proton source using the Track A nano-ionizer and a
designed target (neutristor class) for calibration, well logging, medical isotopes research.

**Gate 1 (Dec 2029) — the main decision.**
- *Pass B:* any light-controlled or designed-structure-controlled change in a nuclear rate ≥ 2× at
  fixed beam conditions, or any beamless nuclear signal at 5σ, replicated in two laboratories.
  → Track B becomes the main line.
- *Fail B, pass A/D:* F-leverage ≥ × 5 demonstrated, or the Track D paper study survives.
  → Track B to the watch-list; program continues as A/D with products.
- *Fail all:* close the energy program; keep P1 and the metrology platform.

## Phase 2 — 2030–2031: first atomically precise reaction sites

**Needs:** APM-1 moving to APM-2 (fallback: site-as-molecule chemistry plus directed placement on
conventional nanofab). $20–40 M/yr (estimate).

- Build sites to atomic specification from the Phase 1 winner(s): chosen defect, exact fuel count,
  isotopically pure host, antenna gap set to ± 1 atom.
- Integrate the photon source on-chip (waveguide-fed nanolaser first, per-site single-photon emitters
  for the quantum-regime experiments).
- **Fusion microscopy:** every event attributed to a site and time-stamped against the optical drive.
  This turns rate-versus-design into a dataset of millions of sites per chip, i.e. combinatorial
  nuclear materials science.
- Simulator v1: closed-loop design — generate site variants, predict, fabricate arrays of variants on
  one chip, measure, refit.
- Fuel switch study: move the best mechanism from D-D to p-⁷Li and p-¹¹B hosts (LiH, borophane,
  h-¹¹BN) and measure what survives the higher Gamow barrier.

**Gate 2 (Dec 2031).** Pass if a single tile shows drive-correlated events with measured N_γ ≤ 10¹⁰
and a validated model path to ≤ 10⁵, or F-leverage ≥ × 10 (Track A/D). Kill the energy goal if the
best measured Q_site < 10⁻⁶ with no modelled path to 10⁻².

## Phase 3 — 2032–2033: proof-of-concept cell

**Needs:** APM-2/3. $40–80 M/yr (estimate).

- NF-cell v2 with fuel feed, helium venting, thermal path and first real capture stage.
- Capture down-select: direct charge collection, damage-tolerant wide-gap junctions, or thermal.
  Radiation-damage lifetime measured, not assumed.
- Aneutronic operation demonstrated at the tile level; neutron and gamma budget measured.
- Start regulatory engagement early (in the US, fusion devices sit under the NRC byproduct-material
  framework; a sealed consumer cell has no precedent and will need one).

**Gate 3 (Dec 2033).** Scientific gain Q_tile ≥ 0.1 (stretch: ≥ 1) for ≥ 1 hour with closed energy
accounting audited by an outside group. Below 10⁻³: stop scaling, publish, continue as a source and
instrument company.

**Product off-ramp P2:** designed-lattice alpha/proton micro-sources; nuclear-photonics crystals
(²²⁹Th-style nuclear clocks and sensors share the doping, cavity and detection stack).

## Phase 4 — 2034–2035: pilot manufacturing and reliability

**Needs:** APM-3; pilot line. $100 M+/yr (estimate).

- Tile → die → stack. 10⁹–10¹² sites/cm² per layer, layer pitch set by alpha range (~10–20 µm).
- Yield and defect tolerance: sites fail independently, so design for graceful degradation and per-tile
  disconnect.
- Lifetime: fuel burn-up is negligible (19 kWh per mg of p-¹¹B); life is set by helium accumulation,
  displacement damage in collectors and antenna drift. Target 1000 h, then 10 000 h.
- Battery prototypes at 1 mW, 100 mW, 1 W. Safety case: dose at contact, failure modes, shipping.

**Gate 4 (Dec 2035).** Engineering gain Q_cell ≥ 1 (electricity out over all electricity in) for
1000 h; dose within the limits agreed with the regulator; pilot-line yield ≥ 50 %.

## Phase 5 — 2036: mass-fabrication readiness

**Needs:** APM-4 or the site-as-molecule route at scale.

- Process transfer to a volume line; statistical process control on the site (the only
  atomically-critical step).
- Cost model in $/W and $/Wh-lifetime. Isotope supply is benign: ¹¹B is 80 % of natural boron, ⁷Li is
  92.5 % of natural lithium, deuterium is cheap.
- Product ladder: µW "install-and-forget" sensors → mW implants and IoT → W-class handhelds and
  drones → kW modules. Each rung is a 10³ scale-up in sites, not a new physics problem.

---

## Timeline

```
            2027   2028   2029   2030   2031   2032   2033   2034   2035   2036
Phase 0     ████ G0
Phase 1            ███████████ G1
Phase 2                          ███████████ G2
Phase 3                                        ███████████ G3
Phase 4                                                      ███████████ G4
Phase 5                                                                    ████
Simulator   v0──────v1 (closed loop)──────v2 (device)──────v3 (process/yield)
CAD         cell v0───site library───tile v1───cell v2───die/stack───product
Products                 P1 source───────P2 micro-sources/nuclear photonics────battery
APM need    0      0-1    0-1    1-2    2      2-3    3      3      3-4    4
```

## Top risks

| Risk | Consequence | Mitigation |
|---|---|---|
| The flagship physics is simply absent | Track B ends at Gate 1 | Gate is early and cheap; A/D and products continue |
| Systematics mimic an effect (fast neutrals, surface deuterium, contamination, calorimetry drift) | False positive, the 1989 failure mode | Differential/lock-in designs, nuclear diagnostics only, blinding, two-lab replication before any claim |
| Atomic fabrication arrives late | Phases 2–5 slip | Site-as-molecule chemistry; atomic precision only at the site |
| Neutrons or tritium in the product fuel cycle | Unsellable | Aneutronic fuels as the product baseline from Phase 2; D-D is a lab fuel |
| Capture stage destroyed by its own alphas | No electrical output | Capture is a Phase 3 gate item with measured damage rates |
| Reputational drag from "cold fusion" | Funding and partner loss | Publish nulls; claim only what replicates; lead with metrology |

## First 90 days

1. Full-text read of the seven-item reading queue; correct the literature review where abstracts misled.
2. Extend `sim/baseline.py` into a package: channeling reduction factors, thin-target/recirculation
   and confined-ion (Rider) models; grow the pinned regression suite in `sim/test_baseline.py`.
3. Stand up the atomistic toolchain on PdD: DFT relaxations of D at vacancies, phonon spectrum (check
   the 8/15/20 THz assignment), a first path-integral estimate of the D-D pair distribution at a
   vacancy.
4. Write the E1 count-rate and systematics budget properly and take it to a beam group.
5. Find the ARPA-E LENR outcomes — especially Stanford (deuterated nanoparticles under phonon
   stimulation) and Amphionic (nanogap potential wells), which overlap E3 and E1 — and contact the
   LBNL/UC Davis and UBC teams.
6. Freeze NF-cell v0 (a first 2D drawing is generated by `cad/render_cell.py`) and choose the 3D CAD
   kernel (design note DN-009).
