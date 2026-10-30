import zipfile, re
from collections import Counter

DWF_PER_M = 472.4409448818898
dwfx_path = r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה\6.5.26-hagasha.dwfx"
with zipfile.ZipFile(dwfx_path, 'r') as z:
    fpage = z.read("dwf/documents/20557152-C9F2-4F2A-83D0-E6D25FE4C692/sections/com.autodesk.dwf.ePlot_20557153-C9F2-4F2A-83D0-E6D25FE4C692/FixedPage.fpage").decode('utf-8', errors='replace')

ax, ay = 255.841 + 20.482, 7.353 + 17.714
all_paths = re.findall(r'<Path([^>]+)/>', fpage)
c_Types = Counter()
samples = {}
for attr in all_paths:
    m_d = re.search(r'Data="M([-+]?\d*\.?\d+),([-+]?\d*\.?\d+)', attr)
    if not m_d: continue
    x = float(m_d.group(1)) / DWF_PER_M - ax
    y = float(m_d.group(2)) / DWF_PER_M - ay
    if -19.0 <= x <= 19.0 and -16.0 <= y <= 17.0:
        mf = re.search(r'Fill="([^"]+)"', attr)
        ms = re.search(r'Stroke="([^"]+)"', attr)
        mt = re.search(r'StrokeThickness="([^"]+)"', attr)
        key = (mf.group(1) if mf else None, ms.group(1) if ms else None, mt.group(1) if mt else None)
        c_Types[key] += 1
        if key not in samples:
            samples[key] = attr[:220]

for k, cnt in c_Types.most_common(25):
    print(f"{str(k):38s}: {cnt:5d} | {samples[k]}")
