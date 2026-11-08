---
okf_type: design_refactoring_pattern
pattern_id: PAT_ZERO_LINE_CLOSET_CORRIDOR
title_he: קיצור פרוזדור דירתי ושילוב נישות ארונות בקו אפס (Zero-Line Closet Reclamation)
category: INTERNAL_APARTMENT_YIELD
target_zone: apartment_corridor_and_bedrooms
required_wall_mutability:
  - FLEXIBLE_DRY_PARTITION
forbidden_wall_mutability:
  - WET_PLUMBING_WALL
  - LOCKED_MAMAD_WALL
  - LOCKED_SHEAR_CORE
hard_guardrails:
  - closet_niche_clear_depth_cm: 62
  - corridor_min_clear_width_cm: 100
  - bathroom_door_front_clearance_min_cm: 95
  - bedroom_vestibule_door_spacing_min_cm: 110
expected_yield_sqm_per_unit_range: [1.2, 2.2]
---
# PAT_ZERO_LINE_CLOSET_CORRIDOR: קיצור פרוזדור דירתי ונישות ארונות בקו אפס

## תנאי הפעלה טופולוגי (Trigger Condition)
מופעל כאשר שטח הפרוזדור הפנימי בדירה עולה על 8% משטח הדירה נטו, או כאשר קצה הפרוזדור מוביל לדלת חדר שינה קצה שניתן לפתוח מציר המבואה.

## טרנספורמציית הגרף המרחבי (Graph Transformation)
1. **Corridor Tail Reclamation**: קידום דלת הכניסה של חדר השינה/סוויטת ההורים בקצה הפרוזדור ב-90–110 ס"מ וסיפוח שטח המעבר לחדר השינה (בכפוף לשמירת מרווח ≥95 ס"מ מול דלת חדר הרחצה ומבואה ≥110 ס"מ בין דלתות).
2. **Zero-Line Dry Wall Recess**: יצירת מדרגת מחיצה ("זיגזג") בעומק נטו של 62 ס"מ במחיצות יבשות בלבד (`FLEXIBLE_DRY_PARTITION`) לטובת ארון בגדים אינטגרלי בקו אפס עם הקיר — לעולם לא על חשבון קיר חדר רחצה (`WET_PLUMBING_WALL`) או קיר בטון.
