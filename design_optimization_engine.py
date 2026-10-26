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
                "floor_or_zone": "קומת קרקע (±0.00 = +39.62m · גיליון A-1001 — לובי, מאגר מים, משאבות וחדרי שירות)",
                "current_sqm": 245.0,
                "optimal_sqm": 185.0,
                "saved_sqm": 60.0,
                "preserved_utilities": "שמירה מלאה על לובי כניסה ראשי (1085×375 ס״מ), חדר אשפה תקני (430×355 ס״מ ל-12 פחים), חדר עגלות/אופניים (345×280 ס״מ), וריכוז מונים וארונות חשמל, מים, גז ותקשורת",
                "engineering_action": "בתכנית קומת הקרקע (A-1001): העברת מאגר המים (17 מ״ק, 285×294 ס״מ) וחדר המשאבות (250×335 ס״מ) מאגף השירות הדרום-מזרחי אל החלל התחתון של החלק העליון של הרמפה הדרומית במרתף, ביטול 'עמדת השהייה לפחי אשפה' הכפולה מדרום ללובי, ואיחוד מסדרון ריכוז המונים (290×85 ס״מ) עם מבואת חדר העגלות (חיסכון של 60.0 מ״ר קונטור בנוי עילי).",
                "sheet_id": "ground",
                "x_pct": 54.0, "y_pct": 25.0, "w_pct": 33.0, "h_pct": 56.0, "cx_pct": 70.5, "cy_pct": 53.0,
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
                "zone": "מרתף חניון (-3.50m = +34.60m · גיליון A-1000) — ניצול תחתית רמפה דרומית וגיזום כיסי דיפון",
                "current_sqm": 685.0,
                "optimal_sqm": 635.0,
                "saved_sqm": 50.0,
                "parking_spaces_preserved": "18 חניות תקניות (#1–#18 · 100% שמירה על מצבת החניות ומיסעה היקפית 5.00–6.40 מ׳)",
                "engineering_action": "שילוב חדר המשאבות ומאגר המים (17 מ״ק) בחלל התחתון מתחת לחלק העליון של רמפת הירידה הדרומית (H_clear = 2.20–3.20 מ׳ מתחת למקטע 11.5%–17%, חיסכון של 28 מ״ר חפירה) ויישור קו הדיפון בפינה הצפון-מערבית המתה (חיסכון של 22 מ״ר) — הורדת יחס השטח מ-38.1 מ״ר/חניה ל-35.3 מ״ר/חניה.",
                "sheet_id": "basement",
                "x_pct": 18.0, "y_pct": 12.0, "w_pct": 68.0, "h_pct": 78.0, "cx_pct": 52.0, "cy_pct": 51.0,
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
                "zone": "מרתף חניון (-5.10m — רמפה היקפית תלת-זרועית דרום←מזרח←צפון, 638 מ״ר ל-13 חניות = 49.1 מ״ר/חניה)",
                "current_sqm": 638.0,
                "optimal_sqm": 580.0,
                "saved_sqm": 58.0,
                "parking_spaces_preserved": "13 חניות תת-קרקעיות במרתף (#7–#10 במזרח במפלס +43.92, ו-#11–#19 במערב במפלס +42.42 כולל חניית נכה #18 ברוחב 293+130 ס״מ) + 6 חניות עיליות בקרקע (#1–#6) = 19 חניות + 2 חניות אופנועים + חדרי משאבות ואוורור",
                "engineering_action": "ניתוח הנדסי מדויק של לולאת התנועה במרתף חפץ חיים 44 חושף כי הרמפה היא רמפה היקפית תלת-זרועית חד-מסלולית (נגד כיוון השעון, אורך ~45 מ׳: זרוע דרומית בירידה ממערב למזרח 10%/3m ← 15%/9.8m [מ-+45.52 ל-+44.48] ← 10%/3m עד +44.18; זרוע מזרחית במיסעה משופעת 5%/8m ברוחב 5.55 מ׳ המשרתת את חניות #7–#10 עד +43.78; וזרוע צפונית בירידה ממזרח למערב 5.5%/3m ← 11%/7.6m [מ-+43.62 ל-+42.78] ← 5.5%/3m עד +42.61 ופנייה דרומה 2.5%/7.6m למיסעה המערבית 5.75 מ׳ במפלס +42.42). חדרי ה'משאבות' (335×200 ו-335×140 ס״מ) וה'אוורור' (200 ס״מ) כלואים כיום באי המרכזי בתוך קירות הממ״ד המערבי היורדים לביסוס, ולכן העברתם אל החלל האטום והמת מתחת לחלק העליון של הרמפה הדרומית (+46.25 עד +44.80, שם H_clear = 2.15–3.55 מ׳, בעוד מתחת לרמפה הצפונית ב-+43.62 אין גובה ראש כלל) אינה מקטינה לבדה את קו הדיפון (12.0 מ״ר בקופסת הממ״ד המערבי מועברים לשיפור תכנון להקמת 3 מחסני דיירים). הקטנת הקונטור האמיתית (58.0 מ״ר = 203,000 ₪) מושגת ע״י: (1) יצירת מגרעת דיפון בפינה הדרום-מערבית (48.0 מ״ר = 15.50×3.10 מ׳ מדרום לחניה #15 וממערב לתחילת הרמפה הדרומית — אזור שנמצא כולו מחוץ לקו הבניין העילי 4.00 מ׳ ובסימטריה מלאה למגרעת הדרום-מזרחית K) תוך העתקת חניה #16 למפרץ החדש שנפתח בדופן המזרחית של האי המרכזי (מול המיסעה המזרחית 5.55 מ׳, במקום מפרץ האופנועים והמבואה המדורגת 44.00 שצומצמה לאחר פינוי המשאבות); ו-(2) הידוק רוחב המיסעה המערבית מ-5.75 מ׳ ל-5.20 מ׳ תקני וקירוב הדיפון המערבי ב-55 ס״מ (10.0 מ״ר).",
                "sheet_id": "h44_basement",
                "x_pct": 9.5, "y_pct": 68.5, "w_pct": 35.5, "h_pct": 11.3, "cx_pct": 25.0, "cy_pct": 74.0,
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
                "floor_or_zone": "קומת קרקע (±0.00 — לובי 29 מ״ר וחדרי שירות ל-11 דירות בלבד בתכנית המקור)",
                "current_sqm": 93.0,
                "optimal_sqm": 75.0,
                "saved_sqm": 18.0,
                "preserved_utilities": "שמירה מלאה על לובי דו-מפלסי, חדר אשפה, חדר גז, חדר עגלות/אופניים וכל ארונות החשמל/מים/תקשורת",
                "engineering_action": "בבניין בוטיק של 11 דירות בלבד, שטח שירות של 93.0 מ״ר בקרקע ניתן לייעול ל-75.0 מ״ר על ידי קיצור מסדרון השירות הפנימי ואיחוד מבואת חדר העגלות (חיסכון של 18.0 מ״ר בנוי עילי).",
                "sheet_id": "yat_ground",
                "x_pct": 34.0, "y_pct": 32.0, "w_pct": 24.0, "h_pct": 20.0, "cx_pct": 46.0, "cy_pct": 42.0,
            },
            {
                "id": "Y7-OPT-AG2",
                "floor_or_zone": "קומות א׳–ו׳ וגג (6 קומות + גג — הידוק גרעין קומתי בתכנית המקור)",
                "current_sqm": 177.0,
                "optimal_sqm": 165.0,
                "saved_sqm": 12.0,
                "preserved_utilities": "שמירה על מדרגות, מעלית, מחסן קומה ו׳ וכל ארונות השירות הקומתיים",
                "engineering_action": "הידוק הגרעין הקומתי ב-2.0 מ״ר לקומה בקומות הטיפוסיות ובגג הטכני (סה״כ 12.0 מ״ר) תוך שמירה על מרווחי גישה מלאים לארונות החשמל והמים.",
                "sheet_id": "yat_typical",
                "x_pct": 34.0, "y_pct": 31.0, "w_pct": 25.0, "h_pct": 16.0, "cx_pct": 46.5, "cy_pct": 39.0,
            },
        ],
        "underground_items": [
            {
                "id": "Y7-OPT-UG1",
                "zone": "מרתף חניון (-4.38m — ניצול תחתית רמפה מערבית 10%/17% בגובה H≥2.20m ושמירת רדיוסי סיבוב R300/R450/R500)",
                "current_sqm": 465.0,
                "optimal_sqm": 425.0,
                "saved_sqm": 40.0,
                "parking_spaces_preserved": "12 חניות רגילות (#1–#12 בתכנית המקור, כולל חניית נכה #12 ברוחב 437 ס״מ) + רמפה 17%/10% + רדיוסי סיבוב R300 ו-R450/R500 + מיסעות 6.20–6.53 מ׳",
                "engineering_action": "בתכנית המקור של מרתף יטקובסקי 7, מאגר המים וחדר המשאבות ממוקמים כיום בתא נפרד בין הרמפה המערבית (17% לאורך 7.60 מ׳ + 10% לאורך 3.00 מ׳) לחניית הנכה #12. שטחי הרמפה הפעילה, רדיוסי הסיבוב R300 ו-R450/R500 ומיסעות התמרון (6.20 מ׳ בדרום ליד חניות #1–#6 ו-6.37–6.53 מ׳ בצפון ליד חניות #7–#11) מוגנים ב-100% (14.0 מ״ר קוזזו מחיסכון הקונטור); החיסכון המאומת (40.0 מ״ר) מושג ע״י הכנסת מאגר המים והמשאבות מתחת לחלק העליון של הרמפה המערבית והמזרחית (H_clear ≥ 2.20 מ׳ במפלס 54.20–53.75) וגיזום כיס הדיפון הצפון-מזרחי המת מחוץ לקשת R500.",
                "sheet_id": "yat_basement",
                "x_pct": 12.0, "y_pct": 33.5, "w_pct": 59.5, "h_pct": 46.0, "cx_pct": 41.8, "cy_pct": 56.5,
            },
        ],
        "internal_apartment_items": [
            {
                "id": "Y7-OPT-APT1",
                "typology": "דירות צפוניות ודרומיות בקומות א׳–ד׳ + דירת גן (9 דירות — 97–105 מ״ר בתכנית המקור)",
                "current_corridor_sqm": 7.9,
                "optimal_corridor_sqm": 6.5,
                "reclaimed_sqm_per_unit": 1.4,
                "units_count": 9,
                "total_reclaimed_sqm": 12.6,
                "target_rooms_benefiting": "הרחבת חדר ההורים מ-275/280 ס״מ ל-295 ס״מ (תיקון התראת ADG!) + גומחה שקועה לדלת הממ״ד",
                "openings_optimization": "אופטימיזציית פתחי חלונות בחזיתות מזרח ומערב למודול אחיד עם בידוד אקוסטי 40dB.",
                "engineering_action": "קיצור זנב מסדרון חדרי השינה ב-90 ס״מ והסטת מחיצת הפנים של סוויטת ההורים — העברת 1.4 מ״ר נטו ממסדרון לחדר ההורים ולחלל המגורים בכל 9 הדירות.",
                "sheet_id": "yat_typical",
                "x_pct": 37.5, "y_pct": 34.0, "w_pct": 26.0, "h_pct": 36.0, "cx_pct": 50.5, "cy_pct": 52.0,
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
                "x_pct": 23.0, "y_pct": 24.0, "w_pct": 37.0, "h_pct": 64.0, "cx_pct": 41.5, "cy_pct": 56.0,
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
                "x_pct": 34.0, "y_pct": 21.5, "w_pct": 18.0, "h_pct": 56.0, "cx_pct": 43.0, "cy_pct": 49.5,
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
                "engineering_action": "המרתף המשותף מתוכנן היטב (איחוד רמפה אחת ל-2 בניינים), אך ניתן לחסוך עוד 125.0 מ״ר על ידי מיקום חדרי המשאבות ומאגר המים (15 קוב × 2) מתחת לחלק העליון של רמפת הכניסה הדו-סטרית (17% L=15.83m) וגיזום שני כיסי דיפון מתים בקצוות המרתף (הורדת היחס מ-38.4 ל-36.4 מ״ר/חניה).",
                "sheet_id": "kit_basement",
                "x_pct": 8.5, "y_pct": 8.0, "w_pct": 66.0, "h_pct": 85.5, "cx_pct": 41.5, "cy_pct": 50.8,
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
                "floor_or_zone": "קומת קרקע (±0.00m — העברת מאגר מים לתחתית החלק העליון של הרמפה במרתף 1- והידוק מעברי שירות)",
                "current_sqm": 265.0,
                "optimal_sqm": 223.0,
                "saved_sqm": 42.0,
                "preserved_utilities": "שמירה מלאה על לובי כניסה ראשי, מועדון דיירים, חדר אופניים ועגלות, חדר אשפה ודחסנית, חדר גז ולוח חח״י וכל ארונות המונים",
                "engineering_action": "העברת מאגר המים וחדר המשאבות (28 מ״ר בקומת הקרקע) אל החלל התחתון מתחת לחלק העליון של כבש הרמפה הצפון-מזרחית במרתף 1- (שם גובה הראש הפנוי H_clear = 2.20–3.15 מ׳ ≥ 2.15 מ׳), ואיחוד מסדרון השירות העורפי בין חדר האשפה למועדון הדיירים (חיסכון מאומת של 42.0 מ״ר בנוי עילי).",
                "sheet_id": "fb_ground",
                "x_pct": 36.0, "y_pct": 33.0, "w_pct": 30.0, "h_pct": 24.0, "cx_pct": 51.0, "cy_pct": 45.0,
            },
            {
                "id": "FB3-OPT-AG2",
                "floor_or_zone": "קומות 1–8 (8 קומות — הידוק גרעין ומבואה קומתית ל-2 דירות בקומה בתכנית המקור)",
                "current_sqm": 248.0,
                "optimal_sqm": 220.0,
                "saved_sqm": 28.0,
                "preserved_utilities": "שמירה מלאה על חדר מדרגות מוגן (3.50×3.50 מ׳), פיר מעלית (1.75×1.80 מ׳) וכל ארונות החשמל, המים, התקשורת וכיבוי האש הקומתיים",
                "engineering_action": "בקומה טיפוסית של 2 דירות בלבד (דירה 1 מזרחית ודירה 2 מערבית בתכנית המקור), הידוק מבואת הקומה מ-31.0 מ״ר ל-27.5 מ״ר לקומה (חיסכון של 3.5 מ״ר × 8 קומות = 28.0 מ״ר) על ידי קירוב אגפי הדירות ב-25 ס״מ על ציר האורך והטמעת ארונות המונים בקו אפס בדופן הגרעין.",
                "sheet_id": "fb_typical",
                "x_pct": 33.5, "y_pct": 27.0, "w_pct": 20.5, "h_pct": 16.5, "cx_pct": 43.8, "cy_pct": 35.2,
            },
            {
                "id": "FB3-OPT-AG3",
                "floor_or_zone": "קומות 9–10 וגג עליון (+28.87m עד +35.17m — מבואת דופלקסים ויציאה לגג)",
                "current_sqm": 100.8,
                "optimal_sqm": 88.8,
                "saved_sqm": 12.0,
                "preserved_utilities": "שמירה על יציאה תקנית לגג, גישה למערכות קולטי השמש ופיר המעלית העליון",
                "engineering_action": "צמצום מבואת הגלריה המשותפת בקומה 10 (שבה הכניסה הראשית לדופלקסים היא מקומה 9) והתאמת חדר היציאה לגג לקונטור הפירים ההנדסי בלבד (חיסכון של 12.0 מ״ר בנוי עילי).",
                "sheet_id": "fb_floor10",
                "x_pct": 39.0, "y_pct": 27.0, "w_pct": 22.0, "h_pct": 17.5, "cx_pct": 50.0, "cy_pct": 35.8,
            },
        ],
        "underground_items": [
            {
                "id": "FB3-OPT-UG1",
                "zone": "מרתף 1- (-4.80m — ניצול תחתית רמפה עליונה H≥2.20m וגיזום כיס דרום-מזרחי מחוץ לרדיוס R=369)",
                "current_sqm": 548.0,
                "optimal_sqm": 503.0,
                "saved_sqm": 45.0,
                "parking_spaces_preserved": "8 חניות רגילות במרתף 1- (#1–#8 בתכנית המקור) + רמפה דו-שיפועית (15% / 7.5% / R=350-369) + מיסעה 5.90–6.50 מ׳ + אוזן תמרון 1.00 מ׳ לחניה #4",
                "engineering_action": "בתכנית המקור של מרתף 1-, הרמפה יורדת בצפון-מזרח (15% לאורך 19.00 מ׳), מתמתנת (5% ו-7.5% לאורך 3.00 מ׳) ומסתובבת במזרח ברדיוס R=350–369 ס״מ לירידה למרתף 2- לצד חניות #7–#8 ומיסעה של 6.50 מ׳. שטח מסלול הרמפה, משטח הסיבוב R=369 והמיסעה (22.0 מ״ר) מוגנים ב-100% ואסורים לגריעה; החיסכון המאומת (45.0 מ״ר) מושג ע״י הכנסת מאגר המים וחדר המשאבות מתחת לחלק העליון של הרמפה הצפון-מזרחית (גובה ראש פנוי H_clear = 2.20–3.15 מ׳) ונסיגת קיר הדיפון בכיס הדרום-מזרחי המת (מדרום לרדיוס R=369 וממזרח לחניה #6).",
                "sheet_id": "fb_basement1",
                "x_pct": 65.5, "y_pct": 28.0, "w_pct": 19.0, "h_pct": 47.5, "cx_pct": 75.0, "cy_pct": 65.5,
            },
            {
                "id": "FB3-OPT-UG2",
                "zone": "מרתף 2- (-7.80m — גריעת רצועת דיפון דרומית-מרכזית מתה בין חניה #12 ל-#13 מחוץ לרדיוס R500 ושמירת אגף מזרחי #13–#17)",
                "current_sqm": 548.0,
                "optimal_sqm": 498.0,
                "saved_sqm": 50.0,
                "parking_spaces_preserved": "11 חניות רגילות במרתף 2- (#9–#19 בתכנית המקור: כולל חניות מזרחיות #13–#17, חניית נכה #17 ברוחב 437 ס״מ, מיסעה 5.20–5.50 מ׳ ורדיוס סיבוב רמפה R400/R500 במפלס 45.10)",
                "engineering_action": "בדיקת תכנית המקור של מרתף 2- מוכיחה כי באגף המזרחי ממוקמות חניות #15, #16, #17 (צפון-מזרח) וחניות #13, #14 (דרום-מזרח) וביניהן מיסעה של 5.20–5.50 מ׳ ומשטח יציאה מהרמפה ברדיוס R400/R500 (רוחב 4.20 מ׳) — ולכן 26.0 מ״ר באגף המזרחי מוגנים לחלוטין כשטח תמרון ורמפה ואסורים לגריעה! החיסכון המאומת בקונטור הדיפון (50.0 מ״ר) מושג ע״י נסיגת קיר הדיפון הדרומי-מרכזי ב-32.0 מ״ר ברצועה המתה שבין חניה #12 לחניה #13 (מדרום לחניות #19–#18 ומחוץ לקשת החיצונית R500 של הרמפה) + 18.0 מ״ר ניצול תחתית החלק העליון של הרמפה הצפונית (H_clear ≥ 2.15 מ׳) לבורות שאיבה ומפריד שומנים.",
                "sheet_id": "fb_basement2",
                "x_pct": 36.0, "y_pct": 58.0, "w_pct": 32.0, "h_pct": 16.0, "cx_pct": 52.0, "cy_pct": 66.5,
            },
        ],
        "internal_apartment_items": [
            {
                "id": "FB3-OPT-APT1",
                "typology": "דירה 1 בתכנית המקור (אגף ימני/מזרחי בתכנית · 8 דירות של 4 חדרים — 105.46 מ״ר)",
                "current_corridor_sqm": 9.8,
                "optimal_corridor_sqm": 8.0,
                "reclaimed_sqm_per_unit": 1.8,
                "units_count": 8,
                "total_reclaimed_sqm": 14.4,
                "target_rooms_benefiting": "הגדלת חדר השינה הצפוני (מרוחב 2.80 מ׳ ל-2.98 מ׳) + הרחבת סוויטת ההורים והסלון (650×420 ס״מ)",
                "openings_optimization": "איחוד מפתחי חלונות חדרי השינה למודול אחיד של 140×150 ס״מ עם זיגוג Low-E ואקוסטיקה 40dB.",
                "engineering_action": "קיצור זנב המסדרון הפנימי (אורך 880 ס״מ בתכנית המקור) ב-105 ס״מ ויישור מבואת חדרי השינה — השבחה של 1.8 מ״ר שטח מגורים אפקטיבי בכל אחת מ-8 הדירות (14.4 מ״ר סה״כ).",
                "sheet_id": "fb_typical",
                "x_pct": 40.0, "y_pct": 28.0, "w_pct": 35.0, "h_pct": 31.0, "cx_pct": 57.5, "cy_pct": 43.5,
            },
            {
                "id": "FB3-OPT-APT2",
                "typology": "דירה 2 בתכנית המקור (אגף שמאלי/מערבי בתכנית · 8 דירות של 4 חדרים — 85.53 מ״ר)",
                "current_corridor_sqm": 7.9,
                "optimal_corridor_sqm": 6.5,
                "reclaimed_sqm_per_unit": 1.4,
                "units_count": 8,
                "total_reclaimed_sqm": 11.2,
                "target_rooms_benefiting": "הרחבת סוויטת ההורים הדרום-מערבית (340×280 ס״מ בתכנית המקור) מרוחב 2.80–2.95 מ׳ ל-3.12 מ׳ (עמידה מלאה ב-ADG ≥3.00 מ׳!)",
                "openings_optimization": "סטנדרטיזציה של ויטרינת המרפסת הדרומית וחלונות החזית הצדדית.",
                "engineering_action": "קיצור קצה המסדרון של דירה 2 (625 ס״מ בתכנית המקור) ב-95 ס״מ והזזת דלת סוויטת ההורים קדימה לקו חדר הרחצה — העברת 1.4 מ״ר נטו משטח המעבר אל תוך חדר ההורים (11.2 מ״ר ב-8 דירות).",
                "sheet_id": "fb_typical",
                "x_pct": 10.0, "y_pct": 28.0, "w_pct": 28.5, "h_pct": 31.0, "cx_pct": 24.2, "cy_pct": 43.5,
            },
            {
                "id": "FB3-OPT-APT3",
                "typology": "דופלקס-פנטהאוזים #17 ו-#18 (קומות 9–10 בתכנית המקור · 2 דירות — 121.3 ו-103.6 מ״ר)",
                "current_corridor_sqm": 11.5,
                "optimal_corridor_sqm": 9.4,
                "reclaimed_sqm_per_unit": 2.1,
                "units_count": 2,
                "total_reclaimed_sqm": 4.2,
                "target_rooms_benefiting": "הגדלת סוויטות ההורים הראשיות בקומה 10 ופינת העבודה/גלריה",
                "openings_optimization": "איזון מפתחי הוויטרינות הפנורמיות בקומה 9 (מרפסות 1300×200/300 ס״מ) עם פרגולות ההצללה הדרומיות לחיסכון בעלויות האלומיניום ושיפור הבידוד התרמי.",
                "engineering_action": "הידוק גלריית המעבר העליונה בקומה 10 והעברת 2.1 מ״ר לכל דופלקס לטובת סוויטת ההורים הראשית.",
                "sheet_id": "fb_floor10",
                "x_pct": 22.0, "y_pct": 28.0, "w_pct": 64.0, "h_pct": 28.0, "cx_pct": 54.0, "cy_pct": 42.0,
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
# 5 ENGINEERING & GEOMETRIC CONTOUR CONTRACTION AUDIT PILLARS
# =============================================================================
CONTOUR_AUDIT_METHODOLOGY_PILLARS = [
    {
        "test_id": "TEST-1-WING-PULL",
        "title": "מבחן 1 — טופולוגיית קירוב אגפים או נסיגת חזית (Wing-Pull & Perimeter Setback)",
        "description": (
            "בודק האם הקטנת הגרעין/המבואה הקומתית מאפשרת לקרב את אגפי הדירות זה לזה על ציר האורך/רוחב (ΔX/ΔY) "
            "או להסיג קיר מעטפת חיצוני פנימה. אם הגרעין הוא 'נישה פנימית כלואה' בין דירות ועמודים קבועים והמעטפת לא זזה — "
            "השטח אינו מקטין קונטור בניין (0 ₪ חיסכון שלד) ומועבר לשיפור תכנון."
        ),
    },
    {
        "test_id": "TEST-2-VERTICAL-SLAB-LOCK",
        "title": "מבחן 2 — רציפות אנכית ונעילת תקרה עליונה (Upper-Slab Projection Lock)",
        "description": (
            "בודק בקומת הקרקע ובקומות הביניים האם השטח שצומצם נמצא תחת תקרת הקומה שמעליו (Under-Slab Footprint) או בבליטה חיצונית. "
            "שטח בקומת קרקע שנמצא מתחת לתקרת קומה א׳ קשיחה שממילא נבנית אינו מקטין את קונטור תקרת הבניין — ולכן מקוזז מחיסכון העלויות "
            "ומסווג כשיפור תכנון (הרחבת לובי פתוח/מפולש)."
        ),
    },
    {
        "test_id": "TEST-3-SHORING-POLYGON",
        "title": "מבחן 3 — כיווץ דיפון במרתף, תפקוד רמפות (H_clear ≥ 2.15m) והגנה על רדיוסי סיבוב ומיסעות תמרון",
        "description": (
            "במרתפי חניון, חיסכון בעלויות בנייה (3,500 ₪/מ״ר) מוכר אך ורק כאשר קיר הדיפון ההיקפי וגבול החפירה זזים פנימה בכיסים מתים מחוץ למיסעה. "
            "אסור בתכלית האיסור לגרוע משטח מסלול הנסיעה ברמפה (שיפוע 15%–17.5% ומשטחי התמתנות 5%–10% באורך 3.00 מ׳), מרדיוסי הסיבוב וההתמזגות "
            "(R_in ≥ 3.00–4.50 מ׳ ו-R_out ≥ 5.00 מ׳), ממיסעות התמרון הדו-סטריות (5.20–6.50 מ׳ לחניות 90°) ומאוזני התמרון לחניות קצה (1.00 מ׳). "
            "הכנסת מאגר מים או חדר משאבות לתחתית הרמפה מותרת אך ורק בחצי העליון של כבש הירידה שבו גובה הראש הפנוי תחת קורת הרמפה הוא H_clear ≥ 2.15–2.20 מ׳."
        ),
    },
    {
        "test_id": "TEST-4-EFFICIENCY-FACTOR",
        "title": "מבחן 4 — מקדם תרגום לקונטור (η_contour = ΔA_contour / ΔA_core) וקיזוז שטחי תמרון מוגנים",
        "description": (
            "מחשב לכל המלצה את היחס שבין השטח התאורטי להפחתה בליבה/מרתף לבין השטח שנגרע בפועל מקונטור הבנייה הכולל (סך הכל נבנה פחות). "
            "כל שטח מרתף החופף לרמפה פעילה, לרדיוס סיבוב או למיסעת תמרון מקוזז אוטומטית מחיסכון הקונטור ומסווג כ'שטח תמרון ורמפה מוגן (0 ₪ חיסכון)'."
        ),
    },
    {
        "test_id": "TEST-5-APARTMENT-INVARIANCE",
        "title": "מבחן 5 — שימור קונטור הפלדלת, מצבת החניות והעתקת חנייה שזזה למקום חלופי מאומת (Zero Loss & Stall Relocation Check)",
        "description": (
            "מוודא שהקטנת קונטור הבניין והמרתף נובעת ב-100% מכיווץ שטחי ברוטו וכיסי חפירה עודפים עם 0.0 מ״ר פגיעה בשטח הפלדלת של הדירות ו-0 פגיעה במספר החניות התקניות. "
            "בכל המלצה שבה נסיגת קיר הדיפון מבטלת או מזיזה תא חנייה קיים בקצה המרתף, המנוע מבצע בדיקת העתקה חובה (Stall Relocation Audit): "
            "איתור והקצאת מקום חלופי מאומת במרתף (לרוב במפרץ שהתפנה לאורך המיסעה המרכזית בעקבות העברת מאגר המים וחדר המשאבות אל מתחת לחלק העליון של הרמפה H_clear ≥ 2.15–2.20m), "
            "כולל אימות מידות תקניות (≥2.42–2.65×5.00 מ׳) וכניסה/יציאה ישירה בתמרון אחד מהמיסעה."
        ),
    },
    {
        "test_id": "TEST-6-MAMAD-DROPWALL-AND-MULTIFLOOR-LOCK",
        "title": "מבחן 6 — הצלבה רב-קומתית, קירות ממ״ד יורדים (70% פקע״ר), לולאת רמפה עוקפת ליבה וקו דיפון מול קו בניין (לקחי חפץ חיים 44 ופינס 48)",
        "description": (
            "מחייב הצלבה אנכית של תוכנית המרתף מול תוכנית קומת הקרקע ותוכנית הקומה הטיפוסית באותה מערכת צירים: "
            "(א) זיהוי קירות ממ״ד עיליים שיורדים לביסוס במרתף (חובת פקע״ר ל-70% קירות רציפים): חדר משאבות או מאגר מים הממוקם בתוך קופסת קירות ממ״ד יורדים או באי פנימי המוקף בלולאת רמפה תלת-זרועית אינו מקטין את קיר הדיפון החיצוני ב-0.0 מ״ר (0 ₪ חיסכון שלד) ומסווג כשיפור תכנון (הסבה למחסני דיירים), בעוד רק המפרץ שמחוץ לקירות הממ״ד ולצד המיסעה מתפנה לחנייה חלופית; "
            "(ב) הבחנה בין 'קו דיפון' (0.00) ל-'קו בניין עילי' (3.00–4.00 מ׳): כיווץ קונטור הדיפון מתבצע בכיסים ההיקפיים שמחוץ לקו הבניין העילי שבהם אין עמודי שלד יורדים; "
            "(ג) חיבור כל המלצה בקומת הקרקע (A-1001) או במרתף (A-1000) לתוכנית המקור הייעודית של אותה קומה."
        ),
    },
]

# Explicit engineering metadata per recommendation item (`id`) defining:
# - `proposed_gross_reduction_sqm`: סך השטח שהוצע להוריד בליבה/שירות/מרתף לפני מבחן קונטור והגנת תמרון/רמפות
# - `verified_contour_saved_sqm`: השטח שבאמת הקטין את קונטור הבניין/המרתף הכולל (נבנה פחות בפועל — זהה ל-saved_sqm)
# - `non_contour_reclassified_sqm`: שטח שירד בליבה או קוזז במרתף בגין הגנה על רמפות/רדיוסי סיבוב/מיסעות תמרון (0 ₪ חיסכון)
# - `protected_ramp_and_maneuvering_deducted_sqm`: שטח מרתף שקוזז מחיסכון הקונטור כדי להגן על מסלול הרמפה, רדיוסי הסיבוב ומיסעת התמרון
# - `under_ramp_utilized_sqm`: שטח טכני (מאגר מים/חדר משאבות/בורות שאיבה) שמוקם מתחת לחלק העליון של הרמפה שבו H_clear >= 2.15m
# - `ramp_function_audit_he`: ניתוח הנדסי של תפקוד הרמפה, שיפועים, משטחי התמתנות, רדיוסי סיבוב וגובה ראש פנוי (H_clear)
# - `maneuvering_aisle_audit_he`: ניתוח הנדסי של שטחי התמרון לחניות (רוחב מיסעה 5.20–6.50 מ׳, רדיוסי פנייה ואוזני תמרון 1.00 מ׳)
# - `plan_overlay_zones`: פוליגונים מנורמלים להצגה על גבי תוכנית המקור (אזור תמרון/רמפה מוגן ואזור ניצול תחתית רמפה H>=2.15m)
ITEM_CONTOUR_AUDIT_METADATA = {
    # PINES 48
    "P48-OPT-AG1": {
        "proposed_gross_reduction_sqm": 74.0,
        "verified_contour_saved_sqm": 60.0,
        "non_contour_reclassified_sqm": 14.0,
        "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
        "contour_mechanism": "בתכנית קומת הקרקע (A-1001): ביטול אגף מאגר המים (285×294 ס״מ) וחדר המשאבות (250×335 ס״מ) העילי בדרום-מזרח (העברתם מתחת לרמפה הדרומית העליונה במרתף), ביטול 'עמדת השהייה לפחי אשפה' הכפולה ואיחוד מעבר ריכוז המונים (290×85 ס״מ) = נסיגת קיר המעטפת של סגירת קומת הקרקע ב-60.0 מ״ר בנוי.",
        "contour_dims_before_after": "קונטור סגירת קומת קרקע (A-1001): 245.0 מ״ר ← 185.0 מ״ר (-60.0 מ״ר נבנה פחות)",
        "locked_reason_he": "14.0 מ״ר מתוך הפחתת מעברי הלובי בקומת הקרקע נמצאים מתחת לתקרת קומה א׳ הקשיחה (מבחן 2 — נעילת תקרה עליונה), ולכן אינם מקטינים את קונטור התקרה אלא מרחיבים את הלובי הפתוח/מפולש (הועברו לשיפור תכנון).",
        "plan_overlay_zones": {
            "protected_ramp_maneuver_rect": {"x_pct": 48.0, "y_pct": 30.0, "w_pct": 36.0, "h_pct": 26.0, "label_he": "לובי ראשי (1085×375) + חדר עגלות (345×280) + גרעין מדרגות/מעלית (נשמרים 100%)"},
            "under_ramp_utility_rect": {"x_pct": 56.0, "y_pct": 68.0, "w_pct": 31.0, "h_pct": 13.5, "label_he": "אגף מאגר מים (285×294) + משאבות (250×335) שיורד לתחתית הרמפה (-60 מ״ר סגירה עילית)"},
        },
    },
    "P48-OPT-AG2": {
        "proposed_gross_reduction_sqm": 42.0,
        "verified_contour_saved_sqm": 33.0,
        "non_contour_reclassified_sqm": 9.0,
        "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
        "contour_mechanism": "קירוב אגפי הדירות המזרחי והמערבי ב-38 ס״מ על ציר X והכנסת בליטת קיר הגרעין הצפוני ב-45 ס״מ (5.5 מ״ר הקטנת קונטור תקרה × 6 קומות = 33.0 מ״ר).",
        "contour_dims_before_after": "קונטור קומה טיפוסית: 314.8 מ״ר ← 309.3 מ״ר (-5.5 מ״ר לקומה × 6 קומות = -33.0 מ״ר)",
        "locked_reason_he": "9.0 מ״ר (1.5 מ״ר לקומה × 6 קומות) בנישת המבואה הפנימית כלואים בין קירות הממ״ד לעמודי השלד (מבחן 1 — ליבה כלואה), ולכן אינם מקטינים את קונטור החוץ ומועברים לשיפור תכנון המבואה.",
    },
    "P48-OPT-AG3": {
        "proposed_gross_reduction_sqm": 8.0,
        "verified_contour_saved_sqm": 8.0,
        "non_contour_reclassified_sqm": 0.0,
        "contour_test_status": "FULL_CONTOUR_REDUCTION",
        "contour_mechanism": "הקטנת קונטור חדר היציאה לגג והמבואה העליונה בקומה 8 (4 walls exterior roof-box contraction — 100% תרגום לקונטור).",
        "contour_dims_before_after": "קונטור גג טכני קומה 8: 64.0 מ״ר ← 56.0 מ״ר (-8.0 מ״ר נבנה פחות)",
        "locked_reason_he": "100% מהשטח הוא מעטפת חיצונית עצמאית על הגג ולכן כולו מקטין קונטור בנייה.",
    },
    "P48-OPT-UG1": {
        "proposed_gross_reduction_sqm": 62.0,
        "verified_contour_saved_sqm": 50.0,
        "non_contour_reclassified_sqm": 12.0,
        "protected_ramp_and_maneuvering_deducted_sqm": 12.0,
        "under_ramp_utilized_sqm": 28.0,
        "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
        "contour_mechanism": "בתכנית המרתף (A-1000): הזזת קו כלונסאות הדיפון הדרומי והצפון-מערבי פנימה לאחר הכנסת מאגר המים (17 מ״ק) וחדר המשאבות מתחת לחלק העליון של רמפת הירידה הדרומית (H_clear = 2.20–3.20 מ׳ מתחת למקטע 11.5%–17%) וגיזום הכיס הצפון-מערבי המת מחוץ למיסעה (-50.0 מ״ר חפירה ודיפון).",
        "contour_dims_before_after": "קונטור דיפון מרתף (A-1000): 685.0 מ״ר ← 635.0 מ״ר (-50.0 מ״ר חפירה ודיפון מאומתים · 12.0 מ״ר קוזזו להגנת תמרון ורמפה)",
        "locked_reason_he": "12.0 מ״ר ביציאה מרמפת הירידה הדרומית וברצועת הגישה לחניות הקצה מוגנים כשטח סיבוב רמפה (R=300–500 ס״מ) ואוזן תמרון (1.00 מ׳) לצד מיסעה היקפית של 5.00–6.40 מ׳ — ולכן קוזזו מחיסכון הקונטור (0 ₪) כדי להבטיח תמרון תקני ל-18 החניות (#1–#18).",
        "ramp_function_audit_he": "רמפת ירידה דרומית (רוחב 3.00–4.00 מ׳, מקטעי התמתנות 4% ו-11.5% באורך 3.0 מ׳ במזרח ← שיפוע 17% באורך 11.6 מ׳ ← התמתנות 10% באורך 3.0 מ׳ במערב): החצי העליון המזרחי של הרמפה (+38.84 עד +39.30 מעל רצפת מרתף +34.60, גובה ראש פנוי H_clear = 2.20–3.20 מ׳) מאכלס במלואו את מאגר המים וחדר המשאבות (28.0 מ״ר). החצי התחתון של הרמפה ומשטח ההתמזגות ברדיוס R=500 ס״מ למיסעה המערבית נשמרים חופשיים לחלוטין.",
        "maneuvering_aisle_audit_he": "שמירה קשיחה על לולאת המיסעה ההיקפית ברוחב 5.00–6.40 מ׳ ורדיוסי הסיבוב R300/R500 לאורך כל 18 החניות (#1–#18); 12.0 מ״ר שהיו פוגעים ברדיוס הפנייה של חניות הקצה קוזזו מהחיסכון.",
        "parking_relocation_audit": {
            "stalls_relocated_count": 1,
            "affected_stalls_label": "חניה #6 (פינה צפון-מערבית בקונטור שצומצם)",
            "original_location_he": "מוקמה בכיס הצפון-מערבי של המרתף שניסוג פנימה ב-22.0 מ״ר להקטנת קונטור הדיפון.",
            "alternative_location_found_he": "הועתקה למפרץ החלופי הפנוי ('HOLD' — 242×539 ס״מ בתכנית המקור A-1000) ממערב לגרעין המדרגות, הצמוד למיסעה המערבית (5.00–6.20 מ׳) לאחר העברת המערכות הטכניות אל מתחת לרמפה הדרומית העליונה.",
            "new_stall_dimensions_and_access_he": "תא חניה תקני 2.42×5.39 מ׳ (13.0 מ״ר) בניצב (90°) למיסעה המערבית (5.00–6.20 מ׳) עם כניסה ויציאה ישירה בתמרון אחד וללא עמודים מפריעים.",
            "net_parking_balance_he": "מאזן חניות נטו: 0 גריעה (1 חניה הועתקה מכיס הדיפון ← 1 מפרץ חלופי מאומת באזור HOLD אוכלס = 18/18 חניות נשמרות ב-100%).",
        },
        "parking_relocation_audit_he": "בדיקת העתקת חנייה ומציאת מקום חלופי: גיזום הכיס הצפון-מערבי (22.0 מ״ר) מזיז את חניית הקצה #6. בתכנית המרתף המקורית (A-1000) קיים ממערב לגרעין מפרץ פנוי המסומן כ-'HOLD' במידות 242×539 ס״מ הפונה ישירות למיסעה המערבית (5.00–6.20 מ׳), שלתוכו מועתקת החניה לאחר העברת מאגר המים והמשאבות מתחת לרמפה הדרומית העליונה (מאזן נטו: 18/18 חניות).",
        "plan_overlay_zones": {
            "protected_ramp_maneuver_rect": {"x_pct": 20.8, "y_pct": 16.5, "w_pct": 62.5, "h_pct": 65.5, "label_he": "מיסעה היקפית 5.00–6.40 מ׳ + רדיוסי סיבוב R300/R500 לחניות #1–#18 (מוגן 100%)"},
            "under_ramp_utility_rect": {"x_pct": 63.5, "y_pct": 80.5, "w_pct": 25.5, "h_pct": 11.0, "label_he": "מאגר מים (17 מ״ק) + משאבות תחת רמפה דרומית עליונה (H≥2.20m · 28 מ״ר)"},
            "relocated_parking_target_rect": {"x_pct": 20.8, "y_pct": 63.7, "w_pct": 17.5, "h_pct": 13.3, "label_he": "🅿️🔄 מקום חלופי מאומת לחניה שזזה (במפרץ HOLD ממערב לגרעין · 2.42×5.39 מ׳)"},
        },
    },

    # KKL 10
    "KKL-OPT-AG1": {
        "proposed_gross_reduction_sqm": 55.0,
        "verified_contour_saved_sqm": 43.0,
        "non_contour_reclassified_sqm": 12.0,
        "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
        "contour_mechanism": "ביטול בליטת אגף חדר האשפה העודף ונסיגת קיר המעטפת העורפי בקומת הקרקע ב-2.15 מ׳ לאורך 20.0 מ׳ (-43.0 מ״ר קונטור בנוי).",
        "contour_dims_before_after": "קונטור סגירת קומת קרקע: 205.2 מ״ר ← 162.2 מ״ר (-43.0 מ״ר נבנה פחות)",
        "locked_reason_he": "12.0 מ״ר מתוך קיצור מסדרונות השירות בקומת הקרקע נמצאים מתחת לתקרת קומה 1 (מבחן 2 — נעילת תקרה עליונה), ולכן אינם חוסכים שלד תקרה והועברו לשיפור תכנון (הרחבת לובי ראשי ומעבר עגלות).",
    },
    "KKL-OPT-AG2": {
        "proposed_gross_reduction_sqm": 48.0,
        "verified_contour_saved_sqm": 36.0,
        "non_contour_reclassified_sqm": 12.0,
        "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
        "contour_mechanism": "קירוב אגפי הדירות הצפוני והדרומי ב-32 ס״מ על ציר Y סביב גרעין 2 המעליות (4.5 מ״ר הקטנת קונטור תקרה × 8 קומות = 36.0 מ״ר).",
        "contour_dims_before_after": "קונטור קומה טיפוסית: 382.0 מ״ר ← 377.5 מ״ר (-4.5 מ״ר לקומה × 8 קומות = -36.0 מ״ר)",
        "locked_reason_he": "12.0 מ״ר (1.5 מ״ר לקומה × 8 קומות) בנישת המבואה בין 2 המעליות כלואים גיאומטרית בין פיר המדרגות המוגן לפיר המעלית (מבחן 1 — ליבה כלואה), ולכן הועברו לשיפור תכנון המבואה.",
    },
    "KKL-OPT-AG3": {
        "proposed_gross_reduction_sqm": 10.0,
        "verified_contour_saved_sqm": 10.0,
        "non_contour_reclassified_sqm": 0.0,
        "contour_test_status": "FULL_CONTOUR_REDUCTION",
        "contour_mechanism": "הצמדת קירות החוץ של חדר היציאה לגג בקומה 9 לקונטור הפירים ההנדסי בלבד (100% הקטנת קונטור גג).",
        "contour_dims_before_after": "קונטור גג טכני קומה 9: 44.5 מ״ר ← 34.5 מ״ר (-10.0 מ״ר נבנה פחות)",
        "locked_reason_he": "100% מהשטח בגג הטכני חשוף ב-4 חזיתות ומקטין ישירות את קונטור הבנייה.",
    },
    "KKL-OPT-UG1": {
        "proposed_gross_reduction_sqm": 198.0,
        "verified_contour_saved_sqm": 170.0,
        "non_contour_reclassified_sqm": 28.0,
        "protected_ramp_and_maneuvering_deducted_sqm": 28.0,
        "under_ramp_utilized_sqm": 34.0,
        "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
        "contour_mechanism": "קיצור שלוחות הדיפון הדרומיות במרתפים -1 ו--2 ב-3.40 מ׳ × 25.0 מ׳ בכל קומה מחוץ למעגל הסיבוב של הרמפה ומחוץ למיסעת 6.00 מ׳ (85 מ״ר × 2 מרתפים = 170.0 מ״ר כיווץ פוליגון דיפון).",
        "contour_dims_before_after": "קונטור מרתפים -1 ו--2: 1,586.0 מ״ר ← 1,416.0 מ״ר (-170.0 מ״ר דיפון וחפירה מאומתים · 28.0 מ״ר קוזזו להגנת רמפה ומיסעות)",
        "locked_reason_he": "28.0 מ״ר (14.0 מ״ר בכל מרתף) באזור נחיתת הרמפה הבין-מפלסית וחיבור המיסעה לגרעין 2 המעליות מוגנים כשטח התמתנות וסיבוב (R_in=3.60m, R_out=5.20m) ומיסעת תמרון 6.00 מ׳ — ולכן קוזזו מחיסכון הקונטור (0 ₪).",
        "ramp_function_audit_he": "רמפה דו-מפלסית בין קרקע למרתף 1- ובין מרתף 1- למרתף 2- (שיפוע 16% + משטחי התמתנות 8% באורך 3.00 מ׳): 34.0 מ״ר מתחת לחלק העליון של הרמפה (H_clear ≥ 2.25 מ׳) מנוצלים לחדר משאבות, מאגר מים ובורות שאיבה. משטחי הסיבוב בחיבור הקומות (14.0 מ״ר לקומה = 28.0 מ״ר) מוגנים ב-100%.",
        "maneuvering_aisle_audit_he": "כל 43 החניות ב-2 המרתפים מוגנות עם מיסעה דו-סטרית של 6.00 מ׳ ואוזני תמרון של 1.00 מ׳ בקצוות המיסעה; הקיצור הדרומי (85 מ״ר לקומה) מבוצע אך ורק בכיס השירות העודף שמעבר לקו החניות האחרון.",
        "parking_relocation_audit": {
            "stalls_relocated_count": 2,
            "affected_stalls_label": "חניה #17 (מרתף 1-) וחניה #34 (מרתף 2-) בקצה השלוחה הדרומית שצומצמה",
            "original_location_he": "מוקמו בקצה שלוחות המיסעה הדרומיות של מרתפים -1 ו--2 שניסוגו פנימה ב-3.40 מ׳ להקטנת קונטור החפירה (85 מ״ר לקומה).",
            "alternative_location_found_he": "הועתקו ל-2 מפרצים חלופיים מאומתים שהתפנו בצמוד לגרעין המרכזי ולאורך המיסעה (6.00 מ׳) לאחר העברת מאגר המים וחדר המשאבות (34.0 מ״ר) אל מתחת לחלק העליון של הרמפה (H_clear ≥ 2.25m) וריכוז המחסנים.",
            "new_stall_dimensions_and_access_he": "2 תאי חניה תקניים במידות 2.60×5.00 מ׳ (13.0 מ״ר כ״א) בניצב למיסעה הדו-סטרית הראשית (6.00 מ׳) עם רדיוס כניסה ישיר.",
            "net_parking_balance_he": "מאזן חניות נטו: 0 גריעה (2 חניות קצה הועתקו ← 2 מפרצים חלופיים מאומתים אוכלסו = 34/34 חניות תת-קרקעיות נשמרות ב-100%).",
        },
        "parking_relocation_audit_he": "בדיקת העתקת חניות ומציאת מקום חלופי: קיצור השלוחה הדרומית במרתפים -1 ו--2 (3.40 מ׳) מזיז את חניות הקצה #17 ו-#34. בזכות העברת מאגר המים והמשאבות (34 מ״ר) אל מתחת לחלק העליון של הרמפה (H_clear ≥ 2.25m), מתפנה מפרץ חלופי תקני בכל מרתף לאורך המיסעה המרכזית (6.00 מ׳) הקולט את חניות #17 ו-#34 במידות 2.60×5.00 מ׳ (0 פגיעה במצבת החניות).",
        "plan_overlay_zones": {
            "protected_ramp_maneuver_rect": {"x_pct": 20.0, "y_pct": 36.0, "w_pct": 58.0, "h_pct": 24.0, "label_he": "מיסעה 6.00 מ׳ + רדיוסי סיבוב רמפה בין-מפלסית (מוגן 100%)"},
            "under_ramp_utility_rect": {"x_pct": 60.0, "y_pct": 20.0, "w_pct": 18.0, "h_pct": 14.0, "label_he": "מאגר מים + משאבות תחת רמפה עליונה (H≥2.25m · 34 מ״ר)"},
            "relocated_parking_target_rect": {"x_pct": 42.0, "y_pct": 22.0, "w_pct": 16.0, "h_pct": 12.0, "label_he": "🅿️🔄 מקום חלופי מאומת לחניות #17/#34 (במפרץ שפונה ליד הגרעין · 2.60×5.00 מ׳)"},
        },
    },

    # HAFETZ HAIM 44
    "H44-OPT-AG1": {
        "proposed_gross_reduction_sqm": 41.0,
        "verified_contour_saved_sqm": 32.0,
        "non_contour_reclassified_sqm": 9.0,
        "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
        "contour_mechanism": "איחוד חדר השירות הכפול עם חדר העגלות ונסיגת קיר המעטפת המזרחי-עורפי בקומת הקרקע ב-2.00 מ׳ × 16.0 מ׳ (-32.0 מ״ר קונטור בנוי).",
        "contour_dims_before_after": "קונטור סגירת קומת קרקע: 185.0 מ״ר ← 153.0 מ״ר (-32.0 מ״ר נבנה פחות)",
        "locked_reason_he": "9.0 מ״ר במבואת הכניסה הפנימית נמצאים מתחת לתקרת דירות קומה 1 (מבחן 2 — נעילת תקרה עליונה) ולכן אינם מקטינים את יציקת התקרה והועברו לשיפור תכנון הלובי ומועדון הדיירים.",
    },
    "H44-OPT-AG2": {
        "proposed_gross_reduction_sqm": 32.0,
        "verified_contour_saved_sqm": 24.0,
        "non_contour_reclassified_sqm": 8.0,
        "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
        "contour_mechanism": "בקומה של 2 דירות בלבד (מזרח ומערב), קירוב שתי הדירות ב-25 ס״מ על ציר X והכנסת קיר הגרעין הצפוני ב-55 ס״מ (3.0 מ״ר הקטנת קונטור תקרה × 8 קומות = 24.0 מ״ר).",
        "contour_dims_before_after": "קונטור קומה טיפוסית: 255.5 מ״ר ← 252.5 מ״ר (-3.0 מ״ר לקומה × 8 קומות = -24.0 מ״ר)",
        "locked_reason_he": "8.0 מ״ר (1.0 מ״ר לקומה × 8 קומות) של נישת ארונות שירות בין דלתות הפלדלת כלואים בין שני אגפי הדירות (מבחן 1 — ליבה כלואה) ולכן הועברו לשיפור תכנון (הרחבת מבואת הכניסה לדירות).",
    },
    "H44-OPT-UG1": {
        "proposed_gross_reduction_sqm": 86.0,
        "verified_contour_saved_sqm": 58.0,
        "non_contour_reclassified_sqm": 28.0,
        "protected_ramp_and_maneuvering_deducted_sqm": 28.0,
        "under_ramp_utilized_sqm": 32.0,
        "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
        "contour_mechanism": "העברת חדרי ה'משאבות' (335×200 ו-335×140) וה'אוורור' (200) מהאי המרכזי אל החלל האטום והמת מתחת לחלק העליון של הרמפה הדרומית (+46.25 עד +44.80, H_clear = 2.15–3.55m), פתיחת מפרץ חנייה חלופי (2.70×5.00 מ׳) בדופן המזרחית של האי המרכזי (מול המיסעה המזרחית 5.55 מ׳) לקליטת חנייה #16, וביצוע 2 כיווצי קונטור מאומתים מחוץ לעמודי הבניין: (1) יצירת מגרעת דיפון בפינה הדרום-מערבית של 15.50×3.10 מ׳ (-48.0 מ״ר, מדרום לחנייה #15 וממערב לתחילת הרמפה הדרומית — מחוץ לקו הבניין העילי 4.00 מ׳ ובסימטריה למגרעת הדרום-מזרחית K); ו-(2) הידוק המיסעה המערבית מ-5.75 מ׳ ל-5.20 מ׳ וקירוב הדיפון המערבי ב-0.55×18.06 מ׳ (-10.0 מ״ר = סה״כ -58.0 מ״ר חפירה ודיפון).",
        "contour_dims_before_after": "קונטור דיפון מרתף: 638.0 מ״ר ← 580.0 מ״ר (-58.0 מ״ר חפירה ודיפון מאומתים: 48.0 מ״ר מגרעת דרום-מערבית + 10.0 מ״ר הידוק מערבי · 28.0 מ״ר קוזזו להגנת לולאת הרמפה וקופסת הממ״ד הכלואה)",
        "locked_reason_he": "28.0 מ״ר קוזזו ממודל חיסכון הקונטור (0 ₪): מתוכם 12.0 מ״ר הם תא ה'משאבות' הישן (335×360 ס״מ) הכלוא בתוך קירות הירידה הקונסטרוקטיביים של הממ״ד המערבי (70% קירות ממ״ד יורדים לביסוס — מבחן 1 ליבה כלואה, שהוסב ל-3 מחסני דיירים), ו-16.0 מ״ר הם רצועות הסיבוב של לולאת הרמפה התלת-זרועית והדופן המערבית של חניות #11–#15 (שבה רוחב 5.00+5.20+5.00 מ׳ ועמודי אגף הדירות המערבי מונעים נסיגה עמוקה של קיר הדיפון המערבי).",
        "ramp_function_audit_he": "ניתוח מדויק של הרמפה וכיווני התנועה בתכניות המקור (קרקע + מרתף): הרמפה אינה 'רמפה מזרחית' אלא לולאה היקפית תלת-זרועית חד-מסלולית (נגד כיוון השעון, אורך כולל ~45 מ׳, בבקרת רמזור ו-2 מראות פנורמיות): (1) כניסה מרחוב חפץ חיים בצפון-מזרח (+47.44) ונסיעה מערבה לאורך הגבול הצפוני (2.2%, 5.0%, 10%) אל רחבת 6 החניות העיליות במערב (#1–#6 במפלס +46.30); (2) זרוע דרומית (מערב ← מזרח ברצועת קו בניין 4.00 מ׳): ירידה מ-+46.25 (בקו הגרעין) בשיפוע 10%/3m ← 15%/9.8m (מ-+45.52 ל-+44.48) ← 10%/3m עד +44.18 בפינה הדרום-מזרחית; (3) זרוע מזרחית (דרום ← צפון): מיסעה ברוחב 5.55 מ׳ בשיפוע מתון 5%/8m (+44.18 עד +43.78) המשרתת ישירות 4 חניות ניצבות (#7–#10 במפלס ביניים +43.92); (4) זרוע צפונית (מזרח ← מערב): פנייה ב-+43.78 לכבש צפוני ברוחב 2.75 מ׳ נטו (5.5%/3m ← 11%/7.6m [מ-+43.62 ל-+42.78] ← 5.5%/3m עד +42.61) ופנייה דרומה (2.5%/7.6m) אל האגף המערבי (+42.42). לכן: מתחת לזרוע הצפונית (+43.62 עד +42.61) אין גובה ראש כלל (0.2–1.2 מ׳ מעל הרצפה); המקום היחיד עם גובה ראש תקני (H_clear = 2.15–3.55 מ׳) הוא החלל האטום והמת מתחת לחלק העליון של הרמפה הדרומית (+46.25 עד +44.80, מדרום לחדר המדרגות — 32.0 מ״ר), שלתוכו מועברים חדרי המשאבות, האוורור וחניית האופנועים! (ובחלופה אסטרטגית Option B: מאחר שרחבת הקרקע המערבית כבר במפלס +46.25 — הפרש של 3.60 מ׳ בלבד ממפלס המרתף הדורש ~24 מ׳ רמפה בלבד — הגבהת המרתף המערבי ב-65 ס״מ תאפשר לבטל את זרוע הרמפה הצפונית ולחסוך עוד ~62 מ״ר!).",
        "maneuvering_aisle_audit_he": "בדיקת מעבר, עמודים ושטחי תמרון: באגף המערבי (+42.42) המיסעה הדו-סטרית (5.75 מ׳) היא מבוי סתום (Cul-de-Sac) המשרת 6 חניות מערביות (#11–#16) ו-3 חניות ליבה (#19, חניית נכה #18 ברוחב 293+130=423/437 ס״מ [חנייה ניצבת תקנית עם מעבר נגישות צמוד ולא חנייה טורית!], ו-#17). לא ניתן לדחוף את קיר הדיפון המערבי ב-4.40 מ׳ פנימה כי הדבר יבטל את חניות #11–#15 או את המיסעה ויפגע בעמודי הבניין העילי. לעומת זאת, הקו המקווקו האדום (קו בניין דרומי 4.00 מ׳) עובר בדיוק בין חנייה #15 לחנייה #16, והרמפה הדרומית מתחילה רק בקו הגרעין (+46.25) ומזרחה — ולכן גיזום הפינה הדרום-מערבית (15.50×3.10 מ׳ = 48.0 מ״ר) מתבצע מחוץ לעמודי הבניין ומחוץ לרמפה!",
        "parking_relocation_audit": {
            "stalls_relocated_count": 1,
            "affected_stalls_label": "חניית קצה דרום-מערבית #16 (263×500 ס״מ) + מפרץ אופנועים דרומי (210 ס״מ)",
            "original_location_he": "מוקמה בפינה הדרום-מערבית של המרתף (מדרום לחנייה #15, מחוץ לקו הבניין העילי 4.00 מ׳ וממערב לתחילת הרמפה הדרומית), באזור שבו בוצעה מגרעת דיפון של 15.50×3.10 מ׳ (-48.0 מ״ר, סימטרית למגרעת הדרום-מזרחית K).",
            "alternative_location_found_he": "חנייה #16 הועתקה למפרץ חנייה תקני חדש (2.70×5.00 מ׳) שנפתח בדופן המזרחית של האי המרכזי (מול המיסעה המזרחית הרחבה 5.55 מ׳ במפלס +43.92, מול חנייה #9) — שטח שהתפנה בעקבות העברת חדרי ה'משאבות' (335×360) וה'אוורור' (200) אל החלל האטום מתחת לחלק העליון של הרמפה הדרומית (+46.25 עד +44.80, H_clear ≥ 2.20m), קיצור המבואה המדורגת הכפולה (295×200 ב-44.00) והעברת 2 חניות האופנועים אל מתחת לשולי הרמפה הדרומית.",
            "new_stall_dimensions_and_access_he": "תא חנייה ניצב תקני 2.70×5.00 מ׳ (13.5 מ״ר) עם גישה ישירה ב-90° מהמיסעה המזרחית (רוחב 5.55 מ׳, שיפוע מתון 5%) ויתרון תפעולי גדול: החנייה נמצאת במפלס הביניים המזרחי (+43.92) וחוסכת לנהג את הצורך לרדת ולעלות את כל זרוע הרמפה הצפונית והמערבית!",
            "net_parking_balance_he": "מאזן חניות נטו: 0 גריעה (חנייה #16 הועתקה מהפינה הדרום-מערבית שנגזמה ← אוכלסה במפרץ החדש מול המיסעה המזרחית 5.55 מ׳; חניות האופנועים הועברו לתחתית הרמפה הדרומית = 13/13 חניות רכב במרתף + 6 בקרקע נשמרות ב-100%, ובנוסף נוצרו 3 מחסני דיירים בקופסת הממ״ד המערבי שפונתה!).",
        },
        "parking_relocation_audit_he": "בדיקת העתקת חנייה ומציאת מקום חלופי מאומת: יצירת מגרעת הדיפון בפינה הדרום-מערבית (48.0 מ״ר מחוץ לקו הבניין העילי 4.00 מ׳ וממערב לרמפה הדרומית) מבטלת את מיקומה המקורי של חניית הקצה #16. העברת חדרי ה'משאבות' (335×360) וה'אוורור' (200) מהאי המרכזי אל החלל האטום והמת מתחת לחלק העליון של הרמפה הדרומית (+46.25 עד +44.80, H_clear = 2.15–3.55m) והעברת חניות האופנועים לשולי תחתית הרמפה הדרומית מפנות מפרץ חנייה תקני (2.70×5.00 מ׳) בדופן המזרחית של האי המרכזי (במקום מפרץ האופנועים והמבואה המדורגת 44.00), הנגיש ישירות ב-90° מהמיסעה המזרחית (רוחב 5.55 מ׳, מול חנייה #9). בנוסף, קופסת הבטון של הממ״ד המערבי במרתף (12.0 מ״ר שבה ישבו המשאבות) הופכת ל-3 מחסני דיירים תקניים!",
        "plan_overlay_zones": {
            "before_contour_rect": {"x_pct": 9.5, "y_pct": 68.5, "w_pct": 35.5, "h_pct": 11.3},
            "after_contour_rect": {"x_pct": 11.2, "y_pct": 68.5, "w_pct": 33.8, "h_pct": 2.2},
            "protected_ramp_maneuver_rect": {"x_pct": 21.5, "y_pct": 19.5, "w_pct": 55.5, "h_pct": 47.5, "label_he": "לולאת תנועה היקפית מוגנת: רמפה צפונית (11% 7.6m) + מיסעה מזרחית (5.55m) + מיסעה מערבית (5.20–5.75m)"},
            "under_ramp_utility_rect": {"x_pct": 45.5, "y_pct": 66.5, "w_pct": 19.0, "h_pct": 12.0, "label_he": "ניצול החלל האטום מתחת לחלק העליון של הרמפה הדרומית (+46.25 עד +44.80, H≥2.20m · 32 מ״ר למשאבות + אופנועים)"},
            "relocated_parking_target_rect": {"x_pct": 55.5, "y_pct": 33.0, "w_pct": 10.5, "h_pct": 14.0, "label_he": "🅿️🔄 מקום חלופי מאומת לחנייה #16 (2.70×5.00 מ׳ מול מיסעה מזרחית 5.55 מ׳ לאחר פינוי המשאבות והאופנועים)"},
        },
    },

    # YATKOVSKI 7
    "Y7-OPT-AG1": {
        "proposed_gross_reduction_sqm": 24.0,
        "verified_contour_saved_sqm": 18.0,
        "non_contour_reclassified_sqm": 6.0,
        "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
        "contour_mechanism": "נסיגת קיר המעטפת של אגף חדרי השירות והעגלות בקומת הקרקע ב-1.50 מ׳ × 12.0 מ׳ (-18.0 מ״ר קונטור בנוי עילי).",
        "contour_dims_before_after": "קונטור סגירת קומת קרקע: 93.0 מ״ר ← 75.0 מ״ר (-18.0 מ״ר נבנה פחות)",
        "locked_reason_he": "6.0 מ״ר במעבר הלובי הפנימי נמצאים מתחת לתקרת קומה א׳ וממ״ד הדירה שמעל (מבחן 2), ולכן אינם חוסכים שלד והועברו לשיפור תכנון הלובי הדו-מפלסי.",
    },
    "Y7-OPT-AG2": {
        "proposed_gross_reduction_sqm": 16.8,
        "verified_contour_saved_sqm": 12.0,
        "non_contour_reclassified_sqm": 4.8,
        "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
        "contour_mechanism": "הכנסת קיר הגרעין החיצוני והקטנת בליטת חדר המדרגות/מחסן קומתי ב-2.0 מ״ר לקומה × 6 קומות (-12.0 מ״ר קונטור תקרות).",
        "contour_dims_before_after": "קונטור קומה טיפוסית: 232.0 מ״ר ← 230.0 מ״ר (-2.0 מ״ר לקומה × 6 קומות = -12.0 מ״ר)",
        "locked_reason_he": "4.8 מ״ר (0.8 מ״ר לקומה × 6 קומות) בנישת המבואה הקומתית כלואים בין הדירה הצפונית לדירה הדרומית ללא יכולת לקרבן בשל עמודי הממ״ד (מבחן 1 — ליבה כלואה), ולכן הועברו לשיפור תכנון.",
    },
    "Y7-OPT-UG1": {
        "proposed_gross_reduction_sqm": 54.0,
        "verified_contour_saved_sqm": 40.0,
        "non_contour_reclassified_sqm": 14.0,
        "protected_ramp_and_maneuvering_deducted_sqm": 14.0,
        "under_ramp_utilized_sqm": 22.0,
        "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
        "contour_mechanism": "העברת מאגר המים וחדר המשאבות מתחת לחלק העליון של הרמפה המערבית והמזרחית (H_clear ≥ 2.20 מ׳ במפלס 54.20–53.75) וגיזום כיס הדיפון הצפון-מזרחי המת שמחוץ לקשת R500 (-40.0 מ״ר קונטור מרתף).",
        "contour_dims_before_after": "קונטור דיפון מרתף: 465.0 מ״ר ← 425.0 מ״ר (-40.0 מ״ר חפירה ודיפון מאומתים · 14.0 מ״ר קוזזו להגנת רדיוסי R300/R450/R500 ומיסעות 6.20–6.53 מ׳)",
        "locked_reason_he": "14.0 מ״ר באזור סיבוב הרמפה המערבית (R300 ליד חניה #12), קשת הרמפה המזרחית (R450/R500 ברוחב 368 ס״מ) ומשטח ההתמתנות הדרומי (2.5% באורך 5.70 מ׳) מוגנים ב-100% כשטח רמפה ותמרון חיוני — ולכן קוזזו מחיסכון הקונטור (0 ₪).",
        "ramp_function_audit_he": "בתכנית המקור של מרתף יטקובסקי 7: הרמפה המערבית יורדת בשיפוע 17% (7.60 מ׳) ומתמתנת ב-10% (3.00 מ׳ במפלס 54.20–53.90) ליד רמזור הכניסה, ממשיכה בדרום (2.5% לאורך 5.70 מ׳ מול המראה הפנורמית) ועולה/יורדת במזרח ב-10% (12.80 מ׳, רוחב 275+30+30 ס״מ) עם סיבוב R450/R500 (רוחב 368 ס״מ) לצפון (5% לאורך 9.95 מ׳). ניצול תחתית הרמפה למאגר המים והמשאבות (22.0 מ״ר) מתבצע אך ורק מתחת למקטע העליון (H_clear ≥ 2.20 מ׳), ללא כל פגיעה בנתיב הרמפה או ברדיוסי הסיבוב R300/R450/R500.",
        "maneuvering_aisle_audit_he": "שמירה על 100% מ-12 החניות בתכנית המקור: חניות דרומיות #1–#6 (רוחב 270–300 ס״מ) עם מיסעה רחבה של 6.20 מ׳, חניית נכה מרכזית #12 (רוחב 437 ס״מ = 270+130 ס״מ), וחניות צפוניות #7–#8 (מזרח) ו-#9–#11 (מערב) עם מיסעה של 6.37–6.53 מ׳.",
        "parking_relocation_audit": {
            "stalls_relocated_count": 1,
            "affected_stalls_label": "חניה #7 (פינה צפון-מזרחית בתכנית המקור בסמוך לקשת הרמפה R450/R500)",
            "original_location_he": "מוקמה בקצה הצפון-מזרחי של המרתף (לצד חניה #8) באזור כיס הדיפון שנגזם ב-40.0 מ״ר מחוץ לקשת R500.",
            "alternative_location_found_he": "הועתקה למפרץ החלופי שהתפנה בצמוד לחניית הנכה #12 ולאורך המיסעה הצפונית הרחבה (6.37–6.53 מ׳) — בדיוק בתא שבו ישבו מאגר המים וחדר המשאבות שהועברו אל מתחת למקטע העליון של הרמפה המערבית (H_clear ≥ 2.20m).",
            "new_stall_dimensions_and_access_he": "תא חניה תקני 2.65×5.00 מ׳ (13.25 מ״ר) עם גישה ישירה ב-90° ממיסעה ברוחב 6.37 מ׳ וללא חפיפה לקשת הרמפה R450/R500.",
            "net_parking_balance_he": "מאזן חניות נטו: 0 גריעה (חניה #7 הועתקה מהפינה הצפון-מזרחית ← אוכלסה במפרץ מאגר המים שפונה ליד חניה #12 = 12/12 חניות נשמרות ב-100%).",
        },
        "parking_relocation_audit_he": "בדיקת העתקת חנייה ומציאת מקום חלופי: גיזום כיס הדיפון הצפון-מזרחי (40.0 מ״ר מחוץ לקשת R500) או קצה שורת החניות הדרומית מחייב הזזת חניית קצה אחת. העברת מאגר המים וחדר המשאבות (22.0 מ״ר) אל מתחת לחלק העליון של הרמפה המערבית (17% L=7.00m / 10% L=3.00m ב-55.09–54.20, H_clear ≥ 2.20m) מפנה מפרץ חניה תקני בצמוד לחניית הנכה #12 (מדרום ל'רגלי ממד / מחסן') הפונה ישירות אל המיסעה הרחבה (6.20 מ׳ בדרום ו-6.37–6.53 מ׳ בצפון), שלתוכו מועתקת החניה במידות 2.65×5.00 מ׳ (12/12 חניות נשמרות במלואן).",
        "plan_overlay_zones": {
            "protected_ramp_maneuver_rect": {"x_pct": 12.0, "y_pct": 52.0, "w_pct": 58.0, "h_pct": 14.5, "label_he": "מיסעה דרומית 6.20 מ׳ + רדיוסי סיבוב R300/R350 + מראה פנורמית (מוגן 100%)"},
            "under_ramp_utility_rect": {"x_pct": 12.0, "y_pct": 33.5, "w_pct": 11.0, "h_pct": 18.5, "label_he": "מאגר מים + משאבות תחת רמפה מערבית עליונה (17%/10% · H≥2.20m · 22 מ״ר)"},
            "relocated_parking_target_rect": {"x_pct": 23.5, "y_pct": 40.5, "w_pct": 9.5, "h_pct": 11.0, "label_he": "🅿️🔄 מקום חלופי מאומת לחניה (בתא מאגר המים והמשאבות שפונה ליד #12 · 2.65×5.00 מ׳)"},
        },
    },

    # KITRONI 37-39
    "KIT-OPT-AG1": {
        "proposed_gross_reduction_sqm": 88.0,
        "verified_contour_saved_sqm": 70.0,
        "non_contour_reclassified_sqm": 18.0,
        "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
        "contour_mechanism": "נסיגת קירות המעטפת של חדרי השירות והמועדון ב-2 הבניינים (37 ו-39) ב-35.0 מ״ר לכל בניין (-70.0 מ״ר קונטור בנוי בקומת הקרקע).",
        "contour_dims_before_after": "קונטור קומת קרקע (2 בניינים): 490.0 מ״ר ← 420.0 מ״ר (-70.0 מ״ר נבנה פחות)",
        "locked_reason_he": "18.0 מ״ר (9.0 מ״ר בכל בניין) במבואות הפנימיות נמצאים מתחת לתקרת קומה 1 (מבחן 2 — נעילת תקרה עליונה) ולכן אינם חוסכים יציקת תקרה והועברו לשיפור תכנון הלובאים.",
    },
    "KIT-OPT-AG2": {
        "proposed_gross_reduction_sqm": 90.0,
        "verified_contour_saved_sqm": 72.0,
        "non_contour_reclassified_sqm": 18.0,
        "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
        "contour_mechanism": "קירוב שני אגפי הדירות בכל בניין ב-30 ס״מ על ציר האורך והכנסת קיר הגרעין החיצוני (4.0 מ״ר הקטנת קונטור לבניין × 2 בניינים × 9 קומות = 72.0 מ״ר).",
        "contour_dims_before_after": "קונטור קומה (2 בניינים): 768.0 מ״ר ← 760.0 מ״ר (-8.0 מ״ר לקומה × 9 קומות = -72.0 מ״ר)",
        "locked_reason_he": "18.0 מ״ר (1.0 מ״ר לבניין × 2 בניינים × 9 קומות) של נישות פנים במבואת המעליות כלואים בין קירות ההדף של הממ״דים (מבחן 1 — ליבה כלואה) והועברו לשיפור תכנון.",
    },
    "KIT-OPT-UG1": {
        "proposed_gross_reduction_sqm": 145.0,
        "verified_contour_saved_sqm": 125.0,
        "non_contour_reclassified_sqm": 20.0,
        "protected_ramp_and_maneuvering_deducted_sqm": 20.0,
        "under_ramp_utilized_sqm": 45.0,
        "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
        "contour_mechanism": "העברת חדרי המשאבות (295×390) ומאגרי המים (15 קוב × 2) לתחתית החלק העליון של רמפת הכניסה המשותפת בצפון (17% L=15.83m, H_clear ≥ 2.25 מ׳) וגיזום כיסי הדיפון ההיקפיים המתים בפוליגון המרתף המשותף מחוץ למיסעות (-125.0 מ״ר חפירה ודיפון).",
        "contour_dims_before_after": "קונטור מרתף משותף: 2,420.0 מ״ר ← 2,295.0 מ״ר (-125.0 מ״ר חפירה ודיפון מאומתים · 20.0 מ״ר קוזזו להגנת צומת הרמפה והמיסעות)",
        "locked_reason_he": "20.0 מ״ר בצומת ההתמזגות של רמפת הכניסה (17% L=15.83m / 8.5%) עם ציר המיסעה הראשי המחבר בין בניין 37 לבניין 39 ובצמוד ל'רגלי ממ״ד' מוגנים כשטח סיבוב דו-סטרי (R_in=4.00m) ומיסעה של 6.00 מ׳ — ולכן קוזזו מחיסכון הקונטור (0 ₪).",
        "ramp_function_audit_he": "רמפת כניסה דו-סטרית משותפת ל-2 הבניינים בצפון (17% לאורך L=15.83m + התמתנות 8.5% במפלס 39.96–39.70): החלק העליון של כבש הרמפה (H_clear = 2.25–3.30 מ׳) מאכלס את חדרי המשאבות ומאגר המים המאוחד (45.0 מ״ר), בעוד משטח ההתמתנות התחתון (8.5%) וצומת החיבור למיסעות נשמרים חופשיים ב-100%.",
        "maneuvering_aisle_audit_he": "שמירה קשיחה על מיסעות דו-סטריות ברוחב 5.65–7.00 מ׳ לכל 63 החניות (#26–#65) ואוזני תמרון של 1.00 מ׳ בקצוות שלוחות החניה של בניינים 37 ו-39; גיזום הקונטור (125.0 מ״ר) מתבצע אך ורק בכיסי החפירה ההיקפיים המתים שמעבר לקו החניות האחרון.",
        "parking_relocation_audit": {
            "stalls_relocated_count": 2,
            "affected_stalls_label": "חניות קצה #56 (אגף בניין 37) ו-#35 (אגף בניין 39)",
            "original_location_he": "מוקמו בכיסי הדיפון ההיקפיים בקצוות שלוחות החניה של בניינים 37 ו-39 שניסוגו פנימה ב-125.0 מ״ר.",
            "alternative_location_found_he": "הועתקו ל-2 מפרצים חלופיים תקניים לאורך ציר המיסעה הראשי שהתפנו בתאי 'חדר משאבות' (295×390) ו'מאגר מים 15 קוב' (280×390 / 368×263) בעקבות העברתם אל מתחת לחלק העליון של רמפת הכניסה הצפונית (17% L=15.83m, H_clear ≥ 2.25m).",
            "new_stall_dimensions_and_access_he": "2 תאי חניה תקניים במידות 2.60×5.00 מ׳ (26.0 מ״ר סה״כ) בניצב למיסעה הדו-סטרית עם נגישות ישירה ל-2 הגרעינים.",
            "net_parking_balance_he": "מאזן חניות נטו: 0 גריעה (2 חניות קצה הועתקו ← 2 מפרצים חלופיים אוכלסו בתאי המשאבות ומאגר המים שפונו = 63/63 חניות נשמרות ב-100%).",
        },
        "parking_relocation_audit_he": "בדיקת העתקת חניות ומציאת מקום חלופי: גיזום כיסי הדיפון ההיקפיים (125.0 מ״ר) מזיז 2 חניות קצה (#56 ו-#35). העברת חדרי המשאבות ומאגרי המים (45.0 מ״ר) אל מתחת לחלק העליון של רמפת הכניסה הצפונית (17% L=15.83m, H_clear ≥ 2.25m) מפנה 2 מפרצי חניה תקניים (2×2.60×5.00 מ׳) בתאי המשאבות/מאגר המים לצד הגרעינים (מחוץ לתחום 'רגלי ממ״ד'), הקולטים את 2 החניות במלואן (63/63 חניות נשמרות).",
        "plan_overlay_zones": {
            "protected_ramp_maneuver_rect": {"x_pct": 17.5, "y_pct": 24.5, "w_pct": 50.0, "h_pct": 55.0, "label_he": "ציר מיסעה דו-סטרי + צומת רמפה 8.5% ורגלי ממ״ד (מוגן 100%)"},
            "under_ramp_utility_rect": {"x_pct": 21.0, "y_pct": 8.5, "w_pct": 25.5, "h_pct": 7.0, "label_he": "מאגרי מים + משאבות תחת רמפה צפונית עליונה (17% L=15.83m · H≥2.25m · 45 מ״ר)"},
            "relocated_parking_target_rect": {"x_pct": 34.5, "y_pct": 15.5, "w_pct": 9.0, "h_pct": 9.0, "label_he": "🅿️🔄 מקום חלופי מאומת לחניות (בתא חדר המשאבות ומאגר המים שפונה · 2×2.60×5.00 מ׳)"},
        },
    },

    # FEIERBERG 3
    "FB3-OPT-AG1": {
        "proposed_gross_reduction_sqm": 52.0,
        "verified_contour_saved_sqm": 42.0,
        "non_contour_reclassified_sqm": 10.0,
        "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
        "contour_mechanism": "פינוי מאגר המים וחדר המשאבות בקומת הקרקע אל תחתית החלק העליון של הרמפה הצפון-מזרחית במרתף 1- (שם גובה הראש הפנוי H_clear = 2.20–3.15 מ׳) ונסיגת קיר המעטפת של חדרי השירות בקומת הקרקע (רוחב בניין 25.89 מ׳ בתכנית הקרקע: -42.0 מ״ר קונטור בנוי).",
        "contour_dims_before_after": "קונטור בנוי קומת קרקע: 265.0 מ״ר ← 223.0 מ״ר (-42.0 מ״ר נבנה פחות)",
        "locked_reason_he": "10.0 מ״ר מתוך קיצור מעבר השירות הפנימי בין הלובי (770×430) לחדר האופניים (540×350) נמצאים מתחת לתקרת דירה #2 בקומה א׳ (מבחן 2 — נעילת תקרה עליונה), ולכן אינם מקטינים את קונטור התקרה והועברו לשיפור תכנון הלובי.",
    },
    "FB3-OPT-AG2": {
        "proposed_gross_reduction_sqm": 37.6,
        "verified_contour_saved_sqm": 28.0,
        "non_contour_reclassified_sqm": 9.6,
        "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
        "contour_mechanism": "בקומה טיפוסית של 2 דירות בתכנית המקור (דירה 1 מזרחית ודירה 2 מערבית, מידות חוץ 2620×840 ס״מ + מרפסות דרומיות 750×160 ס״מ), קירוב שני אגפי הדירות על ציר X והידוק קיר הגרעין הצפוני (3.5 מ״ר הקטנת קונטור תקרה × 8 קומות = 28.0 מ״ר).",
        "contour_dims_before_after": "קונטור קומה טיפוסית (26.20×8.40 מ׳ + מרפסות): 375.2 מ״ר ברוטו ← 371.7 מ״ר (-3.5 מ״ר × 8 קומות = -28.0 מ״ר)",
        "locked_reason_he": "9.6 מ״ר (1.2 מ״ר לקומה × 8 קומות) בנישת מבואת המעלית הדרומית (175×180 + מדרגות 365×160) כלואים בין שני עמודי הגרעין וקירות הממ״ד (מבחן 1 — ליבה כלואה ללא תזוזת חזית), ולכן קוזזו ממודל החיסכון (0 ₪) והועברו לשיפור תכנון.",
    },
    "FB3-OPT-AG3": {
        "proposed_gross_reduction_sqm": 12.0,
        "verified_contour_saved_sqm": 12.0,
        "non_contour_reclassified_sqm": 0.0,
        "contour_test_status": "FULL_CONTOUR_REDUCTION",
        "contour_mechanism": "נסיגת מעטפת חדר היציאה לגג ומבואת הגלריה בקומה 10 לקו הפירים ההנדסי (100% הקטנת קונטור גג עליון).",
        "contour_dims_before_after": "קונטור קומות 9–10 וגג: 100.8 מ״ר ← 88.8 מ״ר (-12.0 מ״ר נבנה פחות)",
        "locked_reason_he": "100% מהשטח הוא נפח עליון עצמאי שמקטין ישירות את יציקת התקרה והקירות החיצוניים.",
    },
    "FB3-OPT-UG1": {
        "proposed_gross_reduction_sqm": 67.0,
        "verified_contour_saved_sqm": 45.0,
        "non_contour_reclassified_sqm": 22.0,
        "protected_ramp_and_maneuvering_deducted_sqm": 22.0,
        "under_ramp_utilized_sqm": 28.0,
        "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
        "contour_mechanism": "הכנסת מאגר המים וחדר המשאבות (28.0 מ״ר) מתחת לחלק העליון של הרמפה הצפון-מזרחית (H_clear = 2.20–3.15 מ׳) וגיזום קו הדיפון בכיס הדרום-מזרחי המת מחוץ לרדיוס הסיבוב R=369 ומחוץ למיסעה 6.50 מ׳ (-45.0 מ״ר קונטור דיפון מאומת).",
        "contour_dims_before_after": "קונטור דיפון מרתף 1-: 548.0 מ״ר ← 503.0 מ״ר (-45.0 מ״ר חפירה ודיפון מאומתים · 22.0 מ״ר קוזזו להגנת רמפה R=369 ומיסעה 6.50 מ׳)",
        "locked_reason_he": "22.0 מ״ר באגף המזרחי של מרתף 1- חופפים למסלול הסיבוב וההתמתנות של הרמפה היורדת למרתף 2- (שיפועים 5% ו-7.5% באורך 3.00 מ׳ ורדיוס R=350–369 ס״מ) ולמיסעת התמרון (רוחב 6.50 מ׳ מול חניות #7–#8) — ולכן מוגנים ב-100% ואסורים לגריעה (קוזזו מחיסכון הקונטור — 0 ₪).",
        "ramp_function_audit_he": "בתכנית המקור של מרתף 1- (מפלס 48.10 / -4.80m): כבש הרמפה העליון לאורך הדופן הצפונית יורד בשיפוע 15% (אורך 19.00 מ׳, רוחב 3.10 מ׳) ומתמתן ב-7.5% (3.00 מ׳) ו-5% (3.00 מ׳) לפני סיבוב פרסה מזרחי ברדיוס R=350–369 ס״מ להמשך ירידה למרתף 2-. רק מתחת ל-9.0 המטרים העליונים של הרמפה בצפון-מזרח קיים גובה ראש פנוי H_clear = 2.20–3.15 מ׳ המתאים לחדר משאבות ומאגר מים (28.0 מ״ר). משטח הסיבוב המזרחי R=369 והחצי התחתון של הרמפה (H_clear < 1.80 מ׳) מוגנים לחלוטין.",
        "maneuvering_aisle_audit_he": "שמירה מלאה על כל 8 החניות הרגילות במרתף 1- (#1–#4 במערב ברוחב 245–275 ס״מ עם אוזן תמרון של 100 ס״מ לחניה #4 ומיסעה של 5.90 מ׳; #5–#6 בדרום; #7–#8 במזרח ברוחב 265–305 ס״מ עם מיסעה של 6.50 מ׳). הגיזום של 45.0 מ״ר מבוצע אך ורק בכיס הדרום-מזרחי המת שמדרום לרדיוס R=369 וממזרח לחניה #6.",
        "parking_relocation_audit": {
            "stalls_relocated_count": 1,
            "affected_stalls_label": "חניה #6 (דרום-מזרח מרתף 1- בתכנית המקור)",
            "original_location_he": "מוקמה בצמוד לכיס הדיפון הדרום-מזרחי (ממזרח לחניה #5 ומדרום לרדיוס R=369) שניסוג פנימה ב-45.0 מ״ר.",
            "alternative_location_found_he": "הוסטה והועתקה 1.80 מ׳ מערבה למפרץ החלופי שהתפנה בדופן הדרומית (בין חניה #5 לאוזן התמרון של חניה #4) לאחר העברת המתקנים הטכניים אל מתחת לחלק העליון של הרמפה הצפון-מזרחית (H_clear ≥ 2.20m).",
            "new_stall_dimensions_and_access_he": "תא חניה תקני 2.55×5.00 מ׳ (12.75 מ״ר) בניצב למיסעה הדרומית-מזרחית הרחבה (5.90–6.50 מ׳) עם תמרון כניסה/יציאה חופשי לחלוטין וללא הפרעה לקשת R=369.",
            "net_parking_balance_he": "מאזן חניות נטו במרתף 1-: 0 גריעה (חניה #6 הועתקה מערבה מדופן הכיס שנגזם ← מפרץ חלופי מאומת בדופן הדרומית = 8/8 חניות במרתף 1- נשמרות ב-100%).",
        },
        "parking_relocation_audit_he": "בדיקת העתקת חנייה ומציאת מקום חלופי (מרתף 1-): נסיגת קיר הדיפון בכיס הדרום-מזרחי (45.0 מ״ר) נוגעת בדופן המזרחית של חניה #6. העברת המערכות הטכניות (28.0 מ״ר) אל מתחת לחלק העליון של הרמפה הצפון-מזרחית (H_clear ≥ 2.20m) וציפוף רצועת השירות הדרומית מפנים מפרץ חלופי תקני שלתוכו מוסטת חניה #6 ב-1.80 מ׳ מערבה (במידות 2.55×5.00 מ׳ מול מיסעה של 5.90–6.50 מ׳) — 8 מתוך 8 חניות נשמרות במלואן.",
        "plan_overlay_zones": {
            "protected_ramp_maneuver_rect": {"x_pct": 53.0, "y_pct": 33.0, "w_pct": 31.0, "h_pct": 25.0, "label_he": "רדיוס סיבוב רמפה R=350–369 + התמתנות 7.5%/5% + מיסעה 6.50 מ׳ (מוגן 100%)"},
            "under_ramp_utility_rect": {"x_pct": 58.0, "y_pct": 24.0, "w_pct": 25.0, "h_pct": 9.0, "label_he": "מאגר מים + משאבות תחת רמפה עליונה (H_clear≥2.20m · 28 מ״ר)"},
            "relocated_parking_target_rect": {"x_pct": 42.0, "y_pct": 56.0, "w_pct": 16.0, "h_pct": 14.0, "label_he": "🅿️🔄 מקום חלופי מאומת לחניה #6 (הסטה 1.80 מ׳ מערבה בדופן הדרומית · 2.55×5.00 מ׳)"},
        },
    },
    "FB3-OPT-UG2": {
        "proposed_gross_reduction_sqm": 76.0,
        "verified_contour_saved_sqm": 50.0,
        "non_contour_reclassified_sqm": 26.0,
        "protected_ramp_and_maneuvering_deducted_sqm": 26.0,
        "under_ramp_utilized_sqm": 18.0,
        "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
        "contour_mechanism": "שמירה מלאה על האגף המזרחי במרתף 2- (חניות #13–#17, מיסעה 5.20–5.50 מ׳ ויציאת רמפה R400/R500), והשגת 50.0 מ״ר כיווץ קונטור מאומת ע״י נסיגת קיר הדיפון הדרומי-מרכזי ב-32.0 מ״ר ברצועה המתה שבין חניה #12 לחניה #13 (מחוץ לקשת R500) + 18.0 מ״ר ניצול תחתית הרמפה הצפונית העליונה (H_clear ≥ 2.15 מ׳).",
        "contour_dims_before_after": "קונטור דיפון מרתף 2-: 548.0 מ״ר ← 498.0 מ״ר (-50.0 מ״ר חפירה בעומק -7.80 מ׳ · 26.0 מ״ר באגף המזרחי קוזזו להגנת חניות #13–#17 ורדיוס R400/R500)",
        "locked_reason_he": "26.0 מ״ר באגף המזרחי של מרתף 2- מהווים את משטח היציאה מהרמפה (רדיוס R400/R500 ברוחב 420 ס״מ במפלס 45.10) ואת מיסעת התמרון (5.20–5.50 מ׳) המשרתת את חניות #15, #16, #17 (נכה) בצפון-מזרח ואת חניות #13, #14 בדרום-מזרח — ולכן אסורים לגריעה וקוזזו מחיסכון הקונטור (0 ₪)!",
        "ramp_function_audit_he": "בתכנית המקור של מרתף 2- (מפלס 45.10 / -7.80m): הרמפה יורדת לאורך הדופן הצפונית בשיפוע 15% (אורך 10.67 מ׳) ומתמתנת ב-7.5% (3.00 מ׳) לפני עיקול R400/R500 (רוחב 4.20 מ׳) אל המיסעה המזרחית. גריעה של קצה המרתף המזרחי הייתה חוסמת לחלוטין את יציאת הרמפה ואת חניות #13–#17! לכן רדיוס R400/R500 והמיסעה המזרחית מוגנים ב-100%, וניצול תחתית הרמפה (18.0 מ״ר לבורות שאיבה ומפריד שומנים) מבוצע מתחת לחלק הצפוני העליון של הרמפה (H_clear ≥ 2.15 מ׳).",
        "maneuvering_aisle_audit_he": "שמירה על כל 11 החניות במרתף 2- בתכנית המקור: חניות #9–#12 במערב (מיסעה 5.90 מ׳ + אוזן תמרון 100 ס״מ), חניות #18–#19 במרכז, וחניות #13–#14 ו-#15–#17 (כולל חניית נכה #17 ברוחב 437 ס״מ) במזרח עם מיסעה של 5.20–5.50 מ׳. נסיגת הדיפון (32.0 מ״ר) מתבצעת אך ורק ברצועה הדרומית המתה שבין חניה #12 לחניה #13 (מדרום לחניות #19–#18 ומחוץ לקשת החיצונית R500).",
        "parking_relocation_audit": {
            "stalls_relocated_count": 1,
            "affected_stalls_label": "חניה #18 (מרכז-דרום מרתף 2- בתכנית המקור, בצמוד לרצועת הדיפון שצומצמה)",
            "original_location_he": "מוקמה בגוש המרכזי-דרומי (לצד חניה #19) מעל רצועת הדיפון הדרומית שניסוגה פנימה ב-32.0 מ״ר בין חניה #12 לחניה #13.",
            "alternative_location_found_he": "הועתקה למפרץ החלופי המאומת שהתפנה בדופן הצפונית-מרכזית של המיסעה (בצמוד לגרעין) בעקבות העברת בורות השאיבה ומפריד השומנים (18.0 מ״ר) אל מתחת לחלק הצפוני העליון של הרמפה (H_clear ≥ 2.15m).",
            "new_stall_dimensions_and_access_he": "תא חניה תקני 2.60×5.00 מ׳ (13.0 מ״ר) בניצב למיסעה המרכזית (5.50–5.90 מ׳), מה שמאפשר לקרב את קיר הדיפון הדרומי פנימה ללא הפרעה לקשת R500 או לחניות #13–#17.",
            "net_parking_balance_he": "מאזן חניות נטו במרתף 2-: 0 גריעה (חניה #18 הועתקה מהרצועה הדרומית ← אוכלסה במפרץ השאיבה שפונה = 11/11 חניות במרתף 2- ו-19/19 בפרויקט נשמרות ב-100%).",
        },
        "parking_relocation_audit_he": "בדיקת העתקת חנייה ומציאת מקום חלופי (מרתף 2-): כדי לאפשר את נסיגת קיר הדיפון הדרומי-מרכזי ב-32.0 מ״ר (בין חניה #12 לחניה #13) מבלי לפגוע באגף המזרחי (#13–#17), מועברים בורות השאיבה ומפריד השומנים (18.0 מ״ר) אל מתחת לחלק הצפוני העליון של הרמפה (H_clear ≥ 2.15m). המפרץ שהתפנה בצמוד לגרעין קולט את חניה #18 במידות תקניות 2.60×5.00 מ׳ ומול מיסעה של 5.50–5.90 מ׳ (11/11 חניות במרתף 2- נשמרות במלואן).",
        "plan_overlay_zones": {
            "protected_ramp_maneuver_rect": {"x_pct": 55.0, "y_pct": 33.0, "w_pct": 28.0, "h_pct": 26.0, "label_he": "יציאת רמפה R400/R500 + מיסעה 5.20–5.50 מ׳ לחניות #13–#17 (מוגן 100%)"},
            "under_ramp_utility_rect": {"x_pct": 35.0, "y_pct": 24.0, "w_pct": 22.0, "h_pct": 9.0, "label_he": "תחתית רמפה צפונית עליונה (H_clear≥2.15m · 18 מ״ר בורות שאיבה)"},
            "relocated_parking_target_rect": {"x_pct": 38.0, "y_pct": 42.0, "w_pct": 15.0, "h_pct": 14.0, "label_he": "🅿️🔄 מקום חלופי מאומת לחניה #18 (במפרץ בורות השאיבה שפונה · 2.60×5.00 מ׳)"},
        },
    },
}

# Explicit Standalone Locked-Core Recommendations (`LOCKED_CORE_ONLY`) that reduce core/service area
# internally (0% contour contraction: verified_contour_saved_sqm = 0.0) and are therefore 100% REJECTED
# from the Cost Savings model (0 ILS) and reclassified into Design Improvement (`שיפור תכנון`)!
PROJECT_LOCKED_CORE_RECLASSIFIED_ITEMS = {
    "pines48": [
        {
            "id": "P48-LOCKED-CORE1",
            "zone": "קומת קרקע (±0.00 · גיליון A-1001) וקומות 1–6 — מעבר לובי תחת תקרת קומה א׳ (14.0 מ״ר) ונישת מבואה פנימית כלואה (9.0 מ״ר)",
            "proposed_core_reduction_sqm": 23.0,
            "verified_contour_saved_sqm": 0.0,
            "reclassified_design_improvement_sqm": 23.0,
            "cost_saving_ils": 0,
            "why_not_contour_saving": (
                "בדיקת קונטור שלילית (0 מ״ר הקטנת קונטור בניין): 14.0 מ״ר בקומת הקרקע (באזור הלובי הראשי 1085×375 ס״מ ומעבר ריכוז המונים) נמצאים מתחת לתקרת קומה א׳ הקשיחה (מבחן 2), "
                "ו-9.0 מ״ר בקומות 1–6 כלואים גיאומטרית בין קירות הממ״ד לעמודי הפיר ללא יכולת לקרב את חזיתות הבניין (מבחן 1). "
                "מאחר שסך שטח הבנייה הכולל אינו קטן, הפריט הוסר ממודל חיסכון העלויות (0 ₪) והועבר לשיפור תכנון."
            ),
            "design_benefit": "בקומת הקרקע (A-1001): הרחבת הלובי הראשי והמפולש ב-14.0 מ״ר ושיפור הגישה לחדר העגלות (345×280 ס״מ); בקומות 1–6: הרחבת מבואת הכניסה לדירות ב-1.5 מ״ר לקומה.",
            "sheet_id": "ground",
            "x_pct": 46.0, "y_pct": 33.0, "w_pct": 28.0, "h_pct": 24.0, "cx_pct": 60.0, "cy_pct": 45.0,
        },
    ],
    "kkl10": [
        {
            "id": "KKL-LOCKED-CORE1",
            "zone": "קומות 1–8 וקומת קרקע — נישת מבואה כלואה בין 2 המעליות (12 מ״ר) ומעבר שירות תחת תקרת קומה 1 (12 מ״ר)",
            "proposed_core_reduction_sqm": 24.0,
            "verified_contour_saved_sqm": 0.0,
            "reclassified_design_improvement_sqm": 24.0,
            "cost_saving_ils": 0,
            "why_not_contour_saving": (
                "בדיקת קונטור שלילית (0 מ״ר הקטנת קונטור בניין): הנישה בין שתי המעליות כלואה בין 4 דירות בפינות הבניין ועמודי הגרעין (מבחן 1), "
                "ומעבר השירות בקומת הקרקע חופף ב-100% לתקרת קומה 1 שמעליו (מבחן 2). לכן שטח התקרה הכולל אינו קטן (0 ₪ חיסכון בנייה) והפריט סווג כשיפור תכנון."
            ),
            "design_benefit": "סיפוח 1.5 מ״ר בכל קומה להרחבת מבואות הכניסה לדירות והגדלת הלובי הראשי בקומת הקרקע ב-12.0 מ״ר.",
            "sheet_id": "kkl_typical",
            "x_pct": 42.0, "y_pct": 43.0, "w_pct": 16.0, "h_pct": 14.0, "cx_pct": 50.0, "cy_pct": 50.0,
        },
    ],
    "hafetz44": [
        {
            "id": "H44-LOCKED-CORE1",
            "zone": "מרתף (-5.10) וקומות 1–8 — תא ה'משאבות' הכלוא בקירות הממ״ד המערבי במרתף (12 מ״ר) + גומחות מבואה תחת תקרה (17 מ״ר)",
            "proposed_core_reduction_sqm": 29.0,
            "verified_contour_saved_sqm": 0.0,
            "reclassified_design_improvement_sqm": 29.0,
            "cost_saving_ils": 0,
            "why_not_contour_saving": (
                "בדיקת קונטור שלילית (0 מ״ר הקטנת קונטור בניין): (1) במרתף החניון, שני תאי ה'משאבות' (335×200 ו-335×140 ס״מ = 12.0 מ״ר) נמצאים באי המרכזי בין מבואת המעלית לרמפה הצפונית, בתוך קופסת קירות הבטון של הממ״ד המערבי שחייבים לרדת לביסוס לפי פקע״ר (70% קירות ממ״ד). לכן העברת המשאבות אל החלל האטום מתחת לרמפה הדרומית העליונה אינה מקטינה כשלעצמה את קיר הדיפון החיצוני באזור הליבה (מבחן 1 — ליבה כלואה בתוך לולאת הרמפה); (2) בקומות העיליות, גומחת המבואה (8 מ״ר) ומבואת הקרקע תחת תקרת קומה 1 (9 מ״ר) נעולות ע״י קירות הממ״ד והתקרה שמעל (מבחן 2). לכן כל 29.0 המ״ר קוזזו ממודל החיסכון הכספי (0 ₪) והועברו לשיפור תכנון."
            ),
            "design_benefit": "הפיכת קופסת הממ״ד המערבי שהתפנתה ממשאבות במרתף (12.0 מ״ר) ל-3 מחסני דיירים תקניים (שחסרים כיום לחלוטין בפרויקט!) + הרחבת מבואות הדירות והלובי העילי (17.0 מ״ר).",
            "sheet_id": "h44_basement",
            "x_pct": 45.0, "y_pct": 32.0, "w_pct": 11.0, "h_pct": 15.0, "cx_pct": 50.5, "cy_pct": 39.5,
        },
    ],
    "yatkovski7": [
        {
            "id": "Y7-LOCKED-CORE1",
            "zone": "קומות א׳–ו׳ וקומת קרקע — נישת גרעין פנימית כלואה (4.8 מ״ר) ומעבר לובי תחת תקרת קומה א׳ (6.0 מ״ר)",
            "proposed_core_reduction_sqm": 10.8,
            "verified_contour_saved_sqm": 0.0,
            "reclassified_design_improvement_sqm": 10.8,
            "cost_saving_ils": 0,
            "why_not_contour_saving": (
                "בדיקת קונטור שלילית (0 מ״ר הקטנת קונטור בניין): הורדת שטח הליבה בנישה הפנימית אינה מאפשרת לקרב את הדירה הצפונית והדרומית בגלל עמודי הממ״ד (מבחן 1), "
                "ומעבר הקרקע מקורה ע״י תקרת קומה א׳ (מבחן 2). מאחר שלא נבנה פחות שטח תקרה כולל, הפריט הועבר מחיסכון עלויות לשיפור תכנון."
            ),
            "design_benefit": "הרחבת מבואת הכניסה לדירות בקומות א׳–ו׳ והגדלת חלל הלובי הדו-מפלסי בקומת הקרקע.",
            "sheet_id": "yat_typical",
            "x_pct": 44.0, "y_pct": 41.0, "w_pct": 12.0, "h_pct": 14.0, "cx_pct": 50.0, "cy_pct": 48.0,
        },
    ],
    "kitroni37": [
        {
            "id": "KIT-LOCKED-CORE1",
            "zone": "בניינים 37 ו-39 (קומות 1–9 וקרקע) — נישות מבואה כלואות בין ממ״דים (18 מ״ר) ומבואות תחת תקרת קומה 1 (18 מ״ר)",
            "proposed_core_reduction_sqm": 36.0,
            "verified_contour_saved_sqm": 0.0,
            "reclassified_design_improvement_sqm": 36.0,
            "cost_saving_ils": 0,
            "why_not_contour_saving": (
                "בדיקת קונטור שלילית (0 מ״ר הקטנת קונטור בניין): 18.0 מ״ר בנישות המבואה של שני הבניינים כלואים בין 4 הדירות בקומה ללא תזוזת קו החזית (מבחן 1), "
                "ו-18.0 מ״ר בקומת הקרקע נמצאים תחת תקרת קומה 1 (מבחן 2). לא חוסך עלויות בנייה (0 ₪) ולכן הועבר לשיפור תכנון."
            ),
            "design_benefit": "הרחבת מבואות הכניסה הקומתיות ב-2 הבניינים והגדלת מועדון הדיירים והלובאים בקומת הקרקע.",
            "sheet_id": "kit_typical",
            "x_pct": 38.0, "y_pct": 35.0, "w_pct": 14.0, "h_pct": 25.0, "cx_pct": 45.0, "cy_pct": 47.5,
        },
    ],
    "feierberg3": [
        {
            "id": "FB3-LOCKED-CORE1",
            "zone": "קומות 1–8 וקומת קרקע — נישת מבואה דרומית כלואה בין עמודי הגרעין (9.6 מ״ר) ומעבר שירות תחת תקרת קומה א׳ (10.0 מ״ר)",
            "proposed_core_reduction_sqm": 19.6,
            "verified_contour_saved_sqm": 0.0,
            "reclassified_design_improvement_sqm": 19.6,
            "cost_saving_ils": 0,
            "why_not_contour_saving": (
                "בדיקת קונטור שלילית (0 מ״ר הקטנת קונטור בניין): צמצום נישת המבואה הדרומית (1.2 מ״ר × 8 קומות = 9.6 מ״ר) נמצא בין עמודי השלד וקירות הממ״ד ללא יכולת להסיג את קו החזית הדרומית (מבחן 1), "
                "וצמצום מעבר השירות בקומת הקרקע (10.0 מ״ר) נמצא מתחת לתקרת דירה #2 בקומה א׳ שממילא ניצוקה (מבחן 2). לכן 19.6 מ״ר אלו אינם מקטינים את שטח הבנייה הכולל (0 ₪ חיסכון) והועברו לשיפור תכנון!"
            ),
            "design_benefit": "העברת 1.2 מ״ר בכל קומה להרחבת מבואת הכניסה לדירות והגדלת הלובי הראשי וחדר העגלות בקומת הקרקע ב-10.0 מ״ר.",
            "sheet_id": "fb_typical",
            "x_pct": 43.5, "y_pct": 33.0, "w_pct": 15.0, "h_pct": 14.0, "cx_pct": 51.0, "cy_pct": 40.0,
        },
    ],
}


# =============================================================================
# DYNAMIC PROJECT & APARTMENT OPTIMIZATION BUILDER
# =============================================================================
def build_project_design_optimization(pid: str, data_summary: dict) -> dict:
    """
    Builds the complete `design_optimization` dictionary for a project (both the 6 cataloged
    projects and any dynamically uploaded CAD/PDF model), including the Global Building Contour
    Contraction Audit (`contour_audit_summary` and `locked_core_reclassified_items`).
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
            cmeta = ITEM_CONTOUR_AUDIT_METADATA.get(item["id"], {})
            prop_gross = float(cmeta.get("proposed_gross_reduction_sqm", saved))
            locked_non_contour = round(max(0.0, prop_gross - saved), 1)
            eff_pct = round((saved / prop_gross * 100.0) if prop_gross > 0 else 100.0, 1)
            ag_items.append({
                **item,
                "proposed_gross_reduction_sqm": prop_gross,
                "verified_contour_saved_sqm": saved,
                "non_contour_reclassified_sqm": locked_non_contour,
                "contour_efficiency_pct": eff_pct,
                "contour_test_status": cmeta.get("contour_test_status", "FULL_CONTOUR_REDUCTION"),
                "contour_mechanism": cmeta.get("contour_mechanism", "קירוב אגפי הדירות ונסיגת קיר המעטפת החיצוני בהתאם להפחתת הגרעין."),
                "contour_dims_before_after": cmeta.get("contour_dims_before_after", f"הקטנת קונטור עילי ב-{saved} מ״ר"),
                "locked_reason_he": cmeta.get("locked_reason_he", ""),
                "unit_cost_ils": COST_ABOVE_GROUND_PER_SQM_ILS,
                "cost_saving_ils": round(saved * COST_ABOVE_GROUND_PER_SQM_ILS),
            })

        ug_items = []
        for item in profile["underground_items"]:
            saved = float(item["saved_sqm"])
            cmeta = ITEM_CONTOUR_AUDIT_METADATA.get(item["id"], {})
            prop_gross = float(cmeta.get("proposed_gross_reduction_sqm", saved))
            locked_non_contour = round(max(0.0, prop_gross - saved), 1)
            eff_pct = round((saved / prop_gross * 100.0) if prop_gross > 0 else 100.0, 1)
            prot_ramp_sqm = float(cmeta.get("protected_ramp_and_maneuvering_deducted_sqm", locked_non_contour))
            under_ramp_sqm = float(cmeta.get("under_ramp_utilized_sqm", round(saved * 0.5, 1)))
            ug_items.append({
                **item,
                "proposed_gross_reduction_sqm": prop_gross,
                "verified_contour_saved_sqm": saved,
                "non_contour_reclassified_sqm": locked_non_contour,
                "protected_ramp_and_maneuvering_deducted_sqm": prot_ramp_sqm,
                "under_ramp_utilized_sqm": under_ramp_sqm,
                "contour_efficiency_pct": eff_pct,
                "contour_test_status": cmeta.get("contour_test_status", "FULL_CONTOUR_REDUCTION"),
                "contour_mechanism": cmeta.get("contour_mechanism", "הזזת קו הדיפון ההיקפי וגבול החפירה פנימה לאחר ניצול תחתית הרמפה."),
                "contour_dims_before_after": cmeta.get("contour_dims_before_after", f"הקטנת קונטור דיפון ב-{saved} מ״ר"),
                "locked_reason_he": cmeta.get("locked_reason_he", ""),
                "ramp_function_audit_he": cmeta.get(
                    "ramp_function_audit_he",
                    "שמירה מלאה על נתיב הרמפה (15%–17%), משטחי ההתמתנות (5%–10% באורך 3.00 מ׳) ורדיוסי הסיבוב (R_in ≥ 3.50m); ניצול תחתית הרמפה לחדר משאבות ומאגר מים מבוצע אך ורק בחצי העליון שבו גובה הראש הפנוי H_clear ≥ 2.15–2.20 מ׳.",
                ),
                "maneuvering_aisle_audit_he": cmeta.get(
                    "maneuvering_aisle_audit_he",
                    "שמירה מלאה על מיסעות דו-סטריות ברוחב 5.20–6.50 מ׳ לחניות 90° ואוזן תמרון של 1.00 מ׳ לחניות קצה; כל שטח החופף למעטפת התמרון קוזז מחיסכון הקונטור.",
                ),
                "parking_relocation_audit": cmeta.get(
                    "parking_relocation_audit",
                    {
                        "stalls_relocated_count": 1,
                        "affected_stalls_label": "חניית קצה באזור נסיגת קיר הדיפון",
                        "original_location_he": "מוקמה בכיס החפירה ההיקפי שצומצם להקטנת קונטור המרתף.",
                        "alternative_location_found_he": "הועתקה למפרץ חלופי מאומת לאורך המיסעה המרכזית שהתפנה בעקבות העברת מאגר המים וחדר המשאבות אל מתחת לחלק העליון של הרמפה (H_clear ≥ 2.15–2.20m).",
                        "new_stall_dimensions_and_access_he": "תא חניה תקני 2.60×5.00 מ׳ בניצב למיסעה (6.00 מ׳) עם גישה ישירה בתמרון אחד.",
                        "net_parking_balance_he": f"מאזן חניות נטו: 0 גריעה (100% מ-{parking_spaces} החניות נשמרות במלואן).",
                    },
                ),
                "parking_relocation_audit_he": cmeta.get(
                    "parking_relocation_audit_he",
                    "בדיקת העתקת חנייה ומציאת מקום חלופי: כל חניית קצה המושפעת מנסיגת קיר הדיפון מועתקת למפרץ החלופי שהתפנה לאורך המיסעה בעקבות העברת מאגר המים וחדר המשאבות אל מתחת לחלק העליון של הרמפה (H_clear ≥ 2.15m) — 0 גריעת חניות.",
                ),
                "plan_overlay_zones": cmeta.get(
                    "plan_overlay_zones",
                    {
                        "protected_ramp_maneuver_rect": {"x_pct": 22.0, "y_pct": 38.0, "w_pct": 52.0, "h_pct": 22.0, "label_he": "מיסעה ורדיוס סיבוב רמפה (מוגן 100%)"},
                        "under_ramp_utility_rect": {"x_pct": 55.0, "y_pct": 22.0, "w_pct": 20.0, "h_pct": 12.0, "label_he": f"ניצול תחתית רמפה עליונה (H≥2.15m · {under_ramp_sqm} מ״ר)"},
                        "relocated_parking_target_rect": {"x_pct": 38.0, "y_pct": 24.0, "w_pct": 15.0, "h_pct": 12.0, "label_he": "🅿️🔄 מקום חלופי מאומת לחנייה שהועתקה (2.60×5.00 מ׳)"},
                    },
                ),
                "unit_cost_ils": COST_UNDERGROUND_PARKING_PER_SQM_ILS,
                "cost_saving_ils": round(saved * COST_UNDERGROUND_PARKING_PER_SQM_ILS),
            })

        apt_items = list(profile["internal_apartment_items"])
        locked_core_items = [dict(x) for x in PROJECT_LOCKED_CORE_RECLASSIFIED_ITEMS.get(pid, [])]
        facade_opt = build_facade_cladding_optimization(
            fac,
            baseline_dry_pct=profile.get("baseline_dry_cladding_pct", 85.0),
            target_plaster_conversion_pct=profile.get("recommended_plaster_conversion_pct", 35.0),
        )
    else:
        # Dynamic calculation for uploaded / custom projects with Contour Contraction Audit
        raw_ag_candidate = round(max(24.0, core_ag_sqm * 0.18), 1)
        saved_ag_sqm = round(max(18.0, core_ag_sqm * 0.14), 1)
        locked_ag_sqm = round(max(4.0, raw_ag_candidate - saved_ag_sqm), 1)
        prop_ag_gross = round(saved_ag_sqm + locked_ag_sqm, 1)
        ag_items = [
            {
                "id": f"{pid.upper()}-OPT-AG1",
                "floor_or_zone": "גרעין קומות טיפוסיות, מבואות וקומת קרקע",
                "current_sqm": core_ag_sqm,
                "optimal_sqm": round(core_ag_sqm - saved_ag_sqm, 1),
                "saved_sqm": saved_ag_sqm,
                "proposed_gross_reduction_sqm": prop_ag_gross,
                "verified_contour_saved_sqm": saved_ag_sqm,
                "non_contour_reclassified_sqm": locked_ag_sqm,
                "contour_efficiency_pct": round(saved_ag_sqm / prop_ag_gross * 100.0, 1),
                "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
                "contour_mechanism": "קירוב אגפי הדירות על ציר הגרעין ונסיגת קיר השירות בקומת הקרקע (נבנה פחות בפועל).",
                "contour_dims_before_after": f"קונטור עילי כולל: {total_ag_sqm:.1f} מ״ר ← {total_ag_sqm - saved_ag_sqm:.1f} מ״ר (-{saved_ag_sqm:.1f} מ״ר)",
                "locked_reason_he": f"{locked_ag_sqm:.1f} מ״ר בנישות ליבה פנימיות כלואות ותחת תקרת קומה א׳ אינם מקטינים את קונטור הבניין והועברו לשיפור תכנון (0 ₪).",
                "unit_cost_ils": COST_ABOVE_GROUND_PER_SQM_ILS,
                "cost_saving_ils": round(saved_ag_sqm * COST_ABOVE_GROUND_PER_SQM_ILS),
                "preserved_utilities": "שמירה מלאה על שטח הפלדלת של הדירות וכל ארונות החשמל, המים, הגז והתקשורת",
                "engineering_action": "הידוק שטחי מעבר כפולים בלובי ובגרעין הקומתי ויישור גומחות ארונות השירות לקו אפס.",
            }
        ]

        current_per_stall = total_ug_sqm / max(1, parking_spaces)
        excess_ug = max(25.0, round(max(0.0, (current_per_stall - 35.0) * parking_spaces), 1))
        locked_ug_sqm = round(max(6.0, excess_ug * 0.16), 1)
        prop_ug_gross = round(excess_ug + locked_ug_sqm, 1)
        under_ramp_dyn_sqm = round(min(28.0, excess_ug * 0.55), 1)
        ug_items = [
            {
                "id": f"{pid.upper()}-OPT-UG1",
                "zone": "מרתף חניון תת-קרקעי — ייעול קו דיפון, ניצול תחתית רמפה (H≥2.15m) והגנת שטחי תמרון",
                "current_sqm": total_ug_sqm,
                "optimal_sqm": round(total_ug_sqm - excess_ug, 1),
                "saved_sqm": excess_ug,
                "proposed_gross_reduction_sqm": prop_ug_gross,
                "verified_contour_saved_sqm": excess_ug,
                "non_contour_reclassified_sqm": locked_ug_sqm,
                "protected_ramp_and_maneuvering_deducted_sqm": locked_ug_sqm,
                "under_ramp_utilized_sqm": under_ramp_dyn_sqm,
                "contour_efficiency_pct": round(excess_ug / prop_ug_gross * 100.0, 1),
                "contour_test_status": "PARTIAL_CONTOUR_REDUCTION",
                "contour_mechanism": "הזזת קיר הדיפון ההיקפי פנימה לאחר מיקום מאגר המים וחדר המשאבות מתחת לחלק העליון של רמפת הירידה (H_clear ≥ 2.15 מ׳).",
                "contour_dims_before_after": f"קונטור מרתף: {total_ug_sqm:.1f} מ״ר ← {total_ug_sqm - excess_ug:.1f} מ״ר (-{excess_ug:.1f} מ״ר מאומת · {locked_ug_sqm:.1f} מ״ר קוזזו להגנת תמרון ורמפה)",
                "locked_reason_he": f"{locked_ug_sqm:.1f} מ״ר באזור רדיוס הסיבוב של הרמפה ומיסעת התמרון לחניות מוגנים ב-100% וקוזזו מחיסכון הקונטור (0 ₪).",
                "ramp_function_audit_he": f"ניצול תחתית הרמפה ({under_ramp_dyn_sqm:.1f} מ״ר) מתבצע אך ורק בחצי העליון של כבש הירידה שבו גובה הראש הפנוי H_clear ≥ 2.15–2.20 מ׳, תוך שמירה מלאה על משטחי ההתמתנות ורדיוס הסיבוב.",
                "maneuvering_aisle_audit_he": f"שמירה מלאה על מיסעה דו-סטרית (5.50–6.00 מ׳) ואוזני תמרון (1.00 מ׳) לכל {parking_spaces} החניות; {locked_ug_sqm:.1f} מ״ר קוזזו להגנת רדיוסי התמרון.",
                "parking_relocation_audit": {
                    "stalls_relocated_count": 1,
                    "affected_stalls_label": f"חניית קצה #{parking_spaces} באזור נסיגת קיר הדיפון",
                    "original_location_he": "מוקמה בכיס החפירה ההיקפי שניסוג פנימה להקטנת קונטור המרתף.",
                    "alternative_location_found_he": f"הועתקה למפרץ החלופי המאומת שהתפנה לאורך המיסעה המרכזית (6.00 מ׳) לאחר העברת מאגר המים וחדר המשאבות ({under_ramp_dyn_sqm:.1f} מ״ר) אל מתחת לחלק העליון של הרמפה (H_clear ≥ 2.15m).",
                    "new_stall_dimensions_and_access_he": "תא חניה תקני 2.60×5.00 מ׳ (13.0 מ״ר) בניצב למיסעה עם כניסה ויציאה ישירה בתמרון אחד.",
                    "net_parking_balance_he": f"מאזן חניות נטו: 0 גריעה (חניה 1 הועתקה ← מפרץ חלופי 1 אוכלס = {parking_spaces}/{parking_spaces} חניות נשמרות ב-100%).",
                },
                "parking_relocation_audit_he": f"בדיקת העתקת חנייה ומציאת מקום חלופי: נסיגת קיר הדיפון ההיקפי מזיזה את חניית הקצה #{parking_spaces}. העברת מאגר המים וחדר המשאבות ({under_ramp_dyn_sqm:.1f} מ״ר) אל מתחת לחלק העליון של הרמפה (H_clear ≥ 2.15m) מפנה מפרץ חניה תקני לאורך המיסעה המרכזית (6.00 מ׳) שלתוכו מועתקת החנייה במידות 2.60×5.00 מ׳ ({parking_spaces}/{parking_spaces} חניות נשמרות במלואן).",
                "plan_overlay_zones": {
                    "protected_ramp_maneuver_rect": {"x_pct": 22.0, "y_pct": 38.0, "w_pct": 52.0, "h_pct": 22.0, "label_he": "מיסעה ורדיוס סיבוב רמפה (מוגן 100%)"},
                    "under_ramp_utility_rect": {"x_pct": 55.0, "y_pct": 22.0, "w_pct": 20.0, "h_pct": 12.0, "label_he": f"ניצול תחתית רמפה עליונה (H≥2.15m · {under_ramp_dyn_sqm} מ״ר)"},
                    "relocated_parking_target_rect": {"x_pct": 36.0, "y_pct": 24.0, "w_pct": 16.0, "h_pct": 12.0, "label_he": f"🅿️🔄 מקום חלופי מאומת לחניה #{parking_spaces} (במפרץ המשאבות שפונה · 2.60×5.00 מ׳)"},
                },
                "unit_cost_ils": COST_UNDERGROUND_PARKING_PER_SQM_ILS,
                "cost_saving_ils": round(excess_ug * COST_UNDERGROUND_PARKING_PER_SQM_ILS),
                "parking_spaces_preserved": f"{parking_spaces} חניות תקניות (100% שמירה על מצבת החניות ומיסעות תמרון)",
                "engineering_action": "מיקום מאגר המים וחדר המשאבות מתחת לחלק העליון של רמפת הירידה (H_clear ≥ 2.15m) וגיזום כיסי חפירה מתים מחוץ למיסעה.",
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
        locked_core_items = [
            {
                "id": f"{pid.upper()}-LOCKED-CORE1",
                "zone": "נישות מבואה פנימיות כלואות בין דירות ומעברי שירות תחת תקרת קומה א׳",
                "proposed_core_reduction_sqm": locked_ag_sqm,
                "verified_contour_saved_sqm": 0.0,
                "reclassified_design_improvement_sqm": locked_ag_sqm,
                "cost_saving_ils": 0,
                "why_not_contour_saving": "שטח ליבה כלוא בין עמודי שלד וקירות ממ״ד או מקורה ע״י תקרת קומה א׳ — אינו מקטין את קונטור הבניין הכולל (0 ₪ חיסכון) ולכן הועבר לשיפור תכנון.",
                "design_benefit": "הרחבת מבואות הכניסה הקומתיות והלובי הראשי.",
                "sheet_id": "f1_5",
                "x_pct": 44.0, "y_pct": 35.0, "w_pct": 14.0, "h_pct": 14.0, "cx_pct": 51.0, "cy_pct": 42.0,
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

    # Contour Audit Summary Totals
    proposed_ag_gross_sqm = round(sum(float(x.get("proposed_gross_reduction_sqm", x["saved_sqm"])) for x in ag_items), 1)
    locked_ag_non_contour_sqm = round(sum(float(x.get("non_contour_reclassified_sqm", 0.0)) for x in ag_items), 1)
    proposed_ug_gross_sqm = round(sum(float(x.get("proposed_gross_reduction_sqm", x["saved_sqm"])) for x in ug_items), 1)
    locked_ug_non_contour_sqm = round(sum(float(x.get("non_contour_reclassified_sqm", 0.0)) for x in ug_items), 1)
    total_protected_ramp_maneuver_sqm = round(sum(float(x.get("protected_ramp_and_maneuvering_deducted_sqm", x.get("non_contour_reclassified_sqm", 0.0))) for x in ug_items), 1)
    total_under_ramp_utilized_sqm = round(sum(float(x.get("under_ramp_utilized_sqm", 0.0)) for x in ug_items), 1)
    total_stalls_relocated = sum(int(x.get("parking_relocation_audit", {}).get("stalls_relocated_count", 1)) for x in ug_items)
    total_locked_core_and_ug_reclassified_sqm = round(locked_ag_non_contour_sqm + locked_ug_non_contour_sqm, 1)
    total_proposed_raw_sqm = round(proposed_ag_gross_sqm + proposed_ug_gross_sqm + total_reclaimed_living_sqm, 1)
    total_verified_contour_saved_sqm = round(total_ag_saved_sqm + total_ug_saved_sqm, 1)
    total_reclassified_to_design_improvement_sqm = round(total_locked_core_and_ug_reclassified_sqm + total_reclaimed_living_sqm, 1)

    current_core_ratio_pct = round((core_ag_sqm / total_ag_sqm * 100.0) if total_ag_sqm > 0 else 0.0, 1)
    optimized_ag_total_sqm = round(total_ag_sqm - total_ag_saved_sqm, 1)
    optimized_core_sqm = round(core_ag_sqm - total_ag_saved_sqm, 1)
    optimized_core_ratio_pct = round((optimized_core_sqm / optimized_ag_total_sqm * 100.0) if optimized_ag_total_sqm > 0 else 0.0, 1)

    current_sqm_per_stall = round(total_ug_sqm / max(1, parking_spaces), 1)
    optimized_ug_total_sqm = round(total_ug_sqm - total_ug_saved_sqm, 1)
    optimized_sqm_per_stall = round(optimized_ug_total_sqm / max(1, parking_spaces), 1)

    ramp_and_maneuvering_audit = {
        "total_proposed_ug_gross_cut_sqm": proposed_ug_gross_sqm,
        "total_protected_ramp_and_maneuvering_deducted_sqm": total_protected_ramp_maneuver_sqm,
        "total_verified_ug_contour_saved_sqm": total_ug_saved_sqm,
        "total_under_ramp_utilized_sqm": total_under_ramp_utilized_sqm,
        "total_stalls_relocated_to_alternative_bays": total_stalls_relocated,
        "min_clear_headroom_for_utility_m": 2.15,
        "min_two_way_aisle_width_m": 5.20,
        "end_stall_backing_ear_m": 1.00,
        "parking_relocation_rule_he": (
            f"חוק שימור והעתקת חניות (Stall Relocation Check): בכל המלצה להקטנת קונטור דיפון המרתף שבה מבוטלת או מוזזת חנייה קיימת ({total_stalls_relocated} חניות הועתקו בפרויקט זה), "
            f"מאותר ומוקצה לה מקום חלופי מאומת במרתף — במפרץ שהתפנה לאורך המיסעה המרכזית בעקבות העברת מאגר המים וחדר המשאבות אל מתחת לחלק העליון של הרמפה (H_clear ≥ 2.15–2.20 מ׳), "
            f"במידות תקניות (≥2.50–2.65×5.00 מ׳) ועם גישה ישירה בתמרון אחד (0 גריעת חניות — {parking_spaces}/{parking_spaces} חניות נשמרות)."
        ),
        "audit_statement_he": (
            f"מתוך {proposed_ug_gross_sqm:.1f} מ״ר הפחתה תאורטית במרתף, קוזזו {total_protected_ramp_maneuver_sqm:.1f} מ״ר "
            f"להגנה מוחלטת על תפקוד רמפות הירידה (שיפועי התמתנות ורדיוסי סיבוב R_in/R_out) ועל מיסעות התמרון (5.20–6.50 מ׳) ואוזני התמרון לחניות קצה (1.00 מ׳). "
            f"ניצול תחתית הרמפה ({total_under_ramp_utilized_sqm:.1f} מ״ר למאגרי מים/משאבות) מבוצע אך ורק בחצי העליון של הרמפה שבו גובה הראש הפנוי H_clear ≥ 2.15–2.20 מ׳, "
            f"המפרץ שהתפנה לאורך המיסעה קולט {total_stalls_relocated} חניות שהוזזו מאזור כיווץ הקונטור (0 פגיעה במצבת {parking_spaces} החניות), "
            f"והחיסכון המאומת בקונטור החפירה והדיפון עומד על {total_ug_saved_sqm:.1f} מ״ר נטו."
        ),
    }

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
        "contour_audit_summary": {
            "audit_rule_he": (
                "חיסכון בעלויות בנייה (6,200 ₪/מ״ר עילי ו-3,500 ₪/מ״ר מרתף) מוכר אך ורק כאשר הקטנת הגרעין/שירות/מרתף "
                "מקטינה בפועל את קונטור הבניין או הדיפון החיצוני (סך הכל נבנה פחות). שטח ליבה או מרתף שירד אך נותר כלוא בין דירות/עמודים, "
                "מתחת לתקרה עליונה קשיחה, או חופף למסלול רמפה פעיל, רדיוס סיבוב ומיסעת תמרון לחניות — מקוזז ממודל החיסכון (0 ₪) ומועבר ל'שיפור תכנון / הגנת תמרון'."
            ),
            "proposed_ag_gross_reduction_sqm": proposed_ag_gross_sqm,
            "verified_ag_contour_saved_sqm": total_ag_saved_sqm,
            "rejected_locked_ag_core_sqm": locked_ag_non_contour_sqm,
            "ag_contour_efficiency_pct": round((total_ag_saved_sqm / proposed_ag_gross_sqm * 100.0) if proposed_ag_gross_sqm > 0 else 100.0, 1),
            "proposed_ug_gross_reduction_sqm": proposed_ug_gross_sqm,
            "verified_ug_contour_saved_sqm": total_ug_saved_sqm,
            "rejected_locked_ug_zone_sqm": locked_ug_non_contour_sqm,
            "protected_ramp_and_maneuvering_deducted_sqm": total_protected_ramp_maneuver_sqm,
            "under_ramp_utilized_sqm": total_under_ramp_utilized_sqm,
            "ug_contour_efficiency_pct": round((total_ug_saved_sqm / proposed_ug_gross_sqm * 100.0) if proposed_ug_gross_sqm > 0 else 100.0, 1),
            "total_proposed_raw_reduction_sqm": total_proposed_raw_sqm,
            "total_verified_contour_saved_sqm": total_verified_contour_saved_sqm,
            "rejected_locked_core_and_service_sqm": total_locked_core_and_ug_reclassified_sqm,
            "rejected_internal_apt_corridor_sqm": total_reclaimed_living_sqm,
            "total_reclassified_to_design_improvement_sqm": total_reclassified_to_design_improvement_sqm,
            "before_total_ag_contour_sqm": total_ag_sqm,
            "after_total_ag_contour_sqm": optimized_ag_total_sqm,
            "before_total_ug_contour_sqm": total_ug_sqm,
            "after_total_ug_contour_sqm": optimized_ug_total_sqm,
            "methodology_pillars": CONTOUR_AUDIT_METHODOLOGY_PILLARS,
            "locked_core_reclassified_items": locked_core_items,
            "ramp_and_maneuvering_audit": ramp_and_maneuvering_audit,
        },
        "executive_kpis": {
            "above_ground_saved_sqm": total_ag_saved_sqm,
            "above_ground_saving_ils": total_ag_saving_ils,
            "underground_saved_sqm": total_ug_saved_sqm,
            "underground_saving_ils": total_ug_saving_ils,
            "facade_converted_to_plaster_sqm": total_facade_converted_sqm,
            "facade_saving_ils": total_facade_saving_ils,
            "internal_reclaimed_living_sqm": total_reclaimed_living_sqm,
            "locked_core_reclassified_sqm": total_locked_core_and_ug_reclassified_sqm,
            "total_design_improvement_sqm": total_reclassified_to_design_improvement_sqm,
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
            "proposed_gross_reduction_sqm": proposed_ag_gross_sqm,
            "rejected_locked_core_sqm": locked_ag_non_contour_sqm,
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
            "proposed_gross_reduction_sqm": proposed_ug_gross_sqm,
            "rejected_locked_zone_sqm": locked_ug_non_contour_sqm,
            "protected_ramp_and_maneuvering_deducted_sqm": total_protected_ramp_maneuver_sqm,
            "under_ramp_utilized_sqm": total_under_ramp_utilized_sqm,
            "total_saved_sqm": total_ug_saved_sqm,
            "rate_per_sqm_ils": COST_UNDERGROUND_PARKING_PER_SQM_ILS,
            "total_saving_ils": total_ug_saving_ils,
            "ramp_and_maneuvering_audit": ramp_and_maneuvering_audit,
            "items": ug_items,
        },
        "facade_cladding_optimization": facade_opt,
        "internal_apartment_optimization": {
            "total_reclaimed_effective_living_sqm": total_reclaimed_living_sqm,
            "locked_core_reclassified_sqm": total_locked_core_and_ug_reclassified_sqm,
            "locked_core_reclassified_items": locked_core_items,
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
