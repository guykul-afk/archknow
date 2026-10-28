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
# 1. EXACT 1:1 METRIC CAD 3D COORDINATES FOR HAFETZ HAIM 44 (חפץ חיים 44)
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
        "bbox_3d": [-13.10, -0.25, -6.55, 3.96, 12.98, 15.65],
        "extra_boxes_3d": [[-15.35, -4.90, -13.10, 3.96, 12.98, 14.15]],
        "pin_3d": [-10.20, 14.85, 2.20],
        "camera": {"target": [-10.5, 13.8, 1.8], "radius": 18.5, "phi": 0.60, "theta": -2.15},
        "callout_he": "✓ ח. מגורים (418×635) + פ. אוכל (418×340) + מרפסת שמש מערבית (200×900 · כ-18.5 מ״ר)",
        "category_3d": "PASS",
    },
    "H44-W-02": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-6.40, 1.18, -3.38, 3.96, 12.98, 15.65],
        "pin_3d": [-4.90, 14.85, 2.60],
        "camera": {"target": [-4.90, 13.7, 2.50], "radius": 13.5, "phi": 0.55, "theta": 1.85},
        "callout_he": "✓ מטבח דירה מערבית (340×418 ס״מ): משולש עבודה תקני, נישת מקרר ודלפק חצי-אי",
        "category_3d": "PASS",
    },
    "H44-W-03": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-13.10, -4.95, -9.65, -0.35, 12.98, 15.65],
        "pin_3d": [-11.60, 14.85, -1.85],
        "camera": {"target": [-11.60, 13.7, -2.10], "radius": 13.5, "phi": 0.50, "theta": -2.35},
        "callout_he": "⚠️ חדר הורים מערבי (468×299) + ח. ארונות (165×160) + ח. רחצה (160×160): מעבר 52 ס״מ ← סיבוב מיטה + דלת כיס",
        "category_3d": "WARN",
        "before_after_scene": "west_master_suite",
    },
    "H44-W-04": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-1.05, -4.33, 2.25, -0.33, 12.98, 15.65],
        "pin_3d": [0.60, 14.85, -2.33],
        "camera": {"target": [0.60, 13.8, -2.33], "radius": 14.0, "phi": 0.54, "theta": -1.57},
        "callout_he": "✓ ממ״ד דירה מערבית תקני (335×400 ס״מ = 13.40 מ״ר נטו — 49% מעל דרישת המינימום של פקע״ר)",
        "category_3d": "PASS",
    },
    "H44-W-05": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-9.79, -1.48, -1.25, -0.33, 12.98, 15.45],
        "pin_3d": [-6.80, 14.80, -0.85],
        "camera": {"target": [-6.80, 13.6, -1.00], "radius": 13.0, "phi": 0.45, "theta": 1.57},
        "callout_he": "⚠️ מסדרון מערבי (100/105 ס״מ לאורך 7.11 מ׳): יישור מדרגת קיר וביטול היצרות משקוף (90 ס״מ) בכניסה להורים",
        "category_3d": "WARN",
        "before_after_scene": "west_corridor_fix",
    },
    "H44-W-06": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-9.55, -4.95, -3.61, -1.48, 12.98, 15.65],
        "extra_boxes_3d": [[-3.55, -4.23, -1.25, -1.48, 12.98, 15.65]],
        "pin_3d": [-6.58, 14.85, -3.20],
        "camera": {"target": [-6.58, 13.7, -3.10], "radius": 14.0, "phi": 0.52, "theta": -1.57},
        "callout_he": "✓ חדרי שינה צפוניים בדירה המערבית: חדר (299×348 ס״מ) וחדר (285×348 ס״מ) + ח. רחצה (240×170) וח. שירות (240×95)",
        "category_3d": "PASS",
    },
    "H44-E-01": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [5.66, -0.25, 14.10, 3.96, 12.98, 15.65],
        "extra_boxes_3d": [[14.10, -4.90, 16.35, 3.96, 12.98, 14.15]],
        "pin_3d": [10.20, 14.85, 2.20],
        "camera": {"target": [10.50, 13.8, 1.80], "radius": 18.5, "phi": 0.60, "theta": 0.85},
        "callout_he": "✓ דירה מזרחית: ח. מגורים (545×418) + פ. אוכל (418×245) + מטבח (300×418) + מרפסת שמש (200×940)",
        "category_3d": "PASS",
    },
    "H44-E-02": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [10.95, -4.95, 14.10, -0.35, 12.98, 15.65],
        "pin_3d": [12.50, 14.85, -2.20],
        "camera": {"target": [12.50, 13.7, -2.20], "radius": 13.5, "phi": 0.52, "theta": 0.95},
        "callout_he": "✓ סוויטת הורים מזרחית: חדר הורים (422×300 ס״מ — עובר ADG!) + ח. ארונות (149×158) + ח. רחצה (160×158)",
        "category_3d": "PASS",
    },
    "H44-E-03": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [8.05, -4.95, 10.88, -1.48, 12.98, 15.65],
        "pin_3d": [9.45, 14.85, -3.20],
        "camera": {"target": [9.45, 13.7, -3.10], "radius": 12.5, "phi": 0.50, "theta": -1.45},
        "callout_he": "⚠️ חדר שינה צפוני מזרחי (279×348 ס״מ): 0 פלישה למסדרון (כדי לא לחסום את הכניסה לאמבטיה הכללית!) · הזזת דלת ב-5 ס״מ לארון 60 ס״מ",
        "category_3d": "WARN",
        "before_after_scene": "east_north_bedroom_fix",
    },
    "H44-E-04": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [5.45, -1.55, 10.95, -0.35, 12.98, 15.45],
        "extra_boxes_3d": [[5.66, -4.23, 7.96, -1.48, 12.98, 15.65]],
        "pin_3d": [8.20, 14.80, -0.95],
        "camera": {"target": [8.20, 13.6, -1.10], "radius": 13.5, "phi": 0.48, "theta": 1.40},
        "callout_he": "⚠️ מסדרון מזרחי מוגן ב-100% (416×105 ס״מ — 0 ס״מ קיצור כדי לא לחסום את האמבטיה הכללית 238×170!) + דלת כיס בח. שירות (238×93)",
        "category_3d": "WARN",
        "before_after_scene": "east_corridor_doors",
    },
    "H44-E-05": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [2.46, -4.33, 5.46, -0.33, 12.98, 15.65],
        "pin_3d": [3.96, 14.85, -2.33],
        "camera": {"target": [3.96, 13.8, -2.33], "radius": 13.5, "phi": 0.54, "theta": -1.57},
        "callout_he": "✓ ממ״ד דירה מזרחית תקני (295×400 ס״מ = 11.80 מ״ר נטו — חדר שינה זוגי מרווח)",
        "category_3d": "PASS",
    },
    "H44-CORE-01": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-1.05, -0.33, 5.46, 1.48, 12.98, 15.65],
        "extra_boxes_3d": [[-3.16, 1.48, 3.70, 4.99, 12.98, 15.65]],
        "pin_3d": [0.80, 14.85, 0.25],
        "camera": {"target": [0.80, 13.7, 0.50], "radius": 14.5, "phi": 0.52, "theta": 1.57},
        "callout_he": "✓ לובי קומתי בוטיק (651×142 ס״מ) + 2 מחסנים דירתיים (120×351): מוגן אדריכלית, מרחבית ועיצובית (0 מ״ר קיטון לובי!)",
        "category_3d": "PASS",
        "before_after_scene": "typical_lobby_protected",
    },
    "H44-PH-01": {
        "floor_id": "f9",
        "slice_mode": "single",
        "bbox_3d": [3.80, -4.94, 9.55, 0.85, 28.73, 31.30],
        "extra_boxes_3d": [
            [9.60, -5.18, 14.36, 4.22, 28.73, 30.20],
            [-13.36, -5.18, -10.21, 4.22, 28.73, 30.20],
            [2.51, -4.33, 3.66, -1.62, 28.73, 31.30],
        ],
        "pin_3d": [7.50, 30.50, -1.80],
        "camera": {"target": [7.50, 29.5, -1.20], "radius": 18.5, "phi": 0.56, "theta": 0.85},
        "callout_he": "✓ פנטהאוז #17 (148.1+73.0 מ״ר): ח. מגורים פנורמי (560×841) + פ. אוכל (320×260) + 2 מרפסות גג (456×940 ו-295×940)",
        "category_3d": "PASS",
    },
    "H44-PH-02": {
        "floor_id": "f9",
        "slice_mode": "single",
        "bbox_3d": [4.25, 1.10, 9.35, 3.98, 28.73, 31.30],
        "pin_3d": [7.25, 30.50, 2.85],
        "camera": {"target": [6.80, 29.5, 2.40], "radius": 13.5, "phi": 0.52, "theta": 1.15},
        "callout_he": "⚠️ מטבח פנטהאוז (510×420 ס״מ): מרווח 96 ס״מ בין האי לשיש הדרומי ← הזזת האי ב-24 ס״מ צפונה למעבר 120 ס״מ",
        "category_3d": "WARN",
        "before_after_scene": "penthouse_island_fix",
    },
    "H44-PH-03": {
        "floor_id": "f9",
        "slice_mode": "single",
        "bbox_3d": [-9.95, -0.25, -7.15, 3.98, 28.73, 31.30],
        "extra_boxes_3d": [
            [-9.95, -4.94, -3.69, -1.48, 28.73, 31.30],
            [-7.05, -0.25, -2.00, 3.99, 28.73, 31.30],
            [-1.05, -4.33, 2.25, -1.62, 28.73, 31.30],
        ],
        "pin_3d": [-8.55, 30.50, 2.10],
        "camera": {"target": [-6.80, 29.5, -0.50], "radius": 15.5, "phi": 0.50, "theta": -2.15},
        "callout_he": "⚠️ חדרי שינה בפנטהאוז: הרחבת החדר הדרום-מערבי מ-280×423 ל-300×423 ס״מ (ADG) וייעול החדרים הצפון-מערביים (306×344)",
        "category_3d": "WARN",
        "before_after_scene": "penthouse_bedrooms_fix",
    },
    "H44-GND-01": {
        "floor_id": "kar",
        "slice_mode": "single",
        "bbox_3d": [2.35, -0.12, 13.80, 3.95, 0.03, 3.10],
        "extra_boxes_3d": [[-1.05, -4.43, 8.61, -0.33, 0.03, 3.10]],
        "pin_3d": [8.20, 2.25, 1.80],
        "camera": {"target": [6.50, 1.2, 0.20], "radius": 19.0, "phi": 0.56, "theta": 1.15},
        "callout_he": "✓ קומת קרקע (±0.00): לובי ראשי (974×413) בריהוט ציבורי מותאם, חדר דיירים (260×408), חדר עגלות (305×400) ואשפה (330×355)",
        "category_3d": "PASS",
    },
    "H44-BSM-01": {
        "floor_id": "mar",
        "slice_mode": "single",
        "bbox_3d": [-4.80, 5.95, 4.20, 8.85, -5.08, -2.75],
        "extra_boxes_3d": [[-5.50, -4.33, -1.05, -0.33, -5.08, -2.25]],
        "pin_3d": [-0.30, -3.10, 7.40],
        "camera": {"target": [-2.0, -4.3, 3.0], "radius": 28.0, "phi": 0.52, "theta": 1.55},
        "callout_he": "✓ מרתף חניון (-5.10): 0 הזזת חניות! כל 13 החניות (#7–#19) נשמרות במקומן המקורי · משאבות תחת רמפה דרומית ממזרח ל-#17 + 3 מחסנים בקיר ממ״דים",
        "category_3d": "PASS",
        "before_after_scene": "basement_ve_full",
    },
    "H44-OPT-AG1": {
        "floor_id": "kar",
        "slice_mode": "single",
        "bbox_3d": [8.60, -4.90, 13.90, -2.62, 0.03, 3.15],
        "extra_boxes_3d": [[-4.25, -5.18, -2.75, -0.77, 0.03, 3.15]],
        "pin_3d": [11.10, 2.40, -3.80],
        "camera": {"target": [8.50, 1.4, -2.60], "radius": 18.5, "phi": 0.56, "theta": -1.10},
        "callout_he": "💰 חיסכון מאומת 74,400 ₪: הידוק תאי אוורור החניון החיצוניים הבולטים (530×228 ו-150×441 ס״מ = -12 מ״ר · 0 פגיעה בלובי ובחדרי השירות!)",
        "category_3d": "VE_AG",
        "before_after_scene": "ground_contour_recess",
    },
    "H44-OPT-AG2": {
        "floor_id": "gag",
        "slice_mode": "single",
        "bbox_3d": [-8.60, -4.50, 8.20, 1.50, 31.85, 33.10],
        "pin_3d": [0.30, 33.40, -1.00],
        "camera": {"target": [0.30, 32.2, -1.00], "radius": 18.5, "phi": 0.52, "theta": 1.57},
        "callout_he": "💰 חיסכון מאומת 86,800 ₪: הידוק מסתורי המערכות ודודי השמש בגג העליון (+31.85m · -14.0 מ״ר · 0 מ״ר קיטון בלובי הקומתי!)",
        "category_3d": "VE_AG",
        "before_after_scene": "roof_tech_tighten",
    },
    "H44-OPT-UG1": {
        "floor_id": "mar",
        "slice_mode": "single",
        "bbox_3d": [-4.80, 5.95, 4.20, 8.85, -5.08, -2.75],
        "extra_boxes_3d": [[-5.50, -4.33, -1.05, -0.33, -5.08, -2.25]],
        "pin_3d": [-0.30, -3.00, 7.40],
        "camera": {"target": [-2.00, -4.3, 3.00], "radius": 28.0, "phi": 0.50, "theta": 1.55},
        "callout_he": "💰 חיסכון מאומת 35,000 ₪ (0 הזזת חניות! #7–#19 נשמרות במקומן): משאבות תחת רמפה דרומית ממזרח לחניה #17 + 3 מחסנים בליבה + הידוק שולי דיפון (-10 מ״ר)",
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
        "callout_he": "🔄 ליבה כלואה בקירות ממ״ד יורדים (12 מ״ר במרתף + 24 מ״ר לובי קומתי מוגן · 0 ₪ שלד): הסבת תא המשאבות ל-3 מחסני דיירים ושימור הלובי הקומתי",
        "category_3d": "LOCKED_CORE",
        "before_after_scene": "basement_ve_full",
    },
    "H44-LOCKED-CORE2": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-1.05, -0.33, 5.46, 1.48, 12.98, 15.65],
        "pin_3d": [0.80, 14.85, 0.25],
        "camera": {"target": [0.80, 13.7, 0.50], "radius": 14.5, "phi": 0.52, "theta": 1.57},
        "callout_he": "🛡️ לובי קומתי בוטיק (651×142 ס״מ בקומות 1–8) וחדרי שירות בקרקע תחת תקרת קומה 1: מוגנים 100% אדריכלית, מרחבית ועיצובית (0 מ״ר קיטון לובי!)",
        "category_3d": "LOCKED_CORE",
        "before_after_scene": "typical_lobby_protected",
    },
    "H44-OPT-APT1": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-11.45, -4.95, -3.50, -0.45, 12.98, 15.65],
        "pin_3d": [-9.80, 14.85, -3.60],
        "camera": {"target": [-9.20, 13.7, -2.50], "radius": 15.0, "phi": 0.48, "theta": -2.10},
        "callout_he": "🛋️ שיפור תכנון דירה מערבית (+1.8 מ״ר לדירה): ביטול קירות חדר ארונות צפוף + יישור משקוף מסדרון ל-105 ס״מ (ללא חסימת דלת האמבטיה הכללית!)",
        "category_3d": "APT_IMP",
        "before_after_scene": "west_corridor_fix",
    },
    "H44-OPT-APT2": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [10.95, -4.95, 12.55, -3.35, 12.98, 15.65],
        "extra_boxes_3d": [[5.66, -4.23, 7.96, -1.48, 12.98, 15.65]],
        "pin_3d": [11.50, 14.85, -3.80],
        "camera": {"target": [9.20, 13.7, -2.50], "radius": 14.0, "phi": 0.50, "theta": 1.35},
        "callout_he": "🛋️ שיפור תכנון פנים-דירתי בדירה המזרחית (+0.9 מ״ר בתוך החדרים): ביטול מחיצות ח. ארונות (149×158) + דלת כיס בח. שירות (0 ס״מ קיצור מסדרון — הגנה מלאה על הכניסה לאמבטיה הכללית!)",
        "category_3d": "APT_IMP",
        "before_after_scene": "east_corridor_apt_fix",
    },
}


# =============================================================================
# 2. EXACT 1:1 METRIC CAD 3D COORDINATES FOR FEIERBERG 3 (פאירברג 3, פתח תקווה)
# =============================================================================
# Coordinate convention in feierberg3_3d_model.html & feierberg3_extracted_plans.json:
#   - Building Typical Envelope (f1..f8): X in [-13.125, +13.125] (26.25m), Z (CAD Y) in [-4.20, +4.20] (8.40m) + South Balconies Z in [+4.20, +5.80]
#   - Note: In the 3D BIM model (`feierberg3_3d_model.html`), Apartment 1 (105.46 sqm, 880cm corridor, 650x420 living room, 350x360 master suite)
#     is positioned on the West/Left wing (X in [-13.125, +1.55]), and Apartment 2 (85.53 sqm, 625cm corridor) is positioned on the East/Right wing (X in [+1.68, +13.125]).
#   - Floor IDs & Elevations in feierberg3_3d_model.html (`FLOORS`):
#       * b2  (Basement -2): zFloor = -7.80, zCeil = -5.05
#       * b1  (Basement -1): zFloor = -4.80, zCeil = -0.25
#       * kar (Ground):      zFloor =  0.00, zCeil =  3.25
#       * f4  (Typical 1-8): zFloor = 12.95, zCeil = 15.70
#       * f9  (Duplex Low):  zFloor = 28.87, zCeil = 31.82
#       * f10 (Duplex High): zFloor = 32.02, zCeil = 34.97
#       * gag (Top Roof):    zFloor = 35.17, zCeil = 37.50
FEIERBERG3_SPATIAL_3D = {
    "FB3-W-01": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-4.95, 0.20, 1.55, 4.00, 12.98, 15.65],
        "extra_boxes_3d": [[-5.88, 4.20, 1.57, 5.80, 12.98, 14.15]],
        "pin_3d": [-1.70, 14.85, 2.30],
        "camera": {"target": [-1.80, 13.80, 2.20], "radius": 16.5, "phi": 0.56, "theta": 1.65},
        "callout_he": "✓ דירה 1 (105.5 מ״ר): סלון ופינת אוכל דרומיים רחבים (650×420 ס״מ = 27.3 מ״ר) + מרפסת שמש (12.0 מ״ר)",
        "category_3d": "PASS",
    },
    "FB3-W-02": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-12.95, -0.20, -8.10, 4.00, 12.98, 15.65],
        "pin_3d": [-10.50, 14.85, 2.10],
        "camera": {"target": [-10.50, 13.75, 1.90], "radius": 14.0, "phi": 0.52, "theta": 1.85},
        "callout_he": "✓ דירה 1: סוויטת הורים מרווחת (350×360 ס״מ), חדר ארונות ורחצה הורים מאווררת טבעית",
        "category_3d": "PASS",
    },
    "FB3-W-03": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-6.35, -4.00, -3.50, -0.30, 12.98, 15.65],
        "pin_3d": [-4.95, 14.85, -2.15],
        "camera": {"target": [-4.95, 13.75, -2.15], "radius": 14.0, "phi": 0.50, "theta": -1.65},
        "callout_he": "⚠️ דירה 1: חדר שינה צפוני (370×280 ס״מ = 10.36 מ״ר) ושמירת מעבר מסדרון מול האמבטיה הכללית ← נישת ארון קו-אפס במחיצה הפנימית",
        "category_3d": "WARN",
        "before_after_scene": "fb3_apt1_corridor_fix",
    },
    "FB3-W-04": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-12.95, -4.00, -10.05, -0.40, 12.98, 15.65],
        "pin_3d": [-11.50, 14.85, -2.20],
        "camera": {"target": [-11.50, 13.75, -2.20], "radius": 14.0, "phi": 0.50, "theta": -1.95},
        "callout_he": "✓ דירה 1: ממ״ד צפון-מזרחי תקני ומרווח (350×280 ס״מ = 9.80 מ״ר נטו — עובר פקע״ר ו-NDSS!)",
        "category_3d": "PASS",
    },
    "FB3-W-05": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-10.05, -0.45, -3.50, 0.55, 12.98, 15.55],
        "pin_3d": [-6.80, 14.85, 0.05],
        "camera": {"target": [-6.80, 13.75, 0.05], "radius": 14.5, "phi": 0.48, "theta": 1.57},
        "callout_he": "⚠️ דירה 1: מסדרון חדרי שינה (880×100 ס״מ) ← שמירה מלאה מול דלת האמבטיה הכללית וקיצור הקצה המזרחי בלבד (+1.1 מ״ר)",
        "category_3d": "WARN",
        "before_after_scene": "fb3_apt1_corridor_fix",
    },
    "FB3-E-01": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [1.70, 0.60, 6.08, 4.00, 12.98, 15.65],
        "extra_boxes_3d": [[1.68, 4.20, 9.12, 5.80, 12.98, 14.15]],
        "pin_3d": [3.90, 14.85, 2.30],
        "camera": {"target": [4.20, 13.80, 2.20], "radius": 16.5, "phi": 0.56, "theta": 1.35},
        "callout_he": "✓ דירה 2 (85.5 מ״ר): סלון ופינת אוכל (625×370/410 ס״מ = 24.8 מ״ר) ומרפסת דרומית (12.0 מ״ר)",
        "category_3d": "PASS",
    },
    "FB3-E-03": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [6.08, 0.60, 8.55, 4.00, 12.98, 15.65],
        "pin_3d": [7.30, 14.85, 2.50],
        "camera": {"target": [7.30, 13.80, 2.30], "radius": 13.5, "phi": 0.52, "theta": 1.45},
        "callout_he": "✓ דירה 2: מטבח מקבילי עם אי עבודה ואכילה (340×255 ס״מ = 8.65 מ״ר · מעבר 105 ס״מ)",
        "category_3d": "PASS",
    },
    "FB3-E-02": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [8.65, 0.45, 12.95, 4.00, 12.98, 15.65],
        "pin_3d": [10.80, 14.85, 2.20],
        "camera": {"target": [10.60, 13.75, 2.00], "radius": 14.0, "phi": 0.52, "theta": 1.20},
        "callout_he": "⚠️ דירה 2: סוויטת הורים דרום-מערבית (340×280/295 ס״מ) ← הרחבה ל-3.12 מ׳ ע״י קיצור המסדרון",
        "category_3d": "WARN",
        "before_after_scene": "fb3_apt2_corridor_fix",
    },
    "FB3-E-04": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [9.25, -4.00, 12.95, -1.25, 12.98, 15.65],
        "extra_boxes_3d": [[4.38, -4.00, 7.20, -0.40, 12.98, 15.65]],
        "pin_3d": [11.10, 14.85, -2.60],
        "camera": {"target": [8.50, 13.75, -2.40], "radius": 15.0, "phi": 0.50, "theta": -1.35},
        "callout_he": "⚠️ דירה 2: חדר שינה צפוני (350×280 ס״מ = 9.80 מ״ר) וממ״ד (365×265 ס״מ = 9.67 מ״ר) מאווררים לצפון",
        "category_3d": "WARN",
    },
    "FB3-E-05": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [4.38, -1.25, 10.15, 0.45, 12.98, 15.55],
        "pin_3d": [7.25, 14.85, -0.35],
        "camera": {"target": [7.25, 13.75, -0.35], "radius": 14.0, "phi": 0.48, "theta": 1.57},
        "callout_he": "⚠️ דירה 2: מסדרון חדרי שינה (625×100 ס״מ) ← קיצור קצה המסדרון ב-95 ס״מ (+1.4 מ״ר להורים)",
        "category_3d": "WARN",
        "before_after_scene": "fb3_apt2_corridor_fix",
    },
    "FB3-CORE-01": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-3.48, -4.20, 4.38, -0.20, 12.98, 15.65],
        "pin_3d": [0.50, 14.85, -1.50],
        "camera": {"target": [0.50, 13.75, -1.50], "radius": 14.5, "phi": 0.50, "theta": 1.57},
        "callout_he": "✓ לובי קומתי בוטיק מוגן (380×185 ס״מ), מעלית וחדר מדרגות: מוגן 100% מקיטון (מבחן 7 — 0 מ״ר גריעה!)",
        "category_3d": "PASS",
    },
    "FB3-PH-01": {
        "floor_id": "f9",
        "slice_mode": "single",
        "bbox_3d": [-8.50, -0.20, 10.20, 5.60, 28.90, 31.75],
        "pin_3d": [0.00, 30.90, 2.80],
        "camera": {"target": [0.00, 29.80, 1.80], "radius": 24.0, "phi": 0.58, "theta": 1.52},
        "callout_he": "✓ קומה 9: סלונים ופינות אוכל בדופלקס-פנטהאוזים #17 ו-#18 + מרפסות גג דרומיות (43.3 ו-36.4 מ״ר)",
        "category_3d": "PASS",
    },
    "FB3-PH-02": {
        "floor_id": "f9",
        "slice_mode": "single",
        "bbox_3d": [-11.50, -3.95, -8.50, 2.00, 28.90, 31.75],
        "extra_boxes_3d": [[4.40, -3.95, 11.50, -1.10, 28.90, 31.75]],
        "pin_3d": [-10.00, 30.90, -1.00],
        "camera": {"target": [0.00, 29.80, -1.80], "radius": 22.0, "phi": 0.54, "theta": -1.57},
        "callout_he": "✓ קומה 9: מטבחי שף מקבילים וממ״דים קומתיים (350×280 ו-365×265 ס״מ) במפלס התחתון של דופלקסים #17 ו-#18",
        "category_3d": "PASS",
    },
    "FB3-PH-03": {
        "floor_id": "f10",
        "slice_mode": "single",
        "bbox_3d": [-11.50, -3.95, 11.50, 2.00, 32.05, 34.90],
        "pin_3d": [-9.40, 34.10, -2.20],
        "camera": {"target": [0.00, 33.10, -1.00], "radius": 22.0, "phi": 0.54, "theta": 1.52},
        "callout_he": "⚠️ קומה 10: סוויטות הורים נשיאותיות (380×360 ו-370×350 ס״מ), חדרי שינה עליונים וגלריות מעבר ← הידוק גלריה (+2.1 מ״ר)",
        "category_3d": "WARN",
        "before_after_scene": "fb3_f10_gallery_fix",
    },
    "FB3-GND-01": {
        "floor_id": "kar",
        "slice_mode": "single",
        "bbox_3d": [-8.50, -3.60, 8.50, 3.20, 0.03, 3.20],
        "pin_3d": [0.50, 2.35, 1.80],
        "camera": {"target": [0.50, 1.30, 0.80], "radius": 20.0, "phi": 0.56, "theta": 1.45},
        "callout_he": "✓ קומת קרקע (±0.00): לובי ראשי (770×430) בריהוט ציבורי מותאם, חדר דיירים (450×410), אופניים (540×350) ואשפה (390×360)",
        "category_3d": "PASS",
    },
    "FB3-BSM-01": {
        "floor_id": "b1",
        "slice_mode": "single",
        "bbox_3d": [-16.60, -7.20, 14.80, 7.00, -4.78, -0.45],
        "pin_3d": [-2.50, -2.20, 1.20],
        "camera": {"target": [-1.00, -3.80, 0.50], "radius": 32.0, "phi": 0.52, "theta": 1.52},
        "callout_he": "✓ מרתפים 1- ו-2-: 19 חניות קונבנציונליות רגילות, רמפה תקנית (15%/7.5% וסיבוב R=369/R500) ומיסעות 5.90–6.50 מ׳",
        "category_3d": "PASS",
    },
    "FB3-OPT-AG1": {
        "floor_id": "kar",
        "slice_mode": "single",
        "bbox_3d": [4.38, -4.15, 12.80, 0.20, 0.03, 3.20],
        "pin_3d": [8.60, 2.35, -1.95],
        "camera": {"target": [7.50, 1.30, -1.50], "radius": 18.5, "phi": 0.54, "theta": -1.15},
        "callout_he": "💰 חיסכון מאומת 260,400 ₪: פינוי מאגר המים וחדר המשאבות בקרקע לתחתית הרמפה העליונה במרתף 1- (-42 מ״ר בנוי עילי)",
        "category_3d": "VE_AG",
    },
    "FB3-OPT-AG2": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-3.48, -4.20, 4.38, -2.20, 12.98, 15.65],
        "pin_3d": [0.45, 14.85, -3.20],
        "camera": {"target": [0.45, 13.80, -2.50], "radius": 14.5, "phi": 0.50, "theta": -1.57},
        "callout_he": "💰 חיסכון מאומת 173,600 ₪: הידוק בליטת פיר המדרגות הצפוני והטמעת ארונות שירות ב-3.5 מ״ר/קומה × 8 קומות (0 מ״ר קיטון בלובי הקומתי!)",
        "category_3d": "VE_AG",
    },
    "FB3-OPT-AG3": {
        "floor_id": "f10",
        "slice_mode": "single",
        "bbox_3d": [-3.48, -4.20, 4.38, 0.85, 32.05, 37.30],
        "pin_3d": [0.45, 34.40, -1.65],
        "camera": {"target": [0.45, 33.20, -1.50], "radius": 16.5, "phi": 0.54, "theta": -1.50},
        "callout_he": "💰 חיסכון מאומת 74,400 ₪: צמצום מבואת הגלריה המשותפת בקומה 10 והתאמת חדר היציאה לגג לקו הפירים (-12.0 מ״ר)",
        "category_3d": "VE_AG",
    },
    "FB3-OPT-UG1": {
        "floor_id": "b1",
        "slice_mode": "single",
        "bbox_3d": [4.80, 1.80, 14.50, 7.10, -4.78, -0.45],
        "extra_boxes_3d": [[4.50, -7.60, 14.50, -4.20, -4.78, -1.50]],
        "pin_3d": [9.65, -2.10, 4.45],
        "camera": {"target": [7.50, -3.60, 2.00], "radius": 25.0, "phi": 0.50, "theta": 1.25},
        "callout_he": "💰 חיסכון מאומת 157,500 ₪ במרתף 1-: מאגר מים תחת רמפה עליונה (H≥2.20m) + גיזום כיס דרום-מזרחי מחוץ ל-R=369 (-45 מ״ר)",
        "category_3d": "VE_UG",
    },
    "FB3-OPT-UG2": {
        "floor_id": "b2",
        "slice_mode": "single",
        "bbox_3d": [-11.50, 2.10, 2.20, 7.10, -7.78, -5.10],
        "extra_boxes_3d": [[-9.50, -7.60, 2.20, -4.20, -7.78, -5.50]],
        "pin_3d": [-4.65, -5.80, 4.60],
        "camera": {"target": [-3.50, -6.80, 2.50], "radius": 25.0, "phi": 0.50, "theta": 1.57},
        "callout_he": "💰 חיסכון מאומת 175,000 ₪ במרתף 2-: נסיגת רצועת דיפון דרומית-מרכזית מתה בין חניה #12 ל-#13 מחוץ ל-R500 (-50 מ״ר)",
        "category_3d": "VE_UG",
    },
    "FEIERBERG3-VE-FAC-1": {
        "floor_id": "all",
        "slice_mode": "cumulative",
        "bbox_3d": [-13.15, 4.00, 13.15, 5.85, 3.50, 35.00],
        "pin_3d": [0.00, 19.50, 6.10],
        "camera": {"target": [0.0, 17.5, 2.5], "radius": 44.0, "phi": 1.02, "theta": 1.57},
        "callout_he": "🏛️ חזית דרומית ראשית (רחוב פאירברג 3): שימור 670 מ״ר חיפוי אבן נסורה לבנה ומסגרות כהות (0 ₪ פגיעה בחזית הרחוב)",
        "category_3d": "VE_FAC_KEEP",
    },
    "FEIERBERG3-VE-FAC-2": {
        "floor_id": "all",
        "slice_mode": "cumulative",
        "bbox_3d": [-13.15, -4.45, 13.15, -3.95, 3.50, 35.00],
        "pin_3d": [0.00, 19.50, -4.75],
        "camera": {"target": [0.0, 17.5, -2.5], "radius": 44.0, "phi": 1.02, "theta": -1.57},
        "callout_he": "💰 חזית צפונית עורפית: חיסכון 291,200 ₪ (המרת 728 מ״ר חיפוי קשיח בהגשה לטיח חוץ אקרילי)",
        "category_3d": "VE_FAC_SAVE",
    },
    "FEIERBERG3-VE-FAC-3": {
        "floor_id": "all",
        "slice_mode": "cumulative",
        "bbox_3d": [-13.35, -4.25, -12.85, 4.25, 3.50, 35.00],
        "pin_3d": [-13.65, 19.50, 0.00],
        "camera": {"target": [-10.0, 17.5, 0.0], "radius": 40.0, "phi": 1.02, "theta": 3.10},
        "callout_he": "💰 חזית צד מערבית: חיסכון 83,600 ₪ (המרת 209 מ״ר חיפוי קשיח בהגשה לטיח חוץ אקרילי)",
        "category_3d": "VE_FAC_SAVE",
    },
    "FEIERBERG3-VE-FAC-4": {
        "floor_id": "all",
        "slice_mode": "cumulative",
        "bbox_3d": [12.85, -4.25, 13.35, 4.25, 3.50, 35.00],
        "pin_3d": [13.65, 19.50, 0.00],
        "camera": {"target": [10.0, 17.5, 0.0], "radius": 40.0, "phi": 1.02, "theta": 0.05},
        "callout_he": "💰 חזית צד מזרחית: חיסכון 81,200 ₪ (המרת 203 מ״ר חיפוי קשיח בהגשה לטיח חוץ אקרילי)",
        "category_3d": "VE_FAC_SAVE",
    },
    "FB3-LOCKED-CORE1": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [0.42, -2.00, 4.18, -0.20, 12.98, 15.60],
        "pin_3d": [2.30, 14.85, -1.10],
        "camera": {"target": [2.30, 13.75, -1.10], "radius": 13.5, "phi": 0.48, "theta": 1.57},
        "callout_he": "🔄 נישת מבואה דרומית כלואה בין עמודי הגרעין והממ״ד (19.6 מ״ר · 0 ₪ שלד) ← הועברה לשיפור תכנון והרחבת מבואות הדירות",
        "category_3d": "LOCKED_CORE",
    },
    "FB3-OPT-APT1": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-10.95, -1.35, -1.80, 0.45, 12.98, 15.55],
        "pin_3d": [-6.40, 14.85, -0.15],
        "camera": {"target": [-6.40, 13.75, -0.15], "radius": 14.5, "phi": 0.48, "theta": 1.57},
        "callout_he": "🛋️ שיפור תכנון דירה 1 (+1.1 מ״ר לדירה · +8.8 מ״ר ב-8 דירות): נישת ארון קו-אפס במחיצה הפנימית וקיצור קצה המסדרון מעבר לדלת האמבטיה הכללית",
        "category_3d": "APT_IMP",
        "before_after_scene": "fb3_apt1_corridor_fix",
    },
    "FB3-OPT-APT2": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [4.35, -1.35, 10.15, 0.45, 12.98, 15.55],
        "pin_3d": [7.25, 14.85, -0.35],
        "camera": {"target": [7.25, 13.75, -0.35], "radius": 14.0, "phi": 0.48, "theta": 1.57},
        "callout_he": "🛋️ שיפור תכנון דירה 2 (+1.0 מ״ר לדירה · +8.0 מ״ר ב-8 דירות): נישת ארון קו-אפס והזזת דלת סוויטת ההורים מעבר לקו דלת האמבטיה הכללית",
        "category_3d": "APT_IMP",
        "before_after_scene": "fb3_apt2_corridor_fix",
    },
    "FB3-OPT-APT3": {
        "floor_id": "f10",
        "slice_mode": "single",
        "bbox_3d": [-7.30, -2.20, -3.50, 0.70, 32.05, 34.80],
        "extra_boxes_3d": [[4.40, -2.20, 8.60, 0.70, 32.05, 34.80]],
        "pin_3d": [-5.40, 34.10, -0.75],
        "camera": {"target": [0.00, 33.10, -0.75], "radius": 17.5, "phi": 0.50, "theta": 1.57},
        "callout_he": "🛋️ שיפור תכנון דופלקסים קומה 10 (+2.1 מ״ר לדופלקס · +4.2 מ״ר סה״כ): הידוק גלריית המעבר העליונה להגדלת סוויטות ההורים",
        "category_3d": "APT_IMP",
        "before_after_scene": "fb3_f10_gallery_fix",
    },
}


# =============================================================================
# 3. EXACT 1:1 METRIC CAD 3D COORDINATES FOR YATKOVSKI 7 (האחים יטקובסקי 7)
# =============================================================================
# Coordinate convention in yatkovski7_3d_model.html & yatkovski7_extracted_plans.json:
#   - Building Typical Envelope (f1..f4): X in [-8.14, +6.60], Z (CAD Y) in [-6.10, +16.20]
#   - Floor IDs & Elevations in yatkovski7_3d_model.html (`FLOORS`):
#       * mar (Basement):   zFloor = -4.38, zCeil = -0.25
#       * kar (Ground):     zFloor =  0.00, zCeil =  3.60
#       * f4  (Typical):    zFloor = 13.30, zCeil = 16.28
#       * f5  (Mini-PH):    zFloor = 16.53, zCeil = 19.51
#       * f6  (Penthouse):  zFloor = 19.76, zCeil = 22.74
YATKOVSKI7_SPATIAL_3D = {
    "YAT-N-01": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-1.80, -5.60, 3.20, -0.80, 13.33, 16.20],
        "extra_boxes_3d": [[-3.60, -7.40, 1.20, -5.00, 13.33, 14.50]],
        "pin_3d": [0.50, 15.40, -3.20],
        "camera": {"target": [0.20, 14.30, -3.50], "radius": 15.5, "phi": 0.54, "theta": -1.57},
        "callout_he": "✓ דירה צפונית (97 מ״ר): סלון ופינת אוכל (410×460 ס״מ) + מרפסת סוכה צפונית",
        "category_3d": "PASS",
    },
    "YAT-N-02": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [3.20, -1.80, 6.60, 2.20, 13.33, 16.20],
        "pin_3d": [5.10, 15.40, 0.20],
        "camera": {"target": [4.80, 14.30, 0.20], "radius": 14.0, "phi": 0.52, "theta": 0.25},
        "callout_he": "✓ דירה צפונית: סוויטת הורים מזרחית מבודדת אקוסטית (340×360 ס״מ = 12.24 מ״ר)",
        "category_3d": "PASS",
    },
    "YAT-N-03": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-7.80, -4.60, -4.40, -1.60, 13.33, 16.20],
        "pin_3d": [-6.10, 15.40, -3.10],
        "camera": {"target": [-5.80, 14.30, -3.00], "radius": 14.0, "phi": 0.52, "theta": -2.45},
        "callout_he": "✓ דירה צפונית: מטבח מערבי מאוורר (310×290 ס״מ = 8.99 מ״ר) עם חלון חוץ ישיר",
        "category_3d": "PASS",
    },
    "YAT-N-04": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-7.80, -1.60, -3.80, 1.50, 13.33, 16.20],
        "pin_3d": [-5.80, 15.40, -0.05],
        "camera": {"target": [-5.50, 14.30, -0.05], "radius": 14.5, "phi": 0.52, "theta": -2.20},
        "callout_he": "⚠️ דירה צפונית: חדר שינה צפון-מערבי (295×340 ס״מ = 10.03 מ״ר) וחדר רחצה ראשי (260×210 ס״מ)",
        "category_3d": "WARN",
    },
    "YAT-N-05": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-7.80, 1.50, -4.20, 4.50, 13.33, 16.20],
        "pin_3d": [-6.00, 15.40, 3.00],
        "camera": {"target": [-5.60, 14.30, 3.00], "radius": 14.0, "phi": 0.52, "theta": 2.45},
        "callout_he": "✓ דירה צפונית: ממ״ד מערבי תקני ומרווח (335×290 ס״מ = 9.72 מ״ר נטו — עובר פקע״ר!)",
        "category_3d": "PASS",
    },
    "YAT-S-01": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-6.80, 9.20, -0.80, 14.35, 13.33, 16.20],
        "extra_boxes_3d": [[-6.80, 14.35, -0.50, 16.15, 13.33, 14.50]],
        "pin_3d": [-3.80, 15.40, 12.00],
        "camera": {"target": [-3.80, 14.30, 11.50], "radius": 16.0, "phi": 0.55, "theta": 1.85},
        "callout_he": "✓ דירה דרומית (102 מ״ר): סלון שטוף שמש (420×460 ס״מ), פינת אוכל (310×260) ומרפסת דרומית (680×180)",
        "category_3d": "PASS",
    },
    "YAT-S-03": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-7.80, 5.20, -4.20, 9.20, 13.33, 16.20],
        "pin_3d": [-6.00, 15.40, 7.20],
        "camera": {"target": [-5.60, 14.30, 7.20], "radius": 14.0, "phi": 0.52, "theta": 2.15},
        "callout_he": "✓ דירה דרומית: מטבח מערבי רחב ומואר (340×310 ס״מ = 10.54 מ״ר · מעבר 130 ס״מ)",
        "category_3d": "PASS",
    },
    "YAT-S-02": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-0.80, 10.20, 3.60, 14.35, 13.33, 16.20],
        "pin_3d": [1.40, 15.40, 12.20],
        "camera": {"target": [1.20, 14.30, 11.80], "radius": 14.5, "phi": 0.52, "theta": 1.25},
        "callout_he": "✓ דירה דרומית: סוויטת הורים דרום-מזרחית שקטה (340×360 ס״מ = 12.24 מ״ר — עוברת ADG!)",
        "category_3d": "PASS",
    },
    "YAT-S-04": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [0.20, 7.10, 3.60, 10.20, 13.33, 16.20],
        "pin_3d": [1.90, 15.40, 8.65],
        "camera": {"target": [1.60, 14.30, 8.65], "radius": 14.0, "phi": 0.52, "theta": 0.95},
        "callout_he": "⚠️ דירה דרומית: חדר שינה דרום-מזרחי (290×340 ס״מ = 9.86 מ״ר) ← הרחבה ל-304 ס״מ ע״י קיצור המסדרון",
        "category_3d": "WARN",
    },
    "YAT-S-05": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-1.80, 4.80, 3.60, 7.80, 13.33, 16.20],
        "pin_3d": [0.90, 15.40, 6.30],
        "camera": {"target": [0.80, 14.30, 6.30], "radius": 14.0, "phi": 0.50, "theta": 1.15},
        "callout_he": "⚠️ דירה דרומית: ממ״ד מזרחי (335×290 ס״מ = 9.72 מ״ר) ומסדרון (395×105 ס״מ) ← גומחה שקועה לדלת הדף",
        "category_3d": "WARN",
    },
    "YAT-CORE-01": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-3.05, -1.03, 2.95, 4.40, 13.33, 16.20],
        "pin_3d": [-0.50, 15.40, 1.80],
        "camera": {"target": [-0.50, 14.30, 1.80], "radius": 14.5, "phi": 0.50, "theta": 1.57},
        "callout_he": "✓ לובי קומתי בוטיק מוגן (260×380 ס״מ), מעלית וחדר מדרגות: מוגן 100% מקיטון (מבחן 7 — 0 מ״ר גריעה!)",
        "category_3d": "PASS",
    },
    "YAT-PH-01": {
        "floor_id": "f5",
        "slice_mode": "single",
        "bbox_3d": [-7.80, -3.80, 6.40, 14.30, 16.56, 19.45],
        "pin_3d": [-2.50, 18.70, 3.50],
        "camera": {"target": [-1.50, 17.60, 4.00], "radius": 22.0, "phi": 0.56, "theta": 1.57},
        "callout_he": "⚠️ קומה ה׳ — מיני-פנטהאוז #10 (150+64 מ״ר): סלון פנורמי (560×480), מרפסות גג ומטבח שף + אי (מעבר 105 ← 115 ס״מ)",
        "category_3d": "WARN",
    },
    "YAT-PH-02": {
        "floor_id": "f6",
        "slice_mode": "single",
        "bbox_3d": [-7.80, -3.80, 3.50, 5.50, 19.80, 22.70],
        "pin_3d": [-1.80, 21.90, 0.80],
        "camera": {"target": [-1.50, 20.80, 1.00], "radius": 20.0, "phi": 0.56, "theta": -1.57},
        "callout_he": "✓ קומה ו׳ — פנטהאוז #11 (125+52 מ״ר): סלון פנורמי (540×460 ס״מ), מטבח שף ומרפסות גג היקפיות (52 מ״ר)",
        "category_3d": "PASS",
    },
    "YAT-PH-03": {
        "floor_id": "f6",
        "slice_mode": "single",
        "bbox_3d": [-7.80, 5.50, 3.60, 14.30, 19.80, 22.70],
        "pin_3d": [-1.50, 21.90, 9.80],
        "camera": {"target": [-1.50, 20.80, 9.50], "radius": 19.0, "phi": 0.54, "theta": 1.57},
        "callout_he": "✓ קומה ו׳ — פנטהאוז #11: סוויטת הורים נשיאותית (350×410 ס״מ = 14.35 מ״ר), ממ״ד וחדרי שינה (320×330 ס״מ)",
        "category_3d": "PASS",
    },
    "YAT-GND-01": {
        "floor_id": "kar",
        "slice_mode": "single",
        "bbox_3d": [-7.80, 5.00, 3.40, 16.80, 0.03, 3.55],
        "pin_3d": [-2.40, 2.75, 11.50],
        "camera": {"target": [-2.20, 1.60, 11.00], "radius": 20.0, "phi": 0.56, "theta": 1.65},
        "callout_he": "✓ קומת קרקע: דירת גן #1 (105 מ״ר) עם גינה פרטית היקפית של 153 מ״ר",
        "category_3d": "PASS",
    },
    "YAT-BSM-01": {
        "floor_id": "mar",
        "slice_mode": "single",
        "bbox_3d": [-11.15, -10.90, 6.30, 19.00, -4.35, -0.30],
        "pin_3d": [-2.20, -1.80, 11.50],
        "camera": {"target": [-2.20, -3.20, 6.00], "radius": 28.0, "phi": 0.52, "theta": 1.57},
        "callout_he": "✓ מרתף חניון (-4.38m): 12 חניות תת-קרקעיות רגילות ל-11 דירות ומיסעה דו-סטרית 6.02 מ׳",
        "category_3d": "PASS",
    },
    "Y7-OPT-AG1": {
        "floor_id": "kar",
        "slice_mode": "single",
        "bbox_3d": [-6.25, -4.15, 6.35, 1.20, 0.03, 3.55],
        "pin_3d": [0.50, 2.75, -1.80],
        "camera": {"target": [0.00, 1.60, -1.50], "radius": 18.0, "phi": 0.54, "theta": -1.57},
        "callout_he": "💰 חיסכון מאומת 111,600 ₪ בקומת הקרקע: צמצום 18.0 מ״ר קונטור עילי בחדרי השירות",
        "category_3d": "VE_AG",
    },
    "Y7-OPT-AG2": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-3.05, -1.03, 2.95, 4.40, 13.33, 16.20],
        "pin_3d": [-0.50, 15.40, 1.80],
        "camera": {"target": [-0.50, 14.30, 1.80], "radius": 14.5, "phi": 0.50, "theta": 1.57},
        "callout_he": "💰 חיסכון מאומת 74,400 ₪: הידוק בליטות פיר מערכות וחדר יציאה לגג (-12.0 מ״ר בנוי עילי · 0 מ״ר קיטון בלובי הקומתי!)",
        "category_3d": "VE_AG",
    },
    "Y7-OPT-UG1": {
        "floor_id": "mar",
        "slice_mode": "single",
        "bbox_3d": [-11.15, -10.90, 6.30, -4.50, -4.35, -0.30],
        "pin_3d": [-2.50, -1.80, -7.20],
        "camera": {"target": [-2.50, -3.20, -6.00], "radius": 22.0, "phi": 0.50, "theta": -1.57},
        "callout_he": "💰 חיסכון מאומת 140,000 ₪ במרתף: ניצול תחתית רמפה מערבית (H≥2.15m) וצמצום 40 מ״ר דיפון צפוני",
        "category_3d": "VE_UG",
    },
    "YATKOVSKI7-VE-FAC-1": {
        "floor_id": "all",
        "slice_mode": "cumulative",
        "bbox_3d": [-7.80, -6.50, 6.60, -3.80, 0.00, 23.00],
        "pin_3d": [-0.60, 13.50, -6.80],
        "camera": {"target": [-0.60, 11.50, -2.00], "radius": 34.0, "phi": 1.02, "theta": -1.57},
        "callout_he": "🏛️ חזית צפונית ראשית (רחוב האחים יטקובסקי 7): שימור 142 מ״ר חיפוי קשיח מתכנית ההגשה",
        "category_3d": "VE_FAC_KEEP",
    },
    "YATKOVSKI7-VE-FAC-2": {
        "floor_id": "all",
        "slice_mode": "cumulative",
        "bbox_3d": [-7.80, 14.00, 3.60, 16.20, 0.00, 23.00],
        "pin_3d": [-2.10, 13.50, 16.50],
        "camera": {"target": [-2.10, 11.50, 10.00], "radius": 34.0, "phi": 1.02, "theta": 1.57},
        "callout_he": "✓ חזית דרומית עורפית: כבר מתוכננת ב-100% טיח חוץ בתכנית ההגשה (174 מ״ר טיח)",
        "category_3d": "VE_FAC_KEEP",
    },
    "YATKOVSKI7-VE-FAC-3": {
        "floor_id": "all",
        "slice_mode": "cumulative",
        "bbox_3d": [-8.20, -6.00, -7.50, 14.50, 0.00, 23.00],
        "pin_3d": [-8.50, 13.50, 4.20],
        "camera": {"target": [-5.00, 11.50, 4.20], "radius": 34.0, "phi": 1.02, "theta": 3.10},
        "callout_he": "💰 חזית צד מערבית: חיסכון 47,200 ₪ (המרת 118 מ״ר חיפוי קשיח בהגשה לטיח חוץ)",
        "category_3d": "VE_FAC_SAVE",
    },
    "YATKOVSKI7-VE-FAC-4": {
        "floor_id": "all",
        "slice_mode": "cumulative",
        "bbox_3d": [3.20, -4.20, 6.65, 14.50, 0.00, 23.00],
        "pin_3d": [6.90, 13.50, 4.20],
        "camera": {"target": [3.00, 11.50, 4.20], "radius": 34.0, "phi": 1.02, "theta": 0.05},
        "callout_he": "💰 חזית צד מזרחית: חיסכון 48,800 ₪ (המרת 122 מ״ר חיפוי קשיח בהגשה לטיח חוץ)",
        "category_3d": "VE_FAC_SAVE",
    },
    "Y7-LOCKED-CORE1": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-3.05, 0.80, -0.90, 2.95, 13.33, 16.20],
        "pin_3d": [-1.95, 15.40, 1.85],
        "camera": {"target": [-1.95, 14.30, 1.85], "radius": 13.5, "phi": 0.48, "theta": 1.57},
        "callout_he": "🔄 נישת גרעין פנימית כלואה (10.8 מ״ר · 0 ₪ שלד) ← הועברה לשיפור תכנון והרחבת מבואות הכניסה",
        "category_3d": "LOCKED_CORE",
    },
    "Y7-OPT-APT1": {
        "floor_id": "f4",
        "slice_mode": "single",
        "bbox_3d": [-4.50, -1.80, 2.80, 0.40, 13.33, 16.10],
        "extra_boxes_3d": [[-3.80, 7.20, 1.20, 11.20, 13.33, 16.10]],
        "pin_3d": [-1.20, 15.40, -0.70],
        "camera": {"target": [-1.20, 14.30, 4.50], "radius": 16.5, "phi": 0.50, "theta": 1.57},
        "callout_he": "🛋️ שיפור תכנון פנים-דירתי (+1.4 מ״ר לדירה · +12.6 מ״ר ב-9 דירות): קיצור זנב המסדרון להרחבת חדרי השינה",
        "category_3d": "APT_IMP",
    },
}


def _infer_generic_spatial_3d(note):
    """
    Fallback 3D coordinate mapper for projects without explicit 1:1 room tables,
    mapping sheet_id + (x_pct, y_pct, w_pct, h_pct) to metric coordinates.
    """
    sheet_id = (note.get("sheet_id") or "").lower()
    if "basement2" in sheet_id or "b2" in sheet_id:
        floor_id = "b2"
        z0, z1 = -7.8, -5.05
    elif "basement1" in sheet_id or "b1" in sheet_id:
        floor_id = "b1"
        z0, z1 = -4.8, -0.25
    elif "basement" in sheet_id or "bsm" in sheet_id:
        floor_id = "mar"
        z0, z1 = -5.0, -2.3
    elif "ground" in sheet_id or "gnd" in sheet_id:
        floor_id = "kar"
        z0, z1 = 0.05, 3.1
    elif "floor10" in sheet_id or "f10" in sheet_id:
        floor_id = "f10"
        z0, z1 = 32.02, 34.97
    elif "floor9" in sheet_id or "f9" in sheet_id or "penthouse" in sheet_id or "ph" in sheet_id or "f6" in sheet_id or "f7" in sheet_id or "floor5" in sheet_id:
        floor_id = "f9"
        z0, z1 = 28.87, 31.82
    elif "roof" in sheet_id or "gag" in sheet_id:
        floor_id = "gag"
        z0, z1 = 32.16, 35.16
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
        "callout_he": f"#{note.get('pin_num')}: {note.get('room_name', '')} — {note.get('title', '')}",
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

    project_spatial_map = {
        "hafetz44": HAFETZ44_SPATIAL_3D,
        "feierberg3": FEIERBERG3_SPATIAL_3D,
        "yatkovski7": YATKOVSKI7_SPATIAL_3D,
    }.get(pid)

    for note in payload.get("notes", []):
        nid = note.get("id", "")
        if project_spatial_map and nid in project_spatial_map:
            note["spatial_3d"] = dict(project_spatial_map[nid])
        elif "spatial_3d" not in note:
            note["spatial_3d"] = _infer_generic_spatial_3d(note)

    return payload


def validate_project_spatial_catalog(payload):
    """
    Systemic Semantic-Coordinate Cataloging Validator (מנגנון בקרת קטלוג סמנטי-מרחבי):
    Verifies that every note's 2D room identity (`room_name` / `title`) matches its 3D
    `spatial_3d.callout_he` and `bbox_3d` location, preventing room swaps (e.g., Kitchen vs. Mamad)
    and ensuring atomic room-level cataloging.
    Returns a list of error strings (empty list == 100% valid).
    """
    errors = []
    EXCLUSIVE_ROOM_GROUPS = [
        ("kitchen", ["מטבח"]),
        ("mamad", ["ממ״ד", 'ממ"ד', "ממד"]),
        ("corridor", ["מסדרון"]),
        ("master_suite", ["סוויטת הורים", "יחידת הורים", "חדר הורים", "ח. הורים", "חדר שינה ראשי"]),
        ("living_room", ["סלון", "חלל מגורים", "חלל ציבורי", "פינת אוכל", "פ. אוכל"]),
    ]

    for note in payload.get("notes", []):
        if note.get("is_value_eng") or note.get("is_design_improvement"):
            continue
        nid = note.get("id", "")
        rname = note.get("room_name", "")
        s3d = note.get("spatial_3d") or {}
        callout = s3d.get("callout_he", "")
        callout_subject = callout.split("←")[0]
        bbox = s3d.get("bbox_3d")
        if not bbox or len(bbox) != 6:
            errors.append(f"{nid}: Missing or invalid 6-element bbox_3d")
            continue

        # Check exclusive room semantic consistency: if room_name is exclusively about Kitchen (and not Mamad),
        # callout_he must mention Kitchen and must NOT mention Mamad!
        rname_and_title = f"{rname} {note.get('title', '')}"
        for grp_name, kw_list in EXCLUSIVE_ROOM_GROUPS:
            in_room = any(k in rname for k in kw_list)
            other_kw_in_room = any(
                ok in rname_and_title
                for og, okl in EXCLUSIVE_ROOM_GROUPS
                if og != grp_name
                for ok in okl
            )
            if in_room and not other_kw_in_room:
                if not any(k in callout_subject for k in kw_list):
                    errors.append(
                        f"{nid}: Semantic mismatch — room_name='{rname}' is exclusively '{grp_name}', "
                        f"but spatial_3d.callout_he='{callout}' does not contain {kw_list}"
                    )
                for og, okl in EXCLUSIVE_ROOM_GROUPS:
                    if og != grp_name and any(ok in callout_subject for ok in okl):
                        errors.append(
                            f"{nid}: Cross-room swap detected — room_name='{rname}' is '{grp_name}', "
                            f"but spatial_3d.callout_he='{callout}' references '{og}'!"
                        )

    return errors
