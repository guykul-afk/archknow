import os
import json
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

scratch_dir = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch"
base_dir = r"G:\Shared drives\פרויקטים שוטפים\פרויקטים בביצוע\יטקובסקי 7"

# 1. Print pages from 410-1272517 and architectural PDFs in pdfs_text_dump.json
with open(os.path.join(scratch_dir, "pdfs_text_dump.json"), "r", encoding="utf-8") as f:
    dump = json.load(f)

with open(os.path.join(scratch_dir, "taba_and_plans_text.txt"), "w", encoding="utf-8") as out:
    for k, v in dump.items():
        if "מפרט טכני" in k:
            continue
        out.write(f"=== FILE: {k} ({v['page_count']} pages) ===\n")
        for p in v["pages"]:
            out.write(p + "\n")

# 2. Extract text from docx files (combination agreement & advisor list)
docx_files = [
    r"הסכם קומבינציה\משא ומתן\13.6.2023\בן אהרון מעודכן 18.6.2023.docx",
    r"ניהול ותיאום\רשימת יועצים יטקובסקי 7.docx",
]
with open(os.path.join(scratch_dir, "docx_texts.txt"), "w", encoding="utf-8") as out:
    for rel in docx_files:
        p = os.path.join(base_dir, rel)
        if os.path.exists(p):
            out.write(f"=== DOCX: {rel} ===\n")
            with zipfile.ZipFile(p) as z:
                xml_content = z.read("word/document.xml")
                tree = ET.fromstring(xml_content)
                paragraphs = []
                for elem in tree.iter():
                    if elem.tag.endswith("}p"):
                        texts = [t.text for t in elem.iter() if t.tag.endswith("}t") and t.text]
                        if texts:
                            paragraphs.append("".join(texts))
                out.write("\n".join(paragraphs) + "\n\n")

# 3. Fast stream-scan of yatkovski7_100_20.dxf ENTITIES section
dxf_path = os.path.join(scratch_dir, "yatkovski7_100_20.dxf")
print("Scanning DXF:", dxf_path)

in_entities = False
entity_counts = Counter()
layer_counts = Counter()
texts_found = []

with open(dxf_path, "r", encoding="utf-8", errors="ignore") as f:
    prev_code = None
    curr_entity = None
    curr_layer = None
    curr_text = None
    curr_x = None
    curr_y = None
    section_esper = False
    while True:
        code_line = f.readline()
        if not code_line:
            break
        val_line = f.readline()
        if not val_line:
            break
        code = code_line.strip()
        val = val_line.strip()
        if code == "0" and val == "SECTION":
            section_esper = True
            continue
        if section_esper and code == "2":
            section_esper = False
            if val == "ENTITIES":
                in_entities = True
                print("Entered ENTITIES section!")
            elif in_entities:
                break
            continue
        if not in_entities:
            continue
        if code == "0":
            if curr_entity in ("TEXT", "MTEXT", "ATTRIB") and curr_text:
                texts_found.append({
                    "type": curr_entity,
                    "layer": curr_layer,
                    "text": curr_text,
                    "x": curr_x,
                    "y": curr_y
                })
            if val == "ENDSEC":
                break
            curr_entity = val
            entity_counts[curr_entity] += 1
            curr_layer = None
            curr_text = None
            curr_x = None
            curr_y = None
        elif code == "8":
            if curr_layer is None:
                curr_layer = val
                layer_counts[val] += 1
        elif code == "1":
            curr_text = val
        elif code == "10" and curr_x is None:
            try:
                curr_x = round(float(val), 2)
            except:
                pass
        elif code == "20" and curr_y is None:
            try:
                curr_y = round(float(val), 2)
            except:
                pass

dxf_summary = {
    "entity_counts": dict(entity_counts.most_common(50)),
    "layer_counts": dict(layer_counts.most_common(100)),
    "texts_count": len(texts_found),
    "sample_texts": texts_found[:500]
}
with open(os.path.join(scratch_dir, "dxf_summary.json"), "w", encoding="utf-8") as f:
    json.dump(dxf_summary, f, ensure_ascii=False, indent=2)
with open(os.path.join(scratch_dir, "dxf_all_texts.json"), "w", encoding="utf-8") as f:
    json.dump(texts_found, f, ensure_ascii=False, indent=2)

print("Done! Entity counts:", entity_counts.most_common(15))
print("Top layers:", layer_counts.most_common(20))
print("Total texts found:", len(texts_found))
