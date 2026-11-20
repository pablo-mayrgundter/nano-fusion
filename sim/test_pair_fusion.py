"""Regression tests for sim/pair_fusion.py and sim/cell_model.py.

Run:  python3 sim/test_pair_fusion.py      (or: pytest sim/)      about 20 seconds
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pair_fusion as pf  # noqa: E402


def test_free_particle_in_a_sphere_is_exact():
    mu, rc = 1835.0, 2.0                                   # no barrier: analytic ground state
    energy, log_psi = pf.ground_state(lambda r: 0.0, mu, r_max=rc)
    assert abs(energy - math.pi ** 2 / (2 * mu * rc ** 2)) < 1e-3 * energy
    assert abs(10 ** log_psi - math.pi / (2 * rc ** 3)) < 2e-3 * math.pi / (2 * rc ** 3)


def test_molecular_binding_energies_match_spectroscopy():
    for pair, d0 in (("D-D", 4.556), ("p-D", 4.514), ("D-T", 4.573)):
        assert abs(pf.rate_molecule(pair)[1] - d0) < 0.003       # eV


def test_d2_fusion_rate_matches_koonin_nauenberg():
    log_rate = pf.rate_molecule("D-D")[0]
    assert abs(log_rate - math.log10(3e-64)) < 0.5               # within a factor of three


def test_heavier_electron_reaches_claimed_rates_at_5_to_10():
    assert -24 < pf.rate_molecule("D-D", 5.0)[0] < -16           # Koonin-Nauenberg's statement
    assert -12 < pf.rate_molecule("D-D", 10.0)[0] < -6
    assert pf.rate_molecule("D-D", 207.0)[0] > 9                 # muonic molecule: fast


def test_nuclear_constant_for_dd():
    assert abs(pf.nuclear_constant("D-D") - 1.5e-16) < 0.1e-16   # cm3/s, as in Koonin-Nauenberg


def test_lattice_sites_are_worse_than_a_molecule():
    assert pf.rate_site("D-D", 285.0, 40.0, 21.6) < pf.rate_molecule("D-D")[0] - 15


def test_cage_rate_rises_as_screening_tightens_and_falls_with_charge():
    assert pf.rate_cage("D-D", 100.0, 1.0) > pf.rate_cage("D-D", 100.0, 5.0) > pf.rate_cage("D-D", 100.0, 20.0)
    at_1pm = [pf.rate_cage(p, 100.0, 1.0) for p in ("D-D", "p-7Li", "p-11B")]
    assert at_1pm[0] > at_1pm[1] > at_1pm[2]


def test_field_coupling_vanishes_for_identical_nuclei():
    assert pf.effective_charge("D-D") == 0.0
    assert abs(pf.effective_charge("p-7Li") - 0.5) < 0.01
    assert abs(pf.effective_charge("p-11B") - 0.5) < 0.01


def test_cell_model_energy_accounting():
    import yaml
    import cell_model as cm
    with open(os.path.join(os.path.dirname(HERE), "design", "nf-cell-v1.yaml")) as fh:
        cell = cm.Cell(yaml.safe_load(fh))
    assert abs(cell.pairs_per_cm3 - 2.5e19) < 1e17
    assert abs(cell.photons_per_fusion_allowed("p-11B", 1.0) - 1.3e5) < 0.02e5
    req = cell.requirements("p-11B", 1.0, q_eng=3.0)
    gross = cell.eta_capture * req["fusion power [W/cm3]"]
    laser_electric = (req["fusion power [W/cm3]"] / (8.68e6 * cm.EV) * req["photons allowed per fusion"]
                      * cell.photon_j / (cell.eta_laser * cell.eta_dist))
    assert abs(gross - laser_electric - 1.0) < 1e-6              # net = out - in
    assert abs(gross / laser_electric - 3.0) < 1e-6              # the stated gain
    stored, power, rate = cell.drive_cost("p-11B", 1.0, 40.0, 10.0)
    assert 1.5 < stored < 3.0 and 0.5e-4 < power < 2e-4 and rate > 1e9


def test_beam_route_numbers():
    import beam_route as br
    assert 80 < br.scattering_per_fusion(653.0, 10.0) < 110          # rad^2 per fusion mean free path
    assert 0.09 < br.bare_ion_yield(2000.0, 10.0) < 0.15             # fusion probability, proton stopping
    assert br.bare_ion_yield(2000.0, 10.0) * br.E_FUS_PB11 / 2e6 < 1.0   # below break-even if it just stops


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("ok  ", t.__name__)
    print(f"{len(tests)} passed")
