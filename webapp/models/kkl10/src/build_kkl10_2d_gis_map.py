import json
import os

BRAIN_DIR = r"C:\Users\User\.gemini\antigravity\brain\17cdeb22-38a8-4e04-b15d-67ce64232225"
SCRATCH_DIR = r"C:\Users\User\.gemini\antigravity\scratch\kkl10"
GDRIVE_DIR = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\קקל 10 פתח תקווה"

with open(os.path.join(SCRATCH_DIR, "data", "spatial_map_data.json"), "r", encoding="utf-8") as f:
    spatial_data = json.load(f)

pois_json = json.dumps(spatial_data["pois"], ensure_ascii=False)

HTML_2D_MAP = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>קק"ל 10, פתח תקווה — מפת סביבה, מרחקים ו-46 מוקדי עניין (GIS)</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body, html {{ width: 100%; height: 100%; overflow: hidden; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; background: #0f172a; color: #f8fafc; }}
    #map-canvas {{ width: 100%; height: 100%; display: block; cursor: grab; }}
    #map-canvas:active {{ cursor: grabbing; }}
    .glass {{
      background: rgba(15, 23, 42, 0.92);
      border: 1px solid rgba(148, 163, 184, 0.28);
      backdrop-filter: blur(12px);
      border-radius: 14px;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
    }}
    .top-bar {{
      position: absolute; top: 14px; right: 14px; left: 14px; z-index: 20;
      display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;
      padding: 10px 16px;
    }}
    .sidebar {{
      position: absolute; top: 76px; right: 14px; bottom: 14px; width: 360px; z-index: 20;
      display: flex; flex-direction: column; gap: 10px; padding: 14px;
    }}
    .chip {{
      border: 1px solid #334155; background: #1e293b; color: #e2e8f0;
      padding: 5px 10px; border-radius: 8px; font-size: 11.5px; font-weight: 700; cursor: pointer;
    }}
    .chip.active {{ background: #2563eb; border-color: #3b82f6; color: #fff; }}
    .poi-list {{ flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 6px; padding-left: 4px; }}
    .poi-item {{
      display: flex; align-items: center; justify-content: space-between; gap: 8px;
      padding: 8px 10px; border-radius: 10px; background: rgba(30, 41, 59, 0.75);
      border: 1px solid rgba(71, 85, 105, 0.5); cursor: pointer; transition: 0.15s;
    }}
    .poi-item:hover, .poi-item.active {{ background: rgba(37, 99, 235, 0.25); border-color: #3b82f6; }}
  </style>
</head>
<body>
  <canvas id="map-canvas"></canvas>

  <header class="glass top-bar">
    <div style="display:flex;align-items:center;gap:10px;">
      <div style="background:#f59e0b;color:#0f172a;font-weight:900;padding:6px 10px;border-radius:8px;font-size:13px;">קק"ל 10</div>
      <div>
        <div style="font-size:15px;font-weight:800;">קבוצת קולסקי · קק"ל 10, פתח תקווה — מפת GIS ו-46 מוקדי סביבה</div>
        <div style="font-size:11px;color:#94a3b8;">גוש 6374 חלקה 112 · רדיוסי הליכה מדויקים (150 מ' עד 2,000 מ') · לחץ על מוקד לפרטים</div>
      </div>
    </div>
    <div style="display:flex;gap:8px;align-items:center;">
      <button onclick="resetView()" class="chip">🎯 מרכז לקק"ל 10</button>
      <a href="kkl10_3d_bim_viewer.html" class="chip active" style="text-decoration:none;">🏢 חזרה למודל ה-3D BIM</a>
    </div>
  </header>

  <aside class="glass sidebar">
    <div style="font-size:13px;font-weight:800;color:#fbbf24;">סינון 46 מוקדי עניין בפתח תקווה:</div>
    <div style="display:flex;flex-wrap:wrap;gap:5px;" id="cat-bar">
      <button class="chip active" onclick="setCat('all', this)">הכל (46)</button>
      <button class="chip" onclick="setCat('education', this)">🎓 חינוך</button>
      <button class="chip" onclick="setCat('transport', this)">🚌 תחבורה ומטרו</button>
      <button class="chip" onclick="setCat('shopping', this)">🛒 קניות</button>
      <button class="chip" onclick="setCat('parks', this)">🌳 פארקים</button>
      <button class="chip" onclick="setCat('health', this)">🏥 בריאות</button>
    </div>
    <div class="poi-list" id="poi-list"></div>
  </aside>

  <script>
    const POIS = {pois_json};
    const RINGS = [150, 250, 350, 500, 750, 1000, 1500, 2000];
    let activeCat = 'all';
    let selectedPoi = null;
    let cam = {{ x: 0, y: 0, scale: 0.32 }};

    const canvas = document.getElementById('map-canvas');
    const ctx = canvas.getContext('2d');

    function setCat(c, btn) {{
      activeCat = c;
      document.querySelectorAll('#cat-bar .chip').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderList();
      draw();
    }}

    function resetView() {{
      cam = {{ x: -160, y: 0, scale: 0.32 }};
      draw();
    }}

    function renderList() {{
      const list = document.getElementById('poi-list');
      const filtered = POIS.filter(p => activeCat === 'all' || p.cat === activeCat);
      list.innerHTML = filtered.map((p, idx) => `
        <div class="poi-item ${{selectedPoi === p ? 'active' : ''}}" onclick="focusPoi(${{POIS.indexOf(p)}})">
          <div>
            <div style="font-size:12px;font-weight:800;color:#fff;">${{p.name}}</div>
            <div style="font-size:10.5px;color:#94a3b8;">${{p.cat_he}} · הליכה ~${{p.walk_min}} דק'</div>
          </div>
          <span style="background:${{p.color}}22;color:${{p.color}};border:1px solid ${{p.color}}66;padding:2px 7px;border-radius:999px;font-size:11px;font-weight:800;white-space:nowrap;">
            ${{p.dist}} מ'
          </span>
        </div>
      `).join('');
    }}

    function focusPoi(i) {{
      selectedPoi = POIS[i];
      cam.x = -selectedPoi.east_m * cam.scale * 0.5 - 140;
      cam.y = selectedPoi.north_m * cam.scale * 0.5;
      renderList();
      draw();
    }}

    function draw() {{
      const dpr = window.devicePixelRatio || 1;
      canvas.width = window.innerWidth * dpr;
      canvas.height = window.innerHeight * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      const w = window.innerWidth, h = window.innerHeight;
      ctx.fillStyle = '#090d16';
      ctx.fillRect(0, 0, w, h);

      const cx = w * 0.5 + cam.x;
      const cy = h * 0.5 + cam.y;

      // Grid
      ctx.strokeStyle = 'rgba(148,163,184,0.06)';
      ctx.lineWidth = 1;
      const step = 100 * cam.scale;
      if (step > 8) {{
        for (let x = cx % step; x < w; x += step) {{ ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke(); }}
        for (let y = cy % step; y < h; y += step) {{ ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke(); }}
      }}

      // Concentric Distance Rings
      for (const r of RINGS) {{
        const rad = r * cam.scale;
        ctx.beginPath();
        ctx.arc(cx, cy, rad, 0, Math.PI * 2);
        ctx.strokeStyle = r <= 500 ? 'rgba(16, 185, 129, 0.35)' : 'rgba(59, 130, 246, 0.28)';
        ctx.setLineDash([5, 5]);
        ctx.lineWidth = 1.5;
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = '#94a3b8';
        ctx.font = 'bold 11px system-ui';
        ctx.fillText(r + " מ'", cx + 6, cy - rad + 13);
      }}

      // Selected POI radial line
      if (selectedPoi) {{
        const px = cx + selectedPoi.east_m * cam.scale;
        const py = cy - selectedPoi.north_m * cam.scale;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(px, py);
        ctx.strokeStyle = '#fbbf24';
        ctx.lineWidth = 2.5;
        ctx.setLineDash([6, 4]);
        ctx.stroke();
        ctx.setLineDash([]);
      }}

      // POIs
      for (const p of POIS) {{
        if (activeCat !== 'all' && p.cat !== activeCat) continue;
        const px = cx + p.east_m * cam.scale;
        const py = cy - p.north_m * cam.scale;
        const isSel = (selectedPoi === p);

        ctx.beginPath();
        ctx.arc(px, py, isSel ? 9 : 6, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = isSel ? 2.5 : 1.5;
        ctx.stroke();

        if (cam.scale > 0.22 || isSel) {{
          ctx.fillStyle = isSel ? '#fde047' : '#e2e8f0';
          ctx.font = (isSel ? 'bold 12px' : '600 10.5px') + ' system-ui';
          ctx.fillText(`${{p.name}} (${{p.dist}} מ')`, px + 10, py + 4);
        }}
      }}

      // KKL 10 Center Marker
      ctx.beginPath();
      ctx.arc(cx, cy, 11, 0, Math.PI * 2);
      ctx.fillStyle = '#f59e0b';
      ctx.fill();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 3;
      ctx.stroke();
      ctx.fillStyle = '#fde047';
      ctx.font = '900 13px system-ui';
      ctx.fillText('🏢 פרויקט קק"ל 10, פתח תקווה', cx + 15, cy + 5);
    }}

    let dragging = false, lx = 0, ly = 0;
    canvas.addEventListener('mousedown', e => {{ dragging = true; lx = e.clientX; ly = e.clientY; }});
    window.addEventListener('mouseup', () => dragging = false);
    window.addEventListener('mousemove', e => {{
      if (!dragging) return;
      cam.x += e.clientX - lx; cam.y += e.clientY - ly;
      lx = e.clientX; ly = e.clientY;
      draw();
    }});
    canvas.addEventListener('wheel', e => {{
      e.preventDefault();
      cam.scale = Math.max(0.08, Math.min(2.5, cam.scale * (1 - e.deltaY * 0.001)));
      draw();
    }}, {{ passive: false }});
    window.addEventListener('resize', draw);

    resetView();
    renderList();
  </script>
</body>
</html>
"""

for root in [BRAIN_DIR, SCRATCH_DIR, GDRIVE_DIR]:
    with open(os.path.join(root, "kkl10_spatial_map.html"), "w", encoding="utf-8") as f:
        f.write(HTML_2D_MAP)
print("Generated kkl10_spatial_map.html in all 3 directories!")
