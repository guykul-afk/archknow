"""
plan_analyzer.pipeline — builds the *Plan Data Model* (the analysis database) from
an architectural PDF. Workflow adapted from the `arch-2d-to-3d-bim` skill
("מידול אדריכלי"), stopping before 3D:

  1. Sheet intake        render, text layer, sheet classification      (skill step 1)
  2. Reading & datum     title block, scale, labels, dimensions, north  (skill step 2)
  3. 2D model            walls, openings, spaces, topology              (skill step 3, no extrusion)
  4. Validation          scale / area / dimension / ממ"ד / topology QA  (skill step 4a)
  5. Engine adapter      apartment JSON for validation_engine           (adapter.py)

Zero-trust: every value carries provenance; nothing is defaulted silently.
"""
import datetime
import math
import os

import numpy as np
from scipy import ndimage as ndi

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover
    fitz = None

from . import geometry as G
from . import reading as R
from . import qa as QA
from .taxonomy import (classify_label, is_in_unit, INTERIOR_TYPES, OUTDOOR_TYPES, HABITABLE_TYPES,
                       WET_TYPES, ROOM_COUNT_TYPES)

SCHEMA_VERSION = "archknow.plan-model/1.0"
PT_TO_CM = 2.54 / 72.0

# Datum & rules defaults (skill step 2 / Israeli practice). Used ONLY for clearly
# flagged estimates (window glazing area); never as measured facts.
DEFAULTS = {
    "door_h_m": 2.10,        # בקע 2.10
    "win_sill_m": 1.00,      # בקת 1.00
    "win_lintel_m": 2.10,    # ק.ע. 2.10
    "mamad_wall_min_cm": 20.0,
}

STAGES = [
    {"id": 1, "name": "sheet_intake", "he": "קליטת גיליון: רינדור, שכבת טקסט, סיווג"},
    {"id": 2, "name": "reading_datum", "he": "קריאה ועוגנים: טבלת שרטוט, קנה מידה, תוויות, מידות, צפון"},
    {"id": 3, "name": "model_2d", "he": "מודל דו-ממדי: קירות, פתחים, חללים, טופולוגיה"},
    {"id": 4, "name": "validation", "he": "ולידציה: קנה מידה, שטחים, מידות, ממ\"ד, טופולוגיה"},
    {"id": 5, "name": "engine_adapter", "he": "המרה לנתוני מנוע הניתוח"},
]


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------
def _parse_scale(s):
    if not s:
        return None
    import re
    m = re.search(r"1\s*:\s*(\d+)", str(s))
    if m:
        v = float(m.group(1))
        return v if 5 <= v <= 1000 else None
    return None


def _nearest_free(lab, x, y, radius):
    H, W = lab.shape
    x, y = int(round(x)), int(round(y))
    if 0 <= y < H and 0 <= x < W and lab[y, x] > 0:
        return int(lab[y, x])
    for r in range(2, radius + 1, 2):
        y0, y1, x0, x1 = max(0, y - r), min(H, y + r + 1), max(0, x - r), min(W, x + r + 1)
        win = lab[y0:y1, x0:x1]
        nz = win[win > 0]
        if nz.size:
            return int(np.bincount(nz).argmax())
    return 0


def _mask_polygon(mask, cm_per_px, origin=(0, 0)):
    """Outer boundary polygon (cm) of a boolean mask via row-run rectangles."""
    try:
        from shapely.geometry import box
        from shapely.ops import unary_union
    except ImportError:
        return None
    ys, xs = np.nonzero(mask)
    if ys.size == 0:
        return None
    rects = []
    for y in np.unique(ys):
        row = mask[y]
        d = np.diff(np.concatenate([[0], row.astype(np.int8), [0]]))
        starts, ends = np.flatnonzero(d == 1), np.flatnonzero(d == -1)
        for s, e in zip(starts, ends):
            rects.append(box(s, y, e, y + 1))
    geom = unary_union(rects)
    if geom.geom_type == "MultiPolygon":
        geom = max(geom.geoms, key=lambda g: g.area)
    geom = geom.simplify(1.5, preserve_topology=True)
    ox, oy = origin
    return [[round((x + ox) * cm_per_px, 1), round((y + oy) * cm_per_px, 1)] for x, y in geom.exterior.coords[:-1]]


def _min_rect_dims(poly_cm):
    try:
        from shapely.geometry import Polygon
        r = Polygon(poly_cm).minimum_rotated_rectangle
        c = list(r.exterior.coords)
        a, b = math.dist(c[0], c[1]), math.dist(c[1], c[2])
        return min(a, b), max(a, b)
    except Exception:
        return None, None


def _compass(bearing):
    b = bearing % 360
    return "N" if (b >= 315 or b < 45) else "E" if b < 135 else "S" if b < 225 else "W"


# ---------------------------------------------------------------------------
# stage 3a — geometry
# ---------------------------------------------------------------------------
def _main_structure(walls, cm_per_px):
    """Drop wall-like blobs far from the main plan (title-block glyphs, logos).
    Pieces near the main plan's bounding box (e.g. piers between large windows) are kept."""
    k = max(1, int(round(40 / cm_per_px)))
    grown = ndi.binary_dilation(walls, iterations=k)
    lab, n = ndi.label(grown)
    if n <= 1:
        return walls
    sizes = ndi.sum(walls, lab, index=np.arange(1, n + 1))
    objs = ndi.find_objects(lab)
    big = [i for i in range(n) if sizes[i] >= 0.05 * sizes.max() and objs[i] is not None]
    pad = int(round((G.OPENING_MAX_CM + 40) / cm_per_px))
    my0 = min(objs[i][0].start for i in big) - pad
    my1 = max(objs[i][0].stop for i in big) + pad
    mx0 = min(objs[i][1].start for i in big) - pad
    mx1 = max(objs[i][1].stop for i in big) + pad
    keep = np.zeros(n + 1, bool)
    for i, sl in enumerate(objs, start=1):
        if sl is None:
            continue
        inside = sl[0].start >= my0 and sl[0].stop <= my1 and sl[1].start >= mx0 and sl[1].stop <= mx1
        keep[i] = (i - 1) in big or inside
    return walls & keep[lab]


def run_geometry(page, zoom, cm_per_px):
    img = G.render_page(page, zoom)
    walls = G.wall_mask(img, cm_per_px)
    walls = _main_structure(walls, cm_per_px)
    dark = G.dark_mask(img, page, zoom)
    br_mask, bridges = G.find_openings(walls, cm_per_px, dark)
    lab, info = G.segment_spaces(walls | br_mask, cm_per_px)
    arcs = G.door_arcs(page, zoom, cm_per_px)
    openings = G.classify_openings(lab, info, bridges, arcs, cm_per_px)
    return {"img": img, "walls": walls, "dark": dark, "bridges": br_mask, "lab": lab, "info": info,
            "arcs": arcs, "openings": openings}


# ---------------------------------------------------------------------------
# stage 2b — dimension lines (scale verification + room extents)
# ---------------------------------------------------------------------------
def _axis_lines(page):
    """Axis-aligned straight segments of the vector layer, in pt: (x0,y0,x1,y1,horizontal)."""
    hs, vs = [], []
    for d in page.get_drawings():
        for it in d.get("items", []):
            if it[0] != "l":
                continue
            p1, p2 = it[1], it[2]
            dx, dy = abs(p2.x - p1.x), abs(p2.y - p1.y)
            if dy < 0.25 and dx > 4:
                hs.append((min(p1.x, p2.x), p1.y, max(p1.x, p2.x), p2.y))
            elif dx < 0.25 and dy > 4:
                vs.append((p1.x, min(p1.y, p2.y), p2.x, max(p1.y, p2.y)))
    return np.array(hs, float).reshape(-1, 4), np.array(vs, float).reshape(-1, 4)


def match_dimension_lines(page, dims, cm_per_pt):
    """Find the dimension line drawn under each written dimension.
    Returns list of matches {value_cm, line_pt:[x0,y0,x1,y1], orientation, ratio}."""
    W, H = page.rect.width, page.rect.height
    hs, vs = _axis_lines(page)
    out = []
    for d in dims:
        b = d["box"]
        cx, cy = (b[0] + b[2]) / 2 * W, (b[1] + b[3]) / 2 * H
        horiz = d.get("orientation", "horizontal").startswith("h")
        th = max(((b[3] - b[1]) * H) if horiz else ((b[2] - b[0]) * W), 3.0)
        exp_len = d["value_cm"] / cm_per_pt
        L = hs if horiz else vs
        if L.size == 0:
            continue
        if horiz:
            along0, along1, perp, c_al, c_pe = L[:, 0], L[:, 2], L[:, 1], cx, cy
        else:
            along0, along1, perp, c_al, c_pe = L[:, 1], L[:, 3], L[:, 0], cy, cx
        length = along1 - along0
        ratio = length / exp_len
        dp = np.abs(perp - c_pe)
        ok = (along0 - 2 <= c_al) & (c_al <= along1 + 2) & (dp <= max(2.5 * th, 8.0)) & \
             (ratio > 0.80) & (ratio < 1.25)
        if not ok.any():
            continue
        score = np.where(ok, np.abs(ratio - 1) + 0.02 * dp / th, np.inf)
        i = int(np.argmin(score))
        out.append({"value_cm": d["value_cm"], "orientation": "horizontal" if horiz else "vertical",
                    "line_pt": [float(v) for v in L[i]], "ratio": float(ratio[i]), "box": b})
    return out


# ---------------------------------------------------------------------------
# stage 3b — region splitting for open plans with several labels
# ---------------------------------------------------------------------------
def _geodesic_partition(region, seeds):
    """Multi-source constrained growth. `seeds`: int array (0 = unassigned) inside `region`."""
    assign = seeds.copy()
    st = ndi.generate_binary_structure(2, 1)
    for _ in range(4000):
        un = region & (assign == 0)
        if not un.any():
            break
        grew = False
        for k in np.unique(assign[assign > 0]):
            g = ndi.binary_dilation(assign == k, structure=st) & un
            if g.any():
                assign[g] = k
                un &= ~g
                grew = True
        if not grew:
            break
    return assign


def split_region(region, labels, dims_px, dark):
    """Split a region (bool mask, crop) among several labels.

    labels: list of (x, y) in crop px. dims_px: list of dicts with 'orientation'
    and 'span' (x0,y0,x1,y1) in crop px. Returns (assign int array, method)."""
    H, W = region.shape
    n = len(labels)
    seeds = np.zeros(region.shape, np.int32)
    # 1) exclusive rectangles from the written room dimensions
    rects = {}
    for i, (lx, ly) in enumerate(labels):
        hs = [d for d in dims_px if d["orientation"] == "horizontal" and d["span"][0] - 4 <= lx <= d["span"][2] + 4]
        vs = [d for d in dims_px if d["orientation"] == "vertical" and d["span"][1] - 4 <= ly <= d["span"][3] + 4]
        if hs and vs:
            h = min(hs, key=lambda d: abs(d["span"][1] - ly))
            v = min(vs, key=lambda d: abs(d["span"][0] - lx))
            r = (h["span"][0], v["span"][1], h["span"][2], v["span"][3])
            others = [labels[j] for j in range(n) if j != i]
            if not any(r[0] <= ox <= r[2] and r[1] <= oy <= r[3] for ox, oy in others):
                rects[i] = r
    if rects:
        for i, r in sorted(rects.items(), key=lambda kv: -(kv[1][2] - kv[1][0]) * (kv[1][3] - kv[1][1])):
            x0, y0, x1, y1 = [int(round(v)) for v in r]
            sub = np.zeros_like(region)
            sub[max(0, y0 - 3):min(H, y1 + 4), max(0, x0 - 3):min(W, x1 + 4)] = True
            seeds[sub & region] = i + 1
        for i, (lx, ly) in enumerate(labels):
            if i not in rects:
                yy, xx = int(np.clip(ly, 0, H - 1)), int(np.clip(lx, 0, W - 1))
                if region[yy, xx] and seeds[yy, xx] == 0:
                    seeds[max(0, yy - 2):yy + 3, max(0, xx - 2):xx + 3] = i + 1
        return _geodesic_partition(region, seeds * region), "written_dimensions"
    # 2) a straight drawn line spanning the region between two labels
    if n == 2:
        (x1, y1), (x2, y2) = labels
        vertical_sep = abs(y2 - y1) >= abs(x2 - x1)
        a, b = (int(min(y1, y2)), int(max(y1, y2))) if vertical_sep else (int(min(x1, x2)), int(max(x1, x2)))
        best = None
        for t in range(a + 3, b - 2):
            line_reg = region[t, :] if vertical_sep else region[:, t]
            line_dark = (dark[t, :] if vertical_sep else dark[:, t]) & line_reg
            nreg = line_reg.sum()
            if nreg > 10 and line_dark.sum() >= 0.85 * nreg:
                dist = abs(t - (a + b) / 2)
                if best is None or dist < best[0]:
                    best = (dist, t)
        if best is not None:
            t = best[1]
            assign = np.zeros(region.shape, np.int32)
            first = 1 if (y1 < y2 if vertical_sep else x1 < x2) else 2
            if vertical_sep:
                assign[:t, :] = first
                assign[t:, :] = 3 - first
            else:
                assign[:, :t] = first
                assign[:, t:] = 3 - first
            return assign * region, "drawn_line"
    # 3) geodesic Voronoi from the label positions
    for i, (lx, ly) in enumerate(labels):
        yy, xx = int(np.clip(ly, 0, H - 1)), int(np.clip(lx, 0, W - 1))
        seeds[max(0, yy - 2):yy + 3, max(0, xx - 2):xx + 3] = i + 1
    return _geodesic_partition(region, seeds * region), "label_voronoi"


# ---------------------------------------------------------------------------
# stage 3c — outdoor spaces drawn without closing walls (balconies)
# ---------------------------------------------------------------------------
def outdoor_mask(geo, cx, cy, cm_per_px, written_area_m2=None, dims_px=None, other_labels=()):
    """Balcony footprint around a label lying in the exterior.

    1) rectangle spanned by the written dimension lines nearest the label
       (horizontal × vertical), intersected with non-wall exterior;
    2) fallback: free space bounded by walls *and* drawn lines (railings),
       merging fragments cut by dimension lines."""
    lab, info, dark = geo["lab"], geo["info"], geo["dark"]
    ext_ids = [i for i, v in info.items() if v["exterior"]]
    ext = np.isin(lab, ext_ids)
    H, W = lab.shape
    px_area = (cm_per_px ** 2) / 1e4
    if dims_px:
        hs = [d for d in dims_px if d["orientation"] == "horizontal" and d["span"][0] - 4 <= cx <= d["span"][2] + 4]
        vs = [d for d in dims_px if d["orientation"] == "vertical" and d["span"][1] - 4 <= cy <= d["span"][3] + 4]
        if hs and vs:
            h = min(hs, key=lambda d: abs(d["span"][1] - cy))
            v = min(vs, key=lambda d: abs(d["span"][0] - cx))
            x0, x1 = int(round(h["span"][0])), int(round(h["span"][2]))
            y0, y1 = int(round(v["span"][1])), int(round(v["span"][3]))
            if not any(x0 <= ox <= x1 and y0 <= oy <= y1 for ox, oy in other_labels):
                m = np.zeros(lab.shape, bool)
                m[max(0, y0):min(H, y1), max(0, x0):min(W, x1)] = True
                m &= ext
                a = m.sum() * px_area
                if a > 0.5 and (not written_area_m2 or 0.7 <= a / written_area_m2 <= 1.3):
                    return m
    free = ext & ~ndi.binary_dilation(dark, iterations=1)
    comp, n = ndi.label(free)
    start = _nearest_free(comp, cx, cy, 25)
    if not start:
        return None
    border = set(np.unique(np.concatenate([comp[0], comp[-1], comp[:, 0], comp[:, -1]])).tolist())
    if start in border:
        return None
    sizes = ndi.sum(free, comp, index=np.arange(n + 1))
    chosen = {start}
    mask = comp == start
    limit = (written_area_m2 * 1.08) if written_area_m2 else 40.0
    for _ in range(60):
        ring = ndi.binary_dilation(mask, iterations=3) & ~mask
        cand = [c for c in np.unique(comp[ring]) if c and c not in chosen and c not in border]
        cand = [c for c in cand if sizes[c] * px_area < 25.0]
        if not cand:
            break
        added = False
        for c in sorted(cand, key=lambda c: -sizes[c]):
            new_area = (mask.sum() + sizes[c]) * px_area
            if new_area > limit:
                continue
            chosen.add(c)
            mask |= comp == c
            added = True
        if not added:
            break
    mask = ndi.binary_closing(mask, iterations=2) & ext
    return mask


# ---------------------------------------------------------------------------
# main entry
# ---------------------------------------------------------------------------
def analyze_pdf(pdf_path, work_dir, file_hash, preview_dir=None, use_vision=True,
                reading_override=None, log=print):
    """Analyse every plan page of a PDF. Returns the plan model (dict)."""
    if fitz is None:
        raise RuntimeError("PyMuPDF is required")
    doc = fitz.open(pdf_path)
    if len(doc) == 0:
        raise ValueError("הקובץ ריק או אינו תקין.")
    os.makedirs(work_dir, exist_ok=True)
    preview_dir = preview_dir or work_dir
    os.makedirs(preview_dir, exist_ok=True)
    sheets, warnings = [], []
    for pno in range(len(doc)):
        page = doc[pno]
        suffix = "" if pno == 0 else f"_p{pno + 1}"
        try:
            sheet = analyze_page(page, pno, work_dir, preview_dir, f"{file_hash}{suffix}",
                                 use_vision=use_vision,
                                 reading_override=(reading_override[pno] if isinstance(reading_override, list)
                                                   else reading_override),
                                 log=log)
        except Exception as e:  # keep other pages
            warnings.append(f"עמוד {pno + 1}: {e}")
            log(f"[plan_analyzer] page {pno + 1} failed: {e}")
            continue
        if sheet is not None:
            sheets.append(sheet)
    doc.close()
    return {
        "schema": SCHEMA_VERSION,
        "source_file": os.path.basename(pdf_path),
        "file_hash": file_hash,
        "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "workflow": STAGES,
        "defaults": DEFAULTS,
        "sheets": sheets,
        "warnings": warnings,
    }


def analyze_page(page, pno, work_dir, preview_dir, stem, use_vision=True, reading_override=None, log=print):
    W_pt, H_pt = page.rect.width, page.rect.height
    warnings = []

    # ---------------- stage 1: sheet intake ----------------
    prev_zoom = 2.0
    pix = page.get_pixmap(matrix=fitz.Matrix(prev_zoom, prev_zoom), alpha=False)
    preview_name = f"{stem}_page.png"
    pix.save(os.path.join(preview_dir, preview_name))
    has_text = len(page.get_text("words")) >= 5

    # ---------------- stage 2: reading & datum ----------------
    if reading_override is not None:
        reading = R.normalise_reading(reading_override, reading_override.get("source", "override"))
        read_err = None
    else:
        text_rd = R.read_text_layer(page) if has_text else None
        vis_rd, read_err = (None, None)
        if use_vision and (text_rd is None or len(text_rd["spaces"]) < 3 or len(text_rd["dimensions"]) < 3):
            vis_rd, read_err = R.read_with_vision(pix.tobytes("png"),
                                                  cache_path=os.path.join(work_dir, f"{stem}_vision.json"))
        reading = R.merge_readings(text_rd, vis_rd) if (text_rd or vis_rd) else None
    if read_err:
        warnings.append(read_err)
    if reading is None:
        reading = R.normalise_reading({}, "none")
        warnings.append("לא נמצאה שכבת טקסט ולא בוצעה קריאת Vision — חללים יזוהו גאומטרית בלבד, ללא שמות ומידות כתובות.")
    sheet_meta = reading.get("sheet") or {}
    scale = _parse_scale(sheet_meta.get("scale"))
    scale_source = "title_block" if scale else "default"
    if not scale:
        scale = 50.0
        warnings.append("קנה מידה לא זוהה בגיליון — הונח 1:50 ונבדק מול המידות הכתובות.")
    cm_per_pt = PT_TO_CM * scale

    # verify / calibrate the scale against written dimensions (skill step 4: dimension checksum)
    matches = match_dimension_lines(page, reading["dimensions"], cm_per_pt)
    calib = {"matched_dimensions": len(matches), "total_dimensions": len(reading["dimensions"]),
             "correction": 1.0, "median_error_pct": None}
    if matches:
        ratios = np.array([m["ratio"] for m in matches])
        corr = float(np.median(1.0 / ratios))  # value / measured
        calib["median_error_pct"] = round(float(np.median(np.abs(ratios - 1.0))) * 100, 2)
        if len(matches) >= 3 and abs(corr - 1.0) > 0.015:
            calib["correction"] = round(corr, 4)
            cm_per_pt *= corr
            scale_source += "+dimension_calibration"
            warnings.append(f"קנה המידה תוקן בפקטור {corr:.3f} לפי {len(matches)} מידות כתובות.")
            matches = match_dimension_lines(page, reading["dimensions"], cm_per_pt)

    # ---------------- stage 3: 2D model ----------------
    zoom = float(np.clip(cm_per_pt / 0.9, 1.5, 4.0))
    cm_per_px = cm_per_pt / zoom
    geo = run_geometry(page, zoom, cm_per_px)
    lab, info, openings = geo["lab"], geo["info"], geo["openings"]
    Hpx, Wpx = lab.shape
    px_area = (cm_per_px ** 2) / 1e4
    if geo["walls"].sum() < 500:
        log(f"[plan_analyzer] page {pno + 1}: no wall poché found — skipped")
        return None

    def pt2px(x, y):
        return x * zoom, y * zoom

    def nbox_center_px(b):
        return (b[0] + b[2]) / 2 * W_pt * zoom, (b[1] + b[3]) / 2 * H_pt * zoom

    # dimensions in px, attached to the region under the line midpoint
    dims_px = []
    for m in matches:
        x0, y0, x1, y1 = m["line_pt"]
        span = [x0 * zoom, y0 * zoom, x1 * zoom, y1 * zoom]
        rid = _nearest_free(lab, (span[0] + span[2]) / 2, (span[1] + span[3]) / 2, 12)
        dims_px.append({"value_cm": m["value_cm"], "orientation": m["orientation"], "span": span, "region": rid})

    # labels → regions
    radius = int(round(40 / cm_per_px))
    label_items = []
    for s in reading["spaces"]:
        typ, name = classify_label(s["label"])
        cx, cy = nbox_center_px(s["box"])
        rid = _nearest_free(lab, cx, cy, radius)
        label_items.append({"label": s["label"], "name": name, "type": typ, "x": cx, "y": cy,
                            "region": rid, "in_unit": is_in_unit(typ, s.get("inside_unit", True)),
                            "area_written": s.get("area_sqm_written")})

    # ---- region bookkeeping: spaces = (mask on full image, meta) ----
    spaces = []   # list of dicts with "mask"
    used_regions = set()
    by_region = {}
    for li in label_items:
        if li["region"]:
            by_region.setdefault(li["region"], []).append(li)

    for rid, items in by_region.items():
        if info[rid]["exterior"]:
            continue  # outdoor labels handled below
        used_regions.add(rid)
        region_full = lab == rid
        unit_items = [i for i in items if i["in_unit"]] or items
        if len(unit_items) == 1:
            li = unit_items[0]
            spaces.append({"mask": region_full, "item": li, "method": "closed_region", "confidence": 0.9})
            continue
        sl = ndi.find_objects(region_full.astype(np.int32))[0]
        crop = region_full[sl]
        oy, ox = sl[0].start, sl[1].start
        lbls = [(i["x"] - ox, i["y"] - oy) for i in unit_items]
        dloc = [{"orientation": d["orientation"],
                 "span": [d["span"][0] - ox, d["span"][1] - oy, d["span"][2] - ox, d["span"][3] - oy]}
                for d in dims_px if d["region"] == rid]
        assign, method = split_region(crop, lbls, dloc, geo["dark"][sl])
        for k, li in enumerate(unit_items, start=1):
            m = np.zeros_like(region_full)
            m[sl] = assign == k
            if m.sum() * px_area < 0.3:
                warnings.append(f"התווית '{li['name']}' לא קיבלה שטח בחלוקת החלל הפתוח.")
                continue
            spaces.append({"mask": m, "item": li, "method": f"split:{method}", "split_group": rid,
                           "confidence": {"written_dimensions": 0.8, "drawn_line": 0.75}.get(method, 0.6)})

    # geometry-only fallback: no labels at all → every enclosed region is an unlabeled space
    if not label_items:
        for rid, v in info.items():
            if v["exterior"] or v["tiny"] or v["area_m2"] > 80:
                continue
            ys, xs = np.nonzero(lab == rid)
            spaces.append({"mask": lab == rid, "method": "geometry_only", "confidence": 0.4,
                           "item": {"label": None, "name": f"חלל {len(spaces) + 1}", "type": "unknown",
                                    "in_unit": True, "x": float(xs.mean()), "y": float(ys.mean()),
                                    "area_written": None}})
            used_regions.add(rid)

    # outdoor spaces (labels that fall in the exterior)
    for li in label_items:
        if not li["region"] or not info[li["region"]]["exterior"]:
            continue
        if li["type"] not in OUTDOOR_TYPES and li["type"] not in ("unknown",):
            continue
        others = [(o["x"], o["y"]) for o in label_items if o is not li]
        m = outdoor_mask(geo, li["x"], li["y"], cm_per_px, li.get("area_written"), dims_px, others)
        method = "outdoor_dimensions" if (m is not None and dims_px) else "outdoor_lines"
        if m is None or m.sum() * px_area < 0.5:
            spaces.append({"mask": None, "item": li, "method": "label_only", "confidence": 0.5})
        else:
            spaces.append({"mask": m, "item": li, "method": method, "confidence": 0.7})

    # unlabeled interior regions reachable from the unit
    unit_regions = {int(np.bincount(lab[s["mask"]][lab[s["mask"]] > 0]).argmax())
                    for s in spaces if s["mask"] is not None and s["item"]["in_unit"]
                    and s["item"]["type"] in INTERIOR_TYPES | {"unknown"}}
    excluded_regions = {s_rid for s_rid, items in by_region.items()
                        if not info[s_rid]["exterior"] and not any(i["in_unit"] for i in items)}
    adj = {}
    ext_open = set()
    for o in openings:
        a, b = o["regions"]
        if o["kind"] in ("door", "opening"):
            for x, y in (o.get("links") or [[a, b]]):
                if x and y and not info[x]["exterior"] and not info[y]["exterior"]:
                    adj.setdefault(x, set()).add((y, o["kind"]))
                    adj.setdefault(y, set()).add((x, o["kind"]))
        if o["kind"] == "exterior_opening":
            for r in (a, b):
                if r and not info[r]["exterior"]:
                    ext_open.add(r)
    frontier = list(unit_regions)
    reach = set()
    while frontier:
        r = frontier.pop()
        for nb, kind in adj.get(r, ()):
            if nb in used_regions or nb in reach or nb in excluded_regions:
                continue
            if info[nb]["tiny"] or info[nb]["area_m2"] > 60 or nb in ext_open:
                continue
            reach.add(nb)
            frontier.append(nb)
    # group unlabeled regions joined by plain openings into zones
    zones, seen = [], set()
    for r in reach:
        if r in seen:
            continue
        comp, stack = {r}, [r]
        while stack:
            u = stack.pop()
            for nb, kind in adj.get(u, ()):
                if nb in reach and nb not in comp and kind == "opening":
                    comp.add(nb)
                    stack.append(nb)
        seen |= comp
        zones.append(comp)
    for z in zones:
        m = np.isin(lab, list(z))
        spaces.append({"mask": m, "item": {"label": None, "name": None, "type": "corridor_candidate",
                                           "in_unit": True, "x": None, "y": None, "area_written": None},
                       "method": "unlabeled_zone", "confidence": 0.6, "regions": z})

    # ---------------- per-space attributes ----------------
    region_to_space = {}
    model_spaces = []
    fixtures_px = [(f["type"],) + nbox_center_px(f["box"]) for f in reading.get("fixtures", [])]
    for idx, s in enumerate(spaces):
        sid = f"S{idx + 1:02d}"
        s["id"] = sid
        m = s["mask"]
        li = s["item"]
        entry = {"id": sid, "label_raw": li.get("label"), "name": li.get("name"), "type": li["type"],
                 "in_unit": bool(li["in_unit"]), "method": s["method"], "confidence": s["confidence"],
                 "provenance": {}}
        if m is not None:
            ids = lab[m]
            ids = ids[ids > 0]
            for r in np.unique(ids):
                if info[int(r)]["exterior"]:
                    continue  # outdoor footprints are matched by mask, not by the shared exterior region
                region_to_space.setdefault(int(r), []).append(sid)
            area = float(m.sum() * px_area)
            sl = ndi.find_objects(m.astype(np.int32))[0]
            crop = m[sl]
            dt = ndi.distance_transform_edt(crop)
            poly = _mask_polygon(crop, cm_per_px, origin=(sl[1].start, sl[0].start))
            ys, xs = np.nonzero(m)
            entry.update({
                "area_sqm": round(area, 2),
                "inscribed_width_cm": round(float(dt.max()) * 2 * cm_per_px, 1),
                "bbox_cm": [round(sl[1].start * cm_per_px, 1), round(sl[0].start * cm_per_px, 1),
                            round(sl[1].stop * cm_per_px, 1), round(sl[0].stop * cm_per_px, 1)],
                "centroid_pct": [round(float(xs.mean()) / Wpx * 100, 2), round(float(ys.mean()) / Hpx * 100, 2)],
                "polygon_cm": poly,
            })
            entry["provenance"]["area_sqm"] = "measured_geometry"
            if poly and len(poly) >= 3:
                w_, l_ = _min_rect_dims(poly)
                entry["mbr_cm"] = [round(w_, 1), round(l_, 1)] if w_ else None
            # written dimensions inside the space
            hd = [d["value_cm"] for d in dims_px if d["region"] and m[int(np.clip((d["span"][1] + d["span"][3]) / 2, 0, Hpx - 1)),
                                                                     int(np.clip((d["span"][0] + d["span"][2]) / 2, 0, Wpx - 1))]
                  and d["orientation"] == "horizontal"]
            vd = [d["value_cm"] for d in dims_px if d["region"] and m[int(np.clip((d["span"][1] + d["span"][3]) / 2, 0, Hpx - 1)),
                                                                     int(np.clip((d["span"][0] + d["span"][2]) / 2, 0, Wpx - 1))]
                  and d["orientation"] == "vertical"]
            entry["written_dimensions_cm"] = {"horizontal": hd, "vertical": vd}
            if hd and vd:
                a_, b_ = max(hd), max(vd)
                entry["width_cm"], entry["length_cm"] = float(min(a_, b_)), float(max(a_, b_))
                entry["provenance"]["width_cm"] = "written_dimension"
            elif entry.get("mbr_cm"):
                entry["width_cm"], entry["length_cm"] = entry["mbr_cm"]
                entry["provenance"]["width_cm"] = "measured_geometry"
            # fixtures
            fx = [t for t, fx_x, fx_y in fixtures_px
                  if 0 <= int(fx_y) < Hpx and 0 <= int(fx_x) < Wpx and m[int(fx_y), int(fx_x)]]
            if fx:
                entry["fixtures_detected"] = fx
        else:
            entry["area_sqm"] = None
        if li.get("area_written"):
            entry["area_written_sqm"] = float(li["area_written"])
        if li.get("x") is not None:
            entry["label_pct"] = [round(li["x"] / Wpx * 100, 2), round(li["y"] / Hpx * 100, 2)]
        model_spaces.append(entry)
        s["entry"] = entry

    space_by_id = {e["id"]: e for e in model_spaces}

    def space_at_region(r, px=None, py=None):
        """Space id owning region r (if split, pick the one under the point)."""
        cands = region_to_space.get(int(r), []) if r else []
        if len(cands) == 1 or (cands and px is None):
            return cands[0]
        for s in spaces:
            if s["id"] in cands and s["mask"] is not None:
                yy, xx = int(np.clip(py, 0, Hpx - 1)), int(np.clip(px, 0, Wpx - 1))
                if s["mask"][yy, xx]:
                    return s["id"]
        return cands[0] if cands else None

    outdoor_spaces = [s for s in spaces if s["item"]["type"] in OUTDOOR_TYPES and s["mask"] is not None]

    # ---------------- openings → spaces ----------------
    model_openings = []
    north = (sheet_meta.get("north_arrow") or {})
    north_deg = north.get("north_direction_deg") if north.get("present") else None
    offset = max(3, int(round(15 / cm_per_px)))
    for k, o in enumerate(openings):
        if o["kind"] == "exterior_gap":
            continue
        x0, y0, x1, y1 = o["bbox_px"]
        cx, cy = o["center_px"]
        if o["axis"] == "horizontal":
            pa, pb = (cx, y0 - offset), (cx, y1 + offset)
        else:
            pa, pb = (x0 - offset, cy), (x1 + offset, cy)
        ra, rb = o["regions"]
        sa = space_at_region(ra, *pa) if ra else None
        sb = space_at_region(rb, *pb) if rb else None
        # exterior side may be a balcony footprint
        for side, (px_, py_) in (("a", pa), ("b", pb)):
            if (sa if side == "a" else sb) is None:
                for s in outdoor_spaces:
                    yy, xx = int(np.clip(py_, 0, Hpx - 1)), int(np.clip(px_, 0, Wpx - 1))
                    if s["mask"][max(0, yy - offset):yy + offset, max(0, xx - offset):xx + offset].any():
                        if side == "a":
                            sa = s["id"]
                        else:
                            sb = s["id"]
                        break
        mo = {"id": f"O{k + 1:02d}", "kind": o["kind"], "width_cm": o["width_cm"],
              "wall_thickness_cm": o["wall_thickness_cm"], "axis": o["axis"],
              "spaces": [sa, sb], "exterior_side": None,
              "center_pct": [round(cx / Wpx * 100, 2), round(cy / Hpx * 100, 2)],
              "spanning_lines": o["spanning_lines"], "door_leaf_cm": o["door_leaf_cm"]}
        if o["swing_region"]:
            mo["swing_into"] = space_at_region(o["swing_region"])
        extra = set()
        for x, y in o.get("links") or []:
            if len(region_to_space.get(int(x), [])) != 1 or len(region_to_space.get(int(y), [])) != 1:
                continue  # split open-plan region: side ownership is ambiguous
            sx, sy = space_at_region(x), space_at_region(y)
            if sx and sy and sx != sy and {sx, sy} != {sa, sb}:
                extra.add(tuple(sorted((sx, sy))))
        if extra:
            mo["extra_links"] = [list(p) for p in sorted(extra)]
        ext_a = (not ra) or info[ra]["exterior"]
        ext_b = (not rb) or info[rb]["exterior"]
        if ext_a != ext_b:
            mo["exterior_side"] = "a" if ext_a else "b"
            if north_deg is not None:
                if o["axis"] == "horizontal":
                    outward = 0.0 if mo["exterior_side"] == "a" else 180.0
                else:
                    outward = 270.0 if mo["exterior_side"] == "a" else 90.0
                mo["facing"] = _compass(outward - float(north_deg))
        model_openings.append(mo)

    # open-plan connections between parts split from the same region (no wall between them)
    groups = {}
    for s in spaces:
        if s.get("split_group") is not None:
            groups.setdefault(s["split_group"], []).append(s)
    k = len(model_openings)
    for parts in groups.values():
        for i in range(len(parts)):
            for j in range(i + 1, len(parts)):
                touch = ndi.binary_dilation(parts[i]["mask"], iterations=1) & parts[j]["mask"]
                n = int(touch.sum())
                if n < 3:
                    continue
                ys, xs = np.nonzero(touch)
                k += 1
                model_openings.append({
                    "id": f"O{k:02d}", "kind": "open_plan", "width_cm": round(n * cm_per_px, 1),
                    "wall_thickness_cm": 0.0, "axis": None, "spaces": [parts[i]["id"], parts[j]["id"]],
                    "exterior_side": None, "spanning_lines": 0, "door_leaf_cm": None,
                    "center_pct": [round(float(xs.mean()) / Wpx * 100, 2), round(float(ys.mean()) / Hpx * 100, 2)]})
    # ---------------- unlabeled zones: classify / merge ----------------
    def openings_of(sid):
        return [o for o in model_openings if sid in o["spaces"]]

    entrance = None
    unit_ids = {e["id"] for e in model_spaces if e["in_unit"] and e["type"] in INTERIOR_TYPES | {"corridor_candidate", "unknown"}}
    for o in model_openings:
        if o["kind"] != "door":
            continue
        a, b = o["spaces"]
        inside = [s for s in (a, b) if s in unit_ids]
        outside = [s for s in (a, b) if s not in unit_ids]
        if len(inside) == 1 and len(outside) == 1:
            other = outside[0]
            if other is not None and space_by_id.get(other, {}).get("type") in OUTDOOR_TYPES:
                continue
            if entrance is None or o["width_cm"] > entrance["width_cm"]:
                entrance = o
    for e in model_spaces:
        if e["type"] != "corridor_candidate":
            continue
        ops = openings_of(e["id"])
        doors = [o for o in ops if o["kind"] == "door"]
        plain = [o for o in ops if o["kind"] == "opening"]
        narrow = (e.get("inscribed_width_cm") or 999) <= 170
        if entrance and entrance["id"] in [o["id"] for o in ops]:
            e["type"] = "entrance" if (e["area_sqm"] or 0) < 6 else "corridor"
            e["provenance"]["type"] = "contains_entrance_door"
        elif len(doors) >= 2 or narrow:
            e["type"] = "corridor"
            e["provenance"]["type"] = "circulation_geometry"
        elif (e["area_sqm"] or 0) < 3 and len(doors) == 1 and not plain:
            e["type"] = "storage"
            e["provenance"]["type"] = "small_closed_room"
        else:
            e["type"] = "corridor"
            e["provenance"]["type"] = "unlabeled_default"
        e["name"] = {"corridor": "מסדרון / מעבר", "entrance": "מבואת כניסה", "storage": "מחסן / ארון"}[e["type"]]
        e["name_inferred"] = True

    # ---------------- topology ----------------
    exit_marks = [nbox_center_px(a["box"]) for a in reading.get("annotations", [])
                  if any(k in str(a.get("text", "")) for k in ("יציאה", "למרפסת", "כניסה למרפסת"))]
    near_px = 160 / cm_per_px

    def near_exit_mark(o):
        cx, cy = o["center_pct"][0] / 100 * Wpx, o["center_pct"][1] / 100 * Hpx
        return any(math.dist((cx, cy), p) <= near_px for p in exit_marks)

    topology = []
    for o in model_openings:
        a, b = o["spaces"]
        if not (a and b) or a == b:
            continue
        ea, eb = space_by_id.get(a), space_by_id.get(b)
        if not (ea and eb and ea["in_unit"] and eb["in_unit"]):
            continue
        outdoor_pair = (ea["type"] in OUTDOOR_TYPES) != (eb["type"] in OUTDOOR_TYPES)
        if outdoor_pair:
            access = o["kind"] == "door" or (o["kind"] == "exterior_opening" and o["width_cm"] >= 60) or \
                (o["kind"] == "window" and (o["width_cm"] >= 180 or near_exit_mark(o)))
            if access:
                o["balcony_access"] = True
                topology.append({"source": a, "target": b, "type": "door", "width_cm": o["width_cm"],
                                 "opening": o["id"], "via": "glazed_door" if o["kind"] == "window" else o["kind"]})
            elif o["kind"] == "window":
                o["faces_outdoor_space"] = True
        elif o["kind"] in ("door", "opening", "open_plan"):
            topology.append({"source": a, "target": b, "type": "door" if o["kind"] == "door" else "opening",
                             "width_cm": o["width_cm"], "opening": o["id"]})
    for o in model_openings:
        if o["kind"] not in ("door", "opening"):
            continue
        for x, y in o.get("extra_links", []):
            ex_, ey_ = space_by_id.get(x), space_by_id.get(y)
            if ex_ and ey_ and ex_["in_unit"] and ey_["in_unit"] and \
                    (ex_["type"] in OUTDOOR_TYPES) == (ey_["type"] in OUTDOOR_TYPES):
                topology.append({"source": x, "target": y, "type": "opening", "width_cm": o["width_cm"],
                                 "opening": o["id"], "via": "shared_passage"})
    if entrance:
        entrance["is_entrance"] = True
        inside = [s for s in entrance["spaces"] if s in unit_ids][0]
        topology.append({"source": "EXT", "target": inside, "type": "door", "width_cm": entrance["width_cm"],
                         "opening": entrance["id"]})

    # ---------------- windows, depth, orientation per space ----------------
    for e in model_spaces:
        ops = openings_of(e["id"])
        wins = [o for o in ops if o["kind"] in ("window", "exterior_opening") and not o.get("balcony_access")
                or (o.get("balcony_access") and e["type"] not in OUTDOOR_TYPES)]
        wins = [o for o in wins if o["exterior_side"] is not None]
        e["windows"] = [o["id"] for o in wins]
        e["doors"] = [o["id"] for o in ops if o["kind"] == "door"]
        e["has_window"] = bool(wins) if e["type"] not in OUTDOOR_TYPES else None
        if wins and e["type"] not in OUTDOOR_TYPES:
            area = 0.0
            for o in wins:
                full = o.get("balcony_access") or o["width_cm"] >= 200
                h = DEFAULTS["door_h_m"] if full else DEFAULTS["win_lintel_m"] - DEFAULTS["win_sill_m"]
                area += o["width_cm"] / 100.0 * h
            e["window_area_sqm_est"] = round(area, 2)
            e["provenance"]["window_area_sqm_est"] = "opening_width × default glazing height (בקת/ק.ע.) — estimate"
            facing = sorted({o["facing"] for o in wins if o.get("facing")})
            if facing:
                e["orientation"] = facing
        doors = [o for o in ops if o["kind"] == "door"]
        if doors:
            e["door_width_cm"] = min(o["width_cm"] for o in doors)
            e["provenance"]["door_width_cm"] = "measured_opening"
        # room depth from the main window wall
        sp = next((s for s in spaces if s["id"] == e["id"]), None)
        if wins and sp is not None and sp["mask"] is not None and e["type"] in HABITABLE_TYPES:
            o = max(wins, key=lambda o: o["width_cm"])
            cx = o["center_pct"][0] / 100 * Wpx
            cy = o["center_pct"][1] / 100 * Hpx
            m = sp["mask"]
            if o["axis"] == "horizontal":
                col = m[:, int(np.clip(cx, 0, Wpx - 1))]
                depth_px = col.sum()
            else:
                row = m[int(np.clip(cy, 0, Hpx - 1)), :]
                depth_px = row.sum()
            e["depth_m"] = round(depth_px * cm_per_px / 100.0, 2)
            e["provenance"]["depth_m"] = "measured_perpendicular_to_main_window"

    # outdoor spaces: area/depth preferring written values
    for e in model_spaces:
        if e["type"] not in OUTDOOR_TYPES:
            continue
        if e.get("area_written_sqm"):
            e["area_measured_sqm"] = e.get("area_sqm")
            e["area_sqm"] = e["area_written_sqm"]
            e["provenance"]["area_sqm"] = "written_on_plan"
        wd = e.get("written_dimensions_cm") or {}
        hv = [max(v) for v in (wd.get("horizontal"), wd.get("vertical")) if v]
        if hv:
            e["depth_m"] = round(min(hv) / 100.0, 2)
            e["provenance"]["depth_m"] = "written_dimension (shorter side)"
        if "depth_m" not in e and e.get("mbr_cm"):
            e["depth_m"] = round(e["mbr_cm"][0] / 100.0, 2)
            e["provenance"]["depth_m"] = "measured_min_rect"

    # ממ"ד wall thickness (skill: topological & clash check — ממ"ד walls ≥ 20–25 cm)
    walls = geo["walls"]
    for s in spaces:
        e = s["entry"]
        if e["type"] != "safe_room" or s["mask"] is None:
            continue
        m = s["mask"]
        sl = ndi.find_objects(m.astype(np.int32))[0]
        y0, y1, x0, x1 = sl[0].start, sl[0].stop - 1, sl[1].start, sl[1].stop - 1
        maxr = int(round(80 / cm_per_px))
        sides = {}
        for side in ("top", "bottom", "left", "right"):
            vals = []
            for f in (0.25, 0.5, 0.75):
                if side in ("top", "bottom"):
                    x = int(x0 + f * (x1 - x0))
                    y = y0 - 1 if side == "top" else y1 + 1
                    step = (0, -1) if side == "top" else (0, 1)
                else:
                    y = int(y0 + f * (y1 - y0))
                    x = x0 - 1 if side == "left" else x1 + 1
                    step = (-1, 0) if side == "left" else (1, 0)
                n = 0
                while 0 <= y < Hpx and 0 <= x < Wpx and walls[y, x] and n < maxr:
                    n += 1
                    x += step[0]
                    y += step[1]
                if n:
                    vals.append(n)
            if vals:
                sides[side] = round(float(np.median(vals)) * cm_per_px, 1)
        ops = openings_of(e["id"])
        e["mamad"] = {
            "wall_thickness_cm": sides,
            "min_wall_thickness_cm": min(sides.values()) if sides else None,
            "has_door": any(o["kind"] == "door" for o in ops),
            "has_window": any(o["kind"] in ("window", "exterior_opening") for o in ops),
        }

    # ---------------- apartment summary ----------------
    unit = [e for e in model_spaces if e["in_unit"] and e["area_sqm"] is not None]
    interior = [e for e in unit if e["type"] in INTERIOR_TYPES]
    outdoor = [e for e in unit if e["type"] in OUTDOOR_TYPES]
    orient = sorted({d for e in unit if e["type"] in HABITABLE_TYPES | OUTDOOR_TYPES for d in e.get("orientation", [])})
    apartment = {
        "net_interior_area_sqm": round(sum(e["area_sqm"] for e in interior), 2),
        "outdoor_area_sqm": round(sum(e["area_sqm"] for e in outdoor), 2),
        "declared_area_sqm": sheet_meta.get("apartment_area_sqm"),
        "declared_rooms": sheet_meta.get("rooms_count"),
        "rooms_count_measured": sum(1 for e in interior if e["type"] in ROOM_COUNT_TYPES),
        "bedrooms": sum(1 for e in interior if e["type"] in ("bedroom", "safe_room")),
        "bathrooms": sum(1 for e in interior if e["type"] == "bathroom"),
        "toilets": sum(1 for e in interior if e["type"] == "toilet"),
        "orientations": orient,
        "entrance_space_id": next((t["target"] for t in topology if t["source"] == "EXT"), None),
        "main_entrance_width_cm": entrance["width_cm"] if entrance else None,
        "instances": {"floors": sheet_meta.get("floors") or [], "floors_text": sheet_meta.get("floors_text"),
                      "apartments": [str(a) for a in (sheet_meta.get("apartment_numbers") or [])]},
    }

    wall_px = geo["walls"].sum()
    sheet = {
        "page": pno + 1,
        "preview_image": preview_name,
        "image_size_px": [Wpx, Hpx],
        "sheet": {k: sheet_meta.get(k) for k in ("project_name", "city", "plan_type", "sheet_kind", "floors_text",
                                                  "floors", "apartment_numbers", "rooms_count", "apartment_area_sqm",
                                                  "scale", "date", "sheet_number")},
        "reading_source": reading.get("source"),
        "has_text_layer": has_text,
        "calibration": dict(calib, scale=f"1:{scale:g}", scale_source=scale_source,
                            cm_per_pt=round(cm_per_pt, 5), render_zoom=round(zoom, 3), cm_per_px=round(cm_per_px, 4)),
        "north": {"present": bool(north.get("present")), "north_direction_deg": north_deg},
        "walls_summary": {"wall_footprint_sqm": round(float(wall_px * px_area), 2),
                          "door_arcs_detected": len(geo["arcs"])},
        "spaces": model_spaces,
        "openings": model_openings,
        "topology": topology,
        "apartment": apartment,
        "dimensions": [{"value_cm": d["value_cm"], "orientation": d["orientation"],
                        "space": space_at_region(d["region"], (d["span"][0] + d["span"][2]) / 2,
                                                 (d["span"][1] + d["span"][3]) / 2) if d["region"] else None}
                       for d in dims_px],
        "unmatched_dimensions": [d["value_cm"] for d in reading["dimensions"]
                                 if not any(m["box"] == d["box"] for m in matches)],
        "labels_outside_unit": [li["name"] for li in label_items if not li["in_unit"]],
        "unmapped_labels": [li["name"] for li in label_items if not li["region"]],
        "annotations": reading.get("annotations", []),
        "notes": reading.get("notes", []),
        "warnings": warnings,
    }
    sheet["qa"] = QA.run_checks(sheet)
    return sheet
