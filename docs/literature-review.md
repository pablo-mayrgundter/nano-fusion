# Literature review: synthetic crystals, the LENR regime, and photon-energized reaction sites

Compiled 2026-11-20 from web searches plus the two NanoFusion Google Docs. Citations marked ✔ were
confirmed in this session against an abstract, journal listing or institutional page; citations marked
◦ are from memory and should be checked against the journal before being quoted externally. Nothing
here was read in full text — treat the numbers as abstract-level. (arxiv.org is outside this cloud
session's network allowlist, so preprint abstracts came through search summaries, not direct fetches.)

**Bottom line.** There is a real, mainstream-published body of evidence that a metal lattice changes
low-energy fusion rates by large factors, and it got stronger in 2025–2026. There is no confirmed
evidence that any lattice effect produces net energy, and no confirmed evidence that low-intensity light
changes a nuclear rate at all. The photon-energized-site idea has a clear theoretical motivation, a
directly on-point patent family from the Google-funded team, a 2025 plasmonic-nanoshell proposal from
mainstream theorists, an ARPA-E-funded Stanford test whose results I could not find, and one
unreplicated experimental claim.
It is an open experimental question that atomically precise fabrication is unusually well placed to
settle.

Evidence is sorted into three tiers. Tier 1 is safe to design around. Tier 2 is a hypothesis to test.
Tier 3 is a claim to test sceptically.

---

## Tier 1 — established or mainstream-published experimental results

### 1.1 The lattice changes the fusion rate (electron screening and beyond)

| Result | Reference | What it shows |
|---|---|---|
| Screening energies of several hundred eV in deuterated metals, versus ~25 eV for D₂ gas; small effect in insulators and semiconductors | ✔ Raiola et al., *Eur. Phys. J. A* 19, 283 (2004); ✔ Kasagi et al., *J. Phys. Soc. Jpn.* 71, 2881 (2002) (~600 eV in PdO); ✔ Czerski et al., *Europhys. Lett.* 54, 449 (2001); Rolfs group Pt: 670 ± 50 eV | Metals enhance sub-10-keV D-D rates far beyond what atomic screening theory gives |
| The values disagree strongly between hosts and between experiments; Debye-plasma explanation excluded | ✔ Huke, Czerski et al., [arXiv:0805.4538](https://www.arxiv.org/abs/0805.4538) (*Phys. Rev. C* 78, 015803 ◦) | The effect is real but not understood, and target surface/loading state is a major systematic |
| Uₑ = 1000 ± 250 eV in Pd under pulsed glow discharge; conference abstract reports > 100× bare yield below 2 keV | ✔ Schenkel et al., *J. Appl. Phys.* 126, 203302 (2019), [arXiv:1905.03400](https://doi.org/10.48550/arXiv.1905.03400) | Google-funded LBNL result, consistent with the accelerator data |
| Electrochemical loading of a Pd target raises D-D rate by 15(2) % | ✔ Chen et al., *Nature* 644, 640–645 (2025), [doi:10.1038/s41586-025-09042-7](https://ideas.repec.org/a/nat/nature/v644y2025i8077d10.1038_s41586-025-09042-7.html) ("Thunderbird" reactor, UBC) | First clean demonstration that a *chemical/electrical* knob on the lattice moves a nuclear rate. No net energy |
| **D-D yield stops falling below ~2–2.5 keV and plateaus; > 10¹⁸ over bare-nucleus theory in Pd and Ti hydride foils; depends on how the foil was loaded** | ✔ Karahadian, Colborne, Persaud, Schenkel, Munday, [arXiv:2512.06212](https://arxiv.org/abs/2512.06212v1); *Nature Communications*, July 2026 ([Physics World](https://physicsworld.com/a/nuclear-fusion-persists-at-ultralow-energies-inside-metal-foils/), [LBNL](https://newscenter.lbl.gov/2026/07/23/when-it-comes-to-fusion-materials-matter/)) | The most important new datum for this project. Authors call it a regime where the material actively shapes the reaction and say the microscopic origin (electrons, defects) is unknown. Absolute rate "far too small for energy production" |
| Yield anisotropy × 2 for 20 keV D⁺ along crystal planes of deuterated Pd; none in homogeneous TiD; similar in textured CVD diamond | ✔ Dalkarov, Bagulya et al. (Lebedev HELIS), *J. Surf. Investig.* (2020) [doi:10.1134/S102745102002024X](https://www.doi.org/10.1134/S102745102002024X); *NIM B* (2015) doi:10.1016/j.nimb.2015.01.021 | Crystal *order* matters: channeling and flux peaking concentrate the beam on interstitial fuel |

Why this matters for synthetic crystals: every one of these effects depends on things that conventional
metallurgy controls poorly and atom-by-atom synthesis controls completely — defect type and density,
loading ratio, interstitial site occupancy, surface termination, crystal orientation. The 2026 result
explicitly points at loading history and defects. A lattice built to specification is the natural next
experiment, whatever the answer turns out to be.

### 1.2 Lattice confinement fusion (NASA Glenn)

- ✔ Steinetz et al., "Novel nuclear reactions observed in bremsstrahlung-irradiated deuterated metals,"
  *Phys. Rev. C* 101, 044610 (2020); ✔ Pines et al., "Nuclear fusion reactions in deuterated metals,"
  *Phys. Rev. C* 101, 044609 (2020). ErD₃ and TiD₂ at ~10²³ D/cm³ irradiated with 2.9 MeV
  bremsstrahlung; photodisintegration neutrons heat deuterons, which fuse in the screened lattice;
  ~4 and ~5 MeV neutrons reported.
  ([NASA page](https://www.nasa.gov/glenn/glenn-expertise-space-exploration/lattice-confinement-fusion/),
  [ADS](https://ui.adsabs.harvard.edu/abs/2020PhRvC.101d4610S))
- **Counter-evidence:** ✔ Gillespie et al., [arXiv:2308.01434](https://arxiv.org/pdf/2308.01434) and
  [arXiv:2508.18243](https://web3.arxiv.org/pdf/2508.18243) irradiated TiD₂ at the Missouri research
  reactor. In the ~90 % thermal spectrum, tritium was within 25 % of conventional simulation, "without
  invoking screening-enhanced recoil-induced fusion." The second paper's title claims enhanced tritium
  under energetic neutrons; that part was not verified here. **Action: read both in full.**
- NASA follow-ups are white papers and presentations (Benyo & Forsley, Nov 2024; Jan 2025) aimed at a
  fusion-fast-fission hybrid for space power, not new peer-reviewed measurements.

LCF is photon-driven, but by MeV gammas from an accelerator. It is evidence that a deuterated lattice
is a usable fusion fuel form; it is not evidence for low-energy photon triggering.

### 1.3 Crystals and chips that already do fusion (without net energy)

- ✔ Naranjo, Gimzewski, Putterman, "Observation of nuclear fusion driven by a pyroelectric crystal,"
  *Nature* 434, 1115 (2005). A heated LiTaO₃ crystal makes ~100 kV; a tungsten nanotip field-ionises
  and accelerates D⁺ into ErD₂. Replicated: ✔ Geuther, Danon, Saglime, *Phys. Rev. Lett.* 96, 054803
  (2006). A crystal is the accelerator.
- ✔ Sandia "neutristor" (Elizondo-Decanini): a neutron generator in flat chip geometry; neutrons
  demonstrated at mm scale, ion sources at µm scale
  ([Sandia](https://newsreleases.sandia.gov/?p=4374)). Fusion-on-a-chip exists as a product concept.
- ✔ Curtis et al., "Micro-scale fusion in dense relativistic nanowire array plasmas,"
  *Nat. Commun.* 9, 1077 (2018): deuterated nanowire arrays give 2 × 10⁶ neutrons per joule, ~500× a
  flat target. Nanostructure multiplies laser-fusion yield, at relativistic intensity.
- ✔ Ditmire et al., *Nature* 398, 489–492 (1999): fusion from Coulomb explosion of laser-heated
  deuterium clusters, ~10⁵ neutrons per joule from a table-top laser.
- Laser-initiated p-¹¹B (the reaction in the main doc): ✔ Labaune et al., *Nat. Commun.* 4, 2506 (2013);
  ◦ Giuffrida et al., *Phys. Rev. E* 101, 013204 (2020); ✔ Magee et al., *Nat. Commun.* 14, 955 (2023)
  (first p-¹¹B in a magnetically confined plasma).

### 1.4 A laser addressing a nucleus inside a designed crystal

- ✔ Tiedau et al., *Phys. Rev. Lett.* 132, 182501 (2024): first resonant laser excitation of the ²²⁹Th
  nucleus, doped in CaF₂. ✔ Zhang, Ye et al., *Nature* 633, 63–70 (2024): VUV frequency comb drives the
  same nuclear transition in a solid host and links it to the Sr atomic clock
  ([paper](https://jila.colorado.edu/sites/default/files/2024-09/Th%20nuclear%20clock%202024-Nature.pdf)).
  ✔ Elwell et al., [arXiv:2404.12311](https://arxiv.org/abs/2404.12311) (LiSrAlF₆ host, isomer at
  8.355733 eV; journal reference *Phys. Rev. Lett.* 133, 013201 ◦); ✔ thin-film ²²⁹ThF₄ follow-up
  from JILA (*Nature*, Dec 2024).

This is the only case where coherent light has been shown to drive a nuclear state inside an engineered
crystal. It is an 8.4 eV isomer, not fusion. Its relevance is as an existence proof and as a toolkit:
the host crystal's electric field gradients, doping sites and defect chemistry measurably shape a
nuclear transition, and the community has built the doping, spectroscopy and theory to engineer it.

### 1.5 Putting a photon on one site

- ✔ Benz et al., *Science* 354, 726–729 (2016) (picocavities: light confined to well below 1 nm³ at a
  single atom, 10⁶ enhancement of optomechanical coupling to individual bonds);
  ✔ Chikkaraddy et al., *Nature* 535, 127–130 (2016) (single-molecule strong coupling in a plasmonic
  nanocavity below 40 nm³ at room temperature).
- ✔ Liu, Tang, Hentschel, Giessen, Alivisatos, *Nat. Mater.* 10, 631–636 (2011): one palladium
  nanoparticle placed in the nanofocus of a gold antenna, its hydrogen uptake read out optically. This
  is the NF-cell v0 site geometry, already fabricated, for sensing.
- ✔ Lozada-Hidalgo et al., [arXiv:1511.06693](https://arxiv.org/abs/1511.06693v1) (*Science* 2016 ◦):
  graphene and hBN monolayers pass protons about ten times faster than deuterons at room temperature
  — a one-atom-thick hydrogen-isotope membrane.
- ✔ Strong-field emission from plasmonic nanotips with few-cycle mid-IR pulses: electrons reach
  hundreds of eV, escaping the nanolocalised field within a fraction of an optical cycle (✔ Herink,
  Solli, Gulde, Ropers, *Nature* 483, 190–193 (2012); ✔ Echternkamp et al., *Appl. Phys. B* 2016). eV photons become sub-keV particles
  on a nanostructure, with oscillator-level pulse energies.
- On-chip accelerators from the Notes doc: ◦ Sapra et al., *Science* 367, 79 (2020); ◦ Chlouba et al.,
  *Nature* 622, 476 (2023). Both accelerate relativistic or near-relativistic *electrons*. For slow
  ions the only work found is a feasibility study for proton nanobeams in low-β dielectric laser
  stages with a dielectric RFQ front end (✔ Torrisi et al., [arXiv:2106.13701](https://www.arxiv.org/abs/2106.13701), 2021); no experiment; the required 6–70 nm periods are computed in `physics-baseline.md`.
- On-chip single-photon and nanolaser sources (quantum dots, hBN and diamond colour centres, plasmonic
  nanolasers) are mature enough to treat as components.

### 1.6 Muon catalysis (the 2014 idea)

- ✔ ~150 D-T fusions per muon remains the experimental ceiling; alpha sticking 0.3–1 % in the
  literature. ✔ Acceleron Fusion's MuFusE diamond-anvil experiment
  ([arXiv:2606.05333](https://arxiv.org/pdf/2606.05333)) reports up to 150 ± 20 fusions per muon and
  is exploring higher pressure and temperature; 2026 modelling
  ([arXiv:2605.26432](https://arxiv.org/pdf/2605.26432)) puts polarisation-assisted improvement at
  148 → ~193 cycles. The sticking problem the Notes doc proposed to attack with geometry is still the
  open problem, and it is being attacked with pressure rather than nanostructure.

---

## Tier 2 — peer-reviewed theory, or single-group experiments awaiting confirmation

| Idea | Reference | Relevance | Caveat |
|---|---|---|---|
| Fusion rate in D₂ is 3 × 10⁻⁶⁴ s⁻¹; an electron mass of 5–10 mₑ would reach the claimed cold-fusion rates | ✔ Koonin & Nauenberg, *Nature* 339, 690 (1989) | Defines the size of the gap and its extreme sensitivity to screening | Free molecule; later work notes neglected state dependence |
| Barrier penetration in an **equilibrium** solid cannot be enhanced anywhere near enough | ✔ Leggett & Baym, *Nature* 340, 45 (1989); *Phys. Rev. Lett.* 63, 191 (1989) | The central no-go theorem. Its escape clause is non-equilibrium driving, i.e. the photons | A driven system is not thereby shown to work |
| Dynamically assisted tunnelling: a weak, fast field superposed on the Coulomb barrier raises tunnelling | ✔ Queisser & Schützhold, *Phys. Rev. C* 100, 041601 (2019), [arXiv:1902.04905](https://arxiv.org/pdf/1902.04905); Lv, Duan, Liu, *Phys. Rev. C* 100, 064610 (2019) and comment; Wang, *Phys. Rev. C* 102, 011601 (2020) ◦ | Peer-reviewed mechanism by which light assists fusion | Needs XFEL-class fields; no experiment yet |
| A 1.55 eV laser at 10²⁰ W/cm² raises fusion probability × 10³ at 1 keV | ✔ Qi, Zhou, Wang, *Nucl. Sci. Tech.*, doi:10.1007/s41365-025-01879-x ([summary](https://www.miragenews.com/laser-enhanced-nuclear-fusion-reactions-study-1605247/)) | Low-frequency light can help, in principle | Idealised two-body theory; intensity ~10¹⁰ above anything a diode delivers |
| Catalogue of known mechanisms that raise solid-state fusion rates; > 40 orders needed, cascading mechanisms argued to reach it | ✔ Metzler, Hunt, Hagelstein, Galvanetto, *New J. Phys.* 26, 101202 (2024), [arXiv:2208.07245](https://arxiv.org/abs/2208.07245) | The best single map of the enhancement landscape | Review of mechanisms, not a demonstration |
| Nuclear Dicke model: D-D ↔ Pd energy transfer via lattice vibrations, with screening and tunnelling, gives > 40 orders | ✔ Hagelstein, Metzler, Lilley, Messinger, Galvanetto, [arXiv:2501.08338](https://arxiv.org/abs/2501.08338v2) (2025). Almost certainly the paper behind the 2025-01-14 video in the Notes doc | The most explicit theory in which a *driven lattice mode* is the active ingredient | Preprint in physics.gen-ph; unconfirmed |
| A 0⁺ threshold resonance in ⁴He dominates D-D at very low energy, decaying by e⁺e⁻ pairs | ✔ Czerski et al., *Phys. Rev. C* 109, L021601 (2024); [arXiv:2408.07567](https://arxiv.org/abs/2408.07567v2); [arXiv:2409.02112](https://export.arxiv.org/pdf/2409.02112) (D-D at thermal energies in ion tracks) | Would change the branching ratio as well as the rate — a route to neutron-poor D-D | One group (Szczecin); Czerski did publicly welcome the 2026 LBNL result as corroboration |
| **Light-driven plasmon oscillations concentrate electrons around light nuclei, giving transient screening above any static value** | ✔ US 10,566,094 B2 ([Google Patents](https://patents.google.com/patent/US10566094B2/en)) and US 10,264,661 B2 ([link](https://patents.google.com/patent/US10264661B2)); Google LLC / Univ. of Maryland; Munday, Murray, Narayan, Fork | **The closest published statement of the NanoFusion photon-energized-site concept**, from the team behind the 2019 and 2026 papers | Patents, not data. No published confirmation found |
| **Fusion in a nanoshell:** moderate-intensity laser on D₂O-filled metal nanoshells; plasmonic field enhancement accelerates deuterons | ✔ Kharzeev, Levitt, Trallero-Herrero, [arXiv:2503.15531](https://arxiv.org/abs/2503.15531v2) (2025) | A plasmonic nanostructure as the fusion driver, proposed by mainstream nuclear and strong-field physicists. Same family as the v0 nanogap site | Rate estimates only; no measurement |
| Nano-plasmonic laser fusion (NAPLIFE): gold nanorod antennas embedded in the target absorb fs laser light | ✔ Hungarian NAPLIFE collaboration ([overview](https://communities.springernature.com/posts/nano-plasmonic-laser-induced-fusion-energy-naplife), [Laser Focus World](https://www.laserfocusworld.com/lasers-sources/article/55283233/catalyzing-nuclear-fusion-via-nanoplasmonics)) | An experimental programme built on resonant nano-antennas inside the fuel | Reported effect is 3–4× larger laser craters, not a measured fusion rate; high-intensity fs pulses; one collaboration |
| Anomalous heat from Ni-based nano-multilayers with H₂ | ✔ Iwamura et al., *Jpn. J. Appl. Phys.* 63, 037001 (2024) ([open access](https://iopscience.iop.org/article/10.35848/1347-4065/ad2622)); Clean Planet / Tohoku | Nano-*structure* as the active ingredient, in a mainstream journal | Calorimetry only, one lineage of groups, no correlated nuclear products |

---

## Tier 3 — contested or unreplicated

- **Two-laser stimulation of PdD (Letts, Cravens, Hagelstein).** ✔ Excess power reported only when two
  lasers' difference frequency hit 8.3, 15.3 or 20.4 THz, matched to optical-phonon modes of PdD;
  required p-polarisation and overlapped beams (*J. Condensed Matter Nucl. Sci.* 3, 59–76 (2010);
  [2008 paper](https://www.newenergytimes.com/v2/library/2008/2008LettsHagelstein-StimulationofOpticalPhonons.pdf)).
  This is the single experimental claim that matches "reaction sites energized by laser diodes," and
  it used exactly diode-class lasers. No independent replication was found, the diagnostics were
  calorimetric, and it was published in the field's own journal. **It is the first thing this program
  should replicate with nuclear diagnostics** (Phase 1, experiment E3).
- **Fleischmann-Pons excess heat and descendants.** ✔ The Google-funded multi-institution effort found
  no evidence under rigorous conditions (Berlinguette et al., "Revisiting the cold case of cold fusion,"
  *Nature* 570, 45–51 (2019)), while generating the screening results in Tier 1.
- **Phonon-nuclear excitation transfer (⁵⁷Co/⁵⁷Fe).** ✔ MIT theses report 17–19 % emission anomalies
  after mechanical stress, described by their own authors as "not inconsistent" with theory. Unreplicated.
- **Ultra-dense deuterium / Rydberg-matter fusion (Holmlid).** ✔ Published critiques find the core
  claims unsupported (Hansen & Engelen comment; Shmatov, *Energy, Sustainability and Society* (2024)).
  Not a basis for design. Note this is distinct from the sound physics of Rydberg atom arrays cited in
  the main doc.
- **ARPA-E LENR exploratory programme.** ✔ $10 M to eight teams in Feb 2023 (Amphionic, Energetics
  Technology Center, LBNL, MIT, Stanford, Texas Tech, Michigan × 2), explicitly to settle the question
  either way. Two of the funded projects are close relatives of the NanoFusion concept
  ([project descriptions](https://arpa-e.energy.gov/sites/default/files/2025-01/Project%20Descriptions_LENR.pdf)):
  Stanford, "Nuclear Product Detection from Deuterated Nanoparticles Under Phonon Stimulation"
  ($1.5 M), i.e. a driven lattice read out with nuclear diagnostics; and Amphionic, testing whether
  reactions occur in "potential wells existing between two nanoscale surfaces" by controlling
  nanoparticle geometry, separation, composition and loading. Texas Tech is the shared
  nuclear-diagnostics hub. No outcome statement was found as of this date; the 2026 LBNL paper is
  plausibly one of the programme's outputs. **Action: find the Stanford and Amphionic results before
  designing E1 and E3 — they may already have run them.**

---

## Enabling technology: atomically precise fabrication today

The plan assumes this matures. Where it actually stands (✔ all from 2025–2026 reports, mostly secondary
sources):

- CBN Nano: positionally controlled C₂ donation and stepwise C-C bond formation on H-passivated
  Si(100) by inverted-mode STM (arXiv:2605.27250, May 2026).
- ORNL: AI-driven atom-by-atom assembly; 37-molecule artificial graphene lattice with a measured Dirac
  point (*ACS Nano*).
- Zyvex Labs: hydrogen depassivation lithography at sub-nm resolution with the ZyVector/ZL-1 tools;
  DOE's own assessment calls it slow and limited to phosphorus dopants.
- Silicon Quantum Computing: phosphorus placement in silicon at ~0.13 nm accuracy
  (*Nature Nanotechnology* comment).

Chemistry is the other route to atom-exact objects, and it already works in bulk: ✔ Komatsu, Murata,
Murata, *Science* 307, 238–240 (2005) sealed H₂ inside C₆₀ by organic synthesis ("molecular surgery"),
and D₂@C₆₀ has since been made and studied spectroscopically. That is an atom-exact cage holding
exactly one fuel pair, produced by the flask.

Today positional assembly is 2D, ultra-high-vacuum, a few atoms per second, and a handful of chemistries. The roadmap
therefore defines capability levels (APM-0 to APM-4) and names a bridging process for every phase.

---

## What the literature does and does not support

Supported:

1. A metal lattice changes sub-10-keV fusion rates by orders of magnitude beyond theory, the effect
   depends on loading and defects, and it persists to lower energy than anyone expected (2026).
2. Crystal order changes yield (channeling, × 2).
3. An electrical knob on the lattice changes a nuclear rate (2025, 15 %).
4. A laser can coherently drive a nucleus in a designed crystal (2024, ²²⁹Th).
5. Nanostructure multiplies laser-fusion yield (2018, × 500).
6. Theory in which a driven, non-equilibrium lattice or field assists tunnelling is published in
   mainstream journals, and the no-go theorem applies only to equilibrium.

Not supported:

1. Net energy from any lattice-assisted reaction. Every confirmed rate is many orders below useful.
2. Any confirmed nuclear effect of low-intensity light on a deuterated lattice.
3. A dominant aneutronic D-D channel.
4. A known mechanism by which one eV-scale photon triggers one MeV-scale event.

The gap between the lists is the research programme. The best confirmed enhancement is 10¹⁸ relative to
bare nuclei at sub-keV beam energy; a beamless cell needs 10⁴⁸–10⁵² relative to a D₂ molecule at rest.
The baselines differ, so the remaining gap is not a simple subtraction, but it is tens of orders of
magnitude, to be delivered at room temperature and steered by light. That should be read as a long shot
with a cheap, decisive first test, not as an engineering problem.

## Reading queue

1. Karahadian et al. 2026 full text and methods (what exactly plateaus; fast-neutral backgrounds).
2. Gillespie et al. arXiv:2508.18243 (the energetic-neutron result).
3. US 10,566,094 B2 claims and any associated experimental disclosure.
4. Hagelstein et al. arXiv:2501.08338: extract the predicted dependence on phonon mode, drive power
   and loading, so E3 can be designed to falsify it.
5. Letts-Hagelstein 2010 for exact laser powers, spot sizes, cathode preparation.
6. Czerski arXiv:2408.07567 for the predicted e⁺e⁻ branching ratio versus energy.
7. Rider 1995 thesis, re-read for which assumptions fail at 10–100 nm with 1–10 V/nm electrodes.
8. Kharzeev et al. arXiv:2503.15531: their rate estimate and required intensity, as a cross-check on
   the v0 nanogap numbers.
9. ARPA-E LENR project outcomes, Stanford and Amphionic first.
