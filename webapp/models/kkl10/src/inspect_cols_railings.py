import collections
import math
import re

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

# Check S-COLS, A-FLOR-HRAL, Q-SPCQ across all clusters
for cname, dx, xmin, xmax in clusters:
    cols_list = []
    hral_list = []
    spcq_list = []
    for etype, pairs in entities:
        if etype != 'INSERT': continue
        d = dict(pairs)
        if d.get('67', '0') != '0': continue
        lay = d.get('8', '')
        ix = float(d.get('10', 0))
        iy = float(d.get('20', 0))
        if not (xmin <= ix < xmax and -25000 <= iy <= 20000): continue
        xb = round((ix - dx + 3426.041)/1000.0, 2)
        nb = round((iy + 18555.823)/1000.0, 2)
        bname = d.get('2', '')
        if lay == 'S-COLS': cols_list.append((xb, nb, bname))
        elif lay == 'A-FLOR-HRAL': hral_list.append((xb, nb, bname))
        elif lay == 'Q-SPCQ': spcq_list.append((xb, nb, bname))
    print(f'{cname:15s}: S-COLS={len(cols_list):2d}, A-FLOR-HRAL={len(hral_list):2d}, Q-SPCQ={len(spcq_list):2d}')
    for xb, nb, b in cols_list:
        print(f'   COL at ({xb:6.2f}, {nb:6.2f}): {b[:35]}')
