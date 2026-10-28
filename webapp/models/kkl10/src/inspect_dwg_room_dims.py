from inspect_walls_and_slabs import entities, clusters

for cname, dx, xmin, xmax in clusters:
    dims = []
    for etype, pairs in entities:
        if etype != 'DIMENSION': continue
        d = dict(pairs)
        if d.get('67', '0') != '0': continue
        x = float(d.get('11', d.get('10', 0)))
        y = float(d.get('21', d.get('20', 0)))
        if not (xmin <= x < xmax and -25000 <= y <= 20000): continue
        xb = round((x - dx + 3426.041)/1000.0, 2)
        nb = round((y + 18555.823)/1000.0, 2)
        val = round(float(d.get('42', 0)))
        ang = round(float(d.get('50', 0))) % 180
        txt = d.get('1', '')
        # Filter to interior room dimensions (inside building footprint X in [0..12.8], N in [-2..34], excluding window tags with \X)
        if -0.5 <= xb <= 13.0 and -2.0 <= nb <= 34.0 and '\\X' not in txt:
            dims.append((nb, xb, val, ang, txt))
    dims.sort()
    print(f'=== {cname} ({len(dims)} interior dims) ===')
    for nb, xb, val, ang, txt in dims:
        axis = 'W-E (X)' if ang == 0 else f'S-N (N,{ang})'
        print(f'  BIM(X={xb:5.2f}, N={nb:5.2f}) | {val:4d} cm | {axis}')
