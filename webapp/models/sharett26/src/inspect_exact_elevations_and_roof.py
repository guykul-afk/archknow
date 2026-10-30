import pymupdf as fitz, os, re
from test_xps_extractor import parse_xps_subpaths, PLANS_ANCHORS, DWF_PER_M, all_paths

DWFX_PATH = r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה\6.5.26-hagasha.dwfx"
OUT_DIR = r"C:\Users\User\.gemini\antigravity\brain\71931cc9-7058-41f3-a9f0-80549e5c535b\scratch"

doc = fitz.open(DWFX_PATH)
page = doc[0]
clip = fitz.Rect(9200, 0, 13000, 2834)
pix = page.get_pixmap(matrix=fitz.Matrix(1.2, 1.2), clip=clip)
pix.save(os.path.join(OUT_DIR, "ground_and_south_elev_real.png"))
print("Saved ground_and_south_elev_real.png", pix.width, pix.height)

# Inspect all stroke colors & thicknesses on floor_9_roof and upper_roof, and find why fill_polys was 0 on floor_9_roof
for pname in ["upper_roof", "floor_9_roof", "floor_8", "floors_1267"]:
    ax, ay = PLANS_ANCHORS[pname]
    stats = {}
    blue_bounds = []
    thick19_bounds = []
    for attr in all_paths:
        m_d = re.search(r'Data="M([-+]?\d*\.?\d+),([-+]?\d*\.?\d+)', attr)
        if not m_d: continue
        x_init = float(m_d.group(1)) / DWF_PER_M - ax
        y_init = float(m_d.group(2)) / DWF_PER_M - ay
        if not (-20.0 <= x_init <= 20.0 and -18.0 <= y_init <= 18.0): continue
        mf = re.search(r'Fill="([^"]+)"', attr)
        ms = re.search(r'Stroke="([^"]+)"', attr)
        mt = re.search(r'StrokeThickness="([^"]+)"', attr)
        fc = mf.group(1).upper() if mf else None
        sc = ms.group(1).upper() if ms else None
        th = mt.group(1) if mt else None
        key = (fc, sc, th)
        stats[key] = stats.get(key, 0) + 1
        d_full = re.search(r'Data="([^"]+)"', attr).group(1)
        if sc == '#1C14FF' or fc == '#1C14FF':
            for sp in parse_xps_subpaths(d_full, ax, ay):
                xs = [p[0] for p in sp]
                ys = [p[1] for p in sp]
                blue_bounds.append((round(min(xs),2), round(min(ys),2), round(max(xs),2), round(max(ys),2)))
        if sc == '#000000' and th == '19':
            for sp in parse_xps_subpaths(d_full, ax, ay):
                xs = [p[0] for p in sp]
                ys = [p[1] for p in sp]
                thick19_bounds.append((round(min(xs),2), round(min(ys),2), round(max(xs),2), round(max(ys),2)))
    print(f"=== {pname} (anchor {ax:.1f}, {ay:.1f}) ===")
    for k, v in sorted(stats.items(), key=lambda x: -x[1])[:10]:
        print("  ", k, ":", v)
    if pname in ("upper_roof", "floor_9_roof"):
        print("  blue_bounds sample:", blue_bounds[:10])
        print("  thick19_bounds:", thick19_bounds)
