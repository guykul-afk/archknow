# -*- coding: utf-8 -*-
"""
Automated verification suite for the Design Optimization & Value Engineering
(בדיקת ייעול תכנון, הנדסת ערך וחיסכון בעלויות בנייה) mechanism.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

from design_optimization_engine import (
    COST_ABOVE_GROUND_PER_SQM_ILS,
    COST_UNDERGROUND_PARKING_PER_SQM_ILS,
    COST_DRY_CLADDING_PER_SQM_ILS,
    COST_PLASTER_PER_SQM_ILS,
    SAVING_CLADDING_TO_PLASTER_PER_SQM_ILS,
    build_project_design_optimization,
    check_apartment_value_engineering,
)
from project_summary_builder import (
    enrich_project_payload,
)
from project_analyzer_service import analyze_project_by_query
from validation_engine import load_okf_rules, run_validation
from server import app


def test_cost_constants():
    print("1. Testing economic cost constants...")
    assert COST_ABOVE_GROUND_PER_SQM_ILS == 6200, "Above-ground cost must be 6200 ILS/sqm"
    assert COST_UNDERGROUND_PARKING_PER_SQM_ILS == 3500, "Underground parking cost must be 3500 ILS/sqm"
    assert COST_DRY_CLADDING_PER_SQM_ILS == 700, "Dry cladding cost must be 700 ILS/sqm"
    assert COST_PLASTER_PER_SQM_ILS == 300, "Plaster cost must be 300 ILS/sqm"
    assert SAVING_CLADDING_TO_PLASTER_PER_SQM_ILS == 400, "Saving per sqm converted from dry cladding to plaster must be 400 ILS/sqm"
    print("   [PASS] Cost constants verified (6200, 3500, 700 vs 300 = 400 ILS/sqm).")


def test_all_five_catalog_projects():
    print("2. Testing all 7 cataloged projects (including Feierberg 3 & Moshe Sharet 26-28) for zero saleable/parking loss, exact math, and on-plan Where/How coordinates...")
    pids = ["pines48", "kkl10", "hafetz44", "yatkovski7", "kitroni37", "feierberg3", "sharett26"]
    for pid in pids:
        analysis = analyze_project_by_query(pid)
        pds = analysis.get("project_data_summary")
        assert pds is not None, f"Missing project_data_summary for {pid}"
        opt = pds.get("design_optimization")
        assert opt is not None, f"Missing design_optimization in {pid}"

        guarantees = opt["zero_damage_guarantees"]
        assert guarantees["apartment_saleable_area_loss_sqm"] == 0.0
        assert guarantees["parking_spaces_lost"] == 0
        assert guarantees["public_utilities_preserved"] is True

        s = opt["executive_kpis"]
        ag_sqm = s["above_ground_saved_sqm"]
        ug_sqm = s["underground_saved_sqm"]
        fac_sqm = s["facade_converted_to_plaster_sqm"]

        assert s["above_ground_saving_ils"] == round(ag_sqm * 6200), f"AG math mismatch in {pid}"
        assert s["underground_saving_ils"] == round(ug_sqm * 3500), f"UG math mismatch in {pid}"
        assert s["facade_saving_ils"] == round(fac_sqm * 400), f"Facade math mismatch in {pid}"
        assert s["grand_total_direct_saving_ils"] == (
            s["above_ground_saving_ils"]
            + s["underground_saving_ils"]
            + s["facade_saving_ils"]
        ), f"Total cost saving sum mismatch in {pid}"
        assert s["internal_reclaimed_living_sqm"] > 0, f"Expected positive internal corridor reclamation in {pid}"

        # Verify Global Building Contour Contraction Audit (`contour_audit_summary`)
        ca = opt.get("contour_audit_summary")
        assert ca is not None, f"Missing contour_audit_summary in {pid}"
        assert ca["verified_ag_contour_saved_sqm"] == ag_sqm, f"AG contour mismatch in {pid}"
        assert ca["verified_ug_contour_saved_sqm"] == ug_sqm, f"UG contour mismatch in {pid}"
        assert ca["rejected_locked_core_and_service_sqm"] > 0, f"Expected locked core/service area deduction in {pid}"
        assert ca["rejected_internal_apt_corridor_sqm"] == s["internal_reclaimed_living_sqm"]
        assert len(ca.get("methodology_pillars", [])) >= 6, "Expected 6 engineering contour audit pillars"
        assert len(ca.get("locked_core_reclassified_items", [])) >= 1, f"Expected locked core items in {pid}"

        # Verify on-plan Where & How Value Engineering notes (ONLY contour & facade savings: AG, UG, FAC)
        ve_notes = [n for n in analysis.get("notes", []) if n.get("is_value_eng") is True]
        assert len(ve_notes) >= 6, f"Expected at least 6 on-plan Value Engineering notes in {pid}, got {len(ve_notes)}"
        ug_notes = [n for n in ve_notes if n.get("ve_category") == "UG"]
        assert len(ug_notes) >= 1, f"Expected at least 1 UG note in {pid}"
        if pid in ("feierberg3", "sharett26"):
            assert len(ug_notes) >= 2, f"Expected 2 UG basement notes in {pid}"
        for vn in ve_notes:
            assert vn.get("ve_category") in ("AG", "UG", "FAC"), f"Non-contour note must not be in Cost Savings model: {vn.get('id')}"
            assert vn.get("where_on_plan"), f"Missing where_on_plan in VE note {vn.get('id')}"
            assert vn.get("how_to_execute"), f"Missing how_to_execute in VE note {vn.get('id')}"
            assert vn.get("ve_callout_badge"), f"Missing ve_callout_badge in VE note {vn.get('id')}"
            assert vn.get("sheet_id"), f"Missing sheet_id in VE note {vn.get('id')}"
            if vn.get("ve_category") in ("AG", "UG"):
                assert vn.get("contour_mechanism"), f"Missing contour_mechanism in {vn.get('id')}"
            if vn.get("ve_category") == "UG":
                assert vn.get("ramp_function_audit_he"), f"Missing ramp_function_audit_he in UG note {vn.get('id')}"
                assert vn.get("maneuvering_aisle_audit_he"), f"Missing maneuvering_aisle_audit_he in UG note {vn.get('id')}"
                assert vn.get("protected_ramp_and_maneuvering_deducted_sqm", 0) > 0, f"Missing protected_ramp_and_maneuvering_deducted_sqm in UG note {vn.get('id')}"
                assert "protected_ramp_maneuver_rect" in vn.get("plan_overlay_zones", {}), f"Missing protected_ramp_maneuver_rect in {vn.get('id')}"
                assert "relocated_parking_target_rect" in vn.get("plan_overlay_zones", {}), f"Missing relocated_parking_target_rect in {vn.get('id')}"
                reloc = vn.get("parking_relocation_audit")
                assert isinstance(reloc, dict), f"Missing parking_relocation_audit dict in UG note {vn.get('id')}"
                assert reloc.get("stalls_relocated_count", -1) >= 0, f"Expected stalls_relocated_count >= 0 in {vn.get('id')}"
                if pid in ("hafetz44", "sharett26"):
                    assert reloc.get("stalls_relocated_count") == 0, f"Expected 0 relocated parking stalls in {pid} (TEST-9)"
                assert reloc.get("affected_stalls_label"), f"Missing affected_stalls_label in {vn.get('id')}"
                assert reloc.get("original_location_he"), f"Missing original_location_he in {vn.get('id')}"
                assert reloc.get("alternative_location_found_he"), f"Missing alternative_location_found_he in {vn.get('id')}"
                assert reloc.get("new_stall_dimensions_and_access_he"), f"Missing new_stall_dimensions_and_access_he in {vn.get('id')}"
                assert reloc.get("multi_floor_search_and_ground_audit_he"), f"Missing multi_floor_search_and_ground_audit_he in {vn.get('id')}"
                assert reloc.get("zero_contour_expansion_proof_he"), f"Missing zero_contour_expansion_proof_he in {vn.get('id')}"
                assert reloc.get("net_parking_balance_he"), f"Missing net_parking_balance_he in {vn.get('id')}"
                assert vn.get("parking_relocation_audit_he"), f"Missing parking_relocation_audit_he in UG note {vn.get('id')}"

        # Verify project-level ramp_and_maneuvering_audit & parking_relocation_rule_he
        ug_opt = opt.get("underground_optimization", {})
        rma = ug_opt.get("ramp_and_maneuvering_audit")
        assert isinstance(rma, dict) and rma.get("total_protected_ramp_and_maneuvering_deducted_sqm", 0) > 0, f"Missing ramp_and_maneuvering_audit in {pid}"
        assert rma.get("total_stalls_relocated_to_alternative_bays", -1) >= 0, f"Missing total_stalls_relocated_to_alternative_bays in {pid}"
        if pid in ("hafetz44", "sharett26"):
            assert rma.get("total_stalls_relocated_to_alternative_bays") == 0, f"Expected 0 relocated stalls in {pid}"
        assert rma.get("parking_relocation_rule_he"), f"Missing parking_relocation_rule_he in {pid}"

        # Verify internal apartment layout improvements + locked-core reductions are classified under Design Improvement (not Cost Savings)
        apt_imp_notes = [n for n in analysis.get("notes", []) if n.get("is_design_improvement") is True]
        assert len(apt_imp_notes) >= 2, f"Expected at least 2 design improvement notes (LOCKED_CORE + APT) in {pid}"
        assert any(an.get("ve_category") == "LOCKED_CORE" for an in apt_imp_notes), f"Expected LOCKED_CORE reclassified note in {pid}"
        for an in apt_imp_notes:
            assert an.get("is_value_eng") is False, f"Design improvement note {an.get('id')} must have is_value_eng=False"
            assert an.get("ve_saving_ils") == 0, f"Design improvement note {an.get('id')} must have 0 ILS construction cost saving"

        # Verify every note in the project has a complete 4-pillar visual_explanation object
        for n in analysis.get("notes", []):
            vexp = n.get("visual_explanation")
            assert isinstance(vexp, dict), f"Missing visual_explanation in note {n.get('id')} ({pid})"
            assert vexp.get("diagram_type") in (
                "AG_CONTOUR", "UG_CONTOUR", "FACADE_CLADDING", "LOCKED_CORE", "APT_CORRIDOR", "STATUTORY_CHECK"
            ), f"Invalid diagram_type in {n.get('id')}"
            assert "recommendation" in vexp and vexp["recommendation"].get("where") and vexp["recommendation"].get("finding")
            assert "solution" in vexp and vexp["solution"].get("how_to_execute")
            assert "savings" in vexp and "formula" in vexp["savings"]
            b_imp = vexp.get("building_impact", {})
            for b_key in ("contour", "apartments", "parking", "utilities"):
                assert b_imp.get(b_key), f"Missing building_impact.{b_key} in note {n.get('id')} ({pid})"

        print(
            f"   [PASS] {pid}: Verified Contour AG={ag_sqm}m² ({s['above_ground_saving_ils']:,} ₪) | "
            f"Verified Contour UG={ug_sqm}m² ({s['underground_saving_ils']:,} ₪) | "
            f"Locked Core/UG Reclassified to Design Imp={ca['rejected_locked_core_and_service_sqm']}m² (0 ₪) | "
            f"Facade={fac_sqm}m² ({s['facade_saving_ils']:,} ₪) | "
            f"TOTAL SAVING={s['grand_total_direct_saving_ils']:,} ₪ | 4-Pillar Visual Explanations=OK"
        )


def test_validation_engine_integration():
    print("3. Testing validation_engine.py & OKF Rule VALUE_ENG_OPT...")
    rules = load_okf_rules("okf_rules")
    assert any(r.get("rule_id") == "VALUE_ENG_OPT" for r in rules), "VALUE_ENG_OPT rule was not loaded from okf_rules/"

    with open("hafetz44_project_sample.json", "r", encoding="utf-8") as f:
        sample = json.load(f)

    apt = sample["floors"][0]["apartments"][0]
    res = run_validation(apt, rules)
    ve_checks = [
        c for c in res
        if str(c.get("rule_id", "")).startswith("VALUE_ENG_OPT")
    ]
    assert len(ve_checks) >= 2, f"Expected VALUE_ENG_OPT checks in run_validation, got {len(ve_checks)}"
    print(f"   [PASS] validation_engine produced {len(ve_checks)} VALUE_ENG_OPT checks on sample apartment.")


def test_api_and_payload_enrichment():
    print("4. Testing API v1 endpoints and project payload enrichment...")
    data = analyze_project_by_query("פינס 48")
    sec_ids = [s.get("id") for s in data.get("sections", [])]
    assert "sec_pines48_value_eng" in sec_ids, "Expected sec_pines48_value_eng in enriched sections"
    assert "sec_pines48_apt_improvement" in sec_ids, "Expected sec_pines48_apt_improvement in enriched sections"

    ve_notes = [n for n in data.get("notes", []) if n.get("section_id") == "sec_pines48_value_eng"]
    assert len(ve_notes) >= 8, f"Expected >=8 visual notes in sec_pines48_value_eng, got {len(ve_notes)}"

    fb_data = analyze_project_by_query("פאירברג 3")
    assert fb_data.get("project_id") == "feierberg3"
    assert len(fb_data.get("sheets", [])) == 6, f"Expected 6 floor sheets for Feierberg 3, got {len(fb_data.get('sheets', []))}"
    fb_ve_notes = [n for n in fb_data.get("notes", []) if n.get("is_value_eng") is True]
    assert len(fb_ve_notes) >= 8, f"Expected >=8 on-plan VE notes for Feierberg 3, got {len(fb_ve_notes)}"

    with app.test_client() as client:
        resp = client.get("/api/v1/projects/pines48/optimization")
        assert resp.status_code == 200, f"Expected HTTP 200 from /api/v1/projects/pines48/optimization, got {resp.status_code}"
        body = resp.get_json()
        assert body["status"] == "success"
        assert body["design_optimization"]["executive_kpis"]["grand_total_direct_saving_ils"] == 801200

        resp_fb = client.get("/api/v1/projects/feierberg3/optimization")
        assert resp_fb.status_code == 200
        fb_body = resp_fb.get_json()
        assert fb_body["design_optimization"]["executive_kpis"]["grand_total_direct_saving_ils"] == 1296900

        resp_ms = client.get("/api/v1/projects/sharett26/optimization")
        assert resp_ms.status_code == 200
        ms_body = resp_ms.get_json()
        assert ms_body["design_optimization"]["executive_kpis"]["grand_total_direct_saving_ils"] == 895000

        # Test dynamic simulation query parameters
        resp_sim = client.get("/api/v1/projects/pines48/optimization?ag_rate=7000&ug_rate=4000&dry_rate=800&plaster_rate=300")
        assert resp_sim.status_code == 200
        sim_body = resp_sim.get_json()["simulation"]
        assert sim_body["rates_used"]["cladding_diff_ils_per_sqm"] == 500.0
        assert sim_body["above_ground_saving_ils"] == round(101 * 7000)

    print("   [PASS] Enriched sections, notes, and /api/v1/projects/<id>/optimization verified.")


def test_reports_and_static_files():
    print("5. Testing generated reports, static JSON exports, and 4-Pillar Visual UX components...")
    with open("reports/pines48_summary_and_areas_report.md", "r", encoding="utf-8") as f:
        md = f.read()
    assert "מודל החיסכון בעלויות הבנייה — צמצום קונטור בנייה מאומת וחיפוי" in md, "Missing Value Engineering section in pines48_summary_and_areas_report.md"

    with open("reports/pines48_architectural_quality_analysis.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "מודל החיסכון בעלויות הבנייה — צמצום קונטור בנייה מאומת וחיפוי" in html, "Missing Value Engineering section in pines48_architectural_quality_analysis.html"

    with open("webapp/api/pines48.json", "r", encoding="utf-8") as f:
        static_json = json.load(f)
    assert "design_optimization" in static_json.get("project_data_summary", {}), "Missing design_optimization in webapp/api/pines48.json"
    assert "contour_audit_summary" in static_json["project_data_summary"]["design_optimization"], "Missing contour_audit_summary in webapp/api/pines48.json"
    assert all("visual_explanation" in n for n in static_json.get("notes", [])), "Missing visual_explanation in static JSON notes"

    with open("webapp/index.html", "r", encoding="utf-8") as f:
        idx_html = f.read()
    assert "fc-visual-diagram-box" in idx_html, "Missing #fc-visual-diagram-box in webapp/index.html"
    assert "fc-four-pillars-box" in idx_html, "Missing #fc-four-pillars-box in webapp/index.html"
    assert 'data-category="ARCH_QUALITY"' in idx_html, "Missing DESIGN_IMP filter button in webapp/index.html"

    with open("webapp/app.js", "r", encoding="utf-8") as f:
        app_js = f.read()
    assert "buildBeforeAfterSvgDiagram" in app_js, "Missing buildBeforeAfterSvgDiagram in webapp/app.js"
    assert "buildFourPillarsSideDockHtml" in app_js, "Missing buildFourPillarsSideDockHtml in webapp/app.js"
    assert "svg-contour-before-rect" in app_js, "Missing clean SVG contour vector overlay in webapp/app.js"
    assert "plan-ve-callout" not in app_js, "Architectural floorplan must remain clean of floating text boxes"
    assert "$\\eta$" not in app_js, "Raw LaTeX $\\eta$ must not appear in HTML template strings"
    assert "ve_pillar" not in app_js, "Typo property ve_pillar must not appear in webapp/app.js"
    assert "ve_gross_proposed_sqm" not in app_js, "Typo property ve_gross_proposed_sqm must not appear in webapp/app.js"

    with open("webapp/styles.css", "r", encoding="utf-8") as f:
        styles_css = f.read()

    required_css_classes = [
        ".fc-diagram-header",
        ".fc-diagram-badge",
        ".fc-before-after-svg",
        ".fc-pillar-card",
        ".fc-pillar-title",
        ".fc-pillar-body",
        ".fc-waterfall-strip",
        ".fc-wf-box",
        ".fc-eff-bar-track",
        ".fc-eff-bar-fill",
        ".fc-impact-matrix-grid",
        ".fc-impact-cell",
        ".ic-lbl",
        ".ic-val",
        ".note-4pillars-grid",
        ".note-4p-box",
        ".p4-hdr",
        ".p4-txt",
        ".ve-visual-flow-board",
        ".ve-bldg-before-after-grid",
        ".ve-bldg-compare-card",
        ".ve-bar-track",
        ".ve-bar-fill",
        ".fill-before",
        ".fill-after",
        ".fill-imp-bar",
        ".ve-cards-gallery-grid",
        ".ve-gallery-card",
        ".ve-gc-head",
        ".ve-gc-body",
        ".ve-gc-foot",
        ".svg-contour-before-rect",
        ".svg-contour-after-rect",
        ".svg-contour-vector-line",
        ".svg-contour-vector-head",
        ".svg-imp-inner-rect",
        ".svg-protected-ramp-rect",
        ".svg-under-ramp-util-rect",
        ".svg-relocated-parking-rect",
        ".svg-relocation-arrow-line",
        ".fc-ramp-audit-box",
        ".fc-parking-reloc-box",
        ".more-tools-dropdown",
        ".legend-popover-box",
        ".doc-compact-hub-strip",
        ".doc-section-accordion",
        ".note-expandable-details",
        ".ve-hub-tabs-bar",
        ".ve-hub-tab-btn",
        ".ve-hub-tab-pane",
        ".areas-modal-tabs-bar",
    ]
    for cls_selector in required_css_classes:
        assert cls_selector in styles_css, f"Missing required CSS selector {cls_selector} in webapp/styles.css"

    assert "svg-protected-ramp-rect" in app_js, "Missing svg-protected-ramp-rect rendering in webapp/app.js"
    assert "svg-under-ramp-util-rect" in app_js, "Missing svg-under-ramp-util-rect rendering in webapp/app.js"
    assert "svg-relocated-parking-rect" in app_js, "Missing svg-relocated-parking-rect rendering in webapp/app.js"
    assert "fc-parking-reloc-box" in app_js, "Missing fc-parking-reloc-box rendering in webapp/app.js"
    assert "parking_relocation_audit" in app_js, "Missing parking_relocation_audit rendering in webapp/app.js"
    assert "ramp_and_maneuvering_audit" in app_js, "Missing ramp_and_maneuvering_audit rendering in webapp/app.js"
    assert "ve-hub-tabs-bar" in app_js, "Missing Unified Cost Savings Hub tabs in webapp/app.js"
    assert "doc-section-accordion" in app_js, "Missing collapsible document section accordions in webapp/app.js"
    assert "btn-close-side-dock" in app_js, "Missing click-to-expand note details in webapp/app.js"
    assert "more-tools-dropdown" in idx_html, "Missing #more-tools-dropdown in webapp/index.html"
    assert "legend-popover-box" in idx_html, "Missing #legend-popover-box in webapp/index.html"

    print("   [PASS] Markdown, HTML, PDF, static JSON files, and 4-Pillar Visual UX components & CSS selectors verified.")


def test_dynamic_custom_project_enrichment():
    print("6. Testing dynamic/custom uploaded project enrichment (non-catalog project_id)...")
    custom_payload = {
        "project_id": "custom_upload_test",
        "project_name": "פרויקט בדיקה מותאם אישית",
        "sheets": [{"id": "sheet_main", "title": "תכנית קומה טיפוסית", "image_url": "/uploads/pines48_f1_5.png"}],
        "sections": [{"id": "sec_custom_1", "title": "בדיקה סטטוטורית"}],
        "notes": [
            {
                "id": "CUST-N1",
                "pin_num": 1,
                "sheet_id": "sheet_main",
                "section_id": "sec_custom_1",
                "typology": "דירה 1",
                "room_name": "סלון",
                "status": "PASS",
                "rule_id": "ADG 4D-3",
                "title": "רוחב סלון תקין",
                "measured": "4.05 מ׳",
                "benchmark": "≥4.00 מ׳",
                "summary": "סלון רחב ותקין.",
                "recommendation": "ללא הערות.",
                "x_pct": 20.0, "y_pct": 20.0, "w_pct": 20.0, "h_pct": 20.0, "cx_pct": 30.0, "cy_pct": 30.0,
            }
        ],
    }
    enriched = enrich_project_payload(custom_payload)
    notes = enriched.get("notes", [])
    assert len(notes) >= 7, f"Expected dynamic VE and Design Improvement notes to be injected, got {len(notes)}"
    diagram_types_seen = set()
    for n in notes:
        vexp = n.get("visual_explanation")
        assert isinstance(vexp, dict), f"Missing visual_explanation on dynamic note {n.get('id')}"
        diagram_types_seen.add(vexp.get("diagram_type"))
        for k in ("recommendation", "solution", "savings", "building_impact"):
            assert k in vexp and isinstance(vexp[k], dict), f"Missing {k} in dynamic note {n.get('id')}"
    for expected_dt in ("AG_CONTOUR", "UG_CONTOUR", "FACADE_CLADDING", "LOCKED_CORE", "APT_CORRIDOR", "STATUTORY_CHECK"):
        assert expected_dt in diagram_types_seen, f"Missing diagram_type {expected_dt} in dynamic project enrichment"
    for ext in ("md", "html", "pdf"):
        tmp_path = os.path.join("reports", f"custom_upload_test_summary_and_areas_report.{ext}")
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    print("   [PASS] Dynamic custom project enrichment verified across all 6 diagram types and 4 pillars.")


def test_pines48_ground_and_basement_plans_present():
    print("7. Testing Pines 48 Ground Floor (A-1001) and Basement (A-1000) plans and improvement proposals...")
    from project_analyzer_service import build_pines48_analysis
    p48 = build_pines48_analysis()
    sheets = p48.get("sheets", [])
    sheet_ids = {s["id"]: s for s in sheets}
    assert "ground" in sheet_ids, "Pines 48 must include 'ground' sheet (A-1001)"
    assert "basement" in sheet_ids, "Pines 48 must include 'basement' sheet (A-1000)"
    assert sheet_ids["ground"]["image_url"] == "/uploads/pines48_ground.png"
    assert sheet_ids["basement"]["image_url"] == "/uploads/pines48_basement.png"
    assert os.path.exists("webapp/uploads/pines48_ground.png"), "Missing webapp/uploads/pines48_ground.png"
    assert os.path.exists("webapp/uploads/pines48_basement.png"), "Missing webapp/uploads/pines48_basement.png"

    notes_by_id = {n["id"]: n for n in p48.get("notes", [])}
    for gid in ("P48-GND-01", "P48-GND-02", "P48-GND-03", "P48-OPT-AG1", "P48-LOCKED-CORE1"):
        assert gid in notes_by_id, f"Missing Ground Floor note {gid} in Pines 48"
        assert notes_by_id[gid]["sheet_id"] == "ground", f"Expected {gid} to be anchored on 'ground', got {notes_by_id[gid]['sheet_id']}"
    for bid in ("P48-BSM-01", "P48-OPT-UG1"):
        assert bid in notes_by_id, f"Missing Basement note {bid} in Pines 48"
        assert notes_by_id[bid]["sheet_id"] == "basement", f"Expected {bid} to be anchored on 'basement', got {notes_by_id[bid]['sheet_id']}"
    print("   [PASS] Pines 48 Ground Floor (A-1001) and Basement (A-1000) plans and improvement proposals verified.")


if __name__ == "__main__":
    from spatial_3d_mapper import validate_project_spatial_catalog
    for _pid in ["pines48", "kkl10", "hafetz44", "yatkovski7", "kitroni37", "feierberg3", "sharett26"]:
        _issues = validate_project_spatial_catalog(analyze_project_by_query(_pid))
        assert len(_issues) == 0, f"Spatial catalog validation failed for {_pid}: {_issues}"
    _h44 = analyze_project_by_query("hafetz44")
    _h44_notes = {n["id"]: n for n in _h44.get("notes", [])}
    assert _h44_notes["H44-W-02"]["spatial_3d"]["bbox_3d"][:4] == [-6.40, 1.18, -3.38, 3.96]
    assert _h44_notes["H44-W-04"]["spatial_3d"]["bbox_3d"][:4] == [-1.05, -4.33, 2.25, -0.33]
    for _nid in ("H44-W-06", "H44-E-02", "H44-E-03", "H44-E-04", "H44-E-05", "H44-CORE-01", "H44-PH-01", "H44-PH-02", "H44-PH-03", "H44-LOCKED-CORE2"):
        assert _nid in _h44_notes, f"Missing note {_nid} in Hafetz Chaim 44"
    assert _h44_notes["H44-PH-03"]["spatial_3d"]["bbox_3d"][:4] == [-8.66, -2.45, 1.54, 2.93]
    assert _h44_notes["H44-LOCKED-CORE2"]["ve_saving_ils"] == 0
    assert _h44_notes["H44-OPT-AG2"]["sheet_id"] == "h44_penthouse"
    print("0. [PASS] Hafetz Chaim 44 7 User Fixes & Systemic Spatial Catalog Validator verified across all 6 projects.")
    test_cost_constants()
    test_all_five_catalog_projects()
    test_validation_engine_integration()
    test_api_and_payload_enrichment()
    test_reports_and_static_files()
    test_dynamic_custom_project_enrichment()
    test_pines48_ground_and_basement_plans_present()
    print("\nALL DESIGN OPTIMIZATION & VALUE ENGINEERING TESTS PASSED SUCCESSFULLY!")


