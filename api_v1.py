# -*- coding: utf-8 -*-
"""
ArchiCheck (ArchKnow) - AI & External Agent REST API (v1)

This module provides a production-grade API designed specifically for external
AI systems, LLM agents (ChatGPT Custom GPTs, Claude Projects, LangChain, CrewAI,
AutoGen, Cursor, Windsurf, etc.), and programmatic architectural analysis.

Features:
- Standardized RESTful endpoints with rich query filtering.
- AI-tailored token-budgeted executive summaries (pre-formatted Markdown + structured JSON).
- Semantic & keyword context packer for LLM RAG / prompt injection (/ai/context).
- Cross-project benchmarking & spatial metrics comparisons.
- Rule discovery against the OKF (Open Knowledge Format) architectural standards.
- Custom plan validation (JSON payloads and file uploads).
- Pre-baked OpenAI Function Calling & Anthropic Tools definitions (/ai/tools).
- Standard OpenAPI 3.1.0 specification (/openapi.json) for 1-click Custom GPT Actions.
- Interactive Swagger UI documentation (/docs).
- Configurable API Key authentication via header 'X-API-Key' or 'Authorization: Bearer <token>'.
"""

import os
import json
import functools
from flask import Blueprint, request, jsonify, make_response, render_template_string, send_file
from project_analyzer_service import get_projects_catalog, analyze_project_by_query
from validation_engine import run_validation, load_okf_rules

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OKF_RULES_DIR = os.path.join(BASE_DIR, 'okf_rules')
CLIENT_PY_PATH = os.path.join(BASE_DIR, 'archknow_client.py')
API_KEY_ENV = os.environ.get("ARCHKNOW_API_KEY", "").strip()


@api_v1.route('/client.py', methods=['GET'])
@api_v1.route('/archknow_client.py', methods=['GET'])
def download_client_sdk():
    """Serves the standalone archknow_client.py connector file for direct download by external AI systems."""
    return send_file(
        CLIENT_PY_PATH,
        mimetype='text/x-python',
        as_attachment=False,
        download_name='archknow_client.py'
    )

# Lazy cache for loaded OKF rules to optimize response times
_CACHED_RULES = None


def get_cached_rules():
    global _CACHED_RULES
    if _CACHED_RULES is None:
        try:
            if os.path.exists(OKF_RULES_DIR):
                _CACHED_RULES = load_okf_rules(OKF_RULES_DIR)
            else:
                _CACHED_RULES = []
        except Exception as e:
            _CACHED_RULES = []
    return _CACHED_RULES


def require_api_key(view_func):
    """
    Optional API Key protection.
    If ARCHKNOW_API_KEY is configured in the environment, validates the header.
    Otherwise allows open access (development / demo mode).
    """
    @functools.wraps(view_func)
    def decorated_function(*args, **kwargs):
        if not API_KEY_ENV or API_KEY_ENV.lower() in ("none", "development", "disabled", "false"):
            return view_func(*args, **kwargs)

        auth_header = request.headers.get("Authorization", "")
        api_key_header = request.headers.get("X-API-Key", "")
        token = None

        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
        elif api_key_header:
            token = api_key_header.strip()

        if not token or token != API_KEY_ENV:
            return jsonify({
                "status": "error",
                "error_code": "UNAUTHORIZED",
                "message": "Invalid or missing API key. Provide via 'X-API-Key' header or 'Authorization: Bearer <key>'."
            }), 401

        return view_func(*args, **kwargs)
    return decorated_function


@api_v1.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-API-Key, Accept'
    if not API_KEY_ENV:
        response.headers['X-Auth-Mode'] = 'open'
    else:
        response.headers['X-Auth-Mode'] = 'key-required'
    return response


@api_v1.route('/<path:dummy>', methods=['OPTIONS'])
@api_v1.route('/', methods=['OPTIONS'])
def options_preflight(dummy=''):
    return ('', 204)


# =====================================================================
# 1. Health & Status
# =====================================================================

@api_v1.route('/health', methods=['GET'])
def health():
    """System health check and architectural analysis engine status."""
    catalog = get_projects_catalog()
    rules = get_cached_rules()
    return jsonify({
        "status": "healthy",
        "service": "ArchiCheck Architectural Quality AI API",
        "version": "1.0.0",
        "loaded_projects_count": len(catalog),
        "loaded_okf_rules_count": len(rules),
        "auth_required": bool(API_KEY_ENV),
        "supported_standards": [
            "Israeli Statutory Planning & Building Regulations",
            "Israeli Accessibility Standard IS 1918",
            "UK NDSS (Nationally Described Space Standard) & London Plan D6",
            "NSW Apartment Design Guide (ADG)",
            "Swiss WBS (Wohnungs-Bewertungs-System)",
            "NKBA Kitchen & Bathroom Planning Guidelines",
            "Alexander Pattern Language for Housing",
            "Space Syntax & SAGA Spatial Topology Metrics"
        ]
    })


# =====================================================================
# 2. Projects & Analysis Endpoints
# =====================================================================

@api_v1.route('/projects', methods=['GET'])
@require_api_key
def list_projects():
    """
    List all cataloged architectural projects with summary stats and quick links.
    Query params:
      - q: filter projects by name or keyword
    """
    query = request.args.get('q', '').strip().lower()
    catalog = get_projects_catalog()

    if query:
        filtered = []
        for p in catalog:
            combined_text = f"{p.get('id', '')} {p.get('name', '')} {p.get('short_name', '')} {p.get('subtitle', '')} {' '.join(p.get('keywords', []))}".lower()
            if query in combined_text:
                filtered.append(p)
        projects = filtered
    else:
        projects = catalog

    # Format project items with direct API resource links for agents
    results = []
    for p in projects:
        pid = p.get('id')
        results.append({
            "id": pid,
            "name": p.get('name'),
            "short_name": p.get('short_name'),
            "subtitle": p.get('subtitle'),
            "score": p.get('score'),
            "status_summary": p.get('status_summary'),
            "keywords": p.get('keywords', []),
            "pdf_report_url": p.get('pdf_report_url'),
            "links": {
                "self": f"/api/v1/projects/{pid}",
                "analysis": f"/api/v1/projects/{pid}/analysis",
                "summary_for_ai": f"/api/v1/projects/{pid}/summary",
                "spatial_metrics": f"/api/v1/projects/{pid}/spatial-metrics",
                "optimization": f"/api/v1/projects/{pid}/optimization"
            }
        })

    return jsonify({
        "status": "success",
        "total": len(results),
        "projects": results
    })


@api_v1.route('/projects/<project_id>', methods=['GET'])
@require_api_key
def get_project_details(project_id):
    """
    Get detailed metadata, sheets (plans), sections, and high-level KPIs for a specific project.
    """
    analysis = analyze_project_by_query(project_id)
    if not analysis or analysis.get('project_id') != project_id:
        # Check if project exists in catalog
        catalog = {p['id']: p for p in get_projects_catalog()}
        if project_id not in catalog:
            return jsonify({
                "status": "error",
                "error_code": "PROJECT_NOT_FOUND",
                "message": f"Project '{project_id}' not found. Available IDs: {list(catalog.keys())}"
            }), 404

    return jsonify({
        "status": "success",
        "project": {
            "project_id": analysis.get('project_id'),
            "project_name": analysis.get('project_name'),
            "project_subtitle": analysis.get('project_subtitle'),
            "overall_score": analysis.get('overall_score'),
            "metrics": analysis.get('metrics', []),
            "sheets_count": len(analysis.get('sheets', [])),
            "sheets": analysis.get('sheets', []),
            "sections_count": len(analysis.get('sections', [])),
            "sections": analysis.get('sections', []),
            "total_notes_count": len(analysis.get('notes', [])),
            "pdf_report_url": analysis.get('pdf_report_url'),
            "viewer_3d_url": analysis.get('viewer_3d_url'),
            "discovered_files_count": len(analysis.get('discovered_files', [])),
            "discovered_files": analysis.get('discovered_files', [])[:10],
            "model_3d_sync_status": analysis.get('model_3d_sync_status'),
            "bim_3d_validation": analysis.get('bim_3d_validation'),
            "project_data_summary": analysis.get('project_data_summary'),
            "links": {
                "analysis": f"/api/v1/projects/{project_id}/analysis",
                "summary_for_ai": f"/api/v1/projects/{project_id}/summary",
                "spatial_metrics": f"/api/v1/projects/{project_id}/spatial-metrics",
                "optimization": f"/api/v1/projects/{project_id}/optimization",
                "check_3d_update": f"/api/v1/projects/{project_id}/check-3d-update"
            }
        }
    })


@api_v1.route('/projects/<project_id>/check-3d-update', methods=['GET', 'POST'])
@require_api_key
def check_project_3d_model_update(project_id):
    """
    Checks whether the base 3D model for `project_id` has been modified or updated.
    If modified (or if `force=true`), automatically triggers a full new planning audit
    and returns the sync status, 3D BIM validation results, and updated audit summary.
    """
    from model_3d_change_detector import check_and_reaudit_project

    if request.method == 'POST':
        body = request.get_json(silent=True) or {}
        force = str(body.get('force', '')).lower() in ('1', 'true', 'yes')
    else:
        force = str(request.args.get('force', '')).lower() in ('1', 'true', 'yes')

    res = check_and_reaudit_project(project_id, force=force, rebuild_artifacts=True)
    return jsonify({
        "status": "success",
        "project_id": res.get("project_id"),
        "project_name": res.get("project_name"),
        "overall_score": res.get("overall_score"),
        "total_notes": res.get("total_notes"),
        "model_3d_sync_status": res.get("model_3d_sync_status"),
        "bim_3d_validation": res.get("bim_3d_validation"),
    })


@api_v1.route('/models/check-updates', methods=['GET', 'POST'])
@require_api_key
def check_all_models_updates():
    """
    Checks all projects' base 3D models in the Single Source of Truth repository.
    Runs a full new planning audit for any project whose base 3D model was updated.
    """
    from model_3d_change_detector import check_all_projects_3d_models

    if request.method == 'POST':
        body = request.get_json(silent=True) or {}
        force = str(body.get('force', '')).lower() in ('1', 'true', 'yes')
    else:
        force = str(request.args.get('force', '')).lower() in ('1', 'true', 'yes')

    summary = check_all_projects_3d_models(force=force, rebuild_artifacts=True)
    return jsonify({
        "status": "success",
        **summary,
    })


@api_v1.route('/projects/<project_id>/analysis', methods=['GET'])
@require_api_key
def get_project_analysis(project_id):
    """
    Get all architectural quality audit findings (notes) for a project with granular filtering.
    Designed for AI agents to pinpoint statutory failures, warnings, room-specific checks, or guidelines.

    Query parameters:
      - status: comma-separated statuses to include: 'FAIL', 'WARN', 'PASS' (e.g. 'FAIL,WARN')
      - rule_id: partial or exact rule ID match (e.g. 'B1.13', 'IS1918', 'NKBA', 'NDSS')
      - room: keyword match on room_name or typology (e.g. 'ממ"ד', 'מטבח', 'סלון', 'מרפסת')
      - sheet_id: filter by sheet/floor ID (e.g. 'f1_5', 'roof', 'basement')
      - section_id: filter by section ID
      - q: free-text keyword search across title, summary, and recommendation
      - limit: max number of items to return (default: 50, max: 200)
      - offset: starting item index (default: 0)
    """
    analysis = analyze_project_by_query(project_id)
    notes = analysis.get('notes', [])

    # Filter parameters
    status_filter = request.args.get('status', '').strip().upper()
    rule_id_filter = request.args.get('rule_id', '').strip().lower()
    room_filter = request.args.get('room', '').strip().lower()
    sheet_filter = request.args.get('sheet_id', '').strip()
    section_filter = request.args.get('section_id', '').strip()
    q_filter = request.args.get('q', '').strip().lower()

    try:
        limit = min(int(request.args.get('limit', 50)), 200)
        offset = max(int(request.args.get('offset', 0)), 0)
    except ValueError:
        limit = 50
        offset = 0

    allowed_statuses = set(status_filter.split(',')) if status_filter else None

    filtered_notes = []
    status_counts = {"PASS": 0, "WARN": 0, "FAIL": 0}

    for note in notes:
        st = note.get('status', 'INFO').upper()
        if st in status_counts:
            status_counts[st] += 1

        if allowed_statuses and st not in allowed_statuses:
            continue

        if rule_id_filter and rule_id_filter not in str(note.get('rule_id', '')).lower():
            continue

        if room_filter:
            target = f"{note.get('room_name', '')} {note.get('typology', '')}".lower()
            if room_filter not in target:
                continue

        if sheet_filter and note.get('sheet_id') != sheet_filter:
            continue

        if section_filter and note.get('section_id') != section_filter:
            continue

        if q_filter:
            searchable = f"{note.get('title', '')} {note.get('summary', '')} {note.get('recommendation', '')} {note.get('measured', '')} {note.get('benchmark', '')}".lower()
            if q_filter not in searchable:
                continue

        filtered_notes.append(note)

    paged_notes = filtered_notes[offset:offset + limit]

    return jsonify({
        "status": "success",
        "project_id": analysis.get('project_id'),
        "project_name": analysis.get('project_name'),
        "overall_score": analysis.get('overall_score'),
        "total_notes": len(notes),
        "total_matched": len(filtered_notes),
        "status_distribution": status_counts,
        "offset": offset,
        "limit": limit,
        "notes": paged_notes
    })


@api_v1.route('/projects/<project_id>/summary', methods=['GET'])
@require_api_key
def get_project_ai_summary(project_id):
    """
    AI-Optimized Executive Summary.
    Returns a token-budgeted, pre-formatted Markdown document + structured JSON
    tailored specifically for inclusion into external LLM prompts and agent reasoning loops.
    """
    analysis = analyze_project_by_query(project_id)
    notes = analysis.get('notes', [])

    fails = [n for n in notes if n.get('status') == 'FAIL']
    warns = [n for n in notes if n.get('status') == 'WARN']
    passes = [n for n in notes if n.get('status') == 'PASS']

    # Highlight top issues
    critical_issues = []
    for item in fails:
        critical_issues.append({
            "id": item.get('id'),
            "room": item.get('room_name'),
            "title": item.get('title'),
            "measured": item.get('measured'),
            "benchmark": item.get('benchmark'),
            "recommendation": item.get('recommendation')
        })

    key_warnings = []
    for item in warns[:8]:
        key_warnings.append({
            "id": item.get('id'),
            "room": item.get('room_name'),
            "title": item.get('title'),
            "measured": item.get('measured'),
            "benchmark": item.get('benchmark'),
            "recommendation": item.get('recommendation')
        })

    # Generate ready-to-inject Markdown summary
    md_lines = [
        f"# Architectural Quality & Compliance Audit: {analysis.get('project_name')}",
        f"**Subtitle:** {analysis.get('project_subtitle')}",
        f"**Overall Score:** {analysis.get('overall_score')} / 100",
        "",
        "## Summary Metrics",
        f"- **Passed Checks:** {len(passes)}",
        f"- **Quality Warnings (WARN):** {len(warns)} (benchmarks / ergonomic alerts)",
        f"- **Statutory Violations (FAIL):** {len(fails)} (statutory non-compliance)",
    ]

    for m in analysis.get('metrics', []):
        md_lines.append(f"- **{m.get('label')}:** {m.get('value')} ({m.get('sub', '')})")

    if fails:
        md_lines.append("\n## Critical Statutory Violations (FAIL)")
        for f in fails:
            md_lines.append(f"- **[{f.get('id')}] {f.get('title')}** ({f.get('room_name')}):")
            md_lines.append(f"  - Measured: `{f.get('measured')}` vs Required: `{f.get('benchmark')}`")
            md_lines.append(f"  - Fix: {f.get('recommendation')}")
    else:
        md_lines.append("\n## Statutory Compliance Status")
        md_lines.append("0 statutory failures detected. Full compliance with mandatory Israeli building code regulations.")

    if warns:
        md_lines.append("\n## Key Design & Ergonomic Warnings (WARN)")
        for w in warns[:6]:
            md_lines.append(f"- **[{w.get('id')}] {w.get('title')}** ({w.get('room_name')}):")
            md_lines.append(f"  - Measured: `{w.get('measured')}` vs Benchmark: `{w.get('benchmark')}`")
            md_lines.append(f"  - Recommendation: {w.get('recommendation')}")

    pds = analysis.get('project_data_summary', {})
    ag = pds.get('above_ground_areas', {})
    ug = pds.get('underground_areas', {})
    rt = pds.get('roof_terraces', {})
    sb = pds.get('suspended_balconies', {})
    fac = pds.get('facades', {})
    sdoc = pds.get('summary_document', {})

    if pds:
        md_lines.extend([
            "",
            "## Quantitative Project Areas & Facades Summary",
            f"- **Total Built Area (Above + Underground):** {pds.get('total_built_area_sqm')} sqm",
            f"- **Above-Ground Construction Area:** {ag.get('total_sqm')} sqm (Net Apartments: {ag.get('net_apartments_sqm')} sqm, Core/Service: {ag.get('core_and_service_sqm')} sqm)",
            f"- **Underground Construction Area:** {ug.get('total_sqm')} sqm ({ug.get('parking_spaces')} parking spaces)",
            f"- **Roof Terraces Area:** {rt.get('total_sqm')} sqm ({rt.get('count')} terraces)",
            f"- **Suspended/Cantilevered Balconies Area:** {sb.get('total_sqm')} sqm ({sb.get('count')} balconies)",
            f"- **Total Facades Area:** {fac.get('total_sqm')} sqm (Glazing: {fac.get('total_glazing_sqm')} sqm, Opaque: {fac.get('total_opaque_sqm')} sqm)",
        ])
        for d in fac.get('by_direction', []):
            md_lines.append(f"  - **{d.get('facade_name')}:** {d.get('gross_area_sqm')} sqm ({d.get('pct_of_total')}%)")

        opt = pds.get('design_optimization', {})
        if opt:
            opt_sum = opt.get('executive_kpis', {})
            md_lines.extend([
                "",
                "## Design Optimization & Value Engineering (ייעול תכנון וחיסכון בעלויות בנייה)",
                f"- **Total Potential Cost Saving:** {opt_sum.get('grand_total_direct_saving_ils', 0):,} ILS",
                f"- **Above-Ground Volume Saving (6,200 ILS/sqm):** {opt_sum.get('above_ground_saved_sqm', 0)} sqm ({opt_sum.get('above_ground_saving_ils', 0):,} ILS) | Zero loss to saleable apartment area (`0%` loss)",
                f"- **Underground Parking Saving (3,500 ILS/sqm):** {opt_sum.get('underground_saved_sqm', 0)} sqm ({opt_sum.get('underground_saving_ils', 0):,} ILS) | Zero loss to parking spaces",
                f"- **Facade Cladding Optimization (700 vs 300 = 400 ILS/sqm):** {opt_sum.get('facade_converted_to_plaster_sqm', 0)} sqm converted from dry cladding to plaster ({opt_sum.get('facade_saving_ils', 0):,} ILS)",
                f"- **Internal Apartment Layout Optimization:** +{opt_sum.get('internal_reclaimed_living_sqm', 0)} sqm reclaimed from corridors into living/bedroom areas",
            ])

        if sdoc.get('improvement_proposals'):
            md_lines.append("\n## Actionable Improvement Proposals")
            for idx, prop in enumerate(sdoc.get('improvement_proposals', []), 1):
                md_lines.append(f"{idx}. **[{prop.get('priority')}] {prop.get('target')}** — {prop.get('proposal')}")

    markdown_content = "\n".join(md_lines)
    approx_tokens = len(markdown_content) // 3  # rough estimate for mixed Hebrew/English

    return jsonify({
        "status": "success",
        "project_id": analysis.get('project_id'),
        "project_name": analysis.get('project_name'),
        "token_estimate": approx_tokens,
        "markdown_prompt_context": markdown_content,
        "structured": {
            "score": analysis.get('overall_score'),
            "counts": {
                "total": len(notes),
                "pass": len(passes),
                "warn": len(warns),
                "fail": len(fails)
            },
            "statutory_failures": critical_issues,
            "top_warnings": key_warnings,
            "metrics": analysis.get('metrics', []),
            "project_data_summary": pds
        }
    })


@api_v1.route('/projects/<project_id>/spatial-metrics', methods=['GET'])
@require_api_key
def get_project_spatial_metrics(project_id):
    """
    Extract dimensional, room, and space syntax topology metrics for a project.
    Reads detailed apartment JSON data when available on disk.
    """
    analysis = analyze_project_by_query(project_id)

    # Locate sample JSON if exists for richer spatial data
    sample_files = {
        "pines48": "pines48_apt_c_sample.json",
        "hafetz44": "hafetz44_project_sample.json",
        "yatkovski7": "yatkovski7_project_sample.json",
        "kitroni37": "kitroni37_project_sample.json",
        "feierberg3": "feierberg3_project_sample.json"
    }

    raw_sample = None
    fn = sample_files.get(project_id)
    if fn:
        p = os.path.join(BASE_DIR, fn)
        if os.path.exists(p):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    raw_sample = json.load(f)
            except Exception:
                pass

    spatial_data = {
        "project_id": project_id,
        "project_name": analysis.get('project_name'),
        "overall_score": analysis.get('overall_score'),
        "has_cad_raw_topology": bool(raw_sample),
        "sheets": [{"id": s.get('id'), "title": s.get('title'), "sheet_code": s.get('sheet_code')} for s in analysis.get('sheets', [])],
        "kpis": analysis.get('metrics', []),
        "project_data_summary": analysis.get('project_data_summary')
    }

    if raw_sample:
        if "floors" in raw_sample:
            apts = []
            for fl in raw_sample.get("floors", []):
                for apt in fl.get("apartments", []):
                    apts.append({
                        "apartment_id": apt.get("apartment_id"),
                        "bedrooms": apt.get("bedrooms"),
                        "bedspaces": apt.get("bedspaces"),
                        "net_area_sqm": apt.get("net_area_sqm"),
                        "orientations": apt.get("orientations", []),
                        "sunlight_hours": apt.get("sunlight_hours"),
                        "ceiling_height_m": apt.get("global_parameters", {}).get("ceiling_height_m"),
                        "storage": apt.get("storage", {}),
                        "rooms_count": len(apt.get("rooms", [])),
                        "rooms_sample": [{"name": r.get("room_name"), "type": r.get("room_type"), "area_sqm": r.get("area_sqm")} for r in apt.get("rooms", [])[:8]]
                    })
            spatial_data["apartments_spatial_breakdown"] = apts
        elif "rooms" in raw_sample:
            spatial_data["single_unit_breakdown"] = {
                "apartment_id": raw_sample.get("apartment_id"),
                "net_area_sqm": raw_sample.get("net_area_sqm"),
                "rooms": [{"name": r.get("room_name"), "type": r.get("room_type"), "area_sqm": r.get("area_sqm")} for r in raw_sample.get("rooms", [])]
            }

    return jsonify({
        "status": "success",
        "spatial_metrics": spatial_data
    })


@api_v1.route('/projects/<project_id>/optimization', methods=['GET'])
@require_api_key
def get_project_optimization(project_id):
    """
    Design Optimization & Value Engineering (בדיקת ייעול תכנון והנדסת ערך).
    Returns detailed cost-saving breakdown for above-ground volume (6,200 ILS/sqm),
    underground parking efficiency (3,500 ILS/sqm), facade dry cladding vs plaster
    ratio optimization (700 vs 300 = 400 ILS/sqm), and internal apartment corridor
    to living space reclamation — with zero loss to saleable apartment area or public utilities.

    Optional query parameters for dynamic simulation:
      - ag_rate: Above-ground construction cost per sqm (default: 6200)
      - ug_rate: Underground parking construction cost per sqm (default: 3500)
      - dry_rate: Rigid/dry cladding cost per sqm (default: 700)
      - plaster_rate: Exterior plaster cost per sqm (default: 300)
    """
    analysis = analyze_project_by_query(project_id)
    if not analysis:
        return jsonify({
            "status": "error",
            "error_code": "PROJECT_NOT_FOUND",
            "message": f"Project '{project_id}' not found."
        }), 404

    pds = analysis.get('project_data_summary', {})
    opt = pds.get('design_optimization', {})

    # Optional custom rate simulation
    try:
        ag_rate = float(request.args.get('ag_rate', 6200))
        ug_rate = float(request.args.get('ug_rate', 3500))
        dry_rate = float(request.args.get('dry_rate', 700))
        plaster_rate = float(request.args.get('plaster_rate', 300))
    except ValueError:
        ag_rate, ug_rate, dry_rate, plaster_rate = 6200.0, 3500.0, 700.0, 300.0

    opt_sum = opt.get('executive_kpis', {})
    ag_saved = float(opt_sum.get('above_ground_saved_sqm', 0))
    ug_saved = float(opt_sum.get('underground_saved_sqm', 0))
    fac_conv = float(opt_sum.get('facade_converted_to_plaster_sqm', 0))
    cladding_diff = max(0.0, dry_rate - plaster_rate)

    simulated = {
        "rates_used": {
            "above_ground_ils_per_sqm": ag_rate,
            "underground_ils_per_sqm": ug_rate,
            "dry_cladding_ils_per_sqm": dry_rate,
            "plaster_ils_per_sqm": plaster_rate,
            "cladding_diff_ils_per_sqm": cladding_diff
        },
        "above_ground_saving_ils": round(ag_saved * ag_rate),
        "underground_saving_ils": round(ug_saved * ug_rate),
        "facade_cladding_saving_ils": round(fac_conv * cladding_diff),
        "total_cost_saving_ils": round(ag_saved * ag_rate + ug_saved * ug_rate + fac_conv * cladding_diff)
    }

    return jsonify({
        "status": "success",
        "project_id": analysis.get('project_id'),
        "project_name": analysis.get('project_name'),
        "design_optimization": opt,
        "simulation": simulated
    })


@api_v1.route('/compare', methods=['GET'])
@require_api_key
def compare_projects():
    """
    Side-by-side benchmarking of architectural projects.
    Query params:
      - projects: comma-separated project IDs (e.g. 'pines48,kkl10,kitroni37').
                  Defaults to all 5 catalog projects if omitted.
    """
    catalog = get_projects_catalog()
    catalog_ids = [p['id'] for p in catalog]

    req_projects = request.args.get('projects', '').strip()
    if req_projects:
        target_ids = [pid.strip() for pid in req_projects.split(',') if pid.strip() in catalog_ids]
    else:
        target_ids = catalog_ids

    comparison_items = []
    for pid in target_ids:
        data = analyze_project_by_query(pid)
        notes = data.get('notes', [])
        fails = sum(1 for n in notes if n.get('status') == 'FAIL')
        warns = sum(1 for n in notes if n.get('status') == 'WARN')
        passes = sum(1 for n in notes if n.get('status') == 'PASS')

        comparison_items.append({
            "project_id": pid,
            "project_name": data.get('project_name'),
            "score": data.get('overall_score'),
            "total_checks": len(notes),
            "pass_count": passes,
            "warn_count": warns,
            "fail_count": fails,
            "pass_rate_pct": round((passes / len(notes) * 100) if notes else 0, 1),
            "metrics": data.get('metrics', []),
            "sheets_count": len(data.get('sheets', []))
        })

    # Sort by score descending
    comparison_items.sort(key=lambda x: x.get('score', 0), reverse=True)

    return jsonify({
        "status": "success",
        "total_compared": len(comparison_items),
        "comparison": comparison_items
    })


# =====================================================================
# 3. AI Context & Semantic Retrieval (for LLMs & RAG)
# =====================================================================

@api_v1.route('/ai/context', methods=['POST'])
@require_api_key
def get_ai_context():
    """
    Context Packer for External AI Systems.
    Given a question or topic and an optional project ID, extracts the most relevant
    architectural findings, benchmarks, statutory rules, and recommendations.
    Returns a ready-to-inject LLM context block.

    JSON Body:
      - query (str, required): The user query or question (e.g., 'מה הליקויים במיסעה ובממדים בקק״ל 10?')
      - project_id (str, optional): Target project ID (defaults to automatic keyword inference or 'pines48')
      - max_items (int, optional): Max relevant notes to include (default: 6)
    """
    body = request.get_json(silent=True) or {}
    query_text = body.get('query', '').strip()
    if not query_text:
        return jsonify({
            "status": "error",
            "error_code": "MISSING_QUERY",
            "message": "Field 'query' is required."
        }), 400

    project_id = body.get('project_id', '').strip()
    max_items = min(int(body.get('max_items', 6)), 20)

    # If project_id is not specified, resolve from query
    if not project_id:
        q_low = query_text.lower()
        if any(k in q_low for k in ["פאירברג", "פאיירברג", "פיארברג", "feierberg", "fairberg", "6387"]):
            project_id = "feierberg3"
        elif any(k in q_low for k in ["יטקובסקי", "yatkovski", "7א"]):
            project_id = "yatkovski7"
        elif any(k in q_low for k in ["קיטרוני", "קטרוני", "kitroni", "37"]):
            project_id = "kitroni37"
        elif any(k in q_low for k in ["חפץ", "hafetz", "44"]):
            project_id = "hafetz44"
        elif any(k in q_low for k in ["קקל", "קק\"ל", "קק״ל", "kkl", "10"]):
            project_id = "kkl10"
        else:
            project_id = "pines48"

    analysis = analyze_project_by_query(project_id)
    notes = analysis.get('notes', [])

    # Score notes by relevance to query tokens
    query_tokens = [t for t in query_text.lower().replace('"', '').replace("'", '').split() if len(t) > 1]

    scored = []
    for note in notes:
        score = 0
        searchable = f"{note.get('title', '')} {note.get('room_name', '')} {note.get('rule_id', '')} {note.get('summary', '')} {note.get('recommendation', '')}".lower()
        for tok in query_tokens:
            if tok in searchable:
                score += 2
        # Prioritize FAIL and WARN notes for engineering / audit queries
        if note.get('status') == 'FAIL':
            score += 3
        elif note.get('status') == 'WARN':
            score += 1

        if score > 0:
            scored.append((score, note))

    scored.sort(key=lambda x: x[0], reverse=True)
    top_notes = [item[1] for item in scored[:max_items]]

    # If no specific matches found, supply top fails and warns
    if not top_notes:
        top_notes = [n for n in notes if n.get('status') in ('FAIL', 'WARN')][:max_items]

    # Build prompt context text block
    prompt_context = [
        f"### ARCHITECTURAL AUDIT DATA: {analysis.get('project_name')}",
        f"- Score: {analysis.get('overall_score')}/100 | {analysis.get('project_subtitle')}",
        f"- User Query: {query_text}",
        "",
        "### RELEVANT FINDINGS & AUDIT NOTES:"
    ]

    for i, n in enumerate(top_notes, 1):
        prompt_context.append(f"{i}. [{n.get('status')}] {n.get('title')} (Room: {n.get('room_name')}, Rule: {n.get('rule_id')})")
        prompt_context.append(f"   - Measured Value: {n.get('measured')}")
        prompt_context.append(f"   - Standard/Benchmark: {n.get('benchmark')}")
        prompt_context.append(f"   - Engineering Summary: {n.get('summary')}")
        prompt_context.append(f"   - Recommended Solution: {n.get('recommendation')}")

    context_str = "\n".join(prompt_context)

    return jsonify({
        "status": "success",
        "resolved_project_id": analysis.get('project_id'),
        "project_name": analysis.get('project_name'),
        "matched_count": len(top_notes),
        "prompt_context": context_str,
        "findings": top_notes,
        "suggested_ai_instruction": "You are an expert Israeli architectural auditor. Answer the user query using the provided verified architectural findings and statutory benchmarks."
    })


# =====================================================================
# 4. OKF Architectural Rules Knowledge Base
# =====================================================================

@api_v1.route('/rules', methods=['GET'])
@require_api_key
def list_rules():
    """
    Search and explore OKF architectural rules and standards.
    Query params:
      - category: filter by category (e.g. 'Accessibility', 'Kitchen & Bathroom Ergonomics', 'Planning Standards')
      - q: free-text search in rule_id, description_summary, subcategory
      - limit: default 50, max 100
      - offset: default 0
    """
    rules = get_cached_rules()
    cat_filter = request.args.get('category', '').strip().lower()
    q_filter = request.args.get('q', '').strip().lower()

    try:
        limit = min(int(request.args.get('limit', 50)), 100)
        offset = max(int(request.args.get('offset', 0)), 0)
    except ValueError:
        limit = 50
        offset = 0

    filtered = []
    categories_set = set()

    for r in rules:
        c = r.get('category')
        if c:
            categories_set.add(c)

        if cat_filter and cat_filter not in str(c or '').lower():
            continue

        if q_filter:
            text = f"{r.get('rule_id', '')} {r.get('category', '')} {r.get('subcategory', '')} {r.get('description_summary', '')}".lower()
            if q_filter not in text:
                continue

        filtered.append(r)

    paged = filtered[offset:offset + limit]

    return jsonify({
        "status": "success",
        "total_rules": len(rules),
        "matched": len(filtered),
        "available_categories": sorted(list(categories_set)),
        "offset": offset,
        "limit": limit,
        "rules": paged
    })


@api_v1.route('/rules/<rule_id>', methods=['GET'])
@require_api_key
def get_rule_detail(rule_id):
    """Get full specification and thresholds for a specific rule ID."""
    rules = get_cached_rules()
    rule_id_clean = rule_id.strip().lower()

    for r in rules:
        if str(r.get('rule_id', '')).lower() == rule_id_clean:
            return jsonify({
                "status": "success",
                "rule": r
            })

    return jsonify({
        "status": "error",
        "error_code": "RULE_NOT_FOUND",
        "message": f"Rule '{rule_id}' not found."
    }), 404


# =====================================================================
# 5. Live Plan Validation & Upload
# =====================================================================

@api_v1.route('/analyze/plan', methods=['POST'])
@require_api_key
def analyze_custom_plan():
    """
    Validate a custom apartment schema JSON in real-time against statutory & OKF rules.

    Body: JSON representing an apartment object (net_area_sqm, bedrooms, ceiling_height, rooms array, etc.).
    """
    apartment_data = request.get_json(silent=True)
    if not apartment_data:
        return jsonify({
            "status": "error",
            "error_code": "INVALID_JSON",
            "message": "Request body must be valid JSON apartment data."
        }), 400

    rules = get_cached_rules()
    try:
        results = run_validation(apartment_data, rules)
    except Exception as e:
        return jsonify({
            "status": "error",
            "error_code": "VALIDATION_FAILED",
            "message": f"Engine validation error: {str(e)}"
        }), 500

    status_counts = {"PASS": 0, "WARN": 0, "FAIL": 0}
    for item in results:
        st = item.get('status', 'INFO').upper()
        if st in status_counts:
            status_counts[st] += 1

    return jsonify({
        "status": "success",
        "apartment_id": apartment_data.get('apartment_id', 'custom_unit'),
        "total_checks": len(results),
        "status_distribution": status_counts,
        "results": results
    })


# =====================================================================
# 6. AI Agent Tooling (OpenAI & Anthropic Schemas)
# =====================================================================

@api_v1.route('/ai/tools', methods=['GET'])
def get_ai_tools_spec():
    """
    Exports function calling tool definitions ready to be plugged directly into:
    - OpenAI Chat Completions API (`tools=[...]`)
    - Anthropic Claude API (`tools=[...]`)
    - LangChain / CrewAI / AutoGen agents
    """
    openai_tools = [
        {
            "type": "function",
            "function": {
                "name": "list_architectural_projects",
                "description": "Lists all architectural projects cataloged in the system with their compliance scores and summaries.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "q": {
                            "type": "string",
                            "description": "Optional search term to filter by project name or location"
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_project_ai_summary",
                "description": "Retrieves a token-budgeted, pre-formatted executive architectural summary for a project including scores, statutory violations, and recommendations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "Project ID (e.g. 'pines48', 'kkl10', 'hafetz44', 'yatkovski7', 'kitroni37')",
                            "enum": ["pines48", "kkl10", "hafetz44", "yatkovski7", "kitroni37"]
                        }
                    },
                    "required": ["project_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_project_audit_notes",
                "description": "Queries specific architectural quality audit findings (PASS/WARN/FAIL) with filtering by room type, rule ID, or statutory status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "Project ID (e.g. 'pines48', 'kkl10', 'hafetz44', 'yatkovski7', 'kitroni37')",
                            "enum": ["pines48", "kkl10", "hafetz44", "yatkovski7", "kitroni37"]
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by status: 'FAIL' (statutory violations), 'WARN' (design/ergonomic alerts), or 'PASS'",
                            "enum": ["FAIL", "WARN", "PASS", "FAIL,WARN"]
                        },
                        "room": {
                            "type": "string",
                            "description": "Optional room or space keyword (e.g. 'ממ\"ד', 'מטבח', 'מרפסת', 'חניה')"
                        },
                        "q": {
                            "type": "string",
                            "description": "Free text keyword to search in findings"
                        }
                    },
                    "required": ["project_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_ai_architectural_context",
                "description": "Extracts relevant architectural findings, measured values vs standards, and recommendations to answer a specific user query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The user query or topic to extract architectural context for"
                        },
                        "project_id": {
                            "type": "string",
                            "description": "Optional target project ID ('pines48', 'kkl10', 'hafetz44', 'yatkovski7', 'kitroni37')"
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "compare_architectural_projects",
                "description": "Compares 2 or more architectural projects across compliance scores, pass rates, room counts, and quality benchmarks.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "projects": {
                            "type": "string",
                            "description": "Comma-separated project IDs (e.g. 'pines48,kkl10,kitroni37')"
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_architectural_rules",
                "description": "Searches the OKF knowledge base of statutory Israeli codes, NDSS, NKBA ergonomics, and Space Syntax rules.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "q": {
                            "type": "string",
                            "description": "Keyword search (e.g. 'ממ\"ד', 'רוחב פרוזדור', 'אוורור', 'גובה תקרה')"
                        },
                        "category": {
                            "type": "string",
                            "description": "Category filter (e.g. 'Planning Standards', 'Accessibility', 'Kitchen & Bathroom Ergonomics')"
                        }
                    }
                }
            }
        }
    ]

    anthropic_tools = [
        {
            "name": tool["function"]["name"],
            "description": tool["function"]["description"],
            "input_schema": tool["function"]["parameters"]
        }
        for tool in openai_tools
    ]

    return jsonify({
        "status": "success",
        "description": "Tool calling specifications for AI Agents (OpenAI & Anthropic formats)",
        "openai_tools": openai_tools,
        "anthropic_tools": anthropic_tools
    })


# =====================================================================
# 7. OpenAPI 3.1.0 Specification (For Custom GPTs & Agents)
# =====================================================================

@api_v1.route('/openapi.json', methods=['GET'])
def get_openapi_spec():
    """Returns a full OpenAPI 3.1.0 schema specification for ChatGPT Custom GPT Actions & Agents."""
    server_url = request.host_url.rstrip('/')

    spec = {
        "openapi": "3.1.0",
        "info": {
            "title": "ArchiCheck Architectural Quality & Compliance AI API",
            "description": "REST API for external AI systems, LLM agents, and architectural tools to access, analyze, and benchmark residential plan validation results, statutory Israeli codes, NKBA guidelines, and Space Syntax spatial metrics.",
            "version": "1.0.0",
            "contact": {
                "name": "ArchiCheck Platform Engineering",
                "url": server_url
            }
        },
        "servers": [
            {
                "url": f"{server_url}/api/v1",
                "description": "Current Server (Local or Deployed)"
            }
        ],
        "paths": {
            "/projects": {
                "get": {
                    "operationId": "listProjects",
                    "summary": "List all architectural projects",
                    "description": "Returns catalog of projects with compliance scores and summary links.",
                    "parameters": [
                        {
                            "name": "q",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string"},
                            "description": "Search query for filtering by name or keyword"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "List of projects",
                            "content": {
                                "application/json": {
                                    "schema": {"type": "object"}
                                }
                            }
                        }
                    }
                }
            },
            "/projects/{project_id}": {
                "get": {
                    "operationId": "getProjectDetails",
                    "summary": "Get project metadata and sheets",
                    "parameters": [
                        {
                            "name": "project_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"},
                            "description": "Project ID (e.g. pines48, kkl10, hafetz44, yatkovski7, kitroni37)"
                        }
                    ],
                    "responses": {
                        "200": {"description": "Project details"},
                        "404": {"description": "Project not found"}
                    }
                }
            },
            "/projects/{project_id}/summary": {
                "get": {
                    "operationId": "getProjectSummaryForAI",
                    "summary": "Get AI-optimized executive summary",
                    "description": "Token-budgeted summary containing scores, statutory failures, top quality warnings, and recommendations formatted in Markdown.",
                    "parameters": [
                        {
                            "name": "project_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {"description": "Executive summary"}
                    }
                }
            },
            "/projects/{project_id}/analysis": {
                "get": {
                    "operationId": "getProjectAnalysisNotes",
                    "summary": "Query architectural audit findings",
                    "description": "Filter notes by status (FAIL, WARN, PASS), rule, room, or search keyword.",
                    "parameters": [
                        {
                            "name": "project_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "status",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string"},
                            "description": "Filter by status: 'FAIL', 'WARN', 'PASS', or 'FAIL,WARN'"
                        },
                        {
                            "name": "room",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string"},
                            "description": "Room keyword filter (e.g. ממ\"ד, מטבח, סלון)"
                        },
                        {
                            "name": "rule_id",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string"},
                            "description": "Rule ID filter"
                        },
                        {
                            "name": "q",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string"},
                            "description": "Free text search in findings"
                        },
                        {
                            "name": "limit",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "integer", "default": 50}
                        },
                        {
                            "name": "offset",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "integer", "default": 0}
                        }
                    ],
                    "responses": {
                        "200": {"description": "Filtered analysis notes"}
                    }
                }
            },
            "/projects/{project_id}/spatial-metrics": {
                "get": {
                    "operationId": "getProjectSpatialMetrics",
                    "summary": "Get dimensional and topology metrics",
                    "parameters": [
                        {
                            "name": "project_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {"description": "Spatial metrics"}
                    }
                }
            },
            "/compare": {
                "get": {
                    "operationId": "compareProjects",
                    "summary": "Compare architectural projects side-by-side",
                    "parameters": [
                        {
                            "name": "projects",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string"},
                            "description": "Comma-separated project IDs (e.g. pines48,kkl10,kitroni37)"
                        }
                    ],
                    "responses": {
                        "200": {"description": "Comparative table"}
                    }
                }
            },
            "/ai/context": {
                "post": {
                    "operationId": "getAIArchitecturalContext",
                    "summary": "Extract prompt context for an LLM query",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["query"],
                                    "properties": {
                                        "query": {"type": "string"},
                                        "project_id": {"type": "string"},
                                        "max_items": {"type": "integer", "default": 6}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Structured prompt context"}
                    }
                }
            },
            "/rules": {
                "get": {
                    "operationId": "listRules",
                    "summary": "Search OKF architectural rules",
                    "parameters": [
                        {
                            "name": "category",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "q",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {"description": "List of rules"}
                    }
                }
            },
            "/rules/{rule_id}": {
                "get": {
                    "operationId": "getRuleDetail",
                    "summary": "Get specific rule thresholds",
                    "parameters": [
                        {
                            "name": "rule_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {"description": "Rule specification"},
                        "404": {"description": "Rule not found"}
                    }
                }
            },
            "/analyze/plan": {
                "post": {
                    "operationId": "analyzeCustomPlan",
                    "summary": "Run live validation on custom apartment JSON",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"type": "object"}
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Live validation results"}
                    }
                }
            }
        }
    }
    return jsonify(spec)


# =====================================================================
# 8. Interactive API Explorer & Documentation UI
# =====================================================================

DOCS_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ArchiCheck AI API — תיעוד וממשק התחברות לסוכני AI</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.11.0/swagger-ui.css" />
    <style>
        :root {
            --bg-dark: #0f172a;
            --card-bg: #1e293b;
            --accent: #38bdf8;
            --accent-green: #10b981;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
        }
        body {
            margin: 0;
            padding: 0;
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            direction: rtl;
        }
        .header-bar {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border-bottom: 1px solid var(--border);
            padding: 24px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }
        .header-title h1 {
            margin: 0;
            font-size: 24px;
            display: flex;
            align-items: center;
            gap: 10px;
            color: #fff;
        }
        .badge {
            background: rgba(56, 189, 248, 0.2);
            color: var(--accent);
            border: 1px solid rgba(56, 189, 248, 0.4);
            font-size: 12px;
            padding: 4px 10px;
            border-radius: 9999px;
            font-weight: 600;
        }
        .badge-green {
            background: rgba(16, 185, 129, 0.2);
            color: var(--accent-green);
            border-color: rgba(16, 185, 129, 0.4);
        }
        .header-actions {
            display: flex;
            gap: 12px;
        }
        .btn {
            background: #2563eb;
            color: #fff;
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s;
            border: 1px solid transparent;
        }
        .btn:hover {
            background: #1d4ed8;
        }
        .btn-outline {
            background: transparent;
            border: 1px solid var(--border);
            color: var(--text-main);
        }
        .btn-outline:hover {
            background: #334155;
        }
        .hero-banner {
            padding: 24px 32px;
            background: #1e293b;
            margin: 20px 32px;
            border-radius: 12px;
            border: 1px solid var(--border);
        }
        .hero-banner h2 {
            margin-top: 0;
            color: var(--accent);
            font-size: 18px;
        }
        .grid-3 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 16px;
            margin-top: 16px;
        }
        .card {
            background: #0f172a;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 16px;
        }
        .card h3 {
            margin: 0 0 8px 0;
            font-size: 15px;
            color: #fff;
        }
        .card p {
            margin: 0;
            font-size: 13px;
            color: var(--text-muted);
            line-height: 1.5;
        }
        .code-pill {
            display: inline-block;
            background: #334155;
            color: #38bdf8;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 12px;
            direction: ltr;
        }
        #swagger-container {
            margin: 0 32px 40px 32px;
            background: #ffffff;
            border-radius: 12px;
            padding: 16px;
            direction: ltr;
        }
    </style>
</head>
<body>
    <div class="header-bar">
        <div class="header-title">
            <h1>ArchiCheck AI API <span class="badge">v1.0.0</span> <span class="badge badge-green">OpenAPI 3.1</span></h1>
            <p style="margin: 6px 0 0 0; color: var(--text-muted); font-size: 14px;">
                ממשק מובנה המאפשר ל-Custom GPTs, Claude Projects, LangChain, וסוכני בינה מלאכותית חיצוניים להתחבר ולנתח תוצאות בדיקה אדריכליות
            </p>
        </div>
        <div class="header-actions">
            <a href="/api/v1/client.py" download="archknow_client.py" class="btn" style="background: #10b981;">📥 הורד קובץ קישור (archknow_client.py)</a>
            <a href="/api/v1/openapi.json" target="_blank" class="btn">📄 הורד openapi.json</a>
            <a href="/api/v1/ai/tools" target="_blank" class="btn btn-outline">🛠️ כלי OpenAI & Claude</a>
            <a href="/" class="btn btn-outline">🖥️ חזרה לדשבורד</a>
        </div>
    </div>

    <div class="hero-banner">
        <h2>🚀 מדריך חיבור מהיר למערכות AI</h2>
        <div class="grid-3">
            <div class="card">
                <h3>🤖 חיבור ל-ChatGPT (Custom GPT)</h3>
                <p>
                    בהגדרות ה-GPT, בחר ב-<strong>Create Action</strong>, והדבק את כתובת ה-OpenAPI של המערכת:
                    <br><span class="code-pill">{{ server_url }}/api/v1/openapi.json</span>
                    <br>ה-GPT יקבל גישה אוטומטית לכל הפרויקטים, הליקויים וההמלצות.
                </p>
            </div>
            <div class="card">
                <h3>🧠 חיבור ל-Claude / LangChain / CrewAI</h3>
                <p>
                    משוך את סכמת הפונקציות המוכנה מ-<span class="code-pill">/api/v1/ai/tools</span> או שלח שאילתה ישירה ל-
                    <span class="code-pill">/api/v1/ai/context</span> לקבלת Prompt Context חסכוני ומדויק ללא שריפת טוקנים.
                </p>
            </div>
            <div class="card">
                <h3>📊 סיכום מנהלים חכם (Token Budgeted)</h3>
                <p>
                    הנקודה <span class="code-pill">/api/v1/projects/{id}/summary</span> מחזירה טקסט Markdown תמציתי ומדויק
                    עם הפרדה ברורה בין כשלים סטטוטוריים (FAIL), התראות איכות (WARN) וציונים.
                </p>
            </div>
        </div>
    </div>

    <div id="swagger-container">
        <div id="swagger-ui"></div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.11.0/swagger-ui-bundle.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/5.11.0/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {
            SwaggerUIBundle({
                url: "/api/v1/openapi.json",
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                layout: "BaseLayout"
            });
        };
    </script>
</body>
</html>
"""


@api_v1.route('/sync', methods=['POST', 'GET'])
@require_api_key
def trigger_drive_sync():
    """Triggers an incremental synchronization of all project data to the Google Shared Drive."""
    try:
        from sync_to_shared_drive import sync_all
        force = request.args.get('force', 'false').lower() == 'true'
        res = sync_all(force=force)
        return jsonify(res)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@api_v1.route('/docs', methods=['GET'])
def api_docs():
    """Serves the interactive Swagger UI and developer connection guide."""
    server_url = request.host_url.rstrip('/')
    return render_template_string(DOCS_HTML_TEMPLATE, server_url=server_url)
