# -*- coding: utf-8 -*-
import re, math, json
from collections import Counter
from shapely.geometry import Polygon, box, Point
from shapely.ops import unary_union
from test_xps_extractor import parse_xps_subpaths, PLANS_ANCHORS, all_paths
from export_sharett_json import get_building_footprint_poly

with open(r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה\data\sharett_extracted_plans.json", "r", encoding="utf-8") as f:
    plans = json.load(f)

for pname in ("floors_345", "floor_8"):
    ax, ay = PLANS_ANCHORS[pname]
    c = Counter()
    for attr in all_paths:
        ms = re.search(r'Stroke="([^"]+)"', attr)
        mt = re.search(r'StrokeThickness="([^"]+)"', attr)
        sc = ms.group(1).upper() if ms else None
        th = mt.group(1) if mt else None
        d_full = re.search(r'Data="([^"]+)"', attr).group(1)
        for sp in parse_xps_subpaths(d_full, ax, ay):
            if sp and -17.0 <= sp[0][0] <= 17.0 and -14.0 <= sp[0][1] <= 14.0:
                c[(sc, th)] += len(sp) - 1
    print(f"=== {pname} stroke (color, thickness) segment counts ===")
    for k, v in c.most_common(12):
        print(f"  {k}: {v}")

    # Reconstruct interior rooms from wall_polys
    fp = get_building_footprint_poly(pname)
    w_polys = []
    for wp in plans[pname]["wall_polys"]:
        ext = wp["exterior"]
        holes = wp.get("holes", [])
        if len(ext) >= 3:
            p = Polygon(ext, holes).buffer(0)
            if not p.is_empty:
                w_polys.append(p)
    u_walls = unary_union(w_polys)
    rooms_geom = fp.buffer(-0.05).difference(u_walls.buffer(0.02))
    print(f"=== {pname} West Wing Rooms (X < 0) ===")
    r_list = list(rooms_geom.geoms) if hasattr(rooms_geom, "geoms") else [rooms_geom]
    r_list = [r for r in r_list if r.area >= 2.0 and r.centroid.x < 0]
    r_list.sort(key=lambda r: (round(r.centroid.y, 1), round(r.centroid.x, 1)))
    for r in r_list:
        b = r.bounds
        print(f"  Room area={r.area:5.1f}m2  bounds=X[{b[0]:6.2f}..{b[2]:6.2f}] Y[{b[1]:6.2f}..{b[3]:6.2f}]  center=({0.5*(b[0]+b[2]):6.2f}, {0.5*(b[1]+b[3]):6.2f})  size=({b[2]-b[0]:4.2f}x{b[3]-b[1]:4.2f})")
