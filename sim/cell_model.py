#!/usr/bin/env python3
"""Device-level cell model: turn a claim about site physics into a statement about a battery.

The site physics is unknown, so this model runs in two directions:

  requirements  -- for a target power density, what must each site do, how many photons may each
                   fusion cost, how many reactors can share one laser, and what limits lifetime;
  drive cost    -- if a site has to be held in an optical field, what does holding it cost, and
                   how reactive must the site be for the light to pay for itself.

Everything is read from the concept spec (design/nf-cell-v1.yaml); nothing here is tuned.
Needs PyYAML.   Run:  python3 sim/cell_model.py [spec.yaml]
"""
import math
import sys

import yaml

EV = 1.602176634e-19
EPS0 = 8.8541878128e-12
HBAR_EVS = 6.582119569e-16
N_A = 6.02214076e23
YEAR = 3.156e7

FUELS = {  # MeV per reaction, charged products per reaction, fuel atoms (name, mass number)
    "p-11B": (8.68, 3, (("H", 1), ("B", 11))),
    "p-7Li": (17.35, 2, (("H", 1), ("Li", 7))),
    "p-6Li": (4.02, 2, (("H", 1), ("Li", 6))),
    "D-D": (3.65, 1, (("D", 2), ("D", 2))),
}


def val(node):
    return float(node["value"]) if isinstance(node, dict) else float(node)


class Cell:
    def __init__(self, spec):
        self.spec = spec
        self.layer_cm = val(spec["stack"]["layer_pitch_um"]) * 1e-4
        crystal = spec["site_crystal"]
        cage_cm = val(crystal["cage_pitch_nm"]) * 1e-7
        self.film_cm = val(crystal["film_thickness_nm"]) * 1e-7
        self.pairs_per_cm2 = (val(crystal["areal_fill"]) * self.film_cm / cage_cm ** 3
                              * val(spec["site"]["pairs_per_cage"]))            # per layer
        self.pairs_per_cm3 = self.pairs_per_cm2 / self.layer_cm
        self.pixels_per_cm2 = 1.0 / (val(spec["pixel"]["pitch_nm"]) * 1e-7) ** 2
        lu = spec["laser_unit"]
        self.laser_w = val(lu["optical_power_mW"]) * 1e-3
        self.photon_j = val(lu["photon_energy_eV"]) * EV
        self.eta_laser = val(lu["wall_plug_efficiency"])
        self.eta_dist = val(lu["distribution_efficiency"])
        self.eta_capture = val(spec["capture"]["efficiency"])
        self.damage_fluence = val(spec["capture"]["damage_fluence_alpha_per_cm2"])
        self.h = val(spec["thermal"]["passive_h_W_per_m2K"])
        self.dt = val(spec["thermal"]["allowed_delta_T_K"])

    # -- photon economy ---------------------------------------------------------
    def photons_per_fusion_allowed(self, fuel, q_eng):
        """Photons that may be spent per fusion event for electricity out / electricity in = q_eng."""
        e_f = FUELS[fuel][0] * 1e6 * EV
        return self.eta_capture * self.eta_laser * self.eta_dist * e_f / (self.photon_j * q_eng)

    # -- requirements for a target ------------------------------------------------
    def requirements(self, fuel, net_w_per_cm3, q_eng=3.0):
        e_f = FUELS[fuel][0] * 1e6 * EV
        n_charged = FUELS[fuel][1]
        # net = gross electric - laser electric = eta_c * P_fus * (1 - 1/q_eng)
        p_fus = net_w_per_cm3 / (self.eta_capture * (1.0 - 1.0 / q_eng))
        events_cm3 = p_fus / e_f
        per_pair = events_cm3 / self.pairs_per_cm3
        n_gamma = self.photons_per_fusion_allowed(fuel, q_eng)
        light_cm3 = events_cm3 * n_gamma * self.photon_j                 # optical W absorbed per cm3
        alpha_flux = events_cm3 * self.layer_cm * n_charged              # per cm2 of collector per s
        heat = p_fus * (1.0 - self.eta_capture) + self.eta_capture * p_fus / q_eng
        return {
            "fusion power [W/cm3]": p_fus,
            "rate per fuel pair [/s]": per_pair,
            "photons allowed per fusion": n_gamma,
            "light per pixel [W]": light_cm3 * self.layer_cm / self.pixels_per_cm2,
            "light per fuel pair [W]": light_cm3 / self.pairs_per_cm3,
            "cm3 of stack per 1 mW laser": self.laser_w * self.eta_dist / light_cm3,
            "fuel film burn-up without resupply [yr]": 1.0 / per_pair / YEAR,
            "helium [cm3 STP per cm3 per yr]": events_cm3 * n_charged * YEAR / N_A * 22414.0,
            "collector life at damage fluence [h]": self.damage_fluence / alpha_flux / 3600.0,
            "thickest passively cooled sheet [mm]": 2.0 * self.h * self.dt / (heat * 1e6) * 1e3,
        }

    # -- cost of holding a site in an optical field ---------------------------------
    def drive_cost(self, fuel, field_v_per_nm, mode_volume_nm3, quality_factor):
        """Power dissipated to hold one mode at the given field, and the fusion rate that mode's
        sites must reach (while lit) for the light to pay for itself at q_eng = 1."""
        stored = EPS0 * (field_v_per_nm * 1e9) ** 2 * mode_volume_nm3 * 1e-27     # J
        omega = self.photon_j / EV / HBAR_EVS
        power = stored * omega / quality_factor
        e_f = FUELS[fuel][0] * 1e6 * EV
        rate = power / (self.eta_capture * self.eta_laser * self.eta_dist * e_f)
        return stored / EV, power, rate


def fmt(x):
    if x == float("inf"):
        return "unlimited"
    return f"{x:.3g}"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "design/nf-cell-v1.yaml"
    with open(path) as fh:
        spec = yaml.safe_load(fh)
    cell = Cell(spec)
    print(f"== {spec['meta']['name']}: geometry ==")
    print(f"  site crystal: {cell.pairs_per_cm2:.2e} fuel pairs per cm2 per layer, {1 / cell.layer_cm:.0f} layers per cm,"
          f" {cell.pairs_per_cm3:.2e} pairs per cm3 of stack")
    print(f"  (a fully dense crystal would hold ~3e22 per cm3; a single pair per 200 nm pixel only"
          f" {cell.pixels_per_cm2 / cell.layer_cm:.1e})")
    print(f"  efficiencies: capture {cell.eta_capture}, laser {cell.eta_laser}, distribution {cell.eta_dist}"
          f"  (all assumed)")

    print("\n== Photon economy: photons that may be spent per fusion ==")
    for fuel in ("p-11B", "p-7Li", "p-6Li", "D-D"):
        print(f"  {fuel:6s} break-even {cell.photons_per_fusion_allowed(fuel, 1.0):9.3g}"
              f"    for electricity out = 3 x in {cell.photons_per_fusion_allowed(fuel, 3.0):9.3g}")

    tiers = spec["tiers"]
    for fuel in (spec["fuel"]["primary"], spec["fuel"]["alternates"][0]):
        print(f"\n== Requirements, fuel {fuel}, electricity out = 3 x electricity in ==")
        rows = {name: cell.requirements(fuel, float(p)) for name, p in tiers.items()}
        print(f"  {'tier':42s}" + "".join(f"{n:>12s}" for n in tiers))
        print(f"  {'net electrical power [W/cm3]':42s}" + "".join(f"{float(p):>12.0e}" for p in tiers.values()))
        for key in next(iter(rows.values())):
            print(f"  {key:42s}" + "".join(f"{fmt(rows[n][key]):>12s}" for n in tiers))

    print("\n== Cost of holding a site in an optical field (fuel p-11B, 2 eV light) ==")
    print("  case                                                stored [eV]   power [W]   fusions/s needed while lit")
    cases = (("plasmonic gap, 1 V/nm, 40 nm3, Q 10", 1.0, 40.0, 10.0),
             ("plasmonic gap, 0.1 V/nm, 40 nm3, Q 10", 0.1, 40.0, 10.0),
             ("dielectric cavity, 1 V/nm, 125 nm3 per site, Q 1e6", 1.0, 125.0, 1e6),
             ("dielectric cavity, 0.01 V/nm, 125 nm3 per site, Q 1e6", 0.01, 125.0, 1e6))
    for label, e, v, q in cases:
        stored, power, rate = cell.drive_cost("p-11B", e, v, q)
        print(f"  {label:52s} {stored:9.3g}   {power:9.3g}   {rate:10.3g}")
    need = cell.requirements("p-11B", 1.0)
    print(f"  for comparison, the handheld tier allows {need['light per fuel pair [W]']:.1e} W of light per fuel pair")
    print("  -> a continuously held optical field costs many orders of magnitude more than a site can repay.")

    print("\n== If light instead WRITES a long-lived active state (one photon per write) ==")
    for fuel in ("p-11B", "p-7Li"):
        n = cell.photons_per_fusion_allowed(fuel, 1.0)
        for rate in (1e-11, 1e-7, 1e-3):
            life = 1.0 / (n * rate)
            print(f"  {fuel:6s} pair rate {rate:7.0e} /s  ->  the written state must last {life:9.3g} s"
                  f" ({life / 86400:.3g} days) to break even")


if __name__ == "__main__":
    main()
