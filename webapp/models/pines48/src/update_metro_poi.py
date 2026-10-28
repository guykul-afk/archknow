import json
import math

SPATIAL_DATA_PATH = r"C:\Users\User\.gemini\antigravity\brain\60b6f7e6-94a5-48b9-b12c-1728c4428342\scratch\spatial_map_data.json"

with open(SPATIAL_DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

proj_lat = data["proj_lat"]
proj_lon = data["proj_lon"]

# Remove any existing metro entry if re-running
pois = [p for p in data["pois"] if "מטרו" not in p["name"]]

# Exact coordinates of future Metro M2 Station at Petah Tikva Municipality (Haim Ozer / HaAliya HaShniya 1)
metro_lat = 32.08714
metro_lon = 34.88783

R_EARTH = 6371000.0
dlat = math.radians(metro_lat - proj_lat)
dlon = math.radians(metro_lon - proj_lon)
a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(proj_lat)) * math.cos(math.radians(metro_lat)) * math.sin(dlon / 2) ** 2
dist_m = int(round(2 * R_EARTH * math.asin(math.sqrt(a))))

# Compute pixel positions on the 2D z16 and z15 maps (same Web Mercator formula used in spatial_map_data.json)
R_MERC = 6378137.0
cos_lat0 = math.cos(math.radians(proj_lat))
dx_m = (metro_lon - proj_lon) * (math.pi / 180.0) * R_MERC * cos_lat0
dy_m = (metro_lat - proj_lat) * (math.pi / 180.0) * R_MERC  # North is +dy_m, screen y is -dy_m

cx16, cy16, mpp16 = data["z16"]["cx"], data["z16"]["cy"], data["z16"]["mpp"]
cx15, cy15, mpp15 = data["z15"]["cx"], data["z15"]["cy"], data["z15"]["mpp"]

x16 = round(cx16 + dx_m / mpp16, 1)
y16 = round(cy16 - dy_m / mpp16, 1)
x15 = round(cx15 + dx_m / mpp15, 1)
y15 = round(cy15 - dy_m / mpp15, 1)

metro_poi = {
    "id": 14,
    "cat": "transport",
    "name": "תחנת מטרו עיריית פ\"ת (קו M2 העתידי)",
    "sub": "תת\"ל 102 / תמ\"א 70 (רח' חיים עוזר / העלייה השנייה) — קישור מהיר לגוש דן ות\"א",
    "lat": metro_lat,
    "lon": metro_lon,
    "dist_m": dist_m,
    "walk_min": 11,
    "drive_min": 3,
    "show_z16": True,
    "x16": x16,
    "y16": y16,
    "x15": x15,
    "y15": y15
}

# Insert into transport category ordered by distance
new_pois = []
inserted = False
for p in pois:
    if p["cat"] == "transport" and p["dist_m"] > dist_m and not inserted:
        new_pois.append(metro_poi)
        inserted = True
    new_pois.append(p)
if not inserted:
    new_pois.append(metro_poi)

# Re-number sequential IDs 1..28
for idx, p in enumerate(new_pois, start=1):
    p["id"] = idx

data["pois"] = new_pois

with open(SPATIAL_DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

print(f"Updated spatial_map_data.json with {len(new_pois)} POIs. Metro station ID={metro_poi['id']}, dist={dist_m}m, x16={x16}, y16={y16}")
