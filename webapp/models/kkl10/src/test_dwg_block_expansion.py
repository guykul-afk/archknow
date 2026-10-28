import collections
import math
import re

def decode_dxf_str(s):
    def repl_u(m):
        return chr(int(m.group(1), 16))
    s = re.sub(r'\\U\+([0-9A-Fa-f]{4})', repl_u, s)
    def repl_m(m):
        hi = int(m.group(1), 16)
        lo = int(m.group(2), 16)
        if 0xFA <= lo <= 0xFB:
            try:
                return bytes([lo]).decode('cp1255')
            except:
                pass
        return '?'
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
    s = s.replace('\\P', '\n').replace('{', '').replace('}', '')
    return s.strip()

with open('kkl10_gramoshka.dxf', 'r', encoding='utf-8', errors='replace') as f:
    lines = [l.rstrip('\r\n') for l in f]

i, n = 0, len(lines)
sec = None
cur_block = None
blocks = collections.defaultdict(list)
block_base = {}
entities = []

def read_entity(start_i):
    etype = lines[start_i - 1].strip()
    i = start_i
    pairs = []
    while i + 1 < n and lines[i].strip() != '0':
        pairs.append((lines[i].strip(), lines[i+1].strip()))
        i += 2
    return etype, pairs, i

while i + 1 < n:
    c, v = lines[i].strip(), lines[i+1].strip()
    i += 2
    if c == '0' and v == 'SECTION' and i + 1 < n:
        sec = lines[i+1].strip()
        i += 2
        continue
    if sec == 'BLOCKS':
        if c == '0' and v == 'BLOCK':
            bname = ''
            bx = by = 0.0
            while i + 1 < n and lines[i].strip() != '0':
                cc, vv = lines[i].strip(), lines[i+1].strip()
                i += 2
                if cc == '2': bname = vv
                elif cc == '10':
                    try: bx = float(vv)
                    except: pass
                elif cc == '20':
                    try: by = float(vv)
                    except: pass
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

def transform_pt(px, py, bx, by, ix, iy, sx, sy, rot_rad):
    dx = (px - bx) * sx
    dy = (py - by) * sy
    c = math.cos(rot_rad)
    s = math.sin(rot_rad)
    tx = ix + dx * c - dy * s
    ty = iy + dx * s + dy * c
    return tx, ty

def extract_entity_segments(etype, pairs):
    segs = []
    if etype == 'LINE':
        x1 = y1 = x2 = y2 = None
        for c, v in pairs:
            if c == '10': x1 = float(v)
            elif c == '20': y1 = float(v)
            elif c == '11': x2 = float(v)
            elif c == '21': y2 = float(v)
        if None not in (x1, y1, x2, y2):
            segs.append((x1, y1, x2, y2))
    elif etype == 'LWPOLYLINE':
        pts = []
        cur_x = None
        closed = False
        for c, v in pairs:
            if c == '70': closed = (int(v) & 1) != 0
            elif c == '10': cur_x = float(v)
            elif c == '20' and cur_x is not None:
                pts.append((cur_x, float(v)))
                cur_x = None
        for k in range(len(pts) - 1):
            segs.append((pts[k][0], pts[k][1], pts[k+1][0], pts[k+1][1]))
        if closed and len(pts) >= 3:
            segs.append((pts[-1][0], pts[-1][1], pts[0][0], pts[0][1]))
    elif etype == 'ARC':
        cx = cy = r = a0 = a1 = None
        for c, v in pairs:
            if c == '10': cx = float(v)
            elif c == '20': cy = float(v)
            elif c == '40': r = float(v)
            elif c == '50': a0 = float(v)
            elif c == '51': a1 = float(v)
        if None not in (cx, cy, r, a0, a1):
            if a1 < a0: a1 += 360.0
            span = a1 - a0
            steps = max(4, min(16, int(span / 12.0) + 1))
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
            if c == '10': cx = float(v)
            elif c == '20': cy = float(v)
            elif c == '40': r = float(v)
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
    if depth > 5 or bname not in blocks:
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
                if c == '2': sub_b = v
                elif c == '10': six = float(v)
                elif c == '20': siy = float(v)
                elif c == '41': ssx = float(v)
                elif c == '42': ssy = float(v)
                elif c == '50': srot = float(v)
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

# Test expanding all A-DOOR, A-GLAZ, A-GLAZ-HDLN, Q-CASE, I-FURN in Cluster 3 (DX=150886.0)
DX3 = 150886.0
for target_lay in ['A-DOOR', 'A-GLAZ', 'A-GLAZ-HDLN', 'Q-CASE']:
    print(f'=== {target_lay} in Cluster 3 (F1_2_Typical) ===')
    for etype, pairs in entities:
        if etype != 'INSERT': continue
        d = dict(pairs)
        if d.get('67', '0') != '0': continue
        lay = d.get('8', '')
        if lay != target_lay: continue
        ix = float(d.get('10', 0))
        iy = float(d.get('20', 0))
        if not (135000 <= ix <= 175000 and -25000 <= iy <= 20000): continue
        sx = float(d.get('41', 1.0))
        sy = float(d.get('42', 1.0))
        rot = float(d.get('50', 0.0))
        bname = d.get('2', '')
        segs = expand_insert(bname, ix, iy, sx, sy, rot)
        if not segs: continue
        xs = [(x - DX3 + 3426.041)/1000.0 for s in segs for x in (s[0], s[2])]
        ns = [(y + 18555.823)/1000.0 for s in segs for y in (s[1], s[3])]
        b_heb = decode_dxf_str(bname)
        print(f'  [{min(xs):6.2f}..{max(xs):6.2f}, N={min(ns):6.2f}..{max(ns):6.2f}] ({len(segs):2d} segs) rot={rot:5.1f} | {b_heb}')
