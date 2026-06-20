import fitz
import re
import os
import yaml

def clean_text(text):
    # Remove excessive whitespaces and clean up text
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def process_neufert():
    doc = fitz.open("03. Architect_s Data.pdf")
    output_dir = "okf_rules"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Processing Neufert (Pages 50 to 80)...")
    
    # We will process pages 50 to 80 (0-indexed: 49 to 79)
    rules_count = 0
    for page_idx in range(49, 80):
        text = doc[page_idx].get_text()
        lines = text.split('\n')
        
        page_num = page_idx + 1
        page_title = "Neufert Page Title"
        for line in lines[:5]:
            if line.strip() and not line.strip().isdigit() and len(line.strip()) > 3:
                page_title = line.strip()
                break
        
        # Split text into paragraphs or bullet-like structures
        # Look for headers in all-caps or paragraphs with bullet points
        paragraphs = re.split(r'\n(?=[A-Z0-9\s]{4,}\n|•|\d\s[A-Z])', text)
        
        for idx, para in enumerate(paragraphs):
            para_clean = para.strip()
            if len(para_clean) < 100: # skip short headers or page noise
                continue
                
            # Generate a rule ID and filename
            rule_id = f"N.{page_num}.{idx+1}"
            short_desc = clean_text(para_clean)[:50]
            safe_desc = re.sub(r'[^a-z0-9]+', '_', short_desc.lower()).strip('_')
            filename = f"{rule_id.lower().replace('.', '_')}_{safe_desc}.md"
            filepath = os.path.join(output_dir, filename)
            
            frontmatter = {
                "type": "architectural_standard",
                "rule_id": rule_id,
                "source": f"Neufert Architects' Data, Page {page_num}",
                "topic": page_title,
                "description_summary": clean_text(para_clean)[:80] + "..."
            }
            
            yaml_str = yaml.dump(frontmatter, default_flow_style=False)
            
            md_content = f"---\n{yaml_str}---\n# Standard from {frontmatter['source']}\n\n"
            md_content += f"## Topic: {page_title}\n\n"
            md_content += f"## Standard Details\n{para_clean}\n"
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(md_content)
            rules_count += 1
            
    print(f"Generated {rules_count} OKF standards from Neufert.")

def process_metric_handbook():
    doc = fitz.open("preview-9781000449549_A42256746.pdf")
    output_dir = "okf_rules"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Processing Metric Handbook (Pages 54 to 90)...")
    
    # Process Chapter 4 (pages 54 to 90, 0-indexed: 53 to 89)
    rules_count = 0
    for page_idx in range(53, min(90, len(doc))):
        text = doc[page_idx].get_text()
        lines = text.split('\n')
        
        page_num = page_idx + 1
        page_title = "Metric Handbook Accessibility"
        for line in lines[:5]:
            if line.strip() and not line.strip().isdigit() and len(line.strip()) > 3:
                page_title = line.strip()
                break
                
        paragraphs = re.split(r'\n(?=[0-9]\.[0-9]|\n|•)', text)
        
        for idx, para in enumerate(paragraphs):
            para_clean = para.strip()
            if len(para_clean) < 120 or "Contents" in para_clean:
                continue
                
            rule_id = f"MH.{page_num}.{idx+1}"
            short_desc = clean_text(para_clean)[:50]
            safe_desc = re.sub(r'[^a-z0-9]+', '_', short_desc.lower()).strip('_')
            filename = f"{rule_id.lower().replace('.', '_')}_{safe_desc}.md"
            filepath = os.path.join(output_dir, filename)
            
            frontmatter = {
                "type": "accessibility_standard",
                "rule_id": rule_id,
                "source": f"Metric Handbook, Page {page_num}",
                "topic": page_title,
                "description_summary": clean_text(para_clean)[:80] + "..."
            }
            
            yaml_str = yaml.dump(frontmatter, default_flow_style=False)
            
            md_content = f"---\n{yaml_str}---\n# Accessibility Standard: {page_title}\n\n"
            md_content += f"## Details from {frontmatter['source']}\n\n"
            md_content += f"{para_clean}\n"
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(md_content)
            rules_count += 1
            
    print(f"Generated {rules_count} OKF standards from Metric Handbook.")

def update_index():
    output_dir = "okf_rules"
    files = [f for f in os.listdir(output_dir) if f.endswith(".md") and f != "index.md"]
    
    # Sort files by rule prefix
    files.sort()
    
    index_content = "---\ntype: index\ntitle: Architectural & Accessibility Knowledge Base Index\n---\n# Complete Architectural & Accessibility Knowledge Base\n\n"
    
    categories = {
        "A": "Technical Performance Regulations",
        "B": "Functional Design Regulations",
        "C": "Behavioral Design Regulations",
        "N": "Neufert Architectural Design Standards",
        "MH": "Metric Handbook Accessibility Standards"
    }
    
    grouped = {k: [] for k in categories.keys()}
    
    for f in files:
        filepath = os.path.join(output_dir, f)
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
            # extract yaml frontmatter
            fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
            if fm_match:
                try:
                    fm = yaml.safe_load(fm_match.group(1))
                    rule_id = fm.get("rule_id", "")
                    prefix = rule_id.split(".")[0]
                    if prefix.startswith("A"):
                        grouped["A"].append((rule_id, fm.get("description_summary", ""), f))
                    elif prefix.startswith("B"):
                        grouped["B"].append((rule_id, fm.get("description_summary", ""), f))
                    elif prefix.startswith("C"):
                        grouped["C"].append((rule_id, fm.get("description_summary", ""), f))
                    elif prefix.startswith("N"):
                        grouped["N"].append((rule_id, fm.get("description_summary", ""), f))
                    elif prefix.startswith("MH"):
                        grouped["MH"].append((rule_id, fm.get("description_summary", ""), f))
                except Exception as e:
                    print(f"Error parsing yaml in {f}: {e}")
                    
    for prefix, cat_name in categories.items():
        index_content += f"\n## {cat_name}\n"
        for rule_id, summary, filename in grouped[prefix]:
            index_content += f"- **[{rule_id}]({filename})**: {summary}\n"
            
    with open(os.path.join(output_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(index_content)
    print("Updated index.md with all categories.")

if __name__ == "__main__":
    process_neufert()
    process_metric_handbook()
    update_index()
