# -*- coding: utf-8 -*-
import os
import json
import shutil
import sys
sys.stdout.reconfigure(encoding='utf-8')

from project_analyzer_service import get_projects_catalog, analyze_project_by_query
from sync_3d_models import CENTRAL_MODELS_ROOT, PROJECTS_CONFIG

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
with open('webapp/api/projects.json', 'w', encoding='utf-8', newline='\n') as f:
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
    with open(out_p, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'Wrote {out_p} ({len(data["notes"])} notes, {len(data["sheets"])} sheets)')

# 3. Sync existing 3D model viewers from Central Repository (G:\Shared drives\שליטה ובקרה\מודלים פרויקטים)
#    into webapp/models/<pid>/ for Firebase Hosting (Zero-Rebuild, runtime overlay injected)
for cfg in PROJECTS_CONFIG:
    pid = cfg['id']
    if pid not in project_queries:
        continue
    src_dir = os.path.join(CENTRAL_MODELS_ROOT, cfg['folder_name'])
    if not os.path.isdir(src_dir):
        print(f'WARNING: Central model folder not found for {pid}: {src_dir}')
        continue

    dst_dir = os.path.join('webapp', 'models', pid)
    os.makedirs(dst_dir, exist_ok=True)

    # Copy any required companion JS files (e.g., kkl10_threejs_bim_v6_1.js)
    for fn in os.listdir(src_dir):
        if fn.endswith('.js') and not fn.startswith('hafetz44_audit_'):
            shutil.copy2(os.path.join(src_dir, fn), os.path.join(dst_dir, fn))

    # Sync HTML viewers and ensure runtime overlay script is injected
    html_files = set(filter(None, [cfg.get('primary_viewer'), cfg.get('bim_viewer'), cfg.get('spatial_map')]))
    overlay_block = (
        f'\n<!-- ARCHICHECK_3D_OVERLAY_START -->\n'
        f'<script>window.__ARCHICHECK_PROJECT_ID__ = "{pid}";</script>\n'
        f'<script src="/audit_3d_overlay.js?v=5.3"></script>\n'
        f'<!-- ARCHICHECK_3D_OVERLAY_END -->\n'
    )
    for html_fn in html_files:
        src_html = os.path.join(src_dir, html_fn)
        if not os.path.isfile(src_html):
            continue
        with open(src_html, 'r', encoding='utf-8', errors='replace') as fh:
            html_content = fh.read()
        if '<!-- ARCHICHECK_3D_OVERLAY_START -->' in html_content:
            s_idx = html_content.index('<!-- ARCHICHECK_3D_OVERLAY_START -->')
            e_idx = html_content.index('<!-- ARCHICHECK_3D_OVERLAY_END -->') + len('<!-- ARCHICHECK_3D_OVERLAY_END -->')
            html_content = html_content[:s_idx] + overlay_block.strip() + html_content[e_idx:]
        elif '</body>' in html_content:
            html_content = html_content.replace('</body>', overlay_block + '</body>', 1)
        else:
            html_content += overlay_block

        dst_html = os.path.join(dst_dir, html_fn)
        with open(dst_html, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(html_content)
        print(f'Synced 3D viewer to static hosting: {dst_html}')

print('Static export complete!')
