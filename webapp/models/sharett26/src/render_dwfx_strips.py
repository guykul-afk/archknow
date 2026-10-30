import os
import sys
import zipfile
import fitz

sys.stdout.reconfigure(encoding='utf-8')
ws = r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה"
dwfx_path = os.path.join(ws, "6.5.26-hagasha.dwfx")
scratch_dir = r"C:\Users\User\.gemini\antigravity\brain\71931cc9-7058-41f3-a9f0-80549e5c535b\scratch"
os.makedirs(scratch_dir, exist_ok=True)

doc = fitz.open(dwfx_path)
page = doc[0]
W, H = page.rect.width, page.rect.height
print(f"DWFX Page size: {W} x {H} pt ({W/28.3464567:.2f}m x {H/28.3464567:.2f}m at 1:100)")

# Render 6 overlapping horizontal strips across W (0 to 25511.25)
num_strips = 6
strip_w = W / num_strips
for i in range(num_strips):
    x0 = max(0, i * strip_w - 100)
    x1 = min(W, (i + 1) * strip_w + 100)
    clip = fitz.Rect(x0, 0, x1, H)
    pix = page.get_pixmap(clip=clip, dpi=96)
    out_png = os.path.join(scratch_dir, f"dwfx_strip_{i}_{int(x0)}_{int(x1)}.png")
    pix.save(out_png)
    print(f"Saved {out_png} ({pix.width}x{pix.height})")

# Also inspect XML files inside DWFX
with zipfile.ZipFile(dwfx_path, 'r') as z:
    for name in z.namelist():
        if name.endswith(".xml") or name.endswith(".fpage"):
            info = z.getinfo(name)
            print(f"Archive member: {name} ({info.file_size} bytes)")
            if name.endswith("0630D146-B0BA-4575-BAEE-0E7C415555BB.xml") or name.endswith("CD0B4778-58C4-4F54-9747-E013640531B5.xml"):
                raw = z.read(name).decode('utf-8', errors='replace')
                print(f"  Sample of {os.path.basename(name)}:")
                print(raw[:1500])
