# -*- coding: utf-8 -*-
"""
Renders high-resolution architectural floor plan PNGs for Feierberg 3, Petah Tikva
into webapp/uploads/ using PyMuPDF (fitz) from the verified 1:1 vector geometry in
feierberg3_extracted_plans.json.
Coordinate system in feierberg3_extracted_plans.json:
  X in [-18.5, +18.5] meters (West = -X, East = +X, span = 37.0m)
  Z in [-9.5,  +9.5]  meters (North = -Z, South/Feierberg St. = +Z, span = 19.0m)
"""

import json
import os
import sys
import fitz

sys.stdout.reconfigure(encoding="utf-8")

PLANS_JSON = r"G:\Shared drives\פרויקטים שוטפים\פרויקטים בביצוע\פאירברג 3\מודל\data\feierberg3_extracted_plans.json"
OUT_DIR = r"c:\Users\User\archknow\webapp\uploads"
os.makedirs(OUT_DIR, exist_ok=True)

CANVAS_W = 1800.0
CANVAS_H = 1050.0

X_MIN, X_MAX = -18.5, 18.5   # 37.0m span
Z_MIN, Z_MAX = -9.5, 9.5     # 19.0m span


def world_to_pt(xm, zm):
    px = (xm - X_MIN) / (X_MAX - X_MIN) * CANVAS_W
    py = (zm - Z_MIN) / (Z_MAX - Z_MIN) * CANVAS_H
    return fitz.Point(px, py)


def rgb(r, g, b):
    return (r / 255.0, g / 255.0, b / 255.0)


with open(PLANS_JSON, "r", encoding="utf-8") as f:
    plans_data = json.load(f)

SHEETS_SPEC = [
    (
        "floors_1_7",
        "feierberg3_typical.png",
        "פאירברג 3, פתח תקווה — קומות 1–8 (קומה טיפוסית: דירות 4 חד׳ מערב 105.5 מ״ר ומזרח 85.5 מ״ר)",
        "גיליון FA-P1-8 · מפלס +3.50m עד +25.55m · קנ״מ 1:50 · א. קולסקי · אלישע רובין אדריכלים",
    ),
    (
        "floor_9",
        "feierberg3_floor9.png",
        "פאירברג 3, פתח תקווה — קומה 9 (מפלס תחתון דופלקס-פנטהאוזים #17 ו-#18 + מרפסות גג היקפיות)",
        "גיליון FA-P9 · מפלס +28.87m · מרפסות גג: מערב 43.3 מ״ר + מזרח 36.4 מ״ר · קנ״מ 1:50",
    ),
    (
        "floor_10",
        "feierberg3_floor10.png",
        "פאירברג 3, פתח תקווה — קומה 10 (מפלס עליון דופלקס-פנטהאוזים #17 ו-#18 — סוויטות הורים וגלריות)",
        "גיליון FA-P10 · מפלס +32.02m · קנ״מ 1:50",
    ),
    (
        "ground",
        "feierberg3_ground.png",
        "פאירברג 3, פתח תקווה — קומת קרקע ופיתוח מגרש (±0.00m · לובי, מועדון דיירים, אופניים, אשפה ורמפה)",
        "גיליון הגשה קרקע · מפלס ±0.00m · מגרש 548 מ״ר (33.5×16.4 מ׳)",
    ),
    (
        "basement_1",
        "feierberg3_basement1.png",
        "פאירברג 3, פתח תקווה — קומת מרתף 1- (חניון עליון: 8 חניות רגילות #1–#8, רמפה דו-שיפועית וגרעין)",
        "גיליון מרתף 1- · מפלס -4.80m · קנ״מ 1:50",
    ),
    (
        "basement_2",
        "feierberg3_basement2.png",
        "פאירברג 3, פתח תקווה — קומת מרתף 2- (חניון תחתון: 11 חניות רגילות #9–#19, בורות שאיבה וגרעין)",
        "גיליון מרתף 2- · מפלס -7.80m · קנ״מ 1:50",
    ),
]

for plan_key, out_fn, title_he, sub_he in SHEETS_SPEC:
    pdata = plans_data[plan_key]
    doc = fitz.open()
    page = doc.new_page(width=CANVAS_W, height=CANVAS_H)
    shape = page.new_shape()

    # Background
    shape.draw_rect(fitz.Rect(0, 0, CANVAS_W, CANVAS_H))
    shape.finish(fill=rgb(248, 250, 252), color=None)

    # 1. Metric grid
    for xm in range(-18, 19):
        p1 = world_to_pt(xm, -9.0)
        p2 = world_to_pt(xm, 9.0)
        shape.draw_line(p1, p2)
        is_major = (xm % 5 == 0)
        shape.finish(color=rgb(226, 232, 240) if is_major else rgb(241, 245, 249), width=1.0 if is_major else 0.5)

    for zm in range(-9, 10):
        p1 = world_to_pt(-18.0, zm)
        p2 = world_to_pt(18.0, zm)
        shape.draw_line(p1, p2)
        is_major = (zm % 5 == 0)
        shape.finish(color=rgb(226, 232, 240) if is_major else rgb(241, 245, 249), width=1.0 if is_major else 0.5)

    # 2. Lot boundary (-16.75..+16.75 x -8.20..+8.20)
    lp0 = world_to_pt(-16.75, -8.20)
    lp1 = world_to_pt(16.75, 8.20)
    shape.draw_rect(fitz.Rect(lp0, lp1))
    shape.finish(color=rgb(148, 163, 184), width=1.8, dashes="[6 4] 0")

    # 3. Main Slab Polygon
    slab = pdata.get("slab_poly", {})
    if slab and slab.get("outline"):
        pts = [world_to_pt(p[0], p[1]) for p in slab["outline"]]
        if len(pts) >= 3:
            shape.draw_polyline(pts + [pts[0]])
            fill_col = rgb(241, 245, 249) if "basement" in plan_key else rgb(255, 255, 255)
            shape.finish(fill=fill_col, color=rgb(100, 116, 139), width=1.5)
            for hole in slab.get("holes", []):
                hpts = [world_to_pt(p[0], p[1]) for p in hole]
                if len(hpts) >= 3:
                    shape.draw_polyline(hpts + [hpts[0]])
                    shape.finish(fill=rgb(226, 232, 240), color=rgb(71, 85, 105), width=1.2)

    # 4. Balconies & Roof Terraces
    for bpoly in pdata.get("balc_polys", []):
        if bpoly.get("outline"):
            pts = [world_to_pt(p[0], p[1]) for p in bpoly["outline"]]
            if len(pts) >= 3:
                shape.draw_polyline(pts + [pts[0]])
                shape.finish(fill=rgb(240, 249, 255), color=rgb(14, 165, 233), width=1.5)

    # 5. Pergola Polygons
    for ppoly in pdata.get("pergola_polys", []):
        if ppoly.get("outline"):
            pts = [world_to_pt(p[0], p[1]) for p in ppoly["outline"]]
            if len(pts) >= 3:
                shape.draw_polyline(pts + [pts[0]])
                shape.finish(fill=rgb(224, 242, 254), color=rgb(2, 132, 199), width=1.0)

    # 6. 2D CAD lines & Furniture lines
    for seg in pdata.get("cad_lines", []):
        p1 = world_to_pt(seg[0], seg[1])
        p2 = world_to_pt(seg[2], seg[3])
        shape.draw_line(p1, p2)
        shape.finish(color=rgb(148, 163, 184), width=0.9)

    for seg in pdata.get("furn_lines", []):
        p1 = world_to_pt(seg[0], seg[1])
        p2 = world_to_pt(seg[2], seg[3])
        shape.draw_line(p1, p2)
        shape.finish(color=rgb(100, 116, 139), width=0.9)

    # 7. Furniture & Parking Stalls
    stall_labels = []
    for item in pdata.get("furn_items", []):
        p0 = world_to_pt(item["x0"], item["y0"])
        p1 = world_to_pt(item["x1"], item["y1"])
        r = fitz.Rect(min(p0.x, p1.x), min(p0.y, p1.y), max(p0.x, p1.x), max(p0.y, p1.y))
        kind = item.get("kind", "")
        if kind == "car_stall":
            shape.draw_rect(r)
            shape.finish(fill=rgb(224, 242, 254), color=rgb(2, 132, 199), width=1.8)
            stall_labels.append((r, item.get("id", "P")))
        elif kind in ("bed_double", "bed_single", "sofa", "sofa_east_f4"):
            shape.draw_rect(r)
            shape.finish(fill=rgb(254, 243, 199), color=rgb(217, 119, 6), width=1.0)
        elif kind in ("kcounter", "fridge", "ksink", "stove"):
            shape.draw_rect(r)
            shape.finish(fill=rgb(220, 252, 231), color=rgb(22, 163, 74), width=1.0)
        elif kind in ("bathtub", "shower", "toilet", "vanity", "washer"):
            shape.draw_rect(r)
            shape.finish(fill=rgb(224, 231, 255), color=rgb(79, 70, 229), width=1.0)
        else:
            shape.draw_rect(r)
            shape.finish(fill=rgb(241, 245, 249), color=rgb(100, 116, 139), width=0.9)

    # 8. Structural & Interior Walls
    for wpoly in pdata.get("wall_polys", []):
        if wpoly.get("outline"):
            pts = [world_to_pt(p[0], p[1]) for p in wpoly["outline"]]
            if len(pts) >= 3:
                shape.draw_polyline(pts + [pts[0]])
                shape.finish(fill=rgb(30, 41, 59), color=rgb(15, 23, 42), width=1.0)
            for hole in wpoly.get("holes", []):
                hpts = [world_to_pt(p[0], p[1]) for p in hole]
                if len(hpts) >= 3:
                    shape.draw_polyline(hpts + [hpts[0]])
                    shape.finish(fill=rgb(255, 255, 255), color=rgb(30, 41, 59), width=1.0)

    # 9. Railing segments
    for rseg in pdata.get("railing_segs", []):
        p1 = world_to_pt(rseg[0], rseg[1])
        p2 = world_to_pt(rseg[2], rseg[3])
        shape.draw_line(p1, p2)
        shape.finish(color=rgb(2, 132, 199), width=2.8)

    # 10. Architectural Openings
    for op in pdata.get("openings", []):
        orient, x0, z0, x1, z1, kind = op
        p0 = world_to_pt(x0, z0)
        p1 = world_to_pt(x1, z1)
        r = fitz.Rect(min(p0.x, p1.x) - 1, min(p0.y, p1.y) - 1, max(p0.x, p1.x) + 1, max(p0.y, p1.y) + 1)
        if kind in ("window", "vitrine"):
            shape.draw_rect(r)
            shape.finish(fill=rgb(186, 230, 253), color=rgb(2, 132, 199), width=1.8)
        elif kind == "mamad_win":
            shape.draw_rect(r)
            shape.finish(fill=rgb(254, 202, 202), color=rgb(220, 38, 38), width=1.8)
        elif kind == "door":
            shape.draw_rect(r)
            shape.finish(fill=rgb(254, 240, 138), color=rgb(202, 138, 4), width=1.6)

    # Header & Footer Bars
    shape.draw_rect(fitz.Rect(0, 0, CANVAS_W, 56))
    shape.finish(fill=rgb(15, 23, 42), color=None)
    shape.draw_rect(fitz.Rect(0, CANVAS_H - 38, CANVAS_W, CANVAS_H))
    shape.finish(fill=rgb(226, 232, 240), color=None)

    shape.commit()

    # Insert Header & Footer HTML boxes with full native Hebrew RTL
    page.insert_htmlbox(
        fitz.Rect(20, 6, CANVAS_W - 20, 52),
        f"""
        <div dir="rtl" style="font-family: Arial, sans-serif; display:flex; justify-content:space-between; align-items:center;">
          <div style="color:#ffffff; font-size:19px; font-weight:bold;">{title_he}</div>
          <div style="color:#94a3b8; font-size:13px; margin-top:2px;">{sub_he}</div>
        </div>
        """,
    )

    page.insert_htmlbox(
        fitz.Rect(20, 60, CANVAS_W - 20, 86),
        """
        <div dir="rtl" style="font-family: Arial, sans-serif; text-align:center; color:#475569; font-size:12.5px; font-weight:bold;">
          ⬆ חזית צפונית (עורפית) · קו בניין 4.00 מ׳ ⬆
        </div>
        """,
    )

    page.insert_htmlbox(
        fitz.Rect(20, CANVAS_H - 32, CANVAS_W - 20, CANVAS_H - 4),
        """
        <div dir="rtl" style="font-family: Arial, sans-serif; text-align:center; color:#1e3a8a; font-size:13.5px; font-weight:bold;">
          ⬇ חזית דרומית ראשית — רחוב פאירברג 3, פתח תקווה (גוש 6387, חלקה 193) ⬇
        </div>
        """,
    )

    # Parking stall IDs
    for r, pid_txt in stall_labels:
        page.insert_htmlbox(
            r,
            f'<div style="font-family:Arial,sans-serif;font-size:13px;font-weight:bold;color:#0369a1;text-align:center;padding-top:14px;">{pid_txt}</div>',
        )

    # Room Labels
    for rl in pdata.get("room_labels", []):
        pt = world_to_pt(rl["x"], rl["z"])
        lbl_rect = fitz.Rect(pt.x - 135, pt.y - 16, pt.x + 135, pt.y + 18)
        page.insert_htmlbox(
            lbl_rect,
            f"""
            <div dir="rtl" style="font-family:Arial,sans-serif;font-size:11.5px;font-weight:bold;color:#0f172a;background-color:#ffffff;border:1px solid #94a3b8;border-radius:4px;padding:2px 5px;text-align:center;">
              {rl["name"]}
            </div>
            """,
        )

    pix = page.get_pixmap(dpi=96)
    out_path = os.path.join(OUT_DIR, out_fn)
    pix.save(out_path)
    doc.close()
    print(f"[OK] Rendered {out_path} ({pix.width}x{pix.height})")

import shutil
MODEL_DIR = r"G:\Shared drives\פרויקטים שוטפים\פרויקטים בביצוע\פאירברג 3\מודל"
WEBAPP_DIR = r"c:\Users\User\archknow\webapp"
for fn in ["feierberg3_3d_bim_viewer.html", "feierberg3_spatial_map.html", "feierberg3_model.glb", "feierberg3_model.obj", "feierberg3_model.mtl"]:
    src_p = os.path.join(MODEL_DIR, fn)
    dst_p = os.path.join(WEBAPP_DIR, fn)
    if os.path.exists(src_p):
        shutil.copy2(src_p, dst_p)
        print(f"[OK] Copied {fn} to webapp/")

