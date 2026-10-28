import urllib.request
import math
import io
import base64
import json
import os
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

SCRATCH_DIR = r"C:\Users\User\.gemini\antigravity\scratch\kkl10"
GDRIVE_DIR = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\קקל 10 פתח תקווה"

# Exact geometric center of the KKL 10 lot (רחוב קרן קימת לישראל 10, פתח תקווה - Gush 6374 Helka 112)
CENTER_LAT = 32.078730
CENTER_LON = 34.882516
STREET_ALIGN_DEG = -16.5  # Aligns Keren Kayemet LeYisrael street & lot orthogonally with the BIM model axes
R_MERC = 6378137.0
COS_LAT0 = math.cos(math.radians(CENTER_LAT))

def latlon_to_tile_xy(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = (lon + 180.0) / 360.0 * n
    ytile = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
    return xtile, ytile

def fetch_symmetric_map(zoom, grid_size, half_px, out_px, lyrs="y", quality=82):
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
    # Rotate around the exact lot center by -16.5 deg so KKL street & lot align 100% with the 3D BIM model
    canvas = canvas.rotate(STREET_ALIGN_DEG, resample=Image.Resampling.BICUBIC, center=(px_cx, px_cy))
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

print("Fetching 3D Triple-Resolution Maps (Z15, Z17, Z19) centered on KKL 10, Petah Tikva...")
outer_map = fetch_symmetric_map(zoom=15, grid_size=8, half_px=896, out_px=1536, quality=80)
inner_map = fetch_symmetric_map(zoom=17, grid_size=8, half_px=800, out_px=1536, quality=82)
closeup_map = fetch_symmetric_map(zoom=19, grid_size=6, half_px=512, out_px=1280, quality=85)

unified_3d = {
    "center_lat": CENTER_LAT,
    "center_lon": CENTER_LON,
    "outer_z15": outer_map,
    "inner_z17": inner_map,
    "closeup_z19": closeup_map
}

for root in [SCRATCH_DIR, GDRIVE_DIR]:
    with open(os.path.join(root, "data", "unified_3d_map.json"), "w", encoding="utf-8") as f:
        json.dump(unified_3d, f)

print("Saved unified_3d_map.json!")
print("outer_z15 span:", outer_map["world_span_m"], "m, uri len:", len(outer_map["data_uri"]))
print("inner_z17 span:", inner_map["world_span_m"], "m, uri len:", len(inner_map["data_uri"]))
print("closeup_z19 span:", closeup_map["world_span_m"], "m, uri len:", len(closeup_map["data_uri"]))
