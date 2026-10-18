from flask import Flask, send_from_directory, jsonify, request
import json
import hashlib
import os
from validation_engine import run_validation, load_okf_rules
from cad_parser import parse_multi_apartment_cad
from converter import convert_to_dxf
from pdf_parser import parse_pdf_plan

app = Flask(__name__, static_folder='webapp')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def serve_index():
    return send_from_directory('webapp', 'index.html')

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
            # smart analysis: plan_analyzer (reading + 2D model + QA), legacy fallback inside
            parse_pdf_plan(input_path, project_json_path, file_hash, preview_dir=os.path.join("webapp", "uploads"))
        except Exception as e:
            return jsonify({"error": f"Error parsing PDF plan: {str(e)}"}), 400
    else:
        # 1. Convert to DXF if necessary and generate PNG preview
        png_path = os.path.join("webapp/uploads", f"{file_hash}_page.png")
        try:
            convert_to_dxf(input_path, dxf_path, png_path)
        except FileNotFoundError as e:
            return jsonify({"error": str(e)}), 412  # Precondition Failed
        except Exception as e:
            return jsonify({"error": f"Conversion error: {str(e)}"}), 500
            
        # 2. Parse the DXF
        try:
            parse_multi_apartment_cad(dxf_path, project_json_path)
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    # 3. Read and run validation engine
    try:
        with open(project_json_path, "r", encoding="utf-8") as f:
            project_data = json.load(f)
    except Exception as e:
        return jsonify({"error": f"Failed to load parsed project: {str(e)}"}), 500

    bg_filename = f"{file_hash}_page.png"
    if os.path.exists(os.path.join("webapp/uploads", bg_filename)):
        project_data["bg_image_url"] = f"/uploads/{bg_filename}"

    rules = load_okf_rules("okf_rules")
    
    # Run validation on every apartment in every floor
    for floor in project_data.get("floors", []):
        for apt in floor.get("apartments", []):
            # Quantitative validation
            val_results = run_validation(apt, rules)
            apt["validation_results"] = val_results
            
            # Mock Qualitative validation per apartment (placeholder — not for analyzed PDFs,
            # whose plan-derived findings come from the engine's topology checks)
            if "plan_extraction" in apt:
                apt["qualitative_insights"] = []
                continue
            apt["qualitative_insights"] = [
                {
                    "title": "⚠️ פגיעה בפרטיות (כלל B1.2)",
                    "description": "הגרף המרחבי מראה כי דלת הכניסה נפתחת ישירות לסלון. מומלץ להוסיף מבואה."
                },
                {
                    "title": "🔄 זרימה ותנועה",
                    "description": "התנועה תקינה ברובה, אך תלויה בסלון כמעבר מרכזי."
                }
            ]
            
    return jsonify(project_data)

if __name__ == '__main__':
    print("Starting ArchiCheck Web Server...")
    print("Open http://127.0.0.1:5000 in your browser.")
    app.run(host='127.0.0.1', port=5000)
