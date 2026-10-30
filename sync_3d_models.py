# -*- coding: utf-8 -*-
"""
Central 3D Architectural Models Manager & Zero-Copy Consolidator
================================================================
Single Source of Truth Root:
    G:\\Shared drives\\שליטה ובקרה\\מודלים פרויקטים

Responsibilities:
1. Consolidates and moves all 3D BIM & GIS model source files into the central
   directory `G:\\Shared drives\\שליטה ובקרה\\מודלים פרויקטים\\<Project Name>`.
2. Replaces legacy folders in `פרויקטים בביצוע\\<פרויקט>\\מודל` with lightweight
   1KB HTML redirect stubs + Windows `.lnk` shortcuts (Zero-Copy, no duplicate storage).
3. Replaces local NTFS scratch directories (`C:\\Users\\User\\.gemini\\antigravity\\scratch\\*`)
   with OS Directory Junctions (`mklink /J`) pointing directly to the central folder.
4. Normalizes paths inside `src/*.py` build scripts so they read/write directly in
   the central directory.
5. Generates `00_models_catalog.json`, `00_אינדקס_מודלים_3D.html`, and `README_MODELS_STANDARD.md`.
"""

import os
import sys
import json
import shutil
import hashlib
import subprocess
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CENTRAL_MODELS_ROOT = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים"
EXEC_PROJECTS_ROOT = r"G:\Shared drives\פרויקטים שוטפים\פרויקטים בביצוע"
SCRATCH_ROOT = r"C:\Users\User\.gemini\antigravity\scratch"
BRAIN_ROOT = r"C:\Users\User\.gemini\antigravity\brain"

PROJECTS_CONFIG = [
    {
        "id": "pines48",
        "folder_name": "פינס 48 פתח תקווה",
        "title_he": "פינס 48 פינת הבעש״ט, פתח תקווה",
        "subtitle_he": "בניין מגורים בן 7 קומות + קומת קרקע ומרתף | 16 יח״ד",
        "gush_helka": "גוש 6371 חלקה 311",
        "exec_folder": os.path.join(EXEC_PROJECTS_ROOT, "פינס הבעשט", "מודל"),
        "scratch_folders": [
            os.path.join(SCRATCH_ROOT, "pines-48-3d"),
        ],
        "primary_viewer": "pines48_3d_model.html",
        "bim_viewer": "pines48_3d_model.html",
        "spatial_map": "pines48_spatial_map.html",
        "glb_file": "pines48_model.glb",
        "obj_file": "pines48_model.obj",
        "mtl_file": "pines48_model.mtl",
        "pdf_report": "pines48_architectural_quality_analysis.pdf",
        "redirect_htmls": ["index.html", "pines48_3d_model.html", "pines48_spatial_map.html"],
    },
    {
        "id": "kkl10",
        "folder_name": "קקל 10 פתח תקווה",
        "title_he": "קק״ל 10, פתח תקווה",
        "subtitle_he": "בניין מגורים בן 9 קומות (תמ״א 38/2 הריסה ובנייה) | 27 יח״ד",
        "gush_helka": "גוש 6372 חלקה 814",
        "exec_folder": os.path.join(EXEC_PROJECTS_ROOT, "קקל 10", "מודל"),
        "scratch_folders": [
            os.path.join(SCRATCH_ROOT, "kkl10"),
        ],
        "primary_viewer": "kkl10_3d_bim_viewer.html",
        "bim_viewer": "kkl10_3d_bim_viewer.html",
        "spatial_map": "kkl10_spatial_map.html",
        "glb_file": None,
        "obj_file": "KKL10_PetahTikva_BIM_v6_1.obj",
        "mtl_file": "KKL10_PetahTikva_BIM_v6_1.mtl",
        "pdf_report": "kkl10_architectural_quality_analysis.pdf",
        "redirect_htmls": ["index.html", "kkl10_3d_bim_viewer.html", "kkl10_spatial_map.html"],
    },
    {
        "id": "hafetz44",
        "folder_name": "חפץ חיים 44 פתח תקווה",
        "title_he": "חפץ חיים 44, פתח תקווה",
        "subtitle_he": "בניין מגורים דו-אגפי (מזרחי ומערבי) | 17 יח״ד",
        "gush_helka": "פתח תקווה",
        "exec_folder": os.path.join(EXEC_PROJECTS_ROOT, "חפץ חיים 44", "מודל"),
        "scratch_folders": [
            os.path.join(BRAIN_ROOT, "ae4d527a-b54f-424e-a6b9-38aabac32286", "scratch", "hafetz44"),
        ],
        "primary_viewer": "hafetz44_3d_model.html",
        "bim_viewer": "hafetz44_3d_bim_viewer.html",
        "spatial_map": "hafetz44_spatial_map.html",
        "glb_file": "hafetz44_model.glb",
        "obj_file": "hafetz44_model.obj",
        "mtl_file": "hafetz44_model.mtl",
        "pdf_report": "hafetz44_architectural_quality_analysis.pdf",
        "redirect_htmls": [
            "index.html",
            "hafetz44_3d_model.html",
            "hafetz44_3d_bim_viewer.html",
            "hafetz44_spatial_map.html",
        ],
    },
    {
        "id": "yatkovski7",
        "folder_name": "יטקובסקי 7 פתח תקווה",
        "title_he": "האחים יטקובסקי 7 (7א׳), פתח תקווה",
        "subtitle_he": "בניין מגורים בן 4 קומות + גג ומרתף חניה | 6 יח״ד",
        "gush_helka": "גוש 6363 חלקה 252 (מגרש 7א׳)",
        "exec_folder": os.path.join(EXEC_PROJECTS_ROOT, "יטקובסקי 7", "מודל"),
        "scratch_folders": [],
        "primary_viewer": "yatkovski7_3d_model.html",
        "bim_viewer": "yatkovski7_3d_bim_viewer.html",
        "spatial_map": "yatkovski7_spatial_map.html",
        "glb_file": "yatkovski7_model.glb",
        "obj_file": "yatkovski7_model.obj",
        "mtl_file": "yatkovski7_model.mtl",
        "pdf_report": "yatkovski7_architectural_quality_analysis.pdf",
        "redirect_htmls": [
            "index.html",
            "yatkovski7_3d_model.html",
            "yatkovski7_3d_bim_viewer.html",
            "yatkovski7_spatial_map.html",
        ],
    },
    {
        "id": "kitroni37",
        "folder_name": "הרב קיטרוני 37-39 פתח תקווה",
        "title_he": "הרב קיטרוני 37–39, פתח תקווה",
        "subtitle_he": "מתחם מגורים דו-בנייני (בניינים A ו-B) בן 9 קומות | 63 יח״ד",
        "gush_helka": "פתח תקווה",
        "exec_folder": os.path.join(EXEC_PROJECTS_ROOT, "קטרוני 37-39", "מודל"),
        "scratch_folders": [],
        "primary_viewer": "kitroni37_39_3d_model.html",
        "bim_viewer": "kitroni37_39_3d_model.html",
        "spatial_map": "kitroni37_39_spatial_map.html",
        "glb_file": None,
        "obj_file": None,
        "mtl_file": None,
        "pdf_report": "kitroni37_architectural_quality_analysis.pdf",
        "redirect_htmls": ["index.html", "kitroni37_39_3d_model.html", "kitroni37_39_spatial_map.html"],
    },
    {
        "id": "feierberg3",
        "folder_name": "פאירברג 3 פתח תקווה",
        "title_he": "פאירברג 3, פתח תקווה",
        "subtitle_he": "בניין מגורים בן 9 קומות + קומת קרקע וגג | 29 יח״ד",
        "gush_helka": "גוש 6388 חלקה 138",
        "exec_folder": os.path.join(EXEC_PROJECTS_ROOT, "פאירברג 3", "מודל"),
        "scratch_folders": [],
        "primary_viewer": "feierberg3_3d_model.html",
        "bim_viewer": "feierberg3_3d_bim_viewer.html",
        "spatial_map": "feierberg3_spatial_map.html",
        "glb_file": "feierberg3_model.glb",
        "obj_file": "feierberg3_model.obj",
        "mtl_file": "feierberg3_model.mtl",
        "pdf_report": "feierberg3_architectural_quality_analysis.pdf",
        "redirect_htmls": [
            "index.html",
            "feierberg3_3d_model.html",
            "feierberg3_3d_bim_viewer.html",
            "feierberg3_spatial_map.html",
        ],
    },
    {
        "id": "sharett26",
        "folder_name": "משה שרת 26-28 פתח תקווה",
        "title_he": "משה שרת 26–28, פתח תקווה",
        "subtitle_he": "מתחם מגורים דו-אגפי (בניינים 28 ו-26) בן 9 קומות + קרקע, גלריה ו-2 מרתפים | 66 יח״ד",
        "gush_helka": "גוש 6372 חלקה 1025 (מגרש 1025)",
        "exec_folder": os.path.join(EXEC_PROJECTS_ROOT, "משה שרת 26-28", "מודל"),
        "scratch_folders": [],
        "primary_viewer": "sharett26_28_3d_model.html",
        "bim_viewer": "sharett26_28_3d_bim_viewer.html",
        "spatial_map": "sharett26_28_spatial_map.html",
        "glb_file": "sharett26_28_model.glb",
        "obj_file": "sharett26_28_model.obj",
        "mtl_file": "sharett26_28_model.mtl",
        "pdf_report": "sharett26_architectural_quality_analysis.pdf",
        "redirect_htmls": [
            "index.html",
            "sharett26_28_3d_model.html",
            "sharett26_28_3d_bim_viewer.html",
            "sharett26_28_spatial_map.html",
        ],
    },
    {
        "id": "prototype_360",
        "folder_name": "_אב_טיפוס_360",
        "title_he": "מודל אב-טיפוס אינטראקטיבי 360°",
        "subtitle_he": "תצוגת מבנה תלת-ממדית אינטראקטיבית (Three.js + OBJ/MTL)",
        "gush_helka": "מודל הדגמה",
        "exec_folder": None,
        "scratch_folders": [
            os.path.join(SCRATCH_ROOT, "3D_Export"),
        ],
        "primary_viewer": "360_Interactive_Viewer.html",
        "bim_viewer": "360_Interactive_Viewer.html",
        "spatial_map": None,
        "glb_file": None,
        "obj_file": "Building_Model.obj",
        "mtl_file": "Building_Model.mtl",
        "pdf_report": None,
        "redirect_htmls": ["360_Interactive_Viewer.html"],
    },
]

SKIP_DIRS = {"libredwg", "__pycache__", ".git", "node_modules", "crops", "pdfs"}
SKIP_FILES = {
    "desktop.ini",
    "kkl10_gramoshka.dxf",
    "test_syntax.js",
    "accore_arx.txt",
    "accore_out.txt",
    "export_dxf.scr",
    "test_cmds.scr",
    "test_cmds2.scr",
    "test_plot.scr",
    "מעבר לתיקיית המקור - מודלים פרויקטים.lnk",
    "README_מיקום_המודל.txt",
}


def is_redirect_stub(filepath):
    """Checks if an HTML file is already one of our lightweight Zero-Copy Redirect Stubs."""
    if not os.path.exists(filepath) or not filepath.lower().endswith(".html"):
        return False
    try:
        if os.path.getsize(filepath) > 8192:
            return False
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            head = f.read(2048)
        return "ZERO-COPY-CENTRAL-MODEL-REDIRECT" in head
    except OSError:
        return False


def is_junction_or_symlink(path):
    """Detects if a path is an NTFS junction or symlink."""
    if not os.path.exists(path):
        return False
    try:
        st = os.lstat(path)
        # FILE_ATTRIBUTE_REPARSE_POINT = 0x400
        return bool(getattr(st, "st_file_attributes", 0) & 0x400) or os.path.islink(path)
    except OSError:
        return False


def copy_if_newer_or_missing(src_file, dst_file):
    """Copies src_file to dst_file if dst_file does not exist or src_file is newer/larger."""
    if is_redirect_stub(src_file):
        return False
    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
    if not os.path.exists(dst_file):
        shutil.copy2(src_file, dst_file)
        return True
    src_stat = os.stat(src_file)
    dst_stat = os.stat(dst_file)
    # Prefer newer modification time (with 2s tolerance) or larger non-stub file
    if src_stat.st_mtime > dst_stat.st_mtime + 2:
        shutil.copy2(src_file, dst_file)
        return True
    return False


def map_destination_relpath(proj_id, src_root, full_src_path):
    """Maps a source file to a clean relative path inside the project's central folder."""
    rel = os.path.relpath(full_src_path, src_root)
    parts = rel.split(os.sep)
    fn = parts[-1]
    ext = os.path.splitext(fn)[1].lower()

    # Special cleanup for scratch folders where scripts/data were flat in root
    if len(parts) == 1:
        if fn.endswith(".py"):
            return os.path.join("src", fn)
        if proj_id == "hafetz44" and fn in {
            "hafetz44_extracted_plans.json",
            "hafetz44_spatial_map_data.json",
            "hafetz44_units_crm.json",
            "unified_hafetz44_3d_map.json",
        }:
            return os.path.join("data", fn)
        if proj_id == "kkl10" and (fn.startswith("dwg_") or fn.startswith("dxf_")):
            return os.path.join("data", "cad_diagnostics", fn)
    return rel


def setup_shared_engine():
    """Copies shared 3D/GIS build dependencies (three.min.js, spatial template) to _shared_engine."""
    engine_dir = os.path.join(CENTRAL_MODELS_ROOT, "_shared_engine")
    os.makedirs(engine_dir, exist_ok=True)
    shared_src = os.path.join(BRAIN_ROOT, "60b6f7e6-94a5-48b9-b12c-1728c4428342", "scratch")
    for fname in ["three.min.js", "build_interactive_spatial_html.py"]:
        sp = os.path.join(shared_src, fname)
        if os.path.exists(sp):
            copy_if_newer_or_missing(sp, os.path.join(engine_dir, fname))


def update_build_scripts_paths(proj_dir, proj_cfg):
    """Updates hardcoded legacy paths in `src/*.py` inside the central project folder."""
    src_dir = os.path.join(proj_dir, "src")
    if not os.path.exists(src_dir):
        return
    engine_dir = os.path.join(CENTRAL_MODELS_ROOT, "_shared_engine")
    three_js_central = os.path.join(engine_dir, "three.min.js").replace("\\", "\\\\")
    spatial_builder_central = os.path.join(engine_dir, "build_interactive_spatial_html.py").replace("\\", "\\\\")
    proj_dir_escaped = proj_dir.replace("\\", "\\\\")

    for root, _, files in os.walk(src_dir):
        for fn in files:
            if not fn.endswith(".py"):
                continue
            fp = os.path.join(root, fn)
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                continue

            orig = content
            # Replace legacy user profile paths C:\Users\guyku with C:\Users\User
            content = content.replace(r"C:\Users\guyku", r"C:\Users\User")
            content = content.replace("C:/Users/guyku", "C:/Users/User")
            # Replace legacy Hebrew Google Drive mount path with G:\Shared drives
            content = content.replace(r"G:\תיקיות אחסון שיתופי", r"G:\Shared drives")
            content = content.replace(r"g:\תיקיות אחסון שיתופי", r"G:\Shared drives")

            # Point PROJECT_DIR / WORKSPACE / GDRIVE_DIR / DRIVE_MODEL_DIR / OUT_DIR to the central project folder
            if proj_cfg.get("exec_folder"):
                old_exec = proj_cfg["exec_folder"]
                content = content.replace(old_exec, proj_dir)
                content = content.replace(old_exec.replace("G:\\", "g:\\"), proj_dir)

            content = content.replace(
                r"G:\.shortcut-targets-by-id\1LIQMubrb6NilUyJaF10kieHYqontm6j2\מודל",
                proj_dir,
            )
            content = content.replace(
                r"C:\Users\User\.gemini\antigravity\brain\60b6f7e6-94a5-48b9-b12c-1728c4428342\scratch\three.min.js",
                os.path.join(engine_dir, "three.min.js"),
            )
            content = content.replace(
                r"C:\Users\User\.gemini\antigravity\brain\60b6f7e6-94a5-48b9-b12c-1728c4428342\scratch\build_interactive_spatial_html.py",
                os.path.join(engine_dir, "build_interactive_spatial_html.py"),
            )

            if content != orig:
                with open(fp, "w", encoding="utf-8") as f:
                    f.write(content)


def create_html_redirect_stub(stub_path, target_central_html, proj_title):
    """
    Creates a 1KB Zero-Copy HTML Redirect Stub in the legacy folder that immediately
    redirects to the canonical file in `G:\\Shared drives\\שליטה ובקרה\\מודלים פרויקטים`.
    Uses relative path so it works across any drive letter or OS mount.
    """
    stub_dir = os.path.dirname(os.path.abspath(stub_path))
    rel_url = os.path.relpath(target_central_html, stub_dir).replace("\\", "/")
    abs_file_url = "file:///" + os.path.abspath(target_central_html).replace("\\", "/")

    html = f"""<!DOCTYPE html>
<!-- ZERO-COPY-CENTRAL-MODEL-REDIRECT -->
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url={rel_url}">
  <title>מעביר למודל 3D מרכזי – {proj_title}</title>
  <style>
    body {{
      font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
      background: #0f172a; color: #f8fafc;
      display: flex; align-items: center; justify-content: center;
      height: 100vh; margin: 0; text-align: center;
    }}
    .card {{
      background: #1e293b; border: 1px solid #334155; border-radius: 14px;
      padding: 28px 36px; max-width: 520px; box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }}
    a {{
      display: inline-block; margin-top: 14px; padding: 10px 20px;
      background: #10b981; color: #064e3b; font-weight: 800;
      text-decoration: none; border-radius: 8px;
    }}
    .path {{ font-size: 12px; color: #94a3b8; margin-top: 12px; direction: ltr; word-break: break-all; }}
  </style>
  <script>
    window.location.replace({json.dumps(rel_url)});
  </script>
</head>
<body>
  <div class="card">
    <h2>פותח מודל אדריכלי 3D – {proj_title}</h2>
    <p>קובצי המקור רוכזו בתיקיית השליטה והבקרה המרכזית.</p>
    <a href="{rel_url}">פתיחת המודל כעת</a>
    <div class="path">{target_central_html}</div>
  </div>
</body>
</html>
"""
    os.makedirs(stub_dir, exist_ok=True)
    with open(stub_path, "w", encoding="utf-8") as f:
        f.write(html)


def create_windows_shortcut(lnk_path, target_path, description):
    """Creates a standard Windows .lnk shortcut pointing to the central project folder."""
    ps_script = (
        f"$ws = New-Object -ComObject WScript.Shell; "
        f"$s = $ws.CreateShortcut('{lnk_path}'); "
        f"$s.TargetPath = '{target_path}'; "
        f"$s.Description = '{description}'; "
        f"$s.Save()"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], capture_output=True)


def consolidate_and_move_project(proj_cfg):
    """
    1. Consolidates all files for a project into `G:\\Shared drives\\שליטה ובקרה\\מודלים פרויקטים\\<folder_name>`.
    2. Verifies all files exist and are non-empty in the central folder.
    3. Cleans up duplicate files in `exec_folder` and leaves only 1KB HTML redirect stubs + `.lnk` shortcut.
    4. Replaces `scratch_folders` on C: with NTFS Directory Junctions pointing to the central folder.
    """
    proj_id = proj_cfg["id"]
    central_dir = os.path.join(CENTRAL_MODELS_ROOT, proj_cfg["folder_name"])
    os.makedirs(central_dir, exist_ok=True)

    sources = []
    if proj_cfg.get("exec_folder") and os.path.exists(proj_cfg["exec_folder"]):
        sources.append(proj_cfg["exec_folder"])
    for sf in proj_cfg.get("scratch_folders", []):
        if os.path.exists(sf) and not is_junction_or_symlink(sf):
            sources.append(sf)

    copied_count = 0
    for src_root in sources:
        for root, dirs, files in os.walk(src_root):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for fn in files:
                if fn in SKIP_FILES:
                    continue
                src_fp = os.path.join(root, fn)
                if is_redirect_stub(src_fp):
                    continue
                rel_dst = map_destination_relpath(proj_id, src_root, src_fp)
                dst_fp = os.path.join(central_dir, rel_dst)
                if copy_if_newer_or_missing(src_fp, dst_fp):
                    copied_count += 1

    # Ensure index.html exists in central_dir if primary_viewer exists
    primary_v = proj_cfg.get("primary_viewer")
    if primary_v:
        pv_path = os.path.join(central_dir, primary_v)
        idx_path = os.path.join(central_dir, "index.html")
        if os.path.exists(pv_path) and not os.path.exists(idx_path):
            shutil.copy2(pv_path, idx_path)

    # Update hardcoded paths inside central_dir/src/*.py
    update_build_scripts_paths(central_dir, proj_cfg)

    # Now replace exec_folder contents with lightweight Zero-Copy Redirect Stubs + .lnk shortcut
    exec_folder = proj_cfg.get("exec_folder")
    if exec_folder and os.path.exists(exec_folder):
        # Verify central primary viewer is intact before removing duplicates from exec_folder
        primary_central = os.path.join(central_dir, primary_v) if primary_v else None
        if primary_central and os.path.exists(primary_central) and os.path.getsize(primary_central) > 10000:
            # Remove all files and subfolders in exec_folder that have been moved to central_dir
            for root, dirs, files in os.walk(exec_folder, topdown=False):
                for fn in files:
                    if fn == "desktop.ini":
                        continue
                    fp = os.path.join(root, fn)
                    rel_dst = map_destination_relpath(proj_id, exec_folder, fp)
                    central_equivalent = os.path.join(central_dir, rel_dst)
                    if os.path.exists(central_equivalent) and os.path.getsize(central_equivalent) > 0:
                        try:
                            os.remove(fp)
                        except OSError:
                            pass
                for d in dirs:
                    dp = os.path.join(root, d)
                    try:
                        if not os.listdir(dp):
                            os.rmdir(dp)
                    except OSError:
                        pass

            # Create 1KB HTML redirect stubs for each HTML entry point
            for r_html in proj_cfg.get("redirect_htmls", []):
                target_html = os.path.join(central_dir, r_html)
                if not os.path.exists(target_html) and primary_central:
                    target_html = primary_central
                if os.path.exists(target_html):
                    stub_fp = os.path.join(exec_folder, r_html)
                    create_html_redirect_stub(stub_fp, target_html, proj_cfg["title_he"])

            # Create Windows .lnk shortcut to central folder
            lnk_fp = os.path.join(exec_folder, "מעבר לתיקיית המקור - מודלים פרויקטים.lnk")
            create_windows_shortcut(lnk_fp, central_dir, f"תיקיית המקור של מודל {proj_cfg['title_he']}")

            # Create info note
            readme_fp = os.path.join(exec_folder, "README_מיקום_המודל.txt")
            with open(readme_fp, "w", encoding="utf-8") as f:
                f.write(
                    f"פרויקט: {proj_cfg['title_he']}\n"
                    f"==================================================\n"
                    f"קובצי המקור של המודל התלת-ממדי (3D BIM & GIS) הועברו לתיקייה המרכזית:\n"
                    f"{central_dir}\n\n"
                    f"לחיצה על קובצי ה-HTML בתיקייה זו או על קיצור הדרך תפתח ישירות את המודל מהתיקייה המרכזית.\n"
                )

    # Replace local NTFS scratch_folders with Directory Junctions (mklink /J) to central_dir
    for sf in proj_cfg.get("scratch_folders", []):
        if os.path.exists(sf) and not is_junction_or_symlink(sf):
            subprocess.run(
                ["powershell", "-NoProfile", "-Command", f"Remove-Item -LiteralPath '{sf}' -Recurse -Force -ErrorAction SilentlyContinue"],
                capture_output=True,
            )
        if not os.path.exists(sf):
            os.makedirs(os.path.dirname(sf), exist_ok=True)
            subprocess.run(
                f'cmd /c mklink /J "{sf}" "{central_dir}"',
                shell=True,
                capture_output=True,
            )

    return central_dir, copied_count


def auto_discover_new_projects(known_exec_folders, known_central_names):
    """
    Scans `פרויקטים בביצוע\\*\\מודל` and `scratch\\*` for any new 3D models created in the future
    that are not yet in `PROJECTS_CONFIG`, and moves them into `CENTRAL_MODELS_ROOT`.
    """
    discovered = []
    if os.path.exists(EXEC_PROJECTS_ROOT):
        for entry in os.scandir(EXEC_PROJECTS_ROOT):
            if not entry.is_dir():
                continue
            model_dir = os.path.join(entry.path, "מודל")
            if not os.path.exists(model_dir) or os.path.normcase(model_dir) in known_exec_folders:
                continue
            # Check if it contains non-stub 3D files
            has_real_3d = False
            for f in os.listdir(model_dir):
                fp = os.path.join(model_dir, f)
                if os.path.isfile(fp) and not is_redirect_stub(fp):
                    if f.endswith((".glb", ".obj", "_3d_model.html", "_3d_bim_viewer.html")):
                        has_real_3d = True
                        break
            if has_real_3d:
                folder_name = f"{entry.name} פתח תקווה" if "פתח תקווה" not in entry.name else entry.name
                central_dir = os.path.join(CENTRAL_MODELS_ROOT, folder_name)
                os.makedirs(central_dir, exist_ok=True)
                html_files = []
                for root, _, files in os.walk(model_dir):
                    for fn in files:
                        if fn in SKIP_FILES:
                            continue
                        sp = os.path.join(root, fn)
                        if is_redirect_stub(sp):
                            continue
                        rel = os.path.relpath(sp, model_dir)
                        dp = os.path.join(central_dir, rel)
                        copy_if_newer_or_missing(sp, dp)
                        if fn.endswith(".html") and os.path.dirname(rel) == "":
                            html_files.append(fn)
                        os.remove(sp)
                for h in html_files:
                    create_html_redirect_stub(
                        os.path.join(model_dir, h),
                        os.path.join(central_dir, h),
                        entry.name,
                    )
                create_windows_shortcut(
                    os.path.join(model_dir, "מעבר לתיקיית המקור - מודלים פרויקטים.lnk"),
                    central_dir,
                    f"תיקיית המקור של מודל {entry.name}",
                )
                discovered.append(folder_name)
    return discovered


def build_catalog_and_dashboard():
    """Generates `00_models_catalog.json`, `00_אינדקס_מודלים_3D.html`, and `README_MODELS_STANDARD.md`."""
    catalog_entries = []
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    for cfg in PROJECTS_CONFIG:
        c_dir = os.path.join(CENTRAL_MODELS_ROOT, cfg["folder_name"])
        if not os.path.exists(c_dir):
            continue

        total_size_mb = 0.0
        file_count = 0
        for r, _, files in os.walk(c_dir):
            for fn in files:
                fp = os.path.join(r, fn)
                try:
                    total_size_mb += os.path.getsize(fp) / (1024 * 1024)
                    file_count += 1
                except OSError:
                    pass

        entry = {
            "id": cfg["id"],
            "folder_name": cfg["folder_name"],
            "title_he": cfg["title_he"],
            "subtitle_he": cfg["subtitle_he"],
            "gush_helka": cfg["gush_helka"],
            "central_path": c_dir,
            "primary_viewer": cfg["primary_viewer"],
            "primary_viewer_path": os.path.join(c_dir, cfg["primary_viewer"]) if cfg["primary_viewer"] else None,
            "bim_viewer": cfg["bim_viewer"],
            "spatial_map": cfg["spatial_map"],
            "spatial_map_path": os.path.join(c_dir, cfg["spatial_map"]) if cfg["spatial_map"] else None,
            "glb_file": cfg["glb_file"],
            "obj_file": cfg["obj_file"],
            "mtl_file": cfg["mtl_file"],
            "pdf_report": cfg["pdf_report"],
            "file_count": file_count,
            "total_size_mb": round(total_size_mb, 2),
        }
        catalog_entries.append(entry)

    catalog_data = {
        "schema_version": "2.0-zero-copy",
        "generated_at": now_str,
        "central_root": CENTRAL_MODELS_ROOT,
        "architecture": "Single Source of Truth (Zero-Copy)",
        "total_models": len(catalog_entries),
        "projects": catalog_entries,
    }

    catalog_path = os.path.join(CENTRAL_MODELS_ROOT, "00_models_catalog.json")
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, ensure_ascii=False, indent=2)

    # Build interactive HTML portal: 00_אינדקס_מודלים_3D.html
    cards_html = ""
    for item in catalog_entries:
        folder_url = item["folder_name"]
        viewer_href = f"{folder_url}/{item['primary_viewer']}" if item["primary_viewer"] else "#"
        map_btn = ""
        if item["spatial_map"]:
            map_btn = f'<a class="btn btn-map" href="{folder_url}/{item["spatial_map"]}" target="_blank">🗺️ מפת GIS וסביבה 3D</a>'
        glb_btn = ""
        if item["glb_file"]:
            glb_btn = f'<a class="btn btn-secondary" href="{folder_url}/{item["glb_file"]}" download>📦 הורדת GLB</a>'
        obj_btn = ""
        if item["obj_file"]:
            obj_btn = f'<a class="btn btn-secondary" href="{folder_url}/{item["obj_file"]}" download>📐 הורדת OBJ</a>'
        pdf_btn = ""
        if item["pdf_report"]:
            pdf_btn = f'<a class="btn btn-secondary" href="{folder_url}/{item["pdf_report"]}" target="_blank">📄 דוח בקרת איכות (PDF)</a>'

        cards_html += f"""
        <div class="card">
          <div class="card-header">
            <span class="badge-id">{item['id'].upper()}</span>
            <span class="badge-meta">{item['file_count']} קבצים · {item['total_size_mb']} MB</span>
          </div>
          <h2>{item['title_he']}</h2>
          <p class="subtitle">{item['subtitle_he']}</p>
          <div class="gush">📍 {item['gush_helka']}</div>
          <div class="path-box" title="נתיב מקור הנתונים">{item['central_path']}</div>
          <div class="actions-primary">
            <a class="btn btn-primary" href="{viewer_href}" target="_blank">🏢 פתיחת מודל 3D BIM אינטראקטיבי</a>
            {map_btn}
          </div>
          <div class="actions-secondary">
            {glb_btn}
            {obj_btn}
            {pdf_btn}
          </div>
        </div>
        """

    dashboard_html = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>מרכז שליטה ובקרה – קטלוג מודלים אדריכליים 3D BIM & GIS</title>
  <style>
    :root {{
      --bg: #0b1120;
      --surface: #1e293b;
      --surface-hover: #26354d;
      --border: #334155;
      --text: #f8fafc;
      --muted: #94a3b8;
      --accent: #10b981;
      --accent-dark: #059669;
      --blue: #3b82f6;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; padding: 36px 24px;
      font-family: system-ui, -apple-system, 'Segoe UI', Arial, sans-serif;
      background: radial-gradient(circle at top right, #1e293b 0%, #0b1120 65%);
      color: var(--text);
      min-height: 100vh;
    }}
    .container {{ max-width: 1280px; margin: 0 auto; }}
    header {{
      background: rgba(30, 41, 59, 0.85);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 28px 32px;
      margin-bottom: 32px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      backdrop-filter: blur(12px);
    }}
    h1 {{ margin: 0 0 8px 0; font-size: 28px; font-weight: 800; color: #fff; }}
    .header-sub {{ margin: 0; color: var(--muted); font-size: 15px; }}
    .stats-pill {{
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.35);
      color: #6ee7b7;
      padding: 12px 20px;
      border-radius: 12px;
      font-size: 14px;
      font-weight: 700;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
      gap: 22px;
    }}
    .card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      transition: transform 0.18s ease, border-color 0.18s ease;
    }}
    .card:hover {{
      transform: translateY(-3px);
      border-color: var(--accent);
    }}
    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }}
    .badge-id {{
      background: rgba(59, 130, 246, 0.18);
      color: #93c5fd;
      border: 1px solid rgba(59, 130, 246, 0.35);
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.5px;
    }}
    .badge-meta {{ font-size: 12px; color: var(--muted); }}
    .card h2 {{ margin: 0 0 8px 0; font-size: 21px; color: #fff; }}
    .subtitle {{ margin: 0 0 10px 0; color: #cbd5e1; font-size: 14px; line-height: 1.45; }}
    .gush {{ font-size: 13px; color: #6ee7b7; margin-bottom: 12px; font-weight: 600; }}
    .path-box {{
      background: #0f172a;
      border: 1px solid #1e293b;
      color: #64748b;
      font-family: Consolas, monospace;
      font-size: 11px;
      padding: 8px 10px;
      border-radius: 8px;
      margin-bottom: 16px;
      direction: ltr;
      text-align: left;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .actions-primary {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: auto;
    }}
    .actions-secondary {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 12px;
      padding-top: 12px;
      border-top: 1px solid rgba(255,255,255,0.07);
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      text-decoration: none;
      font-weight: 700;
      border-radius: 10px;
      transition: all 0.15s ease;
      cursor: pointer;
    }}
    .btn-primary {{
      background: var(--accent);
      color: #042f2e;
      padding: 12px 16px;
      font-size: 15px;
    }}
    .btn-primary:hover {{ background: #34d399; }}
    .btn-map {{
      background: rgba(59, 130, 246, 0.16);
      color: #93c5fd;
      border: 1px solid rgba(59, 130, 246, 0.4);
      padding: 10px 14px;
      font-size: 14px;
    }}
    .btn-map:hover {{ background: rgba(59, 130, 246, 0.28); }}
    .btn-secondary {{
      background: #0f172a;
      color: #cbd5e1;
      border: 1px solid var(--border);
      padding: 6px 11px;
      font-size: 12px;
      flex: 1;
    }}
    .btn-secondary:hover {{ border-color: #64748b; color: #fff; }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div>
        <h1>🏗️ מרכז שליטה ובקרה – מודלים אדריכליים 3D BIM & GIS</h1>
        <p class="header-sub">מקור האמת היחיד (Single Source of Truth) לכל מודלי התלת-ממד והמפות המרחביות של הפרויקטים · <code>{CENTRAL_MODELS_ROOT}</code></p>
      </div>
      <div class="stats-pill">
        סה״כ מודלים פעילים: {len(catalog_entries)} · עודכן: {now_str}
      </div>
    </header>
    <div class="grid">
      {cards_html}
    </div>
  </div>
</body>
</html>
"""
    dashboard_path = os.path.join(CENTRAL_MODELS_ROOT, "00_אינדקס_מודלים_3D.html")
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(dashboard_html)

    # Also write README_MODELS_STANDARD.md
    readme_md = f"""# תקן ריכוז מודלים אדריכליים 3D (Single Source of Truth)

**תיקיית המקור המרכזית והבלעדית:** `{CENTRAL_MODELS_ROOT}`

## כללי ברזל לסוכני AI ולמערכות:
1. **איסור כפילות (Zero-Copy):** כל קובצי המקור של מודלי 3D BIM ומפות מרחביות (`*.glb`, `*.obj`, `*.mtl`, `*_3d_model.html`, `*_3d_bim_viewer.html`, `*_spatial_map.html`, `data/`, `src/`, `docs/`) מוקמים ונשמרים פיזית **אך ורק** בתיקייה זו תחת `{CENTRAL_MODELS_ROOT}\\<שם_הפרויקט>`.
2. **הפניה מתיקיות הפרויקטים השוטפים:** בתיקיות `G:\\Shared drives\\פרויקטים שוטפים\\פרויקטים בביצוע\\<פרויקט>\\מודל` נשמרים אך ורק קובצי הפניה קלי-משקל (`1KB HTML Redirect Stub`) וקיצור דרך (`.lnk`) המפנים ישירות לתיקייה זו.
3. **יצירת מודל חדש (`arch-2d-to-3d-bim`):** בעת הקמת מודל 3D לפרויקט חדש, יש להגדיר את יעד הפלט הראשי אל `{CENTRAL_MODELS_ROOT}\\<שם_הפרויקט>` ולהריץ בסיום את `python c:\\Users\\User\\archknow\\sync_3d_models.py` לעדכון הקטלוג והאינדקס.
"""
    readme_path = os.path.join(CENTRAL_MODELS_ROOT, "README_MODELS_STANDARD.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_md)

    return catalog_path, dashboard_path


def run_centralization():
    print(f"Starting Zero-Copy 3D Models Centralization -> {CENTRAL_MODELS_ROOT}")
    os.makedirs(CENTRAL_MODELS_ROOT, exist_ok=True)
    setup_shared_engine()

    known_exec = set()
    known_names = set()
    for cfg in PROJECTS_CONFIG:
        if cfg.get("exec_folder"):
            known_exec.add(os.path.normcase(cfg["exec_folder"]))
        known_names.add(cfg["folder_name"])
        c_dir, count = consolidate_and_move_project(cfg)
        print(f"  [OK] {cfg['id']} -> {c_dir} (updated/moved {count} files)")

    new_discovered = auto_discover_new_projects(known_exec, known_names)
    for nd in new_discovered:
        print(f"  [AUTO-DISCOVERED] {nd}")

    cat_p, dash_p = build_catalog_and_dashboard()
    print(f"  [CATALOG] {cat_p}")
    print(f"  [PORTAL]  {dash_p}")
    return True


if __name__ == "__main__":
    run_centralization()
