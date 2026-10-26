// -*- coding: utf-8 -*-
/**
 * ArchiCheck AI — Synchronized Split-Screen Architectural Analysis Controller
 * Quarter-screen Textual Audit Document (Right) + Two-Thirds Interactive Floor Plan Canvas (Left)
 */

(function () {
  // DOM References
  const searchForm = document.getElementById('project-search-form');
  const queryInput = document.getElementById('project-query-input');
  const quickChipsContainer = document.getElementById('project-quick-chips');
  const fileUploadInput = document.getElementById('file-upload-input');

  const btnToggleFiles = document.getElementById('btn-toggle-files');
  const filesCountBadge = document.getElementById('files-count-badge');
  const filesDrawer = document.getElementById('discovered-files-drawer');
  const filesDrawerSubtitle = document.getElementById('files-drawer-subtitle');
  const filesListGrid = document.getElementById('discovered-files-list');
  const btnCloseFilesDrawer = document.getElementById('btn-close-files-drawer');
  const btnOpenPdfReport = document.getElementById('btn-open-pdf-report');
  const btnOpen3dViewer = document.getElementById('btn-open-3d-viewer');
  const btnOpenSummaryModal = document.getElementById('btn-open-summary-modal');
  const btnOpenSummaryDoc = document.getElementById('btn-open-summary-doc');
  const summaryAreasModal = document.getElementById('summary-areas-modal');
  const summaryModalTitle = document.getElementById('summary-modal-title');
  const summaryModalPrintLink = document.getElementById('summary-modal-print-link');
  const btnCloseSummaryModal = document.getElementById('btn-close-summary-modal');
  const summaryModalBody = document.getElementById('summary-modal-body');

  const btnOpenValueEngModal = document.getElementById('btn-open-value-eng-modal');
  const valueEngModal = document.getElementById('value-eng-modal');
  const valueEngModalTitle = document.getElementById('value-eng-modal-title');
  const btnCloseValueEngModal = document.getElementById('btn-close-value-eng-modal');
  const valueEngModalBody = document.getElementById('value-eng-modal-body');

  const docProjectTitle = document.getElementById('doc-project-title');
  const docProjectSubtitle = document.getElementById('doc-project-subtitle');
  const docMetricsGrid = document.getElementById('doc-metrics-grid');
  const docSectionsRoot = document.getElementById('doc-sections-root');
  const countAllEl = document.getElementById('count-all');
  const countVeEl = document.getElementById('count-ve');
  const countIssuesEl = document.getElementById('count-issues');
  const countPassEl = document.getElementById('count-pass');
  const filterBtns = document.querySelectorAll('.filter-btn');

  const sheetTabsContainer = document.getElementById('sheet-tabs-container');
  const btnToggleVePlanMode = document.getElementById('btn-toggle-ve-plan-mode');
  const btnToggleAllPins = document.getElementById('btn-toggle-all-pins');
  const vePlanBar = document.getElementById('ve-plan-bar');
  const vePlanBarTotal = document.getElementById('ve-plan-bar-total');
  const vePlanHotspotsList = document.getElementById('ve-plan-hotspots-list');
  const btnZoomIn = document.getElementById('btn-zoom-in');
  const btnZoomOut = document.getElementById('btn-zoom-out');
  const btnZoomReset = document.getElementById('btn-zoom-reset');
  const zoomLevelLabel = document.getElementById('zoom-level-label');

  const planViewport = document.getElementById('plan-viewport');
  const planStage = document.getElementById('plan-stage');
  const planImageWrapper = document.getElementById('plan-image-wrapper');
  const planImage = document.getElementById('plan-image');
  const planSvgOverlay = document.getElementById('plan-svg-overlay');
  const planPinsLayer = document.getElementById('plan-pins-layer');
  const floatingCard = document.getElementById('plan-floating-card');

  const fcPinBadge = document.getElementById('fc-pin-badge');
  const fcStatusBadge = document.getElementById('fc-status-badge');
  const fcRuleBadge = document.getElementById('fc-rule-badge');
  const fcRoomName = document.getElementById('fc-room-name');
  const fcTitle = document.getElementById('fc-title');
  const fcMeasured = document.getElementById('fc-measured');
  const fcBenchmark = document.getElementById('fc-benchmark');
  const fcSummary = document.getElementById('fc-summary');
  const fcVeWhereHowBox = document.getElementById('fc-ve-where-how-box');
  const fcVeSavingBanner = document.getElementById('fc-ve-saving-banner');
  const fcVeWhere = document.getElementById('fc-ve-where');
  const fcVeHow = document.getElementById('fc-ve-how');
  const fcRecommendation = document.getElementById('fc-recommendation');

  const hudSheetBadge = document.getElementById('hud-sheet-badge');
  const hudActiveNoteText = document.getElementById('hud-active-note-text');
  const loadingOverlay = document.getElementById('loading-overlay');
  const loadingTitle = document.getElementById('loading-title');

  // Application State
  let currentProject = null;
  let currentSheetId = null;
  let currentFilter = 'ALL';
  let activeNoteId = null;
  let showAllPins = true;

  // Pan & Zoom State
  let scale = 1.0;
  let panX = 0;
  let panY = 0;
  let isDragging = false;
  let dragStartX = 0;
  let dragStartY = 0;

  const STATUS_LABELS = {
    PASS: 'תקין (PASS)',
    WARN: 'התראת איכות (WARN)',
    FAIL: 'ליקוי חוקי (FAIL)',
  };

  // =========================================================================
  // 1. FETCH & ANALYZE PROJECT ACROSS ALL FOLDERS
  // =========================================================================
  async function loadProjectAnalysis(queryStr) {
    const cleanQuery = (queryStr || 'פינס 48').trim();
    queryInput.value = cleanQuery;

    // Update active state on quick chips
    document.querySelectorAll('.proj-chip').forEach((chip) => {
      const cq = (chip.getAttribute('data-query') || '').trim();
      chip.classList.toggle('active', cq === cleanQuery || cleanQuery.includes(cq));
    });

    loadingTitle.textContent = `סורק תיקיות ומנתח את הפרויקט "${cleanQuery}"...`;
    loadingOverlay.classList.remove('hidden');

    try {
      let data = null;
      try {
        const resp = await fetch('/api/analyze_project', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: cleanQuery }),
        });
        if (resp.ok) {
          data = await resp.json();
        }
      } catch (apiErr) {
        console.warn('API endpoint not reachable, trying static fallback:', apiErr);
      }

      if (!data) {
        // Fallback for Google Cloud / Firebase Hosting
        const q_low = cleanQuery.toLowerCase();
        let staticFile = 'pines48.json';
        if (['פאירברג', 'פאיירברג', 'פיארברג', 'feierberg', 'fairberg', 'feirberg', '6387'].some((k) => q_low.includes(k))) staticFile = 'feierberg3.json';
        else if (['יטקובסקי', 'yatkovski', '7א'].some((k) => q_low.includes(k))) staticFile = 'yatkovski7.json';
        else if (['קיטרוני', 'קטרוני', 'kitroni', '37', '39'].some((k) => q_low.includes(k))) staticFile = 'kitroni37.json';
        else if (['חפץ', 'חיים', 'hafetz', '44'].some((k) => q_low.includes(k))) staticFile = 'hafetz44.json';
        else if (['קקל', 'קק"ל', 'קק״ל', 'kkl', '10'].some((k) => q_low.includes(k))) staticFile = 'kkl10.json';

        const staticResp = await fetch(`/api/${staticFile}`);
        if (!staticResp.ok) {
          throw new Error(`שגיאת שרת (${staticResp.status})`);
        }
        data = await staticResp.json();
      }

      currentProject = data;
      currentFilter = 'ALL';
      filterBtns.forEach((b) => b.classList.toggle('active', b.dataset.filter === 'ALL'));
      if (btnToggleVePlanMode) btnToggleVePlanMode.classList.remove('active');

      renderProjectHeaderAndFiles(data);
      renderSheetTabs(data);
      renderVePlanBar(data);

      // Select first sheet by default
      const firstSheet = (data.sheets && data.sheets[0]) ? data.sheets[0].id : null;
      selectSheet(firstSheet, { keepNote: false });

      renderDocumentSections(data);

      // Highlight the first note automatically so the user immediately sees the visual synchronization
      if (data.notes && data.notes.length > 0) {
        highlightNote(data.notes[0].id, { scrollDoc: false });
      }
    } catch (err) {
      console.error('Analysis error:', err);
      hudActiveNoteText.textContent = `שגיאה בטעינת הפרויקט: ${err.message}`;
    } finally {
      loadingOverlay.classList.add('hidden');
    }
  }

  // =========================================================================
  // 2. RENDER HEADER, SCORECARDS & DISCOVERED FILES ACROSS FOLDERS
  // =========================================================================
  function renderProjectHeaderAndFiles(data) {
    docProjectTitle.textContent = data.project_name || 'דוח ניתוח אדריכלי';
    docProjectSubtitle.textContent = data.project_subtitle || '';

    // PDF Report Button
    if (data.pdf_report_url) {
      btnOpenPdfReport.href = data.pdf_report_url;
      btnOpenPdfReport.classList.remove('hidden');
    } else {
      btnOpenPdfReport.classList.add('hidden');
    }

    // 3D BIM Viewer Button (when web-accessible URL is available, e.g. Feierberg 3)
    if (btnOpen3dViewer) {
      if (data.viewer_3d_url && data.viewer_3d_url.startsWith('/')) {
        btnOpen3dViewer.href = data.viewer_3d_url;
        btnOpen3dViewer.classList.remove('hidden');
      } else {
        btnOpen3dViewer.classList.add('hidden');
      }
    }

    // Summary & Quantitative Data Document Button
    const pds = data.project_data_summary;
    if (pds && pds.summary_doc_url && btnOpenSummaryDoc) {
      btnOpenSummaryDoc.href = pds.summary_doc_url;
      btnOpenSummaryDoc.classList.remove('hidden');
    } else if (btnOpenSummaryDoc) {
      btnOpenSummaryDoc.classList.add('hidden');
    }

    // Scorecards
    docMetricsGrid.innerHTML = '';
    (data.metrics || []).forEach((m) => {
      const card = document.createElement('div');
      card.className = 'doc-metric-card';
      card.innerHTML = `
        <div class="doc-metric-val">${m.value}</div>
        <div class="doc-metric-label">${m.label}</div>
      `;
      docMetricsGrid.appendChild(card);
    });

    // Counts for filter buttons
    const notes = data.notes || [];
    const veCount = notes.filter((n) => n.is_value_eng).length;
    const passCount = notes.filter((n) => n.status === 'PASS').length;
    const issuesCount = notes.filter((n) => n.status !== 'PASS' && !n.is_value_eng).length;
    countAllEl.textContent = notes.length;
    if (countVeEl) countVeEl.textContent = veCount;
    countIssuesEl.textContent = issuesCount;
    countPassEl.textContent = passCount;

    // Discovered files across folders
    const files = data.discovered_files || [];
    filesCountBadge.textContent = files.length;
    filesDrawerSubtitle.textContent = `נמצאו ${files.length} קבצים רלוונטיים עבור "${data.project_name}"`;
    filesListGrid.innerHTML = '';

    files.forEach((f) => {
      const item = document.createElement('div');
      item.className = 'file-item-card';
      item.innerHTML = `
        <div style="overflow:hidden;flex:1;">
          <div class="file-name-text" title="${f.path}">${f.name}</div>
          <div class="file-folder-text" title="${f.folder}">${f.folder}</div>
        </div>
        <span class="file-ext-badge">${f.ext || 'FILE'}</span>
      `;
      filesListGrid.appendChild(item);
    });
  }

  // =========================================================================
  // 3. RENDER FLOOR / SHEET TABS & VISUAL PLAN OVERLAY
  // =========================================================================
  function renderSheetTabs(data) {
    sheetTabsContainer.innerHTML = '';
    const sheets = data.sheets || [];
    const notes = data.notes || [];

    sheets.forEach((sh) => {
      const sheetNotesCount = notes.filter((n) => n.sheet_id === sh.id).length;
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'sheet-tab-btn';
      btn.dataset.sheetId = sh.id;
      btn.innerHTML = `
        <span>📐 ${sh.title}</span>
        <span class="sheet-tab-count">${sheetNotesCount} הערות</span>
      `;
      btn.addEventListener('click', () => {
        selectSheet(sh.id, { keepNote: false });
      });
      sheetTabsContainer.appendChild(btn);
    });
  }

  function selectSheet(sheetId, options = {}) {
    if (!currentProject || !sheetId) return;
    const sheet = (currentProject.sheets || []).find((s) => s.id === sheetId);
    if (!sheet) return;

    const sheetChanged = currentSheetId !== sheetId;
    currentSheetId = sheetId;

    // Update active tab button
    document.querySelectorAll('.sheet-tab-btn').forEach((btn) => {
      btn.classList.toggle('active', btn.dataset.sheetId === sheetId);
    });

    if (sheetChanged) {
      planImage.src = sheet.image_url;
      resetZoomAndPan();
    }

    hudSheetBadge.textContent = `${sheet.sheet_code || ''} · ${sheet.elevation || ''}`;
    renderVisualPlanAnnotations();

    if (!options.keepNote) {
      const firstSheetNote = (currentProject.notes || []).find((n) => n.sheet_id === sheetId && matchesFilter(n));
      if (firstSheetNote) {
        highlightNote(firstSheetNote.id, { scrollDoc: false, switchSheet: false });
      } else {
        floatingCard.classList.add('hidden');
      }
    }
  }

  function renderVePlanBar(data) {
    if (!vePlanBar || !vePlanHotspotsList) return;
    const notes = (data.notes || []).filter((n) => n.is_value_eng);
    const sheetsMap = {};
    (data.sheets || []).forEach((s) => {
      sheetsMap[s.id] = s.title;
    });

    const pds = data.project_data_summary || {};
    const optKpis = (pds.design_optimization || {}).executive_kpis || {};
    if (vePlanBarTotal) {
      vePlanBarTotal.innerHTML = `💰 מודל החיסכון המוצע על התכנית: <strong>${fmtNum(optKpis.grand_total_direct_saving_ils)} ₪</strong> (+${fmtNum(optKpis.internal_reclaimed_living_sqm)} מ״ר השבחת דירות)`;
    }

    vePlanHotspotsList.innerHTML = '';
    const catIcons = { AG: '🏢', UG: '🅿️', FAC: '🧱', APT: '🛋️' };

    notes.forEach((n) => {
      const chip = document.createElement('button');
      chip.type = 'button';
      chip.className = `ve-hotspot-chip ve-cat-${n.ve_category || 'AG'} ${n.id === activeNoteId ? 'active' : ''}`;
      chip.dataset.noteId = n.id;
      chip.dataset.sheetId = n.sheet_id;
      const icon = catIcons[n.ve_category] || '💰';
      const shTitle = (sheetsMap[n.sheet_id] || '').replace('תכנית ', '');
      chip.innerHTML = `
        <span class="ve-chip-pin">#${n.pin_num}</span>
        <span>${icon} ${n.ve_callout_badge || n.measured}</span>
        <span class="ve-chip-sheet">${shTitle}</span>
      `;
      chip.title = `איפה: ${n.where_on_plan || n.room_name}\nאיך: ${n.how_to_execute || n.recommendation}`;
      chip.addEventListener('click', () => {
        focusSavingsItemOnPlan(n.id, n.sheet_id);
      });
      vePlanHotspotsList.appendChild(chip);
    });
  }

  function focusSavingsItemOnPlan(noteId, sheetId) {
    if (!currentProject) return;
    if (valueEngModal) valueEngModal.classList.add('hidden');
    if (summaryAreasModal) summaryAreasModal.classList.add('hidden');

    // Switch filter to VE so all savings zones & callout badges on the floor are highlighted clearly
    currentFilter = 'VE';
    filterBtns.forEach((b) => b.classList.toggle('active', b.dataset.filter === 'VE'));
    if (btnToggleVePlanMode) btnToggleVePlanMode.classList.add('active');

    renderDocumentSections(currentProject);
    if (sheetId && sheetId !== currentSheetId) {
      selectSheet(sheetId, { keepNote: true });
    }
    if (noteId) {
      highlightNote(noteId, { scrollDoc: true, switchSheet: true });
    } else {
      renderVisualPlanAnnotations();
    }
  }

  function matchesFilter(note) {
    if (currentFilter === 'ALL') return true;
    if (currentFilter === 'VE') return Boolean(note.is_value_eng);
    if (currentFilter === 'PASS') return note.status === 'PASS';
    if (currentFilter === 'ISSUES') return (note.status === 'WARN' || note.status === 'FAIL') && !note.is_value_eng;
    return true;
  }

  function renderVisualPlanAnnotations() {
    if (!currentProject) return;
    planSvgOverlay.innerHTML = '';
    planPinsLayer.innerHTML = '';

    const sheetNotes = (currentProject.notes || []).filter(
      (n) => n.sheet_id === currentSheetId && matchesFilter(n)
    );

    sheetNotes.forEach((note) => {
      const isNoteActive = note.id === activeNoteId;
      const isVe = Boolean(note.is_value_eng);

      // 1. SVG Room Zone Bounding Box
      const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      rect.setAttribute('x', note.x_pct);
      rect.setAttribute('y', note.y_pct);
      rect.setAttribute('width', note.w_pct);
      rect.setAttribute('height', note.h_pct);
      rect.setAttribute(
        'class',
        `room-zone-rect zone-${note.status} ${isVe ? 'zone-VE' : ''} ${isNoteActive ? 'active-zone' : ''}`
      );
      rect.dataset.noteId = note.id;

      if (!showAllPins && !isNoteActive && currentFilter !== 'VE') {
        rect.style.opacity = '0';
      }

      rect.addEventListener('mouseenter', () => {
        highlightNote(note.id, { scrollDoc: true, switchSheet: false });
      });
      rect.addEventListener('click', (e) => {
        e.stopPropagation();
        highlightNote(note.id, { scrollDoc: true, switchSheet: false });
      });
      planSvgOverlay.appendChild(rect);

      // 2. Numbered Pin on Plan
      const pin = document.createElement('button');
      pin.type = 'button';
      pin.className = `plan-pin pin-${note.status} ${isVe ? 'pin-VE' : ''} ${isNoteActive ? 'active-pin' : ''}`;
      pin.style.left = `${note.cx_pct}%`;
      pin.style.top = `${note.cy_pct}%`;
      pin.textContent = note.pin_num;
      pin.dataset.noteId = note.id;
      pin.title = `#${note.pin_num}: ${note.room_name} — ${note.title}`;

      if (!showAllPins && !isNoteActive && currentFilter !== 'VE') {
        pin.style.opacity = '0';
        pin.style.pointerEvents = 'none';
      }

      pin.addEventListener('mouseenter', () => {
        highlightNote(note.id, { scrollDoc: true, switchSheet: false });
      });
      pin.addEventListener('click', (e) => {
        e.stopPropagation();
        highlightNote(note.id, { scrollDoc: true, switchSheet: false });
      });

      planPinsLayer.appendChild(pin);

      // 3. On-Plan Visual Callout Badge ("איפה ואיך על התכנית") for Value Engineering items
      if (isVe && (currentFilter === 'VE' || isNoteActive)) {
        const callout = document.createElement('div');
        callout.className = `plan-ve-callout ${isNoteActive ? 'active-callout' : ''}`;
        callout.style.left = `${note.cx_pct}%`;
        callout.style.top = `${note.cy_pct}%`;
        callout.dataset.noteId = note.id;

        const badgeText = note.ve_callout_badge || note.measured;
        const shortRoom = (note.room_name || '').split('—')[0].trim();

        if (isNoteActive) {
          callout.innerHTML = `
            <div class="ve-callout-top">💰 #${note.pin_num} · ${badgeText}</div>
            <div class="ve-callout-where"><strong>📍 איפה:</strong> ${note.where_on_plan || shortRoom}</div>
            <div class="ve-callout-how"><strong>🛠️ איך:</strong> ${note.how_to_execute || note.recommendation}</div>
          `;
        } else {
          callout.innerHTML = `
            <div class="ve-callout-top">💰 #${note.pin_num} · ${badgeText}</div>
            <div class="ve-callout-sub">${shortRoom}</div>
          `;
        }

        callout.addEventListener('click', (e) => {
          e.stopPropagation();
          highlightNote(note.id, { scrollDoc: true, switchSheet: false });
        });
        planPinsLayer.appendChild(callout);
      }
    });
  }

  // =========================================================================
  // 4. RENDER RIGHT-HAND TEXTUAL ANALYSIS DOCUMENT + SUMMARY & QUANTITATIVE DATA
  // =========================================================================
  function fmtNum(val) {
    if (val === undefined || val === null || isNaN(Number(val))) return val || '0';
    return Number(val).toLocaleString('he-IL', { maximumFractionDigits: 2 });
  }

  function buildInlineSummaryAndAreasElement(data) {
    const pds = data.project_data_summary;
    if (!pds) return null;

    const ag = pds.above_ground_areas || {};
    const ug = pds.underground_areas || {};
    const rt = pds.roof_terraces || {};
    const sb = pds.suspended_balconies || {};
    const fac = pds.facades || {};
    const flr = pds.flooring_areas || {};
    const opt = pds.design_optimization || {};
    const optKpis = opt.executive_kpis || {};
    const sdoc = pds.summary_document || {};

    const wrapper = document.createElement('div');
    wrapper.className = 'doc-summary-master-box';

    const agRows = (ag.by_floor || [])
      .map(
        (f) => `
        <tr>
          <td><strong>${f.floor_label}</strong><div style="font-size:9.5px;color:#64748b;">${f.elevation || ''}</div></td>
          <td>${fmtNum(f.apartments_sqm)}</td>
          <td>${fmtNum(f.core_service_sqm)}</td>
          <td><strong>${fmtNum(f.total_floor_sqm)} מ״ר</strong></td>
          <td>${f.pct_of_above_ground}%</td>
        </tr>`
      )
      .join('');

    const ugRows = (ug.by_floor || [])
      .map(
        (f) => `
        <tr>
          <td><strong>${f.floor_label}</strong> (${f.elevation || ''})</td>
          <td>${f.usage_description || ''}</td>
          <td><strong>${fmtNum(f.total_floor_sqm)} מ״ר</strong></td>
        </tr>`
      )
      .join('');

    const rtRows = (rt.breakdown || [])
      .map(
        (b) => `
        <tr>
          <td><strong>${b.floor_label}</strong></td>
          <td>${b.unit_label}<div style="font-size:9.5px;color:#64748b;">${b.dimensions || ''}</div></td>
          <td><strong>${fmtNum(b.area_sqm)} מ״ר</strong></td>
        </tr>`
      )
      .join('');

    const sbRows = (sb.breakdown || [])
      .map(
        (b) => `
        <tr>
          <td><strong>${b.floor_label}</strong></td>
          <td>${b.unit_label} (${b.count} יח׳ × ${fmtNum(b.unit_area_sqm)} מ״ר)</td>
          <td><strong>${fmtNum(b.total_area_sqm)} מ״ר</strong></td>
        </tr>`
      )
      .join('');

    const facRows = (fac.by_direction || [])
      .map(
        (d) => `
        <tr>
          <td><strong>${d.facade_name}</strong></td>
          <td>${fmtNum(d.length_m)}×${fmtNum(d.height_m)} מ׳</td>
          <td><strong>${fmtNum(d.gross_area_sqm)} מ״ר</strong> (${d.pct_of_total}%)</td>
          <td>זיגוג: ${fmtNum(d.glazing_area_sqm)} מ״ר | אטום: ${fmtNum(d.opaque_area_sqm)} מ״ר</td>
        </tr>`
      )
      .join('');

    const flrRows = (flr.by_floor || [])
      .map(
        (f) => `
        <tr>
          <td><strong>${f.floor_label}</strong><div style="font-size:9.5px;color:#64748b;">${f.elevation || ''}</div></td>
          <td>${fmtNum(f.apartments_flooring_sqm)}<div style="font-size:9px;color:#64748b;">יבש: ${fmtNum(f.apartments_dry_sqm)} | רטוב: ${fmtNum(f.apartments_wet_sqm)}</div></td>
          <td>${fmtNum(f.public_flooring_sqm)}</td>
          <td>${fmtNum(f.balconies_flooring_sqm)}</td>
          <td><strong>${fmtNum(f.total_floor_flooring_sqm)} מ״ר</strong></td>
        </tr>`
      )
      .join('');

    const proposalsHtml = (sdoc.improvement_proposals || [])
      .map(
        (p, idx) => `
        <div class="proposal-mini-item">
          <div class="proposal-mini-priority">הצעה #${idx + 1} · עדיפות: ${p.priority}</div>
          <div class="proposal-mini-target">🎯 ${p.target}</div>
          <div class="proposal-mini-text"><strong>הבעיה:</strong> ${p.issue}</div>
          <div class="proposal-mini-text" style="margin-top:3px;color:#1e3a8a;"><strong>✅ הצעה לשיפור:</strong> ${p.proposal}</div>
        </div>`
      )
      .join('');

    const critNotesHtml = (sdoc.critical_notes_summary || [])
      .map((item) => `<li style="margin-bottom:4px;">${item}</li>`)
      .join('');

    wrapper.innerHTML = `
      <div class="doc-summary-master-header">
        <div class="doc-summary-master-title">📊 נתוני פרויקט, שטחים, חזיתות וסיכום הערות</div>
        <button type="button" class="btn-expand-full-summary" id="btn-inline-open-modal">🔍 תצוגת טבלאות מלאה</button>
      </div>

      <!-- Quantitative KPI Cards -->
      <div class="quant-kpi-grid">
        <div class="quant-kpi-card">
          <div class="quant-kpi-label">🏢 סך שטחי בנייה עיליים</div>
          <div class="quant-kpi-value">${fmtNum(ag.total_sqm)} מ״ר</div>
          <div class="quant-kpi-sub">דירות: ${fmtNum(ag.net_apartments_sqm)} | ליבה/שירות: ${fmtNum(ag.core_and_service_sqm)} מ״ר</div>
        </div>
        <div class="quant-kpi-card">
          <div class="quant-kpi-label">🅿️ סך שטחי בנייה תת-קרקעיים</div>
          <div class="quant-kpi-value">${fmtNum(ug.total_sqm)} מ״ר</div>
          <div class="quant-kpi-sub">${ug.parking_spaces || 0} חניות · סה״כ בנוי: ${fmtNum(pds.total_built_area_sqm)} מ״ר</div>
        </div>
        <div class="quant-kpi-card">
          <div class="quant-kpi-label">🌇 סך שטחי מרפסות גג</div>
          <div class="quant-kpi-value">${fmtNum(rt.total_sqm)} מ״ר</div>
          <div class="quant-kpi-sub">${rt.count || 0} טרסות גג${rt.garden_terraces_sqm ? ` (+${fmtNum(rt.garden_terraces_sqm)} מ״ר גינות)` : ''}</div>
        </div>
        <div class="quant-kpi-card">
          <div class="quant-kpi-label">🌿 סך שטחי מרפסות תלויות</div>
          <div class="quant-kpi-value">${fmtNum(sb.total_sqm)} מ״ר</div>
          <div class="quant-kpi-sub">${sb.count || 0} מרפסות זיזיות${sb.service_balconies_sqm ? ` (+${fmtNum(sb.service_balconies_sqm)} מ״ר שירות)` : ''}</div>
        </div>
        <div class="quant-kpi-card kpi-wide">
          <div class="quant-kpi-label">🧱 סך שטחי חזיתות החוץ (בחלוקה ל-4 חזיתות)</div>
          <div class="quant-kpi-value">${fmtNum(fac.total_sqm)} מ״ר</div>
          <div class="quant-kpi-sub">גובה מבנה: ${fmtNum(fac.building_height_m)} מ׳ · פתחים/זיגוג: ${fmtNum(fac.total_glazing_sqm)} מ״ר (${fac.average_wwr_pct}%) · קירות/חיפוי: ${fmtNum(fac.total_opaque_sqm)} מ״ר</div>
        </div>
        <div class="quant-kpi-card">
          <div class="quant-kpi-label">🛋️ סך ריצוף דירות (נטו)</div>
          <div class="quant-kpi-value">${fmtNum(flr.total_apartments_flooring_sqm)} מ״ר</div>
          <div class="quant-kpi-sub">יבש: ${fmtNum(flr.total_apartments_dry_sqm)} | רטוב: ${fmtNum(flr.total_apartments_wet_sqm)} מ״ר</div>
        </div>
        <div class="quant-kpi-card">
          <div class="quant-kpi-label">🏛️ סך ריצוף ציבורי (נטו)</div>
          <div class="quant-kpi-value">${fmtNum(flr.total_public_flooring_sqm)} מ״ר</div>
          <div class="quant-kpi-sub">מרפסות: ${fmtNum(flr.total_balconies_flooring_sqm)} מ״ר · סה״כ ריצוף: ${fmtNum(flr.grand_total_flooring_sqm)} מ״ר</div>
        </div>
        <div class="quant-kpi-card kpi-wide" style="border-right-color:#059669;background:#ecfdf5;border-color:#6ee7b7;cursor:pointer;" id="kpi-card-open-ve">
          <div class="quant-kpi-label" style="color:#065f46;display:flex;justify-content:space-between;align-items:center;">
            <span>💰 פוטנציאל חיסכון בבדיקת ייעול תכנון (ללא פגיעה בדירות/חניות)</span>
            <span style="background:#059669;color:#fff;padding:2px 7px;border-radius:4px;font-size:10px;">פתח סימולטור ◂</span>
          </div>
          <div class="quant-kpi-value" style="color:#047857;font-size:17px;">${fmtNum(optKpis.grand_total_direct_saving_ils)} ₪ חיסכון ישיר</div>
          <div class="quant-kpi-sub" style="color:#065f46;">
            עילי: ${fmtNum(optKpis.above_ground_saved_sqm)} מ״ר (${fmtNum(optKpis.above_ground_saving_ils)} ₪) ·
            חניון: ${fmtNum(optKpis.underground_saved_sqm)} מ״ר (${fmtNum(optKpis.underground_saving_ils)} ₪) ·
            חיפוי/טיח: ${fmtNum(optKpis.facade_saving_ils)} ₪ ·
            השבחת דירות: +${fmtNum(optKpis.internal_reclaimed_living_sqm)} מ״ר
          </div>
        </div>
      </div>

      <!-- 1. Summary Document of Audit Notes & Improvement Proposals -->
      <details class="doc-collapsible-details" open>
        <summary>
          <span>📋 מסמך סיכום הערות והצעות לשיפור (${(sdoc.improvement_proposals || []).length} הצעות)</span>
          <span>▾</span>
        </summary>
        <div class="doc-collapsible-body">
          <div style="background:#eff6ff;border:1px solid #bfdbfe;padding:7px 9px;border-radius:6px;margin-bottom:8px;font-weight:600;color:#1e3a8a;">
            ${sdoc.overall_verdict || ''}
          </div>
          <div style="font-weight:800;color:#0f172a;margin-bottom:4px;">📌 ריכוז הערות מרכזיות בבדיקת המודל:</div>
          <ul style="padding-right:16px;margin:0 0 8px 0;color:#334155;">${critNotesHtml}</ul>
          <div style="font-weight:800;color:#0f172a;margin-bottom:5px;">🛠️ הצעות אופרטיביות לשיפור התכנון:</div>
          ${proposalsHtml}
        </div>
      </details>

      <!-- 2. Above-Ground & Underground Areas by Floor -->
      <details class="doc-collapsible-details">
        <summary>
          <span>🏢 שטחי בנייה עיליים (${fmtNum(ag.total_sqm)} מ״ר) ותת-קרקעיים (${fmtNum(ug.total_sqm)} מ״ר) לפי קומות</span>
          <span>▾</span>
        </summary>
        <div class="doc-collapsible-body">
          <div style="font-weight:800;color:#0f172a;margin-bottom:4px;">א. חלוקת שטחי בנייה עיליים לפי קומות:</div>
          <table class="mini-quant-table">
            <thead>
              <tr>
                <th>קומה ומפלס</th>
                <th>דירות</th>
                <th>ליבה</th>
                <th>סה״כ קומה</th>
                <th>%</th>
              </tr>
            </thead>
            <tbody>
              ${agRows}
              <tr class="total-row">
                <td>סה״כ בנייה עילית</td>
                <td>${fmtNum(ag.net_apartments_sqm)}</td>
                <td>${fmtNum(ag.core_and_service_sqm)}</td>
                <td>${fmtNum(ag.total_sqm)} מ״ר</td>
                <td>100%</td>
              </tr>
            </tbody>
          </table>

          <div style="font-weight:800;color:#0f172a;margin:10px 0 4px 0;">ב. שטחי בנייה תת-קרקעיים (מרתפים):</div>
          <table class="mini-quant-table">
            <thead>
              <tr>
                <th>קומת מרתף</th>
                <th>פירוט שימושים וחניות</th>
                <th>שטח קומה</th>
              </tr>
            </thead>
            <tbody>
              ${ugRows}
              <tr class="total-row">
                <td colspan="2">סה״כ בנייה תת-קרקעית (${ug.parking_spaces || 0} חניות)</td>
                <td>${fmtNum(ug.total_sqm)} מ״ר</td>
              </tr>
              <tr class="total-row" style="background:#dbeafe;">
                <td colspan="2">סה״כ שטח בנוי כולל בפרויקט (עילי + תת-קרקעי)</td>
                <td>${fmtNum(pds.total_built_area_sqm)} מ״ר</td>
              </tr>
            </tbody>
          </table>
        </div>
      </details>

      <!-- 3. Roof Terraces & Suspended Balconies -->
      <details class="doc-collapsible-details">
        <summary>
          <span>🌿 שטחי מרפסות גג (${fmtNum(rt.total_sqm)} מ״ר) ומרפסות תלויות (${fmtNum(sb.total_sqm)} מ״ר)</span>
          <span>▾</span>
        </summary>
        <div class="doc-collapsible-body">
          <div style="font-weight:800;color:#0f172a;margin-bottom:4px;">א. פירוט מרפסות גג (פנטהאוזים ודירות גג):</div>
          <table class="mini-quant-table">
            <thead>
              <tr>
                <th>קומה</th>
                <th>שיוך ומידות</th>
                <th>שטח</th>
              </tr>
            </thead>
            <tbody>
              ${rtRows}
              <tr class="total-row">
                <td colspan="2">סה״כ מרפסות גג (${rt.count || 0} מרפסות)</td>
                <td>${fmtNum(rt.total_sqm)} מ״ר</td>
              </tr>
            </tbody>
          </table>

          <div style="font-weight:800;color:#0f172a;margin:10px 0 4px 0;">ב. פירוט מרפסות תלויות / זיזיות:</div>
          <table class="mini-quant-table">
            <thead>
              <tr>
                <th>קומות</th>
                <th>טיפוס וכמות</th>
                <th>סה״כ שטח</th>
              </tr>
            </thead>
            <tbody>
              ${sbRows}
              <tr class="total-row">
                <td colspan="2">סה״כ מרפסות תלויות (${sb.count || 0} מרפסות)</td>
                <td>${fmtNum(sb.total_sqm)} מ״ר</td>
              </tr>
            </tbody>
          </table>
        </div>
      </details>

      <!-- 4. Facades Breakdown by Direction -->
      <details class="doc-collapsible-details">
        <summary>
          <span>🧱 סך שטחי חזיתות בחלוקה לחזיתות השונות (${fmtNum(fac.total_sqm)} מ״ר)</span>
          <span>▾</span>
        </summary>
        <div class="doc-collapsible-body">
          <table class="mini-quant-table">
            <thead>
              <tr>
                <th>חזית וכיוון</th>
                <th>מידות (א׳×ג׳)</th>
                <th>שטח ברוטו</th>
                <th>פתחים מול אטום</th>
              </tr>
            </thead>
            <tbody>
              ${facRows}
              <tr class="total-row">
                <td colspan="2">סה״כ שטחי חזיתות החוץ</td>
                <td>${fmtNum(fac.total_sqm)} מ״ר (100%)</td>
                <td>זיגוג: ${fmtNum(fac.total_glazing_sqm)} מ״ר | אטום: ${fmtNum(fac.total_opaque_sqm)} מ״ר</td>
              </tr>
            </tbody>
          </table>
        </div>
      </details>

      <!-- 5. Flooring Areas Breakdown (Full Floors: Apartments / Public / Balconies) -->
      <details class="doc-collapsible-details" open>
        <summary>
          <span>🛋️ שטחי ריצוף קומות מלאות — דירות (${fmtNum(flr.total_apartments_flooring_sqm)}) / ציבורי (${fmtNum(flr.total_public_flooring_sqm)}) / מרפסות (${fmtNum(flr.total_balconies_flooring_sqm)} מ״ר)</span>
          <span>▾</span>
        </summary>
        <div class="doc-collapsible-body">
          <div style="font-size:10.5px;color:#334155;margin-bottom:6px;">
            ${flr.summary_note || ''}
          </div>
          <table class="mini-quant-table">
            <thead>
              <tr>
                <th>קומה ומפלס</th>
                <th>ריצוף דירות</th>
                <th>ריצוף ציבורי</th>
                <th>ריצוף מרפסות</th>
                <th>סה״כ בקומה</th>
              </tr>
            </thead>
            <tbody>
              ${flrRows}
              <tr class="total-row">
                <td>סה״כ ריצוף בפרויקט</td>
                <td>${fmtNum(flr.total_apartments_flooring_sqm)} מ״ר<div style="font-size:9px;font-weight:600;">יבש: ${fmtNum(flr.total_apartments_dry_sqm)} | רטוב: ${fmtNum(flr.total_apartments_wet_sqm)}</div></td>
                <td>${fmtNum(flr.total_public_flooring_sqm)} מ״ר</td>
                <td>${fmtNum(flr.total_balconies_flooring_sqm)} מ״ר</td>
                <td>${fmtNum(flr.grand_total_flooring_sqm)} מ״ר</td>
              </tr>
            </tbody>
          </table>
        </div>
      </details>
      <!-- 6. Design Optimization & Value Engineering (בדיקת ייעול תכנון וחיסכון בעלויות) -->
      <details class="doc-collapsible-details" open style="border-color:#059669;">
        <summary style="background:#ecfdf5;color:#065f46;">
          <span>💰 מודל החיסכון המוצע (איפה ואיך על התכנית) — ${fmtNum(optKpis.grand_total_direct_saving_ils)} ₪</span>
          <span>▾</span>
        </summary>
        <div class="doc-collapsible-body">
          <div style="background:#f0fdf4;border:1px solid #86efac;padding:6px 8px;border-radius:6px;margin-bottom:7px;font-size:10.5px;font-weight:700;color:#065f46;">
            🛡️ ${(opt.zero_damage_guarantees || {}).guarantee_statement || ''}
          </div>
          <table class="mini-quant-table">
            <thead>
              <tr>
                <th>ציר ייעול תכנוני</th>
                <th>היקף שטח</th>
                <th>תעריף</th>
                <th>חיסכון כספי</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>1. שטח עילי (ליבה/קרקע/גג)</strong></td>
                <td>${fmtNum(optKpis.above_ground_saved_sqm)} מ״ר</td>
                <td>6,200 ₪/מ״ר</td>
                <td style="font-weight:900;color:#047857;">${fmtNum(optKpis.above_ground_saving_ils)} ₪</td>
              </tr>
              <tr>
                <td><strong>2. מרתף חניון תת-קרקעי</strong></td>
                <td>${fmtNum(optKpis.underground_saved_sqm)} מ״ר</td>
                <td>3,500 ₪/מ״ר</td>
                <td style="font-weight:900;color:#047857;">${fmtNum(optKpis.underground_saving_ils)} ₪</td>
              </tr>
              <tr>
                <td><strong>3. חיפוי יבש (700) ← טיח (300)</strong></td>
                <td>${fmtNum(optKpis.facade_converted_to_plaster_sqm)} מ״ר</td>
                <td>400 ₪/מ״ר</td>
                <td style="font-weight:900;color:#047857;">${fmtNum(optKpis.facade_saving_ils)} ₪</td>
              </tr>
              <tr>
                <td><strong>4. הקטנת מסדרונות לחדרים</strong></td>
                <td>+${fmtNum(optKpis.internal_reclaimed_living_sqm)} מ״ר</td>
                <td>השבחת פנים</td>
                <td style="font-weight:800;color:#1e3a8a;">הגדלת חדרים/סלון</td>
              </tr>
              <tr class="total-row" style="background:#dcfce7;color:#065f46;">
                <td colspan="3">סה״כ פוטנציאל חיסכון ישיר בעלויות הבנייה</td>
                <td>${fmtNum(optKpis.grand_total_direct_saving_ils)} ₪</td>
              </tr>
            </tbody>
          </table>

          <div style="font-weight:800;color:#064e3b;margin:9px 0 5px 0;font-size:11.5px;">📍 מוקדי החיסכון על התכנית (לחץ להצגת איפה ואיך על התכנית):</div>
          <div class="inline-ve-hotspots-list">
            ${(data.notes || [])
              .filter((n) => n.is_value_eng)
              .map(
                (n) => `
              <div class="inline-ve-item" data-note-id="${n.id}" data-sheet-id="${n.sheet_id}">
                <div class="inline-ve-item-top">
                  <span class="inline-ve-badge">סיכה #${n.pin_num} · ${n.ve_callout_badge || n.measured}</span>
                  <button type="button" class="btn-locate-on-plan btn-locate-sm" data-note-id="${n.id}" data-sheet-id="${n.sheet_id}">📍 הצג על התכנית</button>
                </div>
                <div class="inline-ve-where"><strong>📍 איפה:</strong> ${n.where_on_plan || n.room_name}</div>
                <div class="inline-ve-how"><strong>🛠️ איך:</strong> ${n.how_to_execute || n.recommendation}</div>
              </div>`
              )
              .join('')}
          </div>

          <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:8px;">
            <button type="button" id="btn-inline-show-ve-on-plan" style="background:#047857;color:#fff;border:none;padding:7px;border-radius:6px;font-family:'Heebo',sans-serif;font-weight:800;font-size:11px;cursor:pointer;">
              🗺️ הצג מודל חיסכון על התכנית
            </button>
            <button type="button" id="btn-inline-open-ve-modal" style="background:#0f172a;color:#34d399;border:1px solid #10b981;padding:7px;border-radius:6px;font-family:'Heebo',sans-serif;font-weight:800;font-size:11px;cursor:pointer;">
              🧮 סימולטור וטבלאות מלאות
            </button>
          </div>
        </div>
      </details>
    `;

    const inlineBtn = wrapper.querySelector('#btn-inline-open-modal');
    if (inlineBtn) {
      inlineBtn.addEventListener('click', () => openSummaryAreasModal(data));
    }

    const veCardBtn = wrapper.querySelector('#kpi-card-open-ve');
    if (veCardBtn) {
      veCardBtn.addEventListener('click', () => openValueEngineeringModal(data));
    }

    const veInlineBtn = wrapper.querySelector('#btn-inline-open-ve-modal');
    if (veInlineBtn) {
      veInlineBtn.addEventListener('click', () => openValueEngineeringModal(data));
    }

    const veShowOnPlanBtn = wrapper.querySelector('#btn-inline-show-ve-on-plan');
    if (veShowOnPlanBtn) {
      veShowOnPlanBtn.addEventListener('click', () => {
        const firstVe = (data.notes || []).find((n) => n.is_value_eng);
        if (firstVe) {
          focusSavingsItemOnPlan(firstVe.id, firstVe.sheet_id);
        }
      });
    }

    wrapper.querySelectorAll('.inline-ve-item, .btn-locate-on-plan').forEach((el) => {
      el.addEventListener('click', (e) => {
        e.stopPropagation();
        const nid = el.getAttribute('data-note-id');
        const sid = el.getAttribute('data-sheet-id');
        if (nid) focusSavingsItemOnPlan(nid, sid);
      });
    });

    return wrapper;
  }

  function openSummaryAreasModal(data) {
    if (!data || !data.project_data_summary || !summaryAreasModal) return;
    const pds = data.project_data_summary;
    const ag = pds.above_ground_areas || {};
    const ug = pds.underground_areas || {};
    const rt = pds.roof_terraces || {};
    const sb = pds.suspended_balconies || {};
    const fac = pds.facades || {};
    const flr = pds.flooring_areas || {};
    const opt = pds.design_optimization || {};
    const optKpis = opt.executive_kpis || {};
    const sdoc = pds.summary_document || {};

    summaryModalTitle.textContent = sdoc.document_title || `מסמך סיכום הערות ונתוני פרויקט — ${data.project_name}`;
    if (pds.summary_doc_url && summaryModalPrintLink) {
      summaryModalPrintLink.href = pds.summary_doc_url;
    }

    const agRows = (ag.by_floor || [])
      .map(
        (f) => `
        <tr>
          <td><strong>${f.floor_label}</strong></td>
          <td>${f.elevation || ''}</td>
          <td>${f.units_count !== undefined ? f.units_count : '-'}</td>
          <td>${f.usage_description || ''}</td>
          <td>${fmtNum(f.apartments_sqm)} מ״ר</td>
          <td>${fmtNum(f.core_service_sqm)} מ״ר</td>
          <td><strong>${fmtNum(f.total_floor_sqm)} מ״ר</strong></td>
          <td>${f.pct_of_above_ground}%</td>
        </tr>`
      )
      .join('');

    const ugRows = (ug.by_floor || [])
      .map(
        (f) => `
        <tr>
          <td><strong>${f.floor_label}</strong></td>
          <td>${f.elevation || ''}</td>
          <td>${f.usage_description || ''}</td>
          <td><strong>${fmtNum(f.total_floor_sqm)} מ״ר</strong></td>
          <td>${f.pct_of_underground}%</td>
        </tr>`
      )
      .join('');

    const rtRows = (rt.breakdown || [])
      .map(
        (b) => `
        <tr>
          <td><strong>${b.floor_label}</strong></td>
          <td>${b.unit_label}</td>
          <td>${b.dimensions || ''}</td>
          <td><strong>${fmtNum(b.area_sqm)} מ״ר</strong></td>
        </tr>`
      )
      .join('');

    const sbRows = (sb.breakdown || [])
      .map(
        (b) => `
        <tr>
          <td><strong>${b.floor_label}</strong></td>
          <td>${b.unit_label}</td>
          <td>${b.count} מרפסות</td>
          <td>${fmtNum(b.unit_area_sqm)} מ״ר</td>
          <td>${b.dimensions || ''}</td>
          <td><strong>${fmtNum(b.total_area_sqm)} מ״ר</strong></td>
        </tr>`
      )
      .join('');

    const facRows = (fac.by_direction || [])
      .map(
        (d) => `
        <tr>
          <td><strong>${d.facade_name}</strong></td>
          <td>${d.direction}</td>
          <td>${fmtNum(d.length_m)} מ׳</td>
          <td>${fmtNum(d.height_m)} מ׳</td>
          <td><strong>${fmtNum(d.gross_area_sqm)} מ״ר</strong></td>
          <td>${d.pct_of_total}%</td>
          <td>${fmtNum(d.glazing_area_sqm)} מ״ר (${d.wwr_pct}%)</td>
          <td>${fmtNum(d.opaque_area_sqm)} מ״ר</td>
          <td>${d.materials_and_elements || ''}</td>
        </tr>`
      )
      .join('');

    const flrModalRows = (flr.by_floor || [])
      .map(
        (f) => `
        <tr>
          <td><strong>${f.floor_label}</strong></td>
          <td>${f.elevation || ''}</td>
          <td>${f.units_count !== undefined ? f.units_count : '-'}</td>
          <td>${fmtNum(f.apartments_dry_sqm)} מ״ר</td>
          <td>${fmtNum(f.apartments_wet_sqm)} מ״ר</td>
          <td style="font-weight:800;color:#1e3a8a;">${fmtNum(f.apartments_flooring_sqm)} מ״ר</td>
          <td style="font-weight:700;color:#0f766e;">${fmtNum(f.public_flooring_sqm)} מ״ר</td>
          <td style="font-weight:700;color:#b45309;">${fmtNum(f.balconies_flooring_sqm)} מ״ר</td>
          <td style="font-weight:900;background:#f1f5f9;">${fmtNum(f.total_floor_flooring_sqm)} מ״ר</td>
          <td>${f.notes || ''}</td>
        </tr>`
      )
      .join('');

    const proposalRows = (sdoc.improvement_proposals || [])
      .map(
        (p, idx) => `
        <tr>
          <td><strong>#${idx + 1}</strong></td>
          <td><span style="background:#fef3c7;color:#92400e;padding:2px 8px;border-radius:4px;font-weight:800;font-size:11px;">${p.priority}</span></td>
          <td><strong>${p.target}</strong></td>
          <td>${p.issue}</td>
          <td style="color:#1e3a8a;font-weight:700;">${p.proposal}</td>
          <td>${p.impact || ''}</td>
        </tr>`
      )
      .join('');

    const critList = (sdoc.critical_notes_summary || [])
      .map((c) => `<li style="margin-bottom:6px;line-height:1.45;">${c}</li>`)
      .join('');

    summaryModalBody.innerHTML = `
      <!-- Top 5 Quantitative KPI Boxes -->
      <div class="modal-kpi-strip">
        <div class="modal-kpi-box">
          <div class="k-title">🏢 סך שטחי בנייה עיליים</div>
          <div class="k-num">${fmtNum(ag.total_sqm)} מ״ר</div>
          <div class="k-desc">פלדלת: ${fmtNum(ag.net_apartments_sqm)} מ״ר | ליבה: ${fmtNum(ag.core_and_service_sqm)} מ״ר</div>
        </div>
        <div class="modal-kpi-box">
          <div class="k-title">🅿️ סך שטחי בנייה תת-קרקעיים</div>
          <div class="k-num">${fmtNum(ug.total_sqm)} מ״ר</div>
          <div class="k-desc">${ug.parking_spaces || 0} חניות · סה״כ בנוי: ${fmtNum(pds.total_built_area_sqm)} מ״ר</div>
        </div>
        <div class="modal-kpi-box">
          <div class="k-title">🌇 סך שטחי מרפסות גג</div>
          <div class="k-num">${fmtNum(rt.total_sqm)} מ״ר</div>
          <div class="k-desc">${rt.count || 0} מרפסות גג${rt.garden_terraces_sqm ? ` (+${fmtNum(rt.garden_terraces_sqm)} מ״ר גינות)` : ''}</div>
        </div>
        <div class="modal-kpi-box">
          <div class="k-title">🌿 סך שטחי מרפסות תלויות</div>
          <div class="k-num">${fmtNum(sb.total_sqm)} מ״ר</div>
          <div class="k-desc">${sb.count || 0} מרפסות זיזיות (+${fmtNum(sb.service_balconies_sqm)} מ״ר שירות)</div>
        </div>
        <div class="modal-kpi-box">
          <div class="k-title">🧱 סך שטחי חזיתות החוץ</div>
          <div class="k-num">${fmtNum(fac.total_sqm)} מ״ר</div>
          <div class="k-desc">פתחים: ${fmtNum(fac.total_glazing_sqm)} מ״ר (${fac.average_wwr_pct}%) | אטום: ${fmtNum(fac.total_opaque_sqm)} מ״ר</div>
        </div>
        <div class="modal-kpi-box">
          <div class="k-title">🛋️ סך ריצוף דירות (נטו)</div>
          <div class="k-num">${fmtNum(flr.total_apartments_flooring_sqm)} מ״ר</div>
          <div class="k-desc">יבש: ${fmtNum(flr.total_apartments_dry_sqm)} מ״ר | רטוב: ${fmtNum(flr.total_apartments_wet_sqm)} מ״ר</div>
        </div>
        <div class="modal-kpi-box">
          <div class="k-title">🏛️ סך ריצוף ציבורי ומרפסות</div>
          <div class="k-num">${fmtNum(flr.total_public_flooring_sqm)} מ״ר</div>
          <div class="k-desc">מרפסות: ${fmtNum(flr.total_balconies_flooring_sqm)} מ״ר · סה״כ: ${fmtNum(flr.grand_total_flooring_sqm)} מ״ר</div>
        </div>
      </div>

      <!-- Section 1: Summary of Audit Notes & Actionable Improvement Proposals -->
      <div class="modal-section-card">
        <h3>📋 1. מסמך סיכום הערות בקרת איכות והצעות אופרטיביות לשיפור</h3>
        <div class="sec-note" style="background:#eff6ff;border-right:4px solid #2563eb;padding:10px 14px;border-radius:6px;color:#1e3a8a;font-weight:700;">
          ${sdoc.overall_verdict || ''}
        </div>
        <h4 style="font-size:14px;font-weight:800;margin:10px 0 6px 0;color:#0f172a;">📌 ריכוז הערות מרכזיות בבדיקת המודל:</h4>
        <ul style="padding-right:20px;margin-bottom:14px;color:#334155;font-size:13px;">
          ${critList}
        </ul>
        <h4 style="font-size:14px;font-weight:800;margin:10px 0 8px 0;color:#0f172a;">🛠️ טבלת הצעות לשיפור תכנוני והנדסי:</h4>
        <table class="modal-data-table">
          <thead>
            <tr>
              <th>#</th>
              <th>עדיפות</th>
              <th>מוקד / קומה / דירה</th>
              <th>תיאור ההערה / הליקוי</th>
              <th>הצעה מעשית לשיפור</th>
              <th>השפעה ותועלת</th>
            </tr>
          </thead>
          <tbody>${proposalRows}</tbody>
        </table>
      </div>

      <!-- Section 2: Above-Ground Construction Areas (Total & Breakdown by Floor) -->
      <div class="modal-section-card">
        <h3>🏢 2. סך שטחי בנייה עיליים — סך הכל וחלוקה לקומות (${fmtNum(ag.total_sqm)} מ״ר)</h3>
        <div class="sec-note">${ag.summary_note || ''}</div>
        <table class="modal-data-table">
          <thead>
            <tr>
              <th>קומה</th>
              <th>מפלס וגובה</th>
              <th>יח״ד</th>
              <th>פירוט שימושים ויחידות דיור בקומה</th>
              <th>שטח דירות (פלדלת)</th>
              <th>שטח ליבה ושירות</th>
              <th>סה״כ שטח קומה ברוטו</th>
              <th>% מהעילי</th>
            </tr>
          </thead>
          <tbody>
            ${agRows}
            <tr class="total-row">
              <td colspan="2">סה״כ שטחי בנייה עיליים</td>
              <td>${pds.apartments_count || ''} יח״ד</td>
              <td>כל הקומות העיליות (${pds.floors_above_ground || ''} קומות + גג)</td>
              <td>${fmtNum(ag.net_apartments_sqm)} מ״ר</td>
              <td>${fmtNum(ag.core_and_service_sqm)} מ״ר</td>
              <td>${fmtNum(ag.total_sqm)} מ״ר</td>
              <td>100.0%</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Section 3: Underground Construction Areas -->
      <div class="modal-section-card">
        <h3>🅿️ 3. סך שטחי בנייה תת-קרקעיים (${fmtNum(ug.total_sqm)} מ״ר)</h3>
        <div class="sec-note">${ug.summary_note || ''} · יחס חניה: ${ug.parking_ratio || ''}</div>
        <table class="modal-data-table">
          <thead>
            <tr>
              <th>קומת מרתף</th>
              <th>מפלס וגובה</th>
              <th>פירוט חניות, מיסעות, מחסנים וחדרים טכניים</th>
              <th>שטח ברוטו במ״ר</th>
              <th>% מהתת-קרקעי</th>
            </tr>
          </thead>
          <tbody>
            ${ugRows}
            <tr class="total-row">
              <td colspan="3">סה״כ שטחי בנייה תת-קרקעיים (${ug.parking_spaces || 0} חניות)</td>
              <td>${fmtNum(ug.total_sqm)} מ״ר</td>
              <td>100.0%</td>
            </tr>
            <tr class="total-row" style="background:#bfdbfe;">
              <td colspan="3">סה״כ שטח בנוי כולל בפרויקט (עילי + תת-קרקעי)</td>
              <td colspan="2">${fmtNum(pds.total_built_area_sqm)} מ״ר</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Section 4: Roof Terraces & Suspended Balconies -->
      <div class="modal-section-card">
        <h3>🌿 4. סך שטחי מרפסות גג (${fmtNum(rt.total_sqm)} מ״ר) ומרפסות תלויות (${fmtNum(sb.total_sqm)} מ״ר)</h3>
        <div class="sec-note">${rt.summary_note || ''} | ${sb.summary_note || ''}</div>
        <h4 style="font-size:14px;font-weight:800;margin:6px 0;color:#0f172a;">א. מרפסות גג (פנטהאוזים, דופלקסים ודירות גג):</h4>
        <table class="modal-data-table" style="margin-bottom:14px;">
          <thead>
            <tr>
              <th>קומה</th>
              <th>שיוך דירה / טיפוס</th>
              <th>מידות ופירוט הנדסי</th>
              <th>שטח במ״ר</th>
            </tr>
          </thead>
          <tbody>
            ${rtRows}
            <tr class="total-row">
              <td colspan="3">סה״כ שטחי מרפסות גג (${rt.count || 0} מרפסות גג)</td>
              <td>${fmtNum(rt.total_sqm)} מ״ר</td>
            </tr>
          </tbody>
        </table>

        <h4 style="font-size:14px;font-weight:800;margin:6px 0;color:#0f172a;">ב. מרפסות תלויות / זיזיות (קומות טיפוסיות):</h4>
        <table class="modal-data-table">
          <thead>
            <tr>
              <th>קומות</th>
              <th>טיפוס דירה</th>
              <th>כמות מרפסות</th>
              <th>שטח מרפסת יחידה</th>
              <th>מידות ועומק</th>
              <th>סה״כ שטח במ״ר</th>
            </tr>
          </thead>
          <tbody>
            ${sbRows}
            <tr class="total-row">
              <td colspan="5">סה״כ שטחי מרפסות תלויות / זיזיות (${sb.count || 0} מרפסות)</td>
              <td>${fmtNum(sb.total_sqm)} מ״ר</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Section 5: Total Facade Areas by Direction -->
      <div class="modal-section-card">
        <h3>🧱 5. סך שטחי חזיתות בחלוקה לחזיתות השונות (${fmtNum(fac.total_sqm)} מ״ר)</h3>
        <div class="sec-note">${fac.summary_note || ''}</div>
        <table class="modal-data-table">
          <thead>
            <tr>
              <th>שם החזית והפניה</th>
              <th>כיוון</th>
              <th>אורך פיתוח</th>
              <th>גובה משוקלל</th>
              <th>שטח חזית ברוטו</th>
              <th>% מסך החזיתות</th>
              <th>שטח פתחים וזיגוג (WWR)</th>
              <th>שטח קירות אטומים/חיפוי</th>
              <th>חומרי גמר ואלמנטים בחזית</th>
            </tr>
          </thead>
          <tbody>
            ${facRows}
            <tr class="total-row">
              <td colspan="4">סה״כ שטחי חזיתות החוץ (4 חזיתות)</td>
              <td>${fmtNum(fac.total_sqm)} מ״ר</td>
              <td>100.0%</td>
              <td>${fmtNum(fac.total_glazing_sqm)} מ״ר (${fac.average_wwr_pct}%)</td>
              <td>${fmtNum(fac.total_opaque_sqm)} מ״ר</td>
              <td>מעטפת חוץ מלאה</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Section 6: Flooring Areas (Full Floors — Apartments / Public / Balconies) -->
      <div class="modal-section-card">
        <h3>🛋️ 6. שטחי ריצוף נטו (שטחי רצפה של קומות מלאות) — דירות / ציבורי / מרפסות (${fmtNum(flr.grand_total_flooring_sqm)} מ״ר)</h3>
        <div class="sec-note">${flr.summary_note || ''}</div>
        <table class="modal-data-table">
          <thead>
            <tr>
              <th>קומה (קומה מלאה)</th>
              <th>מפלס</th>
              <th>יח״ד</th>
              <th>ריצוף דירות (יבש)</th>
              <th>ריצוף דירות (רטוב)</th>
              <th>סה״כ ריצוף דירות בקומה</th>
              <th>ריצוף ציבורי בקומה</th>
              <th>ריצוף מרפסות בקומה</th>
              <th>סה״כ ריצוף בקומה מלאה</th>
              <th>פירוט והערות ריצוף</th>
            </tr>
          </thead>
          <tbody>
            ${flrModalRows}
            <tr class="total-row">
              <td colspan="2">סה״כ שטחי ריצוף בפרויקט (כל הקומות)</td>
              <td>${pds.apartments_count || ''} יח״ד</td>
              <td>${fmtNum(flr.total_apartments_dry_sqm)} מ״ר</td>
              <td>${fmtNum(flr.total_apartments_wet_sqm)} מ״ר</td>
              <td>${fmtNum(flr.total_apartments_flooring_sqm)} מ״ר</td>
              <td>${fmtNum(flr.total_public_flooring_sqm)} מ״ר</td>
              <td>${fmtNum(flr.total_balconies_flooring_sqm)} מ״ר</td>
              <td style="background:#bfdbfe;color:#1e3a8a;font-weight:900;">${fmtNum(flr.grand_total_flooring_sqm)} מ״ר</td>
              <td>סך ריצוף דירות + ציבורי + מרפסות</td>
            </tr>
          </tbody>
        </table>
      </div>
    `;

    summaryAreasModal.classList.remove('hidden');
  }

  // =========================================================================
  // 4.5 VALUE ENGINEERING & DESIGN OPTIMIZATION MODAL + LIVE SIMULATOR
  // =========================================================================
  function openValueEngineeringModal(data) {
    if (!data || !data.project_data_summary || !valueEngModal) return;
    const pds = data.project_data_summary;
    const opt = pds.design_optimization || {};
    const kpis = opt.executive_kpis || {};
    const guar = opt.zero_damage_guarantees || {};
    const agOpt = opt.above_ground_optimization || {};
    const ugOpt = opt.underground_optimization || {};
    const facOpt = opt.facade_cladding_optimization || {};
    const aptOpt = opt.internal_apartment_optimization || {};

    valueEngModalTitle.textContent = `💰 בדיקת ייעול תכנון והנדסת ערך (Value Engineering) — ${data.project_name}`;

    const agOptRows = (agOpt.items || [])
      .map(
        (item, idx) => `
        <tr>
          <td><strong>#${idx + 1}</strong></td>
          <td><strong>${item.floor_or_zone}</strong></td>
          <td>${fmtNum(item.current_sqm)} מ״ר</td>
          <td>${fmtNum(item.optimal_sqm)} מ״ר</td>
          <td style="font-weight:800;color:#047857;">${fmtNum(item.saved_sqm)} מ״ר</td>
          <td style="font-weight:900;background:#dcfce7;color:#065f46;">${fmtNum(item.cost_saving_ils)} ₪</td>
          <td>
            <div><strong>📍 איפה בתכנית:</strong> ${item.floor_or_zone}</div>
            <div style="margin-top:3px;"><strong>🛠️ איך מבצעים:</strong> ${item.engineering_action}</div>
            <div style="font-size:11px;color:#047857;margin-top:3px;font-weight:700;">🛡️ נשמר במלואו: ${item.preserved_utilities}</div>
          </td>
          <td style="text-align:center;">
            ${item.note_id ? `<button type="button" class="btn-locate-on-plan" data-note-id="${item.note_id}" data-sheet-id="${item.sheet_id}">📍 הצג איפה ואיך על התכנית (#${item.pin_num})</button>` : '-'}
          </td>
        </tr>`
      )
      .join('');

    const ugOptRows = (ugOpt.items || [])
      .map(
        (item, idx) => `
        <tr>
          <td><strong>#${idx + 1}</strong></td>
          <td><strong>${item.zone}</strong></td>
          <td>${fmtNum(item.current_sqm)} מ״ר (${ugOpt.current_sqm_per_stall} מ״ר/חניה)</td>
          <td>${fmtNum(item.optimal_sqm)} מ״ר (${ugOpt.optimized_sqm_per_stall} מ״ר/חניה)</td>
          <td style="font-weight:800;color:#047857;">${fmtNum(item.saved_sqm)} מ״ר</td>
          <td style="font-weight:900;background:#dcfce7;color:#065f46;">${fmtNum(item.cost_saving_ils)} ₪</td>
          <td>
            <div><strong>📍 איפה בתכנית:</strong> ${item.zone}</div>
            <div style="margin-top:3px;"><strong>🛠️ איך מבצעים:</strong> ${item.engineering_action}</div>
            <div style="font-size:11px;color:#0369a1;margin-top:3px;font-weight:700;">🅿️ שמירת חניות: ${item.parking_spaces_preserved}</div>
          </td>
          <td style="text-align:center;">
            ${item.note_id ? `<button type="button" class="btn-locate-on-plan" data-note-id="${item.note_id}" data-sheet-id="${item.sheet_id}">📍 הצג איפה ואיך על התכנית (#${item.pin_num})</button>` : '-'}
          </td>
        </tr>`
      )
      .join('');

    const facOptRows = (facOpt.by_facade || [])
      .map(
        (f) => `
        <tr>
          <td><strong>${f.facade_name}</strong></td>
          <td>${f.direction}</td>
          <td>${fmtNum(f.gross_area_sqm)} מ״ר</td>
          <td>${fmtNum(f.glazing_area_sqm)} מ״ר</td>
          <td><strong>${fmtNum(f.opaque_area_sqm)} מ״ר</strong></td>
          <td>${fmtNum(f.current_dry_cladding_sqm)} מ״ר</td>
          <td style="font-weight:800;color:#0284c7;">${fmtNum(f.recommended_converted_to_plaster_sqm)} מ״ר</td>
          <td><strong>${f.optimized_dry_pct}% יבש / ${f.optimized_plaster_pct}% טיח</strong></td>
          <td style="font-weight:900;background:#dcfce7;color:#065f46;">${fmtNum(f.cost_saving_ils)} ₪</td>
          <td>
            <div><strong>📍 איפה בחזית:</strong> קו מתאר ${f.facade_name} (${f.direction})</div>
            <div style="margin-top:2px;"><strong>🛠️ איך:</strong> ${f.strategy_note}</div>
          </td>
          <td style="text-align:center;">
            ${f.note_id ? `<button type="button" class="btn-locate-on-plan" data-note-id="${f.note_id}" data-sheet-id="${f.sheet_id}">📍 הצג על התכנית (#${f.pin_num})</button>` : '-'}
          </td>
        </tr>`
      )
      .join('');

    const facScenariosRows = (facOpt.scenarios || [])
      .map(
        (s) => `
        <tr>
          <td><strong>${s.title}</strong></td>
          <td>${fmtNum(s.converted_sqm)} מ״ר</td>
          <td>${s.new_dry_pct}% חיפוי יבש (700 ₪) / ${s.new_plaster_pct}% טיח (300 ₪)</td>
          <td style="font-weight:900;color:#047857;background:#ecfdf5;">${fmtNum(s.saving_ils)} ₪</td>
        </tr>`
      )
      .join('');

    const aptOptRows = (aptOpt.items || [])
      .map(
        (a, idx) => `
        <tr>
          <td><strong>#${idx + 1}</strong></td>
          <td><strong>${a.typology}</strong></td>
          <td>${fmtNum(a.current_corridor_sqm)} מ״ר</td>
          <td>${fmtNum(a.optimal_corridor_sqm)} מ״ר</td>
          <td style="font-weight:800;color:#1d4ed8;">+${fmtNum(a.reclaimed_sqm_per_unit)} מ״ר לדירה</td>
          <td style="font-weight:900;background:#dbeafe;color:#1e3a8a;">+${fmtNum(a.total_reclaimed_sqm)} מ״ר (${a.units_count} דירות)</td>
          <td>
            <div><strong>📍 איפה בדירה:</strong> מסדרון פנים ב-${a.typology} ← מומר ל-${a.target_rooms_benefiting}</div>
            <div style="margin-top:3px;"><strong>🛠️ איך מבצעים:</strong> ${a.engineering_action}</div>
            <div style="margin-top:3px;color:#0369a1;"><strong>🪟 ייעול פתחים:</strong> ${a.openings_optimization}</div>
          </td>
          <td style="text-align:center;">
            ${a.note_id ? `<button type="button" class="btn-locate-on-plan" data-note-id="${a.note_id}" data-sheet-id="${a.sheet_id}">📍 הצג איפה ואיך על התכנית (#${a.pin_num})</button>` : '-'}
          </td>
        </tr>`
      )
      .join('');

    const baseAgSaved = Number(kpis.above_ground_saved_sqm || 0);
    const baseUgSaved = Number(kpis.underground_saved_sqm || 0);
    const totalOpaque = Number(facOpt.total_opaque_wall_sqm || 1000);
    const recConvPct = totalOpaque > 0 ? Math.round((Number(kpis.facade_converted_to_plaster_sqm || 0) / totalOpaque) * 100) : 35;

    valueEngModalBody.innerHTML = `
      <!-- Zero-Damage Guarantee Banner -->
      <div class="ve-guarantee-banner">
        <div>
          <strong>🛡️ התחייבות תכנונית (Zero-Impact on Value):</strong>
          ${guar.guarantee_statement || ''}
        </div>
        <div style="white-space:nowrap;background:#059669;color:#fff;padding:6px 12px;border-radius:8px;font-weight:900;">
          0% פגיעה בשטח דירות | 100% שמירת חניות וארונות שירות
        </div>
      </div>

      <!-- Top 5 Value Engineering KPI Boxes -->
      <div class="modal-kpi-strip">
        <div class="modal-kpi-box" style="border-top-color:#059669;background:#ecfdf5;">
          <div class="k-title" style="color:#065f46;">💰 סה״כ פוטנציאל חיסכון ישיר</div>
          <div class="k-num" style="color:#047857;" id="ve-kpi-grand-total">${fmtNum(kpis.grand_total_direct_saving_ils)} ₪</div>
          <div class="k-desc" style="color:#065f46;">עילי + חניון + חזיתות (ללא פגיעה בדירות)</div>
        </div>
        <div class="modal-kpi-box" style="border-top-color:#2563eb;">
          <div class="k-title">🏢 חיסכון שטח עילי (6,200 ₪/מ״ר)</div>
          <div class="k-num" id="ve-kpi-ag-ils">${fmtNum(kpis.above_ground_saving_ils)} ₪</div>
          <div class="k-desc">צמצום ${fmtNum(kpis.above_ground_saved_sqm)} מ״ר ליבה ושירות (יחס ליבה ${kpis.current_core_share_pct}% ← ${kpis.optimized_core_share_pct}%)</div>
        </div>
        <div class="modal-kpi-box" style="border-top-color:#0284c7;">
          <div class="k-title">🅿️ חיסכון מרתף חניון (3,500 ₪/מ״ר)</div>
          <div class="k-num" id="ve-kpi-ug-ils">${fmtNum(kpis.underground_saving_ils)} ₪</div>
          <div class="k-desc">צמצום ${fmtNum(kpis.underground_saved_sqm)} מ״ר (${kpis.current_basement_sqm_per_stall} ← ${kpis.optimized_basement_sqm_per_stall} מ״ר/חניה)</div>
        </div>
        <div class="modal-kpi-box" style="border-top-color:#d97706;">
          <div class="k-title">🧱 חיפוי יבש מול טיח (400 ₪/מ״ר)</div>
          <div class="k-num" id="ve-kpi-fac-ils">${fmtNum(kpis.facade_saving_ils)} ₪</div>
          <div class="k-desc">המרת <span id="ve-kpi-fac-sqm">${fmtNum(kpis.facade_converted_to_plaster_sqm)}</span> מ״ר מחיפוי יבש (700 ₪) לטיח (300 ₪)</div>
        </div>
        <div class="modal-kpi-box" style="border-top-color:#7c3aed;">
          <div class="k-title">🛋️ השבחת שטח אפקטיבי בדירות</div>
          <div class="k-num" style="color:#6d28d9;">+${fmtNum(kpis.internal_reclaimed_living_sqm)} מ״ר</div>
          <div class="k-desc">המרת מסדרונות ומעברים לחדרי מגורים וסלון</div>
        </div>
      </div>

      <!-- INTERACTIVE VALUE ENGINEERING & CLADDING SIMULATOR -->
      <div class="ve-simulator-box">
        <div class="ve-sim-header">
          <div>
            <div class="ve-sim-title">🧮 סימולטור חיסכון אינטראקטיבי — התאמת שטחים, יחס חיפוי יבש/טיח ומחירי יחידה</div>
            <div style="font-size:12px;color:#94a3b8;margin-top:2px;">הזז את המחוונים כדי לבחון תרחישי ייעול שונים של שטח עילי (6,200 ₪/מ״ר), שטח חניון (3,500 ₪/מ״ר) והמרת חיפוי יבש לטיח (700 ₪ לעומת 300 ₪ למ״ר)</div>
          </div>
          <div class="ve-sim-total-pill" id="ve-sim-live-total">
            סה״כ חיסכון בסימולציה: ${fmtNum(kpis.grand_total_direct_saving_ils)} ₪
          </div>
        </div>

        <div class="ve-sim-controls-grid">
          <div class="ve-sim-control-card">
            <label>
              <span>🏢 שטח עילי נחסך (6,200 ₪/מ״ר):</span>
              <strong id="sim-lbl-ag-sqm">${baseAgSaved} מ״ר</strong>
            </label>
            <input type="range" id="sim-range-ag-sqm" min="0" max="${Math.max(150, Math.round(baseAgSaved * 1.6))}" step="1" value="${baseAgSaved}" />
            <div class="sim-sub-val" id="sim-val-ag-ils">חיסכון עילי: ${fmtNum(baseAgSaved * 6200)} ₪</div>
          </div>

          <div class="ve-sim-control-card">
            <label>
              <span>🅿️ שטח מרתף חניון נחסך (3,500 ₪/מ״ר):</span>
              <strong id="sim-lbl-ug-sqm">${baseUgSaved} מ״ר</strong>
            </label>
            <input type="range" id="sim-range-ug-sqm" min="0" max="${Math.max(220, Math.round(baseUgSaved * 1.6))}" step="1" value="${baseUgSaved}" />
            <div class="sim-sub-val" id="sim-val-ug-ils">חיסכון חניון: ${fmtNum(baseUgSaved * 3500)} ₪</div>
          </div>

          <div class="ve-sim-control-card">
            <label>
              <span>🧱 % המרה מחיפוי יבש לטיח (מתוך ${fmtNum(totalOpaque)} מ״ר אטום):</span>
              <strong id="sim-lbl-fac-pct">${recConvPct}% (${fmtNum(kpis.facade_converted_to_plaster_sqm)} מ״ר)</strong>
            </label>
            <input type="range" id="sim-range-fac-pct" min="0" max="75" step="1" value="${recConvPct}" />
            <div class="sim-sub-val" id="sim-val-fac-ils">חיסכון חזיתות (400 ₪/מ״ר): ${fmtNum(kpis.facade_saving_ils)} ₪</div>
          </div>
        </div>
      </div>

      <!-- Pillar 1: Above-Ground Building Volume Optimization -->
      <div class="modal-section-card">
        <h3>🏢 1. ייעול נפחיות הבניין ושטחים עיליים (6,200 ₪ למ״ר נחסך · ללא פגיעה בדירות או בארונות שירות)</h3>
        <div class="sec-note">
          שטח בנייה עילי נוכחי: <strong>${fmtNum(agOpt.current_total_above_ground_sqm)} מ״ר</strong> (מתוכו ליבה ושירות: <strong>${fmtNum(agOpt.current_core_and_service_sqm)} מ״ר = ${kpis.current_core_share_pct}%</strong>) ·
          שטח אופטימלי לאחר ייעול: <strong>${fmtNum(agOpt.optimized_total_above_ground_sqm)} מ״ר</strong> (ליבה: <strong>${fmtNum(agOpt.optimized_core_and_service_sqm)} מ״ר = ${kpis.optimized_core_share_pct}%</strong>) ·
          חיסכון כולל: <strong style="color:#047857;">${fmtNum(agOpt.total_saved_sqm)} מ״ר × 6,200 ₪ = ${fmtNum(agOpt.total_saving_ils)} ₪</strong>
        </div>
        <table class="modal-data-table">
          <thead>
            <tr>
              <th>#</th>
              <th>קומה / אזור בבניין</th>
              <th>שטח ליבה/שירות נוכחי</th>
              <th>שטח אופטימלי</th>
              <th>שטח נחסך</th>
              <th>חיסכון כספי (6,200 ₪/מ״ר)</th>
              <th>איפה ואיך בתכנית + שימושים נשמרים</th>
              <th>מיקום על התכנית</th>
            </tr>
          </thead>
          <tbody>
            ${agOptRows}
            <tr class="total-row">
              <td colspan="2">סה״כ ייעול בנייה עילית</td>
              <td>${fmtNum(agOpt.current_core_and_service_sqm)} מ״ר</td>
              <td>${fmtNum(agOpt.optimized_core_and_service_sqm)} מ״ר</td>
              <td>${fmtNum(agOpt.total_saved_sqm)} מ״ר</td>
              <td style="background:#dcfce7;color:#065f46;">${fmtNum(agOpt.total_saving_ils)} ₪</td>
              <td colspan="2">0% פגיעה בשטח הפלדלת של הדירות (${fmtNum(guar.apartment_saleable_area_preserved_sqm)} מ״ר נשמרים במלואם)</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pillar 2: Underground Parking & Basement Volume Optimization -->
      <div class="modal-section-card">
        <h3>🅿️ 2. ייעול נפחיות חניון תת-קרקעי ומרתפים (3,500 ₪ למ״ר נחסך · 100% שמירה על מצבת החניות)</h3>
        <div class="sec-note">
          שטח מרתף נוכחי: <strong>${fmtNum(ugOpt.current_total_underground_sqm)} מ״ר</strong> ל-<strong>${ugOpt.parking_spaces} חניות</strong> (<strong>${ugOpt.current_sqm_per_stall} מ״ר ברוטו לחניה</strong>) ·
          שטח מרתף אופטימלי: <strong>${fmtNum(ugOpt.optimized_total_underground_sqm)} מ״ר</strong> (<strong>${ugOpt.optimized_sqm_per_stall} מ״ר לחניה</strong>) ·
          חיסכון כולל: <strong style="color:#047857;">${fmtNum(ugOpt.total_saved_sqm)} מ״ר × 3,500 ₪ = ${fmtNum(ugOpt.total_saving_ils)} ₪</strong>
        </div>
        <table class="modal-data-table">
          <thead>
            <tr>
              <th>#</th>
              <th>מוקד במרתף החניון</th>
              <th>שטח מרתף נוכחי</th>
              <th>שטח מרתף אופטימלי</th>
              <th>שטח נחסך</th>
              <th>חיסכון כספי (3,500 ₪/מ״ר)</th>
              <th>איפה ואיך בתכנית המרתף + שמירת חניות</th>
              <th>מיקום על התכנית</th>
            </tr>
          </thead>
          <tbody>
            ${ugOptRows}
          </tbody>
        </table>
      </div>

      <!-- Pillar 3: Facade Cladding vs. Plaster Optimization -->
      <div class="modal-section-card">
        <h3>🧱 3. אופטימיזציית יחס חיפוי קשיח/יבש (700 ₪/מ״ר) לעומת טיח חוץ (300 ₪/מ״ר · חיסכון 400 ₪/מ״ר)</h3>
        <div class="sec-note">
          סך שטח חזיתות ברוטו: <strong>${fmtNum(facOpt.total_facade_gross_sqm)} מ״ר</strong> ·
          שטח פתחים וזיגוג: <strong>${fmtNum(facOpt.total_glazing_sqm)} מ״ר</strong> ·
          <strong>סך שטח קירות אטומים לחיפוי/טיח: ${fmtNum(facOpt.total_opaque_wall_sqm)} מ״ר</strong>.<br/>
          במצב הבסיס (${facOpt.baseline_dry_cladding_pct}% חיפוי יבש = ${fmtNum(facOpt.baseline_dry_cladding_sqm)} מ״ר, עלות ${fmtNum(facOpt.baseline_total_cost_ils)} ₪), המרה חכמה של <strong>${fmtNum(facOpt.recommended_converted_to_plaster_sqm)} מ״ר</strong> בעורף, בצדדים ובקירות פנים-מרפסות לטיח חוץ (${facOpt.optimized_dry_cladding_pct}% יבש / ${facOpt.optimized_plaster_pct}% טיח, עלות ${fmtNum(facOpt.optimized_total_cost_ils)} ₪) חוסכת ישירות <strong style="color:#047857;">${fmtNum(facOpt.recommended_saving_ils)} ₪</strong>!
        </div>

        <h4 style="font-size:13.5px;font-weight:800;margin:8px 0 6px 0;color:#0f172a;">א. ניתוח פרטני לפי כיווני החזיתות:</h4>
        <table class="modal-data-table" style="margin-bottom:14px;">
          <thead>
            <tr>
              <th>חזית</th>
              <th>כיוון</th>
              <th>שטח ברוטו</th>
              <th>פתחים/זיגוג</th>
              <th>שטח אטום</th>
              <th>חיפוי יבש נוכחי</th>
              <th>המרה מומלצת לטיח</th>
              <th>יחס חדש (יבש / טיח)</th>
              <th>חיסכון (400 ₪/מ״ר)</th>
              <th>איפה ואיך בחזיתות</th>
              <th>מיקום על התכנית</th>
            </tr>
          </thead>
          <tbody>
            ${facOptRows}
            <tr class="total-row">
              <td colspan="2">סה״כ 4 חזיתות</td>
              <td>${fmtNum(facOpt.total_facade_gross_sqm)} מ״ר</td>
              <td>${fmtNum(facOpt.total_glazing_sqm)} מ״ר</td>
              <td>${fmtNum(facOpt.total_opaque_wall_sqm)} מ״ר</td>
              <td>${fmtNum(facOpt.baseline_dry_cladding_sqm)} מ״ר</td>
              <td>${fmtNum(facOpt.recommended_converted_to_plaster_sqm)} מ״ר</td>
              <td>${facOpt.optimized_dry_cladding_pct}% יבש / ${facOpt.optimized_plaster_pct}% טיח</td>
              <td style="background:#dcfce7;color:#065f46;">${fmtNum(facOpt.recommended_saving_ils)} ₪</td>
              <td colspan="2">שמירת חזית רחוב ייצוגית ומסד בחיפוי יבש מלא</td>
            </tr>
          </tbody>
        </table>

        <h4 style="font-size:13.5px;font-weight:800;margin:8px 0 6px 0;color:#0f172a;">ב. השוואת 3 תרחישי יחס חיפוי קשיח לעומת טיח:</h4>
        <table class="modal-data-table">
          <thead>
            <tr>
              <th>תרחיש תכנוני</th>
              <th>שטח מומר מחיפוי יבש לטיח</th>
              <th>יחס חיפוי יבש (700 ₪) מול טיח (300 ₪)</th>
              <th>חיסכון כספי בפרויקט</th>
            </tr>
          </thead>
          <tbody>
            ${facScenariosRows}
          </tbody>
        </table>
      </div>

      <!-- Pillar 4: Internal Apartment Layout & Openings Optimization -->
      <div class="modal-section-card">
        <h3>🛋️ 4. ייעול תכנון פנימי בדירות — הקטנת מסדרונות לטובת חדרי מגורים ואופטימיזציית פתחים (+${fmtNum(aptOpt.total_reclaimed_effective_living_sqm)} מ״ר מושבחים)</h3>
        <div class="sec-note">
          שיפור השטחים האפקטיביים בתוך מעטפת הדירה הקיימת: קיצור זנבות מסדרון, איחוד חדרי ארונות צפופים לארונות קו-אפס, ואיזון מפתחי החלונות והוויטרינות.
        </div>
        <table class="modal-data-table">
          <thead>
            <tr>
              <th>#</th>
              <th>טיפוס דירה וקומות</th>
              <th>מסדרון נוכחי</th>
              <th>מסדרון יעיל</th>
              <th>תוספת שטח לחדרים (לדירה)</th>
              <th>סה״כ שטח מושבח בפרויקט</th>
              <th>איפה ואיך בתכנית הדירה + אופטימיזציית פתחים</th>
              <th>מיקום על התכנית</th>
            </tr>
          </thead>
          <tbody>
            ${aptOptRows}
            <tr class="total-row">
              <td colspan="5">סה״כ שטח מסדרונות המומר לשטח חדרי מגורים וסלון אפקטיבי בפרויקט</td>
              <td style="background:#dbeafe;color:#1e3a8a;">+${fmtNum(aptOpt.total_reclaimed_effective_living_sqm)} מ״ר</td>
              <td colspan="2">שיפור דרמטי ברוחב חדרי השינה, יחידות ההורים והסלונים ללא הגדלת שטח הברוטו</td>
            </tr>
          </tbody>
        </table>
      </div>
    `;

    // Wire up Live Interactive Simulator Sliders
    const rangeAg = valueEngModalBody.querySelector('#sim-range-ag-sqm');
    const rangeUg = valueEngModalBody.querySelector('#sim-range-ug-sqm');
    const rangeFac = valueEngModalBody.querySelector('#sim-range-fac-pct');

    function updateLiveSimulation() {
      const agSqm = Number(rangeAg ? rangeAg.value : baseAgSaved);
      const ugSqm = Number(rangeUg ? rangeUg.value : baseUgSaved);
      const facPct = Number(rangeFac ? rangeFac.value : recConvPct);

      const agIls = Math.round(agSqm * 6200);
      const ugIls = Math.round(ugSqm * 3500);
      const facConvSqm = Math.round(totalOpaque * (facPct / 100.0) * 10) / 10;
      const facIls = Math.round(facConvSqm * 400);
      const grandTotalIls = agIls + ugIls + facIls;

      const lblAg = valueEngModalBody.querySelector('#sim-lbl-ag-sqm');
      const valAg = valueEngModalBody.querySelector('#sim-val-ag-ils');
      const lblUg = valueEngModalBody.querySelector('#sim-lbl-ug-sqm');
      const valUg = valueEngModalBody.querySelector('#sim-val-ug-ils');
      const lblFac = valueEngModalBody.querySelector('#sim-lbl-fac-pct');
      const valFac = valueEngModalBody.querySelector('#sim-val-fac-ils');
      const liveTot = valueEngModalBody.querySelector('#ve-sim-live-total');

      if (lblAg) lblAg.textContent = `${fmtNum(agSqm)} מ״ר`;
      if (valAg) valAg.textContent = `חיסכון עילי: ${fmtNum(agIls)} ₪`;
      if (lblUg) lblUg.textContent = `${fmtNum(ugSqm)} מ״ר`;
      if (valUg) valUg.textContent = `חיסכון חניון: ${fmtNum(ugIls)} ₪`;
      if (lblFac) lblFac.textContent = `${facPct}% (${fmtNum(facConvSqm)} מ״ר)`;
      if (valFac) valFac.textContent = `חיסכון חזיתות (400 ₪/מ״ר): ${fmtNum(facIls)} ₪`;
      if (liveTot) liveTot.textContent = `סה״כ חיסכון בסימולציה: ${fmtNum(grandTotalIls)} ₪`;
    }

    if (rangeAg) rangeAg.addEventListener('input', updateLiveSimulation);
    if (rangeUg) rangeUg.addEventListener('input', updateLiveSimulation);
    if (rangeFac) rangeFac.addEventListener('input', updateLiveSimulation);

    // Wire up "הצג איפה ואיך על התכנית" buttons inside the modal tables
    valueEngModalBody.querySelectorAll('.btn-locate-on-plan').forEach((btn) => {
      btn.addEventListener('click', () => {
        const nid = btn.getAttribute('data-note-id');
        const sid = btn.getAttribute('data-sheet-id');
        if (nid) {
          focusSavingsItemOnPlan(nid, sid);
        }
      });
    });

    valueEngModal.classList.remove('hidden');
  }

  function renderDocumentSections(data) {
    docSectionsRoot.innerHTML = '';

    // Inject the Summary Document & Quantitative Areas/Facades Master Box at the top of every audited model
    const summaryMasterEl = buildInlineSummaryAndAreasElement(data);
    if (summaryMasterEl) {
      docSectionsRoot.appendChild(summaryMasterEl);
    }

    const sections = data.sections || [];
    const notes = data.notes || [];

    sections.forEach((sec) => {
      const secNotes = notes.filter((n) => n.section_id === sec.id && matchesFilter(n));
      if (secNotes.length === 0) return;

      const secBlock = document.createElement('div');
      secBlock.className = 'doc-section-block';

      const secHeader = document.createElement('div');
      secHeader.className = 'doc-section-header';
      secHeader.innerHTML = `
        <div class="doc-section-title">${sec.title}</div>
        <div class="doc-section-sub">${sec.subtitle || ''}</div>
        <div class="doc-section-intro">${sec.intro || ''}</div>
      `;
      secBlock.appendChild(secHeader);

      secNotes.forEach((note) => {
        const card = document.createElement('article');
        const isVe = Boolean(note.is_value_eng);
        card.className = `doc-note-card status-${note.status} ${isVe ? 'card-ve' : ''} ${note.id === activeNoteId ? 'active' : ''}`;
        card.dataset.noteId = note.id;
        card.id = `doc-note-${note.id}`;

        const veDetailsHtml = isVe
          ? `
          <div class="note-ve-box">
            <div class="note-ve-row"><strong>📍 איפה על התכנית:</strong> ${note.where_on_plan || note.room_name}</div>
            <div class="note-ve-row" style="margin-top:3px;"><strong>🛠️ איך מבצעים:</strong> ${note.how_to_execute || note.recommendation}</div>
          </div>`
          : `
          <div class="note-rec">
            <strong>💡 המלצה:</strong> ${note.recommendation}
          </div>`;

        card.innerHTML = `
          <div class="note-top-row">
            <div class="note-badges-right">
              <span class="note-pin-circle status-${note.status} ${isVe ? 'pin-circle-ve' : ''}">#${note.pin_num}</span>
              <span class="note-status-pill status-${note.status} ${isVe ? 'pill-ve' : ''}">${isVe ? `💰 ${note.ve_callout_badge || 'מוקד חיסכון'}` : (STATUS_LABELS[note.status] || note.status)}</span>
            </div>
            <span class="note-rule-tag">${note.rule_id}</span>
          </div>
          <div class="note-room-tag">📍 ${note.room_name}</div>
          <h3 class="note-title">${note.title}</h3>
          <div class="note-compare-strip">
            <span><strong>בתכנית:</strong> ${note.measured}</span>
            <span>|</span>
            <span><strong>תקן/יעד:</strong> ${note.benchmark}</span>
          </div>
          <p class="note-summary">${note.summary}</p>
          ${veDetailsHtml}
        `;

        // HOVER SYNCHRONIZATION: Hovering over the text note immediately shows it on the architectural plan!
        card.addEventListener('mouseenter', () => {
          highlightNote(note.id, { scrollDoc: false, switchSheet: true });
        });

        card.addEventListener('click', () => {
          highlightNote(note.id, { scrollDoc: false, switchSheet: true });
        });

        secBlock.appendChild(card);
      });

      docSectionsRoot.appendChild(secBlock);
    });
  }

  // =========================================================================
  // 5. BI-DIRECTIONAL HOVER & HIGHLIGHT SYNCHRONIZATION
  // =========================================================================
  function highlightNote(noteId, options = { scrollDoc: false, switchSheet: true }) {
    if (!currentProject || !noteId) return;
    const note = (currentProject.notes || []).find((n) => n.id === noteId);
    if (!note) return;

    activeNoteId = noteId;

    // 1. Switch floor sheet automatically if the hovered note belongs to a different sheet
    if (options.switchSheet !== false && note.sheet_id !== currentSheetId) {
      selectSheet(note.sheet_id, { keepNote: true });
    }

    // 2. Update active state in the Right-Hand Text Document
    document.querySelectorAll('.doc-note-card').forEach((card) => {
      const isMatch = card.dataset.noteId === noteId;
      card.classList.toggle('active', isMatch);
      if (isMatch && options.scrollDoc) {
        card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });

    // 3. Update active SVG Room Polygon, Pin & On-Plan Callout on the Left-Hand Architectural Plan
    renderVisualPlanAnnotations();

    // Update active state on the On-Plan Savings Navigator Bar chips
    document.querySelectorAll('.ve-hotspot-chip').forEach((chip) => {
      const isMatch = chip.dataset.noteId === noteId;
      chip.classList.toggle('active', isMatch);
      if (isMatch) {
        chip.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      }
    });

    // 4. Populate the Side Inspector Card (displayed beside the plan, never covering it)
    const isVe = Boolean(note.is_value_eng);
    fcPinBadge.textContent = `#${note.pin_num}`;
    fcStatusBadge.textContent = isVe ? `💰 מוקד חיסכון` : (STATUS_LABELS[note.status] || note.status);
    fcStatusBadge.className = `fc-status-badge status-${note.status} ${isVe ? 'status-VE' : ''}`;
    fcRuleBadge.textContent = note.rule_id;
    fcRoomName.textContent = `📍 ${note.typology} · ${note.room_name}`;
    fcTitle.textContent = note.title;
    fcMeasured.textContent = note.measured;
    fcBenchmark.textContent = note.benchmark;
    fcSummary.textContent = note.summary;
    fcRecommendation.textContent = note.recommendation;

    if (fcVeWhereHowBox) {
      if (isVe) {
        fcVeWhereHowBox.classList.remove('hidden');
        if (fcVeSavingBanner) {
          fcVeSavingBanner.textContent = `💰 חיסכון במוקד זה: ${note.ve_callout_badge || note.measured}`;
        }
        if (fcVeWhere) {
          fcVeWhere.textContent = note.where_on_plan || `${note.typology} — ${note.room_name}`;
        }
        if (fcVeHow) {
          fcVeHow.textContent = note.how_to_execute || note.recommendation;
        }
      } else {
        fcVeWhereHowBox.classList.add('hidden');
      }
    }

    floatingCard.classList.remove('hidden');
    floatingCard.style.left = '';
    floatingCard.style.top = '';

    // 5. Update Bottom HUD Bar
    hudActiveNoteText.textContent = isVe
      ? `💰 מוקד חיסכון #${note.pin_num} (${note.ve_callout_badge || ''}): איפה — ${note.where_on_plan || note.room_name}`
      : `הערה #${note.pin_num} [${note.room_name}]: ${note.title}`;
  }

  // =========================================================================
  // 6. ZOOM, PAN & UI EVENT LISTENERS
  // =========================================================================
  function updateStageTransform() {
    planStage.style.transform = `translate(${panX}px, ${panY}px) scale(${scale})`;
    zoomLevelLabel.textContent = `${Math.round(scale * 100)}%`;
  }

  function resetZoomAndPan() {
    scale = 1.0;
    panX = 0;
    panY = 0;
    updateStageTransform();
  }

  btnZoomIn.addEventListener('click', () => {
    scale = Math.min(3.2, +(scale + 0.2).toFixed(2));
    updateStageTransform();
  });

  btnZoomOut.addEventListener('click', () => {
    scale = Math.max(0.6, +(scale - 0.2).toFixed(2));
    updateStageTransform();
  });

  btnZoomReset.addEventListener('click', resetZoomAndPan);

  planViewport.addEventListener(
    'wheel',
    (e) => {
      e.preventDefault();
      const delta = e.deltaY < 0 ? 0.12 : -0.12;
      scale = Math.max(0.6, Math.min(3.5, +(scale + delta).toFixed(2)));
      updateStageTransform();
    },
    { passive: false }
  );

  planViewport.addEventListener('mousedown', (e) => {
    if (e.target.closest('.plan-pin') || e.target.closest('.ctrl-btn')) return;
    isDragging = true;
    dragStartX = e.clientX - panX;
    dragStartY = e.clientY - panY;
  });

  window.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    panX = e.clientX - dragStartX;
    panY = e.clientY - dragStartY;
    updateStageTransform();
  });

  window.addEventListener('mouseup', () => {
    isDragging = false;
  });

  // Toggle All Pins vs. Hover-Only Pin
  btnToggleAllPins.addEventListener('click', () => {
    showAllPins = !showAllPins;
    btnToggleAllPins.classList.toggle('active', showAllPins);
    btnToggleAllPins.textContent = showAllPins ? '📌 הצג כל ההערות' : '🎯 הצג רק הערה בריחוף';
    renderVisualPlanAnnotations();
  });

  // Toggle On-Plan Savings Mode ("הצג מודל חיסכון על התכנית - איפה ואיך")
  if (btnToggleVePlanMode) {
    btnToggleVePlanMode.addEventListener('click', () => {
      if (currentFilter === 'VE') {
        currentFilter = 'ALL';
        btnToggleVePlanMode.classList.remove('active');
      } else {
        currentFilter = 'VE';
        btnToggleVePlanMode.classList.add('active');
      }
      filterBtns.forEach((b) => b.classList.toggle('active', b.dataset.filter === currentFilter));
      if (currentProject) {
        renderDocumentSections(currentProject);
        renderVisualPlanAnnotations();
        if (currentFilter === 'VE') {
          const sheetVe = (currentProject.notes || []).find((n) => n.is_value_eng && n.sheet_id === currentSheetId);
          const anyVe = sheetVe || (currentProject.notes || []).find((n) => n.is_value_eng);
          if (anyVe) {
            highlightNote(anyVe.id, { scrollDoc: true, switchSheet: true });
          }
        }
      }
    });
  }

  // Filter Buttons in Document Panel
  filterBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      currentFilter = btn.dataset.filter || 'ALL';
      filterBtns.forEach((b) => b.classList.toggle('active', b === btn));
      if (btnToggleVePlanMode) {
        btnToggleVePlanMode.classList.toggle('active', currentFilter === 'VE');
      }
      if (currentProject) {
        renderDocumentSections(currentProject);
        renderVisualPlanAnnotations();
        if (currentFilter === 'VE') {
          const sheetVe = (currentProject.notes || []).find((n) => n.is_value_eng && n.sheet_id === currentSheetId);
          const anyVe = sheetVe || (currentProject.notes || []).find((n) => n.is_value_eng);
          if (anyVe) {
            highlightNote(anyVe.id, { scrollDoc: true, switchSheet: true });
          }
        }
      }
    });
  });

  // Search Form Submit
  searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    loadProjectAnalysis(queryInput.value);
  });

  // Quick Project Chips
  quickChipsContainer.addEventListener('click', (e) => {
    const chip = e.target.closest('.proj-chip');
    if (!chip) return;
    const q = chip.getAttribute('data-query');
    if (q) {
      loadProjectAnalysis(q);
    }
  });

  // Discovered Files Drawer Toggle
  btnToggleFiles.addEventListener('click', () => {
    filesDrawer.classList.toggle('hidden');
  });

  btnCloseFilesDrawer.addEventListener('click', () => {
    filesDrawer.classList.add('hidden');
  });

  // Summary & Quantitative Areas Modal Toggle
  if (btnOpenSummaryModal) {
    btnOpenSummaryModal.addEventListener('click', () => {
      if (currentProject) {
        openSummaryAreasModal(currentProject);
      }
    });
  }

  if (btnCloseSummaryModal) {
    btnCloseSummaryModal.addEventListener('click', () => {
      summaryAreasModal.classList.add('hidden');
    });
  }

  if (summaryAreasModal) {
    summaryAreasModal.addEventListener('click', (e) => {
      if (e.target === summaryAreasModal) {
        summaryAreasModal.classList.add('hidden');
      }
    });
  }

  // Value Engineering & Cost Optimization Modal Toggle
  if (btnOpenValueEngModal) {
    btnOpenValueEngModal.addEventListener('click', () => {
      if (currentProject) {
        openValueEngineeringModal(currentProject);
      }
    });
  }

  if (btnCloseValueEngModal) {
    btnCloseValueEngModal.addEventListener('click', () => {
      valueEngModal.classList.add('hidden');
    });
  }

  if (valueEngModal) {
    valueEngModal.addEventListener('click', (e) => {
      if (e.target === valueEngModal) {
        valueEngModal.classList.add('hidden');
      }
    });
  }

  // Optional File Upload Handler
  fileUploadInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    loadingTitle.textContent = `מעלה ומנתח את הקובץ "${file.name}"...`;
    loadingOverlay.classList.remove('hidden');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const resp = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await resp.json();
      if (!resp.ok || data.error) {
        throw new Error(data.error || 'שגיאה בניתוח הקובץ');
      }
      currentProject = data;
      renderProjectHeaderAndFiles(data);
      renderSheetTabs(data);
      const firstSheet = (data.sheets && data.sheets[0]) ? data.sheets[0].id : null;
      selectSheet(firstSheet, { keepNote: false });
      renderDocumentSections(data);
    } catch (err) {
      alert(`שגיאה: ${err.message}`);
    } finally {
      loadingOverlay.classList.add('hidden');
      fileUploadInput.value = '';
    }
  });

  // Initialize on Page Load with Pines 48
  loadProjectAnalysis('פינס 48');
})();
