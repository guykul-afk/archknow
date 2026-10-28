# -*- coding: utf-8 -*-
import os, sys, json, shutil

sys.stdout.reconfigure(encoding='utf-8')

ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\805acd69-24a6-4e01-9e0e-9e19346156a0"
SCRATCH_DIR = os.path.join(ARTIFACT_DIR, "scratch")
THREE_JS_PATH = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\_shared_engine\three.min.js"
PROJECT_DIR = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\פאירברג 3 פתח תקווה"
DATA_DIR = os.path.join(PROJECT_DIR, "data")

with open(THREE_JS_PATH, "r", encoding="utf-8") as f:
    three_js_code = f.read()

with open(os.path.join(DATA_DIR, "feierberg3_extracted_plans.json"), "r", encoding="utf-8") as f:
    plans_data = json.load(f)

with open(os.path.join(DATA_DIR, "feierberg3_units_crm.json"), "r", encoding="utf-8") as f:
    crm_data = json.load(f)

# Enrich CRM units & parking stalls so both snake_case and camelCase fields are present
parking_stalls = []
for b_key, level_id, z_elev in [("basement_1", "b1", -4.78), ("basement_2", "b2", -7.78)]:
    for item in plans_data.get(b_key, {}).get("furn_items", []):
        if item.get("kind") == "car_stall":
            pid = item.get("id", "P1")
            pnum = int(str(pid).replace("P", ""))
            cx = round(0.5 * (item["x0"] + item["x1"]), 2)
            cy = round(0.5 * (item["y0"] + item["y1"]), 2)
            w = round(abs(item["x1"] - item["x0"]), 2)
            d = round(abs(item["y1"] - item["y0"]), 2)
            parking_stalls.append({
                "id": pid,
                "num": pnum,
                "level": level_id,
                "z": z_elev,
                "x": cx,
                "y": cy,
                "w": w,
                "d": d
            })
parking_stalls.sort(key=lambda s: s["num"])
crm_data["parking_stalls"] = parking_stalls
stall_by_num = {s["num"]: s for s in parking_stalls}

for u in crm_data.get("units", []):
    uid = u["unit_id"]
    fl = u["floor"]
    wing_raw = u["wing"]  # 'west' or 'east'
    wing_code = ("PH_W" if wing_raw == "west" else "PH_E") if fl == 9 else ("W" if wing_raw == "west" else "E")
    st_Info = stall_by_num.get(uid if uid <= 18 else 19, {"x": -4.0, "y": 4.5, "level": "b1", "z": -4.78})

    u["id"] = f"apt_{uid}"
    u["aptNum"] = uid
    u["floorNum"] = fl
    u["floorId"] = f"f{fl}"
    u["floorLabel"] = u["floor_label"]
    u["name"] = f"דירה #{uid}"
    u["shortBadge"] = f"דירה #{uid}"
    u["wing"] = wing_code
    u["typeHe"] = u["type"]
    u["area"] = u["area_gross_sqm"]
    u["balcony"] = u["balcony_sqm"]
    u["price"] = u["price_nis"]
    u["status"] = "available" if u["status"] == "available" else ("owner" if "תמורה" in u.get("status_he", "") else "available")
    u["statusHe"] = u["status_he"]
    u["parkingNum"] = uid if uid <= 16 else ("17+18" if uid == 17 else "19")
    u["parkingLevel"] = st_Info["level"]
    u["parkingX"] = st_Info["x"]
    u["parkingY"] = st_Info["y"]
    u["z0"] = u["elevation_m"]
    u["z1"] = round(u["elevation_m"] + u["ceiling_h_m"], 2)
    bx0, bx1 = u["bbox_x"]
    bz0, bz1 = u["bbox_z"]
    u["bbox"] = [bx0, bz0, bx1, bz1]
    u["bx"] = round(-6.8 if wing_raw == "west" else 6.8, 2)
    u["by"] = round(5.2 if fl <= 8 else 3.8, 2)
    u["bz"] = round(u["z0"] + 1.6, 2)
    u["balcPt"] = [-2.2, 5.0] if wing_raw == "west" else [5.4, 5.0]
    if fl == 9:
        u["balcPt"] = [-5.5, 3.8] if wing_raw == "west" else [6.2, 3.8]
    u["lookDir"] = "S"

for p in [
    os.path.join(SCRATCH_DIR, "feierberg3_units_crm.json"),
    os.path.join(DATA_DIR, "feierberg3_units_crm.json"),
]:
    with open(p, "w", encoding="utf-8") as f:
        json.dump(crm_data, f, ensure_ascii=False, indent=2)

with open(os.path.join(DATA_DIR, "unified_feierberg3_3d_map.json"), "r", encoding="utf-8") as f:
    unified_map_data = json.load(f)

with open(os.path.join(DATA_DIR, "feierberg3_spatial_map_data.json"), "r", encoding="utf-8") as f:
    spatial_gis_data = json.load(f)

wide_gmaps_data_uri = unified_map_data["outer_z15"]["data_uri"]
inner_gmaps_data_uri = unified_map_data["inner_z17"]["data_uri"]
closeup_gmaps_data_uri = unified_map_data["closeup_z19"]["data_uri"]
outer_span_m = unified_map_data["outer_z15"]["world_span_m"]
inner_span_m = unified_map_data["inner_z17"]["world_span_m"]
closeup_span_m = unified_map_data["closeup_z19"]["world_span_m"]

plans_json_str = json.dumps(plans_data, ensure_ascii=False, separators=(',', ':'))
crm_json_str = json.dumps(crm_data, ensure_ascii=False, separators=(',', ':'))
spatial_pois_json = json.dumps(spatial_gis_data["pois"], ensure_ascii=False, separators=(',', ':'))

HTML_PART1 = r"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>פאירברג 3, פתח תקווה — מערכת שיווק, מכירות והדמיה תלת-ממדית אינטראקטיבית (1:50 BIM, CRM & GIS)</title>
  <style>
    :root {
      --background: #ffffff;
      --foreground: #0f172a;
      --card: #ffffff;
      --card-foreground: #0f172a;
      --primary: #2563eb;
      --primary-foreground: #ffffff;
      --secondary: #f1f5f9;
      --secondary-foreground: #1e293b;
      --muted: #f8fafc;
      --muted-foreground: #475569;
      --border: #cbd5e1;
    }
    * { box-sizing: border-box; }
    html, body {
      margin: 0; padding: 0; width: 100%; height: 100%;
      overflow: hidden; user-select: none;
      background-color: #ffffff; color: #0f172a;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    #viewport-container { position: relative; width: 100%; height: 100vh; overflow: hidden; background: #ffffff; }
    canvas { display: block; width: 100%; height: 100%; cursor: grab; }
    canvas:active { cursor: grabbing; }
    .glass-panel {
      background: rgba(255, 255, 255, 0.94);
      border: 1px solid rgba(203, 213, 225, 0.85);
      color: #0f172a;
      box-shadow: 0 12px 32px -6px rgba(15, 23, 42, 0.14), 0 4px 12px -2px rgba(15, 23, 42, 0.08);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
    }
    .top-header {
      position: absolute; top: 12px; right: 14px; left: 14px; z-index: 30;
      display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
      gap: 10px; border-radius: 14px; padding: 8px 16px;
    }
    .dropdown-drawer {
      display: none; position: absolute; top: 68px; right: 14px; z-index: 28;
      width: 390px; max-height: calc(100vh - 90px); overflow-y: auto;
      border-radius: 14px; padding: 14px; animation: fadeSlideDown 0.18s ease-out;
    }
    .dropdown-drawer.open { display: block; }
    @keyframes fadeSlideDown {
      from { opacity: 0; transform: translateY(-6px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    .bottom-right-sections {
      position: absolute; bottom: 14px; right: 14px; z-index: 26;
      width: 350px; max-height: calc(100vh - 90px); overflow-y: auto;
      border-radius: 16px; padding: 12px 14px;
      border: 1px solid rgba(147, 197, 253, 0.9);
      background: rgba(255, 255, 255, 0.95);
      box-shadow: 0 16px 36px -6px rgba(15, 23, 42, 0.18), 0 4px 12px rgba(37, 99, 235, 0.10);
      backdrop-filter: blur(14px); transition: all 0.2s ease;
    }
    .bottom-right-sections.collapsed .sections-body { display: none; }
    .menu-trigger-btn {
      display: inline-flex; align-items: center; gap: 6px; border-radius: 10px;
      border: 1px solid #cbd5e1; background: #ffffff; color: #0f172a;
      padding: 7px 12px; font-size: 12px; font-weight: 700; cursor: pointer;
      transition: all 0.15s ease; box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
    }
    .menu-trigger-btn:hover { background: #f1f5f9; border-color: #94a3b8; }
    .menu-trigger-btn.open { background: #1e3a8a; border-color: #1d4ed8; color: #ffffff; box-shadow: 0 0 0 2px #93c5fd; }
    .menu-trigger-btn.lux-trigger { background: linear-gradient(135deg, #b45309 0%, #d97706 100%); border-color: #92400e; color: #ffffff; }
    .menu-trigger-btn.lux-trigger:hover { background: linear-gradient(135deg, #92400e 0%, #b45309 100%); }
    .menu-trigger-btn.lux-trigger.open { box-shadow: 0 0 0 2px #fde68a, 0 4px 12px rgba(180, 83, 9, 0.35); }
    .menu-trigger-btn.emerald-trigger { background: linear-gradient(135deg, #047857 0%, #059669 100%); border-color: #065f46; color: #ffffff; }
    .menu-trigger-btn.emerald-trigger:hover { background: linear-gradient(135deg, #065f46 0%, #047857 100%); }
    .menu-trigger-btn.emerald-trigger.open { box-shadow: 0 0 0 2px #6ee7b7, 0 4px 12px rgba(5, 150, 105, 0.35); }
    .ui-btn {
      display: inline-flex; align-items: center; justify-content: center;
      border-radius: 8px; border: 1px solid #cbd5e1; background: #f8fafc;
      color: #0f172a; padding: 6px 10px; font-size: 12px; font-weight: 600;
      cursor: pointer; transition: all 0.15s ease;
    }
    .ui-btn:hover { background: #e2e8f0; border-color: #94a3b8; }
    .ui-btn.active { background: #2563eb; border-color: #1d4ed8; color: #ffffff; }
    .ui-btn-lux {
      background: linear-gradient(135deg, #b45309 0%, #d97706 100%);
      border-color: #92400e; color: #ffffff; box-shadow: 0 2px 8px rgba(180, 83, 9, 0.25);
    }
    .ui-btn-lux:hover { background: linear-gradient(135deg, #92400e 0%, #b45309 100%); border-color: #78350f; color: #ffffff; }
    .ui-btn-lux.active {
      background: linear-gradient(135deg, #78350f 0%, #b45309 100%);
      border-color: #451a03; color: #ffffff; box-shadow: 0 0 0 2px #fde68a, 0 4px 12px rgba(180, 83, 9, 0.35);
    }
    .aptc-hud {
      position: absolute; bottom: 14px; left: 14px; right: 374px; z-index: 25;
      display: none; flex-direction: column; gap: 8px; border-radius: 14px;
      padding: 10px 14px; background: rgba(255, 252, 245, 0.95); border: 1px solid #e6d5be;
      box-shadow: 0 12px 30px -6px rgba(15, 23, 42, 0.16); backdrop-filter: blur(14px);
    }
    .room-chip {
      display: inline-flex; align-items: center; gap: 5px; border-radius: 8px;
      border: 1px solid #dec9ad; background: #ffffff; color: #451a03;
      padding: 5px 10px; font-size: 11.5px; font-weight: 700; cursor: pointer; transition: all 0.15s ease;
    }
    .room-chip:hover { background: #fef3c7; border-color: #d97706; }
    .room-chip.active { background: #b45309; border-color: #78350f; color: #ffffff; }
    .walk-dpad-btn {
      width: 32px; height: 30px; display: inline-flex; align-items: center; justify-content: center;
      border-radius: 7px; border: 1px solid #d6c7b2; background: #ffffff; color: #1e293b;
      font-size: 13px; font-weight: 800; cursor: pointer; user-select: none;
    }
    .walk-dpad-btn:hover { background: #fef3c7; border-color: #d97706; }
    .walk-dpad-btn:active { background: #b45309; color: #ffffff; }
    .section-box { border-radius: 10px; border: 1px solid #e2e8f0; background: #f8fafc; padding: 10px; margin-bottom: 8px; }
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
    .flex-between { display: flex; align-items: center; justify-content: space-between; }
    .layer-row {
      display: flex; align-items: center; justify-content: space-between;
      border-radius: 8px; border: 1px solid #e2e8f0; background: #ffffff;
      padding: 5px 10px; font-size: 12px; color: #0f172a; margin-bottom: 4px; cursor: pointer;
    }
    .callout-pill {
      position: absolute; transform: translate(-50%, -50%); white-space: nowrap;
      border-radius: 6px; border: 1px solid #cbd5e1; background: rgba(255, 255, 255, 0.94);
      color: #0f172a; padding: 3px 8px; font-size: 11px; font-weight: 700;
      box-shadow: 0 2px 6px rgba(15, 23, 42, 0.14); pointer-events: none; transition: opacity 0.15s ease;
    }
    .callout-pill.b44 { background: #1e3a8a; color: #ffffff; border-color: #1d4ed8; }
    .callout-pill.ph  { background: #b45309; color: #ffffff; border-color: #d97706; }
    .callout-pill.street { background: #0f172a; color: #fde047; border-color: #334155; }
    .cad-badge { font-variant-numeric: tabular-nums; }
    input[type="range"] { width: 100%; cursor: pointer; accent-color: #2563eb; }
    .status-badge {
      display: inline-flex; align-items: center; gap: 4px; padding: 2px 7px;
      border-radius: 999px; font-size: 10px; font-weight: 800; white-space: nowrap;
    }
    .status-available { background: #dcfce7; color: #166534; border: 1px solid #86efac; }
    .status-owner     { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }
    .unit-sales-card {
      display: none; position: absolute; top: 72px; left: 16px; z-index: 29;
      width: 380px; max-height: calc(100vh - 96px); overflow-y: auto;
      background: rgba(15, 23, 42, 0.96); color: #ffffff; border: 1px solid #334155;
      border-radius: 16px; padding: 14px; box-shadow: 0 20px 44px rgba(0, 0, 0, 0.45); backdrop-filter: blur(14px);
    }
    .pkg-card-btn {
      display: flex; flex-direction: column; align-items: flex-start; gap: 3px;
      border-radius: 8px; border: 1px solid #cbd5e1; background: #ffffff;
      padding: 6px 8px; cursor: pointer; text-align: right; transition: all 0.15s ease;
    }
    .pkg-card-btn:hover { background: #f8fafc; border-color: #64748b; }
    .pkg-card-btn.active { background: #eff6ff; border-color: #2563eb; box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.25); }
    .mode-switch { display: flex; background: #f1f5f9; padding: 3px; border-radius: 8px; gap: 4px; margin-bottom: 8px; }
    .mode-switch button {
      flex: 1; border: none; background: transparent; padding: 5px 6px;
      border-radius: 6px; font-size: 11px; font-weight: 700; color: #475569; cursor: pointer;
    }
    .mode-switch button.active { background: #ffffff; color: #2563eb; box-shadow: 0 1px 3px rgba(0,0,0,0.12); }
  </style>
</head>
<body class="antialiased">
  <div id="viewport-container">
    <canvas id="cad-canvas"></canvas>
    <div id="labels-container" style="pointer-events:none;position:absolute;inset:0;overflow:hidden;z-index:6;"></div>
    <div id="gis-labels-container" style="pointer-events:none;position:absolute;inset:0;overflow:hidden;z-index:8;"></div>
    <div id="units-labels-container" style="pointer-events:none;position:absolute;inset:0;overflow:hidden;z-index:12;"></div>
    <div id="measure-labels-container" style="pointer-events:none;position:absolute;inset:0;overflow:hidden;z-index:18;"></div>

    <div id="gis-active-card" style="display:none;position:absolute;bottom:20px;left:20px;z-index:28;width:330px;background:rgba(15,23,42,0.96);color:#ffffff;border:1px solid #334155;border-radius:14px;padding:14px;box-shadow:0 12px 28px rgba(0,0,0,0.35);backdrop-filter:blur(10px);"></div>
    <div id="unit-sales-card" class="unit-sales-card"></div>

    <div id="measure-hud" style="display:none;position:absolute;top:72px;left:50%;transform:translateX(-50%);z-index:27;background:rgba(15,23,42,0.94);color:#ffffff;border:1px solid #38bdf8;border-radius:999px;padding:6px 16px;font-size:12px;font-weight:700;box-shadow:0 8px 24px rgba(0,0,0,0.35);align-items:center;gap:10px;">
      <span>📏 <b>מד טווח לייזר 3D פעיל</b>: לחץ על 2 נקודות במודל למדידת מרחק מדויק</span>
      <span id="measure-last-val" style="background:#0284c7;color:#ffffff;padding:2px 8px;border-radius:999px;font-weight:800;">מוכן למדידה</span>
      <button id="btn-clear-measures" class="ui-btn" style="padding:2px 8px;font-size:11px;background:#334155;color:#ffffff;border-color:#475569;">נקה מדידות</button>
      <button id="btn-close-measure" class="ui-btn" style="padding:2px 7px;font-size:11px;background:#ef4444;color:#ffffff;border-color:#dc2626;">✕</button>
    </div>

    <header class="glass-panel top-header">
      <div style="display:flex;align-items:center;gap:10px;">
        <div style="display:flex;height:36px;width:44px;align-items:center;justify-content:center;border-radius:9px;background:linear-gradient(135deg,#0f172a,#1e3a8a);color:#fde047;font-weight:900;font-size:11.5px;border:1px solid #3b82f6;">
          F3
        </div>
        <div>
          <div style="display:flex;align-items:center;gap:7px;flex-wrap:wrap;">
            <h1 style="margin:0;font-size:14px;font-weight:800;color:#0f172a;">קבוצת קולסקי · פאירברג 3, פתח תקווה</h1>
            <span style="border-radius:6px;border:1px solid #dec9ad;background:#fef3c7;padding:1px 7px;font-size:10px;font-weight:800;color:#92400e;">אלישע רובין אדריכלים · פורטל שיווק ומכירות 3D (18 יח"ד · 19 חניות · גוש 6387 חלקה 193)</span>
          </div>
        </div>
      </div>

      <div style="display:flex;flex-wrap:wrap;align-items:center;gap:5px;" id="view-buttons">
        <button data-view="iso_south" id="btn-top-bldg" class="view-btn ui-btn" title="מבט חוץ אדריכלי על הבניין מרחוב פאירברג 3 (חזית דרומית)">
          🏢 מבט הבניין
        </button>
        <button data-view="gmaps_regional" id="btn-top-gis-map" class="view-btn ui-btn active" title="מבט רחפן על הבניין יושב על מפת העיר פתח תקווה ו-28 מוקדי הסביבה">
          🗺️ מפת סביבה
        </button>
        <button id="btn-top-units-3d" class="ui-btn" style="border-color:#10b981;color:#065f46;background:#ecfdf5;font-weight:800;" title="הצג/הסתר סימון 18 דירות תלת-ממדי לפי זמינות ומחיר על חזיתות הבניין">
          🏢 סימון דירות 3D
        </button>
        <button id="btn-top-radii" class="ui-btn active" title="הדלק/כבה 8 מעגלי מרחק וזמני הליכה סביב פאירברג 3">
          ⭕ רדיוסים: פעיל
        </button>
        <button id="btn-top-pois" class="ui-btn active" title="הדלק/כבה 28 מיקומים ומוקדי סביבה בפתח תקווה">
          📍 מיקומים: פעיל
        </button>
        <button id="btn-top-night" class="ui-btn" title="מצב תאורת לילה / שעת הזהב עם תאורת פנים ומרפסות חמה">
          🌙 מצב לילה
        </button>
        <button id="btn-top-measure" class="ui-btn" title="מד טווח לייזר תלת-ממדי למדידת מרחקים בדירה ובבניין">
          📏 מדידה
        </button>

        <button data-drawer="drawer-units" class="menu-trigger-btn emerald-trigger">
          <span>🏷️ קטלוג דירות ומחירים (18)</span>
          <span style="font-size:10px;">▾</span>
        </button>
        <button data-drawer="drawer-apartments" class="menu-trigger-btn lux-trigger">
          <span>✨ סיור פנים מרוהט 3D ונוף מהמרפסת</span>
          <span style="font-size:10px;">▾</span>
        </button>
        <button data-drawer="drawer-gis" class="menu-trigger-btn">
          <span>📍 מוקדי סביבה (28)</span>
          <span style="font-size:10px;">▾</span>
        </button>
        <button data-drawer="drawer-settings" class="menu-trigger-btn">
          <span>⚙️ עיצוב ושכבות</span>
          <span style="font-size:10px;">▾</span>
        </button>
      </div>
    </header>

    <!-- DRAWER 0: 18 UNITS CATALOG & LIVE CRM -->
    <div id="drawer-units" class="glass-panel dropdown-drawer" style="width:435px;">
      <div class="flex-between" style="margin-bottom:8px;border-bottom:1px solid #e2e8f0;padding-bottom:6px;">
        <div>
          <div style="font-size:13px;font-weight:800;color:#065f46;">🏷️ קטלוג 18 הדירות והמחירון הרשמי — פאירברג 3</div>
          <div style="font-size:11px;color:#64748b;">16 דירות 4 חד' (קומות 1–8) + 2 דופלקס-פנטהאוז 5 חד' (קומות 9–10)</div>
        </div>
        <button data-close-drawer class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
      </div>

      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin-bottom:8px;text-align:center;">
        <div style="background:#ecfdf5;border:1px solid #a7f3d0;border-radius:8px;padding:5px;">
          <div style="font-size:10px;color:#065f46;font-weight:700;">🟢 מלאי קולסקי זמין</div>
          <div id="kpi-avail-count" style="font-size:14px;font-weight:900;color:#047857;">12 דירות</div>
        </div>
        <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:5px;">
          <div style="font-size:10px;color:#1e40af;font-weight:700;">🏢 סה"כ בפרויקט</div>
          <div style="font-size:14px;font-weight:900;color:#1d4ed8;">18 יח"ד · 19 חניות</div>
        </div>
        <div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:8px;padding:5px;">
          <div style="font-size:10px;color:#475569;font-weight:700;">🔒 דירות בעלים</div>
          <div id="kpi-owner-count" style="font-size:14px;font-weight:900;color:#334155;">6 דירות</div>
        </div>
      </div>

      <div class="grid-2" style="margin-bottom:8px;">
        <button id="btn-drawer-units-3d" class="ui-btn" style="background:#059669;color:#ffffff;border-color:#047857;font-weight:800;">
          🏢 הדגש דירות 3D על הבניין
        </button>
        <button id="btn-toggle-prices" class="ui-btn active" style="font-weight:700;">
          👁️ מחירים: מוצג
        </button>
      </div>

      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:6px;" id="unit-bldg-filters">
        <button data-ubldg="all" class="unit-bldg-chip ui-btn active" style="padding:3px 8px;font-size:10px;">כל הדירות (18)</button>
        <button data-ubldg="W" class="unit-bldg-chip ui-btn" style="padding:3px 8px;font-size:10px;">אגף מערבי · 105.5 מ"ר (8)</button>
        <button data-ubldg="E" class="unit-bldg-chip ui-btn" style="padding:3px 8px;font-size:10px;">אגף מזרחי · 85.5 מ"ר (8)</button>
        <button data-ubldg="PH_W" class="unit-bldg-chip ui-btn" style="padding:3px 8px;font-size:10px;">👑 דופלקס מערבי #17</button>
        <button data-ubldg="PH_E" class="unit-bldg-chip ui-btn" style="padding:3px 8px;font-size:10px;">👑 דופלקס מזרחי #18</button>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:6px;" id="unit-status-filters">
        <button data-ustatus="all" class="unit-status-chip ui-btn active" style="padding:3px 8px;font-size:10px;">כל הסטטוסים (18)</button>
        <button data-ustatus="available" class="unit-status-chip ui-btn" style="padding:3px 8px;font-size:10px;">🟢 פנויות לשיווק קולסקי (12)</button>
        <button data-ustatus="owner" class="unit-status-chip ui-btn" style="padding:3px 8px;font-size:10px;">🔒 דירות בעלים (6)</button>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px;" id="unit-room-filters">
        <button data-urooms="all" class="unit-room-chip ui-btn active" style="padding:3px 8px;font-size:10px;">כל הגדלים</button>
        <button data-urooms="4" class="unit-room-chip ui-btn" style="padding:3px 8px;font-size:10px;">4 חד' קומות 1–8 (85.5–105.5 מ"ר)</button>
        <button data-urooms="5" class="unit-room-chip ui-btn" style="padding:3px 8px;font-size:10px;">5 חד' דופלקס-פנטהאוז ק' 9–10</button>
      </div>

      <div id="units-catalog-list" style="max-height:280px;overflow-y:auto;display:flex;flex-direction:column;gap:5px;padding-left:2px;"></div>
    </div>

    <!-- DRAWER 1: APARTMENT TOURS & BALCONY VIEW SIMULATOR -->
    <div id="drawer-apartments" class="glass-panel dropdown-drawer" style="width:420px;">
      <div class="flex-between" style="margin-bottom:10px;border-bottom:1px solid #e2e8f0;padding-bottom:8px;">
        <div>
          <div style="font-size:13px;font-weight:800;color:#78350f;">✨ סיור פנים מרוהט 3D (קומה 4 לדוגמה) ותוכניות הגשה</div>
          <div style="font-size:11px;color:#64748b;">קומה 4 מרוהטת במלואה בתלת-ממד (3D) · שאר הקומות עם ציור ריהוט דו-ממדי (2D) מההגשה</div>
        </div>
        <button data-close-drawer class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
      </div>

      <div style="font-size:11px;font-weight:800;color:#92400e;margin-bottom:5px;">🛋️ מבט-על חתך Dollhouse (קומה 4 מרוהטת 3D + תוכניות הגשה):</div>
      <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:5px;margin-bottom:8px;">
        <button onclick="openFurnishedDollhouse('f4')" class="ui-btn ui-btn-lux" style="grid-column:span 2;font-weight:900;background:#b45309;color:#ffffff;border-color:#d97706;">✨ קומה 4 לדוגמה — ריהוט 3D מלא (דירות #7 ו-#8 · +12.95)</button>
        <button onclick="openFurnishedDollhouse('kar')" class="ui-btn ui-btn-lux" style="font-weight:800;">🏛️ קומת קרקע ולובי (±0.00)</button>
        <button onclick="openFurnishedDollhouse('f8')" class="ui-btn ui-btn-lux" style="font-weight:800;">☀️ קומה 8 + פרגולות (2D)</button>
        <button onclick="openFurnishedDollhouse('f9')" class="ui-btn" style="background:#0f172a;color:#fde047;border-color:#334155;font-weight:800;">👑 דופלקס ק'9 תחתון (2D)</button>
        <button onclick="openFurnishedDollhouse('f10')" class="ui-btn" style="background:#1e293b;color:#fde047;border-color:#475569;font-weight:800;">👑 דופלקס ק'10 עליון (2D)</button>
      </div>

      <div style="font-size:11px;font-weight:800;color:#1e3a8a;margin-bottom:5px;">🏢 סיור בגוף ראשון (1.68 מ') בקומה 4 המרוהטת 3D ובדופלקסים:</div>
      <div class="grid-2" style="margin-bottom:8px;">
        <button onclick="startPresetInteriorTour(4, 'W')" class="ui-btn ui-btn-lux" style="font-weight:800;">✨ ק'4 · 4 חד' מערבית 3D (#7 · 105.5 מ"ר)</button>
        <button onclick="startPresetInteriorTour(4, 'E')" class="ui-btn ui-btn-lux" style="font-weight:800;">✨ ק'4 · 4 חד' מזרחית 3D (#8 · 85.5 מ"ר)</button>
        <button onclick="startPresetInteriorTour(8, 'W')" class="ui-btn">📐 ק'8 · 4 חד' מערבית (תוכנית 2D)</button>
        <button onclick="startPresetInteriorTour(8, 'E')" class="ui-btn">📐 ק'8 · 4 חד' מזרחית (תוכנית 2D)</button>
        <button onclick="startPresetInteriorTour(9, 'PH_W')" class="ui-btn" style="grid-column:span 2;background:#0f172a;color:#fde047;border-color:#334155;font-weight:800;">👑 ק'9–10 · דופלקס-פנטהאוז מערבי (#17 · תוכנית הגשה 2D)</button>
        <button onclick="startPresetInteriorTour(9, 'PH_E')" class="ui-btn" style="grid-column:span 2;background:#1e293b;color:#fde047;border-color:#475569;font-weight:800;">👑 ק'9–10 · דופלקס-פנטהאוז מזרחי (#18 · תוכנית הגשה 2D)</button>
      </div>

      <div class="section-box" style="margin-bottom:0;">
        <div style="font-size:11px;font-weight:800;color:#451a03;margin-bottom:5px;">🔭 סימולטור "נוף מהמרפסת" לפי קומה מדויקת (קומות 1–10):</div>
        <div style="display:flex;flex-wrap:wrap;gap:4px;" id="balcony-floor-selector">
          <button data-bflr="1" class="ui-btn" style="padding:3px 7px;font-size:10px;">ק'1 (+3.50)</button>
          <button data-bflr="3" class="ui-btn" style="padding:3px 7px;font-size:10px;">ק'3 (+9.80)</button>
          <button data-bflr="5" class="ui-btn" style="padding:3px 7px;font-size:10px;">ק'5 (+16.10)</button>
          <button data-bflr="7" class="ui-btn" style="padding:3px 7px;font-size:10px;">ק'7 (+22.40)</button>
          <button data-bflr="8" class="ui-btn active" style="padding:3px 7px;font-size:10px;">ק'8 (+25.55)</button>
          <button data-bflr="9" class="ui-btn" style="padding:3px 7px;font-size:10px;">דופלקס 9 (+28.87)</button>
          <button data-bflr="10" class="ui-btn" style="padding:3px 7px;font-size:10px;">דופלקס 10 (+32.02)</button>
        </div>
      </div>
    </div>

    <!-- DRAWER 2: 3D GIS SPATIAL MAP & 28 POIS -->
    <div id="drawer-gis" class="glass-panel dropdown-drawer" style="width:410px;">
      <div class="flex-between" style="margin-bottom:8px;border-bottom:1px solid #e2e8f0;padding-bottom:6px;">
        <div>
          <div style="font-size:13px;font-weight:800;color:#1e3a8a;">📍 מפת מרחקים ו-28 מוקדי סביבה ועירוניות (Google Maps)</div>
          <div style="font-size:11px;color:#64748b;">חינוך, קניות, בריאות, תחבורה, מטרו M2 ורק"ל סביב פאירברג 3</div>
        </div>
        <button data-close-drawer class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
      </div>
      <div class="grid-2" style="margin-bottom:8px;">
        <button id="btn-side-gis-regional" class="ui-btn active" style="background:#1e3a8a;color:#ffffff;border-color:#1d4ed8;font-weight:700;">
          🌍 כל המיקומים (2.4 ק"מ)
        </button>
        <button id="btn-side-gis-overview" class="ui-btn" style="background:#dbeafe;color:#1e3a8a;border-color:#93c5fd;font-weight:700;">
          🗺️ רדיוס שכונתי (1 ק"מ)
        </button>
        <button id="btn-side-gis-close" class="ui-btn" style="background:#dbeafe;color:#1e3a8a;border-color:#93c5fd;font-weight:700;">
          🏢 תקריב המתחם (300 מ')
        </button>
        <a href="feierberg3_spatial_map.html" target="_blank" class="ui-btn" style="background:#0f172a;color:#38bdf8;border-color:#334155;font-weight:800;text-decoration:none;">
          🧭 מפת GIS דו-ממדית (28) ↗
        </a>
        <button id="btn-side-radii" class="ui-btn active">⭕ רדיוסים (8): פעיל</button>
        <button id="btn-side-pois" class="ui-btn active">📍 מיקומים (28): פעיל</button>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px;" id="gis-cat-buttons">
        <button data-gcat="all" class="gis-cat-chip ui-btn active" style="padding:3px 7px;font-size:10px;">הכל (28)</button>
        <button data-gcat="education" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🎓 חינוך (9)</button>
        <button data-gcat="transport" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🚌 תחבורה ומטרו (7)</button>
        <button data-gcat="shopping" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🛒 קניות ומסחר (6)</button>
        <button data-gcat="health" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🏥 בריאות ורפואה (3)</button>
        <button data-gcat="parks" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🌳 פארקים ותרבות (3)</button>
      </div>
      <div style="font-size:11px;font-weight:700;color:#1e3a8a;margin-bottom:4px;">לחץ על מוקד ברשימה למעבר ממוקד במפה:</div>
      <div id="gis-poi-sidebar-list" style="max-height:245px;overflow-y:auto;display:flex;flex-direction:column;gap:4px;padding-left:2px;"></div>
    </div>

    <!-- DRAWER 3: INTERIOR FINISH PACKAGES, LAYERS & DISPLAY -->
    <div id="drawer-settings" class="glass-panel dropdown-drawer" style="width:390px;">
      <div class="flex-between" style="margin-bottom:8px;border-bottom:1px solid #e2e8f0;padding-bottom:6px;">
        <span style="font-size:13px;font-weight:800;color:#0f172a;">⚙️ עיצוב פנים, שכבות והגדרות תצוגה</span>
        <button data-close-drawer class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
      </div>

      <div class="section-box">
        <div class="flex-between" style="margin-bottom:6px;">
          <span style="font-size:12px;font-weight:800;color:#78350f;">🎨 חבילות ריצוף וגמר פנים בזמן אמת (מפרט קולסקי)</span>
          <span id="active-pkg-badge" style="font-size:10px;font-weight:800;background:#fef3c7;color:#92400e;padding:1px 6px;border-radius:4px;">Nordic Oak</span>
        </div>
        <div class="grid-2" style="margin-bottom:6px;" id="interior-pkg-buttons">
          <button data-pkg="nordic" class="pkg-card-btn active">
            <div style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:800;color:#0f172a;">
              <span style="width:12px;height:12px;border-radius:999px;background:#d8dce2;border:1px solid #64748b;"></span>
              <span>1. Nordic Oak</span>
            </div>
            <span style="font-size:9px;color:#64748b;">פורצלן אפור בהיר ודלתות אלון</span>
          </button>
          <button data-pkg="sahara" class="pkg-card-btn">
            <div style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:800;color:#0f172a;">
              <span style="width:12px;height:12px;border-radius:999px;background:#e7dec8;border:1px solid #a8a29e;"></span>
              <span>2. Warm Sahara</span>
            </div>
            <span style="font-size:9px;color:#64748b;">טרוורטין קרם חם ונגרות קשמיר</span>
          </button>
          <button data-pkg="urban" class="pkg-card-btn">
            <div style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:800;color:#0f172a;">
              <span style="width:12px;height:12px;border-radius:999px;background:#94a3b8;border:1px solid #334155;"></span>
              <span>3. Urban Anthracite</span>
            </div>
            <span style="font-size:9px;color:#64748b;">ריצוף גרפיט מודרני ונגרות כהה</span>
          </button>
          <button data-pkg="parquet" class="pkg-card-btn">
            <div style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:800;color:#0f172a;">
              <span style="width:12px;height:12px;border-radius:999px;background:#d8bc96;border:1px solid #92400e;"></span>
              <span>4. Classic Parquet</span>
            </div>
            <span style="font-size:9px;color:#64748b;">פרקט אלון מלא בכל הדירה</span>
          </button>
        </div>
        <div class="grid-2">
          <button id="btn-balcony-deck" class="ui-btn active" style="font-size:11px;grid-column:span 2;">
            🪵 מרפסות: דמוי דק עץ (לחץ להחלפה לפורצלן אפור)
          </button>
        </div>
      </div>

      <div class="section-box">
        <div class="flex-between" style="margin-bottom:6px;">
          <span style="font-size:12px;font-weight:700;color:#334155;">מצב תצוגה, מפת Google Maps וזוויות</span>
          <span id="proj-badge" style="border-radius:4px;background:#e2e8f0;padding:2px 6px;font-size:11px;font-weight:600;color:#1e293b;">פרספקטיבה</span>
        </div>
        <div class="grid-2">
          <button id="btn-gmaps" class="ui-btn active" style="grid-column:span 2;">
            🗺️ מפת לוויין Google Maps (פאירברג 3): פעיל
          </button>
          <button id="btn-ortho" class="ui-btn">📐 היטל אורתוגרפי (1:50)</button>
          <button id="btn-cad-plan" class="ui-btn active">✏️ שרטוט פנים CAD: פעיל</button>
          <button onclick="activatePreset('iso_south')" class="ui-btn">חזית דרומית (רח' פאירברג)</button>
          <button onclick="activatePreset('iso_north')" class="ui-btn">חזית צפונית (עורף)</button>
        </div>
      </div>

      <div class="section-box">
        <div class="flex-between" style="margin-bottom:6px;">
          <span style="font-size:12px;font-weight:700;color:#334155;">שכבות המודל האדריכלי (BIM Layers)</span>
        </div>
        <div id="layer-toggles"></div>
      </div>

      <div class="section-box flex-between" style="gap:10px;margin-bottom:0;">
        <div style="flex:1;">
          <div class="flex-between" style="font-size:11px;color:#334155;">
            <span style="font-weight:700;">☀️ שמש ושעה ביום</span>
            <span id="sun-val" class="cad-badge" style="color:#64748b;">13:30 · צהריים</span>
          </div>
          <input id="sun-slider" type="range" min="15" max="165" step="1" value="65" />
        </div>
        <button id="btn-export-obj" class="ui-btn" style="background:#0f172a;color:#ffffff;border-color:#0f172a;">
          הורד .OBJ
        </button>
      </div>
    </div>

    <!-- BOTTOM-RIGHT INTERACTIVE SECTION & CUT CONTROLLER -->
    <aside id="sections-panel" class="bottom-right-sections">
      <div class="flex-between" style="margin-bottom:8px;">
        <div style="display:flex;align-items:center;gap:7px;">
          <span style="display:inline-flex;height:24px;width:24px;align-items:center;justify-content:center;border-radius:6px;background:#2563eb;color:#ffffff;font-size:12px;font-weight:800;">✂️</span>
          <div>
            <div style="font-size:13px;font-weight:800;color:#0f172a;line-height:1.15;">חתכי קומות וגבהים (Dollhouse)</div>
            <div style="font-size:10px;color:#64748b;" id="active-floor-label">מבנה שלם · הזז מחוון או בחר קומה</div>
          </div>
        </div>
        <button id="btn-toggle-sections-body" class="ui-btn" style="padding:2px 8px;font-size:11px;" title="מזער/הרחב חלון חתכים">▾</button>
      </div>

      <div class="sections-body">
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:8px 10px;margin-bottom:8px;">
          <div class="flex-between" style="margin-bottom:4px;">
            <label for="clip-slider" style="font-size:11px;font-weight:700;color:#0f172a;">מפלס חתך גובה רציף (Z):</label>
            <span id="clip-val" class="cad-badge" style="font-size:11px;font-weight:800;color:#2563eb;">+38.00 מ' (מלא)</span>
          </div>
          <input id="clip-slider" type="range" min="-8.0" max="38.0" step="0.1" value="38.0" />
          <div class="flex-between cad-badge" style="margin-top:3px;font-size:9.5px;color:#64748b;">
            <span>-7.80</span>
            <span>0.00</span>
            <span>+12.95</span>
            <span>+25.55</span>
            <span>+32.02</span>
            <span>+37.50</span>
          </div>
        </div>

        <div class="mode-switch">
          <button id="mode-single" class="active" onclick="setSliceMode('single')">קומה בודדת (תוכנית)</button>
          <button id="mode-cum" onclick="setSliceMode('cumulative')">חיתוך מצטבר</button>
        </div>

        <div class="grid-2" id="floor-buttons"></div>
      </div>
    </aside>

    <!-- FLOATING BOTTOM-LEFT 3D MOVEMENT & PAN CONTROLLER -->
    <div id="orbit-nav-pad" class="glass-panel" style="position:absolute;bottom:14px;left:14px;z-index:24;border-radius:14px;padding:7px 10px;display:flex;align-items:center;gap:6px;flex-wrap:wrap;box-shadow:0 10px 28px rgba(15,23,42,0.18);">
      <button id="btn-toggle-pan-mode" class="ui-btn" style="font-weight:800;padding:4px 9px;background:#eff6ff;border-color:#93c5fd;color:#1d4ed8;" title="החלף פעולת עכבר שמאלי בין סיבוב המודל (Orbit) לבין הזזה חופשית ימינה/שמאלה/למעלה/למטה (Pan)">
        🔄 עכבר: סיבוב
      </button>
      <div style="display:flex;align-items:center;gap:3px;background:#f8fafc;padding:3px 6px;border-radius:9px;border:1px solid #cbd5e1;">
        <span style="font-size:10.5px;font-weight:800;color:#334155;margin-left:3px;">הזזה:</span>
        <button data-opan="right" class="walk-dpad-btn" title="הזז ימינה (חץ ימינה / D)">➡️</button>
        <button data-opan="left" class="walk-dpad-btn" title="הזז שמאלה (חץ שמאלה / A)">⬅️</button>
        <button data-opan="up" class="walk-dpad-btn" title="הזז למעלה (חץ למעלה / W)">⬆️</button>
        <button data-opan="down" class="walk-dpad-btn" title="הזז למטה (חץ למטה / S)">⬇️</button>
        <button data-opan="elevUp" class="walk-dpad-btn" style="width:auto;padding:0 6px;font-size:10.5px;" title="הגבה מבט אנכית (E / PageUp)">🔼 גובה+</button>
        <button data-opan="elevDown" class="walk-dpad-btn" style="width:auto;padding:0 6px;font-size:10.5px;" title="הנמך מבט אנכית (Q / PageDown)">🔽 גובה-</button>
      </div>
      <div style="display:flex;align-items:center;gap:3px;">
        <button data-opan="zoomIn" class="walk-dpad-btn" title="התקרב (Zoom In)">➕</button>
        <button data-opan="zoomOut" class="walk-dpad-btn" title="התרחק (Zoom Out)">➖</button>
        <button data-opan="reset" class="ui-btn" style="padding:3px 8px;font-size:11px;font-weight:800;" title="מרכז את המודל">🎯 מרכוז</button>
      </div>
    </div>

    <!-- Floating Bottom HUD for First-Person Tour & Balcony View Simulator -->
    <div id="aptc-tour-hud" class="aptc-hud">
      <div class="flex-between" style="flex-wrap:wrap;gap:8px;">
        <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
          <span id="apt-active-badge" style="border-radius:6px;background:#b45309;color:#ffffff;padding:3px 8px;font-size:11px;font-weight:800;">פאירברג 3</span>
          <span id="aptc-active-room-title" style="font-size:13px;font-weight:800;color:#451a03;">סיור פנים אדריכלי 1:50</span>
          <div style="display:inline-flex;align-items:center;gap:3px;background:#fef3c7;border:1px solid #f59e0b;border-radius:6px;padding:2px 6px;">
            <span style="font-size:10px;font-weight:800;color:#92400e;">קומה לנוף:</span>
            <select id="tour-floor-select" style="font-size:11px;font-weight:800;color:#451a03;background:transparent;border:none;cursor:pointer;outline:none;">
              <option value="1">קומה 1 (+3.50)</option>
              <option value="2">קומה 2 (+6.65)</option>
              <option value="3">קומה 3 (+9.80)</option>
              <option value="4">קומה 4 (+12.95)</option>
              <option value="5">קומה 5 (+16.10)</option>
              <option value="6">קומה 6 (+19.25)</option>
              <option value="7">קומה 7 (+22.40)</option>
              <option value="8" selected>קומה 8 (+25.55)</option>
              <option value="9">דופלקס 9 (+28.87)</option>
              <option value="10">דופלקס 10 (+32.02)</option>
            </select>
          </div>
        </div>
        <div style="display:flex;align-items:center;gap:10px;font-size:11px;color:#57534e;font-weight:600;">
          <span>⌨️ <b>WASD / חיצים</b>: תזוזה · <b>E/Q</b>: גובה</span>
          <span>🖱️ <b>גרירה</b>: מבט 360°</span>
          <button id="btn-close-tour-hud" class="ui-btn" style="padding:2px 8px;font-size:11px;font-weight:800;background:#ef4444;color:#fff;border-color:#dc2626;">✕ יציאה מסיור</button>
        </div>
      </div>

      <div class="flex-between" style="gap:10px;flex-wrap:wrap;">
        <div style="display:flex;flex-wrap:wrap;gap:4px;flex:1;">
          <span style="font-size:11px;font-weight:800;color:#1e3a8a;align-self:center;padding:0 2px;">חדרים ומרפסות:</span>
          <button onclick="teleportInTour(-3.5, 1.8, 3.14, 'דירה מערבית (4 חד\') · סלון ומטבח')" class="room-chip">🛋️ סלון מערבי (105.5 מ"ר)</button>
          <button onclick="teleportInTour(-2.2, 5.0, 3.14, 'דירה מערבית · מרפסת שמש דרומית לרחוב פאירברג')" class="room-chip">☀️ מרפסת מערבית (פאירברג)</button>
          <button onclick="teleportInTour(4.8, 1.8, 3.14, 'דירה מזרחית (4 חד\') · סלון ומטבח')" class="room-chip">🛋️ סלון מזרחי (85.5 מ"ר)</button>
          <button onclick="teleportInTour(5.4, 5.0, 3.14, 'דירה מזרחית · מרפסת שמש דרומית לרחוב פאירברג')" class="room-chip">☀️ מרפסת מזרחית (פאירברג)</button>
          <button onclick="teleportInTour(-5.5, 3.8, 3.14, 'דופלקס מערבי #17 · מרפסת גג דרומית ופרגולה', 'f9')" class="room-chip">👑 גג דופלקס מערבי #17</button>
          <button onclick="teleportInTour(6.2, 3.8, 3.14, 'דופלקס מזרחי #18 · מרפסת גג דרומית וג\'קוזי', 'f9')" class="room-chip">👑 גג דופלקס מזרחי #18</button>
        </div>

        <div style="display:flex;align-items:center;gap:4px;background:#f5efe6;padding:4px 8px;border-radius:9px;border:1px solid #dec9ad;">
          <span style="font-size:11px;font-weight:700;color:#78350f;margin-left:4px;">תנועה:</span>
          <button data-move="turnL" class="walk-dpad-btn" title="סיבוב מבט שמאלה">↶</button>
          <button data-move="fwd" class="walk-dpad-btn" title="צעד קדימה (W / ↑)">↑</button>
          <button data-move="back" class="walk-dpad-btn" title="צעד אחורה (S / ↓)">↓</button>
          <button data-move="left" class="walk-dpad-btn" title="תזוזה שמאלה (A / ←)">←</button>
          <button data-move="right" class="walk-dpad-btn" title="תזוזה ימינה (D / →)">→</button>
          <button data-move="up" class="walk-dpad-btn" title="תזוזה למעלה (E)">🔼</button>
          <button data-move="down" class="walk-dpad-btn" title="תזוזה למטה (Q)">🔽</button>
          <button data-move="turnR" class="walk-dpad-btn" title="סיבוב מבט ימינה">↷</button>
        </div>
      </div>
    </div>
  </div>

  <script>__THREE_JS_CODE__</script>
  <script>
    const PLANS = __PLANS_JSON__;
    const CRM_DATA = __CRM_JSON__;
    const YATKOVSKI_UNITS = CRM_DATA.units;
    const PARKING_STALLS = CRM_DATA.parking_stalls;
    const SPATIAL_POIS = __SPATIAL_POIS_JSON__;

    const WIDE_GMAPS_DATA_URI    = "__WIDE_GMAPS_URI__";
    const INNER_GMAPS_DATA_URI   = "__INNER_GMAPS_URI__";
    const CLOSEUP_GMAPS_DATA_URI = "__CLOSEUP_GMAPS_URI__";
    const OUTER_SPAN_M   = __OUTER_SPAN_M__;
    const INNER_SPAN_M   = __INNER_SPAN_M__;
    const CLOSEUP_SPAN_M = __CLOSEUP_SPAN_M__;

    // =========================================================================
    // 1. EXACT FLOOR SCHEDULE & ARCHITECTURAL CONSTANTS (FEIERBERG 3)
    // =========================================================================
    const FLOORS = [
      { id: 'b2',  label: 'מרתף 2- · חניון תחתון (11 חניות)',     zFloor: -7.80, zCeil: -5.05, zTop: -4.80, sheet: 'basement_2', elevText: '-7.80', has3DFurn: true },
      { id: 'b1',  label: 'מרתף 1- · חניון עליון (8 חניות)',      zFloor: -4.80, zCeil: -0.25, zTop:  0.00, sheet: 'basement_1', elevText: '-4.80', has3DFurn: true },
      { id: 'kar', label: 'קרקע · לובי ראשי, מועדון ופיתוח',      zFloor:  0.00, zCeil:  3.25, zTop:  3.50, sheet: 'ground',     elevText: '±0.00', has3DFurn: true },
      { id: 'f1',  label: 'קומה 1 · דירות 1–2 (תוכנית 2D)',       zFloor:  3.50, zCeil:  6.45, zTop:  6.65, sheet: 'floors_1_7', elevText: '+3.50', has3DFurn: false },
      { id: 'f2',  label: 'קומה 2 · דירות 3–4 (תוכנית 2D)',       zFloor:  6.65, zCeil:  9.60, zTop:  9.80, sheet: 'floors_1_7', elevText: '+6.65', has3DFurn: false },
      { id: 'f3',  label: 'קומה 3 · דירות 5–6 (תוכנית 2D)',       zFloor:  9.80, zCeil: 12.75, zTop: 12.95, sheet: 'floors_1_7', elevText: '+9.80', has3DFurn: false },
      { id: 'f4',  label: 'קומה 4 · דירות 7–8 (מרוהטת 3D ✨)',     zFloor: 12.95, zCeil: 15.90, zTop: 16.10, sheet: 'floors_1_7', elevText: '+12.95', has3DFurn: true },
      { id: 'f5',  label: 'קומה 5 · דירות 9–10 (תוכנית 2D)',      zFloor: 16.10, zCeil: 19.05, zTop: 19.25, sheet: 'floors_1_7', elevText: '+16.10', has3DFurn: false },
      { id: 'f6',  label: 'קומה 6 · דירות 11–12 (תוכנית 2D)',     zFloor: 19.25, zCeil: 22.20, zTop: 22.40, sheet: 'floors_1_7', elevText: '+19.25', has3DFurn: false },
      { id: 'f7',  label: 'קומה 7 · דירות 13–14 (תוכנית 2D)',     zFloor: 22.40, zCeil: 25.35, zTop: 25.55, sheet: 'floors_1_7', elevText: '+22.40', has3DFurn: false },
      { id: 'f8',  label: 'קומה 8 · דירות 15–16 (+ פרגולות)',     zFloor: 25.55, zCeil: 28.65, zTop: 28.87, sheet: 'floor_8',    elevText: '+25.55', has3DFurn: false },
      { id: 'f9',  label: 'קומה 9 · דופלקס #17–#18 (תחתון)',      zFloor: 28.87, zCeil: 31.82, zTop: 32.02, sheet: 'floor_9',    elevText: '+28.87', has3DFurn: false },
      { id: 'f10', label: 'קומה 10 · דופלקס #17–#18 (עליון) 👑',  zFloor: 32.02, zCeil: 34.97, zTop: 35.17, sheet: 'floor_10',   elevText: '+32.02', has3DFurn: false },
      { id: 'gag', label: 'גג עליון, חדר יציאה לגג וקולטים',     zFloor: 35.17, zCeil: 37.50, zTop: 37.50, sheet: 'roof',       elevText: '+35.17', has3DFurn: true }
    ];

    const LAYERS_DEF = [
      { id: 'walls',     name: 'קירות חוץ (אבן לבנה ק\' 1–8 + חיפוי כהה ק\' 9–10) וקירות פנים', color: '#fcfdff', visible: true },
      { id: 'slabs',     name: 'רצפות ותקרות מדויקות לפי קווי הבניין ב-DWF/PDF', color: '#d6dae0', visible: true },
      { id: 'windows',   name: 'חלונות, וויטרינות, ארגזי תריס כהים ומעקות', color: '#38bdf8', visible: true },
      { id: 'doors',     name: 'דלתות פנים וכניסה + חלונות הדף ממ"ד', color: '#c89d6c', visible: true },
      { id: 'balconies', name: 'מרפסות שמש דרומיות (ק\' 1–8), מרפסות גג דופלקס ק\' 9–10 ומעקות', color: '#a46b3f', visible: true },
      { id: 'pergolas',  name: 'מסגרות חזית דו-קומתיות, פרגולות ק\' 8–9, רפפות מסתורי כביסה וקולטים', color: '#334155', visible: true },
      { id: 'furn3d',    name: 'ריהוט פנים תלת-ממדי יוקרתי + ציור ריהוט ומטבחים (3D & 2D)', color: '#1e3a8a', visible: true },
      { id: 'cad2d',     name: 'תוכנית CAD וקטורית 1:50 וגבול מגרש על הרצפה', color: '#475569', visible: true },
      { id: 'labels',    name: 'שמות ומידות חדרים פנימיות', color: '#1e293b', visible: true },
      { id: 'site',      name: 'חלקה 193 בגוש 6387 (33.5×16.4 מ\'), מרתפי חניון ורחוב פאירברג 3', color: '#94a3b8', visible: true }
    ];

    // =========================================================================
    // 2. THREE.JS SCENE, CAMERAS & LIGHTING
    // =========================================================================
    const canvas = document.getElementById('cad-canvas');
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance', preserveDrawingBuffer: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.localClippingEnabled = true;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf4f1ea);

    const clipPlane = new THREE.Plane(new THREE.Vector3(0, -1, 0), 38.0);
    const clippingPlanes = [clipPlane];

    const aspect = window.innerWidth / window.innerHeight;
    const perspCam = new THREE.PerspectiveCamera(42, aspect, 0.2, 8000);
    const orthoSize = 22;
    const orthoCam = new THREE.OrthographicCamera(-orthoSize * aspect, orthoSize * aspect, orthoSize, -orthoSize, -2000, 6000);
    let activeCam = perspCam;
    let isOrtho = false;

    const hemiLight = new THREE.HemisphereLight(0xfffdf8, 0xd8d0c2, 0.66);
    hemiLight.position.set(0, 140, 0);
    scene.add(hemiLight);

    const dirLight = new THREE.DirectionalLight(0xfffaf0, 0.72);
    dirLight.position.set(45, 85, 52);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 2048;
    dirLight.shadow.mapSize.height = 2048;
    dirLight.shadow.camera.near = 10;
    dirLight.shadow.camera.far = 220;
    const dCam = 38;
    dirLight.shadow.camera.left = -dCam;
    dirLight.shadow.camera.right = dCam;
    dirLight.shadow.camera.top = dCam;
    dirLight.shadow.camera.bottom = -dCam;
    dirLight.shadow.bias = -0.0004;
    scene.add(dirLight);

    const fillLight = new THREE.DirectionalLight(0xf3ede2, 0.30);
    fillLight.position.set(-48, 45, -48);
    scene.add(fillLight);

    const nightLightsGroup = new THREE.Group();
    nightLightsGroup.visible = false;
    scene.add(nightLightsGroup);
    [[-6, 14, 2], [6, 14, 2], [-6, 26, 2], [6, 26, 2], [-5, 31, 1], [5, 31, 1], [0, 2.5, 2]].forEach(([lx, ly, lz]) => {
      const pl = new THREE.PointLight(0xffb454, 1.4, 32, 1.8);
      pl.position.set(lx, ly, lz);
      nightLightsGroup.add(pl);
    });

    // =========================================================================
    // 3. ARCHITECTURAL MATERIALS & LUXURY INTERIOR PBR MATERIALS
    // =========================================================================
    function createWoodPlankTexture(c1 = '#ad7449', c2 = '#9c653b', groove = '#6e4423') {
      const c = document.createElement('canvas');
      c.width = 256; c.height = 256;
      const ctx = c.getContext('2d');
      ctx.fillStyle = c1; ctx.fillRect(0, 0, 256, 256);
      for (let i = 0; i < 8; i++) {
        const y = i * 32;
        ctx.fillStyle = (i % 2 === 0) ? c1 : c2;
        ctx.fillRect(0, y, 256, 30);
        ctx.fillStyle = groove;
        ctx.fillRect(0, y + 30, 256, 2);
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(2, 2);
      return tex;
    }

    function createTileTexture(bgHex, gridHex, repeatX = 10, repeatY = 10) {
      const c = document.createElement('canvas');
      c.width = 256; c.height = 256;
      const ctx = c.getContext('2d');
      ctx.fillStyle = bgHex; ctx.fillRect(0, 0, 256, 256);
      ctx.strokeStyle = gridHex; ctx.lineWidth = 2;
      for (let i = 0; i <= 256; i += 64) {
        ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, 256); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(256, i); ctx.stroke();
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(repeatX, repeatY);
      return tex;
    }

    function makeTravertineFloorTexture() {
      const c = document.createElement('canvas');
      c.width = 512; c.height = 512;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#efeadd'; ctx.fillRect(0, 0, 512, 512);
      for (let i = 0; i < 28; i++) {
        ctx.strokeStyle = (i % 2 === 0) ? 'rgba(218, 208, 190, 0.35)' : 'rgba(232, 224, 208, 0.45)';
        ctx.lineWidth = 6 + (i % 4) * 3;
        ctx.beginPath();
        const y0 = (i * 21) % 512;
        ctx.moveTo(0, y0);
        ctx.bezierCurveTo(170, y0 + 10, 340, y0 - 10, 512, y0 + 4);
        ctx.stroke();
      }
      ctx.strokeStyle = '#d8cfc0'; ctx.lineWidth = 2;
      for (let g = 0; g <= 512; g += 256) {
        ctx.beginPath(); ctx.moveTo(g, 0); ctx.lineTo(g, 512); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(0, g); ctx.lineTo(512, g); ctx.stroke();
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(3, 3);
      return tex;
    }

    function makeCalacattaMarbleTexture() {
      const c = document.createElement('canvas');
      c.width = 512; c.height = 512;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#fbfaf7'; ctx.fillRect(0, 0, 512, 512);
      const veins = [
        [0, 80, 180, 140, 350, 240, 512, 310, 'rgba(180, 165, 145, 0.42)', 5],
        [40, 0, 210, 190, 310, 360, 490, 512, 'rgba(160, 140, 115, 0.28)', 3],
        [0, 320, 160, 290, 340, 410, 512, 460, 'rgba(195, 170, 130, 0.32)', 4]
      ];
      veins.forEach(v => {
        ctx.strokeStyle = v[8]; ctx.lineWidth = v[9];
        ctx.beginPath(); ctx.moveTo(v[0], v[1]); ctx.bezierCurveTo(v[2], v[3], v[4], v[5], v[6], v[7]); ctx.stroke();
      });
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      return tex;
    }

    function makeFlutedOakTexture() {
      const c = document.createElement('canvas');
      c.width = 512; c.height = 512;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#c89f70'; ctx.fillRect(0, 0, 512, 512);
      for (let x = 0; x < 512; x += 16) {
        ctx.fillStyle = '#d4ad7e'; ctx.fillRect(x, 0, 10, 512);
        ctx.fillStyle = '#8c6238'; ctx.fillRect(x + 10, 0, 6, 512);
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(2, 1);
      return tex;
    }

    function makeWovenRugTexture() {
      const c = document.createElement('canvas');
      c.width = 256; c.height = 256;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#e7dfd1'; ctx.fillRect(0, 0, 256, 256);
      ctx.strokeStyle = 'rgba(195, 182, 162, 0.45)'; ctx.lineWidth = 2;
      for (let y = 0; y < 256; y += 6) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(256, y); ctx.stroke();
      }
      ctx.strokeStyle = '#d2c5b0'; ctx.lineWidth = 8;
      ctx.strokeRect(10, 10, 236, 236);
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      return tex;
    }

    const FINISH_TEXTURES = {
      nordic:  { label: 'Nordic Oak',       map: createTileTexture('#d8dce2', '#c3c9d1'), color: 0xd8dce2, door: 0xd4ad7d },
      sahara:  { label: 'Warm Sahara',      map: createTileTexture('#e7dec8', '#d2c4a8'), color: 0xe7dec8, door: 0xc89a68 },
      urban:   { label: 'Urban Anthracite', map: createTileTexture('#94a3b8', '#78879c'), color: 0x94a3b8, door: 0x64748b },
      parquet: { label: 'Classic Parquet',  map: createWoodPlankTexture('#c89d6c', '#b98b59', '#8c6239'), color: 0xdfc19b, door: 0xb88652 }
    };

    const DECK_TEXTURES = {
      wood: createWoodPlankTexture('#ad7449', '#9c653b', '#6e4423'),
      grey: createTileTexture('#94a3b8', '#64748b', 4, 4)
    };

    const texTravertine = makeTravertineFloorTexture();
    const texCalacatta  = makeCalacattaMarbleTexture();
    const texFlutedOak  = makeFlutedOakTexture();
    const texWovenRug   = makeWovenRugTexture();

    const MATS = {
      wall: new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.76, metalness: 0.01, side: THREE.DoubleSide, clippingPlanes }),
      extWall: new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.68, metalness: 0.02, side: THREE.DoubleSide, clippingPlanes }),
      penthouseWall: new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.56, metalness: 0.14, side: THREE.DoubleSide, clippingPlanes }),
      bronzePortal: new THREE.MeshStandardMaterial({ color: 0x3f3f46, roughness: 0.46, metalness: 0.18, side: THREE.DoubleSide, clippingPlanes }),
      shutterBox: new THREE.MeshStandardMaterial({ color: 0x3f3f46, roughness: 0.50, metalness: 0.25, side: THREE.DoubleSide, clippingPlanes }),
      slabSoffit: new THREE.MeshStandardMaterial({ color: 0x9ca3af, roughness: 0.78, metalness: 0.02, side: THREE.DoubleSide, clippingPlanes }),
      wallCap: new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.80, metalness: 0.02, side: THREE.DoubleSide, clippingPlanes }),
      slabFloor: new THREE.MeshStandardMaterial({ map: FINISH_TEXTURES.nordic.map, color: 0xe2e8f0, roughness: 0.65, metalness: 0.04, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, clippingPlanes }),
      slabEdge: new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.70, clippingPlanes }),
      terraceFloor: new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.72, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, clippingPlanes }),
      woodDeck: new THREE.MeshStandardMaterial({ map: DECK_TEXTURES.wood, color: 0xe2e8f0, roughness: 0.68, metalness: 0.03, clippingPlanes }),
      glassRailing: new THREE.MeshPhysicalMaterial({ color: 0xcbd5e1, transparent: true, opacity: 0.26, roughness: 0.08, metalness: 0.05, side: THREE.DoubleSide, clippingPlanes }),
      aluDark: new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.34, metalness: 0.58, clippingPlanes }),
      louverBronze: new THREE.MeshStandardMaterial({ color: 0x785a46, roughness: 0.42, metalness: 0.45, clippingPlanes }),
      winGlass: new THREE.MeshPhysicalMaterial({ color: 0x93c5fd, emissive: 0x0369a1, emissiveIntensity: 0.10, transparent: true, opacity: 0.54, roughness: 0.08, metalness: 0.22, side: THREE.DoubleSide, clippingPlanes }),
      lightWood: new THREE.MeshStandardMaterial({ color: 0xd4ad7d, roughness: 0.52, metalness: 0.04, clippingPlanes }),
      doorFrame: new THREE.MeshStandardMaterial({ color: 0xb0895a, roughness: 0.55, clippingPlanes }),
      mamadSteel: new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.35, metalness: 0.72, clippingPlanes }),
      basementConcrete: new THREE.MeshStandardMaterial({ color: 0xcbd5e1, roughness: 0.85, side: THREE.DoubleSide, clippingPlanes }),
      asphalt: new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.9, clippingPlanes }),
      sidewalk: new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.85, clippingPlanes }),
      grass: new THREE.MeshStandardMaterial({ color: 0xd1fae5, roughness: 0.9, clippingPlanes }),
      solarPanel: new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.25, metalness: 0.5, clippingPlanes }),
      waterSpa: new THREE.MeshPhysicalMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.72, roughness: 0.08, metalness: 0.1, clippingPlanes }),
      lineFurn: new THREE.LineBasicMaterial({ color: 0x1e3a8a, transparent: true, opacity: 0.94, clippingPlanes }),
      lineCad: new THREE.LineBasicMaterial({ color: 0x0f172a, transparent: true, opacity: 0.82, clippingPlanes }),
      archEdge: new THREE.LineBasicMaterial({ color: 0x1e293b, transparent: true, opacity: 0.55, clippingPlanes }),
      luxTravertine: new THREE.MeshStandardMaterial({ map: texTravertine, color: 0xf5f0e6, roughness: 0.36, metalness: 0.05, clippingPlanes }),
      luxCalacatta:  new THREE.MeshStandardMaterial({ map: texCalacatta,  color: 0xffffff, roughness: 0.18, metalness: 0.08, clippingPlanes }),
      luxFlutedOak:  new THREE.MeshStandardMaterial({ map: texFlutedOak,  color: 0xd4ad7e, roughness: 0.48, metalness: 0.05, clippingPlanes }),
      luxOakSmooth:  new THREE.MeshStandardMaterial({ color: 0xc89d6c, roughness: 0.42, metalness: 0.06, clippingPlanes }),
      luxBoucle:     new THREE.MeshStandardMaterial({ color: 0xf7f3eb, roughness: 0.88, metalness: 0.01, clippingPlanes }),
      luxTaupe:      new THREE.MeshStandardMaterial({ color: 0x9c8b7a, roughness: 0.78, metalness: 0.02, clippingPlanes }),
      luxCabinet:    new THREE.MeshStandardMaterial({ color: 0xf3efe6, roughness: 0.35, metalness: 0.04, clippingPlanes }),
      luxBrass:      new THREE.MeshStandardMaterial({ color: 0xd4af37, roughness: 0.24, metalness: 0.82, clippingPlanes }),
      luxRug:        new THREE.MeshStandardMaterial({ map: texWovenRug, color: 0xede6d8, roughness: 0.92, metalness: 0.0, clippingPlanes }),
      luxCeramic:    new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.15, metalness: 0.05, clippingPlanes }),
      luxPlantOlive: new THREE.MeshStandardMaterial({ color: 0x5c7457, roughness: 0.75, metalness: 0.02, clippingPlanes })
    };

    const floorGroups = {};
    FLOORS.forEach(f => {
      const g = new THREE.Group();
      g.name = 'floor_' + f.id;
      scene.add(g);
      floorGroups[f.id] = g;
    });

    const layerObjects = {};
    LAYERS_DEF.forEach(l => { layerObjects[l.id] = []; });
    const allBuildingMeshes = [];

    function addToFloorAndLayer(floorId, layerId, obj) {
      floorGroups[floorId].add(obj);
      layerObjects[layerId].push(obj);
      obj.traverse(c => { if (c.isMesh) allBuildingMeshes.push(c); });
    }
"""

HTML_PART2A = r"""
    // =========================================================================
    // 4. GEOMETRY HELPERS (100% DWF/PDF-DRIVEN FEIERBERG 3 ARCHITECTURE)
    // =========================================================================
    function ptToSegDist2D(px, py, x1, y1, x2, y2) {
      const dx = x2 - x1, dy = y2 - y1;
      const len2 = dx * dx + dy * dy;
      if (len2 < 1e-8) return Math.hypot(px - x1, py - y1);
      let t = ((px - x1) * dx + (py - y1) * dy) / len2;
      t = Math.max(0, Math.min(1, t));
      return Math.hypot(px - (x1 + t * dx), py - (y1 + t * dy));
    }

    function isExteriorWallFace(sheetKey, x1, y1, x2, y2) {
      if (sheetKey === 'roof') return true;
      if (sheetKey === 'basement_1' || sheetKey === 'basement_2') return false;
      const xm = 0.5 * (x1 + x2);
      const ym = 0.5 * (y1 + y2);
      const pData = PLANS[sheetKey];
      const extRing = pData && pData.slab_poly ? (pData.slab_poly.outline || pData.slab_poly.exterior) : null;
      if (extRing && extRing.length > 0) {
        for (let i = 0; i < extRing.length; i++) {
          const a = extRing[i], b = extRing[(i + 1) % extRing.length];
          if (ptToSegDist2D(xm, ym, a[0], a[1], b[0], b[1]) <= 0.35) return true;
        }
      }
      return false;
    }

    function buildExtrudedTriPoly(polyData, z0, z1, matWall, matCap, sheetKey = null, matExtWall = null, matBotCap = null) {
      const grp = new THREE.Group();
      const h = z1 - z0;
      if (!polyData || !polyData.tris || polyData.tris.length === 0 || h <= 0.005) return grp;

      const topPos = [];
      const botPos = [];
      const tris = polyData.tris;
      if (Array.isArray(tris[0]) && Array.isArray(tris[0][0])) {
        for (const t of tris) {
          topPos.push(t[0][0], z1, t[0][1], t[2][0], z1, t[2][1], t[1][0], z1, t[1][1]);
          botPos.push(t[0][0], z0, t[0][1], t[1][0], z0, t[1][1], t[2][0], z0, t[2][1]);
        }
      } else {
        for (let i = 0; i + 2 < tris.length; i += 3) {
          const p0 = tris[i], p1 = tris[i + 1], p2 = tris[i + 2];
          topPos.push(p0[0], z1, p0[1], p2[0], z1, p2[1], p1[0], z1, p1[1]);
          botPos.push(p0[0], z0, p0[1], p1[0], z0, p1[1], p2[0], z0, p2[1]);
        }
      }

      const topGeo = new THREE.BufferGeometry();
      topGeo.setAttribute('position', new THREE.Float32BufferAttribute(topPos, 3));
      topGeo.computeVertexNormals();
      const topMesh = new THREE.Mesh(topGeo, matCap || matWall);
      topMesh.castShadow = true;
      topMesh.receiveShadow = true;
      grp.add(topMesh);

      const botGeo = new THREE.BufferGeometry();
      botGeo.setAttribute('position', new THREE.Float32BufferAttribute(botPos, 3));
      botGeo.computeVertexNormals();
      const botMesh = new THREE.Mesh(botGeo, matBotCap || matCap || matWall);
      botMesh.castShadow = true;
      botMesh.receiveShadow = true;
      grp.add(botMesh);

      const intSidePos = [];
      const extSidePos = [];
      const edgeLinePos = [];
      const outerRing = polyData.outline || polyData.exterior || [];
      const rings = [outerRing, ...(polyData.holes || [])];
      for (const ring of rings) {
        if (!ring || ring.length < 3) continue;
        const n = ring.length;
        for (let i = 0; i < n; i++) {
          const p1 = ring[i];
          const p2 = ring[(i + 1) % n];
          const useExt = (matExtWall && sheetKey && isExteriorWallFace(sheetKey, p1[0], p1[1], p2[0], p2[1]));
          const targetArr = useExt ? extSidePos : intSidePos;
          targetArr.push(
            p1[0], z0, p1[1],  p2[0], z0, p2[1],  p2[0], z1, p2[1],
            p1[0], z0, p1[1],  p2[0], z1, p2[1],  p1[0], z1, p1[1]
          );
          if (!sheetKey || useExt) {
            edgeLinePos.push(
              p1[0], z0, p1[1], p2[0], z0, p2[1],
              p1[0], z1, p1[1], p2[0], z1, p2[1]
            );
          }
        }
      }
      if (intSidePos.length > 0) {
        const sideGeo = new THREE.BufferGeometry();
        sideGeo.setAttribute('position', new THREE.Float32BufferAttribute(intSidePos, 3));
        sideGeo.computeVertexNormals();
        const sideMesh = new THREE.Mesh(sideGeo, matWall);
        sideMesh.castShadow = true;
        sideMesh.receiveShadow = true;
        grp.add(sideMesh);
      }
      if (extSidePos.length > 0) {
        const extGeo = new THREE.BufferGeometry();
        extGeo.setAttribute('position', new THREE.Float32BufferAttribute(extSidePos, 3));
        extGeo.computeVertexNormals();
        const extMesh = new THREE.Mesh(extGeo, matExtWall);
        extMesh.castShadow = true;
        extMesh.receiveShadow = true;
        grp.add(extMesh);
      }
      if (edgeLinePos.length > 0) {
        const eGeo = new THREE.BufferGeometry();
        eGeo.setAttribute('position', new THREE.Float32BufferAttribute(edgeLinePos, 3));
        grp.add(new THREE.LineSegments(eGeo, MATS.archEdge));
      }
      return grp;
    }

    function makeBox(x0, y0, x1, y1, z0, z1, mat, castShadow = true, withEdges = false) {
      const w = Math.abs(x1 - x0);
      const d = Math.abs(y1 - y0);
      const h = Math.abs(z1 - z0);
      if (w < 0.002 || d < 0.002 || h < 0.002) return new THREE.Group();
      const geo = new THREE.BoxGeometry(w, h, d);
      const m = new THREE.Mesh(geo, mat);
      m.position.set(0.5 * (x0 + x1), 0.5 * (z0 + z1), 0.5 * (y0 + y1));
      m.castShadow = castShadow;
      m.receiveShadow = true;
      if (withEdges) {
        const edges = new THREE.EdgesGeometry(geo);
        const line = new THREE.LineSegments(edges, MATS.archEdge);
        m.add(line);
      }
      return m;
    }

    function makeExteriorOpeningWallBox(floorObj, x0, y0, x1, y1, z0, z1) {
      const isPh = (floorObj.id === 'f9' || floorObj.id === 'f10');
      const extMat = isPh ? MATS.penthouseWall : MATS.extWall;
      return makeBox(x0, y0, x1, y1, z0, z1, extMat, true, true);
    }

    function buildPolygonSlab(pts2d, z0, z1, matTop, matSide) {
      const shape = new THREE.Shape();
      shape.moveTo(pts2d[0][0], -pts2d[0][1]);
      for (let i = 1; i < pts2d.length; i++) {
        shape.lineTo(pts2d[i][0], -pts2d[i][1]);
      }
      shape.closePath();
      const geo = new THREE.ExtrudeGeometry(shape, { depth: z1 - z0, bevelEnabled: false });
      geo.rotateX(-Math.PI / 2);
      const m = new THREE.Mesh(geo, [matTop, matSide || matTop]);
      m.position.y = z0;
      m.receiveShadow = true;
      m.castShadow = true;
      return m;
    }

    function buildOpening3D(floorObj, op) {
      const [orient, x0, y0, x1, y1, kind] = op;
      const zFloor = floorObj.zFloor;
      const zCeil = floorObj.zCeil;
      const midX = 0.5 * (x0 + x1);
      const midY = 0.5 * (y0 + y1);
      const span = (orient === 'H') ? (x1 - x0) : (y1 - y0);

      if (kind === 'vitrine') {
        const zTopOpen = (floorObj.id === 'kar') ? Math.min(zFloor + 2.85, zCeil - 0.15) : Math.min(zFloor + 2.18, zCeil - 0.15);
        const zShutterTop = Math.min(zTopOpen + 0.26, zCeil);
        if (zShutterTop > zTopOpen + 0.02) {
          addToFloorAndLayer(floorObj.id, 'windows', makeBox(x0, y0 - 0.015, x1, y1 + 0.015, zTopOpen, zShutterTop, MATS.shutterBox, true, true));
        }
        if (zCeil > zShutterTop + 0.02) {
          addToFloorAndLayer(floorObj.id, 'walls', makeExteriorOpeningWallBox(floorObj, x0, y0, x1, y1, zShutterTop, zCeil));
        }
        const vGrp = new THREE.Group();
        const fThick = 0.065;
        const padOut = 0.018;
        if (orient === 'H') {
          const fy0 = y0 - padOut, fy1 = y1 + padOut;
          vGrp.add(makeBox(x0, fy0, x1, fy1, zFloor, zFloor + fThick, MATS.aluDark, false));
          vGrp.add(makeBox(x0, fy0, x1, fy1, zTopOpen - fThick, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(x0, fy0, x0 + fThick, fy1, zFloor, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(x1 - fThick, fy0, x1, fy1, zFloor, zTopOpen, MATS.aluDark, false));
          const nPanels = (span >= 2.40) ? 3 : 2;
          for (let i = 1; i < nPanels; i++) {
            const mx = x0 + (span * i) / nPanels;
            vGrp.add(makeBox(mx - 0.032, fy0 + 0.01, mx + 0.032, fy1 - 0.01, zFloor, zTopOpen, MATS.aluDark, false));
          }
          vGrp.add(makeBox(x0 + fThick, midY - 0.022, x1 - fThick, midY + 0.022, zFloor + fThick, zTopOpen - fThick, MATS.winGlass, false));
        } else {
          const fx0 = x0 - padOut, fx1 = x1 + padOut;
          vGrp.add(makeBox(fx0, y0, fx1, y1, zFloor, zFloor + fThick, MATS.aluDark, false));
          vGrp.add(makeBox(fx0, y0, fx1, y1, zTopOpen - fThick, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(fx0, y0, fx1, y0 + fThick, zFloor, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(fx0, y1 - fThick, fx1, y1, zFloor, zTopOpen, MATS.aluDark, false));
          const nPanels = (span >= 2.40) ? 3 : 2;
          for (let i = 1; i < nPanels; i++) {
            const my = y0 + (span * i) / nPanels;
            vGrp.add(makeBox(fx0 + 0.01, my - 0.032, fx1 - 0.01, my + 0.032, zFloor, zTopOpen, MATS.aluDark, false));
          }
          vGrp.add(makeBox(midX - 0.022, y0 + fThick, midX + 0.022, y1 - fThick, zFloor + fThick, zTopOpen - fThick, MATS.winGlass, false));
        }
        addToFloorAndLayer(floorObj.id, 'windows', vGrp);

      } else if (kind === 'win_tall' || kind === 'mamad_win' || kind === 'window') {
        const zSill = (kind === 'win_tall') ? (zFloor + 0.65) : (zFloor + 1.00);
        const zHead = Math.min(zFloor + 2.18, zCeil - 0.15);
        addToFloorAndLayer(floorObj.id, 'walls', makeExteriorOpeningWallBox(floorObj, x0, y0, x1, y1, zFloor, zSill));
        if (zCeil > zHead + 0.02) {
          addToFloorAndLayer(floorObj.id, 'walls', makeExteriorOpeningWallBox(floorObj, x0, y0, x1, y1, zHead, zCeil));
        }
        const wGrp = new THREE.Group();
        const fThick = 0.06;
        const padOut = 0.018;
        if (orient === 'H') {
          const fy0 = y0 - padOut, fy1 = y1 + padOut;
          wGrp.add(makeBox(x0, fy0, x1, fy1, zSill, zSill + fThick, MATS.aluDark, false));
          wGrp.add(makeBox(x0, fy0, x1, fy1, zHead - fThick, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(x0, fy0, x0 + fThick, fy1, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(x1 - fThick, fy0, x1, fy1, zSill, zHead, MATS.aluDark, false));
          const nPanes = (span >= 2.20) ? 3 : ((span >= 0.95) ? 2 : 1);
          for (let i = 1; i < nPanes; i++) {
            const mx = x0 + (span * i) / nPanes;
            wGrp.add(makeBox(mx - 0.028, fy0 + 0.008, mx + 0.028, fy1 - 0.008, zSill, zHead, MATS.aluDark, false));
          }
          wGrp.add(makeBox(x0 + fThick, midY - 0.02, x1 - fThick, midY + 0.02, zSill + fThick, zHead - fThick, MATS.winGlass, false));
        } else {
          const fx0 = x0 - padOut, fx1 = x1 + padOut;
          wGrp.add(makeBox(fx0, y0, fx1, y1, zSill, zSill + fThick, MATS.aluDark, false));
          wGrp.add(makeBox(fx0, y0, fx1, y1, zHead - fThick, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(fx0, y0, fx1, y0 + fThick, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(fx0, y1 - fThick, fx1, y1, zSill, zHead, MATS.aluDark, false));
          const nPanes = (span >= 2.20) ? 3 : ((span >= 0.95) ? 2 : 1);
          for (let i = 1; i < nPanes; i++) {
            const my = y0 + (span * i) / nPanes;
            wGrp.add(makeBox(fx0 + 0.008, my - 0.028, fx1 - 0.008, my + 0.028, zSill, zHead, MATS.aluDark, false));
          }
          wGrp.add(makeBox(midX - 0.02, y0 + fThick, midX + 0.02, y1 - fThick, zSill + fThick, zHead - fThick, MATS.winGlass, false));
        }
        addToFloorAndLayer(floorObj.id, 'windows', wGrp);

      } else if (kind === 'door') {
        const zDoorTop = Math.min(zFloor + 2.10, zCeil - 0.15);
        if (zCeil > zDoorTop + 0.02) {
          addToFloorAndLayer(floorObj.id, 'walls', makeBox(x0, y0, x1, y1, zDoorTop, zCeil, MATS.wall));
        }
        const dGrp = new THREE.Group();
        const fW = 0.04;
        dGrp.add(makeBox(x0, y0, x1, y1, zDoorTop - fW, zDoorTop, MATS.doorFrame, false));
        if (orient === 'H') {
          dGrp.add(makeBox(x0, y0, x0 + fW, y1, zFloor, zDoorTop, MATS.doorFrame, false));
          dGrp.add(makeBox(x1 - fW, y0, x1, y1, zFloor, zDoorTop, MATS.doorFrame, false));
          const leafW = Math.max(0.4, (x1 - x0) - 2 * fW);
          const leafGeo = new THREE.BoxGeometry(leafW, zDoorTop - zFloor - fW, 0.04);
          leafGeo.translate(leafW / 2, 0, 0);
          const leaf = new THREE.Mesh(leafGeo, MATS.lightWood);
          leaf.position.set(x0 + fW, zFloor + 0.5 * (zDoorTop - zFloor - fW), 0.5 * (y0 + y1));
          leaf.rotation.y = 0.38;
          dGrp.add(leaf);
        } else {
          dGrp.add(makeBox(x0, y0, x1, y0 + fW, zFloor, zDoorTop, MATS.doorFrame, false));
          dGrp.add(makeBox(x0, y1 - fW, x1, y1, zFloor, zDoorTop, MATS.doorFrame, false));
          const leafW = Math.max(0.4, (y1 - y0) - 2 * fW);
          const leafGeo = new THREE.BoxGeometry(0.04, zDoorTop - zFloor - fW, leafW);
          leafGeo.translate(0, 0, leafW / 2);
          const leaf = new THREE.Mesh(leafGeo, MATS.lightWood);
          leaf.position.set(0.5 * (x0 + x1), zFloor + 0.5 * (zDoorTop - zFloor - fW), y0 + fW);
          leaf.rotation.y = -0.38;
          dGrp.add(leaf);
        }
        addToFloorAndLayer(floorObj.id, 'doors', dGrp);
      }
    }

    function createFloorLabelMesh(nameText, dimsText, x, y, zFloor) {
      const c = document.createElement('canvas');
      c.width = 256; c.height = 128;
      const ctx = c.getContext('2d');
      ctx.clearRect(0, 0, 256, 128);
      ctx.fillStyle = 'rgba(214, 218, 224, 0.85)';
      ctx.beginPath();
      ctx.roundRect(10, 14, 236, dimsText ? 96 : 62, 12);
      ctx.fill();
      ctx.strokeStyle = 'rgba(71, 85, 105, 0.40)';
      ctx.lineWidth = 2;
      ctx.stroke();

      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = '#0f172a';
      ctx.font = 'bold 20px "Segoe UI", Arial, sans-serif';
      ctx.fillText(nameText, 128, dimsText ? 44 : 45);

      if (dimsText) {
        ctx.fillStyle = '#1d4ed8';
        ctx.font = 'bold 19px "Segoe UI", monospace, sans-serif';
        ctx.fillText(dimsText, 128, 82);
      }

      const tex = new THREE.CanvasTexture(c);
      tex.anisotropy = 4;
      const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, side: THREE.DoubleSide, clippingPlanes });
      const geo = new THREE.PlaneGeometry(1.90, 0.90);
      geo.rotateX(-Math.PI / 2);
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(x, zFloor + 0.028, y);
      return mesh;
    }

    function buildRailingSegment(grp, x1, y1, x2, y2, zFloor, railHeight = 1.05) {
      const len = Math.hypot(x2 - x1, y2 - y1);
      if (len < 0.08) return;
      const zBotRail0 = zFloor + 0.09;
      const zBotRail1 = zFloor + 0.14;
      const zTopRail0 = zFloor + railHeight - 0.06;
      const zTopRail1 = zFloor + railHeight;
      const postHalf = 0.028;

      if (Math.abs(y2 - y1) < 0.05) {
        const xa = Math.min(x1, x2), xb = Math.max(x1, x2), ym = 0.5 * (y1 + y2);
        grp.add(makeBox(xa - 0.02, ym - 0.032, xb + 0.02, ym + 0.032, zBotRail0, zBotRail1, MATS.aluDark, false));
        grp.add(makeBox(xa - 0.025, ym - 0.038, xb + 0.025, ym + 0.038, zTopRail0, zTopRail1, MATS.aluDark, false));
        const nSpans = Math.max(1, Math.round((xb - xa) / 1.45));
        for (let i = 0; i <= nSpans; i++) {
          const px = xa + ((xb - xa) * i) / nSpans;
          grp.add(makeBox(px - postHalf, ym - postHalf, px + postHalf, ym + postHalf, zFloor, zTopRail1, MATS.aluDark, false));
        }
        grp.add(makeBox(xa + 0.01, ym - 0.012, xb - 0.01, ym + 0.012, zBotRail1, zTopRail0, MATS.glassRailing, false));
      } else if (Math.abs(x2 - x1) < 0.05) {
        const ya = Math.min(y1, y2), yb = Math.max(y1, y2), xm = 0.5 * (x1 + x2);
        grp.add(makeBox(xm - 0.032, ya - 0.02, xm + 0.032, yb + 0.02, zBotRail0, zBotRail1, MATS.aluDark, false));
        grp.add(makeBox(xm - 0.038, ya - 0.025, xm + 0.038, yb + 0.025, zTopRail0, zTopRail1, MATS.aluDark, false));
        const nSpans = Math.max(1, Math.round((yb - ya) / 1.45));
        for (let i = 0; i <= nSpans; i++) {
          const py = ya + ((yb - ya) * i) / nSpans;
          grp.add(makeBox(xm - postHalf, py - postHalf, xm + postHalf, py + postHalf, zFloor, zTopRail1, MATS.aluDark, false));
        }
        grp.add(makeBox(xm - 0.012, ya + 0.01, xm + 0.012, yb - 0.01, zBotRail1, zTopRail0, MATS.glassRailing, false));
      }
    }

    function buildLaundryLouverScreens(f) {
      if (!['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8'].includes(f.id)) return;
      const z0 = f.zFloor + 0.08;
      const z1 = f.zCeil - 0.08;
      const lGrp = new THREE.Group();

      // 1. North-West Laundry Louver Screen (מסתור כביסה צפון-מערב: X = [-9.65, -7.20], Z = -4.22)
      const nwx0 = -9.65, nwx1 = -7.20, nwz = -4.22;
      lGrp.add(makeBox(nwx0, nwz - 0.04, nwx0 + 0.05, nwz + 0.02, z0, z1, MATS.louverBronze, false));
      lGrp.add(makeBox(nwx1 - 0.05, nwz - 0.04, nwx1, nwz + 0.02, z0, z1, MATS.louverBronze, false));
      for (let z = z0 + 0.06; z < z1 - 0.04; z += 0.11) {
        lGrp.add(makeBox(nwx0, nwz - 0.03, nwx1, nwz + 0.02, z, z + 0.045, MATS.louverBronze, false));
      }

      // 2. East Laundry Louver Screen (מסתור כביסה מזרח: X = +13.14, Z = [-1.05, +0.95])
      const ex = 13.14, ez0 = -1.05, ez1 = 0.95;
      lGrp.add(makeBox(ex - 0.02, ez0, ex + 0.04, ez0 + 0.05, z0, z1, MATS.louverBronze, false));
      lGrp.add(makeBox(ex - 0.02, ez1 - 0.05, ex + 0.04, ez1, z0, z1, MATS.louverBronze, false));
      for (let z = z0 + 0.06; z < z1 - 0.04; z += 0.11) {
        lGrp.add(makeBox(ex - 0.02, ez0, ex + 0.03, ez1, z, z + 0.045, MATS.louverBronze, false));
      }

      addToFloorAndLayer(f.id, 'pergolas', lGrp);
    }

    function buildCoreStairsAndElevator(f) {
      const z0 = f.zFloor;
      const z1 = f.zTop;
      const h = z1 - z0;
      const cGrp = new THREE.Group();

      // 1. Elevator Car & Stainless Doors in Shaft (inner X = [+2.425, +4.175], Z = [-4.000, -2.200])
      if (f.id !== 'gag') {
        cGrp.add(makeBox(2.46, -3.96, 4.14, -2.24, z0 + 0.01, z0 + 0.08, MATS.aluDark, false));
        cGrp.add(makeBox(2.90, -2.22, 3.80, -2.02, z0, Math.min(z0 + 2.10, f.zCeil - 0.10), MATS.mamadSteel, false));
      }

      // 2. 3D Stepped Concrete Staircase inside Protected Stairwell (inner X = [-3.275, +0.225], Z = [-4.000, -0.400])
      if (f.id !== 'gag' && h > 1.0) {
        const zMid = z0 + h * 0.50;
        // North Half-Landing (X = [-3.25, +0.20], Z = [-3.98, -2.85])
        cGrp.add(makeBox(-3.25, -3.98, 0.20, -2.85, zMid - 0.14, zMid, MATS.slabFloor, false));
        // West Flight ascending North (X = [-3.20, -1.65], Z = [-0.65 .. -2.85])
        const nSteps = 9;
        for (let i = 0; i < nSteps; i++) {
          const sz0 = -0.65 - (2.20 * i) / nSteps;
          const sz1 = -0.65 - (2.20 * (i + 1)) / nSteps;
          const stepTop = z0 + ((zMid - z0) * (i + 1)) / nSteps;
          cGrp.add(makeBox(-3.20, sz1, -1.65, sz0, stepTop - 0.16, stepTop, MATS.slabFloor, false));
        }
        // East Flight ascending South (X = [-1.40, +0.18], Z = [-2.85 .. -0.65])
        for (let i = 0; i < nSteps; i++) {
          const sz0 = -2.85 + (2.20 * i) / nSteps;
          const sz1 = -2.85 + (2.20 * (i + 1)) / nSteps;
          const stepTop = zMid + ((z1 - zMid) * (i + 1)) / nSteps;
          cGrp.add(makeBox(-1.40, sz0, 0.18, sz1, stepTop - 0.16, stepTop, MATS.slabFloor, false));
        }
      }
      addToFloorAndLayer(f.id, 'slabs', cGrp);
    }

    // =========================================================================
    // 5. BUILD ALL 14 FLOORS + 19 UNDERGROUND PARKING STALLS (FEIERBERG 3)
    // =========================================================================
    let parkingHighlightMesh = null;

    function createParkingStallMesh(st) {
      const grp = new THREE.Group();
      const zP = st.z + 0.02;
      const c = document.createElement('canvas');
      c.width = 128; c.height = 256;
      const ctx = c.getContext('2d');
      ctx.fillStyle = 'rgba(30, 41, 59, 0.72)';
      ctx.fillRect(6, 6, 116, 244);
      ctx.strokeStyle = '#fbbf24';
      ctx.lineWidth = 5;
      ctx.strokeRect(6, 6, 116, 244);
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 34px "Segoe UI", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('P-' + st.num, 64, 130);
      const tex = new THREE.CanvasTexture(c);
      const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, side: THREE.DoubleSide, clippingPlanes });
      const geo = new THREE.PlaneGeometry(st.w, st.d);
      geo.rotateX(-Math.PI / 2);
      const m = new THREE.Mesh(geo, mat);
      m.position.set(st.x, zP, st.y);
      grp.add(m);
      return grp;
    }

    function buildArchitecturalFacadeFrames(f) {
      const pGrp = new THREE.Group();
      const zF = f.zFloor;
      const zC = f.zCeil;
      const zTop = f.zTop;

      if (f.id === 'kar') {
        // Ground Floor Structural Columns along Feierberg St. South Facade (+Z = +4.20)
        [-13.00, -9.40, -5.00, -2.35, 3.35, 9.35, 10.35].forEach(cx => {
          pGrp.add(makeBox(cx - 0.18, 3.92, cx + 0.18, 4.25, 0.00, 3.25, MATS.extWall, true, true));
        });
        addToFloorAndLayer('kar', 'pergolas', pGrp);
        return;
      }

      // 2-Story Dark Charcoal Architectural C-Frames on Typical Floors (1-2, 3-4, 5-6, 7-8)
      const flNum = parseInt(f.id.replace('f', ''), 10);
      if (flNum >= 1 && flNum <= 8) {
        // Vertical dark charcoal accent piers framing West & East window bays on South (+Z) and North (-Z)
        [-13.16, -6.10, 9.35, 13.02].forEach(px => {
          pGrp.add(makeBox(px, 4.16, px + 0.16, 4.30, zF - 0.20, zTop, MATS.bronzePortal, true, true));
          pGrp.add(makeBox(px, -4.30, px + 0.16, -4.16, zF - 0.20, zTop, MATS.bronzePortal, true, true));
        });
        // Horizontal 2-story C-frame bands at bottoms of odd floors (1, 3, 5, 7) and tops of even floors (2, 4, 6, 8)
        if (flNum % 2 === 1) {
          pGrp.add(makeBox(-13.16, 4.16, -5.94, 4.32, zF - 0.22, zF + 0.04, MATS.bronzePortal, true, true));
          pGrp.add(makeBox(9.35, 4.16, 13.18, 4.32, zF - 0.22, zF + 0.04, MATS.bronzePortal, true, true));
        } else {
          pGrp.add(makeBox(-13.16, 4.16, -5.94, 4.32, zC - 0.06, zTop + 0.04, MATS.bronzePortal, true, true));
          pGrp.add(makeBox(9.35, 4.16, 13.18, 4.32, zC - 0.06, zTop + 0.04, MATS.bronzePortal, true, true));
        }
        // Central Privacy Divider Wall between West & East South Sun Balconies (X = [1.55, 1.70], Z = [4.20, 5.80])
        pGrp.add(makeBox(1.55, 4.20, 1.70, 5.80, zF, zC, MATS.extWall, true, true));
      }

      // Extrude overhead Pergola beams on Floor 8 & Floor 9 from `pergola_polys`
      const pData = PLANS[f.sheet];
      if (pData && pData.pergola_polys && pData.pergola_polys.length > 0) {
        const pz0 = zC - 0.16;
        const pz1 = zC + 0.02;
        pData.pergola_polys.forEach(pp => {
          pGrp.add(buildExtrudedTriPoly(pp, pz0, pz1, MATS.aluDark, MATS.aluDark));
        });
      }

      if (pGrp.children.length > 0) {
        addToFloorAndLayer(f.id, 'pergolas', pGrp);
      }
    }

    function buildFloorSlabsAndBalconies(f) {
      const zF = f.zFloor;
      const sThick = 0.22;
      const pData = PLANS[f.sheet];
      if (!pData) return;

      if (f.id === 'b2' || f.id === 'b1') {
        addToFloorAndLayer(f.id, 'site', buildExtrudedTriPoly(pData.slab_poly, zF - 0.30, zF, MATS.basementConcrete, MATS.basementConcrete));
        const stallsGrp = new THREE.Group();
        PARKING_STALLS.filter(st => st.level === f.id).forEach(st => {
          stallsGrp.add(createParkingStallMesh(st));
        });
        addToFloorAndLayer(f.id, 'site', stallsGrp);
        buildCoreStairsAndElevator(f);
        return;
      }

      if (f.id === 'kar') {
        const siteGrp = new THREE.Group();
        const curbMat = new THREE.MeshStandardMaterial({ color: 0xcbd5e1, roughness: 0.65, metalness: 0.05, clippingPlanes });
        const markRedMat = new THREE.MeshBasicMaterial({ color: 0xef4444, transparent: true, opacity: 0.92, side: THREE.DoubleSide, clippingPlanes });

        // 1. Statutory Lot 193 in Gush 6387 (33.50m x 16.40m: X = [-16.75, +16.75], Z = [-8.20, +8.20])
        const lotPts = [[-16.75, -8.20], [16.75, -8.20], [16.75, 8.20], [-16.75, 8.20]];
        siteGrp.add(buildPolygonSlab(lotPts, -0.06, -0.01, MATS.sidewalk, MATS.sidewalk));

        // Red statutory lot boundary line (1G-2G-3G-4G)
        siteGrp.add(makeBox(-16.75, -8.20, 16.75, -8.06, 0.01, 0.05, markRedMat, false));
        siteGrp.add(makeBox(-16.75,  8.06, 16.75,  8.20, 0.01, 0.05, markRedMat, false));
        siteGrp.add(makeBox(-16.75, -8.20, -16.61, 8.20, 0.01, 0.05, markRedMat, false));
        siteGrp.add(makeBox( 16.61, -8.20,  16.75, 8.20, 0.01, 0.05, markRedMat, false));

        // 2. Landscaped Gardens & Setbacks per 1:100 Ground Floor Site Plan:
        // South-West Garden (X=[-16.60, -2.50], Z=[+4.20, +8.05])
        siteGrp.add(makeBox(-16.60, 4.20, -2.50, 8.05, -0.01, 0.05, MATS.grass));
        // South-East Garden (X=[+3.50, +13.12], Z=[+4.20, +8.05])
        siteGrp.add(makeBox(  3.50, 4.20, 13.12, 8.05, -0.01, 0.05, MATS.grass));
        // West Garden Strip (X=[-16.60, -13.125], Z=[-8.05, +4.20], 3.62m setback)
        siteGrp.add(makeBox(-16.60, -8.05, -13.125, 4.20, -0.01, 0.05, MATS.grass));
        // North-West Rear Garden (X=[-13.125, -4.50], Z=[-8.05, -4.20], 4.00m setback)
        siteGrp.add(makeBox(-13.125, -8.05, -4.50, -4.20, -0.01, 0.05, MATS.grass));
        // Pedestrian Entrance Walkway from Feierberg St. (+Z = +8.20) to Main Lobby (+Z = +4.20)
        siteGrp.add(makeBox(-2.50, 4.20, 3.50, 8.20, -0.005, 0.025, MATS.luxTravertine));

        // 3. East Driveway & North-Rear Underground Parking Ramp (per 1:100 Site Plan: 3.63m East setback + 4.00m North setback)
        siteGrp.add(makeBox(13.125, -8.05, 16.60, 8.20, -0.45, -0.005, MATS.basementConcrete));
        siteGrp.add(makeBox(-4.50, -8.05, 13.125, -4.20, -1.65, -0.01, MATS.basementConcrete));
        siteGrp.add(makeBox(13.00, -4.20, 13.16, 8.05, 0.00, 1.05, MATS.extWall, true, true));
        siteGrp.add(makeBox(-4.50, -4.35, 13.16, -4.18, 0.00, 1.05, MATS.extWall, true, true));

        // 4. Feierberg Street (רחוב פאירברג 3 — דרך 10.00 מ' סטטוטורית: Z = +8.20 to +18.20)
        siteGrp.add(makeBox(-28.0, 8.20, 28.0, 10.20, -0.10, -0.01, MATS.sidewalk));
        siteGrp.add(makeBox(-28.0, 10.20, 28.0, 10.38, -0.10, 0.02, curbMat));
        siteGrp.add(makeBox(-28.0, 10.38, 28.0, 16.42, -0.15, -0.06, MATS.asphalt));
        siteGrp.add(makeBox(-28.0, 16.42, 28.0, 16.60, -0.10, 0.02, curbMat));
        siteGrp.add(makeBox(-28.0, 16.60, 28.0, 18.20, -0.10, -0.01, MATS.sidewalk));
        for (let sx = -24.0; sx <= 24.0; sx += 4.2) {
          siteGrp.add(makeBox(sx, 13.32, sx + 2.2, 13.48, -0.058, -0.052, MATS.extWall, false));
        }

        // 5. Enclosed Ground Floor Slab
        addToFloorAndLayer('kar', 'slabs', buildExtrudedTriPoly(pData.slab_poly, -0.25, 0.00, MATS.slabEdge, MATS.slabFloor));
        addToFloorAndLayer('kar', 'site', siteGrp);
        buildArchitecturalFacadeFrames(f);
        buildCoreStairsAndElevator(f);
        return;
      }

      if (f.id === 'gag') {
        const phSlab = PLANS['floor_10'] ? PLANS['floor_10'].slab_poly : pData.slab_poly;
        if (phSlab) {
          addToFloorAndLayer('gag', 'slabs', buildExtrudedTriPoly(phSlab, 34.97, 35.17, MATS.extWall, MATS.terraceFloor, null, null, MATS.slabSoffit));
          const pGrp = new THREE.Group();
          pGrp.add(buildExtrudedTriPoly(pData.slab_poly, 37.30, 37.50, MATS.extWall, MATS.extWall));
          pGrp.add(makeBox(2.225, -4.20, 4.375, -2.00, 35.17, 37.50, MATS.extWall, true, true));
          addToFloorAndLayer('gag', 'walls', pGrp);
        }
        const bGrp = new THREE.Group();
        (pData.railing_segs || []).forEach(seg => {
          buildRailingSegment(bGrp, seg[0], seg[1], seg[2], seg[3], 35.17, 1.10);
        });
        addToFloorAndLayer('gag', 'balconies', bGrp);
        return;
      }

      // Residential Floors f1..f10:
      addToFloorAndLayer(f.id, 'slabs', buildExtrudedTriPoly(pData.slab_poly, zF - sThick, zF, MATS.extWall, MATS.slabFloor, null, null, MATS.slabSoffit));

      if (pData.balc_polys && pData.balc_polys.length > 0) {
        const bGrp = new THREE.Group();
        pData.balc_polys.forEach(bp => {
          bGrp.add(buildExtrudedTriPoly(bp, zF - 0.24, zF + 0.02, MATS.extWall, MATS.woodDeck, null, null, MATS.slabSoffit));
        });
        (pData.railing_segs || []).forEach(seg => {
          buildRailingSegment(bGrp, seg[0], seg[1], seg[2], seg[3], zF + 0.02, 1.05);
        });
        addToFloorAndLayer(f.id, 'balconies', bGrp);
      }

      buildArchitecturalFacadeFrames(f);
      buildLaundryLouverScreens(f);
      buildCoreStairsAndElevator(f);
    }

    const hlGeo = new THREE.BoxGeometry(2.60, 1.45, 4.90);
    const hlMat = new THREE.MeshBasicMaterial({ color: 0x10b981, transparent: true, opacity: 0.48 });
    parkingHighlightMesh = new THREE.Mesh(hlGeo, hlMat);
    parkingHighlightMesh.visible = false;
    scene.add(parkingHighlightMesh);

    // =========================================================================
    // 5B. EXACT 1:1 3D INTERIOR FURNITURE, KITCHEN & SANITARY ENGINE
    // =========================================================================
    function makeCylinder(x, y, rTop, rBot, z0, z1, mat, segs = 18) {
      const h = Math.abs(z1 - z0);
      const geo = new THREE.CylinderGeometry(rTop, rBot, h, segs);
      const m = new THREE.Mesh(geo, mat);
      m.position.set(x, 0.5 * (z0 + z1), y);
      m.castShadow = true;
      m.receiveShadow = true;
      return m;
    }

    function buildDWGFurnitureItem(grp, item, zF, zC) {
      const { kind, x0, y0, x1, y1, rot } = item;
      const cx = 0.5 * (x0 + x1);
      const cy = 0.5 * (y0 + y1);
      const w = Math.abs(x1 - x0);
      const d = Math.abs(y1 - y0);
      const r = (((rot || 0) % 360) + 360) % 360;

      if (kind === 'sofa_west_f4') {
        // Exact West Apartment Living Room from FA-p1-8.pdf:
        // Rug: X=[-2.10, +0.90], Z=[+1.00, +3.45]
        grp.add(makeBox(-2.10, 1.00, 0.90, 3.45, zF + 0.012, zF + 0.025, MATS.luxRug, false));
        // 3-Seat Sofa on West side facing East TV (X=[-2.44, -1.70], Z=[1.20, 3.15])
        grp.add(makeBox(-2.44, 1.20, -1.70, 3.15, zF + 0.02, zF + 0.42, MATS.luxBoucle));
        grp.add(makeBox(-2.44, 1.20, -2.24, 3.15, zF + 0.42, zF + 0.78, MATS.luxBoucle));
        grp.add(makeBox(-2.44, 1.20, -1.70, 1.38, zF + 0.42, zF + 0.64, MATS.luxBoucle));
        grp.add(makeBox(-2.44, 2.97, -1.70, 3.15, zF + 0.42, zF + 0.64, MATS.luxBoucle));
        // 2-Seat Sofa on South side facing North (X=[-1.60, -0.05], Z=[3.15, 3.92])
        grp.add(makeBox(-1.60, 3.15, -0.05, 3.92, zF + 0.02, zF + 0.42, MATS.luxBoucle));
        grp.add(makeBox(-1.60, 3.72, -0.05, 3.92, zF + 0.42, zF + 0.78, MATS.luxBoucle));
        grp.add(makeBox(-1.60, 3.15, -1.42, 3.92, zF + 0.42, zF + 0.64, MATS.luxBoucle));
        grp.add(makeBox(-0.23, 3.15, -0.05, 3.92, zF + 0.42, zF + 0.64, MATS.luxBoucle));
        // Round Coffee Table at exact center (-0.85, 2.17) r=0.45m
        grp.add(makeCylinder(-0.85, 2.17, 0.44, 0.44, zF + 0.34, zF + 0.39, MATS.luxCalacatta, 24));
        grp.add(makeCylinder(-0.85, 2.17, 0.24, 0.24, zF + 0.02, zF + 0.34, MATS.luxFlutedOak, 20));

      } else if (kind === 'sofa_east_f4') {
        // Exact East Apartment Living Room from FA-p1-8.pdf:
        // Rug: X=[+2.20, +4.40], Z=[+1.35, +3.55]
        grp.add(makeBox(2.20, 1.35, 4.40, 3.55, zF + 0.012, zF + 0.025, MATS.luxRug, false));
        // 3-Seat Sofa on East side facing West TV (X=[+3.70, +4.44], Z=[1.35, 3.30])
        grp.add(makeBox(3.70, 1.35, 4.44, 3.30, zF + 0.02, zF + 0.42, MATS.luxBoucle));
        grp.add(makeBox(4.24, 1.35, 4.44, 3.30, zF + 0.42, zF + 0.78, MATS.luxBoucle));
        grp.add(makeBox(3.70, 1.35, 4.44, 1.53, zF + 0.42, zF + 0.64, MATS.luxBoucle));
        grp.add(makeBox(3.70, 3.12, 4.44, 3.30, zF + 0.42, zF + 0.64, MATS.luxBoucle));
        // 2-Seat Sofa on South side facing North (X=[+2.35, +3.65], Z=[3.18, 3.95])
        grp.add(makeBox(2.35, 3.18, 3.65, 3.95, zF + 0.02, zF + 0.42, MATS.luxBoucle));
        grp.add(makeBox(2.35, 3.75, 3.65, 3.95, zF + 0.42, zF + 0.78, MATS.luxBoucle));
        grp.add(makeBox(2.35, 3.18, 2.53, 3.95, zF + 0.42, zF + 0.64, MATS.luxBoucle));
        grp.add(makeBox(3.47, 3.18, 3.65, 3.95, zF + 0.42, zF + 0.64, MATS.luxBoucle));
        // Round Coffee Table at exact center (+2.95, 2.25) r=0.42m
        grp.add(makeCylinder(2.95, 2.25, 0.42, 0.42, zF + 0.34, zF + 0.39, MATS.luxCalacatta, 24));
        grp.add(makeCylinder(2.95, 2.25, 0.22, 0.22, zF + 0.02, zF + 0.34, MATS.luxFlutedOak, 20));

      } else if (kind === 'sofa') {
        grp.add(makeBox(x0 - 0.15, y0 - 0.15, x1 + 0.15, y1 + 0.15, zF + 0.012, zF + 0.025, MATS.luxRug, false));
        grp.add(makeBox(x0, y0, x0 + 0.88, y1, zF + 0.02, zF + 0.42, MATS.luxBoucle));
        grp.add(makeBox(x0, y0, x0 + 0.20, y1, zF + 0.42, zF + 0.78, MATS.luxBoucle));
        grp.add(makeBox(x0, y1 - 0.88, x1, y1, zF + 0.02, zF + 0.42, MATS.luxBoucle));
        grp.add(makeBox(x0, y1 - 0.20, x1, y1, zF + 0.42, zF + 0.78, MATS.luxBoucle));
        const tx = x0 + 1.50, ty = y0 + 0.95;
        grp.add(makeCylinder(tx, ty, 0.40, 0.40, zF + 0.34, zF + 0.39, MATS.luxCalacatta, 22));
        grp.add(makeCylinder(tx, ty, 0.22, 0.22, zF + 0.02, zF + 0.34, MATS.luxFlutedOak, 18));

      } else if (kind === 'dining_ns') {
        // North-South Dining Table with 3 chairs on West side and 3 chairs on East side (exact FA-p1-8.pdf layout!)
        grp.add(makeBox(x0, y0, x1, y1, zF + 0.72, zF + 0.77, MATS.luxCalacatta));
        grp.add(makeCylinder(cx, cy - d * 0.25, 0.11, 0.15, zF + 0.02, zF + 0.72, MATS.luxFlutedOak, 16));
        grp.add(makeCylinder(cx, cy + d * 0.25, 0.11, 0.15, zF + 0.02, zF + 0.72, MATS.luxFlutedOak, 16));
        for (let i = 0; i < 3; i++) {
          const sy = y0 + (i + 0.5) * (d / 3.0);
          // West chair + backrest
          grp.add(makeBox(x0 - 0.26, sy - 0.18, x0 - 0.03, sy + 0.18, zF + 0.42, zF + 0.47, MATS.luxBoucle));
          grp.add(makeBox(x0 - 0.28, sy - 0.18, x0 - 0.22, sy + 0.18, zF + 0.47, zF + 0.82, MATS.luxFlutedOak));
          // East chair + backrest
          grp.add(makeBox(x1 + 0.03, sy - 0.18, x1 + 0.26, sy + 0.18, zF + 0.42, zF + 0.47, MATS.luxBoucle));
          grp.add(makeBox(x1 + 0.22, sy - 0.18, x1 + 0.28, sy + 0.18, zF + 0.47, zF + 0.82, MATS.luxFlutedOak));
        }

      } else if (kind === 'dining') {
        grp.add(makeBox(x0, y0, x1, y1, zF + 0.72, zF + 0.77, MATS.luxCalacatta));
        grp.add(makeCylinder(cx - w * 0.22, cy - d * 0.22, 0.11, 0.15, zF + 0.02, zF + 0.72, MATS.luxFlutedOak, 16));
        grp.add(makeCylinder(cx + w * 0.22, cy + d * 0.22, 0.11, 0.15, zF + 0.02, zF + 0.72, MATS.luxFlutedOak, 16));
        for (let i = 0; i < 3; i++) {
          const sx = x0 + (i + 0.5) * (w / 3.0);
          grp.add(makeBox(sx - 0.18, y0 - 0.30, sx + 0.18, y0 - 0.04, zF + 0.42, zF + 0.47, MATS.luxBoucle));
          grp.add(makeBox(sx - 0.18, y1 + 0.04, sx + 0.18, y1 + 0.30, zF + 0.42, zF + 0.47, MATS.luxBoucle));
        }

      } else if (kind === 'tv') {
        const padX = (w < d) ? 0.10 : 0.04;
        const padY = (d < w) ? 0.10 : 0.04;
        grp.add(makeBox(x0 - padX, y0 - padY, x1 + padX, y1 + padY, zF + 0.04, zF + 0.48, MATS.luxFlutedOak));
        grp.add(makeBox(x0, y0, x1, y1, zF + 0.55, zF + 1.35, MATS.aluDark));

      } else if (kind === 'bed_double') {
        grp.add(makeBox(x0, y0, x1, y1, zF + 0.05, zF + 0.28, MATS.luxOakSmooth));
        grp.add(makeBox(x0 + 0.05, y0 + 0.05, x1 - 0.05, y1 - 0.05, zF + 0.28, zF + 0.48, MATS.luxCeramic));
        if (Math.abs(r - 90) < 25) {
          grp.add(makeBox(x0, y0 - 0.10, x0 + 0.12, y1 + 0.10, zF + 0.02, zF + 0.96, MATS.luxFlutedOak));
          grp.add(makeBox(x0 + 0.50, y0 + 0.05, x1 - 0.05, y1 - 0.05, zF + 0.29, zF + 0.50, MATS.luxTaupe));
        } else if (Math.abs(r - 270) < 25) {
          grp.add(makeBox(x1 - 0.12, y0 - 0.10, x1, y1 + 0.10, zF + 0.02, zF + 0.96, MATS.luxFlutedOak));
          grp.add(makeBox(x0 + 0.05, y0 + 0.05, x1 - 0.50, y1 - 0.05, zF + 0.29, zF + 0.50, MATS.luxTaupe));
        } else if (Math.abs(r - 180) < 25) {
          grp.add(makeBox(x0 - 0.10, y0, x1 + 0.10, y0 + 0.12, zF + 0.02, zF + 0.96, MATS.luxFlutedOak));
          grp.add(makeBox(x0 + 0.05, y0 + 0.50, x1 - 0.05, y1 - 0.05, zF + 0.29, zF + 0.50, MATS.luxTaupe));
        } else {
          grp.add(makeBox(x0 - 0.10, y1 - 0.12, x1 + 0.10, y1, zF + 0.02, zF + 0.96, MATS.luxFlutedOak));
          grp.add(makeBox(x0 + 0.05, y0 + 0.05, x1 - 0.05, y1 - 0.50, zF + 0.29, zF + 0.50, MATS.luxTaupe));
        }

      } else if (kind === 'bed_single') {
        grp.add(makeBox(x0, y0, x1, y1, zF + 0.05, zF + 0.26, MATS.luxOakSmooth));
        grp.add(makeBox(x0 + 0.04, y0 + 0.04, x1 - 0.04, y1 - 0.04, zF + 0.26, zF + 0.44, MATS.luxCeramic));
        grp.add(makeBox(x0, y0, x0 + 0.10, y1, zF + 0.02, zF + 0.82, MATS.luxFlutedOak));

      } else if (kind === 'wardrobe') {
        grp.add(makeBox(x0, y0, x1, y1, zF + 0.02, zF + 2.25, MATS.luxCabinet));
        grp.add(makeBox(x0 + 0.01, y0 + 0.01, x1 - 0.01, y1 - 0.01, zF + 2.25, zF + 2.30, MATS.luxFlutedOak));

      } else if (kind === 'desk') {
        grp.add(makeBox(x0, y0, x1, y1, zF + 0.71, zF + 0.75, MATS.luxOakSmooth));
        grp.add(makeCylinder(cx, cy, 0.22, 0.22, zF + 0.42, zF + 0.47, MATS.luxBoucle, 14));

      } else if (kind === 'kcounter') {
        grp.add(makeBox(x0, y0, x1, y1, zF + 0.02, zF + 0.88, MATS.luxCabinet));
        grp.add(makeBox(x0 - 0.015, y0 - 0.015, x1 + 0.015, y1 + 0.015, zF + 0.88, zF + 0.92, MATS.luxCalacatta));

      } else if (kind === 'fridge') {
        grp.add(makeBox(x0, y0, x1, y1, zF + 0.02, zF + 2.08, MATS.aluDark));

      } else if (kind === 'stove') {
        grp.add(makeBox(x0 + 0.04, y0 + 0.04, x1 - 0.04, y1 - 0.04, zF + 0.92, zF + 0.935, MATS.aluDark));

      } else if (kind === 'ksink') {
        grp.add(makeBox(x0, y0, x1, y1, zF + 0.89, zF + 0.928, MATS.mamadSteel));
        grp.add(makeCylinder(cx, cy, 0.025, 0.025, zF + 0.92, zF + 1.18, MATS.luxBrass, 12));

      } else if (kind === 'bathtub') {
        grp.add(makeBox(x0, y0, x1, y1, zF + 0.02, zF + 0.54, MATS.luxCeramic));
        grp.add(makeBox(x0 + 0.08, y0 + 0.08, x1 - 0.08, y1 - 0.08, zF + 0.46, zF + 0.55, MATS.waterSpa));

      } else if (kind === 'shower') {
        grp.add(makeBox(x0, y0, x1, y1, zF + 0.01, zF + 0.05, MATS.luxTravertine));
        grp.add(makeBox(x0, y0, x1, y0 + 0.02, zF + 0.05, zF + 2.05, MATS.glassRailing, false));
        grp.add(makeBox(x0, y0, x0 + 0.02, y1, zF + 0.05, zF + 2.05, MATS.glassRailing, false));

      } else if (kind === 'vanity') {
        grp.add(makeBox(x0, y0, x1, y1, zF + 0.28, zF + 0.82, MATS.luxFlutedOak));
        grp.add(makeBox(x0 - 0.01, y0 - 0.01, x1 + 0.01, y1 + 0.01, zF + 0.82, zF + 0.86, MATS.luxCalacatta));
        grp.add(makeCylinder(cx, cy, 0.18, 0.14, zF + 0.86, zF + 0.96, MATS.luxCeramic, 16));

      } else if (kind === 'toilet') {
        grp.add(makeBox(x0 + 0.04, y0 + 0.04, x1 - 0.04, y1 - 0.04, zF + 0.08, zF + 0.43, MATS.luxCeramic));

      } else if (kind === 'washer') {
        grp.add(makeBox(x0 + 0.02, y0 + 0.02, x1 - 0.02, y1 - 0.02, zF + 0.02, zF + 0.87, MATS.luxCeramic));

      } else if (kind === 'solar_panel') {
        grp.add(makeBox(x0, y0, x1, y1, zF + 0.05, zF + 0.65, MATS.solarPanel));
      }
    }

    function buildBalconyLounge(grp, bx, by, bw, zF) {
      grp.add(makeBox(bx - 0.65, by - 0.35, bx + 0.65, by + 0.35, zF + 0.03, zF + 0.38, MATS.luxBoucle));
      grp.add(makeCylinder(bx, by + 0.48, 0.28, 0.22, zF + 0.03, zF + 0.38, MATS.luxCalacatta, 18));
      [-bw * 0.35, bw * 0.35].forEach(px => {
        grp.add(makeCylinder(bx + px, by, 0.20, 0.15, zF + 0.03, zF + 0.48, MATS.luxCeramic, 16));
        grp.add(makeCylinder(bx + px, by, 0.32, 0.18, zF + 0.48, zF + 1.25, MATS.luxPlantOlive, 14));
      });
    }

    function buildFloorInteriors(f, pData) {
      const fGrp = new THREE.Group();
      const zF = f.zFloor;
      const zC = f.zCeil;

      (pData.furn_items || []).forEach(item => {
        buildDWGFurnitureItem(fGrp, item, zF, zC);
      });

      if (f.id === 'f4') {
        buildBalconyLounge(fGrp, -2.20, 4.95, 5.5, zF);
        buildBalconyLounge(fGrp,  5.40, 4.95, 5.5, zF);
      }

      addToFloorAndLayer(f.id, 'furn3d', fGrp);
    }

    function buildAllFloors() {
      FLOORS.forEach(f => {
        const pData = PLANS[f.sheet];
        if (!pData) return;

        buildFloorSlabsAndBalconies(f);

        const isBasement = (f.id === 'b1' || f.id === 'b2');
        const isPenthouse = (f.id === 'f9' || f.id === 'f10');
        const extMat = isBasement ? null : (isPenthouse ? MATS.penthouseWall : MATS.extWall);

        pData.wall_polys.forEach(wp => {
          const z0 = f.zFloor;
          const z1 = f.zCeil;
          const wMesh = buildExtrudedTriPoly(wp, z0, z1, isBasement ? MATS.basementConcrete : MATS.wall, MATS.wallCap, f.sheet, extMat);
          addToFloorAndLayer(f.id, isBasement ? 'site' : 'walls', wMesh);
        });

        (pData.openings || []).forEach(op => {
          buildOpening3D(f, op);
        });

        if (f.has3DFurn) {
          buildFloorInteriors(f, pData);
        }

        // 1. 2D CAD Architectural Lines on the Floor
        const zCad = f.zFloor + 0.021;
        const cPts = [];
        (pData.cad_lines || []).forEach(s => {
          cPts.push(s[0], zCad, s[1], s[2], zCad, s[3]);
        });
        if (cPts.length > 0) {
          const cGeo = new THREE.BufferGeometry();
          cGeo.setAttribute('position', new THREE.Float32BufferAttribute(cPts, 3));
          const cLines = new THREE.LineSegments(cGeo, MATS.lineCad);
          addToFloorAndLayer(f.id, 'cad2d', cLines);
        }

        // 2. 2D Furniture Plan Lines on the Floor
        const zFurn = f.zFloor + 0.024;
        const fPts = [];
        (pData.furn_lines || []).forEach(s => {
          fPts.push(s[0], zFurn, s[1], s[2], zFurn, s[3]);
        });
        if (fPts.length > 0) {
          const fGeo = new THREE.BufferGeometry();
          fGeo.setAttribute('position', new THREE.Float32BufferAttribute(fPts, 3));
          const fLines = new THREE.LineSegments(fGeo, MATS.lineFurn);
          addToFloorAndLayer(f.id, 'furn3d', fLines);
        }

        (pData.room_labels || []).forEach(rl => {
          const ry = (typeof rl.y === 'number') ? rl.y : rl.z;
          const lblMesh = createFloorLabelMesh(rl.name, rl.dims || '', rl.x, ry, f.zFloor);
          addToFloorAndLayer(f.id, 'labels', lblMesh);
        });
      });
    }

    buildAllFloors();
"""

HTML_PART2B = r"""
    // =========================================================================
    // 6. GEOREFERENCED TRIPLE-RESOLUTION GOOGLE MAPS HYBRID PLANES OF PETAH TIKVA
    //    + 8 CONCENTRIC DISTANCE RINGS + 28 VERIFIED POIS AROUND FEIERBERG 3
    // =========================================================================
    // Exact ITM-Surveyed Center of Parcel 193 in Gush 6387 (ITM E=189354.66, N=665000.12)
    const CENTER_LAT = 32.0778960;
    const CENTER_LON = 34.8856068;
    const R_MERC = 6378137.0;
    const LAT0_RAD = CENTER_LAT * Math.PI / 180.0;
    const LON0_RAD = CENTER_LON * Math.PI / 180.0;
    const COS_LAT0 = Math.cos(LAT0_RAD);
    const MERC_Y0  = Math.asinh(Math.tan(LAT0_RAD));

    const SCENE_CX = 0.0;
    const SCENE_CZ = 0.0;

    // +17.44 deg ENE azimuth of Feierberg St. (2G -> 1G: dE=+31.96m, dN=+10.04m)
    const GMAPS_THETA = 17.44 * Math.PI / 180.0;
    const GMAPS_CT = Math.cos(GMAPS_THETA), GMAPS_ST = Math.sin(GMAPS_THETA);

    function geoMetersTo3D(eastM, northM, y3d = -0.05) {
      const dx = eastM * GMAPS_CT + northM * GMAPS_ST;
      const dy = -eastM * GMAPS_ST + northM * GMAPS_CT;
      return new THREE.Vector3(SCENE_CX + dx, y3d, SCENE_CZ - dy);
    }

    function latLonTo3D(lat, lon, y3d = 0.35) {
      const latRad = lat * Math.PI / 180.0;
      const lonRad = lon * Math.PI / 180.0;
      const eastM = R_MERC * (lonRad - LON0_RAD) * COS_LAT0;
      const northM = R_MERC * (Math.asinh(Math.tan(latRad)) - MERC_Y0) * COS_LAT0;
      return geoMetersTo3D(eastM, northM, y3d);
    }

    function createGeoreferencedMapMesh(halfSpanM, y3d, dataUri, polyOffsetFactor) {
      const tl = geoMetersTo3D(-halfSpanM,  halfSpanM, y3d);
      const tr = geoMetersTo3D( halfSpanM,  halfSpanM, y3d);
      const br = geoMetersTo3D( halfSpanM, -halfSpanM, y3d);
      const bl = geoMetersTo3D(-halfSpanM, -halfSpanM, y3d);

      const geom = new THREE.BufferGeometry();
      geom.setAttribute('position', new THREE.Float32BufferAttribute([
        tl.x, tl.y, tl.z, bl.x, bl.y, bl.z, br.x, br.y, br.z,
        tl.x, tl.y, tl.z, br.x, br.y, br.z, tr.x, tr.y, tr.z
      ], 3));
      geom.setAttribute('uv', new THREE.Float32BufferAttribute([
        0, 1, 0, 0, 1, 0,
        0, 1, 1, 0, 1, 1
      ], 2));
      geom.computeVertexNormals();

      const tex = new THREE.TextureLoader().load(dataUri);
      tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
      const mat = new THREE.MeshBasicMaterial({
        map: tex, side: THREE.DoubleSide,
        polygonOffset: true, polygonOffsetFactor: polyOffsetFactor, polygonOffsetUnits: polyOffsetFactor
      });
      return new THREE.Mesh(geom, mat);
    }

    const gisMapPlanesGroup = new THREE.Group();
    scene.add(gisMapPlanesGroup);

    const wideGoogleMapsMesh    = createGeoreferencedMapMesh(OUTER_SPAN_M * 0.5,   -0.22, WIDE_GMAPS_DATA_URI, 6);
    const googleMapsPlaneMesh   = createGeoreferencedMapMesh(INNER_SPAN_M * 0.5,   -0.14, INNER_GMAPS_DATA_URI, 4);
    const closeupGoogleMapsMesh = createGeoreferencedMapMesh(CLOSEUP_SPAN_M * 0.5, -0.06, CLOSEUP_GMAPS_DATA_URI, 2);
    gisMapPlanesGroup.add(wideGoogleMapsMesh);
    gisMapPlanesGroup.add(googleMapsPlaneMesh);
    gisMapPlanesGroup.add(closeupGoogleMapsMesh);

    const gisLabelsContainer = document.getElementById('gis-labels-container');
    const gisActiveCard = document.getElementById('gis-active-card');
    const gisSidebarList = document.getElementById('gis-poi-sidebar-list');
    const gisRingsGroup = new THREE.Group();
    const gisPoisGroup = new THREE.Group();
    scene.add(gisRingsGroup);
    scene.add(gisPoisGroup);

    const gisRingLabelObjs = [];
    const gisPoiLabelObjs = [];
    let gisRadiiVisible = true;
    let gisPoisVisible = true;
    let gmapsVisible = true;
    let activeGisCategory = 'all';

    const GIS_RINGS_CONFIG = [
      { r: 150,  label: "150 מ' · כ-2 דק' הליכה",   hex: 0x38bdf8, css: "#0284c7" },
      { r: 300,  label: "300 מ' · כ-4 דק' הליכה",   hex: 0x10b981, css: "#059669" },
      { r: 500,  label: "500 מ' · כ-6 דק' הליכה",   hex: 0xf59e0b, css: "#d97706" },
      { r: 750,  label: "750 מ' · כ-9 דק' הליכה",   hex: 0xa855f7, css: "#7c3aed" },
      { r: 1000, label: "1,000 מ' · כ-12 דק' הליכה", hex: 0xef4444, css: "#dc2626" },
      { r: 1250, label: "1.25 ק\"מ · כ-15 דק' הליכה", hex: 0xec4899, css: "#db2777" },
      { r: 1500, label: "1.50 ק\"מ · כ-18 דק' הליכה", hex: 0x6366f1, css: "#4f46e5" },
      { r: 2000, label: "2.00 ק\"מ · 4-5 דק' נסיעה",  hex: 0x14b8a6, css: "#0d9488" }
    ];

    GIS_RINGS_CONFIG.forEach(rc => {
      const ringHalfW = rc.r >= 1000 ? 3.2 : 2.0;
      const ringGeom = new THREE.RingGeometry(rc.r - ringHalfW, rc.r + ringHalfW, 160);
      ringGeom.rotateX(-Math.PI / 2);
      const ringMat = new THREE.MeshBasicMaterial({ color: rc.hex, side: THREE.DoubleSide, transparent: true, opacity: 0.88, depthWrite: false });
      const ringMesh = new THREE.Mesh(ringGeom, ringMat);
      ringMesh.position.set(SCENE_CX, 0.35, SCENE_CZ);
      gisRingsGroup.add(ringMesh);

      const haloGeom = new THREE.RingGeometry(rc.r - 10.0, rc.r + 10.0, 160);
      haloGeom.rotateX(-Math.PI / 2);
      const haloMat = new THREE.MeshBasicMaterial({ color: rc.hex, side: THREE.DoubleSide, transparent: true, opacity: 0.16, depthWrite: false });
      const haloMesh = new THREE.Mesh(haloGeom, haloMat);
      haloMesh.position.set(SCENE_CX, 0.25, SCENE_CZ);
      gisRingsGroup.add(haloMesh);

      [0.65, -2.49].forEach(ang => {
        const el = document.createElement('div');
        el.style.cssText = `position:absolute;transform:translate(-50%,-50%);background:rgba(15,23,42,0.92);color:#ffffff;border:2px solid ${rc.css};border-radius:999px;padding:2px 10px;font-size:11px;font-weight:800;white-space:nowrap;box-shadow:0 3px 10px rgba(0,0,0,0.40);pointer-events:none;transition:opacity 0.15s;`;
        el.textContent = `⭕ ${rc.label}`;
        gisLabelsContainer.appendChild(el);
        gisRingLabelObjs.push({ el, pos: new THREE.Vector3(SCENE_CX + rc.r * Math.cos(ang), 3.0, SCENE_CZ + rc.r * Math.sin(ang)) });
      });
    });

    const GIS_CAT_STYLES = {
      education: { icon: "🎓", label: "מוסד חינוך / בית ספר", hex: 0x2563eb, css: "#2563eb" },
      transport: { icon: "🚌", label: "תחבורה ציבורית ורק\"ל", hex: 0xd97706, css: "#d97706" },
      shopping:  { icon: "🛒", label: "מרכז קניות ומסחר",    hex: 0x9333ea, css: "#9333ea" },
      parks:     { icon: "🌳", label: "פארק, ספורט וקהילה",   hex: 0x059669, css: "#059669" },
      health:    { icon: "🏥", label: "בריאות ומרפאות",       hex: 0xdc2626, css: "#dc2626" }
    };

    function focusCameraOnGisPoi(poi) {
      if (!poi) return;
      showGisActiveCard(poi);
      const p3d = latLonTo3D(poi.lat, poi.lon, 0.35);
      if (camState.walkMode) exitWalkthrough();
      selectFloor('all');
      camState.target.set(SCENE_CX + (p3d.x - SCENE_CX) * 0.48, 4.0, SCENE_CZ + (p3d.z - SCENE_CZ) * 0.48);
      const dist3D = Math.hypot(p3d.x - SCENE_CX, p3d.z - SCENE_CZ);
      camState.spherical.radius = Math.max(260, Math.min(2200, dist3D * 1.45 + 140));
      camState.spherical.phi = 0.58;
      updateCameraFromOrbit();

      gisPoiLabelObjs.forEach(item => {
        const isSel = (item.poi.id === poi.id);
        item.el.style.transform = isSel ? 'translate(-50%,-105%) scale(1.18)' : 'translate(-50%,-100%) scale(1.0)';
        item.el.style.zIndex = isSel ? '30' : '10';
        item.el.style.boxShadow = isSel ? '0 0 0 3px #fde047, 0 8px 20px rgba(0,0,0,0.6)' : '0 4px 12px rgba(0,0,0,0.40)';
        if (item.sidebarRow) {
          item.sidebarRow.style.background = isSel ? '#dbeafe' : '#ffffff';
          item.sidebarRow.style.borderColor = isSel ? '#2563eb' : '#e2e8f0';
        }
      });
    }

    function showGisActiveCard(poi) {
      if (!poi) { gisActiveCard.style.display = 'none'; return; }
      const st = GIS_CAT_STYLES[poi.cat] || GIS_CAT_STYLES.education;
      const distTxt = poi.dist_m >= 1000 ? `${(poi.dist_m / 1000).toFixed(2)} ק"מ (${poi.dist_m} מ')` : `${poi.dist_m} מטרים`;
      const gmapsUrl = `https://www.google.com/maps/dir/${CENTER_LAT},${CENTER_LON}/${poi.lat},${poi.lon}`;
      gisActiveCard.style.display = 'block';
      gisActiveCard.innerHTML = `
        <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:8px;">
          <div style="display:flex;align-items:center;gap:8px;">
            <span style="width:28px;height:28px;border-radius:999px;background:${st.css};color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;flex-shrink:0;">${poi.id}</span>
            <div>
              <div style="font-size:10px;font-weight:700;color:#93c5fd;">${st.icon} ${st.label}</div>
              <div style="font-size:14px;font-weight:800;color:#ffffff;">${poi.name}</div>
            </div>
          </div>
          <button onclick="document.getElementById('gis-active-card').style.display='none'" style="background:transparent;border:none;color:#94a3b8;cursor:pointer;font-size:15px;font-weight:800;padding:0 4px;">✕</button>
        </div>
        <div style="font-size:12px;color:#cbd5e1;margin-bottom:6px;">${poi.sub || ''}</div>
        <div style="font-size:10px;color:#94a3b8;margin-bottom:8px;font-family:monospace;">נ.צ. מאומת: ${poi.lat.toFixed(5)}°N, ${poi.lon.toFixed(5)}°E</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;background:rgba(30,41,59,0.9);border:1px solid #334155;border-radius:8px;padding:7px;text-align:center;margin-bottom:10px;">
          <div>
            <div style="font-size:10px;color:#94a3b8;">מרחק אווירי</div>
            <div style="font-size:12px;font-weight:800;color:#38bdf8;">${distTxt}</div>
          </div>
          <div style="border-right:1px solid #334155;border-left:1px solid #334155;">
            <div style="font-size:10px;color:#94a3b8;">הליכה ברגל</div>
            <div style="font-size:12px;font-weight:800;color:#34d399;">כ-${poi.walk_min} דק'</div>
          </div>
          <div>
            <div style="font-size:10px;color:#94a3b8;">נסיעה ברכב</div>
            <div style="font-size:12px;font-weight:800;color:#fbbf24;">כ-${poi.drive_min} דק'</div>
          </div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;">
          <a href="${gmapsUrl}" target="_blank" style="display:flex;align-items:center;justify-content:center;gap:4px;padding:7px 8px;border-radius:8px;background:#2563eb;color:#ffffff;font-size:11px;font-weight:800;text-decoration:none;">
            <span>מסלול ב-Google Maps</span><span>↗</span>
          </a>
          <a href="feierberg3_spatial_map.html" target="_blank" style="display:flex;align-items:center;justify-content:center;gap:4px;padding:7px 8px;border-radius:8px;background:#334155;color:#38bdf8;font-size:11px;font-weight:800;text-decoration:none;">
            <span>מפת GIS דו-ממדית</span><span>↗</span>
          </a>
        </div>
      `;
    }

    SPATIAL_POIS.forEach(poi => {
      const st = GIS_CAT_STYLES[poi.cat] || GIS_CAT_STYLES.education;
      const p3d = latLonTo3D(poi.lat, poi.lon, 0.35);
      const subGrp = new THREE.Group();
      subGrp.userData = { id: poi.id, cat: poi.cat };

      const lineGeom = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(SCENE_CX, 1.0, SCENE_CZ),
        new THREE.Vector3(p3d.x, 1.0, p3d.z)
      ]);
      subGrp.add(new THREE.Line(lineGeom, new THREE.LineBasicMaterial({ color: st.hex, transparent: true, opacity: 0.82 })));

      const scaleF = poi.dist_m > 1100 ? 1.65 : 1.0;
      const baseRingGeom = new THREE.RingGeometry(4.0 * scaleF, 9.5 * scaleF, 32);
      baseRingGeom.rotateX(-Math.PI / 2);
      const baseRingMesh = new THREE.Mesh(baseRingGeom, new THREE.MeshBasicMaterial({ color: st.hex, side: THREE.DoubleSide }));
      baseRingMesh.position.set(p3d.x, 0.50, p3d.z);
      subGrp.add(baseRingMesh);

      const baseDiscGeom = new THREE.CircleGeometry(4.0 * scaleF, 32);
      baseDiscGeom.rotateX(-Math.PI / 2);
      const baseDiscMesh = new THREE.Mesh(baseDiscGeom, new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide }));
      baseDiscMesh.position.set(p3d.x, 0.55, p3d.z);
      subGrp.add(baseDiscMesh);

      const beaconH = poi.dist_m > 1100 ? 26.0 : 16.5;
      const stemGeom = new THREE.CylinderGeometry(0.85 * scaleF, 0.85 * scaleF, beaconH, 12);
      const stemMesh = new THREE.Mesh(stemGeom, new THREE.MeshBasicMaterial({ color: st.hex }));
      stemMesh.position.set(p3d.x, beaconH / 2, p3d.z);
      subGrp.add(stemMesh);

      const headGeom = new THREE.SphereGeometry(3.8 * scaleF, 18, 18);
      const headMesh = new THREE.Mesh(headGeom, new THREE.MeshBasicMaterial({ color: st.hex }));
      headMesh.position.set(p3d.x, beaconH, p3d.z);
      subGrp.add(headMesh);

      gisPoisGroup.add(subGrp);

      const badgeEl = document.createElement('div');
      const distShort = poi.dist_m >= 1000 ? `${(poi.dist_m / 1000).toFixed(2)} ק"מ` : `${poi.dist_m} מ'`;
      badgeEl.style.cssText = `position:absolute;transform:translate(-50%,-100%);background:rgba(15,23,42,0.93);color:#ffffff;border:2px solid ${st.css};border-radius:10px;padding:3px 8px;font-size:11px;font-weight:700;white-space:nowrap;box-shadow:0 4px 12px rgba(0,0,0,0.40);pointer-events:auto;cursor:pointer;display:flex;align-items:center;gap:5px;transition:transform 0.15s,opacity 0.15s;z-index:10;`;
      badgeEl.innerHTML = `
        <span style="width:18px;height:18px;border-radius:999px;background:${st.css};color:#fff;display:inline-flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;">${poi.id}</span>
        <span>${poi.name}</span>
        <span style="background:rgba(56,189,248,0.20);color:#38bdf8;padding:1px 5px;border-radius:5px;font-weight:800;font-size:10px;">${distShort}</span>
      `;
      badgeEl.addEventListener('click', ev => { ev.stopPropagation(); focusCameraOnGisPoi(poi); });
      gisLabelsContainer.appendChild(badgeEl);

      let sidebarRow = null;
      if (gisSidebarList) {
        sidebarRow = document.createElement('div');
        sidebarRow.style.cssText = 'display:flex;align-items:center;justify-content:space-between;gap:6px;padding:5px 7px;border-radius:6px;border:1px solid #e2e8f0;background:#ffffff;cursor:pointer;font-size:11px;transition:background 0.15s;';
        sidebarRow.innerHTML = `
          <div style="display:flex;align-items:center;gap:6px;min-width:0;">
            <span style="width:18px;height:18px;border-radius:999px;background:${st.css};color:#fff;display:inline-flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;flex-shrink:0;">${poi.id}</span>
            <span style="font-weight:700;color:#0f172a;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${poi.name}</span>
          </div>
          <span style="font-weight:800;color:#0284c7;font-size:10px;white-space:nowrap;flex-shrink:0;">${distShort} · ${poi.walk_min} דק'</span>
        `;
        sidebarRow.addEventListener('click', () => {
          if (!gisPoisVisible) { gisPoisVisible = true; syncGisPoisState(); }
          focusCameraOnGisPoi(poi);
        });
        gisSidebarList.appendChild(sidebarRow);
      }

      gisPoiLabelObjs.push({ el: badgeEl, sidebarRow, poi, subGrp, pos: new THREE.Vector3(p3d.x, beaconH + 4.5, p3d.z) });
    });

    const labelsContainer = document.getElementById('labels-container');
    const exteriorCallouts = [
      { text: "פאירברג 3, פתח תקווה · 18 יח\"ד · רום גג עליון +37.50 מ'", pos: new THREE.Vector3(0.0, 38.4, 0.0), cls: "b44" },
      { text: "דופלקס-פנטהאוז קומות 9–10 (#17 ו-#18) · מרפסות גג פנורמיות", pos: new THREE.Vector3(0.0, 32.8, 3.8), cls: "ph" },
      { text: "רחוב פאירברג 3, פתח תקווה (חזית דרומית · מפלס כניסה ±0.00)", pos: new THREE.Vector3(0.0, 1.4, 13.5), cls: "street" },
      { text: "גוש 6387 חלקה 193 (548 מ\"ר) · 19 חניות ב-2 קומות מרתף (-4.80 / -7.80)", pos: new THREE.Vector3(0.0, 1.4, -10.5), cls: "" }
    ];
    let showLabels = true;
    const calloutObjs = [];
    exteriorCallouts.forEach(c => {
      const el = document.createElement('div');
      el.className = ('callout-pill ' + c.cls).trim();
      el.textContent = c.text;
      labelsContainer.appendChild(el);
      calloutObjs.push({ el, pos: c.pos });
    });

    // =========================================================================
    // 7. 18-UNIT 3D CATALOG & LIVE CRM, PDF QUOTE GENERATOR
    // =========================================================================
    const units3DGroup = new THREE.Group();
    units3DGroup.visible = false;
    scene.add(units3DGroup);

    const unitsLabelsContainer = document.getElementById('units-labels-container');
    const unitSalesCard = document.getElementById('unit-sales-card');
    const unitVolumeMeshes = [];
    const unitBadgeObjs = [];
    let units3DVisible = false;
    let showUnitPrices = true;
    let activeUnitBldgFilter = 'all';
    let activeUnitStatusFilter = 'all';
    let activeUnitRoomFilter = 'all';
    let selectedUnitObj = null;

    function formatILS(n) { return '₪' + n.toLocaleString('he-IL'); }

    YATKOVSKI_UNITS.forEach(u => {
      const [x0, y0, x1, y1] = u.bbox;
      const w = Math.abs(x1 - x0);
      const d = Math.abs(y1 - y0);
      const h = Math.abs(u.z1 - u.z0) - 0.14;
      const isAvail = (u.status === 'available');
      const colHex = isAvail ? 0x10b981 : 0x64748b;

      const geo = new THREE.BoxGeometry(w + 0.15, h, d + 0.15);
      const mat = new THREE.MeshBasicMaterial({
        color: colHex, transparent: true, opacity: isAvail ? 0.34 : 0.18,
        side: THREE.DoubleSide, depthWrite: false
      });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(0.5 * (x0 + x1), 0.5 * (u.z0 + u.z1), 0.5 * (y0 + y1));
      mesh.userData = { unit: u, baseOpacity: mat.opacity };
      units3DGroup.add(mesh);
      unitVolumeMeshes.push(mesh);

      const edges = new THREE.EdgesGeometry(geo);
      const lineMat = new THREE.LineBasicMaterial({ color: isAvail ? 0x34d399 : 0x94a3b8, transparent: true, opacity: 0.88 });
      mesh.add(new THREE.LineSegments(edges, lineMat));

      const pos3D = new THREE.Vector3(u.bx, u.bz, u.by);
      const badge = document.createElement('div');
      badge.style.cssText = 'position:absolute;transform:translate(-50%,-50%);pointer-events:auto;cursor:pointer;padding:3px 8px;border-radius:999px;font-size:10px;font-weight:800;color:#ffffff;box-shadow:0 4px 12px rgba(0,0,0,0.35);white-space:nowrap;display:none;align-items:center;gap:5px;border:1.5px solid #ffffff;transition:transform 0.12s ease;';
      badge.style.background = isAvail ? '#059669' : '#475569';
      badge.innerHTML = `<span>${u.shortBadge} (${u.rooms}חד')</span><span class="ubadge-price">${showUnitPrices && isAvail ? '· ' + formatILS(u.price) : ''}</span>`;
      badge.addEventListener('click', e => { e.stopPropagation(); selectUnitAndOpenCard(u, true); });
      unitsLabelsContainer.appendChild(badge);
      unitBadgeObjs.push({ unit: u, mesh, el: badge, pos: pos3D });
    });

    function unitMatchesFilters(u) {
      if (activeUnitBldgFilter !== 'all' && String(u.wing) !== activeUnitBldgFilter) return false;
      if (activeUnitStatusFilter !== 'all' && u.status !== activeUnitStatusFilter) return false;
      if (activeUnitRoomFilter !== 'all' && String(Math.round(u.rooms)) !== activeUnitRoomFilter) return false;
      return true;
    }

    function renderUnitsCatalogList() {
      const listEl = document.getElementById('units-catalog-list');
      if (!listEl) return;
      listEl.innerHTML = '';

      YATKOVSKI_UNITS.forEach(u => {
        const match = unitMatchesFilters(u);
        const itemObj = unitBadgeObjs.find(b => b.unit.id === u.id);
        if (itemObj) {
          itemObj.mesh.visible = match;
          const prSpan = itemObj.el.querySelector('.ubadge-price');
          if (prSpan) prSpan.textContent = (showUnitPrices && u.status === 'available') ? `· ${formatILS(u.price)}` : '';
        }
        if (!match) return;

        const row = document.createElement('div');
        const isSel = selectedUnitObj && selectedUnitObj.id === u.id;
        row.style.cssText = `display:flex;align-items:center;justify-content:space-between;padding:7px 9px;border-radius:10px;border:1px solid ${isSel ? '#059669' : '#e2e8f0'};background:${isSel ? '#ecfdf5' : '#ffffff'};cursor:pointer;transition:all 0.12s ease;`;
        const badgeCls = u.status === 'available' ? 'status-available' : 'status-owner';
        const priceHtml = (showUnitPrices && u.status === 'available')
          ? `<div style="font-size:12px;font-weight:900;color:#0f172a;">${formatILS(u.price)}</div>`
          : `<div style="font-size:11px;font-weight:700;color:#64748b;">${u.status === 'owner' ? 'דירת בעלים' : 'לפרטים'}</div>`;

        row.innerHTML = `
          <div style="display:flex;align-items:center;gap:8px;">
            <div style="width:36px;height:34px;border-radius:8px;background:#0f172a;color:#fde047;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:900;font-size:10.5px;line-height:1.05;">
              <span>ק'${u.floorNum}</span>
              <span style="font-size:9.5px;color:#93c5fd;">#${u.aptNum}</span>
            </div>
            <div>
              <div style="display:flex;align-items:center;gap:5px;">
                <span style="font-size:12px;font-weight:800;color:#0f172a;">${u.floorLabel} · ${u.rooms} חד'</span>
                <span class="status-badge ${badgeCls}">${u.status === 'available' ? 'זמין · קולסקי' : 'בעלים'}</span>
              </div>
              <div style="font-size:10px;color:#475569;font-weight:600;">${u.area} מ"ר + ${u.balcony} מ"ר מרפסת · ${u.wing_label}</div>
            </div>
          </div>
          <div style="text-align:left;">
            ${priceHtml}
            <div style="font-size:9px;color:#059669;font-weight:800;">כרטיס + PDF ◂</div>
          </div>
        `;
        row.addEventListener('click', () => selectUnitAndOpenCard(u, true));
        listEl.appendChild(row);
      });
    }

    function syncUnits3DToggleUI() {
      units3DGroup.visible = units3DVisible;
      const topBtn = document.getElementById('btn-top-units-3d');
      const drwBtn = document.getElementById('btn-drawer-units-3d');
      if (topBtn) {
        topBtn.className = units3DVisible ? 'ui-btn active' : 'ui-btn';
        topBtn.style.background = units3DVisible ? '#059669' : '#ecfdf5';
        topBtn.style.color = units3DVisible ? '#ffffff' : '#065f46';
      }
      if (drwBtn) drwBtn.textContent = units3DVisible ? '🏢 סימון דירות 3D: פעיל' : '🏢 הדגש דירות 3D על הבניין';
      if (!units3DVisible) unitBadgeObjs.forEach(b => { b.el.style.display = 'none'; });
    }

    function selectUnitAndOpenCard(u, flyTo = true) {
      selectedUnitObj = u;
      units3DVisible = true;
      syncUnits3DToggleUI();

      unitVolumeMeshes.forEach(m => {
        const isTarget = m.userData.unit.id === u.id;
        m.material.opacity = isTarget ? 0.65 : m.userData.baseOpacity * 0.55;
        m.material.color.setHex(isTarget ? 0xfbbf24 : (m.userData.unit.status === 'available' ? 0x10b981 : 0x64748b));
      });
      renderUnitsCatalogList();

      if (flyTo) {
        if (camState.walkMode) exitWalkthrough();
        selectFloor('all');
        const cx = 0.5 * (u.bbox[0] + u.bbox[2]);
        const cy = 0.5 * (u.bbox[1] + u.bbox[3]);
        camState.target.set(cx, u.bz, cy);
        camState.spherical.radius = 44.0;
        camState.spherical.phi = 1.08;
        camState.spherical.theta = 1.55;
        updateCameraFromOrbit();
      }

      const badgeCls = u.status === 'available' ? 'status-available' : 'status-owner';
      const downPayment20 = Math.round(u.price * 0.20);
      const balance80 = u.price - downPayment20;
      const estMonthlyMortgage = Math.round((u.price * 0.55) * 0.0055);
      const pLevelTxt = u.parking_stall || `חניה #${u.parkingNum}`;

      unitSalesCard.style.display = 'block';
      unitSalesCard.innerHTML = `
        <div class="flex-between" style="border-bottom:1px solid #334155;padding-bottom:8px;margin-bottom:10px;">
          <div>
            <div style="display:flex;align-items:center;gap:6px;">
              <span style="background:#fde047;color:#0f172a;font-weight:900;font-size:12px;padding:2px 7px;border-radius:6px;">${u.name}</span>
              <span class="status-badge ${badgeCls}">${u.statusHe}</span>
            </div>
            <div style="font-size:13.5px;font-weight:900;color:#ffffff;margin-top:4px;">
              ${u.typeHe} · ${u.floorLabel}
            </div>
          </div>
          <button id="btn-close-unit-card" class="ui-btn" style="background:#1e293b;color:#ffffff;border-color:#475569;padding:3px 8px;">✕</button>
        </div>

        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-bottom:10px;text-align:center;">
          <div style="background:#1e293b;border:1px solid #334155;border-radius:8px;padding:6px;">
            <div style="font-size:10px;color:#94a3b8;">שטח דירה (פלדלת)</div>
            <div style="font-size:14px;font-weight:900;color:#38bdf8;">${u.area} מ"ר</div>
          </div>
          <div style="background:#1e293b;border:1px solid #334155;border-radius:8px;padding:6px;">
            <div style="font-size:10px;color:#94a3b8;">מרפסת שמש / גג</div>
            <div style="font-size:14px;font-weight:900;color:#fde047;">+${u.balcony} מ"ר</div>
          </div>
          <div style="background:#1e293b;border:1px solid #334155;border-radius:8px;padding:6px;">
            <div style="font-size:10px;color:#94a3b8;">מפלס קומה</div>
            <div style="font-size:13px;font-weight:900;color:#ffffff;">+${u.z0.toFixed(2)} מ'</div>
          </div>
        </div>

        <div style="background:#1e293b;border:1px solid #334155;border-radius:10px;padding:9px;margin-bottom:10px;font-size:11px;">
          <div class="flex-between" style="margin-bottom:4px;">
            <span style="color:#94a3b8;">כיווני אוויר ושמש:</span>
            <span style="font-weight:800;color:#ffffff;">${u.directions}</span>
          </div>
          <div class="flex-between" style="margin-bottom:4px;">
            <span style="color:#94a3b8;">חניה צמודה בטאבו:</span>
            <span style="font-weight:800;color:#6ee7b7;">${pLevelTxt}</span>
          </div>
          <div class="flex-between" style="border-top:1px solid #334155;padding-top:6px;margin-top:6px;">
            <span style="color:#fde047;font-weight:800;">מחיר מחירון רשמי:</span>
            <span style="font-size:15px;font-weight:900;color:#10b981;">${showUnitPrices && u.status === 'available' ? formatILS(u.price) : 'פנה למשרד המכירות'}</span>
          </div>
          ${showUnitPrices && u.status === 'available' ? `
          <div style="margin-top:6px;padding-top:6px;border-top:1px dashed #334155;color:#cbd5e1;font-size:10px;">
            <div>💳 <b>מסלול 20/80 יזמי:</b> בחתימה ${formatILS(downPayment20)} (20%) · במסירה ${formatILS(balance80)} (80%)</div>
            <div style="margin-top:2px;">🏦 אומדן החזר משכנתא חודשי (55% מימון): ~${formatILS(estMonthlyMortgage)} / חודש</div>
          </div>` : ''}
        </div>

        <div class="grid-2" style="margin-bottom:2px;">
          <button id="btn-card-enter-tour" class="ui-btn" style="background:#b45309;color:#ffffff;border-color:#d97706;font-weight:800;">
            ✨ סיור 3D בדירה
          </button>
          <button id="btn-card-balcony-view" class="ui-btn" style="background:#0284c7;color:#ffffff;border-color:#38bdf8;font-weight:800;">
            🔭 נוף מהמרפסת (ק' ${u.floorNum})
          </button>
          <button id="btn-card-show-parking" class="ui-btn" style="background:#1e293b;color:#6ee7b7;border-color:#059669;font-weight:800;">
            🚗 הצג חניה #${u.parkingNum}
          </button>
          <button id="btn-card-pdf-offer" class="ui-btn" style="background:#059669;color:#ffffff;border-color:#10b981;font-weight:800;">
            📄 הצעת מחיר PDF
          </button>
        </div>
      `;

      document.getElementById('btn-close-unit-card').addEventListener('click', () => { unitSalesCard.style.display = 'none'; });
      document.getElementById('btn-card-enter-tour').addEventListener('click', () => {
        closeAllDrawers();
        setSliceMode('single');
        selectFloor(u.floorId);
        const cx = 0.5 * (u.bbox[0] + u.bbox[2]);
        const cy = 0.5 * (u.bbox[1] + u.bbox[3]);
        startWalkthroughAt(cx, u.z0 + 1.68, cy, Math.PI, `${u.name} · ${u.typeHe}`, u.floorLabel);
      });
      document.getElementById('btn-card-balcony-view').addEventListener('click', () => {
        closeAllDrawers();
        selectFloor('all');
        const [bx, by] = u.balcPt;
        startWalkthroughAt(bx, u.z0 + 1.68, by, Math.PI, `נוף מהמרפסת — ${u.name} (גובה +${u.z0.toFixed(2)} מ')`, u.floorLabel);
      });
      document.getElementById('btn-card-show-parking').addEventListener('click', () => {
        closeAllDrawers();
        if (camState.walkMode) exitWalkthrough();
        setSliceMode('single');
        const targetFlr = u.parkingLevel || 'b1';
        const targetZ = (targetFlr === 'b2') ? -7.05 : -4.05;
        selectFloor(targetFlr);
        if (parkingHighlightMesh) {
          parkingHighlightMesh.visible = true;
          parkingHighlightMesh.position.set(u.parkingX, targetZ, u.parkingY);
        }
        camState.target.set(u.parkingX, targetZ - 0.4, u.parkingY);
        camState.spherical = { radius: 24.0, phi: 0.62, theta: 1.55 };
        updateCameraFromOrbit();
      });
      document.getElementById('btn-card-pdf-offer').addEventListener('click', () => printUnitOfferPDF(u));
    }

    function printUnitOfferPDF(u) {
      renderer.render(scene, activeCam);
      const snapshotDataUrl = canvas.toDataURL('image/jpeg', 0.90);
      const down20 = Math.round(u.price * 0.20);
      const bal80 = u.price - down20;
      const todayStr = new Date().toLocaleDateString('he-IL');

      const win = window.open('', '_blank', 'width=940,height=820');
      if (!win) return;
      win.document.write(`<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <title>הצעת מחיר ומפרט טכני — ${u.name} · פאירברג 3 פתח תקווה</title>
  <style>
    body { font-family: 'Segoe UI', Tahoma, Arial, sans-serif; margin: 0; padding: 28px; color: #0f172a; background: #ffffff; }
    .hdr { display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #1e3a8a; padding-bottom: 14px; margin-bottom: 18px; }
    .brand-box { display: flex; align-items: center; gap: 12px; }
    .logo { width: 58px; height: 52px; border-radius: 12px; background: #0f172a; color: #fde047; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 16px; }
    .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 18px; }
    .kpi { background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; padding: 10px; text-align: center; }
    .kpi-lbl { font-size: 11px; color: #64748b; font-weight: 700; }
    .kpi-val { font-size: 18px; font-weight: 900; color: #0f172a; margin-top: 3px; }
    .two-col { display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 16px; margin-bottom: 18px; }
    .box { border: 1px solid #cbd5e1; border-radius: 12px; padding: 14px; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    td { padding: 7px 4px; border-bottom: 1px solid #e2e8f0; }
    .print-btn { background: #059669; color: #fff; border: none; padding: 10px 20px; border-radius: 8px; font-weight: 800; cursor: pointer; font-size: 14px; }
    @media print { .no-print { display: none; } body { padding: 12px; } }
  </style>
</head>
<body>
  <div class="no-print" style="display:flex;justify-content:flex-end;margin-bottom:12px;">
    <button class="print-btn" onclick="window.print()">🖨️ הדפס / שמור כקובץ PDF</button>
  </div>
  <div class="hdr">
    <div class="brand-box">
      <div class="logo">F3</div>
      <div>
        <div style="font-size:20px;font-weight:900;color:#0f172a;">א. קולסקי חברה לבניה והשקעות בע"מ</div>
        <div style="font-size:13px;color:#475569;font-weight:700;">פרויקט בוטיק פאירברג 3, פתח תקווה · אדריכלות: אלישע רובין אדריכלים</div>
      </div>
    </div>
    <div style="text-align:left;font-size:12px;color:#475569;">
      <div><b>תאריך הפקה:</b> ${todayStr}</div>
      <div><b>גוש 6387 חלקה 193</b> · 18 יח"ד · 19 חניות</div>
    </div>
  </div>
  <div class="grid">
    <div class="kpi"><div class="kpi-lbl">מספר דירה</div><div class="kpi-val">${u.name}</div></div>
    <div class="kpi"><div class="kpi-lbl">קומה ומפלס</div><div class="kpi-val">${u.floorLabel} (+${u.z0.toFixed(2)})</div></div>
    <div class="kpi"><div class="kpi-lbl">שטח דירה + מרפסת</div><div class="kpi-val">${u.area} + ${u.balcony} מ"ר</div></div>
    <div class="kpi" style="background:#ecfdf5;border-color:#6ee7b7;"><div class="kpi-lbl" style="color:#065f46;">מחיר מחירון</div><div class="kpi-val" style="color:#047857;">${u.status === 'available' ? formatILS(u.price) : 'דירת בעלים'}</div></div>
  </div>
  <div class="two-col">
    <div class="box">
      <div style="font-size:14px;font-weight:900;color:#1e3a8a;margin-bottom:8px;">📋 מפרט טכני ותנאי עסקה — ${u.name}</div>
      <table>
        <tr><td><b>מספר חדרים וטיפוס:</b></td><td>${u.rooms} חדרים (${u.typeHe})</td></tr>
        <tr><td><b>כיווני אוויר מלאים:</b></td><td>${u.directions}</td></tr>
        <tr><td><b>חניה צמודה בטאבו:</b></td><td>${u.parking_stall || 'חניה מקורה במרתף החניון'}</td></tr>
        <tr><td><b>מפרט פנים יוקרתי:</b></td><td>ריצוף גרניט פורצלן 100×100/80×80, מטבח יוקרה, תריסי אור חשמליים, מערכת מיזוג VRF</td></tr>
        <tr><td><b>תנאי תשלום יזמיים (20/80):</b></td><td>20% בחתימה (${formatILS(down20)}) · 80% במסירת חזקה (${formatILS(bal80)})</td></tr>
        <tr><td><b>נגישות ומוקדי סביבה:</b></td><td>בצמוד לציר רוטשילד, תחנת מטרו M2 מתוכננת, הקו האדום של הרכבת הקלה ובית חולים השרון</td></tr>
      </table>
    </div>
    <div class="box" style="display:flex;flex-direction:column;justify-content:space-between;">
      <div style="font-size:13px;font-weight:800;color:#0f172a;margin-bottom:6px;">📸 הדמיית המודל התלת-ממדי (1:50 BIM):</div>
      <img src="${snapshotDataUrl}" style="width:100%;height:220px;object-fit:cover;border-radius:8px;border:1px solid #cbd5e1;" />
      <div style="font-size:10px;color:#64748b;margin-top:6px;">* ההדמיה והמחירים להמחשה שיווקית בלבד וכפופים להסכם המכר המלא ולמפרט הטכני החתום.</div>
    </div>
  </div>
</body>
</html>`);
      win.document.close();
    }

    // =========================================================================
    // 8. CAMERA CONTROLLER (ORBIT, FIRST-PERSON WALKTHROUGH & PRESETS)
    // =========================================================================
    const camState = {
      target: new THREE.Vector3(0.0, 16.0, 0.5),
      spherical: { radius: 52.0, phi: 1.08, theta: 1.48 },
      isDragging: false,
      isPanning: false,
      downX: 0, downY: 0, prevX: 0, prevY: 0,
      walkMode: false, yaw: 0, pitch: 0, keys: {}
    };

    const VIEW_PRESETS = {
      iso_south:      { theta: 1.48,  phi: 1.08, radius: 52.0,   target: [0.0, 16.0, 0.5], ortho: false, clip: 38.0 },
      iso_north:      { theta: -1.48, phi: 1.08, radius: 52.0,   target: [0.0, 16.0, 0.5], ortho: false, clip: 38.0 },
      gmaps_regional: { theta: 1.48,  phi: 0.56, radius: 1320.0, target: [0.0, 8.0, 0.5],  ortho: false, clip: 38.0 },
      gmaps_aerial:   { theta: 1.48,  phi: 0.60, radius: 460.0,  target: [0.0, 8.0, 0.5],  ortho: false, clip: 38.0 },
      gmaps_close:    { theta: 1.48,  phi: 0.66, radius: 135.0,  target: [0.0, 10.0, 0.5], ortho: false, clip: 38.0 },
      top_plan:       { theta: Math.PI/2, phi: 0.04, radius: 42.0, target: [0.0, 16.1, 0.5], ortho: true, clip: 18.8 }
    };

    function updateCameraFromOrbit() {
      if (camState.walkMode) return;
      const { radius, phi, theta } = camState.spherical;
      const x = camState.target.x + radius * Math.sin(phi) * Math.cos(theta);
      const y = camState.target.y + radius * Math.cos(phi);
      const z = camState.target.z + radius * Math.sin(phi) * Math.sin(theta);
      perspCam.position.set(x, y, z);
      perspCam.lookAt(camState.target);

      orthoCam.position.set(x, y, z);
      orthoCam.lookAt(camState.target);
      orthoCam.zoom = 42.0 / radius;
      orthoCam.updateProjectionMatrix();
    }

    function setOrthoMode(useOrtho) {
      isOrtho = useOrtho;
      activeCam = isOrtho ? orthoCam : perspCam;
      document.getElementById('proj-badge').textContent = isOrtho ? 'אורתוגרפי 1:50' : 'פרספקטיבה';
      document.getElementById('btn-ortho').className = isOrtho ? 'ui-btn active' : 'ui-btn';
      updateCameraFromOrbit();
    }

    function activatePreset(viewKey) {
      const p = VIEW_PRESETS[viewKey];
      if (!p) return;
      if (camState.walkMode) exitWalkthrough();
      if (viewKey !== 'top_plan') selectFloor('all');
      camState.spherical.theta = p.theta;
      camState.spherical.phi = p.phi;
      camState.spherical.radius = p.radius;
      camState.target.set(p.target[0], p.target[1], p.target[2]);
      if (typeof p.clip === 'number') setClipHeight(p.clip);
      setOrthoMode(p.ortho);
      closeAllDrawers();
    }

    function openFurnishedDollhouse(floorId) {
      closeAllDrawers();
      if (camState.walkMode) exitWalkthrough();
      const fObj = FLOORS.find(f => f.id === floorId) || FLOORS[7];
      setSliceMode('single');
      selectFloor(fObj.id);
      setClipHeight(38.0);
      setOrthoMode(false);
      camState.target.set(0.0, fObj.zFloor + 1.0, 0.5);
      camState.spherical.radius = 34.0;
      camState.spherical.phi = 0.56;
      camState.spherical.theta = 1.48;
      updateCameraFromOrbit();
      const badgeEl = document.getElementById('apt-active-badge');
      if (badgeEl) badgeEl.textContent = `${fObj.label} (Dollhouse 3D)`;
    }

    function startWalkthroughAt(x, yEye, z, yawRad, titleText, badgeText) {
      camState.walkMode = true;
      setOrthoMode(false);
      perspCam.fov = 58;
      perspCam.updateProjectionMatrix();
      perspCam.position.set(x, yEye, z);
      camState.yaw = yawRad;
      camState.pitch = -0.04;
      document.getElementById('aptc-tour-hud').style.display = 'flex';
      document.getElementById('aptc-active-room-title').textContent = titleText || 'סיור פנים אדריכלי 1:50';
      if (badgeText) document.getElementById('apt-active-badge').textContent = badgeText;
    }

    function exitWalkthrough() {
      camState.walkMode = false;
      perspCam.fov = 42;
      perspCam.updateProjectionMatrix();
      document.getElementById('aptc-tour-hud').style.display = 'none';
      updateCameraFromOrbit();
    }

    function startPresetInteriorTour(floorNum, wing) {
      closeAllDrawers();
      const u = YATKOVSKI_UNITS.find(x => x.floorNum === floorNum && x.wing === wing) || YATKOVSKI_UNITS[0];
      selectedUnitObj = u;
      setSliceMode('single');
      selectFloor(u.floorId);
      const cx = (wing === 'W' || wing === 'PH_W') ? -3.5 : 4.8;
      const cy = (floorNum === 9) ? 0.8 : 1.8;
      startWalkthroughAt(cx, u.z0 + 1.68, cy, Math.PI, `${u.name} · ${u.typeHe} (${u.area}+${u.balcony} מ"ר)`, u.floorLabel);
    }

    function teleportInTour(x, z, yawRad, labelTxt, forceFloorId = null) {
      const activeF = forceFloorId
        ? (FLOORS.find(f => f.id === forceFloorId) || FLOORS[7])
        : (FLOORS.find(f => f.id === currentFloorId && f.zFloor >= 0) || FLOORS[7]);
      if (!camState.walkMode || forceFloorId) {
        setSliceMode('single');
        selectFloor(activeF.id);
      }
      startWalkthroughAt(x, activeF.zFloor + 1.68, z, yawRad, labelTxt, activeF.label);
    }

    function flyToBalconyFloorView(flrNum) {
      closeAllDrawers();
      selectFloor('all');
      const fObj = FLOORS.find(f => f.id === 'f' + flrNum) || FLOORS[10];
      document.querySelectorAll('#balcony-floor-selector [data-bflr]').forEach(b => {
        b.className = (parseInt(b.dataset.bflr, 10) === flrNum) ? 'ui-btn active' : 'ui-btn';
      });
      const tourSel = document.getElementById('tour-floor-select');
      if (tourSel) tourSel.value = String(flrNum);
      const bx = (flrNum >= 9) ? -5.5 : -2.2;
      const by = (flrNum === 10) ? 1.5 : ((flrNum === 9) ? 3.8 : 5.0);
      startWalkthroughAt(bx, fObj.zFloor + 1.68, by, Math.PI, `🔭 נוף פנורמי מהמרפסת לרחוב פאירברג — קומה ${flrNum} (+${fObj.zFloor.toFixed(2)} מ')`, fObj.label);
    }

    // =========================================================================
    // 9. UI WIRING: DRAWERS, FLOOR SLICER, FINISH PACKAGES, NIGHT MODE, MEASURE
    // =========================================================================
    let sliceMode = 'single';
    let currentFloorId = 'all';

    function closeAllDrawers() {
      document.querySelectorAll('.dropdown-drawer.open').forEach(d => d.classList.remove('open'));
      document.querySelectorAll('[data-drawer].open').forEach(b => b.classList.remove('open'));
    }

    document.querySelectorAll('[data-drawer]').forEach(btn => {
      btn.addEventListener('click', e => {
        e.stopPropagation();
        const drawerId = btn.dataset.drawer;
        const drawer = document.getElementById(drawerId);
        if (!drawer) return;
        const wasOpen = drawer.classList.contains('open');
        closeAllDrawers();
        if (!wasOpen) { drawer.classList.add('open'); btn.classList.add('open'); }
      });
    });

    document.querySelectorAll('[data-close-drawer]').forEach(btn => {
      btn.addEventListener('click', e => { e.preventDefault(); e.stopPropagation(); closeAllDrawers(); });
    });

    const sectionsPanel = document.getElementById('sections-panel');
    const btnToggleSections = document.getElementById('btn-toggle-sections-body');
    if (btnToggleSections && sectionsPanel) {
      btnToggleSections.addEventListener('click', () => {
        const isCollapsed = sectionsPanel.classList.toggle('collapsed');
        btnToggleSections.textContent = isCollapsed ? '+ פתח חתכים' : '▾';
      });
    }

    document.getElementById('btn-close-tour-hud').addEventListener('click', exitWalkthrough);

    let activeDpadInterval = null;
    function stepWalkMovement(m, dt = 0.05) {
      if (!camState.walkMode) return;
      const speed = 3.6 * dt;
      const forward = new THREE.Vector3(Math.sin(camState.yaw), 0, -Math.cos(camState.yaw));
      const right = new THREE.Vector3(Math.cos(camState.yaw), 0, Math.sin(camState.yaw));
      if (m === 'fwd')   perspCam.position.addScaledVector(forward, speed);
      if (m === 'back')  perspCam.position.addScaledVector(forward, -speed);
      if (m === 'left')  perspCam.position.addScaledVector(right, -speed);
      if (m === 'right') perspCam.position.addScaledVector(right, speed);
      if (m === 'up')    perspCam.position.y += speed * 0.75;
      if (m === 'down')  perspCam.position.y -= speed * 0.75;
      if (m === 'turnL') camState.yaw -= 1.5 * dt;
      if (m === 'turnR') camState.yaw += 1.5 * dt;
    }
    document.querySelectorAll('.walk-dpad-btn[data-move]').forEach(btn => {
      const m = btn.dataset.move;
      const startMove = () => {
        stepWalkMovement(m, 0.08);
        clearInterval(activeDpadInterval);
        activeDpadInterval = setInterval(() => stepWalkMovement(m, 0.04), 30);
      };
      const stopMove = () => clearInterval(activeDpadInterval);
      btn.addEventListener('pointerdown', startMove);
      btn.addEventListener('pointerup', stopMove);
      btn.addEventListener('pointerleave', stopMove);
    });

    const btnTogglePanMode = document.getElementById('btn-toggle-pan-mode');
    if (btnTogglePanMode) {
      btnTogglePanMode.addEventListener('click', () => {
        camState.panModeActive = !camState.panModeActive;
        if (camState.panModeActive) {
          btnTogglePanMode.textContent = '✋ עכבר: הזזה';
          btnTogglePanMode.style.background = '#2563eb';
          btnTogglePanMode.style.color = '#ffffff';
          btnTogglePanMode.style.borderColor = '#1d4ed8';
          canvas.style.cursor = 'move';
        } else {
          btnTogglePanMode.textContent = '🔄 עכבר: סיבוב';
          btnTogglePanMode.style.background = '#eff6ff';
          btnTogglePanMode.style.color = '#1d4ed8';
          btnTogglePanMode.style.borderColor = '#93c5fd';
          canvas.style.cursor = 'grab';
        }
      });
    }

    function getCameraScreenAxes() {
      activeCam.updateMatrixWorld();
      const e = activeCam.matrixWorld.elements;
      const camRight = new THREE.Vector3(e[0], e[1], e[2]).normalize();
      const camUp    = new THREE.Vector3(e[4], e[5], e[6]).normalize();
      return { camRight, camUp };
    }

    function stepOrbitPan(action, dt = 0.05) {
      if (camState.walkMode) {
        if (action === 'right') stepWalkMovement('right', dt);
        else if (action === 'left') stepWalkMovement('left', dt);
        else if (action === 'up') stepWalkMovement('fwd', dt);
        else if (action === 'down') stepWalkMovement('back', dt);
        else if (action === 'elevUp') stepWalkMovement('up', dt);
        else if (action === 'elevDown') stepWalkMovement('down', dt);
        return;
      }
      const stepDist = Math.max(0.6, camState.spherical.radius * 0.32) * dt;
      const { camRight, camUp } = getCameraScreenAxes();
      if (action === 'right')    camState.target.addScaledVector(camRight, stepDist);
      if (action === 'left')     camState.target.addScaledVector(camRight, -stepDist);
      if (action === 'up')       camState.target.addScaledVector(camUp, stepDist);
      if (action === 'down')     camState.target.addScaledVector(camUp, -stepDist);
      if (action === 'elevUp')   camState.target.y += stepDist * 0.85;
      if (action === 'elevDown') camState.target.y -= stepDist * 0.85;
      if (action === 'zoomIn')   camState.spherical.radius = Math.max(4.0, camState.spherical.radius * (1 - 0.85 * dt));
      if (action === 'zoomOut')  camState.spherical.radius = Math.min(3200.0, camState.spherical.radius * (1 + 0.85 * dt));
      if (action === 'reset') {
        const activeF = FLOORS.find(f => f.id === currentFloorId);
        camState.target.set(0.0, activeF ? activeF.zFloor + 1.2 : 16.0, 0.5);
      }
      camState.target.y = Math.max(-10.0, Math.min(95.0, camState.target.y));
      updateCameraFromOrbit();
    }

    let activeOrbitPadInterval = null;
    document.querySelectorAll('#orbit-nav-pad [data-opan]').forEach(btn => {
      const act = btn.dataset.opan;
      if (act === 'reset') {
        btn.addEventListener('click', () => stepOrbitPan('reset', 0.1));
        return;
      }
      const startPan = (e) => {
        e.preventDefault();
        stepOrbitPan(act, 0.09);
        clearInterval(activeOrbitPadInterval);
        activeOrbitPadInterval = setInterval(() => stepOrbitPan(act, 0.045), 30);
      };
      const stopPan = () => clearInterval(activeOrbitPadInterval);
      btn.addEventListener('pointerdown', startPan);
      btn.addEventListener('pointerup', stopPan);
      btn.addEventListener('pointerleave', stopPan);
    });

    document.querySelectorAll('#balcony-floor-selector [data-bflr]').forEach(btn => {
      btn.addEventListener('click', () => flyToBalconyFloorView(parseInt(btn.dataset.bflr, 10)));
    });
    document.getElementById('tour-floor-select').addEventListener('change', function() {
      flyToBalconyFloorView(parseInt(this.value, 10));
    });

    document.querySelectorAll('.view-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activatePreset(btn.dataset.view);
      });
    });

    function syncGisRadiiState() {
      gisRingsGroup.visible = gisRadiiVisible;
      const topBtn = document.getElementById('btn-top-radii');
      const sideBtn = document.getElementById('btn-side-radii');
      if (topBtn) {
        topBtn.textContent = gisRadiiVisible ? '⭕ רדיוסים: פעיל' : '⭕ רדיוסים: כבוי';
        topBtn.className = gisRadiiVisible ? 'ui-btn active' : 'ui-btn';
      }
      if (sideBtn) {
        sideBtn.textContent = gisRadiiVisible ? '⭕ רדיוסים (8): פעיל' : '⭕ רדיוסים (8): כבוי';
        sideBtn.className = gisRadiiVisible ? 'ui-btn active' : 'ui-btn';
      }
    }

    function syncGisPoisState() {
      gisPoisGroup.visible = gisPoisVisible;
      gisPoiLabelObjs.forEach(item => {
        const catMatch = (activeGisCategory === 'all' || item.poi.cat === activeGisCategory);
        item.subGrp.visible = gisPoisVisible && catMatch;
        if (item.sidebarRow) item.sidebarRow.style.display = catMatch ? 'flex' : 'none';
      });
      if (!gisPoisVisible) gisActiveCard.style.display = 'none';
      const topBtn = document.getElementById('btn-top-pois');
      const sideBtn = document.getElementById('btn-side-pois');
      if (topBtn) {
        topBtn.textContent = gisPoisVisible ? '📍 מיקומים: פעיל' : '📍 מיקומים: כבוי';
        topBtn.className = gisPoisVisible ? 'ui-btn active' : 'ui-btn';
      }
      if (sideBtn) {
        sideBtn.textContent = gisPoisVisible ? '📍 מיקומים (28): פעיל' : '📍 מיקומים (28): כבוי';
        sideBtn.className = gisPoisVisible ? 'ui-btn active' : 'ui-btn';
      }
    }

    document.getElementById('btn-top-radii').addEventListener('click', () => { gisRadiiVisible = !gisRadiiVisible; syncGisRadiiState(); });
    document.getElementById('btn-side-radii').addEventListener('click', () => { gisRadiiVisible = !gisRadiiVisible; syncGisRadiiState(); });
    document.getElementById('btn-top-pois').addEventListener('click', () => { gisPoisVisible = !gisPoisVisible; syncGisPoisState(); });
    document.getElementById('btn-side-pois').addEventListener('click', () => { gisPoisVisible = !gisPoisVisible; syncGisPoisState(); });

    document.getElementById('btn-side-gis-regional').addEventListener('click', () => activatePreset('gmaps_regional'));
    document.getElementById('btn-side-gis-overview').addEventListener('click', () => activatePreset('gmaps_aerial'));
    document.getElementById('btn-side-gis-close').addEventListener('click', () => activatePreset('gmaps_close'));

    document.querySelectorAll('#gis-cat-buttons .gis-cat-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        activeGisCategory = chip.dataset.gcat;
        document.querySelectorAll('#gis-cat-buttons .gis-cat-chip').forEach(c => {
          c.className = (c === chip) ? 'gis-cat-chip ui-btn active' : 'gis-cat-chip ui-btn';
        });
        if (!gisPoisVisible) gisPoisVisible = true;
        syncGisPoisState();
      });
    });

    document.getElementById('btn-top-units-3d').addEventListener('click', () => {
      units3DVisible = !units3DVisible;
      if (units3DVisible && camState.spherical.radius > 160) activatePreset('iso_south');
      syncUnits3DToggleUI();
    });
    document.getElementById('btn-drawer-units-3d').addEventListener('click', () => {
      units3DVisible = !units3DVisible;
      if (units3DVisible && camState.spherical.radius > 160) activatePreset('iso_south');
      syncUnits3DToggleUI();
    });
    document.getElementById('btn-toggle-prices').addEventListener('click', function() {
      showUnitPrices = !showUnitPrices;
      this.textContent = showUnitPrices ? '👁️ מחירים: מוצג' : '👁️ מחירים: מוסתר';
      this.className = showUnitPrices ? 'ui-btn active' : 'ui-btn';
      renderUnitsCatalogList();
      if (selectedUnitObj && unitSalesCard.style.display === 'block') selectUnitAndOpenCard(selectedUnitObj, false);
    });
    document.querySelectorAll('#unit-bldg-filters .unit-bldg-chip').forEach(btn => {
      btn.addEventListener('click', () => {
        activeUnitBldgFilter = btn.dataset.ubldg;
        document.querySelectorAll('#unit-bldg-filters .unit-bldg-chip').forEach(b => {
          b.className = (b === btn) ? 'unit-bldg-chip ui-btn active' : 'unit-bldg-chip ui-btn';
        });
        renderUnitsCatalogList();
      });
    });
    document.querySelectorAll('#unit-status-filters .unit-status-chip').forEach(btn => {
      btn.addEventListener('click', () => {
        activeUnitStatusFilter = btn.dataset.ustatus;
        document.querySelectorAll('#unit-status-filters .unit-status-chip').forEach(b => {
          b.className = (b === btn) ? 'unit-status-chip ui-btn active' : 'unit-status-chip ui-btn';
        });
        renderUnitsCatalogList();
      });
    });
    document.querySelectorAll('#unit-room-filters .unit-room-chip').forEach(btn => {
      btn.addEventListener('click', () => {
        activeUnitRoomFilter = btn.dataset.urooms;
        document.querySelectorAll('#unit-room-filters .unit-room-chip').forEach(b => {
          b.className = (b === btn) ? 'unit-room-chip ui-btn active' : 'unit-room-chip ui-btn';
        });
        renderUnitsCatalogList();
      });
    });

    document.querySelectorAll('#interior-pkg-buttons [data-pkg]').forEach(btn => {
      btn.addEventListener('click', () => {
        const pkg = FINISH_TEXTURES[btn.dataset.pkg];
        if (!pkg) return;
        document.querySelectorAll('#interior-pkg-buttons [data-pkg]').forEach(b => {
          b.className = (b === btn) ? 'pkg-card-btn active' : 'pkg-card-btn';
        });
        document.getElementById('active-pkg-badge').textContent = pkg.label;
        MATS.slabFloor.map = pkg.map;
        MATS.slabFloor.color.setHex(pkg.color);
        MATS.slabFloor.needsUpdate = true;
        MATS.lightWood.color.setHex(pkg.door);
        MATS.lightWood.needsUpdate = true;
      });
    });

    let isWoodBalcDeck = true;
    document.getElementById('btn-balcony-deck').addEventListener('click', function() {
      isWoodBalcDeck = !isWoodBalcDeck;
      MATS.woodDeck.map = isWoodBalcDeck ? DECK_TEXTURES.wood : DECK_TEXTURES.grey;
      MATS.woodDeck.needsUpdate = true;
      this.textContent = isWoodBalcDeck
        ? '🪵 מרפסות: דמוי דק עץ (לחץ להחלפה לפורצלן אפור)'
        : '🧱 מרפסות: פורצלן אפור (לחץ להחלפה לדק עץ)';
      this.className = isWoodBalcDeck ? 'ui-btn active' : 'ui-btn';
    });

    document.getElementById('btn-gmaps').addEventListener('click', function() {
      gmapsVisible = !gmapsVisible;
      const isBase = (currentFloorId === 'b1' || currentFloorId === 'b2');
      gisMapPlanesGroup.visible = gmapsVisible && !isBase;
      this.textContent = gmapsVisible
        ? '🗺️ מפת לוויין Google Maps (פאירברג 3): פעיל'
        : '🗺️ מפת לוויין Google Maps (פאירברג 3): כבוי';
      this.className = gmapsVisible ? 'ui-btn active' : 'ui-btn';
    });

    document.getElementById('btn-ortho').addEventListener('click', () => setOrthoMode(!isOrtho));

    let cadPlanVisible = true;
    document.getElementById('btn-cad-plan').addEventListener('click', function() {
      cadPlanVisible = !cadPlanVisible;
      toggleLayer('cad2d', cadPlanVisible);
      this.textContent = cadPlanVisible ? '✏️ שרטוט פנים CAD: פעיל' : '✏️ שרטוט פנים CAD: כבוי';
      this.className = cadPlanVisible ? 'ui-btn active' : 'ui-btn';
    });

    const sunSlider = document.getElementById('sun-slider');
    const sunVal = document.getElementById('sun-val');
    sunSlider.addEventListener('input', () => {
      const deg = parseFloat(sunSlider.value);
      const rad = deg * Math.PI / 180;
      dirLight.position.set(55 * Math.cos(rad), 75 * Math.sin(rad) + 15, 48 * Math.sin(rad * 1.2));
      const hour = Math.round(7 + (deg / 180) * 11);
      sunVal.textContent = `~${hour}:00`;
    });

    let isNightMode = false;
    document.getElementById('btn-top-night').addEventListener('click', function() {
      isNightMode = !isNightMode;
      this.className = isNightMode ? 'ui-btn active' : 'ui-btn';
      this.textContent = isNightMode ? '☀️ מצב יום' : '🌙 מצב לילה';
      nightLightsGroup.visible = isNightMode;
      if (isNightMode) {
        scene.background.setHex(0x0b1329);
        hemiLight.intensity = 0.32;
        dirLight.intensity = 0.26;
        dirLight.color.setHex(0xf59e0b);
        MATS.winGlass.emissive.setHex(0xfde68a);
        MATS.winGlass.emissiveIntensity = 0.55;
        MATS.winGlass.opacity = 0.72;
      } else {
        scene.background.setHex(0xf4f1ea);
        hemiLight.intensity = 0.66;
        dirLight.intensity = 0.72;
        dirLight.color.setHex(0xfffaf0);
        MATS.winGlass.emissive.setHex(0x0284c7);
        MATS.winGlass.emissiveIntensity = 0.14;
        MATS.winGlass.opacity = 0.66;
      }
    });

    let isMeasureMode = false;
    let measurePtA = null;
    const measureGroup = new THREE.Group();
    scene.add(measureGroup);
    const measureLabelsContainer = document.getElementById('measure-labels-container');
    const measureHud = document.getElementById('measure-hud');
    const measureLastVal = document.getElementById('measure-last-val');
    const measureBadges = [];

    function clearAllMeasurements() {
      measurePtA = null;
      while (measureGroup.children.length > 0) measureGroup.remove(measureGroup.children[0]);
      measureBadges.forEach(b => b.el.remove());
      measureBadges.length = 0;
      if (measureLastVal) measureLastVal.textContent = 'מוכן למדידה';
    }

    document.getElementById('btn-top-measure').addEventListener('click', function() {
      isMeasureMode = !isMeasureMode;
      this.className = isMeasureMode ? 'ui-btn active' : 'ui-btn';
      measureHud.style.display = isMeasureMode ? 'flex' : 'none';
      measurePtA = null;
    });
    document.getElementById('btn-clear-measures').addEventListener('click', clearAllMeasurements);
    document.getElementById('btn-close-measure').addEventListener('click', () => {
      isMeasureMode = false;
      document.getElementById('btn-top-measure').className = 'ui-btn';
      measureHud.style.display = 'none';
    });

    const clipSlider = document.getElementById('clip-slider');
    const clipVal = document.getElementById('clip-val');

    function setClipHeight(v) {
      clipSlider.value = v;
      clipPlane.constant = v;
      clipVal.textContent = v >= 37.5 ? "+38.00 מ' (מלא)" : `${v >= 0 ? '+' : ''}${v.toFixed(2)} מ' (חתך)`;
      const isBase = (currentFloorId === 'b1' || currentFloorId === 'b2');
      gisMapPlanesGroup.visible = gmapsVisible && (v > 0.0) && !isBase;
    }
    clipSlider.addEventListener('input', () => setClipHeight(parseFloat(clipSlider.value)));

    function setSliceMode(mode) {
      sliceMode = mode;
      document.getElementById('mode-single').classList.toggle('active', mode === 'single');
      document.getElementById('mode-cum').classList.toggle('active', mode === 'cumulative');
      selectFloor(currentFloorId);
    }

    function selectFloor(floorId) {
      if (floorId === 'f0') floorId = 'kar';
      currentFloorId = floorId;
      document.querySelectorAll('#floor-buttons .ui-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('fbtn-' + floorId);
      if (activeBtn) activeBtn.classList.add('active');

      const isBase = (floorId === 'b1' || floorId === 'b2');
      if (parkingHighlightMesh && !isBase) parkingHighlightMesh.visible = false;
      gisMapPlanesGroup.visible = gmapsVisible && !isBase;

      if (floorId === 'all') {
        document.getElementById('active-floor-label').textContent = 'מבנה שלם (כל 14 הקומות)';
        FLOORS.forEach(f => { floorGroups[f.id].visible = true; });
        setClipHeight(38.0);
        return;
      }

      const idx = FLOORS.findIndex(f => f.id === floorId);
      const fObj = FLOORS[idx];
      if (!fObj) return;
      document.getElementById('active-floor-label').textContent = `${fObj.label} (${fObj.elevText} מ')`;
      FLOORS.forEach((f, i) => {
        floorGroups[f.id].visible = (sliceMode === 'single') ? (i === idx) : (i <= idx);
      });
    }

    function toggleLayer(layerId, isVis) {
      (layerObjects[layerId] || []).forEach(obj => { obj.visible = isVis; });
    }

    function initPanels() {
      const fContainer = document.getElementById('floor-buttons');
      const allBtn = document.createElement('button');
      allBtn.className = 'ui-btn active';
      allBtn.style.gridColumn = 'span 2';
      allBtn.id = 'fbtn-all';
      allBtn.innerHTML = '🏢 מבנה שלם (כל 14 הקומות)';
      allBtn.onclick = () => selectFloor('all');
      fContainer.appendChild(allBtn);

      FLOORS.slice().reverse().forEach(f => {
        const b = document.createElement('button');
        b.className = 'ui-btn';
        b.style.justifyContent = 'space-between';
        b.style.fontSize = '10.5px';
        b.id = 'fbtn-' + f.id;
        b.innerHTML = `<span>${f.label}</span><span style="font-size:9px;opacity:0.75;font-family:monospace">${f.elevText}</span>`;
        b.onclick = () => {
          selectFloor(f.id);
          if (camState.spherical.radius > 120) {
            camState.target.set(0.0, Math.max(-6, f.zFloor), 0.5);
            camState.spherical.radius = 44.0;
            camState.spherical.phi = 0.68;
            updateCameraFromOrbit();
          }
        };
        fContainer.appendChild(b);
      });

      const topPlanBtn = document.createElement('button');
      topPlanBtn.className = 'ui-btn';
      topPlanBtn.style.gridColumn = 'span 2';
      topPlanBtn.innerHTML = '📏 תוכנית אדריכלית 1:50 מלמעלה';
      topPlanBtn.onclick = () => {
        if (currentFloorId === 'all') { setSliceMode('single'); selectFloor('f5'); }
        activatePreset('top_plan');
      };
      fContainer.appendChild(topPlanBtn);

      const lContainer = document.getElementById('layer-toggles');
      LAYERS_DEF.forEach(l => {
        const row = document.createElement('label');
        row.className = 'layer-row';
        row.innerHTML = `
          <span style="display:flex;align-items:center;gap:6px;font-weight:600;">
            <input type="checkbox" ${l.visible ? 'checked' : ''} onchange="toggleLayer('${l.id}', this.checked)" />
            <span>${l.name}</span>
          </span>
          <span style="width:12px;height:12px;border-radius:3px;background:${l.color};border:1px solid #94a3b8;"></span>
        `;
        lContainer.appendChild(row);
      });

      renderUnitsCatalogList();
    }
    initPanels();

    document.getElementById('btn-export-obj').addEventListener('click', () => {
      let objLines = ['# Feierberg 3 Petah Tikva - 1:1 Metric Architectural BIM Model (Meters)'];
      let vOffset = 1;
      FLOORS.forEach(f => {
        const fg = floorGroups[f.id];
        if (!fg || !fg.visible) return;
        fg.traverse(node => {
          if (!node.isMesh || !node.visible) return;
          const geo = node.geometry;
          if (!geo || !geo.attributes.position) return;
          const pos = geo.attributes.position;
          const matWorld = node.matrixWorld;
          const v = new THREE.Vector3();
          for (let i = 0; i < pos.count; i++) {
            v.fromBufferAttribute(pos, i).applyMatrix4(matWorld);
            objLines.push(`v ${v.x.toFixed(4)} ${v.y.toFixed(4)} ${v.z.toFixed(4)}`);
          }
          if (geo.index) {
            const idx = geo.index;
            for (let i = 0; i < idx.count; i += 3) {
              objLines.push(`f ${idx.getX(i)+vOffset} ${idx.getX(i+1)+vOffset} ${idx.getX(i+2)+vOffset}`);
            }
          } else {
            for (let i = 0; i < pos.count; i += 3) {
              objLines.push(`f ${i+vOffset} ${i+1+vOffset} ${i+2+vOffset}`);
            }
          }
          vOffset += pos.count;
        });
      });
      const blob = new Blob([objLines.join('\n')], { type: 'text/plain;charset=utf-8' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'feierberg3_model.obj';
      a.click();
    });

    // =========================================================================
    // 10. POINTER, WHEEL, KEYBOARD & ANIMATION LOOP
    // =========================================================================
    const raycaster = new THREE.Raycaster();
    const mouseNDC = new THREE.Vector2();

    canvas.addEventListener('pointerdown', e => {
      closeAllDrawers();
      if (!camState.walkMode && (e.button === 2 || e.button === 1 || (e.button === 0 && (e.shiftKey || camState.panModeActive)))) {
        camState.isPanning = true;
        camState.isDragging = false;
      } else if (e.button === 0) {
        camState.isDragging = true;
        camState.isPanning = false;
      }
      camState.downX = e.clientX;
      camState.downY = e.clientY;
      camState.prevX = e.clientX;
      camState.prevY = e.clientY;
    });

    window.addEventListener('pointerup', e => {
      const moved = Math.hypot(e.clientX - camState.downX, e.clientY - camState.downY);
      if (e.button === 0 && moved < 5) {
        const rect = canvas.getBoundingClientRect();
        mouseNDC.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
        mouseNDC.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
        raycaster.setFromCamera(mouseNDC, activeCam);

        if (isMeasureMode) {
          const visTargets = allBuildingMeshes.filter(m => m.visible && m.parent && m.parent.visible);
          const hits = raycaster.intersectObjects(visTargets, false);
          if (hits.length > 0) {
            const pt = hits[0].point.clone();
            const dot = new THREE.Mesh(new THREE.SphereGeometry(0.14, 16, 16), new THREE.MeshBasicMaterial({ color: 0x38bdf8 }));
            dot.position.copy(pt);
            measureGroup.add(dot);
            if (!measurePtA) {
              measurePtA = pt;
              measureLastVal.textContent = 'בחר נקודה שנייה...';
            } else {
              const distM = measurePtA.distanceTo(pt);
              const lineGeom = new THREE.BufferGeometry().setFromPoints([measurePtA, pt]);
              measureGroup.add(new THREE.Line(lineGeom, new THREE.LineBasicMaterial({ color: 0x38bdf8, linewidth: 3 })));
              const mid = new THREE.Vector3().addVectors(measurePtA, pt).multiplyScalar(0.5);
              const badge = document.createElement('div');
              badge.style.cssText = 'position:absolute;transform:translate(-50%,-50%);background:#0284c7;color:#ffffff;font-weight:900;font-size:11px;padding:3px 8px;border-radius:999px;border:1.5px solid #ffffff;box-shadow:0 4px 10px rgba(0,0,0,0.35);white-space:nowrap;';
              badge.textContent = `📏 ${distM.toFixed(2)} מ' (${Math.round(distM * 100)} ס"מ)`;
              measureLabelsContainer.appendChild(badge);
              measureBadges.push({ pos: mid, el: badge });
              measureLastVal.textContent = `מרחק: ${distM.toFixed(2)} מ'`;
              measurePtA = null;
            }
          }
        } else if (units3DVisible && !camState.walkMode) {
          const visMeshes = unitVolumeMeshes.filter(m => m.visible);
          const uHits = raycaster.intersectObjects(visMeshes, false);
          if (uHits.length > 0 && uHits[0].object.userData.unit) {
            selectUnitAndOpenCard(uHits[0].object.userData.unit, true);
          }
        }
      }
      camState.isDragging = false;
      camState.isPanning = false;
    });

    canvas.addEventListener('dblclick', e => {
      const rect = canvas.getBoundingClientRect();
      mouseNDC.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouseNDC.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
      raycaster.setFromCamera(mouseNDC, activeCam);
      const targets = [];
      FLOORS.forEach(f => { if (floorGroups[f.id].visible) targets.push(floorGroups[f.id]); });
      const hits = raycaster.intersectObjects(targets, true);
      if (hits.length > 0) {
        const pt = hits[0].point;
        if (camState.walkMode) {
          perspCam.position.set(pt.x, pt.y + 1.68, pt.z);
        } else {
          camState.target.copy(pt);
          camState.spherical.radius = Math.max(14.0, camState.spherical.radius * 0.65);
          updateCameraFromOrbit();
        }
      }
    });

    window.addEventListener('contextmenu', e => e.preventDefault());

    canvas.addEventListener('pointermove', e => {
      const dx = e.clientX - camState.prevX;
      const dy = e.clientY - camState.prevY;
      camState.prevX = e.clientX;
      camState.prevY = e.clientY;

      if (camState.walkMode) {
        if (camState.isDragging) {
          camState.yaw -= dx * 0.004;
          camState.pitch = Math.max(-1.25, Math.min(1.25, camState.pitch - dy * 0.004));
        }
        return;
      }

      if (camState.isDragging) {
        camState.spherical.theta += dx * 0.0065;
        camState.spherical.phi = Math.max(0.05, Math.min(Math.PI * 0.49, camState.spherical.phi - dy * 0.0065));
        updateCameraFromOrbit();
      } else if (camState.isPanning) {
        const panScale = Math.max(0.015, camState.spherical.radius * 0.0014);
        const { camRight, camUp } = getCameraScreenAxes();
        camState.target.addScaledVector(camRight, -dx * panScale);
        camState.target.addScaledVector(camUp, dy * panScale);
        camState.target.y = Math.max(-10.0, Math.min(95.0, camState.target.y));
        updateCameraFromOrbit();
      }
    });

    canvas.addEventListener('wheel', e => {
      e.preventDefault();
      if (camState.walkMode) {
        const forward = new THREE.Vector3(Math.sin(camState.yaw), 0, -Math.cos(camState.yaw));
        perspCam.position.addScaledVector(forward, -e.deltaY * 0.004);
        return;
      }
      camState.spherical.radius = Math.max(4.0, Math.min(3200.0, camState.spherical.radius * (1 + e.deltaY * 0.001)));
      updateCameraFromOrbit();
    }, { passive: false });

    window.addEventListener('keydown', e => {
      if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA')) return;
      camState.keys[e.code] = true;
      if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'PageUp', 'PageDown'].includes(e.code)) e.preventDefault();
      if (e.key === 'Escape') {
        closeAllDrawers();
        if (camState.walkMode) exitWalkthrough();
      }
    });
    window.addEventListener('keyup', e => { camState.keys[e.code] = false; });

    window.addEventListener('resize', () => {
      const w = window.innerWidth, h = window.innerHeight, asp = w / h;
      renderer.setSize(w, h);
      perspCam.aspect = asp;
      perspCam.updateProjectionMatrix();
      orthoCam.left = -orthoSize * asp;
      orthoCam.right = orthoSize * asp;
      orthoCam.top = orthoSize;
      orthoCam.bottom = -orthoSize;
      orthoCam.updateProjectionMatrix();
    });

    activatePreset('gmaps_aerial');

    function animate() {
      requestAnimationFrame(animate);

      if (camState.walkMode) {
        const speed = 0.14;
        const forward = new THREE.Vector3(Math.sin(camState.yaw), 0, -Math.cos(camState.yaw));
        const right = new THREE.Vector3(Math.cos(camState.yaw), 0, Math.sin(camState.yaw));
        if (camState.keys['KeyW'] || camState.keys['ArrowUp']) perspCam.position.addScaledVector(forward, speed);
        if (camState.keys['KeyS'] || camState.keys['ArrowDown']) perspCam.position.addScaledVector(forward, -speed);
        if (camState.keys['KeyD'] || camState.keys['ArrowRight']) perspCam.position.addScaledVector(right, speed);
        if (camState.keys['KeyA'] || camState.keys['ArrowLeft']) perspCam.position.addScaledVector(right, -speed);
        if (camState.keys['KeyE'] || camState.keys['PageUp']) perspCam.position.y += speed * 0.75;
        if (camState.keys['KeyQ'] || camState.keys['PageDown']) perspCam.position.y -= speed * 0.75;
        const lookTarget = new THREE.Vector3(
          perspCam.position.x + Math.sin(camState.yaw) * Math.cos(camState.pitch),
          perspCam.position.y + Math.sin(camState.pitch),
          perspCam.position.z - Math.cos(camState.yaw) * Math.cos(camState.pitch)
        );
        perspCam.lookAt(lookTarget);
      } else {
        const kRight = camState.keys['ArrowRight'] || camState.keys['KeyD'];
        const kLeft  = camState.keys['ArrowLeft']  || camState.keys['KeyA'];
        const kUp    = camState.keys['ArrowUp']    || camState.keys['KeyW'];
        const kDown  = camState.keys['ArrowDown']  || camState.keys['KeyS'];
        const kElevU = camState.keys['KeyE']       || camState.keys['PageUp'];
        const kElevD = camState.keys['KeyQ']       || camState.keys['PageDown'];
        if (kRight || kLeft || kUp || kDown || kElevU || kElevD) {
          const step = Math.max(0.18, camState.spherical.radius * 0.0085);
          const { camRight, camUp } = getCameraScreenAxes();
          if (kRight) camState.target.addScaledVector(camRight, step);
          if (kLeft)  camState.target.addScaledVector(camRight, -step);
          if (kUp)    camState.target.addScaledVector(camUp, step);
          if (kDown)  camState.target.addScaledVector(camUp, -step);
          if (kElevU) camState.target.y += step * 0.85;
          if (kElevD) camState.target.y -= step * 0.85;
          camState.target.y = Math.max(-10.0, Math.min(95.0, camState.target.y));
          updateCameraFromOrbit();
        }
      }

      renderer.render(scene, activeCam);
      const w = window.innerWidth, h = window.innerHeight;
      const isBase = (currentFloorId === 'b1' || currentFloorId === 'b2');

      calloutObjs.forEach(c => {
        if (camState.walkMode || !showLabels || c.pos.y > clipPlane.constant) { c.el.style.opacity = '0'; return; }
        const p = c.pos.clone().project(activeCam);
        if (p.z > 1 || p.z < -1) { c.el.style.opacity = '0'; return; }
        const sx = (p.x * 0.5 + 0.5) * w, sy = (-p.y * 0.5 + 0.5) * h;
        c.el.style.left = `${sx}px`; c.el.style.top = `${sy}px`; c.el.style.opacity = '1';
      });

      gisRingLabelObjs.forEach(rl => {
        if (camState.walkMode || !gisRadiiVisible || isBase) { rl.el.style.display = 'none'; return; }
        const p = rl.pos.clone().project(activeCam);
        if (p.z > 1 || p.z < -1) { rl.el.style.display = 'none'; return; }
        const sx = (p.x * 0.5 + 0.5) * w, sy = (-p.y * 0.5 + 0.5) * h;
        if (sx < -60 || sx > w + 60 || sy < 50 || sy > h + 30) { rl.el.style.display = 'none'; return; }
        rl.el.style.display = 'block'; rl.el.style.left = `${sx}px`; rl.el.style.top = `${sy}px`;
      });

      gisPoiLabelObjs.forEach(pl => {
        const catMatch = (activeGisCategory === 'all' || pl.poi.cat === activeGisCategory);
        if (camState.walkMode || !gisPoisVisible || !catMatch || isBase) { pl.el.style.display = 'none'; return; }
        const p = pl.pos.clone().project(activeCam);
        if (p.z > 1 || p.z < -1) { pl.el.style.display = 'none'; return; }
        const sx = (p.x * 0.5 + 0.5) * w, sy = (-p.y * 0.5 + 0.5) * h;
        if (sx < -80 || sx > w + 80 || sy < 50 || sy > h + 30) { pl.el.style.display = 'none'; return; }
        pl.el.style.display = 'flex'; pl.el.style.left = `${sx}px`; pl.el.style.top = `${sy}px`;
      });

      unitBadgeObjs.forEach(ub => {
        if (camState.walkMode || !units3DVisible || !ub.mesh.visible || ub.pos.y > clipPlane.constant) { ub.el.style.display = 'none'; return; }
        const p = ub.pos.clone().project(activeCam);
        if (p.z > 1 || p.z < -1) { ub.el.style.display = 'none'; return; }
        const sx = (p.x * 0.5 + 0.5) * w, sy = (-p.y * 0.5 + 0.5) * h;
        if (sx < -60 || sx > w + 60 || sy < 50 || sy > h + 30) { ub.el.style.display = 'none'; return; }
        ub.el.style.display = 'inline-flex'; ub.el.style.left = `${sx}px`; ub.el.style.top = `${sy}px`;
      });

      measureBadges.forEach(mb => {
        const p = mb.pos.clone().project(activeCam);
        if (p.z > 1 || p.z < -1) { mb.el.style.display = 'none'; return; }
        const sx = (p.x * 0.5 + 0.5) * w, sy = (-p.y * 0.5 + 0.5) * h;
        mb.el.style.display = 'block'; mb.el.style.left = `${sx}px`; mb.el.style.top = `${sy}px`;
      });
    }
    animate();
  </script>
</body>
</html>
"""

HTML_TEMPLATE = HTML_PART1 + HTML_PART2A + HTML_PART2B

html_out = (
    HTML_TEMPLATE
    .replace("__THREE_JS_CODE__", three_js_code)
    .replace("__PLANS_JSON__", plans_json_str)
    .replace("__CRM_JSON__", crm_json_str)
    .replace("__SPATIAL_POIS_JSON__", spatial_pois_json)
    .replace("__WIDE_GMAPS_URI__", wide_gmaps_data_uri)
    .replace("__INNER_GMAPS_URI__", inner_gmaps_data_uri)
    .replace("__CLOSEUP_GMAPS_URI__", closeup_gmaps_data_uri)
    .replace("__OUTER_SPAN_M__", str(outer_span_m))
    .replace("__INNER_SPAN_M__", str(inner_span_m))
    .replace("__CLOSEUP_SPAN_M__", str(closeup_span_m))
)

os.makedirs(PROJECT_DIR, exist_ok=True)
os.makedirs(os.path.join(PROJECT_DIR, "src"), exist_ok=True)

targets = [
    os.path.join(ARTIFACT_DIR, "feierberg3_3d_bim_viewer.html"),
    os.path.join(ARTIFACT_DIR, "feierberg3_3d_model.html"),
    os.path.join(PROJECT_DIR, "feierberg3_3d_bim_viewer.html"),
    os.path.join(PROJECT_DIR, "feierberg3_3d_model.html"),
    os.path.join(PROJECT_DIR, "index.html"),
]

for p in targets:
    with open(p, "w", encoding="utf-8") as f:
        f.write(html_out)
    print("Wrote:", p, "Size:", os.path.getsize(p))
