import sys
import json
try:
    import ezdxf
except ImportError:
    print("Please install ezdxf: pip install ezdxf")
    sys.exit(1)

def point_in_polygon(point, poly_points):
    """Ray casting algorithm to determine if point is inside a polygon."""
    x, y = point[0], point[1]
    inside = False
    n = len(poly_points)
    if n == 0:
        return False
    p1x, p1y = poly_points[0][:2]
    for i in range(n + 1):
        p2x, p2y = poly_points[i % n][:2]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def get_poly_area(points):
    """Calculate area of a polygon using the shoelace formula."""
    area = 0.0
    n = len(points)
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    return abs(area) / 2.0

def parse_multi_apartment_cad(dxf_filepath, output_json_path):
    print(f"Loading CAD file: {dxf_filepath}")
    
    try:
        doc = ezdxf.readfile(dxf_filepath)
    except IOError:
        print(f"Not a valid DXF file or read error: {dxf_filepath}")
        return
    except ezdxf.DXFStructureError:
        print(f"Invalid or corrupted DXF file: {dxf_filepath}")
        return

    msp = doc.modelspace()
    
    project_data = {
        "project_name": dxf_filepath.split("/")[-1],
        "floors": []
    }
    
    # 1. Find Floor Titles
    floor_titles = list(msp.query(f"TEXT[layer=='A-TITLE']"))
    
    # We will assume that any geometry within +/- 5000 units in X of the floor title belongs to that floor.
    # In a real system, we'd use bounding box clustering.
    
    all_apt_boundaries = list(msp.query(f"LWPOLYLINE[layer=='A-AREA-APT']"))
    all_rooms = list(msp.query(f"LWPOLYLINE[layer=='A-WALL']"))
    all_texts = list(msp.query(f"TEXT[layer=='A-TEXT']"))
    
    for title_ent in floor_titles:
        floor_name = title_ent.dxf.text
        title_x = title_ent.dxf.insert[0]
        
        print(f"Found floor: {floor_name}")
        if "חניון" in floor_name or "מרתף" in floor_name:
            print(f"  -> Skipping non-residential floor: {floor_name}")
            continue
            
        floor_data = {
            "floor_name": floor_name,
            "apartments": []
        }
        
        # Find apartments belonging to this floor (based on X proximity to floor title)
        floor_apts = []
        for apt_poly in all_apt_boundaries:
            pts = list(apt_poly.get_points('xy'))
            if pts:
                center_x = sum(p[0] for p in pts) / len(pts)
                if abs(center_x - title_x) < 8000:
                    floor_apts.append((apt_poly, pts))
                    
        for apt_poly, apt_pts in floor_apts:
            # Find texts inside the apartment boundary to identify the apartment name
            apt_name = "דירה לא ידועה"
            for t in all_texts:
                if t.dxf.height >= 30 and point_in_polygon(t.dxf.insert, apt_pts):
                    apt_name = t.dxf.text
                    break
            
            print(f"  -> Found apartment: {apt_name}")
            
            apartment_data = {
                "apartment_id": apt_name,
                "global_parameters": {"ceiling_height_m": 2.7},
                "rooms": [],
                "accessibility": {"main_entrance_width_cm": 90, "has_ramp": True},
                "topology": [] # Simplified for now
            }
            
            # Find rooms inside this apartment boundary
            room_count = 1
            for room_poly in all_rooms:
                r_pts = list(room_poly.get_points('xy'))
                if not r_pts: continue
                # check if room center is inside apt boundary
                r_center_x = sum(p[0] for p in r_pts) / len(r_pts)
                r_center_y = sum(p[1] for p in r_pts) / len(r_pts)
                
                if point_in_polygon((r_center_x, r_center_y), apt_pts):
                    # Found a room inside the apartment!
                    room_area = get_poly_area(r_pts)
                    
                    # Find a text inside the room for its name
                    room_name = f"חדר {room_count}"
                    for t in all_texts:
                        if t.dxf.height < 30 and point_in_polygon(t.dxf.insert, r_pts):
                            room_name = t.dxf.text
                            break
                    
                    # Determine basic type
                    r_type = "bedroom"
                    if "סלון" in room_name: r_type = "living_room"
                    if "מטבח" in room_name: r_type = "kitchen"
                    if "רחצה" in room_name: r_type = "bathroom"
                    
                    apartment_data["rooms"].append({
                        "id": f"R{room_count}",
                        "type": r_type,
                        "name": room_name,
                        "area_sqm": round(room_area / 10000.0, 2), # convert from cm^2 or similar to sqm assumption
                        "has_window": True,
                        "door_width_cm": 80
                    })
                    room_count += 1
            
            # Basic topological connections (just connecting living room to everything for mock)
            lr_id = next((r["id"] for r in apartment_data["rooms"] if r["type"] == "living_room"), None)
            if lr_id:
                for r in apartment_data["rooms"]:
                    if r["id"] != lr_id:
                        apartment_data["topology"].append({"source": lr_id, "target": r["id"], "type": "door", "width_cm": 80})
                        
            floor_data["apartments"].append(apartment_data)
            
        project_data["floors"].append(floor_data)
        
    if not project_data["floors"]:
        print("No A-TITLE layers found. Initiating PURE GEOMETRIC PARSING using Shapely.")
        try:
            from shapely.geometry import LineString, Point
            from shapely.ops import polygonize
            
            lines = []
            count = 0
            # Collect lines and polylines up to a limit to avoid server crash on huge files
            for pl in msp.query('POLYLINE LWPOLYLINE')[:50000]:
                if pl.dxftype() == 'LWPOLYLINE':
                    pts = list(pl.get_points('xy'))
                    if len(pts) > 1:
                        lines.append(LineString([(p[0], p[1]) for p in pts]))
                else:
                    pts = [v.dxf.location for v in pl.vertices]
                    if len(pts) > 1:
                        lines.append(LineString([(p[0], p[1]) for p in pts]))
            
            for ln in msp.query('LINE')[:10000]:
                lines.append(LineString([(ln.dxf.start.x, ln.dxf.start.y), (ln.dxf.end.x, ln.dxf.end.y)]))
                
            print(f"Extracted {len(lines)} geometric lines. Polygonizing...")
            polygons = list(polygonize(lines))
            print(f"Found {len(polygons)} closed geometric polygons.")
            
            if polygons:
                areas = [p.area for p in polygons]
                areas.sort()
                median_area = areas[len(areas)//2]
                unit_factor = 10000.0 if median_area > 10000 else 1.0
                
                # Filter logical room sizes and eliminate shafts
                valid_rooms = []
                for p in polygons:
                    area_sqm = p.area / unit_factor
                    if area_sqm < 1.0 or area_sqm > 200.0:
                        continue # Ignore very small (shafts) or huge (outlines)
                    
                    minx, miny, maxx, maxy = p.bounds
                    width = maxx - minx
                    height = maxy - miny
                    if width == 0 or height == 0:
                        continue
                    
                    aspect_ratio = max(width/height, height/width)
                    if aspect_ratio > 5.0 and area_sqm < 3.0:
                        continue # Likely a shaft or wall artifact
                        
                    valid_rooms.append(p)
                
                valid_rooms = sorted(valid_rooms, key=lambda x: x.area, reverse=True)[:20] # Top 20 rooms
                
                # Extract texts and arcs for name and door detection
                texts = list(msp.query('TEXT MTEXT'))
                arcs = list(msp.query('ARC'))
                
                floor_data = {"floor_name": "קומה מחולצת גיאומטרית (Shapely)", "apartments": []}
                apartment_data = {
                    "apartment_id": "דירה גיאומטרית",
                    "global_parameters": {"ceiling_height_m": 2.7},
                    "rooms": [],
                    "accessibility": {"main_entrance_width_cm": 90, "has_ramp": True},
                    "topology": []
                }
                
                for i, p in enumerate(valid_rooms):
                    name = f"חדר {i}"
                    room_type = "bedroom"
                    
                    for t in texts:
                        txt_pt = Point(t.dxf.insert[0], t.dxf.insert[1])
                        if p.contains(txt_pt):
                            text_val = t.dxf.text if t.dxftype() == 'TEXT' else t.text
                            if text_val:
                                name = text_val.strip()
                                break
                    
                    if "סלון" in name or "מגורים" in name or "Living" in name:
                        room_type = "living_room"
                    elif "רחצה" in name or "שירותים" in name or "מקלחת" in name or "Bath" in name:
                        room_type = "bathroom"
                    elif "מטבח" in name or "Kitchen" in name:
                        room_type = "kitchen"
                    elif "מרפסת" in name or "Balcony" in name:
                        room_type = "balcony"
                    elif "ממ\"ד" in name or "שינה" in name or "חדר" in name:
                        room_type = "bedroom"
                        
                    # Fallback for i=0 if no text matched
                    if room_type == "bedroom" and name == f"חדר {i}" and i == 0:
                        room_type = "living_room"
                        name = "סלון"
                    
                    apartment_data["rooms"].append({
                        "id": f"R{i}",
                        "type": room_type,
                        "name": name,
                        "area_sqm": round(p.area / unit_factor, 2),
                        "has_window": True,
                        "door_width_cm": 80
                    })
                
                if len(apartment_data["rooms"]) > 1:
                    room_polys = {f"R{i}": valid_rooms[i] for i in range(len(valid_rooms))}
                    
                    # Check arcs for doors connecting rooms
                    for arc in arcs:
                        arc_pt = Point(arc.dxf.center[0], arc.dxf.center[1])
                        connected_rooms = []
                        for r_id, r_poly in room_polys.items():
                            # If arc center is near the room boundary
                            if r_poly.distance(arc_pt) < 100.0:
                                connected_rooms.append(r_id)
                        
                        if len(connected_rooms) == 2:
                            r1, r2 = connected_rooms[0], connected_rooms[1]
                            radius = arc.dxf.radius
                            
                            # Avoid duplicates
                            exists = any(t["source"] == r1 and t["target"] == r2 for t in apartment_data["topology"]) or \
                                     any(t["source"] == r2 and t["target"] == r1 for t in apartment_data["topology"])
                            
                            if not exists:
                                apartment_data["topology"].append({
                                    "source": r1,
                                    "target": r2,
                                    "type": "door",
                                    "width_cm": round(radius / (100 if unit_factor > 1 else 1)) if radius > 100 else round(radius)
                                })
                    
                    # Fallback topology if none or very few doors found
                    if len(apartment_data["topology"]) < len(apartment_data["rooms"]) - 1:
                        # Find the living room ID
                        lr_id = next((r["id"] for r in apartment_data["rooms"] if r["type"] == "living_room"), "R0")
                        existing_links = set()
                        for t in apartment_data["topology"]:
                            existing_links.add((t["source"], t["target"]))
                            existing_links.add((t["target"], t["source"]))
                            
                        for i in range(len(apartment_data["rooms"])):
                            r_id = f"R{i}"
                            if r_id != lr_id and (lr_id, r_id) not in existing_links:
                                apartment_data["topology"].append({
                                    "source": lr_id,
                                    "target": r_id,
                                    "type": "door",
                                    "width_cm": 80
                                })
                    
                floor_data["apartments"].append(apartment_data)
                project_data["floors"].append(floor_data)
            else:
                raise ValueError("האנליזה הגיאומטרית נכשלה: לא נמצאו פוליגונים סגורים שיוצרים חדרים בשרטוט.")
                
        except ImportError:
            print("Shapely not installed. Cannot perform geometric parsing.")
            raise ValueError("חסרות חבילות לניתוח גיאומטרי. נא להתקין shapely.")
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully parsed CAD data into {output_json_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        parse_multi_apartment_cad(sys.argv[1], "extracted_project.json")
    else:
        print("Usage: python cad_parser.py <path_to_file.dxf>")
