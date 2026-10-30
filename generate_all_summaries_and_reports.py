# -*- coding: utf-8 -*-
"""
Generates and updates all Summary Documents of Audit Notes & Improvement Proposals
and Quantitative Project Data (Above-Ground Areas by Floor, Underground Areas,
Roof Terraces, Suspended Balconies, and Facades by Direction) across:
1. Standalone Markdown & HTML/PDF Summary Reports (`reports/<id>_summary_and_areas_report.md` & `.html`)
2. Full Markdown Audit Reports (`reports/<id>_architectural_quality_report.md`)
3. Full HTML & PDF Audit Reports (`reports/<id>_architectural_quality_analysis.html` & `.pdf`)
"""

import os
import re
from project_analyzer_service import (
    build_pines48_analysis,
    build_kkl10_analysis,
    build_hafetz44_analysis,
    build_yatkovski7_analysis,
    build_kitroni37_analysis,
    build_feierberg3_analysis,
    build_sharett26_analysis,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

MARKER_MD = "<!-- ARCHICHECK_SUMMARY_AND_AREAS_SECTION -->"
MARKER_HTML_START = "<!-- ARCHICHECK_SUMMARY_AND_AREAS_HTML_START -->"
MARKER_HTML_END = "<!-- ARCHICHECK_SUMMARY_AND_AREAS_HTML_END -->"


def fmt(val):
    if val is None:
        return "0"
    if isinstance(val, (int, float)):
        if float(val).is_integer():
            return f"{int(val):,}"
        return f"{val:,.2f}".rstrip("0").rstrip(".")
    return str(val)


def build_markdown_summary_and_areas_section(payload):
    """Builds the Markdown section for Summary of Notes, Proposals, and Quantitative Areas & Facades."""
    pds = payload.get("project_data_summary", {})
    ag = pds.get("above_ground_areas", {})
    ug = pds.get("underground_areas", {})
    rt = pds.get("roof_terraces", {})
    sb = pds.get("suspended_balconies", {})
    fac = pds.get("facades", {})
    flr = pds.get("flooring_areas", {})
    opt = pds.get("design_optimization", {})
    sdoc = pds.get("summary_document", {})
    notes = payload.get("notes", [])

    lines = [
        MARKER_MD,
        "",
        "---",
        "",
        f"# 📋 מסמך סיכום הערות והצעות לשיפור + 📐 נתוני פרויקט, שטחי בנייה, שטחי ריצוף, מרפסות וחזיתות — {payload.get('project_name')}",
        "",
        f"> **חוות דעת מסכמת:** {sdoc.get('overall_verdict', '')}",
        "",
        "## 1. תקציר מנהלים כמותי — נתוני פרויקט ושטחים מרכזיים",
        "",
        "| מדד כמותי בפרויקט | נתון מסכם | פירוט והערות הנדסיות |",
        "| :--- | :--- | :--- |",
        f"| **סך שטחי בנייה עיליים (ברוטו)** | **{fmt(ag.get('total_sqm'))} מ״ר** | שטחי דירות (פלדלת): **{fmt(ag.get('net_apartments_sqm'))} מ״ר** · ליבה ושירות עילי: **{fmt(ag.get('core_and_service_sqm'))} מ״ר** ({pds.get('floors_above_ground')} קומות) |",
        f"| **סך שטחי בנייה תת-קרקעיים** | **{fmt(ug.get('total_sqm'))} מ״ר** | {ug.get('parking_spaces')} חניות תת-קרקעיות ({ug.get('parking_ratio')}) |",
        f"| **סך שטח בנוי כולל (עילי + תת-קרקעי)** | **{fmt(pds.get('total_built_area_sqm'))} מ״ר** | {pds.get('buildings_count')} מבנים · {pds.get('apartments_count')} יח״ד · מגרש: {fmt(pds.get('lot_area_sqm'))} מ״ר |",
        f"| **סך שטחי מרפסות גג** | **{fmt(rt.get('total_sqm'))} מ״ר** | {rt.get('count')} מרפסות גג בפנטהאוזים/דופלקסים" + (f" (+ {fmt(rt.get('garden_terraces_sqm'))} מ״ר גינות צמודות בקרקע)" if rt.get("garden_terraces_sqm") else "") + " |",
        f"| **סך שטחי מרפסות תלויות (זיזיות)** | **{fmt(sb.get('total_sqm'))} מ״ר** | {sb.get('count')} מרפסות שמש זיזיות בקומות הטיפוסיות (+ {fmt(sb.get('service_balconies_sqm'))} מ״ר מרפסות שירות/כביסה) |",
        f"| **סך שטחי חזיתות החוץ** | **{fmt(fac.get('total_sqm'))} מ״ר** | גובה מבנה: {fmt(fac.get('building_height_m'))} מ׳ · פתחים וזיגוג: **{fmt(fac.get('total_glazing_sqm'))} מ״ר** ({fac.get('average_wwr_pct')}%) · אטום/חיפוי: **{fmt(fac.get('total_opaque_sqm'))} מ״ר** |",
        f"| **סך שטחי ריצוף דירות (נטו)** | **{fmt(flr.get('total_apartments_flooring_sqm'))} מ״ר** | ריצוף פנים יבש: **{fmt(flr.get('total_apartments_dry_sqm'))} מ״ר** · ריצוף חדרים רטובים (R10): **{fmt(flr.get('total_apartments_wet_sqm'))} מ״ר** |",
        f"| **סך שטחי ריצוף ציבורי (נטו)** | **{fmt(flr.get('total_public_flooring_sqm'))} מ״ר** | לובי ראשי, מבואות קומתיות, חדרי מדרגות, מועדון דיירים/עגלות ומחסנים מרוצפים |",
        f"| **סך שטחי ריצוף מרפסות (נטו)** | **{fmt(flr.get('total_balconies_flooring_sqm'))} מ״ר** | מרפסות שמש זיזיות, מרפסות שירות, מרפסות גג ומשטחי גן מרוצפים (R11) |",
        f"| **סה״כ שטחי ריצוף בפרויקט (קומות מלאות)** | **{fmt(flr.get('grand_total_flooring_sqm'))} מ״ר** | סך כל שטחי הרצפה המרוצפים נטו בפרויקט (דירות + ציבורי + מרפסות) |",
        f"| **סנכרון ובקרת מודל 3D בסיסי** | **חתימה `#{payload.get('model_3d_sync_status', {}).get('base_model_hash_short', 'מאומת')}`** | {payload.get('model_3d_sync_status', {}).get('status_message_he', 'המודל התלת-ממדי הבסיסי נבדק ומסונכרן 1:1 מול דוח הבקרה התכנונית')} |",
        "",
        "---",
        "",
        "## 2. סך שטחי בנייה עיליים — סך הכל וחלוקה מפורטת לקומות",
        "",
        f"*{ag.get('summary_note', '')}*",
        "",
        "| קומה | מפלס וגובה | יח״ד בקומה | פירוט שימושים ויחידות דיור | שטח דירות (פלדלת) | שטח ליבה ושירות | סה״כ שטח קומה ברוטו | % מהבנייה העילית |",
        "| :--- | :--- | :---: | :--- | :---: | :---: | :---: | :---: |",
    ]

    for f in ag.get("by_floor", []):
        lines.append(
            f"| **{f.get('floor_label')}** | `{f.get('elevation')}` | {f.get('units_count')} | {f.get('usage_description')} | {fmt(f.get('apartments_sqm'))} מ״ר | {fmt(f.get('core_service_sqm'))} מ״ר | **{fmt(f.get('total_floor_sqm'))} מ״ר** | {f.get('pct_of_above_ground')}% |"
        )

    lines.append(
        f"| **סה״כ בנייה עילית** | **כל הקומות** | **{pds.get('apartments_count')} יח״ד** | **סך שטחי בנייה עיליים בפרויקט** | **{fmt(ag.get('net_apartments_sqm'))} מ״ר** | **{fmt(ag.get('core_and_service_sqm'))} מ״ר** | **{fmt(ag.get('total_sqm'))} מ״ר** | **100.0%** |"
    )

    lines.extend([
        "",
        "---",
        "",
        "## 3. סך שטחי בנייה תת-קרקעיים (קומות מרתף וחניון)",
        "",
        f"*{ug.get('summary_note', '')}*",
        "",
        "| קומת מרתף | מפלס וגובה | פירוט חניות, מיסעות, מחסנים וחדרים טכניים | שטח קומה ברוטו | % מהתת-קרקעי |",
        "| :--- | :--- | :--- | :---: | :---: |",
    ])

    for f in ug.get("by_floor", []):
        lines.append(
            f"| **{f.get('floor_label')}** | `{f.get('elevation')}` | {f.get('usage_description')} | **{fmt(f.get('total_floor_sqm'))} מ״ר** | {f.get('pct_of_underground')}% |"
        )

    lines.extend([
        f"| **סה״כ תת-קרקעי** | **{pds.get('underground_levels')} קומות מרתף** | **{ug.get('parking_spaces')} חניות ({ug.get('parking_ratio')})** | **{fmt(ug.get('total_sqm'))} מ״ר** | **100.0%** |",
        f"| **סה״כ בנוי בפרויקט** | **עילי + תת-קרקעי** | **סך כל שטחי הבנייה בפרויקט** | **{fmt(pds.get('total_built_area_sqm'))} מ״ר** | — |",
        "",
        "---",
        "",
        "## 4. סך שטחי מרפסות גג ומרפסות תלויות (זיזיות)",
        "",
        f"### א. מרפסות גג (סך הכל: **{fmt(rt.get('total_sqm'))} מ״ר** ב-{rt.get('count')} מרפסות גג)",
        "",
        "| קומה | שיוך דירה / טיפוס | מידות ופירוט הנדסי | שטח במ״ר |",
        "| :--- | :--- | :--- | :---: |",
    ])

    for b in rt.get("breakdown", []):
        lines.append(
            f"| **{b.get('floor_label')}** | {b.get('unit_label')} | {b.get('dimensions')} | **{fmt(b.get('area_sqm'))} מ״ר** |"
        )
    lines.append(f"| **סה״כ מרפסות גג** | **{rt.get('count')} מרפסות גג** | {rt.get('summary_note', '')} | **{fmt(rt.get('total_sqm'))} מ״ר** |")

    lines.extend([
        "",
        f"### ב. מרפסות תלויות / זיזיות (סך הכל: **{fmt(sb.get('total_sqm'))} מ״ר** ב-{sb.get('count')} מרפסות)",
        "",
        "| קומות | טיפוס דירה | כמות מרפסות | שטח מרפסת יחידה | מידות והערות | סה״כ שטח במ״ר |",
        "| :--- | :--- | :---: | :---: | :--- | :---: |",
    ])

    for b in sb.get("breakdown", []):
        lines.append(
            f"| **{b.get('floor_label')}** | {b.get('unit_label')} | {b.get('count')} | {fmt(b.get('unit_area_sqm'))} מ״ר | {b.get('dimensions')} | **{fmt(b.get('total_area_sqm'))} מ״ר** |"
        )
    lines.append(
        f"| **סה״כ מרפסות תלויות** | **כל הקומות הטיפוסיות** | **{sb.get('count')}** | — | {sb.get('summary_note', '')} | **{fmt(sb.get('total_sqm'))} מ״ר** |"
    )

    lines.extend([
        "",
        "---",
        "",
        f"## 5. סך שטחי חזיתות וחלוקה מדויקת לחומרים מתכנית ההגשה (סך הכל: **{fmt(fac.get('total_sqm'))} מ״ר ברוטו** · **{fmt(fac.get('total_opaque_sqm'))} מ״ר אטום**)",
        "",
        f"- **מקור תכנית ההגשה והמודל:** {fac.get('submission_plan_source', fac.get('summary_note', ''))}",
        f"- **סיכום שטחי חומרים מתכנית ההגשה (מתוך {fmt(fac.get('total_opaque_sqm'))} מ״ר שטח אטום ורפפות):**",
        f"  - **טיח חוץ בתכנית ההגשה (`300 ₪/מ״ר`):** **{fmt(fac.get('total_plaster_sqm', 0))} מ״ר ({fac.get('total_plaster_pct', 0)}%)**",
        f"  - **חיפוי קשיח / תלייה יבשה בתכנית ההגשה (`700 ₪/מ״ר`):** **{fmt(fac.get('total_dry_cladding_sqm', 0))} מ״ר ({fac.get('total_dry_cladding_pct', 0)}%)**",
        f"  - **רפפות מסתורי כביסה ואלמנטי אוורור בהגשה:** **{fmt(fac.get('total_louvers_sqm', 0))} מ״ר ({fac.get('total_louvers_pct', 0)}%)**",
        "",
        "| שם החזית והפניה | כיוון | שטח חזית ברוטו | פתחים וזיגוג (WWR) | שטח אטום ורפפות | טיח חוץ בהגשה (300 ₪) | חיפוי קשיח בהגשה (700 ₪) | רפפות ומסתורים בהגשה | פירוט חומרים מדויק מתכנית ההגשה |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |",
    ])

    for d in fac.get("by_direction", []):
        lines.append(
            f"| **{d.get('facade_name')}** | {d.get('direction')} | **{fmt(d.get('gross_area_sqm'))} מ״ר** ({d.get('pct_of_total')}%) | {fmt(d.get('glazing_area_sqm'))} מ״ר ({d.get('wwr_pct')}%) | **{fmt(d.get('opaque_area_sqm'))} מ״ר** | **{fmt(d.get('submission_plaster_sqm', 0))} מ״ר** ({d.get('submission_plaster_pct', 0)}%) | **{fmt(d.get('submission_dry_cladding_sqm', 0))} מ״ר** ({d.get('submission_dry_cladding_pct', 0)}%) | {fmt(d.get('submission_louvers_sqm', 0))} מ״ר ({d.get('submission_louvers_pct', 0)}%) | {d.get('materials_and_elements')} |"
        )

    lines.append(
        f"| **סה״כ שטחי חזיתות החוץ** | **4 חזיתות** | **{fmt(fac.get('total_sqm'))} מ״ר (100%)** | **{fmt(fac.get('total_glazing_sqm'))} מ״ר ({fac.get('average_wwr_pct')}%)** | **{fmt(fac.get('total_opaque_sqm'))} מ״ר (100%)** | **{fmt(fac.get('total_plaster_sqm', 0))} מ״ר ({fac.get('total_plaster_pct', 0)}%)** | **{fmt(fac.get('total_dry_cladding_sqm', 0))} מ״ר ({fac.get('total_dry_cladding_pct', 0)}%)** | **{fmt(fac.get('total_louvers_sqm', 0))} מ״ר ({fac.get('total_louvers_pct', 0)}%)** | **סה״כ מעטפת לפי תכנית ההגשה** |"
    )

    if fac.get("materials_breakdown_summary"):
        lines.extend([
            "",
            "### פירוט מקרא חומרי החזיתות מתכנית ההגשה (סיכום כמותי ב-4 החזיתות)",
            "",
            "| קוד / סימון בהגשה | תיאור החומר בתכנית ההגשה | קטגוריית תחשיב | שטח כולל ב-4 החזיתות (מ״ר) | % מסך השטח האטום |",
            "| :---: | :--- | :--- | :---: | :---: |",
        ])
        for m in fac.get("materials_breakdown_summary", []):
            lines.append(
                f"| **`{m.get('code')}`** | **{m.get('name')}** | {m.get('category')} | **{fmt(m.get('area_sqm'))} מ״ר** | **{m.get('pct_of_opaque')}%** |"
            )

    lines.extend([
        "",
        "---",
        "",
        f"## 6. שטחי ריצוף נטו (שטחי רצפה של קומות מלאות) — דירות / ציבורי / מרפסות לפי קומות (סך הכל: **{fmt(flr.get('grand_total_flooring_sqm'))} מ״ר**)",
        "",
        f"*{flr.get('summary_note', '')}*",
        "",
        f"- **סך ריצוף דירות (נטו):** **{fmt(flr.get('total_apartments_flooring_sqm'))} מ״ר** (מתוכם ריצוף פנים יבש: **{fmt(flr.get('total_apartments_dry_sqm'))} מ״ר** · ריצוף חדרים רטובים נגד החלקה R10: **{fmt(flr.get('total_apartments_wet_sqm'))} מ״ר**)",
        f"- **סך ריצוף ציבורי (נטו):** **{fmt(flr.get('total_public_flooring_sqm'))} מ״ר** (לובי כניסה ראשי, מועדון דיירים/עגלות, מבואות מעליות קומתיות, חדרי מדרגות ופודסטים, מחסנים מרוצפים ומבואות מרתף)",
        f"- **סך ריצוף מרפסות (נטו):** **{fmt(flr.get('total_balconies_flooring_sqm'))} מ״ר** (מרפסות שמש זיזיות, מרפסות שירות, מרפסות גג ומשטחי גן מרוצפים R11)",
        f"- **סה״כ שטחי ריצוף בפרויקט (כל הקומות):** **{fmt(flr.get('grand_total_flooring_sqm'))} מ״ר**",
        "",
        "| קומה (קומה מלאה) | מפלס | יח״ד | ריצוף דירות — יבש (מ״ר) | ריצוף דירות — רטוב (מ״ר) | סה״כ ריצוף דירות בקומה | ריצוף ציבורי בקומה | ריצוף מרפסות בקומה | סה״כ ריצוף בקומה מלאה | פירוט והערות ריצוף |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |",
    ])

    for fl in flr.get("by_floor", []):
        lines.append(
            f"| **{fl.get('floor_label')}** | `{fl.get('elevation')}` | {fl.get('units_count')} | {fmt(fl.get('apartments_dry_sqm'))} מ״ר | {fmt(fl.get('apartments_wet_sqm'))} מ״ר | **{fmt(fl.get('apartments_flooring_sqm'))} מ״ר** | **{fmt(fl.get('public_flooring_sqm'))} מ״ר** | **{fmt(fl.get('balconies_flooring_sqm'))} מ״ר** | **{fmt(fl.get('total_floor_flooring_sqm'))} מ״ר** | {fl.get('notes', '')} |"
        )

    lines.append(
        f"| **סה״כ שטחי ריצוף בפרויקט** | **כל הקומות** | **{pds.get('apartments_count')} יח״ד** | **{fmt(flr.get('total_apartments_dry_sqm'))} מ״ר** | **{fmt(flr.get('total_apartments_wet_sqm'))} מ״ר** | **{fmt(flr.get('total_apartments_flooring_sqm'))} מ״ר** | **{fmt(flr.get('total_public_flooring_sqm'))} מ״ר** | **{fmt(flr.get('total_balconies_flooring_sqm'))} מ״ר** | **{fmt(flr.get('grand_total_flooring_sqm'))} מ״ר** | **סך ריצוף דירות + ציבורי + מרפסות** |"
    )

    lines.extend([
        "",
        "---",
        "",
        "## 7. מסמך סיכום הערות בקרת איכות והצעות לשיפור התכנון",
        "",
        "### א. ריכוז ממצאים והערות עיקריות במודל",
        "",
    ])

    for item in sdoc.get("critical_notes_summary", []):
        lines.append(f"- {item}")

    lines.extend([
        "",
        "### ב. טבלת הצעות אופרטיביות לשיפור אדריכלי והנדסי",
        "",
        "| # | רמת עדיפות | מוקד / קומה / דירה | תיאור ההערה / הליקוי | הצעה הנדסית ואדריכלית לשיפור | השפעה צפויה |",
        "| :---: | :--- | :--- | :--- | :--- | :--- |",
    ])

    for idx, p in enumerate(sdoc.get("improvement_proposals", []), 1):
        lines.append(
            f"| **{idx}** | **{p.get('priority')}** | {p.get('target')} | {p.get('issue')} | **{p.get('proposal')}** | {p.get('impact')} |"
        )

    lines.extend([
        "",
        "### ג. אינדקס מלא של כל הערות הבדיקה המסונכרנות על גבי התוכניות",
        "",
        "| סיכה | סטטוס | תקן ייחוס | טיפוס / קומה | חלל / אזור בתוכנית | כותרת הממצא | מדידה מול תקן | המלצה תכנונית |",
        "| :---: | :---: | :--- | :--- | :--- | :--- | :--- | :--- |",
    ])

    for n in notes:
        lines.append(
            f"| **#{n.get('pin_num')}** | `{n.get('status')}` | `{n.get('rule_id')}` | {n.get('typology')} | {n.get('room_name')} | **{n.get('title')}** | {n.get('measured')} (יעד: {n.get('benchmark')}) | {n.get('recommendation')} |"
        )

    # Section 8: Design Optimization & Value Engineering (ייעול תכנון והנדסת ערך)
    if opt:
        kpis = opt.get("executive_kpis", {})
        guar = opt.get("zero_damage_guarantees", {})
        contour_audit = opt.get("contour_audit_summary", {})
        ag_opt = opt.get("above_ground_optimization", {})
        ug_opt = opt.get("underground_optimization", {})
        fac_opt = opt.get("facade_cladding_optimization", {})
        apt_opt = opt.get("internal_apartment_optimization", {})

        lines.extend([
            "",
            "### ג. שיפור תכנון (ללא הקטנת קונטור הבנייה): ייעול פנים-דירתי ושטחי ליבה/שירות כלואים שהועברו מחיסכון עלויות",
            "",
            "| טיפוס דירה / מוקד ליבה כלוא | מצב נוכחי | מצב יעיל | שטח מושבח לדירה/קומה | סה״כ שטח שיפור תכנון בפרויקט | פירוט הנדסי (מדוע לא הקטין קונטור בניין ומהו שיפור התכנון) |",
            "| :--- | :---: | :---: | :---: | :---: | :--- |",
        ])
        for l_item in contour_audit.get("locked_core_reclassified_items", []):
            lines.append(
                f"| **🔄 ליבה כלואה: {l_item.get('zone')}** | הפחתת {fmt(l_item.get('proposed_core_reduction_sqm'))} מ״ר ליבה | 0.0 מ״ר הקטנת קונטור | **0 ₪ חיסכון שלד** | **+{fmt(l_item.get('reclassified_design_improvement_sqm'))} מ״ר שיפור תכנון** | **סיבת נעילת קונטור:** {l_item.get('why_not_contour_saving')} · **תועלת תכנונית:** {l_item.get('design_benefit')} |"
            )
        for a_item in apt_opt.get("items", []):
            lines.append(
                f"| **🛋️ פנים-דירתי: {a_item.get('typology')}** | מסדרון {fmt(a_item.get('current_corridor_sqm'))} מ״ר | מסדרון {fmt(a_item.get('optimal_corridor_sqm'))} מ״ר | **+{fmt(a_item.get('reclaimed_sqm_per_unit'))} מ״ר לדירה** | **+{fmt(a_item.get('total_reclaimed_sqm'))} מ״ר** ({a_item.get('units_count')} דירות) | **חדרים:** {a_item.get('target_rooms_benefiting')} · **פתחים:** {a_item.get('openings_optimization')} |"
            )

        lines.extend([
            "",
            "---",
            "",
            f"## 8. 💰 מודל החיסכון בעלויות הבנייה — צמצום קונטור בנייה מאומת וחיפוי (סה״כ פוטנציאל חיסכון ישיר: **{fmt(kpis.get('grand_total_direct_saving_ils'))} ₪**)",
            "",
            f"> **מנגנון בקרת כיווץ קונטור הבניין הכולל (Contour Shrinkage Audit):** {contour_audit.get('audit_rule_he', '')} · {guar.get('guarantee_statement', '')}",
            "",
            "### א. סיכום מנהלים ובקרת כיווץ קונטור — הפרדה בין הקטנת קונטור (חיסכון כספי) לבין ליבה כלואה (שיפור תכנון)",
            "",
            "| ציר בדיקה | הפחתת שטח גולמית שנבדקה | שטח כלוא שלא הקטין קונטור (0 ₪ ← שיפור תכנון) | שטח קונטור נחסך בפועל (נבנה פחות) | תעריף | אומדן חיסכון כספי ישיר (₪) |",
            "| :--- | :---: | :---: | :---: | :---: | :---: |",
            f"| **1. צמצום קונטור בנייה עילי (ליבה/קרקע/גג)** | {fmt(contour_audit.get('proposed_ag_gross_reduction_sqm'))} מ״ר | {fmt(contour_audit.get('rejected_locked_ag_core_sqm'))} מ״ר (ליבה כלואה/תחת תקרה) | **{fmt(kpis.get('above_ground_saved_sqm'))} מ״ר** | `6,200 ₪ / מ״ר` | **{fmt(kpis.get('above_ground_saving_ils'))} ₪** |",
            f"| **2. צמצום קונטור מרתף וחניון תת-קרקעי** | {fmt(contour_audit.get('proposed_ug_gross_reduction_sqm'))} מ״ר | {fmt(contour_audit.get('rejected_locked_ug_zone_sqm'))} מ״ר (כלוא בין חניות) | **{fmt(kpis.get('underground_saved_sqm'))} מ״ר** | `3,500 ₪ / מ״ר` | **{fmt(kpis.get('underground_saving_ils'))} ₪** |",
            f"| **3. אופטימיזציית חזיתות (חיפוי יבש 700 ₪ מול טיח 300 ₪)** | — | — | **{fmt(kpis.get('facade_converted_to_plaster_sqm'))} מ״ר מומר** | `400 ₪ / מ״ר` | **{fmt(kpis.get('facade_saving_ils'))} ₪** |",
            f"| **4. מסדרונות פנים-דירתיים שהומרו לחדרים** | {fmt(contour_audit.get('rejected_internal_apt_corridor_sqm'))} מ״ר | {fmt(contour_audit.get('rejected_internal_apt_corridor_sqm'))} מ״ר (קונטור דירה קבוע) | **0.0 מ״ר** | `0 ₪` | **0 ₪ (שיפור תכנון)** |",
            f"| **סה״כ פוטנציאל חיסכון ישיר מאומת בעלויות הבנייה** | **{fmt(contour_audit.get('total_proposed_raw_reduction_sqm'))} מ״ר נבדקו** | **{fmt(contour_audit.get('total_reclassified_to_design_improvement_sqm'))} מ״ר הועברו לשיפור תכנון** | **{fmt(contour_audit.get('total_verified_contour_saved_sqm'))} מ״ר קונטור + {fmt(kpis.get('facade_converted_to_plaster_sqm'))} מ״ר חזית** | — | **{fmt(kpis.get('grand_total_direct_saving_ils'))} ₪** |",
            "",
            "### ב. פירוט צמצום קונטור בנייה עילי מאומת (`6,200 ₪ למ״ר קונטור נחסך`)",
            "",
            "| קומה / מוקד | שטח נוכחי | הפחתת ליבה גולמית | ליבה כלואה (0 ₪ ← שיפור תכנון) | קונטור נחסך בפועל (נבנה פחות) | חיסכון כספי (₪) | הוכחת כיווץ קונטור גיאומטרית ושימושים נשמרים |",
            "| :--- | :---: | :---: | :---: | :---: | :---: | :--- |",
        ])
        for item in ag_opt.get("items", []):
            lines.append(
                f"| **{item.get('floor_or_zone')}** | {fmt(item.get('current_sqm'))} מ״ר | {fmt(item.get('proposed_gross_reduction_sqm'))} מ״ר | {fmt(item.get('non_contour_reclassified_sqm'))} מ״ר | **{fmt(item.get('saved_sqm'))} מ״ר** | **{fmt(item.get('cost_saving_ils'))} ₪** | {item.get('engineering_action')} · **כיווץ קונטור:** {item.get('contour_mechanism')} (*{item.get('preserved_utilities')}*) |"
            )

        lines.extend([
            "",
            "### ג. פירוט צמצום קונטור חניון תת-קרקעי ומרתפים (`3,500 ₪ למ״ר קונטור דיפון נחסך`)",
            "",
            "| מוקד במרתף החניון | שטח מרתף נוכחי | הפחתה גולמית | כלוא בין חניות (0 ₪) | קונטור דיפון נחסך (נבנה פחות) | חיסכון כספי (₪) | הוכחת כיווץ פוליגון דיפון ושמירת חניות |",
            "| :--- | :---: | :---: | :---: | :---: | :---: | :--- |",
        ])
        for item in ug_opt.get("items", []):
            lines.append(
                f"| **{item.get('zone')}** | {fmt(item.get('current_sqm'))} מ״ר ({ug_opt.get('current_sqm_per_stall')} מ״ר/חניה) | {fmt(item.get('proposed_gross_reduction_sqm'))} מ״ר | {fmt(item.get('non_contour_reclassified_sqm'))} מ״ר | **{fmt(item.get('saved_sqm'))} מ״ר** | **{fmt(item.get('cost_saving_ils'))} ₪** | {item.get('engineering_action')} · **כיווץ דיפון:** {item.get('contour_mechanism')} (*{item.get('parking_spaces_preserved')}*) |"
            )

        lines.extend([
            "",
            "### ד. אופטימיזציית יחס חיפוי קשיח/יבש (`700 ₪/מ״ר`) לעומת טיח חוץ (`300 ₪/מ״ר` — חיסכון `400 ₪/מ״ר`) לפי תכנית ההגשה",
            "",
            "| חזית וכיוון | שטח אטום ורפפות | טיח קיים בהגשה (300 ₪) | חיפוי קשיח בהגשה (700 ₪) | רפפות בהגשה | המרה מומלצת לטיח | תמהיל מומלץ (יבש / טיח) | חיסכון כספי (₪) | אסטרטגיה אדריכלית לפי תכנית ההגשה |",
            "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |",
        ])
        for f_item in fac_opt.get("by_facade", []):
            lines.append(
                f"| **{f_item.get('facade_name')}** | {fmt(f_item.get('opaque_area_sqm'))} מ״ר | {fmt(f_item.get('current_plaster_sqm', 0))} מ״ר ({f_item.get('current_plaster_pct', 0)}%) | {fmt(f_item.get('current_dry_cladding_sqm'))} מ״ר ({f_item.get('current_dry_pct', 0)}%) | {fmt(f_item.get('current_louvers_sqm', 0))} מ״ר | **{fmt(f_item.get('recommended_converted_to_plaster_sqm'))} מ״ר** | {f_item.get('optimized_dry_pct')}% יבש / {f_item.get('optimized_plaster_pct')}% טיח | **{fmt(f_item.get('cost_saving_ils'))} ₪** | {f_item.get('strategy_note')} |"
            )

    lines.append("")
    return "\n".join(lines)


def build_html_summary_and_areas_block(payload):
    """Builds the rich HTML block to inject into the main HTML/PDF reports and standalone HTML summary report."""
    pds = payload.get("project_data_summary", {})
    ag = pds.get("above_ground_areas", {})
    ug = pds.get("underground_areas", {})
    rt = pds.get("roof_terraces", {})
    sb = pds.get("suspended_balconies", {})
    fac = pds.get("facades", {})
    flr = pds.get("flooring_areas", {})
    opt = pds.get("design_optimization", {})
    sdoc = pds.get("summary_document", {})

    ag_rows = "".join([
        f"""<tr>
          <td><strong>{f.get('floor_label')}</strong></td>
          <td>{f.get('elevation')}</td>
          <td style="text-align:center;">{f.get('units_count')}</td>
          <td>{f.get('usage_description')}</td>
          <td style="text-align:center;">{fmt(f.get('apartments_sqm'))} מ"ר</td>
          <td style="text-align:center;">{fmt(f.get('core_service_sqm'))} מ"ר</td>
          <td style="text-align:center;font-weight:800;color:#1e3a8a;">{fmt(f.get('total_floor_sqm'))} מ"ר</td>
          <td style="text-align:center;">{f.get('pct_of_above_ground')}%</td>
        </tr>"""
        for f in ag.get("by_floor", [])
    ])

    ug_rows = "".join([
        f"""<tr>
          <td><strong>{f.get('floor_label')}</strong></td>
          <td>{f.get('elevation')}</td>
          <td>{f.get('usage_description')}</td>
          <td style="text-align:center;font-weight:800;color:#1e3a8a;">{fmt(f.get('total_floor_sqm'))} מ"ר</td>
          <td style="text-align:center;">{f.get('pct_of_underground')}%</td>
        </tr>"""
        for f in ug.get("by_floor", [])
    ])

    rt_rows = "".join([
        f"""<tr>
          <td><strong>{b.get('floor_label')}</strong></td>
          <td>{b.get('unit_label')}</td>
          <td>{b.get('dimensions')}</td>
          <td style="text-align:center;font-weight:800;color:#1e3a8a;">{fmt(b.get('area_sqm'))} מ"ר</td>
        </tr>"""
        for b in rt.get("breakdown", [])
    ])

    sb_rows = "".join([
        f"""<tr>
          <td><strong>{b.get('floor_label')}</strong></td>
          <td>{b.get('unit_label')}</td>
          <td style="text-align:center;">{b.get('count')}</td>
          <td style="text-align:center;">{fmt(b.get('unit_area_sqm'))} מ"ר</td>
          <td>{b.get('dimensions')}</td>
          <td style="text-align:center;font-weight:800;color:#1e3a8a;">{fmt(b.get('total_area_sqm'))} מ"ר</td>
        </tr>"""
        for b in sb.get("breakdown", [])
    ])

    fac_rows = "".join([
        f"""<tr>
          <td><strong>{d.get('facade_name')}</strong></td>
          <td style="text-align:center;">{d.get('direction')}</td>
          <td style="text-align:center;font-weight:800;color:#1e3a8a;">{fmt(d.get('gross_area_sqm'))} מ"ר ({d.get('pct_of_total')}%)</td>
          <td style="text-align:center;">{fmt(d.get('glazing_area_sqm'))} מ"ר ({d.get('wwr_pct')}%)</td>
          <td style="text-align:center;font-weight:700;">{fmt(d.get('opaque_area_sqm'))} מ"ר</td>
          <td style="text-align:center;color:#0f766e;font-weight:700;">{fmt(d.get('submission_plaster_sqm', 0))} מ"ר ({d.get('submission_plaster_pct', 0)}%)</td>
          <td style="text-align:center;color:#b45309;font-weight:700;">{fmt(d.get('submission_dry_cladding_sqm', 0))} מ"ר ({d.get('submission_dry_cladding_pct', 0)}%)</td>
          <td style="text-align:center;">{fmt(d.get('submission_louvers_sqm', 0))} מ"ר ({d.get('submission_louvers_pct', 0)}%)</td>
          <td>{d.get('materials_and_elements')}</td>
        </tr>"""
        for d in fac.get("by_direction", [])
    ])

    flr_rows = "".join([
        f"""<tr>
          <td><strong>{fl.get('floor_label')}</strong></td>
          <td style="text-align:center;">{fl.get('elevation')}</td>
          <td style="text-align:center;">{fl.get('units_count')}</td>
          <td style="text-align:center;">{fmt(fl.get('apartments_dry_sqm'))} מ"ר</td>
          <td style="text-align:center;">{fmt(fl.get('apartments_wet_sqm'))} מ"ר</td>
          <td style="text-align:center;font-weight:800;color:#1e3a8a;">{fmt(fl.get('apartments_flooring_sqm'))} מ"ר</td>
          <td style="text-align:center;font-weight:700;color:#0f766e;">{fmt(fl.get('public_flooring_sqm'))} מ"ר</td>
          <td style="text-align:center;font-weight:700;color:#b45309;">{fmt(fl.get('balconies_flooring_sqm'))} מ"ר</td>
          <td style="text-align:center;font-weight:900;color:#0f172a;background:#f1f5f9;">{fmt(fl.get('total_floor_flooring_sqm'))} מ"ר</td>
          <td>{fl.get('notes', '')}</td>
        </tr>"""
        for fl in flr.get("by_floor", [])
    ])

    prop_rows = "".join([
        f"""<tr>
          <td style="text-align:center;font-weight:800;">#{idx}</td>
          <td><strong>{p.get('priority')}</strong></td>
          <td><strong>{p.get('target')}</strong></td>
          <td>{p.get('issue')}</td>
          <td style="color:#1e3a8a;font-weight:700;">{p.get('proposal')}</td>
          <td>{p.get('impact')}</td>
        </tr>"""
        for idx, p in enumerate(sdoc.get("improvement_proposals", []), 1)
    ])

    crit_items = "".join([f"<li>{c}</li>" for c in sdoc.get("critical_notes_summary", [])])

    # Build HTML tables for Design Optimization & Value Engineering
    opt_kpis = opt.get("executive_kpis", {})
    opt_guar = opt.get("zero_damage_guarantees", {})
    contour_audit = opt.get("contour_audit_summary", {})
    ag_opt = opt.get("above_ground_optimization", {})
    ug_opt = opt.get("underground_optimization", {})
    fac_opt = opt.get("facade_cladding_optimization", {})
    apt_opt = opt.get("internal_apartment_optimization", {})

    opt_ag_rows = "".join([
        f"""<tr>
          <td><strong>{item.get('floor_or_zone')}</strong></td>
          <td style="text-align:center;">{fmt(item.get('current_sqm'))} מ"ר</td>
          <td style="text-align:center;">{fmt(item.get('proposed_gross_reduction_sqm'))} מ"ר</td>
          <td style="text-align:center;color:#1d4ed8;font-weight:700;">{fmt(item.get('non_contour_reclassified_sqm'))} מ"ר (0 ₪)</td>
          <td style="text-align:center;font-weight:800;color:#15803d;background:#ecfdf5;">{fmt(item.get('saved_sqm'))} מ"ר</td>
          <td style="text-align:center;font-weight:900;color:#15803d;background:#dcfce7;">{fmt(item.get('cost_saving_ils'))} ₪</td>
          <td>
            <div>{item.get('engineering_action')}</div>
            <div style="font-size:8pt;color:#0f766e;margin-top:2px;font-weight:700;">📐 כיווץ קונטור: {item.get('contour_mechanism')}</div>
            <div style="font-size:8pt;color:#475569;margin-top:2px;">🛡️ {item.get('preserved_utilities')}</div>
          </td>
        </tr>"""
        for item in ag_opt.get("items", [])
    ])

    opt_ug_rows = "".join([
        f"""<tr>
          <td><strong>{item.get('zone')}</strong></td>
          <td style="text-align:center;">{fmt(item.get('current_sqm'))} מ"ר ({ug_opt.get('current_sqm_per_stall')} מ"ר/חניה)</td>
          <td style="text-align:center;">{fmt(item.get('proposed_gross_reduction_sqm'))} מ"ר</td>
          <td style="text-align:center;color:#1d4ed8;font-weight:700;">{fmt(item.get('non_contour_reclassified_sqm'))} מ"ר (0 ₪)</td>
          <td style="text-align:center;font-weight:800;color:#15803d;background:#ecfdf5;">{fmt(item.get('saved_sqm'))} מ"ר</td>
          <td style="text-align:center;font-weight:900;color:#15803d;background:#dcfce7;">{fmt(item.get('cost_saving_ils'))} ₪</td>
          <td>
            <div>{item.get('engineering_action')}</div>
            <div style="font-size:8pt;color:#0f766e;margin-top:2px;font-weight:700;">📐 כיווץ דיפון: {item.get('contour_mechanism')}</div>
            <div style="font-size:8pt;color:#475569;margin-top:2px;">🅿️ {item.get('parking_spaces_preserved')}</div>
          </td>
        </tr>"""
        for item in ug_opt.get("items", [])
    ])

    opt_fac_rows = "".join([
        f"""<tr>
          <td><strong>{f_item.get('facade_name')}</strong></td>
          <td style="text-align:center;">{fmt(f_item.get('opaque_area_sqm'))} מ"ר</td>
          <td style="text-align:center;color:#0f766e;font-weight:700;">{fmt(f_item.get('current_plaster_sqm', 0))} מ"ר ({f_item.get('current_plaster_pct', 0)}%)</td>
          <td style="text-align:center;color:#b45309;font-weight:700;">{fmt(f_item.get('current_dry_cladding_sqm'))} מ"ר ({f_item.get('current_dry_pct', 0)}%)</td>
          <td style="text-align:center;font-weight:800;color:#0284c7;">{fmt(f_item.get('recommended_converted_to_plaster_sqm'))} מ"ר</td>
          <td style="text-align:center;">{f_item.get('optimized_dry_pct')}% יבש / {f_item.get('optimized_plaster_pct')}% טיח</td>
          <td style="text-align:center;font-weight:900;color:#15803d;background:#dcfce7;">{fmt(f_item.get('cost_saving_ils'))} ₪</td>
          <td>{f_item.get('strategy_note')}</td>
        </tr>"""
        for f_item in fac_opt.get("by_facade", [])
    ])

    opt_locked_rows = "".join([
        f"""<tr style="background:#eff6ff;">
          <td><strong>🔄 ליבה כלואה: {l_item.get('zone')}</strong></td>
          <td style="text-align:center;">הפחתת {fmt(l_item.get('proposed_core_reduction_sqm'))} מ"ר</td>
          <td style="text-align:center;color:#dc2626;font-weight:800;">0.0 מ"ר קונטור</td>
          <td style="text-align:center;font-weight:800;color:#64748b;">0 ₪</td>
          <td style="text-align:center;font-weight:900;color:#1e3a8a;background:#dbeafe;">+{fmt(l_item.get('reclassified_design_improvement_sqm'))} מ"ר שיפור תכנון</td>
          <td><strong>למה לא הקטין קונטור:</strong> {l_item.get('why_not_contour_saving')}<br/><strong>שיפור תכנון:</strong> {l_item.get('design_benefit')}</td>
        </tr>"""
        for l_item in contour_audit.get("locked_core_reclassified_items", [])
    ])

    opt_apt_rows = opt_locked_rows + "".join([
        f"""<tr>
          <td><strong>🛋️ פנים-דירתי: {a_item.get('typology')}</strong></td>
          <td style="text-align:center;">מסדרון {fmt(a_item.get('current_corridor_sqm'))} מ"ר</td>
          <td style="text-align:center;">מסדרון {fmt(a_item.get('optimal_corridor_sqm'))} מ"ר</td>
          <td style="text-align:center;font-weight:800;color:#1e3a8a;">+{fmt(a_item.get('reclaimed_sqm_per_unit'))} מ"ר לדירה</td>
          <td style="text-align:center;font-weight:900;color:#1e3a8a;background:#dbeafe;">+{fmt(a_item.get('total_reclaimed_sqm'))} מ"ר ({a_item.get('units_count')} דירות)</td>
          <td><strong>הגדלת חדרים:</strong> {a_item.get('target_rooms_benefiting')}<br/><strong>פתחים:</strong> {a_item.get('openings_optimization')}</td>
        </tr>"""
        for a_item in apt_opt.get("items", [])
    ])

    return f"""
{MARKER_HTML_START}
  <div class="page-break"></div>
  <h2>📐 נתוני פרויקט כמותיים: שטחי בנייה (עילי ותת-קרקעי לפי קומות), מרפסות גג, מרפסות תלויות ושטחי חזיתות</h2>

  <div class="scorecard-grid" style="grid-template-columns: repeat(6, 1fr); margin-bottom: 12px;">
    <div class="score-card primary">
      <div class="score-title">סך שטחי בנייה עיליים</div>
      <div class="score-val" style="font-size:14pt;">{fmt(ag.get('total_sqm'))} מ"ר</div>
      <div class="score-sub">דירות: {fmt(ag.get('net_apartments_sqm'))} | ליבה: {fmt(ag.get('core_and_service_sqm'))} מ"ר</div>
    </div>
    <div class="score-card">
      <div class="score-title">סך בנייה תת-קרקעית</div>
      <div class="score-val" style="font-size:14pt;color:#0284c7;">{fmt(ug.get('total_sqm'))} מ"ר</div>
      <div class="score-sub">{ug.get('parking_spaces')} חניות · סה"כ בנוי: {fmt(pds.get('total_built_area_sqm'))} מ"ר</div>
    </div>
    <div class="score-card">
      <div class="score-title">סך מרפסות גג ותלויות</div>
      <div class="score-val" style="font-size:14pt;color:#0f766e;">{fmt((rt.get('total_sqm') or 0) + (sb.get('total_sqm') or 0))} מ"ר</div>
      <div class="score-sub">גג: {fmt(rt.get('total_sqm'))} | תלויות: {fmt(sb.get('total_sqm'))} מ"ר</div>
    </div>
    <div class="score-card">
      <div class="score-title">סך שטחי חזיתות החוץ</div>
      <div class="score-val" style="font-size:14pt;color:#7c3aed;">{fmt(fac.get('total_sqm'))} מ"ר</div>
      <div class="score-sub">פתחים: {fmt(fac.get('total_glazing_sqm'))} מ"ר ({fac.get('average_wwr_pct')}%)</div>
    </div>
    <div class="score-card">
      <div class="score-title">סך ריצוף דירות (נטו)</div>
      <div class="score-val" style="font-size:14pt;color:#1e3a8a;">{fmt(flr.get('total_apartments_flooring_sqm'))} מ"ר</div>
      <div class="score-sub">יבש: {fmt(flr.get('total_apartments_dry_sqm'))} | רטוב: {fmt(flr.get('total_apartments_wet_sqm'))} מ"ר</div>
    </div>
    <div class="score-card">
      <div class="score-title">סך ריצוף ציבורי ומרפסות</div>
      <div class="score-val" style="font-size:14pt;color:#15803d;">{fmt(flr.get('total_public_flooring_sqm'))} מ"ר</div>
      <div class="score-sub">מרפסות: {fmt(flr.get('total_balconies_flooring_sqm'))} | סה"כ: {fmt(flr.get('grand_total_flooring_sqm'))} מ"ר</div>
    </div>
  </div>

  <h3>א. סך שטחי בנייה עיליים — סך הכל וחלוקה לקומות ({fmt(ag.get('total_sqm'))} מ"ר)</h3>
  <table>
    <thead>
      <tr>
        <th style="width:16%;">קומה</th>
        <th style="width:12%;">מפלס וגובה</th>
        <th style="width:6%;text-align:center;">יח"ד</th>
        <th style="width:32%;">פירוט שימושים ויחידות דיור בקומה</th>
        <th style="width:9%;text-align:center;">שטח דירות</th>
        <th style="width:9%;text-align:center;">ליבה ושירות</th>
        <th style="width:9%;text-align:center;">סה"כ קומה</th>
        <th style="width:7%;text-align:center;">% עילי</th>
      </tr>
    </thead>
    <tbody>
      {ag_rows}
      <tr style="background:#dbeafe;font-weight:800;">
        <td colspan="2"><strong>סה"כ שטחי בנייה עיליים</strong></td>
        <td style="text-align:center;"><strong>{pds.get('apartments_count')}</strong></td>
        <td><strong>סך כל הקומות העיליות ({pds.get('floors_above_ground')} קומות + גג טכני)</strong></td>
        <td style="text-align:center;"><strong>{fmt(ag.get('net_apartments_sqm'))} מ"ר</strong></td>
        <td style="text-align:center;"><strong>{fmt(ag.get('core_and_service_sqm'))} מ"ר</strong></td>
        <td style="text-align:center;color:#1e3a8a;"><strong>{fmt(ag.get('total_sqm'))} מ"ר</strong></td>
        <td style="text-align:center;"><strong>100%</strong></td>
      </tr>
    </tbody>
  </table>

  <h3>ב. סך שטחי בנייה תת-קרקעיים ({fmt(ug.get('total_sqm'))} מ"ר)</h3>
  <table>
    <thead>
      <tr>
        <th style="width:18%;">קומת מרתף</th>
        <th style="width:14%;">מפלס וגובה</th>
        <th style="width:46%;">פירוט חניות, מיסעות, רמפות, מחסנים וחדרים טכניים</th>
        <th style="width:12%;text-align:center;">שטח קומה</th>
        <th style="width:10%;text-align:center;">% תת-קרקעי</th>
      </tr>
    </thead>
    <tbody>
      {ug_rows}
      <tr style="background:#dbeafe;font-weight:800;">
        <td colspan="3"><strong>סה"כ שטחי בנייה תת-קרקעיים ({ug.get('parking_spaces')} חניות · {ug.get('parking_ratio')})</strong></td>
        <td style="text-align:center;color:#1e3a8a;"><strong>{fmt(ug.get('total_sqm'))} מ"ר</strong></td>
        <td style="text-align:center;"><strong>100%</strong></td>
      </tr>
      <tr style="background:#bfdbfe;font-weight:900;">
        <td colspan="3"><strong>סה"כ שטח בנוי כולל בפרויקט (עילי + תת-קרקעי)</strong></td>
        <td colspan="2" style="text-align:center;color:#1e3a8a;"><strong>{fmt(pds.get('total_built_area_sqm'))} מ"ר</strong></td>
      </tr>
    </tbody>
  </table>

  <h3>ג. סך שטחי מרפסות גג ({fmt(rt.get('total_sqm'))} מ"ר) ומרפסות תלויות ({fmt(sb.get('total_sqm'))} מ"ר)</h3>
  <table>
    <thead>
      <tr>
        <th style="width:22%;">קומה (מרפסות גג)</th>
        <th style="width:28%;">שיוך דירה / טיפוס</th>
        <th style="width:36%;">מידות ופירוט הנדסי</th>
        <th style="width:14%;text-align:center;">שטח במ"ר</th>
      </tr>
    </thead>
    <tbody>
      {rt_rows}
      <tr style="background:#dbeafe;font-weight:800;">
        <td colspan="3"><strong>סה"כ שטחי מרפסות גג ({rt.get('count')} מרפסות גג)</strong></td>
        <td style="text-align:center;color:#1e3a8a;"><strong>{fmt(rt.get('total_sqm'))} מ"ר</strong></td>
      </tr>
    </tbody>
  </table>

  <table>
    <thead>
      <tr>
        <th style="width:18%;">קומות (מרפסות תלויות)</th>
        <th style="width:24%;">טיפוס דירה</th>
        <th style="width:10%;text-align:center;">כמות</th>
        <th style="width:12%;text-align:center;">שטח יחידה</th>
        <th style="width:22%;">מידות ועומק</th>
        <th style="width:14%;text-align:center;">סה"כ שטח</th>
      </tr>
    </thead>
    <tbody>
      {sb_rows}
      <tr style="background:#dbeafe;font-weight:800;">
        <td colspan="5"><strong>סה"כ שטחי מרפסות תלויות / זיזיות ({sb.get('count')} מרפסות)</strong></td>
        <td style="text-align:center;color:#1e3a8a;"><strong>{fmt(sb.get('total_sqm'))} מ"ר</strong></td>
      </tr>
    </tbody>
  </table>

  <h3>ד. סך שטחי חזיתות וחלוקה מדויקת לחומרים מתכנית ההגשה ({fmt(fac.get('total_sqm'))} מ"ר ברוטו · {fmt(fac.get('total_opaque_sqm'))} מ"ר אטום)</h3>
  <p style="font-size:8.5pt;color:#1e3a8a;margin:2px 0 6px 0;"><strong>מקור תכנית ההגשה:</strong> {fac.get('submission_plan_source', '')}</p>
  <table>
    <thead>
      <tr>
        <th style="width:16%;">שם החזית והפניה</th>
        <th style="width:5%;text-align:center;">כיוון</th>
        <th style="width:10%;text-align:center;">שטח חזית ברוטו</th>
        <th style="width:10%;text-align:center;">זיגוג ופתחים</th>
        <th style="width:9%;text-align:center;">שטח אטום</th>
        <th style="width:11%;text-align:center;">טיח בהגשה (300 ₪)</th>
        <th style="width:11%;text-align:center;">חיפוי קשיח בהגשה (700 ₪)</th>
        <th style="width:8%;text-align:center;">רפפות בהגשה</th>
        <th style="width:20%;">פירוט חומרים מדויק מתכנית ההגשה</th>
      </tr>
    </thead>
    <tbody>
      {fac_rows}
      <tr style="background:#dbeafe;font-weight:800;">
        <td colspan="2"><strong>סה"כ 4 חזיתות המבנה</strong></td>
        <td style="text-align:center;color:#1e3a8a;"><strong>{fmt(fac.get('total_sqm'))} מ"ר (100%)</strong></td>
        <td style="text-align:center;"><strong>{fmt(fac.get('total_glazing_sqm'))} מ"ר ({fac.get('average_wwr_pct')}%)</strong></td>
        <td style="text-align:center;"><strong>{fmt(fac.get('total_opaque_sqm'))} מ"ר (100%)</strong></td>
        <td style="text-align:center;color:#0f766e;"><strong>{fmt(fac.get('total_plaster_sqm', 0))} מ"ר ({fac.get('total_plaster_pct', 0)}%)</strong></td>
        <td style="text-align:center;color:#b45309;"><strong>{fmt(fac.get('total_dry_cladding_sqm', 0))} מ"ר ({fac.get('total_dry_cladding_pct', 0)}%)</strong></td>
        <td style="text-align:center;"><strong>{fmt(fac.get('total_louvers_sqm', 0))} מ"ר ({fac.get('total_louvers_pct', 0)}%)</strong></td>
        <td><strong>חלוקה מדויקת מתכנית ההגשה</strong></td>
      </tr>
    </tbody>
  </table>

  <h3>ה. שטחי ריצוף נטו (קומות מלאות — דירות / ציבורי / מרפסות לפי קומות · סה"כ: {fmt(flr.get('grand_total_flooring_sqm'))} מ"ר)</h3>
  <p style="font-size:8.5pt;color:#334155;margin:2px 0 6px 0;">{flr.get('summary_note', '')}</p>
  <table>
    <thead>
      <tr>
        <th style="width:15%;">קומה (קומה מלאה)</th>
        <th style="width:9%;text-align:center;">מפלס</th>
        <th style="width:5%;text-align:center;">יח"ד</th>
        <th style="width:9%;text-align:center;">ריצוף דירות (יבש)</th>
        <th style="width:9%;text-align:center;">ריצוף דירות (רטוב)</th>
        <th style="width:10%;text-align:center;">סה"כ ריצוף דירות</th>
        <th style="width:9%;text-align:center;">ריצוף ציבורי</th>
        <th style="width:9%;text-align:center;">ריצוף מרפסות</th>
        <th style="width:10%;text-align:center;">סה"כ ריצוף בקומה</th>
        <th style="width:15%;">פירוט והערות ריצוף</th>
      </tr>
    </thead>
    <tbody>
      {flr_rows}
      <tr style="background:#dbeafe;font-weight:900;">
        <td colspan="2"><strong>סה"כ שטחי ריצוף בפרויקט</strong></td>
        <td style="text-align:center;"><strong>{pds.get('apartments_count')}</strong></td>
        <td style="text-align:center;"><strong>{fmt(flr.get('total_apartments_dry_sqm'))} מ"ר</strong></td>
        <td style="text-align:center;"><strong>{fmt(flr.get('total_apartments_wet_sqm'))} מ"ר</strong></td>
        <td style="text-align:center;color:#1e3a8a;"><strong>{fmt(flr.get('total_apartments_flooring_sqm'))} מ"ר</strong></td>
        <td style="text-align:center;color:#0f766e;"><strong>{fmt(flr.get('total_public_flooring_sqm'))} מ"ר</strong></td>
        <td style="text-align:center;color:#b45309;"><strong>{fmt(flr.get('total_balconies_flooring_sqm'))} מ"ר</strong></td>
        <td style="text-align:center;color:#0f172a;background:#bfdbfe;"><strong>{fmt(flr.get('grand_total_flooring_sqm'))} מ"ר</strong></td>
        <td><strong>דירות + ציבורי + מרפסות</strong></td>
      </tr>
    </tbody>
  </table>

  <h2>📋 מסמך סיכום הערות בקרת איכות והצעות לשיפור התכנון</h2>
  <div class="alert-box alert-info" style="background:#eff6ff;border:1px solid #93c5fd;border-right:4px solid #2563eb;padding:9px 12px;border-radius:6px;margin-bottom:10px;">
    <strong>סיכום מנהלים:</strong> {sdoc.get('overall_verdict', '')}
    <ul style="margin:6px 0 0 0;padding-right:18px;">
      {crit_items}
    </ul>
  </div>

  <table>
    <thead>
      <tr>
        <th style="width:5%;text-align:center;">#</th>
        <th style="width:14%;">רמת עדיפות</th>
        <th style="width:20%;">מוקד / קומה / דירה</th>
        <th style="width:21%;">תיאור ההערה / הליקוי</th>
        <th style="width:25%;">הצעה הנדסית ואדריכלית לשיפור</th>
        <th style="width:15%;">השפעה ותועלת</th>
      </tr>
    </thead>
    <tbody>
      {prop_rows}
    </tbody>
  </table>

  <h3>🛋️ שיפור תכנון (ללא הקטנת קונטור הבנייה): ייעול פנים-דירתי ושטחי ליבה כלואים שהועברו מחיסכון עלויות</h3>
  <table>
    <thead>
      <tr>
        <th style="width:22%;">טיפוס דירה / מוקד ליבה כלוא</th>
        <th style="width:10%;text-align:center;">מצב נוכחי</th>
        <th style="width:10%;text-align:center;">מצב יעיל / קונטור</th>
        <th style="width:11%;text-align:center;">תוספת / חיסכון</th>
        <th style="width:13%;text-align:center;">סה"כ שטח שיפור תכנון</th>
        <th style="width:34%;">פירוט הנדסי (מדוע לא הקטין קונטור ומהו שיפור התכנון)</th>
      </tr>
    </thead>
    <tbody>
      {opt_apt_rows}
    </tbody>
  </table>

  <h2>💰 מודל החיסכון בעלויות הבנייה — צמצום קונטור בנייה מאומת וחיפוי (סה"כ חיסכון ישיר: {fmt(opt_kpis.get('grand_total_direct_saving_ils'))} ₪)</h2>
  <div class="alert-box alert-info" style="background:#f0fdf4;border:1px solid #86efac;border-right:4px solid #16a34a;padding:9px 12px;border-radius:6px;margin-bottom:10px;color:#14532d;">
    <strong>📐 מנגנון בקרת כיווץ קונטור הבניין (Contour Shrinkage Audit):</strong> {contour_audit.get('audit_rule_he', '')} · {opt_guar.get('guarantee_statement', '')}
  </div>

  <div class="scorecard-grid" style="grid-template-columns: repeat(4, 1fr); margin-bottom: 12px;">
    <div class="score-card" style="border-top-color:#16a34a;background:#f0fdf4;">
      <div class="score-title">סה"כ חיסכון כספי ישיר בבנייה</div>
      <div class="score-val" style="font-size:13.5pt;color:#15803d;">{fmt(opt_kpis.get('grand_total_direct_saving_ils'))} ₪</div>
      <div class="score-sub">אך ורק מקונטור שנבנה פחות + חיפוי</div>
    </div>
    <div class="score-card" style="border-top-color:#2563eb;">
      <div class="score-title">צמצום קונטור עילי מאומת (6,200 ₪/מ"ר)</div>
      <div class="score-val" style="font-size:13pt;color:#1e3a8a;">{fmt(opt_kpis.get('above_ground_saving_ils'))} ₪</div>
      <div class="score-sub">נבנה פחות: {fmt(opt_kpis.get('above_ground_saved_sqm'))} מ"ר (נוכו {fmt(contour_audit.get('rejected_locked_ag_core_sqm'))} מ"ר כלואים)</div>
    </div>
    <div class="score-card" style="border-top-color:#0284c7;">
      <div class="score-title">צמצום קונטור חניון מאומת (3,500 ₪/מ"ר)</div>
      <div class="score-val" style="font-size:13pt;color:#0284c7;">{fmt(opt_kpis.get('underground_saving_ils'))} ₪</div>
      <div class="score-sub">נבנה פחות: {fmt(opt_kpis.get('underground_saved_sqm'))} מ"ר (נוכו {fmt(contour_audit.get('rejected_locked_ug_zone_sqm'))} מ"ר כלואים)</div>
    </div>
    <div class="score-card" style="border-top-color:#d97706;">
      <div class="score-title">חיפוי יבש מול טיח (400 ₪/מ"ר)</div>
      <div class="score-val" style="font-size:13pt;color:#b45309;">{fmt(opt_kpis.get('facade_saving_ils'))} ₪</div>
      <div class="score-sub">המרת {fmt(opt_kpis.get('facade_converted_to_plaster_sqm'))} מ"ר לטיח</div>
    </div>
  </div>

  <h3>א. צמצום קונטור בנייה עילי מאומת (6,200 ₪ למ"ר קונטור נחסך — בניכוי ליבה כלואה שהועברה לשיפור תכנון)</h3>
  <table>
    <thead>
      <tr>
        <th style="width:18%;">קומה / מוקד</th>
        <th style="width:8%;text-align:center;">שטח נוכחי</th>
        <th style="width:9%;text-align:center;">הפחתה גולמית</th>
        <th style="width:10%;text-align:center;">כלוא (0 ₪ ← שיפור תכנון)</th>
        <th style="width:10%;text-align:center;">קונטור נחסך (נבנה פחות)</th>
        <th style="width:12%;text-align:center;">חיסכון כספי (₪)</th>
        <th style="width:33%;">פעולה הנדסית, הוכחת כיווץ קונטור ושימושים נשמרים</th>
      </tr>
    </thead>
    <tbody>
      {opt_ag_rows}
    </tbody>
  </table>

  <h3>ב. צמצום קונטור מרתף חניון תת-קרקעי מאומת (3,500 ₪ למ"ר קונטור דיפון נחסך — 100% שמירה על מצבת החניות)</h3>
  <table>
    <thead>
      <tr>
        <th style="width:18%;">מוקד במרתף</th>
        <th style="width:11%;text-align:center;">שטח נוכחי</th>
        <th style="width:9%;text-align:center;">הפחתה גולמית</th>
        <th style="width:10%;text-align:center;">כלוא בין חניות (0 ₪)</th>
        <th style="width:10%;text-align:center;">קונטור דיפון נחסך</th>
        <th style="width:12%;text-align:center;">חיסכון כספי (₪)</th>
        <th style="width:30%;">פתרון הנדסי, כיווץ פוליגון דיפון ושמירת חניות</th>
      </tr>
    </thead>
    <tbody>
      {opt_ug_rows}
    </tbody>
  </table>

  <h3>ג. אופטימיזציית חזיתות מתכנית ההגשה — חיפוי קשיח/יבש (700 ₪/מ"ר) מול טיח חוץ (300 ₪/מ"ר · חיסכון 400 ₪/מ"ר)</h3>
  <table>
    <thead>
      <tr>
        <th style="width:15%;">חזית וכיוון</th>
        <th style="width:9%;text-align:center;">שטח אטום</th>
        <th style="width:11%;text-align:center;">טיח קיים בהגשה</th>
        <th style="width:11%;text-align:center;">חיפוי קשיח בהגשה</th>
        <th style="width:10%;text-align:center;">המרה לטיח</th>
        <th style="width:12%;text-align:center;">תמהיל מומלץ</th>
        <th style="width:10%;text-align:center;">חיסכון כספי</th>
        <th style="width:22%;">אסטרטגיה אדריכלית לפי תכנית ההגשה</th>
      </tr>
    </thead>
    <tbody>
      {opt_fac_rows}
    </tbody>
  </table>
{MARKER_HTML_END}
"""


def build_standalone_html_document(payload):
    """Creates a complete standalone printable HTML document for the Summary & Quantitative Areas report."""
    pds = payload.get("project_data_summary", {})
    sdoc = pds.get("summary_document", {})
    body_block = build_html_summary_and_areas_block(payload).replace('<div class="page-break"></div>', "")

    notes_rows = "".join([
        f"""<tr>
          <td style="text-align:center;font-weight:800;">#{n.get('pin_num')}</td>
          <td style="text-align:center;"><strong>{n.get('status')}</strong></td>
          <td>{n.get('rule_id')}</td>
          <td>{n.get('typology')}</td>
          <td><strong>{n.get('room_name')}</strong></td>
          <td>{n.get('title')}</td>
          <td>{n.get('measured')}</td>
          <td style="color:#1e3a8a;">{n.get('recommendation')}</td>
        </tr>"""
        for n in payload.get("notes", [])
    ])

    return f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <title>{sdoc.get('document_title', payload.get('project_name'))}</title>
  <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&family=Heebo:wght@400;500;700;800;900&display=swap" rel="stylesheet" />
  <style>
    @page {{ size: A4 portrait; margin: 12mm; }}
    * {{ box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
    body {{ font-family: 'Assistant', 'Heebo', sans-serif; color: #0f172a; line-height: 1.4; font-size: 9.5pt; margin: 0; padding: 20px; background: #f8fafc; }}
    .page-container {{ max-width: 1100px; margin: 0 auto; background: #ffffff; padding: 28px 32px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
    .header-banner {{ background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); color: #fff; padding: 18px 22px; border-radius: 10px; margin-bottom: 16px; border-right: 6px solid #38bdf8; display: flex; justify-content: space-between; align-items: center; }}
    .header-banner h1 {{ font-family: 'Heebo', sans-serif; font-size: 18pt; margin: 0 0 4px 0; }}
    .header-subtitle {{ font-size: 10.5pt; color: #bae6fd; }}
    .print-btn {{ background: #38bdf8; color: #0f172a; border: none; padding: 8px 16px; border-radius: 6px; font-family: 'Heebo', sans-serif; font-weight: 800; cursor: pointer; font-size: 10pt; }}
    @media print {{ body {{ background: #fff; padding: 0; }} .page-container {{ box-shadow: none; padding: 0; }} .print-btn {{ display: none; }} }}
    h2 {{ font-family: 'Heebo', sans-serif; font-size: 12.5pt; font-weight: 800; color: #0f172a; background: #f1f5f9; border-right: 4px solid #2563eb; padding: 6px 10px; border-radius: 4px; margin: 16px 0 8px 0; }}
    h3 {{ font-family: 'Heebo', sans-serif; font-size: 10.5pt; font-weight: 800; color: #1e3a8a; margin: 12px 0 6px 0; }}
    .scorecard-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin-bottom: 14px; }}
    .score-card {{ background: #f8fafc; border: 1px solid #cbd5e1; border-top: 3px solid #2563eb; border-radius: 8px; padding: 8px 10px; text-align: center; }}
    .score-title {{ font-size: 8.5pt; font-weight: 700; color: #475569; }}
    .score-val {{ font-family: 'Heebo', sans-serif; font-weight: 900; color: #0f172a; margin: 2px 0; }}
    .score-sub {{ font-size: 7.5pt; color: #1d4ed8; font-weight: 600; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 12px; font-size: 8.5pt; }}
    th {{ background: #1e293b; color: #fff; font-weight: 700; text-align: right; padding: 6px 8px; border: 1px solid #1e293b; }}
    td {{ padding: 5px 8px; border: 1px solid #cbd5e1; vertical-align: top; }}
    tr:nth-child(even) td {{ background: #f8fafc; }}
  </style>
</head>
<body>
  <div class="page-container">
    <div class="header-banner">
      <div>
        <h1>{sdoc.get('document_title', payload.get('project_name'))}</h1>
        <div class="header-subtitle">{payload.get('project_subtitle', '')}</div>
      </div>
      <button class="print-btn" onclick="window.print()">🖨️ הדפס / שמור כ-PDF</button>
    </div>

    {body_block}

    <h2>📌 נספח: ריכוז כל הערות הבדיקה הפרטניות במודל ({len(payload.get('notes', []))} הערות)</h2>
    <table>
      <thead>
        <tr>
          <th style="width:5%;">סיכה</th>
          <th style="width:7%;">סטטוס</th>
          <th style="width:10%;">תקן</th>
          <th style="width:16%;">טיפוס / קומה</th>
          <th style="width:16%;">חלל / אזור</th>
          <th style="width:18%;">כותרת הממצא</th>
          <th style="width:12%;">מדידה בתכנית</th>
          <th style="width:16%;">המלצה לשיפור</th>
        </tr>
      </thead>
      <tbody>
        {notes_rows}
      </tbody>
    </table>
  </div>
</body>
</html>"""


def update_all_reports():
    builders = [
        ("pines48", build_pines48_analysis, "generate_pines48_pdf_report.py"),
        ("kkl10", build_kkl10_analysis, "generate_kkl10_pdf_report.py"),
        ("hafetz44", build_hafetz44_analysis, "generate_hafetz44_pdf_report.py"),
        ("yatkovski7", build_yatkovski7_analysis, "generate_yatkovski7_pdf_report.py"),
        ("kitroni37", build_kitroni37_analysis, "generate_kitroni37_pdf_report.py"),
        ("feierberg3", build_feierberg3_analysis, ""),
        ("sharett26", build_sharett26_analysis, ""),
    ]

    for pid, builder_fn, script_name in builders:
        payload = builder_fn()
        md_section = build_markdown_summary_and_areas_section(payload)
        html_section = build_html_summary_and_areas_block(payload)
        standalone_html = build_standalone_html_document(payload)

        # 1. Write standalone Summary & Areas Markdown and HTML
        summary_md_path = os.path.join(REPORTS_DIR, f"{pid}_summary_and_areas_report.md")
        with open(summary_md_path, "w", encoding="utf-8") as f:
            f.write(md_section)

        summary_html_path = os.path.join(REPORTS_DIR, f"{pid}_summary_and_areas_report.html")
        with open(summary_html_path, "w", encoding="utf-8") as f:
            f.write(standalone_html)

        # 2. Update main Markdown report (`reports/<pid>_architectural_quality_report.md`)
        main_md_path = os.path.join(REPORTS_DIR, f"{pid}_architectural_quality_report.md")
        if os.path.exists(main_md_path):
            with open(main_md_path, "r", encoding="utf-8") as f:
                existing_md = f.read()
            if MARKER_MD in existing_md:
                existing_md = existing_md.split(MARKER_MD)[0].rstrip()
            updated_md = existing_md + "\n\n" + md_section
            with open(main_md_path, "w", encoding="utf-8") as f:
                f.write(updated_md)
        else:
            with open(main_md_path, "w", encoding="utf-8") as f:
                f.write(md_section)

        # 3. Update main HTML report (`reports/<pid>_architectural_quality_analysis.html`)
        main_html_path = os.path.join(REPORTS_DIR, f"{pid}_architectural_quality_analysis.html")
        if os.path.exists(main_html_path):
            with open(main_html_path, "r", encoding="utf-8") as f:
                existing_html = f.read()
            if MARKER_HTML_START in existing_html and MARKER_HTML_END in existing_html:
                existing_html = re.sub(
                    re.escape(MARKER_HTML_START) + r".*?" + re.escape(MARKER_HTML_END),
                    "",
                    existing_html,
                    flags=re.DOTALL,
                )
            if "</body>" in existing_html:
                updated_html = existing_html.replace("</body>", html_section + "\n</body>")
            else:
                updated_html = existing_html + "\n" + html_section
            with open(main_html_path, "w", encoding="utf-8") as f:
                f.write(updated_html)
        else:
            with open(main_html_path, "w", encoding="utf-8") as f:
                f.write(standalone_html)

        # 4. Also fix hardcoded `c:\Users\guyku\archknow` paths in `generate_<pid>_pdf_report.py`
        if script_name:
            script_path = os.path.join(BASE_DIR, script_name)
            if os.path.exists(script_path):
                with open(script_path, "r", encoding="utf-8") as f:
                    sc = f.read()
                sc_fixed = sc.replace(
                    r'r"c:\Users\guyku\archknow\reports"',
                    'os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")',
                )
                if sc_fixed != sc:
                    with open(script_path, "w", encoding="utf-8") as f:
                        f.write(sc_fixed)

        print(f"[OK] Updated Summary & Quantitative Areas reports for {pid}")

    # 5. Render updated PDFs using Headless Microsoft Edge (or Playwright fallback)
    import subprocess
    edge_candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    edge_exe = next((p for p in edge_candidates if os.path.exists(p)), None)
    if edge_exe:
        for pid, _, _ in builders:
            for suffix in ["architectural_quality_analysis", "summary_and_areas_report"]:
                html_p = os.path.join(REPORTS_DIR, f"{pid}_{suffix}.html")
                pdf_p = os.path.join(REPORTS_DIR, f"{pid}_{suffix}.pdf")
                if os.path.exists(html_p):
                    file_url = "file:///" + html_p.replace("\\", "/")
                    subprocess.run(
                        [
                            edge_exe,
                            "--headless",
                            "--disable-gpu",
                            "--no-pdf-header-footer",
                            f"--print-to-pdf={pdf_p}",
                            file_url,
                        ],
                        check=False,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    print(f"[PDF] Rendered {pdf_p}")
    else:
        print("[PDF] Edge executable not found for headless PDF rendering.")


if __name__ == "__main__":
    update_all_reports()
