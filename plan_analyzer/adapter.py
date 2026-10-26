"""
Stage 5 — adapter from the Plan Data Model to the apartment/project JSON that
validation_engine.run_validation() and the web UI consume.

Only fields backed by extracted data are emitted (zero-trust): e.g. no ceiling
height is invented for a sales plan, ventilation is left unknown for windowless
bathrooms, and the main-entrance width is emitted only if the door was found.
"""
from .taxonomy import OUTDOOR_TYPES

# plan-model type → engine vocabulary (legacy B1.x checks + v2 _norm_type)
ENGINE_TYPE = {
    "living": "living_room", "dining": "dining", "kitchen": "kitchen", "bedroom": "bedroom",
    "safe_room": "safe_room", "study": "study", "bathroom": "bathroom", "toilet": "toilet",
    "utility": "utility", "storage": "storage", "walk_in_closet": "storage", "corridor": "corridor",
    "entrance": "entrance", "balcony": "balcony", "service_balcony": "service_balcony", "garden": "garden",
    "unknown": "space",
}


def _apartment_title(sheet):
    nums = (sheet.get("sheet") or {}).get("apartment_numbers") or []
    if len(nums) == 1:
        return f"דירה {nums[0]}"
    if nums:
        return "דירות " + ", ".join(str(n) for n in nums)
    return f"דירה (עמוד {sheet.get('page')})"


def to_engine_apartment(sheet):
    """One plan sheet → one apartment dict for validation_engine."""
    rooms = []
    for s in sheet.get("spaces", []):
        if not s.get("in_unit") or s.get("type") not in ENGINE_TYPE:
            continue
        if s.get("area_sqm") is None:
            continue
        r = {
            "id": s["id"],
            "type": ENGINE_TYPE[s["type"]],
            "name": s.get("name") or s["id"],
            "area_sqm": s["area_sqm"],
        }
        for k in ("width_cm", "length_cm", "depth_m", "door_width_cm"):
            if s.get(k) is not None:
                r[k] = s[k]
        if s.get("polygon_cm"):
            r["polygon"] = s["polygon_cm"]
        if s["type"] not in OUTDOOR_TYPES and s.get("has_window") is not None:
            r["has_window"] = bool(s["has_window"])
        if s.get("window_area_sqm_est") is not None:
            r["window_area_sqm"] = s["window_area_sqm_est"]
        pos = s.get("label_pct") or s.get("centroid_pct")
        if pos:
            r["x_pct"], r["y_pct"] = pos
        if s.get("polygon_cm"):
            r["polygon_pct"] = None  # filled by to_project (needs page size)
        r["source"] = {"method": s.get("method"), "confidence": s.get("confidence"),
                       "provenance": s.get("provenance", {})}
        if s.get("fixtures_detected"):
            r["fixtures_detected"] = s["fixtures_detected"]
        if s.get("orientation"):
            r["orientation"] = s["orientation"]
        rooms.append(r)

    ids = {r["id"] for r in rooms}
    topology = [{k: v for k, v in e.items() if k in ("source", "target", "type", "width_cm")}
                for e in sheet.get("topology", [])
                if (e["source"] in ids or e["source"] == "EXT") and e["target"] in ids]
    apt = sheet.get("apartment", {})
    out = {
        "apartment_id": _apartment_title(sheet),
        "global_parameters": {},
        "accessibility": {},
        "rooms": rooms,
        "topology": topology,
    }
    if apt.get("main_entrance_width_cm"):
        out["accessibility"]["main_entrance_width_cm"] = apt["main_entrance_width_cm"]
    if apt.get("entrance_space_id") in ids:
        out["entrance_room_id"] = apt["entrance_space_id"]
    if apt.get("orientations"):
        out["orientations"] = apt["orientations"]
    if apt.get("declared_area_sqm"):
        out["declared_area_sqm"] = apt["declared_area_sqm"]
    inst = apt.get("instances") or {}
    if inst.get("apartments") or inst.get("floors"):
        out["instances"] = inst
    return out


def _pct_polygon(poly_cm, sheet):
    cal = sheet.get("calibration", {})
    W, H = sheet.get("image_size_px", [0, 0])
    cpp = cal.get("cm_per_px")
    if not poly_cm or not W or not cpp:
        return None
    return [[round(x / cpp / W * 100, 2), round(y / cpp / H * 100, 2)] for x, y in poly_cm]


def to_project(model, preview_url_prefix="/uploads/"):
    """Plan model → project JSON (floors → apartments) used by server.py / UI."""
    floors = []
    for sheet in model.get("sheets", []):
        apt = to_engine_apartment(sheet)
        for r in apt["rooms"]:
            if "polygon_pct" in r:
                r["polygon_pct"] = _pct_polygon(r.get("polygon"), sheet)
        meta = sheet.get("sheet") or {}
        floor_name = meta.get("floors_text") or (f"קומה {meta['floors'][0]}" if meta.get("floors") else f"עמוד {sheet['page']}")
        apt["plan_extraction"] = {
            "page": sheet["page"],
            "preview_image": preview_url_prefix + sheet["preview_image"],
            "sheet": meta,
            "calibration": sheet.get("calibration"),
            "north": sheet.get("north"),
            "apartment": sheet.get("apartment"),
            "qa": sheet.get("qa"),
            "warnings": sheet.get("warnings"),
            "reading_source": sheet.get("reading_source"),
            "openings_summary": _openings_summary(sheet),
        }
        floors.append({"floor_name": floor_name, "apartments": [apt],
                       "bg_image_url": preview_url_prefix + sheet["preview_image"]})
    first = model["sheets"][0] if model.get("sheets") else {}
    return {
        "project_name": (first.get("sheet") or {}).get("project_name") or model.get("source_file"),
        "source_file": model.get("source_file"),
        "bg_image_url": preview_url_prefix + first["preview_image"] if first else None,
        "floors": floors,
        "plan_model_schema": model.get("schema"),
        "warnings": model.get("warnings", []),
    }


def _openings_summary(sheet):
    out = {}
    for o in sheet.get("openings", []):
        out[o["kind"]] = out.get(o["kind"], 0) + 1
    return out
