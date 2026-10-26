---
category: Israeli Statutory & Regulatory Standards
subcategory: Ministry of Transport (MoT) — Parking Lot Design Guidelines
description_summary: Israeli Ministry of Transport (Misrad HaTachbura) Parking Lot Design Guidelines (Part D) — open stall width >= 2.40m, adjacent to 1 column/wall >= 2.65-2.90m, between 2 columns/walls >= 2.90-3.00m, 90-deg aisle width >= 5.50-6.00m, accessible parking >= 3.70/4.50m.
indicator: Israeli Ministry of Transport Parking Stall, Column Clearance & Aisle Standards
rule_id: IL_MOT_PARK
type: architectural_rule
check_type: parking_geometry
target_room: parking
engine_usage: validation_engine.run_advanced_checks
mot_parking_stall_open_min_width_m: 2.40
mot_parking_stall_single_column_min_width_m: 2.65
mot_parking_stall_between_columns_min_width_m: 2.90
mot_parking_stall_min_length_m: 5.00
mot_parking_aisle_90deg_min_width_m: 5.50
mot_parking_aisle_90deg_recommended_width_m: 6.00
mot_parking_accessible_car_min_width_m: 3.70
mot_parking_accessible_van_min_width_m: 4.50
---
# IL_MOT_PARK: הנחיות משרד התחבורה לתכנון חניונים (פרק ד') וחניית נכים

## מקור רשמי
- משרד התחבורה והבטיחות בדרכים, *הנחיות לתכנון חניה — פרק ד': תכנון חניונים* + ת"י 1918 חלק 2.

## דרישות גאומטריות לתאי חניה ומיסעות (רמת שירות 1 — מגורים)
1. **רוחב תא חניה בניצב ($90^\circ$) ואורכו**:
   - **תא חניה חופשי (ללא עמודים או קירות צמודים)**: רוחב $\ge \mathbf{2.40\text{ m}}$, אורך $\ge \mathbf{5.00\text{ m}}$.
   - **תא חניה הצמוד לעמוד או קיר מצד אחד**: חובה להוסיף מרווח פתיחת דלת $\leftarrow$ רוחב $\ge \mathbf{2.65\text{–}2.90\text{ m}}$.
   - **תא חניה הכלוא בין שני עמודים או שני קירות**: רוחב $\ge \mathbf{2.90\text{–}3.00\text{ m}}$.
2. **רוחב מיסעה (דרך נסיעה ותמרון לחניה בניצב $90^\circ$)**:
   - מינימום תקני: $\ge \mathbf{5.50\text{ m}}$; מומלץ לתמרון נוח ברמת שירות 1: $\mathbf{6.00\text{ m}}$.
3. **חניית נכים (ת"י 1918 חלק 2)**:
   - רכב רגיל: $\ge \mathbf{3.70\text{ m}}$ ($2.40\text{ m}$ תא + $1.30\text{ m}$ מעבר צד).
   - רכב גבוה (וואן עם מעלון): $\ge \mathbf{4.50\text{ m}}$ וגובה חופשי $\ge \mathbf{2.45\text{ m}}$.
