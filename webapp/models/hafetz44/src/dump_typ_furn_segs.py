import json

with open(r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\hafetz44_extracted_plans.json", encoding="utf-8") as f:
    plans = json.load(f)

def print_segs(plan_name, x0, y0, x1, y1, title):
    print(f"--- {plan_name.upper()}: {title} [{x0}..{x1}, {y0}..{y1}] ---")
    for s in plans[plan_name]["cad_lines"]:
        sx0, sy0, sx1, sy1 = s
        if min(sx0,sx1) >= x0-0.1 and max(sx0,sx1) <= x1+0.1 and min(sy0,sy1) >= y0-0.1 and max(sy0,sy1) <= y1+0.1:
            print(f"  ({sx0:7.3f}, {sy0:7.3f}) -> ({sx1:7.3f}, {sy1:7.3f})")

print_segs("typical", -13.15,  1.20, -3.30,  4.00, "West Living + Dining + Kitchen")
print_segs("typical", -13.15, -5.00, -1.00, -0.30, "West Bedrooms + Baths")
print_segs("typical",  -1.05, -4.40,  5.50, -0.25, "West & East Mamads")
print_segs("typical",   5.55,  1.10, 14.15,  4.00, "East Kitchen + Dining + Living")
print_segs("typical",   5.55, -5.00, 14.15, -0.30, "East Bedrooms + Baths")
