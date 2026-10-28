import collections
import json
import math
import re

def decode_dxf_str(s):
    def repl_u(m):
        return chr(int(m.group(1), 16))
    s = re.sub(r'\\U\+([0-9A-Fa-f]{4})', repl_u, s)
    def repl_m(m):
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

print("Reading kkl10_gramoshka.dxf...")
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

print(f"Parsed {len(blocks)} blocks and {len(entities)} entities.")

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
                        x1 = y1 = x2 = y2 = None
                        while idx < m and pairs[idx][0] in ('10', '20', '11', '21'):
                            ec, ev = pairs[idx]
                            if ec == '10': x1 = float(ev)
                            elif ec == '20': y1 = float(ev)
                            elif ec == '11': x2 = float(ev)
                            elif ec == '21': y2 = float(ev)
                            idx += 1
                        if x1 is not None and y1 is not None:
                            pts.append((x1, y1))
                    else:
                        while idx < m and pairs[idx][0] not in ('72', '97', '92'):
                            ec, ev = pairs[idx]
                            if ec == '10': x1 = float(ev)
                            elif ec == '20': y1 = float(ev)
                            idx += 1
                    edges_read += 1
                elif cc == '10':
                    x1 = float(vv)
                    y1 = float(pairs[idx+1][1]) if idx+1 < m and pairs[idx+1][0] == '20' else 0.0
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

def hatch_loops_to_rects(loops, dx, snap=0.005):
    bim_loops = []
    xs_raw = []
    for lp in loops:
        blp = []
        for x, y in lp:
            xb = round((x - dx + 3426.041) / 1000.0, 3)
            nb = round((y + 18555.823) / 1000.0, 3)
            blp.append((xb, nb))
            xs_raw.append(xb)
        if len(blp) >= 3:
            bim_loops.append(blp)
    if not bim_loops:
        return []

    xs_sorted = sorted(set(xs_raw))
    xs = [xs_sorted[0]]
    for x in xs_sorted[1:]:
        if x - xs[-1] >= snap:
            xs.append(x)

    raw_strips = []
    for k in range(len(xs) - 1):
        xa, xb = xs[k], xs[k+1]
        if xb - xa < snap:
            continue
        xm = 0.5 * (xa + xb)
        n_hits = []
        for blp in bim_loops:
            m = len(blp)
            for j in range(m):
                x1, n1 = blp[j]
                x2, n2 = blp[(j + 1) % m]
                if (x1 <= xm < x2) or (x2 <= xm < x1):
                    t = (xm - x1) / (x2 - x1)
                    nh = n1 + t * (n2 - n1)
                    n_hits.append(round(nh, 3))
        n_hits.sort()
        for p in range(0, len(n_hits) - 1, 2):
            n0, n1 = n_hits[p], n_hits[p+1]
            if n1 - n0 >= snap:
                raw_strips.append([xa, xb, n0, n1])

    raw_strips.sort(key=lambda r: (r[2], r[3], r[0]))
    merged = []
    for r in raw_strips:
        if merged and abs(merged[-1][2] - r[2]) < snap and abs(merged[-1][3] - r[3]) < snap and abs(merged[-1][1] - r[0]) < snap:
            merged[-1][1] = r[1]
        else:
            merged.append(r)
    return merged

def union_and_simplify_wall_rects(raw_rects, snap=0.015):
    if not raw_rects:
        return []
    xs_raw = sorted(set([r[0] for r in raw_rects] + [r[1] for r in raw_rects]))
    xs = [xs_raw[0]]
    for x in xs_raw[1:]:
        if x - xs[-1] >= 0.008:
            xs.append(x)

    x_strips = []
    for k in range(len(xs) - 1):
        xa, xb = xs[k], xs[k+1]
        xm = 0.5 * (xa + xb)
        n_ivs = []
        for rx0, rx1, rn0, rn1 in raw_rects:
            if rx0 - 0.004 <= xm <= rx1 + 0.004:
                n_ivs.append([rn0, rn1])
        if not n_ivs:
            continue
        n_ivs.sort()
        merged_n = [n_ivs[0]]
        for n0, n1 in n_ivs[1:]:
            if n0 <= merged_n[-1][1] + snap:
                merged_n[-1][1] = max(merged_n[-1][1], n1)
            else:
                merged_n.append([n0, n1])
        for n0, n1 in merged_n:
            x_strips.append([xa, xb, n0, n1])

    x_strips.sort(key=lambda r: (round(r[2], 2), round(r[3], 2), r[0]))
    merged_x = []
    for r in x_strips:
        placed = False
        for m in reversed(merged_x):
            if abs(m[2] - r[2]) <= snap and abs(m[3] - r[3]) <= snap and abs(m[1] - r[0]) <= snap:
                m[1] = r[1]
                m[2] = min(m[2], r[2])
                m[3] = max(m[3], r[3])
                placed = True
                break
        if not placed:
            merged_x.append(r)

    ns_raw = sorted(set([r[2] for r in merged_x] + [r[3] for r in merged_x]))
    ns = [ns_raw[0]]
    for n in ns_raw[1:]:
        if n - ns[-1] >= 0.008:
            ns.append(n)

    n_strips = []
    for k in range(len(ns) - 1):
        na, nb = ns[k], ns[k+1]
        nm = 0.5 * (na + nb)
        x_ivs = []
        for rx0, rx1, rn0, rn1 in merged_x:
            if rn0 - 0.004 <= nm <= rn1 + 0.004:
                x_ivs.append([rx0, rx1])
        if not x_ivs:
            continue
        x_ivs.sort()
        uk = [x_ivs[0]]
        for x0, x1 in x_ivs[1:]:
            tol = 0.085 if (x1 <= 0.40 or x0 >= 12.30) else snap
            if x0 <= uk[-1][1] + tol:
                uk[-1][1] = max(uk[-1][1], x1)
            else:
                uk.append([x0, x1])
        for x0, x1 in uk:
            n_strips.append([x0, x1, na, nb])

    n_strips.sort(key=lambda r: (round(r[0], 2), round(r[1], 2), r[2]))
    final_rects = []
    for r in n_strips:
        placed = False
        for m in reversed(final_rects):
            if abs(m[0] - r[0]) <= snap and abs(m[1] - r[1]) <= snap and abs(m[3] - r[2]) <= snap:
                m[3] = r[3]
                placed = True
                break
        if not placed:
            final_rects.append([round(r[0], 2), round(r[1], 2), round(r[2], 2), round(r[3], 2)])

    return [r for r in final_rects if (r[1] - r[0]) >= 0.04 and (r[3] - r[2]) >= 0.04]

def transform_pt(px, py, bx, by, ix, iy, sx, sy, rot_rad):
    dx = (px - bx) * sx
    dy = (py - by) * sy
    c = math.cos(rot_rad)
    s = math.sin(rot_rad)
    return ix + dx * c - dy * s, iy + dx * s + dy * c

def extract_entity_segments(etype, pairs, arc_steps=8):
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
            steps = max(3, min(arc_steps, int(span / 15.0) + 1))
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
            steps = 8
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

def filter_and_round_segs(segs, dx, min_len_m=0.04):
    out = []
    seen = set()
    for x1, y1, x2, y2 in segs:
        xb1 = round((x1 - dx + 3426.041) / 1000.0, 2)
        nb1 = round((y1 + 18555.823) / 1000.0, 2)
        xb2 = round((x2 - dx + 3426.041) / 1000.0, 2)
        nb2 = round((y2 + 18555.823) / 1000.0, 2)
        if math.hypot(xb2 - xb1, nb2 - nb1) < min_len_m:
            continue
        key = (min((xb1, nb1), (xb2, nb2)), max((xb1, nb1), (xb2, nb2)))
        if key in seen:
            continue
        seen.add(key)
        out.append([xb1, nb1, xb2, nb2])
    return out

clusters = [
    ('F0_Ground',      0.00,      -15000,  30000),
    ('B1_Basement1',   48403.69,   35000,  75000),
    ('B2_Basement2',   99239.76,   85000, 125000),
    ('F1_2_Typical',  150886.00,  135000, 175000),
    ('F3_4_Typical',  199602.99,  185000, 225000),
    ('F5_Floor5',     248743.88,  234000, 274000),
    ('F6_7_Floors67', 296972.56,  282000, 322000),
    ('F8_Penthouse',  346186.20,  331000, 372000),
    ('F9_Roof',       393644.67,  378000, 412000),
    ('B2_Reservoir',  416930.93,  412000, 440000),
    ('F10_UpperRoof', 455353.66,  440000, 480000),
]

compiled = {}

for cname, dx, xmin, xmax in clusters:
    raw_wall_rects = []
    for etype, pairs in entities:
        d = dict(pairs)
        if d.get('67', '0') != '0': continue
        if etype == 'HATCH' and d.get('8', '') == 'A-WALL-PATT':
            lps = [lp for lp in parse_hatch_loops(pairs) if xmin <= lp[0][0] < xmax and -25000 <= lp[0][1] <= 20000]
            if lps:
                raw_wall_rects.extend(hatch_loops_to_rects(lps, dx))
    wall_rects = union_and_simplify_wall_rects(raw_wall_rects)

    windows = []
    seen_wins = set()
    doors = []
    wood_boxes = []
    cols = []
    railings = []
    cladding = []
    cad_door = []
    cad_wood = []
    cad_furn = []
    cad_bath = []
    cad_elev = []
    cad_stairs = []

    for etype, pairs in entities:
        d = dict(pairs)
        if d.get('67', '0') != '0': continue
        lay = d.get('8', '')

        if etype in ('LINE', 'LWPOLYLINE', 'ARC') and lay in ('S-STRS', 'S-STRS-MBND'):
            segs = extract_entity_segments(etype, pairs)
            in_cluster = [s for s in segs if xmin <= s[0] < xmax and -25000 <= s[1] <= 20000]
            if in_cluster:
                cad_stairs.extend(filter_and_round_segs(in_cluster, dx, 0.05))

        elif etype == 'INSERT':
            ix, iy = float(d.get('10', 0)), float(d.get('20', 0))
            if not (xmin <= ix < xmax and -25000 <= iy <= 20000): continue
            sx, sy, rot = float(d.get('41', 1)), float(d.get('42', 1)), float(d.get('50', 0))
            bname = d.get('2', '')
            b_heb = decode_dxf_str(bname)
            segs = expand_insert(bname, ix, iy, sx, sy, rot)
            if not segs: continue
            xs = [(x - dx + 3426.041)/1000.0 for s in segs for x in (s[0], s[2])]
            ns = [(y + 18555.823)/1000.0 for s in segs for y in (s[1], s[3])]
            x0, x1, n0, n1 = round(min(xs), 2), round(max(xs), 2), round(min(ns), 2), round(max(ns), 2)
            ins_x = round((ix - dx + 3426.041)/1000.0, 2)
            ins_n = round((iy + 18555.823)/1000.0, 2)

            if lay == 'S-COLS':
                is_round = 'עגול' in b_heb or '600' in b_heb
                cols.append([x0, x1, n0, n1, 1 if is_round else 0])

            elif lay == 'A-DOOR':
                m_wh = re.search(r'(\d{2,3})_(\d{3})', b_heb)
                w_m = int(m_wh.group(1))/100.0 if m_wh else max(x1-x0, n1-n0)
                h_m = int(m_wh.group(2))/100.0 if m_wh else 2.10
                w_m = min(max(w_m, 0.40), 1.40)
                r_norm = round(rot) % 180
                axis = 'X' if r_norm < 45 or r_norm > 135 else 'N'
                doors.append([ins_x, ins_n, round(w_m, 2), round(h_m, 2), axis])
                cad_door.extend(filter_and_round_segs(segs, dx, 0.035))

            elif lay in ('A-GLAZ', 'A-GLAZ-HDLN', 'A-GLAZ-CURT'):
                if 'Pipe' in b_heb or 'צינור' in b_heb:
                    continue
                if 'Mamad Window' in b_heb or '100_100' in b_heb:
                    cn = round(0.5 * (n0 + n1), 2)
                    if abs(cn - 9.08) < 0.25: wn0, wn1 = 8.58, 9.58
                    elif abs(cn - 23.42) < 0.25: wn0, wn1 = 22.92, 23.92
                    else: wn0, wn1 = round(cn - 0.50, 2), round(cn + 0.50, 2)
                    wx0, wx1 = (0.00, 0.35) if x0 < 2.0 else (12.38, 12.73)
                    w_rec = [wx0, wx1, wn0, wn1, 1.10, 2.10, 'X', 1, 1]
                elif lay == 'A-GLAZ-CURT':
                    axis = 'N' if (x1 - x0) >= (n1 - n0) else 'X'
                    if axis == 'N':
                        cm = 0.5 * (n0 + n1)
                        n0, n1 = round(cm - 0.08, 2), round(cm + 0.08, 2)
                    else:
                        cm = 0.5 * (x0 + x1)
                        x0, x1 = round(cm - 0.08, 2), round(cm + 0.08, 2)
                    w_rec = [x0, x1, n0, n1, 0.00, 3.83, axis, 1, 2]
                else:
                    axis = 'N' if (x1 - x0) >= (n1 - n0) else 'X'
                    sill, head, panels, wtype = 0.85, 2.20, 2, 0
                    if '300-245' in b_heb: sill, head, panels = 0.00, 2.35, 3
                    elif '300-265' in b_heb: sill, head, panels = 0.00, 2.55, 3
                    elif '320_240' in b_heb: sill, head, panels = 0.00, 2.35, 3
                    elif '210_240' in b_heb: sill, head, panels = 0.85, 2.40, 2
                    elif '160_240' in b_heb or '110_240' in b_heb: sill, head, panels = 0.85, 2.40, 2
                    elif '160_220' in b_heb: sill, head, panels = 0.85, 2.20, 2
                    elif '130_220' in b_heb or '100_220' in b_heb: sill, head, panels = 0.85, 2.20, 2
                    elif '70_215' in b_heb: sill, head, panels = 1.15, 2.15, 1
                    elif '170w_100h' in b_heb:
                        sill, head, panels, wtype = 1.15, 2.15, 3, 3
                        if x0 < 3.0: x0, x1 = 0.99, 1.15
                        else: x0, x1 = 11.58, 11.74
                    elif 'ES_WIN' in b_heb or '80_60' in b_heb: sill, head, panels = 0.50, 1.20, 1
                    w_rec = [x0, x1, n0, n1, sill, head, axis, panels, wtype]

                w_key = (round(w_rec[0], 1), round(w_rec[1], 1), round(w_rec[2], 1), round(w_rec[3], 1))
                if w_key not in seen_wins:
                    seen_wins.add(w_key)
                    windows.append(w_rec)
                cad_bath.extend(filter_and_round_segs(segs, dx, 0.04))

            elif lay == 'Q-CASE' or (lay == 'I-FURN' and 'ארון' in b_heb):
                wood_boxes.append([x0, x1, n0, n1])
                cad_wood.extend(filter_and_round_segs(segs, dx, 0.04))

            elif lay in ('A-FLOR-HRAL',) or (lay == 'A-DETL-MBND' and 'Railing' in b_heb):
                railings.append([x0, x1, n0, n1])
                cad_stairs.extend(filter_and_round_segs(segs, dx, 0.05))

            elif lay in ('A-GENM', 'A-DETL-MBND') and ('גליף חיפוי אלומיניום' in b_heb or 'קורת מרפסת' in b_heb or 'מעקה מרפסת' in b_heb or 'HPL' in b_heb):
                ctype = 'dark_frame' if 'גליף' in b_heb else ('balc_beam' if 'מרפסת' in b_heb else 'hpl')
                cladding.append([x0, x1, n0, n1, ctype])

            elif 'מעלית' in b_heb:
                cad_elev.extend(filter_and_round_segs(segs, dx, 0.05))

            elif 'גלגלון אש' in b_heb:
                cad_bath.append([x0, n0, x1, n0])
                cad_bath.append([x1, n0, x1, n1])
                cad_bath.append([x1, n1, x0, n1])
                cad_bath.append([x0, n1, x0, n0])

            elif lay in ('I-FURN', 'C-PRKG') or (lay == 'A-DETL-MBND' and ('Carpet' in b_heb or 'כורסה' in b_heb or 'שולחן' in b_heb or 'מיטה' in b_heb or 'חניה' in b_heb)):
                cad_furn.extend(filter_and_round_segs(segs, dx, 0.04))

            elif lay in ('P-SANR-FIXT', 'A-GENM', 'Q-SPCQ', 'Q-SPCQ-HDLN', 'M-EQPM'):
                if 'Gas Hob' in b_heb:
                    cad_bath.extend(filter_and_round_segs(segs, dx, 0.08))
                elif 'שירותים' in b_heb:
                    cad_bath.extend(filter_and_round_segs(segs, dx, 0.05))
                elif 'solar' in b_heb:
                    cladding.append([x0, x1, n0, n1, 'solar'])
                    cad_furn.extend(filter_and_round_segs(segs, dx, 0.06))
                else:
                    cad_bath.extend(filter_and_round_segs(segs, dx, 0.04))

    compiled[cname] = {
        'walls': wall_rects,
        'cols': cols,
        'windows': windows,
        'doors': doors,
        'wood_boxes': wood_boxes,
        'railings': railings,
        'cladding': cladding,
        'cad_door': cad_door,
        'cad_wood': cad_wood,
        'cad_furn': cad_furn,
        'cad_bath': cad_bath,
        'cad_elev': cad_elev,
        'cad_stairs': cad_stairs,
    }
    tot_cad = len(cad_door) + len(cad_wood) + len(cad_furn) + len(cad_bath) + len(cad_elev) + len(cad_stairs)
    print(f"{cname:15s}: walls={len(wall_rects):3d}, wins={len(windows):2d}, doors={len(doors):2d}, wood={len(wood_boxes):2d}, clad={len(cladding):2d}, CAD_segs={tot_cad:4d}")

# Write compact JSON for injection into kkl10_3d_bim_viewer.html
with open('dwg_compiled_clusters.json', 'w', encoding='utf-8') as f:
    json.dump(compiled, f, separators=(',', ':'))
print("Saved dwg_compiled_clusters.json successfully.")
