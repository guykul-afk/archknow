import fitz, math

PT_PER_M = 72.0 / 25.4 * 10.0  # 28.3464567 pt/m
p1_path = r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\pdfs\hafetz44_g9_part1.pdf"
doc1 = fitz.open(p1_path)
page1 = doc1[0]
rot1 = page1.rotation_matrix

regions = {
    'roof_top':  (0.0, 5.0, 38.0, 30.0),
    'penthouse': (40.0, 5.0, 82.0, 30.0),
    'typical':   (84.0, 5.0, 126.0, 30.0),
    'roof_main': (40.0, 31.0, 82.0, 55.0),
    'basement':  (84.0, 31.0, 126.0, 55.0),
    'ground':    (130.0, 5.0, 190.0, 40.0),
}

for rname, (rx0, ry0, rx1, ry1) in regions.items():
    b_xs, b_ys = [], []
    w108_xs, w108_ys = [], []
    for d in page1.get_drawings():
        c = tuple(round(x, 2) for x in d['color']) if d.get('color') else None
        f = tuple(round(x, 2) for x in d['fill']) if d.get('fill') else None
        w = round(d['width'], 2) if d.get('width') is not None else None
        r = d['rect'] * rot1
        x0, y0, x1, y1 = r.x0/PT_PER_M, r.y0/PT_PER_M, r.x1/PT_PER_M, r.y1/PT_PER_M
        if rx0 <= x0 and x1 <= rx1 and ry0 <= y0 and y1 <= ry1:
            if (x1 - x0) > 33.0 and (y1 - y0) > 18.0:
                continue  # skip outer lot frame
            if f == (0.0, 0.32, 1.0):
                b_xs.extend([x0, x1])
                b_ys.extend([y0, y1])
            if c == (0.0, 0.0, 0.0) and w == 1.08:
                w108_xs.extend([x0, x1])
                w108_ys.extend([y0, y1])
    if b_xs:
        print(f"{rname:10s} blue fills : X=[{min(b_xs):.3f}..{max(b_xs):.3f}] (W={max(b_xs)-min(b_xs):.3f}), Y=[{min(b_ys):.3f}..{max(b_ys):.3f}] (H={max(b_ys)-min(b_ys):.3f})")
    if w108_xs:
        print(f"{rname:10s} black w1.08: X=[{min(w108_xs):.3f}..{max(w108_xs):.3f}] (W={max(w108_xs)-min(w108_xs):.3f}), Y=[{min(w108_ys):.3f}..{max(w108_ys):.3f}] (H={max(w108_ys)-min(w108_ys):.3f})")
