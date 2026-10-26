---
category: Israeli Statutory & Regulatory Standards
subcategory: IS 1004 Acoustics in Residential Buildings & IS 1142 Railings and Balustrades
description_summary: Israeli Standard IS 1004 (residential acoustic insulation >= 48 dB airborne sound on party walls/stairs) and IS 1142 (balcony railing height >= 105 cm, stairs >= 90 cm, max opening gap <= 10 cm, anti-climbing rule).
indicator: Israeli Standards IS 1004 (Acoustics) & IS 1142 (Railings Safety)
rule_id: IL_IS1004_1142
type: architectural_rule
check_type: safety_and_acoustics
target_room: apartment
engine_usage: validation_engine.run_advanced_checks
is1004_party_wall_airborne_min_db: 48
is1004_green_building_recommended_db: 50
is1142_balcony_railing_min_height_cm: 105
is1142_stairs_railing_min_height_cm: 90
is1142_railing_max_gap_cm: 10
---
# IL_IS1004_1142: ת"י 1004 (בידוד אקוסטי בבנייני מגורים) ות"י 1142 (מעקים ומסעדים)

## מקורות סטטוטוריים
- מכון התקנים הישראלי, *ת"י 1004 חלקים 1–4: אקוסטיקה בבנייני מגורים*.
- מכון התקנים הישראלי, *ת"י 1142: מעקים ומסעדים*.

## 1. ת"י 1004 — בידוד אקוסטי
- **קיר מפריד בין שתי דירות או בין דירה לחדר מדרגות/מעלית**: בידוד מרעש נישא באוויר $D_{nT,w} + C \ge \mathbf{48\text{ dB}}$ (ובת"י 5281 בנייה ירוקה מומלץ $\ge \mathbf{50\text{–}52\text{ dB}}$).
- **הפרדת חדרי שינה מפיר מעלית / חדרי מכונות**: הימנעות מהצמדת קיר חדר שינה לפיר מעלית או צינור שפכים אנכי ללא הפרדה אקוסטית כפולה.

## 2. ת"י 1142 — בטיחות מעקים ומסעדים
- **גובה מעקה במרפסת, גג, חלון נמוך או מפלס עם סכנת נפילה**: $\ge \mathbf{105\text{ cm}}$ ממפלס הדריכה האפשרי הגבוה ביותר.
- **גובה מעקה/מסעד לאורך שיפוע מדרגות**: $\ge \mathbf{90\text{ cm}}$ (ובפודסט/מישור $\ge 105\text{ cm}$).
- **מרווח נטו מקסימלי במעקה**: $\le \mathbf{10\text{ cm}}$ (כדור בקוטר $10\text{ cm}$ לא יעבור), ואיסור על אלמנטים אופקיים המאפשרים טיפוס ילדים בין גובה $10\text{ cm}$ ל-$90\text{ cm}$.
