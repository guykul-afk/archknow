from inspect_walls_and_slabs import entities, parse_hatch_loops, clusters
from test_wall_decomposition import hatch_loops_to_rects

cname, dx, xmin, xmax = clusters[3] # F1_2_Typical
rects = []
for etype, pairs in entities:
    d = dict(pairs)
    if d.get('67', '0') != '0': continue
    if etype == 'HATCH' and d.get('8', '') == 'A-WALL-PATT':
        lps = [lp for lp in parse_hatch_loops(pairs) if xmin <= lp[0][0] < xmax and -25000 <= lp[0][1] <= 20000]
        if lps:
            rects.extend(hatch_loops_to_rects(lps, dx))

print(f'Total rects in F1_2: {len(rects)}')
west_rects = [r for r in rects if r[0] < 0.45]
west_rects.sort(key=lambda r: (r[2], r[0]))
print(f'West wall rects ({len(west_rects)}):')
for r in west_rects[:30]:
    print(f'  X=[{r[0]:6.3f}..{r[1]:6.3f}] (w={r[1]-r[0]:.3f}), N=[{r[2]:6.3f}..{r[3]:6.3f}] (h={r[3]-r[2]:.3f})')
