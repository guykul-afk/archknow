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
  const hdrVeTotalBadge = document.getElementById('hdr-ve-total-badge');
  const valueEngModal = document.getElementById('value-eng-modal');
  const valueEngModalTitle = document.getElementById('value-eng-modal-title');
  const btnCloseValueEngModal = document.getElementById('btn-close-value-eng-modal');
  const valueEngModalBody = document.getElementById('value-eng-modal-body');

  const btnToggleMoreMenu = document.getElementById('btn-toggle-more-menu');
  const moreToolsDropdown = document.getElementById('more-tools-dropdown');
  const btnToggleLegend = document.getElementById('btn-toggle-legend');
  const legendPopoverBox = document.getElementById('legend-popover-box');

  const topCommandBar = document.getElementById('top-command-bar');
  const btnCollapseTopBar = document.getElementById('btn-collapse-top-bar');
  const btnExpandTopBar = document.getElementById('btn-expand-top-bar');
  const splitWorkspaceEl = document.getElementById('split-workspace');
  const btnCollapseDocPanel = document.getElementById('btn-collapse-doc-panel');
  const btnExpandDocPanel = document.getElementById('btn-expand-doc-panel');
  const btnFocusMode = document.getElementById('btn-focus-mode');
  const btnCenterOnPlan = document.getElementById('btn-center-on-plan');
  const hdrBreadcrumbSub = document.getElementById('hdr-breadcrumb-sub');

  const btnExportDecisions = document.getElementById('btn-export-decisions');
  const hdrDecisionsCount = document.getElementById('hdr-decisions-count');
  const btnCheck3dUpdate = document.getElementById('btn-check-3d-update');
  const hdr3dSyncBadge = document.getElementById('hdr-3d-sync-badge');
  const decisionsExportModal = document.getElementById('decisions-export-modal');
  const decisionsModalTitle = document.getElementById('decisions-modal-title');
  const decisionsModalBody = document.getElementById('decisions-modal-body');
  const btnCloseDecisionsModal = document.getElementById('btn-close-decisions-modal');
  const btnPrintDecisions = document.getElementById('btn-print-decisions');

  const workModesBar = document.getElementById('work-modes-bar');
  const workModeTabs = document.querySelectorAll('.work-mode-tab');
  const docSubfilterBar = document.getElementById('doc-subfilter-bar');
  const veSubfilterBar = document.getElementById('ve-subfilter-bar');
  const countOptEl = document.getElementById('count-opt');

  const planBodyLayoutEl = document.getElementById('plan-body-layout');
  const btnToggleSideDock = document.getElementById('btn-toggle-side-dock');
  const btnCloseSideDock = document.getElementById('btn-close-side-dock');
  const btnOpenVeCenterFromBar = document.getElementById('btn-open-ve-center-from-bar');

  const docProjectTitle = document.getElementById('doc-project-title');
  const docProjectSubtitle = document.getElementById('doc-project-subtitle');
  const docMetricsGrid = document.getElementById('doc-metrics-grid');
  const docSectionsRoot = document.getElementById('doc-sections-root');
  const countAllEl = document.getElementById('count-all');
  const countPolAllEl = document.getElementById('count-pol-all');
  const countPolNegEl = document.getElementById('count-pol-neg');
  const countPolPosEl = document.getElementById('count-pol-pos');
  const countCatAllEl = document.getElementById('count-cat-all');
  const countCatStdEl = document.getElementById('count-cat-std');
  const countCatArchEl = document.getElementById('count-cat-arch');
  const countCatTipEl = document.getElementById('count-cat-tip');
  const countVeAllEl = document.getElementById('count-ve-all');
  const countVeAgEl = document.getElementById('count-ve-ag');
  const countVeUgEl = document.getElementById('count-ve-ug');
  const countVeFacEl = document.getElementById('count-ve-fac');

  const polarityBtns = document.querySelectorAll('.polarity-btn');
  const catFilterBtns = document.querySelectorAll('.cat-filter-btn');
  const veCatBtns = document.querySelectorAll('.ve-cat-btn');
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

  const btnPrevNote = document.getElementById('btn-prev-note');
  const btnNextNote = document.getElementById('btn-next-note');
  const sideDockCounter = document.getElementById('side-dock-counter');
  const fcVisualDiagramBox = document.getElementById('fc-visual-diagram-box');
  const fcFourPillarsBox = document.getElementById('fc-four-pillars-box');

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
  const model3dStage = document.getElementById('model-3d-stage');
  const model3dIframe = document.getElementById('model-3d-iframe');
  const btnHdrToggle3d = document.getElementById('btn-hdr-toggle-3d');
  const vmodeBtns = document.querySelectorAll('#view-mode-switcher .vmode-btn');
  const zoomControlsGroup = document.getElementById('zoom-controls-group');
  let currentViewMode = '2d'; // '2d' | '3d' | 'split'
  let loaded3dProjectUrl = null;
  const hudActiveNoteText = document.getElementById('hud-active-note-text');
  const loadingOverlay = document.getElementById('loading-overlay');
  const loadingTitle = document.getElementById('loading-title');

  // Application State
  let currentProject = null;
  let currentSheetId = null;
  let currentWorkMode = 'FINDINGS'; // 'OVERVIEW' | 'FINDINGS' | 'OPTIMIZATION' | 'COMPARE'
  let currentFilter = 'ALL';
  let currentPolarity = 'ALL'; // 'ALL' | 'NEGATIVE' | 'POSITIVE'
  let currentCategory = 'ALL'; // 'ALL' | 'STANDARD' | 'ARCH_QUALITY' | 'INTERIOR_TIP'
  let currentVeCategory = 'ALL'; // 'ALL' | 'AG' | 'UG' | 'FAC'
  let activeNoteId = null;
  let hoveredNoteId = null;
  let showAllPins = true;
  let isFocusMode = false;

  const EXPLICIT_JS_CATEGORY_MAP = {
    'H44-W-01': 'ARCH_QUALITY', 'H44-W-02': 'INTERIOR_TIP', 'H44-W-03': 'INTERIOR_TIP',
    'H44-W-04': 'STANDARD', 'H44-W-05': 'STANDARD', 'H44-E-01': 'ARCH_QUALITY',
    'H44-E-02': 'INTERIOR_TIP', 'H44-PH-01': 'INTERIOR_TIP', 'H44-GND-01': 'STANDARD',
    'H44-BSM-01': 'STANDARD',
    'P48-B-01': 'INTERIOR_TIP', 'P48-B-02': 'INTERIOR_TIP', 'P48-B-03': 'ARCH_QUALITY',
    'P48-B-04': 'INTERIOR_TIP', 'P48-B-05': 'STANDARD', 'P48-B-06': 'ARCH_QUALITY',
    'P48-A-01': 'ARCH_QUALITY', 'P48-A-02': 'INTERIOR_TIP', 'P48-A-03': 'ARCH_QUALITY',
    'P48-A-04': 'INTERIOR_TIP', 'P48-A-05': 'STANDARD', 'P48-C-01': 'ARCH_QUALITY',
    'P48-C-02': 'INTERIOR_TIP', 'P48-C-03': 'ARCH_QUALITY', 'P48-C-04': 'STANDARD',
    'P48-C-05': 'INTERIOR_TIP', 'P48-CORE-01': 'STANDARD', 'P48-PB-01': 'INTERIOR_TIP',
    'P48-PC-01': 'ARCH_QUALITY', 'P48-F7-01': 'STANDARD', 'P48-ROOF-01': 'STANDARD',
    'P48-GND-01': 'ARCH_QUALITY', 'P48-GND-02': 'STANDARD', 'P48-GND-03': 'STANDARD',
    'P48-BSM-01': 'STANDARD',
    'KKL-PARK-01': 'STANDARD', 'KKL-PARK-02': 'STANDARD', 'KKL-E-01': 'ARCH_QUALITY',
    'KKL-E-02': 'INTERIOR_TIP', 'KKL-E-03': 'ARCH_QUALITY', 'KKL-B-01': 'INTERIOR_TIP',
    'KKL-B-02': 'STANDARD', 'KKL-B-03': 'INTERIOR_TIP', 'KKL-D-01': 'ARCH_QUALITY',
    'KKL-D-02': 'INTERIOR_TIP', 'KKL-CORE-01': 'STANDARD', 'KKL-PH-01': 'STANDARD',
    'KKL-GND-01': 'STANDARD',
    'YAT-N-01': 'ARCH_QUALITY', 'YAT-N-02': 'INTERIOR_TIP', 'YAT-N-03': 'INTERIOR_TIP',
    'YAT-S-01': 'INTERIOR_TIP', 'YAT-S-02': 'STANDARD', 'YAT-PH-01': 'INTERIOR_TIP',
    'YAT-GND-01': 'STANDARD', 'YAT-BSM-01': 'STANDARD',
    'KIT-37-NW': 'INTERIOR_TIP', 'KIT-37-NE': 'ARCH_QUALITY', 'KIT-37-SE': 'INTERIOR_TIP',
    'KIT-37-SW': 'STANDARD', 'KIT-39-W3': 'STANDARD', 'KIT-39-SW': 'ARCH_QUALITY',
    'KIT-PH-01': 'INTERIOR_TIP', 'KIT-BSM-01': 'STANDARD',
    'FB3-W-01': 'ARCH_QUALITY', 'FB3-W-02': 'INTERIOR_TIP', 'FB3-W-03': 'STANDARD',
    'FB3-E-01': 'INTERIOR_TIP', 'FB3-E-02': 'INTERIOR_TIP', 'FB3-PH-01': 'ARCH_QUALITY',
    'FB3-BSM-01': 'STANDARD',
  };

  const CATEGORY_HE_LABELS = {
    STANDARD: 'תקן',
    ARCH_QUALITY: 'איכות תכנון אדריכלי',
    INTERIOR_TIP: 'טיפ עיצוב פנים',
    SAVINGS: 'חיסכון',
  };

  function classifySystemNote(note) {
    if (!note) return { polarity: 'NEGATIVE', polarityHe: 'שלילי', category: 'ARCH_QUALITY', categoryHe: 'איכות תכנון אדריכלי' };
    if (note.is_value_eng) {
      return { polarity: 'SAVINGS', polarityHe: 'חיסכון', category: 'SAVINGS', categoryHe: 'חיסכון' };
    }
    const polarity = note.audit_polarity || (note.status === 'PASS' ? 'POSITIVE' : 'NEGATIVE');
    const polarityHe = polarity === 'POSITIVE' ? 'חיובי' : 'שלילי';
    let category = note.audit_category;
    if (!category || category === 'SAVINGS') {
      const nid = note.id || '';
      if (EXPLICIT_JS_CATEGORY_MAP[nid]) {
        category = EXPLICIT_JS_CATEGORY_MAP[nid];
      } else if (note.is_design_improvement) {
        category = 'ARCH_QUALITY';
      } else {
        const txt = `${note.rule_id || ''} ${note.title || ''} ${note.recommendation || ''}`.toLowerCase();
        if (note.status === 'FAIL' || ['ת״י', 'פקע״ר', 'פיקוד העורף', 'חניונים', 'רישוי', 'תקנות', 'b1.15', 'b1.30', '1918', '1142', '2481'].some((k) => txt.includes(k))) {
          category = 'STANDARD';
        } else if (['nkba', 'אי מטבח', 'ארון', 'דלת כיס', 'pocket', 'ריהוט', 'מיטה', 'שולחן', 'תאורה', 'boverket', 'din 18040'].some((k) => txt.includes(k))) {
          category = 'INTERIOR_TIP';
        } else {
          category = 'ARCH_QUALITY';
        }
      }
    }
    const categoryHe = CATEGORY_HE_LABELS[category] || 'איכות תכנון אדריכלי';
    return { polarity, polarityHe, category, categoryHe };
  }

  // Persistent Architect Decisions Store (localStorage)
  const DECISIONS_STORAGE_KEY = 'archicheck_decisions_v5';
  let decisionsMap = {};
  try {
    const savedDec = localStorage.getItem(DECISIONS_STORAGE_KEY);
    if (savedDec) decisionsMap = JSON.parse(savedDec) || {};
  } catch (e) {
    decisionsMap = {};
  }

  function getNoteDecision(noteId) {
    if (!currentProject || !noteId) return null;
    const key = `${currentProject.project_id || currentProject.project_name}_${noteId}`;
    return decisionsMap[key] || null;
  }

  function setNoteDecision(noteId, statusVal) {
    if (!currentProject || !noteId) return;
    const key = `${currentProject.project_id || currentProject.project_name}_${noteId}`;
    if (!statusVal || decisionsMap[key] === statusVal) {
      delete decisionsMap[key];
    } else {
      decisionsMap[key] = statusVal;
    }
    try {
      localStorage.setItem(DECISIONS_STORAGE_KEY, JSON.stringify(decisionsMap));
    } catch (e) {
      // ignore storage quota errors
    }
    updateDecisionsCountBadge();
  }

  function updateDecisionsCountBadge() {
    if (!hdrDecisionsCount || !currentProject) return;
    const prefix = `${currentProject.project_id || currentProject.project_name}_`;
    const count = Object.keys(decisionsMap).filter((k) => k.startsWith(prefix) && decisionsMap[k]).length;
    hdrDecisionsCount.textContent = count;
  }

  const DECISION_LABELS = {
    TODO: { label: 'לטיפול', cls: 'dec-todo' },
    VERIFIED: { label: 'נבדק', cls: 'dec-verified' },
    APPROVED: { label: 'אושר', cls: 'dec-approved' },
    REJECTED: { label: 'נדחה', cls: 'dec-rejected' },
  };

  // Pan & Zoom State
  let scale = 1.0;
  let panX = 0;
  let panY = 0;
  let isDragging = false;
  let dragStartX = 0;
  let dragStartY = 0;

  const STATUS_LABELS = {
    PASS: 'תקין',
    WARN: 'לבדיקה',
    FAIL: 'ליקוי',
  };

  // =========================================================================
  // 1. FETCH & ANALYZE PROJECT ACROSS ALL FOLDERS
  // =========================================================================
  async function loadProjectAnalysis(queryStr) {
    const cleanQuery = (queryStr || 'חפץ חיים 44').trim();
    queryInput.value = cleanQuery;

    // Update active state on quick chips
    document.querySelectorAll('.proj-chip').forEach((chip) => {
      const cq = (chip.getAttribute('data-query') || '').trim();
      chip.classList.toggle('active', cq === cleanQuery || cleanQuery.includes(cq));
    });

    loadingTitle.textContent = `טוען ומנתח את הפרויקט "${cleanQuery}"...`;
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
        let staticFile = 'hafetz44.json';
        if (['פאירברג', 'פאיירברג', 'פיארברג', 'feierberg', 'fairberg', 'feirberg', '6387'].some((k) => q_low.includes(k))) staticFile = 'feierberg3.json';
        else if (['יטקובסקי', 'yatkovski', '7א'].some((k) => q_low.includes(k))) staticFile = 'yatkovski7.json';
        else if (['קיטרוני', 'קטרוני', 'kitroni', '37', '39'].some((k) => q_low.includes(k))) staticFile = 'kitroni37.json';
        else if (['חפץ', 'חיים', 'hafetz', '44'].some((k) => q_low.includes(k))) staticFile = 'hafetz44.json';
        else if (['קקל', 'קק"ל', 'קק״ל', 'kkl', '10'].some((k) => q_low.includes(k))) staticFile = 'kkl10.json';
        else if (['פינס', 'pines', '48'].some((k) => q_low.includes(k))) staticFile = 'pines48.json';

        const staticResp = await fetch(`/api/${staticFile}`);
        if (!staticResp.ok) {
          throw new Error(`שגיאת שרת (${staticResp.status})`);
        }
        data = await staticResp.json();
      }

      if (data && Array.isArray(data.notes)) {
        data.notes = data.notes.filter(
          (n) => !String(n.id || '').endsWith('-3D-SYNC') && !String(n.rule_id || '').includes('3D_BIM_FULL_AUDIT')
        );
      }

      currentProject = data;
      activeNoteId = null;
      userExplicitlySelectedNote = false;
      hoveredNoteId = null;
      currentFilter = 'ALL';
      currentPolarity = 'ALL';
      currentCategory = 'ALL';
      currentVeCategory = 'ALL';
      currentWorkMode = 'FINDINGS';
      workModeTabs.forEach((t) => t.classList.toggle('active', t.dataset.mode === currentWorkMode));
      if (docSubfilterBar) docSubfilterBar.classList.remove('hidden');
      if (veSubfilterBar) veSubfilterBar.classList.add('hidden');
      polarityBtns.forEach((b) => b.classList.toggle('active', b.dataset.polarity === 'ALL'));
      catFilterBtns.forEach((b) => b.classList.toggle('active', b.dataset.category === 'ALL'));
      veCatBtns.forEach((b) => b.classList.toggle('active', b.dataset.veCat === 'ALL'));
      if (btnToggleVePlanMode) btnToggleVePlanMode.classList.remove('active');
      if (vePlanBar) vePlanBar.classList.add('hidden');
      if (moreToolsDropdown) moreToolsDropdown.classList.add('hidden');
      if (legendPopoverBox) legendPopoverBox.classList.add('hidden');

      // Keep Left Analysis Drawer closed initially so drawing gets maximum space
      toggleSideDock(false);

      renderProjectHeaderAndFiles(data);
      updateDecisionsCountBadge();
      renderSheetTabs(data);
      renderVePlanBar(data);
      renderDocumentSections(data);

      // Select first sheet by default WITHOUT auto-opening the left inspector drawer
      const firstSheet = (data.sheets && data.sheets[0]) ? data.sheets[0].id : null;
      selectSheet(firstSheet, { keepNote: true });
    } catch (err) {
      console.error('Analysis error:', err);
      hudActiveNoteText.textContent = `שגיאה בטעינת הפרויקט: ${err.message}`;
    } finally {
      loadingOverlay.classList.add('hidden');
    }
  }

  function updateSystemFilterCounts(data) {
    if (!data) return;
    const notes = data.notes || [];
    const systemNotes = notes.filter((n) => !n.is_value_eng);
    const veNotes = notes.filter((n) => Boolean(n.is_value_eng));

    const negNotes = systemNotes.filter((n) => classifySystemNote(n).polarity === 'NEGATIVE');
    const posNotes = systemNotes.filter((n) => classifySystemNote(n).polarity === 'POSITIVE');

    if (countAllEl) countAllEl.textContent = systemNotes.length;
    if (countOptEl) countOptEl.textContent = veNotes.length;

    if (countPolAllEl) countPolAllEl.textContent = systemNotes.length;
    if (countPolNegEl) countPolNegEl.textContent = negNotes.length;
    if (countPolPosEl) countPolPosEl.textContent = posNotes.length;

    // Dynamic sub-category counts within the currently selected Polarity (הכל / שלילי / חיובי)
    const polarityScopedNotes = currentPolarity === 'NEGATIVE'
      ? negNotes
      : currentPolarity === 'POSITIVE'
        ? posNotes
        : systemNotes;

    const stdCount = polarityScopedNotes.filter((n) => classifySystemNote(n).category === 'STANDARD').length;
    const archCount = polarityScopedNotes.filter((n) => classifySystemNote(n).category === 'ARCH_QUALITY').length;
    const tipCount = polarityScopedNotes.filter((n) => classifySystemNote(n).category === 'INTERIOR_TIP').length;

    if (countCatAllEl) countCatAllEl.textContent = polarityScopedNotes.length;
    if (countCatStdEl) countCatStdEl.textContent = stdCount;
    if (countCatArchEl) countCatArchEl.textContent = archCount;
    if (countCatTipEl) countCatTipEl.textContent = tipCount;

    // Dedicated Savings tab counts
    if (countVeAllEl) countVeAllEl.textContent = veNotes.length;
    if (countVeAgEl) countVeAgEl.textContent = veNotes.filter((n) => n.ve_category === 'AG').length;
    if (countVeUgEl) countVeUgEl.textContent = veNotes.filter((n) => n.ve_category === 'UG').length;
    if (countVeFacEl) countVeFacEl.textContent = veNotes.filter((n) => n.ve_category === 'FAC').length;
  }

  // =========================================================================
  // 2. RENDER HEADER, EXECUTIVE SUMMARY STRIP & DISCOVERED FILES
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

    // 3D BIM Viewer Button
    const resolved3dUrl = (data.viewer_3d_url && data.viewer_3d_url.startsWith('/'))
      ? data.viewer_3d_url
      : (data.project_id ? `/models/${data.project_id}` : null);
    data._resolved_3d_url = resolved3dUrl;
    if (currentViewMode !== '2d') {
      ensure3dModelLoaded(true);
    } else {
      loaded3dProjectUrl = null;
    }
    if (btnOpen3dViewer) {
      if (resolved3dUrl) {
        btnOpen3dViewer.href = resolved3dUrl;
        btnOpen3dViewer.classList.remove('hidden');
      } else {
        btnOpen3dViewer.classList.add('hidden');
      }
    }
    // Summary & Quantitative Data Document Button + Unified Header Savings Badge
    const pds = data.project_data_summary;
    const optKpis = (pds && pds.design_optimization && pds.design_optimization.executive_kpis) || {};
    if (optKpis.grand_total_direct_saving_ils !== undefined && hdrVeTotalBadge) {
      hdrVeTotalBadge.textContent = `${fmtNum(optKpis.grand_total_direct_saving_ils)} ₪`;
    }
    if (pds && pds.summary_doc_url && btnOpenSummaryDoc) {
      btnOpenSummaryDoc.href = pds.summary_doc_url;
      btnOpenSummaryDoc.classList.remove('hidden');
    } else if (btnOpenSummaryDoc) {
      btnOpenSummaryDoc.classList.add('hidden');
    }

    // Counts for filter & mode buttons
    const notes = data.notes || [];
    const systemNotes = notes.filter((n) => !n.is_value_eng);
    const veCount = notes.filter((n) => Boolean(n.is_value_eng)).length;
    const negCount = systemNotes.filter((n) => classifySystemNote(n).polarity === 'NEGATIVE').length;
    const posCount = systemNotes.filter((n) => classifySystemNote(n).polarity === 'POSITIVE').length;

    updateSystemFilterCounts(data);

    // Clean Executive Score + Findings Breakdown Strip + 3D Base Model Audit Status
    const overallScore = data.overall_score || ((data.metrics && data.metrics[0] && data.metrics[0].value) ? data.metrics[0].value.replace('/100', '') : '90.0');
    const syncSt = data.model_3d_sync_status || (pds && pds.model_3d_sync_status) || {};
    const hashShort = syncSt.base_model_hash_short ? syncSt.base_model_hash_short.slice(0, 8) : 'מאומת';
    const revNum = syncSt.audit_revision || 1;
    const wasUpdated = Boolean(syncSt.was_updated_and_reaudited);
    const total3dChecks = (syncSt.bim_3d_checks_summary && syncSt.bim_3d_checks_summary.total_checks) || 0;

    if (hdr3dSyncBadge) {
      hdr3dSyncBadge.textContent = wasUpdated ? `עודכן! סבב #${revNum}` : `#${hashShort.slice(0, 6)} · סבב #${revNum}`;
      hdr3dSyncBadge.style.background = wasUpdated ? '#dcfce7' : '';
      hdr3dSyncBadge.style.color = wasUpdated ? '#166534' : '';
    }

    docMetricsGrid.innerHTML = `
      <div class="exec-score-strip">
        <div class="exec-score-main">
          <span class="exec-score-num">${overallScore}</span>
          <span class="exec-score-lbl">ציון</span>
        </div>
        <div class="exec-score-divider"></div>
        <div class="exec-score-summary">
          <div class="exec-summary-sub">
            <span class="strip-stat-neg">${negCount} שלילי</span> ·
            <span class="strip-stat-pos">${posCount} חיובי</span> ·
            <span class="strip-stat-ve">${veCount} חיסכון</span>
          </div>
        </div>
      </div>
      <div id="model-3d-sync-strip" style="margin-top:6px;padding:6px 9px;border-radius:8px;border:1px solid ${wasUpdated ? '#86efac' : '#cbd5e1'};background:${wasUpdated ? '#f0fdf4' : '#f8fafc'};display:flex;align-items:center;justify-content:space-between;gap:8px;font-size:11.5px;">
        <div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="${syncSt.status_message_he || 'המודל התלת-ממדי הבסיסי מאומת ומסונכרן'}">
          <strong>${wasUpdated ? '🟢 מודל 3D עודכן — הורצה בדיקה מלאה' : '🧊 מודל 3D בסיסי מנוטר'}</strong>
          <span style="color:#475569;margin-right:4px;">· חתימה <code>#${hashShort}</code> · סבב #${revNum}${total3dChecks ? ` · ${total3dChecks} בדיקות 3D` : ''}</span>
        </div>
        <button type="button" id="btn-inline-reaudit-3d" style="flex-shrink:0;padding:3px 8px;border-radius:6px;border:1px solid #2563eb;background:#eff6ff;color:#1d4ed8;font-family:inherit;font-size:11px;font-weight:700;cursor:pointer;" title="בדוק אם מודל ה-3D הבסיסי שונה או עודכן והרץ בדיקה תכנונית מלאה חדשה">
          🔄 בדוק / הרץ בקרה חדשה
        </button>
      </div>
    `;

    const btnInlineReaudit3d = document.getElementById('btn-inline-reaudit-3d');
    if (btnInlineReaudit3d) {
      btnInlineReaudit3d.addEventListener('click', () => trigger3dModelCheckAndReaudit(true));
    }

    // Discovered files across folders
    const files = data.discovered_files || [];
    filesCountBadge.textContent = files.length;
    filesDrawerSubtitle.textContent = `(${files.length})`;
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
        <span>${sh.title}</span>
        <span class="sheet-tab-count">${sheetNotesCount}</span>
      `;
      btn.addEventListener('click', () => {
        selectSheet(sh.id, { keepNote: true });
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

    // Update top header breadcrumb
    if (hdrBreadcrumbSub) {
      hdrBreadcrumbSub.textContent = `${currentProject.project_name || ''} · ${sheet.title}`;
    }

    // Update active tab button
    document.querySelectorAll('.sheet-tab-btn').forEach((btn) => {
      btn.classList.toggle('active', btn.dataset.sheetId === sheetId);
    });

    if (sheetChanged) {
      planImage.src = sheet.image_url;
      resetZoomAndPan();
    }

    hudSheetBadge.textContent = `${sheet.title} (${sheet.sheet_code || ''})`;
    postMessageTo3D({ type: 'ARCHICHECK_SELECT_SHEET', sheetId: sheetId });
    renderVisualPlanAnnotations();

    if (!options.keepNote) {
      const firstSheetNote = (currentProject.notes || []).find((n) => n.sheet_id === sheetId && matchesFilter(n));
      if (firstSheetNote) {
        highlightNote(firstSheetNote.id, { scrollDoc: false, switchSheet: false, openDock: false });
      }
    }
  }

  function renderVePlanBar(data) {
    if (!vePlanBar || !vePlanHotspotsList) return;
    const notes = (data.notes || []).filter((n) => n.is_value_eng || n.is_design_improvement);
    const sheetsMap = {};
    (data.sheets || []).forEach((s) => {
      sheetsMap[s.id] = s.title;
    });

    const pds = data.project_data_summary || {};
    const opt = pds.design_optimization || {};
    const optKpis = opt.executive_kpis || {};
    const ca = opt.contour_audit_summary || {};
    if (vePlanBarTotal) {
      vePlanBarTotal.innerHTML = `חיסכון: <strong>${fmtNum(optKpis.grand_total_direct_saving_ils)} ₪</strong> (-${fmtNum(ca.total_verified_contour_saved_sqm)} מ״ר)`;
    }

    vePlanHotspotsList.innerHTML = '';

    notes.forEach((n) => {
      const chip = document.createElement('button');
      chip.type = 'button';
      chip.className = `ve-hotspot-chip ${n.id === activeNoteId ? 'active' : ''}`;
      chip.dataset.noteId = n.id;
      chip.dataset.sheetId = n.sheet_id;
      chip.innerHTML = `
        <span class="ve-chip-pin">#${n.pin_num}</span>
        <span>${n.room_name}</span>
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

    const targetNote = (currentProject.notes || []).find((n) => n.id === noteId);
    if (targetNote && targetNote.is_value_eng) {
      currentVeCategory = 'ALL';
      veCatBtns.forEach((b) => b.classList.toggle('active', b.dataset.veCat === 'ALL'));
      switchWorkMode('OPTIMIZATION');
    } else if (targetNote) {
      const cls = classifySystemNote(targetNote);
      currentPolarity = cls.polarity;
      currentCategory = cls.category;
      polarityBtns.forEach((b) => b.classList.toggle('active', b.dataset.polarity === currentPolarity));
      catFilterBtns.forEach((b) => b.classList.toggle('active', b.dataset.category === currentCategory));
      updateSystemFilterCounts(currentProject);
      switchWorkMode('FINDINGS');
    }

    if (sheetId && sheetId !== currentSheetId) {
      selectSheet(sheetId, { keepNote: true });
    }
    if (noteId) {
      highlightNote(noteId, { scrollDoc: true, switchSheet: true, openDock: true, zoomTo: true });
    } else {
      renderVisualPlanAnnotations();
    }
  }

  function matchesFilter(note) {
    if (!note) return false;

    // 1. Separated Savings Tab ("חיסכון"): strictly Value Engineering notes
    if (currentWorkMode === 'OPTIMIZATION') {
      if (!note.is_value_eng) return false;
      if (currentVeCategory !== 'ALL' && note.ve_category !== currentVeCategory) return false;
      return true;
    }

    // 2. System Findings Tab ("הערות מערכת"): strictly non-VE system notes, filtered by שלילי/חיובי and תקן / איכות תכנון אדריכלי / טיפ עיצוב פנים
    if (currentWorkMode === 'FINDINGS') {
      if (note.is_value_eng) return false;
      const cls = classifySystemNote(note);
      if (currentPolarity !== 'ALL' && cls.polarity !== currentPolarity) return false;
      if (currentCategory !== 'ALL' && cls.category !== currentCategory) return false;
      return true;
    }

    // 3. Overview or Compare Mode
    if (currentFilter === 'VE') return Boolean(note.is_value_eng);
    return true;
  }

  function appendSvgArrowVector(svgEl, x1, y1, x2, y2) {
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', x1);
    line.setAttribute('y1', y1);
    line.setAttribute('x2', x2);
    line.setAttribute('y2', y2);
    line.setAttribute('class', 'svg-contour-vector-line');
    svgEl.appendChild(line);

    const dx = x2 - x1;
    const dy = y2 - y1;
    const len = Math.hypot(dx, dy) || 1;
    const ux = dx / len;
    const uy = dy / len;
    const headLen = 1.35;
    const headHalfW = 0.75;
    const bx = x2 - ux * headLen;
    const by = y2 - uy * headLen;
    const px1 = bx - uy * headHalfW;
    const py1 = by + ux * headHalfW;
    const px2 = bx + uy * headHalfW;
    const py2 = by - ux * headHalfW;

    const head = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
    head.setAttribute('points', `${x2},${y2} ${px1},${py1} ${px2},${py2}`);
    head.setAttribute('class', 'svg-contour-vector-head');
    svgEl.appendChild(head);
  }

  function renderVisualPlanAnnotations() {
    if (!currentProject) return;
    planSvgOverlay.innerHTML = '';
    planPinsLayer.innerHTML = '';

    const sheetNotes = (currentProject.notes || []).filter(
      (n) => n.sheet_id === currentSheetId && matchesFilter(n)
    );

    const hasSelectionOnSheet = sheetNotes.some((n) => n.id === activeNoteId);

    sheetNotes.forEach((note) => {
      const isNoteActive = note.id === activeNoteId;
      const isNoteHovered = note.id === hoveredNoteId;
      const isDimmed = hasSelectionOnSheet && !isNoteActive && !isNoteHovered;
      const isVe = Boolean(note.is_value_eng);
      const isImp = Boolean(note.is_design_improvement);

      // 1. Clean SVG Room/Contour Zone Outline on Plan (no text over the drawing!)
      const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      rect.setAttribute('x', note.x_pct);
      rect.setAttribute('y', note.y_pct);
      rect.setAttribute('width', note.w_pct);
      rect.setAttribute('height', note.h_pct);
      rect.setAttribute(
        'class',
        `room-zone-rect zone-${note.status} ${isVe ? 'zone-VE' : ''} ${isImp ? 'zone-IMP' : ''} ${isNoteActive ? 'active-zone' : ''} ${isNoteHovered ? 'hover-zone' : ''} ${isDimmed ? 'dimmed-zone' : ''}`
      );
      rect.dataset.noteId = note.id;

      if (!showAllPins && !isNoteActive && currentFilter !== 'VE' && currentFilter !== 'DESIGN_IMP') {
        rect.style.opacity = '0';
      }

      rect.addEventListener('click', (e) => {
        e.stopPropagation();
        highlightNote(note.id, { scrollDoc: true, switchSheet: false, openDock: true, zoomTo: true });
      });
      planSvgOverlay.appendChild(rect);

      // 1B. If this is the active VE Contour Reduction note (AG or UG), draw Before vs. After geometric contraction vectors on the original plan!
      if (isNoteActive && isVe && (note.ve_category === 'AG' || note.ve_category === 'UG')) {
        const overlayZones = note.plan_overlay_zones || (note.visual_explanation && note.visual_explanation.plan_overlay_zones) || null;
        const beforeBox = (overlayZones && overlayZones.before_contour_rect) || {
          x_pct: Number(note.x_pct),
          y_pct: Number(note.y_pct),
          w_pct: Number(note.w_pct),
          h_pct: Number(note.h_pct),
        };
        const x = Number(beforeBox.x_pct);
        const y = Number(beforeBox.y_pct);
        const w = Number(beforeBox.w_pct);
        const h = Number(beforeBox.h_pct);
        const insetX = Math.max(1.4, w * 0.14);
        const insetY = Math.max(1.4, h * 0.14);

        rect.setAttribute('x', x);
        rect.setAttribute('y', y);
        rect.setAttribute('width', w);
        rect.setAttribute('height', h);
        rect.setAttribute('class', 'svg-contour-before-rect');

        const afterBox = (overlayZones && overlayZones.after_contour_rect) || {
          x_pct: +(x + insetX).toFixed(2),
          y_pct: +(y + insetY).toFixed(2),
          w_pct: +Math.max(2, w - insetX * 2).toFixed(2),
          h_pct: +Math.max(2, h - insetY * 2).toFixed(2),
        };

        const afterRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        afterRect.setAttribute('x', Number(afterBox.x_pct).toFixed(2));
        afterRect.setAttribute('y', Number(afterBox.y_pct).toFixed(2));
        afterRect.setAttribute('width', Number(afterBox.w_pct).toFixed(2));
        afterRect.setAttribute('height', Number(afterBox.h_pct).toFixed(2));
        afterRect.setAttribute('class', 'svg-contour-after-rect');
        planSvgOverlay.appendChild(afterRect);

        // If Underground (UG) or Above-Ground (AG) note has Protected Zone & Utility/Relocation Zones, render them on the original plan!
        if ((note.ve_category === 'UG' || note.ve_category === 'AG') && overlayZones) {
          if (overlayZones.protected_ramp_maneuver_rect) {
            const pr = overlayZones.protected_ramp_maneuver_rect;
            const protRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
            protRect.setAttribute('x', Number(pr.x_pct).toFixed(2));
            protRect.setAttribute('y', Number(pr.y_pct).toFixed(2));
            protRect.setAttribute('width', Number(pr.w_pct).toFixed(2));
            protRect.setAttribute('height', Number(pr.h_pct).toFixed(2));
            protRect.setAttribute('class', 'svg-protected-ramp-rect');
            planSvgOverlay.appendChild(protRect);
          }
          if (overlayZones.under_ramp_utility_rect) {
            const ur = overlayZones.under_ramp_utility_rect;
            const utilRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
            utilRect.setAttribute('x', Number(ur.x_pct).toFixed(2));
            utilRect.setAttribute('y', Number(ur.y_pct).toFixed(2));
            utilRect.setAttribute('width', Number(ur.w_pct).toFixed(2));
            utilRect.setAttribute('height', Number(ur.h_pct).toFixed(2));
            utilRect.setAttribute('class', 'svg-under-ramp-util-rect');
            planSvgOverlay.appendChild(utilRect);
          }
          if (overlayZones.relocated_parking_target_rect) {
            const rp = overlayZones.relocated_parking_target_rect;
            const relRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
            relRect.setAttribute('x', Number(rp.x_pct).toFixed(2));
            relRect.setAttribute('y', Number(rp.y_pct).toFixed(2));
            relRect.setAttribute('width', Number(rp.w_pct).toFixed(2));
            relRect.setAttribute('height', Number(rp.h_pct).toFixed(2));
            relRect.setAttribute('class', 'svg-relocated-parking-rect');
            planSvgOverlay.appendChild(relRect);

            // Draw Relocation Vector Arrow from shrunk contour zone to the verified alternative parking bay
            const srcCx = x + w / 2;
            const srcCy = y + h / 2;
            const dstCx = Number(rp.x_pct) + Number(rp.w_pct) / 2;
            const dstCy = Number(rp.y_pct) + Number(rp.h_pct) / 2;
            const rdx = dstCx - srcCx;
            const rdy = dstCy - srcCy;
            const rlen = Math.hypot(rdx, rdy);
            if (rlen > 1.2) {
              const rLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
              rLine.setAttribute('x1', srcCx.toFixed(2));
              rLine.setAttribute('y1', srcCy.toFixed(2));
              rLine.setAttribute('x2', dstCx.toFixed(2));
              rLine.setAttribute('y2', dstCy.toFixed(2));
              rLine.setAttribute('class', 'svg-relocation-arrow-line');
              planSvgOverlay.appendChild(rLine);

              const rux = rdx / rlen;
              const ruy = rdy / rlen;
              const rbx = dstCx - rux * 1.6;
              const rby = dstCy - ruy * 1.6;
              const rpx1 = rbx - ruy * 0.9;
              const rpy1 = rby + rux * 0.9;
              const rpx2 = rbx + ruy * 0.9;
              const rpy2 = rby - rux * 0.9;
              const rHead = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
              rHead.setAttribute('points', `${dstCx.toFixed(2)},${dstCy.toFixed(2)} ${rpx1.toFixed(2)},${rpy1.toFixed(2)} ${rpx2.toFixed(2)},${rpy2.toFixed(2)}`);
              rHead.setAttribute('class', 'svg-relocation-arrow-head');
              planSvgOverlay.appendChild(rHead);
            }
          }
        }

        // 4 Inward Geometric Contraction Vectors (Left, Right, Top, Bottom)
        const midX = x + w / 2;
        const midY = y + h / 2;
        appendSvgArrowVector(planSvgOverlay, x, midY, Number(afterBox.x_pct), midY);
        appendSvgArrowVector(planSvgOverlay, x + w, midY, Number(afterBox.x_pct) + Number(afterBox.w_pct), midY);
        appendSvgArrowVector(planSvgOverlay, midX, y, midX, Number(afterBox.y_pct));
        appendSvgArrowVector(planSvgOverlay, midX, y + h, midX, Number(afterBox.y_pct) + Number(afterBox.h_pct));
      } else if (isNoteActive && isImp && (note.ve_category === 'LOCKED_CORE' || note.ve_category === 'APT')) {
        // Locked outer contour + internal partition shift indicator (0 ILS shell saving -> Design Improvement)
        const x = Number(note.x_pct);
        const y = Number(note.y_pct);
        const w = Number(note.w_pct);
        const h = Number(note.h_pct);
        const innerX = x + w * 0.25;
        const innerW = Math.max(1.8, w * 0.5);
        const innerRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        innerRect.setAttribute('x', innerX.toFixed(2));
        innerRect.setAttribute('y', (y + h * 0.15).toFixed(2));
        innerRect.setAttribute('width', innerW.toFixed(2));
        innerRect.setAttribute('height', Math.max(1.8, h * 0.7).toFixed(2));
        innerRect.setAttribute('class', 'svg-imp-inner-rect');
        planSvgOverlay.appendChild(innerRect);
      }

      // 2. Clean Numbered Pin on Plan (all detailed text is shown in the Side Dock beside the plan!)
      const pin = document.createElement('button');
      pin.type = 'button';
      pin.className = `plan-pin pin-${note.status} ${isVe ? 'pin-VE' : ''} ${isImp ? 'pin-IMP' : ''} ${isNoteActive ? 'active-pin' : ''} ${isNoteHovered ? 'hover-pin' : ''} ${isDimmed ? 'dimmed-pin' : ''}`;
      pin.style.left = `${note.cx_pct}%`;
      pin.style.top = `${note.cy_pct}%`;
      pin.textContent = note.pin_num;
      pin.dataset.noteId = note.id;
      pin.title = `#${note.pin_num}: ${note.room_name} — ${note.title}`;

      if (!showAllPins && !isNoteActive && currentFilter !== 'VE' && currentFilter !== 'DESIGN_IMP') {
        pin.style.opacity = '0';
        pin.style.pointerEvents = 'none';
      }

      pin.addEventListener('click', (e) => {
        e.stopPropagation();
        highlightNote(note.id, { scrollDoc: true, switchSheet: false, openDock: true, zoomTo: true });
      });

      planPinsLayer.appendChild(pin);
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
    const opt = pds.design_optimization || {};
    const optKpis = opt.executive_kpis || {};
    const contourAudit = opt.contour_audit_summary || {};

    const wrapper = document.createElement('div');
    wrapper.className = 'doc-compact-hub-strip';

    wrapper.innerHTML = `
      <div class="hub-launch-card hub-ve" id="kpi-card-open-ve" title="לחץ לפתיחת מרכז החיסכון בעלויות (הכל מרוכז במקום אחד)">
        <div class="hub-card-top">
          <span>💰 מרכז החיסכון בעלויות</span>
          <span>פתח ◂</span>
        </div>
        <div class="hub-card-val">${fmtNum(optKpis.grand_total_direct_saving_ils)} ₪</div>
        <div class="hub-card-sub">-${fmtNum(contourAudit.total_verified_contour_saved_sqm)} מ״ר קונטור מאומת · 0% פגיעה בדירות</div>
      </div>

      <div class="hub-launch-card hub-areas" id="btn-inline-open-modal" title="לחץ לפתיחת טבלאות שטחים, מרפסות, חזיתות וריצוף">
        <div class="hub-card-top">
          <span>📊 נתוני שטחים וחזיתות</span>
          <span>פתח ◂</span>
        </div>
        <div class="hub-card-val">${fmtNum(pds.total_built_area_sqm)} מ״ר בנוי</div>
        <div class="hub-card-sub">עילי: ${fmtNum(ag.total_sqm)} · מרתף: ${fmtNum(ug.total_sqm)} מ״ר</div>
      </div>
    `;

    const inlineBtn = wrapper.querySelector('#btn-inline-open-modal');
    if (inlineBtn) {
      inlineBtn.addEventListener('click', () => openSummaryAreasModal(data));
    }

    const veCardBtn = wrapper.querySelector('#kpi-card-open-ve');
    if (veCardBtn) {
      veCardBtn.addEventListener('click', () => openValueEngineeringModal(data));
    }

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
    const contourAudit = opt.contour_audit_summary || {};
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
          <td>
            <div>${p.impact || ''}</div>
            ${p.note_id ? `<div style="margin-top:4px;"><button type="button" class="btn-locate-on-plan btn-locate-sm" data-note-id="${p.note_id}" data-sheet-id="${p.sheet_id}">📍 הצג על התכנית (#${p.pin_num})</button></div>` : ''}
          </td>
        </tr>`
      )
      .join('');

    const aptOpt = opt.internal_apartment_optimization || {};
    const aptOptSummaryRows = (aptOpt.items || [])
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
            ${a.note_id ? `<button type="button" class="btn-locate-on-plan" data-note-id="${a.note_id}" data-sheet-id="${a.sheet_id}">📍 הצג על התכנית (#${a.pin_num})</button>` : '-'}
          </td>
        </tr>`
      )
      .join('');

    const critList = (sdoc.critical_notes_summary || [])
      .map((c) => `<li style="margin-bottom:6px;line-height:1.45;">${c}</li>`)
      .join('');

    summaryModalBody.innerHTML = `
      <!-- Top Quantitative KPI Strip -->
      <div class="modal-kpi-strip" style="margin-bottom: 12px;">
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

      <!-- CLEAN CLICKABLE TAB NAVIGATION FOR QUANTITATIVE DATA -->
      <div class="areas-modal-tabs-bar">
        <button type="button" class="areas-tab-btn active" data-areas-tab="summary">
          📋 1. סיכום ממצאים ושיפור תכנון
        </button>
        <button type="button" class="areas-tab-btn" data-areas-tab="built">
          🏢 2. שטחי בנייה עיליים ומרתפים (${fmtNum(pds.total_built_area_sqm)} מ״ר)
        </button>
        <button type="button" class="areas-tab-btn" data-areas-tab="balconies">
          🌿 3. מרפסות גג ותלויות (${fmtNum((rt.total_sqm || 0) + (sb.total_sqm || 0))} מ״ר)
        </button>
        <button type="button" class="areas-tab-btn" data-areas-tab="facades">
          🧱 4. חזיתות החוץ (${fmtNum(fac.total_sqm)} מ״ר)
        </button>
        <button type="button" class="areas-tab-btn" data-areas-tab="flooring">
          🛋️ 5. שטחי ריצוף קומות (${fmtNum(flr.grand_total_flooring_sqm)} מ״ר)
        </button>
      </div>

      <!-- TAB 1: Summary of Audit Notes & Actionable Improvement Proposals -->
      <div class="areas-tab-pane active" data-areas-pane="summary">
        <div class="modal-section-card">
          <h3>📋 1. מסמך סיכום הערות בקרת איכות והצעות אופרטיביות לשיפור התכנון</h3>
          <div class="sec-note" style="background:#eff6ff;border-right:4px solid #2563eb;padding:10px 14px;border-radius:6px;color:#1e3a8a;font-weight:700;">
            ${sdoc.overall_verdict || ''}
          </div>
          <h4 style="font-size:14px;font-weight:800;margin:10px 0 6px 0;color:#0f172a;">📌 ריכוז הערות מרכזיות בבדיקת המודל:</h4>
          <ul style="padding-right:20px;margin-bottom:14px;color:#334155;font-size:13px;">
            ${critList}
          </ul>
          <h4 style="font-size:14px;font-weight:800;margin:10px 0 8px 0;color:#0f172a;">🛠️ א. טבלת הצעות לשיפור תכנוני והנדסי:</h4>
          <table class="modal-data-table" style="margin-bottom:16px;">
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

          <h4 style="font-size:14px;font-weight:800;margin:14px 0 8px 0;color:#1e3a8a;">🛋️ ב. שיפור תכנון פנים-דירתי: הקטנת מסדרונות לטובת חדרי מגורים ואופטימיזציית פתחים (+${fmtNum(aptOpt.total_reclaimed_effective_living_sqm)} מ״ר חדרים מוגדלים — ללא שינוי קונטור הבנייה):</h4>
          <div class="sec-note">
            העברת שטח ממסדרון לחדר מגורים אינה מקטינה את קונטור הבנייה ולכן אינה נכללת במודל החיסכון בעלויות הבנייה, אלא מהווה שיפור תכנון אדריכלי המעלה את נצילות הדירה ואיכות החדרים.
          </div>
          <table class="modal-data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>טיפוס דירה וקומות</th>
                <th>מסדרון נוכחי</th>
                <th>מסדרון יעיל</th>
                <th>תוספת שטח לחדרים (לדירה)</th>
                <th>סה״כ שטח חדרים מוגדל בפרויקט</th>
                <th>איפה ואיך בתכנית הדירה + אופטימיזציית פתחים</th>
                <th>מיקום על התכנית</th>
              </tr>
            </thead>
            <tbody>
              ${aptOptSummaryRows}
            </tbody>
          </table>
        </div>
      </div>

      <!-- TAB 2: Above-Ground & Underground Construction Areas -->
      <div class="areas-tab-pane" data-areas-pane="built">
        <div class="modal-section-card">
          <h3>🏢 סך שטחי בנייה עיליים — סך הכל וחלוקה לקומות (${fmtNum(ag.total_sqm)} מ״ר)</h3>
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

        <div class="modal-section-card">
          <h3>🅿️ סך שטחי בנייה תת-קרקעיים (${fmtNum(ug.total_sqm)} מ״ר)</h3>
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
      </div>

      <!-- TAB 3: Roof Terraces & Suspended Balconies -->
      <div class="areas-tab-pane" data-areas-pane="balconies">
        <div class="modal-section-card">
          <h3>🌿 סך שטחי מרפסות גג (${fmtNum(rt.total_sqm)} מ״ר) ומרפסות תלויות (${fmtNum(sb.total_sqm)} מ״ר)</h3>
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
      </div>

      <!-- TAB 4: Total Facade Areas by Direction -->
      <div class="areas-tab-pane" data-areas-pane="facades">
        <div class="modal-section-card">
          <h3>🧱 סך שטחי חזיתות בחלוקה לחזיתות השונות (${fmtNum(fac.total_sqm)} מ״ר)</h3>
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
      </div>

      <!-- TAB 5: Flooring Areas (Full Floors — Apartments / Public / Balconies) -->
      <div class="areas-tab-pane" data-areas-pane="flooring">
        <div class="modal-section-card">
          <h3>🛋️ שטחי ריצוף נטו (שטחי רצפה של קומות מלאות) — דירות / ציבורי / מרפסות (${fmtNum(flr.grand_total_flooring_sqm)} מ״ר)</h3>
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
      </div>
    `;

    summaryModalBody.querySelectorAll('.areas-tab-btn').forEach((tabBtn) => {
      tabBtn.addEventListener('click', () => {
        const targetTab = tabBtn.getAttribute('data-areas-tab');
        summaryModalBody.querySelectorAll('.areas-tab-btn').forEach((b) => b.classList.toggle('active', b === tabBtn));
        summaryModalBody.querySelectorAll('.areas-tab-pane').forEach((pane) => {
          pane.classList.toggle('active', pane.getAttribute('data-areas-pane') === targetTab);
        });
      });
    });

    summaryModalBody.querySelectorAll('.btn-locate-on-plan').forEach((btn) => {
      btn.addEventListener('click', () => {
        const nid = btn.getAttribute('data-note-id');
        const sid = btn.getAttribute('data-sheet-id');
        if (nid) {
          focusSavingsItemOnPlan(nid, sid);
        }
      });
    });

    summaryAreasModal.classList.remove('hidden');
  }

  // =========================================================================
  // 4.4 VISUAL BEFORE/AFTER SVG SCHEMATIC GENERATOR & 4-PILLAR BUILDER
  // =========================================================================
  function buildBeforeAfterSvgDiagram(note) {
    const vExp = note.visual_explanation || {};
    const dType = vExp.diagram_type || (note.ve_category === 'AG' ? 'AG_CONTOUR' : note.ve_category === 'UG' ? 'UG_CONTOUR' : note.ve_category === 'FAC' ? 'FACADE_CLADDING' : note.ve_category === 'LOCKED_CORE' ? 'LOCKED_CORE' : note.ve_category === 'APT' ? 'APT_CORRIDOR' : 'STATUTORY_CHECK');
    const beforeVal = vExp.before_val !== undefined ? vExp.before_val : '';
    const afterVal = vExp.after_val !== undefined ? vExp.after_val : '';
    const unitLbl = vExp.unit_label || 'מ״ר';

    if (dType === 'AG_CONTOUR' || dType === 'UG_CONTOUR') {
      const isUg = dType === 'UG_CONTOUR';
      const titleHe = isUg
        ? 'שרטוט השוואתי: כיווץ דיפון מרתף (תוך שמירת רמפה ושטחי תמרון)'
        : 'שרטוט השוואתי: כיווץ קונטור חיצוני עילי (נבנה פחות ← חיסכון)';
      const badgeText = `-${fmtNum(note.ve_saved_sqm || 0)} מ״ר קונטור | ${fmtNum(note.ve_saving_ils || 0)} ₪`;
      const rampProtectedSqm = note.protected_ramp_and_maneuvering_deducted_sqm || 0;
      const underRampSqm = note.under_ramp_utilized_sqm || 0;
      const relocAudit = note.parking_relocation_audit || null;
      const relocStallsCount = relocAudit ? (relocAudit.stalls_relocated_count || 1) : 1;
      return `
        <div class="fc-diagram-header">
          <span>📐 ${titleHe}</span>
          <span class="fc-diagram-badge">${badgeText}</span>
        </div>
        <svg class="fc-before-after-svg" viewBox="0 0 310 ${isUg ? 136 : 112}" xmlns="http://www.w3.org/2000/svg">
          <!-- BEFORE SIDE (Right in RTL, x=170..302) -->
          <rect x="170" y="8" width="132" height="${isUg ? 120 : 96}" rx="6" fill="#fef2f2" stroke="#fca5a5" stroke-width="1.2"/>
          <text x="236" y="21" text-anchor="middle" font-size="9.5" font-weight="800" fill="#991b1b">לפני: קונטור מנופח (${beforeVal} ${unitLbl})</text>
          <!-- Outer Red Dashed Contour -->
          <rect x="182" y="27" width="108" height="58" rx="3" fill="#fee2e2" stroke="#ef4444" stroke-width="1.8" stroke-dasharray="4 2"/>
          <!-- Inner Core/Apts -->
          <rect x="196" y="37" width="80" height="38" rx="2" fill="#ffffff" stroke="#64748b" stroke-width="1"/>
          ${isUg ? `<rect x="198" y="39" width="76" height="14" rx="2" fill="#fef3c7" stroke="#f59e0b" stroke-width="1" stroke-dasharray="2 1"/><text x="236" y="49" text-anchor="middle" font-size="7.5" font-weight="800" fill="#b45309">רמפה + מיסעה דו-סטרית 6.00 מ׳</text>` : ''}
          <text x="236" y="${isUg ? 66 : 59}" text-anchor="middle" font-size="8.5" font-weight="700" fill="#334155">${isUg ? 'חניית קצה + חדר מאגר/משאבות' : 'דירות (שטח נשמר)'}</text>
          <text x="236" y="97" text-anchor="middle" font-size="8.5" font-weight="700" fill="#dc2626">${note.contour_dims_before_after ? note.contour_dims_before_after.split('←')[0] : 'מעטפת רחבה'}</text>
          ${isUg ? `<text x="236" y="109" text-anchor="middle" font-size="7.5" font-weight="700" fill="#92400e">רדיוסי סיבוב ואוזן תמרון נשמרים</text>` : ''}
          ${isUg ? `<text x="236" y="121" text-anchor="middle" font-size="7.3" font-weight="800" fill="#b91c1c">חניית קצה על קו הדיפון שנסוג</text>` : ''}

          <!-- CENTER ARROW -->
          <path d="M 164 56 L 144 56" stroke="#059669" stroke-width="2.4" stroke-linecap="round"/>
          <polygon points="144,56 151,51 151,61" fill="#059669"/>

          <!-- AFTER SIDE (Left in RTL, x=8..140) -->
          <rect x="8" y="8" width="132" height="${isUg ? 120 : 96}" rx="6" fill="#ecfdf5" stroke="#6ee7b7" stroke-width="1.2"/>
          <text x="74" y="21" text-anchor="middle" font-size="9.5" font-weight="800" fill="#065f46">אחרי: קונטור מכווץ (${afterVal} ${unitLbl})</text>
          <!-- Ghost Old Contour -->
          <rect x="20" y="27" width="108" height="58" rx="3" fill="none" stroke="#ef4444" stroke-width="1.2" stroke-dasharray="3 3" opacity="0.65"/>
          <!-- Contracted Emerald Contour -->
          <rect x="29" y="33" width="90" height="46" rx="3" fill="#d1fae5" stroke="#059669" stroke-width="2.2"/>
          <rect x="34" y="37" width="80" height="38" rx="2" fill="#ffffff" stroke="#059669" stroke-width="1"/>
          ${isUg ? `<rect x="36" y="39" width="76" height="14" rx="2" fill="#fef3c7" stroke="#f59e0b" stroke-width="1" stroke-dasharray="2 1"/><text x="74" y="49" text-anchor="middle" font-size="7.5" font-weight="800" fill="#b45309">מוגן: רמפה + תמרון (${fmtNum(rampProtectedSqm)} מ״ר)</text>` : ''}
          <text x="74" y="${isUg ? 66 : 59}" text-anchor="middle" font-size="8.5" font-weight="800" fill="#065f46">נבנה פחות: -${fmtNum(note.ve_saved_sqm || 0)} מ״ר</text>
          <text x="74" y="97" text-anchor="middle" font-size="8.5" font-weight="800" fill="#047857">חיסכון: ${fmtNum(note.ve_saving_ils || 0)} ₪</text>
          ${isUg && underRampSqm > 0 ? `<text x="74" y="109" text-anchor="middle" font-size="7.4" font-weight="800" fill="#1d4ed8">+${fmtNum(underRampSqm)} מ״ר ניצול תחת רמפה (H≥2.20m)</text>` : ''}
          ${isUg ? `<text x="74" y="121" text-anchor="middle" font-size="7.4" font-weight="900" fill="#0e7490">🔄🅿️ ${relocStallsCount} חניות הועתקו למפרץ חלופי מאומת!</text>` : ''}
        </svg>
      `;
    }

    if (dType === 'FACADE_CLADDING') {
      return `
        <div class="fc-diagram-header">
          <span>🧱 שרטוט השוואתי: אופטימיזציית חיפוי יבש (700 ₪) מול טיח (300 ₪)</span>
          <span class="fc-diagram-badge">חיסכון: ${fmtNum(note.ve_saving_ils || 0)} ₪</span>
        </div>
        <svg class="fc-before-after-svg" viewBox="0 0 310 106" xmlns="http://www.w3.org/2000/svg">
          <rect x="4" y="4" width="302" height="98" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
          <!-- Before bar -->
          <text x="296" y="20" text-anchor="end" font-size="9.2" font-weight="800" fill="#991b1b">לפני: חיפוי יבש מלא גם בעורף/מרפסות (${beforeVal} מ״ר יבש)</text>
          <rect x="14" y="26" width="282" height="20" rx="4" fill="#fca5a5" stroke="#dc2626" stroke-width="1.2"/>
          <text x="155" y="39" text-anchor="middle" font-size="9" font-weight="800" fill="#7f1d1d">חיפוי קשיח יבש יקר (700 ₪/מ״ר)</text>

          <!-- After bar -->
          <text x="296" y="64" text-anchor="end" font-size="9.2" font-weight="800" fill="#065f46">אחרי: היברידי — חזית רחוב ביבש + ${fmtNum(note.ve_saved_sqm || 0)} מ״ר טיח אקרילי (300 ₪)</text>
          <rect x="130" y="70" width="166" height="22" rx="4" fill="#cbd5e1" stroke="#475569" stroke-width="1.2"/>
          <text x="213" y="84" text-anchor="middle" font-size="8.5" font-weight="800" fill="#1e293b">חיפוי יבש בחזית ייצוגית (${afterVal} מ״ר)</text>
          <rect x="14" y="70" width="112" height="22" rx="4" fill="#6ee7b7" stroke="#059669" stroke-width="1.5"/>
          <text x="70" y="84" text-anchor="middle" font-size="8.5" font-weight="900" fill="#064e3b">טיח: -400 ₪/מ״ר</text>
        </svg>
      `;
    }

    if (dType === 'LOCKED_CORE' || dType === 'APT_CORRIDOR') {
      const isApt = dType === 'APT_CORRIDOR';
      const gainedSqm = fmtNum(note.design_improvement_sqm || note.ve_proposed_gross_sqm || 0);
      return `
        <div class="fc-diagram-header hdr-imp">
          <span>🛋️ ${isApt ? 'שרטוט השוואתי: קיצור מסדרון לטובת הגדלת חדרים' : 'שרטוט השוואתי: ליבה כלואה (קונטור קבוע = 0 ₪ חיסכון שלד)'}</span>
          <span class="fc-diagram-badge badge-imp">+${gainedSqm} מ״ר שיפור תכנון</span>
        </div>
        <svg class="fc-before-after-svg" viewBox="0 0 310 108" xmlns="http://www.w3.org/2000/svg">
          <!-- BEFORE (Right) -->
          <rect x="168" y="8" width="134" height="92" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
          <text x="235" y="21" text-anchor="middle" font-size="9" font-weight="800" fill="#334155">לפני: קונטור חיצוני קבוע</text>
          <rect x="180" y="28" width="110" height="52" rx="3" fill="#e2e8f0" stroke="#475569" stroke-width="1.8"/>
          <rect x="210" y="28" width="50" height="52" fill="#fecaca" stroke="#dc2626" stroke-width="1.2"/>
          <text x="235" y="57" text-anchor="middle" font-size="8" font-weight="800" fill="#991b1b">${isApt ? 'מסדרון מבוזבז' : 'ליבה רחבה'}</text>
          <text x="235" y="93" text-anchor="middle" font-size="8" font-weight="700" fill="#475569">קונטור בניין נעול</text>

          <!-- ARROW -->
          <path d="M 162 54 L 144 54" stroke="#2563eb" stroke-width="2.2" stroke-linecap="round"/>
          <polygon points="144,54 151,49 151,59" fill="#2563eb"/>

          <!-- AFTER (Left) -->
          <rect x="8" y="8" width="134" height="92" rx="6" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5"/>
          <text x="75" y="21" text-anchor="middle" font-size="9" font-weight="800" fill="#1e3a8a">אחרי: אותו קונטור (0 ₪ שלד)</text>
          <rect x="20" y="28" width="110" height="52" rx="3" fill="#dbeafe" stroke="#1e40af" stroke-width="1.8"/>
          <rect x="60" y="28" width="30" height="52" fill="#f1f5f9" stroke="#64748b" stroke-width="1"/>
          <text x="40" y="56" text-anchor="middle" font-size="8" font-weight="900" fill="#1e40af">+חדר</text>
          <text x="110" y="56" text-anchor="middle" font-size="8" font-weight="900" fill="#1e40af">+חדר</text>
          <text x="75" y="93" text-anchor="middle" font-size="8.5" font-weight="800" fill="#1d4ed8">+${gainedSqm} מ״ר שטח שימושי נטו!</text>
        </svg>
      `;
    }

    // Default Statutory / Functional Engineering Check Diagram
    const statusColor = note.status === 'FAIL' ? '#dc2626' : note.status === 'WARN' ? '#d97706' : '#16a34a';
    const statusBg = note.status === 'FAIL' ? '#fef2f2' : note.status === 'WARN' ? '#fffbeb' : '#f0fdf4';
    return `
      <div class="fc-diagram-header" style="background:${statusBg};color:${statusColor};border-bottom-color:#cbd5e1;">
        <span>📏 בקרת תאימות הנדסית וסטטוטורית (${note.rule_id})</span>
        <span class="fc-diagram-badge" style="background:${statusColor};color:#fff;">${STATUS_LABELS[note.status] || note.status}</span>
      </div>
      <svg class="fc-before-after-svg" viewBox="0 0 310 86" xmlns="http://www.w3.org/2000/svg">
        <rect x="162" y="10" width="138" height="66" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2"/>
        <text x="231" y="28" text-anchor="middle" font-size="9" font-weight="800" fill="#475569">נמדד בתכנית (Measured)</text>
        <text x="231" y="52" text-anchor="middle" font-size="10.5" font-weight="900" fill="${statusColor}">${(note.measured || '').slice(0, 22)}</text>

        <path d="M 156 43 L 142 43" stroke="${statusColor}" stroke-width="2" stroke-linecap="round"/>
        <polygon points="142,43 148,38 148,48" fill="${statusColor}"/>

        <rect x="10" y="10" width="128" height="66" rx="6" fill="${statusBg}" stroke="${statusColor}" stroke-width="1.4"/>
        <text x="74" y="28" text-anchor="middle" font-size="9" font-weight="800" fill="#334155">דרישת תקן / יעד</text>
        <text x="74" y="52" text-anchor="middle" font-size="10" font-weight="900" fill="#0f172a">${(note.benchmark || '').slice(0, 22)}</text>
      </svg>
    `;
  }

  function buildFourPillarsSideDockHtml(note) {
    const vExp = note.visual_explanation || {};
    const rec = vExp.recommendation || {};
    const sol = vExp.solution || {};
    const sav = vExp.savings || {};
    const imp = vExp.building_impact || {};

    const isVe = Boolean(note.is_value_eng);
    const isDesignImp = Boolean(note.is_design_improvement);
    const effPct = sav.efficiency_pct !== undefined ? sav.efficiency_pct : (isVe ? 100 : 0);

    // 4 Decision Value Dimensions (Financial, Planning, Feasibility, Certainty)
    const finImpactText = isVe
      ? `חיסכון ישיר: ${fmtNum(sav.saving_ils !== undefined ? sav.saving_ils : (note.ve_saving_ils || 0))} ₪ (-${fmtNum(sav.net_contour_sqm || note.ve_saved_sqm || 0)} מ״ר קונטור)`
      : isDesignImp
        ? `0 ₪ שלד (השבחת +${fmtNum(note.design_improvement_sqm || sav.locked_sqm || 0)} מ״ר שטח שימושי)`
        : note.status === 'FAIL'
          ? 'מניעת עיכוב היתר / עלות תיקון בביצוע'
          : 'ללא השפעה תקציבית ישירה';

    const planImpactText = imp.contour
      ? `${imp.contour} · ${imp.apartments || '0% פגיעה בדירות'}`
      : (note.room_name || 'בדיקת התאמה תכנונית');

    const feasibilityText = isVe
      ? (note.ve_category === 'FAC' ? 'גבוהה — עדכון מפרט גמר חזיתות' : 'בינונית — עדכון קונטור וקואורדינציית יועצים')
      : isDesignImp
        ? 'גבוהה — הזזת מחיצות פנים בלבד'
        : note.status === 'PASS'
          ? 'מאושר — אין צורך בשינוי'
          : 'דורש בדיקת מתכנן ועדכון שרטוט';

    const certaintyText = note.rule_id
      ? `מדידה וקטורית מהתכנית מול תקן (${note.rule_id})`
      : 'חישוב הנדסי מתוך קואורדינטות התכנית';

    const currentDecision = getNoteDecision(note.id);

    const waterfallHtml = (isVe || isDesignImp)
      ? `
        <div class="fc-waterfall-strip">
          <div class="fc-wf-box fc-wf-step wf-gross">
            <span class="wf-lbl">שטח שנבדק</span>
            <span class="wf-val">${fmtNum(sav.gross_sqm || note.ve_proposed_gross_sqm || note.ve_saved_sqm || 0)} מ״ר</span>
          </div>
          <div class="fc-wf-box fc-wf-step wf-locked">
            <span class="wf-lbl">כלוא (שיפור תכנון)</span>
            <span class="wf-val">${fmtNum(sav.locked_sqm || note.ve_locked_non_contour_sqm || (isDesignImp ? note.design_improvement_sqm : 0))} מ״ר (0 ₪)</span>
          </div>
          <div class="fc-wf-box fc-wf-step wf-net">
            <span class="wf-lbl">כיווץ קונטור נטו</span>
            <span class="wf-val">${fmtNum(sav.net_contour_sqm || (isVe ? note.ve_saved_sqm : 0) || 0)} מ״ר</span>
          </div>
        </div>
        <div class="fc-eff-bar-wrap">
          <div class="fc-eff-bar-labels">
            <span>יעילות כיווץ קונטור הבניין (η): <strong>${effPct}%</strong></span>
            <span><strong>${fmtNum(sav.saving_ils !== undefined ? sav.saving_ils : (note.ve_saving_ils || 0))} ₪</strong></span>
          </div>
          <div class="fc-eff-bar-track">
            <div class="fc-eff-bar-fill ${isDesignImp ? 'fill-imp fc-eff-bar-fill-blue' : 'fc-eff-bar-fill-green'}" style="width:${Math.max(8, effPct)}%;"></div>
          </div>
        </div>
      `
      : '';

    const rampAndManeuverBoxHtml = (note.ramp_function_audit_he || note.maneuvering_aisle_audit_he || (sav && sav.ramp_and_maneuver_deducted_sqm > 0))
      ? `
        <div class="fc-ramp-audit-box">
          <div class="fc-ramp-audit-title">🛣️ בקרת רמפות ירידה, רדיוסי סיבוב ושטחי תמרון לחניות</div>
          ${note.ramp_function_audit_he ? `<div><strong>• תפקוד רמפה וגובה ראש (H_clear):</strong> ${note.ramp_function_audit_he}</div>` : ''}
          ${note.maneuvering_aisle_audit_he ? `<div style="margin-top:3px;"><strong>• שטחי תמרון ומיסעות מוגנים (${fmtNum(note.protected_ramp_and_maneuvering_deducted_sqm || sav.ramp_and_maneuver_deducted_sqm || 0)} מ״ר = 0 ₪):</strong> ${note.maneuvering_aisle_audit_he}</div>` : ''}
          ${note.under_ramp_utilized_sqm > 0 ? `<div style="margin-top:3px;color:#0284c7;font-weight:800;">💧 שטח מנוצל מתחת לרמפה (H_clear ≥ 2.20 מ׳): ${fmtNum(note.under_ramp_utilized_sqm)} מ״ר למאגר/משאבות</div>` : ''}
        </div>
      `
      : '';

    const pReloc = note.parking_relocation_audit || sol.parking_relocation_audit || null;
    const parkingRelocBoxHtml = (pReloc || note.parking_relocation_audit_he)
      ? `
        <div class="fc-parking-reloc-box">
          <div class="fc-parking-reloc-title">🔄🅿️ בדיקת העתקת חנייה ומציאת מקום חלופי מאומת (0 חניות אבודות)</div>
          ${pReloc ? `
            <div><strong>• חנייה שהוזזה מאזור כיווץ הקונטור:</strong> ${pReloc.affected_stalls_label || ''} (${pReloc.original_location_he || ''})</div>
            <div style="margin-top:3px;"><strong>• מקום חלופי מאומת שנמצא בתכנית:</strong> <strong>${pReloc.alternative_location_found_he || ''}</strong></div>
            <div style="margin-top:3px;"><strong>• מידות וגישה לתמרון במיקום החדש:</strong> ${pReloc.new_stall_dimensions_and_access_he || ''}</div>
            <div style="margin-top:3px;color:#047857;font-weight:900;">✅ מאזן חניות נטו: ${pReloc.net_parking_balance_he || ''}</div>
          ` : `<div>${note.parking_relocation_audit_he}</div>`}
        </div>
      `
      : '';

    return `
      <div class="l2-finding-summary-box">
        <div class="l2-sec-text">${rec.finding || note.summary}</div>
        <div class="l2-action-box">
          ${sol.how_to_execute || note.how_to_execute || note.recommendation}
        </div>
      </div>

      <div class="l2-decision-workflow-box">
        <div class="l2-dec-buttons">
          <button type="button" class="btn-dec-state ${currentDecision === 'TODO' ? 'active dec-todo' : ''}" data-dec="TODO" data-note-id="${note.id}">לטיפול</button>
          <button type="button" class="btn-dec-state ${currentDecision === 'VERIFIED' ? 'active dec-verified' : ''}" data-dec="VERIFIED" data-note-id="${note.id}">נבדק</button>
          <button type="button" class="btn-dec-state ${currentDecision === 'APPROVED' ? 'active dec-approved' : ''}" data-dec="APPROVED" data-note-id="${note.id}">אושר</button>
          <button type="button" class="btn-dec-state ${currentDecision === 'REJECTED' ? 'active dec-rejected' : ''}" data-dec="REJECTED" data-note-id="${note.id}">נדחה</button>
        </div>
      </div>

      <details class="l3-evidence-drawer">
        <summary class="l3-evidence-summary">
          <span>פירוט נוסף ותחשיב</span>
          <span class="l3-chevron">▾</span>
        </summary>
        <div class="l3-evidence-body">
          <div class="l2-value-metrics-grid">
            <div class="l2-val-card">
              <span class="l2-val-lbl">השפעה כספית</span>
              <strong class="l2-val-txt">${finImpactText}</strong>
            </div>
            <div class="l2-val-card">
              <span class="l2-val-lbl">השפעה תכנונית</span>
              <strong class="l2-val-txt">${planImpactText}</strong>
            </div>
            <div class="l2-val-card">
              <span class="l2-val-lbl">ישימות</span>
              <strong class="l2-val-txt">${feasibilityText}</strong>
            </div>
            <div class="l2-val-card">
              <span class="l2-val-lbl">מקור נתון</span>
              <strong class="l2-val-txt">${certaintyText}</strong>
            </div>
          </div>

          <div class="l3-block">
            <div class="l3-block-title">תחשיב (${sav.rate_label || note.rule_id})</div>
            <div>${sav.formula || note.measured}</div>
            ${waterfallHtml}
          </div>

          ${parkingRelocBoxHtml}
          ${rampAndManeuverBoxHtml}

          <div style="margin-top:8px;">
            ${buildBeforeAfterSvgDiagram(note)}
          </div>
        </div>
      </details>
    `;
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
    const contourAudit = opt.contour_audit_summary || {};
    const agOpt = opt.above_ground_optimization || {};
    const ugOpt = opt.underground_optimization || {};
    const facOpt = opt.facade_cladding_optimization || {};

    valueEngModalTitle.textContent = `💰 מודל החיסכון בעלויות הבנייה ובקרת כיווץ קונטור — ${data.project_name}`;

    const pillarsHtml = (contourAudit.methodology_pillars || [])
      .map(
        (p) => `
        <div style="background:#f8fafc;border:1px solid #cbd5e1;border-right:4px solid #0284c7;border-radius:6px;padding:8px 10px;">
          <div style="font-weight:800;font-size:12px;color:#0f172a;margin-bottom:3px;">📐 ${p.title}</div>
          <div style="font-size:11.5px;color:#334155;line-height:1.4;">${p.description}</div>
        </div>`
      )
      .join('');

    // Build Interactive 4-Pillar Visual Recommendation Cards Gallery for all VE & Design Improvement Notes
    const veAndImpNotes = (data.notes || []).filter((n) => n.is_value_eng || n.is_design_improvement);
    const visualGalleryCardsHtml = veAndImpNotes
      .map((n) => {
        const isVe = Boolean(n.is_value_eng);
        const vExp = n.visual_explanation || {};
        const rec = vExp.recommendation || {};
        const sol = vExp.solution || {};
        const sav = vExp.savings || {};
        const imp = vExp.building_impact || {};
        return `
          <div class="ve-gallery-card ${isVe ? '' : 'card-imp-mode'}">
            <div class="ve-gc-head">
              <div class="ve-gc-title">
                <span>${isVe ? '💰' : '🛋️'} #${n.pin_num} · ${n.room_name}</span>
                <span class="ve-gc-badge ${isVe ? 'badge-save' : 'badge-imp'}">${n.ve_callout_badge || n.measured}</span>
              </div>
              <div style="font-size:11.5px;font-weight:700;color:#334155;">${n.title}</div>
            </div>
            <div style="padding:8px 10px;background:#f8fafc;border-bottom:1px solid #e2e8f0;">
              ${buildBeforeAfterSvgDiagram(n)}
            </div>
            <div class="ve-gc-body">
              <div class="note-4p-box p-rec">
                <div class="p4-hdr">🎯 1. ההמלצה (איפה ומה אותר)</div>
                <div class="p4-txt"><strong>${rec.where || n.where_on_plan || n.room_name}:</strong> ${rec.finding || n.summary}</div>
              </div>
              <div class="note-4p-box p-sol">
                <div class="p4-hdr">🛠️ 2. הפתרון ההנדסי (איך מבצעים)</div>
                <div class="p4-txt">${sol.how_to_execute || n.how_to_execute || n.recommendation}</div>
                ${n.parking_relocation_audit ? `<div style="margin-top:4px;padding:4px 6px;background:#ecfeff;border:1px solid #67e8f9;border-right:3px solid #0891b2;border-radius:4px;font-size:10.5px;color:#0e7490;"><strong>🔄🅿️ העתקת חנייה למקום חלופי מאומת (${n.parking_relocation_audit.affected_stalls_label}):</strong> מ-${n.parking_relocation_audit.original_location_he} ⬅️ <strong>${n.parking_relocation_audit.alternative_location_found_he}</strong> (${n.parking_relocation_audit.new_stall_dimensions_and_access_he})</div>` : ''}
              </div>
              <div class="note-4p-box p-sav ${isVe ? '' : 'p-sav-zero'}">
                <div class="p4-hdr">💰 3. החיסכון ובקרת הקונטור</div>
                <div class="p4-txt"><strong>${sav.formula || n.measured}</strong> (${sav.rate_label || ''})</div>
              </div>
              <div class="note-4p-box p-imp">
                <div class="p4-hdr">🏢 4. ההשפעה על הבניין</div>
                <div class="p4-txt">
                  <div>• <strong>קונטור:</strong> ${imp.contour || '-'}</div>
                  <div>• <strong>דירות וחניות:</strong> ${imp.apartments || '-'} | ${imp.parking || '-'}</div>
                </div>
              </div>
            </div>
            <div class="ve-gc-foot">
              <span style="font-size:11px;font-weight:800;color:#475569;">גיליון: ${n.typology}</span>
              <button type="button" class="btn-locate-on-plan" data-note-id="${n.id}" data-sheet-id="${n.sheet_id}">📍 הצג איפה ואיך על התכנית (#${n.pin_num})</button>
            </div>
          </div>
        `;
      })
      .join('');

    const lockedCoreRows = (contourAudit.locked_core_reclassified_items || [])
      .map(
        (l, idx) => `
        <tr>
          <td><strong>#${idx + 1}</strong></td>
          <td><strong>${l.zone}</strong></td>
          <td>${fmtNum(l.proposed_core_reduction_sqm)} מ״ר</td>
          <td style="font-weight:900;color:#dc2626;background:#fef2f2;">0.0 מ״ר (קונטור נעול)</td>
          <td style="font-weight:800;color:#64748b;">0 ₪ (קוזז מחיסכון)</td>
          <td style="font-weight:900;background:#dbeafe;color:#1e3a8a;">+${fmtNum(l.reclassified_design_improvement_sqm)} מ״ר שיפור תכנון</td>
          <td>
            <div style="color:#991b1b;font-weight:700;"><strong>🔍 למה לא הקטין קונטור:</strong> ${l.why_not_contour_saving}</div>
            <div style="margin-top:3px;color:#1e3a8a;"><strong>🛋️ שיפור תכנון שהושג:</strong> ${l.design_benefit}</div>
          </td>
          <td style="text-align:center;">
            ${l.note_id ? `<button type="button" class="btn-locate-on-plan" data-note-id="${l.note_id}" data-sheet-id="${l.sheet_id}">📍 הצג על התכנית (#${l.pin_num})</button>` : '-'}
          </td>
        </tr>`
      )
      .join('');

    const agOptRows = (agOpt.items || [])
      .map(
        (item, idx) => `
        <tr>
          <td><strong>#${idx + 1}</strong></td>
          <td><strong>${item.floor_or_zone}</strong></td>
          <td>${fmtNum(item.current_sqm)} מ״ר</td>
          <td>${fmtNum(item.proposed_gross_reduction_sqm || item.saved_sqm)} מ״ר</td>
          <td style="color:#1d4ed8;font-weight:700;">${fmtNum(item.non_contour_reclassified_sqm || 0)} מ״ר (0 ₪ ← שיפור תכנון)</td>
          <td style="font-weight:900;color:#047857;background:#ecfdf5;">${fmtNum(item.saved_sqm)} מ״ר (${item.contour_efficiency_pct || 100}%)</td>
          <td style="font-weight:900;background:#dcfce7;color:#065f46;">${fmtNum(item.cost_saving_ils)} ₪</td>
          <td>
            <div><strong>📍 איפה ואיך:</strong> ${item.engineering_action}</div>
            <div style="margin-top:3px;color:#0f766e;font-weight:700;"><strong>📐 הוכחת כיווץ קונטור (${item.contour_dims_before_after || ''}):</strong> ${item.contour_mechanism || ''}</div>
            ${item.non_contour_reclassified_sqm > 0 ? `<div style="margin-top:2px;font-size:11px;color:#1e40af;"><strong>🔄 קיזוז ליבה כלואה:</strong> ${item.locked_reason_he}</div>` : ''}
            <div style="font-size:11px;color:#047857;margin-top:2px;font-weight:700;">🛡️ נשמר במלואו: ${item.preserved_utilities}</div>
          </td>
          <td style="text-align:center;">
            ${item.note_id ? `<button type="button" class="btn-locate-on-plan" data-note-id="${item.note_id}" data-sheet-id="${item.sheet_id}">📍 הצג על התכנית (#${item.pin_num})</button>` : '-'}
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
          <td>${fmtNum(item.proposed_gross_reduction_sqm || item.saved_sqm)} מ״ר</td>
          <td style="color:#b45309;font-weight:800;background:#fffbeb;">
            <div>${fmtNum(item.protected_ramp_and_maneuvering_deducted_sqm || item.non_contour_reclassified_sqm || 0)} מ״ר (0 ₪ — מוגן לרמפה/תמרון)</div>
            ${item.under_ramp_utilized_sqm > 0 ? `<div style="color:#1d4ed8;font-size:10.5px;margin-top:2px;">+${fmtNum(item.under_ramp_utilized_sqm)} מ״ר נוצל תחת רמפה (H≥2.20m)</div>` : ''}
          </td>
          <td style="font-weight:900;color:#047857;background:#ecfdf5;">${fmtNum(item.saved_sqm)} מ״ר (${item.contour_efficiency_pct || 100}%)</td>
          <td style="font-weight:900;background:#dcfce7;color:#065f46;">${fmtNum(item.cost_saving_ils)} ₪</td>
          <td>
            <div><strong>📍 איפה ואיך על תכנית המקור:</strong> ${item.engineering_action}</div>
            <div style="margin-top:3px;color:#0f766e;font-weight:700;"><strong>📐 הוכחת כיווץ פוליגון דיפון (${item.contour_dims_before_after || ''}):</strong> ${item.contour_mechanism || ''}</div>
            ${item.parking_relocation_audit ? `
              <div style="margin-top:4px;font-size:11px;color:#0e7490;background:#ecfeff;padding:5px 8px;border-radius:5px;border:1px solid #67e8f9;border-right:3.5px solid #0891b2;">
                <div style="font-weight:900;color:#155e75;margin-bottom:2px;">🔄🅿️ בדיקת העתקת חנייה ומציאת מקום חלופי מאומת (${item.parking_relocation_audit.affected_stalls_label}):</div>
                <div>• <strong>מיקום מקורי שבוטל/הוזז עקב כיווץ הדיפון:</strong> ${item.parking_relocation_audit.original_location_he}</div>
                <div>• <strong>מקום חלופי מאומת שנמצא בתכנית:</strong> <strong style="color:#0369a1;">${item.parking_relocation_audit.alternative_location_found_he}</strong></div>
                <div>• <strong>מידות וגישה לתמרון במיקום החדש:</strong> ${item.parking_relocation_audit.new_stall_dimensions_and_access_he}</div>
                <div style="font-weight:800;color:#047857;">✅ מאזן חניות נטו: ${item.parking_relocation_audit.net_parking_balance_he}</div>
              </div>
            ` : ''}
            ${item.ramp_function_audit_he ? `<div style="margin-top:3px;font-size:11px;color:#92400e;background:#fffbeb;padding:3px 6px;border-radius:4px;border-right:3px solid #f59e0b;"><strong>🛣️ תפקוד רמפת ירידה וגובה ראש (H_clear):</strong> ${item.ramp_function_audit_he}</div>` : ''}
            ${item.maneuvering_aisle_audit_he ? `<div style="margin-top:3px;font-size:11px;color:#1e40af;background:#eff6ff;padding:3px 6px;border-radius:4px;border-right:3px solid #3b82f6;"><strong>🅿️ שטחי תמרון ומיסעות מוגנים:</strong> ${item.maneuvering_aisle_audit_he}</div>` : ''}
            <div style="font-size:11px;color:#0369a1;margin-top:3px;font-weight:700;">🅿️ שמירת חניות ותמרון: ${item.parking_spaces_preserved}</div>
          </td>
          <td style="text-align:center;">
            ${item.note_id ? `<button type="button" class="btn-locate-on-plan" data-note-id="${item.note_id}" data-sheet-id="${item.sheet_id}">📍 הצג על תכנית המקור (#${item.pin_num})</button>` : '-'}
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

    const baseAgSaved = Number(kpis.above_ground_saved_sqm || 0);
    const baseUgSaved = Number(kpis.underground_saved_sqm || 0);
    const totalOpaque = Number(facOpt.total_opaque_wall_sqm || 1000);
    const recConvPct = totalOpaque > 0 ? Math.round((Number(kpis.facade_converted_to_plaster_sqm || 0) / totalOpaque) * 100) : 35;

    const agBeforeSqm = Number(agOpt.current_total_above_ground_sqm || 1);
    const agAfterSqm = Number(agOpt.optimized_total_above_ground_sqm || agBeforeSqm);
    const agAfterPct = Math.max(60, Math.min(99, Math.round((agAfterSqm / agBeforeSqm) * 100)));

    const ugBeforeSqm = Number(ugOpt.current_total_underground_sqm || 1);
    const ugAfterSqm = Number(ugOpt.optimized_total_underground_sqm || ugBeforeSqm);
    const ugAfterPct = Math.max(60, Math.min(99, Math.round((ugAfterSqm / ugBeforeSqm) * 100)));

    valueEngModalBody.innerHTML = `
      <!-- Top 4 Construction Cost Savings KPI Boxes (Always Visible Summary Header) -->
      <div class="modal-kpi-strip" style="grid-template-columns: repeat(4, 1fr); margin-bottom: 12px;">
        <div class="modal-kpi-box" style="border-top-color:#059669;background:#ecfdf5;">
          <div class="k-title" style="color:#065f46;">💰 סה״כ חיסכון בעלויות הבנייה</div>
          <div class="k-num" style="color:#047857;" id="ve-kpi-grand-total">${fmtNum(kpis.grand_total_direct_saving_ils)} ₪</div>
          <div class="k-desc" style="color:#065f46;">אך ורק מקונטור שנבנה פחות + חיפוי</div>
        </div>
        <div class="modal-kpi-box" style="border-top-color:#2563eb;">
          <div class="k-title">🏢 צמצום קונטור עילי מאומת (6,200 ₪/מ״ר)</div>
          <div class="k-num" id="ve-kpi-ag-ils">${fmtNum(kpis.above_ground_saving_ils)} ₪</div>
          <div class="k-desc">נבנה פחות: ${fmtNum(kpis.above_ground_saved_sqm)} מ״ר (נוכו ${fmtNum(contourAudit.rejected_locked_ag_core_sqm)} מ״ר ליבה כלואה)</div>
        </div>
        <div class="modal-kpi-box" style="border-top-color:#0284c7;">
          <div class="k-title">🅿️ צמצום קונטור חניון מאומת (3,500 ₪/מ״ר)</div>
          <div class="k-num" id="ve-kpi-ug-ils">${fmtNum(kpis.underground_saving_ils)} ₪</div>
          <div class="k-desc">נבנה פחות: ${fmtNum(kpis.underground_saved_sqm)} מ״ר (נוכו ${fmtNum(contourAudit.rejected_locked_ug_zone_sqm)} מ״ר רמפה ותמרון)</div>
        </div>
        <div class="modal-kpi-box" style="border-top-color:#d97706;">
          <div class="k-title">🧱 חיפוי יבש מול טיח (400 ₪/מ״ר)</div>
          <div class="k-num" id="ve-kpi-fac-ils">${fmtNum(kpis.facade_saving_ils)} ₪</div>
          <div class="k-desc">המרת <span id="ve-kpi-fac-sqm">${fmtNum(kpis.facade_converted_to_plaster_sqm)}</span> מ״ר מחיפוי יבש (700 ₪) לטיח (300 ₪)</div>
        </div>
      </div>

      <!-- UNIFIED SAVINGS COMMAND CENTER TAB NAVIGATION BAR (Click to switch views cleanly) -->
      <div class="ve-hub-tabs-bar">
        <button type="button" class="ve-hub-tab-btn active" data-ve-tab="overview">
          📊 1. מבט על וסימולטור חיסכון
        </button>
        <button type="button" class="ve-hub-tab-btn" data-ve-tab="gallery">
          🖼️ 2. כרטיסיות המלצה ופתרון (${veAndImpNotes.length})
        </button>
        <button type="button" class="ve-hub-tab-btn" data-ve-tab="ag">
          🏢 3. קונטור עילי (-${fmtNum(agOpt.total_saved_sqm)} מ״ר)
        </button>
        <button type="button" class="ve-hub-tab-btn" data-ve-tab="ug">
          🅿️ 4. מרתף חניון, רמפות ותמרון (-${fmtNum(ugOpt.total_saved_sqm)} מ״ר)
        </button>
        <button type="button" class="ve-hub-tab-btn" data-ve-tab="fac">
          🧱 5. חזיתות וחיפוי (${fmtNum(facOpt.recommended_saving_ils)} ₪)
        </button>
        <button type="button" class="ve-hub-tab-btn" data-ve-tab="locked">
          🛋️ 6. ליבה כלואה ושיפור תכנון (+${fmtNum(kpis.total_design_improvement_sqm)} מ״ר)
        </button>
      </div>

      <!-- TAB 1: OVERVIEW, BEFORE/AFTER BOARD & LIVE SIMULATOR -->
      <div class="ve-hub-tab-pane active" data-ve-pane="overview">
        <!-- Zero-Damage & Contour Shrinkage Guarantee Banner -->
        <div class="ve-guarantee-banner">
          <div>
            <strong>📐 מנגנון בקרת כיווץ קונטור הבניין (Global Building Contour Contraction Audit):</strong>
            ${contourAudit.audit_rule_he || 'חיסכון בעלויות הבנייה מוכר אך ורק כאשר הקטנת שטח ליבה/מרתף מקטינה בפועל את קונטור הבניין הכולל (סך הכל נבנה פחות).'}
          </div>
          <div style="white-space:nowrap;background:#059669;color:#fff;padding:6px 12px;border-radius:8px;font-weight:900;">
            רק קונטור שנבנה פחות = חיסכון | ליבה כלואה = שיפור תכנון
          </div>
        </div>

        <!-- Visual Whole-Building Before vs. After Impact Board -->
        <div class="ve-visual-flow-board">
          <div class="ve-flow-header">
            <div class="ve-flow-title">🏢 תמונת המצב הוויזואלית על הבניין: לפני ואחרי התייעלות (המלצה ← פתרון ← חיסכון ← השפעה על הבניין)</div>
            <span style="font-size:12px;font-weight:800;color:#047857;background:#ecfdf5;padding:4px 10px;border-radius:999px;border:1px solid #6ee7b7;">
              0% פגיעה בדירות (${fmtNum(guar.apartment_saleable_area_preserved_sqm)} מ״ר פלדלת) · 100% שמירת חניות (${guar.parking_spaces_preserved || guar.parking_stalls_after || ''})
            </span>
          </div>
          <div class="ve-bldg-before-after-grid">
            <div class="ve-bldg-compare-card">
              <h4>🏢 1. קונטור בנייה עילי כולל (6,200 ₪/מ״ר)</h4>
              <div class="ve-bar-pair">
                <div class="ve-bar-row">
                  <div class="ve-bar-lbl"><span>לפני (תכנון נוכחי):</span><strong>${fmtNum(agBeforeSqm)} מ״ר</strong></div>
                  <div class="ve-bar-track"><div class="ve-bar-fill fill-before" style="width:100%;">100%</div></div>
                </div>
                <div class="ve-bar-row">
                  <div class="ve-bar-lbl"><span>אחרי כיווץ קונטור עילי (-${fmtNum(agOpt.total_saved_sqm)} מ״ר):</span><strong style="color:#047857;">${fmtNum(agAfterSqm)} מ״ר (חיסכון ${fmtNum(agOpt.total_saving_ils)} ₪)</strong></div>
                  <div class="ve-bar-track"><div class="ve-bar-fill fill-after" style="width:${agAfterPct}%;">נבנה פחות: -${fmtNum(agOpt.total_saved_sqm)} מ״ר</div></div>
                </div>
              </div>
            </div>

            <div class="ve-bldg-compare-card">
              <h4>🅿️ 2. קונטור דיפון ומרתפי חניון (3,500 ₪/מ״ר)</h4>
              <div class="ve-bar-pair">
                <div class="ve-bar-row">
                  <div class="ve-bar-lbl"><span>לפני (${ugOpt.current_sqm_per_stall} מ״ר/חניה):</span><strong>${fmtNum(ugBeforeSqm)} מ״ר</strong></div>
                  <div class="ve-bar-track"><div class="ve-bar-fill fill-before" style="width:100%;">100%</div></div>
                </div>
                <div class="ve-bar-row">
                  <div class="ve-bar-lbl"><span>אחרי כיווץ דיפון (-${fmtNum(ugOpt.total_saved_sqm)} מ״ר · ${ugOpt.optimized_sqm_per_stall} מ״ר/חניה):</span><strong style="color:#047857;">${fmtNum(ugAfterSqm)} מ״ר (חיסכון ${fmtNum(ugOpt.total_saving_ils)} ₪)</strong></div>
                  <div class="ve-bar-track"><div class="ve-bar-fill fill-after" style="width:${ugAfterPct}%;">נבנה פחות: -${fmtNum(ugOpt.total_saved_sqm)} מ״ר</div></div>
                </div>
              </div>
            </div>

            <div class="ve-bldg-compare-card">
              <h4>🧱 3. מעטפת חזיתות + 🛋️ שטחים שהועברו לשיפור תכנון</h4>
              <div class="ve-bar-pair">
                <div class="ve-bar-row">
                  <div class="ve-bar-lbl"><span>חיפוי יבש מול טיח (${facOpt.optimized_dry_cladding_pct}% יבש / ${facOpt.optimized_plaster_pct}% טיח):</span><strong style="color:#047857;">חיסכון ${fmtNum(facOpt.recommended_saving_ils)} ₪</strong></div>
                  <div class="ve-bar-track"><div class="ve-bar-fill fill-after" style="width:${100 - (facOpt.optimized_plaster_pct || 30)}%;">${facOpt.optimized_dry_cladding_pct}% יבש</div></div>
                </div>
                <div class="ve-bar-row">
                  <div class="ve-bar-lbl"><span>שטחים כלואים ומסדרונות שהפכו לחדרים מרווחים (0 ₪ שלד):</span><strong style="color:#1d4ed8;">+${fmtNum(kpis.total_design_improvement_sqm)} מ״ר שיפור תכנון</strong></div>
                  <div class="ve-bar-track"><div class="ve-bar-fill fill-imp-bar" style="width:100%;">+${fmtNum(kpis.total_design_improvement_sqm)} מ״ר שטח שימושי נטו בדירות ובבניין</div></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- INTERACTIVE VALUE ENGINEERING & CLADDING SIMULATOR -->
        <div class="ve-simulator-box">
          <div class="ve-sim-header">
            <div>
              <div class="ve-sim-title">🧮 סימולטור חיסכון אינטראקטיבי — צמצום קונטור בנייה מאומת ויחס חיפוי יבש/טיח</div>
              <div style="font-size:12px;color:#94a3b8;margin-top:2px;">הזז את המחוונים כדי לבחון תרחישי צמצום קונטור עילי (6,200 ₪/מ״ר), קונטור חניון (3,500 ₪/מ״ר) והמרת חיפוי יבש לטיח (700 ₪ לעומת 300 ₪ למ״ר)</div>
            </div>
            <div class="ve-sim-total-pill" id="ve-sim-live-total">
              סה״כ חיסכון בסימולציה: ${fmtNum(kpis.grand_total_direct_saving_ils)} ₪
            </div>
          </div>

          <div class="ve-sim-controls-grid">
            <div class="ve-sim-control-card">
              <label>
                <span>🏢 שטח קונטור עילי נחסך (6,200 ₪/מ״ר):</span>
                <strong id="sim-lbl-ag-sqm">${baseAgSaved} מ״ר</strong>
              </label>
              <input type="range" id="sim-range-ag-sqm" min="0" max="${Math.max(150, Math.round(baseAgSaved * 1.6))}" step="1" value="${baseAgSaved}" />
              <div class="sim-sub-val" id="sim-val-ag-ils">חיסכון עילי: ${fmtNum(baseAgSaved * 6200)} ₪</div>
            </div>

            <div class="ve-sim-control-card">
              <label>
                <span>🅿️ שטח קונטור חניון נחסך (3,500 ₪/מ״ר):</span>
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

        <!-- Contour Audit Executive Breakdown Card -->
        <div class="modal-section-card" style="border:2px solid #0284c7;background:#f0f9ff;margin-bottom:0;">
          <h3 style="color:#0369a1;margin-bottom:8px;">🔍 דו״ח סינון ובקרת כיווץ קונטור הבניין — הפרדה הנדסית בין חיסכון בבנייה לשיפור תכנון</h3>
          <div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:10px;margin-bottom:10px;">
            <div style="background:#fff;border:1px solid #bae6fd;border-radius:8px;padding:9px 12px;">
              <div style="font-size:11px;font-weight:800;color:#475569;">1. סך שטחים שנבדקו להפחתה</div>
              <div style="font-size:19px;font-weight:900;color:#0f172a;">${fmtNum(contourAudit.total_proposed_raw_reduction_sqm)} מ״ר</div>
              <div style="font-size:10.5px;color:#64748b;">ליבה עילית + מרתפים + מסדרונות דירה</div>
            </div>
            <div style="background:#ecfdf5;border:1px solid #6ee7b7;border-radius:8px;padding:9px 12px;">
              <div style="font-size:11px;font-weight:800;color:#065f46;">2. ✅ הקטין קונטור בניין/מרתף (נבנה פחות)</div>
              <div style="font-size:19px;font-weight:900;color:#047857;">${fmtNum(contourAudit.total_verified_contour_saved_sqm)} מ״ר</div>
              <div style="font-size:10.5px;color:#065f46;">עילי: ${fmtNum(contourAudit.verified_ag_contour_saved_sqm)} מ״ר | מרתף: ${fmtNum(contourAudit.verified_ug_contour_saved_sqm)} מ״ר</div>
            </div>
            <div style="background:#eff6ff;border:1px solid #93c5fd;border-radius:8px;padding:9px 12px;">
              <div style="font-size:11px;font-weight:800;color:#1e40af;">3. 🔄 ליבה/מרתף כלואים ומוגני תמרון</div>
              <div style="font-size:19px;font-weight:900;color:#1d4ed8;">${fmtNum(contourAudit.rejected_locked_core_and_service_sqm)} מ״ר</div>
              <div style="font-size:10.5px;color:#1e3a8a;">0 ₪ חיסכון שלד ← הועבר לשיפור תכנון!</div>
            </div>
            <div style="background:#eff6ff;border:1px solid #93c5fd;border-radius:8px;padding:9px 12px;">
              <div style="font-size:11px;font-weight:800;color:#1e40af;">4. 🛋️ מסדרונות פנים-דירתיים שהומרו לחדרים</div>
              <div style="font-size:19px;font-weight:900;color:#1d4ed8;">${fmtNum(contourAudit.rejected_internal_apt_corridor_sqm)} מ״ר</div>
              <div style="font-size:10.5px;color:#1e3a8a;">קונטור דירה קבוע ← הועבר לשיפור תכנון!</div>
            </div>
          </div>
          <details style="background:#fff;border:1px solid #cbd5e1;border-radius:6px;padding:8px 10px;">
            <summary style="cursor:pointer;font-weight:800;font-size:12px;color:#0f172a;">📐 לחץ להצגת 5 המבחנים ההנדסיים-גיאומטריים לבדיקת הקטנת קונטור הבניין הכולל ▾</summary>
            <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(260px, 1fr));gap:8px;margin-top:8px;">
              ${pillarsHtml}
            </div>
          </details>
        </div>
      </div>

      <!-- TAB 2: VISUAL 4-PILLAR RECOMMENDATION CARDS GALLERY -->
      <div class="ve-hub-tab-pane" data-ve-pane="gallery">
        <div class="modal-section-card" style="background:#f8fafc;border:2px solid #cbd5e1;">
          <h3 style="margin-bottom:6px;">🖼️ כרטיסיות המחשה וויזואלית לכל המלצה (לפני מול אחרי + 4 עמודי ההסבר: המלצה · פתרון · חיסכון · השפעה על הבניין)</h3>
          <div class="sec-note">
            כל כרטיסייה מציגה שרטוט סכמטי של המצב לפני ואחרי, פירוט מלא של 4 עמודי ההסבר ההנדסיים, וכפתור <strong>📍 הצג איפה ואיך על התכנית</strong> שממקד מיד את תכנית המקור במוקד.
          </div>
          <div class="ve-cards-gallery-grid">
            ${visualGalleryCardsHtml}
          </div>
        </div>
      </div>

      <!-- TAB 3: ABOVE-GROUND BUILDING CONTOUR OPTIMIZATION -->
      <div class="ve-hub-tab-pane" data-ve-pane="ag">
        <div class="modal-section-card">
          <h3>🏢 צמצום קונטור הבניין ושטחים עיליים (6,200 ₪ למ״ר קונטור נחסך · בניכוי שטחי ליבה כלואים שלא הקטינו קונטור)</h3>
          <div class="sec-note">
            קונטור בנייה עילי נוכחי: <strong>${fmtNum(agOpt.current_total_above_ground_sqm)} מ״ר</strong> ·
            קונטור עילי לאחר כיווץ: <strong>${fmtNum(agOpt.optimized_total_above_ground_sqm)} מ״ר</strong> ·
            סך הפחתת ליבה/שירות שנבדקה: <strong>${fmtNum(agOpt.proposed_gross_reduction_sqm || agOpt.total_saved_sqm)} מ״ר</strong>, מתוכה <strong style="color:#1d4ed8;">${fmtNum(agOpt.rejected_locked_core_sqm || 0)} מ״ר ליבה כלואה/תחת תקרה קשיחה קוזזו לשיפור תכנון (0 ₪)</strong>, ו-<strong style="color:#047857;">${fmtNum(agOpt.total_saved_sqm)} מ״ר הקטינו בפועל את קונטור הבניין (${fmtNum(agOpt.total_saving_ils)} ₪)</strong>!
          </div>
          <table class="modal-data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>קומה / אזור בבניין</th>
                <th>שטח ליבה נוכחי</th>
                <th>הפחתת ליבה גולמית</th>
                <th>ליבה כלואה שלא הקטינה קונטור (0 ₪)</th>
                <th>קונטור נחסך בפועל (נבנה פחות)</th>
                <th>חיסכון כספי (6,200 ₪/מ״ר)</th>
                <th>איפה ואיך בתכנית + הוכחת כיווץ קונטור גיאומטרית</th>
                <th>מיקום על התכנית</th>
              </tr>
            </thead>
            <tbody>
              ${agOptRows}
              <tr class="total-row">
                <td colspan="2">סה״כ צמצום קונטור בנייה עילי מאומת</td>
                <td>${fmtNum(agOpt.current_core_and_service_sqm)} מ״ר</td>
                <td>${fmtNum(agOpt.proposed_gross_reduction_sqm || agOpt.total_saved_sqm)} מ״ר</td>
                <td style="color:#1d4ed8;">${fmtNum(agOpt.rejected_locked_core_sqm || 0)} מ״ר ← שיפור תכנון</td>
                <td style="background:#ecfdf5;color:#047857;">${fmtNum(agOpt.total_saved_sqm)} מ״ר</td>
                <td style="background:#dcfce7;color:#065f46;">${fmtNum(agOpt.total_saving_ils)} ₪</td>
                <td colspan="2">0% פגיעה בשטח הפלדלת של הדירות (${fmtNum(guar.apartment_saleable_area_preserved_sqm)} מ״ר נשמרים במלואם)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- TAB 4: UNDERGROUND PARKING, RAMP FUNCTION & MANEUVERING AUDIT -->
      <div class="ve-hub-tab-pane" data-ve-pane="ug">
        <div class="modal-section-card">
          <h3>🅿️ צמצום קונטור דיפון וחפירה במרתף החניון (3,500 ₪ למ״ר קונטור נחסך · 100% שמירה על מצבת החניות, תפקוד רמפות ושטחי תמרון)</h3>
          <div class="sec-note">
            קונטור מרתף נוכחי: <strong>${fmtNum(ugOpt.current_total_underground_sqm)} מ״ר</strong> (${ugOpt.current_sqm_per_stall} מ״ר/חניה) ·
            קונטור מרתף לאחר כיווץ דיפון: <strong>${fmtNum(ugOpt.optimized_total_underground_sqm)} מ״ר</strong> (${ugOpt.optimized_sqm_per_stall} מ״ר/חניה) ·
            מתוך <strong>${fmtNum(ugOpt.proposed_gross_reduction_sqm || ugOpt.total_saved_sqm)} מ״ר</strong> שנבדקו, <strong style="color:#b45309;">${fmtNum(ugOpt.rejected_locked_zone_sqm || 0)} מ״ר מוגנים לנתיבי רמפות ירידה, רדיוסי סיבוב (R_in ≥ 3.0–5.0m), מיסעות דו-סטריות (6.00 מ׳) ואוזני תמרון לחניות קצה (0 ₪)</strong>, <strong style="color:#1d4ed8;">${fmtNum((ugOpt.ramp_and_maneuvering_audit || {}).total_under_ramp_utilized_sqm || 0)} מ״ר נוצלו מתחת למקטע הגבוה של הרמפה (H_clear ≥ 2.20 מ׳)</strong>, ו-<strong style="color:#047857;">${fmtNum(ugOpt.total_saved_sqm)} מ״ר הקטינו בפועל את קו הדיפון (${fmtNum(ugOpt.total_saving_ils)} ₪)</strong>!
          </div>
          ${ugOpt.ramp_and_maneuvering_audit ? `
            <div style="background:#fffbeb;border:1px solid #fcd34d;border-right:4px solid #f59e0b;border-radius:8px;padding:8px 12px;margin-bottom:10px;font-size:11.5px;color:#78350f;line-height:1.45;">
              <div style="font-weight:900;color:#92400e;margin-bottom:3px;">🛣️ ממצאי בקרת הנדסת תנועה, תפקוד רמפות ירידה, שטחי תמרון והעתקת חניות למקום חלופי על תכניות המקור:</div>
              <div>• <strong>בקרת רמפה וגובה ראש פנוי (H_clear ≥ 2.15–2.20 מ׳):</strong> ${ugOpt.ramp_and_maneuvering_audit.audit_statement_he || ''}</div>
              ${ugOpt.ramp_and_maneuvering_audit.parking_relocation_rule_he ? `<div style="margin-top:4px;color:#0e7490;background:#ecfeff;padding:5px 8px;border-radius:5px;border:1px solid #67e8f9;">• <strong>🔄🅿️ חוק ברזל להעתקת חניות (סה״כ ${ugOpt.ramp_and_maneuvering_audit.total_stalls_relocated_to_alternative_bays || 1} חניות הועתקו למפרץ חלופי מאומת):</strong> ${ugOpt.ramp_and_maneuvering_audit.parking_relocation_rule_he}</div>` : ''}
            </div>
          ` : ''}
          <table class="modal-data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>מוקד במרתף החניון</th>
                <th>שטח מרתף נוכחי</th>
                <th>הפחתה גולמית שנבדקה</th>
                <th>שטח מוגן לרמפה, רדיוס סיבוב ותמרון חניות (0 ₪)</th>
                <th>קונטור דיפון נחסך (נבנה פחות)</th>
                <th>חיסכון כספי (3,500 ₪/מ״ר)</th>
                <th>איפה ואיך על תכנית המקור + בקרת רמפות, תמרון והוכחת כיווץ דיפון</th>
                <th>מיקום על תכנית המקור</th>
              </tr>
            </thead>
            <tbody>
              ${ugOptRows}
            </tbody>
          </table>
        </div>
      </div>

      <!-- TAB 5: FACADE CLADDING VS. PLASTER OPTIMIZATION -->
      <div class="ve-hub-tab-pane" data-ve-pane="fac">
        <div class="modal-section-card">
          <h3>🧱 אופטימיזציית יחס חיפוי קשיח/יבש (700 ₪/מ״ר) לעומת טיח חוץ (300 ₪/מ״ר · חיסכון 400 ₪/מ״ר)</h3>
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
      </div>

      <!-- TAB 6: RECLASSIFIED LOCKED-CORE & APARTMENT DESIGN IMPROVEMENTS -->
      <div class="ve-hub-tab-pane" data-ve-pane="locked">
        <div class="modal-section-card" style="border-color:#93c5fd;background:#eff6ff;">
          <h3 style="color:#1e3a8a;">🔄 שטחי ליבה ושירות שירדו אך לא הקטינו את קונטור הבניין הכולל — הועברו ממודל החיסכון (0 ₪) ל"שיפור תכנון"</h3>
          <div class="sec-note" style="background:#dbeafe;color:#1e3a8a;">
            המוקדים הבאים מקטינים שטחי ליבה או מעברי שירות, אך מאחר שהם כלואים גיאומטרית בין דירות/עמודים (מבחן 1) או נמצאים מתחת לתקרת קומה א׳ קשיחה שממילא נבנית (מבחן 2), סך שטח הבנייה הכולל לא קטן. לכן הם <strong>אינם נספרים כחיסכון בעלויות הבנייה (0 ₪)</strong> ומסווגים תחת <strong>שיפור תכנון</strong>.
          </div>
          <table class="modal-data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>מוקד ליבה / שירות בבניין</th>
                <th>שטח ליבה שירד</th>
                <th>הקטנת קונטור בניין בפועל</th>
                <th>חיסכון בבנייה</th>
                <th>סיווג מחדש</th>
                <th>ניתוח הנדסי: מדוע הקונטור נעול ומהו שיפור התכנון</th>
                <th>מיקום על התכנית</th>
              </tr>
            </thead>
            <tbody>
              ${lockedCoreRows}
            </tbody>
          </table>
        </div>
      </div>
    `;

    // Wire up Tab Switching inside Unified Cost Savings Command Center
    valueEngModalBody.querySelectorAll('.ve-hub-tab-btn').forEach((tabBtn) => {
      tabBtn.addEventListener('click', () => {
        const targetTab = tabBtn.getAttribute('data-ve-tab');
        valueEngModalBody.querySelectorAll('.ve-hub-tab-btn').forEach((b) => b.classList.toggle('active', b === tabBtn));
        valueEngModalBody.querySelectorAll('.ve-hub-tab-pane').forEach((pane) => {
          pane.classList.toggle('active', pane.getAttribute('data-ve-pane') === targetTab);
        });
      });
    });

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

    // Wire up "הצג איפה ואיך על התכנית" buttons inside the modal tables and cards
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

  function jumpToSystemFilter(polarity, category) {
    currentPolarity = polarity || 'ALL';
    currentCategory = category || 'ALL';
    polarityBtns.forEach((b) => b.classList.toggle('active', b.dataset.polarity === currentPolarity));
    catFilterBtns.forEach((b) => b.classList.toggle('active', b.dataset.category === currentCategory));
    if (currentProject) {
      updateSystemFilterCounts(currentProject);
    }
    switchWorkMode('FINDINGS', { preserveSubfilters: true });
  }

  function buildOverviewModeElement(data) {
    const pds = data.project_data_summary || {};
    const opt = pds.design_optimization || {};
    const optKpis = opt.executive_kpis || {};
    const contourAudit = opt.contour_audit_summary || {};
    const sdoc = pds.summary_document || {};
    const notes = data.notes || [];
    const sysNotes = notes.filter((n) => !n.is_value_eng);
    const veNotes = notes.filter((n) => Boolean(n.is_value_eng));

    const negNotes = sysNotes.filter((n) => classifySystemNote(n).polarity === 'NEGATIVE');
    const posNotes = sysNotes.filter((n) => classifySystemNote(n).polarity === 'POSITIVE');

    const groupByCat = (list) => ({
      STANDARD: list.filter((n) => classifySystemNote(n).category === 'STANDARD'),
      ARCH_QUALITY: list.filter((n) => classifySystemNote(n).category === 'ARCH_QUALITY'),
      INTERIOR_TIP: list.filter((n) => classifySystemNote(n).category === 'INTERIOR_TIP'),
    });

    const negByCat = groupByCat(negNotes);
    const posByCat = groupByCat(posNotes);

    const catMeta = [
      { key: 'STANDARD', label: 'תקן', icon: '⚖️' },
      { key: 'ARCH_QUALITY', label: 'איכות תכנון אדריכלי', icon: '📐' },
      { key: 'INTERIOR_TIP', label: 'טיפ עיצוב פנים', icon: '🛋️' },
    ];

    const renderGroupRows = (grouped, polarity) =>
      catMeta
        .map((cm) => {
          const items = grouped[cm.key] || [];
          if (items.length === 0) return '';
          const bulletsHtml = items
            .map(
              (n) => `
              <li class="ov-verbal-bullet" data-note-id="${n.id}">
                <span class="ov-bullet-pin">#${n.pin_num}</span>
                <div class="ov-bullet-body">
                  <strong>${n.room_name} — ${n.title}:</strong>
                  <span>${n.measured}${n.recommendation ? ` · <em>${n.recommendation}</em>` : ''}</span>
                </div>
              </li>
            `
            )
            .join('');
          return `
            <div class="ov-verbal-cat-block">
              <div class="ov-verbal-cat-hdr">
                <span class="ov-verbal-cat-title">${cm.icon} ${cm.label} (${items.length})</span>
                <button type="button" class="ov-filter-jump-btn" data-jump-pol="${polarity}" data-jump-cat="${cm.key}">
                  סנן ב״הערות מערכת״ ◂
                </button>
              </div>
              <ul class="ov-verbal-bullet-list">
                ${bulletsHtml}
              </ul>
            </div>
          `;
        })
        .join('');

    const overallVerdictText =
      (sdoc.concise_verbal_review && sdoc.concise_verbal_review.executive_paragraph) ||
      sdoc.overall_verdict ||
      data.project_subtitle ||
      `בדיקת התכנון האדריכלית זיהתה ${negNotes.length} הערות לטיפול ושיפור (${negByCat.STANDARD.length} תקן, ${negByCat.ARCH_QUALITY.length} איכות תכנון אדריכלי, ${negByCat.INTERIOR_TIP.length} טיפ עיצוב פנים) לצד ${posNotes.length} נקודות חוזק חיוביות בתכנון.`;

    const wrap = document.createElement('div');
    wrap.className = 'mode-overview-container';

    wrap.innerHTML = `
      <div class="ov-section-card ov-verbal-hero">
        <div class="ov-card-header-row">
          <span class="ov-card-title">📋 סקירה מילולית מתומצתת של בדיקת התכנון</span>
          <span class="ov-score-pill">ציון תכנון: ${data.overall_score || '—'}</span>
        </div>
        <p class="ov-verbal-lead">${overallVerdictText}</p>
        <div class="ov-polarity-summary-strip">
          <button type="button" class="ov-pol-chip ov-pol-neg" data-jump-pol="NEGATIVE" data-jump-cat="ALL">
            <span class="ov-pol-dot neg"></span>
            <span>שלילי / לטיפול: <strong>${negNotes.length}</strong></span>
          </button>
          <button type="button" class="ov-pol-chip ov-pol-pos" data-jump-pol="POSITIVE" data-jump-cat="ALL">
            <span class="ov-pol-dot pos"></span>
            <span>חיובי / נקודות חוזק: <strong>${posNotes.length}</strong></span>
          </button>
          <button type="button" class="ov-pol-chip ov-pol-ve" id="ov-switch-ve-tab">
            <span>💰 טאב חיסכון: <strong>${veNotes.length}</strong></span>
          </button>
        </div>
      </div>

      <div class="ov-section-card ov-verbal-card ov-verbal-negative">
        <div class="ov-card-header-row">
          <span class="ov-card-title">🔴 תמצית ממצאים שליליים לטיפול (${negNotes.length})</span>
          <button type="button" class="btn-link-Action" data-jump-pol="NEGATIVE" data-jump-cat="ALL">כל השליליים ◂</button>
        </div>
        <div class="ov-verbal-groups">
          ${renderGroupRows(negByCat, 'NEGATIVE')}
        </div>
      </div>

      <div class="ov-section-card ov-verbal-card ov-verbal-positive">
        <div class="ov-card-header-row">
          <span class="ov-card-title">🟢 תמצית נקודות חוזק חיוביות בתכנון (${posNotes.length})</span>
          <button type="button" class="btn-link-Action" data-jump-pol="POSITIVE" data-jump-cat="ALL">כל החיוביים ◂</button>
        </div>
        <div class="ov-verbal-groups">
          ${renderGroupRows(posByCat, 'POSITIVE')}
        </div>
      </div>

      <div class="ov-section-card">
        <div class="ov-kpi-pair">
          <div class="ov-kpi-box" id="ov-open-ve">
            <span class="ov-kpi-lbl">פוטנציאל חיסכון (בטאב נפרד)</span>
            <strong class="ov-kpi-val">${fmtNum(optKpis.grand_total_direct_saving_ils)} ₪</strong>
            <span class="ov-kpi-sub">-${fmtNum(contourAudit.total_verified_contour_saved_sqm)} מ״ר קונטור (${veNotes.length} מוקדים)</span>
          </div>
          <div class="ov-kpi-box" id="ov-open-areas">
            <span class="ov-kpi-lbl">מאזן שטחים ושיפור תכנון</span>
            <strong class="ov-kpi-val">+${fmtNum(optKpis.total_design_improvement_sqm)} מ״ר</strong>
            <span class="ov-kpi-sub">טבלאות שטחים והשבחת פנים</span>
          </div>
        </div>
      </div>
    `;

    const veBox = wrap.querySelector('#ov-open-ve');
    if (veBox) veBox.addEventListener('click', () => switchWorkMode('OPTIMIZATION'));

    const switchVeBtn = wrap.querySelector('#ov-switch-ve-tab');
    if (switchVeBtn) switchVeBtn.addEventListener('click', () => switchWorkMode('OPTIMIZATION'));

    const areasBox = wrap.querySelector('#ov-open-areas');
    if (areasBox) areasBox.addEventListener('click', () => openSummaryAreasModal(data));

    wrap.querySelectorAll('[data-jump-pol]').forEach((btn) => {
      btn.addEventListener('click', () => {
        jumpToSystemFilter(btn.getAttribute('data-jump-pol'), btn.getAttribute('data-jump-cat'));
      });
    });

    wrap.querySelectorAll('.ov-verbal-bullet[data-note-id]').forEach((li) => {
      li.addEventListener('click', () => {
        const nid = li.getAttribute('data-note-id');
        if (nid) {
          highlightNote(nid, { scrollDoc: false, switchSheet: true, openDock: true, zoomTo: true });
        }
      });
    });

    return wrap;
  }

  function buildCompareModeElement(data) {
    const pds = data.project_data_summary || {};
    const ag = pds.above_ground_areas || {};
    const ug = pds.underground_areas || {};
    const opt = pds.design_optimization || {};
    const agOpt = opt.above_ground_optimization || {};
    const ugOpt = opt.underground_optimization || {};
    const facOpt = opt.facade_cladding_optimization || {};
    const veNotes = (data.notes || []).filter((n) => n.is_value_eng || n.is_design_improvement);

    const wrap = document.createElement('div');
    wrap.className = 'mode-compare-container';

    wrap.innerHTML = `
      <div class="ov-section-card">
        <div class="ov-card-title">קיים מול מומלץ</div>
        <table class="compact-compare-table">
          <thead>
            <tr>
              <th>רכיב</th>
              <th>קיים</th>
              <th>מומלץ</th>
              <th>הפרש</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>קונטור עילי</strong></td>
              <td>${fmtNum(agOpt.current_total_above_ground_sqm || ag.total_sqm)} מ״ר</td>
              <td>${fmtNum(agOpt.optimized_total_above_ground_sqm || ag.total_sqm)} מ״ר</td>
              <td>-${fmtNum(agOpt.total_saved_sqm)} מ״ר</td>
            </tr>
            <tr>
              <td><strong>קונטור מרתף</strong></td>
              <td>${fmtNum(ugOpt.current_total_underground_sqm || ug.total_sqm)} מ״ר</td>
              <td>${fmtNum(ugOpt.optimized_total_underground_sqm || ug.total_sqm)} מ״ר</td>
              <td>-${fmtNum(ugOpt.total_saved_sqm)} מ״ר</td>
            </tr>
            <tr>
              <td><strong>שטח דירות</strong></td>
              <td>${fmtNum(ag.net_apartments_sqm)} מ״ר</td>
              <td>${fmtNum(ag.net_apartments_sqm)} מ״ר</td>
              <td>ללא שינוי</td>
            </tr>
            <tr>
              <td><strong>חיפוי יבש</strong></td>
              <td>${fmtNum(facOpt.baseline_dry_cladding_sqm)} מ״ר</td>
              <td>${fmtNum(facOpt.optimized_dry_cladding_sqm)} מ״ר</td>
              <td>-${fmtNum(facOpt.recommended_saving_ils)} ₪</td>
            </tr>
          </tbody>
        </table>
        <div style="display:flex;gap:6px;margin-top:10px;">
          <button type="button" class="btn-locate-on-plan" id="cmp-btn-open-ve" style="flex:1;">פירוט חיסכון</button>
          <button type="button" class="btn-locate-on-plan" id="cmp-btn-open-areas" style="flex:1;">טבלאות שטחים</button>
        </div>
      </div>

      <div class="ov-section-card">
        <div class="ov-card-title">מוקדים להשוואה (${veNotes.length})</div>
        <div id="cmp-notes-list"></div>
      </div>
    `;

    const btnVe = wrap.querySelector('#cmp-btn-open-ve');
    if (btnVe) btnVe.addEventListener('click', () => openValueEngineeringModal(data));

    const btnAreas = wrap.querySelector('#cmp-btn-open-areas');
    if (btnAreas) btnAreas.addEventListener('click', () => openSummaryAreasModal(data));

    const listEl = wrap.querySelector('#cmp-notes-list');
    veNotes.forEach((n) => {
      listEl.appendChild(createLevel1NoteCard(n));
    });

    return wrap;
  }

  function buildInlineNoteDetailsHtml(note) {
    return `
      <div class="fc-metrics-row" style="margin-top:8px;">
        <div class="fc-metric-box metric-current">
          <span class="fc-metric-label">קיים</span>
          <strong class="fc-metric-big">${note.measured || ''}</strong>
        </div>
        <div class="fc-metric-box metric-target">
          <span class="fc-metric-label">יעד / מומלץ</span>
          <strong class="fc-metric-big">${note.benchmark || ''}</strong>
        </div>
      </div>
      ${buildFourPillarsSideDockHtml(note)}
      <div style="display:flex;align-items:center;justify-content:space-between;gap:6px;margin-top:6px;">
        <button type="button" class="ctrl-btn btn-inline-center-plan" style="flex:1;justify-content:center;" title="מרכז ממצא בשרטוט ובמודל התלת-ממדי">
          🎯 מרכז בשרטוט / מודל 3D
        </button>
      </div>
    `;
  }

  function wireInlineExpandedEvents(containerEl, note) {
    if (!containerEl || !note) return;
    containerEl.addEventListener('click', (e) => {
      e.stopPropagation();
    });
    containerEl.querySelectorAll('.btn-dec-state').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const decVal = btn.getAttribute('data-dec');
        setNoteDecision(note.id, decVal);
        renderDocumentSections(currentProject);
      });
    });
    const centerBtn = containerEl.querySelector('.btn-inline-center-plan');
    if (centerBtn) {
      centerBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        panAndZoomToNoteOnPlan(note);
        postMessageTo3D({ type: 'ARCHICHECK_SELECT_NOTE', noteId: note.id });
      });
    }
  }

  function createLevel1NoteCard(note) {
    const card = document.createElement('article');
    const isVe = Boolean(note.is_value_eng);
    const isDesignImp = Boolean(note.is_design_improvement);
    const isActive = note.id === activeNoteId;
    const dec = getNoteDecision(note.id);
    const decObj = dec ? DECISION_LABELS[dec] : null;
    const clsInfo = classifySystemNote(note);

    card.className = `doc-note-card status-${note.status} ${isVe ? 'card-ve' : `polarity-${clsInfo.polarity} cat-${clsInfo.category}`} ${isDesignImp ? 'card-imp' : ''} ${isActive ? 'active' : ''}`;
    card.dataset.noteId = note.id;
    card.id = `doc-note-${note.id}`;

    let taxBadgesHtml = '';
    if (isVe) {
      const veLabel = note.ve_callout_badge || `חיסכון: ${fmtNum(note.ve_saving_ils)} ₪`;
      taxBadgesHtml = `<span class="note-ve-pill">${veLabel}</span>`;
    } else {
      const polClass = clsInfo.polarity === 'NEGATIVE' ? 'pol-neg' : 'pol-pos';
      const catClass = `cat-${clsInfo.category.toLowerCase()}`;
      taxBadgesHtml = `
        <span class="note-polarity-pill ${polClass}">${clsInfo.polarityHe}</span>
        <span class="note-cat-pill ${catClass}">${clsInfo.categoryHe}</span>
      `;
    }

    card.innerHTML = `
      <div class="note-top-row">
        <div class="note-badges-right">
          <span class="note-pin-circle">#${note.pin_num}</span>
          <span class="note-room-tag">${note.room_name}</span>
        </div>
        <div class="note-badges-left">
          ${taxBadgesHtml}
          ${decObj ? `<span class="note-dec-badge ${decObj.cls}">${decObj.label}</span>` : ''}
        </div>
      </div>
      <h3 class="note-title">${note.title}</h3>
      <div class="note-meta-line">${note.measured}</div>
      <div class="note-inline-expanded ${isActive ? '' : 'hidden'}">
        ${isActive ? buildInlineNoteDetailsHtml(note) : ''}
      </div>
    `;

    const expandedBox = card.querySelector('.note-inline-expanded');
    if (isActive && expandedBox) {
      wireInlineExpandedEvents(expandedBox, note);
    }

    card.addEventListener('mouseenter', () => {
      if (note.sheet_id === currentSheetId) {
        hoveredNoteId = note.id;
        renderVisualPlanAnnotations();
      }
    });
    card.addEventListener('mouseleave', () => {
      if (hoveredNoteId === note.id) {
        hoveredNoteId = null;
        renderVisualPlanAnnotations();
      }
    });

    card.addEventListener('click', () => {
      highlightNote(note.id, { scrollDoc: false, switchSheet: true, openDock: false, zoomTo: true });
    });

    return card;
  }

  function renderDocumentSections(data) {
    docSectionsRoot.innerHTML = '';

    if (currentWorkMode === 'OVERVIEW') {
      docSectionsRoot.appendChild(buildOverviewModeElement(data));
      return;
    }

    if (currentWorkMode === 'COMPARE') {
      docSectionsRoot.appendChild(buildCompareModeElement(data));
      return;
    }

    if (currentWorkMode === 'OPTIMIZATION') {
      const pds = data.project_data_summary || {};
      const opt = pds.design_optimization || {};
      const optKpis = opt.executive_kpis || {};
      const contourAudit = opt.contour_audit_summary || {};

      const veBanner = document.createElement('div');
      veBanner.className = 've-tab-summary-card';
      veBanner.innerHTML = `
        <div class="ve-tab-summary-row">
          <div>
            <div class="ve-tab-summary-lbl">סה״כ פוטנציאל חיסכון ישיר בבנייה</div>
            <div class="ve-tab-summary-val">${fmtNum(optKpis.grand_total_direct_saving_ils)} ₪</div>
            <div class="ve-tab-summary-sub">הקטנת קונטור מאומתת: -${fmtNum(contourAudit.total_verified_contour_saved_sqm)} מ״ר + אופטימיזציית חזיתות</div>
          </div>
          <button type="button" class="btn-locate-on-plan" id="ve-tab-open-modal">סימולטור ודו״ח חיסכון מלא ◂</button>
        </div>
      `;
      const openModalBtn = veBanner.querySelector('#ve-tab-open-modal');
      if (openModalBtn) {
        openModalBtn.addEventListener('click', () => openValueEngineeringModal(data));
      }
      docSectionsRoot.appendChild(veBanner);
    }

    const sections = data.sections || [];
    const notes = data.notes || [];
    const isFiltered =
      currentWorkMode === 'OPTIMIZATION' ||
      currentPolarity !== 'ALL' ||
      currentCategory !== 'ALL';

    let totalRendered = 0;

    sections.forEach((sec, secIdx) => {
      const secNotes = notes.filter((n) => n.section_id === sec.id && matchesFilter(n));
      if (secNotes.length === 0) return;
      totalRendered += secNotes.length;

      const secAccordion = document.createElement('details');
      secAccordion.className = 'doc-section-accordion';
      if (secIdx === 0 || isFiltered) {
        secAccordion.setAttribute('open', '');
      }

      const secSummary = document.createElement('summary');
      secSummary.className = 'doc-section-summary';
      secSummary.innerHTML = `
        <div class="doc-section-title">${sec.title}</div>
        <div class="doc-section-summary-left">
          <span class="doc-sec-count-pill">${secNotes.length}</span>
          <span class="doc-sec-chevron">▾</span>
        </div>
      `;
      secAccordion.appendChild(secSummary);

      const secNotesList = document.createElement('div');
      secNotesList.className = 'doc-section-notes-list';

      secNotes.forEach((note) => {
        secNotesList.appendChild(createLevel1NoteCard(note));
      });

      secAccordion.appendChild(secNotesList);
      docSectionsRoot.appendChild(secAccordion);
    });

    if (totalRendered === 0) {
      const emptyEl = document.createElement('div');
      emptyEl.className = 'doc-empty-filter-state';
      emptyEl.textContent = 'אין הערות בקטגוריה זו עבור הסינון שנבחר.';
      docSectionsRoot.appendChild(emptyEl);
    }
  }

  // =========================================================================
  // 5. BI-DIRECTIONAL CLICK SYNCHRONIZATION, AUTO-ZOOM & DRAWER MANAGEMENT
  // =========================================================================
  function panAndZoomToNoteOnPlan(note) {
    if (!note || !planViewport || !planImageWrapper) return;
    const cx = Number(note.cx_pct !== undefined ? note.cx_pct : (Number(note.x_pct || 50) + Number(note.w_pct || 0) / 2));
    const cy = Number(note.cy_pct !== undefined ? note.cy_pct : (Number(note.y_pct || 50) + Number(note.h_pct || 0) / 2));
    if (isNaN(cx) || isNaN(cy)) return;

    const targetScale = Math.max(scale, 1.38);
    scale = Math.min(2.4, +targetScale.toFixed(2));

    const wrapRect = planImageWrapper.getBoundingClientRect();
    const baseW = wrapRect.width / (scale || 1) || 700;
    const baseH = wrapRect.height / (scale || 1) || 520;

    // Offset from center (50%, 50%) in pixels
    const offsetX = ((50 - cx) / 100) * baseW * scale;
    const offsetY = ((50 - cy) / 100) * baseH * scale;

    panX = Math.round(offsetX);
    panY = Math.round(offsetY);
    updateStageTransform();
  }

  function highlightNote(noteId, options = { scrollDoc: false, switchSheet: true, openDock: false, zoomTo: false }) {
    if (!currentProject || !noteId) return;
    const allNotes = currentProject.notes || [];
    const note = allNotes.find((n) => n.id === noteId);
    if (!note) return;

    activeNoteId = noteId;
    if (options.openDock !== false || options.zoomTo) {
      userExplicitlySelectedNote = true;
    }

    // 1. Switch floor sheet automatically if the selected note belongs to a different sheet
    const sheetWillChange = options.switchSheet !== false && note.sheet_id !== currentSheetId;
    if (sheetWillChange) {
      selectSheet(note.sheet_id, { keepNote: true });
    }

    // 2. Left Inspector Drawer is permanently disabled — all details expand inline in the Right Panel (#doc-panel)
    toggleSideDock(false);

    // If selected from a 2D/3D pin and the note card is not currently rendered in the Right Panel, switch to its tab
    if (options.scrollDoc && !document.querySelector(`.doc-note-card[data-note-id="${noteId}"]`)) {
      if (note.is_value_eng) {
        currentVeCategory = 'ALL';
        veCatBtns.forEach((b) => b.classList.toggle('active', b.dataset.veCat === 'ALL'));
        switchWorkMode('OPTIMIZATION');
      } else {
        currentPolarity = 'ALL';
        currentCategory = 'ALL';
        polarityBtns.forEach((b) => b.classList.toggle('active', b.dataset.polarity === 'ALL'));
        catFilterBtns.forEach((b) => b.classList.toggle('active', b.dataset.category === 'ALL'));
        switchWorkMode('FINDINGS', { preserveSubfilters: true });
      }
    }

    // 3. Center and zoom to the finding's coordinates on the plan if requested
    if (options.zoomTo) {
      setTimeout(() => {
        panAndZoomToNoteOnPlan(note);
        postMessageTo3D({ type: 'ARCHICHECK_SELECT_NOTE', noteId: note.id });
      }, sheetWillChange ? 90 : 10);
    }

    // 4. Update active state and inline expanded details inside the Right-Hand Panel (#doc-panel)
    document.querySelectorAll('.doc-note-card').forEach((card) => {
      const isMatch = card.dataset.noteId === noteId;
      card.classList.toggle('active', isMatch);
      const expBox = card.querySelector('.note-inline-expanded');
      if (expBox) {
        if (isMatch) {
          expBox.innerHTML = buildInlineNoteDetailsHtml(note);
          expBox.classList.remove('hidden');
          wireInlineExpandedEvents(expBox, note);
        } else {
          expBox.classList.add('hidden');
          expBox.innerHTML = '';
        }
      }
      if (isMatch && options.scrollDoc) {
        const parentDetails = card.closest('.doc-section-accordion');
        if (parentDetails && !parentDetails.hasAttribute('open')) {
          parentDetails.setAttribute('open', '');
        }
        card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });

    // 5. Update active SVG Room Polygon, Dimming of other pins & Contour Vectors on the Plan
    renderVisualPlanAnnotations();

    // Update active state on the On-Plan Savings Navigator Bar chips
    document.querySelectorAll('.ve-hotspot-chip').forEach((chip) => {
      const isMatch = chip.dataset.noteId === noteId;
      chip.classList.toggle('active', isMatch);
      if (isMatch) {
        chip.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      }
    });

    // 6. Update Minimalist Bottom HUD Bar & 3D selection
    hudActiveNoteText.textContent = `ממצא #${note.pin_num} · ${note.room_name} — ${note.title}`;
    if (!options.from3D) {
      postMessageTo3D({ type: 'ARCHICHECK_SELECT_NOTE', noteId: note.id });
    }
  }

  function stepNote(direction) {
    if (!currentProject) return;
    const visibleNotes = (currentProject.notes || []).filter((n) => matchesFilter(n));
    if (visibleNotes.length === 0) return;
    let idx = visibleNotes.findIndex((n) => n.id === activeNoteId);
    if (idx < 0) idx = 0;
    else idx = (idx + direction + visibleNotes.length) % visibleNotes.length;
    const target = visibleNotes[idx];
    if (target) {
      highlightNote(target.id, { scrollDoc: true, switchSheet: true, openDock: true, zoomTo: true });
    }
  }

  if (btnPrevNote) {
    btnPrevNote.addEventListener('click', () => stepNote(-1));
  }
  if (btnNextNote) {
    btnNextNote.addEventListener('click', () => stepNote(1));
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

  // Toggle All Pins vs. Active Pin Only
  btnToggleAllPins.addEventListener('click', () => {
    showAllPins = !showAllPins;
    btnToggleAllPins.classList.toggle('active', showAllPins);
    btnToggleAllPins.textContent = showAllPins ? 'סיכות' : 'פעיל בלבד';
    renderVisualPlanAnnotations();
  });

  // Work Modes Switcher (סקירה · הערות מערכת · חיסכון · השוואה)
  function switchWorkMode(mode, opts = {}) {
    currentWorkMode = mode || 'FINDINGS';
    workModeTabs.forEach((t) => t.classList.toggle('active', t.dataset.mode === currentWorkMode));

    if (currentWorkMode === 'OPTIMIZATION') {
      currentFilter = 'VE';
      if (docSubfilterBar) docSubfilterBar.classList.add('hidden');
      if (veSubfilterBar) veSubfilterBar.classList.remove('hidden');
      if (btnToggleVePlanMode) btnToggleVePlanMode.classList.add('active');
      if (vePlanBar) vePlanBar.classList.remove('hidden');
    } else if (currentWorkMode === 'FINDINGS') {
      currentFilter = 'ALL';
      if (!opts.preserveSubfilters) {
        polarityBtns.forEach((b) => b.classList.toggle('active', b.dataset.polarity === currentPolarity));
        catFilterBtns.forEach((b) => b.classList.toggle('active', b.dataset.category === currentCategory));
      }
      if (docSubfilterBar) docSubfilterBar.classList.remove('hidden');
      if (veSubfilterBar) veSubfilterBar.classList.add('hidden');
      if (btnToggleVePlanMode) btnToggleVePlanMode.classList.remove('active');
      if (vePlanBar) vePlanBar.classList.add('hidden');
    } else {
      // OVERVIEW or COMPARE
      currentFilter = 'ALL';
      if (docSubfilterBar) docSubfilterBar.classList.add('hidden');
      if (veSubfilterBar) veSubfilterBar.classList.add('hidden');
      if (btnToggleVePlanMode) btnToggleVePlanMode.classList.remove('active');
      if (vePlanBar) vePlanBar.classList.add('hidden');
    }

    if (currentProject) {
      updateSystemFilterCounts(currentProject);
      renderDocumentSections(currentProject);
      renderVisualPlanAnnotations();
    }
  }

  workModeTabs.forEach((tabBtn) => {
    tabBtn.addEventListener('click', () => {
      switchWorkMode(tabBtn.dataset.mode);
    });
  });

  // Toggle On-Plan Savings Mode ("חיסכון" button on canvas toolbar)
  if (btnToggleVePlanMode) {
    btnToggleVePlanMode.addEventListener('click', () => {
      if (currentWorkMode === 'OPTIMIZATION') {
        switchWorkMode('FINDINGS');
      } else {
        switchWorkMode('OPTIMIZATION');
        if (currentProject) {
          const sheetMatch = (currentProject.notes || []).find((n) => matchesFilter(n) && n.sheet_id === currentSheetId);
          const anyMatch = sheetMatch || (currentProject.notes || []).find((n) => matchesFilter(n));
          if (anyMatch) {
            highlightNote(anyMatch.id, { scrollDoc: true, switchSheet: true, openDock: true, zoomTo: true });
          }
        }
      }
    });
  }

  // Primary Polarity Filter Buttons (הכל / שלילי / חיובי) in System Notes tab
  polarityBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      currentPolarity = btn.dataset.polarity || 'ALL';
      polarityBtns.forEach((b) => b.classList.toggle('active', b === btn));
      if (currentProject) {
        updateSystemFilterCounts(currentProject);
        renderDocumentSections(currentProject);
        renderVisualPlanAnnotations();
      }
    });
  });

  // Secondary Category Filter Buttons (הכל / תקן / איכות תכנון אדריכלי / טיפ עיצוב פנים)
  catFilterBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      currentCategory = btn.dataset.category || 'ALL';
      catFilterBtns.forEach((b) => b.classList.toggle('active', b === btn));
      if (currentProject) {
        renderDocumentSections(currentProject);
        renderVisualPlanAnnotations();
      }
    });
  });

  // VE Sub-Filter Buttons inside the separate "חיסכון" tab
  veCatBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      currentVeCategory = btn.dataset.veCat || 'ALL';
      veCatBtns.forEach((b) => b.classList.toggle('active', b === btn));
      if (currentProject) {
        renderDocumentSections(currentProject);
        renderVisualPlanAnnotations();
      }
    });
  });

  // Center on Plan button inside Side Dock
  if (btnCenterOnPlan) {
    btnCenterOnPlan.addEventListener('click', () => {
      if (!currentProject || !activeNoteId) return;
      const note = (currentProject.notes || []).find((n) => n.id === activeNoteId);
      if (note) {
        panAndZoomToNoteOnPlan(note);
        postMessageTo3D({ type: 'ARCHICHECK_SELECT_NOTE', noteId: note.id });
      }
    });
  }

  // Collapsible Top Bar Toggle
  function toggleTopBar(forceShow) {
    const isCollapsed = document.body.classList.contains('top-bar-collapsed');
    const shouldShow = forceShow !== undefined ? forceShow : isCollapsed;
    document.body.classList.toggle('top-bar-collapsed', !shouldShow);
    if (topCommandBar) {
      topCommandBar.classList.toggle('hidden', !shouldShow);
    }
    if (btnExpandTopBar) {
      btnExpandTopBar.classList.toggle('hidden', shouldShow);
    }
  }

  if (btnCollapseTopBar) {
    btnCollapseTopBar.addEventListener('click', () => toggleTopBar(false));
  }
  if (btnExpandTopBar) {
    btnExpandTopBar.addEventListener('click', () => toggleTopBar(true));
  }

  // Focus Mode Toggle (One-Click Maximize Drawing Stage)
  function toggleFocusMode(forceVal) {
    isFocusMode = forceVal !== undefined ? forceVal : !isFocusMode;
    if (btnFocusMode) {
      btnFocusMode.classList.toggle('active', isFocusMode);
      btnFocusMode.textContent = isFocusMode ? 'יציאה ממיקוד' : 'מיקוד';
    }
    if (isFocusMode) {
      if (splitWorkspaceEl) splitWorkspaceEl.classList.add('doc-collapsed');
      if (btnExpandDocPanel) btnExpandDocPanel.classList.remove('hidden');
      toggleSideDock(false);
      toggleTopBar(false);
    } else {
      if (splitWorkspaceEl) splitWorkspaceEl.classList.remove('doc-collapsed');
      if (btnExpandDocPanel) btnExpandDocPanel.classList.add('hidden');
      toggleTopBar(true);
    }
  }

  if (btnFocusMode) {
    btnFocusMode.addEventListener('click', () => toggleFocusMode());
  }

  // Export Selected Decisions Modal
  function openDecisionsExportModal() {
    if (!currentProject || !decisionsExportModal || !decisionsModalBody) return;
    const notes = currentProject.notes || [];
    const decidedNotes = notes.filter((n) => getNoteDecision(n.id));

    decisionsModalTitle.textContent = `דוח החלטות מתכנן ומעקב ביצוע — ${currentProject.project_name}`;

    if (decidedNotes.length === 0) {
      decisionsModalBody.innerHTML = `
        <div class="modal-section-card" style="text-align:center;padding:32px;">
          <h3>טרם סומנו החלטות על ממצאים בפרויקט זה</h3>
          <p class="sec-note" style="margin-top:6px;">לחץ על ממצא כלשהו ברשימה או בשרטוט, ובחר בחלונית הניתוח השמאלית את הסטטוס הרצוי: <strong>לטיפול · נבדק · אושר לביצוע · נדחה</strong>.</p>
        </div>
      `;
    } else {
      const rowsHtml = decidedNotes
        .map((n) => {
          const dCode = getNoteDecision(n.id);
          const dMeta = DECISION_LABELS[dCode] || { label: dCode, cls: '' };
          return `
            <tr>
              <td><strong>#${n.pin_num}</strong></td>
              <td><span class="note-dec-badge ${dMeta.cls}">${dMeta.label}</span></td>
              <td><strong>${n.typology} · ${n.room_name}</strong></td>
              <td>${n.title}</td>
              <td>${n.measured} ⬅️ ${n.benchmark}</td>
              <td>${(n.visual_explanation && n.visual_explanation.solution && n.visual_explanation.solution.how_to_execute) || n.how_to_execute || n.recommendation}</td>
            </tr>
          `;
        })
        .join('');

      decisionsModalBody.innerHTML = `
        <div class="modal-section-card">
          <h3>ריכוז ממצאים שנבחרו למעקב (${decidedNotes.length} ממצאים)</h3>
          <table class="modal-data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>החלטת מתכנן</th>
                <th>קומה ומיקום</th>
                <th>ממצא</th>
                <th>קיים מול יעד</th>
                <th>פעולה הנדסית לביצוע</th>
              </tr>
            </thead>
            <tbody>${rowsHtml}</tbody>
          </table>
        </div>
      `;
    }

    decisionsExportModal.classList.remove('hidden');
  }

  if (btnExportDecisions) {
    btnExportDecisions.addEventListener('click', openDecisionsExportModal);
  }
  if (btnCloseDecisionsModal && decisionsExportModal) {
    btnCloseDecisionsModal.addEventListener('click', () => decisionsExportModal.classList.add('hidden'));
    decisionsExportModal.addEventListener('click', (e) => {
      if (e.target === decisionsExportModal) decisionsExportModal.classList.add('hidden');
    });
  }
  if (btnPrintDecisions) {
    btnPrintDecisions.addEventListener('click', () => window.print());
  }

  // Keyboard Navigation (Up/Down Arrows for findings, F for Focus Mode, Esc to close drawers/modals)
  window.addEventListener('keydown', (e) => {
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;

    if (e.key === 'Escape') {
      if (valueEngModal && !valueEngModal.classList.contains('hidden')) {
        valueEngModal.classList.add('hidden');
        return;
      }
      if (summaryAreasModal && !summaryAreasModal.classList.contains('hidden')) {
        summaryAreasModal.classList.add('hidden');
        return;
      }
      if (decisionsExportModal && !decisionsExportModal.classList.contains('hidden')) {
        decisionsExportModal.classList.add('hidden');
        return;
      }
      if (isFocusMode) {
        toggleFocusMode(false);
        return;
      }
      toggleSideDock(false);
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      stepNote(1);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      stepNote(-1);
    } else if (e.key === 'f' || e.key === 'F' || e.key === 'כ') {
      if (!e.ctrlKey && !e.metaKey && !e.altKey) {
        e.preventDefault();
        toggleFocusMode();
      }
    }
  });

  // Click-to-Toggle More Tools Menu & Legend Popover
  if (btnToggleMoreMenu && moreToolsDropdown) {
    btnToggleMoreMenu.addEventListener('click', (e) => {
      e.stopPropagation();
      moreToolsDropdown.classList.toggle('hidden');
      if (legendPopoverBox) legendPopoverBox.classList.add('hidden');
    });
  }

  if (btnToggleLegend && legendPopoverBox) {
    btnToggleLegend.addEventListener('click', (e) => {
      e.stopPropagation();
      legendPopoverBox.classList.toggle('hidden');
      if (moreToolsDropdown) moreToolsDropdown.classList.add('hidden');
    });
  }

  document.addEventListener('click', (e) => {
    if (moreToolsDropdown && !moreToolsDropdown.classList.contains('hidden') && !e.target.closest('.tools-dropdown-wrap')) {
      moreToolsDropdown.classList.add('hidden');
    }
    if (legendPopoverBox && !legendPopoverBox.classList.contains('hidden') && !e.target.closest('.legend-popover-wrap')) {
      legendPopoverBox.classList.add('hidden');
    }
  });

  // Collapsible Right Document Panel Toggle
  if (btnCollapseDocPanel && splitWorkspaceEl) {
    btnCollapseDocPanel.addEventListener('click', () => {
      splitWorkspaceEl.classList.add('doc-collapsed');
      if (btnExpandDocPanel) btnExpandDocPanel.classList.remove('hidden');
    });
  }

  if (btnExpandDocPanel && splitWorkspaceEl) {
    btnExpandDocPanel.addEventListener('click', () => {
      splitWorkspaceEl.classList.remove('doc-collapsed');
      btnExpandDocPanel.classList.add('hidden');
    });
  }

  // Left Side Inspector Dock is permanently disabled (only Right Panel #doc-panel is used)
  function toggleSideDock() {
    if (planBodyLayoutEl) {
      planBodyLayoutEl.classList.add('dock-collapsed');
    }
    if (btnToggleSideDock) {
      btnToggleSideDock.classList.remove('active');
      btnToggleSideDock.classList.add('hidden');
    }
  }

  if (btnToggleSideDock) {
    btnToggleSideDock.addEventListener('click', () => toggleSideDock());
  }

  if (btnCloseSideDock) {
    btnCloseSideDock.addEventListener('click', () => toggleSideDock(false));
  }

  if (btnOpenVeCenterFromBar) {
    btnOpenVeCenterFromBar.addEventListener('click', () => {
      if (currentProject) openValueEngineeringModal(currentProject);
    });
  }

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
    if (moreToolsDropdown) moreToolsDropdown.classList.add('hidden');
    filesDrawer.classList.toggle('hidden');
  });

  btnCloseFilesDrawer.addEventListener('click', () => {
    filesDrawer.classList.add('hidden');
  });

  // Summary & Quantitative Areas Modal Toggle (Click to Open or Close)
  if (btnOpenSummaryModal) {
    btnOpenSummaryModal.addEventListener('click', () => {
      if (!currentProject) return;
      if (valueEngModal) valueEngModal.classList.add('hidden');
      if (!summaryAreasModal.classList.contains('hidden')) {
        summaryAreasModal.classList.add('hidden');
      } else {
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

  // Unified Cost Savings Command Center Toggle (Click to Open or Close)
  if (btnOpenValueEngModal) {
    btnOpenValueEngModal.addEventListener('click', () => {
      if (!currentProject) return;
      if (summaryAreasModal) summaryAreasModal.classList.add('hidden');
      if (!valueEngModal.classList.contains('hidden')) {
        valueEngModal.classList.add('hidden');
      } else {
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
      renderVePlanBar(data);
      const firstSheet = (data.sheets && data.sheets[0]) ? data.sheets[0].id : null;
      selectSheet(firstSheet, { keepNote: false });
      renderDocumentSections(data);
      if (data.notes && data.notes.length > 0) {
        highlightNote(data.notes[0].id, { scrollDoc: false });
      }
    } catch (err) {
      alert(`שגיאה: ${err.message}`);
    } finally {
      loadingOverlay.classList.add('hidden');
      fileUploadInput.value = '';
    }
  });

  // =========================================================================
  // 7. SYNCHRONIZED 2D / 3D BIM / SPLIT VIEW CONTROLLER
  // =========================================================================
  let userExplicitlySelectedNote = false;

  function postMessageTo3D(payload) {
    if (!model3dIframe || !model3dIframe.contentWindow || currentViewMode === '2d') return;
    try {
      model3dIframe.contentWindow.postMessage(payload, '*');
    } catch (err) {
      // ignore cross-frame race conditions
    }
  }

  function ensure3dModelLoaded(forceReload = false) {
    if (!currentProject || !model3dIframe) return;
    const baseUrl = currentProject._resolved_3d_url || (currentProject.project_id ? `/models/${currentProject.project_id}` : null);
    if (!baseUrl) return;
    const targetSrc = `${baseUrl}${baseUrl.includes('?') ? '&' : '?'}embed=1&v=6.5`;
    if (forceReload || loaded3dProjectUrl !== targetSrc) {
      loaded3dProjectUrl = targetSrc;
      model3dIframe.src = targetSrc;
    }
  }

  function setViewMode(mode) {
    currentViewMode = mode || '2d';
    if (planViewport) {
      planViewport.classList.remove('vmode-2d', 'vmode-3d', 'vmode-split');
      planViewport.classList.add(`vmode-${currentViewMode}`);
    }
    if (model3dStage) {
      model3dStage.classList.toggle('hidden', currentViewMode === '2d');
    }
    if (zoomControlsGroup) {
      zoomControlsGroup.classList.toggle('hidden', currentViewMode === '3d');
    }
    vmodeBtns.forEach((btn) => {
      btn.classList.toggle('active', btn.getAttribute('data-vmode') === currentViewMode);
    });
    if (btnHdrToggle3d) {
      btnHdrToggle3d.classList.toggle('active', currentViewMode !== '2d');
      btnHdrToggle3d.innerHTML = currentViewMode === '2d'
        ? '🧊 מודל 3D חי'
        : (currentViewMode === '3d' ? '📐 חזור ל-2D / מפוצל' : '🌓 תצוגה מפוצלת 2D+3D');
    }

    if (currentViewMode !== '2d') {
      ensure3dModelLoaded(false);
      [80, 260, 600].forEach((delay) => {
        setTimeout(() => {
          try {
            if (model3dIframe && model3dIframe.contentWindow) {
              model3dIframe.contentWindow.dispatchEvent(new Event('resize'));
            }
          } catch (e) {}
        }, delay);
      });
      setTimeout(() => {
        if (userExplicitlySelectedNote && activeNoteId) {
          postMessageTo3D({ type: 'ARCHICHECK_SELECT_NOTE', noteId: activeNoteId });
        }
      }, 250);
    }
  }

  vmodeBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      setViewMode(btn.getAttribute('data-vmode') || '2d');
    });
  });

  if (btnHdrToggle3d) {
    btnHdrToggle3d.addEventListener('click', () => {
      if (currentViewMode === '2d') setViewMode('3d');
      else if (currentViewMode === '3d') setViewMode('split');
      else setViewMode('2d');
    });
  }

  async function trigger3dModelCheckAndReaudit(forceReaudit = true) {
    const pid = (currentProject && currentProject.project_id) || queryInput.value || 'hafetz44';
    loadingTitle.textContent = `בודק שינויים במודל ה-3D הבסיסי ומריץ בדיקה תכנונית מלאה חדשה עבור "${currentProject ? currentProject.project_name : pid}"...`;
    loadingOverlay.classList.remove('hidden');

    try {
      const resp = await fetch('/api/check_3d_models', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ project: pid, force: Boolean(forceReaudit) }),
      });
      if (!resp.ok) {
        throw new Error(`שגיאה בבדיקת מודל ה-3D (${resp.status})`);
      }
      const resData = await resp.json();
      const updatedPayload = resData.payload || currentProject;
      if (updatedPayload) {
        if (Array.isArray(updatedPayload.notes)) {
          updatedPayload.notes = updatedPayload.notes.filter(
            (n) => !String(n.id || '').endsWith('-3D-SYNC') && !String(n.rule_id || '').includes('3D_BIM_FULL_AUDIT')
          );
        }
        currentProject = updatedPayload;
        renderProjectHeaderAndFiles(updatedPayload);
        renderSheetTabs(updatedPayload);
        renderVePlanBar(updatedPayload);
        renderDocumentSections(updatedPayload);
        selectSheet(currentSheetId || ((updatedPayload.sheets && updatedPayload.sheets[0]) ? updatedPayload.sheets[0].id : null), { keepNote: true });
        if (currentViewMode !== '2d') {
          ensure3dModelLoaded(true);
        }
        const st = updatedPayload.model_3d_sync_status || {};
        if (hudActiveNoteText) {
          hudActiveNoteText.textContent = st.status_message_he || 'הורצה בדיקה תכנונית מלאה חדשה על בסיס המודל התלת-ממדי.';
        }
      }
    } catch (err) {
      console.error('3D Model check/reaudit error:', err);
      if (hudActiveNoteText) {
        hudActiveNoteText.textContent = `שגיאה בבדיקת מודל 3D: ${err.message}`;
      }
    } finally {
      loadingOverlay.classList.add('hidden');
    }
  }

  if (btnCheck3dUpdate) {
    btnCheck3dUpdate.addEventListener('click', () => trigger3dModelCheckAndReaudit(true));
  }

  window.addEventListener('message', (event) => {
    const msg = event.data;
    if (!msg || typeof msg !== 'object') return;
    if (msg.type === 'ARCHICHECK_3D_PIN_CLICKED' && msg.noteId) {
      highlightNote(msg.noteId, {
        scrollDoc: true,
        switchSheet: true,
        openDock: true,
        zoomTo: true,
        from3D: true,
      });
    } else if (msg.type === 'ARCHICHECK_3D_READY') {
      if (userExplicitlySelectedNote && activeNoteId) {
        postMessageTo3D({ type: 'ARCHICHECK_SELECT_NOTE', noteId: activeNoteId });
      }
    } else if (msg.type === 'ARCHICHECK_3D_REAUDITED' && msg.payload) {
      if (Array.isArray(msg.payload.notes)) {
        msg.payload.notes = msg.payload.notes.filter(
          (n) => !String(n.id || '').endsWith('-3D-SYNC') && !String(n.rule_id || '').includes('3D_BIM_FULL_AUDIT')
        );
      }
      currentProject = msg.payload;
      renderProjectHeaderAndFiles(msg.payload);
      renderSheetTabs(msg.payload);
      renderVePlanBar(msg.payload);
      renderDocumentSections(msg.payload);
    }
  });

  window.addEventListener('keydown', (e) => {
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;
    if (e.key === '3' && !e.ctrlKey && !e.metaKey && !e.altKey) {
      e.preventDefault();
      setViewMode(currentViewMode === '3d' ? 'split' : '3d');
    }
  });

  // Initialize on Page Load with Hafetz Haim 44
  loadProjectAnalysis('חפץ חיים 44');
})();
