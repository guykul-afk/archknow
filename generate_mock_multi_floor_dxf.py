import ezdxf

def create_mock_project():
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Layers
    doc.layers.add('A-WALL', color=7)
    doc.layers.add('A-TEXT', color=3)
    doc.layers.add('A-AREA-APT', color=5) # Apartment boundary
    doc.layers.add('A-TITLE', color=6) # Floor titles
    
    # ==============================
    # FLOOR 1: PARKING (at X=0, Y=0)
    # ==============================
    # Floor Title
    msp.add_text("חניון", dxfattribs={'layer': 'A-TITLE', 'height': 50}).set_placement((500, 1500))
    # Parking outline
    msp.add_lwpolyline([(0,0), (2000,0), (2000,1000), (0,1000)], close=True, dxfattribs={'layer': 'A-WALL'})
    # Some texts
    msp.add_text("חניה 1", dxfattribs={'layer': 'A-TEXT', 'height': 20}).set_placement((100, 500))
    msp.add_text("חניה 2", dxfattribs={'layer': 'A-TEXT', 'height': 20}).set_placement((500, 500))

    # ==============================
    # FLOOR 2: RESIDENTIAL (at X=5000, Y=0)
    # ==============================
    # Floor Title
    msp.add_text("קומת מגורים 1", dxfattribs={'layer': 'A-TITLE', 'height': 50}).set_placement((5500, 1500))
    
    # Apartment 1 (Left: X=5000 to X=6000)
    # Boundary
    msp.add_lwpolyline([(5000,0), (6000,0), (6000,1000), (5000,1000)], close=True, dxfattribs={'layer': 'A-AREA-APT'})
    msp.add_text("דירה 1", dxfattribs={'layer': 'A-TEXT', 'height': 30}).set_placement((5050, 900))
    # Rooms in Apt 1
    # Living room
    msp.add_lwpolyline([(5000,0), (5500,0), (5500,500), (5000,500)], close=True, dxfattribs={'layer': 'A-WALL'})
    msp.add_text("סלון", dxfattribs={'layer': 'A-TEXT', 'height': 20}).set_placement((5100, 200))
    # Bedroom
    msp.add_lwpolyline([(5500,0), (6000,0), (6000,500), (5500,500)], close=True, dxfattribs={'layer': 'A-WALL'})
    msp.add_text("חדר שינה", dxfattribs={'layer': 'A-TEXT', 'height': 20}).set_placement((5600, 200))
    # Kitchen
    msp.add_lwpolyline([(5000,500), (6000,500), (6000,800), (5000,800)], close=True, dxfattribs={'layer': 'A-WALL'})
    msp.add_text("מטבח", dxfattribs={'layer': 'A-TEXT', 'height': 20}).set_placement((5500, 600))
    
    # Apartment 2 (Right: X=6200 to X=7200)
    # Boundary
    msp.add_lwpolyline([(6200,0), (7200,0), (7200,1000), (6200,1000)], close=True, dxfattribs={'layer': 'A-AREA-APT'})
    msp.add_text("דירה 2", dxfattribs={'layer': 'A-TEXT', 'height': 30}).set_placement((6250, 900))
    # Rooms in Apt 2
    # Living room
    msp.add_lwpolyline([(6200,0), (6800,0), (6800,500), (6200,500)], close=True, dxfattribs={'layer': 'A-WALL'})
    msp.add_text("סלון", dxfattribs={'layer': 'A-TEXT', 'height': 20}).set_placement((6400, 200))
    # Mamad
    msp.add_lwpolyline([(6800,0), (7200,0), (7200,500), (6800,500)], close=True, dxfattribs={'layer': 'A-WALL'})
    msp.add_text("ממ\"ד", dxfattribs={'layer': 'A-TEXT', 'height': 20}).set_placement((6900, 200))
    # Bathroom
    msp.add_lwpolyline([(6200,500), (7200,500), (7200,800), (6200,800)], close=True, dxfattribs={'layer': 'A-WALL'})
    msp.add_text("רחצה", dxfattribs={'layer': 'A-TEXT', 'height': 20}).set_placement((6600, 600))
    
    doc.saveas('sample_project.dxf')
    print("Created mock DXF file: sample_project.dxf")

if __name__ == '__main__':
    create_mock_project()
