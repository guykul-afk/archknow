---
category: Computational Plan Analysis
indicator: Space Syntax configurational metrics, plan efficiency and SAGA-inspired adaptability proxies
rule_id: SPACE_SYNTAX_SAGA
type: standard_compendium
engine_usage: validation_engine.run_advanced_checks (topology, corridor ratio, rectangularity)
verification_status: Space Syntax formulas per Hillier & Hanson (1984). Corridor-ratio and rectangularity thresholds are archknow heuristics (to be calibrated on a reference set of plans). SAGA metrics in the engine are simplified proxies, not the published SAGA algorithm.
corridor_ratio_good_max: 0.10
corridor_ratio_warn_max: 0.15
rectangularity_min: 0.85
topology_min_coverage: 0.70
private_room_min_depth: 2
---
# ניתוח תצורה מרחבית (Space Syntax), יעילות תוכנית וגמישות (SAGA)

## 1. Space Syntax — הלוגיקה החברתית של החלל
**מקורות**:
- Bill Hillier & Julienne Hanson, *The Social Logic of Space*, Cambridge University Press, 1984.
- Bill Hillier, *Space is the Machine*, Cambridge University Press, 1996.
- Michael Benedikt, "To take hold of space: isovists and isovist fields", *Environment and Planning B*, 6(1), 1979.
- Alasdair Turner, Maria Doxa, David O'Sullivan & Alan Penn, "From isovists to visibility graphs", *Environment and Planning B*, 28(1), 2001.

### 1.1 ייצוג: גרף עומק מוצדק (Justified Plan Graph)
- כל חדר = **צומת**; כל דלת או פתח מעבר = **קשת**.
- צומת השורש (*Carrier*) = **החוץ** (חדר המדרגות / הלובי הקומתי). במנוע: הצומת `__EXT__`, המחובר לחדרים שהקשת שלהם בשדה `topology` מסומנת `ENTRANCE` / `EXT`, או לחדר שבשדה `entrance_room_id`.
- **עומק** (*Depth*) של חדר = מספר הקשתות המינימלי מהשורש.

### 1.2 נוסחאות
עבור גרף עם $k$ צמתים, ועבור צומת $i$:

$$MD_i = \frac{\sum_j d_{ij}}{k-1} \qquad RA_i = \frac{2\,(MD_i - 1)}{k-2}$$

$$D_k = \frac{2\left[k\left(\log_2\frac{k+2}{3} - 1\right) + 1\right]}{(k-1)(k-2)} \qquad RRA_i = \frac{RA_i}{D_k} \qquad I_i = \frac{1}{RRA_i}$$

- $MD$ — עומק ממוצע; $RA$ — אסימטריה יחסית; $RRA$ — אסימטריה יחסית "אמיתית" (מנורמלת לגודל הגרף ע"י ערך היהלום $D_k$); $I$ — **אינטגרציה**.
- אינטגרציה גבוהה = חלל מרכזי ונגיש (צומת תנועה). אינטגרציה נמוכה = חלל מבודד ופרטי.

### 1.3 חוקים הנגזרים מהתיאוריה (נבדקים במנוע)
| מזהה | חוק | בסיס |
| :--- | :--- | :--- |
| `SS-1` | הסלון / המטבח / פינת האוכל יהיו בין החללים **המשולבים ביותר** בדירה; חדר שינה בעל אינטגרציה גבוהה מהסלון מעיד שהוא משמש כמעבר. | Hillier & Hanson 1984; `APL#129` |
| `SS-2` | עומק כל חדר שינה ≥ **2**, ועמוק יותר מהסלון (מדרג פרטיות). | `APL#127`, `B5` |
| `SS-3` | הכניסה לא תוביל ישירות לחלל הציבורי ללא מבואה. | `B1.2`, `APL#112`, `APL#130` |
| `SS-4` | חדר רחצה / שירותים לא ייפתח ישירות לסלון, למטבח או לפינת האוכל. | `C1`, `ISRAEL_2026` פרק 3 |
| `SS-5` | חדר שינה לא ישמש מעבר לחדר אחר (פרט לחדר רחצה צמוד, ארון או מרפסת). | Ching — *Pass-through spaces* |
| `SS-6` | מספר מעגלי התנועה (Loops) $= E - V + C$ מדווח כמדד לחופש תנועה. | `APL#131`; SAGA (proxy) |

### 1.4 ניתוח שדה ראייה (Isovist / VGA) — שלב עתידי
דורש פוליגונים מלאים של החדרים ומיקומי פתחים. מדדים מתוכננים: אחוז שטח הסלון הנחשף מדלת הכניסה; האם נחשפים אסלה או חדר שינה מהכניסה; אורך קו הראייה המקסימלי מהכניסה אל חלון ("מבט רחוק", פרק 4.2 ב-`ISRAEL_2026`).

---

## 2. יעילות תוכנית (Plan Efficiency)
| מזהה | מדד | נוסחה | רף |
| :--- | :--- | :--- | :--- |
| `EF-1` | **יחס שטחי מעבר** | $\sum A_{corridor} / A_{apartment}$ | ≤ 10% טוב · 10–15% `WARN` · > 15% `WARN` חמור |
| `EF-2` | **מלבניות חדר** | $A_{room} / A_{min\,bounding\,rectangle}$ | ≥ 0.85 (חדר "משונן" או טרפזי מתחת לרף) |

- `EF-1` ממחיש את `APL#132` (Short Passages) ואת פרק 3.2 ב-`ISRAEL_2026`.
- `EF-2` ממחיש את `APL#191` ואת עיקרון יכולת הריהוט של WBS. המלבן החוסם המינימלי מחושב ע"י סיבוב על צלעות המעטפת הקמורה (Rotating calipers).

> [!WARNING]
> הרפים של `EF-1` ו-`EF-2` הם **היוריסטיקה של archknow** ולא תקן רשמי. יש לכייל אותם על מדגם תוכניות ייחוס (למשל מאגר Swiss Dwellings) לפני שימוש בהם כקריטריון מחייב.

---

## 3. SAGA — גמישות והתאמה של תוכנית
**מקור**: Pieter Herthogs et al., "Quantifying the Generality and Adaptability of Building Layouts Using Weighted Graphs: The SAGA Method", *Buildings*, 9(4), 2019.

- השיטה המקורית מגדירה שני ממדים: **Generality** — כמה תרחישי שימוש שונים התוכנית מסוגלת להכיל כפי שהיא; **Adaptability** — כמה בקלות ניתן לשנות את התוכנית כדי להכיל תרחישים נוספים. החישוב מתבסס על **גרפים משוקללים** של התוכנית ושל תרחישי השימוש.
- **המנוע אינו מממש את אלגוריתם SAGA המלא.** הוא מדווח שני מדדי קירוב (proxy) בלבד:
  1. **מספר מעגלי התנועה** בגרף (`SS-6`) — יותר מעגלים = יותר חופש בשימוש.
  2. **מיקום רכיבים קשיחים** — ממ"ד (בטון מזוין, אינו ניתן להריסה) שממוקם **בין** שני חדרי שינה חוסם איחוד עתידי שלהם. נבדק איכותנית ב-`qualitative_analyzer.py`.

> [!NOTE]
> **תיקון לתיאור קודם**: בסקירה הקודמת תואר מדד ה-Generality של SAGA כ"אחוז הקשתות הקיימות מתוך החיבורים האפשריים". זה תיאור לא מדויק של השיטה המקורית; התיאור בסעיף זה הוא הנכון.

---

## 4. מאגרי ייחוס לכיול (Benchmark Datasets)
- **Swiss Dwellings** (Archilyse / ETH Zürich) ו-**MSD — Modified Swiss Dwellings** (Casper van Engelenburg et al., 2024): תוכניות דירות שוויצריות וקטוריות עם גרפי מעבר. מתאים לכיול רפי `EF-1`, `EF-2` ו-`SS-1`.
- **RPLAN** (Wu et al., *ACM TOG* 2019): כ-80,000 תוכניות דירה (סין) עם תוויות חדרים.

---

## 5. קלט נדרש למנוע
```json
{
  "entrance_room_id": "R1",
  "topology": [
    {"source": "EXT", "target": "R1", "type": "door"},
    {"source": "R1", "target": "R2", "type": "opening"},
    {"source": "R2", "target": "R3", "type": "door"}
  ],
  "rooms": [
    {"id": "R1", "type": "entrance", "area_sqm": 3.2,
     "polygon": [[0,0],[1.6,0],[1.6,2.0],[0,2.0]]}
  ]
}
```
- אם פחות מ-70% מהחדרים מופיעים בגרף, המנוע **אינו מחשב** מדדי תצורה (כדי לא לדווח מספרים מטעים) ומחזיר `WARN` על טופולוגיה חסרה.
