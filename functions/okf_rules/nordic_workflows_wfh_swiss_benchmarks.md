---
category: Domestic Chore Workflows, WFH Ergonomics, Asian High-Density & Computational Floor Plan Benchmarks
subcategory: Finnish RT-kortisto (Rakennustieto), Danish SBi-anvisninger (249/253), Swedish Konsumentverket, Leesman Home Index (WFH), Singapore BCA/HDB & Archilyse Swiss Dwellings (45k)
description_summary: Quantitative domestic ergonomics for daily household chores (food safety prep vector, laundry loop, grocery-to-pantry vector, 3-tier storage), Work-From-Home (WFH) visual/acoustic ergonomics, Singapore HDB household shelter placement rules, and statistical percentile benchmarks from the 45,000-unit Swiss Dwellings dataset.
indicator: Food Safety Triangle, Laundry Loop Ergonomics, WFH Station Quality, HDB/Mamad Facade Preservation & Swiss Dwellings Statistical Percentiles
rule_id: WORKFLOWS_WFH_SWISS
type: standard_compendium
engine_usage: validation_engine.run_advanced_checks
verification_status: Compiled from Rakennustieto RT-kortisto (Finland), SBi-anvisning 249 & 253 (BUILD Denmark), Swedish Konsumentverket domestic workflow studies, Leesman Home Index & BCO Homeworking Guidelines, Singapore BCA Universal Design Index & HDB Design Guidelines, and Archilyse AG Swiss Dwellings Dataset v3.0 (Zenodo 7788422).
sbi_food_safety_prep_min_width_cm: 80
sbi_food_safety_prep_optimal_width_cm: 120
sbi_sink_to_prep_max_dist_m: 1.00
chore_grocery_entry_to_fridge_max_m: 6.00
chore_laundry_folding_surface_min_cm: 90
rt_wardrobe_length_per_person_min_m: 0.60
rt_entry_coat_closet_min_width_m: 1.20
rt_cleaning_utility_closet_min_cm: 60
wfh_desk_min_width_cm: 120
wfh_desk_min_depth_cm: 80
swiss_corridor_ratio_p25_excellent: 0.08
swiss_corridor_ratio_p50_median: 0.115
swiss_corridor_ratio_p75_warn: 0.155
swiss_rectangularity_p50_median: 0.89
swiss_entry_private_exposure_max_share: 0.05
---
# הנדסת אנוש של מטלות הבית, עבודה מהבית (WFH), בנייה רוויה באסיה וכיול סטטיסטי (Swiss Dwellings)
## Finnish RT-kortisto · Danish SBi · Konsumentverket · Leesman WFH · Singapore HDB · Archilyse Swiss Dwellings (45k)

> **מטרת הקובץ**: להשלים את בדיקת המידות הסטטיות של החדרים באמצעות **ניתוח זרימת המטלות היומיומיות בדירה (Domestic Chore Workflows)**, **ארגונומיה של עבודה היברידית מהבית (WFH)**, **כללי סינגפור למיקום ממ"ד/מקלט דירתי מבלי לחסום חזיתות**, ו**טבלאות הכיול הסטטיסטיות של מאגר Swiss Dwellings (45,000+ דירות)**.

---

## 1. הנדסת אנוש סקנדינבית של מטלות הבית (RT-kortisto · SBi · Konsumentverket)
**מקורות**:
- Rakennustieto (Finland), *RT-kortisto (Building Information File)* — Asuntosuunnittelu (Housing Design: Kitchens, Laundry, Storage).
- BUILD / Statens Byggeforskningsinstitut (Denmark), *SBi-anvisning 253 (Boligers indretning)* & *SBi-anvisning 249 (Tilgængelige boliger)*.
- Konsumentverket (Swedish Consumer Agency), *Bostadens brukbarhet (Usability of the Home — Kitchen & Laundry Studies)*.

### 1.1 משולש בטיחות המזון ורצף ההכנה במטבח (*Food Safety & Prep Workflow*)
מעבר למשולש העבודה הקלאסי של NKBA (מקרר–כיור–כיריים), המחקרים הסקנדינביים בוחנים את **וקטור ההיגיינה והכנת המזון**:
1. **הסדר הפונקציונלי הנכון:** `מקרר/מזווה ← משטח הנחה (40 ס"מ) ← כיור שטיפה ← משטח הכנה עיקרי (80–120 ס"מ) ← כיריים ← משטח הגשה`.
2. **רצף משטח ההכנה העיקרי ($\ge 80\text{–}120\text{ cm}$):** משטח העבודה העיקרי חייב להימצא **בין הכיור לבין הכיריים** ובמרחק של **$\le \mathbf{1.00\text{ m}}$** מהכיור. כאשר הכיור והכיריים צמודים מדי ($< 60\text{ cm}$) או מופרדים על ידי מעבר/מקרר, הדייר נאלץ להעביר מזון שטוף ורטוב מעל הרצפה, מה שמייצר מפגע החלקה וזיהום צולב.

### 1.2 מסלול הכביסה המשפחתי (*The Domestic Laundry Loop*)
אחת המטלות השוחקות ביותר בדירת מגורים היא שינוע כביסה. המדד בודק את אורך וטופולוגיית הלולאה:
$$\text{Bedrooms (Dirty Laundry)} \longrightarrow \text{Washer / Dryer} \longrightarrow \text{Drying / Folding Surface} \longrightarrow \text{Bedroom Wardrobes}$$
- **תכנון מיטבי (`PASS`):** חדר כביסה או מפרץ שירות הממוקם **בתוך אגף חדרי השינה** (או בצמוד לחדר הרחצה המשפחתי), הכולל מכונת כביסה ומייבש, אוורור ישיר, ומשטח קיפול ומיון צמוד ברוחב $\ge \mathbf{90\text{ cm}}$.
- **תכנון לקוי (`WARN`):** מכונת כביסה הממוקמת במרפסת שירות הקשורה למטבח או לסלון, המחייבת נשיאת סלי כביסה דרך חלל האירוח הציבורי.

### 1.3 וקטור קניות–מזווה–אשפה (*Grocery & Waste Vector*)
- **מרחק מדלת הכניסה למקרר/מזווה ($\le \mathbf{6.00\text{ m}}$):** כניסה עם שקיות קניות כבדות צריכה להוביל ישירות למטבח/מזווה מבלי לחצות את השטיח ואזור הישיבה בסלון.
- **היררכיית אחסון בת 3 שכבות (*RT-kortisto Storage Hierarchy*):**
  1. **אחסון כניסה (*Eteinen*):** ארון מעילים, נעליים ותיקים ברוחב $\ge \mathbf{1.20\text{ m}}$ ועומק $60\text{ cm}$ סמוך לדלת הכניסה.
  2. **ארון תחזוקה וניקיון (*Siivouskaappi*):** תא ייעודי של $\ge \mathbf{60 \times 60\text{ cm}}$ עם שקע טעינה לשואב אבק רובוטי/אלחוטי, מגב וחומרי ניקוי (בטיחותי מילדים).
  3. **אחסון בגדים אישי:** $\ge \mathbf{0.60\text{ m}}$ אורך ארון ($60\text{ cm}$ עומק) לכל נפש בדירה.

---

## 2. ארגונומיה של עבודה מהבית — *Leesman Home Index* & *BCO Homeworking*
**מקורות**:
- Leesman, *The Home Working Impact Code / Leesman Home Index* (מבוסס על 250,000+ שאלוני עובדים מהבית).
- British Council for Offices (BCO), * Wellness Matter & Homeworking Ergonomics Guidelines*.

### 2.1 קריטריונים כמותיים לעמדת עבודה בדירה (`WFH-1`)
1. **שטח מוגדר לעמדת עבודה ארגונומית ($\ge 120 \times 80\text{ cm}$):**
   - נישה שקטה, חדר עבודה או אזור מוגדר בחדר שינה/ממ"ד המאפשר הצבת שולחן בעומק $\ge 70\text{–}80\text{ cm}$ וברוחב $\ge 120\text{ cm}$ + כיסא ארגונומי, **מבלי לתפוס את שולחן האוכל המשפחתי**.
2. **העמדה בניצב לחלון ($90^\circ$ Daylight Orientation):**
   - מיקום מסך המחשב עם הפנים לחלון יוצר סנוור ניגודיות (Contrast Glare), ומיקום עם הגב לחלון יוצר השתקפות על המסך וצללית שחורה בשיחות וידאו. העמדה האופטימלית היא **בניצב לחלון ($90^\circ$)**.
3. **רקע אקוסטי וויזואלי מוגן (*Acoustic & Camera Privacy*):**
   - גב הכיסא פונה לקיר אטום או ספרייה (ולא למסדרון מעבר לחדרי רחצה או למטבח הפעיל).

---

## 3. Singapore BCA / HDB — כללי מיקום ממ"ד (*Household Shelter*) ואוורור טבעי
**מקורות**:
- Building and Construction Authority (BCA Singapore) & Housing and Development Board (HDB), *Universal Design Guide* & *Technical Requirements for Household Shelters*.

בסינגפור, בדומה לישראל, קיימת חובת בניית **מקלט דירתי מבטון מזוין (*Household Shelter*)** בכל דירה חדשה:
1. **איסור חסימת חזית החוץ הראשית (*Zero Perimeter Facade Obstruction*):**
   - ב-HDB סינגפור, המקלט הדירתי ממוקם באזור הליבה הפנימית של הדירה (סמוך לכניסה או למטבח/שירות) כדי להשאיר 100% מאורך חזיתות החוץ לחדרי שינה ולסלון.
   - **יישום מותאם לישראל** (שבה הממ"ד חייב בחלון חוץ לפי פקע"ר): מיקום הממ"ד ב**קצה האגף הפרטי** (ולא במרכז החזית בין הסלון לחדר השינה או בין שני חדרי ילדים), כך שקירות הבטון שלו לא יקטעו את רצף החזית ולא ימנעו איחוד/שינוי של חדרי השינה בעתיד.

---

## 4. כיול סטטיסטי מול מאגר *Archilyse Swiss Dwellings (45,000+ Apartments)*
**מקור**:
- Matthias Standfest et al. (Archilyse AG), *Swiss Dwellings: A large dataset of canonicalized floor plans with graph and simulation metrics* (Zenodo Record `7788422`, ~45,000 apartments, ~370,000 rooms).
- Casper van Engelenburg et al. (TU Delft, 2024), *MSD: Modified Swiss Dwellings Benchmark*.

מאגר **Swiss Dwellings** מאפשר להעביר את הערכת התוכנית מבדיקת סף בינארית (עובר/נכשל) ל**דירוג אחוזוני (Percentile Ranking)** מול 45,000 דירות אירופאיות:

| מדד תכנוני (Metric) | אחוזון 25 ($P_{25}$ — חלש) | חציון ($P_{50}$ — ממוצע) | אחוזון 75 ($P_{75}$ — טוב מאוד) | אחוזון 90 ($P_{90}$ — מצטיין) |
| :--- | :---: | :---: | :---: | :---: |
| **יחס שטח מסדרון/מעברים מתוך הדירה (`EF-1`)** | $15.5\%$ | $11.5\%$ | $8.0\%$ | $\le 5.5\%$ (*Hallenwohnung*) |
| **מלבניות ממוצעת של חדרי שינה (`EF-2`)** | $0.82$ | $0.89$ | $0.94$ | $\ge 0.97$ |
| **חשיפת חדרים פרטיים ב-Isovist מדלת הכניסה** | $> 12\%$ | $5.0\%$ | $1.5\%$ | $0.0\%$ (פרטיות מלאה) |
| **יחס שטח חלל ציבורי לשטח הדירה נטו** | $26\%$ | $32\%$ | $37\%$ | $40\%\text{–}44\%$ |
| **מספר כיווני אוויר ושמש לחלל המגורים** | $1$ (חד-כיווני) | $1.5$ | $2$ (דו-כיווני פינתי) | $2\text{–}3$ (*Durchwohnen* מפולש) |
