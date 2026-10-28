import fitz, math, collections
from PIL import Image, ImageDraw

path2 = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\חפץ חיים 44 פתח תקווה\חפץ 44- ג9 -חלק 2 (1).pdf"
doc = fitz.open(path2)
page = doc[0]
rot = page.rotation_matrix

# Scale 1:100 -> 1m = 10mm = 10 / 25.4 * 72 = 28.346456692913385 pt
PT_PER_M = 72.0 / 25.4 * 10.0

# Wait: where are the floor plans in rotated page coordinates (x in 0..14173, y in 0..2580)?
# Let's check where we cropped the floor plans earlier!
# Earlier in crop_facades_and_plans.py:
# Let's check all segments with L > 1.0m (28.35 pt) across the entire sheet!
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
            if L >= 0.8:
                by_cw[(c, fill, w)] += 1
                segs_by_cw[(c, fill, w)].append((p1.x, p1.y, p2.x, p2.y, L))

print("Top (color, fill, width) for segments >= 0.8m in Part 2:")
for k, cnt in by_cw.most_common(20):
    xs = [s[0] for s in segs_by_cw[k]] + [s[2] for s in segs_by_cw[k]]
    ys = [s[1] for s in segs_by_cw[k]] + [s[3] for s in segs_by_cw[k]]
    print(f"  {k}: {cnt} segs, X=[{min(xs):.0f}..{max(xs):.0f}], Y=[{min(ys):.0f}..{max(ys):.0f}]")
