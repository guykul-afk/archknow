from flask import Flask, send_from_directory, jsonify, request
import json
import os
from validation_engine import run_validation, load_okf_rules
from cad_parser import parse_multi_apartment_cad
from converter import convert_to_dxf

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
    
    if ext not in ['.dxf', '.dwg']:
        return jsonify({"error": f"Unsupported format: {ext}"}), 400
        
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)
    
    dxf_path = os.path.join(UPLOAD_FOLDER, "converted.dxf")
    
    # 1. Convert to DXF if necessary
    try:
        convert_to_dxf(input_path, dxf_path)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 412  # Precondition Failed (needs ODA installation)
    except Exception as e:
        return jsonify({"error": f"Conversion error: {str(e)}"}), 500
        
    # 2. Parse the DXF
    project_json_path = os.path.join(UPLOAD_FOLDER, "extracted_project.json")
    try:
        parse_multi_apartment_cad(dxf_path, project_json_path)
    except Exception as e:
        return jsonify({"error": f"Failed to parse CAD: {str(e)}"}), 500
        
    # 3. Read and run validation engine
    try:
        with open(project_json_path, "r", encoding="utf-8") as f:
            project_data = json.load(f)
    except Exception as e:
        return jsonify({"error": f"Failed to load parsed project: {str(e)}"}), 500

    rules = load_okf_rules("okf_rules")
    
    # Run validation on every apartment in every floor
    for floor in project_data.get("floors", []):
        for apt in floor.get("apartments", []):
            # Quantitative validation
            val_results = run_validation(apt, rules)
            apt["validation_results"] = val_results
            
            # Mock Qualitative validation per apartment
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
