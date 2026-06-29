import sys
import os
import json
import numpy as np
import scipy.ndimage as ndimage
from collections import Counter
import fitz  # PyMuPDF

def parse_pdf_plan(pdf_filepath, output_json_path, file_hash):
    print(f"Parsing PDF morphologically: {pdf_filepath}")
    doc = fitz.open(pdf_filepath)
    if len(doc) == 0:
        raise ValueError("הקובץ ריק או אינו תקין.")
        
    page = doc.load_page(0)
    rect = page.rect
    page_width = rect.width
    page_height = rect.height
    
    # 1. Export Page Background Image
    os.makedirs("webapp/uploads", exist_ok=True)
    bg_filename = f"{file_hash}_page.png"
    bg_path = os.path.join("webapp/uploads", bg_filename)
    pix = page.get_pixmap(dpi=150)
    pix.save(bg_path)
    print(f"Saved background image to {bg_path}")
    
    # 2. Render drawings onto a grid for morphological analysis
    # grid_scale = 0.5 means 1 point on PDF = 2 pixels on grid (to keep it fast and accurate)
    grid_scale = 0.5
    width = int(page_width * grid_scale)
    height = int(page_height * grid_scale)
    
    walls = np.zeros((height, width), dtype=bool)
    drawings = page.get_drawings()
    
    for draw in drawings:
        for item in draw.get("items", []):
            if item[0] == "l":
                p1, p2 = item[1], item[2]
                x1, y1 = int(p1.x * grid_scale), int(p1.y * grid_scale)
                x2, y2 = int(p2.x * grid_scale), int(p2.y * grid_scale)
                x1, x2 = np.clip([x1, x2], 0, width - 1)
                y1, y2 = np.clip([y1, y2], 0, height - 1)
                num_pts = max(abs(x2 - x1), abs(y2 - y1)) + 1
                xs = np.linspace(x1, x2, num_pts).astype(int)
                ys = np.linspace(y1, y2, num_pts).astype(int)
                walls[ys, xs] = True
            elif item[0] == "re":
                r = item[1]
                x0 = int(r.x0 * grid_scale)
                y0 = int(r.y0 * grid_scale)
                x1 = int(r.x1 * grid_scale)
                y1 = int(r.y1 * grid_scale)
                x0, x1 = np.clip([x0, x1], 0, width - 1)
                y0, y1 = np.clip([y0, y1], 0, height - 1)
                walls[y0:y1+1, x0] = True
                walls[y0:y1+1, x1] = True
                walls[y0, x0:x1+1] = True
                walls[y1, x0:x1+1] = True
                
    # 3. Morphological Dilation to Close Doorways (80-90cm)
    # R=15 pixels at scale 0.5 (representing ~30pt doorway closure)
    struct_size = 15
    struct = np.ones((struct_size, struct_size), dtype=bool)
    thick_walls = ndimage.binary_dilation(walls, structure=struct)
    free_space = ~thick_walls
    
    # Label the disconnected cores
    labeled_cores, num_features = ndimage.label(free_space)
    
    # 4. Region Growing (Watershed expansion) back to original wall boundaries
    labels = labeled_cores.copy()
    for _ in range(50):
        dilated = ndimage.maximum_filter(labels, size=3)
        # Only grow into original free space (not walls) and don't overwrite other labels
        labels = np.where((labels == 0) & (~walls), dilated, labels)
        
    # 5. Identify and Filter Outside Background
    border_pixels = []
    border_pixels.extend(labels[0, :])
    border_pixels.extend(labels[-1, :])
    border_pixels.extend(labels[:, 0])
    border_pixels.extend(labels[:, -1])
    counts = Counter(border_pixels)
    outside_label = counts.most_common(1)[0][0] if counts else 0
    
    # 6. Extract Rooms and Calibrate Scale
    total_area_sqpt = 0
    raw_rooms = []
    
    for idx in range(1, num_features + 1):
        if idx == outside_label:
            continue
        ys, xs = np.where(labels == idx)
        if len(xs) < 300: # skip noise
            continue
            
        area_pixels = len(xs)
        area_sqpt = area_pixels / (grid_scale ** 2)
        total_area_sqpt += area_sqpt
        
        # Centroid
        cy, cx = np.mean(ys), np.mean(xs)
        rx = (cx / width) * 100
        ry = (cy / height) * 100
        
        # Bounding box dimensions in points
        w_pt = (xs.max() - xs.min()) / grid_scale
        h_pt = (ys.max() - ys.min()) / grid_scale
        
        raw_rooms.append({
            "id": idx,
            "area_sqpt": area_sqpt,
            "x_pct": rx,
            "y_pct": ry,
            "w_pt": w_pt,
            "h_pt": h_pt
        })
        
    # Extract PDF words and map them to room indices using the label mask
    extracted_words = page.get_text("words")
    word_mappings = {}
    
    def fix_hebrew_text(text):
        if not text:
            return ""
        has_hebrew = any(0x0590 <= ord(c) <= 0x05FF for c in text)
        if has_hebrew:
            # Reverse Hebrew sequences to fix PDF RTL export reversals
            reversed_chars = []
            current_heb = []
            for c in text:
                if 0x0590 <= ord(c) <= 0x05FF:
                    current_heb.append(c)
                else:
                    if current_heb:
                        reversed_chars.extend(reversed(current_heb))
                        current_heb = []
                    reversed_chars.append(c)
            if current_heb:
                reversed_chars.extend(reversed(current_heb))
            return "".join(reversed_chars)
        return text

    for w in extracted_words:
        x0, y0, x1, y1, word_str, block_no, line_no, word_no = w
        cx_pt = (x0 + x1) / 2.0
        cy_pt = (y0 + y1) / 2.0
        
        gx = int(cx_pt * grid_scale)
        gy = int(cy_pt * grid_scale)
        
        if 0 <= gx < width and 0 <= gy < height:
            room_idx = labels[gy, gx]
            if room_idx > 0 and room_idx != outside_label:
                if room_idx not in word_mappings:
                    word_mappings[room_idx] = []
                word_mappings[room_idx].append({
                    "text": fix_hebrew_text(word_str),
                    "x": cx_pt,
                    "y": cy_pt,
                    "line": line_no,
                    "block": block_no
                })
                
    room_texts = {}
    for r_idx, words in word_mappings.items():
        # Sort words inside the room from left to right (X coordinate)
        sorted_words = sorted(words, key=lambda w: (w["block"], w["line"], w["x"]))
        joined = " ".join([w["text"] for w in sorted_words])
        room_texts[r_idx] = joined.strip()
        
    # Calibrate Scale: total area should be around 95 sqm (950,000 sqcm)
    if total_area_sqpt > 0:
        scale = (850000.0 / total_area_sqpt) ** 0.5
        scale = np.clip(scale, 0.6, 2.2)
    else:
        scale = 1.2
        
    print(f"Auto-calibrated scale: {scale:.4f} cm/point")
    
    # 7. Semantic Classification & Output Generation
    apartment_data = {
        "apartment_id": "דירת PDF מנותחת",
        "global_parameters": {"ceiling_height_m": 2.50},
        "rooms": [],
        "accessibility": {"main_entrance_width_cm": 80, "has_ramp": True},
        "topology": []
    }
    
    # Sort rooms by area in descending order
    sorted_rooms = sorted(raw_rooms, key=lambda x: x["area_sqpt"], reverse=True)
    
    for i, r in enumerate(sorted_rooms):
        area_sqm = (r["area_sqpt"] * (scale ** 2)) / 10000.0
        width_cm = min(r["w_pt"], r["h_pt"]) * scale
        
        extracted_name = room_texts.get(r["id"], "")
        
        if extracted_name:
            room_name = extracted_name
            if "סלון" in room_name or "מגורים" in room_name or "Living" in room_name:
                room_type = "living_room"
            elif "רחצה" in room_name or "שירותים" in room_name or "מקלחת" in room_name or "Bath" in room_name:
                room_type = "bathroom"
            elif "מטבח" in room_name or "Kitchen" in room_name:
                room_type = "kitchen"
            elif "מרפסת" in room_name or "Balcony" in room_name:
                room_type = "balcony"
            else:
                room_type = "bedroom"
        else:
            if i == 0:
                room_type = "living_room"
                room_name = "סלון"
            elif i == len(sorted_rooms) - 1 or (i == len(sorted_rooms) - 2 and area_sqm < 4.0):
                room_type = "bathroom"
                room_name = f"חדר רחצה {len([rm for rm in apartment_data['rooms'] if rm['type'] == 'bathroom']) + 1}"
            elif i == 1 and area_sqm > 8.0:
                room_type = "kitchen"
                room_name = "מטבח"
            else:
                room_type = "bedroom"
                is_mamad = len([rm for rm in apartment_data['rooms'] if rm['type'] == 'bedroom']) == 0
                room_name = "ממ\"ד" if is_mamad else f"חדר שינה {len([rm for rm in apartment_data['rooms'] if rm['type'] == 'bedroom'])}"
                
        apartment_data["rooms"].append({
            "id": f"R{i}",
            "type": room_type,
            "name": room_name,
            "area_sqm": round(area_sqm, 2),
            "width_cm": round(width_cm, 1),
            "has_window": True,
            "door_width_cm": 80,
            "x_pct": round(r["x_pct"], 1),
            "y_pct": round(r["y_pct"], 1)
        })
        
    # Generate mock topology linking living room to other rooms
    lr_id = next((r["id"] for r in apartment_data["rooms"] if r["type"] == "living_room"), None)
    if lr_id:
        for r in apartment_data["rooms"]:
            if r["id"] != lr_id:
                apartment_data["topology"].append({
                    "source": lr_id,
                    "target": r["id"],
                    "type": "door",
                    "width_cm": 80
                })
                
    project_data = {
        "project_name": pdf_filepath.split("/")[-1],
        "bg_image_url": f"/uploads/{bg_filename}",
        "floors": [{
            "floor_name": "קומה מתוך PDF",
            "apartments": [apartment_data]
        }]
    }
    
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully processed PDF into {output_json_path}")
    return project_data

if __name__ == "__main__":
    if len(sys.argv) > 2:
        parse_pdf_plan(sys.argv[1], sys.argv[2], "test_hash")
    else:
        print("Usage: python pdf_parser.py <input.pdf> <output.json>")
