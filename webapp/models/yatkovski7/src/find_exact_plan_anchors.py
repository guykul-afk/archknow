import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

scratch_dir = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch"
with open(os.path.join(scratch_dir, "dwg_frames_and_data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)
with open(os.path.join(scratch_dir, "all_texts_fixed.json"), "r", encoding="utf-8") as f:
    texts = json.load(f)

# Let's inspect the Elevator door block or "טיפוס 1" text or KB lines or elevator shaft walls in each of the 9 plans!
# Notice in plans_report.txt:
# Every floor plan has the text "טיפוס 1" (raw="yhpux 1") inside the elevator shaft!
# Let's check the exact coordinates of "טיפוס 1" and "מעלית" and the elevator shaft lines in each plan!
print("=== 'טיפוס 1' (ELEVATOR TYPE 1) COORDS ACROSS ALL PLANS ===")
for t in sorted([t for t in texts if t["val"] == "yhpux 1"], key=lambda x: -x["x"]):
    print(f"  טיפוס 1 at ({t['x']:9.2f}, {t['y']:9.2f})")

print("\n=== 'מעלית' COORDS ACROSS ALL PLANS ===")
for t in sorted([t for t in texts if t["val"] == "ngkh," and -23000 <= t["x"] <= 2000 and -80000 <= t["y"] <= -75000], key=lambda x: -x["x"]):
    print(f"  מעלית at ({t['x']:9.2f}, {t['y']:9.2f})")

# Even better: let's find the exact geometric lines of the elevator shaft or KB lines in each plan!
# In floor_1..upper_roof, look at KB lines:
# floor_1: KB 0: (-6833.97, -78830.86) -> (-5775.92, -78830.86)
# floor_2: KB 9: (-9497.54, -78830.86) -> (-8439.49, -78830.86)  (dX = -2663.57)
# floors_3_4: KB 12: (-12112.62, -78830.86) -> (-11054.57, -78830.86) (dX = -2615.08)
# floor_5: KB 2: (-14787.25, -78830.86) -> (-13729.20, -78830.86) (dX = -2674.63)
# floor_6: KB 5: (-16363.83, -76595.22) -> (-17511.30, -76837.14)
# roofs: KB 15: (-19019.01, -76595.22) -> (-20166.48, -76837.14)
# upper_roof: KB 16: (-21643.41, -76595.22) -> (-22790.89, -76837.14)

# What about basement and ground? Let's find the elevator core box in basement, ground, floor_1..upper_roof!
# Near "מעלית" (x_m, y_m), let's find horizontal and vertical lines on layer '4' or '8' within 250 cm of "מעלית"!
plans_m = [
    ("basement", 1065.81, -76177.32),
    ("ground", -2312.45, -77245.54),
    ("floor_1", -6035.63, -77235.37),
    ("floor_2", -8699.20, -77235.37),
    ("floors_3_4", -11314.28, -77235.37),
    ("floor_5", -13973.07, -77229.29),
    ("floor_6", -16661.42, -77218.57),
    ("roofs", -19316.60, -77218.57),
    ("upper_roof", -21941.00, -77218.57),
]

for pname, xm, ym in plans_m:
    # Check inserts near (xm, ym)
    near_ins = [ins for ins in data["inserts"] if abs(ins["x"] - xm) < 350 and abs(ins["y"] - ym) < 350]
    print(f"\nPlan {pname:12s} near ({xm:8.2f}, {ym:8.2f}):")
    for ins in near_ins[:12]:
        print(f"  Insert {ins['block']:15s} L={ins['layer']:10s} at ({ins['x']:9.2f}, {ins['y']:9.2f})")
