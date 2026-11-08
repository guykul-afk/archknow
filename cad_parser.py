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


def _classify_room_type_by_name(room_name: str, default_type: str = "bedroom") -> str:
    rn = str(room_name or "").strip()
    if any(k in rn for k in ("ממ\"ד", "ממד", "מרחב מוגן", "Safe", "Mamad")):
        return "safe_room"
    if any(k in rn for k in ("סלון", "מגורים", "דיור", "Living")):
        return "living_room"
    if any(k in rn for k in ("מטבח", "Kitchen")):
        return "kitchen"
    if any(k in rn for k in ("אוכל", "Dining")):
        return "dining"
    if any(k in rn for k in ("רחצה", "אמבטיה", "מקלחת", "Bath")):
        return "bathroom"
    if any(k in rn for k in ("שירותים", "אסלה", "WC", "Toilet")):
        return "toilet"
    if any(k in rn for k in ("מסדרון", "מעבר", "הול", "Corridor", "Hall")):
        return "corridor"
    if any(k in rn for k in ("מבואה", "כניסה", "Entrance", "Foyer")):
        return "entrance"
    if any(k in rn for k in ("מרפסת שירות", "כביסה", "שירות", "Service", "Utility")):
        return "utility"
    if any(k in rn for k in ("מרפסת", "גזוזטרה", "Balcony")):
        return "balcony"
    if any(k in rn for k in ("מחסן", "ארונות", "Storage", "Closet")):
        return "storage"
    return default_type


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
        "project_name": str(dxf_filepath).replace("\\", "/").split("/")[-1],
        "floors": [],
    }

    # 1. Find Floor Titles
    floor_titles = list(msp.query("TEXT[layer=='A-TITLE']"))

    all_apt_boundaries = list(msp.query("LWPOLYLINE[layer=='A-AREA-APT']"))
    all_rooms = list(msp.query("LWPOLYLINE[layer=='A-WALL']"))
    all_texts = list(msp.query("TEXT[layer=='A-TEXT']"))
    all_parking = (
        list(msp.query("LWPOLYLINE[layer=='A-PARK']"))
        + list(msp.query("LWPOLYLINE[layer=='PARKING']"))
    )

    for title_ent in floor_titles:
        floor_name = title_ent.dxf.text
        title_x = title_ent.dxf.insert[0]

        print(f"Found floor: {floor_name}")
        if "חניון" in floor_name or "מרתף" in floor_name:
            print(f"  -> Parsing basement / underground parking floor: {floor_name}")
            floor_stalls = []
            for p_poly in all_parking:
                pts = list(p_poly.get_points("xy"))
                if pts:
                    cx = sum(p[0] for p in pts) / len(pts)
                    if abs(cx - title_x) < 8000:
                        xs = [p[0] for p in pts]
                        ys = [p[1] for p in pts]
                        dims = sorted([max(xs) - min(xs), max(ys) - min(ys)])
                        floor_stalls.append({
                            "width_cm": round(dims[0], 1),
                            "length_cm": round(dims[1], 1),
                            "area_sqm": round(get_poly_area(pts) / 10000.0, 2),
                        })

            basement_rooms = []
            b_idx = 1
            for room_poly in all_rooms:
                r_pts = list(room_poly.get_points("xy"))
                if not r_pts:
                    continue
                rcx = sum(p[0] for p in r_pts) / len(r_pts)
                if abs(rcx - title_x) < 8000:
                    r_area = round(get_poly_area(r_pts) / 10000.0, 2)
                    r_name = f"חלל מרתף {b_idx}"
                    for t in all_texts:
                        if point_in_polygon(t.dxf.insert, r_pts):
                            r_name = t.dxf.text
                            break
                    r_xs = [p[0] for p in r_pts]
                    r_ys = [p[1] for p in r_pts]
                    dims_cm = sorted([max(r_xs) - min(r_xs), max(r_ys) - min(r_ys)])
                    basement_rooms.append({
                        "id": f"UG_R{b_idx}",
                        "type": "storage" if ("מחסן" in r_name or r_area < 15.0) else "utility",
                        "name": r_name,
                        "area_sqm": r_area,
                        "width_cm": round(dims_cm[0], 1),
                        "length_cm": round(dims_cm[1], 1),
                        "polygon": [
                            [round((p[0] - min(r_xs)) / 100.0, 3), round((p[1] - min(r_ys)) / 100.0, 3)]
                            for p in r_pts
                        ],
                    })
                    b_idx += 1

            min_stall_w_m = round(min((s["width_cm"] for s in floor_stalls), default=245.0) / 100.0, 2)
            project_data["floors"].append({
                "floor_name": floor_name,
                "floor_type": "underground_parking",
                "parking_summary": {
                    "stalls_detected": len(floor_stalls),
                    "min_stall_width_m": min_stall_w_m,
                    "stalls": floor_stalls,
                    "basement_rooms_count": len(basement_rooms),
                },
                "apartments": [{
                    "apartment_id": f"מרתף חניון ({floor_name})",
                    "is_underground_floor": True,
                    "global_parameters": {"ceiling_height_m": 2.45},
                    "parking": {
                        "stall_width_m": min_stall_w_m,
                        "aisle_width_m": 6.00,
                        "adjacent_columns_or_walls": 1,
                    },
                    "rooms": basement_rooms,
                    "topology": [],
                }] if (basement_rooms or floor_stalls) else [],
            })
            continue

        floor_data = {
            "floor_name": floor_name,
            "floor_type": "residential",
            "apartments": [],
        }

        # Find apartments belonging to this floor (based on X proximity to floor title)
        floor_apts = []
        for apt_poly in all_apt_boundaries:
            pts = list(apt_poly.get_points("xy"))
            if pts:
                center_x = sum(p[0] for p in pts) / len(pts)
                if abs(center_x - title_x) < 8000:
                    floor_apts.append((apt_poly, pts))

        for apt_poly, apt_pts in floor_apts:
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
                "topology": [],
            }

            room_count = 1
            apt_xs = [p[0] for p in apt_pts]
            apt_ys = [p[1] for p in apt_pts]
            apt_min_x, apt_max_x = min(apt_xs), max(apt_xs)
            apt_min_y, apt_max_y = min(apt_ys), max(apt_ys)
            apt_w = apt_max_x - apt_min_x
            apt_h = apt_max_y - apt_min_y

            for room_poly in all_rooms:
                r_pts = list(room_poly.get_points("xy"))
                if not r_pts:
                    continue
                r_center_x = sum(p[0] for p in r_pts) / len(r_pts)
                r_center_y = sum(p[1] for p in r_pts) / len(r_pts)

                if point_in_polygon((r_center_x, r_center_y), apt_pts):
                    room_area = get_poly_area(r_pts)
                    room_name = f"חדר {room_count}"
                    for t in all_texts:
                        if t.dxf.height < 30 and point_in_polygon(t.dxf.insert, r_pts):
                            room_name = t.dxf.text
                            break

                    r_type = _classify_room_type_by_name(room_name, default_type="bedroom")
                    r_xs = [p[0] for p in r_pts]
                    r_ys = [p[1] for p in r_pts]
                    dims_cm = sorted([max(r_xs) - min(r_xs), max(r_ys) - min(r_ys)])
                    x_pct = (r_center_x - apt_min_x) / apt_w * 100 if apt_w > 0 else 50
                    y_pct = (apt_max_y - r_center_y) / apt_h * 100 if apt_h > 0 else 50

                    room_rec = {
                        "id": f"R{room_count}",
                        "type": r_type,
                        "name": room_name,
                        "area_sqm": round(room_area / 10000.0, 2),
                        "width_cm": round(dims_cm[0], 1),
                        "length_cm": round(dims_cm[1], 1),
                        "polygon": [
                            [round((p[0] - apt_min_x) / 100.0, 3), round((p[1] - apt_min_y) / 100.0, 3)]
                            for p in r_pts
                        ],
                        "has_window": True,
                        "door_width_cm": 80,
                        "x_pct": round(x_pct, 1),
                        "y_pct": round(y_pct, 1),
                    }
                    if r_type == "balcony":
                        room_rec["depth_m"] = round(dims_cm[0] / 100.0, 2)
                    apartment_data["rooms"].append(room_rec)
                    room_count += 1

            # Topological connections
            lr_id = next((r["id"] for r in apartment_data["rooms"] if r["type"] == "living_room"), None)
            cor_id = next((r["id"] for r in apartment_data["rooms"] if r["type"] == "corridor"), None)
            if lr_id:
                apartment_data["topology"].append({"source": "EXT", "target": lr_id, "type": "door", "width_cm": 90})
                for r in apartment_data["rooms"]:
                    if r["id"] != lr_id:
                        src = cor_id if (cor_id and r["id"] != cor_id and r["type"] in ("bedroom", "safe_room", "bathroom")) else lr_id
                        apartment_data["topology"].append({"source": src, "target": r["id"], "type": "door", "width_cm": 80})

            try:
                from spatial_intelligence_engine import (
                    compute_sightline_and_aesthetics_metrics,
                    simulate_apartment_furnishability,
                    analyze_resident_livability,
                )
                apartment_data["spatial_intelligence"] = {
                    "sightlines_and_aesthetics": compute_sightline_and_aesthetics_metrics(apartment_data),
                    "furnishability_simulation": simulate_apartment_furnishability(apartment_data),
                    "resident_livability": analyze_resident_livability(apartment_data),
                }
            except Exception:
                pass

            floor_data["apartments"].append(apartment_data)

        project_data["floors"].append(floor_data)

    if not any(f.get("floor_type") != "underground_parking" for f in project_data["floors"]):
        print("No residential A-TITLE layers found. Initiating PURE GEOMETRIC PARSING using Shapely.")
        try:
            from shapely.geometry import LineString, Point
            from shapely.ops import polygonize

            lines = []
            for pl in list(msp.query("POLYLINE LWPOLYLINE"))[:50000]:
                if pl.dxftype() == "LWPOLYLINE":
                    pts = list(pl.get_points("xy"))
                    if len(pts) > 1:
                        lines.append(LineString([(p[0], p[1]) for p in pts]))
                else:
                    pts = [v.dxf.location for v in pl.vertices]
                    if len(pts) > 1:
                        lines.append(LineString([(p[0], p[1]) for p in pts]))

            for ln in list(msp.query("LINE"))[:10000]:
                lines.append(LineString([(ln.dxf.start.x, ln.dxf.start.y), (ln.dxf.end.x, ln.dxf.end.y)]))

            print(f"Extracted {len(lines)} geometric lines. Polygonizing...")
            polygons = list(polygonize(lines))
            print(f"Found {len(polygons)} closed geometric polygons.")

            if polygons:
                areas = sorted(p.area for p in polygons)
                median_area = areas[len(areas) // 2]
                unit_factor = 10000.0 if median_area > 10000 else 1.0
                linear_scale_to_cm = 1.0 if unit_factor == 10000.0 else 100.0

                valid_rooms = []
                for p in polygons:
                    area_sqm = p.area / unit_factor
                    if area_sqm < 1.0 or area_sqm > 200.0:
                        continue
                    minx, miny, maxx, maxy = p.bounds
                    w = maxx - minx
                    h = maxy - miny
                    if w == 0 or h == 0:
                        continue
                    aspect_ratio = max(w / h, h / w)
                    if aspect_ratio > 5.0 and area_sqm < 3.0:
                        continue
                    valid_rooms.append(p)

                valid_rooms = sorted(valid_rooms, key=lambda x: x.area, reverse=True)[:20]

                texts = list(msp.query("TEXT MTEXT"))
                arcs = list(msp.query("ARC"))

                all_xs, all_ys = [], []
                for p in valid_rooms:
                    minx, miny, maxx, maxy = p.bounds
                    all_xs.extend([minx, maxx])
                    all_ys.extend([miny, maxy])

                if all_xs and all_ys:
                    min_x, max_x = min(all_xs), max(all_xs)
                    min_y, max_y = min(all_ys), max(all_ys)
                    width = max_x - min_x
                    height = max_y - min_y
                else:
                    min_x, max_x, min_y, max_y, width, height = 0, 100, 0, 100, 100, 100

                floor_data = {"floor_name": "קומה מחולצת גיאומטרית (Shapely)", "floor_type": "residential", "apartments": []}
                apartment_data = {
                    "apartment_id": "דירה גיאומטרית",
                    "global_parameters": {"ceiling_height_m": 2.7},
                    "rooms": [],
                    "accessibility": {"main_entrance_width_cm": 90, "has_ramp": True},
                    "topology": [],
                }

                for i, p in enumerate(valid_rooms):
                    name = f"חדר {i}"
                    for t in texts:
                        txt_pt = Point(t.dxf.insert[0], t.dxf.insert[1])
                        if p.contains(txt_pt):
                            text_val = t.dxf.text if t.dxftype() == "TEXT" else t.text
                            if text_val:
                                name = text_val.strip()
                                break

                    room_type = _classify_room_type_by_name(name, default_type="bedroom")
                    if room_type == "bedroom" and name == f"חדר {i}" and i == 0:
                        room_type = "living_room"
                        name = "סלון"

                    centroid = p.centroid
                    x_pct = (centroid.x - min_x) / width * 100 if width > 0 else 50
                    y_pct = (max_y - centroid.y) / height * 100 if height > 0 else 50
                    p_minx, p_miny, p_maxx, p_maxy = p.bounds
                    dims_cm = sorted([
                        (p_maxx - p_minx) * linear_scale_to_cm,
                        (p_maxy - p_miny) * linear_scale_to_cm,
                    ])
                    ext_coords = list(p.exterior.coords)[:-1]
                    poly_m = [
                        [
                            round((pt[0] - min_x) * linear_scale_to_cm / 100.0, 3),
                            round((pt[1] - min_y) * linear_scale_to_cm / 100.0, 3),
                        ]
                        for pt in ext_coords
                    ]

                    apartment_data["rooms"].append({
                        "id": f"R{i}",
                        "type": room_type,
                        "name": name,
                        "area_sqm": round(p.area / unit_factor, 2),
                        "width_cm": round(dims_cm[0], 1),
                        "length_cm": round(dims_cm[1], 1),
                        "polygon": poly_m,
                        "has_window": True,
                        "door_width_cm": 80,
                        "x_pct": round(x_pct, 1),
                        "y_pct": round(y_pct, 1),
                    })

                if len(apartment_data["rooms"]) > 1:
                    room_polys = {f"R{i}": valid_rooms[i] for i in range(len(valid_rooms))}

                    for arc in arcs:
                        arc_pt = Point(arc.dxf.center[0], arc.dxf.center[1])
                        connected_rooms = []
                        for r_id, r_poly in room_polys.items():
                            if r_poly.distance(arc_pt) < 100.0:
                                connected_rooms.append(r_id)

                        if len(connected_rooms) == 2:
                            r1, r2 = connected_rooms[0], connected_rooms[1]
                            radius = arc.dxf.radius
                            exists = any(
                                (t["source"] == r1 and t["target"] == r2) or (t["source"] == r2 and t["target"] == r1)
                                for t in apartment_data["topology"]
                            )
                            if not exists:
                                apartment_data["topology"].append({
                                    "source": r1,
                                    "target": r2,
                                    "type": "door",
                                    "width_cm": round(radius / (100 if unit_factor > 1 else 1)) if radius > 100 else round(radius),
                                })

                    if len(apartment_data["topology"]) < len(apartment_data["rooms"]) - 1:
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
                                    "width_cm": 80,
                                })

                try:
                    from spatial_intelligence_engine import (
                        compute_sightline_and_aesthetics_metrics,
                        simulate_apartment_furnishability,
                        analyze_resident_livability,
                    )
                    apartment_data["spatial_intelligence"] = {
                        "sightlines_and_aesthetics": compute_sightline_and_aesthetics_metrics(apartment_data),
                        "furnishability_simulation": simulate_apartment_furnishability(apartment_data),
                        "resident_livability": analyze_resident_livability(apartment_data),
                    }
                except Exception:
                    pass

                floor_data["apartments"].append(apartment_data)
                project_data["floors"].append(floor_data)
            else:
                raise ValueError("האנליזה הגיאומטרית נכשלה: לא נמצאו פוליגונים סגורים שיוצרים חדרים בשרטוט.")

        except ImportError:
            print("Shapely not installed. Cannot perform geometric parsing.")
            raise ValueError("חסרות חבילות לניתוח גיאומטרי. נא להתקין shapely.")

    try:
        from spatial_intelligence_engine import audit_multi_floor_vertical_stack
        project_data["vertical_stack_audit"] = audit_multi_floor_vertical_stack(project_data["floors"])
    except Exception:
        pass

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=2, ensure_ascii=False)

    print(f"Successfully parsed CAD data into {output_json_path}")
    return project_data


if __name__ == "__main__":
    if len(sys.argv) > 1:
        parse_multi_apartment_cad(sys.argv[1], "extracted_project.json")
    else:
        print("Usage: python cad_parser.py <path_to_file.dxf>")
