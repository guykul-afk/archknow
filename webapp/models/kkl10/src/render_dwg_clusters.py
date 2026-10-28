import collections
import math
from PIL import Image, ImageDraw
from test_dwg_block_expansion import blocks, block_base, entities, expand_insert, extract_entity_segments
from inspect_walls_and_slabs import parse_hatch_loops, clusters

# Render a grid of the first 9 clusters into a high-res image
W, H = 900, 1400
cols, rows = 3, 3
img = Image.new('RGB', (W * cols, H * rows), (15, 23, 42))
draw = ImageDraw.Draw(img)

def to_px(xbim, nbim, col_idx, row_idx):
    # xbim in [-6..18] (span 24m), nbim in [-6..38] (span 44m)
    scale = 30.0
    px = col_idx * W + int((xbim + 5.0) * scale)
    py = row_idx * H + int((37.5 - nbim) * scale)
    return px, py

for idx, (cname, dx, xmin, xmax) in enumerate(clusters[:9]):
    c_idx = idx % cols
    r_idx = idx // cols
    # Draw border
    draw.rectangle([c_idx*W, r_idx*H, (c_idx+1)*W-1, (r_idx+1)*H-1], outline=(71, 85, 105), width=2)

    for etype, pairs in entities:
        d = dict(pairs)
        if d.get('67', '0') != '0': continue
        lay = d.get('8', '')

        if etype == 'HATCH' and lay == 'A-WALL-PATT':
            for lp in parse_hatch_loops(pairs):
                if xmin <= lp[0][0] < xmax and -25000 <= lp[0][1] <= 20000:
                    poly = [to_px((x - dx + 3426.041)/1000.0, (y + 18555.823)/1000.0, c_idx, r_idx) for x, y in lp]
                    if len(poly) >= 3:
                        draw.polygon(poly, fill=(226, 232, 240), outline=(148, 163, 184))
        elif etype in ('LINE', 'LWPOLYLINE', 'ARC') and lay in ('A-WALL', 'I-WALL', 'A-FLOR', 'S-STRS'):
            segs = extract_entity_segments(etype, pairs)
            col = (248, 250, 252) if lay == 'A-WALL' else ((251, 191, 36) if lay == 'I-WALL' else ((56, 189, 248) if lay == 'A-FLOR' else (192, 132, 252)))
            for x1, y1, x2, y2 in segs:
                if xmin <= x1 < xmax and -25000 <= y1 <= 20000:
                    p1 = to_px((x1 - dx + 3426.041)/1000.0, (y1 + 18555.823)/1000.0, c_idx, r_idx)
                    p2 = to_px((x2 - dx + 3426.041)/1000.0, (y2 + 18555.823)/1000.0, c_idx, r_idx)
                    draw.line([p1, p2], fill=col, width=1)
        elif etype == 'INSERT' and lay in ('A-DOOR', 'A-GLAZ', 'A-GLAZ-HDLN', 'A-GLAZ-CURT', 'Q-CASE', 'I-FURN', 'P-SANR-FIXT', 'C-PRKG', 'S-COLS'):
            ix = float(d.get('10', 0))
            iy = float(d.get('20', 0))
            if not (xmin <= ix < xmax and -25000 <= iy <= 20000): continue
            sx = float(d.get('41', 1.0))
            sy = float(d.get('42', 1.0))
            rot = float(d.get('50', 0.0))
            bname = d.get('2', '')
            segs = expand_insert(bname, ix, iy, sx, sy, rot)
            if lay == 'A-DOOR': col = (249, 115, 22)
            elif lay in ('A-GLAZ', 'A-GLAZ-HDLN', 'A-GLAZ-CURT'): col = (56, 189, 248)
            elif lay == 'Q-CASE': col = (217, 119, 6)
            elif lay == 'I-FURN': col = (96, 165, 250)
            elif lay == 'P-SANR-FIXT': col = (45, 212, 191)
            elif lay == 'S-COLS': col = (239, 68, 68)
            else: col = (148, 163, 184)
            for x1, y1, x2, y2 in segs:
                p1 = to_px((x1 - dx + 3426.041)/1000.0, (y1 + 18555.823)/1000.0, c_idx, r_idx)
                p2 = to_px((x2 - dx + 3426.041)/1000.0, (y2 + 18555.823)/1000.0, c_idx, r_idx)
                draw.line([p1, p2], fill=col, width=1)

out_path = r'C:\Users\User\.gemini\antigravity\brain\17cdeb22-38a8-4e04-b15d-67ce64232225\dwg_9clusters_preview.jpg'
img.save(out_path, quality=92)
print('Saved', out_path)
