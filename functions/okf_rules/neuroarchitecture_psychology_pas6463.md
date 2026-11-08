---
category: Neuroarchitecture, Environmental Psychology & Sensory Well-Being
subcategory: BSI PAS 6463:2022, ANFA (Vartanian & Meyers-Levy), Ulrich SRT, Kaplan ART, Appleton Prospect-Refuge & Evans Crowding Stress
description_summary: Quantifiable architectural and spatial psychology rules evaluating cognitive load, sensory regulation (PAS 6463), volumetric proportion (Cathedral Effect), sleep/work Command Position (Prospect & Refuge), restorative sightlines (ART/SRT), and household crowding decompression spaces.
indicator: Neurodiversity & Sensory Calm, Volumetric Slenderness, Command Position, Restorative Views & Psychological Privacy (PAS 6463 / ANFA / SRT / ART)
rule_id: NEURO_PSYCH_PAS6463
type: standard_compendium
engine_usage: validation_engine.run_advanced_checks
verification_status: Compiled from BSI PAS 6463:2022 (Design for the Mind — Neurodiversity and the Built Environment), Meyers-Levy & Zhu (2007) Cathedral Effect, Vartanian et al. (2013/2015) fMRI Neuroaesthetics, Roger Ulrich (1984/1991) Stress Recovery Theory, Kaplan & Kaplan (1989) Attention Restoration Theory, Jay Appleton (1975) Prospect-Refuge Theory, and Gary Evans (Cornell) Residential Crowding Stress studies.
pas6463_max_doors_per_corridor_node: 5
pas6463_bedroom_max_ambient_noise_dba: 30
pas6463_living_max_ambient_noise_dba: 35
anfa_cathedral_public_ceiling_recommended_m: 2.85
anfa_volumetric_slenderness_min_ratio: 0.48
anfa_volumetric_slenderness_optimal_ratio: 0.54
anfa_min_interior_corner_angle_deg: 75
art_restorative_sightline_min_m: 6.0
command_pos_min_door_to_bed_offset_m: 0.60
evans_crowding_secondary_retreat_min_bedspaces: 5
---
# נוירו-אדריכלות, פסיכולוגיה סביבתית וויסות חושי בדירת המגורים
## BSI PAS 6463:2022 · ANFA (Vartanian & Meyers-Levy) · Ulrich SRT · Kaplan ART · Prospect-Refuge · Evans Crowding

> **מטרת הקובץ**: לתרגם ממצאים קליניים ואמפיריים מתחומי **מדעי המוח לאדריכלות (Neuroarchitecture)**, **פסיכולוגיה סביבתית** ו**תכנון רגיש-חושית (Neuro-Inclusive Design)** למדדים גאומטריים וטופולוגיים כמותיים הניתנים לבדיקה אוטומטית על תוכנית דירה (2D ו-3D BIM).

---

## 1. BSI PAS 6463:2022 — תכנון לתודעה, שונות נוירולוגית וויסות חושי (*Design for the Mind*)
**מקור**: British Standards Institution (BSI), *PAS 6463:2022 — Design for the mind: Neurodiversity and the built environment — Guide*.

התקן מגדיר שלושה עקרונות ליבה לתכנון המפחית עומס קוגניטיבי וחושי (עבור כלל האוכלוסייה ובפרט אנשים עם קשב וריכוז ADHD, רגישות חושית גבוהה HSP, הספקטרום האוטיסטי, חרדה או שחיקה נפשית): **Clarity (בהירות מרחבית)**, **Control (שליטה בסביבה)** ו-**Calm (מרחב התאוששות ושקט)**.

### 1.1 קריטריונים כמותיים לתוכנית הדירה
1. **מובנות מרחבית ומניעת עומס צמתים (*Spatial Legibility & Junction Overload*):**
   - צומת מסדרון או מבואה שבהם נפתחות מעל **$5$ דלתות צמודות** ללא היררכיה ויזואלית ברורה יוצר עומס קוגניטיבי, תחושת מבוך והתנגשויות תנועה.
   - **כלל תכנוני:** ריווח פתחי חדרים או חלוקת המסדרון למבואות משנה שקטות ($\le 4\text{–}5$ דלתות לצומת).
2. **מרחב ויסות והתאוששות שקט (*Calm / Decompression Refuge Space*):**
   - בכל דירה (ובפרט בדירות משפחתיות עם $\ge 4$ נפשות) נדרש לפחות חלל שהייה או נישה מוגדרת המאפשרים התבודדות שקטה מחוץ לציר התנועה הראשי (ערך אינטגרציה נמוך בגרף ה-Space Syntax, ללא קיר משותף עם פיר מעלית או מערכות מכניות).
3. **מניעת סנוור קצה וצללית במסדרון (*Corridor Silhouette Glare Avoidance*):**
   - חלון לא מוצלל הפונה למערב או לדרום בקצה מסדרון צר וארוך יוצר "אפקט סנוור צללית" (הופך אנשים הבאים ממול לצלליות כהות ומעורר דריכות חושית). פתחי קצה במסדרון יופנו לצפון/מזרח או יכללו הצללה אדריכלית/זכוכית חלבית מרככת.
4. **הפרדת ריחות ורעש תדר-נמוך (*Olfactory & Low-Frequency Noise Containment*):**
   - יכולת סגירה אקוסטית וריחנית (דלת הזזה אטומה או הפרדה מרחבית) בין אזור הבישול/כביסה לבין אזור העבודה או המנוחה, ושמירה על מפלס רעש מערכות $\le \mathbf{30\text{ dBA}}$ בחדרי שינה.

---

## 2. מחקרי ANFA — אפקט הקתדרלה (*Cathedral Effect*) וגיאומטריית החלל
**מקורות**:
- Joan Meyers-Levy & Rui Zhu (2007), "The Influence of Ceiling Height: The Effect of Priming on the Type of Processing That People Use", *Journal of Consumer Research*, 34(2).
- Oshin Vartanian et al. (2013, 2015), "Impact of contour on aesthetic judgments and approach-avoidance decisions in architecture" & "Architectural design and the brain: Effects of ceiling height and perceived enclosure on beauty judgments and approach-avoidance decisions", *PNAS* / *Journal of Environmental Psychology*.

### 2.1 יחס נפח-שטח וגובה תקרה דיפרנציאלי (*Volumetric Slenderness Ratio*)
מחקרי הדמיית מוח (fMRI) מראים כי המוח האנושי אינו מגיב לגובה תקרה אבסולוטי בלבד, אלא ל**פרופורציה שבין גובה התקרה ($H_{clear}$) לבין מפתח החדר ($\sqrt{A_{room}}$)**:

$$R_v = \frac{H_{clear}}{\sqrt{A_{room}}}$$

- **בחלל המגורים הציבורי (סלון + פינת אוכל $> 25\text{ m}^2$):**
  - כאשר גובה התקרה הוא המינימום החוקי בלבד ($2.50\text{–}2.55\text{ m}$) בחלל רחב של $30\text{–}35\text{ m}^2$, יחס הגבהות צונח ל-$R_v \approx 0.43 < 0.48$, מה שמפעיל תחושת דחיסות אנכית ("אפקט מערה/חניון").
  - **סף מומלץ ($R_v \ge 0.48\text{–}0.54$):** גובה תקרה נטו של **$\ge \mathbf{2.80\text{–}3.00\text{ m}}$** בחלל הציבורי מעורר חשיבה יצירתית, תחושת רווחה ונטייה חברתית חיובית (*Approach response*), תוך הימנעות מהנמכות גבס רחבות של מיזוג במרכז הסלון.
- **בחדרי שינה ופינות ריכוז ($9\text{–}14\text{ m}^2$):**
  - גובה תקרה אינטימי של **$2.60\text{–}2.75\text{ m}$** ($R_v \approx 0.72\text{–}0.85$) תומך בתחושת מוגנות (*Enclosure*), קשב ממוקד והירדמות מהירה.

### 2.2 מניעת זוויות חדות ובליטות מאיימות (*Acute Corner & Cortical Threat Avoidance*)
- במחקרי Vartanian נמצא כי חללים עם זוויות פנימיות חדות (**$< 75^\circ$**) או פינות עמודים חדות הבולטות לתוך נתיב ההליכה מפעילים את ה**אמיגדלה** (מנגנון זיהוי סכנה קדום) ומעלים רמות מתח, לעומת גיאומטריה אורתוגונלית נקייה או פינות מרוככות.

---

## 3. תיאוריות השיקום הקוגניטיבי ועמדת השליטה האמפירית
**מקורות**:
- Roger S. Ulrich (1984, 1991), *Stress Recovery Theory (SRT)* — "View through a window may influence recovery from surgery", *Science*.
- Rachel Kaplan & Stephen Kaplan (1989), *The Experience of Nature: A Psychological Perspective — Attention Restoration Theory (ART)*.
- Jay Appleton (1975), *The Experience of Landscape (Prospect-Refuge Theory)*.
- Gary W. Evans (Cornell University, 2003), "The Built Environment and Mental Health", *Journal of Urban Health*.

### 3.1 עמדת שליטה בשינה ובעבודה (*Empirical Command Position / Prospect & Refuge*)
תרגום מדעי של תיאוריית **מבט ומקלט (Prospect & Refuge)** להעמדת המיטה בחדר השינה ושולחן העבודה:
1. **גב מוגן (*Refuge*):** ראש המיטה וגב כיסא העבודה חייבים להישען על **קיר מלא ואטום** (ללא חלון נמוך או דלת מאחורי הגב).
2. **שדה ראייה לפתח הכניסה (*Prospect*):** מהמיטה או משולחן העבודה קיים קו ראייה ברור אל דלת הכניסה לחדר.
3. **אי-הצבה בציר התנועה הישיר (*Direct Door-Line Offset $\ge 60\text{ cm}$*):** המיטה אינה מוצבת בקו ישר מול דלת הכניסה לחדר (ובוודאי לא מול דלת חדר הרחצה/מסדרון), אלא בהיסט אלכסוני המאפשר פרטיות ויזואלית בעת פתיחת הדלת ומפחית דריכות לילית של מערכת העצבים הסימפתטית.

### 3.2 מבט משקם קשב (*ART Soft Fascination Sightline*)
- כדי לאפשר הרפיה של שריר העין (Ciliary muscle relaxation) ושיקום קשב ממוקד לאחר עבודה מול מסכים, מנקודת הישיבה העיקרית בסלון ומפינת העבודה קיים קו ראייה חופשי באורך **$\ge \mathbf{6.0\text{ m}}$** אל חלון חיצוני, שמיים או צמחייה במרפסת.

### 3.3 מיתון צפיפות פסיכולוגית במשפחות גדולות (*Evans Household Crowding Buffer*)
- מחקריו של פרופ' Gary Evans מראים כי מצוקה פסיכולוגית בדירה אינה נגרמת רק משטח כולל קטן, אלא מ**היעדר יכולת וויסות אינטראקציה חברתית**.
- בדירות המיועדות ל-**$\ge 5$ נפשות** (דירות 4–5 חדרים ומעלה), מומלץ לתכנן **אזור שהייה משני** (פינת משפחה / הול מרכזי רחב *Hallenwohnung* / גינת חורף סגורה / חדר עבודה שקט) המאפשר לשני מעגלי פעילות (למשל: אירוח או צפייה בטלוויזיה בסלון מול הכנת שיעורים או שיחת טלפון שקטה) להתקיים בו-זמנית ללא הפרעה הדדית.
