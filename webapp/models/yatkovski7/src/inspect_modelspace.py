import os
import json
from collections import Counter
import aspose.cad as cad
import aspose.pycore as pycore

scratch_dir = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch"
dwg_path = r"c:\Users\guyku\Downloads\yatkovski7-100-20 (2).dwg"

img = cad.Image.load(dwg_path)
cimg = pycore.cast(cad.fileformats.cad.CadImage, img)

blocks = dict(zip(cimg.block_entities.keys, cimg.block_entities.values))
print("Special blocks:", [k for k in blocks.keys() if k.startswith("*")])

def extract_from_iterable(ent_iter):
    t_counts = Counter()
    l_counts = Counter()
    texts = []
    inserts = []
    for ent in ent_iter:
        tname = ent.type_name.name
        lname = str(getattr(ent, 'layer_name', ''))
        t_counts[tname] += 1
        l_counts[lname] += 1
        if tname == "TEXT":
            try:
                cent = pycore.cast(cad.fileformats.cad.cadobjects.CadText, ent)
                val = cent.default_value
                pt = cent.first_alignment_point
                texts.append({"type": "TEXT", "layer": lname, "val": val, "x": round(pt.x, 2), "y": round(pt.y, 2), "h": round(cent.text_height, 2)})
            except Exception as e:
                pass
        elif tname == "MTEXT":
            try:
                cent = pycore.cast(cad.fileformats.cad.cadobjects.CadMText, ent)
                val = cent.full_clear_text or cent.text
                pt = cent.insertion_point
                texts.append({"type": "MTEXT", "layer": lname, "val": val, "x": round(pt.x, 2), "y": round(pt.y, 2)})
            except Exception as e:
                pass
        elif tname == "INSERT":
            try:
                cent = pycore.cast(cad.fileformats.cad.cadobjects.CadInsertObject, ent)
                pt = cent.insertion_point
                inserts.append({
                    "block": cent.name,
                    "layer": lname,
                    "x": round(pt.x, 2),
                    "y": round(pt.y, 2),
                    "sx": round(cent.scale_x, 4),
                    "sy": round(cent.scale_y, 4),
                    "rot": round(cent.rotation_angle, 2)
                })
            except Exception as e:
                pass
    return t_counts, l_counts, texts, inserts

print("--- PaperSpace (cimg.entities) ---")
ps_t, ps_l, ps_texts, ps_inserts = extract_from_iterable(cimg.entities)
print("PS types:", ps_t.most_common(10))
print("PS texts:", ps_texts)
print("PS inserts:", ps_inserts)

for ms_key in [k for k in blocks.keys() if "Model" in k or "MODEL" in k or "Paper" in k or "PAPER" in k]:
    blk = pycore.cast(cad.fileformats.cad.cadobjects.CadBlockEntity, blocks[ms_key])
    ms_t, ms_l, ms_texts, ms_inserts = extract_from_iterable(blk.entities)
    print(f"--- Block {ms_key} ---")
    print("Types:", ms_t.most_common(15))
    print("Top Layers:", ms_l.most_common(25))
    print("Texts count:", len(ms_texts), "Inserts count:", len(ms_inserts))
    with open(os.path.join(scratch_dir, f"dwg_{ms_key.strip('*')}.json"), "w", encoding="utf-8") as f:
        json.dump({
            "types": dict(ms_t),
            "layers": dict(ms_l.most_common(100)),
            "texts": ms_texts,
            "inserts": ms_inserts
        }, f, ensure_ascii=False, indent=2)
