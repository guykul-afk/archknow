from test_dwg_block_expansion import blocks, block_base, entities, expand_insert, decode_dxf_str
from inspect_walls_and_slabs import clusters

for cname, dx, xmin, xmax in clusters:
    wins = []
    for etype, pairs in entities:
        if etype != 'INSERT': continue
        d = dict(pairs)
        if d.get('67', '0') != '0': continue
        lay = d.get('8', '')
        if lay not in ('A-GLAZ', 'A-GLAZ-HDLN', 'A-GLAZ-CURT'): continue
        ix, iy = float(d.get('10', 0)), float(d.get('20', 0))
        if not (xmin <= ix < xmax and -25000 <= iy <= 20000): continue
        sx, sy, rot = float(d.get('41', 1)), float(d.get('42', 1)), float(d.get('50', 0))
        bname = d.get('2', '')
        b_heb = decode_dxf_str(bname)
        if 'Pipe' in b_heb or 'צינור' in b_heb: continue
        segs = expand_insert(bname, ix, iy, sx, sy, rot)
        if not segs: continue
        xs = [(x - dx + 3426.041)/1000.0 for s in segs for x in (s[0], s[2])]
        ns = [(y + 18555.823)/1000.0 for s in segs for y in (s[1], s[3])]
        wins.append((lay, min(xs), max(xs), min(ns), max(ns), rot, b_heb))
    print(f'=== {cname} ({len(wins)} windows/curtain panels) ===')
    for lay, x0, x1, n0, n1, rot, b_heb in wins:
        print(f'  [{lay:11s}] X=[{x0:6.2f}..{x1:6.2f}], N=[{n0:6.2f}..{n1:6.2f}] rot={rot:5.1f} | {b_heb}')
