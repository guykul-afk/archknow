---
okf_type: design_refactoring_pattern
pattern_id: PAT_FENESTRATION_WWR_SKU
title_he: אופטימיזציית מפתחי חלונות (WFR/WWR), כיס חלון ממ״ד ואיחוד מק״טי אלומיניום
category: FENESTRATION_AND_ENVELOPE
target_zone: building_envelope_and_openings
hard_guardrails:
  - statutory_room_wfr_min_pct: 8.0
  - daylight_en17037_wfr_target_pct: 12.0
  - building_wwr_thermal_target_pct_range: [18.0, 25.0]
  - street_facade_acoustic_glazing_min_db: 38
  - kitchen_window_sill_min_cm: 105
  - bedroom_window_lintel_target_cm: 225
---
# PAT_FENESTRATION_WWR_SKU: אופטימיזציית מפתחי חלונות ואיחוד מק״טי אלומיניום

## תנאי הפעלה טופולוגי (Trigger Condition)
מופעל בבקרת פתחי החוץ של הדירות והחזיתות כאשר יחס החלון לרצפה (`WFR`) בחלל מגורים עולה על 30% (סיכון תרמי/סנוור), או מתחת ל-12% (תת-תאורה טבעית), או כאשר קיימת שונות גבוהה במידות החלונות בין הקומות.

## טרנספורמציית הגרף המרחבי (Graph Transformation)
1. **Thermal & Daylight Balancing**: בוויטרינות עם `WFR > 30%` בחזיתות מערב/דרום — הגדרת זיגוג בידודית `Low-E` (`SHGC ≤ 0.36`) והצללה חיצונית; בחדרי שינה — הגבהת משקוף עליון ל-225 ס"מ להגדלת עומק חדירת האור הטבעי ב-25%.
2. **Functional Hardware Ergonomics**: בממ"ד — חלון הדף פלדה וחלון אלומיניום דו-כנפי נגררים לכיס מלא (תיקון 163, ללא כנף ציר פנימית); במטבח — סף תחתון בגובה 105 ס"מ מעל השיש ופתיחת הזזה/דריי-קיפ מעל גובה הברז.
3. **Aluminum SKU Consolidation**: איחוד רוחבי חלונות חדרי השינה ל-2 מק"טים מודולריים אחידים לאורך הקומות (חיסכון 8%–10% בעלות חבילת האלומיניום).
