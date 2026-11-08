"""
Comprehensive Verification Suite for ArchiCheck System Upgrades:
- spatial_intelligence_engine.py (Sightlines, Zero-Line Closet Solver, Furnishability, Livability, Vertical Stack)
- design_optimization_engine.py (5-Pillar Contractor Constructability & Developer Revenue Yield + Dynamic BoQ)
- export_engine.py (AutoCAD R2010 DXF Redline Overlay + 5-Sheet OpenXML .xlsx BoQ Exporter)
- cad_parser.py (Multi-Floor & Underground Parking DXF Parser with Polygons & Dimensions)
- server.py / api_v1.py (REST Export & Spatial Intelligence Endpoints)
"""
import io
import os
import tempfile
import zipfile
import ezdxf

from spatial_intelligence_engine import (
    compute_sightline_and_aesthetics_metrics,
    solve_zero_line_closet_niche,
    simulate_apartment_furnishability,
    analyze_resident_livability,
    audit_multi_floor_vertical_stack,
)
from design_optimization_engine import build_project_design_optimization
from export_engine import generate_project_dxf_redline, generate_project_excel_boq
from project_analyzer_service import analyze_project_by_query
from cad_parser import parse_multi_apartment_cad


SAMPLE_APARTMENT = {
    "apartment_id": "דירה 4 (קומה ב׳)",
    "orientations": ["S", "W", "N"],
    "rooms": [
        {"id": "ENT", "type": "entrance", "name": "מבואת כניסה", "area_sqm": 2.4, "width_cm": 135, "length_cm": 180},
        {"id": "LIV", "type": "living_room", "name": "סלון", "area_sqm": 22.0, "width_cm": 400, "length_cm": 550},
        {"id": "DIN", "type": "dining", "name": "פינת אוכל", "area_sqm": 7.5, "width_cm": 260, "length_cm": 290},
        {"id": "KIT", "type": "kitchen", "name": "מטבח", "area_sqm": 9.2, "width_cm": 260, "length_cm": 355},
        {"id": "COR", "type": "corridor", "name": "מסדרון", "area_sqm": 5.4, "width_cm": 105, "length_cm": 510},
        {"id": "MBR", "type": "bedroom", "name": "חדר שינה הורים", "area_sqm": 13.2, "width_cm": 330, "length_cm": 400},
        {"id": "BR2", "type": "bedroom", "name": "חדר ילדים", "area_sqm": 10.4, "width_cm": 285, "length_cm": 365},
        {"id": "MMD", "type": "safe_room", "name": "ממ\"ד", "area_sqm": 9.8, "width_cm": 280, "length_cm": 350},
        {"id": "BTH", "type": "bathroom", "name": "חדר רחצה כללי", "area_sqm": 4.2, "width_cm": 175, "length_cm": 240},
        {"id": "WC", "type": "toilet", "name": "שירותי אורחים", "area_sqm": 1.8, "width_cm": 100, "length_cm": 180},
        {"id": "BAL", "type": "balcony", "name": "מרפסת שמש", "area_sqm": 14.0, "width_cm": 240, "length_cm": 580},
    ],
    "topology": [
        {"source": "EXT", "target": "ENT", "type": "door", "width_cm": 90},
        {"source": "ENT", "target": "LIV", "type": "opening", "width_cm": 140},
        {"source": "LIV", "target": "DIN", "type": "opening", "width_cm": 240},
        {"source": "LIV", "target": "KIT", "type": "opening", "width_cm": 220},
        {"source": "LIV", "target": "BAL", "type": "door", "width_cm": 280},
        {"source": "LIV", "target": "COR", "type": "opening", "width_cm": 110},
        {"source": "COR", "target": "MBR", "type": "door", "width_cm": 80},
        {"source": "COR", "target": "BR2", "type": "door", "width_cm": 80},
        {"source": "COR", "target": "MMD", "type": "door", "width_cm": 80},
        {"source": "COR", "target": "BTH", "type": "door", "width_cm": 70},
        {"source": "ENT", "target": "WC", "type": "door", "width_cm": 70},
    ],
}


def test_sightlines_and_zero_line_closet_solver():
    apt = dict(SAMPLE_APARTMENT)
    metrics = compute_sightline_and_aesthetics_metrics(apt)
    assert metrics["status"] == "OK"
    assert metrics["diagonal_sightline_ratio"] >= 1.15
    assert metrics["genkan_depth_m"] >= 1.20
    assert metrics["max_balcony_winter_garden_depth_m"] == 2.40

    # Test Zero-Line Closet Solver: Valid dry bedroom pair vs. Forbidden wet/structural target
    rooms = SAMPLE_APARTMENT["rooms"]
    topo = SAMPLE_APARTMENT["topology"]
    mbr = next(r for r in rooms if r["id"] == "MBR")
    niche_res = solve_zero_line_closet_niche(mbr, rooms, topo)
    assert niche_res["feasible"] is True
    assert niche_res["niche_depth_cm"] == 62

    mmd = next(r for r in rooms if r["id"] == "MMD")
    mmd_res = solve_zero_line_closet_niche(mmd, rooms, topo)
    assert mmd_res["feasible"] is False


def test_furnishability_and_livability_engines():
    # Zero-Trust abstention check on empty dict
    assert simulate_apartment_furnishability({})["status"] == "INSUFFICIENT_DATA"
    assert analyze_resident_livability({})["status"] == "INSUFFICIENT_DATA"

    furn = simulate_apartment_furnishability(SAMPLE_APARTMENT)
    assert furn["status"] == "OK"
    assert furn["furnishability_score"] >= 80
    assert len(furn["room_simulations"]) == 3  # MBR, BR2, MMD
    assert furn["hosting_12_guests"]["status"] == "PASS"

    liv = analyze_resident_livability(SAMPLE_APARTMENT)
    assert liv["status"] == "OK"
    assert liv["acoustic_shield_score"] >= 80
    assert liv["solar_and_ventilation"]["cross_ventilation_potential"] in ("HIGH", "MODERATE")
    assert liv["entry_stroller_and_robot_vacuum_zone"]["has_stroller_park_zone"] is True


def test_multi_floor_vertical_stack_auditor():
    floors = [
        {"floor_name": "קומה א׳", "apartments": [SAMPLE_APARTMENT]},
        {"floor_name": "קומה ב׳", "apartments": [SAMPLE_APARTMENT]},
    ]
    res = audit_multi_floor_vertical_stack(floors)
    assert res["status"] == "OK"
    assert res["mamad_continuity_estimated_pct"] >= 70.0
    assert res["mamad_vertical_continuity_status"] == "PASS"
    assert res["wet_shaft_alignment_status"] == "PASS"


def test_contractor_constructability_and_yield_engine():
    # Zero-Trust abstention on empty data_summary
    empty_opt = build_project_design_optimization("custom_empty", {})
    assert empty_opt["validation_status"] == "INSUFFICIENT_DATA"
    assert empty_opt["contractor_constructability_and_yield"]["total_constructability_saving_ils"] == 0

    # Full verified project
    payload = analyze_project_by_query("pines48", rebuild_artifacts=False)
    opt = payload["design_optimization"]
    ccy = opt.get("contractor_constructability_and_yield")
    assert ccy is not None
    assert ccy["validation_status"] == "VERIFIED"
    assert ccy["total_constructability_saving_ils"] > 100000
    assert ccy["total_developer_yield_uplift_ils"] > 100000
    assert len(ccy["pillars"]) == 5


def test_dxf_and_excel_exporters():
    payload = analyze_project_by_query("hafetz44", rebuild_artifacts=False)

    # 1. DXF Redline Overlay
    dxf_bytes = generate_project_dxf_redline(payload)
    assert len(dxf_bytes) > 1000
    doc = ezdxf.read(io.StringIO(dxf_bytes.decode("utf-8")))
    layer_names = {layer.dxf.name for layer in doc.layers}
    assert "ARCHICHECK-VE-CONTOUR-BEFORE" in layer_names
    assert "ARCHICHECK-VE-CONTOUR-AFTER" in layer_names
    assert "ARCHICHECK-STALL-RELOC" in layer_names

    # 2. Excel (.xlsx) Multi-Sheet Workbook
    xlsx_bytes = generate_project_excel_boq(payload)
    assert len(xlsx_bytes) > 2000
    with zipfile.ZipFile(io.BytesIO(xlsx_bytes), "r") as zf:
        names = set(zf.namelist())
        assert "xl/workbook.xml" in names
        assert "xl/worksheets/sheet1.xml" in names
        assert "xl/worksheets/sheet5.xml" in names


def test_upgraded_cad_parser_with_basement_and_polygons():
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    for lname in ("A-TITLE", "A-AREA-APT", "A-WALL", "A-TEXT", "A-PARK"):
        doc.layers.add(name=lname)

    # Floor 1: Underground Parking Basement (x around 0)
    msp.add_text("מרתף חניון -1", dxfattribs={"layer": "A-TITLE", "height": 50, "insert": (0, 1200)})
    msp.add_lwpolyline([(0, 0), (250, 0), (250, 500), (0, 500), (0, 0)], dxfattribs={"layer": "A-PARK"})
    msp.add_lwpolyline([(300, 0), (550, 0), (550, 500), (300, 500), (300, 0)], dxfattribs={"layer": "A-PARK"})

    # Floor 2: Typical Residential Floor (x around 20,000)
    msp.add_text("קומה א׳", dxfattribs={"layer": "A-TITLE", "height": 50, "insert": (20000, 1200)})
    msp.add_lwpolyline(
        [(20000, 0), (21000, 0), (21000, 1000), (20000, 1000), (20000, 0)],
        dxfattribs={"layer": "A-AREA-APT"},
    )
    msp.add_text("דירה 1", dxfattribs={"layer": "A-TEXT", "height": 35, "insert": (20100, 900)})
    # Living room polygon (400x500 cm = 20 sqm)
    msp.add_lwpolyline(
        [(20050, 50), (20450, 50), (20450, 550), (20050, 550), (20050, 50)],
        dxfattribs={"layer": "A-WALL"},
    )
    msp.add_text("סלון", dxfattribs={"layer": "A-TEXT", "height": 20, "insert": (20200, 250)})
    # Safe room Mamad polygon (300x340 cm = 10.2 sqm)
    msp.add_lwpolyline(
        [(20500, 50), (20800, 50), (20800, 390), (20500, 390), (20500, 50)],
        dxfattribs={"layer": "A-WALL"},
    )
    msp.add_text("ממ\"ד", dxfattribs={"layer": "A-TEXT", "height": 20, "insert": (20600, 200)})

    with tempfile.TemporaryDirectory() as tmpdir:
        dxf_path = os.path.join(tmpdir, "test_multi_floor.dxf")
        json_path = os.path.join(tmpdir, "out.json")
        doc.saveas(dxf_path)
        proj = parse_multi_apartment_cad(dxf_path, json_path)
        assert len(proj["floors"]) == 2
        ug_floor = next(f for f in proj["floors"] if f.get("floor_type") == "underground_parking")
        assert ug_floor["parking_summary"]["stalls_detected"] == 2
        res_floor = next(f for f in proj["floors"] if f.get("floor_type") == "residential")
        apt = res_floor["apartments"][0]
        mmd = next(r for r in apt["rooms"] if r["type"] == "safe_room")
        assert mmd["width_cm"] == 300.0
        assert len(mmd["polygon"]) >= 4
        assert "spatial_intelligence" in apt


def test_flask_export_and_spatial_endpoints():
    from server import app

    client = app.test_client()
    r_dxf = client.get("/api/export/dxf?project=pines48")
    assert r_dxf.status_code == 200
    assert b"ARCHICHECK-VE-CONTOUR-AFTER" in r_dxf.data

    r_xls = client.get("/api/export/excel?project=kkl10")
    assert r_xls.status_code == 200
    assert len(r_xls.data) > 2000

    r_si = client.post("/api/spatial_intelligence", json={"apartment": SAMPLE_APARTMENT})
    assert r_si.status_code == 200
    data = r_si.get_json()
    assert data["status"] == "success"
    assert data["furnishability_simulation"]["status"] == "OK"
