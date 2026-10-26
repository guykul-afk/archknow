import sys
import os
import json
import numpy as np
import fitz  # PyMuPDF
import scipy.ndimage as ndimage
from collections import Counter

try:
    from semantic_labeler import classify_room
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from semantic_labeler import classify_room

def fix_hebrew_text(text):
    if not text:
        return ""
    has_hebrew = any(0x0590 <= ord(c) <= 0x05FF for c in text)
    if has_hebrew:
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

def parse_pdf_plan(pdf_filepath, output_json_path, file_hash, preview_dir=None, use_vision=True) -> dict:
    """Smart PDF analysis (plan_analyzer: skill-based reading + 2D model + QA).
    Falls back to the legacy morphological parser if the new pipeline fails.
    Writes the project JSON to `output_json_path` and returns it."""
    work_dir = os.path.dirname(output_json_path) or "."
    try:
        from plan_analyzer import analyze_pdf_to_project
        project_data, _model = analyze_pdf_to_project(pdf_filepath, work_dir, file_hash,
                                                      preview_dir=preview_dir or work_dir, use_vision=use_vision)
    except Exception as e:
        print(f"[pdf_parser] plan_analyzer failed ({e}); falling back to legacy morphological parser")
        project_data = legacy_parse_pdf_plan(pdf_filepath, output_json_path, file_hash)
        project_data.setdefault("warnings", []).append(
            f"הניתוח החכם נכשל ({e}) — הופעל המפענח המורפולוגי הישן; הנתונים משוערים.")
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=2, ensure_ascii=False)
    return project_data


def legacy_parse_pdf_plan(pdf_filepath, output_json_path, file_hash) -> dict:
    print(f"Parsing PDF morphologically: {pdf_filepath}")
    
    try:
        doc = fitz.open(pdf_filepath)
        if len(doc) == 0:
            raise ValueError("הקובץ ריק או אינו תקין.")
        page = doc.load_page(0)
    except Exception as e:
        raise ValueError(f"שגיאה בטעינת קובץ ה-PDF: {str(e)}")
        
    rect = page.rect
    page_width = rect.width
    page_height = rect.height
    
    bg_dir = os.path.dirname(output_json_path) or "."
    os.makedirs(bg_dir, exist_ok=True)
    bg_filename = f"{file_hash}_page.png"
    bg_path = os.path.join(bg_dir, bg_filename)
    try:
        pix = page.get_pixmap(dpi=150)
        pix.save(bg_path)
        print(f"Saved background image to {bg_path}")
    except Exception as e:
        print(f"Warning: Failed to save background image: {str(e)}")
        
    grid_scale = 0.5
    width = int(page_width * grid_scale)
    height = int(page_height * grid_scale)
    
    walls = np.zeros((height, width), dtype=bool)
    try:
        drawings = page.get_drawings()
        for draw in drawings:
            for item in draw.get("items", []):
                if item[0] == "l":
                    p1, p2 = item[1], item[2]
                    dx = p2.x - p1.x
                    dy = p2.y - p1.y
                    line_len = (dx**2 + dy**2)**0.5
                    
                    # Ignore section lines/grid lines that cross completely from one margin to the opposite margin
                    margin_x = page_width * 0.08
                    margin_y = page_height * 0.08
                    is_vertical_section = (min(p1.y, p2.y) < margin_y) and (max(p1.y, p2.y) > page_height - margin_y)
                    is_horizontal_section = (min(p1.x, p2.x) < margin_x) and (max(p1.x, p2.x) > page_width - margin_x)
                    if is_vertical_section or is_horizontal_section:
                        continue
                        
                    if line_len < 25.0:  # Ignore short lines (furniture, text vectors, hatching)
                        continue
                        
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
                    rw = abs(r.x1 - r.x0)
                    rh = abs(r.y1 - r.y0)
                    if rw < 25.0 and rh < 25.0:  # Ignore small rectangles (symbols, column details)
                        continue
                        
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
    except Exception as e:
        print(f"Warning: Failed to extract vector drawings: {str(e)}")

    # 4. Morphological Dilation to Close Doorways (80-90cm)
    struct_size = 25  # Increased to effectively close doorways and small furniture gaps (25px at 0.5 scale = 50pt = ~100cm)
    struct = np.ones((struct_size, struct_size), dtype=bool)
    thick_walls = ndimage.binary_dilation(walls, structure=struct)
    free_space = ~thick_walls
    
    # Label the disconnected cores
    labeled_cores, num_features = ndimage.label(free_space)
    
    # 5. Region Growing (Watershed expansion) back to original wall boundaries
    labels = labeled_cores.copy()
    for _ in range(50):
        dilated = ndimage.maximum_filter(labels, size=3)
        labels = np.where((labels == 0) & (~walls), dilated, labels)
        
    # 6. Identify and Filter Outside Background
    border_pixels = []
    border_pixels.extend(labels[0, :])
    border_pixels.extend(labels[-1, :])
    border_pixels.extend(labels[:, 0])
    border_pixels.extend(labels[:, -1])
    counts = Counter(border_pixels)
    outside_label = counts.most_common(1)[0][0] if counts else 0
    
    # 7. Extract Rooms and Calibrate Scale
    total_area_sqpt = 0
    raw_rooms = []
    
    for idx in range(1, num_features + 1):
        if idx == outside_label:
            continue
        ys, xs = np.where(labels == idx)
        if len(xs) < 800: # Increased threshold to filter out tiny noisy fragments (< ~1.5 sqm)
            continue
            
        area_pixels = len(xs)
        area_sqpt = area_pixels / (grid_scale ** 2)
        total_area_sqpt += area_sqpt
        
        cy, cx = np.mean(ys), np.mean(xs)
        rx = (cx / width) * 100
        ry = (cy / height) * 100
        
        w_pt = (xs.max() - xs.min()) / grid_scale
        h_pt = (ys.max() - ys.min()) / grid_scale
        
        raw_rooms.append({
            "id": idx,
            "area_sqpt": area_sqpt,
            "x_pct": rx,
            "y_pct": ry,
            "w_pt": w_pt,
            "h_pt": h_pt,
            "cx_pt": cx / grid_scale,
            "cy_pt": cy / grid_scale
        })
        
    extracted_words = page.get_text("words")
    word_mappings = {}
    
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
        sorted_words = sorted(words, key=lambda w: (w["block"], w["line"], w["x"]))
        joined = " ".join([w["text"] for w in sorted_words])
        room_texts[r_idx] = joined.strip()
        
    if total_area_sqpt > 0:
        scale = (850000.0 / total_area_sqpt) ** 0.5
        scale = np.clip(scale, 0.6, 2.2)
    else:
        scale = 1.2
        
    print(f"Auto-calibrated scale: {scale:.4f} cm/point")
    
    apartment_data = {
        "apartment_id": "דירת PDF מנותחת",
        "global_parameters": {"ceiling_height_m": 2.50},
        "rooms": [],
        "accessibility": {"main_entrance_width_cm": 80, "has_ramp": True},
        "topology": []
    }
    
    sorted_rooms = sorted(raw_rooms, key=lambda x: x["area_sqpt"], reverse=True)
    
    for i, r in enumerate(sorted_rooms):
        area_sqm = (r["area_sqpt"] * (scale ** 2)) / 10000.0
        width_cm = min(r["w_pt"], r["h_pt"]) * scale
        
        extracted_name = room_texts.get(r["id"], "")
        classified_type = classify_room(extracted_name)
        
        if classified_type != "unknown":
            room_type = classified_type
            room_name = extracted_name
        else:
            w_pt = r["w_pt"]
            h_pt = r["h_pt"]
            ratio = max(w_pt, h_pt) / min(w_pt, h_pt) if min(w_pt, h_pt) > 0 else 1.0
            
            if i == 0:
                room_type = "living_room"
                room_name = "סלון"
            elif i == len(sorted_rooms) - 1 or (i == len(sorted_rooms) - 2 and area_sqm < 4.0):
                room_type = "bathroom"
                room_name = f"חדר רחצה {len([rm for rm in apartment_data['rooms'] if rm['type'] == 'bathroom']) + 1}"
            elif i == 1 and area_sqm > 8.0:
                room_type = "kitchen"
                room_name = "מטבח"
            elif ratio > 2.5 and area_sqm < 12.0:
                room_type = "corridor"
                room_name = f"מסדרון {len([rm for rm in apartment_data['rooms'] if rm['type'] == 'corridor']) + 1}"
            elif area_sqm < 3.0:
                room_type = "utility"
                room_name = f"חדר שירות {len([rm for rm in apartment_data['rooms'] if rm['type'] == 'utility']) + 1}"
            else:
                room_type = "bedroom"
                is_mamad = len([rm for rm in apartment_data['rooms'] if rm['type'] == 'bedroom']) == 0
                room_name = "ממ\"ד" if is_mamad else f"חדר שינה {len([rm for rm in apartment_data['rooms'] if rm['type'] == 'bedroom'])}"
                
        room_type_mapped = room_type
        if room_type in ["bedroom_master", "safe_room"]:
            room_type_mapped = "bedroom"
            
        room_dict = {
            "id": f"R{i}",
            "type": room_type_mapped,
            "name": room_name,
            "area_sqm": round(area_sqm, 2),
            "width_cm": round(width_cm, 1),
            "length_cm": round(max(r["w_pt"], r["h_pt"]) * scale, 1),
            "has_window": True,
            "door_width_cm": 80,
            "x_pct": round(r["x_pct"], 1),
            "y_pct": round(r["y_pct"], 1),
            "cx_pt": r["cx_pt"],
            "cy_pt": r["cy_pt"]
        }
        
        if room_type_mapped == "bathroom":
            room_dict["has_window"] = False
            room_dict["ventilation_type"] = "none"
            
        apartment_data["rooms"].append(room_dict)
        
    for i in range(len(apartment_data["rooms"])):
        for j in range(i + 1, len(apartment_data["rooms"])):
            r1 = apartment_data["rooms"][i]
            r2 = apartment_data["rooms"][j]
            dx = r1.get("cx_pt", 0) - r2.get("cx_pt", 0)
            dy = r1.get("cy_pt", 0) - r2.get("cy_pt", 0)
            dist = (dx**2 + dy**2)**0.5
            
            if dist < 120.0:
                apartment_data["topology"].append({
                    "source": r1["id"],
                    "target": r2["id"],
                    "type": "door",
                    "width_cm": 80
                })
                
    for r in apartment_data["rooms"]:
        r.pop("cx_pt", None)
        r.pop("cy_pt", None)

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
