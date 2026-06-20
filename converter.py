import os
import subprocess
import shutil

# Typical macOS path for ODA File Converter
ODA_CONVERTER_PATH = "/Applications/ODAFileConverter.app/Contents/MacOS/ODAFileConverter"

def convert_to_dxf(input_path, output_dxf_path):
    """
    Converts DWG/DWF to DXF. If the file is already DXF, copies or returns it.
    """
    ext = os.path.splitext(input_path)[1].lower()
    
    if ext == ".dxf":
        if input_path != output_dxf_path:
            shutil.copy(input_path, output_dxf_path)
        return True

    if ext not in [".dwg", ".dwf"]:
        raise ValueError(f"Unsupported file format: {ext}")
        
    if not os.path.exists(ODA_CONVERTER_PATH):
        raise FileNotFoundError(
            "כלי ההמרה ODAFileConverter לא נמצא ב-Applications.\n"
            "יש להוריד ולהתקין אותו מכתובת:\n"
            "https://www.opendesign.com/guestfiles/oda_file_converter\n"
            "כדי לאפשר ניתוח קבצי DWG/DWF במערכת."
        )
        
    # ODA File Converter requires:
    # ODAFileConverter "input_dir" "output_dir" "output_version" "format" "recurse" "audit" [filter]
    input_dir = os.path.dirname(os.path.abspath(input_path))
    output_dir = os.path.dirname(os.path.abspath(output_dxf_path))
    filename = os.path.basename(input_path)
    
    # We target AutoCAD 2018 DXF ASCII
    cmd = [
        ODA_CONVERTER_PATH,
        input_dir,
        output_dir,
        "ACAD2018",
        "DXF",
        "0", # no recurse
        "1", # audit
        filename
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # The converter outputs to output_dir with the same name but .dxf extension
    expected_out = os.path.join(output_dir, os.path.splitext(filename)[0] + ".dxf")
    
    if os.path.exists(expected_out):
        if expected_out != output_dxf_path:
            shutil.move(expected_out, output_dxf_path)
        return True
    else:
        raise RuntimeError(
            f"המרת הקובץ נכשלה.\nפרטי שגיאה:\n{result.stdout}\n{result.stderr}"
        )
