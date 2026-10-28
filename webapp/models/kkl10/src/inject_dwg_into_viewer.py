import json
import os
import shutil

viewer_path = r'C:\Users\User\.gemini\antigravity\brain\17cdeb22-38a8-4e04-b15d-67ce64232225\kkl10_3d_bim_viewer.html'
index_path  = r'C:\Users\User\.gemini\antigravity\brain\17cdeb22-38a8-4e04-b15d-67ce64232225\index.html'
scratch_viewer_path = r'C:\Users\User\.gemini\antigravity\scratch\kkl10\kkl10_3d_bim_viewer.html'
dwg_json_path = r'C:\Users\User\.gemini\antigravity\scratch\kkl10\dwg_compiled_clusters.json'

with open(dwg_json_path, 'r', encoding='utf-8') as f:
    dwg_clusters = json.load(f)

dwg_json_str = json.dumps(dwg_clusters, separators=(',', ':'))
print(f"Loaded dwg_compiled_clusters.json ({len(dwg_json_str):,} bytes)")

# Exact 25 units updated to match the official DWG areas & room counts:
# G-1: 4rm 107.40m², G-2: 4rm 108.40m², B: 4rm 107.00m², A: 4rm 114.00m², C: 5rm 126.40m² + 23m² balc,
# D: 4rm 106.00m², E: 5rm 129.00m², G: 4rm 112.70m², F: 5rm 122.00m², H: 5rm 126.00m²,
# PH-1: 5rm 159.45m² + 44.30m² terrace, PH-2: 4rm 133.45m² + 29.90m² terrace
new_units = [
    {"num": 1,  "floor": 0, "wing": "דרום-מערב (חזית דרומית)", "dir": "דרום, מערב", "type": "G-1 (דירת גן)", "rooms": 4, "area": 107.4, "balcony": 110, "balconyLabel": "גינה פרטית ומשטח מרוצף", "parking": "חניה #1 (מרתף -1)", "parkIdx": 1, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 3490000, "box": [0.00, 0.00, -0.55, 6.27, 4.10, 21.81]},
    {"num": 2,  "floor": 0, "wing": "דרום-מזרח (חזית דרומית)", "dir": "דרום, מזרח", "type": "G-2 (דירת גן)", "rooms": 4, "area": 108.4, "balcony": 105, "balconyLabel": "גינה פרטית ומשטח מרוצף", "parking": "חניה #2 (מרתף -1)", "parkIdx": 2, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 3450000, "box": [6.27, 0.00, -0.55, 12.73, 4.10, 21.36]},
    {"num": 3,  "floor": 1, "wing": "דרום-מזרח", "dir": "דרום, מזרח", "type": "טיפוס A", "rooms": 4, "area": 114.0, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #3 (מרתף -1)", "parkIdx": 3, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 2940000, "box": [6.35, 4.20, 0.00, 12.73, 7.25, 22.07]},
    {"num": 4,  "floor": 1, "wing": "חזית צפונית (קק\"ל)", "dir": "צפון, מזרח, מערב", "type": "טיפוס C", "rooms": 5, "area": 126.4, "balcony": 23, "balconyLabel": "מרפסת 23 מ\"ר", "parking": "חניה #4 (מרתף -1)", "parkIdx": 4, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 3430000, "box": [0.00, 4.20, 22.07, 12.73, 7.25, 32.10]},
    {"num": 5,  "floor": 1, "wing": "דרום-מערב", "dir": "דרום, מערב", "type": "טיפוס B", "rooms": 4, "area": 107.0, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #5 (מרתף -1)", "parkIdx": 5, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 2770000, "box": [0.00, 4.20, 0.00, 6.35, 7.25, 21.81]},
    {"num": 6,  "floor": 2, "wing": "חזית צפונית (קק\"ל)", "dir": "צפון, מזרח, מערב", "type": "טיפוס C", "rooms": 5, "area": 126.4, "balcony": 23, "balconyLabel": "מרפסת 23 מ\"ר", "parking": "חניה #6 (מרתף -1)", "parkIdx": 6, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 3450000, "box": [0.00, 7.35, 22.07, 12.73, 10.40, 32.10]},
    {"num": 7,  "floor": 2, "wing": "דרום-מזרח", "dir": "דרום, מזרח", "type": "טיפוס A", "rooms": 4, "area": 114.0, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #7 (מרתף -1)", "parkIdx": 7, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 2960000, "box": [6.35, 7.35, 0.00, 12.73, 10.40, 22.07]},
    {"num": 8,  "floor": 2, "wing": "דרום-מערב", "dir": "דרום, מערב", "type": "טיפוס B", "rooms": 4, "area": 107.0, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #8 (מרתף -1)", "parkIdx": 8, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 2790000, "box": [0.00, 7.35, 0.00, 6.35, 10.40, 21.81]},
    {"num": 9,  "floor": 3, "wing": "חזית צפונית (קק\"ל)", "dir": "צפון, מזרח, מערב", "type": "טיפוס D", "rooms": 4, "area": 106.0, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #9 (מרתף -1)", "parkIdx": 9, "status": "owner", "owner": "דירת בעלים (לביא / ברוכוב)", "price": 2800000, "box": [0.00, 10.50, 23.47, 12.73, 13.55, 32.10]},
    {"num": 10, "floor": 3, "wing": "דרום-מזרח", "dir": "דרום, מזרח", "type": "טיפוס E", "rooms": 5, "area": 129.0, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #10 (מרתף -1)", "parkIdx": 10, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 3350000, "box": [6.35, 10.50, 0.00, 12.73, 13.55, 25.00]},
    {"num": 11, "floor": 3, "wing": "דרום-מערב", "dir": "דרום, מערב", "type": "טיפוס B", "rooms": 4, "area": 107.0, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #11 (מרתף -1)", "parkIdx": 11, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 2820000, "box": [0.00, 10.50, 0.00, 6.35, 13.55, 21.81]},
    {"num": 12, "floor": 4, "wing": "חזית צפונית (קק\"ל)", "dir": "צפון, מזרח, מערב", "type": "טיפוס D", "rooms": 4, "area": 106.0, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #12 (מרתף -1)", "parkIdx": 12, "status": "owner", "owner": "דירת בעלים (גולדברג)", "price": 2820000, "box": [0.00, 13.65, 23.47, 12.73, 16.70, 32.10]},
    {"num": 13, "floor": 4, "wing": "דרום-מזרח", "dir": "דרום, מזרח", "type": "טיפוס E", "rooms": 5, "area": 129.0, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #13 (מרתף -1)", "parkIdx": 13, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 3370000, "box": [6.35, 13.65, 0.00, 12.73, 16.70, 25.00]},
    {"num": 14, "floor": 4, "wing": "דרום-מערב", "dir": "דרום, מערב", "type": "טיפוס B", "rooms": 4, "area": 107.0, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #14 (מרתף -1)", "parkIdx": 14, "status": "owner", "owner": "דירת בעלים (רדליך)", "price": 2840000, "box": [0.00, 13.65, 0.00, 6.35, 16.70, 21.81]},
    {"num": 15, "floor": 5, "wing": "חזית צפונית (קק\"ל)", "dir": "צפון, מזרח, מערב", "type": "טיפוס G", "rooms": 4, "area": 112.7, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #15 (מרתף -1)", "parkIdx": 15, "status": "reserved", "owner": "מלאי יזם — מכר דניאל", "price": 2950000, "box": [0.00, 16.80, 23.47, 12.73, 19.85, 32.10]},
    {"num": 16, "floor": 5, "wing": "דרום-מזרח", "dir": "דרום, מזרח", "type": "טיפוס F", "rooms": 5, "area": 122.0, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #16 (מרתף -2)", "parkIdx": 16, "status": "owner", "owner": "דירת בעלים (אדן)", "price": 3230000, "box": [6.35, 16.80, 0.00, 12.73, 19.85, 23.70]},
    {"num": 17, "floor": 5, "wing": "דרום-מערב", "dir": "דרום, מערב", "type": "טיפוס B", "rooms": 4, "area": 107.0, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #17 (מרתף -2)", "parkIdx": 17, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 2870000, "box": [0.00, 16.80, 0.00, 6.35, 19.85, 21.81]},
    {"num": 18, "floor": 6, "wing": "חזית צפונית (קק\"ל)", "dir": "צפון, מזרח, מערב", "type": "טיפוס H", "rooms": 5, "area": 126.0, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #18 (מרתף -2)", "parkIdx": 18, "status": "owner", "owner": "דירת בעלים (פלג)", "price": 3250000, "box": [0.00, 19.95, 22.07, 12.73, 23.00, 32.10]},
    {"num": 19, "floor": 6, "wing": "דרום-מזרח", "dir": "דרום, מזרח", "type": "טיפוס A", "rooms": 4, "area": 114.0, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #19 (מרתף -2)", "parkIdx": 19, "status": "owner", "owner": "דירת בעלים (לוי יפה/קרן/ליאור)", "price": 3010000, "box": [6.35, 19.95, 0.00, 12.73, 23.00, 22.07]},
    {"num": 20, "floor": 6, "wing": "דרום-מערב", "dir": "דרום, מערב", "type": "טיפוס B", "rooms": 4, "area": 107.0, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #20 (מרתף -2)", "parkIdx": 20, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 2890000, "box": [0.00, 19.95, 0.00, 6.35, 23.00, 21.81]},
    {"num": 21, "floor": 7, "wing": "חזית צפונית (קק\"ל)", "dir": "צפון, מזרח, מערב", "type": "טיפוס H", "rooms": 5, "area": 126.0, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #21 (מרתף -2)", "parkIdx": 21, "status": "owner", "owner": "דירת בעלים (גרין)", "price": 3280000, "box": [0.00, 23.10, 22.07, 12.73, 26.40, 32.10]},
    {"num": 22, "floor": 7, "wing": "דרום-מזרח", "dir": "דרום, מזרח", "type": "טיפוס A", "rooms": 4, "area": 114.0, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #22 (מרתף -2)", "parkIdx": 22, "status": "owner", "owner": "דירת בעלים (ציאנדר)", "price": 3040000, "box": [6.35, 23.10, 0.00, 12.73, 26.40, 22.07]},
    {"num": 23, "floor": 7, "wing": "דרום-מערב", "dir": "דרום, מערב", "type": "טיפוס B", "rooms": 4, "area": 107.0, "balcony": 12, "balconyLabel": "מרפסת 12 מ\"ר", "parking": "חניה #23 (מרתף -2)", "parkIdx": 23, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 2920000, "box": [0.00, 23.10, 0.00, 6.35, 26.40, 21.81]},
    {"num": 24, "floor": 8, "wing": "פנטהאוז צפוני (חזית קק\"ל)", "dir": "צפון, מזרח, מערב", "type": "פנטהאוז PH-1", "rooms": 5, "area": 159.45, "balcony": 44.3, "balconyLabel": "מרפסת גג 44.30 מ\"ר", "parking": "2 חניות #24–25 (מרתף -2)", "parkIdx": 24, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 4920000, "box": [0.00, 26.50, 7.64, 12.73, 29.80, 29.02]},
    {"num": 25, "floor": 8, "wing": "פנטהאוז דרומי", "dir": "דרום, מזרח, מערב", "type": "פנטהאוז PH-2", "rooms": 4, "area": 133.45, "balcony": 29.9, "balconyLabel": "מרפסת גג 29.90 מ\"ר", "parking": "2 חניות #26–27 (מרתף -2)", "parkIdx": 26, "status": "available", "owner": "מלאי יזם (קולסקי)", "price": 4190000, "box": [0.00, 26.50, 1.74, 12.73, 29.80, 21.80]}
]
new_units_str = f"    const KKL10_UNITS = {json.dumps(new_units, ensure_ascii=False)};"

dwg_builder_js = f"""
    // ============================================================================
    // OFFICIAL AUTOCAD DWG-COMPILED 3D BIM & 2D FLOOR CAD ARCHITECTURE (v7.0 DWG)
    // Source: 246-פרויקט קקל-p-23 - Sheet - A0-000002 - גרמושקה - תכניות-חישוב שטחים רובוטי (1).dwg
    // ============================================================================
    const DWG_CLUSTERS = {dwg_json_str};

    function classifyDwgWall(clusterKey, x0, x1, n0, n1) {{
      const dx = x1 - x0, dn = n1 - n0;
      const minT = Math.min(dx, dn);
      const cx = 0.5 * (x0 + x1), cn = 0.5 * (n0 + n1);

      if (clusterKey.startsWith('B')) {{
        if (x0 <= -2.8 || x1 >= 15.6 || n0 <= -2.9 || n1 >= 35.4 || (x0 >= 12.4 && n0 >= 12.5 && n1 <= 23.5)) {{
          return ['Basements', 'Sub_Concrete'];
        }}
        if (cx >= 4.1 && cx <= 8.5 && cn >= 7.5 && cn <= 21.6) {{
          return ['CoreStairsElev', 'Int_CoreWall'];
        }}
        return ['InteriorWalls', 'Sub_WallFill'];
      }}

      if (clusterKey === 'F9_Roof' || clusterKey === 'F10_UpperRoof') {{
        if (cx >= 4.0 && cx <= 8.6 && cn >= 7.5 && cn <= 21.6) {{
          return ['CoreStairsElev', 'E_LightStucco'];
        }}
        return ['RoofParapets', 'B_WhitePanel'];
      }}

      // Exterior envelope walls on residential floors (F0..F8)
      const isSouthExt = (clusterKey === 'F0_Ground' && n0 <= -0.10) ||
                         (clusterKey === 'F8_Penthouse' && n0 <= 2.20 && n1 >= 1.70 && dn <= 0.55) ||
                         (!['F0_Ground', 'F8_Penthouse'].includes(clusterKey) && n0 <= 0.45 && dn <= 0.55);
      const isNorthExt = (clusterKey === 'F0_Ground' && n1 >= 29.00 && dn <= 0.55) ||
                         (clusterKey === 'F8_Penthouse' && n1 >= 28.55 && n0 <= 29.10 && dn <= 0.55) ||
                         (!['F0_Ground', 'F8_Penthouse'].includes(clusterKey) && n1 >= 31.65 && dn <= 0.55);
      const isWestExt  = (x0 <= 0.42 && dx <= 0.50);
      const isEastExt  = (x1 >= 12.30 && dx <= 0.50) || (clusterKey === 'F0_Ground' && x0 >= 11.80 && n0 >= 17.0 && dx <= 0.50);

      if (isSouthExt || isNorthExt || isWestExt || isEastExt) {{
        return ['MainStructure', 'E_LightStucco'];
      }}

      // MAMAD blast-reinforced concrete walls (20cm-35cm around SW, SE, and NW Mamads)
      if (minT >= 0.18) {{
        if ((x1 <= 3.45 && n0 >= 7.05 && n1 <= 11.45) ||
            (x0 >= 9.35 && n0 >= 7.05 && n1 <= 11.45) ||
            (x1 <= 4.45 && n0 >= 21.65 && n1 <= 25.15 && clusterKey !== 'F0_Ground')) {{
          return ['InteriorWalls', 'Int_MamadWall'];
        }}
      }}

      // Central core (2 elevators + protected stairwell + smoke/utility shafts)
      if (cx >= 4.15 && cx <= 8.55 && cn >= 7.45 && cn <= 21.65) {{
        if (minT >= 0.18) return ['CoreStairsElev', 'Int_CoreWall'];
        return ['InteriorWalls', 'Int_Partition'];
      }}

      // Acoustic apartment party walls (thickness >= 18cm) vs 10cm interior room partitions
      if (minT >= 0.18) {{
        return ['InteriorWalls', 'Int_PartyWall'];
      }}
      return ['InteriorWalls', 'Int_Partition'];
    }}

    function addDwgFloorLabels(floorIdx, y0, clusterKey) {{
      if (clusterKey === 'B1_Basement1') {{
        addRoomLabel(floorIdx, y0, 6.36, 26.00, 'חניון מרתף 1- (15 חניות)', '1875×3971 (793 מ"ר)');
        addRoomLabel(floorIdx, y0, 6.36,  4.50, 'חניות 1-8 + מיגון מרתף', 'שיפוע רמפה 15%');
        addRoomLabel(floorIdx, y0, 1.60, 15.50, 'מחסנים מערביים (6 יח)', '3.7 - 5.2 מ"ר');
        addRoomLabel(floorIdx, y0, 11.20, 14.20, 'מחסנים מזרחיים (4 יח)', '3.8 - 5.0 מ"ר');
        addRoomLabel(floorIdx, y0, 6.83, 16.30, 'חדר מדרגות ומעליות', 'פ.ר -4.25');
        return;
      }}
      if (clusterKey === 'B2_Basement2') {{
        addRoomLabel(floorIdx, y0, 6.36, 26.00, 'חניון מרתף 2- (16 חניות)', '1875×3971 (793 מ"ר)');
        addRoomLabel(floorIdx, y0, 6.36,  4.50, 'חניות 16-24 (מרתף 2-)', 'פ.ר -7.45');
        addRoomLabel(floorIdx, y0, 1.60, 15.50, 'מחסנים מערביים (6 יח)', '3.7 - 5.2 מ"ר');
        addRoomLabel(floorIdx, y0, 11.20, 14.20, 'מחסנים מזרחיים (4 יח)', '3.8 - 5.0 מ"ר');
        addRoomLabel(floorIdx, y0, 14.30, 20.65, 'חדר משאבות (-8.82)', '15.0 מ"ר');
        addRoomLabel(floorIdx, y0, 14.30, 14.30, 'מאגר מים 15 קוב (-8.52)', '335×370 ס"מ');
        return;
      }}
      if (clusterKey === 'F9_Roof') {{
        addRoomLabel(floorIdx, y0, 6.47, 13.50, 'חדר מדרגות ופיר מעליות', '+31.30 / +32.40');
        addRoomLabel(floorIdx, y0, 2.20, 14.43, 'גנרטור חירום', '270×115 ס"מ');
        addRoomLabel(floorIdx, y0, 6.36, 24.50, 'מערכי קולטי שמש צפוניים', 'פ.ר +29.90');
        addRoomLabel(floorIdx, y0, 6.36,  5.60, 'מערכי קולטי שמש דרומיים', 'מעקה גג +31.40');
        return;
      }}
      if (clusterKey === 'F0_Ground') {{
        // Apt G-1 (SW)
        addRoomLabel(0, y0, 3.16,  2.85, 'ח. מגורים ופ. אוכל (G-1)', '591×634 (107.4 מ"ר)');
        addRoomLabel(0, y0, 1.65,  5.00, 'מטבח (G-1)', '287×300 ס"מ');
        addRoomLabel(0, y0, 1.69,  9.26, 'ממ"ד / ח. שינה', '268×345 ס"מ');
        addRoomLabel(0, y0, 2.12, 12.39, 'ח. רחצה', '185×230 ס"מ');
        addRoomLabel(0, y0, 1.63, 15.39, 'ח. שינה', '283×340 ס"מ');
        addRoomLabel(0, y0, 2.18, 18.80, 'ח. שינה הורים', '393×290 ס"מ');
        addRoomLabel(0, y0, 1.40, 20.94, 'ח. רחצה הורים', '239×150 ס"מ');
        addRoomLabel(0, y0, 2.99, -1.85, 'גינה פרטית ומשטח מרוצף (G-1)', 'יציאה דרומית');
        // Apt G-2 (SE)
        addRoomLabel(0, y0, 9.47,  2.85, 'ח. מגורים ופ. אוכל (G-2)', '611×634 (108.4 מ"ר)');
        addRoomLabel(0, y0, 11.09, 5.00, 'מטבח (G-2)', '289×300 ס"מ');
        addRoomLabel(0, y0, 11.06, 9.26, 'ממ"ד / ח. שינה', '264×345 ס"מ');
        addRoomLabel(0, y0, 10.62, 12.39, 'ח. רחצה', '186×230 ס"מ');
        addRoomLabel(0, y0, 11.11, 15.35, 'ח. שינה', '283×332 ס"מ');
        addRoomLabel(0, y0, 10.69, 18.80, 'ח. שינה הורים', '270×373 ס"מ');
        addRoomLabel(0, y0, 8.77, -1.85, 'גינה פרטית ומשטח מרוצף (G-2)', 'יציאה דרומית');
        // North Lobby & Service Wing
        addRoomLabel(0, y0, 8.35, 26.50, 'לובי כניסה ראשי (+0.00)', '760×547 ס"מ');
        addRoomLabel(0, y0, 9.85, 22.85, 'ח. עגלות ואופניים', '405×250 ס"מ');
        addRoomLabel(0, y0, 2.25, 24.60, 'חדר אשפה (עגלות 360 ל)', '389×521 ס"מ');
        addRoomLabel(0, y0, 2.25, 28.35, 'חדר גז', '389×132 ס"מ');
        addRoomLabel(0, y0, 6.58, 16.00, 'חדר מדרגות ו-2 מעליות', '6 נוסעים');
        return;
      }}
      if (clusterKey === 'F8_Penthouse') {{
        // PH-2 (South Penthouse, 4 rooms, 133.45m² + 29.90m² Terrace)
        addRoomLabel(8, y0, 6.37,  0.65, 'מרפסת גג דרומית (PH-2)', '1233×215 (29.90 מ"ר)');
        addRoomLabel(8, y0, 5.80,  4.30, 'ח. מגורים ופ. אוכל (PH-2)', '928×465 (133.45 מ"ר)');
        addRoomLabel(8, y0, 2.30,  5.95, 'מטבח + אי (PH-2)', '419×300 ס"מ');
        addRoomLabel(8, y0, 11.09, 4.30, 'ח. שינה דרום-מזרחי', '289×406 ס"מ');
        addRoomLabel(8, y0, 11.04, 9.50, 'ממ"ד / ח. שינה (PH-2)', '268×370 ס"מ');
        addRoomLabel(8, y0, 10.62, 12.38, 'ח. רחצה (PH-2)', '186×225 ס"מ');
        addRoomLabel(8, y0, 11.11, 15.40, 'ח. שינה (PH-2)', '283×340 ס"מ');
        addRoomLabel(8, y0, 11.08, 19.85, 'ח. שינה הורים (PH-2)', '288×474 ס"מ');
        // PH-1 (North Penthouse, 5 rooms, 159.45m² + 44.30m² Terrace)
        addRoomLabel(8, y0, 1.69,  9.50, 'ממ"ד / ח. שינה (PH-1)', '268×345 ס"מ');
        addRoomLabel(8, y0, 2.12, 12.39, 'ח. רחצה (PH-1)', '185×230 ס"מ');
        addRoomLabel(8, y0, 1.63, 15.54, 'ח. שינה 1 (PH-1)', '283×370 ס"מ');
        addRoomLabel(8, y0, 1.63, 19.26, 'ח. שינה 2 (PH-1)', '283×355 ס"מ');
        addRoomLabel(8, y0, 1.42, 23.10, 'ח. רחצה הורים', '244×205 ס"מ');
        addRoomLabel(8, y0, 2.15, 26.85, 'ח. שינה הורים (PH-1)', '419×353 ס"מ');
        addRoomLabel(8, y0, 7.60, 26.85, 'ח. מגורים ופ. אוכל (PH-1)', '803×658 (159.45 מ"ר)');
        addRoomLabel(8, y0, 10.39, 23.50, 'מטבח + אי (PH-1)', '429×320 ס"מ');
        addRoomLabel(8, y0, 6.37, 30.65, 'מרפסת גג צפונית (PH-1)', '1154×333 (44.30 מ"ר)');
        return;
      }}

      // Typical Residential Floors 1 to 7 (F1_2, F3_4, F5, F6_7)
      // 1. Apt B (South-West, 4 rooms, 107.00m² + 12m² Balcony — identical on Floors 1–7)
      addRoomLabel(floorIdx, y0, 3.30, -0.95, 'מרפסת שמש (B)', '597×207 (12 מ"ר)');
      addRoomLabel(floorIdx, y0, 3.28,  2.85, 'ח. מגורים ופ. אוכל (B)', '614×579 (107.0 מ"ר)');
      addRoomLabel(floorIdx, y0, 1.72,  4.85, 'מטבח (B)', '302×293 ס"מ');
      addRoomLabel(floorIdx, y0, 1.69,  9.26, 'ממ"ד / ח. שינה', '268×345 ס"מ');
      addRoomLabel(floorIdx, y0, 2.12, 12.39, 'ח. רחצה', '185×230 ס"מ');
      addRoomLabel(floorIdx, y0, 1.63, 15.39, 'ח. שינה', '283×340 ס"מ');
      addRoomLabel(floorIdx, y0, 2.18, 18.71, 'ח. שינה הורים', '393×305 ס"מ');
      addRoomLabel(floorIdx, y0, 1.48, 21.01, 'ח. רחצה הורים', '253×135 ס"מ');

      // 2. South-East Apartment: Apt A (F1-2, F6-7: 4rm 114.0m²), Apt E (F3-4: 5rm 129.0m²), Apt F (F5: 5rm 122.0m²)
      const seType = (floorIdx <= 2 || floorIdx >= 6) ? 'A' : (floorIdx <= 4 ? 'E' : 'F');
      const seArea = (seType === 'A') ? '114.00 מ"ר' : (seType === 'E' ? '129.00 מ"ר' : '122.00 מ"ר');
      addRoomLabel(floorIdx, y0, 9.35, -0.95, `מרפסת שמש (${{seType}})`, '597×207 (12 מ"ר)');
      addRoomLabel(floorIdx, y0, 9.59,  2.85, `ח. מגורים ופ. אוכל (${{seType}})`, `588×580 (${{seArea}})`);
      addRoomLabel(floorIdx, y0, 11.01, 4.85, `מטבח (${{seType}})`, '302×292 ס"מ');
      addRoomLabel(floorIdx, y0, 11.04, 9.28, 'ממ"ד / ח. שינה', '268×345 ס"מ');
      addRoomLabel(floorIdx, y0, 10.62, 12.40, 'ח. רחצה', '186×230 ס"מ');
      if (seType === 'A') {{
        addRoomLabel(floorIdx, y0, 11.11, 15.40, 'ח. שינה', '283×340 ס"מ');
        addRoomLabel(floorIdx, y0, 11.08, 19.57, 'ח. שינה הורים', '288×475 ס"מ');
        addRoomLabel(floorIdx, y0, 8.64,  21.00, 'ח. רחצה הורים', '180×195 ס"מ');
      }} else if (seType === 'E') {{
        addRoomLabel(floorIdx, y0, 11.11, 15.50, 'ח. שינה 1', '283×360 ס"מ');
        addRoomLabel(floorIdx, y0, 11.11, 19.22, 'ח. שינה 2', '283×365 ס"מ');
        addRoomLabel(floorIdx, y0, 11.08, 23.15, 'ח. שינה הורים (E)', '288×364 ס"מ');
      }} else {{
        addRoomLabel(floorIdx, y0, 11.11, 15.27, 'ח. שינה 1', '283×314 ס"מ');
        addRoomLabel(floorIdx, y0, 11.11, 18.54, 'ח. שינה 2', '283×320 ס"מ');
        addRoomLabel(floorIdx, y0, 11.08, 22.00, 'ח. שינה הורים (F)', '288×324 ס"מ');
      }}

      // 3. North Apartment: Apt C (F1-2: 5rm 126.40m²), Apt D (F3-4: 4rm 106.00m²), Apt G (F5: 4rm 112.70m²), Apt H (F6-7: 5rm 126.00m²)
      const nType = (floorIdx <= 2) ? 'C' : (floorIdx <= 4 ? 'D' : (floorIdx === 5 ? 'G' : 'H'));
      const nArea = (nType === 'C') ? '126.40 מ"ר' : (nType === 'D' ? '106.00 מ"ר' : (nType === 'G' ? '112.70 מ"ר' : '126.00 מ"ר'));
      if (floorIdx <= 2) {{
        addRoomLabel(floorIdx, y0, 6.37, 33.05, 'מרפסת צפונית (C)', '1199×199 (23 מ"ר)');
      }} else {{
        addRoomLabel(floorIdx, y0, 9.34, 33.05, `מרפסת צפונית (${{nType}})`, '604×200 (12 מ"ר)');
      }}
      addRoomLabel(floorIdx, y0, 2.25, 23.32, 'ממ"ד / ח. שינה', '379×276 ס"מ');
      addRoomLabel(floorIdx, y0, 2.14, 26.10, 'ח. רחצה', '190×230 ס"מ');
      addRoomLabel(floorIdx, y0, 1.65, 28.03, 'ח. רחצה הורים', '288×136 ס"מ');
      addRoomLabel(floorIdx, y0, 2.25, 30.33, 'ח. שינה הורים', '408×305 ס"מ');
      addRoomLabel(floorIdx, y0, 5.89, 30.33, 'ח. שינה צפוני', '300×335 ס"מ');
      addRoomLabel(floorIdx, y0, 10.01, 29.80, `ח. מגורים (${{nType}})`, `503×676 (${{nArea}})`);
      addRoomLabel(floorIdx, y0, 6.49, 27.43, 'פ. אוכל', '200×331 ס"מ');
      if (nType === 'C' || nType === 'H') {{
        addRoomLabel(floorIdx, y0, 10.53, 23.60, 'ח. שינה מזרחי', '399×280 ס"מ');
        addRoomLabel(floorIdx, y0, 10.01, 26.40, `מטבח + אי (${{nType}})`, '398×300 ס"מ');
      }} else if (nType === 'D') {{
        addRoomLabel(floorIdx, y0, 10.01, 26.30, 'מטבח + אי (D)', '398×300 ס"מ');
      }} else {{
        addRoomLabel(floorIdx, y0, 10.01, 25.30, 'מטבח + אי (G)', '468×330 ס"מ');
      }}
    }}

    function renderDwgClusterFloor(floorIdx, clusterKey, y0, y1, slabT) {{
      const c = DWG_CLUSTERS[clusterKey];
      if (!c) return;
      const wt = y1 - slabT;
      const cy = y0 + 0.055;
      const yWood = y0 + 0.032;

      // 1. Floor Base Slabs & Balcony Slabs (exact DWG perimeter per floor)
      if (clusterKey === 'F0_Ground') {{
        addBox('Basements', 'Sub_Concrete', -3.41, -0.35, -3.60, 16.14, 0.00, 36.11, 'F0_Basement_Ceiling_Slab');
        addBox('MainStructure', 'Int_FloorTile', 0.00, 0.00, -0.55, 12.73, 0.03, 21.80, 'F0_Ground_Apts_Floor');
        addBox('MainStructure', 'Int_CorridorFl', 0.20, 0.00, 21.80, 12.15, 0.03, 32.50, 'F0_Ground_Lobby_Floor');
        // South paved garden patios (משטח מרוצף)
        addBox('BalconiesRailings', 'B_WhitePanel', 0.38, -0.02, -2.07, 12.35, 0.02, -0.55, 'F0_South_Garden_Patio');
        // Ground Floor ceiling slab (+3.83..+4.20m)
        addBox('MainStructure', 'B_WhitePanel', 0.00, wt, 0.00, 12.73, y1, 32.10, 'F0_Ceiling_Slab');
      }} else if (clusterKey === 'B1_Basement1') {{
        addBox('Basements', 'Sub_Concrete', -3.41, y0 - 0.35, -3.60, 16.14, y0, 36.11, 'B1_Floor_Slab');
        addSlopedSlabN('Basements', 'Sub_Ramp', 12.65, 15.85, 34.00, 0.00, 8.50, y0, 0.30, 'B1_East_Entry_Ramp');
      }} else if (clusterKey === 'B2_Basement2') {{
        addBox('Basements', 'Sub_Concrete', -3.41, y0 - 0.45, -3.60, 16.14, y0, 36.11, 'B2_Foundation_Slab');
        addSlopedSlabN('Basements', 'Sub_Ramp', -2.90, 0.20, 24.00, -4.35, 8.50, y0, 0.30, 'B2_West_Internal_Ramp');
      }} else if (clusterKey === 'F8_Penthouse') {{
        addBox('MainStructure', 'Int_FloorTile', 0.00, y0, 1.74, 12.73, y0 + 0.03, 29.02, 'F8_PH_Interior_Floor');
        addBox('MainStructure', 'B_WhitePanel', 0.00, wt, 1.74, 12.73, y1, 29.02, 'F8_PH_Ceiling_Slab');
        // PH-2 South Roof Terrace (N = -0.48..1.74m, 29.90m²) & PH-1 North Roof Terrace (N = 29.02..32.35m + NE cantilever to 33.95m, 44.30m²)
        addBox('BalconiesRailings', 'B_WhitePanel', 0.00, y0 - 0.30, -0.55, 12.73, y0 + 0.02, 1.74, 'F8_PH2_South_Terrace_Slab');
        addBox('BalconiesRailings', 'B_WhitePanel', 0.00, y0 - 0.30, 29.02, 12.73, y0 + 0.02, 32.48, 'F8_PH1_North_Terrace_Slab');
        addBox('BalconiesRailings', 'B_WhitePanel', 6.32, y0 - 0.30, 32.48, 12.36, y0 + 0.02, 34.10, 'F8_PH1_NE_Cantilever_Slab');
        addAluminumPergola(0.82, y0, -0.13, 11.91, y1, 1.65, 'F8_PH2_South_Pergola');
        addAluminumPergola(0.82, y0, 29.09, 11.91, y1, 30.95, 'F8_PH1_North_Pergola');
      }} else if (clusterKey === 'F9_Roof') {{
        // Roof bulkhead & elevator machine room caps (+31.30m / +32.40m)
        addBox('CoreStairsElev', 'B_WhitePanel', 5.79, 31.10, 8.20, 8.45, 31.35, 13.25, 'F9_Elevator_Shaft_Cap_3130');
        addBox('CoreStairsElev', 'B_WhitePanel', 5.79, 32.15, 13.25, 8.45, 32.40, 18.00, 'F10_Stair_Bulkhead_Cap_3240');
        // Emergency Generator on Roof (X = 1.05..2.25, N = 13.10..15.80)
        addBox('RoofParapets', 'C_MidSpandrel', 1.05, y0, 13.10, 2.25, y0 + 1.35, 15.80, 'F9_Emergency_Generator');
      }} else {{
        // Typical Floors 1 to 7
        addBox('MainStructure', 'Int_FloorTile', 0.00, y0, 0.00, 12.73, y0 + 0.03, 32.10, `F${{floorIdx}}_Interior_Floor`);
        addBox('MainStructure', 'B_WhitePanel', 0.00, wt, 0.00, 12.73, y1, 32.10, `F${{floorIdx}}_Ceiling_Slab`);
        // South Balconies (Apt B & Apt A/E/F: X = 0.38..12.35, N = -1.92..0.00) + Frosted Glass Privacy Divider at X = 6.27
        addBox('BalconiesRailings', 'B_WhitePanel', 0.38, y0 - 0.28, -1.92, 12.35, y0, 0.00, `F${{floorIdx}}_South_Balconies_Slab`);
        addBox('BalconiesRailings', 'A_FrostedDiv', 6.24, y0, -1.88, 6.32, y0 + 1.85, 0.00, `F${{floorIdx}}_South_Balcony_Divider`);
        // North Balcony: Full width (23m², X = 0.37..12.36) on Floors 1–2; East half (12m², X = 6.32..12.36) on Floors 3–7
        const nbX0 = (floorIdx <= 2) ? 0.37 : 6.32;
        addBox('BalconiesRailings', 'B_WhitePanel', nbX0, y0 - 0.28, 32.10, 12.36, y0, 33.95, `F${{floorIdx}}_North_Balcony_Slab`);
      }}

      // 2. Central Staircase 3D Flights & Elevator Shafts (on B2..F8)
      if (clusterKey !== 'F9_Roof' && clusterKey !== 'F10_UpperRoof' && clusterKey !== 'B2_Reservoir') {{
        const midY = 0.5 * (y0 + y1);
        addBox('CoreStairsElev', 'Int_StairStep', 6.00, midY - 0.14, 15.65, 8.20, midY, 16.95, `F${{floorIdx}}_Stair_Landing`);
        addSlopedSlabN('CoreStairsElev', 'Int_StairStep', 6.00, 7.02, 13.45, y0, 15.65, midY, 0.14, `F${{floorIdx}}_Stair_Flight1`);
        addSlopedSlabN('CoreStairsElev', 'Int_StairStep', 7.18, 8.20, 15.65, midY, 13.45, y1, 0.14, `F${{floorIdx}}_Stair_Flight2`);
      }}

      // 3. All Unified DWG Wall Rectangles (`A-WALL-PATT`)
      for (let i = 0; i < c.walls.length; i++) {{
        const [x0, x1, n0, n1] = c.walls[i];
        const [layer, matKey] = classifyDwgWall(clusterKey, x0, x1, n0, n1);
        let wallTop = wt;
        if (clusterKey === 'F9_Roof') {{
          // Staircase walls go up to +32.40m, elevator walls to +31.30m, perimeter parapet to +31.40m
          if (x0 >= 5.5 && x1 <= 8.6 && n0 >= 13.0 && n1 <= 18.2) wallTop = 32.25;
          else if (x0 >= 5.5 && x1 <= 8.6 && n0 >= 8.0 && n1 <= 13.3) wallTop = 31.20;
          else wallTop = 31.40;
        }}
        addBox(layer, matKey, x0, y0, n0, x1, wallTop, n1, `${{clusterKey}}_Wall_${{i}}`);
      }}

      // 4. Structural Columns (`S-COLS`)
      for (let i = 0; i < c.cols.length; i++) {{
        const [x0, x1, n0, n1, isRound] = c.cols[i];
        const layer = clusterKey.startsWith('B') ? 'Basements' : 'MainStructure';
        const matKey = clusterKey.startsWith('B') ? 'Sub_Concrete' : 'B_WhitePanel';
        addBox(layer, matKey, x0, y0, n0, x1, wt, n1, `${{clusterKey}}_Col_${{i}}`);
      }}

      // 5. Windows, Vitrines, Curtain Walls & Under-Window/Over-Window Wall Sills/Lintels (`A-GLAZ-HDLN`, `A-GLAZ`, `A-GLAZ-CURT`)
      for (let i = 0; i < c.windows.length; i++) {{
        const [x0, x1, n0, n1, sill, head, axis, panels, wtype] = c.windows[i];
        const wy0 = y0 + sill;
        const wy1 = Math.min(wt, y0 + head);
        if (wtype !== 2) {{
          // Fill under-window sill wall & over-window lintel wall so exterior walls are 100% watertight
          const wallMat = (wtype === 1) ? 'Int_MamadWall' : (wtype === 3 ? 'Int_Partition' : 'E_LightStucco');
          const wallLay = (wtype === 1 || wtype === 3) ? 'InteriorWalls' : 'MainStructure';
          if (sill > 0.02) {{
            addBox(wallLay, wallMat, x0, y0, n0, x1, wy0, n1, `${{clusterKey}}_WinSill_${{i}}`);
          }}
          if (wy1 < wt - 0.02) {{
            addBox(wallLay, wallMat, x0, wy1, n0, x1, wt, n1, `${{clusterKey}}_WinLintel_${{i}}`);
          }}
        }}
        addGlazedOpening(x0, wy0, n0, x1, wy1, n1, axis, panels, `${{clusterKey}}_Win_${{i}}`);
      }}

      // 6. Doors: 3D Wooden Door Frames (`Int_DoorFrame`) + Over-Door Wall Lintels (`A-DOOR`)
      for (let i = 0; i < c.doors.length; i++) {{
        const [insX, insN, wM, hM, axis] = c.doors[i];
        const dh = Math.min(hM, wt - y0 - 0.12);
        const halfW = 0.5 * wM;
        const dx0 = (axis === 'X') ? (insX - halfW) : (insX - 0.07);
        const dx1 = (axis === 'X') ? (insX + halfW) : (insX + 0.07);
        const dn0 = (axis === 'N') ? (insN - halfW) : (insN - 0.07);
        const dn1 = (axis === 'N') ? (insN + halfW) : (insN + 0.07);
        const jt = 0.04;
        if (axis === 'X') {{
          addBox('InteriorWalls', 'Int_DoorFrame', dx0, y0, dn0, dx0 + jt, y0 + dh, dn1, `${{clusterKey}}_DoorJamb1_${{i}}`);
          addBox('InteriorWalls', 'Int_DoorFrame', dx1 - jt, y0, dn0, dx1, y0 + dh, dn1, `${{clusterKey}}_DoorJamb2_${{i}}`);
        }} else {{
          addBox('InteriorWalls', 'Int_DoorFrame', dx0, y0, dn0, dx1, y0 + dh, dn0 + jt, `${{clusterKey}}_DoorJamb1_${{i}}`);
          addBox('InteriorWalls', 'Int_DoorFrame', dx0, y0, dn1 - jt, dx1, y0 + dh, dn1, `${{clusterKey}}_DoorJamb2_${{i}}`);
        }}
        addBox('InteriorWalls', 'Int_DoorFrame', dx0, y0 + dh - jt, dn0, dx1, y0 + dh, dn1, `${{clusterKey}}_DoorHead_${{i}}`);
        if (y0 + dh < wt - 0.02 && !clusterKey.startsWith('B')) {{
          addBox('InteriorWalls', 'Int_Partition', dx0, y0 + dh, dn0, dx1, wt, dn1, `${{clusterKey}}_DoorLintel_${{i}}`);
        }}
      }}

      // 7. Light-Wood Kitchen Cabinets, Kitchen Islands & Bedroom Wardrobes (`Q-CASE` + `ארון` in `I-FURN`)
      if (clusterKey !== 'F9_Roof' && clusterKey !== 'F10_UpperRoof') {{
        for (let i = 0; i < c.wood_boxes.length; i++) {{
          const [x0, x1, n0, n1] = c.wood_boxes[i];
          addBox('FloorPlanCAD', 'Int_LightWood', x0, yWood, n0, x1, yWood + 0.018, n1, `${{clusterKey}}_LightWood_${{i}}`);
        }}
      }}

      // 8. Balcony & Staircase Railings (`A-FLOR-HRAL`)
      for (let i = 0; i < c.railings.length; i++) {{
        const [x0, x1, n0, n1] = c.railings[i];
        // Balcony perimeter glass railings
        if (n0 <= 0.10 || n1 >= 29.00) {{
          const rt = 0.06;
          if (n1 <= 1.20) {{
            // South balcony front + side railings
            addGlassRailing(x0, y0, n0, x1, y0 + 1.08, n0 + rt, `${{clusterKey}}_BalcRailS_${{i}}`);
            addGlassRailing(x0, y0, n0, x0 + rt, y0 + 1.08, n1, `${{clusterKey}}_BalcRailSW_${{i}}`);
            addGlassRailing(x1 - rt, y0, n0, x1, y0 + 1.08, n1, `${{clusterKey}}_BalcRailSE_${{i}}`);
          }} else if (n0 >= 28.90 && clusterKey !== 'F0_Ground') {{
            // North balcony front + side railings
            addGlassRailing(x0, y0, n1 - rt, x1, y0 + 1.08, n1, `${{clusterKey}}_BalcRailN_${{i}}`);
            addGlassRailing(x0, y0, n0, x0 + rt, y0 + 1.08, n1, `${{clusterKey}}_BalcRailNW_${{i}}`);
            addGlassRailing(x1 - rt, y0, n0, x1, y0 + 1.08, n1, `${{clusterKey}}_BalcRailNE_${{i}}`);
          }}
        }}
      }}

      // 9. Exterior Dark Aluminum Window Cladding Frames (`גליף חיפוי אלומיניום`), Balcony Beams & Roof Solar Collectors
      for (let i = 0; i < c.cladding.length; i++) {{
        const [x0, x1, n0, n1, ctype] = c.cladding[i];
        if (ctype === 'dark_frame') {{
          if (clusterKey !== 'F9_Roof' && clusterKey !== 'F10_UpperRoof') {{
            addBox('MainStructure', 'C_DarkPanel', x0, y0 + 0.70, n0, x1, y0 + 2.35, n1, `${{clusterKey}}_AluFrame_${{i}}`);
          }}
        }} else if (ctype === 'balc_beam') {{
          if (clusterKey !== 'F9_Roof' && clusterKey !== 'F10_UpperRoof') {{
            addBox('BalconiesRailings', 'C_DarkPanel', x0, y0 - 0.30, n0, x1, y0 - 0.04, n0 + 0.14, `${{clusterKey}}_BalcBeam_${{i}}`);
          }}
        }} else if (ctype === 'solar') {{
          if (clusterKey === 'F9_Roof') {{
            addSlopedSlabN('RoofParapets', 'A_Glass', x0, x1, n0, y0 + 0.15, n1, y0 + 0.85, 0.06, `${{clusterKey}}_Solar_${{i}}`);
          }}
        }}
      }}

      // East & West Service Shaft Aluminum Louver Screens (`מסתור כביסה למעבה ודוד`)
      if (!clusterKey.startsWith('B') && clusterKey !== 'F9_Roof' && clusterKey !== 'F10_UpperRoof') {{
        addLouverScreen(-0.02, y0, 10.75, 0.12, wt, 13.45, `${{clusterKey}}_West_ServiceLouver_S`);
        addLouverScreen(12.61, y0, 10.75, 12.75, wt, 13.45, `${{clusterKey}}_East_ServiceLouver_S`);
        if (clusterKey !== 'F0_Ground' && clusterKey !== 'F8_Penthouse') {{
          addLouverScreen(-0.02, y0, 24.45, 0.12, wt, 27.15, `${{clusterKey}}_West_ServiceLouver_N`);
        }}
      }}

      // 10. 2D CAD Floor Plan Lines (Doors, Light-Wood Kitchens/Wardrobes, Living/Beds/Parking Furniture, Sanitary Fixtures, Elevators & Stairs)
      for (const [x1, n1, x2, n2] of c.cad_door)   addCADLine(cy, x1, n1, x2, n2, COL_DOOR);
      for (const [x1, n1, x2, n2] of c.cad_wood)   addCADLine(cy, x1, n1, x2, n2, COL_WOOD);
      for (const [x1, n1, x2, n2] of c.cad_furn)   addCADLine(cy, x1, n1, x2, n2, COL_FURN);
      for (const [x1, n1, x2, n2] of c.cad_bath)   addCADLine(cy, x1, n1, x2, n2, COL_BATH);
      for (const [x1, n1, x2, n2] of c.cad_elev)   addCADLine(cy, x1, n1, x2, n2, COL_ELEV);
      for (const [x1, n1, x2, n2] of c.cad_stairs) addCADLine(cy, x1, n1, x2, n2, COL_ELEV);

      // 11. Floor-Drawn Room Names & Centimeter Dimensions (`ס"מ × ס"מ`)
      addDwgFloorLabels(floorIdx, y0, clusterKey);
    }}

    function buildKKL10Model() {{
      meshes.length = 0;
      cadPlanLines.length = 0;
      const slabT = 0.30;

      // SITE LOT & KKL STREET DATUM
      addBox('SiteDatum', 'Site_Ground', -3.60, -0.06, -4.60, 16.25, -0.01, 36.11, 'Site_Lot_862sqm');
      addBox('SiteDatum', 'Site_Road',   -7.00, -0.12, 36.11, 20.00, -0.01, 43.00, 'KKL_Street_North');

      // B2 WATER RESERVOIR & PUMP ROOM SUB-PIT (-8.82m to -7.65m)
      renderDwgClusterFloor(-2, 'B2_Reservoir', -8.82, -7.65, 0.20);

      // BASEMENT -2 (-7.65m to -4.35m: 16 Parking Stalls #16-#31 + 10 Storage Rooms + Pump Room + Water Tank)
      renderDwgClusterFloor(-2, 'B2_Basement2', -7.65, -4.35, 0.30);

      // BASEMENT -1 (-4.35m to 0.00m: 15 Parking Stalls #1-#15 + 10 Storage Rooms)
      renderDwgClusterFloor(-1, 'B1_Basement1', -4.35, 0.00, 0.35);

      // GROUND FLOOR (0.00m to +4.20m: Garden Apts G-1 & G-2, Main Entrance Lobby, Stroller/Bike Room, Refuse & Gas Rooms)
      renderDwgClusterFloor(0, 'F0_Ground', 0.00, 4.20, slabT);

      // FLOORS 1 & 2 (+4.20m, +7.35m: Apts B, A, C with full-width 23m² North Balcony)
      renderDwgClusterFloor(1, 'F1_2_Typical', 4.20, 7.35, slabT);
      renderDwgClusterFloor(2, 'F1_2_Typical', 7.35, 10.50, slabT);

      // FLOORS 3 & 4 (+10.50m, +13.65m: Apts B, E, D)
      renderDwgClusterFloor(3, 'F3_4_Typical', 10.50, 13.65, slabT);
      renderDwgClusterFloor(4, 'F3_4_Typical', 13.65, 16.80, slabT);

      // FLOOR 5 (+16.80m: Apts B, F, G)
      renderDwgClusterFloor(5, 'F5_Floor5', 16.80, 19.95, slabT);

      // FLOORS 6 & 7 (+19.95m, +23.10m: Apts B, A, H)
      renderDwgClusterFloor(6, 'F6_7_Floors67', 19.95, 23.10, slabT);
      renderDwgClusterFloor(7, 'F6_7_Floors67', 23.10, 26.50, slabT);

      // FLOOR 8 PENTHOUSES (+26.50m to +29.90m: PH-2 South 4rm 133.45m² + 29.90m² & PH-1 North 5rm 159.45m² + 44.30m²)
      renderDwgClusterFloor(8, 'F8_Penthouse', 26.50, 29.90, slabT);

      // TECHNICAL ROOF & UPPER ROOF (+29.90m to +31.40m / +32.40m: Parapets, Solar Collectors, Generator, Bulkhead)
      renderDwgClusterFloor(9, 'F9_Roof', 29.90, 31.40, 0.20);

      document.getElementById('statsText').textContent =
        `BIM Elements: ${{meshes.length}} Solids | ${{cadPlanLines.length}} DWG 2D CAD Lines | Official Gramoshka DWG v7.0`;
    }}
"""

with open(viewer_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace KKL10_UNITS line
u_start = html.find('    const KKL10_UNITS = [')
u_end   = html.find('\n', u_start)
assert u_start != -1 and u_end != -1, "Could not find KKL10_UNITS line"
html = html[:u_start] + new_units_str + html[u_end:]

# 2. Update FLOOR_LEVELS descriptions for B1/B2 (15 + 16 = 31 parking stalls, 10 storage rooms each)
html = html.replace(
    "{ idx: -2, id: 'B2', name: 'Basement -2 (18 Park + 6 Stor)', heb: 'מרתף 2-', y: -7.65, h: 3.30 }",
    "{ idx: -2, id: 'B2', name: 'Basement -2 (16 Park + 10 Stor + Tank)', heb: 'מרתף 2-', y: -7.65, h: 3.30 }"
).replace(
    "{ idx: -1, id: 'B1', name: 'Basement -1 (16 Park + 8 Stor)', heb: 'מרתף 1-', y: -4.35, h: 4.35 }",
    "{ idx: -1, id: 'B1', name: 'Basement -1 (15 Park + 10 Stor)', heb: 'מרתף 1-', y: -4.35, h: 4.35 }"
)

# 3. Replace old procedural builders (from `// WATERTIGHT INTERIOR APARTMENT & CORE BUILDERS` through the end of `buildKKL10Model()`)
b_start = html.find('    // WATERTIGHT INTERIOR APARTMENT & CORE BUILDERS')
if b_start == -1:
    b_start = html.find('    // OFFICIAL AUTOCAD DWG-COMPILED 3D BIM & 2D FLOOR CAD ARCHITECTURE')
b_end_marker = '    function addGlazedOpening(x0, y0, n0, x1, y1, n1, normalAxis, numPanels, tag) {'
b_end = html.find(b_end_marker)
assert b_start != -1 and b_end != -1, f"Could not find builder markers: b_start={b_start}, b_end={b_end}"

html = html[:b_start] + dwg_builder_js.lstrip('\n') + '\n' + html[b_end:]

with open(viewer_path, 'w', encoding='utf-8') as f:
    f.write(html)
shutil.copyfile(viewer_path, index_path)
shutil.copyfile(viewer_path, scratch_viewer_path)
print("Successfully updated kkl10_3d_bim_viewer.html, index.html, and scratch copy!")
