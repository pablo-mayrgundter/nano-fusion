#!/usr/bin/env python3
"""Lattice route versus beam route for the product fuels, in numbers.

Backs the question "should the product be re-centred on a recirculating proton beam for p-11B?"
(docs/design-notes.md, open question 1).  Everything is built from baseline.py (cross sections,
stopping) and pair_fusion.py (bound-pair rates); nothing here is fitted.

Needs PyYAML (through cell_model).   Run:  python3 sim/beam_route.py
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import baseline as b      # noqa: E402
import cell_model as cm   # noqa: E402
import pair_fusion as pf  # noqa: E402
import yaml               # noqa: E402

E2_EV_CM = 1.43996e-7            # e^2 in eV cm
E_FUS_PB11 = 8.682e6             # eV
NAME = "p->11B"
CMF = b.M_B11 / (b.M_P + b.M_B11)


def lattice_at_face_value(cell):
    """If the screening energies reported in beam experiments applied to a caged pair at rest."""
    reported = {"D-D": ((0.3, "UHV accelerators"), (1.0, "glow discharge, Pd"), (1.7, "2026 membrane, PdD")),
                "p-7Li": ((0.425, "Li metal, Trojan-horse based"), (1.18, "Li metal, direct")),
                "p-11B": ((0.43, "direct measurement"),)}
    print("== Lattice route, taking reported screening at face value (caged pair, 100 pm cage) ==")
    print("  fuel     reported screening        ->  rate per pair      needed (sensor tier)   shortfall")
    for fuel, rows in reported.items():
        need = math.log10(cell.requirements(fuel, 1e-4)["rate per fuel pair [/s]"])
        for kev, label in rows:
            lam = pf.PAIRS[fuel][2] * pf.HARTREE_EV * pf.A0_PM / (kev * 1e3)
            rate = pf.rate_cage(fuel, 100.0, lam)
            short = need - rate
            verdict = "inside the battery band" if short <= 0 else f"{short:5.0f} orders short"
            print(f"  {fuel:6s}   {kev:5.2f} keV ({label:28s})  10^{rate:7.1f} /s      10^{need:5.1f} /s          {verdict}")


def bare_ion_yield(e0, b_max_nm, e_min=150.0, steps=4000):
    """Fusion probability of a proton that slows to rest on bare, cold boron nuclei (no electrons)."""
    h = (e0 - e_min) / steps
    y = 0.0
    for i in range(steps):
        e = e_min + (i + 0.5) * h
        y += b.sigma("pB11", e * CMF) * b.BARN / b.ion_ion_stopping(NAME, e, b_max_nm) * h * 1e3
    return y


def scattering_per_fusion(e_lab, b_max_nm):
    """Mean-square deflection of the proton, in rad^2, accumulated over one fusion mean free path."""
    e_cm = e_lab * CMF * 1e3                                   # eV
    zz = 5.0
    b90_cm = zz * E2_EV_CM / (2.0 * e_cm)
    log = math.log(b_max_nm * 1e-7 / b90_cm)
    theta2_cm = 2.0 * math.pi * (zz * E2_EV_CM / e_cm) ** 2 * log          # cm^2, centre-of-mass angle
    return theta2_cm * CMF ** 2 / (b.sigma("pB11", e_lab * CMF) * b.BARN)   # lab angle of the proton


def main():
    with open(os.path.join(os.path.dirname(HERE), "design", "nf-cell-v1.yaml")) as fh:
        cell = cm.Cell(yaml.safe_load(fh))
    lattice_at_face_value(cell)

    print("\n== Beam route for p-11B: energy out per unit of beam energy dissipated ==")
    f_cold, e_best = b.best_fom(NAME)
    print(f"  into solid boron (electrons present):    F = {f_cold:.1e} at {e_best:.0f} keV")
    for b_max in (10.0, 1000.0):
        f = b.electron_free_fom(NAME, 653.0, b_max)
        print(f"  onto bare boron nuclei, {b_max:6.0f} nm trap:     F = {f:.2f} at 653 keV")
    print("  proton slowing to rest on bare boron (10 nm cut-off):")
    for e0 in (700.0, 1000.0, 2000.0, 3500.0):
        y = bare_ion_yield(e0, 10.0)
        print(f"    injected at {e0:6.0f} keV: fusion probability {100 * y:5.1f} %,"
              f" fusion energy / beam energy = {y * E_FUS_PB11 / (e0 * 1e3):.2f}")

    print("\n== What scattering costs ==")
    for b_max in (10.0, 1000.0):
        r = scattering_per_fusion(653.0, b_max)
        print(f"  {b_max:6.0f} nm trap: {r:5.0f} rad^2 of deflection per fusion mean free path"
              f" (direction randomised ~{r:.0f} times per fusion)")
    r = scattering_per_fusion(653.0, 10.0)
    lost = b.ion_ion_stopping(NAME, 653.0) / (b.sigma("pB11", 653.0 * CMF) * b.BARN) / 653e3
    print(f"  energy handed to boron per fusion mean free path: {lost:.1f} x the proton's own energy")
    print("  beam trap that keeps only protons within a cone, ideal accelerator, 70 % direct conversion:")
    for half_angle in (0.1, 0.3, 1.0):
        p_fus = min(1.0, half_angle ** 2 / r)
        need = 1.0 - p_fus * E_FUS_PB11 * 0.7 / 653e3
        print(f"    acceptance {half_angle:3.1f} rad: fusion probability before loss {100 * p_fus:6.3f} %,"
              f" lost-ion energy recovery needed {100 * need:6.2f} %")

    print("\n== What the nanoscale adds: field, hence density ==")
    for field, gap_nm in ((1.0, 653.0), (5.0, 131.0)):
        charge = 8.8541878128e-12 * field * 1e9 / (1.602176634e-19 * gap_nm * 1e-9) * 1e-6     # e per cm3
        n_p, n_b = charge / 2.0, charge / 2.0 / 5.0
        v = math.sqrt(2.0 * 653e3 * 1.602176634e-19 / 1.6726e-27) * 100.0                       # cm/s
        per_proton = n_b * b.sigma("pB11", 653.0 * CMF) * b.BARN * v
        print(f"  {field:.0f} V/nm across {gap_nm:.0f} nm (653 kV): up to {charge:.1e} charges/cm3,"
              f" one fusion per proton every {1e3 / per_proton:.0f} ms,"
              f" {n_p * per_proton * E_FUS_PB11 * 1.602e-19:.1e} W per cm3 of trap")

    print("\n== Why the fuel matters: D-D at the sensor tier ==")
    n_per_s = 1e-4 * 0.5 / (0.5 * (b.E_DDP + b.E_DDN) * 1e3 * b.EV)
    flux = n_per_s / (4.0 * math.pi * 30.0 ** 2)
    print(f"  100 uW of D-D: {n_per_s:.1e} neutrons/s, {flux:.0f} n/cm2/s at 30 cm,"
          f" about {flux * 3600 * 4.16e-10 * 1e3:.0f} mSv per hour (public limit: 1 mSv per year)")


if __name__ == "__main__":
    main()
