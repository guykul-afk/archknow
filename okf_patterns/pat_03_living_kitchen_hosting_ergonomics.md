---
okf_type: design_refactoring_pattern
pattern_id: PAT_LIVING_KITCHEN_HOSTING_AXIS
title_he: אופטימיזציית ציר סלון–מטבח–מרפסת, מעבר אי NKBA וחיץ אקוסטי (Living-Kitchen Axis)
category: LIVING_KITCHEN_ERGONOMICS
target_zone: public_living_kitchen_zone
required_wall_mutability:
  - FLEXIBLE_DRY_PARTITION
  - EXTERIOR_VITRINE_BOUNDARY
hard_guardrails:
  - living_min_statutory_width_m: 2.60
  - living_target_adg_width_m: 4.00
  - kitchen_island_aisle_min_cm: 115
  - kitchen_island_aisle_target_cm: 120
  - continuous_prep_counter_min_cm: 110
  - shared_bedroom_wall_acoustic_min_db: 48
  - balcony_vitrine_threshold_max_cm: 1.5
---
# PAT_LIVING_KITCHEN_HOSTING_AXIS: אופטימיזציית ציר האירוח סלון–מטבח–מרפסת

## תנאי הפעלה טופולוגי (Trigger Condition)
מופעל בחלל הציבורי של הדירה (סלון, פינת אוכל, מטבח ומרפסת שמש) לשיפור הארגונומיה, קווי הראייה ואירוח 10–12 סועדים.

## טרנספורמציית הגרף המרחבי (Graph Transformation)
1. **NKBA-13 Island Aisle & Work Triangle**: הצבת האי במרחק 120 ס"מ מחזית הארונות (לפתיחת מדיח ומעבר מקביל), שמירת סכום צלעות משולש עבודה בטווח 4.0–7.9 מ', ויצירת משטח הכנה רציף של 115 ס"מ בין כיור לכיריים.
2. **Hosting Table & Sightline Alignment**: יישור ציר שולחן האוכל בהמשך לאי ובניצב לוויטרינת המרפסת (מאפשר פתיחה ל-3.00 מ' עבור 12 סועדים ללא חסימת היציאה למרפסת) ויישור קיר המדיה לרוחב ≥3.80 מ'.
3. **Acoustic & VRF Integration**: שדרוג הקיר המשותף בין הסלון/מטבח לחדר השינה הצמוד לבלוק אקוסטי 15 ס"מ (≥48 dB לפי ת"י 1004), מסילת Zero-Threshold למרפסת, וריכוז הנמכת מיזוג VRF במסדרון.
