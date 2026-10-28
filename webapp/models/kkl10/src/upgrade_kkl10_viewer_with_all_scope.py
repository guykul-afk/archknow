import json
import os

BRAIN_DIR = r"C:\Users\User\.gemini\antigravity\brain\17cdeb22-38a8-4e04-b15d-67ce64232225"
SCRATCH_DIR = r"C:\Users\User\.gemini\antigravity\scratch\kkl10"
GDRIVE_DIR = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\קקל 10 פתח תקווה"

orig_viewer_path = os.path.join(BRAIN_DIR, "kkl10_3d_bim_viewer.html")
with open(orig_viewer_path, "r", encoding="utf-8") as f:
    orig_lines = f.readlines()

start_idx = None
end_idx = None
for i, line in enumerate(orig_lines):
    if "const FLOOR_LEVELS = [" in line and start_idx is None:
        start_idx = i
    if "// WEBGL 3D RENDERING ENGINE" in line and end_idx is None:
        end_idx = i - 1

assert start_idx is not None and end_idx is not None, f"Could not find markers: {start_idx}, {end_idx}"
untouched_arch_model_js = "".join(orig_lines[start_idx:end_idx])
print(f"Extracted untouched architectural model JS: lines {start_idx+1} to {end_idx} ({len(untouched_arch_model_js)} chars)")

with open(os.path.join(SCRATCH_DIR, "data", "embedded_scope_data.js"), "r", encoding="utf-8") as f:
    embedded_scope_data_js = f.read()

with open(os.path.join(SCRATCH_DIR, "data", "unified_3d_map.json"), "r", encoding="utf-8") as f:
    unified_map = json.load(f)

map_constants_js = f"""
    const GMAPS_OUTER_Z15 = {json.dumps(unified_map["outer_z15"])};
    const GMAPS_INNER_Z17 = {json.dumps(unified_map["inner_z17"])};
    const GMAPS_CLOSE_Z19 = {json.dumps(unified_map["closeup_z19"])};
"""

HTML_HEADER_AND_UI = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>קק"ל 10, פתח תקווה — מערכת שיווק, מכירות והדמיית BIM תלת-ממדית אינטראקטיבית (1:50 CAD & GIS)</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    * { box-sizing: border-box; user-select: none; }
    body, html { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; direction: rtl; }
    #glCanvas { width: 100%; height: 100%; display: block; cursor: grab; position: absolute; top: 0; left: 0; z-index: 1; }
    #glCanvas:active { cursor: grabbing; }
    .glass-panel {
      background: rgba(15, 23, 42, 0.92);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid rgba(148, 163, 184, 0.25);
      color: #f8fafc;
      box-shadow: 0 14px 34px -6px rgba(0, 0, 0, 0.55);
    }
    .top-header {
      position: absolute;
      top: 10px;
      right: 12px;
      left: 12px;
      z-index: 30;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      border-radius: 14px;
      padding: 8px 14px;
    }
    .dropdown-drawer {
      display: none;
      position: absolute;
      top: 66px;
      right: 12px;
      z-index: 28;
      width: 420px;
      max-width: calc(100vw - 24px);
      max-height: calc(100vh - 115px);
      overflow-y: auto;
      border-radius: 14px;
      padding: 14px;
      animation: fadeSlideDown 0.16s ease-out;
    }
    .dropdown-drawer.open { display: block; }
    @keyframes fadeSlideDown {
      from { opacity: 0; transform: translateY(-6px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    .bottom-right-sections {
      position: absolute;
      bottom: 42px;
      right: 12px;
      z-index: 26;
      width: 345px;
      max-height: calc(100vh - 120px);
      overflow-y: auto;
      border-radius: 16px;
      padding: 12px 14px;
      border: 1px solid rgba(59, 130, 246, 0.45);
      background: rgba(15, 23, 42, 0.94);
      box-shadow: 0 16px 36px -6px rgba(0, 0, 0, 0.6);
      backdrop-filter: blur(14px);
      transition: all 0.2s ease;
    }
    .bottom-right-sections.collapsed .sections-body { display: none; }
    .menu-trigger-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border-radius: 10px;
      border: 1px solid rgba(148, 163, 184, 0.35);
      background: rgba(30, 41, 59, 0.9);
      color: #f8fafc;
      padding: 6px 11px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .menu-trigger-btn:hover { background: rgba(51, 65, 85, 0.95); border-color: #94a3b8; }
    .menu-trigger-btn.open {
      background: #2563eb;
      border-color: #60a5fa;
      color: #ffffff;
      box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.4);
    }
    .menu-trigger-btn.emerald-trigger {
      background: linear-gradient(135deg, #047857 0%, #059669 100%);
      border-color: #34d399;
      color: #ffffff;
    }
    .menu-trigger-btn.lux-trigger {
      background: linear-gradient(135deg, #b45309 0%, #d97706 100%);
      border-color: #fbbf24;
      color: #ffffff;
    }
    .ui-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      border-radius: 8px;
      border: 1px solid rgba(148, 163, 184, 0.3);
      background: rgba(30, 41, 59, 0.85);
      color: #e2e8f0;
      padding: 5px 10px;
      font-size: 11.5px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .ui-btn:hover { background: rgba(51, 65, 85, 0.95); border-color: #94a3b8; }
    .ui-btn.active { background: #2563eb; border-color: #60a5fa; color: #ffffff; }
    .unit-sales-card {
      display: none;
      position: absolute;
      top: 68px;
      left: 14px;
      z-index: 29;
      width: 385px;
      max-width: calc(100vw - 28px);
      max-height: calc(100vh - 115px);
      overflow-y: auto;
      background: rgba(15, 23, 42, 0.96);
      color: #ffffff;
      border: 1px solid rgba(56, 189, 248, 0.45);
      border-radius: 16px;
      padding: 14px;
      box-shadow: 0 20px 44px rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(14px);
    }
    .pkg-card-btn {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 3px;
      border-radius: 8px;
      border: 1px solid rgba(148, 163, 184, 0.3);
      background: rgba(30, 41, 59, 0.75);
      padding: 7px 9px;
      cursor: pointer;
      text-align: right;
      transition: all 0.15s ease;
      color: #f8fafc;
    }
    .pkg-card-btn:hover { border-color: #94a3b8; background: rgba(51, 65, 85, 0.85); }
    .pkg-card-btn.active { background: rgba(37, 99, 235, 0.25); border-color: #60a5fa; box-shadow: 0 0 0 1px #60a5fa; }
    input[type="range"] { accent-color: #3b82f6; cursor: pointer; }
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-thumb { background: rgba(148, 163, 184, 0.4); border-radius: 3px; }
  </style>
</head>
<body class="bg-[#09090b] text-[#f4f4f5] antialiased relative">

  <!-- 3D WebGL Viewport -->
  <canvas id="glCanvas"></canvas>

  <!-- 3D Overlay Containers for GIS Distance Rings, 46 POIs, 25 Apartment Badges & Laser Measure -->
  <div id="gis-rings-overlay" style="pointer-events:none;position:absolute;inset:0;overflow:hidden;z-index:5;"></div>
  <div id="gis-pois-overlay" style="pointer-events:none;position:absolute;inset:0;overflow:hidden;z-index:6;"></div>
  <div id="units-3d-overlay" style="pointer-events:none;position:absolute;inset:0;overflow:hidden;z-index:7;"></div>
  <div id="measure-overlay" style="pointer-events:none;position:absolute;inset:0;overflow:hidden;z-index:8;"></div>

  <!-- Active GIS POI Floating Card -->
  <div id="gis-active-card" style="display:none;position:absolute;bottom:48px;left:14px;z-index:28;width:335px;background:rgba(15,23,42,0.96);color:#ffffff;border:1px solid #38bdf8;border-radius:14px;padding:13px;box-shadow:0 14px 32px rgba(0,0,0,0.55);backdrop-filter:blur(12px);"></div>

  <!-- Floating Interactive Unit Sales & Financing Card (#unit-sales-card) -->
  <div id="unit-sales-card" class="unit-sales-card"></div>

  <!-- Floating 3D Laser Tape Measure HUD -->
  <div id="measure-hud" style="display:none;position:absolute;top:68px;left:50%;transform:translateX(-50%);z-index:27;background:rgba(15,23,42,0.95);color:#ffffff;border:1px solid #38bdf8;border-radius:999px;padding:6px 16px;font-size:12px;font-weight:700;box-shadow:0 8px 24px rgba(0,0,0,0.45);align-items:center;gap:10px;">
    <span>📏 <b>מד טווח לייזר 3D פעיל</b>: לחץ על 2 נקודות במודל למדידת מרחק מדויק</span>
    <span id="measure-last-val" style="background:#0284c7;color:#ffffff;padding:2px 9px;border-radius:999px;font-weight:800;">מוכן למדידה</span>
    <button onclick="clearMeasurements()" class="ui-btn" style="padding:2px 8px;font-size:11px;">נקה</button>
    <button onclick="toggleMeasureMode(false)" class="ui-btn" style="padding:2px 7px;font-size:11px;background:#ef4444;border-color:#dc2626;color:#fff;">✕</button>
  </div>

  <!-- Floating Balcony View / Walkthrough HUD -->
  <div id="walk-hud" style="display:none;position:absolute;bottom:48px;left:14px;z-index:27;background:rgba(15,23,42,0.95);border:1px solid #fbbf24;border-radius:14px;padding:10px 14px;box-shadow:0 12px 28px rgba(0,0,0,0.55);max-width:520px;">
    <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:6px;">
      <div style="display:flex;align-items:center;gap:8px;">
        <span style="background:#d97706;color:#fff;font-weight:900;font-size:11px;padding:2px 8px;border-radius:6px;" id="walk-hud-badge">קק"ל 10</span>
        <span style="font-weight:800;font-size:13px;color:#fde68a;" id="walk-hud-title">סימולטור נוף וסיור</span>
      </div>
      <button onclick="exitWalkMode()" class="ui-btn" style="background:#ef4444;border-color:#dc2626;color:#fff;padding:2px 8px;font-size:11px;font-weight:800;">✕ חזרה למודל</button>
    </div>
    <div style="display:flex;flex-wrap:wrap;align-items:center;gap:6px;font-size:11px;color:#cbd5e1;">
      <span>🖱️ גרירה: מבט 360°</span>
      <span>·</span>
      <span>בחר קומה לנוף:</span>
      <button onclick="simulateBalconyView(1,'N')" class="ui-btn" style="padding:2px 6px;font-size:10.5px;">ק'1</button>
      <button onclick="simulateBalconyView(3,'N')" class="ui-btn" style="padding:2px 6px;font-size:10.5px;">ק'3</button>
      <button onclick="simulateBalconyView(5,'N')" class="ui-btn" style="padding:2px 6px;font-size:10.5px;">ק'5</button>
      <button onclick="simulateBalconyView(7,'N')" class="ui-btn" style="padding:2px 6px;font-size:10.5px;">ק'7</button>
      <button onclick="simulateBalconyView(8,'N')" class="ui-btn" style="padding:2px 6px;font-size:10.5px;">פנטהאוז ק'8 צפון</button>
      <button onclick="simulateBalconyView(8,'S')" class="ui-btn" style="padding:2px 6px;font-size:10.5px;">פנטהאוז ק'8 דרום</button>
    </div>
  </div>

  <!-- ======================================================================= -->
  <!-- TOP HEADER BAR (CLEAN MARKETING STAGE + 4 POPOVER TRIGGERS)             -->
  <!-- ======================================================================= -->
  <header class="glass-panel top-header">
    <div style="display:flex;align-items:center;gap:10px;">
      <div style="display:flex;height:38px;width:48px;align-items:center;justify-content:center;border-radius:10px;background:linear-gradient(135deg,#f59e0b,#b45309);color:#09090b;font-weight:900;font-size:12px;border:1px solid #fde68a;">
        קק"ל 10
      </div>
      <div>
        <div style="display:flex;align-items:center;gap:7px;flex-wrap:wrap;">
          <h1 style="margin:0;font-size:14.5px;font-weight:900;color:#ffffff;">קבוצת קולסקי · קק"ל 10, פתח תקווה</h1>
          <span style="border-radius:6px;border:1px solid rgba(251,191,36,0.4);background:rgba(245,158,11,0.18);padding:1px 8px;font-size:10.5px;font-weight:800;color:#fde68a;">אדר' אייל סנדרוביץ' · גוש 6374 חלקה 112 · 25 יח"ד (v6.1 BIM)</span>
        </div>
        <div style="font-size:11px;color:#94a3b8;" id="activeFloorTitle">🏢 מבנה שלם על גבי מפת פתח תקווה | 25 דירות · 46 מוקדי GIS</div>
      </div>
    </div>

    <!-- Streamlined Marketing Action Bar & 4 On-Demand Dropdown Triggers -->
    <div style="display:flex;flex-wrap:wrap;align-items:center;gap:5px;">
      <button onclick="setCameraPreset('north_persp')" class="ui-btn" title="מבט חוץ תלת-ממדי מלא על הבניין">
        🏢 מבט הבניין
      </button>
      <button onclick="setCameraPreset('gis_aerial')" class="ui-btn active" id="btn-top-aerial" title="מבט רחפן על הבניין יושב על מפת העיר פתח תקווה ו-46 מוקדי הסביבה">
        🗺️ מפת סביבה
      </button>
      <button id="btn-top-gmaps" onclick="toggleGmapsGround()" class="ui-btn active" title="הצג/הסתר מפת לוויין Google Maps של פתח תקווה כבסיס למודל">
        🌍 מפת פ"ת: פעיל
      </button>
      <button id="btn-top-units3d" onclick="toggleUnits3D()" class="ui-btn" style="border-color:#10b981;color:#6ee7b7;background:rgba(16,185,129,0.15);font-weight:800;" title="הצג/הסתר סימון 25 דירות תלת-ממדי לפי זמינות ומחיר">
        🏢 סימון דירות 3D
      </button>
      <button id="btn-top-radii" onclick="toggleGisRadii()" class="ui-btn active" title="הדלק/כבה 8 מעגלי מרחק וזמני הליכה סביב קק"ל 10">
        ⭕ רדיוסים: פעיל
      </button>
      <button id="btn-top-pois" onclick="toggleGisPois()" class="ui-btn active" title="הדלק/כבה 46 מוקדי סביבה בפתח תקווה">
        📍 מיקומים: פעיל
      </button>
      <button id="btn-top-night" onclick="toggleNightMode()" class="ui-btn" title="מצב תאורת לילה / שעת הזהב">
        🌙 מצב לילה
      </button>
      <button id="btn-top-measure" onclick="toggleMeasureMode()" class="ui-btn" title="מד טווח לייזר תלת-ממדי למדידת מרחקים בדירה ובבניין">
        📏 מדידה
      </button>

      <!-- 4 On-Demand Popover Triggers (Closed by default) -->
      <button onclick="toggleDrawer('drawer-units', this)" class="menu-trigger-btn emerald-trigger">
        <span>🏷️ קטלוג דירות ומחירים (25)</span>
        <span style="font-size:10px;">▾</span>
      </button>
      <button onclick="toggleDrawer('drawer-apartments', this)" class="menu-trigger-btn lux-trigger">
        <span>✨ תוכניות, סיור ונוף מהמרפסת</span>
        <span style="font-size:10px;">▾</span>
      </button>
      <button onclick="toggleDrawer('drawer-gis', this)" class="menu-trigger-btn">
        <span>📍 מוקדי סביבה (46)</span>
        <span style="font-size:10px;">▾</span>
      </button>
      <button onclick="toggleDrawer('drawer-settings', this)" class="menu-trigger-btn">
        <span>⚙️ עיצוב, גמר ושכבות</span>
        <span style="font-size:10px;">▾</span>
      </button>
    </div>
  </header>

  <!-- ======================================================================= -->
  <!-- DRAWER 1: 25 UNITS CATALOG & LIVE CRM (CLOSED BY DEFAULT)               -->
  <!-- ======================================================================= -->
  <div id="drawer-units" class="glass-panel dropdown-drawer">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;border-bottom:1px solid rgba(148,163,184,0.2);padding-bottom:6px;">
      <div>
        <div style="font-size:13.5px;font-weight:800;color:#6ee7b7;">🏷️ קטלוג 25 הדירות והמחירון הרשמי — קק"ל 10, פתח תקווה</div>
        <div style="font-size:11px;color:#94a3b8;">נתוני אמת ממסמך מלאי הדירות · לחץ על דירה לכרטיס מכירה והצעת מחיר PDF</div>
      </div>
      <button onclick="closeAllDrawers()" class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
    </div>

    <!-- Inventory KPI Summary -->
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-bottom:8px;text-align:center;">
      <div style="background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.4);border-radius:8px;padding:5px;">
        <div style="font-size:10px;color:#6ee7b7;font-weight:700;">🟢 מלאי קולסקי זמין</div>
        <div style="font-size:14px;font-weight:900;color:#34d399;">15 דירות</div>
      </div>
      <div style="background:rgba(245,158,11,0.15);border:1px solid rgba(245,158,11,0.4);border-radius:8px;padding:5px;">
        <div style="font-size:10px;color:#fde68a;font-weight:700;">🟡 שמורה / מכר</div>
        <div style="font-size:14px;font-weight:900;color:#fbbf24;">1 דירה</div>
      </div>
      <div style="background:rgba(148,163,184,0.12);border:1px solid rgba(148,163,184,0.3);border-radius:8px;padding:5px;">
        <div style="font-size:10px;color:#cbd5e1;font-weight:700;">🔒 דירות בעלים</div>
        <div style="font-size:14px;font-weight:900;color:#f8fafc;">9 דירות</div>
      </div>
    </div>

    <!-- 3D Volume Highlight & Price Visibility Controls -->
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:8px;">
      <button id="btn-drawer-units3d" onclick="toggleUnits3D()" class="ui-btn" style="background:#059669;color:#ffffff;border-color:#10b981;font-weight:800;">
        🏢 הדגש דירות 3D על הבניין
      </button>
      <button id="btn-toggle-prices" onclick="togglePriceVisibility()" class="ui-btn active" style="font-weight:700;">
        👁️ מחירים: מוצג
      </button>
    </div>

    <!-- Status Filters -->
    <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:6px;" id="unit-status-filters">
      <button onclick="setUnitStatusFilter('all', this)" class="ui-btn active" style="padding:3px 8px;font-size:10.5px;">כל הדירות (25)</button>
      <button onclick="setUnitStatusFilter('available', this)" class="ui-btn" style="padding:3px 8px;font-size:10.5px;">🟢 פנויות קולסקי (15)</button>
      <button onclick="setUnitStatusFilter('owner', this)" class="ui-btn" style="padding:3px 8px;font-size:10.5px;">🔒 בעלים/שמורות (10)</button>
    </div>

    <!-- Room / Typology Filters -->
    <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px;" id="unit-room-filters">
      <button onclick="setUnitRoomFilter('all', this)" class="ui-btn active" style="padding:3px 8px;font-size:10.5px;">כל הטיפוסים</button>
      <button onclick="setUnitRoomFilter('garden', this)" class="ui-btn" style="padding:3px 8px;font-size:10.5px;">🌳 דירות גן (2)</button>
      <button onclick="setUnitRoomFilter('4', this)" class="ui-btn" style="padding:3px 8px;font-size:10.5px;">4 חד' (106–114 מ"ר)</button>
      <button onclick="setUnitRoomFilter('5', this)" class="ui-btn" style="padding:3px 8px;font-size:10.5px;">5 חד' (122–129 מ"ר)</button>
      <button onclick="setUnitRoomFilter('ph', this)" class="ui-btn" style="padding:3px 8px;font-size:10.5px;">👑 פנטהאוזים (2)</button>
    </div>

    <div id="units-catalog-list" style="max-height:290px;overflow-y:auto;display:flex;flex-direction:column;gap:5px;padding-left:2px;"></div>
  </div>

  <!-- ======================================================================= -->
  <!-- DRAWER 2: FLOOR PLANS, INTERIOR WALKTHROUGH & BALCONY VIEW SIMULATOR    -->
  <!-- ======================================================================= -->
  <div id="drawer-apartments" class="glass-panel dropdown-drawer">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;border-bottom:1px solid rgba(148,163,184,0.2);padding-bottom:6px;">
      <div>
        <div style="font-size:13.5px;font-weight:800;color:#fde68a;">✨ חתכי תוכניות מכר 1:50 וסימולטור נוף מהמרפסת</div>
        <div style="font-size:11px;color:#94a3b8;">תוכניות דירה מלאות עם ארונות עץ בהיר, דלתות ומידות חדרים על הרצפה</div>
      </div>
      <button onclick="closeAllDrawers()" class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
    </div>

    <div style="font-size:11.5px;font-weight:800;color:#fbbf24;margin-bottom:5px;">📐 מעבר מהיר לתוכניות קומה תלת-ממדיות (1:50 CAD):</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-bottom:10px;">
      <button onclick="viewFloorPlan(0);closeAllDrawers();" class="ui-btn">🌳 קומת קרקע L0 (דירות גן G-1, G-2)</button>
      <button onclick="viewFloorPlan(1);closeAllDrawers();" class="ui-btn">📐 קומות 1–2 (טיפוסים A, B, C)</button>
      <button onclick="viewFloorPlan(3);closeAllDrawers();" class="ui-btn">📐 קומות 3–4 (טיפוסים E, B, D)</button>
      <button onclick="viewFloorPlan(5);closeAllDrawers();" class="ui-btn">📐 קומה 5 (טיפוסים F, B, G)</button>
      <button onclick="viewFloorPlan(6);closeAllDrawers();" class="ui-btn">📐 קומות 6–7 (טיפוסים A, B, H)</button>
      <button onclick="viewFloorPlan(8);closeAllDrawers();" class="ui-btn" style="background:rgba(245,158,11,0.25);border-color:#fbbf24;color:#fde68a;font-weight:800;">👑 קומה 8 פנטהאוזים (PH-1, PH-2)</button>
      <button onclick="viewFloorPlan(-1);closeAllDrawers();" class="ui-btn">🚗 מרתף 1- (16 חניות ומחסנים)</button>
      <button onclick="viewFloorPlan(-2);closeAllDrawers();" class="ui-btn">🚗 מרתף 2- (18 חניות ומאגר מים)</button>
    </div>

    <div style="font-size:11.5px;font-weight:800;color:#38bdf8;margin-bottom:5px;">🔭 סימולטור "נוף מהמרפסת" לפי קומה וכיוון (קומות 1–8):</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-bottom:8px;">
      <button onclick="simulateBalconyView(1,'N');closeAllDrawers();" class="ui-btn">קומה 1 (+4.20) · מרפסת צפונית</button>
      <button onclick="simulateBalconyView(1,'S');closeAllDrawers();" class="ui-btn">קומה 1 (+4.20) · מרפסת דרומית</button>
      <button onclick="simulateBalconyView(3,'N');closeAllDrawers();" class="ui-btn">קומה 3 (+10.50) · מרפסת צפונית</button>
      <button onclick="simulateBalconyView(3,'S');closeAllDrawers();" class="ui-btn">קומה 3 (+10.50) · מרפסת דרומית</button>
      <button onclick="simulateBalconyView(5,'N');closeAllDrawers();" class="ui-btn">קומה 5 (+16.80) · מרפסת צפונית</button>
      <button onclick="simulateBalconyView(5,'S');closeAllDrawers();" class="ui-btn">קומה 5 (+16.80) · מרפסת דרומית</button>
      <button onclick="simulateBalconyView(7,'N');closeAllDrawers();" class="ui-btn">קומה 7 (+23.10) · מרפסת צפונית</button>
      <button onclick="simulateBalconyView(7,'S');closeAllDrawers();" class="ui-btn">קומה 7 (+23.10) · מרפסת דרומית</button>
      <button onclick="simulateBalconyView(8,'N');closeAllDrawers();" class="ui-btn" style="border-color:#38bdf8;color:#7dd3fc;font-weight:800;">👑 פנטהאוז PH-1 (+26.50) · צפון</button>
      <button onclick="simulateBalconyView(8,'S');closeAllDrawers();" class="ui-btn" style="border-color:#38bdf8;color:#7dd3fc;font-weight:800;">👑 פנטהאוז PH-2 (+26.50) · דרום</button>
    </div>
  </div>

  <!-- ======================================================================= -->
  <!-- DRAWER 3: 3D GIS SPATIAL MAP & 46 PETAH TIKVA POIS (CLOSED BY DEFAULT)  -->
  <!-- ======================================================================= -->
  <div id="drawer-gis" class="glass-panel dropdown-drawer">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;border-bottom:1px solid rgba(148,163,184,0.2);padding-bottom:6px;">
      <div>
        <div style="font-size:13.5px;font-weight:800;color:#60a5fa;">📍 מפת מרחקים ו-46 מוקדי סביבה בפתח תקווה (GIS)</div>
        <div style="font-size:11px;color:#94a3b8;">חינוך, תחבורה ומטרו M2, קניות, בריאות ופארקים סביב קק"ל 10</div>
      </div>
      <button onclick="closeAllDrawers()" class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-bottom:8px;">
      <button onclick="setCameraPreset('gis_regional')" class="ui-btn" style="background:#1e3a8a;color:#fff;border-color:#3b82f6;font-weight:700;">
        🌍 כל המיקומים (2.4 ק"מ)
      </button>
      <button onclick="setCameraPreset('gis_aerial')" class="ui-btn" style="font-weight:700;">
        🗺️ רדיוס שכונתי (800 מ')
      </button>
      <button onclick="setCameraPreset('north_persp')" class="ui-btn">
        🏢 תקריב הבניין (קק"ל 10)
      </button>
      <a href="kkl10_spatial_map.html" target="_blank" class="ui-btn" style="background:#0f172a;color:#38bdf8;border-color:#38bdf8;font-weight:800;text-decoration:none;">
        🧭 מפת GIS דו-ממדית (46) ↗
      </a>
    </div>

    <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px;" id="gis-cat-buttons">
      <button onclick="setGisCategory('all', this)" class="ui-btn active" style="padding:3px 7px;font-size:10.5px;">הכל (46)</button>
      <button onclick="setGisCategory('education', this)" class="ui-btn" style="padding:3px 7px;font-size:10.5px;">🎓 חינוך (13)</button>
      <button onclick="setGisCategory('transport', this)" class="ui-btn" style="padding:3px 7px;font-size:10.5px;">🚌 תחבורה ומטרו (10)</button>
      <button onclick="setGisCategory('shopping', this)" class="ui-btn" style="padding:3px 7px;font-size:10.5px;">🛒 קניות ומסחר (10)</button>
      <button onclick="setGisCategory('health', this)" class="ui-btn" style="padding:3px 7px;font-size:10.5px;">🏥 בריאות (7)</button>
      <button onclick="setGisCategory('parks', this)" class="ui-btn" style="padding:3px 7px;font-size:10.5px;">🌳 פארקים ותרבות (6)</button>
    </div>

    <div id="gis-poi-list" style="max-height:260px;overflow-y:auto;display:flex;flex-direction:column;gap:4px;padding-left:2px;"></div>
  </div>

  <!-- ======================================================================= -->
  <!-- DRAWER 4: FINISH PACKAGES, BIM LAYERS & EXPORT (CLOSED BY DEFAULT)      -->
  <!-- ======================================================================= -->
  <div id="drawer-settings" class="glass-panel dropdown-drawer">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;border-bottom:1px solid rgba(148,163,184,0.2);padding-bottom:6px;">
      <span style="font-size:13.5px;font-weight:800;color:#ffffff;">⚙️ חבילות גמר פנים, שכבות BIM וייצוא קבצים</span>
      <button onclick="closeAllDrawers()" class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
    </div>

    <!-- Real-Time 4 Interior Finish Packages Customizer -->
    <div style="background:rgba(30,41,59,0.6);border:1px solid rgba(148,163,184,0.25);border-radius:10px;padding:9px;margin-bottom:8px;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
        <span style="font-size:12px;font-weight:800;color:#fde68a;">🎨 4 חבילות ריצוף וגמר פנים (מפרט קולסקי)</span>
        <span id="active-pkg-badge" style="font-size:10px;font-weight:800;background:rgba(245,158,11,0.2);color:#fbbf24;padding:1px 6px;border-radius:4px;">Nordic Oak</span>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:5px;" id="pkg-buttons">
        <button onclick="applyFinishPackage('nordic', this)" class="pkg-card-btn active">
          <div style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:800;">
            <span style="width:11px;height:11px;border-radius:999px;background:#efede6;border:1px solid #d97706;"></span>
            <span>1. Nordic Oak</span>
          </div>
          <span style="font-size:9.5px;color:#94a3b8;">פורצלן שמנת וארונות אלון בהיר</span>
        </button>
        <button onclick="applyFinishPackage('sahara', this)" class="pkg-card-btn">
          <div style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:800;">
            <span style="width:11px;height:11px;border-radius:999px;background:#ebd9c0;border:1px solid #b45309;"></span>
            <span>2. Warm Sahara</span>
          </div>
          <span style="font-size:9.5px;color:#94a3b8;">טרוורטין חם ונגרות קשמיר-אגוז</span>
        </button>
        <button onclick="applyFinishPackage('urban', this)" class="pkg-card-btn">
          <div style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:800;">
            <span style="width:11px;height:11px;border-radius:999px;background:#d1d5db;border:1px solid #64748b;"></span>
            <span>3. Urban Anthracite</span>
          </div>
          <span style="font-size:9.5px;color:#94a3b8;">פורצלן אפור בטון ומייפל מולבן</span>
        </button>
        <button onclick="applyFinishPackage('parquet', this)" class="pkg-card-btn">
          <div style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:800;">
            <span style="width:11px;height:11px;border-radius:999px;background:#dfc49b;border:1px solid #92400e;"></span>
            <span>4. Classic Parquet</span>
          </div>
          <span style="font-size:9.5px;color:#94a3b8;">ריצוף פרקט אלון חם ונגרות טבעית</span>
        </button>
      </div>
    </div>

    <!-- Camera & Display Controls -->
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-bottom:8px;">
      <button onclick="toggleOrtho()" id="orthoBtn" class="ui-btn">📐 היטל: פרספקטיבה</button>
      <button onclick="toggleWireframe()" id="wireBtn" class="ui-btn active">🔲 קווי מתאר: פעיל</button>
      <button onclick="setCameraPreset('east_ortho')" class="ui-btn">חזית מזרחית (אורתוגרפי)</button>
      <button onclick="setCameraPreset('south_persp')" class="ui-btn">חזית דרומית (מרפסות)</button>
    </div>

    <!-- BIM Model Layers -->
    <div style="background:rgba(30,41,59,0.6);border:1px solid rgba(148,163,184,0.25);border-radius:10px;padding:9px;margin-bottom:8px;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:5px;">
        <span style="font-size:11.5px;font-weight:800;color:#cbd5e1;">שכבות המודל האדריכלי (BIM Layers)</span>
        <button onclick="toggleAllLayers(true)" style="font-size:10.5px;color:#60a5fa;background:none;border:none;cursor:pointer;">הצג הכל</button>
      </div>
      <div class="space-y-1 text-xs" id="layerList">
        <label class="flex items-center justify-between p-1 rounded hover:bg-white/5 cursor-pointer">
          <span class="flex items-center gap-2">
            <input type="checkbox" checked onchange="toggleLayer('Basements', this.checked)" class="rounded" />
            <span class="w-2.5 h-2.5 rounded-sm bg-blue-600 inline-block"></span>
            <span>1. מרתפים (-1/-2, רמפות, 34 חניות)</span>
          </span>
          <span class="text-slate-400 font-mono">-9.07..0.0</span>
        </label>
        <label class="flex items-center justify-between p-1 rounded hover:bg-white/5 cursor-pointer">
          <span class="flex items-center gap-2">
            <input type="checkbox" checked onchange="toggleLayer('MainStructure', this.checked)" class="rounded" />
            <span class="w-2.5 h-2.5 rounded-sm bg-stone-100 inline-block"></span>
            <span>2. מעטפת קירות חוץ ותקרות (L0–L8)</span>
          </span>
          <span class="text-slate-400 font-mono">B,C,E</span>
        </label>
        <label class="flex items-center justify-between p-1 rounded hover:bg-white/5 cursor-pointer">
          <span class="flex items-center gap-2">
            <input type="checkbox" checked onchange="toggleLayer('InteriorWalls', this.checked)" class="rounded" />
            <span class="w-2.5 h-2.5 rounded-sm bg-amber-200 inline-block"></span>
            <span>3. קירות פנים, ממ"דים ומשקופי דלתות</span>
          </span>
          <span class="text-slate-400 font-mono">1:50</span>
        </label>
        <label class="flex items-center justify-between p-1 rounded hover:bg-white/5 cursor-pointer">
          <span class="flex items-center gap-2">
            <input type="checkbox" checked onchange="toggleLayer('CoreStairsElev', this.checked)" class="rounded" />
            <span class="w-2.5 h-2.5 rounded-sm bg-purple-400 inline-block"></span>
            <span>4. גרעין חדר מדרגות ו-2 מעליות</span>
          </span>
          <span class="text-slate-400 font-mono">Core</span>
        </label>
        <label class="flex items-center justify-between p-1 rounded hover:bg-white/5 cursor-pointer">
          <span class="flex items-center gap-2">
            <input type="checkbox" checked onchange="toggleLayer('FloorPlanCAD', this.checked)" class="rounded" />
            <span class="w-2.5 h-2.5 rounded-sm bg-amber-500 inline-block"></span>
            <span>5. ארונות עץ בהיר, ריהוט ומידות רצפה</span>
          </span>
          <span class="text-slate-400 font-mono">CAD 2D</span>
        </label>
        <label class="flex items-center justify-between p-1 rounded hover:bg-white/5 cursor-pointer">
          <span class="flex items-center gap-2">
            <input type="checkbox" checked onchange="toggleLayer('FacadeOpenings', this.checked)" class="rounded" />
            <span class="w-2.5 h-2.5 rounded-sm bg-sky-300 inline-block"></span>
            <span>6. חלונות, ויטרינות (A) ורפפות (D)</span>
          </span>
          <span class="text-slate-400 font-mono">Glazing</span>
        </label>
        <label class="flex items-center justify-between p-1 rounded hover:bg-white/5 cursor-pointer">
          <span class="flex items-center gap-2">
            <input type="checkbox" checked onchange="toggleLayer('BalconiesRailings', this.checked)" class="rounded" />
            <span class="w-2.5 h-2.5 rounded-sm bg-cyan-400 inline-block"></span>
            <span>7. מרפסות ומעקות זכוכית</span>
          </span>
          <span class="text-slate-400 font-mono">L1–L8</span>
        </label>
        <label class="flex items-center justify-between p-1 rounded hover:bg-white/5 cursor-pointer">
          <span class="flex items-center gap-2">
            <input type="checkbox" checked onchange="toggleLayer('RoofParapets', this.checked)" class="rounded" />
            <span class="w-2.5 h-2.5 rounded-sm bg-zinc-400 inline-block"></span>
            <span>8. גג טכני (+31.40) ופרגולות (F)</span>
          </span>
          <span class="text-slate-400 font-mono">Roof</span>
        </label>
      </div>
    </div>

    <!-- Sun Direction & Export -->
    <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;">
      <div style="flex:1;">
        <div style="display:flex;justify-content:space-between;font-size:11px;color:#cbd5e1;">
          <span>☀️ זווית שמש ותאורה</span>
          <span id="sun-val" style="color:#fbbf24;font-weight:700;">13:30 · צהריים</span>
        </div>
        <input type="range" id="sunSlider" min="15" max="165" value="65" style="width:100%;" oninput="updateSunAngle(this.value)" />
      </div>
      <button onclick="exportOBJ()" class="ui-btn" style="background:#2563eb;color:#fff;border-color:#60a5fa;font-weight:800;">⬇ .OBJ</button>
      <button onclick="downloadThreeJSGenerator()" class="ui-btn" style="background:#059669;color:#fff;border-color:#34d399;font-weight:800;">⬇ .JS</button>
    </div>
  </div>

  <!-- ======================================================================= -->
  <!-- BOTTOM-RIGHT SECTIONS & FLOOR SLICER PANEL (OPEN BY DEFAULT)            -->
  <!-- ======================================================================= -->
  <aside id="sections-panel" class="bottom-right-sections">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
      <div style="display:flex;align-items:center;gap:7px;">
        <span style="display:inline-flex;height:24px;width:24px;align-items:center;justify-content:center;border-radius:6px;background:#2563eb;color:#ffffff;font-size:12px;font-weight:800;">✂️</span>
        <div>
          <div style="font-size:13px;font-weight:800;color:#ffffff;line-height:1.15;">חתכי קומות ותוכניות (Dollhouse)</div>
          <div style="font-size:10.5px;color:#94a3b8;" id="activeFloorDesc">בחר קומה לתוכנית 1:50 או הזז מחווני חיתוך</div>
        </div>
      </div>
      <button onclick="toggleSectionsPanel(this)" class="ui-btn" style="padding:2px 8px;font-size:11px;" title="מזער/הרחב חלון חתכים">▾</button>
    </div>

    <div class="sections-body space-y-2 text-xs">
      <div style="display:flex;align-items:center;justify-content:space-between;background:rgba(30,41,59,0.7);padding:5px 8px;border-radius:8px;border:1px solid rgba(148,163,184,0.2);">
        <span style="font-weight:700;color:#e2e8f0;">בידוד קומה בודדת (Single Floor):</span>
        <input type="checkbox" id="isolateFloorCb" onchange="updateClipping()" class="rounded" />
      </div>

      <div>
        <div class="flex justify-between mb-0.5">
          <span>מפלס חתך גובה (Y Max)</span>
          <span id="clipYVal" class="font-mono text-blue-400" style="direction:ltr;">+32.00 m</span>
        </div>
        <input type="range" id="clipY" min="-9.0" max="32.0" step="0.10" value="32.0" class="w-full" oninput="updateClipping()" />
      </div>

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
        <div>
          <div class="flex justify-between mb-0.5" style="font-size:10.5px;">
            <span>חתך 1-1 (מזרח↔מערב)</span>
            <span id="clipXVal" class="font-mono text-blue-400" style="direction:ltr;">+17.0m</span>
          </div>
          <input type="range" id="clipX" min="-4.0" max="17.0" step="0.15" value="17.0" class="w-full" oninput="updateClipping()" />
        </div>
        <div>
          <div class="flex justify-between mb-0.5" style="font-size:10.5px;">
            <span>חתך 2-2 (דרום↔צפון)</span>
            <span id="clipZVal" class="font-mono text-blue-400" style="direction:ltr;">+38.0m</span>
          </div>
          <input type="range" id="clipZ" min="-4.0" max="38.0" step="0.15" value="38.0" class="w-full" oninput="updateClipping()" />
        </div>
      </div>

      <div style="display:flex;gap:5px;padding-top:2px;">
        <button onclick="resetClipping();setCameraPreset('north_persp');" class="ui-btn" style="flex:1;background:#2563eb;color:#fff;border-color:#60a5fa;font-weight:800;">🏢 מבנה שלם (כל הקומות)</button>
      </div>

      <div style="border-top:1px solid rgba(148,163,184,0.2);padding-top:6px;">
        <div style="font-size:10.5px;font-weight:800;color:#fbbf24;margin-bottom:4px;">קפיצה מהירה לתוכנית קומה (1:50):</div>
        <div id="floorScheduleList" style="display:grid;grid-template-columns:1fr 1fr;gap:4px;"></div>
      </div>
    </div>
  </aside>

  <!-- On-Screen 3D Navigation Controller (Up / Down / Left / Right / Elevation / Drag Mode) -->
  <div id="nav-dpad-panel" class="glass-panel" style="position:absolute;bottom:44px;left:14px;z-index:25;padding:9px;border-radius:14px;display:flex;flex-direction:column;gap:6px;width:166px;user-select:none;">
    <div style="display:flex;align-items:center;justify-content:space-between;gap:4px;">
      <span style="font-size:10.5px;font-weight:800;color:#fbbf24;">🧭 תנועה והזזה במודל</span>
      <button id="btn-drag-mode" onclick="togglePrimaryDragMode()" class="ui-btn" style="padding:2px 6px;font-size:10px;" title="החלף פעולת גרירה שמאלית בין סיבוב להזזה">
        🔄 גרירה: סיבוב
      </button>
    </div>

    <!-- 3x3 D-Pad Grid (Up / Down / Right / Left / Center) -->
    <div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:4px;direction:ltr;">
      <button onmousedown="startHoldNav('elev', 1)" onmouseup="stopHoldNav()" onmouseleave="stopHoldNav()" ontouchstart="startHoldNav('elev', 1);event.preventDefault();" ontouchend="stopHoldNav()" class="ui-btn" style="padding:5px 0;font-size:10px;" title="הגבה מבט (+Y)">🔼 גובה</button>
      <button onmousedown="startHoldNav('up', 1)" onmouseup="stopHoldNav()" onmouseleave="stopHoldNav()" ontouchstart="startHoldNav('up', 1);event.preventDefault();" ontouchend="stopHoldNav()" class="ui-btn active" style="padding:5px 0;font-size:13px;font-weight:900;" title="נוע למעלה (חץ למעלה / W)">⬆️</button>
      <button onmousedown="startHoldNav('zoom', -1)" onmouseup="stopHoldNav()" onmouseleave="stopHoldNav()" ontouchstart="startHoldNav('zoom', -1);event.preventDefault();" ontouchend="stopHoldNav()" class="ui-btn" style="padding:5px 0;font-size:11px;" title="זום פנימה (+)">➕</button>

      <button onmousedown="startHoldNav('left', 1)" onmouseup="stopHoldNav()" onmouseleave="stopHoldNav()" ontouchstart="startHoldNav('left', 1);event.preventDefault();" ontouchend="stopHoldNav()" class="ui-btn active" style="padding:5px 0;font-size:13px;font-weight:900;" title="נוע שמאלה (חץ שמאלה / A)">⬅️</button>
      <button onclick="setCameraPreset('south_persp')" class="ui-btn" style="padding:5px 0;font-size:11px;font-weight:800;" title="מרכז חזרה למודל קק״ל 10">🎯</button>
      <button onmousedown="startHoldNav('right', 1)" onmouseup="stopHoldNav()" onmouseleave="stopHoldNav()" ontouchstart="startHoldNav('right', 1);event.preventDefault();" ontouchend="stopHoldNav()" class="ui-btn active" style="padding:5px 0;font-size:13px;font-weight:900;" title="נוע ימינה (חץ ימינה / D)">➡️</button>

      <button onmousedown="startHoldNav('elev', -1)" onmouseup="stopHoldNav()" onmouseleave="stopHoldNav()" ontouchstart="startHoldNav('elev', -1);event.preventDefault();" ontouchend="stopHoldNav()" class="ui-btn" style="padding:5px 0;font-size:10px;" title="הנמך מבט (-Y)">🔽 גובה</button>
      <button onmousedown="startHoldNav('down', 1)" onmouseup="stopHoldNav()" onmouseleave="stopHoldNav()" ontouchstart="startHoldNav('down', 1);event.preventDefault();" ontouchend="stopHoldNav()" class="ui-btn active" style="padding:5px 0;font-size:13px;font-weight:900;" title="נוע למטה (חץ למטה / S)">⬇️</button>
      <button onmousedown="startHoldNav('zoom', 1)" onmouseup="stopHoldNav()" onmouseleave="stopHoldNav()" ontouchstart="startHoldNav('zoom', 1);event.preventDefault();" ontouchend="stopHoldNav()" class="ui-btn" style="padding:5px 0;font-size:11px;" title="זום החוצה (-)">➖</button>
    </div>
    <div style="font-size:9.5px;color:#94a3b8;text-align:center;">
      חיצי מקלדת / WASD / גרירה ימנית להזזה
    </div>
  </div>

  <!-- Bottom Status Bar -->
  <div class="absolute bottom-2 left-3 right-3 flex items-center justify-between px-3.5 py-1.5 glass-panel rounded-xl text-[11px] pointer-events-none z-20">
    <div class="flex items-center gap-3">
      <span><b>שליטה במודל:</b> חיצי מקלדת / WASD / גרירה ימנית = הזזה (למעלה/למטה/ימינה/שמאלה) | גרירה שמאלית = סיבוב/הזזה | גלגלת = זום</span>
      <span id="statsText" class="text-slate-400">Initializing geometry...</span>
    </div>
    <div class="font-mono text-emerald-400">קק"ל 10 פ"ת · מפת לוויין Google Maps תלת-ממדית · 25 יח"ד · 46 מוקדי GIS · הצעות מחיר PDF</div>
  </div>

  <script>
"""

WEBGL_AND_SCOPE_JS = """
    // ============================================================================
    // WEBGL 3D RENDERING ENGINE + TRIPLE-RESOLUTION PETAH TIKVA GOOGLE MAPS BASE
    // + FULL MARKETING, CRM, GIS & PDF SCOPE EXTENSIONS
    // (100% Untouched Architectural BIM Geometry in buildKKL10Model)
    // ============================================================================
    const canvas = document.getElementById('glCanvas');
    const gl = canvas.getContext('webgl', { antialias: true, alpha: false, preserveDrawingBuffer: true });

    const vsSource = `
      attribute vec3 aPos;
      attribute vec3 aNorm;
      attribute vec4 aCol;
      uniform mat4 uProj;
      uniform mat4 uView;
      varying vec3 vNorm;
      varying vec3 vWorldPos;
      varying vec4 vCol;
      void main() {
        vWorldPos = aPos;
        vNorm = aNorm;
        vCol = aCol;
        gl_Position = uProj * uView * vec4(aPos, 1.0);
      }
    `;

    const fsSource = `
      precision highp float;
      varying vec3 vNorm;
      varying vec3 vWorldPos;
      varying vec4 vCol;
      uniform vec4 uClipBounds; // xMax, yMin, yMax, nMax
      uniform int uIsLine;      // 0 = lit triangle, 1 = clipped line, 2 = unclipped GIS/CRM line, 3 = unclipped translucent box
      uniform vec3 uSunDir;
      uniform float uNightMix;
      void main() {
        if (uIsLine < 2) {
          if (vWorldPos.x > uClipBounds.x || vWorldPos.y < uClipBounds.y || vWorldPos.y > uClipBounds.z || (-vWorldPos.z) > uClipBounds.w) {
            discard;
          }
        }
        if (uIsLine == 1 || uIsLine == 2) {
          gl_FragColor = vCol;
          return;
        }
        vec3 n = normalize(vNorm);
        vec3 lightDir1 = normalize(uSunDir);
        vec3 lightDir2 = normalize(vec3(-0.60, 0.55, 0.50));
        float diff1 = max(dot(n, lightDir1), 0.0);
        float diff2 = max(dot(n, lightDir2), 0.0) * 0.38;
        float amb = (0.52 + 0.12 * n.y) * (1.0 - 0.38 * uNightMix);
        vec3 lit = vCol.rgb * min(amb + diff1 * (0.48 - 0.15 * uNightMix) + diff2, 1.12);
        if (uNightMix > 0.01) {
          lit *= vec3(0.85, 0.90, 1.08);
        }
        gl_FragColor = vec4(lit, vCol.a);
      }
    `;

    // Dedicated Shader Program for 3D Textured Google Maps Ground Planes (Z15, Z17, Z19)
    const mapVsSource = `
      attribute vec3 aMapPos;
      attribute vec2 aMapUV;
      uniform mat4 uProj;
      uniform mat4 uView;
      varying vec2 vUV;
      varying vec3 vPos;
      void main() {
        vUV = aMapUV;
        vPos = aMapPos;
        gl_Position = uProj * uView * vec4(aMapPos, 1.0);
      }
    `;

    const mapFsSource = `
      precision highp float;
      varying vec2 vUV;
      varying vec3 vPos;
      uniform sampler2D uTex;
      uniform float uNightMix;
      uniform int uCutBasementHole;
      void main() {
        // Cut out exact basement footprint (-3.41..16.14, z = -36.11..3.60) so subterranean levels are never occluded
        if (uCutBasementHole == 1) {
          if (vPos.x > -3.41 && vPos.x < 16.14 && vPos.z > -36.11 && vPos.z < 3.60) {
            discard;
          }
        }
        vec4 texCol = texture2D(uTex, vUV);
        vec3 rgb = texCol.rgb * (1.0 - 0.52 * uNightMix);
        if (uNightMix > 0.01) {
          rgb *= vec3(0.82, 0.88, 1.10);
        }
        gl_FragColor = vec4(rgb, 1.0);
      }
    `;

    function compileShader(type, src) {
      const s = gl.createShader(type);
      gl.shaderSource(s, src);
      gl.compileShader(s);
      return s;
    }

    const prog = gl.createProgram();
    gl.attachShader(prog, compileShader(gl.VERTEX_SHADER, vsSource));
    gl.attachShader(prog, compileShader(gl.FRAGMENT_SHADER, fsSource));
    gl.linkProgram(prog);

    const mapProg = gl.createProgram();
    gl.attachShader(mapProg, compileShader(gl.VERTEX_SHADER, mapVsSource));
    gl.attachShader(mapProg, compileShader(gl.FRAGMENT_SHADER, mapFsSource));
    gl.linkProgram(mapProg);

    const aPos = gl.getAttribLocation(prog, 'aPos');
    const aNorm = gl.getAttribLocation(prog, 'aNorm');
    const aCol = gl.getAttribLocation(prog, 'aCol');
    const uProj = gl.getUniformLocation(prog, 'uProj');
    const uView = gl.getUniformLocation(prog, 'uView');
    const uClipBounds = gl.getUniformLocation(prog, 'uClipBounds');
    const uIsLine = gl.getUniformLocation(prog, 'uIsLine');
    const uSunDir = gl.getUniformLocation(prog, 'uSunDir');
    const uNightMix = gl.getUniformLocation(prog, 'uNightMix');

    const aMapPos = gl.getAttribLocation(mapProg, 'aMapPos');
    const aMapUV = gl.getAttribLocation(mapProg, 'aMapUV');
    const uMapProj = gl.getUniformLocation(mapProg, 'uProj');
    const uMapView = gl.getUniformLocation(mapProg, 'uView');
    const uMapTex = gl.getUniformLocation(mapProg, 'uTex');
    const uMapNightMix = gl.getUniformLocation(mapProg, 'uNightMix');
    const uCutBasementHole = gl.getUniformLocation(mapProg, 'uCutBasementHole');

    // Create & load the 3 Petah Tikva Google Maps textures (Z15, Z17, Z19)
    let gmapsGroundVisible = true;
    const mapPlanes = [];

    function createMapPlane(mapMeta, yHeight) {
      const span = mapMeta.world_span_m;
      const half = span * 0.5;
      const cx = 6.365, cz = -16.545;
      const x0 = cx - half, x1 = cx + half;
      const zNorth = cz - half, zSouth = cz + half;

      // 2 triangles covering [x0..x1] x [zNorth..zSouth], with North = v:0, South = v:1, West = u:0, East = u:1
      const verts = new Float32Array([
        x0, yHeight, zNorth,  0.0, 0.0,
        x1, yHeight, zNorth,  1.0, 0.0,
        x1, yHeight, zSouth,  1.0, 1.0,
        x0, yHeight, zNorth,  0.0, 0.0,
        x1, yHeight, zSouth,  1.0, 1.0,
        x0, yHeight, zSouth,  0.0, 1.0
      ]);
      const buf = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, buf);
      gl.bufferData(gl.ARRAY_BUFFER, verts, gl.STATIC_DRAW);

      const tex = gl.createTexture();
      gl.bindTexture(gl.TEXTURE_2D, tex);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array([30, 41, 59, 255]));

      const img = new Image();
      img.onload = () => {
        gl.bindTexture(gl.TEXTURE_2D, tex);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      };
      img.src = mapMeta.data_uri;

      return { buf, tex, yHeight, span };
    }

    function initGroundMapPlanes() {
      mapPlanes.push(createMapPlane(GMAPS_OUTER_Z15, -0.28));
      mapPlanes.push(createMapPlane(GMAPS_INNER_Z17, -0.18));
      mapPlanes.push(createMapPlane(GMAPS_CLOSE_Z19, -0.09));
    }

    function toggleGmapsGround() {
      gmapsGroundVisible = !gmapsGroundVisible;
      const btn = document.getElementById('btn-top-gmaps');
      if (btn) {
        btn.textContent = gmapsGroundVisible ? '🌍 מפת פ"ת: פעיל' : '🌍 מפת פ"ת: כבוי';
        btn.className = gmapsGroundVisible ? 'ui-btn active' : 'ui-btn';
      }
    }

    const opaqueBuf = gl.createBuffer();
    const transBuf = gl.createBuffer();
    const lineBuf = gl.createBuffer();
    const gisLineBuf = gl.createBuffer();
    const unitVolBuf = gl.createBuffer();
    let opaqueCount = 0, transCount = 0, lineCount = 0, gisLineCount = 0, unitVolCount = 0;

    let sunDirVec = [0.55, 0.85, -0.45];
    let isNightMode = false;
    let gisRadiiVisible = true;
    let gisPoisVisible = true;
    let units3DVisible = false;
    let showUnitPrices = true;
    let activeGisCategory = 'all';
    let activeUnitStatusFilter = 'all';
    let activeUnitRoomFilter = 'all';
    let selectedUnitObj = null;
    let selectedPoiObj = null;
    let activeParkingHighlight = null;
    let isMeasureMode = false;
    let measurePtA = null;
    const measureSegments = [];

    function pushLine(arr, p0, p1, col) {
      arr.push(p0[0], p0[1], p0[2], 0, 1, 0, col[0], col[1], col[2], col[3]);
      arr.push(p1[0], p1[1], p1[2], 0, 1, 0, col[0], col[1], col[2], col[3]);
    }

    function pushSolidBoxToArr(arr, x0, y0, n0, x1, y1, n1, col) {
      const minX = Math.min(x0, x1), maxX = Math.max(x0, x1);
      const minY = Math.min(y0, y1), maxY = Math.max(y0, y1);
      const minZ = -Math.max(n0, n1), maxZ = -Math.min(n0, n1);
      const v = [
        [minX, minY, minZ], [maxX, minY, minZ], [maxX, maxY, minZ], [minX, maxY, minZ],
        [minX, minY, maxZ], [maxX, minY, maxZ], [maxX, maxY, maxZ], [minX, maxY, maxZ]
      ];
      const faces = [
        { idx: [0, 2, 1, 0, 3, 2], n: [0, 0, -1] },
        { idx: [4, 5, 6, 4, 6, 7], n: [0, 0, 1] },
        { idx: [0, 4, 7, 0, 7, 3], n: [-1, 0, 0] },
        { idx: [1, 2, 6, 1, 6, 5], n: [1, 0, 0] },
        { idx: [3, 7, 6, 3, 6, 2], n: [0, 1, 0] },
        { idx: [0, 1, 5, 0, 5, 4], n: [0, -1, 0] }
      ];
      for (const f of faces) {
        for (const vi of f.idx) {
          const pt = v[vi];
          arr.push(pt[0], pt[1], pt[2], f.n[0], f.n[1], f.n[2], col[0], col[1], col[2], col[3]);
        }
      }
    }

    function rebuildBuffers() {
      const opaqueData = [];
      const transData = [];
      const lineData = [];

      if (layerState.SiteDatum) {
        pushLine(lineData, [0, 0.02, 0], [18, 0.02, 0], [0.95, 0.25, 0.25, 1.0]);
        pushLine(lineData, [0, 0.02, 0], [0, 33.5, 0], [0.25, 0.90, 0.35, 1.0]);
        pushLine(lineData, [0, 0.02, 0], [0, 0.02, -38], [0.25, 0.55, 0.98, 1.0]);
      }

      if (layerState.FloorPlanCAD) {
        for (const seg of cadPlanLines) {
          pushLine(lineData, seg.p0, seg.p1, seg.col);
        }
      }

      for (const m of meshes) {
        if (!layerState[m.layer]) continue;
        const mat = MATERIALS[m.matKey];
        const alpha = mat.alpha;
        const isTrans = alpha < 0.99;
        const target = isTrans ? transData : opaqueData;

        for (const f of m.faces) {
          for (const vi of f.idx) {
            const pt = m.v[vi];
            target.push(pt[0], pt[1], pt[2], f.n[0], f.n[1], f.n[2], mat.color[0], mat.color[1], mat.color[2], alpha);
          }
        }

        if (showEdges) {
          for (const [e0, e1] of m.edges) {
            pushLine(lineData, m.v[e0], m.v[e1], [0.10, 0.12, 0.16, 0.35]);
          }
        }
      }

      opaqueCount = opaqueData.length / 10;
      gl.bindBuffer(gl.ARRAY_BUFFER, opaqueBuf);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(opaqueData), gl.STATIC_DRAW);

      transCount = transData.length / 10;
      gl.bindBuffer(gl.ARRAY_BUFFER, transBuf);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(transData), gl.STATIC_DRAW);

      lineCount = lineData.length / 10;
      gl.bindBuffer(gl.ARRAY_BUFFER, lineBuf);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(lineData), gl.STATIC_DRAW);

      rebuildScopeOverlayBuffers();
    }

    function rebuildScopeOverlayBuffers() {
      const gisLines = [];
      const volTris = [];
      const cx = 6.36, cz = -16.5;

      // 1. 8 Concentric Distance Rings around KKL 10 (150m to 2000m)
      if (gisRadiiVisible) {
        const radii = [150, 250, 350, 500, 750, 1000, 1500, 2000];
        const segs = 72;
        for (const r of radii) {
          const col = (r <= 500) ? [0.16, 0.92, 0.62, 0.85] : [0.35, 0.72, 1.00, 0.75];
          for (let i = 0; i < segs; i++) {
            const a0 = (i / segs) * Math.PI * 2;
            const a1 = ((i + 1) / segs) * Math.PI * 2;
            pushLine(
              gisLines,
              [cx + Math.cos(a0) * r, 0.35, cz + Math.sin(a0) * r],
              [cx + Math.cos(a1) * r, 0.35, cz + Math.sin(a1) * r],
              col
            );
          }
        }
      }

      // 2. 46 POI Vertical 3D Beacon Pins + Radial Line to Active POI
      if (gisPoisVisible) {
        for (const p of KKL10_POIS) {
          if (activeGisCategory !== 'all' && p.cat !== activeGisCategory) continue;
          const px = cx + p.east_m;
          const pz = -(16.5 + p.north_m);
          const isSel = (selectedPoiObj === p);
          const pinCol = isSel ? [1.0, 0.85, 0.15, 1.0] : [0.22, 0.75, 0.98, 0.90];
          pushLine(gisLines, [px, 0.0, pz], [px, isSel ? 28.0 : 14.0, pz], pinCol);
          if (isSel) {
            pushLine(gisLines, [cx, 2.0, cz], [px, 2.0, pz], [1.0, 0.82, 0.12, 0.98]);
          }
        }
      }

      // 3. 3D Laser Measurement Segments
      for (const m of measureSegments) {
        pushLine(gisLines, m.a, m.b, [0.15, 0.82, 0.98, 1.0]);
      }

      // 4. 3D Unit Volume Highlights (25 Units) & Active Unit Highlight
      for (const u of KKL10_UNITS) {
        const isSel = (selectedUnitObj && selectedUnitObj.num === u.num);
        if (!units3DVisible && !isSel) continue;
        const [x0, y0, n0, x1, y1, n1] = u.box;
        let col;
        if (isSel) {
          col = [0.98, 0.78, 0.12, 0.42];
        } else if (u.status === 'available') {
          col = [0.06, 0.72, 0.50, 0.24];
        } else if (u.status === 'reserved') {
          col = [0.96, 0.62, 0.05, 0.26];
        } else {
          col = [0.45, 0.52, 0.64, 0.18];
        }
        pushSolidBoxToArr(volTris, x0 - 0.12, y0 + 0.05, n0 - 0.12, x1 + 0.12, y1 - 0.05, n1 + 0.12, col);
        if (isSel) {
          const z0 = -n0, z1 = -n1;
          const bCol = [1.0, 0.84, 0.10, 1.0];
          pushLine(gisLines, [x0, y1, z0], [x1, y1, z0], bCol);
          pushLine(gisLines, [x1, y1, z0], [x1, y1, z1], bCol);
          pushLine(gisLines, [x1, y1, z1], [x0, y1, z1], bCol);
          pushLine(gisLines, [x0, y1, z1], [x0, y1, z0], bCol);
        }
      }

      // 5. Basement Parking Stall 3D Highlight
      if (activeParkingHighlight) {
        const p = activeParkingHighlight;
        pushSolidBoxToArr(volTris, p.x0, p.y0, p.n0, p.x1, p.y1, p.n1, [0.06, 0.85, 0.58, 0.50]);
      }

      gisLineCount = gisLines.length / 10;
      gl.bindBuffer(gl.ARRAY_BUFFER, gisLineBuf);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(gisLines), gl.STATIC_DRAW);

      unitVolCount = volTris.length / 10;
      gl.bindBuffer(gl.ARRAY_BUFFER, unitVolBuf);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(volTris), gl.STATIC_DRAW);
    }

    // Camera & Walkthrough State (Starts showing the 3D KKL 10 building aligned with KKL Street & Lot, North UP)
    let cam = {
      yaw: -0.22,
      pitch: 0.56,
      dist: 115.0,
      target: [6.365, 9.0, -16.545],
      walkMode: false,
      eyePos: [6.365, 12.0, 1.5]
    };
    let activePlanFloorIdx = 1;

    function toggleOrtho() {
      isOrtho = !isOrtho;
      document.getElementById('orthoBtn').textContent = `📐 היטל: ${isOrtho ? 'אורתוגרפי 1:50' : 'פרספקטיבה'}`;
    }

    function viewFloorPlan(floorIdx) {
      exitWalkMode();
      const fl = FLOOR_LEVELS.find(f => f.idx === floorIdx);
      if (!fl) return;
      activePlanFloorIdx = floorIdx;
      const cutTop = fl.y + 1.95;
      document.getElementById('clipY').value = cutTop;
      document.getElementById('clipX').value = 17.0;
      document.getElementById('clipZ').value = 38.0;
      updateClipping(fl);

      cam.yaw = 0.0;
      cam.pitch = 1.34;
      cam.dist = 31.0;
      cam.target = [6.365, fl.y + 0.5, -16.545];
    }

    function setCameraPreset(preset) {
      exitWalkMode();
      closeAllDrawers();
      document.getElementById('isolateFloorCb').checked = false;
      resetClipping();
      if (preset === 'north_persp') {
        isOrtho = false;
        document.getElementById('orthoBtn').textContent = '📐 היטל: פרספקטיבה';
        cam.yaw = 2.75; cam.pitch = 0.34; cam.dist = 68; cam.target = [6.365, 11.0, -16.545];
      } else if (preset === 'south_persp') {
        isOrtho = false;
        document.getElementById('orthoBtn').textContent = '📐 היטל: פרספקטיבה';
        cam.yaw = 0.35; cam.pitch = 0.34; cam.dist = 68; cam.target = [6.365, 11.0, -16.545];
      } else if (preset === 'east_ortho') {
        isOrtho = true;
        document.getElementById('orthoBtn').textContent = '📐 היטל: אורתוגרפי 1:50';
        cam.yaw = Math.PI * 0.5; cam.pitch = 0.0; cam.dist = 48; cam.target = [6.365, 11.5, -16.545];
      } else if (preset === 'gis_aerial') {
        isOrtho = false;
        cam.yaw = 0.0; cam.pitch = 0.82; cam.dist = 380; cam.target = [6.365, 0.0, -16.545];
      } else if (preset === 'gis_regional') {
        isOrtho = false;
        cam.yaw = 0.0; cam.pitch = 0.88; cam.dist = 1250; cam.target = [6.365, 0.0, -16.545];
      }
    }

    function simulateBalconyView(floorNum, dir = 'N') {
      const fl = FLOOR_LEVELS.find(f => f.idx === floorNum) || FLOOR_LEVELS[5];
      document.getElementById('isolateFloorCb').checked = false;
      resetClipping();
      isOrtho = false;
      cam.walkMode = true;
      if (dir === 'N') {
        cam.eyePos = [9.2, fl.y + 1.68, -34.2];
        cam.yaw = 0.0;
        cam.pitch = -0.05;
      } else {
        cam.eyePos = [6.36, fl.y + 1.68, 1.2];
        cam.yaw = Math.PI;
        cam.pitch = -0.05;
      }
      document.getElementById('walk-hud').style.display = 'block';
      document.getElementById('walk-hud-badge').textContent = `${fl.heb} (+${fl.y.toFixed(2)} מ')`;
      document.getElementById('walk-hud-title').textContent = `🔭 נוף מהמרפסת ה${dir === 'N' ? 'צפונית (רחוב קק"ל)' : 'דרומית'} — קומה ${floorNum}`;
    }

    function exitWalkMode() {
      if (!cam.walkMode) return;
      cam.walkMode = false;
      document.getElementById('walk-hud').style.display = 'none';
    }

    // Mouse / Pointer Orbit, Pan (Up/Down/Left/Right), Keyboard Arrows/WASD, D-Pad & Touch
    let primaryDragMode = 'orbit'; // 'orbit' or 'pan'
    let dragMode = null, downX = 0, downY = 0, lastX = 0, lastY = 0;
    let activeHoldNav = null; // { dir, sign }
    const keysHeld = {};

    function togglePrimaryDragMode() {
      primaryDragMode = (primaryDragMode === 'orbit') ? 'pan' : 'orbit';
      const btn = document.getElementById('btn-drag-mode');
      if (btn) {
        btn.textContent = (primaryDragMode === 'pan') ? '✋ גרירה: הזזה' : '🔄 גרירה: סיבוב';
        btn.className = (primaryDragMode === 'pan') ? 'ui-btn active' : 'ui-btn';
      }
      canvas.style.cursor = (primaryDragMode === 'pan') ? 'move' : 'grab';
    }

    // Screen-aligned 3D panning: moves along camera Right and camera Up vectors
    function panCameraScreen(dxPixels, dyPixels) {
      const panScale = (cam.walkMode ? 0.035 : cam.dist * 0.00145);
      const rightX = Math.cos(cam.yaw), rightY = 0.0, rightZ = -Math.sin(cam.yaw);
      const upX = -Math.sin(cam.pitch) * Math.sin(cam.yaw);
      const upY = Math.cos(cam.pitch);
      const upZ = -Math.sin(cam.pitch) * Math.cos(cam.yaw);

      const moveX = (-dxPixels * rightX + dyPixels * upX) * panScale;
      const moveY = (-dxPixels * rightY + dyPixels * upY) * panScale;
      const moveZ = (-dxPixels * rightZ + dyPixels * upZ) * panScale;

      if (cam.walkMode) {
        cam.eyePos[0] += moveX;
        cam.eyePos[1] = Math.max(-8.0, Math.min(35.0, cam.eyePos[1] + moveY));
        cam.eyePos[2] += moveZ;
      } else {
        cam.target[0] += moveX;
        cam.target[1] = Math.max(-8.5, Math.min(34.0, cam.target[1] + moveY));
        cam.target[2] += moveZ;
      }
    }

    function stepNavAction(dir, sign = 1, dtScale = 1.0) {
      const stepPx = 14.0 * dtScale;
      if (dir === 'left')  panCameraScreen( stepPx * sign, 0);
      if (dir === 'right') panCameraScreen(-stepPx * sign, 0);
      if (dir === 'up')    panCameraScreen(0,  stepPx * sign);
      if (dir === 'down')  panCameraScreen(0, -stepPx * sign);
      if (dir === 'elev') {
        const elevStep = (cam.walkMode ? 0.22 : Math.max(0.25, cam.dist * 0.012)) * sign * dtScale;
        if (cam.walkMode) cam.eyePos[1] = Math.max(-8.0, Math.min(35.0, cam.eyePos[1] + elevStep));
        else cam.target[1] = Math.max(-8.5, Math.min(34.0, cam.target[1] + elevStep));
      }
      if (dir === 'zoom' && !cam.walkMode) {
        cam.dist = Math.max(4.0, Math.min(2800.0, cam.dist * (1 + 0.025 * sign * dtScale)));
      }
    }

    function startHoldNav(dir, sign) {
      stepNavAction(dir, sign, 1.3);
      activeHoldNav = { dir, sign };
    }

    function stopHoldNav() {
      activeHoldNav = null;
    }

    function updateContinuousNavigation() {
      if (activeHoldNav) {
        stepNavAction(activeHoldNav.dir, activeHoldNav.sign, 0.85);
      }
      if (keysHeld['ArrowLeft']  || keysHeld['KeyA']) stepNavAction('left',  1, 0.85);
      if (keysHeld['ArrowRight'] || keysHeld['KeyD']) stepNavAction('right', 1, 0.85);
      if (keysHeld['ArrowUp']    || keysHeld['KeyW']) stepNavAction('up',    1, 0.85);
      if (keysHeld['ArrowDown']  || keysHeld['KeyS']) stepNavAction('down',  1, 0.85);
      if (keysHeld['PageUp']     || keysHeld['KeyE']) stepNavAction('elev',  1, 0.85);
      if (keysHeld['PageDown']   || keysHeld['KeyQ']) stepNavAction('elev', -1, 0.85);
      if (keysHeld['Equal']      || keysHeld['NumpadAdd'])      stepNavAction('zoom', -1, 0.85);
      if (keysHeld['Minus']      || keysHeld['NumpadSubtract']) stepNavAction('zoom',  1, 0.85);
    }

    window.addEventListener('keydown', e => {
      if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;
      keysHeld[e.code] = true;
      if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'PageUp', 'PageDown'].includes(e.code)) {
        e.preventDefault();
      }
    });
    window.addEventListener('keyup', e => {
      keysHeld[e.code] = false;
    });
    window.addEventListener('blur', () => {
      for (const k in keysHeld) keysHeld[k] = false;
      activeHoldNav = null;
    });

    canvas.addEventListener('mousedown', e => {
      closeAllDrawers();
      if (e.button === 1 || e.button === 2 || e.shiftKey || e.ctrlKey) {
        dragMode = 'pan';
      } else {
        dragMode = primaryDragMode;
      }
      downX = lastX = e.clientX;
      downY = lastY = e.clientY;
    });
    window.addEventListener('mouseup', e => {
      const moved = Math.hypot(e.clientX - downX, e.clientY - downY);
      if (moved < 5 && isMeasureMode && e.button === 0) {
        handleMeasureClick(e.clientX, e.clientY);
      }
      dragMode = null;
    });
    canvas.addEventListener('contextmenu', e => e.preventDefault());
    window.addEventListener('mousemove', e => {
      if (!dragMode) return;
      const dx = e.clientX - lastX, dy = e.clientY - lastY;
      lastX = e.clientX; lastY = e.clientY;
      if (cam.walkMode && dragMode === 'orbit') {
        cam.yaw -= dx * 0.005;
        cam.pitch = Math.max(-1.2, Math.min(1.2, cam.pitch - dy * 0.005));
        return;
      }
      if (dragMode === 'orbit') {
        cam.yaw -= dx * 0.007;
        cam.pitch = Math.max(0.04, Math.min(1.55, cam.pitch + dy * 0.007));
      } else {
        panCameraScreen(dx, dy);
      }
    });
    canvas.addEventListener('wheel', e => {
      e.preventDefault();
      if (cam.walkMode) return;
      cam.dist = Math.max(4.0, Math.min(2800.0, cam.dist * (1 + e.deltaY * 0.001)));
    }, { passive: false });

    // Touch gesture support (1-finger orbit/pan, 2-finger pan + pinch zoom)
    let touchLastX = 0, touchLastY = 0, touchLastDist = 0;
    canvas.addEventListener('touchstart', e => {
      if (e.touches.length === 1) {
        touchLastX = e.touches[0].clientX;
        touchLastY = e.touches[0].clientY;
      } else if (e.touches.length === 2) {
        touchLastX = (e.touches[0].clientX + e.touches[1].clientX) * 0.5;
        touchLastY = (e.touches[0].clientY + e.touches[1].clientY) * 0.5;
        touchLastDist = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
      }
    }, { passive: true });
    canvas.addEventListener('touchmove', e => {
      e.preventDefault();
      if (e.touches.length === 1) {
        const dx = e.touches[0].clientX - touchLastX;
        const dy = e.touches[0].clientY - touchLastY;
        touchLastX = e.touches[0].clientX;
        touchLastY = e.touches[0].clientY;
        if (primaryDragMode === 'pan') {
          panCameraScreen(dx, dy);
        } else {
          cam.yaw -= dx * 0.007;
          cam.pitch = Math.max(0.04, Math.min(1.55, cam.pitch + dy * 0.007));
        }
      } else if (e.touches.length === 2) {
        const cx = (e.touches[0].clientX + e.touches[1].clientX) * 0.5;
        const cy = (e.touches[0].clientY + e.touches[1].clientY) * 0.5;
        const dist = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
        panCameraScreen(cx - touchLastX, cy - touchLastY);
        if (touchLastDist > 10 && dist > 10 && !cam.walkMode) {
          cam.dist = Math.max(4.0, Math.min(2800.0, cam.dist * (touchLastDist / dist)));
        }
        touchLastX = cx; touchLastY = cy; touchLastDist = dist;
      }
    }, { passive: false });

    function perspectiveMat(fov, aspect, near, far) {
      const f = 1.0 / Math.tan(fov * 0.5), nf = 1.0 / (near - far);
      return new Float32Array([
        f / aspect, 0, 0, 0,
        0, f, 0, 0,
        0, 0, (far + near) * nf, -1,
        0, 0, (2 * far * near) * nf, 0
      ]);
    }

    function orthoMat(halfH, aspect, near, far) {
      const r = halfH * aspect, t = halfH, nf = 1.0 / (near - far);
      return new Float32Array([
        1 / r, 0, 0, 0,
        0, 1 / t, 0, 0,
        0, 0, 2 * nf, 0,
        0, 0, (far + near) * nf, 1
      ]);
    }

    function lookAtMat(eye, center, up) {
      let zx = eye[0] - center[0], zy = eye[1] - center[1], zz = eye[2] - center[2];
      let len = Math.hypot(zx, zy, zz) || 1; zx /= len; zy /= len; zz /= len;
      let xx = up[1] * zz - up[2] * zy, xy = up[2] * zx - up[0] * zz, xz = up[0] * zy - up[1] * zx;
      len = Math.hypot(xx, xy, xz) || 1; xx /= len; xy /= len; xz /= len;
      let yx = zy * xz - zz * xy, yy = zz * xx - zx * xz, yz = zx * xy - zy * xx;
      return new Float32Array([
        xx, yx, zx, 0,
        xy, yy, zy, 0,
        xz, yz, zz, 0,
        -(xx * eye[0] + xy * eye[1] + xz * eye[2]),
        -(yx * eye[0] + yy * eye[1] + yz * eye[2]),
        -(zx * eye[0] + zy * eye[1] + zz * eye[2]),
        1
      ]);
    }

    function projectWorldToScreen(wx, wy, wz, P, V, cssW, cssH) {
      const vx = V[0]*wx + V[4]*wy + V[8]*wz + V[12];
      const vy = V[1]*wx + V[5]*wy + V[9]*wz + V[13];
      const vz = V[2]*wx + V[6]*wy + V[10]*wz + V[14];
      const vw = V[3]*wx + V[7]*wy + V[11]*wz + V[15];
      const cx = P[0]*vx + P[4]*vy + P[8]*vz + P[12]*vw;
      const cy = P[1]*vx + P[5]*vy + P[9]*vz + P[13]*vw;
      const cz = P[2]*vx + P[6]*vy + P[10]*vz + P[14]*vw;
      const cw = P[3]*vx + P[7]*vy + P[11]*vz + P[15]*vw;
      if (cw <= 0.05) return null;
      const nx = cx / cw, ny = cy / cw, nz = cz / cw;
      if (nz < -1.0 || nz > 1.0) return null;
      return {
        x: (nx * 0.5 + 0.5) * cssW,
        y: (-ny * 0.5 + 0.5) * cssH
      };
    }

    function bindAttribs(buf) {
      gl.bindBuffer(gl.ARRAY_BUFFER, buf);
      const stride = 10 * 4;
      gl.enableVertexAttribArray(aPos);
      gl.vertexAttribPointer(aPos, 3, gl.FLOAT, false, stride, 0);
      gl.enableVertexAttribArray(aNorm);
      gl.vertexAttribPointer(aNorm, 3, gl.FLOAT, false, stride, 3 * 4);
      gl.enableVertexAttribArray(aCol);
      gl.vertexAttribPointer(aCol, 4, gl.FLOAT, false, stride, 6 * 4);
    }

    function drawGroundMapsPass(projMatrix, viewMatrix) {
      if (!gmapsGroundVisible || mapPlanes.length === 0) return;
      gl.useProgram(mapProg);
      gl.uniformMatrix4fv(uMapProj, false, projMatrix);
      gl.uniformMatrix4fv(uMapView, false, viewMatrix);
      gl.uniform1f(uMapNightMix, isNightMode ? 1.0 : 0.0);
      gl.uniform1i(uCutBasementHole, 1);

      gl.disable(gl.BLEND);
      gl.depthMask(true);
      gl.disableVertexAttribArray(aNorm);
      gl.disableVertexAttribArray(aCol);

      const stride = 5 * 4;
      for (const mp of mapPlanes) {
        gl.bindBuffer(gl.ARRAY_BUFFER, mp.buf);
        gl.enableVertexAttribArray(aMapPos);
        gl.vertexAttribPointer(aMapPos, 3, gl.FLOAT, false, stride, 0);
        gl.enableVertexAttribArray(aMapUV);
        gl.vertexAttribPointer(aMapUV, 2, gl.FLOAT, false, stride, 3 * 4);

        gl.activeTexture(gl.TEXTURE0);
        gl.bindTexture(gl.TEXTURE_2D, mp.tex);
        gl.uniform1i(uMapTex, 0);

        gl.drawArrays(gl.TRIANGLES, 0, 6);
      }

      gl.disableVertexAttribArray(aMapPos);
      gl.disableVertexAttribArray(aMapUV);
      gl.useProgram(prog);
    }

    let currentProjMat = null;
    let currentViewMat = null;
    let currentEyePos = [0, 20, 20];

    function renderLoop() {
      updateContinuousNavigation();
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const cssW = canvas.clientWidth, cssH = canvas.clientHeight;
      const w = cssW * dpr, h = cssH * dpr;
      if (canvas.width !== w || canvas.height !== h) {
        canvas.width = w; canvas.height = h;
      }
      gl.viewport(0, 0, w, h);

      if (isNightMode) gl.clearColor(0.03, 0.05, 0.11, 1.0);
      else gl.clearColor(0.84, 0.90, 0.96, 1.0);

      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      gl.enable(gl.DEPTH_TEST);

      let eye, center;
      if (cam.walkMode) {
        eye = cam.eyePos;
        center = [
          eye[0] + Math.cos(cam.pitch) * Math.sin(cam.yaw),
          eye[1] + Math.sin(cam.pitch),
          eye[2] - Math.cos(cam.pitch) * Math.cos(cam.yaw)
        ];
      } else {
        eye = [
          cam.target[0] + cam.dist * Math.cos(cam.pitch) * Math.sin(cam.yaw),
          cam.target[1] + cam.dist * Math.sin(cam.pitch),
          cam.target[2] + cam.dist * Math.cos(cam.pitch) * Math.cos(cam.yaw)
        ];
        center = cam.target;
      }
      currentEyePos = eye;

      const projMatrix = (isOrtho && !cam.walkMode)
        ? orthoMat(cam.dist * 0.48, w / h, -500.0, 4500.0)
        : perspectiveMat((cam.walkMode ? 58 : 42) * Math.PI / 180, w / h, 0.5, 6500.0);
      const viewMatrix = lookAtMat(eye, center, [0, 1, 0]);
      currentProjMat = projMatrix;
      currentViewMat = viewMatrix;

      // 0. Draw Triple-Resolution Petah Tikva Google Maps Ground Planes (Z15, Z17, Z19)
      drawGroundMapsPass(projMatrix, viewMatrix);

      gl.useProgram(prog);
      gl.uniformMatrix4fv(uProj, false, projMatrix);
      gl.uniformMatrix4fv(uView, false, viewMatrix);
      gl.uniform4f(uClipBounds, clipBounds.x, clipBounds.yMin, clipBounds.yMax, clipBounds.n);
      gl.uniform3f(uSunDir, sunDirVec[0], sunDirVec[1], sunDirVec[2]);
      gl.uniform1f(uNightMix, isNightMode ? 1.0 : 0.0);

      // 1. Opaque BIM Geometry
      gl.disable(gl.BLEND);
      gl.depthMask(true);
      gl.uniform1i(uIsLine, 0);
      if (opaqueCount > 0) {
        bindAttribs(opaqueBuf);
        gl.drawArrays(gl.TRIANGLES, 0, opaqueCount);
      }

      // 2. Clipped CAD Floor Plan Lines & Wireframe Edges
      if (lineCount > 0) {
        gl.enable(gl.BLEND);
        gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
        gl.uniform1i(uIsLine, 1);
        bindAttribs(lineBuf);
        gl.drawArrays(gl.LINES, 0, lineCount);
      }

      // 3. Unclipped GIS Rings, POI Stems & Measurement Lines
      if (gisLineCount > 0) {
        gl.enable(gl.BLEND);
        gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
        gl.uniform1i(uIsLine, 2);
        bindAttribs(gisLineBuf);
        gl.drawArrays(gl.LINES, 0, gisLineCount);
      }

      // 4. Translucent BIM Glazing
      if (transCount > 0) {
        gl.enable(gl.BLEND);
        gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
        gl.depthMask(false);
        gl.uniform1i(uIsLine, 0);
        bindAttribs(transBuf);
        gl.drawArrays(gl.TRIANGLES, 0, transCount);
        gl.depthMask(true);
      }

      // 5. Translucent 3D Unit Highlight Volumes & Parking Highlight
      if (unitVolCount > 0) {
        gl.enable(gl.BLEND);
        gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
        gl.depthMask(false);
        gl.uniform1i(uIsLine, 3);
        bindAttribs(unitVolBuf);
        gl.drawArrays(gl.TRIANGLES, 0, unitVolCount);
        gl.depthMask(true);
      }

      updateDOMOverlays(projMatrix, viewMatrix, cssW, cssH);
      requestAnimationFrame(renderLoop);
    }

    // ============================================================================
    // DOM 3D OVERLAYS: GIS RINGS, 46 POIS, 25 UNIT BADGES & LASER MEASUREMENTS
    // ============================================================================
    const gisRingDomObjs = [];
    const gisPoiDomObjs = [];
    const unitBadgeDomObjs = [];
    const measureDomObjs = [];

    function initDOMOverlays() {
      const ringsContainer = document.getElementById('gis-rings-overlay');
      const poisContainer = document.getElementById('gis-pois-overlay');
      const unitsContainer = document.getElementById('units-3d-overlay');

      // 1. 8 Distance Ring Badges
      const radii = [150, 250, 350, 500, 750, 1000, 1500, 2000];
      for (const r of radii) {
        const el = document.createElement('div');
        const walkMin = Math.max(2, Math.round(r / 75));
        el.style.cssText = 'position:absolute;transform:translate(-50%,-50%);background:rgba(15,23,42,0.88);color:#38bdf8;border:1px solid rgba(56,189,248,0.45);padding:2px 7px;border-radius:999px;font-size:10px;font-weight:800;white-space:nowrap;';
        el.textContent = `⭕ ${r} מ' (~${walkMin} דק' הליכה)`;
        ringsContainer.appendChild(el);
        gisRingDomObjs.push({ el, pos: [6.36, 0.5, -(16.5 + r)] });
      }

      // 2. 46 POI Interactive Badges
      KKL10_POIS.forEach((p, idx) => {
        const el = document.createElement('div');
        el.style.cssText = `position:absolute;transform:translate(-50%,-100%);pointer-events:auto;cursor:pointer;display:flex;align-items:center;gap:4px;background:rgba(15,23,42,0.92);color:#ffffff;border:1.5px solid ${p.color};padding:2px 7px;border-radius:999px;font-size:10.5px;font-weight:700;white-space:nowrap;box-shadow:0 4px 10px rgba(0,0,0,0.45);`;
        el.innerHTML = `<span style="width:7px;height:7px;border-radius:999px;background:${p.color};"></span><span>${p.name}</span><span style="color:#94a3b8;font-size:9.5px;">${p.dist}מ'</span>`;
        el.onclick = (e) => { e.stopPropagation(); selectGisPoi(idx, true); };
        poisContainer.appendChild(el);
        gisPoiDomObjs.push({ el, poi: p, pos: [6.36 + p.east_m, 14.5, -(16.5 + p.north_m)] });
      });

      // 3. 25 Apartment Interactive 3D Badges
      KKL10_UNITS.forEach(u => {
        const el = document.createElement('div');
        const [x0, y0, n0, x1, y1, n1] = u.box;
        const bg = u.status === 'available' ? '#059669' : (u.status === 'reserved' ? '#d97706' : '#475569');
        el.style.cssText = `position:absolute;transform:translate(-50%,-50%);pointer-events:auto;cursor:pointer;display:none;align-items:center;gap:4px;background:${bg};color:#ffffff;border:1.5px solid #ffffff;padding:2px 8px;border-radius:999px;font-size:10.5px;font-weight:800;white-space:nowrap;box-shadow:0 4px 12px rgba(0,0,0,0.5);`;
        el.onclick = (e) => { e.stopPropagation(); selectUnitAndOpenCard(u.num, true); };
        unitsContainer.appendChild(el);
        unitBadgeDomObjs.push({
          el,
          unit: u,
          pos: [(x0 + x1) * 0.5, (y0 + y1) * 0.5, -(n0 + n1) * 0.5]
        });
      });
      refreshUnitBadgesText();
    }

    function refreshUnitBadgesText() {
      for (const ub of unitBadgeDomObjs) {
        const u = ub.unit;
        const priceTxt = (showUnitPrices && u.status === 'available') ? ` · ₪${(u.price / 1000000).toFixed(2)}M` : '';
        ub.el.innerHTML = `<span>דירה ${u.num} (ק'${u.floor})</span><span style="opacity:0.9;">${u.rooms}חד'${priceTxt}</span>`;
      }
    }

    function updateDOMOverlays(P, V, cssW, cssH) {
      // 1. GIS Ring Badges
      for (const r of gisRingDomObjs) {
        if (!gisRadiiVisible || cam.dist < 65) { r.el.style.display = 'none'; continue; }
        const sc = projectWorldToScreen(r.pos[0], r.pos[1], r.pos[2], P, V, cssW, cssH);
        if (!sc || sc.x < 20 || sc.x > cssW - 20 || sc.y < 60 || sc.y > cssH - 40) { r.el.style.display = 'none'; continue; }
        r.el.style.display = 'block';
        r.el.style.left = sc.x + 'px';
        r.el.style.top = sc.y + 'px';
      }

      // 2. 46 POI Badges
      for (const item of gisPoiDomObjs) {
        const catOk = (activeGisCategory === 'all' || item.poi.cat === activeGisCategory);
        if (!gisPoisVisible || !catOk || cam.dist < 65) { item.el.style.display = 'none'; continue; }
        const sc = projectWorldToScreen(item.pos[0], item.pos[1], item.pos[2], P, V, cssW, cssH);
        if (!sc || sc.x < 20 || sc.x > cssW - 20 || sc.y < 60 || sc.y > cssH - 40) { item.el.style.display = 'none'; continue; }
        item.el.style.display = 'inline-flex';
        item.el.style.left = sc.x + 'px';
        item.el.style.top = sc.y + 'px';
      }

      // 3. 25 Unit Badges
      for (const ub of unitBadgeDomObjs) {
        const isSel = (selectedUnitObj && selectedUnitObj.num === ub.unit.num);
        if ((!units3DVisible && !isSel) || ub.pos[1] > clipBounds.yMax) { ub.el.style.display = 'none'; continue; }
        const sc = projectWorldToScreen(ub.pos[0], ub.pos[1], ub.pos[2], P, V, cssW, cssH);
        if (!sc || sc.x < 20 || sc.x > cssW - 20 || sc.y < 60 || sc.y > cssH - 40) { ub.el.style.display = 'none'; continue; }
        ub.el.style.display = 'inline-flex';
        ub.el.style.left = sc.x + 'px';
        ub.el.style.top = sc.y + 'px';
        ub.el.style.transform = isSel ? 'translate(-50%,-50%) scale(1.12)' : 'translate(-50%,-50%)';
        ub.el.style.borderColor = isSel ? '#fde047' : '#ffffff';
      }

      // 4. Measurement Badges
      for (const mb of measureDomObjs) {
        const sc = projectWorldToScreen(mb.pos[0], mb.pos[1], mb.pos[2], P, V, cssW, cssH);
        if (!sc) { mb.el.style.display = 'none'; continue; }
        mb.el.style.display = 'block';
        mb.el.style.left = sc.x + 'px';
        mb.el.style.top = sc.y + 'px';
      }
    }

    // ============================================================================
    // CRM CATALOG, MULTI-FILTERS, FLOATING UNIT SALES CARD & PDF QUOTE GENERATOR
    // ============================================================================
    function formatILS(n) {
      return '₪' + Number(n).toLocaleString('he-IL');
    }

    function setUnitStatusFilter(status, btn) {
      activeUnitStatusFilter = status;
      document.querySelectorAll('#unit-status-filters .ui-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      renderUnitsCatalogList();
    }

    function setUnitRoomFilter(rm, btn) {
      activeUnitRoomFilter = rm;
      document.querySelectorAll('#unit-room-filters .ui-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      renderUnitsCatalogList();
    }

    function togglePriceVisibility() {
      showUnitPrices = !showUnitPrices;
      const btn = document.getElementById('btn-toggle-prices');
      btn.textContent = showUnitPrices ? '👁️ מחירים: מוצג' : '🙈 מחירים: מוסתר';
      btn.className = showUnitPrices ? 'ui-btn active' : 'ui-btn';
      refreshUnitBadgesText();
      renderUnitsCatalogList();
      if (selectedUnitObj && document.getElementById('unit-sales-card').style.display === 'block') {
        selectUnitAndOpenCard(selectedUnitObj.num, false);
      }
    }

    function toggleUnits3D() {
      units3DVisible = !units3DVisible;
      const topBtn = document.getElementById('btn-top-units3d');
      const drwBtn = document.getElementById('btn-drawer-units3d');
      if (topBtn) {
        topBtn.style.background = units3DVisible ? '#059669' : 'rgba(16,185,129,0.15)';
        topBtn.style.color = units3DVisible ? '#ffffff' : '#6ee7b7';
      }
      if (drwBtn) {
        drwBtn.textContent = units3DVisible ? '🏢 סימון דירות 3D: פעיל' : '🏢 הדגש דירות 3D על הבניין';
      }
      if (units3DVisible && cam.dist > 120) setCameraPreset('north_persp');
      rebuildScopeOverlayBuffers();
    }

    function renderUnitsCatalogList() {
      const container = document.getElementById('units-catalog-list');
      if (!container) return;
      const filtered = KKL10_UNITS.filter(u => {
        if (activeUnitStatusFilter === 'available' && u.status !== 'available') return false;
        if (activeUnitStatusFilter === 'owner' && u.status === 'available') return false;
        if (activeUnitRoomFilter === 'garden' && u.floor !== 0) return false;
        if (activeUnitRoomFilter === 'ph' && u.floor !== 8) return false;
        if (activeUnitRoomFilter === '4' && (u.rooms !== 4 || u.floor === 0)) return false;
        if (activeUnitRoomFilter === '5' && (u.rooms !== 5 || u.floor === 8)) return false;
        return true;
      });

      container.innerHTML = filtered.map(u => {
        const isSel = (selectedUnitObj && selectedUnitObj.num === u.num);
        const badgeBg = u.status === 'available' ? 'rgba(16,185,129,0.2)' : (u.status === 'reserved' ? 'rgba(245,158,11,0.2)' : 'rgba(148,163,184,0.15)');
        const badgeCol = u.status === 'available' ? '#34d399' : (u.status === 'reserved' ? '#fbbf24' : '#cbd5e1');
        const statusLbl = u.status === 'available' ? '🟢 פנויה (קולסקי)' : (u.status === 'reserved' ? '🟡 שמורה (מכר דניאל)' : '🔒 ' + u.owner);
        const priceStr = (showUnitPrices && u.status === 'available') ? formatILS(u.price) : (u.status === 'available' ? 'פנה למשרד המכירות' : u.owner);
        return `
          <div onclick="selectUnitAndOpenCard(${u.num}, true)" style="display:flex;align-items:center;justify-content:space-between;padding:8px 10px;border-radius:10px;background:${isSel ? 'rgba(37,99,235,0.28)' : 'rgba(30,41,59,0.75)'};border:1px solid ${isSel ? '#60a5fa' : 'rgba(148,163,184,0.22)'};cursor:pointer;transition:0.15s;">
            <div>
              <div style="display:flex;align-items:center;gap:6px;">
                <span style="font-weight:900;font-size:12.5px;color:#ffffff;">דירה ${u.num} · קומה ${u.floor === 0 ? 'קרקע' : u.floor}</span>
                <span style="background:${badgeBg};color:${badgeCol};padding:1px 7px;border-radius:999px;font-size:10px;font-weight:800;">${statusLbl}</span>
              </div>
              <div style="font-size:11px;color:#94a3b8;margin-top:2px;">
                ${u.type} · ${u.rooms} חד' · ${u.area} מ"ר + ${u.balconyLabel} · ${u.wing}
              </div>
            </div>
            <div style="text-align:left;">
              <div style="font-size:12.5px;font-weight:900;color:${u.status === 'available' ? '#34d399' : '#94a3b8'};">${priceStr}</div>
              <div style="font-size:9.5px;color:#64748b;">לחץ לכרטיס ו-PDF ❯</div>
            </div>
          </div>
        `;
      }).join('');
    }

    function selectUnitAndOpenCard(unitNum, flyToUnit = true) {
      const u = KKL10_UNITS.find(x => x.num === unitNum);
      if (!u) return;
      selectedUnitObj = u;
      activeParkingHighlight = null;
      rebuildScopeOverlayBuffers();
      renderUnitsCatalogList();

      if (flyToUnit) {
        const [x0, y0, n0, x1, y1, n1] = u.box;
        cam.target = [(x0 + x1) * 0.5, (y0 + y1) * 0.5, -(n0 + n1) * 0.5];
        if (cam.dist > 65) cam.dist = 38.0;
      }

      const down20 = Math.round(u.price * 0.20);
      const bal80 = u.price - down20;
      const monthlyMortgage = Math.round((u.price * 0.55) * 0.0053);
      const statusBadge = u.status === 'available'
        ? '<span style="background:#065f46;color:#6ee7b7;border:1px solid #10b981;padding:2px 8px;border-radius:999px;font-size:10.5px;font-weight:800;">🟢 פנויה לשיווק — מלאי קולסקי</span>'
        : `<span style="background:#334155;color:#cbd5e1;border:1px solid #64748b;padding:2px 8px;border-radius:999px;font-size:10.5px;font-weight:800;">🔒 ${u.owner}</span>`;

      const card = document.getElementById('unit-sales-card');
      card.style.display = 'block';
      card.innerHTML = `
        <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:8px;border-bottom:1px solid #334155;padding-bottom:8px;margin-bottom:10px;">
          <div>
            <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
              <span style="font-size:16px;font-weight:900;color:#ffffff;">דירה מס' ${u.num} (${u.type})</span>
              ${statusBadge}
            </div>
            <div style="font-size:11.5px;color:#94a3b8;margin-top:2px;">פרויקט קק"ל 10, פתח תקווה · קומה ${u.floor === 0 ? 'קרקע (0)' : u.floor} · ${u.wing}</div>
          </div>
          <button onclick="closeUnitCard()" class="ui-btn" style="padding:2px 7px;font-weight:800;">✕</button>
        </div>

        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;text-align:center;margin-bottom:10px;">
          <div style="background:#1e293b;border:1px solid #334155;border-radius:8px;padding:6px;">
            <div style="font-size:10px;color:#94a3b8;">חדרים</div>
            <div style="font-size:14px;font-weight:900;color:#ffffff;">${u.rooms}</div>
          </div>
          <div style="background:#1e293b;border:1px solid #334155;border-radius:8px;padding:6px;">
            <div style="font-size:10px;color:#94a3b8;">שטח פנים</div>
            <div style="font-size:14px;font-weight:900;color:#ffffff;">${u.area} מ"ר</div>
          </div>
          <div style="background:#1e293b;border:1px solid #334155;border-radius:8px;padding:6px;">
            <div style="font-size:10px;color:#94a3b8;">${u.floor === 0 ? 'גינה צמודה' : 'מרפסת שמש'}</div>
            <div style="font-size:14px;font-weight:900;color:#38bdf8;">+${u.balcony} מ"ר</div>
          </div>
          <div style="background:#1e293b;border:1px solid #334155;border-radius:8px;padding:6px;">
            <div style="font-size:10px;color:#94a3b8;">מפלס קומה</div>
            <div style="font-size:13px;font-weight:900;color:#fbbf24;direction:ltr;">+${u.box[1].toFixed(2)}m</div>
          </div>
        </div>

        <div style="background:#1e293b;border:1px solid #334155;border-radius:10px;padding:9px;margin-bottom:10px;font-size:11.5px;">
          <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
            <span style="color:#94a3b8;">כיווני אוויר ושמש:</span>
            <span style="font-weight:800;color:#ffffff;">${u.dir}</span>
          </div>
          <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
            <span style="color:#94a3b8;">חניה תת-קרקעית בטאבו:</span>
            <span style="font-weight:800;color:#6ee7b7;">${u.parking}</span>
          </div>
          <div style="display:flex;justify-content:space-between;border-top:1px solid #334155;padding-top:6px;margin-top:6px;">
            <span style="color:#fde047;font-weight:800;">מחיר שיווק רשמי:</span>
            <span style="font-size:15px;font-weight:900;color:#34d399;">${showUnitPrices ? formatILS(u.price) : 'פנה למשרד המכירות'}</span>
          </div>
          ${showUnitPrices ? `
          <div style="margin-top:6px;padding-top:6px;border-top:1px dashed #334155;color:#cbd5e1;font-size:10.5px;">
            <div>💳 <b>מסלול יזם 20/80:</b> בחתימה ${formatILS(down20)} (20%) · באכלוס ${formatILS(bal80)} (80%)</div>
            <div style="margin-top:2px;">🏦 אומדן החזר משכנתא חודשי (55% מימון): ~${formatILS(monthlyMortgage)} / חודש</div>
          </div>` : ''}
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;">
          <button onclick="viewFloorPlan(${u.floor});closeAllDrawers();" class="ui-btn" style="background:#b45309;color:#fff;border-color:#fbbf24;font-weight:800;">
            📐 תוכנית וחתך דירה 1:50
          </button>
          <button onclick="simulateBalconyView(${Math.max(1, u.floor)}, '${u.dir.includes('צפון') ? 'N' : 'S'}');closeAllDrawers();" class="ui-btn" style="background:#0284c7;color:#fff;border-color:#38bdf8;font-weight:800;">
            🔭 נוף מהמרפסת
          </button>
          <button onclick="showUnitParkingIn3D(${u.num})" class="ui-btn" style="background:#1e293b;color:#6ee7b7;border-color:#10b981;font-weight:800;">
            🚗 הצג חניה במרתף
          </button>
          <button onclick="printUnitOfferPDF(${u.num})" class="ui-btn" style="background:#059669;color:#fff;border-color:#34d399;font-weight:800;">
            📄 הצעת מחיר PDF
          </button>
        </div>
      `;
    }

    function closeUnitCard() {
      document.getElementById('unit-sales-card').style.display = 'none';
      selectedUnitObj = null;
      activeParkingHighlight = null;
      rebuildScopeOverlayBuffers();
      renderUnitsCatalogList();
    }

    function showUnitParkingIn3D(unitNum) {
      const u = KKL10_UNITS.find(x => x.num === unitNum);
      if (!u) return;
      closeAllDrawers();
      const isB1 = u.parkIdx <= 16;
      const bFloorIdx = isB1 ? -1 : -2;
      const bElev = isB1 ? -4.35 : -7.65;
      const localIdx = isB1 ? (u.parkIdx - 1) : (u.parkIdx - 17);
      const rowNorth = (localIdx % 2 === 1);
      const colSlot = Math.floor(localIdx / 2) % 7;
      const px0 = -2.5 + colSlot * 2.55;
      const pn0 = rowNorth ? 30.80 : -3.10;
      const pn1 = rowNorth ? 35.60 : 1.80;

      activeParkingHighlight = { x0: px0, y0: bElev + 0.05, n0: pn0, x1: px0 + 2.40, y1: bElev + 1.80, n1: pn1 };
      viewFloorPlan(bFloorIdx);
      cam.target = [px0 + 1.2, bElev + 0.5, -(pn0 + pn1) * 0.5];
      cam.dist = 24.0;
      cam.pitch = 1.15;
      rebuildScopeOverlayBuffers();
    }

    function printUnitOfferPDF(unitNum) {
      const u = KKL10_UNITS.find(x => x.num === unitNum) || selectedUnitObj || KKL10_UNITS[0];
      const snapshotDataUrl = canvas.toDataURL('image/png');
      const down20 = Math.round(u.price * 0.20);
      const bal80 = u.price - down20;
      const todayStr = new Date().toLocaleDateString('he-IL');

      const win = window.open('', '_blank', 'width=960,height=840');
      if (!win) return;
      win.document.write(`<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <title>הצעת מחיר ומפרט טכני — דירה ${u.num} · פרויקט קק"ל 10, פתח תקווה</title>
  <style>
    body { font-family: 'Segoe UI', Tahoma, Arial, sans-serif; margin: 0; padding: 28px; color: #0f172a; background: #ffffff; direction: rtl; }
    .hdr { display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #b45309; padding-bottom: 14px; margin-bottom: 18px; }
    .brand-box { display: flex; align-items: center; gap: 12px; }
    .logo { width: 64px; height: 52px; border-radius: 12px; background: #0f172a; color: #fbbf24; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 15px; }
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
    <button class="print-btn" onclick="window.print()">🖨️ הדפס / שמור הצעת מחיר כקובץ PDF</button>
  </div>
  <div class="hdr">
    <div class="brand-box">
      <div class="logo">קק"ל 10</div>
      <div>
        <div style="font-size:20px;font-weight:900;color:#0f172a;">יצחק קולסקי חברה לבניה והשקעות בע"מ</div>
        <div style="font-size:13px;color:#475569;font-weight:700;">פרויקט בוטיק קק"ל 10, פתח תקווה · אדריכלות: אדר' אייל סנדרוביץ'</div>
      </div>
    </div>
    <div style="text-align:left;font-size:12px;color:#475569;">
      <div><b>תאריך הפקה:</b> ${todayStr}</div>
      <div><b>גוש 6374 חלקה 112</b> · 25 יח"ד (8 קומות + 2 מרתפים)</div>
    </div>
  </div>

  <div class="grid">
    <div class="kpi"><div class="kpi-lbl">מספר דירה וטיפוס</div><div class="kpi-val">דירה ${u.num} (${u.type})</div></div>
    <div class="kpi"><div class="kpi-lbl">קומה ואגף</div><div class="kpi-val">קומה ${u.floor === 0 ? 'קרקע' : u.floor} (${u.wing})</div></div>
    <div class="kpi"><div class="kpi-lbl">שטח פנים + מרפסת/גינה</div><div class="kpi-val">${u.area} + ${u.balcony} מ"ר</div></div>
    <div class="kpi" style="background:#ecfdf5;border-color:#6ee7b7;"><div class="kpi-lbl" style="color:#065f46;">מחיר מחירון</div><div class="kpi-val" style="color:#047857;">${formatILS(u.price)}</div></div>
  </div>

  <div class="two-col">
    <div class="box">
      <div style="font-size:14px;font-weight:900;color:#b45309;margin-bottom:8px;">📋 מפרט טכני עשיר ותנאי תשלום — דירה ${u.num}</div>
      <table>
        <tr><td><b>מספר חדרים וטיפוס אדריכלי:</b></td><td>${u.rooms} חדרים (${u.type})</td></tr>
        <tr><td><b>כיווני אוויר ושמש:</b></td><td>${u.dir}</td></tr>
        <tr><td><b>חניה תת-קרקעית בטאבו:</b></td><td>${u.parking} (גישה ישירה מ-2 מעליות הבניין)</td></tr>
        <tr><td><b>מפרט פנים ונגרות:</b></td><td>ריצוף גרניט פורצלן 100×100/80×80, ארונות מטבח וחדרים בעץ בהיר, תריסי אור חשמליים, מיזוג VRF</td></tr>
        <tr><td><b>תנאי תשלום יזמיים (20/80):</b></td><td>20% בחתימה (${formatILS(down20)}) · 80% במסירת חזקה (${formatILS(bal80)})</td></tr>
        <tr><td><b>נגישות ומוקדי סביבה (GIS):</b></td><td>207 מ' למוסדות חינוך, 550 מ' לתחנת מטרו עיריית פ"ת (קו M2), מרכזי קניות וגינות במרחק הליכה</td></tr>
      </table>
    </div>
    <div class="box" style="display:flex;flex-direction:column;justify-content:space-between;">
      <div style="font-size:13px;font-weight:800;color:#0f172a;margin-bottom:6px;">📸 צילום חי מתוך מודל ה-BIM התלת-ממדי (1:50 CAD):</div>
      <img src="${snapshotDataUrl}" style="width:100%;height:225px;object-fit:cover;border-radius:8px;border:1px solid #cbd5e1;" />
      <div style="font-size:10px;color:#64748b;margin-top:6px;">* ההדמיה, המידות והמחירים להמחשה שיווקית בלבד וכפופים להסכם המכר המלא ולמפרט הטכני החתום של קבוצת קולסקי.</div>
    </div>
  </div>
</body>
</html>`);
      win.document.close();
    }

    // ============================================================================
    // GIS 46 POIS SIDEBAR, FILTERS & ACTIVE POI FLOATING CARD
    // ============================================================================
    function setGisCategory(cat, btn) {
      activeGisCategory = cat;
      document.querySelectorAll('#gis-cat-buttons .ui-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      renderGisPoiList();
      rebuildScopeOverlayBuffers();
    }

    function toggleGisRadii() {
      gisRadiiVisible = !gisRadiiVisible;
      const btn = document.getElementById('btn-top-radii');
      btn.textContent = gisRadiiVisible ? '⭕ רדיוסים: פעיל' : '⭕ רדיוסים: כבוי';
      btn.className = gisRadiiVisible ? 'ui-btn active' : 'ui-btn';
      rebuildScopeOverlayBuffers();
    }

    function toggleGisPois() {
      gisPoisVisible = !gisPoisVisible;
      const btn = document.getElementById('btn-top-pois');
      btn.textContent = gisPoisVisible ? '📍 מיקומים: פעיל' : '📍 מיקומים: כבוי';
      btn.className = gisPoisVisible ? 'ui-btn active' : 'ui-btn';
      if (!gisPoisVisible) document.getElementById('gis-active-card').style.display = 'none';
      rebuildScopeOverlayBuffers();
    }

    function renderGisPoiList() {
      const container = document.getElementById('gis-poi-list');
      if (!container) return;
      const filtered = KKL10_POIS.filter(p => activeGisCategory === 'all' || p.cat === activeGisCategory);
      container.innerHTML = filtered.map(p => {
        const idx = KKL10_POIS.indexOf(p);
        const isSel = (selectedPoiObj === p);
        return `
          <div onclick="selectGisPoi(${idx}, true)" style="display:flex;align-items:center;justify-content:space-between;padding:6px 9px;border-radius:8px;background:${isSel ? 'rgba(37,99,235,0.28)' : 'rgba(30,41,59,0.75)'};border:1px solid ${isSel ? '#38bdf8' : 'rgba(148,163,184,0.2)'};cursor:pointer;">
            <div style="display:flex;align-items:center;gap:7px;">
              <span style="width:9px;height:9px;border-radius:999px;background:${p.color};"></span>
              <div>
                <div style="font-size:11.5px;font-weight:800;color:#ffffff;">${p.name}</div>
                <div style="font-size:10px;color:#94a3b8;">${p.cat_he} · הליכה ~${p.walk_min} דק'</div>
              </div>
            </div>
            <span style="font-size:11px;font-weight:800;color:#38bdf8;">${p.dist} מ'</span>
          </div>
        `;
      }).join('');
    }

    function selectGisPoi(idx, fly = true) {
      const p = KKL10_POIS[idx];
      if (!p) return;
      selectedPoiObj = p;
      gisPoisVisible = true;
      rebuildScopeOverlayBuffers();
      renderGisPoiList();

      if (fly) {
        exitWalkMode();
        document.getElementById('isolateFloorCb').checked = false;
        resetClipping();
        cam.target = [6.36 + p.east_m * 0.45, 0.0, -(16.5 + p.north_m * 0.45)];
        cam.dist = Math.max(260, p.dist * 1.15);
        cam.pitch = 0.62;
      }

      const card = document.getElementById('gis-active-card');
      card.style.display = 'block';
      card.innerHTML = `
        <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:6px;">
          <div>
            <span style="background:${p.color}33;color:${p.color};border:1px solid ${p.color};padding:1px 7px;border-radius:999px;font-size:10px;font-weight:800;">${p.cat_he}</span>
            <div style="font-size:14px;font-weight:900;color:#ffffff;margin-top:4px;">📍 ${p.name}</div>
          </div>
          <button onclick="document.getElementById('gis-active-card').style.display='none';selectedPoiObj=null;rebuildScopeOverlayBuffers();" class="ui-btn" style="padding:2px 6px;">✕</button>
        </div>
        <div style="display:flex;gap:10px;font-size:11.5px;color:#cbd5e1;margin-bottom:8px;">
          <span>📏 <b>מרחק אווירי מקק"ל 10:</b> ${p.dist} מ'</span>
          <span>🚶 <b>זמן הליכה:</b> ~${p.walk_min} דק'</span>
        </div>
        <a href="https://www.google.com/maps/search/?api=1&query=${p.lat},${p.lon}" target="_blank" class="ui-btn" style="width:100%;background:#2563eb;color:#fff;border-color:#60a5fa;text-decoration:none;font-weight:800;">
          🗺️ פתח מיקום ב-Google Maps ↗
        </a>
      `;
    }

    // ============================================================================
    // 4 INTERIOR FINISH PACKAGES, LIGHTING, SUN SLIDER & 3D LASER MEASURE
    // ============================================================================
    const FINISH_PACKAGES = {
      nordic:  { label: 'Nordic Oak',       tile: [0.94, 0.93, 0.90], wood: [0.87, 0.72, 0.49], part: [0.95, 0.91, 0.82] },
      sahara:  { label: 'Warm Sahara',      tile: [0.92, 0.87, 0.78], wood: [0.78, 0.59, 0.38], part: [0.94, 0.89, 0.80] },
      urban:   { label: 'Urban Anthracite', tile: [0.82, 0.84, 0.87], wood: [0.91, 0.82, 0.64], part: [0.92, 0.93, 0.95] },
      parquet: { label: 'Classic Parquet',  tile: [0.86, 0.75, 0.58], wood: [0.84, 0.68, 0.45], part: [0.96, 0.93, 0.86] }
    };

    function applyFinishPackage(pkgKey, btn) {
      const pkg = FINISH_PACKAGES[pkgKey];
      if (!pkg) return;
      MATERIALS.Int_FloorTile.color = pkg.tile.slice();
      MATERIALS.Int_LightWood.color = pkg.wood.slice();
      MATERIALS.Int_Partition.color = pkg.part.slice();
      document.getElementById('active-pkg-badge').textContent = pkg.label;
      document.querySelectorAll('#pkg-buttons .pkg-card-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      rebuildBuffers();
    }

    function toggleNightMode() {
      isNightMode = !isNightMode;
      const btn = document.getElementById('btn-top-night');
      btn.textContent = isNightMode ? '☀️ מצב יום' : '🌙 מצב לילה';
      btn.className = isNightMode ? 'ui-btn active' : 'ui-btn';
      MATERIALS.A_Glass.color = isNightMode ? [0.98, 0.86, 0.52] : [0.58, 0.80, 0.94];
      MATERIALS.A_Glass.alpha = isNightMode ? 0.72 : 0.55;
      rebuildBuffers();
    }

    function updateSunAngle(degVal) {
      const deg = parseFloat(degVal);
      const rad = deg * Math.PI / 180;
      sunDirVec = [Math.cos(rad) * 0.75, Math.max(0.25, Math.sin(rad)), -0.45];
      const hour = Math.round(6 + (deg / 180) * 12);
      document.getElementById('sun-val').textContent = `${hour}:00 · ${hour < 11 ? 'בוקר' : (hour < 16 ? 'צהריים' : 'שעת הזהב')}`;
    }

    function toggleMeasureMode(forceState) {
      isMeasureMode = (typeof forceState === 'boolean') ? forceState : !isMeasureMode;
      measurePtA = null;
      const btn = document.getElementById('btn-top-measure');
      btn.className = isMeasureMode ? 'ui-btn active' : 'ui-btn';
      document.getElementById('measure-hud').style.display = isMeasureMode ? 'flex' : 'none';
    }

    function clearMeasurements() {
      measurePtA = null;
      measureSegments.length = 0;
      measureDomObjs.forEach(m => m.el.remove());
      measureDomObjs.length = 0;
      document.getElementById('measure-last-val').textContent = 'מוכן למדידה';
      rebuildScopeOverlayBuffers();
    }

    function handleMeasureClick(clientX, clientY) {
      if (!currentProjMat || !currentViewMat) return;
      const rect = canvas.getBoundingClientRect();
      const nx = ((clientX - rect.left) / rect.width) * 2 - 1;
      const ny = -((clientY - rect.top) / rect.height) * 2 + 1;

      const fl = FLOOR_LEVELS.find(f => f.idx === activePlanFloorIdx) || FLOOR_LEVELS[3];
      const planeY = (clipBounds.yMax < 31.2) ? (fl.y + 0.08) : 0.05;

      const yaw = cam.yaw, pitch = cam.pitch;
      const fwd = [-Math.cos(pitch) * Math.sin(yaw), -Math.sin(pitch), -Math.cos(pitch) * Math.cos(yaw)];
      const right = [Math.cos(yaw), 0, -Math.sin(yaw)];
      const up = [
        right[1]*fwd[2] - right[2]*fwd[1],
        right[2]*fwd[0] - right[0]*fwd[2],
        right[0]*fwd[1] - right[1]*fwd[0]
      ];
      const asp = rect.width / rect.height;
      let rayOrigin, rayDir;
      if (isOrtho && !cam.walkMode) {
        const halfH = cam.dist * 0.48;
        const halfW = halfH * asp;
        rayOrigin = [
          currentEyePos[0] + right[0] * nx * halfW + up[0] * ny * halfH,
          currentEyePos[1] + right[1] * nx * halfW + up[1] * ny * halfH,
          currentEyePos[2] + right[2] * nx * halfW + up[2] * ny * halfH
        ];
        rayDir = fwd;
      } else {
        const tanHalf = Math.tan(21 * Math.PI / 180);
        rayOrigin = currentEyePos;
        const rx = fwd[0] + right[0] * nx * tanHalf * asp + up[0] * ny * tanHalf;
        const ry = fwd[1] + right[1] * nx * tanHalf * asp + up[1] * ny * tanHalf;
        const rz = fwd[2] + right[2] * nx * tanHalf * asp + up[2] * ny * tanHalf;
        const rLen = Math.hypot(rx, ry, rz) || 1;
        rayDir = [rx / rLen, ry / rLen, rz / rLen];
      }
      if (Math.abs(rayDir[1]) < 0.001) return;
      const t = (planeY - rayOrigin[1]) / rayDir[1];
      if (t <= 0) return;
      const hitPt = [
        rayOrigin[0] + rayDir[0] * t,
        planeY,
        rayOrigin[2] + rayDir[2] * t
      ];

      if (!measurePtA) {
        measurePtA = hitPt;
        document.getElementById('measure-last-val').textContent = 'בחר נקודה שנייה...';
      } else {
        const dist = Math.hypot(hitPt[0] - measurePtA[0], hitPt[1] - measurePtA[1], hitPt[2] - measurePtA[2]);
        measureSegments.push({ a: measurePtA, b: hitPt, dist });
        const mid = [(measurePtA[0] + hitPt[0]) * 0.5, (measurePtA[1] + hitPt[1]) * 0.5 + 0.15, (measurePtA[2] + hitPt[2]) * 0.5];
        const el = document.createElement('div');
        el.style.cssText = 'position:absolute;transform:translate(-50%,-50%);background:#0284c7;color:#ffffff;font-weight:900;font-size:11px;padding:2px 8px;border-radius:999px;border:1.5px solid #ffffff;white-space:nowrap;box-shadow:0 4px 10px rgba(0,0,0,0.45);';
        el.textContent = `📏 ${dist.toFixed(2)} מ' (${Math.round(dist * 100)} ס"מ)`;
        document.getElementById('measure-overlay').appendChild(el);
        measureDomObjs.push({ el, pos: mid });
        document.getElementById('measure-last-val').textContent = `מרחק: ${dist.toFixed(2)} מ'`;
        measurePtA = null;
        rebuildScopeOverlayBuffers();
      }
    }

    // ============================================================================
    // UI POPOVER DRAWERS, CLIPPING & EXPORT HANDLERS
    // ============================================================================
    function closeAllDrawers() {
      document.querySelectorAll('.dropdown-drawer.open').forEach(d => d.classList.remove('open'));
      document.querySelectorAll('.menu-trigger-btn.open').forEach(b => b.classList.remove('open'));
    }

    function toggleDrawer(id, btn) {
      const drw = document.getElementById(id);
      if (!drw) return;
      const wasOpen = drw.classList.contains('open');
      closeAllDrawers();
      if (!wasOpen) {
        drw.classList.add('open');
        if (btn) btn.classList.add('open');
      }
    }

    function toggleSectionsPanel(btn) {
      const p = document.getElementById('sections-panel');
      const collapsed = p.classList.toggle('collapsed');
      btn.textContent = collapsed ? '+ חתכים' : '▾';
    }

    function toggleLayer(layer, checked) {
      layerState[layer] = checked;
      rebuildBuffers();
    }

    function toggleAllLayers(state) {
      for (const k in layerState) layerState[k] = state;
      document.querySelectorAll('#layerList input[type="checkbox"]').forEach(cb => cb.checked = state);
      rebuildBuffers();
    }

    function updateClipping(selectedFloor = null) {
      clipBounds.yMax = parseFloat(document.getElementById('clipY').value);
      clipBounds.x = parseFloat(document.getElementById('clipX').value);
      clipBounds.n = parseFloat(document.getElementById('clipZ').value);

      const activeFl = selectedFloor || FLOOR_LEVELS.slice().reverse().find(f => clipBounds.yMax >= f.y + 0.5);
      if (activeFl) activePlanFloorIdx = activeFl.idx;

      const isolate = document.getElementById('isolateFloorCb').checked;
      if (isolate && activeFl) {
        clipBounds.yMin = activeFl.y - 0.35;
      } else {
        clipBounds.yMin = -9.5;
      }

      if (activeFl && clipBounds.yMax < 31.2) {
        document.getElementById('activeFloorTitle').textContent = `📐 ${activeFl.heb} — ${activeFl.name}`;
      } else {
        document.getElementById('activeFloorTitle').textContent = `🏢 מבנה שלם על גבי מפת פתח תקווה | 25 דירות · 46 מוקדי GIS`;
      }

      document.getElementById('clipYVal').textContent = (clipBounds.yMax >= 0 ? '+' : '') + clipBounds.yMax.toFixed(2) + ' m';
      document.getElementById('clipXVal').textContent = (clipBounds.x >= 0 ? '+' : '') + clipBounds.x.toFixed(1) + 'm';
      document.getElementById('clipZVal').textContent = (clipBounds.n >= 0 ? '+' : '') + clipBounds.n.toFixed(1) + 'm';
    }

    function resetClipping() {
      document.getElementById('clipY').value = 32.0;
      document.getElementById('clipX').value = 17.0;
      document.getElementById('clipZ').value = 38.0;
      document.getElementById('isolateFloorCb').checked = false;
      activeParkingHighlight = null;
      updateClipping();
      rebuildScopeOverlayBuffers();
    }

    function toggleWireframe() {
      showEdges = !showEdges;
      const btn = document.getElementById('wireBtn');
      btn.textContent = `🔲 קווי מתאר: ${showEdges ? 'פעיל' : 'כבוי'}`;
      btn.className = showEdges ? 'ui-btn active' : 'ui-btn';
      rebuildBuffers();
    }

    function populateFloorSchedule() {
      const container = document.getElementById('floorScheduleList');
      container.innerHTML = FLOOR_LEVELS.slice().reverse().map(f => `
        <button onclick="viewFloorPlan(${f.idx})" class="ui-btn" style="justify-content:space-between;padding:4px 8px;font-size:11px;">
          <span>${f.heb}</span>
          <span class="font-mono text-amber-400" style="direction:ltr;font-size:10px;">${f.y >= 0 ? '+' : ''}${f.y.toFixed(2)}m</span>
        </button>
      `).join('');
    }

    function exportOBJ() {
      let obj = `# KKL 10, Petah Tikva - Full Interior + Exterior BIM Model v6.1 (Light-Wood Cabinets + Floor CAD Dims)\n`;
      let vOffset = 1;
      const byLayer = {};
      for (const m of meshes) {
        if (!byLayer[m.layer]) byLayer[m.layer] = [];
        byLayer[m.layer].push(m);
      }
      for (const layerName of Object.keys(byLayer)) {
        obj += `\no Layer_${layerName}\ng ${layerName}\n`;
        for (const m of byLayer[layerName]) {
          obj += `usemtl ${MATERIALS[m.matKey].name}\n`;
          for (const pt of m.v) {
            obj += `v ${pt[0].toFixed(4)} ${pt[1].toFixed(4)} ${pt[2].toFixed(4)}\n`;
          }
          for (const f of m.faces) {
            const i = f.idx;
            obj += `f ${vOffset + i[0]} ${vOffset + i[1]} ${vOffset + i[2]}\n`;
            obj += `f ${vOffset + i[3]} ${vOffset + i[4]} ${vOffset + i[5]}\n`;
          }
          vOffset += 8;
        }
      }
      const blob = new Blob([obj], { type: 'text/plain' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'KKL10_PetahTikva_BIM_v6_1_LightWood.obj';
      a.click();
    }

    function downloadThreeJSGenerator() {
      const elementsJSON = JSON.stringify(meshes.map(m => ({
        layer: m.layer, matKey: m.matKey, tag: m.tag, v: m.v
      })));
      const code = `export const KKL10_BIM_SOLIDS = ${elementsJSON};\n`;
      const blob = new Blob([code], { type: 'text/javascript' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'kkl10_threejs_bim_v6_1.js';
      a.click();
    }

    // Initialize Untouched Architectural BIM Model + Petah Tikva 3D Map Base + All Scope Deliverables
    buildKKL10Model();
    initGroundMapPlanes();
    populateFloorSchedule();
    initDOMOverlays();
    renderUnitsCatalogList();
    renderGisPoiList();
    rebuildBuffers();
    resetClipping();
    requestAnimationFrame(renderLoop);
  </script>
</body>
</html>
"""

full_html = (
    HTML_HEADER_AND_UI
    + "\n    // --- EMBEDDED CRM (25 UNITS), GIS (46 POIS) & PETAH TIKVA GOOGLE MAPS TEXTURES ---\n    "
    + embedded_scope_data_js
    + map_constants_js
    + "\n    // --- UNTOUCHED ARCHITECTURAL 3D BIM & 2D CAD MODEL (v6.1) ---\n"
    + untouched_arch_model_js
    + WEBGL_AND_SCOPE_JS
)

for root in [BRAIN_DIR, SCRATCH_DIR, GDRIVE_DIR]:
    viewer_file = os.path.join(root, "kkl10_3d_bim_viewer.html")
    index_file = os.path.join(root, "index.html")
    with open(viewer_file, "w", encoding="utf-8") as f:
        f.write(full_html)
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Wrote {viewer_file} and {index_file} ({len(full_html)} chars)")
