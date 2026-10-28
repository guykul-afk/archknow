import os, json, math

WORKSPACE = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\הרב קיטרוני 37-39 פתח תקווה"
ARTIFACT_DIR = r"C:\Users\User\.gemini\antigravity\brain\7493e840-6f07-4fdb-9508-8c38dfc14844"
SCRATCH_DIR = os.path.join(ARTIFACT_DIR, "scratch")
THREE_JS_PATH = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\_shared_engine\three.min.js"

with open(THREE_JS_PATH, "r", encoding="utf-8") as f:
    three_js_code = f.read()

with open(os.path.join(SCRATCH_DIR, "kitroni_extracted_plans.json"), "r", encoding="utf-8") as f:
    plans_data = json.load(f)

if not plans_data.get('k5_7', {}).get('furn_lines') and plans_data.get('k1', {}).get('furn_lines'):
    plans_data['k5_7']['furn_lines'] = plans_data['k1']['furn_lines']

with open(os.path.join(SCRATCH_DIR, "unified_kitroni_3d_map.json"), "r", encoding="utf-8") as f:
    map_3d_data = json.load(f)

with open(os.path.join(SCRATCH_DIR, "kitroni_spatial_map_data.json"), "r", encoding="utf-8") as f:
    spatial_gis_data = json.load(f)

# ==============================================================================
# BUILD COMPLETE 63-APARTMENT CATALOG & LIVE CRM DATABASE (BLDG 37: 30, BLDG 39: 33)
# Verified against: קטרוני 37-39 מחירי שיווק 17 במרץ 2025.xlsx & קטרוני נספח 2.xlsx
# ==============================================================================
FLOOR_ELEVS = {
    1: ('f1', 4.08, 6.77),
    2: ('f2', 7.14, 9.83),
    3: ('f3', 10.20, 12.89),
    4: ('f4', 13.26, 15.95),
    5: ('f5', 16.32, 19.01),
    6: ('f6', 19.38, 22.07),
    7: ('f7', 22.44, 25.15),
    8: ('f8', 25.67, 28.40),
    9: ('f9', 28.90, 31.66),
}

def make_unit_geometry(bldg, floor_num, wing):
    f_id, z0, z1 = FLOOR_ELEVS[floor_num]
    if bldg == 37:
        if floor_num == 9:
            if wing == 'W':
                return f_id, z0, z1, [-7.66, -25.15, 5.20, -11.30], -14.2, -18.2, [-11.5, -18.2], 'W'
            else: # E
                return f_id, z0, z1, [5.20, -25.15, 18.42, -11.30], 19.0, -18.2, [16.8, -19.5], 'E'
        elif floor_num == 8:
            if wing == 'NW':
                return f_id, z0, z1, [-13.85, -25.15, 3.00, -18.25], -16.2, -21.5, [-14.8, -21.5], 'W'
            elif wing == 'E':
                return f_id, z0, z1, [3.00, -25.15, 18.42, -11.30], 21.8, -21.0, [18.5, -21.8], 'E'
            else: # SW
                return f_id, z0, z1, [-13.85, -18.25, 3.00, -11.30], -16.2, -15.2, [-14.8, -15.2], 'W'
        elif floor_num in (2, 3, 4):
            if wing == 'NW':
                return f_id, z0, z1, [-13.85, -25.15, 5.00, -18.25], -16.2, -21.5, [-14.8, -21.5], 'W'
            elif wing == 'E':
                return f_id, z0, z1, [5.00, -25.15, 19.63, -11.30], 21.8, -21.5, [20.5, -21.8], 'E'
            else: # SW
                return f_id, z0, z1, [-13.85, -18.25, 5.00, -11.30], -16.2, -15.2, [-14.8, -15.2], 'W'
        else: # floors 1, 5, 6, 7 (4 apts/floor)
            if wing == 'NW':
                return f_id, z0, z1, [-13.85, -25.15, 5.00, -18.25], -16.2, -21.5, [-14.8, -21.5], 'W'
            elif wing == 'NE':
                return f_id, z0, z1, [5.00, -25.15, 19.63, -18.50], 21.8, -21.8, [20.5, -21.8], 'E'
            elif wing == 'SE':
                return f_id, z0, z1, [5.00, -18.50, 19.63, -11.30], 21.8, -15.0, [20.5, -15.0], 'E'
            else: # SW
                return f_id, z0, z1, [-13.85, -18.25, 5.00, -11.30], -16.2, -15.2, [-14.8, -15.2], 'W'
    else: # Building 39
        if floor_num == 9:
            if wing == 'W':
                return f_id, z0, z1, [-10.85, -4.95, 2.50, 7.56], -14.2, 1.3, [-12.4, 1.3], 'W'
            else: # E
                return f_id, z0, z1, [2.50, -4.95, 18.52, 7.56], 19.2, 1.3, [16.6, -1.3], 'E'
        elif floor_num == 8:
            if wing == 'NW':
                return f_id, z0, z1, [-13.95, -4.95, 2.50, 1.25], -16.2, -1.9, [-14.9, -1.9], 'W'
            elif wing == 'E':
                return f_id, z0, z1, [2.50, -4.95, 18.52, 7.56], 21.8, -1.5, [18.2, -1.8], 'E'
            else: # SW
                return f_id, z0, z1, [-13.95, 1.25, 2.50, 7.56], -16.2, 4.4, [-14.9, 4.4], 'W'
        else: # floors 1..7 (4 apts/floor)
            if wing == 'NW':
                return f_id, z0, z1, [-13.95, -4.95, 2.50, 1.25], -16.2, -1.9, [-14.9, -1.9], 'W'
            elif wing == 'NE':
                return f_id, z0, z1, [2.50, -4.95, 19.52, 1.25], 21.8, -1.9, [20.4, -1.9], 'E'
            elif wing == 'SE':
                return f_id, z0, z1, [2.50, 1.25, 19.52, 7.56], 21.8, 4.4, [20.4, 4.4], 'E'
            else: # SW
                return f_id, z0, z1, [-13.95, 1.25, 2.50, 7.56], -16.2, 4.4, [-14.9, 4.4], 'W'

def Math_PI_2_placeholder(d):
    return d

raw_b37 = [
    # (apt_num, floor_num, wing, rooms, area, balc, status, price, dir_he, type_he)
    (1, 1, 'NW', 5, 121.0, 12.0, 'available', 2975000, 'צפון / מערב', 'דירת 5 חדרים מרווחת'),
    (2, 1, 'NE', 3, 80.0,  14.0, 'available', 2250000, 'צפון / מזרח', 'דירת 3 חדרים חזית מזרחית'),
    (3, 1, 'SE', 4, 101.0, 12.0, 'available', 2610000, 'דרום / מזרח', 'דירת 4 חדרים מוארת'),
    (4, 1, 'SW', 4, 103.0, 12.0, 'available', 2670000, 'דרום / מערב (לרחוב קיטרוני)', 'דירת 4 חדרים חזיתית'),
    # Floors 2-4 (Owner 5-room apartments + storage)
    (5, 2, 'NW', 5, 118.2, 12.0, 'owner', 3010000, 'צפון / מערב / דרום', 'דירת 5 חדרים + מחסן (בעלים)'),
    (6, 2, 'E',  5, 118.3, 12.0, 'owner', 3010000, 'צפון / מזרח / דרום', 'דירת 5 חדרים מזרחית + מחסן (בעלים)'),
    (7, 2, 'SW', 5, 118.2, 12.0, 'owner', 3010000, 'דרום / מערב', 'דירת 5 חדרים + מחסן (בעלים)'),
    (8, 3, 'NW', 5, 118.2, 12.0, 'owner', 3030000, 'צפון / מערב / דרום', 'דירת 5 חדרים + מחסן (בעלים)'),
    (9, 3, 'E',  5, 118.3, 12.0, 'owner', 3030000, 'צפון / מזרח / דרום', 'דירת 5 חדרים מזרחית + מחסן (בעלים)'),
    (10,3, 'SW', 5, 118.2, 12.0, 'owner', 3030000, 'דרום / מערב', 'דירת 5 חדרים + מחסן (בעלים)'),
    (11,4, 'NW', 5, 118.2, 12.0, 'owner', 3040000, 'צפון / מערב / דרום', 'דירת 5 חדרים + מחסן (בעלים)'),
    (12,4, 'E',  5, 118.3, 12.0, 'owner', 3040000, 'צפון / מזרח / דרום', 'דירת 5 חדרים מזרחית + מחסן (בעלים)'),
    (13,4, 'SW', 5, 118.2, 12.0, 'owner', 3040000, 'דרום / מערב', 'דירת 5 חדרים + מחסן (בעלים)'),
    # Floor 5
    (14,5, 'NW', 5, 121.0, 12.0, 'available', 3050000, 'צפון / מערב', 'דירת 5 חדרים קומה גבוהה'),
    (15,5, 'NE', 3, 80.0,  14.0, 'available', 2325000, 'צפון / מזרח', 'דירת 3 חדרים קומה גבוהה'),
    (16,5, 'SE', 4, 100.0, 12.0, 'available', 2680000, 'דרום / מזרח', 'דירת 4 חדרים קומה גבוהה'),
    (17,5, 'SW', 4, 103.0, 12.0, 'available', 2730000, 'דרום / מערב', 'דירת 4 חדרים חזיתית'),
    # Floor 6
    (18,6, 'NW', 5, 121.0, 12.0, 'available', 3070000, 'צפון / מערב', 'דירת 5 חדרים פנורמית'),
    (19,6, 'NE', 3, 80.0,  14.0, 'available', 2360000, 'צפון / מזרח', 'דירת 3 חדרים פנורמית'),
    (20,6, 'SE', 4, 100.0, 12.0, 'available', 2750000, 'דרום / מזרח', 'דירת 4 חדרים פנורמית'),
    (21,6, 'SW', 4, 103.0, 12.0, 'available', 2750000, 'דרום / מערב', 'דירת 4 חדרים חזיתית'),
    # Floor 7
    (22,7, 'NW', 5, 121.0, 12.0, 'available', 3090000, 'צפון / מערב', 'דירת 5 חדרים פרימיום'),
    (23,7, 'NE', 3, 80.0,  14.0, 'available', 2380000, 'צפון / מזרח', 'דירת 3 חדרים פרימיום'),
    (24,7, 'SE', 4, 100.0, 12.0, 'available', 2760000, 'דרום / מזרח', 'דירת 4 חדרים + פרגולה'),
    (25,7, 'SW', 4, 103.0, 12.0, 'available', 2770000, 'דרום / מערב', 'דירת 4 חדרים פרימיום'),
    # Floor 8
    (26,8, 'NW', 5, 120.0, 12.0, 'available', 3110000, 'צפון / מערב', 'דירת 5 חדרים + פרגולה'),
    (27,8, 'E',  5, 132.0, 44.0, 'available', 3850000, 'צפון / מזרח / דרום', 'מיני-פנטהאוז 5 חדרים + מרפסת גג 44 מ"ר'),
    (28,8, 'SW', 5, 121.0, 12.0, 'available', 3120000, 'דרום / מערב', 'דירת 5 חדרים + פרגולה'),
    # Floor 9 Penthouse
    (29,9, 'W',  5, 114.0, 70.0, 'available', 3950000, 'צפון / מערב / דרום', 'פנטהאוז מערבי 5 חדרים + מרפסת גג 70 מ"ר'),
    (30,9, 'E',  5, 138.0, 25.0, 'available', 4032000, 'צפון / מזרח / דרום', 'פנטהאוז מזרחי 5 חדרים + מרפסת גג 25 מ"ר'),
]

raw_b39 = [
    # Floor 1
    (1, 1, 'NW', 3, 76.0,  12.0, 'available', 2230000, 'צפון / מערב', 'דירת 3 חדרים חזיתית'),
    (2, 1, 'NE', 3, 78.0,  12.0, 'available', 2250000, 'צפון / מזרח', 'דירת 3 חדרים שקטה'),
    (3, 1, 'SE', 4, 100.0, 12.0, 'available', 2610000, 'דרום / מזרח', 'דירת 4 חדרים מרווחת'),
    (4, 1, 'SW', 4, 102.0, 12.0, 'available', 2670000, 'דרום / מערב', 'דירת 4 חדרים חזיתית'),
    # Floor 2 (Apt 7 is Developer, Apts 5,6,8 are Owner)
    (5, 2, 'NW', 3, 78.5,  12.0, 'owner',     2260000, 'צפון / מערב', 'דירת 3 חדרים + מחסן (בעלים)'),
    (6, 2, 'NE', 3, 78.0,  12.0, 'owner',     2270000, 'צפון / מזרח', 'דירת 3 חדרים + מחסן (בעלים)'),
    (7, 2, 'SE', 4, 100.0, 12.0, 'available', 2630000, 'דרום / מזרח', 'דירת 4 חדרים (מלאי קולסקי)'),
    (8, 2, 'SW', 4, 102.2, 12.0, 'owner',     2690000, 'דרום / מערב', 'דירת 4 חדרים + מחסן (בעלים)'),
    # Floor 3 (Owner)
    (9, 3, 'NW', 3, 78.5,  12.0, 'owner',     2280000, 'צפון / מערב', 'דירת 3 חדרים + מחסן (בעלים)'),
    (10,3, 'NE', 3, 78.0,  12.0, 'owner',     2290000, 'צפון / מזרח', 'דירת 3 חדרים + מחסן (בעלים)'),
    (11,3, 'SE', 4, 100.0, 12.0, 'owner',     2650000, 'דרום / מזרח', 'דירת 4 חדרים + מחסן (בעלים)'),
    (12,3, 'SW', 4, 102.2, 12.0, 'owner',     2700000, 'דרום / מערב', 'דירת 4 חדרים + מחסן (בעלים)'),
    # Floor 4 (Owner)
    (13,4, 'NW', 3, 78.5,  12.0, 'owner',     2300000, 'צפון / מערב', 'דירת 3 חדרים + מחסן (בעלים)'),
    (14,4, 'NE', 3, 78.0,  12.0, 'owner',     2310000, 'צפון / מזרח', 'דירת 3 חדרים + מחסן (בעלים)'),
    (15,4, 'SE', 4, 100.0, 12.0, 'owner',     2670000, 'דרום / מזרח', 'דירת 4 חדרים + מחסן (בעלים)'),
    (16,4, 'SW', 4, 102.2, 12.0, 'owner',     2710000, 'דרום / מערב', 'דירת 4 חדרים + מחסן (בעלים)'),
    # Floor 5 (Developer)
    (17,5, 'NW', 3, 79.0,  12.0, 'available', 2325000, 'צפון / מערב', 'דירת 3 חדרים קומה גבוהה'),
    (18,5, 'NE', 3, 78.0,  12.0, 'available', 2325000, 'צפון / מזרח', 'דירת 3 חדרים קומה גבוהה'),
    (19,5, 'SE', 4, 100.0, 12.0, 'available', 2680000, 'דרום / מזרח', 'דירת 4 חדרים קומה גבוהה'),
    (20,5, 'SW', 4, 102.0, 12.0, 'available', 2730000, 'דרום / מערב', 'דירת 4 חדרים קומה גבוהה'),
    # Floor 6 (Developer)
    (21,6, 'NW', 3, 79.0,  12.0, 'available', 2360000, 'צפון / מערב', 'דירת 3 חדרים פנורמית'),
    (22,6, 'NE', 3, 78.0,  12.0, 'available', 2360000, 'צפון / מזרח', 'דירת 3 חדרים פנורמית'),
    (23,6, 'SE', 4, 100.0, 12.0, 'available', 2750000, 'דרום / מזרח', 'דירת 4 חדרים פנורמית'),
    (24,6, 'SW', 4, 102.0, 12.0, 'available', 2750000, 'דרום / מערב', 'דירת 4 חדרים פנורמית'),
    # Floor 7 (Developer)
    (25,7, 'NW', 3, 79.0,  12.0, 'available', 2370000, 'צפון / מערב', 'דירת 3 חדרים פרימיום'),
    (26,7, 'NE', 3, 78.0,  12.0, 'available', 2370000, 'צפון / מזרח', 'דירת 3 חדרים פרימיום'),
    (27,7, 'SE', 4, 100.0, 12.0, 'available', 2760000, 'דרום / מזרח', 'דירת 4 חדרים + פרגולה'),
    (28,7, 'SW', 4, 102.0, 12.0, 'available', 2760000, 'דרום / מערב', 'דירת 4 חדרים פרימיום'),
    # Floor 8 (Developer)
    (29,8, 'NW', 3, 79.0,  12.0, 'available', 2370000, 'צפון / מערב', 'דירת 3 חדרים קומה 8 + פרגולה'),
    (30,8, 'E',  6, 135.0, 38.0, 'available', 3940000, 'צפון / מזרח / דרום', 'מיני-פנטהאוז 6 חדרים + מרפסת גג 38 מ"ר'),
    (31,8, 'SW', 5, 122.0, 12.0, 'available', 3120000, 'דרום / מערב', 'דירת 5 חדרים קומה 8 + פרגולה'),
    # Floor 9 Penthouse (Developer)
    (32,9, 'W',  5, 123.0, 38.0, 'available', 3850000, 'צפון / מערב / דרום', 'פנטהאוז מערבי 5 חדרים + מרפסת גג 38 מ"ר'),
    (33,9, 'E',  6, 144.0, 27.0, 'available', 4200000, 'צפון / מזרח / דרום', 'פנטהאוז מזרחי 6 חדרים + מרפסת גג 27 מ"ר'),
]

# Generate 63 Underground Parking Stalls in the -3.85m Basement Garage
parking_stalls = []
# Row 1: North wall (y = -27.8 .. -23.0), x from -14.0 to +22.0
for i in range(16):
    sx = -13.5 + i * 2.25
    parking_stalls.append({"num": len(parking_stalls)+1, "x": round(sx, 2), "y": -26.2, "w": 2.10, "d": 4.60})
# Row 2: Upper middle North (y = -18.2 .. -13.6)
for i in range(16):
    sx = -13.5 + i * 2.25
    parking_stalls.append({"num": len(parking_stalls)+1, "x": round(sx, 2), "y": -16.0, "w": 2.10, "d": 4.60})
# Row 3: Lower middle South (y = -9.5 .. -4.9)
for i in range(16):
    sx = -13.5 + i * 2.25
    parking_stalls.append({"num": len(parking_stalls)+1, "x": round(sx, 2), "y": -8.2, "w": 2.10, "d": 4.60})
# Row 4: South perimeter (y = 6.2 .. 10.8)
for i in range(15):
    sx = -13.5 + i * 2.35
    parking_stalls.append({"num": len(parking_stalls)+1, "x": round(sx, 2), "y": 8.4, "w": 2.15, "d": 4.60})

kitroni_units = []
stall_idx = 0

for bldg, rows in [(37, raw_b37), (39, raw_b39)]:
    for (apt_num, floor_num, wing, rooms, area, balc, status, price, dir_he, type_he) in rows:
        f_id, z0, z1, bbox, bx, by, balc_pt, look_dir = make_unit_geometry(bldg, floor_num, wing)
        st = parking_stalls[stall_idx]
        stall_idx += 1
        uid = f"B{bldg}_{apt_num}"
        kitroni_units.append({
            "id": uid,
            "bldg": bldg,
            "aptNum": apt_num,
            "name": f"בניין {bldg} — דירה {apt_num}",
            "shortBadge": f"ב'{bldg} #{apt_num}",
            "floorNum": floor_num,
            "floorId": f_id,
            "floorLabel": f"קומה {floor_num}" + (" (פנטהאוז)" if floor_num == 9 else ""),
            "wing": wing,
            "rooms": rooms,
            "area": area,
            "balcony": balc,
            "status": status,
            "statusHe": "זמין לשיווק (מלאי קולסקי)" if status == "available" else "דירת בעלים (משוריין)",
            "price": price,
            "priceFormatted": f"₪{price:,}",
            "directions": dir_he,
            "typeHe": type_he,
            "z0": z0,
            "z1": z1,
            "bbox": bbox,
            "bx": bx,
            "by": by,
            "bz": round(0.5 * (z0 + z1), 2),
            "balcPt": balc_pt,
            "lookDir": look_dir if isinstance(look_dir, str) else 'W',
            "parkingNum": st["num"],
            "parkingX": st["x"],
            "parkingY": st["y"]
        })

print(f"Built {len(kitroni_units)} apartments ({sum(1 for u in kitroni_units if u['bldg']==37)} in Bldg 37, {sum(1 for u in kitroni_units if u['bldg']==39)} in Bldg 39)")
with open(os.path.join(SCRATCH_DIR, "kitroni_units_crm.json"), "w", encoding="utf-8") as f:
    json.dump({"units": kitroni_units, "parking_stalls": parking_stalls}, f, ensure_ascii=False, indent=2)
