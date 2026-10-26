# -*- coding: utf-8 -*-
import os
import json
import shutil
import sys
sys.stdout.reconfigure(encoding='utf-8')

from project_analyzer_service import get_projects_catalog, analyze_project_by_query

# 1. Copy reports to webapp/reports
os.makedirs('webapp/reports', exist_ok=True)
for fn in os.listdir('reports'):
    src = os.path.join('reports', fn)
    dst = os.path.join('webapp/reports', fn)
    if os.path.isfile(src):
        shutil.copy2(src, dst)
        print('Copied report:', fn)

# 2. Export API data for static hosting
os.makedirs('webapp/api', exist_ok=True)
cat = get_projects_catalog()
with open('webapp/api/projects.json', 'w', encoding='utf-8') as f:
    json.dump({'projects': cat}, f, ensure_ascii=False, indent=2)
print('Wrote webapp/api/projects.json')

project_queries = {
    'pines48': 'פינס 48',
    'kkl10': 'קק״ל 10',
    'hafetz44': 'חפץ חיים 44',
    'yatkovski7': 'יטקובסקי 7',
    'kitroni37': 'קטרוני 37–39',
    'feierberg3': 'פאירברג 3',
}
for pid, q in project_queries.items():
    data = analyze_project_by_query(q)
    out_p = f'webapp/api/{pid}.json'
    with open(out_p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'Wrote {out_p} ({len(data["notes"])} notes, {len(data["sheets"])} sheets)')

print('Static export complete!')
