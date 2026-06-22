import os
import shutil
import aspose.cad as cad

def convert_to_dxf(input_path, output_dxf_path):
    """
    Converts DWG/DWF/DWFX to DXF using aspose-cad.
    If the file is already DXF, copies it.
    """
    ext = os.path.splitext(input_path)[1].lower()
    
    if ext == ".dxf":
        if input_path != output_dxf_path:
            shutil.copy(input_path, output_dxf_path)
        return True

    if ext not in [".dwg", ".dwf", ".dwfx"]:
        raise ValueError(f"Unsupported file format: {ext}")
        
    try:
        # Load the CAD image (DWG, DWF, or DWFX)
        with cad.Image.load(input_path) as image:
            # Save as DXF
            dxf_options = cad.imageoptions.DxfOptions()
            image.save(output_dxf_path, dxf_options)
        return True
    except Exception as e:
        raise RuntimeError(f"Failed to convert {ext} to DXF: {str(e)}")
