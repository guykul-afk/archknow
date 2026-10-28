from test_dwg_block_expansion import blocks, block_base, entities, expand_insert, extract_entity_segments, decode_dxf_str
from inspect_walls_and_slabs import clusters, parse_hatch_loops

for cname, dx, xmin, xmax in clusters:
    print(f'=== {cname} ===')
    for etype, pairs in entities:
        d = dict(pairs)
        if d.get('67', '0') != '0': continue
        lay = d.get('8', '')
        if etype == 'INSERT' and lay in ('A-FLOR-HRAL', 'A-DETL-MBND'):
            ix, iy = float(d.get('10', 0)), float(d.get('20', 0))
            if not (xmin <= ix < xmax and -25000 <= iy <= 20000): continue
            bname = d.get('2', '')
            b_heb = decode_dxf_str(bname)
            if 'Railing' not in b_heb and 'מעקה' not in b_heb and 'קורת מרפסת' not in b_heb:
                continue
            sx, sy, rot = float(d.get('41', 1)), float(d.get('42', 1)), float(d.get('50', 0))
            segs = expand_insert(bname, ix, iy, sx, sy, rot)
            if not segs: continue
            xs = [(x - dx + 3426.041)/1000.0 for s in segs for x in (s[0], s[2])]
            ns = [(y + 18555.823)/1000.0 for s in segs for y in (s[1], s[3])]
            print(f'  [{lay:11s}] X=[{min(xs):6.2f}..{max(xs):6.2f}], N=[{min(ns):6.2f}..{max(ns):6.2f}] | {b_heb}')
