import zipfile, re
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

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
    "basement_2":   (441.014 + 20.536,  6.924 + 17.750),
    "basement_1":   (441.886 + 20.536, 54.335 + 17.750),
}

# Let's check the inner Mamad/Elevator core #1C14FF bounds in relative coordinates (-10..+10, -6..+6) for each plan!
wall_paths = re.findall(r'<Path[^>]*Fill="(#1C14FF)"[^>]*Data="([^"]+)"', fpage)
for pname, (ax, ay) in PLANS_ANCHORS.items():
    core_xs, core_ys = [], []
    for _, d_str in wall_paths:
        pts = parse_svg_path_pts(d_str)
        if not pts: continue
        rpts = [(x - ax, y - ay) for x, y in pts]
        xs = [p[0] for p in rpts]; ys = [p[1] for p in rpts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        if -12.0 <= x0 and x1 <= 12.0 and -12.5 <= y0 and y1 <= 5.0:
            core_xs.extend([x0, x1]); core_ys.extend([y0, y1])
    if core_xs:
        print(f"{pname:14s}: Core #1C14FF rel X=[{min(core_xs):.3f}..{max(core_xs):.3f}], Y=[{min(core_ys):.3f}..{max(core_ys):.3f}]")
