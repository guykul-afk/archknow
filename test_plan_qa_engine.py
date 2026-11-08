# -*- coding: utf-8 -*-
"""
Unit & Integration Tests for the Interactive Plan Q&A and Action Engine (`plan_qa_engine.py`)
and Flask endpoints (`/api/ask_plan`, `/api/v1/ai/ask`).
"""

import re
import pytest
from project_analyzer_service import analyze_project_by_query
from plan_qa_engine import (
    answer_plan_question,
    build_project_qa_knowledge_index,
    classify_question_intent,
)
from validation_engine import FORBIDDEN_META_JARGON_PATTERNS


def test_qa_knowledge_index_attached_to_all_projects():
    for pid in ("hafetz44", "pines48", "kkl10", "yatkovski7", "kitroni37", "feierberg3", "sharett26", "em_hamoshavot"):
        payload = analyze_project_by_query(pid, rebuild_artifacts=False)
        q_idx = payload.get("qa_knowledge_index")
        assert isinstance(q_idx, dict), f"Missing qa_knowledge_index for {pid}"
        assert q_idx.get("project_id") == pid
        assert len(q_idx.get("sample_questions", [])) >= 6
        assert isinstance(q_idx.get("typical_floor_redesign"), dict)
        assert len(q_idx.get("living_kitchen_profiles", [])) >= 1
        assert len(q_idx.get("rooms_windows_analysis", [])) >= 3


def test_three_user_example_questions_and_data_structure():
    payload = analyze_project_by_query("hafetz44", rebuild_artifacts=False)

    # 1. Living Room & Kitchen Improvement
    q1 = "תמליץ על דרך לשפר את אזור הסלון והמטבח"
    assert classify_question_intent(q1) == "LIVING_KITCHEN"
    a1 = answer_plan_question(payload, q1)
    assert a1["intent"] == "LIVING_KITCHEN"
    assert len(a1["comparison_table"]["rows"]) >= 5
    assert len(a1["sections"]) >= 3
    assert len(a1["recommended_architect_actions"]) >= 2
    assert a1["system_actions"]["auto_switch_sheet_id"] is not None

    # 2. Typical Floor Redesign within same Building Lines (Apartments vs Public Ratio)
    q2 = "תמליץ על דרך לתכנן מחדש קומה טיפוסית באותו קווי הבניין על מנת לשפר את יחס השטח בין הדירות לציבורי"
    assert classify_question_intent(q2) == "TYPICAL_FLOOR_RATIO"
    a2 = answer_plan_question(payload, q2)
    assert a2["intent"] == "TYPICAL_FLOOR_RATIO"
    assert len(a2["comparison_table"]["rows"]) >= 4
    assert "קווי בניין" in a2["executive_summary_he"] or "קווי הבניין" in a2["executive_summary_he"]
    assert len(a2["recommended_architect_actions"]) >= 2

    # 3. Window Openings Analysis & Recommendations
    q3 = "נתח את מפתח החלונות בתכנית ותמליץ על שיפורים"
    assert classify_question_intent(q3) == "WINDOWS_OPENINGS"
    a3 = answer_plan_question(payload, q3)
    assert a3["intent"] == "WINDOWS_OPENINGS"
    assert len(a3["comparison_table"]["rows"]) >= 4
    assert "secondary_table" in a3 and len(a3["secondary_table"]["rows"]) >= 4
    assert len(a3["recommended_architect_actions"]) >= 2

    # 4. System Analysis Data Structure
    q4 = "פרט על מבנה המידע של הניתוח שכרגע נשמר במערכת"
    assert classify_question_intent(q4) == "DATA_STRUCTURE"
    a4 = answer_plan_question(payload, q4)
    assert a4["intent"] == "DATA_STRUCTURE"
    assert len(a4["comparison_table"]["rows"]) >= 5

    # Verify zero forbidden meta-jargon across all answers
    for ans in (a1, a2, a3, a4):
        blob = f"{ans.get('answer_title', '')} {ans.get('executive_summary_he', '')} {ans.get('sections', '')}"
        for pat in FORBIDDEN_META_JARGON_PATTERNS:
            assert not re.search(pat, blob), f"Forbidden meta-jargon matched '{pat}'"


def test_flask_ask_plan_endpoints():
    from server import app

    client = app.test_client()
    resp = client.post(
        "/api/ask_plan",
        json={
            "project_id": "hafetz44",
            "question": "תמליץ על דרך לשפר את אזור הסלון והמטבח",
        },
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "success"
    assert data["project_id"] == "hafetz44"
    assert data["answer"]["intent"] == "LIVING_KITCHEN"

    resp_v1 = client.post(
        "/api/v1/ai/ask",
        json={
            "project_id": "pines48",
            "question": "נתח את מפתח החלונות בתכנית ותמליץ על שיפורים",
        },
    )
    assert resp_v1.status_code == 200
    data_v1 = resp_v1.get_json()
    assert data_v1["status"] == "success"
    assert data_v1["project_id"] == "pines48"
    assert data_v1["answer"]["intent"] == "WINDOWS_OPENINGS"


def test_atkg_4_layer_schema_and_graph_reasoner():
    import os
    import json
    from atkg_spatial_graph import load_okf_refactoring_patterns, build_portfolio_atkg_index

    patterns = load_okf_refactoring_patterns()
    assert len(patterns) >= 4

    all_payloads = []
    for pid in ("hafetz44", "pines48", "kkl10", "yatkovski7", "kitroni37", "feierberg3", "sharett26"):
        payload = analyze_project_by_query(pid, rebuild_artifacts=False)
        all_payloads.append(payload)
        atkg = payload.get("atkg_spatial_graph")
        assert isinstance(atkg, dict), f"Missing atkg_spatial_graph for {pid}"
        assert atkg.get("schema_version") == "ATKG-4.0-BOT-OKF"
        assert "layer_1_bim_spatial_atlas" in atkg
        assert "layer_2_topology_and_mutability_graph" in atkg
        assert "layer_3_okf_knowledge_bindings" in atkg
        assert "layer_4_design_deltas_and_views" in atkg

        walls = atkg["layer_2_topology_and_mutability_graph"]["walls_mutability_matrix"]
        assert len(walls) >= 6
        assert any(w["mutability_class"] == "LOCKED_MAMAD_WALL" and not w["can_shift"] for w in walls)
        assert any(w["mutability_class"] == "FLEXIBLE_DRY_PARTITION" and w["can_shift"] for w in walls)

        ai_twin_md = atkg.get("ai_twin_compact_md", "")
        assert len(ai_twin_md) > 1000
        assert "Wall Mutability Matrix" in ai_twin_md

    # Test Portfolio Index
    port_idx = build_portfolio_atkg_index(all_payloads)
    assert port_idx["projects_count"] == 7
    assert len(port_idx["projects_comparison_matrix"]) == 7

    # Test ATKG Graph Reasoner queries (Wall Mutability, Portfolio Compare, WFH)
    h44 = all_payloads[0]
    ans_walls = answer_plan_question(h44, "אילו קירות בדירה ובגרעין ניתנים להזזה ואילו קירות נעולים לפי גרף ה-ATKG?")
    assert ans_walls["intent"] == "WALL_MUTABILITY_ANALYSIS"
    assert len(ans_walls.get("reasoning_chain_he", [])) >= 3

    ans_port = answer_plan_question(h44, "השווה את ניצולת הקומה הטיפוסית בפרויקט זה מול שאר הפרויקטים במערכת", portfolio_index=port_idx)
    assert ans_port["intent"] == "PORTFOLIO_COMPARISON"
    assert len(ans_port["comparison_table"]["rows"]) == 7

    ans_wfh = answer_plan_question(h44, "איך ניתן לשלב פינת עבודה מהבית או משרד ביתי בדירה?")
    assert ans_wfh["intent"] == "WFH_FLEXIBILITY_SYNTHESIS"
    assert len(ans_wfh.get("reasoning_chain_he", [])) >= 3

    # Check zero forbidden meta-jargon across ATKG answers
    for ans in (ans_walls, ans_port, ans_wfh):
        blob = json.dumps(ans, ensure_ascii=False)
        for pat in FORBIDDEN_META_JARGON_PATTERNS:
            assert not re.search(pat, blob), f"Forbidden meta-jargon matched '{pat}'"

    # Verify Gemini 4 / 3.8 / 3.7 / 3.5 / 3.1 models catalog and Thinking-part JSON parser
    from llm_reasoning_agent import (
        DEFAULT_GEMINI_MODEL,
        SUPPORTED_GEMINI_MODELS,
        _extract_gemini_json_and_thoughts,
        discover_live_gemini_models,
    )
    model_ids = [m["id"] for m in SUPPORTED_GEMINI_MODELS]
    assert "gemini-4-argon" in model_ids
    assert "gemini-3.8-flash" in model_ids
    assert "gemini-3.7-flash" in model_ids
    assert "gemini-3.5-flash" in model_ids
    assert "gemini-3.5-flash-lite" in model_ids
    assert DEFAULT_GEMINI_MODEL in ("gemini-3.8-flash", "gemini-4-argon")
    assert len(discover_live_gemini_models("")) >= 5

    sample_thinking_parts = [
        {"thought": True, "text": "בודק קירות ממ״ד וקירות גמישים..."},
        {"text": '```json\n{"answer_title": "בדיקת מודל 3.1", "executive_summary_he": "תקין"}\n```'},
    ]
    parsed_json, thoughts = _extract_gemini_json_and_thoughts(sample_thinking_parts)
    assert parsed_json is not None
    assert parsed_json["answer_title"] == "בדיקת מודל 3.1"
    assert len(thoughts) == 1


def test_gemini_api_cost_calculation_and_top_right_indicator():
    """
    Verifies the exact Gemini API cost formula:
      Cost_USD = (uncached_input / 1M * R_in) + (cached / 1M * R_cached) + ((candidates + thoughts) / 1M * R_out)
    including:
    - Thinking tokens (`thoughtsTokenCount`) billed at Output rate
    - Context caching deduction (`cachedContentTokenCount`)
    - <=200k vs >200k context tiering
    - Daily / Weekly / Cumulative aggregation
    - Top-right UI widget (`#hdr-api-cost-widget` inside `.brand-area`) in `webapp/index.html`.
    """
    from llm_reasoning_agent import (
        USD_TO_ILS_RATE,
        calculate_gemini_call_cost,
        get_api_usage_summary,
    )

    # 1. Test standard <=200k tier with Thinking tokens and Cached tokens on gemini-3.8-flash
    # Rates for gemini-3.8-flash (<=200k): input=$0.75/1M, cached=$0.075/1M, output=$3.75/1M
    usage_meta = {
        "promptTokenCount": 10_000,
        "cachedContentTokenCount": 2_000,
        "candidatesTokenCount": 1_000,
        "thoughtsTokenCount": 1_000,
        "totalTokenCount": 12_000,
    }
    cost_res = calculate_gemini_call_cost("gemini-3.8-flash", usage_metadata=usage_meta)
    assert cost_res["token_source"] == "EXACT_USAGE_METADATA"
    assert cost_res["context_tier"] == "<=200k"
    assert cost_res["uncached_input_tokens"] == 8_000
    assert cost_res["cached_tokens"] == 2_000
    assert cost_res["billable_output_tokens"] == 2_000  # candidates (1000) + thoughts (1000)
    expected_usd = (8_000 / 1e6) * 0.75 + (2_000 / 1e6) * 0.075 + (2_000 / 1e6) * 3.75
    assert abs(cost_res["cost_usd"] - round(expected_usd, 6)) < 1e-7
    assert abs(cost_res["cost_ils"] - round(expected_usd * USD_TO_ILS_RATE, 4)) < 1e-4

    # 2. Test >200k long-context tier on gemini-3.1-pro-preview
    # Rates for gemini-3.1-pro-preview (>200k): input=$4.00/1M, cached=$0.40/1M, output=$18.00/1M
    long_meta = {
        "promptTokenCount": 250_000,
        "cachedContentTokenCount": 50_000,
        "candidatesTokenCount": 2_000,
        "thoughtsTokenCount": 3_000,
        "totalTokenCount": 255_000,
    }
    long_res = calculate_gemini_call_cost("gemini-3.1-pro-preview", usage_metadata=long_meta)
    assert long_res["context_tier"] == ">200k"
    assert long_res["uncached_input_tokens"] == 200_000
    assert long_res["billable_output_tokens"] == 5_000
    expected_long_usd = (200_000 / 1e6) * 4.00 + (50_000 / 1e6) * 0.40 + (5_000 / 1e6) * 18.00
    assert abs(long_res["cost_usd"] - round(expected_long_usd, 6)) < 1e-7

    # 3. Test Daily / Weekly / Cumulative summary aggregation
    import datetime
    import time
    now_ms = int(time.time() * 1000)
    today_ymd = datetime.datetime.now().strftime("%Y-%m-%d")
    mock_events = [
        {**cost_res, "date_ymd": today_ymd, "epoch_ms": now_ms - 10_000},
        {**long_res, "date_ymd": "2026-01-01", "epoch_ms": now_ms - (3 * 86400 * 1000)},  # 3 days ago -> in weekly & cumulative, not daily
        {**cost_res, "date_ymd": "2025-01-01", "epoch_ms": now_ms - (30 * 86400 * 1000)},  # 30 days ago -> only in cumulative
    ]
    summary = get_api_usage_summary(events_override=mock_events)
    assert summary["daily"]["calls_count"] == 1
    assert summary["weekly"]["calls_count"] == 2
    assert summary["cumulative"]["calls_count"] == 3
    assert summary["cumulative"]["cost_usd"] > summary["weekly"]["cost_usd"] > summary["daily"]["cost_usd"] > 0

    # 4. Verify Top-Right Widget (`#hdr-api-cost-widget` inside `.brand-area`) in `webapp/index.html`
    import os
    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "webapp", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_txt = f.read()
    assert 'id="hdr-api-cost-widget"' in html_txt
    assert 'id="hdr-cost-daily"' in html_txt
    assert 'id="hdr-cost-weekly"' in html_txt
    assert 'id="hdr-cost-cum"' in html_txt
    assert 'id="api-cost-breakdown-modal"' in html_txt



