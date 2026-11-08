---
okf_type: design_refactoring_pattern
pattern_id: PAT_CORE_FLUSH_GENKAN
title_he: השקעת ארונות מונים בגרעין וסיפוח מבואת סף כניסה לדירה (Flush Core & Genkan)
category: TYPICAL_FLOOR_EFFICIENCY
target_zone: core_to_apartment_boundary
required_wall_mutability:
  - SEMI_RIGID_CORE_BOUNDARY
forbidden_wall_mutability:
  - LOCKED_MAMAD_WALL
  - LOCKED_SHEAR_CORE
hard_guardrails:
  - mamad_vertical_continuity_min_pct: 70.0
  - stair_flight_min_width_m: 1.10
  - elevator_landing_min_depth_m: 1.50
  - preserve_lobby_natural_window: true
expected_yield_sqm_per_floor_range: [2.6, 5.2]
---
# PAT_CORE_FLUSH_GENKAN: השקעת ארונות מונים בגרעין וסיפוח גומחת סף הכניסה לדירה

## תנאי הפעלה טופולוגי (Trigger Condition)
מופעל בקומה טיפוסית שבה יחס שטח הגרעין והציבורי עולה על 12% משטח הקומה ברוטו, או כאשר קיימות גומחות מבואה חיצוניות לפני דלתות הפלדלת וארונות מונים הבולטים לתוך שטח המעבר.

## טרנספורמציית הגרף המרחבי (Graph Transformation)
1. **Flush Utility Integration**: העברת ארונות חשמל, מים, תקשורת וכיבוי אש למישור קיר המעטפת החיצוני של חדר המדרגות ופיר המעלית (עומק השקעה 25–30 ס"מ).
2. **Threshold Re-indexing (Genkan)**: קידום מישור דלת הפלדלת של הדירה ב-45–60 ס"מ אל קו קיר הלובי הקומתי, כך שגומחת הכניסה החיצונית הופכת למבואת כניסה פרטית (`Genkan`) בתוך שטח הפלדלת של הדירה, תוך שמירה על חלון הלובי הקומתי ועל מרווח 1.50 מ' מול המעלית.
