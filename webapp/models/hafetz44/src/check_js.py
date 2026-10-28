import re, subprocess

html = open(r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\hafetz44_3d_bim_viewer.html", encoding="utf-8").read()
scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', html)
js = max(scripts, key=len)
js_path = r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\test_syntax.js"
open(js_path, "w", encoding="utf-8").write(js)
r = subprocess.run(["node", "--check", js_path], capture_output=True, text=True)
print("EXIT:", r.returncode, "LEN:", len(js), r.stdout, r.stderr)
