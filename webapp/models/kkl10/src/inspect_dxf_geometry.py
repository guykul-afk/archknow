import math
import collections
from PIL import Image, ImageDraw

with open('kkl10_gramoshka.dxf', 'r', encoding='utf-8', errors='replace') as f:
    lines = [l.rstrip('\r\n') for l in f]

# 1. Parse BLOCKS and ENTITIES
i = 0
n = len(lines)
sec = None
cur_block = None

blocks = collections.defaultdict(list)
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

print(f"Parsed {len(blocks)} blocks and {len(entities)} top-level entities.")

def parse_hatch_loops(pairs):
    loops = []
    idx = 0
    m = len(pairs)
    while idx < m:
        c, v = pairs[idx]
        if c == '93': # Number of edges in this boundary path
            num_edges = int(v)
            idx += 1
            pts = []
            # Check if polyline boundary (92 & 2) or edge boundary
            # In our inspection, 72=1 is line edge with 10,20 -> 11,21
            edges_read = 0
            while idx < m and edges_read < num_edges:
                cc, vv = pairs[idx]
                if cc == '72':
                    edge_type = int(vv)
                    idx += 1
                    if edge_type == 1: # Line edge
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
                            if x2 is not None and y2 is not None:
                                last_pt = (x2, y2)
                    else:
                        # Arc/ellipse/spline edge - skip to next 72 or 97
                        while idx < m and pairs[idx][0] not in ('72', '97', '92'):
                            ec, ev = pairs[idx]
                            if ec == '10': x1 = float(ev)
                            elif ec == '20': y1 = float(ev)
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

# Test extracting all loops from A-WALL-PATT in Cluster 3 (DX3 = 150886.00)
DX3 = 150886.00
wall_loops_c3 = []
for etype, pairs in entities:
    if etype == 'HATCH':
        lay = ''
        for c, v in pairs:
            if c == '8': lay = v; break
        if lay == 'A-WALL-PATT':
            for lp in parse_hatch_loops(pairs):
                if 135000 < lp[0][0] < 175000:
                    wall_loops_c3.append([(x - DX3, y) for x, y in lp])

print(f"Cluster 3 has {len(wall_loops_c3)} closed wall hatch loops on A-WALL-PATT!")
for idx, lp in enumerate(wall_loops_c3[:10]):
    xs = [p[0] for p in lp]
    ys = [p[1] for p in lp]
    print(f"  Loop {idx}: {len(lp)} verts, X=[{min(xs):.1f}..{max(xs):.1f}], Y=[{min(ys):.1f}..{max(ys):.1f}]")
