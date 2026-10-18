"""
Stage 3 — deterministic plan geometry (0 LLM tokens).

Adapted from the `arch-2d-to-3d-bim` skill (step 1 vector pre-processing + step 3
compact model), stopping before 3D extrusion: we only build the 2D data the
analysis engine needs — walls, openings, enclosed spaces and their adjacency.

Approach (raster over the *rendered* page, so CAD wipeouts that hide neighbouring
units are respected):
  1. Wall mask       – gray poché fill of cut walls (+ its dark outline).
  2. Opening bridges – gaps inside a wall band whose two jambs are wall ends
                       (doors, windows, passages); closed to separate spaces.
  3. Spaces          – connected components of free space; border-touching
                       components are exterior.
  4. Door arcs       – quarter-circle Béziers from the vector layer classify
                       bridges as doors and give the swing side.
All lengths are converted to centimetres through `cm_per_px`.
"""
import math
import numpy as np
from scipy import ndimage as ndi

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover
    fitz = None

# ---------------------------------------------------------------------------
# Tunables (centimetres unless stated). Kept in one place for calibration.
# ---------------------------------------------------------------------------
WALL_MIN_THICKNESS_CM = 6.0       # thinner gray strokes are not walls
WALL_MAX_THICKNESS_CM = 55.0      # thicker bands are not a single wall
OPENING_MAX_CM = 460.0            # widest gap closed as an opening (sliding doors ≈ 4 m)
OPENING_MIN_CM = 2.0
VIRTUAL_WALL_MAX_CM = 300.0       # wall end → side of another wall (open-plan closure)
DOOR_RADIUS_RANGE_CM = (50.0, 125.0)
MIN_PASSAGE_CM = 45.0             # narrower gaps (no door arc) are drawing gaps, not openings
MIN_SPACE_AREA_M2 = 0.6           # smaller enclosed regions are ignored
EXTERIOR_AREA_M2 = 400.0          # regions larger than this are exterior


def render_page(page, zoom):
    """Render a PyMuPDF page to an RGB uint8 array."""
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    return np.ascontiguousarray(arr[:, :, :3])


def _drop_small(mask, min_px):
    lab, n = ndi.label(mask)
    if n == 0:
        return mask
    sizes = ndi.sum(mask, lab, index=np.arange(1, n + 1))
    keep = np.zeros(n + 1, dtype=bool)
    keep[1:] = sizes >= min_px
    return keep[lab]


def wall_mask(img, cm_per_px, plan_bbox=None):
    """Binary mask of cut walls (gray poché + outline)."""
    g = img.astype(np.int16).mean(axis=2)
    sat = img.max(axis=2).astype(np.int16) - img.min(axis=2)
    fill = (g >= 195) & (g <= 238) & (sat < 18)
    k = max(1, int(round(WALL_MIN_THICKNESS_CM / cm_per_px / 2.0)))
    fill = ndi.binary_opening(fill, structure=np.ones((3, 3), bool), iterations=k)
    dark = g < 120
    walls = fill | (dark & ndi.binary_dilation(fill, iterations=3))
    walls = ndi.binary_closing(walls, iterations=1)
    walls = _drop_small(walls, (12.0 / cm_per_px) ** 2)
    if plan_bbox is not None:
        x0, y0, x1, y1 = plan_bbox
        clip = np.zeros_like(walls)
        clip[y0:y1, x0:x1] = True
        walls &= clip
    return walls


def run_length(mask, axis):
    """Per-pixel length of the run of True values containing it along `axis`."""
    m = np.moveaxis(mask, axis, 0).astype(np.int32)
    fwd = np.zeros_like(m)
    bwd = np.zeros_like(m)
    fwd[0] = m[0]
    for i in range(1, m.shape[0]):
        fwd[i] = (fwd[i - 1] + 1) * m[i]
    bwd[-1] = m[-1]
    for i in range(m.shape[0] - 2, -1, -1):
        bwd[i] = (bwd[i + 1] + 1) * m[i]
    rl = (fwd + bwd - 1) * m
    return np.moveaxis(rl, 0, axis)


def _row_bridges(walls, perp_run, along_run, max_gap, max_t_gap, min_gap, max_t):
    """Candidate opening pixels along rows.

    Each jamb is typed:
      wall end – thin across (perp ≤ max_t) and the wall continues *along* the row
                 at least ~its own thickness (it faces the gap);
      flank    – the side of a perpendicular wall (perp > max_t);
      stub     – anything else (small piece not facing the gap) → never bridged.
    Accepted: end↔end up to `max_gap`; end↔flank (virtual wall closing an
    open-plan zone) up to `max_t_gap`.
    """
    H, _ = walls.shape
    cand = np.zeros_like(walls)
    jamb = np.zeros(walls.shape, dtype=np.int32)
    w8 = walls.astype(np.int8)

    def jtype(perp, along):
        if perp > max_t:
            return "flank"
        return "end" if along >= 0.8 * perp else "stub"

    for y in range(H):
        d = np.diff(w8[y])
        ends = np.flatnonzero(d == -1)
        if ends.size == 0:
            continue
        starts = np.flatnonzero(d == 1) + 1
        if starts.size == 0:
            continue
        j = np.searchsorted(starts, ends)
        ok = j < starts.size
        for e, s in zip(ends[ok], starts[j[ok]]):
            gap = s - e - 1
            if gap < min_gap or gap > max_gap:
                continue
            # perpendicular thickness measured a few px *into* each jamb (robust to outline noise)
            a = int(np.median(perp_run[y, max(0, e - 3):e + 1]))
            b = int(np.median(perp_run[y, s:s + 4]))
            ta, tb = jtype(a, along_run[y, e]), jtype(b, along_run[y, s])
            if ta == "end" and tb == "end":
                t = min(a, b)
            elif {ta, tb} == {"end", "flank"} and gap <= max_t_gap:
                t = a if ta == "end" else b
            else:
                continue
            cand[y, e + 1:s] = True
            jamb[y, e + 1:s] = t
    return cand, jamb


def _count_spanning_lines(dark_band, rows, min_cover=0.85):
    """Number of distinct dark lines running along the gap (rows of `dark_band`,
    coverage measured over the bridge pixels `rows` only)."""
    if dark_band.size == 0 or dark_band.shape[1] == 0:
        return 0
    n = rows.sum(axis=1)
    cover = ((dark_band & rows).sum(axis=1) >= np.maximum(1, n * min_cover)) & (n > 0)
    # count runs of consecutive covered rows (a 2-px thick line is one line)
    return int(np.count_nonzero(np.diff(np.concatenate([[0], cover.astype(np.int8)])) == 1))


def _filter_bridges(cand, jamb, dark, max_t, along_axis):
    """Keep bridge components whose thickness matches the wall band of their jambs."""
    lab, n = ndi.label(cand)
    out = []
    keep = np.zeros_like(cand)
    for i, sl in enumerate(ndi.find_objects(lab), start=1):
        if sl is None:
            continue
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        thick = h if along_axis == 1 else w
        if thick > max_t * 1.15 or thick < 2:
            continue
        comp = lab[sl] == i
        jr = float(np.median(jamb[sl][comp]))
        # a real opening is about as thick as the wall it interrupts; a thin strip
        # between two thick walls is a false bridge across a room
        if thick < 0.6 * jr - 1 or thick > 2.0 * jr + 4:
            continue
        keep[sl] |= comp
        rows = comp if along_axis == 1 else comp.T
        runs = rows.sum(axis=1)
        runs = runs[runs > 0]
        length = int(np.median(runs)) if runs.size else 0
        band = dark[sl] if along_axis == 1 else dark[sl].T
        out.append({"slice": sl, "axis": along_axis, "length_px": length, "thick_px": thick,
                    "spanning_lines": _count_spanning_lines(band, rows)})
    return keep, out


def find_openings(walls, cm_per_px, dark=None):
    """Bridge gaps in wall bands. `dark` (bool mask of drawn strokes) is used to
    count glazing / partition lines running along each gap."""
    if dark is None:
        dark = np.zeros_like(walls)
    max_t = int(round(WALL_MAX_THICKNESS_CM / cm_per_px))
    max_gap = int(round(OPENING_MAX_CM / cm_per_px))
    max_t_gap = int(round(VIRTUAL_WALL_MAX_CM / cm_per_px))
    min_gap = max(1, int(round(OPENING_MIN_CM / cm_per_px)))
    vrun = run_length(walls, axis=0)
    hrun = run_length(walls, axis=1)
    # bridges in horizontal walls run along rows (axis=1)
    cand_h, jamb_h = _row_bridges(walls, vrun, hrun, max_gap, max_t_gap, min_gap, max_t)
    keep_h, br_h = _filter_bridges(cand_h, jamb_h, dark, max_t, along_axis=1)
    # bridges in vertical walls run along columns (axis=0)
    cand_v, jamb_v = _row_bridges(walls.T, hrun.T, vrun.T, max_gap, max_t_gap, min_gap, max_t)
    keep_v, br_v = _filter_bridges(cand_v.T, jamb_v.T, dark, max_t, along_axis=0)
    return keep_h | keep_v, br_h + br_v


def dark_mask(img, page=None, zoom=None):
    """Drawn strokes (black / near-black), excluding mid-gray hatching (floor tiles, decks).

    With `page`, strokes come from the vector layer (only dark-coloured paths), drawn
    at >=1 px so thin glazing lines survive, and intersected with the render so lines
    hidden under CAD wipeouts are ignored. Without it, a raster threshold is used."""
    g = img.astype(np.int16).mean(axis=2)
    if page is None:
        return g < 105
    from PIL import Image, ImageDraw
    H, W = g.shape
    canvas = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(canvas)
    for dr in page.get_drawings():
        col = dr.get("color")
        if col is None or max(col) > 0.35:
            continue
        w = max(1, int(round((dr.get("width") or 0.5) * zoom)))
        for it in dr.get("items", []):
            kind = it[0]
            if kind == "l":
                d.line([(it[1].x * zoom, it[1].y * zoom), (it[2].x * zoom, it[2].y * zoom)], fill=255, width=w)
            elif kind == "re":
                r = it[1]
                d.rectangle([r.x0 * zoom, r.y0 * zoom, r.x1 * zoom, r.y1 * zoom], outline=255, width=w)
            elif kind == "qu":
                q = it[1]
                pts = [(q.ul.x * zoom, q.ul.y * zoom), (q.ur.x * zoom, q.ur.y * zoom),
                       (q.lr.x * zoom, q.lr.y * zoom), (q.ll.x * zoom, q.ll.y * zoom)]
                d.line(pts + [pts[0]], fill=255, width=w)
            elif kind == "c":
                p0, p1, p2, p3 = it[1:5]
                pts = []
                for t in np.linspace(0, 1, 9):
                    mt = 1 - t
                    x = mt ** 3 * p0.x + 3 * mt * mt * t * p1.x + 3 * mt * t * t * p2.x + t ** 3 * p3.x
                    y = mt ** 3 * p0.y + 3 * mt * mt * t * p1.y + 3 * mt * t * t * p2.y + t ** 3 * p3.y
                    pts.append((x * zoom, y * zoom))
                d.line(pts, fill=255, width=w)
    vec = np.asarray(canvas) > 0
    return vec & (g < 215)


def segment_spaces(barrier, cm_per_px):
    """Label free space; returns (labels, info dict per label)."""
    free = ~barrier
    lab, n = ndi.label(free)  # 4-connectivity
    H, W = lab.shape
    border = np.unique(np.concatenate([lab[0, :], lab[-1, :], lab[:, 0], lab[:, -1]]))
    areas = ndi.sum(free, lab, index=np.arange(1, n + 1)) * (cm_per_px ** 2) / 1e4
    info = {}
    for i in range(1, n + 1):
        a = float(areas[i - 1])
        info[i] = {
            "area_m2": a,
            "exterior": bool(i in border or a >= EXTERIOR_AREA_M2),
            "tiny": a < MIN_SPACE_AREA_M2,
        }
    return lab, info


# ---------------------------------------------------------------------------
# Door arcs from the vector layer
# ---------------------------------------------------------------------------
def _arc_center(p1, c1, c2, p2):
    """Circle centre of a Bézier arc: intersection of the normals at both ends."""
    t1 = (c1[0] - p1[0], c1[1] - p1[1])
    t2 = (p2[0] - c2[0], p2[1] - c2[1])
    n1 = (-t1[1], t1[0])
    n2 = (-t2[1], t2[0])
    den = n1[0] * n2[1] - n1[1] * n2[0]
    if abs(den) < 1e-9:
        return None
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    s = (dx * n2[1] - dy * n2[0]) / den
    return (p1[0] + s * n1[0], p1[1] + s * n1[1])


def _fit_circle(pts):
    """Algebraic (Kåsa) least-squares circle fit → (cx, cy, r, rms)."""
    a = np.asarray(pts, dtype=float)
    A = np.column_stack([2 * a[:, 0], 2 * a[:, 1], np.ones(len(a))])
    b = (a ** 2).sum(axis=1)
    sol, *_ = np.linalg.lstsq(A, b, rcond=None)
    cx, cy, c = sol
    r = math.sqrt(max(c + cx * cx + cy * cy, 0.0))
    rms = float(np.sqrt(np.mean((np.hypot(a[:, 0] - cx, a[:, 1] - cy) - r) ** 2)))
    return cx, cy, r, rms


def _polyline_arc_pieces(d, zoom, rmin_px, rmax_px):
    """Arc pieces from chains of short connected line segments inside one path."""
    chains, cur = [], []
    for it in d.get("items", []):
        if it[0] != "l":
            if len(cur) >= 2:
                chains.append(cur)
            cur = []
            continue
        p1 = (it[1].x * zoom, it[1].y * zoom)
        p2 = (it[2].x * zoom, it[2].y * zoom)
        if cur and math.dist(cur[-1], p1) < 0.75:
            cur.append(p2)
        else:
            if len(cur) >= 2:
                chains.append(cur)
            cur = [p1, p2]
    if len(cur) >= 2:
        chains.append(cur)
    pieces = []
    for ch in chains:
        if len(ch) < 6:
            continue
        seg = [math.dist(ch[i], ch[i + 1]) for i in range(len(ch) - 1)]
        if max(seg) > 0.35 * rmax_px:
            continue
        cx, cy, r, rms = _fit_circle(ch)
        if not (rmin_px <= r <= rmax_px) or rms > 0.04 * r:
            continue
        angs = [math.atan2(p[1] - cy, p[0] - cx) for p in ch]
        sweep = sum(abs((math.degrees(angs[i + 1] - angs[i]) + 180) % 360 - 180) for i in range(len(angs) - 1))
        pieces.append({"center": (cx, cy), "r": r, "ends": [ch[0], ch[-1]], "sweep": sweep})
    return pieces


def door_arcs(page, zoom, cm_per_px):
    """Door-swing arcs (≈60°–200° total sweep, door-leaf radius) in pixel coords.
    Arcs split into several Bézier pieces are grouped by centre and radius;
    swings drawn as polylines are recovered by circle fitting."""
    rmin, rmax = DOOR_RADIUS_RANGE_CM
    pieces = []
    for d in page.get_drawings():
        pieces.extend(_polyline_arc_pieces(d, zoom, rmin / cm_per_px, rmax / cm_per_px))
        for it in d.get("items", []):
            if it[0] != "c":
                continue
            p1, c1, c2, p2 = [(pt.x * zoom, pt.y * zoom) for pt in it[1:5]]
            c = _arc_center(p1, c1, c2, p2)
            if c is None:
                continue
            r1, r2 = math.dist(c, p1), math.dist(c, p2)
            if r1 <= 0 or abs(r1 - r2) / r1 > 0.08:
                continue
            if not (rmin <= r1 * cm_per_px <= rmax):
                continue
            a1 = math.atan2(p1[1] - c[1], p1[0] - c[0])
            a2 = math.atan2(p2[1] - c[1], p2[0] - c[0])
            sweep = abs((math.degrees(a2 - a1) + 180) % 360 - 180)
            if sweep < 8:
                continue
            pieces.append({"center": c, "r": (r1 + r2) / 2, "ends": [p1, p2], "sweep": sweep})
    groups = []
    for p in pieces:
        for g in groups:
            if math.dist(p["center"], g["center"]) < 4 and abs(p["r"] - g["r"]) < 4:
                if not any(math.dist(e, f) < 1.0 for e in p["ends"] for f in g["ends_all"]) or \
                        len(g["ends_all"]) < 2 or p["sweep"] + g["sweep"] < 200:
                    # skip exact duplicates (same ends) — CAD often draws arcs twice
                    if all(math.dist(p["ends"][0], q[0]) > 1 or math.dist(p["ends"][1], q[1]) > 1
                           for q in g["pairs"]):
                        g["sweep"] += p["sweep"]
                        g["pairs"].append(p["ends"])
                        g["ends_all"].extend(p["ends"])
                break
        else:
            groups.append({"center": p["center"], "r": p["r"], "sweep": p["sweep"],
                           "pairs": [p["ends"]], "ends_all": list(p["ends"])})
    arcs = []
    for g in groups:
        if not (55 <= g["sweep"] <= 200):
            continue
        # the two outermost ends of the chain
        ends = g["ends_all"]
        p1, p2 = max(((a, b) for a in ends for b in ends), key=lambda ab: math.dist(*ab))
        arcs.append({"center": g["center"], "p1": p1, "p2": p2, "radius_px": g["r"],
                     "radius_cm": g["r"] * cm_per_px, "sweep_deg": round(g["sweep"], 1)})
    return arcs


def _side_regions(lab, br, offset, max_march, with_all=False):
    """Majority region id on each side of a bridge component; marches outward
    (up to `max_march` px) past any wall that backs the bridge. With `with_all`,
    also returns, per side, every region covering ≥ 20 % of that side."""
    sl = br["slice"]
    H, W = lab.shape
    out, allsets = [], []
    for sign in (-1, 1):
        found, sig = 0, []
        for off in range(offset, max_march + 1, 2):
            if br["axis"] == 1:  # horizontal wall → look above / below
                y = sl[0].start - off if sign < 0 else sl[0].stop - 1 + off
                s = lab[y, sl[1].start:sl[1].stop] if 0 <= y < H else None
            else:
                x = sl[1].start - off if sign < 0 else sl[1].stop - 1 + off
                s = lab[sl[0].start:sl[0].stop, x] if 0 <= x < W else None
            if s is None:
                break
            nz = s[s > 0]
            if nz.size >= 0.5 * s.size:
                cnt = np.bincount(nz)
                found = int(cnt.argmax())
                sig = [int(r) for r in np.flatnonzero(cnt >= 0.2 * s.size)]
                break
        out.append(found)
        allsets.append(sig or ([found] if found else []))
    return (out, allsets) if with_all else out


def classify_openings(lab, info, bridges, arcs, cm_per_px):
    """Attach region ids on both sides, type and width (cm) to every bridge.

    kind:
      door          – a swing arc is hinged on the gap
      window        – ≥2 glazing lines along the gap, exterior on one side
      partition     – ≥2 lines along the gap, interior both sides (unfilled drywall) → no passage
      opening       – empty gap between two interior spaces (passage)
      exterior_opening – empty gap to the exterior (balcony access, loggia…)
      exterior_gap  – both sides exterior (drawing artefact, ignored)
      wall_gap      – < MIN_PASSAGE_CM without a door arc (gap in the wall drawing, closed)
    """
    offset = max(2, int(round(6 / cm_per_px)))
    max_march = int(round(WALL_MAX_THICKNESS_CM / cm_per_px)) + offset
    openings = []
    for br in bridges:
        sl = br["slice"]
        (a, b), (sa_all, sb_all) = _side_regions(lab, br, offset, max_march, with_all=True)
        cx = (sl[1].start + sl[1].stop) / 2.0
        cy = (sl[0].start + sl[0].stop) / 2.0
        width_cm = br["length_px"] * cm_per_px
        swing_side = None
        door = None
        best = None
        for arc in arcs:
            dist = math.dist(arc["center"], (cx, cy))
            if dist <= arc["radius_px"] * 0.9 + br["thick_px"] and \
                    abs(arc["radius_px"] - br["length_px"]) <= max(0.35 * br["length_px"], 8):
                if best is None or dist < best:
                    door, best = arc, dist
        ext_a = info.get(a, {}).get("exterior", True) if a else True
        ext_b = info.get(b, {}).get("exterior", True) if b else True
        lines = br.get("spanning_lines", 0)
        if door is not None:
            kind = "door"
            mid = ((door["p1"][0] + door["p2"][0]) / 2.0, (door["p1"][1] + door["p2"][1]) / 2.0)
            # point between hinge and chord midpoint lies inside the swing
            px = int(round((mid[0] + door["center"][0]) / 2.0))
            py = int(round((mid[1] + door["center"][1]) / 2.0))
            if 0 <= py < lab.shape[0] and 0 <= px < lab.shape[1]:
                swing_side = int(lab[py, px]) or None
        elif ext_a and ext_b:
            kind = "exterior_gap"
        elif width_cm < MIN_PASSAGE_CM:
            kind = "wall_gap"
        elif ext_a != ext_b:
            kind = "window" if lines >= 2 else "exterior_opening"
        else:
            kind = "partition" if lines >= 2 else "opening"
        openings.append({
            "kind": kind,
            "regions": [a, b],
            "links": [[x, y] for x in sa_all for y in sb_all if x != y],
            "width_cm": round(width_cm, 1),
            "wall_thickness_cm": round(br["thick_px"] * cm_per_px, 1),
            "axis": "horizontal" if br["axis"] == 1 else "vertical",
            "spanning_lines": lines,
            "center_px": [round(cx, 1), round(cy, 1)],
            "bbox_px": [int(sl[1].start), int(sl[0].start), int(sl[1].stop), int(sl[0].stop)],
            "swing_region": swing_side,
            "door_leaf_cm": round(door["radius_cm"], 1) if door else None,
        })
    return openings
