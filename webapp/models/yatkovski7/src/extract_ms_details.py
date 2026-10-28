import os
import json
import aspose.cad as cad
import aspose.pycore as pycore

scratch_dir = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch"
dwg_path = r"c:\Users\guyku\Downloads\yatkovski7-100-20 (2).dwg"

img = cad.Image.load(dwg_path)
cimg = pycore.cast(cad.fileformats.cad.CadImage, img)
blocks = dict(zip(cimg.block_entities.keys, cimg.block_entities.values))
ms = pycore.cast(cad.fileformats.cad.cadobjects.CadBlockEntity, blocks["*Model_Space"])

co = cad.fileformats.cad.cadobjects

all_texts = []
frames = []
lines_by_layer = {}
lwpolys_by_layer = {}
inserts = []

for ent in ms.entities:
    tname = ent.type_name.name
    lname = str(getattr(ent, 'layer_name', ''))
    if tname == "TEXT":
        try:
            c = pycore.cast(co.CadText, ent)
            val = getattr(c, 'default_value', '')
            pt = getattr(c, 'first_alignment_point', None) or getattr(c, 'second_alignment_point', None)
            all_texts.append({
                "type": "TEXT",
                "layer": lname,
                "val": str(val),
                "x": round(pt.x, 2) if pt else 0,
                "y": round(pt.y, 2) if pt else 0,
                "h": round(getattr(c, 'text_height', 0), 2)
            })
        except Exception:
            pass
    elif tname == "MTEXT":
        try:
            c = pycore.cast(co.CadMText, ent)
            val = getattr(c, 'full_clear_text', None) or getattr(c, 'text', '')
            pt = getattr(c, 'insertion_point', None)
            all_texts.append({
                "type": "MTEXT",
                "layer": lname,
                "val": str(val),
                "x": round(pt.x, 2) if pt else 0,
                "y": round(pt.y, 2) if pt else 0,
                "h": round(getattr(c, 'initial_text_height', 0), 2)
            })
        except Exception:
            pass
    elif tname == "DIMENSION":
        try:
            c = pycore.cast(co.CadDimensionBase, ent)
            val = getattr(c, 'text', '')
            pt = getattr(c, 'text_point', None) or getattr(c, 'definition_point', None)
            all_texts.append({
                "type": "DIM",
                "layer": lname,
                "val": str(val),
                "x": round(pt.x, 2) if pt else 0,
                "y": round(pt.y, 2) if pt else 0,
                "h": 0
            })
        except Exception:
            pass
    elif tname == "LWPOLYLINE":
        try:
            c = pycore.cast(co.CadLwPolyline, ent)
            pts = [[round(p.x, 2), round(p.y, 2)] for p in c.coordinates]
            if lname == "frame":
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
                frames.append({
                    "min_x": min(xs), "max_x": max(xs),
                    "min_y": min(ys), "max_y": max(ys),
                    "w": round(max(xs) - min(xs), 2),
                    "h": round(max(ys) - min(ys), 2)
                })
            lwpolys_by_layer.setdefault(lname, []).append(pts)
        except Exception:
            pass
    elif tname == "LINE":
        try:
            c = pycore.cast(co.CadLine, ent)
            p1 = c.first_point
            p2 = c.second_point
            lines_by_layer.setdefault(lname, []).append([
                round(p1.x, 2), round(p1.y, 2), round(p2.x, 2), round(p2.y, 2)
            ])
        except Exception:
            pass
    elif tname == "INSERT":
        try:
            c = pycore.cast(co.CadInsertObject, ent)
            pt = c.insertion_point
            # also check attributes if any
            inserts.append({
                "block": c.name,
                "layer": lname,
                "x": round(pt.x, 2),
                "y": round(pt.y, 2),
                "sx": round(c.scale_x, 4),
                "sy": round(c.scale_y, 4),
                "rot": round(c.rotation_angle, 2)
            })
        except Exception:
            pass

# Sort frames from top to bottom (descending Y)
frames.sort(key=lambda f: -f["max_y"])
for idx, f in enumerate(frames):
    f["frame_id"] = idx + 1
    f_texts = [t for t in all_texts if f["min_x"] - 200 <= t["x"] <= f["max_x"] + 200 and f["min_y"] - 200 <= t["y"] <= f["max_y"] + 200 and t["val"] and t["val"] != "None"]
    # Sort by height descending to find titles
    large_texts = sorted([t for t in f_texts if t["h"] >= 20 or "KOTERET" in t["layer"] or "TXT" in t["layer"]], key=lambda x: -x["h"])
    f["text_count"] = len(f_texts)
    f["titles"] = [f"{t['val']} (L:{t['layer']}, H:{t['h']})" for t in large_texts[:25]]
    f["sample_texts"] = [t["val"] for t in f_texts[:40]]
    print(f"Frame #{idx+1}: X[{f['min_x']}..{f['max_x']}] Y[{f['min_y']}..{f['max_y']}] ({f['w']}x{f['h']}) - {len(f_texts)} texts | Titles: {f['titles'][:6]}")

with open(os.path.join(scratch_dir, "dwg_frames_and_data.json"), "w", encoding="utf-8") as f_out:
    json.dump({
        "frames": frames,
        "all_texts": all_texts,
        "lwpolys_by_layer": lwpolys_by_layer,
        "lines_by_layer": lines_by_layer,
        "inserts": inserts
    }, f_out, ensure_ascii=False, indent=2)
print("Saved dwg_frames_and_data.json")
