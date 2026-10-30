import zipfile, re, math
from shapely.geometry import LineString, MultiLineString, Polygon, box, Point
from shapely.ops import polygonize, unary_union
from shapely import snap
from test_xps_extractor import parse_xps_subpaths, PLANS_ANCHORS, DWF_PER_M, fpage, all_paths

for pname, (ax, ay) in PLANS_ANCHORS.items():
    thick_segs = []
    thin_segs = []
    fill_polys = []
    for attr in all_paths:
        m_d = re.search(r'Data="M([-+]?\d*\.?\d+),([-+]?\d*\.?\d+)', attr)
        if not m_d: continue
        x_init = float(m_d.group(1)) / DWF_PER_M - ax
        y_init = float(m_d.group(2)) / DWF_PER_M - ay
        if not (-22.0 <= x_init <= 22.0 and -20.0 <= y_init <= 21.0):
            continue
        mf = re.search(r'Fill="([^"]+)"', attr)
        ms = re.search(r'Stroke="([^"]+)"', attr)
        mt = re.search(r'StrokeThickness="([^"]+)"', attr)
        fc = mf.group(1).upper() if mf else None
        sc = ms.group(1).upper() if ms else None
        th = mt.group(1) if mt else None
        d_full = re.search(r'Data="([^"]+)"', attr).group(1)
        if fc in ('#1C14FF', '#FF0000', '#FB2323') and 'a5,5' not in d_full and 'a4,4' not in d_full:
            for sp in parse_xps_subpaths(d_full, ax, ay):
                if len(sp) >= 3:
                    p = Polygon(sp).buffer(0)
                    if not p.is_empty and 0.0005 < p.area < 40.0:
                        fill_polys.append(p)
        elif sc == '#000000' and (th in ('19', '33') or (pname in ('floor_9_roof', 'upper_roof') and th == '12')):
            for sp in parse_xps_subpaths(d_full, ax, ay):
                if len(sp) >= 6 and max((math.hypot(sp[j+1][0]-sp[j][0], sp[j+1][1]-sp[j][1]) for j in range(len(sp)-1)), default=0) < 0.22:
                    continue
                for j in range(len(sp) - 1):
                    p1, p2 = sp[j], sp[j+1]
                    L = math.hypot(p2[0]-p1[0], p2[1]-p1[1])
                    if L >= 0.04 and -20.8 <= p1[0] <= 20.8 and -18.5 <= p1[1] <= 20.5:
                        thick_segs.append(LineString([p1, p2]))

    h_segs, v_segs = [], []
    for l in thick_segs:
        (x1, y1), (x2, y2) = l.coords[0], l.coords[-1]
        if abs(y1 - y2) < 0.015 and abs(x2 - x1) >= 0.05:
            h_segs.append((0.5*(y1+y2), min(x1,x2), max(x1,x2)))
        elif abs(x1 - x2) < 0.015 and abs(y2 - y1) >= 0.05:
            v_segs.append((0.5*(x1+x2), min(y1,y2), max(y1,y2)))

    max_thk = 0.42 if 'basement' in pname else 0.32
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

    mls = MultiLineString(thick_segs)
    noded = unary_union(snap(mls, mls, 0.02))
    polys = [p for p in polygonize(noded) if 0.01 <= p.area < 25.0 and p.buffer(-0.24).is_empty]
    u_walls = unary_union(polys + pair_boxes + fill_polys).buffer(0.005, join_style=2).buffer(-0.005, join_style=2).simplify(0.002, preserve_topology=True)
    geoms = list(u_walls.geoms) if hasattr(u_walls, 'geoms') else ([u_walls] if not u_walls.is_empty else [])
    geoms = [g for g in geoms if g.area >= 0.02]
    print(f"{pname:14s}: merged_walls={len(geoms):3d}, total_wall_area={u_walls.area:6.2f} m2, bounds={[round(x,2) for x in u_walls.bounds] if not u_walls.is_empty else []}")
