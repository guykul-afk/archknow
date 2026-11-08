---
category: Healthy Housing Epidemiology, Domestic Safety, Baubiologie & Dementia-Friendly Design
subcategory: UK HHSRS (29 Hazards), German Baubiologie (IBN / SBM-2015), WHO Housing & Health (2018), WELL Residence, University of Stirling DSDC (EADDAT) & Dutch WoonKeur
description_summary: Comprehensive physical health, accident prevention, sleep-zone building biology (EMF/acoustic/plumbing decoupling & night CO2 volume), and cognitive aging/dementia floor plan guidelines (bed-to-toilet sightlines, rollator usability).
indicator: Domestic Accident Prevention (HHSRS), Sleep Biology (Baubiologie SBM-2015), Night Air Volume, Dementia Bed-to-Toilet Sightline & WoonKeur Lifecycle Safety
rule_id: HEALTH_BAUBIO_DSDC
type: standard_compendium
engine_usage: validation_engine.run_advanced_checks
verification_status: Compiled from UK Housing Health and Safety Rating System (HHSRS Operating Guidance, Housing Act 2004), Institut für Baubiologie + Nachhaltigkeit (IBN 25 Guidelines & SBM-2015 Standard of Building Biology Testing Methods), WHO Housing and Health Guidelines (2018), Harvard T.H. Chan School of Public Health (9 Foundations of a Healthy Building), IWBI WELL for Residential, University of Stirling DSDC (EADDAT), and Dutch SKG-IKOB WoonKeur.
hhsrs_cooktop_side_clearance_min_cm: 40
hhsrs_max_threshold_step_mm: 15
hhsrs_stair_door_landing_min_cm: 100
baubio_bed_to_elec_panel_min_m: 1.50
baubio_bed_to_elevator_shaft_min_m: 1.50
baubio_sleep_air_volume_per_person_min_m3: 13.5
who_night_facade_noise_max_db: 45
dsdc_bed_to_toilet_max_dist_m: 4.50
dsdc_bed_to_toilet_max_turns: 1
woonkeur_rollator_passage_min_cm: 90
---
# אפידמיולוגיה של המגורים, בטיחות ביתית, ביולוגיית המבנה ונגישות קוגניטיבית
## UK HHSRS · Baubiologie SBM-2015 · WHO & Harvard Healthy Buildings · WELL Residence · Stirling DSDC · WoonKeur

> **מטרת הקובץ**: לשלב במנוע הבקרה את בסיסי הידע המובילים בעולם ל**בריאות פיזית**, **מניעת תאונות ביתיות**, **היגיינת שינה וביולוגיית המבנה (Baubiologie)** ו**התאמה קוגניטיבית-מוטורית לגיל השלישי (DSDC / WoonKeur)**.

---

## 1. UK HHSRS — מערכת דירוג הבריאות והבטיחות במגורים (29 מפגעים)
**מקור**: UK Ministry of Housing, Communities and Local Government, *Housing Health and Safety Rating System (HHSRS) Operating Guidance* (Housing Act 2004).

מערכת ה-HHSRS מבוססת על מחקרים אפידמיולוגיים רחבי היקף של פגיעות ותחלואה בבתים, ומחלקת 29 מפגעים ל-4 מחלקות (דרישות פיזיולוגיות, דרישות פסיכולוגיות, הגנה מזיהומים והגנה מתאונות).

### 1.1 חוקים גיאומטריים הנגזרים מ-HHSRS לתוכנית הדירה
1. **מפגע #26 — התנגשות והילכדות (*Collision and Trapping*):**
   - **אי-חפיפת קשתות דלתות (*Zero Door-Swing Clash*):** שתי דלתות סמוכות (כגון דלת חדר רחצה ודלת חדר שינה, או דלת ממ"ד ודלת מסדרון) לא יחפפו בגזרת הפתיחה שלהן.
   - **דלתות הנפתחות למסדרון צר:** דלת חדר או דלת הדף של ממ"ד הנפתחת החוצה לתוך מסדרון ברוחב $< 110\text{ cm}$ חייבת להיסגר לתוך גומחה שקועה בקיר (*Recessed Pocket*) כך שלא תבלוט לנתיב ההליכה.
2. **מפגעים #25 ו-#28 — כוויות, משטחים חמים וארגונומיה של מתקנים (*Hot Surfaces & Position of Amenities*):**
   - **מרווח בטיחות לצידי הכיריים ($\ge 40\text{ cm}$):** אין למקם כיריים בקצה פתוח של דלפק, צמוד למעבר הולכי רגל ראשי (למרפסת או לחדר שירות) או צמוד לדופן ארון גבוה/קיר ניצב ללא מרווח משטח של לפחות **$40\text{ cm}$** מכל צד (מניעת הפלת סירים רותחים על ידי ילדים חולפים).
3. **מפגעים #19, #20 ו-#21 — מניעת נפילות במפלס ובחדרים רטובים (*Falls on the Level & Baths*):**
   - **איסור מדרגות בודדות (*Single-Step Ban*):** אין לתכנן מדרגה בודדת או שתי מדרגות פנימיות בתוך מפלס הדירה (מוקד מוביל למעידות קשות).
   - **סף מרפסת ומקלחון מובלע ($\le 15\text{ mm}$):** מעבר שטוח ללא מכשול מעידה בין הסלון למרפסת ובין רצפת חדר הרחצה למקלחון.
4. **מפגע #1 — לחות, עיבוי ועובש (*Damp and Mould Growth*):**
   - **מניעת הצמדת ארון בגדים לפינת קיר חוץ צפונית (*Thermal Bridge Mold Guard*):** בפינה חיצונית (מפגש שני קירות חוץ), הצמדת ארון בגדים עמוק חוסמת את זרימת האוויר החם אל הקיר הקר ומורידה את טמפרטורת פני השטח מתחת לנקודת הטל ($\text{RH} > 80\%$), מה שגורם לעובש סמוי מאחורי הארון. ארונות קיר יתוכננו על **מחיצות פנים** (שם הם גם משמשים כחיץ אקוסטי!).

---

## 2. ביולוגיית המבנה הגרמנית — *Baubiologie IBN & SBM-2015* (היגיינת אזור השינה)
**מקורות**:
- Institut für Baubiologie + Nachhaltigkeit (IBN, Rosenheim), *25 Guidelines of Building Biology*.
- Maes, W. & IBN (2015), *SBM-2015: Standard of Building Biology Testing Methods — Precautionary Values for Sleeping Areas*.
- Joseph G. Allen & John D. Macomber (Harvard T.H. Chan School of Public Health), *Healthy Buildings: How Indoor Spaces Drive Performance and Productivity* (9 Foundations of a Healthy Building).

לפי תקן ה-**SBM-2015**, אזור המיטה הוא החלל הרגיש ביותר בדירה משום שהגוף נמצא בו במצב של רגנרציה עצבית והורמונלית במשך 7–9 שעות רצופות ביממה.

### 2.1 כללי תכנון כמותיים לאזור השינה (*Sleep Sanctuary Audit*)
1. **מרחק ביטחון ממוקדי קרינה אלקטרומגנטית בתדר נמוך ורעש תשתיתי ($\ge 1.50\text{ m}$):**
   - קיר ראש המיטה **לא יגבול ישירות** (ולא ימוקם במרחק אווירי הקטן מ-**$\mathbf{1.50\text{ m}}$**) ב:
     - **לוח חשמל דירתי או ארון חשמל קומתי** (שדות מגנטיים חילופיים $> 100\text{ nT}$).
     - **פיר מעלית, חדר מכונות או חדר משאבות** (רעש מבני ותנודות תדר נמוך + שדות מנוע).
     - **מעבה מזגן VRF / מנוע משאבת חום או ממיר סולארי** מעבר לקיר החוץ.
     - **גב מטבח עם מכשירי הספק גבוה** (מקרר, תנור אפייה, כיריים אינדוקציה).
2. **הפרדת קיר ראש המיטה מקולטני ביוב וצנרת ראשית (*Plumbing Riser Decoupling*):**
   - אין למקם ראש מיטה על קיר שבו עובר קולטן ביוב $4''$ או צנרת הזנת מים ראשית (הן למניעת יקיצות מיקרוסקופיות מרעש הדחת מים בקומות עליונות והן למניעת שדות מגנטיים מזרמים תועים בצנרת).
3. **נפח אוויר מינימלי בחדר שינה למניעת הצטברות $\text{CO}_2$ לילי ($\ge 13.5\text{ m}^3$ לנפש):**
   - מחקרי Harvard T.H. Chan מראים כי בחדר שינה סגור (ובפרט ב**ממ"ד** המשמש כחדר שינה), ריכוז ה-$\text{CO}_2$ חוצה במהירות $1,000\text{–}1,500\text{ ppm}$ ופוגע באיכות השינה ובתפקוד הקוגניטיבי ביום שלמחרת.
   - **מדד נפח אוויר לשינה:** נפח החדר הפנוי ($A_{net} \times H_{clear}$) צריך לספק לפחות **$\mathbf{13.5\text{ m}^3}$ לנפש** ($\ge 27.0\text{ m}^3$ לחדר שינה זוגי, כלומר שטח $\ge 10.0\text{ m}^2$ בגובה $2.70\text{ m}$), בשילוב פתח אוורור חריצי שקט או מערכת אוורור מאוזנת.

---

## 3. WHO *Housing and Health Guidelines* & *WELL Residence*
**מקורות**:
- World Health Organization (2018), *WHO Housing and Health Guidelines* & *Environmental Noise Guidelines for the European Region*.
- International WELL Building Institute (IWBI), *WELL for Residential (WELL Residence)* Standard.

1. **עקרון החזית השקטה לחדרי שינה (*Quiet Facade Principle — WHO $<45\text{ dB }L_{night}$*):**
   - בבניינים הפונים לרחוב עירוני סואן ($> 53\text{ dB }L_{den}$), תכנון הדירה ימקם את הסלון והמטבח לכיוון הרחוב הפעיל, ולפחות חדר שינה עיקרי אחד יפנה ל**חזית שקטה** (חצר פנימית, גינה עורפית או חזית מוגנת אקוסטית $< 45\text{ dB }L_{night}$).
2. **מחסום אוויר כפול ממקורות זיהום (*WELL Res Air Infiltration Barrier*):**
   - איסור פתיחה ישירה של חדר אשפה, חניון תת-קרקעי או חדר גנרטור אל לובי הקומה/הכניסה ללא **מבואת אוויר כפולה (Airlock Vestibule)** בלחץ שלילי.

---

## 4. University of Stirling DSDC (EADDAT) & תקן *WoonKeur* ההולנדי
**מקורות**:
- University of Stirling, Dementia Services Development Centre (DSDC), *Environments for Ageing and Dementia Design Assessment Tool (EADDAT)*.
- SKG-IKOB (Netherlands), *WoonKeur — Keurmerk voor toegankelijkheid, gebruikskwaliteit en aanpasbaarheid*.
- ISO 21542:2021 — *Building construction — Accessibility and usability of the built environment*.

### 4.1 קו ראייה ממיטה לאסלה ומניעת נפילות לילה (*DSDC Bed-to-Toilet Sightline*)
מחקרים קליניים של מרכז DSDC באוניברסיטת סטירלינג הוכיחו כי אחד הגורמים המכריעים במניעת נפילות לילה, חרדת התמצאות ואי-שליטה בגיל השלישי הוא **קיום קו ראייה ישיר מהמיטה אל האסלה**:
- **מדד גיאומטרי בתוכנית (`DSDC-1`):**
  1. בחדר השינה העיקרי (מאסטר) או ביחידת דיור מותאמת, קיים **קו ראייה ישיר (Unobstructed Sightline)** מכרית המיטה דרך פתח חדר הרחצה אל האסלה (או שניתן לראות את האסלה מיד עם ישיבה על קצה המיטה).
  2. **מרחק הליכה קצר ופשוט:** המרחק מצידי המיטה אל האסלה הוא $\le \mathbf{4.50\text{ m}}$ עם **לכל היותר פנייה אחת ($\le 1$ turn)** וללא דלתות מתנגשות.

### 4.2 תאימות הליכון ומוכנות לסיעוד עתידי (*WoonKeur Rollator & Care-Ready*)
- **מעבר הליכון (*Rollator-Capable*):** רוחב מעבר פנוי של $\ge \mathbf{90\text{ cm}}$ במסדרון, סביב המיטה ובכניסה לחדר הרחצה.
- **קיר פריקה להרחבת חדר רחצה (*Future Care Wall*):** הקיר המפריד בין חדר השינה לחדר הרחצה הצמוד יתוכנן כקיר בלוקים/גבס לא-נושא (ללא עמודים או פירים במרכזו), כך שבעת צורך סיעודי ניתן יהיה לאחד או להרחיב את הפתח למעבר מיטה/מנוף סיעודי.
