# -*- coding: utf-8 -*-
from flask import Flask, send_from_directory, jsonify, request
import json
import hashlib
import os
from validation_engine import run_validation, load_okf_rules
from project_analyzer_service import get_projects_catalog, analyze_project_by_query
from api_v1 import api_v1

app = Flask(__name__, static_folder='webapp')
app.json.ensure_ascii = False  # Ensure clean UTF-8 Hebrew in JSON responses
app.register_blueprint(api_v1)

UPLOAD_FOLDER = 'uploads'
REPORTS_FOLDER = 'reports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)


@app.route('/api/docs')
def serve_docs_redirect():
    from flask import redirect
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
