from inspect_cols_railings import entities, blocks, block_base

# Check all X coordinates of model space entities
xs = []
ps_entities = 0
for etype, pairs in entities:
    d = dict(pairs)
    if d.get('67', '0') == '1':
        ps_entities += 1
        continue
    if '10' in d and '20' in d:
        try:
            xs.append((float(d['10']), float(d['20']), etype, d.get('8', '')))
        except:
            pass

print(f'Total Model Space point entities: {len(xs)}, Paper Space entities: {ps_entities}')
# Check if any model space entities have Y outside [-35000, 25000] or X outside [-20000, 480000]
outliers = [(x, y, et, l) for x, y, et, l in xs if y < -35000 or y > 25000 or x < -20000 or x > 485000]
print(f'Outliers outside the 11 floor plan clusters: {len(outliers)}')
for o in outliers[:20]:
    print('  Outlier:', o)
