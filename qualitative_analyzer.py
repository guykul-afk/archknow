import json
import os
import yaml

def generate_llm_prompt(json_path, okf_rules_dir, output_prompt_path):
    print("Generating LLM Qualitative Prompt...")
    
    # 1. Load Apartment Data (with Topology)
    with open(json_path, "r", encoding="utf-8") as f:
        apartment = json.load(f)
        
    # 2. Extract Qualitative Rules from OKF
    # For this demonstration, we specifically pick rules that require human/AI judgement
    target_qualitative_rules = ["B1.2", "C1", "C4"] # Living space privacy, Acoustic privacy, Moving around
    
    qualitative_text = ""
    for filename in os.listdir(okf_rules_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(okf_rules_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                # Find rule ID from yaml
                yaml_block = content.split("---")[1] if "---" in content else ""
                if any(f"rule_id: {r}" in yaml_block for r in target_qualitative_rules):
                    qualitative_text += f"\n### Rule {filename}\n{content}\n"

    # 3. Build the Prompt
    prompt = f"""You are an expert Architectural AI Assistant evaluating an apartment design.
Please perform a Qualitative Design Review based on the following OKF (Open Knowledge Format) Rules.

=========================================
APARTMENT DATA (JSON FORMAT)
=========================================
{json.dumps(apartment, indent=2, ensure_ascii=False)}

=========================================
QUALITATIVE ARCHITECTURAL RULES TO CHECK
=========================================
{qualitative_text}

=========================================
YOUR TASK
=========================================
Analyze the apartment's 'topology' and 'rooms' against the Qualitative Rules above.
Specifically, answer:
1. Is the Living Space (R4) private from the guest entrance and other private rooms (Rule B1.2)? 
   Note: Look at the connections. Does the Main Entrance open directly to R4? Does the Bathroom (R3) open directly to R4?
2. How is the circulation and "Moving around inside the structure" (Rule C4)?
3. Provide a concluding Architectural Insight on how to improve the layout.

Output your response as a professional architectural review in Hebrew.
"""

    with open(output_prompt_path, "w", encoding="utf-8") as f:
        f.write(prompt)
        
    print(f"Prompt successfully written to {output_prompt_path}")

if __name__ == "__main__":
    generate_llm_prompt("extracted_apartment.json", "okf_rules", "qualitative_prompt.txt")
