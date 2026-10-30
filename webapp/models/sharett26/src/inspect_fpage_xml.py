import zipfile, re
from collections import Counter

dwfx_path = r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה\6.5.26-hagasha.dwfx"
with zipfile.ZipFile(dwfx_path, 'r') as z:
    fpage = z.read("dwf/documents/20557152-C9F2-4F2A-83D0-E6D25FE4C692/sections/com.autodesk.dwf.ePlot_20557153-C9F2-4F2A-83D0-E6D25FE4C692/FixedPage.fpage").decode('utf-8', errors='replace')

print("fpage length:", len(fpage))
print("First 2500 chars:\n", fpage[:2500])

# Find all Path elements
paths = re.findall(r'<Path\s+([^>]+)/>', fpage)
print("Total <Path .../> elements:", len(paths))
for p in paths[:20]:
    print("  Path:", p[:200])
