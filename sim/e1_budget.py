#!/usr/bin/env python3
"""Count-rate and sensitivity budget for experiment E1.

E1: a keV D+ beam on PdD_x nano-antennas while a laser is chopped on and off;
lock-in on the 3 MeV protons from D(d,p)T.  Question answered here: how small a
light-induced change in the D-D rate could E1 see, for the v0 antenna array and
for a denser target built for the purpose?

Estimate-grade inputs (flagged in the output):
  * Stopping of D in Pd: Lindhard-Scharff velocity-proportional formula
    (valid below ~25 keV/u, typically good to a few tens of per cent).
  * Baseline screening energy in Pd: 0.8 keV (literature spans 0.3-1.0 keV).
  * Straight-line paths (no multiple-scattering detour), statistics-limited
    counting, detector covering 10 % of 4 pi.

Run:  python3 sim/e1_budget.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import baseline as b  # noqa: E402

E_CHARGE = 1.602176634e-19
N_PD = 4.0 / (4.03e-8) ** 3          # Pd atoms per cm^3 in beta-PdD (a = 4.03 A)
M_D_U = 2.0141


def stop_in_pd(e_per_u):
    """Lindhard-Scharff electronic stopping of a hydrogen isotope in Pd, eV cm^2/atom."""
    z2 = 46.0
    return 1.9151e-14 * z2 / (1.0 + z2 ** (2.0 / 3.0)) ** 1.5 * math.sqrt(e_per_u / 24.80)


def stop_per_target_d(e_lab, x):
    """Energy loss per (target D atom / cm^2) in PdD_x, eV cm^2."""
    e_u = e_lab / M_D_U
    return b.stop_in_hydrogen(e_u) + stop_in_pd(e_u) / x


def proton_yield(e0, u_e, x=0.9, thickness_nm=None, steps=3000, e_min=0.3):
    """D(d,p)T reactions per incident D+ in a PdD_x layer (thick if thickness_nm is None)."""
    h = (e0 - e_min) / steps
    y, depth_cm = 0.0, 0.0
    limit = None if thickness_nm is None else thickness_nm * 1e-7
    for i in range(steps):
        e = e0 - (i + 0.5) * h
        s = stop_per_target_d(e, x)
        y += b.sigma("DDp", e / 2.0, u_e) * b.BARN / s * h * 1e3
        depth_cm += h * 1e3 / (x * N_PD * s)
        if limit is not None and depth_cm >= limit:
            break
    return y


def budget(label, e0, fill, thickness_nm, f_active, current_ma=1.0, u_e=0.8,
           solid_angle=0.10, days=1.0):
    y = proton_yield(e0, u_e, thickness_nm=thickness_nm)
    rate = current_ma * 1e-3 / E_CHARGE * y * fill * solid_angle
    counts = rate * 86400.0 * days
    m = 6.0 / math.sqrt(counts)                      # 3-sigma on/off modulation
    lo, hi = 0.0, 2.0                                # screening change giving that modulation
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if proton_yield(e0, u_e + mid, thickness_nm=thickness_nm) / y - 1.0 < m:
            lo = mid
        else:
            hi = mid
    print(f"  {label:22s} {e0:4.0f} keV  {rate:9.3g} cps  {counts:9.3g} /day  "
          f"{100 * m:6.2f} %   dUe = {1e3 * hi:6.1f} eV   x{1 + m / f_active:7.1f}")


def main():
    prism_area = math.sqrt(3) / 4 * 30.0 ** 2                  # nm^2, one 30 nm prism
    v0_fill = 2 * prism_area / 200.0 ** 2                      # two prisms per 200 nm pixel
    v0_active = 40.0 / (2 * prism_area * 10.0)                 # 40 nm^3 hot spot / fuel volume
    print("E1 budget: 1 mA D+, Ue(Pd) = 0.8 keV, detector 10 % of 4pi, one day, light chopped 50/50")
    print(f"  Pd stopping check: {stop_in_pd(10.0) * 1e15:.1f}e-15 eV cm2/atom at 10 keV/u "
          f"(measured values for slow protons in Pd/Au are of order 10e-15)")
    print(f"  v0 array: areal fuel fill {100 * v0_fill:.2f} %, hot-spot share of fuel {100 * v0_active:.2f} %")
    print("  columns: target, beam energy, proton count rate, counts, smallest detectable modulation")
    print("           (3 sigma), the screening change that would cause it if all fuel responds,")
    print("           and the enhancement needed if only the gap hot spots respond")
    for e0 in (3.0, 5.0, 10.0):
        budget("thick PdD (reference)", e0, 1.0, None, 1.0)
        budget("v0 array, 10 nm", e0, v0_fill, 10.0, v0_active)
        budget("dense gaps, 50 nm", e0, 0.5, 50.0, v0_active)
    print("  beam power on target = 1 mA x E0 = 3-10 W: loading and temperature must be monitored,")
    print("  and a polarisation flip (field across vs along the gap) is the built-in null control.")


if __name__ == "__main__":
    main()
