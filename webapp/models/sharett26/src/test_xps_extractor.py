import zipfile, re, math
from shapely.geometry import LineString, MultiLineString, Polygon, box, Point
from shapely.ops import polygonize, unary_union
from shapely import snap

DWF_PER_M = 472.4409448818898
dwfx_path = r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה\6.5.26-hagasha.dwfx"
with zipfile.ZipFile(dwfx_path, 'r') as z:
    fpage = z.read("dwf/documents/20557152-C9F2-4F2A-83D0-E6D25FE4C692/sections/com.autodesk.dwf.ePlot_20557153-C9F2-4F2A-83D0-E6D25FE4C692/FixedPage.fpage").decode('utf-8', errors='replace')

def parse_xps_subpaths(d_str, ax=0.0, ay=0.0):
    """
    Parses an XPS Path Data string into a list of subpaths, where each subpath is a list of (x_m, y_m) points.
    Handles M, m, L, l, H, h, V, v, C, c, A, a, Z, z.
    """
    tokens = re.findall(r'[A-Za-z]|[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', d_str)
    subpaths = []
    cur = []
    cx, cy = 0.0, 0.0
    sx, sy = 0.0, 0.0
    i = 0
    cmd = None
    n = len(tokens)
    while i < n:
        t = tokens[i]
        if t[0].isalpha():
            cmd = t
            i += 1
            if cmd in ('Z', 'z'):
                if cur:
                    cur.append((round(sx / DWF_PER_M - ax, 4), round(sy / DWF_PER_M - ay, 4)))
                cx, cy = sx, sy
            continue
        if cmd == 'M' and i + 1 < n:
            if cur: subpaths.append(cur)
            cx, cy = float(tokens[i]), float(tokens[i+1])
            sx, sy = cx, cy
            cur = [(round(cx / DWF_PER_M - ax, 4), round(cy / DWF_PER_M - ay, 4))]
            i += 2
            cmd = 'L'
        elif cmd == 'm' and i + 1 < n:
            if cur: subpaths.append(cur)
            cx += float(tokens[i]); cy += float(tokens[i+1])
            sx, sy = cx, cy
            cur = [(round(cx / DWF_PER_M - ax, 4), round(cy / DWF_PER_M - ay, 4))]
            i += 2
            cmd = 'l'
        elif cmd == 'L' and i + 1 < n:
            cx, cy = float(tokens[i]), float(tokens[i+1])
            cur.append((round(cx / DWF_PER_M - ax, 4), round(cy / DWF_PER_M - ay, 4)))
            i += 2
        elif cmd == 'l' and i + 1 < n:
            cx += float(tokens[i]); cy += float(tokens[i+1])
            cur.append((round(cx / DWF_PER_M - ax, 4), round(cy / DWF_PER_M - ay, 4)))
            i += 2
        elif cmd == 'H' and i < n:
            cx = float(tokens[i])
            cur.append((round(cx / DWF_PER_M - ax, 4), round(cy / DWF_PER_M - ay, 4)))
            i += 1
        elif cmd == 'h' and i < n:
            cx += float(tokens[i])
            cur.append((round(cx / DWF_PER_M - ax, 4), round(cy / DWF_PER_M - ay, 4)))
            i += 1
        elif cmd == 'V' and i < n:
            cy = float(tokens[i])
            cur.append((round(cx / DWF_PER_M - ax, 4), round(cy / DWF_PER_M - ay, 4)))
            i += 1
        elif cmd == 'v' and i < n:
            cy += float(tokens[i])
            cur.append((round(cx / DWF_PER_M - ax, 4), round(cy / DWF_PER_M - ay, 4)))
            i += 1
        elif cmd == 'C' and i + 5 < n:
            cx, cy = float(tokens[i+4]), float(tokens[i+5])
            cur.append((round(cx / DWF_PER_M - ax, 4), round(cy / DWF_PER_M - ay, 4)))
            i += 6
        elif cmd == 'c' and i + 5 < n:
            cx += float(tokens[i+4]); cy += float(tokens[i+5])
            cur.append((round(cx / DWF_PER_M - ax, 4), round(cy / DWF_PER_M - ay, 4)))
            i += 6
        elif cmd == 'A' and i + 6 < n:
            cx, cy = float(tokens[i+5]), float(tokens[i+6])
            cur.append((round(cx / DWF_PER_M - ax, 4), round(cy / DWF_PER_M - ay, 4)))
            i += 7
        elif cmd == 'a' and i + 6 < n:
            cx += float(tokens[i+5]); cy += float(tokens[i+6])
            cur.append((round(cx / DWF_PER_M - ax, 4), round(cy / DWF_PER_M - ay, 4)))
            i += 7
        else:
            i += 1
    if cur:
        subpaths.append(cur)
    return subpaths

PLANS_ANCHORS = {
    "upper_roof":   ( 59.872 + 20.482,  7.351 + 17.714),
    "floor_9_roof": (108.917 + 20.482,  7.351 + 17.714),
    "floor_8":      (157.962 + 20.482,  7.351 + 17.714),
    "floors_345":   (207.010 + 20.482,  7.351 + 17.714),
    "floors_1267":  (255.841 + 20.482,  7.353 + 17.714),
    "gallery":      (312.227 + 20.482,  7.353 + 17.714),
    "ground":       (378.013 + 20.482, 18.144 + 17.714),
    "basement_2":   (441.014 + 20.613,  6.924 + 18.003),
    "basement_1":   (441.886 + 20.613, 54.335 + 18.003),
}

all_paths = re.findall(r'<Path([^>]+)/>', fpage)

for pname, (ax, ay) in PLANS_ANCHORS.items():
    thick_segs = []
    thin_segs = []
    fill_polys = []
    for attr in all_paths:
        m_d = re.search(r'Data="M([-+]?\d*\.?\d+),([-+]?\d*\.?\d+)', attr)
        if not m_d: continue
        x_init = float(m_d.group(1)) / DWF_PER_M - ax
        y_init = float(m_d.group(2)) / DWF_PER_M - ay
        if not (-22.0 <= x_init <= 22.0 and -20.0 <= y_init <= 21.0):
            continue
        mf = re.search(r'Fill="([^"]+)"', attr)
        ms = re.search(r'Stroke="([^"]+)"', attr)
        mt = re.search(r'StrokeThickness="([^"]+)"', attr)
        fc = mf.group(1).upper() if mf else None
        sc = ms.group(1).upper() if ms else None
        th = mt.group(1) if mt else None
        d_full = re.search(r'Data="([^"]+)"', attr).group(1)
        if fc in ('#1C14FF', '#FF0000', '#FB2323') and 'a5,5' not in d_full and 'a4,4' not in d_full:
            for sp in parse_xps_subpaths(d_full, ax, ay):
                if len(sp) >= 3:
                    p = Polygon(sp).buffer(0)
                    if not p.is_empty and 0.0005 < p.area < 40.0:
                        fill_polys.append(p)
        elif sc == '#000000' and th in ('19', '33'):
            for sp in parse_xps_subpaths(d_full, ax, ay):
                for j in range(len(sp) - 1):
                    p1, p2 = sp[j], sp[j+1]
                    L = math.hypot(p2[0]-p1[0], p2[1]-p1[1])
                    if L >= 0.03 and -18.5 <= p1[0] <= 18.5 and -16.5 <= p1[1] <= 16.5:
                        thick_segs.append(LineString([p1, p2]))
        elif sc == '#000000' and th in ('12', '7', '9'):
            for sp in parse_xps_subpaths(d_full, ax, ay):
                # skip tiny text glyphs
                if len(sp) >= 6 and max((math.hypot(sp[j+1][0]-sp[j][0], sp[j+1][1]-sp[j][1]) for j in range(len(sp)-1)), default=0) < 0.22:
                    continue
                for j in range(len(sp) - 1):
                    p1, p2 = sp[j], sp[j+1]
                    L = math.hypot(p2[0]-p1[0], p2[1]-p1[1])
                    if 0.05 <= L <= 8.0 and -18.5 <= p1[0] <= 18.5 and -16.5 <= p1[1] <= 16.5:
                        thin_segs.append((p1, p2))
    print(f"{pname:14s}: fill_polys={len(fill_polys):4d}, thick_segs(19)={len(thick_segs):4d}, thin_segs(12/7)={len(thin_segs):4d}")
