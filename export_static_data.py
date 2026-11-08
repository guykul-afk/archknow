# -*- coding: utf-8 -*-
import os
import json
import shutil
import sys
sys.stdout.reconfigure(encoding='utf-8')

from project_analyzer_service import get_projects_catalog, analyze_project_by_query
from sync_3d_models import CENTRAL_MODELS_ROOT, PROJECTS_CONFIG
from spatial_position_lock import build_and_verify_master_registry
from atkg_spatial_graph import build_portfolio_atkg_index


def _safe_write_text(path: str, text: str) -> None:
    tmp_path = path + '.tmp'
    with open(tmp_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    try:
        os.replace(tmp_path, path)
    except OSError:
        if os.path.exists(path):
            os.remove(path)
        os.replace(tmp_path, path)


def _safe_write_json(path: str, obj) -> None:
    _safe_write_text(path, json.dumps(obj, ensure_ascii=False, indent=2))


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
_safe_write_json('webapp/api/projects.json', {'projects': cat})
print('Wrote webapp/api/projects.json')

project_queries = {
    'pines48': 'פינס 48',
    'kkl10': 'קק״ל 10',
    'hafetz44': 'חפץ חיים 44',
    'yatkovski7': 'יטקובסקי 7',
    'kitroni37': 'קטרוני 37–39',
    'feierberg3': 'פאירברג 3',
    'sharett26': 'משה שרת 26–28',
    'em_hamoshavot': 'אם המושבות',
}
all_exported_payloads = []
for pid, q in project_queries.items():
    data = analyze_project_by_query(q, rebuild_artifacts=False)
    all_exported_payloads.append(data)
    out_p = f'webapp/api/{pid}.json'
    _safe_write_json(out_p, data)
    print(f'Wrote {out_p} ({len(data["notes"])} notes, {len(data["sheets"])} sheets)')
    # Export Tri-Modal View 1: Compact Architectural Twin Markdown (<pid>_ai_twin.md)
    atkg_obj = data.get('atkg_spatial_graph') or {}
    ai_twin_md = atkg_obj.get('ai_twin_compact_md', '')
    if ai_twin_md:
        twin_path = f'webapp/api/{pid}_ai_twin.md'
        _safe_write_text(twin_path, ai_twin_md)
        print(f'Wrote {twin_path} ({len(ai_twin_md)} chars)')
    try:
        from export_engine import generate_project_dxf_redline, generate_project_excel_boq
        with open(f'webapp/api/{pid}_redline.dxf', 'wb') as df:
            df.write(generate_project_dxf_redline(data))
        with open(f'webapp/api/{pid}_boq.xlsx', 'wb') as xf:
            xf.write(generate_project_excel_boq(data))
        print(f'Wrote webapp/api/{pid}_redline.dxf and webapp/api/{pid}_boq.xlsx')
    except Exception as ex:
        print(f'Warning generating static DXF/Excel for {pid}: {ex}')

# Export Tri-Modal View 2: Cross-Project Portfolio ATKG Index (portfolio_atkg_index.json)
portfolio_idx = build_portfolio_atkg_index(all_exported_payloads)
_safe_write_json('webapp/api/portfolio_atkg_index.json', portfolio_idx)
print(f'Wrote webapp/api/portfolio_atkg_index.json ({portfolio_idx["projects_count"]} projects indexed)')

lock_reg = build_and_verify_master_registry(write_file=True)
shutil.copy2('spatial_lock_registry.json', 'webapp/api/spatial_lock_registry.json')
print(f'Wrote webapp/api/spatial_lock_registry.json ({lock_reg["total_notes"]} locked notes, verified_100_pct={lock_reg["verified_100_pct"]})')

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
        if fn.endswith('.js') and not fn.startswith('hafetz44_audit_') and fn != 'audit_3d_overlay.js':
            shutil.copy2(os.path.join(src_dir, fn), os.path.join(dst_dir, fn))

    # Ensure fresh audit_3d_overlay.js in both dst_dir and src_dir
    if os.path.isfile('webapp/audit_3d_overlay.js'):
        shutil.copy2('webapp/audit_3d_overlay.js', os.path.join(dst_dir, 'audit_3d_overlay.js'))
        try:
            shutil.copy2('webapp/audit_3d_overlay.js', os.path.join(src_dir, 'audit_3d_overlay.js'))
        except Exception:
            pass

    # Sync HTML viewers and ensure runtime overlay script is injected before the LAST </body>
    html_files = set(filter(None, [cfg.get('primary_viewer'), cfg.get('bim_viewer'), cfg.get('spatial_map')]))
    overlay_block = (
        f'\n<!-- ARCHICHECK_3D_OVERLAY_START -->\n'
        f'<script>window.__ARCHICHECK_PROJECT_ID__ = "{pid}";</script>\n'
        f'<script src="/audit_3d_overlay.js?v=7.5"></script>\n'
        f'<!-- ARCHICHECK_3D_OVERLAY_END -->\n'
    )
    for html_fn in html_files:
        src_html = os.path.join(src_dir, html_fn)
        dst_html = os.path.join(dst_dir, html_fn)
        if not os.path.isfile(src_html):
            continue
        with open(src_html, 'r', encoding='utf-8', errors='replace') as fh:
            html_content = fh.read()

        # Guard against overwriting rich 3D BIM models with redirect stubs (and reverse-heal central folder if needed)
        if 'ZERO-COPY-CENTRAL-MODEL-REDIRECT' in html_content or len(html_content) < 5000:
            if os.path.isfile(dst_html) and os.path.getsize(dst_html) > 20000:
                print(f'Preserving full 3D viewer and reverse-healing central folder: {dst_html} -> {src_html}')
                with open(dst_html, 'r', encoding='utf-8', errors='replace') as dfh:
                    html_content = dfh.read()
                while '<!-- ARCHICHECK_3D_OVERLAY_START -->' in html_content and '<!-- ARCHICHECK_3D_OVERLAY_END -->' in html_content:
                    s_idx = html_content.index('<!-- ARCHICHECK_3D_OVERLAY_START -->')
                    e_idx = html_content.index('<!-- ARCHICHECK_3D_OVERLAY_END -->') + len('<!-- ARCHICHECK_3D_OVERLAY_END -->')
                    html_content = html_content[:s_idx] + html_content[e_idx:]
                last_body_idx = html_content.rfind('</body>')
                if last_body_idx != -1:
                    html_content = html_content[:last_body_idx] + overlay_block + html_content[last_body_idx:]
                else:
                    html_content += overlay_block
                with open(dst_html, 'w', encoding='utf-8', newline='\n') as fh:
                    fh.write(html_content)
                try:
                    with open(src_html, 'w', encoding='utf-8', newline='\n') as sfh:
                        sfh.write(html_content)
                except Exception:
                    pass
                continue

        while '<!-- ARCHICHECK_3D_OVERLAY_START -->' in html_content and '<!-- ARCHICHECK_3D_OVERLAY_END -->' in html_content:
            s_idx = html_content.index('<!-- ARCHICHECK_3D_OVERLAY_START -->')
            e_idx = html_content.index('<!-- ARCHICHECK_3D_OVERLAY_END -->') + len('<!-- ARCHICHECK_3D_OVERLAY_END -->')
            html_content = html_content[:s_idx] + html_content[e_idx:]

        last_body_idx = html_content.rfind('</body>')
        if last_body_idx != -1:
            html_content = html_content[:last_body_idx] + overlay_block + html_content[last_body_idx:]
        else:
            html_content += overlay_block

        with open(dst_html, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(html_content)
        print(f'Synced 3D viewer to static hosting: {dst_html}')

    # Also ensure index.html in dst_dir is a copy of primary_viewer
    primary_v = cfg.get('primary_viewer')
    if primary_v:
        src_pv = os.path.join(dst_dir, primary_v)
        dst_idx = os.path.join(dst_dir, 'index.html')
        if os.path.isfile(src_pv):
            shutil.copy2(src_pv, dst_idx)

    # If Hafetz Haim 44 has offline standalone overlay in central folder, keep it in sync
    if pid == 'hafetz44':
        if os.path.isdir(src_dir):
            with open('webapp/api/hafetz44.json', 'r', encoding='utf-8') as jf:
                h44_json_str = jf.read()
            with open('webapp/audit_3d_overlay.js', 'r', encoding='utf-8') as of:
                ov_js_str = of.read()
            preload_payload = (
                f'window.__ARCHICHECK_PROJECT_ID__ = "hafetz44";\n'
                f'window.__ARCHICHECK_EMBEDDED_DATA__ = {h44_json_str};\n'
            )
            standalone_payload = (
                f'window.__ARCHICHECK_PROJECT_ID__ = "hafetz44";\n'
                f'window.__ARCHICHECK_EMBEDDED_DATA__ = {h44_json_str};\n'
                f'{ov_js_str}\n'
            )
            for target_folder in (src_dir, dst_dir):
                try:
                    preload_path = os.path.join(target_folder, 'hafetz44_audit_preload.js')
                    with open(preload_path, 'w', encoding='utf-8', newline='\n') as pf:
                        pf.write(preload_payload)
                    standalone_path = os.path.join(target_folder, 'hafetz44_audit_3d_standalone.js')
                    with open(standalone_path, 'w', encoding='utf-8', newline='\n') as sf:
                        sf.write(standalone_payload)
                    print(f'Updated preload & standalone offline overlays in: {target_folder}')
                except Exception as ex:
                    print(f'Notice: Could not update standalone overlays in {target_folder}: {ex}')

print('Static export complete!')
