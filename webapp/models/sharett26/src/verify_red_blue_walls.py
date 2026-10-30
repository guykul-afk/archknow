import re
from test_xps_extractor import parse_xps_subpaths, PLANS_ANCHORS, DWF_PER_M, all_paths

ax, ay = PLANS_ANCHORS["floors_1267"]
h_w, v_w = [], []
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
    if sc == '#000000' and th == '19':
        d_full = re.search(r'Data="([^"]+)"', attr).group(1)
        for sp in parse_xps_subpaths(d_full, ax, ay):
            for j in range(len(sp)-1):
                (x1,y1), (x2,y2) = sp[j], sp[j+1]
                if -4.5 <= min(y1,y2) and max(y1,y2) <= 4.8:
                    if abs(y1-y2) < 0.02 and abs(x2-x1) > 0.2:
                        h_w.append((round(0.5*(y1+y2),2), round(min(x1,x2),2), round(max(x1,x2),2)))
                    elif abs(x1-x2) < 0.02 and abs(y2-y1) > 0.2:
                        v_w.append((round(0.5*(x1+x2),2), round(min(y1,y2),2), round(max(y1,y2),2)))
print("H-walls in Y=[-4.5..4.8]:", sorted(set(h_w)))
print("V-walls in Y=[-4.5..4.8]:", sorted(set(v_w)))
