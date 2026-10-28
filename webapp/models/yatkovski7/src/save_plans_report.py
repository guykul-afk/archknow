import os
import sys
import json

scratch_dir = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch"
with open(os.path.join(scratch_dir, "all_texts_fixed.json"), "r", encoding="utf-8") as f:
    texts = json.load(f)
with open(os.path.join(scratch_dir, "dwg_frames_and_data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

out_lines = []
def log(s=""):
    out_lines.append(s)

log("=== 1. APARTMENT AREAS TABLE (X in [1000, 4800], Y in [-85000, -81000]) ===")
table_texts = [t for t in texts if 1000 <= t["x"] <= 4800 and -85000 <= t["y"] <= -81000]
table_texts.sort(key=lambda t: (-round(t["y"] / 25), -t["x"]))
cur_y = None
row = []
for t in table_texts:
    if cur_y is None or abs(t["y"] - cur_y) > 35:
        if row:
            log(f"Y={cur_y:8.1f} | " + " | ".join(f"{r['heb']} (x={r['x']:.0f})" for r in row))
        cur_y = t["y"]
        row = [t]
    else:
        row.append(t)
if row:
    log(f"Y={cur_y:8.1f} | " + " | ".join(f"{r['heb']} (x={r['x']:.0f})" for r in row))

log("\n=== 2. ALL 'מעלית' (ELEVATOR) TEXTS ACROSS MODELSPACE ===")
for t in sorted([t for t in texts if "מעלית" in t["heb"]], key=lambda x: (-x["x"], -x["y"])):
    log(f"  מעלית at ({t['x']:9.2f}, {t['y']:9.2f}) L={t['layer']} H={t['h']}")

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
    ("sections_BD", "חתכים B-B / D-D", -26300, -23200, -83500, -76000),
    ("sections_AC", "חתכים A-A / C-C", -30700, -26900, -83500, -76000),
    ("elev_west_sec_E", "חזית מערבית / חתך E-E", -34500, -31000, -80200, -76000),
    ("elev_east", "חזית מזרחית", -38800, -35800, -80200, -76000),
    ("elev_north", "חזית צפונית", -41200, -38900, -80200, -76000),
    ("elev_south", "חזית דרומית", -44800, -42400, -80200, -76000),
]

for pid, pname, xmin, xmax, ymin, ymax in plans_info:
    p_texts = [t for t in texts if xmin <= t["x"] <= xmax and ymin <= t["y"] <= ymax]
    kb_in = [l for l in data["lines_by_layer"].get("KB", []) if xmin <= l[0] <= xmax and ymin <= l[1] <= ymax]
    log(f"\n==========================================")
    log(f"PLAN: {pid} ({pname}) X=[{xmin},{xmax}], Y=[{ymin},{ymax}] (Total texts: {len(p_texts)})")
    for l in kb_in:
        log(f"  KB: ({l[0]:.2f}, {l[1]:.2f}) -> ({l[2]:.2f}, {l[3]:.2f})")
    for t in sorted(p_texts, key=lambda x: (-x["y"], -x["x"])):
        log(f"  [{t['x']:8.1f}, {t['y']:8.1f}] L={t['layer']:10s} H={t['h']:4.1f} | {t['heb']}  (raw={t['val']})")

with open(os.path.join(scratch_dir, "plans_report.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))
print("Saved plans_report.txt with", len(out_lines), "lines.")
