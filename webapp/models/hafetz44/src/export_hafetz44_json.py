import fitz
import os, math, json
from shapely.geometry import LineString, MultiLineString, Polygon, Point, box
from shapely.ops import polygonize, unary_union, triangulate
from shapely import snap

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_DIR, "data")
SCRATCH_DIR = r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44"
PDF_PATH = os.path.join(PROJECT_DIR, "חפץ 44- ג9 -חלק 1 (1).pdf")
if not os.path.exists(PDF_PATH):
    PDF_PATH = os.path.join(SCRATCH_DIR, "pdfs", "hafetz44_g9_part1.pdf")
PT_PER_M = 72.0 / 25.4 * 10.0  # 1:100 scale -> 28.3464567 pt/m

# Centered Lot-Box Anchors (ax, ay) & PDF Crop Regions (rx0, rx1, ry0, ry1) on Page 1
PLANS_CFG = {
    'basement':  (105.004, 43.287,  84.5, 125.5, 33.5, 53.5),
    'ground':    (160.203, 24.381, 139.5, 180.5, 14.2, 34.5),
    'typical':   (105.000, 17.768,  84.5, 125.5,  7.8, 27.8),
    'penthouse': ( 60.583, 17.768,  40.2,  81.2,  7.8, 27.8),
    'roof_main': ( 60.583, 43.287,  40.2,  81.2, 33.5, 53.5),
}

def get_enclosed_slab_poly(name):
    """
    Returns the exact 2D enclosed building polygon in centered (x, y) meters:
      +x = East (toward Hafetz Haim St), -x = West
      +y = South, -y = North
    """
    if name in ('typical', 'ground'):
        # Main wing: X=[-13.361..14.359] (27.72m), Y=[-5.184..4.216] (9.40m)
        # Central South core: X=[-3.361..5.669] (9.03m), Y=[4.216..5.196] (+0.98m)
        # Central North Mamad recess: X=[-1.050..5.461] (6.51m), Y=[-5.184..-4.633] (-0.55m)
        main_wing = box(-13.361, -5.184, 14.359, 4.216).difference(box(-1.050, -5.184, 5.461, -4.633))
        south_core = box(-3.361, 4.200, 5.669, 5.196)
        return unary_union([main_wing, south_core])
    elif name == 'penthouse':
        # Penthouse enclosed footprint: X=[-10.211..9.599], Y=[-5.184..4.216] + South core [-3.361..5.669, 4.216..5.196]
        main_ph = box(-10.211, -5.184, 9.599, 4.216).difference(box(-1.050, -5.184, 5.300, -4.633))
        south_core = box(-3.361, 4.200, 5.669, 5.196)
        return unary_union([main_ph, south_core])
    elif name == 'basement':
        # Full basement perimeter with SE infiltration pit cutout (426x545cm at X=14.25..18.51, Y=3.60..9.05)
        return box(-17.721, -9.202, 18.508, 9.048).difference(box(14.250, 3.600, 18.510, 9.050))
    else:
        return box(-1.422, 1.687, 2.358, 5.200)

def classify_exterior_opening(name, orient, mx, my, span):
    if name == 'ground':
        return 'vitrine' if span >= 1.40 else 'window'

    if orient == 'V':
        if name == 'penthouse':
            if mx < -8.0 and span >= 1.45:
                return 'vitrine'
            if mx > 8.0 and span >= 2.20:
                return 'vitrine'
            return 'window'
        else:
            if span >= 2.20:
                return 'vitrine'
            if span >= 1.15:
                return 'win_tall'
            return 'window'

    if my < -3.5:
        if -2.8 <= mx <= 3.8:
            if name == 'penthouse' and mx > 0.5:
                return 'win_tall'
            return 'mamad_win'
        return 'window'
    else:
        if name == 'typical':
            if mx < -6.8 or mx > 8.5:
                return 'win_tall'
        return 'window'

LAUNDRY_OUTER_NICHES = [
    (-5.184, -5.30, -3.20),
    (-5.184,  3.75,  6.25),
]

def is_outer_laundry_louver(orient, mx, my, gap):
    if orient != 'H':
        return False
    for ly, lx0, lx1 in LAUNDRY_OUTER_NICHES:
        if abs(my - ly) < 0.28 and (lx0 <= mx <= lx1):
            return True
    return False

def triangulate_poly(p):
    """
    Slices a wall polygon horizontally at all vertex Y-coordinates into convex/rectangular strips
    and triangulates each strip piece strictly inside p. Guarantees 0 diagonal room-crossing triangles!
    """
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

# Architect-verified room labels & written dimensions (in cm) from hafetz44_g9_part1.pdf (Garmushka)
EXACT_ROOM_LABELS = {
    'basement': [
        {'x':   0.5, 'y':  0.2, 'name': 'לובי מעלית ומבואה מוגנת', 'dims': '370×340'},
        {'x':   0.2, 'y':  3.0, 'name': 'חדר מדרגות מוגן ומעלית', 'dims': '338×311'},
        {'x':  -2.8, 'y':  2.8, 'name': 'חדר משאבות ומאגר מים', 'dims': '324×390'},
        {'x':  -1.5, 'y': -2.2, 'name': 'חדר סינון / מחסן מערבי', 'dims': '295×360'},
        {'x':   4.1, 'y': -2.4, 'name': 'חדר סינון / מחסן מזרחי', 'dims': '365×385'},
        {'x':   3.8, 'y':  6.8, 'name': 'רמפת ירידה דרומית (15%)', 'dims': '300×1580'},
        {'x':   0.6, 'y': -7.0, 'name': 'רמפה צפונית (11%)', 'dims': '275×1360'},
        {'x':  10.2, 'y': -1.0, 'name': 'מיסעה מזרחית (5%)', 'dims': '555×800'},
        {'x':  -9.3, 'y':  1.5, 'name': 'מיסעה מערבית (2.5%)', 'dims': '575×1450'},
        {'x':  16.3, 'y':  6.3, 'name': 'בור חלחול K (מחוץ למרתף)', 'dims': '426×545'},
    ],
    'ground': [
        {'x':   8.2, 'y':  1.8, 'name': 'לובי ראשי', 'dims': '974×413'},
        {'x':  11.1, 'y': -3.8, 'name': 'אורור חניון', 'dims': '530×228'},
        {'x':   7.0, 'y': -2.6, 'name': 'חדר דיירים', 'dims': '260×408'},
        {'x':   4.0, 'y': -2.6, 'name': 'חדר עגלות', 'dims': '305×400'},
        {'x':   0.6, 'y': -2.4, 'name': 'אשפה (+47.22)', 'dims': '330×355'},
        {'x':  -3.5, 'y': -4.0, 'name': 'אורור חניון', 'dims': '150×441'},
        {'x':   0.2, 'y':  3.3, 'name': 'חדר מדרגות', 'dims': '338×311'},
        {'x':   1.6, 'y':  2.8, 'name': 'מעלית', 'dims': '170×185'},
        {'x':  -2.6, 'y':  3.3, 'name': 'מחסן', 'dims': '120×338'},
        {'x':  -4.3, 'y':  2.8, 'name': 'גז (+46.45)', 'dims': '240×240'},
    ],
    'typical': [
        # West Apartment (5 Rooms — דירות מערביות 2,4,6,8,10,12,14,16)
        {'x': -14.3, 'y':  1.5, 'name': 'מרפסת שמש', 'dims': '200×900 (כ-18.5 מ"ר)'},
        {'x': -11.3, 'y':  2.3, 'name': 'ח. מגורים', 'dims': '418×635'},
        {'x':  -8.0, 'y':  2.3, 'name': 'פ. אוכל', 'dims': '418×340'},
        {'x':  -5.0, 'y':  2.6, 'name': 'מטבח', 'dims': '340×418'},
        {'x': -11.0, 'y': -1.8, 'name': 'חדר הורים', 'dims': '468×299'},
        {'x': -12.3, 'y': -4.2, 'name': 'ח. רחצה', 'dims': '160×160'},
        {'x': -10.5, 'y': -4.2, 'name': 'ח. ארונות', 'dims': '165×160'},
        {'x':  -8.1, 'y': -3.2, 'name': 'חדר', 'dims': '299×348'},
        {'x':  -5.0, 'y': -3.2, 'name': 'חדר', 'dims': '285×348'},
        {'x':  -2.3, 'y': -2.3, 'name': 'ח. רחצה', 'dims': '240×170'},
        {'x':  -2.3, 'y': -3.7, 'name': 'ח. שירות', 'dims': '240×95'},
        {'x':  -2.3, 'y': -4.6, 'name': 'מסתור כביסה / דוד ומזגן', 'dims': '240×75'},
        {'x':   0.6, 'y': -2.3, 'name': 'ממ"ד', 'dims': '335×400'},
        # Core (גרעין קומתי נעול)
        {'x':   0.8, 'y':  0.2, 'name': 'לובי קומתי', 'dims': '651×142'},
        {'x':   0.2, 'y':  3.2, 'name': 'חדר מדרגות', 'dims': '338×311'},
        {'x':   1.6, 'y':  2.8, 'name': 'מעלית', 'dims': '170×185'},
        {'x':  -2.6, 'y':  2.8, 'name': 'מחסן', 'dims': '120×351'},
        {'x':   3.1, 'y':  2.8, 'name': 'מחסן', 'dims': '120×351'},
        # East Apartment (4 Rooms — דירות מזרחיות 1,3,5,7,9,11,13,15)
        {'x':   3.9, 'y': -2.3, 'name': 'ממ"ד', 'dims': '295×400'},
        {'x':   6.8, 'y': -2.3, 'name': 'ח. רחצה', 'dims': '238×170'},
        {'x':   6.8, 'y': -3.7, 'name': 'ח. שירות', 'dims': '238×93'},
        {'x':   6.8, 'y': -4.6, 'name': 'מסתור כביסה / דוד ומזגן', 'dims': '238×75'},
        {'x':   9.5, 'y': -3.2, 'name': 'חדר', 'dims': '279×348'},
        {'x':  11.7, 'y': -4.2, 'name': 'ח. ארונות', 'dims': '149×158'},
        {'x':  13.3, 'y': -4.2, 'name': 'ח. רחצה', 'dims': '160×158'},
        {'x':  12.1, 'y': -1.8, 'name': 'חדר הורים', 'dims': '422×300'},
        {'x':   7.0, 'y':  2.6, 'name': 'מטבח', 'dims': '300×418'},
        {'x':   9.4, 'y':  2.3, 'name': 'פ. אוכל', 'dims': '418×245'},
        {'x':  12.1, 'y':  2.3, 'name': 'ח. מגורים', 'dims': '545×418'},
        {'x':  15.3, 'y':  1.5, 'name': 'מרפסת שמש', 'dims': '200×940 (כ-18.5 מ"ר)'},
    ],
    'penthouse': [
        # Full-Floor Luxury Penthouse (קומה ט' — דירה 17, פנטהאוז מפלס מלא)
        {'x':  11.9, 'y': -0.5, 'name': 'מרפסת גג מזרחית + פרגולה', 'dims': '456×940 (כ-73 מ"ר)'},
        {'x': -11.8, 'y': -0.5, 'name': 'מרפסת גג מערבית + פרגולה', 'dims': '295×940'},
        {'x':   6.6, 'y': -2.5, 'name': 'ח. מגורים', 'dims': '560×841'},
        {'x':   8.0, 'y':  0.1, 'name': 'פ. אוכל', 'dims': '320×260'},
        {'x':   6.8, 'y':  2.8, 'name': 'מטבח', 'dims': '510×420'},
        {'x':   3.1, 'y': -2.5, 'name': 'שירותי אורחים', 'dims': '115×183'},
        {'x':   0.6, 'y': -2.9, 'name': 'ממ"ד', 'dims': '335×271'},
        {'x':  -2.4, 'y': -2.3, 'name': 'ח. רחצה', 'dims': '240×171'},
        {'x':  -2.4, 'y': -3.7, 'name': 'ח. שירות', 'dims': '240×90'},
        {'x':  -2.4, 'y': -4.6, 'name': 'מסתור כביסה / דוד ומזגן', 'dims': '240×75'},
        {'x':  -5.3, 'y': -3.2, 'name': 'חדר', 'dims': '306×344'},
        {'x':  -8.5, 'y': -3.2, 'name': 'חדר', 'dims': '306×344'},
        {'x':  -8.6, 'y':  2.1, 'name': 'חדר', 'dims': '280×423'},
        {'x':  -5.4, 'y':  2.1, 'name': 'חדר הורים', 'dims': '335×423'},
        {'x':  -2.8, 'y':  0.8, 'name': 'ח. ארונות', 'dims': '160×210'},
        {'x':  -2.8, 'y':  3.0, 'name': 'ח. רחצה הורים', 'dims': '160×204'},
        {'x':   0.8, 'y':  0.2, 'name': 'לובי קומתי', 'dims': '320×142'},
        {'x':   0.2, 'y':  3.2, 'name': 'חדר מדרגות', 'dims': '338×311'},
        {'x':   1.6, 'y':  2.8, 'name': 'מעלית', 'dims': '170×185'},
    ],
    'roof_main': [
        {'x':   0.4, 'y':  3.4, 'name': 'מגדל יציאה לגג וחדר מדרגות', 'dims': '378×351'},
        {'x':  -6.5, 'y': -1.0, 'name': 'מסתור דודי שמש ומעבים (מערב)', 'dims': '864×338'},
        {'x':   6.0, 'y': -1.0, 'name': 'מסתור דודי שמש ומעבים (מזרח)', 'dims': '705×338'},
        {'x':  11.9, 'y': -0.5, 'name': 'מצללה היקפית מזרחית (פרגולה)', 'dims': '249×940'},
        {'x': -11.8, 'y': -0.5, 'name': 'מצללה היקפית מערבית (פרגולה)', 'dims': '200×940'},
    ]
}

def process_all_plans():
    doc = fitz.open(PDF_PATH)
    page = doc[0]
    rot1 = page.rotation_matrix
    drawings = page.get_drawings()

    out_plans = {}

    for name, (ax, ay, rx0, rx1, ry0, ry1) in PLANS_CFG.items():
        def pt(p):
            pr = p * rot1
            return (round(pr.x / PT_PER_M - ax, 4), round(pr.y / PT_PER_M - ay, 4))

        clip = box(-20.8, -10.5, 20.8, 12.0)
        w108_lines = []
        thin_cad_lines = []
        furn_segs = []
        cad_segs = []
        door_arc_geoms = []
        blue_fill_polys = []

        for d in drawings:
            r = d['rect'] * rot1
            x0, y0, x1, y1 = r.x0 / PT_PER_M, r.y0 / PT_PER_M, r.x1 / PT_PER_M, r.y1 / PT_PER_M
            if x1 < rx0 or x0 > rx1 or y1 < ry0 or y0 > ry1:
                continue
            if (x1 - x0) > 37.0 or (y1 - y0) > 19.5:
                continue

            c = tuple(round(x, 2) for x in d['color']) if d.get('color') else None
            fill = tuple(round(x, 2) for x in d['fill']) if d.get('fill') else None
            w = round(d['width'], 2) if d.get('width') is not None else None
            dashes = d.get("dashes")
            is_dashed = bool(dashes and dashes != "[] 0")

            # Extract CAD blue-filled reinforced concrete walls (perimeter retaining walls, Mamad, core)
            if fill == (0.0, 0.32, 1.0):
                ring = []
                for it in d['items']:
                    if it[0] == 'l':
                        if not ring:
                            ring.append(pt(it[1]))
                        ring.append(pt(it[2]))
                    elif it[0] == 'qu':
                        q = it[1]
                        p = Polygon([pt(q.ul), pt(q.ur), pt(q.lr), pt(q.ll)]).buffer(0)
                        if not p.is_empty and p.area > 0.001 and clip.intersects(p):
                            blue_fill_polys.append(p)
                    elif it[0] == 're':
                        rc = it[1]
                        p = Polygon([pt(fitz.Point(rc.x0, rc.y0)), pt(fitz.Point(rc.x1, rc.y0)), pt(fitz.Point(rc.x1, rc.y1)), pt(fitz.Point(rc.x0, rc.y1))]).buffer(0)
                        if not p.is_empty and p.area > 0.001 and clip.intersects(p):
                            blue_fill_polys.append(p)
                if len(ring) >= 3:
                    p = Polygon(ring).buffer(0)
                    if not p.is_empty and p.area > 0.001 and clip.intersects(p):
                        blue_fill_polys.append(p)

            if is_dashed or w is None or c is None:
                continue

            segs = []
            for it in d['items']:
                if it[0] == 'l':
                    segs.append((pt(it[1]), pt(it[2])))
                elif it[0] == 'qu':
                    q = it[1]
                    pts = [pt(q.ul), pt(q.ur), pt(q.lr), pt(q.ll), pt(q.ul)]
                    for i in range(4): segs.append((pts[i], pts[i+1]))
                elif it[0] == 're':
                    rc = it[1]
                    pts = [pt(fitz.Point(rc.x0, rc.y0)), pt(fitz.Point(rc.x1, rc.y0)), pt(fitz.Point(rc.x1, rc.y1)), pt(fitz.Point(rc.x0, rc.y1))]
                    pts.append(pts[0])
                    for i in range(4): segs.append((pts[i], pts[i+1]))
                elif it[0] == 'c' and c == (0.0, 0.0, 0.0) and w <= 0.85:
                    p1, p2, p3, p4 = pt(it[1]), pt(it[2]), pt(it[3]), pt(it[4])
                    chord = math.hypot(p4[0] - p1[0], p4[1] - p1[1])
                    bpts = []
                    for t in (0.0, 0.25, 0.5, 0.75, 1.0):
                        mt = 1.0 - t
                        bx = (mt**3)*p1[0] + 3*(mt**2)*t*p2[0] + 3*mt*(t**2)*p3[0] + (t**3)*p4[0]
                        by = (mt**3)*p1[1] + 3*(mt**2)*t*p2[1] + 3*mt*(t**2)*p3[1] + (t**3)*p4[1]
                        bpts.append((round(bx, 3), round(by, 3)))
                    for i in range(4): segs.append((bpts[i], bpts[i+1]))
                    if 0.50 <= chord <= 1.35 and clip.contains(Point(p1)) and clip.contains(Point(p4)):
                        arc_ls = LineString(bpts)
                        if not any(arc_ls.distance(existing) < 0.25 for existing in door_arc_geoms):
                            door_arc_geoms.append(arc_ls)

            # Skip exploded text glyphs (many tiny segments < 0.20m)
            if len(segs) >= 8 and max((math.hypot(p2[0]-p1[0], p2[1]-p1[1]) for p1, p2 in segs), default=0) < 0.22:
                continue

            for p1, p2 in segs:
                L = math.hypot(p2[0]-p1[0], p2[1]-p1[1])
                if L < 0.015:
                    continue
                s = LineString([p1, p2])
                if not clip.intersects(s):
                    continue
                if c == (0.0, 0.0, 0.0) and w in (1.08, 0.96, 1.44):
                    w108_lines.append(s)
                elif c == (0.0, 0.0, 0.0) and 0.12 <= w <= 0.85:
                    if L >= 0.06:
                        thin_cad_lines.append(s)
                    if w in (0.72, 0.60, 0.48, 0.36) and 0.08 <= L <= 3.6:
                        mx, my = 0.5*(p1[0]+p2[0]), 0.5*(p1[1]+p2[1])
                        if -18.5 <= mx <= 18.5 and -9.5 <= my <= 9.5:
                            cad_segs.append([round(p1[0], 3), round(p1[1], 3), round(p2[0], 3), round(p2[1], 3)])
                elif c == (0.93, 0.43, 0.0) and 0.06 <= L <= 3.2:
                    mx, my = 0.5*(p1[0]+p2[0]), 0.5*(p1[1]+p2[1])
                    if -15.5 <= mx <= 16.5 and -5.3 <= my <= 5.3:
                        furn_segs.append([round(p1[0], 3), round(p1[1], 3), round(p2[0], 3), round(p2[1], 3)])

        mls = MultiLineString(w108_lines)
        noded = unary_union(snap(mls, mls, 0.02))
        h_segs, v_segs = [], []
        for l in w108_lines:
            (x1, y1), (x2, y2) = l.coords[0], l.coords[-1]
            if abs(y1 - y2) < 0.012 and abs(x2 - x1) >= 0.04:
                h_segs.append((0.5*(y1+y2), min(x1,x2), max(x1,x2)))
            elif abs(x1 - x2) < 0.012 and abs(y2 - y1) >= 0.04:
                v_segs.append((0.5*(x1+x2), min(y1,y2), max(y1,y2)))

        max_wall_thk = 0.55 if name == 'basement' else 0.32
        pair_boxes = []
        h_wall_bands = []
        v_wall_bands = []
        for i in range(len(h_segs)):
            yA, xA0, xA1 = h_segs[i]
            for j in range(i+1, len(h_segs)):
                yB, xB0, xB1 = h_segs[j]
                if 0.075 <= abs(yA - yB) <= max_wall_thk:
                    ox0, ox1 = max(xA0, xB0), min(xA1, xB1)
                    if ox1 - ox0 >= 0.05:
                        ym0, ym1 = min(yA, yB), max(yA, yB)
                        if not any(ym0 + 0.03 < h_segs[k][0] < ym1 - 0.03 and min(ox1, h_segs[k][2]) - max(ox0, h_segs[k][1]) > 0.05 for k in range(len(h_segs))):
                            pair_boxes.append(box(ox0, ym0, ox1, ym1))
                            h_wall_bands.append((round(ym0, 3), round(ym1, 3), ox0, ox1))
        for i in range(len(v_segs)):
            xA, yA0, yA1 = v_segs[i]
            for j in range(i+1, len(v_segs)):
                xB, yB0, yB1 = v_segs[j]
                if 0.075 <= abs(xA - xB) <= max_wall_thk:
                    oy0, oy1 = max(yA0, yB0), min(yA1, yB1)
                    if oy1 - oy0 >= 0.05:
                        xm0, xm1 = min(xA, xB), max(xA, xB)
                        if not any(xm0 + 0.03 < v_segs[k][0] < xm1 - 0.03 and min(oy1, v_segs[k][2]) - max(oy0, v_segs[k][1]) > 0.05 for k in range(len(v_segs))):
                            pair_boxes.append(box(xm0, oy0, xm1, oy1))
                            v_wall_bands.append((round(xm0, 3), round(xm1, 3), oy0, oy1))

        # For Basement & Ground, include exact CAD structural wall segments where vector lines had open gaps:
        extra_structural_walls = []
        if name == 'basement':
            extra_structural_walls = [
                box(-6.25, -8.71,  7.45, -8.41),  # North ramp inner 30cm wall (separating 275cm ramp from central core)
                box( 7.16, -2.16,  7.46,  2.25),  # East ramp inner 30cm wall (separating 555cm East aisle from core)
                box(-1.47,  5.20,  4.21,  5.50),  # South ramp inner 30cm wall (separating 300cm South ramp from core)
            ]
        elif name == 'ground':
            extra_structural_walls = [
                # 1. North-West Parking Ventilation Shaft perimeter walls (אוורור חניון 150x441 at X=-5.86..-1.25, Y=-4.92..-3.02)
                box(-5.86, -4.92, -3.26, -4.72),  # North wall West of louver
                box(-2.06, -4.92, -1.05, -4.72),  # North wall East of louver
                box(-5.86, -4.92, -5.66, -3.02),  # West wall of vent shaft
                box(-5.86, -3.22, -1.25, -3.02),  # South wall separating vent shaft from Parking Stall #1
                # 2. Trash Room (חדר אשפה 330x355) West wall & NW smoke shaft (50x70) & South-East partition
                box(-1.25, -4.72, -1.05, -0.13),  # Continuous West concrete wall of Trash Room
                box(-1.25, -4.63, -0.02, -4.33),  # Trash room North wall West of double door
                box( 0.25, -0.33,  1.25, -0.13),  # Trash room South wall East of water meter niche
                # 3. Solid South concrete wall of Storage Room & Smoke Shaft (מחסן 120x338 ופיר עשן) on Ground Floor
                box(-3.362, 4.997, -1.220, 5.196),
            ]

        max_poly_area = 65.0 if name == 'basement' else 25.0
        # Filter polygonize(noded) with morphological thickness erosion (buffer(-0.26).is_empty) on non-basement sheets
        # so framed text callout boxes (like 'ניקוז S' W04 in Ground Lobby and 'ניקוז K' W00) are never extruded as solid blocks!
        polys = [
            p for p in polygonize(noded)
            if 0.008 <= p.area < max_poly_area and (name == 'basement' or p.buffer(-0.26).is_empty)
        ]
        u_walls = unary_union(polys + pair_boxes + blue_fill_polys + extra_structural_walls).buffer(0.003, join_style=2).buffer(-0.003, join_style=2).simplify(0.002, preserve_topology=True)
        if name == 'ground':
            # Clip out stray text/symbol artifacts outside the Ground Floor building & remove the diagonal CAD leader spike at (-2.06, -5.20)
            u_walls = u_walls.intersection(box(-13.50, -5.19, 14.40, 5.22)).difference(box(-2.06, -5.20, -1.30, -4.73))
        final_walls = list(u_walls.geoms) if hasattr(u_walls, 'geoms') else ([u_walls] if not u_walls.is_empty else [])

        # Keep outer balcony area clean for custom 3D architectural frame columns & railings in viewer
        if name in ('typical', 'penthouse'):
            final_walls = [p for p in final_walls if (p.bounds[2] > -13.40 and p.bounds[0] < 14.40)]

        # Exact architect-verified exterior & primary openings per floor from hafetz44_g9_part1.pdf & part2.pdf
        EXACT_EXT_OPENINGS = {
            'basement': [
                # Core & Mamad Filter / Storage / Pump room doors in Basement (-5.10m)
                ('H',  1.150,  1.687,  2.050,  1.885, 'door'), # Elevator Landing Door
                ('H', -1.200,  1.687, -0.200,  1.885, 'door'), # Stairwell Fire Door
                ('V', -1.420, -0.350, -1.220,  0.550, 'door'), # Basement Protected Lobby West Fire Door
                ('V',  2.300, -0.350,  2.510,  0.550, 'door'), # Basement Protected Lobby East Fire Door
                ('H', -1.000, -3.260, -0.100, -3.060, 'door'), # West Filter/Storage Blast Door
                ('H',  1.300, -3.260,  2.200, -3.060, 'door'), # East Filter/Storage Blast Door
                ('H', -2.800,  1.687, -1.900,  1.885, 'door'), # Pump & Water Tank Room Door
            ],
            'ground': [
                # 1. East Facade (Main Entrance Lobby Glazed Curtain Wall & Entrance Door at X = 13.810..13.970, Y = -2.382..+3.321)
                ('V', 13.810, -2.382, 13.970, -0.350, 'vitrine'),
                ('V', 13.810, -0.350, 13.970,  1.150, 'door'),     # Main Lobby Double Glass Entrance Door
                ('V', 13.810,  1.150, 13.970,  3.321, 'vitrine'),
                # 2. South Facade (Main Lobby 3 Tall Windows at Y = 3.998..4.218; SW Storage South wall is solid concrete on Ground Floor)
                ('H',  6.510,  3.998,  7.708,  4.218, 'win_tall'),
                ('H',  9.058,  3.998, 10.256,  4.218, 'win_tall'),
                ('H', 11.755,  3.998, 12.957,  4.218, 'win_tall'),
                # 3. North Facade (NW Vent Louver, Trash Room Double Door, Stroller Window, Residents Club Window, East Vent Louvers)
                ('H', -3.256, -4.920, -2.058, -4.720, 'window'),   # NW Parking Ventilation Louver
                ('H', -0.023, -4.634,  1.189, -4.333, 'door'),     # Trash Room (חדר אשפה 330x355) North Double Door
                ('H',  3.461, -4.634,  4.470, -4.333, 'window'),   # Stroller & Bicycle Room (חדר עגלות 305x400) North Window
                ('H',  5.943, -4.634,  7.636, -4.414, 'window'),   # Residents Club (חדר דיירים 260x408) North Window
                ('H',  9.053, -5.184, 10.261, -4.964, 'window'),   # East Parking Ventilation Louver 1
                ('H', 11.750, -5.184, 12.962, -4.964, 'window'),   # East Parking Ventilation Louver 2
                # 4. Internal & Service Doors on Ground Floor (Trash Room, Stroller, Club, Elevator, Stairwell, Storage, Gas Room)
                ('H',  1.250, -0.333,  2.247, -0.130, 'door'),     # Trash Room Internal Vestibule Door
                ('H',  3.461, -0.333,  4.470, -0.130, 'door'),     # Stroller Room Door to Lobby
                ('H',  6.619, -0.333,  7.582, -0.130, 'door'),     # Residents Club Door to Lobby
                ('H',  1.145,  1.687,  2.055,  1.885, 'door'),     # Elevator Landing Door
                ('H', -1.213,  1.687, -0.055,  1.885, 'door'),     # Central Stairwell Exit Door to Lobby
                ('H', -3.100,  1.415, -2.300,  1.615, 'door'),     # Storage Room (מחסן 120x338) Door
                ('V', -5.263,  2.326, -5.064,  3.325, 'door'),     # Gas Room (חדר גז 240x245) West Louvered Door
            ],
            'typical': [
                # 1. WEST FACADE (X = -13.361 .. -13.111, total Y = 940cm: 110 + 60 + 105 + 130 + 145 + 300 + 90)
                ('V', -13.361, -4.084, -13.111, -3.484, 'window'),    # Master Bath 60/125 uk=1.05
                ('V', -13.361, -2.432, -13.111, -1.132, 'win_tall'),  # Master Bedroom 130/125 uk=0.40
                ('V', -13.361,  0.320, -13.107,  3.321, 'vitrine'),   # West Living Room Balcony Vitrine 300/220
                # 2. EAST FACADE — HAFETZ HAIM ST (X = +14.105 .. +14.359, total Y = 940cm: 110 + 60 + 105 + 130 + 145 + 300 + 90)
                ('V',  14.109, -4.084,  14.359, -3.484, 'window'),    # East Master Bath 60/125 uk=1.05
                ('V',  14.109, -2.432,  14.359, -1.132, 'win_tall'),  # East Master Bedroom 130/125 uk=0.40
                ('V',  14.105,  0.320,  14.359,  3.321, 'vitrine'),   # East Living Room Balcony Vitrine 300/220
                # 3. NORTH FACADE (Y = -5.184..-4.959 on wings, -4.430..-4.231 behind louvers, -4.633..-4.333 on Mamad core)
                ('H', -12.201, -5.184, -11.600, -4.959, 'window'),    # West Bath North 60/125 uk=1.05
                ('H',  -8.742, -5.184,  -7.544, -4.959, 'window'),    # West Bedroom 1 120/125 uk=1.05
                ('H',  -5.792, -5.184,  -4.594, -4.959, 'window'),    # West Bedroom 2 120/125 uk=1.05
                ('H',  -3.167, -4.430,  -1.470, -4.231, 'window'),    # West General Bath/Laundry 170/125 uk=1.05
                ('H',   0.084, -4.633,   1.084, -4.333, 'mamad_win'), # West Mamad Blast Window 100/100 uk=1.05
                ('H',   3.458, -4.633,   4.461, -4.333, 'mamad_win'), # East Mamad Blast Window 100/100 uk=1.05
                ('H',   5.939, -4.430,   7.636, -4.231, 'window'),    # East General Bath/Laundry 170/125 uk=1.05
                ('H',   8.767, -5.184,  10.066, -4.959, 'window'),    # East Bedroom 130/125 uk=1.05
                ('H',  12.636, -5.184,  13.237, -4.959, 'window'),    # East Bath North 60/125 uk=1.05
                # 4. SOUTH FACADE (Y = +3.998..+4.218 on wings, +4.997..+5.196 on Central Core)
                ('H', -11.761,  3.998, -10.559,  4.218, 'win_tall'),  # West Living 1 120/125 uk=0.40
                ('H',  -8.611,  3.998,  -7.409,  4.218, 'win_tall'),  # West Dining 2 120/125 uk=0.40
                ('H',  -5.411,  3.998,  -4.213,  4.218, 'window'),    # West Kitchen 3 120/125 uk=1.05
                ('H',  -3.163,  4.997,  -1.969,  5.196, 'window'),    # Core West Window Strip 120/125
                ('H',   4.262,  4.997,   5.460,  5.196, 'window'),    # Core East Window Strip 120/125
                ('H',   6.510,  3.998,   7.708,  4.218, 'window'),    # East Kitchen 4 120/125 uk=1.05
                ('H',   9.059,  3.998,  10.257,  4.218, 'win_tall'),  # East Dining 5 120/125 uk=0.40
                ('H',  11.709,  3.998,  12.907,  4.218, 'win_tall'),  # East Living 6 120/125 uk=0.40
                # 5. APARTMENT ENTRANCE & ELEVATOR DOORS FROM LOBBY
                ('V',  -1.420,  0.050,  -1.220,  0.950, 'door'),      # West 5-Room Apartment Entrance Door
                ('V',   2.300,  0.050,   2.510,  0.950, 'door'),      # East 4-Room Apartment Entrance Door
                ('H',   1.150,  1.687,   2.050,  1.885, 'door'),      # Elevator Landing Door
            ],
            'penthouse': [
                # 1. WEST TERRACE FACADE (X = -10.211 .. -9.961, total Y = 940cm: 191 + 170 + 150 + 170 + 259)
                ('V', -10.211, -3.275,  -9.961, -1.577, 'vitrine'),   # West Terrace North Vitrine 170/220
                ('V', -10.211, -0.078,  -9.961,  1.619, 'vitrine'),   # West Terrace South Vitrine 170/220
                # 2. EAST TERRACE FACADE — HAFETZ HAIM ST (X = +9.352 .. +9.601, total Y = 940cm: 110 + 300 + 160 + 358 + 32)
                ('V',   9.352, -4.282,   9.601, -1.281, 'vitrine'),   # Penthouse East Terrace North Sliding Vitrine 300/220
                ('V',   9.352,  0.320,   9.601,  3.896, 'vitrine'),   # Penthouse East Terrace South Giant Vitrine 358/220
                # 3. NORTH FACADE (Y = -4.430..-4.231 behind louvers, -4.633..-4.333 core, -5.184..-4.964 West wing)
                ('H',  -8.746, -5.184,  -7.544, -4.964, 'window'),    # Penthouse West Bedroom 1 North Window 120/125
                ('H',  -5.791, -5.184,  -4.593, -4.964, 'window'),    # Penthouse West Bedroom 2 North Window 120/125
                ('H',  -3.429, -4.430,  -1.443, -4.231, 'window'),    # Penthouse General Bath/Service Window 199/125
                ('H',   0.085, -4.633,   1.084, -4.333, 'mamad_win'), # Penthouse Mamad Blast Window 100/100
                ('H',   2.663, -4.633,   3.467, -4.413, 'window'),    # Penthouse Core Service Window 80/100
                ('H',   4.119, -4.633,   5.300, -4.413, 'win_tall'),  # Penthouse North Living Window 118/125 uk=0.40
                ('H',   8.052, -4.633,   9.352, -4.413, 'window'),    # Penthouse North-East Window 130/125
                # 4. SOUTH FACADE (Y = +3.998..+4.218 on wings, +4.997..+5.196 on Central Core)
                ('H',  -8.610,  3.998,  -7.412,  4.218, 'window'),    # Penthouse Master Closet/Bath South Window 120/125 uk=1.05
                ('H',  -5.414,  3.998,  -4.216,  4.218, 'window'),    # Penthouse Master Suite South Window 120/125 uk=1.05
                ('H',  -3.166,  4.997,  -2.015,  5.196, 'window'),    # Penthouse Core South Window Strip 115/125
                ('H',   6.507,  3.998,   7.709,  4.218, 'window'),    # Penthouse Chef Kitchen South Window 120/125 uk=1.05
                # 5. PENTHOUSE ENTRANCE, STAIRWELL & ELEVATOR DOORS
                ('V',   2.300, -0.500,   2.510,  0.450, 'door'),      # Penthouse Main Entrance Door
                ('H',  -1.200,  1.687,  -0.200,  1.885, 'door'),      # Penthouse Stairwell Fire Door
                ('H',   1.150,  1.687,   2.050,  1.885, 'door'),      # Penthouse Elevator Landing Door
            ],
            'roof_main': [
                ('V',   2.150,  2.200,   2.360,  3.100, 'door'),      # Roof Exit Door from Stairwell Tower (+31.85m)
            ]
        }

        openings = []
        if name in ('basement', 'ground', 'typical', 'penthouse', 'roof_main'):
            # 1. Add all exact architect-verified exterior & primary core openings
            for ext_op in EXACT_EXT_OPENINGS.get(name, []):
                openings.append(ext_op)

            # 2. Detect interior door openings from CAD wall gaps + door swing arcs
            if name in ('typical', 'penthouse'):
                thin_u = unary_union(thin_cad_lines)
                slab_poly = get_enclosed_slab_poly(name)
                slab_boundary = slab_poly.boundary
                candidate_door_gaps = []

                h_clusters = []
                for ym0, ym1, x0, x1 in h_wall_bands:
                    found = False
                    for c in h_clusters:
                        if abs(c[0] - ym0) <= 0.025 and abs(c[1] - ym1) <= 0.025:
                            c[2] = min(c[2], x0)
                            c[3] = max(c[3], x1)
                            found = True
                            break
                    if not found:
                        h_clusters.append([ym0, ym1, x0, x1])

                v_clusters = []
                for xm0, xm1, y0, y1 in v_wall_bands:
                    found = False
                    for c in v_clusters:
                        if abs(c[0] - xm0) <= 0.025 and abs(c[1] - xm1) <= 0.025:
                            c[2] = min(c[2], y0)
                            c[3] = max(c[3], y1)
                            found = True
                            break
                    if not found:
                        v_clusters.append([xm0, xm1, y0, y1])

                for ym0, ym1, xmin, xmax in h_clusters:
                    band = box(-15.0, ym0 + 0.005, 16.0, ym1 - 0.005)
                    solid = band.intersection(u_walls)
                    if solid.is_empty:
                        continue
                    geoms = list(solid.geoms) if hasattr(solid, 'geoms') else [solid]
                    x_intv = []
                    for g in geoms:
                        gx0, gy0, gx1, gy1 = g.bounds
                        if (gy1 - gy0) >= 0.075 and (gx1 - gx0) >= 0.03:
                            x_intv.append((gx0, gx1))
                    x_intv.sort()
                    merged = []
                    for x0, x1 in x_intv:
                        if not merged or x0 > merged[-1][1] + 0.02:
                            merged.append([x0, x1])
                        else:
                            merged[-1][1] = max(merged[-1][1], x1)
                    for i in range(len(merged) - 1):
                        gx0, gx1 = merged[i][1], merged[i+1][0]
                        gap = gx1 - gx0
                        if 0.55 <= gap <= 1.25:
                            gap_box = box(gx0, ym0, gx1, ym1)
                            mx, my = 0.5*(gx0+gx1), 0.5*(ym0+ym1)
                            if not slab_poly.buffer(0.45).contains(Point(mx, my)):
                                continue
                            is_ext = (slab_boundary.distance(Point(mx, my)) <= 0.38) or (abs(my - (-4.25)) <= 0.25 and (-3.6 <= mx <= -1.2 or 5.6 <= mx <= 7.9))
                            if not is_ext and thin_u.intersection(gap_box.buffer(0.05)).length >= 0.30:
                                candidate_door_gaps.append(('H', round(gx0, 3), round(ym0, 3), round(gx1, 3), round(ym1, 3), gap_box, mx, my))

                for xm0, xm1, ymin, ymax in v_clusters:
                    band = box(xm0 + 0.005, -6.0, xm1 - 0.005, 6.0)
                    solid = band.intersection(u_walls)
                    if solid.is_empty:
                        continue
                    geoms = list(solid.geoms) if hasattr(solid, 'geoms') else [solid]
                    y_intv = []
                    for g in geoms:
                        gx0, gy0, gx1, gy1 = g.bounds
                        if (gx1 - gx0) >= 0.075 and (gy1 - gy0) >= 0.03:
                            y_intv.append((gy0, gy1))
                    y_intv.sort()
                    merged = []
                    for y0, y1 in y_intv:
                        if not merged or y0 > merged[-1][1] + 0.02:
                            merged.append([y0, y1])
                        else:
                            merged[-1][1] = max(merged[-1][1], y1)
                    for i in range(len(merged) - 1):
                        gy0, gy1 = merged[i][1], merged[i+1][0]
                        gap = gy1 - gy0
                        if 0.55 <= gap <= 1.25:
                            gap_box = box(xm0, gy0, xm1, gy1)
                            mx, my = 0.5*(xm0+xm1), 0.5*(gy0+gy1)
                            if not slab_poly.buffer(0.45).contains(Point(mx, my)):
                                continue
                            is_ext = (slab_boundary.distance(Point(mx, my)) <= 0.38)
                            if not is_ext and thin_u.intersection(gap_box.buffer(0.05)).length >= 0.30:
                                candidate_door_gaps.append(('V', round(xm0, 3), round(gy0, 3), round(xm1, 3), round(gy1, 3), gap_box, mx, my))

                accepted_door_centers = [(0.5*(o[1]+o[3]), 0.5*(o[2]+o[4])) for o in openings if o[5] == 'door']
                for arc in door_arc_geoms:
                    best_cand = None
                    best_dist = 0.38
                    for cand in candidate_door_gaps:
                        orient, x0, y0, x1, y1, gbox, mx, my = cand
                        d = arc.distance(gbox)
                        if d < best_dist:
                            if not any(math.hypot(mx - cx, my - cy) < 0.65 for cx, cy in accepted_door_centers):
                                best_dist = d
                                best_cand = cand
                    if best_cand is not None:
                        orient, x0, y0, x1, y1, gbox, mx, my = best_cand
                        accepted_door_centers.append((mx, my))
                        openings.append((orient, x0, y0, x1, y1, 'door'))

            # 3. Boolean-subtract every opening (window/vitrine/mamad_win/door) from u_walls
            cut_boxes = []
            for orient, x0, y0, x1, y1, kind in openings:
                pad_perp = 0.14 if kind != 'door' else 0.06
                if orient == 'H':
                    cut_boxes.append(box(x0 - 0.005, y0 - pad_perp, x1 + 0.005, y1 + pad_perp))
                else:
                    cut_boxes.append(box(x0 - pad_perp, y0 - 0.005, x1 + pad_perp, y1 + 0.005))
            if name in ('typical', 'penthouse'):
                cut_boxes.append(box(-3.552, -5.30, -1.250, -4.90))
                cut_boxes.append(box( 5.660, -5.30,  7.840, -4.90))
            if cut_boxes:
                u_walls = u_walls.difference(unary_union(cut_boxes)).buffer(0.001, join_style=2).buffer(-0.001, join_style=2)
                final_walls = list(u_walls.geoms) if hasattr(u_walls, 'geoms') else ([u_walls] if not u_walls.is_empty else [])
                if name in ('typical', 'penthouse'):
                    final_walls = [p for p in final_walls if (p.bounds[2] > -13.40 and p.bounds[0] < 14.40)]

        room_labels = EXACT_ROOM_LABELS.get(name, [])
        wall_polys_json = [triangulate_poly(p) for p in final_walls if p.area >= 0.015]
        door_cnt = len([o for o in openings if o[5] == 'door'])
        ext_cnt = len([o for o in openings if o[5] != 'door'])
        print(f"{name:10s}: walls={len(wall_polys_json):3d}, openings={len(openings):3d} (ext={ext_cnt:2d}, doors={door_cnt:2d}), furn={len(furn_segs):4d}, cad={len(cad_segs):4d}, labels={len(room_labels):2d}")
        out_plans[name] = {
            'wall_polys': wall_polys_json,
            'openings': openings,
            'furn_lines': furn_segs,
            'cad_lines': cad_segs,
            'room_labels': room_labels,
        }

    return out_plans

def build_crm_data():
    """
    Builds the 17-Apartment Catalog & 21-Parking Stall CRM Dataset (19 Vehicle + 2 Motorcycle)
    for Hafetz Haim 44, Petah Tikva (Gush 6396, Helka 85 — Studio Orcha Architects):
      - Floors 1-8 (8 typical floors x 2 units/floor = 16 units):
        - West Apartment (5 rooms, 113.3 sqm net interior / 114.8 sqm incl. Mamad walls + 18.8 sqm West Sun Balcony)
        - East Apartment (4 rooms, 89.4 sqm net interior / 91.8 sqm incl. Mamad walls + 18.8 sqm East Sun Balcony)
      - Floor 9 (Penthouse — 1 full-floor luxury Penthouse):
        - Apt 17: 5-Room Full-Floor Penthouse (148.1 sqm net interior + 73.0 sqm East 456x940 & West 295x940 Roof Terraces with Pergolas)
    """
    # 19 Vehicle Parking Stalls (#1-#6 Ground, #7-#19 Basement) + 2 Motorcycle Bays (#20-#21 Basement) — Exact 1:1 CAD coordinates
    parking_stalls = [
        # Ground Floor Stalls (#1-#6) at z=0.00
        {"num": 1,  "level": "ground",   "x":  -3.75, "y": -1.88, "w": 5.00, "d": 2.70, "vehicleType": "car", "accessible": False},
        {"num": 2,  "level": "ground",   "x": -14.40, "y": -7.30, "w": 5.00, "d": 3.40, "vehicleType": "car", "accessible": False},
        {"num": 3,  "level": "ground",   "x": -14.40, "y": -2.53, "w": 5.00, "d": 3.00, "vehicleType": "car", "accessible": False},
        {"num": 4,  "level": "ground",   "x": -14.40, "y":  0.47, "w": 5.00, "d": 3.00, "vehicleType": "car", "accessible": False},
        {"num": 5,  "level": "ground",   "x": -14.40, "y":  4.49, "w": 5.00, "d": 2.70, "vehicleType": "car", "accessible": False},
        {"num": 6,  "level": "ground",   "x": -14.40, "y":  7.19, "w": 5.00, "d": 2.70, "vehicleType": "car", "accessible": False},
        # Basement Floor East Row Stalls (#7-#10)
        {"num": 7,  "level": "basement", "x":  15.51, "y":  1.74, "w": 5.00, "d": 2.70, "vehicleType": "car", "accessible": False},
        {"num": 8,  "level": "basement", "x":  15.51, "y": -0.81, "w": 5.00, "d": 2.40, "vehicleType": "car", "accessible": False},
        {"num": 9,  "level": "basement", "x":  15.51, "y": -3.36, "w": 5.00, "d": 2.70, "vehicleType": "car", "accessible": False},
        {"num": 10, "level": "basement", "x":  15.51, "y": -7.01, "w": 5.00, "d": 3.40, "vehicleType": "car", "accessible": False},
        # Basement Floor West Row Stalls (#11-#16)
        {"num": 11, "level": "basement", "x": -14.72, "y": -6.85, "w": 5.00, "d": 3.30, "vehicleType": "car", "accessible": False},
        {"num": 12, "level": "basement", "x": -14.72, "y": -3.55, "w": 5.00, "d": 2.63, "vehicleType": "car", "accessible": False},
        {"num": 13, "level": "basement", "x": -14.72, "y": -1.03, "w": 5.00, "d": 2.40, "vehicleType": "car", "accessible": False},
        {"num": 14, "level": "basement", "x": -14.72, "y":  1.49, "w": 5.00, "d": 2.63, "vehicleType": "car", "accessible": False},
        {"num": 15, "level": "basement", "x": -14.72, "y":  4.58, "w": 5.00, "d": 2.63, "vehicleType": "car", "accessible": False},
        {"num": 16, "level": "basement", "x": -14.72, "y":  7.21, "w": 5.00, "d": 2.63, "vehicleType": "car", "accessible": False},
        # Basement Floor Central-West Island Stalls (#17-#19, with #18 Accessible + 130cm Hatched Aisle)
        {"num": 17, "level": "basement", "x":  -3.97, "y":  5.71, "w": 5.00, "d": 2.93, "vehicleType": "car", "accessible": False},
        {"num": 18, "level": "basement", "x":  -3.97, "y":  2.33, "w": 5.00, "d": 2.93, "vehicleType": "car", "accessible": True, "aisleY": 0.22, "aisleD": 1.30},
        {"num": 19, "level": "basement", "x":  -3.92, "y": -1.75, "w": 5.00, "d": 2.63, "vehicleType": "car", "accessible": False},
        # 2 Designated Motorcycle Stalls (אופנוע 210) in Basement per Garmushka Parking Balance
        {"num": 20, "level": "basement", "x":  -5.41, "y":  7.86, "w": 2.10, "d": 1.35, "vehicleType": "motorcycle", "accessible": False},
        {"num": 21, "level": "basement", "x":   4.50, "y": -2.05, "w": 2.10, "d": 1.95, "vehicleType": "motorcycle", "accessible": False},
    ]

    units = []
    apt_num = 1
    for flr in range(1, 9):
        z0 = round(3.50 + (flr - 1) * 3.15, 2)
        z1 = round(z0 + 3.15, 2)
        flr_id = f"f{flr}"
        flr_label = f"קומה {flr}"

        # 1. West Apartment (5 Rooms, 113.3 sqm net interior + 18.8 sqm balcony per Garmushka table)
        is_owner_w = flr in (1, 2, 4)
        st_w = parking_stalls[(apt_num - 1) % 19]
        units.append({
            "id": f"apt_{apt_num}",
            "aptNum": apt_num,
            "bldg": 44,
            "wing": "W",
            "name": f"דירה {apt_num}",
            "shortBadge": f"דירה {apt_num}",
            "floorNum": flr,
            "floorId": flr_id,
            "floorLabel": flr_label,
            "rooms": 5,
            "typeHe": "דירת 5 חדרים מערבית מרווחת (99.86 עיקרי + 13.40 ממ\"ד)",
            "area": 113.3,
            "grossArea": 114.8,
            "balcony": 18.8,
            "directions": "מערב, צפון, דרום (3 כיווני אוויר)",
            "status": "owner" if is_owner_w else "available",
            "statusHe": "דירת בעלים" if is_owner_w else "זמין לשיווק · קולסקי",
            "price": 3480000 + (flr - 1) * 45000,
            "z0": z0,
            "z1": z1,
            "bbox": [-15.36, -5.18, -0.80, 4.22],
            "bx": -14.5,
            "by": 0.0,
            "bz": round(0.5 * (z0 + z1), 2),
            "balcPt": [-14.35, -0.5],
            "lookDir": "W",
            "parkingNum": st_w["num"],
            "parkingLevel": st_w["level"],
            "parkingX": st_w["x"],
            "parkingY": st_w["y"],
        })
        apt_num += 1

        # 2. East Apartment (4 Rooms, 89.4 sqm net interior + 18.8 sqm balcony facing Hafetz Haim St)
        is_owner_e = flr in (1, 3, 5)
        st_e = parking_stalls[(apt_num - 1) % 19]
        units.append({
            "id": f"apt_{apt_num}",
            "aptNum": apt_num,
            "bldg": 44,
            "wing": "E",
            "name": f"דירה {apt_num}",
            "shortBadge": f"דירה {apt_num}",
            "floorNum": flr,
            "floorId": flr_id,
            "floorLabel": flr_label,
            "rooms": 4,
            "typeHe": "דירת 4 חדרים חזיתית לרח' חפץ חיים (77.59 עיקרי + 11.81 ממ\"ד)",
            "area": 89.4,
            "grossArea": 91.8,
            "balcony": 18.8,
            "directions": "מזרח (חזית), צפון, דרום (3 כיווני אוויר)",
            "status": "owner" if is_owner_e else "available",
            "statusHe": "דירת בעלים" if is_owner_e else "זמין לשיווק · קולסקי",
            "price": 2960000 + (flr - 1) * 40000,
            "z0": z0,
            "z1": z1,
            "bbox": [0.80, -5.18, 16.36, 4.22],
            "bx": 15.5,
            "by": 0.0,
            "bz": round(0.5 * (z0 + z1), 2),
            "balcPt": [15.35, -0.5],
            "lookDir": "E",
            "parkingNum": st_e["num"],
            "parkingLevel": st_e["level"],
            "parkingX": st_e["x"],
            "parkingY": st_e["y"],
        })
        apt_num += 1

    # 3. Floor 9 Penthouse (Apt 17 — Full-Floor Luxury Penthouse, 5 Rooms, 148.1 sqm net interior + 73.0 sqm East 456x940 & West 295x940 Roof Terraces)
    st_ph = parking_stalls[9] # Stall #10 + #11 double parking
    units.append({
        "id": "apt_17",
        "aptNum": 17,
        "bldg": 44,
        "wing": "PH",
        "name": "פנטהאוז דירה 17",
        "shortBadge": "פנטהאוז #17",
        "floorNum": 9,
        "floorId": "f9",
        "floorLabel": "קומה 9 (פנטהאוז על קומה שלמה)",
        "rooms": 5,
        "typeHe": "פנטהאוז יוקרה פנורמי על קומה שלמה (139.09 עיקרי + 9.00 ממ\"ד + 72.96 מ\"ר מרפסות גג)",
        "area": 148.1,
        "grossArea": 151.0,
        "balcony": 73.0,
        "directions": "4 כיווני אוויר מלאים (מזרח, מערב, צפון, דרום)",
        "status": "available",
        "statusHe": "זמין לשיווק · פנטהאוז דגל קולסקי",
        "price": 6450000,
        "z0": 28.70,
        "z1": 31.85,
        "bbox": [-13.36, -5.18, 14.36, 5.20],
        "bx": 12.8,
        "by": 0.0,
        "bz": 30.28,
        "balcPt": [11.9, -0.5],
        "lookDir": "E",
        "parkingNum": st_ph["num"],
        "parkingLevel": st_ph["level"],
        "parkingX": st_ph["x"],
        "parkingY": st_ph["y"],
    })

    return {
        "project": {
            "name": "חפץ חיים 44, פתח תקווה",
            "developer": "קולסקי",
            "architect": "סטודיו אורכה — אדר' אורן קמה",
            "gush": 6396,
            "helka": 85,
            "buildingFile": "18-3-2465",
            "permitRequest": "20200777",
            "datumZeroAbs": 47.90,
            "lotAreaSqm": 712,
        },
        "units": units,
        "parking_stalls": parking_stalls,
    }

if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)
    plans_data = process_all_plans()
    plans_out_path = os.path.join(DATA_DIR, "hafetz44_extracted_plans.json")
    with open(plans_out_path, "w", encoding="utf-8") as f:
        json.dump(plans_data, f, ensure_ascii=False)
    print(f"Saved {plans_out_path} ({os.path.getsize(plans_out_path):,} bytes)")

    crm_data = build_crm_data()
    crm_out_path = os.path.join(DATA_DIR, "hafetz44_units_crm.json")
    with open(crm_out_path, "w", encoding="utf-8") as f:
        json.dump(crm_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {crm_out_path} ({len(crm_data['units'])} units, {len(crm_data['parking_stalls'])} parking stalls)")
