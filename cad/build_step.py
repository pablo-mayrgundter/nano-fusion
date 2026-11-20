#!/usr/bin/env python3
"""Build STEP models of the cell from the YAML specs (code-CAD, CadQuery / OpenCascade).

Two models, each at the level of detail where it means something:

  design/step/nf-cell-v0-pixel-block.step   L2: 2 x 2 pixels of the v0 lab cell,
                                            top of the stack, every antenna a solid.
                                            MODEL SCALE: 1 mm in the file = 1 nm.
  design/step/nf-cell-v1-laser-unit.step    L3-L5: one laser die feeding a field of
                                            site-crystal tiles, on a short stack.
                                            MODEL SCALE: 1 mm in the file = 1 um.

STEP has no practical nanometre unit and geometry kernels lose precision far below
a micrometre, so each file is written in millimetres at a declared scale.  The scale
is in the assembly name and in design/step/README.md.

Geometry is generated from the specs; nothing is drawn by hand.
Needs: cadquery, PyYAML.     Run:  python3 cad/build_step.py
"""
import math
import os
import sys

import cadquery as cq
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "design", "step")

COLOURS = {
    "contact": "#525252", "collector": "#d9e6ec", "cladding": "#f0f0f0", "waveguide": "#9e9ac8",
    "spacer": "#74c476", "reaction": "#e6550d", "laser": "#3182bd", "film": "#e6550d",
    "optics": "#bcbddc", "package": "#bdbdbd",
}


def colour(key, alpha=1.0):
    h = COLOURS[key].lstrip("#")
    return cq.Color(*(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)), alpha)


def slab(x, y, z):
    """Box centred in x and y, sitting on z = 0."""
    return cq.Workplane("XY").box(x, y, z, centered=(True, True, False))


def at(x=0.0, y=0.0, z=0.0):
    return cq.Location(cq.Vector(x, y, z))


def val(node):
    return float(node["value"]) if isinstance(node, dict) else float(node)


# --- L2: v0 pixel block, 1 mm = 1 nm ---------------------------------------------------
def build_pixel_block(spec, nx=2, ny=2, collector_shown_nm=300.0):
    pitch = float(spec["pixel"]["pitch_nm"])
    ant, feed = spec["antenna"], spec["photon_feed"]
    edge, thick, gap = float(ant["prism_edge_nm"]), float(ant["thickness_nm"]), val(ant["gap_nm"])
    wg_w = float(feed["waveguide"]["width_nm"])
    rows_per_wg = int(feed["waveguide"]["pixel_rows_per_waveguide"])
    lx, ly = nx * pitch, ny * pitch
    assy = cq.Assembly(name=f"{spec['meta']['name']} pixel block {nx}x{ny} (1 mm = 1 nm)")
    z = 0.0
    for layer in spec["layers"]:
        name, t = layer["name"], float(layer["thickness_nm"])
        if name == "contact":
            continue                                  # 2 um of contact adds nothing at this scale
        if name == "collector":
            assy.add(slab(lx, ly, collector_shown_nm), name=f"collector (top {collector_shown_nm:.0f} nm of {t:.0f} nm shown)",
                     loc=at(z=z), color=colour("collector"))
            z += collector_shown_nm
        elif name == "waveguide":
            period = rows_per_wg * pitch
            strip = slab(lx, wg_w, t)
            fill = slab(lx, (period - wg_w) / 2.0, t)
            for k in range(int(round(ly / period))):
                yc = -ly / 2.0 + (k + 0.5) * period
                assy.add(strip, name=f"waveguide_{k}", loc=at(y=yc, z=z), color=colour("waveguide"))
                for sgn in (-1, 1):
                    yo = yc + sgn * (wg_w / 2.0 + (period - wg_w) / 4.0)
                    assy.add(fill, name=f"side_cladding_{k}_{'a' if sgn < 0 else 'b'}", loc=at(y=yo, z=z),
                             color=colour("cladding"))
            z += t
        elif name == "reaction":
            h = edge * math.sqrt(3.0) / 2.0
            prism = (cq.Workplane("XY").polyline([(0.0, 0.0), (-edge / 2.0, h), (edge / 2.0, h)])
                     .close().extrude(t))             # apex at the origin, pointing to -y
            for i in range(nx):
                for j in range(ny):
                    cx = -lx / 2.0 + (i + 0.5) * pitch
                    cy = -ly / 2.0 + (j + 0.5) * pitch
                    assy.add(prism, name=f"antenna_{i}_{j}_a", loc=at(cx, cy + gap / 2.0, z),
                             color=colour("reaction"))
                    flipped = cq.Location(cq.Vector(cx, cy - gap / 2.0, z), cq.Vector(0, 0, 1), 180.0)
                    assy.add(prism, name=f"antenna_{i}_{j}_b", loc=flipped, color=colour("reaction"))
            z += t
        else:
            assy.add(slab(lx, ly, t), name=f"{name} ({layer['material']})", loc=at(z=z),
                     color=colour(name if name in COLOURS else "cladding"))
            z += t
    return assy


# --- L3-L5: v1 laser unit, 1 mm = 1 um ---------------------------------------------------
def build_laser_unit(spec, die_um=2000.0, tile_um=50.0, street_um=10.0, margin_um=100.0, extra_layers=4):
    layer_pitch = val(spec["stack"]["layer_pitch_um"])
    film = val(spec["site_crystal"]["film_thickness_nm"]) / 1000.0
    optics = 1.2                                                   # cladding + waveguide plane, um
    collector = layer_pitch - film - optics
    lx, ly, lz = (float(v) for v in spec["laser_unit"]["die_footprint_um"])
    field = die_um - 2.0 * margin_um - lx                          # room left for tiles beside the laser
    period = tile_um + street_um
    n = int(field // period)
    assy = cq.Assembly(name=f"{spec['meta']['name']} laser unit, {n * n} tiles per laser (1 mm = 1 um)")

    # lower layers of the stack, plain: same pattern, not repeated in detail
    plain = slab(die_um, die_um, layer_pitch)
    for k in range(extra_layers):
        assy.add(plain, name=f"layer_{k}", loc=at(z=k * layer_pitch),   # same pattern as the top layer
                 color=colour("collector"))
    z = extra_layers * layer_pitch
    assy.add(slab(die_um, die_um, collector), name="collector and heat spreader (diamond)", loc=at(z=z),
             color=colour("collector"))
    z += collector
    assy.add(slab(die_um, die_um, optics), name="optics: cladding and waveguide plane", loc=at(z=z),
             color=colour("optics"))
    z += optics

    x0 = -die_um / 2.0 + margin_um + lx                            # left edge of the tile field
    y0 = -n * period / 2.0
    tile = slab(tile_um, tile_um, film)
    for i in range(n):
        for j in range(n):
            assy.add(tile, name=f"tile_{i}_{j}", color=colour("film"),
                     loc=at(x0 + (i + 0.5) * period, y0 + (j + 0.5) * period, z))
    # waveguide tree: a trunk next to the laser, one branch per street
    wg_w, wg_h = 0.3, 0.2
    branch = slab(n * period, wg_w, wg_h)
    for j in range(n + 1):
        assy.add(branch, name=f"branch_waveguide_{j}", color=colour("waveguide"),
                 loc=at(x0 + n * period / 2.0, y0 + j * period, z))
    assy.add(slab(wg_w, n * period, wg_h), name="trunk_waveguide", loc=at(x0 - street_um / 2.0, 0.0, z),
             color=colour("waveguide"))
    assy.add(slab(lx, ly, lz), name="laser die (one per unit)", color=colour("laser"),
             loc=at(-die_um / 2.0 + margin_um / 2.0 + lx / 2.0, 0.0, z))
    return assy, n * n


def rename_products(path, mapping):
    """STEP names a shared shape (PRODUCT) after its first occurrence; viewers that list product
    names then show e.g. eight parts all called antenna_0_0_a.  Give shared shapes a neutral part
    name.  Occurrence names (NEXT_ASSEMBLY_USAGE_OCCURRENCE) are left untouched."""
    with open(path) as fh:
        text = fh.read()
    for first, neutral in mapping.items():
        old = f"PRODUCT('{first}','{first}'"
        if old not in text:
            raise ValueError(f"product {first!r} not found in {path}")
        text = text.replace(old, f"PRODUCT('{neutral}','{neutral}'")
    with open(path, "w") as fh:
        fh.write(text)


# Neutral names are kept short so the rewritten STEP lines stay within 72 columns.
PIXEL_PARTS = {"antenna_0_0_a": "antenna prism", "side_cladding_0_a": "side cladding",
               "waveguide_0": "waveguide strip"}
UNIT_PARTS = {"tile_0_0": "site-crystal tile", "branch_waveguide_0": "branch waveguide",
              "layer_0": "lower stack layer"}


def report(path):
    shape = cq.importers.importStep(path)
    bb = shape.val().BoundingBox()
    text = open(path).read()
    print(f"  {os.path.relpath(path, ROOT)}: {os.path.getsize(path) / 1e6:.2f} MB, "
          f"{shape.solids().size()} solids on re-import, {text.count('MANIFOLD_SOLID_BREP')} distinct shapes, "
          f"bounding box {bb.xlen:.0f} x {bb.ylen:.0f} x {bb.zlen:.1f} mm")


def main():
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(ROOT, "design", "nf-cell-v0.yaml")) as fh:
        v0 = yaml.safe_load(fh)
    with open(os.path.join(ROOT, "design", "nf-cell-v1.yaml")) as fh:
        v1 = yaml.safe_load(fh)
    p0 = os.path.join(OUT, "nf-cell-v0-pixel-block.step")
    build_pixel_block(v0).export(p0)
    rename_products(p0, PIXEL_PARTS)
    p1 = os.path.join(OUT, "nf-cell-v1-laser-unit.step")
    unit, tiles = build_laser_unit(v1)
    unit.export(p1)
    rename_products(p1, UNIT_PARTS)
    print("wrote:")
    report(p0)
    report(p1)
    pixels = tiles * (50.0e3 / val(v1["pixel"]["pitch_nm"])) ** 2
    print(f"  laser unit: {tiles} tiles = {pixels:.2e} pixels per laser die")
    if "--svg" in sys.argv:                           # hidden-line views, stack normal pointing up
        for path, direction, size in ((p0, (0.9, 0.55, 1.0), (520, 900)), (p1, (0.5, 0.75, 1.0), (1000, 520))):
            shape = cq.importers.importStep(path).rotate((0, 0, 0), (1, 0, 0), -90)
            cq.exporters.export(shape, path.replace(".step", ".svg"),
                                opt={"projectionDir": direction, "showAxes": False, "showHidden": False,
                                     "width": size[0], "height": size[1], "strokeWidth": -1.0,
                                     "marginLeft": 20, "marginTop": 20})
            print("  drew", os.path.relpath(path.replace(".step", ".svg"), ROOT))


if __name__ == "__main__":
    main()
