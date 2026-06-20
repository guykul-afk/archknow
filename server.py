from flask import Flask, send_from_directory, jsonify
import json
import os
from validation_engine import run_validation, load_okf_rules

app = Flask(__name__, static_folder='webapp')

@app.route('/')
def serve_index():
    return send_from_directory('webapp', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('webapp', path)

@app.route('/api/analyze')
def api_analyze():
    try:
        with open("extracted_project.json", "r", encoding="utf-8") as f:
            project_data = json.load(f)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

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
