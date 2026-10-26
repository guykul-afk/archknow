---
category: Environmental Quality, Daylight & Natural Ventilation
indicator: Daylight, View Out, Natural Ventilation, Overheating Risk, IAQ & Biophilic Design (EN 17037 / BR 209 / CIBSE AM10 & TM59 / WELL v2 / ASHRAE 62.2 / IS 5281 / Biophilia)
rule_id: DAYLIGHT_VENT_IEQ
type: standard_compendium
engine_usage: validation_engine.run_advanced_checks
verification_status: Numerical values transcribed from EN 17037:2018+A1:2021, BRE BR 209 (2022), CIBSE AM10 (2005) & TM59 (2017/2026), ASHRAE 62.2, WELL v2 (Light & Air), Israeli Standard IS 5281 technical guides, and Terrapin 14 Patterns of Biophilic Design.
en17037_view_angle_min_deg: 14
en17037_view_angle_med_deg: 28
en17037_view_angle_high_deg: 54
en17037_view_dist_min_m: 6.0
en17037_view_dist_med_m: 20.0
en17037_view_dist_high_m: 50.0
en17037_view_layers_min: 1
en17037_view_layers_med: 2
en17037_view_layers_high: 3
en17037_sunlight_min_hours: 1.5
en17037_sunlight_med_hours: 3.0
en17037_sunlight_high_hours: 4.0
br209_no_sky_line_min_share: 0.80
br209_obstruction_angle_max_deg: 25.0
cibse_single_sided_single_open_depth_to_height: 2.0
cibse_single_sided_dual_open_depth_to_height: 2.5
cibse_cross_vent_max_depth_to_height: 5.0
cibse_openable_window_to_floor_min_ratio: 0.05
tm59_west_unshaded_glazing_warn_ratio: 0.25
well_window_access_max_m: 7.5
well_circadian_optimal_m: 4.5
---
# תאורה טבעית, מבט החוצה, אוורור טבעי ואיכות סביבה פנים (IEQ)
## EN 17037 · BRE BR 209 · CIBSE AM10 & TM59 · WELL v2 · ASHRAE 62.2 · ת"י 5281 · 14 תבניות ביופיליות

> **מטרת הקובץ**: להרחיב את בדיקת האור, האוויר והסביבה מעבר ליחס החלון/רצפה הבסיסי (8%–10% בתקנות ישראל וב-ADG) אל מדדי **איכות מבט**, **עומק אוורור אפקטיבי**, **סיכון להתחממות יתר וסנוור**, **תאורה צירקדית** ו**ביופיליה**.

---

## 1. EN 17037 — אור יום בבניינים (Daylight in Buildings)
**מקור**: CEN, *EN 17037:2018+A1:2021 — Daylight in buildings*.

התקן האירופי מעריך ארבעה ממדים של אור יום בחללי שהייה:

### 1.1 אספקת אור יום (Daylight Provision)
בדיקה שבפני משטח הייחוס (בגובה $0.85\text{ m}$ מעל הרצפה) מתקבלת עוצמת הארה מינימלית במשך 50% משעות אור היום בשנה:
- **רמת מינימום**: $\ge 300\text{ lux}$ על פני 50% משטח החדר, ו-$\ge 100\text{ lux}$ על פני 95% משטח החדר (בחללי מגורים ניתן לתרגם למקדם אור יום $DF \ge 1.5\%\text{–}2.0\%$ בהתאם לקו הרוחב).
- **רמה בינונית / גבוהה**: $\ge 500\text{ lux}$ / $\ge 750\text{ lux}$ על פני 50% מהשטח.

### 1.2 איכות המבט החוצה (View Out)
חלון אינו רק מקור תאורה אלא חיבור פסיכולוגי לסביבה. האיכות נמדדת מנקודת הישיבה של הדייר לפי שלושה פרמטרים:

| רמת איכות (EN 17037) | זווית מבט אופקית ($\theta$) | מרחק מבט החוצה עד מכשול ($d$) | שכבות נוף נראות (שמיים / נוף-אופק / קרקע) |
| :--- | :---: | :---: | :--- |
| **מינימום (Minimum)** | $\ge 14^\circ$ | $\ge 6.0\text{ m}$ | לפחות שכבה 1 (לרוב נוף או שמיים) |
| **בינונית (Medium)** | $\ge 28^\circ$ | $\ge 20.0\text{ m}$ | לפחות 2 שכבות |
| **גבוהה (High)** | $\ge 54^\circ$ | $\ge 50.0\text{ m}$ | כל 3 השכבות (שמיים + אופק/בניינים/צמחייה + קרקע) |

### 1.3 חשיפה לשמש ישירה (Exposure to Sunlight)
לפחות חדר מגורים עיקרי אחד בדירה (סלון או חדר שינה/ילדים) צריך לקבל שמש ישירה ביום הייחוס (21 במרץ / 1 בפברואר לפי נספח לאומי):
- **מינימום**: $\ge 1.5$ שעות שמש ישירה.
- **בינוני**: $\ge 3.0$ שעות.
- **גבוה**: $\ge 4.0$ שעות.

### 1.4 מניעת סנוור (Protection from Glare)
הסתברות סנוור אור יום (*Daylight Glare Probability — DGP*) לא תעלה על $0.45$ (מינימום), $0.40$ (בינוני), או $0.35$ (גבוה). בישראל, חזיתות דרומיות, מזרחיות ומערביות מחייבות אמצעי הצללה חיצוניים או דינמיים (תריסים/רפפות/מצחיות).

---

## 2. BRE BR 209 — תכנון העמדה, קו השמיים והצללה
**מקור**: Paul Littlefair, *Site Layout Planning for Daylight and Sunlight: A Guide to Good Practice* (BRE Report BR 209, 3rd ed., 2022).

- **חוק $25^\circ$ (Obstruction Angle)**: אם זווית ההסתרה האנכית ממרכז החלון הנמוך ביותר אל ראש הבניין שממול היא $\le 25^\circ$, מובטח פוטנציאל טוב לאור יום. מעל $25^\circ$ נדרשת בדיקה מפורטת.
- **No-Sky Line (NSL / אי-ראיית שמיים)**: לפחות **80% משטח החדר** (בגובה משטח העבודה) צריכים לקבל אור ישיר מהשמיים. אם מעל 20% מעומק החדר נמצאים מאחורי קו ה-NSL, החלק האחורי של החדר ייראה קודר וידרוש תאורה מלאכותית קבועה ביום.

---

## 3. CIBSE AM10 & TM59 — אוורור טבעי וסיכון להתחממות יתר
**מקורות**:
- CIBSE Application Manual AM10: *Natural Ventilation in Non-Domestic Buildings* (ועקרונות גאומטריים למגורים).
- CIBSE Technical Memorandum TM59: *Design Methodology for the Assessment of Overheating Risk in Homes*.
- EN 16798-1: *Energy performance of buildings — Ventilation for buildings*.

### 3.1 כללי אצבע גאומטריים ליעילות אוורור טבעי (CIBSE AM10)
כאשר $H$ הוא גובה התקרה בחדר ו-$W$ הוא עומק החדר (או אורך מסלול הזרימה מהחלון):
1. **אוורור חד-צדדי מפתח יחיד (Single-sided, single opening)**: יעיל רק עד עומק $W \le 2.0 \times H$ (בדירה ישראלית עם $H = 2.60\text{ m}$: עד **$5.20\text{ m}$** בלבד).
2. **אוורור חד-צדדי משני פתחים מרוחקים באותה חזית (Single-sided, dual openings)**: יעיל עד עומק $W \le 2.5 \times H$ (כ-**$6.50\text{ m}$**).
3. **אוורור מפולש (Cross-ventilation)**: יעיל לאורך מסלול זרימה בין שתי חזיתות של עד $W \le 5.0 \times H$ (כ-**$13.0\text{ m}$**, וב-ADG עד $18\text{ m}$ זכוכית-לזכוכית בתנאי שהמעבר פתוח).
4. **יחס שטח פתיחה חופשי (Free Openable Area)**: שטח הפתיחה נטו של החלון (לא רק שטח הזיגוג) צריך להיות $\ge 5\%$ משטח רצפת החדר (בישראל תקנות התכנון והבנייה דורשות 8% זיגוג ו-4% פתיחה חופשית בחדר מגורים/שינה).

### 3.2 מניעת התחממות יתר (Overheating Risk — CIBSE TM59 & IES LM-83 ASE)
- **קריטריון שינה בלילה (TM59)**: טמפרטורת חדר השינה בין 22:00 ל-07:00 לא תעלה על $26^\circ\text{C}$ ביותר מ-1% משעות השנה.
- **זיהוי סיכון תכנוני בתוכנית (Plan-level Risk)**:
  - דירה חד-כיוונית הפונה ל**מערב** או **דרום-מערב** ללא אוורור צולב נמצאת בסיכון גבוה מאוד לחימום יתר.
  - חדר עם יחס זיגוג/רצפה $> 25\%$ בחזית מערבית/דרום-מערבית ללא הצללה חיצונית (תריס גלילה / רפפה חיצונית / מרפסת עמוקה מעל) חשוף ל-Annual Sunlight Exposure (ASE) חריג.

---

## 4. WELL v2 (Light & Air) ו-ASHRAE 62.2 — בריאות, שעון ביולוגי ואיכות אוויר
**מקורות**:
- IWBI, *WELL Building Standard v2* — Features L01, L02, L03 (Circadian Lighting), A01, A03 (Ventilation Design).
- ASHRAE Standard 62.2 — *Ventilation and Acceptable Indoor Air Quality in Residential Buildings*.

- **מרחק מחלון מבט (WELL L01 / L03)**: לפחות 75% מאזורי השהייה הקבועים יהיו במרחק $\le 7.5\text{ m}$ מחלון חיצוני, ואזורי עבודה/אכילה יומיומיים במרחק אופטימלי $\le 4.5\text{ m}$ לצורך חשיפה לאור צירקדי (Equivalent Melanopic Lux).
- **אוורור מקומי במטבח ובחדרים רטובים (ASHRAE 62.2 & ת"י 6210)**:
  - במטבח מומלץ מיקום כיריים המאפשר פליטת אדים בתעלה קצרה לקיר חוץ (ספיקה $\ge 50\text{ L/s}$ או $180\text{ m}^3/\text{h}$).
  - חדרי רחצה ושירותים ללא חלון חיצוני חייבים במערכת יניקה מכנית תקנית ($\ge 25\text{ L/s}$ במקלחת).

---

## 5. ת"י 5281 (בנייה בת-קיימא) ו-14 תבניות הביופיליה (Terrapin Bright Green)
**מקורות**:
- מכון התקנים הישראלי והמשרד להגנת הסביבה, *ת"י 5281 — בנייה בת-קיימא (בנייני מגורים)*, מדריכים טכניים לפרק אנרגיה ופרק בריאות ורווחה.
- Browning, Ryan & Clancy (Terrapin Bright Green), *14 Patterns of Biophilic Design* (2014).

- **ת"י 5281 — בריאות ורווחה**: מעניק ניקוד על:
  1. **אוורור טבעי משופר** (פתחים בשתי חזיתות ומעלה בחללי המגורים).
  2. **אור יום ומבט לחוץ** (עמידה במקדם אור יום $DF$ וקשר עין ישיר לחוץ מ-80% משטח החללים העיקריים).
  3. **נוחות אקוסטית** (שיפור של $\ge 2\text{–}4\text{ dB}$ מעל דרישות הבסיס של ת"י 1004 בקירות מפרידים ובתקרות).
- **14 תבניות ביופיליות לתכנון פנים הדירה**:
  - **Pattern #1 — Visual Connection with Nature**: קו ראייה מהסלון/פינת האוכל אל צמחייה, גינה או מרפסת מגוננת.
  - **Pattern #6 — Dynamic & Diffuse Light**: שילוב אור משני כיוונים (תואם `APL#159`) ליצירת מעברי אור-צל רכים.
  - **Pattern #11 & #12 — Prospect and Refuge (מבט רחוק ומקלט)**: אזור ישיבה (ספה בסלון או עמדת עבודה) נהנה מ**גב מוגן** (קיר מלא מאחור — *Refuge*) ומ**מבט ארוך ופתוח** קדימה אל הכניסה ואל החלון (*Prospect*). ספה שגבה מופנה לדלת הכניסה או למעבר מפרה את עיקרון ה-Refuge.
