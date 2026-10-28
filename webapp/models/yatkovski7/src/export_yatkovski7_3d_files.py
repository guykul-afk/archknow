# -*- coding: utf-8 -*-
import os, sys, json, struct

sys.stdout.reconfigure(encoding='utf-8')

SCRATCH_DIR = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch"
PROJECT_DIR = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\יטקובסקי 7 פתח תקווה"

with open(os.path.join(SCRATCH_DIR, "yatkovski7_extracted_plans.json"), "r", encoding="utf-8") as f:
    plans_data = json.load(f)

FLOORS = [
    {"id": "mar", "sheet": "basement",  "zFloor": -4.38, "zCeil": -0.25},
    {"id": "kar", "sheet": "ground",    "zFloor":  0.00, "zCeil":  3.60},
    {"id": "f1",  "sheet": "typical",   "zFloor":  3.85, "zCeil":  6.75},
    {"id": "f2",  "sheet": "typical",   "zFloor":  7.00, "zCeil":  9.90},
    {"id": "f3",  "sheet": "typical",   "zFloor": 10.15, "zCeil": 13.05},
    {"id": "f4",  "sheet": "typical",   "zFloor": 13.30, "zCeil": 16.28},
    {"id": "f5",  "sheet": "floor_5",   "zFloor": 16.53, "zCeil": 19.51},
    {"id": "f6",  "sheet": "penthouse", "zFloor": 19.76, "zCeil": 22.74},
    {"id": "gag", "sheet": "roof_main", "zFloor": 22.99, "zCeil": 25.99},
]

MATERIALS = {
    "ext_white":     (0.98, 0.99, 1.00, 1.0),
    "int_wall":      (0.91, 0.87, 0.82, 1.0),
    "dark_spandrel": (0.12, 0.16, 0.23, 1.0),
    "slab_floor":    (0.85, 0.86, 0.89, 1.0),
    "wood_deck":     (0.68, 0.45, 0.29, 1.0),
    "glass_blue":    (0.73, 0.90, 0.99, 0.45),
    "alu_dark":      (0.15, 0.18, 0.22, 1.0),
    "oak_furn":      (0.78, 0.62, 0.42, 1.0),
    "boucle_sofa":   (0.97, 0.95, 0.92, 1.0),
    "calacatta":     (0.98, 0.97, 0.95, 1.0),
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

def add_extruded_poly(mat_name, poly_data, z0, z1):
    for t in poly_data["tris"]:
        v0 = (t[0][0], z1, t[0][1])
        v1 = (t[1][0], z1, t[1][1])
        v2 = (t[2][0], z1, t[2][1])
        meshes_by_mat[mat_name].append((v0, v2, v1))
        b0 = (t[0][0], z0, t[0][1])
        b1 = (t[1][0], z0, t[1][1])
        b2 = (t[2][0], z0, t[2][1])
        meshes_by_mat[mat_name].append((b0, b1, b2))
    rings = [poly_data["exterior"]] + poly_data.get("holes", [])
    for ring in rings:
        n = len(ring)
        for i in range(n):
            p1 = ring[i]
            p2 = ring[(i + 1) % n]
            a0 = (p1[0], z0, p1[1])
            a1 = (p2[0], z0, p2[1])
            a2 = (p2[0], z1, p2[1])
            a3 = (p1[0], z1, p1[1])
            meshes_by_mat[mat_name].append((a0, a1, a2))
            meshes_by_mat[mat_name].append((a0, a2, a3))

for f in FLOORS:
    zf, zc = f["zFloor"], f["zCeil"]
    pdata = plans_data[f["sheet"]]
    if f["id"] == "mar":
        add_box("slab_floor", -11.15, -11.20, 6.60, 19.30, -4.65, -4.38)
    elif f["id"] == "kar":
        add_box("slab_floor", -11.15, -11.20, 6.60, 19.30, -0.06, -0.01)
        add_box("alu_dark", -16.00, -17.50, 14.00, -11.20, -0.20, -0.08)
        add_box("slab_floor", -8.14, -5.20, 6.60, 3.80, -0.25, 0.00)
        add_box("slab_floor", -8.14, 3.80, 4.00, 14.36, -0.25, 0.00)
    elif f["id"] in ["f1", "f2", "f3", "f4"]:
        add_box("slab_floor", -8.14, -5.21, 6.95, 3.80, zf - 0.25, zf)
        add_box("slab_floor", -8.14, 3.80, 4.00, 14.36, zf - 0.25, zf)
        # North & South Sun Balconies
        add_box("wood_deck", -3.80, -7.32, 1.20, -5.21, zf - 0.03, zf + 0.01)
        add_box("glass_blue", -3.80, -7.32, 1.20, -7.26, zf + 0.14, zf + 1.05)
        add_box("wood_deck", -7.56, 14.36, 0.50, 15.77, zf - 0.03, zf + 0.01)
        add_box("glass_blue", -7.56, 15.71, 0.50, 15.77, zf + 0.14, zf + 1.05)
    elif f["id"] == "f5":
        add_box("slab_floor", -8.14, -2.65, 6.95, 3.80, zf - 0.25, zf)
        add_box("slab_floor", -8.14, 3.80, 4.00, 12.16, zf - 0.25, zf)
        add_box("wood_deck", -8.14, -5.21, 6.95, -2.65, zf - 0.03, zf + 0.01)
        add_box("wood_deck", -8.14, 12.16, 4.00, 15.77, zf - 0.03, zf + 0.01)
        add_box("glass_blue", -8.14, -5.21, 6.95, -5.15, zf + 0.14, zf + 1.05)
        add_box("glass_blue", -8.14, 15.71, 4.00, 15.77, zf + 0.14, zf + 1.05)
        add_box("ext_white", -6.50, -5.00, 3.50, -2.65, zf + 2.65, zf + 2.85)
        add_box("ext_white", -7.50, 12.16, 2.50, 15.20, zf + 2.65, zf + 2.85)
    elif f["id"] == "f6":
        add_box("slab_floor", -8.14, -2.65, 6.95, 3.80, zf - 0.25, zf)
        add_box("slab_floor", -8.14, 3.80, 4.00, 9.20, zf - 0.25, zf)
        add_box("slab_floor", -8.14, 9.20, -3.20, 12.01, zf - 0.25, zf)
        add_box("wood_deck", -8.14, -4.25, 2.50, -2.65, zf - 0.03, zf + 0.01)
        add_box("wood_deck", -3.20, 9.20, 4.00, 14.50, zf - 0.03, zf + 0.01)
        add_box("wood_deck", -8.14, 12.01, -3.20, 14.50, zf - 0.03, zf + 0.01)
        add_box("glass_blue", -8.14, 14.44, 4.00, 14.50, zf + 0.14, zf + 1.05)
        add_box("ext_white", -3.00, 9.40, 3.60, 14.20, zf + 2.65, zf + 2.85)
    elif f["id"] == "gag":
        add_box("slab_floor", -8.14, -2.65, 6.95, 3.80, 22.74, 22.99)
        add_box("slab_floor", -8.14, 3.80, 4.00, 9.20, 22.74, 22.99)
        add_box("ext_white", -2.20, -1.20, 2.40, 5.40, 25.74, 25.99)

    for wp in pdata["wall_polys"]:
        add_extruded_poly("ext_white" if f["id"] != "mar" else "slab_floor", wp, zf, zc)

    for op in pdata.get("openings", []):
        orient, x0, y0, x1, y1, kind = op
        if kind in ["vitrine", "win_tall", "window", "mamad_win"]:
            zsill = zf + (0.0 if kind == "vitrine" else (0.40 if kind == "win_tall" else 1.05))
            zhead = min(zf + (2.50 if kind == "vitrine" else (2.10 if kind == "mamad_win" else 2.20)), zc - 0.15)
            if zsill > zf + 0.02:
                add_box("ext_white", x0, y0, x1, y1, zf, zsill)
            if zc > zhead + 0.02:
                add_box("ext_white", x0, y0, x1, y1, zhead, zc)
            add_box("alu_dark", x0, y0, x1, y1, zsill, zsill + 0.05)
            add_box("alu_dark", x0, y0, x1, y1, zhead - 0.05, zhead)
            add_box("glass_blue", x0, y0, x1, y1, zsill + 0.05, zhead - 0.05)
        elif kind == "door":
            zhead = min(zf + 2.10, zc - 0.15)
            if zc > zhead + 0.02:
                add_box("int_wall", x0, y0, x1, y1, zhead, zc)
            add_box("oak_furn", x0, y0, x1, y1, zf, zhead)

# Write MTL & OBJ
mtl_lines = ["# Yatkovski 7 Petah Tikva - MTL Library"]
for mname, rgba in MATERIALS.items():
    mtl_lines.append(f"newmtl {mname}")
    mtl_lines.append(f"Kd {rgba[0]:.3f} {rgba[1]:.3f} {rgba[2]:.3f}")
    mtl_lines.append(f"d {rgba[3]:.2f}")
    mtl_lines.append("")

obj_lines = [
    "# Yatkovski 7 Petah Tikva - 1:1 Metric Architectural BIM Model",
    "mtllib yatkovski7_model.mtl"
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
    "asset": {"version": "2.0", "generator": "Kolsky BIM Compiler - Yatkovski 7"},
    "scene": 0,
    "scenes": [{"nodes": [0]}],
    "nodes": [{"name": "Yatkovski7_BIM", "mesh": 0}],
    "meshes": [{"name": "Yatkovski7_Mesh", "primitives": gltf_primitives}],
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

for out_dir in [SCRATCH_DIR, PROJECT_DIR]:
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "yatkovski7_model.mtl"), "w", encoding="utf-8") as f:
        f.write("\n".join(mtl_lines))
    with open(os.path.join(out_dir, "yatkovski7_model.obj"), "w", encoding="utf-8") as f:
        f.write("\n".join(obj_lines))
    with open(os.path.join(out_dir, "yatkovski7_model.glb"), "wb") as f:
        f.write(glb_bytes)

print(f"Exported 3D BIM files (.obj: {len(obj_lines)} lines, .glb: {len(glb_bytes):,} bytes) to {PROJECT_DIR}")
