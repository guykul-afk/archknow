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
        with open(full_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        overlay_snippet = (
            f'\n  <script>window.__ARCHICHECK_PROJECT_ID__ = "{project_id}";</script>\n'
            f'  <script src="/audit_3d_overlay.js?v=5.2"></script>\n'
        )
        if "audit_3d_overlay.js" not in html_content:
            if "</body>" in html_content:
                html_content = html_content.replace("</body>", overlay_snippet + "</body>", 1)
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
    else:
        query = request.args.get('q', '')
    result = analyze_project_by_query(query)
    return jsonify(result)


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
