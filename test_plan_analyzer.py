"""
Offline tests for plan_analyzer (no network): a synthetic 1:50 PDF plan with known
geometry is generated with PyMuPDF; the vision reading is injected via
`reading_override`, so geometry, fusion, QA and the engine adapter are tested
deterministically.

    python test_plan_analyzer.py
"""
import os
import sys
import tempfile
import unittest

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from plan_analyzer import analyze_pdf_to_project
from plan_analyzer.reading import normalise_reading
from plan_analyzer.taxonomy import classify_label
from validation_engine import run_validation, load_okf_rules

CM_PER_PT = 2.54 / 72 * 50          # 1:50
GRAY = (0.86, 0.86, 0.86)
PAGE_W, PAGE_H = 1191, 842          # A3 landscape (pt)


def pt(v_cm):
    return v_cm / CM_PER_PT


def rect(page, x0, y0, x1, y1):
    page.draw_rect(fitz.Rect(pt(x0), pt(y0), pt(x1), pt(y1)), color=(0, 0, 0), fill=GRAY, width=0.5)


def line(page, x0, y0, x1, y1, w=0.4):
    page.draw_line(fitz.Point(pt(x0), pt(y0)), fitz.Point(pt(x1), pt(y1)), color=(0, 0, 0), width=w)


def arc(page, cx, cy, sx, sy, beta):
    page.draw_sector(fitz.Point(pt(cx), pt(cy)), fitz.Point(pt(sx), pt(sy)), beta,
                     color=(0, 0, 0), width=0.4, fullSector=False)


def nbox(x0, y0, x1, y1):
    """cm box → Gemini box_2d (ymin, xmin, ymax, xmax) in 0..1000."""
    W, H = PAGE_W * CM_PER_PT, PAGE_H * CM_PER_PT
    return [y0 / H * 1000, x0 / W * 1000, y1 / H * 1000, x1 / W * 1000]


def build_plan(path):
    """Two rooms (living 375×450, bedroom 363×450), interior door 90, entrance 100,
    a 160 cm window with glazing lines, two dimension lines."""
    doc = fitz.open()
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    # exterior walls (25 cm) with a window gap (top) and the entrance gap (bottom)
    rect(page, 200, 200, 700, 225)
    rect(page, 860, 200, 1000, 225)
    rect(page, 200, 675, 300, 700)
    rect(page, 400, 675, 1000, 700)
    rect(page, 200, 200, 225, 700)
    rect(page, 975, 200, 1000, 700)
    # interior partition (12 cm) with a door gap y 400..490
    rect(page, 600, 225, 612, 400)
    rect(page, 600, 490, 612, 675)
    # window glazing: two lines along the gap
    line(page, 700, 209, 860, 209)
    line(page, 700, 216, 860, 216)
    # door swings
    arc(page, 612, 400, 702, 400, 90)     # interior door, swings into the bedroom
    arc(page, 300, 675, 300, 575, 90)     # entrance, swings into the living room
    # dimension lines (with ticks)
    line(page, 225, 300, 600, 300, 0.25)
    line(page, 260, 225, 260, 675, 0.25)
    doc.save(path)
    doc.close()


READING = {
    "source": "override",
    "sheet": {"project_name": "בדיקה", "city": "תל אביב", "plan_type": "sales_plan",
              "floors_text": "קומה 3", "floors": [3], "apartment_numbers": ["7"],
              "rooms_count": 2, "apartment_area_sqm": 40, "scale": "1:50",
              "north_arrow": {"present": True, "label_text": "צפון", "north_direction_deg": 0}},
    "spaces": [
        {"label": "סלון", "box_2d": nbox(380, 430, 450, 460), "inside_unit": True},
        {"label": "חדר שינה", "box_2d": nbox(750, 430, 850, 460), "inside_unit": True},
    ],
    "dimensions": [
        {"value": 375, "unit": "cm", "orientation": "horizontal", "box_2d": nbox(395, 285, 430, 297)},
        {"value": 450, "unit": "cm", "orientation": "vertical", "box_2d": nbox(247, 430, 257, 470)},
    ],
    "annotations": [], "fixtures": [], "notes": [],
}


class PlanAnalyzerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="plan_test_")
        cls.pdf = os.path.join(cls.tmp, "synthetic.pdf")
        build_plan(cls.pdf)
        cls.project, cls.model = analyze_pdf_to_project(cls.pdf, cls.tmp, "synthetic",
                                                        use_vision=False, reading_override=READING,
                                                        log=lambda *a: None)
        cls.sheet = cls.model["sheets"][0]
        cls.by_type = {}
        for s in cls.sheet["spaces"]:
            cls.by_type.setdefault(s["type"], []).append(s)

    def test_scale_verified_by_dimension_lines(self):
        cal = self.sheet["calibration"]
        self.assertEqual(cal["matched_dimensions"], 2)
        self.assertLess(cal["median_error_pct"], 2.0)

    def test_rooms_and_areas(self):
        living = self.by_type["living"][0]
        bed = self.by_type["bedroom"][0]
        self.assertAlmostEqual(living["area_sqm"], 3.75 * 4.50, delta=0.6)
        self.assertAlmostEqual(bed["area_sqm"], 3.63 * 4.50, delta=0.6)
        self.assertEqual(living["width_cm"], 375.0)          # written dimension preferred
        self.assertEqual(living["provenance"]["width_cm"], "written_dimension")

    def test_openings_classified(self):
        kinds = {}
        for o in self.sheet["openings"]:
            kinds.setdefault(o["kind"], []).append(o)
        doors = sorted(o["width_cm"] for o in kinds.get("door", []))
        self.assertEqual(len(doors), 2)
        self.assertAlmostEqual(doors[0], 90, delta=6)
        self.assertAlmostEqual(doors[1], 100, delta=6)
        wins = kinds.get("window", [])
        self.assertEqual(len(wins), 1)
        self.assertAlmostEqual(wins[0]["width_cm"], 160, delta=6)
        self.assertEqual(wins[0]["facing"], "N")

    def test_topology_and_entrance(self):
        living, bed = self.by_type["living"][0]["id"], self.by_type["bedroom"][0]["id"]
        pairs = {frozenset((e["source"], e["target"])) for e in self.sheet["topology"]}
        self.assertIn(frozenset((living, bed)), pairs)
        self.assertIn(frozenset(("EXT", living)), pairs)
        apt = self.sheet["apartment"]
        self.assertAlmostEqual(apt["main_entrance_width_cm"], 100, delta=6)
        self.assertEqual(apt["orientations"], ["N"])

    def test_qa_checks(self):
        qa = {q["check"]: q["status"] for q in self.sheet["qa"]}
        self.assertEqual(qa["קנה מידה ומידות כתובות"], "PASS")
        self.assertEqual(qa["רציפות טופולוגית"], "PASS")
        self.assertEqual(qa["מספר חדרים"], "PASS")

    def test_engine_adapter_and_validation(self):
        apt = self.project["floors"][0]["apartments"][0]
        self.assertEqual(apt["apartment_id"], "דירה 7")
        types = {r["type"] for r in apt["rooms"]}
        self.assertTrue({"living_room", "bedroom"} <= types)
        self.assertNotIn("ceiling_height_m", apt["global_parameters"])   # never invented
        bed = next(r for r in apt["rooms"] if r["type"] == "bedroom")
        self.assertTrue(bed["has_window"])
        self.assertAlmostEqual(bed["window_area_sqm"], 1.6 * 1.1, delta=0.15)
        rules = load_okf_rules(os.path.join(os.path.dirname(os.path.abspath(__file__)), "okf_rules"))
        res = run_validation(apt, rules)
        ceiling = next(r for r in res if r["rule_id"] == "B1.13")
        self.assertEqual(ceiling["status"], "WARN")                       # missing data ≠ violation
        entrance = next(r for r in res if r["rule_id"] == "B44")
        self.assertEqual(entrance["status"], "PASS")

    def test_plan_model_written(self):
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "synthetic_plan_model.json")))
        self.assertEqual(self.model["schema"], "archknow.plan-model/1.0")


class ReadingAndTaxonomyTests(unittest.TestCase):
    def test_taxonomy(self):
        self.assertEqual(classify_label('חדר שינה ממ"ד')[0], "safe_room")
        self.assertEqual(classify_label("שירותי אורחים")[0], "toilet")
        self.assertEqual(classify_label("חדר רחצה הורים")[0], "bathroom")
        self.assertEqual(classify_label("מרפסת 12 מ\"ר")[0], "balcony")
        self.assertEqual(classify_label("מסתור כביסה")[0], "service_balcony")
        self.assertEqual(classify_label("לובי קומתי")[0], "lobby")
        self.assertEqual(classify_label("חדר שרות")[0], "utility")

    def test_box_conversion_and_north_validation(self):
        rd = normalise_reading({"sheet": {"north_arrow": {"present": True, "label_text": "יציאה למרפסת",
                                                          "north_direction_deg": 180}},
                                "spaces": [{"label": "סלון", "box_2d": [100, 200, 300, 400]}]}, "vision")
        self.assertEqual(rd["spaces"][0]["box"], [0.2, 0.1, 0.4, 0.3])
        self.assertFalse(rd["sheet"]["north_arrow"]["present"])        # not labelled north → rejected


if __name__ == "__main__":
    unittest.main(verbosity=2)
