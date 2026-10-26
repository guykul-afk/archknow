---
category: International Housing Quality Benchmarks
indicator: Dwelling Space, Storage, Outdoor Space & Liveability Benchmarks (NDSS / London Plan / NSW ADG / Swiss WBS)
rule_id: WBS_NDSS_ADG
type: standard_compendium
engine_usage: validation_engine.run_advanced_checks
verification_status: NDSS, London Plan D6 and ADG values transcribed from the published documents (2015 / 2021 / 2015 editions). WBS described structurally only (no point values).
ndss_gia_single_storey_sqm:
  1b1p: 39
  1b2p: 50
  2b3p: 61
  2b4p: 70
  3b4p: 74
  3b5p: 86
  3b6p: 95
  4b5p: 90
  4b6p: 99
  4b7p: 108
  4b8p: 117
  5b6p: 103
  5b7p: 112
  5b8p: 121
  6b7p: 116
  6b8p: 125
ndss_storage_sqm:
  1: 1.5
  2: 2.0
  3: 2.5
  4: 3.0
  5: 3.5
  6: 4.0
ndss_single_bedroom_min_sqm: 7.5
ndss_single_bedroom_min_width_m: 2.15
ndss_double_bedroom_min_sqm: 11.5
ndss_main_double_min_width_m: 2.75
ndss_other_double_min_width_m: 2.55
ndss_min_ceiling_m: 2.3
london_min_ceiling_m: 2.5
london_outdoor_base_sqm: 5.0
london_outdoor_per_extra_person_sqm: 1.0
london_outdoor_min_depth_m: 1.5
adg_min_apartment_sqm:
  0: 35
  1: 50
  2: 70
  3: 90
adg_extra_bathroom_sqm: 5
adg_extra_bedroom_sqm: 12
adg_master_bedroom_min_sqm: 10
adg_other_bedroom_min_sqm: 9
adg_bedroom_min_dimension_m: 3.0
adg_living_min_width_small_m: 3.6
adg_living_min_width_large_m: 4.0
adg_habitable_ceiling_m: 2.7
adg_window_to_floor_min_ratio: 0.10
adg_room_depth_to_ceiling_max: 2.5
adg_open_plan_max_depth_m: 8.0
adg_balcony_min:
  0: [4, 0.0]
  1: [8, 2.0]
  2: [10, 2.0]
  3: [12, 2.4]
adg_storage_m3:
  0: 4
  1: 6
  2: 8
  3: 10
adg_storage_inside_min_share: 0.5
adg_cross_vent_min_share: 0.60
adg_sunlight_min_share: 0.70
---
# מדדי שטח, אחסון ואיכות חיים בינלאומיים לדירות מגורים
## NDSS (בריטניה) · London Plan D6 · NSW ADG (אוסטרליה) · WBS (שווייץ)

> **מטרת הקובץ**: להוסיף לבסיס הידע רף **מצוינות** בינלאומי מעבר לרף **החוקי** הישראלי (`ISRAEL_2026`, `B1.*`).
> המנוע מסמן חריגה מרף זה כ-`WARN` (לא `FAIL`), כי מדובר בתקנים זרים ולא בחוק המחייב בישראל.

---

## 1. NDSS — Technical Housing Standards: Nationally Described Space Standard
**מקור**: Department for Communities and Local Government (DCLG), *Technical housing standards – nationally described space standard*, March 2015 (עודכן 2016).

### 1.1 שטח פנים ברוטו מינימלי (GIA) — דירה חד-מפלסית
השטח נמדד **בתוך קירות החוץ, כולל מחיצות פנימיות** (Gross Internal Area). לכן כאשר המנוע מסכם רק את שטחי החדרים נטו, ההשוואה **שמרנית**: אם הדירה עוברת על בסיס סכום החדרים, היא בוודאי עוברת על בסיס GIA.

| חדרי שינה (b) / מיטות (p) | GIA מינ' (מ"ר) | אחסון מובנה מינ' (מ"ר) |
| :--- | :---: | :---: |
| 1b1p | 39 (37 עם מקלחון במקום אמבטיה) | 1.0 |
| 1b2p | 50 | 1.5 |
| 2b3p / 2b4p | 61 / 70 | 2.0 |
| 3b4p / 3b5p / 3b6p | 74 / 86 / 95 | 2.5 |
| 4b5p / 4b6p / 4b7p / 4b8p | 90 / 99 / 108 / 117 | 3.0 |
| 5b6p / 5b7p / 5b8p | 103 / 112 / 121 | 3.5 |
| 6b7p / 6b8p | 116 / 125 | 4.0 |

### 1.2 חדרי שינה
- **חדר יחיד (1 מיטה)**: שטח ≥ **7.5 מ"ר**, רוחב ≥ **2.15 מ'**.
- **חדר זוגי (2 מיטות)**: שטח ≥ **11.5 מ"ר**; חדר הזוגי **הראשון** ברוחב ≥ **2.75 מ'**, וכל חדר זוגי נוסף ≥ **2.55 מ'**.
- ארון מובנה בחדר שינה נכלל בשטח החדר (עד 0.72 מ"ר לחדר יחיד) ונספר גם בשטח האחסון.

### 1.3 גובה
- גובה תקרה ≥ **2.30 מ'** לפחות ב-75% משטח ה-GIA. שטח שגובהו < 1.50 מ' אינו נספר ב-GIA.

### 1.4 התאמה לישראל (מיפוי המנוע)
- **ממ"ד** נספר כחדר שינה (כנהוג בישראל), אלא אם הוגדר אחרת בשדה `bedrooms` של הדירה.
- **מספר מיטות** (`bedspaces`) — אם לא הוזן: חדר ≥ 11.5 מ"ר = 2 מיטות, אחרת = 1 מיטה.

---

## 2. London Plan 2021 — Policy D6 (Housing quality and standards)
**מקור**: Greater London Authority, *The London Plan 2021*, Policy D6; *Housing Design Standards LPG* (2023).

- **גובה תקרה** ≥ **2.50 מ'** לפחות ב-75% משטח הדירה (מחמיר מ-NDSS).
- **שטח חוץ פרטי** (מרפסת/גינה): ≥ **5 מ"ר** לדירת 1–2 נפשות, ועוד **1 מ"ר** לכל נפש נוספת; עומק ורוחב מינימליים **1.50 מ'**.
- **כיווניות**: יש למקסם דירות דו-כיווניות (Dual Aspect). דירה חד-כיוונית תאושר רק כחריג, ו**לעולם לא כשהיא פונה לצפון** (בחצי הכדור הצפוני — רלוונטי ישירות לישראל), חשופה לרעש חריג, או מכילה 3 חדרי שינה ומעלה.

---

## 3. NSW Apartment Design Guide (ADG) — Part 4: Designing the Building
**מקור**: NSW Department of Planning and Environment, *Apartment Design Guide*, July 2015 (מוטמע ב-SEPP 65 / Housing SEPP).
> חלק מהערכים כבר מופיעים ב-[CHECKLIST_ISRAEL_INT](checklist_israel_international_integration.md); כאן הם מנורמלים לשימוש אלגוריתמי.

| סעיף | נושא | ערך מספרי |
| :--- | :--- | :--- |
| 4A | שמש ישירה | ≥ 70% מהדירות מקבלות ≥ 2 שעות שמש ישירה בסלון ובמרפסת בין 9:00–15:00 ביום הקצר בשנה; ≤ 15% ללא שמש ישירה כלל |
| 4B | אוורור צולב | ≥ 60% מהדירות ב-9 הקומות הראשונות מאווררות באוורור צולב טבעי; עומק דירה "חוצה" ≤ 18 מ' (זכוכית לזכוכית) |
| 4C | גובה תקרה | ≥ 2.70 מ' בחדרים עיקריים; ≥ 2.40 מ' בחדרי שירות |
| 4D-1 | שטח דירה מינ' | סטודיו 35 · 1 ח"ש 50 · 2 ח"ש 70 · 3 ח"ש 90 מ"ר (כולל חדר רחצה אחד; +5 מ"ר לכל חדר רחצה נוסף; +12 מ"ר לכל ח"ש נוסף מעבר ל-3) |
| 4D-1 | חלונות | לכל חדר עיקרי חלון חיצוני בשטח זיגוג ≥ 10% משטח הרצפה |
| 4D-2 | עומק חדר | עומק חדר עיקרי ≤ 2.5 × גובה התקרה; בחלל פתוח (סלון-מטבח) — המטבח ≤ 8 מ' מחלון |
| 4D-3 | חדרי שינה | חדר הורים ≥ 10 מ"ר, חדרים אחרים ≥ 9 מ"ר (ללא ארון); מידה מינימלית ≥ 3.0 מ' (ללא ארון) |
| 4D-3 | סלון | רוחב ≥ 3.6 מ' (סטודיו / 1 ח"ש), ≥ 4.0 מ' (2–3 ח"ש) |
| 4E | מרפסת עיקרית | 1 ח"ש: 8 מ"ר / עומק 2.0 מ' · 2 ח"ש: 10 מ"ר / 2.0 מ' · 3+ ח"ש: 12 מ"ר / 2.4 מ' (סטודיו: 4 מ"ר) |
| 4G | אחסון | סטודיו 4 · 1 ח"ש 6 · 2 ח"ש 8 · 3+ ח"ש 10 מ"ק; לפחות 50% בתוך הדירה |

---

## 4. WBS — Wohnungs-Bewertungs-System (שווייץ)
**מקור**: Bundesamt für Wohnungswesen (BWO), *Wohnbauten planen, beurteilen und vergleichen – Wohnungs-Bewertungs-System WBS*, מהדורת 2015 (המהדורה הראשונה פורסמה ב-1975 והתעדכנה מאז מספר פעמים).

**מבנה השיטה** (ללא ערכי ניקוד — אלה דורשים את נוסח המקור):
- הערכת **"ערך השימוש"** (*Gebrauchswert*) של הדירה בשלוש רמות: **מיקום** (*Wohnstandort*), **מתחם/בניין** (*Wohnanlage*) ו**דירה** (*Wohnung*).
- ברמת הדירה הקריטריונים עוסקים, בין השאר, ב:
  1. **יכולת ריהוט** (*Möblierbarkeit*) — האם כל חדר מאפשר יותר מסידור ריהוט אחד (תלוי באורך קירות רציפים ובמיקום הפתחים).
  2. **רב-שימושיות החדרים** (*Nutzungsneutralität*) — האם חדרים בגודל דומה ניתנים להחלפת תפקיד (שינה / עבודה / משחק).
  3. **קשרים בין חללים** — מטבח ↔ פינת אוכל ↔ סלון ↔ מרפסת.
  4. **שטח חוץ פרטי**, **אחסון**, **אור יום** ו**פרטיות**.
- **ערך לבסיס הידע**: WBS הוא המקור המובהק לעיקרון שחדר "טוב" אינו רק חדר שעומד במינימום, אלא חדר **שאינו כופה סידור ריהוט יחיד**. המנוע מממש עיקרון זה בעקיפין דרך מדד המלבניות (`SPACE_SYNTAX_SAGA`).

> [!NOTE]
> הוספת ערכי הניקוד המלאים של WBS דורשת את מסמך ה-PDF הרשמי של ה-BWO. הנושא רשום ב-[SOURCES_REGISTRY](sources_registry_architectural_quality.md) כמקור "לרכישה/השלמה".

---

## 5. איך המנוע משתמש בקובץ (`validation_engine.run_advanced_checks`)
| בדיקה | קלט נדרש בקובץ הדירה | פלט |
| :--- | :--- | :--- |
| שטח דירה מול NDSS ו-ADG | `rooms[].area_sqm` (או `net_area_sqm`) | `WARN` אם מתחת לרף |
| רוחב ושטח חדרי שינה | `rooms[].width_cm`, `area_sqm` | `WARN` מתחת ל-NDSS, `WARN` מתחת ל-ADG בלבד |
| רוחב סלון | `rooms[].width_cm` | `WARN` מתחת ל-3.6 / 4.0 מ' |
| גובה תקרה מצוין | `global_parameters.ceiling_height_m` | `WARN` מתחת ל-2.70 מ' |
| יחס חלון/רצפה | `rooms[].window_area_sqm` | `WARN` מתחת ל-10% |
| עומק חדר | `rooms[].depth_m` | `WARN` מעל 2.5 × גובה תקרה |
| מרפסת | חדר `balcony` עם `area_sqm`, `depth_m` | `WARN` מול ADG / London / Alexander |
| אחסון | `storage.built_in_sqm` / `storage.volume_m3` / חדרי `storage` | `WARN` אם חסר או אין נתון |
| כיווניות | `orientations` (למשל `["N","E"]`) | `WARN` לחד-כיוונית / חד-כיוונית צפונית |
