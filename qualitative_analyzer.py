"""Qualitative design-review prompt generator (archknow v2).

Builds an LLM prompt that grounds a qualitative architectural review in:
  1. the apartment data (rooms + topology),
  2. the quantitative results from validation_engine (statutory FAILs, benchmark WARNs,
     Space Syntax metrics), so the LLM does not contradict computed facts,
  3. the relevant OKF knowledge files (rules + compendia: Pattern Language, Space Syntax,
     NKBA, NDSS/ADG/WBS, accessibility, Israeli planning book).

Usage:
  python qualitative_analyzer.py <apartment_or_project.json> [output_prompt.txt] [--apartment N]
"""
import json
import os
import sys

import yaml

from validation_engine import load_okf_rules, run_validation

# Review dimensions -> knowledge files that inform each one.
REVIEW_DIMENSIONS = [
    {
        "key": "entry_privacy",
        "title": "רצף כניסה, מבואה ופרטיות (Entrance Transition & Privacy)",
        "rules": ["B1.2", "B2", "C1", "APL_HOUSING", "SPACE_SYNTAX_SAGA"],
        "questions": [
            "האם דלת הכניסה נפתחת ישירות לחלל הציבורי, או שיש מבואה / שבירת מבט (APL#112, APL#130, B1.2)?",
            "האם חדרי רחצה או חדרי שינה נחשפים ממבט מהכניסה או מהסלון (C1, SS-4)?",
        ],
    },
    {
        "key": "zoning",
        "title": "מדרג אינטימיות והפרדת אגפים (Intimacy Gradient & Zoning)",
        "rules": ["B5", "APL_HOUSING", "SPACE_SYNTAX_SAGA"],
        "questions": [
            "האם רצף החללים מהכניסה עד חדרי השינה מבטא פרטיות עולה (APL#127, SS-2)?",
            "האם יש יחידת הורים מופרדת (APL#136) ותחום ילדים (APL#137)?",
        ],
    },
    {
        "key": "circulation",
        "title": "תנועה ומעברים (Circulation)",
        "rules": ["C4", "APL_HOUSING", "SPACE_SYNTAX_SAGA"],
        "questions": [
            "מה יחס שטחי המעבר (EF-1) ואורך המסדרונות? האם מסדרון ארוך מטופל כ'חדר' — חלון, נישה, מדפים (APL#132)?",
            "האם יש מעגלי תנועה (APL#131, SS-6) או שכל התנועה תלויה במעבר יחיד?",
            "האם חדר שינה משמש מעבר (SS-5)?",
        ],
    },
    {
        "key": "light_air",
        "title": "אור יום, מבט החוצה, כיווניות ואוורור (Daylight, View Out, Aspect & Ventilation)",
        "rules": ["A4", "A11", "A13", "APL_HOUSING", "WBS_NDSS_ADG", "DAYLIGHT_VENT_IEQ"],
        "questions": [
            "האם הדירה דו-כיוונית ומאפשרת אוורור צולב אפקטיבי (ADG 4B, CIBSE AM10 מסלול ≤ 5×H)? מה עומק החדרים ביחס לגובה התקרה (2.0×H / 2.5×H לאוורור חד-צדדי)?",
            "לאילו חדרים יש אור משני כיוונים (APL#159)? האם הסלון פונה לשמש (APL#128, EN 17037 ≥ 1.5–3.0 שעות) וחדרי השינה למזרח (APL#138)?",
            "מה איכות המבט החוצה מנקודות הישיבה (EN 17037 View Out — זווית מבט, מרחק ≥ 6/20 מ', שכבות נוף) והאם קיים סיכון סנוור/חימום יתר בחזית מערבית (CIBSE TM59 / IES ASE)?",
        ],
    },
    {
        "key": "kitchen_dining",
        "title": "מטבח, פינת אוכל ואירוח בדירה הישראלית",
        "rules": ["B11", "NKBA_KB", "APL_HOUSING", "DAYLIGHT_VENT_IEQ"],
        "questions": [
            "האם המטבח עומד בעקרונות NKBA (משולש עבודה, מעבר 107/122 ס\"מ, משטחי הנחה) והאם מיקום הכיריים מאפשר פליטת אדים ישירה (ASHRAE 62.2 / ת\"י 6210)? אם אין מידות — ציין זאת.",
            "האם פינת האוכל מאפשרת הארכת שולחן לאירוח של 10–14 סועדים עם מרווח 81–112 ס\"מ מאחורי הסועדים ונגישות לאור יום צירקדי (WELL L01 ≤ 4.5 מ')?",
            "האם המטבח משולב בחלל המשפחתי (APL#139)?",
        ],
    },
    {
        "key": "rooms_furnishing",
        "title": "גודל חדרים, איזון פרוגרמטי ויכולת ריהוט (Möblerbarhet & HQI)",
        "rules": ["B1.6", "B6", "WBS_NDSS_ADG", "SPACE_SYNTAX_SAGA", "USABILITY_FURNISH_HQI"],
        "questions": [
            "האם רוחב חדרי השינה ואורך הקירות הרציפים מאפשרים יותר מסידור ריהוט אחד (WBS, Boverket Möblerbarhet ≥ 3.0 מ' למיטה זוגית, ≥ 60 ס\"מ היסט דלת מפינת ארון)? השווה לחוק הישראלי (2.60 מ'), ל-NDSS ול-ADG (3.0 מ').",
            "האם קיים איזון פרוגרמטי (HQI Unit Layout) בין מספר המיטות/הדיירים בדירה לבין שטח הסלון והחלל הציבורי המשולב?",
            "האם יש חדרים לא-מלבניים או משוננים (EF-2, APL#191)?",
        ],
    },
    {
        "key": "outdoor_storage",
        "title": "מרפסת ואחסון",
        "rules": ["B7", "WBS_NDSS_ADG", "APL_HOUSING"],
        "questions": [
            "האם המרפסת היא 'חדר חוץ' שמיש — עומק ≥ 1.83 מ' (APL#167), ADG 4E, London D6?",
            "האם קיים אחסון ייעודי (B7, NDSS, ADG 4G, APL#145)? אם אין נתון — ציין זאת במפורש.",
        ],
    },
    {
        "key": "adaptability",
        "title": "גמישות ועמידות בזמן (Open Building / SAGA / EU Level(s))",
        "rules": ["C5", "C9", "SPACE_SYNTAX_SAGA", "USABILITY_FURNISH_HQI"],
        "questions": [
            "אילו רכיבים קשיחים (ממ\"ד, קירות נושאים, פירים) חוסמים שינוי עתידי, ומה יחס המחיצות הפריקות (EU Level(s) 2.3 ≥ 60%)? האם הממ\"ד ממוקם בין שני חדרים שאפשר היה לאחד?",
            "האם חדרים בגודל דומה ניתנים להחלפת תפקיד (שינה / עבודה / משחק)?",
        ],
    },
    {
        "key": "accessibility",
        "title": "נגישות, שימושיות והזדקנות במקום (Lifetime Homes / DIN 18040-2 / ת\"י 1918)",
        "rules": ["B44", "IS1918_ACCESS", "USABILITY_FURNISH_HQI"],
        "questions": [
            "האם קיים חדר רחצה שניתן להתאים (מעגל סיבוב Ø150), דלתות במעבר נטו 80 ס\"מ, ויציאה למרפסת ללא סף? (ערכי ייחוס — לאימות מול ת\"י 1918)",
            "האם מתקיימים מרווחי שימושיות אוניברסליים (DIN 18040-2 / SIA 500 / Lifetime Homes): מרווח 60 ס\"מ לצד ידית הדלת, מרווח 90–120 ס\"מ לצד מיטה ויחס תקין בין רוחב המסדרון לדלתות בניצב?",
        ],
    },
    {
        "key": "ieq_acoustics_biophilia",
        "title": "איכות סביבה פנים, חיץ אקוסטי וביופיליה (IEQ, POE Acoustics & Biophilic Design)",
        "rules": ["A6", "A8", "A10", "A17", "DAYLIGHT_VENT_IEQ", "USABILITY_FURNISH_HQI"],
        "questions": [
            "האם חדרי השינה מוגנים אקוסטית מחללים רועשים (סלון/טלוויזיה, מטבח, מעלית, מסתור כביסה) באמצעות מסדרון או חיץ ארונות (CBE POE / ת\"י 1004 / ת\"י 5281)?",
            "האם אזורי הישיבה והעבודה מקיימים את עיקרון 'מבט רחוק ומקלט' (Biophilic Prospect & Refuge — גב מוגן לקיר ומבט פתוח לחלון/כניסה) וקשר עין לטבע/מרפסת?",
        ],
    },
]

BAUKULTUR_CRITERIA = ["Governance", "Functionality", "Environment", "Economy",
                      "Diversity", "Context", "Sense of Place", "Beauty"]


def _read_rule_files(okf_rules_dir):
    """Return {rule_id: (filename, full_text)} parsing YAML frontmatter properly."""
    index = {}
    for filename in sorted(os.listdir(okf_rules_dir)):
        if not filename.endswith(".md") or filename == "index.md":
            continue
        with open(os.path.join(okf_rules_dir, filename), "r", encoding="utf-8") as f:
            content = f.read()
        if not content.startswith("---"):
            continue
        end = content.find("---", 3)
        if end == -1:
            continue
        try:
            meta = yaml.safe_load(content[3:end]) or {}
        except yaml.YAMLError:
            continue
        rid = meta.get("rule_id") if isinstance(meta, dict) else None
        if rid is not None:
            index[str(rid)] = (filename, content)
    return index


def _select_apartment(data, apartment_index=0):
    if "floors" in data:
        apts = [a for fl in data.get("floors", []) for a in fl.get("apartments", [])]
        if not apts:
            raise ValueError("Project file contains no apartments.")
        return apts[apartment_index]
    return data


def build_prompt(apartment, okf_rules_dir="okf_rules"):
    rules = load_okf_rules(okf_rules_dir)
    quantitative = run_validation(apartment, rules)
    rule_files = _read_rule_files(okf_rules_dir)

    wanted = []
    for dim in REVIEW_DIMENSIONS:
        for rid in dim["rules"]:
            if rid not in wanted:
                wanted.append(rid)
    missing = [rid for rid in wanted if rid not in rule_files]
    knowledge = "\n".join(
        f"\n### [{rid}] {rule_files[rid][0]}\n{rule_files[rid][1]}\n" for rid in wanted if rid in rule_files
    )

    fails = [r for r in quantitative if r["status"] == "FAIL"]
    warns = [r for r in quantitative if r["status"] == "WARN"]
    passes = [r for r in quantitative if r["status"] == "PASS"]
    q_lines = lambda rs: "\n".join(f"- [{r['rule_id']}] {r['element']}: {r.get('message', '')}" for r in rs) or "- (none)"

    dims_text = ""
    for i, dim in enumerate(REVIEW_DIMENSIONS, 1):
        qs = "\n".join(f"   - {q}" for q in dim["questions"])
        dims_text += f"{i}. **{dim['title']}** — rules: {', '.join(dim['rules'])}\n{qs}\n"

    return f"""You are a senior architect performing a qualitative design review of an apartment plan.
Write the review in professional Hebrew.

=========================================
GROUND RULES (ZERO-TRUST)
=========================================
- Base every statement on the APARTMENT DATA, the QUANTITATIVE RESULTS, or a cited KNOWLEDGE rule.
- The quantitative results were computed by code. Do NOT contradict them; interpret them.
- If the data needed for a question is missing, write "אין נתון" and state what data would be needed. Never invent dimensions.
- Cite rule IDs in square brackets, e.g. [B1.2], [APL#127], [SS-3], [NKBA_KB].
- Distinguish clearly between Israeli statutory requirements (FAIL = legal problem) and international benchmarks (WARN = below best practice, not illegal).
- Rules marked in the knowledge files as "לאימות" (unverified) must be presented as such.

=========================================
APARTMENT DATA (JSON)
=========================================
{json.dumps(apartment, indent=2, ensure_ascii=False)}

=========================================
QUANTITATIVE RESULTS (validation_engine)
=========================================
Statutory FAILs ({len(fails)}):
{q_lines(fails)}

Benchmark WARNs ({len(warns)}):
{q_lines(warns)}

PASS ({len(passes)}):
{q_lines(passes)}

=========================================
KNOWLEDGE RULES (OKF)
=========================================
{knowledge}
{"(Missing knowledge files: " + ", ".join(missing) + ")" if missing else ""}

=========================================
YOUR TASK
=========================================
For each dimension below give: (a) findings with evidence and rule citations, (b) a score 1–5
(5 = exemplary, 3 = acceptable, 1 = significant problem, or "N/A — אין נתון"), (c) one concrete,
buildable improvement that does not require moving structural walls or the safe room unless stated.

{dims_text}
Then:
- **סיכום מנהלים**: 3–5 שורות, ציון משוקלל, ושלושת השיפורים בעלי ההשפעה הגדולה ביותר.
- **פער נתונים**: רשימת הנתונים החסרים שמנעו בדיקה (למשל אחסון, מידות מטבח, טופולוגיה, כיווניות).
- (אופציונלי, אם יש נתוני בניין ומיקום) **Davos Baukultur**: הערה קצרה לכל אחד מ-8 הקריטריונים: {", ".join(BAUKULTUR_CRITERIA)}.
"""


def generate_llm_prompt(json_path, okf_rules_dir, output_prompt_path, apartment_index=0):
    """Backward-compatible entry point."""
    print("Generating LLM Qualitative Prompt...")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    apartment = _select_apartment(data, apartment_index)
    prompt = build_prompt(apartment, okf_rules_dir)
    with open(output_prompt_path, "w", encoding="utf-8") as f:
        f.write(prompt)
    print(f"Prompt successfully written to {output_prompt_path} ({len(prompt):,} chars)")
    return prompt


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    idx = 0
    if "--apartment" in sys.argv:
        idx = int(sys.argv[sys.argv.index("--apartment") + 1])
        args = [a for a in args if a != str(idx)]
    src = args[0] if args else "extracted_apartment.json"
    dst = args[1] if len(args) > 1 else "qualitative_prompt.txt"
    generate_llm_prompt(src, "okf_rules", dst, idx)
