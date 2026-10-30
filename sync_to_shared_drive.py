# -*- coding: utf-8 -*-
r"""
ArchiCheck -> Google Drive Auto-Sync Service
מסנכרן את כל נתוני הפרויקטים, מסמכי סיכום ההערות וההצעות לשיפור, נתוני השטחים והחזיתות, הדוחות ומאגר הידע אל:
1. G:\Shared drives\שליטה ובקרה\תיקיית גרוק גיא\נתוני תכנון משותפים
2. C:\Users\User\My Drive\antigraviti\Projects\archknow

פועל בסנכרון מלא בפעם הראשונה, ומנטר שינויים (Hash/Mtime) כדי לעדכן רק קבצים ששונו.
כולל אפשרות לריצה כ-Watcher ברקע או פקודה חד-פעמית.
"""

import os
import sys
import json
import time
import shutil
import hashlib
from datetime import datetime
from typing import Union

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_DIR = r"G:\Shared drives\שליטה ובקרה\תיקיית גרוק גיא\נתוני תכנון משותפים"
MY_DRIVE_ARCHKNOW_DIR = r"C:\Users\User\My Drive\antigraviti\Projects\archknow"
MANIFEST_FILE = os.path.join(TARGET_DIR, ".sync_manifest.json")

PROJECT_FOLDERS = {
    "pines48": {
        "folder": "01_פינס_48_פתח_תקווה",
        "name_he": "פינס 48 פינת הבעל שם טוב, פתח תקווה",
        "query": "פינס 48",
        "report_prefix": "pines48"
    },
    "kkl10": {
        "folder": "02_קקל_10_פתח_תקווה",
        "name_he": "קק״ל 10, פתח תקווה",
        "query": "קק״ל 10",
        "report_prefix": "kkl10"
    },
    "hafetz44": {
        "folder": "03_חפץ_חיים_44_פתח_תקווה",
        "name_he": "חפץ חיים 44, פתח תקווה",
        "query": "חפץ חיים 44",
        "report_prefix": "hafetz44"
    },
    "yatkovski7": {
        "folder": "04_יטקובסקי_7_פתח_תקווה",
        "name_he": "יטקובסקי אחים 7, פתח תקווה",
        "query": "יטקובסקי 7",
        "report_prefix": "yatkovski7"
    },
    "kitroni37": {
        "folder": "05_קיטרוני_37_39_פתח_תקווה",
        "name_he": "הרב קיטרוני 37–39, פתח תקווה",
        "query": "קטרוני 37–39",
        "report_prefix": "kitroni37"
    },
    "feierberg3": {
        "folder": "06_פאירברג_3_פתח_תקווה",
        "name_he": "פאירברג 3, פתח תקווה",
        "query": "פאירברג 3",
        "report_prefix": "feierberg3"
    },
    "sharett26": {
        "folder": "07_משה_שרת_26_28_פתח_תקווה",
        "name_he": "משה שרת 26–28, פתח תקווה",
        "query": "משה שרת 26–28",
        "report_prefix": "sharett26"
    }
}


def fmt(val):
    if val is None:
        return "0"
    if isinstance(val, (int, float)):
        if float(val).is_integer():
            return f"{int(val):,}"
        return f"{val:,.2f}".rstrip("0").rstrip(".")
    return str(val)


def compute_sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def compute_file_sha256(filepath: str) -> str:
    if not os.path.exists(filepath):
        return ""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest() -> dict:
    if os.path.exists(MANIFEST_FILE):
        try:
            with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_manifest(manifest: dict):
    try:
        with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[sync] Warning: could not write manifest: {e}", file=sys.stderr)


def write_if_changed(target_path: str, content: Union[str, bytes], manifest: dict) -> bool:
    """Writes file only if sha256 hash has changed. Updates manifest."""
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    if isinstance(content, str):
        content_bytes = content.encode("utf-8")
    else:
        content_bytes = content

    new_hash = compute_sha256(content_bytes)
    rel_key = os.path.relpath(target_path, TARGET_DIR).replace("\\", "/")

    if os.path.exists(target_path) and manifest.get(rel_key) == new_hash:
        return False  # No change

    with open(target_path, "wb") as f:
        f.write(content_bytes)
    manifest[rel_key] = new_hash
    return True


def copy_if_changed(src_path: str, target_path: str, manifest: dict) -> bool:
    """Copies file only if content hash differs."""
    if not os.path.exists(src_path):
        return False
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    src_hash = compute_file_sha256(src_path)
    rel_key = os.path.relpath(target_path, TARGET_DIR).replace("\\", "/")

    if os.path.exists(target_path) and manifest.get(rel_key) == src_hash:
        return False

    shutil.copy2(src_path, target_path)
    manifest[rel_key] = src_hash
    return True


def sync_my_drive_mirror() -> list:
    """Syncs updated source files, reports, and static API exports to C:\\Users\\User\\My Drive\\antigraviti\\Projects\\archknow."""
    synced = []
    if not os.path.exists(MY_DRIVE_ARCHKNOW_DIR):
        return synced

    files_to_copy = [
        "project_summary_builder.py",
        "project_analyzer_service.py",
        "generate_all_summaries_and_reports.py",
        "sync_to_shared_drive.py",
        "api_v1.py",
        "server.py",
        "export_static_data.py",
        "generate_pines48_pdf_report.py",
        "generate_kkl10_pdf_report.py",
        "generate_hafetz44_pdf_report.py",
        "generate_yatkovski7_pdf_report.py",
        "generate_kitroni37_pdf_report.py",
        "webapp/index.html",
        "webapp/app.js",
        "webapp/styles.css",
    ]

    for rel_f in files_to_copy:
        src = os.path.join(BASE_DIR, rel_f)
        dst = os.path.join(MY_DRIVE_ARCHKNOW_DIR, rel_f)
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if not os.path.exists(dst) or compute_file_sha256(src) != compute_file_sha256(dst):
                shutil.copy2(src, dst)
                synced.append(f"MyDrive/archknow/{rel_f}")

    for subdir in ["reports", "webapp/reports", "webapp/api"]:
        src_dir = os.path.join(BASE_DIR, subdir)
        dst_dir = os.path.join(MY_DRIVE_ARCHKNOW_DIR, subdir)
        if os.path.exists(src_dir):
            os.makedirs(dst_dir, exist_ok=True)
            for fn in os.listdir(src_dir):
                s_f = os.path.join(src_dir, fn)
                d_f = os.path.join(dst_dir, fn)
                if os.path.isfile(s_f):
                    if not os.path.exists(d_f) or compute_file_sha256(s_f) != compute_file_sha256(d_f):
                        shutil.copy2(s_f, d_f)
                        synced.append(f"MyDrive/archknow/{subdir}/{fn}")

    return synced


def sync_all(force: bool = False) -> dict:
    """
    Main sync function: gathers all analyses, summary documents, quantitative area/facade tables,
    reports, and rules, and syncs them to Google Drive.
    """
    if not os.path.exists(TARGET_DIR):
        try:
            os.makedirs(TARGET_DIR, exist_ok=True)
        except Exception as e:
            return {"status": "error", "error": f"Target drive folder unreachable: {e}"}

    from project_analyzer_service import get_projects_catalog, analyze_project_by_query
    from validation_engine import load_okf_rules

    manifest = {} if force else load_manifest()
    updated_files = []
    skipped_count = 0

    catalog = get_projects_catalog()
    analyses_by_id = {}
    for pid, meta in PROJECT_FOLDERS.items():
        analyses_by_id[pid] = analyze_project_by_query(meta["query"])

    # 1. Projects Catalog JSON (enriched with quantitative summary metrics)
    enriched_catalog = []
    for p in catalog:
        pid = p["id"]
        p_copy = dict(p)
        pds = analyses_by_id.get(pid, {}).get("project_data_summary", {})
        if pds:
            flr_data = pds.get("flooring_areas", {})
            p_copy["quantitative_summary"] = {
                "above_ground_total_sqm": pds.get("above_ground_areas", {}).get("total_sqm"),
                "underground_total_sqm": pds.get("underground_areas", {}).get("total_sqm"),
                "total_built_area_sqm": pds.get("total_built_area_sqm"),
                "roof_terraces_total_sqm": pds.get("roof_terraces", {}).get("total_sqm"),
                "suspended_balconies_total_sqm": pds.get("suspended_balconies", {}).get("total_sqm"),
                "facades_total_sqm": pds.get("facades", {}).get("total_sqm"),
                "facades_by_direction": {
                    d.get("direction"): d.get("gross_area_sqm")
                    for d in pds.get("facades", {}).get("by_direction", [])
                },
                "flooring_apartments_total_sqm": flr_data.get("total_apartments_flooring_sqm"),
                "flooring_apartments_dry_sqm": flr_data.get("total_apartments_dry_sqm"),
                "flooring_apartments_wet_sqm": flr_data.get("total_apartments_wet_sqm"),
                "flooring_public_total_sqm": flr_data.get("total_public_flooring_sqm"),
                "flooring_balconies_total_sqm": flr_data.get("total_balconies_flooring_sqm"),
                "flooring_grand_total_sqm": flr_data.get("grand_total_flooring_sqm"),
            }
        enriched_catalog.append(p_copy)

    catalog_json_str = json.dumps({"projects": enriched_catalog}, indent=2, ensure_ascii=False)
    target_catalog_json = os.path.join(TARGET_DIR, "00_projects_catalog.json")
    if write_if_changed(target_catalog_json, catalog_json_str, manifest):
        updated_files.append("00_projects_catalog.json")
    else:
        skipped_count += 1

    # 2. Master Navigation Guide for AI Agents (Grok, Claude, ChatGPT)
    master_guide_md = [
        "# תיקיית נתוני תכנון משותפים — בסיס הידע האדריכלי של יצחק קולסקי",
        "**מקור המידע:** מערכת בקרת איכות תכנון ArchiCheck (v2.7 — כולל מסמכי סיכום הערות והצעות לשיפור + שטחי בנייה, מרפסות וחזיתות)",
        "",
        "## 1. סקירת פרויקטי הדגל במאגר:",
        "תיקייה זו מרכזת את כל המידע התכנוני, הדוחות האדריכליים, מסמכי סיכום ההערות וההצעות לשיפור, וטבלאות השטחים והחזיתות עבור סוכני AI (כגון גרוק, קלוד, שיווק ותפעול).",
        "",
        "| תיקייה | פרויקט | דירות וקומות | ציון איכות | מסמך סיכום ושטחים | דוח PDF מלא |",
        "| :--- | :--- | :--- | :---: | :--- | :--- |",
    ]

    for p in catalog:
        pid = p["id"]
        p_cfg = PROJECT_FOLDERS.get(pid, {})
        folder_name = p_cfg.get("folder", pid)
        master_guide_md.append(
            f"| `/{folder_name}` | **{p['name']}** | {p['subtitle']} | **{p['score']}** | "
            f"[סיכום הערות ושטחים]({folder_name}/{pid}_summary_and_areas_report.md) | "
            f"[דוח PDF מלא]({folder_name}/{pid}_architectural_quality_analysis.pdf) |"
        )

    master_guide_md.extend([
        "",
        "---",
        "## 2. טבלת השוואה כמותית רוחבית (שטחי בנייה עיליים, תת-קרקעיים, מרפסות גג, מרפסות תלויות ושטחי חזיתות):",
        "",
        "| פרויקט | בנייה עילית ברוטו (מ״ר) | בנייה תת-קרקעית (מ״ר) | סה״כ בנוי (מ״ר) | מרפסות גג (מ״ר) | מרפסות תלויות (מ״ר) | סך חזיתות (מ״ר) | חלוקה לחזיתות (צפון / דרום / מזרח / מערב) |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |",
    ])

    for p in catalog:
        pid = p["id"]
        pds = analyses_by_id.get(pid, {}).get("project_data_summary", {})
        ag = pds.get("above_ground_areas", {})
        ug = pds.get("underground_areas", {})
        rt = pds.get("roof_terraces", {})
        sb = pds.get("suspended_balconies", {})
        fac = pds.get("facades", {})
        dirs_str = " · ".join([
            f"{d.get('direction')}: {fmt(d.get('gross_area_sqm'))}"
            for d in fac.get("by_direction", [])
        ])
        master_guide_md.append(
            f"| **{p['short_name']}** ({pds.get('apartments_count')} יח״ד) | **{fmt(ag.get('total_sqm'))}** | **{fmt(ug.get('total_sqm'))}** | **{fmt(pds.get('total_built_area_sqm'))}** | **{fmt(rt.get('total_sqm'))}** | **{fmt(sb.get('total_sqm'))}** | **{fmt(fac.get('total_sqm'))}** | {dirs_str} מ״ר |"
        )

    master_guide_md.extend([
        "",
        "## 2ב. טבלת השוואת שטחי ריצוף נטו (קומות מלאות — סך ריצוף דירות, סך ריצוף ציבורי וסך ריצוף מרפסות):",
        "",
        "| פרויקט | סך ריצוף דירות נטו (מ״ר) | ריצוף דירות יבש / רטוב (מ״ר) | סך ריצוף ציבורי נטו (מ״ר) | סך ריצוף מרפסות נטו (מ״ר) | סה״כ שטחי ריצוף בפרויקט (מ״ר) |",
        "| :--- | :---: | :---: | :---: | :---: | :---: |",
    ])

    for p in catalog:
        pid = p["id"]
        pds = analyses_by_id.get(pid, {}).get("project_data_summary", {})
        flr = pds.get("flooring_areas", {})
        master_guide_md.append(
            f"| **{p['short_name']}** ({pds.get('apartments_count')} יח״ד) | **{fmt(flr.get('total_apartments_flooring_sqm'))} מ״ר** | יבש: {fmt(flr.get('total_apartments_dry_sqm'))} · רטוב: {fmt(flr.get('total_apartments_wet_sqm'))} | **{fmt(flr.get('total_public_flooring_sqm'))} מ״ר** | **{fmt(flr.get('total_balconies_flooring_sqm'))} מ״ר** | **{fmt(flr.get('grand_total_flooring_sqm'))} מ״ר** |"
        )

    master_guide_md.extend([
        "",
        "---",
        "## 3. מבנה הקבצים בכל תיקיית פרויקט:",
        "1. `*_summary_and_areas_report.md` / `.html` / `.pdf` — **מסמך סיכום הערות והצעות לשיפור + פירוט מלא של שטחי בנייה עיליים לפי קומות, שטחים תת-קרקעיים, מרפסות גג, מרפסות תלויות ושטחי חזיתות בחלוקה לחזיתות השונות.**",
        "2. `*_areas_and_facades.json` — קובץ JSON מובנה של כל נתוני השטחים, הקומות, המרפסות, החזיתות וסיכום ההערות וההצעות לשיפור.",
        "3. `*_full_analysis.json` — קובץ ה-JSON המלא של הפרויקט הכולל את כל הבדיקות, הציונים, החדרים, הממצאים ונתוני השטחים.",
        "4. `*_architectural_report.md` — דוח אדריכלי מילולי מלא כולל תיאור כל הטיפוסים, החדרים, ההמלצות ונספח השטחים והחזיתות.",
        "5. `*_ai_summary.md` & `*_ai_summary.json` — תקציר מנהלים קומפקטי המותאם להזרקה ישירה לפרומפט של LLM (כולל טבלאות שטחים, חזיתות והצעות לשיפור).",
        "6. `*_architectural_quality_analysis.pdf` / `.html` — הדוחות הוויזואליים המלאים להדפסה או לצפייה.",
        "",
        "## 4. תיקיות נוספות:",
        "- `/00_תקנים_וחוקי_תכנון_OKF` — מאגר 400+ חוקי תכנון ובנייה, תקן ישראלי 1918 (נגישות), NKBA ו-Space Syntax.",
        "- `/00_כלי_חיבור_וסכמות_API` — קובץ הקישור `archknow_client.py`, מפרט `openapi.json` ומדריך החיבור.",
    ])

    target_guide_md = os.path.join(TARGET_DIR, "00_אינדקס_פרויקטים_ומדריך_לסוכנים.md")
    if write_if_changed(target_guide_md, "\n".join(master_guide_md), manifest):
        updated_files.append("00_אינדקס_פרויקטים_ומדריך_לסוכנים.md")
    else:
        skipped_count += 1

    # 3. Synchronize Project Folders
    reports_dir = os.path.join(BASE_DIR, "reports")
    for pid, meta in PROJECT_FOLDERS.items():
        folder_path = os.path.join(TARGET_DIR, meta["folder"])
        os.makedirs(folder_path, exist_ok=True)

        analysis_data = analyses_by_id[pid]
        pds = analysis_data.get("project_data_summary", {})
        ag = pds.get("above_ground_areas", {})
        ug = pds.get("underground_areas", {})
        rt = pds.get("roof_terraces", {})
        sb = pds.get("suspended_balconies", {})
        fac = pds.get("facades", {})
        flr = pds.get("flooring_areas", {})
        sdoc = pds.get("summary_document", {})

        # A. Full Analysis JSON
        json_content = json.dumps(analysis_data, indent=2, ensure_ascii=False)
        target_json = os.path.join(folder_path, f"{pid}_full_analysis.json")
        if write_if_changed(target_json, json_content, manifest):
            updated_files.append(f"{meta['folder']}/{pid}_full_analysis.json")
        else:
            skipped_count += 1

        # A2. Dedicated Quantitative Areas, Facades & Summary JSON
        areas_json_content = json.dumps(pds, indent=2, ensure_ascii=False)
        target_areas_json = os.path.join(folder_path, f"{pid}_areas_and_facades.json")
        if write_if_changed(target_areas_json, areas_json_content, manifest):
            updated_files.append(f"{meta['folder']}/{pid}_areas_and_facades.json")
        else:
            skipped_count += 1

        # B. AI Summary (Markdown & JSON) enriched with Quantitative Areas, Facades & Proposals
        notes = analysis_data.get("notes", [])
        fails = [n for n in notes if n.get("status") == "FAIL"]
        warns = [n for n in notes if n.get("status") == "WARN"]
        passes = [n for n in notes if n.get("status") == "PASS"]

        ai_summary_lines = [
            f"# תקציר מנהלים אדריכלי, שטחים, חזיתות והצעות לשיפור: {analysis_data.get('project_name')}",
            f"**פרטי פרויקט:** {analysis_data.get('project_subtitle')}",
            f"**ציון איכות משוקלל:** {analysis_data.get('overall_score')} / 100",
            f"**חוות דעת מסכמת:** {sdoc.get('overall_verdict', '')}",
            "",
            "## 1. נתוני ליבה ובקרת איכות:",
            f"- בדיקות שעברו (PASS): {len(passes)}",
            f"- התראות איכות וארגונומיה (WARN): {len(warns)}",
            f"- כשלים סטטוטוריים חוקיים (FAIL): {len(fails)} (100% תאימות סטטוטורית)" if not fails else f"- כשלים חוקיים (FAIL): {len(fails)}",
        ]
        for m in analysis_data.get("metrics", []):
            ai_summary_lines.append(f"- **{m.get('label')}:** {m.get('value')} ({m.get('sub', '')})")

        ai_summary_lines.extend([
            "",
            "## 2. ריכוז נתוני שטחים, מרפסות, חזיתות ושטחי ריצוף:",
            f"- **סך שטחי בנייה עיליים (ברוטו):** **{fmt(ag.get('total_sqm'))} מ״ר** (שטחי דירות פלדלת: {fmt(ag.get('net_apartments_sqm'))} מ״ר · ליבה ושירות עילי: {fmt(ag.get('core_and_service_sqm'))} מ״ר)",
            f"- **סך שטחי בנייה תת-קרקעיים:** **{fmt(ug.get('total_sqm'))} מ״ר** ({ug.get('parking_spaces')} חניות · {ug.get('parking_ratio')})",
            f"- **סך שטח בנוי כולל בפרויקט (עילי + תת-קרקעי):** **{fmt(pds.get('total_built_area_sqm'))} מ״ר**",
            f"- **סך שטחי מרפסות גג:** **{fmt(rt.get('total_sqm'))} מ״ר** ({rt.get('count')} מרפסות גג" + (f" + {fmt(rt.get('garden_terraces_sqm'))} מ״ר גינות קרקע" if rt.get("garden_terraces_sqm") else "") + ")",
            f"- **סך שטחי מרפסות תלויות (זיזיות):** **{fmt(sb.get('total_sqm'))} מ״ר** ({sb.get('count')} מרפסות שמש זיזיות + {fmt(sb.get('service_balconies_sqm'))} מ״ר מרפסות שירות)",
            f"- **סך שטחי חזיתות החוץ:** **{fmt(fac.get('total_sqm'))} מ״ר** (גובה מבנה: {fmt(fac.get('building_height_m'))} מ׳ · זיגוג ופתחים: {fmt(fac.get('total_glazing_sqm'))} מ״ר [{fac.get('average_wwr_pct')}%] · אטום/חיפוי: {fmt(fac.get('total_opaque_sqm'))} מ״ר)",
            f"- **סך שטחי ריצוף דירות (נטו):** **{fmt(flr.get('total_apartments_flooring_sqm'))} מ״ר** (ריצוף פנים יבש: {fmt(flr.get('total_apartments_dry_sqm'))} מ״ר · ריצוף חדרים רטובים R10: {fmt(flr.get('total_apartments_wet_sqm'))} מ״ר)",
            f"- **סך שטחי ריצוף ציבורי (נטו):** **{fmt(flr.get('total_public_flooring_sqm'))} מ״ר** (לובי כניסה, מועדון דיירים/עגלות, מבואות קומתיות, חדרי מדרגות ומחסנים מרוצפים)",
            f"- **סך שטחי ריצוף מרפסות (נטו):** **{fmt(flr.get('total_balconies_flooring_sqm'))} מ״ר** (מרפסות שמש זיזיות, מרפסות שירות, מרפסות גג ומשטחי גן מרוצפים)",
            f"- **סה״כ שטחי ריצוף בפרויקט (קומות מלאות):** **{fmt(flr.get('grand_total_flooring_sqm'))} מ״ר**",
            "",
            "### א. חלוקת שטחי בנייה עיליים לפי קומות:",
            "| קומה | מפלס | יח״ד | שטח דירות | ליבה ושירות | סה״כ קומה | % מהעילי |",
            "| :--- | :--- | :---: | :---: | :---: | :---: | :---: |",
        ])
        for fl in ag.get("by_floor", []):
            ai_summary_lines.append(
                f"| **{fl.get('floor_label')}** | `{fl.get('elevation')}` | {fl.get('units_count')} | {fmt(fl.get('apartments_sqm'))} מ״ר | {fmt(fl.get('core_service_sqm'))} מ״ר | **{fmt(fl.get('total_floor_sqm'))} מ״ר** | {fl.get('pct_of_above_ground')}% |"
            )

        ai_summary_lines.extend([
            "",
            "### ב. חלוקת שטחי חזיתות לפי כיוונים:",
            "| חזית | כיוון | אורך × גובה | שטח ברוטו | % | זיגוג ופתחים | קירות וחיפוי |",
            "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |",
        ])
        for fd in fac.get("by_direction", []):
            ai_summary_lines.append(
                f"| **{fd.get('facade_name')}** | {fd.get('direction')} | {fmt(fd.get('length_m'))}×{fmt(fd.get('height_m'))} מ׳ | **{fmt(fd.get('gross_area_sqm'))} מ״ר** | {fd.get('pct_of_total')}% | {fmt(fd.get('glazing_area_sqm'))} מ״ר ({fd.get('wwr_pct')}%) | {fmt(fd.get('opaque_area_sqm'))} מ״ר |"
            )

        ai_summary_lines.extend([
            "",
            "### ג. חלוקת שטחי ריצוף נטו לפי קומות מלאות (דירות / ציבורי / מרפסות):",
            "| קומה | מפלס | יח״ד | ריצוף דירות (יבש + רטוב) | ריצוף ציבורי | ריצוף מרפסות | סה״כ ריצוף בקומה | הערות |",
            "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |",
        ])
        for fl_r in flr.get("by_floor", []):
            ai_summary_lines.append(
                f"| **{fl_r.get('floor_label')}** | `{fl_r.get('elevation')}` | {fl_r.get('units_count')} | **{fmt(fl_r.get('apartments_flooring_sqm'))} מ״ר** ({fmt(fl_r.get('apartments_dry_sqm'))}+{fmt(fl_r.get('apartments_wet_sqm'))}) | **{fmt(fl_r.get('public_flooring_sqm'))} מ״ר** | **{fmt(fl_r.get('balconies_flooring_sqm'))} מ״ר** | **{fmt(fl_r.get('total_floor_flooring_sqm'))} מ״ר** | {fl_r.get('notes', '')} |"
            )
        ai_summary_lines.append(
            f"| **סה״כ ריצוף בפרויקט** | **כל הקומות** | **{pds.get('apartments_count')} יח״ד** | **{fmt(flr.get('total_apartments_flooring_sqm'))} מ״ר** ({fmt(flr.get('total_apartments_dry_sqm'))}+{fmt(flr.get('total_apartments_wet_sqm'))}) | **{fmt(flr.get('total_public_flooring_sqm'))} מ״ר** | **{fmt(flr.get('total_balconies_flooring_sqm'))} מ״ר** | **{fmt(flr.get('grand_total_flooring_sqm'))} מ״ר** | **סך ריצוף דירות + ציבורי + מרפסות** |"
        )

        ai_summary_lines.extend([
            "",
            "## 3. מסמך סיכום הערות והצעות אופרטיביות לשיפור:",
        ])
        for c_note in sdoc.get("critical_notes_summary", []):
            ai_summary_lines.append(f"- {c_note}")

        ai_summary_lines.append("\n### הצעות לשיפור התכנון:")
        for idx, prop in enumerate(sdoc.get("improvement_proposals", []), 1):
            ai_summary_lines.append(
                f"{idx}. **[{prop.get('priority')}] {prop.get('target')}** — *הבעיה:* {prop.get('issue')} | *הצעה לשיפור:* **{prop.get('proposal')}** (*השפעה:* {prop.get('impact')})"
            )

        if fails:
            ai_summary_lines.append("\n## 4. ליקויים קריטיים (FAIL):")
            for f in fails:
                ai_summary_lines.append(f"- [{f.get('id')}] {f.get('title')} ({f.get('room_name')}): נמדד `{f.get('measured')}` מול נדרש `{f.get('benchmark')}`. פתרון: {f.get('recommendation')}")

        if warns:
            ai_summary_lines.append("\n## 5. התראות איכות וארגונומיה בולטות (WARN):")
            for w in warns[:8]:
                ai_summary_lines.append(f"- [{w.get('id')}] {w.get('title')} ({w.get('room_name')}): נמדד `{w.get('measured')}` מול בנצ'מרק `{w.get('benchmark')}`. המלצה: {w.get('recommendation')}")

        target_ai_sum_md = os.path.join(folder_path, f"{pid}_ai_summary.md")
        if write_if_changed(target_ai_sum_md, "\n".join(ai_summary_lines), manifest):
            updated_files.append(f"{meta['folder']}/{pid}_ai_summary.md")
        else:
            skipped_count += 1

        ai_summary_json = {
            "project_id": pid,
            "project_name": analysis_data.get("project_name"),
            "score": analysis_data.get("overall_score"),
            "metrics": analysis_data.get("metrics", []),
            "counts": {"pass": len(passes), "warn": len(warns), "fail": len(fails), "total": len(notes)},
            "project_data_summary": pds,
            "failures": fails,
            "top_warnings": warns[:8]
        }
        target_ai_sum_json = os.path.join(folder_path, f"{pid}_ai_summary.json")
        if write_if_changed(target_ai_sum_json, json.dumps(ai_summary_json, indent=2, ensure_ascii=False), manifest):
            updated_files.append(f"{meta['folder']}/{pid}_ai_summary.json")
        else:
            skipped_count += 1

        # C. Copy Full Reports AND Standalone Summary & Areas Reports from reports/
        prefix = meta["report_prefix"]
        report_mappings = [
            (f"{prefix}_architectural_quality_report.md", f"{pid}_architectural_report.md"),
            (f"{prefix}_architectural_quality_analysis.html", f"{prefix}_architectural_quality_analysis.html"),
            (f"{prefix}_architectural_quality_analysis.pdf", f"{prefix}_architectural_quality_analysis.pdf"),
            (f"{prefix}_summary_and_areas_report.md", f"{pid}_summary_and_areas_report.md"),
            (f"{prefix}_summary_and_areas_report.html", f"{pid}_summary_and_areas_report.html"),
            (f"{prefix}_summary_and_areas_report.pdf", f"{pid}_summary_and_areas_report.pdf"),
        ]
        for src_name, dst_name in report_mappings:
            src_file = os.path.join(reports_dir, src_name)
            if os.path.exists(src_file):
                tgt_file = os.path.join(folder_path, dst_name)
                if copy_if_changed(src_file, tgt_file, manifest):
                    updated_files.append(f"{meta['folder']}/{dst_name}")
                else:
                    skipped_count += 1

    # 4. OKF Rules Knowledge Base
    okf_dir = os.path.join(TARGET_DIR, "00_תקנים_וחוקי_תכנון_OKF")
    os.makedirs(okf_dir, exist_ok=True)
    rules_data = load_okf_rules(os.path.join(BASE_DIR, "okf_rules"))
    rules_json_str = json.dumps({"total_rules": len(rules_data), "rules": rules_data}, indent=2, ensure_ascii=False)
    target_rules_json = os.path.join(okf_dir, "okf_rules_catalog.json")
    if write_if_changed(target_rules_json, rules_json_str, manifest):
        updated_files.append("00_תקנים_וחוקי_תכנון_OKF/okf_rules_catalog.json")
    else:
        skipped_count += 1

    # 5. API SDK & Schemas
    tools_dir = os.path.join(TARGET_DIR, "00_כלי_חיבור_וסכמות_API")
    os.makedirs(tools_dir, exist_ok=True)
    for src_fn in ["archknow_client.py", "openapi.json", "AI_API_GUIDE.md"]:
        s_path = os.path.join(BASE_DIR, src_fn)
        if os.path.exists(s_path):
            t_path = os.path.join(tools_dir, src_fn)
            if copy_if_changed(s_path, t_path, manifest):
                updated_files.append(f"00_כלי_חיבור_וסכמות_API/{src_fn}")
            else:
                skipped_count += 1

    # 6. Centralize & catalog 3D BIM models in G:\Shared drives\שליטה ובקרה\מודלים פרויקטים
    try:
        from sync_3d_models import run_centralization, CENTRAL_MODELS_ROOT
        run_centralization()
        cat_src = os.path.join(CENTRAL_MODELS_ROOT, "00_models_catalog.json")
        if os.path.exists(cat_src):
            cat_dst = os.path.join(TARGET_DIR, "00_models_catalog.json")
            if copy_if_changed(cat_src, cat_dst, manifest):
                updated_files.append("00_models_catalog.json")
    except Exception as e:
        print(f"[sync] Warning during 3D models centralization: {e}", file=sys.stderr)

    save_manifest(manifest)

    # 7. Also sync to My Drive archknow mirror
    my_drive_synced = sync_my_drive_mirror()
    updated_files.extend(my_drive_synced)

    return {
        "status": "success",
        "target_directory": TARGET_DIR,
        "my_drive_directory": MY_DRIVE_ARCHKNOW_DIR,
        "updated_files_count": len(updated_files),
        "skipped_unchanged_count": skipped_count,
        "updated_files": updated_files
    }


def watch_and_sync(interval_seconds: int = 10):
    """Watches the project source files and syncs whenever changes occur."""
    print(f"[sync] Starting watcher on '{BASE_DIR}' -> '{TARGET_DIR}' (Interval: {interval_seconds}s)...")
    while True:
        try:
            res = sync_all()
            if res.get("updated_files_count", 0) > 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Synced {res['updated_files_count']} updated file(s) to Google Drive!")
        except Exception as e:
            print(f"[sync] Error in sync loop: {e}", file=sys.stderr)
        time.sleep(interval_seconds)


if __name__ == "__main__":
    if "--watch" in sys.argv:
        watch_and_sync()
    else:
        res = sync_all(force="--force" in sys.argv)
        print(f"Sync complete to: {res['target_directory']}")
        print(f"Updated files: {res['updated_files_count']}")
        print(f"Unchanged files: {res['skipped_unchanged_count']}")
        for f in res.get("updated_files", [])[:60]:
            print(f" + {f}")
        if len(res.get("updated_files", [])) > 60:
            print(f" ... and {len(res['updated_files']) - 60} more files.")
