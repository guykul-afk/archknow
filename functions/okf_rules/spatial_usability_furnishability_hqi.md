---
category: Spatial Usability, Furnishability & Lifecycle Adaptability
indicator: Furnishability, Programmatic Proportionality, Universal Usability & Adaptability (Boverket / Byggforsk / HQI / Lifetime Homes / DIN 18040-2 / SIA 500 / EU Level(s) / CBE POE)
rule_id: USABILITY_FURNISH_HQI
type: standard_compendium
engine_usage: validation_engine.run_advanced_checks
verification_status: Numerical benchmarks compiled from Swedish Boverket BBR (Möblerbarhet) & Norwegian SINTEF Byggforskserien, UK Homes England HQI (Housing Quality Indicators), Lifetime Homes (16 Criteria) / Approved Document M4(2), German DIN 18040-2, Swiss SIA 500, EU Level(s) Indicator 2.3, and UC Berkeley CBE POE survey benchmarks.
boverket_double_bed_wall_min_m: 3.00
boverket_single_bed_wall_min_m: 2.10
boverket_double_wardrobe_wall_min_m: 1.80
boverket_single_wardrobe_wall_min_m: 1.20
boverket_door_corner_offset_min_cm: 60
hqi_combined_living_sqm_by_bedspaces:
  1: 18.0
  2: 21.0
  3: 23.0
  4: 25.0
  5: 27.0
  6: 29.0
  7: 31.0
  8: 33.0
hqi_living_only_min_sqm_by_bedspaces:
  1: 11.0
  2: 12.0
  3: 13.0
  4: 14.0
  5: 16.0
  6: 18.0
  7: 20.0
  8: 21.0
din18040_corridor_min_cm: 120
din18040_latch_side_pull_min_cm: 60
din18040_latch_side_push_min_cm: 30
din18040_bedside_clearance_min_cm: 90
din18040_bedside_wheelchair_min_cm: 120
levels_adaptable_partition_min_ratio: 0.60
---
# שימושיות מרחבית, יכולת ריהוט, איזון פרוגרמטי ועמידות לאורך החיים
## Boverket & Byggforsk · HQI · Lifetime Homes · DIN 18040-2 & SIA 500 · EU Level(s) · CBE POE

> **מטרת הקובץ**: להשלים את בדיקת השטחים והמידות באמצעות מדדי **שימושיות בפועל (Usability)**: האם ניתן לרהט את החדר ביותר מדרך אחת? האם גודל הסלון ופינת האוכל תואם את מספר הדיירים בדירה? האם מיקום הדלתות והקירות מאפשר תנועה נוחה, שקט אקוסטי והתאמה עתידית?

---

## 1. Boverket (שוודיה) & SINTEF Byggforskserien (נורווגיה) — יכולת ריהוט (*Möblerbarhet*)
**מקורות**:
- Boverket (Swedish National Board of Housing, Building and Planning), *Boverkets byggregler (BBR)* — Section 3:2 (Room layout and furnishability / *Möblerbarhet*).
- SINTEF Community (Norway), *Byggforskserien — Planlegging 321 / 330 (Boligplanlegging og møblering)*.
- משלים את עיקרון ה-*Möblierbarkeit* בשיטת **WBS** השוויצרית (`WBS_NDSS_ADG`).

### 1.1 אורך קיר רציף לריהוט (Unbroken Wall Length)
שטח חדר במ"ר אינו מספיק אם הקירות "חתוכים" על ידי דלתות, חלונות נמוכים או נישות:
- **חדר שינה זוגי**:
  - קיר רציף לראש מיטה זוגית + שתי שידות צד: $\ge \mathbf{3.00\text{ m}}$ (מיטה $160\text{–}180\text{ cm}$ + $2 \times 60\text{ cm}$).
  - קיר רציף לארון בגדים: אורך $\ge \mathbf{1.80\text{ m}}$ ($60\text{ cm}$ לאדם + מעבר, או $180\text{–}240\text{ cm}$ לזוג) בעומק נקי של $\ge \mathbf{60\text{ cm}}$.
- **חדר שינה יחיד / ילדים**:
  - קיר רציף למיטה: $\ge \mathbf{2.10\text{ m}}$ + קיר לשולחן כתיבה ($\ge 1.20\text{ m}$) + קיר לארון ($\ge \mathbf{1.20\text{ m}}$).
- **היסט דלת מפינת החדר (Door Corner Offset)**:
  - כאשר דלת חדר השינה ממוקמת סמוך לקיר ניצב שבו מתוכנן ארון בגדים, מרחק המשקוף מפינת החדר חייב להיות $\ge \mathbf{60\text{ cm}}$ (או $\le 10\text{ cm}$ אם הקיר הניצב אינו מיועד לארון). מרחק של $15\text{–}50\text{ cm}$ יוצר "פינה מתה" שבה לא ניתן להעמיד ארון בעומק תקני של $60\text{ cm}$.

---

## 2. UK Housing Quality Indicators (HQI) — איזון פרוגרמטי (Proportionality)
**מקור**: UK Homes and Communities Agency (Homes England), *Housing Quality Indicators (HQI) Form, Version 4* — Indicator 3: Unit Size & Indicator 4: Unit Layout.

אחד הכשלים הנפוצים בדירות יזמיות (בישראל ובעולם) הוא **חוסר פרופורציה בין מספר חדרי השינה לבין גודל החלל הציבורי**: דירת 5 חדרים (6–8 נפשות) שבה הסלון ופינת האוכל זהים בגודלם לדירת 3 חדרים.

### 2.1 שטח מינימלי לחלל הציבורי לפי מספר מיטות/נפשות (Bedspaces $p$)
| מספר מיטות בדירה ($p$) | שטח סלון מינימלי לבדו (מ"ר) | שטח ציבורי משולב מינימלי: סלון + פינת אוכל + מטבח (מ"ר) | מספר מושבים מינימלי בסלון ובשולחן האוכל |
| :---: | :---: | :---: | :---: |
| **1p** | 11.0 | 18.0 | 2–3 |
| **2p** | 12.0 | 21.0 | 3–4 |
| **3p** | 13.0 | 23.0 | 4 |
| **4p** | 14.0 | 25.0 | 4–5 |
| **5p** | 16.0 | 27.0 | 5–6 |
| **6p** | 18.0 | 29.0 | 6 |
| **7p** | 20.0 | 31.0 | 7 |
| **8p+** | 21.0 | 33.0 | 8+ |

---

## 3. Lifetime Homes (16 Criteria), DIN 18040-2 ו-SIA 500 — שימושיות אוניברסלית
**מקורות**:
- Habinteg / Joseph Rowntree Foundation, *Lifetime Homes Revised Criteria* (16 Criteria) & UK *Approved Document M — Category M4(2) Accessible and Adaptable Dwellings*.
- DIN 18040-2: *Barrierefreies Bauen — Planungsgrundlagen — Teil 2: Wohnungen* (גרמניה).
- SIA 500: *Hindernisfreie Bauten* (שווייץ, סעיף 9 — דיור).

### 3.1 גאומטריית דלתות, מסדרונות ומרווחי גישה
- **מרווח צד ליד ידית הדלת (Latch-side Clearance — DIN 18040-2 / Lifetime Homes Crit. 6)**:
  - בצד שבו מושכים את הדלת (Pull side): מרווח קיר פנוי של $\ge \mathbf{60\text{ cm}}$ לצד הידית (כדי שאדם עם עגלה, קביים או כיסא גלגלים יוכל לעמוד לצד כנף הדלת הנפתחת).
  - בצד שבו דוחפים את הדלת (Push side): מרווח קיר פנוי של $\ge \mathbf{30\text{ cm}}$ לצד הידית.
- **רוחב מסדרון מול רוחב דלת בניצב (Lifetime Homes Crit. 6 / M4(2))**:
  - מסדרון ברוחב $\ge 120\text{ cm}$ מאפשר פנייה של $90^\circ$ לתוך דלת ברוחב נטו $75\text{–}80\text{ cm}$.
  - מסדרון ברוחב $105\text{ cm}$ מחייב דלת ברוחב נטו $\ge 80\text{ cm}$.
  - מסדרון ברוחב $90\text{ cm}$ מחייב דלת ברוחב נטו $\ge 90\text{ cm}$ (או דלת בקצה המסדרון בכיוון ההליכה).
- **מרווח גישה לצד מיטה (Bedside Transfer — DIN 18040-2 / SIA 500)**:
  - בחדר השינה העיקרי יישמר מרווח פנוי של $\ge \mathbf{90\text{ cm}}$ (ובדירה נגישה $\ge \mathbf{120\text{ cm}}$) לפחות לאורך צד אחד של המיטה הזוגית.

---

## 4. EU Level(s) Indicator 2.3 — תכנון להתאמה וגמישות עתידית (Adaptability)
**מקור**: European Commission Joint Research Centre (JRC), *Level(s) — A common EU framework of core sustainability indicators for office and residential buildings*, Indicator 2.3: *Design for adaptability and renovation*.

- **יחס מחיצות פנים פריקות (Non-load-bearing Internal Walls)**:
  - לפחות **60% מאורך מחיצות הפנים** בדירה יהיו מחיצות לא-נושאות (בלוקים קלים / גבס) הניתנות לפירוק או הזזה ללא פגיעה בשלד הבניין או בממ"ד.
- **מיקום ליבות רטובות (Wet Cores & Shafts)**:
  - ריכוז פירים אנכיים (אינסטלציה/אוורור) בצמידות למסדרון או לקיר מעטפת פנימי כך שלא יחצו את מרכז הדירה ויאפשרו איחוד/פיצול של חדרי שינה או הרחבת הסלון בעתיד (משלים את גישת *Open Building* של Habraken ואת `SPACE_SYNTAX_SAGA`).

---

## 5. CBE & BUS Post-Occupancy Evaluation — אקוסטיקה פנימית ופרטיות
**מקורות**:
- UC Berkeley Center for the Built Environment (CBE), *Occupant Indoor Environmental Quality (IEQ) Survey Database*.
- BUS Methodology (Building Use Studies, Arup) & תקן ישראלי **ת"י 1004** (בידוד אקוסטי בבנייני מגורים).

מחקרי POE לאחר אכלוס מראים כי **התלונה מספר 1 במגורים רוויים** היא העברת רעש וריחות בתוך הדירה ובין דירות:
- **חיץ אקוסטי פנימי (Internal Acoustic Buffering)**:
  - הימנעות מקיר משותף ישיר בין חדר שינה לבין אזור הטלוויזיה בסלון, המטבח, פיר המעלית או מסתור הכביסה/מזגנים.
  - שימוש בארון בגדים לכל אורך הקיר המשותף (עומק $60\text{ cm}$) משמש כחיץ אקוסטי מצוין בין שני חדרי שינה או בין חדר שינה לסלון.
- **פרטיות ויזואלית בין מרפסות וחלונות (Visual Privacy)**:
  - הימנעות מחלונות חדרי שינה הפונים במרחק קצר ($< 6\text{ m}$) ובזווית ישירה אל מרפסת או סלון של דירה סמוכה באותה קומה.
