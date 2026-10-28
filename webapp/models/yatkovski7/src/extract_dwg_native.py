import os
import json
from collections import Counter
import aspose.cad as cad
import aspose.pycore as pycore

scratch_dir = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch"
dwg_path = r"c:\Users\guyku\Downloads\yatkovski7-100-20 (2).dwg"

img = cad.Image.load(dwg_path)
cimg = pycore.cast(cad.fileformats.cad.CadImage, img)

print("Min:", cimg.min_point.x, cimg.min_point.y, "Max:", cimg.max_point.x, cimg.max_point.y)

type_counts = Counter()
layer_counts = Counter()
sample_by_type = {}
texts = []
inserts = []

for ent in cimg.entities:
    tname = str(getattr(ent, 'type_name', type(ent).__name__))
    lname = str(getattr(ent, 'layer_name', ''))
    type_counts[tname] += 1
    layer_counts[lname] += 1
    if tname not in sample_by_type:
        sample_by_type[tname] = [d for d in dir(ent) if not d.startswith('_')]

    if "TEXT" in tname.upper():
        # Try casting to CadText or CadMText
        val = None
        pt = None
        for cls in (cad.fileformats.cad.cadobjects.CadText, cad.fileformats.cad.cadobjects.CadMText):
            try:
                cent = pycore.cast(cls, ent)
                val = getattr(cent, 'default_value', None) or getattr(cent, 'full_clear_text', None) or getattr(cent, 'text', None)
                pt = getattr(cent, 'first_alignment_point', None) or getattr(cent, 'insertion_point', None)
                break
            except Exception:
                pass
        x = round(pt.x, 2) if pt else None
        y = round(pt.y, 2) if pt else None
        texts.append({"type": tname, "layer": lname, "val": str(val), "x": x, "y": y})
    elif "INSERT" in tname.upper():
        try:
            cent = pycore.cast(cad.fileformats.cad.cadobjects.CadInsertObject, ent)
            bname = str(getattr(cent, 'name', ''))
            pt = getattr(cent, 'insertion_point', None)
            sx = getattr(cent, 'scale_x', 1.0)
            sy = getattr(cent, 'scale_y', 1.0)
            rot = getattr(cent, 'rotation_angle', 0.0)
            x = round(pt.x, 2) if pt else None
            y = round(pt.y, 2) if pt else None
            inserts.append({"block": bname, "layer": lname, "x": x, "y": y, "sx": sx, "sy": sy, "rot": rot})
        except Exception:
            pass

print("Top entity types:", type_counts.most_common(25))
print("Top layers:", layer_counts.most_common(30))
print("Texts count:", len(texts), "Inserts count:", len(inserts))

with open(os.path.join(scratch_dir, "dwg_native_summary.json"), "w", encoding="utf-8") as f:
    json.dump({
        "min_point": [cimg.min_point.x, cimg.min_point.y],
        "max_point": [cimg.max_point.x, cimg.max_point.y],
        "type_counts": dict(type_counts.most_common(50)),
        "layer_counts": dict(layer_counts.most_common(100)),
        "sample_by_type": sample_by_type,
        "texts": texts,
        "inserts": inserts
    }, f, ensure_ascii=False, indent=2)
print("Saved dwg_native_summary.json")
