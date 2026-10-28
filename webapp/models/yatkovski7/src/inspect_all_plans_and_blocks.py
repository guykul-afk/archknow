import os
import sys
import json
import aspose.cad as cad
import aspose.pycore as pycore

sys.stdout.reconfigure(encoding='utf-8')

scratch_dir = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch"
with open(os.path.join(scratch_dir, "dwg_frames_and_data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== ALL KB LINES ===")
for i, l in enumerate(data["lines_by_layer"].get("KB", [])):
    print(f"KB {i:2d}: ({l[0]:9.2f}, {l[1]:9.2f}) -> ({l[2]:9.2f}, {l[3]:9.2f}) | dx={l[2]-l[0]:7.2f}, dy={l[3]-l[1]:7.2f}")

# Let's check why St-3 texts had (0,0) in CadText by inspecting one St-3 entity in aspose.cad
dwg_path = r"c:\Users\guyku\Downloads\yatkovski7-100-20 (2).dwg"
img = cad.Image.load(dwg_path)
cimg = pycore.cast(cad.fileformats.cad.CadImage, img)
blocks = dict(zip(cimg.block_entities.keys, cimg.block_entities.values))
ms = pycore.cast(cad.fileformats.cad.cadobjects.CadBlockEntity, blocks["*Model_Space"])
co = cad.fileformats.cad.cadobjects

for ent in ms.entities:
    if ent.type_name.name == "TEXT" and str(getattr(ent, 'layer_name', '')) == "St-3":
        c = pycore.cast(co.CadText, ent)
        attrs = {}
        for a in dir(c):
            if not a.startswith('_'):
                try:
                    v = getattr(c, a)
                    if hasattr(v, 'x') and hasattr(v, 'y'):
                        attrs[a] = (v.x, v.y, getattr(v, 'z', 0))
                    elif isinstance(v, (int, float, str)):
                        attrs[a] = v
                except Exception:
                    pass
        print("\nSample St-3 CadText attributes:", attrs)
        break

# Also check if there are ATTRIB entities inside INSERTs (like AUMIFLAS3 or title blocks!)
attrib_samples = []
for ent in ms.entities:
    tname = ent.type_name.name
    if tname == "INSERT":
        ins = pycore.cast(co.CadInsertObject, ent)
        # Check child objects of insert if any
        child_objs = getattr(ins, 'child_objects', None)
        if child_objs:
            for ch in child_objs:
                ch_type = ch.type_name.name if hasattr(ch, 'type_name') else str(type(ch))
                if ch_type in ("ATTRIB", "TEXT"):
                    try:
                        att = pycore.cast(co.CadAttrib, ch)
                        val = getattr(att, 'default_value', '')
                        pt = getattr(att, 'first_alignment_point', None) or getattr(att, 'second_alignment_point', None)
                        attrib_samples.append({
                            "block": ins.name,
                            "ins_x": round(ins.insertion_point.x, 2),
                            "ins_y": round(ins.insertion_point.y, 2),
                            "val": val,
                            "tag": getattr(att, 'definition_tag_string', '')
                        })
                    except Exception:
                        pass

print(f"\nFound {len(attrib_samples)} ATTRIBs inside INSERTs! First 30:")
for a in attrib_samples[:30]:
    print("  ", a)

with open(os.path.join(scratch_dir, "insert_attribs.json"), "w", encoding="utf-8") as f:
    json.dump(attrib_samples, f, ensure_ascii=False, indent=2)
