import zipfile, re, math, json, os
from shapely.geometry import LineString, MultiLineString, Polygon, box, Point
from shapely.ops import polygonize, unary_union, triangulate
from shapely import snap
from test_xps_extractor import parse_xps_subpaths, PLANS_ANCHORS, DWF_PER_M, fpage, all_paths

OUT_DIR = r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה\data"
os.makedirs(OUT_DIR, exist_ok=True)

def get_building_footprint_poly(pname):
    if "basement" in pname:
        return box(-20.48, -17.71, 20.48, 17.50)
    if pname in ("ground", "gallery"):
        # On Ground & Gallery (+0.00 .. +6.12), the South-West bay X = [-16.87, -15.34], Y = [-2.99, +13.65]
        # is open for the two-lane underground garage ramp (מנסעה לחניון / רמפה דו-סטרית)!
        ring = [
            (-3.17, -13.24), (-16.87, -13.24), (-16.87, -2.99), (-15.34, -2.99),
            (-15.34, 13.65), ( -3.17,  13.65), ( -3.17,  3.82), (  2.93,  3.82),
            (  2.93, 13.65), ( 16.63,  13.65), ( 16.63,  3.40), ( 15.10,  3.40),
            ( 15.10, -2.99), ( 16.63,  -2.99), ( 16.63, -13.24), ( 2.93, -13.24),
            (  2.93, -3.42), ( -3.17,  -3.42)
        ]
        return Polygon(ring)
    y_s = 12.15 if pname in ("floor_8", "floor_9_roof", "upper_roof") else 13.65
    ring = [
        (-3.17, -13.24), (-16.87, -13.24), (-16.87, -2.99), (-15.34, -2.99),
        (-15.34,  3.40), (-16.87,  3.40), (-16.87,   y_s), ( -3.17,   y_s),
        (-3.17,   3.82), (  2.93,  3.82), (  2.93,   y_s), ( 16.63,   y_s),
        (16.63,   3.40), ( 15.10,  3.40), ( 15.10, -2.99), ( 16.63, -2.99),
        (16.63, -13.24), (  2.93, -13.24), ( 2.93, -3.42), ( -3.17, -3.42)
    ]
    return Polygon(ring)

def get_exact_openings_for_plan(pname):
    if pname in ("basement_1", "basement_2", "upper_roof"):
        return []
    if pname == "floor_9_roof":
        return [
            ["V", -9.52, -4.03, -9.28, -2.98, "door"],
            ["V",  9.03, -4.03,  9.28, -2.98, "door"],
        ]

    ops = []
    is_f8 = (pname == "floor_8")
    is_ground = (pname == "ground")
    is_gal = (pname == "gallery")

    # 1. NORTH FACADE (Y = [-13.24, -12.99]) — West Wing & East Wing
    if is_gal:
        n_specs_gal = [
            (-15.84, -14.64, "win_gal"),
            (-11.74, -10.54, "win_gal"),
            ( -9.34,  -8.14, "win_gal"),
            ( -5.24,  -4.04, "win_gal"),
            (  3.80,   5.00, "win_gal"),
            (  7.90,   9.10, "win_gal"),
            ( 10.30,  11.50, "win_gal"),
            ( 14.40,  15.60, "win_gal"),
        ]
        for x0, x1, knd in n_specs_gal:
            ops.append(["H", x0, -13.24, x1, -12.99, knd])
    else:
        n_specs = [
            (-15.84, -14.64, "window"),
            (-13.54, -10.54, "vitrine"),
            ( -9.34,  -6.34, "vitrine"),
            ( -5.24,  -4.04, "window"),
            (  3.80,   5.00, "window"),
            (  6.10,   9.10, "vitrine"),
            ( 10.30,  13.30, "vitrine"),
            ( 14.40,  15.60, "window"),
        ]
        for x0, x1, knd in n_specs:
            ops.append(["H", x0, -13.24, x1, -12.99, knd])

    # 2. CENTRAL BRIDGE NORTH FACE (Y = [-3.42, -3.20]) & SOUTH FACE (Y = [3.60, 3.82])
    for x0, x1 in [(-2.12, -1.12), (0.88, 1.88)]:
        ops.append(["H", x0, -3.42, x1, -3.20, "win_gal" if is_gal else "win_recess"])
        if not is_ground and not is_gal:
            ops.append(["H", x0, 3.60, x1, 3.82, "win_recess"])

    if is_ground or is_gal:
        ops.append(["H", -2.85, 3.60, 2.60, 3.82, "curtain_3bay_dh" if is_ground else "dh_void"])

    # 3. SOUTH FACADE (Y = [11.90, 12.15] on Floor 8; Y = [13.40, 13.65] on Ground..Floor 7)
    if is_f8:
        s_specs_f8 = [
            (-16.05, -13.65, "vitrine"),
            (-13.38, -10.88, "vitrine"),
            ( -9.59,  -8.39, "window"),
            ( -6.49,  -5.29, "window"),
            (  5.05,   6.25, "window"),
            (  8.15,   9.35, "window"),
            ( 10.64,  13.14, "vitrine"),
            ( 13.41,  15.81, "vitrine"),
        ]
        for x0, x1, knd in s_specs_f8:
            ops.append(["H", x0, 11.90, x1, 12.15, knd])
    elif is_ground or is_gal:
        s_specs_base = [
            (-13.30,  -9.90, "gate_louver_dh" if is_ground else "dh_void"),
            ( -9.34,  -6.34, "vitrine_dh"     if is_ground else "dh_void"),
            ( -5.24,  -4.04, "vitrine_dh"     if is_ground else "dh_void"),
            (  3.80,   5.00, "vitrine_dh"     if is_ground else "dh_void"),
            (  6.10,   9.10, "vitrine_dh"     if is_ground else "dh_void"),
            ( 10.30,  13.30, "vitrine_dh"     if is_ground else "dh_void"),
            ( 14.40,  15.60, "vitrine_dh"     if is_ground else "dh_void"),
        ]
        for x0, x1, knd in s_specs_base:
            ops.append(["H", x0, 13.40, x1, 13.65, knd])
    else:
        s_specs_typ = [
            (-15.84, -14.64, "window"),
            (-13.54, -10.54, "vitrine"),
            ( -9.34,  -6.34, "vitrine"),
            ( -5.24,  -4.04, "window"),
            (  3.80,   5.00, "window"),
            (  6.10,   9.10, "vitrine"),
            ( 10.30,  13.30, "vitrine"),
            ( 14.40,  15.60, "window"),
        ]
        for x0, x1, knd in s_specs_typ:
            ops.append(["H", x0, 13.40, x1, 13.65, knd])

    # 4. OUTER WEST FACADE & OUTER EAST FACADE
    for is_west, wx0, wx1, w_waist0, w_waist1 in [
        (True,  -16.87, -16.62, -15.34, -15.04),
        (False,  16.38,  16.63,  14.80,  15.10)
    ]:
        ops.append(["V", wx0, -12.54, wx1, -11.34, "win_balc"])
        ops.append(["V", wx0, -10.29, wx1,  -9.09, "win_balc"])
        ops.append(["V", wx0,  -8.47, wx1,  -6.46, "louver"])
        ops.append(["V", wx0,  -5.45, wx1,  -4.25, "win_balc"])
        ops.append(["V", w_waist0, -1.77, w_waist1, -0.77, "window"])
        ops.append(["V", w_waist0,  1.18, w_waist1,  2.17, "window"])
        if is_ground or is_gal:
            if not is_west and is_ground:
                ops.append(["V", wx0,  8.00, wx1,  9.00, "door"])
                ops.append(["V", wx0, 10.40, wx1, 11.40, "door"])
        elif is_f8:
            ops.append(["V", wx0, 4.66, wx1,  5.86, "win_balc"])
            ops.append(["V", wx0, 7.57, wx1,  8.77, "louver"])
            ops.append(["V", wx0, 9.60, wx1, 10.80, "win_balc"])
        else:
            ops.append(["V", wx0,  4.66, wx1,  5.86, "win_balc"])
            ops.append(["V", wx0,  6.87, wx1,  8.88, "louver"])
            ops.append(["V", wx0,  9.50, wx1, 10.70, "win_balc"])
            ops.append(["V", wx0, 11.75, wx1, 12.95, "win_balc"])

    # 5. INNER COURTYARD FACADES
    for ix0, ix1 in [(-3.42, -3.17), (2.93, 3.18)]:
        ops.append(["V", ix0, -12.54, ix1, -11.34, "window"])
        ops.append(["V", ix0,  -9.79, ix1,  -8.59, "window"])
        ops.append(["V", ix0,  -7.98, ix1,  -5.87, "louver_Recess"])
        ops.append(["V", ix0,  -5.36, ix1,  -4.36, "win_small"])
        if not (is_ground or is_gal):
            ops.append(["V", ix0,  4.76, ix1,  5.76, "win_small"])
            ops.append(["V", ix0,  6.27, ix1,  8.38, "louver_Recess"])
            ops.append(["V", ix0,  9.00, ix1, 10.20, "window"])
            if not is_f8:
                ops.append(["V", ix0, 11.75, ix1, 12.95, "window"])

    # 6. Interior apartment entrance & room doors (fitted to exact doorway cutouts in interior partitions!)
    if not (is_ground or is_gal):
        door_specs = [
            # West Wing 28 Apartment Entrance Doors from Elevator Lobby
            ("H", -11.15, -7.85, -10.15, -7.65, "door"),
            ("H",  -9.85, -7.85,  -8.85, -7.65, "door"),
            # East Wing 26 Apartment Entrance Doors from Elevator Lobby
            ("H",   8.65, -7.85,   9.65, -7.65, "door"),
            ("H",   9.95, -7.85,  10.95, -7.65, "door"),
            # Bedroom & Bathroom Interior Doors (West Wing 28 & East Wing 26)
            ("V", -13.65, -4.05, -13.45, -3.20, "door"),
            ("V",  -6.65, -2.85,  -6.45, -2.00, "door"),
            ("V",   6.20, -2.85,   6.40, -2.00, "door"),
            ("V",  13.20, -4.05,  13.40, -3.20, "door"),
            ("V", -13.65,  3.50, -13.45,  4.35, "door"),
            ("V",  13.20,  3.50,  13.40,  4.35, "door"),
        ]
        if is_f8:
            # Floor 8 South Penthouse Entrance Doors (#32 West & #33 East)
            door_specs.extend([
                ("H", -9.50, 7.00, -8.50, 7.20, "door"),
                ("H",  8.25, 7.00,  9.25, 7.20, "door"),
            ])
        else:
            # Typical Floors 1..7 South Apartment Entrance Doors
            door_specs.extend([
                ("H", -11.15, 7.00, -10.15, 7.20, "door"),
                ("H",  -9.85, 7.00,  -8.85, 7.20, "door"),
                ("H",   8.65, 7.00,   9.65, 7.20, "door"),
                ("H",   9.95, 7.00,  10.95, 7.20, "door"),
                ("V",  -6.65, 2.20,  -6.45, 3.05, "door"),
                ("V",   6.20, 2.20,   6.40, 3.05, "door"),
            ])
        for d_op in door_specs:
            ops.append(list(d_op))

    return ops

def triangulate_poly(poly):
    pts = []
    pt_idx = {}
    def get_idx(pt):
        key = (round(pt[0], 3), round(pt[1], 3))
        if key not in pt_idx:
            pt_idx[key] = len(pts)
            pts.append([key[0], key[1]])
        return pt_idx[key]

    tris_idx = []
    tris_coords = []
    for tri in triangulate(poly):
        rp = tri.representative_point()
        if poly.contains(rp):
            coords = list(tri.exterior.coords)[:-1]
            if len(coords) == 3:
                c0 = [round(coords[0][0], 3), round(coords[0][1], 3)]
                c1 = [round(coords[1][0], 3), round(coords[1][1], 3)]
                c2 = [round(coords[2][0], 3), round(coords[2][1], 3)]
                i0, i1, i2 = get_idx(c0), get_idx(c1), get_idx(c2)
                if i0 != i1 and i1 != i2 and i2 != i0:
                    tris_idx.append([i0, i1, i2])
                    tris_coords.append([c0, c1, c2])
    ext_ring = [[round(c[0], 3), round(c[1], 3)] for c in list(poly.exterior.coords)[:-1]]
    holes_rings = [
        [[round(c[0], 3), round(c[1], 3)] for c in list(inter.coords)[:-1]]
        for inter in poly.interiors
    ]
    return {
        "pts": pts,
        "tris_idx": tris_idx,
        "tris": tris_coords,
        "exterior": ext_ring,
        "holes": holes_rings
    }

def mirror_segments_symmetrically(segs, is_floor_8=False):
    """
    In the Garmushka CAD, the architect drew 2D furniture only in a subset of apartments
    (e.g. West Wing on floors_345, East Wing on floor_8) because the two wings are symmetric around X = -0.12m!
    Mirroring segments across X = -0.12m guarantees 100% complete, authentic CAD floor drawings in ALL apartments!
    """
    X_SYM = -0.12
    seg_set = set()
    out = []
    def add_seg(x1, y1, x2, y2):
        k1 = (round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2))
        k2 = (round(x2, 2), round(y2, 2), round(x1, 2), round(y1, 2))
        if k1 not in seg_set and k2 not in seg_set:
            seg_set.add(k1)
            out.append([round(x1, 3), round(y1, 3), round(x2, 3), round(y2, 3)])

    for x1, y1, x2, y2 in segs:
        add_seg(x1, y1, x2, y2)
        mx1 = 2.0 * X_SYM - x1
        mx2 = 2.0 * X_SYM - x2
        add_seg(mx1, y1, mx2, y2)
    return out

def extract_plan(pname):
    ax, ay = PLANS_ANCHORS[pname]
    thick_segs = []
    thin_segs = []
    furn_segs = []
    fill_polys = []

    is_bm = "basement" in pname
    fp_poly = get_building_footprint_poly(pname)
    clip_poly = fp_poly.buffer(1.85 if not is_bm else 0.25, join_style=2)
    int_clip_poly = fp_poly.buffer(-0.02, join_style=2)

    x_lim = 21.0 if is_bm else 18.0
    y_lim_min = -18.5 if is_bm else -15.5
    y_lim_max = 18.0 if is_bm else 15.8

    for attr in all_paths:
        mf = re.search(r'Fill="([^"]+)"', attr)
        ms = re.search(r'Stroke="([^"]+)"', attr)
        mt = re.search(r'StrokeThickness="([^"]+)"', attr)
        fc = mf.group(1).upper() if mf else None
        sc = ms.group(1).upper() if ms else None
        th = mt.group(1) if mt else None
        d_full = re.search(r'Data="([^"]+)"', attr).group(1)

        if fc in ('#0051FF', '#1C14FF', '#FF0000', '#FB2323') and 'a5,5' not in d_full and 'a4,4' not in d_full:
            for sp in parse_xps_subpaths(d_full, ax, ay):
                if len(sp) >= 3 and -x_lim <= sp[0][0] <= x_lim and y_lim_min <= sp[0][1] <= y_lim_max:
                    p = Polygon(sp).buffer(0)
                    if not p.is_empty and 0.002 < p.area < 40.0:
                        cx, cy = p.centroid.x, p.centroid.y
                        if -x_lim <= cx <= x_lim and y_lim_min <= cy <= y_lim_max:
                            fill_polys.append(p)
        elif sc == '#000000' and th in ('19', '33'):
            for sp in parse_xps_subpaths(d_full, ax, ay):
                if not sp or not (-x_lim <= sp[0][0] <= x_lim and y_lim_min <= sp[0][1] <= y_lim_max):
                    continue
                if len(sp) >= 6 and max((math.hypot(sp[j+1][0]-sp[j][0], sp[j+1][1]-sp[j][1]) for j in range(len(sp)-1)), default=0) < 0.22:
                    continue
                for j in range(len(sp) - 1):
                    p1, p2 = sp[j], sp[j+1]
                    L = math.hypot(p2[0]-p1[0], p2[1]-p1[1])
                    if L >= 0.04 and -x_lim <= p1[0] <= x_lim and y_lim_min <= p1[1] <= y_lim_max:
                        thick_segs.append(LineString([p1, p2]))

        if sc == '#000000' and th in ('12', '7', '9', '5'):
            for sp in parse_xps_subpaths(d_full, ax, ay):
                if not sp or not (-x_lim <= sp[0][0] <= x_lim and y_lim_min <= sp[0][1] <= y_lim_max):
                    continue
                if len(sp) >= 6 and max((math.hypot(sp[j+1][0]-sp[j][0], sp[j+1][1]-sp[j][1]) for j in range(len(sp)-1)), default=0) < 0.22:
                    continue
                for j in range(len(sp) - 1):
                    p1, p2 = sp[j], sp[j+1]
                    L = math.hypot(p2[0]-p1[0], p2[1]-p1[1])
                    if 0.05 <= L <= 9.0:
                        mid_pt = Point(0.5*(p1[0]+p2[0]), 0.5*(p1[1]+p2[1]))
                        if clip_poly.contains(mid_pt):
                            thin_segs.append(LineString([p1, p2]))
                            if th in ('5', '7') and 0.08 <= L <= 2.6 and int_clip_poly.contains(mid_pt):
                                furn_segs.append([round(p1[0], 3), round(p1[1], 3), round(p2[0], 3), round(p2[1], 3)])

    openings = get_exact_openings_for_plan(pname)

    # Construct exact 3D wall polygons per level
    if pname == "upper_roof":
        u_walls = unary_union([
            box(-12.15, -2.06, -9.30, 0.63).difference(box(-11.95, -1.86, -9.50, 0.43)),
            box(  9.05, -2.06, 11.91, 0.63).difference(box(  9.26, -1.86, 11.70, 0.43))
        ])
    elif pname == "floor_9_roof":
        w_tower = box(-12.15, -4.28, -9.30, 0.63).difference(box(-11.95, -4.08, -9.50, 0.43)).difference(box(-9.55, -4.03, -9.25, -2.98))
        e_tower = box(  9.05, -4.28, 11.91, 0.63).difference(box(  9.26, -4.08, 11.70, 0.43)).difference(box( 9.00, -4.03,  9.30, -2.98))
        u_walls = unary_union([w_tower, e_tower])
    else:
        h_segs, v_segs = [], []
        for l in thick_segs:
            (x1, y1), (x2, y2) = l.coords[0], l.coords[-1]
            if abs(y1 - y2) < 0.015 and abs(x2 - x1) >= 0.05:
                h_segs.append((0.5*(y1+y2), min(x1,x2), max(x1,x2)))
            elif abs(x1 - x2) < 0.015 and abs(y2 - y1) >= 0.05:
                v_segs.append((0.5*(x1+x2), min(y1,y2), max(y1,y2)))

        max_thk = 0.42 if is_bm else 0.32
        pair_boxes = []
        for i in range(len(h_segs)):
            yA, xA0, xA1 = h_segs[i]
            for j in range(i+1, len(h_segs)):
                yB, xB0, xB1 = h_segs[j]
                if 0.08 <= abs(yA - yB) <= max_thk:
                    ox0, ox1 = max(xA0, xB0), min(xA1, xB1)
                    if ox1 - ox0 >= 0.08:
                        ym0, ym1 = min(yA, yB), max(yA, yB)
                        if not any(ym0 + 0.03 < h_segs[k][0] < ym1 - 0.03 and min(ox1, h_segs[k][2]) - max(ox0, h_segs[k][1]) > 0.05 for k in range(len(h_segs))):
                            pair_boxes.append(box(ox0, ym0, ox1, ym1))
        for i in range(len(v_segs)):
            xA, yA0, yA1 = v_segs[i]
            for j in range(i+1, len(v_segs)):
                xB, yB0, yB1 = v_segs[j]
                if 0.08 <= abs(xA - xB) <= max_thk:
                    oy0, oy1 = max(yA0, yB0), min(yA1, yB1)
                    if oy1 - oy0 >= 0.08:
                        xm0, xm1 = min(xA, xB), max(xA, xB)
                        if not any(xm0 + 0.03 < v_segs[k][0] < xm1 - 0.03 and min(oy1, v_segs[k][2]) - max(oy0, v_segs[k][1]) > 0.05 for k in range(len(v_segs))):
                            pair_boxes.append(box(xm0, oy0, xm1, oy1))

        mls = MultiLineString(thick_segs) if thick_segs else MultiLineString()
        noded = unary_union(snap(mls, mls, 0.02)) if not mls.is_empty else MultiLineString()
        polys = [p for p in polygonize(noded) if 0.01 <= p.area < 25.0 and p.buffer(-0.24).is_empty]
        cad_walls = unary_union(polys + pair_boxes + fill_polys).intersection(fp_poly)

        if not is_bm:
            perim_shell = fp_poly.difference(fp_poly.buffer(-0.25, join_style=2))
            core_w = box(-12.15, -4.28, -9.30, 0.63).difference(box(-11.95, -4.08, -9.50, 0.43)).difference(box(-9.55, -2.98, -9.25, 0.43))
            core_e = box(  9.05, -4.28, 11.91, 0.63).difference(box(  9.26, -4.08, 11.70, 0.43)).difference(box( 9.00, -2.98,  9.30, 0.43))
            priv_walls = []
            if pname in ("ground", "gallery", "floors_1267", "floors_345", "floor_8"):
                priv_walls.append(box(-0.22, -3.42, -0.02, -3.15))
            if pname in ("floors_1267", "floors_345", "floor_8"):
                priv_walls.append(box(-10.12, -14.99, -9.92, -13.24))
                priv_walls.append(box(  9.68, -14.99,  9.88, -13.24))
            if pname in ("floors_1267", "floors_345"):
                priv_walls.append(box(-10.12, 13.65, -9.92, 15.40))
                priv_walls.append(box(  9.68, 13.65,  9.88, 15.40))

            combined = unary_union([cad_walls, perim_shell, core_w, core_e] + priv_walls)
            op_cutouts = []
            for op in openings:
                orient, x0, y0, x1, y1, knd = op
                if orient == "H":
                    op_cutouts.append(box(x0, y0 - 0.08, x1, y1 + 0.08))
                else:
                    op_cutouts.append(box(x0 - 0.08, y0, x1 + 0.08, y1))
            if op_cutouts:
                combined = combined.difference(unary_union(op_cutouts))
            u_walls = combined.buffer(0.004, join_style=2).buffer(-0.004, join_style=2).simplify(0.002, preserve_topology=True)
        else:
            u_walls = cad_walls.buffer(0.005, join_style=2).buffer(-0.005, join_style=2).simplify(0.002, preserve_topology=True)

    geoms = list(u_walls.geoms) if hasattr(u_walls, 'geoms') else ([u_walls] if not u_walls.is_empty else [])
    geoms = [g for g in geoms if g.area >= 0.02]

    wall_polys_json = []
    for g in geoms:
        t = triangulate_poly(g)
        if t["tris"]:
            wall_polys_json.append(t)

    cad_lines = []
    for l in (thick_segs + thin_segs):
        (x1, y1), (x2, y2) = l.coords[0], l.coords[-1]
        mid_pt = Point(0.5*(x1+x2), 0.5*(y1+y2))
        if clip_poly.contains(mid_pt):
            cad_lines.append([round(x1, 3), round(y1, 3), round(x2, 3), round(y2, 3)])

    # Mirror furniture & interior CAD lines across X = -0.12m on residential floors so every apartment has 100% complete floor drawings!
    if pname in ("ground", "gallery", "floors_1267", "floors_345", "floor_8"):
        furn_segs = mirror_segments_symmetrically(furn_segs, is_floor_8=(pname == "floor_8"))
        if pname in ("floors_1267", "floors_345", "floor_8"):
            cad_lines = mirror_segments_symmetrically(cad_lines, is_floor_8=(pname == "floor_8"))

    return {
        "wall_polys": wall_polys_json,
        "openings": openings,
        "furn_lines": furn_segs[:3500],
        "cad_lines": cad_lines[:6000],
        "room_labels": get_room_labels_for_plan(pname)
    }

def get_room_labels_for_plan(pname):
    if pname == "basement_2":
        return [
            {"name": "מרתף חניה תחתון (-2)", "dims": "37 חניות (#34–#70)", "x": 0.0, "y": -1.5},
            {"name": "לובי מעליות ב'28", "dims": "מפלס -6.00", "x": -10.7, "y": 1.2},
            {"name": "לובי מעליות ב'26", "dims": "מפלס -6.00", "x": 10.5, "y": 1.2},
            {"name": "רמפת ירידה למרתף -2", "dims": "15% (מערב)", "x": -18.0, "y": -2.0},
            {"name": "מאגר מים ומשאבות", "dims": "580×420", "x": -15.0, "y": -14.0},
        ]
    if pname == "basement_1":
        return [
            {"name": "מרתף חניה עליון (-1)", "dims": "33 חניות (#1–#33)", "x": 0.0, "y": -1.5},
            {"name": "לובי מעליות ב'28", "dims": "מפלס -3.00", "x": -10.7, "y": 1.2},
            {"name": "לובי מעליות ב'26", "dims": "מפלס -3.00", "x": 10.5, "y": 1.2},
            {"name": "מנסעה דו-סטרית לחניון", "dims": "7.5%-15% (מערב)", "x": -17.7, "y": 6.5},
            {"name": "חדר טראפו חח\"י", "dims": "540×380", "x": 13.5, "y": 13.5},
        ]
    if pname == "ground":
        return [
            {"name": "חלל כפול לובי ראשי ב'28", "dims": "0.00± גובה 6.12 מ'", "x": -7.5, "y": 9.5},
            {"name": "חלל כפול לובי ראשי ב'26", "dims": "0.00± גובה 6.12 מ'", "x": 7.5, "y": 9.5},
            {"name": "דופלקס גן #1 (ב'28)", "dims": "108.5 מ\"ר + גינה פרטית", "x": -13.5, "y": -10.5},
            {"name": "דופלקס גן #2 (ב'28)", "dims": "102 מ\"ר + גינה פרטית", "x": -6.8, "y": -10.5},
            {"name": "דופלקס גן #3 (ב'26)", "dims": "102 מ\"ר + גינה פרטית", "x": 6.6, "y": -10.5},
            {"name": "דופלקס גן #4 (ב'26)", "dims": "108.5 מ\"ר + גינה פרטית", "x": 13.3, "y": -10.5},
            {"name": "מנסעה לחניון (רמפה דו-סטרית)", "dims": "כניסה ויציאה מרח׳ משה שרת", "x": -17.7, "y": 9.0},
            {"name": "חדר עגלות ואופניים משותף", "dims": "חלל כפול", "x": 0.0, "y": 1.5},
            {"name": "חלל כפול מועדון דיירים", "dims": "בניין 26", "x": 12.0, "y": 11.2},
        ]
    if pname == "gallery":
        return [
            {"name": "גלריה דופלקס #1 (ב'28)", "dims": "מפלס חדרים +3.10", "x": -13.5, "y": -10.5},
            {"name": "גלריה דופלקס #2 (ב'28)", "dims": "מפלס חדרים +3.10", "x": -6.8, "y": -10.5},
            {"name": "גלריה דופלקס #3 (ב'26)", "dims": "מפלס חדרים +3.10", "x": 6.6, "y": -10.5},
            {"name": "גלריה דופלקס #4 (ב'26)", "dims": "מפלס חדרים +3.10", "x": 13.3, "y": -10.5},
            {"name": "חלל כפול לובי ב'28 (פתוח)", "dims": "גובה כפול 0.00..+6.12", "x": -7.5, "y": 9.5},
            {"name": "חלל כפול לובי ב'26 (פתוח)", "dims": "גובה כפול 0.00..+6.12", "x": 7.5, "y": 9.5},
        ]
    if pname in ("floors_1267", "floors_345"):
        return [
            {"name": "גרעין מדרגות ומעליות ב'28", "dims": "2 מעליות + מדרגות", "x": -10.7, "y": -1.8},
            {"name": "גרעין מדרגות ומעליות ב'26", "dims": "2 מעליות + מדרגות", "x": 10.5, "y": -1.8},
            {"name": "סלון ומטבח צפ'-מערב (ב'28)", "dims": "395×640", "x": -13.4, "y": -10.8},
            {"name": "ממ\"ד צפ'-מערב (ב'28)", "dims": "295×335", "x": -14.8, "y": -4.6},
            {"name": "סלון ומטבח צפ'-פנים (ב'28)", "dims": "380×610", "x": -6.8, "y": -10.8},
            {"name": "ממ\"ד צפ'-פנים (ב'28)", "dims": "295×335", "x": -1.7, "y": -1.5},
            {"name": "סלון ומטבח דר'-מערב (ב'28)", "dims": "415×680", "x": -13.4, "y": 11.2},
            {"name": "ממ\"ד דר'-מערב (ב'28)", "dims": "295×335", "x": -14.8, "y": 5.0},
            {"name": "סלון ומטבח דר'-פנים (ב'28)", "dims": "390×630", "x": -6.8, "y": 11.2},
            {"name": "סלון ומטבח צפ'-פנים (ב'26)", "dims": "380×610", "x": 6.6, "y": -10.8},
            {"name": "סלון ומטבח צפ'-מזרח (ב'26)", "dims": "395×640", "x": 13.2, "y": -10.8},
            {"name": "סלון ומטבח דר'-פנים (ב'26)", "dims": "390×630", "x": 6.6, "y": 11.2},
            {"name": "סלון ומטבח דר'-מזרח (ב'26)", "dims": "415×680", "x": 13.2, "y": 11.2},
            {"name": "מרפסות שמש צפוניות", "dims": "685×175 כל אחת", "x": -10.0, "y": -14.1},
            {"name": "מרפסות שמש דרומיות", "dims": "685×175 כל אחת", "x": -10.0, "y": 14.5},
        ]
    if pname == "floor_8":
        return [
            {"name": "פנטהאוז #32 (בניין 28 מערב)", "dims": "6 חד' · 138 מ\"ר + מרפסת", "x": -12.5, "y": 9.8},
            {"name": "פנטהאוז #33 (בניין 26 מזרח)", "dims": "6 חד' · 138 מ\"ר + מרפסת", "x": 12.3, "y": 9.8},
            {"name": "מרפסת פנטהאוז מערבי (#32)", "dims": "1370×250", "x": -10.0, "y": 13.4},
            {"name": "מרפסת פנטהאוז מזרחי (#33)", "dims": "1370×250", "x": 9.8, "y": 13.4},
            {"name": "דירת 3 חד' צפ'-מערב (ק'8)", "dims": "בניין 28", "x": -13.4, "y": -10.8},
            {"name": "דירת 3 חד' צפ'-פנים (ק'8)", "dims": "בניין 28", "x": -6.8, "y": -10.8},
            {"name": "דירת 3 חד' צפ'-פנים (ק'8)", "dims": "בניין 26", "x": 6.6, "y": -10.8},
            {"name": "דירת 3 חד' צפ'-מזרח (ק'8)", "dims": "בניין 26", "x": 13.2, "y": -10.8},
        ]
    if pname == "floor_9_roof":
        return [
            {"name": "מרפסת גג דשא סינטטי — דירה 32 (ב'28)", "dims": "מפלס +31.32", "x": -10.0, "y": 7.8},
            {"name": "מרפסת גג דשא סינטטי — דירה 33 (ב'26)", "dims": "מפלס +31.32", "x": 9.8, "y": 7.8},
            {"name": "חדר יציאה לגג ב'28", "dims": "+31.32 -> +33.77", "x": -10.7, "y": -1.8},
            {"name": "חדר יציאה לגג ב'26", "dims": "+31.32 -> +33.77", "x": 10.5, "y": -1.8},
            {"name": "גג טכני וקולטי שמש (ב'28)", "dims": "מפלס +31.32 / מעקה +32.37", "x": -10.0, "y": -8.8},
            {"name": "גג טכני וקולטי שמש (ב'26)", "dims": "מפלס +31.32 / מעקה +32.37", "x": 9.8, "y": -8.8},
        ]
    return [
        {"name": "גג עליון (+33.77 / +34.27)", "dims": "חדרי מכונות ומעליות", "x": -10.7, "y": -0.8},
        {"name": "גג עליון (+33.77 / +34.27)", "dims": "חדרי מכונות ומעליות", "x": 10.5, "y": -0.8},
    ]

print("Extracting 9 vector floor plans from 6.5.26-hagasha.dwfx with exact building envelope & complete symmetric 2D furniture...")
plans_data = {}
for pname in PLANS_ANCHORS.keys():
    plans_data[pname] = extract_plan(pname)
    print(f"  {pname:14s}: wall_polys={len(plans_data[pname]['wall_polys']):3d}, openings={len(plans_data[pname]['openings']):2d}, furn_lines={len(plans_data[pname]['furn_lines']):4d}, cad_lines={len(plans_data[pname]['cad_lines']):4d}")

plans_json_path = os.path.join(OUT_DIR, "sharett_extracted_plans.json")
with open(plans_json_path, "w", encoding="utf-8") as f:
    json.dump(plans_data, f, ensure_ascii=False, separators=(",", ":"))
print(f"Saved {plans_json_path} ({os.path.getsize(plans_json_path)/1024:.1f} KB)")
