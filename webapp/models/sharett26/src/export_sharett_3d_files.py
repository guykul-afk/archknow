# -*- coding: utf-8 -*-
import os, json, struct, math

WORKSPACE = r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה"
DATA_DIR = os.path.join(WORKSPACE, "data")

with open(os.path.join(DATA_DIR, "sharett_extracted_plans.json"), "r", encoding="utf-8") as f:
    plans_data = json.load(f)

FLOORS = [
    {"id": "bm2", "sheet": "basement_2",   "zFloor": -6.00, "zCeil": -3.20, "zTop": -3.00},
    {"id": "bm1", "sheet": "basement_1",   "zFloor": -3.00, "zCeil": -0.20, "zTop":  0.00},
    {"id": "kar", "sheet": "ground",       "zFloor":  0.00, "zCeil":  2.90, "zTop":  3.10},
    {"id": "gal", "sheet": "gallery",      "zFloor":  3.10, "zCeil":  5.90, "zTop":  6.12},
    {"id": "f1",  "sheet": "floors_1267",  "zFloor":  6.12, "zCeil":  9.05, "zTop":  9.27},
    {"id": "f2",  "sheet": "floors_1267",  "zFloor":  9.27, "zCeil": 12.20, "zTop": 12.42},
    {"id": "f3",  "sheet": "floors_345",   "zFloor": 12.42, "zCeil": 15.35, "zTop": 15.57},
    {"id": "f4",  "sheet": "floors_345",   "zFloor": 15.57, "zCeil": 18.50, "zTop": 18.72},
    {"id": "f5",  "sheet": "floors_345",   "zFloor": 18.72, "zCeil": 21.65, "zTop": 21.87},
    {"id": "f6",  "sheet": "floors_1267",  "zFloor": 21.87, "zCeil": 24.80, "zTop": 25.02},
    {"id": "f7",  "sheet": "floors_1267",  "zFloor": 25.02, "zCeil": 27.95, "zTop": 28.17},
    {"id": "f8",  "sheet": "floor_8",      "zFloor": 28.17, "zCeil": 31.10, "zTop": 31.32},
    {"id": "f9",  "sheet": "floor_9_roof", "zFloor": 31.32, "zCeil": 33.77, "zTop": 33.77},
    {"id": "gag", "sheet": "upper_roof",   "zFloor": 33.77, "zCeil": 34.27, "zTop": 34.45},
]

MATERIALS = {
    "ext_white":      (0.97, 0.97, 0.96, 1.0),
    "int_wall":       (0.92, 0.89, 0.85, 1.0),
    "hpl_wood":       (0.68, 0.45, 0.28, 1.0),
    "slab_floor":     (0.84, 0.85, 0.88, 1.0),
    "wood_deck":      (0.66, 0.44, 0.29, 1.0),
    "synthetic_turf": (0.13, 0.68, 0.30, 1.0),
    "garden_grass":   (0.28, 0.78, 0.42, 1.0),
    "terracotta":     (0.88, 0.71, 0.60, 1.0),
    "glass_blue":     (0.74, 0.88, 0.96, 0.45),
    "alu_dark":       (0.22, 0.24, 0.27, 1.0),
    "oak_furn":       (0.76, 0.60, 0.40, 1.0),
    "calacatta":      (0.96, 0.95, 0.93, 1.0),
}

meshes_by_mat = {k: [] for k in MATERIALS}

def add_box(mat_name, x0, y0, x1, y1, z0, z1):
    xa, xb = min(x0, x1), max(x0, x1)
    ya, yb = min(y0, y1), max(y0, y1)
    za, zb = min(z0, z1), max(z0, z1)
    if xb - xa < 0.002 or yb - ya < 0.002 or zb - za < 0.002:
        return
    p000 = (xa, za, ya)
    p100 = (xb, za, ya)
    p101 = (xb, za, yb)
    p001 = (xa, za, yb)
    p010 = (xa, zb, ya)
    p110 = (xb, zb, ya)
    p111 = (xb, zb, yb)
    p011 = (xa, zb, yb)
    tris = [
        (p010, p011, p111), (p010, p111, p110),
        (p000, p100, p101), (p000, p101, p001),
        (p001, p101, p111), (p001, p111, p011),
        (p100, p000, p010), (p100, p010, p110),
        (p101, p100, p110), (p101, p110, p111),
        (p000, p001, p011), (p000, p011, p010),
    ]
    meshes_by_mat[mat_name].extend(tris)

def add_footprint_slab(mat_name, y_south, z0, z1, is_ground=False, is_gal=False):
    add_box(mat_name, -16.87, -13.24,  -3.17, -2.99, z0, z1)
    add_box(mat_name,   2.93, -13.24,  16.63, -2.99, z0, z1)
    add_box(mat_name,  -3.17,  -3.42,   2.93,  0.63 if is_gal else 3.82, z0, z1)
    if is_gal:
        # On Gallery (+3.10), slab covers ONLY North Duplex wing & core corridor (Y <= +0.63)
        add_box(mat_name, -15.34, -2.99, -3.17, 0.63, z0, z1)
        add_box(mat_name,   2.93, -2.99, 15.10, 0.63, z0, z1)
        return
    add_box(mat_name, -15.34,  -2.99,  -3.17,  3.40, z0, z1)
    add_box(mat_name, -15.34 if is_ground else -16.87, 3.40, -3.17, y_south, z0, z1)
    add_box(mat_name,   2.93,  -2.99,  15.10,  3.40, z0, z1)
    add_box(mat_name,   2.93,   3.40,  16.63, y_south, z0, z1)

def add_sloped_ramp(mat_name, x0, y0, x1, y1, z_at_min, z_at_max, slope_axis, thick):
    z00 = z_at_min
    z10 = z_at_max if slope_axis == "X" else z_at_min
    z11 = z_at_max
    z01 = z_at_min if slope_axis == "X" else z_at_max
    b00, b10, b11, b01 = z00 - thick, z10 - thick, z11 - thick, z01 - thick
    p010, p110, p111, p011 = (x0, z00, y0), (x1, z10, y0), (x1, z11, y1), (x0, z01, y1)
    p000, p100, p101, p001 = (x0, b00, y0), (x1, b10, y0), (x1, b11, y1), (x0, b01, y1)
    tris = [
        (p010, p011, p111), (p010, p111, p110),
        (p000, p100, p101), (p000, p101, p001),
        (p001, p101, p111), (p001, p111, p011),
        (p100, p000, p010), (p100, p010, p110),
        (p101, p100, p110), (p101, p110, p111),
        (p000, p001, p011), (p000, p011, p010),
    ]
    meshes_by_mat[mat_name].extend(tris)

def add_extruded_poly(mat_name, poly_data, z0, z1):
    pts = poly_data["pts"]
    tris_idx = poly_data.get("tris_idx", [])
    if not pts or not tris_idx:
        return
    edge_counts = {}
    for (i0, i1, i2) in tris_idx:
        p0, p1, p2 = pts[i0], pts[i1], pts[i2]
        v0 = (p0[0], z1, p0[1])
        v1 = (p1[0], z1, p1[1])
        v2 = (p2[0], z1, p2[1])
        meshes_by_mat[mat_name].append((v0, v2, v1))
        b0 = (p0[0], z0, p0[1])
        b1 = (p1[0], z0, p1[1])
        b2 = (p2[0], z0, p2[1])
        meshes_by_mat[mat_name].append((b0, b1, b2))
        for a, b in ((i0, i1), (i1, i2), (i2, i0)):
            key = (min(a, b), max(a, b))
            edge_counts[key] = edge_counts.get(key, 0) + 1

    for (ia, ib), cnt in edge_counts.items():
        if cnt == 1:
            pa, pb = pts[ia], pts[ib]
            a0 = (pa[0], z0, pa[1])
            a1 = (pb[0], z0, pb[1])
            a2 = (pb[0], z1, pb[1])
            a3 = (pa[0], z1, pa[1])
            meshes_by_mat[mat_name].append((a0, a1, a2))
            meshes_by_mat[mat_name].append((a0, a2, a3))

def add_dual_core_stairs(zf, zc):
    zmid = 0.5 * (zf + zc)
    for cx in (-10.72, 10.48):
        add_box("slab_floor", cx - 1.15, -4.02, cx + 1.15, -3.15, zmid - 0.14, zmid)
        n_steps = 8
        sy0, sy1 = -3.15, -1.10
        dy = (sy1 - sy0) / n_steps
        dz1 = (zmid - zf) / n_steps
        dz2 = (zc - zmid) / n_steps
        for i in range(n_steps):
            add_box("slab_floor", cx + 0.06, sy1 - (i + 1) * dy, cx + 1.10, sy1 - i * dy, zf + i * dz1 - 0.06, zf + (i + 1) * dz1)
            add_box("slab_floor", cx - 1.10, sy0 + i * dy, cx - 0.06, sy0 + (i + 1) * dy, zmid + i * dz2 - 0.06, zmid + (i + 1) * dz2)

for f in FLOORS:
    fid = f["id"]
    zf, zc, ztop = f["zFloor"], f["zCeil"], f["zTop"]
    pdata = plans_data[f["sheet"]]
    if fid not in ("gag",):
        add_dual_core_stairs(zf, zc)

    if fid in ("bm2", "bm1"):
        add_box("slab_floor", -20.48, -17.71, 20.48, 17.50, zf - 0.35, zf)
        if fid == "bm1":
            add_sloped_ramp("alu_dark", -20.15, -2.99, -15.34, 17.20, -3.00, 0.00, "Y", 0.24)
        else:
            add_sloped_ramp("alu_dark", -20.15, -14.50, -15.34,  2.50, -6.00, -3.00, "Y", 0.24)
    elif fid == "kar":
        # Ground slab with open cut for the 2-way underground garage ramp at X = [-20.15, -15.34], Y = [-2.99, +17.20]
        add_box("slab_floor", -20.48, -17.71,  20.48,  -2.99, -0.25, -0.02)
        add_box("slab_floor", -15.34,  -2.99,  20.48,  17.50, -0.25, -0.02)
        add_box("slab_floor", -20.48,  -2.99, -20.15,  17.50, -0.25, -0.02)
        add_sloped_ramp("alu_dark", -20.15, -2.99, -15.34, 17.20, -3.00, 0.00, "Y", 0.22)
        # Gardens & Terracotta Entrance Courtyard
        add_box("garden_grass", -20.10, -17.35, 19.85, -15.00, 0.00, 0.06)
        add_box("garden_grass",  -3.17, -15.00,  2.93,  -5.20, 0.00, 0.06)
        add_box("garden_grass", -20.10, -15.00, -16.87, -3.15, 0.00, 0.06)
        add_box("garden_grass",  16.63, -15.00, 19.85,   3.40, 0.00, 0.06)
        add_box("garden_grass", -13.50,  13.65, -6.80,  17.15, 0.00, 0.16)
        add_box("garden_grass",   2.93,  13.65, 11.80,  17.15, 0.00, 0.16)
        add_box("garden_grass",  -1.05,   5.40,  0.85,  14.60, 0.00, 0.18)
        add_box("terracotta",    -6.80,   3.82,  2.93,  17.50, 0.00, 0.03)
        add_box("terracotta",    11.80,  13.65, 18.30,  17.50, 0.00, 0.03)
        add_box("alu_dark",     -24.00,  17.50, 24.00,  24.50, -0.28, -0.10)
        add_footprint_slab("slab_floor", 13.65, -0.22, 0.00, is_ground=True)
    elif fid == "gal":
        add_footprint_slab("slab_floor", 13.65, zf - 0.22, zf, is_gal=True)
        for hx0, hx1 in [(-14.64, -11.74), (-8.14, -5.24), (5.00, 7.90), (11.50, 14.40)]:
            add_box("hpl_wood", hx0, -13.28, hx1, -13.20, zf + 0.35, zf + 2.25)
    elif fid in ("f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8"):
        y_south = 12.15 if fid == "f8" else 13.65
        add_footprint_slab("slab_floor", y_south, zf - 0.22, zf)
        # 4 North Sun Balconies spanning full half-wing width (6.85m each)
        for bx0, bx1 in [(-16.87, -10.12), (-9.92, -3.17), (2.93, 9.68), (9.88, 16.63)]:
            add_box("ext_white", bx0, -14.99, bx1, -13.24, zf - 0.24, zf - 0.02)
            add_box("wood_deck", bx0 + 0.05, -14.94, bx1 - 0.05, -13.24, zf - 0.02, zf + 0.02)
            add_box("alu_dark",  bx0, -14.99, bx1, -14.91, zf + 1.01, zf + 1.05)
        if fid == "f8":
            for bx0, bx1 in [(-16.87, -3.17), (2.93, 16.63)]:
                add_box("ext_white", bx0, 12.15, bx1, 14.65, zf - 0.24, zf - 0.02)
                add_box("wood_deck", bx0 + 0.08, 12.15, bx1 - 0.08, 14.55, zf - 0.02, zf + 0.02)
                add_box("alu_dark",  bx0, 14.58, bx1, 14.65, zf + 1.01, zf + 1.05)
        else:
            for bx0, bx1 in [(-16.87, -10.12), (-9.92, -3.17), (2.93, 9.68), (9.88, 16.63)]:
                add_box("ext_white", bx0, 13.65, bx1, 15.40, zf - 0.24, zf - 0.02)
                add_box("wood_deck", bx0 + 0.05, 13.65, bx1 - 0.05, 15.35, zf - 0.02, zf + 0.02)
                add_box("alu_dark",  bx0, 15.32, bx1, 15.40, zf + 1.01, zf + 1.05)
        for hx0, hx1 in [(-14.64, -13.54), (-10.54, -9.34), (-6.34, -5.24), (5.00, 6.10), (9.10, 10.30), (13.30, 14.40)]:
            add_box("hpl_wood", hx0, -13.28, hx1, -13.20, zf, zf + 2.25)
            if fid != "f8":
                add_box("hpl_wood", hx0, 13.61, hx1, 13.69, zf, zf + 2.25)
    elif fid == "f9":
        add_footprint_slab("slab_floor", 12.15, zf - 0.25, zf)
        z_par = zf + 1.05
        # Solid white perimeter parapet (+31.32 .. +32.37) & South Private Roof Terraces with Synthetic Turf (דשא סינטטי)!
        add_box("synthetic_turf", -16.65, 3.62, -3.39, 11.95, zf, zf + 0.04)
        add_box("synthetic_turf",   3.15, 3.62, 16.41, 11.95, zf, zf + 0.04)
        add_box("ext_white", -16.87, -13.24,  -3.17, -13.04, zf, z_par)
        add_box("ext_white",   2.93, -13.24,  16.63, -13.04, zf, z_par)
        add_box("ext_white", -16.87,  11.95,  -3.17,  12.15, zf, z_par)
        add_box("ext_white",   2.93,  11.95,  16.63,  12.15, zf, z_par)
        add_box("ext_white", -16.87, -13.24, -16.67,  -2.99, zf, z_par)
        add_box("ext_white", -15.34,  -2.99, -15.14,   3.40, zf, z_par)
        add_box("ext_white", -16.87,   3.40, -16.67,  12.15, zf, z_par)
        add_box("ext_white",  16.43, -13.24,  16.63,  -2.99, zf, z_par)
        add_box("ext_white",  14.90,  -2.99,  15.10,   3.40, zf, z_par)
        add_box("ext_white",  16.43,   3.40,  16.63,  12.15, zf, z_par)
    elif fid == "gag":
        add_box("ext_white", -12.15, -4.28, -9.30, 0.63, zf - 0.20, zf)
        add_box("ext_white",   9.05, -4.28, 11.91, 0.63, zf - 0.20, zf)
        add_box("ext_white", -12.15, -2.06, -9.30, 0.63, zc - 0.18, zc)
        add_box("ext_white",   9.05, -2.06, 11.91, 0.63, zc - 0.18, zc)

    wall_mat = "slab_floor" if fid in ("bm2", "bm1") else "ext_white"
    z_wall_top = ztop if fid in ("kar", "gal") else zc
    for wp in pdata["wall_polys"]:
        add_extruded_poly(wall_mat, wp, zf, z_wall_top)

    for op in pdata.get("openings", []):
        orient, x0, y0, x1, y1, kind = op
        if kind == "dh_void":
            add_box("ext_white", x0, y0, x1, y1, 4.50, z_wall_top)
        elif kind in ("vitrine_dh", "curtain_3bay_dh"):
            add_box("alu_dark", x0, y0, x1, y1, 0.00, 0.06)
            add_box("alu_dark", x0, y0, x1, y1, 4.44, 4.50)
            add_box("glass_blue", x0, y0, x1, y1, 0.06, 4.44)
        elif kind == "gate_louver_dh":
            add_box("alu_dark", x0, y0, x1, y1, 0.00, 4.50)
        elif kind in ("vitrine", "win_tall", "window", "win_small", "win_recess", "win_gal", "win_balc"):
            zsill = zf + (0.02 if kind == "vitrine" else (1.35 if kind == "win_small" else (0.70 if kind == "win_recess" else (0.35 if kind in ("win_gal", "win_balc", "win_tall") else 1.05))))
            zhead = min(zf + 2.25, zc - 0.15)
            if zsill > zf + 0.05:
                add_box("ext_white", x0, y0, x1, y1, zf, zsill)
            if z_wall_top > zhead + 0.02:
                add_box("ext_white", x0, y0, x1, y1, zhead, z_wall_top)
            add_box("alu_dark", x0, y0, x1, y1, zsill, zsill + 0.05)
            add_box("alu_dark", x0, y0, x1, y1, zhead - 0.05, zhead)
            add_box("glass_blue", x0, y0, x1, y1, zsill + 0.05, zhead - 0.05)
        elif kind in ("louver", "louver_Recess"):
            zsill = zf + (1.05 if kind == "louver_Recess" else 0.15)
            zhead = (zf + 2.25) if kind == "louver_Recess" else (zc - 0.12)
            add_box("ext_white", x0, y0, x1, y1, zf, zsill)
            add_box("ext_white", x0, y0, x1, y1, zhead, z_wall_top)
            add_box("alu_dark", x0, y0, x1, y1, zsill, zhead)
        elif kind == "door":
            zhead = min(zf + 2.10, zc - 0.15)
            add_box("oak_furn", x0, y0, x1, y1, zf, zhead)

# Write MTL & OBJ
mtl_lines = ["# Moshe Sharett 26-28 Petah Tikva - MTL Library"]
for mname, rgba in MATERIALS.items():
    mtl_lines.append(f"newmtl {mname}")
    mtl_lines.append(f"Kd {rgba[0]:.3f} {rgba[1]:.3f} {rgba[2]:.3f}")
    mtl_lines.append(f"d {rgba[3]:.2f}")
    mtl_lines.append("")

obj_lines = [
    "# Moshe Sharett 26-28 Petah Tikva - 1:1 Metric Architectural BIM Model",
    "mtllib sharett26_28_model.mtl"
]
v_idx = 1
for mname, tris in meshes_by_mat.items():
    if not tris:
        continue
    obj_lines.append(f"g {mname}")
    obj_lines.append(f"usemtl {mname}")
    for (v0, v1, v2) in tris:
        obj_lines.append(f"v {v0[0]:.4f} {v0[1]:.4f} {v0[2]:.4f}")
        obj_lines.append(f"v {v1[0]:.4f} {v1[1]:.4f} {v1[2]:.4f}")
        obj_lines.append(f"v {v2[0]:.4f} {v2[1]:.4f} {v2[2]:.4f}")
        obj_lines.append(f"f {v_idx} {v_idx+1} {v_idx+2}")
        v_idx += 3

# Write binary GLB (glTF 2.0)
bin_chunks = bytearray()
buffer_views = []
accessors = []
gltf_meshes = []
gltf_nodes = []
gltf_materials = []

mat_keys = [k for k in MATERIALS if meshes_by_mat[k]]
for idx, mname in enumerate(mat_keys):
    rgba = MATERIALS[mname]
    mat_def = {
        "name": mname,
        "pbrMetallicRoughness": {
            "baseColorFactor": [rgba[0], rgba[1], rgba[2], rgba[3]],
            "metallicFactor": 0.1 if mname != "alu_dark" else 0.6,
            "roughnessFactor": 0.7 if mname != "glass_blue" else 0.15
        },
        "doubleSided": True
    }
    if rgba[3] < 1.0:
        mat_def["alphaMode"] = "BLEND"
    gltf_materials.append(mat_def)

    tris = meshes_by_mat[mname]
    pos_bytes = bytearray()
    min_x = min_y = min_z = 1e9
    max_x = max_y = max_z = -1e9
    for (v0, v1, v2) in tris:
        for vx, vy, vz in (v0, v1, v2):
            pos_bytes.extend(struct.pack("<3f", vx, vy, vz))
            if vx < min_x: min_x = vx
            if vy < min_y: min_y = vy
            if vz < min_z: min_z = vz
            if vx > max_x: max_x = vx
            if vy > max_y: max_y = vy
            if vz > max_z: max_z = vz

    offset = len(bin_chunks)
    bin_chunks.extend(pos_bytes)
    while len(bin_chunks) % 4 != 0:
        bin_chunks.append(0)

    bv_idx = len(buffer_views)
    buffer_views.append({
        "buffer": 0,
        "byteOffset": offset,
        "byteLength": len(pos_bytes),
        "target": 34962
    })
    acc_idx = len(accessors)
    accessors.append({
        "bufferView": bv_idx,
        "byteOffset": 0,
        "componentType": 5126,
        "count": len(tris) * 3,
        "type": "VEC3",
        "min": [round(min_x, 4), round(min_y, 4), round(min_z, 4)],
        "max": [round(max_x, 4), round(max_y, 4), round(max_z, 4)]
    })
    gltf_meshes.append({
        "name": f"mesh_{mname}",
        "primitives": [{"attributes": {"POSITION": acc_idx}, "material": idx, "mode": 4}]
    })
    gltf_nodes.append({"name": mname, "mesh": idx})

gltf_json = {
    "asset": {"version": "2.0", "generator": "Moshe Sharett 26-28 BIM Exporter"},
    "scene": 0,
    "scenes": [{"name": "MosheSharett26_28", "nodes": list(range(len(gltf_nodes)))}],
    "nodes": gltf_nodes,
    "meshes": gltf_meshes,
    "materials": gltf_materials,
    "accessors": accessors,
    "bufferViews": buffer_views,
    "buffers": [{"byteLength": len(bin_chunks)}]
}

json_bytes = json.dumps(gltf_json, separators=(",", ":")).encode("utf-8")
while len(json_bytes) % 4 != 0:
    json_bytes += b" "

total_len = 12 + 8 + len(json_bytes) + 8 + len(bin_chunks)
glb_bytes = bytearray()
glb_bytes.extend(struct.pack("<4sII", b"glTF", 2, total_len))
glb_bytes.extend(struct.pack("<I4s", len(json_bytes), b"JSON"))
glb_bytes.extend(json_bytes)
glb_bytes.extend(struct.pack("<I4s", len(bin_chunks), b"BIN\x00"))
glb_bytes.extend(bin_chunks)

for d in (WORKSPACE, DATA_DIR):
    with open(os.path.join(d, "sharett26_28_model.mtl"), "w", encoding="utf-8") as f:
        f.write("\n".join(mtl_lines))
    with open(os.path.join(d, "sharett26_28_model.obj"), "w", encoding="utf-8") as f:
        f.write("\n".join(obj_lines))
    with open(os.path.join(d, "sharett26_28_model.glb"), "wb") as f:
        f.write(glb_bytes)

print(f"Exported OBJ ({len(obj_lines)} lines) and GLB ({len(glb_bytes)/(1024*1024):.2f} MB) to workspace and data/")
