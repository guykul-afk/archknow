import collections
from inspect_walls_and_slabs import entities, parse_hatch_loops, clusters

def hatch_loops_to_rects(loops, dx, snap=0.005):
    # Convert loops to BIM meter coords (xbim, nbim)
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

    # Deduplicate xs within snap
    xs_sorted = sorted(set(xs_raw))
    xs = [xs_sorted[0]]
    for x in xs_sorted[1:]:
        if x - xs[-1] >= snap:
            xs.append(x)

    raw_strips = [] # (x0, x1, n0, n1)
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

    # Merge adjacent strips in X that share identical (n0, n1)
    raw_strips.sort(key=lambda r: (r[2], r[3], r[0]))
    merged = []
    for r in raw_strips:
        if merged and abs(merged[-1][2] - r[2]) < snap and abs(merged[-1][3] - r[3]) < snap and abs(merged[-1][1] - r[0]) < snap:
            merged[-1][1] = r[1]
        else:
            merged.append(r)
    return merged

for cname, dx, xmin, xmax in clusters:
    all_rects = []
    hatch_cnt = 0
    for etype, pairs in entities:
        d = dict(pairs)
        if d.get('67', '0') != '0': continue
        if etype == 'HATCH' and d.get('8', '') == 'A-WALL-PATT':
            lps = [lp for lp in parse_hatch_loops(pairs) if xmin <= lp[0][0] < xmax and -25000 <= lp[0][1] <= 20000]
            if lps:
                hatch_cnt += 1
                all_rects.extend(hatch_loops_to_rects(lps, dx))
    print(f'{cname:15s}: {hatch_cnt:3d} HATCH entities -> {len(all_rects):3d} clean 3D wall boxes!')
