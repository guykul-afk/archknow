import zipfile, re

DWF_PER_M = 472.4409448818898
dwfx_path = r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה\6.5.26-hagasha.dwfx"
with zipfile.ZipFile(dwfx_path, 'r') as z:
    fpage = z.read("dwf/documents/20557152-C9F2-4F2A-83D0-E6D25FE4C692/sections/com.autodesk.dwf.ePlot_20557153-C9F2-4F2A-83D0-E6D25FE4C692/FixedPage.fpage").decode('utf-8', errors='replace')

from check_lot_boundaries import parse_svg_path_pts
all_paths = re.findall(r'<Path([^>]+)/>', fpage)
for attr in all_paths:
    if 'Stroke="#0051FF"' in attr:
        pts = parse_svg_path_pts(re.search(r'Data="([^"]+)"', attr).group(1))
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        if 38.0 <= (max(xs) - min(xs)) <= 44.0:
            x0, y0 = min(xs), min(ys)
            rel_pts = [(round(x - x0, 3), round(y - y0, 3)) for x, y in pts]
            print(f"Origin=({x0:.3f}, {y0:.3f}) -> rel_pts={rel_pts}")
