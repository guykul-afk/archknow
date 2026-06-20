import json
import os
import yaml

# For this PoC, we map OKF rule IDs to concrete numerical thresholds.
# In a full system, these values would be directly embedded in the OKF YAML metadata.
RULE_THRESHOLDS = {
    "B1.6": {"min_area_sqm": 9.0},     # Bedroom Area
    "B1.10": {"min_area_sqm": 1.2},    # Toilet Area
    "B1.13": {"min_height_m": 2.7},    # Ceiling Height
    "B44": {"min_width_cm": 90},       # Main Entrance Accessibility (Metric Handbook style)
}

def load_apartment(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def load_okf_rules(rules_dir):
    rules = []
    for filename in os.listdir(rules_dir):
        if filename.endswith(".md") and filename != "index.md":
            filepath = os.path.join(rules_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                # Extract yaml block
                if content.startswith("---"):
                    end_idx = content.find("---", 3)
                    if end_idx != -1:
                        yaml_content = content[3:end_idx].strip()
                        try:
                            rule_meta = yaml.safe_load(yaml_content)
                            rules.append(rule_meta)
                        except:
                            pass
    return rules

def run_validation(apartment, rules):
    results = []
    print(f"Validating Apartment: {apartment['project_name']}")
    print("-" * 50)
    
    # 1. Global Parameters Check (e.g., Ceiling Height B1.13)
    ceiling_height = apartment.get("global_parameters", {}).get("ceiling_height_m", 0)
    rule_b1_13 = next((r for r in rules if r.get("rule_id") == "B1.13"), None)
    if rule_b1_13:
        threshold = RULE_THRESHOLDS.get("B1.13", {}).get("min_height_m", 2.7)
        if ceiling_height < threshold:
            results.append({
                "status": "FAIL",
                "element": "Global Ceiling",
                "rule_id": "B1.13",
                "message": f"Ceiling height {ceiling_height}m is below minimum {threshold}m."
            })
        else:
            results.append({"status": "PASS", "element": "Global Ceiling", "rule_id": "B1.13"})

    # 2. Rooms Check
    for room in apartment.get("rooms", []):
        room_type = room.get("type")
        room_area = room.get("area_sqm", 0)
        
        # Check Bedroom Area (B1.6)
        if room_type == "bedroom":
            rule_b1_6 = next((r for r in rules if r.get("rule_id") == "B1.6"), None)
            if rule_b1_6:
                threshold = RULE_THRESHOLDS.get("B1.6", {}).get("min_area_sqm", 9.0)
                if room_area < threshold:
                    results.append({
                        "status": "FAIL",
                        "element": f"Room {room['name']}",
                        "rule_id": "B1.6",
                        "message": f"Bedroom area {room_area}sqm is below minimum {threshold}sqm."
                    })
                else:
                    results.append({"status": "PASS", "element": f"Room {room['name']}", "rule_id": "B1.6"})
                    
        # Check Ventilation (Simulating an A17 / IAQ check)
        if room_type == "bathroom" and not room.get("has_window") and room.get("ventilation_type") == "none":
            results.append({
                "status": "FAIL",
                "element": f"Room {room['name']}",
                "rule_id": "A17",
                "message": "Bathroom has no window and no mechanical ventilation."
            })
            
    # 3. Accessibility Check
    entrance_width = apartment.get("accessibility", {}).get("main_entrance_width_cm", 0)
    if entrance_width < RULE_THRESHOLDS.get("B44", {}).get("min_width_cm", 90):
        results.append({
            "status": "FAIL",
            "element": "Main Entrance",
            "rule_id": "B44",
            "message": f"Entrance width {entrance_width}cm is below accessibility minimum 90cm."
        })
    else:
        results.append({"status": "PASS", "element": "Main Entrance", "rule_id": "B44"})

    return results

def print_report(results):
    print("\n=== VALIDATION REPORT ===")
    fails = 0
    for res in results:
        status_icon = "✅" if res["status"] == "PASS" else "❌"
        msg = f" - {res['message']}" if "message" in res else ""
        print(f"[{status_icon} {res['status']}] {res['element']} (Rule {res['rule_id']}){msg}")
        if res["status"] == "FAIL":
            fails += 1
            
    print("=" * 25)
    print(f"Total Rules Checked: {len(results)}")
    print(f"Passed: {len(results) - fails}")
    print(f"Failed: {fails}")
    print("=========================\n")

if __name__ == "__main__":
    apartment = load_apartment("extracted_apartment.json")
    rules = load_okf_rules("okf_rules")
    results = run_validation(apartment, rules)
    print_report(results)
