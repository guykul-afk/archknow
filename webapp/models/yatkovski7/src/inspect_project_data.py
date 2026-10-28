import os
import json
import zipfile
import fitz

base_dir = r"G:\Shared drives\פרויקטים שוטפים\פרויקטים בביצוע\יטקובסקי 7"
scratch_dir = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch"

# 1. Inspect DWF file structure (DWF is a zip or binary container)
dwf_path = os.path.join(base_dir, r"תכנון וביצוע\אדריכלות\יטקובסקי-תכניות וחזיתות.dwf")
if os.path.exists(dwf_path):
    print("DWF exists, size:", os.path.getsize(dwf_path))
    if zipfile.is_zipfile(dwf_path):
        with zipfile.ZipFile(dwf_path, 'r') as z:
            print("DWF zip contents:", z.namelist()[:30])

# 2. Extract text from key PDFs
pdfs_to_read = [
    r"הסכם קומבינציה\נסח יטקובסקי 7 פתח תקוה - 12 בדצמבר 2023.pdf",
    r"הסכם קומבינציה\יטקובסקי 7 - נספח להסכם הקומבינציה.pdf",
    r"הסכם קומבינציה\מפרט טכני עקרוני - פרויקט יטקובסקי 7.pdf",
    r"תכנון וביצוע\תבע ונספחים מאושרים למתן תוקף\410-1272517 הוראות התכנית 15_02_2026.pdf",
    r"תכנון וביצוע\אדריכלות\גרסאות קודמות\2026-01-05 - יטקובסקי-בינוי-5-1-26.pdf",
    r"תכנון וביצוע\תוכנית פיתוח\תוכנית פיתוח - 22-07-2026.pdf",
    r"תכנון וביצוע\תנועה וחניה\נספח תנועה וחניה - גרסה 9 - 19-07-2026.pdf",
    r"תכנון וביצוע\מדידות\2023-344B-Model.pdf",
]

summary_out = {}
for rel in pdfs_to_read:
    p = os.path.join(base_dir, rel)
    if not os.path.exists(p):
        print("Missing:", p)
        continue
    doc = fitz.open(p)
    pages_text = []
    for i, page in enumerate(doc):
        t = page.get_text("text")
        pages_text.append(f"--- PAGE {i+1} ({page.rect.width:.0f}x{page.rect.height:.0f}) ---\n" + t[:3000])
    summary_out[rel] = {
        "page_count": len(doc),
        "pages": pages_text
    }
    print(f"Read {rel}: {len(doc)} pages")

with open(os.path.join(scratch_dir, "pdfs_text_dump.json"), "w", encoding="utf-8") as f:
    json.dump(summary_out, f, ensure_ascii=False, indent=2)
print("Saved pdfs_text_dump.json")
