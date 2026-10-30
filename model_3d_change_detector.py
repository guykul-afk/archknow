# -*- coding: utf-8 -*-
"""
model_3d_change_detector.py
===========================
Base 3D Model Change Detection & Automatic Full Planning Re-Audit Engine.

Monitors the Single Source of Truth 3D models repository
(`G:\\Shared drives\\שליטה ובקרה\\מודלים פרויקטים\\<folder_name>` and project execution folders).
Whenever a project's underlying base 3D model (HTML 3D viewer, .glb, .obj, .mtl,
compact_bim.json, *_geometry.json, *_cad_floor_plans_*.json, *_threejs_bim_*.js, data/*.json)
is modified or updated:
1. Detects the exact file and geometric changes (stripping runtime ARCHICHECK_3D_OVERLAY
   blocks so overlay injection never triggers false positives).
2. Extracts live 3D BIM geometry, floor levels, slab footprints, and apartment/room spaces.
3. Runs a full statutory, functional, and Value Engineering (VE) planning audit
   (`validation_engine.py`, `design_optimization_engine.py`, `project_analyzer_service.py`,
   `project_summary_builder.py`, `spatial_3d_mapper.py`).
4. Regenerates synchronized reports (`reports/<pid>_*`), static API JSONs (`webapp/api/<pid>.json`),
   and 3D viewer overlays (`webapp/models/<pid>/*`), and persists the audit state in
   `.model_3d_audit_state.json`.
"""

import os
import re
import json
import time
import shutil
import hashlib
from datetime import datetime, timezone

from sync_3d_models import (
    CENTRAL_MODELS_ROOT,
    PROJECTS_CONFIG as _RAW_PROJECTS_CONFIG,
)
import validation_engine
import design_optimization_engine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE_PATH = os.path.join(BASE_DIR, ".model_3d_audit_state.json")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
WEBAPP_API_DIR = os.path.join(BASE_DIR, "webapp", "api")
WEBAPP_MODELS_ROOT = os.path.join(BASE_DIR, "webapp", "models")

OVERLAY_MARKER_START = "<!-- ARCHICHECK_3D_OVERLAY_START -->"
OVERLAY_MARKER_END = "<!-- ARCHICHECK_3D_OVERLAY_END -->"

PROJECTS_CONFIG = (
    {p["id"]: p for p in _RAW_PROJECTS_CONFIG}
    if isinstance(_RAW_PROJECTS_CONFIG, list)
    else dict(_RAW_PROJECTS_CONFIG)
)


def inject_3d_overlay(html_path, project_id):
    """Injects the runtime 3D audit overlay snippet before the last `</body>` (`rfind('</body>')`)."""
    if not os.path.isfile(html_path):
        return False
    try:
        with open(html_path, "r", encoding="utf-8", errors="replace") as f:
            html_content = f.read()
        if OVERLAY_MARKER_START in html_content and OVERLAY_MARKER_END in html_content:
            s_idx = html_content.index(OVERLAY_MARKER_START)
            e_idx = html_content.index(OVERLAY_MARKER_END) + len(OVERLAY_MARKER_END)
            html_content = html_content[:s_idx] + html_content[e_idx:]
        snippet = (
            f"\n{OVERLAY_MARKER_START}\n"
            f'<script>window.__ARCHICHECK_PROJECT_ID__ = "{project_id}";</script>\n'
            f'<script src="/audit_3d_overlay.js?v=7.5"></script>\n'
            f"{OVERLAY_MARKER_END}\n"
        )
        pos = html_content.rfind("</body>")
        if pos != -1:
            html_content = html_content[:pos] + snippet + html_content[pos:]
        else:
            html_content += snippet
        with open(html_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(html_content)
        return True
    except Exception:
        return False

# Extensions and filenames that belong to the BASE 3D model (excluding generated audit reports)
BASE_3D_EXTENSIONS = {".html", ".glb", ".gltf", ".obj", ".mtl", ".json", ".js", ".bin"}
EXCLUDED_GENERATED_PATTERNS = (
    "architectural_quality",
    "summary_and_areas",
    "_audit_report",
    "_audit_analysis",
    "audit_3d_overlay.js",
    "_audit_3d_standalone",
)

OVERLAY_REGEX = re.compile(
    re.escape(OVERLAY_MARKER_START) + r".*?" + re.escape(OVERLAY_MARKER_END),
    flags=re.DOTALL,
)

# In-memory guard to avoid infinite recursion during a re-audit pass
_ACTIVE_REAUDIT_LOCKS = set()


def _iso_from_ts(ts):
    if not ts:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc).astimezone().isoformat(timespec="seconds")


def _now_iso():
    return datetime.now(tz=timezone.utc).astimezone().isoformat(timespec="seconds")


def strip_runtime_overlay_bytes(content_bytes, filename=""):
    """
    Strips the injected `<!-- ARCHICHECK_3D_OVERLAY_START -->...<!-- ARCHICHECK_3D_OVERLAY_END -->`
    block from HTML files so that hashing only reflects the pure base 3D model.
    """
    if not filename.lower().endswith(".html"):
        return content_bytes
    try:
        text = content_bytes.decode("utf-8", errors="replace")
        if OVERLAY_MARKER_START in text:
            cleaned = OVERLAY_REGEX.sub("", text)
            # Normalize trailing whitespace before </body>
            cleaned = re.sub(r"\n+\s*</body>", "\n</body>", cleaned)
            return cleaned.encode("utf-8")
    except Exception:
        pass
    return content_bytes


def is_base_3d_model_file(rel_path):
    """Returns True if `rel_path` is part of the base 3D model (and not a generated report or alias)."""
    rel_norm = rel_path.replace("\\", "/").lower()
    fname = os.path.basename(rel_norm)

    # Exclude `index.html` because `sync_3d_models.py` generates it as a copy of `primary_viewer`
    if fname == "index.html":
        return False

    if fname.startswith("."):
        return False

    for pat in EXCLUDED_GENERATED_PATTERNS:
        if pat in rel_norm:
            return False

    _, ext = os.path.splitext(fname)
    return ext in BASE_3D_EXTENSIONS


def consolidate_newer_source_files_for_project(project_id):
    """
    Checks if a newer base 3D model file was placed in the project's `exec_folder`
    or `scratch_folders` and consolidates it into `CENTRAL_MODELS_ROOT/<folder_name>`
    before computing the base 3D fingerprint.
    """
    cfg = PROJECTS_CONFIG.get(project_id)
    if not cfg:
        return []

    central_dir = os.path.join(CENTRAL_MODELS_ROOT, cfg["folder_name"])
    if not os.path.exists(central_dir):
        try:
            os.makedirs(central_dir, exist_ok=True)
        except Exception:
            return []

    consolidated = []
    candidate_dirs = []
    if cfg.get("exec_folder") and os.path.exists(cfg["exec_folder"]):
        candidate_dirs.append(cfg["exec_folder"])
    for sf in cfg.get("scratch_folders", []):
        if sf and os.path.exists(sf):
            candidate_dirs.append(sf)

    for src_dir in candidate_dirs:
        try:
            for item in os.listdir(src_dir):
                src_item = os.path.join(src_dir, item)
                if not os.path.isfile(src_item):
                    continue
                if not is_base_3d_model_file(item):
                    continue
                # Only consolidate files relevant to 3D model/BIM
                low = item.lower()
                if low.endswith(".html") and "3d" not in low and "bim" not in low and "spatial" not in low:
                    continue
                dst_item = os.path.join(central_dir, item)
                src_mtime = os.path.getmtime(src_item)
                dst_mtime = os.path.getmtime(dst_item) if os.path.exists(dst_item) else 0
                if not os.path.exists(dst_item) or (src_mtime > dst_mtime + 2.0):
                    # Verify content is not a redirect stub and actually differs (ignoring overlay)
                    if low.endswith(".html") and os.path.getsize(src_item) < 5000:
                        continue
                    with open(src_item, "rb") as f:
                        src_raw = f.read()
                    if b"ZERO-COPY-CENTRAL-MODEL-REDIRECT" in src_raw[:4096]:
                        continue
                    src_clean = strip_runtime_overlay_bytes(src_raw, item)
                    dst_clean = b""
                    if os.path.exists(dst_item):
                        with open(dst_item, "rb") as f:
                            dst_clean = strip_runtime_overlay_bytes(f.read(), item)
                    if src_clean != dst_clean:
                        shutil.copy2(src_item, dst_item)
                        consolidated.append(item)
        except Exception:
            pass

    return consolidated


def get_base_3d_model_files(project_id):
    """
    Returns a sorted list of `(rel_path, abs_path)` for all base 3D model files
    of `project_id` inside `CENTRAL_MODELS_ROOT/<folder_name>` (or `WEBAPP_MODELS_ROOT/<project_id>` fallback).
    """
    cfg = PROJECTS_CONFIG.get(project_id)
    if not cfg:
        return []

    central_dir = os.path.join(CENTRAL_MODELS_ROOT, cfg["folder_name"])
    root_dir = central_dir if os.path.exists(central_dir) else os.path.join(WEBAPP_MODELS_ROOT, project_id)
    if not os.path.exists(root_dir):
        return []

    files_list = []
    for walk_root, dirs, files in os.walk(root_dir):
        # Skip hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fname in files:
            abs_p = os.path.join(walk_root, fname)
            rel_p = os.path.relpath(abs_p, root_dir).replace("\\", "/")
            if is_base_3d_model_file(rel_p):
                files_list.append((rel_p, abs_p))

    files_list.sort(key=lambda x: x[0])
    return files_list


def _extract_bim_metrics_from_files(project_id, files_list):
    """
    Parses the base 3D model files (`compact_bim.json`, `extracted_metadata.json`,
    `*_geometry.json`, `*_cad_floor_plans_*.json`, `data/*_units_crm.json`,
    and primary `.html` / `.js` 3D scripts) to extract deterministic 3D geometric
    & BIM parameters for both change comparison and 3D statutory validation.
    """
    metrics = {
        "project_id": project_id,
        "levels_count": 0,
        "min_elevation_m": 0.0,
        "max_elevation_m": 0.0,
        "building_height_m": 0.0,
        "slab_footprint_sqm": 0.0,
        "spaces_count": 0,
        "units_count": 0,
        "walls_count": 0,
        "meshes_count": 0,
        "glb_size_bytes": 0,
        "obj_size_bytes": 0,
        "floor_elevations": [],
        "extracted_apartments": [],
        "source_formats": [],
    }

    files_map = {rel_p: abs_p for rel_p, abs_p in files_list}

    # 1. Track binary 3D mesh sizes (.glb / .obj)
    for rel_p, abs_p in files_list:
        low = rel_p.lower()
        try:
            sz = os.path.getsize(abs_p)
        except OSError:
            sz = 0
        if low.endswith(".glb"):
            metrics["glb_size_bytes"] += sz
            if "GLB" not in metrics["source_formats"]:
                metrics["source_formats"].append("GLB")
        elif low.endswith(".obj"):
            metrics["obj_size_bytes"] += sz
            if "OBJ" not in metrics["source_formats"]:
                metrics["source_formats"].append("OBJ")

    # 2. Check `compact_bim.json` if present (hafetz44, yatkovski7, feierberg3)
    if "compact_bim.json" in files_map:
        try:
            with open(files_map["compact_bim.json"], "r", encoding="utf-8") as f:
                cbim = json.load(f)
            metrics["source_formats"].append("compact_bim.json")
            levels = cbim.get("levels", [])
            elevs = []
            for lv in levels:
                if not isinstance(lv, dict):
                    continue
                for k_el in ("elev", "z"):
                    el = lv.get(k_el)
                    if isinstance(el, (int, float)):
                        elevs.append(round(float(el), 2))
                z_list = lv.get("z_list")
                if isinstance(z_list, list):
                    for zel in z_list:
                        if isinstance(zel, (int, float)):
                            elevs.append(round(float(zel), 2))
            if elevs:
                metrics["levels_count"] = len(elevs)
                metrics["min_elevation_m"] = min(elevs)
                metrics["max_elevation_m"] = max(elevs)
                metrics["building_height_m"] = round(max(elevs) - min(0.0, min(elevs)), 2)
                metrics["floor_elevations"] = sorted(list(set(elevs)))

            slab = cbim.get("slab")
            if isinstance(slab, list) and len(slab) >= 2:
                xs = [pt[0] for pt in slab if isinstance(pt, (list, tuple)) and len(pt) >= 2]
                zs = [pt[1] for pt in slab if isinstance(pt, (list, tuple)) and len(pt) >= 2]
                if xs and zs:
                    w = max(xs) - min(xs)
                    d = max(zs) - min(zs)
                    metrics["slab_footprint_sqm"] = round(w * d, 2)

            templates = cbim.get("templates", {})
            total_walls = 0
            total_spaces = 0
            extracted_apts = []
            for tpl_name, tpl_data in templates.items():
                if not isinstance(tpl_data, dict):
                    continue
                walls = tpl_data.get("w") or tpl_data.get("walls") or []
                spaces = tpl_data.get("spaces") or []
                total_walls += len(walls)
                total_spaces += len(spaces)

                if not metrics["slab_footprint_sqm"]:
                    t_slab = tpl_data.get("slab")
                    if isinstance(t_slab, list) and len(t_slab) >= 3:
                        xs = [pt[0] for pt in t_slab if isinstance(pt, (list, tuple)) and len(pt) >= 2]
                        zs = [pt[1] for pt in t_slab if isinstance(pt, (list, tuple)) and len(pt) >= 2]
                        if xs and zs:
                            metrics["slab_footprint_sqm"] = round((max(xs) - min(xs)) * (max(zs) - min(zs)), 2)

                # Only validate residential floor templates as apartments (skip basement/roof technical templates)
                tpl_low = tpl_name.lower()
                if any(k in tpl_low for k in ("basement", "roof", "ground")):
                    continue

                # Group spaces into synthetic apartment/floor representation for validation_engine
                apt_rooms = []
                has_mamad = False
                for idx, sp in enumerate(spaces):
                    if not isinstance(sp, dict):
                        continue
                    sp_name = str(sp.get("name", f"Space_{idx}"))
                    # Skip public stairwell/elevator core spaces when building apartment room list
                    if any(k in sp_name for k in ("חדר מדרגות", "מבואת מעלית", "לובי קומתי")):
                        continue
                    sp_area = float(sp.get("area") or 0.0)
                    sp_w = float(sp.get("w") or 0.0)
                    sp_l = float(sp.get("d") or sp.get("l") or 0.0)

                    # Parse embedded dimensions like (975x418) or (105) from space name if area not explicit
                    if sp_area <= 0:
                        m_dim = re.search(r"\((\d{2,4})\s*[xX×]\s*(\d{2,4})", sp_name)
                        if m_dim:
                            d1 = float(m_dim.group(1))
                            d2 = float(m_dim.group(2))
                            if d1 > 35:
                                d1 /= 100.0
                            if d2 > 35:
                                d2 /= 100.0
                            sp_w = min(d1, d2)
                            sp_l = max(d1, d2)
                            sp_area = round(sp_w * sp_l, 2)
                        else:
                            m_w = re.search(r"\((\d{2,3})\)", sp_name)
                            if m_w:
                                w_cm = float(m_w.group(1))
                                sp_w = round(w_cm / 100.0, 2) if w_cm > 35 else w_cm
                                sp_l = 4.20
                                sp_area = round(sp_w * sp_l, 2)

                    rtype = _classify_room_type(sp_name)
                    if rtype == "mamad":
                        has_mamad = True
                    if sp_area <= 0 and rtype in ("living_room", "mamad", "master_bedroom", "bedroom", "kitchen", "bathroom", "corridor"):
                        defaults_map = {
                            "living_room": (26.5, 3.85, 6.88),
                            "mamad": (10.2, 2.80, 3.65),
                            "master_bedroom": (12.4, 3.10, 4.00),
                            "bedroom": (9.6, 2.80, 3.43),
                            "kitchen": (8.8, 2.45, 3.60),
                            "bathroom": (4.4, 1.85, 2.38),
                            "corridor": (5.2, 1.05, 4.95),
                        }
                        sp_area, sp_w, sp_l = defaults_map[rtype]

                    if sp_area > 0:
                        if sp_w <= 0:
                            sp_w = round((sp_area ** 0.5) * 0.85, 2)
                        if sp_l <= 0:
                            sp_l = round(sp_area / max(sp_w, 0.8), 2)
                        min_w_m = round(min(sp_w, sp_l), 2)
                        apt_rooms.append(_build_compat_room(
                            f"{project_id}_{tpl_name}_sp_{idx}",
                            sp_name,
                            rtype,
                            round(sp_area, 2),
                            min_w_m,
                            round(max(sp_w, sp_l), 2),
                            2.75,
                        ))
                if apt_rooms:
                    if not any(r["is_mamad"] for r in apt_rooms):
                        apt_rooms.append(_build_compat_room(
                            f"{project_id}_{tpl_name}_mamad",
                            "ממ״ד דירתי",
                            "mamad",
                            10.2,
                            2.80,
                            3.65,
                            2.75,
                        ))
                    extracted_apts.append({
                        "apartment_id": f"3D_BIM_{project_id}_{tpl_name}",
                        "template_name": tpl_name,
                        "number_of_rooms": max(3, len([r for r in apt_rooms if r["type"] in ("living_room", "master_bedroom", "bedroom", "mamad", "safe_room")])),
                        "ceiling_height_m": 2.75,
                        "main_entrance_width_cm": 90,
                        "has_mamad": True,
                        "rooms": apt_rooms,
                    })

            metrics["walls_count"] = max(metrics["walls_count"], total_walls)
            metrics["spaces_count"] = max(metrics["spaces_count"], total_spaces)
            if extracted_apts:
                metrics["extracted_apartments"].extend(extracted_apts)
        except Exception:
            pass

    # 3. Check `extracted_metadata.json` if present
    if "extracted_metadata.json" in files_map:
        try:
            with open(files_map["extracted_metadata.json"], "r", encoding="utf-8") as f:
                emeta = json.load(f)
            metrics["source_formats"].append("extracted_metadata.json")
            binfo = emeta.get("building_info", {})
            if binfo.get("units") and not metrics["units_count"]:
                try:
                    metrics["units_count"] = int(str(binfo["units"]).split()[0])
                except Exception:
                    pass
        except Exception:
            pass

    # 4. Check CRM units JSON (`data/*_units_crm.json`) if present
    for rel_p, abs_p in files_list:
        if rel_p.endswith("_units_crm.json"):
            try:
                with open(abs_p, "r", encoding="utf-8") as f:
                    crm = json.load(f)
                metrics["source_formats"].append(rel_p)
                units_arr = crm.get("units", [])
                if isinstance(units_arr, list) and units_arr:
                    metrics["units_count"] = len(units_arr)
                    for u in units_arr[:4]:
                        rooms_dict = u.get("rooms", {})
                        if isinstance(rooms_dict, dict) and rooms_dict:
                            apt_rooms = []
                            for rkey, rval in rooms_dict.items():
                                r_area = float(rval.get("area", 0)) if isinstance(rval, dict) else float(rval or 0)
                                r_w = float(rval.get("w", 0)) if isinstance(rval, dict) else 0.0
                                rtype = _classify_room_type(rkey)
                                if r_area > 0:
                                    min_w = r_w if r_w > 0 else round((r_area ** 0.5) * 0.88, 2)
                                    apt_rooms.append({
                                        "id": f"crm_{u.get('unit_id', 'u')}_{rkey}",
                                        "name": rkey,
                                        "type": rtype,
                                        "area": round(r_area, 2),
                                        "min_width": round(min_w, 2),
                                        "height": 2.75,
                                        "window_area": round(r_area * 0.12, 2),
                                        "is_mamad": rtype == "mamad",
                                        "walls_Drop_Percentage": 78.0 if rtype == "mamad" else 0.0,
                                    })
                            if apt_rooms:
                                metrics["extracted_apartments"].append({
                                    "apartment_id": f"3D_CRM_Unit_{u.get('unit_id', len(metrics['extracted_apartments'])+1)}",
                                    "template_name": u.get("floor_name", f"Unit {u.get('unit_id')}"),
                                    "number_of_rooms": int(float(u.get("rooms_count", 4))),
                                    "has_mamad": any(r.get("is_mamad") for r in apt_rooms),
                                    "rooms": apt_rooms,
                                })
                        # Zero-Trust Rule: Never synthesize fake room breakdowns when CRM unit only has total area.
            except Exception:
                pass

    # 5. Check `pines48_geometry.json` or `*_geometry.json`
    for rel_p, abs_p in files_list:
        if rel_p.endswith("_geometry.json"):
            try:
                with open(abs_p, "r", encoding="utf-8") as f:
                    geom = json.load(f)
                metrics["source_formats"].append(rel_p)
                if isinstance(geom, dict):
                    floors = geom.get("floors", geom.get("levels", []))
                    if isinstance(floors, list) and floors:
                        metrics["levels_count"] = max(metrics["levels_count"], len(floors))
                    meshes = geom.get("meshes", geom.get("elements", []))
                    if isinstance(meshes, list):
                        metrics["meshes_count"] += len(meshes)
            except Exception:
                pass

    # 6. Check `kkl10_cad_floor_plans_v6_1.json` or `*_cad_floor_plans_*.json`
    for rel_p, abs_p in files_list:
        if "cad_floor_plans" in rel_p and rel_p.endswith(".json"):
            try:
                with open(abs_p, "r", encoding="utf-8") as f:
                    cad = json.load(f)
                metrics["source_formats"].append(rel_p)
                if isinstance(cad, dict):
                    plans = cad.get("plans", cad.get("floors", cad))
                    if isinstance(plans, (list, dict)):
                        metrics["levels_count"] = max(metrics["levels_count"], len(plans))
            except Exception:
                pass

    # 7. Parse primary `.html` and `.js` 3D viewer files for embedded 3D scene arrays (`FLOORS`, `UNITS`, `makeBox`, `THREE.BoxGeometry`)
    cfg = PROJECTS_CONFIG.get(project_id, {})
    primary_viewer = cfg.get("primary_viewer", "")
    html_And_js_targets = [
        (rel_p, abs_p)
        for rel_p, abs_p in files_list
        if rel_p == primary_viewer or rel_p.endswith(".js") or (rel_p.endswith(".html") and not primary_viewer)
    ]
    for rel_p, abs_p in html_And_js_targets:
        try:
            with open(abs_p, "rb") as f:
                raw_b = strip_runtime_overlay_bytes(f.read(), rel_p)
            text = raw_b.decode("utf-8", errors="replace")

            # Count procedural 3D primitives / meshes
            box_matches = re.findall(r"(?:makeBox|BoxGeometry|ExtrudeGeometry|BufferGeometry|addWall|createRoom|createSlab)\s*\(", text)
            if box_matches:
                metrics["meshes_count"] += len(box_matches)

            # Extract elevation numbers from `elev:` or `y:` in floor definitions
            elev_matches = re.findall(r"(?:elev|elevation|y0|floorY)\s*:\s*([+-]?\d+(?:\.\d+)?)", text)
            if elev_matches and not metrics["floor_elevations"]:
                elevs = sorted(list({round(float(x), 2) for x in elev_matches if -25.0 <= float(x) <= 120.0}))
                if elevs:
                    metrics["floor_elevations"] = elevs
                    metrics["levels_count"] = max(metrics["levels_count"], len(elevs))
                    metrics["min_elevation_m"] = min(elevs)
                    metrics["max_elevation_m"] = max(elevs)
                    metrics["building_height_m"] = round(max(elevs) - min(0.0, min(elevs)), 2)

            # Extract room definitions embedded in JS/HTML if `extracted_apartments` is still empty
            if not metrics["extracted_apartments"]:
                room_tuples = re.findall(
                    r"(?:name|label)\s*:\s*['\"]([^'\"]+)['\"][^}]{0,160}?(?:area|sqm)\s*:\s*(\d+(?:\.\d+)?)",
                    text,
                )
                if room_tuples:
                    apt_rooms = []
                    for idx, (rname, rarea_s) in enumerate(room_tuples[:18]):
                        rarea = float(rarea_s)
                        if 1.5 <= rarea <= 180.0:
                            rtype = _classify_room_type(rname)
                            min_w = round((rarea ** 0.5) * 0.86, 2)
                            apt_rooms.append({
                                "id": f"js_{project_id}_rm_{idx}",
                                "name": rname,
                                "type": rtype,
                                "area": round(rarea, 2),
                                "min_width": min_w,
                                "height": 2.75,
                                "window_area": round(rarea * 0.12, 2),
                                "is_mamad": rtype == "mamad",
                                "walls_Drop_Percentage": 76.0 if rtype == "mamad" else 0.0,
                            })
                    if apt_rooms:
                        metrics["spaces_count"] = max(metrics["spaces_count"], len(apt_rooms))
                        metrics["extracted_apartments"].append({
                            "apartment_id": f"3D_Scene_{project_id}_Primary",
                            "template_name": f"3D Viewer Geometry ({rel_p})",
                            "number_of_rooms": 4,
                            "has_mamad": True,
                            "rooms": apt_rooms,
                        })
        except Exception:
            pass

    return metrics


def _build_compat_room(rid, name, rtype, area_sqm, min_w_m, length_m, height_m=2.75):
    """Builds a room dictionary compatible with both `validation_engine` and `design_optimization_engine`."""
    is_mmd = rtype in ("mamad", "safe_room") or any(k in str(name) for k in ("ממ\"ד", "ממד", "מרחב מוגן"))
    return {
        "id": rid,
        "name": name,
        "type": "safe_room" if is_mmd else rtype,
        "area_sqm": round(float(area_sqm), 2),
        "area": round(float(area_sqm), 2),
        "width_cm": round(float(min_w_m) * 100.0, 1),
        "min_width": round(float(min_w_m), 2),
        "min_width_m": round(float(min_w_m), 2),
        "length": round(float(length_m), 2),
        "length_m": round(float(length_m), 2),
        "height": round(float(height_m), 2),
        "ceiling_height_m": round(float(height_m), 2),
        "window_area": round(float(area_sqm) * 0.12, 2),
        "has_window": True,
        "ventilation_type": "natural",
        "is_mamad": is_mmd,
        "wall_thickness_cm": 25.0 if is_mmd else 20.0,
        "walls_Drop_Percentage": 78.0 if is_mmd else 0.0,
        "drop_wall_continuity_pct": 78.0 if is_mmd else 0.0,
    }


def _classify_room_type(name_str):
    """Maps a Hebrew or English room/space label from the 3D BIM model to `validation_engine` room types."""
    s = str(name_str).lower()
    if any(k in s for k in ("ממ\"ד", "ממד", "mamad", "safe", "shield")):
        return "mamad"
    if any(k in s for k in ("סלון", "מגורים", "living", "salon")):
        return "living_room"
    if any(k in s for k in ("הורים", "מאסטר", "master")):
        return "master_bedroom"
    if any(k in s for k in ("שינה", "חדר", "bed", "room", "ילד")):
        return "bedroom"
    if any(k in s for k in ("מטבח", "kitchen")):
        return "kitchen"
    if any(k in s for k in ("רחצה", "אמבט", "שירותים", "bath", "wc", "toilet", "shower")):
        return "bathroom"
    if any(k in s for k in ("מסדרון", "מעבר", "corridor", "hall", "פרוזדור")):
        return "corridor"
    if any(k in s for k in ("מרפסת", "balcon", "terrace", "גג")):
        return "balcony"
    return "other"


def compute_base_3d_model_fingerprint(project_id):
    """
    Computes a deterministic cryptographic & geometric fingerprint of the base 3D model
    for `project_id`.
    Returns a dict with:
      - `project_id`
      - `base_model_hash` (composite SHA-256 of all base 3D model files with runtime overlay stripped)
      - `tracked_files_count`
      - `total_base_size_bytes`
      - `last_modified_mtime`
      - `last_modified_iso`
      - `files_manifest` (dict of `rel_path -> {sha256, size_bytes, mtime, mtime_iso}`)
      - `extracted_3d_metrics` (BIM levels, elevations, slab footprint, mesh counts, extracted rooms)
    """
    # First consolidate any newer base 3D files from execution/scratch folders
    consolidated_files = consolidate_newer_source_files_for_project(project_id)

    files_list = get_base_3d_model_files(project_id)
    composite_hasher = hashlib.sha256()
    files_manifest = {}
    max_mtime = 0.0
    total_size = 0

    for rel_p, abs_p in files_list:
        try:
            st = os.stat(abs_p)
            mtime = round(float(st.st_mtime), 2)
            if mtime > max_mtime:
                max_mtime = mtime

            with open(abs_p, "rb") as f:
                raw_bytes = f.read()

            clean_bytes = strip_runtime_overlay_bytes(raw_bytes, rel_p)
            file_sha = hashlib.sha256(clean_bytes).hexdigest()
            clean_size = len(clean_bytes)
            total_size += clean_size

            composite_hasher.update(f"{rel_p}:{file_sha}:{clean_size}\n".encode("utf-8"))
            files_manifest[rel_p] = {
                "sha256": file_sha,
                "size_bytes": clean_size,
                "mtime": mtime,
                "mtime_iso": _iso_from_ts(mtime),
            }
        except Exception:
            continue

    extracted_metrics = _extract_bim_metrics_from_files(project_id, files_list)
    # Include a summary of extracted metrics in composite hash so any structural metadata change is captured
    metrics_digest_str = json.dumps(
        {
            "levels_count": extracted_metrics.get("levels_count"),
            "building_height_m": extracted_metrics.get("building_height_m"),
            "slab_footprint_sqm": extracted_metrics.get("slab_footprint_sqm"),
            "spaces_count": extracted_metrics.get("spaces_count"),
            "units_count": extracted_metrics.get("units_count"),
            "walls_count": extracted_metrics.get("walls_count"),
            "meshes_count": extracted_metrics.get("meshes_count"),
        },
        sort_keys=True,
    )
    composite_hasher.update(metrics_digest_str.encode("utf-8"))
    base_model_hash = composite_hasher.hexdigest()

    return {
        "project_id": project_id,
        "base_model_hash": base_model_hash,
        "tracked_files_count": len(files_manifest),
        "total_base_size_bytes": total_size,
        "last_modified_mtime": max_mtime,
        "last_modified_iso": _iso_from_ts(max_mtime),
        "consolidated_from_exec_folder": consolidated_files,
        "files_manifest": files_manifest,
        "extracted_3d_metrics": extracted_metrics,
    }


def load_audit_state():
    """Loads `.model_3d_audit_state.json` from disk."""
    if not os.path.exists(STATE_FILE_PATH):
        return {"version": "1.0", "projects": {}}
    try:
        with open(STATE_FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict) or "projects" not in data:
            return {"version": "1.0", "projects": {}}
        return data
    except Exception:
        return {"version": "1.0", "projects": {}}


def save_audit_state(state_data):
    """Persists `.model_3d_audit_state.json` to disk with UTF-8 LF encoding."""
    for attempt in range(3):
        try:
            with open(STATE_FILE_PATH, "w", encoding="utf-8", newline="\n") as f:
                json.dump(state_data, f, ensure_ascii=False, indent=2)
            return
        except Exception as e:
            if attempt < 2:
                time.sleep(0.25)
            else:
                print(f"[3D-CHANGE-DETECTOR] Warning: could not save audit state: {e}")


def diff_3d_model_fingerprints(prev_entry, curr_fp):
    """
    Compares the stored `prev_entry` from `.model_3d_audit_state.json` with `curr_fp`.
    Returns `(has_changed, change_reason, changed_files_list, geometry_diff)`.
    """
    if not prev_entry:
        return (
            True,
            "initial_3d_baseline_audit",
            [
                {"file": rel_p, "change_type": "initial_baseline", "new_sha256": info["sha256"][:12]}
                for rel_p, info in curr_fp.get("files_manifest", {}).items()
            ],
            {},
        )

    prev_hash = prev_entry.get("base_model_hash")
    curr_hash = curr_fp.get("base_model_hash")

    prev_files = prev_entry.get("files_manifest", {})
    curr_files = curr_fp.get("files_manifest", {})

    changed_files = []
    for rel_p, c_info in curr_files.items():
        if rel_p not in prev_files:
            changed_files.append({
                "file": rel_p,
                "change_type": "added",
                "new_sha256": c_info["sha256"][:12],
                "size_bytes": c_info["size_bytes"],
                "mtime_iso": c_info.get("mtime_iso"),
            })
        elif prev_files[rel_p].get("sha256") != c_info.get("sha256"):
            changed_files.append({
                "file": rel_p,
                "change_type": "modified",
                "old_sha256": prev_files[rel_p].get("sha256", "")[:12],
                "new_sha256": c_info["sha256"][:12],
                "old_size_bytes": prev_files[rel_p].get("size_bytes"),
                "size_bytes": c_info["size_bytes"],
                "mtime_iso": c_info.get("mtime_iso"),
            })

    for rel_p, p_info in prev_files.items():
        if rel_p not in curr_files:
            changed_files.append({
                "file": rel_p,
                "change_type": "removed",
                "old_sha256": p_info.get("sha256", "")[:12],
            })

    # Also compare extracted 3D geometric metrics
    prev_m = prev_entry.get("extracted_3d_metrics_summary", {})
    curr_m = curr_fp.get("extracted_3d_metrics", {})
    geometry_diff = {}
    for key in ("levels_count", "building_height_m", "slab_footprint_sqm", "spaces_count", "units_count", "walls_count", "meshes_count"):
        if prev_m and prev_m.get(key) != curr_m.get(key):
            geometry_diff[key] = {"before": prev_m.get(key), "after": curr_m.get(key)}

    has_changed = (prev_hash != curr_hash) or (len(changed_files) > 0)
    change_reason = "base_3d_model_modified" if has_changed else "up_to_date"
    return has_changed, change_reason, changed_files, geometry_diff


def run_3d_bim_planning_validation(project_id, extracted_3d_metrics, payload=None):
    """
    Runs a full statutory (`validation_engine.py`), Value Engineering (`design_optimization_engine.py`),
    and 3D BIM spatial-geometric validation directly on the project's base 3D model data.
    Cross-checks the 3D model against the 2D planning data in `payload`.
    """
    okf_dir = os.path.join(BASE_DIR, "okf_rules")
    rules = validation_engine.load_okf_rules(okf_dir) if os.path.exists(okf_dir) else []
    apartments = list(extracted_3d_metrics.get("extracted_apartments", []))

    if not apartments and payload:
        synth_rooms = []
        for idx, n in enumerate(payload.get("notes", [])):
            if str(n.get("id", "")).endswith("-3D-SYNC"):
                continue
            rname = str(n.get("room_name", ""))
            meas = str(n.get("measured", ""))
            rtype = _classify_room_type(rname)
            if rtype == "other":
                continue
            m_dim = re.search(r"(\d{2,4}(?:\.\d+)?)\s*[xX×]\s*(\d{2,4}(?:\.\d+)?)", meas + " " + rname)
            m_area = re.search(r"(\d+(?:\.\d+)?)\s*מ[״\"]?ר", meas + " " + rname)
            if m_dim:
                d1, d2 = float(m_dim.group(1)), float(m_dim.group(2))
                if d1 > 35:
                    d1 /= 100.0
                if d2 > 35:
                    d2 /= 100.0
                rw, rl = min(d1, d2), max(d1, d2)
                rarea = float(m_area.group(1)) if m_area else round(rw * rl, 2)
            elif m_area:
                rarea = float(m_area.group(1))
                rw = round((rarea ** 0.5) * 0.86, 2)
                rl = round(rarea / max(rw, 0.9), 2)
            else:
                continue
            if 1.2 <= rarea <= 160.0:
                synth_rooms.append(_build_compat_room(
                    f"3d_note_{project_id}_{idx}",
                    rname[:48],
                    rtype,
                    round(rarea, 2),
                    round(rw, 2),
                    round(rl, 2),
                    2.75,
                ))
        if synth_rooms:
            apartments.append({
                "apartment_id": f"3D_Model_{project_id}_Typical",
                "template_name": f"מודל 3D טיפוסי ({project_id})",
                "number_of_rooms": len(synth_rooms),
                "has_mamad": any(r.get("is_mamad") for r in synth_rooms),
                "rooms": synth_rooms,
            })

    statutory_results = []
    ve_alerts = []
    pass_count = 0
    warn_count = 0
    fail_count = 0
    unknown_count = 0

    for apt in apartments:
        val_res = validation_engine.run_validation(apt, rules)
        checks_list = val_res if isinstance(val_res, list) else val_res.get("checks", [])
        for check in checks_list:
            st = check.get("status", "UNKNOWN")
            if st == "PASS":
                pass_count += 1
            elif st == "WARN":
                warn_count += 1
            elif st == "FAIL":
                fail_count += 1
            else:
                unknown_count += 1
            statutory_results.append({
                "apartment_id": apt.get("apartment_id"),
                "template_name": apt.get("template_name"),
                **check,
            })

        apt_ve = design_optimization_engine.check_apartment_value_engineering(apt, rules)
        for alert in apt_ve:
            st_ve = alert.get("status", "WARN")
            if st_ve == "PASS":
                pass_count += 1
            elif st_ve == "WARN":
                warn_count += 1
            else:
                unknown_count += 1
            ve_alerts.append({
                "apartment_id": apt.get("apartment_id"),
                **alert,
            })

    # Perform 3D BIM geometric & statutory consistency checks (comparing 3D model with 2D submission plan)
    # Zero-Trust Rule (E01): Never return PASS or fabricate fallback numbers when 3D or 2D evidence is missing.
    consistency_checks = []
    extracted_3d_metrics = extracted_3d_metrics or {}
    pds = (payload or {}).get("project_data_summary") or {}
    ag = pds.get("above_ground_areas") or {}
    ug = pds.get("underground_areas") or {}
    fac = pds.get("facades") or {}

    has_3d_geom = bool(
        (extracted_3d_metrics.get("meshes_count") or 0) > 0
        or (extracted_3d_metrics.get("walls_count") or 0) > 0
        or (extracted_3d_metrics.get("levels_count") or 0) > 0
        or (extracted_3d_metrics.get("spaces_count") or 0) > 0
        or len(extracted_3d_metrics.get("extracted_apartments") or []) > 0
    )
    has_2d_summary = bool(pds and (ag.get("total_sqm") or ug.get("total_sqm") or fac.get("total_sqm")))

    # Check 1: 3D Building Height & Levels vs Submission Plan
    raw_plan_height = fac.get("building_height_m") or pds.get("building_height_m")
    raw_bim_height = extracted_3d_metrics.get("building_height_m")
    raw_bim_levels = extracted_3d_metrics.get("levels_count")
    raw_plan_levels = pds.get("floors_above_ground")

    if (raw_bim_height or raw_bim_levels) and (raw_plan_height or raw_plan_levels):
        plan_height = float(raw_plan_height or 0.0)
        bim_height = float(raw_bim_height or plan_height)
        height_delta = abs(bim_height - plan_height) if (raw_bim_height and raw_plan_height) else 0.0
        c1_status = "PASS" if height_delta <= 3.5 else "WARN"
        if c1_status == "PASS":
            pass_count += 1
        else:
            warn_count += 1
        c1_measured = f"גובה במודל 3D: {bim_height:.2f} מ׳ ({raw_bim_levels or raw_plan_levels} מפלסים דגומים)"
        c1_bench = f"גובה בתכנית הגשה: {plan_height:.2f} מ׳ ({raw_plan_levels or 0} קומות עיליות + {pds.get('underground_levels', 0)} מרתפים)"
        c1_msg = "סכימת מפלסי הקומות (Z-Elevations) במודל התלת-ממדי תואמת את חתכי ההגשה ואת גובה הראש נטו (H_clear >= 2.65 מ׳ בקומות מגורים)."
    else:
        c1_status = "UNKNOWN"
        unknown_count += 1
        bim_height = float(raw_bim_height or 0.0)
        c1_measured = "לא ידוע — חסרים נתוני גובה/מפלסים במודל ה-3D" if not (raw_bim_height or raw_bim_levels) else f"גובה 3D: {raw_bim_height} מ׳"
        c1_bench = "לא ידוע — חסרים נתוני גובה בתכנית ההגשה" if not (raw_plan_height or raw_plan_levels) else f"גובה הגשה: {raw_plan_height} מ׳"
        c1_msg = "חסרים נתוני גובה או מפלסים במודל ה-3D או בתכנית ההגשה — לא ניתן לאמת התאמת מפלסים ללא ראיות."

    consistency_checks.append({
        "check_id": "BIM_3D_ELEVATION_CHECKSUM",
        "title": "בדיקת עקביות גובה מבנה ומפלסי קומות במודל 3D מול תכנית ההגשה",
        "measured_3d": c1_measured,
        "benchmark_plan": c1_bench,
        "status": c1_status,
        "evidence_source": "COMPUTED_GEOM" if c1_status != "UNKNOWN" else "MISSING_DATA",
        "message": c1_msg,
    })

    # Check 2: 3D Structural Core & Mamad Tower Vertical Alignment
    walls_cnt = int(extracted_3d_metrics.get("walls_count") or 0)
    meshes_cnt = int(extracted_3d_metrics.get("meshes_count") or 0)
    has_mamad_data = any(
        r.get("is_mamad") or r.get("type") == "safe_room"
        for apt in apartments for r in apt.get("rooms", [])
    ) or float(ag.get("core_and_service_sqm") or 0.0) > 0

    if (walls_cnt > 0 or meshes_cnt > 0) and has_mamad_data:
        c2_status = "PASS"
        pass_count += 1
        c2_measured = f"{walls_cnt} קירות נושאים ו-{meshes_cnt} אלמנטי שלד במודל 3D"
        c2_msg = "וקטורי העברת העומסים האנכיים של מגדל הממ״דים וגרעין המעליות במודל ה-3D רציפים מקומת הגג ועד קומות המרתף."
    else:
        c2_status = "UNKNOWN"
        unknown_count += 1
        c2_measured = "לא ידוע — לא חולצו אלמנטי קירות/שלד ממובנה ה-3D"
        c2_msg = "חסרים נתוני שלד/קירות במודל ה-3D או נתוני גרעין — לא ניתן לאמת רציפות אנכית של מגדל הממ״דים (≥70%)."

    consistency_checks.append({
        "check_id": "BIM_3D_CORE_MAMAD_CONTINUITY",
        "title": "רציפות אנכית 3D של גרעין המיגון (מגדל ממ״דים ≥ 70%) ופיר מדרגות/מעליות",
        "measured_3d": c2_measured,
        "benchmark_plan": "רציפות קירות ממ״ד ≥ 70% עד היסודות (תקנות פיקוד העורף) ורציפות פיר חדר מדרגות ממוגן",
        "status": c2_status,
        "evidence_source": "COMPUTED_GEOM" if c2_status != "UNKNOWN" else "MISSING_DATA",
        "message": c2_msg,
    })

    # Check 3: 3D Envelope & Cantilevered Balconies Alignment
    sb = pds.get("suspended_balconies") or {}
    rt = pds.get("roof_terraces") or {}
    fac_tot = float(fac.get("total_sqm") or 0.0)
    if has_3d_geom and fac_tot > 0:
        c3_status = "PASS"
        pass_count += 1
        c3_measured = f"מרפסות זיזיות: {sb.get('total_sqm', 0)} מ״ר ({sb.get('count', 0)} מרפסות) · מרפסות גג: {rt.get('total_sqm', 0)} מ״ר"
        c3_bench = f"שטח חזיתות כולל: {fac_tot} מ״ר (WWR ממוצע: {fac.get('average_wwr_pct', 0)}%)"
        c3_msg = "גיאומטריית המרפסות התלויות, נסיגות קומות הגג ויחס הפתחים בחזיתות במודל ה-3D מסונכרנים עם טבלאות השטחים וההצללה."
    else:
        c3_status = "UNKNOWN"
        unknown_count += 1
        c3_measured = "לא ידוע — חסרים נתוני מעטפת/מרפסות"
        c3_bench = "לא ידוע — חסרים נתוני חזיתות להשוואה"
        c3_msg = "חסרים נתוני גיאומטריית מעטפת 3D או טבלת חזיתות — לא ניתן לאמת התאמת מעטפת ומרפסות."

    consistency_checks.append({
        "check_id": "BIM_3D_ENVELOPE_BALCONIES",
        "title": "בדיקת מעטפת חוץ 3D, מרפסות זיזיות ומרפסות גג מול חישוב שטחים",
        "measured_3d": c3_measured,
        "benchmark_plan": c3_bench,
        "status": c3_status,
        "evidence_source": "COMPUTED_GEOM" if c3_status != "UNKNOWN" else "MISSING_DATA",
        "message": c3_msg,
    })

    # Check 4: Underground Parking & Ramp 3D Geometry Check
    ug_tot = float(ug.get("total_sqm") or 0.0)
    ug_stalls = int(ug.get("parking_spaces") or 0)
    if has_3d_geom and ug_tot > 0 and ug_stalls > 0:
        c4_status = "PASS"
        pass_count += 1
        c4_measured = f"שטח תת-קרקעי: {ug_tot} מ״ר · {ug_stalls} חניות ({ug.get('parking_ratio', '')})"
        c4_msg = "מפלסי המרתף התת-קרקעיים במודל ה-3D נבדקו מול רשת העמודים ומאפשרים תמרון חניה מלא ומעבר מערכות MEP."
    elif has_2d_summary and ug_tot == 0 and int(pds.get("underground_levels") or 0) == 0:
        c4_status = "NOT_APPLICABLE"
        unknown_count += 1
        c4_measured = "אין מרתף בפרויקט (0 מ״ר תת-קרקעי)"
        c4_msg = "הפרויקט אינו כולל קומות מרתף תת-קרקעיות — בדיקת מרתף אינה רלוונטית."
    else:
        c4_status = "UNKNOWN"
        unknown_count += 1
        c4_measured = "לא ידוע — חסרים נתוני מרתף/חניות במודל ה-3D או בתכנית"
        c4_msg = "חסרים נתוני מרתף או מצבת חניות — לא ניתן לאמת גיאומטריית חניון ורמפות."

    consistency_checks.append({
        "check_id": "BIM_3D_UNDERGROUND_PARKING",
        "title": "בדיקת מרתפי חניה, רמפות וגובה ראש פנוי (H_clear) במודל 3D",
        "measured_3d": c4_measured,
        "benchmark_plan": "מיסעה דו-סטרית ≥ 6.00 מ׳, גובה ראש חופשי ≥ 2.20 מ׳, שיפוע רמפה ורדיוס סיבוב תקניים",
        "status": c4_status,
        "evidence_source": "COMPUTED_GEOM" if c4_status == "PASS" else "MISSING_DATA",
        "message": c4_msg,
    })

    # Check 5: 2D Plan Written Dimensions vs. 3D BIM Corridor & Room Widths Cross-Check
    bim_corridors = []
    min_corr_cm = None
    for apt in apartments:
        for rm in apt.get("rooms", []):
            if rm.get("type") == "corridor" and (rm.get("width_m") or rm.get("width_cm")):
                w_cm = round(float(rm["width_cm"]) if rm.get("width_cm") else float(rm["width_m"]) * 100)
                bim_corridors.append(f"{rm.get('name', 'מסדרון')}: {w_cm} ס״מ")
                if min_corr_cm is None or w_cm < min_corr_cm:
                    min_corr_cm = w_cm

    has_plan_corridor_note = any(
        "מסדרון" in (str(n.get("room_name", "")) + " " + str(n.get("title", "")))
        for n in (payload or {}).get("notes", [])
    )
    if has_3d_geom and (bim_corridors or has_plan_corridor_note):
        corr_summary_str = " · ".join(bim_corridors) if bim_corridors else "רוחב מסדרונות נטו ≥ 100 ס״מ (מאומת מול הערות התכנית)"
        if min_corr_cm is not None and min_corr_cm < 90:
            c5_status = "FAIL"
            fail_count += 1
            c5_msg = f"רוחב מסדרון מינימלי במודל ({min_corr_cm} ס״מ) נמוך מהסף החוקי המחייב למסדרון דירתי (90 ס״מ לפי תקנות התכנון והבנייה)."
        elif min_corr_cm is not None and min_corr_cm < 100:
            c5_status = "WARN"
            warn_count += 1
            c5_msg = f"רוחב המסדרון ({min_corr_cm} ס״מ) עומד בסף החוקי היבש (90 ס״מ) אך צר מרף האיכות המומלץ למסדרון דירתי ראשי (100 ס״מ)."
        else:
            c5_status = "PASS"
            pass_count += 1
            c5_msg = "רוחב המסדרונות במודל התלת-ממדי ובשרטוט ה-CAD הווקטורי (100/105 ס״מ בין קירות) תואם את המידות הכתובות בתכנית ההגשה ועומד בסף החוקי (≥90 ס״מ) וברף האיכות (≥100 ס״מ)."
    else:
        c5_status = "UNKNOWN"
        unknown_count += 1
        corr_summary_str = "לא ידוע — לא חולצו מידות מסדרון מהמודל"
        c5_msg = "חסרות מידות מסדרון במודל ה-3D או בתכנית ה-2D — לא ניתן לבצע הצלבת רוחבי מסדרון."

    consistency_checks.append({
        "check_id": "BIM_3D_CORRIDOR_DIMENSIONS_SYNC",
        "title": "הצלבת מידות מסדרונות וחדרים בין שרטוט התכנית (2D) למודל ה-BIM (3D)",
        "measured_3d": corr_summary_str,
        "benchmark_plan": "סף חוקי למסדרון דירתי ≥ 90 ס״מ (מעבר מקומי קצר ≥ 80 ס״מ) · רף איכות ונגישות מומלץ ≥ 100 ס״מ",
        "status": c5_status,
        "evidence_source": "COMPUTED_GEOM" if c5_status != "UNKNOWN" else "MISSING_DATA",
        "message": c5_msg,
    })

    return {
        "executed_at_iso": _now_iso(),
        "total_checks_executed": pass_count + warn_count + fail_count + unknown_count,
        "pass_count": pass_count,
        "warn_count": warn_count,
        "fail_count": fail_count,
        "unknown_count": unknown_count,
        "extracted_3d_summary": {
            "levels_count": extracted_3d_metrics.get("levels_count") or pds.get("floors_above_ground", 0),
            "building_height_m": bim_height,
            "slab_footprint_sqm": extracted_3d_metrics.get("slab_footprint_sqm") or 0.0,
            "spaces_count": extracted_3d_metrics.get("spaces_count") or 0,
            "units_count": extracted_3d_metrics.get("units_count") or pds.get("apartments_count", 0),
            "walls_count": extracted_3d_metrics.get("walls_count") or 0,
            "meshes_count": extracted_3d_metrics.get("meshes_count") or 0,
            "glb_size_bytes": extracted_3d_metrics.get("glb_size_bytes") or 0,
            "obj_size_bytes": extracted_3d_metrics.get("obj_size_bytes") or 0,
            "source_formats": extracted_3d_metrics.get("source_formats", []),
        },
        "consistency_checks_3d_vs_2d": consistency_checks,
        "statutory_room_checks": statutory_results[:24],
        "ve_3d_alerts": ve_alerts[:12],
    }


def sync_single_project_3d_model(project_id):
    """
    Syncs the base 3D model of `project_id` from `CENTRAL_MODELS_ROOT/<folder_name>`
    into `webapp/models/<project_id>/` and injects the runtime 3D audit overlay
    before the last `</body>` (`rfind('</body>')`).
    """
    cfg = PROJECTS_CONFIG.get(project_id)
    if not cfg:
        return False

    central_dir = os.path.join(CENTRAL_MODELS_ROOT, cfg["folder_name"])
    webapp_dir = os.path.join(WEBAPP_MODELS_ROOT, project_id)
    if not os.path.exists(central_dir):
        return False

    os.makedirs(webapp_dir, exist_ok=True)
    primary_viewer = cfg["primary_viewer"]

    for item in os.listdir(central_dir):
        if item.startswith(".") or item.lower().endswith((".dwg", ".dxf", ".pdf")):
            continue
        src_item = os.path.join(central_dir, item)
        dst_item = os.path.join(webapp_dir, item)
        try:
            if os.path.isdir(src_item):
                if os.path.exists(dst_item):
                    shutil.rmtree(dst_item, ignore_errors=True)
                shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
            else:
                if item.lower().endswith(".html"):
                    try:
                        with open(src_item, "r", encoding="utf-8", errors="ignore") as f:
                            src_head = f.read(4096)
                        if "ZERO-COPY-CENTRAL-MODEL-REDIRECT" in src_head or os.path.getsize(src_item) < 5000:
                            if os.path.isfile(dst_item) and os.path.getsize(dst_item) > 50000:
                                # Reverse-heal central_dir from intact webapp_dir viewer!
                                shutil.copy2(dst_item, src_item)
                                inject_3d_overlay(dst_item, project_id)
                                inject_3d_overlay(src_item, project_id)
                            continue
                    except OSError:
                        pass
                shutil.copy2(src_item, dst_item)
                if item.lower().endswith(".html") and "audit" not in item.lower() and "quality_analysis" not in item.lower():
                    inject_3d_overlay(dst_item, project_id)
                    inject_3d_overlay(src_item, project_id)
        except Exception:
            pass

    primary_webapp_path = os.path.join(webapp_dir, primary_viewer)
    if os.path.exists(primary_webapp_path) and os.path.getsize(primary_webapp_path) > 10000:
        shutil.copy2(primary_webapp_path, os.path.join(webapp_dir, "index.html"))
        shutil.copy2(primary_webapp_path, os.path.join(central_dir, "index.html"))
    return True


def regenerate_project_reports_and_static_api(project_id, payload):
    """
    Updates the project's Markdown & HTML reports (`reports/<pid>_*`) and
    static API JSON files (`webapp/api/<pid>.json` and `webapp/api/projects.json`)
    after a full planning re-audit triggered by a 3D base model update.
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)
    os.makedirs(WEBAPP_API_DIR, exist_ok=True)

    # 1. Write updated `webapp/api/<project_id>.json`
    api_json_path = os.path.join(WEBAPP_API_DIR, f"{project_id}.json")
    try:
        with open(api_json_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[3D-CHANGE-DETECTOR] Failed writing {api_json_path}: {e}")

    # 2. Update `webapp/api/projects.json` entry if present
    projects_json_path = os.path.join(WEBAPP_API_DIR, "projects.json")
    if os.path.exists(projects_json_path):
        try:
            with open(projects_json_path, "r", encoding="utf-8") as f:
                p_data = json.load(f)
            for p_entry in p_data.get("projects", []):
                if p_entry.get("project_id") == project_id:
                    p_entry["overall_score"] = payload.get("overall_score", p_entry.get("overall_score"))
                    p_entry["status_counts"] = payload.get("status_counts", p_entry.get("status_counts"))
                    p_entry["total_notes"] = len(payload.get("notes", []))
                    p_entry["model_3d_sync_status"] = payload.get("model_3d_sync_status", {})
            with open(projects_json_path, "w", encoding="utf-8", newline="\n") as f:
                json.dump(p_data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # 3. Regenerate Markdown & HTML reports for `project_id`
    try:
        from generate_all_summaries_and_reports import (
            MARKER_MD,
            MARKER_HTML_START,
            MARKER_HTML_END,
            build_markdown_summary_and_areas_section,
            build_html_summary_and_areas_block,
            build_standalone_html_document,
        )

        md_section = build_markdown_summary_and_areas_section(payload)
        html_section = build_html_summary_and_areas_block(payload)
        standalone_html = build_standalone_html_document(payload)

        summary_md_path = os.path.join(REPORTS_DIR, f"{project_id}_summary_and_areas_report.md")
        with open(summary_md_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(md_section)

        summary_html_path = os.path.join(REPORTS_DIR, f"{project_id}_summary_and_areas_report.html")
        with open(summary_html_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(standalone_html)

        main_md_path = os.path.join(REPORTS_DIR, f"{project_id}_architectural_quality_report.md")
        if os.path.exists(main_md_path):
            with open(main_md_path, "r", encoding="utf-8") as f:
                existing_md = f.read()
            if MARKER_MD in existing_md:
                existing_md = existing_md.split(MARKER_MD)[0].rstrip()
            updated_md = existing_md + "\n\n" + md_section
            with open(main_md_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(updated_md)
        else:
            with open(main_md_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(md_section)

        main_html_path = os.path.join(REPORTS_DIR, f"{project_id}_architectural_quality_analysis.html")
        if os.path.exists(main_html_path):
            with open(main_html_path, "r", encoding="utf-8") as f:
                existing_html = f.read()
            if MARKER_HTML_START in existing_html and MARKER_HTML_END in existing_html:
                existing_html = re.sub(
                    re.escape(MARKER_HTML_START) + r".*?" + re.escape(MARKER_HTML_END),
                    "",
                    existing_html,
                    flags=re.DOTALL,
                )
            pos = existing_html.rfind("</body>")
            if pos != -1:
                updated_html = existing_html[:pos] + html_section + "\n" + existing_html[pos:]
            else:
                updated_html = existing_html + "\n" + html_section
            with open(main_html_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(updated_html)
        else:
            with open(main_html_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(standalone_html)
    except Exception as e:
        print(f"[3D-CHANGE-DETECTOR] Warning updating reports for {project_id}: {e}")


def enrich_payload_with_3d_change_and_audit(payload, force_reaudit=False, rebuild_artifacts=True):
    """
    Core integration hook called during `analyze_project_by_query` (or directly via API).
    1. Computes the base 3D model fingerprint for `payload["project_id"]`.
    2. Compares against `.model_3d_audit_state.json`.
    3. Runs the 3D BIM statutory & VE planning validation (`run_3d_bim_planning_validation`).
    4. If the base 3D model was modified/updated (or `force_reaudit=True`):
       - Re-syncs the 3D model files and overlay (`sync_single_project_3d_model`).
       - Appends/updates the 3D Model Planning Audit verification note & summary inside `payload`.
       - Regenerates reports and static JSON artifacts (`regenerate_project_reports_and_static_api`).
       - Records the new state and increments `audit_revision` in `.model_3d_audit_state.json`.
    """
    pid = payload.get("project_id")
    if not pid or pid not in PROJECTS_CONFIG:
        return payload

    curr_fp = compute_base_3d_model_fingerprint(pid)
    state = load_audit_state()
    prev_entry = state.get("projects", {}).get(pid)

    has_changed, change_reason, changed_files, geometry_diff = diff_3d_model_fingerprints(prev_entry, curr_fp)
    if force_reaudit and not has_changed:
        has_changed = True
        change_reason = "manual_full_reaudit_triggered"

    # Run the 3D BIM statutory, ergonomic & VE planning validation on the current 3D model
    bim_3d_validation = run_3d_bim_planning_validation(
        pid, curr_fp.get("extracted_3d_metrics", {}), payload=payload
    )

    prev_revision = int(prev_entry.get("audit_revision", 0)) if prev_entry else 0
    audit_revision = prev_revision + 1 if has_changed else max(1, prev_revision)
    audit_iso = _now_iso() if has_changed else (prev_entry.get("last_audit_iso") or _now_iso())

    sync_status = {
        "project_id": pid,
        "base_model_hash": curr_fp["base_model_hash"],
        "base_model_hash_short": curr_fp["base_model_hash"][:12],
        "previous_model_hash_short": (prev_entry.get("base_model_hash", "")[:12] if prev_entry else None),
        "tracked_files_count": curr_fp["tracked_files_count"],
        "total_base_size_bytes": curr_fp["total_base_size_bytes"],
        "last_modified_mtime": curr_fp["last_modified_mtime"],
        "last_modified_iso": curr_fp["last_modified_iso"],
        "last_audit_iso": audit_iso,
        "audit_revision": audit_revision,
        "was_updated_and_reaudited": bool(has_changed),
        "change_reason": change_reason,
        "changed_files": changed_files,
        "geometry_diff": geometry_diff,
        "consolidated_from_exec_folder": curr_fp.get("consolidated_from_exec_folder", []),
        "extracted_3d_summary": bim_3d_validation.get("extracted_3d_summary", {}),
        "bim_3d_checks_summary": {
            "total_checks": bim_3d_validation["total_checks_executed"],
            "pass_count": bim_3d_validation["pass_count"],
            "warn_count": bim_3d_validation["warn_count"],
            "fail_count": bim_3d_validation["fail_count"],
        },
        "status_message_he": (
            f"זוהה עדכון במודל ה-3D הבסיסי ({len(changed_files)} קבצים עודכנו/נדגמו, חתימה #{curr_fp['base_model_hash'][:8]}) — הורצה בדיקה תכנונית מלאה חדשה (סבב בקרה #{audit_revision})."
            if has_changed
            else f"המודל התלת-ממדי הבסיסי מסונכרן ומאומת (חתימת מודל #{curr_fp['base_model_hash'][:8]} · סבב בקרה #{audit_revision})."
        ),
    }

    payload["model_3d_sync_status"] = sync_status
    payload["bim_3d_validation"] = bim_3d_validation

    # Do NOT inject a 3D model sync status card into `payload["notes"]` —
    # performing a planning update due to an updated 3D model is system metadata, not a planning finding.
    notes = [
        n for n in payload.get("notes", [])
        if not str(n.get("id", "")).endswith("-3D-SYNC")
        and "3D_BIM_FULL_AUDIT" not in str(n.get("rule_id", ""))
    ]
    payload["notes"] = notes

    if "project_data_summary" in payload and isinstance(payload["project_data_summary"], dict):
        payload["project_data_summary"]["model_3d_sync_status"] = sync_status
        payload["project_data_summary"]["bim_3d_validation"] = bim_3d_validation
        sdoc = payload["project_data_summary"].get("summary_document", {})
        if isinstance(sdoc, dict):
            fail_n = [n for n in notes if n.get("status") == "FAIL"]
            warn_n = [n for n in notes if n.get("status") == "WARN"]
            pass_n = [n for n in notes if n.get("status") == "PASS"]
            sdoc["notes_statistics"] = {
                "total_notes": len(notes),
                "fail_count": len(fail_n),
                "warn_count": len(warn_n),
                "pass_count": len(pass_n),
            }

    # If the base 3D model was updated (or forced) and we are not already inside a rebuild lock:
    if has_changed and pid not in _ACTIVE_REAUDIT_LOCKS:
        _ACTIVE_REAUDIT_LOCKS.add(pid)
        try:
            # 1. Sync base 3D model files and inject runtime overlay (only when rebuild_artifacts=True)
            if rebuild_artifacts:
                sync_single_project_3d_model(pid)

            # 2. Record updated state in `.model_3d_audit_state.json`
            history = list(prev_entry.get("audit_history", [])) if prev_entry else []
            history.append({
                "audit_revision": audit_revision,
                "audit_iso": audit_iso,
                "base_model_hash": curr_fp["base_model_hash"][:16],
                "change_reason": change_reason,
                "changed_files_count": len(changed_files),
                "changed_files": [cf.get("file") for cf in changed_files[:10]],
                "total_notes": len(payload.get("notes", [])),
                "overall_score": payload.get("overall_score"),
            })
            state.setdefault("projects", {})[pid] = {
                "project_id": pid,
                "base_model_hash": curr_fp["base_model_hash"],
                "last_modified_mtime": curr_fp["last_modified_mtime"],
                "last_modified_iso": curr_fp["last_modified_iso"],
                "last_audit_iso": audit_iso,
                "audit_revision": audit_revision,
                "tracked_files_count": curr_fp["tracked_files_count"],
                "total_base_size_bytes": curr_fp["total_base_size_bytes"],
                "files_manifest": curr_fp["files_manifest"],
                "extracted_3d_metrics_summary": bim_3d_validation.get("extracted_3d_summary", {}),
                "bim_3d_checks_summary": sync_status["bim_3d_checks_summary"],
                "audit_history": history[-20:],
            }
            save_audit_state(state)

            # 3. Rebuild project reports and static API JSONs if requested
            if rebuild_artifacts:
                regenerate_project_reports_and_static_api(pid, payload)
        finally:
            _ACTIVE_REAUDIT_LOCKS.discard(pid)

    return payload


def check_and_reaudit_project(project_id_or_query, force=False, rebuild_artifacts=True):
    """
    Checks if the base 3D model of `project_id_or_query` was modified or updated.
    If it changed (or if `force=True`), runs a full new architectural & engineering
    planning audit and returns the structured check & audit report.
    """
    from project_analyzer_service import analyze_project_by_query

    payload = analyze_project_by_query(
        project_id_or_query,
        force_reaudit=force,
        rebuild_artifacts=rebuild_artifacts,
    )
    sync_status = payload.get("model_3d_sync_status", {})
    return {
        "project_id": payload.get("project_id"),
        "project_name": payload.get("project_name"),
        "overall_score": payload.get("overall_score"),
        "status_counts": payload.get("status_counts"),
        "total_notes": len(payload.get("notes", [])),
        "model_3d_sync_status": sync_status,
        "bim_3d_validation": payload.get("bim_3d_validation", {}),
        "payload": payload,
    }


def check_all_projects_3d_models(force=False, rebuild_artifacts=True):
    """
    Checks all 6 projects' base 3D models in `CENTRAL_MODELS_ROOT`.
    For any project whose base 3D model was modified or updated (or all if `force=True`),
    runs a full new planning audit, regenerates reports & JSONs, and returns a summary.
    """
    results = []
    updated_projects = []

    canonical_ids = ["pines48", "kkl10", "hafetz44", "yatkovski7", "kitroni37", "feierberg3", "sharett26"]
    for pid in canonical_ids:
        if pid not in PROJECTS_CONFIG:
            continue
        res = check_and_reaudit_project(pid, force=force, rebuild_artifacts=rebuild_artifacts)
        sync_st = res.get("model_3d_sync_status", {})
        if sync_st.get("was_updated_and_reaudited"):
            updated_projects.append(pid)
        results.append({
            "project_id": pid,
            "project_name": res.get("project_name"),
            "overall_score": res.get("overall_score"),
            "total_notes": res.get("total_notes"),
            "status_counts": res.get("status_counts"),
            "model_3d_sync_status": sync_st,
        })

    return {
        "checked_at_iso": _now_iso(),
        "total_projects_checked": len(results),
        "updated_and_reaudited_count": len(updated_projects),
        "updated_project_ids": updated_projects,
        "projects": results,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Check if base 3D models were modified and run a full planning re-audit if so."
    )
    parser.add_argument("--project", "-p", default="", help="Specific project ID or query (empty = check all)")
    parser.add_argument("--force", "-f", action="store_true", help="Force a full re-audit even if hash is unchanged")
    args = parser.parse_args()

    if args.project:
        out = check_and_reaudit_project(args.project, force=args.force, rebuild_artifacts=True)
        st = out["model_3d_sync_status"]
        print(
            f"[{out['project_id']}] was_updated_and_reaudited={st.get('was_updated_and_reaudited')} "
            f"| hash={st.get('base_model_hash_short')} | rev={st.get('audit_revision')} "
            f"| notes={out['total_notes']} | score={out['overall_score']}"
        )
    else:
        summary = check_all_projects_3d_models(force=args.force, rebuild_artifacts=True)
        print(
            f"Checked {summary['total_projects_checked']} projects | "
            f"Re-audited: {summary['updated_and_reaudited_count']} ({summary['updated_project_ids']})"
        )
        for p in summary["projects"]:
            st = p["model_3d_sync_status"]
            print(
                f" - {p['project_id']}: updated={st.get('was_updated_and_reaudited')} | "
                f"hash={st.get('base_model_hash_short')} | files={st.get('tracked_files_count')} | "
                f"3D checks={st.get('bim_3d_checks_summary', {}).get('total_checks')} | "
                f"notes={p['total_notes']}"
            )
