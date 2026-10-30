import zipfile, re
from shapely.geometry import Polygon, LineString, MultiLineString, box, Point
from shapely.ops import unary_union, polygonize

DWF_PER_M = 472.4409448818898
dwfx_path = r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה\6.5.26-hagasha.dwfx"
with zipfile.ZipFile(dwfx_path, 'r') as z:
    fpage = z.read("dwf/documents/20557152-C9F2-4F2A-83D0-E6D25FE4C692/sections/com.autodesk.dwf.ePlot_20557153-C9F2-4F2A-83D0-E6D25FE4C692/FixedPage.fpage").decode('utf-8', errors='replace')

from check_lot_boundaries import parse_svg_path_pts

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
    wall_polys = []
    for attr in all_paths:
        m_f = re.search(r'Fill="(#[0-9A-Fa-f]+)"', attr)
        if not m_f: continue
        fc = m_f.group(1).upper()
        if fc not in ('#1C14FF', '#FF0000', '#FB2323', '#F90606', '#FF0F0F'):
            continue
        m_d = re.search(r'Data="([^"]+)"', attr)
        if not m_d: continue
        pts = parse_svg_path_pts(m_d.group(1))
        if len(pts) < 3: continue
        rpts = [(round(x - ax, 4), round(y - ay, 4)) for x, y in pts]
        xs = [p[0] for p in rpts]; ys = [p[1] for p in rpts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        if -21.5 <= x0 and x1 <= 21.5 and -19.5 <= y0 and y1 <= 20.5:
            if (x1 - x0) > 39.0 or (y1 - y0) > 39.0: continue
            p = Polygon(rpts).buffer(0)
            if not p.is_empty and p.area > 0.0005:
                wall_polys.append(p)
    u = unary_union(wall_polys).buffer(0.005, join_style=2).buffer(-0.005, join_style=2).simplify(0.002, preserve_topology=True)
    geoms = list(u.geoms) if hasattr(u, 'geoms') else ([u] if not u.is_empty else [])
    geoms = [g for g in geoms if g.area >= 0.015]
    b = u.bounds if not u.is_empty else (0,0,0,0)
    print(f"{pname:14s}: raw_tris={len(wall_polys):4d} -> merged_polys={len(geoms):3d}, total_area={u.area:6.2f} m2, bounds=[{b[0]:.3f}, {b[1]:.3f}, {b[2]:.3f}, {b[3]:.3f}]")
