import os
import sys
import json
import math
import aspose.cad as cad
import aspose.pycore as pycore

sys.stdout.reconfigure(encoding='utf-8')

scratch_dir = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch"
with open(os.path.join(scratch_dir, "dwg_frames_and_data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

PLANS_ANCHORS = {
    "basement":   (  1013.29, -76113.86),
    "ground":     ( -2352.16, -77276.82),
    "floor_1":    ( -6064.08, -77254.11),
    "floor_2":    ( -8727.65, -77254.11),
    "floors_3_4": (-11342.74, -77254.11),
    "floor_5":    (-14017.36, -77254.11),
    "floor_6":    (-16700.74, -77254.11),
    "roofs":      (-19350.92, -77254.11),
    "upper_roof": (-21975.32, -77254.11),
}

for pname, (ax, ay) in PLANS_ANCHORS.items():
    print(f"\n==================== {pname} ====================")
    ins_list = []
    for ins in data['inserts']:
        ix = (ins['x'] - ax) / 100.0
        iy = -(ins['y'] - ay) / 100.0
        if -12.5 <= ix <= 12.5 and -14.0 <= iy <= 20.0:
            ins_list.append((ins['layer'], ins['block'], round(ix, 2), round(iy, 2), round(ins['rot'], 1), round(ins['sx'], 2), round(ins['sy'], 2)))
    ins_list.sort()
    for l, b, ix, iy, rot, sx, sy in ins_list:
        if l in ('4', '8', 'PARK', 'rehut', 'FURN', 'SANIT', '2', 'M-Prat', '1-solar', 'KONTUR', 'Y-Tnua'):
            print(f"  L={l:10s} | Block={b:18s} | pos=({ix:6.2f}, {iy:6.2f}) | rot={rot:5.1f} | scale=({sx},{sy})")
