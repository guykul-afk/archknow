import fitz, math, os
from PIL import Image, ImageDraw

PT_PER_M = 72.0 / 25.4 * 10.0  # 1:100 scale -> 28.3464567 pt/m

p1_path = r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\pdfs\hafetz44_g9_part1.pdf"
p2_path = r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\pdfs\hafetz44_g9_part2.pdf"

doc1 = fitz.open(p1_path)
page1 = doc1[0]
rot1 = page1.rotation_matrix
W1, H1 = page1.rect.width, page1.rect.height

# Let's check typical floor plan in part1: x in [0.31*W1, 0.64*W1], y in [0.03*H1, 0.48*H1]
# Wait: let's see how d['rect'] transforms under rot1!
r_typ = fitz.Rect(0.32 * W1, 0.05 * H1, 0.56 * W1, 0.45 * H1)

by_cw = {}
for d in page1.get_drawings():
    c = tuple(round(x, 2) for x in d['color']) if d.get('color') else None
    fill = tuple(round(x, 2) for x in d['fill']) if d.get('fill') else None
    w = round(d['width'], 2) if d.get('width') is not None else None
    dashes = d.get('dashes')
    is_dashed = bool(dashes and dashes != "[] 0")
    for it in d['items']:
        if it[0] == 'l':
            p1 = it[1] * rot1
            p2 = it[2] * rot1
            if r_typ.contains(p1) or r_typ.contains(p2):
                L = math.hypot(p2.x - p1.x, p2.y - p1.y) / PT_PER_M
                if L >= 0.05:
                    by_cw.setdefault((c, fill, w, is_dashed), []).append((p1.x/PT_PER_M, p1.y/PT_PER_M, p2.x/PT_PER_M, p2.y/PT_PER_M, L))

print("=== Typical Floor Plan (Part 1, x=0.32..0.56, y=0.05..0.45) vector layers ===")
for k, segs in sorted(by_cw.items(), key=lambda x: -len(x[1]))[:25]:
    maxL = max(s[4] for s in segs)
    avgL = sum(s[4] for s in segs) / len(segs)
    print(f"  color={k[0]} fill={k[1]} w={k[2]} dashed={k[3]}: {len(segs)} segs (avgL={avgL:.2f}m, maxL={maxL:.2f}m)")
