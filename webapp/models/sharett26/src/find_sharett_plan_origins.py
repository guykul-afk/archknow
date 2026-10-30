import zipfile, re

DWF_PER_M = 472.4409448818898  # 1m at 1:100 = 472.44094488 DWF units

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

PT_PER_M = 28.3464567
PLAN_WINDOWS = {
    "basement_2":   (12100/PT_PER_M,  50/PT_PER_M, 13650/PT_PER_M, 1350/PT_PER_M),
    "basement_1":   (12100/PT_PER_M, 1350/PT_PER_M, 13650/PT_PER_M, 2780/PT_PER_M),
    "ground":       (10200/PT_PER_M,   50/PT_PER_M, 12150/PT_PER_M, 1450/PT_PER_M),
    "gallery":      ( 8650/PT_PER_M,  50/PT_PER_M, 10200/PT_PER_M, 1400/PT_PER_M),
    "floors_1267":  ( 7100/PT_PER_M,  50/PT_PER_M,  8650/PT_PER_M, 1350/PT_PER_M),
    "floors_345":   ( 5700/PT_PER_M,  50/PT_PER_M,  7150/PT_PER_M, 1350/PT_PER_M),
    "floor_8":      ( 4300/PT_PER_M,  50/PT_PER_M,  5750/PT_PER_M, 1350/PT_PER_M),
    "floor_9_roof": ( 2950/PT_PER_M,  50/PT_PER_M,  4350/PT_PER_M, 1350/PT_PER_M),
    "upper_roof":   ( 1600/PT_PER_M,  50/PT_PER_M,  3000/PT_PER_M, 1350/PT_PER_M),
}

wall_paths = re.findall(r'<Path[^>]*Fill="(#[0-9A-Fa-f]+)"[^>]*Data="([^"]+)"', fpage)

for pname, (wx0, wy0, wx1, wy1) in PLAN_WINDOWS.items():
    blue_xs, blue_ys = [], []
    red_xs, red_ys = [], []
    for fill_col, d_str in wall_paths:
        if fill_col not in ('#1C14FF', '#FF0000', '#FB2323', '#F90606'):
            continue
        pts = parse_svg_path_pts(d_str)
        if not pts:
            continue
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        if wx0 <= x0 and x1 <= wx1 and wy0 <= y0 and y1 <= wy1:
            if (x1 - x0) > 42.0 or (y1 - y0) > 40.0:
                continue
            if fill_col == '#1C14FF':
                blue_xs.extend([x0, x1]); blue_ys.extend([y0, y1])
            else:
                red_xs.extend([x0, x1]); red_ys.extend([y0, y1])
    if blue_xs:
        bx0, bx1 = min(blue_xs), max(blue_xs)
        by0, by1 = min(blue_ys), max(blue_ys)
        rx0, rx1 = (min(red_xs), max(red_xs)) if red_xs else (bx0, bx1)
        ry0, ry1 = (min(red_ys), max(red_ys)) if red_ys else (by0, by1)
        ax0, ax1 = min(bx0, rx0), max(bx1, rx1)
        ay0, ay1 = min(by0, ry0), max(by1, ry1)
        print(f"{pname:14s}: Blue X=[{bx0:.3f}..{bx1:.3f}] (W={bx1-bx0:.3f}m), Y=[{by0:.3f}..{by1:.3f}] (H={by1-by0:.3f}m) | AllWall X=[{ax0:.3f}..{ax1:.3f}] (W={ax1-ax0:.3f}m), Y=[{ay0:.3f}..{ay1:.3f}] (H={ay1-ay0:.3f}m), Center=({0.5*(ax0+ax1):.3f}, {0.5*(ay0+ay1):.3f})")
