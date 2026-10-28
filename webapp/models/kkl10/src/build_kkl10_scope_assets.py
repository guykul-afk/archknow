import json
import math
import os

BRAIN_DIR = r"C:\Users\User\.gemini\antigravity\brain\17cdeb22-38a8-4e04-b15d-67ce64232225"
SCRATCH_DIR = r"C:\Users\User\.gemini\antigravity\scratch\kkl10"
GDRIVE_DIR = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\קקל 10 פתח תקווה"
KITRONI_DATA = r"G:\Shared drives\פרויקטים שוטפים\פרויקטים בביצוע\קטרוני 37-39\מודל\data\spatial_map_data.json"

for d in [SCRATCH_DIR, os.path.join(SCRATCH_DIR, "data"), os.path.join(SCRATCH_DIR, "docs"),
          GDRIVE_DIR, os.path.join(GDRIVE_DIR, "data"), os.path.join(GDRIVE_DIR, "docs")]:
    os.makedirs(d, exist_ok=True)

# KKL 10, Petah Tikva exact lot center coordinates (רחוב קרן קימת לישראל 10, פתח תקווה - גוש 6374 חלקה 112)
KKL10_LAT = 32.078730
KKL10_LON = 34.882516
STREET_THETA_RAD = math.radians(16.5)

def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    return int(round(2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))))

def latlon_to_meters(lat, lon, ref_lat=KKL10_LAT, ref_lon=KKL10_LON):
    raw_north_m = (lat - ref_lat) * 111132.0
    raw_east_m = (lon - ref_lon) * 111320.0 * math.cos(math.radians(ref_lat))
    east_m = raw_east_m * math.cos(STREET_THETA_RAD) + raw_north_m * math.sin(STREET_THETA_RAD)
    north_m = -raw_east_m * math.sin(STREET_THETA_RAD) + raw_north_m * math.cos(STREET_THETA_RAD)
    return round(east_m, 1), round(north_m, 1)

with open(KITRONI_DATA, "r", encoding="utf-8") as f:
    kitroni_gis = json.load(f)

CAT_HE_MAP = {
    "education": "חינוך וגני ילדים",
    "transit": "תחבורה, רק\"ל ומטרו",
    "transport": "תחבורה, רק\"ל ומטרו",
    "shopping": "קניות, מסחר ופנאי",
    "commercial": "קניות, מסחר ופנאי",
    "parks": "גינות ופארקים",
    "park": "גינות ופארקים",
    "health": "בריאות, קהילה ודת",
    "community": "בריאות, קהילה ודת",
    "culture": "תרבות, קהילה ודת",
    "synagogue": "בתי כנסת וקהילה"
}

CAT_COLOR_MAP = {
    "education": "#3b82f6",
    "transit": "#a855f7",
    "transport": "#a855f7",
    "shopping": "#f59e0b",
    "commercial": "#f59e0b",
    "parks": "#10b981",
    "park": "#10b981",
    "health": "#ef4444",
    "community": "#ec4899",
    "culture": "#ec4899",
    "synagogue": "#06b6d4"
}

pois = []
for p in kitroni_gis.get("pois", []):
    plat = p["lat"]
    plon = p["lon"]
    dist_m = haversine_m(KKL10_LAT, KKL10_LON, plat, plon)
    east_m, north_m = latlon_to_meters(plat, plon)
    walk_min = max(1, int(round(dist_m / 75.0)))
    cat_key = p.get("cat", p.get("category", "community"))
    pois.append({
        "name": p.get("name", ""),
        "cat": cat_key,
        "cat_he": p.get("cat_he", CAT_HE_MAP.get(cat_key, cat_key)),
        "color": p.get("color", CAT_COLOR_MAP.get(cat_key, "#3b82f6")),
        "desc": p.get("desc", p.get("description", "")),
        "lat": plat,
        "lon": plon,
        "dist": dist_m,
        "walk_min": walk_min,
        "east_m": east_m,
        "north_m": north_m
    })

pois.sort(key=lambda x: x["dist"])

spatial_data = {
    "project": {
        "name": "קק\"ל 10, פתח תקווה — קבוצת קולסקי",
        "developer": "יצחק קולסקי חברה לבניה והשקעות בע\"מ",
        "architect": "אדר' אייל סנדרוביץ'",
        "gush": 6374,
        "helka": 112,
        "lot_area_sqm": 862,
        "floors": "קרקע + 8 קומות + גג טכני + 2 מרתפי חניה (-1, -2)",
        "total_units": 25,
        "lat": KKL10_LAT,
        "lon": KKL10_LON
    },
    "distance_rings_m": [150, 250, 350, 500, 750, 1000, 1500, 2000],
    "pois": pois
}

# Preserve satellite tile data from kitroni_gis if present
for k in ["z16", "z17", "z15"]:
    if k in kitroni_gis:
        spatial_data[k] = kitroni_gis[k]

units_crm = [
    {"num": 1,  "floor": 0, "wing": "דרום-מערב (חזית דרומית)", "dir": "דרום, מערב", "type": "G-1 (דירת גן)", "rooms": 4, "area": 108, "balcony": 110, "balconyLabel": "גינה 110 מ\"ר", "parking": "חניה #1 (מרתף -1)", "parkIdx": 1, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 3490000, "box": [0.25, 0.00, 0.25, 6.35, 4.10, 21.75]},
    {"num": 2,  "floor": 0, "wing": "דרום-מזרח (חזית דרומית)", "dir": "דרום, מזרח", "type": "G-2 (דירת גן)", "rooms": 4, "area": 108, "balcony": 105, "balconyLabel": "גינה 105 מ\"ר", "parking": "חניה #2 (מרתף -1)", "parkIdx": 2, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 3450000, "box": [6.55, 0.00, 0.25, 12.48, 4.10, 21.75]},
    {"num": 3,  "floor": 1, "wing": "דרום-מזרח", "dir": "דרום, מזרח", "type": "טיפוס A", "rooms": 4, "area": 114, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #3 (מרתף -1)", "parkIdx": 3, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 2940000, "box": [6.55, 4.20, 0.25, 12.48, 7.25, 21.75]},
    {"num": 4,  "floor": 1, "wing": "חזית צפונית (קק\"ל)", "dir": "צפון, מזרח, מערב", "type": "טיפוס C", "rooms": 5, "area": 126, "balcony": 24, "balconyLabel": "מרפסת 24 מ\"ר", "parking": "חניה #4 (מרתף -1)", "parkIdx": 4, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 3430000, "box": [0.25, 4.20, 22.00, 12.48, 7.25, 32.84]},
    {"num": 5,  "floor": 1, "wing": "דרום-מערב", "dir": "דרום, מערב", "type": "טיפוס B", "rooms": 4, "area": 107, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #5 (מרתף -1)", "parkIdx": 5, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 2770000, "box": [0.25, 4.20, 0.25, 6.35, 7.25, 21.75]},
    {"num": 6,  "floor": 2, "wing": "חזית צפונית (קק\"ל)", "dir": "צפון, מזרח, מערב", "type": "טיפוס C", "rooms": 5, "area": 126, "balcony": 24, "balconyLabel": "מרפסת 24 מ\"ר", "parking": "חניה #6 (מרתף -1)", "parkIdx": 6, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 3450000, "box": [0.25, 7.35, 22.00, 12.48, 10.40, 32.84]},
    {"num": 7,  "floor": 2, "wing": "דרום-מזרח", "dir": "דרום, מזרח", "type": "טיפוס A", "rooms": 4, "area": 114, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #7 (מרתף -1)", "parkIdx": 7, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 2960000, "box": [6.55, 7.35, 0.25, 12.48, 10.40, 21.75]},
    {"num": 8,  "floor": 2, "wing": "דרום-מערב", "dir": "דרום, מערב", "type": "טיפוס B", "rooms": 4, "area": 107, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #8 (מרתף -1)", "parkIdx": 8, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 2790000, "box": [0.25, 7.35, 0.25, 6.35, 10.40, 21.75]},
    {"num": 9,  "floor": 3, "wing": "חזית צפונית (קק\"ל)", "dir": "צפון, מזרח, מערב", "type": "טיפוס D", "rooms": 4, "area": 106, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #9 (מרתף -1)", "parkIdx": 9, "status": "owner", "owner": "דירת בעלים (לביא / ברוכוב)", "price": 2800000, "box": [0.25, 10.50, 22.00, 12.48, 13.55, 32.84]},
    {"num": 10, "floor": 3, "wing": "דרום-מזרח", "dir": "דרום, מזרח", "type": "טיפוס E", "rooms": 5, "area": 129, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #10 (מרתף -1)", "parkIdx": 10, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 3350000, "box": [6.55, 10.50, 0.25, 12.48, 13.55, 21.75]},
    {"num": 11, "floor": 3, "wing": "דרום-מערב", "dir": "דרום, מערב", "type": "טיפוס B", "rooms": 4, "area": 107, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #11 (מרתף -1)", "parkIdx": 11, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 2820000, "box": [0.25, 10.50, 0.25, 6.35, 13.55, 21.75]},
    {"num": 12, "floor": 4, "wing": "חזית צפונית (קק\"ל)", "dir": "צפון, מזרח, מערב", "type": "טיפוס D", "rooms": 4, "area": 106, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #12 (מרתף -1)", "parkIdx": 12, "status": "owner", "owner": "דירת בעלים (גולדברג)", "price": 2820000, "box": [0.25, 13.65, 22.00, 12.48, 16.70, 32.84]},
    {"num": 13, "floor": 4, "wing": "דרום-מזרח", "dir": "דרום, מזרח", "type": "טיפוס E", "rooms": 5, "area": 129, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #13 (מרתף -1)", "parkIdx": 13, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 3370000, "box": [6.55, 13.65, 0.25, 12.48, 16.70, 21.75]},
    {"num": 14, "floor": 4, "wing": "דרום-מערב", "dir": "דרום, מערב", "type": "טיפוס B", "rooms": 4, "area": 107, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #14 (מרתף -1)", "parkIdx": 14, "status": "owner", "owner": "דירת בעלים (רדליך)", "price": 2840000, "box": [0.25, 13.65, 0.25, 6.35, 16.70, 21.75]},
    {"num": 15, "floor": 5, "wing": "חזית צפונית (קק\"ל)", "dir": "צפון, מזרח, מערב", "type": "טיפוס G", "rooms": 4, "area": 112, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #15 (מרתף -1)", "parkIdx": 15, "status": "reserved", "owner": "מלאי יזם — מכר דניאל", "price": 2950000, "box": [0.25, 16.80, 22.00, 12.48, 19.85, 32.84]},
    {"num": 16, "floor": 5, "wing": "דרום-מזרח", "dir": "דרום, מזרח", "type": "טיפוס F", "rooms": 5, "area": 122, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #16 (מרתף -1)", "parkIdx": 16, "status": "owner", "owner": "דירת בעלים (אדן)", "price": 3230000, "box": [6.55, 16.80, 0.25, 12.48, 19.85, 21.75]},
    {"num": 17, "floor": 5, "wing": "דרום-מערב", "dir": "דרום, מערב", "type": "טיפוס B", "rooms": 4, "area": 107, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #17 (מרתף -2)", "parkIdx": 17, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 2870000, "box": [0.25, 16.80, 0.25, 6.35, 19.85, 21.75]},
    {"num": 18, "floor": 6, "wing": "חזית צפונית (קק\"ל)", "dir": "צפון, מזרח, מערב", "type": "טיפוס H", "rooms": 5, "area": 122, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #18 (מרתף -2)", "parkIdx": 18, "status": "owner", "owner": "דירת בעלים (פלג)", "price": 3250000, "box": [0.25, 19.95, 22.00, 12.48, 23.00, 32.84]},
    {"num": 19, "floor": 6, "wing": "דרום-מזרח", "dir": "דרום, מזרח", "type": "טיפוס A", "rooms": 4, "area": 112, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #19 (מרתף -2)", "parkIdx": 19, "status": "owner", "owner": "דירת בעלים (לוי יפה/קרן/ליאור)", "price": 3010000, "box": [6.55, 19.95, 0.25, 12.48, 23.00, 21.75]},
    {"num": 20, "floor": 6, "wing": "דרום-מערב", "dir": "דרום, מערב", "type": "טיפוס B", "rooms": 4, "area": 107, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #20 (מרתף -2)", "parkIdx": 20, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 2890000, "box": [0.25, 19.95, 0.25, 6.35, 23.00, 21.75]},
    {"num": 21, "floor": 7, "wing": "חזית צפונית (קק\"ל)", "dir": "צפון, מזרח, מערב", "type": "טיפוס H", "rooms": 5, "area": 122, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #21 (מרתף -2)", "parkIdx": 21, "status": "owner", "owner": "דירת בעלים (גרין)", "price": 3280000, "box": [0.25, 23.10, 22.00, 12.48, 26.40, 32.84]},
    {"num": 22, "floor": 7, "wing": "דרום-מזרח", "dir": "דרום, מזרח", "type": "טיפוס A", "rooms": 4, "area": 112, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #22 (מרתף -2)", "parkIdx": 22, "status": "owner", "owner": "דירת בעלים (ציאנדר)", "price": 3040000, "box": [6.55, 23.10, 0.25, 12.48, 26.40, 21.75]},
    {"num": 23, "floor": 7, "wing": "דרום-מערב", "dir": "דרום, מערב", "type": "טיפוס B", "rooms": 4, "area": 107, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #23 (מרתף -2)", "parkIdx": 23, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 2920000, "box": [0.25, 23.10, 0.25, 6.35, 26.40, 21.75]},
    {"num": 24, "floor": 8, "wing": "פנטהאוז צפוני (חזית קק\"ל)", "dir": "צפון, מזרח, מערב", "type": "פנטהאוז PH-1", "rooms": 5, "area": 159, "balcony": 44, "balconyLabel": "מרפסת גג 44 מ\"ר", "parking": "2 חניות #24–25 (מרתף -2)", "parkIdx": 24, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 4920000, "box": [0.25, 26.50, 22.00, 12.48, 29.80, 30.78]},
    {"num": 25, "floor": 8, "wing": "פנטהאוז דרומי", "dir": "דרום, מזרח, מערב", "type": "פנטהאוז PH-2", "rooms": 5, "area": 133, "balcony": 39, "balconyLabel": "מרפסת גג 39 מ\"ר", "parking": "2 חניות #26–27 (מרתף -2)", "parkIdx": 26, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 4190000, "box": [0.25, 26.50, 2.30, 12.48, 29.80, 21.75]}
]

crm_payload = {
    "project": spatial_data["project"],
    "summary": {
        "total_units": 25,
        "kolsky_available": 15,
        "kolsky_reserved": 1,
        "owner_units": 9,
        "total_kolsky_revenue_nis": sum(u["price"] for u in units_crm if u["status"] in ("available", "reserved"))
    },
    "units": units_crm
}

for target_root in [SCRATCH_DIR, GDRIVE_DIR]:
    with open(os.path.join(target_root, "data", "spatial_map_data.json"), "w", encoding="utf-8") as f:
        json.dump(spatial_data, f, ensure_ascii=False, indent=2)
    with open(os.path.join(target_root, "data", "unified_3d_map.json"), "w", encoding="utf-8") as f:
        json.dump(spatial_data, f, ensure_ascii=False, indent=2)
    with open(os.path.join(target_root, "data", "kkl10_units_crm.json"), "w", encoding="utf-8") as f:
        json.dump(crm_payload, f, ensure_ascii=False, indent=2)

with open(os.path.join(SCRATCH_DIR, "data", "embedded_scope_data.js"), "w", encoding="utf-8") as f:
    f.write("const KKL10_UNITS = " + json.dumps(units_crm, ensure_ascii=False) + ";\n")
    f.write("const KKL10_POIS = " + json.dumps(pois, ensure_ascii=False) + ";\n")

print(f"Successfully generated CRM ({len(units_crm)} units) and GIS ({len(pois)} POIs) data files!")
