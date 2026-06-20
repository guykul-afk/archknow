import os
import yaml

# Define a set of rules extracted from the Table 1 (Functional performance elements - Design adequacy)
design_adequacy_rules = [
    {
        "id": "B1.1",
        "title": "Adequacy of the guest reception area",
        "category": "Design Adequacy",
        "indicator": "Guest Reception Area",
        "description": "Evaluate the adequacy and size of the guest reception area to ensure it meets spatial needs for visitors.",
        "target_room": "reception/living room",
        "check_type": "area_and_layout"
    },
    {
        "id": "B1.2",
        "title": "Privacy of the living space",
        "category": "Design Adequacy",
        "indicator": "Living Space Privacy",
        "description": "Ensure the family living space is visually and acoustically private from the guest entrance and reception areas.",
        "target_room": "family living space",
        "check_type": "spatial_layout_privacy"
    },
    {
        "id": "B1.3",
        "title": "Area of the living space",
        "category": "Design Adequacy",
        "indicator": "Living Space Area",
        "description": "The total area of the family living space must be adequate for the household size.",
        "target_room": "family living space",
        "check_type": "min_area"
    },
    {
        "id": "B1.6",
        "title": "Area of typical bedrooms",
        "category": "Design Adequacy",
        "indicator": "Bedroom Area",
        "description": "Typical bedrooms must have adequate square footage to accommodate standard furniture (bed, wardrobe, desk) with clear circulation.",
        "target_room": "bedroom",
        "check_type": "min_area"
    },
    {
        "id": "B1.9",
        "title": "Total number of restrooms, bathrooms, and toilets",
        "category": "Design Adequacy",
        "indicator": "Bathroom Quantity",
        "description": "Ensure the total number of restrooms, bathrooms, and toilets matches the household size and bedroom count.",
        "target_room": "bathroom/toilet",
        "check_type": "quantity_ratio"
    },
    {
        "id": "B1.10",
        "title": "Toilet area",
        "category": "Design Adequacy",
        "indicator": "Toilet Area",
        "description": "Ensure toilet compartments have sufficient area for comfortable usage and fixture clearance.",
        "target_room": "toilet",
        "check_type": "min_area"
    },
    {
        "id": "B1.11",
        "title": "Kitchen area",
        "category": "Design Adequacy",
        "indicator": "Kitchen Area",
        "description": "The kitchen must have sufficient area to accommodate basic appliances (fridge, stove, sink) and counter space.",
        "target_room": "kitchen",
        "check_type": "min_area"
    },
    {
        "id": "B1.13",
        "title": "Ceilings height",
        "category": "Design Adequacy",
        "indicator": "Ceiling Height",
        "description": "Ensure the clear height from finished floor to ceiling complies with residential standards (typically minimum 2.7 meters).",
        "target_room": "all",
        "check_type": "height"
    }
]

def generate_okf_files():
    output_dir = "okf_rules"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create index.md for OKF structure navigation
    index_content = "---\ntype: index\ntitle: Architectural Evaluation Rules Index\n---\n# Architectural Evaluation Rules\n\n"
    index_content += "This index lists all the rules extracted from architectural POE and regulations.\n\n## Design Adequacy Rules\n"
    
    for rule in design_adequacy_rules:
        filename = f"{rule['id'].lower().replace('.', '_')}_{rule['indicator'].lower().replace(' ', '_')}.md"
        filepath = os.path.join(output_dir, filename)
        
        # Build YAML Frontmatter
        frontmatter = {
            "type": "architectural_rule",
            "rule_id": rule["id"],
            "category": rule["category"],
            "indicator": rule["indicator"],
            "target_room": rule["target_room"],
            "check_type": rule["check_type"]
        }
        
        yaml_str = yaml.dump(frontmatter, default_flow_style=False)
        
        # Build Markdown content
        md_content = f"---\n{yaml_str}---\n# {rule['title']}\n\n## Description\n{rule['description']}\n\n"
        md_content += f"## Evaluation Parameters\n- **Target Room**: {rule['target_room']}\n- **Check Type**: {rule['check_type']}\n"
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        index_content += f"- [{rule['title']}]({filename})\n"
        print(f"Created OKF file: {filepath}")
        
    # Write index.md
    with open(os.path.join(output_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(index_content)
    print("Created OKF Index: okf_rules/index.md")

if __name__ == "__main__":
    generate_okf_files()
