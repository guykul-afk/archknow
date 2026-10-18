import json
import os
import yaml

# For fallback, we map OKF rule IDs to concrete numerical thresholds.
FALLBACK_THRESHOLDS = {
    "B1.3": {"min_area_sqm": 12.0, "min_width_m": 2.60}, # Living Space Area (סלון)
    "B1.6": {"min_area_sqm": 8.0, "min_width_m": 2.60},  # Bedroom Area
    "B1.9": {"min_area_sqm": 1.8, "min_width_m": 0.90},  # Bathroom Area
    "B1.10": {"min_area_sqm": 1.1, "min_width_m": 0.80}, # Toilet Area
    "B1.11": {"min_area_sqm": 6.0, "min_width_m": 1.70}, # Kitchen Area
    "B1.13": {"min_height_m": 2.50},                     # Ceiling Height
    "B44": {"min_width_cm": 80},                         # Main Entrance
}

def get_rule_param(rules, rule_id, param, default_val):
    # Normalize IDs to handle B1.3 vs B1_3 vs b1_3
    normalized_target = rule_id.replace(".", "_").lower()
    for rule in rules:
        r_id = str(rule.get("rule_id", "")).replace(".", "_").lower()
        if r_id == normalized_target:
            if param in rule:
                try:
                    return float(rule[param])
                except (ValueError, TypeError):
                    return rule[param]
    return default_val

def load_apartment(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def load_okf_rules(rules_dir):
    rules = []
    for filename in os.listdir(rules_dir):
        if filename.endswith(".md") and filename != "index.md":
            filepath = os.path.join(rules_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                # Extract yaml block
                if content.startswith("---"):
                    end_idx = content.find("---", 3)
                    if end_idx != -1:
                        yaml_content = content[3:end_idx].strip()
                        try:
                            rule_meta = yaml.safe_load(yaml_content)
                            rules.append(rule_meta)
                        except:
                            pass
    return rules

def run_validation(apartment, rules):
    results = []
    print(f"Validating Apartment: {apartment.get('apartment_id', 'Unknown')}")
    print("-" * 50)
    
    # 1. Global Parameters Check (Ceiling Height B1.13)
    ceiling_height = apartment.get("global_parameters", {}).get("ceiling_height_m", 0)
    threshold_height = get_rule_param(rules, "B1.13", "min_height_m", FALLBACK_THRESHOLDS["B1.13"]["min_height_m"])
    if not ceiling_height:
        # e.g. PDF sales plans carry no ceiling height — missing data is not a violation
        results.append({
            "status": "WARN",
            "element": "גובה תקרה חלל עיקרי",
            "rule_id": "B1.13",
            "message": f"גובה תקרה לא מופיע בנתוני התכנית — לא ניתן לאמת מול המינימום {threshold_height:.2f} מ'."
        })
    elif ceiling_height < threshold_height:
        results.append({
            "status": "FAIL",
            "element": "גובה תקרה חלל עיקרי",
            "rule_id": "B1.13",
            "message": f"גובה התקרה {ceiling_height} מ' נמוך מהמינימום המחייב {threshold_height} מ'."
        })
    else:
        results.append({"status": "PASS", "element": "גובה תקרה חלל עיקרי", "rule_id": "B1.13", "message": f"תקין (מעל {threshold_height:.2f} מ')" })

    # 2. Rooms Check
    for room in apartment.get("rooms", []):
        room_type = room.get("type")
        room_area = room.get("area_sqm", 0)
        room_name = room.get("name", "חדר")
        
        # Check Living Room (B1.3)
        if room_type == "living_room":
            threshold = get_rule_param(rules, "B1.3", "min_area_sqm", FALLBACK_THRESHOLDS["B1.3"]["min_area_sqm"])
            if room_area < threshold:
                results.append({
                    "status": "FAIL",
                    "element": f"שטח סלון ({room_name})",
                    "rule_id": "B1.3",
                    "message": f"שטח הסלון {room_area} מ\"ר נמוך מהמינימום המחייב {threshold} מ\"ר."
                })
            else:
                results.append({"status": "PASS", "element": f"שטח סלון ({room_name})", "rule_id": "B1.3", "message": f"תקין ({room_area} מ\"ר)"})
        
        # Check Bedroom Area (B1.6)
        elif room_type == "bedroom":
            threshold = get_rule_param(rules, "B1.6", "min_area_sqm", FALLBACK_THRESHOLDS["B1.6"]["min_area_sqm"])
            if room_area < threshold:
                results.append({
                    "status": "FAIL",
                    "element": f"שטח חדר שינה ({room_name})",
                    "rule_id": "B1.6",
                    "message": f"שטח חדר שינה {room_area} מ\"ר נמוך מהמינימום המחייב {threshold} מ\"ר."
                })
            else:
                results.append({"status": "PASS", "element": f"שטח חדר שינה ({room_name})", "rule_id": "B1.6", "message": f"תקין ({room_area} מ\"ר)"})
                
        # Check Bathroom Area (B1.9)
        elif room_type == "bathroom":
            threshold = get_rule_param(rules, "B1.9", "min_area_sqm", FALLBACK_THRESHOLDS["B1.9"]["min_area_sqm"])
            if room_area < threshold:
                results.append({
                    "status": "FAIL",
                    "element": f"שטח חדר רחצה ({room_name})",
                    "rule_id": "B1.9",
                    "message": f"שטח חדר רחצה {room_area} מ\"ר נמוך מהמינימום המחייב {threshold} מ\"ר (מקלחת + אסלה)."
                })
            else:
                results.append({"status": "PASS", "element": f"שטח חדר רחצה ({room_name})", "rule_id": "B1.9", "message": f"תקין ({room_area} מ\"ר)"})

        # Check Kitchen Area (B1.11)
        elif room_type == "kitchen":
            threshold = get_rule_param(rules, "B1.11", "min_area_sqm", FALLBACK_THRESHOLDS["B1.11"]["min_area_sqm"])
            if room_area < threshold:
                results.append({
                    "status": "FAIL",
                    "element": f"שטח מטבח ({room_name})",
                    "rule_id": "B1.11",
                    "message": f"שטח המטבח {room_area} מ\"ר נמוך מהמינימום המחייב {threshold} מ\"ר לדירה בת 2 חדרים ומעלה."
                })
            else:
                results.append({"status": "PASS", "element": f"שטח מטבח ({room_name})", "rule_id": "B1.11", "message": f"תקין ({room_area} מ\"ר)"})

        # Check Corridor Width (B1.30)
        elif room_type == "corridor":
            width = room.get("width_cm", 0)
            if width > 0:
                if width < 80.0:
                    results.append({
                        "status": "FAIL",
                        "element": f"רוחב מסדרון ({room_name})",
                        "rule_id": "B1.30",
                        "message": f"רוחב המסדרון {width} ס\"מ נמוך מהמינימום המוחלט של 80 ס\"מ."
                    })
                elif width < 90.0:
                    results.append({
                        "status": "FAIL", # We can make it a soft fail/warning or fail based on length
                        "element": f"רוחב מסדרון ({room_name})",
                        "rule_id": "B1.30",
                        "message": f"רוחב המסדרון {width} ס\"מ נמוך מרוחב המעבר המומלץ למסדרונות ארוכים (90 ס\"מ)."
                    })
                else:
                    results.append({
                        "status": "PASS",
                        "element": f"רוחב מסדרון ({room_name})",
                        "rule_id": "B1.30",
                        "message": f"תקין ({width} ס\"מ)"
                    })

        # Check Utility Room (B1.31)
        elif room_type == "utility":
            area = room.get("area_sqm", 0)
            results.append({
                "status": "PASS",
                "element": f"שטח חדר שירות ({room_name})",
                "rule_id": "B1.31",
                "message": f"רשום תקין ({area} מ\"ר)"
            })

        # Check Ventilation (Simulating an A17 / IAQ check)
        if room_type == "bathroom" and not room.get("has_window") and room.get("ventilation_type") == "none":
            results.append({
                "status": "FAIL",
                "element": f"אוורור חדר רחצה ({room_name})",
                "rule_id": "A17",
                "message": "לחדר הרחצה אין חלון ואין אוורור מכני."
            })
            
    # 2.5. Safe Room (ממ"ד) Check (Israeli Regulations - B1.15)
    mamad_rooms = []
    for room in apartment.get("rooms", []):
        r_name = room.get("name", "")
        r_type = room.get("type", "")
        is_mamad_name = any(kw in r_name for kw in ["ממד", "ממ\"ד", "מרחב מוגן"])
        if r_type == "safe_room" or is_mamad_name:
            mamad_rooms.append(room)
            
    if not mamad_rooms:
        results.append({
            "status": "FAIL",
            "element": "מרחב מוגן דירתי (ממ\"ד)",
            "rule_id": "B1.15",
            "message": 'לא נמצא ממ"ד (מרחב מוגן דירתי) בדירה כנדרש בתקנות הג"א בישראל.'
        })
    else:
        for m_room in mamad_rooms:
            m_name = m_room.get("name", "ממ\"ד")
            m_area = m_room.get("area_sqm", 0)
            m_width = m_room.get("width_cm", 0) # width in cm
            
            # Area Check (9.0 sqm minimum)
            if m_area < 9.0:
                results.append({
                    "status": "FAIL",
                    "element": f"שטח ממ\"ד ({m_name})",
                    "rule_id": "B1.15",
                    "message": f"שטח הממ\"ד {m_area} מ\"ר נמוך מהמינימום המחייב של 9.0 מ\"ר."
                })
            else:
                results.append({
                    "status": "PASS",
                    "element": f"שטח ממ\"ד ({m_name})",
                    "rule_id": "B1.15",
                    "message": f"תקין ({m_area} מ\"ר)"
                })
                
            # Width Check (2.60m minimum = 260cm)
            if m_width > 0:
                if m_width < 260.0:
                    results.append({
                        "status": "FAIL",
                        "element": f"רוחב פנימי ממ\"ד ({m_name})",
                        "rule_id": "B1.15",
                        "message": f"רוחב הממ\"ד {m_width / 100.0:.2f} מ' נמוך מהמינימום המחייב של 2.60 מ'."
                    })
                else:
                    results.append({
                        "status": "PASS",
                        "element": f"רוחב פנימי ממ\"ד ({m_name})",
                        "rule_id": "B1.15",
                        "message": f"תקין ({m_width / 100.0:.2f} מ')"
                    })

    # 3. Accessibility Check
    entrance_width = apartment.get("accessibility", {}).get("main_entrance_width_cm", 0)
    entrance_threshold = get_rule_param(rules, "B44", "min_width_cm", FALLBACK_THRESHOLDS["B44"]["min_width_cm"])
    if not entrance_width:
        results.append({
            "status": "WARN",
            "element": "רוחב דלת כניסה ראשית",
            "rule_id": "B44",
            "message": f"רוחב דלת הכניסה לא זוהה בנתוני התכנית — לא ניתן לאמת מול {entrance_threshold:.0f} ס\"מ."
        })
    elif entrance_width < entrance_threshold:
        results.append({
            "status": "FAIL",
            "element": "רוחב דלת כניסה ראשית",
            "rule_id": "B44",
            "message": f"רוחב דלת הכניסה {entrance_width} ס\"מ נמוך מהמינימום של {entrance_threshold} ס\"מ לפי ספר התכנון."
        })
    else:
        results.append({"status": "PASS", "element": "רוחב דלת כניסה ראשית", "rule_id": "B44", "message": f"תקין ({entrance_width} ס\"מ)"})

    # 4. Advanced benchmark checks (v2): international benchmarks, ergonomics,
    #    Space Syntax topology, plan efficiency. Reported as WARN, never FAIL.
    try:
        results.extend(run_advanced_checks(apartment, rules))
    except Exception as e:  # never let an advanced check break the statutory report
        results.append({
            "status": "WARN",
            "element": "בדיקות מתקדמות",
            "rule_id": "ENGINE",
            "message": f"שגיאה בהרצת הבדיקות המתקדמות: {e}"
        })

    return results

# =============================================================================
# v2 — ADVANCED BENCHMARK CHECKS
# -----------------------------------------------------------------------------
# Thresholds are read from the knowledge base (frontmatter of okf_rules/*.md)
# through get_rule_param(). ADVANCED_FALLBACKS mirrors those values so the
# engine still works if a file is missing. Knowledge files:
#   WBS_NDSS_ADG          -> okf_rules/wbs_ndss_adg_housing_benchmarks.md
#   NKBA_KB               -> okf_rules/nkba_kitchen_bath_planning_guidelines.md
#   APL_HOUSING           -> okf_rules/alexander_pattern_language_housing.md
#   SPACE_SYNTAX_SAGA     -> okf_rules/space_syntax_saga_metrics.md
#   IS1918_ACCESS         -> okf_rules/israel_accessibility_is1918_housing.md
#   DAYLIGHT_VENT_IEQ     -> okf_rules/daylight_ventilation_ieq_standards.md
#   USABILITY_FURNISH_HQI -> okf_rules/spatial_usability_furnishability_hqi.md
# These are benchmarks / non-Israeli or unverified references, so every
# advanced check reports WARN (never FAIL). Statutory FAILs stay above.
# Every check runs only when its input data exists (zero-trust: no guessing).
# =============================================================================
import math
from collections import deque

ADVANCED_FALLBACKS = {
    "WBS_NDSS_ADG": {
        "ndss_gia_single_storey_sqm": {
            "1b1p": 39, "1b2p": 50, "2b3p": 61, "2b4p": 70, "3b4p": 74, "3b5p": 86,
            "3b6p": 95, "4b5p": 90, "4b6p": 99, "4b7p": 108, "4b8p": 117, "5b6p": 103,
            "5b7p": 112, "5b8p": 121, "6b7p": 116, "6b8p": 125,
        },
        "ndss_storage_sqm": {1: 1.5, 2: 2.0, 3: 2.5, 4: 3.0, 5: 3.5, 6: 4.0},
        "ndss_single_bedroom_min_sqm": 7.5,
        "ndss_single_bedroom_min_width_m": 2.15,
        "ndss_double_bedroom_min_sqm": 11.5,
        "ndss_main_double_min_width_m": 2.75,
        "ndss_other_double_min_width_m": 2.55,
        "london_min_ceiling_m": 2.5,
        "london_outdoor_base_sqm": 5.0,
        "london_outdoor_per_extra_person_sqm": 1.0,
        "london_outdoor_min_depth_m": 1.5,
        "adg_min_apartment_sqm": {0: 35, 1: 50, 2: 70, 3: 90},
        "adg_extra_bathroom_sqm": 5,
        "adg_extra_bedroom_sqm": 12,
        "adg_master_bedroom_min_sqm": 10,
        "adg_other_bedroom_min_sqm": 9,
        "adg_bedroom_min_dimension_m": 3.0,
        "adg_living_min_width_small_m": 3.6,
        "adg_living_min_width_large_m": 4.0,
        "adg_habitable_ceiling_m": 2.7,
        "adg_window_to_floor_min_ratio": 0.10,
        "adg_room_depth_to_ceiling_max": 2.5,
        "adg_balcony_min": {0: [4, 0.0], 1: [8, 2.0], 2: [10, 2.0], 3: [12, 2.4]},
        "adg_storage_m3": {0: 4, 1: 6, 2: 8, 3: 10},
    },
    "NKBA_KB": {
        "kitchen_triangle_max_total_m": 7.92,
        "kitchen_triangle_leg_min_m": 1.22,
        "kitchen_triangle_leg_max_m": 2.74,
        "kitchen_work_aisle_one_cook_cm": 107,
        "kitchen_work_aisle_multi_cook_cm": 122,
        "kitchen_walkway_min_cm": 91,
        "kitchen_countertop_frontage_min_cm": 401,
        "kitchen_seating_clearance_no_traffic_cm": 81,
        "kitchen_seating_clearance_walk_past_cm": 112,
        "bath_toilet_centerline_side_code_cm": 38,
        "bath_toilet_centerline_side_rec_cm": 46,
        "bath_toilet_front_clear_code_cm": 53,
        "bath_toilet_front_clear_rec_cm": 76,
        "bath_lav_front_clear_code_cm": 53,
        "bath_lav_front_clear_rec_cm": 76,
        "bath_shower_min_code_cm": [76, 76],
        "bath_shower_min_rec_cm": [91, 91],
    },
    "APL_HOUSING": {"balcony_min_depth_m": 1.83},
    "SPACE_SYNTAX_SAGA": {
        "corridor_ratio_good_max": 0.10,
        "corridor_ratio_warn_max": 0.15,
        "rectangularity_min": 0.85,
        "topology_min_coverage": 0.70,
        "private_room_min_depth": 2,
    },
    "IS1918_ACCESS": {
        "turning_circle_cm": 150,
        "door_clear_width_cm": 80,
        "threshold_max_cm": 2,
    },
    "DAYLIGHT_VENT_IEQ": {
        "en17037_view_angle_min_deg": 14,
        "en17037_view_angle_med_deg": 28,
        "en17037_view_angle_high_deg": 54,
        "en17037_view_dist_min_m": 6.0,
        "en17037_view_dist_med_m": 20.0,
        "en17037_view_dist_high_m": 50.0,
        "en17037_view_layers_min": 1,
        "en17037_view_layers_med": 2,
        "en17037_view_layers_high": 3,
        "en17037_sunlight_min_hours": 1.5,
        "en17037_sunlight_med_hours": 3.0,
        "en17037_sunlight_high_hours": 4.0,
        "br209_no_sky_line_min_share": 0.80,
        "br209_obstruction_angle_max_deg": 25.0,
        "cibse_single_sided_single_open_depth_to_height": 2.0,
        "cibse_single_sided_dual_open_depth_to_height": 2.5,
        "cibse_cross_vent_max_depth_to_height": 5.0,
        "cibse_openable_window_to_floor_min_ratio": 0.05,
        "tm59_west_unshaded_glazing_warn_ratio": 0.25,
        "well_window_access_max_m": 7.5,
        "well_circadian_optimal_m": 4.5,
    },
    "USABILITY_FURNISH_HQI": {
        "boverket_double_bed_wall_min_m": 3.00,
        "boverket_single_bed_wall_min_m": 2.10,
        "boverket_double_wardrobe_wall_min_m": 1.80,
        "boverket_single_wardrobe_wall_min_m": 1.20,
        "boverket_door_corner_offset_min_cm": 60,
        "hqi_combined_living_sqm_by_bedspaces": {
            1: 18.0, 2: 21.0, 3: 23.0, 4: 25.0, 5: 27.0, 6: 29.0, 7: 31.0, 8: 33.0,
        },
        "hqi_living_only_min_sqm_by_bedspaces": {
            1: 11.0, 2: 12.0, 3: 13.0, 4: 14.0, 5: 16.0, 6: 18.0, 7: 20.0, 8: 21.0,
        },
        "din18040_corridor_min_cm": 120,
        "din18040_latch_side_pull_min_cm": 60,
        "din18040_latch_side_push_min_cm": 30,
        "din18040_bedside_clearance_min_cm": 90,
        "din18040_bedside_wheelchair_min_cm": 120,
        "levels_adaptable_partition_min_ratio": 0.60,
    },
}

SLEEPING = {"bedroom", "safe_room"}
PUBLIC = {"living", "kitchen", "dining"}
WET = {"bathroom", "toilet"}
HABITABLE = {"living", "kitchen", "dining", "bedroom", "safe_room"}
EXT_TOKENS = {"EXT", "EXTERIOR", "ENTRANCE", "OUT", "OUTSIDE", "STAIR", "STAIRS", "LOBBY", "CORE", "__EXT__"}
EXT_NODE = "__EXT__"
ACCESS_NOTE = ' (ערך ייחוס בינלאומי — לאימות מול נוסח ת"י 1918)'


def _p(rules, rule_id, key):
    """Read a threshold from the knowledge base, falling back to the mirrored default."""
    return get_rule_param(rules, rule_id, key, ADVANCED_FALLBACKS[rule_id][key])


def _res(status, element, rule_id, message):
    return {"status": status, "element": element, "rule_id": rule_id, "message": message}


def _int_key(d, k):
    """YAML may load numeric keys as int or str; look up both."""
    if k in d:
        return d[k]
    return d.get(str(k))


def _norm_type(room):
    t = str(room.get("type") or "").strip().lower()
    name = str(room.get("name") or "")
    if t in ("safe_room", "mamad") or any(kw in name for kw in ["ממד", "ממ\"ד", "מרחב מוגן"]):
        return "safe_room"
    rules_ = [
        (("living", "reception", "salon", "lounge"), "living"),
        (("dining",), "dining"),
        (("kitchen",), "kitchen"),
        (("bed",), "bedroom"),
        (("toilet", "wc"), "toilet"),
        (("bath", "shower"), "bathroom"),
        (("corridor", "hall", "passage"), "corridor"),
        (("entr", "foyer", "vestibule"), "entrance"),
        (("balcon", "terrace", "loggia"), "balcony"),
        (("stor", "closet", "pantry"), "storage"),
        (("laundry", "utility", "service"), "utility"),
    ]
    for keys, norm in rules_:
        if any(k in t for k in keys):
            return norm
    return t


def _area(room):
    try:
        return float(room.get("area_sqm") or 0)
    except (TypeError, ValueError):
        return 0.0


def _width_m(room):
    if room.get("width_cm"):
        return float(room["width_cm"]) / 100.0
    if room.get("width_m"):
        return float(room["width_m"])
    return None


def _label(room, fallback="חדר"):
    return room.get("name") or room.get("id") or fallback


# ---------- geometry helpers (rectangularity, EF-2) ----------
def _poly_area(pts):
    s = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0


def _convex_hull(pts):
    pts = sorted(set((float(x), float(y)) for x, y in pts))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def _min_bounding_rect_area(pts):
    """Minimum-area enclosing rectangle (one side is collinear with a hull edge)."""
    hull = _convex_hull(pts)
    if len(hull) < 3:
        return 0.0
    best = float("inf")
    n = len(hull)
    for i in range(n):
        x1, y1 = hull[i]
        x2, y2 = hull[(i + 1) % n]
        ang = math.atan2(y2 - y1, x2 - x1)
        c, s = math.cos(-ang), math.sin(-ang)
        xs = [x * c - y * s for x, y in hull]
        ys = [x * s + y * c for x, y in hull]
        best = min(best, (max(xs) - min(xs)) * (max(ys) - min(ys)))
    return best


# ---------- Space Syntax helpers ----------
def _d_value(k):
    """Hillier & Hanson diamond value D_k used to normalise RA into RRA."""
    if k < 3:
        return None
    return 2.0 * (k * (math.log2((k + 2) / 3.0) - 1) + 1) / ((k - 1) * (k - 2))


def _bfs(adj, src):
    dist = {src: 0}
    q = deque([src])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


# ---------- individual check groups ----------
def _check_dwelling_size(rules, total, n_bed, n_bath, bedspaces, used_room_sum):
    out = []
    if total <= 0:
        return out
    basis = "סכום שטחי החדרים נטו (ללא קירות) — השוואה שמרנית" if used_room_sum else "שטח נטו שהוזן"

    adg_tbl = _p(rules, "WBS_NDSS_ADG", "adg_min_apartment_sqm")
    base = _int_key(adg_tbl, min(n_bed, 3))
    if base is not None:
        req = float(base) \
            + float(_p(rules, "WBS_NDSS_ADG", "adg_extra_bedroom_sqm")) * max(0, n_bed - 3) \
            + float(_p(rules, "WBS_NDSS_ADG", "adg_extra_bathroom_sqm")) * max(0, n_bath - 1)
        status = "PASS" if total >= req else "WARN"
        out.append(_res(status, "שטח דירה מול ADG 4D-1", "WBS_NDSS_ADG",
                        f"{total:.1f} מ\"ר ({basis}) מול מינימום {req:.0f} מ\"ר ל-{n_bed} ח\"ש ו-{n_bath} חדרי רחצה."))

    if 1 <= n_bed <= 6:
        tbl = _p(rules, "WBS_NDSS_ADG", "ndss_gia_single_storey_sqm")
        options = {}
        for k, v in tbl.items():
            k = str(k)
            if k.startswith(f"{n_bed}b"):
                options[int(k.split("b")[1].rstrip("p"))] = float(v)
        if options:
            p = min(options, key=lambda x: (abs(x - bedspaces), -x))
            req = options[p]
            status = "PASS" if total >= req else "WARN"
            out.append(_res(status, f"שטח דירה מול NDSS ({n_bed}b{p}p)", "WBS_NDSS_ADG",
                            f"{total:.1f} מ\"ר ({basis}) מול GIA מינימלי {req:.0f} מ\"ר. "
                            f"NDSS מודד GIA הכולל מחיצות — חריגה קטנה עשויה להיעלם במדידת GIA."))
    return out


def _check_bedrooms(rules, sleeping):
    out = []
    if not sleeping:
        return out
    g = lambda k: float(_p(rules, "WBS_NDSS_ADG", k))
    main = max(sleeping, key=_area)
    for r in sleeping:
        area, w = _area(r), _width_m(r)
        is_main = r is main
        if area >= g("ndss_double_bedroom_min_sqm"):
            ndss_a = g("ndss_double_bedroom_min_sqm")
            ndss_w = g("ndss_main_double_min_width_m") if is_main else g("ndss_other_double_min_width_m")
            kind = "זוגי ראשי" if is_main else "זוגי"
        else:
            ndss_a, ndss_w, kind = g("ndss_single_bedroom_min_sqm"), g("ndss_single_bedroom_min_width_m"), "יחיד"
        adg_a = g("adg_master_bedroom_min_sqm") if is_main else g("adg_other_bedroom_min_sqm")
        adg_w = g("adg_bedroom_min_dimension_m")

        below_ndss, below_adg = [], []
        if area < ndss_a:
            below_ndss.append(f"שטח {area:.2f} < {ndss_a}")
        if w is not None and w < ndss_w:
            below_ndss.append(f"רוחב {w:.2f} < {ndss_w}")
        if area < adg_a:
            below_adg.append(f"שטח {area:.2f} < {adg_a}")
        if w is not None and w < adg_w:
            below_adg.append(f"רוחב {w:.2f} < {adg_w}")
        width_note = "" if w is not None else " (רוחב לא הוזן — נבדק שטח בלבד)"

        if below_ndss:
            out.append(_res("WARN", f"חדר שינה מול NDSS ({_label(r)})", "WBS_NDSS_ADG",
                            f"חדר {kind}: מתחת לרף NDSS — {', '.join(below_ndss)}.{width_note}"))
        elif below_adg:
            out.append(_res("WARN", f"חדר שינה מול ADG ({_label(r)})", "WBS_NDSS_ADG",
                            f"עומד ב-NDSS (חדר {kind}), מתחת לרף המצוינות ADG 4D-3 — {', '.join(below_adg)} "
                            f"(ADG מודד ללא ארון בגדים).{width_note}"))
        else:
            out.append(_res("PASS", f"חדר שינה מול NDSS/ADG ({_label(r)})", "WBS_NDSS_ADG",
                            f"עומד ב-NDSS וב-ADG ({area:.2f} מ\"ר{'' if w is None else f', רוחב {w:.2f} מ'}).{width_note}"))
    return out


def _check_living(rules, livings, n_bed):
    out = []
    with_w = [r for r in livings if _width_m(r) is not None]
    if not with_w:
        return out
    r = max(with_w, key=_area)
    w = _width_m(r)
    key = "adg_living_min_width_small_m" if n_bed <= 1 else "adg_living_min_width_large_m"
    req = float(_p(rules, "WBS_NDSS_ADG", key))
    status = "PASS" if w >= req else "WARN"
    out.append(_res(status, f"רוחב סלון מול ADG ({_label(r)})", "WBS_NDSS_ADG",
                    f"רוחב {w:.2f} מ' מול {req} מ' (ADG 4D-3). המינימום החוקי בישראל (2.60 מ') נבדק בנפרד."))
    return out


def _check_ceiling(rules, ceiling):
    if ceiling <= 0:
        return []
    adg = float(_p(rules, "WBS_NDSS_ADG", "adg_habitable_ceiling_m"))
    london = float(_p(rules, "WBS_NDSS_ADG", "london_min_ceiling_m"))
    if ceiling >= adg:
        return [_res("PASS", "גובה תקרה מול ADG / London", "WBS_NDSS_ADG",
                     f"{ceiling} מ' — עומד ברף ADG 4C ({adg} מ') וב-London D6 ({london} מ').")]
    lon = "עומד" if ceiling >= london else "אינו עומד"
    return [_res("WARN", "גובה תקרה מול ADG / London", "WBS_NDSS_ADG",
                 f"{ceiling} מ' — מתחת לרף ADG 4C ({adg} מ'); {lon} ברף London D6 ({london} מ').")]


def _check_windows_depth(rules, typed, ceiling):
    out = []
    ratio_min = float(_p(rules, "WBS_NDSS_ADG", "adg_window_to_floor_min_ratio"))
    depth_k = float(_p(rules, "WBS_NDSS_ADG", "adg_room_depth_to_ceiling_max"))
    for r, t in typed:
        if t not in HABITABLE:
            continue
        a = _area(r)
        if r.get("window_area_sqm") is not None and a > 0:
            ratio = float(r["window_area_sqm"]) / a
            out.append(_res("PASS" if ratio >= ratio_min else "WARN", f"יחס חלון/רצפה ({_label(r)})", "WBS_NDSS_ADG",
                            f"{ratio:.0%} מול {ratio_min:.0%} (ADG 4D-1)."))
        if r.get("depth_m") is not None and ceiling > 0:
            d, lim = float(r["depth_m"]), depth_k * ceiling
            out.append(_res("PASS" if d <= lim else "WARN", f"עומק חדר מול חדירת אור ({_label(r)})", "WBS_NDSS_ADG",
                            f"עומק {d:.2f} מ' מול מקסימום {lim:.2f} מ' ({depth_k} × גובה תקרה, ADG 4D-2)."))
    return out


def _check_corridor_ratio(rules, typed, total):
    corr = [r for r, t in typed if t == "corridor"]
    if not corr or total <= 0:
        return []
    ca = sum(_area(r) for r in corr)
    ratio = ca / total
    good = float(_p(rules, "SPACE_SYNTAX_SAGA", "corridor_ratio_good_max"))
    warn = float(_p(rules, "SPACE_SYNTAX_SAGA", "corridor_ratio_warn_max"))
    if ratio <= good:
        status, verdict = "PASS", "יעיל"
    elif ratio <= warn:
        status, verdict = "WARN", "גבולי"
    else:
        status, verdict = "WARN", "חריג — מסדרונות ארוכים (APL#132)"
    return [_res(status, "יחס שטחי מעבר (EF-1)", "SPACE_SYNTAX_SAGA",
                 f"{ca:.1f} מ\"ר מסדרונות = {ratio:.1%} משטח הדירה ({verdict}; רף טוב ≤ {good:.0%}, היוריסטיקה לכיול).")]


def _check_rectangularity(rules, typed):
    out = []
    thr = float(_p(rules, "SPACE_SYNTAX_SAGA", "rectangularity_min"))
    for r, t in typed:
        poly = r.get("polygon")
        if not poly or len(poly) < 3:
            continue
        a = _poly_area(poly)
        mbr = _min_bounding_rect_area(poly)
        if mbr <= 0:
            continue
        ratio = a / mbr
        out.append(_res("PASS" if ratio >= thr else "WARN", f"מלבניות חדר (EF-2) ({_label(r)})", "SPACE_SYNTAX_SAGA",
                        f"יחס שטח/מלבן חוסם = {ratio:.2f} (רף {thr}; APL#191, יכולת ריהוט WBS)."))
    return out


def _check_balconies(rules, typed, apartment, n_bed, bedspaces):
    balconies = [r for r, t in typed if t == "balcony"] or list(apartment.get("balconies") or [])
    if not balconies:
        return [_res("WARN", "שטח חוץ פרטי (מרפסת)", "WBS_NDSS_ADG",
                     "לא זוהתה מרפסת בנתוני הדירה (London D6 / ADG 4E). ייתכן שהמפענח לא זיהה אותה — יש לוודא.")]
    b = max(balconies, key=_area)
    a = _area(b)
    depth = b.get("depth_m")
    if depth is None and _width_m(b) is not None:
        depth = _width_m(b)
    adg = _int_key(_p(rules, "WBS_NDSS_ADG", "adg_balcony_min"), min(n_bed, 3)) or [0, 0]
    lon_area = float(_p(rules, "WBS_NDSS_ADG", "london_outdoor_base_sqm")) + \
        float(_p(rules, "WBS_NDSS_ADG", "london_outdoor_per_extra_person_sqm")) * max(0, bedspaces - 2)
    lon_depth = float(_p(rules, "WBS_NDSS_ADG", "london_outdoor_min_depth_m"))
    apl_depth = float(_p(rules, "APL_HOUSING", "balcony_min_depth_m"))
    issues = []
    if a < float(adg[0]):
        issues.append(f"שטח {a:.1f} < {adg[0]} מ\"ר (ADG 4E)")
    if a < lon_area:
        issues.append(f"שטח {a:.1f} < {lon_area:.0f} מ\"ר (London D6)")
    if depth is not None:
        depth = float(depth)
        if depth < float(adg[1]):
            issues.append(f"עומק {depth:.2f} < {adg[1]} מ' (ADG 4E)")
        if depth < lon_depth:
            issues.append(f"עומק {depth:.2f} < {lon_depth} מ' (London D6)")
        elif depth < apl_depth:
            issues.append(f"עומק {depth:.2f} < {apl_depth} מ' (APL#167 Six-Foot Balcony)")
    depth_txt = "עומק לא הוזן" if depth is None else f"עומק {depth:.2f} מ'"
    if issues:
        return [_res("WARN", f"מרפסת עיקרית ({_label(b, 'מרפסת')})", "WBS_NDSS_ADG", "; ".join(issues) + ".")]
    return [_res("PASS", f"מרפסת עיקרית ({_label(b, 'מרפסת')})", "WBS_NDSS_ADG",
                 f"{a:.1f} מ\"ר, {depth_txt} — עומדת ב-ADG 4E, London D6 ו-APL#167.")]


def _check_storage(rules, typed, apartment, n_bed):
    st = apartment.get("storage") or {}
    built = st.get("built_in_sqm")
    store_rooms = sum(_area(r) for r, t in typed if t == "storage")
    if built is None and store_rooms > 0:
        built = store_rooms
    vol = st.get("volume_m3")
    if built is None and vol is None:
        return [_res("WARN", "נפח אחסון ייעודי", "WBS_NDSS_ADG",
                     "אין נתוני אחסון (storage / חדרי storage) — B7, NDSS ו-ADG 4G לא ניתנים לאימות.")]
    out = []
    if built is not None:
        req = _int_key(_p(rules, "WBS_NDSS_ADG", "ndss_storage_sqm"), min(max(n_bed, 1), 6))
        if req is not None:
            out.append(_res("PASS" if float(built) >= float(req) else "WARN", "אחסון מובנה מול NDSS", "WBS_NDSS_ADG",
                            f"{float(built):.1f} מ\"ר מול {req} מ\"ר ל-{n_bed} ח\"ש."))
    if vol is not None:
        req = _int_key(_p(rules, "WBS_NDSS_ADG", "adg_storage_m3"), min(n_bed, 3))
        if req is not None:
            out.append(_res("PASS" if float(vol) >= float(req) else "WARN", "נפח אחסון מול ADG 4G", "WBS_NDSS_ADG",
                            f"{float(vol):.1f} מ\"ק מול {req} מ\"ק (לפחות 50% בתוך הדירה)."))
    return out


def _check_aspect(apartment):
    ori = apartment.get("orientations")
    if not ori:
        return []
    dirs = sorted(set(str(o).strip().upper() for o in ori))
    if len(dirs) >= 2:
        return [_res("PASS", "כיווניות ואוורור צולב", "WBS_NDSS_ADG",
                     f"דירה {len(dirs)}-כיוונית ({', '.join(dirs)}) — מאפשרת אוורור צולב (ADG 4B, London D6, APL#159).")]
    if dirs == ["N"]:
        return [_res("WARN", "כיווניות ואוורור צולב", "WBS_NDSS_ADG",
                     "דירה חד-כיוונית הפונה לצפון — London D6 אוסר זאת; ללא שמש ישירה וללא אוורור צולב.")]
    return [_res("WARN", "כיווניות ואוורור צולב", "WBS_NDSS_ADG",
                 f"דירה חד-כיוונית ({dirs[0]}) — ללא אוורור צולב טבעי (ADG 4B).")]


def _check_kitchen_nkba(rules, typed):
    out = []
    g = lambda k: _p(rules, "NKBA_KB", k)
    for r, t in typed:
        kl = r.get("kitchen_layout")
        if t != "kitchen" or not isinstance(kl, dict):
            continue
        issues, ok = [], []
        legs = kl.get("work_triangle_legs_m")
        if isinstance(legs, (list, tuple)) and len(legs) == 3:
            legs = [float(x) for x in legs]
            tot = sum(legs)
            if tot > float(g("kitchen_triangle_max_total_m")):
                issues.append(f"משולש עבודה {tot:.2f} מ' > {g('kitchen_triangle_max_total_m')} מ'")
            bad = [x for x in legs if x < float(g("kitchen_triangle_leg_min_m")) or x > float(g("kitchen_triangle_leg_max_m"))]
            if bad:
                issues.append(f"צלעות מחוץ לטווח {g('kitchen_triangle_leg_min_m')}–{g('kitchen_triangle_leg_max_m')} מ': {bad}")
            if tot <= float(g("kitchen_triangle_max_total_m")) and not bad:
                ok.append(f"משולש {tot:.2f} מ'")
        if kl.get("aisle_width_cm") is not None:
            cooks = int(kl.get("cooks") or 1)
            req = float(g("kitchen_work_aisle_multi_cook_cm") if cooks >= 2 else g("kitchen_work_aisle_one_cook_cm"))
            v = float(kl["aisle_width_cm"])
            (ok if v >= req else issues).append(f"מעבר עבודה {v:.0f} ס\"מ {'≥' if v >= req else '<'} {req:.0f} ({cooks} בשלנים)")
        if kl.get("walkway_width_cm") is not None:
            v, req = float(kl["walkway_width_cm"]), float(g("kitchen_walkway_min_cm"))
            (ok if v >= req else issues).append(f"מעבר הליכה {v:.0f} ס\"מ {'≥' if v >= req else '<'} {req:.0f}")
        if kl.get("countertop_frontage_cm") is not None:
            v, req = float(kl["countertop_frontage_cm"]), float(g("kitchen_countertop_frontage_min_cm"))
            (ok if v >= req else issues).append(f"חזית משטחים {v:.0f} ס\"מ {'≥' if v >= req else '<'} {req:.0f}")
        if kl.get("seating_clearance_cm") is not None:
            key = "kitchen_seating_clearance_walk_past_cm" if kl.get("traffic_behind_seating") else "kitchen_seating_clearance_no_traffic_cm"
            v, req = float(kl["seating_clearance_cm"]), float(g(key))
            (ok if v >= req else issues).append(f"מרווח מאחורי ישיבה {v:.0f} ס\"מ {'≥' if v >= req else '<'} {req:.0f}")
        if issues:
            out.append(_res("WARN", f"ארגונומיית מטבח NKBA ({_label(r)})", "NKBA_KB", "; ".join(issues) + "."))
        elif ok:
            out.append(_res("PASS", f"ארגונומיית מטבח NKBA ({_label(r)})", "NKBA_KB", "; ".join(ok) + "."))
    return out


def _check_bath_nkba(rules, typed):
    out = []
    g = lambda k: _p(rules, "NKBA_KB", k)
    params = [
        ("toilet_centerline_to_side_cm", "ציר אסלה לקיר צד", "bath_toilet_centerline_side_code_cm", "bath_toilet_centerline_side_rec_cm"),
        ("toilet_front_clearance_cm", "מרווח מול אסלה", "bath_toilet_front_clear_code_cm", "bath_toilet_front_clear_rec_cm"),
        ("lavatory_front_clearance_cm", "מרווח מול כיור", "bath_lav_front_clear_code_cm", "bath_lav_front_clear_rec_cm"),
    ]
    for r, t in typed:
        fx = r.get("fixtures")
        if t not in WET or not isinstance(fx, dict):
            continue
        notes, worst = [], "PASS"
        for key, label, code_k, rec_k in params:
            if fx.get(key) is None:
                continue
            v, code, rec = float(fx[key]), float(g(code_k)), float(g(rec_k))
            if v < code:
                notes.append(f"{label} {v:.0f} < Code {code:.0f}")
                worst = "WARN"
            elif v < rec:
                notes.append(f"{label} {v:.0f}: מעל Code, מתחת למומלץ {rec:.0f}")
                worst = "WARN"
            else:
                notes.append(f"{label} {v:.0f} ✓")
        sh = fx.get("shower_cm")
        if isinstance(sh, (list, tuple)) and len(sh) == 2:
            s = sorted(float(x) for x in sh)
            code, rec = sorted(g("bath_shower_min_code_cm")), sorted(g("bath_shower_min_rec_cm"))
            if s[0] < code[0] or s[1] < code[1]:
                notes.append(f"מקלחון {s[0]:.0f}×{s[1]:.0f} < Code {code[0]}×{code[1]}")
                worst = "WARN"
            elif s[0] < rec[0] or s[1] < rec[1]:
                notes.append(f"מקלחון {s[0]:.0f}×{s[1]:.0f}: מתחת למומלץ {rec[0]}×{rec[1]}")
                worst = "WARN"
            else:
                notes.append(f"מקלחון {s[0]:.0f}×{s[1]:.0f} ✓")
        if notes:
            out.append(_res(worst, f"ארגונומיית רחצה NKBA ({_label(r)})", "NKBA_KB", "; ".join(notes) + "."))
    return out


def _check_accessibility(rules, typed, apartment):
    acc = apartment.get("accessibility") or {}
    if not (apartment.get("accessible_unit") or acc.get("accessible_unit")):
        return []
    out = []
    tc_req = float(_p(rules, "IS1918_ACCESS", "turning_circle_cm"))
    door_req = float(_p(rules, "IS1918_ACCESS", "door_clear_width_cm"))
    thr_max = float(_p(rules, "IS1918_ACCESS", "threshold_max_cm"))

    wet = [r for r, t in typed if t == "bathroom"]
    tcs = [float(r["turning_circle_cm"]) for r in wet if r.get("turning_circle_cm") is not None]
    if not tcs:
        out.append(_res("WARN", "מעגל סיבוב בחדר רחצה", "IS1918_ACCESS",
                        "לא הוזן מעגל סיבוב (turning_circle_cm) לאף חדר רחצה." + ACCESS_NOTE))
    else:
        out.append(_res("PASS" if max(tcs) >= tc_req else "WARN", "מעגל סיבוב בחדר רחצה", "IS1918_ACCESS",
                        f"מקסימום Ø{max(tcs):.0f} ס\"מ מול Ø{tc_req:.0f} ס\"מ." + ACCESS_NOTE))

    narrow = []
    for r, t in typed:
        if r.get("clear_width_cm") is not None:
            v, kind = float(r["clear_width_cm"]), "נטו"
        elif r.get("door_width_cm") is not None:
            v, kind = float(r["door_width_cm"]), "כנף"
        else:
            continue
        if v < door_req:
            narrow.append(f"{_label(r)} ({v:.0f} ס\"מ {kind})")
    out.append(_res("WARN" if narrow else "PASS", "רוחב מעבר בדלתות פנים", "IS1918_ACCESS",
                    (f"מתחת ל-{door_req:.0f} ס\"מ: {', '.join(narrow)}." if narrow else f"כל הדלתות שהוזנו ≥ {door_req:.0f} ס\"מ.")
                    + " רוחב כנף גדול בכ-5–8 ס\"מ מהמעבר הנטו." + ACCESS_NOTE))

    for r, t in typed:
        if t == "balcony" and r.get("threshold_cm") is not None:
            v = float(r["threshold_cm"])
            out.append(_res("PASS" if v <= thr_max else "WARN", f"סף יציאה למרפסת ({_label(r, 'מרפסת')})", "IS1918_ACCESS",
                            f"{v} ס\"מ מול מקסימום {thr_max} ס\"מ." + ACCESS_NOTE))
    return out


def _check_topology(rules, typed, apartment):
    ids = {}
    for r, t in typed:
        if r.get("id") is not None:
            ids[str(r["id"])] = (r, t)
    if not ids:
        return []
    topo = apartment.get("topology") or []
    if not topo:
        return [_res("WARN", "ניתוח תצורה (Space Syntax)", "SPACE_SYNTAX_SAGA",
                     "אין נתוני טופולוגיה (topology) — מדרג פרטיות, עומק ואינטגרציה לא חושבו.")]

    adj = {i: set() for i in ids}
    adj[EXT_NODE] = set()

    def node(x):
        x = str(x)
        if x in ids:
            return x
        return EXT_NODE if x.upper() in EXT_TOKENS else None

    for e in topo:
        a, b = node(e.get("source")), node(e.get("target"))
        if a and b and a != b:
            adj[a].add(b)
            adj[b].add(a)
    ent = apartment.get("entrance_room_id") or (apartment.get("accessibility") or {}).get("entrance_room_id")
    if ent is not None and str(ent) in ids:
        adj[EXT_NODE].add(str(ent))
        adj[str(ent)].add(EXT_NODE)
    has_ext = bool(adj[EXT_NODE])
    if not has_ext:
        del adj[EXT_NODE]

    connected = [i for i in ids if adj[i]]
    min_cov = float(_p(rules, "SPACE_SYNTAX_SAGA", "topology_min_coverage"))
    cov = len(connected) / len(ids)
    if cov < min_cov:
        return [_res("WARN", "ניתוח תצורה (Space Syntax)", "SPACE_SYNTAX_SAGA",
                     f"הטופולוגיה מכסה רק {len(connected)}/{len(ids)} חדרים ({cov:.0%}, סף {min_cov:.0%}) — "
                     f"מדדי תצורה לא חושבו כדי לא לדווח ערכים מטעים.")]

    out = []
    name = lambda i: "כניסה" if i == EXT_NODE else _label(ids[i][0], i)
    nodes = list(adj)

    # components and loops (cyclomatic number E - V + C)
    seen, comps = set(), 0
    for n in nodes:
        if n not in seen:
            comps += 1
            seen |= set(_bfs(adj, n))
    edges = sum(len(adj[n]) for n in nodes) // 2
    loops = edges - len(nodes) + comps

    # integration per node (Hillier & Hanson): MD, RA, RRA, I = 1/RRA
    integ = {}
    for n in nodes:
        d = _bfs(adj, n)
        k = len(d)
        if k < 3:
            continue
        md = sum(d.values()) / (k - 1)
        ra = 2 * (md - 1) / (k - 2)
        dk = _d_value(k)
        rra = ra / dk if dk else None
        integ[n] = float("inf") if not rra else 1.0 / rra

    fmt = lambda v: "∞" if v == float("inf") else f"{v:.2f}"
    ranked = sorted((i for i in integ if i != EXT_NODE), key=lambda i: integ[i], reverse=True)
    if ranked:
        top = ", ".join(f"{name(i)} ({fmt(integ[i])})" for i in ranked[:3])
        out.append(_res("PASS", "אינטגרציה — החללים המרכזיים (Space Syntax)", "SPACE_SYNTAX_SAGA",
                        f"החללים המשולבים ביותר: {top}. מעגלי תנועה: {loops} (SS-6, APL#131)."))

    # SS-1: public rooms should be more integrated than bedrooms
    pub = [i for i in ids if ids[i][1] in PUBLIC and i in integ]
    beds = [i for i in ids if ids[i][1] in SLEEPING and i in integ]
    if pub and beds:
        best_pub = max(integ[i] for i in pub)
        hubs = [i for i in beds if integ[i] > best_pub]
        out.append(_res("WARN" if hubs else "PASS", "היררכיית מרכזיות (SS-1)", "SPACE_SYNTAX_SAGA",
                        (f"חדר שינה משולב יותר מהחלל הציבורי: {', '.join(name(i) for i in hubs)} — משמש כצומת מעבר."
                         if hubs else "החלל הציבורי משולב יותר מכל חדרי השינה (תקין).")))

    if has_ext:
        dist = _bfs(adj, EXT_NODE)
        unreachable = [i for i in ids if i not in dist]
        if unreachable:
            out.append(_res("WARN", "חדרים מנותקים בגרף", "SPACE_SYNTAX_SAGA",
                            f"לא ניתן להגיע מהכניסה אל: {', '.join(name(i) for i in unreachable)} — נתוני טופולוגיה חסרים או שגויים."))

        # SS-3: entrance transition / foyer
        first = [i for i in adj[EXT_NODE]]
        direct_pub = [i for i in first if ids[i][1] in PUBLIC]
        buffer = [i for i in first if ids[i][1] in ("entrance", "corridor")]
        if direct_pub and not buffer:
            out.append(_res("WARN", "רצף כניסה ומבואה (SS-3)", "SPACE_SYNTAX_SAGA",
                            f"הכניסה נפתחת ישירות אל {', '.join(name(i) for i in direct_pub)} ללא מבואה (B1.2, APL#112, APL#130)."))
        else:
            out.append(_res("PASS", "רצף כניסה ומבואה (SS-3)", "SPACE_SYNTAX_SAGA",
                            f"הכניסה מובילה אל: {', '.join(name(i) for i in first)}."))

        # SS-2: intimacy gradient
        min_d = int(_p(rules, "SPACE_SYNTAX_SAGA", "private_room_min_depth"))
        pub_d = [dist[i] for i in ids if ids[i][1] in PUBLIC and i in dist]
        pub_depth = min(pub_d) if pub_d else None
        shallow = []
        for i in ids:
            if ids[i][1] in SLEEPING and i in dist:
                d = dist[i]
                if d < min_d or (pub_depth is not None and d <= pub_depth):
                    shallow.append(f"{name(i)} (עומק {d})")
        if any(ids[i][1] in SLEEPING for i in ids):
            out.append(_res("WARN" if shallow else "PASS", "מדרג פרטיות (SS-2)", "SPACE_SYNTAX_SAGA",
                            (f"חדרי שינה רדודים מדי: {', '.join(shallow)}; עומק החלל הציבורי {pub_depth} (APL#127)."
                             if shallow else f"כל חדרי השינה בעומק ≥ {min_d} ועמוקים מהחלל הציבורי (עומק {pub_depth}).")))

    # SS-4: wet rooms opening onto public rooms
    wet_ids = [i for i in ids if ids[i][1] in WET]
    if wet_ids:
        bad = []
        for i in wet_ids:
            pubs = [j for j in adj[i] if j in ids and ids[j][1] in PUBLIC]
            if pubs:
                bad.append(f"{name(i)} ← {', '.join(name(j) for j in pubs)}")
        out.append(_res("WARN" if bad else "PASS", "פרטיות חדרי רחצה (SS-4)", "SPACE_SYNTAX_SAGA",
                        (f"חדר רחצה נפתח ישירות לחלל ציבורי: {'; '.join(bad)} (C1)." if bad
                         else "אף חדר רחצה אינו נפתח ישירות לסלון, למטבח או לפינת האוכל.")))

    # SS-5: pass-through bedrooms
    through = []
    for i in ids:
        if ids[i][1] not in SLEEPING:
            continue
        others = [j for j in adj[i] if j == EXT_NODE or (j in ids and ids[j][1] not in WET | {"storage", "balcony", "utility"})]
        if len(others) >= 2:
            through.append(name(i))
    if beds or any(ids[i][1] in SLEEPING for i in ids):
        out.append(_res("WARN" if through else "PASS", "חדרי שינה כמעבר (SS-5)", "SPACE_SYNTAX_SAGA",
                        (f"חדר שינה משמש מעבר בין חללים: {', '.join(through)}." if through
                         else "אף חדר שינה אינו משמש מעבר לחלל אחר.")))
    return out


def _check_daylight_vent_ieq(rules, typed, apartment, ceiling):
    """EN 17037, BR 209, CIBSE AM10/TM59 & WELL v2 checks (zero-trust: runs only when inputs exist)."""
    out = []
    g = lambda k: float(_p(rules, "DAYLIGHT_VENT_IEQ", k))

    # 1. EN 17037 Sunlight exposure (apartment-level or room-level)
    sun_hrs = apartment.get("sunlight_hours")
    if sun_hrs is not None:
        v = float(sun_hrs)
        min_h, med_h, high_h = g("en17037_sunlight_min_hours"), g("en17037_sunlight_med_hours"), g("en17037_sunlight_high_hours")
        tier = "גבוהה" if v >= high_h else ("בינונית" if v >= med_h else ("מינימום" if v >= min_h else "מתחת למינימום"))
        out.append(_res("PASS" if v >= min_h else "WARN", "חשיפה לשמש ישירה (EN 17037)", "DAYLIGHT_VENT_IEQ",
                        f"{v:.1f} שעות שמש (רמת EN 17037: {tier}; מינימום {min_h:.1f} שעות)."))

    # 2. CIBSE AM10 apartment-level cross-ventilation path depth
    cv_path = apartment.get("cross_vent_path_m")
    if cv_path is not None and ceiling > 0:
        v = float(cv_path)
        lim = g("cibse_cross_vent_max_depth_to_height") * ceiling
        out.append(_res("PASS" if v <= lim else "WARN", "עומק אוורור מפולש (CIBSE AM10)", "DAYLIGHT_VENT_IEQ",
                        f"אורך מסלול זרימה {v:.2f} מ' מול מקסימום {lim:.2f} מ' (5×H לפי CIBSE AM10)."))

    # 3. CIBSE TM59 single-aspect West/South-West overheating risk
    ori = apartment.get("orientations")
    if ori:
        dirs = sorted(set(str(o).strip().upper() for o in ori))
        if len(dirs) == 1 and dirs[0] in ("W", "SW"):
            out.append(_res("WARN", "סיכון התחממות יתר (CIBSE TM59)", "DAYLIGHT_VENT_IEQ",
                            f"דירה חד-כיוונית הפונה ל-{dirs[0]} ללא אוורור מפולש — סיכון גבוה לחימום יתר בקיץ (CIBSE TM59)."))

    # 4. Per-room daylight, view out, ventilation depth & WELL v2 checks
    for r, t in typed:
        if t not in HABITABLE:
            continue
        lbl = _label(r)
        a = _area(r)

        # EN 17037 View Out (distance, horizontal angle, layers)
        v_dist = r.get("view_distance_m")
        v_ang = r.get("view_angle_deg")
        v_lay = r.get("view_layers")
        if v_dist is not None or v_ang is not None or v_lay is not None:
            issues, notes = [], []
            if v_dist is not None:
                d = float(v_dist)
                min_d = g("en17037_view_dist_min_m")
                (notes if d >= min_d else issues).append(f"מרחק מבט {d:.1f} מ' ({'≥' if d >= min_d else '<'} {min_d:.0f} מ')")
            if v_ang is not None:
                ang = float(v_ang)
                min_a = g("en17037_view_angle_min_deg")
                (notes if ang >= min_a else issues).append(f"זווית מבט {ang:.0f}° ({'≥' if ang >= min_a else '<'} {min_a:.0f}°)")
            if v_lay is not None:
                lay = int(v_lay)
                min_l = int(g("en17037_view_layers_min"))
                (notes if lay >= min_l else issues).append(f"{lay} שכבות נוף")
            out.append(_res("WARN" if issues else "PASS", f"איכות מבט החוצה EN 17037 ({lbl})", "DAYLIGHT_VENT_IEQ",
                            "; ".join(issues + notes) + "."))

        # BR 209 No-Sky Line & obstruction angle
        if r.get("no_sky_line_share") is not None:
            nsl = float(r["no_sky_line_share"])
            req = g("br209_no_sky_line_min_share")
            out.append(_res("PASS" if nsl >= req else "WARN", f"קו שמיים No-Sky Line BR 209 ({lbl})", "DAYLIGHT_VENT_IEQ",
                            f"{nsl:.0%} משטח החדר רואה שמיים מול מינימום מומלץ {req:.0%} (BRE BR 209)."))
        if r.get("obstruction_angle_deg") is not None:
            ang = float(r["obstruction_angle_deg"])
            lim = g("br209_obstruction_angle_max_deg")
            out.append(_res("PASS" if ang <= lim else "WARN", f"זווית הסתרה BR 209 ({lbl})", "DAYLIGHT_VENT_IEQ",
                            f"זווית הסתרה {ang:.1f}° מול סף {lim:.0f}° (BRE BR 209)."))

        # CIBSE AM10 openable window area ratio
        if r.get("openable_window_area_sqm") is not None and a > 0:
            ratio = float(r["openable_window_area_sqm"]) / a
            req = g("cibse_openable_window_to_floor_min_ratio")
            out.append(_res("PASS" if ratio >= req else "WARN", f"שטח פתיחה חופשי לאוורור ({lbl})", "DAYLIGHT_VENT_IEQ",
                            f"{ratio:.1%} משטח הרצפה מול {req:.0%} (CIBSE AM10)."))

        # CIBSE AM10 ventilation mode effective depth
        v_mode = str(r.get("ventilation_mode") or "").strip().lower()
        if v_mode and r.get("depth_m") is not None and ceiling > 0:
            d = float(r["depth_m"])
            if v_mode in ("single", "single_opening", "single_sided"):
                k_mult, desc = g("cibse_single_sided_single_open_depth_to_height"), "אוורור חד-צדדי מפתח יחיד (2.0×H)"
            elif v_mode in ("dual_opening", "single_sided_dual"):
                k_mult, desc = g("cibse_single_sided_dual_open_depth_to_height"), "אוורור חד-צדדי משני פתחים (2.5×H)"
            else:
                k_mult, desc = g("cibse_cross_vent_max_depth_to_height"), "אוורור מפולש (5.0×H)"
            lim = k_mult * ceiling
            out.append(_res("PASS" if d <= lim else "WARN", f"עומק אפקטיבי לאוורור CIBSE AM10 ({lbl})", "DAYLIGHT_VENT_IEQ",
                            f"עומק {d:.2f} מ' מול מקסימום {lim:.2f} מ' עבור {desc}."))

        # CIBSE TM59 / IES ASE West unshaded glazing risk
        w_ori = str(r.get("window_orientation") or "").strip().upper()
        if w_ori in ("W", "SW") and r.get("window_area_sqm") is not None and a > 0:
            w_ratio = float(r["window_area_sqm"]) / a
            warn_r = g("tm59_west_unshaded_glazing_warn_ratio")
            if w_ratio > warn_r and not r.get("external_shading", False):
                out.append(_res("WARN", f"סיכון סנוור וחימום בחזית מערבית ({lbl})", "DAYLIGHT_VENT_IEQ",
                                f"יחס זיגוג {w_ratio:.0%} בחזית {w_ori} ללא הצללה חיצונית (סף {warn_r:.0%}, TM59 / IES ASE)."))

        # WELL v2 circadian & window access distance
        if r.get("distance_to_window_m") is not None:
            dist = float(r["distance_to_window_m"])
            max_d = g("well_window_access_max_m")
            opt_d = g("well_circadian_optimal_m")
            status = "PASS" if dist <= max_d else "WARN"
            note = "אופטימלי לאור צירקדי" if dist <= opt_d else ("בטווח WELL L01" if dist <= max_d else "מעבר לטווח WELL L01")
            out.append(_res(status, f"מרחק מחלון מבט WELL v2 ({lbl})", "DAYLIGHT_VENT_IEQ",
                            f"{dist:.2f} מ' ({note}; אופטימלי ≤ {opt_d} מ', מקסימום ≤ {max_d} מ')."))

    return out


def _check_usability_furnish_hqi(rules, typed, apartment, sleeping, livings, bedspaces):
    """Boverket/Byggforsk Möblerbarhet, HQI proportionality, DIN 18040-2/SIA 500, EU Level(s) 2.3 & CBE POE checks."""
    out = []
    g = lambda k: _p(rules, "USABILITY_FURNISH_HQI", k)
    double_min = float(_p(rules, "WBS_NDSS_ADG", "ndss_double_bedroom_min_sqm"))

    # 1. HQI Programmatic Proportionality (Living / Public area vs. Bedspaces)
    if livings and sleeping and bedspaces >= 1:
        p_key = min(max(bedspaces, 1), 8)
        liv_sqm = sum(_area(r) for r in livings)
        pub_sqm = sum(_area(r) for r, t in typed if t in PUBLIC)
        req_liv = float(_int_key(g("hqi_living_only_min_sqm_by_bedspaces"), p_key) or 12.0)
        req_pub = float(_int_key(g("hqi_combined_living_sqm_by_bedspaces"), p_key) or 21.0)
        issues = []
        if liv_sqm < req_liv:
            issues.append(f"סלון {liv_sqm:.1f} < {req_liv:.0f} מ\"ר")
        if pub_sqm > liv_sqm and pub_sqm < req_pub:
            issues.append(f"חלל ציבורי משולב (סלון+מטבח/אוכל) {pub_sqm:.1f} < {req_pub:.0f} מ\"ר")
        out.append(_res("WARN" if issues else "PASS",
                        f"איזון פרוגרמטי — חלל ציבורי ל-{bedspaces} נפשות (HQI)",
                        "USABILITY_FURNISH_HQI",
                        ("; ".join(issues) + f" עבור דירה ל-{bedspaces} מיטות (HQI Unit Layout)."
                         if issues else f"סלון {liv_sqm:.1f} מ\"ר וחלל ציבורי משולב {pub_sqm:.1f} מ\"ר תואמים {bedspaces} מיטות (HQI).")))

    # 2. Boverket / Byggforsk Furnishability (Möblerbarhet) & DIN 18040-2 / CBE POE on bedrooms
    is_acc = bool(apartment.get("accessible_unit") or (apartment.get("accessibility") or {}).get("accessible_unit"))
    for r in sleeping:
        lbl = _label(r)
        is_double = (_area(r) >= double_min) or (r.get("bedspaces") == 2)
        f_issues, f_ok = [], []

        if r.get("unbroken_wall_m") is not None:
            v = float(r["unbroken_wall_m"])
            req = float(g("boverket_double_bed_wall_min_m") if is_double else g("boverket_single_bed_wall_min_m"))
            (f_ok if v >= req else f_issues).append(f"קיר רציף למיטה {v:.2f} מ' ({'≥' if v >= req else '<'} {req:.2f} מ')")

        if r.get("wardrobe_wall_m") is not None:
            v = float(r["wardrobe_wall_m"])
            req = float(g("boverket_double_wardrobe_wall_min_m") if is_double else g("boverket_single_wardrobe_wall_min_m"))
            (f_ok if v >= req else f_issues).append(f"קיר לארון {v:.2f} מ' ({'≥' if v >= req else '<'} {req:.2f} מ')")

        if r.get("door_corner_offset_cm") is not None:
            off = float(r["door_corner_offset_cm"])
            req_off = float(g("boverket_door_corner_offset_min_cm"))
            if 10.0 < off < req_off:
                f_issues.append(f"היסט דלת מהפינה {off:.0f} ס\"מ < {req_off:.0f} ס\"מ (חוסם ארון בעומק 60 ס\"מ)")
            else:
                f_ok.append(f"היסט דלת מהפינה {off:.0f} ס\"מ תקין")

        if f_issues or f_ok:
            out.append(_res("WARN" if f_issues else "PASS",
                            f"יכולת ריהוט Möblerbarhet ({lbl})",
                            "USABILITY_FURNISH_HQI",
                            "; ".join(f_issues + f_ok) + " (Boverket / Byggforsk / WBS)."))

        if r.get("bedside_clearance_cm") is not None:
            v = float(r["bedside_clearance_cm"])
            req = float(g("din18040_bedside_wheelchair_min_cm") if is_acc else g("din18040_bedside_clearance_min_cm"))
            out.append(_res("PASS" if v >= req else "WARN",
                            f"מרווח גישה לצד מיטה DIN 18040-2 ({lbl})",
                            "USABILITY_FURNISH_HQI",
                            f"{v:.0f} ס\"מ מול מינימום {req:.0f} ס\"מ (DIN 18040-2 / SIA 500)."))

        if r.get("adjacent_to_noisy_zone") is not None:
            noisy = bool(r["adjacent_to_noisy_zone"])
            out.append(_res("WARN" if noisy else "PASS",
                            f"חיץ אקוסטי לחדר שינה CBE POE ({lbl})",
                            "USABILITY_FURNISH_HQI",
                            ("קיר משותף ישיר לחלל רועש (סלון/מטבח/מעלית/מסתור כביסה) ללא חיץ ארון — סיכון רעש (CBE POE / ת\"י 1004)."
                             if noisy else "מופרד אקוסטית מחללים רועשים (CBE POE / ת\"י 1004).")))

    # 3. Door latch-side clearance (Lifetime Homes Crit. 6 / DIN 18040-2 / SIA 500)
    for r, t in typed:
        if r.get("latch_side_clearance_cm") is not None:
            v = float(r["latch_side_clearance_cm"])
            side = str(r.get("door_open_side") or "pull").strip().lower()
            req = float(g("din18040_latch_side_push_min_cm") if side == "push" else g("din18040_latch_side_pull_min_cm"))
            out.append(_res("PASS" if v >= req else "WARN",
                            f"מרווח צד ידית דלת DIN 18040-2 ({_label(r)})",
                            "USABILITY_FURNISH_HQI",
                            f"{v:.0f} ס\"מ בצד ה-{'דחיפה' if side == 'push' else 'משיכה'} מול {req:.0f} ס\"מ (Lifetime Homes / DIN 18040-2)."))

    # 4. EU Level(s) Indicator 2.3 — Non-load-bearing internal partition ratio
    part_ratio = apartment.get("adaptable_partition_ratio")
    if part_ratio is None:
        part_ratio = (apartment.get("global_parameters") or {}).get("adaptable_partition_ratio")
    if part_ratio is not None:
        v = float(part_ratio)
        req = float(g("levels_adaptable_partition_min_ratio"))
        out.append(_res("PASS" if v >= req else "WARN",
                        "גמישות מחיצות פנים — EU Level(s) 2.3",
                        "USABILITY_FURNISH_HQI",
                        f"{v:.0%} מחיצות פנים פריקות (לא-נושאות) מול רף מומלץ ≥ {req:.0%} (EU Level(s) 2.3 / Open Building)."))

    return out


def run_advanced_checks(apartment, rules):
    """v2 benchmark checks. Returns a list of PASS/WARN results (never FAIL)."""
    rooms = apartment.get("rooms") or []
    typed = [(r, _norm_type(r)) for r in rooms]
    sleeping = [r for r, t in typed if t in SLEEPING]
    livings = [r for r, t in typed if t == "living"]
    n_bed = int(apartment["bedrooms"]) if apartment.get("bedrooms") is not None else len(sleeping)
    n_bath = sum(1 for r, t in typed if t == "bathroom")
    used_room_sum = not apartment.get("net_area_sqm")
    total = float(apartment.get("net_area_sqm") or sum(_area(r) for r, t in typed if t != "balcony"))
    ceiling = float((apartment.get("global_parameters") or {}).get("ceiling_height_m") or 0)
    double_min = float(_p(rules, "WBS_NDSS_ADG", "ndss_double_bedroom_min_sqm"))
    bedspaces = int(apartment.get("bedspaces") or sum(2 if _area(r) >= double_min else 1 for r in sleeping))

    out = []
    out += _check_dwelling_size(rules, total, n_bed, n_bath, bedspaces, used_room_sum)
    out += _check_bedrooms(rules, sleeping)
    out += _check_living(rules, livings, n_bed)
    out += _check_ceiling(rules, ceiling)
    out += _check_windows_depth(rules, typed, ceiling)
    out += _check_corridor_ratio(rules, typed, total)
    out += _check_rectangularity(rules, typed)
    out += _check_balconies(rules, typed, apartment, n_bed, bedspaces)
    out += _check_storage(rules, typed, apartment, n_bed)
    out += _check_aspect(apartment)
    out += _check_kitchen_nkba(rules, typed)
    out += _check_bath_nkba(rules, typed)
    out += _check_accessibility(rules, typed, apartment)
    out += _check_topology(rules, typed, apartment)
    out += _check_daylight_vent_ieq(rules, typed, apartment, ceiling)
    out += _check_usability_furnish_hqi(rules, typed, apartment, sleeping, livings, bedspaces)
    return out


def print_report(results):
    print("\n=== VALIDATION REPORT ===")
    icons = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}
    counts = {"PASS": 0, "WARN": 0, "FAIL": 0}
    for res in results:
        st = res["status"]
        counts[st] = counts.get(st, 0) + 1
        msg = f" - {res['message']}" if "message" in res else ""
        print(f"[{icons.get(st, '•')} {st}] {res['element']} (Rule {res['rule_id']}){msg}")

    print("=" * 25)
    print(f"Total Rules Checked: {len(results)}")
    print(f"Passed: {counts['PASS']}")
    print(f"Warnings (benchmarks): {counts['WARN']}")
    print(f"Failed (statutory): {counts['FAIL']}")
    print("=========================\n")


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "extracted_apartment.json"
    data = load_apartment(path)
    rules = load_okf_rules("okf_rules")
    apartments = [a for f in data.get("floors", []) for a in f.get("apartments", [])] if "floors" in data else [data]
    for apartment in apartments:
        print_report(run_validation(apartment, rules))
