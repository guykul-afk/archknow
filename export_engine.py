"""
ArchiCheck CAD Redline (.dxf) & Executive BoQ / Action Package (.xlsx) Export Engine
====================================================================================
Provides one-click deterministic exports for architects, project managers, and contractors:
1. `generate_project_dxf_redline(payload) -> bytes`:
   Generates a layered AutoCAD R2010 `.dxf` file containing all Value Engineering before/after
   contours, relocated parking stall targets, and architectural review callout boxes.
2. `generate_project_excel_boq(payload) -> bytes`:
   Generates a multi-sheet OpenXML `.xlsx` workbook containing Executive KPIs, Value Engineering
   BoQ items, Contractor Constructability & Developer Revenue Yield pillars, Architect Action
   Package decision rows, and Quantitative Floor/Facade Area schedules.
"""
from __future__ import annotations

import io
import zipfile
from xml.sax.saxutils import escape as _xml_escape
import ezdxf


def _rect_to_cad_pts(rect: dict, floor_offset_x: float = 0.0, scale: float = 100.0):
    """Converts normalized percentage rect {x, y, w, h} into CAD modelspace coordinates (cm)."""
    if not isinstance(rect, dict):
        return None
    x = float(rect.get("x", 0.0)) * scale + floor_offset_x
    # Invert Y so top-left (0,0) in web coordinates maps cleanly to CAD Y-up
    w = float(rect.get("w", 10.0)) * scale
    h = float(rect.get("h", 10.0)) * scale
    y_top = (100.0 - float(rect.get("y", 0.0))) * scale
    y_bot = y_top - h
    return [
        (round(x, 2), round(y_bot, 2)),
        (round(x + w, 2), round(y_bot, 2)),
        (round(x + w, 2), round(y_top, 2)),
        (round(x, 2), round(y_top, 2)),
        (round(x, 2), round(y_bot, 2)),
    ]


def generate_project_dxf_redline(payload: dict) -> bytes:
    """
    Builds a multi-layer AutoCAD R2010 DXF redline overlay from a project payload.
    Returns UTF-8 encoded DXF bytes ready for HTTP download or disk save.
    """
    if not isinstance(payload, dict):
        payload = {}

    doc = ezdxf.new("R2010")
    msp = doc.modelspace()

    layers_spec = [
        ("ARCHICHECK-TITLE", 7),
        ("ARCHICHECK-VE-CONTOUR-BEFORE", 1),   # Red: Original contour before contraction
        ("ARCHICHECK-VE-CONTOUR-AFTER", 3),    # Green: Contracted contour after optimization
        ("ARCHICHECK-STALL-RELOC", 5),         # Blue: Relocated parking stall bay
        ("ARCHICHECK-AUDIT-HIGH", 1),          # Red: High-severity architectural notes
        ("ARCHICHECK-AUDIT-MEDIUM", 2),        # Yellow: Medium-severity notes
        ("ARCHICHECK-AUDIT-PASS", 3),          # Green: Positive / verified notes
    ]
    for lname, col in layers_spec:
        if lname not in doc.layers:
            doc.layers.add(name=lname, color=col)

    project_id = str(payload.get("project_id") or payload.get("id") or "project")
    project_title = str(payload.get("project_name") or payload.get("title") or project_id)
    pds = payload.get("project_data_summary") or payload.get("data_summary") or {}
    opt = payload.get("design_optimization") or pds.get("design_optimization") or {}
    kpis = opt.get("executive_kpis") or {}
    construct = opt.get("contractor_constructability_and_yield") or {}

    # 1. Header / Executive Summary Block in CAD
    msp.add_text(
        f"ARCHICHECK CAD REDLINE OVERLAY - {project_title}",
        dxfattribs={"layer": "ARCHICHECK-TITLE", "height": 180.0, "insert": (0, 11200)},
    )
    msp.add_text(
        (
            f"Direct Contour & Facade Saving: {int(kpis.get('grand_total_direct_saving_ils') or 0):,} ILS | "
            f"Net Avoidable: {int(kpis.get('grand_total_net_avoidable_saving_ils') or 0):,} ILS | "
            f"Constructability: {int(construct.get('total_constructability_saving_ils') or 0):,} ILS"
        ),
        dxfattribs={"layer": "ARCHICHECK-TITLE", "height": 110.0, "insert": (0, 10900)},
    )

    # Group notes by floor_key / sheet_id to place each floor in its own CAD X-bay (12,000 units apart)
    notes = payload.get("notes") or []
    floor_keys = []
    for n in notes:
        fk = str(n.get("floor_key") or n.get("sheet_id") or "general")
        if fk not in floor_keys:
            floor_keys.append(fk)
    if not floor_keys:
        floor_keys = ["general"]

    floor_offsets = {fk: idx * 12000.0 for idx, fk in enumerate(floor_keys)}

    for fk, x_off in floor_offsets.items():
        # Draw 10,000 x 10,000 reference frame for the floor sheet
        frame_pts = [(x_off, 0), (x_off + 10000, 0), (x_off + 10000, 10000), (x_off, 10000), (x_off, 0)]
        msp.add_lwpolyline(frame_pts, dxfattribs={"layer": "ARCHICHECK-TITLE"})
        msp.add_text(
            f"FLOOR SHEET: {fk.upper()}",
            dxfattribs={"layer": "ARCHICHECK-TITLE", "height": 140.0, "insert": (x_off + 200, 10200)},
        )

    for n in notes:
        if not isinstance(n, dict):
            continue
        fk = str(n.get("floor_key") or n.get("sheet_id") or "general")
        x_off = floor_offsets.get(fk, 0.0)
        nid = str(n.get("id") or "NOTE")
        title = str(n.get("title") or "")
        sev = str(n.get("severity") or n.get("status") or "medium").lower()
        layer = (
            "ARCHICHECK-AUDIT-HIGH"
            if sev in ("high", "fail")
            else "ARCHICHECK-AUDIT-PASS"
            if sev == "pass"
            else "ARCHICHECK-AUDIT-MEDIUM"
        )

        # Primary bounding box
        bbox = n.get("bbox")
        if not isinstance(bbox, dict) and n.get("x_pct") is not None and n.get("y_pct") is not None:
            bbox = {
                "x": float(n.get("x_pct", 0.0)),
                "y": float(n.get("y_pct", 0.0)),
                "w": float(n.get("w_pct", 10.0)),
                "h": float(n.get("h_pct", 10.0)),
            }
        pts = _rect_to_cad_pts(bbox, floor_offset_x=x_off)
        if pts:
            msp.add_lwpolyline(pts, dxfattribs={"layer": layer})
            msp.add_text(
                f"[{nid}] {title[:48]}",
                dxfattribs={"layer": layer, "height": 75.0, "insert": (pts[0][0] + 40, pts[2][1] - 110)},
            )

        # Before Contour Rect (Red)
        before_pts = _rect_to_cad_pts(n.get("before_contour_rect"), floor_offset_x=x_off)
        if before_pts:
            msp.add_lwpolyline(before_pts, dxfattribs={"layer": "ARCHICHECK-VE-CONTOUR-BEFORE"})
            msp.add_text(
                f"BEFORE CONTOUR ({nid})",
                dxfattribs={
                    "layer": "ARCHICHECK-VE-CONTOUR-BEFORE",
                    "height": 65.0,
                    "insert": (before_pts[0][0] + 30, before_pts[2][1] + 40),
                },
            )

        # After Contour Rect (Green)
        after_pts = _rect_to_cad_pts(n.get("after_contour_rect"), floor_offset_x=x_off)
        if after_pts:
            msp.add_lwpolyline(after_pts, dxfattribs={"layer": "ARCHICHECK-VE-CONTOUR-AFTER"})
            msp.add_text(
                f"AFTER CONTOUR ({nid})",
                dxfattribs={
                    "layer": "ARCHICHECK-VE-CONTOUR-AFTER",
                    "height": 65.0,
                    "insert": (after_pts[0][0] + 30, after_pts[0][1] + 40),
                },
            )

        # Relocated Parking Target Rect (Blue)
        reloc_pts = _rect_to_cad_pts(n.get("relocated_parking_target_rect"), floor_offset_x=x_off)
        if reloc_pts and int(n.get("stalls_relocated_count") or 0) > 0:
            msp.add_lwpolyline(reloc_pts, dxfattribs={"layer": "ARCHICHECK-STALL-RELOC"})
            msp.add_text(
                f"RELOCATED STALLS: {int(n.get('stalls_relocated_count'))} ({nid})",
                dxfattribs={
                    "layer": "ARCHICHECK-STALL-RELOC",
                    "height": 65.0,
                    "insert": (reloc_pts[0][0] + 30, reloc_pts[0][1] + 40),
                },
            )

    buf = io.StringIO()
    doc.write(buf)
    return buf.getvalue().encode("utf-8")


def _col_letter(col_idx_1based: int) -> str:
    """Converts 1-based column index to Excel column letter (A, B, ..., Z, AA...)."""
    res = ""
    n = col_idx_1based
    while n > 0:
        n, rem = divmod(n - 1, 26)
        res = chr(65 + rem) + res
    return res


def _build_worksheet_xml(rows: list[list]) -> str:
    """Builds a valid OpenXML worksheet XML with RTL view and inline string / numeric cells."""
    sheet_rows_xml = []
    for r_idx, row in enumerate(rows, start=1):
        cells_xml = []
        for c_idx, val in enumerate(row, start=1):
            col_ref = f"{_col_letter(c_idx)}{r_idx}"
            style_attr = ' s="1"' if r_idx == 1 else ""
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                cells_xml.append(f'<c r="{col_ref}"{style_attr}><v>{val}</v></c>')
            else:
                txt = _xml_escape(str(val if val is not None else ""))
                cells_xml.append(
                    f'<c r="{col_ref}" t="inlineStr"{style_attr}><is><t xml:space="preserve">{txt}</t></is></c>'
                )
        sheet_rows_xml.append(f'<row r="{r_idx}">{"".join(cells_xml)}</row>')

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<sheetViews><sheetView rightToLeft="1" workbookViewId="0"/></sheetViews>'
        '<sheetFormatPr defaultColWidth="24" defaultRowHeight="18"/>'
        f'<sheetData>{"".join(sheet_rows_xml)}</sheetData>'
        "</worksheet>"
    )


def _create_xlsx_bytes(sheets: list[tuple[str, list[list]]]) -> bytes:
    """Packs multiple (sheet_name, rows) tuples into a valid OpenXML `.xlsx` ZIP archive."""
    out_buf = io.BytesIO()
    with zipfile.ZipFile(out_buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        # 1. [Content_Types].xml
        overrides = "".join(
            f'<Override PartName="/xl/worksheets/sheet{i}.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            for i in range(1, len(sheets) + 1)
        )
        content_types = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/styles.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
            f"{overrides}"
            "</Types>"
        )
        zf.writestr("[Content_Types].xml", content_types.encode("utf-8"))

        # 2. _rels/.rels
        root_rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
            'Target="xl/workbook.xml"/>'
            "</Relationships>"
        )
        zf.writestr("_rels/.rels", root_rels.encode("utf-8"))

        # 3. xl/workbook.xml
        sheet_Nodes = "".join(
            f'<sheet name="{_xml_escape(name[:31])}" sheetId="{i}" r:id="rId{i}"/>'
            for i, (name, _) in enumerate(sheets, start=1)
        )
        workbook_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            f"<sheets>{sheet_Nodes}</sheets>"
            "</workbook>"
        )
        zf.writestr("xl/workbook.xml", workbook_xml.encode("utf-8"))

        # 4. xl/_rels/workbook.xml.rels
        wb_rels_items = "".join(
            f'<Relationship Id="rId{i}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
            f'Target="worksheets/sheet{i}.xml"/>'
            for i in range(1, len(sheets) + 1)
        )
        style_rid = len(sheets) + 1
        wb_rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f"{wb_rels_items}"
            f'<Relationship Id="rId{style_rid}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
            'Target="styles.xml"/>'
            "</Relationships>"
        )
        zf.writestr("xl/_rels/workbook.xml.rels", wb_rels.encode("utf-8"))

        # 5. xl/styles.xml (Default + Bold Header style s="1")
        styles_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<fonts count="2">'
            '<font><sz val="11"/><name val="Arial"/></font>'
            '<font><b/><sz val="11"/><name val="Arial"/></font>'
            "</fonts>"
            '<fills count="2">'
            '<fill><patternFill patternType="none"/></fill>'
            '<fill><patternFill patternType="gray125"/></fill>'
            "</fills>"
            '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
            '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
            '<cellXfs count="2">'
            '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
            '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>'
            "</cellXfs>"
            "</styleSheet>"
        )
        zf.writestr("xl/styles.xml", styles_xml.encode("utf-8"))

        # 6. Worksheets
        for i, (_, rows) in enumerate(sheets, start=1):
            zf.writestr(f"xl/worksheets/sheet{i}.xml", _build_worksheet_xml(rows).encode("utf-8"))

    return out_buf.getvalue()


def generate_project_excel_boq(payload: dict) -> bytes:
    """
    Generates a 5-sheet RTL Excel (.xlsx) workbook with full Value Engineering BoQ,
    Contractor Constructability & Developer Yield analysis, Architect Action Package,
    and Quantitative Area schedules.
    """
    if not isinstance(payload, dict):
        payload = {}

    project_title = str(payload.get("project_name") or payload.get("title") or payload.get("project_id") or payload.get("id") or "פרויקט")
    ds = payload.get("project_data_summary") or payload.get("data_summary") or {}
    opt = payload.get("design_optimization") or ds.get("design_optimization") or {}
    kpis = opt.get("executive_kpis") or {}
    net_bk = opt.get("net_avoidable_cost_breakdown") or {}
    guarantees = opt.get("zero_damage_guarantees") or {}
    construct = opt.get("contractor_constructability_and_yield") or {}
    pkg = payload.get("architect_action_package") or (ds.get("summary_document") or {}).get("architect_action_package") or {}

    # Sheet 1: Executive Summary & Zero-Damage Guarantees
    sheet1_rows = [
        ["מדד / קטגוריה", "ערך", "יחידה", "הסבר ובקרת איכות (Zero-Trust)"],
        ["שם הפרויקט", project_title, "", str(payload.get("subtitle") or "")],
        ["סטטוס אימות הנדסי", str(opt.get("validation_status") or "UNKNOWN"), "", str(guarantees.get("guarantee_statement") or "")],
        ["חיסכון ישיר מכיווץ קונטור עילי", float(kpis.get("above_ground_saving_ils") or 0), "₪", f"{float(kpis.get('above_ground_saved_sqm') or 0):.1f} מ״ר × 6,200 ₪/מ״ר"],
        ["חיסכון ישיר מכיווץ קונטור מרתף", float(kpis.get("underground_saving_ils") or 0), "₪", f"{float(kpis.get('underground_saved_sqm') or 0):.1f} מ״ר × 3,500 ₪/מ״ר"],
        ["חיסכון המרת חיפוי יבש לטיח בחזיתות", float(kpis.get("facade_saving_ils") or 0), "₪", f"{float(kpis.get('facade_converted_to_plaster_sqm') or 0):.1f} מ״ר × 550 ₪/מ״ר"],
        ["סה״כ חיסכון ישיר ברוטו (ללא מע״מ)", float(kpis.get("grand_total_direct_saving_ils") or 0), "₪", "סכום חיסכון קונטור עילי + מרתף + חזיתות"],
        ["קיזוז עלויות יישום, תפרים ותכנון מחדש", float((net_bk.get("implementation_and_transition_cost_ils") or 0) + (net_bk.get("redesign_and_coordination_cost_ils") or 0)), "₪", "עלויות מעבר ושינויי תכנון"],
        ["סה״כ חיסכון נטו בר-השגה (Net Avoidable Saving)", float(kpis.get("grand_total_net_avoidable_saving_ils") or 0), "₪", "חיסכון בנייה נטו לאחר כל הקיזוזים"],
        ["חיסכון ייעול ביצוע לקבלן (אלומיניום, טפסנות, MEP, שינויי דיירים)", float(construct.get("total_constructability_saving_ils") or 0), "₪", "4 צירי ייעול ביצוע ורכש לקבלן"],
        ["השבחת פדיון יזמי (מחסנים מוצמדים + מ״ר אפקטיבי בדירות)", float(construct.get("total_developer_yield_uplift_ils") or 0), "₪", "השבחת ערך שיווקי (מופרד מעלויות הבנייה)"],
        ["שטח דירות שנשמר במלואו (0 פגיעה)", float(guarantees.get("apartment_saleable_area_preserved_sqm") or 0), "מ״ר", "0.0 מ״ר גריעה משטח פלדלת"],
        ["מצבת חניות שנשמרת במלואה (0 פגיעה)", int(guarantees.get("parking_spaces_preserved") or 0), "חניות", "0 גריעת חניות תוך שמירת מיסעות ורמפות"],
    ]

    # Sheet 2: Value Engineering & BoQ Items
    sheet2_rows = [
        ["מזהה סעיף", "קטגוריה", "קומה / חזית", "כותרת הסעיף", "שטח מאומת לחיסכון (מ״ר)", "תעריף יחידה (₪/מ״ר)", "חיסכון כספי ישיר (₪)", "שטח כלוא שסווג להשבחה (מ״ר)", "פעולה הנדסית נדרשת"],
    ]
    ag_opt = opt.get("above_ground_optimization") or {}
    for item in (ag_opt.get("items") or []):
        sheet2_rows.append([
            item.get("id", ""),
            "קונטור עילי (AG)",
            item.get("floor", ""),
            item.get("title", ""),
            float(item.get("saved_sqm") or 0.0),
            float(ag_opt.get("rate_per_sqm_ils") or 6200),
            int(item.get("saving_ils") or 0),
            float(item.get("non_contour_reclassified_sqm") or 0.0),
            item.get("design_solution", ""),
        ])
    ug_opt = opt.get("underground_optimization") or {}
    for item in (ug_opt.get("items") or []):
        sheet2_rows.append([
            item.get("id", ""),
            "קונטור מרתפים וחניון (UG)",
            item.get("floor", ""),
            item.get("title", ""),
            float(item.get("saved_sqm") or 0.0),
            float(ug_opt.get("rate_per_sqm_ils") or 3500),
            int(item.get("saving_ils") or 0),
            float(item.get("non_contour_reclassified_sqm") or 0.0),
            item.get("design_solution", ""),
        ])
    fac_opt = opt.get("facade_cladding_optimization") or {}
    for fdir in (fac_opt.get("by_direction") or []):
        sheet2_rows.append([
            f"FAC-{fdir.get('direction', '')}",
            "אופטימיזציית חיפוי חזיתות (FAC)",
            fdir.get("direction", ""),
            f"המרת חיפוי יבש לטיח אקרילי/סיליקטי ({fdir.get('direction', '')})",
            float(fdir.get("converted_to_plaster_sqm") or 0.0),
            float(fac_opt.get("diff_rate_per_sqm_ils") or 550),
            int(fdir.get("saving_ils") or 0),
            0.0,
            fdir.get("architectural_rationale", ""),
        ])

    # Sheet 3: Contractor Constructability & Developer Revenue Yield
    sheet3_rows = [
        ["מזהה ציר", "סיווג כלכלי", "כותרת הציר", "היקף כמותי", "מצב קיים (לפני)", "פתרון הנדסי/ביצועי (אחרי)", "נוסחת תחשיב", "אומדן ערך / חיסכון (₪)", "נהנה עיקרי"],
    ]
    for p in (construct.get("pillars") or []):
        sheet3_rows.append([
            p.get("id", ""),
            p.get("category", ""),
            p.get("title", ""),
            p.get("metric_label", ""),
            p.get("before_state", ""),
            p.get("after_state", ""),
            p.get("formula_he", ""),
            int(p.get("estimated_saving_ils") or 0),
            p.get("benefit_owner", ""),
        ])

    # Sheet 4: Architect Action Package (Decision Table)
    sheet4_rows = [
        ["מזהה", "מקור", "עדיפות", "קומה / חתך", "אזור / חדר", "בעיה תכנונית / הנדסית", "פעולה נדרשת לתיקון", "השפעה כמותית / כספית", "בסיס תקני / מקצועי", "החלטת אדריכל"],
    ]
    for row in (pkg.get("decision_rows") or []):
        sheet4_rows.append([
            row.get("id", ""),
            row.get("source_label", ""),
            row.get("priority_label", ""),
            row.get("floor_label", ""),
            row.get("element_label", ""),
            row.get("issue_summary", ""),
            row.get("required_action", ""),
            row.get("quantified_delta", ""),
            row.get("normative_basis", ""),
            row.get("status_label", "ממתין להחלטת אדריכל"),
        ])

    # Sheet 5: Quantitative Areas & Flooring Schedule
    sheet5_rows = [
        ["קטגוריה", "קומה / אזור", "סה״כ שטח (מ״ר)", "שטח דירות נטו (מ״ר)", "שטח ליבה ושירות (מ״ר)", "סוג ריצוף וגימור"],
    ]
    for f_row in ((ds.get("above_ground_areas") or {}).get("by_floor") or []):
        sheet5_rows.append([
            "בנייה עילית",
            f_row.get("floor", ""),
            float(f_row.get("total_sqm") or 0.0),
            float(f_row.get("net_apt_sqm") or 0.0),
            float(f_row.get("core_sqm") or 0.0),
            f_row.get("flooring", ""),
        ])
    for u_row in ((ds.get("underground_areas") or {}).get("by_floor") or []):
        sheet5_rows.append([
            "מרתפים וחניון",
            u_row.get("floor", ""),
            float(u_row.get("total_sqm") or 0.0),
            0.0,
            float(u_row.get("total_sqm") or 0.0),
            u_row.get("flooring", ""),
        ])

    return _create_xlsx_bytes([
        ("תקציר מנהלים ואפס-נזק", sheet1_rows),
        ("הנדסת ערך וכתב כמויות", sheet2_rows),
        ("ייעול לקבלן והשבחת פדיון", sheet3_rows),
        ("טבלת החלטות לאדריכל", sheet4_rows),
        ("שטחים וריצוף לפי קומות", sheet5_rows),
    ])
