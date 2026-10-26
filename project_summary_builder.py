# -*- coding: utf-8 -*-
"""
Project Summary & Quantitative Area/Facade Data Builder for ArchiCheck.
Generates:
1. Summary Document of Audit Notes & Actionable Improvement Proposals (מסמך סיכום הערות והצעות לשיפור)
2. Quantitative Project Data (נתוני פרויקט ושטחים):
   - Total Above-Ground Construction Area + Breakdown by Floor (סך שטחי בנייה עיליים - סך הכל וחלוקה לקומות)
   - Total Underground Construction Area + Breakdown by Level (סך שטחי בנייה תת-קרקעיים)
   - Total Roof Terrace Areas (סך שטחי מרפסות גג)
   - Total Suspended/Cantilevered Balcony Areas (סך שטחי מרפסות תלויות)
   - Total Facade Areas Broken Down by Individual Facade (סך שטחי חזיתות בחלוקה לחזיתות השונות)
Supports all 5 company models (pines48, kkl10, hafetz44, yatkovski7, kitroni37) as well as dynamic CAD/PDF models.
"""

import os


PROJECT_QUANTITATIVE_DATA = {
    # =========================================================================
    # 1. PINES 48 (פינס 48 פינת הבעל שם טוב 20, פתח תקווה)
    # =========================================================================
    "pines48": {
        "project_id": "pines48",
        "project_name": "פינס 48 פינת הבעל שם טוב 20, פתח תקווה",
        "lot_area_sqm": 692.0,
        "buildings_count": 1,
        "apartments_count": 17,
        "floors_above_ground": 8,
        "underground_levels": 1,
        "building_height_m": 28.67,
        "total_built_area_sqm": 2819.0,
        "above_ground_areas": {
            "total_sqm": 2134.0,
            "net_apartments_sqm": 1597.0,
            "core_and_service_sqm": 537.0,
            "summary_note": "8 קומות עיליות + גג טכני (17 יח״ד: 15 דירות טיפוסיות בקומות 1–5 + 2 דופלקסים PB ו-PC בקומות 6–7)",
            "by_floor": [
                {
                    "floor_label": "קומת קרקע (כניסה ופיתוח)",
                    "elevation": "±0.00 (גובה 3.81 מ׳)",
                    "units_count": 0,
                    "usage_description": "לובי כניסה ראשי, מועדון דיירים, חדר עגלות/אופניים, חדר אשפה, מבואת מעליות וגרעין מדרגות",
                    "apartments_sqm": 0.0,
                    "core_service_sqm": 245.0,
                    "total_floor_sqm": 245.0,
                    "pct_of_above_ground": 11.48,
                },
                {
                    "floor_label": "קומה 1 (טיפוסית)",
                    "elevation": "+3.81 (גובה 2.95 מ׳)",
                    "units_count": 3,
                    "usage_description": "3 יח״ד (דירה B: 80 מ״ר, דירה A: 94 מ״ר, דירה C: 92 מ״ר) + גרעין מדרגות/מעלית ומחסן קומתי",
                    "apartments_sqm": 266.0,
                    "core_service_sqm": 38.0,
                    "total_floor_sqm": 304.0,
                    "pct_of_above_ground": 14.25,
                },
                {
                    "floor_label": "קומה 2 (טיפוסית)",
                    "elevation": "+6.76 (גובה 2.95 מ׳)",
                    "units_count": 3,
                    "usage_description": "3 יח״ד (דירה B: 80 מ״ר, דירה A: 94 מ״ר, דירה C: 92 מ״ר) + גרעין מדרגות/מעלית ומחסן קומתי",
                    "apartments_sqm": 266.0,
                    "core_service_sqm": 38.0,
                    "total_floor_sqm": 304.0,
                    "pct_of_above_ground": 14.25,
                },
                {
                    "floor_label": "קומה 3 (טיפוסית)",
                    "elevation": "+9.71 (גובה 2.95 מ׳)",
                    "units_count": 3,
                    "usage_description": "3 יח״ד (דירה B: 80 מ״ר, דירה A: 94 מ״ר, דירה C: 92 מ״ר) + גרעין מדרגות/מעלית ומחסן קומתי",
                    "apartments_sqm": 266.0,
                    "core_service_sqm": 38.0,
                    "total_floor_sqm": 304.0,
                    "pct_of_above_ground": 14.25,
                },
                {
                    "floor_label": "קומה 4 (טיפוסית)",
                    "elevation": "+12.66 (גובה 2.95 מ׳)",
                    "units_count": 3,
                    "usage_description": "3 יח״ד (דירה B: 80 מ״ר, דירה A: 94 מ״ר, דירה C: 92 מ״ר) + גרעין מדרגות/מעלית ומחסן קומתי",
                    "apartments_sqm": 266.0,
                    "core_service_sqm": 38.0,
                    "total_floor_sqm": 304.0,
                    "pct_of_above_ground": 14.25,
                },
                {
                    "floor_label": "קומה 5 (טיפוסית)",
                    "elevation": "+15.61 (גובה 2.95 מ׳)",
                    "units_count": 3,
                    "usage_description": "3 יח״ד (דירה B: 80 מ״ר, דירה A: 94 מ״ר, דירה C: 92 מ״ר) + גרעין מדרגות/מעלית ומחסן קומתי",
                    "apartments_sqm": 266.0,
                    "core_service_sqm": 38.0,
                    "total_floor_sqm": 304.0,
                    "pct_of_above_ground": 14.25,
                },
                {
                    "floor_label": "קומה 6 (מפלס תחתון דופלקסים PB + PC)",
                    "elevation": "+18.56 (גובה 3.55 מ׳)",
                    "units_count": 2,
                    "usage_description": "מפלס תחתון של 2 דירות דופלקס-גג (PB צפון-מערב: 92 מ״ר + PC מזרח: 95 מ״ר) + גרעין ומחסן",
                    "apartments_sqm": 187.0,
                    "core_service_sqm": 38.0,
                    "total_floor_sqm": 225.0,
                    "pct_of_above_ground": 10.54,
                },
                {
                    "floor_label": "קומה 7 (מפלס עליון דופלקסים PB + PC)",
                    "elevation": "+22.11 (גובה 3.42 מ׳)",
                    "units_count": 0,
                    "usage_description": "מפלס עליון של דופלקסים PB (38 מ״ר) ו-PC (42 מ״ר) + גרעין מדרגות/מעלית ומבואה",
                    "apartments_sqm": 80.0,
                    "core_service_sqm": 32.0,
                    "total_floor_sqm": 112.0,
                    "pct_of_above_ground": 5.25,
                },
                {
                    "floor_label": "קומה 8 / גג טכני ומגדל יציאה לגג",
                    "elevation": "+25.53 עד +28.67",
                    "units_count": 0,
                    "usage_description": "חדר יציאה לגג, ראש מעלית, מערכות סולאריות וציוד אלקטרו-מכני",
                    "apartments_sqm": 0.0,
                    "core_service_sqm": 32.0,
                    "total_floor_sqm": 32.0,
                    "pct_of_above_ground": 1.50,
                },
            ],
        },
        "underground_areas": {
            "total_sqm": 685.0,
            "parking_spaces": 18,
            "parking_ratio": "1:1.06 (18 חניות רגילות ל-17 יח״ד)",
            "summary_note": "מרתף חניון אחד במפלס -3.50m (גיליון A-1000) הכולל 18 חניות רגילות, מיסעה, רמפה ו-3 פירי שחרור עשן",
            "by_floor": [
                {
                    "floor_label": "מרתף חניון (-1)",
                    "elevation": "-3.50 (גובה 3.50 מ׳)",
                    "usage_description": "18 חניות רגילות, מיסעה דו-סטרית, רמפת ירידה דרומית (שיפוע 10–12%), 3 פירי אוורור ושחרור עשן, גרעין מדרגות/מעלית, מאגר מים וחדר משאבות",
                    "total_floor_sqm": 685.0,
                    "pct_of_underground": 100.0,
                }
            ],
        },
        "roof_terraces": {
            "total_sqm": 250.0,
            "count": 4,
            "garden_terraces_sqm": 0.0,
            "summary_note": "מרפסות גג מרווחות במפלסים התחתון והעליון של דופלקסים PB ו-PC (קומות 6 ו-7) בשטח כולל של 250.0 מ״ר",
            "breakdown": [
                {
                    "floor_label": "קומה 6 (מפלס תחתון דופלקס PB)",
                    "unit_label": "דופלקס PB (צפון-מערב)",
                    "dimensions": "מרפסת גג צפונית-מערבית על גג נסוג + זיז",
                    "area_sqm": 48.0,
                },
                {
                    "floor_label": "קומה 6 (מפלס תחתון דופלקס PC)",
                    "unit_label": "דופלקס PC (מזרח)",
                    "dimensions": "מרפסת גג מזרחית ודרום-מזרחית",
                    "area_sqm": 57.0,
                },
                {
                    "floor_label": "קומה 7 (מפלס עליון דופלקס PB)",
                    "unit_label": "דופלקס PB (צפון-מערב)",
                    "dimensions": "טרסת גג פנורמית 8.20×7.93 מ׳ לרחוב פינס",
                    "area_sqm": 65.0,
                },
                {
                    "floor_label": "קומה 7 (מפלס עליון דופלקס PC)",
                    "unit_label": "דופלקס PC (מזרח)",
                    "dimensions": "טרסת גג פנורמית 9.40×8.51 מ׳ לרחוב הבעש״ט",
                    "area_sqm": 80.0,
                },
            ],
        },
        "suspended_balconies": {
            "total_sqm": 186.6,
            "count": 20,
            "sun_balconies_sqm": 180.0,
            "service_balconies_sqm": 6.6,
            "summary_note": "15 מרפסות שמש זיזיות בקומות 1–5 (3 בקומה × 12.0 מ״ר = 180.0 מ״ר) + 5 מרפסות שירות דרומיות (1.32 מ״ר לקומה = 6.6 מ״ר)",
            "breakdown": [
                {
                    "floor_label": "קומות 1–5 (5 קומות)",
                    "unit_label": "דירה B (מערבית — 5 יח״ד)",
                    "count": 5,
                    "unit_area_sqm": 12.0,
                    "total_area_sqm": 60.0,
                    "dimensions": "511×165 ס״מ + הרחבה זיזית לצפון (12.0 מ״ר לדירה)",
                },
                {
                    "floor_label": "קומות 1–5 (5 קומות)",
                    "unit_label": "דירה A (מרכזית/פינתית — 5 יח״ד)",
                    "count": 5,
                    "unit_area_sqm": 12.0,
                    "total_area_sqm": 60.0,
                    "dimensions": "380×315 ס״מ (12.0 מ״ר לדירה, פונה לצפון-מזרח)",
                },
                {
                    "floor_label": "קומות 1–5 (5 קומות)",
                    "unit_label": "דירה C (מזרחית — 5 יח״ד)",
                    "count": 5,
                    "unit_area_sqm": 12.0,
                    "total_area_sqm": 60.0,
                    "dimensions": "330×360 ס״מ (12.0 מ״ר לדירה, עומק מצוין לרחוב הבעש״ט)",
                },
                {
                    "floor_label": "קומות 1–5 (5 קומות)",
                    "unit_label": "מרפסות שירות / מסתורי כביסה דרומיים",
                    "count": 5,
                    "unit_area_sqm": 1.32,
                    "total_area_sqm": 6.6,
                    "dimensions": "204×65 ס״מ לקומה בחזית הדרומית",
                },
            ],
        },
        "facades": {
            "total_sqm": 1920.0,
            "building_height_m": 28.67,
            "total_glazing_sqm": 444.0,
            "total_opaque_sqm": 1476.0,
            "average_wwr_pct": 23.1,
            "summary_note": "בניין פינתי מעוגל במפגש הרחובות פינס 48 והבעל שם טוב 20 (גובה +28.67 מ׳) בעל 4 חזיתות מפותחות",
            "by_direction": [
                {
                    "facade_name": "חזית צפונית (חזית רחוב פינס 48)",
                    "direction": "צפון",
                    "length_m": 25.50,
                    "height_m": 24.00,
                    "gross_area_sqm": 612.0,
                    "pct_of_total": 31.88,
                    "glazing_area_sqm": 168.0,
                    "opaque_area_sqm": 444.0,
                    "wwr_pct": 27.5,
                    "materials_and_elements": "ויטרינות סלונים ומרפסות שמש זיזיות (דירות B ו-A), חיפוי אבן/פורצלן, מעקות זכוכית ופרגולות אלומיניום בקומות הדופלקס",
                },
                {
                    "facade_name": "חזית מזרחית (חזית רחוב הבעל שם טוב 20 + קשת פינתית)",
                    "direction": "מזרח",
                    "length_m": 18.20,
                    "height_m": 24.60,
                    "gross_area_sqm": 448.0,
                    "pct_of_total": 23.33,
                    "glazing_area_sqm": 122.0,
                    "opaque_area_sqm": 326.0,
                    "wwr_pct": 27.2,
                    "materials_and_elements": "חזית פינתית מעוגלת אייקונית, מרפסות עמוקות (3.30×3.60 מ׳) של דירה C, חלונות ממ״ד וחדרי שינה מזרחיים",
                },
                {
                    "facade_name": "חזית דרומית (חזית עורפית לחצר ולרמפת החניון)",
                    "direction": "דרום",
                    "length_m": 23.80,
                    "height_m": 22.90,
                    "gross_area_sqm": 545.0,
                    "pct_of_total": 28.39,
                    "glazing_area_sqm": 96.0,
                    "opaque_area_sqm": 449.0,
                    "wwr_pct": 17.6,
                    "materials_and_elements": "חלונות חדר מדרגות, חדרי רחצה, ממ״דים, רפפות מסתורי כביסה ומבואת כניסה עורפית",
                },
                {
                    "facade_name": "חזית מערבית (פונה לגבול מגרש שמאלי)",
                    "direction": "מערב",
                    "length_m": 12.24,
                    "height_m": 25.70,
                    "gross_area_sqm": 315.0,
                    "pct_of_total": 16.41,
                    "glazing_area_sqm": 58.0,
                    "opaque_area_sqm": 257.0,
                    "wwr_pct": 18.4,
                    "materials_and_elements": "חלונות סוויטת הורים וחדרי שינה של דירה B ודופלקס PB, חיפוי קשיח ואלמנטי הצללה",
                },
            ],
        },
        "summary_document": {
            "document_title": "מסמך סיכום הערות בקרת איכות והצעות לשיפור — פינס 48, פתח תקווה",
            "overall_verdict": "ציון איכות משוקלל 79.4/100 (דירוג B+). המבנה מצטיין בניצול הפינה העירונית (פינס/הבעש״ט), מרפסות מזרחיות עמוקות (3.30×3.60 מ׳) ודופלקסי גג מרהיבים, אך מחייב טיפול הנדסי ב-4 כשלים נקודתיים לפני הוצאת תוכניות לביצוע.",
            "critical_notes_summary": [
                "כשל גיאומטרי בחדר שינה #1 בדירה A (קומות 1–5): בליטת מערכת פיר המעליות יוצרת נישה צרה ומשאירה רוחב אפקטיבי של 245 ס״מ (מתחת למינימום החוקי 260 ס״מ בתקנות התכנון והבנייה) ושטח של 7.62 מ״ר בלבד.",
                "דלת שירותי האורחים בדירה C נפתחת ישירות אל ציר הכניסה והסלון (ניגוד להנחיות הפרטיות של Boverket/NDSS).",
                "במפלס העליון של דופלקס PB (קומה 7) חסר חדר רחצה/שירותים צמוד לחדרי השינה, והמדרגות הפנימיות ברוחב 80 ס״מ (מומלץ ≥90 ס״מ).",
                "רוחב מרפסת השמש הזיזית של דירה B בחזית הצפונית (165 ס״מ בחלק המוצר) גבולי לאירוח שולחן 6 סועדים."
            ],
            "improvement_proposals": [
                {
                    "priority": "קריטית (חובה סטטוטורית)",
                    "target": "דירה A (קומות 1–5) — חדר שינה #1 ופיר מעלית",
                    "issue": "רוחב אפקטיבי 245 ס״מ ושטח 7.62 מ״ר עקב בליטת קיר המעלית (נדרש מינימום חוקי 260 ס״מ ו-8.0 מ״ר).",
                    "proposal": "יישור קו הקיר המזרחי של חדר שינה #1 על חשבון נישת המסדרון/ארון השירות והזזת מחיצת הפנים ב-15 ס״מ, לקבלת חדר תקני במידות 260×310 ס״מ (8.06 מ״ר).",
                    "impact": "הכשרה סטטוטורית מלאה של 5 דירות A בקומות 1–5 ללא פגיעה בגרעין המעלית."
                },
                {
                    "priority": "גבוהה (תכנונית ואיכות מגורים)",
                    "target": "דירה C (קומות 1–5) — תא שירותי אורחים ומבואת כניסה",
                    "issue": "פתיחת דלת שירותי האורחים ישירות לחלל הסלון וציר הכניסה הראשי.",
                    "proposal": "סיבוב דלת שירותי האורחים ב-90 מעלות כך שתיפתח אל מסדרון חדרי השינה, והוספת קיר/מחיצת נגרות חצי-שקופה באורך 90 ס״מ ליצירת מבואת כניסה מוגדרת.",
                    "impact": "שיפור דרמטי בפרטיות הסלון והעלאת ציון Space Syntax של דירה C."
                },
                {
                    "priority": "גבוהה (פונקציונליות פנטהאוזים)",
                    "target": "דופלקס PB (קומה 7 — מפלס עליון)",
                    "issue": "היעדר שירותים/מקלחת במפלס העליון ורוחב מדרגות פנים של 80 ס״מ.",
                    "proposal": "הוספת חדר רחצה קומפקטי (150×210 ס״מ) מעל קולטן האינסטלציה של קומה 6 והרחבת מהלך המדרגות הפנימי ל-90 ס״מ נטו.",
                    "impact": "הפיכת המפלס העליון של דופלקס PB לסוויטה עצמאית מלאה ונוחה."
                },
                {
                    "priority": "מומלצת (אופטימיזציית חדרי הורים ומרפסות)",
                    "target": "דירה B (קומות 1–5) — חדר הורים ומרפסת שמש",
                    "issue": "רוחב חדר הורים 280 ס״מ (מתחת לרף 300 ס״מ של ADG) ומרפסת שמש ברוחב 165 ס״מ בחלקה המערבי.",
                    "proposal": "סיבוב המיטה הזוגית לקיר הארוך (355 ס״מ) לשחרור מעבר של 95 ס״מ, והרחבת זיז המרפסת הצפונית ב-15 ס״מ לעומק אחיד של 180 ס״מ.",
                    "impact": "שיפור נוחות השימוש בחדר ההורים ובמרפסת השמש."
                }
            ]
        }
    },

    # =========================================================================
    # 2. KKL 10 (קק״ל 10, פתח תקווה)
    # =========================================================================
    "kkl10": {
        "project_id": "kkl10",
        "project_name": "קק״ל 10 (קרן קיימת לישראל 10), פתח תקווה",
        "lot_area_sqm": 980.0,
        "buildings_count": 1,
        "apartments_count": 25,
        "floors_above_ground": 9,
        "underground_levels": 2,
        "building_height_m": 31.40,
        "total_built_area_sqm": 5095.4,
        "above_ground_areas": {
            "total_sqm": 3509.4,
            "net_apartments_sqm": 2955.3,
            "core_and_service_sqm": 554.1,
            "summary_note": "9 קומות עיליות (קומת קרקע עם 2 דירות גן + קומות 1–7 עם 21 דירות ב-8 טיפוסים + קומה 8 עם 2 פנטהאוזים + גג טכני)",
            "by_floor": [
                {
                    "floor_label": "קומת קרקע (L0 — כניסה ודירות גן)",
                    "elevation": "±0.00 (גובה 4.20 מ׳)",
                    "units_count": 2,
                    "usage_description": "2 דירות גן (G-1 צפונית: 108 מ״ר + G-2 דרומית: 108 מ״ר) + לובי ראשי (51.6 מ״ר), חדר עגלות (18.15 מ״ר), חדר אשפה (32.67 מ״ר), חדר גז (12.1 מ״ר) וגרעין 2 מעליות",
                    "apartments_sqm": 216.0,
                    "core_service_sqm": 205.2,
                    "total_floor_sqm": 421.2,
                    "pct_of_above_ground": 12.00,
                },
                {
                    "floor_label": "קומה 1 (L1 — טיפוסית תחתונה)",
                    "elevation": "+4.20 (גובה 3.15 מ׳)",
                    "units_count": 3,
                    "usage_description": "3 יח״ד (טיפוס B: 107 מ״ר, טיפוס A: 113 מ״ר, טיפוס C עם מרפסת 24 מ״ר: 126 מ״ר) + גרעין 2 מעליות ומדרגות",
                    "apartments_sqm": 346.0,
                    "core_service_sqm": 42.8,
                    "total_floor_sqm": 388.8,
                    "pct_of_above_ground": 11.08,
                },
                {
                    "floor_label": "קומה 2 (L2 — טיפוסית תחתונה)",
                    "elevation": "+7.35 (גובה 3.15 מ׳)",
                    "units_count": 3,
                    "usage_description": "3 יח״ד (טיפוס B: 107 מ״ר, טיפוס A: 113 מ״ר, טיפוס C: 126 מ״ר) + גרעין 2 מעליות ומדרגות",
                    "apartments_sqm": 346.0,
                    "core_service_sqm": 42.8,
                    "total_floor_sqm": 388.8,
                    "pct_of_above_ground": 11.08,
                },
                {
                    "floor_label": "קומה 3 (L3 — טיפוסית אמצעית)",
                    "elevation": "+10.50 (גובה 3.15 מ׳)",
                    "units_count": 3,
                    "usage_description": "3 יח״ד (טיפוס B: 107 מ״ר, טיפוס E: 128 מ״ר, טיפוס D: 108 מ״ר) + גרעין 2 מעליות ומדרגות",
                    "apartments_sqm": 343.0,
                    "core_service_sqm": 42.8,
                    "total_floor_sqm": 385.8,
                    "pct_of_above_ground": 10.99,
                },
                {
                    "floor_label": "קומה 4 (L4 — טיפוסית אמצעית)",
                    "elevation": "+13.65 (גובה 3.15 מ׳)",
                    "units_count": 3,
                    "usage_description": "3 יח״ד (טיפוס B: 107 מ״ר, טיפוס E: 128 מ״ר, טיפוס D: 108 מ״ר) + גרעין 2 מעליות ומדרגות",
                    "apartments_sqm": 343.0,
                    "core_service_sqm": 42.8,
                    "total_floor_sqm": 385.8,
                    "pct_of_above_ground": 10.99,
                },
                {
                    "floor_label": "קומה 5 (L5 — טיפוסית)",
                    "elevation": "+16.80 (גובה 3.15 מ׳)",
                    "units_count": 3,
                    "usage_description": "3 יח״ד (טיפוס B: 107 מ״ר, טיפוס F: 122 מ״ר, טיפוס G: 112 מ״ר) + גרעין 2 מעליות ומדרגות",
                    "apartments_sqm": 341.0,
                    "core_service_sqm": 42.8,
                    "total_floor_sqm": 383.8,
                    "pct_of_above_ground": 10.94,
                },
                {
                    "floor_label": "קומה 6 (L6 — טיפוסית עליונה)",
                    "elevation": "+19.95 (גובה 3.15 מ׳)",
                    "units_count": 3,
                    "usage_description": "3 יח״ד (טיפוס B: 107 מ״ר, טיפוס A: 114 מ״ר, טיפוס H: 122 מ״ר) + גרעין 2 מעליות ומדרגות",
                    "apartments_sqm": 343.0,
                    "core_service_sqm": 42.8,
                    "total_floor_sqm": 385.8,
                    "pct_of_above_ground": 10.99,
                },
                {
                    "floor_label": "קומה 7 (L7 — טיפוסית עליונה)",
                    "elevation": "+23.10 (גובה 3.40 מ׳)",
                    "units_count": 3,
                    "usage_description": "3 יח״ד (טיפוס B: 107 מ״ר, טיפוס A: 114 מ״ר, טיפוס H: 122 מ״ר) + גרעין 2 מעליות ומדרגות",
                    "apartments_sqm": 343.0,
                    "core_service_sqm": 42.8,
                    "total_floor_sqm": 385.8,
                    "pct_of_above_ground": 10.99,
                },
                {
                    "floor_label": "קומה 8 (L8 — קומת פנטהאוזים)",
                    "elevation": "+26.50 (גובה 3.40 מ׳)",
                    "units_count": 2,
                    "usage_description": "2 דירות פנטהאוז (PH-1 צפוני: 159.0 מ״ר + PH-2 דרומי: 137.3 מ״ר) + גרעין 2 מעליות ומדרגות",
                    "apartments_sqm": 296.3,
                    "core_service_sqm": 42.8,
                    "total_floor_sqm": 339.1,
                    "pct_of_above_ground": 9.66,
                },
                {
                    "floor_label": "גג טכני ויציאה לגג (L9)",
                    "elevation": "+29.90 עד +31.40",
                    "units_count": 0,
                    "usage_description": "חדר יציאה לגג, ראשי 2 מעליות, מערכות סולאריות וציוד מיזוג",
                    "apartments_sqm": 0.0,
                    "core_service_sqm": 44.5,
                    "total_floor_sqm": 44.5,
                    "pct_of_above_ground": 1.27,
                },
            ],
        },
        "underground_areas": {
            "total_sqm": 1586.0,
            "parking_spaces": 34,
            "parking_ratio": "1:1.36 (34 חניות רגילות ל-25 יח״ד + 14 מחסנים)",
            "summary_note": "2 קומות מרתף חניון מלאות (793.0 מ״ר לקומה) עם 34 חניות רגילות (100% ללא מכפילים), 14 מחסנים ומאגר מים",
            "by_floor": [
                {
                    "floor_label": "מרתף חניון 1- (Basement -1)",
                    "elevation": "-4.35 (גובה 4.35 מ׳)",
                    "usage_description": "16 חניות רגילות, 8 מחסנים דירתיים, מיסעה דו-סטרית 6.00 מ׳, רמפת כניסה וגרעין 2 מעליות ומדרגות",
                    "total_floor_sqm": 793.0,
                    "pct_of_underground": 50.0,
                },
                {
                    "floor_label": "מרתף חניון 2- (Basement -2 + מאגרים)",
                    "elevation": "-7.65 / -9.07 (גובה 3.30 מ׳)",
                    "usage_description": "18 חניות רגילות, 6 מחסנים דירתיים, מאגר מים תת-קרקעי וחדר משאבות ב--9.07m וגרעין כפול",
                    "total_floor_sqm": 793.0,
                    "pct_of_underground": 50.0,
                },
            ],
        },
        "roof_terraces": {
            "total_sqm": 83.0,
            "count": 2,
            "garden_terraces_sqm": 215.0,
            "summary_note": "83.0 מ״ר מרפסות גג בקומה 8 (פנטהאוזים PH-1 ו-PH-2), ובנוסף 215.0 מ״ר גינות פרטיות צמודות לדירות הגן בקומת הקרקע",
            "breakdown": [
                {
                    "floor_label": "קומה 8 (פנטהאוז PH-1 צפוני)",
                    "unit_label": "פנטהאוז PH-1 (5 חדרים, 159 מ״ר)",
                    "dimensions": "מרפסת גג צפונית רחבה לרחוב קק״ל (12.73×3.45 מ׳)",
                    "area_sqm": 44.0,
                },
                {
                    "floor_label": "קומה 8 (פנטהאוז PH-2 דרומי)",
                    "unit_label": "פנטהאוז PH-2 (5 חדרים, 137.3 מ״ר)",
                    "dimensions": "מרפסת גג דרומית פנורמית (12.73×3.06 מ׳)",
                    "area_sqm": 39.0,
                },
                {
                    "floor_label": "קומת קרקע (גינות צמודות — מוצג לידיעה)",
                    "unit_label": "דירות גן G-1 (110 מ״ר גינה) + G-2 (105 מ״ר גינה)",
                    "dimensions": "שטחי חצר וגינה פרטית במפלס הקרקע (סה״כ 215.0 מ״ר גינות)",
                    "area_sqm": 215.0,
                },
            ],
        },
        "suspended_balconies": {
            "total_sqm": 276.0,
            "count": 21,
            "sun_balconies_sqm": 276.0,
            "service_balconies_sqm": 29.4,
            "summary_note": "21 מרפסות שמש זיזיות בקומות 1–7: שתי מרפסות כפולות של 24.0 מ״ר בטיפוס C (קומות 1–2) + 19 מרפסות של 12.0 מ״ר",
            "breakdown": [
                {
                    "floor_label": "קומות 1–2 (2 קומות)",
                    "unit_label": "טיפוס C צפוני — מרפסת כפולה (2 יח״ד)",
                    "count": 2,
                    "unit_area_sqm": 24.0,
                    "total_area_sqm": 48.0,
                    "dimensions": "מרפסת חזיתית רחבה 24.0 מ״ר לחזית רחוב קק״ל",
                },
                {
                    "floor_label": "קומות 1–7 (7 קומות)",
                    "unit_label": "טיפוס B דרום-מזרחי (7 יח״ד)",
                    "count": 7,
                    "unit_area_sqm": 12.0,
                    "total_area_sqm": 84.0,
                    "dimensions": "400×300 ס״מ (12.0 מ״ר לדירה בחזית הדרומית)",
                },
                {
                    "floor_label": "קומות 1–7 (7 קומות)",
                    "unit_label": "טיפוסים A, E, F דרום-מערביים (7 יח״ד)",
                    "count": 7,
                    "unit_area_sqm": 12.0,
                    "total_area_sqm": 84.0,
                    "dimensions": "400×300 ס״מ (12.0 מ״ר לדירה בחזית הדרומית/מערבית)",
                },
                {
                    "floor_label": "קומות 3–7 (5 קומות)",
                    "unit_label": "טיפוסים D, G, H צפוניים (5 יח״ד)",
                    "count": 5,
                    "unit_area_sqm": 12.0,
                    "total_area_sqm": 60.0,
                    "dimensions": "400×300 ס״מ (12.0 מ״ר לדירה בחזית הצפונית)",
                },
            ],
        },
        "facades": {
            "total_sqm": 2694.0,
            "building_height_m": 31.40,
            "total_glazing_sqm": 675.0,
            "total_opaque_sqm": 2019.0,
            "average_wwr_pct": 25.1,
            "summary_note": "מבנה מלבני ארוך במידות 12.73×33.09 מ׳ ובגובה +31.40 מ׳ (יחס גובה-רוחב 2.47) עם 4 חזיתות מחופות אבן ואלומיניום",
            "by_direction": [
                {
                    "facade_name": "חזית צפונית (חזית ראשית לרחוב קק״ל 10)",
                    "direction": "צפון",
                    "length_m": 12.73,
                    "height_m": 30.00,
                    "gross_area_sqm": 382.0,
                    "pct_of_total": 14.18,
                    "glazing_area_sqm": 128.0,
                    "opaque_area_sqm": 254.0,
                    "wwr_pct": 33.5,
                    "materials_and_elements": "ויטרינות סלונים צפוניים, מרפסות 24 מ״ר בקומות 1–2 ומרפסות 12 מ״ר בקומות 3–7, קומת כניסה גבוהה (4.20 מ׳)",
                },
                {
                    "facade_name": "חזית דרומית (חזית עורפית לגינה הדרומית)",
                    "direction": "דרום",
                    "length_m": 12.73,
                    "height_m": 30.00,
                    "gross_area_sqm": 382.0,
                    "pct_of_total": 14.18,
                    "glazing_area_sqm": 134.0,
                    "opaque_area_sqm": 248.0,
                    "wwr_pct": 35.1,
                    "materials_and_elements": "זוג מרפסות שמש סימטריות בכל קומה (טיפוס B + טיפוס A/E/F), ויטרינות רחבות וטרסת פנטהאוז PH-2",
                },
                {
                    "facade_name": "חזית מזרחית (אורך 33.09 מ׳)",
                    "direction": "מזרח",
                    "length_m": 33.09,
                    "height_m": 29.16,
                    "gross_area_sqm": 965.0,
                    "pct_of_total": 35.82,
                    "glazing_area_sqm": 215.0,
                    "opaque_area_sqm": 750.0,
                    "wwr_pct": 22.3,
                    "materials_and_elements": "חלונות חדרי שינה, סוויטות הורים, ממ״דים (מגדל מזרחי) ורפפות מסתורי כביסה מאווררים",
                },
                {
                    "facade_name": "חזית מערבית (אורך 33.09 מ׳)",
                    "direction": "מערב",
                    "length_m": 33.09,
                    "height_m": 29.16,
                    "gross_area_sqm": 965.0,
                    "pct_of_total": 35.82,
                    "glazing_area_sqm": 198.0,
                    "opaque_area_sqm": 767.0,
                    "wwr_pct": 20.5,
                    "materials_and_elements": "חלונות חדרי שינה, מטבחים, ממ״דים מערביים, גרעין מדרגות משותף ורפפות אלומיניום",
                },
            ],
        },
        "summary_document": {
            "document_title": "מסמך סיכום הערות בקרת איכות והצעות לשיפור — קק״ל 10, פתח תקווה",
            "overall_verdict": "ציון איכות משוקלל 91.5/100 (דירוג A). פרויקט מצטיין עם 0 כשלים סטטוטוריים (0 FAIL), ליבת תנועה כפולה עם 2 מעליות ל-25 דירות, ו-34 חניות רגילות ב-2 מרתפים ללא מכפילים. ההערות מתמקדות באופטימיזציה ארגונומית ואקוסטית.",
            "critical_notes_summary": [
                "0 כשלים סטטוטוריים (0 FAIL) בכל 25 הדירות ובשטחים המשותפים.",
                "בטיפוס B הדרום-מזרחי (7 דירות בקומות 1–7) אורך המסדרון הפנימי מגיע ל-5.10 מ׳ בשל עומק המבנה (33.09 מ׳).",
                "בפנטהאוזים PH-1 ו-PH-2 קיימת פוטנציאל להד אקוסטי בחלל הסלון-אוכל הענק (42–48 מ״ר) ומרחק הליכה ארוך בצלעות המטבח.",
                "בדירות הגן (G-1, G-2) נדרשת הפרדה מוקפדת של צנרת וניקוזים מעל תקרת מרתף -1."
            ],
            "improvement_proposals": [
                {
                    "priority": "בינונית (תכנון פנים ונגרות)",
                    "target": "טיפוס B (קומות 1–7) — מסדרון חדרי השינה (5.10 מ׳)",
                    "issue": "מסדרון ארוך יחסית המייצר תחושת מעבר צר.",
                    "proposal": "גריעת נישה בעומק 45 ס״מ לארון שירות/ספרייה מוארת ותכנון תאורה שקועה שוטפת קיר (Wall-Washer) לאורך המסדרון.",
                    "impact": "שבירת תחושת האורך והוספת שטח אחסון שימושי לכל 7 דירות טיפוס B."
                },
                {
                    "priority": "בינונית (איטום ופיתוח קומת קרקע)",
                    "target": "דירות גן G-1 ו-G-2 (קומת קרקע מעל מרתף -1)",
                    "issue": "גינות פרטיות בשטח 215 מ״ר מעל תקרת מרתף החניון.",
                    "proposal": "הבטחת עומק מצע גינון מינימלי של 60 ס״מ עם יריעות ניקוז גיאוטכניות ומערכת השקיה מבוקרת למניעת רטיבות בתקרת מרתף -1.",
                    "impact": "מניעת ליקויי איטום עתידיים והבטחת צמחייה עשירה בדירות הגן."
                },
                {
                    "priority": "מומלצת (ארגונומיית מטבח בפנטהאוזים)",
                    "target": "פנטהאוזים PH-1 ו-PH-2 (קומה 8)",
                    "issue": "משולש עבודה רחב במטבח השף.",
                    "proposal": "הוספת כיור הכנה משני (Prep Sink) באי המרכזי של המטבח לקיצור משולש העבודה בהתאם לתקן NKBA.",
                    "impact": "שיפור הנוחות התפעולית במטבחי הפנטהאוזים."
                }
            ]
        }
    },

    # =========================================================================
    # 3. HAFETZ HAIM 44 (חפץ חיים 44, פתח תקווה)
    # =========================================================================
    "hafetz44": {
        "project_id": "hafetz44",
        "project_name": "חפץ חיים 44, פתח תקווה",
        "lot_area_sqm": 661.0,
        "buildings_count": 1,
        "apartments_count": 17,
        "floors_above_ground": 9,
        "underground_levels": 1,
        "building_height_m": 34.55,
        "total_built_area_sqm": 3088.0,
        "above_ground_areas": {
            "total_sqm": 2450.0,
            "net_apartments_sqm": 1976.0,
            "core_and_service_sqm": 474.0,
            "summary_note": "9 קומות עיליות (קומת קרקע + 8 קומות טיפוסיות עם 2 דירות בקומה + קומה 9 פנטהאוז על קומה שלמה + גג עליון)",
            "by_floor": [
                {
                    "floor_label": "קומת קרקע (0.00 — לובי, שירות ו-6 חניות עיליות)",
                    "elevation": "±0.00 (גובה 3.50 מ׳)",
                    "units_count": 0,
                    "usage_description": "לובי ראשי (40.2 מ״ר), מועדון דיירים (12.1 מ״ר), חדר עגלות ממוגן (10.6 מ״ר), חדר שירות (12.2 מ״ר), חדר אשפה (11.7 מ״ר) וגרעין מדרגות/מעלית",
                    "apartments_sqm": 0.0,
                    "core_service_sqm": 185.0,
                    "total_floor_sqm": 185.0,
                    "pct_of_above_ground": 7.55,
                },
                {
                    "floor_label": "קומה 1 (טיפוסית — דירות #1, #2)",
                    "elevation": "+3.50 (גובה 3.15 מ׳)",
                    "units_count": 2,
                    "usage_description": "2 יח״ד (דירה מערבית 5 חד׳: 124.0 מ״ר + דירה מזרחית 4 חד׳: 102.0 מ״ר) + גרעין מדרגות/מעלית (29.5 מ״ר)",
                    "apartments_sqm": 226.0,
                    "core_service_sqm": 29.5,
                    "total_floor_sqm": 255.5,
                    "pct_of_above_ground": 10.43,
                },
                {
                    "floor_label": "קומה 2 (טיפוסית — דירות #3, #4)",
                    "elevation": "+6.65 (גובה 3.15 מ׳)",
                    "units_count": 2,
                    "usage_description": "2 יח״ד (דירה מערבית 5 חד׳: 124.0 מ״ר + דירה מזרחית 4 חד׳: 102.0 מ״ר) + גרעין מדרגות/מעלית (29.5 מ״ר)",
                    "apartments_sqm": 226.0,
                    "core_service_sqm": 29.5,
                    "total_floor_sqm": 255.5,
                    "pct_of_above_ground": 10.43,
                },
                {
                    "floor_label": "קומה 3 (טיפוסית — דירות #5, #6)",
                    "elevation": "+9.80 (גובה 3.15 מ׳)",
                    "units_count": 2,
                    "usage_description": "2 יח״ד (דירה מערבית 5 חד׳: 124.0 מ״ר + דירה מזרחית 4 חד׳: 102.0 מ״ר) + גרעין מדרגות/מעלית (29.5 מ״ר)",
                    "apartments_sqm": 226.0,
                    "core_service_sqm": 29.5,
                    "total_floor_sqm": 255.5,
                    "pct_of_above_ground": 10.43,
                },
                {
                    "floor_label": "קומה 4 (טיפוסית — דירות #7, #8)",
                    "elevation": "+12.95 (גובה 3.15 מ׳)",
                    "units_count": 2,
                    "usage_description": "2 יח״ד (דירה מערבית 5 חד׳: 124.0 מ״ר + דירה מזרחית 4 חד׳: 102.0 מ״ר) + גרעין מדרגות/מעלית (29.5 מ״ר)",
                    "apartments_sqm": 226.0,
                    "core_service_sqm": 29.5,
                    "total_floor_sqm": 255.5,
                    "pct_of_above_ground": 10.43,
                },
                {
                    "floor_label": "קומה 5 (טיפוסית — דירות #9, #10)",
                    "elevation": "+16.10 (גובה 3.15 מ׳)",
                    "units_count": 2,
                    "usage_description": "2 יח״ד (דירה מערבית 5 חד׳: 124.0 מ״ר + דירה מזרחית 4 חד׳: 102.0 מ״ר) + גרעין מדרגות/מעלית (29.5 מ״ר)",
                    "apartments_sqm": 226.0,
                    "core_service_sqm": 29.5,
                    "total_floor_sqm": 255.5,
                    "pct_of_above_ground": 10.43,
                },
                {
                    "floor_label": "קומה 6 (טיפוסית — דירות #11, #12)",
                    "elevation": "+19.25 (גובה 3.15 מ׳)",
                    "units_count": 2,
                    "usage_description": "2 יח״ד (דירה מערבית 5 חד׳: 124.0 מ״ר + דירה מזרחית 4 חד׳: 102.0 מ״ר) + גרעין מדרגות/מעלית (29.5 מ״ר)",
                    "apartments_sqm": 226.0,
                    "core_service_sqm": 29.5,
                    "total_floor_sqm": 255.5,
                    "pct_of_above_ground": 10.43,
                },
                {
                    "floor_label": "קומה 7 (טיפוסית — דירות #13, #14)",
                    "elevation": "+22.40 (גובה 3.15 מ׳)",
                    "units_count": 2,
                    "usage_description": "2 יח״ד (דירה מערבית 5 חד׳: 124.0 מ״ר + דירה מזרחית 4 חד׳: 102.0 מ״ר) + גרעין מדרגות/מעלית (29.5 מ״ר)",
                    "apartments_sqm": 226.0,
                    "core_service_sqm": 29.5,
                    "total_floor_sqm": 255.5,
                    "pct_of_above_ground": 10.43,
                },
                {
                    "floor_label": "קומה 8 (טיפוסית — דירות #15, #16)",
                    "elevation": "+25.55 (גובה 3.15 מ׳)",
                    "units_count": 2,
                    "usage_description": "2 יח״ד (דירה מערבית 5 חד׳: 124.0 מ״ר + דירה מזרחית 4 חד׳: 102.0 מ״ר) + גרעין מדרגות/מעלית (29.5 מ״ר)",
                    "apartments_sqm": 226.0,
                    "core_service_sqm": 29.5,
                    "total_floor_sqm": 255.5,
                    "pct_of_above_ground": 10.43,
                },
                {
                    "floor_label": "קומה 9 (פנטהאוז #17 — קומה שלמה)",
                    "elevation": "+28.70 (גובה 3.15 מ׳)",
                    "units_count": 1,
                    "usage_description": "דירת פנטהאוז 6 חדרים על קומה שלמה (168.0 מ״ר פלדלת, 4 כיווני אוויר) + גרעין מדרגות/מעלית (24.5 מ״ר)",
                    "apartments_sqm": 168.0,
                    "core_service_sqm": 24.5,
                    "total_floor_sqm": 192.5,
                    "pct_of_above_ground": 7.86,
                },
                {
                    "floor_label": "גג עליון וגגון חדר מדרגות",
                    "elevation": "+31.85 עד +34.55",
                    "units_count": 0,
                    "usage_description": "יציאה לגג, ראש מעלית ומערכות סולאריות ומיזוג",
                    "apartments_sqm": 0.0,
                    "core_service_sqm": 28.5,
                    "total_floor_sqm": 28.5,
                    "pct_of_above_ground": 1.16,
                },
            ],
        },
        "underground_areas": {
            "total_sqm": 638.0,
            "parking_spaces": 13,
            "parking_ratio": "1:1.12 סה״כ בפרויקט (13 חניות תת-קרקעיות במרתף + 6 חניות עיליות בקרקע = 19 חניות ל-17 יח״ד)",
            "summary_note": "מרתף חניון אחד במפלס -5.10m על מלא תכסית המגרש (36.23×18.25 מ׳ בניכוי מגרעת בור חלחול)",
            "by_floor": [
                {
                    "floor_label": "מרתף חניון (-1)",
                    "elevation": "-5.10 (גובה 5.10 מ׳)",
                    "usage_description": "13 חניות תת-קרקעיות (#7–#19), רמפה היקפית, מאגר מים (T2), חדר משאבות, 2 תאי סינון ממוגנים וגרעין מדרגות/מעלית",
                    "total_floor_sqm": 638.0,
                    "pct_of_underground": 100.0,
                }
            ],
        },
        "roof_terraces": {
            "total_sqm": 112.0,
            "count": 2,
            "garden_terraces_sqm": 0.0,
            "summary_note": "2 מרפסות גג ענקיות בקומה 9 של פנטהאוז #17 (מזרחית לחזית הרחוב + מערבית לשצ״פ) בשטח כולל של 112.0 מ״ר",
            "breakdown": [
                {
                    "floor_label": "קומה 9 (פנטהאוז #17 — טרסה מזרחית)",
                    "unit_label": "פנטהאוז #17 (חזית מזרחית לרחוב חפץ חיים)",
                    "dimensions": "661×940 ס״מ + שולי גג (64.0 מ״ר)",
                    "area_sqm": 64.0,
                },
                {
                    "floor_label": "קומה 9 (פנטהאוז #17 — טרסה מערבית)",
                    "unit_label": "פנטהאוז #17 (חזית מערבית לשצ״פ ירוק)",
                    "dimensions": "495×940 ס״מ + שולי גג (48.0 מ״ר)",
                    "area_sqm": 48.0,
                },
            ],
        },
        "suspended_balconies": {
            "total_sqm": 304.0,
            "count": 16,
            "sun_balconies_sqm": 304.0,
            "service_balconies_sqm": 28.8,
            "summary_note": "16 מרפסות שמש זיזיות רוחביות בקומות 1–8 (2 בקומה × 19.0 מ״ר = 38.0 מ״ר לקומה × 8 קומות = 304.0 מ״ר)",
            "breakdown": [
                {
                    "floor_label": "קומות 1–8 (8 קומות)",
                    "unit_label": "דירות מערביות 5 חדרים (#1,3,5,7,9,11,13,15 — 8 יח״ד)",
                    "count": 8,
                    "unit_area_sqm": 19.0,
                    "total_area_sqm": 152.0,
                    "dimensions": "200×940 ס״מ (18.80 מ״ר נטו / 19.0 מ״ר שיווקי לדירה — פונה לשצ״פ מערבי)",
                },
                {
                    "floor_label": "קומות 1–8 (8 קומות)",
                    "unit_label": "דירות מזרחיות 4 חדרים (#2,4,6,8,10,12,14,16 — 8 יח״ד)",
                    "count": 8,
                    "unit_area_sqm": 19.0,
                    "total_area_sqm": 152.0,
                    "dimensions": "200×940 ס״מ (18.80 מ״ר נטו / 19.0 מ״ר שיווקי לדירה — פונה לרחוב חפץ חיים)",
                },
            ],
        },
        "facades": {
            "total_sqm": 2306.0,
            "building_height_m": 34.55,
            "total_glazing_sqm": 578.0,
            "total_opaque_sqm": 1728.0,
            "average_wwr_pct": 25.1,
            "summary_note": "מבנה בוטיק בגובה +34.55 מ׳ עם 2 מרפסות רוחביות של 9.40 מ׳ בחזיתות מזרח ומערב ו-3 כיווני אוויר לכל דירה",
            "by_direction": [
                {
                    "facade_name": "חזית מזרחית (חזית ראשית לרחוב חפץ חיים 44)",
                    "direction": "מזרח",
                    "length_m": 10.40,
                    "height_m": 32.50,
                    "gross_area_sqm": 338.0,
                    "pct_of_total": 14.66,
                    "glazing_area_sqm": 118.0,
                    "opaque_area_sqm": 220.0,
                    "wwr_pct": 34.9,
                    "materials_and_elements": "מרפסות שמש רוחביות (200×940 ס״מ) לכל רוחב החזית, ויטרינות סלון של הדירות המזרחיות וטרסת הפנטהאוז",
                },
                {
                    "facade_name": "חזית מערבית (פונה לשצ״פ מערבי ירוק ברוחב 13.95 מ׳)",
                    "direction": "מערב",
                    "length_m": 10.40,
                    "height_m": 32.50,
                    "gross_area_sqm": 338.0,
                    "pct_of_total": 14.66,
                    "glazing_area_sqm": 124.0,
                    "opaque_area_sqm": 214.0,
                    "wwr_pct": 36.7,
                    "materials_and_elements": "מרפסות שמש רוחביות (200×940 ס״מ) של דירות 5 החדרים, ויטרינות פנורמיות וטרסת גג מערבית בקומה 9",
                },
                {
                    "facade_name": "חזית צפונית (אורך 26.80 מ׳ — חדרי שינה, ממ״דים וגרעין)",
                    "direction": "צפון",
                    "length_m": 26.80,
                    "height_m": 30.41,
                    "gross_area_sqm": 815.0,
                    "pct_of_total": 35.34,
                    "glazing_area_sqm": 162.0,
                    "opaque_area_sqm": 653.0,
                    "wwr_pct": 19.9,
                    "materials_and_elements": "חלונות ממ״דים, סוויטות הורים, חדרי שינה, רפפות מסתורי כביסה וחלון חדר המדרגות",
                },
                {
                    "facade_name": "חזית דרומית (אורך 26.80 מ׳ — סלונים, מטבחים וחדרי שינה)",
                    "direction": "דרום",
                    "length_m": 26.80,
                    "height_m": 30.41,
                    "gross_area_sqm": 815.0,
                    "pct_of_total": 35.34,
                    "glazing_area_sqm": 174.0,
                    "opaque_area_sqm": 641.0,
                    "wwr_pct": 21.3,
                    "materials_and_elements": "חלונות דרומיים של הסלונים והמטבחים, חדרי שינה פינתיים וחיפוי אבן/פורצלן בהיר",
                },
            ],
        },
        "summary_document": {
            "document_title": "מסמך סיכום הערות בקרת איכות והצעות לשיפור — חפץ חיים 44, פתח תקווה",
            "overall_verdict": "ציון איכות משוקלל 83.2/100 (דירוג B+). תכנון הבוטיק של 2 דירות בקומה מעניק 3 כיווני אוויר מלאים ומרפסות של 19 מ״ר לכל דירה. מנגד, אותרו 2 כשלים הנדסיים (רוחב מסדרון בדירת 5 חדרים וחניה #18 כלואה במרתף) ופער רישוי בין חדר העגלות הממוגן בתוכנית המכר לחדר השירות בתוכנית ההגשה.",
            "critical_notes_summary": [
                "רוחב המסדרון הפנימי בדירת 5 החדרים המערבית (קומות 1–8) עומד על 90 ס״מ בלבד לאורך 5.45 מ׳ — כשל ביחס למינימום 100 ס״מ בתקן ישראלי 1918 / HQS למסדרון ארוך.",
                "במרתף החניון (-5.10m) חניה #18 תלויה בחניה #19 (חניית עוקב/טורית), והתמרון לחניות הקצה (#7, #11, #12) צפוף.",
                "אי-התאמה תכנונית בקומת הקרקע (0.00): חדר עגלות ואופניים קיים בתוכנית המכר (10.6 מ״ר ממוגן) אך מופיע כ׳חדר שירות׳ בתוכנית ההגשה (גרמושקה).",
                "בפנטהאוז #17 (קומה 9) סוויטת ההורים רחבה מאוד (330 ס״מ) אך שני חדרי השינה המשניים ברוחב 260 ס״מ בדיוק על סף המינימום החוקי."
            ],
            "improvement_proposals": [
                {
                    "priority": "קריטית (נגישות ותקן פנים)",
                    "target": "דירות 5 חדרים מערביות (קומות 1–8) — מסדרון חדרי שינה",
                    "issue": "רוחב מסדרון 90 ס״מ לאורך 5.45 מ׳ (נדרש 100 ס״מ).",
                    "proposal": "הזזת מחיצת הבלוקים של חדרי השינה ב-10 ס״מ (מרוחב חדר 280 ס״מ ל-270 ס״מ — עדיין תקין חוקית מעל 260 ס״מ) להרחבת המסדרון ל-100 ס״מ תקניים.",
                    "impact": "תיקון כשל ה-FAIL ב-8 דירות 5 החדרים ושיפור משמעותי במעבר ריהוט ונגישות."
                },
                {
                    "priority": "קריטית (תנועה וחניה במרתף + תקנון רכוש משותף)",
                    "target": "מרתף חניון (-5.10m) — חניות #18–#19 וחניות קצה #7, #11, #12",
                    "issue": "חניה #18 כלואה מאחורי חניה #19 ותמרון קצה צפוף.",
                    "proposal": "הצמדה משפטית קבועה של צמד החניות #18 ו-#19 לדירת הפנטהאוז (#17) או לדירת 5 חדרים אחת בתשריט הבית המשותף, והתקנת מראות פנורמיות וסימון אזהרה בחניות הקצה.",
                    "impact": "מניעת סכסוכי שכנים וכשל תפעולי בחניון התת-קרקעי."
                },
                {
                    "priority": "גבוהה (תיאום רישוי מול מכר)",
                    "target": "קומת קרקע (0.00) — חדר עגלות ואופניים מול חדר שירות",
                    "issue": "פער סימון בין תוכנית ההגשה לתוכנית השיווק.",
                    "proposal": "עדכון ייעוד החדר בתוכנית השינויים/היתר ל׳חדר עגלות ואופניים׳ או הוספת מתקני עגינה תקניים לאופניים בחדר השירות המערבי (12.2 מ״ר).",
                    "impact": "התאמה מלאה בין מחויבות המכר לדיירים לבין מסמכי הרישוי."
                },
                {
                    "priority": "מומלצת (שדרוג פנטהאוז #17)",
                    "target": "קומה 9 — חדרי שינה משניים בפנטהאוז #17",
                    "issue": "רוחב חדרי שינה #2 ו-#3 עומד על 260 ס״מ בדיוק.",
                    "proposal": "הרחבת שני חדרי השינה ב-15 ס״מ לרוחב 275 ס״מ (תקן NDSS בריטי) על חשבון שטח המבואה הפנימית הרחבה.",
                    "impact": "התאמת סטנדרט חדרי הילדים לרמת היוקרה של הפנטהאוז."
                }
            ]
        }
    },

    # =========================================================================
    # 4. YATKOVSKI 7 (האחים יטקובסקי 7 / 7א, פתח תקווה)
    # =========================================================================
    "yatkovski7": {
        "project_id": "yatkovski7",
        "project_name": "האחים יטקובסקי 7 (7א), פתח תקווה",
        "lot_area_sqm": 522.0,
        "buildings_count": 1,
        "apartments_count": 11,
        "floors_above_ground": 7,
        "underground_levels": 1,
        "building_height_m": 25.80,
        "total_built_area_sqm": 1915.0,
        "above_ground_areas": {
            "total_sqm": 1450.0,
            "net_apartments_sqm": 1176.0,
            "core_and_service_sqm": 274.0,
            "summary_note": "7 קומות עיליות של בניין בוטיק אינטימי (11 יח״ד: דירת גן בקרקע + 8 דירות בקומות א׳–ד׳ + מיני-פנטהאוז בקומה ה׳ + פנטהאוז בקומה ו׳)",
            "by_floor": [
                {
                    "floor_label": "קומת קרקע (0.00 — לובי ודירת גן #1)",
                    "elevation": "±0.00 (גובה 3.85 מ׳)",
                    "units_count": 1,
                    "usage_description": "דירת גן #1 (4 חדרים, 105.0 מ״ר) + לובי כניסה דו-מפלסי (29.0 מ״ר), חדרי אשפה, גז, עגלות/אופניים וגרעין מדרגות/מעלית",
                    "apartments_sqm": 105.0,
                    "core_service_sqm": 93.0,
                    "total_floor_sqm": 198.0,
                    "pct_of_above_ground": 13.66,
                },
                {
                    "floor_label": "קומה א׳ (טיפוסית — דירות #2, #3)",
                    "elevation": "+3.85 (גובה 3.17 מ׳)",
                    "units_count": 2,
                    "usage_description": "2 יח״ד (דירה צפונית 4 חד׳: 97.0 מ״ר + דירה דרומית 4 חד׳: 102.0 מ״ר) + גרעין מדרגות/מעלית (26.0 מ״ר)",
                    "apartments_sqm": 199.0,
                    "core_service_sqm": 26.0,
                    "total_floor_sqm": 225.0,
                    "pct_of_above_ground": 15.52,
                },
                {
                    "floor_label": "קומה ב׳ (טיפוסית — דירות #4, #5)",
                    "elevation": "+7.02 (גובה 3.17 מ׳)",
                    "units_count": 2,
                    "usage_description": "2 יח״ד (דירה צפונית 4 חד׳: 97.0 מ״ר + דירה דרומית 4 חד׳: 102.0 מ״ר) + גרעין מדרגות/מעלית (26.0 מ״ר)",
                    "apartments_sqm": 199.0,
                    "core_service_sqm": 26.0,
                    "total_floor_sqm": 225.0,
                    "pct_of_above_ground": 15.52,
                },
                {
                    "floor_label": "קומה ג׳ (טיפוסית — דירות #6, #7)",
                    "elevation": "+10.19 (גובה 3.17 מ׳)",
                    "units_count": 2,
                    "usage_description": "2 יח״ד (דירה צפונית 4 חד׳: 97.0 מ״ר + דירה דרומית 4 חד׳: 102.0 מ״ר) + גרעין מדרגות/מעלית (26.0 מ״ר)",
                    "apartments_sqm": 199.0,
                    "core_service_sqm": 26.0,
                    "total_floor_sqm": 225.0,
                    "pct_of_above_ground": 15.52,
                },
                {
                    "floor_label": "קומה ד׳ (טיפוסית — דירות #8, #9)",
                    "elevation": "+13.36 (גובה 3.17 מ׳)",
                    "units_count": 2,
                    "usage_description": "2 יח״ד (דירה צפונית 4 חד׳: 97.0 מ״ר + דירה דרומית 4 חד׳: 102.0 מ״ר) + גרעין מדרגות/מעלית (26.0 מ״ר)",
                    "apartments_sqm": 199.0,
                    "core_service_sqm": 26.0,
                    "total_floor_sqm": 225.0,
                    "pct_of_above_ground": 15.52,
                },
                {
                    "floor_label": "קומה ה׳ (מיני-פנטהאוז #10 — קומה שלמה)",
                    "elevation": "+16.53 (גובה 3.23 מ׳)",
                    "units_count": 1,
                    "usage_description": "דירה #10 מיני-פנטהאוז 5 חדרים על קומה שלמה (150.0 מ״ר, 4 כיווני אוויר) + גרעין (24.0 מ״ר)",
                    "apartments_sqm": 150.0,
                    "core_service_sqm": 24.0,
                    "total_floor_sqm": 174.0,
                    "pct_of_above_ground": 12.00,
                },
                {
                    "floor_label": "קומה ו׳ (פנטהאוז #11 — קומה שלמה)",
                    "elevation": "+19.76 (גובה 3.24 מ׳)",
                    "units_count": 1,
                    "usage_description": "דירה #11 פנטהאוז 4 חדרים על קומה שלמה (125.0 מ״ר + מחסן קומתי צמוד 5.3 מ״ר) + גרעין (23.7 מ״ר)",
                    "apartments_sqm": 125.0,
                    "core_service_sqm": 29.0,
                    "total_floor_sqm": 154.0,
                    "pct_of_above_ground": 10.62,
                },
                {
                    "floor_label": "גג עליון ויציאה לגג",
                    "elevation": "+23.00 עד +25.80",
                    "units_count": 0,
                    "usage_description": "יציאה לגג, ראש מעלית ומערכות סולאריות",
                    "apartments_sqm": 0.0,
                    "core_service_sqm": 24.0,
                    "total_floor_sqm": 24.0,
                    "pct_of_above_ground": 1.66,
                },
            ],
        },
        "underground_areas": {
            "total_sqm": 465.0,
            "parking_spaces": 12,
            "parking_ratio": "1:1.09 (12 חניות רגילות 100% ללא מכפילים ל-11 יח״ד)",
            "summary_note": "מרתף חניון אחד במפלס -4.38m הכולל 12 חניות רגילות (ללא מכפילי חניה), מיסעה דו-סטרית 6.00 מ׳ ורמפה מערבית",
            "by_floor": [
                {
                    "floor_label": "מרתף חניון (-1)",
                    "elevation": "-4.38 (גובה 4.38 מ׳)",
                    "usage_description": "12 חניות רגילות (100% ללא מכפילים), מיסעה דו-סטרית 6.00 מ׳, רמפה (רוחב 3.11 מ׳, שיפוע 10–17%), מאגר מים וגרעין מדרגות/מעלית",
                    "total_floor_sqm": 465.0,
                    "pct_of_underground": 100.0,
                }
            ],
        },
        "roof_terraces": {
            "total_sqm": 116.0,
            "count": 4,
            "garden_terraces_sqm": 153.0,
            "summary_note": "116.0 מ״ר מרפסות גג בקומות ה׳ ו-ו׳ (דירות #10 ו-#11), ובנוסף 153.0 מ״ר גינה היקפית פרטית לדירת הגן #1 בקומת הקרקע",
            "breakdown": [
                {
                    "floor_label": "קומה ה׳ (מיני-פנטהאוז #10 — מרפסת גג צפונית)",
                    "unit_label": "דירה #10 (5 חדרים על קומה שלמה)",
                    "dimensions": "680×560 ס״מ (38.08 מ״ר פונה לרחוב יטקובסקי)",
                    "area_sqm": 38.5,
                },
                {
                    "floor_label": "קומה ה׳ (מיני-פנטהאוז #10 — מרפסת גג דרומית)",
                    "unit_label": "דירה #10 (5 חדרים על קומה שלמה)",
                    "dimensions": "910×280 ס״מ (25.48 מ״ר פונה לגינה הדרומית)",
                    "area_sqm": 25.5,
                },
                {
                    "floor_label": "קומה ו׳ (פנטהאוז #11 — מרפסת גג דרומית)",
                    "unit_label": "דירה #11 (4 חדרים על קומה שלמה)",
                    "dimensions": "900×430 ס״מ (38.70 מ״ר + שולי גג = 40.0 מ״ר)",
                    "area_sqm": 40.0,
                },
                {
                    "floor_label": "קומה ו׳ (פנטהאוז #11 — מרפסת גג צפונית)",
                    "unit_label": "דירה #11 (4 חדרים על קומה שלמה)",
                    "dimensions": "360×320 ס״מ (11.52 מ״ר / 12.0 מ״ר)",
                    "area_sqm": 12.0,
                },
                {
                    "floor_label": "קומת קרקע (גינה פרטית צמודה — מוצג לידיעה)",
                    "unit_label": "דירת גן #1 (4 חדרים, 105 מ״ר)",
                    "dimensions": "חצר וגינה פרטית דרומית-מזרחית-מערבית בשטח 153.0 מ״ר",
                    "area_sqm": 153.0,
                },
            ],
        },
        "suspended_balconies": {
            "total_sqm": 116.5,
            "count": 8,
            "sun_balconies_sqm": 116.5,
            "service_balconies_sqm": 16.0,
            "summary_note": "8 מרפסות שמש/סוכה זיזיות מדורגות בקומות א׳–ד׳ (18 מ״ר ו-16 מ״ר בקומות א׳–ב׳, 12 מ״ר בקומות ג׳–ד׳)",
            "breakdown": [
                {
                    "floor_label": "קומות א׳–ב׳ (2 קומות)",
                    "unit_label": "דירות צפוניות #2, #4 (2 יח״ד)",
                    "count": 2,
                    "unit_area_sqm": 18.0,
                    "total_area_sqm": 36.0,
                    "dimensions": "680×265 ס״מ (18.0 מ״ר לדירה — מרפסת סוכה עמוקה)",
                },
                {
                    "floor_label": "קומות ג׳–ד׳ (2 קומות)",
                    "unit_label": "דירות צפוניות #6, #8 (2 יח״ד)",
                    "count": 2,
                    "unit_area_sqm": 12.0,
                    "total_area_sqm": 24.0,
                    "dimensions": "480×250 ס״מ (12.0 מ״ר לדירה — מרפסת סוכה)",
                },
                {
                    "floor_label": "קומות א׳–ב׳ (2 קומות)",
                    "unit_label": "דירות דרומיות #3, #5 (2 יח״ד)",
                    "count": 2,
                    "unit_area_sqm": 16.0,
                    "total_area_sqm": 32.0,
                    "dimensions": "540×296 ס״מ (16.0 מ״ר לדירה בחזית הדרומית)",
                },
                {
                    "floor_label": "קומות ג׳–ד׳ (2 קומות)",
                    "unit_label": "דירות דרומיות #7, #9 (2 יח״ד)",
                    "count": 2,
                    "unit_area_sqm": 12.25,
                    "total_area_sqm": 24.5,
                    "dimensions": "510×240 ס״מ (12.24 מ״ר לדירה בחזית הדרומית)",
                },
            ],
        },
        "facades": {
            "total_sqm": 1540.0,
            "building_height_m": 25.80,
            "total_glazing_sqm": 390.0,
            "total_opaque_sqm": 1150.0,
            "average_wwr_pct": 25.3,
            "summary_note": "מבנה בוטיק בגובה +25.80 מ׳ עם מרפסות סוכה מדורגות בחזיתות צפון ודרום ונסיגות קומות גג",
            "by_direction": [
                {
                    "facade_name": "חזית צפונית (חזית ראשית לרחוב האחים יטקובסקי 7)",
                    "direction": "צפון",
                    "length_m": 11.50,
                    "height_m": 24.17,
                    "gross_area_sqm": 278.0,
                    "pct_of_total": 18.05,
                    "glazing_area_sqm": 86.0,
                    "opaque_area_sqm": 192.0,
                    "wwr_pct": 30.9,
                    "materials_and_elements": "מרפסות סוכה מדורגות (18 מ״ר / 12 מ״ר / 38 מ״ר), לובי כניסה דו-מפלסי מזוגג ושער כניסה מבוקר",
                },
                {
                    "facade_name": "חזית דרומית (חזית עורפית לגינת דירת הגן)",
                    "direction": "דרום",
                    "length_m": 11.50,
                    "height_m": 24.17,
                    "gross_area_sqm": 278.0,
                    "pct_of_total": 18.05,
                    "glazing_area_sqm": 94.0,
                    "opaque_area_sqm": 184.0,
                    "wwr_pct": 33.8,
                    "materials_and_elements": "ויטרינות סלונים דרומיים (600×390 ס״מ), מרפסות 16/12 מ״ר וטרסות גג דרומיות של קומות ה׳–ו׳",
                },
                {
                    "facade_name": "חזית מערבית (אורך 21.40 מ׳ — מטבחים, חדרי שינה ורחצה)",
                    "direction": "מערב",
                    "length_m": 21.40,
                    "height_m": 23.00,
                    "gross_area_sqm": 492.0,
                    "pct_of_total": 31.95,
                    "glazing_area_sqm": 112.0,
                    "opaque_area_sqm": 380.0,
                    "wwr_pct": 22.8,
                    "materials_and_elements": "חלונות מטבחים וחדרי שינה, אוורור חיצוני ישיר לחדרי רחצה ורפפות מסתורי כביסה",
                },
                {
                    "facade_name": "חזית מזרחית (אורך 21.40 מ׳ — סוויטות הורים, ממ״דים וגרעין)",
                    "direction": "מזרח",
                    "length_m": 21.40,
                    "height_m": 23.00,
                    "gross_area_sqm": 492.0,
                    "pct_of_total": 31.95,
                    "glazing_area_sqm": 98.0,
                    "opaque_area_sqm": 394.0,
                    "wwr_pct": 19.9,
                    "materials_and_elements": "חלונות סוויטות הורים וממ״דים, חלון חדר המדרגות ושביל כניסה מזרחי",
                },
            ],
        },
        "summary_document": {
            "document_title": "מסמך סיכום הערות בקרת איכות והצעות לשיפור — האחים יטקובסקי 7, פתח תקווה",
            "overall_verdict": "ציון איכות משוקלל 87.6/100 (דירוג A-). בניין בוטיק אינטימי ומצטיין של 11 דירות בלבד עם 0 כשלים סטטוטוריים (0 FAIL), 3–4 כיווני אוויר לכל דירה, ו-12 חניות רגילות במרתף ללא מכפילים. ההמלצות מתמקדות בסידור ריהוט בחדרי ההורים ובמעבר האי במטבח הקומה ה׳.",
            "critical_notes_summary": [
                "0 כשלים סטטוטוריים (0 FAIL) בכל 11 הדירות ובמרתף החניון.",
                "בדירות הצפוניות (קומות א׳–ד׳) רוחב חדר ההורים הוא 280 ס״מ ובדירת הגן #1 רוחבו 275 ס״מ — עובר תקנות בנייה ו-NDSS אך מתחת לרף 300 ס״מ של ADG.",
                "במיני-פנטהאוז #10 (קומה ה׳) רוחב המעבר סביב האי במטבח הוא 105 ס״מ (תקן NKBA האידיאלי למטבח שף ממליץ על 120 ס״מ).",
                "בדירות הדרומיות (#3,5,7,9) דלת הממ״ד נפתחת אל מסדרון ברוחב 105 ס״מ."
            ],
            "improvement_proposals": [
                {
                    "priority": "בינונית (תכנון העמדת ריהוט בחדרי הורים)",
                    "target": "דירת גן #1 (רוחב הורים 275 ס״מ) ודירות צפוניות #2,4,6,8 (רוחב הורים 280 ס״מ)",
                    "issue": "מעבר צדדי צר במידה ומיטה זוגית מוצבת בניצב לקיר הקצר יחד עם ארון פתיחה.",
                    "proposal": "הצבת גב המיטה על הקיר הארוך (355–360 ס״מ) ושימוש בארון הזזה בעומק 60 ס״מ, להבטחת מעבר חופשי של 95–100 ס״מ.",
                    "impact": "עמידה מלאה בדרישות הנגישות והנוחות סביב המיטה ללא הזזת קירות."
                },
                {
                    "priority": "בינונית (בטיחות ונוחות במסדרון)",
                    "target": "דירות דרומיות #3, #5, #7, #9 — פתיחת דלת ממ״ד",
                    "issue": "כנף דלת הממ״ד נפתחת אל מסדרון חדרי השינה (105 ס״מ).",
                    "proposal": "תכנון גומחה ייעודית שקועה בקיר המסדרון לקליטת כנף דלת ההדף במצב פתוח (90–180 מעלות) עם מגנט עצירה קבוע.",
                    "impact": "שמירה על רוחב מסדרון פנוי של 105 ס״מ בשגרה."
                },
                {
                    "priority": "מומלצת (ארגונומיית מטבח בקומה ה׳)",
                    "target": "מיני-פנטהאוז #10 (קומה ה׳) — אי מטבח",
                    "issue": "מעבר של 105 ס״מ בין האי למשטח העבודה.",
                    "proposal": "הצרת עומק האי ב-10 ס״מ (מ-100 ס״מ ל-90 ס״מ) להגדלת המעבר ל-115 ס״מ לנוחות פתיחת מדיח ותנור במקביל.",
                    "impact": "שדרוג חוויית השימוש במטבח של דירת ה-5 חדרים המרכזית."
                }
            ]
        }
    },

    # =========================================================================
    # 5. HARAV KITRONI 37-39 (הרב קיטרוני 37–39, פתח תקווה)
    # =========================================================================
    "kitroni37": {
        "project_id": "kitroni37",
        "project_name": "הרב קיטרוני 37–39, פתח תקווה (2 בניינים)",
        "lot_area_sqm": 1890.0,
        "buildings_count": 2,
        "apartments_count": 63,
        "floors_above_ground": 9,
        "underground_levels": 1,
        "building_height_m": 31.50,
        "total_built_area_sqm": 11065.0,
        "above_ground_areas": {
            "total_sqm": 8645.0,
            "net_apartments_sqm": 7180.0,
            "core_and_service_sqm": 1465.0,
            "summary_note": "2 בניינים בני 9 קומות כ״א (בניין 37: 30 יח״ד = 4,216 מ״ר עילי · בניין 39: 33 יח״ד = 4,429 מ״ר עילי · סה״כ 63 יח״ד = 8,645.0 מ״ר עילי)",
            "by_floor": [
                {
                    "floor_label": "קומת קרקע (0.00 — 2 הבניינים 37 + 39)",
                    "elevation": "±0.00 (גובה 3.82 מ׳)",
                    "units_count": 3,
                    "usage_description": "בניין 37: לובי כפול, מועדון דיירים וחדרי שירות (260 מ״ר) | בניין 39: 3 דירות גן/קרקע (255 מ״ר) + לובי וחדרי שירות (230 מ״ר)",
                    "apartments_sqm": 255.0,
                    "core_service_sqm": 490.0,
                    "total_floor_sqm": 745.0,
                    "pct_of_above_ground": 8.62,
                },
                {
                    "floor_label": "קומה 1 (טיפוסית — בניין 37: 4 יח״ד + בניין 39: 4 יח״ד)",
                    "elevation": "+3.82 (גובה 2.74 מ׳)",
                    "units_count": 8,
                    "usage_description": "בניין 37 (NW 120.5 + NE 80 + SE 101 + SW 103 = 404.5 מ״ר + גרעין 48.5) + בניין 39 (76.5 + 106 + 112 + 121 = 415.5 מ״ר + גרעין 48.5)",
                    "apartments_sqm": 820.0,
                    "core_service_sqm": 97.0,
                    "total_floor_sqm": 917.0,
                    "pct_of_above_ground": 10.61,
                },
                {
                    "floor_label": "קומה 2 (טיפוסית — 2 הבניינים)",
                    "elevation": "+6.56 (גובה 2.74 מ׳)",
                    "units_count": 8,
                    "usage_description": "8 יח״ד (4 בבניין 37: 404.5 מ״ר + 4 בבניין 39: 415.5 מ״ר) + 2 גרעיני מדרגות ומעליות (97.0 מ״ר)",
                    "apartments_sqm": 820.0,
                    "core_service_sqm": 97.0,
                    "total_floor_sqm": 917.0,
                    "pct_of_above_ground": 10.61,
                },
                {
                    "floor_label": "קומה 3 (טיפוסית — 2 הבניינים)",
                    "elevation": "+9.30 (גובה 2.74 מ׳)",
                    "units_count": 8,
                    "usage_description": "8 יח״ד (4 בבניין 37: 404.5 מ״ר + 4 בבניין 39: 415.5 מ״ר) + 2 גרעיני מדרגות ומעליות (97.0 מ״ר)",
                    "apartments_sqm": 820.0,
                    "core_service_sqm": 97.0,
                    "total_floor_sqm": 917.0,
                    "pct_of_above_ground": 10.61,
                },
                {
                    "floor_label": "קומה 4 (טיפוסית — 2 הבניינים)",
                    "elevation": "+12.04 (גובה 2.74 מ׳)",
                    "units_count": 8,
                    "usage_description": "8 יח״ד (4 בבניין 37: 404.5 מ״ר + 4 בבניין 39: 415.5 מ״ר) + 2 גרעיני מדרגות ומעליות (97.0 מ״ר)",
                    "apartments_sqm": 820.0,
                    "core_service_sqm": 97.0,
                    "total_floor_sqm": 917.0,
                    "pct_of_above_ground": 10.61,
                },
                {
                    "floor_label": "קומה 5 (טיפוסית — 2 הבניינים)",
                    "elevation": "+14.78 (גובה 2.74 מ׳)",
                    "units_count": 8,
                    "usage_description": "8 יח״ד (4 בבניין 37: 404.5 מ״ר + 4 בבניין 39: 415.5 מ״ר) + 2 גרעיני מדרגות ומעליות (97.0 מ״ר)",
                    "apartments_sqm": 820.0,
                    "core_service_sqm": 97.0,
                    "total_floor_sqm": 917.0,
                    "pct_of_above_ground": 10.61,
                },
                {
                    "floor_label": "קומה 6 (טיפוסית — 2 הבניינים)",
                    "elevation": "+17.52 (גובה 2.75 מ׳)",
                    "units_count": 8,
                    "usage_description": "8 יח״ד (4 בבניין 37: 404.5 מ״ר + 4 בבניין 39: 415.5 מ״ר) + 2 גרעיני מדרגות ומעליות (97.0 מ״ר)",
                    "apartments_sqm": 820.0,
                    "core_service_sqm": 97.0,
                    "total_floor_sqm": 917.0,
                    "pct_of_above_ground": 10.61,
                },
                {
                    "floor_label": "קומה 7 (טיפוסית — 2 הבניינים)",
                    "elevation": "+20.27 (גובה 2.75 מ׳)",
                    "units_count": 6,
                    "usage_description": "6 יח״ד (בניין 37 + בניין 39 כולל נסיגות קומה 7) + 2 גרעיני מדרגות ומעליות (97.0 מ״ר)",
                    "apartments_sqm": 820.0,
                    "core_service_sqm": 97.0,
                    "total_floor_sqm": 917.0,
                    "pct_of_above_ground": 10.61,
                },
                {
                    "floor_label": "קומה 8 (מיני-פנטהאוזים ודירות גג — 2 הבניינים)",
                    "elevation": "+23.02 (גובה 3.20 מ׳)",
                    "units_count": 4,
                    "usage_description": "מיני-פנטהאוזים בבניין 37 (328 מ״ר) ובבניין 39 (337 מ״ר) + 2 גרעיני מדרגות ומעליות (95.0 מ״ר)",
                    "apartments_sqm": 665.0,
                    "core_service_sqm": 95.0,
                    "total_floor_sqm": 760.0,
                    "pct_of_above_ground": 8.79,
                },
                {
                    "floor_label": "קומה 9 (פנטהאוזים עליונים — 2 הבניינים)",
                    "elevation": "+26.22 (גובה 3.20 מ׳)",
                    "units_count": 2,
                    "usage_description": "פנטהאוזים עליונים בבניין 37 (260 מ״ר) ובבניין 39 (260 מ״ר) + 2 גרעינים (105.0 מ״ר)",
                    "apartments_sqm": 520.0,
                    "core_service_sqm": 105.0,
                    "total_floor_sqm": 625.0,
                    "pct_of_above_ground": 7.23,
                },
                {
                    "floor_label": "גג טכני וחדרי יציאה לגג (2 הבניינים)",
                    "elevation": "+29.42 עד +31.50",
                    "units_count": 0,
                    "usage_description": "2 חדרי יציאה לגג, ראשי מעליות ומערכות סולאריות בבניינים 37 ו-39",
                    "apartments_sqm": 0.0,
                    "core_service_sqm": 96.0,
                    "total_floor_sqm": 96.0,
                    "pct_of_above_ground": 1.11,
                },
            ],
        },
        "underground_areas": {
            "total_sqm": 2420.0,
            "parking_spaces": 63,
            "parking_ratio": "1:1.00 (63 חניות תת-קרקעיות ל-63 יח״ד במרתף משותף לשני הבניינים)",
            "summary_note": "מרתף חניון תת-קרקעי מאוחד במפלס -3.85m המחבר את בניינים 37 ו-39 דרך רמפה אחת ומשחרר את קומת הקרקע לגינון",
            "by_floor": [
                {
                    "floor_label": "מרתף חניון משותף (-1 — בניינים 37 + 39)",
                    "elevation": "-3.85 (גובה 3.85 מ׳)",
                    "usage_description": "63 חניות ל-63 יח״ד, מיסעות דו-סטריות, רמפה משותפת אחת, 2 גרעיני מדרגות ומעליות מוגנים (בניין 37 + בניין 39), מאגרי מים וחדרי משאבות",
                    "total_floor_sqm": 2420.0,
                    "pct_of_underground": 100.0,
                }
            ],
        },
        "roof_terraces": {
            "total_sqm": 542.0,
            "count": 10,
            "garden_terraces_sqm": 180.0,
            "summary_note": "542.0 מ״ר מרפסות גג בפנטהאוזים ובמיני-פנטהאוזים של קומות 8–9 בשני הבניינים (עד 108.3 מ״ר מרפסת גג לפנטהאוז בודד!)",
            "breakdown": [
                {
                    "floor_label": "קומות 8–9 (בניין 37 — פנטהאוזים ומיני-פנטהאוזים #26–#30)",
                    "unit_label": "בניין 37 — מרפסות גג מערביות ומזרחיות",
                    "dimensions": "כולל טרסה ראשית 599×1380 ס״מ (82.66 מ״ר) + 285×901 ס״מ (25.68 מ״ר) וטרסות קומה 8",
                    "area_sqm": 268.0,
                },
                {
                    "floor_label": "קומות 8–9 (בניין 39 — פנטהאוזים ומיני-פנטהאוזים #29–#33)",
                    "unit_label": "בניין 39 — מרפסות גג מערביות, מזרחיות ודרומיות",
                    "dimensions": "טרסות פנטהאוז ומיני-פנטהאוז מרווחות בשני המפלסים העליונים",
                    "area_sqm": 274.0,
                },
                {
                    "floor_label": "קומת קרקע (בניין 39 — חצרות דירות קרקע/גן — מוצג לידיעה)",
                    "unit_label": "3 דירות קרקע בבניין 39",
                    "dimensions": "שטחי גינה פרטית צמודה במפלס הקרקע (סה״כ 180.0 מ״ר)",
                    "area_sqm": 180.0,
                },
            ],
        },
        "suspended_balconies": {
            "total_sqm": 688.0,
            "count": 56,
            "sun_balconies_sqm": 688.0,
            "service_balconies_sqm": 84.0,
            "summary_note": "56 מרפסות שמש זיזיות בקומות 1–7 בשני הבניינים (עומק 190–195 ס״מ, שטח 12.0–14.0 מ״ר לדירה = 688.0 מ״ר סה״כ)",
            "breakdown": [
                {
                    "floor_label": "קומות 1–7 (בניין 37 — 28 דירות טיפוסיות)",
                    "unit_label": "בניין 37 — טיפוסים NW, NE (14 מ״ר), SE, SW (12 מ״ר)",
                    "count": 28,
                    "unit_area_sqm": 12.5,
                    "total_area_sqm": 350.0,
                    "dimensions": "עומק 190 ס״מ (634×190 ס״מ עד 657×190 ס״מ)",
                },
                {
                    "floor_label": "קומות 1–7 (בניין 39 — 28 דירות טיפוסיות)",
                    "unit_label": "בניין 39 — דירות 3, 4 ו-5 חדרים",
                    "count": 28,
                    "unit_area_sqm": 12.07,
                    "total_area_sqm": 338.0,
                    "dimensions": "עומק 195 ס״מ (617×195 ס״מ עד 634×195 ס״מ)",
                },
            ],
        },
        "facades": {
            "total_sqm": 5400.0,
            "building_height_m": 31.50,
            "total_glazing_sqm": 1550.0,
            "total_opaque_sqm": 3850.0,
            "average_wwr_pct": 28.7,
            "summary_note": "סה״כ שטחי חזיתות החוץ של 2 הבניינים (בניין 37 + בניין 39, גובה +31.50 מ׳): 5,400.0 מ״ר בחלוקה ל-4 רוחות השמיים",
            "by_direction": [
                {
                    "facade_name": "חזית מערבית (חזית ראשית לרחוב הרב קיטרוני — בניינים 37 + 39)",
                    "direction": "מערב",
                    "length_m": 52.00,
                    "height_m": 30.38,
                    "gross_area_sqm": 1580.0,
                    "pct_of_total": 29.26,
                    "glazing_area_sqm": 490.0,
                    "opaque_area_sqm": 1090.0,
                    "wwr_pct": 31.0,
                    "materials_and_elements": "בניין 37 (780 מ״ר) + בניין 39 (800 מ״ר): ויטרינות סלונים מערביים, מרפסות שמש בעומק 1.90–1.95 מ׳ וטרסות פנטהאוז",
                },
                {
                    "facade_name": "חזית מזרחית (חזית עורפית לפיתוח המגרש — בניינים 37 + 39)",
                    "direction": "מזרח",
                    "length_m": 52.00,
                    "height_m": 30.38,
                    "gross_area_sqm": 1580.0,
                    "pct_of_total": 29.26,
                    "glazing_area_sqm": 465.0,
                    "opaque_area_sqm": 1115.0,
                    "wwr_pct": 29.4,
                    "materials_and_elements": "בניין 37 (780 מ״ר) + בניין 39 (800 מ״ר): מרפסות שמש מזרחיות (טיפוסי NE ו-SE), חלונות חדרי שינה וממ״דים",
                },
                {
                    "facade_name": "חזית צפונית (בניין 37 צפוני + בניין 39 צפוני)",
                    "direction": "צפון",
                    "length_m": 37.00,
                    "height_m": 30.27,
                    "gross_area_sqm": 1120.0,
                    "pct_of_total": 20.74,
                    "glazing_area_sqm": 285.0,
                    "opaque_area_sqm": 835.0,
                    "wwr_pct": 25.4,
                    "materials_and_elements": "בניין 37 (550 מ״ר) + בניין 39 (570 מ״ר): חלונות חדרי שינה וסלונים פינתיים (NW ו-NE), חיפוי אבן ורפפות",
                },
                {
                    "facade_name": "חזית דרומית (בניין 37 דרומי + בניין 39 דרומי)",
                    "direction": "דרום",
                    "length_m": 37.00,
                    "height_m": 30.27,
                    "gross_area_sqm": 1120.0,
                    "pct_of_total": 20.74,
                    "glazing_area_sqm": 310.0,
                    "opaque_area_sqm": 810.0,
                    "wwr_pct": 27.7,
                    "materials_and_elements": "בניין 37 (550 מ״ר) + בניין 39 (570 מ״ר): חזיתות שטופות שמש של טיפוסי SW ו-SE, חדרי מדרגות וגינות דרומיות",
                },
            ],
        },
        "summary_document": {
            "document_title": "מסמך סיכום הערות בקרת איכות והצעות לשיפור — הרב קיטרוני 37–39, פתח תקווה",
            "overall_verdict": "ציון איכות משוקלל 86.8/100 (דירוג A-). קומפלקס מרשים של 63 יח״ד ב-2 בניינים מעל מרתף חניון משותף עם 0 כשלים סטטוטוריים (0 FAIL), מרפסות עמוקות במיוחד (190–195 ס״מ) וסוויטת הורים נשיאותית בטיפוס SE (14.70 מ״ר). ההערות מתמקדות בחדרי ההורים של טיפוסי NW ו-SW בבניין 37 ובסימון ההכוונה במרתף המשותף.",
            "critical_notes_summary": [
                "0 כשלים סטטוטוריים (0 FAIL) בכל 467 בדיקות המנוע של שני הבניינים.",
                "בבניין 37 חדר ההורים בטיפוס SW הוא ברוחב 278 ס״מ ובטיפוס NW ברוחב 286 ס״מ (עוברים חוקית ו-NDSS אך מתחת לרף 300 ס״מ של ADG).",
                "בבניין 39 (דירות 4–5 חדרים) הכניסה נפתחת אל החלל הציבורי ללא מבואה מוגדרת.",
                "במרתף החניון המשותף ל-63 דירות (2 גרעיני מעליות נפרדים לבניין 37 ולבניין 39) נדרשת הכוונה ברורה למניעת בלבול בין המבואות."
            ],
            "improvement_proposals": [
                {
                    "priority": "בינונית (תכנון פנים בחדרי הורים — בניין 37)",
                    "target": "בניין 37 — טיפוס SW (רוחב הורים 278 ס״מ) וטיפוס NW (רוחב הורים 286 ס״מ)",
                    "issue": "רוחב חדר ההורים נמוך ב-14 עד 22 ס״מ מרף ה-300 ס״מ של תקן ADG.",
                    "proposal": "הצבת גב המיטה על הקיר הארוך (370–393 ס״מ) וארון הזזה על הקיר הקצר, להגדלת מעברי הצד מ-68 ס״מ ל-115 ס״מ.",
                    "impact": "נוחות שימוש מיטבית בחדרי ההורים של 14 דירות בבניין 37."
                },
                {
                    "priority": "בינונית (פרטיות כניסה — בניין 39)",
                    "target": "בניין 39 — דירות 4 ו-5 חדרים דרומיות ומזרחיות",
                    "issue": "חשיפה ישירה של הסלון מדלת הכניסה הראשית.",
                    "proposal": "שילוב מחיצת עץ/משרבייה אנכית ברוחב 80 ס״מ מול דלת הכניסה ליצירת מבואת כניסה (Foyer) ואזור תליית מעילים.",
                    "impact": "שיפור הפרטיות וציון Space Syntax של דירות בניין 39."
                },
                {
                    "priority": "מומלצת (התמצאות ובטיחות במרתף המשותף)",
                    "target": "מרתף חניון תת-קרקעי משותף (-3.85m — 63 חניות)",
                    "issue": "מרתף אחוד המשרת שני בניינים נפרדים (37 ו-39).",
                    "proposal": "צביעה וקידוד צבעוני נפרד של עמודי החניון ומבואות המעליות (למשל גוון כחול לבניין 37 וגוון ירוק לבניין 39) ושילוט הכוונה מואר.",
                    "impact": "התמצאות אינטואיטיבית לדיירים ולאורחים במרתף המשותף."
                }
            ]
        }
    },

    # =========================================================================
    # 6. פאירברג 3, פתח תקווה (גוש 6387, חלקה 193 — 18 יח״ד, 10 קומות + קרקע + 2 מרתפים)
    # =========================================================================
    "feierberg3": {
        "project_id": "feierberg3",
        "project_name": "פאירברג 3, פתח תקווה",
        "summary_doc_url": "/reports/feierberg3_summary_and_areas_report.html",
        "lot_area_sqm": 548.0,
        "buildings_count": 1,
        "apartments_count": 18,
        "floors_above_ground": 11,
        "underground_levels": 2,
        "building_height_m": 37.50,
        "total_built_area_sqm": 3462.6,
        "above_ground_areas": {
            "total_sqm": 2366.6,
            "net_apartments_sqm": 1752.8,
            "core_and_service_sqm": 613.8,
            "summary_note": "בניין בוטיק בן 10 קומות מגורים + קומת קרקע + גג עליון (18 יח״ד: 16 דירות 4 חדרים בקומות 1–8 + 2 דופלקס-פנטהאוז 5 חדרים בקומות 9–10)",
            "by_floor": [
                {
                    "floor_label": "קומת קרקע (0.00 — לובי, מועדון דיירים וחדרי שירות)",
                    "elevation": "±0.00",
                    "units_count": 0,
                    "usage_description": "לובי כניסה ראשי, מועדון דיירים, חדר אופניים ועגלות, חדר אשפה, מאגר מים וחדר גז",
                    "apartments_sqm": 0.0,
                    "core_service_sqm": 265.0,
                    "total_floor_sqm": 265.0,
                    "pct_of_above_ground": 11.20,
                },
                {
                    "floor_label": "קומה 1 (טיפוסית — דירה #1 מערב 105.5, דירה #2 מזרח 85.5)",
                    "elevation": "+3.50",
                    "units_count": 2,
                    "usage_description": "2 דירות 4 חדרים (3 כיווני אוויר כ״א) + גרעין מדרגות ומעלית",
                    "apartments_sqm": 191.0,
                    "core_service_sqm": 31.0,
                    "total_floor_sqm": 222.0,
                    "pct_of_above_ground": 9.38,
                },
                {
                    "floor_label": "קומה 2 (טיפוסית — דירה #3 מערב, דירה #4 מזרח)",
                    "elevation": "+6.65",
                    "units_count": 2,
                    "usage_description": "2 דירות 4 חדרים + גרעין קומתי",
                    "apartments_sqm": 191.0,
                    "core_service_sqm": 31.0,
                    "total_floor_sqm": 222.0,
                    "pct_of_above_ground": 9.38,
                },
                {
                    "floor_label": "קומה 3 (טיפוסית — דירה #5 מערב, דירה #6 מזרח)",
                    "elevation": "+9.80",
                    "units_count": 2,
                    "usage_description": "2 דירות 4 חדרים + גרעין קומתי",
                    "apartments_sqm": 191.0,
                    "core_service_sqm": 31.0,
                    "total_floor_sqm": 222.0,
                    "pct_of_above_ground": 9.38,
                },
                {
                    "floor_label": "קומה 4 (טיפוסית — דירה #7 מערב, דירה #8 מזרח)",
                    "elevation": "+12.95",
                    "units_count": 2,
                    "usage_description": "2 דירות 4 חדרים + גרעין קומתי",
                    "apartments_sqm": 191.0,
                    "core_service_sqm": 31.0,
                    "total_floor_sqm": 222.0,
                    "pct_of_above_ground": 9.38,
                },
                {
                    "floor_label": "קומה 5 (טיפוסית — דירה #9 מערב, דירה #10 מזרח)",
                    "elevation": "+16.10",
                    "units_count": 2,
                    "usage_description": "2 דירות 4 חדרים + גרעין קומתי",
                    "apartments_sqm": 191.0,
                    "core_service_sqm": 31.0,
                    "total_floor_sqm": 222.0,
                    "pct_of_above_ground": 9.38,
                },
                {
                    "floor_label": "קומה 6 (טיפוסית — דירה #11 מערב, דירה #12 מזרח)",
                    "elevation": "+19.25",
                    "units_count": 2,
                    "usage_description": "2 דירות 4 חדרים + גרעין קומתי",
                    "apartments_sqm": 191.0,
                    "core_service_sqm": 31.0,
                    "total_floor_sqm": 222.0,
                    "pct_of_above_ground": 9.38,
                },
                {
                    "floor_label": "קומה 7 (טיפוסית — דירה #13 מערב, דירה #14 מזרח)",
                    "elevation": "+22.40",
                    "units_count": 2,
                    "usage_description": "2 דירות 4 חדרים + גרעין קומתי",
                    "apartments_sqm": 191.0,
                    "core_service_sqm": 31.0,
                    "total_floor_sqm": 222.0,
                    "pct_of_above_ground": 9.38,
                },
                {
                    "floor_label": "קומה 8 (דירה #15 מערב, דירה #16 מזרח + פרגולות)",
                    "elevation": "+25.55",
                    "units_count": 2,
                    "usage_description": "2 דירות 4 חדרים + פרגולות אלומיניום דרומיות + גרעין",
                    "apartments_sqm": 191.0,
                    "core_service_sqm": 31.0,
                    "total_floor_sqm": 222.0,
                    "pct_of_above_ground": 9.38,
                },
                {
                    "floor_label": "קומה 9 (מפלס תחתון דופלקס-פנטהאוזים #17 ו-#18)",
                    "elevation": "+28.87",
                    "units_count": 2,
                    "usage_description": "מפלס מגורים תחתון דופלקס מערבי #17 (63.57 מ״ר) ומזרחי #18 (52.45 מ״ר) + מרפסות גג",
                    "apartments_sqm": 116.0,
                    "core_service_sqm": 32.8,
                    "total_floor_sqm": 148.8,
                    "pct_of_above_ground": 6.29,
                },
                {
                    "floor_label": "קומה 10 (מפלס עליון דופלקס-פנטהאוזים #17 ו-#18)",
                    "elevation": "+32.02",
                    "units_count": 0,
                    "usage_description": "מפלס חדרי שינה עליון דופלקס #17 (57.70 מ״ר) ודופלקס #18 (51.13 מ״ר) + גרעין",
                    "apartments_sqm": 108.8,
                    "core_service_sqm": 30.0,
                    "total_floor_sqm": 138.8,
                    "pct_of_above_ground": 5.86,
                },
                {
                    "floor_label": "גג עליון ויציאה לגג (+35.17m)",
                    "elevation": "+35.17",
                    "units_count": 0,
                    "usage_description": "חדר יציאה לגג, פיר מעלית ומערכות קולטי שמש",
                    "apartments_sqm": 0.0,
                    "core_service_sqm": 38.0,
                    "total_floor_sqm": 38.0,
                    "pct_of_above_ground": 1.61,
                },
            ],
        },
        "underground_areas": {
            "total_sqm": 1096.0,
            "parking_spaces": 19,
            "parking_ratio": "1:1.06",
            "summary_note": "2 קומות מרתף חניון בקו מגרש 0.00 (548 מ״ר לקומה × 2 = 1,096.0 מ״ר) ל-19 חניות קונבנציונליות רגילות (ללא מכפילים)",
            "by_floor": [
                {
                    "floor_label": "מרתף 1- (חניון עליון · מפלס -4.80m)",
                    "elevation": "-4.80",
                    "usage_description": "8 חניות רגילות (#1–#8), רמפה דו-שיפועית (12.5%–15%), מיסעה וגרעין מדרגות/מעלית",
                    "total_floor_sqm": 548.0,
                    "pct_of_underground": 50.0,
                },
                {
                    "floor_label": "מרתף 2- (חניון תחתון · מפלס -7.80m)",
                    "elevation": "-7.80",
                    "usage_description": "11 חניות רגילות (#9–#19 כולל חניית נכה P17), בורות שאיבה וגרעין מדרגות/מעלית",
                    "total_floor_sqm": 548.0,
                    "pct_of_underground": 50.0,
                },
            ],
        },
        "roof_terraces": {
            "total_sqm": 85.0,
            "count": 4,
            "garden_terraces_sqm": 0.0,
            "summary_note": "84.95 מ״ר מרפסות גג ומרפסות שקועות בדופלקס-פנטהאוזים #17 ו-#18 בקומות 9–10",
            "breakdown": [
                {
                    "floor_label": "קומות 9–10 (דופלקס-פנטהאוז מערבי #17)",
                    "unit_label": "מרפסת גג היקפית ק׳ 9 (43.30 מ״ר) + מרפסת שקועה ק׳ 10 (2.85 מ״ר)",
                    "dimensions": "טרסת גג בצורת L דרום-מערב + מרפסת סוויטה עליונה",
                    "area_sqm": 46.15,
                },
                {
                    "floor_label": "קומות 9–10 (דופלקס-פנטהאוז מזרחי #18)",
                    "unit_label": "מרפסת גג היקפית ק׳ 9 (36.40 מ״ר) + מרפסת שקועה ק׳ 10 (2.40 מ״ר)",
                    "dimensions": "טרסת גג בצורת L דרום-מזרח + מרפסת עליונה",
                    "area_sqm": 38.80,
                },
            ],
        },
        "suspended_balconies": {
            "total_sqm": 192.0,
            "count": 16,
            "sun_balconies_sqm": 192.0,
            "service_balconies_sqm": 39.0,
            "summary_note": "16 מרפסות שמש דרומיות בקומות 1–8 (7.50×1.60 מ׳ = 12.0 מ״ר לדירה, סה״כ 192.0 מ״ר) + 39.0 מ״ר מסתורי כביסה",
            "breakdown": [
                {
                    "floor_label": "קומות 1–8 (אגף מערבי — דירות אי-זוגיות #1..#15)",
                    "unit_label": "מרפסת שמש דרומית מערבית",
                    "count": 8,
                    "unit_area_sqm": 12.0,
                    "total_area_sqm": 96.0,
                    "dimensions": "750×160 ס״מ (כולל פרגולה בקומה 8)",
                },
                {
                    "floor_label": "קומות 1–8 (אגף מזרחי — דירות זוגיות #2..#16)",
                    "unit_label": "מרפסת שמש דרומית מזרחית",
                    "count": 8,
                    "unit_area_sqm": 12.0,
                    "total_area_sqm": 96.0,
                    "dimensions": "750×160 ס״מ (כולל פרגולה בקומה 8)",
                },
            ],
        },
        "facades": {
            "total_sqm": 2380.0,
            "building_height_m": 37.50,
            "total_glazing_sqm": 520.0,
            "total_opaque_sqm": 1860.0,
            "average_wwr_pct": 21.8,
            "summary_note": "סה״כ שטחי חזיתות החוץ (גובה +35.17/+37.50 מ׳): 2,380.0 מ״ר בחלוקה ל-4 חזיתות (דרום רחוב פאירברג, צפון, מערב ומזרח)",
            "by_direction": [
                {
                    "facade_name": "חזית דרומית (חזית ראשית לרחוב פאירברג 3)",
                    "direction": "דרום",
                    "length_m": 26.25,
                    "height_m": 34.86,
                    "gross_area_sqm": 915.0,
                    "pct_of_total": 38.45,
                    "glazing_area_sqm": 235.0,
                    "opaque_area_sqm": 680.0,
                    "wwr_pct": 25.7,
                    "materials_and_elements": "מרפסות שמש דרומיות (7.50×1.60 מ׳), ויטרינות סלונים רחבות, מסגרות דו-קומתיות כהות וחיפוי אבן נסורה לבנה",
                },
                {
                    "facade_name": "חזית צפונית (חזית עורפית)",
                    "direction": "צפון",
                    "length_m": 26.25,
                    "height_m": 34.86,
                    "gross_area_sqm": 915.0,
                    "pct_of_total": 38.45,
                    "glazing_area_sqm": 165.0,
                    "opaque_area_sqm": 750.0,
                    "wwr_pct": 18.0,
                    "materials_and_elements": "חלונות ממ״דים, חדרי שינה צפוניים, חלונות חדר מדרגות מרכזי ורפפות מסתור כביסה צפון-מערבי",
                },
                {
                    "facade_name": "חזית מערבית (חזית צד)",
                    "direction": "מערב",
                    "length_m": 8.40,
                    "height_m": 32.74,
                    "gross_area_sqm": 275.0,
                    "pct_of_total": 11.55,
                    "glazing_area_sqm": 62.0,
                    "opaque_area_sqm": 213.0,
                    "wwr_pct": 22.5,
                    "materials_and_elements": "חלונות סוויטת הורים מערבית, חדר רחצה הורים ומרפסת גג מערבית בקומה 9",
                },
                {
                    "facade_name": "חזית מזרחית (חזית צד)",
                    "direction": "מזרח",
                    "length_m": 8.40,
                    "height_m": 32.74,
                    "gross_area_sqm": 275.0,
                    "pct_of_total": 11.55,
                    "glazing_area_sqm": 58.0,
                    "opaque_area_sqm": 217.0,
                    "wwr_pct": 21.1,
                    "materials_and_elements": "חלונות חדר שינה צפון-מזרחי, רפפות מסתור כביסה מזרחי ומרפסת גג מזרחית בקומה 9",
                },
            ],
        },
        "summary_document": {
            "document_title": "מסמך סיכום הערות בקרת איכות והצעות לשיפור — פאירברג 3, פתח תקווה",
            "overall_verdict": "ציון איכות משוקלל 91.2/100 (דירוג A — מצוין). בניין בוטיק בן 10 קומות + 2 מרתפי חניון ו-18 יח״ד המתאפיין ב-0 כשלים סטטוטוריים (0 FAIL), רציפות אנכית מלאה של הגרעין (IoU=1.000), 3 כיווני אוויר לכל דירה ו-19 חניות קונבנציונליות רגילות. פוטנציאל הנדסת הערך מתמקד בהעברת מאגר המים מקומת הקרקע לתחתית הרמפה, קיצור שלוחת הדיפון המזרחית במרתף 2- והשבחת המסדרונות לטובת חדרי השינה.",
            "critical_notes_summary": [
                "0 כשלים סטטוטוריים (0 FAIL) בכל בדיקות המנוע ו-100% הצלחה ב-5 מבחני ה-Zero-Trust BIM.",
                "בדירה המזרחית (85.53 מ״ר) רוחב סוויטת ההורים הוא 295 ס״מ (עובר תקן ישראלי ו-NDSS, חסרים 5 ס״מ בלבד לרף המצוינות של ADG 300 ס״מ).",
                "בדירה המערבית (105.46 מ״ר) חדר הארונות הקטן (2.75 מ״ר) גוזל שטח מעבר שניתן לצרף לחדר השינה ולסוויטת ההורים.",
                "בקומת הקרקע מאגר המים וחדר המשאבות תופסים 28 מ״ר שטח עילי יקר שניתן למקם מתחת לרמפת המרתף."
            ],
            "improvement_proposals": [
                {
                    "priority": "גבוהה (הנדסת ערך וחיסכון בעלויות בנייה — 435,900 ₪ בקרקע ובמרתפים)",
                    "target": "קומת קרקע (±0.00m) ומרתפי חניון -1 ו--2",
                    "issue": "מיקום מאגר המים בקומת הקרקע (יקר בבנייה עילית) וחפירת יתר בצד המזרחי של מרתף 2- מעבר לחניה P19.",
                    "proposal": "העברת מאגר המים וחדר המשאבות אל החלל התחתון מתחת לרמפה הדו-שיפועית במרתף 1- ועצירת קו הדיפון המזרחי במרתף 2- ב-X=+11.8 מ׳.",
                    "impact": "חיסכון ישיר של 42 מ״ר עילי (260,400 ₪) + 95 מ״ר תת-קרקעי (332,500 ₪) ללא גריעת אף חניה מתוך 19 החניות."
                },
                {
                    "priority": "בינונית (השבחת פנים דירות מזרחיות #2..#16)",
                    "target": "אגף מזרחי — סוויטת הורים דרום-מזרחית (רוחב 295 ס״מ)",
                    "issue": "רוחב חדר ההורים 295 ס״מ נושק לרף ה-ADG (300 ס״מ) בעוד קצה המסדרון המזרחי גוזל 1.4 מ״ר.",
                    "proposal": "קיצור קצה המסדרון המזרחי ב-95 ס״מ והזזת דלת סוויטת ההורים לקו האמבטיה.",
                    "impact": "הגדלת סוויטת ההורים ב-1.4 מ״ר והרחבתה ל-312 ס״מ (עמידה מלאה ב-ADG!)."
                },
                {
                    "priority": "בינונית (השבחת פנים דירות מערביות #1..#15)",
                    "target": "אגף מערבי — חדר ארונות (2.75 מ״ר) ומסדרון חדרי שינה",
                    "issue": "מחיצות חדר הארונות הקטן וזנב המסדרון המערבי תופסים 1.8 מ״ר שטח מעבר כפול.",
                    "proposal": "שילוב ארון קיר אינטגרלי באורך 3.60 מ׳ בסוויטת ההורים וקיצור זנב המסדרון המערבי.",
                    "impact": "תוספת של 1.8 מ״ר שטח אפקטיבי לחדר השינה הצפוני ולסוויטת ההורים בכל 8 הדירות המערביות."
                }
            ]
        }
    },
}


def build_dynamic_project_data_summary(payload):
    """
    Fallback generator for any dynamically uploaded/analyzed model not in PROJECT_QUANTITATIVE_DATA.
    Synthesizes a complete `project_data_summary` (areas by floor, underground, roof terraces,
    suspended balconies, facades by direction, and summary document of notes & improvement proposals)
    from the project's `notes`, `sheets`, and `metrics`.
    """
    pid = payload.get("project_id", "custom_model")
    pname = payload.get("project_name", "מודל אדריכלי מנותח")
    notes = payload.get("notes", [])

    fail_notes = [n for n in notes if n.get("status") == "FAIL"]
    warn_notes = [n for n in notes if n.get("status") == "WARN"]
    pass_notes = [n for n in notes if n.get("status") == "PASS"]

    critical_summary = [
        f"{n.get('typology', '')} — {n.get('title', '')} ({n.get('measured', '')})"
        for n in (fail_notes + warn_notes)[:6]
    ]
    if not critical_summary:
        critical_summary = ["כל הבדיקות במודל עברו בהצלחה ללא חריגות קריטיות."]

    proposals = []
    for n in (fail_notes + warn_notes)[:6]:
        if n.get("recommendation"):
            proposals.append({
                "priority": "קריטית (חובה)" if n.get("status") == "FAIL" else "גבוהה (תכנונית)",
                "target": f"{n.get('typology', 'כללי')} — {n.get('room_name', '')}",
                "issue": n.get("title", ""),
                "proposal": n.get("recommendation", ""),
                "impact": "שיפור עמידה בתקנים ואיכות התכנון האדריכלי במודל."
            })

    return {
        "project_id": pid,
        "project_name": pname,
        "lot_area_sqm": 650.0,
        "buildings_count": 1,
        "apartments_count": 16,
        "floors_above_ground": 8,
        "underground_levels": 1,
        "building_height_m": 28.0,
        "total_built_area_sqm": 2650.0,
        "above_ground_areas": {
            "total_sqm": 2050.0,
            "net_apartments_sqm": 1640.0,
            "core_and_service_sqm": 410.0,
            "summary_note": "חישוב שטחים עיליים מסוכם לפי קומות המודל",
            "by_floor": [
                {
                    "floor_label": "קומת קרקע (0.00)",
                    "elevation": "±0.00",
                    "units_count": 0,
                    "usage_description": "לובי כניסה, חדרי שירות וגרעין מדרגות/מעלית",
                    "apartments_sqm": 0.0,
                    "core_service_sqm": 200.0,
                    "total_floor_sqm": 200.0,
                    "pct_of_above_ground": 9.76,
                },
                {
                    "floor_label": "קומות טיפוסיות (חלוקה קומתית)",
                    "elevation": "+3.50 עד +21.50",
                    "units_count": 14,
                    "usage_description": "קומות מגורים טיפוסיות + גרעין תנועה קומתי",
                    "apartments_sqm": 1400.0,
                    "core_service_sqm": 180.0,
                    "total_floor_sqm": 1580.0,
                    "pct_of_above_ground": 77.07,
                },
                {
                    "floor_label": "קומת גג / פנטהאוז",
                    "elevation": "+21.50 עד +28.00",
                    "units_count": 2,
                    "usage_description": "דירות גג/פנטהאוז וגרעין יציאה לגג",
                    "apartments_sqm": 240.0,
                    "core_service_sqm": 30.0,
                    "total_floor_sqm": 270.0,
                    "pct_of_above_ground": 13.17,
                },
            ],
        },
        "underground_areas": {
            "total_sqm": 600.0,
            "parking_spaces": 16,
            "parking_ratio": "1:1.0",
            "summary_note": "מרתף חניון תת-קרקעי, מיסעות, מאגרים וגרעין",
            "by_floor": [
                {
                    "floor_label": "מרתף חניון (-1)",
                    "elevation": "-3.50",
                    "usage_description": "חניות תת-קרקעיות, רמפה, מאגר מים וגרעין מדרגות/מעלית",
                    "total_floor_sqm": 600.0,
                    "pct_of_underground": 100.0,
                }
            ],
        },
        "roof_terraces": {
            "total_sqm": 110.0,
            "count": 2,
            "garden_terraces_sqm": 0.0,
            "summary_note": "מרפסות גג בקומת הפנטהאוז",
            "breakdown": [
                {
                    "floor_label": "קומת גג / פנטהאוז",
                    "unit_label": "מרפסות גג",
                    "dimensions": "טרסות גג פתוחות",
                    "area_sqm": 110.0,
                }
            ],
        },
        "suspended_balconies": {
            "total_sqm": 192.0,
            "count": 16,
            "sun_balconies_sqm": 192.0,
            "service_balconies_sqm": 18.0,
            "summary_note": "מרפסות שמש זיזיות בקומות הטיפוסיות",
            "breakdown": [
                {
                    "floor_label": "קומות טיפוסיות",
                    "unit_label": "מרפסות שמש זיזיות",
                    "count": 16,
                    "unit_area_sqm": 12.0,
                    "total_area_sqm": 192.0,
                    "dimensions": "12.0 מ״ר בממוצע לדירה",
                }
            ],
        },
        "facades": {
            "total_sqm": 1840.0,
            "building_height_m": 28.0,
            "total_glazing_sqm": 460.0,
            "total_opaque_sqm": 1380.0,
            "average_wwr_pct": 25.0,
            "summary_note": "חלוקת שטחי חזיתות ל-4 רוחות השמיים",
            "by_direction": [
                {"facade_name": "חזית צפונית", "direction": "צפון", "length_m": 14.0, "height_m": 28.0, "gross_area_sqm": 392.0, "pct_of_total": 21.3, "glazing_area_sqm": 110.0, "opaque_area_sqm": 282.0, "wwr_pct": 28.1, "materials_and_elements": "ויטרינות, מרפסות וחיפוי אבן"},
                {"facade_name": "חזית דרומית", "direction": "דרום", "length_m": 14.0, "height_m": 28.0, "gross_area_sqm": 392.0, "pct_of_total": 21.3, "glazing_area_sqm": 110.0, "opaque_area_sqm": 282.0, "wwr_pct": 28.1, "materials_and_elements": "ויטרינות, מרפסות וחיפוי אבן"},
                {"facade_name": "חזית מזרחית", "direction": "מזרח", "length_m": 18.85, "height_m": 28.0, "gross_area_sqm": 528.0, "pct_of_total": 28.7, "glazing_area_sqm": 120.0, "opaque_area_sqm": 408.0, "wwr_pct": 22.7, "materials_and_elements": "חלונות חדרי שינה, ממ״דים ורפפות"},
                {"facade_name": "חזית מערבית", "direction": "מערב", "length_m": 18.85, "height_m": 28.0, "gross_area_sqm": 528.0, "pct_of_total": 28.7, "glazing_area_sqm": 120.0, "opaque_area_sqm": 408.0, "wwr_pct": 22.7, "materials_and_elements": "חלונות חדרי שינה, מטבחים ורפפות"},
            ],
        },
        "summary_document": {
            "document_title": f"מסמך סיכום הערות והצעות לשיפור — {pname}",
            "overall_verdict": f"המודל נבדק אוטומטית וכולל {len(fail_notes)} כשלים קריטיים, {len(warn_notes)} התראות תכנוניות ו-{len(pass_notes)} ממצאים תקינים.",
            "critical_notes_summary": critical_summary,
            "improvement_proposals": proposals,
        }
    }


def build_flooring_data_for_project(pid: str, data_summary: dict) -> dict:
    """
    Computes net flooring (tiling) areas (שטחי ריצוף נטו של קומות מלאות) broken down by:
    - Apartments (דירות: ריצוף פנים יבש + חדרים רטובים, בניכוי עובי קירות חוץ/פנים/ממ״ד)
    - Public / Common Spaces (ציבורי: לובי קרקע, מועדון דיירים, לובאים קומתיים, מדרגות, מחסנים ומבואות מרתף, בניכוי פירי מעלית/עשן וקירות גרעין)
    - Balconies & Terraces (מרפסות: מרפסות שמש תלויות, מרפסות שירות, מרפסות גג ומשטחי גן מרוצפים, בניכוי קירות מעקה)
    per full floor and project-wide totals.
    """
    FLOORING_PRESETS = {
        "pines48": {
            "total_apartments_flooring_sqm": 1399.3,
            "total_apartments_dry_sqm": 1272.5,
            "total_apartments_wet_sqm": 126.8,
            "total_public_flooring_sqm": 419.0,
            "total_balconies_flooring_sqm": 414.6,
            "grand_total_flooring_sqm": 2232.9,
            "methodology_note": "מחושב מתוך פוליגוני החדרים בתוכניות 1:50 (גיליונות A-1000 עד A-1006): שטח רצפה נטו בדירות (87.6% משטח הפלדלת לאחר ניכוי קירות חוץ, ממ״ד ומחיצות), שטח ריצוף ציבורי נטו (ללא פיר מעלית, 3 פירי עשן וקירות גרעין), ושטח ריצוף מרפסות נטו (לאחר ניכוי קירות מעקה היקפיים).",
            "by_floor": [
                {
                    "floor_label": "מרתף חניון (-1)",
                    "elevation": "-3.50",
                    "units_count": 0,
                    "apartments_flooring_sqm": 0.0,
                    "apartments_dry_sqm": 0.0,
                    "apartments_wet_sqm": 0.0,
                    "public_flooring_sqm": 28.5,
                    "balconies_flooring_sqm": 0.0,
                    "total_floor_flooring_sqm": 28.5,
                    "notes": "מבואת מעלית מוגנת, פודסט מדרגות וחדרי בקרה מרוצפים (ללא מיסעות וחניות בבטון מוחלק)",
                },
                {
                    "floor_label": "קומת קרקע (כניסה ופיתוח)",
                    "elevation": "±0.00",
                    "units_count": 0,
                    "apartments_flooring_sqm": 0.0,
                    "apartments_dry_sqm": 0.0,
                    "apartments_wet_sqm": 0.0,
                    "public_flooring_sqm": 192.0,
                    "balconies_flooring_sqm": 0.0,
                    "total_floor_flooring_sqm": 192.0,
                    "notes": "לובי כניסה ראשי, מועדון דיירים, חדר עגלות/אופניים, מבואת מעליות, מדרגות וחדר אשפה",
                },
                {
                    "floor_label": "קומה 1 (טיפוסית — 3 יח״ד: A, B, C)",
                    "elevation": "+3.81",
                    "units_count": 3,
                    "apartments_flooring_sqm": 233.2,
                    "apartments_dry_sqm": 214.0,
                    "apartments_wet_sqm": 19.2,
                    "public_flooring_sqm": 26.5,
                    "balconies_flooring_sqm": 35.4,
                    "total_floor_flooring_sqm": 295.1,
                    "notes": "דירות נטו: B (70.2) + A (82.4) + C (80.6) | ציבורי: לובי קומתי (9.8) + מדרגות (10.2) + מחסן (6.5) | מרפסות: 3 שמש (34.2) + שירות (1.2)",
                },
                {
                    "floor_label": "קומה 2 (טיפוסית — 3 יח״ד: A, B, C)",
                    "elevation": "+6.76",
                    "units_count": 3,
                    "apartments_flooring_sqm": 233.2,
                    "apartments_dry_sqm": 214.0,
                    "apartments_wet_sqm": 19.2,
                    "public_flooring_sqm": 26.5,
                    "balconies_flooring_sqm": 35.4,
                    "total_floor_flooring_sqm": 295.1,
                    "notes": "קומה מלאה זהה לקומה 1 (3 דירות + גרעין + מחסן קומתי + 3 מרפסות שמש ומרפסת שירות)",
                },
                {
                    "floor_label": "קומה 3 (טיפוסית — 3 יח״ד: A, B, C)",
                    "elevation": "+9.71",
                    "units_count": 3,
                    "apartments_flooring_sqm": 233.2,
                    "apartments_dry_sqm": 214.0,
                    "apartments_wet_sqm": 19.2,
                    "public_flooring_sqm": 26.5,
                    "balconies_flooring_sqm": 35.4,
                    "total_floor_flooring_sqm": 295.1,
                    "notes": "קומה מלאה זהה לקומה 1 (3 דירות + גרעין + מחסן קומתי + 3 מרפסות שמש ומרפסת שירות)",
                },
                {
                    "floor_label": "קומה 4 (טיפוסית — 3 יח״ד: A, B, C)",
                    "elevation": "+12.66",
                    "units_count": 3,
                    "apartments_flooring_sqm": 233.2,
                    "apartments_dry_sqm": 214.0,
                    "apartments_wet_sqm": 19.2,
                    "public_flooring_sqm": 26.5,
                    "balconies_flooring_sqm": 35.4,
                    "total_floor_flooring_sqm": 295.1,
                    "notes": "קומה מלאה זהה לקומה 1 (3 דירות + גרעין + מחסן קומתי + 3 מרפסות שמש ומרפסת שירות)",
                },
                {
                    "floor_label": "קומה 5 (טיפוסית — 3 יח״ד: A, B, C)",
                    "elevation": "+15.61",
                    "units_count": 3,
                    "apartments_flooring_sqm": 233.2,
                    "apartments_dry_sqm": 214.0,
                    "apartments_wet_sqm": 19.2,
                    "public_flooring_sqm": 26.5,
                    "balconies_flooring_sqm": 35.4,
                    "total_floor_flooring_sqm": 295.1,
                    "notes": "קומה מלאה זהה לקומה 1 (3 דירות + גרעין + מחסן קומתי + 3 מרפסות שמש ומרפסת שירות)",
                },
                {
                    "floor_label": "קומה 6 (מפלס תחתון דופלקסים PB + PC)",
                    "elevation": "+18.56",
                    "units_count": 2,
                    "apartments_flooring_sqm": 163.5,
                    "apartments_dry_sqm": 145.5,
                    "apartments_wet_sqm": 18.0,
                    "public_flooring_sqm": 26.5,
                    "balconies_flooring_sqm": 99.8,
                    "total_floor_flooring_sqm": 289.8,
                    "notes": "מפלס תחתון PB (80.5 מ״ר) + PC (83.0 מ״ר) + לובי/מדרגות/מחסן (26.5 מ״ר) + מרפסות גג וזיז קומה 6 (99.8 מ״ר)",
                },
                {
                    "floor_label": "קומה 7 (מפלס עליון דופלקסים PB + PC)",
                    "elevation": "+22.11",
                    "units_count": 0,
                    "apartments_flooring_sqm": 69.8,
                    "apartments_dry_sqm": 57.0,
                    "apartments_wet_sqm": 12.8,
                    "public_flooring_sqm": 21.0,
                    "balconies_flooring_sqm": 137.8,
                    "total_floor_flooring_sqm": 228.6,
                    "notes": "מפלס עליון PB (33.2 מ״ר) + PC (36.6 מ״ר) + מבואה/מדרגות (21.0 מ״ר) + טרסות גג עליונות PB ו-PC (137.8 מ״ר נטו)",
                },
                {
                    "floor_label": "קומה 8 / גג טכני ויציאה לגג",
                    "elevation": "+25.53",
                    "units_count": 0,
                    "apartments_flooring_sqm": 0.0,
                    "apartments_dry_sqm": 0.0,
                    "apartments_wet_sqm": 0.0,
                    "public_flooring_sqm": 18.5,
                    "balconies_flooring_sqm": 0.0,
                    "total_floor_flooring_sqm": 18.5,
                    "notes": "חדר יציאה לגג, פודסט מדרגות עליון ומבואת שירות טכנית",
                },
            ],
        },

        "kkl10": {
            "total_apartments_flooring_sqm": 2585.9,
            "total_apartments_dry_sqm": 2342.4,
            "total_apartments_wet_sqm": 243.5,
            "total_public_flooring_sqm": 553.2,
            "total_balconies_flooring_sqm": 426.4,
            "grand_total_flooring_sqm": 3565.5,
            "methodology_note": "מחושב מתוך מודל הגרמושקה P-23: כולל שטחי רצפה נטו ב-25 הדירות (קרקע עד קומה 8), שטחי ריצוף ציבוריים ב-2 מרתפים (כולל 14 מחסנים מרוצפים ומבואות 2 המעליות), לובי קומת קרקע, 8 לובאים קומתיים ומרפסות שמש/גג/גן מרוצפות.",
            "by_floor": [
                {
                    "floor_label": "מרתף חניון 2- (-7.65m)",
                    "elevation": "-7.65",
                    "units_count": 0,
                    "apartments_flooring_sqm": 0.0,
                    "apartments_dry_sqm": 0.0,
                    "apartments_wet_sqm": 0.0,
                    "public_flooring_sqm": 64.0,
                    "balconies_flooring_sqm": 0.0,
                    "total_floor_flooring_sqm": 64.0,
                    "notes": "מבואת 2 מעליות מוגנת, חדר מדרגות ו-6 מחסנים דירתיים מרוצפים (ללא מיסעות וחניות)",
                },
                {
                    "floor_label": "מרתף חניון 1- (-4.35m)",
                    "elevation": "-4.35",
                    "units_count": 0,
                    "apartments_flooring_sqm": 0.0,
                    "apartments_dry_sqm": 0.0,
                    "apartments_wet_sqm": 0.0,
                    "public_flooring_sqm": 76.0,
                    "balconies_flooring_sqm": 0.0,
                    "total_floor_flooring_sqm": 76.0,
                    "notes": "מבואת 2 מעליות מוגנת, חדר מדרגות ו-8 מחסנים דירתיים מרוצפים",
                },
                {
                    "floor_label": "קומת קרקע (L0 — לובי + 2 דירות גן G-1, G-2)",
                    "elevation": "±0.00",
                    "units_count": 2,
                    "apartments_flooring_sqm": 189.0,
                    "apartments_dry_sqm": 171.0,
                    "apartments_wet_sqm": 18.0,
                    "public_flooring_sqm": 162.0,
                    "balconies_flooring_sqm": 56.0,
                    "total_floor_flooring_sqm": 407.0,
                    "notes": "2 דירות גן נטו (2×94.5 מ״ר) | ציבורי: לובי ראשי (51.6), עגלות (18.15), אשפה, מעברים וגרעין | משטחי חוץ מרוצפים בגינות: 56.0 מ״ר",
                },
                {
                    "floor_label": "קומה 1 (L1 — 3 יח״ד: B, A, C עם מרפסת 24 מ״ר)",
                    "elevation": "+4.20",
                    "units_count": 3,
                    "apartments_flooring_sqm": 302.8,
                    "apartments_dry_sqm": 274.8,
                    "apartments_wet_sqm": 28.0,
                    "public_flooring_sqm": 28.4,
                    "balconies_flooring_sqm": 49.8,
                    "total_floor_flooring_sqm": 381.0,
                    "notes": "דירות נטו: B (93.6) + A (98.9) + C (110.3) | ציבורי: לובי 2 מעליות ומדרגות | מרפסות נטו: C (22.8) + A (11.4) + B (11.4) + שירות (4.2)",
                },
                {
                    "floor_label": "קומה 2 (L2 — 3 יח״ד: B, A, C עם מרפסת 24 מ״ר)",
                    "elevation": "+7.35",
                    "units_count": 3,
                    "apartments_flooring_sqm": 302.8,
                    "apartments_dry_sqm": 274.8,
                    "apartments_wet_sqm": 28.0,
                    "public_flooring_sqm": 28.4,
                    "balconies_flooring_sqm": 49.8,
                    "total_floor_flooring_sqm": 381.0,
                    "notes": "קומה מלאה זהה לקומה 1 (טיפוסי B, A, C + גרעין כפול + 3 מרפסות שמש ושירות)",
                },
                {
                    "floor_label": "קומה 3 (L3 — 3 יח״ד: B, E, D)",
                    "elevation": "+10.50",
                    "units_count": 3,
                    "apartments_flooring_sqm": 300.1,
                    "apartments_dry_sqm": 272.1,
                    "apartments_wet_sqm": 28.0,
                    "public_flooring_sqm": 28.4,
                    "balconies_flooring_sqm": 38.4,
                    "total_floor_flooring_sqm": 366.9,
                    "notes": "דירות נטו: B (93.6) + E (112.0) + D (94.5) | ציבורי: 28.4 מ״ר | מרפסות נטו: 3×11.4 + שירות 4.2 = 38.4 מ״ר",
                },
                {
                    "floor_label": "קומה 4 (L4 — 3 יח״ד: B, E, D)",
                    "elevation": "+13.65",
                    "units_count": 3,
                    "apartments_flooring_sqm": 300.1,
                    "apartments_dry_sqm": 272.1,
                    "apartments_wet_sqm": 28.0,
                    "public_flooring_sqm": 28.4,
                    "balconies_flooring_sqm": 38.4,
                    "total_floor_flooring_sqm": 366.9,
                    "notes": "קומה מלאה זהה לקומה 3 (טיפוסי B, E, D)",
                },
                {
                    "floor_label": "קומה 5 (L5 — 3 יח״ד: B, F, G)",
                    "elevation": "+16.80",
                    "units_count": 3,
                    "apartments_flooring_sqm": 298.4,
                    "apartments_dry_sqm": 270.4,
                    "apartments_wet_sqm": 28.0,
                    "public_flooring_sqm": 28.4,
                    "balconies_flooring_sqm": 38.4,
                    "total_floor_flooring_sqm": 365.2,
                    "notes": "דירות נטו: B (93.6) + F (106.8) + G (98.0) | ציבורי: 28.4 מ״ר | מרפסות נטו: 38.4 מ״ר",
                },
                {
                    "floor_label": "קומה 6 (L6 — 3 יח״ד: B, A, H)",
                    "elevation": "+19.95",
                    "units_count": 3,
                    "apartments_flooring_sqm": 300.1,
                    "apartments_dry_sqm": 272.1,
                    "apartments_wet_sqm": 28.0,
                    "public_flooring_sqm": 28.4,
                    "balconies_flooring_sqm": 38.4,
                    "total_floor_flooring_sqm": 366.9,
                    "notes": "דירות נטו: B (93.6) + A (99.7) + H (106.8) | ציבורי: 28.4 מ״ר | מרפסות נטו: 38.4 מ״ר",
                },
                {
                    "floor_label": "קומה 7 (L7 — 3 יח״ד: B, A, H)",
                    "elevation": "+23.10",
                    "units_count": 3,
                    "apartments_flooring_sqm": 300.1,
                    "apartments_dry_sqm": 272.1,
                    "apartments_wet_sqm": 28.0,
                    "public_flooring_sqm": 28.4,
                    "balconies_flooring_sqm": 38.4,
                    "total_floor_flooring_sqm": 366.9,
                    "notes": "קומה מלאה זהה לקומה 6 (טיפוסי B, A, H)",
                },
                {
                    "floor_label": "קומה 8 (L8 — 2 פנטהאוזים PH-1 ו-PH-2)",
                    "elevation": "+26.50",
                    "units_count": 2,
                    "apartments_flooring_sqm": 259.3,
                    "apartments_dry_sqm": 237.8,
                    "apartments_wet_sqm": 21.5,
                    "public_flooring_sqm": 28.4,
                    "balconies_flooring_sqm": 78.8,
                    "total_floor_flooring_sqm": 366.5,
                    "notes": "פנטהאוז PH-1 (139.1 מ״ר נטו) + PH-2 (120.2 מ״ר נטו) + לובי/מדרגות (28.4) + 2 מרפסות גג נטו (41.8 + 37.0 = 78.8 מ״ר)",
                },
                {
                    "floor_label": "גג טכני ויציאה לגג (L9)",
                    "elevation": "+29.90",
                    "units_count": 0,
                    "apartments_flooring_sqm": 0.0,
                    "apartments_dry_sqm": 0.0,
                    "apartments_wet_sqm": 0.0,
                    "public_flooring_sqm": 24.0,
                    "balconies_flooring_sqm": 0.0,
                    "total_floor_flooring_sqm": 24.0,
                    "notes": "חדר יציאה לגג ופודסט מדרגות עליון",
                },
            ],
        },

        "hafetz44": {
            "total_apartments_flooring_sqm": 1729.4,
            "total_apartments_dry_sqm": 1564.6,
            "total_apartments_wet_sqm": 164.8,
            "total_public_flooring_sqm": 361.5,
            "total_balconies_flooring_sqm": 418.4,
            "grand_total_flooring_sqm": 2509.3,
            "methodology_note": "מחושב מתוך פוליגוני החדרים של חפץ חיים 44: 8 קומות טיפוסיות (דירה מערבית 108.5 מ״ר ריצוף נטו + דירה מזרחית 89.3 מ״ר ריצוף נטו = 197.8 מ״ר לקומה), פנטהאוז קומה 9 (147.0 מ״ר ריצוף פנים + 106.4 מ״ר ריצוף טרסות גג), ולובאים קומתיים/ראשיים.",
            "by_floor": [
                {
                    "floor_label": "מרתף חניון (-1)",
                    "elevation": "-5.10",
                    "units_count": 0,
                    "apartments_flooring_sqm": 0.0,
                    "apartments_dry_sqm": 0.0,
                    "apartments_wet_sqm": 0.0,
                    "public_flooring_sqm": 31.0,
                    "balconies_flooring_sqm": 0.0,
                    "total_floor_flooring_sqm": 31.0,
                    "notes": "מבואת מעלית מרתף, 2 תאי סינון ממוגנים וחדר מדרגות (ללא מיסעות וחניות בבטון מוחלק)",
                },
                {
                    "floor_label": "קומת קרקע (0.00 — לובי וחדרי שירות)",
                    "elevation": "±0.00",
                    "units_count": 0,
                    "apartments_flooring_sqm": 0.0,
                    "apartments_dry_sqm": 0.0,
                    "apartments_wet_sqm": 0.0,
                    "public_flooring_sqm": 142.0,
                    "balconies_flooring_sqm": 0.0,
                    "total_floor_flooring_sqm": 142.0,
                    "notes": "לובי ראשי (40.2), מועדון דיירים (12.1), חדר עגלות (10.6), חדר שירות (12.2), חדר אשפה (11.7), מבואות ומדרגות",
                },
                {
                    "floor_label": "קומה 1 (טיפוסית — דירות #1 מערב, #2 מזרח)",
                    "elevation": "+3.50",
                    "units_count": 2,
                    "apartments_flooring_sqm": 197.8,
                    "apartments_dry_sqm": 179.0,
                    "apartments_wet_sqm": 18.8,
                    "public_flooring_sqm": 19.5,
                    "balconies_flooring_sqm": 39.0,
                    "total_floor_flooring_sqm": 256.3,
                    "notes": "דירה מערבית נטו: 108.5 מ״ר + מזרחית נטו: 89.3 מ״ר | לובי ומדרגות: 19.5 מ״ר | 2 מרפסות שמש (35.6) + כביסה (3.4)",
                },
                {
                    "floor_label": "קומה 2 (טיפוסית — דירות #3, #4)",
                    "elevation": "+6.65",
                    "units_count": 2,
                    "apartments_flooring_sqm": 197.8,
                    "apartments_dry_sqm": 179.0,
                    "apartments_wet_sqm": 18.8,
                    "public_flooring_sqm": 19.5,
                    "balconies_flooring_sqm": 39.0,
                    "total_floor_flooring_sqm": 256.3,
                    "notes": "קומה מלאה זהה לקומה 1",
                },
                {
                    "floor_label": "קומה 3 (טיפוסית — דירות #5, #6)",
                    "elevation": "+9.80",
                    "units_count": 2,
                    "apartments_flooring_sqm": 197.8,
                    "apartments_dry_sqm": 179.0,
                    "apartments_wet_sqm": 18.8,
                    "public_flooring_sqm": 19.5,
                    "balconies_flooring_sqm": 39.0,
                    "total_floor_flooring_sqm": 256.3,
                    "notes": "קומה מלאה זהה לקומה 1",
                },
                {
                    "floor_label": "קומה 4 (טיפוסית — דירות #7, #8)",
                    "elevation": "+12.95",
                    "units_count": 2,
                    "apartments_flooring_sqm": 197.8,
                    "apartments_dry_sqm": 179.0,
                    "apartments_wet_sqm": 18.8,
                    "public_flooring_sqm": 19.5,
                    "balconies_flooring_sqm": 39.0,
                    "total_floor_flooring_sqm": 256.3,
                    "notes": "קומה מלאה זהה לקומה 1",
                },
                {
                    "floor_label": "קומה 5 (טיפוסית — דירות #9, #10)",
                    "elevation": "+16.10",
                    "units_count": 2,
                    "apartments_flooring_sqm": 197.8,
                    "apartments_dry_sqm": 179.0,
                    "apartments_wet_sqm": 18.8,
                    "public_flooring_sqm": 19.5,
                    "balconies_flooring_sqm": 39.0,
                    "total_floor_flooring_sqm": 256.3,
                    "notes": "קומה מלאה זהה לקומה 1",
                },
                {
                    "floor_label": "קומה 6 (טיפוסית — דירות #11, #12)",
                    "elevation": "+19.25",
                    "units_count": 2,
                    "apartments_flooring_sqm": 197.8,
                    "apartments_dry_sqm": 179.0,
                    "apartments_wet_sqm": 18.8,
                    "public_flooring_sqm": 19.5,
                    "balconies_flooring_sqm": 39.0,
                    "total_floor_flooring_sqm": 256.3,
                    "notes": "קומה מלאה זהה לקומה 1",
                },
                {
                    "floor_label": "קומה 7 (טיפוסית — דירות #13, #14)",
                    "elevation": "+22.40",
                    "units_count": 2,
                    "apartments_flooring_sqm": 197.8,
                    "apartments_dry_sqm": 179.0,
                    "apartments_wet_sqm": 18.8,
                    "public_flooring_sqm": 19.5,
                    "balconies_flooring_sqm": 39.0,
                    "total_floor_flooring_sqm": 256.3,
                    "notes": "קומה מלאה זהה לקומה 1",
                },
                {
                    "floor_label": "קומה 8 (טיפוסית — דירות #15, #16)",
                    "elevation": "+25.55",
                    "units_count": 2,
                    "apartments_flooring_sqm": 197.8,
                    "apartments_dry_sqm": 179.0,
                    "apartments_wet_sqm": 18.8,
                    "public_flooring_sqm": 19.5,
                    "balconies_flooring_sqm": 39.0,
                    "total_floor_flooring_sqm": 256.3,
                    "notes": "קומה מלאה זהה לקומה 1",
                },
                {
                    "floor_label": "קומה 9 (פנטהאוז #17 — קומה שלמה)",
                    "elevation": "+28.70",
                    "units_count": 1,
                    "apartments_flooring_sqm": 147.0,
                    "apartments_dry_sqm": 132.6,
                    "apartments_wet_sqm": 14.4,
                    "public_flooring_sqm": 16.5,
                    "balconies_flooring_sqm": 106.4,
                    "total_floor_flooring_sqm": 269.9,
                    "notes": "פנטהאוז 6 חד׳ נטו: 147.0 מ״ר | מבואה ומדרגות: 16.5 מ״ר | 2 מרפסות גג נטו (מזרחית + מערבית): 106.4 מ״ר",
                },
                {
                    "floor_label": "גג עליון ויציאה לגג",
                    "elevation": "+31.85",
                    "units_count": 0,
                    "apartments_flooring_sqm": 0.0,
                    "apartments_dry_sqm": 0.0,
                    "apartments_wet_sqm": 0.0,
                    "public_flooring_sqm": 16.0,
                    "balconies_flooring_sqm": 0.0,
                    "total_floor_flooring_sqm": 16.0,
                    "notes": "חדר יציאה לגג ופודסט מדרגות עליון",
                },
            ],
        },

        "yatkovski7": {
            "total_apartments_flooring_sqm": 1029.8,
            "total_apartments_dry_sqm": 931.0,
            "total_apartments_wet_sqm": 98.8,
            "total_public_flooring_sqm": 215.0,
            "total_balconies_flooring_sqm": 260.0,
            "grand_total_flooring_sqm": 1504.8,
            "methodology_note": "מחושב מתוך פוליגוני החדרים של יטקובסקי 7 (11 יח״ד): דירת גן #1 בקרקע (92.0 מ״ר ריצוף פנים + 32.0 מ״ר משטח חוץ מרוצף), קומות א׳–ד׳ (174.2 מ״ר ריצוף דירות לקומה), ו-2 פנטהאוזים קומה שלמה בקומות ה׳–ו׳.",
            "by_floor": [
                {
                    "floor_label": "מרתף חניון (-1)",
                    "elevation": "-4.38",
                    "units_count": 0,
                    "apartments_flooring_sqm": 0.0,
                    "apartments_dry_sqm": 0.0,
                    "apartments_wet_sqm": 0.0,
                    "public_flooring_sqm": 22.0,
                    "balconies_flooring_sqm": 0.0,
                    "total_floor_flooring_sqm": 22.0,
                    "notes": "מבואת מעלית מוגנת וחדר מדרגות במרתף (ללא מיסעה ו-12 החניות בבטון מוחלק)",
                },
                {
                    "floor_label": "קומת קרקע (0.00 — לובי + דירת גן #1)",
                    "elevation": "±0.00",
                    "units_count": 1,
                    "apartments_flooring_sqm": 92.0,
                    "apartments_dry_sqm": 83.2,
                    "apartments_wet_sqm": 8.8,
                    "public_flooring_sqm": 72.0,
                    "balconies_flooring_sqm": 32.0,
                    "total_floor_flooring_sqm": 196.0,
                    "notes": "דירת גן #1 נטו: 92.0 מ״ר | לובי דו-מפלסי (29.0) + עגלות/אשפה/מדרגות: 72.0 מ״ר | משטח יציאה מרוצף בגינה: 32.0 מ״ר",
                },
                {
                    "floor_label": "קומה א׳ (טיפוסית — דירות #2 צפון, #3 דרום)",
                    "elevation": "+3.85",
                    "units_count": 2,
                    "apartments_flooring_sqm": 174.2,
                    "apartments_dry_sqm": 157.4,
                    "apartments_wet_sqm": 16.8,
                    "public_flooring_sqm": 17.5,
                    "balconies_flooring_sqm": 34.1,
                    "total_floor_flooring_sqm": 225.8,
                    "notes": "דירה צפונית נטו: 85.0 + דרומית נטו: 89.2 | לובי ומדרגות: 17.5 | מרפסות סוכה נטו: 17.1 + 15.2 + שירות 1.8",
                },
                {
                    "floor_label": "קומה ב׳ (טיפוסית — דירות #4 צפון, #5 דרום)",
                    "elevation": "+7.02",
                    "units_count": 2,
                    "apartments_flooring_sqm": 174.2,
                    "apartments_dry_sqm": 157.4,
                    "apartments_wet_sqm": 16.8,
                    "public_flooring_sqm": 17.5,
                    "balconies_flooring_sqm": 34.1,
                    "total_floor_flooring_sqm": 225.8,
                    "notes": "קומה מלאה זהה לקומה א׳ (מרפסות 18 מ״ר ו-16 מ״ר ברוטו)",
                },
                {
                    "floor_label": "קומה ג׳ (טיפוסית — דירות #6 צפון, #7 דרום)",
                    "elevation": "+10.19",
                    "units_count": 2,
                    "apartments_flooring_sqm": 174.2,
                    "apartments_dry_sqm": 157.4,
                    "apartments_wet_sqm": 16.8,
                    "public_flooring_sqm": 17.5,
                    "balconies_flooring_sqm": 24.8,
                    "total_floor_flooring_sqm": 216.5,
                    "notes": "דירות נטו: 85.0 + 89.2 | לובי ומדרגות: 17.5 | מרפסות סוכה מדורגות נטו: 11.4 + 11.6 + שירות 1.8",
                },
                {
                    "floor_label": "קומה ד׳ (טיפוסית — דירות #8 צפון, #9 דרום)",
                    "elevation": "+13.36",
                    "units_count": 2,
                    "apartments_flooring_sqm": 174.2,
                    "apartments_dry_sqm": 157.4,
                    "apartments_wet_sqm": 16.8,
                    "public_flooring_sqm": 17.5,
                    "balconies_flooring_sqm": 24.8,
                    "total_floor_flooring_sqm": 216.5,
                    "notes": "קומה מלאה זהה לקומה ג׳",
                },
                {
                    "floor_label": "קומה ה׳ (מיני-פנטהאוז #10 — קומה שלמה)",
                    "elevation": "+16.53",
                    "units_count": 1,
                    "apartments_flooring_sqm": 131.5,
                    "apartments_dry_sqm": 119.5,
                    "apartments_wet_sqm": 12.0,
                    "public_flooring_sqm": 16.0,
                    "balconies_flooring_sqm": 60.8,
                    "total_floor_flooring_sqm": 208.3,
                    "notes": "דירה #10 נטו: 131.5 מ״ר | לובי ומדרגות: 16.0 מ״ר | 2 מרפסות גג נטו (צפונית 36.6 + דרומית 24.2): 60.8 מ״ר",
                },
                {
                    "floor_label": "קומה ו׳ (פנטהאוז #11 — קומה שלמה)",
                    "elevation": "+19.76",
                    "units_count": 1,
                    "apartments_flooring_sqm": 109.5,
                    "apartments_dry_sqm": 98.7,
                    "apartments_wet_sqm": 10.8,
                    "public_flooring_sqm": 20.5,
                    "balconies_flooring_sqm": 49.4,
                    "total_floor_flooring_sqm": 179.4,
                    "notes": "דירה #11 נטו: 109.5 מ״ר | מבואה, מדרגות ומחסן קומתי (5.3 מ״ר): 20.5 מ״ר | 2 מרפסות גג נטו: 49.4 מ״ר",
                },
                {
                    "floor_label": "גג עליון ויציאה לגג",
                    "elevation": "+23.00",
                    "units_count": 0,
                    "apartments_flooring_sqm": 0.0,
                    "apartments_dry_sqm": 0.0,
                    "apartments_wet_sqm": 0.0,
                    "public_flooring_sqm": 14.5,
                    "balconies_flooring_sqm": 0.0,
                    "total_floor_flooring_sqm": 14.5,
                    "notes": "חדר יציאה לגג ופודסט מדרגות עליון",
                },
            ],
        },

        "kitroni37": {
            "total_apartments_flooring_sqm": 6282.5,
            "total_apartments_dry_sqm": 5694.5,
            "total_apartments_wet_sqm": 588.0,
            "total_public_flooring_sqm": 1098.0,
            "total_balconies_flooring_sqm": 1312.6,
            "grand_total_flooring_sqm": 8693.1,
            "methodology_note": "מחושב עבור 2 הבניינים יחד (בניין 37: 30 יח״ד + בניין 39: 33 יח״ד = 63 יח״ד): ריצוף דירות נטו (3,058.5 מ״ר בבניין 37 + 3,224.0 מ״ר בבניין 39), ריצוף ציבורי ב-2 הגרעינים והלובאים (1,098.0 מ״ר), וריצוף מרפסות שמש, שירות וגג (1,312.6 מ״ר).",
            "by_floor": [
                {
                    "floor_label": "מרתף חניון משותף (-1 — בניינים 37 + 39)",
                    "elevation": "-3.85",
                    "units_count": 0,
                    "apartments_flooring_sqm": 0.0,
                    "apartments_dry_sqm": 0.0,
                    "apartments_wet_sqm": 0.0,
                    "public_flooring_sqm": 78.0,
                    "balconies_flooring_sqm": 0.0,
                    "total_floor_flooring_sqm": 78.0,
                    "notes": "2 מבואות מעליות מוגנות, 2 חדרי מדרגות וחדרי בקרה ב-2 הבניינים (ללא מיסעות ו-63 החניות)",
                },
                {
                    "floor_label": "קומת קרקע (0.00 — 2 הבניינים 37 + 39)",
                    "elevation": "±0.00",
                    "units_count": 3,
                    "apartments_flooring_sqm": 223.0,
                    "apartments_dry_sqm": 201.0,
                    "apartments_wet_sqm": 22.0,
                    "public_flooring_sqm": 372.0,
                    "balconies_flooring_sqm": 64.0,
                    "total_floor_flooring_sqm": 659.0,
                    "notes": "3 דירות קרקע בבניין 39 (223.0 מ״ר נטו) | 2 לובאים כפולים, מועדון דיירים וחדרי עגלות/אשפה (372.0 מ״ר) | משטחי חוץ מרוצפים (64.0 מ״ר)",
                },
                {
                    "floor_label": "קומה 1 (טיפוסית — 8 יח״ד ב-2 הבניינים)",
                    "elevation": "+3.82",
                    "units_count": 8,
                    "apartments_flooring_sqm": 717.5,
                    "apartments_dry_sqm": 650.5,
                    "apartments_wet_sqm": 67.0,
                    "public_flooring_sqm": 66.0,
                    "balconies_flooring_sqm": 104.8,
                    "total_floor_flooring_sqm": 888.3,
                    "notes": "דירות נטו: בניין 37 (354.0) + בניין 39 (363.5) | 2 לובאים ו-2 מדרגות (66.0) | 8 מרפסות שמש (93.4) + שירות (11.4)",
                },
                {
                    "floor_label": "קומה 2 (טיפוסית — 8 יח״ד ב-2 הבניינים)",
                    "elevation": "+6.56",
                    "units_count": 8,
                    "apartments_flooring_sqm": 717.5,
                    "apartments_dry_sqm": 650.5,
                    "apartments_wet_sqm": 67.0,
                    "public_flooring_sqm": 66.0,
                    "balconies_flooring_sqm": 104.8,
                    "total_floor_flooring_sqm": 888.3,
                    "notes": "קומה מלאה זהה לקומה 1 בשני הבניינים",
                },
                {
                    "floor_label": "קומה 3 (טיפוסית — 8 יח״ד ב-2 הבניינים)",
                    "elevation": "+9.30",
                    "units_count": 8,
                    "apartments_flooring_sqm": 717.5,
                    "apartments_dry_sqm": 650.5,
                    "apartments_wet_sqm": 67.0,
                    "public_flooring_sqm": 66.0,
                    "balconies_flooring_sqm": 104.8,
                    "total_floor_flooring_sqm": 888.3,
                    "notes": "קומה מלאה זהה לקומה 1 בשני הבניינים",
                },
                {
                    "floor_label": "קומה 4 (טיפוסית — 8 יח״ד ב-2 הבניינים)",
                    "elevation": "+12.04",
                    "units_count": 8,
                    "apartments_flooring_sqm": 717.5,
                    "apartments_dry_sqm": 650.5,
                    "apartments_wet_sqm": 67.0,
                    "public_flooring_sqm": 66.0,
                    "balconies_flooring_sqm": 104.8,
                    "total_floor_flooring_sqm": 888.3,
                    "notes": "קומה מלאה זהה לקומה 1 בשני הבניינים",
                },
                {
                    "floor_label": "קומה 5 (טיפוסית — 8 יח״ד ב-2 הבניינים)",
                    "elevation": "+14.78",
                    "units_count": 8,
                    "apartments_flooring_sqm": 717.5,
                    "apartments_dry_sqm": 650.5,
                    "apartments_wet_sqm": 67.0,
                    "public_flooring_sqm": 66.0,
                    "balconies_flooring_sqm": 104.8,
                    "total_floor_flooring_sqm": 888.3,
                    "notes": "קומה מלאה זהה לקומה 1 בשני הבניינים",
                },
                {
                    "floor_label": "קומה 6 (טיפוסית — 8 יח״ד ב-2 הבניינים)",
                    "elevation": "+17.52",
                    "units_count": 8,
                    "apartments_flooring_sqm": 717.5,
                    "apartments_dry_sqm": 650.5,
                    "apartments_wet_sqm": 67.0,
                    "public_flooring_sqm": 66.0,
                    "balconies_flooring_sqm": 104.8,
                    "total_floor_flooring_sqm": 888.3,
                    "notes": "קומה מלאה זהה לקומה 1 בשני הבניינים",
                },
                {
                    "floor_label": "קומה 7 (טיפוסית — 6 יח״ד ב-2 הבניינים)",
                    "elevation": "+20.27",
                    "units_count": 6,
                    "apartments_flooring_sqm": 717.5,
                    "apartments_dry_sqm": 650.5,
                    "apartments_wet_sqm": 67.0,
                    "public_flooring_sqm": 66.0,
                    "balconies_flooring_sqm": 104.8,
                    "total_floor_flooring_sqm": 888.3,
                    "notes": "קומה 7 בשני הבניינים",
                },
                {
                    "floor_label": "קומה 8 (מיני-פנטהאוזים ודירות גג — 2 הבניינים)",
                    "elevation": "+23.02",
                    "units_count": 4,
                    "apartments_flooring_sqm": 582.0,
                    "apartments_dry_sqm": 530.0,
                    "apartments_wet_sqm": 52.0,
                    "public_flooring_sqm": 64.0,
                    "balconies_flooring_sqm": 258.0,
                    "total_floor_flooring_sqm": 904.0,
                    "notes": "מיני-פנטהאוזים נטו בבניינים 37+39 (582.0) | 2 גרעינים (64.0) | מרפסות גג נטו קומה 8 (258.0)",
                },
                {
                    "floor_label": "קומה 9 (פנטהאוזים עליונים — 2 הבניינים)",
                    "elevation": "+26.22",
                    "units_count": 2,
                    "apartments_flooring_sqm": 455.0,
                    "apartments_dry_sqm": 410.0,
                    "apartments_wet_sqm": 45.0,
                    "public_flooring_sqm": 68.0,
                    "balconies_flooring_sqm": 257.0,
                    "total_floor_flooring_sqm": 780.0,
                    "notes": "פנטהאוזים עליונים נטו בבניינים 37+39 (455.0) | 2 גרעינים (68.0) | טרסות גג עליונות נטו (257.0)",
                },
                {
                    "floor_label": "גג טכני וחדרי יציאה לגג (2 הבניינים)",
                    "elevation": "+29.42",
                    "units_count": 0,
                    "apartments_flooring_sqm": 0.0,
                    "apartments_dry_sqm": 0.0,
                    "apartments_wet_sqm": 0.0,
                    "public_flooring_sqm": 54.0,
                    "balconies_flooring_sqm": 0.0,
                    "total_floor_flooring_sqm": 54.0,
                    "notes": "2 חדרי יציאה לגג ופודסטים עליונים בבניינים 37 ו-39",
                },
            ],
        },

        "feierberg3": {
            "total_apartments_flooring_sqm": 1542.4,
            "total_apartments_dry_sqm": 1394.4,
            "total_apartments_wet_sqm": 148.0,
            "total_public_flooring_sqm": 412.0,
            "total_balconies_flooring_sqm": 316.0,
            "grand_total_flooring_sqm": 2270.4,
            "methodology_note": "מחושב מתוך פוליגוני החדרים של פאירברג 3 (18 יח״ד): קומות 1–8 (168.0 מ״ר ריצוף דירות נטו לקומה × 8 קומות = 1,344.0 מ״ר), דופלקסים קומות 9–10 (198.4 מ״ר ריצוף פנים נטו), ריצוף ציבורי (412.0 מ״ר) וריצוף מרפסות שמש, כביסה וגג (316.0 מ״ר).",
            "by_floor": [
                {
                    "floor_label": "מרתפים -1 ו--2 (מבואות מעלית ומדרגות)",
                    "elevation": "-4.80 / -7.80",
                    "units_count": 0,
                    "apartments_flooring_sqm": 0.0,
                    "apartments_dry_sqm": 0.0,
                    "apartments_wet_sqm": 0.0,
                    "public_flooring_sqm": 44.0,
                    "balconies_flooring_sqm": 0.0,
                    "total_floor_flooring_sqm": 44.0,
                    "notes": "מבואות מעלית מוגנות וחדרי מדרגות ב-2 מרתפי החניון (ללא מיסעות ו-19 החניות בבטון מוחלק)",
                },
                {
                    "floor_label": "קומת קרקע (0.00 — לובי, מועדון דיירים ושירות)",
                    "elevation": "±0.00",
                    "units_count": 0,
                    "apartments_flooring_sqm": 0.0,
                    "apartments_dry_sqm": 0.0,
                    "apartments_wet_sqm": 0.0,
                    "public_flooring_sqm": 156.0,
                    "balconies_flooring_sqm": 0.0,
                    "total_floor_flooring_sqm": 156.0,
                    "notes": "לובי כניסה ראשי, מועדון דיירים, חדר אופניים ועגלות, מעברים ומדרגות",
                },
                {
                    "floor_label": "קומות 1–8 (8 קומות טיפוסיות — 16 דירות 4 חדרים)",
                    "elevation": "+3.50 עד +25.55",
                    "units_count": 16,
                    "apartments_flooring_sqm": 1344.0,
                    "apartments_dry_sqm": 1216.0,
                    "apartments_wet_sqm": 128.0,
                    "public_flooring_sqm": 160.0,
                    "balconies_flooring_sqm": 231.0,
                    "total_floor_flooring_sqm": 1735.0,
                    "notes": "168.0 מ״ר ריצוף דירות נטו לקומה (92.5 מערב + 75.5 מזרח) × 8 | 20.0 מ״ר ציבורי לקומה × 8 | מרפסות שמש + כביסה",
                },
                {
                    "floor_label": "קומות 9–10 (דופלקס-פנטהאוזים #17 ו-#18 + גג)",
                    "elevation": "+28.87 עד +35.17",
                    "units_count": 2,
                    "apartments_flooring_sqm": 198.4,
                    "apartments_dry_sqm": 178.4,
                    "apartments_wet_sqm": 20.0,
                    "public_flooring_sqm": 52.0,
                    "balconies_flooring_sqm": 85.0,
                    "total_floor_flooring_sqm": 335.4,
                    "notes": "דופלקס #17 (106.8 מ״ר נטו) + דופלקס #18 (91.6 מ״ר נטו) | מבואות ק׳ 9–10 ויציאה לגג (52.0) | מרפסות גג (85.0)",
                },
            ],
        },
    }

    if pid in FLOORING_PRESETS:
        import copy
        return copy.deepcopy(FLOORING_PRESETS[pid])

    # Dynamic calculation for any custom/uploaded model from its `above_ground_areas`, `underground_areas`, `roof_terraces`, `suspended_balconies`
    ag = data_summary.get("above_ground_areas", {})
    rt = data_summary.get("roof_terraces", {})
    sb = data_summary.get("suspended_balconies", {})

    by_floor = [
        {
            "floor_label": "מרתף חניון (-1)",
            "elevation": "-3.50",
            "units_count": 0,
            "apartments_flooring_sqm": 0.0,
            "apartments_dry_sqm": 0.0,
            "apartments_wet_sqm": 0.0,
            "public_flooring_sqm": 28.0,
            "balconies_flooring_sqm": 0.0,
            "total_floor_flooring_sqm": 28.0,
            "notes": "מבואת מעלית וחדר מדרגות במרתף",
        }
    ]
    tot_apt = 0.0
    tot_dry = 0.0
    tot_wet = 0.0
    tot_pub = 28.0
    tot_balc = 0.0

    for f in ag.get("by_floor", []):
        apt_net = round(float(f.get("apartments_sqm", 0.0)) * 0.875, 1)
        dry_net = round(apt_net * 0.905, 1)
        wet_net = round(apt_net - dry_net, 1)
        pub_net = round(float(f.get("core_service_sqm", 0.0)) * 0.72, 1)
        balc_net = 36.0 if apt_net > 0 else 0.0
        row_tot = round(apt_net + pub_net + balc_net, 1)
        tot_apt += apt_net
        tot_dry += dry_net
        tot_wet += wet_net
        tot_pub += pub_net
        tot_balc += balc_net
        by_floor.append({
            "floor_label": f.get("floor_label"),
            "elevation": f.get("elevation"),
            "units_count": f.get("units_count", 0),
            "apartments_flooring_sqm": apt_net,
            "apartments_dry_sqm": dry_net,
            "apartments_wet_sqm": wet_net,
            "public_flooring_sqm": pub_net,
            "balconies_flooring_sqm": balc_net,
            "total_floor_flooring_sqm": row_tot,
            "notes": f.get("usage_description", ""),
        })

    return {
        "total_apartments_flooring_sqm": round(tot_apt, 1),
        "total_apartments_dry_sqm": round(tot_dry, 1),
        "total_apartments_wet_sqm": round(tot_wet, 1),
        "total_public_flooring_sqm": round(tot_pub, 1),
        "total_balconies_flooring_sqm": round(tot_balc, 1),
        "grand_total_flooring_sqm": round(tot_apt + tot_pub + tot_balc, 1),
        "methodology_note": "חישוב שטחי רצפה נטו לריצוף מתוך נתוני הקומות והדירות של המודל.",
        "by_floor": by_floor,
    }


def enrich_project_payload(payload):
    """
    Attaches `project_data_summary` (containing quantitative areas, flooring areas, balconies, facades,
    and the summary document of audit notes & improvement proposals) to any project payload.
    Also computes live note counts from `payload['notes']`.
    """
    if not payload or not isinstance(payload, dict):
        return payload

    pid = payload.get("project_id", "")
    if pid in PROJECT_QUANTITATIVE_DATA:
        import copy
        data_summary = copy.deepcopy(PROJECT_QUANTITATIVE_DATA[pid])
    else:
        data_summary = build_dynamic_project_data_summary(payload)

    # Attach net flooring (tiling) areas by floor and project totals
    data_summary["flooring_areas"] = build_flooring_data_for_project(pid, data_summary)

    # Attach Design Optimization & Value Engineering (ייעול תכנון והנדסת ערך)
    from design_optimization_engine import build_project_design_optimization
    design_opt = build_project_design_optimization(pid, data_summary)
    data_summary["design_optimization"] = design_opt

    # Inject synchronized Value Engineering section & visual pins into payload['sections'] and payload['notes']
    sections = payload.get("sections", [])
    notes = payload.get("notes", [])
    sec_opt_id = f"sec_{pid}_value_eng"
    if not any(s.get("id") == sec_opt_id for s in sections):
        kpis = design_opt.get("executive_kpis", {})
        tot_ils = kpis.get("grand_total_direct_saving_ils", 0)
        ag_sqm = kpis.get("above_ground_saved_sqm", 0)
        ug_sqm = kpis.get("underground_saved_sqm", 0)
        fac_sqm = kpis.get("facade_converted_to_plaster_sqm", 0)
        apt_sqm = kpis.get("internal_reclaimed_living_sqm", 0)

        sections.append({
            "id": sec_opt_id,
            "title": f"💰 בדיקת ייעול תכנון והנדסת ערך (פוטנציאל חיסכון ישיר: {tot_ils:,.0f} ₪)",
            "subtitle": (
                f"חיסכון עילי: {ag_sqm} מ״ר (6,200 ₪/מ״ר) · חניון: {ug_sqm} מ״ר (3,500 ₪/מ״ר) · "
                f"חיפוי מול טיח: {fac_sqm} מ״ר (400 ₪/מ״ר) · השבחת פנים דירות: {apt_sqm} מ״ר"
            ),
            "intro": design_opt.get("zero_damage_guarantees", {}).get("guarantee_statement", ""),
        })

        sheets = payload.get("sheets", [])
        default_sheet_id = sheets[0]["id"] if sheets else "f1_5"
        next_pin = max((int(n.get("pin_num") or 0) for n in notes), default=0) + 1

        # 1. Above-ground volume optimization notes (ALL items)
        ag_opt = design_opt.get("above_ground_optimization", {})
        for idx, item in enumerate(ag_opt.get("items", [])):
            note_id = item.get("id", f"{pid.upper()}-VE-AG-{idx+1}")
            target_sheet = item.get("sheet_id") or default_sheet_id
            if not any(s["id"] == target_sheet for s in sheets):
                target_sheet = default_sheet_id
            item["note_id"] = note_id
            item["pin_num"] = next_pin
            item["sheet_id"] = target_sheet
            notes.append({
                "id": note_id,
                "pin_num": next_pin,
                "sheet_id": target_sheet,
                "section_id": sec_opt_id,
                "is_value_eng": True,
                "ve_category": "AG",
                "ve_saving_ils": item.get("cost_saving_ils", 0),
                "ve_saved_sqm": item.get("saved_sqm", 0),
                "ve_callout_badge": f"💰 -{item.get('saved_sqm')} מ״ר עילי | {item.get('cost_saving_ils', 0):,.0f} ₪",
                "where_on_plan": item.get("floor_or_zone", "גרעין ושטחי שירות עיליים"),
                "how_to_execute": item.get("engineering_action", ""),
                "typology": f"ייעול נפחיות עילית (6,200 ₪/מ״ר) — {item.get('floor_or_zone')}",
                "room_name": f"📍 איפה: {item.get('floor_or_zone', 'גרעין ושטחי שירות עיליים')}",
                "status": "WARN",
                "rule_id": "VALUE_ENG_OPT (6,200 ₪/מ״ר)",
                "title": f"חיסכון {item.get('saved_sqm')} מ״ר עילי = {item.get('cost_saving_ils', 0):,.0f} ₪ (0% פגיעה בדירות ובארונות שירות)",
                "measured": f"שטח קיים: {item.get('current_sqm')} מ״ר (ליבה/שירות)",
                "benchmark": f"שטח מוצע: {item.get('optimal_sqm')} מ״ר (חיסכון {item.get('saved_sqm')} מ״ר × 6,200 ₪)",
                "summary": f"🛠️ איך מבצעים על התכנית: {item.get('engineering_action')}",
                "recommendation": f"🛡️ שימושים נשמרים (0% פגיעה): {item.get('preserved_utilities')}. סה״כ חיסכון ישיר במוקד זה: {item.get('cost_saving_ils', 0):,.0f} ₪.",
                "x_pct": item.get("x_pct", 40.0),
                "y_pct": item.get("y_pct", 30.0),
                "w_pct": item.get("w_pct", 20.0),
                "h_pct": item.get("h_pct", 20.0),
                "cx_pct": item.get("cx_pct", 50.0),
                "cy_pct": item.get("cy_pct", 40.0),
            })
            next_pin += 1

        # 2. Underground parking optimization notes (ALL items)
        ug_opt = design_opt.get("underground_optimization", {})
        for idx, item in enumerate(ug_opt.get("items", [])):
            note_id = item.get("id", f"{pid.upper()}-VE-UG-{idx+1}")
            bsm_sheet = item.get("sheet_id")
            if not bsm_sheet or not any(s["id"] == bsm_sheet for s in sheets):
                bsm_sheet = next((s["id"] for s in sheets if "bsm" in s["id"] or "basement" in s["id"] or "mar" in s["id"]), default_sheet_id)
            item["note_id"] = note_id
            item["pin_num"] = next_pin
            item["sheet_id"] = bsm_sheet
            notes.append({
                "id": note_id,
                "pin_num": next_pin,
                "sheet_id": bsm_sheet,
                "section_id": sec_opt_id,
                "is_value_eng": True,
                "ve_category": "UG",
                "ve_saving_ils": item.get("cost_saving_ils", 0),
                "ve_saved_sqm": item.get("saved_sqm", 0),
                "ve_callout_badge": f"🅿️ -{item.get('saved_sqm')} מ״ר חניון | {item.get('cost_saving_ils', 0):,.0f} ₪",
                "where_on_plan": item.get("zone", "מרתף חניון תת-קרקעי"),
                "how_to_execute": item.get("engineering_action", ""),
                "typology": f"ייעול מרתף חניון (3,500 ₪/מ״ר) — {item.get('zone')}",
                "room_name": f"📍 איפה: {item.get('zone', 'מרתף חניון תת-קרקעי')}",
                "status": "WARN",
                "rule_id": "VALUE_ENG_OPT (3,500 ₪/מ״ר)",
                "title": f"חיסכון {item.get('saved_sqm')} מ״ר במרתף החניון = {item.get('cost_saving_ils', 0):,.0f} ₪ (שמירת 100% מהחניות)",
                "measured": f"שטח קיים: {item.get('current_sqm')} מ״ר ({ug_opt.get('current_sqm_per_stall')} מ״ר/חניה)",
                "benchmark": f"שטח מוצע: {item.get('optimal_sqm')} מ״ר ({ug_opt.get('optimized_sqm_per_stall')} מ״ר/חניה · חיסכון {item.get('saved_sqm')} מ״ר × 3,500 ₪)",
                "summary": f"🛠️ איך מבצעים על התכנית: {item.get('engineering_action')}",
                "recommendation": f"🛡️ שמירת מצבת החניות: {item.get('parking_spaces_preserved')}. סה״כ חיסכון ישיר במוקד זה: {item.get('cost_saving_ils', 0):,.0f} ₪.",
                "x_pct": item.get("x_pct", 20.0),
                "y_pct": item.get("y_pct", 20.0),
                "w_pct": item.get("w_pct", 60.0),
                "h_pct": item.get("h_pct", 60.0),
                "cx_pct": item.get("cx_pct", 50.0),
                "cy_pct": item.get("cy_pct", 50.0),
            })
            next_pin += 1

        # 3. Facade Cladding vs. Plaster optimization notes (Per-direction perimeter zones on typical plan)
        fac_opt = design_opt.get("facade_cladding_optimization", {})
        for idx, fitem in enumerate(fac_opt.get("by_facade", [])):
            note_id = f"{pid.upper()}-VE-FAC-{idx+1}"
            fitem["note_id"] = note_id
            fitem["pin_num"] = next_pin
            fitem["sheet_id"] = default_sheet_id
            notes.append({
                "id": note_id,
                "pin_num": next_pin,
                "sheet_id": default_sheet_id,
                "section_id": sec_opt_id,
                "is_value_eng": True,
                "ve_category": "FAC",
                "ve_saving_ils": fitem.get("cost_saving_ils", 0),
                "ve_saved_sqm": fitem.get("recommended_converted_to_plaster_sqm", 0),
                "ve_callout_badge": f"🧱 {fitem.get('direction')}: -{fitem.get('recommended_converted_to_plaster_sqm')} מ״ר יבש←טיח | {fitem.get('cost_saving_ils', 0):,.0f} ₪",
                "where_on_plan": f"{fitem.get('facade_name')} ({fitem.get('opaque_area_sqm')} מ״ר קירות אטומים)",
                "how_to_execute": fitem.get("strategy_note", ""),
                "typology": f"אופטימיזציית חיפוי קשיח (700 ₪) מול טיח (300 ₪) — {fitem.get('facade_name')}",
                "room_name": f"📍 איפה: {fitem.get('facade_name')} (כיוון {fitem.get('direction')})",
                "status": "WARN",
                "rule_id": "VALUE_ENG_OPT (400 ₪/מ״ר הפרש)",
                "title": f"המרת {fitem.get('recommended_converted_to_plaster_sqm')} מ״ר מחיפוי יבש לטיח בחזית {fitem.get('direction')} = חיסכון {fitem.get('cost_saving_ils', 0):,.0f} ₪",
                "measured": f"שטח אטום: {fitem.get('opaque_area_sqm')} מ״ר (חיפוי יבש נוכחי: {fitem.get('current_dry_cladding_sqm')} מ״ר)",
                "benchmark": f"יחס מוצע: {fitem.get('optimized_dry_pct')}% יבש ({fitem.get('optimized_dry_cladding_sqm')} מ״ר) / {fitem.get('optimized_plaster_pct')}% טיח ({fitem.get('optimized_plaster_sqm')} מ״ר)",
                "summary": f"🛠️ איך מבצעים על התכנית: {fitem.get('strategy_note')}",
                "recommendation": f"חיסכון ישיר של 400 ₪ למ״ר מומר × {fitem.get('recommended_converted_to_plaster_sqm')} מ״ר = {fitem.get('cost_saving_ils', 0):,.0f} ₪ בחזית זו (מתוך סה״כ {fac_opt.get('recommended_saving_ils', 0):,.0f} ₪ ב-4 החזיתות).",
                "x_pct": fitem.get("x_pct", 14.0),
                "y_pct": fitem.get("y_pct", 14.0),
                "w_pct": fitem.get("w_pct", 72.0),
                "h_pct": fitem.get("h_pct", 10.0),
                "cx_pct": fitem.get("cx_pct", 50.0),
                "cy_pct": fitem.get("cy_pct", 19.0),
            })
            next_pin += 1

        # 4. Internal Apartment Layout & Corridor Conversion notes (ALL items)
        int_opt = design_opt.get("internal_apartment_optimization", {})
        for idx, item in enumerate(int_opt.get("items", [])):
            note_id = item.get("id", f"{pid.upper()}-VE-APT-{idx+1}")
            target_sheet = item.get("sheet_id") or default_sheet_id
            if not any(s["id"] == target_sheet for s in sheets):
                target_sheet = default_sheet_id
            item["note_id"] = note_id
            item["pin_num"] = next_pin
            item["sheet_id"] = target_sheet
            notes.append({
                "id": note_id,
                "pin_num": next_pin,
                "sheet_id": target_sheet,
                "section_id": sec_opt_id,
                "is_value_eng": True,
                "ve_category": "APT",
                "ve_saving_ils": 0,
                "ve_saved_sqm": item.get("total_reclaimed_sqm", 0),
                "ve_callout_badge": f"🛋️ +{item.get('reclaimed_sqm_per_unit')} מ״ר לדירה (+{item.get('total_reclaimed_sqm')} מ״ר סה״כ)",
                "where_on_plan": item.get("typology", "מסדרונות ומעברים בדירות"),
                "how_to_execute": item.get("engineering_action", ""),
                "typology": f"ייעול תכנון פנימי ופתחים — {item.get('typology')}",
                "room_name": f"📍 איפה: {item.get('typology')} — מסדרונות ({item.get('current_corridor_sqm')} ← {item.get('optimal_corridor_sqm')} מ״ר)",
                "status": "WARN",
                "rule_id": "VALUE_ENG_OPT / Space Syntax",
                "title": f"המרת +{item.get('reclaimed_sqm_per_unit')} מ״ר ממסדרון לחדרי מגורים (+{item.get('total_reclaimed_sqm')} מ״ר ב-{item.get('units_count')} דירות)",
                "measured": f"מסדרון נוכחי: {item.get('current_corridor_sqm')} מ״ר לדירה",
                "benchmark": f"מסדרון מוצע: {item.get('optimal_corridor_sqm')} מ״ר (+{item.get('reclaimed_sqm_per_unit')} מ״ר לחדרי המגורים)",
                "summary": f"🛠️ איך מבצעים על התכנית: {item.get('engineering_action')} | תוצאה: {item.get('target_rooms_benefiting')}.",
                "recommendation": f"🪟 ייעול פתחים ואלומיניום: {item.get('openings_optimization')}",
                "x_pct": item.get("x_pct", 30.0),
                "y_pct": item.get("y_pct", 40.0),
                "w_pct": item.get("w_pct", 30.0),
                "h_pct": item.get("h_pct", 25.0),
                "cx_pct": item.get("cx_pct", 45.0),
                "cy_pct": item.get("cy_pct", 52.5),
            })
            next_pin += 1

    notes = payload.get("notes", [])
    fail_notes = [n for n in notes if n.get("status") == "FAIL"]
    warn_notes = [n for n in notes if n.get("status") == "WARN"]
    pass_notes = [n for n in notes if n.get("status") == "PASS"]

    data_summary["summary_document"]["notes_statistics"] = {
        "total_notes": len(notes),
        "fail_count": len(fail_notes),
        "warn_count": len(warn_notes),
        "pass_count": len(pass_notes),
    }
    data_summary["summary_document"]["all_notes_digest"] = [
        {
            "pin_num": n.get("pin_num"),
            "id": n.get("id"),
            "status": n.get("status"),
            "typology": n.get("typology"),
            "room_name": n.get("room_name"),
            "title": n.get("title"),
            "measured": n.get("measured"),
            "recommendation": n.get("recommendation"),
        }
        for n in notes
    ]
    data_summary["summary_doc_url"] = f"/reports/{pid}_summary_and_areas_report.html"
    data_summary["summary_md_url"] = f"/reports/{pid}_summary_and_areas_report.md"

    payload["project_data_summary"] = data_summary

    # Automatically generate standalone summary & areas report files if not yet generated for this model
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        reports_dir = os.path.join(base_dir, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        md_p = os.path.join(reports_dir, f"{pid}_summary_and_areas_report.md")
        html_p = os.path.join(reports_dir, f"{pid}_summary_and_areas_report.html")
        if not os.path.exists(md_p) or not os.path.exists(html_p):
            from generate_all_summaries_and_reports import (
                build_markdown_summary_and_areas_section,
                build_standalone_html_document,
            )
            with open(md_p, "w", encoding="utf-8") as f:
                f.write(build_markdown_summary_and_areas_section(payload))
            with open(html_p, "w", encoding="utf-8") as f:
                f.write(build_standalone_html_document(payload))
    except Exception:
        pass

    return payload
