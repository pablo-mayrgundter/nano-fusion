# Worked example: from one D₂ molecule to a battery tile

The whole argument in nine steps, each a number you can reproduce. Run the four scripts at the bottom
and every figure on this page reappears.

## 1. One molecule, as nature made it

Two deuterons bound in a D₂ molecule sit 74 pm apart behind a Coulomb barrier. Quantum mechanics lets
them tunnel through it, very rarely. `sim/pair_fusion.py` solves that problem with the exact molecular
potential:

    D2   binding energy 4.556 eV (measured 4.556)    fusion rate 2.0e-64 per second

The binding energy is the check that the potential and the solver are right; the published rate
(Koonin & Nauenberg 1989) is 3 × 10⁻⁶⁴. A kilogram of deuterium gas would produce one fusion every
10³⁰ years.

## 2. How far is that from useful?

`sim/cell_model.py` works backwards from a battery. For the smallest useful product, a
100 µW/cm³ "install and forget" sensor cell, each fuel pair must fuse about 5 × 10⁻¹¹ times per
second. The gap is **53 orders of magnitude**.

## 3. What controls the rate

Almost entirely one thing: how well the electrons around the pair cancel its repulsion at short
range. The rate is exponential in that screening.

![Fusion rate against screening length for four fuels](figures/pair-fusion-requirements.svg)

Reading the D–D curve: in a molecule the effective screening length is ~22 pm. Shrink it to 1.5 pm
and the rate rises 53 orders, into the band a battery needs. A second way to say the same thing is
Koonin and Nauenberg's thought experiment of a heavier electron:

| Electron mass | Bond length | Fusion rate per second |
|---|---|---|
| 1 (real) | 74 pm | 10⁻⁶⁴ |
| 5 | 15 pm | 10⁻²⁰ |
| 10 | 7 pm | 10⁻⁹ |
| 207 (a muon) | 0.36 pm | 10¹² |

The last row is real: it is muon-catalysed fusion. Everything in this project lives between rows one
and three.

## 4. Does anything measured come close?

Yes, on paper. When deuterons are fired into metals at a few keV, they fuse more often than bare
nuclei would, as if the metal handed them an extra 0.3–1.7 keV. A pair at rest that enjoyed the same
screening would need ~1.0–1.5 keV (caged-pair model) or ~0.5–0.65 keV (heavier-electron model). The
measured and the required numbers overlap.

That overlap is the entire case for the lattice route. It is also unproven in three ways: nobody has
shown the beam number applies to a pair at rest; the measurements have known artifacts; and an
ordinary electron gas cannot screen that tightly (palladium's manages ~40 pm).

## 5. Where the pair must sit

The same solver, with two deuterons on neighbouring sites of a palladium-deuteride lattice (285 pm
apart, each in its own well):

    10^-88 per second with molecule-like screening

That is 24 orders worse than the free molecule. Loading deuterium into a metal moves the nuclei
apart. A useful site has to hold the pair in one cage: a vacancy, an endohedral molecule. The first
atom-exact model of such a site is `design/sites/S1-PdD-vacancy.xyz`.

## 6. Change the fuel

Deuterium fusion makes neutrons, so the product fuels are p-¹¹B and p-⁷Li. Their nuclei carry more
charge, and the barrier grows with it:

| Fuel | Screening length needed | For scale |
|---|---|---|
| D–D | 1.5 → 1.0 pm | measured beam values correspond to ~1–5 pm |
| p–⁷Li | 0.57 → 0.37 pm | |
| p–¹¹B | 0.43 → 0.30 pm | a muon's orbit is 0.26 pm |

For lithium and boron the lattice route needs nearly what a muon provides, and ten times more than
has been reported for them. So deuterium is the fuel for finding out whether the physics exists, and
p-¹¹B is better matched to schemes that give the proton real kinetic energy.

## 7. Build the cell around it

Suppose a site did work. The concept cell (`design/nf-cell-v1.yaml`) is a 1 µm film of site crystal,
one caged pair per cubic nanometre, on a 20 µm collector, repeated 500 times per centimetre.

| | Sensor | Implant | Handheld |
|---|---|---|---|
| Net electrical power, W/cm³ | 10⁻⁴ | 10⁻² | 1 |
| Fusions per pair per second (p-¹¹B) | 2 × 10⁻¹¹ | 2 × 10⁻⁹ | 2 × 10⁻⁷ |
| Light per fuel pair, W | 3 × 10⁻²⁵ | 3 × 10⁻²³ | 3 × 10⁻²¹ |
| Stack served by one 1 mW laser | 67 cm³ | 0.67 cm³ | 0.007 cm³ |
| Fuel film lasts without new boron | 1500 years | 15 years | 2 months |
| Helium to vent, cm³ per cm³ per year | 0.002 | 0.2 | 19 |
| Junction collector survives | 1 year | 4 days | 1 hour |
| Thickest sheet that cools passively | no limit | 12 mm | 0.12 mm |

Two things stand out. One ordinary laser diode would run a whole watt-class cell, so "many reactors
per laser" is easy: the unit below has 625 tiles and 39 million pixels on one laser die. And only the
sensor tier is gentle on everything else, which makes it the natural first product.

![One laser die feeding a field of site-crystal tiles](../design/step/nf-cell-v1-laser-unit.svg)

## 8. What the light can and cannot do

A watt-class cell has 3 × 10⁻²¹ W of light to spend on each fuel pair. Holding one site in a strong
optical field costs vastly more:

| Field held at one site | Power | Fusions per second needed to pay for it |
|---|---|---|
| 1 V/nm, plasmonic gap | 0.1 mW | 3 × 10⁹ |
| 1 V/nm, low-loss cavity | 3 nW | 8 × 10⁴ |

So light cannot be what *sustains* the reaction. It can switch a site into an active state that then
persists (at 10⁻¹¹ fusions per second the state must last nine days per photon), it can trigger, and
it can probe. One more fact favours your fuels here: a field pushes a proton against lithium or boron
(effective charge 0.5 e) but cannot push one deuteron against another at all.

## 9. What the first experiment would see

Experiment E1 fires keV deuterons at palladium nano-antennas and chops a laser on and off
(`sim/e1_budget.py`). A dense-gap target resolves a 0.5 % change in fusion yield in a day, equivalent
to a 2 eV change in screening. Known physics predicts about that much in a single atomic layer, which
is to say nothing detectable. Any light-on/light-off difference would be new physics, cheaply found.

![The laboratory cell: four antennas on the stack](../design/step/nf-cell-v0-pixel-block.svg)

## What would change the picture

1. A low-energy plateau measured with a beam shown to be free of fast neutrals.
2. A first-principles screening length at a designed vacancy site that comes out below ~5 pm.
3. Any reproducible light-on/light-off difference in E1.
4. Proton-on-lithium screening above ~5 keV in any designed host.

## Reproduce

```bash
python3 sim/pair_fusion.py
```

```bash
python3 sim/cell_model.py
```

```bash
python3 sim/e1_budget.py
```

```bash
python3 sim/plot_pair_fusion.py
```
