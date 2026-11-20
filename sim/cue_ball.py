#!/usr/bin/env python3
"""The aimed single shot ("cue ball"): how well can one nucleus be aimed at another?

Three questions, each with a number:
  1. If the collision is perfectly head-on, how often does it fuse?        (the pocket)
  2. How well is the target nucleus located, even at absolute zero?         (the jitter)
  3. What does perfect aiming buy, against an unaimed beam?                 (the gain)

Standard library only.   Run:  python3 sim/cue_ball.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import baseline as b  # noqa: E402

HBARC = 197.3269804      # MeV fm
AMU = 931.49410          # MeV
EV_A2 = (HBARC * 1e-5 * 1e6) ** 2      # (hbar c)^2 in eV^2 A^2  (1 fm = 1e-5 A)


def wavelength_fm(mu_mev, e_cm_kev):
    """Reduced de Broglie wavelength of the relative motion."""
    return HBARC / math.sqrt(2.0 * mu_mev * e_cm_kev * 1e-3)


def zero_point_pm(mass_u, quantum_ev):
    """RMS zero-point displacement along one axis for a nucleus in a well of energy quantum hw."""
    return math.sqrt(EV_A2 / (2.0 * mass_u * AMU * 1e6) / quantum_ev) * 100.0


def main():
    print("== 1. The pocket: a head-on collision against the quantum limit pi*lambda-bar^2 ==")
    cases = (("p-11B at the 600 keV resonance", "pB11", b.M_P * b.M_B11 / (b.M_P + b.M_B11) * 1e-3, 600.0),
             ("D-T at the 64 keV resonance", "DT", b.M_D * b.M_T / (b.M_D + b.M_T) * 1e-3, 64.0),
             ("D-D at 50 keV", "DD", b.M_D / 2.0 * 1e-3, 50.0),
             ("D-D at 10 keV", "DD", b.M_D / 2.0 * 1e-3, 10.0))
    for label, key, mu, e in cases:
        lam = wavelength_fm(mu, e)
        limit = math.pi * lam * lam / 100.0                              # barn
        sig = b.sigma(key, e) if key != "DD" else b.sigma("DDp", e) + b.sigma("DDn", e)
        print(f"  {label:32s} lambda-bar {lam:5.1f} fm   limit {limit:6.2f} b   measured {sig:8.2e} b"
              f"   -> head-on fusion probability ~{min(1.0, sig / limit):.2g}")

    sig_f = b.sigma("pB11", 600.0) * 100.0                               # fm^2
    pocket = math.sqrt(sig_f / math.pi)
    print(f"\n  p-11B pocket: {sig_f:.0f} fm2, i.e. a disc of radius {pocket:.1f} fm")

    print("\n== 2. The jitter: zero-point motion of the target nucleus (one axis, at absolute zero) ==")
    targets = (("boron in a stiff covalent lattice", 11.009, 0.110), ("lithium in LiH", 7.016, 0.060),
               ("deuterium in PdD", 2.014, 0.040), ("hydrogen in PdH", 1.008, 0.060))
    for label, mass, hw in targets:
        print(f"  {label:34s} {zero_point_pm(mass, hw):5.1f} pm")
    sigma_t = zero_point_pm(11.009, 0.110) * 1e3                          # fm
    p_hit = sig_f / (2.0 * math.pi * sigma_t ** 2)
    print(f"  boron: jitter {sigma_t:.0f} fm against a {pocket:.1f} fm pocket"
          f" -> a perfect shot at the site centre hits with probability {p_hit:.1e}")
    pin = EV_A2 / (2.0 * 11.009 * AMU * 1e6) / (4.0 * (pocket * 1e-5) ** 2)
    print(f"  pinning a boron nucleus to {pocket:.1f} fm would take {2 * pin / 1e3:.0f} keV of zero-point energy"
          f" (two axes); a chemical bond supplies about {0.110 / 4 * 2 * 1e3:.0f} meV")

    print("\n== 3. What perfect aiming buys (650 keV protons on boron) ==")
    n_layer = 1.30e23 ** (2.0 / 3.0)                                      # atoms per cm2 in one atomic layer
    s_e = b.stop_in_boron(653.0 / 1.00728)
    p_unaimed = sig_f * 1e-26 * n_layer
    e_layer = s_e * n_layer
    print(f"  unaimed, per atomic layer: hit probability {p_unaimed:.1e}, energy lost {e_layer:.0f} eV"
          f" -> gain {p_unaimed * 8.682e6 / e_layer:.4f}")
    print(f"  aimed at each nucleus:     hit probability {p_hit:.1e}  ({p_hit / p_unaimed:.0f} times better)")
    for label, loss in (("if a central pass cost only the average", e_layer),
                        ("central pass through the K shell, low estimate", 60.0),
                        ("central pass through the K shell, high estimate", 110.0)):
        print(f"    {label:48s} {loss:5.0f} eV per shot -> gain {p_hit * 8.682e6 / loss:.2f}")
    print("  (K-shell figures are estimates: ionisation probability 0.1-0.2 per central pass at ~450 eV,")
    print("   plus 15-20 eV to valence electrons)")

    print("\n== 4. Is a photon a fine enough tool? ==")
    p_proton = math.sqrt(2.0 * 938.272 * 0.650)                           # MeV/c
    kick = 2.0e-6 / p_proton
    print(f"  one 2 eV photon turns a 650 keV proton by {kick:.1e} rad: {kick * 1e8:.1f} fm over 100 nm of flight")
    print(f"  one unit of angular momentum at a 100 nm standoff is a sideways momentum of"
          f" {HBARC / 1e8 * 1e6:.1f} eV/c: one visible photon")
    lam_lab = HBARC / p_proton
    print(f"  to use the {sigma_t / 1e3:.1f} pm jitter the beam needs a {sigma_t / 1e3:.1f} pm focus"
          f" (convergence {lam_lab / (2 * sigma_t) * 1e3:.1f} mrad); to reach the {pocket:.0f} fm pocket itself"
          f" it would need {lam_lab / (2 * pocket):.2f} rad")

    print("\n== 5. Knocking one nucleus of a bonded pair into the other (D2 molecule, bond 74 pm) ==")
    import pair_fusion as pf
    m_d_ev = pf.MASS["D"] * 510998.95
    print(f"  a free deuteron absorbing one 2 eV photon recoils with {2.0 ** 2 / (2 * m_d_ev):.1e} eV")
    print(f"  a 10 keV knock needs a photon momentum of {math.sqrt(2 * m_d_ev * 1e4) / 1e6:.1f} MeV/c (a gamma ray),")
    print(f"  or a field of {1e4 / 74.1 * 1e3:.0f} V/nm across the bond (materials fail near 10 V/nm)")
    print("  the hardest knock the bond itself can hold: pump the pair up its vibrational ladder")
    base = pf.rate_molecule("D-D")[0]
    best = (base, 0, 0.0)
    for v in (1, 5, 10, 15, 18, 21):
        rate, bound = pf.rate_molecule("D-D", 1.0, v)
        best = max(best, (rate, v, 4.556 - bound))
        print(f"    vibrational level {v:2d} ({4.556 - bound:4.2f} eV above ground): fusion rate 10^{rate:6.1f} /s")
    print(f"  ground state 10^{base:.1f}; best is level {best[1]} at 10^{best[0]:.1f}:"
          f" {best[0] - base:.0f} of the ~53 orders a battery needs")
    print("  a muon in place of an electron: 10^11.6 /s with no knock at all (sim/pair_fusion.py)")


if __name__ == "__main__":
    main()
