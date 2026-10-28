import json
from pathlib import Path

map_3d_path = Path(r"C:\Users\User\.gemini\antigravity\scratch\kkl10\data\unified_3d_map.json")
mdata = json.loads(map_3d_path.read_text(encoding="utf-8"))
outer_json = json.dumps(mdata["outer_z15"], ensure_ascii=False)
inner_json = json.dumps(mdata["inner_z17"], ensure_ascii=False)
close_json = json.dumps(mdata["closeup_z19"], ensure_ascii=False)

spatial_path = Path(r"C:\Users\User\.gemini\antigravity\brain\17cdeb22-38a8-4e04-b15d-67ce64232225\kkl10_spatial_map.html")
html = spatial_path.read_text(encoding="utf-8")

old_draw_start = """      const cx = w * 0.5 + cam.x;
      const cy = h * 0.5 + cam.y;"""

new_draw_start = """      const cx = w * 0.5 + cam.x;
      const cy = h * 0.5 + cam.y;

      // Draw Petah Tikva Google Maps Hybrid Ground Layers
      if (window._gmapsImgs) {
        for (const layer of window._gmapsImgs) {
          if (layer.img.complete && layer.img.naturalWidth > 0) {
            const span = layer.meta.world_span_m * cam.scale;
            ctx.save();
            ctx.globalAlpha = 0.88;
            ctx.drawImage(layer.img, cx - span * 0.5, cy - span * 0.5, span, span);
            ctx.restore();
          }
        }
      }"""

init_code = f"""
    const GMAPS_LAYERS = [
      {outer_json},
      {inner_json},
      {close_json}
    ];
    window._gmapsImgs = GMAPS_LAYERS.map(meta => {{
      const img = new Image();
      img.onload = () => draw();
      img.src = meta.data_uri;
      return {{ meta, img }};
    }});
"""

html = html.replace(old_draw_start, new_draw_start)
html = html.replace("resetView();", init_code + "\n    resetView();")

targets = [
    Path(r"C:\Users\User\.gemini\antigravity\brain\17cdeb22-38a8-4e04-b15d-67ce64232225\kkl10_spatial_map.html"),
    Path(r"C:\Users\User\.gemini\antigravity\scratch\kkl10\kkl10_spatial_map.html"),
    Path(r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\קקל 10 פתח תקווה\kkl10_spatial_map.html"),
]
for t in targets:
    t.write_text(html, encoding="utf-8")
    print("Updated", t)
