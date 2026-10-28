import fitz, math, os
from PIL import Image, ImageDraw
import shapely
from shapely.geometry import LineString, MultiLineString, Polygon, Point, box
from shapely.ops import polygonize, unary_union
from shapely import snap

PT_PER_M = 72.0 / 25.4 * 10.0  # 28.3464567 pt/m
p1_path = r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\pdfs\hafetz44_g9_part1.pdf"
out_dir = r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\crops\cad_diag"
os.makedirs(out_dir, exist_ok=True)

doc1 = fitz.open(p1_path)
page1 = doc1[0]
rot1 = page1.rotation_matrix

# First let's check roof_top staircase tower to get its exact (ox, oy)
for d in page1.get_drawings():
    r = d['rect'] * rot1
    x0, y0, x1, y1 = r.x0/PT_PER_M, r.y0/PT_PER_M, r.x1/PT_PER_M, r.y1/PT_PER_M
    if x1 < 38.0 and 5.0 < y0 < 30.0:
        c = tuple(round(x, 2) for x in d['color']) if d.get('color') else None
        w = round(d['width'], 2) if d.get('width') is not None else None
        if w in (1.08, 0.96) or (3.2 <= (x1-x0) <= 4.0 and 3.0 <= (y1-y0) <= 3.8):
            print(f"roof_top candidate: X=[{x0:.3f}..{x1:.3f}] (W={x1-x0:.3f}), Y=[{y0:.3f}..{y1:.3f}] (H={y1-y0:.3f}) c={c} w={w}")

# Now let's inspect the Typical Floor (ox=85.590, oy=26.969) in detail:
# What drawing types/fills/widths make up the walls vs windows vs doors vs furniture?
ox, oy = 85.590, 26.969
rx0, ry0, rx1, ry1 = 85.0, 8.0, 125.0, 27.5

# Let's render separate diagnostic images for:
# 1. Blue fills (0.0, 0.32, 1.0) + White fills (1.0, 1.0, 1.0) + Yellow fills (1.0, 1.0, 0.06)
# 2. Black lines w=1.08, w=0.96, w=0.72, w=0.60, w=0.48
W_img, H_img = 1941, 920  # 50 px per meter for 38.82m x 18.40m!
scale = 50.0

def to_px(x_m, y_m):
    return (int(round(x_m * scale)), int(round((18.40 - y_m) * scale)))

img_fills = Image.new("RGB", (W_img, H_img), (240, 244, 248))
dr_fills = ImageDraw.Draw(img_fills)

img_w108 = Image.new("RGB", (W_img, H_img), (255, 255, 255))
dr_w108 = ImageDraw.Draw(img_w108)

img_w072 = Image.new("RGB", (W_img, H_img), (255, 255, 255))
dr_w072 = ImageDraw.Draw(img_w072)

for d in page1.get_drawings():
    r = d['rect'] * rot1
    x0, y0, x1, y1 = r.x0/PT_PER_M, r.y0/PT_PER_M, r.x1/PT_PER_M, r.y1/PT_PER_M
    if not (rx0 <= x0 and x1 <= rx1 and ry0 <= y0 and y1 <= ry1):
        continue
    if (x1 - x0) > 35.0:
        continue
    c = tuple(round(x, 2) for x in d['color']) if d.get('color') else None
    f = tuple(round(x, 2) for x in d['fill']) if d.get('fill') else None
    w = round(d['width'], 2) if d.get('width') is not None else None
    dashes = d.get('dashes')
    is_dashed = bool(dashes and dashes != "[] 0")

    # Check filled polygons
    if f in ((0.0, 0.32, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, 0.06)):
        pts = []
        for it in d['items']:
            if it[0] == 'l':
                p1 = it[1] * rot1
                pts.append(to_px(p1.x/PT_PER_M - ox, oy - p1.y/PT_PER_M))
            elif it[0] == 're':
                rr = it[1] * rot1
                p_a = to_px(rr.x0/PT_PER_M - ox, oy - rr.y0/PT_PER_M)
                p_b = to_px(rr.x1/PT_PER_M - ox, oy - rr.y1/PT_PER_M)
                col = (37, 99, 235) if f == (0.0, 0.32, 1.0) else ((250, 204, 21) if f == (1.0, 1.0, 0.06) else (255, 255, 255))
                dr_fills.rectangle([min(p_a[0],p_b[0]), min(p_a[1],p_b[1]), max(p_a[0],p_b[0]), max(p_a[1],p_b[1])], fill=col, outline=(100,116,139))
        if len(pts) >= 3:
            col = (37, 99, 235) if f == (0.0, 0.32, 1.0) else ((250, 204, 21) if f == (1.0, 1.0, 0.06) else (255, 255, 255))
            dr_fills.polygon(pts, fill=col, outline=(100,116,139))

    if not is_dashed and c == (0.0, 0.0, 0.0):
        for it in d['items']:
            if it[0] == 'l':
                p1, p2 = it[1] * rot1, it[2] * rot1
                pa = to_px(p1.x/PT_PER_M - ox, oy - p1.y/PT_PER_M)
                pb = to_px(p2.x/PT_PER_M - ox, oy - p2.y/PT_PER_M)
                if w in (1.08, 0.96, 1.44):
                    col = (220, 38, 38) if w == 1.08 else (37, 99, 235)
                    dr_w108.line([pa, pb], fill=col, width=2)
                elif w == 0.72:
                    dr_w072.line([pa, pb], fill=(15, 23, 42), width=1)
                elif w in (0.60, 0.48):
                    dr_w072.line([pa, pb], fill=(217, 119, 6), width=1)

img_fills.save(os.path.join(out_dir, "typ_fills.png"))
img_w108.save(os.path.join(out_dir, "typ_w108.png"))
img_w072.save(os.path.join(out_dir, "typ_w072.png"))
print("Saved diagnostic images!")
