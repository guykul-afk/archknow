"""
Render High-Resolution Original Architectural Plans (תוכניות המקור) for:
1. Feierberg 3, Tel Aviv (פאירברג 3, תל אביב) — from FA-hagsha-הגשה בצבע (1).dwfx
2. Yatkovski 7, Petah Tikva (יטקובסקי 7, פתח תקווה) — from 2026-01-05 - יטקובסקי-בינוי-5-1-26.pdf
3. Moshe Sharet 26-28, Petah Tikva (משה שרת 26-28, פתח תקווה) — from 6.5.26-hagasha.dwfx

Saves clean, full-color original CAD/Gramoshka plans into both `webapp/uploads/` and `uploads/`.
"""

import os
import shutil
import fitz  # PyMuPDF

OUT_DIR_WEBAPP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "webapp", "uploads")
OUT_DIR_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(OUT_DIR_WEBAPP, exist_ok=True)
os.makedirs(OUT_DIR_ROOT, exist_ok=True)

FEIERBERG3_DWFX = r"G:\Shared drives\פרויקטים שוטפים\פרויקטים בביצוע\פאירברג 3\FA-hagsha-הגשה בצבע (1).dwfx"
YATKOVSKI7_PDF = r"G:\Shared drives\פרויקטים שוטפים\פרויקטים בביצוע\יטקובסקי 7\תכנון וביצוע\אדריכלות\גרסאות קודמות\2026-01-05 - יטקובסקי-בינוי-5-1-26.pdf"
SHARETT26_DWFX = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה\6.5.26-hagasha.dwfx"

FEIERBERG3_CROPS = {
    "feierberg3_basement1.png": (9530, 160, 10680, 880),
    "feierberg3_basement2.png": (9530, 885, 10680, 1620),
    "feierberg3_ground.png": (8380, 220, 9540, 1480),
    "feierberg3_typical.png": (7320, 240, 8300, 880),
    "feierberg3_floor9.png": (7320, 950, 8300, 1590),
    "feierberg3_floor10.png": (6290, 240, 7280, 880),
}

YATKOVSKI7_CROPS = {
    "yatkovski7_basement.png": (4180, 800, 5020, 2000),
    "yatkovski7_ground.png": (2900, 800, 4180, 2380),
    "yatkovski7_typical.png": (2180, 1050, 2920, 2260),
    "yatkovski7_floor5.png": (1380, 1050, 2140, 2260),
    "yatkovski7_penthouse.png": (580, 1050, 1340, 2260),
}

SHARETT26_PT_PER_M = 72.0 / 0.0254 / 100.0  # 28.3464567 pt/m at 1:100 scale
SHARETT26_WINDOW_M = (-23.0, -20.0, 23.0, 20.0)  # X in [-23, +23] (46m), Z in [-20, +20] (40m)
SHARETT26_ANCHORS_M = {
    "sharett26_typical.png": (227.492, 25.065),      # floors_345 (Typical Floors 1-7)
    "sharett26_floor8.png": (178.444, 25.065),       # floor_8 (Penthouses #32 & #33 + 4 North units)
    "sharett26_floor9_roof.png": (129.399, 25.065),  # floor_9_roof (Roof terraces & solar roof)
    "sharett26_gallery.png": (332.709, 25.067),      # gallery (Upper duplexes #1-#4 & lobby voids)
    "sharett26_ground.png": (398.495, 35.858),       # ground (Lobbies, Garden Duplexes #1-#4 & lot)
    "sharett26_basement1.png": (462.499, 72.338),    # basement_1 (33 stalls #1-#33 & west ramp)
    "sharett26_basement2.png": (461.627, 24.927),    # basement_2 (37 stalls #34-#70 & water tank)
}


def _save_to_both(filename: str, pix: fitz.Pixmap) -> None:
    dst_webapp = os.path.join(OUT_DIR_WEBAPP, filename)
    dst_root = os.path.join(OUT_DIR_ROOT, filename)
    pix.save(dst_webapp)
    shutil.copy2(dst_webapp, dst_root)
    print(f"Saved original architectural plan: {dst_webapp} ({pix.width}x{pix.height})")


def render_feierberg3_original_plans() -> None:
    if not os.path.exists(FEIERBERG3_DWFX):
        print(f"WARNING: {FEIERBERG3_DWFX} not found, skipping Feierberg 3 extraction.")
        return
    doc = fitz.open(FEIERBERG3_DWFX)
    page = doc[0]
    mat = fitz.Matrix(2.2, 2.2)
    for fname, rect_tuple in FEIERBERG3_CROPS.items():
        pix = page.get_pixmap(matrix=mat, clip=fitz.Rect(*rect_tuple), alpha=False)
        _save_to_both(fname, pix)
    doc.close()


def render_yatkovski7_original_plans() -> None:
    if not os.path.exists(YATKOVSKI7_PDF):
        print(f"WARNING: {YATKOVSKI7_PDF} not found, skipping Yatkovski 7 extraction.")
        return
    doc = fitz.open(YATKOVSKI7_PDF)
    page = doc[0]
    mat = fitz.Matrix(2.0, 2.0)
    for fname, rect_tuple in YATKOVSKI7_CROPS.items():
        pix = page.get_pixmap(matrix=mat, clip=fitz.Rect(*rect_tuple), alpha=False)
        _save_to_both(fname, pix)
    doc.close()


def render_sharett26_original_plans() -> None:
    if not os.path.exists(SHARETT26_DWFX):
        print(f"WARNING: {SHARETT26_DWFX} not found, skipping Moshe Sharet 26-28 extraction.")
        return
    doc = fitz.open(SHARETT26_DWFX)
    page = doc[0]
    mat = fitz.Matrix(2.2, 2.2)
    x0_m, z0_m, x1_m, z1_m = SHARETT26_WINDOW_M
    for fname, (ax_m, ay_m) in SHARETT26_ANCHORS_M.items():
        clip_rect = fitz.Rect(
            (ax_m + x0_m) * SHARETT26_PT_PER_M,
            (ay_m + z0_m) * SHARETT26_PT_PER_M,
            (ax_m + x1_m) * SHARETT26_PT_PER_M,
            (ay_m + z1_m) * SHARETT26_PT_PER_M,
        )
        pix = page.get_pixmap(matrix=mat, clip=clip_rect, alpha=False)
        _save_to_both(fname, pix)
    doc.close()


if __name__ == "__main__":
    render_feierberg3_original_plans()
    render_yatkovski7_original_plans()
    render_sharett26_original_plans()
    print("All original architectural plans rendered successfully.")
