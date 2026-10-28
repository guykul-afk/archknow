import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

scratch_dir = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch"
with open(os.path.join(scratch_dir, "all_texts_fixed.json"), "r", encoding="utf-8") as f:
    texts = json.load(f)
with open(os.path.join(scratch_dir, "dwg_frames_and_data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== 1. APARTMENT AREAS TABLE (X in [1500, 4500], Y in [-85000, -81000]) ===")
table_texts = [t for t in texts if 1500 <= t["x"] <= 4500 and -85000 <= t["y"] <= -81000]
# Group by row (y within 30 units)
table_texts.sort(key=lambda t: (-round(t["y"] / 30), -t["x"]))
cur_y = None
row = []
for t in table_texts:
    if cur_y is None or abs(t["y"] - cur_y) > 40:
        if row:
            print(f"Y={cur_y:8.1f} | " + " | ".join(f"{r['heb']} (x={r['x']:.0f})" for r in row))
        cur_y = t["y"]
        row = [t]
    else:
        row.append(t)
if row:
    print(f"Y={cur_y:8.1f} | " + " | ".join(f"{r['heb']} (x={r['x']:.0f})" for r in row))

# Let's check the KB lines or common elevator/stair anchor across the 9 floor plans
# Notice KB line with dx=-1147.47, dy=-241.92 (the northern building line parallel to Yatkovski street):
# Let's see where it is in each floor plan!
print("\n=== 2. NORTHERN KB LINE & ELEVATOR CORE ANCHORS PER PLAN ===")
plans_info = [
    ("basement", "תוכנית קומת מרתף", -500, 2000, -79200, -74500),
    ("ground", "תוכנית קומת קרקע", -4000, -1500, -80200, -75000),
    ("floor_1", "תוכנית קומה 1", -7200, -5200, -79600, -75500),
    ("floor_2", "תוכנית קומה 2", -9900, -7900, -79600, -75500),
    ("floors_3_4", "תוכנית קומות 3-4", -12500, -10500, -79600, -75500),
    ("floor_5", "תוכנית קומה 5", -15200, -13200, -79600, -75500),
    ("floor_6", "תוכנית קומה 6", -17900, -15900, -79600, -75500),
    ("roofs", "תוכנית גגות", -20500, -18500, -79600, -75500),
    ("upper_roof", "תוכנית גג עליון", -23100, -21100, -79600, -75500),
]

for pid, pname, xmin, xmax, ymin, ymax in plans_info:
    p_texts = [t for t in texts if xmin <= t["x"] <= xmax and ymin <= t["y"] <= ymax]
    # Find texts that look like room labels, areas, dimensions, or levels
    interesting = [t for t in p_texts if any(c.isalpha() or '\u0590' <= c <= '\u05FF' for c in t["heb"]) or '.' in t["heb"] or '+' in t["heb"] or '-' in t["heb"]]
    # Find block `saff` or `D100` or `m17` or `KB` inside this bbox
    kb_in = [l for l in data["lines_by_layer"].get("KB", []) if xmin <= l[0] <= xmax and ymin <= l[1] <= ymax]
    print(f"\n--- {pid} ({pname}) X=[{xmin},{xmax}] ---")
    for l in kb_in:
        print(f"  KB: ({l[0]:.2f}, {l[1]:.2f}) -> ({l[2]:.2f}, {l[3]:.2f})")
    for t in sorted(interesting, key=lambda x: (-x["y"], -x["x"])):
        print(f"  [{t['x']:8.1f}, {t['y']:8.1f}] L={t['layer']:10s} H={t['h']:4.1f} | {t['heb']}  (raw={t['val']})")
