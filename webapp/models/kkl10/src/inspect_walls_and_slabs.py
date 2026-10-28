import collections
import math
import re
from PIL import Image, ImageDraw

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
            # Check if polyline boundary (code 72 is has_bulge, followed by 73 is_closed, 93 num_vertices, then 10,20)
            # Or edge boundary (72=1 line edge with 10,20,11,21)
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
                    # Polyline vertex directly under 93
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

for cname, dx, xmin, xmax in clusters:
    wall_loops = 0
    flor_loops = 0
    wall_lines = 0
    iwall_lines = 0
    flor_lines = 0
    for etype, pairs in entities:
        d = dict(pairs)
        if d.get('67', '0') != '0': continue
        lay = d.get('8', '')
        if etype == 'HATCH' and lay in ('A-WALL-PATT', 'A-FLOR-PATT', 'A-DETL-GENF'):
            for lp in parse_hatch_loops(pairs):
                if xmin <= lp[0][0] < xmax and -25000 <= lp[0][1] <= 20000:
                    if lay == 'A-WALL-PATT': wall_loops += 1
                    elif lay == 'A-FLOR-PATT': flor_loops += 1
        elif etype == 'LINE' and lay in ('A-WALL', 'I-WALL', 'A-FLOR'):
            x1 = float(d.get('10', 0))
            y1 = float(d.get('20', 0))
            if xmin <= x1 < xmax and -25000 <= y1 <= 20000:
                if lay == 'A-WALL': wall_lines += 1
                elif lay == 'I-WALL': iwall_lines += 1
                elif lay == 'A-FLOR': flor_lines += 1
    print(f'{cname:15s}: A-WALL-PATT loops={wall_loops:3d}, A-FLOR-PATT loops={flor_loops:3d}, A-WALL lines={wall_lines:4d}, I-WALL lines={iwall_lines:3d}, A-FLOR lines={flor_lines:3d}')
