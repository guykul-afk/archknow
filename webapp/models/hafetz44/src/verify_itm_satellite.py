import urllib.request, io, math
from PIL import Image, ImageDraw
from pyproj import Transformer

t = Transformer.from_crs('EPSG:2039', 'EPSG:4326', always_xy=True)

# 4 Parcel corners (Total 58.15m x 18.40m = 1,067 sqm)
p1_e, p1_n = 189575.46, 665350.11 # SE (Street front)
p2_e, p2_n = 189519.44, 665334.51 # SW (Rear)
p3_e, p3_n = 189514.50, 665352.23 # NW (Rear)
p4_e, p4_n = 189570.52, 665367.83 # NE (Street front)

# Unit vectors from Pt 1 along South edge (toward West, length 58.15m) and along East edge (toward North, length 18.40m)
ux, uy = (p2_e - p1_e) / 58.15, (p2_n - p1_n) / 58.15
vx, vy = (p4_e - p1_e) / 18.40, (p4_n - p1_n) / 18.40

# Lot 85-2 (Residential net lot after 5.38m road expropriation on East and 13.95m public space on West):
# Starts at 5.38m from Pt 1/4, ends at 5.38 + 38.82 = 44.20m from Pt 1/4
lot85_2_itm = [
    (p1_e + ux * 5.38,  p1_n + uy * 5.38),
    (p1_e + ux * 44.20, p1_n + uy * 44.20),
    (p4_e + ux * 44.20, p4_n + uy * 44.20),
    (p4_e + ux * 5.38,  p4_n + uy * 5.38),
]

# Center of Lot 85-2 (x=0, y=0 in our 3D model):
c_e = p1_e + ux * (5.38 + 38.82 / 2.0) + vx * (18.40 / 2.0)
c_n = p1_n + uy * (5.38 + 38.82 / 2.0) + vy * (18.40 / 2.0)
c_lon, c_lat = t.transform(c_e, c_n)
print(f"Lot 85-2 Center: lat={c_lat:.7f}, lon={c_lon:.7f}")

# Building enclosed footprint in local model coords (x in [-13.361..14.359], y in [-5.184..4.216])
# Note: in local model coords:
# +x points East (toward Street, i.e. -ux, -uy)
# +y points South (toward Pt1-Pt2 edge, i.e. -vx, -vy)
def model_xy_to_latlon(mx, my):
    e = c_e - ux * mx - vx * my
    n = c_n - uy * mx - vy * my
    lon, lat = t.transform(e, n)
    return lat, lon

# Fetch Z19 Google Satellite + Hybrid around (c_lat, c_lon)
zoom = 19
lat_rad = math.radians(c_lat)
n_tiles = 2.0 ** zoom
cx = (c_lon + 180.0) / 360.0 * n_tiles
cy = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n_tiles
sx, sy = int(math.floor(cx)) - 1, int(math.floor(cy)) - 1

canvas = Image.new("RGB", (3 * 256, 3 * 256))
for dx in range(3):
    for dy in range(3):
        url = f"https://mt1.google.com/vt/lyrs=y&x={sx+dx}&y={sy+dy}&z={zoom}&hl=iw"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            im = Image.open(io.BytesIO(r.read())).convert("RGB")
            canvas.paste(im, (dx * 256, dy * 256))

def latlon_to_px(lat, lon):
    lr = math.radians(lat)
    tx = (lon + 180.0) / 360.0 * n_tiles
    ty = (1.0 - math.asinh(math.tan(lr)) / math.pi) / 2.0 * n_tiles
    return (tx - sx) * 256.0, (ty - sy) * 256.0

draw = ImageDraw.Draw(canvas)
# Draw full parcel 85 (1..4) in yellow
full_poly = [latlon_to_px(*t.transform(e, n)[::-1]) for e, n in [(p1_e,p1_n),(p2_e,p2_n),(p3_e,p3_n),(p4_e,p4_n)]]
draw.polygon(full_poly, outline=(255, 230, 0), width=3)

# Draw Lot 85-2 (38.82x18.40m) in cyan
lot2_poly = [latlon_to_px(*t.transform(e, n)[::-1]) for e, n in lot85_2_itm]
draw.polygon(lot2_poly, outline=(0, 220, 255), width=3)

# Draw Building footprint in red
bldg_corners = [(-13.361, -5.184), (14.359, -5.184), (14.359, 4.216), (-13.361, 4.216)]
bldg_poly = [latlon_to_px(*model_xy_to_latlon(x, y)) for x, y in bldg_corners]
draw.polygon(bldg_poly, outline=(255, 50, 50), width=4)

out_path = r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\crops\smart\verify_itm_satellite.jpg"
canvas.save(out_path, quality=92)
print("Saved", out_path)
