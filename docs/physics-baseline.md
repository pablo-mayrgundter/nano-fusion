# Physics baseline: the numbers the nano-reactor has to beat

Every figure here is produced by [`sim/baseline.py`](../sim/baseline.py) (output saved in
[`sim/baseline-output.txt`](../sim/baseline-output.txt)) from published parametrisations, and the script
reproduces the published check values (D-T 2.702e-2 b and D-D(p) 2.812e-4 b at 10 keV; p-11B 1.19 b at
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
| Photons per fusion, NIF Dec 2022 shot | 3 × 10⁶ |
| Photons per fusion, deuterated nanowire arrays | ~5 × 10¹¹ |
| Photons per fusion allowed at break-even (30 % emitter, p-¹¹B) | ≤ ~10⁶ (≤ ~10⁵ with realistic capture) |

Reading of the table:

- A single photon squeezed into a picocavity produces a field of volts per nanometre. That is a
  chemically large field, a few per cent of the inter-nuclear field at bond distances, and it acts on
  electrons, not on nuclei (the deuteron's quiver energy in that field is ~10⁻⁵ eV).
- Light therefore reaches the nucleus only **through electrons** (plasmon-driven transient screening)
  or **through the lattice** (resonant phonon pumping). Those are the two photon channels the
  literature offers, and neither has a confirmed nuclear effect yet.
- The program metric is **photons per fusion, N_γ**. The 2014 doc's own arithmetic (10⁵ one-eV photons
  per 500 keV proton) lands on the same number from the other direction. Track B succeeds if
  N_γ ≤ 10⁵; today's best photon-driven nanostructure result is six orders away, and it gets there by
  brute-force relativistic heating, not by lattice physics.
- A laser-driven accelerator for slow ions needs a structure period of βλ: 6.5 nm for 10 keV D⁺,
  21 nm for 100 keV D⁺, 72 nm for 600 keV protons (λ = 2 µm), with the accelerating near-field
  decaying within 1–11 nm of the surface. That is beyond conventional lithography and squarely an
  atomically-precise-fabrication structure. It is the concrete form of the 2014 "group the photons
  onto protons" idea.

## Summary of targets

| Track | Wall attacked | Required | Best evidence today |
|---|---|---|---|
| B — driven coherent lattice (flagship hypothesis) | 1 | ≥ 10⁴⁸ over D₂ rate; N_γ ≤ 10⁵ | 10¹⁸ over bare at sub-keV; no light-driven nuclear effect confirmed |
| A — screened lattice + nano-accelerator | 1, 2 | σ/Sₑ × 72 (D-T), × 520 (p-¹¹B), × 800–2000 (D-D) | channeling × 2–10, screening negligible at these energies |
| D — electron-free nano-collider | 2 | power to keep ions confined and non-thermal < fusion power | ideal-case F ≈ 8 (D-T), 1.6 (p-¹¹B) computed; nothing built |
| C — muon-catalysed nano-cell | 1 | ≥ ~500–1000 fusions per muon at today's ~5 GeV per muon, or much cheaper muons | ~150 fusions per muon |
