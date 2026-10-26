import sys
try:
    import ezdxf
except ImportError:
    print("Please install ezdxf")
    sys.exit(1)

def create_mock_dxf(filename="sample_apartment.dxf"):
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    
    # Create required layers
    doc.layers.add("ROOM_POLYGONS", color=2) # Yellow
    doc.layers.add("ROOM_LABELS", color=3)   # Green
    
    # Room 1: Master Bedroom (3m x 4m)
    # Coordinates: (0,0) to (3,4)
    # Area: 12 sqm
    points_room1 = [(0, 0), (3, 0), (3, 4), (0, 4), (0, 0)]
    msp.add_lwpolyline(points_room1, dxfattribs={"layer": "ROOM_POLYGONS"})
    msp.add_text("Bedroom 1", dxfattribs={"layer": "ROOM_LABELS", "height": 0.2}).set_placement((1, 2))
    
    # Room 2: Small Room / Mamad (2m x 3m)
    # Coordinates: (3,0) to (5,3)
    # Area: 6 sqm
    points_room2 = [(3, 0), (5, 0), (5, 3), (3, 3), (3, 0)]
    msp.add_lwpolyline(points_room2, dxfattribs={"layer": "ROOM_POLYGONS"})
    msp.add_text("Mamad", dxfattribs={"layer": "ROOM_LABELS", "height": 0.2}).set_placement((3.5, 1.5))
    
    # Room 3: Bathroom (2m x 2m)
    # Coordinates: (5,0) to (7,2)
    # Area: 4 sqm
    points_room3 = [(5, 0), (7, 0), (7, 2), (5, 2), (5, 0)]
    msp.add_lwpolyline(points_room3, dxfattribs={"layer": "ROOM_POLYGONS"})
    msp.add_text("Bathroom", dxfattribs={"layer": "ROOM_LABELS", "height": 0.2}).set_placement((5.5, 1))

    doc.saveas(filename)
    print(f"Created mock DXF file: {filename}")

if __name__ == "__main__":
    create_mock_dxf()
