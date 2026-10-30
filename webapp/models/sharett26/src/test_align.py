import math, fitz

halfSpanM = 259.039 / 2.0  # 129.5195 m
mpp = 259.039 / 1024.0     # 0.25296777 m/px

# We want the building center (x3d=0, z3d=0) to sit at pixel (496, 514),
# and the street line (z3d = +20.0m, x3d = -25..+25m) to lie right along the center of Moshe Sharett St
# from (256, 578) to (768, 636) -> slope = +58 / 512 => angle = +6.46 deg!

def test_overlay(theta_deg, cx, cz, out_name):
    theta = theta_deg * math.pi / 180.0
    ct, st = math.cos(theta), math.sin(theta)
    # Inverse of:
    # dx = eastM * ct - northM * st = x3d - cx
    # dy = eastM * st + northM * ct = cz - z3d
    # => eastM  = (x3d - cx)*ct + (cz - z3d)*st
    # => northM = -(x3d - cx)*st + (cz - z3d)*ct
    def world_to_px(x3d, z3d):
        dx = x3d - cx
        dy = cz - z3d
        eastM = dx * ct + dy * st
        northM = -dx * st + dy * ct
        px = 512.0 + eastM / mpp
        py = 512.0 - northM / mpp
        return (px, py)

    doc = fitz.open()
    p = doc.new_page(width=1024, height=1024)
    p.insert_image(fitz.Rect(0, 0, 1024, 1024), filename=r"C:\Users\User\.gemini\antigravity\brain\71931cc9-7058-41f3-a9f0-80549e5c535b\scratch\closeup_z19.png")

    # Draw Lot Boundary (-20.48..+20.48, -17.71..+17.50) in yellow
    lot = [(-20.48, -17.71), (20.48, -17.71), (20.48, 17.50), (-20.48, 17.50)]
    lot_px = [world_to_px(x, z) for x, z in lot]
    for i in range(4):
        p.draw_line(lot_px[i], lot_px[(i+1)%4], color=(1, 1, 0), width=2.5)

    # Draw Building Footprint (-16.87..+16.63, -13.24..+13.65) in cyan
    bldg = [(-16.87, -13.24), (16.63, -13.24), (16.63, 13.65), (-16.87, 13.65)]
    bldg_px = [world_to_px(x, z) for x, z in bldg]
    for i in range(4):
        p.draw_line(bldg_px[i], bldg_px[(i+1)%4], color=(0, 1, 1), width=3.0)

    # Draw Street Roadway (-24..+24, +18.80..+24.50) in red/magenta
    st_poly = [(-24.0, 18.80), (24.0, 18.80), (24.0, 24.50), (-24.0, 24.50)]
    st_px = [world_to_px(x, z) for x, z in st_poly]
    for i in range(4):
        p.draw_line(st_px[i], st_px[(i+1)%4], color=(1, 0, 0.5), width=2.5)

    p.get_pixmap().save(out_name)

test_overlay(+6.8, 3.8, -5.0, r"C:\Users\User\.gemini\antigravity\brain\71931cc9-7058-41f3-a9f0-80549e5c535b\scratch\align_test3.png")
print("Saved align_test3.png")
