import json, math
from shapely.geometry import box

with open(r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\hafetz44_extracted_plans.json", encoding="utf-8") as f:
    plans = json.load(f)

def dump_segs_in_box(plan_name, x0, y0, x1, y1, label):
    segs = plans[plan_name]["cad_lines"]
    xs, ys = [], []
    hit = []
    for s in segs:
        sx0, sy0, sx1, sy1 = s
        mx, my = 0.5*(sx0+sx1), 0.5*(sy0+sy1)
        if x0 <= mx <= x1 and y0 <= my <= y1:
            xs.extend([sx0, sx1])
            ys.extend([sy0, sy1])
            hit.append(s)
    if xs:
        print(f"[{plan_name}] {label:32s}: count={len(hit):3d} bbox=[{min(xs):7.3f}, {min(ys):7.3f}, {max(xs):7.3f}, {max(ys):7.3f}]")
    else:
        print(f"[{plan_name}] {label:32s}: EMPTY")

print("=== TYPICAL FLOOR WEST APARTMENT ===")
dump_segs_in_box("typical", -13.10,  1.20,  -9.20,  3.95, "W Living Sofa/Table/Armchair")
dump_segs_in_box("typical", -12.60,  3.10, -10.20,  3.95, "W Living 3-Seat Sofa (South)")
dump_segs_in_box("typical", -11.90,  1.80, -10.80,  2.95, "W Living Coffee Table")
dump_segs_in_box("typical", -10.60,  1.90,  -9.60,  3.10, "W Living Armchair")
dump_segs_in_box("typical", -12.80,  1.35, -10.00,  3.60, "W Living Rug")
dump_segs_in_box("typical",  -9.20,  2.20,  -7.40,  3.95, "W Dining Table & 6 Chairs")
dump_segs_in_box("typical",  -7.20,  2.20,  -5.80,  3.95, "W Kitchen Peninsula/Bar")
dump_segs_in_box("typical",  -5.50,  1.20,  -3.30,  3.95, "W Kitchen L-Counter (E+S)")
dump_segs_in_box("typical", -13.10, -3.10, -10.90, -0.90, "W Master Bed + Nightstands")
dump_segs_in_box("typical", -10.90, -4.90,  -9.60, -3.30, "W Master Walk-in Closet")
dump_segs_in_box("typical", -13.10, -4.90, -11.00, -3.30, "W Master Bathroom")
dump_segs_in_box("typical",  -9.50, -4.90,  -6.50, -1.50, "W Bedroom 1 (Bed+Wardrobe)")
dump_segs_in_box("typical",  -9.50, -3.80,  -8.00, -1.60, "W Bedroom 1 Bed")
dump_segs_in_box("typical",  -9.40, -1.90,  -7.40, -1.20, "W Bedroom 1 Wardrobe")
dump_segs_in_box("typical",  -6.50, -3.80,  -5.00, -1.60, "W Bedroom 2 Bed")
dump_segs_in_box("typical",  -6.40, -1.90,  -4.60, -1.20, "W Bedroom 2 Wardrobe")
dump_segs_in_box("typical",  -3.60, -4.20,  -1.15, -1.20, "W General Bathroom")
dump_segs_in_box("typical",  -1.05, -4.30,   2.25, -0.30, "W Mamad (Bed+Wardrobe)")
dump_segs_in_box("typical",   0.80, -3.60,   2.25, -1.20, "W Mamad Bed (East wall)")
dump_segs_in_box("typical",  -0.30, -0.90,   1.80, -0.25, "W Mamad Wardrobe (South wall)")

print("\n=== TYPICAL FLOOR EAST APARTMENT ===")
dump_segs_in_box("typical",  10.20,  1.20,  14.10,  3.95, "E Living Sofa/Table/Armchair")
dump_segs_in_box("typical",  11.00,  3.10,  13.80,  3.95, "E Living 3-Seat Sofa (South)")
dump_segs_in_box("typical",  11.50,  1.80,  12.80,  2.95, "E Living Coffee Table")
dump_segs_in_box("typical",  10.20,  1.90,  11.30,  3.10, "E Living Armchair")
dump_segs_in_box("typical",   8.40,  2.20,  10.10,  3.95, "E Dining Table & 6 Chairs")
dump_segs_in_box("typical",   7.00,  2.20,   8.30,  3.95, "E Kitchen Peninsula/Bar")
dump_segs_in_box("typical",   5.65,  1.20,   7.50,  3.95, "E Kitchen L-Counter (W+S)")
dump_segs_in_box("typical",  11.80, -3.10,  14.10, -0.90, "E Master Bed + Nightstands")
dump_segs_in_box("typical",  10.80, -4.90,  12.40, -3.30, "E Master Walk-in Closet")
dump_segs_in_box("typical",  12.40, -4.90,  14.10, -3.30, "E Master Bathroom")
dump_segs_in_box("typical",   9.20, -3.80,  10.80, -1.60, "E Bedroom 1 Bed")
dump_segs_in_box("typical",   8.60, -1.90,  10.70, -1.20, "E Bedroom 1 Wardrobe")
dump_segs_in_box("typical",   5.65, -4.20,   7.90, -1.20, "E General Bathroom")
dump_segs_in_box("typical",   2.45, -3.60,   3.90, -1.20, "E Mamad Bed (West wall)")
dump_segs_in_box("typical",   2.50, -0.90,   4.50, -0.25, "E Mamad Wardrobe (South wall)")


print("\n=== PENTHOUSE FLOOR 9 ===")
dump_segs_in_box("penthouse",   4.50, -4.60,   8.80, -0.20, "PH Living Room (Sofa+Table+Chair)")
dump_segs_in_box("penthouse",   5.50, -2.50,   8.30, -1.20, "PH Living 3-Seat Sofa")
dump_segs_in_box("penthouse",   6.00, -3.70,   7.50, -2.60, "PH Living Coffee Table")
dump_segs_in_box("penthouse",   4.70, -3.60,   5.90, -2.20, "PH Living Armchair (West)")
dump_segs_in_box("penthouse",   6.50, -1.00,   9.10,  1.20, "PH Dining Table & 6 Chairs")
dump_segs_in_box("penthouse",   5.20,  1.60,   8.50,  2.80, "PH Kitchen Island")
dump_segs_in_box("penthouse",   3.90,  1.10,   9.30,  3.95, "PH Kitchen L-Counter (W+S)")
dump_segs_in_box("penthouse",  -7.20,  1.20,  -4.60,  3.60, "PH Master Bed + Nightstands")
dump_segs_in_box("penthouse", -10.00,  0.50,  -7.10,  3.95, "PH Master Walk-in Closet / Study")
dump_segs_in_box("penthouse",  -3.60,  1.90,  -1.40,  4.00, "PH Master Bathroom")
dump_segs_in_box("penthouse",  -9.95, -4.90,  -8.40, -2.50, "PH Bedroom W1 Bed")
dump_segs_in_box("penthouse",  -9.95, -0.80,  -8.20,  0.60, "PH Bedroom W1 Closets")
dump_segs_in_box("penthouse",  -6.80, -4.90,  -5.20, -2.50, "PH Bedroom W2 Bed")
dump_segs_in_box("penthouse",  -6.80, -2.20,  -5.00, -1.20, "PH Bedroom W2 Wardrobe")
dump_segs_in_box("penthouse",  -3.60, -4.20,  -1.15, -1.20, "PH General Bathroom")
dump_segs_in_box("penthouse",  -1.05, -4.30,   2.25, -1.50, "PH Mamad Bed+Closet")
dump_segs_in_box("penthouse",   2.30, -4.40,   3.90, -0.50, "PH Guest WC & Closet")
