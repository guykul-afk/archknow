import urllib.request
import math
import io
import base64
import json
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

CENTER_LAT = 32.081015
CENTER_LON = 34.893785
R_MERC = 6378137.0
COS_LAT0 = math.cos(math.radians(CENTER_LAT))

def latlon_to_tile_xy(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    xtile = (lon + 180.0) / 360.0 * n
    ytile = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
    return xtile, ytile

def fetch_symmetric_map(zoom, grid_size, half_px, out_px, quality=86):
    cx, cy = latlon_to_tile_xy(CENTER_LAT, CENTER_LON, zoom)
    start_x = int(math.floor(cx - grid_size / 2.0))
    start_y = int(math.floor(cy - grid_size / 2.0))

    canvas = Image.new('RGB', (grid_size * 256, grid_size * 256))

    def fetch_one(args):
        dx, dy = args
        tx = start_x + dx
        ty = start_y + dy
        url = f"https://mt1.google.com/vt/lyrs=y&x={tx}&y={ty}&z={zoom}&hl=iw"
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

    # Exact Web Mercator ground meters per raw tile pixel at CENTER_LAT
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

# 1. Outer Regional Map (Zoom 15): 8x8 tiles (2048px), cropped to 1792x1792 raw px -> 7,253.7m x 7,253.7m (7.25 km x 7.25 km!)
outer_map = fetch_symmetric_map(zoom=15, grid_size=8, half_px=896, out_px=2048, quality=84)
print(f"Outer Z15 Map: {outer_map['world_span_m']:.1f}m x {outer_map['world_span_m']:.1f}m, size={len(outer_map['data_uri']):,} bytes")

# 2. Mid Neighborhood Map (Zoom 17): 8x8 tiles (2048px), cropped to 1600x1600 raw px -> 1,619.1m x 1,619.1m (1.62 km x 1.62 km!)
inner_map = fetch_symmetric_map(zoom=17, grid_size=8, half_px=800, out_px=2048, quality=85)
print(f"Inner Z17 Map: {inner_map['world_span_m']:.1f}m x {inner_map['world_span_m']:.1f}m, size={len(inner_map['data_uri']):,} bytes")

# 3. Ultra-Sharp Close-Up Intersection Map (Zoom 19): 6x6 tiles (1536px), cropped to 1024x1024 raw px -> 259.1m x 259.1m at 0.25m/px!
closeup_map = fetch_symmetric_map(zoom=19, grid_size=6, half_px=512, out_px=1536, quality=88)
print(f"Close-up Z19 Map: {closeup_map['world_span_m']:.1f}m x {closeup_map['world_span_m']:.1f}m, size={len(closeup_map['data_uri']):,} bytes")

out_info = {
    "center_lat": CENTER_LAT,
    "center_lon": CENTER_LON,
    "outer_z15": outer_map,
    "inner_z17": inner_map,
    "closeup_z19": closeup_map
}

with open('C:/Users/User/.gemini/antigravity/brain/60b6f7e6-94a5-48b9-b12c-1728c4428342/scratch/unified_3d_map.json', 'w', encoding='utf-8') as f:
    json.dump(out_info, f)
print("Saved multi-scale Z15 + Z17 + Z19 Google Maps Hybrid textures to unified_3d_map.json!")
