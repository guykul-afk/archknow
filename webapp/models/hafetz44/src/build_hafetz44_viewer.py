# -*- coding: utf-8 -*-
import os, json, shutil

ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\ee869ca7-2259-4d89-9693-4d5c0376b65b"
PREV_ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e"
SCRATCH_DIR = os.path.join(ARTIFACT_DIR, "scratch", "hafetz44")
THREE_JS_PATH = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\_shared_engine\three.min.js"
PUBLIC_DIR = os.path.join(os.getcwd(), "public", "projects", "hafetz-44")
DRIVE_MODEL_DIR = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\חפץ חיים 44 פתח תקווה"

with open(THREE_JS_PATH, "r", encoding="utf-8") as f:
    three_js_code = f.read()

DATA_DIR = os.path.join(DRIVE_MODEL_DIR, "data")
os.makedirs(SCRATCH_DIR, exist_ok=True)
for fn in ["hafetz44_extracted_plans.json", "hafetz44_units_crm.json"]:
    src_p = os.path.join(DATA_DIR, fn)
    dst_p = os.path.join(SCRATCH_DIR, fn)
    if os.path.exists(src_p):
        shutil.copy2(src_p, dst_p)

with open(os.path.join(DATA_DIR, "hafetz44_extracted_plans.json"), "r", encoding="utf-8") as f:
    plans_data = json.load(f)

with open(os.path.join(DATA_DIR, "hafetz44_units_crm.json"), "r", encoding="utf-8") as f:
    crm_data = json.load(f)

with open(os.path.join(DATA_DIR, "unified_hafetz44_3d_map.json"), "r", encoding="utf-8") as f:
    unified_map_data = json.load(f)

with open(os.path.join(DATA_DIR, "hafetz44_spatial_map_data.json"), "r", encoding="utf-8") as f:
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
  <title>חפץ חיים 44, פתח תקוה — מערכת שיווק, מכירות והדמיה תלת-ממדית אינטראקטיבית (1:50 CAD & GIS)</title>
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
          HH44
        </div>
        <div>
          <div style="display:flex;align-items:center;gap:7px;flex-wrap:wrap;">
            <h1 style="margin:0;font-size:14px;font-weight:800;color:#0f172a;">קבוצת קולסקי · חפץ חיים 44, פתח תקווה</h1>
            <span style="border-radius:6px;border:1px solid #dec9ad;background:#fef3c7;padding:1px 7px;font-size:10px;font-weight:800;color:#92400e;">סטודיו אורכה — אדר' אורן קמה · פורטל הנדסי ושיווקי 3D (17 יח"ד · גוש 6396 חלקה 85)</span>
          </div>
        </div>
      </div>

      <div style="display:flex;flex-wrap:wrap;align-items:center;gap:5px;" id="view-buttons">
        <button data-view="iso_east" id="btn-top-bldg" class="view-btn ui-btn" title="מבט חוץ אדריכלי על הבניין מרחוב חפץ חיים 44">
          🏢 מבט הבניין
        </button>
        <button data-view="gmaps_regional" id="btn-top-gis-map" class="view-btn ui-btn active" title="מבט רחפן על הבניין יושב על מפת העיר פתח תקווה ו-28 מוקדי הסביבה">
          🗺️ מפת סביבה
        </button>
        <button id="btn-top-units-3d" class="ui-btn" style="border-color:#10b981;color:#065f46;background:#ecfdf5;font-weight:800;" title="הצג/הסתר סימון 17 דירות תלת-ממדי לפי זמינות ומחיר על חזיתות הבניין">
          🏢 סימון דירות 3D
        </button>
        <button id="btn-top-radii" class="ui-btn active" title="הדלק/כבה 8 מעגלי מרחק וזמני הליכה סביב חפץ חיים 44">
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
          <span>🏷️ קטלוג דירות ומחירים (17)</span>
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

    <!-- DRAWER 0: 17 UNITS CATALOG & LIVE CRM -->
    <div id="drawer-units" class="glass-panel dropdown-drawer" style="width:425px;">
      <div class="flex-between" style="margin-bottom:8px;border-bottom:1px solid #e2e8f0;padding-bottom:6px;">
        <div>
          <div style="font-size:13px;font-weight:800;color:#065f46;">🏷️ קטלוג 17 הדירות והמחירון הרשמי — חפץ חיים 44</div>
          <div style="font-size:11px;color:#64748b;">2 דירות בקומה (ק' 1–8) + פנטהאוז יוקרה בקומה 9 · לחץ על דירה לכרטיס ו-PDF</div>
        </div>
        <button data-close-drawer class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
      </div>

      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin-bottom:8px;text-align:center;">
        <div style="background:#ecfdf5;border:1px solid #a7f3d0;border-radius:8px;padding:5px;">
          <div style="font-size:10px;color:#065f46;font-weight:700;">🟢 מלאי קולסקי זמין</div>
          <div id="kpi-avail-count" style="font-size:14px;font-weight:900;color:#047857;">11 דירות</div>
        </div>
        <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:5px;">
          <div style="font-size:10px;color:#1e40af;font-weight:700;">🏢 סה"כ בפרויקט</div>
          <div style="font-size:14px;font-weight:900;color:#1d4ed8;">17 יח"ד · 19 חניות + 2 אופנועים</div>
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
        <button data-ubldg="all" class="unit-bldg-chip ui-btn active" style="padding:3px 8px;font-size:10px;">כל האגפים (17)</button>
        <button data-ubldg="W" class="unit-bldg-chip ui-btn" style="padding:3px 8px;font-size:10px;">אגף מערבי · 5 חד' (8)</button>
        <button data-ubldg="E" class="unit-bldg-chip ui-btn" style="padding:3px 8px;font-size:10px;">אגף מזרחי · 4 חד' (8)</button>
        <button data-ubldg="PH" class="unit-bldg-chip ui-btn" style="padding:3px 8px;font-size:10px;">👑 פנטהאוז קומה 9 (1)</button>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:6px;" id="unit-status-filters">
        <button data-ustatus="all" class="unit-status-chip ui-btn active" style="padding:3px 8px;font-size:10px;">כל הסטטוסים (17)</button>
        <button data-ustatus="available" class="unit-status-chip ui-btn" style="padding:3px 8px;font-size:10px;">🟢 פנויות לשיווק קולסקי (11)</button>
        <button data-ustatus="owner" class="unit-status-chip ui-btn" style="padding:3px 8px;font-size:10px;">🔒 דירות בעלים (6)</button>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px;" id="unit-room-filters">
        <button data-urooms="all" class="unit-room-chip ui-btn active" style="padding:3px 8px;font-size:10px;">כל הגדלים</button>
        <button data-urooms="4" class="unit-room-chip ui-btn" style="padding:3px 8px;font-size:10px;">4 חד' מזרח (89.4+18.8 מ"ר)</button>
        <button data-urooms="5" class="unit-room-chip ui-btn" style="padding:3px 8px;font-size:10px;">5 חד' מערב (113.3+18.8 מ"ר)</button>
        <button data-urooms="6" class="unit-room-chip ui-btn" style="padding:3px 8px;font-size:10px;">6 חד' פנטהאוז (148.1+73.0 מ"ר)</button>
      </div>

      <div id="units-catalog-list" style="max-height:280px;overflow-y:auto;display:flex;flex-direction:column;gap:5px;padding-left:2px;"></div>
    </div>

    <!-- DRAWER 1: APARTMENT TOURS & BALCONY VIEW SIMULATOR -->
    <div id="drawer-apartments" class="glass-panel dropdown-drawer" style="width:415px;">
      <div class="flex-between" style="margin-bottom:10px;border-bottom:1px solid #e2e8f0;padding-bottom:8px;">
        <div>
          <div style="font-size:13px;font-weight:800;color:#78350f;">✨ סיור פנים מרוהט 3D (ק' 4, 5 ופנטהאוז 9) ונוף מהמרפסת</div>
          <div style="font-size:11px;color:#64748b;">מידול פנים תלת-ממדי מלא במפרט פינס 48 + ג'קוזי ומטבח חוץ בפנטהאוז</div>
        </div>
        <button data-close-drawer class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
      </div>

      <div style="font-size:11px;font-weight:800;color:#92400e;margin-bottom:5px;">🛋️ מבט-על חתך Dollhouse לקומות המרוהטות בתלת-ממד (מפרט פינס 48):</div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin-bottom:8px;">
        <button onclick="openFurnishedDollhouse('f4')" class="ui-btn ui-btn-lux" style="font-weight:800;">✨ קומה 4 (+12.95)</button>
        <button onclick="openFurnishedDollhouse('f5')" class="ui-btn ui-btn-lux" style="font-weight:800;">✨ קומה 5 (+16.10)</button>
        <button onclick="openFurnishedDollhouse('f9')" class="ui-btn" style="background:#0f172a;color:#fde047;border-color:#334155;font-weight:800;">👑 פנטהאוז 9 (+28.70)</button>
      </div>

      <div style="font-size:11px;font-weight:800;color:#1e3a8a;margin-bottom:5px;">🏢 סיור בגוף ראשון (1.68 מ') בדירות המרוהטות של חפץ חיים 44:</div>
      <div class="grid-2" style="margin-bottom:8px;">
        <button onclick="startPresetInteriorTour(4, 'W')" class="ui-btn ui-btn-lux">✨ ק'4 · דירת 5 חד' מערבית (#7)</button>
        <button onclick="startPresetInteriorTour(4, 'E')" class="ui-btn ui-btn-lux">✨ ק'4 · דירת 4 חד' מזרחית (#8)</button>
        <button onclick="startPresetInteriorTour(5, 'W')" class="ui-btn ui-btn-lux">✨ ק'5 · דירת 5 חד' מערבית (#9)</button>
        <button onclick="startPresetInteriorTour(5, 'E')" class="ui-btn ui-btn-lux">✨ ק'5 · דירת 4 חד' מזרחית (#10)</button>
        <button onclick="startPresetInteriorTour(9, 'PH')" class="ui-btn" style="grid-column:span 2;background:#0f172a;color:#fde047;border-color:#334155;font-weight:800;">👑 ק'9 · פנטהאוז יוקרה על קומה שלמה (#17 · 148.1+73.0 מ"ר + ג'קוזי ו-BBQ)</button>
      </div>

      <div class="section-box" style="margin-bottom:0;">
        <div style="font-size:11px;font-weight:800;color:#451a03;margin-bottom:5px;">🔭 סימולטור "נוף מהמרפסת" לפי קומה מדויקת (קומות 1–9):</div>
        <div style="display:flex;flex-wrap:wrap;gap:4px;" id="balcony-floor-selector">
          <button data-bflr="1" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 1 (+3.50)</button>
          <button data-bflr="2" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 2 (+6.65)</button>
          <button data-bflr="3" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 3 (+9.80)</button>
          <button data-bflr="4" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 4 (+12.95)</button>
          <button data-bflr="5" class="ui-btn active" style="padding:3px 7px;font-size:10px;">קומה 5 (+16.10)</button>
          <button data-bflr="6" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 6 (+19.25)</button>
          <button data-bflr="7" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 7 (+22.40)</button>
          <button data-bflr="8" class="ui-btn" style="padding:3px 7px;font-size:10px;">קומה 8 (+25.55)</button>
          <button data-bflr="9" class="ui-btn" style="padding:3px 7px;font-size:10px;">פנטהאוז 9 (+28.70)</button>
        </div>
      </div>
    </div>

    <!-- DRAWER 2: 3D GIS SPATIAL MAP & 28 POIS -->
    <div id="drawer-gis" class="glass-panel dropdown-drawer" style="width:410px;">
      <div class="flex-between" style="margin-bottom:8px;border-bottom:1px solid #e2e8f0;padding-bottom:6px;">
        <div>
          <div style="font-size:13px;font-weight:800;color:#1e3a8a;">📍 מפת מרחקים ו-28 מוקדי סביבה ועירוניות (Google Maps)</div>
          <div style="font-size:11px;color:#64748b;">חינוך, קניות, בריאות, תחבורה ורכבת קלה, תרבות ופארקים סביב חפץ חיים 44</div>
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
        <a href="hafetz44_spatial_map.html" target="_blank" class="ui-btn" style="background:#0f172a;color:#38bdf8;border-color:#334155;font-weight:800;text-decoration:none;">
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
            🗺️ מפת לוויין Google Maps (חפץ חיים 44): פעיל
          </button>
          <button id="btn-ortho" class="ui-btn">📐 היטל אורתוגרפי (1:50)</button>
          <button id="btn-cad-plan" class="ui-btn active">✏️ שרטוט פנים CAD: פעיל</button>
          <button onclick="activatePreset('iso_east')" class="ui-btn">חזית מזרחית (חפץ חיים)</button>
          <button onclick="activatePreset('iso_west')" class="ui-btn">חזית מערבית (עורפית)</button>
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
            <span id="clip-val" class="cad-badge" style="font-size:11px;font-weight:800;color:#2563eb;">+35.50 מ' (מלא)</span>
          </div>
          <input id="clip-slider" type="range" min="-5.10" max="35.5" step="0.1" value="35.5" />
          <div class="flex-between cad-badge" style="margin-top:3px;font-size:9.5px;color:#64748b;">
            <span>-5.10</span>
            <span>0.00</span>
            <span>+9.80</span>
            <span>+19.25</span>
            <span>+28.70</span>
            <span>+34.55</span>
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
          <span id="apt-active-badge" style="border-radius:6px;background:#b45309;color:#ffffff;padding:3px 8px;font-size:11px;font-weight:800;">חפץ חיים 44</span>
          <span id="aptc-active-room-title" style="font-size:13px;font-weight:800;color:#451a03;">סיור פנים אדריכלי 1:50</span>
          <div style="display:inline-flex;align-items:center;gap:3px;background:#fef3c7;border:1px solid #f59e0b;border-radius:6px;padding:2px 6px;">
            <span style="font-size:10px;font-weight:800;color:#92400e;">קומה לנוף:</span>
            <select id="tour-floor-select" style="font-size:11px;font-weight:800;color:#451a03;background:transparent;border:none;cursor:pointer;outline:none;">
              <option value="1">קומה 1 (+3.50)</option>
              <option value="2">קומה 2 (+6.65)</option>
              <option value="3">קומה 3 (+9.80)</option>
              <option value="4">קומה 4 (+12.95)</option>
              <option value="5" selected>קומה 5 (+16.10)</option>
              <option value="6">קומה 6 (+19.25)</option>
              <option value="7">קומה 7 (+22.40)</option>
              <option value="8">קומה 8 (+25.55)</option>
              <option value="9">פנטהאוז 9 (+28.70)</option>
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
          <button onclick="teleportInTour(-10.5, 1.3, -1.57, 'דירה מערבית (5 חד\') · סלון ומטבח')" class="room-chip">🛋️ סלון מערבי (5 חד')</button>
          <button onclick="teleportInTour(-14.4, 1.0, -1.57, 'דירה מערבית · מרפסת שמש מערבית')" class="room-chip">☀️ מרפסת מערבית</button>
          <button onclick="teleportInTour(11.3, 1.3, 1.57, 'דירה מזרחית (4 חד\') · סלון ומטבח')" class="room-chip">🛋️ סלון מזרחי (4 חד')</button>
          <button onclick="teleportInTour(15.35, 1.0, 1.57, 'דירה מזרחית · מרפסת שמש לרחוב חפץ חיים')" class="room-chip">☀️ מרפסת מזרחית (חפץ חיים)</button>
          <button onclick="teleportInTour(0.95, 2.5, 0, 'לובי מעליות קומתי')" class="room-chip">🚪 לובי מעליות</button>
          <button onclick="teleportInTour(-11.8, 0.5, -1.57, 'פנטהאוז קומה 9 · מרפסת גג מערבית וג\'קוזי (295×940)', 'f9')" class="room-chip">👑 גג פנטהאוז מערב (ג'קוזי)</button>
          <button onclick="teleportInTour(11.9, 0.5, 1.57, 'פנטהאוז קומה 9 · מרפסת גג מזרחית ו-BBQ (456×940)', 'f9')" class="room-chip">👑 גג פנטהאוז מזרח (BBQ)</button>
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
    const HAFETZ_UNITS = CRM_DATA.units;
    const PARKING_STALLS = CRM_DATA.parking_stalls;
    const SPATIAL_POIS = __SPATIAL_POIS_JSON__;

    const WIDE_GMAPS_DATA_URI    = "__WIDE_GMAPS_URI__";
    const INNER_GMAPS_DATA_URI   = "__INNER_GMAPS_URI__";
    const CLOSEUP_GMAPS_DATA_URI = "__CLOSEUP_GMAPS_URI__";
    const OUTER_SPAN_M   = __OUTER_SPAN_M__;
    const INNER_SPAN_M   = __INNER_SPAN_M__;
    const CLOSEUP_SPAN_M = __CLOSEUP_SPAN_M__;

    // =========================================================================
    // 1. EXACT FLOOR SCHEDULE & ARCHITECTURAL CONSTANTS (HAFETZ HAIM 44)
    // =========================================================================
    const FLOORS = [
      { id: 'mar', label: 'מרתף חניון (13 חניות + 2 אופנועים)', zFloor: -5.10, zCeil: -0.35, zTop: 0.00, sheet: 'basement', elevText: '-5.10' },
      { id: 'kar', label: 'קומת קרקע ולובי ✨',   zFloor: 0.00,  zCeil: 3.22,  zTop: 3.50, sheet: 'ground',   elevText: '±0.00', has3DFurn: true },
      { id: 'f1',  label: 'קומה 1 (דירות 1–2)',   zFloor: 3.50,  zCeil: 6.37,  zTop: 6.65, sheet: 'typical',  elevText: '+3.50' },
      { id: 'f2',  label: 'קומה 2 (דירות 3–4)',   zFloor: 6.65,  zCeil: 9.52,  zTop: 9.80, sheet: 'typical',  elevText: '+6.65' },
      { id: 'f3',  label: 'קומה 3 (דירות 5–6)',   zFloor: 9.80,  zCeil: 12.67, zTop: 12.95, sheet: 'typical', elevText: '+9.80' },
      { id: 'f4',  label: 'קומה 4 · מרוהטת 3D ✨', zFloor: 12.95, zCeil: 15.82, zTop: 16.10, sheet: 'typical', elevText: '+12.95', has3DFurn: true },
      { id: 'f5',  label: 'קומה 5 · מרוהטת 3D ✨', zFloor: 16.10, zCeil: 18.97, zTop: 19.25, sheet: 'typical', elevText: '+16.10', has3DFurn: true },
      { id: 'f6',  label: 'קומה 6 (דירות 11–12)', zFloor: 19.25, zCeil: 22.12, zTop: 22.40, sheet: 'typical', elevText: '+19.25' },
      { id: 'f7',  label: 'קומה 7 (דירות 13–14)', zFloor: 22.40, zCeil: 25.27, zTop: 25.55, sheet: 'typical', elevText: '+22.40' },
      { id: 'f8',  label: 'קומה 8 (דירות 15–16)', zFloor: 25.55, zCeil: 28.42, zTop: 28.70, sheet: 'typical', elevText: '+25.55' },
      { id: 'f9',  label: 'קומה 9 · פנטהאוז 3D 👑', zFloor: 28.70, zCeil: 31.57, zTop: 31.85, sheet: 'penthouse', elevText: '+28.70', has3DFurn: true },
      { id: 'gag', label: 'גג עליון ומגדל יציאה',  zFloor: 31.85, zCeil: 34.55, zTop: 34.55, sheet: 'roof_main', elevText: '+31.85' }
    ];

    const LAYERS_DEF = [
      { id: 'walls',     name: 'קירות חוץ (אבן/טיח לבן + חיפוי חום-נחושת אדריכלי) וקירות פנים', color: '#8c5646', visible: true },
      { id: 'slabs',     name: 'רצפות, תקרות וקרניזים היקפיים (4 חבילות גמר)', color: '#d6dae0', visible: true },
      { id: 'windows',   name: 'חלונות, וויטרינות, ארגזי תריס חום-נחושת ומעקות', color: '#38bdf8', visible: true },
      { id: 'doors',     name: 'דלתות פנים וכניסה + חלונות הדף ממ"ד', color: '#c89d6c', visible: true },
      { id: 'balconies', name: 'מרפסות שמש, מרפסות גג פנטהאוז ומעקות אלומיניום לבן וזכוכית', color: '#fcfdff', visible: true },
      { id: 'pergolas',  name: 'פרגולות פנטהאוז לבנות, רפפות מסתורי כביסה חום-נחושת וקולטים', color: '#784838', visible: true },
      { id: 'furn3d',    name: 'ריהוט פנים תלת-ממדי יוקרתי (קרקע, ק\' 4–5 ופנטהאוז 9)', color: '#d97706', visible: true },
      { id: 'cad2d',     name: 'תוכנית CAD וקטורית 1:50 על הרצפה', color: '#475569', visible: true },
      { id: 'labels',    name: 'שמות ומידות חדרים פנימיות (בס"מ)', color: '#1e293b', visible: true },
      { id: 'site',      name: 'חניון קרקע (6) ומרתף (13+2 אופנועים), רמפות ופיתוח', color: '#94a3b8', visible: true }
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

    const clipPlane = new THREE.Plane(new THREE.Vector3(0, -1, 0), 35.5);
    const clippingPlanes = [clipPlane];

    const aspect = window.innerWidth / window.innerHeight;
    const perspCam = new THREE.PerspectiveCamera(42, aspect, 0.2, 8000);
    const orthoSize = 22;
    const orthoCam = new THREE.OrthographicCamera(-orthoSize * aspect, orthoSize * aspect, orthoSize, -orthoSize, -2000, 6000);
    let activeCam = perspCam;
    let isOrtho = false;

    const hemiLight = new THREE.HemisphereLight(0xfffdf8, 0xd8d0c2, 0.66);
    hemiLight.position.set(0, 120, 0);
    scene.add(hemiLight);

    const dirLight = new THREE.DirectionalLight(0xfffaf0, 0.72);
    dirLight.position.set(48, 82, 42);
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
    fillLight.position.set(-55, 50, -45);
    scene.add(fillLight);

    const nightLightsGroup = new THREE.Group();
    nightLightsGroup.visible = false;
    scene.add(nightLightsGroup);
    [[-10, 16, 0], [10, 16, 0], [-10, 26, 0], [10, 26, 0], [0, 30, 0], [-12, 30, 0], [12, 30, 0], [1, 3, 2]].forEach(([lx, ly, lz]) => {
      const pl = new THREE.PointLight(0xffb454, 1.4, 34, 1.8);
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

    function createTileTexture(bgHex, gridHex, repeatX = 12, repeatY = 6) {
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
      extWall: new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.64, metalness: 0.02, side: THREE.DoubleSide, clippingPlanes }),
      darkSpandrel: new THREE.MeshStandardMaterial({ color: 0x8c5646, roughness: 0.46, metalness: 0.24, side: THREE.DoubleSide, clippingPlanes }),
      wallCap: new THREE.MeshStandardMaterial({ color: 0xd2c7b4, roughness: 0.88, metalness: 0.02, side: THREE.DoubleSide, clippingPlanes }),
      slabFloor: new THREE.MeshStandardMaterial({ map: FINISH_TEXTURES.nordic.map, color: 0xd8dce2, roughness: 0.65, metalness: 0.04, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, clippingPlanes }),
      slabEdge: new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.68, clippingPlanes }),
      terraceFloor: new THREE.MeshStandardMaterial({ color: 0xcbd5e1, roughness: 0.72, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, clippingPlanes }),
      woodDeck: new THREE.MeshStandardMaterial({ map: DECK_TEXTURES.wood, roughness: 0.55, metalness: 0.05, clippingPlanes }),
      glassRailing: new THREE.MeshPhysicalMaterial({ color: 0xe0f2fe, transparent: true, opacity: 0.26, roughness: 0.08, metalness: 0.05, side: THREE.DoubleSide, clippingPlanes }),
      railWhite: new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.30, metalness: 0.45, clippingPlanes }),
      aluDark: new THREE.MeshStandardMaterial({ color: 0x43332e, roughness: 0.36, metalness: 0.55, clippingPlanes }),
      louverGray: new THREE.MeshStandardMaterial({ color: 0x784838, roughness: 0.42, metalness: 0.38, clippingPlanes }),
      winGlass: new THREE.MeshPhysicalMaterial({ color: 0x93c5fd, emissive: 0x0284c7, emissiveIntensity: 0.10, transparent: true, opacity: 0.62, roughness: 0.05, metalness: 0.30, side: THREE.DoubleSide, clippingPlanes }),
      lightWood: new THREE.MeshStandardMaterial({ color: 0xd4ad7d, roughness: 0.52, metalness: 0.04, clippingPlanes }),
      doorFrame: new THREE.MeshStandardMaterial({ color: 0xb0895a, roughness: 0.55, clippingPlanes }),
      mamadSteel: new THREE.MeshStandardMaterial({ color: 0x4a3832, roughness: 0.35, metalness: 0.65, clippingPlanes }),
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

HTML_PART2 = r"""
    // =========================================================================
    // 4. GEOMETRY HELPERS (PRESERVING EXACT 1:1 HAFETZ HAIM 44 ARCHITECTURE)
    // =========================================================================
    function isExteriorWallFace(sheetKey, x1, y1, x2, y2) {
      if (sheetKey === 'roof_main') return true;
      if (sheetKey === 'basement') return false;
      const xm = 0.5 * (x1 + x2);
      const ym = 0.5 * (y1 + y2);
      const tol = 0.085;

      if (sheetKey === 'ground' || sheetKey === 'typical') {
        if (xm <= -13.361 + tol || xm >= 14.359 - tol) return true;
        if (ym <= -5.184 + tol) return true;
        if (xm >= -3.552 - tol && xm <= 7.840 + tol && ym <= -4.220 + tol) return true;
        if ((xm <= -3.361 + tol || xm >= 5.669 - tol) && ym >= 4.216 - tol) return true;
        if (ym >= 5.196 - tol) return true;
        if (ym >= 4.216 - tol && (Math.abs(xm - (-3.361)) <= tol || Math.abs(xm - 5.669) <= tol)) return true;
        return false;
      }

      if (sheetKey === 'penthouse') {
        if (xm <= -10.211 + tol || xm >= 9.599 - tol) return true;
        if (ym <= -5.184 + tol) return true;
        if (xm >= -3.552 - tol && xm <= 7.840 + tol && ym <= -4.220 + tol) return true;
        if ((xm <= -3.361 + tol || xm >= 5.669 - tol) && ym >= 4.216 - tol) return true;
        if (ym >= 5.196 - tol) return true;
        if (ym >= 4.216 - tol && (Math.abs(xm - (-3.361)) <= tol || Math.abs(xm - 5.669) <= tol)) return true;
        return false;
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

    function makeSlopedRampSegment(x0, y0, x1, y1, zAtMin, zAtMax, slopeAxis, thick, mat) {
      // Builds a 3D sloped ramp slab where top surface slopes from zAtMin (at x0 or y0) to zAtMax (at x1 or y1)
      const z00 = zAtMin;
      const z10 = (slopeAxis === 'X') ? zAtMax : zAtMin;
      const z11 = zAtMax;
      const z01 = (slopeAxis === 'X') ? zAtMin : zAtMax;
      const b00 = z00 - thick, b10 = z10 - thick, b11 = z11 - thick, b01 = z01 - thick;
      const pos = [
        // Top face
        x0, z00, y0,  x0, z01, y1,  x1, z11, y1,
        x0, z00, y0,  x1, z11, y1,  x1, z10, y0,
        // Bottom face
        x0, b00, y0,  x1, b11, y1,  x0, b01, y1,
        x0, b00, y0,  x1, b10, y0,  x1, b11, y1,
        // North (y0)
        x0, b00, y0,  x0, z00, y0,  x1, z10, y0,
        x0, b00, y0,  x1, z10, y0,  x1, b10, y0,
        // South (y1)
        x0, b01, y1,  x1, z11, y1,  x0, z01, y1,
        x0, b01, y1,  x1, b11, y1,  x1, z11, y1,
        // West (x0)
        x0, b00, y0,  x0, z01, y1,  x0, z00, y0,
        x0, b00, y0,  x0, b01, y1,  x0, z01, y1,
        // East (x1)
        x1, b10, y0,  x1, z10, y0,  x1, z11, y1,
        x1, b10, y0,  x1, z11, y1,  x1, b11, y1
      ];
      const geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
      geo.computeVertexNormals();
      const m = new THREE.Mesh(geo, mat);
      m.castShadow = true;
      m.receiveShadow = true;
      return m;
    }

    function buildStaircaseFlights3D(floorId, zF, zC) {
      if (floorId === 'gag') return;
      const sGrp = new THREE.Group();
      const zMid = 0.5 * (zF + zC);
      // Intermediate North Landing inside stairwell (X=-1.18..+2.10, Y=+1.94..+2.96)
      sGrp.add(makeBox(-1.18, 1.94, 2.10, 2.96, zMid - 0.16, zMid, MATS.slabFloor));
      const nSteps = 9;
      const stepY0 = 2.96, stepY1 = 4.86;
      const dY = (stepY1 - stepY0) / nSteps;
      const dZ1 = (zMid - zF) / nSteps;
      const dZ2 = (zC - zMid) / nSteps;
      for (let i = 0; i < nSteps; i++) {
        // Flight 1 (East half: X=+0.52..+2.08): rises from South landing (Y=4.86) to North mid-landing (Y=2.96)
        const sy1_a = stepY1 - (i + 1) * dY;
        const sy1_b = stepY1 - i * dY;
        const sz1 = zF + (i + 1) * dZ1;
        sGrp.add(makeBox(0.52, sy1_a, 2.08, sy1_b, sz1 - dZ1 - 0.08, sz1, MATS.slabFloor));
        // Flight 2 (West half: X=-1.16..+0.40): rises from North mid-landing (Y=2.96) to South upper landing (Y=4.86)
        const sy2_a = stepY0 + i * dY;
        const sy2_b = stepY0 + (i + 1) * dY;
        const sz2 = zMid + (i + 1) * dZ2;
        sGrp.add(makeBox(-1.16, sy2_a, 0.40, sy2_b, sz2 - dZ2 - 0.08, sz2, MATS.slabFloor));
      }
      // Central stairwell divider guardrail (X=+0.42..+0.50, Y=+2.96..+4.86)
      sGrp.add(makeBox(0.42, 2.96, 0.50, 4.86, zF + 0.20, zC - 0.10, MATS.railWhite, false));
      addToFloorAndLayer(floorId, 'slabs', sGrp);
    }

    function makeExteriorOpeningWallBox(x0, y0, x1, y1, z0, z1, orient, useDarkSpandrel = false) {
      const xm = 0.5 * (x0 + x1);
      const ym = 0.5 * (y0 + y1);
      const extMat = useDarkSpandrel ? MATS.darkSpandrel : MATS.extWall;
      let matPX = MATS.wall, matNX = MATS.wall, matPZ = MATS.wall, matNZ = MATS.wall;
      let bx0 = x0, by0 = y0, bx1 = x1, by1 = y1;
      const proud = useDarkSpandrel ? 0.015 : 0.0;
      if (orient === 'H') {
        if (ym > 0.0) { matPZ = extMat; by1 += proud; }
        else { matNZ = extMat; by0 -= proud; }
      } else {
        if (xm > 0.0) { matPX = extMat; bx1 += proud; }
        else { matNX = extMat; bx0 -= proud; }
      }
      return makeBox(bx0, by0, bx1, by1, z0, z1, [matPX, matNX, MATS.wallCap, MATS.wallCap, matPZ, matNZ]);
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

      // Spandrel rule per Hafetz Haim 44 Architectural Renderings:
      // - Primary walls and sill walls below standard windows (zFloor..zSill=1.05m) are crisp white plaster/HPL (useDarkBelow=false).
      // - Recessed tall-window bays (win_tall) have warm copper-brown HPL spandrels below sill and above header.
      // - Roller-shutter header boxes / lintel panels above balcony vitrines and main windows are warm copper-brown HPL (useDarkAbove=true).
      // - Small square bathroom/service windows on North facade (span < 0.85m) and North Central Mamad Core (-2.85 <= midX <= 3.85) are all-white.
      const isCentralCoreNorth = (orient === 'H' && midY < 0.0 && midX >= -2.85 && midX <= 3.85);
      const isLaundryInnerWall = (orient === 'H' && Math.abs(midY - (-4.334)) <= 0.22);
      const isSmallNorthBathWin = (orient === 'H' && midY < 0.0 && span < 0.85);
      const useDarkBelow = (kind === 'win_tall') && !isCentralCoreNorth && !isLaundryInnerWall;
      const useDarkAbove = (orient === 'V') || ((orient === 'H') && !isCentralCoreNorth && !isLaundryInnerWall && !isSmallNorthBathWin);

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
          const outY = (midY < 0.0) ? (y0 - 0.02) : (y1 + 0.02);
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
          const outX = (midX < 0.0) ? (x0 - 0.02) : (x1 + 0.02);
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
        // Mamad windows sit in the white plaster central North core (useDarkSpandrel = false)
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
      const sDepth = thickFascia ? 0.42 : 0.26;
      const curbH = thickFascia ? 0.22 : 0.14;
      bGrp.add(makeBox(x0 - 0.06, y0 - 0.06, x1 + 0.06, y1 + 0.06, zFloor - sDepth, zFloor - 0.03, MATS.extWall));
      bGrp.add(makeBox(x0, y0, x1, y1, zFloor - 0.03, zFloor + 0.01, MATS.woodDeck));

      const zRailTop = zFloor + railHeight;
      const cMat = MATS.extWall;
      const rMat = MATS.railWhite || MATS.extWall;
      openSides.forEach(side => {
        if (side === 'W') {
          bGrp.add(makeBox(x0, y0, x0 + 0.14, y1, zFloor, zFloor + curbH, cMat, false));
          bGrp.add(makeBox(x0 + 0.03, y0 + 0.03, x0 + 0.06, y1 - 0.03, zFloor + curbH, zRailTop - 0.03, MATS.glassRailing, false));
          bGrp.add(makeBox(x0 + 0.01, y0, x0 + 0.08, y1, zRailTop - 0.035, zRailTop, rMat, false));
          for (let py = y0 + 0.15; py < y1 - 0.10; py += 0.24) {
            bGrp.add(makeBox(x0 + 0.02, py - 0.01, x0 + 0.07, py + 0.01, zFloor + curbH, zRailTop - 0.03, rMat, false));
          }
        } else if (side === 'E') {
          bGrp.add(makeBox(x1 - 0.14, y0, x1, y1, zFloor, zFloor + curbH, cMat, false));
          bGrp.add(makeBox(x1 - 0.06, y0 + 0.03, x1 - 0.03, y1 - 0.03, zFloor + curbH, zRailTop - 0.03, MATS.glassRailing, false));
          bGrp.add(makeBox(x1 - 0.08, y0, x1 - 0.01, y1, zRailTop - 0.035, zRailTop, rMat, false));
          for (let py = y0 + 0.15; py < y1 - 0.10; py += 0.24) {
            bGrp.add(makeBox(x1 - 0.07, py - 0.01, x1 - 0.02, py + 0.01, zFloor + curbH, zRailTop - 0.03, rMat, false));
          }
        } else if (side === 'N') {
          bGrp.add(makeBox(x0, y0, x1, y0 + 0.14, zFloor, zFloor + curbH, cMat, false));
          bGrp.add(makeBox(x0 + 0.03, y0 + 0.03, x1 - 0.03, y0 + 0.06, zFloor + curbH, zRailTop - 0.03, MATS.glassRailing, false));
          bGrp.add(makeBox(x0, y0 + 0.01, x1, y0 + 0.08, zRailTop - 0.035, zRailTop, rMat, false));
          for (let px = x0 + 0.15; px < x1 - 0.10; px += 0.24) {
            bGrp.add(makeBox(px - 0.01, y0 + 0.02, px + 0.01, y0 + 0.07, zFloor + curbH, zRailTop - 0.03, rMat, false));
          }
        } else if (side === 'S') {
          bGrp.add(makeBox(x0, y1 - 0.14, x1, y1, zFloor, zFloor + curbH, cMat, false));
          bGrp.add(makeBox(x0 + 0.03, y1 - 0.06, x1 - 0.03, y1 - 0.03, zFloor + curbH, zRailTop - 0.03, MATS.glassRailing, false));
          bGrp.add(makeBox(x0, y1 - 0.08, x1, y1 - 0.01, zRailTop - 0.035, zRailTop, rMat, false));
          for (let px = x0 + 0.15; px < x1 - 0.10; px += 0.24) {
            bGrp.add(makeBox(px - 0.01, y1 - 0.07, px + 0.01, y1 - 0.02, zFloor + curbH, zRailTop - 0.03, rMat, false));
          }
        }
      });

      addToFloorAndLayer(floorId, 'balconies', bGrp);
      if (hasPergola) buildLightPergola(floorId, x0, y0, x1, y1, zFloor + 2.75);
    }

    function buildLightPergola(floorId, x0, y0, x1, y1, zPergola, zFloorSupport = null) {
      const pGrp = new THREE.Group();
      const fH = 0.40, fW = 0.24;
      // Crisp white architectural concrete perimeter beam (+31.45..+31.85m) + warm wood-look louvers inside
      pGrp.add(makeBox(x0, y0, x1, y0 + fW, zPergola, zPergola + fH, MATS.extWall));
      pGrp.add(makeBox(x0, y1 - fW, x1, y1, zPergola, zPergola + fH, MATS.extWall));
      pGrp.add(makeBox(x0, y0, x0 + fW, y1, zPergola, zPergola + fH, MATS.extWall));
      pGrp.add(makeBox(x1 - fW, y0, x1, y1, zPergola, zPergola + fH, MATS.extWall));
      if (typeof zFloorSupport === 'number') {
        // Outer corner concrete columns (25x55cm) supporting the Penthouse pergola beam per Garmushka Section B-B
        const isWest = (x0 < 0);
        const cx0 = isWest ? x0 : (x1 - 0.25);
        const cx1 = isWest ? (x0 + 0.25) : x1;
        pGrp.add(makeBox(cx0, y0, cx1, y0 + 0.55, zFloorSupport, zPergola + fH, MATS.extWall));
        pGrp.add(makeBox(cx0, y1 - 0.55, cx1, y1, zFloorSupport, zPergola + fH, MATS.extWall));
      }
      for (let y = y0 + 0.34; y < y1 - 0.22; y += 0.26) {
        pGrp.add(makeBox(x0 + fW, y, x1 - fW, y + 0.08, zPergola + 0.08, zPergola + fH - 0.06, MATS.luxOakSmooth, false));
      }
      addToFloorAndLayer(floorId, 'pergolas', pGrp);
    }

    function buildNorthLaundryLouvers(floorId, zF, zC, shafts) {
      const lGrp = new THREE.Group();
      shafts.forEach(([lx0, lx1, ly0, ly1]) => {
        // Warm copper-brown vertical frame posts & recessed shadow backing plate (matching North-East rendering)
        lGrp.add(makeBox(lx0, ly0 - 0.02, lx0 + 0.06, ly0 + 0.08, zF - 0.28, zC, MATS.darkSpandrel, false));
        lGrp.add(makeBox(lx1 - 0.06, ly0 - 0.02, lx1, ly0 + 0.08, zF - 0.28, zC, MATS.darkSpandrel, false));
        lGrp.add(makeBox(lx0 + 0.04, ly0 + 0.03, lx1 - 0.04, ly0 + 0.07, zF - 0.28, zC, MATS.aluDark, false));
        // Full-height horizontal warm copper-brown aluminum louvers across floor + slab band
        for (let z = zF - 0.26; z < zC - 0.04; z += 0.11) {
          lGrp.add(makeBox(lx0 + 0.02, ly0 - 0.03, lx1 - 0.02, ly0 + 0.035, z, z + 0.055, MATS.louverGray, false));
        }
      });
      addToFloorAndLayer(floorId, 'pergolas', lGrp);
    }

    // =========================================================================
    // 5. BUILD ALL FLOORS + 19 PARKING STALLS (6 GROUND + 13 BASEMENT)
    // =========================================================================
    let parkingHighlightMesh = null;

    function createParkingStallMesh(st) {
      const grp = new THREE.Group();
      const zP = (st.level === 'basement') ? -5.08 : 0.025;
      const isMoto = (st.vehicleType === 'motorcycle');
      const isAcc = Boolean(st.accessible);
      const c = document.createElement('canvas');
      c.width = 256; c.height = 128; // Landscape canvas matching 5.00m x 2.40m stalls
      const ctx = c.getContext('2d');
      ctx.fillStyle = isAcc
        ? 'rgba(3, 105, 161, 0.72)'
        : (isMoto ? 'rgba(15, 118, 110, 0.70)' : ((st.level === 'basement') ? 'rgba(30, 41, 59, 0.68)' : 'rgba(15, 23, 42, 0.55)'));
      ctx.fillRect(6, 6, 244, 116);
      ctx.strokeStyle = isAcc ? '#38bdf8' : (isMoto ? '#2dd4bf' : '#fbbf24');
      ctx.lineWidth = 5;
      ctx.strokeRect(6, 6, 244, 116);
      ctx.fillStyle = '#ffffff';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      if (isMoto) {
        ctx.font = 'bold 24px "Segoe UI", sans-serif';
        ctx.fillText('🏍️ אופנוע #' + st.num, 128, 64);
      } else if (isAcc) {
        ctx.font = 'bold 30px "Segoe UI", sans-serif';
        ctx.fillText('♿ P-' + st.num + ' נכה', 128, 64);
      } else {
        ctx.font = 'bold 36px "Segoe UI", sans-serif';
        ctx.fillText('P-' + st.num, 128, 64);
      }
      const tex = new THREE.CanvasTexture(c);
      const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, side: THREE.DoubleSide, clippingPlanes });
      const geo = new THREE.PlaneGeometry(st.w, st.d);
      geo.rotateX(-Math.PI / 2);
      const m = new THREE.Mesh(geo, mat);
      m.position.set(st.x, zP, st.y);
      grp.add(m);

      // If stall has an adjacent Accessible Transfer Zone (מעבר נכה 130 ס"מ בין חניות 18-19), render hatched zone
      if (isAcc && st.aisleD && typeof st.aisleY === 'number') {
        const ac = document.createElement('canvas');
        ac.width = 256; ac.height = 64;
        const actx = ac.getContext('2d');
        actx.fillStyle = 'rgba(2, 132, 199, 0.28)';
        actx.fillRect(0, 0, 256, 64);
        actx.strokeStyle = '#38bdf8';
        actx.lineWidth = 4;
        actx.strokeRect(2, 2, 252, 60);
        for (let sx = -64; sx < 256; sx += 24) {
          actx.beginPath(); actx.moveTo(sx, 64); actx.lineTo(sx + 48, 0); actx.stroke();
        }
        const atex = new THREE.CanvasTexture(ac);
        const amat = new THREE.MeshBasicMaterial({ map: atex, transparent: true, depthWrite: false, side: THREE.DoubleSide, clippingPlanes });
        const ageo = new THREE.PlaneGeometry(st.w, st.aisleD);
        ageo.rotateX(-Math.PI / 2);
        const am = new THREE.Mesh(ageo, amat);
        am.position.set(st.x, zP, st.aisleY);
        grp.add(am);
      }
      return grp;
    }

    function buildFloorSlabsAndBalconies(f) {
      const zF = f.zFloor;
      const sThick = 0.28;

      if (f.id === 'mar') {
        // Exact Basement -1 (-5.10m) footprint per CAD: X=[-17.721..+18.508] (36.23m), Y=[-9.202..+9.048] (18.25m)
        // with South-East cutout at X=[+14.249..+18.508], Y=[+3.600..+9.048] (4.26m x 5.45m for Infiltration Pit K)
        const marSlabPts = [
          [-17.721, -9.202], [18.508, -9.202], [18.508, 3.600],
          [14.249, 3.600], [14.249, 9.048], [-17.721, 9.048]
        ];
        addToFloorAndLayer('mar', 'site', buildPolygonSlab(marSlabPts, -5.50, -5.10, MATS.basementConcrete, MATS.basementConcrete));

        // 3D Multi-Segment Sloped Vehicle Ramp arriving in Basement (+45.63 -> +44.18 -> +43.78 -> +42.80 = -5.10m)
        const marRampGrp = new THREE.Group();
        const rampAsphaltMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.85, metalness: 0.05, clippingPlanes });
        // 1. South-East Ramp Arrival (X=-1.47..+7.45, Y=+5.50..+8.44): slopes Eastward from z=-2.27m down to z=-3.72m (+44.18)
        marRampGrp.add(makeSlopedRampSegment(-1.47, 5.50, 7.45, 8.44, -2.27, -3.72, 'X', 0.28, rampAsphaltMat));
        // 2. South-East Turning Platform (+44.18 => z=-3.72m at X=+7.45..+13.01, Y=+3.10..+8.44)
        marRampGrp.add(makeBox(7.45, 3.10, 13.01, 8.44, -4.00, -3.72, rampAsphaltMat));
        // 3. East Aisle Ramp (5% slope Northward, X=+7.45..+13.01, Y=-5.66..+3.10): z=-4.12m (+43.78) at North to z=-3.72m (+44.18) at South
        marRampGrp.add(makeSlopedRampSegment(7.45, -5.66, 13.01, 3.10, -4.12, -3.72, 'Y', 0.28, rampAsphaltMat));
        // 4. North-East Turning Platform (+43.78 => z=-4.12m at X=+7.45..+13.01, Y=-8.60..-5.66)
        marRampGrp.add(makeBox(7.45, -8.60, 13.01, -5.66, -4.40, -4.12, rampAsphaltMat));
        // 5. North Ramp (11% slope Westward, X=-6.25..+7.45, Y=-8.60..-5.66): z=-5.10m (+42.80) at West to z=-4.12m (+43.78) at East
        marRampGrp.add(makeSlopedRampSegment(-6.25, -8.60, 7.45, -5.66, -5.10, -4.12, 'X', 0.28, rampAsphaltMat));
        addToFloorAndLayer('mar', 'site', marRampGrp);

        const stallsGrp = new THREE.Group();
        PARKING_STALLS.filter(s => s.level === 'basement').forEach(st => {
          stallsGrp.add(createParkingStallMesh(st));
        });
        addToFloorAndLayer('mar', 'site', stallsGrp);
        return;
      }

      if (f.id === 'kar') {
        const siteGrp = new THREE.Group();
        // 1. Residential Net Lot 85-2 (38.82m x 18.40m = 714 sqm): X=[-19.411..+19.409], Y=[-9.202..+9.196]
        siteGrp.add(makeBox(-19.411, -9.202, 19.409, 9.196, -0.06, -0.01, MATS.sidewalk));

        // 2. Front Pedestrians Entry & Gardens along East Setback (X=+14.359..+19.409, 5.05m setback to Lot Line)
        // North-East Front Garden (גינון חזית צפון-מזרח: X=+14.41..+19.31, Y=-4.50..-0.24)
        siteGrp.add(makeBox(14.41, -4.50, 19.31, -0.24, -0.01, 0.08, MATS.grass));
        // Main Lobby Entry Walkway with 6 Architectural Steps from Street (+47.70) to Lobby (±0.00 = +47.90)
        // CAD steps at Y = -0.240 .. +1.471, X = +14.109 .. +19.409
        siteGrp.add(makeBox(14.109, -0.24, 19.409, 1.47, -0.01, 0.03, MATS.luxTravertine));
        // South-East Front Garden & Infiltration Pit K (גינון חזית דרום-מזרח: X=+14.41..+19.31, Y=+1.47..+9.10)
        siteGrp.add(makeBox(14.41, 1.47, 19.31, 9.10, -0.01, 0.08, MATS.grass));
        // South-East Garden Strip East of the covered ramp mouth (X=+7.75..+14.41, Y=+5.25..+9.00)
        siteGrp.add(makeBox(7.75, 5.25, 14.41, 9.00, -0.01, 0.08, MATS.grass));
        // West Rear Garden strips flanking Stalls #2-#6 (X=-19.21..-16.90, Y=-9.00..+9.00)
        siteGrp.add(makeBox(-19.21, -9.00, -16.90, 9.00, -0.01, 0.08, MATS.grass));

        // 3. Vehicle Driveway & 3D Sloped Basement Ramp (רמפת ירידה למרתף לאורך גבול צפוני, מערב ודרום):
        const asphaltMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.88, metalness: 0.05, clippingPlanes });
        const curbMat = new THREE.MeshStandardMaterial({ color: 0xcbd5e1, roughness: 0.65, metalness: 0.05, clippingPlanes });
        const markRedMat = new THREE.MeshBasicMaterial({ color: 0xef4444, transparent: true, opacity: 0.85, side: THREE.DoubleSide, clippingPlanes });
        const markBlueMat = new THREE.MeshBasicMaterial({ color: 0x0284c7, transparent: true, opacity: 0.85, side: THREE.DoubleSide, clippingPlanes });

        // North entry driveway from Hafetz Haim St (X=-6.35..+19.41, Y=-9.00..-5.45)
        siteGrp.add(makeSlopedRampSegment(-6.35, -9.00, 19.41, -5.45, -0.32, 0.01, 'X', 0.18, asphaltMat));
        // West turning aisle for Ground Stalls #2-#6 (X=-11.90..-6.35, Y=-9.00..+5.50, width 5.55m)
        siteGrp.add(makeSlopedRampSegment(-11.90, -9.00, -6.35, 5.50, -0.32, -0.50, 'Y', 0.18, asphaltMat));
        // South-West turning corner into South Ramp Trench (X=-11.90..-6.35, Y=+5.50..+8.44)
        siteGrp.add(makeBox(-11.90, 5.50, -6.35, 8.44, -0.68, -0.50, asphaltMat));
        // South 3D Sloped Ramp Descending Eastward inside Concrete Trench (Y=+5.50..+8.44):
        // Segment 1 (10% slope, X=-6.35..-3.35): z=-0.50m -> -0.80m
        siteGrp.add(makeSlopedRampSegment(-6.35, 5.50, -3.35, 8.44, -0.50, -0.80, 'X', 0.25, asphaltMat));
        // Segment 2 (15% slope, X=-3.35..+6.45): z=-0.80m -> -2.27m (+45.63)
        siteGrp.add(makeSlopedRampSegment(-3.35, 5.50, 6.45, 8.44, -0.80, -2.27, 'X', 0.25, asphaltMat));
        // Segment 3 (10% transition under Ground slab, X=+6.45..+7.71): z=-2.27m -> -2.42m
        siteGrp.add(makeSlopedRampSegment(6.45, 5.50, 7.71, 8.44, -2.27, -2.42, 'X', 0.25, asphaltMat));
        // Concrete Trench Retaining Side Walls & Safety Parapets (H=1.15m above ground down to ramp soffit)
        siteGrp.add(makeBox(-6.35, 5.20, 7.71, 5.50, -2.50, 1.15, MATS.extWall));
        siteGrp.add(makeBox(-6.35, 8.44, 7.71, 8.74, -2.50, 1.15, MATS.extWall));

        // Ground Floor Sunken Trash Room slab (+47.22 = -0.68m at X=-1.25..+2.25, Y=-4.63..-0.13)
        siteGrp.add(makeBox(-1.25, -4.63, 2.25, -0.13, -0.88, -0.68, MATS.terraceFloor));
        // Gas Room slab (+46.45 / -0.32m at X=-5.26..-3.36, Y=+1.42..+4.22)
        siteGrp.add(makeBox(-5.26, 1.42, -3.36, 4.22, -0.55, -0.32, MATS.terraceFloor));
        // West Covered Passage & 8 Exterior Steps (8x17/27 at X=-5.26..-3.10, Y=-0.12..+1.42)
        for (let st = 0; st < 8; st++) {
          const sx0 = -3.10 - (st + 1) * (2.16 / 8.0);
          const sx1 = -3.10 - st * (2.16 / 8.0);
          const szTop = -st * 0.04;
          siteGrp.add(makeBox(sx0, -0.12, sx1, 1.42, -0.50, szTop, MATS.luxTravertine));
        }
        // North-West Basement Ventilation Grate (אוורור חניון מערבי 150x441 at X=-5.86..-1.25, Y=-4.92..-3.02)
        siteGrp.add(makeBox(-5.66, -4.72, -1.45, -3.22, -0.32, -0.22, MATS.aluDark));
        // North-East Basement Ventilation Grate (אוורור חניון מזרחי 530x228 at X=+8.81..+14.11, Y=-5.00..-2.38)
        siteGrp.add(makeBox(8.95, -4.90, 14.00, -2.50, 0.01, 0.06, MATS.aluDark));

        // 4. Perimeter Stone Lot Walls (גדר אבן היקפית בגבול מגרש 85-2: X=-19.411..+19.409, Y=-9.202..+9.196)
        // North wall (from X=-19.411 to +19.409 at Y=-9.202..-9.00)
        siteGrp.add(makeBox(-19.411, -9.202, 19.409, -9.00, 0.00, 1.15, MATS.extWall));
        // South wall (from X=-19.411 to +19.409 at Y=+9.00..+9.196)
        siteGrp.add(makeBox(-19.411, 9.00, 19.409, 9.196, 0.00, 1.15, MATS.extWall));
        // West wall (at X=-19.411..-19.21, Y=-9.202..+9.196)
        siteGrp.add(makeBox(-19.411, -9.202, -19.21, 9.196, 0.00, 1.15, MATS.extWall));
        // East Front Low Wall along New Lot Line X=+19.409 (with openings for vehicle gate Y=-9.00..-4.60 and pedestrian lobby entry Y=-0.24..+1.47)
        siteGrp.add(makeBox(19.21, -4.60, 19.409, -0.24, 0.00, 1.10, MATS.extWall));
        siteGrp.add(makeBox(19.21,  1.47, 19.409,  9.196, 0.00, 1.10, MATS.extWall));

        // 5. East Expropriation Strip 85-1 (הפקעה לדרך 5.38 מ': X=+19.409..+24.789) & Hafetz Haim Street (רחוב חפץ חיים: X=+24.789..+32.789)
        // Sidewalk & Future Road Widening Strip (X=+19.409..+24.789, Y=-18.00..+18.00)
        siteGrp.add(makeBox(19.409, -18.00, 24.789, 18.00, -0.18, -0.02, MATS.sidewalk));
        siteGrp.add(makeBox(24.64, -18.00, 24.789, 18.00, -0.18, 0.01, curbMat));
        // Hafetz Haim Street Asphalt Roadway (6.00m carriageway + 2.00m East sidewalk: X=+24.789..+30.789, Y=-18.00..+18.00)
        siteGrp.add(makeBox(24.789, -18.00, 30.789, 18.00, -0.24, -0.12, asphaltMat));
        // White dashed road center-line markings along Hafetz Haim Street (X=+27.789)
        for (let ry = -16.0; ry <= 14.0; ry += 4.0) {
          siteGrp.add(makeBox(27.72, ry, 27.86, ry + 2.2, -0.118, -0.112, MATS.extWall));
        }
        // Opposite (East) Sidewalk of Hafetz Haim St (X=+30.789..+32.789)
        siteGrp.add(makeBox(30.789, -18.00, 30.94, 18.00, -0.18, 0.01, curbMat));
        siteGrp.add(makeBox(30.789, -18.00, 32.789, 18.00, -0.18, -0.02, MATS.sidewalk));

        // 6. West Public Open Space Strip 85-3 (שצ"פ מערבי ברוחב 13.95 מ': X=-33.361..-19.411, Y=-9.202..+9.196)
        siteGrp.add(makeBox(-33.361, -9.202, -19.411, 9.196, -0.10, -0.01, MATS.grass));

        // 7. CAD Setback & Lot Boundary Indicator Lines on Ground Plane (קווי בניין וגבול מגרש)
        // Red Lot 85-2 perimeter outline (-19.411..+19.409, -9.202..+9.196)
        siteGrp.add(makeBox(-19.43, -9.22, 19.43, -9.16, 0.02, 0.03, markRedMat));
        siteGrp.add(makeBox(-19.43,  9.16, 19.43,  9.22, 0.02, 0.03, markRedMat));
        // Blue Building Setback Lines (קו בניין קדמי מזרחי 5.05 מ' ממרפסת/3.05 מ', קו בניין צדי 4.00 מ' ב-Y=-5.184 ו-Y=+5.196, קו בניין מערבי 6.05 מ' ב-X=-13.361)
        siteGrp.add(makeBox(-13.38, -5.20, 14.38, -5.15, 0.02, 0.03, markBlueMat));
        siteGrp.add(makeBox(-13.38,  5.17, 14.38,  5.22, 0.02, 0.03, markBlueMat));

        // 8. 6 Ground-level parking stalls (#1..#6) at exact CAD coordinates
        PARKING_STALLS.filter(s => s.level === 'ground').forEach(st => {
          siteGrp.add(createParkingStallMesh(st));
        });

        // 9. Enclosed Ground Floor building slab (±0.00 = +47.90, excluding West open Pilotis parking & sunken Trash Room)
        const gSlabPts = [
          [2.250, -4.633], [5.461, -4.633], [5.461, -5.184], [14.359, -5.184],
          [14.359, 4.216], [5.669, 4.216], [5.669, 5.196], [-3.361, 5.196],
          [-3.361, 1.415], [-3.100, 1.415], [-3.100, -0.130], [2.250, -0.130]
        ];
        addToFloorAndLayer('kar', 'slabs', buildPolygonSlab(gSlabPts, -0.25, 0.00, MATS.slabFloor, MATS.slabEdge));
        addToFloorAndLayer('kar', 'site', siteGrp);
        return;
      }

      if (f.id === 'gag') {
        const gagPts = [
          [-10.211, -5.184], [10.355, -5.184], [10.355, -4.434],
          [9.599, -4.434], [9.599, 4.216], [5.669, 4.216],
          [5.669, 5.196], [-3.361, 5.196], [-3.361, 4.216], [-10.211, 4.216]
        ];
        addToFloorAndLayer('gag', 'slabs', buildPolygonSlab(gagPts, 31.57, 31.85, MATS.terraceFloor, MATS.extWall));
        // Roof perimeter parapet (מעקה גג בנוי עד +32.95)
        const pGrp = new THREE.Group();
        pGrp.add(makeBox(-10.211, -5.184, 10.355, -4.95, 31.85, 32.95, MATS.extWall));
        pGrp.add(makeBox(-10.211, -5.184, -9.96, 4.216, 31.85, 32.95, MATS.extWall));
        pGrp.add(makeBox(9.35, -4.434, 9.599, 4.216, 31.85, 32.95, MATS.extWall));
        pGrp.add(makeBox(-10.211, 3.98, -3.361, 4.216, 31.85, 32.95, MATS.extWall));
        pGrp.add(makeBox(5.669, 3.98, 9.599, 4.216, 31.85, 32.95, MATS.extWall));
        // Top cap of staircase & elevator tower at +34.55m
        pGrp.add(makeBox(-1.48, 1.64, 2.42, 5.24, 34.30, 34.55, MATS.extWall));
        addToFloorAndLayer('gag', 'walls', pGrp);

        // Solar panels array on Main Roof (+31.85m)
        const solarGrp = new THREE.Group();
        [[-8.2, -3.2], [-5.6, -3.2], [-8.2, 0.4], [-5.6, 0.4], [4.2, -3.2], [6.8, -3.2], [4.2, 0.4], [6.8, 0.4]].forEach(([sx, sy]) => {
          solarGrp.add(makeBox(sx, sy, sx + 1.8, sy + 2.1, 31.85, 32.65, MATS.solarPanel));
        });
        addToFloorAndLayer('gag', 'pergolas', solarGrp);
        return;
      }

      if (['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8'].includes(f.id)) {
        const typPts = [
          [-13.361, -5.184], [-3.548, -5.184], [-3.548, -4.430],
          [-1.050, -4.430], [-1.050, -4.633], [5.461, -4.633],
          [5.461, -4.430], [7.840, -4.430], [7.840, -5.184],
          [14.359, -5.184], [14.359, 4.216], [5.669, 4.216],
          [5.669, 5.196], [-3.361, 5.196], [-3.361, 4.216], [-13.361, 4.216]
        ];
        addToFloorAndLayer(f.id, 'slabs', buildPolygonSlab(typPts, zF - sThick, zF, MATS.slabFloor, MATS.extWall));

        // Continuous white architectural perimeter cornice (קרניז לבן היקפי בולט 10 ס"מ)
        const cornGrp = new THREE.Group();
        cornGrp.add(makeBox(-13.46, -5.28, 14.46, -5.10, zF - sThick, zF + 0.02, MATS.extWall));
        cornGrp.add(makeBox(-13.46, 4.14, 14.46, 4.32, zF - sThick, zF + 0.02, MATS.extWall));
        cornGrp.add(makeBox(-3.46, 5.12, 5.76, 5.30, zF - sThick, zF + 0.02, MATS.extWall));
        addToFloorAndLayer(f.id, 'slabs', cornGrp);

        // West Sun Balcony (-15.361 .. -13.361, y=-5.184..4.216) & East Sun Balcony (14.359 .. 16.359, y=-5.184..4.216)
        buildBalconyBox(f.id, -15.361, -5.184, -13.361, 4.216, zF, ['W', 'N', 'S'], false, 1.05, false);
        buildBalconyBox(f.id, 14.359, -5.184, 16.359, 4.216, zF, ['E', 'N', 'S'], false, 1.05, false);

        // Outer Balcony Architectural Concrete Frame Columns & Perimeter Beams (per Garmushka Sections A-A/B-B & 3D Renders)
        const bFrameGrp = new THREE.Group();
        const zC = f.zCeil;
        // West Balcony outer corner columns (X=-15.361..-15.11, Y=-5.184..-4.63 & Y=+3.66..+4.216)
        bFrameGrp.add(makeBox(-15.361, -5.184, -15.11, -4.63, zF, zC, MATS.extWall));
        bFrameGrp.add(makeBox(-15.361,  3.66,  -15.11,  4.216, zF, zC, MATS.extWall));
        // East Balcony outer corner columns (X=+16.11..+16.359, Y=-5.184..-4.63 & Y=+3.66..+4.216)
        bFrameGrp.add(makeBox(16.11, -5.184, 16.359, -4.63, zF, zC, MATS.extWall));
        bFrameGrp.add(makeBox(16.11,  3.66,  16.359,  4.216, zF, zC, MATS.extWall));
        addToFloorAndLayer(f.id, 'balconies', bFrameGrp);

        // North Facade Laundry Shaft Louvers (מסתורי כביסה מערבי ומזרחי)
        buildNorthLaundryLouvers(f.id, zF, f.zCeil, [
          [-3.548, -1.250, -5.184, -4.430],
          [5.664, 7.840, -5.184, -4.430]
        ]);
        return;
      }

      if (f.id === 'f9') {
        // Penthouse Enclosed Footprint Slab
        const phPts = [
          [-10.211, -5.184], [-3.548, -5.184], [-3.548, -4.430],
          [-1.050, -4.430], [-1.050, -4.633], [5.461, -4.633],
          [5.461, -4.430], [7.840, -4.430], [7.840, -5.184],
          [10.355, -5.184], [10.355, -4.434], [9.599, -4.434],
          [9.599, 4.216], [5.669, 4.216], [5.669, 5.196],
          [-3.361, 5.196], [-3.361, 4.216], [-10.211, 4.216]
        ];
        addToFloorAndLayer('f9', 'slabs', buildPolygonSlab(phPts, zF - 0.36, zF, MATS.slabFloor, MATS.extWall));

        // West Roof Terrace (-13.361 .. -10.211, y=-5.184..4.216 -> 295x940cm = 28.15 sqm per Garmushka) with Full Concrete Frame Pergola
        buildBalconyBox('f9', -13.361, -5.184, -10.211, 4.216, zF, ['W', 'N', 'S'], false, 1.15, true);
        buildLightPergola('f9', -13.361, -5.184, -10.211, 4.216, zF + 2.75, zF);

        // East Roof Terrace (9.599 .. 14.359, y=-5.184..4.216 -> 456x940cm = 44.81 sqm per Garmushka) with Full Concrete Frame Pergola
        buildBalconyBox('f9', 9.599, -5.184, 14.359, 4.216, zF, ['E', 'N', 'S'], false, 1.15, true);
        buildLightPergola('f9', 9.599, -5.184, 14.359, 4.216, zF + 2.75, zF);

        // Penthouse North Laundry Shaft Louvers (matching North Elevation up to +31.85m)
        buildNorthLaundryLouvers('f9', zF, f.zCeil, [
          [-3.548, -1.250, -5.184, -4.430],
          [5.664, 7.840, -5.184, -4.430]
        ]);
        return;
      }
    }

    // Highlight box for selected unit's parking stall (works in both Basement and Ground Floor)
    const hlGeo = new THREE.BoxGeometry(4.85, 1.45, 2.35);
    const hlMat = new THREE.MeshBasicMaterial({ color: 0x10b981, transparent: true, opacity: 0.48 });
    parkingHighlightMesh = new THREE.Mesh(hlGeo, hlMat);
    parkingHighlightMesh.visible = false;
    scene.add(parkingHighlightMesh);

    // =========================================================================
    // 5B. EXACT 1:1 CAD-ALIGNED 3D LUXURY INTERIOR MODELING ENGINE
    //     Every sofa, bed, nightstand, dining table, chair, kitchen counter,
    //     island, wardrobe, desk, bathtub, shower, vanity, and WC is positioned
    //     at the exact (X, Y) coordinates drawn on the CAD floor plans.
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

    // 1. 3-Seater Sofa with back along 'N' or 'S' wall
    function addCADSofa3Seat(grp, x0, y0, x1, y1, zF, backDir = 'S') {
      const w = x1 - x0;
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.02, zF + 0.11, MATS.luxOakSmooth));
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.11, zF + 0.41, MATS.luxBoucle));
      const cStep = (w - 0.32) / 3.0;
      for (let i = 0; i < 3; i++) {
        const cx0 = x0 + 0.16 + i * cStep;
        grp.add(makeBox(cx0 + 0.01, y0 + 0.04, cx0 + cStep - 0.01, y1 - 0.04, zF + 0.41, zF + 0.46, MATS.luxBoucle));
      }
      const by0 = (backDir === 'S') ? (y1 - 0.18) : y0;
      const by1 = (backDir === 'S') ? y1 : (y0 + 0.18);
      grp.add(makeBox(x0, by0, x1, by1, zF + 0.41, zF + 0.78, MATS.luxBoucle));
      grp.add(makeBox(x0, y0, x0 + 0.16, y1, zF + 0.41, zF + 0.64, MATS.luxBoucle));
      grp.add(makeBox(x1 - 0.16, y0, x1, y1, zF + 0.41, zF + 0.64, MATS.luxBoucle));
      const py0 = (backDir === 'S') ? (by0 - 0.14) : by1;
      const py1 = (backDir === 'S') ? by0 : (by1 + 0.14);
      grp.add(makeBox(x0 + 0.22, py0, x0 + 0.65, py1, zF + 0.45, zF + 0.72, MATS.luxTaupe));
      grp.add(makeBox(x1 - 0.65, py0, x1 - 0.22, py1, zF + 0.45, zF + 0.72, MATS.luxLinenSand));
    }

    // 2. Accent Armchair with backrest on 'E' or 'W' side
    function addCADArmchair(grp, x0, y0, x1, y1, zF, backDir = 'E') {
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.02, zF + 0.10, MATS.luxOakSmooth));
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.10, zF + 0.40, MATS.luxBoucle));
      const bx0 = (backDir === 'E') ? (x1 - 0.16) : x0;
      const bx1 = (backDir === 'E') ? x1 : (x0 + 0.16);
      grp.add(makeBox(bx0, y0, bx1, y1, zF + 0.40, zF + 0.74, MATS.luxBoucle));
      grp.add(makeBox(x0, y0, x1, y0 + 0.14, zF + 0.40, zF + 0.60, MATS.luxBoucle));
      grp.add(makeBox(x0, y1 - 0.14, x1, y1, zF + 0.40, zF + 0.60, MATS.luxBoucle));
    }

    // 3. Nested Round Calacatta & Fluted Oak Coffee Tables (exact CAD circles)
    function addCADCoffeeTables(grp, cx1, cy1, r1, cx2, cy2, r2, zF) {
      grp.add(makeCylinder(cx1, cy1, r1 * 0.55, r1 * 0.55, zF + 0.02, zF + 0.36, MATS.luxFlutedOak, 20));
      grp.add(makeCylinder(cx1, cy1, r1, r1, zF + 0.36, zF + 0.40, MATS.luxCalacatta, 24));
      grp.add(makeCylinder(cx2, cy2, r2 * 0.55, r2 * 0.55, zF + 0.02, zF + 0.43, MATS.luxBrass, 18));
      grp.add(makeCylinder(cx2, cy2, r2, r2, zF + 0.43, zF + 0.46, MATS.luxOakSmooth, 20));
      grp.add(makeCylinder(cx1, cy1, 0.07, 0.09, zF + 0.40, zF + 0.58, MATS.luxCeramic, 12));
      grp.add(makeCylinder(cx1, cy1, 0.15, 0.05, zF + 0.56, zF + 0.76, MATS.luxPlantOlive, 10));
    }

    // 4. 6-Seater Dining Table (orient='V' -> chairs on W/E sides; orient='H' -> chairs on N/S sides)
    function addCADDiningTable6(grp, x0, y0, x1, y1, zF, zC, orient = 'V') {
      const cx = 0.5 * (x0 + x1), cy = 0.5 * (y0 + y1);
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.72, zF + 0.77, MATS.luxCalacatta));
      grp.add(makeCylinder(cx - (x1 - x0) * 0.24, cy - (y1 - y0) * 0.24, 0.12, 0.16, zF + 0.02, zF + 0.72, MATS.luxFlutedOak, 16));
      grp.add(makeCylinder(cx + (x1 - x0) * 0.24, cy + (y1 - y0) * 0.24, 0.12, 0.16, zF + 0.02, zF + 0.72, MATS.luxFlutedOak, 16));
      if (orient === 'V') {
        const step = (y1 - y0) / 3.0;
        for (let i = 0; i < 3; i++) {
          const sy = y0 + (i + 0.5) * step;
          // West chair
          grp.add(makeBox(x0 - 0.38, sy - 0.21, x0 - 0.04, sy + 0.21, zF + 0.42, zF + 0.47, MATS.luxBoucle));
          grp.add(makeBox(x0 - 0.42, sy - 0.21, x0 - 0.34, sy + 0.21, zF + 0.47, zF + 0.82, MATS.luxBoucle));
          grp.add(makeBox(x0 - 0.36, sy - 0.18, x0 - 0.08, sy + 0.18, zF + 0.02, zF + 0.42, MATS.luxOakSmooth));
          // East chair
          grp.add(makeBox(x1 + 0.04, sy - 0.21, x1 + 0.38, sy + 0.21, zF + 0.42, zF + 0.47, MATS.luxBoucle));
          grp.add(makeBox(x1 + 0.34, sy - 0.21, x1 + 0.42, sy + 0.21, zF + 0.47, zF + 0.82, MATS.luxBoucle));
          grp.add(makeBox(x1 + 0.08, sy - 0.18, x1 + 0.36, sy + 0.18, zF + 0.02, zF + 0.42, MATS.luxOakSmooth));
        }
      } else {
        const step = (x1 - x0) / 3.0;
        for (let i = 0; i < 3; i++) {
          const sx = x0 + (i + 0.5) * step;
          // North chair
          grp.add(makeBox(sx - 0.21, y0 - 0.38, sx + 0.21, y0 - 0.04, zF + 0.42, zF + 0.47, MATS.luxBoucle));
          grp.add(makeBox(sx - 0.21, y0 - 0.42, sx + 0.21, y0 - 0.34, zF + 0.47, zF + 0.82, MATS.luxBoucle));
          grp.add(makeBox(sx - 0.18, y0 - 0.36, sx + 0.18, y0 - 0.08, zF + 0.02, zF + 0.42, MATS.luxOakSmooth));
          // South chair
          grp.add(makeBox(sx - 0.21, y1 + 0.04, sx + 0.21, y1 + 0.38, zF + 0.42, zF + 0.47, MATS.luxBoucle));
          grp.add(makeBox(sx - 0.21, y1 + 0.34, sx + 0.21, y1 + 0.42, zF + 0.47, zF + 0.82, MATS.luxBoucle));
          grp.add(makeBox(sx - 0.18, y1 + 0.08, sx + 0.18, y1 + 0.36, zF + 0.02, zF + 0.42, MATS.luxOakSmooth));
        }
      }
      // Brass chandelier over dining table
      grp.add(makeCylinder(cx, cy, 0.01, 0.01, zF + 1.85, zC - 0.02, MATS.luxBrass, 8));
      grp.add(makeCylinder(cx, cy, 0.28, 0.28, zF + 1.76, zF + 1.84, MATS.luxBrass, 20));
      grp.add(makeCylinder(cx, cy, 0.22, 0.22, zF + 1.73, zF + 1.77, MATS.luxGlowWarm, 16));
    }

    // 5. Double Master Bed with Headboard on wall ('W', 'E', 'N', 'S') + 2 Nightstands
    function addCADMasterBed(grp, x0, y0, x1, y1, zF, headDir = 'W', ns1 = null, ns2 = null) {
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.06, zF + 0.28, MATS.luxOakSmooth));
      grp.add(makeBox(x0 + 0.05, y0 + 0.05, x1 - 0.05, y1 - 0.05, zF + 0.28, zF + 0.48, MATS.luxCeramic));
      if (headDir === 'W') {
        grp.add(makeBox(x0, y0 - 0.08, x0 + 0.12, y1 + 0.08, zF + 0.02, zF + 0.92, MATS.luxFlutedOak));
        grp.add(makeBox(x0 + 0.12, y0 + 0.10, x0 + 0.42, 0.5 * (y0 + y1) - 0.04, zF + 0.48, zF + 0.60, MATS.luxBoucle));
        grp.add(makeBox(x0 + 0.12, 0.5 * (y0 + y1) + 0.04, x0 + 0.42, y1 - 0.10, zF + 0.48, zF + 0.60, MATS.luxBoucle));
        grp.add(makeBox(x0 + 0.48, y0 + 0.04, x1 - 0.04, y1 - 0.04, zF + 0.29, zF + 0.50, MATS.luxTaupe));
      } else if (headDir === 'E') {
        grp.add(makeBox(x1 - 0.12, y0 - 0.08, x1, y1 + 0.08, zF + 0.02, zF + 0.92, MATS.luxFlutedOak));
        grp.add(makeBox(x1 - 0.42, y0 + 0.10, x1 - 0.12, 0.5 * (y0 + y1) - 0.04, zF + 0.48, zF + 0.60, MATS.luxBoucle));
        grp.add(makeBox(x1 - 0.42, 0.5 * (y0 + y1) + 0.04, x1 - 0.12, y1 - 0.10, zF + 0.48, zF + 0.60, MATS.luxBoucle));
        grp.add(makeBox(x0 + 0.04, y0 + 0.04, x1 - 0.48, y1 - 0.04, zF + 0.29, zF + 0.50, MATS.luxTaupe));
      }
      [ns1, ns2].forEach(ns => {
        if (!ns) return;
        const [nx0, ny0, nx1, ny1] = ns;
        grp.add(makeBox(nx0, ny0, nx1, ny1, zF + 0.06, zF + 0.44, MATS.luxOakSmooth));
        grp.add(makeBox(nx0 - 0.01, ny0 - 0.01, nx1 + 0.01, ny1 + 0.01, zF + 0.44, zF + 0.47, MATS.luxCalacatta));
        const ncx = 0.5 * (nx0 + nx1), ncy = 0.5 * (ny0 + ny1);
        grp.add(makeCylinder(ncx, ncy, 0.04, 0.06, zF + 0.47, zF + 0.62, MATS.luxBrass, 12));
        grp.add(makeCylinder(ncx, ncy, 0.09, 0.11, zF + 0.60, zF + 0.72, MATS.luxGlowWarm, 12));
      });
    }

    // 6. Single/Youth Bed with Headboard on 'N', 'S', 'E', or 'W'
    function addCADSingleBed(grp, x0, y0, x1, y1, zF, headDir = 'N') {
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.05, zF + 0.26, MATS.luxOakSmooth));
      grp.add(makeBox(x0 + 0.04, y0 + 0.04, x1 - 0.04, y1 - 0.04, zF + 0.26, zF + 0.44, MATS.luxCeramic));
      if (headDir === 'N') {
        grp.add(makeBox(x0, y0, x1, y0 + 0.10, zF + 0.02, zF + 0.78, MATS.luxFlutedOak));
        grp.add(makeBox(x0 + 0.10, y0 + 0.12, x1 - 0.10, y0 + 0.38, zF + 0.44, zF + 0.54, MATS.luxBoucle));
        grp.add(makeBox(x0 + 0.03, y0 + 0.42, x1 - 0.03, y1 - 0.03, zF + 0.27, zF + 0.46, MATS.luxTaupe));
      } else if (headDir === 'S') {
        grp.add(makeBox(x0, y1 - 0.10, x1, y1, zF + 0.02, zF + 0.78, MATS.luxFlutedOak));
        grp.add(makeBox(x0 + 0.10, y1 - 0.38, x1 - 0.10, y1 - 0.12, zF + 0.44, zF + 0.54, MATS.luxBoucle));
        grp.add(makeBox(x0 + 0.03, y0 + 0.03, x1 - 0.03, y1 - 0.42, zF + 0.27, zF + 0.46, MATS.luxTaupe));
      } else if (headDir === 'E') {
        grp.add(makeBox(x1 - 0.10, y0, x1, y1, zF + 0.02, zF + 0.78, MATS.luxFlutedOak));
        grp.add(makeBox(x1 - 0.38, y0 + 0.10, x1 - 0.12, y1 - 0.10, zF + 0.44, zF + 0.54, MATS.luxBoucle));
        grp.add(makeBox(x0 + 0.03, y0 + 0.03, x1 - 0.42, y1 - 0.03, zF + 0.27, zF + 0.46, MATS.luxTaupe));
      } else if (headDir === 'W') {
        grp.add(makeBox(x0, y0, x0 + 0.10, y1, zF + 0.02, zF + 0.78, MATS.luxFlutedOak));
        grp.add(makeBox(x0 + 0.12, y0 + 0.10, x0 + 0.38, y1 - 0.10, zF + 0.44, zF + 0.54, MATS.luxBoucle));
        grp.add(makeBox(x0 + 0.42, y0 + 0.03, x1 - 0.03, y1 - 0.03, zF + 0.27, zF + 0.46, MATS.luxTaupe));
      }
    }

    // 7. Wardrobe / Closet (marked with X in CAD)
    function addCADWardrobe(grp, x0, y0, x1, y1, zF) {
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.02, zF + 2.22, MATS.luxCabinet));
      grp.add(makeBox(x0 + 0.02, y0 + 0.02, x1 - 0.02, y1 - 0.02, zF + 2.22, zF + 2.26, MATS.luxFlutedOak));
    }

    // 8. Study Desk + Chair
    function addCADDesk(grp, x0, y0, x1, y1, zF, chairSide = 'W') {
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.71, zF + 0.75, MATS.luxOakSmooth));
      grp.add(makeBox(x0 + 0.03, y0 + 0.03, x1 - 0.03, y0 + 0.08, zF + 0.02, zF + 0.71, MATS.aluDark));
      grp.add(makeBox(x0 + 0.03, y1 - 0.08, x1 - 0.03, y1 - 0.03, zF + 0.02, zF + 0.71, MATS.aluDark));
      const cy = 0.5 * (y0 + y1);
      const cx = (chairSide === 'W') ? (x0 - 0.22) : (x1 + 0.22);
      grp.add(makeCylinder(cx, cy, 0.20, 0.20, zF + 0.42, zF + 0.47, MATS.luxBoucle, 14));
      grp.add(makeCylinder(cx, cy, 0.04, 0.16, zF + 0.02, zF + 0.42, MATS.aluDark, 12));
    }

    // 9. Bathroom Fixtures (Vanity, WC, Bathtub, Shower, Washer/Dryer)
    function addCADVanity(grp, x0, y0, x1, y1, zF, wallSide = 'E') {
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.25, zF + 0.82, MATS.luxFlutedOak));
      grp.add(makeBox(x0 - 0.01, y0 - 0.01, x1 + 0.01, y1 + 0.01, zF + 0.82, zF + 0.86, MATS.luxCalacatta));
      const cx = 0.5 * (x0 + x1), cy = 0.5 * (y0 + y1);
      grp.add(makeCylinder(cx, cy, 0.16, 0.13, zF + 0.86, zF + 0.97, MATS.luxCeramic, 18));
      grp.add(makeCylinder(cx, cy, 0.015, 0.02, zF + 0.97, zF + 1.09, MATS.luxBrass, 10));
      if (wallSide === 'E') {
        grp.add(makeBox(x1 - 0.03, y0 + 0.05, x1, y1 - 0.05, zF + 1.02, zF + 1.90, MATS.luxMirror));
      } else if (wallSide === 'W') {
        grp.add(makeBox(x0, y0 + 0.05, x0 + 0.03, y1 - 0.05, zF + 1.02, zF + 1.90, MATS.luxMirror));
      } else if (wallSide === 'N') {
        grp.add(makeBox(x0 + 0.05, y0, x1 - 0.05, y0 + 0.03, zF + 1.02, zF + 1.90, MATS.luxMirror));
      } else if (wallSide === 'S') {
        grp.add(makeBox(x0 + 0.05, y1 - 0.03, x1 - 0.05, y1, zF + 1.02, zF + 1.90, MATS.luxMirror));
      }
    }

    function addCADWC(grp, x0, y0, x1, y1, zF) {
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.16, zF + 0.43, MATS.luxCeramic));
      grp.add(makeBox(x0 + 0.03, y0 + 0.03, x1 - 0.03, y1 - 0.03, zF + 0.43, zF + 0.46, MATS.luxCeramic));
    }

    function addCADBathtub(grp, x0, y0, x1, y1, zF) {
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.02, zF + 0.56, MATS.luxCeramic));
      grp.add(makeBox(x0 + 0.08, y0 + 0.08, x1 - 0.08, y1 - 0.08, zF + 0.44, zF + 0.55, MATS.waterSpa));
      grp.add(makeCylinder(0.5 * (x0 + x1), y0 + 0.12, 0.02, 0.025, zF + 0.56, zF + 0.72, MATS.luxBrass, 10));
    }

    function addCADShower(grp, x0, y0, x1, y1, zF) {
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.005, zF + 0.03, MATS.luxCalacatta));
      grp.add(makeBox(x0, y1 - 0.02, x1, y1, zF + 0.03, zF + 2.05, MATS.luxClearGlass, false));
      grp.add(makeBox(x1 - 0.02, y0, x1, y1, zF + 0.03, zF + 2.05, MATS.luxClearGlass, false));
      grp.add(makeCylinder(0.5 * (x0 + x1), 0.5 * (y0 + y1), 0.12, 0.12, zF + 2.05, zF + 2.08, MATS.luxBrass, 14));
    }

    function addCADWasher(grp, x0, y0, x1, y1, zF) {
      grp.add(makeBox(x0, y0, x1, y1, zF + 0.02, zF + 0.87, MATS.luxCeramic));
      grp.add(makeBox(x0 - 0.01, y0 - 0.01, x1 + 0.01, y1 + 0.01, zF + 0.87, zF + 0.90, MATS.luxCalacatta));
    }

    function buildPines48BalconyLounge(grp, bx, by, bw, bd, zF) {
      const sx0 = bx - 0.42, sx1 = bx + 0.42;
      const sy0 = by - 1.05, sy1 = by + 0.45;
      grp.add(makeBox(sx0, sy0, sx1, sy1, zF + 0.02, zF + 0.14, MATS.luxOakSmooth));
      grp.add(makeBox(sx0 + 0.03, sy0 + 0.03, sx1 - 0.03, sy1 - 0.03, zF + 0.14, zF + 0.38, MATS.luxBoucle));
      grp.add(makeBox(sx0, sy0, sx1, sy0 + 0.16, zF + 0.38, zF + 0.68, MATS.luxTaupe));
      grp.add(makeCylinder(bx, by + 0.95, 0.36, 0.28, zF + 0.02, zF + 0.36, MATS.luxCalacatta, 18));
      [by - bd * 0.38, by + bd * 0.38].forEach(py => {
        grp.add(makeCylinder(bx, py, 0.24, 0.18, zF + 0.02, zF + 0.52, MATS.luxCeramic, 16));
        grp.add(makeCylinder(bx, py, 0.035, 0.045, zF + 0.52, zF + 1.15, MATS.luxOakSmooth, 10));
        grp.add(makeCylinder(bx, py, 0.38, 0.22, zF + 1.05, zF + 1.68, MATS.luxPlantOlive, 14));
      });
    }

    // =========================================================================
    // TYPICAL FLOOR (F1-F8) EXACT 1:1 CAD FURNITURE BUILDER
    // =========================================================================
    function buildTypicalFloorExactCADFurniture(grp, zF, zC) {
      // --- 1. WEST APARTMENT (5 ROOMS) ---
      // Floor finish zones
      grp.add(makeBox(-13.10, -0.25, -3.40, 3.96, zF + 0.004, zF + 0.015, MATS.luxTravertine, false));
      grp.add(makeBox(-13.10, -4.94, -3.60, -0.35, zF + 0.004, zF + 0.015, MATS.woodDeck, false));
      grp.add(makeBox(-1.04, -4.30, 2.24, -0.35, zF + 0.004, zF + 0.015, MATS.woodDeck, false));

      // 1A. West Living Room (exact CAD coords):
      // Rug [-12.60.. -10.05, 1.29.. 3.60]
      grp.add(makeBox(-12.60, 1.29, -10.05, 3.60, zF + 0.015, zF + 0.028, MATS.luxRug, false));
      // 3-Seat Sofa on South wall [-12.60.. -10.21, 3.04.. 3.90]
      addCADSofa3Seat(grp, -12.60, 3.04, -10.21, 3.90, zF, 'S');
      // Nested Round Coffee Tables at (-11.35, 2.35) & (-10.95, 2.15)
      addCADCoffeeTables(grp, -11.35, 2.35, 0.42, -10.95, 2.15, 0.28, zF);
      // Armchair on East side of rug [-10.55.. -9.68, 1.85.. 2.75] facing West
      addCADArmchair(grp, -10.55, 1.85, -9.68, 2.75, zF, 'E');
      // Sheer curtains along West balcony vitrine (X = -13.02, Y = 0.58..3.73)
      grp.add(makeBox(-13.08, 0.58, -12.92, 1.15, zF + 0.03, zC - 0.18, MATS.luxCurtain, false));
      grp.add(makeBox(-13.08, 3.20, -12.92, 3.75, zF + 0.03, zC - 0.18, MATS.luxCurtain, false));

      // 1B. West Dining Area (exact CAD coords: Table [-8.42.. -7.62, 2.42.. 3.88] + 6 Chairs)
      addCADDiningTable6(grp, -8.42, 2.42, -7.62, 3.88, zF, zC, 'V');

      // 1C. West Kitchen (exact CAD L-Counter + Peninsula + Fridge):
      // Fridge niche on East wall [-4.02.. -3.38, 1.82.. 2.58]
      grp.add(makeBox(-4.02, 1.82, -3.38, 2.58, zF + 0.02, zF + 2.18, MATS.luxFlutedOak));
      grp.add(makeBox(-4.04, 1.86, -4.01, 2.54, zF + 0.05, zF + 2.10, MATS.mamadSteel));
      // North-East Tall Oven Pantry [-4.02.. -3.38, 1.18.. 1.82]
      grp.add(makeBox(-4.02, 1.18, -3.38, 1.82, zF + 0.02, zF + 2.18, MATS.luxFlutedOak));
      // East counter leg [-4.02.. -3.38, 2.58.. 3.92]
      grp.add(makeBox(-4.02, 2.58, -3.38, 3.92, zF + 0.02, zF + 0.88, MATS.luxCabinet));
      grp.add(makeBox(-4.04, 2.58, -3.38, 3.92, zF + 0.88, zF + 0.92, MATS.luxCalacatta));
      // South counter leg [-6.36.. -3.38, 3.30.. 3.96] with Sink at X=-4.85
      grp.add(makeBox(-6.36, 3.30, -3.38, 3.96, zF + 0.02, zF + 0.88, MATS.luxCabinet));
      grp.add(makeBox(-6.38, 3.28, -3.38, 3.96, zF + 0.88, zF + 0.92, MATS.luxCalacatta));
      grp.add(makeBox(-5.20, 3.42, -4.50, 3.82, zF + 0.86, zF + 0.925, MATS.luxCeramic)); // Sink basin
      grp.add(makeCylinder(-4.85, 3.86, 0.018, 0.022, zF + 0.92, zF + 1.22, MATS.luxBrass, 12)); // Faucet
      // West Peninsula / Bar leg [-6.36.. -5.66, 2.16.. 3.96] + 2 Barstools on West side
      grp.add(makeBox(-6.36, 2.16, -5.66, 3.96, zF + 0.02, zF + 0.88, MATS.luxFlutedOak));
      grp.add(makeBox(-6.40, 2.14, -5.64, 3.96, zF + 0.88, zF + 0.92, MATS.luxCalacatta));
      [2.58, 3.15].forEach(sy => {
        grp.add(makeCylinder(-6.58, sy, 0.025, 0.14, zF + 0.02, zF + 0.64, MATS.luxBrass, 12));
        grp.add(makeCylinder(-6.58, sy, 0.17, 0.17, zF + 0.64, zF + 0.70, MATS.luxBoucle, 16));
      });

      // 1D. West Master Suite (exact CAD Bed on West wall [-13.10.. -11.05, -2.65.. -0.95]):
      grp.add(makeBox(-12.95, -2.85, -10.75, -0.75, zF + 0.015, zF + 0.026, MATS.luxRug, false));
      addCADMasterBed(grp, -13.10, -2.65, -11.05, -0.95, zF, 'W', [-13.10, -3.18, -12.65, -2.72], [-13.10, -0.88, -12.65, -0.42]);
      // Walk-in Closet (ח. ארונות) [-11.35.. -9.65, -4.95.. -3.38] — West & East wardrobes
      addCADWardrobe(grp, -11.35, -4.95, -10.95, -3.38, zF);
      addCADWardrobe(grp, -10.02, -4.95, -9.62, -3.38, zF);
      // Master Bathroom [-13.11.. -11.45, -4.95.. -3.48]: Shower NW, WC West, Vanity North
      addCADShower(grp, -13.10, -4.95, -12.25, -4.25, zF);
      addCADWC(grp, -13.10, -4.10, -12.55, -3.68, zF);
      addCADVanity(grp, -12.15, -4.95, -11.48, -4.50, zF, 'N');

      // 1E. West Bedroom 1 (exact CAD: Bed [-9.52.. -8.52, -4.94.. -2.94], Desk [-7.05.. -6.65, -4.45.. -3.55], Wardrobe [-9.52.. -7.82, -2.02.. -1.48])
      addCADSingleBed(grp, -9.52, -4.94, -8.52, -2.94, zF, 'N');
      addCADDesk(grp, -7.05, -4.45, -6.65, -3.55, zF, 'W');
      addCADWardrobe(grp, -9.52, -2.02, -7.82, -1.48, zF);

      // 1F. West Bedroom 2 (exact CAD: Bed [-6.45.. -5.45, -4.94.. -2.94], Desk [-4.15.. -3.75, -4.45.. -3.55], Wardrobe [-6.45.. -4.85, -2.02.. -1.48])
      addCADSingleBed(grp, -6.45, -4.94, -5.45, -2.94, zF, 'N');
      addCADDesk(grp, -4.15, -4.45, -3.75, -3.55, zF, 'W');
      addCADWardrobe(grp, -6.45, -2.02, -4.85, -1.48, zF);

      // 1G. West General Bathroom & Service Room [-3.55.. -1.25, -4.23.. -1.48]:
      addCADBathtub(grp, -3.52, -3.15, -2.82, -1.50, zF);
      addCADWC(grp, -1.80, -3.12, -1.28, -2.72, zF);
      addCADVanity(grp, -1.78, -2.55, -1.28, -1.75, zF, 'E');
      addCADWasher(grp, -3.52, -4.15, -2.85, -3.45, zF);

      // 1H. West Mamad [-1.05.. +2.25, -4.33.. -0.33] (Bed along East partition [1.22.. 2.22, -4.23.. -2.45], Wardrobe on South [0.55.. 2.22, -0.88.. -0.35])
      addCADSingleBed(grp, 1.22, -4.23, 2.22, -2.45, zF, 'N');
      addCADWardrobe(grp, 0.55, -0.88, 2.22, -0.35, zF);

      // --- 2. EAST APARTMENT (4 ROOMS, FACING HAFETZ HAIM ST) ---
      // Floor finish zones
      grp.add(makeBox(5.65, -0.25, 14.10, 3.96, zF + 0.004, zF + 0.015, MATS.luxTravertine, false));
      grp.add(makeBox(5.65, -4.94, 14.10, -0.35, zF + 0.004, zF + 0.015, MATS.woodDeck, false));
      grp.add(makeBox(2.46, -4.30, 5.45, -0.35, zF + 0.004, zF + 0.015, MATS.woodDeck, false));

      // 2A. East Living Room (exact CAD coords):
      // Rug [11.00.. 13.78, 1.24.. 3.60]
      grp.add(makeBox(11.00, 1.24, 13.78, 3.60, zF + 0.015, zF + 0.028, MATS.luxRug, false));
      // 3-Seat Sofa on South wall [11.13.. 13.78, 2.99.. 3.88]
      addCADSofa3Seat(grp, 11.13, 2.99, 13.78, 3.88, zF, 'S');
      // Nested Round Coffee Tables at (12.15, 2.30) & (11.75, 2.15)
      addCADCoffeeTables(grp, 12.15, 2.30, 0.42, 11.75, 2.15, 0.28, zF);
      // Armchair on West side of rug [10.45.. 11.35, 1.88.. 2.78] facing East
      addCADArmchair(grp, 10.45, 1.88, 11.35, 2.78, zF, 'W');
      // Sheer curtains along East balcony vitrine (X = +14.02, Y = 0.58..3.73)
      grp.add(makeBox(13.92, 0.58, 14.08, 1.15, zF + 0.03, zC - 0.18, MATS.luxCurtain, false));
      grp.add(makeBox(13.92, 3.20, 14.08, 3.75, zF + 0.03, zC - 0.18, MATS.luxCurtain, false));

      // 2B. East Dining Area (exact CAD coords: Table [8.98.. 9.78, 2.42.. 3.88] + 6 Chairs)
      addCADDiningTable6(grp, 8.98, 2.42, 9.78, 3.88, zF, zC, 'V');

      // 2C. East Kitchen (exact CAD L-Counter + Peninsula + Fridge):
      // Fridge niche on West wall [5.66.. 6.30, 1.82.. 2.58] & Tall Pantry [5.66.. 6.30, 1.18.. 1.82]
      grp.add(makeBox(5.66, 1.82, 6.30, 2.58, zF + 0.02, zF + 2.18, MATS.luxFlutedOak));
      grp.add(makeBox(6.29, 1.86, 6.32, 2.54, zF + 0.05, zF + 2.10, MATS.mamadSteel));
      grp.add(makeBox(5.66, 1.18, 6.30, 1.82, zF + 0.02, zF + 2.18, MATS.luxFlutedOak));
      // West counter leg [5.66.. 6.30, 2.58.. 3.92]
      grp.add(makeBox(5.66, 2.58, 6.30, 3.92, zF + 0.02, zF + 0.88, MATS.luxCabinet));
      grp.add(makeBox(5.66, 2.58, 6.32, 3.92, zF + 0.88, zF + 0.92, MATS.luxCalacatta));
      // South counter leg [5.66.. 8.40, 3.30.. 3.96] with Sink at X=+7.10
      grp.add(makeBox(5.66, 3.30, 8.40, 3.96, zF + 0.02, zF + 0.88, MATS.luxCabinet));
      grp.add(makeBox(5.66, 3.28, 8.42, 3.96, zF + 0.88, zF + 0.92, MATS.luxCalacatta));
      grp.add(makeBox(6.75, 3.42, 7.45, 3.82, zF + 0.86, zF + 0.925, MATS.luxCeramic));
      grp.add(makeCylinder(7.10, 3.86, 0.018, 0.022, zF + 0.92, zF + 1.22, MATS.luxBrass, 12));
      // East Peninsula / Bar leg [7.72.. 8.42, 2.16.. 3.96] + 2 Barstools on East side
      grp.add(makeBox(7.72, 2.16, 8.42, 3.96, zF + 0.02, zF + 0.88, MATS.luxFlutedOak));
      grp.add(makeBox(7.70, 2.14, 8.44, 3.96, zF + 0.88, zF + 0.92, MATS.luxCalacatta));
      [2.58, 3.15].forEach(sy => {
        grp.add(makeCylinder(8.64, sy, 0.025, 0.14, zF + 0.02, zF + 0.64, MATS.luxBrass, 12));
        grp.add(makeCylinder(8.64, sy, 0.17, 0.17, zF + 0.64, zF + 0.70, MATS.luxBoucle, 16));
      });

      // 2D. East Master Suite (exact CAD Bed on East wall [12.05.. 14.10, -2.65.. -0.95]):
      grp.add(makeBox(11.75, -2.85, 13.95, -0.75, zF + 0.015, zF + 0.026, MATS.luxRug, false));
      addCADMasterBed(grp, 12.05, -2.65, 14.10, -0.95, zF, 'E', [13.65, -3.18, 14.10, -2.72], [13.65, -0.88, 14.10, -0.42]);
      // Walk-in Closet (ח. ארונות) [10.95.. 12.44, -4.95.. -3.38] — West & East wardrobes
      addCADWardrobe(grp, 10.95, -4.95, 11.35, -3.38, zF);
      addCADWardrobe(grp, 12.04, -4.95, 12.44, -3.38, zF);
      // Master Bathroom [12.54.. 14.11, -4.95.. -3.38]: Shower NE, WC North, Vanity East
      addCADShower(grp, 13.30, -4.95, 14.10, -4.25, zF);
      addCADWC(grp, 12.68, -4.95, 13.12, -4.42, zF);
      addCADVanity(grp, 13.62, -4.15, 14.10, -3.48, zF, 'E');

      // 2E. East Bedroom 1 (exact CAD: Bed [9.82.. 10.82, -4.94.. -2.94], Desk [8.05.. 8.45, -4.45.. -3.55], Wardrobe [9.35.. 10.82, -2.02.. -1.48])
      addCADSingleBed(grp, 9.82, -4.94, 10.82, -2.94, zF, 'N');
      addCADDesk(grp, 8.05, -4.45, 8.45, -3.55, zF, 'E');
      addCADWardrobe(grp, 9.35, -2.02, 10.82, -1.48, zF);

      // 2F. East General Bathroom & Service Room [5.66.. 7.96, -4.23.. -1.48]:
      addCADBathtub(grp, 5.68, -3.15, 6.38, -1.50, zF);
      addCADWC(grp, 7.40, -3.12, 7.92, -2.72, zF);
      addCADVanity(grp, 7.42, -2.55, 7.92, -1.75, zF, 'E');
      addCADWasher(grp, 5.68, -4.15, 6.35, -3.45, zF);

      // 2G. East Mamad [2.46.. 5.46, -4.33.. -0.33] (Bed along West partition [2.52.. 3.52, -4.22.. -2.44], Wardrobe on South [2.52.. 4.22, -0.88.. -0.35])
      addCADSingleBed(grp, 2.52, -4.22, 3.52, -2.44, zF, 'N');
      addCADWardrobe(grp, 2.52, -0.88, 4.22, -0.35, zF);

      // --- 3. WEST & EAST SUN BALCONIES + CORE STORAGE ROOMS (מחסנים דירתיים 120x351) ---
      buildPines48BalconyLounge(grp, -14.35, -0.50, 2.0, 9.4, zF);
      buildPines48BalconyLounge(grp,  15.35, -0.50, 2.0, 9.4, zF);
      // West Storage Room (מחסן 120×351 at X=-3.16..-1.96, Y=1.48..4.99) & East Storage Room (מחסן 120×351 at X=2.50..3.70, Y=1.48..4.99)
      [0.45, 1.05, 1.65].forEach(shZ => {
        grp.add(makeBox(-3.12, 1.85, -2.65, 4.75, zF + shZ, zF + shZ + 0.04, MATS.luxOakSmooth));
        grp.add(makeBox( 3.20, 1.85,  3.67, 4.75, zF + shZ, zF + shZ + 0.04, MATS.luxOakSmooth));
      });
    }

    // =========================================================================
    // PENTHOUSE FLOOR 9 EXACT 1:1 CAD FURNITURE BUILDER
    // =========================================================================
    function buildPenthouseExactCADFurniture(grp, zF, zC) {
      // Floor finish zones
      grp.add(makeBox(3.90, -4.50, 9.35, 3.96, zF + 0.004, zF + 0.015, MATS.luxTravertine, false));
      grp.add(makeBox(-10.00, -4.94, 2.25, 3.96, zF + 0.004, zF + 0.015, MATS.woodDeck, false));

      // 1. Penthouse Living Room (exact CAD coords: Rug [5.17.. 8.04, -3.50.. -1.20]):
      grp.add(makeBox(5.17, -3.50, 8.04, -1.20, zF + 0.015, zF + 0.028, MATS.luxRug, false));
      // 3-Seat Sofa on South side of living area facing North [5.64.. 8.04, -1.92.. -1.05]
      addCADSofa3Seat(grp, 5.64, -1.92, 8.04, -1.05, zF, 'S');
      // Nested Round Coffee Tables at (6.50, -2.55) & (6.85, -2.65)
      addCADCoffeeTables(grp, 6.50, -2.55, 0.44, 6.85, -2.65, 0.28, zF);
      // Armchair on West side of rug facing East [4.77.. 5.64, -2.85.. -1.95]
      addCADArmchair(grp, 4.77, -2.85, 5.64, -1.95, zF, 'W');

      // 2. Penthouse 6-Seat Dining Table (exact CAD Horizontal Table [7.20.. 8.85, -0.35.. 0.55])
      addCADDiningTable6(grp, 7.20, -0.35, 8.85, 0.55, zF, zC, 'H');

      // 3. Penthouse Chef Kitchen & Waterfall Island (exact CAD Island [6.06.. 8.49, 1.52.. 2.42]):
      const islX0 = 6.06, islX1 = 8.49, islY0 = 1.52, islY1 = 2.42;
      grp.add(makeBox(islX0 + 0.05, islY0 + 0.04, islX1 - 0.05, islY1 - 0.04, zF + 0.02, zF + 0.88, MATS.luxFlutedOak));
      grp.add(makeBox(islX0, islY0, islX1, islY1, zF + 0.88, zF + 0.93, MATS.luxCalacatta));
      grp.add(makeBox(islX0, islY0, islX0 + 0.05, islY1, zF + 0.02, zF + 0.88, MATS.luxCalacatta));
      grp.add(makeBox(islX1 - 0.05, islY0, islX1, islY1, zF + 0.02, zF + 0.88, MATS.luxCalacatta));
      // 4 Bar Stools on North side of Island
      [6.45, 7.00, 7.55, 8.10].forEach(sx => {
        grp.add(makeCylinder(sx, islY0 - 0.24, 0.025, 0.14, zF + 0.02, zF + 0.64, MATS.luxBrass, 12));
        grp.add(makeCylinder(sx, islY0 - 0.24, 0.17, 0.17, zF + 0.64, zF + 0.70, MATS.luxBoucle, 16));
      });
      // West Tall Pantry & Fridge Wall [4.25.. 4.90, 1.52.. 3.38]
      grp.add(makeBox(4.25, 1.52, 4.90, 3.38, zF + 0.02, zF + 2.20, MATS.luxFlutedOak));
      grp.add(makeBox(4.89, 2.55, 4.92, 3.30, zF + 0.06, zF + 2.10, MATS.mamadSteel));
      // South Counter & Sink Run [4.25.. 9.30, 3.38.. 3.98]
      grp.add(makeBox(4.25, 3.38, 9.30, 3.98, zF + 0.02, zF + 0.88, MATS.luxCabinet));
      grp.add(makeBox(4.25, 3.36, 9.32, 3.98, zF + 0.88, zF + 0.92, MATS.luxCalacatta));
      grp.add(makeBox(6.85, 3.48, 7.55, 3.88, zF + 0.86, zF + 0.925, MATS.luxCeramic));
      grp.add(makeCylinder(7.20, 3.90, 0.018, 0.022, zF + 0.92, zF + 1.22, MATS.luxBrass, 12));

      // 4. Penthouse Guest Powder Room [2.50.. 3.80, -4.40.. -1.48]
      addCADWC(grp, 2.85, -4.40, 3.35, -3.90, zF);
      addCADVanity(grp, 3.35, -2.25, 3.78, -1.55, zF, 'E');

      // 5. Penthouse Mamad [-1.05.. +2.25, -4.33.. -1.48] (Bed [-0.95.. 0.85, -3.28.. -2.28], Wardrobe [1.75.. 2.22, -3.15.. -1.65], Desk [-0.95.. -0.10, -2.02.. -1.52])
      addCADSingleBed(grp, -0.95, -3.28, 0.85, -2.28, zF, 'W');
      addCADWardrobe(grp, 1.75, -3.15, 2.22, -1.65, zF);
      addCADDesk(grp, -0.95, -2.02, -0.10, -1.52, zF, 'N');

      // 6. Penthouse General Bathroom & Service Room [-3.65.. -1.25, -4.23.. -1.48]
      addCADBathtub(grp, -2.00, -3.15, -1.30, -1.50, zF);
      addCADWC(grp, -3.62, -3.12, -3.10, -2.72, zF);
      addCADVanity(grp, -3.62, -2.55, -3.12, -1.75, zF, 'W');
      addCADWasher(grp, -2.05, -4.15, -1.35, -3.45, zF);

      // 7. Penthouse North-West Bedroom 2 [-6.75.. -3.80, -4.94.. -1.48]
      addCADSingleBed(grp, -6.65, -4.94, -5.65, -2.94, zF, 'N');
      addCADDesk(grp, -4.25, -4.45, -3.85, -3.55, zF, 'W');
      addCADWardrobe(grp, -6.65, -2.02, -5.25, -1.48, zF);

      // 8. Penthouse North-West Bedroom 1 [-9.95.. -6.85, -4.94.. -1.48]
      addCADSingleBed(grp, -9.92, -4.94, -8.92, -2.94, zF, 'N');
      addCADDesk(grp, -7.35, -4.45, -6.95, -3.55, zF, 'W');
      addCADWardrobe(grp, -9.95, -1.52, -8.32, -0.92, zF);

      // 9. Penthouse South-West Master Suite & Study/Dressing Room:
      // Study/Dressing Room [-9.95.. -7.15, -0.25.. +3.98]: Daybed/Sofa [-9.92.. -8.92, 2.20.. 3.96], Desk [-7.65.. -7.20, 2.75.. 3.65], North Closet [-9.95.. -8.32, -0.82.. -0.25]
      addCADWardrobe(grp, -9.95, -0.82, -8.32, -0.25, zF);
      addCADSingleBed(grp, -9.92, 2.20, -8.92, 3.96, zF, 'S');
      addCADDesk(grp, -7.65, 2.75, -7.20, 3.65, zF, 'W');
      // Master Bedroom [-7.05.. -3.70, 0.80.. 3.98]: Double Bed on West wall [-7.02.. -5.02, 1.55.. 2.75] + 2 Nightstands
      grp.add(makeBox(-6.90, 1.25, -4.60, 3.10, zF + 0.015, zF + 0.026, MATS.luxRug, false));
      addCADMasterBed(grp, -7.02, 1.55, -5.02, 2.75, zF, 'W', [-7.02, 1.15, -6.62, 1.52], [-7.02, 2.78, -6.62, 3.15]);
      // Master Walk-in Closet [-3.65.. -2.05, 0.80.. 2.25]
      addCADWardrobe(grp, -3.65, 0.80, -2.05, 1.35, zF);
      addCADWardrobe(grp, -3.65, 1.75, -2.05, 2.25, zF);
      // Master En-Suite Bathroom [-3.65.. -2.05, 2.30.. 4.95]
      addCADWC(grp, -2.55, 2.35, -2.05, 2.75, zF);
      addCADVanity(grp, -2.55, 2.90, -2.05, 3.70, zF, 'E');
      addCADShower(grp, -3.62, 4.10, -2.05, 4.95, zF);

      // 10. Penthouse West & East Roof Terrace Outdoor Furniture (aligned to Garmushka 295x940 & 456x940 terraces)
      // West Roof Terrace (-13.361..-10.211): Luxury Jacuzzi Spa + 2 Sun Loungers + Lounge Seating
      const jx0 = -13.05, jx1 = -11.05, jy0 = -4.50, jy1 = -2.50;
      grp.add(makeBox(jx0, jy0, jx1, jy1, zF + 0.02, zF + 0.78, MATS.luxFlutedOak));
      grp.add(makeBox(jx0 + 0.12, jy0 + 0.12, jx1 - 0.12, jy1 - 0.12, zF + 0.78, zF + 0.84, MATS.luxCeramic));
      grp.add(makeBox(jx0 + 0.22, jy0 + 0.22, jx1 - 0.22, jy1 - 0.22, zF + 0.70, zF + 0.82, MATS.waterSpa));
      [-1.70, -0.75].forEach(ly => {
        grp.add(makeBox(-12.95, ly, -11.15, ly + 0.72, zF + 0.02, zF + 0.24, MATS.luxOakSmooth));
        grp.add(makeBox(-12.90, ly + 0.04, -11.20, ly + 0.68, zF + 0.24, zF + 0.34, MATS.luxBoucle));
      });
      buildPines48BalconyLounge(grp, -11.75, 1.85, 2.0, 3.8, zF);

      // East Roof Terrace (9.599..14.359, facing Hafetz Haim St): Outdoor BBQ Kitchen + 8-Seat Dining Table + Lounge
      grp.add(makeBox(10.20, -4.65, 13.80, -3.95, zF + 0.02, zF + 0.88, MATS.aluDark));
      grp.add(makeBox(10.18, -4.67, 13.82, -3.93, zF + 0.88, zF + 0.93, MATS.luxCalacatta));
      grp.add(makeBox(11.20, -4.55, 12.25, -4.05, zF + 0.93, zF + 1.08, MATS.mamadSteel));
      const tx = 11.40, ty = -1.35;
      grp.add(makeBox(tx - 0.55, ty - 1.40, tx + 0.55, ty + 1.40, zF + 0.72, zF + 0.77, MATS.luxCalacatta));
      grp.add(makeBox(tx - 0.35, ty - 1.00, tx + 0.35, ty - 0.85, zF + 0.02, zF + 0.72, MATS.luxOakSmooth));
      grp.add(makeBox(tx - 0.35, ty + 0.85, tx + 0.35, ty + 1.00, zF + 0.02, zF + 0.72, MATS.luxOakSmooth));
      [-1.05, -0.35, 0.35, 1.05].forEach(dy => {
        grp.add(makeBox(tx - 0.92, ty + dy - 0.22, tx - 0.60, ty + dy + 0.22, zF + 0.02, zF + 0.45, MATS.luxBoucle));
        grp.add(makeBox(tx + 0.60, ty + dy - 0.22, tx + 0.92, ty + dy + 0.22, zF + 0.02, zF + 0.45, MATS.luxBoucle));
      });
      buildPines48BalconyLounge(grp, 12.95, 2.10, 2.0, 3.8, zF);
    }

    function buildPines48StyleFloorInteriors(f, pData) {
      const fGrp = new THREE.Group();
      const zF = f.zFloor;
      const zC = f.zCeil;

      if (f.id === 'kar') {
        // 1. Public Residential Building Entrance Lobby (לובי ראשי 974x413 at X=+2.35..+13.80, Y=-0.12..+3.95 & Core Lobby X=-3.05..+2.35, Y=-0.10..+1.40)
        // Architectural stone flooring (Travertine + Calacatta border inlay — NO residential apartment sofa, coffee table, or rug)
        fGrp.add(makeBox(2.35, -0.12, 13.80, 3.95, zF + 0.005, zF + 0.018, MATS.luxTravertine, false));
        fGrp.add(makeBox(-3.05, -0.10, 2.35, 1.40, zF + 0.005, zF + 0.018, MATS.luxTravertine, false));
        fGrp.add(makeBox(6.20, 0.35, 12.60, 3.45, zF + 0.018, zF + 0.026, MATS.luxCalacatta, false));

        // Recessed Architectural Mailbox Array & Intercom Panel on North-West Lobby Wall (תיבות דואר שקועות ואינטרקום בניין)
        fGrp.add(makeBox(3.15, -0.12, 5.45, 0.14, zF + 0.15, zF + 2.25, MATS.luxFlutedOak));
        fGrp.add(makeBox(3.30, 0.12, 5.15, 0.18, zF + 0.85, zF + 1.85, MATS.luxBrass));
        fGrp.add(makeBox(5.20, 0.12, 5.38, 0.18, zF + 1.15, zF + 1.55, MATS.mamadSteel));

        // Architectural Lobby Concierge / Reception Console on South Wall (דלפק לובי אדריכלי)
        fGrp.add(makeBox(6.60, 2.95, 9.10, 3.55, zF + 0.03, zF + 1.02, MATS.luxFlutedOak));
        fGrp.add(makeBox(6.55, 2.90, 9.15, 3.60, zF + 1.02, zF + 1.08, MATS.luxCalacatta));

        // Monolithic Public Lobby Waiting Benches (ספסלי המתנה אדריכליים ללובי בניין מעץ ואבן — מותאם לשימוש ציבורי)
        fGrp.add(makeBox(6.60, 0.08, 9.20, 0.62, zF + 0.03, zF + 0.42, MATS.luxCalacatta));
        fGrp.add(makeBox(6.65, 0.12, 9.15, 0.58, zF + 0.42, zF + 0.47, MATS.luxOakSmooth));
        fGrp.add(makeBox(10.10, 3.10, 12.30, 3.62, zF + 0.03, zF + 0.42, MATS.luxCalacatta));
        fGrp.add(makeBox(10.15, 3.14, 12.25, 3.58, zF + 0.42, zF + 0.47, MATS.luxOakSmooth));

        // Indoor Lobby Planters flanking East Entrance Vitrine (אדניות לובי כניסה)
        [[13.05, 0.42], [13.05, 3.32]].forEach(([px, py]) => {
          fGrp.add(makeCylinder(px, py, 0.32, 0.26, zF + 0.02, zF + 0.65, MATS.luxCeramic, 16));
          fGrp.add(makeCylinder(px, py, 0.05, 0.06, zF + 0.65, zF + 1.45, MATS.luxOakSmooth, 10));
          fGrp.add(makeCylinder(px, py, 0.42, 0.35, zF + 1.35, zF + 2.05, MATS.grass, 14));
        });

        // 2. Residents' Multi-Purpose Room / Club (חדר דיירים 260x408 at X=+5.66..+8.61, Y=-4.43..-0.35)
        // Furnished for building committee meetings & community use (refreshment counter + meeting table & chairs, no apartment chandelier)
        fGrp.add(makeBox(5.68, -4.40, 8.60, -0.38, zF + 0.005, zF + 0.016, MATS.woodDeck, false));
        // North wall refreshment credenza / kitchenette counter
        fGrp.add(makeBox(5.95, -4.38, 8.35, -3.88, zF + 0.02, zF + 0.88, MATS.luxCabinet));
        fGrp.add(makeBox(5.93, -4.38, 8.37, -3.86, zF + 0.88, zF + 0.92, MATS.luxCalacatta));
        // Committee / Residents Meeting Table & 6 Perimeter Chairs (without residential dining chandelier)
        fGrp.add(makeBox(6.65, -3.20, 7.65, -1.40, zF + 0.72, zF + 0.76, MATS.luxOakSmooth));
        fGrp.add(makeBox(6.85, -2.95, 7.45, -2.80, zF + 0.02, zF + 0.72, MATS.aluDark));
        fGrp.add(makeBox(6.85, -1.80, 7.45, -1.65, zF + 0.02, zF + 0.72, MATS.aluDark));
        [-2.90, -2.30, -1.70].forEach(cy => {
          fGrp.add(makeBox(6.18, cy - 0.20, 6.55, cy + 0.20, zF + 0.02, zF + 0.45, MATS.luxBoucle));
          fGrp.add(makeBox(7.75, cy - 0.20, 8.12, cy + 0.20, zF + 0.02, zF + 0.45, MATS.luxBoucle));
        });

        // 3. Strollers & Bicycles Room (חדר עגלות 305x400 at X=+2.45..+5.46, Y=-4.43..-0.35)
        fGrp.add(makeBox(2.46, -4.40, 5.45, -0.38, zF + 0.005, zF + 0.016, MATS.terraceFloor, false));
        // North wall steel bicycle docking racks (מתקני עגינה לאופניים)
        for (let bx = 2.80; bx <= 5.10; bx += 0.46) {
          fGrp.add(makeBox(bx - 0.06, -4.28, bx + 0.06, -3.25, zF + 0.02, zF + 0.72, MATS.aluDark));
          fGrp.add(makeCylinder(bx, -3.75, 0.30, 0.30, zF + 0.32, zF + 0.38, MATS.mamadSteel, 14));
        }
        // West wall stroller parking bays & storage shelf (תאי חניית עגלות)
        [[-2.65, -2.05], [-1.85, -1.25]].forEach(([sy0, sy1]) => {
          fGrp.add(makeBox(2.58, sy0, 3.35, sy1, zF + 0.08, zF + 0.55, MATS.luxBoucle));
          fGrp.add(makeBox(2.55, sy0, 2.68, sy1, zF + 0.55, zF + 0.92, MATS.aluDark));
        });

        // 4. Sunken Trash & Recycling Room (אשפה +47.22 => z=-0.68m at X=-1.05..+2.25, Y=-4.33..-0.33, 330x355)
        // Exact 7 Wheeled Waste/Recycling Containers per CAD Plan (4 Green 360L on East wall + 1 Orange & 2 Blue on West wall)
        const binGreenMat = new THREE.MeshStandardMaterial({ color: 0x15803d, roughness: 0.45 });
        const binOrangeMat = new THREE.MeshStandardMaterial({ color: 0xea580c, roughness: 0.45 });
        const binBlueMat = new THREE.MeshStandardMaterial({ color: 0x1d4ed8, roughness: 0.45 });
        [-3.95, -3.10, -2.25, -1.40].forEach(by => {
          fGrp.add(makeBox(1.38, by, 2.08, by + 0.68, -0.66, 0.42, binGreenMat));
        });
        fGrp.add(makeBox(-0.92, -3.95, -0.22, -3.25, -0.66, 0.42, binOrangeMat));
        [-2.95, -2.05].forEach(by => {
          fGrp.add(makeBox(-0.92, by, -0.22, by + 0.68, -0.66, 0.42, binBlueMat));
        });

        // 5. Ground Floor Storage Room (מחסן 120x338 at X=-3.16..-1.96, Y=+1.62..+5.00)
        [0.45, 1.05, 1.65].forEach(shZ => {
          fGrp.add(makeBox(-3.12, 1.85, -2.62, 4.80, zF + shZ, zF + shZ + 0.04, MATS.luxOakSmooth));
        });

        // 6. Gas Room (גז +46.45, 240x240 at X=-5.06..-3.56, Y=+1.62..+4.02, z=-0.32m) — 4 Gas Cylinders per CAD Plan
        [[-4.75, 2.10], [-4.75, 3.40], [-3.85, 2.10], [-3.85, 3.40]].forEach(([gx, gy]) => {
          fGrp.add(makeCylinder(gx, gy, 0.22, 0.22, -0.30, 1.15, MATS.mamadSteel, 14));
        });
        addToFloorAndLayer(f.id, 'furn3d', fGrp);
        return;
      }

      if (f.id === 'f9') {
        buildPenthouseExactCADFurniture(fGrp, zF, zC);
      } else {
        buildTypicalFloorExactCADFurniture(fGrp, zF, zC);
      }

      [[-10.2, 1.0], [-5.5, -2.5], [1.0, 2.5], [6.5, -2.5], [10.8, 1.0]].forEach(([lx, ly]) => {
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
        buildStaircaseFlights3D(f.id, f.zFloor, f.zCeil);

        pData.wall_polys.forEach(wp => {
          const z0 = (f.id === 'kar') ? -0.68 : f.zFloor;
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

    // =========================================================================
    // 6. GEOREFERENCED TRIPLE-RESOLUTION GOOGLE MAPS HYBRID PLANES OF PETAH TIKVA
    //    + 8 CONCENTRIC DISTANCE RINGS + 28 VERIFIED POIS AROUND HAFETZ HAIM 44
    // =========================================================================
    // Exact ITM-Surveyed Center of Lot 85-2 (ITM E=189549.11, N=665352.32 from Surveyor Table on Sheet 1)
    const CENTER_LAT = 32.0810722;
    const CENTER_LON = 34.8876650;
    const R_MERC = 6378137.0;
    const LAT0_RAD = CENTER_LAT * Math.PI / 180.0;
    const LON0_RAD = CENTER_LON * Math.PI / 180.0;
    const COS_LAT0 = Math.cos(LAT0_RAD);
    const MERC_Y0  = Math.asinh(Math.tan(LAT0_RAD));

    const SCENE_CX = 0.0;
    const SCENE_CZ = 0.0;

    // Exact ITM Azimuth from Surveyor Coordinate Table (Points 1-4):
    // Lot Long Axis (+X toward Hafetz Haim St) is rotated +15.56 deg North of East -> GMAPS_THETA = -15.56 deg
    const GMAPS_THETA = -15.56 * Math.PI / 180.0;
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
          <a href="hafetz44_spatial_map.html" target="_blank" style="display:flex;align-items:center;justify-content:center;gap:4px;padding:7px 8px;border-radius:8px;background:#334155;color:#38bdf8;font-size:11px;font-weight:800;text-decoration:none;">
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
      { text: "חפץ חיים 44 · 17 יח\"ד · רום גג +34.55 מ'", pos: new THREE.Vector3(0.5, 35.4, 3.0), cls: "b44" },
      { text: "פנטהאוז קומה 9 (+28.70) · 148.1+73.0 מ\"ר מרפסות גג", pos: new THREE.Vector3(0.0, 32.3, -4.5), cls: "ph" },
      { text: "רחוב חפץ חיים 44 (קו מגרש +19.41 · הפקעה 5.38 מ' · תוואי דרך +24.79)", pos: new THREE.Vector3(25.5, 1.4, 0.5), cls: "street" },
      { text: "מגרש 85-2 (38.82×18.40 מ') · קווי בניין: 5.05 מ' מזרח, 6.05 מ' מערב, 4.00 מ' צפון/דרום", pos: new THREE.Vector3(-15.0, 1.4, 7.5), cls: "" }
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
    // 7. 17-UNIT 3D CATALOG & LIVE CRM, PDF QUOTE GENERATOR
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

    HAFETZ_UNITS.forEach(u => {
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

      HAFETZ_UNITS.forEach(u => {
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
              <div style="font-size:10px;color:#475569;font-weight:600;">${u.area} מ"ר + ${u.balcony} מ"ר מרפסת · ${u.directions}</div>
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
        camState.spherical.theta = (u.bx < 0) ? -2.45 : 0.65;
        updateCameraFromOrbit();
      }

      const badgeCls = u.status === 'available' ? 'status-available' : 'status-owner';
      const downPayment20 = Math.round(u.price * 0.20);
      const balance80 = u.price - downPayment20;
      const estMonthlyMortgage = Math.round((u.price * 0.55) * 0.0055);
      const pStall = PARKING_STALLS.find(p => p.num === u.parkingNum);
      const pLevelTxt = (pStall && pStall.level === 'ground') ? 'קומת קרקע (±0.00)' : 'מרתף חניון (-5.10)';

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
        const targetFlr = (pStall && pStall.level === 'ground') ? 'kar' : 'mar';
        const targetZ = (targetFlr === 'kar') ? 0.72 : -4.35;
        selectFloor(targetFlr);
        if (parkingHighlightMesh) {
          parkingHighlightMesh.visible = true;
          parkingHighlightMesh.position.set(u.parkingX, targetZ, u.parkingY);
        }
        camState.target.set(u.parkingX, targetZ - 0.4, u.parkingY);
        camState.spherical = { radius: 22.0, phi: 0.62, theta: -1.6 };
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
  <title>הצעת מחיר ומפרט טכני — ${u.name} · חפץ חיים 44 פתח תקווה</title>
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
      <div class="logo">HH44</div>
      <div>
        <div style="font-size:20px;font-weight:900;color:#0f172a;">יצחק קולסקי חברה לבניה והשקעות בע"מ</div>
        <div style="font-size:13px;color:#475569;font-weight:700;">פרויקט בוטיק חפץ חיים 44, פתח תקווה · אדריכלות: סטודיו אורכה — אדר' אורן קמה</div>
      </div>
    </div>
    <div style="text-align:left;font-size:12px;color:#475569;">
      <div><b>תאריך הפקה:</b> ${todayStr}</div>
      <div><b>גוש 6396 חלקה 85</b> · 17 יח"ד</div>
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
        <tr><td><b>חניה צמודה בטאבו:</b></td><td>חניה מקורה #${u.parkingNum}</td></tr>
        <tr><td><b>מפרט פנים יוקרתי:</b></td><td>ריצוף גרניט פורצלן 100×100/80×80, מטבח יוקרה, תריסי אור חשמליים, מערכת מיזוג VRF</td></tr>
        <tr><td><b>תנאי תשלום יזמיים (20/80):</b></td><td>20% בחתימה (${formatILS(down20)}) · 80% במסירת חזקה (${formatILS(bal80)})</td></tr>
        <tr><td><b>נגישות ומוקדי סביבה:</b></td><td>מרחק הליכה מתיכון אחד העם, גן העצמאות, הקו האדום של הרכבת הקלה ומרכז פתח תקווה</td></tr>
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
      target: new THREE.Vector3(0.5, 8.0, 0.0),
      spherical: { radius: 480.0, phi: 0.60, theta: 0.68 },
      isDragging: false,
      isPanning: false,
      downX: 0, downY: 0, prevX: 0, prevY: 0,
      walkMode: false, yaw: 0, pitch: 0, keys: {}
    };

    const VIEW_PRESETS = {
      iso_east:       { theta: 0.68,  phi: 1.08, radius: 52.0,   target: [0.5, 14.5, 0.0], ortho: false, clip: 35.5 },
      iso_west:       { theta: -2.42, phi: 1.08, radius: 52.0,   target: [0.5, 14.5, 0.0], ortho: false, clip: 35.5 },
      gmaps_regional: { theta: 0.68,  phi: 0.56, radius: 1320.0, target: [0.5, 6.0, 0.0],  ortho: false, clip: 35.5 },
      gmaps_aerial:   { theta: 0.68,  phi: 0.60, radius: 480.0,  target: [0.5, 6.0, 0.0],  ortho: false, clip: 35.5 },
      gmaps_close:    { theta: 0.68,  phi: 0.66, radius: 145.0,  target: [0.5, 8.0, 0.0],  ortho: false, clip: 35.5 },
      top_plan:       { theta: -Math.PI/2, phi: 0.04, radius: 42.0, target: [0.5, 13.5, 0.0], ortho: true, clip: 15.8 }
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
      const fObj = FLOORS.find(f => f.id === floorId) || FLOORS[5];
      setSliceMode('single');
      selectFloor(fObj.id);
      setClipHeight(35.5);
      setOrthoMode(false);
      camState.target.set(0.5, fObj.zFloor + 1.0, 0.0);
      camState.spherical.radius = 34.0;
      camState.spherical.phi = 0.56;
      camState.spherical.theta = 1.25;
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
      const u = HAFETZ_UNITS.find(x => x.floorNum === floorNum && x.wing === wing) || HAFETZ_UNITS[0];
      selectedUnitObj = u;
      setSliceMode('single');
      selectFloor(u.floorId);
      const cx = (wing === 'W') ? -10.2 : ((wing === 'E') ? 11.2 : 0.0);
      const cy = 1.2;
      startWalkthroughAt(cx, u.z0 + 1.68, cy, (wing === 'W') ? -1.57 : 1.57, `${u.name} · ${u.typeHe} (${u.area}+${u.balcony} מ"ר)`, u.floorLabel);
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
      const bx = (flrNum === 9) ? 13.0 : 15.35;
      startWalkthroughAt(bx, fObj.zFloor + 1.68, 0.5, Math.PI / 2, `🔭 נוף פנורמי מהמרפסת לרחוב חפץ חיים — קומה ${flrNum} (+${fObj.zFloor.toFixed(2)} מ')`, fObj.label);
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
        camState.target.set(0.5, activeF ? activeF.zFloor + 1.2 : 12.0, 0.0);
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
      if (units3DVisible && camState.spherical.radius > 160) activatePreset('iso_east');
      syncUnits3DToggleUI();
    });
    document.getElementById('btn-drawer-units-3d').addEventListener('click', () => {
      units3DVisible = !units3DVisible;
      if (units3DVisible && camState.spherical.radius > 160) activatePreset('iso_east');
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
        ? '🗺️ מפת לוויין Google Maps (חפץ חיים 44): פעיל'
        : '🗺️ מפת לוויין Google Maps (חפץ חיים 44): כבוי';
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
        MATS.winGlass.emissive.setHex(0x000000);
        MATS.winGlass.emissiveIntensity = 0.0;
        MATS.winGlass.opacity = 0.42;
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
      clipVal.textContent = v >= 35.0 ? "+35.50 מ' (מלא)" : `${v >= 0 ? '+' : ''}${v.toFixed(2)} מ' (חתך)`;
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

      if (parkingHighlightMesh && floorId !== 'mar' && floorId !== 'kar') parkingHighlightMesh.visible = false;
      gisMapPlanesGroup.visible = gmapsVisible && (floorId !== 'mar');

      if (floorId === 'all') {
        document.getElementById('active-floor-label').textContent = 'מבנה שלם (כל הקומות)';
        FLOORS.forEach(f => { floorGroups[f.id].visible = true; });
        setClipHeight(35.5);
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
            camState.target.set(0.5, Math.max(-3, f.zFloor), 0.0);
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
      let objLines = ['# Hafetz Haim 44 Petah Tikva - 1:1 Metric Architectural BIM Model (Meters)'];
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
      a.download = 'hafetz44_model.obj';
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
          camState.target.y = Math.max(-8.0, Math.min(95.0, camState.target.y));
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
<!-- ARCHICHECK_3D_OVERLAY_START -->
<script>window.__ARCHICHECK_PROJECT_ID__ = "hafetz44";</script>
<script src="/audit_3d_overlay.js?v=6.4"></script>
<!-- ARCHICHECK_3D_OVERLAY_END -->
</body>
</html>
"""

HTML_TEMPLATE = HTML_PART1 + HTML_PART2

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

DIST_DIR = os.path.join(os.getcwd(), "dist", "projects", "hafetz-44")
os.makedirs(PUBLIC_DIR, exist_ok=True)
os.makedirs(DIST_DIR, exist_ok=True)
os.makedirs(DRIVE_MODEL_DIR, exist_ok=True)

targets = [
    os.path.join(ARTIFACT_DIR, "hafetz44_3d_bim_viewer.html"),
    os.path.join(ARTIFACT_DIR, "hafetz44_3d_model.html"),
    os.path.join(PUBLIC_DIR, "hafetz44_3d_bim_viewer.html"),
    os.path.join(PUBLIC_DIR, "hafetz44_3d_model.html"),
    os.path.join(PUBLIC_DIR, "index.html"),
    os.path.join(DIST_DIR, "hafetz44_3d_bim_viewer.html"),
    os.path.join(DIST_DIR, "hafetz44_3d_model.html"),
    os.path.join(DIST_DIR, "index.html"),
    os.path.join(DRIVE_MODEL_DIR, "hafetz44_3d_bim_viewer.html"),
    os.path.join(DRIVE_MODEL_DIR, "hafetz44_3d_model.html"),
    os.path.join(DRIVE_MODEL_DIR, "index.html"),
]

for p in targets:
    with open(p, "w", encoding="utf-8") as f:
        f.write(html_out)
    print("Wrote:", p, "Size:", os.path.getsize(p))

# Also copy hafetz44_spatial_map.html to PUBLIC_DIR and DRIVE_MODEL_DIR
spatial_src = os.path.join(ARTIFACT_DIR, "hafetz44_spatial_map.html")
if os.path.exists(spatial_src):
    for dst_dir in [PUBLIC_DIR, DRIVE_MODEL_DIR]:
        dst_p = os.path.join(dst_dir, "hafetz44_spatial_map.html")
        shutil.copy2(spatial_src, dst_p)
        print("Copied spatial map:", dst_p, "Size:", os.path.getsize(dst_p))
