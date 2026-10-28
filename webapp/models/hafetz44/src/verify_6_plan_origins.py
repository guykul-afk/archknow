import fitz, math

PT_PER_M = 72.0 / 25.4 * 10.0  # 28.3464567 pt/m
p1_path = r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\pdfs\hafetz44_g9_part1.pdf"
doc1 = fitz.open(p1_path)
page1 = doc1[0]
rot1 = page1.rotation_matrix

# Let's find the exact lot boundary boxes or elevator shafts in all 6 plans!
# Notice in Cluster 2,3,4,5:
# Top row Y_lot_top = 8.57m, Y_lot_bot = 26.97m (height = 18.40m)
# Bot row Y_lot_top = 34.09m, Y_lot_bot = 52.49m (height = 18.40m)
# Let's check where the Ground Floor lot boundary (38.82m x 18.40m) is around X=135..185m!
for d in page1.get_drawings():
    r = d['rect'] * rot1
    x0, y0, x1, y1 = r.x0/PT_PER_M, r.y0/PT_PER_M, r.x1/PT_PER_M, r.y1/PT_PER_M
    w, h = x1 - x0, y1 - y0
    if 18.30 <= h <= 18.50 and w >= 33.0:
        print(f"Lot Box candidate: X=[{x0:.3f}..{x1:.3f}] (W={w:.3f}), Y=[{y0:.3f}..{y1:.3f}] (H={h:.3f}) color={d.get('color')} w={d.get('width')}")

# Also let's check elevator shaft (1.70m x 1.85m) in each plan region!
regions = {
    'roof_top':  (0.0, 5.0, 38.0, 30.0),
    'penthouse': (40.0, 5.0, 82.0, 30.0),
    'typical':   (84.0, 5.0, 126.0, 30.0),
    'roof_main': (40.0, 31.0, 82.0, 55.0),
    'basement':  (84.0, 31.0, 126.0, 55.0),
    'ground':    (130.0, 5.0, 190.0, 40.0),
}

for rname, (rx0, ry0, rx1, ry1) in regions.items():
    # Find blue concrete or thick black lines in this region
    b_xs, b_ys = [], []
    for d in page1.get_drawings():
        c = tuple(round(x, 2) for x in d['color']) if d.get('color') else None
        f = tuple(round(x, 2) for x in d['fill']) if d.get('fill') else None
        w = round(d['width'], 2) if d.get('width') is not None else None
        r = d['rect'] * rot1
        x0, y0, x1, y1 = r.x0/PT_PER_M, r.y0/PT_PER_M, r.x1/PT_PER_M, r.y1/PT_PER_M
        if rx0 <= x0 and x1 <= rx1 and ry0 <= y0 and y1 <= ry1:
            if c == (0.0, 0.32, 1.0) or f == (0.0, 0.32, 1.0):
                b_xs.extend([x0, x1])
                b_ys.extend([y0, y1])
    if b_xs:
        print(f"Region {rname:10s}: blue bounds X=[{min(b_xs):.3f}..{max(b_xs):.3f}] (W={max(b_xs)-min(b_xs):.3f}), Y=[{min(b_ys):.3f}..{max(b_ys):.3f}] (H={max(b_ys)-min(b_ys):.3f})")
