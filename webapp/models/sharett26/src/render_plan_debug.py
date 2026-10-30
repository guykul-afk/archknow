# -*- coding: utf-8 -*-
import json, fitz

with open(r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה\data\sharett_extracted_plans.json", "r", encoding="utf-8") as f:
    plans = json.load(f)

def render_plan_debug(pname, out_name):
    doc = fitz.open()
    W, H = 1200, 1000
    p = doc.new_page(width=W, height=H)
    scale = 28.0
    cx, cy = W / 2.0, H / 2.0
    def to_px(x, y):
        return (cx + x * scale, cy + y * scale)

    # 1. Draw CAD lines in light gray, furn_lines in blue
    for s in plans[pname]["cad_lines"]:
        p.draw_line(to_px(s[0], s[1]), to_px(s[2], s[3]), color=(0.75, 0.78, 0.82), width=0.6)
    for s in plans[pname]["furn_lines"]:
        p.draw_line(to_px(s[0], s[1]), to_px(s[2], s[3]), color=(0.15, 0.45, 0.85), width=1.1)

    # 2. Draw wall_polys in dark charcoal
    for wp in plans[pname]["wall_polys"]:
        ext = wp["exterior"]
        for i in range(len(ext)):
            p.draw_line(to_px(ext[i][0], ext[i][1]), to_px(ext[(i+1)%len(ext)][0], ext[(i+1)%len(ext)][1]), color=(0.1, 0.1, 0.1), width=1.8)
        for h in wp.get("holes", []):
            for i in range(len(h)):
                p.draw_line(to_px(h[i][0], h[i][1]), to_px(h[(i+1)%len(h)][0], h[(i+1)%len(h)][1]), color=(0.1, 0.1, 0.1), width=1.4)

    # 3. Draw grid every 2m with coordinate labels
    for xm in range(-18, 19, 2):
        p.draw_line(to_px(xm, -16), to_px(xm, 16), color=(1, 0, 0) if xm == 0 else (0.9, 0.9, 0.9), width=0.5)
        p.insert_text((to_px(xm, -15.5)[0] - 8, to_px(xm, -15.5)[1]), f"{xm}", color=(0.8, 0, 0), fontsize=8)
    for ym in range(-14, 16, 2):
        p.draw_line(to_px(-18, ym), to_px(18, ym), color=(1, 0, 0) if ym == 0 else (0.9, 0.9, 0.9), width=0.5)
        p.insert_text((to_px(-17.8, ym)[0], to_px(-17.8, ym)[1] + 3), f"{ym}", color=(0.8, 0, 0), fontsize=8)

    p.get_pixmap().save(out_name)

render_plan_debug("ground", r"C:\Users\User\.gemini\antigravity\brain\71931cc9-7058-41f3-a9f0-80549e5c535b\scratch\debug_ground.png")
render_plan_debug("gallery", r"C:\Users\User\.gemini\antigravity\brain\71931cc9-7058-41f3-a9f0-80549e5c535b\scratch\debug_gallery.png")
render_plan_debug("floors_1267", r"C:\Users\User\.gemini\antigravity\brain\71931cc9-7058-41f3-a9f0-80549e5c535b\scratch\debug_f1267.png")
print("Rendered debug_ground, debug_gallery, debug_f1267")
