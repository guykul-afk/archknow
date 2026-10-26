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
| הנחיות פיקוד העורף לתכנון ממ"ד (כולל תיקון 163 לחדר רטוב 2025) | פקע"ר / כנסת ישראל | ✅ | `B1.15`, `ACADEMIC_ARCH_COMPENDIUM` (9.0 מ"ר נטו + עד 3.0 מ"ר חדר רטוב פנימי) |
| ת"י 1918 — נגישות הסביבה הבנויה (כל החלקים) | מכון התקנים | 🟡 | `IS1918_ACCESS` — מבנה בלבד, ערכי ייחוס בינלאומיים |
| ת"י 5281 — בנייה בת-קיימא (בנייני מגורים + מדריכים טכניים) | מכון התקנים / המשרד להגנת הסביבה | ✅ | `DAYLIGHT_VENT_IEQ`, `CHECKLIST_ISRAEL_INT` — פרקי אור יום, אוורור ובריאות ורווחה |
| ת"י 6210 — אוורור בנייני מגורים | מכון התקנים | 🟡 | `DAYLIGHT_VENT_IEQ` — עקרונות אוורור חדרים רטובים ומטבחים |
| ת"י 1045 — בידוד תרמי של בניינים | מכון התקנים | ⬜ | ערכי התנגדות תרמית לפי אזורי אקלים |
| ת"י 1004 — אקוסטיקה בבניינים (חלקים 1–4) | מכון התקנים | ✅ | `USABILITY_FURNISH_HQI`, `ACADEMIC_ARCH_COMPENDIUM` ($\ge 48\text{ dB}$ בקיר מפריד) |
| ת"י 1142 — מעקים ומסעדים | מכון התקנים | ✅ | `ACADEMIC_ARCH_COMPENDIUM` (גובה מרפסת $\ge 105\text{ cm}$, מדרגות $\ge 90\text{ cm}$, מרווח $\le 10\text{ cm}$) |
| אוגדן הנחיות לעבודות תכנון (פרק בינוי ופרוגרמות דיור) | משרד הבינוי והשיכון | ✅ | `ACADEMIC_ARCH_COMPENDIUM` (חדר רגיל $\ge 9\text{ m}^2 / 2.80\text{ m}$, הורים $\ge 11\text{ m}^2 / 2.90\text{ m}$) |
| כלי המדידה "שכונה 360°" (גרסה 2.0) | משרד הבינוי והשיכון / המועצה לבנייה ירוקה | 🟡 | ממשק בניין-סביבה, מיקרו-אקלים, רוחות והצללה |
| המדריך לתכנון בתי דיור לגיל הזהב | משרד הבינוי והשיכון | ⬜ | רלוונטי ל-Aging in Place |
| תדריך ארצי לתמהיל יחידות דיור | מינהל התכנון | ⬜ | ברמת תוכנית / שכונה |
| הנחיות לתכנון חניונים וחניית נכים (פרק ד') | משרד התחבורה | ✅ | `ACADEMIC_ARCH_COMPENDIUM` (רוחב תא $2.40\text{ m}$, ליד עמוד $2.65\text{–}2.90\text{ m}$, מיסעה $5.50\text{–}6.00\text{ m}$) |
| הנחיות מרחביות — ועדה מקומית תל אביב-יפו | עיריית ת"א-יפו | ⬜ | דוגמה להנחיות מרחביות מכוח סעיף 145ד' |

## ב. מסגרות איכות דיור, שימושיות וקיימות בינלאומיות

| מקור | גוף | סטטוס | קובץ |
| :--- | :--- | :---: | :--- |
| NSW Apartment Design Guide (2015) | NSW Government (אוסטרליה) | ✅ | `CHECKLIST_ISRAEL_INT`, `WBS_NDSS_ADG` |
| Nationally Described Space Standard (2015) | DCLG (בריטניה) | ✅ | `WBS_NDSS_ADG` |
| London Plan 2021, Policy D6 + Housing Design Standards LPG (2023) | Greater London Authority | ✅ | `WBS_NDSS_ADG` (D6) |
| Housing Quality Indicators — HQI (Version 4) | Homes England (בריטניה) | ✅ | `USABILITY_FURNISH_HQI` — איזון פרוגרמטי (שטח ציבורי מול מספר מיטות) |
| Boverket BBR (*Möblerbarhet*) & SINTEF Byggforskserien | Boverket (שוודיה) / SINTEF (נורווגיה) | ✅ | `USABILITY_FURNISH_HQI` — יכולת ריהוט ואורך קירות רציפים |
| Lifetime Homes Standard (16 Criteria) & UK Approved Document M4(2) | JRF / Habinteg / UK Gov | ✅ | `USABILITY_FURNISH_HQI` — מרווחי גישה לדלתות, מסדרונות והתאמה למעגל החיים |
| EU Level(s) Framework — Indicator 2.3 (Adaptability) & Macro-Objective 4 | European Commission (JRC) | ✅ | `USABILITY_FURNISH_HQI` — יחס מחיצות פריקות וגמישות עתידית |
| Wohnungs-Bewertungs-System WBS (2015) | BWO (שווייץ) | 🟡 | `WBS_NDSS_ADG`, `USABILITY_FURNISH_HQI` — עקרונות יכולת ריהוט ורב-שימושיות |
| Building for a Healthy Life (2020) | Homes England / NHS England | ⬜ | 12 שיקולים ברמת שכונה ורחוב |
| Davos Baukultur Quality System (2021) | Swiss Federal Office of Culture | 🟡 | 8 קריטריונים — משמש כמסגרת ב-`qualitative_analyzer.py` |
| Active Design Guidelines & Fitwel Standard | NYC DDC / Center for Active Design | 🟡 | עידוד תנועה, מדרגות מוארות ואחסון אופניים/עגלות |
| *Growing Up: Planning for Children in New Vertical Communities* (2020) | City of Toronto | ✅ | `ACADEMIC_ARCH_COMPENDIUM` — שטחי דירות משפחתיות (87/100 מ"ר), מבואת כניסה וכביסה |
| *High-Density Housing for Families with Children Guidelines* | City of Vancouver | ✅ | `ACADEMIC_ARCH_COMPENDIUM` — אחסון ציוד גדול ($\ge 5.7\text{ m}^3$), קשר עין הורי וחדר רחצה משפחתי |
| Japanese *San-ten Bunri* (三点分離) & *Genkan* Standards | JASS / Japan Housing | ✅ | `ACADEMIC_ARCH_COMPENDIUM` — הפרדה משולשת של חלל רטוב (WC, כיור, מקלחת) ומבואת כניסה |

## ג. תאורה, אוורור, אקלים פנים וביופיליה (Daylight, Ventilation & IEQ)

| מקור | גוף | סטטוס | קובץ |
| :--- | :--- | :---: | :--- |
| EN 17037:2018+A1:2021 — *Daylight in Buildings* | CEN (האיחוד האירופי) | ✅ | `DAYLIGHT_VENT_IEQ` — אור יום, איכות מבט החוצה (View Out), שמש וסנוור |
| BRE Report BR 209 — *Site Layout Planning for Daylight and Sunlight* (2022) | BRE (בריטניה) | ✅ | `DAYLIGHT_VENT_IEQ` — קו השמיים (No-Sky Line ≥ 80%) וזווית הסתרה 25° |
| CIBSE AM10 (*Natural Ventilation*) & CIBSE TM59 (*Overheating Risk in Homes*) | CIBSE (בריטניה) | ✅ | `DAYLIGHT_VENT_IEQ` — יחסי עומק/גובה לאוורור חד-צדדי (2H/2.5H) ומפולש (5H), וסיכון התחממות יתר |
| WELL Building Standard v2 (Light L01–L09 & Air A01–A06) | IWBI | ✅ | `DAYLIGHT_VENT_IEQ` — מרחק מחלון לתאורה צירקדית (4.5–7.5 מ') ואיכות אוויר |
| ASHRAE Standard 62.2 & EN 16798-1 | ASHRAE / CEN | ✅ | `DAYLIGHT_VENT_IEQ` — אוורור מגורים, פליטת אדים במטבח וחדרים רטובים |
| IES LM-83-23 (sDA & ASE — Spatial Daylight Autonomy / Annual Sunlight Exposure) | IES | ✅ | `DAYLIGHT_VENT_IEQ` — סיכון סנוור וחימום יתר בחזיתות מערביות/דרומיות |
| *14 Patterns of Biophilic Design* (2014) | Terrapin Bright Green | ✅ | `DAYLIGHT_VENT_IEQ` — קשר עין לטבע, אור דינמי, ומבט רחוק ומקלט (Prospect & Refuge) |
| CBE Occupant IEQ Survey & BUS Methodology (POE) | UC Berkeley / Arup | ✅ | `USABILITY_FURNISH_HQI` — ממצאי POE על חיץ אקוסטי פנימי ופרטיות ויזואלית |

## ד. ארגונומיה, נגישות ומידות

| מקור | סטטוס | קובץ |
| :--- | :---: | :--- |
| Ernst & Peter Neufert, *Architects' Data* | 🟡 | `N.*` (85 קבצים — חילוץ חלקי) |
| *Metric Handbook: Planning and Design Data* (Adler / Littlefield) | 🟡 | `MH.*` (214 קבצים — חילוץ חלקי) |
| NKBA Kitchen & Bath Planning Guidelines | ✅ | `NKBA_KB` |
| DIN 18040-2 (*Barrierefreies Bauen — Wohnungen*) & SIA 500 (*Hindernisfreie Bauten*) | ✅ | `USABILITY_FURNISH_HQI` — מרווחי תמרון, צד ידית דלת (60/30 ס"מ) ומרווח לצד מיטה (90/120 ס"מ) |
| ISO 21542:2021 — Accessibility and usability of the built environment | 🟡 | `IS1918_ACCESS` (ערכי ייחוס) |
| EN 81-70 — Accessibility to lifts | 🟡 | `IS1918_ACCESS` (תא מעלית) |
| Julius Panero & Martin Zelnik, *Human Dimension & Interior Space* (1979) | ⬜ | אנתרופומטריה לפי אחוזונים |

## ה. תיאוריה אדריכלית, בתי ספר לאדריכלות, מגזינים ואדריכלים מובילים

| מקור | סטטוס | קובץ |
| :--- | :---: | :--- |
| Christopher Alexander et al., *A Pattern Language* (1977) | ✅ | `APL_HOUSING` (29 תבניות) |
| Bill Hillier & Julienne Hanson, *The Social Logic of Space* (1984) | ✅ | `SPACE_SYNTAX_SAGA` |
| N. John Habraken, *Supports: An Alternative to Mass Housing* (1961/1972) | ✅ | עקרון Support/Infill ב-`USABILITY_FURNISH_HQI` וב-`qualitative_analyzer.py` |
| Dietmar Eberle & Susanne Schmid (ETH Zürich), *Raumhaltigkeit* & *Hallenwohnung* | ✅ | `ACADEMIC_ARCH_COMPENDIUM` — ריבוד קונצנטרי, עומק מבנה ודירת הול מרכזי |
| Xavier Monteys & Pere Fuertes (ETSAB *Habitar*), *Casa Collage* & MAIO (Anna Puigjaner) | ✅ | `ACADEMIC_ARCH_COMPENDIUM` — חדרים גנריים שווי-גודל ($3.60 \times 3.60\text{ m}$), קירות מרוהטים |
| Herman Hertzberger & Bernard Leupen (TU Delft), *Lessons for Students* & *Polyvalence* | ✅ | `ACADEMIC_ARCH_COMPENDIUM`, `USABILITY_FURNISH_HQI` — אזור הסף (*In-Between*), מטבח חצי-פתוח |
| Oliver Heckmann & Friederike Schneider, *Floor Plan Manual Housing* (Birkhäuser) | ✅ | `ACADEMIC_ARCH_COMPENDIUM` — טיפולוגיות תוכנית ומערכות תנועה |
| Edition Hochparterre & *Werk, Bauen + Wohnen*, *Grundrissfibel* (Swiss Competitions) | ✅ | `ACADEMIC_ARCH_COMPENDIUM` — *Durchwohnen*, *Schaltzimmer*, מבחן האלכסון הראשי |
| Lacaton & Vassal (Pritzker 2021) & Frédéric Druot, *Plus* (Winter Gardens & Loggias) | ✅ | `ACADEMIC_ARCH_COMPENDIUM` — גינת חורף אקלימית בעומק $3.00\text{–}3.80\text{ m}$ ונגישות מכל חדר |
| Francis D.K. Ching, *Architecture: Form, Space, and Order* | 🟡 | יחסי מסלול-חלל (`SS-5`) |
| Steen Eiler Rasmussen, *Experiencing Architecture* (1959) | ⬜ | תפיסה חושית של חלל |
| Juhani Pallasmaa, *The Eyes of the Skin* (1996) | ⬜ | פנומנולוגיה |

## ו. מחקר חישובי ומאגרי תוכניות לכיול (Open Benchmark Datasets)

| מקור | סטטוס | הערה |
| :--- | :---: | :--- |
| Herthogs et al., "The SAGA Method", *Buildings* 9(4), 2019 | 🟡 | המנוע מממש מדדי קירוב + יחס מחיצות פריקות מ-EU Level(s) |
| Benedikt (1979); Turner et al. (2001) — Isovists / VGA | 🟡 | מתועד; משולב עם Prospect & Refuge ב-`DAYLIGHT_VENT_IEQ` |
| Swiss Dwellings / MSD (van Engelenburg et al., ECCV 2024) | ⬜ | לכיול רפי היוריסטיקה (`EF-1`, `EF-2`, `SS-1`) |
| CubiCasa5K (Kalervo et al., SCIA 2019 — 5,000 Nordic SVG Floorplans) | ⬜ | מאגר וקטורי מפינלנד הכולל ריהוט וכלים סניטריים — לכיול *Möblerbarhet* |
| ZInD — Zillow Indoor Dataset (Cruz et al., CVPR 2021) | ⬜ | תוכניות קומה מפורטות עם פתחים וחלונות לכיול יחסי חלון/עומק |
| RPLAN (Wu et al., ACM TOG 2019) & LIFULL HOME'S Dataset | ⬜ | לכיול גרפי קשרים (Adjacency Graphs) |

---

## סדר עדיפויות מומלץ להמשך
1. **ת"י 1918** (נוסח רשמי מלא) — כדי להפוך את `IS1918_ACCESS` מ-`WARN` לבדיקה סטטוטורית מחייבת.
2. **הנחיות משרד התחבורה לחניונים** — לבדיקה אוטומטית של תאי חניה ומיסעות בקומות מרתף/מגרש.
3. **כיול אמפירי של רפי `EF-1` / `EF-2` ו-`USABILITY_FURNISH_HQI`** על מאגרי **CubiCasa5K** ו-**Swiss Dwellings**.
