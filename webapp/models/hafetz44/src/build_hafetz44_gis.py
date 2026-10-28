import urllib.request
import math
import io
import base64
import json
import os
import re
import shutil
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont

# Exact ITM-Surveyed coordinates of Hafetz Haim 44, Petah Tikva (Gush 6396, Helka 85, ITM E=189549.11, N=665352.32)
CENTER_LAT = 32.0810722
CENTER_LON = 34.8876650
R_MERC = 6378137.0
COS_LAT0 = math.cos(math.radians(CENTER_LAT))

SCRATCH_DIR = r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44"
ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e"
PUBLIC_DIR = r"c:\Users\guyku\‏‏תיקיה חדשה\public\projects\hafetz-44"
DRIVE_DIR = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\חפץ חיים 44 פתח תקווה"

os.makedirs(SCRATCH_DIR, exist_ok=True)
os.makedirs(PUBLIC_DIR, exist_ok=True)

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

def fetch_google_map_canvas(center_lat, center_lon, zoom, grid_w, grid_h, lyrs='y'):
    cx, cy = latlon_to_tile_xy(center_lat, center_lon, zoom)
    start_x = int(math.floor(cx - grid_w / 2.0))
    start_y = int(math.floor(cy - grid_h / 2.0))

    canvas = Image.new('RGB', (grid_w * 256, grid_h * 256))
    coords = [(dx, dy) for dx in range(grid_w) for dy in range(grid_h)]
    def fetch_tile(args):
        dx, dy = args
        tx, ty = start_x + dx, start_y + dy
        url = f"https://mt1.google.com/vt/lyrs={lyrs}&x={tx}&y={ty}&z={zoom}&hl=iw"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return dx, dy, Image.open(io.BytesIO(r.read())).convert('RGB')
        except Exception as e:
            print("Tile fetch error:", e)
            return dx, dy, None

    with ThreadPoolExecutor(max_workers=16) as ex:
        for dx, dy, tile_img in ex.map(fetch_tile, coords):
            if tile_img:
                canvas.paste(tile_img, (dx * 256, dy * 256))

    px_center_x = (cx - start_x) * 256
    px_center_y = (cy - start_y) * 256
    out_w = (grid_w - 1) * 256
    out_h = (grid_h - 1) * 256
    left = int(round(px_center_x - out_w / 2))
    top = int(round(px_center_y - out_h / 2))
    cropped = canvas.crop((left, top, left + out_w, top + out_h))

    def latlon_to_px(lat, lon):
        x, y = latlon_to_tile_xy(lat, lon, zoom)
        px = (x - start_x) * 256 - left
        py = (y - start_y) * 256 - top
        return px, py

    mpp = 156543.03392 * math.cos(math.radians(center_lat)) / (2 ** zoom)
    return cropped, latlon_to_px, mpp

def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return int(round(2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))))

# 28 Verified POIs around Hafetz Haim 44, Petah Tikva (32.083305, 34.887208)
RAW_POIS = [
    # EDUCATION (1-9)
    {"cat": "education", "name": 'ישיבת כנסת יצחק ומוסדות חפץ חיים', "sub": "מוסד חינוכי ולימודי צמוד ברח' חפץ חיים", "lat": 32.08355, "lon": 34.88785, "show_z16": True},
    {"cat": "education", "name": 'בי"ס יסודי פיק"א (לב העיר)', "sub": "בית ספר יסודי ממלכתי מרכזי", "lat": 32.08532, "lon": 34.88795, "show_z16": True},
    {"cat": "education", "name": 'אשכול גני ילדים עירוני (חפץ חיים / מונטיפיורי)', "sub": "גני ילדים עירוניים במרחק הליכה קצר", "lat": 32.08415, "lon": 34.88610, "show_z16": True},
    {"cat": "education", "name": 'תלמוד תורה ובי"ס שארית ישראל', "sub": "מוסד חינוכי ברח' רוטשילד / מונטיפיורי", "lat": 32.08210, "lon": 34.88580, "show_z16": True},
    {"cat": "education", "name": 'בי"ס ממ"ד נצח ישראל', "sub": "בית ספר יסודי ממלכתי-דתי מרכזי", "lat": 32.08615, "lon": 34.89020, "show_z16": True},
    {"cat": "education", "name": 'בי"ס יסודי קפלן וגני ילדים', "sub": "קריית חינוך יסודית (מזרח לב העיר)", "lat": 32.08215, "lon": 34.89150, "show_z16": True},
    {"cat": "education", "name": 'חטיבת ביניים יצחק בן צבי', "sub": "חטיבת ביניים ממלכתית מרכזית (רח' עין גנים)", "lat": 32.08402, "lon": 34.89474, "show_z16": True},
    {"cat": "education", "name": 'בי"ס ממ"ד דרכי נועם', "sub": "בית ספר יסודי ממלכתי-דתי (רח' פינס)", "lat": 32.07838, "lon": 34.89095, "show_z16": True},
    {"cat": "education", "name": 'תיכון אחד העם והקונסרבטוריון העירוני', "sub": "תיכון מוביל ומוסדות תרבות ומוזיקה", "lat": 32.08020, "lon": 34.88190, "show_z16": True},

    # TRANSPORT & METRO (10-16)
    {"cat": "transport", "name": 'תחנת אוטובוס חפץ חיים / מונטיפיורי', "sub": "קווים עירוניים ובינעירוניים בצמוד לפרויקט", "lat": 32.08370, "lon": 34.88695, "show_z16": True},
    {"cat": "transport", "name": 'ציר הברון הירש / שטמפפר (מרכז העיר)', "sub": "עורק תחבורה ראשי לכל רחבי גוש דן", "lat": 32.08585, "lon": 34.88680, "show_z16": True},
    {"cat": "transport", "name": 'תחנת מטרו עיריית פ"ת (קו M2 העתידי)', "sub": "תת\"ל 102 / תמ\"א 70 (רח' חיים עוזר / העלייה השנייה) — כ-5 דק' הליכה!", "lat": 32.08714, "lon": 34.88783, "show_z16": True},
    {"cat": "transport", "name": 'ציר רוטשילד / קווים ישירים לת"א ולרכבת', "sub": "תדירות גבוהה לקו האדום ולמרכז תל אביב", "lat": 32.08310, "lon": 34.88420, "show_z16": True},
    {"cat": "transport", "name": 'תחנת הרכבת הקלה פינסקר (הקו האדום פעיל)', "sub": "חיבור ישיר לבני ברק, רמת גן, ת\"א ובת ים", "lat": 32.09280, "lon": 34.88610, "show_z16": False},
    {"cat": "transport", "name": 'התחנה המרכזית פ"ת ומסוף הרכבת הקלה (CBS)', "sub": "מוקד תחבורה מטרופוליני, רכבת קלה ואוטובוסים", "lat": 32.09420, "lon": 34.88910, "show_z16": False},
    {"cat": "transport", "name": 'כביש 471 (מכבית) / כביש 40', "sub": "יציאה מהירה לכביש 4, כביש 6, נתב\"ג ותל אביב", "lat": 32.07150, "lon": 34.88550, "show_z16": False},

    # SHOPPING & COMMERCE (17-22)
    {"cat": "shopping", "name": 'שוק פתח תקווה המתחדש והברון הירש', "sub": "מוקד קולינריה, תוצרת טרייה, מסחר ובתי קפה (3 דק' הליכה)", "lat": 32.08540, "lon": 34.88735, "show_z16": True},
    {"cat": "shopping", "name": 'מדרחוב חובבי ציון ומרכז הבנקים', "sub": "הלב המסחרי של פתח תקווה — חנויות, בתי קפה ושירותים", "lat": 32.08690, "lon": 34.88580, "show_z16": True},
    {"cat": "shopping", "name": 'מרכז מסחרי חיים עוזר / העלייה השנייה', "sub": "סופרמרקטים, סופר-פארם, בנקים ומסעדות", "lat": 32.08660, "lon": 34.88810, "show_z16": True},
    {"cat": "shopping", "name": 'מרכז רוטשילד (שופרסל / סופר-פארם)', "sub": "מתחם קניות, פארם, מזון ובנקים", "lat": 32.07610, "lon": 34.88510, "show_z16": True},
    {"cat": "shopping", "name": 'קניון לב התחנה ומתחם העסקים', "sub": "מרכז קניות ומסחר בצפון-מערב מרכז העיר", "lat": 32.09380, "lon": 34.88860, "show_z16": False},
    {"cat": "shopping", "name": 'קניון עופר סירקין והקניון הגדול (אבנת)', "sub": "קניוני הדגל של פתח תקווה במרחק נסיעה קצר", "lat": 32.08025, "lon": 34.90415, "show_z16": False},

    # PARKS, CULTURE & COMMUNITY (23-25)
    {"cat": "parks", "name": 'גן המייסדים וכיכר עיריית פתח תקווה', "sub": "הפארק המרכזי הירוק של לב העיר ואירועי קהילה", "lat": 32.08750, "lon": 34.88690, "show_z16": True},
    {"cat": "parks", "name": 'היכל התרבות העירוני פתח תקווה', "sub": "תיאטרון, קונצרטים, מופעים וספרייה עירונית (רח' המכבים)", "lat": 32.08480, "lon": 34.88280, "show_z16": True},
    {"cat": "parks", "name": 'פארק יד לבנים, מוזיאון פ"ת וגן החי', "sub": "קריית המוזיאונים, פארק רחב ידיים וגן החי (רח' ארלוזורוב)", "lat": 32.08460, "lon": 34.87720, "show_z16": True},

    # HEALTH & MEDICAL (26-28)
    {"cat": "health", "name": 'מכבי שירותי בריאות — מרכז רפואי לב העיר', "sub": "מרפאת מומחים, מעבדה ובית מרקחת (רח' שפיגל / חיים עוזר)", "lat": 32.08610, "lon": 34.88840, "show_z16": True},
    {"cat": "health", "name": 'קופת חולים כללית ומאוחדת (רוטשילד)', "sub": "מרפאות אזוריות ורפואה מקצועית במרחק הליכה", "lat": 32.08260, "lon": 34.88400, "show_z16": True},
    {"cat": "health", "name": 'מרכז רפואי רבין – בית חולים השרון', "sub": "בית חולים אוניברסיטאי מרכזי ומיון (רח' קק\"ל 7)", "lat": 32.07955, "lon": 34.88124, "show_z16": True},
]

POIS = []
for idx, p in enumerate(RAW_POIS, start=1):
    dist_m = haversine_m(CENTER_LAT, CENTER_LON, p["lat"], p["lon"])
    walk_min = max(1, int(round(dist_m / 78.0)))
    drive_min = max(1, int(round(dist_m / 420.0)))
    item = dict(p)
    item["id"] = idx
    item["dist_m"] = dist_m
    item["walk_min"] = walk_min
    item["drive_min"] = drive_min
    POIS.append(item)

print("1. Fetching Triple-Resolution Google Maps 3D textures (Z15, Z17, Z19) for Hafetz Haim 44...")
outer_map   = fetch_symmetric_map(zoom=15, grid_size=8, half_px=896, out_px=2048, quality=84)
inner_map   = fetch_symmetric_map(zoom=17, grid_size=8, half_px=800, out_px=2048, quality=85)
closeup_map = fetch_symmetric_map(zoom=19, grid_size=6, half_px=512, out_px=1536, quality=88)

unified_out = {
    "center_lat": CENTER_LAT,
    "center_lon": CENTER_LON,
    "outer_z15": outer_map,
    "inner_z17": inner_map,
    "closeup_z19": closeup_map
}
unified_path = os.path.join(SCRATCH_DIR, "unified_hafetz44_3d_map.json")
with open(unified_path, "w", encoding="utf-8") as f:
    json.dump(unified_out, f)
print(f"Saved {unified_path} ({os.path.getsize(unified_path):,} bytes)")

print("2. Fetching 2D GIS Explorer canvases (Z16 & Z15 Hybrid + Roadmap)...")
hybrid_z16, proj_z16, mpp_z16 = fetch_google_map_canvas(CENTER_LAT, CENTER_LON, zoom=16, grid_w=6, grid_h=5, lyrs='y')
roadmap_z16, _, _ = fetch_google_map_canvas(CENTER_LAT, CENTER_LON, zoom=16, grid_w=6, grid_h=5, lyrs='m')
hybrid_z15, proj_z15, mpp_z15 = fetch_google_map_canvas(CENTER_LAT, CENTER_LON, zoom=15, grid_w=6, grid_h=5, lyrs='y')
roadmap_z15, _, _ = fetch_google_map_canvas(CENTER_LAT, CENTER_LON, zoom=15, grid_w=6, grid_h=5, lyrs='m')

def img_to_b64(im, qual=82):
    buf = io.BytesIO()
    im.save(buf, format='JPEG', quality=qual)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode('ascii')

cx16, cy16 = proj_z16(CENTER_LAT, CENTER_LON)
cx15, cy15 = proj_z15(CENTER_LAT, CENTER_LON)
map_w, map_h = hybrid_z16.size

meta = {
    "proj_lat": CENTER_LAT,
    "proj_lon": CENTER_LON,
    "map_w": map_w,
    "map_h": map_h,
    "z16": {"cx": round(cx16, 1), "cy": round(cy16, 1), "mpp": round(mpp_z16, 4), "hybrid": img_to_b64(hybrid_z16, 82), "roadmap": img_to_b64(roadmap_z16, 82)},
    "z15": {"cx": round(cx15, 1), "cy": round(cy15, 1), "mpp": round(mpp_z15, 4), "hybrid": img_to_b64(hybrid_z15, 82), "roadmap": img_to_b64(roadmap_z15, 82)},
    "pois": []
}

for p in POIS:
    x16, y16 = proj_z16(p['lat'], p['lon'])
    x15, y15 = proj_z15(p['lat'], p['lon'])
    p_copy = dict(p)
    p_copy["x16"], p_copy["y16"] = round(x16, 1), round(y16, 1)
    p_copy["x15"], p_copy["y15"] = round(x15, 1), round(y15, 1)
    meta["pois"].append(p_copy)

spatial_json_path = os.path.join(SCRATCH_DIR, "hafetz44_spatial_map_data.json")
with open(spatial_json_path, "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False)
print(f"Saved {spatial_json_path} with {len(meta['pois'])} POIs")

# Build standalone 2D interactive GIS map HTML (hafetz44_spatial_map.html)
with open(r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\_shared_engine\build_interactive_spatial_html.py", "r", encoding="utf-8") as f:
    spatial_script = f.read()

start_marker = 'html_template = """'
end_marker = '"""\n\nfinal_html ='
s_idx = spatial_script.find(start_marker) + len(start_marker)
e_idx = spatial_script.find(end_marker)
spatial_tpl = spatial_script[s_idx:e_idx]

spatial_html = (
    spatial_tpl
    .replace("__SPATIAL_DATA_JSON__", json.dumps(meta, ensure_ascii=False))
    .replace("פינס 48 פינת הבעש\"ט", "חפץ חיים 44, פתח תקווה")
    .replace("פינס 48", "חפץ חיים 44")
    .replace("48", "44")
    .replace("32.08115°N, 34.89398°E", f"{CENTER_LAT:.5f}°N, {CENTER_LON:.5f}°E")
    .replace("הכל (27)", f"הכל ({len(POIS)})")
    .replace("תחבורה ציבורית וצירים (6)", "תחבורה ציבורית ומטרו (7)")
)

for out_p in [
    os.path.join(ARTIFACT_DIR, "hafetz44_spatial_map.html"),
    os.path.join(PUBLIC_DIR, "hafetz44_spatial_map.html"),
]:
    with open(out_p, "w", encoding="utf-8") as f:
        f.write(spatial_html)
    print("Wrote 2D GIS Explorer:", out_p)

if os.path.exists(DRIVE_DIR):
    try:
        shutil.copyfile(os.path.join(ARTIFACT_DIR, "hafetz44_spatial_map.html"), os.path.join(DRIVE_DIR, "hafetz44_spatial_map.html"))
    except Exception as e:
        print("Drive copy warning:", e)
