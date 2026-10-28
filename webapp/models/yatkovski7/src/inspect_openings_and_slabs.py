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

dwg_path = r"c:\Users\guyku\Downloads\yatkovski7-100-20 (2).dwg"
img = cad.Image.load(dwg_path)
cimg = pycore.cast(cad.fileformats.cad.CadImage, img)
blocks = dict(zip(cimg.block_entities.keys, cimg.block_entities.values))
co = cad.fileformats.cad.cadobjects

# Let's inspect the bounding boxes of door/window block definitions in DWG!
dw_block_names = ['D100', 'd80', 'd81', 'd110', 'd111', 'd120', 'w300', 'w140', 'w140h20', 'w160', 'w160h20', 'w200h20', 'w120', 'w80', 'w70', 'W100', 'wh3']
print("=== DOOR & WINDOW BLOCK DEFINITIONS BOUNDS ===")
for bname in dw_block_names:
    if bname in blocks:
        blk = pycore.cast(co.CadBlockEntity, blocks[bname])
        xs, ys = [], []
        for e in blk.entities:
            tname = e.type_name.name
            if tname == "LINE":
                l = pycore.cast(co.CadLine, e)
                xs.extend([l.first_point.x, l.second_point.x])
                ys.extend([l.first_point.y, l.second_point.y])
            elif tname == "LWPOLYLINE":
                p = pycore.cast(co.CadLwPolyline, e)
                for pt in p.coordinates:
                    xs.append(pt.x)
                    ys.append(pt.y)
        if xs:
            print(f"  {bname:10s}: X=[{min(xs):6.1f}, {max(xs):6.1f}], Y=[{min(ys):6.1f}, {max(ys):6.1f}]")

# Now let's print all door/window inserts per plan with their exact block bounds transformed to local meters!
PLANS_ANCHORS = {
    "basement":   (  1013.29, -76113.86),
    "ground":     ( -2352.16, -77276.82),
    "typical":    ( -6064.08, -77254.11),
    "floor_5":    (-14017.36, -77254.11),
    "penthouse":  (-16700.74, -77254.11),
    "roof_main":  (-19350.92, -77254.11),
}

for pname, (ax, ay) in PLANS_ANCHORS.items():
    print(f"\n=== OPENINGS IN {pname} ===")
    for ins in data['inserts']:
        bname = ins['block']
        if bname in dw_block_names:
            ix = (ins['x'] - ax) / 100.0
            iy = -(ins['y'] - ay) / 100.0
            if -12.0 <= ix <= 8.0 and -12.0 <= iy <= 19.0:
                print(f"  {bname:10s} at ({ix:6.2f}, {iy:6.2f}) rot={ins['rot']:5.1f} sx={ins['sx']:4.1f} sy={ins['sy']:4.1f}")
