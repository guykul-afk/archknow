import fitz
import re
import os
import yaml

def extract_table_rows(pdf_path):
    doc = fitz.open(pdf_path)
    table_text = ""
    # Table 1 is on page 7 and 8 (0-indexed pages 6 and 7)
    table_text += doc[6].get_text()
    table_text += doc[7].get_text()
    
    lines = table_text.split('\n')
    
    categories = {
        "A": "Technical performance elements",
        "B": "Functional performance elements",
        "C": "Components of behavioral performance"
    }
    
    subcategories = {
        "A1": "Thermal comfort",
        "A2": "Acoustical comfort",
        "A3": "Visual comfort",
        "A4": "Indoor air quality (IAQ)",
        "A5": "Safety and security",
        "B1": "Design adequacy",
        "B2": "Finishing",
        "B3": "Equipment, fixtures, and furnishings",
        "B4": "Building location",
        "B5": "Building support services",
        "C1": "Features of apartment building (elements)",
        "C2": "Administrative and practical assistance"
    }

    rules = []
    current_category = ""
    current_subcategory = ""
    
    # We want to match patterns like:
    # A1 Temperature in summer and winter
    # A20 Fire sprinkler distribution...
    # B10 Toilet area
    # C1 The degree of acoustic...
    # C12 Facilitating sustainable...
    
    # Let's clean lines and loop through them
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Detect main category
        if "A. Technical performance elements" in line:
            current_category = "Technical performance elements"
        elif "B. Functional performance elements" in line:
            current_category = "Functional performance elements"
        elif "C. Components of behavioral performance" in line or "C. Behavioral performance" in line:
            current_category = "Components of behavioral performance"
            
        # Detect subcategories
        for sub_id, sub_name in subcategories.items():
            if line.startswith(sub_id + ". ") or line == sub_id + "." or line == sub_name:
                current_subcategory = sub_name
        
        # Check if line matches an indicator ID (like A1, A2, B21, C12 etc.)
        match = re.match(r'^([A-C])([0-9]+)$', line)
        if match:
            prefix = match.group(1)
            num = match.group(2)
            rule_id = f"{prefix}{num}"
            
            # The next line(s) usually contain the description
            desc_parts = []
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                # Stop if we hit another ID or main section
                if re.match(r'^[A-C][0-9]+$', next_line) or "Table 1" in next_line or "Cont." in next_line or next_line.startswith("References") or next_line.startswith("Performance Indicators"):
                    break
                if next_line:
                    # Remove reference brackets at the end of description like [4,6,8...]
                    cleaned = re.sub(r'\s*\[[0-9,\s–-]+\]\s*$', '', next_line)
                    if cleaned:
                        desc_parts.append(cleaned)
                j += 1
            
            description = " ".join(desc_parts).strip()
            # Clean up trailing reference brackets if any remain
            description = re.sub(r'\s*\[[0-9,\s–-]+\]\s*$', '', description)
            
            if description:
                rules.append({
                    "id": rule_id,
                    "category": current_category or "Unknown",
                    "subcategory": current_subcategory or "Unknown",
                    "description": description
                })
        i += 1
        
    return rules

def build_okf(rules):
    output_dir = "okf_rules"
    os.makedirs(output_dir, exist_ok=True)
    
    index_content = "---\ntype: index\ntitle: Complete Architectural Evaluation Rules Index\n---\n# Complete Architectural Evaluation Rules\n\n"
    
    # Group by category
    categories = {}
    for rule in rules:
        cat = rule["category"]
        sub = rule["subcategory"]
        if cat not in categories:
            categories[cat] = {}
        if sub not in categories[cat]:
            categories[cat][sub] = []
        categories[cat][sub].append(rule)
        
    for cat, subs in categories.items():
        index_content += f"\n## {cat}\n"
        for sub, sub_rules in subs.items():
            index_content += f"\n### {sub}\n"
            for rule in sub_rules:
                # Sanitize filename
                safe_desc = re.sub(r'[^a-z0-9]+', '_', rule["description"].lower())[:40].strip('_')
                filename = f"{rule['id'].lower()}_{safe_desc}.md"
                filepath = os.path.join(output_dir, filename)
                
                frontmatter = {
                    "type": "architectural_rule",
                    "rule_id": rule["id"],
                    "category": rule["category"],
                    "subcategory": rule["subcategory"],
                    "description_summary": rule["description"][:60] + "..." if len(rule["description"]) > 60 else rule["description"]
                }
                
                yaml_str = yaml.dump(frontmatter, default_flow_style=False)
                
                md_content = f"---\n{yaml_str}---\n# {rule['id']}: {rule['description']}\n\n"
                md_content += f"## Details\n- **Category**: {rule['category']}\n- **Subcategory**: {rule['subcategory']}\n"
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(md_content)
                
                index_content += f"- [{rule['id']}: {rule['description']}]({filename})\n"
                
    with open(os.path.join(output_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(index_content)
    
    print(f"Successfully generated {len(rules)} OKF files in '{output_dir}/'")

if __name__ == "__main__":
    rules = extract_table_rows("architecture-05-00008-v2.pdf")
    build_okf(rules)
