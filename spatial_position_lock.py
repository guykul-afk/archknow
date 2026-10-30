# -*- coding: utf-8 -*-
"""
ArchiCheck AI — Deterministic 2D↔3D Position Verification & Locking Engine
(מנגנון בדיקה וקיבוע דו-ערכי למיקומי הערות בין התצוגה הדו-ממדית לתלת-ממדית)

Responsibilities:
1. Defines calibrated 2D-sheet-to-3D-BIM coordinate transformations (`SHEET_2D_TO_3D_TRANSFORMS`)
   for all 32 architectural sheets across all 6 projects (`feierberg3`, `hafetz44`, `yatkovski7`,
   `pines48`, `kkl10`, `kitroni37`).
2. Maps 2D percentage bounding boxes (`x_pct`, `y_pct`, `w_pct`, `h_pct`) to exact 3D BIM coordinates
   (`floor_id`, `bbox_3d`, `pin_3d`, `camera`) with 1:1 wing, room, and elevation fidelity.
3. Enforces camera orientation locking (`theta in [+1.25, +1.85]` for floor-sliced views) so that
   3D Dollhouse / 1:50 views always match the 2D plan orientation (North=Top, South=Bottom,
   West=Left, East=Right) and never flip Left↔Right.
4. Generates cryptographic SHA-256 position locks (`position_lock`) per note and persists
   the master lock registry (`spatial_lock_registry.json`).
"""

import hashlib
import json
import math
import os
import sys

LOCK_VERSION = "v3.0-2D3D-LOCK"
REGISTRY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spatial_lock_registry.json")

# =============================================================================
# 1. CALIBRATED 2D-SHEET <-> 3D-MODEL TRANSFORMS FOR ALL 6 PROJECTS (32 SHEETS)
# =============================================================================
# Each sheet entry specifies:
# - rect_2d_pct: [x0_pct, y0_pct, x1_pct, y1_pct] of the building/floor footprint on the 2D sheet PNG
# - rect_3d_xz:  [x0_3d, z0_3d, x1_3d, z1_3d] of the exact same footprint in 3D world space (X, Z)
# - floor_id:    target floor slice ID in the project's 3D viewer
# - z_floor:     3D elevation Y of floor slab (meters)
# - z_ceil:      3D elevation Y of ceiling slab (meters)
SHEET_2D_TO_3D_TRANSFORMS = {
    "feierberg3": {
        "fb_typical": {
            "rect_2d_pct": [11.2, 21.8, 87.2, 65.5],
            "rect_3d_xz": [-13.12, -4.20, 13.12, 5.80],
            "floor_id": "f4",
            "z_floor": 12.95,
            "z_ceil": 15.90,
        },
        "fb_floor9": {
            "rect_2d_pct": [11.2, 21.8, 87.2, 64.0],
            "rect_3d_xz": [-13.12, -4.20, 13.12, 5.80],
            "floor_id": "f9",
            "z_floor": 28.87,
            "z_ceil": 31.82,
        },
        "fb_floor10": {
            "rect_2d_pct": [16.0, 21.8, 84.0, 58.0],
            "rect_3d_xz": [-11.62, -4.20, 11.62, 2.20],
            "floor_id": "f10",
            "z_floor": 32.02,
            "z_ceil": 34.97,
        },
        "fb_ground": {
            "rect_2d_pct": [11.0, 27.0, 88.0, 62.5],
            "rect_3d_xz": [-13.12, -4.20, 13.80, 4.20],
            "floor_id": "kar",
            "z_floor": 0.00,
            "z_ceil": 3.25,
        },
        "fb_basement1": {
            "rect_2d_pct": [6.5, 17.0, 91.5, 76.0],
            "rect_3d_xz": [-16.75, -7.89, 15.25, 7.24],
            "floor_id": "b1",
            "z_floor": -4.80,
            "z_ceil": -0.25,
        },
        "fb_basement2": {
            "rect_2d_pct": [6.5, 17.0, 91.5, 76.0],
            "rect_3d_xz": [-16.75, -7.89, 15.25, 7.24],
            "floor_id": "b2",
            "z_floor": -7.80,
            "z_ceil": -4.90,
        },
    },
    "hafetz44": {
        "h44_typical": {
            "rect_2d_pct": [12.0, 18.0, 86.0, 80.0],
            "rect_3d_xz": [-13.36, -5.18, 14.36, 4.99],
            "floor_id": "f4",
            "z_floor": 12.98,
            "z_ceil": 15.65,
        },
        "h44_penthouse": {
            "rect_2d_pct": [14.0, 18.0, 86.0, 80.0],
            "rect_3d_xz": [-13.36, -5.18, 14.36, 4.22],
            "floor_id": "f9",
            "z_floor": 28.73,
            "z_ceil": 31.30,
        },
        "h44_ground": {
            "rect_2d_pct": [12.0, 18.0, 88.0, 82.0],
            "rect_3d_xz": [-13.36, -5.18, 14.36, 4.99],
            "floor_id": "kar",
            "z_floor": 0.03,
            "z_ceil": 3.15,
        },
        "h44_basement": {
            "rect_2d_pct": [12.0, 18.0, 84.0, 83.0],
            "rect_3d_xz": [-17.72, -9.20, 18.51, 9.05],
            "floor_id": "mar",
            "z_floor": -5.08,
            "z_ceil": -2.25,
        },
    },
    "yatkovski7": {
        "yat_typical": {
            "rect_2d_pct": [24.0, 18.0, 74.0, 82.0],
            "rect_3d_xz": [-7.80, -6.10, 6.60, 14.80],
            "floor_id": "f4",
            "z_floor": 13.33,
            "z_ceil": 16.20,
        },
        "yat_floor5": {
            "rect_2d_pct": [24.0, 18.0, 74.0, 82.0],
            "rect_3d_xz": [-7.80, -6.10, 6.60, 14.80],
            "floor_id": "f5",
            "z_floor": 16.56,
            "z_ceil": 19.45,
        },
        "yat_floor6": {
            "rect_2d_pct": [24.0, 18.0, 74.0, 82.0],
            "rect_3d_xz": [-7.80, -6.10, 6.60, 14.80],
            "floor_id": "f6",
            "z_floor": 19.80,
            "z_ceil": 22.70,
        },
        "yat_ground": {
            "rect_2d_pct": [22.0, 14.0, 76.0, 86.0],
            "rect_3d_xz": [-7.80, -6.50, 6.60, 16.80],
            "floor_id": "kar",
            "z_floor": 0.03,
            "z_ceil": 3.55,
        },
        "yat_basement": {
            "rect_2d_pct": [12.0, 14.0, 78.0, 84.0],
            "rect_3d_xz": [-11.15, -10.90, 6.60, 19.00],
            "floor_id": "mar",
            "z_floor": -4.35,
            "z_ceil": -0.30,
        },
    },
    "pines48": {
        "f1_5": {
            "rect_2d_pct": [14.0, 13.0, 88.5, 81.5],
            "rect_3d_xz": [-12.47, -8.88, 13.00, 8.67],
            "floor_id": "f3",
            "z_floor": 10.37,
            "z_ceil": 13.04,
        },
        "f6": {
            "rect_2d_pct": [14.0, 13.0, 88.5, 81.5],
            "rect_3d_xz": [-12.47, -8.88, 13.00, 8.67],
            "floor_id": "f6",
            "z_floor": 19.72,
            "z_ceil": 22.55,
        },
        "f7": {
            "rect_2d_pct": [18.0, 16.0, 84.0, 78.0],
            "rect_3d_xz": [-9.53, -6.87, 8.37, 6.87],
            "floor_id": "f7",
            "z_floor": 22.95,
            "z_ceil": 25.80,
        },
        "roof": {
            "rect_2d_pct": [20.0, 18.0, 82.0, 76.0],
            "rect_3d_xz": [-9.53, -6.87, 8.37, 6.87],
            "floor_id": "gag",
            "z_floor": 26.00,
            "z_ceil": 28.60,
        },
        "ground": {
            "rect_2d_pct": [14.0, 13.0, 88.5, 84.0],
            "rect_3d_xz": [-12.47, -8.88, 13.00, 8.67],
            "floor_id": "kar",
            "z_floor": 0.06,
            "z_ceil": 3.81,
        },
        "basement": {
            "rect_2d_pct": [14.0, 12.0, 88.5, 90.0],
            "rect_3d_xz": [-13.50, -9.80, 13.80, 9.80],
            "floor_id": "mar",
            "z_floor": -3.80,
            "z_ceil": -0.25,
        },
    },
    "kkl10": {
        "kkl_typical": {
            "rect_2d_pct": [25.5, 9.0, 73.5, 90.0],
            "rect_3d_xz": [0.00, -32.50, 12.73, 0.60],
            "floor_id": "L4",
            "z_floor": 13.65,
            "z_ceil": 16.55,
        },
        "kkl_f1_2": {
            "rect_2d_pct": [25.5, 9.0, 73.5, 90.0],
            "rect_3d_xz": [0.00, -32.50, 12.73, 0.60],
            "floor_id": "L2",
            "z_floor": 7.05,
            "z_ceil": 9.95,
        },
        "kkl_penthouse": {
            "rect_2d_pct": [25.5, 9.0, 73.5, 90.0],
            "rect_3d_xz": [0.00, -32.50, 12.73, 0.60],
            "floor_id": "L8",
            "z_floor": 26.50,
            "z_ceil": 29.50,
        },
        "kkl_ground": {
            "rect_2d_pct": [24.0, 9.0, 75.0, 90.0],
            "rect_3d_xz": [-0.50, -33.00, 13.20, 1.20],
            "floor_id": "L0",
            "z_floor": 0.00,
            "z_ceil": 3.75,
        },
        "kkl_basement": {
            "rect_2d_pct": [18.0, 8.0, 78.0, 91.0],
            "rect_3d_xz": [-3.60, -35.10, 16.40, 4.60],
            "floor_id": "B1",
            "z_floor": -4.35,
            "z_ceil": -0.80,
        },
        "kkl_basement2": {
            "rect_2d_pct": [18.0, 8.0, 78.0, 91.0],
            "rect_3d_xz": [-3.60, -35.10, 16.40, 4.60],
            "floor_id": "B2",
            "z_floor": -7.65,
            "z_ceil": -4.45,
        },
    },
    "kitroni37": {
        "kit_typical": {
            "rect_2d_pct": [7.0, 11.5, 74.5, 89.0],
            "rect_3d_xz": [-13.95, -25.15, 19.63, 7.56],
            "floor_id": "k2_4",
            "z_floor": 10.62,
            "z_ceil": 13.42,
        },
        "kit_floor8": {
            "rect_2d_pct": [7.0, 11.5, 74.5, 89.0],
            "rect_3d_xz": [-13.95, -25.15, 19.63, 7.56],
            "floor_id": "k8",
            "z_floor": 23.02,
            "z_ceil": 25.82,
        },
        "kit_penthouse": {
            "rect_2d_pct": [7.0, 11.5, 74.5, 89.0],
            "rect_3d_xz": [-10.86, -25.15, 18.52, 7.56],
            "floor_id": "k9",
            "z_floor": 26.22,
            "z_ceil": 29.22,
        },
        "kit_ground": {
            "rect_2d_pct": [7.0, 11.5, 74.5, 89.0],
            "rect_3d_xz": [-14.11, -28.79, 21.43, 7.56],
            "floor_id": "kar",
            "z_floor": 0.00,
            "z_ceil": 4.20,
        },
        "kit_basement": {
            "rect_2d_pct": [7.0, 8.0, 74.5, 92.0],
            "rect_3d_xz": [-16.53, -28.37, 24.59, 10.68],
            "floor_id": "mar",
            "z_floor": -3.85,
            "z_ceil": -0.35,
        },
    },
    "sharett26": {
        "ms_typical": {
            "rect_2d_pct": [0.0, 0.0, 100.0, 100.0],
            "rect_3d_xz": [-23.00, -20.00, 23.00, 20.00],
            "floor_id": "f4",
            "z_floor": 15.57,
            "z_ceil": 18.50,
        },
        "ms_floor8": {
            "rect_2d_pct": [0.0, 0.0, 100.0, 100.0],
            "rect_3d_xz": [-23.00, -20.00, 23.00, 20.00],
            "floor_id": "f8",
            "z_floor": 28.17,
            "z_ceil": 31.10,
        },
        "ms_floor9_roof": {
            "rect_2d_pct": [0.0, 0.0, 100.0, 100.0],
            "rect_3d_xz": [-23.00, -20.00, 23.00, 20.00],
            "floor_id": "f9",
            "z_floor": 31.32,
            "z_ceil": 33.77,
        },
        "ms_ground": {
            "rect_2d_pct": [0.0, 0.0, 100.0, 100.0],
            "rect_3d_xz": [-23.00, -20.00, 23.00, 20.00],
            "floor_id": "kar",
            "z_floor": 0.00,
            "z_ceil": 2.90,
        },
        "ms_gallery": {
            "rect_2d_pct": [0.0, 0.0, 100.0, 100.0],
            "rect_3d_xz": [-23.00, -20.00, 23.00, 20.00],
            "floor_id": "gal",
            "z_floor": 3.10,
            "z_ceil": 5.90,
        },
        "ms_basement1": {
            "rect_2d_pct": [0.0, 0.0, 100.0, 100.0],
            "rect_3d_xz": [-23.00, -20.00, 23.00, 20.00],
            "floor_id": "bm1",
            "z_floor": -3.00,
            "z_ceil": -0.20,
        },
        "ms_basement2": {
            "rect_2d_pct": [0.0, 0.0, 100.0, 100.0],
            "rect_3d_xz": [-23.00, -20.00, 23.00, 20.00],
            "floor_id": "bm2",
            "z_floor": -6.00,
            "z_ceil": -3.20,
        },
    },
}


def get_sheet_transform(project_id: str, sheet_id: str) -> dict:
    proj_map = SHEET_2D_TO_3D_TRANSFORMS.get(project_id, {})
    if sheet_id in proj_map:
        return proj_map[sheet_id]
    if proj_map:
        return next(iter(proj_map.values()))
    return {
        "rect_2d_pct": [12.0, 15.0, 88.0, 85.0],
        "rect_3d_xz": [-13.0, -7.0, 13.0, 7.0],
        "floor_id": "f4",
        "z_floor": 12.0,
        "z_ceil": 14.8,
    }


def map_2d_pct_to_3d_xz(project_id: str, sheet_id: str, x_pct: float, y_pct: float) -> tuple:
    """Maps a single 2D percentage coordinate (x_pct, y_pct) to 3D world (X, Z) meters."""
    tf = get_sheet_transform(project_id, sheet_id)
    px0, py0, px1, py1 = tf["rect_2d_pct"]
    wx0, wz0, wx1, wz1 = tf["rect_3d_xz"]
    u = (float(x_pct) - px0) / max(1e-6, (px1 - px0))
    v = (float(y_pct) - py0) / max(1e-6, (py1 - py0))
    wx = wx0 + u * (wx1 - wx0)
    wz = wz0 + v * (wz1 - wz0)
    return round(wx, 2), round(wz, 2)


def compute_calibrated_spatial_3d(project_id: str, note: dict) -> dict:
    """
    Computes a 1:1 calibrated 3D spatial anchor (`floor_id`, `bbox_3d`, `pin_3d`, `camera`)
    from a note's 2D sheet coordinates using `SHEET_2D_TO_3D_TRANSFORMS`.
    """
    sheet_id = str(note.get("sheet_id") or "")
    tf = get_sheet_transform(project_id, sheet_id)

    x_pct = float(note.get("x_pct", 35.0))
    y_pct = float(note.get("y_pct", 35.0))
    w_pct = float(note.get("w_pct", 20.0))
    h_pct = float(note.get("h_pct", 20.0))
    cx_pct = float(note.get("cx_pct", x_pct + w_pct * 0.5))
    cy_pct = float(note.get("cy_pct", y_pct + h_pct * 0.5))

    x0_3d, z0_3d = map_2d_pct_to_3d_xz(project_id, sheet_id, x_pct, y_pct)
    x1_3d, z1_3d = map_2d_pct_to_3d_xz(project_id, sheet_id, x_pct + w_pct, y_pct + h_pct)
    px_3d, pz_3d = map_2d_pct_to_3d_xz(project_id, sheet_id, cx_pct, cy_pct)

    xa, xb = round(min(x0_3d, x1_3d), 2), round(max(x0_3d, x1_3d), 2)
    za, zb = round(min(z0_3d, z1_3d), 2), round(max(z0_3d, z1_3d), 2)
    if xb - xa < 1.2:
        mid_x = 0.5 * (xa + xb)
        xa, xb = round(mid_x - 0.6, 2), round(mid_x + 0.6, 2)
    if zb - za < 1.2:
        mid_z = 0.5 * (za + zb)
        za, zb = round(mid_z - 0.6, 2), round(mid_z + 0.6, 2)

    px_3d = round(max(xa + 0.1, min(xb - 0.1, px_3d)), 2)
    pz_3d = round(max(za + 0.1, min(zb - 0.1, pz_3d)), 2)

    is_facade = str(note.get("ve_pillar") or "") == "FACADE" or "-FAC-" in str(note.get("id") or "")
    if is_facade:
        floor_id = "all"
        y0, y1 = 0.0, 28.5
        py_3d = 14.5
        # Facade camera looks from outside toward the facade
        title = str(note.get("title") or "") + " " + str(note.get("room_name") or "")
        if "צפונ" in title:
            theta, phi, radius = -1.57, 1.05, 42.0
        elif "מערב" in title:
            theta, phi, radius = 3.08, 1.05, 42.0
        elif "מזרח" in title:
            theta, phi, radius = 0.08, 1.05, 42.0
        else:
            theta, phi, radius = 1.57, 1.05, 42.0
    else:
        floor_id = tf["floor_id"]
        y0 = round(float(tf["z_floor"]), 2)
        y1 = round(float(tf["z_ceil"]), 2)
        py_3d = round(y0 + 1.20, 2)
        span = max(xb - xa, zb - za)
        radius = round(max(13.5, min(32.0, span * 1.45 + 9.0)), 1)
        theta = 1.57
        phi = 0.50

    return {
        "floor_id": floor_id,
        "slice_mode": "cumulative" if is_facade else "single",
        "bbox_3d": [xa, za, xb, zb, y0, y1],
        "pin_3d": [px_3d, py_3d, pz_3d],
        "camera": {
            "target": [px_3d, round(0.5 * (y0 + y1), 2), pz_3d],
            "radius": radius,
            "theta": theta,
            "phi": phi,
            "ortho": False,
        },
        "callout_he": f"#{note.get('pin_num')}: {note.get('room_name', '')} — {note.get('title', '')}",
        "category_3d": note.get("ve_category") or note.get("status", "PASS"),
        "Elements_3d": [str(note.get("room_name") or note.get("title") or "")],
    }


def _classify_wing(norm_u: float, norm_v: float) -> str:
    """Classifies normalized position (u, v) in [0..1] into horizontal & vertical wing labels."""
    if norm_u < 0.43:
        h_wing = "WEST_LEFT"
    elif norm_u > 0.57:
        h_wing = "EAST_RIGHT"
    else:
        h_wing = "CENTER"

    if norm_v < 0.42:
        v_wing = "NORTH_TOP"
    elif norm_v > 0.58:
        v_wing = "SOUTH_BOTTOM"
    else:
        v_wing = "MID"
    return f"{h_wing}:{v_wing}"


def verify_and_lock_project_positions(payload: dict, strict_sync: bool = True) -> dict:
    """
    Audits, aligns, and locks every note's 2D and 3D positions in `payload`:
    1. Ensures 2D center (`cx_pct`, `cy_pct`) matches (`x_pct + w_pct/2`, `y_pct + h_pct/2`).
    2. Ensures `pin_3d` lies inside `bbox_3d`.
    3. Ensures 3D horizontal position (`pin_3d[0], pin_3d[2]`) matches the calibrated 2D position
       and lies in the exact same wing/quadrant (Left/Center/Right & Top/Mid/Bottom).
    4. Locks camera orientation (`theta in [+1.25, +1.85]`, `phi in [0.42, 0.62]`) for all floor-sliced
       notes so the 3D view never flips Left↔Right relative to the 2D plan.
    5. Attaches `position_lock` to every note and `spatial_lock_summary` to `payload`.
    """
    if not isinstance(payload, dict):
        return payload

    pid = str(payload.get("project_id") or "")
    notes = payload.get("notes") or []

    locked_count = 0
    wing_match_count = 0
    orient_locked_count = 0
    drifts = []
    note_hashes = []

    for note in notes:
        nid = str(note.get("id") or "")
        sheet_id = str(note.get("sheet_id") or "")
        tf = get_sheet_transform(pid, sheet_id)
        px0, py0, px1, py1 = tf["rect_2d_pct"]
        wx0, wz0, wx1, wz1 = tf["rect_3d_xz"]

        # 1. Lock 2D box internal consistency
        x_pct = round(float(note.get("x_pct", 35.0)), 2)
        y_pct = round(float(note.get("y_pct", 35.0)), 2)
        w_pct = round(max(2.5, float(note.get("w_pct", 15.0))), 2)
        h_pct = round(max(2.5, float(note.get("h_pct", 15.0))), 2)
        cx_pct = round(x_pct + w_pct * 0.5, 2)
        cy_pct = round(y_pct + h_pct * 0.5, 2)
        note["x_pct"] = x_pct
        note["y_pct"] = y_pct
        note["w_pct"] = w_pct
        note["h_pct"] = h_pct
        note["cx_pct"] = cx_pct
        note["cy_pct"] = cy_pct

        # Expected 3D position from calibrated 2D sheet transform
        exp_x, exp_z = map_2d_pct_to_3d_xz(pid, sheet_id, cx_pct, cy_pct)
        u_2d = (cx_pct - px0) / max(1e-6, (px1 - px0))
        v_2d = (cy_pct - py0) / max(1e-6, (py1 - py0))

        sp = note.get("spatial_3d")
        if not sp or not isinstance(sp, dict):
            sp = compute_calibrated_spatial_3d(pid, note)
            note["spatial_3d"] = sp

        bbox = list(sp.get("bbox_3d") or [-2.0, 0.0, -2.0, 2.0, 3.0, 2.0])
        pin = list(sp.get("pin_3d") or [exp_x, 1.2, exp_z])
        cam = dict(sp.get("camera") or {})
        floor_id = str(sp.get("floor_id") or tf["floor_id"])

        # Normalize bbox ordering: bbox_3d is [x0, z0, x1, z1, y0_elev, y1_elev]
        bx0, bx1 = min(float(bbox[0]), float(bbox[2])), max(float(bbox[0]), float(bbox[2]))
        bz0, bz1 = min(float(bbox[1]), float(bbox[3])), max(float(bbox[1]), float(bbox[3]))
        by0, by1 = min(float(bbox[4]), float(bbox[5])), max(float(bbox[4]), float(bbox[5]))

        # 2. Check normalized 2D vs 3D drift and wing match
        u_3d = (float(pin[0]) - wx0) / max(1e-6, (wx1 - wx0))
        v_3d = (float(pin[2]) - wz0) / max(1e-6, (wz1 - wz0))

        # Check if 2D and 3D are on opposite sides of the building centerline (u=0.5)
        opposite_h_wing = (u_2d < 0.44 and u_3d > 0.56) or (u_2d > 0.56 and u_3d < 0.44)
        opposite_v_wing = (v_2d < 0.38 and v_3d > 0.62) or (v_2d > 0.62 and v_3d < 0.38)
        raw_drift_pct = math.hypot(u_3d - u_2d, v_3d - v_2d) * 100.0

        is_facade = str(note.get("ve_pillar") or "") == "FACADE" or "-FAC-" in nid or floor_id == "all"

        if strict_sync and not is_facade and (opposite_h_wing or opposite_v_wing or raw_drift_pct > 25.0):
            # Re-anchor 3D bbox & pin to match 2D calibrated location
            cal = compute_calibrated_spatial_3d(pid, note)
            bx0, bz0, bx1, bz1, by0, by1 = cal["bbox_3d"]
            pin = cal["pin_3d"]
            u_3d = (float(pin[0]) - wx0) / max(1e-6, (wx1 - wx0))
            v_3d = (float(pin[2]) - wz0) / max(1e-6, (wz1 - wz0))

        # Ensure pin_3d is inside bbox_3d (allow exterior offset for facade callouts)
        pad_xz = -0.60 if is_facade else 0.05
        pin[0] = round(max(bx0 + pad_xz, min(bx1 - pad_xz, float(pin[0]))), 2)
        pin[1] = round(max(by0 + 0.05, min(by1 + 0.80, float(pin[1]))), 2)
        pin[2] = round(max(bz0 + pad_xz, min(bz1 - pad_xz, float(pin[2]))), 2)
        bbox = [round(bx0, 2), round(bz0, 2), round(bx1, 2), round(bz1, 2), round(by0, 2), round(by1, 2)]
        sp["bbox_3d"] = bbox
        sp["pin_3d"] = pin

        # 3. Lock Camera Orientation so 3D floor plan matches 2D floor plan (South looking North: theta in [+1.25, +1.85])
        theta = float(cam.get("theta", 1.57))
        phi = float(cam.get("phi", 0.50))
        radius = float(cam.get("radius", 16.0))
        if not is_facade:
            if theta < 1.20 or theta > 1.95:
                theta = 1.57
            if phi < 0.38 or phi > 0.68:
                phi = 0.50
            cam["target"] = [pin[0], round(0.5 * (by0 + by1), 2), pin[2]]
        cam["theta"] = round(theta, 2)
        cam["phi"] = round(phi, 2)
        cam["radius"] = round(radius, 1)
        cam["ortho"] = bool(cam.get("ortho", False))
        sp["camera"] = cam

        # Recompute final metrics after lock
        u_3d = (float(pin[0]) - wx0) / max(1e-6, (wx1 - wx0))
        v_3d = (float(pin[2]) - wz0) / max(1e-6, (wz1 - wz0))
        drift_pct = round(math.hypot(u_3d - u_2d, v_3d - v_2d) * 100.0, 2)
        drifts.append(drift_pct)

        wing_2d = _classify_wing(u_2d, v_2d)
        wing_3d = _classify_wing(u_3d, v_3d)
        # Wing match is true if horizontal & vertical sides do not oppose each other
        h_ok = not ((u_2d < 0.45 and u_3d > 0.55) or (u_2d > 0.55 and u_3d < 0.45))
        v_ok = not ((v_2d < 0.40 and v_3d > 0.60) or (v_2d > 0.60 and v_3d < 0.40))
        wing_match = bool(h_ok and v_ok) or is_facade

        lock_payload_str = json.dumps(
            {
                "id": nid,
                "sheet_id": sheet_id,
                "box_2d": [x_pct, y_pct, w_pct, h_pct, cx_pct, cy_pct],
                "floor_id": floor_id,
                "bbox_3d": bbox,
                "pin_3d": pin,
                "cam_theta": cam["theta"],
                "cam_phi": cam["phi"],
            },
            sort_keys=True,
        )
        lock_hash = hashlib.sha256(lock_payload_str.encode("utf-8")).hexdigest()[:12]
        note_hashes.append(lock_hash)

        lock_obj = {
            "locked": True,
            "verified": True,
            "lock_version": LOCK_VERSION,
            "lock_hash": lock_hash,
            "sheet_id": sheet_id,
            "floor_id": floor_id,
            "wing_2d": wing_2d,
            "wing_3d": wing_3d,
            "wing_match": wing_match,
            "expected_3d_xz": [exp_x, exp_z],
            "actual_3d_xz": [pin[0], pin[2]],
            "normalized_drift_pct": drift_pct,
            "orientation_locked": True,
            "camera_theta": cam["theta"],
        }
        note["position_lock"] = lock_obj
        sp["position_lock"] = lock_obj

        locked_count += 1
        if wing_match:
            wing_match_count += 1
        orient_locked_count += 1

    master_hash = hashlib.sha256("|".join(note_hashes).encode("utf-8")).hexdigest()[:16]
    payload["spatial_lock_summary"] = {
        "lock_version": LOCK_VERSION,
        "project_id": pid,
        "total_notes": len(notes),
        "locked_notes": locked_count,
        "wing_match_count": wing_match_count,
        "orientation_locked_count": orient_locked_count,
        "max_drift_pct": round(max(drifts) if drifts else 0.0, 2),
        "avg_drift_pct": round(sum(drifts) / len(drifts) if drifts else 0.0, 2),
        "verified_100_pct": (locked_count == len(notes) and wing_match_count == len(notes)),
        "registry_hash": master_hash,
    }
    return payload


def build_and_verify_master_registry(write_file: bool = True) -> dict:
    """
    Loads all 6 projects via `project_analyzer_service.analyze_project_by_query()`,
    runs full 2D↔3D position verification & locking, and writes `spatial_lock_registry.json`.
    """
    from project_analyzer_service import analyze_project_by_query

    project_ids = ["feierberg3", "hafetz44", "yatkovski7", "pines48", "kkl10", "kitroni37", "sharett26"]
    registry = {
        "lock_version": LOCK_VERSION,
        "total_projects": len(project_ids),
        "total_notes": 0,
        "verified_100_pct": True,
        "projects": {},
    }

    for pid in project_ids:
        data = analyze_project_by_query(pid)
        summary = data.get("spatial_lock_summary") or {}
        notes = data.get("notes") or []
        registry["total_notes"] += len(notes)
        if not summary.get("verified_100_pct", False):
            registry["verified_100_pct"] = False

        registry["projects"][pid] = {
            "summary": summary,
            "notes": {
                str(n.get("id")): {
                    "pin_num": n.get("pin_num"),
                    "sheet_id": n.get("sheet_id"),
                    "box_2d": [n.get("x_pct"), n.get("y_pct"), n.get("w_pct"), n.get("h_pct"), n.get("cx_pct"), n.get("cy_pct")],
                    "floor_id": n.get("spatial_3d", {}).get("floor_id"),
                    "bbox_3d": n.get("spatial_3d", {}).get("bbox_3d"),
                    "pin_3d": n.get("spatial_3d", {}).get("pin_3d"),
                    "camera": n.get("spatial_3d", {}).get("camera"),
                    "position_lock": n.get("position_lock"),
                }
                for n in notes
            },
        }

    if write_file:
        with open(REGISTRY_PATH, "w", encoding="utf-8", newline="\n") as f:
            json.dump(registry, f, ensure_ascii=False, indent=2)

    return registry


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    reg = build_and_verify_master_registry(write_file=True)
    print(f"=== Spatial 2D<->3D Lock Registry ({reg['lock_version']}) ===")
    print(f"Total Projects: {reg['total_projects']} | Total Notes Locked: {reg['total_notes']} | Verified 100%: {reg['verified_100_pct']}")
    for pid, pinfo in reg["projects"].items():
        s = pinfo["summary"]
        print(
            f"  [{pid:11s}] locked={s['locked_notes']}/{s['total_notes']} | "
            f"wing_match={s['wing_match_count']}/{s['total_notes']} | "
            f"avg_drift={s['avg_drift_pct']:.2f}% | max_drift={s['max_drift_pct']:.2f}% | "
            f"hash={s['registry_hash']}"
        )
    if not reg["verified_100_pct"]:
        sys.exit(1)
