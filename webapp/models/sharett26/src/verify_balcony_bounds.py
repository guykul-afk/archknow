import re
from test_xps_extractor import parse_xps_subpaths, PLANS_ANCHORS, DWF_PER_M, all_paths

for pname in ["floors_1267", "floors_345", "floor_8", "floor_9_roof"]:
    ax, ay = PLANS_ANCHORS[pname]
    n_lines, s_lines = [], []
    for attr in all_paths:
        m_d = re.search(r'Data="M([-+]?\d*\.?\d+),([-+]?\d*\.?\d+)', attr)
        if not m_d: continue
        x_init = float(m_d.group(1)) / DWF_PER_M - ax
        y_init = float(m_d.group(2)) / DWF_PER_M - ay
        if not (-20.0 <= x_init <= 20.0 and -18.0 <= y_init <= 18.0): continue
        ms = re.search(r'Stroke="([^"]+)"', attr)
        mt = re.search(r'StrokeThickness="([^"]+)"', attr)
        sc = ms.group(1).upper() if ms else None
        th = mt.group(1) if mt else None
        if sc == '#000000' and th in ('12', '19'):
            d_full = re.search(r'Data="([^"]+)"', attr).group(1)
            for sp in parse_xps_subpaths(d_full, ax, ay):
                for j in range(len(sp)-1):
                    (x1,y1), (x2,y2) = sp[j], sp[j+1]
                    if max(y1,y2) <= -13.20 and (abs(x2-x1) > 0.5 or abs(y2-y1) > 0.5):
                        n_lines.append((round(min(x1,x2),2), round(min(y1,y2),2), round(max(x1,x2),2), round(max(y1,y2),2)))
                    if min(y1,y2) >= 12.10 and (abs(x2-x1) > 0.5 or abs(y2-y1) > 0.5):
                        s_lines.append((round(min(x1,x2),2), round(min(y1,y2),2), round(max(x1,x2),2), round(max(y1,y2),2)))
    print(f"=== {pname} ===")
    print("  North (< -13.20):", sorted(set(n_lines)))
    print("  South (> +12.10):", sorted(set(s_lines)))
