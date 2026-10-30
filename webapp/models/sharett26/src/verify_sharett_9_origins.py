import zipfile, re

DWF_PER_M = 472.4409448818898
PT_PER_M = 28.3464567

dwfx_path = r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה\6.5.26-hagasha.dwfx"
with zipfile.ZipFile(dwfx_path, 'r') as z:
    fpage = z.read("dwf/documents/20557152-C9F2-4F2A-83D0-E6D25FE4C692/sections/com.autodesk.dwf.ePlot_20557153-C9F2-4F2A-83D0-E6D25FE4C692/FixedPage.fpage").decode('utf-8', errors='replace')

def parse_svg_path_pts(d_str):
    tokens = re.findall(r'[A-Za-z]|[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', d_str)
    cx, cy = 0.0, 0.0
    sx, sy = 0.0, 0.0
    pts = []
    i = 0
    cmd = None
    n = len(tokens)
    while i < n:
        t = tokens[i]
        if t[0].isalpha():
            cmd = t
            i += 1
            if cmd in ('Z', 'z'):
                cx, cy = sx, sy
            continue
        if cmd == 'M' and i + 1 < n:
            cx, cy = float(tokens[i]), float(tokens[i+1])
            sx, sy = cx, cy
            pts.append((cx / DWF_PER_M, cy / DWF_PER_M))
            i += 2
            cmd = 'L'
        elif cmd == 'm' and i + 1 < n:
            cx += float(tokens[i]); cy += float(tokens[i+1])
            sx, sy = cx, cy
            pts.append((cx / DWF_PER_M, cy / DWF_PER_M))
            i += 2
            cmd = 'l'
        elif cmd == 'L' and i + 1 < n:
            cx, cy = float(tokens[i]), float(tokens[i+1])
            pts.append((cx / DWF_PER_M, cy / DWF_PER_M))
            i += 2
        elif cmd == 'l' and i + 1 < n:
            cx += float(tokens[i]); cy += float(tokens[i+1])
            pts.append((cx / DWF_PER_M, cy / DWF_PER_M))
            i += 2
        elif cmd == 'H' and i < n:
            cx = float(tokens[i])
            pts.append((cx / DWF_PER_M, cy / DWF_PER_M))
            i += 1
        elif cmd == 'h' and i < n:
            cx += float(tokens[i])
            pts.append((cx / DWF_PER_M, cy / DWF_PER_M))
            i += 1
        elif cmd == 'V' and i < n:
            cy = float(tokens[i])
            pts.append((cx / DWF_PER_M, cy / DWF_PER_M))
            i += 1
        elif cmd == 'v' and i < n:
            cy += float(tokens[i])
            pts.append((cx / DWF_PER_M, cy / DWF_PER_M))
            i += 1
        elif cmd == 'C' and i + 5 < n:
            cx, cy = float(tokens[i+4]), float(tokens[i+5])
            pts.append((cx / DWF_PER_M, cy / DWF_PER_M))
            i += 6
        elif cmd == 'c' and i + 5 < n:
            cx += float(tokens[i+4]); cy += float(tokens[i+5])
            pts.append((cx / DWF_PER_M, cy / DWF_PER_M))
            i += 6
        else:
            i += 1
    return pts

# Notice in FixedPage.fpage:
# floors_1267: Blue X=[259.442..292.963], Y=[11.790..40.454], AllWall Y=[11.322..40.454]
# floors_345 : AllWall X=[210.610..244.371], Y=[11.320..40.454]
# floor_8    : Blue X=[161.571..195.076], Y=[11.790..37.203], AllWall Y=[11.320..38.811]
# gallery    : Blue X=[315.836..349.349], Y=[11.822..38.716], AllWall Y=[11.322..38.811]
# Wait! Look at the Y coordinates of gallery, floors_1267, floors_345, floor_8:
# Gallery, floors_1267, floors_345, floor_8 ALL have top North wall at Y = 11.322m (or 11.790m for blue core)!
# Let's check floor_9_roof (x in 104..154m) and upper_roof (x in 56..106m) for all paths (fills & strokes)!

all_paths = re.findall(r'<Path([^>]+)/>', fpage)
print("Total paths:", len(all_paths))

for pname, (wx0, wy0, wx1, wy1) in [
    ("floor_9_roof", (2950/PT_PER_M, 50/PT_PER_M, 4350/PT_PER_M, 1350/PT_PER_M)),
    ("upper_roof",   (1600/PT_PER_M, 50/PT_PER_M, 3000/PT_PER_M, 1350/PT_PER_M)),
]:
    cols = {}
    for attr in all_paths:
        m_d = re.search(r'Data="([^"]+)"', attr)
        if not m_d: continue
        pts = parse_svg_path_pts(m_d.group(1))
        if not pts: continue
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        if wx0 <= x0 and x1 <= wx1 and wy0 <= y0 and y1 <= wy1:
            if (x1 - x0) > 42.0 or (y1 - y0) > 40.0: continue
            m_f = re.search(r'Fill="(#[0-9A-Fa-f]+)"', attr)
            m_s = re.search(r'Stroke="(#[0-9A-Fa-f]+)"', attr)
            key = ("F:" + m_f.group(1)) if m_f else (("S:" + m_s.group(1)) if m_s else "other")
            if key not in cols:
                cols[key] = [x0, x1, y0, y1, 1]
            else:
                cols[key][0] = min(cols[key][0], x0)
                cols[key][1] = max(cols[key][1], x1)
                cols[key][2] = min(cols[key][2], y0)
                cols[key][3] = max(cols[key][3], y1)
                cols[key][4] += 1
    print(f"=== {pname} ===")
    for k, v in sorted(cols.items(), key=lambda x: -x[1][4]):
        print(f"  {k:14s}: count={v[4]:4d}, X=[{v[0]:.3f}..{v[1]:.3f}] (W={v[1]-v[0]:.3f}m), Y=[{v[2]:.3f}..{v[3]:.3f}] (H={v[3]-v[2]:.3f}m)")
