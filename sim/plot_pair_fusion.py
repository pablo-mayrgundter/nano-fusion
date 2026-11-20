#!/usr/bin/env python3
"""Draw docs/figures/pair-fusion-requirements.svg from the cage model in pair_fusion.py.

The curves are cached in sim/pair-fusion-curves.csv, which is also the table view of the
chart.  Pass --recompute to rebuild the cache (about a minute).
Standard library only.   Run:  python3 sim/plot_pair_fusion.py
"""
import csv
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pair_fusion as pf  # noqa: E402

CSV_PATH = os.path.join(HERE, "pair-fusion-curves.csv")
SVG_PATH = os.path.join(os.path.dirname(HERE), "docs", "figures", "pair-fusion-requirements.svg")
FUELS = ("D-D", "p-6Li", "p-7Li", "p-11B")
PRETTY = {"D-D": "D–D", "p-6Li": "p–⁶Li", "p-7Li": "p–⁷Li", "p-11B": "p–¹¹B"}
CAGE_PM = 100.0
BATTERY = (2e-11, 2e-7)                # per-pair rates of the v1 sensor and handheld tiers
REPORTED_EV = (300.0, 1700.0)          # screening energies reported for deuterium in metals
SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def curves(recompute=False):
    if os.path.exists(CSV_PATH) and not recompute:
        with open(CSV_PATH) as fh:
            rows = list(csv.DictReader(r for r in fh if not r.startswith("#")))
        return [float(r["screening_length_pm"]) for r in rows], {f: [float(r[f]) for r in rows] for f in FUELS}
    lams = [0.25 * (60.0 / 0.25) ** (i / 23.0) for i in range(24)]
    data = {f: [pf.rate_cage(f, CAGE_PM, lam) for lam in lams] for f in FUELS}
    with open(CSV_PATH, "w", newline="") as fh:
        fh.write("# log10 of the fusion rate per pair per second, two nuclei in a 100 pm cage (pair_fusion.py model c)\n")
        w = csv.writer(fh)
        w.writerow(["screening_length_pm"] + list(FUELS))
        for i, lam in enumerate(lams):
            w.writerow([f"{lam:.4g}"] + [f"{data[f][i]:.2f}" for f in FUELS])
    return lams, data


def power10(n):
    return "10" + str(n).translate(SUP)


def build_svg(lams, data):
    width, height = 920, 640
    left, top, plot_w, plot_h = 84, 126, 640, 400
    x_lo, x_hi, y_lo, y_hi = math.log10(0.2), math.log10(60.0), -110.0, 15.0

    def sx(lam):
        return left + (math.log10(lam) - x_lo) / (x_hi - x_lo) * plot_w

    def sy(v):
        return top + (y_hi - v) / (y_hi - y_lo) * plot_h

    def lam_at(fuel, v):                       # screening length where a curve reaches log-rate v
        ys = data[fuel]
        for i in range(len(lams) - 1):
            if (ys[i] - v) * (ys[i + 1] - v) <= 0:
                t = (v - ys[i]) / (ys[i + 1] - ys[i])
                return lams[i] * (lams[i + 1] / lams[i]) ** t
        return None

    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" '
             f'height="{height}" role="img" aria-labelledby="pf-title pf-desc">')
    o.append('<title id="pf-title">What a resting fuel pair needs</title>')
    o.append('<desc id="pf-desc">Fusion rate per pair per second against the screening length of the '
             'surrounding electrons, for D-D, p-6Li, p-7Li and p-11B. The rate rises by tens of orders of '
             'magnitude as the screening length shrinks from 53 picometres toward 0.3. D-D reaches the range '
             'a battery needs near 2 picometres; the lithium fuels near 0.8 and boron near 0.5.</desc>')
    o.append('''<style>
  svg { --surface:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#898781; --grid:#e1e0d9; --axis:#c3c2b7;
        --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --s4:#eda100; --wash:#52514e;
        font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }
  @media (prefers-color-scheme: dark) {
    svg { --surface:#1a1a19; --ink:#f0efec; --ink2:#c3c2b7; --muted:#898781; --grid:#2c2c2a; --axis:#383835;
          --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; --wash:#c3c2b7; } }
  .t { fill: var(--ink); } .t2 { fill: var(--ink2); } .tm { fill: var(--muted); }
  .grid { stroke: var(--grid); stroke-width: 1; } .axis { stroke: var(--axis); stroke-width: 1; }
  .line { fill: none; stroke-width: 2; stroke-linejoin: round; stroke-linecap: round; }
  .tick { font-size: 11px; font-variant-numeric: tabular-nums; }
</style>''')
    o.append(f'<rect width="{width}" height="{height}" fill="var(--surface)"/>')
    o.append('<text x="24" y="34" class="t" font-size="17" font-weight="600">What a resting fuel pair needs</text>')
    o.append('<text x="24" y="54" class="t2" font-size="12.5">Fusion rate of two nuclei sharing a 100 pm cage, '
             'against how tightly the surrounding electrons screen them.</text>')
    lx = 24                                                       # legend
    for k, fuel in enumerate(FUELS):
        o.append(f'<line x1="{lx}" y1="78" x2="{lx + 22}" y2="78" class="line" stroke="var(--s{k + 1})"/>')
        o.append(f'<text x="{lx + 28}" y="82" class="t2" font-size="12.5">{PRETTY[fuel]}</text>')
        lx += 92

    # grid and axes
    for v in range(-100, 1, 20):
        o.append(f'<line x1="{left}" y1="{sy(v):.1f}" x2="{left + plot_w}" y2="{sy(v):.1f}" class="grid"/>')
        o.append(f'<text x="{left - 8}" y="{sy(v) + 4:.1f}" text-anchor="end" class="tm tick">{power10(v)}</text>')
    for lam in (0.2, 0.5, 1, 2, 5, 10, 20, 50):
        o.append(f'<line x1="{sx(lam):.1f}" y1="{top}" x2="{sx(lam):.1f}" y2="{top + plot_h}" class="grid"/>')
        o.append(f'<text x="{sx(lam):.1f}" y="{top + plot_h + 18}" text-anchor="middle" class="tm tick">{lam:g}</text>')
    o.append(f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" class="axis"/>')
    o.append(f'<text x="{left + plot_w / 2:.0f}" y="{top + plot_h + 42}" text-anchor="middle" class="t2" '
             f'font-size="12.5">Screening length of the electrons around the pair, picometres (log scale)</text>')
    o.append(f'<text x="{left - 58}" y="{top - 12}" class="t2" font-size="12.5">Fusions per pair per second (log scale)</text>')

    # reference washes: the reported screening range for deuterium, and what a battery needs
    lam_hi, lam_lo = (27.211386 * 52.9177 / e for e in REPORTED_EV)       # 4.8 pm and 0.85 pm
    o.append(f'<rect x="{sx(lam_lo):.1f}" y="{top}" width="{sx(lam_hi) - sx(lam_lo):.1f}" height="{plot_h}" '
             f'fill="var(--wash)" opacity="0.07"/>')
    o.append(f'<text x="{sx(lam_lo) + 6:.1f}" y="{top + 16}" class="t2" font-size="11.5">reported for deuterium</text>')
    o.append(f'<text x="{sx(lam_lo) + 6:.1f}" y="{top + 30}" class="t2" font-size="11.5">in metals, 0.3–1.7 keV</text>')
    o.append(f'<text x="{sx(lam_lo) + 6:.1f}" y="{top + 44}" class="tm" font-size="11">(beam experiments)</text>')
    b_lo, b_hi = (math.log10(v) for v in BATTERY)
    o.append(f'<rect x="{left}" y="{sy(b_hi):.1f}" width="{plot_w}" height="{sy(b_lo) - sy(b_hi):.1f}" '
             f'fill="var(--wash)" opacity="0.16"/>')
    bx = left + plot_w + 10
    o.append(f'<text x="{bx}" y="{sy(b_hi) + 1:.1f}" class="t" font-size="12" font-weight="600">what a battery needs</text>')
    o.append(f'<text x="{bx}" y="{sy(b_hi) + 16:.1f}" class="t2" font-size="11.5">{power10(-11)} to {power10(-7)} per second</text>')
    for lam, label, anchor, dx, ly in ((0.256, "muon orbit, 0.26 pm", "start", 5, top + plot_h - 8),
                                       (52.9, "electron orbit, 53 pm", "end", -5, top + 16)):
        o.append(f'<line x1="{sx(lam):.1f}" y1="{top}" x2="{sx(lam):.1f}" y2="{top + plot_h}" class="axis"/>')
        o.append(f'<text x="{sx(lam) + dx:.1f}" y="{ly}" text-anchor="{anchor}" class="tm" '
                 f'font-size="11">{label}</text>')

    # the four curves
    o.append(f'<clipPath id="pf-clip"><rect x="{left}" y="{top}" width="{plot_w}" height="{plot_h}"/></clipPath>')
    for k, fuel in enumerate(FUELS):
        pts = " ".join(f"{sx(lam):.1f},{sy(v):.1f}" for lam, v in zip(lams, data[fuel]))
        o.append(f'<polyline points="{pts}" class="line" stroke="var(--s{k + 1})" clip-path="url(#pf-clip)"/>')
    # direct labels, one per curve, beside the line
    for fuel, v, side in (("p-11B", -88.0, "end"), ("p-7Li", -62.0, "end"), ("p-6Li", -42.0, "start"), ("D-D", -22.0, "start")):
        lam = lam_at(fuel, v)
        dx = 9 if side == "start" else -9
        o.append(f'<text x="{sx(lam) + dx:.1f}" y="{sy(v) + 4:.1f}" text-anchor="{side}" class="t" font-size="12.5" '
                 f'font-weight="600">{PRETTY[fuel]}</text>')
    # the one measured-physics anchor: the D2 molecule as it is
    d2 = pf.rate_molecule("D-D")[0]
    lam_d2 = lam_at("D-D", d2)
    o.append(f'<circle cx="{sx(lam_d2):.1f}" cy="{sy(d2):.1f}" r="5" fill="var(--s1)" stroke="var(--surface)" stroke-width="2"/>')
    o.append(f'<text x="{sx(lam_d2) + 12:.1f}" y="{sy(d2) - 22:.1f}" class="t" font-size="12" font-weight="600">'
             f'D₂ molecule as it is</text>')
    o.append(f'<text x="{sx(lam_d2) + 12:.1f}" y="{sy(d2) - 7:.1f}" class="t2" font-size="11.5">'
             f'2 × {power10(-64)} per second</text>')
    o.append(f'<text x="24" y="{height - 30}" class="tm" font-size="11">Model: Coulomb repulsion screened as '
             f'exp(−r/λ); sim/pair_fusion.py, model c. Values: sim/pair-fusion-curves.csv.</text>')
    o.append(f'<text x="24" y="{height - 14}" class="tm" font-size="11">The beam-experiment range is not known '
             f'to apply to a pair at rest; that is the open question.</text>')
    o.append("</svg>")
    return "\n".join(o)


def main():
    lams, data = curves("--recompute" in sys.argv)
    os.makedirs(os.path.dirname(SVG_PATH), exist_ok=True)
    with open(SVG_PATH, "w") as fh:
        fh.write(build_svg(lams, data))
    print("wrote", os.path.relpath(SVG_PATH, os.path.dirname(HERE)))


if __name__ == "__main__":
    main()
