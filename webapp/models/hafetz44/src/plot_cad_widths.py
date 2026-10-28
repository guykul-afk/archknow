import fitz, math, os
from PIL import Image, ImageDraw

PT_PER_M = 72.0 / 25.4 * 10.0  # 28.3464567 pt/m
p1_path = r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\pdfs\hafetz44_g9_part1.pdf"
out_dir = r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\crops\cad_diag"
os.makedirs(out_dir, exist_ok=True)

doc1 = fitz.open(p1_path)
page1 = doc1[0]
rot1 = page1.rotation_matrix
W1, H1 = page1.rect.width, page1.rect.height

# Wait: where is Typical Floor in Part 1?
# Let's check crops/smart/crop_typical... or typ_full_dims.jpg!
# In extract_facade_crops.py:
# typ_full_dims: (0.31, 0.03, 0.64, 0.48) -> wait: let's view typ_full_dims.jpg or check what is in x=0..0.65!
# Let's plot all segments in x = [0, 0.66*W1], y = [0, H1] by width!
by_w = {}
for d in page1.get_drawings():
    c = tuple(round(x, 2) for x in d['color']) if d.get('color') else None
    w = round(d['width'], 2) if d.get('width') is not None else None
    dashes = d.get('dashes')
    is_dashed = bool(dashes and dashes != "[] 0")
    if is_dashed or c != (0.0, 0.0, 0.0):
        continue
    for it in d['items']:
        if it[0] == 'l':
            p1 = it[1] * rot1
            p2 = it[2] * rot1
            if p1.x <= 0.68 * W1 and p2.x <= 0.68 * W1:
                L = math.hypot(p2.x - p1.x, p2.y - p1.y) / PT_PER_M
                if L >= 0.05:
                    by_w.setdefault(w, []).append((p1.x/PT_PER_M, p1.y/PT_PER_M, p2.x/PT_PER_M, p2.y/PT_PER_M, L))

for w, segs in sorted(by_w.items(), key=lambda x: -len(x[1])):
    xs = [s[0] for s in segs] + [s[2] for s in segs]
    ys = [s[1] for s in segs] + [s[3] for s in segs]
    print(f"Black solid w={w}: {len(segs)} segs, X=[{min(xs):.1f}..{max(xs):.1f}m], Y=[{min(ys):.1f}..{max(ys):.1f}m]")
