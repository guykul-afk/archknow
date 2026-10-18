---
category: Knowledge Governance
indicator: Registry of authoritative sources for architectural & housing design quality
rule_id: SOURCES_REGISTRY
type: knowledge_registry
---
# מרשם מקורות — איכות אדריכלית ואיכות תכנון דיור

המרשם מתעד כל מקור מופת / מקור רשמי שהוצע לבסיס הידע, ואת **סטטוס השילוב** שלו. המטרה: לדעת בכל רגע מה בבסיס הידע מבוסס על נוסח מקור, מה מבוסס על מקור משני, ומה עדיין חסר.

**מקרא סטטוס**
- ✅ **שולב** — ערכים מספריים הוטמעו בקובץ `okf_rules` ונקראים ע"י המנוע.
- 🟡 **שולב חלקית / לאימות** — מבנה או עקרונות שולבו; ערכים דורשים אימות מול נוסח המקור.
- ⬜ **להשלמה** — מקור מומלץ שטרם שולב (בדרך כלל נדרשת רכישה או הורדה של המסמך).

---

## א. ישראל — רגולציה, תקינה ומדיניות

| מקור | גוף | סטטוס | קובץ בבסיס הידע / הערה |
| :--- | :--- | :---: | :--- |
| תקנות התכנון והבנייה (בקשה להיתר, תנאיו ואגרות), התשע"ו-2016 | מדינת ישראל | 🟡 | `ISRAEL_2026`, `CHECKLIST_ISRAEL_INT`, `B1.*` |
| הנחיות פיקוד העורף לתכנון ממ"ד | פקע"ר | 🟡 | `B1.15` במנוע (9.0 מ"ר / 2.60 מ'); לאמת מול המהדורה העדכנית |
| ת"י 1918 — נגישות הסביבה הבנויה (כל החלקים) | מכון התקנים | 🟡 | `IS1918_ACCESS` — מבנה בלבד, ערכי ייחוס בינלאומיים |
| ת"י 5281 — בנייה בת-קיימא (חלק בנייני מגורים) | מכון התקנים | ⬜ | נדרש נוסח התקן לטבלת הניקוד |
| ת"י 1045 — בידוד תרמי של בניינים | מכון התקנים | ⬜ | ערכי התנגדות תרמית לפי אזורי אקלים |
| ת"י 1004 — אקוסטיקה בבניינים | מכון התקנים | ⬜ | ערכי בידוד קול אווירי וקול הולם בין דירות |
| ת"י 1142 — מעקים ומסעדים | מכון התקנים | ⬜ | גובה מעקה ומרווחים |
| אוגדן הנחיות לעבודות תכנון | משרד הבינוי והשיכון | ⬜ | gov.il |
| המדריך לתכנון בתי דיור לגיל הזהב | משרד הבינוי והשיכון | ⬜ | רלוונטי ל-Aging in Place |
| תדריך ארצי לתמהיל יחידות דיור | מינהל התכנון | ⬜ | ברמת תוכנית / שכונה |
| הנחיות לתכנון חניונים וחניית נכים | משרד התחבורה | ⬜ | רוחב תאים, תוספת ליד עמוד/קיר, חניית נכים |
| הנחיות מרחביות — ועדה מקומית תל אביב-יפו | עיריית ת"א-יפו | ⬜ | דוגמה להנחיות מרחביות מכוח סעיף 145ד' |

## ב. מסגרות איכות דיור בינלאומיות

| מקור | גוף | סטטוס | קובץ |
| :--- | :--- | :---: | :--- |
| NSW Apartment Design Guide (2015) | NSW Government (אוסטרליה) | ✅ | `CHECKLIST_ISRAEL_INT`, `WBS_NDSS_ADG` |
| Nationally Described Space Standard (2015) | DCLG (בריטניה) | ✅ | `WBS_NDSS_ADG` |
| London Plan 2021, Policy D6 + Housing Design Standards LPG (2023) | Greater London Authority | ✅ | `WBS_NDSS_ADG` (D6) |
| Wohnungs-Bewertungs-System WBS (2015) | BWO (שווייץ) | 🟡 | `WBS_NDSS_ADG` — מבנה בלבד; נדרש ה-PDF לערכי ניקוד |
| Building for a Healthy Life (2020) | Homes England / NHS England | ⬜ | 12 שיקולים ברמת שכונה ורחוב |
| Davos Baukultur Quality System (2021) | Swiss Federal Office of Culture | 🟡 | 8 קריטריונים — משמש כמסגרת ב-`qualitative_analyzer.py` |
| WELL Building Standard v2 | IWBI | ⬜ | אור צירקדי, אקוסטיקה, אוויר |

## ג. ארגונומיה ומידות

| מקור | סטטוס | קובץ |
| :--- | :---: | :--- |
| Ernst & Peter Neufert, *Architects' Data* | 🟡 | `N.*` (85 קבצים — חילוץ חלקי) |
| *Metric Handbook: Planning and Design Data* (Adler / Littlefield) | 🟡 | `MH.*` (214 קבצים — חילוץ חלקי) |
| NKBA Kitchen & Bath Planning Guidelines | ✅ | `NKBA_KB` |
| Julius Panero & Martin Zelnik, *Human Dimension & Interior Space* (1979) | ⬜ | אנתרופומטריה לפי אחוזונים |
| ISO 21542:2021 — Accessibility and usability of the built environment | 🟡 | `IS1918_ACCESS` (ערכי ייחוס) |
| EN 81-70 — Accessibility to lifts | 🟡 | `IS1918_ACCESS` (תא מעלית) |

## ד. תיאוריה אדריכלית וקאנון

| מקור | סטטוס | קובץ |
| :--- | :---: | :--- |
| Christopher Alexander et al., *A Pattern Language* (1977) | ✅ | `APL_HOUSING` (29 תבניות) |
| Bill Hillier & Julienne Hanson, *The Social Logic of Space* (1984) | ✅ | `SPACE_SYNTAX_SAGA` |
| N. John Habraken, *Supports: An Alternative to Mass Housing* (1961/1972) | 🟡 | עקרון Support/Infill ב-`qualitative_analyzer.py` |
| Bernard Leupen, *Frame and Generic Space* (2006) | ⬜ | גמישות ו-Polyvalence |
| Francis D.K. Ching, *Architecture: Form, Space, and Order* | 🟡 | יחסי מסלול-חלל (`SS-5`) |
| Steen Eiler Rasmussen, *Experiencing Architecture* (1959) | ⬜ | תפיסה חושית של חלל |
| Juhani Pallasmaa, *The Eyes of the Skin* (1996) | ⬜ | פנומנולוגיה |

## ה. מחקר חישובי ומאגרי ייחוס

| מקור | סטטוס | הערה |
| :--- | :---: | :--- |
| Herthogs et al., "The SAGA Method", *Buildings* 9(4), 2019 | 🟡 | המנוע מממש מדדי קירוב בלבד |
| Benedikt (1979); Turner et al. (2001) — Isovists / VGA | 🟡 | מתועד; מימוש מתוכנן |
| Swiss Dwellings / MSD (van Engelenburg et al., ECCV 2024) | ⬜ | לכיול רפי היוריסטיקה |
| RPLAN (Wu et al., ACM TOG 2019) | ⬜ | לכיול |

---

## סדר עדיפויות מומלץ להשלמה
1. **ת"י 1918** (נוסח מלא) — כדי להפוך את `IS1918_ACCESS` מ-`WARN` לבדיקה סטטוטורית.
2. **הנחיות משרד התחבורה לחניונים** — כדי לבדוק חניות (ממצא פתוח בפינס 48).
3. **ת"י 1004 ו-ת"י 1045** — לאקוסטיקה ובידוד תרמי כמותיים.
4. **WBS (PDF של ה-BWO)** — לערכי ניקוד יכולת ריהוט.
5. **כיול רפי `EF-1` / `EF-2`** על מאגר Swiss Dwellings.
