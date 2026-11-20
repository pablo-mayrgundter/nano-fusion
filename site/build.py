#!/usr/bin/env python3
"""Build the NanoFusion site: index.html and onepager.html at the repository root.

    python3 sim/plot_pair_fusion.py     # only if the site model changed: refreshes site/fig/
    python3 site/build.py               # assemble the pages
    node site/snap.js                   # optional: re-render site/onepager.png and site/og.png (Playwright)
    python3 site/build.py --shrink      # optional: palette-compress site/onepager.png (Pillow)

The pages are static HTML with inline SVG, served by GitHub Pages from the repository root.
Sources:  site/src/*.html  the text          site/figures.py  the drawings
          site/fig/        the chart         site/site.css, site/site.js

Before writing anything the build checks that every number the pages rely on is still in the saved
simulator outputs (CHECKS below), so the site cannot drift from the models unnoticed.
Standard library only.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import figures  # noqa: E402

REPO = "https://github.com/pablo-mayrgundter/nano-fusion"
GH = REPO + "/blob/HEAD/"
URL = "https://pablo-mayrgundter.github.io/nano-fusion/"

# (file, text that must be in it, what the site says on the strength of it).  Runs of spaces are loose.
CHECKS = (
    ("sim/pair-fusion-output.txt", "fusion rate = 2.0e-64 /s", "a D2 pair fuses at 2 x 10^-64 per second"),
    ("sim/pair-fusion-output.txt", "Koonin & Nauenberg 1989 for D2: 3e-64 /s", "published value 3 x 10^-64"),
    ("sim/pair-fusion-output.txt", "D0 = 4.556 eV (measured 4.556)", "binding energy to 1 meV"),
    ("sim/pair-fusion-output.txt", "match the D2 molecule: 21.6 pm", "22 pm of screening in a molecule"),
    ("sim/pair-fusion-output.txt", "lam = 21.6 pm: 10^-88 /s", "neighbouring PdD sites: 10^-88"),
    ("sim/pair-fusion-output.txt", "207 0.36 10723 11.6", "muonic D2: 4 x 10^11 per second"),
    ("sim/pair-fusion-output.txt", "muon Bohr radius 0.256 pm", "a muon's orbit is 0.26 pm"),
    ("sim/pair-fusion-output.txt", "p-6Li 1 W/cm3 0.64 6.72 0.43", "light pushes p-6Li with 0.43 e"),
    ("sim/pair-fusion-output.txt", "p-11B 1 W/cm3 0.42 16.96 0.50", "light pushes p-11B with 0.50 e"),
    ("sim/pair-fusion-output.txt", "D-D 1 W/cm3 1.50 0.96 0.00", "light does not push D-D"),
    ("sim/cue-ball-output.txt", "best is level 18 at 10^-55.3: 8 of the ~53 orders", "vibrational ladder: 10^-55, 8 of 53 orders"),
    ("sim/cue-ball-output.txt", "a disc of radius 6.2 fm", "the pocket: 6 fm in radius"),
    ("sim/cue-ball-output.txt", "boron in a stiff covalent lattice 4.2 pm", "the nucleus jitters +-4.2 pm"),
    ("sim/cue-ball-output.txt", "jitter 4154 fm against a 6.2 fm pocket", "jitter 670 times the pocket"),
    ("sim/cue-ball-output.txt", "hits with probability 1.1e-06", "a perfect shot hits once in a million"),
    ("sim/cue-ball-output.txt", "pinning a boron nucleus to 6.2 fm would take 25 keV", "pinning takes 25 keV"),
    ("sim/cue-ball-output.txt", "a chemical bond supplies about 55 meV", "a bond supplies 55 meV"),
    ("sim/cue-ball-output.txt", "hit probability 3.1e-09, energy lost 14 eV", "14 eV per layer, one hit in 3 x 10^8"),
    ("sim/cue-ball-output.txt", "(359 times better)", "aimed is 360 times better"),
    ("sim/cue-ball-output.txt", "14 eV per shot -> gain 0.69", "aimed gain up to 0.7"),
    ("sim/cue-ball-output.txt", "110 eV per shot -> gain 0.09", "aimed gain from 0.1"),
    ("sim/cue-ball-output.txt", "5.7 fm over 100 nm of flight", "a photon steers 6 fm per 100 nm"),
    ("sim/cue-ball-output.txt", "head-on fusion probability ~1", "head-on they fuse almost every time"),
    ("sim/cue-ball-output.txt", "recoils with 1.1e-09 eV", "photon recoil 10^-9 eV"),
    ("sim/cue-ball-output.txt", "a field of 134953 V/nm", "a knock needs 135,000 V/nm"),
    ("sim/beam-route-output.txt", "10^ -26.9 /s", "caged D-D with 0.3 keV: 10^-27"),
    ("sim/beam-route-output.txt", "10^ -5.0 /s", "caged D-D with 1.7 keV: 10^-5"),
    ("sim/beam-route-output.txt", "10^ -79.3 /s", "p-7Li with reported screening: 10^-79"),
    ("sim/beam-route-output.txt", "10^ -43.9 /s", "p-7Li with reported screening: 10^-44"),
    ("sim/beam-route-output.txt", "10^ -135.3 /s", "p-11B with reported screening: 10^-135"),
    ("sim/beam-route-output.txt", "F = 1.9e-03 at 653 keV", "0.19 % of beam energy returns from solid boron"),
    ("sim/beam-route-output.txt", "10 nm trap: F = 1.58", "bare nuclei: up to 1.6"),
    ("sim/beam-route-output.txt", "1000 nm trap: F = 1.20", "bare nuclei: from 1.2"),
    ("sim/beam-route-output.txt", "direction randomised ~92 times per fusion", "scatters about a hundred times per fusion"),
    ("sim/beam-route-output.txt", "lost-ion energy recovery needed 99.90 %", "recycling at up to 99.9 %"),
    ("sim/beam-route-output.txt", "lost-ion energy recovery needed 89.85 %", "recycling at 90 %"),
    ("sim/beam-route-output.txt", "about 11 mSv per hour (public limit: 1 mSv per year)", "D-D dose at 30 cm"),
    ("sim/cell-model-output.txt", "500 layers per cm, 2.50e+19 pairs per cm3 of stack", "2.5 x 10^19 pairs per cm3"),
    ("sim/cell-model-output.txt", "p-11B break-even 1.3e+05 for electricity out = 3 x in 4.34e+04", "43,000 photons per fusion"),
    ("sim/cell-model-output.txt", "rate per fuel pair [/s] 2.16e-11 2.16e-09 2.16e-07", "tiers need 2 x 10^-11 to 2 x 10^-7"),
    ("sim/cell-model-output.txt", "light per fuel pair [W] 3e-25 3e-23 3e-21", "3 x 10^-21 W per fuel pair"),
    ("sim/cell-model-output.txt", "cm3 of stack per 1 mW laser 66.7 0.667 0.00667", "stack lit by a 1 mW laser"),
    ("sim/cell-model-output.txt", "fuel film burn-up without resupply [yr] 1.47e+03 14.7 0.147", "fuel film life"),
    ("sim/cell-model-output.txt", "helium [cm3 STP per cm3 per yr] 0.0019 0.19 19", "helium to vent"),
    ("sim/cell-model-output.txt", "collector life at damage fluence [h] 8.58e+03 85.8 0.858", "collector life"),
    ("sim/cell-model-output.txt", "thickest passively cooled sheet [mm] 1.23e+03 12.3 0.123", "passively cooled sheet"),
    ("sim/cell-model-output.txt", "dielectric cavity, 1 V/nm, 125 nm3 per site, Q 1e6 6.91 3.36e-09", "holding a site costs 3 nW"),
    ("sim/cell-model-output.txt", "plasmonic gap, 1 V/nm, 40 nm3, Q 10 2.21 0.000108", "up to 16 orders too expensive"),
    ("sim/cell-model-output.txt", "7.68e+05 s (8.89 days)", "a written state must last nine days"),
    ("sim/cell-model-output.txt", "76.8 s", "or about a minute"),
    ("docs/physics-baseline.md", "| D–D | 1.5 → 1.0 pm | 1.0 → 1.5 keV | 0.3–1.7 keV |", "what D-D needs"),
    ("docs/physics-baseline.md", "| p–⁶Li | 0.65 → 0.43 pm | 6.7 → 10 keV |", "what p-6Li needs"),
    ("docs/physics-baseline.md", "| p–⁷Li | 0.57 → 0.37 pm | 7.6 → 12 keV |", "what p-7Li needs"),
    ("docs/physics-baseline.md", "| p–¹¹B | 0.43 → 0.30 pm | 17 → 24 keV |", "what p-11B needs"),
    ("docs/physics-baseline.md", "NIF Dec 2022 shot (2.05 MJ in, 3.15 MJ out) | 3 × 10⁶", "NIF: 3 x 10^6 photons per fusion"),
    ("docs/physics-baseline.md", "deuterated nanowire arrays | ~5 × 10¹¹", "nanowires: 5 x 10^11 photons per fusion"),
    ("docs/physics-baseline.md", "**19 kWh per milligram**", "19 kWh per milligram"),
    ("design/nf-cell-v1.yaml", "layer_pitch_um", "the v1 cell specification exists"),
)

PHASES = (
    ("Phase 0", "2027", 1, "Baseline", "The simulator reproduces published results; experiments are designed to count rates.",
     "Gate 0 · Dec 2027", "can an experiment tell?", False),
    ("Phase 1", "2028–29", 2, "Discriminating experiments",
     "Seven experiments on engineered lattices: light on and off, designed defects, the clean fuels.",
     "Gate 1 · Dec 2029", "the main decision: does structure or light change a nuclear rate?", True),
    ("Phase 2", "2030–31", 2, "Atom-exact sites",
     "Sites built to specification, every event tied to its site, and the switch from deuterium to lithium and boron.",
     "Gate 2 · Dec 2031", "drive-correlated events from one tile", False),
    ("Phase 3", "2032–33", 2, "Proof-of-concept cell",
     "Fuel feed, helium venting, a heat path and the first real capture stage.",
     "Gate 3 · Dec 2033", "tile gain ≥ 0.1 for an hour, audited", False),
    ("Phase 4", "2034–35", 2, "Pilot line",
     "Tile to die to stack; laser units as tested parts; lifetime; prototypes from 1 mW to 1 W.",
     "Gate 4 · Dec 2035", "cell gain ≥ 1 for 1,000 hours", False),
    ("Phase 5", "2036", 1, "Mass-fab readiness",
     "Process transfer to a volume line, a cost model and the product ladder.", "", "", False),
)


def check_sources():
    missing = []
    for path, needle, claim in CHECKS:
        with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
            body = fh.read()
        pattern = r"\s+".join(re.escape(part) for part in needle.split())
        if not re.search(pattern, body):
            missing.append(f"  {path}: no longer contains {needle!r}\n    the site says: {claim}")
    if missing:
        sys.exit("The site relies on numbers that the sources no longer show:\n" + "\n".join(missing))
    print(f"checked {len(CHECKS)} numbers against the saved outputs")


def read(*parts):
    with open(os.path.join(HERE, *parts), encoding="utf-8") as fh:
        return fh.read().rstrip("\n")


def head(title, description, source):
    fonts = ("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600"
             "&amp;family=Public+Sans:ital,wght@0,400;0,600;1,400&amp;family=Saira+Condensed:wght@500;600;700"
             "&amp;display=swap")
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<!-- Generated by site/build.py from site/src/{source}; edit the source, not this file. -->
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{URL}site/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="site/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonts}">
<link rel="stylesheet" href="site/site.css">'''


def nav(current):
    items = (("index.html", "Overview"), ("onepager.html", "One-pager"))
    links = '<span aria-hidden="true">·</span>'.join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == current else ""}>{name}</a>' for href, name in items)
    return (f'<nav class="family" aria-label="Site"><span class="lab">NanoFusion</span>{links}'
            f'<span class="sp"></span><a href="{REPO}">GitHub</a></nav>')


def timeline(short=False):
    o = ['<div class="tl" role="list" aria-label="Phases and gates, 2027 to 2036">']
    o += [f'<div class="yr" aria-hidden="true">{year}</div>' for year in range(2027, 2037)]
    for key, years, span, name, what, gate, test, main in PHASES:
        o.append(f'<div class="ph{" main" if main else ""}" style="--n:{span}" role="listitem">'
                 f'<div class="k">{key}<span class="yrs"> · {years}</span></div><h4>{name}</h4>'
                 + ("" if short else f"<p>{what}</p>")
                 + (f'<div class="g"><b>{gate}</b><span>{test}</span></div>' if gate else "")
                 + "</div>")
    o.append("</div>")
    return "\n".join(o)


def fill(template, parts):
    used = set()

    def sub(match):
        key = match.group(1)
        if key not in parts:
            sys.exit(f"template asks for {{{{{key}}}}}, which build.py does not provide")
        used.add(key)
        return parts[key]

    return re.sub(r"\{\{(\w+)\}\}", sub, template), used


def shrink(path):
    """Palette-compress a screenshot: flat colour and text survive it, and the file drops to a third."""
    from PIL import Image
    before = os.path.getsize(path)
    image = Image.open(path).convert("RGB")
    image.quantize(colors=192, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(path, optimize=True)
    print(f"shrank {os.path.relpath(path, ROOT)}: {before / 1000:.0f} kB -> {os.path.getsize(path) / 1000:.0f} kB")


def main():
    if "--shrink" in sys.argv:
        shrink(os.path.join(HERE, "onepager.png"))
        return
    check_sources()
    shared = {
        "gh": GH, "repo": REPO,
        "zoom_ladder": figures.zoom_ladder(), "zoom_strip": figures.zoom_strip(),
        "rate_wide": figures.rate_ladder(False), "rate_compact": figures.rate_ladder(True),
        "way_rest": figures.way_rest(), "way_beam": figures.way_beam(), "way_aim": figures.way_aim(),
        "photon_wide": figures.photon_ladder(False), "photon_compact": figures.photon_ladder(True),
        "layer_section": figures.layer_section(),
        "chart_wide": read("fig", "pair-chart-wide.svg"), "chart_compact": read("fig", "pair-chart-compact.svg"),
        "chart_table": read("fig", "pair-chart-table.html"),
        "chart_data": '<script type="application/json" id="pf-data">' + read("fig", "pair-chart-data.json") + "</script>",
        "timeline": timeline(), "timeline_short": timeline(short=True),
    }
    pages = (
        ("index.html", "NanoFusion",
         "A fusion battery built one reaction site at a time: what it would take, what is ruled out, "
         "and a ten-year plan to find out. A screening-level concept study."),
        ("onepager.html", "NanoFusion: the one-pager",
         "The NanoFusion concept study on one page: the idea, the 53-order gap, three ways to make two "
         "nuclei meet, what each fuel needs, what light can do, and the plan."),
    )
    for name, title, description in pages:
        parts = dict(shared, head=head(title, description, name), nav=nav(name))
        html, _ = fill(read("src", name), parts)
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as fh:
            fh.write(html + "\n")
        print(f"wrote {name} ({len(html) / 1000:.0f} kB)")
    with open(os.path.join(HERE, "favicon.svg"), "w", encoding="utf-8") as fh:
        fh.write(figures.favicon() + "\n")
    open(os.path.join(ROOT, ".nojekyll"), "a").close()


if __name__ == "__main__":
    main()
