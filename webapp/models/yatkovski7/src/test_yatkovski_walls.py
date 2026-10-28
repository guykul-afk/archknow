import os
import sys
import json
import math
from shapely.geometry import LineString, MultiLineString, Polygon, Point, box
from shapely.ops import polygonize, unary_union
from shapely import snap

sys.stdout.reconfigure(encoding='utf-8')

scratch_dir = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch"
with open(os.path.join(scratch_dir, "dwg_frames_and_data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

PLANS_ANCHORS = {
    "basement":   (  1013.29, -76113.86),
    "ground":     ( -2352.16, -77276.82),
    "typical":    ( -6064.08, -77254.11), # floor_1..4
    "floor_5":    (-14017.36, -77254.11),
    "penthouse":  (-16700.74, -77254.11), # floor_6
    "roof_main":  (-19350.92, -77254.11), # roofs
}

for pname, (ax, ay) in PLANS_ANCHORS.items():
    wall_lines = []
    for layer in ('8', '4'):
        for p in data['lwpolys_by_layer'].get(layer, []):
            pts = [(round((x - ax)/100.0, 4), round(-(y - ay)/100.0, 4)) for x, y in p]
            for i in range(len(pts) - 1):
                p1, p2 = pts[i], pts[i+1]
                if -11.5 <= p1[0] <= 7.0 and -12.5 <= p1[1] <= 19.5 and -11.5 <= p2[0] <= 7.0 and -12.5 <= p2[1] <= 19.5:
                    if math.hypot(p2[0]-p1[0], p2[1]-p1[1]) >= 0.04:
                        wall_lines.append(LineString([p1, p2]))
        for l in data['lines_by_layer'].get(layer, []):
            p1 = (round((l[0] - ax)/100.0, 4), round(-(l[1] - ay)/100.0, 4))
            p2 = (round((l[2] - ax)/100.0, 4), round(-(l[3] - ay)/100.0, 4))
            if -11.5 <= p1[0] <= 7.0 and -12.5 <= p1[1] <= 19.5 and -11.5 <= p2[0] <= 7.0 and -12.5 <= p2[1] <= 19.5:
                if math.hypot(p2[0]-p1[0], p2[1]-p1[1]) >= 0.04:
                    wall_lines.append(LineString([p1, p2]))

    h_segs, v_segs = [], []
    for l in wall_lines:
        (x1, y1), (x2, y2) = l.coords[0], l.coords[-1]
        if abs(y1 - y2) < 0.015 and abs(x2 - x1) >= 0.05:
            h_segs.append((0.5*(y1+y2), min(x1,x2), max(x1,x2)))
        elif abs(x1 - x2) < 0.015 and abs(y2 - y1) >= 0.05:
            v_segs.append((0.5*(x1+x2), min(y1,y2), max(y1,y2)))

    pair_boxes = []
    for i in range(len(h_segs)):
        yA, xA0, xA1 = h_segs[i]
        for j in range(i+1, len(h_segs)):
            yB, xB0, xB1 = h_segs[j]
            if 0.075 <= abs(yA - yB) <= 0.35:
                ox0, ox1 = max(xA0, xB0), min(xA1, xB1)
                if ox1 - ox0 >= 0.05:
                    ym0, ym1 = min(yA, yB), max(yA, yB)
                    if not any(ym0 + 0.03 < h_segs[k][0] < ym1 - 0.03 and min(ox1, h_segs[k][2]) - max(ox0, h_segs[k][1]) > 0.05 for k in range(len(h_segs))):
                        pair_boxes.append(box(ox0, ym0, ox1, ym1))
    for i in range(len(v_segs)):
        xA, yA0, yA1 = v_segs[i]
        for j in range(i+1, len(v_segs)):
            xB, yB0, yB1 = v_segs[j]
            if 0.075 <= abs(xA - xB) <= 0.35:
                oy0, oy1 = max(yA0, yB0), min(yA1, yB1)
                if oy1 - oy0 >= 0.05:
                    xm0, xm1 = min(xA, xB), max(xA, xB)
                    if not any(xm0 + 0.03 < v_segs[k][0] < xm1 - 0.03 and min(oy1, v_segs[k][2]) - max(oy0, v_segs[k][1]) > 0.05 for k in range(len(v_segs))):
                        pair_boxes.append(box(xm0, oy0, xm1, oy1))

    mls = MultiLineString(wall_lines)
    noded = unary_union(snap(mls, mls, 0.02))
    polys = [p for p in polygonize(noded) if 0.01 <= p.area < 18.0]
    u_walls = unary_union(polys + pair_boxes).buffer(0.003, join_style=2).buffer(-0.003, join_style=2).simplify(0.002, preserve_topology=True)
    final_walls = list(u_walls.geoms) if hasattr(u_walls, 'geoms') else ([u_walls] if not u_walls.is_empty else [])
    print(f"{pname:10s}: wall_lines={len(wall_lines):4d}, pair_boxes={len(pair_boxes):3d}, final_walls={len(final_walls):3d}, total_wall_area={u_walls.area:6.2f} sqm, bounds={[round(b,2) for b in u_walls.bounds]}")
