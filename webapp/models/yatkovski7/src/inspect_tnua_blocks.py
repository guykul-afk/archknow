import os
import sys
import json
import math
import aspose.cad as cad
import aspose.pycore as pycore

sys.stdout.reconfigure(encoding='utf-8')

dwg_path = r"c:\Users\guyku\Downloads\yatkovski7-100-20 (2).dwg"
img = cad.Image.load(dwg_path)
cimg = pycore.cast(cad.fileformats.cad.CadImage, img)
blocks = dict(zip(cimg.block_entities.keys, cimg.block_entities.values))
co = cad.fileformats.cad.cadobjects

def transform_pt(px, py, ins_x, ins_y, sx, sy, rot_deg):
    rad = math.radians(rot_deg)
    cx, cy = math.cos(rad), math.sin(rad)
    x1, y1 = px * sx, py * sy
    rx = x1 * cx - y1 * cy + ins_x
    ry = x1 * cy + y1 * cx + ins_y
    return rx, ry

# Basement anchor: (1013.29, -76113.86)
# Ground #2 anchor: (-2352.16, -88604.96)  (Notice Ground #1 is at -77276.82 and Ground #2 is shifted by dY = -11328.14!)
configs = [
    ("tnua m 19-7-26", -4342.37, -81570.88, 1.0, 1.0, 13.56, 1013.29, -76113.86),
    ("tnua k 19-7-26", -11362.17, -84036.83, 1.0, 1.0, 13.56, -2352.16, -88604.96),
]

for bname, ix, iy, sx, sy, rot, ax, ay in configs:
    blk = pycore.cast(co.CadBlockEntity, blocks[bname])
    bp = getattr(blk, 'base_point', None)
    bpx, bpy = (bp.x, bp.y) if bp else (0.0, 0.0)
    print(f"\n=== Block '{bname}' (base_point=({bpx:.1f},{bpy:.1f})) ===")
    for e in blk.entities:
        tname = e.type_name.name
        if tname == "INSERT":
            ins = pycore.cast(co.CadInsertObject, e)
            px, py = ins.insertion_point.x - bpx, ins.insertion_point.y - bpy
            mx, my = transform_pt(px, py, ix, iy, sx, sy, rot)
            lx, ly = (mx - ax)/100.0, -(my - ay)/100.0
            print(f"  Sub-Insert: {ins.name:18s} L={e.layer_name:12s} | MS=({mx:8.1f}, {my:8.1f}) | local=({lx:6.2f}, {ly:6.2f}) rot={ins.rotation_angle + rot:.1f}")
        elif tname == "TEXT":
            c = pycore.cast(co.CadText, e)
            p1 = getattr(c, 'first_alignment', None)
            if p1:
                px, py = p1.x - bpx, p1.y - bpy
                mx, my = transform_pt(px, py, ix, iy, sx, sy, rot)
                lx, ly = (mx - ax)/100.0, -(my - ay)/100.0
                print(f"  Text: {c.default_value:18s} L={e.layer_name:12s} | MS=({mx:8.1f}, {my:8.1f}) | local=({lx:6.2f}, {ly:6.2f})")
