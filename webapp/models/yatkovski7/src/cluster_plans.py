import os
import sys
import json
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

scratch_dir = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch"
with open(os.path.join(scratch_dir, "dwg_frames_and_data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)
with open(os.path.join(scratch_dir, "all_texts_fixed.json"), "r", encoding="utf-8") as f:
    texts = json.load(f)

# Let's cluster geometry along X in the main drawing strip Y in [-92000, -45000]
# First, let's look at where AUMIFLAS1 / AUMIFLAS3 / saff / d80 / w140 / KB are located!
print("=== LAYER 'KB' (Kavei Binyan / Building Lines) ===")
for i, l in enumerate(data["lines_by_layer"].get("KB", [])):
    print(f"KB line {i}: ({l[0]:.1f}, {l[1]:.1f}) -> ({l[2]:.1f}, {l[3]:.1f})")

# Let's bin all wall segments (layer '4' and '8') in Y in [-91000, -70000] by X-intervals
x_pts = []
for layer in ['4', '8', 'PARK', 'D', '2']:
    for p in data['lwpolys_by_layer'].get(layer, []):
        for x, y in p:
            if -91000 <= y <= -74000 and -60000 <= x <= 15000:
                x_pts.append((x, y, layer))
    for l in data['lines_by_layer'].get(layer, []):
        if -91000 <= l[1] <= -74000 and -60000 <= l[0] <= 15000:
            x_pts.append((l[0], l[1], layer))

# Sort x_pts by X and find gaps > 400 units (4 meters)
xs_sorted = sorted(set(round(p[0], 1) for p in x_pts))
clusters = []
if xs_sorted:
    cur_start = xs_sorted[0]
    cur_end = xs_sorted[0]
    for x in xs_sorted[1:]:
        if x - cur_end > 450:
            clusters.append((cur_start, cur_end))
            cur_start = x
        cur_end = x
    clusters.append((cur_start, cur_end))

print(f"\nFound {len(clusters)} X-clusters in Y=[-91000, -74000]:")
for idx, (xmin, xmax) in enumerate(clusters):
    c_pts = [p for p in x_pts if xmin <= p[0] <= xmax]
    if len(c_pts) < 10:
        continue
    ymin = min(p[1] for p in c_pts)
    ymax = max(p[1] for p in c_pts)
    # Find texts inside or near this cluster
    c_texts = [t for t in texts if (xmin - 300) <= t['x'] <= (xmax + 300) and (ymin - 800) <= t['y'] <= (ymax + 800)]
    sample_heb = []
    for t in c_texts:
        h = t['heb'].strip()
        if len(h) >= 2 and h not in sample_heb:
            sample_heb.append(f"{h} ({t['val']})")
    # Also find elevation markers (AUMIFLAS)
    miflas_ins = [ins for ins in data['inserts'] if ins['block'].startswith('AUMIFLAS') and (xmin - 200) <= ins['x'] <= (xmax + 200) and (ymin - 500) <= ins['y'] <= (ymax + 500)]
    print(f"Cluster {idx:2d}: X=[{xmin:8.1f}, {xmax:8.1f}] (W={xmax-xmin:6.1f}), Y=[{ymin:8.1f}, {ymax:8.1f}] (H={ymax-ymin:6.1f}) | {len(c_pts):4d} pts | {len(c_texts):3d} texts | {len(miflas_ins):2d} miflas")
    print("   Sample texts:", sample_heb[:25])
