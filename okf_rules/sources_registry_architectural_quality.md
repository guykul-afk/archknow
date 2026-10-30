---
category: Knowledge Governance
indicator: Registry of authoritative sources for architectural & housing design quality
rule_id: SOURCES_REGISTRY
type: knowledge_registry
---
# מרשם מקורות — איכות אדריכלית ואיכות תכנון דיור (9 בסיסי ידע משולבים)

המרשם מתעד כל מקור מופת / מקור רשמי ששולב במנוע הבקרה של **ArchiCheck**, ואת **סטטוס השילוב** שלו ב-9 בסיסי הידע של המערכת.

**מקרא סטטוס**
- ✅ **שולב במלואו** — ערכים כמותיים ואיכותניים הוטמעו ב-`okf_rules` וב-`architect_review_builder.py` ומוצגים בדו״ח ובממשק.
- 🟡 **שולב חלקית / לאימות** — מבנה או עקרונות שולבו; ערכים דורשים אימות מול נוסח המקור.

---

## א. ישראל — רגולציה, תקינה, בטיחות ומדיניות מרחבית (`KB_ISRAELI_STATUTORY` · `KB_URBAN_LOCAL` · `KB_ACOUSTICS_MEP`)

| מקור | גוף | סטטוס | קובץ בבסיס הידע / הערה |
| :--- | :--- | :---: | :--- |
| תקנות התכנון והבנייה (בקשה להיתר, תנאיו ואגרות), התשע"ו-2016 | מדינת ישראל | ✅ | `ISRAEL_2026`, `CHECKLIST_ISRAEL_INT`, `B1.*`, `KB_ISRAELI_STATUTORY` |
| הנחיות פיקוד העורף לתכנון ממ"ד (כולל תיקון 163 לחדר רטוב 2025) | פקע"ר / כנסת ישראל | ✅ | `B1.15`, `KB_ISRAELI_STATUTORY` ($9.0\text{ m}^2$ נטו + רציפות קירות $70\%$) |
| ת"י 1918 — נגישות הסביבה הבנויה (חלקים 1–4) | מכון התקנים | ✅ | `IS1918_ACCESS`, `KB_ISRAELI_STATUTORY` — מעגל תמרון $150\text{ cm}$, מעברים ושיפועים |
| ת"י 5281 ו-ת"י 5282 — בנייה בת-קיימא ודירוג אנרגטי לבנייני מגורים | מכון התקנים / המשרד להגנת הסביבה | ✅ | `DAYLIGHT_VENT_IEQ`, `KB_DAYLIGHT_IEQ` — אור יום, אוורור, הצללה ובריאות ורווחה |
| ת"י 6210 — אוורור בנייני מגורים | מכון התקנים | ✅ | `DAYLIGHT_VENT_IEQ`, `KB_DAYLIGHT_IEQ` — אוורור חדרים רטובים ומטבחים |
| ת"י 1045 — בידוד תרמי של בניינים (אזורי אקלים א'–ד') | מכון התקנים | ✅ | `KB_DAYLIGHT_IEQ` — גשרי קור בארגזי תריס/קירות ממ"ד ואיזון יחס זיגוג WWR |
| ת"י 1004 — אקוסטיקה בבניינים (חלקים 1–4) + זונינג אקוסטי פנימי | מכון התקנים | ✅ | `USABILITY_FURNISH_HQI`, `KB_ACOUSTICS_MEP` ($\ge 48\text{ dB}$ בקיר מפריד + ארון חוצץ סלון↔שינה) |
| ת"י 1142 — מעקים ומסעדים | מכון התקנים | ✅ | `ACADEMIC_ARCH_COMPENDIUM`, `KB_ISRAELI_STATUTORY` (גובה מרפסת $\ge 105\text{ cm}$, מדרגות $\ge 90\text{ cm}$) |
| ת"י 2481 — מעליות (חלק 70: נגישות ומפתח תא) | מכון התקנים | ✅ | `KB_ISRAELI_STATUTORY` — תא מעלית, יחס מעליות לדירות ורוחב מבואת המתנה ($\ge 150\text{ cm}$) |
| ת"י 1205 (מתקני תברואה) ותקנות הל"ת (הוראות למתקני תברואה) | מכון התקנים / משרד הפנים | ✅ | `KB_ACOUSTICS_MEP` — מיקום קולטנים $4''$, מרחק אסלה מקולטן ($\le 3.0\text{ m}$) והלימה אנכית של חדרים רטובים בין קומות |
| תקנות שירותי כבאות והצלה (חלק ג' — בטיחות אש בבניינים) | הרשות הארצית לכבאות והצלה | ✅ | `KB_ISRAELI_STATUTORY` — מרחקי מילוט לחדר מדרגות מוגן, פרוזדור מילוט ושחרור עשן |
| אוגדן הנחיות לעבודות תכנון (פרק בינוי ופרוגרמות דיור) | משרד הבינוי והשיכון | ✅ | `ACADEMIC_ARCH_COMPENDIUM`, `KB_INTL_HOUSING` (חדר רגיל $\ge 9\text{ m}^2 / 2.80\text{ m}$, הורים $\ge 11\text{ m}^2 / 2.90\text{ m}$) |
| כלי המדידה "שכונה 360°" (גרסה 2.0) | משרד הבינוי והשיכון / המועצה לבנייה ירוקה | ✅ | `KB_URBAN_LOCAL` — ממשק בניין-רחוב, מיקרו-אקלים, חלחול והצללה |
| המדריך לתכנון בתי דיור לגיל הזהב (Aging in Place / Downsizers) | משרד הבינוי והשיכון / ג'וינט אשל | ✅ | `KB_INTL_HOUSING`, `KB_ADAPTABILITY_FAMILY` — מקלחון Walk-in ללא סף, רצף נגישות למרפסת ודלתות חילוץ |
| תדריך ארצי לתמהיל יחידות דיור | מינהל התכנון | ✅ | `KB_URBAN_LOCAL` — איזון תמהיל דירות ופרוגרמת שטחים קומתית |
| הנחיות לתכנון חניונים וחניית נכים (פרק ד') | משרד התחבורה | ✅ | `KB_ISRAELI_STATUTORY` (רוחב תא $2.40\text{ m}$, ליד עמוד $2.65\text{–}2.90\text{ m}$, מיסעה $5.50\text{–}6.00\text{ m}$) |
| הנחיות מרחביות של ועדות מקומיות (סעיף 145ד' — ת"א-יפו, פתח תקווה, ר"ג) | ועדות מקומיות לתכנון ובנייה | ✅ | `KB_URBAN_LOCAL` — גובה ושקיפות לובי, אחוז חלחול בקרקע טבעית, מסתורי כביסה/VRF ונסיגות קומות גג |

---

## ב. מסגרות איכות דיור, גמישות תכנונית ומשפחות בינלאומיות (`KB_INTL_HOUSING` · `KB_ADAPTABILITY_FAMILY`)

| מקור | גוף | סטטוס | קובץ / בסיס ידע |
| :--- | :--- | :---: | :--- |
| NSW Apartment Design Guide (2015) | NSW Government (אוסטרליה) | ✅ | `CHECKLIST_ISRAEL_INT`, `WBS_NDSS_ADG`, `KB_INTL_HOUSING` |
| Nationally Described Space Standard (2015) | DCLG (בריטניה) | ✅ | `WBS_NDSS_ADG`, `KB_INTL_HOUSING` |
| London Plan 2021, Policy D6 + Housing Design Standards LPG (2023) | Greater London Authority | ✅ | `WBS_NDSS_ADG` (D6), `KB_INTL_HOUSING` |
| Housing Quality Indicators — HQI (Version 4) | Homes England (בריטניה) | ✅ | `USABILITY_FURNISH_HQI`, `KB_INTL_HOUSING` — איזון פרוגרמטי |
| Boverket BBR (*Möblerbarhet*) & SINTEF Byggforskserien | Boverket (שוודיה) / SINTEF (נורווגיה) | ✅ | `USABILITY_FURNISH_HQI`, `KB_ERGONOMICS_INTERIOR` — יכולת ריהוט ואורך קירות רציפים |
| Lifetime Homes Standard (16 Criteria) & UK Approved Document M4(2) | JRF / Habinteg / UK Gov | ✅ | `USABILITY_FURNISH_HQI`, `KB_ADAPTABILITY_FAMILY` — התאמה למעגל החיים |
| EU Level(s) Framework — Indicator 2.3 (Adaptability) & Macro-Objective 4 | European Commission (JRC) | ✅ | `USABILITY_FURNISH_HQI`, `KB_ADAPTABILITY_FAMILY` — יחס מחיצות פריקות וגמישות עתידית |
| Wohnungs-Bewertungs-System WBS (2015) | BWO (שווייץ) | ✅ | `WBS_NDSS_ADG`, `KB_INTL_HOUSING` — עקרונות יכולת ריהוט ורב-שימושיות |
| Building for a Healthy Life (2020) & Active Design / Fitwel | Homes England / NYC DDC | ✅ | `KB_URBAN_LOCAL` — ממשק רחוב, עידוד תנועה, מדרגות מוארות ואחסון אופניים/עגלות |
| Davos Baukultur Quality System (2021) | Swiss Federal Office of Culture | ✅ | `qualitative_analyzer.py`, `KB_URBAN_LOCAL` — 8 קריטריונים לתרבות הבנייה |
| *Growing Up: Planning for Children in New Vertical Communities* (2020) | City of Toronto | ✅ | `ACADEMIC_ARCH_COMPENDIUM`, `KB_ADAPTABILITY_FAMILY` — שטחי דירות משפחתיות, מבואת כניסה וכביסה |
| *High-Density Housing for Families with Children Guidelines* | City of Vancouver | ✅ | `ACADEMIC_ARCH_COMPENDIUM`, `KB_ADAPTABILITY_FAMILY` — אחסון ציוד גדול ($\ge 5.7\text{ m}^3$), קשר עין הורי וחדר רחצה משפחתי |
| Japanese *San-ten Bunri* (三点分離) & *Genkan* Standards | JASS / Japan Housing | ✅ | `ACADEMIC_ARCH_COMPENDIUM`, `KB_ERGONOMICS_INTERIOR`, `KB_SPACE_SYNTAX` — הפרדה משולשת של חלל רטוב ומבואת כניסה |

---

## ג. תאורה, אוורור, אקלים פנים, אקוסטיקה וביופיליה (`KB_DAYLIGHT_IEQ` · `KB_ACOUSTICS_MEP`)

| מקור | גוף | סטטוס | קובץ / בסיס ידע |
| :--- | :--- | :---: | :--- |
| EN 17037:2018+A1:2021 — *Daylight in Buildings* | CEN (האיחוד האירופי) | ✅ | `DAYLIGHT_VENT_IEQ`, `KB_DAYLIGHT_IEQ` — אור יום, איכות מבט החוצה (View Out), שמש וסנוור |
| BRE Report BR 209 — *Site Layout Planning for Daylight and Sunlight* (2022) | BRE (בריטניה) | ✅ | `DAYLIGHT_VENT_IEQ`, `KB_DAYLIGHT_IEQ` — קו השמיים (No-Sky Line $\ge 80\%$) וזווית הסתרה $25^\circ$ |
| CIBSE AM10 (*Natural Ventilation*) & CIBSE TM59 (*Overheating Risk in Homes*) | CIBSE (בריטניה) | ✅ | `DAYLIGHT_VENT_IEQ`, `KB_DAYLIGHT_IEQ` — יחסי עומק/גובה לאוורור חד-צדדי ($2H/2.5H$) ומפולש ($5H$) |
| WELL Building Standard v2 (Light L01–L09, Air A01–A06, Sound S01–S06) | IWBI | ✅ | `DAYLIGHT_VENT_IEQ`, `KB_DAYLIGHT_IEQ`, `KB_ACOUSTICS_MEP` — תאורה צירקדית וזונינג אקוסטי |
| ASHRAE Standard 62.2, EN 16798-1 & Residential VRF Duct Routing | ASHRAE / CEN | ✅ | `DAYLIGHT_VENT_IEQ`, `KB_ACOUSTICS_MEP` — אוורור ונתיבי הנמכות גבס למיזוג VRF ללא פגיעה בסלון |
| IES LM-83-23 (sDA & ASE — Spatial Daylight Autonomy / Annual Sunlight Exposure) | IES | ✅ | `DAYLIGHT_VENT_IEQ`, `KB_DAYLIGHT_IEQ` — סיכון סנוור וחימום יתר בחזיתות מערביות/דרומיות |
| *14 Patterns of Biophilic Design* (2014) | Terrapin Bright Green | ✅ | `DAYLIGHT_VENT_IEQ`, `KB_DAYLIGHT_IEQ` — קשר עין לטבע ומבט רחוק ומקלט (*Prospect & Refuge*) |
| CBE Occupant IEQ Survey & BUS Methodology (POE) | UC Berkeley / Arup | ✅ | `USABILITY_FURNISH_HQI`, `KB_ACOUSTICS_MEP` — ממצאי POE על חיץ אקוסטי פנימי ופרטיות ויזואלית |

---

## ד. ארגונומיה, אנתרופומטריה, נגישות ומידות (`KB_ERGONOMICS_INTERIOR`)

| מקור | סטטוס | קובץ / בסיס ידע |
| :--- | :---: | :--- |
| Ernst & Peter Neufert, *Architects' Data* | ✅ | `N.*`, `KB_ERGONOMICS_INTERIOR` |
| *Metric Handbook: Planning and Design Data* (Adler / Littlefield) | ✅ | `MH.*`, `KB_ERGONOMICS_INTERIOR` |
| NKBA Kitchen & Bath Planning Guidelines | ✅ | `NKBA_KB`, `KB_ERGONOMICS_INTERIOR` |
| DIN 18040-2 (*Barrierefreies Bauen — Wohnungen*) & SIA 500 (*Hindernisfreie Bauten*) | ✅ | `USABILITY_FURNISH_HQI`, `KB_ERGONOMICS_INTERIOR` — מרווחי תמרון, צד ידית דלת ($60/30\text{ cm}$) ומרווח לצד מיטה |
| Julius Panero & Martin Zelnik, *Human Dimension & Interior Space* (1979) | ✅ | `KB_ERGONOMICS_INTERIOR` — אנתרופומטריה לפי אחוזונים, מרווחי גישה למיטה, אי מטבח וארונות |

---

## ה. תיאוריה אדריכלית, בתי ספר לאדריכלות וביקורת תוכניות (`KB_SPACE_SYNTAX` · `KB_ADAPTABILITY_FAMILY`)

| מקור | סטטוס | קובץ / בסיס ידע |
| :--- | :---: | :--- |
| Christopher Alexander et al., *A Pattern Language* (1977) | ✅ | `APL_HOUSING`, `KB_SPACE_SYNTAX` (29 תבניות: *Intimacy Gradient*, *Light on Two Sides* וכו') |
| Bill Hillier & Julienne Hanson, *The Social Logic of Space* (1984) & SAGA | ✅ | `SPACE_SYNTAX_SAGA`, `KB_SPACE_SYNTAX` |
| N. John Habraken, *Supports: An Alternative to Mass Housing* (1961/1972) | ✅ | עקרון *Support/Infill* ב-`USABILITY_FURNISH_HQI` וב-`KB_ADAPTABILITY_FAMILY` |
| Dietmar Eberle & Susanne Schmid (ETH Zürich), *Raumhaltigkeit* & *Hallenwohnung* | ✅ | `ACADEMIC_ARCH_COMPENDIUM`, `KB_SPACE_SYNTAX` — ריבוד קונצנטרי, עומק מבנה ודירת הול מרכזי |
| Xavier Monteys & Pere Fuertes (ETSAB *Habitar*), *Casa Collage* & MAIO | ✅ | `ACADEMIC_ARCH_COMPENDIUM`, `KB_ADAPTABILITY_FAMILY` — חדרים שווי-ערך ($3.20\text{–}3.60\text{ m}$), קירות מרוהטים |
| Herman Hertzberger & Bernard Leupen (TU Delft), *Polyvalence* | ✅ | `ACADEMIC_ARCH_COMPENDIUM`, `KB_SPACE_SYNTAX` — אזור הסף (*In-Between*), מטבח חצי-פתוח |
| Oliver Heckmann & Friederike Schneider, *Floor Plan Manual Housing* (Birkhäuser) | ✅ | `ACADEMIC_ARCH_COMPENDIUM`, `KB_SPACE_SYNTAX` — טיפולוגיות תוכנית ומערכות תנועה |
| Edition Hochparterre & *Werk, Bauen + Wohnen*, *Grundrissfibel* (Swiss Competitions) | ✅ | `ACADEMIC_ARCH_COMPENDIUM`, `KB_SPACE_SYNTAX` — *Durchwohnen*, *Schaltzimmer*, מבחן האלכסון הראשי |
| Lacaton & Vassal (Pritzker 2021) & Frédéric Druot, *Plus* (Winter Gardens & Loggias) | ✅ | `ACADEMIC_ARCH_COMPENDIUM`, `KB_INTL_HOUSING` — מרפסות עמוקות ונגישות מכל חדר |
