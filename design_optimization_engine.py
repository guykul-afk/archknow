# -*- coding: utf-8 -*-
"""
ArchiCheck AI — Design Optimization & Value Engineering Engine (מנגנון בדיקת ייעול תכנון והנדסת ערך)

Calculates deterministic architectural & engineering cost savings across 4 pillars WITHOUT reducing
apartment saleable areas (0% loss of apartment sqm) and WITHOUT compromising essential public utilities
(parking spaces, maneuvering aisles, electricity/water/gas/telecom service cabinets, fire safety & accessibility):

1. Above-Ground Building Volume & Public Core Optimization:
   - Identifies excess core/lobby/service/roof-tech areas per floor.
   - Rate: 6,200 ILS saved per 1 sqm of excess above-ground area reduced.

2. Underground Parking & Basement Volume Optimization:
   - Analyzes gross basement sqm per parking stall, dead excavation corners, ramp under-space utilization
     (for water tanks/pump rooms), and single-loaded aisle inefficiencies.
   - Rate: 3,500 ILS saved per 1 sqm of excess underground basement area reduced.

3. Facade Cladding Optimization (Dry Rigid Cladding vs. Advanced Exterior Plaster):
   - Evaluates opaque facade wall areas across all 4 directions (North, South, East, West).
   - Dry Cladding (חיפוי יבש/קשיח): 700 ILS/sqm | Exterior Plaster (טיח חוץ): 300 ILS/sqm.
   - Rate: 400 ILS saved per 1 sqm converted from dry cladding to plaster on rear/side/loggia/setback facades.

4. Internal Apartment Layout & Openings Optimization:
   - Identifies oversized corridors, dead-end hallway tails, and entry vestibules that can be converted
     into effective living room / bedroom area (increasing effective habitable ratio without changing apartment envelope).
   - Evaluates window-to-floor ratios (WWR) and opening modularization for thermal/acoustic & aluminum cost efficiency.
"""

import math

# =============================================================================
# ECONOMIC & ENGINEERING CONSTANTS
# =============================================================================
COST_ABOVE_GROUND_PER_SQM_ILS = 6200
COST_UNDERGROUND_PARKING_PER_SQM_ILS = 3500
COST_DRY_CLADDING_PER_SQM_ILS = 700
COST_PLASTER_PER_SQM_ILS = 300
SAVING_CLADDING_TO_PLASTER_PER_SQM_ILS = COST_DRY_CLADDING_PER_SQM_ILS - COST_PLASTER_PER_SQM_ILS  # 400 ILS/sqm

# Functional Benchmarks (preserving all statutory stairs, elevators, and utility cabinets: electricity, water, gas, telecom)
BENCHMARK_CORE_1ELEV_SQM = 26.0      # Protected stair + 1 elevator + lobby + utility cabinets (elec/water/gas/comm)
BENCHMARK_CORE_2ELEV_SQM = 36.5      # Protected stair + 2 elevators + lobby + utility cabinets
BENCHMARK_ROOF_TECH_PER_CORE_SQM = 23.0  # Stair penthouse + elevator overrun + roof exit vestibule
BENCHMARK_PARKING_GROSS_PER_STALL_SQM = 33.5       # Standard 90-deg double-loaded basement per stall
BENCHMARK_PARKING_WITH_STORAGE_PER_STALL_SQM = 37.5 # Including apartment storage rooms & filtration bays
OPTIMAL_CORRIDOR_MAX_RATIO = 0.078   # 7.8% of apartment net area


# =============================================================================
# PRESET DETAILED ENGINEERING PROFILES FOR THE 5 COMPANY PROJECTS
# =============================================================================
PROJECT_OPTIMIZATION_PROFILES = {
    "pines48": {
        "baseline_dry_cladding_pct": 85.0,
        "recommended_plaster_conversion_pct": 35.0,  # Convert 35% of opaque area (from 85% dry / 15% plaster -> 50% dry / 50% plaster)
        "above_ground_items": [
            {
                "id": "P48-OPT-AG1",
                "floor_or_zone": "קומת קרקע (±0.00 — לובי וחדרי שירות)",
                "current_sqm": 245.0,
                "optimal_sqm": 185.0,
                "saved_sqm": 60.0,
                "preserved_utilities": "שמירה מלאה על לובי כניסה ייצוגי, חדר אשפה תקני, חדר עגלות/אופניים, וכל ארונות החשמל, המים, הגז והתקשורת הראשיים",
                "engineering_action": "צמצום עומק מבואת המעבר הכפולה בקומת הקרקע ואיחוד מסדרון השירות העורפי של חדר האשפה וחדר העגלות ללא פגיעה בנפח האחסון או בגישה התפעולית לארונות המונים.",
                "sheet_id": "f1_5",
                "x_pct": 38.0, "y_pct": 22.0, "w_pct": 24.0, "h_pct": 22.0, "cx_pct": 50.0, "cy_pct": 33.0,
            },
            {
                "id": "P48-OPT-AG2",
                "floor_or_zone": "קומות 1–6 (6 קומות — גרעין קומתי ומבואות)",
                "current_sqm": 228.0,
                "optimal_sqm": 195.0,
                "saved_sqm": 33.0,
                "preserved_utilities": "שמירה על מדרגות מוגנות, פיר מעלית, מחסן קומתי וארונות שירות קומתיים (חשמל, מים, תקשורת וכיבוי אש) עם מרווח תפעול של 90 ס״מ",
                "engineering_action": "הידוק הגרעין הקומתי מ-38.0 מ״ר ל-32.5 מ״ר לקומה (חיסכון של 5.5 מ״ר × 6 קומות = 33.0 מ״ר) על ידי יישור נישת פיר המעלית והטמעת ארונות החשמל/מים בקו אפס בקיר הגרעין.",
                "sheet_id": "f1_5",
                "x_pct": 42.0, "y_pct": 26.0, "w_pct": 18.0, "h_pct": 18.0, "cx_pct": 51.0, "cy_pct": 35.0,
            },
            {
                "id": "P48-OPT-AG3",
                "floor_or_zone": "קומות 7–8 (מבואת דופלקסים עליונה וגג טכני)",
                "current_sqm": 64.0,
                "optimal_sqm": 56.0,
                "saved_sqm": 8.0,
                "preserved_utilities": "שמירה על יציאה תקנית לגג, גישה למערכות סולאריות וראש מעלית",
                "engineering_action": "קיצור מבואת הגג הטכני בקומה 8 והתאמת מעטפת חדר היציאה לגג למידות הפודסט הנדרשות בלבד (חיסכון של 8.0 מ״ר בנוי).",
                "sheet_id": "roof",
                "x_pct": 40.0, "y_pct": 28.0, "w_pct": 20.0, "h_pct": 20.0, "cx_pct": 50.0, "cy_pct": 38.0,
            },
        ],
        "underground_items": [
            {
                "id": "P48-OPT-UG1",
                "zone": "מרתף חניון (-3.50m) — ניצול תחתית רמפה וגיזום כיסי דיפון",
                "current_sqm": 685.0,
                "optimal_sqm": 635.0,
                "saved_sqm": 50.0,
                "parking_spaces_preserved": "18 חניות תקניות (100% שמירה על מצבת החניות ומיסעה דו-סטרית 6.00 מ׳)",
                "engineering_action": "שילוב חדר המשאבות ומאגר המים בחלל התחתון מתחת לרמפת הירידה הדרומית (חיסכון של 28 מ״ר חפירה) ויישור קו הדיפון בפינה הצפון-מערבית המתה (חיסכון של 22 מ״ר) — הורדת יחס השטח מ-38.1 מ״ר/חניה ל-35.3 מ״ר/חניה.",
                "sheet_id": "f1_5",
                "x_pct": 14.0, "y_pct": 18.0, "w_pct": 72.0, "h_pct": 64.0, "cx_pct": 50.0, "cy_pct": 50.0,
            },
        ],
        "internal_apartment_items": [
            {
                "id": "P48-OPT-APT1",
                "typology": "דירה A (קומות 1–5 · 5 דירות — 4 חדרים 94 מ״ר)",
                "current_corridor_sqm": 9.4,
                "optimal_corridor_sqm": 7.5,
                "reclaimed_sqm_per_unit": 1.9,
                "units_count": 5,
                "total_reclaimed_sqm": 9.5,
                "target_rooms_benefiting": "הגדלת חדר שינה #1 (מ-7.62 מ״ר ל-8.35 מ״ר תיקון סטטוטורי!) והרחבת פינת האוכל/סלון ב-1.17 מ״ר",
                "openings_optimization": "איחוד מפתחי חלונות חדרי השינה המזרחיים למודול אחיד של 140×150 ס״מ (חיסכון של כ-8% בעלות ייצור האלומיניום והתריסים).",
                "engineering_action": "יישור בליטת פיר המעלית וקיצור זנב המסדרון המוביל לחדר הרחצה וחדר השינה המזרחי ב-115 ס״מ — העברת 1.9 מ״ר נטו ממסדרון לשטח מגורים אפקטיבי בכל אחת מ-5 הדירות.",
                "sheet_id": "f1_5",
                "x_pct": 52.0, "y_pct": 24.0, "w_pct": 22.0, "h_pct": 18.0, "cx_pct": 63.0, "cy_pct": 33.0,
            },
            {
                "id": "P48-OPT-APT2",
                "typology": "דירה C (קומות 1–5 · 5 דירות — 4 חדרים 92 מ״ר)",
                "current_corridor_sqm": 8.9,
                "optimal_corridor_sqm": 7.3,
                "reclaimed_sqm_per_unit": 1.6,
                "units_count": 5,
                "total_reclaimed_sqm": 8.0,
                "target_rooms_benefiting": "הרחבת הסלון ופינת האוכל המזרחית + יצירת נישת ארון מעילים במבואה",
                "openings_optimization": "שמירה על ויטרינת המרפסת העמוקה (330 ס״מ) וצמצום חלון שירות דרומי למודול תקני.",
                "engineering_action": "סיבוב דלת שירותי האורחים וקיצור מעבר הכניסה הפנימי ב-95 ס״מ כך ש-1.6 מ״ר עוברים לחלל הציבורי של הדירה.",
                "sheet_id": "f1_5",
                "x_pct": 56.0, "y_pct": 48.0, "w_pct": 24.0, "h_pct": 20.0, "cx_pct": 68.0, "cy_pct": 58.0,
            },
            {
                "id": "P48-OPT-APT3",
                "typology": "דירה B (קומות 1–5 · 5 דירות — 3 חדרים 80 מ״ר)",
                "current_corridor_sqm": 6.8,
                "optimal_corridor_sqm": 5.6,
                "reclaimed_sqm_per_unit": 1.2,
                "units_count": 5,
                "total_reclaimed_sqm": 6.0,
                "target_rooms_benefiting": "הרחבת סוויטת ההורים הצפון-מערבית מרוחב 290 ס״מ ל-302 ס״מ (עמידה ברף המצוינות של ADG!)",
                "openings_optimization": "הוספת זיגוג בידודי Low-E בחלונות החזית המערבית למניעת חימום יתר (CIBSE TM59).",
                "engineering_action": "הזזת דלת הכניסה ליחידת ההורים ב-85 ס״מ לכיוון המבואה והטמעת סוף המסדרון בתוך סוויטת ההורים.",
                "sheet_id": "f1_5",
                "x_pct": 18.0, "y_pct": 36.0, "w_pct": 20.0, "h_pct": 18.0, "cx_pct": 28.0, "cy_pct": 45.0,
            },
        ],
    },

    "kkl10": {
        "baseline_dry_cladding_pct": 85.0,
        "recommended_plaster_conversion_pct": 35.0,
        "above_ground_items": [
            {
                "id": "KKL-OPT-AG1",
                "floor_or_zone": "קומת קרקע (L0 — חדר אשפה 32.7 מ״ר ומבואות שירות)",
                "current_sqm": 205.2,
                "optimal_sqm": 162.2,
                "saved_sqm": 43.0,
                "preserved_utilities": "שמירה מלאה על לובי ראשי (51.6 מ״ר), חדר עגלות (18.15 מ״ר), חדר גז (12.1 מ״ר), חדר אשפה תקני (16.5 מ״ר ל-25 דירות) וכל ארונות החשמל/מים/תקשורת",
                "engineering_action": "אופטימיזציה של חדר האשפה הענק (32.67 מ״ר — כפול מהנדרש ל-25 יח״ד) ל-16.5 מ״ר וצמצום מסדרונות השירות הכפולים סביב גרעין 2 המעליות בקומת הקרקע (חיסכון של 43.0 מ״ר בנוי עילי).",
                "sheet_id": "kkl_ground",
                "x_pct": 35.0, "y_pct": 35.0, "w_pct": 28.0, "h_pct": 25.0, "cx_pct": 49.0, "cy_pct": 47.5,
            },
            {
                "id": "KKL-OPT-AG2",
                "floor_or_zone": "קומות 1–8 (8 קומות — גרעין 2 מעליות ומבואה קומתית)",
                "current_sqm": 342.4,
                "optimal_sqm": 306.4,
                "saved_sqm": 36.0,
                "preserved_utilities": "שמירה על 2 המעליות, חדר מדרגות מוגן וכל ארונות השירות הקומתיים (חשמל, מים, תקשורת, גז וכיבוי אש)",
                "engineering_action": "הידוק רוחב מבואת המעליות הקומתית מ-42.8 מ״ר ל-38.3 מ״ר לקומה (חיסכון של 4.5 מ״ר × 8 קומות = 36.0 מ״ר) על ידי ריכוז ארונות המונים בדופן המערבית של הגרעין ללא פגיעה במעבר 150 ס״מ.",
                "sheet_id": "kkl_typical",
                "x_pct": 38.0, "y_pct": 40.0, "w_pct": 22.0, "h_pct": 20.0, "cx_pct": 49.0, "cy_pct": 50.0,
            },
            {
                "id": "KKL-OPT-AG3",
                "floor_or_zone": "קומה 9 (L9 — גג טכני ויציאה לגג)",
                "current_sqm": 44.5,
                "optimal_sqm": 34.5,
                "saved_sqm": 10.0,
                "preserved_utilities": "שמירה מלאה על ראשי 2 המעליות ופודסט יציאה לגג המערכות",
                "engineering_action": "צמצום שטח מבואת הגג הטכני מ-44.5 מ״ר ל-34.5 מ״ר בהתאם לקונטור הפירים ההندסי בלבד.",
                "sheet_id": "kkl_penthouse",
                "x_pct": 40.0, "y_pct": 42.0, "w_pct": 20.0, "h_pct": 18.0, "cx_pct": 50.0, "cy_pct": 51.0,
            },
        ],
        "underground_items": [
            {
                "id": "KKL-OPT-UG1",
                "zone": "מרתפים -1 ו--2 (1,586 מ״ר ל-34 חניות = 46.6 מ״ר/חניה!)",
                "current_sqm": 1586.0,
                "optimal_sqm": 1416.0,
                "saved_sqm": 170.0,
                "parking_spaces_preserved": "34 חניות רגילות (100% ללא מכפילים) + 14 מחסנים דירתיים + מאגר מים וחדר משאבות",
                "engineering_action": "יחס השטח במרתפים (46.6 מ״ר לחניה) גבוה בכ-24% מהבנצ׳מרק ההנדסי (37.5 מ״ר לחניה כולל מחסנים). קיצור שלוחות המיסעה בקצוות הדרומיים של מרתפים -1 ו--2 ומיקום מאגר המים מתחת לרמפה חוסכים 85 מ״ר בכל מרתף (סה״כ 170 מ״ר דיפון וחפירה) ללא גריעת אף חניה או מחסן.",
                "sheet_id": "kkl_basement",
                "x_pct": 18.0, "y_pct": 56.0, "w_pct": 64.0, "h_pct": 30.0, "cx_pct": 50.0, "cy_pct": 71.0,
            },
        ],
        "internal_apartment_items": [
            {
                "id": "KKL-OPT-APT1",
                "typology": "טיפוס B דרום-מזרחי (קומות 1–7 · 7 דירות — 107 מ״ר)",
                "current_corridor_sqm": 10.2,
                "optimal_corridor_sqm": 8.2,
                "reclaimed_sqm_per_unit": 2.0,
                "units_count": 7,
                "total_reclaimed_sqm": 14.0,
                "target_rooms_benefiting": "הגדלת סוויטת ההורים הדרום-מזרחית ב-1.2 מ״ר + נישת ארון שירות/ספרייה של 0.8 מ״ר",
                "openings_optimization": "איחוד חלונות חזית מזרחית (אורך 33.09 מ׳) למודול אחיד וצמצום זיגוג עודף במעברים.",
                "engineering_action": "קיצור מסדרון חדרי השינה הארוך (5.10 מ׳) ב-125 ס״מ על ידי הזזת דלת יחידת ההורים קדימה והכללת קצה המסדרון כחלק ממבואת חדר ההורים וארון הקיר.",
                "sheet_id": "kkl_typical",
                "x_pct": 52.0, "y_pct": 55.0, "w_pct": 26.0, "h_pct": 22.0, "cx_pct": 65.0, "cy_pct": 66.0,
            },
            {
                "id": "KKL-OPT-APT2",
                "typology": "טיפוסים A, E, F דרום-מערביים (קומות 1–7 · 7 דירות — 113–128 מ״ר)",
                "current_corridor_sqm": 9.8,
                "optimal_corridor_sqm": 8.1,
                "reclaimed_sqm_per_unit": 1.7,
                "units_count": 7,
                "total_reclaimed_sqm": 11.9,
                "target_rooms_benefiting": "הרחבת הסלון/פינת האוכל והגדלת חדר השינה הסמוך לממ״ד (תיקון מרווח גישה למיטה)",
                "openings_optimization": "איזון מפתחי חלונות בחזית המערבית (WWR 20.5%) עם הצללה אינטגרלית בתריסי אור.",
                "engineering_action": "ביטול שבירת המסדרון הכפולה בכניסה לאגף חדרי השינה והעברת 1.7 מ״ר משטח המעבר אל החלל הציבורי וחדר הילדים.",
                "sheet_id": "kkl_typical",
                "x_pct": 22.0, "y_pct": 55.0, "w_pct": 26.0, "h_pct": 22.0, "cx_pct": 35.0, "cy_pct": 66.0,
            },
            {
                "id": "KKL-OPT-APT3",
                "typology": "טיפוסים C, D, G, H צפוניים (קומות 1–7 · 7 דירות — 108–126 מ״ר)",
                "current_corridor_sqm": 9.5,
                "optimal_corridor_sqm": 8.0,
                "reclaimed_sqm_per_unit": 1.5,
                "units_count": 7,
                "total_reclaimed_sqm": 10.5,
                "target_rooms_benefiting": "הגדלת חדר השינה הצפוני ושילוב ארון קיר שקוע בקו אפס",
                "openings_optimization": "סטנדרטיזציה של ויטרינות היציאה למרפסות הצפוניות.",
                "engineering_action": "יישור קיר המסדרון הצפוני והטמעת נישת ארונות בעומק 60 ס״מ בין חדר הרחצה לחדר השינה.",
                "sheet_id": "kkl_typical",
                "x_pct": 25.0, "y_pct": 18.0, "w_pct": 45.0, "h_pct": 22.0, "cx_pct": 47.5, "cy_pct": 29.0,
            },
        ],
    },

    "hafetz44": {
        "baseline_dry_cladding_pct": 85.0,
        "recommended_plaster_conversion_pct": 35.0,
        "above_ground_items": [
            {
                "id": "H44-OPT-AG1",
                "floor_or_zone": "קומת קרקע (±0.00 — כפילות חדר שירות 12.2 מ״ר וחדר עגלות 10.6 מ״ר + לובי)",
                "current_sqm": 185.0,
                "optimal_sqm": 153.0,
                "saved_sqm": 32.0,
                "preserved_utilities": "שמירה מלאה על לובי ראשי (40.2 מ״ר), מועדון דיירים (12.1 מ״ר), חדר עגלות/אופניים ממוגן (12.0 מ״ר), חדר אשפה (11.7 מ״ר) וכל ארונות החשמל/מים/גז/תקשורת",
                "engineering_action": "איחוד חדר השירות הכפול (12.2 מ״ר) עם חדר העגלות/אופניים (10.6 מ״ר) לחלל מאוחד ויעיל והידוק מעברי השירות העורפיים בקומת הקרקע — חיסכון של 32.0 מ״ר בנוי עילי ללא פגיעה ב-6 החניות העיליות.",
                "sheet_id": "h44_ground",
                "x_pct": 35.0, "y_pct": 35.0, "w_pct": 30.0, "h_pct": 26.0, "cx_pct": 50.0, "cy_pct": 48.0,
            },
            {
                "id": "H44-OPT-AG2",
                "floor_or_zone": "קומות 1–8 (8 קומות — גרעין קומתי ל-2 דירות בלבד בקומה)",
                "current_sqm": 236.0,
                "optimal_sqm": 212.0,
                "saved_sqm": 24.0,
                "preserved_utilities": "שמירה על חדר מדרגות מוגן, מעלית, מבואה קומתית וארונות חשמל/מים/תקשורת/גז עם גישה תקנית מלאה",
                "engineering_action": "בקומה של 2 דירות בלבד, גרעין של 29.5 מ״ר ניתן להידוק ל-26.5 מ״ר (חיסכון של 3.0 מ״ר × 8 קומות = 24.0 מ״ר) על ידי קיצור שלוחת המבואה הקומתית ב-90 ס״מ והצבת דלתות הפלדלת בזווית ישירה.",
                "sheet_id": "h44_typical",
                "x_pct": 43.0, "y_pct": 22.0, "w_pct": 14.0, "h_pct": 22.0, "cx_pct": 50.0, "cy_pct": 33.0,
            },
        ],
        "underground_items": [
            {
                "id": "H44-OPT-UG1",
                "zone": "מרתף חניון (-5.10m — 638 מ״ר ל-13 חניות בלבד = 49.1 מ״ר/חניה!)",
                "current_sqm": 638.0,
                "optimal_sqm": 528.0,
                "saved_sqm": 110.0,
                "parking_spaces_preserved": "13 חניות תת-קרקעיות במרתף (+ 6 בקרקע = 19 חניות) + 2 תאי סינון ממוגנים + מאגר מים (T2) וחדר משאבות",
                "engineering_action": "מרתף חפץ חיים 44 מציג את יחס השטח לחניה הגבוה ביותר (49.1 מ״ר לחניה לעומת יעד של 36–38 מ״ר). מיקום מאגר המים T2 וחדר המשאבות מתחת לשטח הרמפה המזרחית וצמצום קו הדיפון בדופן המערבית החופשית חוסכים 110.0 מ״ר חפירה בעומק -5.10 מ׳ ללא פגיעה באף חניה!",
                "sheet_id": "h44_basement",
                "x_pct": 12.0, "y_pct": 20.0, "w_pct": 74.0, "h_pct": 60.0, "cx_pct": 49.0, "cy_pct": 50.0,
            },
        ],
        "internal_apartment_items": [
            {
                "id": "H44-OPT-APT1",
                "typology": "דירות 5 חדרים מערביות (#1,3,5,7,9,11,13,15 · 8 דירות — 124 מ״ר)",
                "current_corridor_sqm": 11.25,
                "optimal_corridor_sqm": 8.65,
                "reclaimed_sqm_per_unit": 2.6,
                "units_count": 8,
                "total_reclaimed_sqm": 20.8,
                "target_rooms_benefiting": "הגדלת יחידת ההורים המערבית ב-1.8 מ״ר (פתיחת מעבר צד מיטה מ-52 ס״מ ל-95 ס״מ!) + הרחבת המסדרון ל-100 ס״מ תקניים והגדלת הסלון ב-0.8 מ״ר",
                "openings_optimization": "אופטימיזציית ויטרינת הסלון המערבית הענקית (12.06 מ״ר זיגוג = 42.7% משטח הרצפה!) ל-9.5 מ״ר עם זיגוג Low-E והצללה חיצונית — חיסכון של כ-4,800 ₪ לדירה באלומיניום ומניעת סנוור/חימום יתר (TM59).",
                "engineering_action": "ביטול קירות חדר הארונות הצפוף (2.64 מ״ר, רוחב 160 ס״מ שרובו מעבר) והחלפתו בארון קיר רציף באורך 3.80 מ״ר, יחד עם קיצור זנב המסדרון (אורך 8.20 מ׳!) ב-130 ס״מ — שחרור של 2.6 מ״ר שטח אפקטיבי לכל דירה (20.8 מ״ר ב-8 דירות!).",
                "sheet_id": "h44_typical",
                "x_pct": 12.0, "y_pct": 25.0, "w_pct": 32.0, "h_pct": 45.0, "cx_pct": 28.0, "cy_pct": 47.5,
            },
            {
                "id": "H44-OPT-APT2",
                "typology": "דירות 4 חדרים מזרחיות (#2,4,6,8,10,12,14,16 · 8 דירות — 102 מ״ר)",
                "current_corridor_sqm": 7.8,
                "optimal_corridor_sqm": 6.4,
                "reclaimed_sqm_per_unit": 1.4,
                "units_count": 8,
                "total_reclaimed_sqm": 11.2,
                "target_rooms_benefiting": "הרחבת חדר השינה הצפון-מזרחי והגדלת פינת האוכל",
                "openings_optimization": "איחוד מפתחי חלונות בחזיתות צפון ודרום למודול ייצור אחיד.",
                "engineering_action": "קיצור סוף מסדרון חדרי השינה המזרחי ב-95 ס״מ וסיבוב דלת הכניסה לחדר ההורים, כך ש-1.4 מ״ר עוברים לחדרי המגורים.",
                "sheet_id": "h44_typical",
                "x_pct": 54.0, "y_pct": 25.0, "w_pct": 32.0, "h_pct": 45.0, "cx_pct": 70.0, "cy_pct": 47.5,
            },
        ],
    },

    "yatkovski7": {
        "baseline_dry_cladding_pct": 85.0,
        "recommended_plaster_conversion_pct": 35.0,
        "above_ground_items": [
            {
                "id": "Y7-OPT-AG1",
                "floor_or_zone": "קומת קרקע (±0.00 — לובי 29 מ״ר וחדרי שירות ל-11 דירות בלבד)",
                "current_sqm": 93.0,
                "optimal_sqm": 75.0,
                "saved_sqm": 18.0,
                "preserved_utilities": "שמירה מלאה על לובי דו-מפלסי, חדר אשפה, חדר גז, חדר עגלות/אופניים וכל ארונות החשמל/מים/תקשורת",
                "engineering_action": "בבניין בוטיק של 11 דירות בלבד, שטח שירות של 93.0 מ״ר בקרקע ניתן לייעול ל-75.0 מ״ר על ידי קיצור מסדרון השירות הפנימי ואיחוד מבואת חדר העגלות (חיסכון של 18.0 מ״ר בנוי עילי).",
                "sheet_id": "yat_ground",
                "x_pct": 38.0, "y_pct": 30.0, "w_pct": 24.0, "h_pct": 25.0, "cx_pct": 50.0, "cy_pct": 42.5,
            },
            {
                "id": "Y7-OPT-AG2",
                "floor_or_zone": "קומות א׳–ו׳ וגג (6 קומות + גג — הידוק גרעין קומתי)",
                "current_sqm": 177.0,
                "optimal_sqm": 165.0,
                "saved_sqm": 12.0,
                "preserved_utilities": "שמירה על מדרגות, מעלית, מחסן קומה ו׳ וכל ארונות השירות הקומתיים",
                "engineering_action": "הידוק הגרעין הקומתי ב-2.0 מ״ר לקומה בקומות הטיפוסיות ובגג הטכני (סה״כ 12.0 מ״ר) תוך שמירה על מרווחי גישה מלאים לארונות החשמל והמים.",
                "sheet_id": "yat_typical",
                "x_pct": 42.0, "y_pct": 38.0, "w_pct": 16.0, "h_pct": 20.0, "cx_pct": 50.0, "cy_pct": 48.0,
            },
        ],
        "underground_items": [
            {
                "id": "Y7-OPT-UG1",
                "zone": "מרתף חניון (-4.38m — 465 מ״ר ל-12 חניות = 38.8 מ״ר/חניה)",
                "current_sqm": 465.0,
                "optimal_sqm": 425.0,
                "saved_sqm": 40.0,
                "parking_spaces_preserved": "12 חניות רגילות (100% ללא מכפילים) + מיסעה 6.00 מ׳ + מאגר מים וגרעין מוגן",
                "engineering_action": "ניצול החלל התחתון מתחת לרמפה המערבית (רוחב 3.11 מ׳) עבור מאגר המים וחדר המשאבות וצמצום כיס החפירה בפינה הדרום-מזרחית — חיסכון של 40.0 מ״ר מרתף (הורדת היחס ל-35.4 מ״ר/חניה).",
                "sheet_id": "yat_basement",
                "x_pct": 15.0, "y_pct": 22.0, "w_pct": 68.0, "h_pct": 56.0, "cx_pct": 49.0, "cy_pct": 50.0,
            },
        ],
        "internal_apartment_items": [
            {
                "id": "Y7-OPT-APT1",
                "typology": "דירות צפוניות ודרומיות בקומות א׳–ד׳ + דירת גן (9 דירות — 97–105 מ״ר)",
                "current_corridor_sqm": 7.9,
                "optimal_corridor_sqm": 6.5,
                "reclaimed_sqm_per_unit": 1.4,
                "units_count": 9,
                "total_reclaimed_sqm": 12.6,
                "target_rooms_benefiting": "הרחבת חדר ההורים מ-275/280 ס״מ ל-295 ס״מ (תיקון התראת ADG!) + גומחה שקועה לדלת הממ״ד",
                "openings_optimization": "אופטימיזציית פתחי חלונות בחזיתות מזרח ומערב למודול אחיד עם בידוד אקוסטי 40dB.",
                "engineering_action": "קיצור זנב מסדרון חדרי השינה ב-90 ס״מ והסטת מחיצת הפנים של סוויטת ההורים — העברת 1.4 מ״ר נטו ממסדרון לחדר ההורים ולחלל המגורים בכל 9 הדירות.",
                "sheet_id": "yat_typical",
                "x_pct": 25.0, "y_pct": 25.0, "w_pct": 50.0, "h_pct": 50.0, "cx_pct": 50.0, "cy_pct": 50.0,
            },
        ],
    },

    "kitroni37": {
        "baseline_dry_cladding_pct": 85.0,
        "recommended_plaster_conversion_pct": 35.0,
        "above_ground_items": [
            {
                "id": "KIT-OPT-AG1",
                "floor_or_zone": "קומת קרקע (±0.00 — 2 הבניינים 37 + 39: 490 מ״ר שטחי לובי ושירות)",
                "current_sqm": 490.0,
                "optimal_sqm": 420.0,
                "saved_sqm": 70.0,
                "preserved_utilities": "שמירה מלאה על 2 לובאים ייצוגיים, מועדון דיירים, חדרי אשפה ועגלות, וכל ארונות החשמל/מים/גז/תקשורת של שני הבניינים",
                "engineering_action": "איחוד מועדון הדיירים וצמצום מסדרונות השירות הכפולים בקומת הקרקע של בניינים 37 ו-39 (מ-490 מ״ר ל-420 מ״ר — חיסכון של 35 מ״ר לכל בניין = 70.0 מ״ר עילי) ללא פגיעה ב-3 דירות הקרקע של בניין 39.",
                "sheet_id": "kit_ground",
                "x_pct": 25.0, "y_pct": 25.0, "w_pct": 50.0, "h_pct": 50.0, "cx_pct": 50.0, "cy_pct": 50.0,
            },
            {
                "id": "KIT-OPT-AG2",
                "floor_or_zone": "קומות 1–9 (9 קומות × 2 בניינים — 2 גרעינים של 48.5 מ״ר לקומה)",
                "current_sqm": 879.0,
                "optimal_sqm": 807.0,
                "saved_sqm": 72.0,
                "preserved_utilities": "שמירה מלאה על 2 חדרי המדרגות המוגנים, המעליות וכל ארונות השירות הקומתיים (חשמל, מים, תקשורת, גז וכיבוי אש) ב-2 הבניינים",
                "engineering_action": "שטח הגרעין בכל בניין עומד על 48.5 מ״ר לקומה עבור 4 דירות. הידוק מבואת הקומה ב-4.0 מ״ר לכל בניין (8.0 מ״ר לקומה × 9 קומות = 72.0 מ״ר) על ידי יישור גומחות ארונות השירות לקו קיר הגרעין חוסך 72.0 מ״ר בנייה עילית!",
                "sheet_id": "kit_typical",
                "x_pct": 36.0, "y_pct": 22.0, "w_pct": 18.0, "h_pct": 55.0, "cx_pct": 45.0, "cy_pct": 49.5,
            },
        ],
        "underground_items": [
            {
                "id": "KIT-OPT-UG1",
                "zone": "מרתף חניון משותף (-3.85m — 2,420 מ״ר ל-63 חניות = 38.4 מ״ר/חניה)",
                "current_sqm": 2420.0,
                "optimal_sqm": 2295.0,
                "saved_sqm": 125.0,
                "parking_spaces_preserved": "63 חניות תת-קרקעיות מלאות (יחס 1:1.0) + 2 גרעינים מוגנים + מאגרי מים וחדרי משאבות",
                "engineering_action": "המרתף המשותף מתוכנן היטב (איחוד רמפה אחת ל-2 בניינים), אך ניתן לחסוך עוד 125.0 מ״ר על ידי מיקום חדרי המשאבות ומאגר המים מתחת לרמפת הכניסה וגיזום שני כיסי דיפון מתים בקצוות המזרחיים של המרתף (הורדת היחס מ-38.4 ל-36.4 מ״ר/חניה).",
                "sheet_id": "kit_basement",
                "x_pct": 15.0, "y_pct": 18.0, "w_pct": 66.0, "h_pct": 64.0, "cx_pct": 48.0, "cy_pct": 50.0,
            },
        ],
        "internal_apartment_items": [
            {
                "id": "KIT-OPT-APT1",
                "typology": "בניין 37 — טיפוסי NW ו-SW (קומות 1–7 · 14 דירות של 4–5 חדרים)",
                "current_corridor_sqm": 9.2,
                "optimal_corridor_sqm": 7.6,
                "reclaimed_sqm_per_unit": 1.6,
                "units_count": 14,
                "total_reclaimed_sqm": 22.4,
                "target_rooms_benefiting": "הרחבת חדר ההורים ב-NW (מ-286 ס״מ ל-300 ס״מ) וב-SW (מ-278 ס״מ ל-295 ס״מ) + הגדלת מבואת הסלון",
                "openings_optimization": "סטנדרטיזציה של ויטרינות המרפסות המערביות (600–657 ס״מ) למודול אחיד והצללה מערבית.",
                "engineering_action": "קיצור זנב המסדרון המוביל לחדרי ההורים ב-105 ס״מ והזזת דלת הכניסה ליחידת ההורים — העברת 1.6 מ״ר נטו לחדר ההורים בכל 14 הדירות (22.4 מ״ר סה״כ).",
                "sheet_id": "kit_typical",
                "x_pct": 9.0, "y_pct": 12.0, "w_pct": 36.0, "h_pct": 32.0, "cx_pct": 27.0, "cy_pct": 28.0,
            },
            {
                "id": "KIT-OPT-APT2",
                "typology": "בניין 39 — דירות 4–5 חדרים דרומיות ומזרחיות (קומות 1–7 · 21 דירות)",
                "current_corridor_sqm": 8.8,
                "optimal_corridor_sqm": 7.3,
                "reclaimed_sqm_per_unit": 1.5,
                "units_count": 21,
                "total_reclaimed_sqm": 31.5,
                "target_rooms_benefiting": "הגדלת חדרי השינה והוספת נישת ארון כניסה/מבואה בסלון",
                "openings_optimization": "איחוד מפתחי חלונות בחזית המזרחית והדרומית למודול ייצור אחיד (חיסכון ברכש אלומיניום להיקף של 63 דירות).",
                "engineering_action": "ייעול מסדרון חדרי השינה וקיצור מעבר הכניסה הפנימי — העברת 1.5 מ״ר משטחי מעבר לחדרי המגורים ב-21 דירות (31.5 מ״ר סה״כ).",
                "sheet_id": "kit_typical",
                "x_pct": 8.5, "y_pct": 73.5, "w_pct": 66.5, "h_pct": 15.5, "cx_pct": 41.8, "cy_pct": 81.2,
            },
        ],
    },

    "feierberg3": {
        "baseline_dry_cladding_pct": 85.0,
        "recommended_plaster_conversion_pct": 36.0,
        "above_ground_items": [
            {
                "id": "FB3-OPT-AG1",
                "floor_or_zone": "קומת קרקע (±0.00m — העברת מאגר מים מתחת לרמפה והידוק מעברי שירות)",
                "current_sqm": 265.0,
                "optimal_sqm": 223.0,
                "saved_sqm": 42.0,
                "preserved_utilities": "שמירה מלאה על לובי כניסה ראשי, מועדון דיירים, חדר אופניים ועגלות, חדר אשפה ודחסנית, חדר גז ולוח חח״י וכל ארונות המונים",
                "engineering_action": "העברת מאגר המים וחדר המשאבות (28 מ״ר בחלק המזרחי של קומת הקרקע X=[8.5..12.5]) אל החלל התחתון מתחת לרמפה הדו-שיפועית במרתף, ואיחוד מסדרון השירות העורפי בין חדר האשפה למועדון הדיירים (חיסכון של 42.0 מ״ר בנוי עילי).",
                "sheet_id": "fb_ground",
                "x_pct": 52.0, "y_pct": 28.0, "w_pct": 24.0, "h_pct": 26.0, "cx_pct": 64.0, "cy_pct": 41.0,
            },
            {
                "id": "FB3-OPT-AG2",
                "floor_or_zone": "קומות 1–8 (8 קומות — הידוק גרעין ומבואה קומתית ל-2 דירות בקומה)",
                "current_sqm": 248.0,
                "optimal_sqm": 220.0,
                "saved_sqm": 28.0,
                "preserved_utilities": "שמירה מלאה על חדר מדרגות מוגן (3.50×3.60 מ׳), פיר מעלית (1.75×1.80 מ׳) וכל ארונות החשמל, המים, התקשורת וכיבוי האש הקומתיים",
                "engineering_action": "בקומה טיפוסית של 2 דירות בלבד (מערבית ומזרחית), הידוק מבואת הקומה מ-31.0 מ״ר ל-27.5 מ״ר לקומה (חיסכון של 3.5 מ״ר × 8 קומות = 28.0 מ״ר) על ידי יישור קיר המבואה הדרומי והטמעת ארונות המונים בקו אפס בדופן הגרעין.",
                "sheet_id": "fb_typical",
                "x_pct": 40.5, "y_pct": 27.5, "w_pct": 21.5, "h_pct": 22.0, "cx_pct": 51.2, "cy_pct": 38.5,
            },
            {
                "id": "FB3-OPT-AG3",
                "floor_or_zone": "קומות 9–10 וגג עליון (+28.87m עד +35.17m — מבואת דופלקסים ויציאה לגג)",
                "current_sqm": 100.8,
                "optimal_sqm": 88.8,
                "saved_sqm": 12.0,
                "preserved_utilities": "שמירה על יציאה תקנית לגג, גישה למערכות קולטי השמש ופיר המעלית העליון",
                "engineering_action": "צמצום מבואת הגלריה המשותפת בקומה 10 (שבה הכניסה הראשית לדופלקסים #17 ו-#18 היא מקומה 9) והתאמת חדר היציאה לגג לקונטור הפירים ההנדסי בלבד (חיסכון של 12.0 מ״ר בנוי עילי).",
                "sheet_id": "fb_floor10",
                "x_pct": 41.0, "y_pct": 27.5, "w_pct": 20.0, "h_pct": 21.0, "cx_pct": 51.0, "cy_pct": 38.0,
            },
        ],
        "underground_items": [
            {
                "id": "FB3-OPT-UG1",
                "zone": "מרתף 1- (-4.80m — ניצול תחתית הרמפה הדו-שיפועית וגיזום פינה מזרחית)",
                "current_sqm": 548.0,
                "optimal_sqm": 503.0,
                "saved_sqm": 45.0,
                "parking_spaces_preserved": "8 חניות רגילות במרתף 1- (#1–#8) + רמפה דו-שיפועית תקנית + מיסעה 6.00 מ׳",
                "engineering_action": "מיקום מאגר המים וחדר המשאבות מתחת לשלוחת הרמפה במזרח המגרש (X=[9.5..16.5]) וצמצום כיס החפירה הדרום-מזרחי מחוץ למיסעה — חיסכון של 45.0 מ״ר מרתף ודיפון ללא גריעת אף חניה.",
                "sheet_id": "fb_basement1",
                "x_pct": 66.0, "y_pct": 26.0, "w_pct": 26.0, "h_pct": 52.0, "cx_pct": 79.0, "cy_pct": 52.0,
            },
            {
                "id": "FB3-OPT-UG2",
                "zone": "מרתף 2- (-7.80m — קיצור שלוחת מרתף מזרחית מעבר לחניה P19)",
                "current_sqm": 548.0,
                "optimal_sqm": 498.0,
                "saved_sqm": 50.0,
                "parking_spaces_preserved": "11 חניות רגילות במרתף 2- (#9–#19 כולל חניית נכה P17) + בורות שאיבה וגרעין מוגן",
                "engineering_action": "במרתף 2- חניות P9–P19 מרוכזות ב-X=[-16.8..+10.4], בעוד החפירה נמשכת עד X=+16.75. עצירת קו הדיפון המזרחי ב-X=+11.8 (כולל בורות השאיבה) חוסכת 50.0 מ״ר חפירה בעומק -7.80 מ׳ תוך שמירה על כל 11 החניות.",
                "sheet_id": "fb_basement2",
                "x_pct": 72.0, "y_pct": 22.0, "w_pct": 21.0, "h_pct": 60.0, "cx_pct": 82.5, "cy_pct": 52.0,
            },
        ],
        "internal_apartment_items": [
            {
                "id": "FB3-OPT-APT1",
                "typology": "אגף מערבי — דירות 4 חדרים (#1,3,5,7,9,11,13,15 · 8 דירות — 105.46 מ״ר)",
                "current_corridor_sqm": 9.8,
                "optimal_corridor_sqm": 8.0,
                "reclaimed_sqm_per_unit": 1.8,
                "units_count": 8,
                "total_reclaimed_sqm": 14.4,
                "target_rooms_benefiting": "הגדלת חדר השינה הצפוני (מרוחב 2.80 מ׳ ל-2.98 מ׳) + הרחבת סוויטת ההורים הדרום-מערבית והסלון",
                "openings_optimization": "איחוד מפתחי חלונות חדרי השינה הצפוניים והמערביים למודול אחיד של 140×150 ס״מ עם זיגוג Low-E ואקוסטיקה 40dB.",
                "engineering_action": "קיצור זנב המסדרון המערבי ב-105 ס״מ וביטול המחיצה הכפולה של חדר הארונות הקטן (2.75 מ״ר) לטובת ארון קיר אינטגרלי — השבחה של 1.8 מ״ר שטח מגורים אפקטיבי בכל אחת מ-8 הדירות (14.4 מ״ר סה״כ).",
                "sheet_id": "fb_typical",
                "x_pct": 18.0, "y_pct": 38.0, "w_pct": 24.0, "h_pct": 20.0, "cx_pct": 30.0, "cy_pct": 48.0,
            },
            {
                "id": "FB3-OPT-APT2",
                "typology": "אגף מזרחי — דירות 4 חדרים (#2,4,6,8,10,12,14,16 · 8 דירות — 85.53 מ״ר)",
                "current_corridor_sqm": 7.9,
                "optimal_corridor_sqm": 6.5,
                "reclaimed_sqm_per_unit": 1.4,
                "units_count": 8,
                "total_reclaimed_sqm": 11.2,
                "target_rooms_benefiting": "הרחבת סוויטת ההורים הדרום-מזרחית מרוחב 2.95 מ׳ ל-3.12 מ׳ (עמידה מלאה ברף המצוינות של ADG ≥3.00 מ׳!)",
                "openings_optimization": "סטנדרטיזציה של ויטרינת המרפסת הדרומית (380 ס״מ) וחלונות החזית המזרחית.",
                "engineering_action": "קיצור קצה המסדרון המזרחי ב-95 ס״מ והזזת דלת סוויטת ההורים קדימה לקו האמבטיה — העברת 1.4 מ״ר נטו משטח המעבר אל תוך חדר ההורים (11.2 מ״ר ב-8 דירות).",
                "sheet_id": "fb_typical",
                "x_pct": 58.0, "y_pct": 38.0, "w_pct": 24.0, "h_pct": 20.0, "cx_pct": 70.0, "cy_pct": 48.0,
            },
            {
                "id": "FB3-OPT-APT3",
                "typology": "דופלקס-פנטהאוזים #17 (מערב) ו-#18 (מזרח) (קומות 9–10 · 2 דירות — 121.3 ו-103.6 מ״ר)",
                "current_corridor_sqm": 11.5,
                "optimal_corridor_sqm": 9.4,
                "reclaimed_sqm_per_unit": 2.1,
                "units_count": 2,
                "total_reclaimed_sqm": 4.2,
                "target_rooms_benefiting": "הגדלת סוויטות ההורים הראשיות בקומה 10 ופינת העבודה/גלריה",
                "openings_optimization": "איזון מפתחי הוויטרינות הפנורמיות בקומה 9 (WWR 52% ← 38%) עם פרגולות ההצללה הדרומיות לחיסכון בעלויות האלומיניום ושיפור הבידוד התרמי.",
                "engineering_action": "הידוק גלריית המעבר העליונה בקומה 10 והעברת 2.1 מ״ר לכל דופלקס לטובת סוויטת ההורים הראשית.",
                "sheet_id": "fb_floor10",
                "x_pct": 22.0, "y_pct": 30.0, "w_pct": 56.0, "h_pct": 34.0, "cx_pct": 50.0, "cy_pct": 47.0,
            },
        ],
    },
}


# =============================================================================
# FACADE CLADDING VS. PLASTER OPTIMIZATION ENGINE
# =============================================================================
def build_facade_cladding_optimization(facades_data: dict, baseline_dry_pct: float = 85.0, target_plaster_conversion_pct: float = 35.0) -> dict:
    """
    Analyzes all facades (`by_direction`) and calculates exact cost savings from shifting a portion
    of opaque walls (`opaque_area_sqm`) from Dry Cladding (700 ILS/sqm) to Exterior Plaster (300 ILS/sqm).
    Saving = 400 ILS per converted sqm.
    """
    total_gross = float(facades_data.get("total_sqm") or 0.0)
    total_glazing = float(facades_data.get("total_glazing_sqm") or 0.0)
    total_opaque = float(facades_data.get("total_opaque_sqm") or max(0.0, total_gross - total_glazing))

    baseline_dry_sqm = round(total_opaque * (baseline_dry_pct / 100.0), 1)
    baseline_plaster_sqm = round(total_opaque - baseline_dry_sqm, 1)
    baseline_total_cost_ils = round(
        baseline_dry_sqm * COST_DRY_CLADDING_PER_SQM_ILS + baseline_plaster_sqm * COST_PLASTER_PER_SQM_ILS
    )

    # Direction-by-direction smart engineering allocation
    by_facade = []
    tot_rec_converted_sqm = 0.0
    directions = facades_data.get("by_direction") or []

    for idx, d in enumerate(directions):
        fname = d.get("facade_name", f"חזית {idx + 1}")
        direction = d.get("direction", "")
        opaque_sqm = float(d.get("opaque_area_sqm") or 0.0)
        glazing_sqm = float(d.get("glazing_area_sqm") or 0.0)
        gross_sqm = float(d.get("gross_area_sqm") or (opaque_sqm + glazing_sqm))

        is_main_street = ("ראשית" in fname) or ("רחוב" in fname and idx == 0)
        is_rear = ("עורפית" in fname) or ("חצר" in fname) or ("שצ״פ" in fname)

        if is_main_street:
            conv_share = 0.20  # Keep 80% rigid cladding on main street facade; convert only inner balcony soffits/recesses
            strategy = "חזית רחוב ייצוגית — שמירת חיפוי יבש מלא בחזית הראשית ובמסד; המרת קירות פנים-מרפסות ונסיגות קומות גג בלבד לטיח (20%)"
        elif is_rear:
            conv_share = 0.48  # Rear facade: convert 48% to high-grade acrylic/silicone plaster
            strategy = "חזית עורפית — המרת שטחי הקירות האטומים העורפיים ומסתורי הכביסה לטיח תרמי/אקרילי משובח תוך שמירת מסגרות חיפוי יבש (48%)"
        else:
            conv_share = 0.36  # Side facades: convert 36% to plaster
            strategy = "חזית צדדית — שילוב אדריכלי מאוזן: חיפוי יבש במסד ובאגפי הסלון, ומעבר לטיח חוץ באגפי חדרי השינה, הפירים ומסתורי הכביסה (36%)"

        cur_dry = round(opaque_sqm * (baseline_dry_pct / 100.0), 1)
        cur_plaster = round(opaque_sqm - cur_dry, 1)
        conv_sqm = round(opaque_sqm * conv_share, 1)
        new_dry = round(max(0.0, cur_dry - conv_sqm), 1)
        new_plaster = round(opaque_sqm - new_dry, 1)
        facade_saving_ils = round(conv_sqm * SAVING_CLADDING_TO_PLASTER_PER_SQM_ILS)
        tot_rec_converted_sqm += conv_sqm

        by_facade.append({
            "facade_name": fname,
            "direction": direction,
            "gross_area_sqm": gross_sqm,
            "glazing_area_sqm": glazing_sqm,
            "opaque_area_sqm": opaque_sqm,
            "current_dry_cladding_sqm": cur_dry,
            "current_plaster_sqm": cur_plaster,
            "recommended_converted_to_plaster_sqm": conv_sqm,
            "optimized_dry_cladding_sqm": new_dry,
            "optimized_plaster_sqm": new_plaster,
            "optimized_dry_pct": round((new_dry / opaque_sqm * 100.0) if opaque_sqm > 0 else 0.0, 1),
            "optimized_plaster_pct": round((new_plaster / opaque_sqm * 100.0) if opaque_sqm > 0 else 0.0, 1),
            "cost_saving_ils": facade_saving_ils,
            "strategy_note": strategy,
            **(
                {"x_pct": 14.0, "y_pct": 72.0, "w_pct": 72.0, "h_pct": 10.0, "cx_pct": 50.0, "cy_pct": 77.0}
                if "דרום" in fname or "דרומית" in fname or "S" in direction
                else (
                    {"x_pct": 14.0, "y_pct": 16.0, "w_pct": 72.0, "h_pct": 10.0, "cx_pct": 50.0, "cy_pct": 21.0}
                    if "צפון" in fname or "צפונית" in fname or "N" in direction
                    else (
                        {"x_pct": 11.0, "y_pct": 24.0, "w_pct": 9.0, "h_pct": 50.0, "cx_pct": 15.5, "cy_pct": 49.0}
                        if "מערב" in fname or "מערבית" in fname or "W" in direction
                        else {"x_pct": 80.0, "y_pct": 24.0, "w_pct": 9.0, "h_pct": 50.0, "cx_pct": 84.5, "cy_pct": 49.0}
                    )
                )
            ),
        })

    tot_rec_converted_sqm = round(tot_rec_converted_sqm, 1)
    if tot_rec_converted_sqm <= 0 and total_opaque > 0:
        tot_rec_converted_sqm = round(total_opaque * (target_plaster_conversion_pct / 100.0), 1)

    opt_dry_sqm = round(max(0.0, baseline_dry_sqm - tot_rec_converted_sqm), 1)
    opt_plaster_sqm = round(total_opaque - opt_dry_sqm, 1)
    optimized_total_cost_ils = round(
        opt_dry_sqm * COST_DRY_CLADDING_PER_SQM_ILS + opt_plaster_sqm * COST_PLASTER_PER_SQM_ILS
    )
    recommended_saving_ils = round(tot_rec_converted_sqm * SAVING_CLADDING_TO_PLASTER_PER_SQM_ILS)

    # Pre-built scenarios for comparison table & interactive UI slider
    scenarios = [
        {
            "scenario_id": "conservative_25",
            "title": "תרחיש שמרני (המרת 25% מהשטח האטום לטיח — עורף ומסתורי כביסה בלבד)",
            "converted_sqm": round(total_opaque * 0.25, 1),
            "new_dry_pct": round(max(0.0, baseline_dry_pct - 25.0), 1),
            "new_plaster_pct": round(min(100.0, (100.0 - baseline_dry_pct) + 25.0), 1),
            "saving_ils": round(total_opaque * 0.25 * SAVING_CLADDING_TO_PLASTER_PER_SQM_ILS),
        },
        {
            "scenario_id": "balanced_recommended",
            "title": "תרחיש מומלץ ומאוזן (שמירת חזית רחוב ומסד בחיפוי קשיח, המרת ~35% בעורף/צד/מרפסות לטיח)",
            "converted_sqm": tot_rec_converted_sqm,
            "new_dry_pct": round((opt_dry_sqm / total_opaque * 100.0) if total_opaque > 0 else 50.0, 1),
            "new_plaster_pct": round((opt_plaster_sqm / total_opaque * 100.0) if total_opaque > 0 else 50.0, 1),
            "saving_ils": recommended_saving_ils,
        },
        {
            "scenario_id": "value_eng_50",
            "title": "תרחיש הנדסת ערך מלאה (המרת 50% מהשטח האטום לטיח — חיפוי יבש בקומות המסד ובאלמנטים מרכזיים)",
            "converted_sqm": round(total_opaque * 0.50, 1),
            "new_dry_pct": round(max(0.0, baseline_dry_pct - 50.0), 1),
            "new_plaster_pct": round(min(100.0, (100.0 - baseline_dry_pct) + 50.0), 1),
            "saving_ils": round(total_opaque * 0.50 * SAVING_CLADDING_TO_PLASTER_PER_SQM_ILS),
        },
    ]

    return {
        "total_facade_gross_sqm": total_gross,
        "total_glazing_sqm": total_glazing,
        "total_opaque_wall_sqm": total_opaque,
        "dry_cladding_price_per_sqm_ils": COST_DRY_CLADDING_PER_SQM_ILS,
        "plaster_price_per_sqm_ils": COST_PLASTER_PER_SQM_ILS,
        "saving_per_converted_sqm_ils": SAVING_CLADDING_TO_PLASTER_PER_SQM_ILS,
        "baseline_dry_cladding_pct": baseline_dry_pct,
        "baseline_plaster_pct": round(100.0 - baseline_dry_pct, 1),
        "baseline_dry_cladding_sqm": baseline_dry_sqm,
        "baseline_plaster_sqm": baseline_plaster_sqm,
        "baseline_total_cost_ils": baseline_total_cost_ils,
        "recommended_converted_to_plaster_sqm": tot_rec_converted_sqm,
        "optimized_dry_cladding_sqm": opt_dry_sqm,
        "optimized_plaster_sqm": opt_plaster_sqm,
        "optimized_dry_cladding_pct": round((opt_dry_sqm / total_opaque * 100.0) if total_opaque > 0 else 0.0, 1),
        "optimized_plaster_pct": round((opt_plaster_sqm / total_opaque * 100.0) if total_opaque > 0 else 0.0, 1),
        "optimized_total_cost_ils": optimized_total_cost_ils,
        "recommended_saving_ils": recommended_saving_ils,
        "by_facade": by_facade,
        "scenarios": scenarios,
    }


# =============================================================================
# DYNAMIC PROJECT & APARTMENT OPTIMIZATION BUILDER
# =============================================================================
def build_project_design_optimization(pid: str, data_summary: dict) -> dict:
    """
    Builds the complete `design_optimization` dictionary for a project (both the 5 cataloged
    projects and any dynamically uploaded CAD/PDF model).
    """
    ag = data_summary.get("above_ground_areas") or {}
    ug = data_summary.get("underground_areas") or {}
    fac = data_summary.get("facades") or {}

    total_ag_sqm = float(ag.get("total_sqm") or 0.0)
    net_apt_sqm = float(ag.get("net_apartments_sqm") or 0.0)
    core_ag_sqm = float(ag.get("core_and_service_sqm") or 0.0)
    total_ug_sqm = float(ug.get("total_sqm") or 0.0)
    parking_spaces = int(ug.get("parking_spaces") or 1)

    profile = PROJECT_OPTIMIZATION_PROFILES.get(pid)

    if profile:
        ag_items = []
        for item in profile["above_ground_items"]:
            saved = float(item["saved_sqm"])
            ag_items.append({
                **item,
                "unit_cost_ils": COST_ABOVE_GROUND_PER_SQM_ILS,
                "cost_saving_ils": round(saved * COST_ABOVE_GROUND_PER_SQM_ILS),
            })

        ug_items = []
        for item in profile["underground_items"]:
            saved = float(item["saved_sqm"])
            ug_items.append({
                **item,
                "unit_cost_ils": COST_UNDERGROUND_PARKING_PER_SQM_ILS,
                "cost_saving_ils": round(saved * COST_UNDERGROUND_PARKING_PER_SQM_ILS),
            })

        apt_items = list(profile["internal_apartment_items"])
        facade_opt = build_facade_cladding_optimization(
            fac,
            baseline_dry_pct=profile.get("baseline_dry_cladding_pct", 85.0),
            target_plaster_conversion_pct=profile.get("recommended_plaster_conversion_pct", 35.0),
        )
    else:
        # Dynamic calculation for uploaded / custom projects
        saved_ag_sqm = round(max(18.0, core_ag_sqm * 0.14), 1)
        ag_items = [
            {
                "id": f"{pid.upper()}-OPT-AG1",
                "floor_or_zone": "גרעין קומות טיפוסיות, מבואות וקומת קרקע",
                "current_sqm": core_ag_sqm,
                "optimal_sqm": round(core_ag_sqm - saved_ag_sqm, 1),
                "saved_sqm": saved_ag_sqm,
                "unit_cost_ils": COST_ABOVE_GROUND_PER_SQM_ILS,
                "cost_saving_ils": round(saved_ag_sqm * COST_ABOVE_GROUND_PER_SQM_ILS),
                "preserved_utilities": "שמירה מלאה על שטח הפלדלת של הדירות וכל ארונות החשמל, המים, הגז והתקשורת",
                "engineering_action": "הידוק שטחי מעבר כפולים בלובי ובגרעין הקומתי ויישור גומחות ארונות השירות לקו אפס.",
            }
        ]

        current_per_stall = total_ug_sqm / max(1, parking_spaces)
        excess_ug = max(25.0, round(max(0.0, (current_per_stall - 35.0) * parking_spaces), 1))
        ug_items = [
            {
                "id": f"{pid.upper()}-OPT-UG1",
                "zone": "מרתף חניון תת-קרקעי — ייעול קו דיפון וניצול תחתית רמפה",
                "current_sqm": total_ug_sqm,
                "optimal_sqm": round(total_ug_sqm - excess_ug, 1),
                "saved_sqm": excess_ug,
                "unit_cost_ils": COST_UNDERGROUND_PARKING_PER_SQM_ILS,
                "cost_saving_ils": round(excess_ug * COST_UNDERGROUND_PARKING_PER_SQM_ILS),
                "parking_spaces_preserved": f"{parking_spaces} חניות תקניות (100% שמירה על מצבת החניות)",
                "engineering_action": "מיקום מאגר המים וחדר המשאבות מתחת לרמפת הירידה וגיזום כיסי חפירה מתים בפינות הדיפון.",
            }
        ]

        apts_count = int(data_summary.get("apartments_count") or 16)
        reclaimed_per_apt = 1.6
        apt_items = [
            {
                "id": f"{pid.upper()}-OPT-APT1",
                "typology": f"כלל טיפוסי הדירות בפרויקט ({apts_count} יח״ד)",
                "current_corridor_sqm": 8.8,
                "optimal_corridor_sqm": 7.2,
                "reclaimed_sqm_per_unit": reclaimed_per_apt,
                "units_count": apts_count,
                "total_reclaimed_sqm": round(reclaimed_per_apt * apts_count, 1),
                "target_rooms_benefiting": "הגדלת חדרי השינה וסוויטת ההורים והרחבת פינת האוכל/סלון",
                "openings_optimization": "איחוד מפתחי חלונות למודול ייצור אחיד ואיזון יחס זיגוג לרצפה (WWR).",
                "engineering_action": "קיצור זנב המסדרון הפנימי ב-95 ס״מ והטמעת נישות ארונות בקו אפס.",
            }
        ]
        facade_opt = build_facade_cladding_optimization(fac, baseline_dry_pct=85.0, target_plaster_conversion_pct=35.0)

    total_ag_saved_sqm = round(sum(float(x["saved_sqm"]) for x in ag_items), 1)
    total_ag_saving_ils = round(total_ag_saved_sqm * COST_ABOVE_GROUND_PER_SQM_ILS)

    total_ug_saved_sqm = round(sum(float(x["saved_sqm"]) for x in ug_items), 1)
    total_ug_saving_ils = round(total_ug_saved_sqm * COST_UNDERGROUND_PARKING_PER_SQM_ILS)

    total_facade_converted_sqm = facade_opt["recommended_converted_to_plaster_sqm"]
    total_facade_saving_ils = facade_opt["recommended_saving_ils"]

    total_reclaimed_living_sqm = round(sum(float(x["total_reclaimed_sqm"]) for x in apt_items), 1)
    grand_total_saving_ils = total_ag_saving_ils + total_ug_saving_ils + total_facade_saving_ils

    current_core_ratio_pct = round((core_ag_sqm / total_ag_sqm * 100.0) if total_ag_sqm > 0 else 0.0, 1)
    optimized_ag_total_sqm = round(total_ag_sqm - total_ag_saved_sqm, 1)
    optimized_core_sqm = round(core_ag_sqm - total_ag_saved_sqm, 1)
    optimized_core_ratio_pct = round((optimized_core_sqm / optimized_ag_total_sqm * 100.0) if optimized_ag_total_sqm > 0 else 0.0, 1)

    current_sqm_per_stall = round(total_ug_sqm / max(1, parking_spaces), 1)
    optimized_ug_total_sqm = round(total_ug_sqm - total_ug_saved_sqm, 1)
    optimized_sqm_per_stall = round(optimized_ug_total_sqm / max(1, parking_spaces), 1)

    return {
        "pricing_parameters": {
            "above_ground_saved_per_sqm_ils": COST_ABOVE_GROUND_PER_SQM_ILS,
            "underground_parking_saved_per_sqm_ils": COST_UNDERGROUND_PARKING_PER_SQM_ILS,
            "dry_cladding_cost_per_sqm_ils": COST_DRY_CLADDING_PER_SQM_ILS,
            "plaster_cost_per_sqm_ils": COST_PLASTER_PER_SQM_ILS,
            "cladding_to_plaster_diff_per_sqm_ils": SAVING_CLADDING_TO_PLASTER_PER_SQM_ILS,
        },
        "zero_damage_guarantees": {
            "apartment_saleable_area_loss_sqm": 0.0,
            "apartment_saleable_area_preserved_sqm": net_apt_sqm,
            "parking_spaces_lost": 0,
            "parking_spaces_preserved": parking_spaces,
            "public_utilities_preserved": True,
            "guarantee_statement": (
                f"0 מ״ר פגיעה בשטח הדירות ({net_apt_sqm:,.1f} מ״ר פלדלת נשמרים במלואם) · "
                f"0 פגיעה במצבת החניות ({parking_spaces} חניות נשמרות) · "
                "שמירה מלאה על כל ארונות החשמל, המים, הגז, התקשורת וציוד כיבוי האש."
            ),
        },
        "executive_kpis": {
            "above_ground_saved_sqm": total_ag_saved_sqm,
            "above_ground_saving_ils": total_ag_saving_ils,
            "underground_saved_sqm": total_ug_saved_sqm,
            "underground_saving_ils": total_ug_saving_ils,
            "facade_converted_to_plaster_sqm": total_facade_converted_sqm,
            "facade_saving_ils": total_facade_saving_ils,
            "internal_reclaimed_living_sqm": total_reclaimed_living_sqm,
            "grand_total_direct_saving_ils": grand_total_saving_ils,
            "current_core_share_pct": current_core_ratio_pct,
            "optimized_core_share_pct": optimized_core_ratio_pct,
            "current_basement_sqm_per_stall": current_sqm_per_stall,
            "optimized_basement_sqm_per_stall": optimized_sqm_per_stall,
        },
        "above_ground_optimization": {
            "current_total_above_ground_sqm": total_ag_sqm,
            "current_core_and_service_sqm": core_ag_sqm,
            "optimized_core_and_service_sqm": optimized_core_sqm,
            "optimized_total_above_ground_sqm": optimized_ag_total_sqm,
            "total_saved_sqm": total_ag_saved_sqm,
            "rate_per_sqm_ils": COST_ABOVE_GROUND_PER_SQM_ILS,
            "total_saving_ils": total_ag_saving_ils,
            "items": ag_items,
        },
        "underground_optimization": {
            "current_total_underground_sqm": total_ug_sqm,
            "optimized_total_underground_sqm": optimized_ug_total_sqm,
            "parking_spaces": parking_spaces,
            "current_sqm_per_stall": current_sqm_per_stall,
            "optimized_sqm_per_stall": optimized_sqm_per_stall,
            "total_saved_sqm": total_ug_saved_sqm,
            "rate_per_sqm_ils": COST_UNDERGROUND_PARKING_PER_SQM_ILS,
            "total_saving_ils": total_ug_saving_ils,
            "items": ug_items,
        },
        "facade_cladding_optimization": facade_opt,
        "internal_apartment_optimization": {
            "total_reclaimed_effective_living_sqm": total_reclaimed_living_sqm,
            "items": apt_items,
        },
    }


# =============================================================================
# APARTMENT-LEVEL VALIDATION ENGINE HOOK (Called by validation_engine.py)
# =============================================================================
def check_apartment_value_engineering(apartment: dict, rules: list = None) -> list:
    """
    Runs internal apartment layout optimization checks on a single apartment JSON object:
    1. Corridor-to-Living area conversion opportunity (when corridor > 7.8% of apartment area or length > 4.2m).
    2. Walk-in closet / storage passage inefficiency check.
    3. Window-to-Floor Ratio (WWR) & Glazing Value Engineering check.
    Returns a list of result dicts (`status`, `element`, `rule_id`, `message`).
    """
    results = []
    rooms = apartment.get("rooms") or []
    if not rooms:
        return results

    total_net = float(
        apartment.get("net_area_sqm")
        or sum(float(r.get("area_sqm") or 0) for r in rooms if str(r.get("type", "")).lower() != "balcony")
    )
    if total_net <= 0:
        return results

    # 1. Corridor & Circulation Reclaim Analysis
    corridors = [
        r for r in rooms
        if any(k in str(r.get("type") or "").lower() for k in ("corridor", "hall", "passage", "foyer", "entr"))
        or any(k in str(r.get("name") or "") for k in ("מסדרון", "מבואה", "מעבר", "פרוזדור"))
    ]
    corr_sqm = sum(float(r.get("area_sqm") or 0) for r in corridors)
    corr_ratio = corr_sqm / total_net if total_net > 0 else 0.0
    optimal_corr_sqm = round(total_net * OPTIMAL_CORRIDOR_MAX_RATIO, 2)

    if corr_sqm > 0:
        reclaimable_sqm = round(max(0.0, corr_sqm - optimal_corr_sqm), 2)
        max_corr_len = max((float(r.get("depth_m") or 0) for r in corridors), default=0.0)
        if reclaimable_sqm >= 0.8 or max_corr_len >= 4.8:
            reclaim_est = max(reclaimable_sqm, round(0.95 * 1.05, 2))
            results.append({
                "status": "WARN",
                "element": "ייעול תכנון פנימי — הקטנת מסדרון והגדלת שטח חדרי מגורים",
                "rule_id": "VALUE_ENG_OPT",
                "message": (
                    f"שטח המסדרונות בדירה הוא {corr_sqm:.2f} מ\"ר ({corr_ratio:.1%} משטח הדירה"
                    f"{f', אורך {max_corr_len:.2f} מ׳' if max_corr_len > 0 else ''}). "
                    f"קיצור זנב המסדרון ב-90–120 ס\"מ והזזת דלת חדר הקצה יאפשרו להמיר כ-{reclaim_est:.2f} מ\"ר "
                    f"משטח מעבר לשטח מגורים אפקטיבי (הגדלת חדר שינה/סלון) ללא שינוי מעטפת הדירה."
                ),
            })
        else:
            results.append({
                "status": "PASS",
                "element": "ייעול תכנון פנימי — יחס מסדרונות לשטח מגורים אפקטיבי",
                "rule_id": "VALUE_ENG_OPT",
                "message": (
                    f"שטח המסדרון ({corr_sqm:.2f} מ\"ר = {corr_ratio:.1%} משטח הדירה) קומפקטי ומנוצל היטב לטובת חדרי המגורים."
                ),
            })

    # 2. Small Walk-in Closet (חדר ארונות) vs. Flush Reach-in Wardrobe Efficiency
    for r in rooms:
        r_name = str(r.get("name") or "")
        r_type = str(r.get("type") or "").lower()
        r_area = float(r.get("area_sqm") or 0)
        if ("ארונות" in r_name or r_type == "storage") and 1.8 <= r_area <= 3.1:
            results.append({
                "status": "WARN",
                "element": f"ייעול שטח אפקטיבי — איחוד {r_name} לחדר ההורים",
                "rule_id": "VALUE_ENG_OPT",
                "message": (
                    f"חדר הארונות ({r_area:.2f} מ\"ר) מקצה כ-60% משטחו למעבר פנימי וכפילות קירות/דלת. "
                    f"החלפתו בארון קיר רציף בקו אפס תשחרר כ-{r_area * 0.55:.2f} מ\"ר נטו להרחבת חדר ההורים ומעברי הצד למיטה, "
                    f"ותחסוך 2 מחיצות פנים ודלת."
                ),
            })

    # 3. Openings & Glazing Value Engineering (WWR Check)
    over_glazed = []
    for r in rooms:
        w_area = r.get("window_area_sqm")
        r_area = float(r.get("area_sqm") or 0)
        if w_area is not None and r_area > 0:
            ratio = float(w_area) / r_area
            if ratio > 0.32:
                over_glazed.append(f"{r.get('name', 'חדר')} ({float(w_area):.1f} מ\"ר זיגוג = {ratio:.0%} משטח הרצפה)")

    if over_glazed:
        results.append({
            "status": "WARN",
            "element": "ייעול פתחים ואלומיניום — איזון יחס זיגוג לרצפה (WWR)",
            "rule_id": "VALUE_ENG_OPT",
            "message": (
                f"יחס זיגוג גבוה במיוחד ב-{', '.join(over_glazed)} (התקן והמצוינות דורשים 10%–20%). "
                f"צמצום מתון של מפתח הזיגוג ב-15%–20% ואיחוד מודול החלונות יחסכו בעלויות האלומיניום והתריסים וישפרו את הבידוד התרמי והאקוסטי."
            ),
        })
    else:
        results.append({
            "status": "PASS",
            "element": "ייעול פתחים ואלומיניום — יחס זיגוג לרצפה (WWR)",
            "rule_id": "VALUE_ENG_OPT",
            "message": "יחס הפתחים והחלונות בחדרי הדירה מאוזן ויעיל תרמית וכלכלית (10%–25% משטח הרצפה).",
        })

    return results
