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
        
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully parsed CAD data into {output_json_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        parse_multi_apartment_cad(sys.argv[1], "extracted_project.json")
    else:
        print("Usage: python cad_parser.py <path_to_file.dxf>")
