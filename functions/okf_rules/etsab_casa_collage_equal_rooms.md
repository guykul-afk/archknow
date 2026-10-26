---
category: Academic Housing Typology
subcategory: ETSAB Barcelona Habitar — Non-Hierarchical Generic Rooms
description_summary: ETSAB Barcelona (Xavier Monteys & Pere Fuertes, Casa Collage) and MAIO (Anna Puigjaner) equal-sized generic rooms (~12.5-14 sqm, 3.60x3.60m), low bedroom size variance (<=1.25), and equipped storage walls.
indicator: Casa Collage Non-Hierarchical Rooms & Equipped Walls
rule_id: ETSAB_CC_1
type: architectural_rule
check_type: room_hierarchy_balance
target_room: bedroom
engine_usage: validation_engine.run_advanced_checks
etsab_generic_room_min_sqm: 12.5
etsab_generic_room_target_width_m: 3.60
etsab_room_size_variance_max_ratio: 1.25
etsab_equipped_wall_min_depth_cm: 60
---
# ETSAB_CC_1: ETSAB Barcelona (*Habitar*) & MAIO — *Casa Collage* וחדרים גנריים שווי-גודל

## מקור אקדמי
- Xavier Monteys & Pere Fuertes (ETSAB / UPC Barcelona), *Casa Collage: Un ensayo sobre la arquitectura de la casa* (Gustavo Gili).
- Anna Puigjaner (MAIO Architects / ETH Zürich / Columbia GSAPP), *110 Rooms Housing, Barcelona*.

## עקרונות ומדדים לניתוח תכנוני
1. **שוויון חדרים ואי-היררכיה (*La casa de habitaciones iguales*)**:
   - יחס השטח בין חדר השינה הגדול ביותר לחדר השינה הקטן ביותר בדירה: $\le \mathbf{1.25:1}$.
   - שטח חדר גנרי רב-שימושי: $\ge \mathbf{12.5\text{ m}^2}$ במודול ריבועי/כמעט-ריבועי של $\mathbf{3.60 \times 3.60\text{ m}}$.
   - מאפשר החלפת תפקודים לאורך חיי המשפחה (חדר הורים $\leftrightarrow$ חדר לשני ילדים $\leftrightarrow$ סטודיו עבודה $\leftrightarrow$ חדר מגורים שני).
2. **קירות מרוהטים (*Paredes Equipadas*)**:
   - ריכוז ארונות ומערכות ברצועות אחסון בעומק $\ge \mathbf{60\text{ cm}}$ המשמשות כחיץ אקוסטי בין החדרים הגנריים.
