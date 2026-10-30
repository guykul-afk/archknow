import os
import sys
import zipfile
import re
import fitz

sys.stdout.reconfigure(encoding='utf-8')
ws = r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה"
dwfx_path = os.path.join(ws, "6.5.26-hagasha.dwfx")
scratch_dir = r"C:\Users\User\.gemini\antigravity\brain\71931cc9-7058-41f3-a9f0-80549e5c535b\scratch"

# 1. Check Glyphs in FixedPage.fpage
with zipfile.ZipFile(dwfx_path, 'r') as z:
    fpage = z.read("dwf/documents/20557152-C9F2-4F2A-83D0-E6D25FE4C692/sections/com.autodesk.dwf.ePlot_20557153-C9F2-4F2A-83D0-E6D25FE4C692/FixedPage.fpage").decode('utf-8', errors='replace')
    glyphs = re.findall(r'<Glyphs[^>]*UnicodeString="([^"]*)"[^>]*OriginX="([^"]*)"[^>]*OriginY="([^"]*)"', fpage)
    print(f"Found {len(glyphs)} Glyphs in FixedPage.fpage")
    for g in glyphs[:30]:
        print("  Glyph:", g)

# 2. Render high-res crops of key tables, sections, elevations, and plans
doc = fitz.open(dwfx_path)
page = doc[0]

crops = {
    "title_and_area_table": (21200, 100, 23250, 1450, 220),
    "rishui_zamin_pages":   (23250, 50, 25500, 2750, 180),
    "surveyor_header":      (15750, 50, 16750, 1380, 240),
    "parking_tables":       (13750, 1400, 15250, 2550, 200),
    "plan_basement2":       (12100, 50, 13650, 1350, 180),
    "plan_basement1":       (12100, 1350, 13650, 2780, 180),
    "plan_ground_site":     (10200, 0, 12150, 2800, 180),
    "plan_gallery":         (8650, 50, 10200, 1400, 180),
    "plan_floors_1267":     (7100, 50, 8650, 1350, 180),
    "plan_floors_345":      (5700, 50, 7150, 1350, 180),
    "plan_floor_8":         (4300, 50, 5750, 1350, 180),
    "plan_floor_9_roof":    (2950, 50, 4350, 1350, 180),
    "plan_upper_roof":      (1600, 50, 3000, 1350, 180),
    "sections_all":         (400, 1400, 4700, 2800, 160),
    "elevations_east_west": (4700, 1400, 7450, 2800, 160),
    "elevations_north_south":(7450, 1400, 10200, 2800, 160),
}

for name, (x0, y0, x1, y1, dpi) in crops.items():
    pix = page.get_pixmap(clip=fitz.Rect(x0, y0, x1, y1), dpi=dpi)
    out_p = os.path.join(scratch_dir, f"crop_{name}.png")
    pix.save(out_p)
    print(f"Saved {name}: {pix.width}x{pix.height}")
