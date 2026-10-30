import fitz
import os, math
from collections import Counter

DWFX_PATH = r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה\6.5.26-hagasha.dwfx"
doc = fitz.open(DWFX_PATH)
page = doc[0]
print("Page rect:", page.rect, "Rotation:", page.rotation)
W_pt, H_pt = page.rect.width, page.rect.height
# Since 9000mm x 1000mm at 1:100 is 900m x 100m in real-world 1:100 units:
# Let's check the exact scale factor PT_PER_M:
# 1 inch = 25.4 mm = 72 pt -> 10 mm (1m at 1:100) = 72 / 25.4 * 10 = 28.3464567 pt/m
PT_PER_M = 72.0 / 25.4 * 10.0
print(f"Page in 1:100 meters: {W_pt / PT_PER_M:.3f}m x {H_pt / PT_PER_M:.3f}m")

drawings = page.get_drawings()
print("Total drawings:", len(drawings))

# Let's inspect the bounding boxes of the 9 floor plan crops we rendered earlier!
# Recall in inspect_dwfx_details.py we used normalized coordinates (nx0, ny0, nx1, ny1).
# Let's check what colors, widths, and fills exist in the typical floor plan region!
# Typical floors 1,2,6,7 was around nx=[0.33..0.52], ny=[0.02..0.48] or similar.
# Let's read inspect_dwfx_details.py to see the exact normalized boxes we used.
with open(r"C:\Users\User\.gemini\antigravity\brain\71931cc9-7058-41f3-a9f0-80549e5c535b\scratch\inspect_dwfx_details.py", "r", encoding="utf-8") as f:
    print(f.read())
