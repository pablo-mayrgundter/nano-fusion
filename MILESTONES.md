# Milestones

## M1 — Physics baseline and first simulator

**2026-11-20 · tag `m1` · [site](https://pablo-mayrgundter.github.io/nano-fusion/) · [one-pager](https://pablo-mayrgundter.github.io/nano-fusion/onepager.html)**

The first pass at turning the NanoFusion idea into numbers: what a nano-scale fusion battery would
need from its reaction sites, which routes the physics closes, and a gate-driven plan for finding out
about the rest. Modelling and published data only. No hardware, no experimental results of our own.

### What is in it

| Area | Delivered |
|---|---|
| Physics | [`docs/physics-baseline.md`](docs/physics-baseline.md): the four walls (tunnelling, stopping, radiation, capture) as quantitative targets; [`docs/worked-example.md`](docs/worked-example.md): the argument in nine reproducible steps |
| Evidence | [`docs/literature-review.md`](docs/literature-review.md): fifteen papers read in full, each claim graded by how closely its source was read |
| Simulator | [`sim/pair_fusion.py`](sim/pair_fusion.py) (fusion rate of a resting pair), [`sim/baseline.py`](sim/baseline.py) (beams and stopping), [`sim/beam_route.py`](sim/beam_route.py), [`sim/cue_ball.py`](sim/cue_ball.py), [`sim/cell_model.py`](sim/cell_model.py), [`sim/e1_budget.py`](sim/e1_budget.py); 21 regression tests; saved outputs beside each script |
| Device | [`design/nf-cell-v0.yaml`](design/nf-cell-v0.yaml) (laboratory cell) and [`design/nf-cell-v1.yaml`](design/nf-cell-v1.yaml) (product concept, shared laser units) |
| CAD | [`cad/build_step.py`](cad/build_step.py): STEP assemblies generated from the specs, tried in Bldrs Share, with viewer findings in [`design/step/README.md`](design/step/README.md) |
| Plan | [`docs/roadmap-10yr.md`](docs/roadmap-10yr.md): 2027–2036 in six phases, seven experiments, five gates and the off-ramps |
| Site | [`index.html`](index.html) and [`onepager.html`](onepager.html), built by [`site/build.py`](site/build.py), which checks every number on the pages against the saved simulator outputs |

### What it found

1. A battery is a per-pair rate problem. A deuterium pair in a molecule fuses at 2 × 10⁻⁶⁴ per second
   (published: 3 × 10⁻⁶⁴); a battery needs 10⁻¹¹ to 10⁻⁷. The 53 orders between them are set almost
   entirely by the electron screening length: about 22 pm in a molecule, 1 to 1.5 pm needed.
2. Deuterons fired into metals behave as if screened by 0.3–1.7 keV, which is the strength a resting
   deuterium pair would need. Whether it applies to a pair at rest is the open question.
3. The clean fuels need 0.3–0.6 pm, close to a muon's orbit and about ten times beyond anything
   reported for them. Deuterium is the fuel for proving the physics; p-¹¹B and p-⁷Li suit the routes
   that give the proton real kinetic energy.
4. Light cannot knock, pump or hold: a held optical field costs 8 to 16 orders of magnitude more than
   a site can repay. Within a budget of about 43,000 photons per fusion it could still write, trigger
   and probe. No nuclear effect of low-power light has been confirmed.
5. A beam into cold matter returns 0.1–1 % of its energy; into solid boron, 0.19 %. Among bare nuclei
   the ceiling is 1.2–1.6 on paper, if a beam that scatters a hundred times per fusion can be recycled.
6. A perfectly aimed single shot hits about once in a million: the target nucleus's zero-point jitter
   is 670 times the size of the pocket. Aiming is not the limit.

### What it did not do

- No atomistic calculation of a real site. Rates come from model potentials (screened Coulomb,
  harmonic wells), benchmarked on molecules.
- No independent check of the screening energies taken from beam experiments.
- No treatment of how a non-equilibrium drive would act on a site, beyond its energy cost.
- No engineering of the capture stage beyond an assumed efficiency and damage limit.

### Next, toward Gate 0 (December 2027)

1. A first computed rate for a real site: deuterium at a palladium vacancy, with relaxed geometry and
   electron density fed into `sim/pair_fusion.py` in place of its model potentials.
2. The go/no-go paper study for the electron-free collider at 10–100 nm.
3. The count-rate and systematics budget for experiment E1, taken to a beam group.
4. The remaining simulator benchmarks (screening by host metal, the sub-keV plateau, channeling).
