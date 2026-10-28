import urllib.request
import math
import io
import base64
import json
import os
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

WORKSPACE = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\הרב קיטרוני 37-39 פתח תקווה"
ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\7493e840-6f07-4fdb-9508-8c38dfc14844"
SCRATCH_DIR = os.path.join(ARTIFACT_DIR, "scratch")
PINES_SCRATCH = r"C:\Users\User\.gemini\antigravity\brain\60b6f7e6-94a5-48b9-b12c-1728c4428342\scratch"

# Exact verified midpoint between Kitroni 37 (32.081801, 34.890261) and Kitroni 39 (32.081646, 34.890340)
CENTER_LAT = 32.081724
CENTER_LON = 34.890301
R_MERC = 6378137.0
COS_LAT0 = math.cos(math.radians(CENTER_LAT))

def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2)**2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def latlon_to_tile_xy(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = (lon + 180.0) / 360.0 * n
    ytile = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
    return xtile, ytile

def fetch_symmetric_map(zoom, grid_size, half_px, out_px, lyrs="y", quality=85):
    cx, cy = latlon_to_tile_xy(CENTER_LAT, CENTER_LON, zoom)
    start_x = int(math.floor(cx - grid_size / 2.0))
    start_y = int(math.floor(cy - grid_size / 2.0))

    canvas = Image.new('RGB', (grid_size * 256, grid_size * 256))

    def fetch_one(args):
        dx, dy = args
        tx = start_x + dx
        ty = start_y + dy
        url = f"https://mt1.google.com/vt/lyrs={lyrs}&x={tx}&y={ty}&z={zoom}&hl=iw"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=12) as r:
                im = Image.open(io.BytesIO(r.read())).convert('RGB')
                return dx, dy, im
        except Exception as e:
            print(f"Error z={zoom} tile ({dx},{dy}):", e)
            return dx, dy, None

    coords = [(dx, dy) for dx in range(grid_size) for dy in range(grid_size)]
    with ThreadPoolExecutor(max_workers=16) as ex:
        for dx, dy, im in ex.map(fetch_one, coords):
            if im:
                canvas.paste(im, (dx * 256, dy * 256))

    px_cx = (cx - start_x) * 256.0
    px_cy = (cy - start_y) * 256.0
    left = int(round(px_cx - half_px))
    top = int(round(px_cy - half_px))
    size_px = half_px * 2
    cropped = canvas.crop((left, top, left + size_px, top + size_px))

    if size_px != out_px:
        final_img = cropped.resize((out_px, out_px), Image.Resampling.LANCZOS)
    else:
        final_img = cropped

    mpp_raw = (2.0 * math.pi * R_MERC * COS_LAT0) / (256.0 * (2 ** zoom))
    world_span_m = size_px * mpp_raw

    buf = io.BytesIO()
    final_img.save(buf, format='JPEG', quality=quality)
    b64_uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode('ascii')
    return {
        "zoom": zoom,
        "world_span_m": round(world_span_m, 3),
        "data_uri": b64_uri
    }

def fetch_rect_map_2d(zoom, w_px=1280, h_px=1024, lyrs="y", quality=84):
    grid_size = 8
    cx, cy = latlon_to_tile_xy(CENTER_LAT, CENTER_LON, zoom)
    start_x = int(math.floor(cx - grid_size / 2.0))
    start_y = int(math.floor(cy - grid_size / 2.0))
    canvas = Image.new('RGB', (grid_size * 256, grid_size * 256))

    def fetch_one(args):
        dx, dy = args
        tx, ty = start_x + dx, start_y + dy
        url = f"https://mt1.google.com/vt/lyrs={lyrs}&x={tx}&y={ty}&z={zoom}&hl=iw"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=12) as r:
                return dx, dy, Image.open(io.BytesIO(r.read())).convert('RGB')
        except Exception:
            return dx, dy, None

    coords = [(dx, dy) for dx in range(grid_size) for dy in range(grid_size)]
    with ThreadPoolExecutor(max_workers=16) as ex:
        for dx, dy, im in ex.map(fetch_one, coords):
            if im:
                canvas.paste(im, (dx * 256, dy * 256))

    px_cx = (cx - start_x) * 256.0
    px_cy = (cy - start_y) * 256.0
    left = int(round(px_cx - w_px / 2))
    top = int(round(px_cy - h_px / 2))
    cropped = canvas.crop((left, top, left + w_px, top + h_px))
    buf = io.BytesIO()
    cropped.save(buf, format='JPEG', quality=quality)
    mpp = (2.0 * math.pi * R_MERC * COS_LAT0) / (256.0 * (2 ** zoom))
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode('ascii'), mpp

print("Fetching 3D Triple-Resolution Maps (Z15, Z17, Z19) centered on Kitroni 37-39...")
outer_map = fetch_symmetric_map(zoom=15, grid_size=8, half_px=896, out_px=1600, quality=82)
inner_map = fetch_symmetric_map(zoom=17, grid_size=8, half_px=800, out_px=1600, quality=84)
closeup_map = fetch_symmetric_map(zoom=19, grid_size=6, half_px=512, out_px=1400, quality=86)

unified_3d = {
    "center_lat": CENTER_LAT,
    "center_lon": CENTER_LON,
    "outer_z15": outer_map,
    "inner_z17": inner_map,
    "closeup_z19": closeup_map
}
with open(os.path.join(SCRATCH_DIR, "unified_kitroni_3d_map.json"), "w", encoding="utf-8") as f:
    json.dump(unified_3d, f)
print("Saved unified_kitroni_3d_map.json!")

# Load the 28 POIs from Pines 48 and recalculate exact distances from Kitroni 37-39
with open(os.path.join(PINES_SCRATCH, "spatial_map_data.json"), "r", encoding="utf-8") as f:
    pines_spatial = json.load(f)

cx16, cy16 = latlon_to_tile_xy(CENTER_LAT, CENTER_LON, 16)
cx15, cy15 = latlon_to_tile_xy(CENTER_LAT, CENTER_LON, 15)

kitroni_pois = []
for p in pines_spatial["pois"]:
    lat, lon = p["lat"], p["lon"]
    dist_m = int(round(haversine_m(CENTER_LAT, CENTER_LON, lat, lon)))
    walk_min = max(1, int(round(dist_m / 75.0)))
    drive_min = max(1, int(round(dist_m / 380.0)))
    tx16, ty16 = latlon_to_tile_xy(lat, lon, 16)
    tx15, ty15 = latlon_to_tile_xy(lat, lon, 15)
    x_z16 = 640.0 + (tx16 - cx16) * 256.0
    y_z16 = 512.0 + (ty16 - cy16) * 256.0
    x_z15 = 640.0 + (tx15 - cx15) * 256.0
    y_z15 = 512.0 + (ty15 - cy15) * 256.0
    show_z16 = (40 <= x_z16 <= 1240 and 40 <= y_z16 <= 984)
    np = dict(p)
    np["dist_m"] = dist_m
    np["walk_min"] = walk_min
    np["drive_min"] = drive_min
    np["x_z16"] = round(x_z16, 1)
    np["y_z16"] = round(y_z16, 1)
    np["x_z15"] = round(x_z15, 1)
    np["y_z15"] = round(y_z15, 1)
    np["show_z16"] = show_z16
    kitroni_pois.append(np)

# Sort within categories or keep ID order 1..28
z16_hyb, mpp16 = fetch_rect_map_2d(16, 1280, 1024, "y", 82)
z16_rd, _ = fetch_rect_map_2d(16, 1280, 1024, "m", 82)
z15_hyb, mpp15 = fetch_rect_map_2d(15, 1280, 1024, "y", 82)
z15_rd, _ = fetch_rect_map_2d(15, 1280, 1024, "m", 82)

kitroni_spatial_data = {
    "project": {
        "name": "קיטרוני 37–39, פתח תקווה",
        "lat": CENTER_LAT,
        "lon": CENTER_LON
    },
    "z16": {"cx": 640, "cy": 512, "mpp": round(mpp16, 4), "hybrid": z16_hyb, "roadmap": z16_rd},
    "z15": {"cx": 640, "cy": 512, "mpp": round(mpp15, 4), "hybrid": z15_hyb, "roadmap": z15_rd},
    "pois": kitroni_pois
}

with open(os.path.join(SCRATCH_DIR, "kitroni_spatial_map_data.json"), "w", encoding="utf-8") as f:
    json.dump(kitroni_spatial_data, f, ensure_ascii=False)
print("Saved kitroni_spatial_map_data.json with", len(kitroni_pois), "POIs!")

# Also generate kitroni37_39_spatial_map.html by adapting Pines 48's interactive spatial HTML
with open(os.path.join(PINES_SCRATCH, "build_interactive_spatial_html.py"), "r", encoding="utf-8") as f:
    sp_script = f.read()

start_idx = sp_script.find('html_template = """') + len('html_template = """')
end_idx = sp_script.rfind('"""')
sp_html_tmpl = sp_script[start_idx:end_idx]

sp_html_out = (
    sp_html_tmpl
    .replace("פינס 48 פינת הבעש\"ט, פתח תקווה", "קיטרוני 37–39, פתח תקווה")
    .replace("פינס 48, פתח תקווה", "קיטרוני 37–39, פתח תקווה")
    .replace("מפינס 48", "מקיטרוני 37–39")
    .replace(">48<", ">K37<")
    .replace("32.08115°N, 34.89398°E", f"{CENTER_LAT:.5f}°N, {CENTER_LON:.5f}°E")
    .replace("32.08115,34.89398", f"{CENTER_LAT:.5f},{CENTER_LON:.5f}")
    .replace("__DATA_JSON__", json.dumps(kitroni_spatial_data, ensure_ascii=False))
)

for out_p in [
    os.path.join(WORKSPACE, "kitroni37_39_spatial_map.html"),
    os.path.join(ARTIFACT_DIR, "kitroni37_39_spatial_map.html")
]:
    with open(out_p, "w", encoding="utf-8") as f:
        f.write(sp_html_out)
    print("Wrote 2D GIS Map:", out_p, "Size:", os.path.getsize(out_p))
