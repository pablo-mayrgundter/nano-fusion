"""Regression tests pinning sim/baseline.py to published values.

Run:  python3 sim/test_baseline.py      (or: pytest sim/)
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import baseline as b  # noqa: E402


def close(a, ref, rel):
    return abs(a - ref) <= rel * abs(ref)


def test_gamow_constants():
    assert close(b.gamow_constant(1, 1, b.M_D, b.M_D), 31.3970, 1e-3)   # Bosch-Hale
    assert close(b.gamow_constant(1, 1, b.M_D, b.M_T), 34.3827, 1e-3)   # Bosch-Hale
    assert close(b.B_G_PB11, 150.3, 2e-3)                               # Nevins-Swain


def test_cross_sections_match_tables():
    assert close(b.sigma("DT", 10.0), 2.702e-2, 5e-3)     # Bosch-Hale Table VIII
    assert close(b.sigma("DDp", 10.0), 2.812e-4, 5e-3)
    assert 1.1 < b.sigma("pB11", 600.0) < 1.3             # ~1.2 b peak


def test_pb11_fit_is_continuous_at_range_joins():
    for e in (400.0, 642.0):
        assert close(b.s_factor("pB11", e - 1e-6), b.s_factor("pB11", e + 1e-6), 0.02)


def test_hydrogen_stopping_matches_pstar():
    mev_cm2_g = b.stop_in_hydrogen(1000.0) * 6.022e23 / 1.008 / 1e6
    assert close(mev_cm2_g, 683.0, 0.02)


def test_screening_is_negligible_at_high_energy_and_huge_at_low():
    assert b.screening_enhancement("DDp", 50.0, 1.0) < 1.05
    assert b.screening_enhancement("DDp", 1.0, 1.0) > 1e3


def test_gain_ceiling_for_cold_targets():
    f_dt, e_dt = b.best_fom("D->T")
    f_pb, e_pb = b.best_fom("p->11B")
    assert 1.0e-2 < f_dt < 2.0e-2 and 90 < e_dt < 130
    assert 1.5e-3 < f_pb < 2.5e-3 and 600 < e_pb < 700
    # thick-target gain is always below the ceiling
    assert b.thick_target("D->T", 200.0)[1] < f_dt
    assert b.thick_target("p->11B", 700.0)[1] < f_pb


def test_electron_free_zone_lifts_the_ceiling_by_about_1000():
    for name, e in (("D->T", 108.0), ("p->11B", 653.0)):
        gain = b.electron_free_fom(name, e) / b.figure_of_merit(name, e)
        assert 300 < gain < 3000


def test_single_photon_field_scaling():
    assert close(b.single_photon_field(2.0, 1.0), 4.25, 0.01)
    assert close(b.single_photon_field(2.0, 4.0) * 2, b.single_photon_field(2.0, 1.0), 1e-9)


def test_e1_budget_inputs_are_sane():
    import e1_budget as e1
    assert 8e-15 < e1.stop_in_pd(10.0) < 14e-15           # slow protons in Pd: ~10e-15 eV cm2
    thick = e1.proton_yield(5.0, 0.8)
    thin = e1.proton_yield(5.0, 0.8, thickness_nm=10.0)
    assert 0.0 < thin < thick                              # a 10 nm layer cannot beat a thick target
    assert e1.proton_yield(10.0, 0.8) > 10 * thick         # steep energy dependence
    assert e1.proton_yield(5.0, 1.0) > thick               # more screening, more yield


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("ok  ", t.__name__)
    print(f"{len(tests)} passed")
