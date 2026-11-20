#!/usr/bin/env python3
"""Draw the "what a resting fuel pair needs" chart from the cage model in pair_fusion.py.

Outputs
  docs/figures/pair-fusion-requirements.svg   standalone, for the Markdown docs
  site/fig/pair-chart-wide.svg                inline fragment for the site, desktop
  site/fig/pair-chart-compact.svg             inline fragment for the site, phones
  site/fig/pair-chart-table.html              the table view of the same data
  site/fig/pair-chart-data.json               what the hover layer reads

The curves are cached in sim/pair-fusion-curves.csv.  Pass --recompute to rebuild the cache
(about fifteen seconds).  Standard library only.   Run:  python3 sim/plot_pair_fusion.py
"""
import csv
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import pair_fusion as pf  # noqa: E402

CSV_PATH = os.path.join(HERE, "pair-fusion-curves.csv")
DOC_SVG = os.path.join(ROOT, "docs", "figures", "pair-fusion-requirements.svg")
SITE_FIG = os.path.join(ROOT, "site", "fig")
FUELS = ("D-D", "p-6Li", "p-7Li", "p-11B")
PRETTY = {"D-D": "D–D", "p-6Li": "p–⁶Li", "p-7Li": "p–⁷Li", "p-11B": "p–¹¹B"}
CAGE_PM = 100.0
BATTERY = (2e-11, 2e-7)                # per-pair rates of the v1 sensor and handheld tiers
REPORTED_EV = (300.0, 1700.0)          # screening energies reported for deuterium in metals
SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
X_LO, X_HI, Y_LO, Y_HI = math.log10(0.2), math.log10(60.0), -110.0, 15.0

STANDALONE_STYLE = '''<style>
  svg { --pf-surface:#fcfcfb; --pf-ink:#0b0b0b; --pf-ink2:#52514e; --pf-muted:#898781; --pf-grid:#e1e0d9;
        --pf-axis:#c3c2b7; --pf-s1:#2a78d6; --pf-s2:#eb6834; --pf-s3:#1baf7a; --pf-s4:#eda100; --pf-wash:#52514e;
        font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }
  @media (prefers-color-scheme: dark) {
    svg { --pf-surface:#1a1a19; --pf-ink:#f0efec; --pf-ink2:#c3c2b7; --pf-muted:#898781; --pf-grid:#2c2c2a;
          --pf-axis:#383835; --pf-s1:#3987e5; --pf-s2:#d95926; --pf-s3:#199e70; --pf-s4:#c98500; --pf-wash:#c3c2b7; } }
  .pf-t { fill: var(--pf-ink); } .pf-t2 { fill: var(--pf-ink2); } .pf-tm { fill: var(--pf-muted); }
  .pf-grid { stroke: var(--pf-grid); stroke-width: 1; } .pf-axis { stroke: var(--pf-axis); stroke-width: 1; }
  .pf-line { fill: none; stroke-width: 2; stroke-linejoin: round; stroke-linecap: round; }
  .pf-tick { font-size: 11px; font-variant-numeric: tabular-nums; }
  .pf-halo { paint-order: stroke; stroke: var(--pf-surface); stroke-width: 4px; stroke-linejoin: round; }
</style>'''


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


def interp(lams, ys, lam):
    for i in range(len(lams) - 1):
        if lams[i] <= lam <= lams[i + 1]:
            t = math.log(lam / lams[i]) / math.log(lams[i + 1] / lams[i])
            return ys[i] + t * (ys[i + 1] - ys[i])
    return ys[0] if lam < lams[0] else ys[-1]


def plot_body(lams, data, d2_rate, left, top, plot_w, plot_h, compact, uid):
    """The plot itself: grid, reference washes, curves, direct labels."""
    def sx(lam):
        return left + (math.log10(lam) - X_LO) / (X_HI - X_LO) * plot_w

    def sy(v):
        return top + (Y_HI - v) / (Y_HI - Y_LO) * plot_h

    def lam_at(fuel, v):
        ys = data[fuel]
        for i in range(len(lams) - 1):
            if (ys[i] - v) * (ys[i + 1] - v) <= 0:
                t = (v - ys[i]) / (ys[i + 1] - ys[i])
                return lams[i] * (lams[i + 1] / lams[i]) ** t
        return None

    o = []
    fs = 11 if compact else 11.5
    for v in range(-100, 1, 20):
        o.append(f'<line x1="{left}" y1="{sy(v):.1f}" x2="{left + plot_w}" y2="{sy(v):.1f}" class="pf-grid"/>')
        o.append(f'<text x="{left - 7}" y="{sy(v) + 4:.1f}" text-anchor="end" class="pf-tm pf-tick">{power10(v)}</text>')
    for lam in (0.2, 0.5, 1, 2, 5, 10, 20, 50):
        o.append(f'<line x1="{sx(lam):.1f}" y1="{top}" x2="{sx(lam):.1f}" y2="{top + plot_h}" class="pf-grid"/>')
        o.append(f'<text x="{sx(lam):.1f}" y="{top + plot_h + 17}" text-anchor="middle" class="pf-tm pf-tick">{lam:g}</text>')
    o.append(f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" class="pf-axis"/>')
    x_title = ("Screening length, picometres (log scale)" if compact else
               "Screening length of the electrons around the pair, picometres (log scale)")
    o.append(f'<text x="{left + plot_w / 2:.0f}" y="{top + plot_h + 38}" text-anchor="middle" class="pf-t2" '
             f'font-size="12">{x_title}</text>')
    o.append(f'<text x="{left - (40 if compact else 58)}" y="{top - 11}" class="pf-t2" font-size="12">'
             f'Fusions per pair per second (log scale)</text>')

    # what beam experiments report for deuterium, as a screening length
    lam_hi, lam_lo = (27.211386 * 52.9177 / e for e in REPORTED_EV)
    o.append(f'<rect x="{sx(lam_lo):.1f}" y="{top}" width="{sx(lam_hi) - sx(lam_lo):.1f}" height="{plot_h}" '
             f'fill="var(--pf-wash)" opacity="0.07"/>')
    wx = sx(lam_lo) + 5
    for k, line in enumerate(("reported for", "deuterium in metals,", "0.3–1.7 keV") if compact else
                             ("reported for deuterium", "in metals, 0.3–1.7 keV")):
        o.append(f'<text x="{wx:.1f}" y="{top + 15 + 13.5 * k:.1f}" class="pf-t2" font-size="{fs}">{line}</text>')
    o.append(f'<text x="{wx:.1f}" y="{top + 15 + 13.5 * (3 if compact else 2):.1f}" class="pf-tm" '
             f'font-size="{fs - 0.5}">(beam experiments)</text>')
    # what a battery needs
    b_lo, b_hi = (math.log10(v) for v in BATTERY)
    o.append(f'<rect x="{left}" y="{sy(b_hi):.1f}" width="{plot_w}" height="{sy(b_lo) - sy(b_hi):.1f}" '
             f'fill="var(--pf-wash)" opacity="0.17"/>')
    if compact:
        o.append(f'<text x="{left + plot_w - 5}" y="{sy(b_lo) + 15:.1f}" text-anchor="end" class="pf-t" '
                 f'font-size="{fs}" font-weight="600">what a battery needs</text>')
    else:
        bx = left + plot_w + 10
        o.append(f'<text x="{bx}" y="{sy(b_hi) + 1:.1f}" class="pf-t" font-size="12" font-weight="600">'
                 f'what a battery needs</text>')
        o.append(f'<text x="{bx}" y="{sy(b_hi) + 16:.1f}" class="pf-t2" font-size="11.5">'
                 f'{power10(-11)} to {power10(-7)} per second</text>')
    # the two orbit sizes, for scale
    o.append(f'<line x1="{sx(52.9):.1f}" y1="{top}" x2="{sx(52.9):.1f}" y2="{top + plot_h}" class="pf-axis"/>')
    o.append(f'<text x="{sx(52.9) - 5:.1f}" y="{top + 15}" text-anchor="end" class="pf-tm" font-size="{fs - 0.5}">'
             f'electron orbit, 53 pm</text>')
    o.append(f'<line x1="{sx(0.256):.1f}" y1="{top}" x2="{sx(0.256):.1f}" y2="{top + plot_h}" class="pf-axis"/>')
    my = top + plot_h - (36 if compact else 22)
    muon = (("muon orbit, 0.26 pm:", "a real route for", "hydrogen pairs only") if compact else
            ("muon orbit, 0.26 pm: a real route", "for hydrogen pairs only"))
    for k, line in enumerate(muon):
        cls, weight = ("pf-t2", ' font-weight="600"') if k == 0 else ("pf-tm", "")
        o.append(f'<text x="{sx(0.256) + 5:.1f}" y="{my + 13.5 * k:.1f}" class="{cls}" font-size="{fs - 0.5}"{weight}>'
                 f'{line}</text>')

    o.append(f'<clipPath id="{uid}-clip"><rect x="{left}" y="{top}" width="{plot_w}" height="{plot_h}"/></clipPath>')
    for k, fuel in enumerate(FUELS):
        pts = " ".join(f"{sx(lam):.1f},{sy(v):.1f}" for lam, v in zip(lams, data[fuel]))
        o.append(f'<polyline points="{pts}" class="pf-line" stroke="var(--pf-s{k + 1})" clip-path="url(#{uid}-clip)"/>')
    spots = ((("p-11B", -92.0, "end"), ("p-7Li", -66.0, "end"), ("p-6Li", -44.0, "start"), ("D-D", -24.0, "start"))
             if compact else
             (("p-11B", -88.0, "end"), ("p-7Li", -62.0, "end"), ("p-6Li", -42.0, "start"), ("D-D", -22.0, "start")))
    for fuel, v, side in spots:
        lam = lam_at(fuel, v)
        dx = 8 if side == "start" else -8
        o.append(f'<text x="{sx(lam) + dx:.1f}" y="{sy(v) + 4:.1f}" text-anchor="{side}" class="pf-t pf-halo" '
                 f'font-size="12.5" font-weight="600">{PRETTY[fuel]}</text>')
    lam_d2 = lam_at("D-D", d2_rate)
    o.append(f'<circle cx="{sx(lam_d2):.1f}" cy="{sy(d2_rate):.1f}" r="5" fill="var(--pf-s1)" '
             f'stroke="var(--pf-surface)" stroke-width="2"/>')
    if compact:                                       # above and to the right, where the curve has already fallen away
        xr, yd = left + plot_w - 4, sy(d2_rate)
        o.append(f'<line x1="{xr - 30:.1f}" y1="{yd - 31:.1f}" x2="{sx(lam_d2) + 4:.1f}" y2="{yd - 6:.1f}" class="pf-axis"/>')
        o.append(f'<text x="{xr:.1f}" y="{yd - 51:.1f}" text-anchor="end" class="pf-t pf-halo" '
                 f'font-size="{fs}" font-weight="600">D₂ as it is:</text>')
        o.append(f'<text x="{xr:.1f}" y="{yd - 37:.1f}" text-anchor="end" class="pf-t2 pf-halo" '
                 f'font-size="{fs}">2 × {power10(-64)}</text>')
    else:
        o.append(f'<text x="{sx(lam_d2) + 12:.1f}" y="{sy(d2_rate) - 22:.1f}" class="pf-t pf-halo" font-size="12" '
                 f'font-weight="600">D₂ molecule as it is</text>')
        o.append(f'<text x="{sx(lam_d2) + 12:.1f}" y="{sy(d2_rate) - 7:.1f}" class="pf-t2 pf-halo" font-size="11.5">'
                 f'2 × {power10(-64)} per second</text>')
    return "\n".join(o)


DESC = ("Fusion rate per pair per second against the screening length of the surrounding electrons, for D-D, "
        "p-6Li, p-7Li and p-11B. The rate rises by tens of orders of magnitude as the screening length shrinks "
        "from 53 picometres toward 0.3. D-D reaches the range a battery needs near 1 to 1.5 picometres, the "
        "lithium fuels near 0.5 and boron near 0.4. A muon gives 0.26 picometres for hydrogen pairs only.")


def standalone(lams, data, d2_rate):
    width, height, left, top, plot_w, plot_h = 920, 656, 84, 126, 640, 400
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
         f'role="img" aria-labelledby="pf-title pf-desc">',
         '<title id="pf-title">What a resting fuel pair needs</title>', f'<desc id="pf-desc">{DESC}</desc>',
         STANDALONE_STYLE, f'<rect width="{width}" height="{height}" fill="var(--pf-surface)"/>',
         '<text x="24" y="34" class="pf-t" font-size="17" font-weight="600">What a resting fuel pair needs</text>',
         '<text x="24" y="54" class="pf-t2" font-size="12.5">Fusion rate of two nuclei sharing a 100 pm cage, '
         'against how tightly the surrounding electrons screen them.</text>']
    lx = 24
    for k, fuel in enumerate(FUELS):
        o.append(f'<line x1="{lx}" y1="78" x2="{lx + 22}" y2="78" class="pf-line" stroke="var(--pf-s{k + 1})"/>')
        o.append(f'<text x="{lx + 28}" y="82" class="pf-t2" font-size="12.5">{PRETTY[fuel]}</text>')
        lx += 92
    o.append(plot_body(lams, data, d2_rate, left, top, plot_w, plot_h, False, "pf"))
    notes = ("Model: Coulomb repulsion screened as exp(−r/λ); sim/pair_fusion.py, model c. Values: sim/pair-fusion-curves.csv.",
             "The beam-experiment range is not known to apply to a pair at rest; that is the open question.",
             "One muon screens one charge. It gives 0.26 pm for hydrogen pairs; for lithium and boron no single particle does.")
    for k, line in enumerate(notes):
        o.append(f'<text x="24" y="{height - 46 + 16 * k}" class="pf-tm" font-size="11">{line}</text>')
    o.append("</svg>")
    return "\n".join(o)


def fragment(lams, data, d2_rate, compact):
    if compact:
        width, height, left, top, plot_w, plot_h = 400, 440, 52, 30, 338, 350
    else:
        width, height, left, top, plot_w, plot_h = 880, 470, 76, 30, 620, 380
    uid = "pfc" if compact else "pfw"
    geom = (f'data-left="{left}" data-top="{top}" data-w="{plot_w}" data-h="{plot_h}" data-xlo="{X_LO:.5f}" '
            f'data-xhi="{X_HI:.5f}" data-ylo="{Y_LO}" data-yhi="{Y_HI}" data-vw="{width}" data-vh="{height}"')
    return (f'<svg class="pf-chart" viewBox="0 0 {width} {height}" role="img" tabindex="0" {geom} '
            f'aria-label="{DESC}">\n' + plot_body(lams, data, d2_rate, left, top, plot_w, plot_h, compact, uid)
            + '\n<line class="pf-cross" x1="0" y1="0" x2="0" y2="0" visibility="hidden"/>\n</svg>')


def table_html(lams, data):
    rows = ['<table class="data"><caption>Fusions per pair per second, as a power of ten</caption>',
            "<thead><tr><th scope=\"col\">Screening length</th>"
            + "".join(f'<th scope="col">{PRETTY[f]}</th>' for f in FUELS) + "</tr></thead><tbody>"]
    for lam in (0.25, 0.5, 1.0, 1.5, 2.0, 5.0, 10.0, 20.0, 50.0):
        cells = "".join(f"<td>{power10(round(interp(lams, data[f], lam)))}</td>" for f in FUELS)
        rows.append(f'<tr><th scope="row">{lam:g} pm</th>{cells}</tr>')
    rows.append("</tbody></table>")
    return "\n".join(rows)


def main():
    lams, data = curves("--recompute" in sys.argv)
    d2_rate = pf.rate_molecule("D-D")[0]
    os.makedirs(os.path.dirname(DOC_SVG), exist_ok=True)
    os.makedirs(SITE_FIG, exist_ok=True)
    outputs = {
        DOC_SVG: standalone(lams, data, d2_rate),
        os.path.join(SITE_FIG, "pair-chart-wide.svg"): fragment(lams, data, d2_rate, False),
        os.path.join(SITE_FIG, "pair-chart-compact.svg"): fragment(lams, data, d2_rate, True),
        os.path.join(SITE_FIG, "pair-chart-table.html"): table_html(lams, data),
        os.path.join(SITE_FIG, "pair-chart-data.json"): json.dumps(
            {"lams": [round(v, 4) for v in lams], "fuels": [PRETTY[f] for f in FUELS],
             "series": [[round(v, 2) for v in data[f]] for f in FUELS]}),
    }
    for path, text in outputs.items():
        with open(path, "w") as fh:
            fh.write(text + "\n")
        print("wrote", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    main()
