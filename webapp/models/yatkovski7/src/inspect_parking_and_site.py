import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

scratch_dir = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch"
with open(os.path.join(scratch_dir, "dwg_frames_and_data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)
with open(os.path.join(scratch_dir, "all_texts_fixed.json"), "r", encoding="utf-8") as f:
    texts = json.load(f)

print("=== LAYER 'PARK' LWPOLYS & LINES ===")
for i, p in enumerate(data['lwpolys_by_layer'].get('PARK', [])):
    xs = [pt[0] for pt in p]
    ys = [pt[1] for pt in p]
    print(f"PARK poly {i:2d}: X=[{min(xs):8.1f}, {max(xs):8.1f}], Y=[{min(ys):8.1f}, {max(ys):8.1f}] (W={max(xs)-min(xs):5.1f}, H={max(ys)-min(ys):5.1f})")

print("\n=== ALL INSERTS ON LAYER 'PARK' OR 'Y-Tnua' ===")
for ins in data['inserts']:
    if 'PARK' in ins['layer'].upper() or 'TNUA' in ins['layer'].upper() or 'CAR' in ins['block'].upper():
        print(" ", ins)

# Wait: what is inside block 'tnua m 19-7-26' on layer 'Y-Tnua' at (-4342.37, -81570.88)?
# And what is inside block '12561101' on layer 'KONTUR' at (-3422.6, -78038.27) and (-57.19, -76875.31)?
import aspose.cad as cad
import aspose.pycore as pycore
dwg_path = r"c:\Users\guyku\Downloads\yatkovski7-100-20 (2).dwg"
img = cad.Image.load(dwg_path)
cimg = pycore.cast(cad.fileformats.cad.CadImage, img)
blocks = dict(zip(cimg.block_entities.keys, cimg.block_entities.values))
co = cad.fileformats.cad.cadobjects

for bname in ['tnua m 19-7-26', '12561101']:
    if bname in blocks:
        blk = pycore.cast(co.CadBlockEntity, blocks[bname])
        from collections import Counter
        tcounts = Counter(e.type_name.name for e in blk.entities)
        lcounts = Counter(str(getattr(e, 'layer_name', '')) for e in blk.entities)
        print(f"\nBlock '{bname}': types={dict(tcounts)}, layers={dict(lcounts)}")
        for e in blk.entities:
            if e.type_name.name in ('TEXT', 'MTEXT'):
                try:
                    c = pycore.cast(co.CadText, e)
                    p1 = getattr(c, 'first_alignment', None)
                    print(f"   TEXT in {bname}: L={e.layer_name} val={c.default_value} at ({p1.x if p1 else 0:.1f}, {p1.y if p1 else 0:.1f})")
                except Exception:
                    pass
