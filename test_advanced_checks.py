"""Tests for validation_engine v2 advanced checks.

Run:  python test_advanced_checks.py      (or: python -m pytest test_advanced_checks.py)
"""
import copy
import json

from validation_engine import load_okf_rules, run_validation, run_advanced_checks, _min_bounding_rect_area, _poly_area

RULES = load_okf_rules("okf_rules")


def by_element(results, fragment):
    return [r for r in results if fragment in r["element"]]


# --------------------------------------------------------------------------
# 1. Knowledge base: new files load and thresholds come from the files
# --------------------------------------------------------------------------
def test_new_rule_files_loaded():
    ids = {str(r.get("rule_id")) for r in RULES if isinstance(r, dict)}
    for rid in [
        "WBS_NDSS_ADG", "NKBA_KB", "APL_HOUSING", "SPACE_SYNTAX_SAGA",
        "IS1918_ACCESS", "SOURCES_REGISTRY", "DAYLIGHT_VENT_IEQ", "USABILITY_FURNISH_HQI",
        "ACADEMIC_ARCH_COMPENDIUM", "ETH_TYPO_1", "ETSAB_CC_1", "TUD_HERTZ_1",
        "SWISS_GK_1", "LV_PLUS_1", "JPN_SB_1", "FAM_VERT_1",
        "IL_OREF_2025", "IL_MOCH_PROG", "IL_MOT_PARK", "IL_IS1004_1142",
    ]:
        assert rid in ids, f"{rid} not loaded from okf_rules"


def test_threshold_read_from_knowledge_file():
    # Change the threshold in a copy of the loaded rules -> engine must follow the file, not the fallback.
    rules = copy.deepcopy(RULES)
    for r in rules:
        if isinstance(r, dict) and r.get("rule_id") == "SPACE_SYNTAX_SAGA":
            r["corridor_ratio_good_max"] = 0.50
    apt = {"rooms": [{"id": "A", "type": "living_room", "area_sqm": 20}, {"id": "B", "type": "corridor", "area_sqm": 6}]}
    res = by_element(run_advanced_checks(apt, rules), "EF-1")[0]
    assert res["status"] == "PASS", res  # 23% would be WARN with the default 10%


# --------------------------------------------------------------------------
# 2. Backward compatibility: legacy statutory results are unchanged
# --------------------------------------------------------------------------
def test_legacy_statutory_checks_unchanged():
    with open("apartment_schema.json", encoding="utf-8") as f:
        apt = json.load(f)
    res = run_validation(apt, RULES)
    statutory = [r for r in res if r["rule_id"] in {"B1.13", "B1.3", "B1.6", "B1.9", "B1.11", "B1.15", "B44", "A17"}]
    assert all(r["status"] in ("PASS", "FAIL") for r in statutory)
    # the 6.5 sqm bedroom must still FAIL B1.6, and no advanced check may emit FAIL
    assert any(r["rule_id"] == "B1.6" and r["status"] == "FAIL" for r in res)
    advanced = run_advanced_checks(apt, RULES)
    assert all(r["status"] in ("PASS", "WARN") for r in advanced)


# --------------------------------------------------------------------------
# 3. Pines 48 — Apartment C (4 rooms, 92+12 sqm), dimensions from the 1:50 model
# --------------------------------------------------------------------------
PINES_C = {
    "apartment_id": "Pines 48 - Apt C",
    "global_parameters": {"ceiling_height_m": 2.67},
    "accessibility": {"main_entrance_width_cm": 90},
    "orientations": ["S", "E"],
    "rooms": [
        {"id": "LIV", "type": "living_room", "name": "סלון C", "area_sqm": 19.20, "width_cm": 400},
        {"id": "KIT", "type": "kitchen", "name": "מטבח C", "area_sqm": 8.16, "width_cm": 245},
        {"id": "COR", "type": "corridor", "name": "מסדרון C", "area_sqm": 8.69, "width_cm": 110},
        {"id": "MBR", "type": "bedroom", "name": "חדר הורים C", "area_sqm": 11.51, "width_cm": 295},
        {"id": "ENS", "type": "bathroom", "name": "רחצה הורים C", "area_sqm": 3.09, "width_cm": 165, "has_window": True},
        {"id": "BR2", "type": "bedroom", "name": "חדר דרומי C", "area_sqm": 9.32, "width_cm": 270},
        {"id": "MMD", "type": "safe_room", "name": "ממד C", "area_sqm": 9.49, "width_cm": 292},
        {"id": "BTH", "type": "bathroom", "name": "רחצה כללי C", "area_sqm": 3.74, "width_cm": 170, "has_window": True},
        {"id": "SRV", "type": "utility", "name": "שירות C", "area_sqm": 2.53},
        {"id": "BAL", "type": "balcony", "name": "מרפסת C", "area_sqm": 12.0, "depth_m": 2.0},
    ],
    "topology": [
        {"source": "EXT", "target": "LIV", "type": "door"},
        {"source": "LIV", "target": "KIT", "type": "opening"},
        {"source": "LIV", "target": "BAL", "type": "door"},
        {"source": "LIV", "target": "COR", "type": "opening"},
        {"source": "COR", "target": "MBR", "type": "door"},
        {"source": "COR", "target": "BR2", "type": "door"},
        {"source": "COR", "target": "MMD", "type": "door"},
        {"source": "COR", "target": "BTH", "type": "door"},
        {"source": "COR", "target": "SRV", "type": "door"},
        {"source": "MBR", "target": "ENS", "type": "door"},
    ],
}


def test_pines_c_statutory_all_pass():
    res = run_validation(PINES_C, RULES)
    assert not [r for r in res if r["status"] == "FAIL"], [r for r in res if r["status"] == "FAIL"]


def test_pines_c_findings_match_manual_review():
    res = run_advanced_checks(PINES_C, RULES)
    # Entrance opens straight into the living room -> B1.2 / APL#112 warning (manual review finding)
    assert by_element(res, "SS-3")[0]["status"] == "WARN"
    # Corridor 8.69 / 76.4 sqm (room sum excl. balcony) = 11.4% -> borderline WARN
    ef1 = by_element(res, "EF-1")[0]
    assert ef1["status"] == "WARN" and "11." in ef1["message"], ef1
    # Bedrooms 2.70-2.95 m wide: meet NDSS, below ADG 3.0 m
    br2 = by_element(res, "חדר דרומי C")[0]
    assert br2["status"] == "WARN" and "ADG" in br2["message"], br2
    # Privacy gradient and wet-room privacy are good
    assert by_element(res, "SS-2")[0]["status"] == "PASS"
    assert by_element(res, "SS-4")[0]["status"] == "PASS"
    assert by_element(res, "SS-5")[0]["status"] == "PASS"
    # Living room is the most integrated space
    assert by_element(res, "SS-1")[0]["status"] == "PASS"
    # Balcony 12 sqm x 2.0 m: below ADG 3-bed depth 2.4 m
    bal = by_element(res, "מרפסת")[0]
    assert bal["status"] == "WARN" and "2.4" in bal["message"], bal
    # No storage data in the model -> B7 cannot be verified
    assert by_element(res, "נפח אחסון")[0]["status"] == "WARN"
    # Kitchen clearances were not measured in the model -> NKBA check must stay silent (zero-trust)
    assert not by_element(res, "NKBA")
    # Dual aspect
    assert by_element(res, "כיווניות")[0]["status"] == "PASS"
    # Ceiling 2.67 < ADG 2.7 but >= London 2.5
    ceil = by_element(res, "גובה תקרה מול ADG")[0]
    assert ceil["status"] == "WARN" and "עומד ברף London" in ceil["message"], ceil


# --------------------------------------------------------------------------
# 4. Synthetic edge cases
# --------------------------------------------------------------------------
def test_bad_topology_detected():
    apt = {
        "entrance_room_id": "LIV",
        "rooms": [
            {"id": "LIV", "type": "living_room", "area_sqm": 20},
            {"id": "WC", "type": "toilet", "area_sqm": 1.5},
            {"id": "B1", "type": "bedroom", "area_sqm": 10},
            {"id": "B2", "type": "bedroom", "area_sqm": 9},
        ],
        "topology": [
            {"source": "LIV", "target": "WC"},  # toilet opens onto living room
            {"source": "LIV", "target": "B1"},
            {"source": "B1", "target": "B2"},   # B1 is a pass-through bedroom
        ],
    }
    res = run_advanced_checks(apt, RULES)
    assert by_element(res, "SS-4")[0]["status"] == "WARN"
    assert by_element(res, "SS-5")[0]["status"] == "WARN"
    assert by_element(res, "SS-3")[0]["status"] == "WARN"


def test_low_topology_coverage_skips_metrics():
    apt = {"rooms": [{"id": f"R{i}", "type": "bedroom", "area_sqm": 9} for i in range(10)],
           "topology": [{"source": "R0", "target": "R1"}]}
    res = by_element(run_advanced_checks(apt, RULES), "Space Syntax")
    assert len(res) == 1 and res[0]["status"] == "WARN" and "לא חושבו" in res[0]["message"]


def test_rectangularity():
    square = [[0, 0], [3, 0], [3, 3], [0, 3]]
    assert abs(_poly_area(square) / _min_bounding_rect_area(square) - 1.0) < 1e-9
    rotated = [[0, 0], [2, 2], [0, 4], [-2, 2]]  # square rotated 45 degrees
    assert abs(_poly_area(rotated) / _min_bounding_rect_area(rotated) - 1.0) < 1e-9
    l_shape = [[0, 0], [4, 0], [4, 1.5], [1.5, 1.5], [1.5, 4], [0, 4]]
    apt = {"rooms": [{"id": "L", "type": "bedroom", "area_sqm": 9.75, "polygon": l_shape}]}
    res = by_element(run_advanced_checks(apt, RULES), "EF-2")[0]
    assert res["status"] == "WARN", res  # 9.75 / 16 = 0.61


def test_accessibility_only_when_declared():
    apt = {"rooms": [{"id": "B", "type": "bathroom", "area_sqm": 4, "door_width_cm": 70}]}
    assert not by_element(run_advanced_checks(apt, RULES), "מעגל סיבוב")
    apt["accessible_unit"] = True
    res = run_advanced_checks(apt, RULES)
    assert by_element(res, "מעגל סיבוב")[0]["status"] == "WARN"
    door = by_element(res, "דלתות פנים")[0]
    assert door["status"] == "WARN" and "ת\"י 1918" in door["message"]


def test_nkba_triangle():
    apt = {"rooms": [{"id": "K", "type": "kitchen", "area_sqm": 10,
                      "kitchen_layout": {"work_triangle_legs_m": [3.0, 3.0, 2.5]}}]}
    res = by_element(run_advanced_checks(apt, RULES), "NKBA")[0]
    assert res["status"] == "WARN" and "8.50" in res["message"], res


def test_real_parsed_upload_does_not_crash():
    import glob
    for path in glob.glob("uploads/*_project.json")[:5]:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for fl in data.get("floors", []):
            for apt in fl.get("apartments", []):
                res = run_validation(apt, RULES)
                assert not [r for r in res if r["rule_id"] == "ENGINE"], [r for r in res if r["rule_id"] == "ENGINE"]


def test_daylight_vent_ieq_checks():
    apt = {
        "global_parameters": {"ceiling_height_m": 2.60},
        "orientations": ["W"],
        "sunlight_hours": 1.0,
        "cross_vent_path_m": 15.0,
        "rooms": [
            {
                "id": "LIV",
                "type": "living_room",
                "name": "סלון מערבי",
                "area_sqm": 20.0,
                "depth_m": 6.0,
                "ventilation_mode": "single_opening",
                "window_orientation": "W",
                "window_area_sqm": 6.0,
                "openable_window_area_sqm": 0.6,
                "view_distance_m": 4.0,
                "view_angle_deg": 10,
                "view_layers": 1,
                "no_sky_line_share": 0.65,
                "obstruction_angle_deg": 32.0,
                "distance_to_window_m": 8.2,
            }
        ],
    }
    res = run_advanced_checks(apt, RULES)
    assert by_element(res, "חשיפה לשמש ישירה (EN 17037)")[0]["status"] == "WARN"
    assert by_element(res, "עומק אוורור מפולש (CIBSE AM10)")[0]["status"] == "WARN"
    assert by_element(res, "סיכון התחממות יתר (CIBSE TM59)")[0]["status"] == "WARN"
    assert by_element(res, "איכות מבט החוצה EN 17037")[0]["status"] == "WARN"
    assert by_element(res, "קו שמיים No-Sky Line BR 209")[0]["status"] == "WARN"
    assert by_element(res, "זווית הסתרה BR 209")[0]["status"] == "WARN"
    assert by_element(res, "שטח פתיחה חופשי לאוורור")[0]["status"] == "WARN"
    assert by_element(res, "עומק אפקטיבי לאוורור CIBSE AM10")[0]["status"] == "WARN"
    assert by_element(res, "סיכון סנוור וחימום בחזית מערבית")[0]["status"] == "WARN"
    assert by_element(res, "מרחק מחלון מבט WELL v2")[0]["status"] == "WARN"


def test_usability_furnish_hqi_checks():
    apt = {
        "adaptable_partition_ratio": 0.45,
        "rooms": [
            {"id": "LIV", "type": "living_room", "name": "סלון קטן", "area_sqm": 13.0, "latch_side_clearance_cm": 40},
            {"id": "KIT", "type": "kitchen", "name": "מטבח", "area_sqm": 6.0},
            {
                "id": "B1",
                "type": "bedroom",
                "name": "חדר הורים",
                "area_sqm": 12.0,
                "unbroken_wall_m": 2.65,
                "wardrobe_wall_m": 1.40,
                "door_corner_offset_cm": 35,
                "bedside_clearance_cm": 70,
                "adjacent_to_noisy_zone": True,
            },
            {"id": "B2", "type": "bedroom", "name": "חדר 2", "area_sqm": 10.0},
            {"id": "B3", "type": "bedroom", "name": "חדר 3", "area_sqm": 10.0},
            {"id": "MMD", "type": "safe_room", "name": "ממד", "area_sqm": 9.5},
        ],
    }
    res = run_advanced_checks(apt, RULES)
    # 5 bedspaces (1 double + 3 singles) with 13 sqm living & 19 sqm combined public -> WARN on HQI proportionality
    assert by_element(res, "איזון פרוגרמטי")[0]["status"] == "WARN"
    assert by_element(res, "יכולת ריהוט Möblerbarhet")[0]["status"] == "WARN"
    assert by_element(res, "מרווח גישה לצד מיטה DIN 18040-2")[0]["status"] == "WARN"
    assert by_element(res, "חיץ אקוסטי לחדר שינה CBE POE")[0]["status"] == "WARN"
    assert by_element(res, "מרווח צד ידית דלת DIN 18040-2")[0]["status"] == "WARN"
    assert by_element(res, "גמישות מחיצות פנים — EU Level(s) 2.3")[0]["status"] == "WARN"


def test_qualitative_prompt_includes_new_compendia():
    from qualitative_analyzer import build_prompt
    prompt = build_prompt(PINES_C, "okf_rules")
    assert "DAYLIGHT_VENT_IEQ" in prompt
    assert "USABILITY_FURNISH_HQI" in prompt
    assert "ACADEMIC_ARCH_COMPENDIUM" in prompt
    assert "ETSAB_CC_1" in prompt
    assert "IL_MOCH_PROG" in prompt
    assert "(Missing knowledge files:" not in prompt


def test_academic_and_new_standards_checks():
    apt = {
        "net_area_sqm": 82.0,
        "central_hall_width_m": 2.40,
        "diagonal_sightline_ratio": 1.20,
        "kitchen_counter_upstand_cm": 10,
        "genkan_depth_m": 0.85,
        "party_wall_db": 45,
        "balcony_railing_height_cm": 100,
        "railing_gap_cm": 12,
        "parking": {"stall_width_m": 2.40, "adjacent_columns_or_walls": 1, "aisle_width_m": 5.10},
        "rooms": [
            {"id": "LIV", "type": "living_room", "name": "סלון", "area_sqm": 20.0},
            {"id": "B1", "type": "bedroom", "name": "חדר הורים", "area_sqm": 14.5, "width_cm": 285},
            {"id": "B2", "type": "bedroom", "name": "חדר ילדים", "area_sqm": 8.4, "width_cm": 270},
            {"id": "MMD", "type": "safe_room", "name": "ממד", "area_sqm": 9.2, "width_cm": 280, "wet_room_area_sqm": 3.5, "external_wall_plumbing": True},
            {"id": "BTH", "type": "bathroom", "name": "חדר רחצה יחיד", "area_sqm": 4.0},
            {"id": "BAL", "type": "balcony", "name": "מרפסת", "area_sqm": 10.0, "depth_m": 2.0, "winter_garden_depth_m": 2.2},
        ],
    }
    res = run_advanced_checks(apt, RULES)
    assert by_element(res, "ETSAB_CC_1")[0]["status"] == "WARN"
    assert by_element(res, "IL_MOCH_PROG")[0]["status"] == "WARN"
    assert by_element(res, "FAM_VERT_1")[0]["status"] == "WARN"
    assert by_element(res, "San-ten Bunri (JPN_SB_1)")[0]["status"] == "WARN"
    assert by_element(res, "Genkan (JPN_SB_1)")[0]["status"] == "WARN"
    assert by_element(res, "LV_PLUS_1")[0]["status"] == "WARN"
    assert by_element(res, "ETH_TYPO_1")[0]["status"] == "WARN"
    assert by_element(res, "SWISS_GK_1")[0]["status"] == "WARN"
    assert by_element(res, "TUD_HERTZ_1")[0]["status"] == "WARN"
    assert by_element(res, "IL_OREF_2025")[0]["status"] == "WARN"
    assert by_element(res, "IL_MOT_PARK")[0]["status"] == "WARN"
    assert by_element(res, "IL_IS1004_1142")[0]["status"] == "WARN"


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL  {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    raise SystemExit(1 if failed else 0)
