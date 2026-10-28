import json
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch\dwg_frames_and_data.json', encoding='utf-8') as f:
    data = json.load(f)

SHX_MAP = {'t':'א','c':'ב','d':'ג','s':'ד','v':'ה','u':'ו','z':'ז','j':'ח','y':'ט','h':'י','f':'כ','k':'ל','n':'מ','b':'נ','x':'ס','g':'ע','p':'פ','m':'צ','e':'ק','r':'ר','a':'ש',',':'ת','l':'ך','o':'ם','i':'ן',';':'ף','.':'ץ'}

def decode_shx(s):
    if any('\u0590' <= ch <= '\u05FF' for ch in s):
        return s
    res = ''.join(SHX_MAP.get(ch.lower(), ch) for ch in s)
    return res[::-1]

print("=== ALL TEXTS ON LAYER St-3 OR LARGE TEXTS ===")
for t in data['all_texts']:
    dec = decode_shx(t['val'])
    if t['layer'] in ['St-3', 'KOTERET1', 'KOTERET2'] or any(w in dec for w in ['תוכנית', 'תכנית', 'קומה', 'קומת', 'מרתף', 'קרקע', 'גג', 'חזית', 'חתך']):
        if t.get('h', 0) >= 18 or t['layer'] == 'St-3':
            print(f"{t['layer']:10s} | ({t['x']:9.1f}, {t['y']:9.1f}) | H={t.get('h',0):5.1f} | {dec}  [raw: {t['val']}]")

print("\n=== INSERTS SUMMARY ===")
ins_blocks = Counter((ins['block'], ins['layer']) for ins in data['inserts'])
for (b, l), c in ins_blocks.most_common(40):
    sample_coords = [(round(ins['x'], 1), round(ins['y'], 1)) for ins in data['inserts'] if ins['block'] == b and ins['layer'] == l][:5]
    print(f"Block: {b:20s} | Layer: {l:15s} | Count: {c:4d} | Coords: {sample_coords}")
