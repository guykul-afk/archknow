import sys
import json
try:
    import ezdxf
except ImportError:
    print("Please install ezdxf: pip install ezdxf")
    sys.exit(1)

def parse_cad_to_json(dxf_filepath, output_json_path):
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
    
    # Define expected CAD layer standards
    ROOM_POLY_LAYER = "ROOM_POLYGONS"
    ROOM_TEXT_LAYER = "ROOM_LABELS"
    
    apartment_data = {
        "project_name": dxf_filepath.split("/")[-1],
        "global_parameters": {
            "ceiling_height_m": 2.7 # Default assumption if not in CAD
        },
        "rooms": [],
        "accessibility": {
            "main_entrance_width_cm": 90, # Default assumption
            "has_ramp": True
        }
    }
    
    # Step 1: Find Room Polylines
    # We look for closed LWPOLYLINE entities on the ROOM_POLY_LAYER
    polylines = msp.query(f"LWPOLYLINE[layer=='{ROOM_POLY_LAYER}']")
    
    room_count = 1
    for poly in polylines:
        points = list(poly.get_points('xy'))
        if len(points) < 3:
            continue
            
        # Shoelace formula for area
        area = 0.0
        n = len(points)
        for i in range(n):
            j = (i + 1) % n
            area += points[i][0] * points[j][1]
            area -= points[j][0] * points[i][1]
        area = abs(area) / 2.0
        
        # Step 2: Find the label inside this polyline (Simplified spatial check)
        # In a real app, we use ray-casting or bounding boxes. Here we just mock assigning the first text.
        room_name = f"Room_{room_count}"
        room_type = "bedroom" # Default fallback
        
        apartment_data["rooms"].append({
            "id": f"R{room_count}",
            "type": room_type,
            "name": room_name,
            "area_sqm": round(area, 2),
            "has_window": True,  # Would be extracted from WINDOW layer blocks
            "door_width_cm": 80  # Would be extracted from DOOR layer blocks
        })
        room_count += 1
            
    # If the file was empty or didn't follow our layers, let's output a warning
    if not apartment_data["rooms"]:
        print(f"WARNING: No closed polylines found on layer '{ROOM_POLY_LAYER}'.")
        print("Ensure the CAD file is organized according to the required layer standards.")
        
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(apartment_data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully parsed CAD data into {output_json_path}")
    print(json.dumps(apartment_data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        parse_cad_to_json(sys.argv[1], "extracted_apartment.json")
    else:
        print("Usage: python cad_parser.py <path_to_file.dxf>")
