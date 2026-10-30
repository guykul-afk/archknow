import zipfile, re

dwfx_path = r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה\6.5.26-hagasha.dwfx"
with zipfile.ZipFile(dwfx_path, 'r') as z:
    fpage = z.read("dwf/documents/20557152-C9F2-4F2A-83D0-E6D25FE4C692/sections/com.autodesk.dwf.ePlot_20557153-C9F2-4F2A-83D0-E6D25FE4C692/FixedPage.fpage").decode('utf-8', errors='replace')

all_paths = re.findall(r'<Path([^>]+)/>', fpage)
for attr in all_paths:
    if '#F90606' in attr:
        print("F90606 attr:", attr[:260])
for attr in all_paths:
    if 'StrokeThickness="19"' in attr or 'StrokeThickness="33"' in attr:
        print("Thick stroke:", attr[:260])
        break
