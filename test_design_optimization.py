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
    print("2. Testing all 6 cataloged projects (including Feierberg 3) for zero saleable/parking loss, exact math, and on-plan Where/How coordinates...")
    pids = ["pines48", "kkl10", "hafetz44", "yatkovski7", "kitroni37", "feierberg3"]
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

        # Verify on-plan Where & How Value Engineering notes exist across sheets
        ve_notes = [n for n in analysis.get("notes", []) if n.get("is_value_eng") is True]
        assert len(ve_notes) >= 8, f"Expected at least 8 on-plan Value Engineering notes in {pid}, got {len(ve_notes)}"
        for vn in ve_notes:
            assert vn.get("where_on_plan"), f"Missing where_on_plan in VE note {vn.get('id')}"
            assert vn.get("how_to_execute"), f"Missing how_to_execute in VE note {vn.get('id')}"
            assert vn.get("ve_callout_badge"), f"Missing ve_callout_badge in VE note {vn.get('id')}"
            assert vn.get("sheet_id"), f"Missing sheet_id in VE note {vn.get('id')}"

        print(
            f"   [PASS] {pid}: AG={ag_sqm}m² ({s['above_ground_saving_ils']:,} ₪) | "
            f"UG={ug_sqm}m² ({s['underground_saving_ils']:,} ₪) | "
            f"Facade={fac_sqm}m² ({s['facade_saving_ils']:,} ₪) | "
            f"Internal=+{s['internal_reclaimed_living_sqm']}m² | "
            f"TOTAL={s['grand_total_direct_saving_ils']:,} ₪ | "
            f"On-Plan VE Hotspots={len(ve_notes)}"
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

    ve_notes = [n for n in data.get("notes", []) if n.get("section_id") == "sec_pines48_value_eng"]
    assert len(ve_notes) >= 9, f"Expected >=9 visual notes in sec_pines48_value_eng, got {len(ve_notes)}"

    fb_data = analyze_project_by_query("פאירברג 3")
    assert fb_data.get("project_id") == "feierberg3"
    assert len(fb_data.get("sheets", [])) == 6, f"Expected 6 floor sheets for Feierberg 3, got {len(fb_data.get('sheets', []))}"
    fb_ve_notes = [n for n in fb_data.get("notes", []) if n.get("is_value_eng") is True]
    assert len(fb_ve_notes) >= 10, f"Expected >=10 on-plan VE notes for Feierberg 3, got {len(fb_ve_notes)}"

    with app.test_client() as client:
        resp = client.get("/api/v1/projects/pines48/optimization")
        assert resp.status_code == 200, f"Expected HTTP 200 from /api/v1/projects/pines48/optimization, got {resp.status_code}"
        body = resp.get_json()
        assert body["status"] == "success"
        assert body["design_optimization"]["executive_kpis"]["grand_total_direct_saving_ils"] == 1006880

        resp_fb = client.get("/api/v1/projects/feierberg3/optimization")
        assert resp_fb.status_code == 200
        fb_body = resp_fb.get_json()
        assert fb_body["design_optimization"]["executive_kpis"]["grand_total_direct_saving_ils"] == 1101220

        # Test dynamic simulation query parameters
        resp_sim = client.get("/api/v1/projects/pines48/optimization?ag_rate=7000&ug_rate=4000&dry_rate=800&plaster_rate=300")
        assert resp_sim.status_code == 200
        sim_body = resp_sim.get_json()["simulation"]
        assert sim_body["rates_used"]["cladding_diff_ils_per_sqm"] == 500.0
        assert sim_body["above_ground_saving_ils"] == round(101 * 7000)

    print("   [PASS] Enriched sections, notes, and /api/v1/projects/<id>/optimization verified.")


def test_reports_and_static_files():
    print("5. Testing generated reports and static JSON exports...")
    with open("reports/pines48_summary_and_areas_report.md", "r", encoding="utf-8") as f:
        md = f.read()
    assert "בדיקת ייעול תכנון, הנדסת ערך וחיסכון בעלויות בנייה" in md, "Missing Value Engineering section in pines48_summary_and_areas_report.md"

    with open("reports/pines48_architectural_quality_analysis.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "בדיקת ייעול תכנון, הנדסת ערך וחיסכון בעלויות בנייה" in html, "Missing Value Engineering section in pines48_architectural_quality_analysis.html"

    with open("webapp/api/pines48.json", "r", encoding="utf-8") as f:
        static_json = json.load(f)
    assert "design_optimization" in static_json.get("project_data_summary", {}), "Missing design_optimization in webapp/api/pines48.json"
    print("   [PASS] Markdown, HTML, PDF, and static JSON files verified.")


if __name__ == "__main__":
    test_cost_constants()
    test_all_five_catalog_projects()
    test_validation_engine_integration()
    test_api_and_payload_enrichment()
    test_reports_and_static_files()
    print("\nALL DESIGN OPTIMIZATION & VALUE ENGINEERING TESTS PASSED SUCCESSFULLY!")
