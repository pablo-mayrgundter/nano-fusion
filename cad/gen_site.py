#!/usr/bin/env python3
"""Generate L0 reaction-site models (atom-exact) as extended XYZ.

First site: S1, a Pd monovacancy in PdD_x.  Pd sits on an fcc lattice and D on
the octahedral interstitials (rock-salt arrangement).  The six D atoms that
surround the vacancy are kept and tagged; the rest of the D sublattice is
thinned at random (fixed seed) to the loading ratio in the spec.

The structure is UNRELAXED -- ideal lattice positions -- and is meant as the
starting geometry for DFT relaxation, not as a result.

Isotopes: species is the chemical symbol (so standard tools can read the file);
the mass_number column carries the isotope (2 = deuterium, 0 = natural mix).

Usage:  python3 cad/gen_site.py [spec.yaml] [out.xyz] [cells_per_side]
Needs:  PyYAML.
"""
import itertools
import math
import os
import random
import sys

import yaml

FCC = [(0, 0, 0), (0, 0.5, 0.5), (0.5, 0, 0.5), (0.5, 0.5, 0)]
OCT = [(0.5, 0.5, 0.5), (0.5, 0, 0), (0, 0.5, 0), (0, 0, 0.5)]


def mic_distance(p, q, n):
    """Minimum-image distance in units of the lattice constant, cubic box of side n."""
    return math.sqrt(sum(((x - y + n / 2) % n - n / 2) ** 2 for x, y in zip(p, q)))


def build_pdd_vacancy(n, loading_x, seed=0):
    cells = list(itertools.product(range(n), repeat=3))
    pd = [(i + u, j + v, k + w) for i, j, k in cells for u, v, w in FCC]
    d = [(i + u, j + v, k + w) for i, j, k in cells for u, v, w in OCT]
    vacancy = (n // 2, n // 2, n // 2)
    pd.remove(vacancy)
    shell = [p for p in d if mic_distance(p, vacancy, n) < 0.5 + 1e-6]
    others = sorted(p for p in d if p not in shell)
    n_keep = round(loading_x * len(pd)) - len(shell)
    kept = random.Random(seed).sample(others, n_keep)
    atoms = [("Pd", p, 0, "host") for p in pd]
    atoms += [("H", p, 2, "vacancy_shell") for p in shell]
    atoms += [("H", p, 2, "bulk") for p in sorted(kept)]
    return atoms, vacancy, shell


def write_extxyz(path, atoms, a, n, info):
    box = a * n
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as fh:
        fh.write(f"{len(atoms)}\n")
        extra = " ".join(f'{k}="{v}"' for k, v in info.items())
        fh.write(f'Lattice="{box:.5f} 0 0 0 {box:.5f} 0 0 0 {box:.5f}" '
                 f'Properties=species:S:1:pos:R:3:mass_number:I:1:tag:S:1 pbc="T T T" {extra}\n')
        for sym, p, mass_number, tag in atoms:
            x, y, z = (c * a for c in p)
            fh.write(f"{sym:2s} {x:10.5f} {y:10.5f} {z:10.5f} {mass_number:d} {tag}\n")


def main():
    spec_path = sys.argv[1] if len(sys.argv) > 1 else "design/nf-cell-v0.yaml"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "design/sites/S1-PdD-vacancy.xyz"
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    with open(spec_path) as fh:
        site = yaml.safe_load(fh)["site"]
    a = float(site["host"]["a_angstrom"])
    x = float(site["loading_x"]["value"])
    atoms, vacancy, shell = build_pdd_vacancy(n, x)
    n_pd = sum(1 for s in atoms if s[0] == "Pd")
    n_d = len(atoms) - n_pd
    write_extxyz(out_path, atoms, a, n, {
        "site_id": site["id"], "state": "unrelaxed",
        "vacancy_at_angstrom": " ".join(f"{c * a:.5f}" for c in vacancy),
        "loading_D_per_Pd": f"{n_d / n_pd:.3f}",
    })
    shell_dd = min(mic_distance(p, q, n) for p, q in itertools.combinations(shell, 2)) * a
    print(f"wrote {out_path}")
    print(f"  supercell {n}x{n}x{n}, box {a * n:.2f} A, {n_pd} Pd + {n_d} D, D/Pd = {n_d / n_pd:.3f}")
    print(f"  vacancy shell: {len(shell)} D at {0.5 * a:.3f} A from the vacancy; "
          f"nearest D-D in shell {shell_dd:.3f} A (D2 molecule: 0.74 A)")


if __name__ == "__main__":
    main()
