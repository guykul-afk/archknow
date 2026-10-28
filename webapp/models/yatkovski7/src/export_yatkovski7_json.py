import os
import sys
import json
import math
import aspose.cad as cad
import aspose.pycore as pycore
from shapely.geometry import LineString, MultiLineString, Polygon, Point, box
from shapely.ops import polygonize, unary_union, triangulate
from shapely import snap

sys.stdout.reconfigure(encoding='utf-8')

SCRATCH_DIR = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch"
PROJECT_DIR = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\יטקובסקי 7 פתח תקווה"
DWG_PATH = r"c:\Users\guyku\Downloads\yatkovski7-100-20 (2).dwg"

with open(os.path.join(SCRATCH_DIR, "dwg_frames_and_data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

PLANS_ANCHORS = {
    "basement":   (  1013.29, -76113.86),
    "ground":     ( -2352.16, -77276.82),
    "typical":    ( -6064.08, -77254.11), # Floors 1-4
    "floor_5":    (-14017.36, -77254.11), # Floor 5 (Mini-Penthouse Apt 10)
    "penthouse":  (-16700.74, -77254.11), # Floor 6 (Penthouse Apt 11)
    "roof_main":  (-19350.92, -77254.11), # Roofs & Upper Roof Core
}

# Exact CAD block opening definitions: (bx0, by0, bx1, by1, kind)
DW_BLOCK_DEFS = {
    "D100":    (   0.0,   0.0, 100.0,  15.0, "door"),
    "d80":     (   0.0,   0.0,  80.0,  15.0, "door"),
    "d81":     ( -80.0,   0.0,   0.0,  15.0, "door"),
    "d101":    (   0.0,   0.0, 100.0,  15.0, "door"),
    "d110":    (   0.0,   0.0, 110.0,  15.0, "door"),
    "d111":    (-110.0,   0.0,   0.0,  15.0, "door"),
    "d120":    (   0.0,   0.0, 120.0,  15.0, "door"),
    "w300":    (   0.0,   0.0, 300.0,  22.0, "vitrine"),
    "w200h20": (   0.0,   0.0, 200.0,  22.0, "vitrine"),
    "w160":    (  57.1, -34.3, 217.1, -14.3, "window"),
    "w160h20": (   0.0,   0.0, 160.0,  22.0, "win_tall"),
    "w140":    (  77.1, -34.3, 217.1, -14.3, "window"),
    "w140h20": (   0.0,   0.0, 140.0,  22.0, "win_tall"),
    "w120":    (   0.0,   0.0, 120.0,  22.0, "window"),
    "W100":    (   0.0,   0.0, 100.0,  22.0, "window"),
    "w80":     (   0.0,   0.0,  80.0,  22.0, "window"),
    "w70":     (   0.0,   0.0,  70.0,  15.0, "window"),
    "wh3":     (-100.0, -30.0,   0.0,   0.0, "mamad_win"),
}

def transform_cad_pt(px, py, ins_x, ins_y, sx, sy, rot_deg):
    rad = math.radians(rot_deg)
    cx, cy = math.cos(rad), math.sin(rad)
    x1, y1 = px * sx, py * sy
    rx = x1 * cx - y1 * cy + ins_x
    ry = x1 * cy + y1 * cx + ins_y
    return rx, ry

def triangulate_poly(p):
    ext = [[round(x, 3), round(y, 3)] for x, y in list(p.exterior.coords)[:-1]]
    holes = [[[round(x, 3), round(y, 3)] for x, y in list(h.coords)[:-1]] for h in p.interiors]
    ys = sorted(set(round(pt[1], 3) for pt in ext + [pt for h in holes for pt in h]))
    minx, miny, maxx, maxy = p.bounds
    tris = []
    p_buf = p.buffer(0.002)
    for i in range(len(ys) - 1):
        y0, y1 = ys[i], ys[i+1]
        if y1 - y0 < 0.002:
            continue
        strip = box(minx - 0.1, y0, maxx + 0.1, y1).intersection(p)
        if strip.is_empty:
            continue
        geoms = list(strip.geoms) if hasattr(strip, 'geoms') else [strip]
        for g in geoms:
            if g.geom_type != 'Polygon' or g.area < 0.0005:
                continue
            for t in triangulate(g):
                if p_buf.contains(t) and g.contains(t.representative_point()):
                    tc = list(t.exterior.coords)[:-1]
                    if len(tc) == 3:
                        tris.append([[round(tc[0][0], 3), round(tc[0][1], 3)],
                                     [round(tc[1][0], 3), round(tc[1][1], 3)],
                                     [round(tc[2][0], 3), round(tc[2][1], 3)]])
    return {'exterior': ext, 'holes': holes, 'tris': tris}

EXACT_ROOM_LABELS = {
    "basement": [
        {"x":  0.0, "y":  0.0, "name": "פיר מעלית (טיפוס 1)", "dims": "190×165"},
        {"x": -1.2, "y":  1.5, "name": "לובי מעלית מרתף", "dims": "210×260"},
        {"x": -0.5, "y":  3.2, "name": "חדר מדרגות מוגן", "dims": "260×440"},
        {"x": -6.0, "y":  2.6, "name": "רגלי ממ\"ד + מחסן", "dims": "335×380"},
        {"x": -7.5, "y":  4.2, "name": "חדר משאבות ומאגר מים", "dims": "360×340"},
        {"x": -2.5, "y": 12.0, "name": "מיסעה ורמפת חניה (רמת שירות 2)", "dims": "602×1550"},
        {"x": -2.0, "y": 16.8, "name": "שורת חניות דרומית (#1–#6)", "dims": "1520×500"},
        {"x": -7.8, "y": -5.2, "name": "תאי חניה צפון-מערב (#10–#12)", "dims": "500×740"},
        {"x":  3.5, "y": -7.8, "name": "תאי חניה צפון-מזרח (#8–#9)", "dims": "500×520"},
    ],
    "ground": [
        {"x":  0.5, "y": -1.8, "name": "לובי כניסה ראשי (תקרה כפולה)", "dims": "29.0 מ\"ר"},
        {"x": -5.5, "y": -1.8, "name": "חדר אשפה מאוורר", "dims": "8.5 מ\"ר"},
        {"x": -5.0, "y":  0.6, "name": "מחסן עגלות ואופניים", "dims": "6.0 מ\"ר"},
        {"x":  5.0, "y":  0.6, "name": "חדר גז + מחסן", "dims": "6.0 מ\"ר"},
        {"x": -5.4, "y":  3.0, "name": "מאגר מים ורגלי ממ\"ד", "dims": "10.7 מ\"ק"},
        {"x":  0.0, "y":  0.0, "name": "מעלית וחדר מדרגות", "dims": "310×580"},
        {"x":  0.3, "y":  5.7, "name": "ממ\"ד (דירת גן #1)", "dims": "335×290"},
        {"x": -4.4, "y":  7.3, "name": "מטבח (דירת גן #1)", "dims": "340×310"},
        {"x": -2.4, "y": 10.0, "name": "פינת אוכל", "dims": "300×260"},
        {"x": -6.0, "y": 11.8, "name": "סלון (דירת גן 105 מ\"ר)", "dims": "420×480"},
        {"x": -1.9, "y": 12.3, "name": "חדר שינה 1", "dims": "290×340"},
        {"x":  2.2, "y": 12.3, "name": "סוויטת הורים (דירת גן)", "dims": "340×360"},
        {"x": -2.0, "y": 16.8, "name": "גינה פרטית היקפית (דירה #1)", "dims": "153 מ\"ר"},
    ],
    "typical": [
        # North Apartment (97 sqm gross / 85 sqm main + Sukkah Balcony)
        {"x": -1.2, "y": -6.2, "name": "מרפסת שמש סוכה (צפון)", "dims": "480×240"},
        {"x":  0.5, "y": -3.2, "name": "סלון ופינת אוכל (דירה צפונית 97 מ\"ר)", "dims": "410×460"},
        {"x": -2.8, "y": -3.0, "name": "מטבח (דירה צפונית)", "dims": "310×290"},
        {"x": -5.8, "y": -2.8, "name": "ח. שינה 1 (צפון-מערב)", "dims": "295×340"},
        {"x":  5.6, "y":  0.2, "name": "סוויטת הורים (מזרח)", "dims": "340×360"},
        {"x": -4.4, "y":  3.4, "name": "ממ\"ד (דירה צפונית)", "dims": "335×290"},
        {"x": -7.8, "y":  0.4, "name": "ח. רחצה ומסתור כביסה", "dims": "260×210"},
        # Core
        {"x": -2.2, "y":  0.8, "name": "לובי קומתי ומעלית", "dims": "260×380"},
        {"x": -0.5, "y":  3.2, "name": "חדר מדרגות ופירים", "dims": "260×440"},
        # South Apartment (102 sqm gross / 90 sqm main + Sukkah Balcony)
        {"x":  1.0, "y":  6.4, "name": "ממ\"ד (דירה דרומית)", "dims": "335×290"},
        {"x": -5.8, "y":  6.5, "name": "מטבח (דירה דרומית)", "dims": "340×310"},
        {"x":  3.5, "y":  8.2, "name": "ח. רחצה ומסתור כביסה", "dims": "260×210"},
        {"x": -2.2, "y": 10.3, "name": "פינת אוכל (דירה דרומית 102 מ\"ר)", "dims": "310×260"},
        {"x": -5.5, "y": 11.6, "name": "סלון מרווח (דרום-מערב)", "dims": "420×460"},
        {"x": -1.7, "y": 12.4, "name": "ח. שינה (דרום)", "dims": "290×340"},
        {"x":  1.4, "y": 12.4, "name": "סוויטת הורים (דרום-מזרח)", "dims": "340×360"},
        {"x": -3.8, "y": 15.2, "name": "מרפסת שמש סוכה (דרום)", "dims": "680×180"},
    ],
    "floor_5": [
        # Mini-Penthouse Apt 10 (150 sqm gross / 133 sqm main + 2 Roof Terraces)
        {"x": -1.5, "y": -4.6, "name": "מרפסת גג צפונית + פרגולה וסוכה", "dims": "1120×340"},
        {"x": -5.8, "y": -0.8, "name": "סלון פנורמי (מיני-פנטהאוז 150 מ\"ר)", "dims": "560×480"},
        {"x":  5.6, "y":  0.5, "name": "סוויטת הורים ראשית (מזרח)", "dims": "350×410"},
        {"x": -5.6, "y":  3.4, "name": "מטבח שף ופינת אוכל", "dims": "480×360"},
        {"x": -1.5, "y":  0.5, "name": "לובי מעלית פרטי ומדרגות", "dims": "260×380"},
        {"x":  1.4, "y":  6.4, "name": "ממ\"ד קומה 5", "dims": "335×290"},
        {"x": -5.9, "y":  6.7, "name": "ח. שינה מערבי 1", "dims": "320×340"},
        {"x":  3.6, "y":  8.3, "name": "ח. רחצה ומסתור כביסה", "dims": "260×210"},
        {"x": -6.0, "y": 10.1, "name": "ח. שינה מערבי 2", "dims": "320×340"},
        {"x": -3.6, "y": 11.6, "name": "ח. שינה דרומי 3", "dims": "300×340"},
        {"x": -0.2, "y": 11.6, "name": "ח. שינה דרומי 4", "dims": "300×340"},
        {"x": -3.8, "y": 14.0, "name": "מרפסת גג דרומית + פרגולה", "dims": "980×260"},
    ],
    "penthouse": [
        # Penthouse Apt 11 (125 sqm gross / 102 sqm main + North Balcony & Giant South Roof Terrace)
        {"x": -3.2, "y": -3.6, "name": "מרפסת שמש צפונית (פנטהאוז)", "dims": "720×160"},
        {"x": -5.8, "y": -0.8, "name": "סלון אירוח פנטהאוז (125 מ\"ר)", "dims": "540×460"},
        {"x":  5.6, "y":  0.6, "name": "סוויטת הורים פנטהאוז", "dims": "350×410"},
        {"x": -5.6, "y":  3.4, "name": "מטבח שף ואי מרכזי", "dims": "460×350"},
        {"x": -1.5, "y":  0.5, "name": "לובי מעלית קומה 6", "dims": "260×380"},
        {"x":  1.0, "y":  6.4, "name": "ממ\"ד פנטהאוז", "dims": "335×290"},
        {"x": -2.8, "y":  7.4, "name": "מחסן צמוד ופיר אוורור", "dims": "220×240"},
        {"x": -6.0, "y":  7.6, "name": "ח. שינה פנטהאוז 1", "dims": "320×330"},
        {"x": -5.8, "y": 10.5, "name": "ח. שינה פנטהאוז 2", "dims": "320×330"},
        {"x": -1.5, "y": 12.2, "name": "מרפסת גג פנטהאוז דרומית + פרגולה קלה", "dims": "860×450"},
    ],
    "roof_main": [
        {"x":  0.0, "y":  0.0, "name": "חדר מכונות מעלית וגג עליון", "dims": "240×220"},
        {"x": -0.5, "y":  3.2, "name": "יציאה לגג + חלון רפפה לשחרור עשן", "dims": "260×440"},
        {"x": -4.0, "y":  1.5, "name": "גג בטון לבן + קולטים סולאריים", "dims": "קו עיגון חיים"},
    ],
}

def expand_furn_blocks():
    img = cad.Image.load(DWG_PATH)
    cimg = pycore.cast(cad.fileformats.cad.CadImage, img)
    blocks = dict(zip(cimg.block_entities.keys, cimg.block_entities.values))
    co = cad.fileformats.cad.cadobjects
    block_segs = {}
    for bname, bobj in blocks.items():
        if bname.startswith("*Model") or bname.startswith("*Paper"):
            continue
        blk = pycore.cast(co.CadBlockEntity, bobj)
        bp = getattr(blk, 'base_point', None)
        bpx, bpy = (bp.x, bp.y) if bp else (0.0, 0.0)
        segs = []
        for e in blk.entities:
            t = e.type_name.name
            if t == "LINE":
                l = pycore.cast(co.CadLine, e)
                segs.append((l.first_point.x - bpx, l.first_point.y - bpy, l.second_point.x - bpx, l.second_point.y - bpy))
            elif t == "LWPOLYLINE":
                p = pycore.cast(co.CadLwPolyline, e)
                pts = [(pt.x - bpx, pt.y - bpy) for pt in p.coordinates]
                if len(pts) >= 2:
                    if getattr(p, 'flags', 0) & 1:
                        pts.append(pts[0])
                    for i in range(len(pts) - 1):
                        segs.append((pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1]))
        if segs:
            block_segs[bname] = segs
    return block_segs

def process_all_plans():
    block_segs = expand_furn_blocks()
    out_plans = {}

    for pname, (ax, ay) in PLANS_ANCHORS.items():
        wall_lines = []
        cad_segs = []
        furn_segs = []

        # 1. Extract wall lines from layers '8' and '4'
        for layer in ('8', '4'):
            for p in data['lwpolys_by_layer'].get(layer, []):
                pts = [(round((x - ax)/100.0, 4), round(-(y - ay)/100.0, 4)) for x, y in p]
                for i in range(len(pts) - 1):
                    p1, p2 = pts[i], pts[i+1]
                    if -11.8 <= p1[0] <= 7.2 and -12.5 <= p1[1] <= 19.8 and -11.8 <= p2[0] <= 7.2 and -12.5 <= p2[1] <= 19.8:
                        L = math.hypot(p2[0]-p1[0], p2[1]-p1[1])
                        if L >= 0.04:
                            wall_lines.append(LineString([p1, p2]))
                            cad_segs.append([round(p1[0], 3), round(p1[1], 3), round(p2[0], 3), round(p2[1], 3)])
            for l in data['lines_by_layer'].get(layer, []):
                p1 = (round((l[0] - ax)/100.0, 4), round(-(l[1] - ay)/100.0, 4))
                p2 = (round((l[2] - ax)/100.0, 4), round(-(l[3] - ay)/100.0, 4))
                if -11.8 <= p1[0] <= 7.2 and -12.5 <= p1[1] <= 19.8 and -11.8 <= p2[0] <= 7.2 and -12.5 <= p2[1] <= 19.8:
                    L = math.hypot(p2[0]-p1[0], p2[1]-p1[1])
                    if L >= 0.04:
                        wall_lines.append(LineString([p1, p2]))
                        cad_segs.append([round(p1[0], 3), round(p1[1], 3), round(p2[0], 3), round(p2[1], 3)])

        # 2. Extract detail lines from layers 'D', '2', 'HID', 'PARK'
        for layer in ('D', '2', 'HID', 'PARK'):
            for p in data['lwpolys_by_layer'].get(layer, []):
                pts = [(round((x - ax)/100.0, 3), round(-(y - ay)/100.0, 3)) for x, y in p]
                for i in range(len(pts) - 1):
                    p1, p2 = pts[i], pts[i+1]
                    if -11.8 <= p1[0] <= 7.2 and -12.5 <= p1[1] <= 19.8 and -11.8 <= p2[0] <= 7.2 and -12.5 <= p2[1] <= 19.8:
                        cad_segs.append([p1[0], p1[1], p2[0], p2[1]])
            for l in data['lines_by_layer'].get(layer, []):
                p1 = (round((l[0] - ax)/100.0, 3), round(-(l[1] - ay)/100.0, 3))
                p2 = (round((l[2] - ax)/100.0, 3), round(-(l[3] - ay)/100.0, 3))
                if -11.8 <= p1[0] <= 7.2 and -12.5 <= p1[1] <= 19.8 and -11.8 <= p2[0] <= 7.2 and -12.5 <= p2[1] <= 19.8:
                    cad_segs.append([p1[0], p1[1], p2[0], p2[1]])

        # 3. Extract openings & furniture inserts
        openings = []
        for ins in data['inserts']:
            ix_m = (ins['x'] - ax) / 100.0
            iy_m = -(ins['y'] - ay) / 100.0
            if not (-11.8 <= ix_m <= 7.2 and -12.5 <= iy_m <= 19.8):
                continue
            bname = ins['block']
            # Expand furniture / sanitary / stair / solar block lines
            if ins['layer'] in ('rehut', 'FURN', 'SANIT', '2', '1-solar') and bname in block_segs:
                for x1, y1, x2, y2 in block_segs[bname]:
                    mx1, my1 = transform_cad_pt(x1, y1, ins['x'], ins['y'], ins['sx'], ins['sy'], ins['rot'])
                    mx2, my2 = transform_cad_pt(x2, y2, ins['x'], ins['y'], ins['sx'], ins['sy'], ins['rot'])
                    furn_segs.append([
                        round((mx1 - ax)/100.0, 3), round(-(my1 - ay)/100.0, 3),
                        round((mx2 - ax)/100.0, 3), round(-(my2 - ay)/100.0, 3)
                    ])
            elif bname.startswith('m17') and bname in block_segs:
                for x1, y1, x2, y2 in block_segs[bname]:
                    mx1, my1 = transform_cad_pt(x1, y1, ins['x'], ins['y'], ins['sx'], ins['sy'], ins['rot'])
                    mx2, my2 = transform_cad_pt(x2, y2, ins['x'], ins['y'], ins['sx'], ins['sy'], ins['rot'])
                    cad_segs.append([
                        round((mx1 - ax)/100.0, 3), round(-(my1 - ay)/100.0, 3),
                        round((mx2 - ax)/100.0, 3), round(-(my2 - ay)/100.0, 3)
                    ])
            # Door/Window openings
            if bname in DW_BLOCK_DEFS:
                bx0, by0, bx1, by1, kind = DW_BLOCK_DEFS[bname]
                corners = [
                    transform_cad_pt(bx0, by0, ins['x'], ins['y'], ins['sx'], ins['sy'], ins['rot']),
                    transform_cad_pt(bx1, by0, ins['x'], ins['y'], ins['sx'], ins['sy'], ins['rot']),
                    transform_cad_pt(bx1, by1, ins['x'], ins['y'], ins['sx'], ins['sy'], ins['rot']),
                    transform_cad_pt(bx0, by1, ins['x'], ins['y'], ins['sx'], ins['sy'], ins['rot']),
                ]
                xs = [(c[0] - ax)/100.0 for c in corners]
                ys = [-(c[1] - ay)/100.0 for c in corners]
                ox0, ox1 = round(min(xs), 3), round(max(xs), 3)
                oy0, oy1 = round(min(ys), 3), round(max(ys), 3)
                orient = 'H' if (ox1 - ox0) >= (oy1 - oy0) else 'V'
                openings.append([orient, ox0, oy0, ox1, oy1, kind])

        # 4. Polygonize wall segments and subtract openings
        h_segs, v_segs = [], []
        for l in wall_lines:
            (x1, y1), (x2, y2) = l.coords[0], l.coords[-1]
            if abs(y1 - y2) < 0.015 and abs(x2 - x1) >= 0.05:
                h_segs.append((0.5*(y1+y2), min(x1,x2), max(x1,x2)))
            elif abs(x1 - x2) < 0.015 and abs(y2 - y1) >= 0.05:
                v_segs.append((0.5*(x1+x2), min(y1,y2), max(y1,y2)))

        pair_boxes = []
        for i in range(len(h_segs)):
            yA, xA0, xA1 = h_segs[i]
            for j in range(i+1, len(h_segs)):
                yB, xB0, xB1 = h_segs[j]
                if 0.075 <= abs(yA - yB) <= 0.35:
                    ox0, ox1 = max(xA0, xB0), min(xA1, xB1)
                    if ox1 - ox0 >= 0.05:
                        ym0, ym1 = min(yA, yB), max(yA, yB)
                        if not any(ym0 + 0.03 < h_segs[k][0] < ym1 - 0.03 and min(ox1, h_segs[k][2]) - max(ox0, h_segs[k][1]) > 0.05 for k in range(len(h_segs))):
                            pair_boxes.append(box(ox0, ym0, ox1, ym1))
        for i in range(len(v_segs)):
            xA, yA0, yA1 = v_segs[i]
            for j in range(i+1, len(v_segs)):
                xB, yB0, yB1 = v_segs[j]
                if 0.075 <= abs(xA - xB) <= 0.35:
                    oy0, oy1 = max(yA0, yB0), min(yA1, yB1)
                    if oy1 - oy0 >= 0.05:
                        xm0, xm1 = min(xA, xB), max(xA, xB)
                        if not any(xm0 + 0.03 < v_segs[k][0] < xm1 - 0.03 and min(oy1, v_segs[k][2]) - max(oy0, v_segs[k][1]) > 0.05 for k in range(len(v_segs))):
                            pair_boxes.append(box(xm0, oy0, xm1, oy1))

        # For basement, add the outer perimeter retaining wall box (X=[-11.15, 6.60], Y=[-11.20, 19.30])
        if pname == "basement":
            outer_b = box(-11.15, -11.20, 6.60, 19.30)
            inner_b = box(-10.85, -10.90, 6.30, 19.00)
            pair_boxes.append(outer_b.difference(inner_b))

        mls = MultiLineString(wall_lines)
        noded = unary_union(snap(mls, mls, 0.02))
        polys = [p for p in polygonize(noded) if 0.01 <= p.area < 18.0]
        u_walls = unary_union(polys + pair_boxes).buffer(0.003, join_style=2).buffer(-0.003, join_style=2).simplify(0.002, preserve_topology=True)

        # Boolean subtract openings so walls never bridge across windows/doors
        cut_boxes = []
        for orient, x0, y0, x1, y1, kind in openings:
            pad_perp = 0.16 if kind != 'door' else 0.06
            if orient == 'H':
                cut_boxes.append(box(x0 - 0.005, y0 - pad_perp, x1 + 0.005, y1 + pad_perp))
            else:
                cut_boxes.append(box(x0 - pad_perp, y0 - 0.005, x1 + pad_perp, y1 + 0.005))
        if cut_boxes:
            u_walls = u_walls.difference(unary_union(cut_boxes)).buffer(0.001, join_style=2).buffer(-0.001, join_style=2)

        final_walls = list(u_walls.geoms) if hasattr(u_walls, 'geoms') else ([u_walls] if not u_walls.is_empty else [])
        wall_polys_json = [triangulate_poly(p) for p in final_walls if p.area >= 0.015]
        room_labels = EXACT_ROOM_LABELS.get(pname, [])
        door_cnt = len([o for o in openings if o[5] == 'door'])
        ext_cnt = len([o for o in openings if o[5] != 'door'])
        print(f"{pname:10s}: walls={len(wall_polys_json):3d}, openings={len(openings):3d} (ext={ext_cnt:2d}, doors={door_cnt:2d}), furn={len(furn_segs):4d}, cad={len(cad_segs):4d}, labels={len(room_labels):2d}")
        out_plans[pname] = {
            "wall_polys": wall_polys_json,
            "openings": openings,
            "furn_lines": furn_segs,
            "cad_lines": cad_segs,
            "room_labels": room_labels,
        }
    return out_plans

def build_crm_data():
    """
    11-Apartment Catalog & 12-Parking Stall CRM Dataset for Yatkovski 7, Petah Tikva:
      - Combination Deal: 52% Kolsky (6 developer units: #1, #3, #6, #8, #10, #11) / 48% Ben Aharon Landowners (5 owner units: #2, #4, #5, #7, #9)
      - Exact Areas per DWG Apartment Table & Floor Plans:
        - Apt 1 (Ground Floor Garden Apt): 4 Rooms, 83 sqm main / 105 sqm gross + 153 sqm Private Garden
        - Apts 2, 4, 6, 8 (Floors 1-4 South Wing): 4 Rooms, 90 sqm main / 102 sqm gross + 14 sqm South Sukkah Balcony
        - Apts 3, 5, 7, 9 (Floors 1-4 North Wing facing Yatkovski St): 4 Rooms, 85 sqm main / 97 sqm gross + 12 sqm North Sukkah Balcony
        - Apt 10 (Floor 5 Full-Floor Mini-Penthouse): 5 Rooms, 133 sqm main / 150 sqm gross + 64 sqm North & South Roof Terraces with Pergolas
        - Apt 11 (Floor 6 Full-Floor Penthouse): 5 Rooms, 102 sqm main / 125 sqm gross + 52 sqm North Balcony & South Roof Terrace with Pergola
    """
    parking_stalls = [
        {"num": 1,  "level": "basement", "x": -9.1, "y": 16.5, "w": 2.6, "d": 5.0},
        {"num": 2,  "level": "basement", "x": -6.0, "y": 16.5, "w": 2.6, "d": 5.0},
        {"num": 3,  "level": "basement", "x": -3.2, "y": 16.5, "w": 2.6, "d": 5.0},
        {"num": 4,  "level": "basement", "x": -0.3, "y": 16.5, "w": 2.5, "d": 5.0},
        {"num": 5,  "level": "basement", "x":  2.3, "y": 16.5, "w": 2.6, "d": 5.0},
        {"num": 6,  "level": "basement", "x":  5.5, "y": 16.5, "w": 2.8, "d": 5.0},
        {"num": 7,  "level": "basement", "x": -2.4, "y":  7.2, "w": 2.8, "d": 5.0},
        {"num": 8,  "level": "basement", "x":  3.5, "y": -6.5, "w": 5.0, "d": 2.5},
        {"num": 9,  "level": "basement", "x":  3.5, "y": -9.3, "w": 5.0, "d": 2.6},
        {"num": 10, "level": "basement", "x": -8.4, "y": -7.5, "w": 5.0, "d": 2.5},
        {"num": 11, "level": "basement", "x": -8.0, "y": -5.1, "w": 5.0, "d": 2.4},
        {"num": 12, "level": "basement", "x": -7.6, "y": -3.1, "w": 5.0, "d": 2.4},
    ]

    units = [
        # Apt 1: Ground Floor Garden Apartment
        {
            "id": "apt_1", "aptNum": 1, "bldg": 7, "wing": "S",
            "name": "דירת גן 1", "shortBadge": "דירת גן #1",
            "floorNum": 0, "floorId": "f0", "floorLabel": "קומת קרקע (דירת גן)",
            "rooms": 4, "typeHe": "דירת גן 4 חדרים דרומית + 153 מ\"ר גינה פרטית",
            "area": 105, "mainArea": 83, "balcony": 153,
            "directions": "דרום, מערב, מזרח (3 כיווני אוויר)",
            "status": "available", "statusHe": "זמין לשיווק · קולסקי",
            "price": 3650000,
            "z0": 0.00, "z1": 3.85,
            "bbox": [-8.14, 3.80, 4.00, 14.36],
            "bx": -2.5, "by": 14.8, "bz": 1.80,
            "balcPt": [-2.5, 15.8], "lookDir": "S",
            "parkingNum": 7, "parkingLevel": "basement", "parkingX": -2.4, "parkingY": 7.2,
        }
    ]

    apt_num = 2
    for flr in range(1, 5):
        z0 = round(3.85 + (flr - 1) * 3.15, 2)
        z1 = round(z0 + 3.15, 2)
        flr_id = f"f{flr}"
        flr_label = f"קומה {flr}"

        # South Apartment (Apts 2, 4, 6, 8): 102 sqm gross (90 sqm main) + 14 sqm Sukkah Balcony
        is_owner_s = flr in (1, 2)
        st_s = parking_stalls[apt_num - 2]
        units.append({
            "id": f"apt_{apt_num}", "aptNum": apt_num, "bldg": 7, "wing": "S",
            "name": f"דירה {apt_num}", "shortBadge": f"דירה {apt_num}",
            "floorNum": flr, "floorId": flr_id, "floorLabel": flr_label,
            "rooms": 4, "typeHe": "דירת 4 חדרים עורפית שקטה + מרפסת סוכה",
            "area": 102, "mainArea": 90, "balcony": 14,
            "directions": "דרום, מערב, מזרח (3 כיווני אוויר)",
            "status": "owner" if is_owner_s else "available",
            "statusHe": "דירת בעלים (בן אהרון)" if is_owner_s else "זמין לשיווק · קולסקי",
            "price": 3080000 + (flr - 1) * 45000,
            "z0": z0, "z1": z1,
            "bbox": [-8.14, 4.80, 4.00, 15.77],
            "bx": -2.5, "by": 15.6, "bz": round(0.5*(z0+z1), 2),
            "balcPt": [-3.8, 15.2], "lookDir": "S",
            "parkingNum": st_s["num"], "parkingLevel": "basement", "parkingX": st_s["x"], "parkingY": st_s["y"],
        })
        apt_num += 1

        # North Apartment (Apts 3, 5, 7, 9): 97 sqm gross (85 sqm main) + 12 sqm Sukkah Balcony
        is_owner_n = flr in (2, 3, 4)
        st_n = parking_stalls[apt_num - 2]
        units.append({
            "id": f"apt_{apt_num}", "aptNum": apt_num, "bldg": 7, "wing": "N",
            "name": f"דירה {apt_num}", "shortBadge": f"דירה {apt_num}",
            "floorNum": flr, "floorId": flr_id, "floorLabel": flr_label,
            "rooms": 4, "typeHe": "דירת 4 חדרים חזיתית (רח' יטקובסקי) + מרפסת סוכה",
            "area": 97, "mainArea": 85, "balcony": 12,
            "directions": "צפון (חזית), מערב, מזרח (3 כיווני אוויר)",
            "status": "owner" if is_owner_n else "available",
            "statusHe": "דירת בעלים (בן אהרון)" if is_owner_n else "זמין לשיווק · קולסקי",
            "price": 2980000 + (flr - 1) * 45000,
            "z0": z0, "z1": z1,
            "bbox": [-8.14, -7.32, 6.95, 3.80],
            "bx": -1.2, "by": -6.8, "bz": round(0.5*(z0+z1), 2),
            "balcPt": [-1.2, -6.2], "lookDir": "N",
            "parkingNum": st_n["num"], "parkingLevel": "basement", "parkingX": st_n["x"], "parkingY": st_n["y"],
        })
        apt_num += 1

    # Apt 10: Floor 5 Full-Floor Mini-Penthouse (150 sqm gross / 133 sqm main + 64 sqm North & South Roof Terraces)
    st_10 = parking_stalls[9]
    units.append({
        "id": "apt_10", "aptNum": 10, "bldg": 7, "wing": "F5",
        "name": "מיני-פנטהאוז דירה 10", "shortBadge": "מיני-פנטהאוז #10",
        "floorNum": 5, "floorId": "f5", "floorLabel": "קומה 5 (דירה על כל הקומה)",
        "rooms": 5, "typeHe": "מיני-פנטהאוז קומתי 5 חדרים + 2 מרפסות גג ופרגולות",
        "area": 150, "mainArea": 133, "balcony": 64,
        "directions": "4 כיווני אוויר מלאים (צפון, דרום, מזרח, מערב)",
        "status": "available", "statusHe": "זמין לשיווק · דירת דגל קולסקי",
        "price": 4950000,
        "z0": 16.53, "z1": 19.76,
        "bbox": [-8.14, -7.32, 6.95, 15.77],
        "bx": -1.5, "by": -5.2, "bz": 18.15,
        "balcPt": [-1.5, -4.6], "lookDir": "N",
        "parkingNum": st_10["num"], "parkingLevel": "basement", "parkingX": st_10["x"], "parkingY": st_10["y"],
    })

    # Apt 11: Floor 6 Full-Floor Luxury Penthouse (125 sqm gross / 102 sqm main + 52 sqm Roof Terraces)
    st_11 = parking_stalls[10]
    units.append({
        "id": "apt_11", "aptNum": 11, "bldg": 7, "wing": "PH",
        "name": "פנטהאוז דירה 11", "shortBadge": "פנטהאוז #11",
        "floorNum": 6, "floorId": "f6", "floorLabel": "קומה 6 (פנטהאוז על כל הקומה)",
        "rooms": 5, "typeHe": "פנטהאוז יוקרה על קומה שלמה + מרפסות גג, פרגולות ומחסן צמוד",
        "area": 125, "mainArea": 102, "balcony": 52,
        "directions": "4 כיווני אוויר מלאים (צפון, דרום, מזרח, מערב)",
        "status": "available", "statusHe": "זמין לשיווק · פנטהאוז דגל קולסקי",
        "price": 5350000,
        "z0": 19.76, "z1": 22.99,
        "bbox": [-8.14, -7.32, 6.95, 14.50],
        "bx": -1.5, "by": 12.2, "bz": 21.38,
        "balcPt": [-1.5, 12.2], "lookDir": "S",
        "parkingNum": st_11["num"], "parkingLevel": "basement", "parkingX": st_11["x"], "parkingY": st_11["y"],
    })

    return {"units": units, "parking_stalls": parking_stalls}

def build_compact_bim():
    """
    Generates compact_bim.json strictly adhering to compact_bim_schema.json and engineering checks in validate_bim.py.
    """
    bim = {
        "meta": {
            "project_name": "יטקובסקי אחים 7 (7א), פתח תקווה | גוש 6714 חלקה 470 | תב\"ע 410-1272517",
            "scale": "1:100",
            "datum_abs": 57.00,
            "defaults": {
                "door_h": 2.10,
                "win_lintel": 2.10,
                "win_sill": 1.05,
                "ext_wall_t": 0.25,
                "int_wall_t": 0.10,
                "mamad_wall_t": 0.30,
                "slab_t": 0.25
            },
            "notes": "מודל BIM אדריכלי מלא מתוך קובץ ה-DWG המקורי yatkovski7-100-20 (2).dwg ותוכנית מפורטת מאושרת 410-1272517"
        },
        "site": {
            "lot_boundary": [[-11.15, -11.20], [6.95, -11.20], [6.95, 19.30], [-11.15, 19.30]],
            "building_line": [[-11.15, -11.20], [6.95, -11.20], [6.95, 19.30], [-11.15, 19.30]],
            "ramps": [
                {
                    "id": "ramp_basement",
                    "start": [-9.50, -10.00],
                    "end": [-9.50, 19.20],
                    "width": 3.20,
                    "slope_pct": 15.0,
                    "target_z": -4.38
                }
            ]
        },
        "levels": [
            {"level_id": "L_B1", "name": "קומת מרתף חניה (-1)", "z": -4.38, "h": 4.38},
            {"level_id": "L_0",  "name": "קומת קרקע (לובי ודירת גן)", "z": 0.00, "h": 3.85},
            {"level_id": "L_TYP_1_3", "name": "קומות 1–3 טיפוסיות", "z_list": [3.85, 7.00, 10.15], "h": 3.15},
            {"level_id": "L_4",  "name": "קומה 4 טיפוסית", "z": 13.30, "h": 3.23},
            {"level_id": "L_5",  "name": "קומה 5 (מיני-פנטהאוז קומתי)", "z": 16.53, "h": 3.23},
            {"level_id": "L_6",  "name": "קומה 6 (פנטהאוז קומתי)", "z": 19.76, "h": 3.23, "pergola_z": 22.50, "parapet_z": 24.05},
            {"level_id": "L_ROOF", "name": "קומת גג טכני ועליית גג", "z": 22.99, "h": 3.00, "parapet_z": 25.99}
        ],
        "templates": {
            "tpl_basement": {
                "slab": [[-11.15, -11.20], [6.60, -11.20], [6.60, 19.30], [-11.15, 19.30]],
                "w": [
                    [-11.15, -11.20,  6.60, -11.20, 0.30, "retaining", "concrete"],
                    [  6.60, -11.20,  6.60,  19.30, 0.30, "retaining", "concrete"],
                    [  6.60,  19.30,-11.15,  19.30, 0.30, "retaining", "concrete"],
                    [-11.15,  19.30,-11.15, -11.20, 0.30, "retaining", "concrete"],
                    [ -1.10,  -0.95,  1.10,  -0.95, 0.25, "core", "concrete"],
                    [  1.10,  -0.95,  1.10,   5.20, 0.25, "core", "concrete"],
                    [  1.10,   5.20, -1.10,   5.20, 0.25, "core", "concrete"],
                    [ -1.10,   5.20, -1.10,  -0.95, 0.25, "core", "concrete"],
                    [ -5.80,   1.80, -1.10,   1.80, 0.30, "mamad", "concrete"],
                    [ -5.80,   1.80, -5.80,   7.50, 0.30, "mamad", "concrete"],
                    [ -5.80,   7.50, -1.10,   7.50, 0.30, "mamad", "concrete"]
                ],
                "o": [
                    [7, 1.80, 1.10, "d", 0.0, 2.10],
                    [8, 1.50, 1.10, "md", 0.0, 2.10],
                    [9, 2.00, 1.00, "mw", 1.05, 1.05]
                ],
                "spaces": [
                    {"name": "מרתף חניה ומיסעה", "center": [-2.0, 11.0]},
                    {"name": "לובי מעלית וחדר מדרגות", "center": [0.0, 2.0]},
                    {"name": "רגלי ממ\"ד וחדר משאבות", "center": [-3.5, 4.5]}
                ]
            },
            "tpl_ground": {
                "slab": [[-8.14, -5.20], [6.60, -5.20], [6.60, 3.80], [4.00, 3.80], [4.00, 14.36], [-8.14, 14.36]],
                "w": [
                    [-8.14, -5.20,  6.60, -5.20, 0.25, "ext", "stone"],
                    [ 6.60, -5.20,  6.60,  3.80, 0.25, "ext", "stone"],
                    [ 6.60,  3.80,  4.00,  3.80, 0.25, "ext", "stone"],
                    [ 4.00,  3.80,  4.00, 14.36, 0.25, "ext", "white_plaster"],
                    [ 4.00, 14.36, -8.14, 14.36, 0.25, "ext", "white_plaster"],
                    [-8.14, 14.36, -8.14, -5.20, 0.25, "ext", "white_plaster"],
                    [-1.10, -0.95,  1.10, -0.95, 0.25, "core", "concrete"],
                    [ 1.10, -0.95,  1.10,  5.20, 0.25, "core", "concrete"],
                    [ 1.10,  5.20, -1.10,  5.20, 0.25, "core", "concrete"],
                    [-1.10,  5.20, -1.10, -0.95, 0.25, "core", "concrete"],
                    [-1.10,  5.20,  3.60,  5.20, 0.30, "mamad", "concrete"],
                    [ 3.60,  5.20,  3.60,  8.10, 0.30, "mamad", "concrete"],
                    [ 3.60,  8.10, -1.10,  8.10, 0.30, "mamad", "concrete"]
                ],
                "o": [
                    [0, 8.20, 1.60, "sw", 0.0, 2.40],
                    [4, 2.50, 1.60, "w", 0.40, 1.80],
                    [4, 8.00, 3.00, "sw", 0.0, 2.20],
                    [11, 0.80, 1.00, "mw", 1.05, 1.05],
                    [12, 1.20, 0.80, "md", 0.0, 2.05]
                ],
                "spaces": [
                    {"name": "לובי כניסה ראשי", "center": [0.5, -1.8]},
                    {"name": "חדר אשפה", "center": [-5.5, -1.8]},
                    {"name": "מחסן עגלות ואופניים", "center": [-5.0, 0.6]},
                    {"name": "סלון ומטבח (דירת גן)", "center": [-5.0, 10.5]},
                    {"name": "ממ\"ד (דירת גן)", "center": [1.0, 6.4]},
                    {"name": "חדרי שינה (דירת גן)", "center": [0.5, 12.3]}
                ]
            },
            "tpl_typical": {
                "slab": [[-8.14, -5.21], [6.95, -5.21], [6.95, 3.80], [4.00, 3.80], [4.00, 14.36], [-8.14, 14.36]],
                "balconies": [
                    {"id": "balc_north", "polygon": [[-3.80, -7.32], [1.20, -7.32], [1.20, -5.21], [-3.80, -5.21]], "railing_type": "glass", "railing_h": 1.05},
                    {"id": "balc_south", "polygon": [[-7.56, 14.36], [0.50, 14.36], [0.50, 15.77], [-7.56, 15.77]], "railing_type": "glass", "railing_h": 1.05}
                ],
                "w": [
                    [-8.14, -5.21,  6.95, -5.21, 0.25, "ext", "stone"],
                    [ 6.95, -5.21,  6.95,  3.80, 0.25, "ext", "white_plaster"],
                    [ 6.95,  3.80,  4.00,  3.80, 0.25, "ext", "white_plaster"],
                    [ 4.00,  3.80,  4.00, 14.36, 0.25, "ext", "white_plaster"],
                    [ 4.00, 14.36, -8.14, 14.36, 0.25, "ext", "white_plaster"],
                    [-8.14, 14.36, -8.14, -5.21, 0.25, "ext", "white_plaster"],
                    [-1.10, -0.95,  1.10, -0.95, 0.25, "core", "concrete"],
                    [ 1.10, -0.95,  1.10,  5.20, 0.25, "core", "concrete"],
                    [ 1.10,  5.20, -1.10,  5.20, 0.25, "core", "concrete"],
                    [-1.10,  5.20, -1.10, -0.95, 0.25, "core", "concrete"],
                    [-6.20,  1.80, -2.80,  1.80, 0.30, "mamad", "concrete"],
                    [-6.20,  1.80, -6.20,  4.70, 0.30, "mamad", "concrete"],
                    [-6.20,  4.70, -2.80,  4.70, 0.30, "mamad", "concrete"],
                    [-1.10,  5.20,  3.60,  5.20, 0.30, "mamad", "concrete"],
                    [ 3.60,  5.20,  3.60,  8.10, 0.30, "mamad", "concrete"],
                    [ 3.60,  8.10, -1.10,  8.10, 0.30, "mamad", "concrete"]
                ],
                "o": [
                    [0, 6.50, 3.00, "sw", 0.0, 2.20],
                    [0, 11.00, 1.60, "w", 1.05, 1.10],
                    [4, 2.50, 1.60, "w", 1.05, 1.10],
                    [4, 8.00, 3.00, "sw", 0.0, 2.20],
                    [5, 2.00, 1.40, "w", 1.05, 1.10],
                    [5, 5.50, 1.40, "w", 1.05, 1.10],
                    [5, 9.00, 1.40, "w", 1.05, 1.10],
                    [11, 0.80, 1.00, "mw", 1.05, 1.05],
                    [10, 1.00, 0.80, "md", 0.0, 2.05],
                    [14, 0.80, 1.00, "mw", 1.05, 1.05],
                    [15, 1.20, 0.80, "md", 0.0, 2.05]
                ],
                "spaces": [
                    {"name": "סלון ומטבח (דירה צפונית)", "center": [-1.0, -3.1]},
                    {"name": "ממ\"ד (דירה צפונית)", "center": [-4.4, 3.4]},
                    {"name": "סוויטת הורים (דירה צפונית)", "center": [5.6, 0.2]},
                    {"name": "לובי קומתי וחדר מדרגות", "center": [-1.0, 2.0]},
                    {"name": "סלון ומטבח (דירה דרומית)", "center": [-5.5, 9.5]},
                    {"name": "ממ\"ד (דירה דרומית)", "center": [1.0, 6.4]},
                    {"name": "חדרי שינה (דירה דרומית)", "center": [0.0, 12.4]}
                ]
            },
            "tpl_floor5": {
                "slab": [[-8.14, -2.65], [6.95, -2.65], [6.95, 3.80], [4.00, 3.80], [4.00, 12.16], [-8.14, 12.16]],
                "balconies": [
                    {"id": "terrace_f5_north", "polygon": [[-8.14, -5.21], [6.95, -5.21], [6.95, -2.65], [-8.14, -2.65]], "railing_type": "glass", "railing_h": 1.05},
                    {"id": "terrace_f5_south", "polygon": [[-8.14, 12.16], [4.00, 12.16], [4.00, 15.77], [-8.14, 15.77]], "railing_type": "glass", "railing_h": 1.05}
                ],
                "pergolas": [
                    {"id": "perg_f5_n", "polygon": [[-6.50, -5.00], [3.50, -5.00], [3.50, -2.65], [-6.50, -2.65]], "type": "light_aluminum", "z_offset": 2.60},
                    {"id": "perg_f5_s", "polygon": [[-7.50, 12.16], [2.50, 12.16], [2.50, 15.20], [-7.50, 15.20]], "type": "light_aluminum", "z_offset": 2.60}
                ],
                "w": [
                    [-8.14, -2.65,  6.95, -2.65, 0.25, "ext", "stone"],
                    [ 6.95, -2.65,  6.95,  3.80, 0.25, "ext", "white_plaster"],
                    [ 6.95,  3.80,  4.00,  3.80, 0.25, "ext", "white_plaster"],
                    [ 4.00,  3.80,  4.00, 12.16, 0.25, "ext", "white_plaster"],
                    [ 4.00, 12.16, -8.14, 12.16, 0.25, "ext", "white_plaster"],
                    [-8.14, 12.16, -8.14, -2.65, 0.25, "ext", "white_plaster"],
                    [-1.10, -0.95,  1.10, -0.95, 0.25, "core", "concrete"],
                    [ 1.10, -0.95,  1.10,  5.20, 0.25, "core", "concrete"],
                    [ 1.10,  5.20, -1.10,  5.20, 0.25, "core", "concrete"],
                    [-1.10,  5.20, -1.10, -0.95, 0.25, "core", "concrete"],
                    [-1.10,  5.20,  3.60,  5.20, 0.30, "mamad", "concrete"],
                    [ 3.60,  5.20,  3.60,  8.10, 0.30, "mamad", "concrete"],
                    [ 3.60,  8.10, -1.10,  8.10, 0.30, "mamad", "concrete"]
                ],
                "o": [
                    [0, 1.70, 3.00, "sw", 0.0, 2.20],
                    [0, 5.80, 3.00, "sw", 0.0, 2.20],
                    [4, 2.00, 2.20, "sw", 0.0, 2.20],
                    [4, 6.00, 2.20, "sw", 0.0, 2.20],
                    [11, 0.80, 1.00, "mw", 1.05, 1.05],
                    [12, 1.20, 0.80, "md", 0.0, 2.05]
                ],
                "spaces": [
                    {"name": "סלון ומטבח מיני-פנטהאוז (#10)", "center": [-5.6, 1.2]},
                    {"name": "ממ\"ד קומה 5", "center": [1.4, 6.4]},
                    {"name": "חדרי שינה וסוויטת הורים (#10)", "center": [-3.0, 9.5]}
                ]
            },
            "tpl_penthouse": {
                "slab": [[-8.14, -2.65], [6.95, -2.65], [6.95, 3.80], [4.00, 3.80], [4.00, 9.20], [-3.20, 9.20], [-3.20, 12.01], [-8.14, 12.01]],
                "balconies": [
                    {"id": "terrace_ph_north", "polygon": [[-8.14, -4.25], [2.50, -4.25], [2.50, -2.65], [-8.14, -2.65]], "railing_type": "glass", "railing_h": 1.05},
                    {"id": "terrace_ph_south", "polygon": [[-3.20, 9.20], [4.00, 9.20], [4.00, 14.50], [-8.14, 14.50], [-8.14, 12.01], [-3.20, 12.01]], "railing_type": "glass", "railing_h": 1.05}
                ],
                "pergolas": [
                    {"id": "perg_ph_s", "polygon": [[-3.00, 9.40], [3.60, 9.40], [3.60, 14.20], [-3.00, 14.20]], "type": "light_aluminum", "z_offset": 2.60}
                ],
                "w": [
                    [-8.14, -2.65,  6.95, -2.65, 0.25, "ext", "stone"],
                    [ 6.95, -2.65,  6.95,  3.80, 0.25, "ext", "white_plaster"],
                    [ 6.95,  3.80,  4.00,  3.80, 0.25, "ext", "white_plaster"],
                    [ 4.00,  3.80,  4.00,  9.20, 0.25, "ext", "white_plaster"],
                    [ 4.00,  9.20, -3.20,  9.20, 0.25, "ext", "white_plaster"],
                    [-3.20,  9.20, -3.20, 12.01, 0.25, "ext", "white_plaster"],
                    [-3.20, 12.01, -8.14, 12.01, 0.25, "ext", "white_plaster"],
                    [-8.14, 12.01, -8.14, -2.65, 0.25, "ext", "white_plaster"],
                    [-1.10, -0.95,  1.10, -0.95, 0.25, "core", "concrete"],
                    [ 1.10, -0.95,  1.10,  5.20, 0.25, "core", "concrete"],
                    [ 1.10,  5.20, -1.10,  5.20, 0.25, "core", "concrete"],
                    [-1.10,  5.20, -1.10, -0.95, 0.25, "core", "concrete"],
                    [-1.10,  5.20,  3.60,  5.20, 0.30, "mamad", "concrete"],
                    [ 3.60,  5.20,  3.60,  8.10, 0.30, "mamad", "concrete"],
                    [ 3.60,  8.10, -1.10,  8.10, 0.30, "mamad", "concrete"]
                ],
                "o": [
                    [0, 1.20, 3.00, "sw", 0.0, 2.20],
                    [0, 5.80, 3.00, "sw", 0.0, 2.20],
                    [4, 2.20, 2.20, "sw", 0.0, 2.20],
                    [13, 0.80, 1.00, "mw", 1.05, 1.05],
                    [14, 1.20, 0.80, "md", 0.0, 2.05]
                ],
                "spaces": [
                    {"name": "סלון ומטבח פנטהאוז (#11)", "center": [-5.6, 1.2]},
                    {"name": "ממ\"ד פנטהאוז", "center": [1.0, 6.4]},
                    {"name": "חדרי שינה וסוויטת הורים (#11)", "center": [-5.8, 9.0]}
                ]
            },
            "tpl_roof": {
                "slab": [[-2.20, -1.20], [2.40, -1.20], [2.40, 5.40], [-2.20, 5.40]],
                "w": [
                    [-2.20, -1.20,  2.40, -1.20, 0.25, "core", "white_plaster"],
                    [ 2.40, -1.20,  2.40,  5.40, 0.25, "core", "white_plaster"],
                    [ 2.40,  5.40, -2.20,  5.40, 0.25, "core", "white_plaster"],
                    [-2.20,  5.40, -2.20, -1.20, 0.25, "core", "white_plaster"]
                ],
                "o": [
                    [2, 1.20, 1.10, "d", 0.0, 2.10],
                    [1, 1.50, 1.20, "w", 1.05, 1.05]
                ],
                "spaces": [
                    {"name": "יציאה לגג וחדר מכונות מעלית", "center": [0.0, 2.0]}
                ]
            }
        },
        "instances": [
            {"bldg_id": "bldg_7", "template": "tpl_basement",  "levels": ["L_B1"],      "transform": [0, 0, 0, False]},
            {"bldg_id": "bldg_7", "template": "tpl_ground",    "levels": ["L_0"],       "transform": [0, 0, 0, False]},
            {"bldg_id": "bldg_7", "template": "tpl_typical",   "levels": ["L_TYP_1_3", "L_4"], "transform": [0, 0, 0, False]},
            {"bldg_id": "bldg_7", "template": "tpl_floor5",    "levels": ["L_5"],       "transform": [0, 0, 0, False]},
            {"bldg_id": "bldg_7", "template": "tpl_penthouse", "levels": ["L_6"],       "transform": [0, 0, 0, False]},
            {"bldg_id": "bldg_7", "template": "tpl_roof",      "levels": ["L_ROOF"],    "transform": [0, 0, 0, False]}
        ]
    }
    return bim

if __name__ == "__main__":
    plans_data = process_all_plans()
    plans_path = os.path.join(SCRATCH_DIR, "yatkovski7_extracted_plans.json")
    with open(plans_path, "w", encoding="utf-8") as f:
        json.dump(plans_data, f, ensure_ascii=False)
    print(f"Saved {plans_path} ({os.path.getsize(plans_path):,} bytes)")

    crm_data = build_crm_data()
    crm_path = os.path.join(SCRATCH_DIR, "yatkovski7_units_crm.json")
    with open(crm_path, "w", encoding="utf-8") as f:
        json.dump(crm_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {crm_path} ({len(crm_data['units'])} units, {len(crm_data['parking_stalls'])} parking stalls)")

    os.makedirs(os.path.join(PROJECT_DIR, "data"), exist_ok=True)
    with open(os.path.join(PROJECT_DIR, "data", "yatkovski7_extracted_plans.json"), "w", encoding="utf-8") as f:
        json.dump(plans_data, f, ensure_ascii=False)
    with open(os.path.join(PROJECT_DIR, "data", "yatkovski7_units_crm.json"), "w", encoding="utf-8") as f:
        json.dump(crm_data, f, ensure_ascii=False, indent=2)

    bim_data = build_compact_bim()
    bim_path = os.path.join(PROJECT_DIR, "compact_bim.json")
    with open(bim_path, "w", encoding="utf-8") as f:
        json.dump(bim_data, f, ensure_ascii=False, indent=2)
    with open(os.path.join(PROJECT_DIR, "data", "compact_bim.json"), "w", encoding="utf-8") as f:
        json.dump(bim_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {bim_path}")
