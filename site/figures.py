#!/usr/bin/env python3
"""Hand-built SVG figures for the NanoFusion site.  Imported by site/build.py.

Each function returns an inline <svg> fragment that takes its colours from the page's CSS
variables (site/site.css), so it follows the light and dark themes.  Figures that carry many
labels come in a wide and a compact drawing and the page shows whichever fits the screen.

Numbers drawn here are the ones in sim/*-output.txt; build.py checks that they are still there.
"""
import math

SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def p10(n):
    return "10" + str(n).translate(SUP)


# --- drawing helpers -------------------------------------------------------------------------
def text(x, y, s, cls="g-t", size=12, anchor="start", weight=None, extra=""):
    a = "" if anchor == "start" else f' text-anchor="{anchor}"'
    w = f' font-weight="{weight}"' if weight else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" font-size="{size}"{a}{w}{extra}>{s}</text>'


def line(x1, y1, x2, y2, c="ink", w=1.0, dash=None, extra=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="st-{c}" '
            f'stroke-width="{w}"{d}{extra}/>')


def rect(x, y, w, h, fill="none", stroke="none", sw=1.0, op=None, dash=None):
    a = f' fill-opacity="{op}"' if op is not None else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" class="fi-{fill} st-{stroke}" '
            f'stroke-width="{sw}"{a}{d}/>')


def circle(cx, cy, r, fill="none", stroke="none", sw=1.0, op=None, dash=None):
    a = f' fill-opacity="{op}"' if op is not None else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" class="fi-{fill} st-{stroke}" '
            f'stroke-width="{sw}"{a}{d}/>')


def head(x, y, ang, c="ink", size=7.0):
    """Filled triangle with its tip at (x, y), pointing along ang."""
    bx, by = x - size * math.cos(ang), y - size * math.sin(ang)
    px, py = -math.sin(ang) * size * 0.42, math.cos(ang) * size * 0.42
    return (f'<polygon points="{x:.1f},{y:.1f} {bx + px:.1f},{by + py:.1f} {bx - px:.1f},{by - py:.1f}" '
            f'class="fi-{c}"/>')


def arrow(x1, y1, x2, y2, c="ink", w=1.5, size=7.0, dash=None):
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - size * 0.8 * math.cos(ang), y2 - size * 0.8 * math.sin(ang)
    return line(x1, y1, bx, by, c, w, dash, ' stroke-linecap="round"') + head(x2, y2, ang, c, size)


def wavy(x1, y1, x2, y2, c="light", w=1.5, amp=2.6, waves=4, size=6.0):
    """A photon: a sine wave from (x1, y1) toward (x2, y2), ending in an arrowhead."""
    length = math.hypot(x2 - x1, y2 - y1)
    ang = math.atan2(y2 - y1, x2 - x1)
    ux, uy = math.cos(ang), math.sin(ang)
    seg = (length - size) / (2 * waves)
    d = f"M{x1:.1f},{y1:.1f}"
    for k in range(2 * waves):
        sign = 1 if k % 2 == 0 else -1
        mx, my = x1 + ux * seg * (k + 0.5), y1 + uy * seg * (k + 0.5)
        ex, ey = x1 + ux * seg * (k + 1), y1 + uy * seg * (k + 1)
        d += f" Q{mx - uy * 2 * amp * sign:.1f},{my + ux * 2 * amp * sign:.1f} {ex:.1f},{ey:.1f}"
    return (f'<path d="{d}" class="fi-none st-{c}" stroke-width="{w}" stroke-linecap="round"/>'
            + head(x2, y2, ang, c, size))


def svg_open(w, h, label, cls="g"):
    return f'<svg class="{cls}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">'


# --- from a battery down to one fuel pair ---------------------------------------------------------
S = 96            # side of one zoom frame


def _frame_cell(x, y):
    """The cell: a stack of layers, seen from the side.  Returns the drawing and the box that is magnified next."""
    o = [rect(x, y, S, S, "surface", "rule")]
    for k in range(7):
        o.append(rect(x + 10, y + 9.5 + 11.6 * k, S - 20, 7, "wash", "ink2", 0.8, 0.16))
    ly = y + 9.5 + 11.6 * 4
    box = (x + 56, ly - 3.5, x + 70, ly + 10.5)
    return "".join(o), box


def _frame_unit(x, y):
    """The laser unit, seen from above: laser die, waveguide tree, tiles."""
    o = [rect(x, y, S, S, "surface", "rule"), rect(x + 7, y + 30, 11, 36, "light"),
         line(x + 18, y + 48, x + 25, y + 48, "light", 1.5), line(x + 25, y + 11, x + 25, y + 85, "light", 1.5)]
    for k in range(6):
        o.append(line(x + 25, y + 11 + 14.8 * k, x + 89, y + 11 + 14.8 * k, "light", 1.0))
    for i in range(5):
        for j in range(5):
            o.append(rect(x + 30 + 12 * j, y + 14 + 14.8 * i, 9, 8.8, "wash", "ink2", 0.8, 0.16))
    tx, ty = x + 30 + 12 * 2, y + 14 + 14.8 * 3
    return "".join(o), (tx - 1.6, ty - 1.6, tx + 10.6, ty + 10.4)


def _frame_tile(x, y):
    """One tile: a film of site crystal under a branch waveguide."""
    o = [rect(x, y, S, S, "surface", "rule"), rect(x + 10, y + 16, 76, 72, "wash", "ink2", 0.8, 0.16),
         line(x + 4, y + 9, x + 92, y + 9, "light", 2.0)]
    for k in range(3):
        o.append(line(x + 22 + 26 * k, y + 9, x + 22 + 26 * k, y + 16, "light", 1.0))
    for i in range(7):
        for j in range(7):
            o.append(circle(x + 10 + 76 * (j + 0.5) / 7, y + 16 + 72 * (i + 0.5) / 7, 1.4, "ink3"))
    cx, cy = x + 10 + 76 * 4.5 / 7, y + 16 + 72 * 4.5 / 7
    return "".join(o), (cx - 5, cy - 5, cx + 5, cy + 5)


def _frame_site(x, y):
    """One site: a cage holding a proton and a boron nucleus, a photon arriving."""
    cx, cy = x + S / 2 + 4, y + S / 2 + 4
    o = [rect(x, y, S, S, "surface", "rule"), circle(cx, cy, 21, "wash", op=0.13)]
    for k in range(8):
        a = math.pi / 8 + k * math.pi / 4
        o.append(circle(cx + 33 * math.cos(a), cy + 33 * math.sin(a), 6.2, "surface", "ink2", 1.0))
    o += [circle(cx - 9, cy, 2.6, "ink"), circle(cx + 8, cy, 4.6, "ink"),
          wavy(x + 5, y + 7, cx - 15, cy - 13, "light", 1.4, 2.2, 3, 5.5)]
    return "".join(o), None


ZOOM_LABEL = ("Four nested views of the concept cell. A one cubic centimetre battery cell is a stack of 500 layers. "
              "Each layer is tiled with 2 millimetre laser units, in which one laser die lights 625 tiles through a "
              "waveguide tree. Each 50 micrometre tile carries a 1 micrometre film of site crystal. Each reaction "
              "site is a 1 nanometre cage holding one fuel pair.")
ZOOM_FRAMES = (_frame_cell, _frame_unit, _frame_tile, _frame_site)


def zoom_ladder():
    """The four views stacked, each with its description beside it."""
    W, H, X, P, Y0, LX = 460, 474, 10, 118, 8, 124
    ys = [Y0 + P * k for k in range(4)]
    o = [svg_open(W, H, ZOOM_LABEL)]
    for k, draw in enumerate(ZOOM_FRAMES):
        body, box = draw(X, ys[k])
        o.append(body)
        if box:
            o.append(rect(box[0], box[1], box[2] - box[0], box[3] - box[1], "none", "ink", 1.5))
            o.append(line(box[0], box[3], X, ys[k + 1], "ink3", 0.9, "2 3"))
            o.append(line(box[2], box[3], X + S, ys[k + 1], "ink3", 0.9, "2 3"))
    labels = (("Battery cell", "1 cm³", ("500 layers of fuel film and collector,", "2.5 × 10¹⁹ fuel pairs in all")),
              ("Laser unit", "2 mm", ("one laser die lights 625 tiles", "through a waveguide tree")),
              ("Tile", "50 µm", ("a 1 µm film of site crystal:", "1.25 × 10¹² cages, 1 nm apart")),
              ("Reaction site", "1 nm", ("one cage holding one fuel pair,", "built to atomic specification")))
    for y, (name, size, lines) in zip(ys, labels):
        o.append(text(LX, y + 24, name, "g-t disp", 21, weight=700))
        o.append(text(W - 4, y + 24, size, "g-t3 mono", 12.5, "end"))
        for k, s in enumerate(lines):
            o.append(text(LX, y + 46 + 17 * k, s, "g-t2", 13.5))
    o.append(text(LX, ys[3] + 46 + 17 * 2 + 3, "p + ¹¹B → 3 ⁴He + 8.7 MeV", "g-t", 13.5, weight=600))
    o.append("</svg>")
    return "\n".join(o)


def zoom_strip():
    """The same four views in a row, for wide and shallow spaces."""
    W, H, X0, P, Y = 660, 172, 6, 166, 6
    xs = [X0 + P * k for k in range(4)]
    o = [svg_open(W, H, ZOOM_LABEL)]
    for k, draw in enumerate(ZOOM_FRAMES):
        body, box = draw(xs[k], Y)
        o.append(body)
        if box:
            o.append(rect(box[0], box[1], box[2] - box[0], box[3] - box[1], "none", "ink", 1.5))
            o.append(line(box[2], box[1], xs[k + 1], Y, "ink3", 0.9, "2 3"))
            o.append(line(box[2], box[3], xs[k + 1], Y + S, "ink3", 0.9, "2 3"))
    labels = (("Battery cell", "1 cm³", ("500 layers,", "2.5 × 10¹⁹ fuel pairs")),
              ("Laser unit", "2 mm", ("one laser die", "lights 625 tiles")),
              ("Tile", "50 µm", ("1 µm of site crystal,", "1.25 × 10¹² cages")),
              ("Reaction site", "1 nm", ("one cage,", "one fuel pair")))
    for x, (name, size, lines) in zip(xs, labels):
        o.append(text(x, Y + S + 22, name, "g-t disp", 17, weight=700))
        o.append(text(x + 150, Y + S + 22, size, "g-t3 mono", 11.5, "end"))
        for k, s in enumerate(lines):
            o.append(text(x, Y + S + 39 + 15 * k, s, "g-t2", 12))
    o.append("</svg>")
    return "\n".join(o)


# --- the rate ladder ---------------------------------------------------------------------------
PDD, D2, VIB, MUON = -88.0, -63.7, -55.3, 11.6          # log10 fusions per pair per second
IF_LO, IF_HI = -26.9, -5.0                              # caged D-D pair with reported screening
BAND = (math.log10(2e-11), math.log10(2e-7))            # what a battery needs
LI_LO, LI_HI, B_REP = -79.3, -43.9, -135.3              # clean fuels with their reported screening
R_LO, R_HI = -100.0, 15.0


def _value_label(x, y, value, lines, anchor="start", size=12):
    o = [text(x, y, value, "g-t", size + 1, anchor, 600)]
    for k, s in enumerate(lines):
        o.append(text(x, y + 15 * (k + 1), s, "g-t2", size, anchor))
    return "".join(o)


def rate_ladder(compact=False):
    label = ("Fusion rate of one deuterium pair in different surroundings, on a logarithmic scale. Deuterons on "
             "neighbouring lattice sites of palladium deuteride: ten to the minus 88 per second. A deuterium "
             "molecule: two times ten to the minus 64. The same molecule pumped to the top of its vibrational "
             "ladder: ten to the minus 55. A battery needs ten to the minus 11 to ten to the minus 7, which is 53 "
             "orders of magnitude above the molecule. A caged pair would reach ten to the minus 27 to ten to "
             "the minus 5 if the screening measured in beam experiments held for a pair at rest. With a muon "
             "in place of the electron the rate is four times ten to the 11.")
    return _rate_compact(label) if compact else _rate_wide(label)


def _rate_wide(label):
    W, H, X0, X1, AY = 1100, 330, 60, 1060, 192

    def sx(v):
        return X0 + (v - R_LO) / (R_HI - R_LO) * (X1 - X0)

    o = [svg_open(W, H, label)]
    # the band a battery needs, behind everything
    o.append(rect(sx(BAND[0]), 46, sx(BAND[1]) - sx(BAND[0]), 256, "wash", op=0.17))
    mid = (sx(BAND[0]) + sx(BAND[1])) / 2
    o.append(text(mid, 22, "what a battery needs", "g-t", 13, "middle", 600))
    o.append(text(mid, 38, f"{p10(-11)} to {p10(-7)} per second", "g-t2", 12, "middle"))
    # axis
    o.append(line(X0, AY, X1, AY, "ink2", 1.0))
    for v in range(-100, 11, 10):
        o.append(line(sx(v), AY, sx(v), AY + 5, "ink2", 1.0))
        o.append(text(sx(v), AY + 19, p10(v) if v else "1", "g-t3", 11, "middle"))
    o.append(text(X0, 20, "DEUTERIUM", "g-t3 mono", 10.5, extra=' letter-spacing="1.2"'))
    o.append(text(X0, 242, "CLEAN FUELS", "g-t3 mono", 10.5, extra=' letter-spacing="1.2"'))
    o.append(text(X0, H - 8, "Fusions per fuel pair per second. Logarithmic scale: each tick is ten orders of magnitude.",
                  "g-t3", 11.5))

    # deuterium items
    x = sx(PDD)
    o.append(line(x, AY - 5, x, 82, "ink3", 0.9))
    o.append(_value_label(x + 6, 92, p10(-88), ("deuterons on neighbouring", "lattice sites of PdD")))
    x = sx(D2)
    o.append(line(x, AY - 5, x, 64, "ink3", 0.9))
    o.append(_value_label(x - 6, 142, f"2 × {p10(-64)}", ("D₂ molecule, as it is",), "end"))
    o.append(arrow(x, 64, sx(BAND[0]) - 1, 64, "ink", 1.3, 8))
    o.append(text((x + sx(BAND[0])) / 2, 56, "53 orders of magnitude to go", "g-t", 12.5, "middle", 600))
    x = sx(VIB)
    o.append(line(x, AY - 5, x, 132, "ink3", 0.9))
    o.append(_value_label(x + 6, 142, p10(-55), ("D₂ pumped to the top of", "its vibrational ladder")))
    # the conditional range
    xa, xb = sx(IF_LO), sx(IF_HI)
    o.append(rect(xa, AY - 6, xb - xa, 12, "s1", "s1", 1.5, 0.22, "4 3"))
    xl = sx(BAND[0]) - 12
    o.append(line(xl, AY - 6, xl, 128, "ink3", 0.9))
    o.append(_value_label(xl - 6, 92, f"{p10(-27)} to {p10(-5)}",
                          ("a caged D–D pair, if the screening seen in", "beam experiments held for a pair at rest"),
                          "end"))
    x = sx(MUON)
    o.append(line(x, AY - 5, x, 132, "ink3", 0.9))
    o.append(_value_label(x - 6, 142, f"4 × {p10(11)}", ("D₂ with a muon in", "place of its electron"), "end"))
    for v in (PDD, D2, VIB, MUON):
        o.append(circle(sx(v), AY, 5, "s1", "surface", 2))

    # clean fuels, with the screening reported for them
    xa, xb = sx(LI_LO), sx(LI_HI)
    o.append(rect(xa, 232, xb - xa, 12, "s3", "s3", 1.5, 0.22, "4 3"))
    o.append(_value_label(xb + 10, 236, f"{p10(-79)} to {p10(-44)}",
                          ("p–⁷Li, with the screening reported for lithium",)))
    o.append(arrow(104, 284, X0 + 2, 284, "s4", 2.2, 9))
    o.append(_value_label(112, 281, p10(-135), ("p–¹¹B, with the screening reported for boron: off the scale",)))
    o.append("</svg>")
    return "\n".join(o)


def _rate_compact(label):
    W, H, AX, Y0, Y1, LX = 400, 634, 92, 34, 584, 108

    def sy(v):
        return Y0 + (R_HI - v) / (R_HI - R_LO) * (Y1 - Y0)

    o = [svg_open(W, H, label)]
    o.append(rect(AX, sy(BAND[1]), W - 8 - AX, sy(BAND[0]) - sy(BAND[1]), "wash", op=0.17))
    o.append(text(LX, sy(BAND[1]) - 7, "what a battery needs:", "g-t", 12.5, weight=600))
    o.append(text(LX + 134, sy(BAND[1]) - 7, f"{p10(-11)} to {p10(-7)} per second", "g-t2", 12))
    o.append(line(AX, Y0, AX, Y1, "ink2", 1.0))
    for v in range(-100, 1, 20):
        o.append(line(AX - 5, sy(v), AX, sy(v), "ink2", 1.0))
        o.append(text(AX - 10, sy(v) + 4, p10(v) if v else "1", "g-t3", 11, "end"))
    # 53 orders, as a dimension arrow up the left edge
    ya, yb = sy(D2), sy(BAND[0])
    o.append(arrow(22, ya, 22, yb + 1, "ink", 1.3, 8))
    o.append(line(16, ya, AX - 8, ya, "ink3", 0.9, "2 3"))
    ym = (ya + yb) / 2
    o.append(text(13, ym, "53 orders of magnitude to go", "g-t", 12, "middle", 600,
                  f' transform="rotate(-90 13 {ym:.1f})"'))
    # items
    o.append(_value_label(LX, sy(MUON) - 2, f"4 × {p10(11)}", ("D₂ with a muon in place of its electron",)))
    ya, yb = sy(IF_HI), sy(IF_LO)
    o.append(rect(AX - 6, ya, 12, yb - ya, "s1", "s1", 1.5, 0.22, "4 3"))
    o.append(_value_label(LX, 188, f"{p10(-27)} to {p10(-5)}",
                          ("a caged D–D pair, if the screening seen in", "beam experiments held for a pair at rest")))
    o.append(_value_label(LX, sy(VIB) - 2, p10(-55), ("D₂ pumped up its vibrational ladder",)))
    o.append(_value_label(LX, sy(D2) + 4, f"2 × {p10(-64)}", ("D₂ molecule, as it is",)))
    o.append(_value_label(LX, sy(PDD) - 2, p10(-88), ("deuterons on neighbouring sites in PdD",)))
    for v in (PDD, D2, VIB, MUON):
        o.append(circle(AX, sy(v), 5, "s1", "surface", 2))
    o.append(text(8, H - 26, "Clean fuels, with the screening reported for them:", "g-t2", 12))
    o.append(text(8, H - 9, f"p–⁷Li {p10(-79)} to {p10(-44)}  ·  p–¹¹B {p10(-135)}", "g-t", 12.5, weight=600))
    o.append("</svg>")
    return "\n".join(o)


# --- three ways to make two nuclei meet ----------------------------------------------------------
def way_rest():
    W, H, cx, cy = 320, 172, 160, 76
    o = [svg_open(W, H, "Two deuterium nuclei at rest in one cage of host atoms, 74 picometres apart, with a cloud "
                        "of electrons between them.")]
    for k in range(12):
        a = 2 * math.pi * k / 12
        o.append(circle(cx + 118 * math.cos(a), cy + 54 * math.sin(a), 9, "surface", "ink3", 1.0))
    o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="74" ry="30" class="fi-wash" fill-opacity="0.13"/>')
    o.append(line(cx - 36, cy, cx + 36, cy, "ink2", 1.0, "2 3"))
    for x in (cx - 42, cx + 42):
        o.append(circle(x, cy, 6, "s1", "ink", 0.8))
        o.append(text(x, cy - 12, "D", "g-t", 12, "middle", 600))
    o.append(line(cx - 42, cy + 20, cx + 42, cy + 20, "ink2", 0.9))
    for x in (cx - 42, cx + 42):
        o.append(line(x, cy + 16, x, cy + 24, "ink2", 0.9))
    o.append(text(cx, cy + 35, "74 pm", "g-t2 mono", 11, "middle"))
    o.append(text(cx, 162, "at rest in one cage; electrons screen the repulsion", "g-t2", 12, "middle"))
    o.append("</svg>")
    return "\n".join(o)


def way_beam():
    W, H = 320, 172
    o = [svg_open(W, H, "A proton crossing rows of boron atoms. It passes through the electron cloud of each atom "
                        "and misses the small nuclei.")]
    for i in range(3):
        for j in range(6):
            x, y = 146 + 30 * j, 30 + 36 * i
            o.append(circle(x, y, 13, "wash", op=0.13))
            o.append(circle(x, y, 3.4, "s4", "ink", 0.8))
    o.append(arrow(30, 56, 310, 56, "ink", 1.6, 8))
    o.append(circle(26, 56, 3.6, "ink"))
    o.append(text(8, 40, "proton, 650 keV", "g-t", 12, weight=600))
    o.append(text(8, 84, "through the electrons,", "g-t2", 12))
    o.append(text(8, 99, "past the nuclei", "g-t2", 12))
    o.append(text(W / 2, 146, "every layer of electrons takes 14 eV;", "g-t2", 12, "middle"))
    o.append(text(W / 2, 162, f"one layer in 3 × {p10(8)} ends in a hit", "g-t2", 12, "middle"))
    o.append("</svg>")
    return "\n".join(o)


def way_aim():
    W, H, bx, by = 320, 172, 232, 70
    o = [svg_open(W, H, "A proton aimed at the centre of a wide blur that marks where a boron nucleus may be. The "
                        "target it must hit is a tiny dot at the centre of the blur.")]
    for r, op in ((58, 0.07), (42, 0.08), (26, 0.10)):
        o.append(circle(bx, by, r, "wash", op=op))
    o.append(circle(bx, by, 58, "none", "ink3", 0.9, dash="3 3"))
    o.append(arrow(22, by, bx - 6, by, "ink", 1.6, 8))
    o.append(circle(18, by, 3.6, "ink"))
    o.append(circle(bx, by, 2.4, "s4", "ink", 0.8))
    o.append(text(8, 22, "the nucleus is somewhere", "g-t", 12, weight=600))
    o.append(text(8, 37, "in this blur: ±4.2 pm", "g-t", 12, weight=600))
    o.append(line(150, 30, bx - 50, by - 30, "ink3", 0.8))
    o.append(text(8, 108, "the pocket: 6 fm in radius", "g-t2", 12))
    o.append(text(8, 123, "(drawn 50 times too large)", "g-t3", 11.5))
    o.append(line(142, 103, bx - 4, by + 3, "ink3", 0.8))
    o.append(text(W / 2, 162, "a perfect shot hits about once in a million", "g-t2", 12, "middle"))
    o.append("</svg>")
    return "\n".join(o)


# --- photons spent per fusion --------------------------------------------------------------------
def photon_ladder(compact=False):
    label = ("Photons spent per fusion, on a logarithmic scale. A battery burning hydrogen and boron can afford at "
             "most forty thousand. The 2022 ignition shot at the National Ignition Facility spent three million. "
             "Laser-heated deuterated nanowires spent five hundred billion. Low-power light on a lattice has "
             "produced no confirmed fusion at any photon count.")
    W, H = (400, 208) if compact else (1100, 176)
    X0, X1, AY = (22, 356, 104) if compact else (70, 940, 96)
    lo, hi = 3.0, 13.0

    def sx(v):
        return X0 + (v - lo) / (hi - lo) * (X1 - X0)

    budget, even, nif, wires = math.log10(4.34e4), math.log10(1.3e5), math.log10(3e6), math.log10(5e11)
    o = [svg_open(W, H, label)]
    o.append(rect(X0, AY - 22, sx(budget) - X0, 44, "wash", op=0.17))
    o.append(line(X0, AY, X1, AY, "ink2", 1.0))
    for v in range(3, 14):
        o.append(line(sx(v), AY, sx(v), AY + 5, "ink2", 1.0))
        if not compact or v % 2 == 1:
            o.append(text(sx(v), AY + 19, p10(v), "g-t3", 11, "middle"))
    o.append(arrow(X1, AY, X1 + (30 if compact else 110), AY, "ink2", 1.0, 7, "3 3"))
    if compact:
        o.append(_value_label(X0, 24, f"≤ 4 × {p10(4)}", ("what a p–¹¹B battery can afford",)))
        o.append(line(sx(budget), AY - 22, sx(budget), 46, "ink3", 0.9))
        o.append(_value_label(sx(nif) + 6, 150, f"3 × {p10(6)}", ("ignition shot, NIF 2022",)))
        o.append(line(sx(nif), AY + 5, sx(nif), 158, "ink3", 0.9))
        o.append(_value_label(sx(wires) - 6, 60, f"5 × {p10(11)}", ("laser-heated nanowires",), "end"))
        o.append(line(sx(wires), AY - 5, sx(wires), 50, "ink3", 0.9))
        o.append(text(W - 6, 150, "no fusion seen", "g-t", 12.5, "end", 600))
        o.append(text(W - 6, 165, "low-power light", "g-t2", 12, "end"))
        o.append(text(W - 6, 180, "on a lattice", "g-t2", 12, "end"))
        o.append(text(X0, H - 6, "Photons spent per fusion (log scale)", "g-t3", 11.5))
    else:
        o.append(_value_label(X0, 22, f"≤ 4 × {p10(4)}", ("what a p–¹¹B battery can afford",)))
        o.append(line(sx(budget), AY - 22, sx(budget), 44, "ink3", 0.9))
        o.append(_value_label(sx(even) + 6, 62, f"1.3 × {p10(5)}", ("break-even",)))
        o.append(line(sx(even), AY - 5, sx(even), 52, "ink3", 0.9))
        o.append(circle(sx(even), AY, 3.5, "surface", "ink2", 1.5))
        o.append(_value_label(sx(nif) + 6, 22, f"3 × {p10(6)}", ("ignition shot, National Ignition Facility, 2022",)))
        o.append(line(sx(nif), AY - 5, sx(nif), 12, "ink3", 0.9))
        o.append(_value_label(sx(wires) - 6, 62, f"5 × {p10(11)}", ("laser-heated deuterated nanowires, 2018",), "end"))
        o.append(line(sx(wires), AY - 5, sx(wires), 52, "ink3", 0.9))
        o.append(text(W - 6, 62, "no fusion seen", "g-t", 12.5, "end", 600))
        o.append(text(W - 6, 77, "low-power light on a lattice", "g-t2", 12, "end"))
        o.append(text(X0, H - 8, "Photons spent per fusion. Logarithmic scale: each tick is a factor of ten.",
                      "g-t3", 11.5))
    for v in (nif, wires):
        o.append(circle(sx(v), AY, 5, "light", "surface", 2))
    o.append("</svg>")
    return "\n".join(o)


# --- one layer of the stack, in section ----------------------------------------------------------
def layer_section():
    W, H, GX, XL, XR = 440, 306, 142, 152, 432
    o = [svg_open(W, H, "Cross-section of one layer of the cell. Light travels along a waveguide under a one "
                        "micrometre film of fuel sites. A fusion in the film sends three alpha particles outward. "
                        "They stop in the diamond collectors above and below the film, which turn part of their "
                        "energy into electric current and carry the rest away as heat.")]
    bands = ((14, 46, "wash", 0.10), (60, 50, "surface", None), (110, 26, "wash", 0.04), (136, 104, "wash", 0.10))
    for top, height, fill, op in bands:
        o.append(rect(XL, top, XR - XL, height, fill, "ink3", 0.8, op))
    o.append(rect(XL, 240, XR - XL, 11, "ink2", "ink3", 0.8, 0.55))
    for i in range(4):                                                         # the cages in the film
        for j in range(23):
            o.append(circle(XL + 8 + 12 * j, 67 + 12 * i, 1.3, "ink3"))
    # light along the waveguide, leaking up into the film
    o.append(arrow(XL - 8, 123, XR + 6, 123, "light", 2.6, 9))
    for x in (188, 244, 356, 412):
        o.append(arrow(x, 121, x, 106, "light", 1.2, 5))
    # one fusion and its three alphas
    fx, fy = 300, 85
    for ex, ey in ((262, 28), (238, 196), (374, 184)):
        o.append(arrow(fx, fy, ex, ey, "ink", 1.6, 7))
        for d in (-1, 1):
            a = math.atan2(ey - fy, ex - fx) + d * 1.25
            o.append(line(ex, ey, ex + 7 * math.cos(a), ey + 7 * math.sin(a), "ink2", 0.9))
    o.append(f'<path d="M{fx},{fy - 9} L{fx + 2.8},{fy - 2.8} L{fx + 9},{fy} L{fx + 2.8},{fy + 2.8} L{fx},{fy + 9} '
             f'L{fx - 2.8},{fy + 2.8} L{fx - 9},{fy} L{fx - 2.8},{fy - 2.8}Z" class="fi-s4 st-ink" stroke-width="0.8"/>')
    o.append(text(XR - 8, 32, "one fusion:", "g-t", 12, "end", 600))
    o.append(text(XR - 8, 47, "3 alphas, 8.7 MeV", "g-t2", 12, "end"))
    o.append(line(330, 50, fx + 7, fy - 6, "ink3", 0.8))
    o.append(text(XR - 8, 212, "alphas stop here,", "g-t2", 12, "end"))
    o.append(text(XR - 8, 227, "freeing charge", "g-t2", 12, "end"))
    # layer names, in the gutter
    names = ((33, ("collector of", "the layer above"), False),
             (79, ("fuel film:", "site crystal, 1 µm"), True),
             (119, ("waveguide: light", "from the laser unit"), False),
             (176, ("collector and", "heat spreader:", "diamond, 18 µm"), True),
             (249, ("contact",), False))
    for y, lines, strong in names:
        for k, s in enumerate(lines):
            o.append(text(GX, y + 15 * k, s, "g-t" if strong and k == 0 else "g-t2", 12, "end",
                          600 if strong and k == 0 else None))
    o.append(text(XR, 272, "electricity out: 20 % of the alpha energy assumed", "g-t2", 12, "end"))
    o.append(text(XR, 288, "the rest leaves as heat, through the diamond", "g-t3", 11.5, "end"))
    o.append(text(4, 300, "Not to scale.", "g-t3", 11.5))
    o.append("</svg>")
    return "\n".join(o)


def favicon():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" '
            'fill="#161b22"/><circle cx="32" cy="32" r="21" fill="none" stroke="#c5ccd5" stroke-width="3" '
            'stroke-dasharray="5 6"/><circle cx="24" cy="32" r="5" fill="#eda100"/>'
            '<circle cx="41" cy="32" r="8" fill="#eda100"/></svg>')
