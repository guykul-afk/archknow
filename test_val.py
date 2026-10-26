import json
from validation_engine import run_validation, load_okf_rules

with open("uploads/1d0d61f838bdcbdd67b5167d1acda5be_project.json", "r", encoding="utf-8") as f:
    data = json.load(f)

rules = load_okf_rules("okf_rules")
print(f"Loaded {len(rules)} rules.")

apt = data["floors"][0]["apartments"][0]
results = run_validation(apt, rules)

for r in results:
    print(r["rule_id"], r["status"], r["element"])
