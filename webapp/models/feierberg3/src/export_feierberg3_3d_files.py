# -*- coding: utf-8 -*-
import os
import sys
import json
import struct

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\פאירברג 3 פתח תקווה"
DATA_DIR    = os.path.join(PROJECT_DIR, "data")

with open(os.path.join(DATA_DIR, "feierberg3_extracted_plans.json"), "r", encoding="utf-8") as f:
    plans_data = json.load(f)

FLOORS = [
    {"id": "b2",  "sheet": "basement_2", "zFloor": -7.80, "zCeil": -4.80},
    {"id": "b1",  "sheet": "basement_1", "zFloor": -4.80, "zCeil":  0.00},
    {"id": "kar", "sheet": "ground",     "zFloor":  0.00, "zCeil":  3.50},
    {"id": "f1",  "sheet": "floors_1_7", "zFloor":  3.50, "zCeil":  6.65},
    {"id": "f2",  "sheet": "floors_1_7", "zFloor":  6.65, "zCeil":  9.80},
    {"id": "f3",  "sheet": "floors_1_7", "zFloor":  9.80, "zCeil": 12.95},
    {"id": "f4",  "sheet": "floors_1_7", "zFloor": 12.95, "zCeil": 16.10},
    {"id": "f5",  "sheet": "floors_1_7", "zFloor": 16.10, "zCeil": 19.25},
    {"id": "f6",  "sheet": "floors_1_7", "zFloor": 19.25, "zCeil": 22.40},
    {"id": "f7",  "sheet": "floors_1_7", "zFloor": 22.40, "zCeil": 25.55},
    {"id": "f8",  "sheet": "floor_8",    "zFloor": 25.55, "zCeil": 28.87},
    {"id": "f9",  "sheet": "floor_9",    "zFloor": 28.87, "zCeil": 32.02},
    {"id": "f10", "sheet": "floor_10",   "zFloor": 32.02, "zCeil": 35.17},
    {"id": "gag", "sheet": "roof",       "zFloor": 35.17, "zCeil": 37.50},
]

MATERIALS = {
    "ext_white":      (0.97, 0.97, 0.96, 1.0),
    "charcoal_crown": (0.20, 0.22, 0.25, 1.0),
    "int_wall":       (0.95, 0.95, 0.94, 1.0),
    "bronze_portal":  (0.45, 0.36, 0.29, 1.0),
    "shutter_box":    (0.24, 0.25, 0.27, 1.0),
    "slab_floor":     (0.88, 0.90, 0.92, 1.0),
    "glass_blue":     (0.55, 0.76, 0.96, 0.48),
    "alu_dark":       (0.11, 0.13, 0.16, 1.0),
    "oak_furn":       (0.76, 0.59, 0.40, 1.0),
}

meshes_by_mat = {k: [] for k in MATERIALS}


def add_box(mat_name, x0, z0, x1, z1, y0, y1):
    xa, xb = min(x0, x1), max(x0, x1)
    za, zb = min(z0, z1), max(z0, z1)
    ya, yb = min(y0, y1), max(y0, y1)
    if xb - xa < 0.002 or zb - za < 0.002 or yb - ya < 0.002:
        return
    p000 = (xa, ya, za)
    p100 = (xb, ya, za)
    p101 = (xb, ya, zb)
    p001 = (xa, ya, zb)
    p010 = (xa, yb, za)
    p110 = (xb, yb, za)
    p111 = (xb, yb, zb)
    p011 = (xa, yb, zb)
    tris = [
        (p010, p011, p111), (p010, p111, p110),
        (p000, p100, p101), (p000, p101, p001),
        (p001, p101, p111), (p001, p111, p011),
        (p100, p000, p010), (p100, p010, p110),
        (p101, p100, p110), (p101, p110, p111),
        (p000, p001, p011), (p000, p011, p010),
    ]
    meshes_by_mat[mat_name].extend(tris)


def add_extruded_poly(mat_name, poly_data, y0, y1):
    tris = poly_data.get("tris", [])
    for i in range(0, len(tris) - 2, 3):
        p0, p1, p2 = tris[i], tris[i + 1], tris[i + 2]
        v0 = (p0[0], y1, p0[1])
        v1 = (p1[0], y1, p1[1])
        v2 = (p2[0], y1, p2[1])
        meshes_by_mat[mat_name].append((v0, v2, v1))
        b0 = (p0[0], y0, p0[1])
        b1 = (p1[0], y0, p1[1])
        b2 = (p2[0], y0, p2[1])
        meshes_by_mat[mat_name].append((b0, b1, b2))
    outline = poly_data.get("outline") or poly_data.get("exterior") or []
    rings = [outline] + poly_data.get("holes", [])
    for ring in rings:
        n = len(ring)
        for i in range(n):
            p1 = ring[i]
            p2 = ring[(i + 1) % n]
            a0 = (p1[0], y0, p1[1])
            a1 = (p2[0], y0, p2[1])
            a2 = (p2[0], y1, p2[1])
            a3 = (p1[0], y1, p1[1])
            meshes_by_mat[mat_name].append((a0, a1, a2))
            meshes_by_mat[mat_name].append((a0, a2, a3))


for f in FLOORS:
    zf, zc = f["zFloor"], f["zCeil"]
    pdata = plans_data[f["sheet"]]
    wall_mat = "charcoal_crown" if f["id"] in ("f9", "f10") else ("slab_floor" if f["id"] in ("b1", "b2") else "ext_white")

    # Floor Slab
    if pdata.get("slab_poly"):
        slab_thick = 0.35 if f["id"] in ("b1", "b2") else 0.22
        add_extruded_poly("slab_floor", pdata["slab_poly"], zf - slab_thick, zf)

    # Balconies & Roof Terraces
    for bp in pdata.get("balc_polys", []):
        add_extruded_poly("ext_white", bp, zf - 0.22, zf + 0.02)

    # Balcony Glass Railings & Aluminum Top/Bottom Rails
    for rs in pdata.get("railing_segs", []):
        add_box("alu_dark",   rs[0] - 0.03, rs[1] - 0.03, rs[2] + 0.03, rs[3] + 0.03, zf + 0.05, zf + 0.10)
        add_box("glass_blue", rs[0] - 0.01, rs[1] - 0.01, rs[2] + 0.01, rs[3] + 0.01, zf + 0.10, zf + 1.05)
        add_box("alu_dark",   rs[0] - 0.03, rs[1] - 0.03, rs[2] + 0.03, rs[3] + 0.03, zf + 1.05, zf + 1.10)

    # Overhead Pergolas on Floor 8 & Floor 9
    for pp in pdata.get("pergola_polys", []):
        add_extruded_poly("bronze_portal", pp, zc - 0.22, zc - 0.04)

    # 2-Story Architectural Facade C-Frames & Laundry Louvers on Typical Floors 1-8
    if f["id"] in ("f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8"):
        # Laundry louver screens (מסתורי כביסה) on North-West and East facades
        y_louver = zf + 0.15
        while y_louver < zc - 0.15:
            add_box("bronze_portal", -7.97, -4.18, -6.47, -4.08, y_louver, y_louver + 0.05)
            add_box("bronze_portal", 13.02, -0.90, 13.14,  0.60, y_louver, y_louver + 0.05)
            y_louver += 0.14
        # 2-story dark charcoal accent bands between window pairs on South/North/East/West facades
        add_box("charcoal_crown", -13.18,  1.85, -13.11,  3.25, zf, zc)
        add_box("charcoal_crown",  13.11, -3.15,  13.18, -1.85, zf, zc)

    # Ground Floor Street Colonnade Pilotis Columns (5 round/octagonal columns along South facade)
    if f["id"] == "kar":
        for cx in (-12.75, -7.65, 2.55, 7.65, 12.75):
            add_box("ext_white", cx - 0.28, 3.57, cx + 0.28, 4.13, 0.00, 3.50)

    # Extrude Wall Polygons
    for wp in pdata.get("wall_polys", []):
        add_extruded_poly(wall_mat, wp, zf, zc)

    # Window Sill Walls, Overhead Lintels, Aluminum Frames, Glass Panes & Wood Doors
    for op in pdata.get("openings", []):
        orient, x0, z0, x1, z1, kind = op
        if kind in ("vitrine", "win_tall", "window", "mamad_win"):
            zsill = zf + (0.02 if kind == "vitrine" else (0.45 if kind == "win_tall" else 1.00))
            zhead = min(zf + (2.25 if kind == "vitrine" else 2.15), zc - 0.18)
            if zsill > zf + 0.03:
                add_box(wall_mat, x0, z0, x1, z1, zf, zsill)
            if kind == "vitrine":
                zshut = min(zhead + 0.24, zc)
                add_box("shutter_box", x0, z0, x1, z1, zhead, zshut)
                if zc > zshut + 0.02:
                    add_box(wall_mat, x0, z0, x1, z1, zshut, zc)
            elif zc > zhead + 0.02:
                add_box(wall_mat, x0, z0, x1, z1, zhead, zc)
            add_box("alu_dark",   x0, z0, x1, z1, zsill, zsill + 0.05)
            add_box("alu_dark",   x0, z0, x1, z1, zhead - 0.05, zhead)
            add_box("glass_blue", x0, z0, x1, z1, zsill + 0.05, zhead - 0.05)
        elif kind == "door":
            zhead = min(zf + 2.10, zc - 0.15)
            if zc > zhead + 0.02:
                add_box("int_wall", x0, z0, x1, z1, zhead, zc)
            add_box("oak_furn", x0, z0, x1, z1, zf, zhead)

# Upper Roof Bulkhead Cap Slab at +37.50m
if "roof" in plans_data and plans_data["roof"].get("slab_poly"):
    add_extruded_poly("ext_white", plans_data["roof"]["slab_poly"], 37.50, 37.72)

# Write Wavefront MTL & OBJ
mtl_lines = ["# Feierberg 3 Petah Tikva - MTL Library"]
for mname, rgba in MATERIALS.items():
    mtl_lines.append(f"newmtl {mname}")
    mtl_lines.append(f"Kd {rgba[0]:.3f} {rgba[1]:.3f} {rgba[2]:.3f}")
    mtl_lines.append(f"d {rgba[3]:.2f}")
    mtl_lines.append("")

obj_lines = [
    "# Feierberg 3 Petah Tikva - 1:1 Metric Architectural BIM Model",
    "mtllib feierberg3_model.mtl"
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

# Write Binary glTF 2.0 (.glb)
bin_chunks = bytearray()
buffer_views = []
accessors = []
gltf_materials = []
gltf_primitives = []

mat_keys = [k for k, t in meshes_by_mat.items() if len(t) > 0]
for m_i, mname in enumerate(mat_keys):
    rgba = MATERIALS[mname]
    mat_def = {
        "name": mname,
        "pbrMetallicRoughness": {
            "baseColorFactor": [rgba[0], rgba[1], rgba[2], rgba[3]],
            "metallicFactor": 0.1,
            "roughnessFactor": 0.65
        },
        "doubleSided": True
    }
    if rgba[3] < 0.99:
        mat_def["alphaMode"] = "BLEND"
    gltf_materials.append(mat_def)

    tris = meshes_by_mat[mname]
    floats = []
    min_v = [1e9, 1e9, 1e9]
    max_v = [-1e9, -1e9, -1e9]
    for (v0, v1, v2) in tris:
        for vx, vy, vz in (v0, v1, v2):
            floats.extend([vx, vy, vz])
            if vx < min_v[0]: min_v[0] = vx
            if vy < min_v[1]: min_v[1] = vy
            if vz < min_v[2]: min_v[2] = vz
            if vx > max_v[0]: max_v[0] = vx
            if vy > max_v[1]: max_v[1] = vy
            if vz > max_v[2]: max_v[2] = vz

    raw_bytes = struct.pack(f"<{len(floats)}f", *floats)
    offset = len(bin_chunks)
    bin_chunks.extend(raw_bytes)
    while len(bin_chunks) % 4 != 0:
        bin_chunks.append(0)

    bv_idx = len(buffer_views)
    buffer_views.append({
        "buffer": 0,
        "byteOffset": offset,
        "byteLength": len(raw_bytes),
        "target": 34962
    })
    acc_idx = len(accessors)
    accessors.append({
        "bufferView": bv_idx,
        "byteOffset": 0,
        "componentType": 5126,
        "count": len(tris) * 3,
        "type": "VEC3",
        "min": [round(x, 4) for x in min_v],
        "max": [round(x, 4) for x in max_v]
    })
    gltf_primitives.append({
        "attributes": {"POSITION": acc_idx},
        "material": m_i,
        "mode": 4
    })

gltf_json = {
    "asset": {"version": "2.0", "generator": "Kolsky BIM Compiler - Feierberg 3 Petah Tikva"},
    "scene": 0,
    "scenes": [{"nodes": [0]}],
    "nodes": [{"name": "Feierberg3_BIM", "mesh": 0}],
    "meshes": [{"name": "Feierberg3_Mesh", "primitives": gltf_primitives}],
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
glb_bytes.extend(struct.pack("<III", 0x46546C67, 2, total_len))
glb_bytes.extend(struct.pack("<II", len(json_bytes), 0x4E4F534A))
glb_bytes.extend(json_bytes)
glb_bytes.extend(struct.pack("<II", len(bin_chunks), 0x004E4942))
glb_bytes.extend(bin_chunks)

with open(os.path.join(PROJECT_DIR, "feierberg3_model.mtl"), "w", encoding="utf-8") as f:
    f.write("\n".join(mtl_lines))
with open(os.path.join(PROJECT_DIR, "feierberg3_model.obj"), "w", encoding="utf-8") as f:
    f.write("\n".join(obj_lines))
with open(os.path.join(PROJECT_DIR, "feierberg3_model.glb"), "wb") as f:
    f.write(glb_bytes)

print(f"Exported 3D BIM files (.obj: {len(obj_lines):,} lines, .glb: {len(glb_bytes):,} bytes) to {PROJECT_DIR}")
