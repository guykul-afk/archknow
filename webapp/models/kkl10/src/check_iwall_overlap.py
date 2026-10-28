from inspect_walls_and_slabs import entities, parse_hatch_loops, clusters
from test_wall_decomposition import hatch_loops_to_rects
from test_iwall_boxes import extract_iwall_boxes

cname, dx, xmin, xmax = clusters[3] # F1_2_Typical
hatch_rects = []
for etype, pairs in entities:
    d = dict(pairs)
    if d.get('67', '0') != '0': continue
    if etype == 'HATCH' and d.get('8', '') == 'A-WALL-PATT':
        lps = [lp for lp in parse_hatch_loops(pairs) if xmin <= lp[0][0] < xmax and -25000 <= lp[0][1] <= 20000]
        if lps:
            hatch_rects.extend(hatch_loops_to_rects(lps, dx))

iwall_rects = extract_iwall_boxes(entities, dx, xmin, xmax)

overlap_cnt = 0
distinct_cnt = 0
for ix0, ix1, in0, in1 in iwall_rects:
    icx, icn = 0.5*(ix0+ix1), 0.5*(in0+in1)
    hit = False
    for hx0, hx1, hn0, hn1 in hatch_rects:
        if hx0 - 0.02 <= icx <= hx1 + 0.02 and hn0 - 0.02 <= icn <= hn1 + 0.02:
            hit = True
            break
    if hit: overlap_cnt += 1
    else: distinct_cnt += 1

print(f'F1_2_Typical: {len(iwall_rects)} I-WALL boxes -> {overlap_cnt} already in A-WALL-PATT, {distinct_cnt} distinct!')
