import os
import json

scratch_dir = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch"
with open(os.path.join(scratch_dir, "dwg_frames_and_data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

SHX_MAP = {
    't': 'א', 'c': 'ב', 'd': 'ג', 's': 'ד', 'v': 'ה', 'u': 'ו', 'z': 'ז',
    'j': 'ח', 'y': 'ט', 'h': 'י', 'f': 'כ', 'k': 'ל', 'n': 'מ', 'b': 'נ',
    'x': 'ס', 'g': 'ע', 'p': 'פ', 'm': 'צ', 'e': 'ק', 'r': 'ר', 'a': 'ש',
    ',': 'ת', 'l': 'ך', 'o': 'ם', 'i': 'ן', ';': 'ף', '.': 'ץ'
}

def decode_shx_hebrew(s):
    if not s:
        return ""
    # If already contains unicode Hebrew, return as is
    if any('\u0590' <= ch <= '\u05FF' for ch in s):
        return s
    # Check if mostly lowercase letters/punctuation typical of SHX Hebrew
    # Only decode lowercase letters and , ; . if adjacent to letters
    out = []
    for ch in s:
        if ch in SHX_MAP:
            out.append(SHX_MAP[ch])
        else:
            out.append(ch)
    return "".join(out)

texts = data["all_texts"]
for t in texts:
    t["heb"] = decode_shx_hebrew(t["val"])

# Find all floor/elevation titles (e.g. containing קומה, קומת, מרתף, קרקע, גג, חזית, חתך, תכנית)
keywords = ["קומה", "קומות", "מרתף", "קרקע", "גג", "חזית", "חתך", "תכנית", "פיתוח", "חניה"]
title_texts = []
for t in texts:
    heb = t["heb"]
    if any(kw in heb for kw in keywords) or t["h"] >= 40:
        title_texts.append(t)

# Sort by Y descending, then X
title_texts.sort(key=lambda x: (-x["y"], x["x"]))

print(f"Found {len(title_texts)} title/header texts:")
for t in title_texts:
    if any(kw in t["heb"] for kw in keywords):
        print(f"  [{t['x']:9.1f}, {t['y']:9.1f}] H={t['h']:5.1f} L={t['layer']:12s} | {t['heb']}  (raw: {t['val']})")

with open(os.path.join(scratch_dir, "decoded_titles.json"), "w", encoding="utf-8") as f:
    json.dump(title_texts, f, ensure_ascii=False, indent=2)
