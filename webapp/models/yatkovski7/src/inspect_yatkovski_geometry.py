import os
import sys
import json
from shapely.geometry import LineString, Polygon, MultiLineString, box
from shapely.ops import polygonize, unary_union
from shapely import snap

sys.stdout.reconfigure(encoding='utf-8')

scratch_dir = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch"
with open(os.path.join(scratch_dir, "dwg_frames_and_data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)
with open(os.path.join(scratch_dir, "all_texts_fixed.json"), "r", encoding="utf-8") as f:
    texts = json.load(f)

# Common anchor (ax, ay) = Center of inner elevator shaft (1.90m x 1.65m) in each plan:
# Note: in CAD, +X is East, +Y is North (Yatkovski St is at larger Y, e.g. -76000, while South garden is at -79000).
# If we use:
#   x_m = (cad_x - ax) / 100.0   (+x = East, -x = West)
#   y_m = -(cad_y - ay) / 100.0  (-y = North toward Yatkovski St, +y = South toward Rear Garden)
PLANS_ANCHORS = {
    "basement":   (  1013.29, -76113.86),
    "ground":     ( -2352.16, -77276.82),
    "floor_1":    ( -6064.08, -77254.11),
    "floor_2":    ( -8727.65, -77254.11),
    "floors_3_4": (-11342.74, -77254.11),
    "floor_5":    (-14017.36, -77254.11),
    "floor_6":    (-16700.74, -77254.11),
    "roofs":      (-19350.92, -77254.11),
    "upper_roof": (-21975.32, -77254.11),
}

for pname, (ax, ay) in PLANS_ANCHORS.items():
    # Collect lines & lwpolys in layers '8' (concrete) and '4' (walls) within [-12m..+12m] in X and [-15m..+20m] in Y
    segs8 = []
    segs4 = []
    for layer, target in [('8', segs8), ('4', segs4)]:
        for p in data['lwpolys_by_layer'].get(layer, []):
            pts = [((x - ax)/100.0, -(y - ay)/100.0) for x, y in p]
            for i in range(len(pts) - 1):
                if -12.5 <= pts[i][0] <= 12.5 and -14.0 <= pts[i][1] <= 20.0:
                    target.append((pts[i], pts[i+1]))
        for l in data['lines_by_layer'].get(layer, []):
            p1 = ((l[0] - ax)/100.0, -(l[1] - ay)/100.0)
            p2 = ((l[2] - ax)/100.0, -(l[3] - ay)/100.0)
            if -12.5 <= p1[0] <= 12.5 and -14.0 <= p1[1] <= 20.0 and -12.5 <= p2[0] <= 12.5 and -14.0 <= p2[1] <= 20.0:
                target.append((p1, p2))
    all_xs = [p[0] for s in segs8 + segs4 for p in s]
    all_ys = [p[1] for s in segs8 + segs4 for p in s]
    # Also find door/window inserts in this plan
    plan_ins = []
    for ins in data['inserts']:
        ix = (ins['x'] - ax) / 100.0
        iy = -(ins['y'] - ay) / 100.0
        if -12.5 <= ix <= 12.5 and -14.0 <= iy <= 20.0:
            if ins['layer'] in ('4', '8', 'rehut', 'FURN', 'SANIT', '2', 'PARK', '1-solar'):
                plan_ins.append((ins['block'], ins['layer'], round(ix, 2), round(iy, 2), round(ins['rot'], 1)))
    print(f"{pname:12s}: segs8={len(segs8):4d}, segs4={len(segs4):4d} | X=[{min(all_xs) if all_xs else 0:6.2f}, {max(all_xs) if all_xs else 0:6.2f}], Y=[{min(all_ys) if all_ys else 0:6.2f}, {max(all_ys) if all_ys else 0:6.2f}] | inserts={len(plan_ins)}")
    # Print door/window inserts on layer 4
    dw_ins = [x for x in plan_ins if x[1] == '4' and x[0].lower().startswith(('d', 'w', 'm17'))]
    print(f"   Door/Win inserts ({len(dw_ins)}): {dw_ins[:15]}")
