import os, json

WORKSPACE = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\הרב קיטרוני 37-39 פתח תקווה"
ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\7493e840-6f07-4fdb-9508-8c38dfc14844"
SCRATCH_DIR = os.path.join(ARTIFACT_DIR, "scratch")
THREE_JS_PATH = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\_shared_engine\three.min.js"

with open(THREE_JS_PATH, "r", encoding="utf-8") as f:
    three_js_code = f.read()

with open(os.path.join(SCRATCH_DIR, "kitroni_extracted_plans.json"), "r", encoding="utf-8") as f:
    plans_data = json.load(f)

if not plans_data.get('k5_7', {}).get('furn_lines') and plans_data.get('k1', {}).get('furn_lines'):
    plans_data['k5_7']['furn_lines'] = plans_data['k1']['furn_lines']

with open(os.path.join(SCRATCH_DIR, "kitroni_units_crm.json"), "r", encoding="utf-8") as f:
    crm_data = json.load(f)

with open(os.path.join(SCRATCH_DIR, "unified_kitroni_3d_map.json"), "r", encoding="utf-8") as f:
    unified_map_data = json.load(f)

with open(os.path.join(SCRATCH_DIR, "kitroni_spatial_map_data.json"), "r", encoding="utf-8") as f:
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

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>קיטרוני 37–39, פתח תקוה — מערכת שיווק, מכירות והדמיה תלת-ממדית אינטראקטיבית (1:50 CAD & GIS)</title>
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
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      user-select: none;
      background-color: #ffffff;
      color: #0f172a;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    #viewport-container {
      position: relative;
      width: 100%;
      height: 100vh;
      overflow: hidden;
      background: #ffffff;
    }
    canvas {
      display: block;
      width: 100%;
      height: 100%;
      cursor: grab;
    }
    canvas:active {
      cursor: grabbing;
    }
    .glass-panel {
      background: rgba(255, 255, 255, 0.94);
      border: 1px solid rgba(203, 213, 225, 0.85);
      color: #0f172a;
      box-shadow: 0 12px 32px -6px rgba(15, 23, 42, 0.14), 0 4px 12px -2px rgba(15, 23, 42, 0.08);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
    }
    .top-header {
      position: absolute;
      top: 12px;
      right: 14px;
      left: 14px;
      z-index: 30;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      border-radius: 14px;
      padding: 8px 16px;
    }
    .dropdown-drawer {
      display: none;
      position: absolute;
      top: 68px;
      right: 14px;
      z-index: 28;
      width: 390px;
      max-height: calc(100vh - 90px);
      overflow-y: auto;
      border-radius: 14px;
      padding: 14px;
      animation: fadeSlideDown 0.18s ease-out;
    }
    .dropdown-drawer.open {
      display: block;
    }
    @keyframes fadeSlideDown {
      from { opacity: 0; transform: translateY(-6px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    .bottom-right-sections {
      position: absolute;
      bottom: 14px;
      right: 14px;
      z-index: 26;
      width: 340px;
      max-height: calc(100vh - 90px);
      overflow-y: auto;
      border-radius: 16px;
      padding: 12px 14px;
      border: 1px solid rgba(147, 197, 253, 0.9);
      background: rgba(255, 255, 255, 0.95);
      box-shadow: 0 16px 36px -6px rgba(15, 23, 42, 0.18), 0 4px 12px rgba(37, 99, 235, 0.10);
      backdrop-filter: blur(14px);
      transition: all 0.2s ease;
    }
    .bottom-right-sections.collapsed .sections-body {
      display: none;
    }
    .menu-trigger-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border-radius: 10px;
      border: 1px solid #cbd5e1;
      background: #ffffff;
      color: #0f172a;
      padding: 7px 12px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s ease;
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
    }
    .menu-trigger-btn:hover {
      background: #f1f5f9;
      border-color: #94a3b8;
    }
    .menu-trigger-btn.open {
      background: #1e3a8a;
      border-color: #1d4ed8;
      color: #ffffff;
      box-shadow: 0 0 0 2px #93c5fd;
    }
    .menu-trigger-btn.lux-trigger {
      background: linear-gradient(135deg, #b45309 0%, #d97706 100%);
      border-color: #92400e;
      color: #ffffff;
    }
    .menu-trigger-btn.lux-trigger:hover {
      background: linear-gradient(135deg, #92400e 0%, #b45309 100%);
    }
    .menu-trigger-btn.lux-trigger.open {
      box-shadow: 0 0 0 2px #fde68a, 0 4px 12px rgba(180, 83, 9, 0.35);
    }
    .menu-trigger-btn.emerald-trigger {
      background: linear-gradient(135deg, #047857 0%, #059669 100%);
      border-color: #065f46;
      color: #ffffff;
    }
    .menu-trigger-btn.emerald-trigger:hover {
      background: linear-gradient(135deg, #065f46 0%, #047857 100%);
    }
    .menu-trigger-btn.emerald-trigger.open {
      box-shadow: 0 0 0 2px #6ee7b7, 0 4px 12px rgba(5, 150, 105, 0.35);
    }
    .ui-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border-radius: 8px;
      border: 1px solid #cbd5e1;
      background: #f8fafc;
      color: #0f172a;
      padding: 6px 10px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .ui-btn:hover {
      background: #e2e8f0;
      border-color: #94a3b8;
    }
    .ui-btn.active {
      background: #2563eb;
      border-color: #1d4ed8;
      color: #ffffff;
    }
    .ui-btn-lux {
      background: linear-gradient(135deg, #b45309 0%, #d97706 100%);
      border-color: #92400e;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(180, 83, 9, 0.25);
    }
    .ui-btn-lux:hover {
      background: linear-gradient(135deg, #92400e 0%, #b45309 100%);
      border-color: #78350f;
      color: #ffffff;
    }
    .ui-btn-lux.active {
      background: linear-gradient(135deg, #78350f 0%, #b45309 100%);
      border-color: #451a03;
      color: #ffffff;
      box-shadow: 0 0 0 2px #fde68a, 0 4px 12px rgba(180, 83, 9, 0.35);
    }
    .aptc-hud {
      position: absolute;
      bottom: 14px;
      left: 14px;
      right: 368px;
      z-index: 25;
      display: none;
      flex-direction: column;
      gap: 8px;
      border-radius: 14px;
      padding: 10px 14px;
      background: rgba(255, 252, 245, 0.95);
      border: 1px solid #e6d5be;
      box-shadow: 0 12px 30px -6px rgba(15, 23, 42, 0.16);
      backdrop-filter: blur(14px);
    }
    .room-chip {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      border-radius: 8px;
      border: 1px solid #dec9ad;
      background: #ffffff;
      color: #451a03;
      padding: 5px 10px;
      font-size: 11.5px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .room-chip:hover {
      background: #fef3c7;
      border-color: #d97706;
    }
    .room-chip.active {
      background: #b45309;
      border-color: #78350f;
      color: #ffffff;
    }
    .walk-dpad-btn {
      width: 32px;
      height: 30px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border-radius: 7px;
      border: 1px solid #d6c7b2;
      background: #ffffff;
      color: #1e293b;
      font-size: 13px;
      font-weight: 800;
      cursor: pointer;
      user-select: none;
    }
    .walk-dpad-btn:hover {
      background: #fef3c7;
      border-color: #d97706;
    }
    .walk-dpad-btn:active {
      background: #b45309;
      color: #ffffff;
    }
    .section-box {
      border-radius: 10px;
      border: 1px solid #e2e8f0;
      background: #f8fafc;
      padding: 10px;
      margin-bottom: 8px;
    }
    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
    }
    .flex-between {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .layer-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-radius: 8px;
      border: 1px solid #e2e8f0;
      background: #ffffff;
      padding: 5px 10px;
      font-size: 12px;
      color: #0f172a;
      margin-bottom: 4px;
      cursor: pointer;
    }
    .callout-pill {
      position: absolute;
      transform: translate(-50%, -50%);
      white-space: nowrap;
      border-radius: 6px;
      border: 1px solid #cbd5e1;
      background: rgba(255, 255, 255, 0.94);
      color: #0f172a;
      padding: 3px 8px;
      font-size: 11px;
      font-weight: 700;
      box-shadow: 0 2px 6px rgba(15, 23, 42, 0.14);
      pointer-events: none;
      transition: opacity 0.15s ease;
    }
    .callout-pill.b37 { background: #1e3a8a; color: #ffffff; border-color: #1d4ed8; }
    .callout-pill.b39 { background: #047857; color: #ffffff; border-color: #059669; }
    .callout-pill.street { background: #0f172a; color: #fde047; border-color: #334155; }
    .cad-badge {
      font-variant-numeric: tabular-nums;
    }
    input[type="range"] {
      width: 100%;
      cursor: pointer;
      accent-color: #2563eb;
    }
    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 2px 7px;
      border-radius: 999px;
      font-size: 10px;
      font-weight: 800;
      white-space: nowrap;
    }
    .status-available { background: #dcfce7; color: #166534; border: 1px solid #86efac; }
    .status-owner     { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }
    .unit-sales-card {
      display: none;
      position: absolute;
      top: 72px;
      left: 16px;
      z-index: 29;
      width: 380px;
      max-height: calc(100vh - 96px);
      overflow-y: auto;
      background: rgba(15, 23, 42, 0.96);
      color: #ffffff;
      border: 1px solid #334155;
      border-radius: 16px;
      padding: 14px;
      box-shadow: 0 20px 44px rgba(0, 0, 0, 0.45);
      backdrop-filter: blur(14px);
    }
    .pkg-card-btn {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 3px;
      border-radius: 8px;
      border: 1px solid #cbd5e1;
      background: #ffffff;
      padding: 6px 8px;
      cursor: pointer;
      text-align: right;
      transition: all 0.15s ease;
    }
    .pkg-card-btn:hover {
      background: #f8fafc;
      border-color: #64748b;
    }
    .pkg-card-btn.active {
      background: #eff6ff;
      border-color: #2563eb;
      box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.25);
    }
    .mode-switch {
      display: flex;
      background: #f1f5f9;
      padding: 3px;
      border-radius: 8px;
      gap: 4px;
      margin-bottom: 8px;
    }
    .mode-switch button {
      flex: 1;
      border: none;
      background: transparent;
      padding: 5px 6px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      color: #475569;
      cursor: pointer;
    }
    .mode-switch button.active {
      background: #ffffff;
      color: #2563eb;
      box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
  </style>
</head>
<body class="antialiased">
  <div id="viewport-container">
    <!-- 3D WebGL Canvas -->
    <canvas id="cad-canvas"></canvas>

    <!-- 2D Floating HTML Overlay Labels for Datum Elevations & Streets -->
    <div id="labels-container" style="pointer-events:none;position:absolute;inset:0;overflow:hidden;z-index:6;"></div>
    <!-- 3D Georeferenced Distance Rings & 28 POI Location Badges Overlay -->
    <div id="gis-labels-container" style="pointer-events:none;position:absolute;inset:0;overflow:hidden;z-index:8;"></div>
    <!-- 3D Interactive 63-Unit Badges & Laser Measure Overlay -->
    <div id="units-labels-container" style="pointer-events:none;position:absolute;inset:0;overflow:hidden;z-index:12;"></div>
    <div id="measure-labels-container" style="pointer-events:none;position:absolute;inset:0;overflow:hidden;z-index:18;"></div>

    <!-- Active Selected GIS Location Info Card -->
    <div id="gis-active-card" style="display:none;position:absolute;bottom:20px;left:20px;z-index:28;width:330px;background:rgba(15,23,42,0.96);color:#ffffff;border:1px solid #334155;border-radius:14px;padding:14px;box-shadow:0 12px 28px rgba(0,0,0,0.35);backdrop-filter:blur(10px);"></div>

    <!-- Floating Interactive Unit Sales & Financing Card (#unit-sales-card) -->
    <div id="unit-sales-card" class="unit-sales-card"></div>

    <!-- Floating 3D Laser Tape Measure Banner (Hidden unless measure mode is active) -->
    <div id="measure-hud" style="display:none;position:absolute;top:72px;left:50%;transform:translateX(-50%);z-index:27;background:rgba(15,23,42,0.94);color:#ffffff;border:1px solid #38bdf8;border-radius:999px;padding:6px 16px;font-size:12px;font-weight:700;box-shadow:0 8px 24px rgba(0,0,0,0.35);align-items:center;gap:10px;">
      <span>📏 <b>מד טווח לייזר 3D פעיל</b>: לחץ על 2 נקודות במודל למדידת מרחק מדויק</span>
      <span id="measure-last-val" style="background:#0284c7;color:#ffffff;padding:2px 8px;border-radius:999px;font-weight:800;">מוכן למדידה</span>
      <button id="btn-clear-measures" class="ui-btn" style="padding:2px 8px;font-size:11px;background:#334155;color:#ffffff;border-color:#475569;">נקה מדידות</button>
      <button id="btn-close-measure" class="ui-btn" style="padding:2px 7px;font-size:11px;background:#ef4444;color:#ffffff;border-color:#dc2626;">✕</button>
    </div>

    <!-- Clean Marketing Top Header Bar: Brand Identity + On-Demand Popover Menu Triggers -->
    <header class="glass-panel top-header">
      <div style="display:flex;align-items:center;gap:10px;">
        <div style="display:flex;height:36px;width:44px;align-items:center;justify-content:center;border-radius:9px;background:linear-gradient(135deg,#0f172a,#1e3a8a);color:#fde047;font-weight:900;font-size:11.5px;border:1px solid #3b82f6;">
          K37-39
        </div>
        <div>
          <div style="display:flex;align-items:center;gap:7px;flex-wrap:wrap;">
            <h1 style="margin:0;font-size:14px;font-weight:800;color:#0f172a;">קבוצת קולסקי · קיטרוני 37–39, פתח תקווה</h1>
            <span style="border-radius:6px;border:1px solid #dec9ad;background:#fef3c7;padding:1px 7px;font-size:10px;font-weight:800;color:#92400e;">אילת קורן אדריכלים · פורטל שיווק ומכירות 3D (63 דירות)</span>
          </div>
        </div>
      </div>

      <!-- Streamlined Marketing Action Bar & On-Demand Dropdown Triggers (All menus closed by default) -->
      <div style="display:flex;flex-wrap:wrap;align-items:center;gap:5px;" id="view-buttons">
        <button data-view="iso_west" id="btn-top-bldg" class="view-btn ui-btn" title="מבט חוץ אדריכלי מלא על שני הבניינים (37 ו-39)">
          🏢 מבט הבניין
        </button>
        <button data-view="gmaps_regional" id="btn-top-gis-map" class="view-btn ui-btn active" title="מבט רחפן על הבניין יושב על מפת העיר פתח תקווה ו-28 מוקדי הסביבה">
          🗺️ מפת סביבה
        </button>

        <button id="btn-top-units-3d" class="ui-btn" style="border-color:#10b981;color:#065f46;background:#ecfdf5;font-weight:800;" title="הצג/הסתר סימון 63 דירות תלת-ממדי לפי זמינות ומחיר על חזיתות הבניינים">
          🏢 סימון דירות 3D
        </button>
        <button id="btn-top-radii" class="ui-btn active" title="הדלק/כבה 8 מעגלי מרחק וזמני הליכה סביב המתחם">
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

        <!-- 4 On-Demand Popover Triggers (Closed by default, open on click) -->
        <button data-drawer="drawer-units" class="menu-trigger-btn emerald-trigger">
          <span>🏷️ קטלוג דירות ומחירים (63)</span>
          <span style="font-size:10px;">▾</span>
        </button>
        <button data-drawer="drawer-apartments" class="menu-trigger-btn lux-trigger">
          <span>✨ סיור בדירות ונוף מהמרפסת (ק' 4–5 מרוהטות 3D)</span>
          <span style="font-size:10px;">▾</span>
        </button>
        <button data-drawer="drawer-gis" class="menu-trigger-btn">
          <span>📍 מוקדי סביבה (46)</span>
          <span style="font-size:10px;">▾</span>
        </button>
        <button data-drawer="drawer-settings" class="menu-trigger-btn">
          <span>⚙️ עיצוב ושכבות</span>
          <span style="font-size:10px;">▾</span>
        </button>
      </div>
    </header>

    <!-- ===================================================================== -->
    <!-- ON-DEMAND POPOVER DRAWER 0: 63 UNITS CATALOG & LIVE CRM (CLOSED BY DEFAULT) -->
    <!-- ===================================================================== -->
    <div id="drawer-units" class="glass-panel dropdown-drawer" style="width:425px;">
      <div class="flex-between" style="margin-bottom:8px;border-bottom:1px solid #e2e8f0;padding-bottom:6px;">
        <div>
          <div style="font-size:13px;font-weight:800;color:#065f46;">🏷️ קטלוג 63 הדירות והמחירון הרשמי — קיטרוני 37–39</div>
          <div style="font-size:11px;color:#64748b;">נתוני אמת ממחירון השיווק ונספח התמורות · לחץ על דירה לכרטיס מכירה ו-PDF</div>
        </div>
        <button data-close-drawer class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
      </div>

      <!-- Inventory KPI Summary -->
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin-bottom:8px;text-align:center;">
        <div style="background:#ecfdf5;border:1px solid #a7f3d0;border-radius:8px;padding:5px;">
          <div style="font-size:10px;color:#065f46;font-weight:700;">🟢 מלאי קולסקי זמין</div>
          <div id="kpi-avail-count" style="font-size:14px;font-weight:900;color:#047857;">41 דירות</div>
        </div>
        <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:5px;">
          <div style="font-size:10px;color:#1e40af;font-weight:700;">🏢 בניין 37 / בניין 39</div>
          <div style="font-size:14px;font-weight:900;color:#1d4ed8;">30 / 33 דירות</div>
        </div>
        <div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:8px;padding:5px;">
          <div style="font-size:10px;color:#475569;font-weight:700;">🔒 דירות בעלים</div>
          <div id="kpi-owner-count" style="font-size:14px;font-weight:900;color:#334155;">22 דירות</div>
        </div>
      </div>

      <!-- 3D Volume Highlight & Price Visibility Controls -->
      <div class="grid-2" style="margin-bottom:8px;">
        <button id="btn-drawer-units-3d" class="ui-btn" style="background:#059669;color:#ffffff;border-color:#047857;font-weight:800;">
          🏢 הדגש דירות 3D על הבניינים
        </button>
        <button id="btn-toggle-prices" class="ui-btn active" style="font-weight:700;">
          👁️ מחירים: מוצג
        </button>
      </div>

      <!-- Smart Buyer Filters (Building, Availability & Rooms) -->
      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:6px;" id="unit-bldg-filters">
        <button data-ubldg="all" class="unit-bldg-chip ui-btn active" style="padding:3px 8px;font-size:10px;">שני הבניינים (63)</button>
        <button data-ubldg="37" class="unit-bldg-chip ui-btn" style="padding:3px 8px;font-size:10px;">בניין 37 — צפוני (30)</button>
        <button data-ubldg="39" class="unit-bldg-chip ui-btn" style="padding:3px 8px;font-size:10px;">בניין 39 — דרומי (33)</button>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:6px;" id="unit-status-filters">
        <button data-ustatus="all" class="unit-status-chip ui-btn active" style="padding:3px 8px;font-size:10px;">כל הסטטוסים (63)</button>
        <button data-ustatus="available" class="unit-status-chip ui-btn" style="padding:3px 8px;font-size:10px;">🟢 פנויות לשיווק קולסקי (41)</button>
        <button data-ustatus="owner" class="unit-status-chip ui-btn" style="padding:3px 8px;font-size:10px;">🔒 דירות בעלים (22)</button>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px;" id="unit-room-filters">
        <button data-urooms="all" class="unit-room-chip ui-btn active" style="padding:3px 8px;font-size:10px;">כל הגדלים</button>
        <button data-urooms="3" class="unit-room-chip ui-btn" style="padding:3px 8px;font-size:10px;">3 חד' (76–80 מ"ר)</button>
        <button data-urooms="4" class="unit-room-chip ui-btn" style="padding:3px 8px;font-size:10px;">4 חד' (100–103 מ"ר)</button>
        <button data-urooms="5" class="unit-room-chip ui-btn" style="padding:3px 8px;font-size:10px;">5 חד' (114–138 מ"ר)</button>
        <button data-urooms="6" class="unit-room-chip ui-btn" style="padding:3px 8px;font-size:10px;">6 חד' / פנטהאוז</button>
      </div>

      <div id="units-catalog-list" style="max-height:280px;overflow-y:auto;display:flex;flex-direction:column;gap:5px;padding-left:2px;"></div>
    </div>

    <!-- ===================================================================== -->
    <!-- ON-DEMAND POPOVER DRAWER 1: APARTMENT TOURS & BALCONY VIEW SIMULATOR -->
    <!-- ===================================================================== -->
    <div id="drawer-apartments" class="glass-panel dropdown-drawer" style="width:415px;">
      <div class="flex-between" style="margin-bottom:10px;border-bottom:1px solid #e2e8f0;padding-bottom:8px;">
        <div>
          <div style="font-size:13px;font-weight:800;color:#78350f;">✨ סיור פנים מרוהט 3D (קומות 4 ו-5) ונוף מהמרפסת</div>
          <div style="font-size:11px;color:#64748b;">מידול פנים תלת-ממדי מלא במפרט פינס 48 בקומות 4 ו-5 + סיור בגוף ראשון</div>
        </div>
        <button data-close-drawer class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
      </div>

      <div style="font-size:11px;font-weight:800;color:#92400e;margin-bottom:5px;">🛋️ מבט-על חתך Dollhouse לקומות המרוהטות בתלת-ממד (מפרט פינס 48):</div>
      <div class="grid-2" style="margin-bottom:8px;">
        <button onclick="openFurnishedDollhouse('f4')" class="ui-btn ui-btn-lux" style="font-weight:800;">✨ קומה 4 מרוהטת 3D (+13.26)</button>
        <button onclick="openFurnishedDollhouse('f5')" class="ui-btn ui-btn-lux" style="font-weight:800;">✨ קומה 5 מרוהטת 3D (+16.32)</button>
      </div>

      <div style="font-size:11px;font-weight:800;color:#1e3a8a;margin-bottom:5px;">🏢 בניין 37 (צפוני) — סיור פנים מרוהט 3D (קומות 4–5 ופנטהאוז):</div>
      <div class="grid-2" style="margin-bottom:8px;">
        <button onclick="startPresetInteriorTour(37, 4, 'NW')" class="ui-btn ui-btn-lux">✨ ב'37 ק'4 · 5 חד' צפ'-מערב</button>
        <button onclick="startPresetInteriorTour(37, 4, 'E')" class="ui-btn ui-btn-lux">✨ ב'37 ק'4 · 5 חד' חזית מזרחית</button>
        <button onclick="startPresetInteriorTour(37, 5, 'NE')" class="ui-btn ui-btn-lux">✨ ב'37 ק'5 · 3 חד' צפ'-מזרח</button>
        <button onclick="startPresetInteriorTour(37, 5, 'SE')" class="ui-btn ui-btn-lux">✨ ב'37 ק'5 · 4 חד' דר'-מזרח</button>
        <button onclick="startPresetInteriorTour(37, 8, 'E')" class="ui-btn" style="background:#0f172a;color:#fde047;border-color:#334155;font-weight:800;">👑 ב'37 · מיני-פנטהאוז ק' 8</button>
        <button onclick="startPresetInteriorTour(37, 9, 'W')" class="ui-btn" style="background:#0f172a;color:#fde047;border-color:#334155;font-weight:800;">👑 ב'37 · פנטהאוז ק' 9</button>
      </div>

      <div style="font-size:11px;font-weight:800;color:#047857;margin-bottom:5px;">🏢 בניין 39 (דרומי) — סיור פנים מרוהט 3D (קומות 4–5 ופנטהאוז):</div>
      <div class="grid-2" style="margin-bottom:8px;">
        <button onclick="startPresetInteriorTour(39, 4, 'NW')" class="ui-btn ui-btn-lux">✨ ב'39 ק'4 · 3 חד' צפ'-מערב</button>
        <button onclick="startPresetInteriorTour(39, 5, 'SW')" class="ui-btn ui-btn-lux">✨ ב'39 ק'5 · 4 חד' דר'-מערב</button>
        <button onclick="startPresetInteriorTour(39, 5, 'SE')" class="ui-btn ui-btn-lux">✨ ב'39 ק'5 · 4 חד' דר'-מזרח</button>
        <button onclick="startPresetInteriorTour(39, 9, 'E')" class="ui-btn" style="background:#0f172a;color:#fde047;border-color:#334155;font-weight:800;">👑 ב'39 · פנטהאוז 6 חד' ק' 9</button>
      </div>

      <div class="section-box" style="margin-bottom:0;">
        <div style="font-size:11px;font-weight:800;color:#451a03;margin-bottom:5px;">🔭 סימולטור "נוף מהמרפסת" לפי קומה מדויקת (קומות 1–9):</div>
        <div style="display:flex;flex-wrap:wrap;gap:4px;" id="balcony-floor-selector">
          <button data-bflr="1" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 1 (+4.08)</button>
          <button data-bflr="2" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 2 (+7.14)</button>
          <button data-bflr="3" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 3 (+10.20)</button>
          <button data-bflr="4" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 4 (+13.26)</button>
          <button data-bflr="5" class="ui-btn active" style="padding:3px 7px;font-size:10px;">קומה 5 (+16.32)</button>
          <button data-bflr="6" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 6 (+19.38)</button>
          <button data-bflr="7" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 7 (+22.44)</button>
          <button data-bflr="8" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 8 (+25.67)</button>
          <button data-bflr="9" class="ui-btn" style="padding:3px 7px;font-size:10px;">פנטהאוז 9 (+28.90)</button>
        </div>
      </div>
    </div>

    <!-- ===================================================================== -->
    <!-- ON-DEMAND POPOVER DRAWER 2: 3D GIS SPATIAL MAP & 46 POIS (CLOSED BY DEFAULT) -->
    <!-- ===================================================================== -->
    <div id="drawer-gis" class="glass-panel dropdown-drawer" style="width:410px;">
      <div class="flex-between" style="margin-bottom:8px;border-bottom:1px solid #e2e8f0;padding-bottom:6px;">
        <div>
          <div style="font-size:13px;font-weight:800;color:#1e3a8a;">📍 מפת מרחקים ו-46 מוקדי סביבה ועירוניות (Google Maps)</div>
          <div style="font-size:11px;color:#64748b;">חינוך, קניות, בריאות, תחבורה ומטרו, תרבות ופארקים בפתח תקווה</div>
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
        <a href="kitroni37_39_spatial_map.html" target="_blank" class="ui-btn" style="background:#0f172a;color:#38bdf8;border-color:#334155;font-weight:800;text-decoration:none;">
          🧭 מפת GIS דו-ממדית (46) ↗
        </a>
        <button id="btn-side-radii" class="ui-btn active">⭕ רדיוסים (8): פעיל</button>
        <button id="btn-side-pois" class="ui-btn active">📍 מיקומים (46): פעיל</button>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px;" id="gis-cat-buttons">
        <button data-gcat="all" class="gis-cat-chip ui-btn active" style="padding:3px 7px;font-size:10px;">הכל (46)</button>
        <button data-gcat="education" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🎓 חינוך (13)</button>
        <button data-gcat="transport" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🚌 תחבורה ומטרו (10)</button>
        <button data-gcat="shopping" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🛒 קניות ומסחר (10)</button>
        <button data-gcat="health" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🏥 בריאות ורפואה (7)</button>
        <button data-gcat="parks" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🌳 פארקים ותרבות (6)</button>
      </div>
      <div style="font-size:11px;font-weight:700;color:#1e3a8a;margin-bottom:4px;">לחץ על מוקד ברשימה למעבר ממוקד במפה:</div>
      <div id="gis-poi-sidebar-list" style="max-height:245px;overflow-y:auto;display:flex;flex-direction:column;gap:4px;padding-left:2px;"></div>
    </div>

    <!-- ===================================================================== -->
    <!-- ON-DEMAND POPOVER DRAWER 3: INTERIOR FINISH PACKAGES, LAYERS & DISPLAY -->
    <!-- ===================================================================== -->
    <div id="drawer-settings" class="glass-panel dropdown-drawer" style="width:390px;">
      <div class="flex-between" style="margin-bottom:8px;border-bottom:1px solid #e2e8f0;padding-bottom:6px;">
        <span style="font-size:13px;font-weight:800;color:#0f172a;">⚙️ עיצוב פנים, שכבות והגדרות תצוגה</span>
        <button data-close-drawer class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
      </div>

      <!-- Real-Time 4 Interior Finish Packages Customizer -->
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

      <!-- Projection & Display Toggles -->
      <div class="section-box">
        <div class="flex-between" style="margin-bottom:6px;">
          <span style="font-size:12px;font-weight:700;color:#334155;">מצב תצוגה, מפת Google Maps וזוויות</span>
          <span id="proj-badge" style="border-radius:4px;background:#e2e8f0;padding:2px 6px;font-size:11px;font-weight:600;color:#1e293b;">פרספקטיבה</span>
        </div>
        <div class="grid-2">
          <button id="btn-gmaps" class="ui-btn active" style="grid-column:span 2;">
            🗺️ מפת לוויין Google Maps (קיטרוני 37–39): פעיל
          </button>
          <button id="btn-ortho" class="ui-btn">📐 היטל אורתוגרפי (1:50)</button>
          <button id="btn-cad-plan" class="ui-btn active">✏️ שרטוט פנים CAD: פעיל</button>
          <button onclick="activatePreset('iso_west')" class="ui-btn">חזית מערבית (קיטרוני)</button>
          <button onclick="activatePreset('iso_east')" class="ui-btn">חזית מזרחית (עורפית)</button>
        </div>
      </div>

      <!-- BIM Layers Visibility -->
      <div class="section-box">
        <div class="flex-between" style="margin-bottom:6px;">
          <span style="font-size:12px;font-weight:700;color:#334155;">שכבות המודל האדריכלי (BIM Layers)</span>
        </div>
        <div id="layer-toggles"></div>
      </div>

      <!-- Sun & Export Row -->
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

    <!-- ===================================================================== -->
    <!-- ONLY PANEL OPEN BY DEFAULT: BOTTOM-RIGHT INTERACTIVE SECTION & CUT CONTROLLER -->
    <!-- ===================================================================== -->
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
        <!-- Continuous Z-Section Height Slider -->
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:8px 10px;margin-bottom:8px;">
          <div class="flex-between" style="margin-bottom:4px;">
            <label for="clip-slider" style="font-size:11px;font-weight:700;color:#0f172a;">מפלס חתך גובה רציף (Z):</label>
            <span id="clip-val" class="cad-badge" style="font-size:11px;font-weight:800;color:#2563eb;">+36.00 מ' (מלא)</span>
          </div>
          <input id="clip-slider" type="range" min="-3.85" max="36.0" step="0.1" value="36.0" />
          <div class="flex-between cad-badge" style="margin-top:3px;font-size:9.5px;color:#64748b;">
            <span>-3.85</span>
            <span>0.00</span>
            <span>+10.20</span>
            <span>+19.38</span>
            <span>+28.90</span>
            <span>+35.16</span>
          </div>
        </div>

        <div class="mode-switch">
          <button id="mode-single" class="active" onclick="setSliceMode('single')">קומה בודדת (תוכנית)</button>
          <button id="mode-cum" onclick="setSliceMode('cumulative')">חיתוך מצטבר</button>
        </div>

        <div class="grid-2" id="floor-buttons"></div>
      </div>
    </aside>

    <!-- ===================================================================== -->
    <!-- FLOATING BOTTOM-LEFT 3D MOVEMENT & PAN CONTROLLER (RIGHT/LEFT/UP/DOWN) -->
    <!-- ===================================================================== -->
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
          <span id="apt-active-badge" style="border-radius:6px;background:#b45309;color:#ffffff;padding:3px 8px;font-size:11px;font-weight:800;">קיטרוני 37–39</span>
          <span id="aptc-active-room-title" style="font-size:13px;font-weight:800;color:#451a03;">סיור פנים אדריכלי 1:50</span>
          <div style="display:inline-flex;align-items:center;gap:3px;background:#fef3c7;border:1px solid #f59e0b;border-radius:6px;padding:2px 6px;">
            <span style="font-size:10px;font-weight:800;color:#92400e;">קומה לנוף:</span>
            <select id="tour-floor-select" style="font-size:11px;font-weight:800;color:#451a03;background:transparent;border:none;cursor:pointer;outline:none;">
              <option value="1">קומה 1 (+4.08)</option>
              <option value="2">קומה 2 (+7.14)</option>
              <option value="3">קומה 3 (+10.20)</option>
              <option value="4">קומה 4 (+13.26)</option>
              <option value="5" selected>קומה 5 (+16.32)</option>
              <option value="6">קומה 6 (+19.38)</option>
              <option value="7">קומה 7 (+22.44)</option>
              <option value="8">קומה 8 (+25.67)</option>
              <option value="9">פנטהאוז 9 (+28.90)</option>
            </select>
          </div>
        </div>
        <div style="display:flex;align-items:center;gap:10px;font-size:11px;color:#57534e;font-weight:600;">
          <span>⌨️ <b>WASD / חיצים</b>: תזוזה ימינה/שמאלה/קדימה/אחורה · <b>E/Q</b>: למעלה/למטה</span>
          <span>🖱️ <b>גרירה</b>: מבט 360°</span>
          <button id="btn-close-tour-hud" class="ui-btn" style="padding:2px 8px;font-size:11px;font-weight:800;background:#ef4444;color:#fff;border-color:#dc2626;">✕ יציאה מסיור</button>
        </div>
      </div>

      <div class="flex-between" style="gap:10px;flex-wrap:wrap;">
        <div style="display:flex;flex-wrap:wrap;gap:4px;flex:1;">
          <span style="font-size:11px;font-weight:800;color:#1e3a8a;align-self:center;padding:0 2px;">בניין 37:</span>
          <button onclick="teleportInTour(-11.2, -21.5, 1.4, 'בניין 37 · סלון צפ\'-מערב')" class="room-chip">🛋️ סלון צפ'-מערב</button>
          <button onclick="teleportInTour(14.5, -21.5, -1.4, 'בניין 37 · דירה מזרחית')" class="room-chip">🛋️ דירה מזרחית</button>
          <button onclick="teleportInTour(-14.8, -21.5, -1.57, 'בניין 37 · מרפסת מערבית')" class="room-chip">☀️ מרפסת מערבית</button>
          <button onclick="teleportInTour(6.5, -18.2, 0, 'בניין 37 · לובי מעליות')" class="room-chip">🚪 לובי מעליות</button>
          <span style="font-size:11px;font-weight:800;color:#047857;align-self:center;padding:0 2px;margin-right:4px;">בניין 39:</span>
          <button onclick="teleportInTour(-11.2, -1.8, 1.4, 'בניין 39 · דירה צפ\'-מערב')" class="room-chip">🛋️ צפ'-מערב (3 חד')</button>
          <button onclick="teleportInTour(-11.2, 4.2, 1.4, 'בניין 39 · דירה דר\'-מערב')" class="room-chip">🛋️ דר'-מערב (4 חד')</button>
          <button onclick="teleportInTour(14.5, 4.2, -1.4, 'בניין 39 · דירה דר\'-מזרח')" class="room-chip">🛋️ דר'-מזרח (4 חד')</button>
          <button onclick="teleportInTour(-14.9, 4.2, -1.57, 'בניין 39 · מרפסת שמש מערבית')" class="room-chip">☀️ מרפסת ב'39</button>
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

  <!-- Inlined Three.js r128 Core Library -->
  <script>__THREE_JS_CODE__</script>

  <!-- Main Application Script -->
  <script>
    const PLANS = __PLANS_JSON__;
    const CRM_DATA = __CRM_JSON__;
    const KITRONI_UNITS = CRM_DATA.units;
    const PARKING_STALLS = CRM_DATA.parking_stalls;
    const SPATIAL_POIS = __SPATIAL_POIS_JSON__;

    const WIDE_GMAPS_DATA_URI    = "__WIDE_GMAPS_URI__";
    const INNER_GMAPS_DATA_URI   = "__INNER_GMAPS_URI__";
    const CLOSEUP_GMAPS_DATA_URI = "__CLOSEUP_GMAPS_URI__";
    const OUTER_SPAN_M   = __OUTER_SPAN_M__;
    const INNER_SPAN_M   = __INNER_SPAN_M__;
    const CLOSEUP_SPAN_M = __CLOSEUP_SPAN_M__;

    // =========================================================================
    // 1. EXACT FLOOR SCHEDULE & ARCHITECTURAL CONSTANTS (1:1 METERS)
    // =========================================================================
    const FLOORS = [
      { id: 'mar', label: 'מרתף חניון', zFloor: -3.85, zCeil: -0.35, zTop: 0.00, sheet: 'mar', elevText: '-3.85' },
      { id: 'kar', label: 'קומת קרקע', zFloor: 0.00,  zCeil: 3.63,  zTop: 4.08, sheet: 'kar', elevText: '±0.00' },
      { id: 'f1',  label: 'קומה 1',    zFloor: 4.08,  zCeil: 6.77,  zTop: 7.14, sheet: 'k1',  elevText: '+4.08' },
      { id: 'f2',  label: 'קומה 2',    zFloor: 7.14,  zCeil: 9.83,  zTop: 10.20, sheet: 'k2_4', elevText: '+7.14' },
      { id: 'f3',  label: 'קומה 3',    zFloor: 10.20, zCeil: 12.89, zTop: 13.26, sheet: 'k2_4', elevText: '+10.20' },
      { id: 'f4',  label: 'קומה 4 · מרוהטת 3D ✨', zFloor: 13.26, zCeil: 15.95, zTop: 16.32, sheet: 'k2_4', elevText: '+13.26', has3DFurn: true },
      { id: 'f5',  label: 'קומה 5 · מרוהטת 3D ✨', zFloor: 16.32, zCeil: 19.01, zTop: 19.38, sheet: 'k5_7', elevText: '+16.32', has3DFurn: true },
      { id: 'f6',  label: 'קומה 6',    zFloor: 19.38, zCeil: 22.07, zTop: 22.44, sheet: 'k5_7', elevText: '+19.38' },
      { id: 'f7',  label: 'קומה 7',    zFloor: 22.44, zCeil: 25.15, zTop: 25.67, sheet: 'k5_7', elevText: '+22.44' },
      { id: 'f8',  label: 'קומה 8',    zFloor: 25.67, zCeil: 28.40, zTop: 28.90, sheet: 'k8',   elevText: '+25.67' },
      { id: 'f9',  label: 'קומה 9 (פנטהאוז)', zFloor: 28.90, zCeil: 31.66, zTop: 32.16, sheet: 'k9', elevText: '+28.90' },
      { id: 'gag', label: 'גג וחדרי יציאה', zFloor: 32.16, zCeil: 35.16, zTop: 35.16, sheet: 'gag', elevText: '+32.16' }
    ];

    const LAYERS_DEF = [
      { id: 'walls',     name: 'קירות חוץ (לבן) וקירות פנים (אוף-וויט)', color: '#fcfdff', visible: true },
      { id: 'slabs',     name: 'רצפות ותקרות (4 חבילות גמר)', color: '#d6dae0', visible: true },
      { id: 'windows',   name: 'חלונות, וויטרינות ואלומיניום', color: '#38bdf8', visible: true },
      { id: 'doors',     name: 'דלתות פנים וכניסה (עץ בהיר)', color: '#c89d6c', visible: true },
      { id: 'balconies', name: 'מרפסות שמש, חיפוי עץ ומעקות', color: '#a46b3f', visible: true },
      { id: 'pergolas',  name: 'פרגולות קלות ומסתורי כביסה', color: '#334155', visible: true },
      { id: 'furn3d',    name: 'ריהוט פנים תלת-ממדי יוקרתי (קומות 4–5)', color: '#d97706', visible: true },
      { id: 'cad2d',     name: 'ריהוט וכלים סניטריים (2D על הרצפה)', color: '#475569', visible: true },
      { id: 'labels',    name: 'שמות ומידות חדרים פנימיות (בס"מ)', color: '#1e293b', visible: true },
      { id: 'site',      name: 'מרתף חניון (63 חניות), רמפה ופיתוח', color: '#94a3b8', visible: true }
    ];

    // =========================================================================
    // 2. THREE.JS SCENE, CAMERAS (PERSPECTIVE + ORTHO 1:50) & LIGHTING
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

    const clipPlane = new THREE.Plane(new THREE.Vector3(0, -1, 0), 36.0);
    const clippingPlanes = [clipPlane];

    const aspect = window.innerWidth / window.innerHeight;
    const perspCam = new THREE.PerspectiveCamera(42, aspect, 0.2, 8000);
    const orthoSize = 26;
    const orthoCam = new THREE.OrthographicCamera(-orthoSize * aspect, orthoSize * aspect, orthoSize, -orthoSize, -2000, 6000);
    let activeCam = perspCam;
    let isOrtho = false;

    const hemiLight = new THREE.HemisphereLight(0xfffdf8, 0xd8d0c2, 0.66);
    hemiLight.position.set(0, 120, 0);
    scene.add(hemiLight);

    const dirLight = new THREE.DirectionalLight(0xfffaf0, 0.72);
    dirLight.position.set(-48, 82, 42);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 2048;
    dirLight.shadow.mapSize.height = 2048;
    dirLight.shadow.camera.near = 10;
    dirLight.shadow.camera.far = 220;
    const dCam = 48;
    dirLight.shadow.camera.left = -dCam;
    dirLight.shadow.camera.right = dCam;
    dirLight.shadow.camera.top = dCam;
    dirLight.shadow.camera.bottom = -dCam;
    dirLight.shadow.bias = -0.0004;
    scene.add(dirLight);

    const fillLight = new THREE.DirectionalLight(0xf3ede2, 0.30);
    fillLight.position.set(55, 50, -45);
    scene.add(fillLight);

    const nightLightsGroup = new THREE.Group();
    nightLightsGroup.visible = false;
    scene.add(nightLightsGroup);
    [[-8, 16, -18], [12, 16, -18], [-8, 16, 1], [12, 16, 1], [2, 30, -18], [2, 30, 1], [2, 4, -8]].forEach(([lx, ly, lz]) => {
      const pl = new THREE.PointLight(0xffb454, 1.4, 38, 1.8);
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
      ctx.fillStyle = c1;
      ctx.fillRect(0, 0, 256, 256);
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

    function createTileTexture(bgHex, gridHex, repeatX = 12, repeatY = 6) {
      const c = document.createElement('canvas');
      c.width = 256; c.height = 256;
      const ctx = c.getContext('2d');
      ctx.fillStyle = bgHex;
      ctx.fillRect(0, 0, 256, 256);
      ctx.strokeStyle = gridHex;
      ctx.lineWidth = 2;
      for (let i = 0; i <= 256; i += 64) {
        ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, 256); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(256, i); ctx.stroke();
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(repeatX, repeatY);
      return tex;
    }

    // Pines-48 Specification Luxury Procedural Textures
    function makeTravertineFloorTexture() {
      const c = document.createElement('canvas');
      c.width = 512; c.height = 512;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#efeadd';
      ctx.fillRect(0, 0, 512, 512);
      for (let i = 0; i < 28; i++) {
        ctx.strokeStyle = (i % 2 === 0) ? 'rgba(218, 208, 190, 0.35)' : 'rgba(232, 224, 208, 0.45)';
        ctx.lineWidth = 6 + (i % 4) * 3;
        ctx.beginPath();
        const y0 = (i * 21) % 512;
        ctx.moveTo(0, y0);
        ctx.bezierCurveTo(170, y0 + 10, 340, y0 - 10, 512, y0 + 4);
        ctx.stroke();
      }
      ctx.strokeStyle = '#d8cfc0';
      ctx.lineWidth = 2;
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
      ctx.fillStyle = '#fbfaf7';
      ctx.fillRect(0, 0, 512, 512);
      const veins = [
        [0, 80, 180, 140, 350, 240, 512, 310, 'rgba(180, 165, 145, 0.42)', 5],
        [40, 0, 210, 190, 310, 360, 490, 512, 'rgba(160, 140, 115, 0.28)', 3],
        [0, 320, 160, 290, 340, 410, 512, 460, 'rgba(195, 170, 130, 0.32)', 4]
      ];
      veins.forEach(v => {
        ctx.strokeStyle = v[8];
        ctx.lineWidth = v[9];
        ctx.beginPath();
        ctx.moveTo(v[0], v[1]);
        ctx.bezierCurveTo(v[2], v[3], v[4], v[5], v[6], v[7]);
        ctx.stroke();
      });
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      return tex;
    }

    function makeFlutedOakTexture() {
      const c = document.createElement('canvas');
      c.width = 512; c.height = 512;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#c89f70';
      ctx.fillRect(0, 0, 512, 512);
      for (let x = 0; x < 512; x += 16) {
        ctx.fillStyle = '#d4ad7e';
        ctx.fillRect(x, 0, 10, 512);
        ctx.fillStyle = '#8c6238';
        ctx.fillRect(x + 10, 0, 6, 512);
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
      ctx.fillStyle = '#e7dfd1';
      ctx.fillRect(0, 0, 256, 256);
      ctx.strokeStyle = 'rgba(195, 182, 162, 0.45)';
      ctx.lineWidth = 2;
      for (let y = 0; y < 256; y += 6) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(256, y); ctx.stroke();
      }
      ctx.strokeStyle = '#d2c5b0';
      ctx.lineWidth = 8;
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

    function makeOffWhitePlasterTexture() {
      const c = document.createElement('canvas');
      c.width = 256; c.height = 256;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#e8dfd0';
      ctx.fillRect(0, 0, 256, 256);
      for (let i = 0; i < 240; i++) {
        ctx.fillStyle = (i % 2 === 0) ? 'rgba(210, 198, 178, 0.26)' : 'rgba(242, 236, 224, 0.30)';
        ctx.fillRect(Math.random() * 256, Math.random() * 256, 14 + Math.random() * 28, 8 + Math.random() * 18);
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(3, 3);
      return tex;
    }

    const texTravertine   = makeTravertineFloorTexture();
    const texCalacatta    = makeCalacattaMarbleTexture();
    const texFlutedOak    = makeFlutedOakTexture();
    const texWovenRug     = makeWovenRugTexture();
    const texOffWhiteWall = makeOffWhitePlasterTexture();

    const MATS = {
      wall: new THREE.MeshStandardMaterial({ map: texOffWhiteWall, color: 0xe8dfd0, roughness: 0.85, metalness: 0.01, side: THREE.DoubleSide, clippingPlanes }),
      extWall: new THREE.MeshStandardMaterial({ color: 0xfcfdff, roughness: 0.72, metalness: 0.02, side: THREE.DoubleSide, clippingPlanes }),
      wallCap: new THREE.MeshStandardMaterial({ color: 0xd2c7b4, roughness: 0.88, metalness: 0.02, side: THREE.DoubleSide, clippingPlanes }),
      slabFloor: new THREE.MeshStandardMaterial({ map: FINISH_TEXTURES.nordic.map, color: 0xd8dce2, roughness: 0.65, metalness: 0.04, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, clippingPlanes }),
      slabEdge: new THREE.MeshStandardMaterial({ color: 0xfcfdff, roughness: 0.76, clippingPlanes }),
      terraceFloor: new THREE.MeshStandardMaterial({ color: 0xcbd5e1, roughness: 0.72, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, clippingPlanes }),
      woodDeck: new THREE.MeshStandardMaterial({ map: DECK_TEXTURES.wood, roughness: 0.55, metalness: 0.05, clippingPlanes }),
      glassRailing: new THREE.MeshPhysicalMaterial({ color: 0xdbeafe, transparent: true, opacity: 0.38, roughness: 0.1, metalness: 0.05, side: THREE.DoubleSide, clippingPlanes }),
      aluDark: new THREE.MeshStandardMaterial({ color: 0x242930, roughness: 0.4, metalness: 0.6, clippingPlanes }),
      winGlass: new THREE.MeshPhysicalMaterial({ color: 0xbae6fd, emissive: 0x000000, emissiveIntensity: 0.0, transparent: true, opacity: 0.42, roughness: 0.08, metalness: 0.15, side: THREE.DoubleSide, clippingPlanes }),
      lightWood: new THREE.MeshStandardMaterial({ color: 0xd4ad7d, roughness: 0.52, metalness: 0.04, clippingPlanes }),
      doorFrame: new THREE.MeshStandardMaterial({ color: 0xb0895a, roughness: 0.55, clippingPlanes }),
      basementConcrete: new THREE.MeshStandardMaterial({ color: 0xcbd5e1, roughness: 0.85, side: THREE.DoubleSide, clippingPlanes }),
      asphalt: new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.9, clippingPlanes }),
      sidewalk: new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.85, clippingPlanes }),
      grass: new THREE.MeshStandardMaterial({ color: 0xd1fae5, roughness: 0.9, clippingPlanes }),
      solarPanel: new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.25, metalness: 0.5, clippingPlanes }),
      lineFurn: new THREE.LineBasicMaterial({ color: 0x334155, transparent: true, opacity: 0.85, clippingPlanes }),
      lineCad: new THREE.LineBasicMaterial({ color: 0x0f172a, transparent: true, opacity: 0.78, clippingPlanes }),
      // Pines-48 Luxury Interior Materials (for Floors 4 & 5)
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

    // =========================================================================
    // 4. GEOMETRY HELPERS (PRESERVING EXACT 1:1 KITRONI 37-39 ARCHITECTURE)
    // =========================================================================
    function isExteriorWallFace(sheetKey, x1, y1, x2, y2) {
      if (sheetKey === 'gag') return true;
      if (sheetKey === 'mar') return false;
      const xm = 0.5 * (x1 + x2);
      const ym = 0.5 * (y1 + y2);
      const tol = 0.085;
      const isB37 = (ym < -8.0);

      if (sheetKey === 'kar') {
        if (xm >= 19.44 || xm <= -13.78 || ym <= -25.07 || ym >= 7.48) return true;
        if (isB37 && ym >= -11.38) return true;
        if (!isB37 && ym <= -4.87) return true;
        return false;
      }

      if (sheetKey === 'k1' || sheetKey === 'k2_4' || sheetKey === 'k5_7') {
        if (isB37) {
          return (xm <= -13.855 + tol || xm >= 19.628 - tol || ym <= -25.148 + tol || ym >= -11.300 - tol);
        } else {
          return (xm <= -13.949 + tol || xm >= 19.522 - tol || ym <= -4.950 + tol || ym >= 7.559 - tol);
        }
      }

      if (sheetKey === 'k8') {
        if (isB37) {
          if (xm <= -13.855 + tol || ym <= -25.148 + tol || ym >= -11.300 - tol) return true;
          if (ym <= -19.85 && xm >= 15.575 - tol) return true;
          if (xm >= 15.50 && Math.abs(ym - (-19.939)) <= tol) return true;
          if (ym >= -20.02 && xm >= 18.424 - tol) return true;
          return false;
        } else {
          if (xm <= -13.948 + tol || ym <= -4.949 + tol || ym >= 7.559 - tol) return true;
          if (ym <= -0.40 && xm >= 14.790 - tol) return true;
          if (xm >= 14.71 && Math.abs(ym - (-0.481)) <= tol) return true;
          if (ym >= -0.56 && xm >= 18.519 - tol) return true;
          return false;
        }
      }

      if (sheetKey === 'k9') {
        if (isB37) {
          if (xm <= -7.671 + tol) return true;
          if (ym <= -23.91 && xm <= -3.196 + tol) return true;
          if (xm <= -3.11 && Math.abs(ym - (-23.999)) <= tol) return true;
          if (ym <= -25.148 + tol) return true;
          if (xm <= 2.53 && Math.abs(ym - (-13.320)) <= tol) return true;
          if (ym >= -13.40 && Math.abs(xm - 2.449) <= tol) return true;
          if (ym >= -11.300 - tol) return true;
          if (ym <= -16.05 && xm >= 15.572 - tol) return true;
          if (xm >= 15.49 && Math.abs(ym - (-16.139)) <= tol) return true;
          if (ym >= -16.22 && xm >= 18.419 - tol) return true;
          return false;
        } else {
          if (xm <= -10.855 + tol || ym <= -4.951 + tol || ym >= 7.559 - tol) return true;
          if (ym <= 2.30 && xm >= 14.783 - tol) return true;
          if (xm >= 14.70 && Math.abs(ym - 2.218) <= tol) return true;
          if (ym >= 2.13 && xm >= 18.518 - tol) return true;
          return false;
        }
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

    function makeExteriorOpeningWallBox(x0, y0, x1, y1, z0, z1, orient) {
      const xm = 0.5 * (x0 + x1);
      const ym = 0.5 * (y0 + y1);
      const bCenterY = (ym < -8.0) ? -18.2 : 1.3;
      // BoxGeometry material order: [+X (East), -X (West), +Y (Top), -Y (Bot), +Z (South), -Z (North)]
      let matPX = MATS.wall, matNX = MATS.wall, matPZ = MATS.wall, matNZ = MATS.wall;
      if (orient === 'H') {
        if (ym > bCenterY) matPZ = MATS.extWall;
        else matNZ = MATS.extWall;
      } else {
        if (xm > 2.5) matPX = MATS.extWall;
        else matNX = MATS.extWall;
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

      if (kind === 'vitrine') {
        const zTopOpen = Math.min(zFloor + 2.20, zCeil - 0.15);
        if (zCeil > zTopOpen + 0.02) {
          const lintel = makeExteriorOpeningWallBox(x0, y0, x1, y1, zTopOpen, zCeil, orient);
          addToFloorAndLayer(floorObj.id, 'walls', lintel);
        }
        const vGrp = new THREE.Group();
        const fThick = 0.05;
        vGrp.add(makeBox(x0, y0, x1, y1, zFloor, zFloor + fThick, MATS.aluDark, false));
        vGrp.add(makeBox(x0, y0, x1, y1, zTopOpen - fThick, zTopOpen, MATS.aluDark, false));
        if (orient === 'H') {
          const midX = 0.5 * (x0 + x1);
          const midY = 0.5 * (y0 + y1);
          vGrp.add(makeBox(x0, y0, x0 + fThick, y1, zFloor, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(x1 - fThick, y0, x1, y1, zFloor, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(midX - 0.025, midY - 0.04, midX + 0.025, midY + 0.04, zFloor, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(x0 + fThick, midY - 0.015, x1 - fThick, midY + 0.015, zFloor + fThick, zTopOpen - fThick, MATS.winGlass, false));
        } else {
          const midX = 0.5 * (x0 + x1);
          const midY = 0.5 * (y0 + y1);
          vGrp.add(makeBox(x0, y0, x1, y0 + fThick, zFloor, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(x0, y1 - fThick, x1, y1, zFloor, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(midX - 0.04, midY - 0.025, midX + 0.04, midY + 0.025, zFloor, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(midX - 0.015, y0 + fThick, midX + 0.015, y1 - fThick, zFloor + fThick, zTopOpen - fThick, MATS.winGlass, false));
        }
        addToFloorAndLayer(floorObj.id, 'windows', vGrp);

      } else if (kind === 'win_tall') {
        const zSill = zFloor + 0.15;
        const zGuard = zFloor + 1.10;
        const zHead = Math.min(zFloor + 2.20, zCeil - 0.15);
        addToFloorAndLayer(floorObj.id, 'walls', makeExteriorOpeningWallBox(x0, y0, x1, y1, zFloor, zSill, orient));
        if (zCeil > zHead + 0.02) {
          addToFloorAndLayer(floorObj.id, 'walls', makeExteriorOpeningWallBox(x0, y0, x1, y1, zHead, zCeil, orient));
        }
        const wGrp = new THREE.Group();
        const fThick = 0.045;
        wGrp.add(makeBox(x0 - 0.01, y0 - 0.01, x1 + 0.01, y1 + 0.01, zSill - 0.03, zSill + 0.02, MATS.slabEdge, false));
        wGrp.add(makeBox(x0, y0, x1, y1, zHead - fThick, zHead, MATS.aluDark, false));
        wGrp.add(makeBox(x0, y0, x1, y1, zGuard - 0.025, zGuard + 0.025, MATS.aluDark, false));

        if (orient === 'H') {
          const midX = 0.5 * (x0 + x1);
          const midY = 0.5 * (y0 + y1);
          const outY = (midY < -18.0 || (midY > -5.5 && midY < 0.0)) ? (y0 + 0.02) : (y1 - 0.02);
          wGrp.add(makeBox(x0, y0, x0 + fThick, y1, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(x1 - fThick, y0, x1, y1, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(midX - 0.02, midY - 0.03, midX + 0.02, midY + 0.03, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(x0 + fThick, midY - 0.012, x1 - fThick, midY + 0.012, zSill + 0.02, zHead - fThick, MATS.winGlass, false));
          wGrp.add(makeBox(x0 + 0.02, outY - 0.01, x1 - 0.02, outY + 0.01, zSill + 0.02, zGuard, MATS.glassRailing, false));
        } else {
          const midX = 0.5 * (x0 + x1);
          const midY = 0.5 * (y0 + y1);
          const outX = (midX < 0) ? (x0 + 0.02) : (x1 - 0.02);
          wGrp.add(makeBox(x0, y0, x1, y0 + fThick, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(x0, y1 - fThick, x1, y1, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(midX - 0.03, midY - 0.02, midX + 0.03, midY + 0.02, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(midX - 0.012, y0 + fThick, midX + 0.012, y1 - fThick, zSill + 0.02, zHead - fThick, MATS.winGlass, false));
          wGrp.add(makeBox(outX - 0.01, y0 + 0.02, outX + 0.01, y1 - 0.02, zSill + 0.02, zGuard, MATS.glassRailing, false));
        }
        addToFloorAndLayer(floorObj.id, 'windows', wGrp);

      } else if (kind === 'window') {
        const span = (orient === 'H') ? (x1 - x0) : (y1 - y0);
        const zSill = (span <= 0.85) ? (zFloor + 1.35) : (zFloor + 1.10);
        const zHead = Math.min(zFloor + 2.20, zCeil - 0.15);
        addToFloorAndLayer(floorObj.id, 'walls', makeExteriorOpeningWallBox(x0, y0, x1, y1, zFloor, zSill, orient));
        if (zCeil > zHead + 0.02) {
          addToFloorAndLayer(floorObj.id, 'walls', makeExteriorOpeningWallBox(x0, y0, x1, y1, zHead, zCeil, orient));
        }
        const wGrp = new THREE.Group();
        const fThick = 0.045;
        wGrp.add(makeBox(x0 - 0.01, y0 - 0.01, x1 + 0.01, y1 + 0.01, zSill - 0.03, zSill + 0.02, MATS.slabEdge, false));
        wGrp.add(makeBox(x0, y0, x1, y1, zHead - fThick, zHead, MATS.aluDark, false));
        if (orient === 'H') {
          const midX = 0.5 * (x0 + x1);
          const midY = 0.5 * (y0 + y1);
          wGrp.add(makeBox(x0, y0, x0 + fThick, y1, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(x1 - fThick, y0, x1, y1, zSill, zHead, MATS.aluDark, false));
          if (span >= 1.15) {
            wGrp.add(makeBox(midX - 0.02, midY - 0.03, midX + 0.02, midY + 0.03, zSill, zHead, MATS.aluDark, false));
          }
          wGrp.add(makeBox(x0 + fThick, midY - 0.012, x1 - fThick, midY + 0.012, zSill + 0.02, zHead - fThick, MATS.winGlass, false));
        } else {
          const midX = 0.5 * (x0 + x1);
          const midY = 0.5 * (y0 + y1);
          wGrp.add(makeBox(x0, y0, x1, y0 + fThick, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(x0, y1 - fThick, x1, y1, zSill, zHead, MATS.aluDark, false));
          if (span >= 1.15) {
            wGrp.add(makeBox(midX - 0.03, midY - 0.02, midX + 0.03, midY + 0.02, zSill, zHead, MATS.aluDark, false));
          }
          wGrp.add(makeBox(midX - 0.012, y0 + fThick, midX + 0.012, y1 - fThick, zSill + 0.02, zHead - fThick, MATS.winGlass, false));
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
      c.width = 256;
      c.height = 128;
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
      ctx.font = 'bold 26px "Segoe UI", Arial, sans-serif';
      ctx.fillText(nameText, 128, dimsText ? 44 : 45);

      if (dimsText) {
        ctx.fillStyle = '#1d4ed8';
        ctx.font = 'bold 22px "Segoe UI", monospace, sans-serif';
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
      const sDepth = thickFascia ? 0.50 : 0.24;
      const curbH = thickFascia ? 0.20 : 0.12;
      bGrp.add(makeBox(x0, y0, x1, y1, zFloor - sDepth, zFloor - 0.03, thickFascia ? MATS.extWall : MATS.slabEdge));
      bGrp.add(makeBox(x0, y0, x1, y1, zFloor - sDepth - 0.02, zFloor - sDepth, MATS.woodDeck));
      bGrp.add(makeBox(x0, y0, x1, y1, zFloor - 0.03, zFloor + 0.01, MATS.woodDeck));

      const zRailTop = zFloor + railHeight;
      const cMat = thickFascia ? MATS.extWall : MATS.slabEdge;
      openSides.forEach(side => {
        if (side === 'W') {
          bGrp.add(makeBox(x0, y0, x0 + 0.12, y1, zFloor, zFloor + curbH, cMat, false));
          bGrp.add(makeBox(x0 + 0.03, y0 + 0.03, x0 + 0.06, y1 - 0.03, zFloor + curbH, zRailTop - 0.03, MATS.glassRailing, false));
          bGrp.add(makeBox(x0 + 0.01, y0, x0 + 0.08, y1, zRailTop - 0.03, zRailTop, MATS.aluDark, false));
        } else if (side === 'E') {
          bGrp.add(makeBox(x1 - 0.12, y0, x1, y1, zFloor, zFloor + curbH, cMat, false));
          bGrp.add(makeBox(x1 - 0.06, y0 + 0.03, x1 - 0.03, y1 - 0.03, zFloor + curbH, zRailTop - 0.03, MATS.glassRailing, false));
          bGrp.add(makeBox(x1 - 0.08, y0, x1 - 0.01, y1, zRailTop - 0.03, zRailTop, MATS.aluDark, false));
        } else if (side === 'N') {
          bGrp.add(makeBox(x0, y0, x1, y0 + 0.12, zFloor, zFloor + curbH, cMat, false));
          bGrp.add(makeBox(x0 + 0.03, y0 + 0.03, x1 - 0.03, y0 + 0.06, zFloor + curbH, zRailTop - 0.03, MATS.glassRailing, false));
          bGrp.add(makeBox(x0, y0 + 0.01, x1, y0 + 0.08, zRailTop - 0.03, zRailTop, MATS.aluDark, false));
        } else if (side === 'S') {
          bGrp.add(makeBox(x0, y1 - 0.12, x1, y1, zFloor, zFloor + curbH, cMat, false));
          bGrp.add(makeBox(x0 + 0.03, y1 - 0.06, x1 - 0.03, y1 - 0.03, zFloor + curbH, zRailTop - 0.03, MATS.glassRailing, false));
          bGrp.add(makeBox(x0, y1 - 0.08, x1, y1 - 0.01, zRailTop - 0.03, zRailTop, MATS.aluDark, false));
        }
      });

      addToFloorAndLayer(floorId, 'balconies', bGrp);

      if (hasPergola) {
        buildLightPergola(floorId, x0, y0, x1, y1, zFloor + 2.75);
      }
    }

    function buildFacadeEnclosures(floorId, zF, zC, laundryShafts) {
      const wGrp = new THREE.Group();
      const lGrp = new THREE.Group();
      const winGrp = new THREE.Group();

      // 1. Staircase (חדר מדרגות) North Exterior Wall & Louvered Glazing in B37 (x=5.20..7.75, y=-25.148..-24.850) and B39 (x=-0.45..2.10, y=-4.950..-4.650)
      [[5.20, 7.75, -25.148, -24.850], [-0.45, 2.10, -4.950, -4.650]].forEach(([sx0, sx1, sy0, sy1]) => {
        // Side wall cheeks (55cm each) + lower sill (0.90m) + upper lintel (zF+2.35..zC)
        wGrp.add(makeExteriorOpeningWallBox(sx0, sy0, sx0 + 0.55, sy1, zF, zC, 'H'));
        wGrp.add(makeExteriorOpeningWallBox(sx1 - 0.55, sy0, sx1, sy1, zF, zC, 'H'));
        wGrp.add(makeExteriorOpeningWallBox(sx0 + 0.55, sy0, sx1 - 0.55, sy1, zF, zF + 0.90, 'H'));
        if (zC > zF + 2.35) {
          wGrp.add(makeExteriorOpeningWallBox(sx0 + 0.55, sy0, sx1 - 0.55, sy1, zF + 2.35, zC, 'H'));
        }
        const wx0 = sx0 + 0.55, wx1 = sx1 - 0.55, wyMid = 0.5 * (sy0 + sy1);
        winGrp.add(makeBox(wx0, sy0, wx1, sy1, zF + 0.88, zF + 0.93, MATS.slabEdge, false));
        winGrp.add(makeBox(wx0 + 0.03, wyMid - 0.015, wx1 - 0.03, wyMid + 0.015, zF + 0.93, zF + 2.33, MATS.winGlass, false));
        for (let z = zF + 0.98; z < zF + 2.30; z += 0.22) {
          lGrp.add(makeBox(wx0 + 0.02, sy0 - 0.02, wx1 - 0.02, sy0 + 0.04, z, z + 0.05, MATS.aluDark, false));
        }
      });

      // 2. Laundry Shafts (מסתור כביסה): Exterior 1.10m sill wall (+26.77 on k8), upper lintel, aluminum louvers, and inner bathroom backing wall + frosted window
      laundryShafts.forEach(([lx0, lx1, ly]) => {
        const isNorth = (ly < -18.0 || (ly > -8.0 && ly < 0.0));
        const wy0 = isNorth ? ly : (ly - 0.25);
        const wy1 = isNorth ? (ly + 0.25) : ly;
        const zSill = zF + 1.10;
        const zHead = Math.min(zF + 2.25, zC - 0.15);

        // Exterior sill wall (0..1.10m) and upper lintel in crisp white exterior finish
        wGrp.add(makeExteriorOpeningWallBox(lx0 - 0.05, wy0, lx1 + 0.05, wy1, zF, zSill, 'H'));
        if (zC > zHead + 0.02) {
          wGrp.add(makeExteriorOpeningWallBox(lx0 - 0.05, wy0, lx1 + 0.05, wy1, zHead, zC, 'H'));
        }
        wGrp.add(makeBox(lx0 - 0.06, wy0 - 0.02, lx1 + 0.06, wy1 + 0.02, zSill - 0.03, zSill + 0.02, MATS.slabEdge, false));

        // Horizontal aluminum louvers across the laundry shaft opening
        for (let z = zSill + 0.08; z < zHead - 0.04; z += 0.18) {
          lGrp.add(makeBox(lx0, ly - 0.04, lx1, ly + 0.04, z, z + 0.055, MATS.aluDark, false));
        }

        // Inner recess backing wall & side cheeks (1.02m deep into shaft) so bathroom interior is enclosed
        const inSign = isNorth ? 1 : -1;
        const backY0 = Math.min(ly + inSign * 0.92, ly + inSign * 1.06);
        const backY1 = Math.max(ly + inSign * 0.92, ly + inSign * 1.06);
        const sideY0 = Math.min(ly, ly + inSign * 1.06);
        const sideY1 = Math.max(ly, ly + inSign * 1.06);
        wGrp.add(makeBox(lx0 - 0.12, sideY0, lx0 + 0.02, sideY1, zF, zC, MATS.wall));
        wGrp.add(makeBox(lx1 - 0.02, sideY0, lx1 + 0.12, sideY1, zF, zC, MATS.wall));
        wGrp.add(makeBox(lx0, backY0, lx1, backY1, zF, zF + 1.35, MATS.wall));
        if (zC > zF + 2.05) {
          wGrp.add(makeBox(lx0, backY0, lx1, backY1, zF + 2.05, zC, MATS.wall));
        }
        winGrp.add(makeBox(lx0 + 0.15, 0.5 * (backY0 + backY1) - 0.02, lx1 - 0.15, 0.5 * (backY0 + backY1) + 0.02, zF + 1.35, zF + 2.05, MATS.winGlass, false));
      });

      addToFloorAndLayer(floorId, 'walls', wGrp);
      addToFloorAndLayer(floorId, 'pergolas', lGrp);
      addToFloorAndLayer(floorId, 'windows', winGrp);
    }

    function buildRoofTerrace(floorId, x0, y0, x1, y1, zFloor, openSides, hasPergola = false, railHeight = 1.10, isWalkableDeck = true) {
      const tGrp = new THREE.Group();
      // Full-depth structural roof slab fascia in crisp exterior white (capping the apartment ceiling below)
      tGrp.add(makeBox(x0, y0, x1, y1, zFloor - 0.50, zFloor - 0.02, MATS.extWall));
      tGrp.add(makeBox(x0, y0, x1, y1, zFloor - 0.02, zFloor + 0.01, isWalkableDeck ? MATS.woodDeck : MATS.terraceFloor));

      const curbH = 0.25; // Architectural curb "55/20 O.K.=+0.25" per k8/k9 plans
      const zRailTop = zFloor + railHeight;
      openSides.forEach(side => {
        if (side === 'W') {
          tGrp.add(makeBox(x0, y0, x0 + 0.20, y1, zFloor, zFloor + curbH, MATS.extWall, false));
          if (railHeight > curbH + 0.05) {
            tGrp.add(makeBox(x0 + 0.07, y0 + 0.03, x0 + 0.10, y1 - 0.03, zFloor + curbH, zRailTop - 0.03, MATS.glassRailing, false));
            tGrp.add(makeBox(x0 + 0.05, y0, x0 + 0.12, y1, zRailTop - 0.03, zRailTop, MATS.aluDark, false));
          }
        } else if (side === 'E') {
          tGrp.add(makeBox(x1 - 0.20, y0, x1, y1, zFloor, zFloor + curbH, MATS.extWall, false));
          if (railHeight > curbH + 0.05) {
            tGrp.add(makeBox(x1 - 0.10, y0 + 0.03, x1 - 0.07, y1 - 0.03, zFloor + curbH, zRailTop - 0.03, MATS.glassRailing, false));
            tGrp.add(makeBox(x1 - 0.12, y0, x1 - 0.05, y1, zRailTop - 0.03, zRailTop, MATS.aluDark, false));
          }
        } else if (side === 'N') {
          tGrp.add(makeBox(x0, y0, x1, y0 + 0.20, zFloor, zFloor + curbH, MATS.extWall, false));
          if (railHeight > curbH + 0.05) {
            tGrp.add(makeBox(x0 + 0.03, y0 + 0.07, x1 - 0.03, y0 + 0.10, zFloor + curbH, zRailTop - 0.03, MATS.glassRailing, false));
            tGrp.add(makeBox(x0, y0 + 0.05, x1, y0 + 0.12, zRailTop - 0.03, zRailTop, MATS.aluDark, false));
          }
        } else if (side === 'S') {
          tGrp.add(makeBox(x0, y1 - 0.20, x1, y1, zFloor, zFloor + curbH, MATS.extWall, false));
          if (railHeight > curbH + 0.05) {
            tGrp.add(makeBox(x0 + 0.03, y1 - 0.10, x1 - 0.03, y1 - 0.07, zFloor + curbH, zRailTop - 0.03, MATS.glassRailing, false));
            tGrp.add(makeBox(x0, y1 - 0.12, x1, y1 - 0.05, zRailTop - 0.03, zRailTop, MATS.aluDark, false));
          }
        }
      });

      addToFloorAndLayer(floorId, 'balconies', tGrp);

      if (hasPergola) {
        buildLightPergola(floorId, x0, y0, x1, y1, zFloor + 2.75);
      }
    }

    function buildLightPergola(floorId, x0, y0, x1, y1, zPergola) {
      const pGrp = new THREE.Group();
      const fH = 0.14, fW = 0.07;
      pGrp.add(makeBox(x0, y0, x1, y0 + fW, zPergola, zPergola + fH, MATS.aluDark));
      pGrp.add(makeBox(x0, y1 - fW, x1, y1, zPergola, zPergola + fH, MATS.aluDark));
      pGrp.add(makeBox(x0, y0, x0 + fW, y1, zPergola, zPergola + fH, MATS.aluDark));
      pGrp.add(makeBox(x1 - fW, y0, x1, y1, zPergola, zPergola + fH, MATS.aluDark));
      for (let y = y0 + 0.25; y < y1 - 0.15; y += 0.28) {
        pGrp.add(makeBox(x0 + fW, y, x1 - fW, y + 0.05, zPergola + 0.03, zPergola + fH - 0.02, MATS.aluDark, false));
      }
      addToFloorAndLayer(floorId, 'pergolas', pGrp);
    }

    // =========================================================================
    // 5. BUILD ALL FLOORS + 63 UNDERGROUND PARKING STALLS IN BASEMENT (-3.85m)
    // =========================================================================
    let parkingHighlightMesh = null;

    function createParkingStallMesh(st) {
      const grp = new THREE.Group();
      const zP = -3.835;
      const c = document.createElement('canvas');
      c.width = 128; c.height = 256;
      const ctx = c.getContext('2d');
      ctx.fillStyle = 'rgba(30, 41, 59, 0.55)';
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
      const sThick = 0.28;

      if (f.id === 'mar') {
        const matSlab = makeBox(-17.03, -28.77, 25.10, 11.18, -4.25, -3.85, MATS.basementConcrete);
        addToFloorAndLayer('mar', 'site', matSlab);
        addToFloorAndLayer('mar', 'site', makeBox(5.15, -25.15, 8.06, -20.00, -5.35, -3.85, MATS.basementConcrete));
        addToFloorAndLayer('mar', 'site', makeBox(-0.20, -4.95, 2.70, 0.20, -5.35, -3.85, MATS.basementConcrete));

        const stallsGrp = new THREE.Group();
        PARKING_STALLS.forEach(st => {
          stallsGrp.add(createParkingStallMesh(st));
        });
        addToFloorAndLayer('mar', 'site', stallsGrp);

        const hlGeo = new THREE.BoxGeometry(2.25, 1.4, 4.75);
        const hlMat = new THREE.MeshBasicMaterial({ color: 0x10b981, transparent: true, opacity: 0.45 });
        parkingHighlightMesh = new THREE.Mesh(hlGeo, hlMat);
        parkingHighlightMesh.visible = false;
        floorGroups['mar'].add(parkingHighlightMesh);

        const rampGrp = new THREE.Group();
        const nSegs = 14;
        for (let i = 0; i < nSegs; i++) {
          const t0 = i / nSegs, t1 = (i + 1) / nSegs;
          const rx0 = -16.5 + t0 * 24.0;
          const rx1 = -16.5 + t1 * 24.0;
          const rz0 = 0.00 - t0 * 3.85;
          const rz1 = 0.00 - t1 * 3.85;
          rampGrp.add(makeBox(rx0, -31.65, rx1, -28.77, 0.5*(rz0+rz1) - 0.25, 0.5*(rz0+rz1), MATS.asphalt));
          rampGrp.add(makeBox(rx0, -31.85, rx1, -31.60, rz1 - 0.25, 0.90, MATS.basementConcrete));
        }
        addToFloorAndLayer('mar', 'site', rampGrp);
        return;
      }

      if (f.id === 'kar') {
        const siteGrp = new THREE.Group();
        // Immediate building lot pad & garden strips (leaving Google Maps street & neighborhood visible all around!)
        siteGrp.add(makeBox(-16.2, -26.5, 21.5, 8.8, -0.04, -0.01, MATS.sidewalk));
        siteGrp.add(makeBox(-12.0, -10.2, -3.0, -6.0, 0.00, 0.06, MATS.grass));
        siteGrp.add(makeBox(4.0, -10.2, 14.0, -6.0, 0.00, 0.06, MATS.grass));
        addToFloorAndLayer('kar', 'slabs', makeBox(-13.855, -25.150, 19.628, -11.300, -0.25, 0.00, MATS.slabFloor));
        addToFloorAndLayer('kar', 'slabs', makeBox(-13.949, -4.950, 19.522, 7.559, -0.25, 0.00, MATS.slabFloor));
        buildLightPergola('kar', 20.2, -25.0, 24.8, 7.5, 2.85);
        addToFloorAndLayer('kar', 'site', siteGrp);
        return;
      }

      if (f.id === 'gag') {
        const b37Gag = [
          [-2.995, -25.148], [15.577, -25.148], [15.577, -16.134],
          [18.430, -16.134], [18.430, -11.299], [2.455, -11.299],
          [2.455, -13.354], [-7.666, -13.354], [-7.666, -23.980], [-2.995, -23.980]
        ];
        const b39Gag = [
          [-10.848, -4.950], [14.791, -4.950], [14.791, 2.224],
          [18.521, 2.224], [18.521, 7.558], [-10.848, 7.558]
        ];
        addToFloorAndLayer('gag', 'slabs', buildPolygonSlab(b37Gag, 31.66, 32.16, MATS.terraceFloor, MATS.slabEdge));
        addToFloorAndLayer('gag', 'slabs', buildPolygonSlab(b39Gag, 31.66, 32.16, MATS.terraceFloor, MATS.slabEdge));
        addToFloorAndLayer('gag', 'slabs', makeBox(5.156, -25.144, 8.056, -19.999, 34.86, 35.16, MATS.slabEdge));
        addToFloorAndLayer('gag', 'slabs', makeBox(-0.199, -4.949, 2.701, 0.199, 34.86, 35.16, MATS.slabEdge));
        const solarGrp = new THREE.Group();
        [[0.5, -22.5], [3.0, -22.5], [10.5, -22.5], [13.0, -22.5], [-4.5, -2.5], [-2.0, -2.5], [6.5, -2.5], [9.0, -2.5]].forEach(([sx, sy]) => {
          solarGrp.add(makeBox(sx, sy, sx + 1.6, sy + 1.8, 32.16, 32.95, MATS.solarPanel));
        });
        addToFloorAndLayer('gag', 'pergolas', solarGrp);
        return;
      }

      if (['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7'].includes(f.id)) {
        const isK2_4 = ['f2', 'f3', 'f4'].includes(f.id);
        addToFloorAndLayer(f.id, 'slabs', makeBox(-13.855, -25.150, 19.628, -11.300, zF - sThick, zF, [MATS.slabEdge, MATS.slabEdge, MATS.slabFloor, MATS.slabEdge, MATS.slabEdge, MATS.slabEdge]));
        addToFloorAndLayer(f.id, 'slabs', makeBox(-13.949, -4.950, 19.522, 7.559, zF - sThick, zF, [MATS.slabEdge, MATS.slabEdge, MATS.slabFloor, MATS.slabEdge, MATS.slabEdge, MATS.slabEdge]));

        buildBalconyBox(f.id, -15.855, -24.330, -13.855, -18.390, zF, ['W', 'N', 'S'], false);
        buildBalconyBox(f.id, -15.855, -18.270, -13.855, -12.330, zF, ['W', 'N', 'S'], false);
        buildBalconyBox(f.id, 19.628, -25.150, 21.528, -18.830, zF, ['E', 'N', 'S'], false);

        if (isK2_4) {
          const frameGrp = new THREE.Group();
          const fx0 = 19.628, fx1 = 20.080;
          const fy0 = -20.550, fy1 = -15.550;
          const fz0 = zF - 0.15, fz1 = zF + 2.38;
          const ft = 0.22;
          frameGrp.add(makeBox(fx0, fy0, fx1, fy1, fz0, fz0 + ft, MATS.extWall));
          frameGrp.add(makeBox(fx0, fy0, fx1, fy1, fz1 - ft, fz1, MATS.extWall));
          frameGrp.add(makeBox(fx0, fy0, fx1, fy0 + ft, fz0, fz1, MATS.extWall));
          frameGrp.add(makeBox(fx0, fy1 - ft, fx1, fy1, fz0, fz1, MATS.extWall));
          addToFloorAndLayer(f.id, 'walls', frameGrp);
        } else {
          // On Floor 1 (+6.83), the SE balcony of B37 has a light pergola at ceiling level
          const hasSE37Pergola = (f.id === 'f1');
          buildBalconyBox(f.id, 19.628, -18.710, 21.528, -11.300, zF, ['E', 'N', 'S'], hasSE37Pergola);
        }

        buildBalconyBox(f.id, -15.900, -4.950, -13.949, 1.180, zF, ['W', 'N', 'S'], false);
        buildBalconyBox(f.id, -15.900, 1.300, -13.949, 7.559, zF, ['W', 'N', 'S'], false);
        buildBalconyBox(f.id, 19.522, -4.950, 21.422, 1.180, zF, ['E', 'N', 'S'], false);
        buildBalconyBox(f.id, 19.522, 1.360, 21.422, 7.559, zF, ['E', 'N', 'S'], false);

        buildFacadeEnclosures(f.id, zF, f.zCeil, [
          [0.35, 2.45, -25.15], [11.05, 13.15, -25.15], [-3.10, -0.95, -11.30], [13.20, 15.35, -11.30],
          [-9.15, -7.15, -4.95], [7.55, 9.65, -4.95], [-1.40, 0.80, 7.56], [9.75, 11.95, 7.56]
        ]);
        return;
      }

      if (f.id === 'f8') {
        const b37K8 = [
          [-13.855, -25.148], [15.575, -25.148], [15.575, -19.939],
          [18.424, -19.939], [18.424, -11.300], [-13.855, -11.300]
        ];
        const b39K8 = [
          [-13.949, -4.950], [14.790, -4.950], [14.790, -0.481],
          [18.519, -0.481], [18.519, 7.559], [-13.949, 7.559]
        ];
        addToFloorAndLayer('f8', 'slabs', buildPolygonSlab(b37K8, zF - 0.52, zF, MATS.slabFloor, MATS.slabEdge));
        addToFloorAndLayer('f8', 'slabs', buildPolygonSlab(b39K8, zF - 0.52, zF, MATS.slabFloor, MATS.slabEdge));

        // Building 37 (Apt 27 — Rear East Facade, Roof Terrace, Cantilevered Balcony, Continuous SE Walkway & Pergolas):
        // 1. Seamless NE Roof Terrace (מרפסת גג 501×575 on Floor 7 slab) + Cantilevered East Balcony (מרפסת 190×653) + Continuous SE Balcony Walkway (120cm wide outside bedroom vitrines)
        buildRoofTerrace('f8', 15.575, -25.148, 19.628, -19.939, zF, ['N'], false, 1.10, true);
        buildRoofTerrace('f8', 18.424, -19.939, 19.628, -18.610, zF, [], false, 1.10, true);
        buildBalconyBox('f8', 19.628, -25.148, 21.528, -18.610, zF, ['N', 'E', 'S'], false, 1.10, true);
        // Continuous SE terrace walkway (x=18.424..19.628, y=-18.610..-11.300) with 1.10m glass railing (מעקה שקוף 110)
        buildRoofTerrace('f8', 18.424, -18.610, 19.628, -11.300, zF, ['E', 'S'], false, 1.10, true);
        // 2. SE Light Pergolas (פרגולה קלה) on Floor 8:
        //    - At Floor 8 slab level (+24.79 on k8 plan / +25.30 on East elevation), projecting East (190×732 cm) over Floor 7's SE balcony
        buildLightPergola('f8', 19.628, -18.610, 21.528, -11.300, zF - 0.48);
        //    - At Floor 8 ceiling level (+28.40 on k9 plan & East elevation), projecting East (190×482 cm) from SE wall (x=18.419..20.319, y=-16.139..-11.300)
        buildLightPergola('f8', 18.419, -16.139, 20.319, -11.300, zF + 2.73);

        // Building 39 (Apt 30 — Rear East Facade, Roof Terrace, Cantilevered Balcony, Continuous SE Walkway & Pergolas):
        // 1. Seamless NE Roof Terrace (מרפסת גג 447×663 on Floor 7 slab) + Cantilevered East Balcony (מרפסת 190×477) + Continuous SE Balcony Walkway (100cm wide outside bedroom vitrines)
        buildRoofTerrace('f8', 14.790, -4.950, 19.522, -0.481, zF, ['N'], false, 1.10, true);
        buildRoofTerrace('f8', 18.519, -0.481, 19.522, -0.180, zF, [], false, 1.10, true);
        buildBalconyBox('f8', 19.522, -4.950, 21.422, -0.180, zF, ['N', 'E', 'S'], false, 1.10, true);
        // Continuous SE terrace walkway (x=18.519..19.522, y=-0.180..7.559) with 1.10m glass railing (מעקה שקוף 110)
        buildRoofTerrace('f8', 18.519, -0.180, 19.522, 7.559, zF, ['E', 'S'], false, 1.10, true);
        // 2. SE Light Pergolas (פרגולה קלה) on Floor 8:
        //    - At Floor 8 slab level (+24.79 on k8 plan / +25.30 on East elevation), projecting East (190×774 cm) over Floor 7's SE balcony
        buildLightPergola('f8', 19.522, -0.180, 21.422, 7.559, zF - 0.48);
        //    - At Floor 8 ceiling level (+28.40 on k9 plan & East elevation), projecting East (190×534 cm) from SE wall (x=18.518..20.418, y=2.218..7.559)
        buildLightPergola('f8', 18.518, 2.218, 20.418, 7.559, zF + 2.73);

        // West Balconies on Floor 8 — WITH their light pergolas at the ceiling of Floor 8 (+27.85 / +28.40 per k9 plan & West elevation!)
        buildBalconyBox('f8', -15.855, -24.330, -13.855, -18.390, zF, ['W', 'N', 'S'], true, 1.10);
        buildBalconyBox('f8', -15.855, -18.270, -13.855, -12.330, zF, ['W', 'N', 'S'], true, 1.10);
        buildBalconyBox('f8', -15.900, -4.950, -13.949, 1.180, zF, ['W', 'N', 'S'], true, 1.10);
        buildBalconyBox('f8', -15.900, 1.300, -13.949, 7.559, zF, ['W', 'N', 'S'], true, 1.10);

        buildFacadeEnclosures('f8', zF, f.zCeil, [
          [0.35, 2.45, -25.15], [-3.10, -0.95, -11.30], [13.20, 15.35, -11.30],
          [-9.15, -7.15, -4.95], [-1.40, 0.80, 7.56], [9.75, 11.95, 7.56]
        ]);
        return;
      }

      if (f.id === 'f9') {
        const b37K9 = [
          [-3.196, -25.148], [15.572, -25.148], [15.572, -16.139],
          [18.419, -16.139], [18.419, -11.299], [2.449, -11.299],
          [2.449, -13.320], [-7.671, -13.320], [-7.671, -23.999], [-3.196, -23.999]
        ];
        const b39K9 = [
          [-10.855, -4.951], [14.783, -4.951], [14.783, 2.218],
          [18.518, 2.218], [18.518, 7.559], [-10.855, 7.559]
        ];
        addToFloorAndLayer('f9', 'slabs', buildPolygonSlab(b37K9, zF - 0.50, zF, MATS.slabFloor, MATS.slabEdge));
        addToFloorAndLayer('f9', 'slabs', buildPolygonSlab(b39K9, zF - 0.50, zF, MATS.slabFloor, MATS.slabEdge));

        // Building 37 Penthouse Roof Terraces & Pergolas (exact match to k9 plan & elevations: NO cantilevered balconies on f9!)
        // 1. West Roof Terrace (מרפסת גג 618×1385 on Floor 8 slab) with 130cm glass railing & light pergola at +31.66
        buildRoofTerrace('f9', -13.855, -25.148, -7.671, -11.300, zF, ['W', 'N', 'S'], true, 1.30, true);
        // 2. NW Setback Terrace Strip (448×115) & SW Roof Terrace (מרפסת גג 1012×202)
        buildRoofTerrace('f9', -7.671, -25.148, -3.196, -23.999, zF, ['N'], false, 1.30, true);
        buildRoofTerrace('f9', -7.671, -13.320, 2.449, -11.300, zF, ['S', 'E'], false, 1.30, true);
        // 3. East Roof Terrace (מרפסת גג 285×901 on Floor 8 slab, open 'N' & 'E'; South side y=-16.139 is Master Bedroom wall) + light pergola over northern bay
        buildRoofTerrace('f9', 15.572, -25.148, 18.419, -16.139, zF, ['N', 'E'], false, 1.30, true);
        buildLightPergola('f9', 15.572, -25.148, 18.419, -19.939, zF + 2.75);

        // Building 39 Penthouses (Apt 32 West & Apt 33 East) Roof Terraces & Pergolas (exact match to k9 plan & elevations)
        // 1. West Roof Terrace (מרפסת גג 309×1251 on Floor 8 slab) with 130cm glass railing & light pergola at +31.66
        buildRoofTerrace('f9', -13.949, -4.951, -10.855, 7.559, zF, ['W', 'N', 'S'], true, 1.30, true);
        // 2. East Roof Terrace (מרפסת גג 374×717 on Floor 8 slab, open 'N' & 'E'; South side y=2.218 is Master Bedroom wall) + light pergola over northern bay
        buildRoofTerrace('f9', 14.783, -4.951, 18.518, 2.218, zF, ['N', 'E'], false, 1.30, true);
        buildLightPergola('f9', 14.783, -4.951, 18.518, -0.481, zF + 2.75);

        buildFacadeEnclosures('f9', zF, f.zCeil, [
          [0.35, 2.45, -25.15], [13.20, 15.35, -11.30],
          [-1.40, 0.80, 7.56], [9.75, 11.95, 7.56]
        ]);
        return;
      }
    }

    // =========================================================================
    // 5B. PINES-48 SPECIFICATION 3D LUXURY INTERIOR MODELING ENGINE (FLOORS 4 & 5)
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

    function parseDimsMeters(dimsStr, defW = 3.2, defD = 3.6) {
      if (!dimsStr || !dimsStr.includes('×')) return [defW, defD];
      const parts = dimsStr.split('×').map(s => parseFloat(s.trim()));
      if (parts.length === 2 && !isNaN(parts[0]) && !isNaN(parts[1])) {
        return [parts[0] / 100.0, parts[1] / 100.0];
      }
      return [defW, defD];
    }

    function buildPines48LivingRoom(grp, rx, ry, rw, rd, zF, zC, isWestWing) {
      // 1. Travertine floor zone + hand-woven wool area rug
      grp.add(makeBox(rx - rw * 0.46, ry - rd * 0.46, rx + rw * 0.46, ry + rd * 0.46, zF + 0.004, zF + 0.016, MATS.luxTravertine, false));
      const rugW = Math.min(2.50, rw * 0.68);
      const rugD = Math.min(3.10, rd * 0.64);
      grp.add(makeBox(rx - rugW * 0.5, ry - rugD * 0.5, rx + rugW * 0.5, ry + rugD * 0.5, zF + 0.016, zF + 0.030, MATS.luxRug, false));

      // Orientation: Sofa on inner wall facing TV wall toward outer side (or North/South wall)
      const dir = isWestWing ? -1 : 1; // -1 = West balcony at x-1.9, +1 = East balcony at x+1.9
      const sofaX = rx - dir * 0.82;
      const tvX   = rx + dir * 1.42;

      // 2. 3-Seater Italian Bouclé Sofa (2.30m long along Y, 0.92m deep along X)
      const sLen = Math.min(2.36, rd * 0.52);
      const sHalf = sLen * 0.5;
      const sx0 = sofaX - 0.44, sx1 = sofaX + 0.44;
      // Oak plinth & legs
      grp.add(makeBox(sx0, ry - sHalf, sx1, ry + sHalf, zF + 0.03, zF + 0.11, MATS.luxOakSmooth));
      // Seat base & 3 bouclé cushions
      grp.add(makeBox(sx0, ry - sHalf, sx1, ry + sHalf, zF + 0.11, zF + 0.41, MATS.luxBoucle));
      const cStep = (sLen - 0.24) / 3.0;
      for (let i = 0; i < 3; i++) {
        const cy0 = (ry - sHalf + 0.12) + i * cStep;
        const cy1 = cy0 + cStep - 0.02;
        grp.add(makeBox(sx0 + 0.04, cy0, sx1 - 0.04, cy1, zF + 0.41, zF + 0.46, MATS.luxBoucle));
      }
      // Backrest & armrests (kept low at +0.76m per Pines 48 spec)
      const backX0 = isWestWing ? (sx1 - 0.18) : sx0;
      const backX1 = isWestWing ? sx1 : (sx0 + 0.18);
      grp.add(makeBox(backX0, ry - sHalf, backX1, ry + sHalf, zF + 0.41, zF + 0.76, MATS.luxBoucle));
      grp.add(makeBox(sx0, ry - sHalf, sx1, ry - sHalf + 0.16, zF + 0.41, zF + 0.64, MATS.luxBoucle));
      grp.add(makeBox(sx0, ry + sHalf - 0.16, sx1, ry + sHalf, zF + 0.41, zF + 0.64, MATS.luxBoucle));
      // Accent throw pillows (mocha-taupe & sand linen)
      const pFrontX = isWestWing ? (backX0 - 0.14) : (backX1 + 0.14);
      grp.add(makeBox(Math.min(backX0, pFrontX), ry - sHalf + 0.22, Math.max(backX1, pFrontX), ry - sHalf + 0.56, zF + 0.45, zF + 0.72, MATS.luxTaupe));
      grp.add(makeBox(Math.min(backX0, pFrontX), ry + sHalf - 0.56, Math.max(backX1, pFrontX), ry + sHalf - 0.22, zF + 0.45, zF + 0.72, MATS.luxLinenSand));

      // 3. Sculptural Calacatta Marble Coffee Table on Fluted Oak Pedestals
      const ctX = rx + dir * 0.15;
      grp.add(makeCylinder(ctX, ry - 0.34, 0.18, 0.18, zF + 0.03, zF + 0.35, MATS.luxFlutedOak, 16));
      grp.add(makeCylinder(ctX, ry + 0.34, 0.18, 0.18, zF + 0.03, zF + 0.35, MATS.luxFlutedOak, 16));
      grp.add(makeBox(ctX - 0.42, ry - 0.65, ctX + 0.42, ry + 0.65, zF + 0.35, zF + 0.40, MATS.luxCalacatta));
      // Brass tray & ceramic olive vase
      grp.add(makeBox(ctX - 0.18, ry - 0.22, ctX + 0.18, ry + 0.18, zF + 0.40, zF + 0.425, MATS.luxBrass));
      grp.add(makeCylinder(ctX, ry - 0.04, 0.07, 0.09, zF + 0.425, zF + 0.62, MATS.luxCeramic, 12));
      grp.add(makeCylinder(ctX, ry - 0.04, 0.16, 0.05, zF + 0.60, zF + 0.82, MATS.luxPlantOlive, 10));

      // 4. Bouclé Lounge Armchair
      const chairY = ry + sHalf + 0.52;
      if (Math.abs(chairY - ry) < rd * 0.44) {
        grp.add(makeBox(ctX - 0.36, chairY - 0.36, ctX + 0.36, chairY + 0.36, zF + 0.03, zF + 0.38, MATS.luxBoucle));
        grp.add(makeBox(ctX - 0.36, chairY + 0.18, ctX + 0.36, chairY + 0.36, zF + 0.38, zF + 0.72, MATS.luxTaupe));
      }

      // 5. Low Floating Cashmere & Calacatta Console (No TV per user request)
      const mediaY = (ry < -18 || (ry > -5 && ry < 0)) ? (ry - rd * 0.44) : (ry + rd * 0.44);
      const mSign = (mediaY < ry) ? 1 : -1;
      const mDepthY0 = Math.min(mediaY, mediaY + mSign * 0.42);
      const mDepthY1 = Math.max(mediaY, mediaY + mSign * 0.42);
      grp.add(makeBox(rx - 1.10, mDepthY0, rx + 1.10, mDepthY1, zF + 0.22, zF + 0.50, MATS.luxCabinet));
      grp.add(makeBox(rx - 1.12, mDepthY0 - 0.01, rx + 1.12, mDepthY1 + 0.01, zF + 0.50, zF + 0.53, MATS.luxCalacatta));

      // 6. Sheer Linen Curtains flanking the balcony vitrine
      const vitX = rx + dir * (rw * 0.45);
      grp.add(makeBox(vitX - 0.08, ry - rd * 0.42, vitX + 0.08, ry - rd * 0.28, zF + 0.03, zC - 0.18, MATS.luxCurtain, false));
      grp.add(makeBox(vitX - 0.08, ry + rd * 0.28, vitX + 0.08, ry + rd * 0.42, zF + 0.03, zC - 0.18, MATS.luxCurtain, false));

      // 7. Ceiling Magnetic Track Lighting
      grp.add(makeBox(rx - 0.90, ry - 1.10, rx + 0.90, ry - 1.04, zC - 0.04, zC - 0.01, MATS.aluDark, false));
      grp.add(makeBox(rx - 0.90, ry + 1.04, rx + 0.90, ry + 1.10, zC - 0.04, zC - 0.01, MATS.aluDark, false));
      grp.add(makeBox(rx - 0.75, ry - 1.09, rx + 0.75, ry - 1.05, zC - 0.045, zC - 0.035, MATS.luxGlowWarm, false));
      grp.add(makeBox(rx - 0.75, ry + 1.05, rx + 0.75, ry + 1.09, zC - 0.045, zC - 0.035, MATS.luxGlowWarm, false));
    }

    function buildPines48KitchenAndDining(grp, kx, ky, kw, kd, zF, zC) {
      // 1. Travertine floor zone
      grp.add(makeBox(kx - kw * 0.48, ky - kd * 0.48, kx + kw * 0.48, ky + kd * 0.48, zF + 0.004, zF + 0.016, MATS.luxTravertine, false));

      // Determine back wall Y (North wall if ky is near -23.1 or -3.1, South wall if ky is near -13.4 or +5.7)
      const isNorthWall = (ky < -18.0 || (ky > -8.0 && ky < 0.0));
      const wallY = isNorthWall ? (ky - kd * 0.44) : (ky + kd * 0.44);
      const inSign = isNorthWall ? 1 : -1;

      const cX0 = kx - kw * 0.44;
      const cX1 = kx + kw * 0.44;
      const runLen = cX1 - cX0;
      const tallW = Math.min(1.20, runLen * 0.36);

      // 2. Tall Fluted-Oak Appliance Tower (Built-in Ovens + Integrated Fridge)
      const tY0 = Math.min(wallY, wallY + inSign * 0.64);
      const tY1 = Math.max(wallY, wallY + inSign * 0.64);
      grp.add(makeBox(cX0, tY0, cX0 + tallW, tY1, zF + 0.02, zF + 2.18, MATS.luxFlutedOak));
      // Built-in black glass oven & microwave
      const ovFaceY = wallY + inSign * 0.645;
      grp.add(makeBox(cX0 + 0.08, ovFaceY - 0.015, cX0 + tallW * 0.52, ovFaceY + 0.015, zF + 0.85, zF + 1.45, MATS.luxDarkGlass));
      grp.add(makeBox(cX0 + 0.12, ovFaceY - 0.025, cX0 + tallW * 0.48, ovFaceY + 0.025, zF + 1.38, zF + 1.41, MATS.luxBrass));
      // Vertical brass handle for integrated fridge
      grp.add(makeBox(cX0 + tallW * 0.58, ovFaceY - 0.025, cX0 + tallW * 0.61, ovFaceY + 0.025, zF + 0.70, zF + 1.75, MATS.luxBrass));

      // 3. Lower Cashmere Cabinets + Calacatta Countertop + Full-Height Calacatta Backsplash
      const lowX0 = cX0 + tallW + 0.02;
      const lowY0 = Math.min(wallY, wallY + inSign * 0.62);
      const lowY1 = Math.max(wallY, wallY + inSign * 0.62);
      grp.add(makeBox(lowX0, lowY0, cX1, lowY1, zF + 0.02, zF + 0.87, MATS.luxCabinet));
      grp.add(makeBox(lowX0 - 0.01, lowY0 - 0.02, cX1 + 0.01, lowY1 + 0.02, zF + 0.87, zF + 0.91, MATS.luxCalacatta));
      // Backsplash
      grp.add(makeBox(lowX0, wallY, cX1, wallY + inSign * 0.03, zF + 0.91, zF + 1.52, MATS.luxCalacatta));
      // Upper Fluted-Oak Cabinets + Warm LED Strip
      const upY0 = Math.min(wallY, wallY + inSign * 0.36);
      const upY1 = Math.max(wallY, wallY + inSign * 0.36);
      grp.add(makeBox(lowX0, upY0, cX1, upY1, zF + 1.52, zF + 2.18, MATS.luxFlutedOak));
      grp.add(makeBox(lowX0 + 0.05, wallY + inSign * 0.18, cX1 - 0.05, wallY + inSign * 0.24, zF + 1.50, zF + 1.52, MATS.luxGlowWarm));

      // 4. Induction Cooktop + Undermount Ceramic Sink + Arched Brass Faucet
      const midLowX = 0.5 * (lowX0 + cX1);
      const cntY = wallY + inSign * 0.31;
      // Cooktop
      grp.add(makeBox(lowX0 + 0.18, cntY - 0.22, midLowX - 0.08, cntY + 0.22, zF + 0.91, zF + 0.925, MATS.luxDarkGlass));
      // Sink & brass faucet
      grp.add(makeBox(midLowX + 0.10, cntY - 0.20, cX1 - 0.18, cntY + 0.20, zF + 0.89, zF + 0.918, MATS.luxCeramic));
      const sinkX = 0.5 * (midLowX + 0.10 + cX1 - 0.18);
      grp.add(makeCylinder(sinkX, wallY + inSign * 0.09, 0.018, 0.022, zF + 0.91, zF + 1.20, MATS.luxBrass, 12));
      grp.add(makeBox(sinkX - 0.015, wallY + inSign * 0.09, sinkX + 0.015, cntY, zF + 1.18, zF + 1.21, MATS.luxBrass));

      // 5. Sculptural Waterfall Kitchen Island + 2 Bouclé Bar Stools + 2 Brass Pendant Lights
      const islY = wallY + inSign * 1.65;
      const islX0 = kx - 0.92, islX1 = kx + 0.92;
      const islY0 = islY - 0.44, islY1 = islY + 0.44;
      // Fluted oak core
      grp.add(makeBox(islX0 + 0.05, islY0 + 0.04, islX1 - 0.05, islY1 - 0.04, zF + 0.02, zF + 0.87, MATS.luxFlutedOak));
      // Waterfall Calacatta top & sides
      grp.add(makeBox(islX0, islY0, islX1, islY1, zF + 0.87, zF + 0.92, MATS.luxCalacatta));
      grp.add(makeBox(islX0, islY0, islX0 + 0.05, islY1, zF + 0.02, zF + 0.87, MATS.luxCalacatta));
      grp.add(makeBox(islX1 - 0.05, islY0, islX1, islY1, zF + 0.02, zF + 0.87, MATS.luxCalacatta));

      // 2 Bar stools on outer side of island
      const stoolY = islY + inSign * 0.56;
      [-0.45, 0.45].forEach(dx => {
        const sx = kx + dx;
        grp.add(makeCylinder(sx, stoolY, 0.025, 0.16, zF + 0.02, zF + 0.64, MATS.luxBrass, 14));
        grp.add(makeCylinder(sx, stoolY, 0.19, 0.19, zF + 0.64, zF + 0.70, MATS.luxBoucle, 16));
      });

      // 2 Suspended Brass Pendant Lamps above island
      [-0.46, 0.46].forEach(dx => {
        const px = kx + dx;
        grp.add(makeCylinder(px, islY, 0.008, 0.008, zF + 1.85, zC - 0.02, MATS.luxBrass, 8));
        grp.add(makeCylinder(px, islY, 0.11, 0.14, zF + 1.72, zF + 1.85, MATS.luxBrass, 16));
        grp.add(makeCylinder(px, islY, 0.08, 0.08, zF + 1.69, zF + 1.73, MATS.luxGlowWarm, 12));
      });
    }

    function buildPines48Bedroom(grp, bx, by, bw, bd, zF, zC, isMaster) {
      // 1. Warm Oak Parquet floor zone + woven area rug
      grp.add(makeBox(bx - bw * 0.46, by - bd * 0.46, bx + bw * 0.46, by + bd * 0.46, zF + 0.004, zF + 0.015, MATS.woodDeck, false));
      const rugW = isMaster ? 2.20 : 1.75;
      const rugD = isMaster ? 2.40 : 2.00;
      grp.add(makeBox(bx - rugW * 0.5, by - rugD * 0.5, bx + rugW * 0.5, by + rugD * 0.5, zF + 0.015, zF + 0.028, MATS.luxRug, false));

      // Place bed headboard against North or South wall
      const headNorth = (by < -18.0 || (by > -8.0 && by < 0.0));
      const hSign = headNorth ? -1 : 1;
      const headWallY = by + hSign * (bd * 0.43);

      const bedW = isMaster ? 1.76 : 1.42;
      const bedLen = isMaster ? 2.06 : 1.96;
      const bedY0 = Math.min(headWallY, headWallY - hSign * bedLen);
      const bedY1 = Math.max(headWallY, headWallY - hSign * bedLen);

      // 2. Low Fluted-Oak & Sand-Linen Headboard (strictly zF+0.02 .. zF+0.74 below window sills!)
      const hbY0 = Math.min(headWallY, headWallY - hSign * 0.12);
      const hbY1 = Math.max(headWallY, headWallY - hSign * 0.12);
      grp.add(makeBox(bx - bedW * 0.56, hbY0, bx + bedW * 0.56, hbY1, zF + 0.02, zF + 0.74, MATS.luxFlutedOak));
      grp.add(makeBox(bx - bedW * 0.48, hbY0 - 0.01, bx + bedW * 0.48, hbY1 + 0.01, zF + 0.34, zF + 0.70, MATS.luxLinenSand));

      // 3. Solid Oak Bed Frame, White Mattress, Quilted Mocha-Taupe Duvet & Pillows
      grp.add(makeBox(bx - bedW * 0.5, bedY0, bx + bedW * 0.5, bedY1, zF + 0.08, zF + 0.28, MATS.luxOakSmooth));
      grp.add(makeBox(bx - bedW * 0.47, bedY0 + 0.05, bx + bedW * 0.47, bedY1 - 0.05, zF + 0.28, zF + 0.48, MATS.luxCeramic));
      // Duvet runner on foot half of bed
      const duvY0 = headNorth ? (bedY0 + bedLen * 0.38) : (bedY0 + 0.04);
      const duvY1 = headNorth ? (bedY1 - 0.04) : (bedY1 - bedLen * 0.38);
      grp.add(makeBox(bx - bedW * 0.48, duvY0, bx + bedW * 0.48, duvY1, zF + 0.29, zF + 0.50, MATS.luxTaupe));
      // Pillows
      const pilY0 = Math.min(headWallY - hSign * 0.14, headWallY - hSign * 0.42);
      const pilY1 = Math.max(headWallY - hSign * 0.14, headWallY - hSign * 0.42);
      grp.add(makeBox(bx - bedW * 0.42, pilY0, bx - 0.05, pilY1, zF + 0.48, zF + 0.60, MATS.luxBoucle));
      grp.add(makeBox(bx + 0.05, pilY0, bx + bedW * 0.42, pilY1, zF + 0.48, zF + 0.60, MATS.luxBoucle));

      // 4. Floating Nightstands & Brass Table Lamps
      const nsY0 = Math.min(headWallY - hSign * 0.04, headWallY - hSign * 0.42);
      const nsY1 = Math.max(headWallY - hSign * 0.04, headWallY - hSign * 0.42);
      const nsYMid = 0.5 * (nsY0 + nsY1);
      [-1, 1].forEach(side => {
        if (!isMaster && side === 1) return; // Single nightstand + study desk in secondary rooms
        const nx = bx + side * (bedW * 0.5 + 0.28);
        if (Math.abs(nx - bx) < bw * 0.47) {
          grp.add(makeBox(nx - 0.22, nsY0, nx + 0.22, nsY1, zF + 0.24, zF + 0.44, MATS.luxOakSmooth));
          grp.add(makeBox(nx - 0.23, nsY0 - 0.01, nx + 0.23, nsY1 + 0.01, zF + 0.44, zF + 0.46, MATS.luxCalacatta));
          grp.add(makeCylinder(nx, nsYMid, 0.04, 0.06, zF + 0.46, zF + 0.62, MATS.luxBrass, 12));
          grp.add(makeCylinder(nx, nsYMid, 0.09, 0.11, zF + 0.60, zF + 0.72, MATS.luxGlowWarm, 12));
        }
      });

      // 5. Custom Floor-to-Ceiling Wardrobe with Brass Handles along side wall
      const wardX = bx + (bx < 0 ? 1 : -1) * (bw * 0.40);
      const wDepth = 0.56;
      const wx0 = Math.min(wardX, wardX - (bx < 0 ? 1 : -1) * wDepth);
      const wx1 = Math.max(wardX, wardX - (bx < 0 ? 1 : -1) * wDepth);
      const wy0 = by - bd * 0.32;
      const wy1 = by + bd * 0.32;
      grp.add(makeBox(wx0, wy0, wx1, wy1, zF + 0.02, zF + 2.18, MATS.luxCabinet));
      const handleX = (bx < 0) ? (wx0 - 0.015) : (wx1 + 0.015);
      grp.add(makeBox(handleX - 0.01, by - 0.06, handleX + 0.01, by - 0.02, zF + 0.85, zF + 1.55, MATS.luxBrass));
      grp.add(makeBox(handleX - 0.01, by + 0.02, handleX + 0.01, by + 0.06, zF + 0.85, zF + 1.55, MATS.luxBrass));
    }

    function buildPines48Bathroom(grp, bx, by, bw, bd, zF, zC) {
      // 1. Matte Calacatta Marble Floor
      grp.add(makeBox(bx - bw * 0.46, by - bd * 0.46, bx + bw * 0.46, by + bd * 0.46, zF + 0.005, zF + 0.018, MATS.luxCalacatta, false));

      // 2. Floating Fluted-Oak Vanity + Calacatta Countertop + Ceramic Vessel Sink + Backlit Mirror
      const vy0 = by - 0.42, vy1 = by + 0.42;
      const vx0 = bx - bw * 0.42, vx1 = vx0 + 0.50;
      grp.add(makeBox(vx0, vy0, vx1, vy1, zF + 0.28, zF + 0.82, MATS.luxFlutedOak));
      grp.add(makeBox(vx0 - 0.01, vy0 - 0.01, vx1 + 0.02, vy1 + 0.01, zF + 0.82, zF + 0.86, MATS.luxCalacatta));
      grp.add(makeCylinder(vx0 + 0.26, by, 0.18, 0.14, zF + 0.86, zF + 0.98, MATS.luxCeramic, 18));
      grp.add(makeCylinder(vx0 + 0.08, by, 0.015, 0.02, zF + 0.86, zF + 1.08, MATS.luxBrass, 10));
      // Backlit LED Mirror
      grp.add(makeBox(vx0, vy0 + 0.05, vx0 + 0.02, vy1 - 0.05, zF + 1.04, zF + 1.92, MATS.luxGlowWarm));
      grp.add(makeBox(vx0 + 0.02, vy0 + 0.08, vx0 + 0.04, vy1 - 0.08, zF + 1.07, zF + 1.89, MATS.luxMirror));

      // 3. Walk-in Clear Glass Shower Partition + Brass Profile + Rainfall Head
      const sx0 = bx + bw * 0.05, sx1 = bx + bw * 0.44;
      const sy0 = by - bd * 0.44, sy1 = by - 0.05;
      grp.add(makeBox(sx0, sy1 - 0.02, sx1, sy1 + 0.02, zF + 0.02, zF + 2.05, MATS.luxClearGlass, false));
      grp.add(makeBox(sx0, sy1 - 0.025, sx1, sy1 + 0.025, zF + 2.03, zF + 2.06, MATS.luxBrass, false));
      grp.add(makeCylinder(0.5 * (sx0 + sx1), 0.5 * (sy0 + sy1), 0.14, 0.14, zF + 2.08, zF + 2.11, MATS.luxBrass, 16));

      // 4. Wall-Hung White Ceramic Toilet + Brass Flush Plate
      const tx = bx + bw * 0.22;
      const ty = by + bd * 0.26;
      grp.add(makeBox(tx - 0.19, ty - 0.26, tx + 0.19, ty + 0.26, zF + 0.18, zF + 0.43, MATS.luxCeramic));
      grp.add(makeBox(tx - 0.12, ty + 0.22, tx + 0.12, ty + 0.26, zF + 0.88, zF + 1.04, MATS.luxBrass));
    }

    function buildPines48BalconyLounge(grp, bx, by, bw, bd, zF) {
      // 1. Outdoor Teak & Bouclé Lounge Sofa
      const sx0 = bx - 0.42, sx1 = bx + 0.42;
      const sy0 = by - 1.05, sy1 = by + 0.45;
      grp.add(makeBox(sx0, sy0, sx1, sy1, zF + 0.02, zF + 0.14, MATS.luxOakSmooth));
      grp.add(makeBox(sx0 + 0.03, sy0 + 0.03, sx1 - 0.03, sy1 - 0.03, zF + 0.14, zF + 0.38, MATS.luxBoucle));
      grp.add(makeBox(sx0, sy0, sx1, sy0 + 0.16, zF + 0.38, zF + 0.68, MATS.luxTaupe));

      // 2. Round Calacatta Outdoor Coffee Table
      grp.add(makeCylinder(bx, by + 0.95, 0.36, 0.28, zF + 0.02, zF + 0.36, MATS.luxCalacatta, 18));

      // 3. 2 Potted Mediterranean Olive Trees in White Ceramic Planters
      [by - bd * 0.38, by + bd * 0.38].forEach(py => {
        grp.add(makeCylinder(bx, py, 0.24, 0.18, zF + 0.02, zF + 0.52, MATS.luxCeramic, 16));
        grp.add(makeCylinder(bx, py, 0.035, 0.045, zF + 0.52, zF + 1.15, MATS.luxOakSmooth, 10));
        grp.add(makeCylinder(bx, py, 0.38, 0.22, zF + 1.05, zF + 1.68, MATS.luxPlantOlive, 14));
      });
    }

    function buildPines48StyleFloorInteriors(f, pData) {
      const fGrp = new THREE.Group();
      const zF = f.zFloor;
      const zC = f.zCeil;

      (pData.room_labels || []).forEach(rl => {
        const [rw, rd] = parseDimsMeters(rl.dims, 3.2, 3.6);
        const rx = rl.x, ry = rl.y;
        const isWestWing = (rx < 2.5);

        if (rl.name === 'סלון') {
          buildPines48LivingRoom(fGrp, rx, ry, rw, rd, zF, zC, isWestWing);
        } else if (rl.name === 'סלון / מטבח') {
          if (f.sheet === 'k2_4') {
            // 3-Room East-South unit on Floor 4: North half is Living Room, South half is Kitchen
            buildPines48LivingRoom(fGrp, rx, ry - 1.35, 3.6, 3.4, zF, zC, false);
            buildPines48KitchenAndDining(fGrp, rx - 0.6, ry + 1.65, 3.1, 2.8, zF, zC);
          } else {
            // 5-Room East-South unit on Floor 5: Full Living Room facing East balcony
            buildPines48LivingRoom(fGrp, rx, ry, rw, rd, zF, zC, false);
          }
        } else if (rl.name === 'מטבח') {
          buildPines48KitchenAndDining(fGrp, rx, ry, rw, rd, zF, zC);
        } else if (rl.name === 'ח. הורים') {
          buildPines48Bedroom(fGrp, rx, ry, rw, rd, zF, zC, true);
        } else if (rl.name === 'ח. שינה' || rl.name === 'ממ"ד') {
          buildPines48Bedroom(fGrp, rx, ry, rw, rd, zF, zC, false);
        } else if (rl.name.includes('רחצה')) {
          buildPines48Bathroom(fGrp, rx, ry, Math.min(rw, 2.3), Math.min(rd, 2.5), zF, zC);
        } else if (rl.name === 'מרפסת שמש') {
          buildPines48BalconyLounge(fGrp, rx, ry, rw, rd, zF);
        } else if (rl.name === 'לובי מעליות') {
          // Elevator Lobby Travertine & Calacatta Medallion + Fluted Oak Feature Wall
          fGrp.add(makeBox(rx - 2.6, ry - 1.8, rx + 2.6, ry + 1.8, zF + 0.004, zF + 0.016, MATS.luxTravertine, false));
          fGrp.add(makeBox(rx - 1.4, ry - 0.9, rx + 1.4, ry + 0.9, zF + 0.016, zF + 0.024, MATS.luxCalacatta, false));
        }
      });

      // Warm Interior Ambient PointLights across the 4 apartments of Building 37 & Building 39
      [[-10.5, -21.5], [15.5, -21.5], [-10.5, -14.5], [15.5, -14.5],
       [-10.5, -1.5],  [15.5, -1.5],  [-10.5, 4.5],   [15.5, 4.5]].forEach(([lx, ly]) => {
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
          let z0 = f.zFloor;
          let z1 = f.zCeil;
          if (f.id === 'gag') {
            const cx = wp.exterior[0][0], cy = wp.exterior[0][1];
            const isCore = ((cx >= 4.8 && cx <= 8.5 && cy <= -19.5) || (cx >= -0.6 && cx <= 3.1 && cy >= -5.2 && cy <= 0.6));
            z1 = isCore ? 35.16 : 33.46;
          }
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
        if (!f.has3DFurn && pData.furn_lines && pData.furn_lines.length > 0) {
          const fPts = [];
          pData.furn_lines.forEach(s => {
            fPts.push(s[0], zLine, s[1], s[2], zLine, s[3]);
          });
          const fGeo = new THREE.BufferGeometry();
          fGeo.setAttribute('position', new THREE.Float32BufferAttribute(fPts, 3));
          const fLines = new THREE.LineSegments(fGeo, MATS.lineFurn);
          addToFloorAndLayer(f.id, 'cad2d', fLines);
        }
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

    // =========================================================================
    // 6. GEOREFERENCED TRIPLE-RESOLUTION GOOGLE MAPS HYBRID PLANES OF PETAH TIKVA
    //    + 8 CONCENTRIC DISTANCE RINGS + 46 VERIFIED POIS
    // =========================================================================
    const CENTER_LAT = 32.081724;
    const CENTER_LON = 34.890301;
    const R_MERC = 6378137.0;
    const LAT0_RAD = CENTER_LAT * Math.PI / 180.0;
    const LON0_RAD = CENTER_LON * Math.PI / 180.0;
    const COS_LAT0 = Math.cos(LAT0_RAD);
    const MERC_Y0  = Math.asinh(Math.tan(LAT0_RAD));

    // Exact calibrated midpoint & street azimuth (-14.8 deg West of North) matching HaRav Kitroni St
    const SCENE_CX = 0.2;
    const SCENE_CZ = -9.2;

    // Align North-up Google Maps with HaRav Kitroni Street orientation (-14.8 deg)
    const GMAPS_THETA = -14.8 * Math.PI / 180.0;
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
        tl.x, tl.y, tl.z,
        bl.x, bl.y, bl.z,
        br.x, br.y, br.z,
        tl.x, tl.y, tl.z,
        br.x, br.y, br.z,
        tr.x, tr.y, tr.z
      ], 3));
      geom.setAttribute('uv', new THREE.Float32BufferAttribute([
        0, 1, 0, 0, 1, 0,
        0, 1, 1, 0, 1, 1
      ], 2));
      geom.computeVertexNormals();

      const tex = new THREE.TextureLoader().load(dataUri);
      tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
      const mat = new THREE.MeshBasicMaterial({
        map: tex,
        side: THREE.DoubleSide,
        polygonOffset: true,
        polygonOffsetFactor: polyOffsetFactor,
        polygonOffsetUnits: polyOffsetFactor
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

    // 8 Concentric Distance Rings (150m to 2,000m) + Walking-Time Badges
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
      const ringMat = new THREE.MeshBasicMaterial({
        color: rc.hex,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.88,
        depthWrite: false
      });
      const ringMesh = new THREE.Mesh(ringGeom, ringMat);
      ringMesh.position.set(SCENE_CX, 0.35, SCENE_CZ);
      gisRingsGroup.add(ringMesh);

      const haloGeom = new THREE.RingGeometry(rc.r - 10.0, rc.r + 10.0, 160);
      haloGeom.rotateX(-Math.PI / 2);
      const haloMat = new THREE.MeshBasicMaterial({
        color: rc.hex,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.16,
        depthWrite: false
      });
      const haloMesh = new THREE.Mesh(haloGeom, haloMat);
      haloMesh.position.set(SCENE_CX, 0.25, SCENE_CZ);
      gisRingsGroup.add(haloMesh);

      [0.65, -2.49].forEach(ang => {
        const el = document.createElement('div');
        el.style.cssText = `position:absolute;transform:translate(-50%,-50%);background:rgba(15,23,42,0.92);color:#ffffff;border:2px solid ${rc.css};border-radius:999px;padding:2px 10px;font-size:11px;font-weight:800;white-space:nowrap;box-shadow:0 3px 10px rgba(0,0,0,0.40);pointer-events:none;transition:opacity 0.15s;`;
        el.textContent = `⭕ ${rc.label}`;
        gisLabelsContainer.appendChild(el);
        gisRingLabelObjs.push({
          el,
          pos: new THREE.Vector3(SCENE_CX + rc.r * Math.cos(ang), 3.0, SCENE_CZ + rc.r * Math.sin(ang))
        });
      });
    });

    const GIS_CAT_STYLES = {
      education: { icon: "🎓", label: "מוסד חינוך / בית ספר", hex: 0x2563eb, css: "#2563eb" },
      transport: { icon: "🚌", label: "תחבורה ציבורית ומטרו", hex: 0xd97706, css: "#d97706" },
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
      if (!poi) {
        gisActiveCard.style.display = 'none';
        return;
      }
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
            <span>מסלול ב-Google Maps</span>
            <span>↗</span>
          </a>
          <a href="kitroni37_39_spatial_map.html" target="_blank" style="display:flex;align-items:center;justify-content:center;gap:4px;padding:7px 8px;border-radius:8px;background:#334155;color:#38bdf8;font-size:11px;font-weight:800;text-decoration:none;">
            <span>מפת GIS דו-ממדית</span>
            <span>↗</span>
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
      const lineMat = new THREE.LineBasicMaterial({ color: st.hex, transparent: true, opacity: 0.82 });
      subGrp.add(new THREE.Line(lineGeom, lineMat));

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
      badgeEl.addEventListener('click', ev => {
        ev.stopPropagation();
        focusCameraOnGisPoi(poi);
      });
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
          if (!gisPoisVisible) {
            gisPoisVisible = true;
            syncGisPoisState();
          }
          focusCameraOnGisPoi(poi);
        });
        gisSidebarList.appendChild(sidebarRow);
      }

      gisPoiLabelObjs.push({
        el: badgeEl,
        sidebarRow,
        poi,
        subGrp,
        pos: new THREE.Vector3(p3d.x, beaconH + 4.5, p3d.z)
      });
    });

    // Exterior Callout Pills for Kitroni 37 & 39
    const labelsContainer = document.getElementById('labels-container');
    const exteriorCallouts = [
      { text: "בניין 37 (צפוני) · 30 דירות · גג +35.16", pos: new THREE.Vector3(2.5, 35.8, -18.2), cls: "b37" },
      { text: "בניין 39 (דרומי) · 33 דירות · גג +35.16", pos: new THREE.Vector3(2.5, 35.8, 1.3),   cls: "b39" },
      { text: "רחוב קיטרוני 37–39 (חזית מערבית)",         pos: new THREE.Vector3(-21.0, 0.8, -8.5), cls: "street" },
      { text: "מרווח בין הבניינים: 6.35 מ' (635 ס\"מ)",    pos: new THREE.Vector3(-12.0, 2.2, -8.1), cls: "" }
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
    // 7. 63-UNIT 3D CATALOG & LIVE CRM, PDF QUOTE GENERATOR
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
    let hoveredUnitObj = null;

    function formatILS(n) {
      return '₪' + n.toLocaleString('he-IL');
    }

    function updateUnit3DVisualState() {
      unitVolumeMeshes.forEach(m => {
        const u = m.userData.unit;
        const isSel = selectedUnitObj && selectedUnitObj.id === u.id;
        const isHov = hoveredUnitObj && hoveredUnitObj.id === u.id;
        if (isSel) {
          m.material.color.setHex(0xfbbf24);
          m.material.opacity = 0.65;
        } else if (isHov) {
          m.material.color.setHex(u.status === 'available' ? 0x10b981 : 0x64748b);
          m.material.opacity = u.status === 'available' ? 0.58 : 0.38;
        } else {
          m.material.color.setHex(u.status === 'available' ? 0x10b981 : 0x64748b);
          m.material.opacity = selectedUnitObj ? (m.userData.baseOpacity * 0.55) : m.userData.baseOpacity;
        }
      });
    }

    function setHoveredUnit(u) {
      if (hoveredUnitObj === u) return;
      hoveredUnitObj = u;
      updateUnit3DVisualState();
      if (!camState.walkMode && !camState.isDragging && !camState.isPanning) {
        canvas.style.cursor = u ? 'pointer' : (camState.panModeActive ? 'move' : 'grab');
      }
      unitBadgeObjs.forEach(b => {
        if (b.rowPriceEl && b.rowStatusDotEl) {
          const isHov = (u && b.unit.id === u.id);
          b.rowPriceEl.style.display = isHov ? 'block' : 'none';
          b.rowStatusDotEl.style.display = isHov ? 'none' : 'inline-flex';
        }
      });
    }

    KITRONI_UNITS.forEach(u => {
      const [x0, y0, x1, y1] = u.bbox;
      const w = Math.abs(x1 - x0);
      const d = Math.abs(y1 - y0);
      const h = Math.abs(u.z1 - u.z0) - 0.14;
      const isAvail = (u.status === 'available');
      const colHex = isAvail ? 0x10b981 : 0x64748b;

      const geo = new THREE.BoxGeometry(w + 0.20, h, d + 0.20);
      const mat = new THREE.MeshBasicMaterial({
        color: colHex,
        transparent: true,
        opacity: isAvail ? 0.36 : 0.22,
        side: THREE.DoubleSide,
        depthWrite: false
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
      badge.style.cssText = 'position:absolute;transform:translate(-50%,-115%);pointer-events:none;padding:5px 11px;border-radius:999px;font-size:11.5px;font-weight:900;color:#ffffff;box-shadow:0 8px 20px rgba(0,0,0,0.42);white-space:nowrap;display:none;align-items:center;gap:6px;border:2px solid #ffffff;z-index:30;';
      badge.style.background = isAvail ? '#059669' : '#475569';
      const priceText = (showUnitPrices && isAvail) ? ('· ' + formatILS(u.price)) : (isAvail ? '· זמין לשיווק' : '· דירת בעלים');
      badge.innerHTML = `<span>${u.shortBadge} (${u.rooms} חד')</span><span class="ubadge-price" style="color:#fde047;">${priceText}</span>`;
      unitsLabelsContainer.appendChild(badge);
      unitBadgeObjs.push({ unit: u, mesh, el: badge, pos: pos3D, rowPriceEl: null, rowStatusDotEl: null });
    });

    function unitMatchesFilters(u) {
      if (activeUnitBldgFilter !== 'all' && String(u.bldg) !== activeUnitBldgFilter) return false;
      if (activeUnitStatusFilter !== 'all' && u.status !== activeUnitStatusFilter) return false;
      if (activeUnitRoomFilter !== 'all' && String(u.rooms) !== activeUnitRoomFilter) return false;
      return true;
    }

    function renderUnitsCatalogList() {
      const listEl = document.getElementById('units-catalog-list');
      if (!listEl) return;
      listEl.innerHTML = '';

      KITRONI_UNITS.forEach(u => {
        const match = unitMatchesFilters(u);
        const itemObj = unitBadgeObjs.find(b => b.unit.id === u.id);
        if (itemObj) {
          itemObj.mesh.visible = match;
          itemObj.rowPriceEl = null;
          itemObj.rowStatusDotEl = null;
          const prSpan = itemObj.el.querySelector('.ubadge-price');
          if (prSpan) {
            prSpan.textContent = (showUnitPrices && u.status === 'available')
              ? `· ${formatILS(u.price)}`
              : (u.status === 'available' ? '· זמין לשיווק' : '· דירת בעלים');
          }
        }
        if (!match) return;

        const row = document.createElement('div');
        const isSel = selectedUnitObj && selectedUnitObj.id === u.id;
        const isAvail = u.status === 'available';
        row.style.cssText = `display:flex;align-items:center;justify-content:space-between;padding:7px 9px;border-radius:10px;border:1px solid ${isSel ? '#059669' : (isAvail ? '#a7f3d0' : '#e2e8f0')};background:${isSel ? '#ecfdf5' : (isAvail ? '#f0fdf4' : '#f8fafc')};cursor:pointer;transition:all 0.12s ease;`;
        const badgeCls = isAvail ? 'status-available' : 'status-owner';
        const hoverPriceStr = (showUnitPrices && isAvail) ? formatILS(u.price) : (isAvail ? 'זמין · לפרטים' : 'דירת בעלים');

        row.innerHTML = `
          <div style="display:flex;align-items:center;gap:8px;">
            <div style="width:36px;height:34px;border-radius:8px;background:${isAvail ? '#059669' : '#475569'};color:#ffffff;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:900;font-size:10.5px;line-height:1.05;">
              <span>ב'${u.bldg}</span>
              <span style="font-size:9.5px;color:#fde047;">#${u.aptNum}</span>
            </div>
            <div>
              <div style="display:flex;align-items:center;gap:5px;">
                <span style="font-size:12px;font-weight:800;color:#0f172a;">${u.floorLabel} · ${u.rooms} חד'</span>
                <span class="status-badge ${badgeCls}">${isAvail ? 'זמין · קולסקי' : 'בעלים'}</span>
              </div>
              <div style="font-size:10px;color:#475569;font-weight:600;">${u.area} מ"ר + ${u.balcony} מ"ר מרפסת · ${u.directions}</div>
            </div>
          </div>
          <div style="text-align:left;min-width:92px;display:flex;flex-direction:column;align-items:flex-end;">
            <div class="row-status-only" style="display:inline-flex;align-items:center;gap:5px;font-size:10.5px;font-weight:800;color:${isAvail ? '#059669' : '#64748b'};">
              <span style="width:10px;height:10px;border-radius:999px;background:${isAvail ? '#10b981' : '#64748b'};display:inline-block;box-shadow:0 0 0 2px ${isAvail ? '#a7f3d0' : '#cbd5e1'};"></span>
              <span>${isAvail ? 'פנוי' : 'בעלים'}</span>
            </div>
            <div class="row-hover-price" style="display:none;font-size:12.5px;font-weight:900;color:#0f172a;background:#fef3c7;padding:1px 6px;border-radius:5px;border:1px solid #f59e0b;">${hoverPriceStr}</div>
            <div style="font-size:9px;color:#059669;font-weight:800;margin-top:2px;">כרטיס + PDF ◂</div>
          </div>
        `;
        if (itemObj) {
          itemObj.rowPriceEl = row.querySelector('.row-hover-price');
          itemObj.rowStatusDotEl = row.querySelector('.row-status-only');
        }
        row.addEventListener('pointerenter', () => {
          setHoveredUnit(u);
        });
        row.addEventListener('pointerleave', () => {
          if (hoveredUnitObj && hoveredUnitObj.id === u.id) setHoveredUnit(null);
        });
        row.addEventListener('click', () => {
          selectUnitAndOpenCard(u, true);
        });
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
      if (drwBtn) {
        drwBtn.textContent = units3DVisible ? '🏢 סימון דירות 3D: פעיל' : '🏢 הדגש דירות 3D על הבניינים';
      }
      if (!units3DVisible) {
        hoveredUnitObj = null;
        unitBadgeObjs.forEach(b => { b.el.style.display = 'none'; });
      }
    }

    function selectUnitAndOpenCard(u, flyTo = true) {
      selectedUnitObj = u;
      units3DVisible = true;
      syncUnits3DToggleUI();
      updateUnit3DVisualState();
      renderUnitsCatalogList();

      if (flyTo) {
        if (camState.walkMode) exitWalkthrough();
        selectFloor('all');
        const cx = 0.5 * (u.bbox[0] + u.bbox[2]);
        const cy = 0.5 * (u.bbox[1] + u.bbox[3]);
        camState.target.set(cx, u.bz, cy);
        camState.spherical.radius = 42.0;
        camState.spherical.phi = 1.08;
        camState.spherical.theta = (u.bx < 0) ? -2.45 : 0.65;
        updateCameraFromOrbit();
      }

      const badgeCls = u.status === 'available' ? 'status-available' : 'status-owner';
      const downPayment20 = Math.round(u.price * 0.20);
      const balance80 = u.price - downPayment20;
      const estMonthlyMortgage = Math.round((u.price * 0.55) * 0.0055);

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
            <div style="font-size:10px;color:#94a3b8;">שטח פנים (פלדלת)</div>
            <div style="font-size:14px;font-weight:900;color:#38bdf8;">${u.area} מ"ר</div>
          </div>
          <div style="background:#1e293b;border:1px solid #334155;border-radius:8px;padding:6px;">
            <div style="font-size:10px;color:#94a3b8;">מרפסת שמש/גג</div>
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
            <span style="color:#94a3b8;">חניה תת-קרקעית צמודה:</span>
            <span style="font-weight:800;color:#6ee7b7;">חניה #${u.parkingNum} (מפלס -3.85)</span>
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
            🚗 הצג חניה #${u.parkingNum} במרתף
          </button>
          <button id="btn-card-pdf-offer" class="ui-btn" style="background:#059669;color:#ffffff;border-color:#10b981;font-weight:800;">
            📄 הצעת מחיר PDF
          </button>
        </div>
      `;

      document.getElementById('btn-close-unit-card').addEventListener('click', () => {
        unitSalesCard.style.display = 'none';
      });
      document.getElementById('btn-card-enter-tour').addEventListener('click', () => {
        closeAllDrawers();
        setSliceMode('single');
        selectFloor(u.floorId);
        const cx = 0.5 * (u.bbox[0] + u.bbox[2]);
        const cy = 0.5 * (u.bbox[1] + u.bbox[3]);
        startWalkthroughAt(cx, u.z0 + 1.68, cy, (u.bx < 0) ? -1.57 : 1.57, `${u.name} · ${u.typeHe}`, u.floorLabel);
      });
      document.getElementById('btn-card-balcony-view').addEventListener('click', () => {
        closeAllDrawers();
        selectFloor('all');
        const [bx, by] = u.balcPt;
        const yaw = (u.lookDir === 'W') ? -Math.PI / 2 : Math.PI / 2;
        startWalkthroughAt(bx, u.z0 + 1.68, by, yaw, `נוף מהמרפסת — ${u.name} (גובה +${u.z0.toFixed(2)} מ')`, u.floorLabel);
      });
      document.getElementById('btn-card-show-parking').addEventListener('click', () => {
        closeAllDrawers();
        if (camState.walkMode) exitWalkthrough();
        setSliceMode('single');
        selectFloor('mar');
        if (parkingHighlightMesh) {
          parkingHighlightMesh.visible = true;
          parkingHighlightMesh.position.set(u.parkingX, -3.10, u.parkingY);
        }
        camState.target.set(u.parkingX, -3.5, u.parkingY);
        camState.spherical = { radius: 24.0, phi: 0.62, theta: -1.8 };
        updateCameraFromOrbit();
      });
      document.getElementById('btn-card-pdf-offer').addEventListener('click', () => {
        printUnitOfferPDF(u);
      });
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
  <title>הצעת מחיר ומפרט טכני — ${u.name} · קיטרוני 37–39 פתח תקווה</title>
  <style>
    body { font-family: 'Segoe UI', Tahoma, Arial, sans-serif; margin: 0; padding: 28px; color: #0f172a; background: #ffffff; }
    .hdr { display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #1e3a8a; padding-bottom: 14px; margin-bottom: 18px; }
    .brand-box { display: flex; align-items: center; gap: 12px; }
    .logo { width: 58px; height: 52px; border-radius: 12px; background: #0f172a; color: #fde047; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 15px; }
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
      <div class="logo">K37-39</div>
      <div>
        <div style="font-size:20px;font-weight:900;color:#0f172a;">יצחק קולסקי חברה לבניה והשקעות בע"מ</div>
        <div style="font-size:13px;color:#475569;font-weight:700;">פרויקט בוטיק קיטרוני 37–39, פתח תקווה · אדריכלות: אילת קורן אדריכלים</div>
      </div>
    </div>
    <div style="text-align:left;font-size:12px;color:#475569;">
      <div><b>תאריך הפקה:</b> ${todayStr}</div>
      <div><b>גוש 6375 חלקות 237–238</b> · 63 יח"ד</div>
    </div>
  </div>

  <div class="grid">
    <div class="kpi"><div class="kpi-lbl">בניין ומספר דירה</div><div class="kpi-val">${u.name}</div></div>
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
        <tr><td><b>חניה תת-קרקעית בטאבו:</b></td><td>חניה מקורה #${u.parkingNum} במפלס מרתף החניון (-3.85 מ')</td></tr>
        <tr><td><b>מפרט פנים יוקרתי:</b></td><td>ריצוף גרניט פורצלן 100×100/80×80, מטבח יוקרה, תריסי אור חשמליים, הכנה למיזוג VRF</td></tr>
        <tr><td><b>תנאי תשלום יזמיים (20/80):</b></td><td>20% בחתימה (${formatILS(down20)}) · 80% במסירת חזקה (${formatILS(bal80)})</td></tr>
        <tr><td><b>נגישות תחבורתית ומוקדי סביבה:</b></td><td>כ-640 מ' לתחנת מטרו עיריית פ"ת (קו M2), מוסדות חינוך וגינות במרחק הליכה קצר</td></tr>
      </table>
    </div>
    <div class="box" style="display:flex;flex-direction:column;justify-content:space-between;">
      <div style="font-size:13px;font-weight:800;color:#0f172a;margin-bottom:6px;">📸 הדמיית המודל התלת-ממדי (1:50 CAD):</div>
      <img src="${snapshotDataUrl}" style="width:100%;height:220px;object-fit:cover;border-radius:8px;border:1px solid #cbd5e1;" />
      <div style="font-size:10px;color:#64748b;margin-top:6px;">* ההדמיה והמחירים להמחשה שיווקית בלבד וכפופים להסכם המכר המלא ולמפרט הטכני החתום של קבוצת קולסקי.</div>
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
      target: new THREE.Vector3(0.2, 8.0, -9.2),
      spherical: { radius: 520.0, phi: 0.60, theta: -2.98 },
      isDragging: false,
      isPanning: false,
      downX: 0,
      downY: 0,
      prevX: 0,
      prevY: 0,
      walkMode: false,
      yaw: 0,
      pitch: 0,
      keys: {}
    };

    const VIEW_PRESETS = {
      iso_west:       { theta: -2.42, phi: 1.08, radius: 66.0,   target: [2.5, 14.0, -8.5], ortho: false, clip: 36.0 },
      iso_east:       { theta: 0.62,  phi: 1.08, radius: 66.0,   target: [2.5, 14.0, -8.5], ortho: false, clip: 36.0 },
      gmaps_regional: { theta: -2.98, phi: 0.56, radius: 1350.0, target: [0.2, 6.0, -9.2],  ortho: false, clip: 36.0 },
      gmaps_aerial:   { theta: -2.98, phi: 0.60, radius: 520.0,  target: [0.2, 6.0, -9.2],  ortho: false, clip: 36.0 },
      gmaps_close:    { theta: -2.98, phi: 0.66, radius: 175.0,  target: [0.2, 8.0, -9.2],  ortho: false, clip: 36.0 },
      top_plan:       { theta: -Math.PI/2, phi: 0.04, radius: 54.0, target: [2.5, 13.5, -8.5], ortho: true, clip: 15.8 }
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
      orthoCam.zoom = 48.0 / radius;
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
      setClipHeight(36.0);
      setOrthoMode(false);
      camState.target.set(2.5, fObj.zFloor + 1.0, -8.5);
      camState.spherical.radius = 42.0;
      camState.spherical.phi = 0.56;
      camState.spherical.theta = -Math.PI * 0.58;
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

    function startPresetInteriorTour(bldg, floorNum, wing) {
      closeAllDrawers();
      const u = KITRONI_UNITS.find(x => x.bldg === bldg && x.floorNum === floorNum && x.wing === wing) || KITRONI_UNITS[0];
      selectedUnitObj = u;
      setSliceMode('single');
      selectFloor(u.floorId);
      const cx = 0.5 * (u.bbox[0] + u.bbox[2]);
      const cy = 0.5 * (u.bbox[1] + u.bbox[3]);
      startWalkthroughAt(cx, u.z0 + 1.68, cy, (u.bx < 0) ? -1.57 : 1.57, `${u.name} · ${u.typeHe} (${u.area}+${u.balcony} מ"ר)`, u.floorLabel);
    }

    function teleportInTour(x, z, yawRad, labelTxt) {
      const activeF = FLOORS.find(f => f.id === currentFloorId && f.zFloor >= 0) || FLOORS[5];
      if (!camState.walkMode) {
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
      const bx = (flrNum === 9) ? -12.2 : -14.85;
      startWalkthroughAt(bx, fObj.zFloor + 1.68, -21.3, -Math.PI / 2, `🔭 נוף פנורמי מהמרפסת — קומה ${flrNum} (מפלס +${fObj.zFloor.toFixed(2)} מ')`, fObj.label);
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
        if (!wasOpen) {
          drawer.classList.add('open');
          btn.classList.add('open');
        }
      });
    });

    document.querySelectorAll('[data-close-drawer]').forEach(btn => {
      btn.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();
        closeAllDrawers();
      });
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

    // Wire Walkthrough D-Pad buttons
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

    // Wire Orbit 3D Navigation Pad (Right / Left / Up / Down / Elevation / Zoom / Pan Mode Toggle)
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
        camState.target.set(2.5, activeF ? activeF.zFloor + 1.2 : 12.0, -8.5);
      }
      camState.target.y = Math.max(-8.0, Math.min(95.0, camState.target.y));
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

    // Top view buttons
    document.querySelectorAll('.view-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activatePreset(btn.dataset.view);
      });
    });

    // GIS Radii & POIs toggles
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
        if (item.sidebarRow) {
          item.sidebarRow.style.display = catMatch ? 'flex' : 'none';
        }
      });
      if (!gisPoisVisible) gisActiveCard.style.display = 'none';
      const topBtn = document.getElementById('btn-top-pois');
      const sideBtn = document.getElementById('btn-side-pois');
      if (topBtn) {
        topBtn.textContent = gisPoisVisible ? '📍 מיקומים: פעיל' : '📍 מיקומים: כבוי';
        topBtn.className = gisPoisVisible ? 'ui-btn active' : 'ui-btn';
      }
      if (sideBtn) {
        sideBtn.textContent = gisPoisVisible ? '📍 מיקומים (46): פעיל' : '📍 מיקומים (46): כבוי';
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

    // CRM Filters & Toggles
    document.getElementById('btn-top-units-3d').addEventListener('click', () => {
      units3DVisible = !units3DVisible;
      if (units3DVisible && camState.spherical.radius > 160) activatePreset('iso_west');
      syncUnits3DToggleUI();
    });
    document.getElementById('btn-drawer-units-3d').addEventListener('click', () => {
      units3DVisible = !units3DVisible;
      if (units3DVisible && camState.spherical.radius > 160) activatePreset('iso_west');
      syncUnits3DToggleUI();
    });
    document.getElementById('btn-toggle-prices').addEventListener('click', function() {
      showUnitPrices = !showUnitPrices;
      this.textContent = showUnitPrices ? '👁️ מחירים: מוצג' : '👁️ מחירים: מוסתר';
      this.className = showUnitPrices ? 'ui-btn active' : 'ui-btn';
      renderUnitsCatalogList();
      if (selectedUnitObj && unitSalesCard.style.display === 'block') {
        selectUnitAndOpenCard(selectedUnitObj, false);
      }
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

    // Finish Packages & Settings
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
        ? '🗺️ מפת לוויין Google Maps (קיטרוני 37–39): פעיל'
        : '🗺️ מפת לוויין Google Maps (קיטרוני 37–39): כבוי';
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

    // Sun Slider
    const sunSlider = document.getElementById('sun-slider');
    const sunVal = document.getElementById('sun-val');
    sunSlider.addEventListener('input', () => {
      const deg = parseFloat(sunSlider.value);
      const rad = deg * Math.PI / 180;
      dirLight.position.set(-55 * Math.cos(rad), 65 * Math.sin(rad) + 15, 42 * Math.sin(rad * 1.2));
      const hour = Math.round(7 + (deg / 180) * 11);
      sunVal.textContent = `~${hour}:00`;
    });

    // Night Mode
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
        MATS.winGlass.emissive.setHex(0x000000);
        MATS.winGlass.emissiveIntensity = 0.0;
        MATS.winGlass.opacity = 0.42;
      }
    });

    // 3D Laser Tape Measure
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

    // Section Clip Height Slider & Floor Buttons
    const clipSlider = document.getElementById('clip-slider');
    const clipVal = document.getElementById('clip-val');

    function setClipHeight(v) {
      clipSlider.value = v;
      clipPlane.constant = v;
      clipVal.textContent = v >= 35.6 ? "+36.00 מ' (מלא)" : `${v >= 0 ? '+' : ''}${v.toFixed(2)} מ' (חתך)`;
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
      currentFloorId = floorId;
      document.querySelectorAll('#floor-buttons .ui-btn').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('fbtn-' + floorId);
      if (activeBtn) activeBtn.classList.add('active');

      if (parkingHighlightMesh && floorId !== 'mar') parkingHighlightMesh.visible = false;
      gisMapPlanesGroup.visible = gmapsVisible && (floorId !== 'mar');

      if (floorId === 'all') {
        document.getElementById('active-floor-label').textContent = 'מבנה שלם (כל הקומות)';
        FLOORS.forEach(f => { floorGroups[f.id].visible = true; });
        setClipHeight(36.0);
        return;
      }

      const idx = FLOORS.findIndex(f => f.id === floorId);
      const fObj = FLOORS[idx];
      document.getElementById('active-floor-label').textContent = `${fObj.label} (${fObj.elevText} מ')`;
      FLOORS.forEach((f, i) => {
        floorGroups[f.id].visible = (sliceMode === 'single') ? (i === idx) : (i <= idx);
      });
    }

    function toggleLayer(layerId, isVis) {
      (layerObjects[layerId] || []).forEach(obj => { obj.visible = isVis; });
    }

    // Populate Floor Buttons & Layer Checkboxes
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
            camState.target.set(2.5, Math.max(-2, f.zFloor), -8.5);
            camState.spherical.radius = 52.0;
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
        if (currentFloorId === 'all') { setSliceMode('single'); selectFloor('f3'); }
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

    // Export .OBJ
    document.getElementById('btn-export-obj').addEventListener('click', () => {
      let objLines = ['# Kitroni 37-39 Petah Tikva - 1:1 Metric Architectural BIM Model (Meters)'];
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
      a.download = 'kitroni37_39_model.obj';
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
        camState.target.y = Math.max(-8.0, Math.min(95.0, camState.target.y));
        updateCameraFromOrbit();
      } else if (units3DVisible && !isMeasureMode) {
        const rect = canvas.getBoundingClientRect();
        mouseNDC.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
        mouseNDC.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
        raycaster.setFromCamera(mouseNDC, activeCam);
        const visMeshes = unitVolumeMeshes.filter(m => m.visible && m.position.y <= clipPlane.constant);
        const uHits = raycaster.intersectObjects(visMeshes, false);
        const hitUnit = (uHits.length > 0 && uHits[0].object.userData.unit) ? uHits[0].object.userData.unit : null;
        setHoveredUnit(hitUnit);
      }
    });

    canvas.addEventListener('pointerleave', () => {
      if (hoveredUnitObj) setHoveredUnit(null);
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
      if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'PageUp', 'PageDown'].includes(e.code)) {
        e.preventDefault();
      }
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

    // Start on Aerial Overview showing the 3D Kitroni 37-39 buildings sitting on the Petah Tikva Google Maps + Distance Rings + POIs!
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
        // Orbit Mode Keyboard Panning (Right / Left / Up / Down / Elevation)
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
          camState.target.y = Math.max(-8.0, Math.min(95.0, camState.target.y));
          updateCameraFromOrbit();
        }
      }

      renderer.render(scene, activeCam);

      const w = window.innerWidth, h = window.innerHeight;

      // 1. Exterior Callout Pills
      calloutObjs.forEach(c => {
        if (camState.walkMode || !showLabels || c.pos.y > clipPlane.constant) {
          c.el.style.opacity = '0';
          return;
        }
        const p = c.pos.clone().project(activeCam);
        if (p.z > 1 || p.z < -1) { c.el.style.opacity = '0'; return; }
        const sx = (p.x * 0.5 + 0.5) * w;
        const sy = (-p.y * 0.5 + 0.5) * h;
        c.el.style.left = `${sx}px`;
        c.el.style.top = `${sy}px`;
        c.el.style.opacity = '1';
      });

      // 2. 3D GIS Distance Ring Badges
      gisRingLabelObjs.forEach(rl => {
        if (camState.walkMode || !gisRadiiVisible || currentFloorId === 'mar') {
          rl.el.style.display = 'none';
          return;
        }
        const p = rl.pos.clone().project(activeCam);
        if (p.z > 1 || p.z < -1) { rl.el.style.display = 'none'; return; }
        const sx = (p.x * 0.5 + 0.5) * w;
        const sy = (-p.y * 0.5 + 0.5) * h;
        if (sx < -60 || sx > w + 60 || sy < 50 || sy > h + 30) { rl.el.style.display = 'none'; return; }
        rl.el.style.display = 'block';
        rl.el.style.left = `${sx}px`;
        rl.el.style.top = `${sy}px`;
      });

      // 3. 28 GIS POI Location Badges
      gisPoiLabelObjs.forEach(pl => {
        const catMatch = (activeGisCategory === 'all' || pl.poi.cat === activeGisCategory);
        if (camState.walkMode || !gisPoisVisible || !catMatch || currentFloorId === 'mar') {
          pl.el.style.display = 'none';
          return;
        }
        const p = pl.pos.clone().project(activeCam);
        if (p.z > 1 || p.z < -1) { pl.el.style.display = 'none'; return; }
        const sx = (p.x * 0.5 + 0.5) * w;
        const sy = (-p.y * 0.5 + 0.5) * h;
        if (sx < -80 || sx > w + 80 || sy < 50 || sy > h + 30) { pl.el.style.display = 'none'; return; }
        pl.el.style.display = 'flex';
        pl.el.style.left = `${sx}px`;
        pl.el.style.top = `${sy}px`;
      });

      // 4. 3D Interactive 63-Unit Badges — ONLY shown when hovering with the mouse over that specific apartment!
      unitBadgeObjs.forEach(ub => {
        const isHovered = (hoveredUnitObj && ub.unit.id === hoveredUnitObj.id);
        if (camState.walkMode || !units3DVisible || !isHovered || !ub.mesh.visible || ub.pos.y > clipPlane.constant) {
          ub.el.style.display = 'none';
          return;
        }
        const p = ub.pos.clone().project(activeCam);
        if (p.z > 1 || p.z < -1) { ub.el.style.display = 'none'; return; }
        const sx = (p.x * 0.5 + 0.5) * w;
        const sy = (-p.y * 0.5 + 0.5) * h;
        if (sx < -60 || sx > w + 60 || sy < 50 || sy > h + 30) { ub.el.style.display = 'none'; return; }
        ub.el.style.display = 'inline-flex';
        ub.el.style.left = `${sx}px`;
        ub.el.style.top = `${sy}px`;
      });

      // 5. 3D Laser Measurement Badges
      measureBadges.forEach(mb => {
        const p = mb.pos.clone().project(activeCam);
        if (p.z > 1 || p.z < -1) { mb.el.style.display = 'none'; return; }
        const sx = (p.x * 0.5 + 0.5) * w;
        const sy = (-p.y * 0.5 + 0.5) * h;
        mb.el.style.display = 'block';
        mb.el.style.left = `${sx}px`;
        mb.el.style.top = `${sy}px`;
      });
    }
    animate();
  </script>
</body>
</html>
"""

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

out_workspace_model = os.path.join(WORKSPACE, "kitroni37_39_3d_model.html")
out_workspace_index = os.path.join(WORKSPACE, "index.html")
out_artifact_model = os.path.join(ARTIFACT_DIR, "kitroni37_39_3d_model.html")

for p in [out_workspace_model, out_workspace_index, out_artifact_model]:
    with open(p, "w", encoding="utf-8") as f:
        f.write(html_out)
    print("Wrote:", p, "Size:", os.path.getsize(p))
