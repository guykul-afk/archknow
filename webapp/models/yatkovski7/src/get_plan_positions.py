import os
import json
import aspose.cad as cad
import aspose.pycore as pycore

scratch_dir = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch"
dwg_path = r"c:\Users\guyku\Downloads\yatkovski7-100-20 (2).dwg"

SHX_MAP = {
    't': 'א', 'c': 'ב', 'd': 'ג', 's': 'ד', 'v': 'ה', 'u': 'ו', 'z': 'ז',
    'j': 'ח', 'y': 'ט', 'h': 'י', 'f': 'כ', 'k': 'ל', 'n': 'מ', 'b': 'נ',
    'x': 'ס', 'g': 'ע', 'p': 'פ', 'm': 'צ', 'e': 'ק', 'r': 'ר', 'a': 'ש',
    ',': 'ת', 'l': 'ך', 'o': 'ם', 'i': 'ן', ';': 'ף', '.': 'ץ'
}

def decode_shx_hebrew(s):
    if not s:
        return ""
    if any('\u0590' <= ch <= '\u05FF' for ch in s):
        return s
    return "".join(SHX_MAP.get(ch, ch) for ch in s)

img = cad.Image.load(dwg_path)
cimg = pycore.cast(cad.fileformats.cad.CadImage, img)
blocks = dict(zip(cimg.block_entities.keys, cimg.block_entities.values))
ms = pycore.cast(cad.fileformats.cad.cadobjects.CadBlockEntity, blocks["*Model_Space"])
co = cad.fileformats.cad.cadobjects

all_texts = []
for ent in ms.entities:
    tname = ent.type_name.name
    lname = str(getattr(ent, 'layer_name', ''))
    if tname == "TEXT":
        try:
            c = pycore.cast(co.CadText, ent)
            val = str(getattr(c, 'default_value', ''))
            p1 = getattr(c, 'first_alignment_point', None)
            p2 = getattr(c, 'second_alignment_point', None)
            pt = p1
            if (not pt or (abs(pt.x) < 1e-3 and abs(pt.y) < 1e-3)) and p2 and (abs(p2.x) > 1e-3 or abs(p2.y) > 1e-3):
                pt = p2
            all_texts.append({
                "type": "TEXT",
                "layer": lname,
                "val": val,
                "heb": decode_shx_hebrew(val),
                "x": round(pt.x, 2) if pt else 0,
                "y": round(pt.y, 2) if pt else 0,
                "h": round(getattr(c, 'text_height', 0), 2)
            })
        except Exception:
            pass
    elif tname == "MTEXT":
        try:
            c = pycore.cast(co.CadMText, ent)
            val = str(getattr(c, 'full_clear_text', None) or getattr(c, 'text', ''))
            pt = getattr(c, 'insertion_point', None)
            all_texts.append({
                "type": "MTEXT",
                "layer": lname,
                "val": val,
                "heb": decode_shx_hebrew(val),
                "x": round(pt.x, 2) if pt else 0,
                "y": round(pt.y, 2) if pt else 0,
                "h": round(getattr(c, 'initial_text_height', 0), 2)
            })
        except Exception:
            pass

with open(os.path.join(scratch_dir, "all_texts_fixed.json"), "w", encoding="utf-8") as f:
    json.dump(all_texts, f, ensure_ascii=False, indent=2)

st3_texts = [t for t in all_texts if t["layer"] == "St-3" or t["h"] >= 45]
st3_texts.sort(key=lambda t: (-t["x"], -t["y"]))
for t in st3_texts:
    print(f"[{t['x']:10.2f}, {t['y']:10.2f}] H={t['h']:5.1f} L={t['layer']:12s} | raw={t['val']}")
