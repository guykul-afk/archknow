// -*- coding: utf-8 -*-
/**
 * ArchiCheck AI — Universal 3D Planning Audit & Value Engineering Runtime Overlay
 * ===============================================================================
 * Zero-Rebuild Architecture:
 * Dynamically attaches to any existing Three.js BIM model served from:
 *   G:\Shared drives\שליטה ובקרה\מודלים פרויקטים
 * (e.g., hafetz44_3d_model.html) without modifying or rebuilding the base model.
 *
 * Capabilities:
 * 1. Renders all 20 Planning Audit, Value Engineering (VE), and Design Improvement
 *    findings directly in 3D space (1:1 metric CAD coordinates).
 * 2. Provides Interactive "Before (מצב קיים) ↔ After (מצב מוצע)" 3D geometric overlays
 *    for Hafetz Haim 44 (Basement 3-arm ramp headroom H_clear, 58m² shoring cut,
 *    Stall #16 relocation, Mamad drop-walls 3 storage rooms, West corridor 90->100cm,
 *    Walk-in closet cancellation, Penthouse 96->120cm island shift, Ground 32m² recess,
 *    and 4-Facade 524m² HPL vs. Plaster material breakdown).
 * 3. Bi-directional postMessage sync with ArchiCheck Web UI (2D Plan + Inspector Drawer).
 */

(function () {
  if (window.__ARCHICHECK_3D_OVERLAY_LOADED__) return;
  window.__ARCHICHECK_3D_OVERLAY_LOADED__ = true;

  const projectId = window.__ARCHICHECK_PROJECT_ID__ || 'hafetz44';
  const urlParams = new URLSearchParams(window.location.search);
  const isEmbedded = urlParams.get('embed') === '1' || window.self !== window.top;

  // Wait until Three.js scene and FLOORS are initialized in the host model
  function waitForHostScene(cb, retries = 40) {
    if (typeof THREE !== 'undefined' && typeof scene !== 'undefined' && typeof activeCam !== 'undefined') {
      cb();
    } else if (retries > 0) {
      setTimeout(() => waitForHostScene(cb, retries - 1), 100);
    }
  }

  waitForHostScene(initAudit3DOverlay);

  function initAudit3DOverlay() {
    // =========================================================================
    // 0. CLEAN ARCHITECTURAL PLANNING MODE (STRIP MARKETING / GIS / CATALOG)
    // =========================================================================
    function enforceCleanArchitecturalScene() {
      try {
        if (typeof gmapsVisible !== 'undefined') gmapsVisible = false;
        if (typeof gisMapPlanesGroup !== 'undefined' && gisMapPlanesGroup) {
          gisMapPlanesGroup.visible = false;
        }
        if (typeof gisRadiiVisible !== 'undefined') gisRadiiVisible = false;
        if (typeof gisRingsGroup !== 'undefined' && gisRingsGroup) {
          gisRingsGroup.visible = false;
        }
        if (typeof gisPoisVisible !== 'undefined') gisPoisVisible = false;
        if (typeof gisPoisGroup !== 'undefined' && gisPoisGroup) {
          gisPoisGroup.visible = false;
        }
        if (typeof units3DVisible !== 'undefined') units3DVisible = false;
        if (typeof units3DGroup !== 'undefined' && units3DGroup) {
          units3DGroup.visible = false;
        }
        if (typeof showLabels !== 'undefined') showLabels = false;
        if (typeof isNightMode !== 'undefined' && isNightMode && typeof nightLightsGroup !== 'undefined') {
          isNightMode = false;
          nightLightsGroup.visible = false;
        }
        if (typeof scene !== 'undefined' && scene && scene.background && typeof scene.background.setHex === 'function') {
          scene.background.setHex(0xeef2f6);
        }
      } catch (e) {}
    }

    enforceCleanArchitecturalScene();

    // Add a clean architectural studio metric CAD grid at ground level (y = -0.15)
    let archGroundGrid = null;
    try {
      archGroundGrid = new THREE.GridHelper(68, 68, 0x94a3b8, 0xdbe3ec);
      archGroundGrid.position.set(0.5, -0.15, 0.0);
      if (archGroundGrid.material) {
        archGroundGrid.material.transparent = true;
        archGroundGrid.material.opacity = 0.55;
      }
      scene.add(archGroundGrid);
    } catch (e) {}

    // Focus camera directly on the building in clean architectural view and sync WebGL canvas size
    if (typeof activatePreset === 'function') {
      try {
        activatePreset('iso_east');
        if (typeof camState !== 'undefined' && typeof updateCameraFromOrbit === 'function') {
          camState.spherical.radius = 44.0;
          camState.spherical.phi = 1.02;
          camState.target.set(0.5, 13.5, 0.0);
          updateCameraFromOrbit();
        }
      } catch (e) {}
    }
    enforceCleanArchitecturalScene();

    const triggerHostResize = () => {
      try { window.dispatchEvent(new Event('resize')); } catch (e) {}
    };
    triggerHostResize();
    setTimeout(triggerHostResize, 120);
    setTimeout(triggerHostResize, 450);
    if (typeof ResizeObserver !== 'undefined' && document.body) {
      const ro = new ResizeObserver(() => triggerHostResize());
      ro.observe(document.body);
    }

    // 1. Inject Styles for Clean Architectural Mode, 3D Audit Pins, HUD & Before/After Controls
    const styleEl = document.createElement('style');
    styleEl.textContent = `
      /* Hide all marketing, GIS, radii, POIs, and apartment sales catalog UI elements */
      #gis-labels-container,
      #gis-active-card,
      #units-labels-container,
      #unit-sales-card,
      #labels-container,
      #drawer-units,
      #drawer-apartments,
      #drawer-gis,
      #btn-top-gis-map,
      #btn-top-units-3d,
      #btn-top-radii,
      #btn-top-pois,
      #btn-top-night,
      #btn-gmaps,
      [data-drawer="drawer-units"],
      [data-drawer="drawer-apartments"],
      [data-drawer="drawer-gis"] {
        display: none !important;
      }

      /* Architectural Toolbar Buttons in .top-header */
      .arch-nav-btn {
        border: 1px solid #cbd5e1;
        background: #ffffff;
        color: #1e293b;
        border-radius: 7px;
        padding: 4px 9px;
        font-family: 'Heebo', system-ui, sans-serif;
        font-size: 11.5px;
        font-weight: 800;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        transition: all 0.14s ease;
        white-space: nowrap;
      }
      .arch-nav-btn:hover {
        background: #f1f5f9;
        border-color: #94a3b8;
      }
      .arch-nav-btn.active {
        background: #1e3a8a;
        color: #ffffff;
        border-color: #1d4ed8;
        box-shadow: 0 2px 6px rgba(30, 58, 138, 0.25);
      }
      .arch-nav-sep {
        width: 1px;
        height: 18px;
        background: #cbd5e1;
        margin: 0 2px;
      }

      #audit-3d-pins-container {
        position: absolute;
        inset: 0;
        pointer-events: none;
        overflow: hidden;
        z-index: 24;
      }
      .audit-3d-pin {
        position: absolute;
        transform: translate(-50%, -100%);
        pointer-events: auto;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 9px;
        border-radius: 999px;
        font-family: 'Heebo', system-ui, -apple-system, sans-serif;
        font-size: 11.5px;
        font-weight: 900;
        color: #ffffff;
        border: 2px solid #ffffff;
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.42);
        transition: transform 0.16s ease, box-shadow 0.16s ease, opacity 0.16s ease;
        white-space: nowrap;
        user-select: none;
      }
      .audit-3d-pin::after {
        content: '';
        position: absolute;
        bottom: -7px;
        left: 50%;
        transform: translateX(-50%);
        border-width: 7px 6px 0 6px;
        border-style: solid;
        border-color: #ffffff transparent transparent transparent;
      }
      .audit-3d-pin:hover {
        transform: translate(-50%, -108%) scale(1.12);
        z-index: 50 !important;
      }
      .audit-3d-pin.active-pin {
        transform: translate(-50%, -112%) scale(1.18);
        box-shadow: 0 0 0 3px #fde047, 0 10px 24px rgba(15, 23, 42, 0.65);
        z-index: 60 !important;
      }
      .audit-3d-pin.dimmed-pin {
        opacity: 0.45;
      }
      .audit-pin-FAIL { background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%); }
      .audit-pin-WARN { background: linear-gradient(135deg, #d97706 0%, #b45309 100%); }
      .audit-pin-PASS { background: linear-gradient(135deg, #16a34a 0%, #15803d 100%); }
      .audit-pin-VE   { background: linear-gradient(135deg, #059669 0%, #047857 100%); border-color: #fde047; }
      .audit-pin-IMP  { background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); }

      .audit-3d-label-tag {
        position: absolute;
        transform: translate(-50%, -50%);
        pointer-events: none;
        padding: 4px 10px;
        border-radius: 8px;
        font-family: 'Heebo', system-ui, sans-serif;
        font-size: 11px;
        font-weight: 800;
        color: #ffffff;
        background: rgba(15, 23, 42, 0.90);
        border: 1.5px solid #38bdf8;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
        white-space: nowrap;
        z-index: 23;
      }

      /* Floating ArchiCheck 3D Control Dock — hidden to prevent duplicate text box next to findings panel */
      #archicheck-3d-hud {
        display: none !important;
      }
      .ac3d-hdr {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
      }
      .ac3d-title {
        font-size: 12px;
        font-weight: 900;
        color: #fde047;
        display: flex;
        align-items: center;
        gap: 6px;
      }
      .ac3d-btn-row {
        display: flex;
        flex-wrap: wrap;
        gap: 4px;
      }
      .ac3d-chip {
        flex: 1;
        min-width: 54px;
        border: 1px solid #475569;
        background: #1e293b;
        color: #e2e8f0;
        border-radius: 7px;
        padding: 4px 6px;
        font-size: 10.5px;
        font-weight: 700;
        cursor: pointer;
        text-align: center;
        transition: all 0.14s ease;
      }
      .ac3d-chip:hover { background: #334155; }
      .ac3d-chip.active {
        background: #2563eb;
        border-color: #60a5fa;
        color: #ffffff;
      }
      .ac3d-ba-toggle {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 5px;
        background: #0f172a;
        padding: 4px;
        border-radius: 9px;
        border: 1px solid #334155;
      }
      .ac3d-ba-btn {
        border: none;
        border-radius: 6px;
        padding: 5px 7px;
        font-size: 11px;
        font-weight: 800;
        cursor: pointer;
        color: #94a3b8;
        background: transparent;
        transition: all 0.15s ease;
      }
      .ac3d-ba-btn.active-before {
        background: #dc2626;
        color: #ffffff;
        box-shadow: 0 2px 8px rgba(220, 38, 38, 0.4);
      }
      .ac3d-ba-btn.active-after {
        background: #059669;
        color: #ffffff;
        box-shadow: 0 2px 8px rgba(5, 150, 105, 0.45);
      }
      .ac3d-active-callout {
        background: rgba(30, 41, 59, 0.95);
        border: 1px solid #38bdf8;
        border-radius: 9px;
        padding: 7px 9px;
        font-size: 11px;
        line-height: 1.38;
      }
      .top-header {
        top: 8px !important;
        right: 10px !important;
        left: 10px !important;
        padding: 6px 12px !important;
        border-radius: 12px !important;
      }
      body.archicheck-embedded .bottom-right-sections {
        bottom: 10px;
        right: 10px;
        width: 265px;
        padding: 8px 10px;
      }
      body.archicheck-embedded #archicheck-3d-hud {
        top: 56px;
        left: 10px;
        width: 300px;
      }
    `;
    document.head.appendChild(styleEl);

    // Transform the Host Top Header & Settings Drawer into a Clean Architectural Planning Interface
    function adaptHostInterfaceForPlanningAnalysis() {
      // 1. Update header subtitle from marketing portal to architectural planning analysis
      const headerEl = document.querySelector('header.top-header');
      if (headerEl) {
        const badgeSpans = headerEl.querySelectorAll('span');
        badgeSpans.forEach((sp) => {
          if (sp.textContent && (sp.textContent.includes('שיווק') || sp.textContent.includes('דרגן'))) {
            sp.textContent = '📐 סביבת ניתוח אדריכלי, בקרת תכנון והנדסת ערך (BIM 1:50)';
            sp.style.background = '#eff6ff';
            sp.style.borderColor = '#93c5fd';
            sp.style.color = '#1e3a8a';
          }
        });
      }

      // 2. Clean up #drawer-settings (hide marketing finish packages, keep BIM layers & CAD controls)
      const drawerSettings = document.getElementById('drawer-settings');
      if (drawerSettings) {
        const titleSpan = drawerSettings.querySelector('.flex-between span');
        if (titleSpan) titleSpan.textContent = '🧱 שכבות BIM, שרטוט CAD והגדרות מודל תכנוני';
        const pkgButtons = document.getElementById('interior-pkg-buttons');
        if (pkgButtons) {
          const pkgBox = pkgButtons.closest('.section-box');
          if (pkgBox) pkgBox.style.display = 'none';
        }
      }

      // 3. Rebuild #view-buttons into a clean Architectural Planning & Floor Cut Bar
      const viewBtnsContainer = document.getElementById('view-buttons');
      const measureBtn = document.getElementById('btn-top-measure');
      const settingsBtn = document.querySelector('[data-drawer="drawer-settings"]');

      if (viewBtnsContainer) {
        // Keep measureBtn and settingsBtn in DOM but detach temporarily
        if (measureBtn) {
          measureBtn.className = 'arch-nav-btn';
          measureBtn.innerHTML = '📏 מדידה';
        }
        if (settingsBtn) {
          settingsBtn.className = 'arch-nav-btn';
          settingsBtn.innerHTML = '<span>🧱 שכבות BIM</span><span style="font-size:10px;">▾</span>';
        }

        // Hide all existing marketing buttons inside #view-buttons
        Array.from(viewBtnsContainer.children).forEach((ch) => {
          if (ch !== measureBtn && ch !== settingsBtn) {
            ch.style.display = 'none';
          }
        });

        // Create dedicated Architectural Planning Floor & Projection buttons
        const archButtons = [
          {
            id: 'arch-btn-all',
            label: '🏢 מבנה שלם',
            title: 'תצוגת מבנה שלם בתלת-ממד (איזומטריה)',
            active: true,
            onClick: () => {
              if (typeof selectFloor === 'function') selectFloor('all');
              if (typeof activatePreset === 'function') activatePreset('iso_east');
              if (typeof camState !== 'undefined' && typeof updateCameraFromOrbit === 'function') {
                camState.spherical.radius = 44.0;
                camState.spherical.phi = 1.02;
                camState.target.set(0.5, 13.5, 0.0);
                updateCameraFromOrbit();
              }
              enforceCleanArchitecturalScene();
              syncArchFloorBtns('all');
            }
          },
          {
            id: 'arch-btn-mar',
            label: '🅿️ מרתף (-5.10)',
            title: 'חתך קומת מרתף חניון, רמפה היקפית ודיפון',
            onClick: () => {
              if (typeof setOrthoMode === 'function') setOrthoMode(false);
              if (typeof setSliceMode === 'function') setSliceMode('single');
              if (typeof selectFloor === 'function') selectFloor('mar');
              if (typeof camState !== 'undefined' && typeof updateCameraFromOrbit === 'function') {
                camState.target.set(-2.0, -4.5, 1.5);
                camState.spherical.radius = 34.0;
                camState.spherical.phi = 0.52;
                camState.spherical.theta = 1.25;
                updateCameraFromOrbit();
              }
              renderBeforeAfterScene3D('basement_ve_full');
              enforceCleanArchitecturalScene();
              syncArchFloorBtns('mar');
              syncAuditVisibility();
            }
          },
          {
            id: 'arch-btn-kar',
            label: '🏛️ קרקע (±0.00)',
            title: 'חתך קומת קרקע, לובי, פיתוח מגרש וחניות עיליות',
            onClick: () => {
              if (typeof setOrthoMode === 'function') setOrthoMode(false);
              if (typeof setSliceMode === 'function') setSliceMode('single');
              if (typeof selectFloor === 'function') selectFloor('kar');
              if (typeof camState !== 'undefined' && typeof updateCameraFromOrbit === 'function') {
                camState.target.set(1.5, 0.5, 0.0);
                camState.spherical.radius = 34.0;
                camState.spherical.phi = 0.56;
                camState.spherical.theta = 1.22;
                updateCameraFromOrbit();
              }
              renderBeforeAfterScene3D('ground_contour_recess');
              enforceCleanArchitecturalScene();
              syncArchFloorBtns('kar');
              syncAuditVisibility();
            }
          },
          {
            id: 'arch-btn-f4',
            label: '📐 קומה טיפוסית (ק׳ 1–8)',
            title: 'חתך קומה טיפוסית (דירת 5 חד׳ מערבית + דירת 4 חד׳ מזרחית)',
            onClick: () => {
              if (typeof setOrthoMode === 'function') setOrthoMode(false);
              if (typeof setSliceMode === 'function') setSliceMode('single');
              if (typeof selectFloor === 'function') selectFloor('f4');
              if (typeof camState !== 'undefined' && typeof updateCameraFromOrbit === 'function') {
                camState.target.set(-1.0, 13.5, -0.5);
                camState.spherical.radius = 28.0;
                camState.spherical.phi = 0.50;
                camState.spherical.theta = 1.45;
                updateCameraFromOrbit();
              }
              renderBeforeAfterScene3D('west_corridor_fix');
              enforceCleanArchitecturalScene();
              syncArchFloorBtns('f4');
              syncAuditVisibility();
            }
          },
          {
            id: 'arch-btn-f9',
            label: '👑 פנטהאוז (ק׳ 9)',
            title: 'חתך קומת פנטהאוז ומרפסות גג (+28.70)',
            onClick: () => {
              if (typeof setOrthoMode === 'function') setOrthoMode(false);
              if (typeof setSliceMode === 'function') setSliceMode('single');
              if (typeof selectFloor === 'function') selectFloor('f9');
              if (typeof camState !== 'undefined' && typeof updateCameraFromOrbit === 'function') {
                camState.target.set(0.5, 29.2, 0.0);
                camState.spherical.radius = 28.0;
                camState.spherical.phi = 0.52;
                camState.spherical.theta = 1.35;
                updateCameraFromOrbit();
              }
              renderBeforeAfterScene3D('penthouse_island_fix');
              enforceCleanArchitecturalScene();
              syncArchFloorBtns('f9');
              syncAuditVisibility();
            }
          }
        ];

        const frag = document.createDocumentFragment();
        archButtons.forEach((cfg) => {
          const b = document.createElement('button');
          b.type = 'button';
          b.id = cfg.id;
          b.className = 'arch-nav-btn arch-floor-quick' + (cfg.active ? ' active' : '');
          b.title = cfg.title;
          b.textContent = cfg.label;
          b.addEventListener('click', cfg.onClick);
          frag.appendChild(b);
        });

        const sep1 = document.createElement('span');
        sep1.className = 'arch-nav-sep';
        frag.appendChild(sep1);

        // Top-Down 1:50 Orthographic Plan Button
        const orthoQuickBtn = document.createElement('button');
        orthoQuickBtn.type = 'button';
        orthoQuickBtn.id = 'arch-btn-ortho-top';
        orthoQuickBtn.className = 'arch-nav-btn';
        orthoQuickBtn.title = 'מעבר בין מבט-על אורתוגרפי דו-ממדי (1:50) לבין מבט תלת-ממדי (פרספקטיבה)';
        orthoQuickBtn.textContent = '📐 היטל 1:50';
        orthoQuickBtn.addEventListener('click', () => {
          if (typeof isOrtho !== 'undefined' && typeof setOrthoMode === 'function') {
            const nextOrtho = !isOrtho;
            if (nextOrtho) {
              if (typeof currentFloorId !== 'undefined' && currentFloorId === 'all') {
                if (typeof setSliceMode === 'function') setSliceMode('single');
                if (typeof selectFloor === 'function') selectFloor('f4');
                syncArchFloorBtns('f4');
              }
              if (typeof camState !== 'undefined' && typeof updateCameraFromOrbit === 'function') {
                camState.spherical.theta = -Math.PI / 2;
                camState.spherical.phi = 0.03;
                camState.spherical.radius = 32.0;
                updateCameraFromOrbit();
              }
              setOrthoMode(true);
            } else {
              setOrthoMode(false);
              if (typeof camState !== 'undefined' && typeof updateCameraFromOrbit === 'function') {
                camState.spherical.phi = 0.56;
                camState.spherical.theta = 1.25;
                updateCameraFromOrbit();
              }
            }
            orthoQuickBtn.classList.toggle('active', nextOrtho);
          }
        });
        frag.appendChild(orthoQuickBtn);

        // Toggle 3D Furniture Button (so architect can inspect bare CAD walls vs furnished rooms)
        let furnVis = true;
        const furnQuickBtn = document.createElement('button');
        furnQuickBtn.type = 'button';
        furnQuickBtn.id = 'arch-btn-furn';
        furnQuickBtn.className = 'arch-nav-btn active';
        furnQuickBtn.title = 'הצג/הסתר ריהוט פנים תלת-ממדי לצפייה נקייה בקירות ובשרטוט ה-CAD';
        furnQuickBtn.textContent = '🛋️ ריהוט 3D';
        furnQuickBtn.addEventListener('click', () => {
          furnVis = !furnVis;
          if (typeof toggleLayer === 'function') toggleLayer('furn3d', furnVis);
          furnQuickBtn.classList.toggle('active', furnVis);
        });
        frag.appendChild(furnQuickBtn);

        // Compact Before/After Toggle Button in Top Bar (replaces floating left HUD box)
        const baQuickBtn = document.createElement('button');
        baQuickBtn.type = 'button';
        baQuickBtn.id = 'arch-btn-ba-mode';
        baQuickBtn.className = 'arch-nav-btn active';
        baQuickBtn.style.background = '#059669';
        baQuickBtn.style.borderColor = '#047857';
        baQuickBtn.style.color = '#ffffff';
        baQuickBtn.title = 'החלף בין מצב מוצע (VE + תיקון) לבין מצב קיים בתכנית';
        baQuickBtn.textContent = '🟢 מצב מוצע (VE)';
        baQuickBtn.addEventListener('click', () => {
          const nextMode = !isProposedMode;
          setBeforeAfterMode(nextMode);
          baQuickBtn.textContent = nextMode ? '🟢 מצב מוצע (VE)' : '🔴 מצב קיים';
          baQuickBtn.style.background = nextMode ? '#059669' : '#dc2626';
          baQuickBtn.style.borderColor = nextMode ? '#047857' : '#b91c1c';
        });
        frag.appendChild(baQuickBtn);

        viewBtnsContainer.insertBefore(frag, viewBtnsContainer.firstChild);
      }
    }

    function syncArchFloorBtns(floorId) {
      const mapId = {
        all: 'arch-btn-all',
        mar: 'arch-btn-mar',
        kar: 'arch-btn-kar',
        f1: 'arch-btn-f4', f2: 'arch-btn-f4', f3: 'arch-btn-f4', f4: 'arch-btn-f4',
        f5: 'arch-btn-f4', f6: 'arch-btn-f4', f7: 'arch-btn-f4', f8: 'arch-btn-f4',
        f9: 'arch-btn-f9'
      };
      const targetBtnId = mapId[floorId] || '';
      document.querySelectorAll('.arch-floor-quick').forEach((b) => {
        b.classList.toggle('active', b.id === targetBtnId);
      });
      if (archGroundGrid) {
        archGroundGrid.visible = (floorId !== 'mar');
      }
    }

    adaptHostInterfaceForPlanningAnalysis();

    if (isEmbedded) {
      document.body.classList.add('archicheck-embedded');
      // Collapse sections panel by default in embedded mode so maximum 3D model is visible
      const secPanel = document.getElementById('sections-panel');
      const secBtn = document.getElementById('btn-toggle-sections-body');
      if (secPanel && !secPanel.classList.contains('collapsed')) {
        secPanel.classList.add('collapsed');
        if (secBtn) secBtn.textContent = '+ פתח חתכים';
      }
    }

    // 2. Create DOM Containers for 3D Pins & ArchiCheck 3D HUD
    const vpContainer = document.getElementById('viewport-container') || document.body;
    const pinsContainer = document.createElement('div');
    pinsContainer.id = 'audit-3d-pins-container';
    vpContainer.appendChild(pinsContainer);

    const hudEl = document.createElement('div');
    hudEl.id = 'archicheck-3d-hud';
    hudEl.innerHTML = `
      <div class="ac3d-hdr">
        <div class="ac3d-title">
          <span>🎯 שכבת בקרת תכנון ו-VE בתלת-ממד</span>
        </div>
        <div style="display:flex;gap:4px;">
          <button id="ac3d-btn-toggle-pins" class="ac3d-chip active" style="flex:0;min-width:auto;padding:3px 8px;" title="הצג/הסתר סיכות 3D">📌 פעיל</button>
          <button id="ac3d-btn-min" class="ac3d-chip" style="flex:0;min-width:auto;padding:3px 7px;" title="מזער חלונית">▾</button>
        </div>
      </div>
      <div class="hud-body-content" style="display:flex;flex-direction:column;gap:7px;">
        <div class="ac3d-ba-toggle" title="החלף בין המצב הקיים בתכנית לבין המצב המוצע (הזזת קירות/דיפון ב-3D)">
          <button type="button" id="ac3d-mode-before" class="ac3d-ba-btn">🔴 מצב קיים (תכנית)</button>
          <button type="button" id="ac3d-mode-after" class="ac3d-ba-btn active-after">🟢 מצב מוצע (VE + תיקון)</button>
        </div>
        <div class="ac3d-btn-row" id="ac3d-filter-row">
          <button type="button" class="ac3d-chip active" data-acfilter="ALL">הכל</button>
          <button type="button" class="ac3d-chip" data-acfilter="ISSUES">ליקויים</button>
          <button type="button" class="ac3d-chip" data-acfilter="VE">חיסכון VE</button>
          <button type="button" class="ac3d-chip" data-acfilter="FAC">חזיתות HPL</button>
          <button type="button" class="ac3d-chip" data-acfilter="BSM">מרתף ורמפה</button>
        </div>
        <div id="ac3d-active-callout" class="ac3d-active-callout">
          <div style="font-weight:800;color:#fde047;margin-bottom:2px;">בחר סיכה במודל או ממצא ברשימה</div>
          <div style="color:#cbd5e1;font-size:11px;">המודל יחתוך אוטומטית לקומה הרלוונטית ויציג את נפח הבדיקה והשינוי המוצע בתלת-ממד.</div>
        </div>
        <div id="ac3d-model-sync-bar" style="display:flex;align-items:center;justify-content:space-between;gap:6px;padding:5px 8px;border-radius:7px;background:rgba(15,23,42,0.88);border:1px solid #334155;font-size:10.5px;color:#cbd5e1;">
          <span id="ac3d-sync-status-lbl" style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">🧊 מודל 3D בסיסי מנוטר...</span>
          <button type="button" id="ac3d-btn-reaudit" class="ac3d-chip" style="flex:0;min-width:auto;padding:2px 7px;border-color:#38bdf8;color:#38bdf8;" title="בדוק אם מודל ה-3D הבסיסי שונה והרץ בדיקה תכנונית מלאה חדשה">🔄 בדוק/בקר</button>
        </div>
      </div>
    `;
    vpContainer.appendChild(hudEl);

    // 3. Three.js Groups for Audit Volumes & Before/After Engineering Geometry
    const clipPlanesRef = (typeof clippingPlanes !== 'undefined') ? clippingPlanes : [];
    const audit3DGroup = new THREE.Group();
    audit3DGroup.name = 'archicheck_audit_3d_group';
    scene.add(audit3DGroup);

    const beforeAfterGroup = new THREE.Group();
    beforeAfterGroup.name = 'archicheck_before_after_3d_group';
    scene.add(beforeAfterGroup);

    const facadeCladdingGroup = new THREE.Group();
    facadeCladdingGroup.name = 'archicheck_facade_cladding_3d_group';
    facadeCladdingGroup.visible = false;
    scene.add(facadeCladdingGroup);

    let projectData = null;
    let auditPinsVisible = true;
    let auditFilter = 'ALL';
    let activeAuditNoteId = null;
    let isProposedMode = true; // true = After (Proposed VE/Fix), false = Before (As-Designed)
    const auditPinItems = []; // { note, pinEl, volumeMesh, wireMesh, extraMeshes, pos3D, floorId }
    const dynamic3DLabels = []; // { pos: Vector3, el: HTMLElement, floorId: string }

    function clearDynamic3DLabels() {
      while (dynamic3DLabels.length > 0) {
        const item = dynamic3DLabels.pop();
        if (item.el && item.el.parentNode) item.el.parentNode.removeChild(item.el);
      }
    }

    function addDynamic3DLabel(x, yElev, z, text, borderColor = '#38bdf8', bg = 'rgba(15, 23, 42, 0.90)') {
      const el = document.createElement('div');
      el.className = 'audit-3d-label-tag';
      el.style.borderColor = borderColor;
      el.style.background = bg;
      el.innerHTML = text;
      pinsContainer.appendChild(el);
      dynamic3DLabels.push({ pos: new THREE.Vector3(x, yElev, z), el });
    }

    function makeOverlayBox(x0, y0, x1, y1, z0, z1, hexColor, opacity = 0.28, wireHex = null) {
      const w = Math.abs(x1 - x0);
      const d = Math.abs(y1 - y0);
      const h = Math.abs(z1 - z0);
      const grp = new THREE.Group();
      if (w < 0.01 || d < 0.01 || h < 0.01) return grp;

      const geo = new THREE.BoxGeometry(w, h, d);
      const mat = new THREE.MeshStandardMaterial({
        color: hexColor,
        emissive: hexColor,
        emissiveIntensity: 0.22,
        transparent: true,
        opacity: opacity,
        roughness: 0.35,
        depthWrite: false,
        side: THREE.DoubleSide,
        clippingPlanes: clipPlanesRef,
      });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(0.5 * (x0 + x1), 0.5 * (z0 + z1), 0.5 * (y0 + y1));
      grp.add(mesh);

      const edges = new THREE.EdgesGeometry(geo);
      const lineMat = new THREE.LineBasicMaterial({
        color: wireHex !== null ? wireHex : hexColor,
        transparent: true,
        opacity: Math.min(1.0, opacity + 0.55),
        clippingPlanes: clipPlanesRef,
      });
      const wire = new THREE.LineSegments(edges, lineMat);
      wire.position.copy(mesh.position);
      grp.add(wire);

      grp.userData = { mesh, wire, baseOpacity: opacity, baseColor: hexColor };
      return grp;
    }

    function make3DArrow(fromX, fromY, fromZ, toX, toY, toZ, hexColor = 0x10b981) {
      const p1 = new THREE.Vector3(fromX, fromZ, fromY);
      const p2 = new THREE.Vector3(toX, toZ, toY);
      const dir = new THREE.Vector3().subVectors(p2, p1);
      const len = dir.length();
      if (len < 0.05) return new THREE.Group();
      dir.normalize();
      const arrow = new THREE.ArrowHelper(dir, p1, len, hexColor, Math.min(0.65, len * 0.32), Math.min(0.42, len * 0.22));
      return arrow;
    }

    // =========================================================================
    // 4. HAFETZ HAIM 44 — 3D FACADE CLADDING LAYER (524m² HPL vs. 1,048m² PLASTER)
    // =========================================================================
    function buildHafetz44FacadeCladdingLayer() {
      while (facadeCladdingGroup.children.length > 0) {
        facadeCladdingGroup.remove(facadeCladdingGroup.children[0]);
      }
      if (projectId !== 'hafetz44') return;

      // 1. East Street Facade HPL Piers (88 sqm — PRESERVED on Hafetz Haim St, Gold/Emerald)
      [[-4.95, -3.85], [-0.45, 0.55], [3.15, 4.15]].forEach(([y0, y1]) => {
        facadeCladdingGroup.add(makeOverlayBox(16.20, y0, 16.45, y1, 3.50, 28.70, 0x10b981, 0.52, 0xfde047));
      });
      // 2. West Rear Facade HPL Piers (86 sqm — CONVERT TO PLASTER, Saving 34,400 ILS, Cyan/Orange)
      [[-4.95, -3.85], [-0.45, 0.55], [3.15, 4.15]].forEach(([y0, y1]) => {
        facadeCladdingGroup.add(makeOverlayBox(-15.45, y0, -15.20, y1, 3.50, 28.70, 0xf97316, 0.52, 0x38bdf8));
      });
      // 3. North Side Facade Vertical Window Framing HPL Bands (166 sqm — Saving 66,400 ILS)
      [[-12.6, -11.4], [-9.2, -8.0], [-5.8, -4.6], [6.2, 7.4], [9.6, 10.8], [12.4, 13.6]].forEach(([x0, x1]) => {
        facadeCladdingGroup.add(makeOverlayBox(x0, -5.32, x1, -5.08, 3.50, 31.50, 0xf97316, 0.46, 0x38bdf8));
      });
      // 4. South Side Facade Window Bands & Core Accent (184 sqm — Saving 73,600 ILS)
      [[-12.2, -10.4], [-6.2, -4.4], [-1.8, 2.2], [6.4, 8.2], [11.2, 13.0]].forEach(([x0, x1]) => {
        const yFace = (x0 >= -2.5 && x1 <= 3.0) ? 5.20 : 4.22;
        facadeCladdingGroup.add(makeOverlayBox(x0, yFace - 0.12, x1, yFace + 0.14, 3.50, 31.50, 0xf97316, 0.46, 0x38bdf8));
      });
    }

    // =========================================================================
    // 5. HAFETZ HAIM 44 — INTERACTIVE BEFORE / AFTER 3D ENGINEERING SCENES
    // =========================================================================
    function renderBeforeAfterScene3D(sceneKey) {
      while (beforeAfterGroup.children.length > 0) {
        beforeAfterGroup.remove(beforeAfterGroup.children[0]);
      }
      clearDynamic3DLabels();
      facadeCladdingGroup.visible = false;

      if (projectId !== 'hafetz44' || !sceneKey) return;

      // -----------------------------------------------------------------------
      // SCENE A: BASEMENT 3-ARM RAMP, UNDER-RAMP PUMPS, -58m² SHORING & STALL #16
      // -----------------------------------------------------------------------
      if (sceneKey === 'basement_ve_full') {
        // 1. 3-Arm Sloped Perimeter Ramp Visualization (Protected Trajectory)
        // South Upper Ramp Arm descending West->East (H_clear = 2.15m..3.55m beneath it!)
        const rampSouth = makeOverlayBox(-11.90, 5.45, 13.50, 8.60, -2.10, -1.75, 0x64748b, 0.30, 0x94a3b8);
        rampSouth.rotation.z = -0.095; // ~10-15% slope descending Eastward
        beforeAfterGroup.add(rampSouth);
        addDynamic3DLabel(1.0, -1.20, 7.0, '🛣️ זרוע דרומית עליונה של הרמפה (שיפוע 10%–15%) · מוגנת ב-100%', '#94a3b8');

        // 2. Mamad Drop-Walls in Central Core Island (H44-LOCKED-CORE1: 12 sqm -> 3 Tenant Storages)
        beforeAfterGroup.add(makeOverlayBox(-5.50, -4.33, -1.05, -0.33, -5.08, -2.25, 0x0284c7, 0.34, 0x38bdf8));
        if (isProposedMode) {
          // Divide into 3 Tenant Storage Units (4 sqm each)
          [-4.02, -2.54].forEach(divX => {
            beforeAfterGroup.add(makeOverlayBox(divX - 0.06, -4.33, divX + 0.06, -0.33, -5.08, -2.30, 0x38bdf8, 0.75, 0xffffff));
          });
          addDynamic3DLabel(-3.25, -2.05, -2.33, '🔄 ליבה כלואה בקירות ממ״ד יורדים: 3 מחסני דיירים (4 מ״ר × 3 = ~180,000 ₪)', '#38bdf8', 'rgba(3, 105, 161, 0.92)');
        } else {
          addDynamic3DLabel(-3.25, -2.05, -2.33, '📍 מצב קיים: תאי משאבות כלואים בקירות ממ״ד יורדים (12 מ״ר)', '#f59e0b');
        }

        if (!isProposedMode) {
          // BEFORE MODE: Original SW Shoring Pocket (48 sqm) + West Strip (10 sqm) + Old Stall #16
          beforeAfterGroup.add(makeOverlayBox(-17.72, 5.90, -2.22, 9.05, -5.08, -2.25, 0xdc2626, 0.38, 0xfca5a5));
          beforeAfterGroup.add(makeOverlayBox(-17.72, -9.05, -17.17, 5.90, -5.08, -2.25, 0xdc2626, 0.38, 0xfca5a5));
          // Old Stall #16 in SW corner
          beforeAfterGroup.add(makeOverlayBox(-16.80, 3.80, -14.15, 8.80, -5.05, -4.20, 0xf59e0b, 0.55, 0xfde047));
          addDynamic3DLabel(-10.0, -1.90, 7.50, '🔴 מצב קיים: כיס דיפון דרום-מערבי (48 מ״ר) + רצועה מערבית (10 מ״ר) + חניה #16', '#f87171', 'rgba(153, 27, 27, 0.92)');
        } else {
          // AFTER (PROPOSED VE) MODE:
          // A. Relocated Pump & Ventilation Rooms (32 sqm) under South Upper Ramp Soffit (H_clear >= 2.15m)
          beforeAfterGroup.add(makeOverlayBox(-11.50, 5.60, -1.50, 8.55, -5.08, -2.75, 0x10b981, 0.48, 0x6ee7b7));
          addDynamic3DLabel(-6.50, -3.20, 7.10, '🟢 חדרי משאבות ואוורור מתחת לרמפה העליונה (32 מ״ר · גובה ראש פנוי H=2.15–3.55m)', '#34d399', 'rgba(6, 95, 70, 0.94)');

          // B. Retracted Shoring Wall (-58 sqm = 203,000 ILS Verified Saving!)
          beforeAfterGroup.add(makeOverlayBox(-17.72, 5.90, -2.22, 9.05, -5.08, -2.25, 0x059669, 0.18, 0xfde047));
          // New Shoring Wall line at Y = +5.90
          beforeAfterGroup.add(makeOverlayBox(-17.17, 5.75, -2.22, 6.02, -5.08, -2.20, 0x10b981, 0.85, 0xffffff));
          beforeAfterGroup.add(make3DArrow(-10.0, 8.95, -3.5, -10.0, 6.05, -3.5, 0x10b981));
          beforeAfterGroup.add(make3DArrow(-14.5, 8.95, -3.5, -14.5, 6.05, -3.5, 0x10b981));
          addDynamic3DLabel(-11.50, -1.80, 7.80, '💰 קיצוץ 58 מ״ר קונטור דיפון וחפירה = חיסכון מאומת 203,000 ₪!', '#fde047', 'rgba(4, 120, 87, 0.95)');

          // C. Relocated Stall #16 (2.65 x 5.00m) on East face of Central Island facing 5.55m East Aisle
          beforeAfterGroup.add(makeOverlayBox(1.80, -4.80, 4.45, 0.20, -5.05, -3.60, 0x06b6d4, 0.62, 0x67e8f9));
          beforeAfterGroup.add(make3DArrow(-15.0, 6.20, -4.2, 3.10, -2.30, -4.2, 0x38bdf8));
          addDynamic3DLabel(3.15, -3.10, -2.30, '🚗 חניה #16 חלופית מאומתת (2.65×5.00 מ׳) בגישה ישירה ממיסעה 5.55 מ׳ (0 אובדן חניות)', '#67e8f9', 'rgba(14, 116, 144, 0.95)');
        }
      }

      // -----------------------------------------------------------------------
      // SCENE B: WEST APARTMENT CORRIDOR (100/105cm -> UNIFORM 105cm) & WALK-IN CLOSET (+2.6m²)
      // -----------------------------------------------------------------------
      else if (sceneKey === 'west_corridor_fix') {
        const zF = 12.95;
        if (!isProposedMode) {
          // BEFORE: 100/105cm Corridor (7.11m long) with 90cm door-frame pinch + Cramped 160x165cm Walk-In Closet Walls
          beforeAfterGroup.add(makeOverlayBox(-9.79, -1.38, -1.25, -0.33, zF + 0.03, zF + 2.45, 0xd97706, 0.42, 0xfde047));
          beforeAfterGroup.add(makeOverlayBox(-11.35, -4.95, -9.65, -3.38, zF + 0.03, zF + 2.45, 0xf59e0b, 0.42, 0xfde047));
          addDynamic3DLabel(-6.80, zF + 2.65, -0.85, '🟠 מצב קיים (WARN): רוחב מסדרון 100/105 ס״מ (תקין ≥100) לאורך 7.11 מ׳ + היצרות משקוף 90 ס״מ', '#fbbf24', 'rgba(146, 64, 14, 0.94)');
          addDynamic3DLabel(-10.50, zF + 2.65, -4.15, '🟠 חדר ארונות צפוף (160×165 ס״מ · מעבר 45 ס״מ בלבד)', '#fbbf24');
        } else {
          // AFTER: Uniform 105cm Corridor (shortened tail & aligned partition) + 3.80m Flush Wardrobe (+2.6 sqm)
          beforeAfterGroup.add(makeOverlayBox(-8.50, -1.38, -1.25, -0.33, zF + 0.03, zF + 2.45, 0x10b981, 0.45, 0x6ee7b7));
          // Aligned partition wall in glowing green
          beforeAfterGroup.add(makeOverlayBox(-8.50, -1.48, -1.25, -1.38, zF + 0.03, zF + 2.60, 0x059669, 0.85, 0xffffff));
          // New 3.80m Flush Wardrobe along North/East wall freeing +2.6 sqm
          beforeAfterGroup.add(makeOverlayBox(-11.40, -4.95, -9.60, -4.35, zF + 0.03, zF + 2.40, 0x0284c7, 0.72, 0x7dd3fc));
          addDynamic3DLabel(-6.80, zF + 2.75, -0.85, '🟢 מצב מוצע: יישור מסדרון ל-105 ס״מ אחיד וקיצור זנב המסדרון ב-1.30 מ׳', '#34d399', 'rgba(6, 95, 70, 0.94)');
          addDynamic3DLabel(-10.50, zF + 2.75, -4.45, '🛋️ ביטול קירות חדר ארונות ← ארון קיר 3.80 מ׳ (+2.6 מ״ר נטו לחדרים!)', '#38bdf8', 'rgba(3, 105, 161, 0.94)');
        }
      }

      // -----------------------------------------------------------------------
      // SCENE C: WEST MASTER SUITE (299cm WIDTH, 52cm CLEARANCE -> ROTATED BED + POCKET DOOR)
      // -----------------------------------------------------------------------
      else if (sceneKey === 'west_master_suite') {
        const zF = 12.95;
        if (!isProposedMode) {
          beforeAfterGroup.add(makeOverlayBox(-11.05, -2.65, -10.11, -0.95, zF + 0.03, zF + 1.20, 0xd97706, 0.52, 0xfde047));
          addDynamic3DLabel(-10.55, zF + 1.65, -1.80, '🟠 מצב קיים: מעבר 52 ס״מ בלבד בקצה המיטה + התנגשות דלת כנף בחדר רחצה', '#fbbf24');
        } else {
          // Proposed rotated bed on North/South 4.68m axis + Pocket Door
          beforeAfterGroup.add(makeOverlayBox(-12.55, -2.95, -10.95, -0.95, zF + 0.05, zF + 0.85, 0x10b981, 0.60, 0x6ee7b7));
          beforeAfterGroup.add(makeOverlayBox(-12.25, -3.52, -11.45, -3.38, zF + 0.05, zF + 2.15, 0x06b6d4, 0.85, 0xffffff));
          addDynamic3DLabel(-11.65, zF + 1.75, -1.95, '🟢 מצב מוצע: סיבוב מיטה לקיר 4.68 מ׳ (מעבר 110 ס״מ) + דלת כיס לחדר הרחצה', '#34d399', 'rgba(6, 95, 70, 0.94)');
        }
      }

      // -----------------------------------------------------------------------
      // SCENE D: EAST APARTMENT CORRIDOR 3-DOOR CLASH
      // -----------------------------------------------------------------------
      else if (sceneKey === 'east_corridor_doors') {
        const zF = 12.95;
        if (!isProposedMode) {
          beforeAfterGroup.add(makeOverlayBox(5.45, -1.55, 8.20, -0.35, zF + 0.03, zF + 2.20, 0xd97706, 0.45, 0xfde047));
          addDynamic3DLabel(6.85, zF + 2.45, -0.95, '🟠 מצב קיים: התנגשות 3 דלתות + דלת שירות חוסמת 50% מארון המסדרון', '#fbbf24');
        } else {
          beforeAfterGroup.add(makeOverlayBox(5.45, -1.55, 8.20, -0.35, zF + 0.03, zF + 2.20, 0x10b981, 0.40, 0x6ee7b7));
          addDynamic3DLabel(6.85, zF + 2.45, -0.95, '🟢 מצב מוצע: דלת הזזה/היפוך ציר בחדר שירות ← 100% נגישות לארון המסדרון', '#34d399', 'rgba(6, 95, 70, 0.94)');
        }
      }

      // -----------------------------------------------------------------------
      // SCENE E: PENTHOUSE FLOOR 9 (ISLAND 96cm -> 120cm & BEDROOMS 260cm -> 275cm)
      // -----------------------------------------------------------------------
      else if (sceneKey === 'penthouse_island_fix') {
        const zF = 28.70;
        if (!isProposedMode) {
          // 96cm gap between Island (Y=2.42) and South Counter (Y=3.38)
          beforeAfterGroup.add(makeOverlayBox(6.06, 2.42, 8.49, 3.38, zF + 0.03, zF + 1.10, 0xdc2626, 0.52, 0xfca5a5));
          addDynamic3DLabel(7.25, zF + 1.55, 2.90, '🔴 מצב קיים: מעבר 96 ס״מ בלבד בין אי המטבח לארונות (נדרש 110–120 ס״מ)', '#f87171', 'rgba(153, 27, 27, 0.94)');
        } else {
          // Shifted Island 24cm North (Y = 1.28..2.18) leaving 120cm green clearance (Y = 2.18..3.38)
          beforeAfterGroup.add(makeOverlayBox(6.06, 1.28, 8.49, 2.18, zF + 0.05, zF + 0.96, 0x059669, 0.72, 0xffffff));
          beforeAfterGroup.add(makeOverlayBox(6.06, 2.18, 8.49, 3.38, zF + 0.03, zF + 0.45, 0x10b981, 0.38, 0x6ee7b7));
          beforeAfterGroup.add(make3DArrow(7.25, 2.42, zF + 1.05, 7.25, 2.18, zF + 1.05, 0x10b981));
          addDynamic3DLabel(7.25, zF + 1.65, 2.40, '🟢 מצב מוצע: הזזת אי המטבח 24 ס״מ צפונה ← מעבר מרווח 120 ס״מ ✓', '#34d399', 'rgba(6, 95, 70, 0.94)');
        }
      }

      // -----------------------------------------------------------------------
      // SCENE F: GROUND FLOOR CONTOUR RECESS (-32m² = 198,400 ILS vs. 9m² LOCKED LOBBY)
      // -----------------------------------------------------------------------
      else if (sceneKey === 'ground_contour_recess') {
        const zF = 0.00;
        // 9.0 sqm Locked Lobby trapped under Floor 1 slab (Vertical Slab Lock)
        beforeAfterGroup.add(makeOverlayBox(-1.20, -1.80, 2.20, 0.80, zF + 0.05, zF + 3.10, 0x0284c7, 0.32, 0x38bdf8));
        addDynamic3DLabel(0.50, zF + 1.80, -0.50, '🔒 9.0 מ״ר לובי כלואים תחת תקרת קומה 1 (0 ₪ חיסכון שלד ← הרחבת מבואה)', '#38bdf8');

        if (!isProposedMode) {
          beforeAfterGroup.add(makeOverlayBox(1.50, -5.18, 7.80, -0.50, zF + 0.05, zF + 3.15, 0xdc2626, 0.40, 0xfca5a5));
          addDynamic3DLabel(4.65, zF + 2.40, -2.85, '🔴 מצב קיים: כפילות חדר עגלות (10.6 מ״ר) + חדר שירות (12.2 מ״ר) ובליטת מעטפת', '#f87171');
        } else {
          beforeAfterGroup.add(makeOverlayBox(1.50, -5.18, 7.80, -0.50, zF + 0.05, zF + 3.15, 0x10b981, 0.25, 0xfde047));
          // Retracted Ground Floor Exterior Wall
          beforeAfterGroup.add(makeOverlayBox(1.50, -2.20, 7.80, -1.95, zF + 0.05, zF + 3.15, 0x059669, 0.85, 0xffffff));
          beforeAfterGroup.add(make3DArrow(4.65, -5.10, zF + 1.5, 4.65, -2.25, zF + 1.5, 0x10b981));
          addDynamic3DLabel(4.65, zF + 2.50, -2.85, '💰 נסיגת מעטפת קומת קרקע (-32 מ״ר מאומתים) = חיסכון 198,400 ₪!', '#fde047', 'rgba(4, 120, 87, 0.95)');
        }
      }

      // -----------------------------------------------------------------------
      // SCENE G: TYPICAL FLOOR CORE TIGHTENING (-24m² = 148,800 ILS) & EAST FOYER (+1.5m²)
      // -----------------------------------------------------------------------
      else if (sceneKey === 'typical_core_tighten') {
        const zF = 12.95;
        beforeAfterGroup.add(makeOverlayBox(-2.20, -2.50, 1.80, 1.10, zF + 0.04, zF + 2.65, 0x8b5cf6, 0.38, 0xc4b5fd));
        beforeAfterGroup.add(makeOverlayBox(1.80, -0.45, 5.65, 1.55, zF + 0.04, zF + 2.65, 0x06b6d4, 0.45, 0x67e8f9));
        addDynamic3DLabel(-0.20, zF + 2.80, -0.70, '💰 הידוק גרעין ופירים: -3.0 מ״ר/קומה × 8 קומות = חיסכון 148,800 ₪', '#c4b5fd', 'rgba(91, 33, 182, 0.94)');
        addDynamic3DLabel(3.75, zF + 2.30, 0.55, '🛋️ סיפוח +1.5 מ״ר למבואת כניסה וארון מעילים בדירה המזרחית', '#67e8f9', 'rgba(14, 116, 144, 0.94)');
      }

      // -----------------------------------------------------------------------
      // SCENE H: FACADE CLADDING (524m² HPL vs. 1,048m² PLASTER = 174,400 ILS SAVING)
      // -----------------------------------------------------------------------
      else if (sceneKey.startsWith('facade_cladding_')) {
        facadeCladdingGroup.visible = true;
        if (sceneKey === 'facade_cladding_east') {
          addDynamic3DLabel(16.5, 18.5, 0.0, '🏛️ חזית רחוב מזרחית: שימור מלא של 88 מ״ר חיפוי HPL לבן בעמודוני המרפסות', '#fde047', 'rgba(6, 95, 70, 0.95)');
        } else if (sceneKey === 'facade_cladding_west') {
          addDynamic3DLabel(-15.5, 18.5, 0.0, '💰 חזית אחורית מערבית: המרת 86 מ״ר HPL לטיח אקרילי גמיש = חיסכון 34,400 ₪', '#38bdf8', 'rgba(154, 52, 18, 0.95)');
        } else if (sceneKey === 'facade_cladding_north') {
          addDynamic3DLabel(0.5, 18.5, -5.6, '💰 חזית צד צפונית: המרת 166 מ״ר רצועות HPL סביב חלונות = חיסכון 66,400 ₪', '#38bdf8', 'rgba(154, 52, 18, 0.95)');
        } else if (sceneKey === 'facade_cladding_south') {
          addDynamic3DLabel(0.5, 18.5, 5.6, '💰 חזית צד דרומית: המרת 184 מ״ר רצועות HPL = חיסכון 73,600 ₪ (סה״כ חזיתות: 174,400 ₪)', '#38bdf8', 'rgba(154, 52, 18, 0.95)');
        }
      }
    }

    // =========================================================================
    // 6. BUILD 20 3D PINS & VOLUMES FROM PROJECT JSON
    // =========================================================================
    function matchesAudit3DFilter(note) {
      if (auditFilter === 'ALL') return true;
      const s3d = note.spatial_3d || {};
      if (auditFilter === 'ISSUES') return (note.status === 'FAIL' || note.status === 'WARN') && !note.is_value_eng && !note.is_design_improvement;
      if (auditFilter === 'VE') return Boolean(note.is_value_eng || note.is_design_improvement);
      if (auditFilter === 'FAC') return note.ve_category === 'FAC';
      if (auditFilter === 'BSM') return s3d.floor_id === 'mar' || note.sheet_id.includes('basement');
      return true;
    }

    function getNoteHexAndClass(note) {
      if (note.is_value_eng) return { hex: 0x10b981, wire: 0xfde047, cls: 'audit-pin-VE', icon: '💰' };
      if (note.is_design_improvement) return { hex: 0x0284c7, wire: 0x38bdf8, cls: 'audit-pin-IMP', icon: '🛋️' };
      if (note.status === 'FAIL') return { hex: 0xdc2626, wire: 0xfca5a5, cls: 'audit-pin-FAIL', icon: '❌' };
      if (note.status === 'WARN') return { hex: 0xd97706, wire: 0xfde047, cls: 'audit-pin-WARN', icon: '⚠️' };
      return { hex: 0x16a34a, wire: 0x86efac, cls: 'audit-pin-PASS', icon: '✓' };
    }

    function buildAuditPinsAndVolumes(data) {
      projectData = data;
      while (audit3DGroup.children.length > 0) audit3DGroup.remove(audit3DGroup.children[0]);
      pinsContainer.innerHTML = '';
      auditPinItems.length = 0;

      buildHafetz44FacadeCladdingLayer();

      const notes = (data.notes || []).filter(
        (n) => !String(n.id || '').endsWith('-3D-SYNC') && !String(n.rule_id || '').includes('3D_BIM_FULL_AUDIT')
      );
      data.notes = notes;
      notes.forEach((note) => {
        const s3d = note.spatial_3d;
        if (!s3d || !s3d.bbox_3d) return;

        const [x0, y0, x1, y1, z0, z1] = s3d.bbox_3d;
        const styleMeta = getNoteHexAndClass(note);
        const baseOp = note.status === 'FAIL' ? 0.34 : (note.is_value_eng ? 0.24 : 0.16);
        const boxGrp = makeOverlayBox(x0, y0, x1, y1, z0, z1, styleMeta.hex, baseOp, styleMeta.wire);
        boxGrp.userData.note = note;
        audit3DGroup.add(boxGrp);

        const extraMeshes = [];
        (s3d.extra_boxes_3d || []).forEach((eb) => {
          const eg = makeOverlayBox(eb[0], eb[1], eb[2], eb[3], eb[4], eb[5], styleMeta.hex, baseOp * 0.85, styleMeta.wire);
          audit3DGroup.add(eg);
          extraMeshes.push(eg);
        });

        const [px, pyElev, pz] = s3d.pin_3d || [0.5 * (x0 + x1), z1 - 0.5, 0.5 * (y0 + y1)];
        const pinEl = document.createElement('div');
        pinEl.className = `audit-3d-pin ${styleMeta.cls}`;
        pinEl.dataset.noteId = note.id;

        const shortBadge = note.is_value_eng && note.ve_saving_ils > 0
          ? `#${note.pin_num} · ${(note.ve_saving_ils / 1000).toFixed(0)}K ₪`
          : `#${note.pin_num}`;
        pinEl.innerHTML = `<span>${styleMeta.icon}</span><span>${shortBadge}</span>`;
        pinEl.title = s3d.callout_he || `#${note.pin_num}: ${note.title}`;

        const pinItemObj = {
          note,
          s3d,
          pinEl,
          boxGrp,
          extraMeshes,
          pos3D: new THREE.Vector3(px, pyElev, pz),
          floorId: s3d.floor_id || 'all',
          isHovered: false,
        };

        pinEl.addEventListener('mouseenter', () => {
          pinItemObj.isHovered = true;
          syncAuditVisibility();
        });
        pinEl.addEventListener('mouseleave', () => {
          pinItemObj.isHovered = false;
          syncAuditVisibility();
        });
        pinEl.addEventListener('click', (e) => {
          e.stopPropagation();
          selectAuditNote3D(note.id, { flyTo: true, notifyParent: true });
        });

        pinsContainer.appendChild(pinEl);
        auditPinItems.push(pinItemObj);
      });

      syncAuditVisibility();
    }

    function syncAuditVisibility() {
      audit3DGroup.visible = auditPinsVisible;
      const hasActive = Boolean(activeAuditNoteId);
      const curFlr = (typeof currentFloorId !== 'undefined') ? currentFloorId : 'all';

      auditPinItems.forEach((item) => {
        const filterOk = matchesAudit3DFilter(item.note);
        const floorOk = (curFlr === 'all')
          ? true
          : (item.floorId === curFlr || (item.floorId === 'all' && auditFilter === 'FAC'));
        const isVis = auditPinsVisible && filterOk && floorOk;
        const isTarget = item.note.id === activeAuditNoteId;
        const showVolume = auditPinsVisible && (isTarget || item.isHovered || (auditFilter === 'FAC' && item.note.ve_category === 'FAC'));

        item.boxGrp.visible = showVolume;
        item.extraMeshes.forEach((em) => { em.visible = showVolume; });

        if (item.boxGrp.userData.mesh) {
          item.boxGrp.userData.mesh.material.opacity = isTarget
            ? 0.45
            : (item.isHovered ? 0.36 : item.boxGrp.userData.baseOpacity);
        }

        item.pinEl.classList.toggle('active-pin', isTarget);
        item.pinEl.classList.toggle('dimmed-pin', hasActive && !isTarget && !item.isHovered);
        item.pinEl.dataset.allowed = (isVis || isTarget) ? '1' : '0';
        if (!isVis && !isTarget) {
          item.pinEl.style.display = 'none';
        }
      });
    }

    // =========================================================================
    // 7. AUTO-SLICE FLOOR, CAMERA FLY-TO & BEFORE/AFTER TRIGGER ON NOTE SELECT
    // =========================================================================
    function selectAuditNote3D(noteId, opts = {}) {
      const item = auditPinItems.find((x) => x.note.id === noteId);
      if (!item) return;

      activeAuditNoteId = noteId;
      const { note, s3d } = item;

      // 1. Auto-slice the 3D building to the exact floor (mar, kar, f4, f9, or all for facades)
      if (opts.flyTo !== false) {
        if (typeof camState !== 'undefined' && camState.walkMode && typeof exitWalkthrough === 'function') {
          exitWalkthrough();
        }
        if (typeof setOrthoMode === 'function') {
          setOrthoMode(false);
          const orthoQuickBtn = document.getElementById('arch-btn-ortho-top');
          if (orthoQuickBtn) orthoQuickBtn.classList.remove('active');
        }

        const targetFloor = s3d.floor_id || 'f4';
        const targetSliceMode = s3d.slice_mode || (targetFloor === 'all' ? 'cumulative' : 'single');

        if (typeof setSliceMode === 'function') {
          setSliceMode(targetSliceMode);
        }
        if (typeof selectFloor === 'function') {
          selectFloor(targetFloor);
        }
        syncArchFloorBtns(targetFloor);
        enforceCleanArchitecturalScene();

        // 2. Smooth Camera Orbit Positioning
        if (s3d.camera && typeof camState !== 'undefined' && typeof updateCameraFromOrbit === 'function') {
          const [tx, ty, tz] = s3d.camera.target;
          camState.target.set(tx, ty, tz);
          camState.spherical.radius = s3d.camera.radius || 18.0;
          camState.spherical.phi = s3d.camera.phi || 0.54;
          camState.spherical.theta = s3d.camera.theta || 1.25;
          updateCameraFromOrbit();
        }
      }

      // 3. Render Before/After 3D Engineering Geometry for this note
      renderBeforeAfterScene3D(s3d.before_after_scene || null);

      // 4. Update HUD Callout Card
      const calloutEl = document.getElementById('ac3d-active-callout');
      if (calloutEl) {
        const modeBadge = isProposedMode
          ? '<span style="background:#059669;color:#fff;padding:1px 6px;border-radius:4px;font-size:10px;">מצב מוצע (VE/תיקון)</span>'
          : '<span style="background:#dc2626;color:#fff;padding:1px 6px;border-radius:4px;font-size:10px;">מצב קיים בתכנית</span>';
        calloutEl.innerHTML = `
          <div style="display:flex;align-items:center;justify-content:space-between;gap:6px;margin-bottom:4px;">
            <strong style="color:#fde047;font-size:12px;">ממצא #${note.pin_num} · ${note.room_name.replace('📍 ', '')}</strong>
            ${modeBadge}
          </div>
          <div style="color:#ffffff;font-weight:700;margin-bottom:3px;">${s3d.callout_he || note.title}</div>
          <div style="color:#93c5fd;font-size:10.5px;"><strong>קיים:</strong> ${note.measured} ⬅️ <strong>יעד:</strong> ${note.benchmark}</div>
        `;
      }

      syncAuditVisibility();

      // 5. Notify parent ArchiCheck Web UI if clicked inside the 3D model
      if (opts.notifyParent && window.parent && window.parent !== window) {
        window.parent.postMessage({
          type: 'ARCHICHECK_3D_PIN_CLICKED',
          noteId: note.id,
          sheetId: note.sheet_id,
        }, '*');
      }
    }

    // Wire HUD Controls
    const btnTogglePins = document.getElementById('ac3d-btn-toggle-pins');
    if (btnTogglePins) {
      btnTogglePins.addEventListener('click', () => {
        auditPinsVisible = !auditPinsVisible;
        btnTogglePins.classList.toggle('active', auditPinsVisible);
        btnTogglePins.textContent = auditPinsVisible ? '📌 פעיל' : '📌 מוסתר';
        if (!auditPinsVisible) {
          beforeAfterGroup.visible = false;
          facadeCladdingGroup.visible = false;
          clearDynamic3DLabels();
        } else {
          beforeAfterGroup.visible = true;
          const activeItem = auditPinItems.find((x) => x.note.id === activeAuditNoteId);
          if (activeItem && activeItem.s3d) renderBeforeAfterScene3D(activeItem.s3d.before_after_scene);
        }
        syncAuditVisibility();
      });
    }

    const btnMinHud = document.getElementById('ac3d-btn-min');
    if (btnMinHud) {
      btnMinHud.addEventListener('click', () => {
        const isMin = hudEl.classList.toggle('hud-minimized');
        btnMinHud.textContent = isMin ? '➕' : '▾';
      });
    }

    const btnModeBefore = document.getElementById('ac3d-mode-before');
    const btnModeAfter = document.getElementById('ac3d-mode-after');
    function setBeforeAfterMode(proposed) {
      isProposedMode = proposed;
      if (btnModeBefore) btnModeBefore.className = !proposed ? 'ac3d-ba-btn active-before' : 'ac3d-ba-btn';
      if (btnModeAfter) btnModeAfter.className = proposed ? 'ac3d-ba-btn active-after' : 'ac3d-ba-btn';
      if (activeAuditNoteId) {
        selectAuditNote3D(activeAuditNoteId, { flyTo: false, notifyParent: false });
      } else if (projectId === 'hafetz44') {
        renderBeforeAfterScene3D('basement_ve_full');
      }
    }
    if (btnModeBefore) btnModeBefore.addEventListener('click', () => setBeforeAfterMode(false));
    if (btnModeAfter) btnModeAfter.addEventListener('click', () => setBeforeAfterMode(true));

    document.querySelectorAll('#ac3d-filter-row [data-acfilter]').forEach((btn) => {
      btn.addEventListener('click', () => {
        auditFilter = btn.getAttribute('data-acfilter') || 'ALL';
        document.querySelectorAll('#ac3d-filter-row [data-acfilter]').forEach((b) => b.classList.toggle('active', b === btn));
        if (auditFilter === 'FAC') {
          if (typeof selectFloor === 'function') selectFloor('all');
          syncArchFloorBtns('all');
          facadeCladdingGroup.visible = true;
          if (typeof activatePreset === 'function') activatePreset('iso_east');
        } else if (auditFilter === 'BSM') {
          if (typeof setSliceMode === 'function') setSliceMode('single');
          if (typeof selectFloor === 'function') selectFloor('mar');
          syncArchFloorBtns('mar');
          renderBeforeAfterScene3D('basement_ve_full');
        }
        enforceCleanArchitecturalScene();
        syncAuditVisibility();
      });
    });

    // Listen for postMessage commands from the parent ArchiCheck Workspace
    window.addEventListener('message', (event) => {
      const msg = event.data;
      if (!msg || typeof msg !== 'object') return;

      if (msg.type === 'ARCHICHECK_SELECT_NOTE' && msg.noteId) {
        auditPinsVisible = true;
        auditFilter = 'ALL';
        document.querySelectorAll('#ac3d-filter-row [data-acfilter]').forEach((b) => {
          b.classList.toggle('active', b.getAttribute('data-acfilter') === 'ALL');
        });
        selectAuditNote3D(msg.noteId, { flyTo: true, notifyParent: false });
      } else if (msg.type === 'ARCHICHECK_SELECT_SHEET' && msg.sheetId) {
        const sid = msg.sheetId.toLowerCase();
        if (typeof setSliceMode === 'function' && typeof selectFloor === 'function') {
          if (sid.includes('basement')) {
            setSliceMode('single');
            selectFloor('mar');
            syncArchFloorBtns('mar');
            renderBeforeAfterScene3D('basement_ve_full');
          } else if (sid.includes('ground')) {
            setSliceMode('single');
            selectFloor('kar');
            syncArchFloorBtns('kar');
            renderBeforeAfterScene3D('ground_contour_recess');
          } else if (sid.includes('penthouse')) {
            setSliceMode('single');
            selectFloor('f9');
            syncArchFloorBtns('f9');
            renderBeforeAfterScene3D('penthouse_island_fix');
          } else if (sid.includes('typical')) {
            setSliceMode('single');
            selectFloor('f4');
            syncArchFloorBtns('f4');
            renderBeforeAfterScene3D('west_corridor_fix');
          }
          enforceCleanArchitecturalScene();
          syncAuditVisibility();
        }
      } else if (msg.type === 'ARCHICHECK_SET_BA_MODE') {
        setBeforeAfterMode(Boolean(msg.proposed));
      }
    });

    // Allow clicking directly on 3D Audit Volumes in the Three.js canvas
    const hostCanvas = document.getElementById('cad-canvas') || document.querySelector('canvas');
    if (hostCanvas) {
      let downPt = { x: 0, y: 0 };
      hostCanvas.addEventListener('pointerdown', (e) => {
        downPt = { x: e.clientX, y: e.clientY };
      });
      hostCanvas.addEventListener('pointerup', (e) => {
        if (e.button !== 0 || !auditPinsVisible) return;
        if (typeof isMeasureMode !== 'undefined' && isMeasureMode) return;
        if (typeof camState !== 'undefined' && camState.walkMode) return;
        if (Math.hypot(e.clientX - downPt.x, e.clientY - downPt.y) > 5) return;

        const rect = hostCanvas.getBoundingClientRect();
        const ndc = new THREE.Vector2(
          ((e.clientX - rect.left) / rect.width) * 2 - 1,
          -((e.clientY - rect.top) / rect.height) * 2 + 1
        );
        const rc = new THREE.Raycaster();
        rc.setFromCamera(ndc, activeCam);
        const pickMeshes = [];
        auditPinItems.forEach((it) => {
          if (it.boxGrp.visible && it.boxGrp.userData.mesh) {
            it.boxGrp.userData.mesh.userData.note = it.note;
            pickMeshes.push(it.boxGrp.userData.mesh);
          }
        });
        const hits = rc.intersectObjects(pickMeshes, false);
        if (hits.length > 0 && hits[0].object.userData.note) {
          selectAuditNote3D(hits[0].object.userData.note.id, { flyTo: true, notifyParent: true });
        }
      });
    }

    // Project 3D Audit Pin Badges every frame & enforce clean architectural scene state
    const clipHeightRef = () => (typeof clipPlane !== 'undefined' ? clipPlane.constant : 999);
    function updateAuditPinsProjection() {
      requestAnimationFrame(updateAuditPinsProjection);
      if (typeof gisMapPlanesGroup !== 'undefined' && gisMapPlanesGroup && gisMapPlanesGroup.visible) {
        gisMapPlanesGroup.visible = false;
      }
      if (typeof gisRingsGroup !== 'undefined' && gisRingsGroup && gisRingsGroup.visible) {
        gisRingsGroup.visible = false;
      }
      if (typeof gisPoisGroup !== 'undefined' && gisPoisGroup && gisPoisGroup.visible) {
        gisPoisGroup.visible = false;
      }
      if (typeof units3DGroup !== 'undefined' && units3DGroup && units3DGroup.visible) {
        units3DGroup.visible = false;
      }
      if (archGroundGrid && typeof currentFloorId !== 'undefined') {
        archGroundGrid.visible = (currentFloorId !== 'mar');
      }
      if (typeof activeCam === 'undefined' || !auditPinsVisible) return;
      if (typeof camState !== 'undefined' && camState.walkMode) {
        auditPinItems.forEach((it) => { it.pinEl.style.display = 'none'; });
        dynamic3DLabels.forEach((dl) => { dl.el.style.display = 'none'; });
        return;
      }

      const w = window.innerWidth;
      const h = window.innerHeight;
      const cLimit = clipHeightRef();

      auditPinItems.forEach((item) => {
        if (item.pinEl.dataset.allowed !== '1' || item.pos3D.y > cLimit + 0.5) {
          item.pinEl.style.display = 'none';
          return;
        }
        const p = item.pos3D.clone().project(activeCam);
        if (p.z > 1 || p.z < -1) {
          item.pinEl.style.display = 'none';
          return;
        }
        const sx = (p.x * 0.5 + 0.5) * w;
        const sy = (-p.y * 0.5 + 0.5) * h;
        if (sx < -40 || sx > w + 40 || sy < 40 || sy > h + 30) {
          item.pinEl.style.display = 'none';
          return;
        }
        item.pinEl.style.display = 'inline-flex';
        item.pinEl.style.left = `${sx}px`;
        item.pinEl.style.top = `${sy}px`;
      });

      dynamic3DLabels.forEach((dl) => {
        const p = dl.pos.clone().project(activeCam);
        if (p.z > 1 || p.z < -1) {
          dl.el.style.display = 'none';
          return;
        }
        const sx = (p.x * 0.5 + 0.5) * w;
        const sy = (-p.y * 0.5 + 0.5) * h;
        if (sx < -100 || sx > w + 100 || sy < 40 || sy > h + 20) {
          dl.el.style.display = 'none';
          return;
        }
        dl.el.style.display = 'block';
        dl.el.style.left = `${sx}px`;
        dl.el.style.top = `${sy}px`;
      });
    }
    updateAuditPinsProjection();

    // 8. Fetch the Project Analysis JSON (or use offline embedded data for file:// mode) and Build the 3D Overlay
    function updateHudSyncStatus(data) {
      const lbl = document.getElementById('ac3d-sync-status-lbl');
      if (!lbl || !data) return;
      const st = data.model_3d_sync_status || (data.project_data_summary && data.project_data_summary.model_3d_sync_status) || {};
      const hShort = st.base_model_hash_short ? st.base_model_hash_short.slice(0, 8) : 'מאומת';
      const rev = st.audit_revision || 1;
      if (st.was_updated_and_reaudited) {
        lbl.innerHTML = `<strong style="color:#4ade80;">🟢 מודל עודכן (סבב #${rev})</strong> · <code>#${hShort}</code>`;
      } else {
        lbl.innerHTML = `🧊 מודל 3D מאומת · <code>#${hShort}</code> · סבב #${rev}`;
      }
      lbl.title = st.status_message_he || '';
    }

    function applyAuditData(data) {
      if (data && data.notes) {
        updateHudSyncStatus(data);
        buildAuditPinsAndVolumes(data);
        if (window.parent && window.parent !== window) {
          window.parent.postMessage({ type: 'ARCHICHECK_3D_READY', projectId }, '*');
        }
      }
    }

    const btnReaudit3d = document.getElementById('ac3d-btn-reaudit');
    if (btnReaudit3d) {
      btnReaudit3d.addEventListener('click', () => {
        const lbl = document.getElementById('ac3d-sync-status-lbl');
        if (lbl) lbl.textContent = '⏳ בודק שינויים במודל ה-3D ומריץ בקרה תכנונית מלאה...';
        fetch('/api/check_3d_models', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ project: projectId, force: true }),
        })
          .then((r) => r.json())
          .then((res) => {
            if (res && res.payload) {
              applyAuditData(res.payload);
              if (window.parent && window.parent !== window) {
                window.parent.postMessage({ type: 'ARCHICHECK_3D_REAUDITED', payload: res.payload }, '*');
              }
            }
          })
          .catch(() => {
            if (lbl) lbl.textContent = '⚠️ מצב לא מקוון — נתוני בקרה מקומיים פעילים';
          });
      });
    }

    if (window.location.protocol === 'file:' && window.__ARCHICHECK_EMBEDDED_DATA__) {
      applyAuditData(window.__ARCHICHECK_EMBEDDED_DATA__);
    } else {
      fetch(`/api/analyze_project?q=${encodeURIComponent(projectId)}`)
        .then((r) => (r.ok ? r.json() : fetch(`/api/${projectId}.json`).then((r2) => r2.json())))
        .then((data) => applyAuditData(data))
        .catch(() => {
          fetch(`/api/${projectId}.json`)
            .then((r) => r.json())
            .then((data) => applyAuditData(data))
            .catch(() => {
              if (window.__ARCHICHECK_EMBEDDED_DATA__) {
                applyAuditData(window.__ARCHICHECK_EMBEDDED_DATA__);
              }
            });
        });
    }
  }
})();
