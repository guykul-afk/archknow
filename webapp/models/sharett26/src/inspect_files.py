import os
import sys
import zipfile
import fitz

sys.stdout.reconfigure(encoding='utf-8')
ws = r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה"
pdf_path = os.path.join(ws, "10000623388_28.10.2026 12.35.pdf")
dwfx_path = os.path.join(ws, "6.5.26-hagasha.dwfx")

print("=== PDF INSPECTION ===")
doc = fitz.open(pdf_path)
print("Pages:", len(doc))
for i, page in enumerate(doc):
    print(f"Page {i}: rect={page.rect}, drawings={len(page.get_drawings())}, images={len(page.get_images())}")
    txt = page.get_text("text")
    print(f"Text ({len(txt)} chars):")
    print(txt[:1500])

print("\n=== DWFX INSPECTION ===")
if zipfile.is_zipfile(dwfx_path):
    with zipfile.ZipFile(dwfx_path, 'r') as z:
        for info in z.infolist():
            print(f"{info.filename}: {info.file_size} bytes")
else:
    print("Not a zip file")
