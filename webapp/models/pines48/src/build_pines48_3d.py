import os
import math
import json
import struct

OUT_DIR = r"C:\Users\User\.gemini\antigravity\scratch\pines-48-3d"
SCRATCH_DIR = r"C:\Users\User\.gemini\antigravity\brain\60b6f7e6-94a5-48b9-b12c-1728c4428342\scratch"
os.makedirs(OUT_DIR, exist_ok=True)

with open(os.path.join(SCRATCH_DIR, "extracted_interior_plans.json"), "r", encoding="utf-8") as f:
    INTERIOR_PLANS = json.load(f)

# ==============================================================================
# 1. EXACT CAD COORDINATE SYSTEM & GEOMETRIC PRIMITIVES (1:50 AUTO-EXTRACTED)
# ==============================================================================
CX, CY = 17.50, 13.00

def cad_to_3d(x, y, z):
    return (round(x - CX, 4), round(z, 4), round(-(y - CY), 4))

def cubic_bezier(p0, p1, p2, p3, n=16):
    pts = []
    for i in range(n + 1):
        t = i / n
        mt = 1.0 - t
        x = (mt**3)*p0[0] + 3*(mt**2)*t*p1[0] + 3*mt*(t**2)*p2[0] + (t**3)*p3[0]
        y = (mt**3)*p0[1] + 3*(mt**2)*t*p1[1] + 3*mt*(t**2)*p2[1] + (t**3)*p3[1]
        pts.append((x, y))
    return pts

NW_CORNER = (4.045, 17.266)
EU = (0.978462, 0.206425)          # Along North wall (East-Northeast)
ES = (0.206425, -0.978462)         # Along West wall (South-Southeast)
EN_NORTH = (-0.206425, 0.978462)   # Outward normal of North wall
EN_WEST  = (-0.978462, -0.206425)  # Outward normal of West wall

def pt_uv(u, s):
    return (
        NW_CORNER[0] + u * EU[0] + s * ES[0],
        NW_CORNER[1] + u * EU[1] + s * ES[1],
    )

NE_ARC_OUTER = cubic_bezier((26.990, 22.106), (27.937, 22.195), (28.820, 21.619), (29.122, 20.717), n=16)
NE_ARC_INNER = cubic_bezier((26.948, 21.902), (27.806, 21.983), (28.606, 21.461), (28.880, 20.644), n=16)
LOT_NE_CURVE = cubic_bezier((34.100, 22.107), (34.100, 25.800), (28.500, 27.798), (24.205, 26.892), n=20)
SETBACK_NE_CURVE = cubic_bezier((26.625, 22.342), (29.210, 22.887), (31.594, 20.654), (31.100, 18.021), n=16)

POLY_LOT = [(0.000, 0.000), (34.049, 0.000)] + LOT_NE_CURVE + [(0.184, 21.800), (0.066, 7.847)]
POLY_SETBACK = [(4.000, 4.000), (31.100, 4.000)] + list(reversed(SETBACK_NE_CURVE)) + [(4.000, 17.569)]

POLY_OUTER = (
    [(4.045, 17.266)] +
    NE_ARC_OUTER +
    [
        (30.726, 13.134),
        (30.726, 12.150),
        (30.351, 12.150),
        (30.351, 4.199),
        (22.849, 4.199),
        (22.849, 4.100),
        (17.251, 4.100),
        (17.251, 4.951),
        (12.399, 4.951),
        (12.399, 6.517),
        (6.572, 5.287),
    ]
)

POLY_F1_5_SLAB = (
    [
        (4.045, 17.266),
        (4.436, 17.349),
        (4.560, 16.761),
        (21.096, 20.250),
        (20.972, 20.837),
    ] +
    NE_ARC_OUTER +
    [
        (30.726, 13.134),
        (30.726, 12.150),
        (30.351, 12.150),
        (30.351, 4.199),
        (22.849, 4.199),
        (22.849, 4.100),
        (17.251, 4.100),
        (17.251, 4.951),
        (12.399, 4.951),
        (12.399, 6.517),
        (6.572, 5.287),
    ]
)

POLY_F6_WALLS = [
    (4.045, 17.266),
    (16.863, 19.971),
    (17.617, 16.400),
    (18.440, 16.368),
    (19.039, 13.530),
    (21.984, 14.150),
    (30.351, 14.150),
    (30.351, 7.550),
    (26.151, 7.550),
    (26.151, 4.199),
    (22.849, 4.199),
    (22.849, 4.100),
    (17.251, 4.100),
    (17.251, 4.951),
    (12.399, 4.951),
    (12.399, 6.517),
    (6.572, 5.287),
]

POLY_UPPER_ROOF_OUTER = [
    (7.628, 14.086),
    (18.440, 16.368),
    (19.039, 13.530),
    (21.984, 14.150),
    (23.899, 14.150),
    (23.899, 11.250),
    (26.151, 11.250),
    (26.151, 5.850),
    (18.201, 5.848),
    (18.201, 9.550),
    (17.437, 9.550),
    (17.437, 10.329),
    (15.502, 9.921),
    (15.970, 7.698),
    (10.295, 6.502),
    (9.394, 10.778),
    (8.371, 10.564),
]

POLY_TOWER_OUTER = [
    (12.611, 14.933),
    (16.624, 15.780),
    (17.367, 12.258),
    (13.354, 11.411),
]

BALCONY_NW = [pt_uv(4.10, 0.60), pt_uv(4.10, -1.90), pt_uv(8.55, -1.90), pt_uv(8.55, 0.60)]
BALCONY_NC = [pt_uv(12.75, 0.60), pt_uv(12.75, -1.90), pt_uv(17.20, -1.90), pt_uv(17.20, 0.60)]
BALCONY_NW_F6 = [pt_uv(4.10, 0.00), pt_uv(4.10, -1.90), pt_uv(8.55, -1.90), pt_uv(8.55, 0.00)]
BALCONY_E  = [(30.351, 6.750), (32.550, 6.750), (32.550, 12.150), (30.351, 12.150)]
BALCONY_S_SERVICE = [(13.601, 4.951), (13.601, 4.100), (15.150, 4.100), (15.150, 4.951)]

# ==============================================================================
# 2. ROBUST CONCAVE POLYGON TRIANGULATOR & MESH BUILDER
# ==============================================================================

def clean_polygon_2d(poly):
    pts = []
    for p in poly:
        if not pts or math.hypot(p[0] - pts[-1][0], p[1] - pts[-1][1]) > 1e-3:
            pts.append((float(p[0]), float(p[1])))
    if len(pts) > 1 and math.hypot(pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1]) <= 1e-3:
        pts.pop()
    cleaned = True
    while cleaned and len(pts) > 3:
        cleaned = False
        n = len(pts)
        for i in range(n):
            a = pts[(i - 1) % n]
            b = pts[i]
            c = pts[(i + 1) % n]
            ux, uy = b[0] - a[0], b[1] - a[1]
            vx, vy = c[0] - b[0], c[1] - b[1]
            lu = math.hypot(ux, uy)
            lv = math.hypot(vx, vy)
            if lu < 1e-4 or lv < 1e-4:
                pts.pop(i)
                cleaned = True
                break
            cross = abs(ux * vy - uy * vx) / (lu * lv)
            dot = (ux * vx + uy * vy) / (lu * lv)
            if cross < 1e-4 and dot > 0:
                pts.pop(i)
                cleaned = True
                break
    return pts

def signed_area_2d(poly):
    a = 0.0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        a += (x1 * y2 - x2 * y1)
    return 0.5 * a

def point_in_tri_2d(pt, a, b, c):
    px, py = pt
    ax, ay = a
    bx, by = b
    cx, cy = c
    c1 = (bx - ax) * (py - ay) - (by - ay) * (px - ax)
    c2 = (cx - bx) * (py - by) - (cy - by) * (px - bx)
    c3 = (ax - cx) * (py - cy) - (ay - cy) * (px - cx)
    return (c1 >= -1e-6) and (c2 >= -1e-6) and (c3 >= -1e-6)

def triangulate_polygon_2d(pts_ccw):
    n = len(pts_ccw)
    if n < 3:
        return []
    indices = list(range(n))
    tris = []
    for tol in (1e-6, 1e-9, -1e-4):
        guard = 0
        while len(indices) > 3 and guard < 1000:
            guard += 1
            m = len(indices)
            ear_found = False
            for idx in range(m):
                i_prev = indices[(idx - 1) % m]
                i_curr = indices[idx]
                i_next = indices[(idx + 1) % m]
                a, b, c = pts_ccw[i_prev], pts_ccw[i_curr], pts_ccw[i_next]
                cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
                if cross <= tol:
                    continue
                inside = False
                for other_idx in indices:
                    if other_idx in (i_prev, i_curr, i_next):
                        continue
                    p = pts_ccw[other_idx]
                    if math.hypot(p[0]-a[0], p[1]-a[1]) < 1e-4 or math.hypot(p[0]-b[0], p[1]-b[1]) < 1e-4 or math.hypot(p[0]-c[0], p[1]-c[1]) < 1e-4:
                        continue
                    if point_in_tri_2d(p, a, b, c):
                        inside = True
                        break
                if not inside:
                    tris.append((i_prev, i_curr, i_next))
                    indices.pop(idx)
                    ear_found = True
                    break
            if not ear_found:
                break
        if len(indices) <= 3:
            break
    if len(indices) == 3:
        tris.append((indices[0], indices[1], indices[2]))
    return tris


class SceneBuilder:
    def __init__(self):
        self.materials = {
            "mat_D_white_plaster": {
                "name": "D - טיח בגוון לבן (White Stucco)",
                "code": "D",
                "color": [0.955, 0.948, 0.930],
                "roughness": 0.78,
                "metalness": 0.02,
                "opacity": 1.0,
            },
            "mat_B_gray_plaster": {
                "name": "B - טיח בגוון אפור (Dark Gray Plaster)",
                "code": "B",
                "color": [0.380, 0.395, 0.415],
                "roughness": 0.72,
                "metalness": 0.04,
                "opacity": 1.0,
            },
            "mat_C_white_louvers": {
                "name": "C - רפפות אלומיניום בגוון לבן (White Aluminum Louvers)",
                "code": "C",
                "color": [0.910, 0.925, 0.940],
                "roughness": 0.38,
                "metalness": 0.35,
                "opacity": 1.0,
            },
            "mat_A_iron_railing": {
                "name": "A - מעקה ברזל (Charcoal Iron Railing)",
                "code": "A",
                "color": [0.150, 0.165, 0.185],
                "roughness": 0.35,
                "metalness": 0.80,
                "opacity": 1.0,
            },
            "mat_interior_wall": {
                "name": "קירות פנים (אחיד)",
                "code": "IW",
                "color": [0.968, 0.961, 0.941],
                "roughness": 0.72,
                "metalness": 0.02,
                "opacity": 1.0,
            },
            "mat_core_concrete": {
                "name": "קירות פנים (אחיד)",
                "code": "IW",
                "color": [0.968, 0.961, 0.941],
                "roughness": 0.72,
                "metalness": 0.02,
                "opacity": 1.0,
            },
            "mat_interior_partition": {
                "name": "קירות פנים (אחיד)",
                "code": "IW",
                "color": [0.968, 0.961, 0.941],
                "roughness": 0.72,
                "metalness": 0.02,
                "opacity": 1.0,
            },
            "mat_interior_wood_fixtures": {
                "name": "מדרגות פנים (Interior Staircases)",
                "code": "WD",
                "color": [0.720, 0.560, 0.400],
                "roughness": 0.55,
                "metalness": 0.05,
                "opacity": 1.0,
            },
            "mat_window_glass": {
                "name": "זכוכית בידודית (Architectural Glazing)",
                "code": "GL",
                "color": [0.210, 0.375, 0.525],
                "roughness": 0.10,
                "metalness": 0.65,
                "opacity": 0.75,
            },
            "mat_alu_frame": {
                "name": "פרופילי אלומיניום (Dark Aluminum Mullions)",
                "code": "AL",
                "color": [0.195, 0.210, 0.230],
                "roughness": 0.40,
                "metalness": 0.75,
                "opacity": 1.0,
            },
            "mat_concrete_curb": {
                "name": "קורת בטון ופרגולות (Architectural Concrete & Slabs)",
                "code": "CN",
                "color": [0.855, 0.848, 0.830],
                "roughness": 0.82,
                "metalness": 0.02,
                "opacity": 1.0,
            },
            "mat_terrace_tile": {
                "name": "ריצוף פנים ומרפסות (Floor & Terrace Stone Tile)",
                "code": "TL",
                "color": [0.835, 0.815, 0.785],
                "roughness": 0.68,
                "metalness": 0.05,
                "opacity": 1.0,
            },
            "mat_solar_panel": {
                "name": "קולטי שמש (Rooftop Solar Collectors)",
                "code": "SL",
                "color": [0.110, 0.165, 0.275],
                "roughness": 0.18,
                "metalness": 0.70,
                "opacity": 1.0,
            },
            "mat_site_ground": {
                "name": "פיתוח מגרש ומדרכות (Site Paving & Context)",
                "code": "ST",
                "color": [0.825, 0.810, 0.785],
                "roughness": 0.88,
                "metalness": 0.00,
                "opacity": 1.0,
            },
            "mat_road_asphalt": {
                "name": "כביש אספלט (רח' פינס / רח' בעש\"ט)",
                "code": "RD",
                "color": [0.240, 0.250, 0.265],
                "roughness": 0.92,
                "metalness": 0.00,
                "opacity": 1.0,
            },
            "mat_landscape_green": {
                "name": "גינון וצמחייה (Landscaping & Trees)",
                "code": "GR",
                "color": [0.330, 0.490, 0.310],
                "roughness": 0.85,
                "metalness": 0.00,
                "opacity": 1.0,
            },
            "mat_cad_setback": {
                "name": "קו בניין / קו מגרש (CAD Lot & Setback Lines)",
                "code": "CD",
                "color": [0.860, 0.190, 0.180],
                "roughness": 0.50,
                "metalness": 0.00,
                "opacity": 1.0,
            },
            "mat_cad_furniture_2d": {
                "name": "סימון דו-מימדי: ריהוט וארונות על הרצפה (2D Furniture & Wardrobes Plan)",
                "code": "F2D",
                "color": [0.145, 0.388, 0.922],
                "roughness": 0.50,
                "metalness": 0.00,
                "opacity": 1.0,
            },
            "mat_cad_fixtures_2d": {
                "name": "סימון דו-מימדי: מטבחים, כלים סניטריים ודלתות (2D Kitchens, Sanitary & Doors Plan)",
                "code": "K2D",
                "color": [0.706, 0.325, 0.035],
                "roughness": 0.50,
                "metalness": 0.00,
                "opacity": 1.0,
            },
        }
        self.groups = {}

    def _get_group(self, layer, mat):
        key = (layer, mat)
        if key not in self.groups:
            self.groups[key] = {"layer": layer, "material": mat, "positions": [], "normals": [], "indices": []}
        return self.groups[key]

    def add_quad_3d(self, layer, mat, p0, p1, p2, p3):
        g = self._get_group(layer, mat)
        v0 = cad_to_3d(*p0)
        v1 = cad_to_3d(*p1)
        v2 = cad_to_3d(*p2)
        v3 = cad_to_3d(*p3)
        ux, uy, uz = v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]
        vx, vy, vz = v3[0] - v0[0], v3[1] - v0[1], v3[2] - v0[2]
        nx = uy * vz - uz * vy
        ny = uz * vx - ux * vz
        nz = ux * vy - uy * vx
        ln = math.sqrt(nx*nx + ny*ny + nz*nz)
        if ln < 1e-9:
            return
        nx, ny, nz = round(nx/ln, 4), round(ny/ln, 4), round(nz/ln, 4)
        base = len(g["positions"]) // 3
        for v in (v0, v1, v2, v3):
            g["positions"].extend(v)
            g["normals"].extend((nx, ny, nz))
        g["indices"].extend((base, base + 1, base + 2, base, base + 2, base + 3))

    def add_extruded_polygon(self, layer, mat, poly_2d, z_min, z_max, cap_bottom=True, cap_top=True, top_mat=None):
        pts_clean = clean_polygon_2d(poly_2d)
        if len(pts_clean) < 3 or abs(z_max - z_min) < 1e-6:
            return
        area = signed_area_2d(pts_clean)
        pts = pts_clean if area > 0 else list(reversed(pts_clean))
        n = len(pts)

        for i in range(n):
            x0, y0 = pts[i]
            x1, y1 = pts[(i + 1) % n]
            if math.hypot(x1 - x0, y1 - y0) < 1e-5:
                continue
            self.add_quad_3d(
                layer, mat,
                (x0, y0, z_min),
                (x1, y1, z_min),
                (x1, y1, z_max),
                (x0, y0, z_max),
            )

        if cap_top or cap_bottom:
            tris = triangulate_polygon_2d(pts)
            if cap_top:
                tmat = top_mat if top_mat else mat
                g_top = self._get_group(layer, tmat)
                base = len(g_top["positions"]) // 3
                for (x, y) in pts:
                    g_top["positions"].extend(cad_to_3d(x, y, z_max))
                    g_top["normals"].extend((0.0, 1.0, 0.0))
                for (i0, i1, i2) in tris:
                    g_top["indices"].extend((base + i0, base + i1, base + i2))

            if cap_bottom:
                g_bot = self._get_group(layer, mat)
                base = len(g_bot["positions"]) // 3
                for (x, y) in pts:
                    g_bot["positions"].extend(cad_to_3d(x, y, z_min))
                    g_bot["normals"].extend((0.0, -1.0, 0.0))
                for (i0, i1, i2) in tris:
                    g_bot["indices"].extend((base + i0, base + i2, base + i1))

    def add_box_aligned(self, layer, mat, origin_xy, u_vec, v_vec, u0, u1, v0, v1, z0, z1):
        if (u1 - u0) < 1e-3 or abs(v1 - v0) < 1e-3 or (z1 - z0) < 1e-3:
            return
        ox, oy = origin_xy
        ux, uy = u_vec
        vx, vy = v_vec
        poly = [
            (ox + u0*ux + v0*vx, oy + u0*uy + v0*vy),
            (ox + u1*ux + v0*vx, oy + u1*uy + v0*vy),
            (ox + u1*ux + v1*vx, oy + u1*uy + v1*vy),
            (ox + u0*ux + v1*vx, oy + u0*uy + v1*vy),
        ]
        self.add_extruded_polygon(layer, mat, poly, z0, z1)

    def add_wall_strip(self, layer, mat, path_2d, thickness, z0, z1, closed=False):
        n = len(path_2d)
        limit = n if closed else n - 1
        for i in range(limit):
            x0, y0 = path_2d[i]
            x1, y1 = path_2d[(i + 1) % n]
            dx, dy = x1 - x0, y1 - y0
            L = math.hypot(dx, dy)
            if L < 1e-4:
                continue
            ux, uy = dx / L, dy / L
            nx, ny = -uy, ux
            self.add_box_aligned(layer, mat, (x0, y0), (ux, uy), (nx, ny), -0.02, L + 0.02, -thickness, 0.0, z0, z1)

    def add_stair_flight_3d(self, layer, mat, origin_xy, u_vec, v_vec, width, length, z_bot, z_top, num_steps=9):
        dz = (z_top - z_bot) / num_steps
        du = length / num_steps
        for k in range(num_steps):
            u0 = k * du
            u1 = (k + 1) * du
            zk0 = z_bot + k * dz
            zk1 = z_bot + (k + 1) * dz
            self.add_box_aligned(layer, mat, origin_xy, u_vec, v_vec, u0, u1, 0.0, width, max(z_bot, zk1 - 0.16), zk1)

    def add_iron_railing_path(self, layer, path_2d, z_base, height=1.05, curb_h=0.22, closed=False):
        n = len(path_2d)
        limit = n if closed else n - 1
        for i in range(limit):
            x0, y0 = path_2d[i]
            x1, y1 = path_2d[(i + 1) % n]
            dx, dy = x1 - x0, y1 - y0
            L = math.hypot(dx, dy)
            if L < 0.08:
                continue
            ux, uy = dx / L, dy / L
            nx, ny = -uy, ux

            if curb_h > 0.01:
                self.add_box_aligned(
                    layer, "mat_concrete_curb", (x0, y0), (ux, uy), (nx, ny),
                    0.0, L, -0.09, 0.09, z_base, z_base + curb_h
                )
            z_rail0 = z_base + curb_h
            z_rail1 = z_rail0 + height

            self.add_box_aligned(
                layer, "mat_A_iron_railing", (x0, y0), (ux, uy), (nx, ny),
                0.0, L, -0.025, 0.025, z_rail1 - 0.04, z_rail1
            )
            self.add_box_aligned(
                layer, "mat_A_iron_railing", (x0, y0), (ux, uy), (nx, ny),
                0.0, L, -0.02, 0.02, z_rail0 + 0.06, z_rail0 + 0.09
            )

            num_pickets = max(2, int(L / 0.15))
            step = L / num_pickets
            for k in range(num_pickets + 1):
                s = k * step
                is_post = (k == 0 or k == num_pickets or k % 8 == 0)
                pw = 0.036 if is_post else 0.018
                z_bot = z_rail0 if is_post else z_rail0 + 0.06
                self.add_box_aligned(
                    layer, "mat_A_iron_railing", (x0, y0), (ux, uy), (nx, ny),
                    s - pw*0.5, s + pw*0.5, -pw*0.5, pw*0.5, z_bot, z_rail1 - 0.03
                )

    def add_window_assembly(self, layer, origin_xy, u_vec, n_out_vec, u0, u1, z0, z1, has_shutter_box=True, num_panels=2):
        w = u1 - u0
        h = z1 - z0
        if w < 0.25 or h < 0.25:
            return
        frame_t = 0.055
        self.add_box_aligned(layer, "mat_alu_frame", origin_xy, u_vec, n_out_vec, u0, u0 + frame_t, -0.15, -0.02, z0, z1)
        self.add_box_aligned(layer, "mat_alu_frame", origin_xy, u_vec, n_out_vec, u1 - frame_t, u1, -0.15, -0.02, z0, z1)
        self.add_box_aligned(layer, "mat_alu_frame", origin_xy, u_vec, n_out_vec, u0, u1, -0.15, 0.01, z0, z0 + frame_t)
        self.add_box_aligned(layer, "mat_alu_frame", origin_xy, u_vec, n_out_vec, u0, u1, -0.15, -0.02, z1 - frame_t, z1)

        glass_z1 = z1 - frame_t
        if has_shutter_box and h >= 1.10:
            sb_h = 0.20
            self.add_box_aligned(layer, "mat_alu_frame", origin_xy, u_vec, n_out_vec, u0 + frame_t, u1 - frame_t, -0.14, -0.03, z1 - sb_h, z1 - frame_t)
            glass_z1 = z1 - sb_h

        panel_w = (w - 2*frame_t) / num_panels
        for p in range(1, num_panels):
            mu = u0 + frame_t + p * panel_w
            self.add_box_aligned(layer, "mat_alu_frame", origin_xy, u_vec, n_out_vec, mu - 0.022, mu + 0.022, -0.12, -0.04, z0 + frame_t, glass_z1)

        if h >= 2.00:
            zt = z0 + 1.05
            self.add_box_aligned(layer, "mat_alu_frame", origin_xy, u_vec, n_out_vec, u0 + frame_t, u1 - frame_t, -0.12, -0.04, zt - 0.02, zt + 0.02)

        self.add_box_aligned(layer, "mat_window_glass", origin_xy, u_vec, n_out_vec, u0 + frame_t, u1 - frame_t, -0.10, -0.06, z0 + frame_t, glass_z1)

    def add_exterior_wall_with_openings(self, layer, p0, p1, thickness, z_flr, z_ceil, openings=None, wall_mat="mat_D_white_plaster", z_soffit=None):
        if openings is None:
            openings = []
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L = math.hypot(dx, dy)
        if L < 0.05:
            return
        ux, uy = dx / L, dy / L
        n_out = (-uy, ux)
        sorted_ops = sorted(openings, key=lambda op: op["u0"])

        cursor = -0.04
        for op in sorted_ops:
            u0 = max(0.0, op["u0"])
            u1 = min(L, op["u1"])
            z_bot = op["zBot"]
            z_top = op["zTop"]
            if u0 > cursor + 0.01:
                self.add_box_aligned(layer, wall_mat, p0, (ux, uy), n_out, cursor, u0, -thickness, 0.0, z_flr, z_ceil)
            # Sill wall ONLY under windows (NEVER under floor-to-ceiling vitrinas!)
            if z_bot > z_flr + 0.08:
                self.add_box_aligned(layer, wall_mat, p0, (ux, uy), n_out, u0, u1, -thickness, 0.0, z_flr, z_bot)
            # Lintel header wall above opening
            if z_top < z_ceil - 0.02:
                self.add_box_aligned(layer, wall_mat, p0, (ux, uy), n_out, u0, u1, -thickness, 0.0, z_top, z_ceil)
            # Glazing / window assembly
            if not op.get("openOnly", False):
                self.add_window_assembly(
                    layer, p0, (ux, uy), n_out, u0, u1, z_bot, z_top,
                    has_shutter_box=op.get("shutter", True),
                    num_panels=op.get("panels", 2)
                )
            # Material B Gray Plaster spandrel panels above and below window
            if op.get("graySpandrel", False):
                z_sp_bot = z_soffit if z_soffit is not None else z_flr
                if z_bot > z_sp_bot + 0.05:
                    self.add_box_aligned(layer, "mat_B_gray_plaster", p0, (ux, uy), n_out, u0 - 0.03, u1 + 0.03, -0.02, 0.025, z_sp_bot, z_bot)
                if z_top < z_ceil - 0.02:
                    self.add_box_aligned(layer, "mat_B_gray_plaster", p0, (ux, uy), n_out, u0 - 0.03, u1 + 0.03, -0.02, 0.025, z_top, z_ceil)
            cursor = u1

        if cursor < L + 0.04:
            self.add_box_aligned(layer, wall_mat, p0, (ux, uy), n_out, cursor, L + 0.04, -thickness, 0.0, z_flr, z_ceil)

    def add_louver_screen(self, layer, origin_xy, u_vec, n_out_vec, u0, u1, z0, z1, slat_step=0.14):
        w = u1 - u0
        self.add_box_aligned(layer, "mat_alu_frame", origin_xy, u_vec, n_out_vec, u0, u1, 0.01, 0.045, z0, z1)
        self.add_box_aligned(layer, "mat_C_white_louvers", origin_xy, u_vec, n_out_vec, u0, u0 + 0.06, 0.02, 0.12, z0, z1)
        self.add_box_aligned(layer, "mat_C_white_louvers", origin_xy, u_vec, n_out_vec, u1 - 0.06, u1, 0.02, 0.12, z0, z1)
        if w > 1.30:
            um = 0.5 * (u0 + u1)
            self.add_box_aligned(layer, "mat_C_white_louvers", origin_xy, u_vec, n_out_vec, um - 0.025, um + 0.025, 0.03, 0.11, z0, z1)
        z = z0 + 0.05
        while z < z1 - 0.04:
            self.add_box_aligned(layer, "mat_C_white_louvers", origin_xy, u_vec, n_out_vec, u0 + 0.05, u1 - 0.05, 0.05, 0.115, z, z + 0.065)
            z += slat_step

    def add_concrete_pergola(self, layer, mat, origin_xy, u_vec, v_vec, u0, u1, v0, v1, z_bot, z_top, num_beams=10):
        bw = 0.24
        self.add_box_aligned(layer, mat, origin_xy, u_vec, v_vec, u0, u1, v0, v0 + bw, z_bot, z_top)
        self.add_box_aligned(layer, mat, origin_xy, u_vec, v_vec, u0, u1, v1 - bw, v1, z_bot, z_top)
        self.add_box_aligned(layer, mat, origin_xy, u_vec, v_vec, u0, u0 + bw, v0 + bw, v1 - bw, z_bot, z_top)
        self.add_box_aligned(layer, mat, origin_xy, u_vec, v_vec, u1 - bw, u1, v0 + bw, v1 - bw, z_bot, z_top)
        span = (u1 - bw) - (u0 + bw)
        step = span / (num_beams + 1)
        for k in range(1, num_beams + 1):
            uk = u0 + bw + k * step
            self.add_box_aligned(layer, mat, origin_xy, u_vec, v_vec, uk - 0.06, uk + 0.06, v0 + bw, v1 - bw, z_bot + 0.04, z_top - 0.02)

    def add_2d_floor_plan_lines(self, layer, segs, mat, z_flr, stroke_w=0.034):
        z_top = z_flr + 0.015
        hw = 0.5 * stroke_w
        for (x0, y0, x1, y1) in segs:
            dx, dy = x1 - x0, y1 - y0
            L = math.hypot(dx, dy)
            if L < 0.025:
                continue
            nx, ny = -dy / L * hw, dx / L * hw
            self.add_quad_3d(
                layer, mat,
                (x0 - nx, y0 - ny, z_top),
                (x1 - nx, y1 - ny, z_top),
                (x1 + nx, y1 + ny, z_top),
                (x0 + nx, y0 + ny, z_top),
            )

    def add_wall_polygon_mesh(self, layer, mat, wp, z_min, z_max):
        ext = wp.get("exterior", [])
        if len(ext) < 3 or abs(z_max - z_min) < 1e-5:
            return
        ext_ring = list(ext)
        if signed_area_2d(ext_ring) < 0:
            ext_ring.reverse()
        rings = [ext_ring]
        for h in wp.get("holes", []):
            if len(h) >= 3:
                hr = list(h)
                if signed_area_2d(hr) > 0:
                    hr.reverse()
                rings.append(hr)

        for ring in rings:
            n = len(ring)
            for i in range(n):
                x0, y0 = ring[i]
                x1, y1 = ring[(i + 1) % n]
                if math.hypot(x1 - x0, y1 - y0) < 1e-5:
                    continue
                self.add_quad_3d(
                    layer, mat,
                    (x0, y0, z_min),
                    (x1, y1, z_min),
                    (x1, y1, z_max),
                    (x0, y0, z_max),
                )

        g = self._get_group(layer, mat)
        for tri in wp.get("tris", []):
            if len(tri) < 3:
                continue
            (ax, ay), (bx, by), (cx, cy) = tri[0], tri[1], tri[2]
            cross_2d = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
            if cross_2d < 0:
                bx, by, cx, cy = cx, cy, bx, by
            # Top cap (+Y normal in 3D)
            base_top = len(g["positions"]) // 3
            for (px, py) in ((ax, ay), (bx, by), (cx, cy)):
                g["positions"].extend(cad_to_3d(px, py, z_max))
                g["normals"].extend((0.0, 1.0, 0.0))
            g["indices"].extend((base_top, base_top + 1, base_top + 2))
            # Bottom cap (-Y normal in 3D)
            base_bot = len(g["positions"]) // 3
            for (px, py) in ((ax, ay), (cx, cy), (bx, by)):
                g["positions"].extend(cad_to_3d(px, py, z_min))
                g["normals"].extend((0.0, -1.0, 0.0))
            g["indices"].extend((base_bot, base_bot + 1, base_bot + 2))

    def add_extracted_floor_walls(self, layer, plan_key, z_flr, z_ceil):
        plan = INTERIOR_PLANS[plan_key]
        for wp in plan.get("wall_polys", []):
            self.add_wall_polygon_mesh(layer, "mat_interior_wall", wp, z_flr, z_ceil)

        self.add_2d_floor_plan_lines(layer, plan.get("furniture_lines", []), "mat_cad_furniture_2d", z_flr, stroke_w=0.036)
        self.add_2d_floor_plan_lines(layer, plan.get("cad_lines", []), "mat_cad_fixtures_2d", z_flr, stroke_w=0.032)

    def add_central_core_stairs_and_elevator(self, layer, z_flr, z_ceil):
        pass


# ==============================================================================
# 3. ASSEMBLE THE COMPLETE EXTERIOR + INTERIOR ARCHITECTURAL MODEL
# ==============================================================================

scene = SceneBuilder()

L_SITE = "0_site_and_ground"
L_F1_5 = "1_floors_1_to_5"
L_F6   = "2_floor_6_penthouse"
L_F7   = "3_floor_7_penthouse"
L_ROOF = "4_upper_roof_and_tower"

# ------------------------------------------------------------------------------
# LAYER 0: SITE CONTEXT, STREETS, SETBACK LINES, RAMP & GROUND FLOOR (0.00..+3.81)
# ------------------------------------------------------------------------------
ROAD_NORTH = [(-6.0, 20.50), (42.0, 30.62), (42.0, 38.50), (-6.0, 28.38)]
ROAD_EAST = [(34.10, -6.00), (42.50, -6.00), (42.50, 34.00), (34.10, 34.00)]
scene.add_extruded_polygon(L_SITE, "mat_road_asphalt", ROAD_NORTH, -0.18, -0.04)
scene.add_extruded_polygon(L_SITE, "mat_road_asphalt", ROAD_EAST, -0.18, -0.04)
scene.add_extruded_polygon(L_SITE, "mat_site_ground", POLY_LOT, -0.15, 0.00)

GREEN_WEST = [(0.25, 0.25), (3.80, 0.25), (3.80, 21.20), (0.25, 21.20)]
GREEN_NORTH = [pt_uv(-2.0, -3.8), pt_uv(21.5, -3.8), pt_uv(21.5, -2.3), pt_uv(-2.0, -2.3)]
scene.add_extruded_polygon(L_SITE, "mat_landscape_green", GREEN_WEST, 0.00, 0.08)
scene.add_extruded_polygon(L_SITE, "mat_landscape_green", GREEN_NORTH, 0.00, 0.08)

n_sb = len(POLY_SETBACK)
for i in range(n_sb):
    p0 = POLY_SETBACK[i]
    p1 = POLY_SETBACK[(i + 1) % n_sb]
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy)
    if L < 0.1:
        continue
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    s = 0.0
    while s < L:
        s_end = min(L, s + 0.65)
        scene.add_box_aligned(L_SITE, "mat_cad_setback", p0, (ux, uy), (nx, ny), s, s_end, -0.06, 0.06, 0.01, 0.04)
        s += 1.05

# Sloped Underground Parking Ramp & South Smoke Ventilation Portals
RAMP_WALL_SOUTH = [(19.50, 0.15), (33.85, 0.15), (33.85, 0.40), (19.50, 0.40)]
RAMP_WALL_NORTH = [(19.50, 3.85), (33.85, 3.85), (33.85, 4.10), (19.50, 4.10)]
scene.add_extruded_polygon(L_SITE, "mat_concrete_curb", RAMP_WALL_SOUTH, -2.50, 1.15)
scene.add_extruded_polygon(L_SITE, "mat_concrete_curb", RAMP_WALL_NORTH, -2.50, 1.15)
scene.add_quad_3d(
    L_SITE, "mat_road_asphalt",
    (33.80, 0.40, 0.00), (33.80, 3.85, 0.00),
    (19.50, 3.85, -2.45), (19.50, 0.40, -2.45)
)
scene.add_box_aligned(L_SITE, "mat_D_white_plaster", (4.00, 4.00), (1, 0), (0, 1), 0.0, 13.25, 0.0, 0.30, 2.81, 3.37)
for px in [4.00, 9.20, 12.40, 14.00, 17.00]:
    scene.add_box_aligned(L_SITE, "mat_D_white_plaster", (px, 4.00), (1, 0), (0, 1), 0.0, 0.35, 0.0, 0.30, 0.0, 2.81)
scene.add_iron_railing_path(L_SITE, [(4.35, 4.15), (9.20, 4.15)], 0.0, height=1.15, curb_h=0.25)
scene.add_iron_railing_path(L_SITE, [(9.55, 4.15), (12.40, 4.15)], 0.0, height=1.15, curb_h=0.25)
scene.add_iron_railing_path(L_SITE, [(14.35, 4.15), (17.00, 4.15)], 0.0, height=1.15, curb_h=0.25)

POLY_GROUND_FLOOR = [
    (4.045, 17.266),
    (26.990, 22.106),
    (29.122, 20.717),
    (30.726, 13.134),
    (30.351, 12.150),
    (30.351, 4.199),
    (17.251, 4.199),
    (17.251, 4.951),
    (12.399, 4.951),
    (12.399, 6.517),
    (6.572, 5.287),
]
scene.add_extruded_polygon(L_SITE, "mat_terrace_tile", POLY_GROUND_FLOOR, 0.00, 0.06)

scene.add_exterior_wall_with_openings(L_SITE, (4.045, 17.266), (26.990, 22.106), 0.25, 0.00, 3.81, [
    {"u0": 12.80, "u1": 17.20, "zBot": 0.00, "zTop": 2.81, "panels": 3, "shutter": False},
    {"u0": 18.20, "u1": 21.20, "zBot": 0.00, "zTop": 2.81, "panels": 2, "shutter": True},
])
scene.add_exterior_wall_with_openings(L_SITE, (26.990, 22.106), (29.122, 20.717), 0.25, 0.00, 3.81, [])
scene.add_exterior_wall_with_openings(L_SITE, (29.122, 20.717), (30.726, 13.134), 0.25, 0.00, 3.81, [
    {"u0": 1.20, "u1": 2.20, "zBot": 1.10, "zTop": 2.10, "panels": 1, "shutter": False, "openOnly": True},
    {"u0": 3.60, "u1": 7.10, "zBot": 0.00, "zTop": 2.81, "panels": 3, "shutter": False},
])
en_u = ((30.726 - 29.122)/7.75, (13.134 - 20.717)/7.75)
en_n = (-en_u[1], en_u[0])
scene.add_louver_screen(L_SITE, (29.122, 20.717), en_u, en_n, 1.20, 2.20, 1.10, 2.10, slat_step=0.12)
scene.add_exterior_wall_with_openings(L_SITE, (30.351, 12.150), (30.351, 4.199), 0.25, 0.00, 3.81, [])
scene.add_exterior_wall_with_openings(L_SITE, (30.351, 4.199), (17.251, 4.199), 0.25, 0.00, 3.81, [
    {"u0": 3.35, "u1": 4.35, "zBot": 1.10, "zTop": 2.10, "panels": 1, "shutter": False, "openOnly": True},
])
scene.add_louver_screen(L_SITE, (30.351, 4.199), (-1, 0), (0, -1), 3.35, 4.35, 1.10, 2.10, slat_step=0.12)
scene.add_exterior_wall_with_openings(L_SITE, (17.251, 4.951), (12.399, 4.951), 0.25, 0.00, 3.81, [])
scene.add_exterior_wall_with_openings(L_SITE, (12.399, 6.517), (6.572, 5.287), 0.25, 0.00, 3.81, [])
scene.add_exterior_wall_with_openings(L_SITE, (6.572, 5.287), (4.045, 17.266), 0.25, 0.00, 3.81, [])

for wp in INTERIOR_PLANS["f1_5"].get("wall_polys", []):
    ext = wp.get("exterior", [])
    if any(12.2 <= x <= 19.2 and 10.8 <= y <= 16.2 for (x, y) in ext):
        scene.add_wall_polygon_mesh(L_SITE, "mat_interior_wall", wp, 0.00, 3.81)
scene.add_central_core_stairs_and_elevator(L_SITE, 0.00, 3.81)

# ------------------------------------------------------------------------------
# LAYER 1: FLOORS 1 TO 5 (קומות 1-5: Z = +3.81m to +19.16m)
# ------------------------------------------------------------------------------
FLOOR_LEVELS_1_5 = [
    (1, 3.81, 4.25, 6.92),
    (2, 6.92, 7.31, 9.98),
    (3, 9.98, 10.37, 13.04),
    (4, 13.04, 13.43, 16.10),
    (5, 16.10, 16.49, 19.16),
]

ne_beam_poly = NE_ARC_OUTER + list(reversed(NE_ARC_INNER))

for fnum, z_soffit, z_flr, z_ceil in FLOOR_LEVELS_1_5:
    scene.add_extruded_polygon(L_F1_5, "mat_D_white_plaster", POLY_F1_5_SLAB, z_soffit, z_flr, top_mat="mat_terrace_tile")
    scene.add_extracted_floor_walls(L_F1_5, "f1_5", z_flr, z_ceil)
    scene.add_central_core_stairs_and_elevator(L_F1_5, z_flr, z_ceil + 0.39)

    z_sill = z_flr + 0.85
    z_mamad_sill = z_flr + 1.05
    z_head = z_flr + 2.35
    z_door = z_flr + 2.42

    # Edge 0 & 1: NW corner pier and 60cm recess step
    scene.add_exterior_wall_with_openings(L_F1_5, (4.045, 17.266), (4.436, 17.349), 0.25, z_flr, z_ceil, [], "mat_D_white_plaster", z_soffit)
    scene.add_exterior_wall_with_openings(L_F1_5, (4.436, 17.349), (4.560, 16.761), 0.25, z_flr, z_ceil, [], "mat_D_white_plaster", z_soffit)

    # Edge 2: Recessed North Wall (4.560, 16.761) -> (21.096, 20.250), L = 16.90m
    scene.add_exterior_wall_with_openings(L_F1_5, (4.560, 16.761), (21.096, 20.250), 0.25, z_flr, z_ceil, [
        {"u0": 0.75,  "u1": 2.15,  "zBot": z_sill, "zTop": z_head, "panels": 2, "shutter": True,  "graySpandrel": True},
        {"u0": 4.25,  "u1": 7.25,  "zBot": z_flr,  "zTop": z_door, "panels": 3, "shutter": True,  "graySpandrel": False},
        {"u0": 8.55,  "u1": 9.25,  "zBot": z_sill, "zTop": z_head, "panels": 1, "shutter": False, "graySpandrel": True},
        {"u0": 10.85, "u1": 11.55, "zBot": z_sill, "zTop": z_head, "panels": 1, "shutter": False, "graySpandrel": True},
        {"u0": 12.90, "u1": 15.90, "zBot": z_flr,  "zTop": z_door, "panels": 3, "shutter": True,  "graySpandrel": False},
    ], "mat_D_white_plaster", z_soffit)
    scene.add_box_aligned(L_F1_5, "mat_B_gray_plaster", (4.560, 16.761), EU, EN_NORTH, 2.15, 3.65, -0.02, 0.03, z_soffit, z_ceil)

    # Edge 3 & 4: Step outward & Flush North Wall (20.972, 20.837) -> (26.990, 22.106), L = 6.15m
    scene.add_exterior_wall_with_openings(L_F1_5, (21.096, 20.250), (20.972, 20.837), 0.25, z_flr, z_ceil, [], "mat_D_white_plaster", z_soffit)
    scene.add_exterior_wall_with_openings(L_F1_5, (20.972, 20.837), (26.990, 22.106), 0.25, z_flr, z_ceil, [
        {"u0": 1.50, "u1": 2.90, "zBot": z_sill, "zTop": z_head, "panels": 2, "shutter": True, "graySpandrel": True},
    ], "mat_D_white_plaster", z_soffit)
    scene.add_box_aligned(L_F1_5, "mat_B_gray_plaster", (20.972, 20.837), EU, EN_NORTH, 0.00, 1.50, -0.02, 0.03, z_soffit, z_ceil)

    # Edge 5 & 6: Curved NE Corner Balcony Walls
    scene.add_exterior_wall_with_openings(L_F1_5, (26.990, 22.106), (27.268, 21.039), 0.25, z_flr, z_ceil, [
        {"u0": 0.15, "u1": 0.95, "zBot": z_flr, "zTop": z_head, "panels": 1, "shutter": True},
    ], "mat_D_white_plaster", z_soffit)
    scene.add_exterior_wall_with_openings(L_F1_5, (27.268, 21.039), (29.122, 20.717), 0.25, z_flr, z_ceil, [
        {"u0": 0.35, "u1": 1.35, "zBot": z_sill, "zTop": z_head, "panels": 2, "shutter": True},
    ], "mat_D_white_plaster", z_soffit)

    # Edge 7: East-North Tilted Wall (29.122, 20.717) -> (30.726, 13.134), L = 7.75m
    scene.add_exterior_wall_with_openings(L_F1_5, (29.122, 20.717), (30.726, 13.134), 0.25, z_flr, z_ceil, [
        {"u0": 0.95, "u1": 1.95, "zBot": z_mamad_sill, "zTop": z_flr + 2.15, "panels": 1, "shutter": False, "graySpandrel": True},
        {"u0": 3.95, "u1": 5.35, "zBot": z_sill,       "zTop": z_head,       "panels": 2, "shutter": True,  "graySpandrel": True},
        {"u0": 6.25, "u1": 7.25, "zBot": z_flr,        "zTop": z_head,       "panels": 1, "shutter": False, "graySpandrel": False},
    ], "mat_D_white_plaster", z_soffit)

    # Edge 8, 9, 10: East Vertical Wall (30.351, 12.150) -> (30.351, 4.199), L = 7.951m
    scene.add_exterior_wall_with_openings(L_F1_5, (30.726, 13.134), (30.726, 12.150), 0.25, z_flr, z_ceil, [], "mat_D_white_plaster", z_soffit)
    scene.add_exterior_wall_with_openings(L_F1_5, (30.726, 12.150), (30.351, 12.150), 0.25, z_flr, z_ceil, [], "mat_D_white_plaster", z_soffit)
    scene.add_exterior_wall_with_openings(L_F1_5, (30.351, 12.150), (30.351, 4.199), 0.25, z_flr, z_ceil, [
        {"u0": 1.20, "u1": 4.20, "zBot": z_flr,  "zTop": z_door, "panels": 3, "shutter": True, "graySpandrel": False},
        {"u0": 6.00, "u1": 7.40, "zBot": z_sill, "zTop": z_head, "panels": 2, "shutter": True, "graySpandrel": True},
    ], "mat_D_white_plaster", z_soffit)

    # Edge 11..17: South Walls
    scene.add_exterior_wall_with_openings(L_F1_5, (30.351, 4.199), (22.849, 4.199), 0.25, z_flr, z_ceil, [
        {"u0": 1.05, "u1": 2.45, "zBot": z_sill,       "zTop": z_head,       "panels": 2, "shutter": True,  "graySpandrel": True},
        {"u0": 5.65, "u1": 6.65, "zBot": z_mamad_sill, "zTop": z_flr + 2.15, "panels": 1, "shutter": False, "graySpandrel": True},
    ], "mat_D_white_plaster", z_soffit)
    scene.add_exterior_wall_with_openings(L_F1_5, (22.849, 4.199), (22.849, 4.100), 0.25, z_flr, z_ceil, [], "mat_D_white_plaster", z_soffit)
    scene.add_exterior_wall_with_openings(L_F1_5, (22.849, 4.100), (17.251, 4.100), 0.25, z_flr, z_ceil, [
        {"u0": 1.55, "u1": 2.95, "zBot": z_sill,       "zTop": z_head,       "panels": 2, "shutter": True,  "graySpandrel": True},
        {"u0": 4.00, "u1": 4.50, "zBot": z_mamad_sill, "zTop": z_flr + 2.15, "panels": 1, "shutter": False, "graySpandrel": True},
    ], "mat_D_white_plaster", z_soffit)
    scene.add_exterior_wall_with_openings(L_F1_5, (17.251, 4.100), (17.251, 4.951), 0.25, z_flr, z_ceil, [], "mat_D_white_plaster", z_soffit)
    scene.add_exterior_wall_with_openings(L_F1_5, (17.251, 4.951), (12.399, 4.951), 0.25, z_flr, z_ceil, [
        {"u0": 1.10, "u1": 2.00, "zBot": z_sill, "zTop": z_head, "panels": 1, "shutter": False},
        {"u0": 2.60, "u1": 3.40, "zBot": z_flr,  "zTop": z_head, "panels": 1, "shutter": False},
    ], "mat_D_white_plaster", z_soffit)
    scene.add_exterior_wall_with_openings(L_F1_5, (12.399, 4.951), (12.399, 6.517), 0.25, z_flr, z_ceil, [], "mat_D_white_plaster", z_soffit)
    scene.add_exterior_wall_with_openings(L_F1_5, (12.399, 6.517), (6.572, 5.287), 0.25, z_flr, z_ceil, [], "mat_D_white_plaster", z_soffit)

    # Edge 18: West Wall (6.572, 5.287) -> (4.045, 17.266), L = 12.242m
    scene.add_exterior_wall_with_openings(L_F1_5, (6.572, 5.287), (4.045, 17.266), 0.25, z_flr, z_ceil, [
        {"u0": 1.29,  "u1": 2.29,  "zBot": z_mamad_sill, "zTop": z_flr + 2.15, "panels": 1, "shutter": False, "graySpandrel": True},
        {"u0": 3.34,  "u1": 4.34,  "zBot": z_sill,       "zTop": z_head,       "panels": 1, "shutter": False, "graySpandrel": False},
        {"u0": 5.94,  "u1": 6.44,  "zBot": z_mamad_sill, "zTop": z_head,       "panels": 1, "shutter": False, "graySpandrel": True},
        {"u0": 7.69,  "u1": 8.19,  "zBot": z_mamad_sill, "zTop": z_head,       "panels": 1, "shutter": False, "graySpandrel": True},
        {"u0": 10.64, "u1": 11.24, "zBot": z_sill,       "zTop": z_head,       "panels": 1, "shutter": True,  "graySpandrel": True},
    ], "mat_D_white_plaster", z_soffit)

    # Curved NE Corner Decorative Beam & Railing + Balconies
    scene.add_extruded_polygon(L_F1_5, "mat_D_white_plaster", ne_beam_poly, z_ceil - 0.35, z_ceil)
    scene.add_iron_railing_path(L_F1_5, NE_ARC_OUTER, z_flr, height=1.05, curb_h=0.18, closed=False)

    for b_poly in (BALCONY_NW, BALCONY_NC, BALCONY_E):
        scene.add_extruded_polygon(L_F1_5, "mat_concrete_curb", b_poly, z_soffit, z_flr, top_mat="mat_terrace_tile")
        scene.add_iron_railing_path(L_F1_5, b_poly, z_flr, height=1.05, curb_h=0.22, closed=False)

    scene.add_extruded_polygon(L_F1_5, "mat_concrete_curb", BALCONY_S_SERVICE, z_soffit, z_flr, top_mat="mat_terrace_tile")
    scene.add_iron_railing_path(L_F1_5, [(13.601, 4.951), (13.601, 4.100), (15.150, 4.100)], z_flr, height=1.05, curb_h=0.18)

# Material B Vertical Balcony L-Frames & Material C White Aluminum Louver Shafts
scene.add_box_aligned(L_F1_5, "mat_B_gray_plaster", NW_CORNER, EU, EN_NORTH, 8.55, 8.95, -0.60, 1.90, 3.81, 23.60)
scene.add_box_aligned(L_F1_5, "mat_B_gray_plaster", NW_CORNER, EU, EN_NORTH, 3.70, 4.10, -0.60, 0.35, 3.81, 23.60)
scene.add_box_aligned(L_F1_5, "mat_B_gray_plaster", NW_CORNER, EU, EN_NORTH, 12.35, 12.75, -0.60, 1.90, 3.81, 19.45)
scene.add_box_aligned(L_F1_5, "mat_B_gray_plaster", NW_CORNER, EU, EN_NORTH, 17.20, 17.60, -0.60, 0.35, 3.81, 19.45)
scene.add_box_aligned(L_F1_5, "mat_B_gray_plaster", (30.351, 0.0), (0, 1), (1, 0), 6.35, 6.75, 0.00, 2.20, 3.81, 23.40)
scene.add_box_aligned(L_F1_5, "mat_B_gray_plaster", (30.351, 0.0), (0, 1), (1, 0), 12.15, 12.55, 0.00, 0.40, 3.81, 23.40)

scene.add_louver_screen(L_F1_5, (6.572, 5.287), (-ES[0], -ES[1]), EN_WEST, 3.10, 4.65, 4.11, 22.39)
scene.add_louver_screen(L_F1_5, (29.122, 20.717), en_u, en_n, 5.85, 7.55, 4.11, 19.16)
scene.add_louver_screen(L_F1_5, (17.251, 4.951), (-1, 0), (0, -1), 0.85, 2.25, 4.11, 22.39)

# ------------------------------------------------------------------------------
# LAYER 2: FLOOR 6 PENTHOUSE DUPLEX LOWER LEVEL (קומה 6: Z = +19.16m to +22.55m)
# ------------------------------------------------------------------------------
z_f6_flr, z_f6_ceil, z_f6_sill, z_f6_mamad_sill, z_f6_head, z_f6_door = 19.72, 22.55, 20.57, 20.77, 22.12, 22.17

scene.add_extruded_polygon(L_F6, "mat_D_white_plaster", POLY_OUTER, 19.16, z_f6_flr, top_mat="mat_terrace_tile")
scene.add_extracted_floor_walls(L_F6, "f6", z_f6_flr, z_f6_ceil)

# Exact Floor 6 Exterior Walls & Openings
scene.add_exterior_wall_with_openings(L_F6, (4.045, 17.266), (16.863, 19.971), 0.25, z_f6_flr, z_f6_ceil, [
    {"u0": 1.15, "u1": 2.55,  "zBot": z_f6_sill, "zTop": z_f6_head, "panels": 2, "shutter": True, "graySpandrel": True},
    {"u0": 4.85, "u1": 7.85,  "zBot": z_f6_flr,  "zTop": z_f6_door, "panels": 3, "shutter": True, "graySpandrel": False},
    {"u0": 9.85, "u1": 11.25, "zBot": z_f6_sill, "zTop": z_f6_head, "panels": 2, "shutter": True, "graySpandrel": False},
], "mat_D_white_plaster", 19.16)
scene.add_box_aligned(L_F6, "mat_B_gray_plaster", (4.045, 17.266), EU, EN_NORTH, 2.55, 3.70, -0.02, 0.03, 19.16, z_f6_ceil)

scene.add_exterior_wall_with_openings(L_F6, (16.863, 19.971), (17.617, 16.400), 0.25, z_f6_flr, z_f6_ceil, [
    {"u0": 0.65, "u1": 2.65, "zBot": z_f6_flr, "zTop": z_f6_door, "panels": 2, "shutter": True},
])
scene.add_exterior_wall_with_openings(L_F6, (17.617, 16.400), (18.440, 16.368), 0.25, z_f6_flr, z_f6_ceil, [])
scene.add_exterior_wall_with_openings(L_F6, (18.440, 16.368), (19.039, 13.530), 0.25, z_f6_flr, z_f6_ceil, [])
scene.add_exterior_wall_with_openings(L_F6, (19.039, 13.530), (21.984, 14.150), 0.25, z_f6_flr, z_f6_ceil, [], "mat_B_gray_plaster")
scene.add_exterior_wall_with_openings(L_F6, (21.984, 14.150), (30.351, 14.150), 0.25, z_f6_flr, z_f6_ceil, [
    {"u0": 2.81, "u1": 5.72, "zBot": z_f6_flr, "zTop": z_f6_door, "panels": 3, "shutter": True},
    {"u0": 6.67, "u1": 7.47, "zBot": z_f6_flr, "zTop": z_f6_door, "panels": 1, "shutter": True},
], "mat_B_gray_plaster")
scene.add_exterior_wall_with_openings(L_F6, (30.351, 14.150), (30.351, 7.550), 0.25, z_f6_flr, z_f6_ceil, [
    {"u0": 0.55, "u1": 1.95, "zBot": z_f6_sill, "zTop": z_f6_head, "panels": 2, "shutter": True},
    {"u0": 2.55, "u1": 5.55, "zBot": z_f6_flr,  "zTop": z_f6_door, "panels": 3, "shutter": True},
])
scene.add_exterior_wall_with_openings(L_F6, (30.351, 7.550), (26.151, 7.550), 0.25, z_f6_flr, z_f6_ceil, [
    {"u0": 2.20, "u1": 3.83, "zBot": z_f6_flr, "zTop": z_f6_head, "panels": 2, "shutter": True},
])
scene.add_exterior_wall_with_openings(L_F6, (26.151, 7.550), (26.151, 4.199), 0.25, z_f6_flr, z_f6_ceil, [
    {"u0": 0.75, "u1": 2.55, "zBot": z_f6_flr, "zTop": z_f6_head, "panels": 2, "shutter": True},
])
scene.add_exterior_wall_with_openings(L_F6, (26.151, 4.199), (22.849, 4.199), 0.25, z_f6_flr, z_f6_ceil, [
    {"u0": 1.45, "u1": 2.45, "zBot": z_f6_mamad_sill, "zTop": z_f6_flr + 2.15, "panels": 1, "shutter": False, "graySpandrel": True},
], "mat_D_white_plaster", 19.16)
scene.add_exterior_wall_with_openings(L_F6, (22.849, 4.199), (22.849, 4.100), 0.25, z_f6_flr, z_f6_ceil, [])
scene.add_exterior_wall_with_openings(L_F6, (22.849, 4.100), (17.251, 4.100), 0.25, z_f6_flr, z_f6_ceil, [
    {"u0": 1.55, "u1": 2.95, "zBot": z_f6_sill,       "zTop": z_f6_head,       "panels": 2, "shutter": True,  "graySpandrel": True},
    {"u0": 4.00, "u1": 4.50, "zBot": z_f6_mamad_sill, "zTop": z_f6_flr + 2.15, "panels": 1, "shutter": False, "graySpandrel": True},
], "mat_D_white_plaster", 19.16)
scene.add_exterior_wall_with_openings(L_F6, (17.251, 4.100), (17.251, 4.951), 0.25, z_f6_flr, z_f6_ceil, [])
scene.add_exterior_wall_with_openings(L_F6, (17.251, 4.951), (12.399, 4.951), 0.25, z_f6_flr, z_f6_ceil, [
    {"u0": 1.10, "u1": 2.00, "zBot": z_f6_sill, "zTop": z_f6_head, "panels": 1, "shutter": False},
    {"u0": 2.60, "u1": 3.40, "zBot": z_f6_flr,  "zTop": z_f6_head, "panels": 1, "shutter": False},
], "mat_D_white_plaster", 19.16)
scene.add_exterior_wall_with_openings(L_F6, (12.399, 4.951), (12.399, 6.517), 0.25, z_f6_flr, z_f6_ceil, [])
scene.add_exterior_wall_with_openings(L_F6, (12.399, 6.517), (6.572, 5.287), 0.25, z_f6_flr, z_f6_ceil, [])
scene.add_exterior_wall_with_openings(L_F6, (6.572, 5.287), (4.045, 17.266), 0.25, z_f6_flr, z_f6_ceil, [
    {"u0": 1.29,  "u1": 2.29,  "zBot": z_f6_mamad_sill, "zTop": z_f6_flr + 2.15, "panels": 1, "shutter": False, "graySpandrel": True},
    {"u0": 3.34,  "u1": 4.34,  "zBot": z_f6_sill,       "zTop": z_f6_head,       "panels": 1, "shutter": False, "graySpandrel": False},
    {"u0": 5.94,  "u1": 6.44,  "zBot": z_f6_mamad_sill, "zTop": z_f6_head,       "panels": 1, "shutter": False, "graySpandrel": True},
    {"u0": 7.69,  "u1": 8.19,  "zBot": z_f6_mamad_sill, "zTop": z_f6_head,       "panels": 1, "shutter": False, "graySpandrel": True},
    {"u0": 10.64, "u1": 11.24, "zBot": z_f6_sill,       "zTop": z_f6_head,       "panels": 1, "shutter": True,  "graySpandrel": True},
], "mat_D_white_plaster", 19.16)

scene.add_extruded_polygon(L_F6, "mat_concrete_curb", BALCONY_NW_F6, 19.16, z_f6_flr, top_mat="mat_terrace_tile")
scene.add_iron_railing_path(L_F6, BALCONY_NW_F6, z_f6_flr, height=1.05, curb_h=0.22)
scene.add_extruded_polygon(L_F6, "mat_concrete_curb", BALCONY_E, 19.16, z_f6_flr, top_mat="mat_terrace_tile")
scene.add_iron_railing_path(L_F6, BALCONY_E, z_f6_flr, height=1.05, curb_h=0.22)
scene.add_extruded_polygon(L_F6, "mat_concrete_curb", BALCONY_S_SERVICE, 19.16, z_f6_flr, top_mat="mat_terrace_tile")
scene.add_iron_railing_path(L_F6, [(13.601, 4.951), (13.601, 4.100), (15.150, 4.100)], z_f6_flr, height=1.05, curb_h=0.18)

scene.add_concrete_pergola(L_F6, "mat_B_gray_plaster", NW_CORNER, EU, EN_NORTH, 12.55, 17.40, 0.0, 1.90, 19.16, 19.52, num_beams=9)
scene.add_extruded_polygon(L_F6, "mat_D_white_plaster", ne_beam_poly, 19.16, 19.52)

scene.add_iron_railing_path(L_F6, [(16.863, 19.971)] + NE_ARC_OUTER + [(30.726, 13.134), (30.726, 12.150), (30.351, 12.150)], z_f6_flr, height=1.05, curb_h=0.22)
scene.add_wall_strip(L_F6, "mat_D_white_plaster", [(21.25, 20.89), (21.984, 14.150)], 0.20, z_f6_flr, 21.72)
scene.add_iron_railing_path(L_F6, [(26.151, 4.199), (30.351, 4.199), (30.351, 7.550)], z_f6_flr, height=1.05, curb_h=0.22)
scene.add_box_aligned(L_F6, "mat_D_white_plaster", (30.10, 4.20), (1, 0), (0, 1), 0.0, 0.25, 0.0, 0.25, z_f6_flr, 24.00)
scene.add_wall_strip(L_F6, "mat_D_white_plaster", [(26.151, 4.199), (30.351, 4.199), (30.351, 7.550)], 0.24, 22.55, 24.00)

# ------------------------------------------------------------------------------
# LAYER 3: FLOOR 7 PENTHOUSE DUPLEX UPPER LEVEL (קומה 7: Z = +22.95m to +25.53m)
# ------------------------------------------------------------------------------
z_f7_flr, z_f7_ceil, z_f7_sill, z_f7_bath_sill, z_f7_head = 22.95, 25.53, 23.80, 24.00, 25.20

scene.add_extruded_polygon(L_F7, "mat_D_white_plaster", POLY_F6_WALLS, 22.55, z_f7_flr, top_mat="mat_terrace_tile")
scene.add_extracted_floor_walls(L_F7, "f7", z_f7_flr, z_f7_ceil)
scene.add_central_core_stairs_and_elevator(L_F7, z_f7_flr, z_f7_ceil)

scene.add_exterior_wall_with_openings(L_F7, (7.628, 14.086), (18.440, 16.368), 0.25, z_f7_flr, z_f7_ceil, [
    {"u0": 3.70, "u1": 4.20,  "zBot": z_f7_bath_sill, "zTop": z_f7_head, "panels": 1, "shutter": False},
    {"u0": 8.85, "u1": 10.05, "zBot": z_f7_sill,      "zTop": z_f7_head, "panels": 2, "shutter": False},
], "mat_B_gray_plaster")
scene.add_exterior_wall_with_openings(L_F7, (18.440, 16.368), (19.039, 13.530), 0.25, z_f7_flr, z_f7_ceil, [], "mat_B_gray_plaster")
scene.add_exterior_wall_with_openings(L_F7, (19.039, 13.530), (21.984, 14.150), 0.25, z_f7_flr, z_f7_ceil, [], "mat_B_gray_plaster")
scene.add_exterior_wall_with_openings(L_F7, (21.984, 14.150), (23.899, 14.150), 0.25, z_f7_flr, z_f7_ceil, [], "mat_B_gray_plaster")
scene.add_exterior_wall_with_openings(L_F7, (23.899, 14.150), (23.899, 11.250), 0.25, z_f7_flr, z_f7_ceil, [], "mat_B_gray_plaster")
scene.add_exterior_wall_with_openings(L_F7, (23.899, 11.250), (26.151, 11.250), 0.25, z_f7_flr, z_f7_ceil, [], "mat_B_gray_plaster")

scene.add_exterior_wall_with_openings(L_F7, (26.151, 11.250), (26.151, 5.850), 0.25, z_f7_flr, z_f7_ceil, [
    {"u0": 2.30, "u1": 3.30, "zBot": z_f7_flr,  "zTop": z_f7_head, "panels": 1, "shutter": True},
    {"u0": 3.95, "u1": 4.75, "zBot": z_f7_sill, "zTop": z_f7_head, "panels": 1, "shutter": True},
], "mat_B_gray_plaster")
scene.add_exterior_wall_with_openings(L_F7, (26.151, 5.850), (18.201, 5.848), 0.25, z_f7_flr, z_f7_ceil, [
    {"u0": 1.55, "u1": 3.35, "zBot": z_f7_flr,       "zTop": z_f7_head, "panels": 2, "shutter": True},
    {"u0": 6.55, "u1": 7.05, "zBot": z_f7_bath_sill, "zTop": z_f7_head, "panels": 1, "shutter": False},
], "mat_B_gray_plaster")

scene.add_exterior_wall_with_openings(L_F7, (18.201, 5.848), (18.201, 9.550), 0.25, z_f7_flr, z_f7_ceil, [])
scene.add_exterior_wall_with_openings(L_F7, (18.201, 9.550), (17.437, 9.550), 0.25, z_f7_flr, z_f7_ceil, [])
scene.add_exterior_wall_with_openings(L_F7, (17.437, 9.550), (17.437, 10.329), 0.25, z_f7_flr, z_f7_ceil, [])
scene.add_exterior_wall_with_openings(L_F7, (17.437, 10.329), (15.502, 9.921), 0.25, z_f7_flr, z_f7_ceil, [])
scene.add_exterior_wall_with_openings(L_F7, (15.502, 9.921), (15.970, 7.698), 0.25, z_f7_flr, z_f7_ceil, [])
scene.add_exterior_wall_with_openings(L_F7, (15.970, 7.698), (10.295, 6.502), 0.25, z_f7_flr, z_f7_ceil, [
    {"u0": 1.20, "u1": 3.00, "zBot": z_f7_flr, "zTop": z_f7_head, "panels": 2, "shutter": True},
])
scene.add_exterior_wall_with_openings(L_F7, (10.295, 6.502), (9.394, 10.778), 0.25, z_f7_flr, z_f7_ceil, [
    {"u0": 3.37, "u1": 4.37, "zBot": z_f7_sill, "zTop": z_f7_head, "panels": 1, "shutter": True},
])
scene.add_exterior_wall_with_openings(L_F7, (9.394, 10.778), (8.371, 10.564), 0.25, z_f7_flr, z_f7_ceil, [])
scene.add_exterior_wall_with_openings(L_F7, (8.371, 10.564), (7.628, 14.086), 0.25, z_f7_flr, z_f7_ceil, [
    {"u0": 0.60, "u1": 2.40, "zBot": z_f7_flr, "zTop": z_f7_head, "panels": 2, "shutter": True},
], "mat_B_gray_plaster")

# Outer Perimeter Screen Walls, Pergolas & Railings up to +24.00
scene.add_wall_strip(L_F7, "mat_D_white_plaster", [(6.572, 5.287), (4.045, 17.266), (16.863, 19.971), (17.617, 16.400)], 0.25, 22.55, 24.00)
scene.add_concrete_pergola(L_F7, "mat_B_gray_plaster", NW_CORNER, EU, EN_NORTH, 3.80, 8.85, 0.0, 1.90, 23.15, 23.60, num_beams=10)
scene.add_concrete_pergola(L_F7, "mat_D_white_plaster", NW_CORNER, EU, (-EN_NORTH[0], -EN_NORTH[1]), 0.25, 12.80, 0.25, 3.20, 23.65, 24.00, num_beams=16)

scene.add_concrete_pergola(L_F7, "mat_B_gray_plaster", (30.351, 0.0), (0, 1), (1, 0), 6.50, 12.35, 0.0, 2.20, 22.95, 23.40, num_beams=11)
scene.add_concrete_pergola(L_F7, "mat_B_gray_plaster", (26.151, 7.550), (1, 0), (0, 1), 0.0, 4.20, 0.0, 6.60, 23.60, 24.00, num_beams=9)
scene.add_box_aligned(L_F7, "mat_B_gray_plaster", (30.10, 7.55), (1, 0), (0, 1), 0.0, 0.25, 0.0, 0.25, 22.55, 24.00)
scene.add_box_aligned(L_F7, "mat_B_gray_plaster", (30.10, 13.90), (1, 0), (0, 1), 0.0, 0.25, 0.0, 0.25, 22.55, 24.00)
scene.add_iron_railing_path(L_F7, [(26.151, 7.550), (30.351, 7.550), (30.351, 14.150), (23.899, 14.150)], z_f7_flr, height=1.05, curb_h=0.22)

scene.add_wall_strip(L_F7, "mat_D_white_plaster", [(6.572, 5.287), (12.399, 6.517), (12.399, 4.951), (17.251, 4.951), (17.251, 4.100), (22.849, 4.100), (22.849, 4.199), (26.151, 4.199), (26.151, 5.850)], 0.24, 22.55, 24.00)
scene.add_concrete_pergola(L_F7, "mat_D_white_plaster", (10.30, 4.95), (1, 0), (0, 1), 0.0, 6.95, 0.0, 2.70, 23.65, 24.00, num_beams=10)

# ------------------------------------------------------------------------------
# LAYER 4: UPPER ROOF PARAPETS, STAIR/ELEVATOR TOWER & 10 SOLAR COLLECTORS (+25.53..+28.67m)
# ------------------------------------------------------------------------------
scene.add_extruded_polygon(L_ROOF, "mat_D_white_plaster", POLY_UPPER_ROOF_OUTER, 25.30, 25.53, top_mat="mat_terrace_tile")
scene.add_wall_strip(L_ROOF, "mat_B_gray_plaster", [(8.371, 10.564), (7.628, 14.086), (12.611, 14.933)], 0.26, 25.53, 26.97)
scene.add_wall_strip(L_ROOF, "mat_B_gray_plaster", [(19.039, 13.530), (21.984, 14.150), (23.899, 14.150), (23.899, 11.250), (26.151, 11.250), (26.151, 5.850), (18.201, 5.848)], 0.26, 25.53, 26.97)
scene.add_wall_strip(L_ROOF, "mat_D_white_plaster", [(18.201, 5.848), (18.201, 9.550), (17.437, 9.550), (17.437, 10.329), (15.502, 9.921), (15.970, 7.698), (10.295, 6.502), (9.394, 10.778), (8.371, 10.564)], 0.25, 25.53, 27.37)

scene.add_extruded_polygon(L_ROOF, "mat_D_white_plaster", POLY_TOWER_OUTER, 25.53, 28.67, top_mat="mat_terrace_tile")
scene.add_window_assembly(L_ROOF, (13.354, 11.411), EU, (-EN_NORTH[0], -EN_NORTH[1]), 1.20, 2.20, 25.60, 27.70, has_shutter_box=False, num_panels=1)
scene.add_window_assembly(L_ROOF, (12.611, 14.933), EU, EN_NORTH, 1.10, 2.90, 26.50, 28.10, has_shutter_box=False, num_panels=2)

def add_solar_collector(origin_xy, u_vec, v_vec, w=1.40, l=1.50, z_deck=25.53):
    scene.add_box_aligned(L_ROOF, "mat_alu_frame", origin_xy, u_vec, v_vec, 0.05, 0.12, 0.10, l - 0.10, z_deck, z_deck + 0.20)
    scene.add_box_aligned(L_ROOF, "mat_alu_frame", origin_xy, u_vec, v_vec, w - 0.12, w - 0.05, 0.10, l - 0.10, z_deck, z_deck + 0.20)
    scene.add_box_aligned(L_ROOF, "mat_alu_frame", origin_xy, u_vec, v_vec, 0.05, 0.12, l - 0.20, l - 0.08, z_deck, z_deck + 0.85)
    scene.add_box_aligned(L_ROOF, "mat_alu_frame", origin_xy, u_vec, v_vec, w - 0.12, w - 0.05, l - 0.20, l - 0.08, z_deck, z_deck + 0.85)
    ox, oy = origin_xy
    ux, uy = u_vec
    vx, vy = v_vec
    p0 = (ox, oy, z_deck + 0.22)
    p1 = (ox + w*ux, oy + w*uy, z_deck + 0.22)
    p2 = (ox + w*ux + l*vx, oy + w*uy + l*vy, z_deck + 0.88)
    p3 = (ox + l*vx, oy + l*vy, z_deck + 0.88)
    scene.add_quad_3d(L_ROOF, "mat_solar_panel", p0, p1, p2, p3)
    scene.add_box_aligned(L_ROOF, "mat_C_white_louvers", origin_xy, u_vec, v_vec, 0.20, w - 0.20, l - 0.35, l + 0.05, z_deck + 0.82, z_deck + 1.18)

WEST_SOLAR_ORIGINS = [
    (8.98, 12.15), (10.74, 12.52),
    (9.45, 7.66),  (11.21, 8.03),  (12.97, 8.40)
]
for orig in WEST_SOLAR_ORIGINS:
    add_solar_collector(orig, EU, EN_NORTH)

EAST_SOLAR_ORIGINS = [
    (18.92, 9.75), (20.80, 9.75),
    (18.88, 7.45), (20.88, 7.45), (22.88, 7.45)
]
for orig in EAST_SOLAR_ORIGINS:
    add_solar_collector(orig, (1.0, 0.0), (0.0, 1.0))

TREE_COORDS = [
    (2.1, 3.0, 4.2), (1.8, 9.5, 5.0), (2.0, 15.5, 4.5),
    (6.0, 21.8, 4.8), (14.5, 23.6, 5.2), (23.5, 25.4, 4.6),
    (32.5, 16.5, 4.5), (32.5, 21.0, 4.2)
]
for (tx, ty, th) in TREE_COORDS:
    scene.add_box_aligned(L_SITE, "mat_concrete_curb", (tx, ty), (1, 0), (0, 1), -0.12, 0.12, -0.12, 0.12, 0.00, th * 0.42)
    oct_pts = [(tx + 1.15*math.cos(a), ty + 1.15*math.sin(a)) for a in [i*math.pi/4 for i in range(8)]]
    scene.add_extruded_polygon(L_SITE, "mat_landscape_green", oct_pts, th * 0.38, th * 0.85)
    oct_top = [(tx + 0.75*math.cos(a), ty + 0.75*math.sin(a)) for a in [i*math.pi/4 for i in range(8)]]
    scene.add_extruded_polygon(L_SITE, "mat_landscape_green", oct_top, th * 0.85, th * 1.05)


# ==============================================================================
# 4. EXPORT WAVEFRONT .OBJ + .MTL, BINARY .GLB (glTF 2.0), AND COMPACT JSON
# ==============================================================================

def export_obj_and_mtl(scene, obj_path, mtl_path):
    mtl_name = os.path.basename(mtl_path)
    with open(mtl_path, "w", encoding="utf-8") as mf:
        mf.write("# Pines 48, Petah Tikva - Architectural CAD Materials (Exterior + Interior)\n")
        for mid, m in scene.materials.items():
            r, g, b = m["color"]
            mf.write(f"\nnewmtl {mid}\n")
            mf.write(f"Kd {r:.4f} {g:.4f} {b:.4f}\n")
            mf.write(f"Ka {r*0.2:.4f} {g*0.2:.4f} {b*0.2:.4f}\n")
            mf.write(f"Ks 0.1500 0.1500 0.1500\n")
            mf.write(f"d {m['opacity']:.4f}\n")

    with open(obj_path, "w", encoding="utf-8") as of:
        of.write("# Pines 48, Petah Tikva (פינס 48, פתח תקוה) - 1:50 Exterior & Interior Architectural 3D Model\n")
        of.write(f"mtllib {mtl_name}\n")
        v_offset = 1
        for (layer, mat), grp in scene.groups.items():
            pos = grp["positions"]
            nrm = grp["normals"]
            idx = grp["indices"]
            if not idx:
                continue
            of.write(f"\ng {layer}__{mat}\n")
            of.write(f"usemtl {mat}\n")
            num_v = len(pos) // 3
            for i in range(num_v):
                of.write(f"v {pos[3*i]:.4f} {pos[3*i+1]:.4f} {pos[3*i+2]:.4f}\n")
            for i in range(num_v):
                of.write(f"vn {nrm[3*i]:.4f} {nrm[3*i+1]:.4f} {nrm[3*i+2]:.4f}\n")
            for i in range(0, len(idx), 3):
                i0 = idx[i] + v_offset
                i1 = idx[i+1] + v_offset
                i2 = idx[i+2] + v_offset
                of.write(f"f {i0}//{i0} {i1}//{i1} {i2}//{i2}\n")
            v_offset += num_v

def export_glb(scene, glb_path):
    mat_keys = list(scene.materials.keys())
    mat_index = {k: i for i, k in enumerate(mat_keys)}

    gltf_materials = []
    for k in mat_keys:
        m = scene.materials[k]
        r, g, b = m["color"]
        mat_def = {
            "name": k,
            "pbrMetallicRoughness": {
                "baseColorFactor": [r, g, b, m["opacity"]],
                "metallicFactor": m["metalness"],
                "roughnessFactor": m["roughness"],
            },
            "doubleSided": True,
        }
        if m["opacity"] < 0.99:
            mat_def["alphaMode"] = "BLEND"
        gltf_materials.append(mat_def)

    bin_chunks = bytearray()
    buffer_views = []
    accessors = []
    meshes = []
    nodes = []

    for (layer, mat), grp in scene.groups.items():
        pos = grp["positions"]
        nrm = grp["normals"]
        idx = grp["indices"]
        if not idx:
            continue
        num_v = len(pos) // 3
        xs = pos[0::3]
        ys = pos[1::3]
        zs = pos[2::3]
        vmin = [min(xs), min(ys), min(zs)]
        vmax = [max(xs), max(ys), max(zs)]

        pos_bytes = struct.pack(f"<{len(pos)}f", *pos)
        pos_offset = len(bin_chunks)
        bin_chunks.extend(pos_bytes)
        bv_pos = len(buffer_views)
        buffer_views.append({"buffer": 0, "byteOffset": pos_offset, "byteLength": len(pos_bytes), "target": 34962})
        acc_pos = len(accessors)
        accessors.append({
            "bufferView": bv_pos, "componentType": 5126, "count": num_v,
            "type": "VEC3", "min": vmin, "max": vmax
        })

        nrm_bytes = struct.pack(f"<{len(nrm)}f", *nrm)
        nrm_offset = len(bin_chunks)
        bin_chunks.extend(nrm_bytes)
        bv_nrm = len(buffer_views)
        buffer_views.append({"buffer": 0, "byteOffset": nrm_offset, "byteLength": len(nrm_bytes), "target": 34962})
        acc_nrm = len(accessors)
        accessors.append({
            "bufferView": bv_nrm, "componentType": 5126, "count": num_v, "type": "VEC3"
        })

        idx_bytes = struct.pack(f"<{len(idx)}I", *idx)
        idx_offset = len(bin_chunks)
        bin_chunks.extend(idx_bytes)
        bv_idx = len(buffer_views)
        buffer_views.append({"buffer": 0, "byteOffset": idx_offset, "byteLength": len(idx_bytes), "target": 34963})
        acc_idx = len(accessors)
        accessors.append({
            "bufferView": bv_idx, "componentType": 5125, "count": len(idx), "type": "SCALAR"
        })

        mesh_id = len(meshes)
        meshes.append({
            "name": f"{layer}__{mat}",
            "primitives": [{
                "attributes": {"POSITION": acc_pos, "NORMAL": acc_nrm},
                "indices": acc_idx,
                "material": mat_index[mat],
            }]
        })
        nodes.append({"name": f"{layer}__{mat}", "mesh": mesh_id})

    while len(bin_chunks) % 4 != 0:
        bin_chunks.append(0)

    gltf_dict = {
        "asset": {"version": "2.0", "generator": "Antigravity CAD 3D Compiler - Pines 48 Petah Tikva"},
        "scene": 0,
        "scenes": [{"name": "Pines_48_Petah_Tikva_Full_BIM", "nodes": list(range(len(nodes)))}],
        "nodes": nodes,
        "meshes": meshes,
        "materials": gltf_materials,
        "accessors": accessors,
        "bufferViews": buffer_views,
        "buffers": [{"byteLength": len(bin_chunks)}],
    }

    json_bytes = json.dumps(gltf_dict, separators=(",", ":")).encode("utf-8")
    while len(json_bytes) % 4 != 0:
        json_bytes += b" "

    total_len = 12 + 8 + len(json_bytes) + 8 + len(bin_chunks)
    with open(glb_path, "wb") as f:
        f.write(struct.pack("<III", 0x46546C67, 2, total_len))
        f.write(struct.pack("<II", len(json_bytes), 0x4E4F534A))
        f.write(json_bytes)
        f.write(struct.pack("<II", len(bin_chunks), 0x004E4942))
        f.write(bin_chunks)

obj_path = os.path.join(OUT_DIR, "pines48_model.obj")
mtl_path = os.path.join(OUT_DIR, "pines48_model.mtl")
glb_path = os.path.join(OUT_DIR, "pines48_model.glb")
json_path = os.path.join(OUT_DIR, "pines48_geometry.json")

export_obj_and_mtl(scene, obj_path, mtl_path)
export_glb(scene, glb_path)

compact_data = {
    "project": {
        "title_he": "פינס 48, פתח תקוה",
        "title_en": "Pines 48, Petah Tikva",
        "architect_he": "נחומי אדריכלים בע\"מ (Nachumi Architects Ltd.)",
        "developer_he": "יצחק קדלסקי חברה לבניה והשקעות בע\"מ",
        "scale": "1:50",
    },
    "materials": scene.materials,
    "meshes": [
        {
            "layer": grp["layer"],
            "material": grp["material"],
            "positions": grp["positions"],
            "normals": grp["normals"],
            "indices": grp["indices"],
        }
        for grp in scene.groups.values() if grp["indices"]
    ]
}

with open(json_path, "w", encoding="utf-8") as jf:
    json.dump(compact_data, jf, ensure_ascii=False, separators=(",", ":"))

total_verts = sum(len(g["positions"]) // 3 for g in scene.groups.values())
total_tris = sum(len(g["indices"]) // 3 for g in scene.groups.values())
print(f"Successfully generated Full Exterior + Interior Pines 48 3D CAD Model:")
print(f"  Total Meshes:    {len(compact_data['meshes'])}")
print(f"  Total Vertices:  {total_verts:,}")
print(f"  Total Triangles: {total_tris:,}")
