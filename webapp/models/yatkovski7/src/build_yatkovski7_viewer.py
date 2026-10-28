# -*- coding: utf-8 -*-
import os, sys, json, shutil

sys.stdout.reconfigure(encoding='utf-8')

ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15"
SCRATCH_DIR = os.path.join(ARTIFACT_DIR, "scratch")
THREE_JS_PATH = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\_shared_engine\three.min.js"
PROJECT_DIR = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\יטקובסקי 7 פתח תקווה"

with open(THREE_JS_PATH, "r", encoding="utf-8") as f:
    three_js_code = f.read()

with open(os.path.join(SCRATCH_DIR, "yatkovski7_extracted_plans.json"), "r", encoding="utf-8") as f:
    plans_data = json.load(f)

with open(os.path.join(SCRATCH_DIR, "yatkovski7_units_crm.json"), "r", encoding="utf-8") as f:
    crm_data = json.load(f)

for u in crm_data.get("units", []):
    if u.get("floorId") == "f0":
        u["floorId"] = "kar"

for p in [
    os.path.join(SCRATCH_DIR, "yatkovski7_units_crm.json"),
    os.path.join(PROJECT_DIR, "data", "yatkovski7_units_crm.json"),
]:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(crm_data, f, ensure_ascii=False, indent=2)

with open(os.path.join(SCRATCH_DIR, "unified_yatkovski7_3d_map.json"), "r", encoding="utf-8") as f:
    unified_map_data = json.load(f)

with open(os.path.join(SCRATCH_DIR, "yatkovski7_spatial_map_data.json"), "r", encoding="utf-8") as f:
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
  <title>יטקובסקי אחים 7 (7א), פתח תקוה — מערכת שיווק, מכירות והדמיה תלת-ממדית אינטראקטיבית (1:50 CAD & GIS)</title>
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
      width: 340px; max-height: calc(100vh - 90px); overflow-y: auto;
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
      position: absolute; bottom: 14px; left: 14px; right: 368px; z-index: 25;
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
          Y7
        </div>
        <div>
          <div style="display:flex;align-items:center;gap:7px;flex-wrap:wrap;">
            <h1 style="margin:0;font-size:14px;font-weight:800;color:#0f172a;">קבוצת קולסקי · יטקובסקי אחים 7 (7א), פתח תקווה</h1>
            <span style="border-radius:6px;border:1px solid #dec9ad;background:#fef3c7;padding:1px 7px;font-size:10px;font-weight:800;color:#92400e;">א.ב. דרגן אדריכלים · פורטל שיווק ומכירות 3D (11 יח"ד · גוש 6385 חלקה 136 מגרש 57)</span>
          </div>
        </div>
      </div>

      <div style="display:flex;flex-wrap:wrap;align-items:center;gap:5px;" id="view-buttons">
        <button data-view="iso_north" id="btn-top-bldg" class="view-btn ui-btn" title="מבט חוץ אדריכלי על הבניין מרחוב האחים יטקובסקי 7">
          🏢 מבט הבניין
        </button>
        <button data-view="gmaps_regional" id="btn-top-gis-map" class="view-btn ui-btn active" title="מבט רחפן על הבניין יושב על מפת העיר פתח תקווה ו-28 מוקדי הסביבה">
          🗺️ מפת סביבה
        </button>
        <button id="btn-top-units-3d" class="ui-btn" style="border-color:#10b981;color:#065f46;background:#ecfdf5;font-weight:800;" title="הצג/הסתר סימון 11 דירות תלת-ממדי לפי זמינות ומחיר על חזיתות הבניין">
          🏢 סימון דירות 3D
        </button>
        <button id="btn-top-radii" class="ui-btn active" title="הדלק/כבה 8 מעגלי מרחק וזמני הליכה סביב יטקובסקי 7">
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
          <span>🏷️ קטלוג דירות ומחירים (11)</span>
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

    <!-- DRAWER 0: 11 UNITS CATALOG & LIVE CRM -->
    <div id="drawer-units" class="glass-panel dropdown-drawer" style="width:425px;">
      <div class="flex-between" style="margin-bottom:8px;border-bottom:1px solid #e2e8f0;padding-bottom:6px;">
        <div>
          <div style="font-size:13px;font-weight:800;color:#065f46;">🏷️ קטלוג 11 הדירות והמחירון הרשמי — יטקובסקי 7</div>
          <div style="font-size:11px;color:#64748b;">דירת גן + 8 דירות 4 חד' (ק' 1–4) + מיני-פנטהאוז ק'5 + פנטהאוז ק'6</div>
        </div>
        <button data-close-drawer class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
      </div>

      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin-bottom:8px;text-align:center;">
        <div style="background:#ecfdf5;border:1px solid #a7f3d0;border-radius:8px;padding:5px;">
          <div style="font-size:10px;color:#065f46;font-weight:700;">🟢 מלאי קולסקי זמין</div>
          <div id="kpi-avail-count" style="font-size:14px;font-weight:900;color:#047857;">6 דירות</div>
        </div>
        <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:5px;">
          <div style="font-size:10px;color:#1e40af;font-weight:700;">🏢 סה"כ בפרויקט</div>
          <div style="font-size:14px;font-weight:900;color:#1d4ed8;">11 יח"ד · 12 חניות</div>
        </div>
        <div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:8px;padding:5px;">
          <div style="font-size:10px;color:#475569;font-weight:700;">🔒 דירות בעלים</div>
          <div id="kpi-owner-count" style="font-size:14px;font-weight:900;color:#334155;">5 דירות</div>
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
        <button data-ubldg="all" class="unit-bldg-chip ui-btn active" style="padding:3px 8px;font-size:10px;">כל הדירות (11)</button>
        <button data-ubldg="N" class="unit-bldg-chip ui-btn" style="padding:3px 8px;font-size:10px;">חזית צפונית · 4 חד' (4)</button>
        <button data-ubldg="S" class="unit-bldg-chip ui-btn" style="padding:3px 8px;font-size:10px;">עורף דרומי · גן ו-4 חד' (5)</button>
        <button data-ubldg="F5" class="unit-bldg-chip ui-btn" style="padding:3px 8px;font-size:10px;">✨ מיני-פנטהאוז ק'5 (1)</button>
        <button data-ubldg="PH" class="unit-bldg-chip ui-btn" style="padding:3px 8px;font-size:10px;">👑 פנטהאוז ק'6 (1)</button>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:6px;" id="unit-status-filters">
        <button data-ustatus="all" class="unit-status-chip ui-btn active" style="padding:3px 8px;font-size:10px;">כל הסטטוסים (11)</button>
        <button data-ustatus="available" class="unit-status-chip ui-btn" style="padding:3px 8px;font-size:10px;">🟢 פנויות לשיווק קולסקי (6)</button>
        <button data-ustatus="owner" class="unit-status-chip ui-btn" style="padding:3px 8px;font-size:10px;">🔒 דירות בעלים (5)</button>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px;" id="unit-room-filters">
        <button data-urooms="all" class="unit-room-chip ui-btn active" style="padding:3px 8px;font-size:10px;">כל הגדלים</button>
        <button data-urooms="4" class="unit-room-chip ui-btn" style="padding:3px 8px;font-size:10px;">4 חד' ודירת גן (97–105 מ"ר)</button>
        <button data-urooms="5" class="unit-room-chip ui-btn" style="padding:3px 8px;font-size:10px;">5 חד' קומתיות (125–150 מ"ר)</button>
      </div>

      <div id="units-catalog-list" style="max-height:280px;overflow-y:auto;display:flex;flex-direction:column;gap:5px;padding-left:2px;"></div>
    </div>

    <!-- DRAWER 1: APARTMENT TOURS & BALCONY VIEW SIMULATOR -->
    <div id="drawer-apartments" class="glass-panel dropdown-drawer" style="width:415px;">
      <div class="flex-between" style="margin-bottom:10px;border-bottom:1px solid #e2e8f0;padding-bottom:8px;">
        <div>
          <div style="font-size:13px;font-weight:800;color:#78350f;">✨ סיור פנים מרוהט 3D (קרקע, ק' 3–4, מיני-פנטהאוז 5 ופנטהאוז 6)</div>
          <div style="font-size:11px;color:#64748b;">מידול פנים תלת-ממדי מלא במפרט פינס 48 + ג'קוזי ומטבח חוץ בפנטהאוז</div>
        </div>
        <button data-close-drawer class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
      </div>

      <div style="font-size:11px;font-weight:800;color:#92400e;margin-bottom:5px;">🛋️ מבט-על חתך Dollhouse לקומות המרוהטות בתלת-ממד (מפרט פינס 48):</div>
      <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:5px;margin-bottom:8px;">
        <button onclick="openFurnishedDollhouse('kar')" class="ui-btn ui-btn-lux" style="font-weight:800;">🌳 קרקע ודירת גן #1 (±0.00)</button>
        <button onclick="openFurnishedDollhouse('f4')" class="ui-btn ui-btn-lux" style="font-weight:800;">✨ קומה 4 טיפוסית (+13.30)</button>
        <button onclick="openFurnishedDollhouse('f5')" class="ui-btn ui-btn-lux" style="font-weight:800;">✨ מיני-פנטהאוז ק'5 (+16.53)</button>
        <button onclick="openFurnishedDollhouse('f6')" class="ui-btn" style="background:#0f172a;color:#fde047;border-color:#334155;font-weight:800;">👑 פנטהאוז ק'6 (+19.76)</button>
      </div>

      <div style="font-size:11px;font-weight:800;color:#1e3a8a;margin-bottom:5px;">🏢 סיור בגוף ראשון (1.68 מ') בדירות המרוהטות של יטקובסקי 7:</div>
      <div class="grid-2" style="margin-bottom:8px;">
        <button onclick="startPresetInteriorTour(0, 'S')" class="ui-btn ui-btn-lux">🌳 קרקע · דירת גן 4 חד' (#1)</button>
        <button onclick="startPresetInteriorTour(3, 'S')" class="ui-btn ui-btn-lux">✨ ק'3 · 4 חד' עורפית דרומית (#6)</button>
        <button onclick="startPresetInteriorTour(4, 'S')" class="ui-btn ui-btn-lux">✨ ק'4 · 4 חד' עורפית דרומית (#8)</button>
        <button onclick="startPresetInteriorTour(4, 'N')" class="ui-btn ui-btn-lux">✨ ק'4 · 4 חד' חזיתית צפונית (#9)</button>
        <button onclick="startPresetInteriorTour(5, 'F5')" class="ui-btn ui-btn-lux" style="grid-column:span 2;">✨ ק'5 · מיני-פנטהאוז קומתי 5 חד' (#10 · 150+64 מ"ר מרפסות גג)</button>
        <button onclick="startPresetInteriorTour(6, 'PH')" class="ui-btn" style="grid-column:span 2;background:#0f172a;color:#fde047;border-color:#334155;font-weight:800;">👑 ק'6 · פנטהאוז יוקרה קומתי (#11 · 125+52 מ"ר + ג'קוזי ו-BBQ)</button>
      </div>

      <div class="section-box" style="margin-bottom:0;">
        <div style="font-size:11px;font-weight:800;color:#451a03;margin-bottom:5px;">🔭 סימולטור "נוף מהמרפסת" לפי קומה מדויקת (קומות 1–6):</div>
        <div style="display:flex;flex-wrap:wrap;gap:4px;" id="balcony-floor-selector">
          <button data-bflr="1" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 1 (+3.85)</button>
          <button data-bflr="2" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 2 (+7.00)</button>
          <button data-bflr="3" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 3 (+10.15)</button>
          <button data-bflr="4" class="ui-btn active" style="padding:3px 7px;font-size:10px;">קומה 4 (+13.30)</button>
          <button data-bflr="5" class="ui-btn" style="padding:3px 7px;font-size:10px;">מיני-פנטהאוז 5 (+16.53)</button>
          <button data-bflr="6" class="ui-btn" style="padding:3px 7px;font-size:10px;">פנטהאוז 6 (+19.76)</button>
        </div>
      </div>
    </div>

    <!-- DRAWER 2: 3D GIS SPATIAL MAP & 28 POIS -->
    <div id="drawer-gis" class="glass-panel dropdown-drawer" style="width:410px;">
      <div class="flex-between" style="margin-bottom:8px;border-bottom:1px solid #e2e8f0;padding-bottom:6px;">
        <div>
          <div style="font-size:13px;font-weight:800;color:#1e3a8a;">📍 מפת מרחקים ו-28 מוקדי סביבה ועירוניות (Google Maps)</div>
          <div style="font-size:11px;color:#64748b;">חינוך, קניות, בריאות, תחבורה ורכבת קלה, תרבות ופארקים סביב יטקובסקי 7</div>
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
        <a href="yatkovski7_spatial_map.html" target="_blank" class="ui-btn" style="background:#0f172a;color:#38bdf8;border-color:#334155;font-weight:800;text-decoration:none;">
          🧭 מפת GIS דו-ממדית (28) ↗
        </a>
        <button id="btn-side-radii" class="ui-btn active">⭕ רדיוסים (8): פעיל</button>
        <button id="btn-side-pois" class="ui-btn active">📍 מיקומים (28): פעיל</button>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px;" id="gis-cat-buttons">
        <button data-gcat="all" class="gis-cat-chip ui-btn active" style="padding:3px 7px;font-size:10px;">הכל (28)</button>
        <button data-gcat="education" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🎓 חינוך (8)</button>
        <button data-gcat="transport" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🚌 תחבורה ורק"ל (6)</button>
        <button data-gcat="shopping" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🛒 קניות ומסחר (5)</button>
        <button data-gcat="health" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🏥 בריאות ורפואה (4)</button>
        <button data-gcat="parks" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🌳 פארקים ותרבות (5)</button>
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
            🗺️ מפת לוויין Google Maps (יטקובסקי 7): פעיל
          </button>
          <button id="btn-ortho" class="ui-btn">📐 היטל אורתוגרפי (1:50)</button>
          <button id="btn-cad-plan" class="ui-btn active">✏️ שרטוט פנים CAD: פעיל</button>
          <button onclick="activatePreset('iso_north')" class="ui-btn">חזית צפונית (יטקובסקי)</button>
          <button onclick="activatePreset('iso_south')" class="ui-btn">חזית דרומית (גינה עורפית)</button>
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
            <span id="clip-val" class="cad-badge" style="font-size:11px;font-weight:800;color:#2563eb;">+26.50 מ' (מלא)</span>
          </div>
          <input id="clip-slider" type="range" min="-4.40" max="26.5" step="0.1" value="26.5" />
          <div class="flex-between cad-badge" style="margin-top:3px;font-size:9.5px;color:#64748b;">
            <span>-4.38</span>
            <span>0.00</span>
            <span>+7.00</span>
            <span>+13.30</span>
            <span>+19.76</span>
            <span>+25.99</span>
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
          <span id="apt-active-badge" style="border-radius:6px;background:#b45309;color:#ffffff;padding:3px 8px;font-size:11px;font-weight:800;">יטקובסקי 7</span>
          <span id="aptc-active-room-title" style="font-size:13px;font-weight:800;color:#451a03;">סיור פנים אדריכלי 1:50</span>
          <div style="display:inline-flex;align-items:center;gap:3px;background:#fef3c7;border:1px solid #f59e0b;border-radius:6px;padding:2px 6px;">
            <span style="font-size:10px;font-weight:800;color:#92400e;">קומה לנוף:</span>
            <select id="tour-floor-select" style="font-size:11px;font-weight:800;color:#451a03;background:transparent;border:none;cursor:pointer;outline:none;">
              <option value="1">קומה 1 (+3.85)</option>
              <option value="2">קומה 2 (+7.00)</option>
              <option value="3">קומה 3 (+10.15)</option>
              <option value="4" selected>קומה 4 (+13.30)</option>
              <option value="5">מיני-פנטהאוז 5 (+16.53)</option>
              <option value="6">פנטהאוז 6 (+19.76)</option>
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
          <button onclick="teleportInTour(0.5, -2.8, 0, 'דירה צפונית (4 חד\') · סלון ומטבח')" class="room-chip">🛋️ סלון צפוני (4 חד')</button>
          <button onclick="teleportInTour(-1.2, -6.2, 0, 'דירה צפונית · מרפסת סוכה לרחוב יטקובסקי')" class="room-chip">☀️ מרפסת צפונית (יטקובסקי)</button>
          <button onclick="teleportInTour(-4.8, 11.2, 3.14, 'דירה דרומית (4 חד\') · סלון ומטבח')" class="room-chip">🛋️ סלון דרומי (4 חד')</button>
          <button onclick="teleportInTour(-3.8, 15.1, 3.14, 'דירה דרומית · מרפסת סוכה עורפית')" class="room-chip">☀️ מרפסת דרומית</button>
          <button onclick="teleportInTour(-1.5, -4.4, 0, 'מיני-פנטהאוז קומה 5 · מרפסת גג צפונית ופרגולה', 'f5')" class="room-chip">✨ גג מיני-פנטהאוז ק'5</button>
          <button onclick="teleportInTour(0.4, 12.2, 3.14, 'פנטהאוז קומה 6 · מרפסת גג דרומית, ג\'קוזי ו-BBQ', 'f6')" class="room-chip">👑 גג פנטהאוז ק'6 (ג'קוזי ו-BBQ)</button>
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
    // 1. EXACT FLOOR SCHEDULE & ARCHITECTURAL CONSTANTS (YATKOVSKI 7)
    // =========================================================================
    const FLOORS = [
      { id: 'mar', label: 'מרתף חניון (12 חניות)',   zFloor: -4.38, zCeil: -0.25, zTop: 0.00,  sheet: 'basement',  elevText: '-4.38' },
      { id: 'kar', label: 'קרקע · לובי ודירת גן #1 ✨', zFloor: 0.00,  zCeil: 3.60,  zTop: 3.85,  sheet: 'ground',    elevText: '±0.00',  has3DFurn: true },
      { id: 'f1',  label: 'קומה 1 (דירות 2–3)',       zFloor: 3.85,  zCeil: 6.75,  zTop: 7.00,  sheet: 'typical',   elevText: '+3.85' },
      { id: 'f2',  label: 'קומה 2 (דירות 4–5)',       zFloor: 7.00,  zCeil: 9.90,  zTop: 10.15, sheet: 'typical',   elevText: '+7.00' },
      { id: 'f3',  label: 'קומה 3 · מרוהטת 3D ✨',    zFloor: 10.15, zCeil: 13.05, zTop: 13.30, sheet: 'typical',   elevText: '+10.15', has3DFurn: true },
      { id: 'f4',  label: 'קומה 4 · מרוהטת 3D ✨',    zFloor: 13.30, zCeil: 16.28, zTop: 16.53, sheet: 'typical',   elevText: '+13.30', has3DFurn: true },
      { id: 'f5',  label: 'קומה 5 · מיני-פנטהאוז ✨', zFloor: 16.53, zCeil: 19.51, zTop: 19.76, sheet: 'floor_5',   elevText: '+16.53', has3DFurn: true },
      { id: 'f6',  label: 'קומה 6 · פנטהאוז 3D 👑',   zFloor: 19.76, zCeil: 22.74, zTop: 22.99, sheet: 'penthouse', elevText: '+19.76', has3DFurn: true },
      { id: 'gag', label: 'גג עליון ומגדל מעלית',     zFloor: 22.99, zCeil: 25.99, zTop: 25.99, sheet: 'roof_main', elevText: '+22.99' }
    ];

    const LAYERS_DEF = [
      { id: 'walls',     name: 'קירות חוץ (טיח/אבן לבנה + אפור פחם) וקירות פנים', color: '#fcfdff', visible: true },
      { id: 'slabs',     name: 'רצפות, תקרות וקרניזים היקפיים (4 חבילות גמר)', color: '#d6dae0', visible: true },
      { id: 'windows',   name: 'חלונות, וויטרינות, תריסים כהים ומעקות זכוכית', color: '#38bdf8', visible: true },
      { id: 'doors',     name: 'דלתות פנים וכניסה + חלונות הדף ממ"ד', color: '#c89d6c', visible: true },
      { id: 'balconies', name: 'מרפסות סוכה, מרפסות גג קומות 5–6 ומעקות', color: '#a46b3f', visible: true },
      { id: 'pergolas',  name: 'פרגולות קומות 5–6, רפפות מסתורי כביסה וקולטים', color: '#334155', visible: true },
      { id: 'furn3d',    name: 'ריהוט פנים תלת-ממדי יוקרתי (קרקע, ק\' 3–4, 5 ו-6)', color: '#d97706', visible: true },
      { id: 'cad2d',     name: 'תוכנית CAD וקטורית 1:50 על הרצפה', color: '#475569', visible: true },
      { id: 'labels',    name: 'שמות ומידות חדרים פנימיות (בס"מ)', color: '#1e293b', visible: true },
      { id: 'site',      name: 'חניון מרתף (12 חניות), גינת דירה #1 ופיתוח מגרש', color: '#94a3b8', visible: true }
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

    const clipPlane = new THREE.Plane(new THREE.Vector3(0, -1, 0), 26.5);
    const clippingPlanes = [clipPlane];

    const aspect = window.innerWidth / window.innerHeight;
    const perspCam = new THREE.PerspectiveCamera(42, aspect, 0.2, 8000);
    const orthoSize = 20;
    const orthoCam = new THREE.OrthographicCamera(-orthoSize * aspect, orthoSize * aspect, orthoSize, -orthoSize, -2000, 6000);
    let activeCam = perspCam;
    let isOrtho = false;

    const hemiLight = new THREE.HemisphereLight(0xfffdf8, 0xd8d0c2, 0.66);
    hemiLight.position.set(0, 120, 0);
    scene.add(hemiLight);

    const dirLight = new THREE.DirectionalLight(0xfffaf0, 0.72);
    dirLight.position.set(42, 76, -42);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 2048;
    dirLight.shadow.mapSize.height = 2048;
    dirLight.shadow.camera.near = 10;
    dirLight.shadow.camera.far = 200;
    const dCam = 34;
    dirLight.shadow.camera.left = -dCam;
    dirLight.shadow.camera.right = dCam;
    dirLight.shadow.camera.top = dCam;
    dirLight.shadow.camera.bottom = -dCam;
    dirLight.shadow.bias = -0.0004;
    scene.add(dirLight);

    const fillLight = new THREE.DirectionalLight(0xf3ede2, 0.30);
    fillLight.position.set(-48, 45, 48);
    scene.add(fillLight);

    const nightLightsGroup = new THREE.Group();
    nightLightsGroup.visible = false;
    scene.add(nightLightsGroup);
    [[-3, 12, -3], [2, 12, 10], [-3, 18, -3], [-2, 18, 12], [-2, 21, -2], [0, 21, 11], [0, 2.5, -2]].forEach(([lx, ly, lz]) => {
      const pl = new THREE.PointLight(0xffb454, 1.4, 30, 1.8);
      pl.position.set(lx, ly, lz);
      nightLightsGroup.add(pl);
    });

    // =========================================================================
    // 3. ARCHITECTURAL MATERIALS & PINES-48 LUXURY INTERIOR PBR MATERIALS
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

    function makeOffWhitePlasterTexture() {
      const c = document.createElement('canvas');
      c.width = 256; c.height = 256;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#e8dfd0'; ctx.fillRect(0, 0, 256, 256);
      for (let i = 0; i < 240; i++) {
        ctx.fillStyle = (i % 2 === 0) ? 'rgba(210, 198, 178, 0.26)' : 'rgba(242, 236, 224, 0.30)';
        ctx.fillRect(Math.random() * 256, Math.random() * 256, 14 + Math.random() * 28, 8 + Math.random() * 18);
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(3, 3);
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

    const texTravertine   = makeTravertineFloorTexture();
    const texCalacatta    = makeCalacattaMarbleTexture();
    const texFlutedOak    = makeFlutedOakTexture();
    const texWovenRug     = makeWovenRugTexture();
    const texOffWhiteWall = makeOffWhitePlasterTexture();

    const MATS = {
      wall: new THREE.MeshStandardMaterial({ map: texOffWhiteWall, color: 0xe8dfd0, roughness: 0.85, metalness: 0.01, side: THREE.DoubleSide, clippingPlanes }),
      extWall: new THREE.MeshStandardMaterial({ color: 0xfcfdff, roughness: 0.72, metalness: 0.02, side: THREE.DoubleSide, clippingPlanes }),
      darkSpandrel: new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.55, metalness: 0.25, side: THREE.DoubleSide, clippingPlanes }),
      wallCap: new THREE.MeshStandardMaterial({ color: 0xd2c7b4, roughness: 0.88, metalness: 0.02, side: THREE.DoubleSide, clippingPlanes }),
      slabFloor: new THREE.MeshStandardMaterial({ map: FINISH_TEXTURES.nordic.map, color: 0xd8dce2, roughness: 0.65, metalness: 0.04, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, clippingPlanes }),
      slabEdge: new THREE.MeshStandardMaterial({ color: 0xfcfdff, roughness: 0.76, clippingPlanes }),
      terraceFloor: new THREE.MeshStandardMaterial({ color: 0xcbd5e1, roughness: 0.72, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, clippingPlanes }),
      woodDeck: new THREE.MeshStandardMaterial({ map: DECK_TEXTURES.wood, roughness: 0.55, metalness: 0.05, clippingPlanes }),
      glassRailing: new THREE.MeshPhysicalMaterial({ color: 0xdbeafe, transparent: true, opacity: 0.38, roughness: 0.1, metalness: 0.05, side: THREE.DoubleSide, clippingPlanes }),
      aluDark: new THREE.MeshStandardMaterial({ color: 0x242930, roughness: 0.4, metalness: 0.6, clippingPlanes }),
      louverGray: new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.45, metalness: 0.55, clippingPlanes }),
      winGlass: new THREE.MeshPhysicalMaterial({ color: 0x7dd3fc, emissive: 0x0284c7, emissiveIntensity: 0.14, transparent: true, opacity: 0.66, roughness: 0.06, metalness: 0.25, side: THREE.DoubleSide, clippingPlanes }),
      lightWood: new THREE.MeshStandardMaterial({ color: 0xd4ad7d, roughness: 0.52, metalness: 0.04, clippingPlanes }),
      doorFrame: new THREE.MeshStandardMaterial({ color: 0xb0895a, roughness: 0.55, clippingPlanes }),
      mamadSteel: new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.35, metalness: 0.72, clippingPlanes }),
      basementConcrete: new THREE.MeshStandardMaterial({ color: 0xcbd5e1, roughness: 0.85, side: THREE.DoubleSide, clippingPlanes }),
      asphalt: new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.9, clippingPlanes }),
      sidewalk: new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.85, clippingPlanes }),
      grass: new THREE.MeshStandardMaterial({ color: 0xd1fae5, roughness: 0.9, clippingPlanes }),
      solarPanel: new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.25, metalness: 0.5, clippingPlanes }),
      waterSpa: new THREE.MeshPhysicalMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.72, roughness: 0.08, metalness: 0.1, clippingPlanes }),
      lineFurn: new THREE.LineBasicMaterial({ color: 0x334155, transparent: true, opacity: 0.85, clippingPlanes }),
      lineCad: new THREE.LineBasicMaterial({ color: 0x0f172a, transparent: true, opacity: 0.78, clippingPlanes }),
      luxTravertine: new THREE.MeshStandardMaterial({ map: texTravertine, color: 0xf5f0e6, roughness: 0.36, metalness: 0.05, clippingPlanes }),
      luxCalacatta:  new THREE.MeshStandardMaterial({ map: texCalacatta,  color: 0xffffff, roughness: 0.18, metalness: 0.08, clippingPlanes }),
      luxFlutedOak:  new THREE.MeshStandardMaterial({ map: texFlutedOak,  color: 0xd4ad7e, roughness: 0.48, metalness: 0.05, clippingPlanes }),
      luxOakSmooth:  new THREE.MeshStandardMaterial({ color: 0xc89d6c, roughness: 0.42, metalness: 0.06, clippingPlanes }),
      luxBoucle:     new THREE.MeshStandardMaterial({ color: 0xf7f3eb, roughness: 0.88, metalness: 0.01, clippingPlanes }),
      luxLinenSand:  new THREE.MeshStandardMaterial({ color: 0xe5dccb, roughness: 0.82, metalness: 0.01, clippingPlanes }),
      luxTaupe:      new THREE.MeshStandardMaterial({ color: 0x9c8b7a, roughness: 0.78, metalness: 0.02, clippingPlanes }),
      luxCabinet:    new THREE.MeshStandardMaterial({ color: 0xf3efe6, roughness: 0.35, metalness: 0.04, clippingPlanes }),
      luxBrass:      new THREE.MeshStandardMaterial({ color: 0xd4af37, roughness: 0.24, metalness: 0.82, clippingPlanes }),
      luxRug:        new THREE.MeshStandardMaterial({ map: texWovenRug, color: 0xede6d8, roughness: 0.92, metalness: 0.0, clippingPlanes }),
      luxCurtain:    new THREE.MeshPhysicalMaterial({ color: 0xfaf7f0, transparent: true, opacity: 0.55, roughness: 0.65, side: THREE.DoubleSide, clippingPlanes }),
      luxDarkGlass:  new THREE.MeshPhysicalMaterial({ color: 0x111827, roughness: 0.12, metalness: 0.25, clippingPlanes }),
      luxClearGlass: new THREE.MeshPhysicalMaterial({ color: 0xe0f2fe, transparent: true, opacity: 0.34, roughness: 0.08, metalness: 0.1, side: THREE.DoubleSide, clippingPlanes }),
      luxMirror:     new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.05, metalness: 0.92, clippingPlanes }),
      luxGlowWarm:   new THREE.MeshBasicMaterial({ color: 0xffefc2, clippingPlanes }),
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
    // 4. GEOMETRY HELPERS (PRESERVING EXACT 1:1 YATKOVSKI 7 ARCHITECTURE)
    // =========================================================================
    function isExteriorWallFace(sheetKey, x1, y1, x2, y2) {
      if (sheetKey === 'roof_main') return true;
      if (sheetKey === 'basement') return false;
      const xm = 0.5 * (x1 + x2);
      const ym = 0.5 * (y1 + y2);
      const tol = 0.14;
      if (xm <= -8.00 + tol || xm >= 3.85 - tol || ym <= -2.55 + tol || ym >= 9.10 - tol) {
        return true;
      }
      return false;
    }

    function buildExtrudedTriPoly(polyData, z0, z1, matWall, matCap, sheetKey = null, matExtWall = null) {
      const grp = new THREE.Group();
      const h = z1 - z0;
      if (h <= 0.005) return grp;

      const capPos = [];
      for (const t of polyData.tris) {
        capPos.push(t[0][0], z1, t[0][1], t[2][0], z1, t[2][1], t[1][0], z1, t[1][1]);
        capPos.push(t[0][0], z0, t[0][1], t[1][0], z0, t[1][1], t[2][0], z0, t[2][1]);
      }
      const capGeo = new THREE.BufferGeometry();
      capGeo.setAttribute('position', new THREE.Float32BufferAttribute(capPos, 3));
      capGeo.computeVertexNormals();
      const capMesh = new THREE.Mesh(capGeo, matCap || matWall);
      capMesh.castShadow = true;
      capMesh.receiveShadow = true;
      grp.add(capMesh);

      const intSidePos = [];
      const extSidePos = [];
      const rings = [polyData.exterior, ...(polyData.holes || [])];
      for (const ring of rings) {
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
      return grp;
    }

    function makeBox(x0, y0, x1, y1, z0, z1, mat, castShadow = true) {
      const w = Math.abs(x1 - x0);
      const d = Math.abs(y1 - y0);
      const h = Math.abs(z1 - z0);
      if (w < 0.002 || d < 0.002 || h < 0.002) return new THREE.Group();
      const geo = new THREE.BoxGeometry(w, h, d);
      const m = new THREE.Mesh(geo, mat);
      m.position.set(0.5 * (x0 + x1), 0.5 * (z0 + z1), 0.5 * (y0 + y1));
      m.castShadow = castShadow;
      m.receiveShadow = true;
      return m;
    }

    function makeExteriorOpeningWallBox(x0, y0, x1, y1, z0, z1, orient, useDarkSpandrel = false) {
      const xm = 0.5 * (x0 + x1);
      const ym = 0.5 * (y0 + y1);
      const extMat = useDarkSpandrel ? MATS.darkSpandrel : MATS.extWall;
      let matPX = MATS.wall, matNX = MATS.wall, matPZ = MATS.wall, matNZ = MATS.wall;
      if (orient === 'H') {
        if (ym > 4.0) matPZ = extMat;
        else matNZ = extMat;
      } else {
        if (xm > -1.0) matPX = extMat;
        else matNX = extMat;
      }
      return makeBox(x0, y0, x1, y1, z0, z1, [matPX, matNX, MATS.wallCap, MATS.wallCap, matPZ, matNZ]);
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

      const useDarkBelow = (orient === 'V') && (midX <= -7.9 || midX >= 3.8);
      const useDarkAbove = true;

      if (kind === 'vitrine') {
        const zTopOpen = (floorObj.id === 'kar') ? Math.min(zFloor + 2.80, zCeil - 0.15) : Math.min(zFloor + 2.25, zCeil - 0.15);
        if (zCeil > zTopOpen + 0.02) {
          const lintel = makeExteriorOpeningWallBox(x0, y0, x1, y1, zTopOpen, zCeil, orient, true);
          addToFloorAndLayer(floorObj.id, 'walls', lintel);
        }
        const vGrp = new THREE.Group();
        const fThick = 0.055;
        const padOut = 0.012;
        if (orient === 'H') {
          const fy0 = y0 - padOut, fy1 = y1 + padOut;
          vGrp.add(makeBox(x0, fy0, x1, fy1, zFloor, zFloor + fThick, MATS.aluDark, false));
          vGrp.add(makeBox(x0, fy0, x1, fy1, zTopOpen - fThick, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(x0, fy0, x0 + fThick, fy1, zFloor, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(x1 - fThick, fy0, x1, fy1, zFloor, zTopOpen, MATS.aluDark, false));
          const nPanels = (span >= 2.60) ? 3 : 2;
          for (let i = 1; i < nPanels; i++) {
            const mx = x0 + (span * i) / nPanels;
            vGrp.add(makeBox(mx - 0.025, fy0 + 0.02, mx + 0.025, fy1 - 0.02, zFloor, zTopOpen, MATS.aluDark, false));
          }
          vGrp.add(makeBox(x0 + fThick, midY - 0.022, x1 - fThick, midY + 0.022, zFloor + fThick, zTopOpen - fThick, MATS.winGlass, false));
        } else {
          const fx0 = x0 - padOut, fx1 = x1 + padOut;
          vGrp.add(makeBox(fx0, y0, fx1, y1, zFloor, zFloor + fThick, MATS.aluDark, false));
          vGrp.add(makeBox(fx0, y0, fx1, y1, zTopOpen - fThick, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(fx0, y0, fx1, y0 + fThick, zFloor, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(fx0, y1 - fThick, fx1, y1, zFloor, zTopOpen, MATS.aluDark, false));
          const nPanels = (span >= 2.60) ? 3 : 2;
          for (let i = 1; i < nPanels; i++) {
            const my = y0 + (span * i) / nPanels;
            vGrp.add(makeBox(fx0 + 0.02, my - 0.025, fx1 - 0.02, my + 0.025, zFloor, zTopOpen, MATS.aluDark, false));
          }
          vGrp.add(makeBox(midX - 0.022, y0 + fThick, midX + 0.022, y1 - fThick, zFloor + fThick, zTopOpen - fThick, MATS.winGlass, false));
        }
        addToFloorAndLayer(floorObj.id, 'windows', vGrp);

      } else if (kind === 'win_tall') {
        const zSill = zFloor + 0.40;
        const zGuard = zFloor + 1.05;
        const zHead = Math.min(zFloor + 2.30, zCeil - 0.15);
        addToFloorAndLayer(floorObj.id, 'walls', makeExteriorOpeningWallBox(x0, y0, x1, y1, zFloor, zSill, orient, useDarkBelow));
        if (zCeil > zHead + 0.02) {
          addToFloorAndLayer(floorObj.id, 'walls', makeExteriorOpeningWallBox(x0, y0, x1, y1, zHead, zCeil, orient, useDarkAbove));
        }
        const wGrp = new THREE.Group();
        const fThick = 0.05;
        const padOut = 0.015;
        if (orient === 'H') {
          const fy0 = y0 - padOut, fy1 = y1 + padOut;
          const outY = (midY < 4.0) ? (y0 - 0.02) : (y1 + 0.02);
          wGrp.add(makeBox(x0 - 0.02, y0 - 0.035, x1 + 0.02, y1 + 0.035, zSill - 0.035, zSill + 0.02, MATS.slabEdge, false));
          wGrp.add(makeBox(x0, fy0, x1, fy1, zHead - fThick, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(x0, fy0, x1, fy1, zGuard - 0.028, zGuard + 0.028, MATS.aluDark, false));
          wGrp.add(makeBox(x0, fy0, x0 + fThick, fy1, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(x1 - fThick, fy0, x1, fy1, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(midX - 0.025, fy0 + 0.01, midX + 0.025, fy1 - 0.01, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(x0 + fThick, midY - 0.02, x1 - fThick, midY + 0.02, zSill + 0.02, zHead - fThick, MATS.winGlass, false));
          wGrp.add(makeBox(x0 + 0.02, outY - 0.012, x1 - 0.02, outY + 0.012, zSill + 0.02, zGuard, MATS.glassRailing, false));
        } else {
          const fx0 = x0 - padOut, fx1 = x1 + padOut;
          const outX = (midX < -1.0) ? (x0 - 0.02) : (x1 + 0.02);
          wGrp.add(makeBox(x0 - 0.035, y0 - 0.02, x1 + 0.035, y1 + 0.02, zSill - 0.035, zSill + 0.02, MATS.slabEdge, false));
          wGrp.add(makeBox(fx0, y0, fx1, y1, zHead - fThick, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(fx0, y0, fx1, y1, zGuard - 0.028, zGuard + 0.028, MATS.aluDark, false));
          wGrp.add(makeBox(fx0, y0, fx1, y0 + fThick, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(fx0, y1 - fThick, fx1, y1, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(fx0 + 0.01, midY - 0.025, fx1 - 0.01, midY + 0.025, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(midX - 0.02, y0 + fThick, midX + 0.02, y1 - fThick, zSill + 0.02, zHead - fThick, MATS.winGlass, false));
          wGrp.add(makeBox(outX - 0.012, y0 + 0.02, outX + 0.012, y1 - 0.02, zSill + 0.02, zGuard, MATS.glassRailing, false));
        }
        addToFloorAndLayer(floorObj.id, 'windows', wGrp);

      } else if (kind === 'mamad_win') {
        const zSill = zFloor + 1.05;
        const zHead = Math.min(zFloor + 2.05, zCeil - 0.15);
        addToFloorAndLayer(floorObj.id, 'walls', makeExteriorOpeningWallBox(x0, y0, x1, y1, zFloor, zSill, orient, false));
        if (zCeil > zHead + 0.02) {
          addToFloorAndLayer(floorObj.id, 'walls', makeExteriorOpeningWallBox(x0, y0, x1, y1, zHead, zCeil, orient, false));
        }
        const mGrp = new THREE.Group();
        const fThick = 0.06;
        const fy0 = y0 - 0.02, fy1 = y1 + 0.02;
        mGrp.add(makeBox(x0 - 0.02, fy0 - 0.015, x1 + 0.02, fy1 + 0.015, zSill - 0.03, zSill + 0.02, MATS.slabEdge, false));
        mGrp.add(makeBox(x0, fy0, x1, fy1, zSill, zSill + fThick, MATS.mamadSteel, false));
        mGrp.add(makeBox(x0, fy0, x1, fy1, zHead - fThick, zHead, MATS.mamadSteel, false));
        mGrp.add(makeBox(x0, fy0, x0 + fThick, fy1, zSill, zHead, MATS.mamadSteel, false));
        mGrp.add(makeBox(x1 - fThick, fy0, x1, fy1, zSill, zHead, MATS.mamadSteel, false));
        mGrp.add(makeBox(midX - 0.022, fy0 + 0.01, midX + 0.022, fy1 - 0.01, zSill, zHead, MATS.mamadSteel, false));
        mGrp.add(makeBox(x0 + fThick, midY - 0.02, x1 - fThick, midY + 0.02, zSill + fThick, zHead - fThick, MATS.winGlass, false));
        addToFloorAndLayer(floorObj.id, 'windows', mGrp);

      } else if (kind === 'window') {
        const zSill = zFloor + 1.05;
        const zHead = Math.min(zFloor + 2.30, zCeil - 0.15);
        addToFloorAndLayer(floorObj.id, 'walls', makeExteriorOpeningWallBox(x0, y0, x1, y1, zFloor, zSill, orient, useDarkBelow));
        if (zCeil > zHead + 0.02) {
          addToFloorAndLayer(floorObj.id, 'walls', makeExteriorOpeningWallBox(x0, y0, x1, y1, zHead, zCeil, orient, useDarkAbove));
        }
        const wGrp = new THREE.Group();
        const fThick = 0.05;
        const padOut = 0.015;
        if (orient === 'H') {
          const fy0 = y0 - padOut, fy1 = y1 + padOut;
          wGrp.add(makeBox(x0 - 0.02, y0 - 0.035, x1 + 0.02, y1 + 0.035, zSill - 0.035, zSill + 0.02, MATS.slabEdge, false));
          wGrp.add(makeBox(x0, fy0, x1, fy1, zHead - fThick, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(x0, fy0, x0 + fThick, fy1, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(x1 - fThick, fy0, x1, fy1, zSill, zHead, MATS.aluDark, false));
          const nPanes = (span >= 2.20) ? 3 : ((span >= 1.05) ? 2 : 1);
          for (let i = 1; i < nPanes; i++) {
            const mx = x0 + (span * i) / nPanes;
            wGrp.add(makeBox(mx - 0.024, fy0 + 0.01, mx + 0.024, fy1 - 0.01, zSill, zHead, MATS.aluDark, false));
          }
          wGrp.add(makeBox(x0 + fThick, midY - 0.02, x1 - fThick, midY + 0.02, zSill + 0.02, zHead - fThick, MATS.winGlass, false));
        } else {
          const fx0 = x0 - padOut, fx1 = x1 + padOut;
          wGrp.add(makeBox(x0 - 0.035, y0 - 0.02, x1 + 0.035, y1 + 0.02, zSill - 0.035, zSill + 0.02, MATS.slabEdge, false));
          wGrp.add(makeBox(fx0, y0, fx1, y1, zHead - fThick, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(fx0, y0, fx1, y0 + fThick, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(fx0, y1 - fThick, fx1, y1, zSill, zHead, MATS.aluDark, false));
          const nPanes = (span >= 2.20) ? 3 : ((span >= 1.05) ? 2 : 1);
          for (let i = 1; i < nPanes; i++) {
            const my = y0 + (span * i) / nPanes;
            wGrp.add(makeBox(fx0 + 0.01, my - 0.024, fx1 - 0.01, my + 0.024, zSill, zHead, MATS.aluDark, false));
          }
          wGrp.add(makeBox(midX - 0.02, y0 + fThick, midX + 0.02, y1 - fThick, zSill + 0.02, zHead - fThick, MATS.winGlass, false));
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
      ctx.roundRect(14, 14, 228, dimsText ? 96 : 62, 12);
      ctx.fill();
      ctx.strokeStyle = 'rgba(71, 85, 105, 0.40)';
      ctx.lineWidth = 2;
      ctx.stroke();

      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = '#0f172a';
      ctx.font = 'bold 24px "Segoe UI", Arial, sans-serif';
      ctx.fillText(nameText, 128, dimsText ? 44 : 45);

      if (dimsText) {
        ctx.fillStyle = '#1d4ed8';
        ctx.font = 'bold 21px "Segoe UI", monospace, sans-serif';
        const suffix = dimsText.includes('×') ? ' ס"מ' : '';
        ctx.fillText(dimsText + suffix, 128, 82);
      }

      const tex = new THREE.CanvasTexture(c);
      tex.anisotropy = 4;
      const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, side: THREE.DoubleSide, clippingPlanes });
      const geo = new THREE.PlaneGeometry(1.70, 0.85);
      geo.rotateX(-Math.PI / 2);
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(x, zFloor + 0.028, y);
      return mesh;
    }

    function buildBalconyBox(floorId, x0, y0, x1, y1, zFloor, openSides, hasPergola = false, railHeight = 1.05, thickFascia = false) {
      const bGrp = new THREE.Group();
      const sDepth = thickFascia ? 0.36 : 0.25;
      const curbH = thickFascia ? 0.20 : 0.14;
      bGrp.add(makeBox(x0 - 0.06, y0 - 0.06, x1 + 0.06, y1 + 0.06, zFloor - sDepth, zFloor - 0.03, MATS.extWall));
      bGrp.add(makeBox(x0, y0, x1, y1, zFloor - 0.03, zFloor + 0.01, MATS.woodDeck));

      const zRailTop = zFloor + railHeight;
      const cMat = MATS.extWall;
      openSides.forEach(side => {
        if (side === 'W') {
          bGrp.add(makeBox(x0, y0, x0 + 0.14, y1, zFloor, zFloor + curbH, cMat, false));
          bGrp.add(makeBox(x0 + 0.03, y0 + 0.03, x0 + 0.06, y1 - 0.03, zFloor + curbH, zRailTop - 0.03, MATS.glassRailing, false));
          bGrp.add(makeBox(x0 + 0.01, y0, x0 + 0.08, y1, zRailTop - 0.03, zRailTop, MATS.aluDark, false));
        } else if (side === 'E') {
          bGrp.add(makeBox(x1 - 0.14, y0, x1, y1, zFloor, zFloor + curbH, cMat, false));
          bGrp.add(makeBox(x1 - 0.06, y0 + 0.03, x1 - 0.03, y1 - 0.03, zFloor + curbH, zRailTop - 0.03, MATS.glassRailing, false));
          bGrp.add(makeBox(x1 - 0.08, y0, x1 - 0.01, y1, zRailTop - 0.03, zRailTop, MATS.aluDark, false));
        } else if (side === 'N') {
          bGrp.add(makeBox(x0, y0, x1, y0 + 0.14, zFloor, zFloor + curbH, cMat, false));
          bGrp.add(makeBox(x0 + 0.03, y0 + 0.03, x1 - 0.03, y0 + 0.06, zFloor + curbH, zRailTop - 0.03, MATS.glassRailing, false));
          bGrp.add(makeBox(x0, y0 + 0.01, x1, y0 + 0.08, zRailTop - 0.03, zRailTop, MATS.aluDark, false));
        } else if (side === 'S') {
          bGrp.add(makeBox(x0, y1 - 0.14, x1, y1, zFloor, zFloor + curbH, cMat, false));
          bGrp.add(makeBox(x0 + 0.03, y1 - 0.06, x1 - 0.03, y1 - 0.03, zFloor + curbH, zRailTop - 0.03, MATS.glassRailing, false));
          bGrp.add(makeBox(x0, y1 - 0.08, x1, y1 - 0.01, zRailTop - 0.03, zRailTop, MATS.aluDark, false));
        }
      });

      addToFloorAndLayer(floorId, 'balconies', bGrp);
      if (hasPergola) buildLightPergola(floorId, x0, y0, x1, y1, zFloor + 2.68);
    }

    function buildLightPergola(floorId, x0, y0, x1, y1, zPergola) {
      const pGrp = new THREE.Group();
      const fH = 0.20, fW = 0.15;
      pGrp.add(makeBox(x0, y0, x1, y0 + fW, zPergola, zPergola + fH, MATS.extWall));
      pGrp.add(makeBox(x0, y1 - fW, x1, y1, zPergola, zPergola + fH, MATS.extWall));
      pGrp.add(makeBox(x0, y0, x0 + fW, y1, zPergola, zPergola + fH, MATS.extWall));
      pGrp.add(makeBox(x1 - fW, y0, x1, y1, zPergola, zPergola + fH, MATS.extWall));
      for (let y = y0 + 0.28; y < y1 - 0.18; y += 0.30) {
        pGrp.add(makeBox(x0 + fW, y, x1 - fW, y + 0.05, zPergola + 0.04, zPergola + fH - 0.03, MATS.aluDark, false));
      }
      addToFloorAndLayer(floorId, 'pergolas', pGrp);
    }

    // =========================================================================
    // 5. BUILD ALL FLOORS + 12 UNDERGROUND PARKING STALLS (YATKOVSKI 7)
    // =========================================================================
    let parkingHighlightMesh = null;

    function createParkingStallMesh(st) {
      const grp = new THREE.Group();
      const zP = -4.36;
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

    function buildFloorSlabsAndBalconies(f) {
      const zF = f.zFloor;
      const sThick = 0.25;

      if (f.id === 'mar') {
        const marSlabPts = [
          [-11.15, -11.20], [6.60, -11.20], [6.60, 19.30], [-11.15, 19.30]
        ];
        addToFloorAndLayer('mar', 'site', buildPolygonSlab(marSlabPts, -4.68, -4.38, MATS.basementConcrete, MATS.basementConcrete));

        const stallsGrp = new THREE.Group();
        PARKING_STALLS.forEach(st => {
          stallsGrp.add(createParkingStallMesh(st));
        });
        addToFloorAndLayer('mar', 'site', stallsGrp);
        return;
      }

      if (f.id === 'kar') {
        const siteGrp = new THREE.Group();
        const asphaltMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.88, metalness: 0.05, clippingPlanes });
        const curbMat = new THREE.MeshStandardMaterial({ color: 0xcbd5e1, roughness: 0.65, metalness: 0.05, clippingPlanes });
        const markRedMat = new THREE.MeshBasicMaterial({ color: 0xef4444, transparent: true, opacity: 0.85, side: THREE.DoubleSide, clippingPlanes });

        // 1. Lot 57 base platform (-11.15..+6.60, -11.20..+19.30)
        siteGrp.add(makeBox(-11.15, -11.20, 6.60, 19.30, -0.06, -0.01, MATS.sidewalk));

        // 2. Private Garden of Garden Apartment #1 (153 sqm on South & West/East margins)
        siteGrp.add(makeBox(-11.00, 14.36, 6.45, 19.15, -0.01, 0.08, MATS.grass));
        siteGrp.add(makeBox(-11.00, 3.80, -8.14, 14.36, -0.01, 0.08, MATS.grass));
        siteGrp.add(makeBox(-7.56, 14.36, 0.80, 16.40, -0.01, 0.04, MATS.woodDeck));

        // 3. Front North Garden & Main Pedestrian Lobby Walkway from Yatkovski St
        siteGrp.add(makeBox(-8.00, -11.00, -1.80, -5.20, -0.01, 0.08, MATS.grass));
        siteGrp.add(makeBox(-1.80, -11.20, 2.20, -5.20, -0.01, 0.03, MATS.luxTravertine));
        siteGrp.add(makeBox(2.20, -11.00, 6.45, -5.20, -0.01, 0.08, MATS.grass));

        // 4. Vehicle Ramp along West boundary (X=-11.10..-8.15, Y=-11.20..+3.80)
        siteGrp.add(makeBox(-11.10, -11.20, -8.15, 3.80, -1.60, -0.01, MATS.basementConcrete));
        siteGrp.add(makeBox(-8.25, -9.50, -8.05, 3.80, 0.00, 1.10, MATS.extWall));

        // 5. Perimeter Stone Walls around Lot 57
        siteGrp.add(makeBox(-11.15, 19.10, 6.60, 19.30, 0.00, 1.15, MATS.extWall));
        siteGrp.add(makeBox(-11.15, -11.20, -10.95, 19.30, 0.00, 1.15, MATS.extWall));
        siteGrp.add(makeBox(6.40, -11.20, 6.60, 19.30, 0.00, 1.15, MATS.extWall));
        siteGrp.add(makeBox(-11.15, -11.22, 6.60, -11.15, 0.02, 0.03, markRedMat));
        siteGrp.add(makeBox(-11.15, 19.25, 6.60, 19.32, 0.02, 0.03, markRedMat));

        // 6. Yatkovski Brothers Street on the North (Y = -18.50 .. -11.20)
        siteGrp.add(makeBox(-22.00, -13.20, 18.00, -11.20, -0.16, -0.02, MATS.sidewalk));
        siteGrp.add(makeBox(-22.00, -13.35, 18.00, -13.20, -0.16, 0.01, curbMat));
        siteGrp.add(makeBox(-22.00, -18.50, 18.00, -13.35, -0.22, -0.10, asphaltMat));
        for (let rx = -18.0; rx <= 14.0; rx += 4.0) {
          siteGrp.add(makeBox(rx, -15.95, rx + 2.2, -15.80, -0.098, -0.092, MATS.extWall));
        }

        // 7. Enclosed Ground Floor Building Slab (Lobby + Garden Apt #1)
        const gSlabPts = [
          [-8.14, -5.20], [6.60, -5.20], [6.60, 3.80],
          [4.00, 3.80], [4.00, 14.36], [-8.14, 14.36]
        ];
        addToFloorAndLayer('kar', 'slabs', buildPolygonSlab(gSlabPts, -0.25, 0.00, MATS.slabFloor, MATS.slabEdge));
        addToFloorAndLayer('kar', 'site', siteGrp);
        return;
      }

      if (['f1', 'f2', 'f3', 'f4'].includes(f.id)) {
        const typPts = [
          [-8.14, -5.21], [6.95, -5.21], [6.95, 3.80],
          [4.00, 3.80], [4.00, 14.36], [-8.14, 14.36]
        ];
        addToFloorAndLayer(f.id, 'slabs', buildPolygonSlab(typPts, zF - sThick, zF, MATS.slabFloor, MATS.extWall));

        // North Sukkah Balcony (facing Yatkovski St: X=-3.80..+1.20, Y=-7.32..-5.21)
        buildBalconyBox(f.id, -3.80, -7.32, 1.20, -5.21, zF, ['N', 'W', 'E'], false, 1.05, false);
        // South Sukkah Balcony (facing Rear Garden: X=-7.56..+0.50, Y=14.36..15.77)
        buildBalconyBox(f.id, -7.56, 14.36, 0.50, 15.77, zF, ['S', 'W', 'E'], false, 1.05, false);
        return;
      }

      if (f.id === 'f5') {
        const f5Pts = [
          [-8.14, -2.65], [6.95, -2.65], [6.95, 3.80],
          [4.00, 3.80], [4.00, 12.16], [-8.14, 12.16]
        ];
        addToFloorAndLayer('f5', 'slabs', buildPolygonSlab(f5Pts, zF - sThick, zF, MATS.slabFloor, MATS.extWall));
        // North Roof Terrace + Pergola (X=-8.14..+6.95, Y=-5.21..-2.65)
        buildBalconyBox('f5', -8.14, -5.21, 6.95, -2.65, zF, ['N', 'W', 'E'], true, 1.10, true);
        // South Roof Terrace + Pergola (X=-8.14..+4.00, Y=12.16..15.77)
        buildBalconyBox('f5', -8.14, 12.16, 4.00, 15.77, zF, ['S', 'W', 'E'], true, 1.10, true);
        return;
      }

      if (f.id === 'f6') {
        const f6Pts = [
          [-8.14, -2.65], [6.95, -2.65], [6.95, 3.80],
          [4.00, 3.80], [4.00, 9.20], [-3.20, 9.20],
          [-3.20, 12.01], [-8.14, 12.01]
        ];
        addToFloorAndLayer('f6', 'slabs', buildPolygonSlab(f6Pts, zF - sThick, zF, MATS.slabFloor, MATS.extWall));
        // North Penthouse Balcony (X=-8.14..+2.50, Y=-4.25..-2.65)
        buildBalconyBox('f6', -8.14, -4.25, 2.50, -2.65, zF, ['N', 'W', 'E'], false, 1.10, true);
        // South-East & South-West Penthouse Roof Terraces + Pergola
        buildBalconyBox('f6', -3.20, 9.20, 4.00, 14.50, zF, ['S', 'E'], true, 1.10, true);
        buildBalconyBox('f6', -8.14, 12.01, -3.20, 14.50, zF, ['S', 'W'], false, 1.10, true);
        return;
      }

      if (f.id === 'gag') {
        const gagPts = [
          [-8.14, -2.65], [6.95, -2.65], [6.95, 3.80],
          [4.00, 3.80], [4.00, 9.20], [-8.14, 9.20]
        ];
        addToFloorAndLayer('gag', 'slabs', buildPolygonSlab(gagPts, 22.74, 22.99, MATS.terraceFloor, MATS.extWall));
        const pGrp = new THREE.Group();
        pGrp.add(makeBox(-8.14, -2.65, 6.95, -2.42, 22.99, 24.05, MATS.extWall));
        pGrp.add(makeBox(-8.14, 8.95, 4.00, 9.20, 22.99, 24.05, MATS.extWall));
        pGrp.add(makeBox(-8.14, -2.65, -7.90, 9.20, 22.99, 24.05, MATS.extWall));
        pGrp.add(makeBox(6.70, -2.65, 6.95, 3.80, 22.99, 24.05, MATS.extWall));
        pGrp.add(makeBox(-2.20, -1.20, 2.40, 5.40, 25.74, 25.99, MATS.extWall));
        addToFloorAndLayer('gag', 'walls', pGrp);

        const solarGrp = new THREE.Group();
        [[-6.8, -1.2], [-4.4, -1.2], [-6.8, 5.2], [-4.4, 5.2], [3.6, -1.2]].forEach(([sx, sy]) => {
          solarGrp.add(makeBox(sx, sy, sx + 1.8, sy + 2.1, 22.99, 23.75, MATS.solarPanel));
        });
        addToFloorAndLayer('gag', 'pergolas', solarGrp);
        return;
      }
    }

    const hlGeo = new THREE.BoxGeometry(2.60, 1.45, 4.90);
    const hlMat = new THREE.MeshBasicMaterial({ color: 0x10b981, transparent: true, opacity: 0.48 });
    parkingHighlightMesh = new THREE.Mesh(hlGeo, hlMat);
    parkingHighlightMesh.visible = false;
    scene.add(parkingHighlightMesh);

    // =========================================================================
    // 5B. EXACT 1:1 CAD-ALIGNED 3D LUXURY INTERIOR MODELING ENGINE (YATKOVSKI 7)
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

    function addCADSofa3Seat(grp, x0, y0, x1, y1, zF, backDir = 'S') {
      const w = x1 - x0;
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.02, zF + 0.11, MATS.luxOakSmooth));
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.11, zF + 0.41, MATS.luxBoucle));
      const cStep = Math.max(0.2, (w - 0.32) / 3.0);
      for (let i = 0; i < 3; i++) {
        const cx0 = x0 + 0.16 + i * cStep;
        grp.add(makeBox(cx0 + 0.01, y0 + 0.04, cx0 + cStep - 0.01, y1 - 0.04, zF + 0.41, zF + 0.46, MATS.luxBoucle));
      }
      const by0 = (backDir === 'S') ? (y1 - 0.18) : y0;
      const by1 = (backDir === 'S') ? y1 : (y0 + 0.18);
      grp.add(makeBox(x0, by0, x1, by1, zF + 0.41, zF + 0.78, MATS.luxBoucle));
      grp.add(makeBox(x0, y0, x0 + 0.16, y1, zF + 0.41, zF + 0.64, MATS.luxBoucle));
      grp.add(makeBox(x1 - 0.16, y0, x1, y1, zF + 0.41, zF + 0.64, MATS.luxBoucle));
    }

    function addCADArmchair(grp, x0, y0, x1, y1, zF, backDir = 'E') {
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.02, zF + 0.10, MATS.luxOakSmooth));
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.10, zF + 0.40, MATS.luxBoucle));
      const bx0 = (backDir === 'E') ? (x1 - 0.16) : x0;
      const bx1 = (backDir === 'E') ? x1 : (x0 + 0.16);
      grp.add(makeBox(bx0, y0, bx1, y1, zF + 0.40, zF + 0.74, MATS.luxBoucle));
      grp.add(makeBox(x0, y0, x1, y0 + 0.14, zF + 0.40, zF + 0.60, MATS.luxBoucle));
      grp.add(makeBox(x0, y1 - 0.14, x1, y1, zF + 0.40, zF + 0.60, MATS.luxBoucle));
    }

    function addCADCoffeeTables(grp, cx1, cy1, r1, cx2, cy2, r2, zF) {
      grp.add(makeCylinder(cx1, cy1, r1 * 0.55, r1 * 0.55, zF + 0.02, zF + 0.36, MATS.luxFlutedOak, 20));
      grp.add(makeCylinder(cx1, cy1, r1, r1, zF + 0.36, zF + 0.40, MATS.luxCalacatta, 24));
      grp.add(makeCylinder(cx2, cy2, r2 * 0.55, r2 * 0.55, zF + 0.02, zF + 0.43, MATS.luxBrass, 18));
      grp.add(makeCylinder(cx2, cy2, r2, r2, zF + 0.43, zF + 0.46, MATS.luxOakSmooth, 20));
      grp.add(makeCylinder(cx1, cy1, 0.07, 0.09, zF + 0.40, zF + 0.58, MATS.luxCeramic, 12));
      grp.add(makeCylinder(cx1, cy1, 0.15, 0.05, zF + 0.56, zF + 0.76, MATS.luxPlantOlive, 10));
    }

    function addCADDiningTable6(grp, x0, y0, x1, y1, zF, zC, orient = 'H') {
      const cx = 0.5 * (x0 + x1), cy = 0.5 * (y0 + y1);
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.72, zF + 0.77, MATS.luxCalacatta));
      grp.add(makeCylinder(cx - (x1 - x0) * 0.24, cy - (y1 - y0) * 0.24, 0.12, 0.16, zF + 0.02, zF + 0.72, MATS.luxFlutedOak, 16));
      grp.add(makeCylinder(cx + (x1 - x0) * 0.24, cy + (y1 - y0) * 0.24, 0.12, 0.16, zF + 0.02, zF + 0.72, MATS.luxFlutedOak, 16));
      const step = (x1 - x0) / 3.0;
      for (let i = 0; i < 3; i++) {
        const sx = x0 + (i + 0.5) * step;
        grp.add(makeBox(sx - 0.20, y0 - 0.36, sx + 0.20, y0 - 0.04, zF + 0.42, zF + 0.47, MATS.luxBoucle));
        grp.add(makeBox(sx - 0.20, y1 + 0.04, sx + 0.20, y1 + 0.36, zF + 0.42, zF + 0.47, MATS.luxBoucle));
      }
      grp.add(makeCylinder(cx, cy, 0.24, 0.24, zF + 1.76, zF + 1.84, MATS.luxBrass, 20));
      grp.add(makeCylinder(cx, cy, 0.18, 0.18, zF + 1.73, zF + 1.77, MATS.luxGlowWarm, 16));
    }

    function addCADMasterBed(grp, x0, y0, x1, y1, zF, headDir = 'E') {
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.06, zF + 0.28, MATS.luxOakSmooth));
      grp.add(makeBox(x0 + 0.05, y0 + 0.05, x1 - 0.05, y1 - 0.05, zF + 0.28, zF + 0.48, MATS.luxCeramic));
      if (headDir === 'E') {
        grp.add(makeBox(x1 - 0.12, y0 - 0.06, x1, y1 + 0.06, zF + 0.02, zF + 0.92, MATS.luxFlutedOak));
        grp.add(makeBox(x0 + 0.04, y0 + 0.04, x1 - 0.42, y1 - 0.04, zF + 0.29, zF + 0.50, MATS.luxTaupe));
      } else {
        grp.add(makeBox(x0, y0 - 0.06, x0 + 0.12, y1 + 0.06, zF + 0.02, zF + 0.92, MATS.luxFlutedOak));
        grp.add(makeBox(x0 + 0.42, y0 + 0.04, x1 - 0.04, y1 - 0.04, zF + 0.29, zF + 0.50, MATS.luxTaupe));
      }
    }

    function addCADSingleBed(grp, x0, y0, x1, y1, zF, headDir = 'N') {
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.05, zF + 0.26, MATS.luxOakSmooth));
      grp.add(makeBox(x0 + 0.04, y0 + 0.04, x1 - 0.04, y1 - 0.04, zF + 0.26, zF + 0.44, MATS.luxCeramic));
      if (headDir === 'N') {
        grp.add(makeBox(x0, y0, x1, y0 + 0.10, zF + 0.02, zF + 0.78, MATS.luxFlutedOak));
      } else {
        grp.add(makeBox(x0, y1 - 0.10, x1, y1, zF + 0.02, zF + 0.78, MATS.luxFlutedOak));
      }
    }

    function addCADWardrobe(grp, x0, y0, x1, y1, zF) {
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.02, zF + 2.20, MATS.luxCabinet));
      grp.add(makeBox(x0 + 0.02, y0 + 0.02, x1 - 0.02, y1 - 0.02, zF + 2.20, zF + 2.24, MATS.luxFlutedOak));
    }

    function buildPines48BalconyLounge(grp, bx, by, bw, bd, zF) {
      grp.add(makeBox(bx - 0.65, by - 0.35, bx + 0.65, by + 0.35, zF + 0.02, zF + 0.36, MATS.luxBoucle));
      grp.add(makeCylinder(bx, by + 0.65, 0.32, 0.26, zF + 0.02, zF + 0.36, MATS.luxCalacatta, 18));
      [-bw * 0.35, bw * 0.35].forEach(px => {
        grp.add(makeCylinder(bx + px, by, 0.22, 0.16, zF + 0.02, zF + 0.50, MATS.luxCeramic, 16));
        grp.add(makeCylinder(bx + px, by, 0.34, 0.20, zF + 0.50, zF + 1.35, MATS.luxPlantOlive, 14));
      });
    }

    function buildTypicalFloorExactCADFurniture(grp, zF, zC) {
      // --- 1. NORTH APARTMENT (4 ROOMS, 97 SQM FACING YATKOVSKI ST) ---
      grp.add(makeBox(-0.80, -4.40, 2.40, -1.90, zF + 0.015, zF + 0.028, MATS.luxRug, false));
      addCADSofa3Seat(grp, -0.50, -2.50, 2.10, -1.70, zF, 'S');
      addCADCoffeeTables(grp, 0.80, -3.20, 0.40, 0.35, -3.35, 0.26, zF);
      addCADDiningTable6(grp, -2.10, -2.20, -0.70, -1.35, zF, zC, 'H');
      // North Kitchen [-3.90..-2.30, -4.60..-2.50]
      grp.add(makeBox(-3.90, -4.60, -2.30, -3.95, zF + 0.02, zF + 0.88, MATS.luxCabinet));
      grp.add(makeBox(-3.92, -4.62, -2.28, -3.93, zF + 0.88, zF + 0.92, MATS.luxCalacatta));
      // North Master Suite (East) [4.10..6.70, -1.40..+1.80]
      addCADMasterBed(grp, 4.70, -0.70, 6.70, 1.00, zF, 'E');
      // North Bedroom 1 (NW) [-6.90..-4.50, -4.60..-1.80]
      addCADSingleBed(grp, -6.70, -4.50, -5.65, -2.60, zF, 'N');
      addCADWardrobe(grp, -6.70, -2.20, -5.10, -1.65, zF);
      // North Mamad [-5.60..-3.20, 2.10..3.70]
      addCADSingleBed(grp, -5.40, 2.20, -3.60, 3.15, zF, 'N');
      buildPines48BalconyLounge(grp, -1.30, -6.25, 3.6, 1.8, zF);

      // --- 2. SOUTH APARTMENT (4 ROOMS, 102 SQM REAR GARDEN VIEW) ---
      grp.add(makeBox(-6.90, 10.40, -3.80, 13.40, zF + 0.015, zF + 0.028, MATS.luxRug, false));
      addCADSofa3Seat(grp, -6.70, 10.50, -4.10, 11.35, zF, 'N');
      addCADCoffeeTables(grp, -5.40, 12.00, 0.42, -4.95, 12.15, 0.28, zF);
      addCADDiningTable6(grp, -3.30, 9.60, -1.70, 10.50, zF, zC, 'H');
      // South Kitchen [-7.20..-4.40, 5.50..7.60]
      grp.add(makeBox(-7.20, 5.50, -4.40, 6.15, zF + 0.02, zF + 0.88, MATS.luxCabinet));
      grp.add(makeBox(-7.22, 5.48, -4.38, 6.17, zF + 0.88, zF + 0.92, MATS.luxCalacatta));
      // South Master Suite (SE) [0.40..3.70, 11.10..14.00]
      addCADMasterBed(grp, 1.60, 11.50, 3.65, 13.20, zF, 'E');
      // South Bedroom 1 [-2.80..-0.40, 11.20..14.00]
      addCADSingleBed(grp, -2.40, 11.95, -1.35, 13.85, zF, 'S');
      // South Mamad [0.00..2.60, 5.20..7.40]
      addCADSingleBed(grp, 0.30, 5.40, 2.10, 6.35, zF, 'N');
      buildPines48BalconyLounge(grp, -3.60, 15.05, 4.8, 1.4, zF);
    }

    function buildFloor5MiniPenthouseFurniture(grp, zF, zC) {
      // Full-Floor Mini-Penthouse (#10, 150 sqm + 64 sqm terraces)
      grp.add(makeBox(-7.10, -2.10, -3.60, 1.10, zF + 0.015, zF + 0.028, MATS.luxRug, false));
      addCADSofa3Seat(grp, -6.90, -0.20, -4.10, 0.65, zF, 'S');
      addCADCoffeeTables(grp, -5.50, -1.10, 0.44, -5.00, -1.25, 0.28, zF);
      addCADDiningTable6(grp, -6.50, 2.20, -4.70, 3.15, zF, zC, 'H');
      // Chef Kitchen Island
      grp.add(makeBox(-6.60, 3.60, -4.30, 4.45, zF + 0.02, zF + 0.88, MATS.luxFlutedOak));
      grp.add(makeBox(-6.64, 3.56, -4.26, 4.49, zF + 0.88, zF + 0.93, MATS.luxCalacatta));
      // Master Suite East [4.20..6.70, -1.20..+2.10]
      addCADMasterBed(grp, 4.65, -0.40, 6.70, 1.30, zF, 'E');
      // Southern Bedrooms
      addCADSingleBed(grp, -7.20, 9.20, -5.20, 10.20, zF, 'W');
      addCADSingleBed(grp, -4.40, 10.10, -3.30, 11.95, zF, 'S');
      addCADSingleBed(grp, -1.00, 10.10, 0.10, 11.95, zF, 'S');
      buildPines48BalconyLounge(grp, -1.50, -3.95, 6.0, 2.2, zF);
      buildPines48BalconyLounge(grp, -2.20, 13.90, 5.5, 2.4, zF);
    }

    function buildFloor6PenthouseFurniture(grp, zF, zC) {
      // Full-Floor Luxury Penthouse (#11, 125 sqm + 52 sqm Roof Terraces + Jacuzzi & Outdoor BBQ)
      grp.add(makeBox(-7.10, -2.10, -3.60, 1.10, zF + 0.015, zF + 0.028, MATS.luxRug, false));
      addCADSofa3Seat(grp, -6.90, -0.20, -4.10, 0.65, zF, 'S');
      addCADCoffeeTables(grp, -5.50, -1.10, 0.44, -5.00, -1.25, 0.28, zF);
      addCADDiningTable6(grp, -6.50, 2.20, -4.70, 3.15, zF, zC, 'H');
      // Penthouse Kitchen & Waterfall Island
      grp.add(makeBox(-6.60, 3.60, -4.30, 4.45, zF + 0.02, zF + 0.88, MATS.luxFlutedOak));
      grp.add(makeBox(-6.64, 3.56, -4.26, 4.49, zF + 0.88, zF + 0.93, MATS.luxCalacatta));
      // Master Suite East [4.20..6.70, -1.10..+2.10]
      addCADMasterBed(grp, 4.65, -0.35, 6.70, 1.35, zF, 'E');
      // Southern Bedrooms
      addCADSingleBed(grp, -7.20, 6.90, -5.20, 7.90, zF, 'W');
      addCADSingleBed(grp, -7.20, 9.80, -5.20, 10.80, zF, 'W');

      // Penthouse South Roof Terrace (-3.20..+4.00, 9.20..14.50): Luxury Jacuzzi Spa + Outdoor BBQ + 8-Seat Table
      const jx0 = 1.40, jx1 = 3.50, jy0 = 11.80, jy1 = 13.90;
      grp.add(makeBox(jx0, jy0, jx1, jy1, zF + 0.02, zF + 0.78, MATS.luxFlutedOak));
      grp.add(makeBox(jx0 + 0.12, jy0 + 0.12, jx1 - 0.12, jy1 - 0.12, zF + 0.78, zF + 0.84, MATS.luxCeramic));
      grp.add(makeBox(jx0 + 0.22, jy0 + 0.22, jx1 - 0.22, jy1 - 0.22, zF + 0.70, zF + 0.82, MATS.waterSpa));

      // Outdoor BBQ Kitchen on South-East Roof Terrace
      grp.add(makeBox(0.80, 9.45, 3.60, 10.15, zF + 0.02, zF + 0.88, MATS.aluDark));
      grp.add(makeBox(0.78, 9.43, 3.62, 10.17, zF + 0.88, zF + 0.93, MATS.luxCalacatta));
      // Outdoor Dining Table on Terrace
      addCADDiningTable6(grp, -2.40, 11.20, -0.60, 12.15, zF, zC, 'H');
      buildPines48BalconyLounge(grp, -5.60, 13.20, 3.6, 2.0, zF);
    }

    function buildPines48StyleFloorInteriors(f, pData) {
      const fGrp = new THREE.Group();
      const zF = f.zFloor;
      const zC = f.zCeil;

      if (f.id === 'kar') {
        // 1. Main Entrance Lobby (X=-1.80..+3.60, Y=-5.00..+0.20)
        fGrp.add(makeBox(-1.80, -5.00, 3.60, 0.20, zF + 0.005, zF + 0.018, MATS.luxTravertine, false));
        fGrp.add(makeBox(0.40, -3.40, 2.60, -2.75, zF + 0.03, zF + 1.05, MATS.luxFlutedOak));
        fGrp.add(makeBox(0.36, -3.44, 2.64, -2.71, zF + 1.05, zF + 1.10, MATS.luxCalacatta));
        // 2. Garden Apartment #1 (South wing: Y=+4.20..+14.36)
        fGrp.add(makeBox(-6.90, 10.40, -3.80, 13.40, zF + 0.015, zF + 0.028, MATS.luxRug, false));
        addCADSofa3Seat(fGrp, -6.70, 10.50, -4.10, 11.35, zF, 'N');
        addCADCoffeeTables(fGrp, -5.40, 12.00, 0.42, -4.95, 12.15, 0.28, zF);
        addCADDiningTable6(fGrp, -3.30, 9.60, -1.70, 10.50, zF, zC, 'H');
        addCADMasterBed(fGrp, 1.60, 11.50, 3.65, 13.20, zF, 'E');
        buildPines48BalconyLounge(fGrp, -3.50, 15.60, 5.2, 2.2, zF);
        addToFloorAndLayer(f.id, 'furn3d', fGrp);
        return;
      }

      if (f.id === 'f5') {
        buildFloor5MiniPenthouseFurniture(fGrp, zF, zC);
      } else if (f.id === 'f6') {
        buildFloor6PenthouseFurniture(fGrp, zF, zC);
      } else {
        buildTypicalFloorExactCADFurniture(fGrp, zF, zC);
      }

      [[-4.5, -2.0], [1.5, -2.0], [-4.5, 10.5], [1.0, 10.5]].forEach(([lx, ly]) => {
        const pl = new THREE.PointLight(0xfff3d6, 0.36, 12.5, 1.6);
        pl.position.set(lx, zC - 0.25, ly);
        fGrp.add(pl);
      });

      addToFloorAndLayer(f.id, 'furn3d', fGrp);
    }

    function buildAllFloors() {
      FLOORS.forEach(f => {
        const pData = PLANS[f.sheet];
        if (!pData) return;

        buildFloorSlabsAndBalconies(f);

        pData.wall_polys.forEach(wp => {
          const z0 = f.zFloor;
          const z1 = f.zCeil;
          const wMesh = buildExtrudedTriPoly(wp, z0, z1, (f.id === 'mar') ? MATS.basementConcrete : MATS.wall, MATS.wallCap, f.sheet, (f.id === 'mar') ? null : MATS.extWall);
          addToFloorAndLayer(f.id, (f.id === 'mar') ? 'site' : 'walls', wMesh);
        });

        (pData.openings || []).forEach(op => {
          buildOpening3D(f, op);
        });

        if (f.has3DFurn) {
          buildPines48StyleFloorInteriors(f, pData);
        }

        const zLine = f.zFloor + 0.018;
        if (pData.cad_lines && pData.cad_lines.length > 0) {
          const cPts = [];
          pData.cad_lines.forEach(s => {
            cPts.push(s[0], zLine + 0.003, s[1], s[2], zLine + 0.003, s[3]);
          });
          const cGeo = new THREE.BufferGeometry();
          cGeo.setAttribute('position', new THREE.Float32BufferAttribute(cPts, 3));
          const cLines = new THREE.LineSegments(cGeo, MATS.lineCad);
          addToFloorAndLayer(f.id, 'cad2d', cLines);
        }

        (pData.room_labels || []).forEach(rl => {
          const lblMesh = createFloorLabelMesh(rl.name, rl.dims, rl.x, rl.y, f.zFloor);
          addToFloorAndLayer(f.id, 'labels', lblMesh);
        });
      });
    }

    buildAllFloors();
"""

HTML_PART2B = r"""
    // =========================================================================
    // 6. GEOREFERENCED TRIPLE-RESOLUTION GOOGLE MAPS HYBRID PLANES OF PETAH TIKVA
    //    + 8 CONCENTRIC DISTANCE RINGS + 28 VERIFIED POIS AROUND YATKOVSKI 7
    // =========================================================================
    // Exact ITM-Surveyed Center of Lot 57 (Gush 6385, Parcel 136, ITM E=188765, N=664953)
    const CENTER_LAT = 32.0774502;
    const CENTER_LON = 34.8793726;
    const R_MERC = 6378137.0;
    const LAT0_RAD = CENTER_LAT * Math.PI / 180.0;
    const LON0_RAD = CENTER_LON * Math.PI / 180.0;
    const COS_LAT0 = Math.cos(LAT0_RAD);
    const MERC_Y0  = Math.asinh(Math.tan(LAT0_RAD));

    const SCENE_CX = -1.5;
    const SCENE_CZ = 3.5;

    const GMAPS_THETA = -8.0 * Math.PI / 180.0;
    const GMAPS_CT = Math.cos(GMAPS_THETA), GMAPS_ST = Math.sin(GMAPS_THETA);

    function geoMetersTo3D(eastM, northM, y3d = -0.05) {
      const dx = eastM * GMAPS_CT - northM * GMAPS_ST;
      const dy = eastM * GMAPS_ST + northM * GMAPS_CT;
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
          <a href="yatkovski7_spatial_map.html" target="_blank" style="display:flex;align-items:center;justify-content:center;gap:4px;padding:7px 8px;border-radius:8px;background:#334155;color:#38bdf8;font-size:11px;font-weight:800;text-decoration:none;">
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
      { text: "יטקובסקי אחים 7 (7א) · 11 יח\"ד · רום גג +25.99 מ' (+82.99)", pos: new THREE.Vector3(-1.5, 26.8, 2.0), cls: "b44" },
      { text: "פנטהאוז קומה 6 (+19.76) · 125+52 מ\"ר מרפסות גג + ג'קוזי", pos: new THREE.Vector3(-1.5, 23.6, 12.0), cls: "ph" },
      { text: "רחוב האחים יטקובסקי 7 (מפלס כניסה 0.00 = +57.00 מ')", pos: new THREE.Vector3(0.0, 1.4, -14.5), cls: "street" },
      { text: "גוש 6385 חלקה 136 מגרש 57 (522 מ\"ר) · גינת דירת גן #1 (153 מ\"ר)", pos: new THREE.Vector3(-2.0, 1.4, 17.5), cls: "" }
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
    // 7. 11-UNIT 3D CATALOG & LIVE CRM, PDF QUOTE GENERATOR
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

      const geo = new THREE.BoxGeometry(w + 0.20, h, d + 0.20);
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
      if (activeUnitRoomFilter !== 'all' && String(u.rooms) !== activeUnitRoomFilter) return false;
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
              <div style="font-size:10px;color:#475569;font-weight:600;">${u.area} מ"ר + ${u.balcony} מ"ר חוץ · ${u.directions}</div>
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
        camState.spherical.radius = 38.0;
        camState.spherical.phi = 1.08;
        camState.spherical.theta = (u.lookDir === 'N') ? -1.45 : 1.65;
        updateCameraFromOrbit();
      }

      const badgeCls = u.status === 'available' ? 'status-available' : 'status-owner';
      const downPayment20 = Math.round(u.price * 0.20);
      const balance80 = u.price - downPayment20;
      const estMonthlyMortgage = Math.round((u.price * 0.55) * 0.0055);
      const pLevelTxt = 'מרתף חניון (-4.38)';

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
            <div style="font-size:10px;color:#94a3b8;">מרפסת / גינה</div>
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
            <span style="font-weight:800;color:#6ee7b7;">חניה #${u.parkingNum} (${pLevelTxt})</span>
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
        selectFloor(u.floorId === 'f0' ? 'kar' : u.floorId);
        const cx = 0.5 * (u.bbox[0] + u.bbox[2]);
        const cy = 0.5 * (u.bbox[1] + u.bbox[3]);
        startWalkthroughAt(cx, u.z0 + 1.68, cy, (u.lookDir === 'N') ? 0.0 : Math.PI, `${u.name} · ${u.typeHe}`, u.floorLabel);
      });
      document.getElementById('btn-card-balcony-view').addEventListener('click', () => {
        closeAllDrawers();
        selectFloor('all');
        const [bx, by] = u.balcPt;
        const yaw = (u.lookDir === 'N') ? 0.0 : Math.PI;
        startWalkthroughAt(bx, u.z0 + 1.68, by, yaw, `נוף מהמרפסת — ${u.name} (גובה +${u.z0.toFixed(2)} מ')`, u.floorLabel);
      });
      document.getElementById('btn-card-show-parking').addEventListener('click', () => {
        closeAllDrawers();
        if (camState.walkMode) exitWalkthrough();
        setSliceMode('single');
        const targetFlr = 'mar';
        const targetZ = -3.65;
        selectFloor(targetFlr);
        if (parkingHighlightMesh) {
          parkingHighlightMesh.visible = true;
          parkingHighlightMesh.position.set(u.parkingX, targetZ, u.parkingY);
        }
        camState.target.set(u.parkingX, targetZ - 0.4, u.parkingY);
        camState.spherical = { radius: 22.0, phi: 0.62, theta: -1.55 };
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
  <title>הצעת מחיר ומפרט טכני — ${u.name} · יטקובסקי אחים 7 פתח תקווה</title>
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
      <div class="logo">Y7</div>
      <div>
        <div style="font-size:20px;font-weight:900;color:#0f172a;">יצחק קולסקי חברה לבניה והשקעות בע"מ</div>
        <div style="font-size:13px;color:#475569;font-weight:700;">פרויקט בוטיק יטקובסקי אחים 7 (7א), פתח תקווה · אדריכלות: א.ב. דרגן אדריכלים</div>
      </div>
    </div>
    <div style="text-align:left;font-size:12px;color:#475569;">
      <div><b>תאריך הפקה:</b> ${todayStr}</div>
      <div><b>גוש 6385 חלקה 136 מגרש 57</b> · 11 יח"ד</div>
    </div>
  </div>
  <div class="grid">
    <div class="kpi"><div class="kpi-lbl">מספר דירה</div><div class="kpi-val">${u.name}</div></div>
    <div class="kpi"><div class="kpi-lbl">קומה ומפלס</div><div class="kpi-val">${u.floorLabel} (+${u.z0.toFixed(2)})</div></div>
    <div class="kpi"><div class="kpi-lbl">שטח דירה + חוץ</div><div class="kpi-val">${u.area} + ${u.balcony} מ"ר</div></div>
    <div class="kpi" style="background:#ecfdf5;border-color:#6ee7b7;"><div class="kpi-lbl" style="color:#065f46;">מחיר מחירון</div><div class="kpi-val" style="color:#047857;">${u.status === 'available' ? formatILS(u.price) : 'דירת בעלים'}</div></div>
  </div>
  <div class="two-col">
    <div class="box">
      <div style="font-size:14px;font-weight:900;color:#1e3a8a;margin-bottom:8px;">📋 מפרט טכני ותנאי עסקה — ${u.name}</div>
      <table>
        <tr><td><b>מספר חדרים וטיפוס:</b></td><td>${u.rooms} חדרים (${u.typeHe})</td></tr>
        <tr><td><b>כיווני אוויר מלאים:</b></td><td>${u.directions}</td></tr>
        <tr><td><b>חניה צמודה בטאבו:</b></td><td>חניה מקורה #${u.parkingNum} במרתף החניון</td></tr>
        <tr><td><b>מפרט פנים יוקרתי:</b></td><td>ריצוף גרניט פורצלן 100×100/80×80, מטבח יוקרה, תריסי אור חשמליים, מערכת מיזוג VRF</td></tr>
        <tr><td><b>תנאי תשלום יזמיים (20/80):</b></td><td>20% בחתימה (${formatILS(down20)}) · 80% במסירת חזקה (${formatILS(bal80)})</td></tr>
        <tr><td><b>נגישות ומוקדי סביבה:</b></td><td>מרחק הליכה מתיכון אחד העם, הקו האדום של הרכבת הקלה, הפארק הגדול ומרכז רפואי רבין</td></tr>
      </table>
    </div>
    <div class="box" style="display:flex;flex-direction:column;justify-content:space-between;">
      <div style="font-size:13px;font-weight:800;color:#0f172a;margin-bottom:6px;">📸 הדמיית המודל התלת-ממדי (1:50 CAD):</div>
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
      target: new THREE.Vector3(-1.5, 8.0, 3.5),
      spherical: { radius: 460.0, phi: 0.60, theta: -1.45 },
      isDragging: false,
      isPanning: false,
      downX: 0, downY: 0, prevX: 0, prevY: 0,
      walkMode: false, yaw: 0, pitch: 0, keys: {}
    };

    const VIEW_PRESETS = {
      iso_north:      { theta: -1.42, phi: 1.08, radius: 46.0,   target: [-1.5, 11.5, 3.5], ortho: false, clip: 26.5 },
      iso_south:      { theta: 1.68,  phi: 1.08, radius: 46.0,   target: [-1.5, 11.5, 3.5], ortho: false, clip: 26.5 },
      gmaps_regional: { theta: -1.42, phi: 0.56, radius: 1320.0, target: [-1.5, 6.0, 3.5],  ortho: false, clip: 26.5 },
      gmaps_aerial:   { theta: -1.42, phi: 0.60, radius: 460.0,  target: [-1.5, 6.0, 3.5],  ortho: false, clip: 26.5 },
      gmaps_close:    { theta: -1.42, phi: 0.66, radius: 135.0,  target: [-1.5, 8.0, 3.5],  ortho: false, clip: 26.5 },
      top_plan:       { theta: -Math.PI/2, phi: 0.04, radius: 38.0, target: [-1.5, 13.3, 3.5], ortho: true, clip: 15.8 }
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
      orthoCam.zoom = 38.0 / radius;
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
      const fObj = FLOORS.find(f => f.id === floorId) || FLOORS[5];
      setSliceMode('single');
      selectFloor(fObj.id);
      setClipHeight(26.5);
      setOrthoMode(false);
      camState.target.set(-1.5, fObj.zFloor + 1.0, 3.5);
      camState.spherical.radius = 32.0;
      camState.spherical.phi = 0.56;
      camState.spherical.theta = -1.35;
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
      selectFloor(u.floorId === 'f0' ? 'kar' : u.floorId);
      const cx = 0.5 * (u.bbox[0] + u.bbox[2]);
      const cy = 0.5 * (u.bbox[1] + u.bbox[3]);
      startWalkthroughAt(cx, u.z0 + 1.68, cy, (u.lookDir === 'N') ? 0.0 : Math.PI, `${u.name} · ${u.typeHe} (${u.area}+${u.balcony} מ"ר)`, u.floorLabel);
    }

    function teleportInTour(x, z, yawRad, labelTxt, forceFloorId = null) {
      const activeF = forceFloorId
        ? (FLOORS.find(f => f.id === forceFloorId) || FLOORS[5])
        : (FLOORS.find(f => f.id === currentFloorId && f.zFloor >= 0) || FLOORS[5]);
      if (!camState.walkMode || forceFloorId) {
        setSliceMode('single');
        selectFloor(activeF.id);
      }
      startWalkthroughAt(x, activeF.zFloor + 1.68, z, yawRad, labelTxt, activeF.label);
    }

    function flyToBalconyFloorView(flrNum) {
      closeAllDrawers();
      selectFloor('all');
      const fObj = FLOORS.find(f => f.id === 'f' + flrNum) || FLOORS[5];
      document.querySelectorAll('#balcony-floor-selector [data-bflr]').forEach(b => {
        b.className = (parseInt(b.dataset.bflr, 10) === flrNum) ? 'ui-btn active' : 'ui-btn';
      });
      const tourSel = document.getElementById('tour-floor-select');
      if (tourSel) tourSel.value = String(flrNum);
      const bx = -1.2;
      const by = (flrNum === 6) ? -3.6 : ((flrNum === 5) ? -4.4 : -6.2);
      startWalkthroughAt(bx, fObj.zFloor + 1.68, by, 0.0, `🔭 נוף פנורמי מהמרפסת לרחוב האחים יטקובסקי — קומה ${flrNum} (+${fObj.zFloor.toFixed(2)} מ')`, fObj.label);
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
        camState.target.set(-1.5, activeF ? activeF.zFloor + 1.2 : 11.5, 3.5);
      }
      camState.target.y = Math.max(-8.0, Math.min(85.0, camState.target.y));
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
      if (units3DVisible && camState.spherical.radius > 160) activatePreset('iso_north');
      syncUnits3DToggleUI();
    });
    document.getElementById('btn-drawer-units-3d').addEventListener('click', () => {
      units3DVisible = !units3DVisible;
      if (units3DVisible && camState.spherical.radius > 160) activatePreset('iso_north');
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
      gisMapPlanesGroup.visible = gmapsVisible && (currentFloorId !== 'mar');
      this.textContent = gmapsVisible
        ? '🗺️ מפת לוויין Google Maps (יטקובסקי 7): פעיל'
        : '🗺️ מפת לוויין Google Maps (יטקובסקי 7): כבוי';
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
      dirLight.position.set(55 * Math.cos(rad), 65 * Math.sin(rad) + 15, 42 * Math.sin(rad * 1.2));
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
      clipVal.textContent = v >= 26.0 ? "+26.50 מ' (מלא)" : `${v >= 0 ? '+' : ''}${v.toFixed(2)} מ' (חתך)`;
      gisMapPlanesGroup.visible = gmapsVisible && (v > 0.0) && (currentFloorId !== 'mar');
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

      if (parkingHighlightMesh && floorId !== 'mar') parkingHighlightMesh.visible = false;
      gisMapPlanesGroup.visible = gmapsVisible && (floorId !== 'mar');

      if (floorId === 'all') {
        document.getElementById('active-floor-label').textContent = 'מבנה שלם (כל הקומות)';
        FLOORS.forEach(f => { floorGroups[f.id].visible = true; });
        setClipHeight(26.5);
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
      allBtn.innerHTML = '🏢 מבנה שלם (כל הקומות)';
      allBtn.onclick = () => selectFloor('all');
      fContainer.appendChild(allBtn);

      FLOORS.slice().reverse().forEach(f => {
        const b = document.createElement('button');
        b.className = 'ui-btn';
        b.style.justifyContent = 'space-between';
        b.style.fontSize = '11px';
        b.id = 'fbtn-' + f.id;
        b.innerHTML = `<span>${f.label}</span><span style="font-size:9.5px;opacity:0.75;font-family:monospace">${f.elevText}</span>`;
        b.onclick = () => {
          selectFloor(f.id);
          if (camState.spherical.radius > 120) {
            camState.target.set(-1.5, Math.max(-3, f.zFloor), 3.5);
            camState.spherical.radius = 40.0;
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
        if (currentFloorId === 'all') { setSliceMode('single'); selectFloor('f4'); }
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
      let objLines = ['# Yatkovski 7 Petah Tikva - 1:1 Metric Architectural BIM Model (Meters)'];
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
      a.download = 'yatkovski7_model.obj';
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
        camState.target.y = Math.max(-8.0, Math.min(85.0, camState.target.y));
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
          camState.target.y = Math.max(-8.0, Math.min(85.0, camState.target.y));
          updateCameraFromOrbit();
        }
      }

      renderer.render(scene, activeCam);
      const w = window.innerWidth, h = window.innerHeight;

      calloutObjs.forEach(c => {
        if (camState.walkMode || !showLabels || c.pos.y > clipPlane.constant) { c.el.style.opacity = '0'; return; }
        const p = c.pos.clone().project(activeCam);
        if (p.z > 1 || p.z < -1) { c.el.style.opacity = '0'; return; }
        const sx = (p.x * 0.5 + 0.5) * w, sy = (-p.y * 0.5 + 0.5) * h;
        c.el.style.left = `${sx}px`; c.el.style.top = `${sy}px`; c.el.style.opacity = '1';
      });

      gisRingLabelObjs.forEach(rl => {
        if (camState.walkMode || !gisRadiiVisible || currentFloorId === 'mar') { rl.el.style.display = 'none'; return; }
        const p = rl.pos.clone().project(activeCam);
        if (p.z > 1 || p.z < -1) { rl.el.style.display = 'none'; return; }
        const sx = (p.x * 0.5 + 0.5) * w, sy = (-p.y * 0.5 + 0.5) * h;
        if (sx < -60 || sx > w + 60 || sy < 50 || sy > h + 30) { rl.el.style.display = 'none'; return; }
        rl.el.style.display = 'block'; rl.el.style.left = `${sx}px`; rl.el.style.top = `${sy}px`;
      });

      gisPoiLabelObjs.forEach(pl => {
        const catMatch = (activeGisCategory === 'all' || pl.poi.cat === activeGisCategory);
        if (camState.walkMode || !gisPoisVisible || !catMatch || currentFloorId === 'mar') { pl.el.style.display = 'none'; return; }
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
    os.path.join(ARTIFACT_DIR, "yatkovski7_3d_bim_viewer.html"),
    os.path.join(ARTIFACT_DIR, "yatkovski7_3d_model.html"),
    os.path.join(PROJECT_DIR, "yatkovski7_3d_bim_viewer.html"),
    os.path.join(PROJECT_DIR, "yatkovski7_3d_model.html"),
    os.path.join(PROJECT_DIR, "index.html"),
]

for p in targets:
    with open(p, "w", encoding="utf-8") as f:
        f.write(html_out)
    print("Wrote:", p, "Size:", os.path.getsize(p))
