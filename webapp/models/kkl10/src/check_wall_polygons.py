from inspect_walls_and_slabs import entities, parse_hatch_loops, clusters

for cname, dx, xmin, xmax in clusters:
    total = 0
    rect4 = 0
    ortho_poly = 0
    non_ortho = 0
    for etype, pairs in entities:
        d = dict(pairs)
        if d.get('67', '0') != '0': continue
        if etype == 'HATCH' and d.get('8', '') == 'A-WALL-PATT':
            for lp in parse_hatch_loops(pairs):
                if xmin <= lp[0][0] < xmax and -25000 <= lp[0][1] <= 20000:
                    total += 1
                    # Check if all edges are axis-aligned (dx < 1mm or dy < 1mm)
                    is_ortho = True
                    for k in range(len(lp)):
                        x1, y1 = lp[k]
                        x2, y2 = lp[(k+1) % len(lp)]
                        if abs(x2 - x1) > 2.0 and abs(y2 - y1) > 2.0:
                            is_ortho = False
                            break
                    if not is_ortho:
                        non_ortho += 1
                    elif len(lp) == 4:
                        rect4 += 1
                    else:
                        ortho_poly += 1
    print(f'{cname:15s}: total={total:3d} | 4-pt rect={rect4:3d} | ortho L/T poly={ortho_poly:3d} | non-ortho={non_ortho:3d}')
