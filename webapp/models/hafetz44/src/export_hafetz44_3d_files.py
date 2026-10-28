# -*- coding: utf-8 -*-
import os, json, struct, shutil

ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\ee869ca7-2259-4d89-9693-4d5c0376b65b"
SCRATCH_DIR = os.path.join(ARTIFACT_DIR, "scratch", "hafetz44")
PUBLIC_DIR = os.path.join(os.getcwd(), "public", "projects", "hafetz-44")
DRIVE_MODEL_DIR = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\חפץ חיים 44 פתח תקווה"
DATA_DIR = os.path.join(DRIVE_MODEL_DIR, "data")

with open(os.path.join(DATA_DIR, "hafetz44_extracted_plans.json"), "r", encoding="utf-8") as f:
    plans_data = json.load(f)

FLOORS = [
    {"id": "mar", "sheet": "basement",  "zFloor": -5.10, "zCeil": -0.35},
    {"id": "kar", "sheet": "ground",    "zFloor":  0.00, "zCeil":  3.22},
    {"id": "f1",  "sheet": "typical",   "zFloor":  3.50, "zCeil":  6.37},
    {"id": "f2",  "sheet": "typical",   "zFloor":  6.65, "zCeil":  9.52},
    {"id": "f3",  "sheet": "typical",   "zFloor":  9.80, "zCeil": 12.67},
    {"id": "f4",  "sheet": "typical",   "zFloor": 12.95, "zCeil": 15.82},
    {"id": "f5",  "sheet": "typical",   "zFloor": 16.10, "zCeil": 18.97},
    {"id": "f6",  "sheet": "typical",   "zFloor": 19.25, "zCeil": 22.12},
    {"id": "f7",  "sheet": "typical",   "zFloor": 22.40, "zCeil": 25.27},
    {"id": "f8",  "sheet": "typical",   "zFloor": 25.55, "zCeil": 28.42},
    {"id": "f9",  "sheet": "penthouse", "zFloor": 28.70, "zCeil": 31.57},
    {"id": "gag", "sheet": "roof_main", "zFloor": 31.85, "zCeil": 34.55},
]

MATERIALS = {
    "ext_white":     (1.00, 1.00, 1.00, 1.0),
    "int_wall":      (0.91, 0.87, 0.82, 1.0),
    "dark_spandrel": (0.55, 0.34, 0.27, 1.0),
    "slab_floor":    (0.85, 0.86, 0.89, 1.0),
    "wood_deck":     (0.68, 0.45, 0.29, 1.0),
    "glass_blue":    (0.77, 0.89, 0.96, 0.45),
    "alu_dark":      (0.26, 0.20, 0.18, 1.0),
    "oak_furn":      (0.78, 0.62, 0.42, 1.0),
    "boucle_sofa":   (0.97, 0.95, 0.92, 1.0),
    "calacatta":     (0.98, 0.97, 0.95, 1.0),
}

meshes_by_mat = {k: [] for k in MATERIALS}  # list of triangles [(v0, v1, v2), ...] in Three.js Y-up coords (x, z_elev, y)

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
        (p010, p011, p111), (p010, p111, p110), # Top
        (p000, p100, p101), (p000, p101, p001), # Bottom
        (p001, p101, p111), (p001, p111, p011), # South (+Y)
        (p100, p000, p010), (p100, p010, p110), # North (-Y)
        (p101, p100, p110), (p101, p110, p111), # East (+X)
        (p000, p001, p011), (p000, p011, p010), # West (-X)
    ]
    meshes_by_mat[mat_name].extend(tris)

def add_sloped_ramp(mat_name, x0, y0, x1, y1, z_at_min, z_at_max, slope_axis, thick):
    z00 = z_at_min
    z10 = z_at_max if slope_axis == "X" else z_at_min
    z11 = z_at_max
    z01 = z_at_min if slope_axis == "X" else z_at_max
    b00, b10, b11, b01 = z00 - thick, z10 - thick, z11 - thick, z01 - thick
    p010 = (x0, z00, y0)
    p110 = (x1, z10, y0)
    p111 = (x1, z11, y1)
    p011 = (x0, z01, y1)
    p000 = (x0, b00, y0)
    p100 = (x1, b10, y0)
    p101 = (x1, b11, y1)
    p001 = (x0, b01, y1)
    tris = [
        (p010, p011, p111), (p010, p111, p110), # Top
        (p000, p100, p101), (p000, p101, p001), # Bottom
        (p001, p101, p111), (p001, p111, p011), # South (+Y)
        (p100, p000, p010), (p100, p010, p110), # North (-Y)
        (p101, p100, p110), (p101, p110, p111), # East (+X)
        (p000, p001, p011), (p000, p011, p010), # West (-X)
    ]
    meshes_by_mat[mat_name].extend(tris)

def add_staircase_flights(zf, zc):
    zmid = 0.5 * (zf + zc)
    add_box("slab_floor", -1.18, 1.94, 2.10, 2.96, zmid - 0.16, zmid)
    n_steps = 9
    sy0, sy1 = 2.96, 4.86
    dy = (sy1 - sy0) / n_steps
    dz1 = (zmid - zf) / n_steps
    dz2 = (zc - zmid) / n_steps
    for i in range(n_steps):
        add_box("slab_floor", 0.52, sy1 - (i + 1) * dy, 2.08, sy1 - i * dy, zf + i * dz1 - 0.08, zf + (i + 1) * dz1)
        add_box("slab_floor", -1.16, sy0 + i * dy, 0.40, sy0 + (i + 1) * dy, zmid + i * dz2 - 0.08, zmid + (i + 1) * dz2)

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
    if f["id"] != "gag":
        add_staircase_flights(zf, zc)

    # Slabs & Balconies
    if f["id"] == "mar":
        add_box("slab_floor", -17.721, -9.202, 14.249, 9.048, -5.50, -5.10)
        add_box("slab_floor", 14.249, -9.202, 18.508, 3.600, -5.50, -5.10)
        # 3D Multi-Segment Sloped Vehicle Ramp in Basement
        add_sloped_ramp("alu_dark", -1.47, 5.50, 7.45, 8.44, -2.27, -3.72, "X", 0.28)
        add_box("alu_dark", 7.45, 3.10, 13.01, 8.44, -4.00, -3.72)
        add_sloped_ramp("alu_dark", 7.45, -5.66, 13.01, 3.10, -4.12, -3.72, "Y", 0.28)
        add_box("alu_dark", 7.45, -8.60, 13.01, -5.66, -4.40, -4.12)
        add_sloped_ramp("alu_dark", -6.25, -8.60, 7.45, -5.66, -5.10, -4.12, "X", 0.28)
    elif f["id"] == "kar":
        # Net Lot 85-2 (38.82x18.40m) + Expropriation Strip 85-1 (5.38m) + Hafetz Haim Street (6.00m road + 2.00m East sidewalk)
        add_box("slab_floor", -19.411, -9.202, 19.409, 9.196, -0.06, -0.01)
        add_box("slab_floor", 19.409, -15.00, 24.789, 15.00, -0.18, -0.02)
        add_box("alu_dark", 24.789, -15.00, 30.789, 15.00, -0.24, -0.12)
        add_box("slab_floor", 30.789, -15.00, 32.789, 15.00, -0.18, -0.02)
        # Ground 3D Sloped Ramp Segments & Trench Walls
        add_sloped_ramp("alu_dark", -6.35, -9.00, 19.41, -5.45, -0.32, 0.01, "X", 0.18)
        add_sloped_ramp("alu_dark", -11.90, -9.00, -6.35, 5.50, -0.32, -0.50, "Y", 0.18)
        add_sloped_ramp("alu_dark", -6.35, 5.50, -3.35, 8.44, -0.50, -0.80, "X", 0.25)
        add_sloped_ramp("alu_dark", -3.35, 5.50, 6.45, 8.44, -0.80, -2.27, "X", 0.25)
        add_box("ext_white", -6.35, 5.20, 7.71, 5.50, -2.50, 1.15)
        add_box("ext_white", -6.35, 8.44, 7.71, 8.74, -2.50, 1.15)
        # Enclosed Ground Floor Building Slab & Sunken Trash Room (-0.68m = +47.22) & Gas Room (-0.32m)
        add_box("slab_floor", 2.250, -5.184, 14.359, 4.216, -0.28, 0.00)
        add_box("slab_floor", -3.100, -0.130, 2.250, 4.216, -0.28, 0.00)
        add_box("slab_floor", -3.361, 1.415, 5.669, 5.196, -0.28, 0.00)
        add_box("slab_floor", -1.250, -4.630, 2.250, -0.130, -0.88, -0.68)
        add_box("slab_floor", -5.260, 1.420, -3.361, 4.220, -0.55, -0.32)
    elif f["id"] in ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8"]:
        add_box("slab_floor", -13.361, -5.184, 14.359, 4.216, zf - 0.28, zf)
        add_box("slab_floor", -3.361, 4.216, 5.669, 5.196, zf - 0.28, zf)
        # West & East Sun Balconies + Outer Concrete Corner Frame Columns
        add_box("ext_white", -15.42, -5.24, -13.361, 4.27, zf - 0.42, zf - 0.03)
        add_box("wood_deck", -15.361, -5.184, -13.361, 4.216, zf - 0.03, zf + 0.01)
        add_box("glass_blue", -15.361, -5.184, -15.30, 4.216, zf + 0.14, zf + 1.05)
        add_box("ext_white", -15.361, -5.184, -15.11, -4.63, zf, zc)
        add_box("ext_white", -15.361,  3.66,  -15.11,  4.216, zf, zc)
        add_box("ext_white", 14.359, -5.24, 16.42, 4.27, zf - 0.42, zf - 0.03)
        add_box("wood_deck", 14.359, -5.184, 16.359, 4.216, zf - 0.03, zf + 0.01)
        add_box("glass_blue", 16.30, -5.184, 16.359, 4.216, zf + 0.14, zf + 1.05)
        add_box("ext_white", 16.11, -5.184, 16.359, -4.63, zf, zc)
        add_box("ext_white", 16.11,  3.66,  16.359,  4.216, zf, zc)
        # North Copper-Brown Louver Shafts
        for z in [zf - 0.20, zf + 0.15, zf + 0.50, zf + 0.85, zf + 1.20, zf + 1.55, zf + 1.90, zf + 2.25, zf + 2.60]:
            add_box("dark_spandrel", -3.548, -5.21, -1.250, -5.14, z, z + 0.07)
            add_box("dark_spandrel", 5.664, -5.21, 7.840, -5.14, z, z + 0.07)
    elif f["id"] == "f9":
        add_box("slab_floor", -10.211, -5.184, 9.599, 4.216, zf - 0.36, zf)
        add_box("slab_floor", -3.361, 4.216, 5.669, 5.196, zf - 0.36, zf)
        # West (295x940cm: -13.361..-10.211) & East (456x940cm: 9.599..14.359) Roof Terraces per Garmushka
        add_box("wood_deck", -13.361, -5.184, -10.211, 4.216, zf - 0.03, zf + 0.01)
        add_box("wood_deck", 9.599, -5.184, 14.359, 4.216, zf - 0.03, zf + 0.01)
        add_box("glass_blue", -13.361, -5.184, -13.30, 4.216, zf + 0.20, zf + 1.15)
        add_box("glass_blue", 14.30, -5.184, 14.359, 4.216, zf + 0.20, zf + 1.15)
        # Pergolas + Corner Columns
        add_box("ext_white", -13.361, -5.184, -10.211, 4.216, zf + 2.75, zf + 3.15)
        add_box("ext_white", 9.599, -5.184, 14.359, 4.216, zf + 2.75, zf + 3.15)
        add_box("ext_white", -13.361, -5.184, -13.11, -4.63, zf, zf + 3.15)
        add_box("ext_white", -13.361,  3.66,  -13.11,  4.216, zf, zf + 3.15)
        add_box("ext_white", 14.11, -5.184, 14.359, -4.63, zf, zf + 3.15)
        add_box("ext_white", 14.11,  3.66,  14.359,  4.216, zf, zf + 3.15)
        # Jacuzzi & BBQ
        add_box("oak_furn", -13.05, -4.50, -11.05, -2.50, zf + 0.02, zf + 0.80)
        add_box("calacatta", 10.20, -4.65, 13.80, -3.95, zf + 0.02, zf + 0.92)
    elif f["id"] == "gag":
        add_box("slab_floor", -10.211, -5.184, 9.599, 4.216, 31.57, 31.85)
        add_box("slab_floor", -3.361, 4.216, 5.669, 5.196, 31.57, 31.85)
        add_box("ext_white", -1.48, 1.64, 2.42, 5.24, 34.30, 34.55)

    for wp in pdata["wall_polys"]:
        z0_w = -0.68 if f["id"] == "kar" else zf
        add_extruded_poly("ext_white" if f["id"] != "mar" else "slab_floor", wp, z0_w, zc)

    for op in pdata.get("openings", []):
        orient, x0, y0, x1, y1, kind = op
        midx, midy = 0.5 * (x0 + x1), 0.5 * (y0 + y1)
        span = (x1 - x0) if orient == "H" else (y1 - y0)
        is_core_n = (orient == "H" and midy < 0.0 and -2.85 <= midx <= 3.85)
        is_laundry = (orient == "H" and abs(midy - (-4.334)) <= 0.22)
        is_small_n = (orient == "H" and midy < 0.0 and span < 0.85)
        below_mat = "dark_spandrel" if (kind == "win_tall" and not is_core_n and not is_laundry) else "ext_white"
        above_mat = "dark_spandrel" if ((orient == "V" or (orient == "H" and not is_core_n and not is_laundry and not is_small_n)) and kind != "mamad_win") else "ext_white"
        if kind in ["vitrine", "win_tall", "window", "mamad_win"]:
            zsill = zf + (0.0 if kind == "vitrine" else (0.40 if kind == "win_tall" else 1.05))
            zhead = min(zf + (2.80 if (kind == "vitrine" and f["id"] == "kar") else (2.05 if kind == "mamad_win" else 2.28)), zc - 0.15)
            if zsill > zf + 0.02:
                add_box(below_mat, x0, y0, x1, y1, zf, zsill)
            if zc > zhead + 0.02:
                add_box(above_mat, x0, y0, x1, y1, zhead, zc)
            add_box("alu_dark", x0, y0, x1, y1, zsill, zsill + 0.05)
            add_box("alu_dark", x0, y0, x1, y1, zhead - 0.05, zhead)
            add_box("glass_blue", x0, y0, x1, y1, zsill + 0.05, zhead - 0.05)
        elif kind == "door":
            zhead = min(zf + 2.10, zc - 0.15)
            if zc > zhead + 0.02:
                add_box("int_wall", x0, y0, x1, y1, zhead, zc)
            add_box("oak_furn", x0, y0, x1, y1, zf, zhead)

    # 1:1 CAD-Aligned Interior Furniture on Furnished Floors (kar, f4, f5, f9)
    if f["id"] == "kar":
        add_box("calacatta", 6.80, 2.50, 9.20, 3.15, zf + 0.02, zf + 1.05)
        add_box("oak_furn", 6.80, 0.20, 9.40, 1.05, zf + 0.02, zf + 0.82)
        add_box("oak_furn", 6.45, -3.55, 7.85, -2.15, zf + 0.02, zf + 0.76)
    elif f["id"] in ["f4", "f5"]:
        add_box("oak_furn", -12.60, 3.04, -10.21, 3.90, zf + 0.02, zf + 0.84)
        add_box("oak_furn", -10.55, 1.85, -9.68, 2.75, zf + 0.02, zf + 0.80)
        add_box("oak_furn", -8.42, 2.42, -7.62, 3.88, zf + 0.02, zf + 0.76)
        add_box("calacatta", -4.02, 1.18, -3.38, 3.92, zf + 0.02, zf + 2.15)
        add_box("calacatta", -6.36, 3.30, -3.38, 3.96, zf + 0.02, zf + 0.90)
        add_box("calacatta", -6.36, 2.16, -5.66, 3.96, zf + 0.02, zf + 0.92)
        add_box("oak_furn", 11.13, 2.99, 13.78, 3.88, zf + 0.02, zf + 0.84)
        add_box("oak_furn", 10.45, 1.88, 11.35, 2.78, zf + 0.02, zf + 0.80)
        add_box("oak_furn", 8.98, 2.42, 9.78, 3.88, zf + 0.02, zf + 0.76)
        add_box("calacatta", 5.66, 1.18, 6.30, 3.92, zf + 0.02, zf + 2.15)
        add_box("calacatta", 5.66, 3.30, 8.40, 3.96, zf + 0.02, zf + 0.90)
        add_box("calacatta", 7.72, 2.16, 8.42, 3.96, zf + 0.02, zf + 0.92)
        add_box("oak_furn", -13.10, -2.65, -11.05, -0.95, zf + 0.02, zf + 0.62)
        add_box("oak_furn", 12.05, -2.65, 14.10, -0.95, zf + 0.02, zf + 0.62)
        add_box("oak_furn", -9.52, -4.94, -8.52, -2.94, zf + 0.02, zf + 0.56)
        add_box("oak_furn", -6.45, -4.94, -5.45, -2.94, zf + 0.02, zf + 0.56)
        add_box("oak_furn", 9.82, -4.94, 10.82, -2.94, zf + 0.02, zf + 0.56)
        add_box("oak_furn", 1.22, -4.23, 2.22, -2.45, zf + 0.02, zf + 0.56)
        add_box("oak_furn", 2.52, -4.22, 3.52, -2.44, zf + 0.02, zf + 0.56)
    elif f["id"] == "f9":
        add_box("oak_furn", 5.64, -1.92, 8.04, -1.05, zf + 0.02, zf + 0.84)
        add_box("oak_furn", 4.77, -2.85, 5.64, -1.95, zf + 0.02, zf + 0.80)
        add_box("oak_furn", 7.20, -0.35, 8.85, 0.55, zf + 0.02, zf + 0.76)
        add_box("calacatta", 4.25, 3.38, 9.30, 3.98, zf + 0.02, zf + 0.90)
        add_box("calacatta", 6.06, 1.52, 8.49, 2.42, zf + 0.02, zf + 0.92)
        add_box("oak_furn", -7.02, 1.55, -5.02, 2.75, zf + 0.02, zf + 0.62)
        add_box("oak_furn", -9.52, -4.94, -8.52, -2.94, zf + 0.02, zf + 0.56)
        add_box("oak_furn", -6.45, -4.94, -5.45, -2.94, zf + 0.02, zf + 0.56)
        add_box("oak_furn", 1.22, -4.23, 2.22, -2.45, zf + 0.02, zf + 0.56)

# Write MTL & OBJ
mtl_lines = ["# Hafetz Haim 44 Petah Tikva - MTL Library"]
for mname, rgba in MATERIALS.items():
    mtl_lines.append(f"newmtl {mname}")
    mtl_lines.append(f"Kd {rgba[0]:.3f} {rgba[1]:.3f} {rgba[2]:.3f}")
    mtl_lines.append(f"d {rgba[3]:.2f}")
    mtl_lines.append("")

obj_lines = [
    "# Hafetz Haim 44 Petah Tikva - 1:1 Metric Architectural BIM Model",
    "mtllib hafetz44_model.mtl"
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
    "asset": {"version": "2.0", "generator": "HafetzHaim44-CAD-BIM-Exporter"},
    "scene": 0,
    "scenes": [{"nodes": [0]}],
    "nodes": [{"name": "HafetzHaim44_BIM", "mesh": 0}],
    "meshes": [{"name": "HafetzHaim44_Mesh", "primitives": gltf_primitives}],
    "materials": gltf_materials,
    "buffers": [{"byteLength": len(bin_chunks)}],
    "bufferViews": buffer_views,
    "accessors": accessors
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

DIST_DIR = os.path.join(os.getcwd(), "dist", "projects", "hafetz-44")
for out_dir in [ARTIFACT_DIR, PUBLIC_DIR, DIST_DIR, DRIVE_MODEL_DIR]:
    os.makedirs(out_dir, exist_ok=True)
    mtl_p = os.path.join(out_dir, "hafetz44_model.mtl")
    obj_p = os.path.join(out_dir, "hafetz44_model.obj")
    glb_p = os.path.join(out_dir, "hafetz44_model.glb")
    with open(mtl_p, "w", encoding="utf-8") as f:
        f.write("\n".join(mtl_lines))
    with open(obj_p, "w", encoding="utf-8") as f:
        f.write("\n".join(obj_lines))
    with open(glb_p, "wb") as f:
        f.write(glb_bytes)
    print("Exported to:", out_dir, "OBJ:", os.path.getsize(obj_p), "GLB:", os.path.getsize(glb_p))
