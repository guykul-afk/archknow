import os
import shutil
import aspose.cad as cad

def convert_to_dxf(input_path, output_dxf_path, output_png_path=None):
    """
    Converts DWG/DWF/DWFX to DXF using aspose-cad.
    If the file is already DXF, copies it.
    Also generates a PNG preview image if output_png_path is provided.
    """
    ext = os.path.splitext(input_path)[1].lower()
    
    if ext == ".dxf":
        if input_path != output_dxf_path:
            shutil.copy(input_path, output_dxf_path)
        if output_png_path:
            try:
                with cad.Image.load(input_path) as image:
                    png_options = cad.imageoptions.PngOptions()
                    raster_options = cad.imageoptions.CadRasterizationOptions()
                    raster_options.page_width = 1200.0
                    raster_options.page_height = 800.0
                    png_options.vector_rasterization_options = raster_options
                    image.save(output_png_path, png_options)
            except Exception as e:
                print(f"Warning: Failed to render DXF preview: {e}")
        return True

    if ext not in [".dwg", ".dwf", ".dwfx"]:
        raise ValueError(f"Unsupported file format: {ext}")
        
    try:
        # Load the CAD image (DWG, DWF, or DWFX)
        with cad.Image.load(input_path) as image:
            # Save as DXF
            dxf_options = cad.imageoptions.DxfOptions()
            image.save(output_dxf_path, dxf_options)
            
            # Save as PNG
            if output_png_path:
                png_options = cad.imageoptions.PngOptions()
                raster_options = cad.imageoptions.CadRasterizationOptions()
                raster_options.page_width = 1200.0
                raster_options.page_height = 800.0
                png_options.vector_rasterization_options = raster_options
                image.save(output_png_path, png_options)
        return True
    except Exception as e:
        raise RuntimeError(f"Failed to convert {ext} to DXF: {str(e)}")
