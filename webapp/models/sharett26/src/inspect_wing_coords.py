import zipfile, re, math
from shapely.geometry import LineString, MultiLineString, Polygon, box
from shapely.ops import polygonize, unary_union
from shapely import snap
from test_xps_extractor import parse_xps_subpaths, PLANS_ANCHORS, DWF_PER_M, fpage, all_paths

def get_plan_walls_and_thin(pname):
    ax, ay = PLANS_ANCHORS[pname]
    thick_segs = []
    thin_segs = []
    door_arcs = []
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
        if sc == '#000000' and th in ('12', '7', '9'):
            # Check for door arcs ('a' or 'A' in d_full with radius ~0.6..1.1m = 280..520 DWF units)
            for m_arc in re.finditer(r'M([-+]?\d*\.?\d+),([-+]?\d*\.?\d+)a(\d+),(\d+)\s+[-+]?\d*\.?\d+\s+\d\s+\d\s+([-+]?\d*\.?\d+),([-+]?\d*\.?\d+)', d_full):
                rx_m = float(m_arc.group(3)) / DWF_PER_M
                if 0.55 <= rx_m <= 1.15:
                    ax0 = float(m_arc.group(1)) / DWF_PER_M - ax
                    ay0 = float(m_arc.group(2)) / DWF_PER_M - ay
                    ax1 = ax0 + float(m_arc.group(5)) / DWF_PER_M
                    ay1 = ay0 + float(m_arc.group(6)) / DWF_PER_M
                    if -17.5 <= ax0 <= 17.5 and -15.5 <= ay0 <= 15.5:
                        door_arcs.append(LineString([(ax0, ay0), (ax1, ay1)]))
            for sp in parse_xps_subpaths(d_full, ax, ay):
                if len(sp) >= 6 and max((math.hypot(sp[j+1][0]-sp[j][0], sp[j+1][1]-sp[j][1]) for j in range(len(sp)-1)), default=0) < 0.22:
                    continue
                for j in range(len(sp) - 1):
                    p1, p2 = sp[j], sp[j+1]
                    L = math.hypot(p2[0]-p1[0], p2[1]-p1[1])
                    if 0.05 <= L <= 8.0 and -18.5 <= p1[0] <= 18.5 and -16.5 <= p1[1] <= 16.5:
                        thin_segs.append(LineString([p1, p2]))
    return thick_segs, thin_segs, door_arcs, fill_polys

for pname in ["floors_1267", "floors_345", "floor_8", "ground", "gallery", "floor_9_roof", "upper_roof"]:
    thick_segs, thin_segs, door_arcs, fill_polys = get_plan_walls_and_thin(pname)
    # Print major horizontal and vertical wall coordinates (total length > 3.0m)
    from collections import defaultdict
    h_tot = defaultdict(float)
    v_tot = defaultdict(float)
    for l in thick_segs:
        (x1, y1), (x2, y2) = l.coords[0], l.coords[-1]
        if abs(y1 - y2) < 0.015:
            h_tot[round(0.5*(y1+y2), 2)] += abs(x2 - x1)
        elif abs(x1 - x2) < 0.015:
            v_tot[round(0.5*(x1+x2), 2)] += abs(y2 - y1)
    top_h = sorted([(y, round(L,1)) for y, L in h_tot.items() if L >= 4.0])
    top_v = sorted([(x, round(L,1)) for x, L in v_tot.items() if L >= 4.0])
    print(f"=== {pname} (door_arcs={len(door_arcs)}) ===")
    print("  Major Y (H walls):", top_h)
    print("  Major X (V walls):", top_v)
