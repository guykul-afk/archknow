# -*- coding: utf-8 -*-
import json
from shapely.geometry import Polygon
from shapely.ops import unary_union

with open(r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה\data\sharett_extracted_plans.json", "r", encoding="utf-8") as f:
    plans = json.load(f)

def get_fp(y_s):
    return Polygon([
        (-3.17, -13.24), (-16.87, -13.24), (-16.87, -2.99), (-15.34, -2.99),
        (-15.34,  3.40), (-16.87,  3.40), (-16.87,   y_s), ( -3.17,   y_s),
        (-3.17,   3.82), (  2.93,  3.82), (  2.93,   y_s), ( 16.63,   y_s),
        (16.63,   3.40), ( 15.10,  3.40), ( 15.10, -2.99), ( 16.63, -2.99),
        (16.63, -13.24), (  2.93, -13.24), ( 2.93, -3.42), ( -3.17, -3.42)
    ])

for pname, ys in [("floors_345", 13.65), ("floor_8", 12.15)]:
    fp = get_fp(ys)
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
    print(f"=== {pname} ALL ROOMS ===")
    r_list = list(rooms_geom.geoms) if hasattr(rooms_geom, "geoms") else [rooms_geom]
    r_list = [r for r in r_list if r.area >= 2.5]
    r_list.sort(key=lambda r: (round(r.centroid.y, 1), round(r.centroid.x, 1)))
    for r in r_list:
        b = r.bounds
        print(f"  area={r.area:5.1f}m2  X[{b[0]:6.2f}..{b[2]:6.2f}] Y[{b[1]:6.2f}..{b[3]:6.2f}]  ctr=({0.5*(b[0]+b[2]):6.2f}, {0.5*(b[1]+b[3]):6.2f})  sz=({b[2]-b[0]:4.2f}x{b[3]-b[1]:4.2f})")
