import os
import sys

dwg_path = r"c:\Users\guyku\Downloads\yatkovski7-100-20 (2).dwg"
scratch_dir = r"C:\Users\User\.gemini\antigravity\brain\d2d68241-91a0-4e6e-a361-97f12e33db15\scratch"
os.makedirs(scratch_dir, exist_ok=True)
dxf_out = os.path.join(scratch_dir, "yatkovski7_100_20.dxf")

with open(dwg_path, "rb") as f:
    header = f.read(6)
print("DWG version header:", header)

# Try accoreconsole or aspose.cad
try:
    import aspose.cad as cad
    print("aspose.cad available! Loading DWG...")
    with cad.Image.load(dwg_path) as img:
        print("Loaded image type:", type(img))
        dxf_opts = cad.imageoptions.DxfOptions()
        img.save(dxf_out, dxf_opts)
        print("Saved DXF to:", dxf_out, "size:", os.path.getsize(dxf_out))
except Exception as e:
    print("aspose.cad error:", e)
