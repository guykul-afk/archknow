import sys
import json
import aspose.cad as cad
from aspose.pycore import cast
import aspose.cad.fileformats.cad.cadobjects as co

sys.stdout.reconfigure(encoding='utf-8')

dwg_path = r'c:\Users\guyku\Downloads\yatkovski7-100-20 (2).dwg'
img = cad.Image.load(dwg_path)
cimg = cast(cad.fileformats.cad.CadImage, img)
ms = cimg.block_entities['*Model_Space']

SHX_MAP = {'t':'א','c':'ב','d':'ג','s':'ד','v':'ה','u':'ו','z':'ז','j':'ח','y':'ט','h':'י','f':'כ','k':'ל','n':'מ','b':'נ','x':'ס','g':'ע','p':'פ','m':'צ','e':'ק','r':'ר','a':'ש',',':'ת','l':'ך','o':'ם','i':'ן',';':'ף','.':'ץ'}
def decode_shx(s):
    if not s:
        return ''
    if any('\u0590' <= ch <= '\u05FF' for ch in s):
        return s
    res = ''.join(SHX_MAP.get(ch.lower(), ch) for ch in s)
    return res[::-1]

st3_texts = []
all_real_texts = []

for e in ms.entities:
    tname = e.type_name.name if hasattr(e.type_name, 'name') else str(e.type_name)
    if tname == 'TEXT':
        c = cast(co.CadText, e)
        x, y = c.first_alignment_point.x, c.first_alignment_point.y
        if abs(x) < 1e-3 and abs(y) < 1e-3 and hasattr(c, 'second_alignment_point') and c.second_alignment_point:
            x, y = c.second_alignment_point.x, c.second_alignment_point.y
        val = c.default_value or ''
        dec = decode_shx(val)
        item = {'layer': e.layer_name, 'x': round(x, 2), 'y': round(y, 2), 'h': round(c.text_height, 2), 'raw': val, 'dec': dec}
        all_real_texts.append(item)
        if e.layer_name == 'St-3' or c.text_height >= 35:
            st3_texts.append(item)
    elif tname == 'MTEXT':
        c = cast(co.CadMText, e)
        x, y = c.insertion_point.x, c.insertion_point.y
        val = c.text or ''
        dec = decode_shx(val)
        item = {'layer': e.layer_name, 'x': round(x, 2), 'y': round(y, 2), 'h': round(c.initial_text_height, 2), 'raw': val, 'dec': dec}
        all_real_texts.append(item)
        if e.layer_name == 'St-3' or c.initial_text_height >= 35:
            st3_texts.append(item)

st3_texts.sort(key=lambda item: (-item['x'], item['y']))
print(f"Found {len(st3_texts)} title texts:")
for t in st3_texts:
    if -45000 <= t['x'] <= 15000 and -95000 <= t['y'] <= -45000:
        print(f"L:{t['layer']:10s} | ({t['x']:9.1f}, {t['y']:9.1f}) | H={t['h']:5.1f} | {t['dec']}  [{t['raw']}]")

with open('all_texts_with_second_align.json', 'w', encoding='utf-8') as f:
    json.dump(all_real_texts, f, ensure_ascii=False, indent=2)
