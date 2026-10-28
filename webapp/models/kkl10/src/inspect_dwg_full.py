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

# Check DIMENSION entities in Cluster 3 (F1_2_Typical, DX=150886.0)
DX3 = 150886.0
dims_c3 = []
for etype, pairs in entities:
    if etype == 'DIMENSION':
        d = dict(pairs)
        if d.get('67', '0') != '0': continue
        lay = d.get('8', '')
        x = float(d.get('11', d.get('10', 0)))
        y = float(d.get('21', d.get('20', 0)))
        val = float(d.get('42', 0))
        txt = d.get('1', '')
        bname = d.get('2', '')
        # Also check rotation / angle 50
        ang = float(d.get('50', 0))
        if 135000 <= x <= 175000 and -25000 <= y <= 20000:
            xbim = (x - DX3 + 3426.041)/1000.0
            nbim = (y + 18555.823)/1000.0
            dims_c3.append((xbim, nbim, val, ang, txt, bname))

print(f'Cluster 3 has {len(dims_c3)} DIMENSION entities:')
for xbim, nbim, val, ang, txt, bname in dims_c3[:45]:
    print(f'  BIM({xbim:6.2f}, {nbim:6.2f}) val={val:7.1f} ang={ang:5.1f} txt="{txt}" blk={bname}')
