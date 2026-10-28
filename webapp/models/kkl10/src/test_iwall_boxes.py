from inspect_walls_and_slabs import entities, clusters

def extract_iwall_boxes(entities, dx, xmin, xmax):
    h_segs = [] # (y, x0, x1)
    v_segs = [] # (x, y0, y1)
    for etype, pairs in entities:
        if etype != 'LINE': continue
        d = dict(pairs)
        if d.get('67', '0') != '0': continue
        if d.get('8', '') != 'I-WALL': continue
        x1, y1 = float(d.get('10', 0)), float(d.get('20', 0))
        x2, y2 = float(d.get('11', 0)), float(d.get('21', 0))
        if not (xmin <= x1 < xmax and -25000 <= y1 <= 20000): continue
        xb1 = round((x1 - dx + 3426.041) / 1000.0, 3)
        nb1 = round((y1 + 18555.823) / 1000.0, 3)
        xb2 = round((x2 - dx + 3426.041) / 1000.0, 3)
        nb2 = round((y2 + 18555.823) / 1000.0, 3)
        if abs(nb1 - nb2) < 0.005 and abs(xb2 - xb1) > 0.05:
            h_segs.append((round(0.5*(nb1+nb2), 3), min(xb1, xb2), max(xb1, xb2)))
        elif abs(xb1 - xb2) < 0.005 and abs(nb2 - nb1) > 0.05:
            v_segs.append((round(0.5*(xb1+xb2), 3), min(nb1, nb2), max(nb1, nb2)))

    # Pair parallel h_segs within 0.06m..0.22m in N that overlap in X
    boxes = []
    h_segs.sort()
    for i in range(len(h_segs)):
        nA, xa0, xa1 = h_segs[i]
        for j in range(i+1, len(h_segs)):
            nB, xb0, xb1 = h_segs[j]
            dn = nB - nA
            if dn > 0.22: break
            if 0.055 <= dn <= 0.22:
                ox0 = max(xa0, xb0)
                ox1 = min(xa1, xb1)
                if ox1 - ox0 > 0.05:
                    # Check there isn't an intermediate line between nA and nB
                    boxes.append((ox0, ox1, nA, nB))

    v_segs.sort()
    for i in range(len(v_segs)):
        xA, na0, na1 = v_segs[i]
        for j in range(i+1, len(v_segs)):
            xB, nb0, nb1 = v_segs[j]
            dx_w = xB - xA
            if dx_w > 0.22: break
            if 0.055 <= dx_w <= 0.22:
                on0 = max(na0, nb0)
                on1 = min(na1, nb1)
                if on1 - on0 > 0.05:
                    boxes.append((xA, xB, on0, on1))
    return boxes

for cname, dx, xmin, xmax in clusters:
    b = extract_iwall_boxes(entities, dx, xmin, xmax)
    print(f'{cname:15s}: {len(b):3d} I-WALL 3D partition boxes extracted!')
