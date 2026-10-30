import zipfile, re
from collections import Counter

dwfx_path = r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה\6.5.26-hagasha.dwfx"
with zipfile.ZipFile(dwfx_path, 'r') as z:
    fpage = z.read("dwf/documents/20557152-C9F2-4F2A-83D0-E6D25FE4C692/sections/com.autodesk.dwf.ePlot_20557153-C9F2-4F2A-83D0-E6D25FE4C692/FixedPage.fpage").decode('utf-8', errors='replace')

# Let's check all <Canvas> tags and their transforms/clips
canvases = re.findall(r'<Canvas\s+([^>]+)>', fpage)
print(f"Found {len(canvases)} Canvas tags:")
for c in canvases[:15]:
    print(" ", c)

# Let's count Fill colors and Stroke colors across all Path elements
fills = Counter(re.findall(r'Fill="([^"]+)"', fpage))
strokes = Counter(re.findall(r'Stroke="([^"]+)"', fpage))
ethick = Counter(re.findall(r'StrokeThickness="([^"]+)"', fpage))
print("Fills:", fills.most_common(20))
print("Strokes:", strokes.most_common(20))
print("StrokeThickness:", ethick.most_common(20))
