import fitz, math

doc = fitz.open(r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\pdfs\hafetz44_g9_part1.pdf")
p = doc[0]
rot = p.rotation_matrix
pt_m = 72.0 / 25.4 * 10.0

for plan_name, (ax, ay, rx0, rx1, ry0, ry1) in [
    ("ground", (160.203, 24.381, 135.0, 192.0, 11.0, 37.0)),
    ("basement", (105.004, 43.287, 83.0, 128.0, 32.0, 55.0))
]:
    print(f"=== {plan_name.upper()} LONG LINES (>3.0m) ===")
    for d in p.get_drawings():
        r = d['rect'] * rot
        x0, y0, x1, y1 = r.x0 / pt_m, r.y0 / pt_m, r.x1 / pt_m, r.y1 / pt_m
        if x1 < rx0 or x0 > rx1 or y1 < ry0 or y0 > ry1:
            continue
        w_m, h_m = x1 - x0, y1 - y0
        if max(w_m, h_m) < 3.0 or max(w_m, h_m) > 45.0:
            continue
        col = tuple(round(c, 2) for c in d['color']) if d.get('color') else None
        lw = round(d['width'], 2) if d.get('width') is not None else None
        print(f"  [{x0-ax:7.3f}, {y0-ay:7.3f}] -> [{x1-ax:7.3f}, {y1-ay:7.3f}]  span=({w_m:6.2f}x{h_m:6.2f}) col={col} lw={lw} dash={d.get('dashes')}")
