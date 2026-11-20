#!/usr/bin/env python3
"""NanoFusion baseline physics -- the numbers every reactor concept has to beat.

Pure standard library (no numpy) so it runs anywhere.  This is the seed of the
simulator: it holds the *accepted* physics (bare cross sections, electronic
stopping, screening in the standard "energy shift" approximation) so that any
proposed lattice / photon enhancement can be expressed as a multiplier on a
known baseline instead of as a free-floating claim.

Run:  python3 sim/baseline.py

Units: energies in keV unless a name says otherwise; cross sections in barn
(1 b = 1e-24 cm^2); stopping cross sections in eV cm^2 per target atom.

Sources for the parametrisations
  * D-T, D-D cross sections: Bosch & Hale, Nucl. Fusion 32, 611 (1992).
  * p-11B cross section:     Nevins & Swain, Nucl. Fusion 40, 865 (2000).
  * Proton stopping in H:    Andersen & Ziegler (1977) 5-coefficient fit.
  * Proton stopping in B:    Bethe formula, I = 76 eV (good to ~10-20 % above
                             ~300 keV/u, unusable below ~100 keV/u).
  * Screening:               f(E) = sigma(E + Ue) / sigma(E), Assenbaum,
                             Langanke & Rolfs, Z. Phys. A 327, 461 (1987).
"""
import math

ALPHA = 1.0 / 137.035999
AMU = 931494.10          # keV
M_P, M_D, M_T, M_B11 = 938272.09, 1875612.94, 2808921.13, 11.0065622 * AMU
EV = 1.602176634e-19     # J
BARN = 1e-24             # cm^2


def gamow_constant(z1, z2, m1, m2):
    """B_G = pi * alpha * Z1 * Z2 * sqrt(2 * mu c^2), in keV^0.5."""
    mu = m1 * m2 / (m1 + m2)
    return math.pi * ALPHA * z1 * z2 * math.sqrt(2.0 * mu)


# --- bare-nucleus cross sections -------------------------------------------
_BH = {  # Bosch-Hale Table IV: B_G, A1..A5, B1..B4 ; S in keV*mb
    "DT":  (34.3827, (6.927e4, 7.454e8, 2.050e6, 5.2002e4, 0.0),
            (6.38e1, -9.95e-1, 6.981e-5, 1.728e-4)),
    "DDp": (31.3970, (5.5576e4, 2.1054e2, -3.2638e-2, 1.4987e-6, 1.8181e-10),
            (0.0, 0.0, 0.0, 0.0)),
    "DDn": (31.3970, (5.3701e4, 3.3027e2, -1.2706e-1, 2.9327e-5, -2.5151e-9),
            (0.0, 0.0, 0.0, 0.0)),
}
B_G_PB11 = gamow_constant(1, 5, M_P, M_B11)   # ~150.3


def s_factor(reaction, e_cm):
    """Astrophysical S-factor in keV*b at centre-of-mass energy e_cm (keV)."""
    if reaction in _BH:
        _, a, b = _BH[reaction]
        num = a[0] + e_cm * (a[1] + e_cm * (a[2] + e_cm * (a[3] + e_cm * a[4])))
        den = 1.0 + e_cm * (b[0] + e_cm * (b[1] + e_cm * (b[2] + e_cm * b[3])))
        return num / den * 1e-3
    if reaction == "pB11":                      # Nevins-Swain, MeV*b -> keV*b
        e = e_cm
        if e < 400.0:
            s = 197.0 + 0.240 * e + 2.31e-4 * e * e \
                + 1.82e4 / ((e - 148.0) ** 2 + 2.35 ** 2)
        elif e < 642.0:
            x = (e - 400.0) / 100.0
            s = 330.0 + 66.1 * x - 20.3 * x * x - 1.58 * x ** 5
        else:
            s = (2.57e6 / ((e - 581.3) ** 2 + 85.7 ** 2)
                 + 5.67e5 / ((e - 1083.0) ** 2 + 234.0 ** 2)
                 + 1.34e5 / ((e - 2405.0) ** 2 + 138.0 ** 2)
                 + 5.68e5 / ((e - 3344.0) ** 2 + 309.0 ** 2) + 4.38)
        return s * 1e3
    raise ValueError(reaction)


def b_gamow(reaction):
    return B_G_PB11 if reaction == "pB11" else _BH[reaction][0]


def sigma(reaction, e_cm, u_e=0.0):
    """Cross section in barn.  u_e = screening energy in keV (0 = bare)."""
    if e_cm <= 0.0:
        return 0.0
    e_eff = e_cm + u_e
    return s_factor(reaction, e_eff) / e_eff * math.exp(-b_gamow(reaction) / math.sqrt(e_eff))


def screening_enhancement(reaction, e_cm, u_e):
    return sigma(reaction, e_cm, u_e) / sigma(reaction, e_cm)


# --- electronic stopping ----------------------------------------------------
def stop_in_hydrogen(e_per_u):
    """Proton-equivalent stopping per H/D/T atom, eV cm^2, at e_per_u keV/u."""
    a2, a3, a4, a5 = 1.44, 242.6, 1.2e4, 0.1159
    lo = a2 * e_per_u ** 0.45
    hi = a3 / e_per_u * math.log(1.0 + a4 / e_per_u + a5 * e_per_u)
    return lo * hi / (lo + hi) * 1e-15


def stop_in_boron(e_per_u):
    """Bethe stopping per B atom for a proton, eV cm^2 (use above ~150 keV/u)."""
    beta2 = 2.0 * e_per_u / AMU
    two_mv2 = 2.0 * 510998.95 * beta2            # eV
    arg = two_mv2 / 76.0
    if arg <= 1.5:
        return float("nan")
    return 5.099e-19 * 5.0 / beta2 * math.log(arg)


# --- beam on cold target ----------------------------------------------------
REACTIONS = {
    #  name: (channels, beam mass [u], cm fraction, energy per reaction [keV], stopping fn)
    "D->T":   (("DT",), 2.0141, M_T / (M_D + M_T), 17589.0, stop_in_hydrogen),
    "D->D":   (("DDp", "DDn"), 2.0141, 0.5, None, stop_in_hydrogen),
    "p->11B": (("pB11",), 1.00728, M_B11 / (M_P + M_B11), 8682.0, stop_in_boron),
}
E_DDP, E_DDN = 4033.0, 3269.0
PARTICLES = {  # name: (Z_beam, Z_target, m_beam, m_target) in keV
    "D->T": (1, 1, M_D, M_T), "D->D": (1, 1, M_D, M_D), "p->11B": (1, 5, M_P, M_B11),
}


def channel_energy(name, ch):
    if name == "D->D":
        return E_DDP if ch == "DDp" else E_DDN
    return REACTIONS[name][3]


def figure_of_merit(name, e_lab, u_e=0.0):
    """F = sigma * E_fus / S_e : fusion energy released per unit beam energy
    lost to electrons, at beam energy e_lab.  F is the ceiling on the energy
    gain of ANY scheme that sends ions through cold matter, no matter how the
    unburnt beam energy is recovered (see docs/physics-baseline.md)."""
    chans, m_u, cmf, _, stop = REACTIONS[name]
    s_e = stop(e_lab / m_u)
    return sum(sigma(c, e_lab * cmf, u_e) * BARN * channel_energy(name, c) * 1e3
               for c in chans) / s_e


def ion_ion_stopping(name, e_lab, b_max_nm=10.0):
    """Coulomb stopping of the beam ion on bare, free target nuclei, eV cm^2 per
    target ion (the only drag left in an electron-free reaction zone).
    S_n = K Z1^2 Z2^2 (m_e/M2) / beta^2 * ln(b_max / b_90), K = 4 pi r_e^2 m_e c^2."""
    z1, z2, m1, m2 = PARTICLES[name]
    beta2 = 2.0 * e_lab / m1
    e_cm = e_lab * m2 / (m1 + m2)
    b90_nm = 1.43996e-3 * z1 * z2 / (2.0 * e_cm)          # e^2 = 1.43996 eV nm
    return 5.099e-19 * z1 ** 2 * z2 ** 2 * (510.99895 / m2) / beta2 * math.log(b_max_nm / b90_nm)


def electron_free_fom(name, e_lab, b_max_nm=10.0):
    """F with electronic stopping replaced by ion-ion Coulomb stopping (Track D)."""
    chans, _, cmf, _, _ = REACTIONS[name]
    s_n = ion_ion_stopping(name, e_lab, b_max_nm)
    return sum(sigma(c, e_lab * cmf) * BARN * channel_energy(name, c) * 1e3 for c in chans) / s_n


def thick_target(name, e0, u_e=0.0, e_min=None, steps=4000):
    """Reactions per incident ion stopping in a pure fuel target, and gain Q."""
    chans, m_u, cmf, _, stop = REACTIONS[name]
    e_min = e_min if e_min is not None else (150.0 if name == "p->11B" else 0.5)
    if e0 <= e_min:
        return 0.0, 0.0
    h = (e0 - e_min) / steps
    y, e_out = 0.0, 0.0
    for i in range(steps):                       # midpoint rule in beam energy
        e = e_min + (i + 0.5) * h
        s_e = stop(e / m_u)
        for c in chans:
            dy = sigma(c, e * cmf, u_e) * BARN / s_e * h * 1e3   # h keV -> eV
            y += dy
            e_out += dy * channel_energy(name, c)
    return y, e_out / e0


def best_fom(name, u_e=0.0):
    grid = [10.0 * 1.02 ** i for i in range(315)]          # 10 keV .. ~5 MeV
    if name == "p->11B":
        grid = [e for e in grid if e > 200.0]
    return max((figure_of_merit(name, e, u_e), e) for e in grid)


# --- solid-state (no beam) rate targets -------------------------------------
def required_rate_per_pair(power_w_per_cm3, e_fus_mev, pairs_per_cm3):
    return power_w_per_cm3 / (e_fus_mev * 1e6 * EV) / pairs_per_cm3


def single_photon_field(photon_ev, volume_nm3, eps_r=1.0):
    """Vacuum (one-photon) RMS field in V/nm for a mode of given volume."""
    eps0 = 8.8541878128e-12
    return math.sqrt(photon_ev * EV / (2.0 * eps0 * eps_r * volume_nm3 * 1e-27)) * 1e-9


def main():
    print("== Gamow constants B_G [keV^0.5] ==")
    for label, args in (("D-D", (1, 1, M_D, M_D)), ("D-T", (1, 1, M_D, M_T)),
                        ("p-7Li", (1, 3, M_P, 7.01600 * AMU)),
                        ("p-11B", (1, 5, M_P, M_B11)),
                        ("p-15N", (1, 7, M_P, 15.0001 * AMU))):
        print(f"  {label:6s} {gamow_constant(*args):7.2f}")

    print("\n== Sanity checks against published values ==")
    print(f"  sigma DT  @ 10 keV cm : {sigma('DT', 10):.3e} b   (Bosch-Hale table 2.702e-2)")
    print(f"  sigma DDp @ 10 keV cm : {sigma('DDp', 10):.3e} b   (Bosch-Hale table 2.812e-4)")
    print(f"  sigma pB11@ 600 keV cm: {sigma('pB11', 600):.3f} b      (peak ~1.2 b)")
    print(f"  S_e p in H @ 1 MeV    : {stop_in_hydrogen(1000)*6.022e23/1.008/1e6:.0f} MeV cm2/g (PSTAR ~683)")

    print("\n== Bare cross sections and screening enhancement f = sigma(E+Ue)/sigma(E), D-D (both branches) ==")
    print("  E_cm[keV]   sigma_bare[b]   f(Ue=0.3)   f(Ue=1.0)   f(Ue=3.0 keV)")
    for e in (0.5, 1.0, 2.0, 5.0, 10.0, 25.0, 50.0):
        s0 = sigma("DDp", e) + sigma("DDn", e)
        fs = [(sigma("DDp", e, u) + sigma("DDn", e, u)) / s0 for u in (0.3, 1.0, 3.0)]
        print(f"  {e:8.1f}   {s0:12.3e}   {fs[0]:9.3g}   {fs[1]:9.3g}   {fs[2]:9.3g}")

    print("\n== Beam into cold fuel: figure of merit F = sigma*E_fus/S_e (ceiling on gain) ==")
    for name in REACTIONS:
        f, e = best_fom(name)
        print(f"  {name:7s} F_max = {f:.2e} at E_beam = {e:7.0f} keV  -> need sigma/S improved x{1/f:,.0f} for F=1")

    print("\n== Electron-free reaction zone (Track D): F with ion-ion Coulomb stopping only, b_max = 10 nm ==")
    for name, e in (("D->T", 108.0), ("p->11B", 653.0), ("D->D", 500.0), ("D->D", 2000.0)):
        ratio = ion_ion_stopping(name, e) / REACTIONS[name][4](e / REACTIONS[name][1])
        print(f"  {name:7s} E_beam = {e:6.0f} keV  S_ion/S_electron = {ratio:.2e}  F_electron_free = {electron_free_fom(name, e):6.2f}")
    print("  (elastic scattering is not a true loss if scattered ions stay confined; see Rider 1995)")

    print("\n== Thick-target yield and gain, bare vs screened (Ue in keV) ==")
    print("  reaction  E0[keV]   Ue    reactions/ion      Q = E_fus/E_beam")
    for name, e0s in (("D->T", (20, 50, 100, 200)), ("D->D", (5, 20, 100, 200)),
                      ("p->11B", (400, 700, 1500))):
        for e0 in e0s:
            for u in (0.0, 1.0):
                y, q = thick_target(name, float(e0), u)
                print(f"  {name:7s} {e0:7d}   {u:3.1f}   {y:12.3e}      {q:10.3e}")

    print("\n== Solid-state route: fusion rate per fuel pair needed (D-D -> 23.85 MeV, 3.4e22 pairs/cm3) ==")
    kn = 3e-64   # Koonin & Nauenberg 1989, free D2 molecule
    for label, p in (("betavoltaic-class 100 uW/cm3", 1e-4), ("1 mW/cm3", 1e-3),
                     ("1 W/cm3", 1.0), ("1 kW/cm3", 1e3)):
        r = required_rate_per_pair(p, 23.85, 3.4e22)
        print(f"  {label:30s} {r:9.2e} /s per pair = 10^{math.log10(r/kn):.0f} x free-D2 rate")

    print("\n== Conventional D-D neutron output per unit fusion power (why fuel choice matters) ==")
    per_w = 1.0 / (0.5 * (E_DDP + E_DDN) * 1e3 * EV)
    print(f"  {per_w:.2e} reactions/s per W -> {0.5*per_w:.2e} n/s per W ({0.5*per_w*1e-6:.1e} n/s per uW)")

    print("\n== One-photon electric field vs mode volume (2 eV photon) ==")
    for label, v, eps in (("photonic-crystal cavity (lambda/n)^3 ~ 9e7 nm3, Si", 9e7, 12.0),
                          ("plasmonic nanogap 40 nm3", 40.0, 1.0),
                          ("picocavity 1 nm3", 1.0, 1.0)):
        print(f"  {label:52s} {single_photon_field(2.0, v, eps):9.2e} V/nm")
    print("  (compare: Coulomb field between two deuterons at 10 pm = 1.4e4 V/nm, at 100 pm = 144 V/nm)")

    print("\n== Low-beta laser accelerator: structure period = beta*lambda (lambda = 2 um) ==")
    for label, e, m in (("D+ 10 keV", 10.0, M_D), ("D+ 100 keV", 100.0, M_D),
                        ("p 100 keV", 100.0, M_P), ("p 600 keV", 600.0, M_P)):
        beta = math.sqrt(2.0 * e / m)
        print(f"  {label:11s} beta = {beta:.4f}  period = {beta*2000:6.1f} nm  evanescent decay ~ {beta*2000/(2*math.pi):5.1f} nm")


if __name__ == "__main__":
    main()
