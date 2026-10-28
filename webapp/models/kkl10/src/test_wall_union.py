from inspect_walls_and_slabs import entities, parse_hatch_loops, clusters
from test_wall_decomposition import hatch_loops_to_rects

def union_and_simplify_wall_rects(raw_rects, snap=0.015):
    if not raw_rects:
        return []
    # 1. Collect unique X coordinates
    xs_raw = sorted(set([r[0] for r in raw_rects] + [r[1] for r in raw_rects]))
    xs = [xs_raw[0]]
    for x in xs_raw[1:]:
        if x - xs[-1] >= 0.008:
            xs.append(x)

    # 2. For each X-slab, union all covering N-intervals
    x_strips = []
    for k in range(len(xs) - 1):
        xa, xb = xs[k], xs[k+1]
        xm = 0.5 * (xa + xb)
        n_ivs = []
        for rx0, rx1, rn0, rn1 in raw_rects:
            if rx0 - 0.004 <= xm <= rx1 + 0.004:
                n_ivs.append([rn0, rn1])
        if not n_ivs:
            continue
        n_ivs.sort()
        merged_n = [n_ivs[0]]
        for n0, n1 in n_ivs[1:]:
            if n0 <= merged_n[-1][1] + snap:
                merged_n[-1][1] = max(merged_n[-1][1], n1)
            else:
                merged_n.append([n0, n1])
        for n0, n1 in merged_n:
            x_strips.append([xa, xb, n0, n1])

    # 3. Merge adjacent X-strips that share the same [n0, n1]
    x_strips.sort(key=lambda r: (round(r[2], 2), round(r[3], 2), r[0]))
    merged_x = []
    for r in x_strips:
        placed = False
        for m in reversed(merged_x):
            if abs(m[2] - r[2]) <= snap and abs(m[3] - r[3]) <= snap and abs(m[1] - r[0]) <= snap:
                m[1] = r[1]
                m[2] = min(m[2], r[2])
                m[3] = max(m[3], r[3])
                placed = True
                break
        if not placed:
            merged_x.append(r)

    # 4. Now do the exact same union along N-slabs so vertical walls with slight X-steps (like plaster) merge cleanly!
    ns_raw = sorted(set([r[2] for r in merged_x] + [r[3] for r in merged_x]))
    ns = [ns_raw[0]]
    for n in ns_raw[1:]:
        if n - ns[-1] >= 0.008:
            ns.append(n)

    n_strips = []
    for k in range(len(ns) - 1):
        na, nb = ns[k], ns[k+1]
        nm = 0.5 * (na + nb)
        x_ivs = []
        for rx0, rx1, rn0, rn1 in merged_x:
            if rn0 - 0.004 <= nm <= rn1 + 0.004:
                x_ivs.append([rx0, rx1])
        if not x_ivs:
            continue
        x_ivs.sort()
        uk = [x_ivs[0]]
        for x0, x1 in x_ivs[1:]:
            if x0 <= uk[-1][1] + snap:
                uk[-1][1] = max(uk[-1][1], x1)
            else:
                uk.append([x0, x1])
        for x0, x1 in uk:
            n_strips.append([x0, x1, na, nb])

    n_strips.sort(key=lambda r: (round(r[0], 2), round(r[1], 2), r[2]))
    final_rects = []
    for r in n_strips:
        placed = False
        for m in reversed(final_rects):
            if abs(m[0] - r[0]) <= snap and abs(m[1] - r[1]) <= snap and abs(m[3] - r[2]) <= snap:
                m[3] = r[3]
                placed = True
                break
        if not placed:
            final_rects.append([round(r[0], 3), round(r[1], 3), round(r[2], 3), round(r[3], 3)])

    return final_rects

for cname, dx, xmin, xmax in clusters:
    raw = []
    for etype, pairs in entities:
        d = dict(pairs)
        if d.get('67', '0') != '0': continue
        if etype == 'HATCH' and d.get('8', '') == 'A-WALL-PATT':
            lps = [lp for lp in parse_hatch_loops(pairs) if xmin <= lp[0][0] < xmax and -25000 <= lp[0][1] <= 20000]
            if lps:
                raw.extend(hatch_loops_to_rects(lps, dx))
    unioned = union_and_simplify_wall_rects(raw)
    print(f'{cname:15s}: {len(raw):3d} raw -> {len(unioned):3d} unified solid wall piers!')
    if cname == 'F1_2_Typical':
        west = [r for r in unioned if r[0] < 0.45]
        west.sort(key=lambda r: (r[2], r[0]))
        for r in west[:18]:
            print(f'   West pier: X=[{r[0]:6.3f}..{r[1]:6.3f}] (w={r[1]-r[0]:.3f}), N=[{r[2]:6.3f}..{r[3]:6.3f}] (h={r[3]-r[2]:.3f})')
