# Physics baseline: the numbers the nano-reactor has to beat

Every figure here is produced by the scripts in [`sim/`](../sim/) (outputs saved beside them as
`*-output.txt`) from published parametrisations. `baseline.py` reproduces the published check values (D-T 2.702e-2 b and D-D(p) 2.812e-4 b at 10 keV; p-11B 1.19 b at
600 keV; proton stopping in hydrogen 679 vs 683 MeV cm²/g at 1 MeV). Anything not computed there is
marked as an estimate.

The purpose is to turn "LENR regime" from a slogan into a set of quantitative targets. There are four
walls. A design is interesting to the degree it says which wall it attacks and by how many orders of
magnitude.

## Wall 1 — tunnelling: how far away is a quiet lattice?

| Quantity | Value | Source |
|---|---|---|
| D-D fusion rate in a free D₂ molecule (0.74 Å) | 3 × 10⁻⁶⁴ s⁻¹ per pair | Koonin & Nauenberg 1989 |
| Nearest D-D distance in β-PdD (octahedral sites) | ~2.85 Å — *further* apart than in D₂ | lattice constant 4.03–4.07 Å |
| Rate needed for a 100 µW/cm³ (betavoltaic-class) cell | 8 × 10⁻¹⁶ s⁻¹ per pair = 10⁴⁸ × D₂ | script |
| Rate needed for 1 W/cm³ | 8 × 10⁻¹² s⁻¹ per pair = 10⁵² × D₂ | script |
| Electron-mass enhancement that would close the gap | m* ≈ 5–10 mₑ | Koonin & Nauenberg 1989 |
| Muonic molecule (m = 207 mₑ), for scale | ~10¹² s⁻¹ (dtμ) | muon-catalysed fusion |

The two "rate needed" rows assume a fully dense crystal and count all the fusion energy. The v1
concept cell (a 1 µm film of sites per 20 µm layer, 20 % capture, light paid for) needs
2 × 10⁻¹¹ to 2 × 10⁻⁷ s⁻¹ per pair; those are the figures used further down.

Two consequences:

1. An equilibrium crystal is ruled out, and not merely by the numbers above: Leggett & Baym (1989)
   proved an upper bound on barrier penetration for any system **in equilibrium**. The bound says
   nothing about a driven system. That is the real job of the on-board photon sources: they are
   what makes the device non-equilibrium. A design in which the light is decoration has no route past
   Leggett-Baym.
2. The tunnelling exponent is brutally sensitive to anything that acts like a heavier electron or a
   shorter approach distance. A factor 5–10 in effective screening mass is the difference between
   nothing and a power source. This is why the screening anomalies in the literature (Wall 1 evidence,
   see the literature review) matter even though the absolute rates measured so far are tiny.

### What screening buys (standard energy-shift model)

Enhancement f = σ(E + Uₑ)/σ(E) for D-D, both branches:

| E_cm (keV) | bare σ (b) | Uₑ = 0.3 keV | Uₑ = 1 keV | Uₑ = 3 keV |
|---|---|---|---|---|
| 0.5 | 1.1e-17 | 6.8e3 | 4.7e7 | 1.4e11 |
| 1 | 2.5e-12 | 37 | 5.0e3 | 1.7e6 |
| 2 | 1.3e-8 | 3.9 | 39 | 1.4e3 |
| 5 | 1.8e-5 | 1.4 | 2.9 | 12 |
| 10 | 5.6e-4 | 1.1 | 1.5 | 2.6 |
| 50 | 3.2e-2 | 1.01 | 1.03 | 1.08 |

Screening of the size measured in metals (0.3–1 keV) is enormous in relative terms below 2 keV and
irrelevant above 10 keV. The measured sub-keV "plateau" (Karahadian et al. 2026, >10¹⁸ over bare) sits
exactly in the region where the bare cross section is so small that 10¹⁸ still leaves nothing usable.

### What a resting pair needs (first site-physics model)

[`sim/pair_fusion.py`](../sim/pair_fusion.py) solves the Schrödinger equation for two nuclei in a given
potential and returns the fusion rate Λ = A·|ψ(0)|². Checks: with the exact H₂ potential (Pachucki
2010) it gives the dissociation energies of D₂, HD and DT to 1 meV and a D₂ fusion rate of
2.0 × 10⁻⁶⁴ s⁻¹ (Koonin & Nauenberg: 3 × 10⁻⁶⁴); a free particle in a sphere comes out exact.

![What a resting fuel pair needs: fusion rate against screening length for D-D, p-6Li, p-7Li and p-11B](figures/pair-fusion-requirements.svg)

Values behind the chart: [`sim/pair-fusion-curves.csv`](../sim/pair-fusion-curves.csv).

**1. Where the pair sits matters as much as screening.** Two deuterons on neighbouring octahedral
sites of PdD, 285 pm apart, fuse at ~10⁻⁸⁸ s⁻¹ with molecule-like screening. That is 24 orders *below*
a free D₂ molecule, because the zero-point overlap of two separately confined nuclei costs ~10⁻³⁴
before the Coulomb barrier is counted. A useful site holds the pair in one cage. (Metzler et al. make
the same point: proximity is worth ~80 orders.)

**2. For deuterium, the requirement lands on the measured numbers.**

| Picture | To reach the v1 cell's tiers, 5 × 10⁻¹¹ to 5 × 10⁻⁷ s⁻¹ per pair |
|---|---|
| Heavier electron (Koonin-Nauenberg): the whole molecule shrinks | m* = 9–13; bond 8–6 pm; screening at contact 480–660 eV |
| Caged pair, screened Coulomb repulsion | screening length 1.5–1.0 pm; screening at contact 1.0–1.5 keV |
| Fixed 74 pm bond plus screening (Hagelstein et al., their Table 8) | 10⁻²² s⁻¹ at 300 eV, 10⁻²⁰ at 350 eV |
| **Reported for deuterium in metals (beam experiments)** | **0.2–0.4 keV in ultra-high vacuum; 0.4–1.0 keV elsewhere; 0.8–1.7 keV in the 2026 membrane work** |

The reported screening energies are the size a resting pair would need. That coincidence is what the
LENR-regime hypothesis rests on, and it is exactly where the doubt lies:

- A beam's screening energy is not known to apply to a pair at rest. Hagelstein et al. themselves note
  that free-electron screening "is much smaller at zero relative energy."
- The reported values may partly be artifacts of deuterium density profiles and surface layers (Huke
  et al.), and the plateau data have an unresolved fast-neutral question.
- A free-electron gas cannot do it. The Thomas-Fermi length in palladium's electron gas is ~40 pm;
  reaching 2 pm would take ~10⁷–10⁸ times the electron density.

**3. For the product fuels, it does not.**

| Fuel | Screening length needed, sensor → handheld tier | Screening at contact | Largest reported |
|---|---|---|---|
| D–D | 1.5 → 1.0 pm | 1.0 → 1.5 keV | 0.3–1.7 keV |
| p–⁶Li | 0.65 → 0.43 pm | 6.7 → 10 keV | 0.4–1.2 keV (lithium in metals) |
| p–⁷Li | 0.57 → 0.37 pm | 7.6 → 12 keV | 0.4–1.2 keV |
| p–¹¹B | 0.43 → 0.30 pm | 17 → 24 keV | ~0.4 keV |

For scale, an electron's orbit is 52.9 pm and a muon's is 0.256 pm. Lithium and boron need
sub-picometre screening, within a factor of 1.2–2.5 of a muon's orbit and an order of magnitude beyond
anything reported for them. In the bound-pair regime the aneutronic fuels are muon-class hard, and
muons themselves do not help because they bind to the heavier nucleus.

Consequences for the plan: deuterium is the only fuel with which the lattice hypothesis can be tested
or first demonstrated; p-¹¹B belongs to the beam and collider tracks, where it is the best aneutronic
fuel (F = 1.9 × 10⁻³ cold, 1.6 electron-free); and lithium is the least-bad aneutronic lattice fuel.
Natural lithium behaves as a p-⁶Li fuel at low energy: ⁶Li is 7.5 % of the atoms but has 60 times the
S-factor, so it takes ~83 % of the reactions.

## Wall 2 — stopping: why firing ions into cold matter cannot break even

An ion moving through matter loses energy to electrons at a rate set by the stopping cross section Sₑ,
and fuses at a rate set by σ. Their ratio, times the energy per reaction, is a dimensionless figure of
merit:

    F(E) = σ(E) · E_fus / Sₑ(E)

F is the fusion energy released per unit of beam energy dissipated. For a thin target of areal density
N with the unburnt beam decelerated and recovered at efficiency η, the gain is

    Q = F / [1 + (1 − η)·E_beam / (Sₑ·N)]  ≤  F

so **no amount of beam-energy recovery lifts the gain above F**. Recirculation, energy-recovery linacs
and one-atom-thick targets all converge on F from below. F is a property of the fuel and the medium.

| Beam → target | F_max | at beam energy | σ/Sₑ improvement needed for F = 1 |
|---|---|---|---|
| D → T | 1.4 × 10⁻² | 108 keV | × 72 |
| p → ¹¹B | 1.9 × 10⁻³ | 653 keV | × 520 |
| D → D | 0.5–1.2 × 10⁻³ | 1.7–5 MeV (still rising slowly) | × 800–2000 |

Thick-target gains (ion stops completely in pure fuel) are lower still: D→T 0.8 % at 200 keV, p→¹¹B
0.06 % at 0.7–1.5 MeV, D→D 2 × 10⁻⁵ at 200 keV. A 1 keV screening energy changes the 100–200 keV
numbers by under 5 %.

So the question for any beam-into-lattice architecture is: **can an engineered crystal change σ/Sₑ by
10²–10³·⁵ at 100–700 keV?** Known levers, with honest sizes:

| Lever | Size | Status |
|---|---|---|
| Channeling (ions steered down low-electron-density channels) | Sₑ ÷ 2–10 for the well-channeled fraction | established ion-beam physics |
| Flux peaking (channeled flux concentrated on interstitial fuel) | yield × ~2 observed | Lebedev HELIS, Pd/D |
| Screening | × 1.0–1.1 at these energies | established, irrelevant here |
| Resonances (p-¹¹B 148 keV, 600 keV; D-T 64 keV) | already inside F | — |
| Electron-free reaction zone (bare ions held by fields) | Sₑ → ion-ion Coulomb stopping, ÷ 600–1100 (computed) | known physics, unbuilt at nanoscale |

The last row is the only known-physics lever of the right size. Ion-on-ion Coulomb stopping is smaller
than electronic stopping by roughly Z·mₑ/M per target atom times a ratio of Coulomb logarithms —
about 10⁻³. With a 10 nm cut-off the script gives **F ≈ 8 for D-T** at 108 keV, **1.6 for p-¹¹B** at
653 keV and 0.1–0.7 for D-D at 0.5–2 MeV. This is the idealised ceiling: it counts only energy handed
to target ions and ignores what it costs to keep the ions confined and non-thermal. The catch is
Rider's result (MIT thesis 1995, linked in the Notes doc): keeping
ions non-thermal against their own elastic scattering costs recirculating power that tends to exceed
fusion power. Whether atomically precise electrodes at ~1–10 V/nm change the terms of that argument is
an open, answerable modelling question.

### The beam route for p-¹¹B, in numbers

From [`sim/beam_route.py`](../sim/beam_route.py):

| Case | Fusion energy out ÷ beam energy spent |
|---|---|
| Proton into solid boron | 0.002 |
| Proton held at the 653 keV resonance among bare boron nuclei | 1.6 (10 nm trap), 1.2 (1 µm trap) |
| Proton injected at 0.7–3.5 MeV and left to slow down on bare boron | 0.5–0.7 |

Even with every electron removed and nothing lost, the scheme is at about break-even once conversion
losses are counted. It can only do better if the boron is hot too, which means confining an ion cloud
rather than passing a beam through a target.

The obstacle is one ratio. Over the distance in which a proton has one chance to fuse, Coulomb
collisions with boron nuclei deflect it by ~90–120 rad² in total and hand over 8 times its energy: its
direction is randomised about a hundred times per fusion. A beam cannot stay a beam. So:

- a trap that keeps only protons inside a cone of 0.1, 0.3 or 1 rad must recover 99.9 %, 99.1 % or
  90 % of the energy of every proton it loses, just to break even;
- put the other way, break-even needs each proton held for about **ten** direction-randomising
  collisions if lost ions dump their energy as heat, or about **one** if 90 % of it is recovered.
  Magnetic-mirror loss cones give two or three.

What the small scale adds is field strength. At 1–5 V/nm a 650 kV well fits in 130–650 nm and can hold
10¹⁷–10¹⁸ charges per cm³, about a million times a magnetic trap's limit, so a proton would fuse every
4–90 ms and power density is not the constraint. The megavolt well is also, by construction, a direct
converter for the alphas. What it does not change is the hundred-to-one ratio, or Earnshaw's theorem:
every static electrostatic trap has a hole in phase space, and the design question is whether ions
leaving through it arrive slow (climbing to a retarding electrode, energy recovered for free) or fast
(falling into an attracting one, energy lost).

## Wall 3 — branching and radiation: what comes out

| Reaction | Energy | Products | Note |
|---|---|---|---|
| D + D | 3.27 / 4.03 MeV | n + ³He / p + T (≈ 50/50) | 8.5 × 10⁵ n/s per µW; 8.5 × 10¹¹ n/s per W |
| D + D → ⁴He | 23.85 MeV | γ (10⁻⁷ branch conventionally) | the "LENR channel"; heat only if real |
| D + T | 17.6 MeV | n (14.1 MeV) + α | 80 % of energy in neutrons |
| p + ¹¹B | 8.68 MeV | 3 α | aneutronic to ~10⁻³; B_G = 150 keV^½ |
| p + ⁷Li | 17.3 MeV | 2 α | aneutronic below 1.88 MeV; B_G = 88 keV^½ |
| D + ⁶Li | 22.4 MeV | 2 α | D-D side reactions give neutrons |

A watt of conventional D-D fusion is a ~10¹² n/s neutron source and breeds tritium. A consumer battery
cannot be D-D unless the anomalous ⁴He channel is real and dominant, which is unproven. The product
fuel is therefore p-¹¹B or p-⁷Li; D-D is the *laboratory* fuel because its neutrons and 3 MeV protons
make single events easy to count.

Fuel is never the constraint: p-¹¹B releases 7 × 10¹³ J/kg, i.e. **19 kWh per milligram**. A
nano-fusion battery is power-limited and lifetime-limited, not energy-limited. Helium is the ash:
1 W of p-¹¹B makes 2.5 cm³ (STP) of helium per year, which must be vented.

## Wall 4 — capture: getting electricity out

- Alpha range at ~3 MeV is ~6–12 µm in diamond/silicon. That length, not the site size, sets the
  vertical pitch of a stack.
- Semiconductor junction converters (alpha-/betavoltaics) are single-digit-percent efficient in practice
  and are damaged by MeV ions; at W/cm² alpha fluxes a conventional junction lasts minutes. Capture
  needs either damage-tolerant direct charge collection or a thermal route (thermoelectric,
  thermophotovoltaic — the 40 % TPV result in the Notes doc needs ~2000 °C, which a nano-cell will not
  reach).
- The Rydberg-array "force field" idea in the main doc does not apply to MeV products: Rydberg
  transitions live at µeV–meV scales and have no meaningful cross section for MeV photons or ions.
  It is retired here (design note DN-014); charged-particle capture is the working assumption.

## What a photon can and cannot do

| Fact | Number |
|---|---|
| Photon energy available on-chip | 1–3 eV |
| One-photon field, photonic-crystal cavity ((λ/n)³) | 1 × 10⁻⁴ V/nm |
| One-photon field, plasmonic nanogap (40 nm³) | 0.7 V/nm |
| One-photon field, picocavity (1 nm³) | 4 V/nm |
| Coulomb field between two deuterons at 100 pm / 10 pm | 144 / 14 000 V/nm |
| Laser intensity at which theory predicts × 10³ tunnelling boost at 1 keV | 10²⁰ W/cm² (Qi, Zhou, Wang) |
| Photons per fusion, NIF Dec 2022 shot (2.05 MJ in, 3.15 MJ out) | 3 × 10⁶ |
| Photons per fusion, deuterated nanowire arrays | ~5 × 10¹¹ |
| Photons per fusion allowed at break-even (30 % emitter, p-¹¹B) | ≤ ~10⁶ (≤ ~10⁵ with realistic capture) |

Reading of the table:

- A single photon squeezed into a picocavity produces a field of volts per nanometre. That is a
  chemically large field, a few per cent of the inter-nuclear field at bond distances, and it acts on
  electrons, not on nuclei (the deuteron's quiver energy in that field is ~10⁻⁵ eV).
- Light therefore reaches the nucleus **through electrons** (plasmon-driven transient screening),
  **through the lattice** (resonant phonon pumping), or, for unlike pairs only, through the pair's own
  dipole (next section). None has a confirmed nuclear effect yet. A free-electron estimate of the first:
  screening energy scales as density^(1/6), so a 2 % density swing in the surface layer of a gap at
  1 V/nm moves a ~500 eV screening energy by ~2 eV, in one atomic layer.
- The program metric is **photons per fusion, N_γ**. The 2014 doc's own arithmetic (10⁵ one-eV photons
  per 500 keV proton) lands on the same number from the other direction. Track B succeeds if
  N_γ ≤ 10⁵; today's best photon-driven nanostructure result is six orders away, and it gets there by
  brute-force relativistic heating, not by lattice physics.
- A laser-driven accelerator for slow ions needs a structure period of βλ: 6.5 nm for 10 keV D⁺,
  21 nm for 100 keV D⁺, 72 nm for 600 keV protons (λ = 2 µm), with the accelerating near-field
  decaying within 1–11 nm of the surface. That is beyond conventional lithography and squarely an
  atomically-precise-fabrication structure. It is the concrete form of the 2014 "group the photons
  onto protons" idea.

### Light pushes unlike pairs, not like pairs

A uniform field drives the *relative* motion of two nuclei with an effective charge
(Z₁m₂ − Z₂m₁)/(m₁ + m₂):

| Pair | D–D | D–T | p–⁶Li | p–⁷Li | p–¹¹B |
|---|---|---|---|---|---|
| q_eff / e | 0 | 0.20 | 0.43 | 0.50 | 0.50 |

Light cannot push one deuteron against another at all (Queisser & Schützhold make the same point for
X-ray-assisted tunnelling). It does couple to p–Li and p–B, and lithium hydride's lattice vibrations
are infrared-active. If light is ever to act on the pair directly, the product fuels are the ones it
can act on.

### A held field cannot pay for itself

[`sim/cell_model.py`](../sim/cell_model.py), with 20 % capture, a 30 % laser and 50 % distribution:

| Holding one site at | costs | and needs, while lit |
|---|---|---|
| 1 V/nm in a plasmonic gap (40 nm³, Q ≈ 10) | 0.1 mW | 3 × 10⁹ fusions per second |
| 1 V/nm in a dielectric cavity (Q = 10⁶) | 3 nW | 8 × 10⁴ per second |
| 0.01 V/nm in the same cavity | 0.3 pW | 8 per second |

A 1 W/cm³ cell has 3 × 10⁻²¹ W of light to spend per fuel pair. Continuous optical excitation is
therefore 8–16 orders of magnitude too expensive at any rate a battery would run at. What light can
still be:

- a **writer** of long-lived active states. One photon per write breaks even only if
  (rate) × (lifetime of the written state) ≥ 1/N_γ ≈ 10⁻⁵, e.g. nine days at 10⁻¹¹ s⁻¹;
- a **trigger or control signal** at low duty;
- a **probe**, as in experiment E1;
- the **energy carrier of an accelerator**, where the stopping ceiling applies instead.

The same accounting applies to any drive. The acoustic drive in the Hagelstein model dissipates 1 W
for 10⁹ fusions per second, which is ~4 mW (our arithmetic from their numbers; the authors say the
coefficient of performance "will be poor").

## Summary of targets

| Track | Wall attacked | Required | Best evidence today |
|---|---|---|---|
| B — driven lattice site (flagship hypothesis) | 1 | caged pair with ~1–1.5 pm screening for D-D (0.3–0.6 pm for Li, B); drive cost below 3 × 10⁻²¹ W per pair | beam screening of 0.3–1.7 keV in metals, not shown for a pair at rest; no light-driven nuclear effect confirmed |
| A — screened lattice + nano-accelerator | 1, 2 | σ/Sₑ × 72 (D-T), × 520 (p-¹¹B), × 800–2000 (D-D) | channeling × 2–10, screening negligible at these energies |
| D — electron-free nano-collider | 2 | power to keep ions confined and non-thermal < fusion power | ideal-case F ≈ 8 (D-T), 1.6 (p-¹¹B) computed; nothing built |
| C — muon-catalysed nano-cell | 1 | ≥ ~500–1000 fusions per muon at today's ~5 GeV per muon, or much cheaper muons | ~150 fusions per muon |
