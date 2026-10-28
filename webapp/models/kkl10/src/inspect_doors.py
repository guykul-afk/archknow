from test_dwg_block_expansion import blocks, block_base, entities, expand_insert, decode_dxf_str
from inspect_walls_and_slabs import clusters

cname, dx, xmin, xmax = clusters[3] # F1_2_Typical
for etype, pairs in entities:
    if etype != 'INSERT': continue
    d = dict(pairs)
    if d.get('67', '0') != '0': continue
    if d.get('8', '') != 'A-DOOR': continue
    ix, iy = float(d.get('10', 0)), float(d.get('20', 0))
    if not (xmin <= ix < xmax and -25000 <= iy <= 20000): continue
    sx, sy, rot = float(d.get('41', 1)), float(d.get('42', 1)), float(d.get('50', 0))
    bname = d.get('2', '')
    b_heb = decode_dxf_str(bname)
    xb = (ix - dx + 3426.041)/1000.0
    nb = (iy + 18555.823)/1000.0
    segs = expand_insert(bname, ix, iy, sx, sy, rot)
    xs = [(x - dx + 3426.041)/1000.0 for s in segs for x in (s[0], s[2])]
    ns = [(y + 18555.823)/1000.0 for s in segs for y in (s[1], s[3])]
    print(f'ins=({xb:6.2f}, {nb:6.2f}) rot={rot:5.1f} sx={sx:4.1f} sy={sy:4.1f} bbox=[{min(xs):5.2f}..{max(xs):5.2f}, {min(ns):5.2f}..{max(ns):5.2f}] | {b_heb}')
