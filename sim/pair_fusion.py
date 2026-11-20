#!/usr/bin/env python3
"""Fusion rate of a *bound* fuel pair:  Lambda = A * |psi(0)|^2.

Site physics, first model.  Two nuclei sit in a potential and never get a kick;
how often do they tunnel together and fuse?  This is the number a lattice site
has to deliver (see docs/physics-baseline.md, Wall 1).

  (a) Molecule.  The exact Born-Oppenheimer potential of H2 (Pachucki 2010) for
      any hydrogen-isotope pair, and for a hypothetical heavier electron m*
      (the Koonin-Nauenberg thought experiment: a heavier electron pulls the
      nuclei closer and screens them better).  Benchmark: Koonin & Nauenberg,
      Nature 339, 690 (1989), 3e-64 per second for D2.

  (b) Lattice sites.  Two nuclei on separate sites a distance R0 apart, each
      held by a harmonic well of energy quantum hw, repelled by a screened
      Coulomb potential Z1 Z2 e^2 exp(-R/lam)/R.  For nuclei on a lattice.

  (c) Cage.  Two nuclei sharing one cage of radius Rc (a vacancy, an endohedral
      molecule), kept apart only by the screened Coulomb potential.  The one
      free parameter that matters is the screening length lam, so this is the
      model used to state what each fuel needs.

Method: s-wave radial Schroedinger equation on a logarithmic grid, Numerov
integration outward from R -> 0 with running rescaling (the wavefunction grows
by up to e^700 through the barrier), ground state by bisection on node count.
All results are returned as log10, because the rates underflow a double.

Atomic units inside (hbar = m_e = e = 1).  Standard library only.
Run:  python3 sim/pair_fusion.py
"""
import math
import os

A0_CM = 0.529177210903e-8
A0_PM = 52.9177210903
HARTREE_EV = 27.211386245988
ME_KEV = 510.99895
ALPHA = 7.2973525693e-3
C_CM = 2.99792458e10
U_ME = 1822.888486209              # electron masses per atomic mass unit
E_HE_ATOM = -2.903724377034        # united-atom limit of H2: the helium ground state

MASS = {                           # nuclear masses in electron masses
    "p": 1836.15267343, "D": 3670.48296788, "T": 5496.92153573,
    "6Li": 6.0151228874 * U_ME - 3, "7Li": 7.0160034366 * U_ME - 3,
    "11B": 11.0093054 * U_ME - 5,
}
# name: (nucleus 1, nucleus 2, Z1*Z2, S(0) in keV b, MeV per reaction, source of S)
PAIRS = {
    "D-D":   ("D", "D", 1, 109.3, 3.65, "Bosch-Hale 1992, both branches"),
    "p-D":   ("p", "D", 1, 2.1e-4, 5.49, "NACRE II"),
    "D-T":   ("D", "T", 1, 1.14e4, 17.59, "Bosch-Hale 1992 at 0.5 keV"),
    "p-6Li": ("p", "6Li", 3, 3.1e3, 4.02, "NACRE II"),
    "p-7Li": ("p", "7Li", 3, 52.0, 17.35, "NACRE II"),
    "p-11B": ("p", "11B", 5, 2.1e5, 8.68, "NACRE II"),
}
LOG_BIG = math.log(1e200)


def reduced_mass(pair):
    a, b = PAIRS[pair][0], PAIRS[pair][1]
    return MASS[a] * MASS[b] / (MASS[a] + MASS[b])


def nuclear_constant(pair):
    """A in cm^3/s, from sigma*v = A |psi_Coulomb(0)|^2  =>  A = S(0) c / (pi alpha Z1Z2 mu c^2)."""
    zz, s0 = PAIRS[pair][2], PAIRS[pair][3]
    return s0 * 1e-24 * C_CM / (math.pi * ALPHA * zz * reduced_mass(pair) * ME_KEV)


# --- potentials ---------------------------------------------------------------
class ClampedSpline:
    """Cubic spline with zero slope at the first node and natural end."""

    def __init__(self, xs, ys):
        n = len(xs)
        h = [xs[i + 1] - xs[i] for i in range(n - 1)]
        a, b, c, d = [0.0] * n, [0.0] * n, [0.0] * n, [0.0] * n
        b[0], c[0], d[0] = 2 * h[0], h[0], 6 * (ys[1] - ys[0]) / h[0]     # y'(x0) = 0
        for i in range(1, n - 1):
            a[i], b[i], c[i] = h[i - 1], 2 * (h[i - 1] + h[i]), h[i]
            d[i] = 6 * ((ys[i + 1] - ys[i]) / h[i] - (ys[i] - ys[i - 1]) / h[i - 1])
        b[n - 1] = 1.0
        for i in range(1, n):                                             # Thomas algorithm
            w = a[i] / b[i - 1]
            b[i] -= w * c[i - 1]
            d[i] -= w * d[i - 1]
        m = [0.0] * n
        m[n - 1] = d[n - 1] / b[n - 1]
        for i in range(n - 2, -1, -1):
            m[i] = (d[i] - c[i] * m[i + 1]) / b[i]
        self.xs, self.ys, self.m, self.h = xs, ys, m, h

    def __call__(self, x):
        xs = self.xs
        lo, hi = 0, len(xs) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if xs[mid] > x:
                hi = mid
            else:
                lo = mid
        h, t0, t1 = self.h[lo], xs[lo + 1] - x, x - xs[lo]
        return (self.m[lo] * t0 ** 3 + self.m[lo + 1] * t1 ** 3) / (6 * h) \
            + (self.ys[lo] / h - self.m[lo] * h / 6) * t0 + (self.ys[lo + 1] / h - self.m[lo + 1] * h / 6) * t1


def _load_h2_potential():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "h2_bo_pachucki2010.txt")
    rs, es = [0.0], [E_HE_ATOM]
    with open(path) as fh:
        for line in fh:
            if line.strip() and not line.startswith("#"):
                r, e = (float(v) for v in line.split())
                rs.append(r)
                es.append(e - 1.0 / r)                 # electronic energy: smooth through R = 0
    return ClampedSpline(rs, es), rs[-1]


_H2_ELECTRONIC, _H2_RMAX = _load_h2_potential()


def v_h2(r):
    """Born-Oppenheimer potential of H2 in hartree, r in bohr (includes the 1/r repulsion)."""
    if r >= _H2_RMAX:
        return -1.0 - 6.499 / r ** 6
    return 1.0 / r + _H2_ELECTRONIC(r)


def v_site(zz, lam, r0, mu, hw):
    """Screened Coulomb repulsion plus a harmonic lattice well centred on r0 (all atomic units)."""
    k = mu * hw * hw
    return lambda r: zz * math.exp(-r / lam) / r + 0.5 * k * (r - r0) ** 2


# --- radial solver --------------------------------------------------------------
def _shoot(rs, r2v, h, two_mu, energy, keep):
    """Numerov on x = ln r for w = u / sqrt(r).  Returns (nodes, ln|u| per point or None)."""
    c = h * h / 12.0
    f0 = 1.0 - c * (0.25 + two_mu * (r2v[0] - rs[0] ** 2 * energy))
    f1 = 1.0 - c * (0.25 + two_mu * (r2v[1] - rs[1] ** 2 * energy))
    w0, w1 = math.sqrt(rs[0]), math.sqrt(rs[1])       # u ~ r at the origin
    scale, nodes = 0.0, 0
    lnu = [math.log(rs[0]), math.log(rs[1])] if keep else None
    for i in range(2, len(rs)):
        f2 = 1.0 - c * (0.25 + two_mu * (r2v[i] - rs[i] ** 2 * energy))
        w2 = ((12.0 - 10.0 * f1) * w1 - f0 * w0) / f2
        if (w2 < 0.0) != (w1 < 0.0):
            nodes += 1
        if abs(w2) > 1e200:
            w1 /= 1e200
            w2 /= 1e200
            scale += LOG_BIG
        if keep:
            lnu.append(math.log(abs(w2) + 1e-300) + scale + 0.5 * math.log(rs[i]))
        w0, w1, f0, f1 = w1, w2, f1, f2
    return nodes, lnu


def ground_state(potential, mu, r_max, r_min=1e-8, n=4000, level=0):
    """Bound state number `level` (0 = ground state, counting radial nodes) of two nuclei of
    reduced mass mu in potential(r).  Returns (energy [hartree], log10 |psi(0)|^2 [bohr^-3])."""
    h = math.log(r_max / r_min) / (n - 1)
    rs = [r_min * math.exp(i * h) for i in range(n)]
    vs = [potential(r) for r in rs]
    r2v = [r * r * v for r, v in zip(rs, vs)]
    if max(0.25 + 2 * mu * (a - r * r * min(vs)) for r, a in zip(rs, r2v)) * h * h / 12.0 >= 1.0:
        raise ValueError("grid too coarse for this potential; raise n or lower r_max")
    two_mu = 2.0 * mu
    e_lo = min(vs)
    step = 1e-4
    e_hi = e_lo + step
    while _shoot(rs, r2v, h, two_mu, e_hi, False)[0] <= level:
        step *= 2.0
        e_hi = e_lo + step
    for _ in range(46):
        mid = 0.5 * (e_lo + e_hi)
        if _shoot(rs, r2v, h, two_mu, mid, False)[0] <= level:
            e_lo = mid
        else:
            e_hi = mid
    lnu = _shoot(rs, r2v, h, two_mu, e_lo, True)[1]
    allowed = [i for i in range(n) if vs[i] < e_lo]   # the classically allowed well
    peak = max(allowed, key=lnu.__getitem__)
    cut = min(range(allowed[-1], n), key=lnu.__getitem__)   # drop the numerical blow-up beyond it
    norm = sum(math.exp(2.0 * (lnu[i] - lnu[peak])) * rs[i] for i in range(cut + 1)) * h
    ln_psi0_sq = 2.0 * (lnu[0] - math.log(rs[0]) - lnu[peak]) - math.log(4.0 * math.pi * norm)
    return e_lo, ln_psi0_sq / math.log(10.0)


# --- rates ------------------------------------------------------------------------
def rate_molecule(pair, m_star=1.0, level=0):
    """log10 of the fusion rate (per second) for a hydrogen-isotope pair in an H2-type molecule
    whose electrons have mass m_star, in vibrational state `level`.
    Returns (log10 rate, binding energy of that state in eV)."""
    assert PAIRS[pair][2] == 1, "the H2 potential applies to charge-1 pairs only"
    # Scaling lengths by 1/m* and energies by m* maps the problem onto reduced mass mu/m*.
    energy, log_psi = ground_state(v_h2, reduced_mass(pair) / m_star, r_max=14.0,
                                   n=4000 if level == 0 else 12000, level=level)
    if energy >= -1.0:
        raise ValueError(f"no bound vibrational level {level}")
    log_rate = math.log10(nuclear_constant(pair)) + log_psi + 3 * math.log10(m_star / A0_CM)
    return log_rate, (-1.0 - energy) * HARTREE_EV * m_star


def rate_site(pair, r0_pm, hw_mev, lam_pm):
    """log10 of the fusion rate (per second) for a pair at a lattice site.
    r0_pm: equilibrium separation, hw_mev: confinement quantum, lam_pm: screening length."""
    mu, zz = reduced_mass(pair), PAIRS[pair][2]
    r0, lam, hw = r0_pm / A0_PM, lam_pm / A0_PM, hw_mev * 1e-3 / HARTREE_EV
    sigma = 1.0 / math.sqrt(mu * hw)
    _, log_psi = ground_state(v_site(zz, lam, r0, mu, hw), mu, r_max=r0 + 7.0 * sigma)
    return math.log10(nuclear_constant(pair)) + log_psi - 3 * math.log10(A0_CM)


def rate_cage(pair, rc_pm, lam_pm):
    """log10 of the fusion rate (per second) for two nuclei sharing a hard-walled cage of radius
    rc_pm, repelled by a Coulomb potential screened over lam_pm."""
    mu, zz = reduced_mass(pair), PAIRS[pair][2]
    lam = lam_pm / A0_PM
    _, log_psi = ground_state(lambda r: zz * math.exp(-r / lam) / r, mu, r_max=rc_pm / A0_PM)
    return math.log10(nuclear_constant(pair)) + log_psi - 3 * math.log10(A0_CM)


def wkb_exponent_yukawa(pair, lam_pm):
    """Zero-energy tunnelling exponent through a Yukawa core: 4 sqrt(pi mu Z1Z2 lam)."""
    return 4.0 * math.sqrt(math.pi * reduced_mass(pair) * PAIRS[pair][2] * lam_pm / A0_PM)


def effective_charge(pair):
    """Charge (in e) with which a uniform electric field drives the pair's RELATIVE motion:
    (Z1 m2 - Z2 m1) / (m1 + m2).  Zero for identical nuclei: light cannot push D against D."""
    a, b, zz = PAIRS[pair][0], PAIRS[pair][1], PAIRS[pair][2]
    z1 = 1.0
    z2 = float(zz)
    return abs(z1 * MASS[b] - z2 * MASS[a]) / (MASS[a] + MASS[b])


def contact_screening_ev(pair, lam_pm):
    """Energy by which a screening length lam lowers the barrier at contact: Z1 Z2 e^2 / lam."""
    return PAIRS[pair][2] * HARTREE_EV * A0_PM / lam_pm


def solve_for(fn, target, lo, hi, increasing):
    """Bisection for fn(x) = target on [lo, hi] (geometric), fn monotonic."""
    for _ in range(18):
        mid = math.sqrt(lo * hi)
        if (fn(mid) < target) == increasing:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


TARGETS = (("100 uW/cm3 (betavoltaic class)", 1e-4), ("1 W/cm3", 1.0))
PAIRS_PER_CM3 = 3.0e22
CAGE_PM = 100.0


def required_log_rate(pair, watts_per_cm3):
    return math.log10(watts_per_cm3 / (PAIRS[pair][4] * 1.602176634e-13) / PAIRS_PER_CM3)


def required_screening_length(pair, watts_per_cm3, rc_pm=CAGE_PM):
    need = required_log_rate(pair, watts_per_cm3)
    return solve_for(lambda v: rate_cage(pair, rc_pm, v), need, 0.05, 40.0, False)


def main():
    print("== Nuclear constants A = S(0) c / (pi alpha Z1Z2 mu c^2) ==")
    for name in PAIRS:
        print(f"  {name:6s} A = {nuclear_constant(name):9.3e} cm3/s   (S(0) = {PAIRS[name][3]:g} keV b, {PAIRS[name][5]})")

    print("\n== (a) Molecules: benchmark against spectroscopy and Koonin-Nauenberg ==")
    for name, d0_exp in (("D-D", 4.556), ("p-D", 4.514), ("D-T", 4.573)):
        log_rate, d0 = rate_molecule(name)
        print(f"  {name:4s} D0 = {d0:.3f} eV (measured {d0_exp:.3f})   fusion rate = {10 ** log_rate:.1e} /s")
    print("  Koonin & Nauenberg 1989 for D2: 3e-64 /s")

    print("\n== (a) D2 with a hypothetical heavier electron m* ==")
    print("  m*     bond length [pm]   screening at contact [eV]    log10 rate [/s]")
    for m in (1, 2, 3, 5, 7, 10, 15, 20, 50, 100, 207):
        print(f"  {m:5.0f}   {74.1 / m:10.2f}        {51.80 * m:10.0f}              {rate_molecule('D-D', m)[0]:8.1f}")
    for label, p in TARGETS:
        need = required_log_rate("D-D", p)
        m = solve_for(lambda v: rate_molecule("D-D", v)[0], need, 1.0, 207.0, True)
        print(f"  {label}: needs 10^{need:.1f} /s per pair  ->  m* = {m:.1f}  (contact screening {51.80 * m:.0f} eV)")

    print("\n== (b) Nuclei on separate lattice sites: why PdD is worse than a molecule ==")
    d2 = rate_molecule("D-D")[0]
    lam_eq = solve_for(lambda v: rate_cage("D-D", CAGE_PM, v), d2, 2.0, 40.0, False)
    print(f"  screening length that makes a caged pair match the D2 molecule: {lam_eq:.1f} pm")
    for lam in (lam_eq, 10.0, 3.0):
        print(f"  D-D on neighbouring octahedral sites of PdD (285 pm apart, 40 meV wells), lam = {lam:4.1f} pm:"
              f"  10^{rate_site('D-D', 285.0, 40.0, lam):.0f} /s")
    print("  -> distance and well stiffness cost ~10^-34 before screening enters; pairs must share a cage")

    print(f"\n== (c) What each fuel needs: screening length for a pair sharing a {CAGE_PM:.0f} pm cage ==")
    print("  pair     target                           lam [pm]   screening at contact [keV]   field coupling q_eff/e")
    for name in ("D-D", "D-T", "p-6Li", "p-7Li", "p-11B"):
        for label, p in TARGETS:
            lam = required_screening_length(name, p)
            print(f"  {name:6s}   {label:30s}  {lam:6.2f}        {contact_screening_ev(name, lam) / 1e3:7.2f}"
                  f"                    {effective_charge(name):5.2f}")
    print("  for scale: electron Bohr radius 52.9 pm, muon Bohr radius 0.256 pm")
    print("  cage radius hardly matters: D-D at 1 W/cm3 needs lam = "
          + ", ".join(f"{required_screening_length('D-D', 1.0, rc):.2f} pm (Rc {rc:.0f})" for rc in (50.0, 100.0, 200.0)))


if __name__ == "__main__":
    main()
