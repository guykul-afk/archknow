import re, math
from test_xps_extractor import parse_xps_subpaths, PLANS_ANCHORS, DWF_PER_M, all_paths
from shapely.geometry import Polygon, LineString

for pname in ["upper_roof", "floor_9_roof", "floor_8", "floors_1267", "floors_345", "gallery", "ground"]:
    ax, ay = PLANS_ANCHORS[pname]
    h_walls = []
    v_walls = []
    blue_polys = []
    for attr in all_paths:
        m_d = re.search(r'Data="M([-+]?\d*\.?\d+),([-+]?\d*\.?\d+)', attr)
        if not m_d: continue
        x_init = float(m_d.group(1)) / DWF_PER_M - ax
        y_init = float(m_d.group(2)) / DWF_PER_M - ay
        if not (-20.0 <= x_init <= 20.0 and -18.0 <= y_init <= 18.0): continue
        mf = re.search(r'Fill="([^"]+)"', attr)
        ms = re.search(r'Stroke="([^"]+)"', attr)
        mt = re.search(r'StrokeThickness="([^"]+)"', attr)
        fc = mf.group(1).upper() if mf else None
        sc = ms.group(1).upper() if ms else None
        th = mt.group(1) if mt else None
        d_full = re.search(r'Data="([^"]+)"', attr).group(1)
        if fc in ('#0051FF', '#1C14FF', '#FF0000', '#FB2323'):
            for sp in parse_xps_subpaths(d_full, ax, ay):
                if len(sp) >= 3:
                    p = Polygon(sp).buffer(0)
                    if not p.is_empty and p.area > 0.005:
                        blue_polys.append((fc, [round(v, 2) for v in p.bounds]))
        if sc == '#000000' and th == '19':
            for sp in parse_xps_subpaths(d_full, ax, ay):
                for j in range(len(sp)-1):
                    (x1,y1), (x2,y2) = sp[j], sp[j+1]
                    if abs(y1-y2) < 0.02 and abs(x2-x1) > 0.15:
                        h_walls.append((round(0.5*(y1+y2), 2), round(min(x1,x2), 2), round(max(x1,x2), 2)))
                    elif abs(x1-x2) < 0.02 and abs(y2-y1) > 0.15:
                        v_walls.append((round(0.5*(x1+x2), 2), round(min(y1,y2), 2), round(max(y1,y2), 2)))
    print(f"================ {pname} ================")
    if pname in ("upper_roof", "floor_9_roof"):
        print("  Filled polys:", blue_polys)
        print("  H-walls(19):", sorted(set(h_walls)))
        print("  V-walls(19):", sorted(set(v_walls)))
    else:
        # Print exterior H-walls (near y = -13.24, y = +13.65, y = +11.3..12.3) and V-walls (near x = -16.87, -3.17, +2.93, +16.63)
        ext_h = [w for w in set(h_walls) if w[0] <= -12.5 or w[0] >= 10.5 or (-0.5 <= w[0] <= 5.0 and -3.5 <= w[1] and w[2] <= 3.5)]
        ext_v = [w for w in set(v_walls) if w[0] <= -16.0 or w[0] >= 15.8 or (-3.6 <= w[0] <= 3.4)]
        print("  Ext H-walls(19):", sorted(ext_h))
        print("  Ext V-walls(19):", sorted(ext_v))
