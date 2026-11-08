# -*- coding: utf-8 -*-
from flask import Flask, send_from_directory, jsonify, request, Response, redirect
import json
import hashlib
import os
from validation_engine import run_validation, load_okf_rules
from project_analyzer_service import get_projects_catalog, analyze_project_by_query
from sync_3d_models import CENTRAL_MODELS_ROOT, PROJECTS_CONFIG
from api_v1 import api_v1

MODELS_BY_ID = {p["id"]: p for p in PROJECTS_CONFIG}

app = Flask(__name__, static_folder='webapp')
app.json.ensure_ascii = False  # Ensure clean UTF-8 Hebrew in JSON responses
app.register_blueprint(api_v1)

UPLOAD_FOLDER = 'uploads'
REPORTS_FOLDER = 'reports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)


@app.route('/api/docs')
def serve_docs_redirect():
    return redirect('/api/v1/docs')


@app.route('/archknow_client.py')
@app.route('/client.py')
def serve_root_client():
    from flask import send_file
    return send_file(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archknow_client.py'),
        mimetype='text/x-python',
        as_attachment=False,
        download_name='archknow_client.py'
    )


@app.route('/')
def serve_index():
    return send_from_directory('webapp', 'index.html')


@app.route('/reports/<path:filename>')
def serve_reports(filename):
    return send_from_directory(REPORTS_FOLDER, filename)


@app.route('/models/<project_id>')
@app.route('/models/<project_id>/')
def serve_central_3d_model_root(project_id):
    """
    Zero-Copy Central 3D Model Redirector:
    Redirects /models/<project_id> to /models/<project_id>/<primary_viewer> so all
    relative assets (*.glb, *.obj, data/*.json) inside the central folder resolve cleanly.
    """
    cfg = MODELS_BY_ID.get(project_id)
    if not cfg:
        return jsonify({"error": f"Unknown 3D model project_id: {project_id}"}), 404
    viewer_file = cfg.get("primary_viewer") or cfg.get("bim_viewer")
    qs = request.query_string.decode("utf-8")
    target = f"/models/{project_id}/{viewer_file}"
    if qs:
        target = f"{target}?{qs}"
    return redirect(target)


@app.route('/models/<project_id>/<path:filename>')
def serve_central_3d_model_file(project_id, filename):
    """
    Zero-Copy Central 3D Model Server & Runtime Overlay Injector:
    Serves 3D model HTML/GLB/OBJ/JSON directly from G:\\Shared drives\\שליטה ובקרה\\מודלים פרויקטים\\<folder_name>
    without duplicating files into the workspace, and injects the ArchiCheck 3D Audit & VE Overlay script at runtime.
    """
    cfg = MODELS_BY_ID.get(project_id)
    if not cfg:
        return jsonify({"error": f"Unknown 3D model project_id: {project_id}"}), 404

    project_dir = os.path.join(CENTRAL_MODELS_ROOT, cfg["folder_name"])
    full_path = os.path.join(project_dir, filename)
    if not os.path.isfile(full_path):
        return jsonify({"error": f"Model asset not found in central repository: {filename}"}), 404

    if filename.lower().endswith(".html"):
        # Automatically verify whether the base 3D model was modified; if so, trigger a full planning re-audit
        try:
            from model_3d_change_detector import check_and_reaudit_project
            check_and_reaudit_project(project_id, force=False, rebuild_artifacts=True)
        except Exception as e:
            print(f"[SERVER] 3D model change check warning for {project_id}: {e}")

        with open(full_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        if "<!-- ARCHICHECK_3D_OVERLAY_START -->" in html_content and "<!-- ARCHICHECK_3D_OVERLAY_END -->" in html_content:
            s_idx = html_content.index("<!-- ARCHICHECK_3D_OVERLAY_START -->")
            e_idx = html_content.index("<!-- ARCHICHECK_3D_OVERLAY_END -->") + len("<!-- ARCHICHECK_3D_OVERLAY_END -->")
            html_content = html_content[:s_idx] + html_content[e_idx:]

        overlay_snippet = (
            f'\n<!-- ARCHICHECK_3D_OVERLAY_START -->\n'
            f'<script>window.__ARCHICHECK_PROJECT_ID__ = "{project_id}";</script>\n'
            f'<script src="/audit_3d_overlay.js?v=7.5"></script>\n'
            f'<!-- ARCHICHECK_3D_OVERLAY_END -->\n'
        )
        last_body_idx = html_content.rfind("</body>")
        if last_body_idx != -1:
            html_content = html_content[:last_body_idx] + overlay_snippet + html_content[last_body_idx:]
        else:
            html_content += overlay_snippet
        return Response(html_content, mimetype="text/html; charset=utf-8")

    return send_from_directory(project_dir, filename)


@app.route('/api/projects', methods=['GET'])
def api_projects():
    return jsonify({"projects": get_projects_catalog()})


@app.route('/api/analyze_project', methods=['GET', 'POST'])
def api_analyze_project():
    if request.method == 'POST':
        body = request.get_json(silent=True) or {}
        query = body.get('query', '')
        force_reaudit = str(body.get('force_reaudit', '')).lower() in ('1', 'true', 'yes')
    else:
        query = request.args.get('q', '')
        force_reaudit = str(request.args.get('force_reaudit', '')).lower() in ('1', 'true', 'yes')
    result = analyze_project_by_query(query, force_reaudit=force_reaudit, rebuild_artifacts=True)
    return jsonify(result)


@app.route('/api/check_3d_models', methods=['GET', 'POST'])
def api_check_3d_models():
    """
    Checks whether the base 3D model of a specific project (or all projects)
    has been modified or updated. If modified (or if `force=true`), runs a full
    new planning audit and returns the updated payload & sync report.
    """
    from model_3d_change_detector import check_and_reaudit_project, check_all_projects_3d_models

    if request.method == 'POST':
        body = request.get_json(silent=True) or {}
        project_q = body.get('project') or body.get('query') or body.get('q') or ''
        force = str(body.get('force', '')).lower() in ('1', 'true', 'yes')
    else:
        project_q = request.args.get('project') or request.args.get('q') or ''
        force = str(request.args.get('force', '')).lower() in ('1', 'true', 'yes')

    if project_q:
        res = check_and_reaudit_project(project_q, force=force, rebuild_artifacts=True)
        return jsonify(res)
    summary = check_all_projects_3d_models(force=force, rebuild_artifacts=True)
    return jsonify(summary)


@app.route('/api/export/dxf', methods=['GET'])
def api_export_dxf():
    """Exports a layered AutoCAD R2010 DXF redline overlay for a project."""
    from export_engine import generate_project_dxf_redline

    project_id = (request.args.get('project') or request.args.get('id') or 'pines48').strip().lower()
    payload = analyze_project_by_query(project_id, rebuild_artifacts=False)
    pid = str(payload.get('project_id') or payload.get('id') or project_id)
    dxf_bytes = generate_project_dxf_redline(payload)
    return Response(
        dxf_bytes,
        mimetype='application/dxf',
        headers={
            'Content-Disposition': f'attachment; filename="{pid}_archicheck_redline.dxf"'
        },
    )


@app.route('/api/export/excel', methods=['GET'])
def api_export_excel():
    """Exports a multi-sheet Excel (.xlsx) BoQ, Value Engineering & Architect Action Package workbook."""
    from export_engine import generate_project_excel_boq

    project_id = (request.args.get('project') or request.args.get('id') or 'pines48').strip().lower()
    payload = analyze_project_by_query(project_id, rebuild_artifacts=False)
    pid = str(payload.get('project_id') or payload.get('id') or project_id)
    xlsx_bytes = generate_project_excel_boq(payload)
    return Response(
        xlsx_bytes,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': f'attachment; filename="{pid}_archicheck_boq_and_audit.xlsx"'
        },
    )


@app.route('/api/spatial_intelligence', methods=['POST'])
def api_spatial_intelligence():
    """Runs the algorithmic furnishability, sightline, zero-line closet, and livability engines."""
    from spatial_intelligence_engine import (
        compute_sightline_and_aesthetics_metrics,
        simulate_apartment_furnishability,
        analyze_resident_livability,
        audit_multi_floor_vertical_stack,
    )

    body = request.get_json(silent=True) or {}
    apt = body.get('apartment') or body
    sight = compute_sightline_and_aesthetics_metrics(apt)
    furn = simulate_apartment_furnishability(apt)
    liv = analyze_resident_livability(apt)
    floors = body.get('floors') or []
    vert = audit_multi_floor_vertical_stack(floors) if floors else None
    return jsonify({
        "status": "success",
        "sightlines_and_aesthetics": sight,
        "furnishability_simulation": furn,
        "resident_livability": liv,
        "vertical_stack_audit": vert,
    })


@app.route('/api/ask_plan', methods=['GET', 'POST'])
def api_ask_plan():
    """Answers user questions on the architectural plan and its analysis, returning data-grounded recommendations, ATKG reasoning chain, and executable system actions."""
    from plan_qa_engine import answer_plan_question

    if request.method == 'POST':
        body = request.get_json(silent=True) or {}
        project_q = (body.get('project') or body.get('project_id') or body.get('query') or 'hafetz44').strip()
        question = (body.get('question') or body.get('q') or '').strip()
        api_key = (body.get('api_key') or body.get('gemini_api_key') or '').strip() or None
        model_name = (body.get('model') or body.get('model_name') or '').strip() or None
        custom_payload = body.get('payload')
    else:
        project_q = (request.args.get('project') or request.args.get('project_id') or 'hafetz44').strip()
        question = (request.args.get('question') or request.args.get('q') or '').strip()
        api_key = (request.args.get('api_key') or '').strip() or None
        model_name = (request.args.get('model') or request.args.get('model_name') or '').strip() or None
        custom_payload = None

    if isinstance(custom_payload, dict) and custom_payload.get('notes'):
        payload = custom_payload
    else:
        payload = analyze_project_by_query(project_q, rebuild_artifacts=False)

    answer = answer_plan_question(payload, question, api_key=api_key, model_name=model_name)
    return jsonify({
        "status": "success",
        "project_id": payload.get("project_id"),
        "project_name": payload.get("project_name"),
        "answer": answer,
    })


@app.route('/api/atkg/<project_id>', methods=['GET'])
def api_get_project_atkg(project_id):
    """Returns the 4-Layer ATKG (Architectural Topological Knowledge Graph) for a project."""
    payload = analyze_project_by_query(project_id, rebuild_artifacts=False)
    return jsonify({
        "status": "success",
        "project_id": payload.get("project_id"),
        "project_name": payload.get("project_name"),
        "atkg_spatial_graph": payload.get("atkg_spatial_graph"),
    })


@app.route('/api/ai_twin/<project_id>', methods=['GET'])
def api_get_project_ai_twin(project_id):
    """Returns the Compact Architectural Twin Markdown (`ai_twin_compact_md`, ~10KB) for LLM reasoning."""
    payload = analyze_project_by_query(project_id, rebuild_artifacts=False)
    atkg = payload.get("atkg_spatial_graph") or {}
    md_text = atkg.get("ai_twin_compact_md", "")
    return Response(md_text, mimetype="text/markdown; charset=utf-8")


@app.route('/api/portfolio_index', methods=['GET'])
def api_get_portfolio_index():
    """Returns the cross-project ATKG portfolio comparison index across all projects."""
    idx_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'webapp', 'api', 'portfolio_atkg_index.json')
    if os.path.isfile(idx_path):
        with open(idx_path, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    from atkg_spatial_graph import build_portfolio_atkg_index
    all_payloads = [analyze_project_by_query(p['id'], rebuild_artifacts=False) for p in get_projects_catalog()]
    return jsonify(build_portfolio_atkg_index(all_payloads))


@app.route('/api/usage_costs', methods=['GET'])
def api_get_usage_costs():
    """Returns the daily, weekly, and cumulative Gemini API cost & token usage summary."""
    from llm_reasoning_agent import get_api_usage_summary
    return jsonify({
        "status": "success",
        "usage_summary": get_api_usage_summary(),
    })


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('webapp', path)


@app.route('/api/upload', methods=['POST'])
def api_upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()

    if ext not in ['.dxf', '.dwg', '.dwf', '.dwfx', '.pdf']:
        return jsonify({"error": f"Unsupported format: {ext}"}), 400

    file_content = file.read()
    file_hash = hashlib.md5(file_content).hexdigest()
    file.seek(0)

    input_path = os.path.join(UPLOAD_FOLDER, f"{file_hash}_{filename}")
    dxf_path = os.path.join(UPLOAD_FOLDER, f"{file_hash}.dxf")
    project_json_path = os.path.join(UPLOAD_FOLDER, f"{file_hash}_project.json")

    file.save(input_path)

    if ext == '.pdf':
        try:
            from pdf_parser import parse_pdf_plan
            parse_pdf_plan(input_path, project_json_path, file_hash, preview_dir=os.path.join("webapp", "uploads"))
        except Exception as e:
            return jsonify({"error": f"Error parsing PDF plan: {str(e)}"}), 400
    else:
        png_path = os.path.join("webapp/uploads", f"{file_hash}_page.png")
        try:
            from converter import convert_to_dxf
            convert_to_dxf(input_path, dxf_path, png_path)
        except FileNotFoundError as e:
            return jsonify({"error": str(e)}), 412
        except Exception as e:
            return jsonify({"error": f"Conversion error: {str(e)}"}), 500

        try:
            from cad_parser import parse_multi_apartment_cad
            parse_multi_apartment_cad(dxf_path, project_json_path)
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # After saving and parsing into uploads/, analyze it through the unified service
    result = analyze_project_by_query(filename)

    # Automatically synchronize updated data to the Google Shared Drive
    try:
        from sync_to_shared_drive import sync_all
        sync_all()
    except Exception:
        pass

    return jsonify(result)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting ArchiCheck Web Server on http://0.0.0.0:{port} ...")
    app.run(host='0.0.0.0', port=port)
