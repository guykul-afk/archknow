import fitz, math, collections

path1 = r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\pdfs\hafetz44_g9_part1.pdf"
doc = fitz.open(path1)
page = doc[0]
rot = page.rotation_matrix
W, H = page.rect.width, page.rect.height
PT_PER_M = 72.0 / 25.4 * 10.0  # 1:100 scale -> 28.3464567 pt/m

print(f"Part 1 rect: {W} x {H} pt ({W/PT_PER_M:.1f}m x {H/PT_PER_M:.1f}m at 1:100)")

by_cw = collections.Counter()
segs_by_cw = collections.defaultdict(list)

for d in page.get_drawings():
    c = tuple(round(x, 2) for x in d['color']) if d.get('color') else None
    fill = tuple(round(x, 2) for x in d['fill']) if d.get('fill') else None
    w = round(d['width'], 2) if d.get('width') is not None else None
    for it in d['items']:
        if it[0] == 'l':
            p1 = it[1] * rot
            p2 = it[2] * rot
            L = math.hypot(p2.x - p1.x, p2.y - p1.y) / PT_PER_M
            if L >= 0.5:
                by_cw[(c, fill, w)] += 1
                segs_by_cw[(c, fill, w)].append((p1.x, p1.y, p2.x, p2.y, L))

print("Top (color, fill, width) for segments >= 0.5m in Part 1:")
for k, cnt in by_cw.most_common(20):
    xs = [s[0] for s in segs_by_cw[k]] + [s[2] for s in segs_by_cw[k]]
    ys = [s[1] for s in segs_by_cw[k]] + [s[3] for s in segs_by_cw[k]]
    print(f"  {k}: {cnt} segs, X=[{min(xs):.0f}..{max(xs):.0f}] ({min(xs)/W:.2f}..{max(xs)/W:.2f}), Y=[{min(ys):.0f}..{max(ys):.0f}] ({min(ys)/H:.2f}..{max(ys)/H:.2f})")
