#!/usr/bin/env python3
"""Render an NF-cell spec to an SVG drawing: layer stack, pixel top view, site zoom.

Geometry is generated from the YAML spec, never drawn by hand (design note
"source of truth").  This is the first, 2D stand-in for the CAD model.

Usage:  python3 cad/render_cell.py [design/nf-cell-v0.yaml] [design/nf-cell-v0.svg]
Needs:  PyYAML.
"""
import math
import sys
from xml.sax.saxutils import escape

import yaml

FILL = {
    "reservoir": "#9ecae1", "contact": "#525252", "collector": "#d9e6ec",
    "spacer": "#74c476", "reaction": "#e6550d", "cladding": "#f0f0f0",
    "waveguide": "#9e9ac8",
}
INK, MUTED, FUEL = "#1a1a1a", "#666666", "#e6550d"


def fmt_len(nm):
    return f"{nm / 1000:g} µm" if nm >= 1000 else f"{nm:g} nm"


def text(x, y, s, size=12, fill=INK, anchor="start", weight="normal"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{escape(str(s))}</text>')


def bowtie(cx, cy, edge, gap, scale, fill):
    """Two equilateral prisms tip to tip along y, separated by `gap` (nm)."""
    h = edge * math.sqrt(3) / 2
    out = []
    for sign in (-1, 1):
        apex = (cx, cy + sign * gap / 2 * scale)
        base_y = cy + sign * (gap / 2 + h) * scale
        pts = [apex, (cx - edge / 2 * scale, base_y), (cx + edge / 2 * scale, base_y)]
        out.append('<polygon points="%s" fill="%s"/>' %
                   (" ".join(f"{px:.2f},{py:.2f}" for px, py in pts), fill))
    return out


def render(spec):
    layers, ant, feed = spec["layers"], spec["antenna"], spec["photon_feed"]
    pitch = spec["pixel"]["pitch_nm"]
    gap = ant["gap_nm"]["value"]
    edge = ant["prism_edge_nm"]
    wg_w = feed["waveguide"]["width_nm"]
    p = []
    w, h = 1180, 640
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
             f'width="{w}" height="{h}" font-family="Helvetica, Arial, sans-serif">')
    p.append(f'<rect width="{w}" height="{h}" fill="#ffffff"/>')
    meta = spec["meta"]
    p.append(text(40, 34, f'{meta["name"]} (rev {meta["revision"]}, {meta["date"]}) '
                          f'— generated from the parametric spec', 16, weight="bold"))

    # --- layer stack (y-z section), log-scaled heights -----------------------
    x0, y, bw = 40, 78, 250
    p.append(text(x0, 62, "Layer stack, y–z section (heights log-scaled; labels are true)", 12, MUTED))
    for layer in reversed(layers):                    # top layer first
        t = layer["thickness_nm"]
        lh = 18 + 22 * math.log10(t)
        fill = FILL.get(layer["name"], "#cccccc")
        p.append(f'<rect x="{x0}" y="{y:.1f}" width="{bw}" height="{lh:.1f}" fill="{fill}" '
                 f'stroke="{INK}" stroke-width="0.6"/>')
        if layer["name"] == "reaction":               # mark the sites
            for i in range(6):
                cx = x0 + 25 + i * 40
                p.append(f'<circle cx="{cx}" cy="{y + lh / 2:.1f}" r="3" fill="#ffffff"/>')
        mid = y + lh / 2
        p.append(text(x0 + bw + 12, mid - 2, f'{layer["name"]} · {fmt_len(t)}', 12, weight="bold"))
        p.append(text(x0 + bw + 12, mid + 12, f'{layer["material"]} — {layer["role"]}', 11, MUTED))
        y += lh
    p.append(text(x0, y + 20, "z ↑  (beam and loading reach the sites from the top; products are detected below)", 11, MUTED))

    # --- top view of a 2 x 2 pixel block, to scale ---------------------------
    s = 0.9                                           # px per nm
    tx, ty, block = 600, 78, 2 * pitch
    p.append(text(tx, 62, f"Top view, 2 × 2 pixels to scale (pitch {pitch} nm)", 12, MUTED))
    p.append(f'<rect x="{tx}" y="{ty}" width="{block * s}" height="{block * s}" fill="#fafafa" '
             f'stroke="{INK}" stroke-width="0.8"/>')
    wy = ty + (block - wg_w) / 2 * s
    p.append(f'<rect x="{tx}" y="{wy:.1f}" width="{block * s}" height="{wg_w * s:.1f}" '
             f'fill="{FILL["waveguide"]}" fill-opacity="0.35"/>')
    p.append(f'<line x1="{tx + pitch * s}" y1="{ty}" x2="{tx + pitch * s}" y2="{ty + block * s}" '
             f'stroke="{MUTED}" stroke-dasharray="4 4" stroke-width="0.6"/>')
    p.append(f'<line x1="{tx}" y1="{ty + pitch * s}" x2="{tx + block * s}" y2="{ty + pitch * s}" '
             f'stroke="{MUTED}" stroke-dasharray="4 4" stroke-width="0.6"/>')
    for i in range(2):
        for j in range(2):
            cx = tx + (0.5 + i) * pitch * s
            cy = ty + (0.5 + j) * pitch * s
            p += bowtie(cx, cy, edge, gap, s, FUEL)
    by = ty + block * s
    p.append(text(tx, by + 18, f"waveguide {wg_w} nm wide, runs along x, spans two pixel rows; "
                               f"TE field along y", 11, MUTED))
    p.append(text(tx, by + 34, f"antenna: {ant['type']}, {edge} nm prisms, "
                               f"{ant['thickness_nm']} nm thick, {ant['material']}", 11, MUTED))
    p.append(text(tx, by + 50, f"site density {float(spec['pixel']['site_density_per_cm2']['value']):.1e} "
                               f"per cm²", 11, MUTED))
    p.append(text(tx + block * s + 8, ty + block * s, "x →", 11, MUTED))

    # --- site zoom -----------------------------------------------------------
    z = 3.4                                           # px per nm
    zx, zy = 1010, 78
    zw, zh = 150, 230
    p.append(text(zx, 62, "Site zoom (one antenna)", 12, MUTED))
    p.append(f'<rect x="{zx}" y="{zy}" width="{zw}" height="{zh}" fill="#fafafa" stroke="{INK}" '
             f'stroke-width="0.8"/>')
    ccx, ccy = zx + zw / 2, zy + zh / 2
    p += bowtie(ccx, ccy, edge, gap, z, FUEL)
    p.append(f'<circle cx="{ccx}" cy="{ccy}" r="9" fill="none" stroke="{INK}" stroke-width="1"/>')
    p.append(f'<line x1="{ccx + 9}" y1="{ccy}" x2="{zx + zw - 6}" y2="{ccy}" stroke="{INK}" '
             f'stroke-width="0.8"/>')
    p.append(text(zx, zy + zh + 18, f"gap {gap} nm = reaction site", 12, weight="bold"))
    p.append(text(zx, zy + zh + 34, f"hot spot ≤ {ant['hot_spot_volume_nm3']['value']} nm³", 11, MUTED))
    p.append(text(zx, zy + zh + 50, f"~{ant['deuterons_in_hot_spot']['value']} deuterons", 11, MUTED))
    p.append(text(zx, zy + zh + 66, f"{ant['one_photon_field_V_per_nm']['value']} V/nm per photon", 11, MUTED))
    p.append(f'<line x1="{zx}" y1="{zy + zh - 10}" x2="{zx + 10 * z}" y2="{zy + zh - 10}" '
             f'stroke="{INK}" stroke-width="2"/>')
    p.append(text(zx + 10 * z + 6, zy + zh - 6, "10 nm", 10, MUTED))

    p.append(text(40, h - 16, "Laboratory instrument for experiment E1 (light-modulated D-D yield). "
                              "Not an energy-producing design.", 11, MUTED))
    p.append("</svg>")
    return "\n".join(p)


def main():
    spec_path = sys.argv[1] if len(sys.argv) > 1 else "design/nf-cell-v0.yaml"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "design/nf-cell-v0.svg"
    with open(spec_path) as fh:
        spec = yaml.safe_load(fh)
    with open(out_path, "w") as fh:
        fh.write(render(spec))
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
