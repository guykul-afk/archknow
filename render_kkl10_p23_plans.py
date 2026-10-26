# -*- coding: utf-8 -*-
"""
Renders high-resolution 1:100 architectural floor plan PNGs for KKL 10 directly from
the latest Gramoshka CAD file (P-23: kkl10_gramoshka.dxf), matching AutoCAD Gramoshka
color conventions (blue structural RC walls, red interior partitions, dimension lines &
exact room dimensions 268x345, 264x345, 283x340, 2x 6-pax elevators, and 34 parking stalls
with NO basement transformer room).
"""

import collections
import math
import os
import re
from PIL import Image, ImageDraw, ImageFont

DXF_PATH = r"C:\Users\guyku\.gemini\antigravity\scratch\kkl10\kkl10_gramoshka.dxf"
OUT_DIR = r"c:\Users\guyku\archknow\webapp\uploads"

CANVAS_W = 1600
CANVAS_H = 2700
SCALE = 60.0  # pixels per meter
MARGIN_X = 140.0
MARGIN_TOP = 80.0


def bim_to_px(xbim, nbim):
    px = MARGIN_X + (xbim + 4.5) * SCALE
    py = MARGIN_TOP + (37.5 - nbim) * SCALE
    return round(px, 1), round(py, 1)


def decode_dxf_str(s):
    def repl_u(m):
        return chr(int(m.group(1), 16))
    s = re.sub(r'\\U\+([0-9A-Fa-f]{4})', repl_u, s)
    def repl_m(m):
        lo = int(m.group(2), 16)
        if 0xFA <= lo <= 0xFB:
            try:
                return bytes([lo]).decode('cp1255')
            except Exception:
                pass
        return ''
    s = re.sub(r'\\M\+5([0-9A-Fa-f]{2})([0-9A-Fa-f]{2})', repl_m, s)
    out = []
    for ch in s:
        o = ord(ch)
        if 0xE0 <= o <= 0xFA:
            out.append(chr(o - 0xE0 + 0x05D0))
        else:
            out.append(ch)
    s = ''.join(out)
    s = re.sub(r'\\f[^;]+;', '', s)
    s = re.sub(r'\\W[^;]+;', '', s)
    s = re.sub(r'\\H[^;]+;', '', s)
    s = re.sub(r'\\A[^;]+;', '', s)
    s = re.sub(r'\\C[^;]+;', '', s)
    s = s.replace('\\P', '\n').replace('\\X', '\n').replace('{', '').replace('}', '')
    return s.strip()


def bidi_visual(text):
    """Reverses Hebrew runs for Pillow rendering when libraqm is unavailable."""
    lines_out = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        # If line contains Hebrew characters, reverse word/char order appropriately
        if any('\u0590' <= c <= '\u05FF' for c in line):
            # Tokenize into Hebrew vs non-Hebrew (numbers/latin) runs
            tokens = re.findall(r'[\u0590-\u05FF"\']+|[0-9.,+\-*/xX×%()]+|\s+|[^\u0590-\u05FF0-9\s]+', line)
            rev_tokens = []
            for tok in reversed(tokens):
                if any('\u0590' <= c <= '\u05FF' for c in tok):
                    rev_tokens.append(tok[::-1])
                else:
                    rev_tokens.append(tok)
            lines_out.append(''.join(rev_tokens))
        else:
            lines_out.append(line)
    return '\n'.join(lines_out)


print("Loading kkl10_gramoshka.dxf...")
with open(DXF_PATH, 'r', encoding='utf-8', errors='replace') as f:
    lines = [l.rstrip('\r\n') for l in f]

i, n = 0, len(lines)
sec = None
cur_block = None
blocks = collections.defaultdict(list)
block_base = {}
entities = []


def read_entity(start_i):
    etype = lines[start_i - 1].strip()
    idx = start_i
    pairs = []
    while idx + 1 < n and lines[idx].strip() != '0':
        pairs.append((lines[idx].strip(), lines[idx + 1].strip()))
        idx += 2
    return etype, pairs, idx


while i + 1 < n:
    c, v = lines[i].strip(), lines[i + 1].strip()
    i += 2
    if c == '0' and v == 'SECTION' and i + 1 < n:
        sec = lines[i + 1].strip()
        i += 2
        continue
    if sec == 'BLOCKS':
        if c == '0' and v == 'BLOCK':
            bname = ''
            bx = by = 0.0
            while i + 1 < n and lines[i].strip() != '0':
                cc, vv = lines[i].strip(), lines[i + 1].strip()
                i += 2
                if cc == '2':
                    bname = vv
                elif cc == '10':
                    try:
                        bx = float(vv)
                    except Exception:
                        pass
                elif cc == '20':
                    try:
                        by = float(vv)
                    except Exception:
                        pass
            cur_block = bname
            block_base[bname] = (bx, by)
        elif c == '0' and v == 'ENDBLK':
            cur_block = None
        elif c == '0' and cur_block:
            etype, pairs, i = read_entity(i)
            blocks[cur_block].append((etype, pairs))
    elif sec == 'ENTITIES' and c == '0':
        if v == 'ENDSEC':
            sec = None
            continue
        etype, pairs, i = read_entity(i)
        entities.append((etype, pairs))

print(f"Loaded {len(blocks)} blocks and {len(entities)} entities.")


def parse_hatch_loops(pairs):
    loops = []
    idx = 0
    m = len(pairs)
    while idx < m:
        c, v = pairs[idx]
        if c == '93':
            num_edges = int(v)
            idx += 1
            pts = []
            edges_read = 0
            while idx < m and edges_read < num_edges:
                cc, vv = pairs[idx]
                if cc == '72':
                    edge_type = int(vv)
                    idx += 1
                    if edge_type == 1:
                        x1 = y1 = None
                        while idx < m and pairs[idx][0] in ('10', '20', '11', '21'):
                            ec, ev = pairs[idx]
                            if ec == '10':
                                x1 = float(ev)
                            elif ec == '20':
                                y1 = float(ev)
                            idx += 1
                        if x1 is not None and y1 is not None:
                            pts.append((x1, y1))
                    else:
                        while idx < m and pairs[idx][0] not in ('72', '97', '92'):
                            idx += 1
                    edges_read += 1
                elif cc == '10':
                    x1 = float(vv)
                    y1 = float(pairs[idx + 1][1]) if idx + 1 < m and pairs[idx + 1][0] == '20' else 0.0
                    pts.append((x1, y1))
                    idx += 2
                    if idx < m and pairs[idx][0] == '42':
                        idx += 1
                    edges_read += 1
                elif cc in ('97', '92', '75'):
                    break
                else:
                    idx += 1
            if len(pts) >= 3:
                loops.append(pts)
        else:
            idx += 1
    return loops


def transform_pt(px, py, bx, by, ix, iy, sx, sy, rot_rad):
    dx = (px - bx) * sx
    dy = (py - by) * sy
    c = math.cos(rot_rad)
    s = math.sin(rot_rad)
    return ix + dx * c - dy * s, iy + dx * s + dy * c


def extract_entity_segments(etype, pairs, arc_steps=12):
    segs = []
    if etype == 'LINE':
        x1 = y1 = x2 = y2 = None
        for c, v in pairs:
            if c == '10':
                x1 = float(v)
            elif c == '20':
                y1 = float(v)
            elif c == '11':
                x2 = float(v)
            elif c == '21':
                y2 = float(v)
        if None not in (x1, y1, x2, y2):
            segs.append((x1, y1, x2, y2))
    elif etype == 'LWPOLYLINE':
        pts = []
        cur_x = None
        closed = False
        for c, v in pairs:
            if c == '70':
                closed = (int(v) & 1) != 0
            elif c == '10':
                cur_x = float(v)
            elif c == '20' and cur_x is not None:
                pts.append((cur_x, float(v)))
                cur_x = None
        for k in range(len(pts) - 1):
            segs.append((pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1]))
        if closed and len(pts) >= 3:
            segs.append((pts[-1][0], pts[-1][1], pts[0][0], pts[0][1]))
    elif etype == 'ARC':
        cx = cy = r = a0 = a1 = None
        for c, v in pairs:
            if c == '10':
                cx = float(v)
            elif c == '20':
                cy = float(v)
            elif c == '40':
                r = float(v)
            elif c == '50':
                a0 = float(v)
            elif c == '51':
                a1 = float(v)
        if None not in (cx, cy, r, a0, a1):
            if a1 < a0:
                a1 += 360.0
            span = a1 - a0
            steps = max(4, min(arc_steps, int(span / 12.0) + 1))
            prev = None
            for k in range(steps + 1):
                ang = math.radians(a0 + span * (k / steps))
                pt = (cx + r * math.cos(ang), cy + r * math.sin(ang))
                if prev is not None:
                    segs.append((prev[0], prev[1], pt[0], pt[1]))
                prev = pt
    elif etype == 'CIRCLE':
        cx = cy = r = None
        for c, v in pairs:
            if c == '10':
                cx = float(v)
            elif c == '20':
                cy = float(v)
            elif c == '40':
                r = float(v)
        if None not in (cx, cy, r):
            steps = 12
            prev = None
            for k in range(steps + 1):
                ang = 2 * math.pi * (k / steps)
                pt = (cx + r * math.cos(ang), cy + r * math.sin(ang))
                if prev is not None:
                    segs.append((prev[0], prev[1], pt[0], pt[1]))
                prev = pt
    return segs


def expand_insert(bname, ix, iy, sx, sy, rot_deg, depth=0):
    if depth > 4 or bname not in blocks:
        return []
    bx, by = block_base.get(bname, (0.0, 0.0))
    rot_rad = math.radians(rot_deg)
    out_segs = []
    for etype, pairs in blocks[bname]:
        if etype == 'INSERT':
            sub_b = ''
            six = siy = 0.0
            ssx = ssy = 1.0
            srot = 0.0
            for c, v in pairs:
                if c == '2':
                    sub_b = v
                elif c == '10':
                    six = float(v)
                elif c == '20':
                    siy = float(v)
                elif c == '41':
                    ssx = float(v)
                elif c == '42':
                    ssy = float(v)
                elif c == '50':
                    srot = float(v)
            sub_segs = expand_insert(sub_b, six, siy, ssx, ssy, srot, depth + 1)
            for x1, y1, x2, y2 in sub_segs:
                tx1, ty1 = transform_pt(x1, y1, bx, by, ix, iy, sx, sy, rot_rad)
                tx2, ty2 = transform_pt(x2, y2, bx, by, ix, iy, sx, sy, rot_rad)
                out_segs.append((tx1, ty1, tx2, ty2))
        else:
            for x1, y1, x2, y2 in extract_entity_segments(etype, pairs):
                tx1, ty1 = transform_pt(x1, y1, bx, by, ix, iy, sx, sy, rot_rad)
                tx2, ty2 = transform_pt(x2, y2, bx, by, ix, iy, sx, sy, rot_rad)
                out_segs.append((tx1, ty1, tx2, ty2))
    return out_segs


# Load Windows fonts for crisp Hebrew + numeric rendering
FONT_PATH_REG = r"C:\Windows\Fonts\arial.ttf"
FONT_PATH_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
font_dim = ImageFont.truetype(FONT_PATH_BOLD, 13)
font_room = ImageFont.truetype(FONT_PATH_BOLD, 14)
font_small = ImageFont.truetype(FONT_PATH_REG, 11)
font_title = ImageFont.truetype(FONT_PATH_BOLD, 24)
font_sub = ImageFont.truetype(FONT_PATH_REG, 16)

SHEETS_TO_RENDER = [
    ("B1_Basement1", 48403.69, 35000, 75000, "kkl10_basement.png",
     "קק״ל 10, פתח תקווה — תכנית מרתף חניון 1- (גרמושקה P-23)",
     "מפלס -4.35 מ׳ · 16 חניות רגילות (#1–#16) · 8 מחסנים · 2 מעליות 6 נוסעים · ללא חדר שנאים"),
    ("B2_Basement2", 99239.76, 85000, 125000, "kkl10_basement2.png",
     "קק״ל 10, פתח תקווה — תכנית מרתף חניון 2- (גרמושקה P-23)",
     "מפלס -7.65 מ׳ · 18 חניות רגילות (#17–#34) · 6 מחסנים · מאגר מים וחדר משאבות"),
    ("F0_Ground", 0.00, -15000, 30000, "kkl10_ground.png",
     "קק״ל 10, פתח תקווה — תכנית קומת קרקע ±0.00 (גרמושקה P-23)",
     "לובי כניסה ראשי · חדר עגלות ואופניים · חדר אשפה · דירות גן G-1 (ממ״ד 268×345) ו-G-2 (ממ״ד 264×345)"),
    ("F1_2_Typical", 150886.00, 135000, 175000, "kkl10_f1_2.png",
     "קק״ל 10, פתח תקווה — תכנית קומות 1–2 (גרמושקה P-23)",
     "דירה B (4 חד׳ דרום-מערב) · דירה A (4 חד׳ דרום-מזרח) · דירה C (5 חד׳ צפונית) · ממ״דים 268×345 ס״מ · חדרי שינה 283×340 ס״מ"),
    ("F3_4_Typical", 199602.99, 185000, 225000, "kkl10_typical.png",
     "קק״ל 10, פתח תקווה — תכנית קומות טיפוסיות 3–4 (גרמושקה P-23)",
     "דירה B (ממ״ד 264×345, ח.שינה 283×340) · דירה E (5 חד׳: ממ״ד 268×345, חדרים 283×360/365) · דירה D (4 חד׳ צפונית)"),
    ("F8_Penthouse", 346186.20, 331000, 372000, "kkl10_penthouse.png",
     "קק״ל 10, פתח תקווה — תכנית קומה 8 פנטהאוזים (גרמושקה P-23)",
     "פנטהאוז צפוני PH-1 (5 חד׳) + פנטהאוז דרומי PH-2 (5 חד׳) · ממ״דים 268×345 ס״מ · חדרי שינה 283×340 ס״מ"),
]

os.makedirs(OUT_DIR, exist_ok=True)

for cname, dx, xmin, xmax, out_fn, title_heb, sub_heb in SHEETS_TO_RENDER:
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Subtle outer frame
    draw.rectangle([20, 20, CANVAS_W - 20, CANVAS_H - 120], outline=(203, 213, 225), width=2)

    # 1. Floor tile hatches & subtle background patterns
    for etype, pairs in entities:
        d = dict(pairs)
        if d.get('67', '0') != '0':
            continue
        lay = d.get('8', '')
        if etype == 'HATCH' and lay == 'A-FLOR-PATT':
            for lp in parse_hatch_loops(pairs):
                if xmin <= lp[0][0] < xmax and -25000 <= lp[0][1] <= 20000:
                    poly = [bim_to_px((x - dx + 3426.041) / 1000.0, (y + 18555.823) / 1000.0) for x, y in lp]
                    if len(poly) >= 3:
                        draw.polygon(poly, fill=(248, 250, 252), outline=(226, 232, 240))

    # 2. Structural RC Wall Hatches (Blue Gramoshka fill)
    for etype, pairs in entities:
        d = dict(pairs)
        if d.get('67', '0') != '0':
            continue
        lay = d.get('8', '')
        if etype == 'HATCH' and lay == 'A-WALL-PATT':
            for lp in parse_hatch_loops(pairs):
                if xmin <= lp[0][0] < xmax and -25000 <= lp[0][1] <= 20000:
                    poly = [bim_to_px((x - dx + 3426.041) / 1000.0, (y + 18555.823) / 1000.0) for x, y in lp]
                    if len(poly) >= 3:
                        draw.polygon(poly, fill=(79, 110, 247), outline=(30, 58, 138))

    # 3. Linework (Walls, Interior Partitions, Stairs, Floor edges, Lot boundary)
    for etype, pairs in entities:
        d = dict(pairs)
        if d.get('67', '0') != '0':
            continue
        lay = d.get('8', '')
        if etype in ('LINE', 'LWPOLYLINE', 'ARC', 'CIRCLE'):
            segs = extract_entity_segments(etype, pairs)
            if not segs:
                continue
            if not (xmin <= segs[0][0] < xmax and -25000 <= segs[0][1] <= 20000):
                continue

            if lay == 'I-WALL':
                col, w = (220, 38, 38), 2  # Red Gramoshka interior walls
            elif lay == 'A-WALL':
                col, w = (30, 58, 138), 2  # Dark blue structural wall outlines
            elif lay in ('S-STRS', 'S-STRS-MBND'):
                col, w = (15, 23, 42), 2
            elif lay in ('A-FLOR', 'A-FLOR-OVHD'):
                col, w = (71, 85, 105), 1
            elif lay in ('A-DETL-WIDE', 'A-DETL-MEDM'):
                col, w = (37, 99, 235), 2
            elif lay in ('A-DETL', 'A-DETL-THIN', 'A-DETL-HDLN', 'A-DETL-MBND'):
                col, w = (100, 116, 139), 1
            else:
                col, w = (148, 163, 184), 1

            for x1, y1, x2, y2 in segs:
                if xmin <= x1 < xmax and -25000 <= y1 <= 20000:
                    p1 = bim_to_px((x1 - dx + 3426.041) / 1000.0, (y1 + 18555.823) / 1000.0)
                    p2 = bim_to_px((x2 - dx + 3426.041) / 1000.0, (y2 + 18555.823) / 1000.0)
                    draw.line([p1, p2], fill=col, width=w)

    # 4. Block Inserts (Doors, Windows, Furniture, Sanitary, Elevators, Parking stalls, Columns)
    for etype, pairs in entities:
        if etype != 'INSERT':
            continue
        d = dict(pairs)
        if d.get('67', '0') != '0':
            continue
        lay = d.get('8', '')
        ix = float(d.get('10', 0))
        iy = float(d.get('20', 0))
        if not (xmin <= ix < xmax and -25000 <= iy <= 20000):
            continue
        sx = float(d.get('41', 1.0))
        sy = float(d.get('42', 1.0))
        rot = float(d.get('50', 0.0))
        bname = d.get('2', '')
        segs = expand_insert(bname, ix, iy, sx, sy, rot)
        if not segs:
            continue

        if lay == 'A-DOOR':
            col, w = (15, 23, 42), 2
        elif lay in ('A-GLAZ', 'A-GLAZ-HDLN', 'A-GLAZ-CURT', 'A-GLAZ-CWMG'):
            col, w = (14, 116, 144), 2
        elif lay == 'S-COLS':
            col, w = (30, 58, 138), 3
        elif lay in ('I-FURN', 'Q-CASE', 'P-SANR-FIXT', 'C-PRKG'):
            col, w = (51, 65, 85), 1
        else:
            col, w = (100, 116, 139), 1

        for x1, y1, x2, y2 in segs:
            p1 = bim_to_px((x1 - dx + 3426.041) / 1000.0, (y1 + 18555.823) / 1000.0)
            p2 = bim_to_px((x2 - dx + 3426.041) / 1000.0, (y2 + 18555.823) / 1000.0)
            draw.line([p1, p2], fill=col, width=w)

    # 5. Dimension Blocks (Dimension lines + extension lines)
    for etype, pairs in entities:
        if etype != 'DIMENSION':
            continue
        d = dict(pairs)
        if d.get('67', '0') != '0':
            continue
        x = float(d.get('11', d.get('10', 0)))
        y = float(d.get('21', d.get('20', 0)))
        if not (xmin <= x < xmax and -25000 <= y <= 20000):
            continue
        bname = d.get('2', '')
        if bname in blocks:
            for betype, bpairs in blocks[bname]:
                for x1, y1, x2, y2 in extract_entity_segments(betype, bpairs):
                    if xmin <= x1 < xmax and -25000 <= y1 <= 20000:
                        p1 = bim_to_px((x1 - dx + 3426.041) / 1000.0, (y1 + 18555.823) / 1000.0)
                        p2 = bim_to_px((x2 - dx + 3426.041) / 1000.0, (y2 + 18555.823) / 1000.0)
                        draw.line([p1, p2], fill=(148, 163, 184), width=1)

    # 6. MTEXT / TEXT Room & Architectural Labels
    for etype, pairs in entities:
        if etype not in ('MTEXT', 'TEXT'):
            continue
        d = dict(pairs)
        if d.get('67', '0') != '0':
            continue
        x = float(d.get('10', 0))
        y = float(d.get('20', 0))
        if not (xmin <= x < xmax and -25000 <= y <= 20000):
            continue
        xb = (x - dx + 3426.041) / 1000.0
        nb = (y + 18555.823) / 1000.0
        if not (-4.2 <= xb <= 17.2 and -4.2 <= nb <= 37.2):
            continue
        raw_txt = d.get('1', '')
        clean = decode_dxf_str(raw_txt)
        if not clean:
            continue
        vis = bidi_visual(clean)
        px, py = bim_to_px(xb, nb)
        is_room = any(k in clean for k in ['שינה', 'ממ"ד', 'מגורים', 'מטבח', 'רחצה', 'מרפסת', 'מדרגות', 'מעלית', 'מחסן', 'חניות', 'לובי', 'אשפה'])
        fnt = font_room if is_room else font_small
        col = (15, 23, 42) if is_room else (71, 85, 105)
        draw.text((px, py), vis, font=fnt, fill=col, anchor="mm")

    # 7. Interior Dimension Numbers (highlighted crisply at exact measurement positions)
    for etype, pairs in entities:
        if etype != 'DIMENSION':
            continue
        d = dict(pairs)
        if d.get('67', '0') != '0':
            continue
        x = float(d.get('11', d.get('10', 0)))
        y = float(d.get('21', d.get('20', 0)))
        if not (xmin <= x < xmax and -25000 <= y <= 20000):
            continue
        xb = (x - dx + 3426.041) / 1000.0
        nb = (y + 18555.823) / 1000.0
        val = round(float(d.get('42', 0)))
        txt = d.get('1', '')
        if -1.5 <= xb <= 14.5 and -2.5 <= nb <= 35.0 and '\\X' not in txt and val >= 50:
            px, py = bim_to_px(xb, nb)
            s_val = str(val)
            # Small white halo for readability
            bbox = draw.textbbox((px, py), s_val, font=font_dim, anchor="mm")
            draw.rectangle([bbox[0] - 2, bbox[1] - 1, bbox[2] + 2, bbox[3] + 1], fill=(255, 255, 255))
            # Highlight critical narrow widths (264, 265, 268) in deep crimson/blue so they are unmistakable
            dim_col = (185, 28, 28) if val in (264, 265, 268) else (30, 64, 175)
            draw.text((px, py), s_val, font=font_dim, fill=dim_col, anchor="mm")

    # 8. Title Block Banner at Bottom
    draw.rectangle([20, CANVAS_H - 115, CANVAS_W - 20, CANVAS_H - 20], fill=(248, 250, 252), outline=(148, 163, 184), width=2)
    draw.text((CANVAS_W - 45, CANVAS_H - 82), bidi_visual(title_heb), font=font_title, fill=(30, 58, 138), anchor="rm")
    draw.text((CANVAS_W - 45, CANVAS_H - 46), bidi_visual(sub_heb), font=font_sub, fill=(71, 85, 105), anchor="rm")
    draw.text((45, CANVAS_H - 65), "SENDROWITZ ARCHITECTS | KULESKI GROUP | SCALE 1:100 (P-23)", font=font_sub, fill=(100, 116, 139), anchor="lm")

    out_path = os.path.join(OUT_DIR, out_fn)
    img.save(out_path, optimize=True)
    print(f"Rendered {out_fn} ({os.path.getsize(out_path)//1024} KB)")
