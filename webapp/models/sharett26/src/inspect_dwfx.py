import os
import sys
import zipfile
import fitz
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')
ws = r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה"
dwfx_path = os.path.join(ws, "6.5.26-hagasha.dwfx")

print("=== 1. CHECK OTHER MOSHE SHARETT FOLDER ===")
other_dir = r"G:\Shared drives\פרויקטים שוטפים\פרויקטים בביצוע\משה שרת"
if os.path.exists(other_dir):
    for root, dirs, files in os.walk(other_dir):
        for f in files:
            fp = os.path.join(root, f)
            print(f"  {fp} ({os.path.getsize(fp)} bytes)")

print("\n=== 2. TRY FITZ OPEN DWFX AS XPS ===")
try:
    doc = fitz.open(dwfx_path)
    print(f"Fitz opened DWFX directly! Pages: {len(doc)}")
    for i, page in enumerate(doc):
        drw = page.get_drawings()
        txt = page.get_text("text")
        print(f"  Page {i}: rect={page.rect}, drawings={len(drw)}, text_len={len(txt)}")
        print("  Sample text:", txt[:600].replace("\n", " | "))
except Exception as e:
    print("Fitz open failed:", e)

print("\n=== 3. INSPECT DWFX XML MANIFEST & DESCRIPTOR ===")
with zipfile.ZipFile(dwfx_path, 'r') as z:
    for name in z.namelist():
        if name.endswith("descriptor.xml") or name.endswith("DWFProperties.xml") or name.endswith(".dsd"):
            print(f"\n--- {name} ---")
            data = z.read(name).decode('utf-8', errors='replace')
            print(data[:2000])
