# -*- coding: utf-8 -*-
"""
Captures and freezes the exact baseline metrics (v1) of the Hafetz Haim 44 3D BIM model
(hafetz44_3d_model.html + data/hafetz44_extracted_plans.json) for deterministic comparison
against the upgraded ArchBIM-Engine v2.0 execution.
"""
import os
import json
import time
import subprocess
import tempfile
from shapely.geometry import Polygon, MultiPolygon, LineString, box
from shapely.ops import unary_union, polygonize

PROJECT_DIR = r"G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\חפץ חיים 44 פתח תקווה"
DATA_DIR = os.path.join(PROJECT_DIR, "data")
BENCH_DIR = os.path.join(PROJECT_DIR, "src", "benchmark_v2")
os.makedirs(BENCH_DIR, exist_ok=True)

V1_HTML_PATH = os.path.join(PROJECT_DIR, "hafetz44_3d_model.html")
V1_PLANS_PATH = os.path.join(DATA_DIR, "hafetz44_extracted_plans.json")
V1_CRM_PATH = os.path.join(DATA_DIR, "hafetz44_units_crm.json")
BASELINE_OUT_PATH = os.path.join(BENCH_DIR, "v1_baseline_metrics.json")


def inspect_html_in_headless_node(html_path):
    """Runs the standalone Three.js HTML viewer inside a headless Node VM context and extracts exact scene metrics."""
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Extract all <script> blocks (excluding external src scripts)
    import re
    scripts = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", html, re.IGNORECASE)
    if len(scripts) < 2:
        raise RuntimeError(f"Expected at least 2 inline script blocks in {html_path}, found {len(scripts)}")

    three_js_code = scripts[0]
    app_js_code = scripts[1]

    harness_js = r"""
const { performance } = require('perf_hooks');
const vm = require('vm');
const fs = require('fs');

const threeCode = fs.readFileSync(process.argv[2], 'utf8');
const appCode = fs.readFileSync(process.argv[3], 'utf8');

function makeMockElement(tag) {
  return {
    tagName: (tag || 'DIV').toUpperCase(),
    style: {},
    classList: { add(){}, remove(){}, toggle(){}, contains(){ return false; } },
    dataset: {},
    children: [],
    appendChild(c) { this.children.push(c); return c; },
    removeChild() {},
    setAttribute(k, v) { this[k] = v; },
    getAttribute(k) { return this[k] || null; },
    addEventListener() {},
    removeEventListener() {},
    getBoundingClientRect() { return { left: 0, top: 0, width: 1920, height: 1080 }; },
    querySelector() { return makeMockElement('div'); },
    querySelectorAll() { return []; },
    getContext(type) {
      if (type === '2d') {
        return {
          fillStyle: '', strokeStyle: '', lineWidth: 1, font: '', textAlign: '', textBaseline: '',
          fillRect(){}, clearRect(){}, strokeRect(){}, beginPath(){}, moveTo(){}, lineTo(){},
          closePath(){}, stroke(){}, fill(){}, arc(){}, roundRect(){}, fillText(){},
          bezierCurveTo(){}, createLinearGradient(){ return { addColorStop(){} }; },
          createRadialGradient(){ return { addColorStop(){} }; },
          getImageData(){ return { data: new Uint8ClampedArray(4) }; },
          putImageData(){}
        };
      }
      // Mock WebGLRenderingContext for Three.js WebGLRenderer
      return null;
    },
    width: 512,
    height: 512,
     innerHTML: '',
    textContent: ''
  };
}

const elementsById = {};
const sandbox = {
  console,
  setTimeout: () => 1,
  clearTimeout: () => {},
  setInterval: () => 1,
  clearInterval: () => {},
  requestAnimationFrame: () => 1,
  cancelAnimationFrame: () => {},
  performance,
  Math,
  Date,
  JSON,
  Array, Object, String, Number, Boolean, RegExp, Map, Set, WeakMap, WeakSet, Promise,
  Float32Array, Float64Array, Int32Array, Int16Array, Int8Array, Uint32Array, Uint16Array, Uint8Array, Uint8ClampedArray, ArrayBuffer, DataView,
  window: null,
  document: {
    body: makeMockElement('body'),
    documentElement: makeMockElement('html'),
    getElementById(id) {
      if (!elementsById[id]) elementsById[id] = makeMockElement('div');
      return elementsById[id];
    },
    createElement(tag) { return makeMockElement(tag); },
    createElementNS(ns, tag) { return makeMockElement(tag); },
    querySelector() { return makeMockElement('div'); },
    querySelectorAll() { return []; },
    addEventListener() {}
  },
  innerWidth: 1920,
  innerHeight: 1080,
  devicePixelRatio: 2,
  addEventListener() {},
  removeEventListener() {},
  open() { return { document: { write(){}, close(){} }, focus(){}, print(){} }; },
  Image: function() { this.addEventListener = ()=>{}; }
};
sandbox.window = sandbox;
sandbox.self = sandbox;

vm.createContext(sandbox);
vm.runInContext(threeCode, sandbox);

// Replace THREE.WebGLRenderer with a lightweight instrumentation mock so scene construction runs at native speed
const overrideRendererCode = `
  THREE.WebGLRenderer = function(params) {
    this.domElement = (params && params.canvas) || document.createElement('canvas');
    this.shadowMap = { enabled: false, type: null };
    this.capabilities = { getMaxAnisotropy: function(){ return 16; } };
    this.localClippingEnabled = false;
    this.toneMapping = null;
    this.toneMappingExposure = 1.0;
    this.outputEncoding = null;
    this.renderCalls = 0;
    this.lastScene = null;
    this.lastCamera = null;
    this.setPixelRatio = function(){};
    this.setSize = function(){};
    this.render = function(sc, cam) {
      this.renderCalls++;
      this.lastScene = sc;
      this.lastCamera = cam;
    };
    this.dispose = function(){};
  };
  THREE.PMREMGenerator = function() {
    this.compileEquirectangularShader = function(){};
    this.fromEquirectangular = function(tex) { return { texture: tex, dispose: function(){} }; };
    this.fromScene = function(sc) { return { texture: new THREE.Texture(), dispose: function(){} }; };
    this.dispose = function(){};
  };
`;
vm.runInContext(overrideRendererCode, sandbox);

const t0 = performance.now();
let runtimeError = null;
try {
  vm.runInContext(appCode, sandbox);
} catch (err) {
  runtimeError = String(err && err.stack ? err.stack : err);
}
const t1 = performance.now();

const inspectCode = `
(function() {
  const safeGet = (fn, defVal) => { try { return fn(); } catch(e) { return defVal; } };
  const sc = safeGet(() => scene, null);
  if (!sc) return { error: 'scene undefined' };
  let totalMeshes = 0;
  let visibleMeshes = 0;
  let batchedMeshes = 0;
  let instancedMeshes = 0;
  let lineSegmentsCount = 0;
  let edgeLinesCount = 0;
  let totalVertices = 0;
  let totalTriangles = 0;
  let vertexAOMeshes = 0;
  let bumpMapMaterials = 0;
  const geoSet = new Set();
  const matSet = new Set();

  sc.traverse(obj => {
    if (obj.isMesh) {
      totalMeshes++;
      if (obj.visible) visibleMeshes++;
      if (obj.isInstancedMesh) instancedMeshes++;
      if (obj.userData && obj.userData.isBatchedFloorMesh) batchedMeshes++;
      if (obj.geometry) {
        geoSet.add(obj.geometry.uuid);
        const pos = obj.geometry.attributes && obj.geometry.attributes.position;
        if (pos) {
          totalVertices += pos.count;
          if (obj.geometry.index) {
            totalTriangles += Math.round(obj.geometry.index.count / 3);
          } else {
            totalTriangles += Math.round(pos.count / 3);
          }
        }
        if (obj.geometry.attributes && obj.geometry.attributes.color) {
          vertexAOMeshes++;
        }
      }
      const mats = Array.isArray(obj.material) ? obj.material : [obj.material];
      mats.forEach(m => {
        if (m) {
          matSet.add(m.uuid);
          if (m.bumpMap) bumpMapMaterials++;
        }
      });
    } else if (obj.isLineSegments) {
      lineSegmentsCount++;
      if (obj.userData && obj.userData.isSectionEdgeOutline) edgeLinesCount++;
    }
  });

  const flCount = safeGet(() => FLOORS.length, 0);
  const fgObj = safeGet(() => floorGroups, null);
  const fgKeys = fgObj ? Object.keys(fgObj) : [];
  const perFloorMeshes = {};
  if (fgObj) {
    for (const k of fgKeys) {
      let mc = 0;
      fgObj[k].traverse(o => { if (o.isMesh) mc++; });
      perFloorMeshes[k] = mc;
    }
  }

  return {
    floorsCount: flCount,
    floorGroupKeys: fgKeys,
    perFloorMeshes,
    totalMeshes,
    visibleMeshes,
    batchedMeshes,
    instancedMeshes,
    lineSegmentsCount,
    edgeLinesCount,
    activeDrawCallsFullBuilding: visibleMeshes + lineSegmentsCount,
    uniqueGeometries: geoSet.size,
    uniqueMaterials: matSet.size,
    totalVertices,
    totalTriangles,
    allBuildingMeshesLen: safeGet(() => allBuildingMeshes.length, 0),
    unitBadgesLen: safeGet(() => unitBadgeObjs.length, 0),
    parkingStallsLen: safeGet(() => PARKING_STALLS.length, 0),
    hasPMREMEnvMap: Boolean(sc.environment),
    vertexAOMeshes,
    bumpMapMaterials,
    hasSectionPocheCaps: Boolean(typeof window.__ARCH_BIM_V2_META__ !== 'undefined' && window.__ARCH_BIM_V2_META__.hasSectionPocheCaps),
    hasBaseboards: Boolean(typeof window.__ARCH_BIM_V2_META__ !== 'undefined' && window.__ARCH_BIM_V2_META__.hasBaseboards),
    v2Meta: (typeof window.__ARCH_BIM_V2_META__ !== 'undefined') ? window.__ARCH_BIM_V2_META__ : null
  };
})();
`;

const sceneMetrics = vm.runInContext(inspectCode, sandbox);
sceneMetrics.buildTimeMs = Number((t1 - t0).toFixed(2));
sceneMetrics.runtimeError = runtimeError;
console.log(JSON.stringify(sceneMetrics));
""".lstrip()

    with tempfile.TemporaryDirectory() as tmpdir:
        p_three = os.path.join(tmpdir, "three.js")
        p_app = os.path.join(tmpdir, "app.js")
        p_harn = os.path.join(tmpdir, "harness.js")
        with open(p_three, "w", encoding="utf-8") as f:
            f.write(three_js_code)
        with open(p_app, "w", encoding="utf-8") as f:
            f.write(app_js_code)
        with open(p_harn, "w", encoding="utf-8") as f:
            f.write(harness_js)

        proc = subprocess.run(
            ["node", p_harn, p_three, p_app],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30
        )
        if proc.returncode != 0:
            raise RuntimeError(f"Node harness failed: {proc.stderr}\n{proc.stdout}")
        lines = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip().startswith("{")]
        return json.loads(lines[-1])


def analyze_extracted_plans_json(plans_path):
    with open(plans_path, "r", encoding="utf-8") as f:
        plans = json.load(f)

    sheet_stats = {}
    total_wall_polys = 0
    total_openings = 0
    total_cad_lines = 0
    total_room_labels = 0
    total_room_cells = 0

    for sheet_name, sdata in plans.items():
        wps = sdata.get("wall_polys", [])
        ops = sdata.get("openings", [])
        cads = sdata.get("cad_lines", [])
        lbls = sdata.get("room_labels", [])
        rcells = sdata.get("room_cells", [])

        wall_area = 0.0
        for wp in wps:
            ext = wp.get("exterior", [])
            holes = wp.get("holes", [])
            if len(ext) >= 3:
                p = Polygon(ext, holes)
                if p.is_valid:
                    wall_area += p.area

        sheet_stats[sheet_name] = {
            "wall_poly_count": len(wps),
            "wall_area_sqm": round(wall_area, 3),
            "openings_count": len(ops),
            "cad_lines_count": len(cads),
            "room_labels_count": len(lbls),
            "room_cells_count": len(rcells),
            "has_auto_envelope": "auto_envelope_poly" in sdata,
            "envelope_iou": sdata.get("envelope_iou", None)
        }
        total_wall_polys += len(wps)
        total_openings += len(ops)
        total_cad_lines += len(cads)
        total_room_labels += len(lbls)
        total_room_cells += len(rcells)

    return {
        "sheets": sheet_stats,
        "total_wall_polys": total_wall_polys,
        "total_openings": total_openings,
        "total_cad_lines": total_cad_lines,
        "total_room_labels": total_room_labels,
        "total_room_cells": total_room_cells
    }


def main():
    print("Capturing v1 Baseline Metrics for Hafetz Haim 44...")
    scene_metrics = inspect_html_in_headless_node(V1_HTML_PATH)
    plans_metrics = analyze_extracted_plans_json(V1_PLANS_PATH)

    src_dir = os.path.join(PROJECT_DIR, "src")
    py_scripts = [fn for fn in os.listdir(src_dir) if fn.endswith(".py")]

    baseline = {
        "version": "v1_baseline",
        "project": "חפץ חיים 44, פתח תקווה",
        "captured_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "html_file": V1_HTML_PATH,
        "html_size_bytes": os.path.getsize(V1_HTML_PATH),
        "html_size_mb": round(os.path.getsize(V1_HTML_PATH) / (1024 * 1024), 3),
        "src_script_count": len(py_scripts),
        "scene_metrics": scene_metrics,
        "plans_metrics": plans_metrics,
        "architecture_audit": {
            "uses_manual_footprint_coords": True,
            "uses_manual_exterior_wall_thresholds": True,
            "uses_per_floor_geometry_batching": False,
            "uses_procedural_pmrem_hdri": False,
            "uses_baked_vertex_ao": False,
            "uses_section_poche_caps": False,
            "uses_7cm_interior_baseboards": False,
            "uses_automated_room_cell_graph": False
        }
    }

    with open(BASELINE_OUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(baseline, f, ensure_ascii=False, indent=2)

    print(f"Saved v1 baseline to {BASELINE_OUT_PATH}")
    print(f"  - HTML Size: {baseline['html_size_mb']} MB")
    print(f"  - Floors: {scene_metrics['floorsCount']} | Total Meshes: {scene_metrics['totalMeshes']} | Active Draw Calls: {scene_metrics['activeDrawCallsFullBuilding']}")
    print(f"  - Unique Geometries: {scene_metrics['uniqueGeometries']} | Unique Materials: {scene_metrics['uniqueMaterials']}")
    print(f"  - Total Vertices: {scene_metrics['totalVertices']} | Total Triangles: {scene_metrics['totalTriangles']}")
    print(f"  - Scene Build Time: {scene_metrics['buildTimeMs']} ms | Runtime Errors: {scene_metrics['runtimeError']}")


if __name__ == "__main__":
    main()
