# -*- coding: utf-8 -*-
import os, json, re

WORKSPACE = r"g:\Shared drives\שליטה ובקרה\מודלים פרויקטים\משה שרת 26-28 פתח תקווה"
DATA_DIR = os.path.join(WORKSPACE, "data")
THREE_JS_PATH = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\_shared_engine\three.min.js"
KITRONI_VIEWER_PY = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\הרב קיטרוני 37-39 פתח תקווה\src\build_html_viewer.py"

with open(THREE_JS_PATH, "r", encoding="utf-8") as f:
    three_js_code = f.read()

with open(os.path.join(DATA_DIR, "sharett_extracted_plans.json"), "r", encoding="utf-8") as f:
    plans_data = json.load(f)

with open(os.path.join(DATA_DIR, "sharett_units_crm.json"), "r", encoding="utf-8") as f:
    crm_data = json.load(f)

with open(os.path.join(DATA_DIR, "unified_sharett_3d_map.json"), "r", encoding="utf-8") as f:
    unified_map_data = json.load(f)

with open(os.path.join(DATA_DIR, "sharett_spatial_map_data.json"), "r", encoding="utf-8") as f:
    spatial_gis_data = json.load(f)

wide_gmaps_data_uri = unified_map_data["outer_z15"]["data_uri"]
inner_gmaps_data_uri = unified_map_data["inner_z17"]["data_uri"]
closeup_gmaps_data_uri = unified_map_data["closeup_z19"]["data_uri"]
outer_span_m = unified_map_data["outer_z15"]["world_span_m"]
inner_span_m = unified_map_data["inner_z17"]["world_span_m"]
closeup_span_m = unified_map_data["closeup_z19"]["world_span_m"]

plans_json_str = json.dumps(plans_data, ensure_ascii=False, separators=(',', ':'))
crm_json_str = json.dumps(crm_data, ensure_ascii=False, separators=(',', ':'))
spatial_pois_json = json.dumps(spatial_gis_data["pois"], ensure_ascii=False, separators=(',', ':'))

with open(KITRONI_VIEWER_PY, "r", encoding="utf-8") as f:
    src_py = f.read()

s_idx = src_py.find('HTML_TEMPLATE = r"""') + len('HTML_TEMPLATE = r"""')
e_idx = src_py.rfind('"""')
tmpl = src_py[s_idx:e_idx]

# 0. Inject Synthetic Grass, Terracotta Paver, and Garden Soil Materials into MATS
SYNTH_TURF_JS = """    function createSyntheticTurfTexture() {
      const c = document.createElement('canvas');
      c.width = 256; c.height = 256;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#15803d';
      ctx.fillRect(0, 0, 256, 256);
      for (let i = 0; i < 3200; i++) {
        const x = (i * 73) % 256;
        const y = (i * 137) % 256;
        ctx.fillStyle = (i % 3 === 0) ? '#22c55e' : ((i % 3 === 1) ? '#16a34a' : '#14532d');
        ctx.fillRect(x, y, 2, 3);
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(8, 8);
      return tex;
    }
    const texSyntheticTurf = createSyntheticTurfTexture();
    const MATS = {
      syntheticGrass: new THREE.MeshStandardMaterial({ map: texSyntheticTurf, color: 0x22c55e, roughness: 0.78, metalness: 0.02, polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -1, clippingPlanes }),
      gardenGrass: new THREE.MeshStandardMaterial({ map: texSyntheticTurf, color: 0x4ade80, roughness: 0.85, metalness: 0.01, clippingPlanes }),
      terracottaPaver: new THREE.MeshStandardMaterial({ color: 0xe6b89c, roughness: 0.78, metalness: 0.02, clippingPlanes }),
      patioPaver: new THREE.MeshStandardMaterial({ color: 0xd6d3d1, roughness: 0.75, metalness: 0.02, clippingPlanes }),"""

tmpl = tmpl.replace("    const MATS = {", SYNTH_TURF_JS, 1)

# 1. Replace FLOORS definition with the exact 14 levels of Moshe Sharett 26-28
NEW_FLOORS_JS = """    const FLOORS = [
      { id: 'bm2', label: 'מרתף חניה -2', zFloor: -6.00, zCeil: -3.20, zTop: -3.00, sheet: 'basement_2',   elevText: '-6.00' },
      { id: 'bm1', label: 'מרתף חניה -1', zFloor: -3.00, zCeil: -0.20, zTop:  0.00, sheet: 'basement_1',   elevText: '-3.00' },
      { id: 'kar', label: 'קומת קרקע (חלל כפול)', zFloor: 0.00, zCeil: 2.90, zTop: 3.10, sheet: 'ground', elevText: '±0.00' },
      { id: 'gal', label: 'קומת גלריה (דופלקסים)', zFloor: 3.10, zCeil: 5.90, zTop: 6.12, sheet: 'gallery', elevText: '+3.10' },
      { id: 'f1',  label: 'קומה 1',       zFloor:  6.12, zCeil:  9.05, zTop:  9.27, sheet: 'floors_1267',  elevText: '+6.12' },
      { id: 'f2',  label: 'קומה 2',       zFloor:  9.27, zCeil: 12.20, zTop: 12.42, sheet: 'floors_1267',  elevText: '+9.27' },
      { id: 'f3',  label: 'קומה 3',       zFloor: 12.42, zCeil: 15.35, zTop: 15.57, sheet: 'floors_345',   elevText: '+12.42' },
      { id: 'f4',  label: 'קומה 4 · מרוהטת 3D ✨', zFloor: 15.57, zCeil: 18.50, zTop: 18.72, sheet: 'floors_345', elevText: '+15.57', has3DFurn: true },
      { id: 'f5',  label: 'קומה 5 · מרוהטת 3D ✨', zFloor: 18.72, zCeil: 21.65, zTop: 21.87, sheet: 'floors_345', elevText: '+18.72', has3DFurn: true },
      { id: 'f6',  label: 'קומה 6',       zFloor: 21.87, zCeil: 24.80, zTop: 25.02, sheet: 'floors_1267',  elevText: '+21.87' },
      { id: 'f7',  label: 'קומה 7',       zFloor: 25.02, zCeil: 27.95, zTop: 28.17, sheet: 'floors_1267',  elevText: '+25.02' },
      { id: 'f8',  label: 'קומה 8 (פנטהאוז) ✨', zFloor: 28.17, zCeil: 31.10, zTop: 31.32, sheet: 'floor_8', elevText: '+28.17', has3DFurn: true },
      { id: 'f9',  label: 'קומה 9 (מרפסת גג דשא סינטטי)', zFloor: 31.32, zCeil: 33.77, zTop: 33.77, sheet: 'floor_9_roof', elevText: '+31.32' },
      { id: 'gag', label: 'גג עליון (+34.27)', zFloor: 33.77, zCeil: 34.27, zTop: 34.45, sheet: 'upper_roof',   elevText: '+33.77' }
    ];"""

tmpl = re.sub(r"const FLOORS = \[[\s\S]*?\];", NEW_FLOORS_JS, tmpl, count=1)

# 2. Replace isExteriorWallFace for Moshe Sharett 26-28's exact envelope
NEW_EXT_WALL_FN = """    function isExteriorWallFace(sheetKey, x1, y1, x2, y2) {
      if (sheetKey === 'upper_roof' || sheetKey === 'floor_9_roof') return true;
      if (sheetKey === 'basement_1' || sheetKey === 'basement_2') return false;
      const xm = 0.5 * (x1 + x2);
      const ym = 0.5 * (y1 + y2);
      const tol = 0.16;
      if (xm <= -16.62 + tol || xm >= 16.38 - tol) return true;
      if ((sheetKey === 'ground' || sheetKey === 'gallery') && ym >= -3.15 && xm <= -15.04 + tol) return true;
      if (ym >= -3.15 && ym <= 3.55 && (xm <= -15.04 + tol || xm >= 14.80 - tol)) return true;
      if (ym <= -12.99 + tol || ym >= 13.40 - tol) return true;
      if (sheetKey === 'floor_8' && ym >= 11.90 - tol) return true;
      if (Math.abs(xm - (-3.17)) <= 0.28 || Math.abs(xm - 2.93) <= 0.28) return true;
      if (xm >= -3.25 && xm <= 3.00 && (Math.abs(ym - (-3.42)) <= 0.26 || Math.abs(ym - 3.82) <= 0.26)) return true;
      return false;
    }"""

tmpl = re.sub(r"function isExteriorWallFace\(sheetKey, x1, y1, x2, y2\) \{[\s\S]*?\n    \}", NEW_EXT_WALL_FN, tmpl, count=1)

# 3. Replace buildBalconyBox so all balconies on Floors 1..7 have crisp white slab fascias (שליכט אקרילי לבן)
#    and dark charcoal vertical metal picket railings (מעקה מתכת) per Image 1, 3, 4, 5!
NEW_BALCONY_FN = """    function buildMetalPicketRailing(grp, x0, y0, x1, y1, zBot, zTop, side) {
      // Top & bottom horizontal metal rails
      grp.add(makeBox(x0, y0, x1, y1, zTop - 0.04, zTop, MATS.aluDark, false));
      grp.add(makeBox(x0, y0, x1, y1, zBot, zBot + 0.03, MATS.aluDark, false));
      // Vertical metal pickets every 18cm + semi-transparent safety glass backing
      if (side === 'N' || side === 'S') {
        const my = 0.5 * (y0 + y1);
        grp.add(makeBox(x0 + 0.02, my - 0.01, x1 - 0.02, my + 0.01, zBot + 0.03, zTop - 0.04, MATS.glassRailing, false));
        for (let px = x0 + 0.04; px <= x1 - 0.04; px += 0.18) {
          grp.add(makeBox(px - 0.012, my - 0.02, px + 0.012, my + 0.02, zBot + 0.03, zTop - 0.04, MATS.aluDark, false));
        }
      } else {
        const mx = 0.5 * (x0 + x1);
        grp.add(makeBox(mx - 0.01, y0 + 0.02, mx + 0.01, y1 - 0.02, zBot + 0.03, zTop - 0.04, MATS.glassRailing, false));
        for (let py = y0 + 0.04; py <= y1 - 0.04; py += 0.18) {
          grp.add(makeBox(mx - 0.02, py - 0.012, mx + 0.02, py + 0.012, zBot + 0.03, zTop - 0.04, MATS.aluDark, false));
        }
      }
    }

    function buildBalconyBox(floorId, x0, y0, x1, y1, zFloor, openSides, hasPergola = false, railHeight = 1.05, thickFascia = false) {
      const bGrp = new THREE.Group();
      const sDepth = 0.24;
      const curbH = 0.14;
      // Crisp white concrete balcony slab fascia (שליכט אקרילי לבן) on ALL floors per Image 1, 3, 4, 5!
      bGrp.add(makeBox(x0, y0, x1, y1, zFloor - sDepth, zFloor - 0.02, MATS.extWall));
      bGrp.add(makeBox(x0 + 0.06, y0 + 0.06, x1 - 0.06, y1 - 0.06, zFloor - 0.02, zFloor + 0.01, MATS.woodDeck));

      const zRailTop = zFloor + railHeight;
      openSides.forEach(side => {
        if (side === 'W') {
          bGrp.add(makeBox(x0, y0, x0 + 0.12, y1, zFloor, zFloor + curbH, MATS.extWall, false));
          buildMetalPicketRailing(bGrp, x0 + 0.02, y0, x0 + 0.09, y1, zFloor + curbH, zRailTop, 'W');
        } else if (side === 'E') {
          bGrp.add(makeBox(x1 - 0.12, y0, x1, y1, zFloor, zFloor + curbH, MATS.extWall, false));
          buildMetalPicketRailing(bGrp, x1 - 0.09, y0, x1 - 0.02, y1, zFloor + curbH, zRailTop, 'E');
        } else if (side === 'N') {
          bGrp.add(makeBox(x0, y0, x1, y0 + 0.12, zFloor, zFloor + curbH, MATS.extWall, false));
          buildMetalPicketRailing(bGrp, x0, y0 + 0.02, x1, y0 + 0.09, zFloor + curbH, zRailTop, 'N');
        } else if (side === 'S') {
          bGrp.add(makeBox(x0, y1 - 0.12, x1, y1, zFloor, zFloor + curbH, MATS.extWall, false));
          buildMetalPicketRailing(bGrp, x0, y1 - 0.09, x1, y1 - 0.02, zFloor + curbH, zRailTop, 'S');
        }
      });

      addToFloorAndLayer(floorId, 'balconies', bGrp);
    }"""

tmpl = re.sub(
    r"function buildBalconyBox\(floorId, x0, y0, x1, y1, zFloor, openSides, hasPergola = false, railHeight = 1\.05, thickFascia = false\) \{[\s\S]*?\n    \}",
    NEW_BALCONY_FN,
    tmpl,
    count=1
)

# 4. Replace makeExteriorOpeningWallBox & buildOpening3D to render exact Garmushka window/opening sizes and double-height South openings
NEW_OPENING_BUILDER = """    function makeExteriorOpeningWallBox(x0, y0, x1, y1, z0, z1, orient) {
      return makeBox(x0, y0, x1, y1, z0, z1, [MATS.extWall, MATS.extWall, MATS.wallCap, MATS.wallCap, MATS.extWall, MATS.extWall]);
    }

    function buildPolygonSlab(pts2d, z0, z1, matTop, matSide) {
      const shape = new THREE.Shape();
      shape.moveTo(pts2d[0][0], -pts2d[0][1]);
      for (let i = 1; i < pts2d.length; i++) {
        shape.lineTo(pts2d[i][0], -pts2d[i][1]);
      }
      shape.closePath();
      const geo = new THREE.ExtrudeGeometry(shape, { depth: z1 - z0, bevelEnabled: false });
      geo.rotateX(-Math.PI / 2);
      const m = new THREE.Mesh(geo, [matTop, matSide || matTop]);
      m.position.y = z0;
      m.receiveShadow = true;
      m.castShadow = true;
      return m;
    }

    function buildOpening3D(floorObj, op) {
      const [orient, x0, y0, x1, y1, kind] = op;
      const zFloor = floorObj.zFloor;
      const zCeil = floorObj.zCeil;

      // Double-height upper void on Gallery level ('dh_void'): fill ONLY from +4.50m up to +6.12m so the tall opening below (0.00..+4.50) stays open!
      if (kind === 'dh_void') {
        const zHeadDH = 4.50;
        addToFloorAndLayer(floorObj.id, 'walls', makeExteriorOpeningWallBox(x0, y0, x1, y1, zHeadDH, zCeil, orient));
        return;
      }

      // Double-Height South Facade Glazed Lobby Storefront / Tall Window (0.00 .. +4.50m) per Image 5 (חזית דרומית)
      if (kind === 'vitrine_dh' || kind === 'curtain_3bay_dh') {
        const zTopDH = 4.50;
        const vGrp = new THREE.Group();
        const fThick = 0.06;
        const midY = 0.5 * (y0 + y1);
        vGrp.add(makeBox(x0, y0, x1, y1, zFloor, zFloor + fThick, MATS.aluDark, false));
        vGrp.add(makeBox(x0, y0, x1, y1, zTopDH - fThick, zTopDH, MATS.aluDark, false));
        vGrp.add(makeBox(x0, y0, x0 + fThick, y1, zFloor, zTopDH, MATS.aluDark, false));
        vGrp.add(makeBox(x1 - fThick, y0, x1, y1, zFloor, zTopDH, MATS.aluDark, false));
        // Horizontal transom bar at z = +2.40m
        vGrp.add(makeBox(x0, midY - 0.04, x1, midY + 0.04, 2.38, 2.44, MATS.aluDark, false));
        if (kind === 'curtain_3bay_dh') {
          const wBay = (x1 - x0) / 3.0;
          for (let b = 1; b <= 2; b++) {
            const mx = x0 + b * wBay;
            vGrp.add(makeBox(mx - 0.03, midY - 0.04, mx + 0.03, midY + 0.04, zFloor, zTopDH, MATS.aluDark, false));
          }
        } else if ((x1 - x0) >= 2.2) {
          const mx = 0.5 * (x0 + x1);
          vGrp.add(makeBox(mx - 0.03, midY - 0.04, mx + 0.03, midY + 0.04, zFloor, zTopDH, MATS.aluDark, false));
        }
        vGrp.add(makeBox(x0 + fThick, midY - 0.015, x1 - fThick, midY + 0.015, zFloor + fThick, zTopDH - fThick, MATS.winGlass, false));
        addToFloorAndLayer(floorObj.id, 'windows', vGrp);
        return;
      }

      // Double-Height South Facade Horizontal Louver/Service Gate (X = -13.30..-9.90, z = 0.00..+4.50m) per Image 5
      if (kind === 'gate_louver_dh') {
        const zTopDH = 4.50;
        const gGrp = new THREE.Group();
        const midY = 0.5 * (y0 + y1);
        gGrp.add(makeBox(x0, y0, x0 + 0.06, y1, zFloor, zTopDH, MATS.aluDark, false));
        gGrp.add(makeBox(x1 - 0.06, y0, x1, y1, zFloor, zTopDH, MATS.aluDark, false));
        gGrp.add(makeBox(x0, y0, x1, y1, zTopDH - 0.06, zTopDH, MATS.aluDark, false));
        gGrp.add(makeBox(x0 + 0.04, midY - 0.02, x1 - 0.04, midY + 0.02, zFloor, zTopDH, MATS.wall, false));
        for (let z = zFloor + 0.06; z < zTopDH - 0.06; z += 0.13) {
          gGrp.add(makeBox(x0 + 0.04, midY - 0.05, x1 - 0.04, midY + 0.05, z, z + 0.06, MATS.aluDark, false));
        }
        addToFloorAndLayer(floorObj.id, 'windows', gGrp);
        return;
      }

      if (kind === 'vitrine') {
        const zTopOpen = Math.min(zFloor + 2.25, zCeil - 0.15);
        if (zCeil > zTopOpen + 0.02) {
          addToFloorAndLayer(floorObj.id, 'walls', makeExteriorOpeningWallBox(x0, y0, x1, y1, zTopOpen, zCeil, orient));
        }
        const vGrp = new THREE.Group();
        const fThick = 0.05;
        vGrp.add(makeBox(x0, y0, x1, y1, zFloor, zFloor + fThick, MATS.aluDark, false));
        vGrp.add(makeBox(x0, y0, x1, y1, zTopOpen - fThick, zTopOpen, MATS.aluDark, false));
        if (orient === 'H') {
          const midX = 0.5 * (x0 + x1);
          const midY = 0.5 * (y0 + y1);
          vGrp.add(makeBox(x0, y0, x0 + fThick, y1, zFloor, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(x1 - fThick, y0, x1, y1, zFloor, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(midX - 0.025, midY - 0.04, midX + 0.025, midY + 0.04, zFloor, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(x0 + fThick, midY - 0.015, x1 - fThick, midY + 0.015, zFloor + fThick, zTopOpen - fThick, MATS.winGlass, false));
        } else {
          const midX = 0.5 * (x0 + x1);
          const midY = 0.5 * (y0 + y1);
          vGrp.add(makeBox(x0, y0, x1, y0 + fThick, zFloor, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(x0, y1 - fThick, x1, y1, zFloor, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(midX - 0.04, midY - 0.025, midX + 0.04, midY + 0.025, zFloor, zTopOpen, MATS.aluDark, false));
          vGrp.add(makeBox(midX - 0.015, y0 + fThick, midX + 0.015, y1 - fThick, zFloor + fThick, zTopOpen - fThick, MATS.winGlass, false));
        }
        addToFloorAndLayer(floorObj.id, 'windows', vGrp);

      } else if (kind === 'louver' || kind === 'louver_Recess') {
        // Dark-Gray Horizontal Aluminum Laundry Shaft Louver Screen
        // On inner courtyard walls ('louver_Recess'), keep a continuous white spandrel wall up to zFloor+1.05 so it doesn't look like a dark pit!
        const zSill = (kind === 'louver_Recess') ? (zFloor + 1.05) : (zFloor + 0.15);
        const zHead = (kind === 'louver_Recess') ? Math.min(zFloor + 2.25, zCeil - 0.15) : (zCeil - 0.12);
        addToFloorAndLayer(floorObj.id, 'walls', makeExteriorOpeningWallBox(x0, y0, x1, y1, zFloor, zSill, orient));
        if (zCeil > zHead + 0.01) {
          addToFloorAndLayer(floorObj.id, 'walls', makeExteriorOpeningWallBox(x0, y0, x1, y1, zHead, zCeil, orient));
        }
        const lGrp = new THREE.Group();
        const midX = 0.5 * (x0 + x1);
        const midY = 0.5 * (y0 + y1);
        lGrp.add(makeBox(x0, y0, x1, y1, zSill, zSill + 0.04, MATS.aluDark, false));
        lGrp.add(makeBox(x0, y0, x1, y1, zHead - 0.04, zHead, MATS.aluDark, false));
        if (orient === 'V') {
          lGrp.add(makeBox(x0, y0, x1, y0 + 0.04, zSill, zHead, MATS.aluDark, false));
          lGrp.add(makeBox(x0, y1 - 0.04, x1, y1, zSill, zHead, MATS.aluDark, false));
          lGrp.add(makeBox(midX - 0.03, midY - 0.02, midX + 0.03, midY + 0.02, zSill, zHead, MATS.aluDark, false));
          for (let z = zSill + 0.08; z < zHead - 0.06; z += 0.14) {
            lGrp.add(makeBox(midX - 0.04, y0 + 0.03, midX + 0.04, y1 - 0.03, z, z + 0.055, MATS.aluDark, false));
          }
          const inX = (midX < -10.0 || (midX > 0.0 && midX < 10.0)) ? (x1 - 0.02) : (x0 + 0.02);
          lGrp.add(makeBox(inX - 0.02, y0 + 0.02, inX + 0.02, y1 - 0.02, zSill, zHead, MATS.extWall, false));
        } else {
          lGrp.add(makeBox(x0, y0, x0 + 0.04, y1, zSill, zHead, MATS.aluDark, false));
          lGrp.add(makeBox(x1 - 0.04, y0, x1, y1, zSill, zHead, MATS.aluDark, false));
          for (let z = zSill + 0.08; z < zHead - 0.06; z += 0.14) {
            lGrp.add(makeBox(x0 + 0.03, midY - 0.04, x1 - 0.03, midY + 0.04, z, z + 0.055, MATS.aluDark, false));
          }
        }
        addToFloorAndLayer(floorObj.id, 'windows', lGrp);

      } else if (['window', 'win_small', 'win_tall', 'win_recess', 'win_gal', 'win_balc'].includes(kind)) {
        const span = (orient === 'H') ? (x1 - x0) : (y1 - y0);
        let zSill = zFloor + 1.05;
        if (kind === 'win_small') zSill = zFloor + 1.35;
        else if (kind === 'win_recess') zSill = zFloor + 0.70;
        else if (kind === 'win_gal' || kind === 'win_balc' || kind === 'win_tall') zSill = zFloor + 0.35;

        const zHead = Math.min(zFloor + 2.25, zCeil - 0.15);
        addToFloorAndLayer(floorObj.id, 'walls', makeExteriorOpeningWallBox(x0, y0, x1, y1, zFloor, zSill, orient));
        if (zCeil > zHead + 0.02) {
          addToFloorAndLayer(floorObj.id, 'walls', makeExteriorOpeningWallBox(x0, y0, x1, y1, zHead, zCeil, orient));
        }
        const wGrp = new THREE.Group();
        const fThick = 0.045;
        wGrp.add(makeBox(x0 - 0.01, y0 - 0.01, x1 + 0.01, y1 + 0.01, zSill - 0.03, zSill + 0.02, MATS.slabEdge, false));
        wGrp.add(makeBox(x0, y0, x1, y1, zHead - fThick, zHead, MATS.aluDark, false));

        // Lower horizontal transom bar at zFloor + 1.05m for 'win_recess', 'win_gal', and 'win_balc' per Garmushka Elevations!
        const hasTransom = (kind === 'win_recess' || kind === 'win_gal' || kind === 'win_balc');
        const zTransom = zFloor + 1.05;

        if (orient === 'H') {
          const midX = 0.5 * (x0 + x1);
          const midY = 0.5 * (y0 + y1);
          wGrp.add(makeBox(x0, y0, x0 + fThick, y1, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(x1 - fThick, y0, x1, y1, zSill, zHead, MATS.aluDark, false));
          if (hasTransom) {
            wGrp.add(makeBox(x0, midY - 0.035, x1, midY + 0.035, zTransom - 0.025, zTransom + 0.025, MATS.aluDark, false));
            wGrp.add(makeBox(midX - 0.02, midY - 0.03, midX + 0.02, midY + 0.03, zTransom, zHead, MATS.aluDark, false));
          } else if (span >= 1.10) {
            wGrp.add(makeBox(midX - 0.02, midY - 0.03, midX + 0.02, midY + 0.03, zSill, zHead, MATS.aluDark, false));
          }
          wGrp.add(makeBox(x0 + fThick, midY - 0.012, x1 - fThick, midY + 0.012, zSill + 0.02, zHead - fThick, MATS.winGlass, false));
        } else {
          const midX = 0.5 * (x0 + x1);
          const midY = 0.5 * (y0 + y1);
          wGrp.add(makeBox(x0, y0, x1, y0 + fThick, zSill, zHead, MATS.aluDark, false));
          wGrp.add(makeBox(x0, y1 - fThick, x1, y1, zSill, zHead, MATS.aluDark, false));
          if (hasTransom) {
            wGrp.add(makeBox(midX - 0.035, y0, midX + 0.035, y1, zTransom - 0.025, zTransom + 0.025, MATS.aluDark, false));
            wGrp.add(makeBox(midX - 0.03, midY - 0.02, midX + 0.03, midY + 0.02, zTransom, zHead, MATS.aluDark, false));
            if (kind === 'win_balc') {
              // Outer dark metal safety balustrade on West/East bedroom windows per East & West Elevations
              for (let py = y0 + 0.08; py <= y1 - 0.08; py += 0.16) {
                wGrp.add(makeBox(midX - 0.04, py - 0.01, midX + 0.04, py + 0.01, zSill, zTransom, MATS.aluDark, false));
              }
            }
          } else if (span >= 1.10) {
            wGrp.add(makeBox(midX - 0.03, midY - 0.02, midX + 0.03, midY + 0.02, zSill, zHead, MATS.aluDark, false));
          }
          wGrp.add(makeBox(midX - 0.012, y0 + fThick, midX + 0.012, y1 - fThick, zSill + 0.02, zHead - fThick, MATS.winGlass, false));
        }
        addToFloorAndLayer(floorObj.id, 'windows', wGrp);

      } else if (kind === 'door') {
        const zDoorTop = Math.min(zFloor + 2.10, zCeil - 0.15);
        if (zCeil > zDoorTop + 0.02) {
          addToFloorAndLayer(floorObj.id, 'walls', makeBox(x0, y0, x1, y1, zDoorTop, zCeil, MATS.extWall));
        }
        const dGrp = new THREE.Group();
        const fW = 0.04;
        dGrp.add(makeBox(x0, y0, x1, y1, zDoorTop - fW, zDoorTop, MATS.doorFrame, false));
        if (orient === 'H') {
          dGrp.add(makeBox(x0, y0, x0 + fW, y1, zFloor, zDoorTop, MATS.doorFrame, false));
          dGrp.add(makeBox(x1 - fW, y0, x1, y1, zFloor, zDoorTop, MATS.doorFrame, false));
          const leafW = Math.max(0.4, (x1 - x0) - 2 * fW);
          const leafGeo = new THREE.BoxGeometry(leafW, zDoorTop - zFloor - fW, 0.04);
          leafGeo.translate(leafW / 2, 0, 0);
          const leaf = new THREE.Mesh(leafGeo, MATS.lightWood);
          leaf.position.set(x0 + fW, zFloor + 0.5 * (zDoorTop - zFloor - fW), 0.5 * (y0 + y1));
          leaf.rotation.y = 0.38;
          dGrp.add(leaf);
        } else {
          dGrp.add(makeBox(x0, y0, x1, y0 + fW, zFloor, zDoorTop, MATS.doorFrame, false));
          dGrp.add(makeBox(x0, y1 - fW, x1, y1, zFloor, zDoorTop, MATS.doorFrame, false));
          const leafW = Math.max(0.4, (y1 - y0) - 2 * fW);
          const leafGeo = new THREE.BoxGeometry(0.04, zDoorTop - zFloor - fW, leafW);
          leafGeo.translate(0, 0, leafW / 2);
          const leaf = new THREE.Mesh(leafGeo, MATS.lightWood);
          leaf.position.set(0.5 * (x0 + x1), zFloor + 0.5 * (zDoorTop - zFloor - fW), y0 + fW);
          leaf.rotation.y = -0.38;
          dGrp.add(leaf);
        }
        addToFloorAndLayer(floorObj.id, 'doors', dGrp);
      }
    }"""

tmpl = re.sub(
    r"function makeExteriorOpeningWallBox\(x0, y0, x1, y1, z0, z1, orient\) \{[\s\S]*?function createFloorLabelMesh",
    NEW_OPENING_BUILDER + "\n\n    function createFloorLabelMesh",
    tmpl,
    count=1
)

# 5. Replace buildFloorSlabsAndBalconies(f) with:
#    - Exact Ground Floor Site Development Plan (Image 2: תכנית פיתוח קומת הקרקע):
#      * Open cut in the ground slab for the two-way underground garage ramp (מנסעה לחניון / רמפה דו-סטרית) on the West side (X = -20.15 .. -15.34, Y = -2.99 .. +17.50)
#      * Exact North & Side private duplex gardens (דשא), 1.75m deep paved patios (משטח מרוצף), and North-Central Courtyard garden
#      * Exact South front gardens, terracotta-paved central entrance courtyard, and kidney-shaped central garden island with 3D trees
#    - Gallery floor ('gal') slab ONLY on the North Duplex wing (Y = -13.24 .. +0.63m) so the South lobbies/club are a true double-height space (0.00..+6.12m)!
#    - Synthetic grass ('MATS.syntheticGrass') on the uppermost roof terrace ('f9' at +31.32m)!
NEW_SLABS_AND_BALCONIES = """    function createParkingStallMesh(st) {
      const grp = new THREE.Group();
      const zP = (st.level === 'bm2') ? -5.98 : -2.98;
      const c = document.createElement('canvas');
      c.width = 128; c.height = 256;
      const ctx = c.getContext('2d');
      ctx.fillStyle = 'rgba(30, 41, 59, 0.58)';
      ctx.fillRect(6, 6, 116, 244);
      ctx.strokeStyle = '#fbbf24';
      ctx.lineWidth = 5;
      ctx.strokeRect(6, 6, 116, 244);
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 34px "Segoe UI", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('P-' + st.num, 64, 130);
      const tex = new THREE.CanvasTexture(c);
      const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, side: THREE.DoubleSide, clippingPlanes });
      const geo = new THREE.PlaneGeometry(st.w, st.d);
      geo.rotateX(-Math.PI / 2);
      const m = new THREE.Mesh(geo, mat);
      m.position.set(st.x, zP, st.y);
      grp.add(m);
      return grp;
    }

    function getFootprintPts2D(ySouth) {
      return [
        [-3.17, -13.24], [-16.87, -13.24], [-16.87, -2.99], [-15.34, -2.99],
        [-15.34,  3.40], [-16.87,  3.40], [-16.87, ySouth], [-3.17, ySouth],
        [-3.17,   3.82], [  2.93,  3.82], [  2.93, ySouth], [16.63, ySouth],
        [16.63,   3.40], [ 15.10,  3.40], [ 15.10, -2.99], [16.63, -2.99],
        [16.63, -13.24], [  2.93, -13.24], [ 2.93, -3.42], [-3.17, -3.42]
      ];
    }

    function getGroundFootprintPts2D() {
      // On Ground ('kar'), West-South bay X = [-16.87, -15.34], Y = [-2.99, +13.65] is open for the 2-way garage ramp!
      return [
        [-3.17, -13.24], [-16.87, -13.24], [-16.87, -2.99], [-15.34, -2.99],
        [-15.34, 13.65], [ -3.17,  13.65], [ -3.17,  3.82], [  2.93,  3.82],
        [  2.93, 13.65], [ 16.63,  13.65], [ 16.63,  3.40], [ 15.10,  3.40],
        [ 15.10, -2.99], [ 16.63,  -2.99], [ 16.63, -13.24], [ 2.93, -13.24],
        [  2.93, -3.42], [ -3.17,  -3.42]
      ];
    }

    function getGalleryNorthSlabPts2D() {
      // On Gallery ('gal', +3.10m), ONLY the North Duplex Wing (Y = -13.24 .. +0.63m) has an intermediate floor slab!
      // The entire South Wing (Y = +0.63 .. +13.65m) is a Double-Height Lobby & Residents' Club (חלל כפול 0.00..+6.12m)!
      return [
        [-3.17, -13.24], [-16.87, -13.24], [-16.87, -2.99], [-15.34, -2.99],
        [-15.34,  0.63], [ 15.10,   0.63], [ 15.10, -2.99], [ 16.63, -2.99],
        [16.63, -13.24], [  2.93, -13.24], [  2.93, -3.42], [ -3.17, -3.42]
      ];
    }

    function buildSiteTree3D(grp, tx, ty, zBase, scale = 1.0) {
      const trunkH = 1.8 * scale;
      const trunkGeo = new THREE.CylinderGeometry(0.11 * scale, 0.16 * scale, trunkH, 8);
      const trunk = new THREE.Mesh(trunkGeo, MATS.doorFrame);
      trunk.position.set(tx, zBase + 0.5 * trunkH, ty);
      trunk.castShadow = true;
      grp.add(trunk);
      const cr1 = new THREE.Mesh(new THREE.SphereGeometry(1.15 * scale, 12, 10), MATS.gardenGrass);
      cr1.position.set(tx, zBase + trunkH + 0.65 * scale, ty);
      cr1.scale.set(1.0, 0.82, 1.0);
      cr1.castShadow = true;
      grp.add(cr1);
      const cr2 = new THREE.Mesh(new THREE.SphereGeometry(0.85 * scale, 10, 8), MATS.syntheticGrass);
      cr2.position.set(tx + 0.35 * scale, zBase + trunkH + 1.05 * scale, ty - 0.25 * scale);
      cr2.castShadow = true;
      grp.add(cr2);
    }

    function buildConcreteRoofPergola(floorId, x0, y0, x1, y1, zBase, zTop, isNorth) {
      const pGrp = new THREE.Group();
      const bThick = 0.25;
      if (isNorth) {
        pGrp.add(makeBox(x0, y0, x1, y0 + bThick, zBase, zTop, MATS.extWall));
      } else {
        pGrp.add(makeBox(x0, y1 - bThick, x1, y1, zBase, zTop, MATS.extWall));
      }
      pGrp.add(makeBox(x0, y0, x0 + 0.20, y1, zBase, zTop, MATS.extWall));
      pGrp.add(makeBox(x1 - 0.20, y0, x1, y1, zBase, zTop, MATS.extWall));
      const ry0 = isNorth ? (y0 + bThick) : y0;
      const ry1 = isNorth ? y1 : (y1 - bThick);
      for (let rx = x0 + 0.55; rx <= x1 - 0.70; rx += 0.65) {
        pGrp.add(makeBox(rx, ry0, rx + 0.25, ry1, zTop - 0.30, zTop, MATS.extWall));
      }
      addToFloorAndLayer(floorId, 'pergolas', pGrp);
    }

    function buildFloorSlabsAndBalconies(f) {
      const zF = f.zFloor;
      const zC = f.zCeil;
      const sThick = 0.22;

      // Dual Core 3D Staircase Flights inside the exact Core Towers (West cx=-10.72, East cx=+10.48, Y=-4.05..+0.35)
      if (f.id !== 'gag') {
        const stGrp = new THREE.Group();
        const zMid = 0.5 * (zF + zC);
        [-10.72, 10.48].forEach(cx => {
          stGrp.add(makeBox(cx - 1.15, -4.02, cx + 1.15, -3.15, zMid - 0.14, zMid, MATS.slabFloor));
          const nSteps = 8, sy0 = -3.15, sy1 = -1.10;
          const dy = (sy1 - sy0) / nSteps;
          const dz1 = (zMid - zF) / nSteps;
          const dz2 = (zC - zMid) / nSteps;
          for (let i = 0; i < nSteps; i++) {
            stGrp.add(makeBox(cx + 0.06, sy1 - (i + 1) * dy, cx + 1.10, sy1 - i * dy, zF + i * dz1 - 0.06, zF + (i + 1) * dz1, MATS.slabFloor));
            stGrp.add(makeBox(cx - 1.10, sy0 + i * dy, cx - 0.06, sy0 + (i + 1) * dy, zMid + i * dz2 - 0.06, zMid + (i + 1) * dz2, MATS.slabFloor));
          }
        });
        addToFloorAndLayer(f.id, (f.id === 'bm1' || f.id === 'bm2') ? 'site' : 'slabs', stGrp);
      }

      if (f.id === 'bm2' || f.id === 'bm1') {
        const matSlab = makeBox(-20.48, -17.71, 20.48, 17.50, zF - 0.35, zF, MATS.basementConcrete);
        addToFloorAndLayer(f.id, 'site', matSlab);

        const stallsGrp = new THREE.Group();
        PARKING_STALLS.filter(st => st.level === f.id).forEach(st => {
          stallsGrp.add(createParkingStallMesh(st));
        });
        addToFloorAndLayer(f.id, 'site', stallsGrp);

        if (f.id === 'bm1') {
          const hlGeo = new THREE.BoxGeometry(2.20, 1.4, 4.70);
          const hlMat = new THREE.MeshBasicMaterial({ color: 0x10b981, transparent: true, opacity: 0.48 });
          parkingHighlightMesh = new THREE.Mesh(hlGeo, hlMat);
          parkingHighlightMesh.visible = false;
          scene.add(parkingHighlightMesh);
        }

        // Two-Way Underground Garage Ramp (מנסעה לחניון / רמפה דו-סטרית, X = -20.15..-15.34)
        const rampGrp = new THREE.Group();
        const nSegs = 16;
        const ryStart = (f.id === 'bm1') ? 17.20 : 2.50;
        const ryEnd   = (f.id === 'bm1') ? -2.99 : -14.50;
        const rzStart = (f.id === 'bm1') ?  0.00 : -3.00;
        const rzEnd   = (f.id === 'bm1') ? -3.00 : -6.00;
        for (let i = 0; i < nSegs; i++) {
          const t0 = i / nSegs, t1 = (i + 1) / nSegs;
          const ry0 = ryStart + t0 * (ryEnd - ryStart);
          const ry1 = ryStart + t1 * (ryEnd - ryStart);
          const rz = 0.5 * ((rzStart + t0 * (rzEnd - rzStart)) + (rzStart + t1 * (rzEnd - rzStart)));
          rampGrp.add(makeBox(-20.15, Math.min(ry0, ry1), -15.34, Math.max(ry0, ry1), rz - 0.24, rz, MATS.asphalt));
          // Yellow center lane divider line (כניסה / יציאה)
          rampGrp.add(makeBox(-17.80, Math.min(ry0, ry1) + 0.15, -17.70, Math.max(ry0, ry1) - 0.15, rz, rz + 0.02, MATS.lightWood));
        }
        addToFloorAndLayer(f.id, 'site', rampGrp);
        return;
      }

      if (f.id === 'kar') {
        const siteGrp = new THREE.Group();
        // 1. Base Lot Slab with Open Cutout at X = [-20.15, -15.34], Y = [-2.99, +17.20] for the 2-Way Underground Garage Ramp!
        siteGrp.add(makeBox(-20.48, -17.71,  20.48,  -2.99, -0.06, -0.01, MATS.sidewalk));
        siteGrp.add(makeBox(-15.34,  -2.99,  20.48,  17.50, -0.06, -0.01, MATS.sidewalk));
        siteGrp.add(makeBox(-20.48,  -2.99, -20.15,  17.50, -0.06, -0.01, MATS.sidewalk));

        // 2. Visible Sloped Two-Way Garage Ramp (מנסעה לחניון / רמפה דו-סטרית) + Retaining Walls (קיר דיפון) & Safety Railings
        const nSegs = 16, ryStart = 17.20, ryEnd = -2.99, rzStart = 0.00, rzEnd = -3.00;
        for (let i = 0; i < nSegs; i++) {
          const t0 = i / nSegs, t1 = (i + 1) / nSegs;
          const ry0 = ryStart + t0 * (ryEnd - ryStart);
          const ry1 = ryStart + t1 * (ryEnd - ryStart);
          const rz = 0.5 * ((rzStart + t0 * (rzEnd - rzStart)) + (rzStart + t1 * (rzEnd - rzStart)));
          siteGrp.add(makeBox(-20.15, Math.min(ry0, ry1), -15.34, Math.max(ry0, ry1), rz - 0.22, rz, MATS.asphalt));
          siteGrp.add(makeBox(-17.80, Math.min(ry0, ry1) + 0.15, -17.70, Math.max(ry0, ry1) - 0.15, rz, rz + 0.02, MATS.lightWood));
        }
        // Ramp retaining walls (קיר דיפון) along West lot boundary (X=-20.35..-20.12), North end (Y=-3.15..-2.95), and East edge (X=-15.48..-15.30)
        siteGrp.add(makeBox(-20.35, -3.10, -20.12, 17.20, -3.00, 0.95, MATS.extWall));
        siteGrp.add(makeBox(-20.35, -3.15, -15.30, -2.95, -3.00, 0.95, MATS.extWall));
        siteGrp.add(makeBox(-15.48, -3.10, -15.30, 16.50, -3.00, 0.45, MATS.extWall));
        buildMetalPicketRailing(siteGrp, -20.28, -3.05, -20.16, 16.80, 0.95, 1.45, 'W');

        // 3. Exact North & Side Private Duplex Gardens (דשא / גינה) + 1.75m Paved Patios (משטח מרוצף) per Image 2 (תכנית פיתוח קומת הקרקע)
        // Paved Patios (משטח מרוצף, Y = -15.00 .. -13.24) outside each of the 4 North Garden Duplexes
        [[-16.87, -10.07], [-9.97, -3.17], [2.93, 9.73], [9.83, 16.63]].forEach(([px0, px1]) => {
          siteGrp.add(makeBox(px0, -15.00, px1, -13.24, 0.00, 0.04, MATS.patioPaver));
        });
        // North-Central Recess Paved Strip (Y = -5.20 .. -3.42)
        siteGrp.add(makeBox(-3.17, -5.20, 2.93, -3.42, 0.00, 0.04, MATS.patioPaver));
        // Lush Green Private Garden Lawns (גינה) wrapping North, North-Central Courtyard, West-North, and East-North
        siteGrp.add(makeBox(-20.10, -17.35, 19.85, -15.00, 0.00, 0.06, MATS.gardenGrass));
        siteGrp.add(makeBox( -3.17, -15.00,  2.93,  -5.20, 0.00, 0.06, MATS.gardenGrass));
        siteGrp.add(makeBox(-20.10, -15.00, -16.87, -3.15, 0.00, 0.06, MATS.gardenGrass));
        siteGrp.add(makeBox( 16.63, -15.00, 19.85,   3.40, 0.00, 0.06, MATS.gardenGrass));
        // Low garden dividing walls between the 4 private duplex gardens
        [-10.02, -0.12, 9.78].forEach(gx => {
          siteGrp.add(makeBox(gx - 0.08, -17.35, gx + 0.08, (gx === -0.12) ? -3.42 : -13.24, 0.00, 0.85, MATS.extWall));
        });

        // 4. Exact South Front Gardens, Terracotta-Paved Entrance Courtyard & Kidney-Shaped Central Planter Island per Image 2!
        // Central Terracotta-Paved Entrance Courtyard (X = -6.80 .. +2.93, Y = +3.82 .. +17.50) + West Lobby Path
        siteGrp.add(makeBox( -6.80,  3.82,  2.93, 17.50, 0.00, 0.035, MATS.terracottaPaver));
        siteGrp.add(makeBox(-15.34, 13.65, -13.50, 17.50, 0.00, 0.035, MATS.terracottaPaver));
        // South-East Terracotta-Paved Courtyard & East Side Path (X = +11.80 .. +18.30, Y = +13.65 .. +17.50 & X = +16.63 .. +18.30, Y = +3.40 .. +13.65)
        siteGrp.add(makeBox( 11.80, 13.65, 18.30, 17.50, 0.00, 0.035, MATS.terracottaPaver));
        siteGrp.add(makeBox( 16.63,  3.40, 18.30, 13.65, 0.00, 0.035, MATS.terracottaPaver));
        // Outer East Asphalt Path (שביל אספלט, X = +18.30 .. +20.40, Y = -2.00 .. +17.50)
        siteGrp.add(makeBox( 18.30, -2.00, 20.40, 17.50, -0.01, 0.02, MATS.asphalt));
        // West Front Garden (in front of Bldg 28: X = -13.50 .. -6.80, Y = +13.65 .. +17.15) with white concrete curb
        siteGrp.add(makeBox(-13.50, 13.65, -6.80, 17.15, 0.00, 0.14, MATS.extWall));
        siteGrp.add(makeBox(-13.38, 13.75, -6.92, 17.03, 0.14, 0.20, MATS.gardenGrass));
        // East Front Garden (in front of Bldg 26: X = +2.93 .. +11.80, Y = +13.65 .. +17.15) with white concrete curb
        siteGrp.add(makeBox(  2.93, 13.65, 11.80, 17.15, 0.00, 0.14, MATS.extWall));
        siteGrp.add(makeBox(  3.05, 13.75, 11.68, 17.03, 0.14, 0.20, MATS.gardenGrass));

        // Central Sculpted Organic Kidney-Shaped Garden Planter Island (X = -1.25 .. +1.05, Y = +5.20 .. +14.80) per Image 2!
        const islandPts = [
          [-0.95,  5.40], [-1.25,  7.20], [-0.85,  9.80], [-1.20, 12.40], [-0.80, 14.60],
          [ 0.65, 14.60], [ 1.05, 12.40], [ 0.55,  9.80], [ 0.95,  7.20], [ 0.60,  5.40]
        ];
        siteGrp.add(buildPolygonSlab(islandPts, 0.00, 0.18, MATS.extWall, MATS.extWall));
        const islandGrassPts = islandPts.map(([px, py]) => [px * 0.84, py]);
        siteGrp.add(buildPolygonSlab(islandGrassPts, 0.18, 0.24, MATS.gardenGrass, MATS.extWall));

        // 5. 3D Landscape Trees in exact Garmushka positions (Front Gardens, Central Planter Island, and North/Side Gardens)
        [
          [-11.6, 15.4, 0.95], [-9.2, 15.8, 0.85], [-8.0, 14.9, 0.75],
          [-0.1,  6.8, 0.85],  [-0.2, 10.2, 0.90], [ 0.0, 13.4, 0.85],
          [ 4.6, 15.5, 0.90],  [ 6.8, 15.9, 0.80], [ 8.8, 15.2, 0.95], [10.4, 15.6, 1.05],
          [-18.5, -15.8, 0.95], [-13.5, -16.2, 0.90], [-6.5, -16.2, 0.90], [0.0, -15.8, 0.95],
          [  6.5, -16.2, 0.90], [ 13.5, -16.2, 0.90], [18.2, -15.5, 1.00], [18.4, -7.5, 0.95]
        ].forEach(([tx, ty, sc]) => buildSiteTree3D(siteGrp, tx, ty, 0.15, sc));

        // 6. South Moshe Sharett Street Sidewalk & Roadway
        siteGrp.add(makeBox(-22.00, 17.15, 22.00, 18.80, -0.02, 0.03, MATS.terracottaPaver));
        siteGrp.add(makeBox(-22.00, 18.80, 22.00, 24.50, -0.14, -0.02, MATS.asphalt));
        addToFloorAndLayer('kar', 'site', siteGrp);

        // Ground floor building slab (with West-South ramp cut out!)
        addToFloorAndLayer('kar', 'slabs', buildPolygonSlab(getGroundFootprintPts2D(), -0.25, 0.00, MATS.slabFloor, MATS.slabEdge));

        // North Ground Floor HPL Wood Cladding Panels between the 1.20m window and 3.00m vitrine (Image 4: חזית צפונית)
        const hplKar = new THREE.Group();
        [[-14.64, -13.54], [-10.54, -9.34], [-6.34, -5.24], [5.00, 6.10], [9.10, 10.30], [13.30, 14.40]].forEach(([hx0, hx1]) => {
          hplKar.add(makeBox(hx0, -13.28, hx1, -13.20, 0.00, 2.25, MATS.luxFlutedOak));
        });
        addToFloorAndLayer('kar', 'pergolas', hplKar);
        return;
      }

      if (f.id === 'gal') {
        // Gallery Slab (+3.10m) ONLY on the North Duplex Wing (Y = -13.24 .. +0.63m) so South Lobbies & Club are true double-height (0.00..+6.12m)!
        addToFloorAndLayer('gal', 'slabs', buildPolygonSlab(getGalleryNorthSlabPts2D(), zF - sThick, zF, MATS.slabFloor, MATS.slabEdge));

        // Gallery North Facade HPL Wood Cladding Panels between each duplex's two bedroom windows + Central Recess Metal Railing (Image 4)
        const galAccents = new THREE.Group();
        [[-14.64, -11.74], [-8.14, -5.24], [5.00, 7.90], [11.50, 14.40]].forEach(([hx0, hx1]) => {
          galAccents.add(makeBox(hx0, -13.28, hx1, -13.20, zF + 0.35, zF + 2.25, MATS.luxFlutedOak));
        });
        buildMetalPicketRailing(galAccents, -3.17, -3.48, 2.93, -3.40, zF, zF + 1.05, 'N');
        addToFloorAndLayer('gal', 'pergolas', galAccents);
        return;
      }

      if (['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8'].includes(f.id)) {
        const isF8 = (f.id === 'f8');
        const ySouth = isF8 ? 12.15 : 13.65;
        addToFloorAndLayer(f.id, 'slabs', buildPolygonSlab(getFootprintPts2D(ySouth), zF - sThick, zF, MATS.slabFloor, MATS.slabEdge));

        // 4 North Sun Balconies spanning full half-wing width (6.85m each) with crisp white slab fascias & dark metal picket railings
        buildBalconyBox(f.id, -16.87, -14.99, -10.12, -13.24, zF, ['N', 'W'], false, 1.05, false);
        buildBalconyBox(f.id,  -9.92, -14.99,  -3.17, -13.24, zF, ['N', 'E'], false, 1.05, false);
        buildBalconyBox(f.id,   2.93, -14.99,   9.68, -13.24, zF, ['N', 'W'], false, 1.05, false);
        buildBalconyBox(f.id,   9.88, -14.99,  16.63, -13.24, zF, ['N', 'E'], false, 1.05, false);

        if (isF8) {
          // Floor 8 South Penthouse Terraces (Y = 12.15 .. 14.65m across full wing width -16.87..-3.17 and 2.93..16.63)
          buildBalconyBox('f8', -16.87, 12.15, -3.17, 14.65, zF, ['S', 'W', 'E'], false, 1.05, false);
          buildBalconyBox('f8',   2.93, 12.15, 16.63, 14.65, zF, ['S', 'W', 'E'], false, 1.05, false);
          // Exterior Stairs climbing from Floor 8 South Penthouse Terrace (+28.17) up to Floor 9 Private Roof Terrace (+31.32)
          const extStGrp = new THREE.Group();
          [[-16.45, -15.45], [15.20, 16.20]].forEach(([sx0, sx1]) => {
            const nSt = 12, sy0 = 12.20, sy1 = 14.35, dz = (zC + 0.22 - zF) / nSt, dy = (sy1 - sy0) / nSt;
            for (let i = 0; i < nSt; i++) {
              extStGrp.add(makeBox(sx0, sy1 - (i + 1) * dy, sx1, sy1 - i * dy, zF + i * dz, zF + (i + 1) * dz, MATS.luxFlutedOak));
            }
          });
          addToFloorAndLayer('f8', 'slabs', extStGrp);
        } else {
          // Typical Floors 1..7 South Sun Balconies spanning full half-wing width (6.85m each, Y = 13.65 .. 15.40m)
          buildBalconyBox(f.id, -16.87, 13.65, -10.12, 15.40, zF, ['S', 'W'], false, 1.05, false);
          buildBalconyBox(f.id,  -9.92, 13.65,  -3.17, 15.40, zF, ['S', 'E'], false, 1.05, false);
          buildBalconyBox(f.id,   2.93, 13.65,   9.68, 15.40, zF, ['S', 'W'], false, 1.05, false);
          buildBalconyBox(f.id,   9.88, 13.65,  16.63, 15.40, zF, ['S', 'E'], false, 1.05, false);
        }

        // Signature Warm HPL Wood-Look Facade Cladding Panels (HPL דמוי טרספה) on the wall behind the balconies between windows & vitrines (Image 4 & 5)
        const hplGrp = new THREE.Group();
        [[-14.64, -13.54], [-10.54, -9.34], [-6.34, -5.24], [5.00, 6.10], [9.10, 10.30], [13.30, 14.40]].forEach(([hx0, hx1]) => {
          hplGrp.add(makeBox(hx0, -13.28, hx1, -13.20, zF, zF + 2.25, MATS.luxFlutedOak));
          if (!isF8) {
            hplGrp.add(makeBox(hx0, 13.61, hx1, 13.69, zF, zF + 2.25, MATS.luxFlutedOak));
          }
        });
        // West & East Side Facade HPL Accents between the bedroom windows (Y = -11.34..-10.29 and Y = 10.70..11.75)
        hplGrp.add(makeBox(-16.90, -11.34, -16.83, -10.29, zF, zF + 2.25, MATS.luxFlutedOak));
        hplGrp.add(makeBox( 16.59, -11.34,  16.66, -10.29, zF, zF + 2.25, MATS.luxFlutedOak));
        if (!isF8) {
          hplGrp.add(makeBox(-16.90, 10.70, -16.83, 11.75, zF, zF + 2.25, MATS.luxFlutedOak));
          hplGrp.add(makeBox( 16.59, 10.70,  16.66, 11.75, zF, zF + 2.25, MATS.luxFlutedOak));
        }
        // Central Recess crisp white floor slab band across X = -3.17..+2.93 on North (Y=-3.42) & South (Y=+3.82) per Image 1, 3, 4, 5
        hplGrp.add(makeBox(-3.17, -3.46, 2.93, -3.38, zF - 0.22, zF, MATS.extWall));
        hplGrp.add(makeBox(-3.17,  3.78, 2.93,  3.86, zF - 0.22, zF, MATS.extWall));
        addToFloorAndLayer(f.id, 'pergolas', hplGrp);
        return;
      }

      if (f.id === 'f9') {
        // 1. Main Roof Slab (+31.07 .. +31.32m) across the exact 20-vertex footprint
        addToFloorAndLayer('f9', 'slabs', buildPolygonSlab(getFootprintPts2D(12.15), zF - 0.25, zF, MATS.terraceFloor, MATS.extWall));

        // 2. Solid White Perimeter Parapet Wall (מעקה בנוי +32.37, height 1.05m from +31.32 to +32.37) around the entire 20-vertex roof perimeter!
        const zParapet = zF + 1.05; // +32.37m
        const pGrp = new THREE.Group();
        const outerPts = getFootprintPts2D(12.15);
        for (let i = 0; i < outerPts.length; i++) {
          const [xA, yA] = outerPts[i];
          const [xB, yB] = outerPts[(i + 1) % outerPts.length];
          const x0 = Math.min(xA, xB) - (Math.abs(xA - xB) < 0.05 ? 0.10 : 0.0);
          const x1 = Math.max(xA, xB) + (Math.abs(xA - xB) < 0.05 ? 0.10 : 0.0);
          const y0 = Math.min(yA, yB) - (Math.abs(yA - yB) < 0.05 ? 0.10 : 0.0);
          const y1 = Math.max(yA, yB) + (Math.abs(yA - yB) < 0.05 ? 0.10 : 0.0);
          pGrp.add(makeBox(x0, y0, x1, y1, zF, zParapet, MATS.extWall));
        }
        pGrp.add(makeBox(-16.67, 3.42, -3.37, 3.62, zF, zParapet, MATS.extWall));
        pGrp.add(makeBox(  3.13, 3.42, 16.43, 3.62, zF, zParapet, MATS.extWall));
        addToFloorAndLayer('f9', 'walls', pGrp);

        // 3. Uppermost Private Roof Terraces (גג פרטי לדירה 32 ו-33, Y = 3.62 .. 11.95m) surfaced with Lush Synthetic Grass (דשא סינטטי) per User Request!
        const deckGrp = new THREE.Group();
        deckGrp.add(makeBox(-16.65, 3.62, -3.39, 11.95, zF, zF + 0.04, MATS.syntheticGrass));
        deckGrp.add(makeBox(  3.15, 3.62, 16.41, 11.95, zF, zF + 0.04, MATS.syntheticGrass));
        buildPines48BalconyLounge(deckGrp, -10.0, 7.8, 5.2, 3.6, zF + 0.04);
        buildPines48BalconyLounge(deckGrp,   9.8, 7.8, 5.2, 3.6, zF + 0.04);
        addToFloorAndLayer('f9', 'balconies', deckGrp);

        // 4. Integrated White Concrete Roof Pergolas (פרגולה בטון at +31.32 .. +32.37m) on North & South edges per Garmushka plan_upper_roof
        buildConcreteRoofPergola('f9', -16.87, -14.99, -10.02, -13.24, zF, zParapet, true);
        buildConcreteRoofPergola('f9', -10.02, -14.99,  -3.17, -13.24, zF, zParapet, true);
        buildConcreteRoofPergola('f9',   2.93, -14.99,   9.78, -13.24, zF, zParapet, true);
        buildConcreteRoofPergola('f9',   9.78, -14.99,  16.63, -13.24, zF, zParapet, true);

        buildConcreteRoofPergola('f9', -16.87,  12.15, -10.02,  13.66, zF, zParapet, false);
        buildConcreteRoofPergola('f9', -10.02,  12.15,  -3.17,  13.66, zF, zParapet, false);
        buildConcreteRoofPergola('f9',   2.93,  12.15,   9.78,  13.66, zF, zParapet, false);
        buildConcreteRoofPergola('f9',   9.78,  12.15,  16.63,  13.66, zF, zParapet, false);

        // 5. Low Solar Water Heater Collectors (קולטי שמש) on North Technical Roof (hidden inside the +32.37m parapet!)
        const solarGrp = new THREE.Group();
        [-12.50, -9.76, -7.18].forEach(sy => {
          [-15.44, -13.62, -11.80, -9.97, -8.15, -6.33, 4.22, 6.05, 7.87, 9.69, 11.51, 13.34].forEach(sx => {
            solarGrp.add(makeBox(sx, sy, sx + 1.48, sy + 1.95, zF + 0.08, zF + 0.62, MATS.solarPanel));
          });
        });
        addToFloorAndLayer('f9', 'pergolas', solarGrp);
        return;
      }

      if (f.id === 'gag') {
        // Upper Roof Slabs capping ONLY the two Stair/Elevator Core Towers (+33.77m stair roof & +34.27m elevator shaft top)
        const gagGrp = new THREE.Group();
        gagGrp.add(makeBox(-12.15, -4.28, -9.30, 0.63, zF - 0.20, zF, MATS.extWall));
        gagGrp.add(makeBox(  9.05, -4.28, 11.91, 0.63, zF - 0.20, zF, MATS.extWall));
        gagGrp.add(makeBox(-12.15, -2.06, -9.30, 0.63, zC - 0.18, zC, MATS.extWall));
        gagGrp.add(makeBox(  9.05, -2.06, 11.91, 0.63, zC - 0.18, zC, MATS.extWall));
        addToFloorAndLayer('gag', 'slabs', gagGrp);
        return;
      }
    }"""

tmpl = re.sub(
    r"function createParkingStallMesh\(st\) \{[\s\S]*?function makeCylinder",
    NEW_SLABS_AND_BALCONIES + "\n\n    function makeCylinder",
    tmpl,
    count=1
)

# 6. Replace buildPines48StyleFloorInteriors & buildAllFloors to furnish Floors 4, 5, and 8 cleanly inside exact Garmushka room boxes!
NEW_INTERIORS_AND_BUILD = """    function buildSharettLivingAndDining(grp, x0, y0, x1, y1, zF, zC, isNorth, sofaWall, kCorner) {
      // 1. Travertine floor zone strictly inside the room walls
      grp.add(makeBox(x0 + 0.08, y0 + 0.08, x1 - 0.08, y1 - 0.08, zF + 0.004, zF + 0.014, MATS.luxTravertine, false));

      // 2. Living Room Sitting Area (Sofa + Rug + Coffee Table + Media Console)
      const sY = isNorth ? (y0 + 1.85) : (y1 - 1.85);
      const sX = (sofaWall === 'W') ? (x0 + 1.45) : (x1 - 1.45);
      grp.add(makeBox(sX - 1.25, sY - 1.35, sX + 1.25, sY + 1.35, zF + 0.015, zF + 0.026, MATS.luxRug, false));

      // 3-Seater Italian Bouclé Sofa against sofaWall ('W' or 'E')
      const sw0 = (sofaWall === 'W') ? (x0 + 0.16) : (x1 - 0.98);
      const sw1 = (sofaWall === 'W') ? (x0 + 0.98) : (x1 - 0.16);
      grp.add(makeBox(sw0, sY - 1.05, sw1, sY + 1.05, zF + 0.03, zF + 0.11, MATS.luxOakSmooth));
      grp.add(makeBox(sw0, sY - 1.05, sw1, sY + 1.05, zF + 0.11, zF + 0.42, MATS.luxBoucle));
      const backX0 = (sofaWall === 'W') ? sw0 : (sw1 - 0.18);
      const backX1 = (sofaWall === 'W') ? (sw0 + 0.18) : sw1;
      grp.add(makeBox(backX0, sY - 1.05, backX1, sY + 1.05, zF + 0.42, zF + 0.76, MATS.luxBoucle));
      grp.add(makeBox(sw0, sY - 1.05, sw1, sY - 0.89, zF + 0.42, zF + 0.64, MATS.luxBoucle));
      grp.add(makeBox(sw0, sY + 0.89, sw1, sY + 1.05, zF + 0.42, zF + 0.64, MATS.luxBoucle));

      // Calacatta Marble Coffee Table
      const ctX = (sofaWall === 'W') ? (sw1 + 0.58) : (sw0 - 0.58);
      grp.add(makeCylinder(ctX, sY - 0.30, 0.16, 0.16, zF + 0.03, zF + 0.35, MATS.luxFlutedOak, 14));
      grp.add(makeCylinder(ctX, sY + 0.30, 0.16, 0.16, zF + 0.03, zF + 0.35, MATS.luxFlutedOak, 14));
      grp.add(makeBox(ctX - 0.38, sY - 0.58, ctX + 0.38, sY + 0.58, zF + 0.35, zF + 0.40, MATS.luxCalacatta));
      grp.add(makeCylinder(ctX, sY, 0.08, 0.09, zF + 0.40, zF + 0.58, MATS.luxPlantOlive, 10));

      // Accent Lounge Armchair on inner side of rug
      const chY = isNorth ? (sY + 1.05) : (sY - 1.05);
      grp.add(makeBox(ctX - 0.35, chY - 0.32, ctX + 0.35, chY + 0.32, zF + 0.03, zF + 0.40, MATS.luxBoucle));

      // 3. Kitchen Cabinetry & Dining Table in the opposite side of the room (kCorner: 'W' or 'E')
      const kY = isNorth ? (y1 - 0.90) : (y0 + 0.90);
      const kx0 = (kCorner === 'W') ? (x0 + 0.14) : (x1 - 2.65);
      const kx1 = (kCorner === 'W') ? (x0 + 2.65) : (x1 - 0.14);
      const kwY0 = isNorth ? (y1 - 0.72) : (y0 + 0.10);
      const kwY1 = isNorth ? (y1 - 0.10) : (y0 + 0.72);
      grp.add(makeBox(kx0, kwY0, kx1, kwY1, zF + 0.02, zF + 0.88, MATS.luxCabinet));
      grp.add(makeBox(kx0 - 0.01, kwY0 - 0.01, kx1 + 0.01, kwY1 + 0.01, zF + 0.88, zF + 0.92, MATS.luxCalacatta));
      grp.add(makeBox(kx0, kwY0, kx1, kwY1, zF + 1.52, zF + 2.15, MATS.luxFlutedOak));

      // Dining Table & 4 Chairs
      const dtX = (kCorner === 'W') ? (x0 + 1.40) : (x1 - 1.40);
      const dtY = isNorth ? (y0 + 2.40) : (y1 - 2.40);
      grp.add(makeBox(dtX - 0.75, dtY - 0.45, dtX + 0.75, dtY + 0.45, zF + 0.72, zF + 0.77, MATS.luxCalacatta));
      grp.add(makeCylinder(dtX - 0.42, dtY, 0.12, 0.14, zF + 0.02, zF + 0.72, MATS.luxFlutedOak, 12));
      grp.add(makeCylinder(dtX + 0.42, dtY, 0.12, 0.14, zF + 0.02, zF + 0.72, MATS.luxFlutedOak, 12));
      [-0.42, 0.42].forEach(dx => {
        [-0.62, 0.62].forEach(dy => {
          grp.add(makeBox(dtX + dx - 0.18, dtY + dy - 0.18, dtX + dx + 0.18, dtY + dy + 0.18, zF + 0.02, zF + 0.46, MATS.luxBoucle));
        });
      });
    }

    function buildSharettBedroom(grp, x0, y0, x1, y1, zF, zC, headWall, isMaster) {
      // 1. Warm Oak Parquet Floor strictly inside the room walls (zero wall bleed!)
      grp.add(makeBox(x0 + 0.08, y0 + 0.08, x1 - 0.08, y1 - 0.08, zF + 0.004, zF + 0.015, MATS.woodDeck, false));
      const cx = 0.5 * (x0 + x1);
      const cy = 0.5 * (y0 + y1);
      const rw = x1 - x0;
      const rd = y1 - y0;
      grp.add(makeBox(cx - Math.min(1.05, rw * 0.36), cy - Math.min(1.10, rd * 0.36), cx + Math.min(1.05, rw * 0.36), cy + Math.min(1.10, rd * 0.36), zF + 0.015, zF + 0.026, MATS.luxRug, false));

      const bedW = isMaster ? 1.64 : 1.36;
      const bedL = isMaster ? 1.98 : 1.86;

      if (headWall === 'W' || headWall === 'E') {
        const hx = (headWall === 'W') ? (x0 + 0.12) : (x1 - 0.12);
        const dir = (headWall === 'W') ? 1 : -1;
        const bx0 = Math.min(hx, hx + dir * bedL);
        const bx1 = Math.max(hx, hx + dir * bedL);
        const hbx0 = Math.min(hx, hx + dir * 0.12);
        const hbx1 = Math.max(hx, hx + dir * 0.12);
        grp.add(makeBox(hbx0, cy - bedW * 0.54, hbx1, cy + bedW * 0.54, zF + 0.02, zF + 0.72, MATS.luxFlutedOak));
        grp.add(makeBox(bx0, cy - bedW * 0.50, bx1, cy + bedW * 0.50, zF + 0.08, zF + 0.28, MATS.luxOakSmooth));
        grp.add(makeBox(bx0 + 0.05, cy - bedW * 0.46, bx1 - 0.05, cy + bedW * 0.46, zF + 0.28, zF + 0.48, MATS.luxCeramic));
        const pilX0 = Math.min(hx + dir * 0.14, hx + dir * 0.42);
        const pilX1 = Math.max(hx + dir * 0.14, hx + dir * 0.42);
        grp.add(makeBox(pilX0, cy - bedW * 0.40, pilX1, cy - 0.05, zF + 0.48, zF + 0.58, MATS.luxBoucle));
        grp.add(makeBox(pilX0, cy + 0.05, pilX1, cy + bedW * 0.40, zF + 0.48, zF + 0.58, MATS.luxBoucle));
      } else {
        const hy = (headWall === 'N') ? (y0 + 0.12) : (y1 - 0.12);
        const dir = (headWall === 'N') ? 1 : -1;
        const by0 = Math.min(hy, hy + dir * bedL);
        const by1 = Math.max(hy, hy + dir * bedL);
        const hby0 = Math.min(hy, hy + dir * 0.12);
        const hby1 = Math.max(hy, hy + dir * 0.12);
        grp.add(makeBox(cx - bedW * 0.54, hby0, cx + bedW * 0.54, hby1, zF + 0.02, zF + 0.72, MATS.luxFlutedOak));
        grp.add(makeBox(cx - bedW * 0.50, by0, cx + bedW * 0.50, by1, zF + 0.08, zF + 0.28, MATS.luxOakSmooth));
        grp.add(makeBox(cx - bedW * 0.46, by0 + 0.05, cx + bedW * 0.46, by1 - 0.05, zF + 0.28, zF + 0.48, MATS.luxCeramic));
        const pilY0 = Math.min(hy + dir * 0.14, hy + dir * 0.42);
        const pilY1 = Math.max(hy + dir * 0.14, hy + dir * 0.42);
        grp.add(makeBox(cx - bedW * 0.40, pilY0, cx - 0.05, pilY1, zF + 0.48, zF + 0.58, MATS.luxBoucle));
        grp.add(makeBox(cx + 0.05, pilY0, cx + bedW * 0.40, pilY1, zF + 0.48, zF + 0.58, MATS.luxBoucle));
      }
    }

    function buildPines48StyleFloorInteriors(f, pData) {
      const fGrp = new THREE.Group();
      const zF = f.zFloor;
      const zC = f.zCeil;

      // 1. North Apartments (NW28, NE28, NW26, NE26) — exact room boxes from debug_f345.png & debug_f8.png
      // Living + Kitchen + Dining Rooms
      buildSharettLivingAndDining(fGrp, -16.62, -12.99, -10.12, -8.65, zF, zC, true, 'E', 'W');
      buildSharettLivingAndDining(fGrp,  -9.92, -12.99,  -3.42, -8.10, zF, zC, true, 'W', 'E');
      buildSharettLivingAndDining(fGrp,   3.18, -12.99,   9.68, -8.10, zF, zC, true, 'E', 'W');
      buildSharettLivingAndDining(fGrp,   9.88, -12.99,  16.38, -8.65, zF, zC, true, 'W', 'E');

      // North Master & Secondary Bedrooms + Mamads (strictly inside each room's 4 walls!)
      buildSharettBedroom(fGrp, -16.62, -6.25, -13.35, -3.15, zF, zC, 'W', true);
      buildSharettBedroom(fGrp, -15.05, -2.85, -12.15, -0.10, zF, zC, 'S', false);
      buildSharettBedroom(fGrp,  -6.45, -5.65,  -3.42, -2.85, zF, zC, 'S', false);
      buildSharettBedroom(fGrp,  -3.17, -3.20,  -0.25, -0.10, zF, zC, 'E', true);

      buildSharettBedroom(fGrp,   0.02, -3.20,   2.93, -0.10, zF, zC, 'W', true);
      buildSharettBedroom(fGrp,   3.18, -5.65,   6.20, -2.85, zF, zC, 'S', false);
      buildSharettBedroom(fGrp,  11.90, -2.85,  14.80, -0.10, zF, zC, 'S', false);
      buildSharettBedroom(fGrp,  13.10, -6.25,  16.38, -3.15, zF, zC, 'E', true);

      // North Bathrooms (Calacatta marble floors & vanities inside exact bathroom walls)
      buildPines48Bathroom(fGrp, -15.10, -7.45, 2.6, 1.8, zF, zC);
      buildPines48Bathroom(fGrp,  -5.05, -6.90, 2.6, 1.8, zF, zC);
      buildPines48Bathroom(fGrp,   4.80, -6.90, 2.6, 1.8, zF, zC);
      buildPines48Bathroom(fGrp,  14.85, -7.45, 2.6, 1.8, zF, zC);

      // North Balcony Lounges
      [-13.5, -6.5, 6.3, 13.3].forEach(wx => buildPines48BalconyLounge(fGrp, wx, -14.1, 3.0, 1.4, zF));

      if (f.id === 'f8') {
        // 2. Floor 8 South Penthouses (#32 in Bldg 28 West, #33 in Bldg 26 East) — exact Garmushka layout from debug_f8.png!
        // Penthouse #32 (West Wing) & #33 (East Wing) Expansive South Living + Dining + Island Kitchen (X = -16.62..-8.35 and +8.10..+16.38, Y = +7.10..+11.90)
        buildSharettLivingAndDining(fGrp, -16.62, 7.15, -8.35, 11.90, zF, zC, false, 'W', 'E');
        buildSharettLivingAndDining(fGrp,   8.10, 7.15, 16.38, 11.90, zF, zC, false, 'E', 'W');

        // Penthouse #32 & #33 Bedrooms in exact room boxes (zero wall overlap!)
        buildSharettBedroom(fGrp,  -6.45, 8.85, -3.42, 11.90, zF, zC, 'S', true);   // South-Inner Master Suite #32
        buildSharettBedroom(fGrp, -16.62, 3.65, -13.35,  6.75, zF, zC, 'W', true);   // West Middle Bedroom #32
        buildSharettBedroom(fGrp, -15.05, 0.10, -12.15,  3.25, zF, zC, 'N', false);  // West Waist Bedroom #32
        buildSharettBedroom(fGrp,  -6.45, 3.15,  -3.42,  5.95, zF, zC, 'N', false);  // Inner-South Bedroom #32
        buildSharettBedroom(fGrp,  -3.17, 0.10,  -0.25,  3.55, zF, zC, 'E', true);   // Central Bridge Mamad #32

        buildSharettBedroom(fGrp,   3.18, 8.85,   6.20, 11.90, zF, zC, 'S', true);   // South-Inner Master Suite #33
        buildSharettBedroom(fGrp,  13.10, 3.65,  16.38,  6.75, zF, zC, 'E', true);   // East Middle Bedroom #33
        buildSharettBedroom(fGrp,  11.90, 0.10,  14.80,  3.25, zF, zC, 'N', false);  // East Waist Bedroom #33
        buildSharettBedroom(fGrp,   3.18, 3.15,   6.20,  5.95, zF, zC, 'N', false);  // Inner-South Bedroom #33
        buildSharettBedroom(fGrp,   0.02, 0.10,   2.93,  3.55, zF, zC, 'W', true);   // Central Bridge Mamad #33

        // Penthouse Bathrooms (inside X = -6.45..-3.42, Y = 6.20..8.55 and X = 3.18..6.20, Y = 6.20..8.55)
        buildPines48Bathroom(fGrp, -5.05, 7.35, 2.4, 1.9, zF, zC);
        buildPines48Bathroom(fGrp,  4.80, 7.35, 2.4, 1.9, zF, zC);

        // Penthouse South Terraces
        buildPines48BalconyLounge(fGrp, -10.5, 13.4, 5.0, 2.0, zF);
        buildPines48BalconyLounge(fGrp,  10.3, 13.4, 5.0, 2.0, zF);
      } else {
        // 3. Typical Floors 4 & 5 South Apartments (SW28, SE28, SW26, SE26) — exact room boxes from debug_f345.png!
        buildSharettLivingAndDining(fGrp, -16.62, 9.05, -10.12, 13.40, zF, zC, false, 'E', 'W');
        buildSharettLivingAndDining(fGrp,  -9.92, 8.55,  -3.42, 13.40, zF, zC, false, 'W', 'E');
        buildSharettLivingAndDining(fGrp,   3.18, 8.55,   9.68, 13.40, zF, zC, false, 'E', 'W');
        buildSharettLivingAndDining(fGrp,   9.88, 9.05,  16.38, 13.40, zF, zC, false, 'W', 'E');

        buildSharettBedroom(fGrp, -16.62, 3.65, -13.35,  6.70, zF, zC, 'W', true);
        buildSharettBedroom(fGrp, -15.05, 0.10, -12.15,  3.25, zF, zC, 'N', false);
        buildSharettBedroom(fGrp,  -6.45, 3.15,  -3.42,  5.95, zF, zC, 'N', false);
        buildSharettBedroom(fGrp,  -3.17, 0.10,  -0.25,  3.55, zF, zC, 'E', true);

        buildSharettBedroom(fGrp,   0.02, 0.10,   2.93,  3.55, zF, zC, 'W', true);
        buildSharettBedroom(fGrp,   3.18, 3.15,   6.20,  5.95, zF, zC, 'N', false);
        buildSharettBedroom(fGrp,  11.90, 0.10,  14.80,  3.25, zF, zC, 'N', false);
        buildSharettBedroom(fGrp,  13.10, 3.65,  16.38,  6.70, zF, zC, 'E', true);

        buildPines48Bathroom(fGrp, -15.10, 7.85, 2.6, 1.8, zF, zC);
        buildPines48Bathroom(fGrp,  -5.05, 7.35, 2.6, 1.8, zF, zC);
        buildPines48Bathroom(fGrp,   4.80, 7.35, 2.6, 1.8, zF, zC);
        buildPines48Bathroom(fGrp,  14.85, 7.85, 2.6, 1.8, zF, zC);

        [-13.5, -6.5, 6.3, 13.3].forEach(wx => buildPines48BalconyLounge(fGrp, wx, 14.5, 3.0, 1.4, zF));
      }

      [[-11.5, -8.5], [11.5, -8.5], [-11.5, 8.5], [11.5, 8.5]].forEach(([lx, ly]) => {
        const pl = new THREE.PointLight(0xfff3d6, 0.36, 14.0, 1.6);
        pl.position.set(lx, zC - 0.25, ly);
        fGrp.add(pl);
      });

      addToFloorAndLayer(f.id, 'furn3d', fGrp);
    }

    function buildAllFloors() {
      FLOORS.forEach(f => {
        const pData = PLANS[f.sheet];
        if (!pData) return;

        buildFloorSlabsAndBalconies(f);

        const isBm = (f.id === 'bm1' || f.id === 'bm2');
        const zWallTop = (f.id === 'kar' || f.id === 'gal') ? f.zTop : f.zCeil;
        pData.wall_polys.forEach(wp => {
          const z0 = f.zFloor;
          const z1 = zWallTop;
          const wMesh = buildExtrudedTriPoly(wp, z0, z1, isBm ? MATS.basementConcrete : MATS.wall, MATS.wallCap, f.sheet, isBm ? null : MATS.extWall);
          addToFloorAndLayer(f.id, isBm ? 'site' : 'walls', wMesh);
        });

        (pData.openings || []).forEach(op => {
          buildOpening3D(f, op);
        });

        if (f.has3DFurn) {
          buildPines48StyleFloorInteriors(f, pData);
        }

        // Render exact 2D architectural furniture floor drawings on ALL floors (including 3D-furnished floors!)
        const zLine = f.zFloor + 0.032;
        if (pData.furn_lines && pData.furn_lines.length > 0) {
          const fPts = [];
          pData.furn_lines.forEach(s => {
            if (f.id === 'gal' && s[1] > 0.6 && s[3] > 0.6) return;
            fPts.push(s[0], zLine, s[1], s[2], zLine, s[3]);
          });
          if (fPts.length > 0) {
            const fGeo = new THREE.BufferGeometry();
            fGeo.setAttribute('position', new THREE.Float32BufferAttribute(fPts, 3));
            const fLines = new THREE.LineSegments(fGeo, MATS.lineFurn);
            addToFloorAndLayer(f.id, 'cad2d', fLines);
          }
        }
        if (pData.cad_lines && pData.cad_lines.length > 0) {
          const cPts = [];
          pData.cad_lines.forEach(s => {
            if (f.id === 'gal' && s[1] > 0.6 && s[3] > 0.6) return;
            cPts.push(s[0], zLine + 0.003, s[1], s[2], zLine + 0.003, s[3]);
          });
          if (cPts.length > 0) {
            const cGeo = new THREE.BufferGeometry();
            cGeo.setAttribute('position', new THREE.Float32BufferAttribute(cPts, 3));
            const cLines = new THREE.LineSegments(cGeo, MATS.lineCad);
            addToFloorAndLayer(f.id, 'cad2d', cLines);
          }
        }

        (pData.room_labels || []).forEach(rl => {
          const lblMesh = createFloorLabelMesh(rl.name, rl.dims, rl.x, rl.y, f.zFloor);
          addToFloorAndLayer(f.id, 'labels', lblMesh);
        });
      });
    }"""

tmpl = re.sub(
    r"function buildPines48StyleFloorInteriors\(f, pData\) \{[\s\S]*?buildAllFloors\(\);",
    NEW_INTERIORS_AND_BUILD + "\n\n    buildAllFloors();",
    tmpl,
    count=1
)

# 7. Update Georeferencing constants & Exterior Callouts for Moshe Sharett 26-28
# Calibrated on closeup_z19.png so the building lot sits squarely on Parcel 1025 and South street aligns with Moshe Sharett St!
tmpl = tmpl.replace("const CENTER_LAT = 32.081724;", "const CENTER_LAT = 32.088485;")
tmpl = tmpl.replace("const CENTER_LON = 34.890301;", "const CENTER_LON = 34.871580;")
tmpl = tmpl.replace("const SCENE_CX = 0.2;", "const SCENE_CX = 3.8;")
tmpl = tmpl.replace("const SCENE_CZ = -9.2;", "const SCENE_CZ = -5.0;")
tmpl = tmpl.replace("const GMAPS_THETA = -14.8 * Math.PI / 180.0;", "const GMAPS_THETA = +6.8 * Math.PI / 180.0;")

NEW_CALLOUTS = """    const exteriorCallouts = [
      { text: "בניין 28 (אגף מערבי) · 33 יח\\"ד · גג +34.27", pos: new THREE.Vector3(-10.7, 35.0, -1.0), cls: "b37" },
      { text: "בניין 26 (אגף מזרחי) · 33 יח\\"ד · גג +34.27", pos: new THREE.Vector3( 10.5, 35.0, -1.0), cls: "b39" },
      { text: "רחוב משה שרת 26–28 (חזית דרומית)",            pos: new THREE.Vector3(  0.0,  1.2, 18.5), cls: "street" },
      { text: "גוש 6372 חלקה 1025 · 1,497 מ\\"ר · 70 חניות", pos: new THREE.Vector3(  0.0,  2.6, -15.5), cls: "" }
    ];"""
tmpl = re.sub(r"const exteriorCallouts = \[[\s\S]*?\];", NEW_CALLOUTS, tmpl, count=1)

# 8. Remove spiderweb radial GIS lines cutting through the building facades
tmpl = tmpl.replace(
    "subGrp.add(new THREE.Line(lineGeom, lineMat));",
    "// radial line omitted so building facades remain 100% clean"
)

# 9. Update Parking Highlight button handler to switch to the unit's specific basement level (bm1 or bm2)
tmpl = tmpl.replace(
    "selectFloor('mar');\n        if (parkingHighlightMesh) {\n          parkingHighlightMesh.visible = true;\n          parkingHighlightMesh.position.set(u.parkingX, -3.10, u.parkingY);\n        }\n        camState.target.set(u.parkingX, -3.5, u.parkingY);",
    "selectFloor(u.parkingLevel || 'bm1');\n        if (parkingHighlightMesh) {\n          parkingHighlightMesh.visible = true;\n          parkingHighlightMesh.position.set(u.parkingX, (u.parkingZ || -3.0) + 0.75, u.parkingY);\n        }\n        camState.target.set(u.parkingX, u.parkingZ || -3.0, u.parkingY);"
)

# 10. Update text & UI references from Kitroni 37-39 to Moshe Sharett 26-28
replacements = [
    ("קיטרוני 37–39, פתח תקוה", "משה שרת 26–28, פתח תקווה"),
    ("קיטרוני 37–39, פתח תקווה", "משה שרת 26–28, פתח תקווה"),
    ("קיטרוני 37–39", "משה שרת 26–28"),
    ("קיטרוני 37-39", "משה שרת 26-28"),
    ("קבוצת קולסקי · משה שרת 26–28, פתח תקווה", "משה שרת 26–28, פתח תקווה · מודל BIM אדריכלי 1:100"),
    ("יצחק קולסקי חברה לבניה והשקעות בע\"מ", "פרויקט משה שרת 26–28 פתח תקווה (א.ב. שרת בע\"מ)"),
    ("אילת קורן אדריכלים · פורטל שיווק ומכירות 3D (63 דירות)", "א.ל.ר אדריכלים · 66 יח\"ד + 70 חניות ב-2 מרתפים"),
    ("אילת קורן אדריכלים", "א.ל.ר אדריכלים בע\"מ"),
    ("גוש 6375 חלקות 237–238", "גוש 6372 חלקה 1025 (מגרש 1025 — 1,497 מ\"ר)"),
    ("K37-39", "MS26-28"),
    ("kitroni37_39_spatial_map.html", "sharett26_28_spatial_map.html"),
    ("kitroni37_39_model.obj", "sharett26_28_model.obj"),
    ("63 הדירות", "66 הדירות"),
    ("63 דירות", "66 דירות"),
    ("(63)", "(66)"),
    ("63 חניות", "70 חניות (מרתפים -1 ו--2)"),
    ("🏢 בניין 37 / בניין 39", "🏢 בניין 28 (מערב) / בניין 26 (מזרח)"),
    ("30 / 33 דירות", "33 / 33 דירות"),
    ("41 דירות", "35 דירות"),
    ("22 דירות", "31 דירות"),
    ("(41)", "(35)"),
    ("(22)", "(31)"),
    ('data-ubldg="37" class="unit-bldg-chip ui-btn" style="padding:3px 8px;font-size:10px;">בניין 37 — צפוני (30)', 'data-ubldg="28" class="unit-bldg-chip ui-btn" style="padding:3px 8px;font-size:10px;">בניין 28 — מערבי (33)'),
    ('data-ubldg="39" class="unit-bldg-chip ui-btn" style="padding:3px 8px;font-size:10px;">בניין 39 — דרומי (33)', 'data-ubldg="26" class="unit-bldg-chip ui-btn" style="padding:3px 8px;font-size:10px;">בניין 26 — מזרחי (33)'),
    ("startPresetInteriorTour(37, 4, 'NW')", "startPresetInteriorTour(28, 4, 'NW')"),
    ("startPresetInteriorTour(37, 4, 'E')",  "startPresetInteriorTour(28, 4, 'SW')"),
    ("startPresetInteriorTour(37, 5, 'NE')", "startPresetInteriorTour(28, 5, 'NE')"),
    ("startPresetInteriorTour(37, 5, 'SE')", "startPresetInteriorTour(28, 5, 'SE')"),
    ("startPresetInteriorTour(37, 8, 'E')",  "startPresetInteriorTour(28, 8, 'NW')"),
    ("startPresetInteriorTour(37, 9, 'W')",  "startPresetInteriorTour(28, 8, 'PH')"),
    ("startPresetInteriorTour(39, 4, 'NW')", "startPresetInteriorTour(26, 4, 'NW')"),
    ("startPresetInteriorTour(39, 5, 'SW')", "startPresetInteriorTour(26, 5, 'SW')"),
    ("startPresetInteriorTour(39, 5, 'SE')", "startPresetInteriorTour(26, 5, 'SE')"),
    ("startPresetInteriorTour(39, 9, 'E')",  "startPresetInteriorTour(26, 8, 'PH')"),
    ("בניין 37 (צפוני)", "בניין 28 (מערבי)"),
    ("בניין 39 (דרומי)", "בניין 26 (מזרחי)"),
    ("ב'37", "ב'28"),
    ("ב'39", "ב'26"),
    ("בניין 37:", "בניין 28:"),
    ("בניין 39:", "בניין 26:"),
    ("currentFloorId === 'mar'", "(currentFloorId === 'bm1' || currentFloorId === 'bm2')"),
    ("currentFloorId !== 'mar'", "(currentFloorId !== 'bm1' && currentFloorId !== 'bm2')"),
    ("floorId !== 'mar'", "(floorId !== 'bm1' && floorId !== 'bm2')"),
    ('min="-3.85" max="36.0"', 'min="-6.5" max="36.0"'),
    ('<span>-3.85</span>', '<span>-6.00</span>'),
    ("target: [2.5, 14.0, -8.5]", "target: [0.0, 14.0, 0.0]"),
    ("target: [0.2, 6.0, -9.2]",  "target: [0.0, 6.0, 0.0]"),
    ("target: [0.2, 8.0, -9.2]",  "target: [0.0, 8.0, 0.0]"),
    ("target: [2.5, 13.5, -8.5]", "target: [0.0, 13.5, 0.0]"),
    ("new THREE.Vector3(0.2, 8.0, -9.2)", "new THREE.Vector3(0.0, 8.0, 0.0)"),
    ("camState.target.set(2.5, fObj.zFloor + 1.0, -8.5);", "camState.target.set(0.0, fObj.zFloor + 1.0, 0.0);"),
    ("camState.target.set(2.5, activeF ? activeF.zFloor + 1.2 : 12.0, -8.5);", "camState.target.set(0.0, activeF ? activeF.zFloor + 1.2 : 12.0, 0.0);"),
    ("camState.target.set(2.5, Math.max(-2, f.zFloor), -8.5);", "camState.target.set(0.0, Math.max(-6, f.zFloor), 0.0);"),
]

for old_s, new_s in replacements:
    tmpl = tmpl.replace(old_s, new_s)

html_out = (
    tmpl
    .replace("__THREE_JS_CODE__", three_js_code)
    .replace("__PLANS_JSON__", plans_json_str)
    .replace("__CRM_JSON__", crm_json_str)
    .replace("__SPATIAL_POIS_JSON__", spatial_pois_json)
    .replace("__WIDE_GMAPS_URI__", wide_gmaps_data_uri)
    .replace("__INNER_GMAPS_URI__", inner_gmaps_data_uri)
    .replace("__CLOSEUP_GMAPS_URI__", closeup_gmaps_data_uri)
    .replace("__OUTER_SPAN_M__", str(outer_span_m))
    .replace("__INNER_SPAN_M__", str(inner_span_m))
    .replace("__CLOSEUP_SPAN_M__", str(closeup_span_m))
)

for fname in ("sharett26_28_3d_bim_viewer.html", "sharett26_28_3d_model.html", "index.html"):
    out_p = os.path.join(WORKSPACE, fname)
    with open(out_p, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"Wrote {out_p} ({os.path.getsize(out_p)/(1024*1024):.2f} MB)")
