import os
import json
import base64

THREE_JS_PATH = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\_shared_engine\three.min.js"
EXTRACTED_PLANS_PATH = r"C:\Users\User\.gemini\antigravity\brain\60b6f7e6-94a5-48b9-b12c-1728c4428342\scratch\extracted_interior_plans.json"
UNIFIED_MAP_PATH = r"C:\Users\User\.gemini\antigravity\brain\60b6f7e6-94a5-48b9-b12c-1728c4428342\scratch\unified_3d_map.json"
SPATIAL_DATA_PATH = r"C:\Users\User\.gemini\antigravity\brain\60b6f7e6-94a5-48b9-b12c-1728c4428342\scratch\spatial_map_data.json"
OUT_WORKSPACE_HTML = r"C:\Users\User\.gemini\antigravity\scratch\pines-48-3d\index.html"

with open(THREE_JS_PATH, "r", encoding="utf-8") as f:
    three_js_code = f.read()

with open(EXTRACTED_PLANS_PATH, "r", encoding="utf-8") as f:
    extracted_plans_data = json.load(f)

with open(UNIFIED_MAP_PATH, "r", encoding="utf-8") as f:
    unified_map_data = json.load(f)
wide_gmaps_data_uri = unified_map_data["outer_z15"]["data_uri"]
inner_gmaps_data_uri = unified_map_data["inner_z17"]["data_uri"]
closeup_gmaps_data_uri = unified_map_data["closeup_z19"]["data_uri"]

with open(SPATIAL_DATA_PATH, "r", encoding="utf-8") as f:
    spatial_data = json.load(f)
spatial_pois_json = json.dumps(spatial_data["pois"], ensure_ascii=False, separators=(",", ":"))

extracted_plans_json = json.dumps(extracted_plans_data, separators=(",", ":"))

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>פינס 48, פתח תקוה — מודל אדריכלי תלת-מימדי מלא (חוץ + תכנון פנים 1:50 CAD)</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
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
      width: 350px;
      max-height: calc(100vh - 290px);
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
    .ui-btn-cut {
      background: #eff6ff;
      border-color: #93c5fd;
      color: #1e40af;
    }
    .ui-btn-cut:hover {
      background: #dbeafe;
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
      font-size: 12px;
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
    .callout-pill.apt-b { background: #2563eb; color: #ffffff; border-color: #1d4ed8; }
    .callout-pill.apt-a { background: #059669; color: #ffffff; border-color: #047857; }
    .callout-pill.apt-c { background: #d97706; color: #ffffff; border-color: #b45309; }
    .callout-pill.core  { background: #1e293b; color: #ffffff; border-color: #0f172a; }
    .cad-badge {
      font-variant-numeric: tabular-nums;
    }
    input[type="range"] {
      width: 100%;
      cursor: pointer;
      accent-color: #2563eb;
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
    .menu-trigger-btn.royal-trigger {
      background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
      border-color: #1e40af;
      color: #ffffff;
    }
    .menu-trigger-btn.royal-trigger:hover {
      background: linear-gradient(135deg, #172554 0%, #1e3a8a 100%);
    }
    .menu-trigger-btn.royal-trigger.open {
      box-shadow: 0 0 0 2px #93c5fd, 0 4px 12px rgba(37, 99, 235, 0.35);
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
    .status-shared    { background: #fef3c7; color: #92400e; border: 1px solid #fde047; }
    .status-owner     { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }
    .unit-sales-card {
      display: none;
      position: absolute;
      top: 72px;
      left: 16px;
      z-index: 29;
      width: 375px;
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
    .modal-backdrop {
      display: none;
      position: fixed;
      inset: 0;
      z-index: 60;
      background: rgba(15, 23, 42, 0.68);
      backdrop-filter: blur(6px);
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .modal-backdrop.open {
      display: flex;
    }
  </style>
</head>
<body class="antialiased">
  <div id="viewport-container">
    <!-- 3D WebGL Canvas -->
    <canvas id="cad-canvas"></canvas>

    <!-- 2D Floating HTML Overlay Labels for Datum Elevations, Streets & Interior Rooms -->
    <div id="labels-container" style="pointer-events:none;position:absolute;inset:0;overflow:hidden;"></div>
    <!-- 3D Georeferenced Distance Rings & POI Location Badges Overlay -->
    <div id="gis-labels-container" style="pointer-events:none;position:absolute;inset:0;overflow:hidden;z-index:8;"></div>
    <!-- 3D Interactive Unit Badges & Laser Measure Overlay -->
    <div id="units-labels-container" style="pointer-events:none;position:absolute;inset:0;overflow:hidden;z-index:12;"></div>
    <div id="measure-labels-container" style="pointer-events:none;position:absolute;inset:0;overflow:hidden;z-index:18;"></div>

    <!-- Active Selected GIS Location Info Card -->
    <div id="gis-active-card" style="display:none;position:absolute;bottom:20px;left:20px;z-index:28;width:320px;background:rgba(15,23,42,0.96);color:#ffffff;border:1px solid #334155;border-radius:14px;padding:14px;box-shadow:0 12px 28px rgba(0,0,0,0.35);backdrop-filter:blur(10px);"></div>

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
        <div style="display:flex;height:36px;width:36px;align-items:center;justify-content:center;border-radius:9px;background:linear-gradient(135deg,#0f172a,#1e3a8a);color:#fde047;font-weight:900;font-size:12px;border:1px solid #3b82f6;">
          K48
        </div>
        <div>
          <div style="display:flex;align-items:center;gap:7px;flex-wrap:wrap;">
            <h1 style="margin:0;font-size:14px;font-weight:800;color:#0f172a;">קבוצת קולסקי · פינס 48 פינת הבעל שם טוב, פ"ת</h1>
            <span style="border-radius:6px;border:1px solid #dec9ad;background:#fef3c7;padding:1px 7px;font-size:10px;font-weight:800;color:#92400e;">נחומי אדריכלים · פורטל שיווק ומכירות 3D</span>
          </div>
        </div>
      </div>

      <!-- Streamlined Marketing Action Bar & On-Demand Dropdown Triggers (All menus closed by default) -->
      <div style="display:flex;flex-wrap:wrap;align-items:center;gap:5px;" id="view-buttons">
        <!-- Quick Primary Camera Views -->
        <button data-view="iso_ne" class="view-btn ui-btn" title="מבט חוץ אדריכלי מלא על הבניין">
          🏢 מבט הבניין
        </button>
        <button data-view="gmaps_regional" id="btn-top-gis-map" class="view-btn ui-btn active" style="background:#1e3a8a;color:#ffffff;border-color:#1d4ed8;font-weight:700;">
          🗺️ מפת סביבה
        </button>

        <!-- Quick One-Click Toggles for 3D Unit Volumes, Radii, POIs, Night Mode & Laser Measure -->
        <button id="btn-top-units-3d" class="ui-btn" style="border-color:#10b981;color:#065f46;background:#ecfdf5;font-weight:800;" title="הצג/הסתר סימון דירות תלת-ממדי לפי זמינות ומחיר על חזית הבניין">
          🏢 סימון דירות 3D
        </button>
        <button id="btn-top-radii" class="ui-btn active" title="הדלק/כבה מעגלי מרחק סביב הבניין">
          ⭕ רדיוסים: פעיל
        </button>
        <button id="btn-top-pois" class="ui-btn active" title="הדלק/כבה מיקומים ומוקדי סביבה סביב הבניין">
          📍 מיקומים: פעיל
        </button>
        <button id="btn-top-night" class="ui-btn" title="מצב תאורת לילה / שעת הזהב עם תאורת פנים ומרפסות חמה">
          🌙 מצב לילה
        </button>
        <button id="btn-top-measure" class="ui-btn" title="מד טווח לייזר תלת-ממדי למדידת מרחקים בדירה ובבניין">
          📏 מדידה
        </button>

        <!-- On-Demand Popover Triggers (Closed by default, open on click) -->
        <button data-drawer="drawer-units" class="menu-trigger-btn emerald-trigger">
          <span>🏷️ קטלוג דירות ומחירים (17)</span>
          <span style="font-size:10px;">▾</span>
        </button>
        <button data-drawer="drawer-apartments" class="menu-trigger-btn lux-trigger">
          <span>✨ סיור בדירות (A/B/C/פנטהאוז)</span>
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

    <!-- ===================================================================== -->
    <!-- ON-DEMAND POPOVER DRAWER 0: 17 UNITS CATALOG & LIVE CRM (CLOSED BY DEFAULT) -->
    <!-- ===================================================================== -->
    <div id="drawer-units" class="glass-panel dropdown-drawer" style="width:410px;">
      <div class="flex-between" style="margin-bottom:8px;border-bottom:1px solid #e2e8f0;padding-bottom:6px;">
        <div>
          <div style="font-size:13px;font-weight:800;color:#065f46;">🏷️ קטלוג 17 הדירות והמחירון הרשמי — פינס 48</div>
          <div style="font-size:11px;color:#64748b;">נתוני אמת מפרוטוקול החלוקה ודוח האפס · לחץ על דירה לכרטיס מכירה ו-PDF</div>
        </div>
        <button data-close-drawer class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
      </div>

      <!-- Inventory KPI Summary -->
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin-bottom:8px;text-align:center;">
        <div style="background:#ecfdf5;border:1px solid #a7f3d0;border-radius:8px;padding:5px;">
          <div style="font-size:10px;color:#065f46;font-weight:700;">🟢 פנויות קולסקי</div>
          <div id="kpi-avail-count" style="font-size:14px;font-weight:900;color:#047857;">10 דירות</div>
        </div>
        <div style="background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:5px;">
          <div style="font-size:10px;color:#92400e;font-weight:700;">🟡 משותפות / שמורות</div>
          <div id="kpi-shared-count" style="font-size:14px;font-weight:900;color:#b45309;">2 דירות</div>
        </div>
        <div style="background:#f8fafc;border:1px solid #cbd5e1;border-radius:8px;padding:5px;">
          <div style="font-size:10px;color:#475569;font-weight:700;">🔒 בעלים / נמכרו</div>
          <div id="kpi-owner-count" style="font-size:14px;font-weight:900;color:#334155;">5 דירות</div>
        </div>
      </div>

      <!-- 3D Volume Highlight & Price Visibility Controls -->
      <div class="grid-2" style="margin-bottom:8px;">
        <button id="btn-drawer-units-3d" class="ui-btn" style="background:#059669;color:#ffffff;border-color:#047857;font-weight:800;">
          🏢 הדגש דירות 3D על הבניין
        </button>
        <button id="btn-toggle-prices" class="ui-btn active" style="font-weight:700;">
          👁️ מחירים: מוצג
        </button>
      </div>

      <!-- Smart Buyer Filters (Availability & Rooms) -->
      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:6px;" id="unit-status-filters">
        <button data-ustatus="all" class="unit-status-chip ui-btn active" style="padding:3px 8px;font-size:10px;">הכל (17)</button>
        <button data-ustatus="kuleski" class="unit-status-chip ui-btn" style="padding:3px 8px;font-size:10px;">🟢 מלאי קולסקי זמין (12)</button>
        <button data-ustatus="available" class="unit-status-chip ui-btn" style="padding:3px 8px;font-size:10px;">פנויות בלבד (10)</button>
        <button data-ustatus="owner" class="unit-status-chip ui-btn" style="padding:3px 8px;font-size:10px;">דירות בעלים (5)</button>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px;" id="unit-room-filters">
        <button data-urooms="all" class="unit-room-chip ui-btn active" style="padding:3px 8px;font-size:10px;">כל הגדלים</button>
        <button data-urooms="3" class="unit-room-chip ui-btn" style="padding:3px 8px;font-size:10px;">3 חד' · 80+12 מ"ר (B)</button>
        <button data-urooms="4" class="unit-room-chip ui-btn" style="padding:3px 8px;font-size:10px;">4 חד' · 92–94+12 מ"ר (A/C)</button>
        <button data-urooms="5" class="unit-room-chip ui-btn" style="padding:3px 8px;font-size:10px;">פנטהאוז דופלקס 5 חד' (PB/PC)</button>
      </div>

      <div id="units-catalog-list" style="max-height:265px;overflow-y:auto;display:flex;flex-direction:column;gap:5px;padding-left:2px;"></div>
    </div>

    <!-- ===================================================================== -->
    <!-- ON-DEMAND POPOVER DRAWER 1: LUXURY APARTMENTS A, B, C & PENTHOUSES TOUR (CLOSED BY DEFAULT) -->
    <!-- ===================================================================== -->
    <div id="drawer-apartments" class="glass-panel dropdown-drawer" style="width:385px;">
      <div class="flex-between" style="margin-bottom:10px;border-bottom:1px solid #e2e8f0;padding-bottom:8px;">
        <div>
          <div style="font-size:13px;font-weight:800;color:#78350f;">✨ סיור פנים יוקרתי — דירות A, B, C, פנטהאוזים ולובי</div>
          <div style="font-size:11px;color:#64748b;">כל טיפוסי הדירות מרוהטים ב-3D מלא + בחירת קומה לנוף מהמרפסת</div>
        </div>
        <button data-close-drawer class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
      </div>
      <div class="grid-2" style="margin-bottom:6px;">
        <button id="btn-enter-apta-fp" class="ui-btn ui-btn-lux">✨ סיור פנים — דירה A (4 חד')</button>
        <button id="btn-enter-apta-dollhouse" class="ui-btn ui-btn-lux">🏠 מבט-על — דירה A</button>
        <button id="btn-enter-aptb-fp" class="ui-btn ui-btn-lux">✨ סיור פנים — דירה B (3 חד')</button>
        <button id="btn-enter-aptb-dollhouse" class="ui-btn ui-btn-lux">🏠 מבט-על — דירה B</button>
        <button id="btn-enter-aptc-fp" class="ui-btn ui-btn-lux">✨ סיור פנים — דירה C (4 חד')</button>
        <button id="btn-enter-aptc-dollhouse" class="ui-btn ui-btn-lux">🏠 מבט-על — דירה C</button>
        <button id="btn-enter-pent-pb" class="ui-btn" style="background:#0f172a;color:#fde047;border-color:#334155;font-weight:800;">👑 פנטהאוז מערבי PB (ק' 6–7)</button>
        <button id="btn-enter-pent-pc" class="ui-btn" style="background:#0f172a;color:#fde047;border-color:#334155;font-weight:800;">👑 פנטהאוז מזרחי PC (ק' 6–7)</button>
      </div>
      <div class="grid-2" style="margin-bottom:8px;">
        <button id="btn-enter-f3-both" class="ui-btn ui-btn-lux">
          🏢 חתך קומה 3 (A + B + C)
        </button>
        <button id="btn-enter-lobby-fp" class="ui-btn" style="background:#f1f5f9;color:#0f172a;border-color:#94a3b8;font-weight:700;">
          🚪 לובי כניסה ראשי (0.00)
        </button>
      </div>
      <div class="section-box" style="margin-bottom:0;">
        <div style="font-size:11px;font-weight:800;color:#451a03;margin-bottom:5px;">🔭 סימולטור "נוף מהמרפסת" לפי קומה מדויקת (קומות 1–7):</div>
        <div style="display:flex;flex-wrap:wrap;gap:4px;" id="balcony-floor-selector">
          <button data-bflr="1" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 1 (+4.25)</button>
          <button data-bflr="2" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 2 (+7.31)</button>
          <button data-bflr="3" class="ui-btn active" style="padding:3px 7px;font-size:10px;">קומה 3 (+10.37)</button>
          <button data-bflr="4" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 4 (+13.43)</button>
          <button data-bflr="5" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 5 (+16.49)</button>
          <button data-bflr="6" class="ui-btn" style="padding:3px 7px;font-size:10px;">גג דופלקס 6 (+19.72)</button>
          <button data-bflr="7" class="ui-btn" style="padding:3px 7px;font-size:10px;">גג עליון 7 (+22.95)</button>
        </div>
      </div>
      <!-- Hidden duplicate IDs kept for JS compatibility -->
      <div style="display:none;">
        <button id="btn-side-apta-fp"></button>
        <button id="btn-side-apta-doll"></button>
        <button id="btn-side-aptc-fp"></button>
        <button id="btn-side-aptc-doll"></button>
      </div>
    </div>

    <!-- ===================================================================== -->
    <!-- ON-DEMAND POPOVER DRAWER 2: 3D GIS SPATIAL MAP & 28 POIS (CLOSED BY DEFAULT) -->
    <!-- ===================================================================== -->
    <div id="drawer-gis" class="glass-panel dropdown-drawer">
      <div class="flex-between" style="margin-bottom:8px;border-bottom:1px solid #e2e8f0;padding-bottom:6px;">
        <div>
          <div style="font-size:13px;font-weight:800;color:#1e3a8a;">📍 מפת מרחקים ו-28 מוקדי סביבה (Google Maps)</div>
          <div style="font-size:11px;color:#64748b;">סינון קטגוריות וטיסה ישירה לכל מוקד במפה</div>
        </div>
        <button data-close-drawer class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
      </div>
      <div class="grid-2" style="margin-bottom:8px;">
        <button id="btn-side-gis-regional" class="ui-btn active" style="background:#1e3a8a;color:#ffffff;border-color:#1d4ed8;font-weight:700;">
          🌍 כל המיקומים (2 ק"מ)
        </button>
        <button id="btn-side-gis-overview" class="ui-btn" style="background:#dbeafe;color:#1e3a8a;border-color:#93c5fd;font-weight:700;">
          🗺️ רדיוס שכונתי (1 ק"מ)
        </button>
        <button id="btn-side-gis-close" class="ui-btn" style="background:#dbeafe;color:#1e3a8a;border-color:#93c5fd;font-weight:700;">
          🏢 תקריב הצומת (300 מ')
        </button>
        <a href="pines48_spatial_map.html" target="_blank" class="ui-btn" style="background:#0f172a;color:#38bdf8;border-color:#334155;font-weight:800;text-decoration:none;">
          🧭 מפת GIS דו-ממדית ↗
        </a>
        <button id="btn-side-radii" class="ui-btn active">⭕ רדיוסים (8): פעיל</button>
        <button id="btn-side-pois" class="ui-btn active">📍 מיקומים (28): פעיל</button>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px;" id="gis-cat-buttons">
        <button data-gcat="all" class="gis-cat-chip ui-btn active" style="padding:3px 7px;font-size:10px;">הכל (28)</button>
        <button data-gcat="education" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🎓 חינוך (9)</button>
        <button data-gcat="transport" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🚌 תחבורה (7)</button>
        <button data-gcat="shopping" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🛒 מסחר (6)</button>
        <button data-gcat="parks" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🌳 פארקים (3)</button>
        <button data-gcat="health" class="gis-cat-chip ui-btn" style="padding:3px 7px;font-size:10px;">🏥 בריאות (3)</button>
      </div>
      <div style="font-size:11px;font-weight:700;color:#1e3a8a;margin-bottom:4px;">לחץ על מוקד ברשימה למעבר ממוקד במפה:</div>
      <div id="gis-poi-sidebar-list" style="max-height:210px;overflow-y:auto;display:flex;flex-direction:column;gap:4px;padding-left:2px;"></div>
    </div>

    <!-- ===================================================================== -->
    <!-- ON-DEMAND POPOVER DRAWER 3: INTERIOR DESIGN PACKAGES, LAYERS & DISPLAY (CLOSED BY DEFAULT) -->
    <!-- ===================================================================== -->
    <div id="drawer-settings" class="glass-panel dropdown-drawer" style="width:380px;">
      <div class="flex-between" style="margin-bottom:8px;border-bottom:1px solid #e2e8f0;padding-bottom:6px;">
        <span style="font-size:13px;font-weight:800;color:#0f172a;">⚙️ עיצוב פנים, שכבות והגדרות תצוגה</span>
        <button data-close-drawer class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
      </div>

      <!-- Real-Time 4 Interior Finish Packages Customizer -->
      <div class="section-box">
        <div class="flex-between" style="margin-bottom:6px;">
          <span style="font-size:12px;font-weight:800;color:#78350f;">🎨 חבילות עיצוב פנים בזמן אמת (מפרט קולסקי)</span>
          <span id="active-pkg-badge" style="font-size:10px;font-weight:800;background:#fef3c7;color:#92400e;padding:1px 6px;border-radius:4px;">Nordic Oak</span>
        </div>
        <div class="grid-2" style="margin-bottom:6px;" id="interior-pkg-buttons">
          <button data-pkg="nordic_oak" class="pkg-card-btn active">
            <div style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:800;color:#0f172a;">
              <span style="width:12px;height:12px;border-radius:999px;background:#b4bac2;border:1px solid #64748b;"></span>
              <span>1. Nordic Oak</span>
            </div>
            <span style="font-size:9px;color:#64748b;">פורצלן אפור בהיר, אלון וקלקטה</span>
          </button>
          <button data-pkg="warm_sahara" class="pkg-card-btn">
            <div style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:800;color:#0f172a;">
              <span style="width:12px;height:12px;border-radius:999px;background:#dfd3c3;border:1px solid #a8a29e;"></span>
              <span>2. Warm Sahara</span>
            </div>
            <span style="font-size:9px;color:#64748b;">טרוורטין קרם חם ומטבח קשמיר</span>
          </button>
          <button data-pkg="urban_anthracite" class="pkg-card-btn">
            <div style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:800;color:#0f172a;">
              <span style="width:12px;height:12px;border-radius:999px;background:#646b75;border:1px solid #334155;"></span>
              <span>3. Urban Anthracite</span>
            </div>
            <span style="font-size:9px;color:#64748b;">ריצוף גרפיט מודרני ונגרות אגוז</span>
          </button>
          <button data-pkg="classic_parquet" class="pkg-card-btn">
            <div style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:800;color:#0f172a;">
              <span style="width:12px;height:12px;border-radius:999px;background:#d8bc96;border:1px solid #92400e;"></span>
              <span>4. Classic Parquet</span>
            </div>
            <span style="font-size:9px;color:#64748b;">פרקט אלון מלא ומטבח לבן קלאסי</span>
          </button>
        </div>
        <div class="grid-2">
          <button id="btn-balcony-deck" class="ui-btn" style="font-size:11px;">
            🪵 מרפסות: פורצלן אפור
          </button>
          <button id="btn-toggle-furniture" class="ui-btn active" style="font-size:11px;">
            🪑 ריהוט 3D: פעיל
          </button>
        </div>
      </div>

      <!-- Projection & Display Toggles -->
      <div class="section-box">
        <div class="flex-between" style="margin-bottom:6px;">
          <span style="font-size:12px;font-weight:700;color:#334155;">מצב תצוגה ושכבות שרטוט</span>
          <span id="proj-badge" style="border-radius:4px;background:#e2e8f0;padding:2px 6px;font-size:11px;font-weight:600;color:#1e293b;">פרספקטיבה</span>
        </div>
        <div class="grid-2">
          <button id="btn-gmaps" class="ui-btn active" style="grid-column:span 2;">
            מפת Google Maps (פינס פינת בעש"ט): פעיל
          </button>
          <button id="btn-ortho" class="ui-btn">היטל אורתוגרפי (1:50)</button>
          <button id="btn-cad-plan" class="ui-btn active">שרטוט פנים CAD: פעיל</button>
          <button id="btn-edges" class="ui-btn active">קווי מתאר 3D: פעיל</button>
          <button id="btn-labels" class="ui-btn active">תוויות חדרים: פעיל</button>
        </div>
      </div>

      <!-- Floor Layers Visibility -->
      <div class="section-box">
        <div class="flex-between" style="margin-bottom:6px;">
          <span style="font-size:12px;font-weight:700;color:#334155;">שכבות קומות (A-1000..A-1006)</span>
          <button id="btn-all-floors" style="border:none;background:none;font-size:12px;font-weight:600;color:#2563eb;cursor:pointer;">הצג הכל</button>
        </div>
        <div id="layer-toggles">
          <label class="layer-row">
            <span style="display:flex;align-items:center;gap:6px;font-weight:600;">
              <input type="checkbox" data-layer="4_upper_roof_and_tower" checked />
              גג עליון וקולטי שמש (A-1006)
            </span>
            <span class="cad-badge" style="color:#64748b;">+25.53..+28.67</span>
          </label>
          <label class="layer-row">
            <span style="display:flex;align-items:center;gap:6px;font-weight:600;">
              <input type="checkbox" data-layer="3_floor_7_penthouse" checked />
              קומה 7 — דופלקסים עליון (A-1004)
            </span>
            <span class="cad-badge" style="color:#64748b;">+22.95..+25.53</span>
          </label>
          <label class="layer-row">
            <span style="display:flex;align-items:center;gap:6px;font-weight:600;">
              <input type="checkbox" data-layer="2_floor_6_penthouse" checked />
              קומה 6 — דופלקסים תחתון (A-1003)
            </span>
            <span class="cad-badge" style="color:#64748b;">+19.16..+22.95</span>
          </label>
          <label class="layer-row">
            <span style="display:flex;align-items:center;gap:6px;font-weight:600;">
              <input type="checkbox" data-layer="1_floors_1_to_5" checked />
              קומות 1–5 — דירות A, B, C (A-1002)
            </span>
            <span class="cad-badge" style="color:#64748b;">+3.81..+19.16</span>
          </label>
          <label class="layer-row">
            <span style="display:flex;align-items:center;gap:6px;font-weight:600;">
              <input type="checkbox" data-layer="0_site_and_ground" checked />
              קומת קרקע, לובי ומגרש (A-1001)
            </span>
            <span class="cad-badge" style="color:#64748b;">0.00..+3.81</span>
          </label>
          <label class="layer-row">
            <span style="display:flex;align-items:center;gap:6px;font-weight:600;">
              <input type="checkbox" data-layer="-1_basement_parking" checked />
              מרתף חניון (18 חניות · A-1000)
            </span>
            <span class="cad-badge" style="color:#64748b;">-3.50..0.00</span>
          </label>
        </div>
      </div>

      <!-- Materials Legend -->
      <div class="section-box">
        <div class="flex-between" style="margin-bottom:6px;">
          <span style="font-size:12px;font-weight:700;color:#334155;">מקרא חומרים והדגשה</span>
          <button id="btn-reset-mat" style="border:none;background:none;font-size:12px;font-weight:600;color:#2563eb;cursor:pointer;">איפוס</button>
        </div>
        <div class="grid-2" id="material-cards">
          <button data-mat="mat_D_white_plaster" class="mat-btn ui-btn" style="justify-content:flex-start;gap:6px;">
            <span style="display:inline-block;height:12px;width:12px;border-radius:3px;border:1px solid #94a3b8;background:#f4f2ed;"></span>
            <span>D — קירות חוץ</span>
          </button>
          <button data-mat="mat_B_gray_plaster" class="mat-btn ui-btn" style="justify-content:flex-start;gap:6px;">
            <span style="display:inline-block;height:12px;width:12px;border-radius:3px;border:1px solid #475569;background:#5f6368;"></span>
            <span>B — טיח אפור</span>
          </button>
          <button data-mat="mat_interior_wall" class="mat-btn ui-btn" style="justify-content:flex-start;gap:6px;">
            <span style="display:inline-block;height:12px;width:12px;border-radius:3px;border:1px solid #94a3b8;background:#fdfcfb;"></span>
            <span>קירות פנים</span>
          </button>
          <button data-mat="mat_C_white_louvers" class="mat-btn ui-btn" style="justify-content:flex-start;gap:6px;">
            <span style="display:inline-block;height:12px;width:12px;border-radius:3px;border:1px solid #94a3b8;background:#e8ecf0;"></span>
            <span>C — מסתורים</span>
          </button>
        </div>
      </div>

      <!-- Sun & Export Row -->
      <div class="section-box flex-between" style="gap:10px;margin-bottom:0;">
        <div style="flex:1;">
          <div class="flex-between" style="font-size:11px;color:#334155;">
            <span style="font-weight:700;">☀️ שמש ועונה</span>
            <span id="sun-val" class="cad-badge" style="color:#64748b;">13:30 · קיץ</span>
          </div>
          <input id="sun-slider" type="range" min="15" max="165" step="1" value="62" />
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
            <div style="font-size:10px;color:#64748b;">הזז את המחוון או בחר קומה לחשיפת הפנים</div>
          </div>
        </div>
        <button id="btn-toggle-sections-body" class="ui-btn" style="padding:2px 8px;font-size:11px;" title="מזער/הרחב חלון חתכים">▾</button>
      </div>

      <div class="sections-body">
        <!-- Continuous Z-Section Height Slider -->
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:8px 10px;margin-bottom:8px;">
          <div class="flex-between" style="margin-bottom:4px;">
            <label for="clip-slider" style="font-size:11px;font-weight:700;color:#0f172a;">מפלס חתך גובה רציף:</label>
            <span id="clip-val" class="cad-badge" style="font-size:11px;font-weight:800;color:#2563eb;">+29.50 מ' (מלא)</span>
          </div>
          <input id="clip-slider" type="range" min="-2.0" max="29.5" step="0.05" value="29.5" />
          <div class="flex-between cad-badge" style="margin-top:3px;font-size:10px;color:#64748b;">
            <span>-3.50</span>
            <span>0.00</span>
            <span>+10.37</span>
            <span>+19.72</span>
            <span>+22.95</span>
            <span>+28.67</span>
          </div>
        </div>

        <!-- Floor Cut Quick Presets -->
        <div class="grid-2" id="floor-cut-buttons">
          <button data-cut="29.5" data-view="iso_ne" class="cut-btn ui-btn">
            🏢 מבנה שלם (מלא)
          </button>
          <button data-cut="-0.25" data-view="cut_basement" class="cut-btn ui-btn">
            🚗 מרתף חניון (-3.50)
          </button>
          <button id="btn-cut-f3-lux" class="ui-btn ui-btn-lux" style="grid-column:span 2;">
            ✨ חתך קומה 3 המרוהטת (דירות יוקרה A + B + C)
          </button>
          <button data-cut="2.30" data-view="cut_ground" class="cut-btn ui-btn">
            🚪 קומת קרקע ולובי
          </button>
          <button data-cut="5.95" data-view="cut_f1_5" class="cut-btn ui-btn">
            📐 קומות 1–5 (A,B,C)
          </button>
          <button data-cut="21.45" data-view="cut_f6" class="cut-btn ui-btn">
            🏡 קומה 6 (דופלקסים)
          </button>
          <button data-cut="24.35" data-view="cut_f7" class="cut-btn ui-btn">
            ☀️ קומה 7 (גג עליון)
          </button>
          <button data-cut="5.95" data-view="top_plan_f1_5" class="cut-btn ui-btn" style="grid-column:span 2;">
            📏 תוכנית אדריכלית 1:50 מלמעלה
          </button>
        </div>
      </div>
    </aside>

    <!-- Floating Bottom HUD for Apartment A, B, C & Penthouse Interactive Interior Tour (Hidden unless inside tour) -->
    <div id="aptc-tour-hud" class="aptc-hud">
      <div class="flex-between" style="flex-wrap:wrap;gap:8px;">
        <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
          <span id="apt-active-badge" style="border-radius:6px;background:#b45309;color:#ffffff;padding:3px 8px;font-size:11px;font-weight:800;">דירות A / B / C · קומה 3 (+10.37)</span>
          <span id="aptc-active-room-title" style="font-size:13px;font-weight:800;color:#451a03;">סלון מרכזי ויציאה למרפסת שמש</span>
          <div style="display:inline-flex;align-items:center;gap:3px;background:#fef3c7;border:1px solid #f59e0b;border-radius:6px;padding:2px 6px;">
            <span style="font-size:10px;font-weight:800;color:#92400e;">קומה בסיור:</span>
            <select id="tour-floor-select" style="font-size:11px;font-weight:800;color:#451a03;background:transparent;border:none;cursor:pointer;outline:none;">
              <option value="1">קומה 1 (+4.25)</option>
              <option value="2">קומה 2 (+7.31)</option>
              <option value="3" selected>קומה 3 המרוהטת (+10.37)</option>
              <option value="4">קומה 4 (+13.43)</option>
              <option value="5">קומה 5 (+16.49)</option>
              <option value="6">קומה 6 דופלקסים (+19.72)</option>
              <option value="7">קומה 7 גג עליון (+22.95)</option>
            </select>
          </div>
        </div>
        <div style="display:flex;align-items:center;gap:10px;font-size:11px;color:#57534e;font-weight:600;">
          <span>⌨️ <b>WASD / חיצים</b>: הליכה</span>
          <span>🖱️ <b>גרירה</b>: מבט 360°</span>
          <span>👆 <b>לחיצה כפולה על הרצפה</b>: צעידה</span>
          <button id="btn-close-tour-hud" class="ui-btn" style="padding:2px 8px;font-size:11px;font-weight:800;">✕ סגור סרגל חדרים</button>
        </div>
      </div>

      <div class="flex-between" style="gap:10px;flex-wrap:wrap;">
        <!-- Room Teleport Bar (Apartment C + Apartment A + Apartment B + Penthouses) -->
        <div style="display:flex;flex-wrap:wrap;gap:4px;flex:1;" id="aptc-room-buttons">
          <span style="font-size:11px;font-weight:800;color:#92400e;align-self:center;padding:0 2px;">C:</span>
          <button data-room="living_main" class="room-chip active">🛋️ סלון C</button>
          <button data-room="kitchen_island" class="room-chip">🍽️ מטבח C</button>
          <button data-room="sun_balcony" class="room-chip">☀️ מרפסת C</button>
          <button data-room="master_suite" class="room-chip">🛏️ הורים C</button>
          <span style="font-size:11px;font-weight:800;color:#047857;align-self:center;padding:0 2px;margin-right:3px;">A:</span>
          <button data-room="apta_living" class="room-chip">🛋️ סלון A</button>
          <button data-room="apta_kitchen_dining" class="room-chip">🍽️ מטבח A</button>
          <button data-room="apta_balcony" class="room-chip">☀️ מרפסת A</button>
          <button data-room="apta_master" class="room-chip">🛏️ הורים A</button>
          <span style="font-size:11px;font-weight:800;color:#1d4ed8;align-self:center;padding:0 2px;margin-right:3px;">B:</span>
          <button data-room="aptb_living" class="room-chip">🛋️ סלון ומטבח B</button>
          <button data-room="aptb_balcony" class="room-chip">☀️ מרפסת B</button>
          <button data-room="aptb_master" class="room-chip">🛏️ הורים B</button>
          <span style="font-size:11px;font-weight:800;color:#7c3aed;align-self:center;padding:0 2px;margin-right:3px;">גג:</span>
          <button data-room="pent_pb_terrace" class="room-chip">👑 גג וג'קוזי PB</button>
          <button data-room="pent_pc_terrace" class="room-chip">👑 גג וג'קוזי PC</button>
          <button data-room="lobby_main" class="room-chip">🚪 לובי ראשי</button>
        </div>

        <!-- On-Screen Movement Controls -->
        <div style="display:flex;align-items:center;gap:4px;background:#f5efe6;padding:4px 8px;border-radius:9px;border:1px solid #dec9ad;">
          <span style="font-size:11px;font-weight:700;color:#78350f;margin-left:4px;">תנועה:</span>
          <button data-move="turnL" class="walk-dpad-btn" title="סיבוב מבט שמאלה">↶</button>
          <button data-move="fwd" class="walk-dpad-btn" title="צעד קדימה (W / ↑)">↑</button>
          <button data-move="back" class="walk-dpad-btn" title="צעד אחורה (S / ↓)">↓</button>
          <button data-move="left" class="walk-dpad-btn" title="תזוזה שמאלה (A / ←)">←</button>
          <button data-move="right" class="walk-dpad-btn" title="תזוזה ימינה (D / →)">→</button>
          <button data-move="turnR" class="walk-dpad-btn" title="סיבוב מבט ימינה">↷</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Inlined Three.js r128 Core Library (CSP-Safe) -->
  <script>__THREE_JS_INLINED__</script>

  <!-- Extracted 1:50 AutoCAD Unified Interior Wall Polygons & 2D Floor Plan Blueprint Lines -->
  <script>
    window.EXTRACTED_INTERIOR_PLANS = __EXTRACTED_PLANS_JSON__;
  </script>

  <!-- Parametric 1:50 Architectural CAD 3D Scene & Interactive Controller -->
  <script>
  (function() {
    const canvas = document.getElementById('cad-canvas');
    const labelsContainer = document.getElementById('labels-container');
    const PLANS = window.EXTRACTED_INTERIOR_PLANS;

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance', preserveDrawingBuffer: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.localClippingEnabled = true;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xffffff);

    // Clipping plane for interactive height sectioning
    const clipPlane = new THREE.Plane(new THREE.Vector3(0, -1, 0), 29.5);

    // Cameras: Perspective & Orthographic
    const aspect = window.innerWidth / window.innerHeight;
    const perspCam = new THREE.PerspectiveCamera(40, aspect, 0.5, 5000);
    const orthoSize = 20;
    const orthoCam = new THREE.OrthographicCamera(-orthoSize * aspect, orthoSize * aspect, orthoSize, -orthoSize, -2000, 5000);
    let activeCam = perspCam;
    let isOrtho = false;

    // Architectural Studio Lighting on Pure White Background
    const hemiLight = new THREE.HemisphereLight(0xffffff, 0xcbd5e1, 0.72);
    hemiLight.position.set(0, 60, 0);
    scene.add(hemiLight);

    const sunLight = new THREE.DirectionalLight(0xfffdf8, 0.88);
    sunLight.position.set(32, 48, 28);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 2048;
    sunLight.shadow.mapSize.height = 2048;
    sunLight.shadow.camera.near = 5;
    sunLight.shadow.camera.far = 140;
    const d = 28;
    sunLight.shadow.camera.left = -d;
    sunLight.shadow.camera.right = d;
    sunLight.shadow.camera.top = d;
    sunLight.shadow.camera.bottom = -d;
    sunLight.shadow.bias = -0.0005;
    scene.add(sunLight);

    const fillLight = new THREE.DirectionalLight(0xe2e8f0, 0.48);
    fillLight.position.set(-30, 25, -25);
    scene.add(fillLight);

    // =========================================================================
    // EXACT 1:50 CAD COORDINATE SYSTEM & MATERIALS
    // =========================================================================
    const CX = 17.50, CY = 13.00;
    function cadTo3D(x, y, z) {
      return new THREE.Vector3(x - CX, z, -(y - CY));
    }

    function cubicBezier2D(p0, p1, p2, p3, n = 18) {
      const pts = [];
      for (let i = 0; i <= n; i++) {
        const t = i / n, mt = 1 - t;
        pts.push([
          mt*mt*mt*p0[0] + 3*mt*mt*t*p1[0] + 3*mt*t*t*p2[0] + t*t*t*p3[0],
          mt*mt*mt*p0[1] + 3*mt*mt*t*p1[1] + 3*mt*t*t*p2[1] + t*t*t*p3[1]
        ]);
      }
      return pts;
    }

    const NW_CORNER = [4.045, 17.266];
    const EU = [0.978462, 0.206425];
    const ES = [0.206425, -0.978462];
    const EN_NORTH = [-0.206425, 0.978462];
    const EN_WEST  = [-0.978462, -0.206425];

    function ptUV(u, s) {
      return [
        NW_CORNER[0] + u * EU[0] + s * ES[0],
        NW_CORNER[1] + u * EU[1] + s * ES[1]
      ];
    }

    const NE_ARC_OUTER = cubicBezier2D([26.990, 22.106], [27.937, 22.195], [28.820, 21.619], [29.122, 20.717], 18);
    const NE_ARC_INNER = cubicBezier2D([26.948, 21.902], [27.806, 21.983], [28.606, 21.461], [28.880, 20.644], 18);
    const LOT_NE_CURVE = cubicBezier2D([34.100, 22.107], [34.100, 25.800], [28.500, 27.798], [24.205, 26.892], 20);
    const SETBACK_NE_CURVE = cubicBezier2D([26.625, 22.342], [29.210, 22.887], [31.594, 20.654], [31.100, 18.021], 16);

    const POLY_LOT = [[0, 0], [34.049, 0], ...LOT_NE_CURVE, [0.184, 21.800], [0.066, 7.847]];
    const POLY_SETBACK = [[4.0, 4.0], [31.1, 4.0], ...SETBACK_NE_CURVE.slice().reverse(), [4.0, 17.569]];

    // Outer slab contour (Floors 1-5 & Floor 6 terrace deck)
    const POLY_OUTER = [
      [4.045, 17.266],
      ...NE_ARC_OUTER,
      [30.726, 13.134],
      [30.726, 12.150],
      [30.351, 12.150],
      [30.351, 4.199],
      [22.849, 4.199],
      [22.849, 4.100],
      [17.251, 4.100],
      [17.251, 4.951],
      [12.399, 4.951],
      [12.399, 6.517],
      [6.572, 5.287]
    ];

    // True Floors 1-5 floor slab polygon (follows the 60cm North recess and inner NE corner wall, leaving the X void inside the decorative NE beam)
    const POLY_F1_5_SLAB = [
      [4.045, 17.266],
      [4.436, 17.349],
      [4.560, 16.761],
      [21.096, 20.250],
      [20.972, 20.837],
      [26.990, 22.106],
      [27.412, 20.356],
      [29.122, 20.717],
      [30.726, 13.134],
      [30.726, 12.150],
      [30.351, 12.150],
      [30.351, 4.199],
      [22.849, 4.199],
      [22.849, 4.100],
      [17.251, 4.100],
      [17.251, 4.951],
      [12.399, 4.951],
      [12.399, 6.517],
      [6.572, 5.287]
    ];

    // True Floor 6 enclosed exterior wall polygon (verified from A-1003; PB living room East wall is at 15.495,19.680 -> 16.328,15.716)
    const POLY_F6_WALLS = [
      [4.045, 17.266],
      [15.495, 19.680],
      [16.328, 15.716],
      [18.089, 16.089],
      [18.049, 16.284],
      [18.440, 16.368],
      [19.039, 13.530],
      [21.984, 14.150],
      [30.351, 14.150],
      [30.351, 7.550],
      [26.151, 7.550],
      [26.151, 4.199],
      [22.849, 4.199],
      [22.849, 4.100],
      [17.251, 4.100],
      [17.251, 4.951],
      [12.399, 4.951],
      [12.399, 6.517],
      [6.572, 5.287]
    ];

    // True Floor 7 enclosed exterior wall polygon (verified from A-1004)
    const POLY_UPPER_ROOF_OUTER = [
      [7.628, 14.086],
      [18.440, 16.368],
      [19.039, 13.530],
      [21.984, 14.150],
      [23.899, 14.150],
      [23.899, 11.250],
      [26.151, 11.250],
      [26.151, 5.850],
      [18.201, 5.848],
      [18.201, 9.550],
      [17.437, 9.550],
      [17.437, 10.329],
      [15.502, 9.921],
      [15.970, 7.698],
      [10.295, 6.502],
      [9.394, 10.778],
      [8.371, 10.564]
    ];

    const POLY_TOWER_OUTER = [
      [12.611, 14.933],
      [16.624, 15.780],
      [17.367, 12.258],
      [13.354, 11.411]
    ];

    // Balcony Polygons (NW and NC extend from recessed wall s=+0.60 out to s=-1.90, total depth 2.50m!)
    const BALCONY_NW = [ptUV(4.10, 0.60), ptUV(4.10, -1.90), ptUV(8.55, -1.90), ptUV(8.55, 0.60)];
    const BALCONY_NC = [ptUV(12.75, 0.60), ptUV(12.75, -1.90), ptUV(17.20, -1.90), ptUV(17.20, 0.60)];
    const BALCONY_NW_F6 = [ptUV(4.10, 0.00), ptUV(4.10, -1.90), ptUV(8.55, -1.90), ptUV(8.55, 0.00)];
    const BALCONY_E  = [[30.351, 6.750], [32.550, 6.750], [32.550, 12.150], [30.351, 12.150]];
    const BALCONY_S_SERVICE = [[13.601, 4.951], [13.601, 4.100], [15.150, 4.100], [15.150, 4.951]];

    // PBR Materials (Exterior + Interior - Unified smooth interior wall finish for buyer presentation)
    const matInteriorUnified = new THREE.MeshStandardMaterial({
      color: 0xfdfcfb,
      roughness: 0.64,
      metalness: 0.01,
      side: THREE.DoubleSide,
      clippingPlanes: [clipPlane]
    });
    const matDefs = {
      mat_D_white_plaster:        new THREE.MeshStandardMaterial({ color: 0xfbfaf8, roughness: 0.72, metalness: 0.02, clippingPlanes: [clipPlane] }),
      mat_B_gray_plaster:         new THREE.MeshStandardMaterial({ color: 0x5f6368, roughness: 0.70, metalness: 0.05, clippingPlanes: [clipPlane] }),
      mat_C_white_louvers:        new THREE.MeshStandardMaterial({ color: 0xe8edf2, roughness: 0.36, metalness: 0.35, clippingPlanes: [clipPlane] }),
      mat_A_iron_railing:         new THREE.MeshStandardMaterial({ color: 0x24282e, roughness: 0.35, metalness: 0.80, clippingPlanes: [clipPlane] }),
      mat_window_glass:           new THREE.MeshStandardMaterial({ color: 0x356288, roughness: 0.12, metalness: 0.70, transparent: true, opacity: 0.78, clippingPlanes: [clipPlane] }),
      mat_alu_frame:              new THREE.MeshStandardMaterial({ color: 0x2e3238, roughness: 0.40, metalness: 0.75, clippingPlanes: [clipPlane] }),
      mat_concrete_curb:          new THREE.MeshStandardMaterial({ color: 0xb8bec6, roughness: 0.80, metalness: 0.02, clippingPlanes: [clipPlane] }),
      mat_terrace_tile:           new THREE.MeshStandardMaterial({ map: makeTravertineFloorTexture(), color: 0xbec4cc, roughness: 0.34, metalness: 0.05, clippingPlanes: [clipPlane] }),
      mat_solar_panel:            new THREE.MeshStandardMaterial({ color: 0x1b2a47, roughness: 0.18, metalness: 0.72, clippingPlanes: [clipPlane] }),
      mat_site_ground:            new THREE.MeshStandardMaterial({ color: 0xebe7e0, roughness: 0.88, metalness: 0.00, clippingPlanes: [clipPlane] }),
      mat_road_asphalt:           new THREE.MeshStandardMaterial({ color: 0x64686e, roughness: 0.92, metalness: 0.00, clippingPlanes: [clipPlane] }),
      mat_landscape_green:        new THREE.MeshStandardMaterial({ color: 0x67945e, roughness: 0.85, metalness: 0.00, clippingPlanes: [clipPlane] }),
      mat_cad_setback:            new THREE.MeshStandardMaterial({ color: 0xdc2626, roughness: 0.50, metalness: 0.00, clippingPlanes: [clipPlane] }),
      mat_interior_wall:          matInteriorUnified,
      mat_core_concrete:          matInteriorUnified,
      mat_interior_partition:     matInteriorUnified,
      mat_interior_wood_fixtures: new THREE.MeshStandardMaterial({ color: 0xc49a6c, roughness: 0.52, metalness: 0.06, clippingPlanes: [clipPlane] })
    };

    // =========================================================================
    // PROCEDURAL HIGH-RES PBR TEXTURES FOR LUXURY LIGHT-TONED APARTMENT C
    // =========================================================================
    function makeTravertineFloorTexture() {
      const c = document.createElement('canvas');
      c.width = 512; c.height = 512;
      const ctx = c.getContext('2d');
      // Architectural light-grey porcelain base (distinct contrast against crisp white walls)
      ctx.fillStyle = '#b4bac2';
      ctx.fillRect(0, 0, 512, 512);
      // Subtle cool-grey stone clouding & fine mineral veins
      for (let i = 0; i < 32; i++) {
        ctx.strokeStyle = i % 2 === 0 ? 'rgba(142, 149, 158, 0.36)' : 'rgba(206, 212, 220, 0.32)';
        ctx.lineWidth = 1.2 + (i % 4) * 1.4;
        ctx.beginPath();
        let x = (i * 37) % 512, y = 0;
        ctx.moveTo(x, y);
        while (y < 512) {
          y += 32;
          x += Math.sin(y * 0.03 + i) * 14;
          ctx.lineTo(x, y);
        }
        ctx.stroke();
      }
      // 120x120cm porcelain tile crisp architectural joint grid
      ctx.strokeStyle = 'rgba(116, 123, 133, 0.55)';
      ctx.lineWidth = 2.2;
      ctx.strokeRect(1, 1, 254, 254);
      ctx.strokeRect(257, 1, 254, 254);
      ctx.strokeRect(1, 257, 254, 254);
      ctx.strokeRect(257, 257, 254, 254);
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(0.42, 0.42);
      return tex;
    }

    function makeLightOakParquetTexture() {
      const c = document.createElement('canvas');
      c.width = 512; c.height = 512;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#d8bc96';
      ctx.fillRect(0, 0, 512, 512);
      const plankH = 64;
      for (let row = 0; row < 8; row++) {
        const y0 = row * plankH;
        const offset = (row % 2) * 128;
        for (let col = -1; col < 3; col++) {
          const x0 = col * 256 + offset;
          const shade = ((row * 3 + col * 7) % 5) * 4 - 8;
          ctx.fillStyle = `rgb(${216 + shade}, ${186 + shade}, ${148 + shade})`;
          ctx.fillRect(x0, y0, 254, plankH - 2);
          ctx.strokeStyle = 'rgba(145, 110, 72, 0.32)';
          ctx.lineWidth = 1;
          for (let g = 6; g < plankH - 4; g += 9) {
            ctx.beginPath();
            ctx.moveTo(x0, y0 + g);
            ctx.lineTo(x0 + 254, y0 + g + Math.sin(row + g) * 2);
            ctx.stroke();
          }
        }
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(0.65, 0.65);
      return tex;
    }

    function makeCalacattaMarbleTexture() {
      const c = document.createElement('canvas');
      c.width = 512; c.height = 512;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#fcfaf7';
      ctx.fillRect(0, 0, 512, 512);
      for (let i = 0; i < 20; i++) {
        ctx.strokeStyle = i % 3 === 0 ? 'rgba(176, 138, 86, 0.38)' : 'rgba(150, 142, 132, 0.30)';
        ctx.lineWidth = 1.2 + (i % 3) * 1.5;
        ctx.beginPath();
        let x = (i * 53) % 512, y = 0;
        ctx.moveTo(x, y);
        while (y < 512) {
          y += 28;
          x += Math.cos(y * 0.025 + i) * 18;
          ctx.lineTo(x, y);
        }
        ctx.stroke();
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(0.5, 0.5);
      return tex;
    }

    function makeFlutedOakTexture() {
      const c = document.createElement('canvas');
      c.width = 256; c.height = 256;
      const ctx = c.getContext('2d');
      for (let x = 0; x < 256; x += 8) {
        ctx.fillStyle = '#c9a070';
        ctx.fillRect(x, 0, 5, 256);
        ctx.fillStyle = '#8f683d';
        ctx.fillRect(x + 5, 0, 3, 256);
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(2.0, 1.0);
      return tex;
    }

    function makeLightWoodCabinetTexture() {
      const c = document.createElement('canvas');
      c.width = 512; c.height = 512;
      const ctx = c.getContext('2d');
      // Warm light natural oak veneer base
      ctx.fillStyle = '#d6b284';
      ctx.fillRect(0, 0, 512, 512);
      // Subtle vertical veneer bands & warm wood grain fibers
      for (let i = 0; i < 4; i++) {
        const x0 = i * 128;
        const delta = (i % 2 === 0) ? 5 : -5;
        ctx.fillStyle = `rgb(${214 + delta}, ${178 + delta}, ${132 + delta})`;
        ctx.fillRect(x0, 0, 128, 512);
        // Fine vertical cabinet reveal seam
        ctx.fillStyle = 'rgba(115, 80, 42, 0.42)';
        ctx.fillRect(x0, 0, 2, 512);
      }
      // Natural vertical oak grain lines & cathedrals
      for (let g = 0; g < 140; g++) {
        const gx = (g * 3.7) % 512;
        ctx.strokeStyle = (g % 3 === 0) ? 'rgba(242, 220, 188, 0.32)' : 'rgba(148, 106, 60, 0.30)';
        ctx.lineWidth = (g % 4 === 0) ? 1.6 : 0.9;
        ctx.beginPath();
        ctx.moveTo(gx, 0);
        for (let y = 32; y <= 512; y += 32) {
          ctx.lineTo(gx + Math.sin(y * 0.02 + g) * 3.5, y);
        }
        ctx.stroke();
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(1.2, 1.0);
      return tex;
    }

    function makeWovenRugTexture() {
      const c = document.createElement('canvas');
      c.width = 256; c.height = 256;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#d2c2ae';
      ctx.fillRect(0, 0, 256, 256);
      ctx.strokeStyle = 'rgba(162, 140, 114, 0.35)';
      ctx.lineWidth = 2;
      for (let y = 0; y < 256; y += 6) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(256, y); ctx.stroke();
      }
      ctx.strokeStyle = 'rgba(138, 114, 88, 0.45)';
      ctx.lineWidth = 8;
      ctx.strokeRect(6, 6, 244, 244);
      return new THREE.CanvasTexture(c);
    }

    function makeWoodDeckTexture() {
      const c = document.createElement('canvas');
      c.width = 512; c.height = 512;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#9c6b3f';
      ctx.fillRect(0, 0, 512, 512);
      const slatH = 32;
      for (let r = 0; r < 16; r++) {
        const y0 = r * slatH;
        const delta = ((r * 7) % 5) * 4 - 8;
        ctx.fillStyle = `rgb(${158 + delta}, ${108 + delta}, ${64 + delta})`;
        ctx.fillRect(0, y0, 512, slatH - 3);
        ctx.fillStyle = 'rgba(45, 28, 14, 0.72)';
        ctx.fillRect(0, y0 + slatH - 3, 512, 3);
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(0.75, 0.75);
      return tex;
    }

    const defaultTravertineTex = makeTravertineFloorTexture();
    const defaultParquetTex = makeLightOakParquetTexture();
    const defaultCalacattaTex = makeCalacattaMarbleTexture();
    const defaultWoodDeckTex = makeWoodDeckTexture();

    Object.assign(matDefs, {
      mat_lux_travertine_floor: new THREE.MeshStandardMaterial({ map: defaultTravertineTex, color: 0xbec5ce, roughness: 0.28, metalness: 0.06, clippingPlanes: [clipPlane] }),
      mat_lux_oak_parquet:      new THREE.MeshStandardMaterial({ map: defaultParquetTex, color: 0xe6cda8, roughness: 0.36, metalness: 0.02, clippingPlanes: [clipPlane] }),
      mat_lux_calacatta_marble: new THREE.MeshStandardMaterial({ map: defaultCalacattaTex, color: 0xffffff, roughness: 0.16, metalness: 0.06, clippingPlanes: [clipPlane] }),
      mat_lux_fluted_oak:       new THREE.MeshStandardMaterial({ map: makeFlutedOakTexture(), color: 0xcca272, roughness: 0.40, metalness: 0.05, clippingPlanes: [clipPlane] }),
      mat_lux_oak_smooth:       new THREE.MeshStandardMaterial({ color: 0xc49a68, roughness: 0.36, metalness: 0.04, clippingPlanes: [clipPlane] }),
      mat_lux_boucle_cream:     new THREE.MeshStandardMaterial({ color: 0xeee7dc, roughness: 0.85, metalness: 0.01, clippingPlanes: [clipPlane] }),
      mat_lux_linen_sand:       new THREE.MeshStandardMaterial({ color: 0xd4c3ad, roughness: 0.82, metalness: 0.01, clippingPlanes: [clipPlane] }),
      mat_lux_pillow_taupe:     new THREE.MeshStandardMaterial({ color: 0x9c7e61, roughness: 0.78, metalness: 0.02, clippingPlanes: [clipPlane] }),
      mat_lux_cabinet_cream:    new THREE.MeshStandardMaterial({ map: makeLightWoodCabinetTexture(), color: 0xdcb98a, roughness: 0.34, metalness: 0.03, clippingPlanes: [clipPlane] }),
      mat_lux_champagne_brass:  new THREE.MeshStandardMaterial({ color: 0xb89058, roughness: 0.24, metalness: 0.86, clippingPlanes: [clipPlane] }),
      mat_lux_rug_woven:        new THREE.MeshStandardMaterial({ map: makeWovenRugTexture(), color: 0xd5c5b0, roughness: 0.90, metalness: 0.00, clippingPlanes: [clipPlane] }),
      mat_lux_sheer_curtain:    new THREE.MeshStandardMaterial({ color: 0xfaf6ef, roughness: 0.65, metalness: 0.00, transparent: true, opacity: 0.78, side: THREE.DoubleSide, clippingPlanes: [clipPlane] }),
      mat_lux_dark_glass:       new THREE.MeshStandardMaterial({ color: 0x181c22, roughness: 0.10, metalness: 0.82, clippingPlanes: [clipPlane] }),
      mat_lux_clear_glass:      new THREE.MeshStandardMaterial({ color: 0xe0f2fe, roughness: 0.08, metalness: 0.25, transparent: true, opacity: 0.34, side: THREE.DoubleSide, clippingPlanes: [clipPlane] }),
      mat_lux_mirror:           new THREE.MeshStandardMaterial({ color: 0xeef4f8, roughness: 0.04, metalness: 0.94, clippingPlanes: [clipPlane] }),
      mat_lux_glow_warm:        new THREE.MeshStandardMaterial({ color: 0xfffbeb, emissive: 0xfde68a, emissiveIntensity: 0.95, roughness: 0.20, clippingPlanes: [clipPlane] }),
      mat_lux_ceramic_white:    new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.14, metalness: 0.05, clippingPlanes: [clipPlane] }),
      mat_lux_plant_olive:      new THREE.MeshStandardMaterial({ color: 0x5c7c52, roughness: 0.78, metalness: 0.00, clippingPlanes: [clipPlane] }),
      mat_wood_deck:            new THREE.MeshStandardMaterial({ map: defaultWoodDeckTex, color: 0xc89666, roughness: 0.45, metalness: 0.04, clippingPlanes: [clipPlane] }),
      mat_jacuzzi_water:        new THREE.MeshStandardMaterial({ color: 0x38bdf8, emissive: 0x0284c7, emissiveIntensity: 0.35, roughness: 0.08, metalness: 0.15, transparent: true, opacity: 0.82, clippingPlanes: [clipPlane] }),
      mat_parking_asphalt:      new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.86, metalness: 0.04, clippingPlanes: [clipPlane] }),
      mat_parking_line:         new THREE.MeshStandardMaterial({ color: 0xf8fafc, emissive: 0xe2e8f0, emissiveIntensity: 0.22, roughness: 0.40, clippingPlanes: [clipPlane] })
    });

    const edgeMaterial = new THREE.LineBasicMaterial({ color: 0x475569, transparent: true, opacity: 0.24, clippingPlanes: [clipPlane] });
    const furniturePlanLineMaterial = new THREE.LineBasicMaterial({ color: 0x1d4ed8, transparent: true, opacity: 0.92, clippingPlanes: [clipPlane] });
    const cadPlanLineMaterial = new THREE.LineBasicMaterial({ color: 0xb45309, transparent: true, opacity: 0.88, clippingPlanes: [clipPlane] });

    // Layer Groups
    const layerGroups = {
      "-1_basement_parking": new THREE.Group(),
      "0_site_and_ground": new THREE.Group(),
      "1_floors_1_to_5": new THREE.Group(),
      "2_floor_6_penthouse": new THREE.Group(),
      "3_floor_7_penthouse": new THREE.Group(),
      "4_upper_roof_and_tower": new THREE.Group()
    };
    const edgeLines = [];
    const cadPlanLineMeshes = [];
    const allMeshes = [];
    const interiorFurnitureMeshes = [];
    const balconyFloorMeshes = [];
    const interiorPointLights = [];
    const balconySpotLights = [];
    let isBuildingInteriorFurniture = false;

    Object.values(layerGroups).forEach(g => scene.add(g));

    function isFurnitureMat(matKey) {
      return isBuildingInteriorFurniture &&
        matKey !== "mat_lux_travertine_floor" &&
        matKey !== "mat_lux_calacatta_marble" &&
        matKey !== "mat_terrace_tile" &&
        matKey !== "mat_interior_wall";
    }

    function addExtrudedPolygon(layerKey, matKey, poly2d, zMin, zMax, withEdges = true) {
      if (poly2d.length < 3 || Math.abs(zMax - zMin) < 1e-4) return null;
      const shape = new THREE.Shape();
      shape.moveTo(poly2d[0][0] - CX, poly2d[0][1] - CY);
      for (let i = 1; i < poly2d.length; i++) {
        shape.lineTo(poly2d[i][0] - CX, poly2d[i][1] - CY);
      }
      shape.closePath();

      const geom = new THREE.ExtrudeGeometry(shape, { depth: zMax - zMin, bevelEnabled: false });
      geom.rotateX(-Math.PI / 2);
      geom.translate(0, zMin, 0);
      geom.computeVertexNormals();

      const mesh = new THREE.Mesh(geom, matDefs[matKey]);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      mesh.userData = { layer: layerKey, matKey };
      layerGroups[layerKey].add(mesh);
      allMeshes.push(mesh);
      if (isFurnitureMat(matKey)) {
        interiorFurnitureMeshes.push(mesh);
      }

      if (withEdges) {
        const edges = new THREE.EdgesGeometry(geom, 28);
        const line = new THREE.LineSegments(edges, edgeMaterial);
        layerGroups[layerKey].add(line);
        edgeLines.push(line);
      }
      return mesh;
    }

    function addBoxAligned(layerKey, matKey, origXY, uVec, vVec, u0, u1, v0, v1, z0, z1, withEdges = true) {
      if (u1 - u0 < 1e-3 || Math.abs(v1 - v0) < 1e-3 || z1 - z0 < 1e-3) return null;
      const [ox, oy] = origXY;
      const [ux, uy] = uVec;
      const [vx, vy] = vVec;
      const poly = [
        [ox + u0*ux + v0*vx, oy + u0*uy + v0*vy],
        [ox + u1*ux + v0*vx, oy + u1*uy + v0*vy],
        [ox + u1*ux + v1*vx, oy + u1*uy + v1*vy],
        [ox + u0*ux + v1*vx, oy + u0*uy + v1*vy]
      ];
      return addExtrudedPolygon(layerKey, matKey, poly, z0, z1, withEdges);
    }

    function addWallStrip(layerKey, matKey, path2d, thickness, z0, z1, closed = false, withEdges = true) {
      const n = path2d.length;
      const limit = closed ? n : n - 1;
      for (let i = 0; i < limit; i++) {
        const [x0, y0] = path2d[i];
        const [x1, y1] = path2d[(i + 1) % n];
        const dx = x1 - x0, dy = y1 - y0;
        const L = Math.hypot(dx, dy);
        if (L < 1e-3) continue;
        const ux = dx / L, uy = dy / L;
        const nx = -uy, ny = ux;
        addBoxAligned(layerKey, matKey, [x0, y0], [ux, uy], [nx, ny], -0.02, L + 0.02, -thickness, 0.0, z0, z1, withEdges);
      }
    }

    function add2DLineSegmentsOnFloor(layerKey, linesArray, zElev, lineMat) {
      if (!linesArray || linesArray.length === 0) return;
      const positions = new Float32Array(linesArray.length * 6);
      for (let i = 0; i < linesArray.length; i++) {
        const [x0, y0, x1, y1] = linesArray[i];
        const idx = i * 6;
        positions[idx]     = x0 - CX;
        positions[idx + 1] = zElev;
        positions[idx + 2] = -(y0 - CY);
        positions[idx + 3] = x1 - CX;
        positions[idx + 4] = zElev;
        positions[idx + 5] = -(y1 - CY);
      }
      const lineGeom = new THREE.BufferGeometry();
      lineGeom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      const lineSegs = new THREE.LineSegments(lineGeom, lineMat);
      layerGroups[layerKey].add(lineSegs);
      cadPlanLineMeshes.push(lineSegs);
    }

    function signedArea2D(ring) {
      let a = 0;
      for (let i = 0, n = ring.length; i < n; i++) {
        const [x0, y0] = ring[i];
        const [x1, y1] = ring[(i + 1) % n];
        a += (x0 * y1 - x1 * y0);
      }
      return 0.5 * a;
    }

    // Extrude exact closed 2D CAD wall polygons (with holes and pre-triangulated caps) into smooth, flat-shaded 3D walls
    function addWallPolygonMesh(layerKey, matKey, wp, zMin, zMax) {
      if (!wp || !wp.exterior || wp.exterior.length < 3) return;
      const verts = [];
      const edgeSegs = [];

      const extRing = wp.exterior.slice();
      if (signedArea2D(extRing) < 0) extRing.reverse(); // Ensure CCW in CAD XY
      const rings = [extRing];
      if (wp.holes && wp.holes.length) {
        wp.holes.forEach(h => {
          if (h.length >= 3) {
            const hr = h.slice();
            if (signedArea2D(hr) > 0) hr.reverse(); // Ensure CW in CAD XY for holes
            rings.push(hr);
          }
        });
      }

      rings.forEach(ring => {
        const n = ring.length;
        for (let i = 0; i < n; i++) {
          const [x0, y0] = ring[i];
          const [x1, y1] = ring[(i + 1) % n];
          const X0 = x0 - CX, Z0 = -(y0 - CY);
          const X1 = x1 - CX, Z1 = -(y1 - CY);
          // Flat-shaded vertical quad (2 triangles with outward normal)
          verts.push(
            X0, zMin, Z0,  X1, zMin, Z1,  X1, zMax, Z1,
            X0, zMin, Z0,  X1, zMax, Z1,  X0, zMax, Z0
          );
          // Top and bottom horizontal contour edges
          edgeSegs.push(
            X0, zMax, Z0,  X1, zMax, Z1,
            X0, zMin, Z0,  X1, zMin, Z1
          );
          // Vertical corner edge only at true corners (> 22 deg turn)
          const [xp, yp] = ring[(i - 1 + n) % n];
          const dx1 = x0 - xp, dy1 = y0 - yp, L1 = Math.hypot(dx1, dy1);
          const dx2 = x1 - x0, dy2 = y1 - y0, L2 = Math.hypot(dx2, dy2);
          if (L1 > 1e-3 && L2 > 1e-3) {
            const cosA = (dx1 * dx2 + dy1 * dy2) / (L1 * L2);
            if (cosA < 0.927) {
              edgeSegs.push(X0, zMin, Z0,  X0, zMax, Z0);
            }
          }
        }
      });

      if (wp.tris) {
        for (let i = 0; i < wp.tris.length; i++) {
          const [[ax, ay], [bx, by], [cx, cy]] = wp.tris[i];
          const AX = ax - CX, AZ = -(ay - CY);
          const BX = bx - CX, BZ = -(by - CY);
          const CX_ = cx - CX, CZ = -(cy - CY);
          const crossY = (BX - AX) * (CZ - AZ) - (BZ - AZ) * (CX_ - AX);
          if (crossY >= 0) {
            // Top cap (+Y normal)
            verts.push(AX, zMax, AZ,  BX, zMax, BZ,  CX_, zMax, CZ);
            // Bottom cap (-Y normal)
            verts.push(AX, zMin, AZ,  CX_, zMin, CZ,  BX, zMin, BZ);
          } else {
            verts.push(AX, zMax, AZ,  CX_, zMax, CZ,  BX, zMax, BZ);
            verts.push(AX, zMin, AZ,  BX, zMin, BZ,  CX_, zMin, CZ);
          }
        }
      }

      const geom = new THREE.BufferGeometry();
      geom.setAttribute('position', new THREE.Float32BufferAttribute(verts, 3));
      geom.computeVertexNormals();

      const mesh = new THREE.Mesh(geom, matDefs[matKey]);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      mesh.userData = { layer: layerKey, matKey };
      layerGroups[layerKey].add(mesh);
      allMeshes.push(mesh);

      if (edgeSegs.length > 0) {
        const eGeom = new THREE.BufferGeometry();
        eGeom.setAttribute('position', new THREE.Float32BufferAttribute(edgeSegs, 3));
        const line = new THREE.LineSegments(eGeom, edgeMaterial);
        layerGroups[layerKey].add(line);
        edgeLines.push(line);
      }
    }

    // Add extracted continuous 3D interior walls (unified material, smooth closed polygons) + 2D floor markings
    const APT_A_O = [15.0, 13.0];
    const APT_A_U = [0.9784574, 0.2064488];
    const APT_A_V = [-0.2064488, 0.9784574];
    function aptA_XY(u, v) {
      return [
        APT_A_O[0] + u * APT_A_U[0] + v * APT_A_V[0],
        APT_A_O[1] + u * APT_A_U[1] + v * APT_A_V[1]
      ];
    }

    function isInsideAptC(x, y) {
      if (y > 12.15 || x < 12.40) return false;
      if (x < 17.40 && y > 9.15) return false;
      if (x < 25.10 && y > 9.15) return false;
      return true;
    }

    function isInsideAptA(x, y) {
      const rx = x - APT_A_O[0], ry = y - APT_A_O[1];
      const u = rx * APT_A_U[0] + ry * APT_A_U[1];
      const v = rx * APT_A_V[0] + ry * APT_A_V[1];
      if (u >= 0.75 && u <= 7.66 && v >= 2.38 && v <= 6.45) return true;
      if (u >= 4.06 && u <= 7.78 && v >= -0.45 && v <= 2.38) return true;
      if (u >= 7.66 && u <= 13.66 && v >= 2.03 && v <= 6.45) return true;
      if (u >= 9.86 && u <= 15.42 && v >= -3.12 && v <= 4.65) return true;
      return false;
    }

    function isInsideAptB(x, y) {
      const dx = x - NW_CORNER[0], dy = y - NW_CORNER[1];
      const u = dx * EU[0] + dy * EU[1];
      const s = dx * ES[0] + dy * ES[1];
      if (u >= 0.15 && u <= 10.45 && s >= 0.70 && s <= 4.02) return true;
      if (u >= 0.15 && u <= 7.85 && s >= 3.70 && s <= 7.02) return true;
      if (u >= 0.15 && u <= 5.75 && s >= 7.02 && s <= 12.05) return true;
      return false;
    }

    function addExtractedFloorWalls(layerKey, floorPlanKey, zFlr, zCeil) {
      const polys = PLANS[floorPlanKey].wall_polys || [];
      for (let i = 0; i < polys.length; i++) {
        addWallPolygonMesh(layerKey, "mat_interior_wall", polys[i], zFlr, zCeil);
      }

      // On Floor 3 (zFlr = 10.37), Apartments A, B, and C are modeled in full luxury 3D (floors, rugs, furniture, kitchen, sanitary),
      // and on Floors 6 & 7 (f6, f7), Penthouses PB & PC are modeled in full luxury 3D!
      const isFeaturedLuxFloor = (floorPlanKey === "f1_5" && Math.abs(zFlr - 10.37) < 0.05);
      const isPenthouseFloor = (floorPlanKey === "f6" || floorPlanKey === "f7");
      const furnLines = isFeaturedLuxFloor
        ? (PLANS[floorPlanKey].furniture_lines || []).filter(([x0, y0, x1, y1]) => {
            const mx = 0.5 * (x0 + x1), my = 0.5 * (y0 + y1);
            return !isInsideAptC(mx, my) && !isInsideAptA(mx, my) && !isInsideAptB(mx, my);
          })
        : (isPenthouseFloor ? [] : PLANS[floorPlanKey].furniture_lines);
      const cadLines = isFeaturedLuxFloor
        ? (PLANS[floorPlanKey].cad_lines || []).filter(([x0, y0, x1, y1]) => {
            const mx = 0.5 * (x0 + x1), my = 0.5 * (y0 + y1);
            return !isInsideAptC(mx, my) && !isInsideAptA(mx, my) && !isInsideAptB(mx, my);
          })
        : (isPenthouseFloor
            ? (PLANS[floorPlanKey].cad_lines || []).filter(([x0, y0, x1, y1]) => {
                const mx = 0.5 * (x0 + x1), my = 0.5 * (y0 + y1);
                return (mx >= 12.5 && mx <= 19.0 && my >= 10.8 && my <= 16.2);
              })
            : PLANS[floorPlanKey].cad_lines);

      add2DLineSegmentsOnFloor(layerKey, furnLines, zFlr + 0.025, furniturePlanLineMaterial);
      add2DLineSegmentsOnFloor(layerKey, cadLines, zFlr + 0.028, cadPlanLineMaterial);
    }

    // =========================================================================
    // LUXURY ARCHITECTURAL SALES MODEL OF APARTMENT C (LIGHT TONES + WARM CONTRAST)
    // =========================================================================
    const aptCFloorMeshes = [];
    const aptCWaypointMeshes = [];

    function addBoxXY(layerKey, matKey, x0, x1, y0, y1, z0, z1, withEdges = false) {
      return addBoxAligned(layerKey, matKey, [x0, y0], [1, 0], [0, 1], 0, x1 - x0, 0, y1 - y0, z0, z1, withEdges);
    }

    function addCylinder3D(layerKey, matKey, cx, cy, z0, z1, rTop, rBot = rTop, segs = 24) {
      const h = z1 - z0;
      if (h <= 1e-4) return null;
      const geom = new THREE.CylinderGeometry(rTop, rBot, h, segs);
      geom.translate(cx - CX, z0 + h * 0.5, -(cy - CY));
      const mesh = new THREE.Mesh(geom, matDefs[matKey]);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      mesh.userData = { layer: layerKey, matKey };
      layerGroups[layerKey].add(mesh);
      allMeshes.push(mesh);
      if (isFurnitureMat(matKey)) {
        interiorFurnitureMeshes.push(mesh);
      }
      return mesh;
    }

    function addLuxuryDoor(layerKey, x0, x1, y0, y1, zFlr, zCeil, hingeSide, openAngleRad) {
      const zDoorTop = zFlr + 2.12;
      // 1. Wall Lintel Header above doorway (from +2.12m up to ceiling +2.67m) so walls are continuous and complete
      addBoxXY(layerKey, "mat_interior_wall", x0, x1, y0, y1, zDoorTop, zCeil, false);

      // 2. Zero-Frame Warm Oak/Cashmere Door Jambs & Swing Leaf
      const isHorizontalOpening = (x1 - x0) > (y1 - y0);
      const frameT = 0.035;
      if (isHorizontalOpening) {
        const w = x1 - x0;
        addBoxXY(layerKey, "mat_lux_oak_smooth", x0, x0 + frameT, y0 - 0.01, y1 + 0.01, zFlr, zDoorTop, false);
        addBoxXY(layerKey, "mat_lux_oak_smooth", x1 - frameT, x1, y0 - 0.01, y1 + 0.01, zFlr, zDoorTop, false);
        addBoxXY(layerKey, "mat_lux_oak_smooth", x0, x1, y0 - 0.01, y1 + 0.01, zDoorTop - frameT, zDoorTop, false);
        const leafLen = w - 2 * frameT;
        const hx = hingeSide === "left" ? x0 + frameT : x1 - frameT;
        const hy = 0.5 * (y0 + y1);
        const ux = Math.cos(openAngleRad) * (hingeSide === "left" ? 1 : -1);
        const uy = Math.sin(openAngleRad);
        const nx = -uy, ny = ux;
        addBoxAligned(layerKey, "mat_lux_cabinet_cream", [hx, hy], [ux, uy], [nx, ny], 0, leafLen, -0.022, 0.022, zFlr + 0.01, zDoorTop - frameT, false);
        addBoxAligned(layerKey, "mat_lux_champagne_brass", [hx, hy], [ux, uy], [nx, ny], leafLen - 0.14, leafLen - 0.04, -0.045, 0.045, zFlr + 1.02, zFlr + 1.05, false);
      } else {
        const w = y1 - y0;
        addBoxXY(layerKey, "mat_lux_oak_smooth", x0 - 0.01, x1 + 0.01, y0, y0 + frameT, zFlr, zDoorTop, false);
        addBoxXY(layerKey, "mat_lux_oak_smooth", x0 - 0.01, x1 + 0.01, y1 - frameT, y1, zFlr, zDoorTop, false);
        addBoxXY(layerKey, "mat_lux_oak_smooth", x0 - 0.01, x1 + 0.01, y0, y1, zDoorTop - frameT, zDoorTop, false);
        const leafLen = w - 2 * frameT;
        const hx = 0.5 * (x0 + x1);
        const hy = hingeSide === "bottom" ? y0 + frameT : y1 - frameT;
        const uy = Math.cos(openAngleRad) * (hingeSide === "bottom" ? 1 : -1);
        const ux = Math.sin(openAngleRad);
        const nx = -uy, ny = ux;
        addBoxAligned(layerKey, "mat_lux_cabinet_cream", [hx, hy], [ux, uy], [nx, ny], 0, leafLen, -0.022, 0.022, zFlr + 0.01, zDoorTop - frameT, false);
        addBoxAligned(layerKey, "mat_lux_champagne_brass", [hx, hy], [ux, uy], [nx, ny], leafLen - 0.14, leafLen - 0.04, -0.045, 0.045, zFlr + 1.02, zFlr + 1.05, false);
      }
    }

    function addSheerCurtainPanel(layerKey, x0, x1, y0, y1, zBot, zTop, pleatAxis = "y") {
      const nPleats = 10;
      if (pleatAxis === "y") {
        const step = (y1 - y0) / nPleats;
        for (let i = 0; i < nPleats; i++) {
          const ya = y0 + i * step, yb = ya + step * 0.85;
          const xOff = (i % 2 === 0) ? 0.0 : 0.035;
          addBoxXY(layerKey, "mat_lux_sheer_curtain", x0 + xOff, x1 + xOff, ya, yb, zBot, zTop, false);
        }
      } else {
        const step = (x1 - x0) / nPleats;
        for (let i = 0; i < nPleats; i++) {
          const xa = x0 + i * step, xb = xa + step * 0.85;
          const yOff = (i % 2 === 0) ? 0.0 : 0.035;
          addBoxXY(layerKey, "mat_lux_sheer_curtain", xa, xb, y0 + yOff, y1 + yOff, zBot, zTop, false);
        }
      }
    }

    function buildLuxuryApartmentC(layerKey, zFlr, zCeil) {
      isBuildingInteriorFurniture = true;
      // -----------------------------------------------------------------------
      // 1. CUSTOM FLOORING BY ZONE (120x120 Travertine, Golden-Oak Parquet, Calacatta Baths)
      // -----------------------------------------------------------------------
      // A. Main Public Zone (Living Room, Dining, Kitchen, Foyer & Hallway)
      const publicFloorPoly = [
        [25.35, 11.95], [30.12, 11.95], [30.12, 4.43], [25.85, 4.43],
        [25.85, 7.95], [17.95, 7.95], [17.95, 9.05], [25.35, 9.05]
      ];
      addExtrudedPolygon(layerKey, "mat_lux_travertine_floor", publicFloorPoly, zFlr + 0.004, zFlr + 0.018, false);
      aptCFloorMeshes.push(allMeshes[allMeshes.length - 1]);

      // B. 3 Bedrooms in Light-Grey Architectural Porcelain Flooring
      // Bedroom 1 (South-East Middle: 270x345 cm)
      addBoxXY(layerKey, "mat_lux_travertine_floor", 23.05, 25.75, 4.43, 7.85, zFlr + 0.005, zFlr + 0.019, false);
      aptCFloorMeshes.push(allMeshes[allMeshes.length - 1]);
      // Bedroom 2 (Mamad: 300x325 cm)
      addBoxXY(layerKey, "mat_lux_travertine_floor", 19.85, 22.85, 4.45, 7.75, zFlr + 0.005, zFlr + 0.019, false);
      aptCFloorMeshes.push(allMeshes[allMeshes.length - 1]);
      // Master Bedroom (390x295 cm)
      addBoxXY(layerKey, "mat_lux_travertine_floor", 14.40, 17.85, 4.95, 9.05, zFlr + 0.005, zFlr + 0.019, false);
      aptCFloorMeshes.push(allMeshes[allMeshes.length - 1]);

      // C. Bathrooms & Service Room in Matte Calacatta Porcelain
      addBoxXY(layerKey, "mat_lux_calacatta_marble", 17.45, 19.65, 4.95, 7.85, zFlr + 0.005, zFlr + 0.019, false);
      aptCFloorMeshes.push(allMeshes[allMeshes.length - 1]);
      addBoxXY(layerKey, "mat_lux_calacatta_marble", 12.65, 14.30, 5.18, 7.05, zFlr + 0.005, zFlr + 0.019, false);
      aptCFloorMeshes.push(allMeshes[allMeshes.length - 1]);

      // D. East Sun Balcony Deck (200x500 cm)
      const balCFloor = addBoxXY(layerKey, "mat_terrace_tile", 30.35, 32.52, 6.77, 12.13, zFlr + 0.005, zFlr + 0.020, false);
      aptCFloorMeshes.push(balCFloor);
      if (balCFloor) balconyFloorMeshes.push(balCFloor);

      // -----------------------------------------------------------------------
      // 2. ALL 7 DOORS WITH FULL-HEIGHT HEADERS & ZERO-FRAME LUXURY CASINGS
      // -----------------------------------------------------------------------
      // Entrance Door (Closed, with warm fluted oak inner cladding & brass bar handle)
      addBoxXY(layerKey, "mat_interior_wall", 25.15, 25.35, 10.65, 11.65, zFlr + 2.22, zCeil, false);
      addBoxXY(layerKey, "mat_lux_fluted_oak", 25.24, 25.31, 10.68, 11.62, zFlr + 0.02, zFlr + 2.22, false);
      addBoxXY(layerKey, "mat_lux_champagne_brass", 25.31, 25.34, 10.78, 10.81, zFlr + 0.85, zFlr + 1.55, false);

      // Interior Doors (Open 65°-80° for seamless walkthrough)
      addLuxuryDoor(layerKey, 23.05, 23.95, 7.85, 7.95, zFlr, zCeil, "left",  -1.22); // Bedroom 1 (SE-Mid)
      addLuxuryDoor(layerKey, 19.95, 20.75, 7.75, 7.95, zFlr, zCeil, "left",   1.35); // Mamad Door
      addLuxuryDoor(layerKey, 18.10, 18.90, 7.85, 7.95, zFlr, zCeil, "left",  -1.15); // Main Bath Door
      addLuxuryDoor(layerKey, 18.10, 18.90, 6.10, 6.20, zFlr, zCeil, "left",  -1.10); // Laundry Room Door
      addLuxuryDoor(layerKey, 17.85, 17.95, 8.10, 8.90, zFlr, zCeil, "top",   -1.30); // Master Suite Door
      addLuxuryDoor(layerKey, 14.30, 14.40, 6.25, 7.05, zFlr, zCeil, "top",   -1.18); // Master Bath Door

      // -----------------------------------------------------------------------
      // 3. LIVING ROOM (ח. מגורים 480×400 — Warm Contrast Rug, Bouclé, Oak & Proportional 55" TV)
      // -----------------------------------------------------------------------
      // Woven Greige-Taupe Area Rug (X=27.05..29.66, Y=9.15..11.75) for clear contrast against ivory floor
      addBoxXY(layerKey, "mat_lux_rug_woven", 27.05, 29.66, 9.15, 11.75, zFlr + 0.019, zFlr + 0.032, false);

      // 3-Seater Designer Bouclé Sofa (X=26.85..27.62, Y=9.56..11.62) with warm oak plinth & contrasting mocha/sand pillows
      addBoxXY(layerKey, "mat_lux_oak_smooth",   26.86, 27.61, 9.57, 11.61, zFlr + 0.03, zFlr + 0.12, false); // Warm Oak plinth
      addBoxXY(layerKey, "mat_lux_linen_sand",   26.85, 27.04, 9.56, 11.62, zFlr + 0.12, zFlr + 0.80, false); // Outer back in warm sand
      addBoxXY(layerKey, "mat_lux_linen_sand",   26.85, 27.62, 9.56, 9.78,  zFlr + 0.12, zFlr + 0.62, false); // South Armrest
      addBoxXY(layerKey, "mat_lux_linen_sand",   26.85, 27.62, 11.40, 11.62, zFlr + 0.12, zFlr + 0.62, false); // North Armrest
      for (let i = 0; i < 3; i++) {
        const cy0 = 9.80 + i * 0.53, cy1 = cy0 + 0.51;
        addBoxXY(layerKey, "mat_lux_boucle_cream", 27.02, 27.62, cy0, cy1, zFlr + 0.12, zFlr + 0.42, false);
        addBoxXY(layerKey, "mat_lux_linen_sand",   27.03, 27.20, cy0 + 0.02, cy1 - 0.02, zFlr + 0.42, zFlr + 0.82, false);
      }
      addBoxXY(layerKey, "mat_lux_pillow_taupe", 27.16, 27.36, 9.85, 10.18, zFlr + 0.42, zFlr + 0.72, false);
      addBoxXY(layerKey, "mat_lux_pillow_taupe", 27.16, 27.36, 11.00, 11.33, zFlr + 0.42, zFlr + 0.72, false);

      // Pair of Lounge Armchairs (X=27.55..28.18 & 28.45..29.08, Y=8.88..9.58) with warm oak arms & mocha cushions
      [[27.55, 28.18], [28.45, 29.08]].forEach(([ax0, ax1]) => {
        addBoxXY(layerKey, "mat_lux_oak_smooth",   ax0 + 0.02, ax1 - 0.02, 8.88, 9.56, zFlr + 0.03, zFlr + 0.13, false);
        addBoxXY(layerKey, "mat_lux_linen_sand",   ax0, ax1, 8.88, 9.04, zFlr + 0.13, zFlr + 0.76, false); // Back
        addBoxXY(layerKey, "mat_lux_oak_smooth",   ax0, ax0 + 0.10, 8.88, 9.56, zFlr + 0.13, zFlr + 0.56, false); // Oak Arm W
        addBoxXY(layerKey, "mat_lux_oak_smooth",   ax1 - 0.10, ax1, 8.88, 9.56, zFlr + 0.13, zFlr + 0.56, false); // Oak Arm E
        addBoxXY(layerKey, "mat_lux_boucle_cream", ax0 + 0.10, ax1 - 0.10, 9.02, 9.56, zFlr + 0.13, zFlr + 0.41, false); // Seat
        addBoxXY(layerKey, "mat_lux_pillow_taupe", ax0 + 0.14, ax1 - 0.14, 9.04, 9.18, zFlr + 0.41, zFlr + 0.72, false); // Cushion
      });

      // Sculptural Travertine & Warm Oak Coffee Table (X=27.78..28.54, Y=10.18..10.98)
      addCylinder3D(layerKey, "mat_lux_fluted_oak", 28.00, 10.42, zFlr + 0.03, zFlr + 0.35, 0.16);
      addCylinder3D(layerKey, "mat_lux_fluted_oak", 28.32, 10.74, zFlr + 0.03, zFlr + 0.35, 0.14);
      addBoxXY(layerKey, "mat_lux_calacatta_marble", 27.78, 28.54, 10.18, 10.98, zFlr + 0.35, zFlr + 0.40, false);
      addCylinder3D(layerKey, "mat_lux_champagne_brass", 28.16, 10.60, zFlr + 0.40, zFlr + 0.42, 0.16);
      addCylinder3D(layerKey, "mat_lux_ceramic_white",   28.16, 10.60, zFlr + 0.42, zFlr + 0.62, 0.05, 0.07);
      addCylinder3D(layerKey, "mat_lux_plant_olive",     28.16, 10.60, zFlr + 0.60, zFlr + 0.76, 0.12, 0.04);

      // North Media Wall: Subtle Fluted-Oak Accent Strip + Slim Floating Console + Proportional 55" TV (105×58 cm)
      addBoxXY(layerKey, "mat_lux_fluted_oak",       27.35, 27.75, 11.89, 11.94, zFlr + 0.02, zCeil - 0.12, false);
      // Slim Floating Media Console in Warm Oak & Cashmere
      addBoxXY(layerKey, "mat_lux_oak_smooth",       27.45, 29.15, 11.60, 11.89, zFlr + 0.26, zFlr + 0.46, false);
      addBoxXY(layerKey, "mat_lux_calacatta_marble", 27.44, 29.16, 11.59, 11.90, zFlr + 0.46, zFlr + 0.49, false);
      // Proportional 55-inch OLED TV (width 1.05m, height 0.58m) centered above console
      addBoxXY(layerKey, "mat_lux_dark_glass",       27.82, 28.87, 11.84, 11.87, zFlr + 0.86, zFlr + 1.44, false);
      addBoxXY(layerKey, "mat_lux_champagne_brass",  27.81, 28.88, 11.85, 11.86, zFlr + 0.85, zFlr + 0.86, false);

      // Sheer Linen Drapes flanking the East Living Room Balcony Vitrina
      addSheerCurtainPanel(layerKey, 29.95, 30.08, 7.65, 8.25,  zFlr + 0.02, zCeil - 0.04, "y");
      addSheerCurtainPanel(layerKey, 29.95, 30.08, 10.95, 11.75, zFlr + 0.02, zCeil - 0.04, "y");

      // -----------------------------------------------------------------------
      // 4. LUXURY KITCHEN, SLIM ISLAND & PROPORTIONAL DINING AREA (מטבח, אי ופינת אוכל)
      // -----------------------------------------------------------------------
      // A. Tall Appliance Wall on North-West of Kitchen (X=25.85..26.48, Y=6.15..7.83): Fridge + Oven Tower
      addBoxXY(layerKey, "mat_lux_cabinet_cream",   25.85, 26.48, 6.15, 7.83, zFlr + 0.02, zCeil - 0.28, false);
      addBoxXY(layerKey, "mat_lux_champagne_brass", 26.48, 26.50, 6.88, 6.91, zFlr + 0.80, zFlr + 1.65, false);
      addBoxXY(layerKey, "mat_lux_champagne_brass", 26.48, 26.50, 6.95, 6.98, zFlr + 0.80, zFlr + 1.65, false);
      addBoxXY(layerKey, "mat_lux_dark_glass",      26.47, 26.50, 6.24, 6.80, zFlr + 0.85, zFlr + 1.42, false);
      addBoxXY(layerKey, "mat_lux_dark_glass",      26.47, 26.50, 6.24, 6.80, zFlr + 1.48, zFlr + 1.86, false);
      addBoxXY(layerKey, "mat_lux_champagne_brass", 26.49, 26.51, 6.28, 6.76, zFlr + 1.38, zFlr + 1.40, false);

      // B. West & South Lower Kitchen Cabinetry (Warm Cashmere-Greige + Honey-Oak Base) & Calacatta Countertop
      addBoxXY(layerKey, "mat_lux_cabinet_cream",    25.85, 26.46, 4.50, 6.15, zFlr + 0.02, zFlr + 0.87, false);
      addBoxXY(layerKey, "mat_lux_calacatta_marble", 25.85, 26.48, 4.50, 6.15, zFlr + 0.87, zFlr + 0.91, false);
      addBoxXY(layerKey, "mat_lux_cabinet_cream",    26.46, 28.30, 4.50, 5.10, zFlr + 0.02, zFlr + 0.87, false);
      addBoxXY(layerKey, "mat_lux_calacatta_marble", 26.46, 28.30, 4.50, 5.12, zFlr + 0.87, zFlr + 0.91, false);
      // Calacatta Marble Backsplash on West Wall + Warm Fluted-Oak Upper Cabinets
      addBoxXY(layerKey, "mat_lux_calacatta_marble", 25.85, 25.89, 4.50, 6.15, zFlr + 0.91, zFlr + 1.55, false);
      addBoxXY(layerKey, "mat_lux_fluted_oak",       25.85, 26.23, 4.50, 6.15, zFlr + 1.55, zCeil - 0.28, false);
      addBoxXY(layerKey, "mat_lux_glow_warm",        26.16, 26.20, 4.55, 6.10, zFlr + 1.53, zFlr + 1.55, false);
      // 4-Zone Black Glass Induction Cooktop on West Counter (X=25.95..26.40, Y=5.07..5.67)
      addBoxXY(layerKey, "mat_lux_dark_glass",       25.95, 26.40, 5.07, 5.67, zFlr + 0.91, zFlr + 0.92, false);
      // Undermount Sink & Champagne-Brass Arched Faucet on South Counter (X=26.78..27.38, Y=4.58..5.00)
      addBoxXY(layerKey, "mat_lux_ceramic_white",    26.78, 27.38, 4.58, 5.00, zFlr + 0.86, zFlr + 0.915, false);
      addCylinder3D(layerKey, "mat_lux_champagne_brass", 27.08, 4.56, zFlr + 0.91, zFlr + 1.22, 0.016);
      addBoxXY(layerKey, "mat_lux_champagne_brass",  27.06, 27.10, 4.56, 4.75, zFlr + 1.20, zFlr + 1.23, false);

      // C. Proportional Waterfall Kitchen Island (56×106 cm: X=27.18..27.74, Y=6.38..7.44) + 2 Compact Bar Stools
      addBoxXY(layerKey, "mat_lux_fluted_oak",       27.22, 27.68, 6.42, 7.40, zFlr + 0.02, zFlr + 0.88, false);
      addBoxXY(layerKey, "mat_lux_calacatta_marble", 27.18, 27.74, 6.38, 7.44, zFlr + 0.88, zFlr + 0.92, false);
      addBoxXY(layerKey, "mat_lux_calacatta_marble", 27.18, 27.74, 6.38, 6.43, zFlr + 0.02, zFlr + 0.88, false);
      addBoxXY(layerKey, "mat_lux_calacatta_marble", 27.18, 27.74, 7.39, 7.44, zFlr + 0.02, zFlr + 0.88, false);
      // 2 Compact Low-Profile Bar Stools tucked cleanly on East side of Island (X=27.74..27.98)
      [6.64, 7.18].forEach(sy => {
        addCylinder3D(layerKey, "mat_lux_oak_smooth",  27.84, sy, zFlr + 0.02, zFlr + 0.62, 0.025, 0.13);
        addCylinder3D(layerKey, "mat_lux_linen_sand",  27.84, sy, zFlr + 0.62, zFlr + 0.68, 0.15);
      });
      // 2 Slim Champagne-Brass Pendant Lamps over Island
      [6.64, 7.18].forEach(py => {
        addCylinder3D(layerKey, "mat_lux_champagne_brass", 27.46, py, zFlr + 1.84, zCeil, 0.006);
        addCylinder3D(layerKey, "mat_lux_champagne_brass", 27.46, py, zFlr + 1.74, zFlr + 1.84, 0.06, 0.03);
        addCylinder3D(layerKey, "mat_lux_glow_warm",       27.46, py, zFlr + 1.70, zFlr + 1.74, 0.05);
      });

      // D. Proportional, Compact Dining Area (פ. אוכל — 72×116 cm Table at X=28.88..29.60, Y=5.08..6.24 + 4 Compact Chairs)
      addCylinder3D(layerKey, "mat_lux_fluted_oak", 29.24, 5.36, zFlr + 0.02, zFlr + 0.72, 0.12, 0.15);
      addCylinder3D(layerKey, "mat_lux_fluted_oak", 29.24, 5.96, zFlr + 0.02, zFlr + 0.72, 0.12, 0.15);
      addBoxXY(layerKey, "mat_lux_calacatta_marble", 28.88, 29.60, 5.08, 6.24, zFlr + 0.72, zFlr + 0.76, false);
      // 4 Compact Upholstered Dining Chairs (2 West, 2 East) leaving generous room circulation
      [5.35, 5.95].forEach(cy => {
        // West chair facing East
        addBoxXY(layerKey, "mat_lux_oak_smooth",  28.64, 28.86, cy - 0.15, cy + 0.15, zFlr + 0.02, zFlr + 0.43, false);
        addBoxXY(layerKey, "mat_lux_linen_sand",  28.62, 28.88, cy - 0.16, cy + 0.16, zFlr + 0.43, zFlr + 0.48, false);
        addBoxXY(layerKey, "mat_lux_oak_smooth",  28.60, 28.66, cy - 0.16, cy + 0.16, zFlr + 0.48, zFlr + 0.79, false);
        // East chair facing West
        addBoxXY(layerKey, "mat_lux_oak_smooth",  29.62, 29.84, cy - 0.15, cy + 0.15, zFlr + 0.02, zFlr + 0.43, false);
        addBoxXY(layerKey, "mat_lux_linen_sand",  29.60, 29.86, cy - 0.16, cy + 0.16, zFlr + 0.43, zFlr + 0.48, false);
        addBoxXY(layerKey, "mat_lux_oak_smooth",  29.82, 29.88, cy - 0.16, cy + 0.16, zFlr + 0.48, zFlr + 0.79, false);
      });
      // Refined 26cm Pendant Lamp above Dining Table
      addCylinder3D(layerKey, "mat_lux_champagne_brass", 29.24, 5.66, zFlr + 1.85, zCeil, 0.008);
      addCylinder3D(layerKey, "mat_lux_champagne_brass", 29.24, 5.66, zFlr + 1.78, zFlr + 1.85, 0.24, 0.24);
      addCylinder3D(layerKey, "mat_lux_glow_warm",       29.24, 5.66, zFlr + 1.74, zFlr + 1.78, 0.22, 0.22);

      // -----------------------------------------------------------------------
      // 5. EAST SUN BALCONY (מרפסת שמש 200×500 — Outdoor Lounge & Olive Trees)
      // -----------------------------------------------------------------------
      addBoxXY(layerKey, "mat_lux_oak_smooth",   31.55, 32.25, 8.80, 11.10, zFlr + 0.03, zFlr + 0.34, false);
      addBoxXY(layerKey, "mat_lux_boucle_cream", 31.55, 32.15, 8.80, 11.10, zFlr + 0.34, zFlr + 0.44, false);
      addBoxXY(layerKey, "mat_lux_linen_sand",   32.10, 32.25, 8.80, 11.10, zFlr + 0.34, zFlr + 0.74, false);
      addCylinder3D(layerKey, "mat_lux_calacatta_marble", 31.10, 9.95, zFlr + 0.03, zFlr + 0.38, 0.26);
      [[31.95, 7.20], [31.95, 11.70]].forEach(([px, py]) => {
        addCylinder3D(layerKey, "mat_lux_ceramic_white", px, py, zFlr + 0.02, zFlr + 0.55, 0.26, 0.20);
        addCylinder3D(layerKey, "mat_lux_oak_smooth",    px, py, zFlr + 0.55, zFlr + 1.35, 0.04, 0.05);
        addCylinder3D(layerKey, "mat_lux_plant_olive",   px, py, zFlr + 1.20, zFlr + 1.90, 0.44, 0.28);
      });

      // -----------------------------------------------------------------------
      // 6. MASTER SUITE (יחידת הורים 390×295 — South Window 100% Visible & Unobstructed!)
      // -----------------------------------------------------------------------
      // Warm Woven Area Rug under Bed
      addBoxXY(layerKey, "mat_lux_rug_woven", 14.90, 17.10, 5.20, 7.25, zFlr + 0.020, zFlr + 0.032, false);
      // Low Designer Headboard in Warm Oak & Sand Linen (zFlr + 0.03 .. zFlr + 0.74 — strictly 11cm BELOW the South window sill at zFlr + 0.85 so 100% of the window is exposed!)
      addBoxXY(layerKey, "mat_lux_fluted_oak",   14.65, 17.25, 5.04, 5.11, zFlr + 0.02, zFlr + 0.72, false);
      addBoxXY(layerKey, "mat_lux_linen_sand",   15.12, 16.78, 5.11, 5.20, zFlr + 0.30, zFlr + 0.74, false);
      // King-Size Bed Frame, Crisp White Mattress & Contrasting Mocha/Sand Duvet Runner
      addBoxXY(layerKey, "mat_lux_oak_smooth",    15.10, 16.80, 5.20, 7.05, zFlr + 0.03, zFlr + 0.30, false); // Warm Oak Bed frame
      addBoxXY(layerKey, "mat_lux_ceramic_white", 15.16, 16.74, 5.22, 6.98, zFlr + 0.30, zFlr + 0.50, false); // Mattress
      addBoxXY(layerKey, "mat_lux_pillow_taupe",  15.14, 16.76, 6.00, 7.00, zFlr + 0.32, zFlr + 0.52, false); // Contrasting Mocha-Taupe runner
      // 4 Pillows (sitting at zFlr + 0.50..0.64, well below the zFlr + 0.85 window sill)
      addBoxXY(layerKey, "mat_lux_boucle_cream", 15.22, 15.90, 5.22, 5.56, zFlr + 0.50, zFlr + 0.64, false);
      addBoxXY(layerKey, "mat_lux_boucle_cream", 16.00, 16.68, 5.22, 5.56, zFlr + 0.50, zFlr + 0.64, false);
      addBoxXY(layerKey, "mat_lux_pillow_taupe", 15.30, 15.85, 5.50, 5.76, zFlr + 0.50, zFlr + 0.62, false);
      addBoxXY(layerKey, "mat_lux_pillow_taupe", 16.05, 16.60, 5.50, 5.76, zFlr + 0.50, zFlr + 0.62, false);
      // 2 Floating Oak Nightstands flanking the South window (at X=14.80 and X=17.05, no hanging cords near window)
      [[14.55, 15.05], [16.85, 17.30]].forEach(([nx0, nx1]) => {
        const cx = 0.5 * (nx0 + nx1);
        addBoxXY(layerKey, "mat_lux_oak_smooth",       nx0, nx1, 5.10, 5.50, zFlr + 0.28, zFlr + 0.48, false);
        addBoxXY(layerKey, "mat_lux_calacatta_marble", nx0, nx1, 5.10, 5.51, zFlr + 0.48, zFlr + 0.51, false);
        addCylinder3D(layerKey, "mat_lux_champagne_brass", cx, 5.30, zFlr + 0.51, zFlr + 0.62, 0.015);
        addCylinder3D(layerKey, "mat_lux_glow_warm",       cx, 5.30, zFlr + 0.62, zFlr + 0.74, 0.075);
      });
      // Floor-to-Ceiling Custom 4-Door Wardrobe on North Wall (X=14.40..16.50, Y=8.40..9.03)
      addBoxXY(layerKey, "mat_lux_cabinet_cream", 14.40, 16.50, 8.40, 9.03, zFlr + 0.02, zCeil - 0.08, false);
      addBoxXY(layerKey, "mat_lux_fluted_oak",    16.50, 17.05, 8.40, 9.03, zFlr + 0.02, zCeil - 0.08, false);
      [14.92, 15.45, 15.98].forEach(wx => {
        addBoxXY(layerKey, "mat_lux_champagne_brass", wx - 0.01, wx + 0.01, 8.38, 8.40, zFlr + 0.85, zFlr + 1.65, false);
      });

      // Master En-Suite Bathroom (X=12.65..14.30, Y=5.18..7.05)
      addBoxXY(layerKey, "mat_lux_clear_glass",     13.48, 13.52, 5.18, 6.10, zFlr + 0.02, zFlr + 2.10, false);
      addBoxXY(layerKey, "mat_lux_champagne_brass", 12.68, 13.05, 5.55, 5.59, zFlr + 2.05, zFlr + 2.08, false);
      addBoxXY(layerKey, "mat_lux_fluted_oak",       12.65, 13.15, 6.25, 6.95, zFlr + 0.42, zFlr + 0.82, false);
      addBoxXY(layerKey, "mat_lux_calacatta_marble", 12.65, 13.17, 6.25, 6.95, zFlr + 0.82, zFlr + 0.86, false);
      addCylinder3D(layerKey, "mat_lux_ceramic_white", 12.92, 6.60, zFlr + 0.86, zFlr + 0.96, 0.16);
      addBoxXY(layerKey, "mat_lux_mirror",           12.66, 12.70, 6.28, 6.92, zFlr + 1.05, zFlr + 1.95, false);
      addBoxXY(layerKey, "mat_lux_ceramic_white",    13.72, 14.10, 5.20, 5.72, zFlr + 0.18, zFlr + 0.43, false);

      // -----------------------------------------------------------------------
      // 7. BEDROOM 1 (SOUTH BEDROOM — 270×345 cm) & BEDROOM 2 (MAMAD — 300×325 cm)
      // -----------------------------------------------------------------------
      // Bedroom 1 (X=23.05..25.75, Y=4.45..7.85)
      addBoxXY(layerKey, "mat_lux_cabinet_cream",   24.25, 25.75, 7.25, 7.85, zFlr + 0.02, zCeil - 0.10, false); // Wardrobe
      addBoxXY(layerKey, "mat_lux_champagne_brass", 24.98, 25.02, 7.23, 7.25, zFlr + 0.85, zFlr + 1.60, false);
      addBoxXY(layerKey, "mat_lux_rug_woven",       23.80, 25.65, 4.60, 6.45, zFlr + 0.020, zFlr + 0.030, false);
      addBoxXY(layerKey, "mat_lux_oak_smooth",      24.85, 25.73, 4.48, 6.30, zFlr + 0.03, zFlr + 0.32, false); // Bed base
      addBoxXY(layerKey, "mat_lux_ceramic_white",   24.90, 25.70, 4.52, 6.24, zFlr + 0.32, zFlr + 0.52, false); // Mattress
      addBoxXY(layerKey, "mat_lux_pillow_taupe",    24.88, 25.72, 5.50, 6.26, zFlr + 0.34, zFlr + 0.54, false); // Mocha throw
      addBoxXY(layerKey, "mat_lux_linen_sand",      24.88, 25.72, 4.46, 4.56, zFlr + 0.32, zFlr + 0.82, false); // Low headboard
      addBoxXY(layerKey, "mat_lux_pillow_taupe",    25.02, 25.60, 4.58, 4.88, zFlr + 0.52, zFlr + 0.65, false); // Pillow
      addBoxXY(layerKey, "mat_lux_oak_smooth",      23.06, 23.62, 4.75, 5.65, zFlr + 0.70, zFlr + 0.75, false); // Study Desk
      addBoxXY(layerKey, "mat_lux_oak_smooth",      23.06, 23.62, 4.75, 4.82, zFlr + 0.02, zFlr + 0.70, false);
      addCylinder3D(layerKey, "mat_lux_linen_sand", 23.82, 5.20, zFlr + 0.42, zFlr + 0.48, 0.19); // Desk Chair

      // Bedroom 2 — Mamad (X=19.85..22.85, Y=4.45..7.75)
      addBoxXY(layerKey, "mat_lux_cabinet_cream",   21.32, 22.82, 7.12, 7.72, zFlr + 0.02, zCeil - 0.10, false); // Wardrobe
      addBoxXY(layerKey, "mat_lux_champagne_brass", 22.05, 22.09, 7.10, 7.12, zFlr + 0.85, zFlr + 1.60, false);
      addBoxXY(layerKey, "mat_lux_rug_woven",       20.75, 22.75, 4.65, 6.50, zFlr + 0.020, zFlr + 0.030, false);
      addBoxXY(layerKey, "mat_lux_oak_smooth",      21.95, 22.82, 4.55, 6.42, zFlr + 0.03, zFlr + 0.32, false); // Bed base
      addBoxXY(layerKey, "mat_lux_ceramic_white",   22.00, 22.78, 4.60, 6.36, zFlr + 0.32, zFlr + 0.52, false); // Mattress
      addBoxXY(layerKey, "mat_lux_pillow_taupe",    21.98, 22.80, 5.60, 6.38, zFlr + 0.34, zFlr + 0.54, false); // Mocha throw
      addBoxXY(layerKey, "mat_lux_linen_sand",      21.95, 22.82, 4.55, 4.65, zFlr + 0.32, zFlr + 0.82, false); // Low headboard
      addBoxXY(layerKey, "mat_lux_pillow_taupe",    22.10, 22.68, 4.68, 4.98, zFlr + 0.52, zFlr + 0.65, false); // Pillow
      addBoxXY(layerKey, "mat_lux_oak_smooth",      19.90, 20.50, 4.55, 5.75, zFlr + 0.70, zFlr + 0.75, false); // Desk
      addBoxXY(layerKey, "mat_lux_oak_smooth",      19.90, 20.50, 4.55, 4.62, zFlr + 0.02, zFlr + 0.70, false);
      addCylinder3D(layerKey, "mat_lux_linen_sand", 20.72, 5.15, zFlr + 0.42, zFlr + 0.48, 0.19); // Chair

      // -----------------------------------------------------------------------
      // 8. MAIN FAMILY BATHROOM & SERVICE LAUNDRY ROOM (ח. רחצה כללי וח. שירות)
      // -----------------------------------------------------------------------
      addBoxXY(layerKey, "mat_lux_calacatta_marble", 18.95, 19.64, 6.20, 7.84, zFlr + 0.02, zFlr + 0.54, false);
      addBoxXY(layerKey, "mat_lux_ceramic_white",    19.03, 19.58, 6.28, 7.76, zFlr + 0.54, zFlr + 0.57, false);
      addBoxXY(layerKey, "mat_lux_clear_glass",      18.95, 18.98, 7.05, 7.84, zFlr + 0.55, zFlr + 2.05, false);
      addBoxXY(layerKey, "mat_lux_fluted_oak",       17.46, 17.96, 7.10, 7.78, zFlr + 0.42, zFlr + 0.82, false);
      addBoxXY(layerKey, "mat_lux_calacatta_marble", 17.46, 17.98, 7.10, 7.78, zFlr + 0.82, zFlr + 0.86, false);
      addCylinder3D(layerKey, "mat_lux_ceramic_white", 17.72, 7.44, zFlr + 0.86, zFlr + 0.96, 0.16);
      addBoxXY(layerKey, "mat_lux_mirror",           17.46, 17.50, 7.12, 7.76, zFlr + 1.05, zFlr + 1.95, false);
      addBoxXY(layerKey, "mat_lux_ceramic_white",    17.46, 17.98, 6.42, 6.78, zFlr + 0.18, zFlr + 0.43, false);
      addBoxXY(layerKey, "mat_lux_cabinet_cream",    18.95, 19.62, 5.12, 5.82, zFlr + 0.02, zFlr + 1.85, false);

      // -----------------------------------------------------------------------
      // 9. DROPPED GYPSUM CEILING SOFFITS, MAGNETIC TRACKS & WARM INTERIOR LIGHTS
      // -----------------------------------------------------------------------
      addBoxXY(layerKey, "mat_interior_wall", 25.85, 26.55, 4.45, 7.95, zCeil - 0.28, zCeil, false); // Above West kitchen
      addBoxXY(layerKey, "mat_interior_wall", 17.95, 25.85, 7.95, 9.05, zCeil - 0.24, zCeil, false); // Hallway AC soffit
      addBoxXY(layerKey, "mat_lux_dark_glass", 27.55, 29.25, 9.55, 9.61,  zCeil - 0.03, zCeil, false);
      addBoxXY(layerKey, "mat_lux_dark_glass", 27.55, 29.25, 11.35, 11.41, zCeil - 0.03, zCeil, false);
      addBoxXY(layerKey, "mat_lux_dark_glass", 29.19, 29.25, 9.55, 11.41, zCeil - 0.03, zCeil, false);

      // Hallway Framed Artworks on North Wall (Y=9.03)
      [19.20, 21.60, 23.80].forEach(ax => {
        addBoxXY(layerKey, "mat_lux_champagne_brass", ax - 0.46, ax + 0.46, 9.01, 9.04, zFlr + 1.13, zFlr + 1.97, false);
        addBoxXY(layerKey, "mat_lux_linen_sand",      ax - 0.43, ax + 0.43, 9.00, 9.02, zFlr + 1.16, zFlr + 1.94, false);
      });

      // Warm Interior PointLights for Luxury Real-Time Illumination
      const lightCoords = [
        [28.35, 10.50, zCeil - 0.25, 0.68, 9.5], // Living Room
        [27.55, 6.85,  zCeil - 0.35, 0.55, 7.5], // Kitchen & Island
        [29.20, 5.65,  zCeil - 0.40, 0.55, 7.5], // Dining Area
        [21.80, 8.50,  zCeil - 0.30, 0.42, 7.0], // Hallway
        [15.95, 6.50,  zCeil - 0.25, 0.62, 7.5], // Master Bedroom
        [24.40, 6.10,  zCeil - 0.25, 0.48, 6.5], // South Bedroom
        [21.35, 6.10,  zCeil - 0.25, 0.48, 6.5]  // Mamad Bedroom
      ];
      lightCoords.forEach(([lx, ly, lz, intensity, dist]) => {
        const ptLight = new THREE.PointLight(0xfff5e4, intensity, dist, 1.6);
        ptLight.position.copy(cadTo3D(lx, ly, lz));
        ptLight.userData = { baseIntensity: intensity };
        layerGroups[layerKey].add(ptLight);
        interiorPointLights.push(ptLight);
      });
      isBuildingInteriorFurniture = false;
    }

    // =========================================================================
    // LUXURY ARCHITECTURAL SALES MODEL OF APARTMENT A (4 ROOMS, NORTH-EAST)
    // =========================================================================
    function addBoxAptA(layerKey, matKey, u0, u1, v0, v1, z0, z1, withEdges = false) {
      return addBoxAligned(layerKey, matKey, APT_A_O, APT_A_U, APT_A_V, u0, u1, v0, v1, z0, z1, withEdges);
    }

    function addCylAptA(layerKey, matKey, cu, cv, z0, z1, rTop, rBot = rTop, segs = 24) {
      const [cx, cy] = aptA_XY(cu, cv);
      return addCylinder3D(layerKey, matKey, cx, cy, z0, z1, rTop, rBot, segs);
    }

    function addLuxuryDoorAptA(layerKey, u0, u1, v0, v1, zFlr, zCeil, hingeSide, openAngleRad) {
      const zDoorTop = zFlr + 2.12;
      // 1. Wall Lintel Header above doorway (from +2.12m up to ceiling +2.67m) so interior walls are continuous and complete
      addBoxAptA(layerKey, "mat_interior_wall", u0, u1, v0, v1, zDoorTop, zCeil, false);

      // 2. Zero-Frame Warm Oak/Cashmere Door Jambs & Swing Leaf in Apartment A's rotated coordinate system
      const isHorizontalOpening = (u1 - u0) > (v1 - v0);
      const frameT = 0.035;
      if (isHorizontalOpening) {
        const w = u1 - u0;
        addBoxAptA(layerKey, "mat_lux_oak_smooth", u0, u0 + frameT, v0 - 0.01, v1 + 0.01, zFlr, zDoorTop, false);
        addBoxAptA(layerKey, "mat_lux_oak_smooth", u1 - frameT, u1, v0 - 0.01, v1 + 0.01, zFlr, zDoorTop, false);
        addBoxAptA(layerKey, "mat_lux_oak_smooth", u0, u1, v0 - 0.01, v1 + 0.01, zDoorTop - frameT, zDoorTop, false);
        const leafLen = w - 2 * frameT;
        const hu = hingeSide === "left" ? u0 + frameT : u1 - frameT;
        const hv = 0.5 * (v0 + v1);
        const hXY = aptA_XY(hu, hv);
        const c = Math.cos(openAngleRad) * (hingeSide === "left" ? 1 : -1);
        const s = Math.sin(openAngleRad);
        const ux = c * APT_A_U[0] + s * APT_A_V[0];
        const uy = c * APT_A_U[1] + s * APT_A_V[1];
        const nx = -uy, ny = ux;
        addBoxAligned(layerKey, "mat_lux_cabinet_cream", hXY, [ux, uy], [nx, ny], 0, leafLen, -0.022, 0.022, zFlr + 0.01, zDoorTop - frameT, false);
        addBoxAligned(layerKey, "mat_lux_champagne_brass", hXY, [ux, uy], [nx, ny], leafLen - 0.14, leafLen - 0.04, -0.045, 0.045, zFlr + 1.02, zFlr + 1.05, false);
      } else {
        const w = v1 - v0;
        addBoxAptA(layerKey, "mat_lux_oak_smooth", u0 - 0.01, u1 + 0.01, v0, v0 + frameT, zFlr, zDoorTop, false);
        addBoxAptA(layerKey, "mat_lux_oak_smooth", u0 - 0.01, u1 + 0.01, v1 - frameT, v1, zFlr, zDoorTop, false);
        addBoxAptA(layerKey, "mat_lux_oak_smooth", u0 - 0.01, u1 + 0.01, v0, v1, zDoorTop - frameT, zDoorTop, false);
        const leafLen = w - 2 * frameT;
        const hu = 0.5 * (u0 + u1);
        const hv = hingeSide === "bottom" ? v0 + frameT : v1 - frameT;
        const hXY = aptA_XY(hu, hv);
        const c = Math.cos(openAngleRad) * (hingeSide === "bottom" ? 1 : -1);
        const s = Math.sin(openAngleRad);
        const ux = s * APT_A_U[0] + c * APT_A_V[0];
        const uy = s * APT_A_U[1] + c * APT_A_V[1];
        const nx = -uy, ny = ux;
        addBoxAligned(layerKey, "mat_lux_cabinet_cream", hXY, [ux, uy], [nx, ny], 0, leafLen, -0.022, 0.022, zFlr + 0.01, zDoorTop - frameT, false);
        addBoxAligned(layerKey, "mat_lux_champagne_brass", hXY, [ux, uy], [nx, ny], leafLen - 0.14, leafLen - 0.04, -0.045, 0.045, zFlr + 1.02, zFlr + 1.05, false);
      }
    }

    function addSheerCurtainAptA(layerKey, u0, u1, v0, v1, zBot, zTop) {
      const nPleats = 9;
      const step = (u1 - u0) / nPleats;
      for (let i = 0; i < nPleats; i++) {
        const ua = u0 + i * step, ub = ua + step * 0.85;
        const vOff = (i % 2 === 0) ? 0.0 : -0.035;
        addBoxAptA(layerKey, "mat_lux_sheer_curtain", ua, ub, v0 + vOff, v1 + vOff, zBot, zTop, false);
      }
    }

    function buildLuxuryApartmentA(layerKey, zFlr, zCeil) {
      isBuildingInteriorFurniture = true;
      // -----------------------------------------------------------------------
      // 1. CUSTOM FLOORING BY ZONE (120x120 Travertine, Golden-Oak Parquet, Calacatta Baths)
      // -----------------------------------------------------------------------
      // A. Main Public Zone (Kitchen, Living Room, Entrance Foyer, Dining & Hallway)
      addBoxAptA(layerKey, "mat_lux_travertine_floor", 0.81, 7.51, 2.38, 5.82, zFlr + 0.004, zFlr + 0.018, false);
      aptCFloorMeshes.push(allMeshes[allMeshes.length - 1]);
      addBoxAptA(layerKey, "mat_lux_travertine_floor", 4.06, 7.76, -0.32, 2.38, zFlr + 0.004, zFlr + 0.018, false);
      aptCFloorMeshes.push(allMeshes[allMeshes.length - 1]);
      addBoxAptA(layerKey, "mat_lux_travertine_floor", 7.51, 11.46, 2.03, 3.03, zFlr + 0.004, zFlr + 0.018, false);
      aptCFloorMeshes.push(allMeshes[allMeshes.length - 1]);
      addBoxAptA(layerKey, "mat_lux_travertine_floor", 9.86, 11.46, 0.28, 2.03, zFlr + 0.004, zFlr + 0.018, false);
      aptCFloorMeshes.push(allMeshes[allMeshes.length - 1]);

      // B. 3 Bedrooms in Light-Grey Architectural Porcelain Flooring
      // Master Bedroom (385x290 cm: u=7.66..11.46, v=3.13..6.20)
      addBoxAptA(layerKey, "mat_lux_travertine_floor", 7.66, 11.46, 3.13, 6.20, zFlr + 0.005, zFlr + 0.019, false);
      aptCFloorMeshes.push(allMeshes[allMeshes.length - 1]);
      // Bedroom 2 — Mamad (337x280 cm: u=11.66..15.18, v=1.68..4.58)
      addBoxAptA(layerKey, "mat_lux_travertine_floor", 11.66, 15.18, 1.68, 4.58, zFlr + 0.005, zFlr + 0.019, false);
      aptCFloorMeshes.push(allMeshes[allMeshes.length - 1]);
      // Bedroom 3 — East Bedroom (340x280 cm: u=11.66..15.18, v=-1.41..1.38)
      addBoxAptA(layerKey, "mat_lux_travertine_floor", 11.66, 15.18, -1.41, 1.38, zFlr + 0.005, zFlr + 0.019, false);
      aptCFloorMeshes.push(allMeshes[allMeshes.length - 1]);

      // C. Bathrooms & Service Laundry Room in Matte Calacatta Porcelain
      addBoxAptA(layerKey, "mat_lux_calacatta_marble", 11.56, 13.48, 4.60, 6.20, zFlr + 0.005, zFlr + 0.019, false);
      aptCFloorMeshes.push(allMeshes[allMeshes.length - 1]);
      addBoxAptA(layerKey, "mat_lux_calacatta_marble", 9.86, 11.46, -3.11, 0.18, zFlr + 0.005, zFlr + 0.019, false);
      aptCFloorMeshes.push(allMeshes[allMeshes.length - 1]);
      addBoxAptA(layerKey, "mat_lux_calacatta_marble", 11.56, 15.18, -3.11, -1.58, zFlr + 0.005, zFlr + 0.019, false);
      aptCFloorMeshes.push(allMeshes[allMeshes.length - 1]);

      // D. North-Central Sun Balcony Deck (BALCONY_NC)
      const balAFloor = addExtrudedPolygon(layerKey, "mat_terrace_tile", BALCONY_NC, zFlr + 0.005, zFlr + 0.020, false);
      aptCFloorMeshes.push(balAFloor);
      if (balAFloor) balconyFloorMeshes.push(balAFloor);

      // -----------------------------------------------------------------------
      // 2. ALL 7 DOORS OF APARTMENT A WITH FULL-HEIGHT LINTEL HEADERS
      // -----------------------------------------------------------------------
      // Entrance Door (Closed, with warm fluted honey-oak inner cladding & brass bar handle)
      addBoxAptA(layerKey, "mat_interior_wall",     4.16, 5.16, -0.52, -0.32, zFlr + 2.22, zCeil, false);
      addBoxAptA(layerKey, "mat_lux_fluted_oak",    4.18, 5.14, -0.45, -0.36, zFlr + 0.02, zFlr + 2.22, false);
      addBoxAptA(layerKey, "mat_lux_champagne_brass", 4.96, 4.99, -0.36, -0.32, zFlr + 0.85, zFlr + 1.55, false);

      // 6 Interior Doors (Ajar for Seamless Walkthrough & Sightlines)
      addLuxuryDoorAptA(layerKey, 8.36,  9.16,  3.03,  3.13,  zFlr, zCeil, "left",    1.05); // Master Bedroom
      addLuxuryDoorAptA(layerKey, 11.46, 11.56, 4.65,  5.38,  zFlr, zCeil, "bottom",  0.85); // Master En-Suite Bath
      addLuxuryDoorAptA(layerKey, 11.46, 11.66, 1.68,  2.42,  zFlr, zCeil, "top",    -0.95); // Mamad Bedroom
      addLuxuryDoorAptA(layerKey, 11.46, 11.66, 0.50,  1.32,  zFlr, zCeil, "bottom",  0.95); // East Bedroom
      addLuxuryDoorAptA(layerKey, 10.56, 11.36, 0.18,  0.28,  zFlr, zCeil, "right",  -0.85); // Main Family Bathroom
      addLuxuryDoorAptA(layerKey, 11.46, 11.56, -2.41, -1.62, zFlr, zCeil, "bottom",  0.80); // Service Laundry Room

      // -----------------------------------------------------------------------
      // 3. LIVING ROOM (סלון — Warm Contrast Rug, Sofa, Lounge Chairs & Proportional 55" TV)
      // -----------------------------------------------------------------------
      // Woven Greige-Taupe Area Rug with contrasting border
      addBoxAptA(layerKey, "mat_lux_rug_woven", 4.35, 7.18, 2.95, 5.45, zFlr + 0.020, zFlr + 0.032, false);

      // 3-Seater Bouclé & Sand-Linen Sofa along South of Living Room (u=4.88..6.94, v=2.75..3.52) facing North
      addBoxAptA(layerKey, "mat_lux_oak_smooth",   4.88, 6.94, 2.75, 3.52, zFlr + 0.04, zFlr + 0.16, false); // Warm Honey-Oak plinth
      addBoxAptA(layerKey, "mat_lux_boucle_cream", 4.88, 6.94, 2.75, 2.92, zFlr + 0.16, zFlr + 0.78, false); // Backrest
      addBoxAptA(layerKey, "mat_lux_boucle_cream", 4.88, 5.05, 2.75, 3.52, zFlr + 0.16, zFlr + 0.62, false); // Left arm
      addBoxAptA(layerKey, "mat_lux_boucle_cream", 6.77, 6.94, 2.75, 3.52, zFlr + 0.16, zFlr + 0.62, false); // Right arm
      // 3 Plush Sand-Linen Seat Cushions + 3 Back Cushions + 3 Contrasting Mocha-Taupe Throw Pillows
      [[5.07, 5.62], [5.64, 6.18], [6.20, 6.75]].forEach(([cu0, cu1], idx) => {
        addBoxAptA(layerKey, "mat_lux_linen_sand",   cu0, cu1, 2.90, 3.50, zFlr + 0.16, zFlr + 0.42, false);
        addBoxAptA(layerKey, "mat_lux_boucle_cream", cu0 + 0.03, cu1 - 0.03, 2.91, 3.07, zFlr + 0.42, zFlr + 0.75, false);
        if (idx !== 1) {
          addBoxAptA(layerKey, "mat_lux_pillow_taupe", cu0 + 0.08, cu1 - 0.10, 3.06, 3.20, zFlr + 0.42, zFlr + 0.66, false);
        }
      });

      // 2 Designer Lounge Armchairs on West side of Living Room (u=4.18..4.80, v=3.62..4.24 & v=4.48..5.10) facing East
      [[3.62, 4.24], [4.48, 5.10]].forEach(([av0, av1]) => {
        addBoxAptA(layerKey, "mat_lux_oak_smooth",   4.18, 4.80, av0, av1, zFlr + 0.04, zFlr + 0.16, false);
        addBoxAptA(layerKey, "mat_lux_linen_sand",   4.20, 4.78, av0 + 0.05, av1 - 0.05, zFlr + 0.16, zFlr + 0.40, false);
        addBoxAptA(layerKey, "mat_lux_boucle_cream", 4.18, 4.32, av0, av1, zFlr + 0.16, zFlr + 0.74, false); // Backrest
        addBoxAptA(layerKey, "mat_lux_boucle_cream", 4.18, 4.78, av0, av0 + 0.10, zFlr + 0.16, zFlr + 0.56, false);
        addBoxAptA(layerKey, "mat_lux_boucle_cream", 4.18, 4.78, av1 - 0.10, av1, zFlr + 0.16, zFlr + 0.56, false);
        addBoxAptA(layerKey, "mat_lux_pillow_taupe", 4.32, 4.46, av0 + 0.14, av1 - 0.14, zFlr + 0.40, zFlr + 0.62, false);
      });

      // Architectural Calacatta & Fluted-Oak Coffee Table (u=5.45..6.35, v=3.82..4.78)
      addCylAptA(layerKey, "mat_lux_fluted_oak", 5.90, 4.12, zFlr + 0.03, zFlr + 0.34, 0.18);
      addCylAptA(layerKey, "mat_lux_fluted_oak", 5.90, 4.48, zFlr + 0.03, zFlr + 0.34, 0.18);
      addBoxAptA(layerKey, "mat_lux_calacatta_marble", 5.45, 6.35, 3.82, 4.78, zFlr + 0.34, zFlr + 0.39, false);
      addCylAptA(layerKey, "mat_lux_champagne_brass", 5.90, 4.30, zFlr + 0.39, zFlr + 0.41, 0.14);
      addCylAptA(layerKey, "mat_lux_ceramic_white",   5.90, 4.30, zFlr + 0.41, zFlr + 0.56, 0.055, 0.075);
      addCylAptA(layerKey, "mat_lux_plant_olive",     5.90, 4.30, zFlr + 0.56, zFlr + 0.72, 0.12, 0.04);

      // Proportional Floating Media Console & Scaled-Down 55" OLED TV (105x58 cm) on East Wall W10 (u=7.51)
      addBoxAptA(layerKey, "mat_lux_oak_smooth",       7.18, 7.50, 3.75, 5.35, zFlr + 0.26, zFlr + 0.46, false);
      addBoxAptA(layerKey, "mat_lux_calacatta_marble", 7.17, 7.50, 3.74, 5.36, zFlr + 0.46, zFlr + 0.49, false);
      addBoxAptA(layerKey, "mat_lux_dark_glass",       7.45, 7.49, 4.02, 5.07, zFlr + 0.86, zFlr + 1.44, false); // 55" TV (105x58 cm)
      addBoxAptA(layerKey, "mat_lux_champagne_brass",  7.46, 7.50, 4.01, 5.08, zFlr + 0.85, zFlr + 0.86, false);

      // Sheer Pleated Linen Curtains flanking the North Balcony Vitrina
      addSheerCurtainAptA(layerKey, 3.48, 4.02, 5.62, 5.74, zFlr + 0.02, zCeil - 0.04);
      addSheerCurtainAptA(layerKey, 6.45, 7.05, 5.62, 5.74, zFlr + 0.02, zCeil - 0.04);

      // -----------------------------------------------------------------------
      // 4. LUXURY KITCHEN, SLIM WATERFALL ISLAND & PROPORTIONAL 4-CHAIR DINING AREA
      // -----------------------------------------------------------------------
      // A. Tall Fridge + Built-in Oven Tower along West Wall (u=0.82..1.46, v=2.40..3.95)
      addBoxAptA(layerKey, "mat_lux_cabinet_cream",   0.82, 1.46, 2.40, 3.95, zFlr + 0.02, zCeil - 0.28, false);
      addBoxAptA(layerKey, "mat_lux_champagne_brass", 1.46, 1.48, 3.12, 3.15, zFlr + 0.80, zFlr + 1.65, false);
      addBoxAptA(layerKey, "mat_lux_champagne_brass", 1.46, 1.48, 3.20, 3.23, zFlr + 0.80, zFlr + 1.65, false);
      addBoxAptA(layerKey, "mat_lux_dark_glass",      1.45, 1.48, 2.48, 3.04, zFlr + 0.85, zFlr + 1.42, false); // Oven
      addBoxAptA(layerKey, "mat_lux_dark_glass",      1.45, 1.48, 2.48, 3.04, zFlr + 1.48, zFlr + 1.86, false); // Microwave

      // B. Lower West & North Kitchen Cabinetry & Calacatta Marble Countertop
      addBoxAptA(layerKey, "mat_lux_cabinet_cream",    0.82, 1.44, 3.95, 5.58, zFlr + 0.02, zFlr + 0.87, false);
      addBoxAptA(layerKey, "mat_lux_calacatta_marble", 0.82, 1.46, 3.95, 5.58, zFlr + 0.87, zFlr + 0.91, false);
      addBoxAptA(layerKey, "mat_lux_cabinet_cream",    1.44, 2.75, 4.98, 5.58, zFlr + 0.02, zFlr + 0.87, false);
      addBoxAptA(layerKey, "mat_lux_calacatta_marble", 1.44, 2.75, 4.96, 5.58, zFlr + 0.87, zFlr + 0.91, false);
      // Calacatta Backsplash & Fluted Honey-Oak Upper Cabinets on West Wall
      addBoxAptA(layerKey, "mat_lux_calacatta_marble", 0.82, 0.86, 3.95, 5.58, zFlr + 0.91, zFlr + 1.55, false);
      addBoxAptA(layerKey, "mat_lux_fluted_oak",       0.82, 1.20, 3.95, 5.58, zFlr + 1.55, zCeil - 0.28, false);
      addBoxAptA(layerKey, "mat_lux_glow_warm",        1.14, 1.18, 4.00, 5.52, zFlr + 1.53, zFlr + 1.55, false);
      // 4-Zone Induction Cooktop on West Counter (u=0.92..1.36, v=4.35..4.95)
      addBoxAptA(layerKey, "mat_lux_dark_glass",       0.92, 1.36, 4.35, 4.95, zFlr + 0.91, zFlr + 0.92, false);
      // Undermount Sink & Champagne-Brass Faucet under North Kitchen Window (u=1.68..2.28, v=5.08..5.48)
      addBoxAptA(layerKey, "mat_lux_ceramic_white",    1.68, 2.28, 5.08, 5.48, zFlr + 0.86, zFlr + 0.915, false);
      addCylAptA(layerKey, "mat_lux_champagne_brass",  1.98, 5.50, zFlr + 0.91, zFlr + 1.22, 0.016);
      addBoxAptA(layerKey, "mat_lux_champagne_brass",  1.96, 2.00, 5.30, 5.50, zFlr + 1.20, zFlr + 1.23, false);

      // C. Proportional Waterfall Kitchen Island (56x112 cm: u=2.66..3.22, v=3.55..4.67) + 2 Compact Bar Stools
      addBoxAptA(layerKey, "mat_lux_fluted_oak",       2.70, 3.18, 3.59, 4.63, zFlr + 0.02, zFlr + 0.88, false);
      addBoxAptA(layerKey, "mat_lux_calacatta_marble", 2.66, 3.22, 3.55, 4.67, zFlr + 0.88, zFlr + 0.92, false);
      addBoxAptA(layerKey, "mat_lux_calacatta_marble", 2.66, 3.22, 3.55, 3.60, zFlr + 0.02, zFlr + 0.88, false);
      addBoxAptA(layerKey, "mat_lux_calacatta_marble", 2.66, 3.22, 4.62, 4.67, zFlr + 0.02, zFlr + 0.88, false);
      // 2 Compact Low-Profile Bar Stools on East side of Island (u=3.32)
      [3.82, 4.40].forEach(sv => {
        addCylAptA(layerKey, "mat_lux_oak_smooth", 3.32, sv, zFlr + 0.02, zFlr + 0.62, 0.025, 0.13);
        addCylAptA(layerKey, "mat_lux_linen_sand", 3.32, sv, zFlr + 0.62, zFlr + 0.68, 0.15);
      });
      // 2 Slim Champagne-Brass Pendant Lamps over Island
      [3.82, 4.40].forEach(pv => {
        addCylAptA(layerKey, "mat_lux_champagne_brass", 2.94, pv, zFlr + 1.84, zCeil, 0.006);
        addCylAptA(layerKey, "mat_lux_champagne_brass", 2.94, pv, zFlr + 1.66, zFlr + 1.84, 0.032);
        addCylAptA(layerKey, "mat_lux_glow_warm",       2.94, pv, zFlr + 1.60, zFlr + 1.66, 0.030);
      });

      // D. Proportional Scaled-Down 4-Person Dining Table (118x72 cm: u=5.82..7.00, v=0.34..1.06) + 4 Chairs
      addCylAptA(layerKey, "mat_lux_fluted_oak", 6.18, 0.70, zFlr + 0.02, zFlr + 0.72, 0.13, 0.16);
      addCylAptA(layerKey, "mat_lux_fluted_oak", 6.64, 0.70, zFlr + 0.02, zFlr + 0.72, 0.13, 0.16);
      addBoxAptA(layerKey, "mat_lux_oak_smooth",       5.82, 7.00, 0.34, 1.06, zFlr + 0.71, zFlr + 0.74, false);
      addBoxAptA(layerKey, "mat_lux_calacatta_marble", 5.84, 6.98, 0.36, 1.04, zFlr + 0.74, zFlr + 0.76, false);
      // 4 Proportional Dining Chairs (2 North, 2 South)
      [6.12, 6.70].forEach(cu => {
        // South chairs facing North (+v)
        addBoxAptA(layerKey, "mat_lux_oak_smooth",   cu - 0.17, cu + 0.17, 0.02, 0.32, zFlr + 0.02, zFlr + 0.43, false);
        addBoxAptA(layerKey, "mat_lux_linen_sand",   cu - 0.18, cu + 0.18, 0.01, 0.33, zFlr + 0.43, zFlr + 0.48, false);
        addBoxAptA(layerKey, "mat_lux_boucle_cream", cu - 0.18, cu + 0.18, 0.00, 0.07, zFlr + 0.48, zFlr + 0.78, false);
        // North chairs facing South (-v)
        addBoxAptA(layerKey, "mat_lux_oak_smooth",   cu - 0.17, cu + 0.17, 1.08, 1.38, zFlr + 0.02, zFlr + 0.43, false);
        addBoxAptA(layerKey, "mat_lux_linen_sand",   cu - 0.18, cu + 0.18, 1.07, 1.39, zFlr + 0.43, zFlr + 0.48, false);
        addBoxAptA(layerKey, "mat_lux_boucle_cream", cu - 0.18, cu + 0.18, 1.33, 1.40, zFlr + 0.48, zFlr + 0.78, false);
      });
      // Proportional Sculptural Brass Ring Pendant over Dining Table
      addCylAptA(layerKey, "mat_lux_champagne_brass", 6.41, 0.70, zFlr + 1.82, zCeil, 0.008);
      addCylAptA(layerKey, "mat_lux_champagne_brass", 6.41, 0.70, zFlr + 1.74, zFlr + 1.82, 0.24, 0.24);
      addCylAptA(layerKey, "mat_lux_glow_warm",       6.41, 0.70, zFlr + 1.71, zFlr + 1.74, 0.22, 0.22);

      // -----------------------------------------------------------------------
      // 5. NORTH-CENTRAL SUN BALCONY (מרפסת שמש צפונית — Outdoor Lounge & Olive Planters)
      // -----------------------------------------------------------------------
      addBoxAptA(layerKey, "mat_lux_oak_smooth",   3.75, 5.75, 7.35, 8.05, zFlr + 0.04, zFlr + 0.26, false);
      addBoxAptA(layerKey, "mat_lux_boucle_cream", 3.80, 5.70, 7.38, 7.98, zFlr + 0.26, zFlr + 0.42, false);
      addBoxAptA(layerKey, "mat_lux_boucle_cream", 3.75, 5.75, 7.92, 8.05, zFlr + 0.42, zFlr + 0.74, false);
      addCylAptA(layerKey, "mat_lux_calacatta_marble", 4.85, 6.72, zFlr + 0.03, zFlr + 0.40, 0.34, 0.24);
      [[3.62, 6.35], [7.25, 7.75]].forEach(([pu, pv]) => {
        addCylAptA(layerKey, "mat_lux_ceramic_white", pu, pv, zFlr + 0.03, zFlr + 0.56, 0.25, 0.19);
        addCylAptA(layerKey, "mat_lux_oak_smooth",    pu, pv, zFlr + 0.56, zFlr + 1.20, 0.035, 0.045);
        addCylAptA(layerKey, "mat_lux_plant_olive",   pu, pv, zFlr + 1.15, zFlr + 1.85, 0.42, 0.26);
      });

      // -----------------------------------------------------------------------
      // 6. MASTER SUITE (יחידת הורים 385×290 — North Window 100% Visible & Unobstructed!)
      // -----------------------------------------------------------------------
      // Warm Woven Greige-Taupe Area Rug under Bed
      addBoxAptA(layerKey, "mat_lux_rug_woven", 8.65, 10.85, 4.05, 6.05, zFlr + 0.020, zFlr + 0.032, false);
      // Low Designer Headboard in Warm Oak & Sand Linen (zFlr + 0.02 .. zFlr + 0.74 — strictly 11cm BELOW the North window sill at zFlr + 0.85 so 100% of the window is exposed!)
      addBoxAptA(layerKey, "mat_lux_fluted_oak", 8.45, 11.00, 6.08, 6.16, zFlr + 0.02, zFlr + 0.72, false);
      addBoxAptA(layerKey, "mat_lux_linen_sand", 8.92, 10.58, 5.98, 6.08, zFlr + 0.30, zFlr + 0.74, false);
      // King-Size Bed Frame, Crisp White Mattress & Contrasting Mocha-Taupe Duvet Runner
      addBoxAptA(layerKey, "mat_lux_oak_smooth",    8.90, 10.60, 4.22, 6.00, zFlr + 0.03, zFlr + 0.30, false);
      addBoxAptA(layerKey, "mat_lux_ceramic_white", 8.96, 10.54, 4.28, 5.98, zFlr + 0.30, zFlr + 0.50, false);
      addBoxAptA(layerKey, "mat_lux_pillow_taupe",  8.94, 10.56, 4.26, 5.20, zFlr + 0.32, zFlr + 0.52, false);
      // 4 Pillows (sitting at zFlr + 0.50..0.64, well below the zFlr + 0.85 window sill)
      addBoxAptA(layerKey, "mat_lux_boucle_cream", 9.02, 9.70,  5.62, 5.95, zFlr + 0.50, zFlr + 0.64, false);
      addBoxAptA(layerKey, "mat_lux_boucle_cream", 9.80, 10.48, 5.62, 5.95, zFlr + 0.50, zFlr + 0.64, false);
      addBoxAptA(layerKey, "mat_lux_pillow_taupe", 9.10, 9.65,  5.40, 5.66, zFlr + 0.50, zFlr + 0.62, false);
      addBoxAptA(layerKey, "mat_lux_pillow_taupe", 9.85, 10.40, 5.40, 5.66, zFlr + 0.50, zFlr + 0.62, false);
      // 2 Floating Oak Nightstands + Warm Table Lamps flanking the Master Bed
      [[8.35, 8.84], [10.66, 11.15]].forEach(([nu0, nu1]) => {
        const cu = 0.5 * (nu0 + nu1);
        addBoxAptA(layerKey, "mat_lux_oak_smooth",       nu0, nu1, 5.68, 6.08, zFlr + 0.28, zFlr + 0.48, false);
        addBoxAptA(layerKey, "mat_lux_calacatta_marble", nu0, nu1, 5.67, 6.08, zFlr + 0.48, zFlr + 0.51, false);
        addCylAptA(layerKey, "mat_lux_champagne_brass", cu, 5.88, zFlr + 0.51, zFlr + 0.62, 0.015);
        addCylAptA(layerKey, "mat_lux_glow_warm",       cu, 5.88, zFlr + 0.62, zFlr + 0.74, 0.075);
      });
      // Custom Floor-to-Ceiling Wardrobe along West Wall W10 (u=7.68..8.28, v=3.20..6.05)
      addBoxAptA(layerKey, "mat_lux_cabinet_cream", 7.68, 8.28, 3.20, 5.40, zFlr + 0.02, zCeil - 0.08, false);
      addBoxAptA(layerKey, "mat_lux_fluted_oak",    7.68, 8.28, 5.40, 6.05, zFlr + 0.02, zCeil - 0.08, false);
      [3.75, 4.30, 4.85].forEach(wv => {
        addBoxAptA(layerKey, "mat_lux_champagne_brass", 8.28, 8.30, wv - 0.01, wv + 0.01, zFlr + 0.85, zFlr + 1.65, false);
      });

      // Master En-Suite Bathroom (u=11.56..13.46, v=4.60..6.20)
      addBoxAptA(layerKey, "mat_lux_clear_glass",      12.68, 12.72, 5.35, 6.18, zFlr + 0.02, zFlr + 2.10, false);
      addBoxAptA(layerKey, "mat_lux_fluted_oak",       11.78, 12.42, 5.72, 6.18, zFlr + 0.42, zFlr + 0.82, false);
      addBoxAptA(layerKey, "mat_lux_calacatta_marble", 11.78, 12.42, 5.70, 6.18, zFlr + 0.82, zFlr + 0.86, false);
      addCylAptA(layerKey, "mat_lux_ceramic_white",    12.10, 5.94, zFlr + 0.86, zFlr + 0.96, 0.15);
      addBoxAptA(layerKey, "mat_lux_mirror",           11.80, 12.40, 6.15, 6.19, zFlr + 1.05, zFlr + 1.95, false);
      addBoxAptA(layerKey, "mat_lux_ceramic_white",    12.85, 13.42, 4.82, 5.22, zFlr + 0.18, zFlr + 0.43, false);

      // -----------------------------------------------------------------------
      // 7. BEDROOM 2 (MAMAD — 337×280 cm) & BEDROOM 3 (EAST BEDROOM — 340×280 cm)
      // -----------------------------------------------------------------------
      // Bedroom 2 — Mamad (u=11.66..15.18, v=1.68..4.58)
      addBoxAptA(layerKey, "mat_lux_cabinet_cream", 11.68, 12.28, 2.75, 4.52, zFlr + 0.02, zCeil - 0.10, false); // Wardrobe
      addBoxAptA(layerKey, "mat_lux_rug_woven",     12.55, 14.85, 2.45, 4.30, zFlr + 0.020, zFlr + 0.030, false);
      addBoxAptA(layerKey, "mat_lux_oak_smooth",    13.15, 15.05, 3.55, 4.46, zFlr + 0.03, zFlr + 0.30, false); // Bed base
      addBoxAptA(layerKey, "mat_lux_ceramic_white", 13.20, 14.98, 3.60, 4.42, zFlr + 0.30, zFlr + 0.50, false); // Mattress
      addBoxAptA(layerKey, "mat_lux_pillow_taupe",  13.18, 13.95, 3.58, 4.44, zFlr + 0.32, zFlr + 0.52, false); // Mocha throw
      addBoxAptA(layerKey, "mat_lux_linen_sand",    14.96, 15.06, 3.55, 4.46, zFlr + 0.30, zFlr + 0.74, false); // Low headboard
      addBoxAptA(layerKey, "mat_lux_pillow_taupe",  14.62, 14.92, 3.72, 4.28, zFlr + 0.50, zFlr + 0.63, false); // Pillow
      addBoxAptA(layerKey, "mat_lux_oak_smooth",    13.85, 14.95, 1.72, 2.30, zFlr + 0.70, zFlr + 0.75, false); // Study Desk
      addBoxAptA(layerKey, "mat_lux_oak_smooth",    14.88, 14.95, 1.72, 2.30, zFlr + 0.02, zFlr + 0.70, false);
      addCylAptA(layerKey, "mat_lux_linen_sand",    14.40, 2.52, zFlr + 0.42, zFlr + 0.48, 0.19); // Desk Chair

      // Bedroom 3 — East Bedroom (u=11.66..15.18, v=-1.41..1.38)
      addBoxAptA(layerKey, "mat_lux_cabinet_cream", 11.68, 12.28, -1.38, 0.18, zFlr + 0.02, zCeil - 0.10, false); // Wardrobe
      addBoxAptA(layerKey, "mat_lux_rug_woven",     12.55, 14.85, -1.25, 0.55, zFlr + 0.020, zFlr + 0.030, false);
      addBoxAptA(layerKey, "mat_lux_oak_smooth",    13.20, 15.05, -1.36, -0.48, zFlr + 0.03, zFlr + 0.30, false); // Bed base
      addBoxAptA(layerKey, "mat_lux_ceramic_white", 13.25, 14.98, -1.32, -0.52, zFlr + 0.30, zFlr + 0.50, false); // Mattress
      addBoxAptA(layerKey, "mat_lux_pillow_taupe",  13.22, 13.98, -1.34, -0.50, zFlr + 0.32, zFlr + 0.52, false); // Mocha throw
      addBoxAptA(layerKey, "mat_lux_linen_sand",    14.96, 15.06, -1.36, -0.48, zFlr + 0.30, zFlr + 0.74, false); // Low headboard (below sill!)
      addBoxAptA(layerKey, "mat_lux_pillow_taupe",  14.62, 14.92, -1.20, -0.64, zFlr + 0.50, zFlr + 0.63, false); // Pillow
      addBoxAptA(layerKey, "mat_lux_oak_smooth",    13.90, 14.98, 0.75, 1.34, zFlr + 0.70, zFlr + 0.75, false); // Study Desk
      addBoxAptA(layerKey, "mat_lux_oak_smooth",    14.90, 14.98, 0.75, 1.34, zFlr + 0.02, zFlr + 0.70, false);
      addCylAptA(layerKey, "mat_lux_linen_sand",    14.44, 0.52, zFlr + 0.42, zFlr + 0.48, 0.19); // Desk Chair

      // -----------------------------------------------------------------------
      // 8. MAIN FAMILY BATHROOM & SERVICE LAUNDRY ROOM (ח. רחצה כללי וח. שירות)
      // -----------------------------------------------------------------------
      addBoxAptA(layerKey, "mat_lux_calacatta_marble", 9.88, 11.44, -3.08, -2.35, zFlr + 0.02, zFlr + 0.54, false); // Bathtub surround
      addBoxAptA(layerKey, "mat_lux_ceramic_white",    9.96, 11.36, -3.00, -2.42, zFlr + 0.54, zFlr + 0.57, false); // Bathtub basin
      addBoxAptA(layerKey, "mat_lux_clear_glass",      9.90, 10.65, -2.38, -2.34, zFlr + 0.55, zFlr + 2.05, false); // Glass screen
      addBoxAptA(layerKey, "mat_lux_fluted_oak",       9.88, 10.40, -0.68, 0.04,  zFlr + 0.42, zFlr + 0.82, false); // Vanity
      addBoxAptA(layerKey, "mat_lux_calacatta_marble", 9.88, 10.42, -0.68, 0.04,  zFlr + 0.82, zFlr + 0.86, false);
      addCylAptA(layerKey, "mat_lux_ceramic_white",    10.15, -0.32, zFlr + 0.86, zFlr + 0.96, 0.15);
      addBoxAptA(layerKey, "mat_lux_mirror",           9.88, 9.92,  -0.65, 0.02,  zFlr + 1.05, zFlr + 1.95, false);
      addBoxAptA(layerKey, "mat_lux_ceramic_white",    9.88, 10.48, -1.38, -0.98, zFlr + 0.18, zFlr + 0.43, false); // Toilet
      addBoxAptA(layerKey, "mat_lux_cabinet_cream",    12.70, 14.10, -3.06, -2.45, zFlr + 0.02, zFlr + 1.85, false); // Laundry cabinet

      // -----------------------------------------------------------------------
      // 9. WARM INTERIOR POINT LIGHTS FOR APARTMENT A
      // -----------------------------------------------------------------------
      const aptALightsUV = [
        [5.65, 4.20, zCeil - 0.25, 0.68, 9.5], // Living Room
        [2.35, 4.10, zCeil - 0.35, 0.55, 7.5], // Kitchen & Island
        [6.30, 0.80, zCeil - 0.40, 0.55, 7.5], // Dining Area
        [9.70, 4.80, zCeil - 0.25, 0.62, 7.5], // Master Bedroom
        [13.50, 3.10, zCeil - 0.25, 0.48, 6.5], // Mamad Bedroom
        [13.50, 0.00, zCeil - 0.25, 0.48, 6.5]  // East Bedroom
      ];
      aptALightsUV.forEach(([lu, lv, lz, intensity, dist]) => {
        const [lx, ly] = aptA_XY(lu, lv);
        const ptLight = new THREE.PointLight(0xfff5e4, intensity, dist, 1.6);
        ptLight.position.copy(cadTo3D(lx, ly, lz));
        ptLight.userData = { baseIntensity: intensity };
        layerGroups[layerKey].add(ptLight);
        interiorPointLights.push(ptLight);
      });
      isBuildingInteriorFurniture = false;
    }

    // =========================================================================
    // LUXURY ARCHITECTURAL SALES MODEL OF APARTMENT B (3 ROOMS, 80+12 SQM, NW)
    // =========================================================================
    function addBoxAptB(layerKey, matKey, u0, u1, s0, s1, z0, z1, withEdges = false) {
      return addBoxAligned(layerKey, matKey, NW_CORNER, EU, ES, u0, u1, s0, s1, z0, z1, withEdges);
    }

    function addCylAptB(layerKey, matKey, cu, cs, z0, z1, rTop, rBot = rTop, segs = 24) {
      const [cx, cy] = ptUV(cu, cs);
      return addCylinder3D(layerKey, matKey, cx, cy, z0, z1, rTop, rBot, segs);
    }

    function buildLuxuryApartmentB(layerKey, zFlr, zCeil) {
      isBuildingInteriorFurniture = true;
      // 1. Custom Flooring by Zone (Public, Master & Mamad Bedrooms, Baths, NW Balcony)
      const fPub1 = addBoxAptB(layerKey, "mat_lux_travertine_floor", 3.95, 10.42, 0.85, 4.02, zFlr + 0.004, zFlr + 0.018, false);
      const fPub2 = addBoxAptB(layerKey, "mat_lux_travertine_floor", 4.25, 7.85,  4.02, 6.92, zFlr + 0.004, zFlr + 0.018, false);
      const fHall = addBoxAptB(layerKey, "mat_lux_travertine_floor", 3.10, 4.10,  3.80, 9.12, zFlr + 0.004, zFlr + 0.018, false);
      const fMast = addBoxAptB(layerKey, "mat_lux_travertine_floor", 0.25, 3.85,  0.85, 3.68, zFlr + 0.005, zFlr + 0.019, false);
      const fMamd = addBoxAptB(layerKey, "mat_lux_travertine_floor", 0.25, 4.08,  9.15, 11.98, zFlr + 0.005, zFlr + 0.019, false);
      const fBth1 = addBoxAptB(layerKey, "mat_lux_calacatta_marble", 0.25, 2.15,  3.80, 5.45, zFlr + 0.005, zFlr + 0.019, false);
      const fBth2 = addBoxAptB(layerKey, "mat_lux_calacatta_marble", 0.25, 3.00,  5.55, 8.90, zFlr + 0.005, zFlr + 0.019, false);
      const balBFloor = addExtrudedPolygon(layerKey, "mat_terrace_tile", BALCONY_NW, zFlr + 0.005, zFlr + 0.020, false);
      [fPub1, fPub2, fHall, fMast, fMamd, fBth1, fBth2, balBFloor].forEach(m => { if (m) aptCFloorMeshes.push(m); });
      if (balBFloor) balconyFloorMeshes.push(balBFloor);

      // 2. Living Room (u=4.20..7.55, s=1.05..3.85) — Woven Rug, Bouclé Sofa, Lounge Chair, Coffee Table & 55" TV
      addBoxAptB(layerKey, "mat_lux_rug_woven", 4.45, 7.25, 1.15, 3.65, zFlr + 0.020, zFlr + 0.032, false);
      // 3-Seater Sofa along South/West of Living Zone (u=4.85..7.05, s=3.05..3.80) facing North Balcony
      addBoxAptB(layerKey, "mat_lux_oak_smooth",   4.85, 7.05, 3.05, 3.80, zFlr + 0.04, zFlr + 0.15, false);
      addBoxAptB(layerKey, "mat_lux_boucle_cream", 4.85, 7.05, 3.62, 3.80, zFlr + 0.15, zFlr + 0.78, false);
      addBoxAptB(layerKey, "mat_lux_boucle_cream", 4.85, 5.04, 3.05, 3.80, zFlr + 0.15, zFlr + 0.60, false);
      addBoxAptB(layerKey, "mat_lux_boucle_cream", 6.86, 7.05, 3.05, 3.80, zFlr + 0.15, zFlr + 0.60, false);
      addBoxAptB(layerKey, "mat_lux_linen_sand",   5.04, 6.86, 3.08, 3.62, zFlr + 0.15, zFlr + 0.42, false);
      addBoxAptB(layerKey, "mat_lux_pillow_taupe", 5.15, 5.55, 3.42, 3.60, zFlr + 0.42, zFlr + 0.68, false);
      addBoxAptB(layerKey, "mat_lux_pillow_taupe", 6.35, 6.75, 3.42, 3.60, zFlr + 0.42, zFlr + 0.68, false);
      // Coffee Table & Vase
      addCylAptB(layerKey, "mat_lux_fluted_oak", 5.95, 2.25, zFlr + 0.03, zFlr + 0.35, 0.22);
      addBoxAptB(layerKey, "mat_lux_calacatta_marble", 5.45, 6.45, 1.85, 2.65, zFlr + 0.35, zFlr + 0.40, false);
      addCylAptB(layerKey, "mat_lux_plant_olive", 5.95, 2.25, zFlr + 0.40, zFlr + 0.68, 0.12, 0.05);
      // West Media Wall Console & 55" TV (on u=3.95..4.30 wall)
      addBoxAptB(layerKey, "mat_lux_oak_smooth",       4.00, 4.32, 1.45, 2.95, zFlr + 0.26, zFlr + 0.46, false);
      addBoxAptB(layerKey, "mat_lux_calacatta_marble", 4.00, 4.33, 1.44, 2.96, zFlr + 0.46, zFlr + 0.49, false);
      addBoxAptB(layerKey, "mat_lux_dark_glass",       4.02, 4.06, 1.68, 2.72, zFlr + 0.86, zFlr + 1.44, false);

      // 3. Kitchen, Waterfall Island & 4-Person Dining Table (u=7.65..10.35, s=0.90..3.95 & u=5.10..7.20, s=4.35..5.65)
      addBoxAptB(layerKey, "mat_lux_cabinet_cream",    9.75, 10.38, 0.90, 3.92, zFlr + 0.02, zFlr + 0.88, false);
      addBoxAptB(layerKey, "mat_lux_calacatta_marble", 9.73, 10.38, 0.90, 3.92, zFlr + 0.88, zFlr + 0.92, false);
      addBoxAptB(layerKey, "mat_lux_fluted_oak",       9.98, 10.38, 0.90, 3.92, zFlr + 1.52, zCeil - 0.25, false);
      addBoxAptB(layerKey, "mat_lux_dark_glass",       9.82, 10.26, 2.10, 2.70, zFlr + 0.92, zFlr + 0.93, false); // Cooktop
      // Kitchen Island (u=8.15..8.75, s=1.65..2.85) + 2 Bar Stools
      addBoxAptB(layerKey, "mat_lux_fluted_oak",       8.18, 8.72, 1.68, 2.82, zFlr + 0.02, zFlr + 0.88, false);
      addBoxAptB(layerKey, "mat_lux_calacatta_marble", 8.15, 8.75, 1.65, 2.85, zFlr + 0.88, zFlr + 0.92, false);
      [1.95, 2.55].forEach(bs => {
        addCylAptB(layerKey, "mat_lux_oak_smooth", 7.92, bs, zFlr + 0.02, zFlr + 0.62, 0.03, 0.13);
        addCylAptB(layerKey, "mat_lux_linen_sand", 7.92, bs, zFlr + 0.62, zFlr + 0.68, 0.15);
      });
      // Dining Table (u=5.35..6.55, s=4.55..5.35) + 4 Chairs
      addCylAptB(layerKey, "mat_lux_fluted_oak", 5.95, 4.95, zFlr + 0.02, zFlr + 0.72, 0.18, 0.22);
      addBoxAptB(layerKey, "mat_lux_calacatta_marble", 5.35, 6.55, 4.55, 5.35, zFlr + 0.72, zFlr + 0.76, false);
      [5.65, 6.25].forEach(cu => {
        addBoxAptB(layerKey, "mat_lux_linen_sand", cu - 0.16, cu + 0.16, 4.22, 4.52, zFlr + 0.02, zFlr + 0.46, false);
        addBoxAptB(layerKey, "mat_lux_linen_sand", cu - 0.16, cu + 0.16, 5.38, 5.68, zFlr + 0.02, zFlr + 0.46, false);
      });

      // 4. NW Sun Balcony (BALCONY_NW: u=4.10..8.55, s=-1.90..0.60)
      addBoxAptB(layerKey, "mat_lux_oak_smooth",   5.10, 7.20, -1.55, -0.80, zFlr + 0.03, zFlr + 0.28, false);
      addBoxAptB(layerKey, "mat_lux_boucle_cream", 5.15, 7.15, -1.50, -0.85, zFlr + 0.28, zFlr + 0.44, false);
      addCylAptB(layerKey, "mat_lux_calacatta_marble", 6.15, -0.35, zFlr + 0.03, zFlr + 0.38, 0.30);
      [[4.45, -1.35], [8.10, -1.35]].forEach(([pu, ps]) => {
        addCylAptB(layerKey, "mat_lux_ceramic_white", pu, ps, zFlr + 0.02, zFlr + 0.55, 0.24, 0.18);
        addCylAptB(layerKey, "mat_lux_plant_olive",   pu, ps, zFlr + 0.55, zFlr + 1.75, 0.38, 0.22);
      });

      // 5. Master Bedroom (u=0.35..3.75, s=0.95..3.60) & Mamad Bedroom (u=0.35..3.95, s=9.25..11.85)
      addBoxAptB(layerKey, "mat_lux_rug_woven",     0.85, 3.15, 1.15, 3.15, zFlr + 0.020, zFlr + 0.030, false);
      addBoxAptB(layerKey, "mat_lux_oak_smooth",    1.10, 2.80, 0.95, 2.85, zFlr + 0.03, zFlr + 0.30, false);
      addBoxAptB(layerKey, "mat_lux_ceramic_white", 1.16, 2.74, 1.00, 2.80, zFlr + 0.30, zFlr + 0.50, false);
      addBoxAptB(layerKey, "mat_lux_pillow_taupe",  1.14, 2.76, 1.95, 2.82, zFlr + 0.32, zFlr + 0.52, false);
      addBoxAptB(layerKey, "mat_lux_linen_sand",    1.10, 2.80, 0.90, 1.00, zFlr + 0.30, zFlr + 0.72, false);
      addBoxAptB(layerKey, "mat_lux_cabinet_cream", 3.20, 3.78, 1.10, 3.10, zFlr + 0.02, zCeil - 0.10, false);
      // Mamad Bed, Desk & Wardrobe
      addBoxAptB(layerKey, "mat_lux_rug_woven",     0.85, 3.35, 9.45, 11.45, zFlr + 0.020, zFlr + 0.030, false);
      addBoxAptB(layerKey, "mat_lux_oak_smooth",    0.35, 2.20, 10.65, 11.80, zFlr + 0.03, zFlr + 0.30, false);
      addBoxAptB(layerKey, "mat_lux_ceramic_white", 0.40, 2.15, 10.70, 11.75, zFlr + 0.30, zFlr + 0.50, false);
      addBoxAptB(layerKey, "mat_lux_pillow_taupe",  1.35, 2.16, 10.68, 11.76, zFlr + 0.32, zFlr + 0.52, false);
      addBoxAptB(layerKey, "mat_lux_cabinet_cream", 2.35, 3.95, 11.25, 11.85, zFlr + 0.02, zCeil - 0.10, false);

      // 6. Warm Interior Lights for Apartment B
      [[6.0, 2.4, 0.65, 9.0], [8.8, 2.2, 0.55, 7.5], [2.0, 2.2, 0.55, 7.0], [2.0, 10.5, 0.48, 6.5]].forEach(([lu, ls, inten, dist]) => {
        const [lx, ly] = ptUV(lu, ls);
        const ptLight = new THREE.PointLight(0xfff5e4, inten, dist, 1.6);
        ptLight.position.copy(cadTo3D(lx, ly, zCeil - 0.25));
        ptLight.userData = { baseIntensity: inten };
        layerGroups[layerKey].add(ptLight);
        interiorPointLights.push(ptLight);
      });
      isBuildingInteriorFurniture = false;
    }

    // =========================================================================
    // GROUND FLOOR LUXURY MAIN LOBBY & UNDERGROUND BASEMENT PARKING (-3.50m)
    // =========================================================================
    function buildLuxuryGroundLobby(layerKey) {
      isBuildingInteriorFurniture = true;
      const zFlr = 0.06, zCeil = 3.81;
      // Calacatta Marble Lobby Carpet Inlay
      addBoxXY(layerKey, "mat_lux_calacatta_marble", 17.50, 26.80, 13.50, 19.60, zFlr + 0.005, zFlr + 0.020, false);
      // Reception Concierge Desk in Calacatta Marble & Fluted Honey-Oak
      addBoxXY(layerKey, "mat_lux_fluted_oak",       19.40, 21.80, 16.20, 17.05, zFlr + 0.02, zFlr + 1.05, false);
      addBoxXY(layerKey, "mat_lux_calacatta_marble", 19.35, 21.85, 16.15, 17.10, zFlr + 1.05, zFlr + 1.12, false);
      addBoxXY(layerKey, "mat_lux_champagne_brass",  19.38, 21.82, 17.05, 17.09, zFlr + 0.02, zFlr + 0.12, false);
      // Lobby Lounge Seating Area (Sofa, 2 Armchairs, Marble Coffee Table & Olive Planters)
      addBoxXY(layerKey, "mat_lux_rug_woven",        22.50, 25.80, 14.80, 18.20, zFlr + 0.022, zFlr + 0.035, false);
      addBoxXY(layerKey, "mat_lux_oak_smooth",       22.80, 25.40, 17.20, 18.00, zFlr + 0.04, zFlr + 0.16, false);
      addBoxXY(layerKey, "mat_lux_boucle_cream",     22.85, 25.35, 17.22, 17.85, zFlr + 0.16, zFlr + 0.44, false);
      addBoxXY(layerKey, "mat_lux_linen_sand",       22.80, 25.40, 17.82, 18.00, zFlr + 0.16, zFlr + 0.82, false);
      addCylinder3D(layerKey, "mat_lux_calacatta_marble", 24.10, 16.20, zFlr + 0.04, zFlr + 0.40, 0.48);
      addCylinder3D(layerKey, "mat_lux_ceramic_white", 26.10, 18.60, zFlr + 0.03, zFlr + 0.65, 0.28, 0.20);
      addCylinder3D(layerKey, "mat_lux_plant_olive",   26.10, 18.60, zFlr + 0.65, zFlr + 2.10, 0.48, 0.28);
      // Sculptural Chandelier Ring in Double-Height Lobby
      addCylinder3D(layerKey, "mat_lux_champagne_brass", 22.80, 16.50, 2.75, 2.88, 0.65, 0.65);
      addCylinder3D(layerKey, "mat_lux_glow_warm",       22.80, 16.50, 2.68, 2.75, 0.62, 0.62);
      const lobbyLight = new THREE.PointLight(0xfff3d6, 0.85, 14.0, 1.5);
      lobbyLight.position.copy(cadTo3D(22.80, 16.50, 3.10));
      lobbyLight.userData = { baseIntensity: 0.85 };
      layerGroups[layerKey].add(lobbyLight);
      interiorPointLights.push(lobbyLight);
      isBuildingInteriorFurniture = false;
    }

    // Underground Basement Parking (-3.50m, Sheet A-1000: 18 Numbered Stalls #1..#18)
    const PARKING_STALL_COORDS = {};
    let parkingHighlightMesh = null;

    function buildUndergroundParkingBasement() {
      const layerKey = "-1_basement_parking";
      const zBot = -3.50, zTop = -0.08;
      // Main Basement Concrete Floor & Perimeter Retaining Walls
      addExtrudedPolygon(layerKey, "mat_parking_asphalt", POLY_SETBACK, zBot - 0.25, zBot, true);
      addWallStrip(layerKey, "mat_concrete_curb", POLY_SETBACK, 0.30, zBot, zTop, true, true);
      // Underground Elevator & Stairwell Core Lobby
      addBoxXY(layerKey, "mat_interior_wall", 12.60, 18.80, 11.20, 15.80, zBot, zTop, true);
      addBoxXY(layerKey, "mat_lux_calacatta_marble", 13.00, 18.40, 9.40, 11.20, zBot + 0.01, zBot + 0.03, false);

      // Define 18 Parking Stalls around the perimeter (North row: #1..#9, South/West rows: #10..#18)
      const stalls = [
        { num: 1,  x: 6.2,  y: 16.2 }, { num: 2,  x: 8.8,  y: 16.7 }, { num: 3,  x: 11.4, y: 17.2 },
        { num: 4,  x: 14.0, y: 17.8 }, { num: 5,  x: 16.6, y: 18.3 }, { num: 6,  x: 19.2, y: 18.8 },
        { num: 7,  x: 21.8, y: 19.4 }, { num: 8,  x: 24.4, y: 19.9 }, { num: 9,  x: 27.0, y: 19.5 },
        { num: 10, x: 6.2,  y: 6.4  }, { num: 11, x: 8.8,  y: 6.4  }, { num: 12, x: 11.4, y: 6.4  },
        { num: 13, x: 14.0, y: 6.4  }, { num: 14, x: 16.6, y: 6.4  }, { num: 15, x: 19.2, y: 6.4  },
        { num: 16, x: 21.8, y: 6.4  }, { num: 17, x: 24.4, y: 6.4  }, { num: 18, x: 27.0, y: 6.4  }
      ];
      stalls.forEach(st => {
        PARKING_STALL_COORDS[st.num] = st;
        // White painted parking bay lines (2.40m x 4.60m)
        addBoxXY(layerKey, "mat_parking_line", st.x - 1.15, st.x - 1.07, st.y - 2.20, st.y + 2.20, zBot + 0.01, zBot + 0.03, false);
        addBoxXY(layerKey, "mat_parking_line", st.x + 1.07, st.x + 1.15, st.y - 2.20, st.y + 2.20, zBot + 0.01, zBot + 0.03, false);
        // Yellow/ brass wheel stop bumper
        addBoxXY(layerKey, "mat_lux_champagne_brass", st.x - 0.85, st.x + 0.85, st.y - 1.95, st.y - 1.80, zBot + 0.01, zBot + 0.14, false);
      });

      // Glowing 3D highlight box for selected unit's parking spot
      const hlGeom = new THREE.BoxGeometry(2.35, 1.60, 4.50);
      const hlMat = new THREE.MeshBasicMaterial({ color: 0x10b981, transparent: true, opacity: 0.42, side: THREE.DoubleSide });
      parkingHighlightMesh = new THREE.Mesh(hlGeom, hlMat);
      parkingHighlightMesh.visible = false;
      layerGroups[layerKey].add(parkingHighlightMesh);
    }

    // =========================================================================
    // LUXURY PENTHOUSE DUPLEXES PB & PC (FLOORS 6 & 7: +19.72m & +22.95m)
    // Includes: Internal Wood & Glass Staircases, Living/Kitchen, Outdoor BBQ Kitchens,
    // Pergola Dining/Lounge Sets, and Rooftop Jacuzzi Spa Pools!
    // =========================================================================
    function buildLuxuryPenthousesF6F7() {
      isBuildingInteriorFurniture = true;
      const zF6 = 19.72, zF6C = 22.55, zF7 = 22.95, zF7C = 25.53;

      // 1. Track Penthouse Floor 6 & 7 Roof Terraces as walkable & deck-switchable
      const f6Deck = addExtrudedPolygon(L_F6, "mat_lux_travertine_floor", POLY_F6_WALLS, zF6 + 0.004, zF6 + 0.018, false);
      const f7Deck = addExtrudedPolygon(L_F7, "mat_lux_travertine_floor", POLY_UPPER_ROOF_OUTER, zF7 + 0.004, zF7 + 0.018, false);
      if (f6Deck) aptCFloorMeshes.push(f6Deck);
      if (f7Deck) aptCFloorMeshes.push(f7Deck);

      // 2. Internal Wood & Glass Staircase in Duplex PB (X=9.65..11.75, Y=7.15..9.55, Z=19.72..22.95)
      const nSteps = 16;
      for (let s = 0; s < nSteps; s++) {
        const zs = zF6 + (s + 1) * ((zF7 - zF6) / nSteps);
        const ys = 7.20 + (s / nSteps) * 2.25;
        addBoxXY(L_F6, "mat_lux_oak_smooth", 9.85, 10.95, ys, ys + 0.22, zs - 0.05, zs, false);
      }
      addBoxXY(L_F6, "mat_lux_clear_glass", 10.92, 10.96, 7.20, 9.45, zF6 + 0.15, zF7 + 0.95, false);
      addBoxXY(L_F6, "mat_lux_champagne_brass", 10.90, 10.98, 7.20, 9.45, zF7 + 0.92, zF7 + 0.97, false);

      // 3. Internal Wood & Glass Staircase in Duplex PC (X=20.15..23.55, Y=11.45..12.55, Z=19.72..22.95)
      for (let s = 0; s < nSteps; s++) {
        const zs = zF6 + (s + 1) * ((zF7 - zF6) / nSteps);
        const xs = 23.45 - (s / nSteps) * 3.10;
        addBoxXY(L_F6, "mat_lux_oak_smooth", xs - 0.22, xs, 11.55, 12.50, zs - 0.05, zs, false);
      }
      addBoxXY(L_F6, "mat_lux_clear_glass", 20.30, 23.45, 11.52, 11.56, zF6 + 0.15, zF7 + 0.95, false);
      addBoxXY(L_F6, "mat_lux_champagne_brass", 20.30, 23.45, 11.50, 11.58, zF7 + 0.92, zF7 + 0.97, false);

      // 4. Duplex PB (West Penthouse) Floor 6 Interior: Living Room, Chef's Island Kitchen & Dining
      addBoxAptB(L_F6, "mat_lux_rug_woven",     7.80, 11.10, 0.95, 3.65, zF6 + 0.020, zF6 + 0.032, false);
      addBoxAptB(L_F6, "mat_lux_oak_smooth",    8.10, 10.80, 2.95, 3.75, zF6 + 0.04,  zF6 + 0.16,  false);
      addBoxAptB(L_F6, "mat_lux_boucle_cream",  8.15, 10.75, 2.98, 3.60, zF6 + 0.16,  zF6 + 0.44,  false);
      addBoxAptB(L_F6, "mat_lux_linen_sand",    8.10, 10.80, 3.58, 3.75, zF6 + 0.16,  zF6 + 0.80,  false);
      addCylAptB(L_F6, "mat_lux_calacatta_marble", 9.45, 2.10, zF6 + 0.03, zF6 + 0.40, 0.42);
      // PB Kitchen & Waterfall Island (u=4.40..7.40, s=0.45..3.20)
      addBoxAptB(L_F6, "mat_lux_cabinet_cream",    4.40, 7.40, 0.35, 1.00, zF6 + 0.02, zF6 + 0.88, false);
      addBoxAptB(L_F6, "mat_lux_calacatta_marble", 4.40, 7.40, 0.35, 1.02, zF6 + 0.88, zF6 + 0.92, false);
      addBoxAptB(L_F6, "mat_lux_fluted_oak",       5.10, 6.80, 1.85, 2.55, zF6 + 0.02, zF6 + 0.88, false);
      addBoxAptB(L_F6, "mat_lux_calacatta_marble", 5.05, 6.85, 1.80, 2.60, zF6 + 0.88, zF6 + 0.92, false);

      // 5. Duplex PB Floor 6 Roof Terrace (+19.72m): Outdoor BBQ Kitchen, Pergola Dining & Rooftop Jacuzzi!
      // Rooftop Jacuzzi Spa Pool (X=16.60..18.85, Y=18.20..20.15)
      addBoxXY(L_F6, "mat_wood_deck",        16.55, 18.90, 18.15, 20.20, zF6 + 0.02, zF6 + 0.62, true);
      addBoxXY(L_F6, "mat_lux_ceramic_white", 16.75, 18.70, 18.35, 20.00, zF6 + 0.62, zF6 + 0.66, false);
      addBoxXY(L_F6, "mat_jacuzzi_water",    16.82, 18.63, 18.42, 19.93, zF6 + 0.54, zF6 + 0.64, false);
      // Outdoor Lounge under PB Pergola (X=16.45..17.65, Y=16.05..17.85)
      addBoxXY(L_F6, "mat_lux_oak_smooth",   16.50, 17.55, 16.15, 17.75, zF6 + 0.03, zF6 + 0.32, false);
      addBoxXY(L_F6, "mat_lux_boucle_cream", 16.55, 17.50, 16.20, 17.70, zF6 + 0.32, zF6 + 0.46, false);
      // PB Outdoor BBQ Kitchen (X=19.20..21.05, Y=19.50..20.45)
      addBoxXY(L_F6, "mat_lux_fluted_oak",       19.20, 21.05, 19.50, 20.20, zF6 + 0.02, zF6 + 0.88, false);
      addBoxXY(L_F6, "mat_lux_calacatta_marble", 19.18, 21.07, 19.48, 20.22, zF6 + 0.88, zF6 + 0.92, false);
      addBoxXY(L_F6, "mat_lux_dark_glass",       19.75, 20.50, 19.55, 20.12, zF6 + 0.92, zF6 + 1.18, false); // BBQ Grill Hood

      // 6. Duplex PC (East Penthouse) Floor 6 Interior: Grand Living Room, Island Kitchen & Dining
      addBoxXY(L_F6, "mat_lux_rug_woven",        25.20, 29.50, 9.20, 13.40, zF6 + 0.020, zF6 + 0.032, false);
      addBoxXY(L_F6, "mat_lux_oak_smooth",       25.50, 28.80, 9.40, 10.25, zF6 + 0.04,  zF6 + 0.16,  false);
      addBoxXY(L_F6, "mat_lux_boucle_cream",     25.55, 28.75, 9.45, 10.15, zF6 + 0.16,  zF6 + 0.44,  false);
      addBoxXY(L_F6, "mat_lux_linen_sand",       25.50, 28.80, 9.35, 9.52,  zF6 + 0.16,  zF6 + 0.80,  false);
      addCylinder3D(L_F6, "mat_lux_calacatta_marble", 27.20, 11.20, zF6 + 0.03, zF6 + 0.40, 0.46);
      // PC Kitchen & Island (X=26.20..29.95, Y=4.55..7.45)
      addBoxXY(L_F6, "mat_lux_cabinet_cream",    26.20, 29.85, 4.55, 5.20, zF6 + 0.02, zF6 + 0.88, false);
      addBoxXY(L_F6, "mat_lux_calacatta_marble", 26.20, 29.85, 4.55, 5.22, zF6 + 0.88, zF6 + 0.92, false);
      addBoxXY(L_F6, "mat_lux_fluted_oak",       27.10, 28.90, 6.00, 6.75, zF6 + 0.02, zF6 + 0.88, false);
      addBoxXY(L_F6, "mat_lux_calacatta_marble", 27.05, 28.95, 5.95, 6.80, zF6 + 0.88, zF6 + 0.92, false);

      // 7. Duplex PC Floor 6 NE Roof Terrace (+19.72m): Outdoor BBQ Kitchen, Pergola Dining & Rooftop Jacuzzi!
      // Rooftop Jacuzzi Spa Pool on NE Curved Terrace (X=25.40..28.10, Y=18.20..20.40)
      addBoxXY(L_F6, "mat_wood_deck",        25.35, 28.15, 18.15, 20.45, zF6 + 0.02, zF6 + 0.62, true);
      addBoxXY(L_F6, "mat_lux_ceramic_white", 25.55, 27.95, 18.35, 20.25, zF6 + 0.62, zF6 + 0.66, false);
      addBoxXY(L_F6, "mat_jacuzzi_water",    25.62, 27.88, 18.42, 20.18, zF6 + 0.54, zF6 + 0.64, false);
      // Outdoor 6-Person Dining Table under PC Wedge Pergola (X=24.80..27.20, Y=14.55..15.65)
      addBoxXY(L_F6, "mat_lux_oak_smooth",       24.80, 27.20, 14.65, 15.55, zF6 + 0.03, zF6 + 0.74, false);
      addBoxXY(L_F6, "mat_lux_calacatta_marble", 24.78, 27.22, 14.63, 15.57, zF6 + 0.74, zF6 + 0.78, false);
      // Outdoor BBQ Kitchen on PC Terrace (X=22.25..24.20, Y=15.50..16.25)
      addBoxXY(L_F6, "mat_lux_fluted_oak",       22.25, 24.20, 15.50, 16.20, zF6 + 0.02, zF6 + 0.88, false);
      addBoxXY(L_F6, "mat_lux_calacatta_marble", 22.22, 24.23, 15.48, 16.22, zF6 + 0.88, zF6 + 0.92, false);
      addBoxXY(L_F6, "mat_lux_dark_glass",       22.85, 23.60, 15.55, 16.12, zF6 + 0.92, zF6 + 1.18, false);

      // 8. Floor 7 Upper Penthouse Master Suites (PB West & PC East at +22.95m)
      // PC Grand Master Suite Bed & Lounge (X=21.20..25.60, Y=6.10..10.80)
      addBoxXY(L_F7, "mat_lux_rug_woven",     22.20, 25.10, 6.40, 9.20, zF7 + 0.020, zF7 + 0.032, false);
      addBoxXY(L_F7, "mat_lux_oak_smooth",    22.60, 24.60, 6.20, 8.20, zF7 + 0.03,  zF7 + 0.32,  false);
      addBoxXY(L_F7, "mat_lux_ceramic_white", 22.66, 24.54, 6.25, 8.15, zF7 + 0.32,  zF7 + 0.52,  false);
      addBoxXY(L_F7, "mat_lux_pillow_taupe",  22.64, 24.56, 7.20, 8.16, zF7 + 0.34,  zF7 + 0.54,  false);
      // PB Upper Master Bed (X=8.60..11.60, Y=11.60..14.10)
      addBoxXY(L_F7, "mat_lux_rug_woven",     8.60, 11.40, 11.80, 13.90, zF7 + 0.020, zF7 + 0.032, false);
      addBoxXY(L_F7, "mat_lux_oak_smooth",    8.80, 10.80, 12.10, 13.85, zF7 + 0.03,  zF7 + 0.32,  false);
      addBoxXY(L_F7, "mat_lux_ceramic_white", 8.86, 10.74, 12.15, 13.80, zF7 + 0.32,  zF7 + 0.52,  false);

      // Penthouse Interior & Rooftop Warm PointLights
      [
        [12.5, 16.5, zF6C - 0.25, L_F6], [27.2, 11.2, zF6C - 0.25, L_F6],
        [17.8, 18.8, zF6 + 2.20,  L_F6], [26.5, 18.5, zF6 + 2.20,  L_F6],
        [23.5, 7.8,  zF7C - 0.25, L_F7], [10.2, 12.8, zF7C - 0.25, L_F7]
      ].forEach(([lx, ly, lz, lk]) => {
        const pt = new THREE.PointLight(0xfff4dc, 0.72, 11.0, 1.5);
        pt.position.copy(cadTo3D(lx, ly, lz));
        pt.userData = { baseIntensity: 0.72 };
        layerGroups[lk].add(pt);
        interiorPointLights.push(pt);
      });
      isBuildingInteriorFurniture = false;
    }

    function addWindowAssembly(layerKey, origXY, uVec, nOutVec, u0, u1, z0, z1, hasShutter = true, numPanels = 2) {
      const w = u1 - u0, h = z1 - z0;
      if (w < 0.25 || h < 0.25) return;
      const ft = 0.055;
      // Sit neatly recessed inside the 25cm exterior wall (v from -0.15 to -0.02)
      addBoxAligned(layerKey, "mat_alu_frame", origXY, uVec, nOutVec, u0, u0 + ft, -0.15, -0.02, z0, z1, false);
      addBoxAligned(layerKey, "mat_alu_frame", origXY, uVec, nOutVec, u1 - ft, u1, -0.15, -0.02, z0, z1, false);
      addBoxAligned(layerKey, "mat_alu_frame", origXY, uVec, nOutVec, u0, u1, -0.15, 0.01, z0, z0 + ft, false);
      addBoxAligned(layerKey, "mat_alu_frame", origXY, uVec, nOutVec, u0, u1, -0.15, -0.02, z1 - ft, z1, false);

      let glassZ1 = z1 - ft;
      if (hasShutter && h >= 1.10) {
        const sbH = 0.20;
        addBoxAligned(layerKey, "mat_alu_frame", origXY, uVec, nOutVec, u0 + ft, u1 - ft, -0.14, -0.03, z1 - sbH, z1 - ft, false);
        glassZ1 = z1 - sbH;
      }
      const panelW = (w - 2 * ft) / numPanels;
      for (let p = 1; p < numPanels; p++) {
        const mu = u0 + ft + p * panelW;
        addBoxAligned(layerKey, "mat_alu_frame", origXY, uVec, nOutVec, mu - 0.022, mu + 0.022, -0.12, -0.04, z0 + ft, glassZ1, false);
      }
      if (h >= 2.0) {
        const zt = z0 + 1.05;
        addBoxAligned(layerKey, "mat_alu_frame", origXY, uVec, nOutVec, u0 + ft, u1 - ft, -0.12, -0.04, zt - 0.02, zt + 0.02, false);
      }
      addBoxAligned(layerKey, "mat_window_glass", origXY, uVec, nOutVec, u0 + ft, u1 - ft, -0.10, -0.06, z0 + ft, glassZ1, false);
    }

    // Parametric Water-Tight Exterior Wall Builder with Exact CAD Window & Vitrina Openings
    // Builds full-height piers between openings, sill walls ONLY under windows (NEVER under floor-to-ceiling vitrinas!),
    // lintel walls above openings, window/vitrina glazing assemblies, and Material B gray spandrel panels.
    function addExteriorWallWithOpenings(layerKey, p0, p1, thickness, zFlr, zCeil, openings = [], wallMatKey = "mat_D_white_plaster", zSoffit = null) {
      const dx = p1[0] - p0[0], dy = p1[1] - p0[1];
      const L = Math.hypot(dx, dy);
      if (L < 0.05) return;
      const ux = dx / L, uy = dy / L;
      // For clockwise polygon edges, outward normal is [-uy, ux]
      const nOut = [-uy, ux];
      const sorted = openings.slice().sort((a, b) => a.u0 - b.u0);

      let cursor = -0.04;
      for (let i = 0; i < sorted.length; i++) {
        const op = sorted[i];
        const u0 = Math.max(0.0, op.u0);
        const u1 = Math.min(L, op.u1);
        if (u0 > cursor + 0.01) {
          addBoxAligned(layerKey, wallMatKey, p0, [ux, uy], nOut, cursor, u0, -thickness, 0.0, zFlr, zCeil, true);
        }
        // Sill wall ONLY if zBot > zFlr + 0.08 (windows only; floor-to-ceiling vitrinas have zBot === zFlr!)
        if (op.zBot > zFlr + 0.08) {
          addBoxAligned(layerKey, wallMatKey, p0, [ux, uy], nOut, u0, u1, -thickness, 0.0, zFlr, op.zBot, true);
        }
        // Lintel header wall above opening
        if (op.zTop < zCeil - 0.02) {
          addBoxAligned(layerKey, wallMatKey, p0, [ux, uy], nOut, u0, u1, -thickness, 0.0, op.zTop, zCeil, true);
        }
        // Window or Vitrina assembly
        if (!op.openOnly) {
          addWindowAssembly(
            layerKey, p0, [ux, uy], nOut, u0, u1, op.zBot, op.zTop,
            op.shutter !== undefined ? op.shutter : true,
            op.panels || 2
          );
        }
        // Material B Gray Plaster vertical spandrel band above and below window (per Sheet A-1007)
        if (op.graySpandrel) {
          const zSpandrelBot = (zSoffit !== null) ? zSoffit : zFlr;
          if (op.zBot > zSpandrelBot + 0.05) {
            addBoxAligned(layerKey, "mat_B_gray_plaster", p0, [ux, uy], nOut, u0 - 0.03, u1 + 0.03, -0.02, 0.025, zSpandrelBot, op.zBot, false);
          }
          if (op.zTop < zCeil - 0.02) {
            addBoxAligned(layerKey, "mat_B_gray_plaster", p0, [ux, uy], nOut, u0 - 0.03, u1 + 0.03, -0.02, 0.025, op.zTop, zCeil, false);
          }
        }
        cursor = u1;
      }
      if (cursor < L + 0.04) {
        addBoxAligned(layerKey, wallMatKey, p0, [ux, uy], nOut, cursor, L + 0.04, -thickness, 0.0, zFlr, zCeil, true);
      }
    }

    // Stair treads and landings are rendered directly as exact 1:50 2D CAD markings on each floor slab
    function addStairFlight3D() {}
    function addCentralStairwell3D() {}

    function addIronRailingPath(layerKey, path2d, zBase, height = 1.05, curbH = 0.22, closed = false) {
      const n = path2d.length;
      const limit = closed ? n : n - 1;
      for (let i = 0; i < limit; i++) {
        const [x0, y0] = path2d[i];
        const [x1, y1] = path2d[(i + 1) % n];
        const dx = x1 - x0, dy = y1 - y0;
        const L = Math.hypot(dx, dy);
        if (L < 0.08) continue;
        const ux = dx / L, uy = dy / L;
        const nx = -uy, ny = ux;

        if (curbH > 0.01) {
          addBoxAligned(layerKey, "mat_concrete_curb", [x0, y0], [ux, uy], [nx, ny], 0, L, -0.09, 0.09, zBase, zBase + curbH, true);
        }
        const zR0 = zBase + curbH;
        const zR1 = zR0 + height;

        addBoxAligned(layerKey, "mat_A_iron_railing", [x0, y0], [ux, uy], [nx, ny], 0, L, -0.025, 0.025, zR1 - 0.04, zR1, false);
        addBoxAligned(layerKey, "mat_A_iron_railing", [x0, y0], [ux, uy], [nx, ny], 0, L, -0.02, 0.02, zR0 + 0.06, zR0 + 0.09, false);

        const numPickets = Math.max(2, Math.floor(L / 0.16));
        const step = L / numPickets;
        for (let k = 0; k <= numPickets; k++) {
          const s = k * step;
          const isPost = (k === 0 || k === numPickets || k % 8 === 0);
          const pw = isPost ? 0.036 : 0.018;
          const zBot = isPost ? zR0 : zR0 + 0.06;
          addBoxAligned(layerKey, "mat_A_iron_railing", [x0, y0], [ux, uy], [nx, ny], s - pw*0.5, s + pw*0.5, -pw*0.5, pw*0.5, zBot, zR1 - 0.03, false);
        }
      }
    }

    function addLouverScreen(layerKey, origXY, uVec, nOutVec, u0, u1, z0, z1, slatStep = 0.15) {
      const w = u1 - u0;
      addBoxAligned(layerKey, "mat_alu_frame", origXY, uVec, nOutVec, u0, u1, 0.01, 0.045, z0, z1, false);
      addBoxAligned(layerKey, "mat_C_white_louvers", origXY, uVec, nOutVec, u0, u0 + 0.06, 0.02, 0.12, z0, z1, false);
      addBoxAligned(layerKey, "mat_C_white_louvers", origXY, uVec, nOutVec, u1 - 0.06, u1, 0.02, 0.12, z0, z1, false);
      if (w > 1.30) {
        const um = 0.5 * (u0 + u1);
        addBoxAligned(layerKey, "mat_C_white_louvers", origXY, uVec, nOutVec, um - 0.025, um + 0.025, 0.03, 0.11, z0, z1, false);
      }
      for (let z = z0 + 0.05; z < z1 - 0.04; z += slatStep) {
        addBoxAligned(layerKey, "mat_C_white_louvers", origXY, uVec, nOutVec, u0 + 0.05, u1 - 0.05, 0.05, 0.115, z, z + 0.065, false);
      }
    }

    function addConcretePergola(layerKey, matKey, origXY, uVec, vVec, u0, u1, v0, v1, zBot, zTop, numBeams = 10) {
      const bw = 0.24;
      addBoxAligned(layerKey, matKey, origXY, uVec, vVec, u0, u1, v0, v0 + bw, zBot, zTop, true);
      addBoxAligned(layerKey, matKey, origXY, uVec, vVec, u0, u1, v1 - bw, v1, zBot, zTop, true);
      addBoxAligned(layerKey, matKey, origXY, uVec, vVec, u0, u0 + bw, v0 + bw, v1 - bw, zBot, zTop, true);
      addBoxAligned(layerKey, matKey, origXY, uVec, vVec, u1 - bw, u1, v0 + bw, v1 - bw, zBot, zTop, true);
      const span = (u1 - bw) - (u0 + bw);
      const step = span / (numBeams + 1);
      for (let k = 1; k <= numBeams; k++) {
        const uk = u0 + bw + k * step;
        addBoxAligned(layerKey, matKey, origXY, uVec, vVec, uk - 0.06, uk + 0.06, v0 + bw, v1 - bw, zBot + 0.04, zTop - 0.02, false);
      }
    }

    // =========================================================================
    // 0. SITE & GROUND FLOOR (קומת קרקע ולובי 0.00 = +39.62 .. +3.81)
    // =========================================================================
    const L_SITE = "0_site_and_ground";
    const L_F1_5 = "1_floors_1_to_5";
    const L_F6   = "2_floor_6_penthouse";
    const L_F7   = "3_floor_7_penthouse";
    const L_ROOF = "4_upper_roof_and_tower";

    // Triple-Resolution Georeferenced Google Maps Hybrid Terrain (centered on SW corner of Pines & HaBa'al Shem Tov):
    // 1. Outer Regional Z15 Plane: 7,253.7m x 7,253.7m (7.25 km x 7.25 km) covering all 27 POIs up to 1,935m
    // 2. Mid Neighborhood Z17 Plane: 1,619.1m x 1,619.1m (1.62 km x 1.62 km) sharp neighborhood streets
    // 3. Close-Up Intersection Z19 Plane: 259.1m x 259.1m at 0.25m/px ultra-sharp around Pines 48 corner HaBa'al Shem Tov
    const WIDE_GMAPS_DATA_URI = "__WIDE_GMAPS_DATA_URI__";
    const INNER_GMAPS_DATA_URI = "__INNER_GMAPS_DATA_URI__";
    const CLOSEUP_GMAPS_DATA_URI = "__CLOSEUP_GMAPS_DATA_URI__";
    const CENTER_LAT = 32.081015, CENTER_LON = 34.893785;
    const R_MERC = 6378137.0;
    const LAT0_RAD = CENTER_LAT * Math.PI / 180.0;
    const LON0_RAD = CENTER_LON * Math.PI / 180.0;
    const COS_LAT0 = Math.cos(LAT0_RAD);
    const MERC_Y0 = Math.asinh(Math.tan(LAT0_RAD));

    const OUTER_SPAN_M = 7253.739;   // Exact Web Mercator span of 1792x1792 Z15 tiles
    const OUTER_HALF_M = OUTER_SPAN_M * 0.5;
    const INNER_SPAN_M = 1619.138;   // Exact Web Mercator span of 1600x1600 Z17 tiles
    const INNER_HALF_M = INNER_SPAN_M * 0.5;
    const CLOSEUP_SPAN_M = 259.062;  // Exact Web Mercator span of 1024x1024 Z19 tiles
    const CLOSEUP_HALF_M = CLOSEUP_SPAN_M * 0.5;

    // Align North-up Google Maps with 3D Building street orientation (Pines St North facade + HaBa'al Shem Tov East facade)
    const GMAPS_THETA = 28.9 * Math.PI / 180.0;
    const GMAPS_CT = Math.cos(GMAPS_THETA), GMAPS_ST = Math.sin(GMAPS_THETA);

    function geoMetersTo3D(eastM, northM, y3d = -0.06) {
      const dx = eastM * GMAPS_CT + northM * GMAPS_ST;
      const dy = -eastM * GMAPS_ST + northM * GMAPS_CT;
      return new THREE.Vector3(dx, y3d, -dy);
    }

    // Exact Web Mercator projection from (lat, lon) to ground meters relative to (CENTER_LAT, CENTER_LON)
    // Guarantees 100% mathematical 1:1 pixel match between POI coordinates and Google Maps tiles!
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

    const wideGoogleMapsMesh = createGeoreferencedMapMesh(OUTER_HALF_M, -0.18, WIDE_GMAPS_DATA_URI, 6);
    const googleMapsPlaneMesh = createGeoreferencedMapMesh(INNER_HALF_M, -0.10, INNER_GMAPS_DATA_URI, 4);
    const closeupGoogleMapsMesh = createGeoreferencedMapMesh(CLOSEUP_HALF_M, -0.04, CLOSEUP_GMAPS_DATA_URI, 2);
    closeupGoogleMapsMesh.receiveShadow = true;
    layerGroups[L_SITE].add(wideGoogleMapsMesh);
    layerGroups[L_SITE].add(googleMapsPlaneMesh);
    layerGroups[L_SITE].add(closeupGoogleMapsMesh);

    // =========================================================================
    // 3D CONCENTRIC DISTANCE RINGS (150m TO 2,000m) & 27 VERIFIED POI LOCATIONS
    // =========================================================================
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
    let activeGisCategory = 'all';
    let selectedGisPoiId = null;

    // 8 Concentric Distance Rings covering all 27 POIs (from 42m up to 1,935m!)
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

    GIS_RINGS_CONFIG.forEach((rc, idx) => {
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
      ringMesh.position.set(0, 0.35, 0);
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
      haloMesh.position.set(0, 0.25, 0);
      gisRingsGroup.add(haloMesh);

      // Two floating HTML distance badges per ring (at opposite diagonals so always readable)
      [0.65, -2.49].forEach(ang => {
        const el = document.createElement('div');
        el.style.cssText = `position:absolute;transform:translate(-50%,-50%);background:rgba(15,23,42,0.92);color:#ffffff;border:2px solid ${rc.css};border-radius:999px;padding:2px 10px;font-size:11px;font-weight:800;white-space:nowrap;box-shadow:0 3px 10px rgba(0,0,0,0.40);pointer-events:none;transition:opacity 0.15s;`;
        el.textContent = `⭕ ${rc.label}`;
        gisLabelsContainer.appendChild(el);
        gisRingLabelObjs.push({
          el,
          pos: new THREE.Vector3(rc.r * Math.cos(ang), 3.0, rc.r * Math.sin(ang))
        });
      });
    });

    const GIS_CAT_STYLES = {
      education: { icon: "🎓", label: "מוסד חינוך / בית ספר", hex: 0x2563eb, css: "#2563eb" },
      transport: { icon: "🚌", label: "תחבורה ציבורית וצירים", hex: 0xd97706, css: "#d97706" },
      shopping:  { icon: "🛒", label: "מרכז קניות ומסחר",    hex: 0x9333ea, css: "#9333ea" },
      parks:     { icon: "🌳", label: "פארק, ספורט וקהילה",   hex: 0x059669, css: "#059669" },
      health:    { icon: "🏥", label: "בריאות ומרפאות",       hex: 0xdc2626, css: "#dc2626" }
    };

    const SPATIAL_POIS = __SPATIAL_POIS_JSON__;

    function focusCameraOnGisPoi(poi) {
      if (!poi) return;
      selectedGisPoiId = poi.id;
      showGisActiveCard(poi);

      const p3d = latLonTo3D(poi.lat, poi.lon, 0.35);
      isFirstPersonAptC = false;
      fpAnim = null;
      isOrtho = false;
      activeCam = perspCam;
      perspCam.fov = 42;
      perspCam.updateProjectionMatrix();
      setClipHeight(29.5);
      document.getElementById('aptc-tour-hud').style.display = 'none';

      // Center view at midpoint between Pines 48 Building (0,0,0) and the selected POI so user sees both and their exact relationship!
      target.set(p3d.x * 0.48, 4.0, p3d.z * 0.48);
      const dist3D = Math.hypot(p3d.x, p3d.z);
      spherical.radius = Math.max(260, Math.min(2200, dist3D * 1.45 + 140));
      spherical.phi = 0.58;
      updateCameraFromSpherical();

      // Highlight selected POI in sidebar list and on map
      gisPoiLabelObjs.forEach(item => {
        const isSel = (item.poi.id === poi.id);
        item.el.style.transform = isSel ? 'translate(-50%,-105%) scale(1.18)' : 'translate(-50%,-100%) scale(1.0)';
        item.el.style.zIndex = isSel ? '30' : '10';
        item.el.style.boxShadow = isSel ? `0 0 0 3px #fde047, 0 8px 20px rgba(0,0,0,0.6)` : '0 4px 12px rgba(0,0,0,0.40)';
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
      const gmapsUrl = `https://www.google.com/maps/dir/32.081015,34.893785/${poi.lat},${poi.lon}`;
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
        <div style="font-size:12px;color:#cbd5e1;margin-bottom:6px;">${poi.sub}</div>
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
          <a href="pines48_spatial_map.html" target="_blank" style="display:flex;align-items:center;justify-content:center;gap:4px;padding:7px 8px;border-radius:8px;background:#334155;color:#38bdf8;font-size:11px;font-weight:800;text-decoration:none;">
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

      // 1. Radial 3D vector line from Pines 48 3D Building (0, 1.0, 0) to exact POI coordinates
      const lineGeom = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, 1.0, 0),
        new THREE.Vector3(p3d.x, 1.0, p3d.z)
      ]);
      const lineMat = new THREE.LineBasicMaterial({ color: st.hex, transparent: true, opacity: 0.82 });
      subGrp.add(new THREE.Line(lineGeom, lineMat));

      // 2. Ground Target Ring + White Core on the Map (scaled gently with distance so distant POIs up to 1.94km are clearly visible)
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

      // 3. Vertical 3D Beacon Stem + Glowing Sphere Top
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

      // 4. Interactive Floating HTML Badge projected at top of 3D beacon
      const badgeEl = document.createElement('div');
      const distShort = poi.dist_m >= 1000 ? `${(poi.dist_m / 1000).toFixed(2)} ק"מ` : `${poi.dist_m} מ'`;
      badgeEl.style.cssText = `position:absolute;transform:translate(-50%,-100%);background:rgba(15,23,42,0.93);color:#ffffff;border:2px solid ${st.css};border-radius:10px;padding:3px 8px;font-size:11px;font-weight:700;white-space:nowrap;box-shadow:0 4px 12px rgba(0,0,0,0.40);pointer-events:auto;cursor:pointer;display:flex;align-items:center;gap:5px;transition:transform 0.15s,opacity 0.15s;z-index:10;`;
      badgeEl.innerHTML = `
        <span style="width:18px;height:18px;border-radius:999px;background:${st.css};color:#fff;display:inline-flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;">${poi.id}</span>
        <span>${poi.name}</span>
        <span style="background:rgba(56,189,248,0.20);color:#38bdf8;padding:1px 5px;border-radius:5px;font-weight:800;font-size:10px;">${distShort}</span>
      `;
      badgeEl.addEventListener('click', (ev) => {
        ev.stopPropagation();
        focusCameraOnGisPoi(poi);
      });
      gisLabelsContainer.appendChild(badgeEl);

      // 5. Sidebar Directory Row for instant 1-click verification & camera fly-to
      let sidebarRow = null;
      if (gisSidebarList) {
        sidebarRow = document.createElement('div');
        sidebarRow.style.cssText = `display:flex;align-items:center;justify-content:space-between;gap:6px;padding:4px 7px;border-radius:6px;border:1px solid #e2e8f0;background:#ffffff;cursor:pointer;font-size:11px;transition:background 0.15s;`;
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

    // Site Lot & Landscaping on top of the Google Maps base
    addExtrudedPolygon(L_SITE, "mat_site_ground", POLY_LOT, -0.03, 0.00, true);
    addExtrudedPolygon(L_SITE, "mat_landscape_green", [[0.25, 0.25], [3.80, 0.25], [3.80, 21.20], [0.25, 21.20]], 0.00, 0.08, false);
    addExtrudedPolygon(L_SITE, "mat_landscape_green", [ptUV(-2.0, -3.8), ptUV(21.5, -3.8), ptUV(21.5, -2.3), ptUV(-2.0, -2.3)], 0.00, 0.08, false);

    // Red Dashed Building Setback Line (קו בניין)
    for (let i = 0; i < POLY_SETBACK.length; i++) {
      const p0 = POLY_SETBACK[i], p1 = POLY_SETBACK[(i + 1) % POLY_SETBACK.length];
      const dx = p1[0] - p0[0], dy = p1[1] - p0[1], L = Math.hypot(dx, dy);
      if (L < 0.1) continue;
      const ux = dx / L, uy = dy / L, nx = -uy, ny = ux;
      for (let s = 0; s < L; s += 1.05) {
        addBoxAligned(L_SITE, "mat_cad_setback", p0, [ux, uy], [nx, ny], s, Math.min(L, s + 0.65), -0.06, 0.06, 0.01, 0.04, false);
      }
    }

    // Parking Ramp (South-East) & South Smoke-Ventilation Portals (matching bot_elev_3_south.png & bot_elev_2_east.png)
    addExtrudedPolygon(L_SITE, "mat_concrete_curb", [[19.5, 0.15], [33.85, 0.15], [33.85, 0.40], [19.5, 0.40]], -2.50, 1.15, true);
    addExtrudedPolygon(L_SITE, "mat_concrete_curb", [[19.5, 3.85], [33.85, 3.85], [33.85, 4.10], [19.5, 4.10]], -2.50, 1.15, true);
    // South & West Perimeter Concrete Portal Beams (+2.81..+3.37, per bot_elev_3_south.png & bot_elev_1_west.png)
    addBoxAligned(L_SITE, "mat_D_white_plaster", [4.00, 4.00], [1, 0], [0, 1], 0.0, 13.25, 0.0, 0.30, 2.81, 3.37, true);
    [4.00, 9.20, 12.40, 14.00, 17.00].forEach(px => {
      addBoxAligned(L_SITE, "mat_D_white_plaster", [px, 4.00], [1, 0], [0, 1], 0.0, 0.35, 0.0, 0.30, 0.0, 2.81, true);
    });
    // Three bays of South vertical iron railings above natural smoke ventilation shafts (bot_elev_3_south.png)
    addIronRailingPath(L_SITE, [[4.35, 4.15], [9.20, 4.15]], 0.0, 1.15, 0.25);
    addIronRailingPath(L_SITE, [[9.55, 4.15], [12.40, 4.15]], 0.0, 1.15, 0.25);
    addIronRailingPath(L_SITE, [[14.35, 4.15], [17.00, 4.15]], 0.0, 1.15, 0.25);

    // Ground Floor Enclosed Lobby & Service Envelope (matching bot_elev_4_north_legend.png, bot_elev_2_east.png, bot_elev_3_south.png, bot_elev_1_west.png)
    const POLY_GROUND_FLOOR = [
      [4.045, 17.266],
      [26.990, 22.106],
      [29.122, 20.717],
      [30.726, 13.134],
      [30.351, 12.150],
      [30.351, 4.199],
      [17.251, 4.199],
      [17.251, 4.951],
      [12.399, 4.951],
      [12.399, 6.517],
      [6.572, 5.287]
    ];
    addExtrudedPolygon(L_SITE, "mat_terrace_tile", POLY_GROUND_FLOOR, 0.00, 0.06, true);

    // Ground Floor North Facade (bot_elev_4_north_legend.png):
    // Main Entrance Glazed Vitrina under NC Balcony (u=12.80..17.20, z=0.00..2.81) + Secondary Glazed/Louver Bay to East (u=18.20..21.20, z=0.00..2.81)
    addExteriorWallWithOpenings(L_SITE, [4.045, 17.266], [26.990, 22.106], 0.25, 0.00, 3.81, [
      { u0: 12.80, u1: 17.20, zBot: 0.00, zTop: 2.81, panels: 3, shutter: false },
      { u0: 18.20, u1: 21.20, zBot: 0.00, zTop: 2.81, panels: 2, shutter: true }
    ]);
    // Ground Floor NE Corner Wall
    addExteriorWallWithOpenings(L_SITE, [26.990, 22.106], [29.122, 20.717], 0.25, 0.00, 3.81, []);
    // Ground Floor East-North Facade (bot_elev_2_east.png):
    // Square louver window on North-East room (u=1.20..2.20, z=1.10..2.10) + 3-panel Lobby Glazed Curtain Wall in center (u=3.60..7.10, z=0.00..2.81)
    addExteriorWallWithOpenings(L_SITE, [29.122, 20.717], [30.726, 13.134], 0.25, 0.00, 3.81, [
      { u0: 1.20, u1: 2.20, zBot: 1.10, zTop: 2.10, panels: 1, shutter: false, openOnly: true },
      { u0: 3.60, u1: 7.10, zBot: 0.00, zTop: 2.81, panels: 3, shutter: false }
    ]);
    addLouverScreen(L_SITE, [29.122, 20.717], [(30.726-29.122)/7.75, (13.134-20.717)/7.75], [(20.717-13.134)/7.75, (30.726-29.122)/7.75], 1.20, 2.20, 1.10, 2.10, 0.12);
    // Ground Floor East-South Facade (under East Balcony, bot_elev_2_east.png):
    addExteriorWallWithOpenings(L_SITE, [30.351, 12.150], [30.351, 4.199], 0.25, 0.00, 3.81, []);
    // Ground Floor South Facade (bot_elev_3_south.png: square louver at X=26.0..27.0, z=1.10..2.10):
    addExteriorWallWithOpenings(L_SITE, [30.351, 4.199], [17.251, 4.199], 0.25, 0.00, 3.81, [
      { u0: 3.35, u1: 4.35, zBot: 1.10, zTop: 2.10, panels: 1, shutter: false, openOnly: true }
    ]);
    addLouverScreen(L_SITE, [30.351, 4.199], [-1, 0], [0, -1], 3.35, 4.35, 1.10, 2.10, 0.12);
    // Ground Floor SW & West Facades (bot_elev_1_west.png):
    addExteriorWallWithOpenings(L_SITE, [17.251, 4.951], [12.399, 4.951], 0.25, 0.00, 3.81, []);
    addExteriorWallWithOpenings(L_SITE, [12.399, 6.517], [6.572, 5.287], 0.25, 0.00, 3.81, []);
    addExteriorWallWithOpenings(L_SITE, [6.572, 5.287], [4.045, 17.266], 0.25, 0.00, 3.81, []);

    // Ground Floor Core Walls & Central Stairwell
    const groundPolys = PLANS["f1_5"].wall_polys || [];
    for (let i = 0; i < groundPolys.length; i++) {
      const wp = groundPolys[i];
      if (wp.exterior && wp.exterior.some(([x, y]) => x >= 12.2 && x <= 19.2 && y >= 10.8 && y <= 16.2)) {
        addWallPolygonMesh(L_SITE, "mat_interior_wall", wp, 0.00, 3.81);
      }
    }
    addCentralStairwell3D(L_SITE, 0.00, 3.81);
    buildLuxuryGroundLobby(L_SITE);
    buildUndergroundParkingBasement();

    // Helper for balcony warm wood soffits, recessed spotlights, and corner planters
    function addBalconySoffitAndLighting(layerKey, bPoly, zSoffit, zFlr) {
      addExtrudedPolygon(layerKey, "mat_lux_oak_smooth", bPoly, zSoffit - 0.015, zSoffit + 0.002, false);
      let cx = 0, cy = 0;
      bPoly.forEach(p => { cx += p[0]; cy += p[1]; });
      cx /= bPoly.length; cy /= bPoly.length;
      // Warm LED strip under balcony slab
      addBoxXY(layerKey, "mat_lux_glow_warm", cx - 0.65, cx + 0.65, cy - 0.04, cy + 0.04, zSoffit - 0.025, zSoffit - 0.01, false);
      const spPos = cadTo3D(cx, cy, zSoffit - 0.05);
      const spot = new THREE.PointLight(0xffdca8, 0.0, 7.5, 2.0);
      spot.position.copy(spPos);
      layerGroups[layerKey].add(spot);
      balconySpotLights.push(spot);
      // Corner architectural planter on balcony floor
      if (bPoly.length >= 3) {
        const cPt = bPoly[1];
        const px = cx * 0.25 + cPt[0] * 0.75;
        const py = cy * 0.25 + cPt[1] * 0.75;
        addBoxXY(layerKey, "mat_B_gray_plaster", px - 0.24, px + 0.24, py - 0.24, py + 0.24, zFlr, zFlr + 0.42, false);
        addBoxXY(layerKey, "mat_landscape_green", px - 0.20, px + 0.20, py - 0.20, py + 0.20, zFlr + 0.42, zFlr + 0.78, false);
      }
    }

    // =========================================================================
    // 1. FLOORS 1 TO 5 (קומות 1–5 — דירות A, B, C — Sheet A-1002 & A-1007)
    // =========================================================================
    const FLOOR_LEVELS_1_5 = [
      [1, 3.81, 4.25, 6.92],
      [2, 6.92, 7.31, 9.98],
      [3, 9.98, 10.37, 13.04],
      [4, 13.04, 13.43, 16.10],
      [5, 16.10, 16.49, 19.16]
    ];

    const neBeamPoly = [...NE_ARC_OUTER, ...NE_ARC_INNER.slice().reverse()];

    FLOOR_LEVELS_1_5.forEach(([fnum, zSoffit, zFlr, zCeil]) => {
      // Floor slab following the exact recessed North wall + curved NE balcony
      addExtrudedPolygon(L_F1_5, "mat_terrace_tile", POLY_F1_5_SLAB, zSoffit, zFlr, true);

      // Extracted 3D interior walls + 2D floor markings (furniture, wardrobes, kitchens, sanitary fixtures, doors)
      addExtractedFloorWalls(L_F1_5, "f1_5", zFlr, zCeil);
      addCentralStairwell3D(L_F1_5, zFlr, zCeil + 0.39);

      const zSill = zFlr + 0.85, zMamadSill = zFlr + 1.05, zHead = zFlr + 2.35, zDoor = zFlr + 2.42;

      // Exact Water-Tight Exterior Walls & Openings for Floors 1-5 (verified from A-1002 & A-1007)
      // Edge 0 & 1: NW corner pier and 60cm recess step
      addExteriorWallWithOpenings(L_F1_5, [4.045, 17.266], [4.436, 17.349], 0.25, zFlr, zCeil, [], "mat_D_white_plaster", zSoffit);
      addExteriorWallWithOpenings(L_F1_5, [4.436, 17.349], [4.560, 16.761], 0.25, zFlr, zCeil, [], "mat_D_white_plaster", zSoffit);

      // Edge 2: Recessed North Wall (4.560, 16.761) -> (21.096, 20.250), L = 16.90m
      addExteriorWallWithOpenings(L_F1_5, [4.560, 16.761], [21.096, 20.250], 0.25, zFlr, zCeil, [
        { u0: 0.75,  u1: 2.15,  zBot: zSill, zTop: zHead, panels: 2, shutter: true,  graySpandrel: true },
        { u0: 4.25,  u1: 7.25,  zBot: zFlr,  zTop: zDoor, panels: 3, shutter: true,  graySpandrel: false, openOnly: (fnum === 3) }, // Apt B NW Balcony Vitrina (open on Floor 3 for walkthrough!)
        { u0: 8.55,  u1: 9.25,  zBot: zSill, zTop: zHead, panels: 1, shutter: false, graySpandrel: true },  // Core West window
        { u0: 10.75, u1: 11.75, zBot: zSill, zTop: zHead, panels: 2, shutter: true,  graySpandrel: true },  // Apt A Kitchen North window
        { u0: 12.90, u1: 15.90, zBot: zFlr,  zTop: zDoor, panels: 3, shutter: true,  graySpandrel: false, openOnly: (fnum === 3) } // Apt A NC Balcony Vitrina (open on Floor 3 for walkthrough!)
      ], "mat_D_white_plaster", zSoffit);
      if (fnum === 3) {
        // Open sliding vitrina frame + stacked clear glass panel on West side of Apt B NW Balcony opening
        addBoxAligned(L_F1_5, "mat_alu_frame", [4.560, 16.761], EU, EN_NORTH, 4.25, 7.25, -0.16, -0.02, zDoor - 0.18, zDoor, false);
        addBoxAligned(L_F1_5, "mat_alu_frame", [4.560, 16.761], EU, EN_NORTH, 4.25, 4.31, -0.16, -0.02, zFlr, zDoor, false);
        addBoxAligned(L_F1_5, "mat_alu_frame", [4.560, 16.761], EU, EN_NORTH, 7.19, 7.25, -0.16, -0.02, zFlr, zDoor, false);
        addBoxAligned(L_F1_5, "mat_alu_frame", [4.560, 16.761], EU, EN_NORTH, 5.25, 5.31, -0.14, -0.04, zFlr, zDoor - 0.18, false);
        addBoxAligned(L_F1_5, "mat_lux_clear_glass", [4.560, 16.761], EU, EN_NORTH, 4.31, 5.25, -0.11, -0.07, zFlr + 0.04, zDoor - 0.18, false);

        // Open sliding vitrina frame + stacked clear glass panel on West side of Apt A North Balcony opening
        addBoxAligned(L_F1_5, "mat_alu_frame", [4.560, 16.761], EU, EN_NORTH, 12.90, 15.90, -0.16, -0.02, zDoor - 0.18, zDoor, false);
        addBoxAligned(L_F1_5, "mat_alu_frame", [4.560, 16.761], EU, EN_NORTH, 12.90, 12.96, -0.16, -0.02, zFlr, zDoor, false);
        addBoxAligned(L_F1_5, "mat_alu_frame", [4.560, 16.761], EU, EN_NORTH, 15.84, 15.90, -0.16, -0.02, zFlr, zDoor, false);
        addBoxAligned(L_F1_5, "mat_alu_frame", [4.560, 16.761], EU, EN_NORTH, 13.90, 13.96, -0.14, -0.04, zFlr, zDoor - 0.18, false);
        addBoxAligned(L_F1_5, "mat_lux_clear_glass", [4.560, 16.761], EU, EN_NORTH, 12.96, 13.90, -0.11, -0.07, zFlr + 0.04, zDoor - 0.18, false);
      }
      // Gray Plaster B accent pier next to Apt B Master Bedroom window & Apt A North Bedroom window (per bot_elev_4_north_legend.png)
      addBoxAligned(L_F1_5, "mat_B_gray_plaster", [4.560, 16.761], EU, EN_NORTH, 2.15, 3.65, -0.02, 0.03, zSoffit, zCeil, false);

      // Edge 3: 60cm step back out to outer line at u = 17.30
      addExteriorWallWithOpenings(L_F1_5, [21.096, 20.250], [20.972, 20.837], 0.25, zFlr, zCeil, [], "mat_D_white_plaster", zSoffit);

      // Edge 4: Flush North Wall (20.972, 20.837) -> (26.990, 22.106), L = 6.15m
      addExteriorWallWithOpenings(L_F1_5, [20.972, 20.837], [26.990, 22.106], 0.25, zFlr, zCeil, [
        { u0: 1.50, u1: 2.90, zBot: zSill, zTop: zHead, panels: 2, shutter: true, graySpandrel: true } // Apt A Master Bedroom North Window (centered over Master Bed!)
      ], "mat_D_white_plaster", zSoffit);
      addBoxAligned(L_F1_5, "mat_B_gray_plaster", [20.972, 20.837], EU, EN_NORTH, 0.00, 1.50, -0.02, 0.03, zSoffit, zCeil, false);

      // Edge 5 & 6: Inner Walls behind the Curved NE Decorative Beam (aligned with W4 & W3)
      addExteriorWallWithOpenings(L_F1_5, [26.990, 22.106], [27.412, 20.356], 0.25, zFlr, zCeil, [
        { u0: 1.00, u1: 1.60, zBot: zMamadSill, zTop: zFlr + 2.15, panels: 1, shutter: false } // Apt A Master En-Suite Bathroom Window
      ], "mat_D_white_plaster", zSoffit);
      addExteriorWallWithOpenings(L_F1_5, [27.412, 20.356], [29.122, 20.717], 0.25, zFlr, zCeil, [], "mat_D_white_plaster", zSoffit);

      // Edge 7: East-North Tilted Wall (29.122, 20.717) -> (30.726, 13.134), L = 7.75m
      addExteriorWallWithOpenings(L_F1_5, [29.122, 20.717], [30.726, 13.134], 0.25, zFlr, zCeil, [
        { u0: 0.95, u1: 1.95, zBot: zMamadSill, zTop: zFlr + 2.15, panels: 1, shutter: false, graySpandrel: true }, // Apt A Mamad window
        { u0: 3.95, u1: 5.35, zBot: zSill,      zTop: zHead,       panels: 2, shutter: true,  graySpandrel: true }, // Apt A East Bedroom window
        { u0: 6.25, u1: 7.25, zBot: zFlr,       zTop: zHead,       panels: 1, shutter: false, graySpandrel: false } // Laundry door behind Louver C
      ], "mat_D_white_plaster", zSoffit);

      // Edge 8 & 9: Step at Y=12.150
      addExteriorWallWithOpenings(L_F1_5, [30.726, 13.134], [30.726, 12.150], 0.25, zFlr, zCeil, [], "mat_D_white_plaster", zSoffit);
      addExteriorWallWithOpenings(L_F1_5, [30.726, 12.150], [30.351, 12.150], 0.25, zFlr, zCeil, [], "mat_D_white_plaster", zSoffit);

      // Edge 10: East Vertical Wall (30.351, 12.150) -> (30.351, 4.199), L = 7.951m
      addExteriorWallWithOpenings(L_F1_5, [30.351, 12.150], [30.351, 4.199], 0.25, zFlr, zCeil, [
        { u0: 1.20, u1: 4.20, zBot: zFlr,  zTop: zDoor, panels: 3, shutter: true, graySpandrel: false, openOnly: (fnum === 3) }, // East Balcony Vitrina (open on Floor 3 for walkthrough!)
        { u0: 6.00, u1: 7.40, zBot: zSill, zTop: zHead, panels: 2, shutter: true, graySpandrel: true }   // SE Bedroom East Window
      ], "mat_D_white_plaster", zSoffit);
      if (fnum === 3) {
        // Open sliding vitrina frame + stacked clear glass panel on North side of opening (Y=7.95..10.95)
        addBoxXY(L_F1_5, "mat_alu_frame", 30.18, 30.32, 7.95, 10.95, zDoor - 0.18, zDoor, false);
        addBoxXY(L_F1_5, "mat_alu_frame", 30.18, 30.32, 7.95, 8.01,  zFlr, zDoor, false);
        addBoxXY(L_F1_5, "mat_alu_frame", 30.18, 30.32, 10.89, 10.95, zFlr, zDoor, false);
        addBoxXY(L_F1_5, "mat_alu_frame", 30.20, 30.28, 9.90, 9.96,  zFlr, zDoor - 0.18, false);
        addBoxXY(L_F1_5, "mat_lux_clear_glass", 30.22, 30.26, 9.95, 10.90, zFlr + 0.04, zDoor - 0.18, false);
      }

      // Edge 11: South-East Wall (30.351, 4.199) -> (22.849, 4.199), L = 7.502m
      addExteriorWallWithOpenings(L_F1_5, [30.351, 4.199], [22.849, 4.199], 0.25, zFlr, zCeil, [
        { u0: 1.05, u1: 2.45, zBot: zSill,      zTop: zHead,       panels: 2, shutter: true,  graySpandrel: true }, // Apt C Kitchen/Dining South Window (X=29.30..27.90)
        { u0: 5.15, u1: 6.55, zBot: zSill,      zTop: zHead,       panels: 2, shutter: true,  graySpandrel: true }  // Apt C South Bedroom Window (X=25.20..23.80)
      ], "mat_D_white_plaster", zSoffit);

      // Edge 12 & 13: South-Center Wall (22.849, 4.100) -> (17.251, 4.100), L = 5.598m
      addExteriorWallWithOpenings(L_F1_5, [22.849, 4.199], [22.849, 4.100], 0.25, zFlr, zCeil, [], "mat_D_white_plaster", zSoffit);
      addExteriorWallWithOpenings(L_F1_5, [22.849, 4.100], [17.251, 4.100], 0.25, zFlr, zCeil, [
        { u0: 1.15, u1: 2.25, zBot: zMamadSill, zTop: zFlr + 2.15, panels: 1, shutter: false, graySpandrel: true }, // Apt C Mamad Window (X=21.70..20.60)
        { u0: 4.00, u1: 4.55, zBot: zMamadSill, zTop: zFlr + 2.15, panels: 1, shutter: false, graySpandrel: true }  // Apt C Bathroom Window (X=18.85..18.30)
      ], "mat_D_white_plaster", zSoffit);

      // Edge 14 & 15: Master Bedroom & South Service Wall (17.251, 4.951) -> (12.399, 4.951), L = 4.852m
      addExteriorWallWithOpenings(L_F1_5, [17.251, 4.100], [17.251, 4.951], 0.25, zFlr, zCeil, [], "mat_D_white_plaster", zSoffit);
      addExteriorWallWithOpenings(L_F1_5, [17.251, 4.951], [12.399, 4.951], 0.25, zFlr, zCeil, [
        { u0: 0.55, u1: 1.95, zBot: zSill, zTop: zHead, panels: 2, shutter: true,  graySpandrel: true }, // Apt C Master Bedroom South Window (X=16.70..15.30, centered over Master Bed!)
        { u0: 2.60, u1: 3.40, zBot: zFlr,  zTop: zHead, panels: 1, shutter: false, graySpandrel: false } // Service balcony door (X=14.65..13.85)
      ], "mat_D_white_plaster", zSoffit);

      // Edge 16 & 17: South-West Step & Tilted Wall (12.399, 6.517) -> (6.572, 5.287), L = 5.955m
      addExteriorWallWithOpenings(L_F1_5, [12.399, 4.951], [12.399, 6.517], 0.25, zFlr, zCeil, [], "mat_D_white_plaster", zSoffit);
      addExteriorWallWithOpenings(L_F1_5, [12.399, 6.517], [6.572, 5.287], 0.25, zFlr, zCeil, [], "mat_D_white_plaster", zSoffit);

      // Edge 18: West Tilted Wall (6.572, 5.287) -> (4.045, 17.266), L = 12.242m
      addExteriorWallWithOpenings(L_F1_5, [6.572, 5.287], [4.045, 17.266], 0.25, zFlr, zCeil, [
        { u0: 1.29,  u1: 2.29,  zBot: zMamadSill, zTop: zFlr + 2.15, panels: 1, shutter: false, graySpandrel: true }, // Apt B Mamad Window
        { u0: 3.34,  u1: 4.34,  zBot: zSill,      zTop: zHead,       panels: 1, shutter: false, graySpandrel: false }, // Laundry behind West Louver C
        { u0: 5.94,  u1: 6.44,  zBot: zMamadSill, zTop: zHead,       panels: 1, shutter: false, graySpandrel: true }, // Bathroom 1
        { u0: 7.69,  u1: 8.19,  zBot: zMamadSill, zTop: zHead,       panels: 1, shutter: false, graySpandrel: true }, // Bathroom 2
        { u0: 10.64, u1: 11.24, zBot: zSill,      zTop: zHead,       panels: 1, shutter: true,  graySpandrel: true }  // Bedroom West Window
      ], "mat_D_white_plaster", zSoffit);

      // Curved NE Decorative Concrete Beam ("קורה דקורטיבית" in white plaster D — NO RAILINGS on Floors 1-5 per A-1002 & A-1007!)
      addExtrudedPolygon(L_F1_5, "mat_D_white_plaster", neBeamPoly, zSoffit - 0.14, zFlr, true);

      // NW, NC, East, and South Service Balconies (Floors 1-5) + Warm Wood Soffits & Spotlights
      [BALCONY_NW, BALCONY_NC, BALCONY_E].forEach(bPoly => {
        addExtrudedPolygon(L_F1_5, "mat_terrace_tile", bPoly, zSoffit, zFlr, true);
        addIronRailingPath(L_F1_5, bPoly, zFlr, 1.05, 0.22, false);
        addBalconySoffitAndLighting(L_F1_5, bPoly, zSoffit, zFlr);
      });
      addExtrudedPolygon(L_F1_5, "mat_terrace_tile", BALCONY_S_SERVICE, zSoffit, zFlr, true);
      addIronRailingPath(L_F1_5, [[13.601, 4.951], [13.601, 4.100], [15.150, 4.100]], zFlr, 1.05, 0.18);

      // Full Luxury 3D Interior Models of Apartments A, B, and C on Floor 3 (+10.37..+13.04)
      if (fnum === 3) {
        buildLuxuryApartmentC(L_F1_5, zFlr, zCeil);
        buildLuxuryApartmentA(L_F1_5, zFlr, zCeil);
        buildLuxuryApartmentB(L_F1_5, zFlr, zCeil);
      }
    });
    // Also add the Ground-Floor ceiling decorative curved NE beam at +3.11..+3.81 (per bot_elev_4_north_legend.png)
    addExtrudedPolygon(L_SITE, "mat_D_white_plaster", neBeamPoly, 3.11, 3.81, true);

    // Material B Vertical Balcony L-Frames (all 3 projecting balconies terminate at +19.41 with concrete pergolas per A-1003, A-1004, A-1006 & A-1007)
    addBoxAligned(L_F1_5, "mat_B_gray_plaster", NW_CORNER, EU, EN_NORTH, 8.55, 8.95, -0.60, 1.90, 3.81, 19.41, true);
    addBoxAligned(L_F1_5, "mat_B_gray_plaster", NW_CORNER, EU, EN_NORTH, 3.70, 4.10, -0.60, 0.35, 3.81, 19.41, true);
    addBoxAligned(L_F1_5, "mat_B_gray_plaster", NW_CORNER, EU, EN_NORTH, 12.35, 12.75, -0.60, 1.90, 3.81, 19.41, true);
    addBoxAligned(L_F1_5, "mat_B_gray_plaster", NW_CORNER, EU, EN_NORTH, 17.20, 17.60, -0.60, 0.35, 3.81, 19.41, true);
    addBoxAligned(L_F1_5, "mat_B_gray_plaster", [30.351, 0], [0, 1], [1, 0], 6.35, 6.75, 0.00, 2.20, 3.81, 19.41, true);
    addBoxAligned(L_F1_5, "mat_B_gray_plaster", [30.351, 0], [0, 1], [1, 0], 12.15, 12.55, 0.00, 0.40, 3.81, 19.41, true);

    // Material C: 3 White Aluminum Louver Laundry Shafts at EXACT CAD positions
    // 1. West Louver Shaft C: along West wall (6.572, 5.287)->(4.045, 17.266) at u = [3.10, 4.65], z = 4.11..22.39
    addLouverScreen(L_F1_5, [6.572, 5.287], [-ES[0], -ES[1]], EN_WEST, 3.10, 4.65, 4.11, 22.39);
    // 2. East-North Louver Shaft C: along East-North wall (29.122, 20.717)->(30.726, 13.134) at u = [5.85, 7.55], z = 4.11..19.16
    const enU = [(30.726 - 29.122)/7.75, (13.134 - 20.717)/7.75];
    const enN = [-enU[1], enU[0]];
    addLouverScreen(L_F1_5, [29.122, 20.717], enU, enN, 5.85, 7.55, 4.11, 19.16);
    // 3. South Louver Shaft C: along South service balcony (X = 13.60..15.15, Y = 4.100), z = 4.11..22.39
    addLouverScreen(L_F1_5, [15.150, 4.100], [-1, 0], [0, -1], 0.00, 1.55, 4.11, 22.39);

    // =========================================================================
    // 2. FLOOR 6 PENTHOUSE (קומה 6 — דופלקסים תחתון +19.16..+22.55 — Sheet A-1003)
    // =========================================================================
    const zF6Flr = 19.72, zF6Ceil = 22.55, zF6Sill = 20.57, zF6MamadSill = 20.77, zF6Head = 22.12, zF6Door = 22.17;

    // Floor 6 Deck Slab (includes roof terraces on NE and SE)
    addExtrudedPolygon(L_F6, "mat_terrace_tile", POLY_OUTER, 19.16, zF6Flr, true);
    addExtractedFloorWalls(L_F6, "f6", zF6Flr, zF6Ceil);

    // Exact Floor 6 Exterior Walls & Openings (verified from A-1003 & A-1007):
    // Edge 0: Duplex PB North Wall (4.045, 17.266) -> (15.495, 19.680), L = 11.70m
    addExteriorWallWithOpenings(L_F6, [4.045, 17.266], [15.495, 19.680], 0.25, zF6Flr, zF6Ceil, [
      { u0: 1.15, u1: 2.55,  zBot: zF6Sill,       zTop: zF6Head, panels: 2, shutter: true, graySpandrel: true },  // PB Master Bedroom
      { u0: 4.85, u1: 7.85,  zBot: zF6Flr + 0.15, zTop: zF6Door, panels: 3, shutter: true, graySpandrel: false }, // PB Kitchen 300/252(+15) window over +19.41 pergola
      { u0: 9.85, u1: 11.25, zBot: zF6Sill,       zTop: zF6Head, panels: 2, shutter: true, graySpandrel: false }  // PB Living Room North Window
    ], "mat_D_white_plaster", 19.16);
    addBoxAligned(L_F6, "mat_B_gray_plaster", [4.045, 17.266], EU, EN_NORTH, 2.55, 3.70, -0.02, 0.03, 19.16, zF6Ceil, false);

    // Edge 1: Duplex PB East Living Room Wall facing Roof Terrace (15.495, 19.680) -> (16.328, 15.716), L = 4.05m
    addExteriorWallWithOpenings(L_F6, [15.495, 19.680], [16.328, 15.716], 0.25, zF6Flr, zF6Ceil, [
      { u0: 0.25, u1: 3.65, zBot: zF6Flr, zTop: zF6Door, panels: 3, shutter: true } // 365/262 Sliding Vitrina to PB Roof Terrace
    ]);
    // Edge 2, 3, 4: Core & Lobby Step Walls
    addExteriorWallWithOpenings(L_F6, [16.328, 15.716], [18.089, 16.089], 0.25, zF6Flr, zF6Ceil, []);
    addExteriorWallWithOpenings(L_F6, [18.089, 16.089], [18.440, 16.368], 0.25, zF6Flr, zF6Ceil, []);
    addExteriorWallWithOpenings(L_F6, [18.440, 16.368], [19.039, 13.530], 0.25, zF6Flr, zF6Ceil, []);
    addExteriorWallWithOpenings(L_F6, [19.039, 13.530], [21.984, 14.150], 0.25, zF6Flr, zF6Ceil, [], "mat_B_gray_plaster");

    // Edge 5: Duplex PC Horizontal North Wall along Y=14.150: (21.984, 14.150) -> (30.351, 14.150), L = 8.367m (Gray Plaster B per top_elev_4_north_legend.png)
    addExteriorWallWithOpenings(L_F6, [21.984, 14.150], [30.351, 14.150], 0.25, zF6Flr, zF6Ceil, [
      { u0: 2.81, u1: 5.72, zBot: zF6Flr, zTop: zF6Door, panels: 3, shutter: true }, // PC Living Room North Vitrina (300cm)
      { u0: 6.67, u1: 7.47, zBot: zF6Flr, zTop: zF6Door, panels: 1, shutter: true }  // PC Dining North Glass Door (80cm)
    ], "mat_B_gray_plaster");

    // Edge 6: Duplex PC East Wall along X=30.351: (30.351, 14.150) -> (30.351, 7.550), L = 6.60m
    addExteriorWallWithOpenings(L_F6, [30.351, 14.150], [30.351, 7.550], 0.25, zF6Flr, zF6Ceil, [
      { u0: 0.55, u1: 1.95, zBot: zF6Sill,       zTop: zF6Head, panels: 2, shutter: true }, // PC Dining Room East Window (140cm)
      { u0: 2.55, u1: 5.55, zBot: zF6Flr + 0.15, zTop: zF6Door, panels: 3, shutter: true }  // PC Living Room East 300/252(+15) Window over +19.41 pergola
    ]);

    // Edge 7 & 8: Duplex PC SE Corner Terrace Walls: (30.351, 7.550)->(26.151, 7.550)->(26.151, 4.199)
    addExteriorWallWithOpenings(L_F6, [30.351, 7.550], [26.151, 7.550], 0.25, zF6Flr, zF6Ceil, [
      { u0: 2.20, u1: 3.83, zBot: zF6Flr, zTop: zF6Head, panels: 2, shutter: true }
    ]);
    addExteriorWallWithOpenings(L_F6, [26.151, 7.550], [26.151, 4.199], 0.25, zF6Flr, zF6Ceil, [
      { u0: 0.75, u1: 2.55, zBot: zF6Flr, zTop: zF6Head, panels: 2, shutter: true }
    ]);

    // Edge 9..16: Floor 6 South & West Walls
    addExteriorWallWithOpenings(L_F6, [26.151, 4.199], [22.849, 4.199], 0.25, zF6Flr, zF6Ceil, [
      { u0: 1.45, u1: 2.45, zBot: zF6MamadSill, zTop: zF6Flr + 2.15, panels: 1, shutter: false, graySpandrel: true }
    ], "mat_D_white_plaster", 19.16);
    addExteriorWallWithOpenings(L_F6, [22.849, 4.199], [22.849, 4.100], 0.25, zF6Flr, zF6Ceil, []);
    addExteriorWallWithOpenings(L_F6, [22.849, 4.100], [17.251, 4.100], 0.25, zF6Flr, zF6Ceil, [
      { u0: 1.55, u1: 2.95, zBot: zF6Sill,      zTop: zF6Head,       panels: 2, shutter: true,  graySpandrel: true },
      { u0: 4.00, u1: 4.50, zBot: zF6MamadSill, zTop: zF6Flr + 2.15, panels: 1, shutter: false, graySpandrel: true }
    ], "mat_D_white_plaster", 19.16);
    addExteriorWallWithOpenings(L_F6, [17.251, 4.100], [17.251, 4.951], 0.25, zF6Flr, zF6Ceil, []);
    addExteriorWallWithOpenings(L_F6, [17.251, 4.951], [12.399, 4.951], 0.25, zF6Flr, zF6Ceil, [
      { u0: 1.10, u1: 2.00, zBot: zF6Sill, zTop: zF6Head, panels: 1, shutter: false },
      { u0: 2.60, u1: 3.40, zBot: zF6Flr,  zTop: zF6Head, panels: 1, shutter: false }
    ], "mat_D_white_plaster", 19.16);
    addExteriorWallWithOpenings(L_F6, [12.399, 4.951], [12.399, 6.517], 0.25, zF6Flr, zF6Ceil, []);
    addExteriorWallWithOpenings(L_F6, [12.399, 6.517], [6.572, 5.287], 0.25, zF6Flr, zF6Ceil, []);
    addExteriorWallWithOpenings(L_F6, [6.572, 5.287], [4.045, 17.266], 0.25, zF6Flr, zF6Ceil, [
      { u0: 1.29,  u1: 2.29,  zBot: zF6MamadSill, zTop: zF6Flr + 2.15, panels: 1, shutter: false, graySpandrel: true },
      { u0: 3.34,  u1: 4.34,  zBot: zF6Sill,      zTop: zF6Head,       panels: 1, shutter: false, graySpandrel: false },
      { u0: 5.94,  u1: 6.44,  zBot: zF6MamadSill, zTop: zF6Head,       panels: 1, shutter: false, graySpandrel: true },
      { u0: 7.69,  u1: 8.19,  zBot: zF6MamadSill, zTop: zF6Head,       panels: 1, shutter: false, graySpandrel: true },
      { u0: 10.64, u1: 11.24, zBot: zF6Sill,      zTop: zF6Head,       panels: 1, shutter: true,  graySpandrel: true }
    ], "mat_D_white_plaster", 19.16);

    // Floor 6 South Service Balcony
    addExtrudedPolygon(L_F6, "mat_terrace_tile", BALCONY_S_SERVICE, 19.16, zF6Flr, true);
    addIronRailingPath(L_F6, [[13.601, 4.951], [13.601, 4.100], [15.150, 4.100]], zF6Flr, 1.05, 0.18);

    // The 3 Projecting Balcony Pergolas at +19.16..+19.41 (over Floor 5 NW, NC, and East balconies, per A-1003, A-1004, A-1006 & A-1007)
    addConcretePergola(L_F6, "mat_D_white_plaster", NW_CORNER, EU, EN_NORTH, 3.90, 8.60, 0.0, 2.10, 19.16, 19.41, 10);
    addConcretePergola(L_F6, "mat_D_white_plaster", NW_CORNER, EU, EN_NORTH, 12.60, 17.30, 0.0, 2.10, 19.16, 19.41, 10);
    addConcretePergola(L_F6, "mat_D_white_plaster", [30.351, 0], [0, 1], [1, 0], 6.75, 12.15, 0.0, 2.20, 19.16, 19.41, 11);

    // Floor 6 NE & SE Roof Terraces Railings + Privacy Divider Wall (+21.72) + SE Corner Frame
    addIronRailingPath(L_F6, [[16.861, 19.969], ...NE_ARC_OUTER, [30.726, 13.134], [30.726, 12.150], [30.351, 12.150]], zF6Flr, 1.05, 0.22);
    addWallStrip(L_F6, "mat_D_white_plaster", [[21.25, 20.89], [21.984, 14.150]], 0.20, zF6Flr, 21.72, false, true);
    addIronRailingPath(L_F6, [[26.151, 4.199], [30.351, 4.199], [30.351, 7.550]], zF6Flr, 1.05, 0.22);
    // SE Corner column & perimeter beam framing the SE corner terrace (per top_elev_2_east.png & top_elev_3_south.png)
    addBoxAligned(L_F6, "mat_D_white_plaster", [30.10, 4.20], [1, 0], [0, 1], 0.0, 0.25, 0.0, 0.25, zF6Flr, 24.00, true);
    addWallStrip(L_F6, "mat_D_white_plaster", [[26.151, 4.199], [30.351, 4.199], [30.351, 7.550]], 0.24, 22.55, 24.00, false, true);

    // =========================================================================
    // 3. FLOOR 7 PENTHOUSE (קומה 7 — דופלקסים עליון +22.95..+25.53 — Sheet A-1004)
    // =========================================================================
    const zF7Flr = 22.95, zF7Ceil = 25.53, zF7Sill = 23.80, zF7BathSill = 24.00, zF7Head = 25.20;

    // Floor 7 Slab covering Floor 6 enclosed area
    addExtrudedPolygon(L_F7, "mat_terrace_tile", POLY_F6_WALLS, 22.55, zF7Flr, true);
    addExtractedFloorWalls(L_F7, "f7", zF7Flr, zF7Ceil);
    addCentralStairwell3D(L_F7, zF7Flr, zF7Ceil);

    // Exact Floor 7 Enclosed Apartment Exterior Walls & Openings (POLY_UPPER_ROOF_OUTER, verified from A-1004 & A-1007):
    // Edge 0: North Wall (7.628, 14.086) -> (18.440, 16.368), L = 11.05m (Gray Plaster B on PB North Room & Core)
    addExteriorWallWithOpenings(L_F7, [7.628, 14.086], [18.440, 16.368], 0.25, zF7Flr, zF7Ceil, [
      { u0: 3.70, u1: 4.20,  zBot: zF7BathSill, zTop: zF7Head, panels: 1, shutter: false }, // Narrow vertical bathroom window (top_elev_4_north_legend.png)
      { u0: 8.85, u1: 10.05, zBot: zF7Sill,     zTop: zF7Head, panels: 2, shutter: false }  // Core stairwell/lobby window
    ], "mat_B_gray_plaster");

    // Edges 1..5: North-East Stepped Walls of Floor 7 (Gray Plaster B per top_elev_4_north_legend.png)
    addExteriorWallWithOpenings(L_F7, [18.440, 16.368], [19.039, 13.530], 0.25, zF7Flr, zF7Ceil, [], "mat_B_gray_plaster");
    addExteriorWallWithOpenings(L_F7, [19.039, 13.530], [21.984, 14.150], 0.25, zF7Flr, zF7Ceil, [], "mat_B_gray_plaster");
    addExteriorWallWithOpenings(L_F7, [21.984, 14.150], [23.899, 14.150], 0.25, zF7Flr, zF7Ceil, [], "mat_B_gray_plaster");
    addExteriorWallWithOpenings(L_F7, [23.899, 14.150], [23.899, 11.250], 0.25, zF7Flr, zF7Ceil, [], "mat_B_gray_plaster");
    addExteriorWallWithOpenings(L_F7, [23.899, 11.250], [26.151, 11.250], 0.25, zF7Flr, zF7Ceil, [], "mat_B_gray_plaster");

    // Edge 6: East Wall of PC Master Suite along X=26.151: (26.151, 11.250) -> (26.151, 5.850), L = 5.40m (Gray Plaster B per top_elev_2_east.png)
    addExteriorWallWithOpenings(L_F7, [26.151, 11.250], [26.151, 5.850], 0.25, zF7Flr, zF7Ceil, [
      { u0: 2.30, u1: 3.30, zBot: zF7Flr,  zTop: zF7Head, panels: 1, shutter: true }, // East Terrace Glass Door (100cm, NO sill wall!)
      { u0: 3.95, u1: 4.75, zBot: zF7Sill, zTop: zF7Head, panels: 1, shutter: true }  // East Master Suite Window (80cm)
    ], "mat_B_gray_plaster");

    // Edge 7: South Wall of PC Master Suite along Y=5.850: (26.151, 5.850) -> (18.201, 5.848), L = 7.95m (Gray Plaster B per top_elev_3_south.png)
    addExteriorWallWithOpenings(L_F7, [26.151, 5.850], [18.201, 5.848], 0.25, zF7Flr, zF7Ceil, [
      { u0: 1.55, u1: 3.35, zBot: zF7Flr,      zTop: zF7Head, panels: 2, shutter: true  }, // PC Master Bedroom South Vitrina (180cm)
      { u0: 6.55, u1: 7.05, zBot: zF7BathSill, zTop: zF7Head, panels: 1, shutter: false }  // PC Master Bath South Window (50cm)
    ], "mat_B_gray_plaster");

    // Edges 8..12: South Recessed Patio Walls
    addExteriorWallWithOpenings(L_F7, [18.201, 5.848], [18.201, 9.550], 0.25, zF7Flr, zF7Ceil, []);
    addExteriorWallWithOpenings(L_F7, [18.201, 9.550], [17.437, 9.550], 0.25, zF7Flr, zF7Ceil, []);
    addExteriorWallWithOpenings(L_F7, [17.437, 9.550], [17.437, 10.329], 0.25, zF7Flr, zF7Ceil, []);
    addExteriorWallWithOpenings(L_F7, [17.437, 10.329], [15.502, 9.921], 0.25, zF7Flr, zF7Ceil, []);
    addExteriorWallWithOpenings(L_F7, [15.502, 9.921], [15.970, 7.698], 0.25, zF7Flr, zF7Ceil, []);

    // Edge 13: South Wall of PB South Bedroom (15.970, 7.698) -> (10.295, 6.502), L = 5.80m
    addExteriorWallWithOpenings(L_F7, [15.970, 7.698], [10.295, 6.502], 0.25, zF7Flr, zF7Ceil, [
      { u0: 1.20, u1: 3.00, zBot: zF7Flr, zTop: zF7Head, panels: 2, shutter: true } // PB South Bedroom Vitrina (180cm)
    ]);

    // Edge 14 & 15: West Wall of PB Corridor (10.295, 6.502) -> (9.394, 10.778), L = 4.37m
    addExteriorWallWithOpenings(L_F7, [10.295, 6.502], [9.394, 10.778], 0.25, zF7Flr, zF7Ceil, [
      { u0: 3.37, u1: 4.37, zBot: zF7Sill, zTop: zF7Head, panels: 1, shutter: true }
    ]);
    addExteriorWallWithOpenings(L_F7, [9.394, 10.778], [8.371, 10.564], 0.25, zF7Flr, zF7Ceil, []);

    // Edge 16: West Wall of PB North Bedroom (8.371, 10.564) -> (7.628, 14.086), L = 3.60m (Gray Plaster B per top_elev_1_west.png)
    addExteriorWallWithOpenings(L_F7, [8.371, 10.564], [7.628, 14.086], 0.25, zF7Flr, zF7Ceil, [
      { u0: 0.60, u1: 2.40, zBot: zF7Flr, zTop: zF7Head, panels: 2, shutter: true } // PB North Bedroom Vitrina (180cm)
    ], "mat_B_gray_plaster");

    // Floor 7 Open-Sky Roof Terraces Parapet Walls (+24.00) & The Two Exact +24.00 Pergolas (verified from A-1004, A-1006 & A-1007):
    // 1. PB West, North-West & East Terrace Parapet Wall up to +24.00
    addWallStrip(L_F7, "mat_D_white_plaster", [[6.572, 5.287], [4.045, 17.266], [15.495, 19.680], [16.328, 15.716], [18.089, 16.089], [18.049, 16.284], [18.440, 16.368]], 0.22, 22.55, 24.00, false, true);

    // 2. Exact Floor 7 Pergola #1: Duplex PB East Overhanging Pergola at +23.65..+24.00 (1.40m × 4.05m, two bays of 1.20×1.82m shading PB's Floor 6 terrace)
    // Outer frame beams & middle divider beam
    addExtrudedPolygon(L_F7, "mat_D_white_plaster", [[15.495, 19.680], [16.861, 19.969], [16.902, 19.774], [15.534, 19.484]], 23.65, 24.00, true);
    addExtrudedPolygon(L_F7, "mat_D_white_plaster", [[16.666, 19.928], [16.861, 19.969], [17.697, 16.006], [17.502, 15.965]], 23.65, 24.00, true);
    addExtrudedPolygon(L_F7, "mat_D_white_plaster", [[15.911, 17.697], [17.088, 17.947], [17.130, 17.750], [15.951, 17.503]], 23.65, 24.00, true);
    addExtrudedPolygon(L_F7, "mat_D_white_plaster", [[16.294, 15.879], [17.507, 15.966], [17.697, 16.006], [16.328, 15.716]], 23.65, 24.00, true);
    // Support column at NE corner of PB pergola descending to Floor 6 wall/terrace (+19.72..+24.00)
    addExtrudedPolygon(L_F7, "mat_D_white_plaster", [[16.666, 19.928], [16.861, 19.969], [16.902, 19.774], [16.707, 19.733]], 19.16, 24.00, true);
    // 10 exact CAD pergola slats (5 in North bay, 5 in South bay)
    [
      [[15.564, 19.340], [16.743, 19.590], [16.772, 19.442], [15.596, 19.194]],
      [[15.657, 18.900], [16.834, 19.149], [16.866, 19.001], [15.687, 18.754]],
      [[15.752, 18.447], [16.931, 18.697], [16.961, 18.550], [15.784, 18.301]],
      [[15.845, 18.006], [17.022, 18.256], [17.054, 18.110], [15.875, 17.860]],
      [[15.981, 17.359], [17.160, 17.609], [17.192, 17.460], [16.013, 17.213]],
      [[16.074, 16.919], [17.253, 17.168], [17.285, 17.020], [16.106, 16.772]],
      [[16.169, 16.466], [17.348, 16.715], [17.380, 16.567], [16.201, 16.319]],
      [[16.262, 16.025], [17.441, 16.275], [17.473, 16.127], [16.294, 15.879]]
    ].forEach(slatPoly => addExtrudedPolygon(L_F7, "mat_D_white_plaster", slatPoly, 23.68, 23.98, false));

    // 3. PC East Roof Terrace Parapet Wall (+24.00 around מרפסת +22.93)
    addWallStrip(L_F7, "mat_D_white_plaster", [[26.151, 7.550], [30.351, 7.550], [30.351, 14.150], [23.899, 14.150]], 0.22, 22.55, 24.00, false, true);

    // 4. Exact Floor 7 Pergola #2: Duplex PC North-East Wedge Pergola at +23.65..+24.00 (projecting North from Y=14.150 over PC's Floor 6 terrace)
    addExtrudedPolygon(L_F7, "mat_D_white_plaster", [[30.201, 14.150], [30.351, 14.150], [30.036, 15.900], [29.881, 15.663]], 23.65, 24.00, true);
    addExtrudedPolygon(L_F7, "mat_D_white_plaster", [[21.984, 14.150], [22.708, 14.150], [29.881, 15.663], [30.036, 15.900], [21.984, 14.200]], 23.65, 24.00, true);
    // Support column at NE corner of PC wedge pergola descending to Floor 6 wall (+19.72..+24.00)
    addExtrudedPolygon(L_F7, "mat_D_white_plaster", [[29.881, 15.663], [30.075, 15.704], [30.036, 15.900], [29.842, 15.859]], 19.72, 24.00, true);
    // 12 exact CAD perpendicular pergola slats inside PC wedge pergola
    [
      [[24.682, 14.150], [24.835, 14.150], [24.744, 14.580], [24.598, 14.548]],
      [[25.142, 14.150], [25.294, 14.150], [25.184, 14.673], [25.038, 14.641]],
      [[25.601, 14.150], [25.756, 14.150], [25.624, 14.766], [25.478, 14.734]],
      [[26.063, 14.150], [26.215, 14.150], [26.065, 14.859], [25.919, 14.827]],
      [[26.522, 14.150], [26.674, 14.150], [26.505, 14.952], [26.359, 14.920]],
      [[26.981, 14.150], [27.136, 14.150], [26.945, 15.043], [26.799, 15.014]],
      [[27.440, 14.150], [27.595, 14.150], [27.385, 15.136], [27.239, 15.107]],
      [[27.902, 14.150], [28.054, 14.150], [27.826, 15.229], [27.680, 15.200]],
      [[28.361, 14.150], [28.514, 14.150], [28.266, 15.323], [28.120, 15.293]],
      [[28.821, 14.150], [28.975, 14.150], [28.706, 15.416], [28.560, 15.384]],
      [[29.282, 14.150], [29.434, 14.150], [29.146, 15.509], [29.000, 15.477]],
      [[29.741, 14.150], [29.894, 14.150], [29.587, 15.602], [29.441, 15.570]]
    ].forEach(slatPoly => addExtrudedPolygon(L_F7, "mat_D_white_plaster", slatPoly, 23.68, 23.98, false));

    // 5. South & South-West Terrace Parapet Wall (+22.55..+24.00, open-sky terrace with NO pergola per A-1004)
    addWallStrip(L_F7, "mat_D_white_plaster", [[6.572, 5.287], [12.399, 6.517], [12.399, 4.951], [17.251, 4.951], [17.251, 4.100], [22.849, 4.100], [22.849, 4.199], [26.151, 4.199], [26.151, 5.850]], 0.24, 22.55, 24.00, false, true);

    // Build Full Luxury Penthouse Duplexes PB & PC (Floors 6-7 + Roof Terraces + Jacuzzis + Outdoor Kitchens)
    buildLuxuryPenthousesF6F7();

    // =========================================================================
    // 4. UPPER ROOF & STAIRWELL/ELEVATOR TOWER (+25.53..+28.67 — Sheet A-1006)
    // =========================================================================
    addExtrudedPolygon(L_ROOF, "mat_terrace_tile", POLY_UPPER_ROOF_OUTER, 25.30, 25.53, true);
    // Roof Parapets (Gray Plaster B on West/North/East/South Master Suite volumes up to +26.97, White Plaster D up to +27.37)
    addWallStrip(L_ROOF, "mat_B_gray_plaster", [[8.371, 10.564], [7.628, 14.086], [12.611, 14.933]], 0.26, 25.53, 26.97, false, true);
    addWallStrip(L_ROOF, "mat_B_gray_plaster", [[19.039, 13.530], [21.984, 14.150], [23.899, 14.150], [23.899, 11.250], [26.151, 11.250], [26.151, 5.850], [18.201, 5.848]], 0.26, 25.53, 26.97, false, true);
    addWallStrip(L_ROOF, "mat_D_white_plaster", [[18.201, 5.848], [18.201, 9.550], [17.437, 9.550], [17.437, 10.329], [15.502, 9.921], [15.970, 7.698], [10.295, 6.502], [9.394, 10.778], [8.371, 10.564]], 0.25, 25.53, 27.37, false, true);

    // Central Stairwell & Elevator Tower (+25.53..+28.67)
    addWallStrip(L_ROOF, "mat_D_white_plaster", POLY_TOWER_OUTER, 0.25, 25.53, 28.67, true, true);
    addExtrudedPolygon(L_ROOF, "mat_D_white_plaster", POLY_TOWER_OUTER, 28.45, 28.67, true);
    addWindowAssembly(L_ROOF, [13.354, 11.411], EU, [-EN_NORTH[0], -EN_NORTH[1]], 1.20, 2.20, 25.60, 27.70, false, 1);
    addWindowAssembly(L_ROOF, [12.611, 14.933], EU, EN_NORTH, 1.10, 2.90, 26.50, 28.10, false, 2);

    function addSolarCollector(origXY, uVec, vVec) {
      const w = 1.40, l = 1.50, zD = 25.53;
      addBoxAligned(L_ROOF, "mat_alu_frame", origXY, uVec, vVec, 0.05, 0.12, 0.10, l - 0.10, zD, zD + 0.22, false);
      addBoxAligned(L_ROOF, "mat_alu_frame", origXY, uVec, vVec, w - 0.12, w - 0.05, 0.10, l - 0.10, zD, zD + 0.22, false);
      addBoxAligned(L_ROOF, "mat_alu_frame", origXY, uVec, vVec, 0.08, w - 0.08, 0.10, l - 0.10, zD + 0.22, zD + 0.58, true);
      addBoxAligned(L_ROOF, "mat_solar_panel", origXY, uVec, vVec, 0.12, w - 0.12, 0.14, l - 0.14, zD + 0.58, zD + 0.66, false);
      addBoxAligned(L_ROOF, "mat_C_white_louvers", origXY, uVec, vVec, 0.20, w - 0.20, l - 0.35, l + 0.05, zD + 0.66, zD + 0.98, true);
    }
    [[8.98, 12.15], [10.74, 12.52], [9.45, 7.66], [11.21, 8.03], [12.97, 8.40]].forEach(o => addSolarCollector(o, EU, EN_NORTH));
    [[18.92, 9.75], [20.80, 9.75], [18.88, 7.45], [20.88, 7.45], [22.88, 7.45]].forEach(o => addSolarCollector(o, [1, 0], [0, 1]));

    // Landscape Trees
    [[2.1, 3.0, 4.2], [1.8, 9.5, 5.0], [2.0, 15.5, 4.5], [6.0, 21.8, 4.8], [14.5, 23.6, 5.2], [23.5, 25.4, 4.6], [32.5, 16.5, 4.5], [32.5, 21.0, 4.2]].forEach(([tx, ty, th]) => {
      addBoxAligned(L_SITE, "mat_concrete_curb", [tx, ty], [1, 0], [0, 1], -0.12, 0.12, -0.12, 0.12, 0, th * 0.42, false);
      const oct1 = Array.from({length: 8}, (_, i) => [tx + 1.1*Math.cos(i*Math.PI/4), ty + 1.1*Math.sin(i*Math.PI/4)]);
      const oct2 = Array.from({length: 8}, (_, i) => [tx + 0.72*Math.cos(i*Math.PI/4), ty + 0.72*Math.sin(i*Math.PI/4)]);
      addExtrudedPolygon(L_SITE, "mat_landscape_green", oct1, th * 0.38, th * 0.85, false);
      addExtrudedPolygon(L_SITE, "mat_landscape_green", oct2, th * 0.85, th * 1.05, false);
    });

    // =========================================================================
    // FLOATING 3D CALLOUT LABELS (EXTERIOR + DYNAMIC INTERIOR ROOM LABELS)
    // =========================================================================
    const exteriorCallouts = [
      { text: "מגדל מדרגות ומעלית +28.67", pos: cadTo3D(14.8, 13.6, 29.1), mode: "ext" },
      { text: "קומה 7 (דופלקס עליון) +22.95", pos: cadTo3D(28.5, 9.5, 23.8), mode: "ext" },
      { text: "מרפסת גג קומה 6 +19.72", pos: cadTo3D(25.5, 19.5, 20.6), mode: "ext" },
      { text: "קומות 1–5 (דירות A, B, C)", pos: cadTo3D(10.0, 20.8, 11.5), mode: "ext" },
      { text: "קומת קרקע ולובי 0.00 (+39.62)", pos: cadTo3D(28.0, 19.0, 1.8), mode: "ext" },
      { text: "רחוב פינס (צפון)", pos: cadTo3D(16.0, 26.8, 0.4), mode: "both" },
      { text: "רחוב בעש\"ט (מזרח)", pos: cadTo3D(36.8, 13.0, 0.4), mode: "both" }
    ];

    const interiorRoomDefs = [
      // Basement (-3.50..0.00)
      { text: "מרתף חניה תת-קרקעי (-3.50) · 18 חניות ומחסנים", x: 18.0, y: 12.2, zMin: -3.6, zMax: 0.2, badgeClass: "dark" },
      // Floors 1-5 (zRange: 3.8..19.2)
      { text: "דירה B (3 חד') · ח. מגורים ומטבח", x: 10.6, y: 16.5, zMin: 3.8, zMax: 19.2, badgeClass: "blue" },
      { text: "דירה B · יח' הורים (365×295)", x: 6.4, y: 15.6, zMin: 3.8, zMax: 19.2 },
      { text: "דירה B · ממ\"ד (370×274)", x: 8.6, y: 8.5, zMin: 3.8, zMax: 19.2 },
      { text: "דירה A (4 חד') · ח. מגורים ומטבח", x: 19.5, y: 18.2, zMin: 3.8, zMax: 19.2, badgeClass: "emerald" },
      { text: "דירה A · יח' הורים (385×290)", x: 23.6, y: 19.6, zMin: 3.8, zMax: 19.2 },
      { text: "דירה A · ממ\"ד (337×280)", x: 28.0, y: 18.8, zMin: 3.8, zMax: 19.2 },
      { text: "דירה A · ח. שינה מזרחי", x: 28.4, y: 15.6, zMin: 3.8, zMax: 19.2 },
      { text: "דירה C (4 חד') · ח. מגורים ומטבח", x: 28.0, y: 9.8, zMin: 3.8, zMax: 19.2, badgeClass: "amber" },
      { text: "דירה C · יח' הורים (390×295)", x: 16.0, y: 6.4, zMin: 3.8, zMax: 19.2 },
      { text: "דירה C · ממ\"ד (325×292)", x: 21.3, y: 6.2, zMin: 3.8, zMax: 19.2 },
      { text: "דירה C · ח. שינה דרומי", x: 24.4, y: 6.2, zMin: 3.8, zMax: 19.2 },
      { text: "חדר מדרגות ומעלית (6 נוסעים)", x: 15.2, y: 12.8, zMin: 0.5, zMax: 25.5, badgeClass: "dark" },
      // Floor 6 Penthouse Duplexes Lower Level (zRange: 19.3..22.8)
      { text: "דופלקס PB (מערב) · ח. מגורים ומטבח", x: 10.8, y: 16.5, zMin: 19.3, zMax: 22.8, badgeClass: "blue" },
      { text: "דופלקס PB · מדרגות פנים לקומה 7", x: 9.8, y: 8.8, zMin: 19.3, zMax: 25.2 },
      { text: "דופלקס PC (מזרח) · ח. מגורים (600×510)", x: 25.5, y: 11.8, zMin: 19.3, zMax: 22.8, badgeClass: "emerald" },
      { text: "דופלקס PC · מרפסת גג, ג'קוזי ומטבח חוץ (+19.72)", x: 25.0, y: 17.5, zMin: 19.3, zMax: 22.8 },
      { text: "דופלקס PC · יח' הורים וממ\"ד", x: 21.8, y: 6.2, zMin: 19.3, zMax: 22.8 },
      // Floor 7 Penthouse Duplexes Upper Level (zRange: 22.8..25.6)
      { text: "דופלקס PB (קומה 7) · 2 חדרי שינה ויציאה לגג", x: 11.2, y: 12.5, zMin: 22.8, zMax: 25.6, badgeClass: "blue" },
      { text: "דופלקס PC (קומה 7) · סוויטת הורים (580×340)", x: 22.5, y: 8.2, zMin: 22.8, zMax: 25.6, badgeClass: "emerald" },
      { text: "מרפסת גג עליון ופרגולות (+22.95)", x: 27.8, y: 9.5, zMin: 22.8, zMax: 25.6 },
      // Ground Floor (zRange: 0.5..3.8)
      { text: "לובי כניסה ראשי מפואר (0.00 = +39.62)", x: 16.5, y: 15.8, zMin: 0.5, zMax: 3.8, badgeClass: "blue" },
      { text: "מועדון דיירים, חדר עגלות ומבואה", x: 22.0, y: 11.0, zMin: 0.5, zMax: 3.8 }
    ];

    let showLabels = true;
    const allCalloutObjs = [];

    exteriorCallouts.forEach(c => {
      const el = document.createElement('div');
      el.className = 'callout-pill';
      el.textContent = c.text;
      labelsContainer.appendChild(el);
      allCalloutObjs.push({ ...c, el, isInterior: false });
    });

    interiorRoomDefs.forEach(r => {
      const el = document.createElement('div');
      const extraCls = r.badgeClass || '';
      el.className = `callout-pill ${extraCls}`.trim();
      el.textContent = r.text;
      labelsContainer.appendChild(el);
      allCalloutObjs.push({ ...r, el, isInterior: true, pos: cadTo3D(r.x, r.y, 6.0) });
    });

    // =========================================================================
    // DUAL CAMERA CONTROLLER:
    // 1. FIRST-PERSON INTERIOR WALKTHROUGH INSIDE APARTMENTS A & C (WASD / Arrows / Mouse Look / Click-to-Walk)
    // 2. ORBIT / PAN / ZOOM CONTROLLER (Exterior & Dollhouse Cutaway Views)
    // =========================================================================
    perspCam.near = 0.08;
    perspCam.far = 10000;
    perspCam.updateProjectionMatrix();
    if (THREE.ACESFilmicToneMapping) {
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.08;
    }

    let isFirstPersonAptC = true;
    const fpEyePos = cadTo3D(25.85, 9.75, 11.95);
    let fpYaw = -1.35;   // Looking East-North-East toward Living Room sofa, coffee table, TV wall & East Balcony
    let fpPitch = -0.05;
    let fpAnim = null;   // Smooth glide animation between rooms

    const APT_C_ROOMS = {
      living_main: {
        title: "דירה C · סלון מרכזי ויציאה למרפסת שמש (480×400 ס\"מ)",
        eye: [25.85, 9.75, 11.95],
        look: [28.80, 10.55, 11.65]
      },
      living_from_balcony: {
        title: "דירה C · מבט פנורמי מוויטרינת המרפסת אל הסלון, האי ופינת האוכל",
        eye: [29.85, 10.55, 11.95],
        look: [26.85, 7.80, 11.55]
      },
      kitchen_island: {
        title: "דירה C · מטבח יוקרתי בגווני קשמיר ואלון חם + אי מפל שיש קלקטה",
        eye: [28.95, 7.65, 11.95],
        look: [26.35, 5.75, 11.45]
      },
      dining_area: {
        title: "דירה C · פינת אוכל פרופורציונלית משיש ואלון חם (4 סועדים)",
        eye: [27.55, 7.75, 11.95],
        look: [29.15, 5.55, 11.45]
      },
      sun_balcony: {
        title: "דירה C · מרפסת שמש מזרחית (200×500 ס\"מ) — פינת לאונג' ונוף לרחוב בעש\"ט",
        eye: [31.55, 7.75, 11.95],
        look: [29.80, 10.45, 11.75]
      },
      foyer_hallway: {
        title: "דירה C · מבואת כניסה ומסדרון חדרי השינה",
        eye: [25.35, 8.50, 11.95],
        look: [18.50, 8.50, 11.80]
      },
      master_suite: {
        title: "דירה C · סוויטת הורים יוקרתית (390×295 ס\"מ) — חלון דרומי גלוי ופרקט אלון",
        eye: [17.42, 8.20, 11.95],
        look: [15.95, 5.35, 11.45]
      },
      master_bath: {
        title: "דירה C · חדר רחצה הורים — מקלחון זכוכית וארון אלון מרחף",
        eye: [14.22, 6.75, 11.95],
        look: [12.95, 5.65, 11.40]
      },
      bedroom_south: {
        title: "דירה C · חדר שינה דרומי (345×270 ס\"מ) — מיטה מרופדת, ארון קיר ופינת עבודה",
        eye: [23.55, 7.55, 11.95],
        look: [25.15, 5.15, 11.40]
      },
      bedroom_mamad: {
        title: "דירה C · ממ\"ד / חדר שינה ועבודה (325×300 ס\"מ)",
        eye: [20.45, 7.45, 11.95],
        look: [22.15, 5.15, 11.40]
      },
      main_bath: {
        title: "דירה C · חדר רחצה כללי וחדר שירות — אמבטיה בנויה וחיפוי שיש קלקטה",
        eye: [18.45, 7.65, 11.95],
        look: [18.45, 6.45, 11.35]
      },
      // Apartment A Luxury Walkthrough Presets
      apta_living: {
        title: "דירה A · סלון מרכזי, קיר טלוויזיה 55\" ויציאה למרפסת שמש צפונית",
        eye: [...aptA_XY(4.65, 3.15), 11.95],
        look: [...aptA_XY(6.85, 4.85), 11.65]
      },
      apta_kitchen_dining: {
        title: "דירה A · מטבח יוקרתי, אי מפל שיש ופינת אוכל פרופורציונלית (4 סועדים)",
        eye: [...aptA_XY(5.35, 1.85), 11.95],
        look: [...aptA_XY(2.25, 4.25), 11.50]
      },
      apta_balcony: {
        title: "דירה A · מרפסת שמש צפונית — פינת לאונג' ומבט לרחוב פינס",
        eye: [...aptA_XY(5.85, 7.35), 11.95],
        look: [...aptA_XY(5.45, 3.65), 11.65]
      },
      apta_master: {
        title: "דירה A · סוויטת הורים יוקרתית (385×290 ס\"מ) — חלון צפוני חשוף במלואו",
        eye: [...aptA_XY(8.85, 3.45), 11.95],
        look: [...aptA_XY(9.75, 5.85), 11.50]
      },
      apta_mamad: {
        title: "דירה A · ממ\"ד / חדר שינה ועבודה (337×280 ס\"מ)",
        eye: [...aptA_XY(12.15, 2.15), 11.95],
        look: [...aptA_XY(14.35, 3.85), 11.45]
      },
      apta_east_bed: {
        title: "דירה A · חדר שינה מזרחי (340×280 ס\"מ) — מיטה, ארון קיר ופינת לימוד",
        eye: [...aptA_XY(12.15, 0.75), 11.95],
        look: [...aptA_XY(14.35, -0.75), 11.45]
      },
      // Apartment B (3 Rooms, 80+12 sqm, North-West) Walkthrough Presets
      aptb_living: {
        title: "דירה B (3 חד' · 80+12 מ\"ר) · סלון מרכזי, מטבח קשמיר ואי שיש קלקטה",
        eye: [...ptUV(6.25, 3.25), 11.95],
        look: [...ptUV(6.15, 0.80), 11.65]
      },
      aptb_balcony: {
        title: "דירה B · מרפסת שמש צפון-מערבית (12 מ\"ר) — פינת לאונג' ונוף לרחוב פינס",
        eye: [...ptUV(6.15, -1.15), 11.95],
        look: [...ptUV(6.15, 2.50), 11.65]
      },
      aptb_master: {
        title: "דירה B · סוויטת הורים מרווחת ופרקט אלון",
        eye: [...ptUV(2.65, 2.95), 11.95],
        look: [...ptUV(1.65, 1.35), 11.45]
      },
      // Penthouse Duplexes PB & PC (Floors 6-7) & Ground Floor Main Lobby
      pent_pb_terrace: {
        title: "פנטהאוז דופלקס מערבי PB (דירה 16 · קומות 6–7) — גג 113 מ\"ר, ג'קוזי ומטבח חוץ",
        eye: [16.95, 16.55, 21.30],
        look: [18.10, 19.25, 20.85]
      },
      pent_pc_terrace: {
        title: "פנטהאוז דופלקס מזרחי PC (דירה 17 · קומות 6–7) — גג 137 מ\"ר, ג'קוזי ופרגולה",
        eye: [24.20, 14.85, 21.30],
        look: [26.85, 19.15, 20.85]
      },
      lobby_main: {
        title: "לובי כניסה ראשי כפול (0.00) — דלפק קונסיירז' משיש קלקטה ופינת המתנה מעוצבת",
        eye: [21.20, 18.80, 1.64],
        look: [23.60, 16.40, 1.45]
      }
    };

    const FLOOR_Z_MAP = {
      0: 0.06,
      1: 4.25,
      2: 7.31,
      3: 10.37,
      4: 13.43,
      5: 16.49,
      6: 19.72,
      7: 22.95
    };
    let currentWalkEyeY = 11.95;

    const target = new THREE.Vector3(0, 12.5, 0);
    let spherical = { radius: 56, theta: 2.48, phi: 1.18 };
    let isDragging = false, dragButton = 0, prevMouse = { x: 0, y: 0 };

    function updateCameraFromFirstPerson() {
      perspCam.position.copy(fpEyePos);
      const cosP = Math.cos(fpPitch);
      const lookDir = new THREE.Vector3(
        -Math.sin(fpYaw) * cosP,
        Math.sin(fpPitch),
        -Math.cos(fpYaw) * cosP
      );
      target.copy(fpEyePos).add(lookDir);
      perspCam.lookAt(target);
    }

    function updateCameraFromSpherical() {
      if (isFirstPersonAptC) {
        updateCameraFromFirstPerson();
        return;
      }
      const sinPhi = Math.sin(spherical.phi);
      const x = target.x + spherical.radius * sinPhi * Math.sin(spherical.theta);
      const y = target.y + spherical.radius * Math.cos(spherical.phi);
      const z = target.z + spherical.radius * sinPhi * Math.cos(spherical.theta);
      perspCam.position.set(x, y, z);
      perspCam.lookAt(target);

      orthoCam.position.set(x, y, z);
      orthoCam.lookAt(target);
      const zoomScale = 48 / spherical.radius;
      orthoCam.zoom = zoomScale;
      orthoCam.updateProjectionMatrix();
    }

    function clampPositionToAptC(pos3D) {
      const cadX = pos3D.x + CX;
      const cadY = CY - pos3D.z;
      const clampedX = Math.max(4.15, Math.min(32.45, cadX));
      const clampedY = Math.max(4.25, Math.min(22.15, cadY));
      pos3D.x = clampedX - CX;
      pos3D.z = -(clampedY - CY);
      pos3D.y = currentWalkEyeY;
    }

    function clearLuxButtonsActive() {
      ['btn-enter-apta-fp', 'btn-enter-apta-dollhouse', 'btn-enter-aptb-fp', 'btn-enter-aptb-dollhouse',
       'btn-enter-aptc-fp', 'btn-enter-aptc-dollhouse', 'btn-enter-f3-both',
       'btn-side-apta-fp', 'btn-side-apta-doll', 'btn-side-aptc-fp', 'btn-side-aptc-doll'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.className = 'ui-btn ui-btn-lux';
      });
      document.querySelectorAll('.view-btn, .cut-btn').forEach(b => b.classList.remove('active'));
    }

    function flyToAptCRoom(roomKey, instant = false) {
      const r = APT_C_ROOMS[roomKey];
      if (!r) return;
      isFirstPersonAptC = true;
      isOrtho = false;
      activeCam = perspCam;
      perspCam.fov = 58;
      perspCam.updateProjectionMatrix();
      setClipHeight(29.5); // Keep ceiling & lighting intact in first-person walkthrough

      currentWalkEyeY = r.eye[2];
      document.getElementById('aptc-tour-hud').style.display = 'flex';
      document.getElementById('aptc-active-room-title').textContent = r.title;
      const badgeEl = document.getElementById('apt-active-badge');
      if (badgeEl) {
        if (roomKey.startsWith('pent_')) badgeEl.textContent = 'פנטהאוזים PB / PC · קומות 6–7 (+19.72)';
        else if (roomKey === 'lobby_main') badgeEl.textContent = 'לובי כניסה ראשי · קומת קרקע (0.00)';
        else badgeEl.textContent = 'דירות A / B / C · קומה 3 (+10.37)';
      }
      document.querySelectorAll('#aptc-room-buttons .room-chip').forEach(b => {
        b.className = (b.dataset.room === roomKey) ? 'room-chip active' : 'room-chip';
      });
      clearLuxButtonsActive();
      if (roomKey.startsWith('apta_')) {
        document.getElementById('btn-enter-apta-fp').className = 'ui-btn ui-btn-lux active';
        document.getElementById('btn-side-apta-fp').className = 'ui-btn ui-btn-lux active';
      } else if (roomKey.startsWith('aptb_')) {
        const bEl = document.getElementById('btn-enter-aptb-fp');
        if (bEl) bEl.className = 'ui-btn ui-btn-lux active';
      } else if (!roomKey.startsWith('pent_') && roomKey !== 'lobby_main') {
        document.getElementById('btn-enter-aptc-fp').className = 'ui-btn ui-btn-lux active';
        document.getElementById('btn-side-aptc-fp').className = 'ui-btn ui-btn-lux active';
      }

      const endPos = cadTo3D(r.eye[0], r.eye[1], r.eye[2]);
      const lookPos = cadTo3D(r.look[0], r.look[1], r.look[2]);
      const dir = new THREE.Vector3().subVectors(lookPos, endPos).normalize();
      const endYaw = Math.atan2(-dir.x, -dir.z);
      const endPitch = Math.asin(Math.max(-0.85, Math.min(0.85, dir.y)));

      if (instant) {
        fpEyePos.copy(endPos);
        fpYaw = endYaw;
        fpPitch = endPitch;
        fpAnim = null;
        updateCameraFromFirstPerson();
      } else {
        let dYaw = endYaw - fpYaw;
        while (dYaw > Math.PI) dYaw -= Math.PI * 2;
        while (dYaw < -Math.PI) dYaw += Math.PI * 2;
        fpAnim = {
          startPos: fpEyePos.clone(),
          endPos,
          startYaw: fpYaw,
          dYaw,
          startPitch: fpPitch,
          endPitch,
          t0: performance.now(),
          dur: 650
        };
      }
    }

    function enterAptCDollhouseMode() {
      isFirstPersonAptC = false;
      fpAnim = null;
      isOrtho = false;
      activeCam = perspCam;
      perspCam.fov = 42;
      perspCam.updateProjectionMatrix();

      setClipHeight(12.68);
      const centerC = cadTo3D(23.6, 7.8, 10.6);
      target.copy(centerC);
      spherical.radius = 16.5;
      spherical.theta = 2.62;
      spherical.phi = 0.64;
      updateCameraFromSpherical();

      document.getElementById('aptc-tour-hud').style.display = 'flex';
      document.getElementById('aptc-active-room-title').textContent = 'מבט-על תלת-ממדי יוקרתי (Dollhouse) — דירה C המלאה (4 חד\', 92+12 מ"ר)';
      clearLuxButtonsActive();
      document.getElementById('btn-enter-aptc-dollhouse').className = 'ui-btn ui-btn-lux active';
      document.getElementById('btn-side-aptc-doll').className = 'ui-btn ui-btn-lux active';
    }

    function enterAptADollhouseMode() {
      isFirstPersonAptC = false;
      fpAnim = null;
      isOrtho = false;
      activeCam = perspCam;
      perspCam.fov = 42;
      perspCam.updateProjectionMatrix();

      setClipHeight(12.68);
      const centerA = cadTo3D(23.2, 17.5, 10.6);
      target.copy(centerA);
      spherical.radius = 16.5;
      spherical.theta = 0.45;
      spherical.phi = 0.62;
      updateCameraFromSpherical();

      document.getElementById('aptc-tour-hud').style.display = 'flex';
      document.getElementById('aptc-active-room-title').textContent = 'מבט-על תלת-ממדי יוקרתי (Dollhouse) — דירה A המלאה (4 חד\', 94+12 מ"ר)';
      clearLuxButtonsActive();
      document.getElementById('btn-enter-apta-dollhouse').className = 'ui-btn ui-btn-lux active';
      document.getElementById('btn-side-apta-doll').className = 'ui-btn ui-btn-lux active';
    }

    function enterAptBDollhouseMode() {
      isFirstPersonAptC = false;
      fpAnim = null;
      isOrtho = false;
      activeCam = perspCam;
      perspCam.fov = 42;
      perspCam.updateProjectionMatrix();

      setClipHeight(12.68);
      const centerB = cadTo3D(9.2, 14.2, 10.6);
      target.copy(centerB);
      spherical.radius = 15.8;
      spherical.theta = -0.55;
      spherical.phi = 0.60;
      updateCameraFromSpherical();

      document.getElementById('aptc-tour-hud').style.display = 'flex';
      document.getElementById('aptc-active-room-title').textContent = 'מבט-על תלת-ממדי יוקרתי (Dollhouse) — דירה B המלאה (3 חד\', 80+12 מ"ר)';
      clearLuxButtonsActive();
      const bEl = document.getElementById('btn-enter-aptb-dollhouse');
      if (bEl) bEl.className = 'ui-btn ui-btn-lux active';
    }

    function enterPenthouseDollhouseMode(which = 'PB') {
      isFirstPersonAptC = false;
      fpAnim = null;
      isOrtho = false;
      activeCam = perspCam;
      perspCam.fov = 42;
      perspCam.updateProjectionMatrix();

      setClipHeight(22.35);
      const centerP = which === 'PB' ? cadTo3D(12.2, 14.8, 20.1) : cadTo3D(24.5, 11.8, 20.1);
      target.copy(centerP);
      spherical.radius = 19.5;
      spherical.theta = which === 'PB' ? -0.35 : 2.35;
      spherical.phi = 0.58;
      updateCameraFromSpherical();

      document.getElementById('aptc-tour-hud').style.display = 'flex';
      document.getElementById('aptc-active-room-title').textContent =
        which === 'PB'
          ? 'פנטהאוז דופלקס מערבי PB (דירה 16 · קומות 6–7) — 131 מ"ר + 113 מ"ר מרפסות גג וג\'קוזי'
          : 'פנטהאוז דופלקס מזרחי PC (דירה 17 · קומות 6–7) — 136 מ"ר + 137 מ"ר מרפסות גג וג\'קוזי';
      clearLuxButtonsActive();
    }

    function flyToBalconyFloorView(flrNum, aptType = 'A') {
      const zFlr = FLOOR_Z_MAP[flrNum] || 10.37;
      currentWalkEyeY = zFlr + 1.58;
      isFirstPersonAptC = true;
      isOrtho = false;
      activeCam = perspCam;
      perspCam.fov = 60;
      perspCam.updateProjectionMatrix();
      setClipHeight(29.5);

      let eyeXY, lookXY, labelTxt;
      if (flrNum >= 6) {
        eyeXY = aptType === 'B' ? [17.2, 18.8] : [26.8, 19.2];
        lookXY = aptType === 'B' ? [14.0, 29.5] : [34.5, 28.5];
        labelTxt = `נוף פנורמי ממרפסת הגג — קומה ${flrNum} (+${zFlr.toFixed(2)} מ')`;
      } else if (aptType === 'B') {
        eyeXY = ptUV(6.2, -1.1);
        lookXY = ptUV(6.2, -14.0);
        labelTxt = `נוף מהמרפסת הצפון-מערבית (דירה B${flrNum}) — קומה ${flrNum} (+${zFlr.toFixed(2)} מ')`;
      } else if (aptType === 'C') {
        eyeXY = [31.6, 9.5];
        lookXY = [44.0, 12.0];
        labelTxt = `נוף מהמרפסת המזרחית (דירה C${flrNum}) — קומה ${flrNum} (+${zFlr.toFixed(2)} מ')`;
      } else {
        eyeXY = ptUV(15.0, -1.1);
        lookXY = ptUV(16.5, -14.0);
        labelTxt = `נוף מהמרפסת הצפונית לצומת פינס/בעש"ט (דירה A${flrNum}) — קומה ${flrNum} (+${zFlr.toFixed(2)} מ')`;
      }

      document.getElementById('aptc-tour-hud').style.display = 'flex';
      document.getElementById('aptc-active-room-title').textContent = labelTxt;
      const badgeEl = document.getElementById('apt-active-badge');
      if (badgeEl) badgeEl.textContent = `קומה ${flrNum} (+${zFlr.toFixed(2)} מ')`;

      const tourSel = document.getElementById('tour-floor-select');
      if (tourSel) tourSel.value = String(flrNum);
      document.querySelectorAll('#balcony-floor-selector [data-bflr]').forEach(b => {
        b.className = (parseInt(b.dataset.bflr, 10) === flrNum) ? 'ui-btn active' : 'ui-btn';
      });

      const endPos = cadTo3D(eyeXY[0], eyeXY[1], currentWalkEyeY);
      const lookPos = cadTo3D(lookXY[0], lookXY[1], currentWalkEyeY - 0.35);
      const dir = new THREE.Vector3().subVectors(lookPos, endPos).normalize();
      fpEyePos.copy(endPos);
      fpYaw = Math.atan2(-dir.x, -dir.z);
      fpPitch = Math.asin(Math.max(-0.85, Math.min(0.85, dir.y)));
      fpAnim = null;
      updateCameraFromFirstPerson();
    }

    function closeAllDrawers() {
      document.querySelectorAll('.dropdown-drawer.open, .popover-drawer.open').forEach(d => d.classList.remove('open'));
      document.querySelectorAll('[data-drawer].open, [data-drawer].drawer-open').forEach(b => {
        b.classList.remove('open');
        b.classList.remove('drawer-open');
      });
    }

    function enterFloor3BothDollhouseMode(openTourHud = false) {
      isFirstPersonAptC = false;
      fpAnim = null;
      isOrtho = false;
      activeCam = perspCam;
      perspCam.fov = 42;
      perspCam.updateProjectionMatrix();

      setClipHeight(12.68);
      const centerAC = cadTo3D(19.5, 12.6, 10.6);
      target.copy(centerAC);
      spherical.radius = 25.5;
      spherical.theta = 2.15;
      spherical.phi = 0.56;
      updateCameraFromSpherical();

      document.getElementById('aptc-tour-hud').style.display = openTourHud ? 'flex' : 'none';
      document.getElementById('aptc-active-room-title').textContent = 'מבט-על תלת-ממדי יוקרתי (Dollhouse) — קומה 3 המלאה: דירות A + B + C';
      clearLuxButtonsActive();
      document.getElementById('btn-enter-f3-both').className = 'ui-btn ui-btn-lux active';
      const cutF3Btn = document.getElementById('btn-cut-f3-lux');
      if (cutF3Btn) {
        document.querySelectorAll('.cut-btn').forEach(b => b.className = 'cut-btn ui-btn');
        cutF3Btn.className = 'ui-btn ui-btn-lux active';
      }
      closeAllDrawers();
    }

    canvas.addEventListener('pointerdown', e => {
      closeAllDrawers();
      isDragging = true;
      dragButton = e.button;
      prevMouse = { x: e.clientX, y: e.clientY };
      canvas.setPointerCapture(e.pointerId);
    });

    canvas.addEventListener('pointermove', e => {
      if (!isDragging) return;
      const dx = e.clientX - prevMouse.x;
      const dy = e.clientY - prevMouse.y;
      prevMouse = { x: e.clientX, y: e.clientY };

      if (isFirstPersonAptC) {
        if (dragButton === 0 && !e.shiftKey) {
          fpYaw += dx * 0.0045;
          fpPitch = Math.max(-1.05, Math.min(0.95, fpPitch + dy * 0.0040));
          updateCameraFromFirstPerson();
        } else {
          // Right-drag or Shift-drag slides horizontally inside the room
          const fwd = new THREE.Vector3(-Math.sin(fpYaw), 0, -Math.cos(fpYaw));
          const right = new THREE.Vector3(Math.cos(fpYaw), 0, -Math.sin(fpYaw));
          fpEyePos.addScaledVector(right, -dx * 0.012);
          fpEyePos.addScaledVector(fwd, dy * 0.012);
          clampPositionToAptC(fpEyePos);
          updateCameraFromFirstPerson();
        }
        return;
      }

      if (dragButton === 0 && !e.shiftKey) {
        spherical.theta -= dx * 0.0075;
        spherical.phi = Math.max(0.05, Math.min(Math.PI * 0.49, spherical.phi - dy * 0.0065));
      } else {
        const forward = new THREE.Vector3().subVectors(target, activeCam.position).normalize();
        const right = new THREE.Vector3().crossVectors(forward, new THREE.Vector3(0, 1, 0)).normalize();
        const up = new THREE.Vector3().crossVectors(right, forward).normalize();
        const panSpeed = spherical.radius * 0.0012;
        target.addScaledVector(right, -dx * panSpeed);
        target.addScaledVector(up, dy * panSpeed);
      }
      updateCameraFromSpherical();
    });

    canvas.addEventListener('pointerup', e => {
      isDragging = false;
      try { canvas.releasePointerCapture(e.pointerId); } catch (_) {}
    });

    // Double-Click on Floor inside Apartment A, B, C or Penthouses to Smoothly Walk to that Point
    const raycaster = new THREE.Raycaster();
    const mouseNDC = new THREE.Vector2();
    canvas.addEventListener('dblclick', e => {
      const rect = canvas.getBoundingClientRect();
      mouseNDC.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouseNDC.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
      raycaster.setFromCamera(mouseNDC, activeCam);
      const hits = raycaster.intersectObjects(aptCFloorMeshes, false);
      if (hits.length > 0) {
        const pt = hits[0].point;
        currentWalkEyeY = pt.y + 1.56;
        const dest = new THREE.Vector3(pt.x, currentWalkEyeY, pt.z);
        clampPositionToAptC(dest);
        isFirstPersonAptC = true;
        perspCam.fov = 58;
        perspCam.updateProjectionMatrix();
        setClipHeight(29.5);
        fpAnim = {
          startPos: fpEyePos.clone(),
          endPos: dest,
          startYaw: fpYaw,
          dYaw: 0,
          startPitch: fpPitch,
          endPitch: fpPitch,
          t0: performance.now(),
          dur: 480
        };
      }
    });

    canvas.addEventListener('contextmenu', e => e.preventDefault());

    canvas.addEventListener('wheel', e => {
      e.preventDefault();
      if (isFirstPersonAptC) {
        // Wheel walks gently forward/backward along look direction in First-Person mode
        const step = -e.deltaY * 0.0032;
        const fwd = new THREE.Vector3(-Math.sin(fpYaw), 0, -Math.cos(fpYaw));
        fpEyePos.addScaledVector(fwd, step);
        clampPositionToAptC(fpEyePos);
        updateCameraFromFirstPerson();
        return;
      }
      spherical.radius = Math.max(6, Math.min(2600, spherical.radius * (1 + e.deltaY * 0.001)));
      updateCameraFromSpherical();
    }, { passive: false });

    // Multi-Touch Pinch-to-Zoom for Tablet / iPad / Mobile Sales Presentations
    let lastTouchDist = null;
    canvas.addEventListener('touchstart', e => {
      if (e.touches.length === 2) {
        const dx = e.touches[0].clientX - e.touches[1].clientX;
        const dy = e.touches[0].clientY - e.touches[1].clientY;
        lastTouchDist = Math.hypot(dx, dy);
      }
    }, { passive: true });
    canvas.addEventListener('touchmove', e => {
      if (e.touches.length === 2 && lastTouchDist !== null) {
        const dx = e.touches[0].clientX - e.touches[1].clientX;
        const dy = e.touches[0].clientY - e.touches[1].clientY;
        const dist = Math.hypot(dx, dy);
        if (dist > 5 && !isFirstPersonAptC) {
          const ratio = lastTouchDist / dist;
          spherical.radius = Math.max(6, Math.min(2600, spherical.radius * ratio));
          updateCameraFromSpherical();
        }
        lastTouchDist = dist;
      }
    }, { passive: true });
    canvas.addEventListener('touchend', () => { lastTouchDist = null; }, { passive: true });

    // Keyboard WASD & Arrow Key Continuous Movement inside Apartment A, B, C & Penthouses
    const keysDown = {};
    window.addEventListener('keydown', e => {
      keysDown[e.code] = true;
      if (e.code === 'Escape') closeAllDrawers();
    });
    window.addEventListener('keyup', e => {
      keysDown[e.code] = false;
    });

    function stepWalkMovement(moveType, dt = 0.016) {
      if (!isFirstPersonAptC) {
        isFirstPersonAptC = true;
        perspCam.fov = 58;
        perspCam.updateProjectionMatrix();
        setClipHeight(29.5);
      }
      const speed = 3.2 * dt;
      const fwd = new THREE.Vector3(-Math.sin(fpYaw), 0, -Math.cos(fpYaw));
      const right = new THREE.Vector3(Math.cos(fpYaw), 0, -Math.sin(fpYaw));
      if (moveType === 'fwd')   fpEyePos.addScaledVector(fwd, speed);
      if (moveType === 'back')  fpEyePos.addScaledVector(fwd, -speed);
      if (moveType === 'left')  fpEyePos.addScaledVector(right, -speed);
      if (moveType === 'right') fpEyePos.addScaledVector(right, speed);
      if (moveType === 'turnL') fpYaw += 1.6 * dt;
      if (moveType === 'turnR') fpYaw -= 1.6 * dt;
      clampPositionToAptC(fpEyePos);
      updateCameraFromFirstPerson();
    }

    // Wire On-Demand Top Bar Popover Drawers
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

    // Wire Bottom-Right Section Panel Collapse / Expand & Luxury Floor 3 Cut Button
    const sectionsPanel = document.getElementById('sections-panel');
    const btnToggleSections = document.getElementById('btn-toggle-sections-body');
    if (btnToggleSections && sectionsPanel) {
      btnToggleSections.addEventListener('click', () => {
        const isCollapsed = sectionsPanel.classList.toggle('collapsed');
        btnToggleSections.textContent = isCollapsed ? '+ פתח חתכים' : '▾';
      });
    }
    const btnCutF3Lux = document.getElementById('btn-cut-f3-lux');
    if (btnCutF3Lux) {
      btnCutF3Lux.addEventListener('click', () => enterFloor3BothDollhouseMode(false));
    }

    const btnCloseTourHud = document.getElementById('btn-close-tour-hud');
    if (btnCloseTourHud) {
      btnCloseTourHud.addEventListener('click', () => {
        document.getElementById('aptc-tour-hud').style.display = 'none';
      });
    }

    // Wire On-Screen D-Pad Buttons (hold or click)
    let activeDpadInterval = null;
    document.querySelectorAll('.walk-dpad-btn').forEach(btn => {
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

    // Wire Apartment A, B, C, Penthouses & Lobby Room Teleport Chips & Mode Buttons
    document.querySelectorAll('#aptc-room-buttons .room-chip').forEach(btn => {
      btn.addEventListener('click', () => {
        flyToAptCRoom(btn.dataset.room, false);
        closeAllDrawers();
      });
    });
    document.getElementById('btn-enter-aptc-fp').addEventListener('click', () => { flyToAptCRoom('living_main', false); closeAllDrawers(); });
    document.getElementById('btn-side-aptc-fp').addEventListener('click', () => { flyToAptCRoom('living_main', false); closeAllDrawers(); });
    document.getElementById('btn-enter-aptc-dollhouse').addEventListener('click', () => { enterAptCDollhouseMode(); closeAllDrawers(); });
    document.getElementById('btn-side-aptc-doll').addEventListener('click', () => { enterAptCDollhouseMode(); closeAllDrawers(); });
    document.getElementById('btn-enter-apta-fp').addEventListener('click', () => { flyToAptCRoom('apta_living', false); closeAllDrawers(); });
    document.getElementById('btn-side-apta-fp').addEventListener('click', () => { flyToAptCRoom('apta_living', false); closeAllDrawers(); });
    document.getElementById('btn-enter-apta-dollhouse').addEventListener('click', () => { enterAptADollhouseMode(); closeAllDrawers(); });
    document.getElementById('btn-side-apta-doll').addEventListener('click', () => { enterAptADollhouseMode(); closeAllDrawers(); });
    const btnEnterAptBFp = document.getElementById('btn-enter-aptb-fp');
    if (btnEnterAptBFp) btnEnterAptBFp.addEventListener('click', () => { flyToAptCRoom('aptb_living', false); closeAllDrawers(); });
    const btnEnterAptBDoll = document.getElementById('btn-enter-aptb-dollhouse');
    if (btnEnterAptBDoll) btnEnterAptBDoll.addEventListener('click', () => { enterAptBDollhouseMode(); closeAllDrawers(); });
    const btnEnterPentPB = document.getElementById('btn-enter-pent-pb');
    if (btnEnterPentPB) btnEnterPentPB.addEventListener('click', () => { enterPenthouseDollhouseMode('PB'); closeAllDrawers(); });
    const btnEnterPentPC = document.getElementById('btn-enter-pent-pc');
    if (btnEnterPentPC) btnEnterPentPC.addEventListener('click', () => { enterPenthouseDollhouseMode('PC'); closeAllDrawers(); });
    const btnEnterLobbyFp = document.getElementById('btn-enter-lobby-fp');
    if (btnEnterLobbyFp) btnEnterLobbyFp.addEventListener('click', () => { flyToAptCRoom('lobby_main', false); closeAllDrawers(); });
    document.getElementById('btn-enter-f3-both').addEventListener('click', () => enterFloor3BothDollhouseMode(true));

    // Wire Multi-Floor Balcony View Simulator (Floors 1-7) & Tour HUD Floor Selector
    document.querySelectorAll('#balcony-floor-selector [data-bflr]').forEach(btn => {
      btn.addEventListener('click', () => {
        const flr = parseInt(btn.dataset.bflr, 10);
        flyToBalconyFloorView(flr, 'A');
        closeAllDrawers();
      });
    });
    const tourFloorSelect = document.getElementById('tour-floor-select');
    if (tourFloorSelect) {
      tourFloorSelect.addEventListener('change', () => {
        const flr = parseInt(tourFloorSelect.value, 10);
        flyToBalconyFloorView(flr, 'A');
      });
    }

    // =========================================================================
    // UI EVENT WIRING (VIEWS, FLOOR CUTS, ORTHO, CLIPPING, FLOORS, MATERIALS)
    // =========================================================================
    const VIEW_PRESETS = {
      iso_ne:         { theta: 2.48,   phi: 1.18, radius: 56,   target: [0, 12.5, 0], ortho: false, clip: 29.5 },
      gmaps_regional: { theta: 2.38,   phi: 0.56, radius: 1550, target: [0, 8.0, 0],  ortho: false, clip: 29.5 },
      gmaps_aerial:   { theta: 2.38,   phi: 0.62, radius: 680,  target: [0, 6.0, 0],  ortho: false, clip: 29.5 },
      gmaps_close:    { theta: 2.38,   phi: 0.68, radius: 220,  target: [0, 8.0, 0],  ortho: false, clip: 29.5 },
      cut_basement:   { theta: 2.55,   phi: 0.54, radius: 36,   target: [0.0, -2.0, 0.0], ortho: false, clip: -0.25 },
      cut_ground:     { theta: 2.65,   phi: 0.62, radius: 38,   target: [0.5, 1.5, -0.5], ortho: false, clip: 2.30 },
      cut_f1_5:       { theta: 2.75,   phi: 0.58, radius: 38,   target: [0.8, 5.0, -0.5], ortho: false, clip: 5.95 },
      cut_f6:         { theta: 2.70,   phi: 0.58, radius: 38,   target: [0.8, 20.2, -0.5], ortho: false, clip: 21.45 },
      cut_f7:         { theta: 2.70,   phi: 0.58, radius: 36,   target: [0.5, 23.2, 0.5], ortho: false, clip: 24.35 },
      top_plan_f1_5:  { theta: 0.0,    phi: 0.02, radius: 42,   target: [0.8, 4.5, -0.5], ortho: true,  clip: 5.95 },
      north:          { theta: -2.933, phi: Math.PI / 2 - 0.01, radius: 52, target: [0, 13.5, 0], ortho: true, clip: 29.5 },
      east:           { theta: Math.PI / 2, phi: Math.PI / 2 - 0.01, radius: 52, target: [0, 13.5, 0], ortho: true, clip: 29.5 },
      south:          { theta: 0.0,    phi: Math.PI / 2 - 0.01, radius: 52, target: [0, 13.5, 0], ortho: true, clip: 29.5 },
      west:           { theta: -1.363, phi: Math.PI / 2 - 0.01, radius: 52, target: [0, 13.5, 0], ortho: true, clip: 29.5 }
    };

    const clipSlider = document.getElementById('clip-slider');
    const clipVal = document.getElementById('clip-val');

    function setClipHeight(v) {
      clipSlider.value = v;
      clipPlane.constant = v;
      clipVal.textContent = v >= 29.2 ? '+29.50 מ\' (מלא)' : `+${v.toFixed(2)} מ' (חתך פנים)`;
    }

    function setOrthoMode(useOrtho) {
      isOrtho = useOrtho;
      activeCam = isOrtho ? orthoCam : perspCam;
      document.getElementById('proj-badge').textContent = isOrtho ? 'אורתוגרפי 1:50' : 'פרספקטיבה';
      const btn = document.getElementById('btn-ortho');
      btn.className = isOrtho ? 'ui-btn active' : 'ui-btn';
      updateCameraFromSpherical();
    }

    function activatePreset(viewKey) {
      const p = VIEW_PRESETS[viewKey];
      if (!p) return;
      isFirstPersonAptC = false;
      fpAnim = null;
      perspCam.fov = 40;
      perspCam.updateProjectionMatrix();
      document.getElementById('aptc-tour-hud').style.display = 'none';
      clearLuxButtonsActive();
      const cutF3Btn = document.getElementById('btn-cut-f3-lux');
      if (cutF3Btn) cutF3Btn.className = 'ui-btn ui-btn-lux';
      spherical.theta = p.theta;
      spherical.phi = p.phi;
      spherical.radius = p.radius;
      target.set(p.target[0], p.target[1], p.target[2]);
      if (typeof p.clip === 'number') {
        setClipHeight(p.clip);
      }
      setOrthoMode(p.ortho);
      closeAllDrawers();
    }

    document.querySelectorAll('.view-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.view-btn').forEach(b => b.className = 'view-btn ui-btn');
        document.querySelectorAll('.cut-btn').forEach(b => b.className = 'cut-btn ui-btn');
        btn.className = 'view-btn ui-btn active';
        activatePreset(btn.dataset.view);
      });
    });

    document.querySelectorAll('.cut-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.cut-btn').forEach(b => b.className = 'cut-btn ui-btn');
        document.querySelectorAll('.view-btn').forEach(b => b.className = 'view-btn ui-btn');
        btn.className = 'cut-btn ui-btn active';
        activatePreset(btn.dataset.view);
      });
    });

    // Wire 3D GIS Distance Radii & POI Locations Toggles
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
      if (!gisPoisVisible) {
        gisActiveCard.style.display = 'none';
      }
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

    document.getElementById('btn-top-radii').addEventListener('click', () => {
      gisRadiiVisible = !gisRadiiVisible;
      syncGisRadiiState();
    });
    document.getElementById('btn-side-radii').addEventListener('click', () => {
      gisRadiiVisible = !gisRadiiVisible;
      syncGisRadiiState();
    });

    document.getElementById('btn-top-pois').addEventListener('click', () => {
      gisPoisVisible = !gisPoisVisible;
      syncGisPoisState();
    });
    document.getElementById('btn-side-pois').addEventListener('click', () => {
      gisPoisVisible = !gisPoisVisible;
      syncGisPoisState();
    });

    const btnGisRegional = document.getElementById('btn-side-gis-regional');
    if (btnGisRegional) {
      btnGisRegional.addEventListener('click', () => {
        activatePreset('gmaps_regional');
      });
    }
    document.getElementById('btn-side-gis-overview').addEventListener('click', () => {
      activatePreset('gmaps_aerial');
    });
    document.getElementById('btn-side-gis-close').addEventListener('click', () => {
      activatePreset('gmaps_close');
    });

    document.querySelectorAll('#gis-cat-buttons .gis-cat-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        activeGisCategory = chip.dataset.gcat;
        document.querySelectorAll('#gis-cat-buttons .gis-cat-chip').forEach(c => {
          c.className = (c === chip) ? 'gis-cat-chip ui-btn active' : 'gis-cat-chip ui-btn';
        });
        if (!gisPoisVisible) {
          gisPoisVisible = true;
        }
        syncGisPoisState();
      });
    });

    let gmapsVisible = true;
    document.getElementById('btn-gmaps').addEventListener('click', function() {
      gmapsVisible = !gmapsVisible;
      googleMapsPlaneMesh.visible = gmapsVisible;
      wideGoogleMapsMesh.visible = gmapsVisible;
      closeupGoogleMapsMesh.visible = gmapsVisible;
      this.textContent = gmapsVisible
        ? 'מפת Google Maps (פינס פינת בעש"ט): פעיל'
        : 'מפת Google Maps (פינס פינת בעש"ט): כבוי';
      this.className = gmapsVisible ? 'ui-btn active' : 'ui-btn';
    });

    document.getElementById('btn-ortho').addEventListener('click', () => setOrthoMode(!isOrtho));

    let cadPlanVisible = true;
    document.getElementById('btn-cad-plan').addEventListener('click', function() {
      cadPlanVisible = !cadPlanVisible;
      cadPlanLineMeshes.forEach(l => l.visible = cadPlanVisible);
      this.textContent = cadPlanVisible ? 'שרטוט פנים CAD: פעיל' : 'שרטוט פנים CAD: כבוי';
      this.className = cadPlanVisible ? 'ui-btn active' : 'ui-btn';
    });

    let edgesVisible = true;
    document.getElementById('btn-edges').addEventListener('click', function() {
      edgesVisible = !edgesVisible;
      edgeLines.forEach(l => l.visible = edgesVisible);
      this.textContent = edgesVisible ? 'קווי מתאר 3D: פעיל' : 'קווי מתאר 3D: כבוי';
      this.className = edgesVisible ? 'ui-btn active' : 'ui-btn';
    });

    document.getElementById('btn-labels').addEventListener('click', function() {
      showLabels = !showLabels;
      labelsContainer.style.display = showLabels ? 'block' : 'none';
      this.textContent = showLabels ? 'תוויות חדרים: פעיל' : 'תוויות חדרים: כבוי';
      this.className = showLabels ? 'ui-btn active' : 'ui-btn';
    });

    clipSlider.addEventListener('input', () => {
      setClipHeight(parseFloat(clipSlider.value));
    });

    // Layer Checkboxes
    document.querySelectorAll('#layer-toggles input[type="checkbox"]').forEach(cb => {
      cb.addEventListener('change', () => {
        const grp = layerGroups[cb.dataset.layer];
        if (grp) grp.visible = cb.checked;
      });
    });
    document.getElementById('btn-all-floors').addEventListener('click', () => {
      document.querySelectorAll('#layer-toggles input[type="checkbox"]').forEach(cb => {
        cb.checked = true;
        if (layerGroups[cb.dataset.layer]) layerGroups[cb.dataset.layer].visible = true;
      });
      setClipHeight(29.5);
    });

    // Interactive Material Legend Highlight
    let activeMatFilter = null;
    function applyMaterialHighlight(matKey) {
      activeMatFilter = matKey;
      allMeshes.forEach(m => {
        if (!matKey) {
          m.material = matDefs[m.userData.matKey];
        } else if (m.userData.matKey === matKey) {
          m.material = matDefs[m.userData.matKey];
        } else {
          if (!m.userData.ghostMat) {
            m.userData.ghostMat = matDefs[m.userData.matKey].clone();
            m.userData.ghostMat.transparent = true;
            m.userData.ghostMat.opacity = 0.12;
          }
          m.material = m.userData.ghostMat;
        }
      });
      document.querySelectorAll('.mat-btn').forEach(b => {
        const isSel = b.dataset.mat === matKey;
        b.style.borderColor = isSel ? '#3b82f6' : '';
        b.style.boxShadow = isSel ? '0 0 0 1px #3b82f6' : '';
      });
    }

    document.querySelectorAll('.mat-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const mk = btn.dataset.mat;
        applyMaterialHighlight(activeMatFilter === mk ? null : mk);
      });
    });
    document.getElementById('btn-reset-mat').addEventListener('click', () => applyMaterialHighlight(null));

    // Sun Angle Slider
    const sunSlider = document.getElementById('sun-slider');
    const sunVal = document.getElementById('sun-val');
    sunSlider.addEventListener('input', () => {
      const deg = parseFloat(sunSlider.value);
      const rad = deg * Math.PI / 180;
      sunLight.position.set(48 * Math.cos(rad), 46 * Math.sin(rad) + 12, 32 * Math.sin(rad * 1.3));
      const hour = Math.round(7 + (deg / 180) * 11);
      sunVal.textContent = `~${hour}:00`;
    });

    // One-Click Wavefront .OBJ Exporter
    document.getElementById('btn-export-obj').addEventListener('click', () => {
      let obj = "# Pines 48, Petah Tikva - 1:50 Architectural Exterior + Interior 3D Model\n";
      let vOffset = 1;
      allMeshes.forEach((mesh, idx) => {
        if (!mesh.visible || !layerGroups[mesh.userData.layer].visible) return;
        const geom = mesh.geometry;
        const pos = geom.attributes.position;
        obj += `o mesh_${idx}_${mesh.userData.matKey}\n`;
        for (let i = 0; i < pos.count; i++) {
          obj += `v ${pos.getX(i).toFixed(4)} ${pos.getY(i).toFixed(4)} ${pos.getZ(i).toFixed(4)}\n`;
        }
        if (geom.index) {
          const index = geom.index;
          for (let i = 0; i < index.count; i += 3) {
            const a = index.getX(i) + vOffset;
            const b = index.getX(i + 1) + vOffset;
            const c = index.getX(i + 2) + vOffset;
            obj += `f ${a} ${b} ${c}\n`;
          }
        } else {
          for (let i = 0; i < pos.count; i += 3) {
            obj += `f ${vOffset + i} ${vOffset + i + 1} ${vOffset + i + 2}\n`;
          }
        }
        vOffset += pos.count;
      });
      const blob = new Blob([obj], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'pines48_petah_tikva_full_3d.obj';
      a.click();
      URL.revokeObjectURL(url);
    });

    // =========================================================================
    // PHASE 1 & 2: 17-UNIT 3D CATALOG & LIVE CRM, PDF OFFER GENERATOR,
    // 4 INTERIOR FINISH PACKAGES, NIGHT MODE & 3D LASER TAPE MEASURE
    // =========================================================================
    const PINES48_UNITS = [
      { num: 1,  code: "B1", type: "B",  floor: 1, zFlr: 4.25,  zCeil: 6.92,  rooms: 3, area: 80,  balcony: 12,  dirs: "צפון, מערב",       price: 2280000, status: "owner",     statusLabel: "דירת בעלים",         parking: 1  },
      { num: 2,  code: "A1", type: "A",  floor: 1, zFlr: 4.25,  zCeil: 6.92,  rooms: 4, area: 94,  balcony: 12,  dirs: "צפון, מזרח",       price: 2566000, status: "owner",     statusLabel: "דירת בעלים",         parking: 2  },
      { num: 3,  code: "C1", type: "C",  floor: 1, zFlr: 4.25,  zCeil: 6.92,  rooms: 4, area: 92,  balcony: 12,  dirs: "דרום, מזרח",       price: 2512000, status: "owner",     statusLabel: "דירת בעלים",         parking: 3  },
      { num: 4,  code: "B2", type: "B",  floor: 2, zFlr: 7.31,  zCeil: 9.98,  rooms: 3, area: 80,  balcony: 12,  dirs: "צפון, מערב",       price: 2305000, status: "available", statusLabel: "פנויה · קולסקי",     parking: 4  },
      { num: 5,  code: "A2", type: "A",  floor: 2, zFlr: 7.31,  zCeil: 9.98,  rooms: 4, area: 94,  balcony: 12,  dirs: "צפון, מזרח",       price: 2591000, status: "owner",     statusLabel: "דירת בעלים",         parking: 5  },
      { num: 6,  code: "C2", type: "C",  floor: 2, zFlr: 7.31,  zCeil: 9.98,  rooms: 4, area: 92,  balcony: 12,  dirs: "דרום, מזרח",       price: 2537000, status: "owner",     statusLabel: "דירת בעלים",         parking: 6  },
      { num: 7,  code: "B3", type: "B",  floor: 3, zFlr: 10.37, zCeil: 13.04, rooms: 3, area: 80,  balcony: 12,  dirs: "צפון, מערב",       price: 2330000, status: "available", statusLabel: "פנויה · קולסקי",     parking: 7  },
      { num: 8,  code: "A3", type: "A",  floor: 3, zFlr: 10.37, zCeil: 13.04, rooms: 4, area: 94,  balcony: 12,  dirs: "צפון, מזרח",       price: 2616000, status: "shared",    statusLabel: "משותפת · קולסקי",    parking: 8  },
      { num: 9,  code: "C3", type: "C",  floor: 3, zFlr: 10.37, zCeil: 13.04, rooms: 4, area: 92,  balcony: 12,  dirs: "דרום, מזרח",       price: 2562000, status: "available", statusLabel: "פנויה · קולסקי",     parking: 9  },
      { num: 10, code: "B4", type: "B",  floor: 4, zFlr: 13.43, zCeil: 16.10, rooms: 3, area: 80,  balcony: 12,  dirs: "צפון, מערב",       price: 2355000, status: "available", statusLabel: "פנויה · קולסקי",     parking: 10 },
      { num: 11, code: "A4", type: "A",  floor: 4, zFlr: 13.43, zCeil: 16.10, rooms: 4, area: 94,  balcony: 12,  dirs: "צפון, מזרח",       price: 2641000, status: "available", statusLabel: "פנויה · קולסקי",     parking: 11 },
      { num: 12, code: "C4", type: "C",  floor: 4, zFlr: 13.43, zCeil: 16.10, rooms: 4, area: 92,  balcony: 12,  dirs: "דרום, מזרח",       price: 2587000, status: "shared",    statusLabel: "משותפת · קולסקי",    parking: 12 },
      { num: 13, code: "B5", type: "B",  floor: 5, zFlr: 16.49, zCeil: 19.16, rooms: 3, area: 80,  balcony: 12,  dirs: "צפון, מערב",       price: 2380000, status: "available", statusLabel: "פנויה · קולסקי",     parking: 13 },
      { num: 14, code: "A5", type: "A",  floor: 5, zFlr: 16.49, zCeil: 19.16, rooms: 4, area: 94,  balcony: 12,  dirs: "צפון, מזרח",       price: 2666000, status: "available", statusLabel: "פנויה · קולסקי",     parking: 14 },
      { num: 15, code: "C5", type: "C",  floor: 5, zFlr: 16.49, zCeil: 19.16, rooms: 4, area: 92,  balcony: 12,  dirs: "דרום, מזרח",       price: 2612000, status: "available", statusLabel: "פנויה · קולסקי",     parking: 15 },
      { num: 16, code: "PB", type: "PB", floor: 6, zFlr: 19.72, zCeil: 25.53, rooms: 5, area: 131, balcony: 113, dirs: "צפון, מערב, דרום", price: 3795000, status: "available", statusLabel: "פנטהאוז דופלקס זמין", parking: 16 },
      { num: 17, code: "PC", type: "PC", floor: 6, zFlr: 19.72, zCeil: 25.53, rooms: 5, area: 136, balcony: 137, dirs: "צפון, מזרח, דרום", price: 4075000, status: "available", statusLabel: "פנטהאוז דופלקס זמין", parking: 17 }
    ];

    const UNIT_POLYS = {
      B:  [[4.56, 16.76], [13.50, 18.65], [12.40, 11.20], [12.40, 6.52], [6.57, 5.29], [4.05, 17.27]],
      A:  [[13.50, 18.65], [21.10, 20.25], [26.99, 22.11], [29.12, 20.72], [30.73, 13.13], [30.35, 12.15], [18.80, 12.15]],
      C:  [[18.80, 12.15], [30.35, 12.15], [30.35, 4.20], [22.85, 4.20], [22.85, 4.10], [17.25, 4.10], [17.25, 4.95], [12.40, 4.95], [12.40, 11.20]],
      PB: [[4.05, 17.27], [15.50, 19.68], [16.33, 15.72], [18.20, 15.80], [18.20, 5.85], [12.40, 4.95], [6.57, 5.29]],
      PC: [[18.20, 15.80], [21.98, 14.15], [30.35, 14.15], [30.35, 4.20], [22.85, 4.20], [18.20, 4.20]]
    };

    const UNIT_BADGE_ANCHORS = {
      B:  [6.8,  15.5],
      A:  [23.5, 20.5],
      C:  [28.5, 6.8],
      PB: [10.5, 16.8],
      PC: [25.5, 13.8]
    };

    const units3DGroup = new THREE.Group();
    units3DGroup.visible = false;
    scene.add(units3DGroup);

    const unitsLabelsContainer = document.getElementById('units-labels-container');
    const unitSalesCard = document.getElementById('unit-sales-card');
    const unitVolumeMeshes = [];
    const unitBadgeObjs = [];
    let units3DVisible = false;
    let showUnitPrices = true;
    let activeUnitStatusFilter = 'all';
    let activeUnitRoomFilter = 'all';
    let selectedUnitObj = null;

    function formatILS(n) {
      return '₪' + n.toLocaleString('he-IL');
    }

    function getUnitStatusColorHex(status) {
      if (status === 'available') return 0x10b981;
      if (status === 'shared')    return 0xf59e0b;
      return 0x64748b;
    }

    // Build 3D Volumes & Floating Badges for all 17 Units
    PINES48_UNITS.forEach(u => {
      const poly = UNIT_POLYS[u.type];
      if (!poly) return;
      const shape = new THREE.Shape();
      shape.moveTo(poly[0][0] - CX, poly[0][1] - CY);
      for (let i = 1; i < poly.length; i++) {
        shape.lineTo(poly[i][0] - CX, poly[i][1] - CY);
      }
      shape.closePath();

      const depth = (u.zCeil - u.zFlr) - 0.18;
      const geom = new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled: false });
      geom.rotateX(-Math.PI / 2);
      geom.translate(0, u.zFlr + 0.08, 0);

      const colHex = getUnitStatusColorHex(u.status);
      const mat = new THREE.MeshBasicMaterial({
        color: colHex,
        transparent: true,
        opacity: u.status === 'owner' ? 0.18 : 0.34,
        side: THREE.DoubleSide,
        depthWrite: false
      });
      const mesh = new THREE.Mesh(geom, mat);
      mesh.userData = { unit: u, baseOpacity: mat.opacity };
      units3DGroup.add(mesh);
      unitVolumeMeshes.push(mesh);

      const edges = new THREE.EdgesGeometry(geom, 25);
      const lineMat = new THREE.LineBasicMaterial({ color: colHex, transparent: true, opacity: 0.85 });
      const line = new THREE.LineSegments(edges, lineMat);
      mesh.add(line);

      // Floating HTML Badge on Facade
      const [ax, ay] = UNIT_BADGE_ANCHORS[u.type] || [20, 15];
      const pos3D = cadTo3D(ax, ay, u.zFlr + 1.45);
      const badge = document.createElement('div');
      badge.style.cssText = 'position:absolute;transform:translate(-50%,-50%);pointer-events:auto;cursor:pointer;padding:3px 8px;border-radius:999px;font-size:10px;font-weight:800;color:#ffffff;box-shadow:0 4px 12px rgba(0,0,0,0.35);white-space:nowrap;display:none;align-items:center;gap:5px;border:1.5px solid #ffffff;transition:transform 0.12s ease;';
      badge.style.background = u.status === 'available' ? '#059669' : (u.status === 'shared' ? '#d97706' : '#475569');
      badge.innerHTML = `<span>דירה ${u.num} (${u.code})</span><span class="ubadge-price">${showUnitPrices && u.status !== 'owner' ? '· ' + formatILS(u.price) : ''}</span>`;
      badge.addEventListener('click', e => {
        e.stopPropagation();
        selectUnitAndOpenCard(u);
      });
      unitsLabelsContainer.appendChild(badge);
      unitBadgeObjs.push({ unit: u, mesh, el: badge, pos: pos3D });
    });

    function unitMatchesFilters(u) {
      if (activeUnitStatusFilter === 'kuleski' && u.status === 'owner') return false;
      if (activeUnitStatusFilter === 'available' && u.status !== 'available') return false;
      if (activeUnitStatusFilter === 'owner' && u.status !== 'owner') return false;
      if (activeUnitRoomFilter !== 'all' && String(u.rooms) !== activeUnitRoomFilter) return false;
      return true;
    }

    function renderUnitsCatalogList() {
      const listEl = document.getElementById('units-catalog-list');
      if (!listEl) return;
      listEl.innerHTML = '';

      PINES48_UNITS.forEach(u => {
        const match = unitMatchesFilters(u);
        const itemObj = unitBadgeObjs.find(b => b.unit.num === u.num);
        if (itemObj) {
          itemObj.mesh.visible = match;
          const prSpan = itemObj.el.querySelector('.ubadge-price');
          if (prSpan) {
            prSpan.textContent = (showUnitPrices && u.status !== 'owner') ? `· ${formatILS(u.price)}` : '';
          }
        }
        if (!match) return;

        const row = document.createElement('div');
        const isSel = selectedUnitObj && selectedUnitObj.num === u.num;
        row.style.cssText = `display:flex;align-items:center;justify-content:space-between;padding:7px 9px;border-radius:10px;border:1px solid ${isSel ? '#059669' : '#e2e8f0'};background:${isSel ? '#ecfdf5' : '#ffffff'};cursor:pointer;transition:all 0.12s ease;`;
        const badgeCls = u.status === 'available' ? 'status-available' : (u.status === 'shared' ? 'status-shared' : 'status-owner');
        const priceHtml = (showUnitPrices && u.status !== 'owner')
          ? `<div style="font-size:12px;font-weight:900;color:#0f172a;">${formatILS(u.price)}</div>`
          : `<div style="font-size:11px;font-weight:700;color:#64748b;">${u.status === 'owner' ? 'בעלים' : 'לפרטים'}</div>`;

        row.innerHTML = `
          <div style="display:flex;align-items:center;gap:8px;">
            <div style="width:32px;height:32px;border-radius:8px;background:#0f172a;color:#fde047;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:900;font-size:11px;line-height:1.05;">
              <span>#${u.num}</span>
              <span style="font-size:9px;color:#93c5fd;">${u.code}</span>
            </div>
            <div>
              <div style="display:flex;align-items:center;gap:5px;">
                <span style="font-size:12px;font-weight:800;color:#0f172a;">קומה ${u.floor}${u.type.startsWith('P') ? '–7 דופלקס' : ''} · ${u.rooms} חד'</span>
                <span class="status-badge ${badgeCls}">${u.statusLabel}</span>
              </div>
              <div style="font-size:10px;color:#475569;font-weight:600;">${u.area} מ"ר פנים + ${u.balcony} מ"ר מרפסת · כיוונים: ${u.dirs}</div>
            </div>
          </div>
          <div style="text-align:left;">
            ${priceHtml}
            <div style="font-size:9px;color:#059669;font-weight:800;">כרטיס + PDF ◂</div>
          </div>
        `;
        row.addEventListener('click', () => {
          selectUnitAndOpenCard(u);
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
        drwBtn.textContent = units3DVisible ? '🏢 סימון דירות 3D: פעיל' : '🏢 הדגש דירות 3D על הבניין';
      }
      if (!units3DVisible) {
        unitBadgeObjs.forEach(b => { b.el.style.display = 'none'; });
      }
    }

    function selectUnitAndOpenCard(u) {
      selectedUnitObj = u;
      unitVolumeMeshes.forEach(m => {
        const isTarget = m.userData.unit.num === u.num;
        m.material.opacity = isTarget ? 0.62 : m.userData.baseOpacity * 0.55;
      });
      renderUnitsCatalogList();

      const badgeCls = u.status === 'available' ? 'status-available' : (u.status === 'shared' ? 'status-shared' : 'status-owner');
      const downPayment20 = Math.round(u.price * 0.20);
      const balance80 = u.price - downPayment20;
      const estMonthlyMortgage = Math.round((u.price * 0.60) * 0.0051); // ~60% LTV 25yr illustrative

      unitSalesCard.style.display = 'block';
      unitSalesCard.innerHTML = `
        <div class="flex-between" style="border-bottom:1px solid #334155;padding-bottom:8px;margin-bottom:10px;">
          <div>
            <div style="display:flex;align-items:center;gap:6px;">
              <span style="background:#fde047;color:#0f172a;font-weight:900;font-size:12px;padding:2px 7px;border-radius:6px;">דירה #${u.num} (${u.code})</span>
              <span class="status-badge ${badgeCls}">${u.statusLabel}</span>
            </div>
            <div style="font-size:14px;font-weight:900;color:#ffffff;margin-top:4px;">
              ${u.type.startsWith('P') ? 'פנטהאוז דופלקס יוקרתי (קומות 6–7)' : `דירת ${u.rooms} חדרים מרווחת · קומה ${u.floor}`}
            </div>
          </div>
          <button id="btn-close-unit-card" class="ui-btn" style="background:#1e293b;color:#ffffff;border-color:#475569;padding:3px 8px;">✕</button>
        </div>

        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-bottom:10px;text-align:center;">
          <div style="background:#1e293b;border:1px solid #334155;border-radius:8px;padding:6px;">
            <div style="font-size:10px;color:#94a3b8;">שטח פנים (נטו)</div>
            <div style="font-size:14px;font-weight:900;color:#38bdf8;">${u.area} מ"ר</div>
          </div>
          <div style="background:#1e293b;border:1px solid #334155;border-radius:8px;padding:6px;">
            <div style="font-size:10px;color:#94a3b8;">מרפסת שמש/גג</div>
            <div style="font-size:14px;font-weight:900;color:#fde047;">+${u.balcony} מ"ר</div>
          </div>
          <div style="background:#1e293b;border:1px solid #334155;border-radius:8px;padding:6px;">
            <div style="font-size:10px;color:#94a3b8;">מפלס קומה</div>
            <div style="font-size:13px;font-weight:900;color:#ffffff;">+${u.zFlr.toFixed(2)} מ'</div>
          </div>
        </div>

        <div style="background:#1e293b;border:1px solid #334155;border-radius:10px;padding:9px;margin-bottom:10px;font-size:11px;">
          <div class="flex-between" style="margin-bottom:4px;">
            <span style="color:#94a3b8;">כיווני אוויר ושמש:</span>
            <span style="font-weight:800;color:#ffffff;">${u.dirs}</span>
          </div>
          <div class="flex-between" style="margin-bottom:4px;">
            <span style="color:#94a3b8;">חניה תת-קרקעית צמודה (תשריט A-1000):</span>
            <span style="font-weight:800;color:#6ee7b7;">חניה #${u.parking} (מפלס -3.50)</span>
          </div>
          <div class="flex-between" style="border-top:1px solid #334155;padding-top:6px;margin-top:6px;">
            <span style="color:#fde047;font-weight:800;">מחיר מחירון רשמי:</span>
            <span style="font-size:15px;font-weight:900;color:#10b981;">${showUnitPrices && u.status !== 'owner' ? formatILS(u.price) : 'פנה למשרד המכירות'}</span>
          </div>
          ${showUnitPrices && u.status !== 'owner' ? `
          <div style="margin-top:6px;padding-top:6px;border-top:1px dashed #334155;color:#cbd5e1;font-size:10px;">
            <div>💳 <b>מסלול 20/80 יזמי:</b> בחתימה ${formatILS(downPayment20)} (20%) · במסירה ${formatILS(balance80)} (80%)</div>
            <div style="margin-top:2px;">🏦 אומדן החזר משכנתא חודשי (60% מימון): ~${formatILS(estMonthlyMortgage)} / חודש</div>
          </div>` : ''}
        </div>

        <div class="grid-2" style="margin-bottom:6px;">
          <button id="btn-card-enter-tour" class="ui-btn" style="background:#b45309;color:#ffffff;border-color:#d97706;font-weight:800;">
            ✨ סיור 3D בדירה
          </button>
          <button id="btn-card-balcony-view" class="ui-btn" style="background:#0284c7;color:#ffffff;border-color:#38bdf8;font-weight:800;">
            🔭 נוף מהמרפסת (ק' ${u.floor})
          </button>
          <button id="btn-card-show-parking" class="ui-btn" style="background:#1e293b;color:#6ee7b7;border-color:#059669;font-weight:800;">
            🚗 הצג חניה #${u.parking} במרתף
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
        if (u.type === 'PB') enterPenthouseDollhouseMode('PB');
        else if (u.type === 'PC') enterPenthouseDollhouseMode('PC');
        else if (u.type === 'A') flyToAptCRoom('apta_living', false);
        else if (u.type === 'B') flyToAptCRoom('aptb_living', false);
        else flyToAptCRoom('living_main', false);
      });
      document.getElementById('btn-card-balcony-view').addEventListener('click', () => {
        closeAllDrawers();
        const baseType = u.type.startsWith('P') ? (u.type === 'PB' ? 'B' : 'A') : u.type;
        flyToBalconyFloorView(u.floor, baseType);
      });
      document.getElementById('btn-card-show-parking').addEventListener('click', () => {
        closeAllDrawers();
        activatePreset('cut_basement');
        const st = PARKING_STALL_COORDS[u.parking];
        if (st && parkingHighlightMesh) {
          parkingHighlightMesh.position.copy(cadTo3D(st.x, st.y, -2.65));
          parkingHighlightMesh.visible = true;
        }
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
  <title>הצעת מחיר ומפרט טכני — דירה #${u.num} (${u.code}) · פינס 48 פתח תקווה</title>
  <style>
    body { font-family: 'Segoe UI', Tahoma, Arial, sans-serif; margin: 0; padding: 28px; color: #0f172a; background: #ffffff; }
    .hdr { display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #1e3a8a; padding-bottom: 14px; margin-bottom: 18px; }
    .brand-box { display: flex; align-items: center; gap: 12px; }
    .logo { width: 52px; height: 52px; border-radius: 12px; background: #0f172a; color: #fde047; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 18px; }
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
      <div class="logo">K48</div>
      <div>
        <div style="font-size:20px;font-weight:900;color:#0f172a;">יצחק קולסקי חברה לבניה והשקעות בע"מ</div>
        <div style="font-size:13px;color:#475569;font-weight:700;">פרויקט בוטיק פינס 48 פינת הבעל שם טוב, פתח תקווה · אדריכלות: נחומי אדריכלים</div>
      </div>
    </div>
    <div style="text-align:left;font-size:12px;color:#475569;">
      <div><b>תאריך הפקה:</b> ${todayStr}</div>
      <div><b>חלקה 91 בגוש 6373</b> · 17 יח"ד</div>
    </div>
  </div>

  <div class="grid">
    <div class="kpi"><div class="kpi-lbl">מספר דירה וטיפוס</div><div class="kpi-val">דירה #${u.num} (${u.code})</div></div>
    <div class="kpi"><div class="kpi-lbl">קומה ומפלס</div><div class="kpi-val">קומה ${u.floor} (+${u.zFlr.toFixed(2)})</div></div>
    <div class="kpi"><div class="kpi-lbl">שטח דירה + מרפסת</div><div class="kpi-val">${u.area} + ${u.balcony} מ"ר</div></div>
    <div class="kpi" style="background:#ecfdf5;border-color:#6ee7b7;"><div class="kpi-lbl" style="color:#065f46;">מחיר מחירון</div><div class="kpi-val" style="color:#047857;">${u.status !== 'owner' ? formatILS(u.price) : 'דירת בעלים'}</div></div>
  </div>

  <div class="two-col">
    <div class="box">
      <div style="font-size:14px;font-weight:900;color:#1e3a8a;margin-bottom:8px;">📋 מפרט טכני ותנאי עסקה — דירה #${u.num} (${u.code})</div>
      <table>
        <tr><td><b>מספר חדרים:</b></td><td>${u.rooms} חדרים (${u.type.startsWith('P') ? 'פנטהאוז דופלקס 2 מפלסים' : 'תכנון אדריכלי מרווח'})</td></tr>
        <tr><td><b>כיווני אוויר מלאים:</b></td><td>${u.dirs}</td></tr>
        <tr><td><b>חניה תת-קרקעית בטאבו:</b></td><td>חניה רגילה #${u.parking} במפלס מרתף (-3.50 מ', תשריט A-1000)</td></tr>
        <tr><td><b>מפרט פנים יוקרתי:</b></td><td>ריצוף גרניט פורצלן 120×120, מטבח יוקרה עם אי שיש קלקטה, תריסי אור חשמליים, מיזוג VRF</td></tr>
        <tr><td><b>תנאי תשלום יזמיים (20/80):</b></td><td>20% בחתימה (${formatILS(down20)}) · 80% במסירת חזקה (${formatILS(bal80)})</td></tr>
        <tr><td><b>נגישות תחבורתית ומוקדי סביבה:</b></td><td>882 מ' לתחנת מטרו עיריית פ"ת (קו M2 העתידי), 220 מ' לביה"ס פיק"א, 1.04 ק"מ לרכבת הקלה</td></tr>
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

    // Wire 17-Unit Catalog Buttons & Filters
    const btnTopUnits3D = document.getElementById('btn-top-units-3d');
    if (btnTopUnits3D) {
      btnTopUnits3D.addEventListener('click', () => {
        units3DVisible = !units3DVisible;
        if (units3DVisible && spherical.radius > 140) {
          activatePreset('iso_ne');
        }
        syncUnits3DToggleUI();
      });
    }
    const btnDrawerUnits3D = document.getElementById('btn-drawer-units-3d');
    if (btnDrawerUnits3D) {
      btnDrawerUnits3D.addEventListener('click', () => {
        units3DVisible = !units3DVisible;
        if (units3DVisible && spherical.radius > 140) {
          activatePreset('iso_ne');
        }
        syncUnits3DToggleUI();
      });
    }
    const btnTogglePrices = document.getElementById('btn-toggle-prices');
    if (btnTogglePrices) {
      btnTogglePrices.addEventListener('click', () => {
        showUnitPrices = !showUnitPrices;
        btnTogglePrices.textContent = showUnitPrices ? '👁️ מחירים: מוצג' : '👁️ מחירים: מוסתר';
        btnTogglePrices.className = showUnitPrices ? 'ui-btn active' : 'ui-btn';
        renderUnitsCatalogList();
        if (selectedUnitObj && unitSalesCard.style.display === 'block') {
          selectUnitAndOpenCard(selectedUnitObj);
        }
      });
    }
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
    renderUnitsCatalogList();

    // =========================================================================
    // REAL-TIME 4 INTERIOR FINISH PACKAGES CUSTOMIZER, BALCONY DECK & FURNITURE
    // =========================================================================
    const INTERIOR_PACKAGES = {
      nordic_oak: {
        label: "Nordic Oak",
        floorMap: defaultTravertineTex,
        floorColor: 0xbec5ce,
        cabinetColor: 0xdcb98a,
        oakColor: 0xc49a68,
        marbleColor: 0xffffff,
        sofaColor: 0xeee7dc
      },
      warm_sahara: {
        label: "Warm Sahara",
        floorMap: defaultTravertineTex,
        floorColor: 0xdfd3c3,
        cabinetColor: 0xe6d7c3,
        oakColor: 0xb88652,
        marbleColor: 0xfaf3e8,
        sofaColor: 0xf4ede2
      },
      urban_anthracite: {
        label: "Urban Anthracite",
        floorMap: defaultTravertineTex,
        floorColor: 0x737b86,
        cabinetColor: 0x947153,
        oakColor: 0x7c5836,
        marbleColor: 0xe2e8f0,
        sofaColor: 0xe2e8f0
      },
      classic_parquet: {
        label: "Classic Parquet",
        floorMap: defaultParquetTex,
        floorColor: 0xe6cda8,
        cabinetColor: 0xf8fafc,
        oakColor: 0xd4a976,
        marbleColor: 0xffffff,
        sofaColor: 0xf5f0e6
      }
    };

    document.querySelectorAll('#interior-pkg-buttons [data-pkg]').forEach(btn => {
      btn.addEventListener('click', () => {
        const pkgKey = btn.dataset.pkg;
        const pkg = INTERIOR_PACKAGES[pkgKey];
        if (!pkg) return;
        document.querySelectorAll('#interior-pkg-buttons [data-pkg]').forEach(b => {
          b.className = (b === btn) ? 'pkg-card-btn active' : 'pkg-card-btn';
        });
        const badge = document.getElementById('active-pkg-badge');
        if (badge) badge.textContent = pkg.label;

        matDefs.mat_lux_travertine_floor.map = pkg.floorMap;
        matDefs.mat_lux_travertine_floor.color.setHex(pkg.floorColor);
        matDefs.mat_lux_travertine_floor.needsUpdate = true;
        matDefs.mat_lux_cabinet_cream.color.setHex(pkg.cabinetColor);
        matDefs.mat_lux_oak_smooth.color.setHex(pkg.oakColor);
        matDefs.mat_lux_fluted_oak.color.setHex(pkg.oakColor);
        matDefs.mat_lux_calacatta_marble.color.setHex(pkg.marbleColor);
        matDefs.mat_lux_boucle_cream.color.setHex(pkg.sofaColor);
      });
    });

    let balconyWoodDeckActive = false;
    const btnBalconyDeck = document.getElementById('btn-balcony-deck');
    if (btnBalconyDeck) {
      btnBalconyDeck.addEventListener('click', () => {
        balconyWoodDeckActive = !balconyWoodDeckActive;
        const targetMat = balconyWoodDeckActive ? matDefs.mat_wood_deck : matDefs.mat_terrace_tile;
        balconyFloorMeshes.forEach(m => { m.material = targetMat; });
        btnBalconyDeck.textContent = balconyWoodDeckActive ? '🪵 מרפסות: דמוי דק עץ' : '🪵 מרפסות: פורצלן אפור';
        btnBalconyDeck.className = balconyWoodDeckActive ? 'ui-btn active' : 'ui-btn';
      });
    }

    let furnitureVisible = true;
    const btnToggleFurniture = document.getElementById('btn-toggle-furniture');
    if (btnToggleFurniture) {
      btnToggleFurniture.addEventListener('click', () => {
        furnitureVisible = !furnitureVisible;
        interiorFurnitureMeshes.forEach(m => { m.visible = furnitureVisible; });
        btnToggleFurniture.textContent = furnitureVisible ? '🪑 ריהוט 3D: פעיל' : '🪑 ריהוט 3D: מוסתר (חלל ריק)';
        btnToggleFurniture.className = furnitureVisible ? 'ui-btn active' : 'ui-btn';
      });
    }

    // =========================================================================
    // ARCHITECTURAL NIGHT / GOLDEN HOUR MODE (🌙 מצב לילה)
    // =========================================================================
    let isNightMode = false;
    const btnTopNight = document.getElementById('btn-top-night');
    if (btnTopNight) {
      btnTopNight.addEventListener('click', () => {
        isNightMode = !isNightMode;
        btnTopNight.className = isNightMode ? 'ui-btn active' : 'ui-btn';
        btnTopNight.textContent = isNightMode ? '☀️ מצב יום' : '🌙 מצב לילה';

        if (isNightMode) {
          scene.background.setHex(0x0b1329);
          hemiLight.color.setHex(0x3b82f6);
          hemiLight.groundColor.setHex(0x0f172a);
          hemiLight.intensity = 0.28;
          sunLight.color.setHex(0xf59e0b);
          sunLight.intensity = 0.22;
          fillLight.intensity = 0.14;
          matDefs.mat_window_glass.emissive = new THREE.Color(0xfde68a);
          matDefs.mat_window_glass.emissiveIntensity = 0.42;
          interiorPointLights.forEach(pt => {
            pt.intensity = (pt.userData.baseIntensity || 0.6) * 2.15;
          });
          balconySpotLights.forEach(sp => {
            sp.intensity = 0.95;
          });
        } else {
          scene.background.setHex(0xffffff);
          hemiLight.color.setHex(0xffffff);
          hemiLight.groundColor.setHex(0xcbd5e1);
          hemiLight.intensity = 0.72;
          sunLight.color.setHex(0xfffdf8);
          sunLight.intensity = 0.88;
          fillLight.intensity = 0.48;
          matDefs.mat_window_glass.emissive = new THREE.Color(0x000000);
          matDefs.mat_window_glass.emissiveIntensity = 0.0;
          interiorPointLights.forEach(pt => {
            pt.intensity = pt.userData.baseIntensity || 0.6;
          });
          balconySpotLights.forEach(sp => {
            sp.intensity = 0.0;
          });
        }
      });
    }

    // =========================================================================
    // 3D LASER TAPE MEASURE TOOL (📏 מדידה) & 3D UNIT CLICK SELECTION
    // =========================================================================
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
      while (measureGroup.children.length > 0) {
        measureGroup.remove(measureGroup.children[0]);
      }
      measureBadges.forEach(b => b.el.remove());
      measureBadges.length = 0;
      if (measureLastVal) measureLastVal.textContent = 'מוכן למדידה';
    }

    const btnTopMeasure = document.getElementById('btn-top-measure');
    if (btnTopMeasure) {
      btnTopMeasure.addEventListener('click', () => {
        isMeasureMode = !isMeasureMode;
        btnTopMeasure.className = isMeasureMode ? 'ui-btn active' : 'ui-btn';
        if (measureHud) measureHud.style.display = isMeasureMode ? 'flex' : 'none';
        measurePtA = null;
      });
    }
    const btnClearMeasures = document.getElementById('btn-clear-measures');
    if (btnClearMeasures) btnClearMeasures.addEventListener('click', clearAllMeasurements);
    const btnCloseMeasure = document.getElementById('btn-close-measure');
    if (btnCloseMeasure) {
      btnCloseMeasure.addEventListener('click', () => {
        isMeasureMode = false;
        if (btnTopMeasure) btnTopMeasure.className = 'ui-btn';
        if (measureHud) measureHud.style.display = 'none';
      });
    }

    let downClientPos = { x: 0, y: 0 };
    canvas.addEventListener('pointerdown', e => {
      downClientPos = { x: e.clientX, y: e.clientY };
    });
    canvas.addEventListener('pointerup', e => {
      const moveDist = Math.hypot(e.clientX - downClientPos.x, e.clientY - downClientPos.y);
      if (moveDist > 5 || e.button !== 0) return;

      const rect = canvas.getBoundingClientRect();
      mouseNDC.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouseNDC.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
      raycaster.setFromCamera(mouseNDC, activeCam);

      // 1. If 3D Laser Tape Measure is active, measure between 2 clicked points
      if (isMeasureMode) {
        const hits = raycaster.intersectObjects(allMeshes, false).filter(h => h.point.y <= clipPlane.constant + 0.05);
        if (hits.length === 0) return;
        const pt = hits[0].point.clone();
        const dotGeom = new THREE.SphereGeometry(0.11, 16, 16);
        const dotMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });
        const dot = new THREE.Mesh(dotGeom, dotMat);
        dot.position.copy(pt);
        measureGroup.add(dot);

        if (!measurePtA) {
          measurePtA = pt;
          if (measureLastVal) measureLastVal.textContent = 'בחר נקודה שנייה...';
        } else {
          const distM = measurePtA.distanceTo(pt);
          const lineGeom = new THREE.BufferGeometry().setFromPoints([measurePtA, pt]);
          const lineMat = new THREE.LineBasicMaterial({ color: 0x38bdf8, linewidth: 3 });
          measureGroup.add(new THREE.Line(lineGeom, lineMat));

          const mid = new THREE.Vector3().addVectors(measurePtA, pt).multiplyScalar(0.5);
          const badge = document.createElement('div');
          badge.style.cssText = 'position:absolute;transform:translate(-50%,-50%);background:#0284c7;color:#ffffff;font-weight:900;font-size:11px;padding:3px 8px;border-radius:999px;border:1.5px solid #ffffff;box-shadow:0 4px 10px rgba(0,0,0,0.35);white-space:nowrap;';
          badge.textContent = `📏 ${distM.toFixed(2)} מ' (${Math.round(distM * 100)} ס"מ)`;
          measureLabelsContainer.appendChild(badge);
          measureBadges.push({ pos: mid, el: badge });
          if (measureLastVal) measureLastVal.textContent = `מרחק: ${distM.toFixed(2)} מ'`;
          measurePtA = null;
        }
        return;
      }

      // 2. If 3D Unit Volumes are visible, clicking a 3D unit opens its Sales Card
      if (units3DVisible) {
        const visMeshes = unitVolumeMeshes.filter(m => m.visible);
        const uHits = raycaster.intersectObjects(visMeshes, false);
        if (uHits.length > 0 && uHits[0].object.userData.unit) {
          selectUnitAndOpenCard(uHits[0].object.userData.unit);
        }
      }
    });

    // Resize Handler
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
      syncSidePanelTop();
    });

    const topHeaderEl = document.querySelector('.top-header');
    const sidePanelEl = document.querySelector('.side-panel');
    function syncSidePanelTop() {
      if (topHeaderEl && sidePanelEl) {
        const bottomEdge = topHeaderEl.offsetTop + topHeaderEl.offsetHeight;
        sidePanelEl.style.top = (bottomEdge + 10) + 'px';
      }
    }
    syncSidePanelTop();
    if (window.ResizeObserver && topHeaderEl) {
      new ResizeObserver(syncSidePanelTop).observe(topHeaderEl);
    }

    // Initialize directly on the 3D Model overlaid on the Regional Google Maps Distance Map (showing all 28 POIs!)
    activatePreset('gmaps_regional');

    // Render Loop
    let lastFrameTime = performance.now();
    function animate(now = performance.now()) {
      requestAnimationFrame(animate);
      const dt = Math.min(0.05, Math.max(0.001, (now - lastFrameTime) * 0.001));
      lastFrameTime = now;

      if (fpAnim) {
        const u = Math.min(1.0, (now - fpAnim.t0) / fpAnim.dur);
        const ease = u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
        fpEyePos.lerpVectors(fpAnim.startPos, fpAnim.endPos, ease);
        fpYaw = fpAnim.startYaw + fpAnim.dYaw * ease;
        fpPitch = fpAnim.startPitch + (fpAnim.endPitch - fpAnim.startPitch) * ease;
        updateCameraFromFirstPerson();
        if (u >= 1.0) fpAnim = null;
      } else if (isFirstPersonAptC) {
        const fwd = (keysDown['KeyW'] || keysDown['ArrowUp'] ? 1 : 0) - (keysDown['KeyS'] || keysDown['ArrowDown'] ? 1 : 0);
        const str = (keysDown['KeyD'] || keysDown['ArrowRight'] ? 1 : 0) - (keysDown['KeyA'] || keysDown['ArrowLeft'] ? 1 : 0);
        const trn = (keysDown['KeyQ'] ? 1 : 0) - (keysDown['KeyE'] ? 1 : 0);
        if (fwd !== 0 || str !== 0 || trn !== 0) {
          const speed = 3.2 * dt;
          const fVec = new THREE.Vector3(-Math.sin(fpYaw), 0, -Math.cos(fpYaw));
          const rVec = new THREE.Vector3(Math.cos(fpYaw), 0, -Math.sin(fpYaw));
          fpEyePos.addScaledVector(fVec, fwd * speed);
          fpEyePos.addScaledVector(rVec, str * speed);
          fpYaw += trn * 1.6 * dt;
          clampPositionToAptC(fpEyePos);
          updateCameraFromFirstPerson();
        }
      }

      renderer.render(scene, activeCam);

      const w = window.innerWidth, h = window.innerHeight;
      if (showLabels) {
        const clipH = clipPlane.constant;
        const isInteriorCut = clipH < 26.0;

        allCalloutObjs.forEach(c => {
          if (isFirstPersonAptC) {
            c.el.style.opacity = '0';
            return;
          }
          let visible = false;
          if (!c.isInterior) {
            visible = (c.mode === "both" || !isInteriorCut) && (c.pos.y <= clipH);
          } else {
            if (isInteriorCut && clipH >= c.zMin && clipH <= c.zMax) {
              visible = true;
              c.pos.y = clipH - 0.35;
            }
          }

          if (!visible) {
            c.el.style.opacity = '0';
            return;
          }
          const p = c.pos.clone().project(activeCam);
          if (p.z > 1 || p.z < -1) {
            c.el.style.opacity = '0';
            return;
          }
          const sx = (p.x * 0.5 + 0.5) * w;
          const sy = (-p.y * 0.5 + 0.5) * h;
          c.el.style.left = `${sx}px`;
          c.el.style.top = `${sy}px`;
          c.el.style.opacity = '1';
        });
      }

      // Project 3D GIS Distance Ring Badges & POI Location Badges
      gisRingLabelObjs.forEach(rl => {
        if (isFirstPersonAptC || !gisRadiiVisible || !layerGroups[L_SITE].visible) {
          rl.el.style.display = 'none';
          return;
        }
        const p = rl.pos.clone().project(activeCam);
        if (p.z > 1 || p.z < -1) {
          rl.el.style.display = 'none';
          return;
        }
        const sx = (p.x * 0.5 + 0.5) * w;
        const sy = (-p.y * 0.5 + 0.5) * h;
        if (sx < -60 || sx > w + 60 || sy < -30 || sy > h + 30) {
          rl.el.style.display = 'none';
          return;
        }
        rl.el.style.display = 'block';
        rl.el.style.left = `${sx}px`;
        rl.el.style.top = `${sy}px`;
      });

      gisPoiLabelObjs.forEach(pl => {
        const catMatch = (activeGisCategory === 'all' || pl.poi.cat === activeGisCategory);
        if (isFirstPersonAptC || !gisPoisVisible || !catMatch || !layerGroups[L_SITE].visible) {
          pl.el.style.display = 'none';
          return;
        }
        const p = pl.pos.clone().project(activeCam);
        if (p.z > 1 || p.z < -1) {
          pl.el.style.display = 'none';
          return;
        }
        const sx = (p.x * 0.5 + 0.5) * w;
        const sy = (-p.y * 0.5 + 0.5) * h;
        if (sx < -80 || sx > w + 80 || sy < -30 || sy > h + 30) {
          pl.el.style.display = 'none';
          return;
        }
        pl.el.style.display = 'flex';
        pl.el.style.left = `${sx}px`;
        pl.el.style.top = `${sy}px`;
      });

      // Project 3D Interactive Unit Badges when units3DVisible is active
      unitBadgeObjs.forEach(ub => {
        if (isFirstPersonAptC || !units3DVisible || !ub.mesh.visible || ub.pos.y > clipPlane.constant) {
          ub.el.style.display = 'none';
          return;
        }
        const p = ub.pos.clone().project(activeCam);
        if (p.z > 1 || p.z < -1) {
          ub.el.style.display = 'none';
          return;
        }
        const sx = (p.x * 0.5 + 0.5) * w;
        const sy = (-p.y * 0.5 + 0.5) * h;
        if (sx < -60 || sx > w + 60 || sy < -30 || sy > h + 30) {
          ub.el.style.display = 'none';
          return;
        }
        ub.el.style.display = 'inline-flex';
        ub.el.style.left = `${sx}px`;
        ub.el.style.top = `${sy}px`;
      });

      // Project 3D Laser Measurement Badges
      measureBadges.forEach(mb => {
        const p = mb.pos.clone().project(activeCam);
        if (p.z > 1 || p.z < -1) {
          mb.el.style.display = 'none';
          return;
        }
        const sx = (p.x * 0.5 + 0.5) * w;
        const sy = (-p.y * 0.5 + 0.5) * h;
        mb.el.style.display = 'block';
        mb.el.style.left = `${sx}px`;
        mb.el.style.top = `${sy}px`;
      });
    }
    animate();
  })();
  </script>
</body>
</html>
"""

final_html = (
    HTML_TEMPLATE
    .replace("__THREE_JS_INLINED__", three_js_code)
    .replace("__EXTRACTED_PLANS_JSON__", extracted_plans_json)
    .replace("__WIDE_GMAPS_DATA_URI__", wide_gmaps_data_uri)
    .replace("__INNER_GMAPS_DATA_URI__", inner_gmaps_data_uri)
    .replace("__CLOSEUP_GMAPS_DATA_URI__", closeup_gmaps_data_uri)
    .replace("__SPATIAL_POIS_JSON__", spatial_pois_json)
)

with open(OUT_WORKSPACE_HTML, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"Saved standalone interactive viewer with full exact facades, interiors & Google Maps base to {OUT_WORKSPACE_HTML} ({len(final_html):,} bytes)")

