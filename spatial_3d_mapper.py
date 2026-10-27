# -*- coding: utf-8 -*-
"""
3D Spatial Anchor & Coordinate Mapper for ArchiCheck AI
=======================================================
Maps 2D architectural audit notes, Value Engineering (VE) contour reductions,
facade cladding analyses, and interior design improvements to exact 1:1 metric
3D coordinates (X, Y, Z in meters) and camera presets on the existing Three.js
BIM models located in:
    G:\\Shared drives\\שליטה ובקרה\\מודלים פרויקטים

Zero-Rebuild Principle:
- Never rebuilds the base 3D models.
- Normalizes `viewer_3d_url` to `/models/<project_id>/<primary_viewer>` (served
  Zero-Copy by `server.py` from `G:\\Shared drives\\שליטה ובקרה\\מודלים פרויקטים`)
  while preserving `central_model_path`.
- Attaches `spatial_3d` metadata to every note so `webapp/audit_3d_overlay.js`
  can render 3D bounding volumes, dimension vectors, Before/After geometry toggles,
  auto-slice floors, and fly the camera directly to the finding.
"""

from sync_3d_models import CENTRAL_MODELS_ROOT, PROJECTS_CONFIG
import os

MODELS_BY_ID = {p["id"]: p for p in PROJECTS_CONFIG}


# =============================================================================
# EXACT 1:1 METRIC CAD 3D COORDINATES FOR HAFETZ HAIM 44 (חפץ חיים 44)
# =============================================================================
# Coordinate convention in hafetz44_3d_model.html (makeBox(x0, y0, x1, y1, z0, z1)):
#   - Three.js X = CAD X: West (-13.36m, balcony -15.36m, basement -17.72m) to East (+14.36m, balcony +16.36m, basement +18.51m)
#   - Three.js Z = CAD Y: North (-5.184m, basement -9.20m) to South (+4.216m, South core +5.196m, basement +9.05m)
#   - Three.js Y = Elevation Z:
#       * mar (Basement): zFloor = -5.10, zCeil = -2.20
#       * kar (Ground):   zFloor =  0.00, zCeil =  3.22
#       * f4  (Typical):  zFloor = 12.95, zCeil = 15.82 (3D Furnished Typical Floor)
#       * f9  (Penthouse):zFloor = 28.70, zCeil = 31.57 (3D Furnished Penthouse)
HAFETZ44_SPATIAL_3D = {
    "H44-W-01": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-13.10, 0.20, -6.55, 3.96, 12.98, 15.65],
        "extra_boxes_3d": [[-15.35, -4.90, -13.10, 3.96, 12.98, 14.15]],
        "pin_3d": [-10.20, 14.85, 2.20],
        "camera": {"target": [-10.5, 13.8, 1.8], "radius": 18.5, "phi": 0.60, "theta": -2.15},
        "callout_he": "✓ סלון ופינת אוכל מערביים (33.3 מ״ר) + מרפסת שמש (13.6 מ״ר · 3 כיווני אוויר)",
        "category_3d": "PASS",
    },
    "H44-W-02": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-1.05, -4.33, 2.25, -0.33, 12.98, 15.65],
        "pin_3d": [0.60, 14.85, -2.33],
        "camera": {"target": [0.60, 13.8, -2.33], "radius": 14.0, "phi": 0.54, "theta": -1.57},
        "callout_he": "✓ ממ״ד מערבי תקני: 10.20 מ״ר נטו (קירות בטון 25–30 ס״מ + חלון הדף דריי-קיפ)",
        "category_3d": "PASS",
    },
    "H44-W-03": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-13.10, -3.35, -10.11, -0.35, 12.98, 15.65],
        "pin_3d": [-11.60, 14.85, -1.85],
        "camera": {"target": [-11.60, 13.7, -2.10], "radius": 13.5, "phi": 0.50, "theta": -2.35},
        "callout_he": "⚠️ יחידת הורים מערבית: רוחב 299 ס״מ (מעבר 52 ס״מ לצד מיטה) ← סיבוב מיטה + דלת כיס",
        "category_3d": "WARN",
        "before_after_scene": "west_master_suite",
    },
    "H44-W-04": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-6.40, 1.18, -3.38, 3.96, 12.98, 15.65],
        "pin_3d": [-4.90, 14.85, 2.60],
        "camera": {"target": [-4.90, 13.7, 2.50], "radius": 13.5, "phi": 0.55, "theta": 1.85},
        "callout_he": "✓ מטבח מערבי (332×262 ס״מ) + דלפק חצי-אי ונישת מקרר",
        "category_3d": "PASS",
    },
    "H44-W-05": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-10.10, -1.42, -3.50, -0.52, 12.98, 15.45],
        "pin_3d": [-6.80, 14.80, -0.97],
        "camera": {"target": [-6.80, 13.6, -1.00], "radius": 13.0, "phi": 0.45, "theta": 1.57},
        "callout_he": "❌ ליקוי סטטוטורי (FAIL): רוחב מסדרון 90 ס״מ לאורך 5.45 מ׳ (נדרש ≥100 ס״מ) ← הזזת מחיצה ב-10 ס״מ",
        "category_3d": "FAIL",
        "before_after_scene": "west_corridor_fix",
    },
    "H44-E-01": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [5.66, 0.20, 14.10, 3.96, 12.98, 15.65],
        "extra_boxes_3d": [[14.10, -4.90, 16.35, 3.96, 12.98, 14.15]],
        "pin_3d": [10.20, 14.85, 2.20],
        "camera": {"target": [10.50, 13.8, 1.80], "radius": 18.5, "phi": 0.60, "theta": 0.85},
        "callout_he": "✓ חלל ציבורי דירה מזרחית (38.2 מ״ר) + מרפסת שמש (13.6 מ״ר) לרחוב חפץ חיים",
        "category_3d": "PASS",
    },
    "H44-E-02": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [5.45, -1.55, 10.95, -0.35, 12.98, 15.45],
        "pin_3d": [8.20, 14.80, -0.95],
        "camera": {"target": [8.20, 13.6, -1.10], "radius": 13.5, "phi": 0.48, "theta": 1.40},
        "callout_he": "⚠️ צומת 3 דלתות במסדרון המזרחי + דלת שירות החוסמת 50% מארון המסדרון",
        "category_3d": "WARN",
        "before_after_scene": "east_corridor_doors",
    },
    "H44-PH-01": {
        "floor_id": "f9",
        "slice_mode": "single",
        "bbox_3d": [4.25, 1.40, 9.30, 3.98, 28.73, 31.30],
        "extra_boxes_3d": [[-9.95, -4.94, -3.80, -1.48, 28.73, 31.30]],
        "pin_3d": [7.25, 30.50, 2.85],
        "camera": {"target": [6.80, 29.5, 2.40], "radius": 14.5, "phi": 0.52, "theta": 1.15},
        "callout_he": "⚠️ פנטהאוז: מרווח 96 ס״מ באי המטבח + חדרי שינה ברוחב 260 ס״מ ← הזזת אי ב-24 ס״מ (ל-120 ס״מ)",
        "category_3d": "WARN",
        "before_after_scene": "penthouse_island_fix",
    },
    "H44-GND-01": {
        "floor_id": "kar",
        "slice_mode": "single",
        "bbox_3d": [-1.50, -5.18, 6.60, 0.20, 0.03, 3.10],
        "pin_3d": [2.55, 2.25, -2.50],
        "camera": {"target": [2.55, 1.2, -2.00], "radius": 19.0, "phi": 0.56, "theta": -1.25},
        "callout_he": "⚠️ קומת קרקע: כפילות חדר עגלות (10.6 מ״ר) וחדר שירות (12.2 מ״ר) לצד מבואת הלובי",
        "category_3d": "WARN",
        "before_after_scene": "ground_contour_recess",
    },
    "H44-BSM-01": {
        "floor_id": "mar",
        "slice_mode": "single",
        "bbox_3d": [-17.72, -9.20, 18.51, 9.05, -5.08, -2.30],
        "pin_3d": [0.00, -3.10, 0.00],
        "camera": {"target": [0.0, -4.5, 0.0], "radius": 34.0, "phi": 0.54, "theta": 1.35},
        "callout_he": "⚠️ מרתף חניון (-5.10): 19 חניות רגילות, רמפה תלת-זרועית ופינת תמרון דרום-מערבית",
        "category_3d": "WARN",
        "before_after_scene": "basement_ve_full",
    },
    "H44-OPT-AG1": {
        "floor_id": "kar",
        "slice_mode": "single",
        "bbox_3d": [0.80, -5.18, 7.80, -0.40, 0.03, 3.15],
        "pin_3d": [4.30, 2.40, -2.80],
        "camera": {"target": [3.80, 1.4, -2.40], "radius": 18.5, "phi": 0.56, "theta": -1.10},
        "callout_he": "💰 חיסכון מאומת 198,400 ₪: נסיגת קונטור קומת קרקע ב-32 מ״ר (9 מ״ר לובי כלואים תחת קומה א׳)",
        "category_3d": "VE_AG",
        "before_after_scene": "ground_contour_recess",
    },
    "H44-OPT-AG2": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-2.20, -2.50, 2.80, 1.20, 12.98, 15.70],
        "pin_3d": [0.30, 14.90, -0.65],
        "camera": {"target": [0.30, 13.8, -0.65], "radius": 15.5, "phi": 0.52, "theta": 1.57},
        "callout_he": "💰 חיסכון מאומת 148,800 ₪: הידוק מבואת מעליות ופירים ב-3.0 מ״ר/קומה × 8 קומות (24 מ״ר)",
        "category_3d": "VE_AG",
        "before_after_scene": "typical_core_tighten",
    },
    "H44-OPT-UG1": {
        "floor_id": "mar",
        "slice_mode": "single",
        "bbox_3d": [-17.72, 5.90, -2.22, 9.05, -5.08, -2.25],
        "extra_boxes_3d": [[-17.72, -9.05, -17.17, 5.90, -5.08, -2.25]],
        "pin_3d": [-10.00, -3.00, 7.45],
        "camera": {"target": [-5.50, -4.4, 3.20], "radius": 27.5, "phi": 0.50, "theta": 1.78},
        "callout_he": "💰 חיסכון מאומת 203,000 ₪: קיצוץ 58 מ״ר דיפון (משאבות תחת רמפה דרומית H≥2.15m + העתקת חניה #16)",
        "category_3d": "VE_UG",
        "before_after_scene": "basement_ve_full",
    },
    "HAFETZ44-VE-FAC-1": {
        "floor_id": "all",
        "slice_mode": "cumulative",
        "bbox_3d": [14.10, -5.18, 16.36, 4.22, 3.50, 31.60],
        "pin_3d": [16.60, 18.00, -0.50],
        "camera": {"target": [12.0, 16.5, 0.0], "radius": 42.0, "phi": 1.05, "theta": 0.15},
        "callout_he": "🏛️ חזית מזרחית (רחוב חפץ חיים): שימור 88 מ״ר חיפוי HPL לבן בעמודוני המרפסות (0 ₪ פגיעה בחזית הרחוב)",
        "category_3d": "VE_FAC_KEEP",
        "before_after_scene": "facade_cladding_east",
    },
    "HAFETZ44-VE-FAC-2": {
        "floor_id": "all",
        "slice_mode": "cumulative",
        "bbox_3d": [-15.36, -5.18, -13.10, 4.22, 3.50, 31.60],
        "pin_3d": [-15.60, 18.00, -0.50],
        "camera": {"target": [-11.5, 16.5, 0.0], "radius": 42.0, "phi": 1.05, "theta": 3.00},
        "callout_he": "💰 חזית אחורית מערבית: חיסכון 34,400 ₪ (המרת 86 מ״ר HPL בעמודוני מרפסות לטיח אקרילי גמיש)",
        "category_3d": "VE_FAC_SAVE",
        "before_after_scene": "facade_cladding_west",
    },
    "HAFETZ44-VE-FAC-3": {
        "floor_id": "all",
        "slice_mode": "cumulative",
        "bbox_3d": [-13.36, -5.45, 14.36, -4.85, 3.50, 31.60],
        "pin_3d": [0.50, 18.00, -5.65],
        "camera": {"target": [0.5, 16.5, -4.0], "radius": 44.0, "phi": 1.02, "theta": -1.57},
        "callout_he": "💰 חזית צד צפונית: חיסכון 66,400 ₪ (המרת 166 מ״ר רצועות מסגור HPL אנכיות לטיח אקרילי)",
        "category_3d": "VE_FAC_SAVE",
        "before_after_scene": "facade_cladding_north",
    },
    "HAFETZ44-VE-FAC-4": {
        "floor_id": "all",
        "slice_mode": "cumulative",
        "bbox_3d": [-13.36, 4.00, 14.36, 5.30, 3.50, 31.60],
        "pin_3d": [0.50, 18.00, 5.55],
        "camera": {"target": [0.5, 16.5, 4.0], "radius": 44.0, "phi": 1.02, "theta": 1.57},
        "callout_he": "💰 חזית צד דרומית: חיסכון 73,600 ₪ (המרת 184 מ״ר רצועות HPL סביב חלונות וקיר מדרגות לטיח)",
        "category_3d": "VE_FAC_SAVE",
        "before_after_scene": "facade_cladding_south",
    },
    "H44-LOCKED-CORE1": {
        "floor_id": "mar",
        "slice_mode": "single",
        "bbox_3d": [-5.50, -4.33, -1.05, -0.33, -5.08, -2.25],
        "pin_3d": [-3.25, -3.00, -2.33],
        "camera": {"target": [-3.25, -4.3, -2.33], "radius": 19.0, "phi": 0.50, "theta": -1.65},
        "callout_he": "🔄 ליבה כלואה בקירות ממ״ד יורדים (12 מ״ר · 0 ₪ שלד): הסבת חדר המשאבות הישן ל-3 מחסני דיירים (~180,000 ₪ ערך)",
        "category_3d": "LOCKED_CORE",
        "before_after_scene": "basement_ve_full",
    },
    "H44-OPT-APT1": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-11.45, -4.95, -3.50, -0.45, 12.98, 15.65],
        "pin_3d": [-9.80, 14.85, -3.60],
        "camera": {"target": [-9.20, 13.7, -2.50], "radius": 15.0, "phi": 0.48, "theta": -2.10},
        "callout_he": "🛋️ שיפור תכנון דירה מערבית (+2.6 מ״ר לדירה): ביטול קירות חדר ארונות צפוף + הרחבת מסדרון ל-100 ס״מ",
        "category_3d": "APT_IMP",
        "before_after_scene": "west_corridor_fix",
    },
    "H44-OPT-APT2": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [1.80, -0.45, 5.65, 1.55, 12.98, 15.65],
        "pin_3d": [3.75, 14.85, 0.55],
        "camera": {"target": [3.75, 13.7, 0.55], "radius": 13.5, "phi": 0.50, "theta": 1.35},
        "callout_he": "🛋️ שיפור תכנון דירה מזרחית (+1.5 מ״ר לדירה): סיפוח נישת המבואה הקומתית למבואת כניסה וארון מעילים",
        "category_3d": "APT_IMP",
        "before_after_scene": "typical_core_tighten",
    },
}


def _infer_generic_spatial_3d(note):
    """
    Fallback 3D coordinate mapper for projects outside HAFETZ44_SPATIAL_3D,
    mapping sheet_id + (x_pct, y_pct, w_pct, h_pct) to approximate metric coordinates.
    """
    sheet_id = (note.get("sheet_id") or "").lower()
    if "basement" in sheet_id or "bsm" in sheet_id:
        floor_id = "mar"
        z0, z1 = -5.0, -2.3
    elif "ground" in sheet_id or "gnd" in sheet_id:
        floor_id = "kar"
        z0, z1 = 0.05, 3.1
    elif "penthouse" in sheet_id or "ph" in sheet_id or "f6" in sheet_id or "f7" in sheet_id or "floor5" in sheet_id:
        floor_id = "f9"
        z0, z1 = 22.0, 24.8
    else:
        floor_id = "f4"
        z0, z1 = 12.95, 15.70

    x_pct = float(note.get("x_pct", 40.0))
    y_pct = float(note.get("y_pct", 40.0))
    w_pct = float(note.get("w_pct", 15.0))
    h_pct = float(note.get("h_pct", 15.0))

    x0 = round((x_pct - 50.0) / 100.0 * 30.0, 2)
    x1 = round(((x_pct + w_pct) - 50.0) / 100.0 * 30.0, 2)
    y0 = round((y_pct - 50.0) / 100.0 * 14.0, 2)
    y1 = round(((y_pct + h_pct) - 50.0) / 100.0 * 14.0, 2)
    cx = round(0.5 * (x0 + x1), 2)
    cy = round(0.5 * (y0 + y1), 2)

    is_fac = note.get("ve_category") == "FAC"
    return {
        "floor_id": "all" if is_fac else floor_id,
        "slice_mode": "cumulative" if is_fac else "single",
        "bbox_3d": [x0, y0, x1, y1, z0, z1],
        "pin_3d": [cx, round(z1 - 0.6, 2), cy],
        "camera": {"target": [cx, round(z0 + 1.0, 2), cy], "radius": 20.0, "phi": 0.56, "theta": 1.25},
        "callout_he": f"#{note.get('pin_num')}: {note.get('title', '')}",
        "category_3d": note.get("ve_category") or note.get("status", "PASS"),
    }


def enrich_payload_with_3d_spatial_data(payload):
    """
    1. Normalizes `viewer_3d_url` to `/models/<pid>/<primary_viewer>` so the web UI
       can embed or open the existing central 3D model from
       `G:\\Shared drives\\שליטה ובקרה\\מודלים פרויקטים` (Zero-Copy).
    2. Attaches `spatial_3d` to every note in `payload["notes"]`.
    """
    if not payload or not isinstance(payload, dict):
        return payload

    pid = payload.get("project_id", "")
    cfg = MODELS_BY_ID.get(pid)
    if cfg:
        viewer_file = cfg.get("primary_viewer") or cfg.get("bim_viewer")
        central_full_path = os.path.join(CENTRAL_MODELS_ROOT, cfg["folder_name"], viewer_file)
        payload["central_model_path"] = central_full_path
        payload["viewer_3d_url"] = f"/models/{pid}/{viewer_file}"

    for note in payload.get("notes", []):
        nid = note.get("id", "")
        if pid == "hafetz44" and nid in HAFETZ44_SPATIAL_3D:
            note["spatial_3d"] = dict(HAFETZ44_SPATIAL_3D[nid])
        elif "spatial_3d" not in note:
            note["spatial_3d"] = _infer_generic_spatial_3d(note)

    return payload
