import re
from test_xps_extractor import parse_xps_subpaths, PLANS_ANCHORS, DWF_PER_M, all_paths

ax, ay = PLANS_ANCHORS["floor_9_roof"]
for attr in all_paths:
    ms = re.search(r'Stroke="([^"]+)"', attr)
    mt = re.search(r'StrokeThickness="([^"]+)"', attr)
    sc = ms.group(1).upper() if ms else None
    th = mt.group(1) if mt else None
    if sc == '#000000' and th in ('7', '9'):
        d_full = re.search(r'Data="([^"]+)"', attr).group(1)
        for sp in parse_xps_subpaths(d_full, ax, ay):
            if len(sp) >= 4 and -17.5 <= sp[0][0] <= 17.5 and -16.0 <= sp[0][1] <= 16.0:
                pts = [(round(x, 2), round(y, 2)) for x, y in sp]
                print(f"th={th} len={len(pts)}:", pts)
