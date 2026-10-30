import re
from test_xps_extractor import parse_xps_subpaths, PLANS_ANCHORS, DWF_PER_M, all_paths

for pname in ["floor_9_roof", "upper_roof"]:
    ax, ay = PLANS_ANCHORS[pname]
    rects = []
    for attr in all_paths:
        m_d = re.search(r'Data="M([-+]?\d*\.?\d+),([-+]?\d*\.?\d+)', attr)
        if not m_d: continue
        x_init = float(m_d.group(1)) / DWF_PER_M - ax
        y_init = float(m_d.group(2)) / DWF_PER_M - ay
        if not (-18.0 <= x_init <= 18.0 and -16.0 <= y_init <= 16.0): continue
        mf = re.search(r'Fill="([^"]+)"', attr)
        fc = mf.group(1).upper() if mf else None
        if fc == '#000000':
            d_full = re.search(r'Data="([^"]+)"', attr).group(1)
            for sp in parse_xps_subpaths(d_full, ax, ay):
                xs = [p[0] for p in sp]
                ys = [p[1] for p in sp]
                x0, y0, x1, y1 = round(min(xs),2), round(min(ys),2), round(max(xs),2), round(max(ys),2)
                if (x1 - x0 > 1.5 or y1 - y0 > 1.5) and -17.5 <= x0 and x1 <= 17.5 and -15.5 <= y0 and y1 <= 15.5:
                    rects.append((x0, y0, x1, y1))
    print(f"=== {pname} Fill=#000000 long rects ({len(rects)}) ===")
    for r in sorted(set(rects)):
        print(" ", r)
