# KKL 10 Architectural BIM Project Rules & Constraints

## 1. Coordinate System & Axis Alignment
- **Datum (0, 0, 0):** South-West exterior corner of the building at Ground Floor finished floor level $\pm 0.00$ ($+59.53\text{ m}$ absolute).
- **Axes:**
  - `+X` = East (`0.00m` to `12.73m`).
  - `+Y` = Up (`-9.07m` to `+31.40m`).
  - `-Z` = North (`N = 0.00m` to `N = 33.09m`, mapped to `z = -N`).
- **North Facade View Rule:** Looking at the building from KKL Street facing South, East is on the LEFT (Living Room vitrine and L3-L7 cantilevered balconies) and West is on the RIGHT (two bedroom windows).

## 2. Vertical Section Datum (Sections 1-1 & 2-2)
- Foundation & Pump Pit: `-9.07m` (Pit floor `-8.62m`).
- Basement -2: `-7.65m` (Height 3.30m, slab thickness 0.35m).
- Basement -1: `-4.35m` (Height 4.35m, slab thickness 0.35m).
- Ground Floor (L0): `0.00m` (Height 4.20m to Floor 1).
- Floors 1 to 6 (L1–L6): `3.15m` typical floor-to-floor height (+4.20, +7.35, +10.50, +13.65, +16.80, +19.95).
- Floor 7 (L7): `+23.10m` with expanded height `3.40m` (ceiling at `+26.50m`).
- Floor 8 Penthouses (L8): `+26.50m` with height `3.40m` (roof slab at `+29.90m`).
- Technical Roof & Parapet: Roof slab `+29.90m`, solid continuous parapet at `+31.40m` (Height 1.50m).

## 3. Floor Plan Layout & Wall-Window Locking
- Exterior windows and interior partition walls must be locked to the cumulative dimension chain from the 1:50 Sales Plans (`3309 cm` North-South $\times$ `1273 cm` East-West).
- No partition wall or Mamad concrete wall may terminate inside a window opening.
- All interior walls must be watertight, continuous polygons meeting cleanly at L-corners and T-junctions with zero gaps or voids.
- Explicit door openings (`H = 2.10m`) with overhead lintel headers and 3D jamb frames must be maintained on all doorways.
- All 2D CAD furniture drawings, light-wood cabinets/wardrobes (`Int_LightWood`), and room dimension labels (`ס"מ × ס"מ`) must be projected directly on the floor slab of each level.
