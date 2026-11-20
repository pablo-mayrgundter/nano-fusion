# Literature review: synthetic crystals, the LENR regime, and photon-energized reaction sites

First compiled 2026-11-20 from web searches; revised the same day after arXiv access was added, when
fifteen papers were read in full text (the 150-page Hagelstein paper: main text and selected appendices).

How to read the marks:

- **✔✔** read in full text this session (arXiv version) by reader agents whose quotes were machine-checked
  against the source file; the passages that changed a conclusion were re-checked by hand. Numbers come
  from the paper itself.
- **✔** confirmed against an abstract, journal listing or institutional page only.
- **◦** from memory; check before quoting externally.

The full-text reading changed several entries. The most important corrections are listed at the end
under "What changed on full reading."

**Bottom line.** A metal lattice changes low-energy D-D fusion rates by large factors, two groups now
see the yield stop falling below ~2–3 keV, and an electrical knob on the lattice moves the rate. None
of it is near useful power, the systematics of the lowest-energy points are not closed, and no
experiment has confirmed that low-intensity light changes a nuclear rate. All of this evidence is for
deuterium. For the product fuels (p-¹¹B, p-⁷Li) the reported lattice effects are far smaller relative
to what would be needed (see `physics-baseline.md`, "What a resting pair needs").

---

## Tier 1 — established or mainstream-published experimental results

### 1.1 The lattice changes the D-D fusion rate

| Result | Reference | What it shows, and its limits |
|---|---|---|
| Screening energies of hundreds of eV in deuterated metals, tens of eV in insulators | ✔✔ Huke, Czerski et al., [arXiv:0805.4538](https://arxiv.org/abs/0805.4538) (*Phys. Rev. C* 78, 015803 ◦), reviewing all groups | Their own ultra-high-vacuum values: Ta 322 ± 15, Zr 297 ± 8, Pd 313 ± 2, Al 190 ± 15 eV, called lower limits. Others: 602 ± 23 eV (Tohoku, Au/Pd/PdO), Pt 440 → 670 eV and Re 700 → 230 eV on re-measurement (Bochum), insulators < 50 eV. Theory (electron polarisation plus lattice cohesion) gives ~50–140 eV, so experiment is about twice theory. **Warnings from the same paper:** a deuterium density profile that changes with beam energy imitates screening in total-yield analyses; a 15 nm surface layer removes the effect; the Debye-plasma explanation is "clearly excluded" |
| Uₑ = 1000 ± 250 eV in Pd under pulsed glow discharge | ✔✔ Schenkel et al., *J. Appl. Phys.* 126, 203302 (2019), [arXiv:1905.03400](https://arxiv.org/abs/1905.03400) | One palladium wire, neutrons only, yields relative to the 12.6 kV point. Ion species and energies were simulated, not measured; the surface carried 30 at% carbon and 20 at% oxygen; the authors say ~1000 eV "is not consistent with established theories" |
| Electrochemical loading of a Pd target raises the D-D rate by 15(2) % | ✔ Chen et al., *Nature* 644, 640–645 (2025) ("Thunderbird", UBC) | A chemical/electrical knob on the lattice moves a nuclear rate. No net energy |
| **Yield plateau below ~2.5 keV (centre of mass) in Pd, PdD, Ti, TiD; measured/bare yield "approaches or exceeds 10¹⁸" at 0.25 keV** | ✔✔ Karahadian, Colborne, Persaud, Schenkel, Munday, [arXiv:2512.06212](https://arxiv.org/abs/2512.06212); *Nature Communications*, July 2026 ✔ | Same membrane geometry as Thunderbird (beam on one face, electrolyte on the other). Fits above the plateau: Pd 0.8 ± 0.2 keV rising to 1.7 ± 0.2 keV with electrochemical loading; Ti 0.3 ± 0.2 → 0.9 ± 0.2 keV. **Limits:** yields are relative, normalised at 6.5 keV, so 10¹⁸ means the 0.25 keV yield is roughly 0.2–5 % of the 6.5 keV yield; the plateau rests on silicon-detector proton counts with statistical errors only; the arXiv text never mentions energetic neutrals or molecular ions (its Methods section is not in the file). Authors: "many orders of magnitude below energy-production thresholds" |
| The same plateau, independently: Zr below 3 keV, Ti below 2 keV, Pd below 6 keV, plus a shift of the proton line | ✔✔ Czerski et al., [arXiv:2409.02112](https://arxiv.org/abs/2409.02112) | Fitted screening: Zr 340 ± 30, Pd 400 ± 40, Ti 25 ± 10 eV. **Limits:** fewer than 40 events per low-energy point from week-long runs; the authors themselves assign their D₂⁺ plateau to un-decelerated fast neutrals and rest the claim on D₃⁺ data, on Pd, and on the line shift. "Thermal fusion in ion tracks" is their model, not an observation. They note the US plateau "agrees with our data" for Pd |
| Yield anisotropy × 2 for 20 keV D⁺ along crystal planes of deuterated Pd | ✔ Dalkarov, Bagulya et al., *J. Surf. Investig.* (2020) [doi](https://www.doi.org/10.1134/S102745102002024X) | Crystal order matters (channeling, flux peaking) |

Why this matters for synthetic crystals: every effect above depends on defect population, loading
ratio, surface state and crystal order, which conventional metallurgy controls poorly. The two
plateau papers and the screening review all point at sample state as the uncontrolled variable. A
lattice built to specification, measured with a beam that is demonstrably free of fast neutrals, is the
experiment that has not been done.

### 1.2 Lattice confinement fusion (NASA Glenn)

- ✔ Steinetz et al., *Phys. Rev. C* 101, 044610 (2020); ✔ Pines et al., *Phys. Rev. C* 101, 044609
  (2020). ErD₃ and TiD₂ under 2.9 MeV bremsstrahlung; neutrons at ~4 and ~5 MeV reported.
- **Replication status is split.** ✔✔ Duncan et al., [arXiv:2308.01434](https://arxiv.org/abs/2308.01434):
  TiD₂ in a 90 % thermal reactor spectrum gave (5.4 ± 0.4) × 10¹² tritium atoms against 3.9 × 10¹²
  simulated (±25 %), "an unsuccessful first attempt to replicate." ✔✔ Gillespie et al.,
  [arXiv:2508.18243](https://arxiv.org/abs/2508.18243): the same group's cyclotron-vault run, with
  energetic neutrons only, gave tritium "2.9–5.1 times higher than predicted," which they present as
  "increasing the credibility in the results from Steinetz et al."
- Caveats on the positive run: three samples, no control result reported for the vault, the two
  260-hour replicates differ by 40 %, and the tabulated totals are about ten times what the paper's own
  stated counts-to-nuclei conversion gives (presumably an aliquot factor that is not spelled out). The
  authors ask for replication.

LCF is evidence that a deuterated lattice is a usable fusion fuel form under MeV irradiation. It says
nothing about low-energy photon triggering.

### 1.3 Screening for the product fuels: lithium and boron

| Target | Adiabatic limit (theory) | Reported | Reference |
|---|---|---|---|
| ⁶Li, ⁷Li + p, insulator (Li₂WO₄) | ~190 eV | 237 (+133/−77) eV | ✔ Cruz et al., *Phys. Lett. B* 624, 181 (2005) and 2008 follow-up |
| Li metal | 610 eV expected (✔✔ Huke et al.) | 1.18 ± 0.06 keV (Cruz); 425 ± 60 eV (Lamia 2012, via the Trojan-horse bare S-factor) | ✔ secondary |
| PdLiₓ alloy | 850 eV expected (✔✔ Huke et al.) | measured value not verified here ◦ | Cruz 2005 |
| ¹H(⁷Li,α)⁴He on hydrogen-loaded Pd foils | — | one foil "up to an order of magnitude above" theory, the other not; large effect only under tensile stress in earlier work | ✔ Lipoglavšek et al., *Phys. Lett. B* (2023); *Eur. Phys. J. A* (2010) |
| ¹¹B + p | 340 eV | 430 ± 80 eV direct; 472 ± 160 and 240 ± 200 eV via Trojan horse | ✔ Angulo et al. 1993 and later Trojan-horse work |

So p + Li has been measured inside metals, including palladium, with sample-dependent enhancement.
The numbers are at most ~1 keV. The bound-pair model in `physics-baseline.md` needs 7–12 keV for
lithium and 17–24 keV for boron. Reference S-factors: ✔✔ NACRE II, [arXiv:1310.7099](https://arxiv.org/abs/1310.7099):
⁶Li(p,α)³He 3.1 ± 0.4 MeV b; ⁷Li(p,α)⁴He 52 (+11/−8) keV b; ¹¹B(p,α)⁸Be 210 (+20/−30) MeV b.

### 1.4 Crystals and chips that already do fusion (without net energy)

- ✔ Naranjo, Gimzewski, Putterman, *Nature* 434, 1115 (2005): a pyroelectric crystal makes ~100 kV and
  drives D-D fusion from a tungsten nanotip; replicated in ✔ *Phys. Rev. Lett.* 96, 054803 (2006).
- ✔ Sandia "neutristor": a neutron generator in flat chip geometry.
- ✔ Curtis et al., *Nat. Commun.* 9, 1077 (2018): deuterated nanowire arrays, 2 × 10⁶ neutrons per
  joule, ~500× a flat target, at relativistic intensity. ✔ Ditmire et al., *Nature* 398, 489 (1999):
  cluster fusion, ~10⁵ neutrons per joule.
- Laser-initiated p-¹¹B: ✔ Labaune et al., *Nat. Commun.* 4, 2506 (2013); ◦ Giuffrida et al.,
  *Phys. Rev. E* 101, 013204 (2020); ✔ Magee et al., *Nat. Commun.* 14, 955 (2023).

### 1.5 A laser addressing a nucleus inside a designed crystal

✔ Tiedau et al., *Phys. Rev. Lett.* 132, 182501 (2024); ✔ Zhang, Ye et al., *Nature* 633, 63–70 (2024);
✔ Elwell et al., [arXiv:2404.12311](https://arxiv.org/abs/2404.12311): the ²²⁹Th isomer at 8.36 eV
driven by a laser inside CaF₂ and LiSrAlF₆. The only case of coherent light driving a nuclear state in
an engineered crystal. An existence proof and a toolkit, not fusion.

### 1.6 Putting light, ions and atoms where you want them

- ✔ Benz et al., *Science* 354, 726–729 (2016): picocavities confine light to well below 1 nm³.
  ✔ Chikkaraddy et al., *Nature* 535, 127–130 (2016): single-molecule strong coupling below 40 nm³.
- ✔ Liu, Tang, Hentschel, Giessen, Alivisatos, *Nat. Mater.* 10, 631–636 (2011): one palladium
  nanoparticle in the nanofocus of a gold antenna, hydrogen uptake read out optically. This is the
  NF-cell v0 site geometry, already fabricated for sensing.
- ✔ Herink, Solli, Gulde, Ropers, *Nature* 483, 190–193 (2012): electrons reach hundreds of eV in the
  near field of a nanotip.
- **Slow-ion laser accelerator.** ✔✔ Torrisi et al., [arXiv:2106.13701](https://arxiv.org/abs/2106.13701)
  is a concept paper: no proton gradient, period, aperture or damage number, no simulation results,
  and "all the experiments carried out so far used electrons." Useful content: the injection chain
  (electrostatic to 50 keV, dielectric RFQ to 1 MeV), a ~15 nm bucket at β = 0.01 and 1.5 µm, a
  nano-aperture ion source expected to give sub-10 nm beams at 0.5–1 nA, and an average beam current of
  order 10 pA. It names "p-B ultracompact nuclear fusion devices based on proton acceleration below
  1 MeV" as an application. Electron structures at 28 keV have reached 25–133 MeV/m.
- **Hydrogen through 2D crystals.** ✔✔ Lozada-Hidalgo et al., [arXiv:1511.06693](https://arxiv.org/abs/1511.06693):
  protons pass graphene and hBN about ten times faster than deuterons (zero-point difference ~60 meV);
  Pt-decorated hBN conducts ≈3 S/cm²; cm-scale CVD membranes keep the factor. For a deuterium feed it
  is poor (only ~10 % of the current emerges as D₂). For a proton-fuelled cell it is a feed that
  filters deuterium out, which is what an aneutronic cell wants.

### 1.7 Muon catalysis (the 2014 idea)

✔ ~150 D-T fusions per muon remains the ceiling; alpha sticking 0.3–1 %. ✔ Acceleron's diamond-anvil
experiment ([arXiv:2606.05333](https://arxiv.org/abs/2606.05333)) reports up to 150 ± 20. Muon
catalysis does not extend to lithium or boron: the muon binds to the higher-Z nucleus ◦.

### 1.8 Smaller is better: micro-scale traps (prior art for Track D)

- ✔ Barnes & Nebel, *Phys. Plasmas* 5 (1998); Nebel & Barnes, *Fusion Technology* 34 (1998): the
  Periodically Oscillating Plasma Sphere. Fusion power density ∝ 1/a⁴ and power per device ∝ 1/a, hence
  a "massively modular" reactor of many small traps. ✔ Park et al., *Phys. Rev. Lett.* (2005): the
  oscillation observed. ✔ Mitchell, Schauer, Barnes, *Phys. Rev. Lett.* 78, 58 (1997): density above
  the Brillouin limit at a 3 mm trap's focus.
- Caveats from the same programme: ~1000:1 compression needed; incomplete space-charge
  neutralisation; no fusion in a Penning trap as of 2020.

I found no treatment of this scaling at 100 nm with solid electrodes at volts per nanometre.

---

## Tier 2 — peer-reviewed theory, or single-group experiments awaiting confirmation

| Idea | Reference | Relevance | Caveat |
|---|---|---|---|
| Fusion rate in D₂ is 3 × 10⁻⁶⁴ s⁻¹; an electron mass of 5–10 mₑ would reach the claimed cold-fusion rates | ✔ Koonin & Nauenberg, *Nature* 339, 690 (1989) | Reproduced here: `sim/pair_fusion.py` gives 2.0 × 10⁻⁶⁴ s⁻¹ and the same 5–10 | A thought experiment, not a mechanism |
| Barrier penetration in an **equilibrium** solid cannot be enhanced nearly enough | ✔ Leggett & Baym, *Nature* 340, 45 (1989); *Phys. Rev. Lett.* 63, 191 (1989) | The central no-go theorem; it leaves driven systems open | A driven system is not thereby shown to work |
| **Models for nuclear fusion in the solid state** | ✔✔ Hagelstein, Metzler, Lilley, Messinger, Galvanetto, [arXiv:2501.08338](https://arxiv.org/abs/2501.08338) (2025); almost certainly the paper behind the 2025-01-14 video | The most developed driven-lattice theory. D₂ molecules in deuterium-packed Pd vacancies; a single uniform **MHz acoustic mode** (1 W, 5 MHz, ~3 mJ stored) transfers the fusion energy to Pd nuclei; 10⁻⁶ s⁻¹ per pair across 10¹⁵ coherent pairs. Screening alone, their Table 8: 150 eV → 1.5 × 10⁻³², 300 eV → 1.5 × 10⁻²², 350 eV → 2.2 × 10⁻²⁰ s⁻¹ | Preprint. By the authors' own account: reasonable dephasing "would show no observable coherent effects" in the simpler versions; the energy cost per transfer means the coefficient of performance "will be poor"; Pd level data are proxied from ¹²⁰Sn; several ingredients are labelled conjectures. Lasers appear only as suggestions, and the two-laser experiments are not mentioned |
| Catalogue of known enhancement mechanisms | ✔✔ Metzler, Hunt, Galvanetto, [arXiv:2208.07245](https://arxiv.org/abs/2208.07245) (*New J. Phys.* 26, 101202) | Proximity (D₂ in a vacancy instead of lattice sites) +80 orders; uniform screening +10–20; fluctuations +5–10; defect screening +5–15; resonances +3–7 and +20–30 | "We offer no single mechanism that could increase fusion rates by 40 orders of magnitude"; whether the factors multiply is not discussed |
| A 0⁺ threshold resonance in ⁴He decaying by e⁺e⁻ pairs | ✔✔ Czerski et al., [arXiv:2305.17101](https://arxiv.org/abs/2305.17101) (*Phys. Rev. C* 109, L021601); Dubey et al., [arXiv:2408.07567](https://arxiv.org/abs/2408.07567), **published as *Phys. Rev. X* 15, 041004 (2025)** | Pair-to-proton ratio measured in ZrD₂: 0.42 ± 0.05 at 10 keV, 0.060 ± 0.012 at 20 keV. Would give a neutron-poor D-D channel at low energy | One group. The fitted pair width rose from 1.4–2.8 to 14 times the proton width between papers after a model change; dominance below 5 keV is extrapolation; no full-energy pair measurement |
| Dynamically assisted tunnelling | ✔✔ Queisser & Schützhold, [arXiv:1902.04905](https://arxiv.org/abs/1902.04905) (*Phys. Rev. C* 100, 041601) | For D + T at 1 keV, a 10 keV X-ray field raises the tunnelling exponent by ten orders. The field couples through the pair's charge-to-mass asymmetry | Needs keV photons at 10¹³–10¹⁵ V/m; "the frequency of an optical laser is so low" that it acts only quasi-statically; **for D–D the coupling is zero** |
| A 1.55 eV laser at 10²⁰ W/cm² raises fusion probability × 10³ at 1 keV | ✔ Qi, Zhou, Wang, *Nucl. Sci. Tech.* (2025) | Low-frequency light can help in principle | ~10¹⁰ above anything a diode delivers |
| Fusion in a nanoshell | ✔✔ Kharzeev, Levitt, Trallero-Herrero, [arXiv:2503.15531](https://arxiv.org/abs/2503.15531) (2025) | A ~100 nm gold shell filled with D₂O, 1 µm laser at ~10⁹ V/cm, internal field ×100, deuterons at 25–60 keV, 10⁷ fusions/s per shell, "Q ≃ 100 is theoretically achievable" | Classical acceleration followed by ordinary beam-target fusion, so the stopping ceiling in `physics-baseline.md` applies unless the electrons are stripped; ionisation "has not yet been incorporated"; one author's company holds the IP |
| Light-driven plasmon oscillations give transient screening above any static value | ✔ US 10,566,094 B2 and US 10,264,661 B2 (Google / Univ. of Maryland) | The closest published statement of the photon-energized-site idea. Metzler et al. credit it with "~15 orders" for a 40 % rise in Uₑ | Patents, not data. A free-electron estimate here gives a far smaller effect (`physics-baseline.md`) |
| Nano-plasmonic laser fusion (NAPLIFE) | ✔ Hungarian collaboration | Resonant nano-antennas inside the fuel | Reported effect is larger laser craters, not a fusion rate |
| Anomalous heat from Ni-based nano-multilayers with H₂ | ✔ Iwamura et al., *Jpn. J. Appl. Phys.* 63, 037001 (2024) | Nanostructure as the active ingredient | Calorimetry only; no correlated nuclear products |

---

## Tier 3 — contested or unreplicated

- **Two-laser stimulation of PdD (Letts, Cravens, Hagelstein).** ✔ Excess power only at difference
  frequencies of 8.3, 15.3, 20.4 THz (*J. Condensed Matter Nucl. Sci.* 3, 59–76 (2010)). The one
  experimental claim that matches "reaction sites energized by laser diodes." No independent
  replication found; calorimetry only. Notably, the 2025 Hagelstein model does not cite it and favours
  acoustic over optical phonons.
- **Fleischmann-Pons excess heat.** ✔ The Google-funded effort found no evidence under rigorous
  conditions (*Nature* 570, 45–51 (2019)).
- **Phonon-nuclear excitation transfer (⁵⁷Co/⁵⁷Fe).** ✔ 17–19 % anomalies in MIT theses; unreplicated.
- **Ultra-dense deuterium / Rydberg-matter fusion (Holmlid).** ✔ Published critiques find the core
  claims unsupported.
- **ARPA-E LENR programme.** ✔ $10 M, eight teams, 2023. Stanford: "Nuclear Product Detection from
  Deuterated Nanoparticles Under Phonon Stimulation." Amphionic: reactions in "potential wells
  existing between two nanoscale surfaces." No outcome statements found; the 2026 LBNL paper is
  plausibly an output.

---

## Enabling technology: atomically precise fabrication today

- ✔✔ CBN Nano, [arXiv:2605.27250](https://arxiv.org/abs/2605.27250) (May 2026): carbon dimers placed one
  at a time by a purely mechanical transfer at 4 K. Largest structure: nine C₂ units (18 carbon atoms)
  in an X; also four- and eight-carbon chains. Per-step yields 84–97 % over 351 attempts; every
  placement consumes a fresh tool molecule and is imaged afterwards. Three-dimensional building is
  stated as a prospect, not a result. No rate or roadmap given.
- ✔ ORNL: AI-driven assembly of a 37-molecule artificial lattice. ✔ Zyvex: hydrogen depassivation
  lithography at sub-nm resolution, slow. ✔ Silicon Quantum Computing: phosphorus placement at ~0.13 nm.
- ✔ Chemistry makes atom-exact objects in bulk: H₂ and D₂ sealed inside C₆₀ by organic synthesis
  (Komatsu, Murata, Murata, *Science* 307, 238 (2005)).

Positional assembly today is ~10¹ atoms per structure for carbon, 2D, cryogenic and serial. The
roadmap's capability levels start from there.

---

## What the literature does and does not support

Supported:

1. A metal lattice raises sub-10-keV D-D rates beyond theory; the effect depends on loading, defects
   and surface state; two groups see a low-energy plateau.
2. Crystal order and an electrochemical bias each change the yield (× 2; +15 %).
3. A laser can coherently drive a nucleus in a designed crystal (²²⁹Th).
4. Nanostructure multiplies laser-fusion yield at high intensity (× 500).
5. Small traps favour fusion power density (1/a⁴).
6. Proton-on-lithium fusion has been measured inside palladium and lithium metal, with
   sample-dependent enhancement.

Not supported:

1. Net energy from any lattice-assisted reaction.
2. Any confirmed nuclear effect of low-intensity light on a hydrided lattice.
3. A plateau free of beam artifacts: neither plateau paper closes the fast-neutral question in the
   text available.
4. Screening anywhere near what lithium or boron fuel would need.
5. A mechanism by which one eV-scale photon triggers one MeV-scale event.

## What changed on full reading

1. **Lattice-confinement replication** is not a clean null: the reactor run failed to confirm, the
   fast-neutron run reported a 3–5× excess. Both are thinly sampled.
2. **The 10¹⁸ figure** is a ratio of normalised yields at 0.25 keV, not an absolute rate, and the
   paper's own fitted screening energies are 0.3–1.7 keV.
3. **The plateau has a second, independent observation** whose authors attribute part of their own
   signal to fast neutrals.
4. **The leading driven-lattice theory drives an acoustic mode at MHz**, not optical phonons or
   plasmons, and predicts a poor energy return by its authors' own estimate.
5. **Field-assisted tunnelling cannot act on D–D** (no relative force on identical nuclei) but does act
   on p–Li and p–B.
6. **The proton laser-accelerator paper is a concept note** without design numbers.
7. **Atom-by-atom carbon assembly stands at 18 atoms**, not thousands.
8. **The threshold-resonance work is now in *Phys. Rev. X***, with its key width revised sixfold.

## Reading queue

1. Karahadian et al., journal version: Methods and Extended Data (beam composition, neutral
   suppression, cross-normalisation of proton and neutron channels).
2. Cruz et al. 2005 and 2008, and Lipoglavšek et al. 2023: the lithium-in-palladium numbers.
3. Chen et al., *Nature* 2025 (Thunderbird) in full; Steinetz and Pines in full.
4. US 10,566,094 B2 claims and any experimental disclosure.
5. Letts-Hagelstein 2010 for exact laser powers and cathode preparation.
6. Rider 1995 thesis; Nevins on recirculating power.
7. Koonin & Nauenberg 1989 in full, to pin down the factor 1.5 between their rate and ours.
8. ARPA-E LENR project outcomes, Stanford and Amphionic first.
