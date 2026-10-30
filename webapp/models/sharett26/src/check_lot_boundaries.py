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
    i = 0; cmd = None; n = len(tokens)
    while i < n:
        t = tokens[i]
        if t[0].isalpha():
            cmd = t; i += 1
            if cmd in ('Z', 'z'): cx, cy = sx, sy
            continue
        if cmd == 'M' and i + 1 < n:
            cx, cy = float(tokens[i]), float(tokens[i+1]); sx, sy = cx, cy
            pts.append((cx / DWF_PER_M, cy / DWF_PER_M)); i += 2; cmd = 'L'
        elif cmd == 'm' and i + 1 < n:
            cx += float(tokens[i]); cy += float(tokens[i+1]); sx, sy = cx, cy
            pts.append((cx / DWF_PER_M, cy / DWF_PER_M)); i += 2; cmd = 'l'
        elif cmd == 'L' and i + 1 < n:
            cx, cy = float(tokens[i]), float(tokens[i+1])
            pts.append((cx / DWF_PER_M, cy / DWF_PER_M)); i += 2
        elif cmd == 'l' and i + 1 < n:
            cx += float(tokens[i]); cy += float(tokens[i+1])
            pts.append((cx / DWF_PER_M, cy / DWF_PER_M)); i += 2
        elif cmd == 'H' and i < n:
            cx = float(tokens[i]); pts.append((cx / DWF_PER_M, cy / DWF_PER_M)); i += 1
        elif cmd == 'h' and i < n:
            cx += float(tokens[i]); pts.append((cx / DWF_PER_M, cy / DWF_PER_M)); i += 1
        elif cmd == 'V' and i < n:
            cy = float(tokens[i]); pts.append((cx / DWF_PER_M, cy / DWF_PER_M)); i += 1
        elif cmd == 'v' and i < n:
            cy += float(tokens[i]); pts.append((cx / DWF_PER_M, cy / DWF_PER_M)); i += 1
        elif cmd in ('C', 'c') and i + 5 < n:
            if cmd == 'C': cx, cy = float(tokens[i+4]), float(tokens[i+5])
            else: cx += float(tokens[i+4]); cy += float(tokens[i+5])
            pts.append((cx / DWF_PER_M, cy / DWF_PER_M)); i += 6
        else:
            i += 1
    return pts

all_paths = re.findall(r'<Path([^>]+)/>', fpage)
for attr in all_paths:
    m_s = re.search(r'Stroke="(#0051FF)"', attr)
    if not m_s: continue
    m_d = re.search(r'Data="([^"]+)"', attr)
    if not m_d: continue
    pts = parse_svg_path_pts(m_d.group(1))
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    if 38.0 <= (x1 - x0) <= 44.0:
        print(f"Lot boundary #0051FF: X=[{x0:.3f}..{x1:.3f}] (W={x1-x0:.3f}), Y=[{y0:.3f}..{y1:.3f}] (H={y1-y0:.3f}), pts={len(pts)}")
