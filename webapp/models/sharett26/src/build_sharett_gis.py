import urllib.request
import math
import base64
import json
import os
import pymupdf as fitz
from concurrent.futures import ThreadPoolExecutor

WORKSPACE = r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה"
DATA_DIR = os.path.join(WORKSPACE, "data")
os.makedirs(DATA_DIR, exist_ok=True)

SHARED_ENGINE = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\_shared_engine"
HAFETZ_DATA = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\חפץ חיים 44 פתח תקווה\data\hafetz44_spatial_map_data.json"
SHARED_SPATIAL = os.path.join(SHARED_ENGINE, "spatial_map_data.json")
KITRONI_DATA = HAFETZ_DATA if os.path.exists(HAFETZ_DATA) else SHARED_SPATIAL

# Verified ITM (E=188030.3, N=666175.8) -> WGS84 coordinates for Moshe Sharett 26-28, Petah Tikva
CENTER_LAT = 32.088485
CENTER_LON = 34.871580
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

def stitch_and_crop_fitz(zoom, grid_size, w_px, h_px, lyrs="y", quality=84):
    cx, cy = latlon_to_tile_xy(CENTER_LAT, CENTER_LON, zoom)
    start_x = int(math.floor(cx - grid_size / 2.0))
    start_y = int(math.floor(cy - grid_size / 2.0))

    canvas = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, grid_size * 256, grid_size * 256), False)
    canvas.clear_with(240)

    def fetch_one(args):
        dx, dy = args
        tx = start_x + dx
        ty = start_y + dy
        url = f"https://mt1.google.com/vt/lyrs={lyrs}&x={tx}&y={ty}&z={zoom}&hl=iw"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=12) as r:
                raw = r.read()
                return dx, dy, raw
        except Exception as e:
            print(f"Error z={zoom} tile ({dx},{dy}):", e)
            return dx, dy, None

    coords = [(dx, dy) for dx in range(grid_size) for dy in range(grid_size)]
    with ThreadPoolExecutor(max_workers=16) as ex:
        for dx, dy, raw in ex.map(fetch_one, coords):
            if raw:
                tp = fitz.Pixmap(raw)
                if tp.n != 3 or tp.alpha:
                    tp = fitz.Pixmap(fitz.csRGB, tp)
                tp.set_origin(dx * 256, dy * 256)
                canvas.copy(tp, tp.irect)

    px_cx = (cx - start_x) * 256.0
    px_cy = (cy - start_y) * 256.0
    left = int(round(px_cx - w_px / 2.0))
    top = int(round(px_cy - h_px / 2.0))
    irect = fitz.IRect(left, top, left + w_px, top + h_px)
    cropped = fitz.Pixmap(fitz.csRGB, irect, False)
    cropped.copy(canvas, irect)
    cropped.set_origin(0, 0)

    mpp = (2.0 * math.pi * R_MERC * COS_LAT0) / (256.0 * (2 ** zoom))
    jpg_bytes = cropped.tobytes("jpeg", jpg_quality=quality)
    b64_uri = "data:image/jpeg;base64," + base64.b64encode(jpg_bytes).decode('ascii')
    return b64_uri, mpp

def fetch_symmetric_map(zoom, grid_size, half_px, quality=84):
    size_px = half_px * 2
    b64_uri, mpp = stitch_and_crop_fitz(zoom, grid_size, size_px, size_px, "y", quality)
    return {
        "zoom": zoom,
        "world_span_m": round(size_px * mpp, 3),
        "data_uri": b64_uri
    }

u3d_path = os.path.join(DATA_DIR, "unified_sharett_3d_map.json")
if not os.path.exists(u3d_path):
    print("Fetching 3D Triple-Resolution Maps (Z15, Z17, Z19) centered on Moshe Sharett 26-28, Petah Tikva...")
    outer_map = fetch_symmetric_map(zoom=15, grid_size=8, half_px=800, quality=80)
    inner_map = fetch_symmetric_map(zoom=17, grid_size=8, half_px=750, quality=82)
    closeup_map = fetch_symmetric_map(zoom=19, grid_size=6, half_px=512, quality=85)

    unified_3d = {
        "center_lat": CENTER_LAT,
        "center_lon": CENTER_LON,
        "outer_z15": outer_map,
        "inner_z17": inner_map,
        "closeup_z19": closeup_map
    }
    with open(u3d_path, "w", encoding="utf-8") as f:
        json.dump(unified_3d, f)
print(f"Verified {u3d_path} ({os.path.getsize(u3d_path)/(1024*1024):.2f} MB)")

# Load base POIs and recalculate exact distances from Moshe Sharett 26-28
with open(KITRONI_DATA, "r", encoding="utf-8") as f:
    kitroni_spatial = json.load(f)

cx16, cy16 = latlon_to_tile_xy(CENTER_LAT, CENTER_LON, 16)
cx15, cy15 = latlon_to_tile_xy(CENTER_LAT, CENTER_LON, 15)

sharett_pois = []
for p in kitroni_spatial["pois"]:
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
    sharett_pois.append(np)

print("Fetching 2D Interactive Spatial Maps (Z16 & Z15 Hybrid + Roadmap)...")
z16_hyb, mpp16 = stitch_and_crop_fitz(16, 8, 1280, 1024, "y", 82)
z16_rd, _ = stitch_and_crop_fitz(16, 8, 1280, 1024, "m", 82)
z15_hyb, mpp15 = stitch_and_crop_fitz(15, 8, 1280, 1024, "y", 82)
z15_rd, _ = stitch_and_crop_fitz(15, 8, 1280, 1024, "m", 82)

sharett_spatial_data = {
    "project": {
        "name": "משה שרת 26–28, פתח תקווה",
        "lat": CENTER_LAT,
        "lon": CENTER_LON
    },
    "z16": {"cx": 640, "cy": 512, "mpp": round(mpp16, 4), "hybrid": z16_hyb, "roadmap": z16_rd},
    "z15": {"cx": 640, "cy": 512, "mpp": round(mpp15, 4), "hybrid": z15_hyb, "roadmap": z15_rd},
    "pois": sharett_pois
}

sp_json_path = os.path.join(DATA_DIR, "sharett_spatial_map_data.json")
with open(sp_json_path, "w", encoding="utf-8") as f:
    json.dump(sharett_spatial_data, f, ensure_ascii=False)
print(f"Saved {sp_json_path} with {len(sharett_pois)} POIs!")

with open(os.path.join(SHARED_ENGINE, "build_interactive_spatial_html.py"), "r", encoding="utf-8") as f:
    sp_script = f.read()

start_idx = sp_script.find('html_template = """') + len('html_template = """')
end_idx = sp_script.rfind('"""')
sp_html_tmpl = sp_script[start_idx:end_idx]

sp_html_out = (
    sp_html_tmpl
    .replace("פינס 48 פינת הבעש\"ט, פתח תקווה", "משה שרת 26–28, פתח תקווה")
    .replace("פינס 48, פתח תקווה", "משה שרת 26–28, פתח תקווה")
    .replace("מפינס 48", "ממשה שרת 26–28")
    .replace(">48<", ">26<")
    .replace("32.08115°N, 34.89398°E", f"{CENTER_LAT:.5f}°N, {CENTER_LON:.5f}°E")
    .replace("32.08115,34.89398", f"{CENTER_LAT:.5f},{CENTER_LON:.5f}")
    .replace("__DATA_JSON__", json.dumps(sharett_spatial_data, ensure_ascii=False))
)

out_html = os.path.join(WORKSPACE, "sharett26_28_spatial_map.html")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(sp_html_out)
print(f"Wrote 2D GIS Map: {out_html} ({os.path.getsize(out_html)/(1024*1024):.2f} MB)")
