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
  const countTaskActionEl = document.getElementById('count-task-action');
  const countTaskOppEl = document.getElementById('count-task-opp');
  const countTaskPreserveEl = document.getElementById('count-task-preserve');
  const countTaskUnknownEl = document.getElementById('count-task-unknown');
  const countCatAllEl = document.getElementById('count-cat-all');
  const countCatStdEl = document.getElementById('count-cat-std');
  const countCatArchEl = document.getElementById('count-cat-arch');
  const countCatTipEl = document.getElementById('count-cat-tip');
  const countKbAllEl = document.getElementById('count-kb-all');
  const countKbIsrEl = document.getElementById('count-kb-isr');
  const countKbIntlEl = document.getElementById('count-kb-intl');
  const countKbSpaceEl = document.getElementById('count-kb-space');
  const countKbErgoEl = document.getElementById('count-kb-ergo');
  const countKbIeqEl = document.getElementById('count-kb-ieq');
  const countKbAdaptEl = document.getElementById('count-kb-adapt');
  const countKbMepEl = document.getElementById('count-kb-mep');
  const countKbUrbanEl = document.getElementById('count-kb-urban');
  const countVeAllEl = document.getElementById('count-ve-all');
  const countVeAgEl = document.getElementById('count-ve-ag');
  const countVeUgEl = document.getElementById('count-ve-ug');
  const countVeFacEl = document.getElementById('count-ve-fac');

  const taskFocusBtns = document.querySelectorAll('.task-focus-btn');
  const polarityBtns = document.querySelectorAll('.polarity-btn');
  const catFilterBtns = document.querySelectorAll('.cat-filter-btn');
  const kbFilterBtns = document.querySelectorAll('.kb-filter-btn');
  const veCatBtns = document.querySelectorAll('.ve-cat-btn');
  const filterBtns = document.querySelectorAll('.filter-btn');

  const sheetTabsContainer = document.getElementById('sheet-tabs-container');
  const visualPanelEl = document.getElementById('visual-panel');
  const visualToolbarEl = document.getElementById('visual-toolbar');
  const btnToggleSheetsCompact = document.getElementById('btn-toggle-sheets-compact');
  const btnCollapsePlanToolbar = document.getElementById('btn-collapse-plan-toolbar');
  const planToolbarRestoreBar = document.getElementById('plan-toolbar-restore-bar');
  const btnRestorePlanToolbar = document.getElementById('btn-restore-plan-toolbar');
  const btnRestoreTopBarFloating = document.getElementById('btn-restore-top-bar-floating');
  const btnRestoreDocPanelFloating = document.getElementById('btn-restore-doc-panel-floating');
  const btnRestoreAllBars = document.getElementById('btn-restore-all-bars');
  const restoreBarSheetName = document.getElementById('restore-bar-sheet-name');
  const btnCollapseVePlanBar = document.getElementById('btn-collapse-ve-plan-bar');
  const btnRestoreVePlanBar = document.getElementById('btn-restore-ve-plan-bar');
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
  let currentWorkMode = 'OVERVIEW'; // 'OVERVIEW' | 'FINDINGS' | 'OPTIMIZATION' | 'COMPARE'
  let currentFilter = 'ALL';
  let currentTaskFocus = 'ACTION_NEEDED'; // 'ACTION_NEEDED' | 'OPPORTUNITIES' | 'PRESERVE' | 'UNKNOWN' | 'ALL'
  let currentPolarity = 'ALL'; // 'ALL' | 'NEGATIVE' | 'POSITIVE'
  let currentCategory = 'ALL'; // 'ALL' | 'STANDARD' | 'ARCH_QUALITY' | 'INTERIOR_TIP'
  let currentKnowledgeBase = 'ALL'; // 'ALL' | 'KB_ISRAELI_STATUTORY' | 'KB_INTL_HOUSING' | 'KB_SPACE_SYNTAX' | 'KB_ERGONOMICS_INTERIOR' | 'KB_DAYLIGHT_IEQ'
  let currentVeCategory = 'ALL'; // 'ALL' | 'AG' | 'UG' | 'FAC'
  let currentActionReqFilter = 'ALL'; // Filter inside Architect Action Package modal
  let activeNoteId = null;
  let hoveredNoteId = null;
  let showAllPins = true;
  let isFocusMode = false;
  let isSheetsCompact = true;
  let isPlanToolbarCollapsed = false;
  let isVePlanBarCollapsed = false;

  function getShortSheetTitle(fullTitle) {
    const raw = String(fullTitle || '').trim();
    if (!raw) return 'קומה';
    const head = raw.split(/\s*[—–-]\s+(?:תכנית|בניין|קומת|דירות|פנטהאוז|דופלקס|מפלס|\d+\s+חניות)/)[0].split(' — ')[0].trim();
    const cleaned = head.replace(/\s*\([^)]*(?:m|מ׳|מ"|±|עד|קומות|טיפוסית)[^)]*\)/gi, '').trim();
    return cleaned || head || raw;
  }

  const KB_META_CATALOG = {
    KB_ISRAELI_STATUTORY: {
      id: 'KB_ISRAELI_STATUTORY',
      icon: '⚖️',
      shortHe: 'תקינה ישראלית ורישוי',
      titleHe: 'חקיקה, תקנות התכנון והבנייה ותקינה ישראלית מחייבת',
      sourcesHe: 'תקנות התכנון והבנייה (B1.3–B1.30) · הנחיות פקע״ר לממ״דים · ת״י 1918 · ת״י 1142 · ת״י 2481 · הנחיות משרד התחבורה לחניונים',
      color: '#1e40af',
      bg: '#eff6ff',
      border: '#bfdbfe',
    },
    KB_INTL_HOUSING: {
      id: 'KB_INTL_HOUSING',
      icon: '🏛️',
      shortHe: 'תקני איכות דיור (NSW/UK/משב״ש)',
      titleHe: 'תקני איכות דיור ופרוגרמה בינלאומיים (NSW ADG · UK NDSS · משרד השיכון)',
      sourcesHe: 'NSW Apartment Design Guide (ADG 4D/4E/4F) · UK Nationally Described Space Standard (NDSS) · אוגדן תכנון משרד הבינוי והשיכון · London Plan D6',
      color: '#4338ca',
      bg: '#eef2ff',
      border: '#c7d2fe',
    },
    KB_SPACE_SYNTAX: {
      id: 'KB_SPACE_SYNTAX',
      icon: '🧭',
      shortHe: 'טופולוגיה, זרימה ופרטיות',
      titleHe: 'טופולוגיה מרחבית, זרימת תנועה והיררכיית פרטיות (Space Syntax & Pattern Language)',
      sourcesHe: 'Hillier & Hanson Space Syntax (SAGA) · Christopher Alexander Pattern Language (#127 Intimacy Gradient, #131 Flow Through Rooms) · ETH Zürich Grundrisskritik',
      color: '#6d28d9',
      bg: '#f5f3ff',
      border: '#ddd6fe',
    },
    KB_ERGONOMICS_INTERIOR: {
      id: 'KB_ERGONOMICS_INTERIOR',
      icon: '🛋️',
      shortHe: 'ארגונומיה, מטבח וריהוט (NKBA)',
      titleHe: 'ארגונומיה, תכנון מטבחים וחדרים רטובים ויכולת ריהוט (NKBA · Boverket · DIN)',
      sourcesHe: 'NKBA Kitchen & Bath Guidelines · Boverket BBR (Sweden Furnishability) · DIN 18040-2 · Neufert Architects’ Data',
      color: '#b45309',
      bg: '#fffbeb',
      border: '#fde68a',
    },
    KB_DAYLIGHT_IEQ: {
      id: 'KB_DAYLIGHT_IEQ',
      icon: '☀️',
      shortHe: 'אור יום, אוורור ואקלים',
      titleHe: 'אקלים פנים, אור יום צירקדי, אוורור טבעי וביופיליה (EN 17037 · WELL v2 · ת״י 5281/1045)',
      sourcesHe: 'EN 17037 (אור יום) · WELL v2 Light & Air · CIBSE AM10/TM59 · ת״י 5281/5282 · ת״י 1045 · Biophilic Prospect & Refuge',
      color: '#0369a1',
      bg: '#f0f9ff',
      border: '#bae6fd',
    },
    KB_ADAPTABILITY_FAMILY: {
      id: 'KB_ADAPTABILITY_FAMILY',
      icon: '🧬',
      shortHe: 'גמישות תכנונית ומשפחות (Open Building)',
      titleHe: 'גמישות תכנונית (Open Building), התאמה למעגל החיים ותכנון למשפחות (Habraken · Toronto)',
      sourcesHe: 'N. John Habraken (Supports / Open Building) · EU Level(s) 2.3 (Adaptability) · UK Lifetime Homes M4(2) · City of Toronto Growing Up & Vancouver Family Housing · Casa Collage',
      color: '#be185d',
      bg: '#fdf2f8',
      border: '#fbcfe8',
    },
    KB_ACOUSTICS_MEP: {
      id: 'KB_ACOUSTICS_MEP',
      icon: '🔇',
      shortHe: 'אקוסטיקה ומערכות MEP/VRF',
      titleHe: 'אקוסטיקה פנימית, תיאום מערכות מיזוג (MEP/VRF) ואינסטלציה (ת״י 1004/1205 · ASHRAE · WELL)',
      sourcesHe: 'ת״י 1004 (בידוד אקוסטי) · WELL v2 Sound & זונינג אקוסטי פנימי (ארון חוצץ סלון↔שינה) · ASHRAE VRF (נתיבי הנמכות גבס) · ת״י 1205 / הל״ת (קולטנים והלימה אנכית)',
      color: '#4338ca',
      bg: '#eef2ff',
      border: '#c7d2fe',
    },
    KB_URBAN_LOCAL: {
      id: 'KB_URBAN_LOCAL',
      icon: '🏙️',
      shortHe: 'ממשק עירוני והנחיות מרחביות',
      titleHe: 'ממשק עירוני, קומת קרקע, מסתורי שירות והנחיות מרחביות מקומיות (סעיף 145ד · שכונה 360°)',
      sourcesHe: 'הנחיות מרחביות של ועדות מקומיות (סעיף 145ד — פתח תקווה, ת״א, ר״ג) · מדד שכונה 360° · Davos Baukultur · Active Design / Fitwel',
      color: '#0e7490',
      bg: '#ecfeff',
      border: '#a5f3fc',
    },
    KB_VALUE_ENG_BIM: {
      id: 'KB_VALUE_ENG_BIM',
      icon: '💰',
      shortHe: 'הנדסת ערך ובקרת קונטור BIM',
      titleHe: 'הנדסת ערך (VE), נצילות שטחי בנייה ובקרת קונטור תלת-ממדית (BIM)',
      sourcesHe: 'פרוטוקול 10 המבחנים לכיווץ קונטור אפקטיבי · ניצול חללים תחת רמפות (H≥2.20m) · אופטימיזציית תמהיל חיפוי חזיתות · הצלבת BIM 2D↔3D',
      color: '#047857',
      bg: '#ecfdf5',
      border: '#a7f3d0',
    },
  };

  const EXPLICIT_JS_KB_MAP = {
    'H44-W-01': 'KB_SPACE_SYNTAX', 'H44-W-02': 'KB_ERGONOMICS_INTERIOR', 'H44-W-03': 'KB_DAYLIGHT_IEQ',
    'H44-W-04': 'KB_ISRAELI_STATUTORY', 'H44-W-05': 'KB_ISRAELI_STATUTORY', 'H44-E-01': 'KB_INTL_HOUSING',
    'H44-E-02': 'KB_ERGONOMICS_INTERIOR', 'H44-PH-01': 'KB_ERGONOMICS_INTERIOR', 'H44-GND-01': 'KB_ISRAELI_STATUTORY',
    'H44-BSM-01': 'KB_ISRAELI_STATUTORY',
    'P48-B-01': 'KB_ERGONOMICS_INTERIOR', 'P48-B-02': 'KB_ERGONOMICS_INTERIOR', 'P48-B-03': 'KB_DAYLIGHT_IEQ',
    'P48-B-04': 'KB_SPACE_SYNTAX', 'P48-B-05': 'KB_ISRAELI_STATUTORY', 'P48-B-06': 'KB_INTL_HOUSING',
    'P48-A-01': 'KB_INTL_HOUSING', 'P48-A-02': 'KB_ERGONOMICS_INTERIOR', 'P48-A-03': 'KB_SPACE_SYNTAX',
    'P48-A-04': 'KB_ERGONOMICS_INTERIOR', 'P48-A-05': 'KB_ISRAELI_STATUTORY', 'P48-C-01': 'KB_SPACE_SYNTAX',
    'P48-C-02': 'KB_ERGONOMICS_INTERIOR', 'P48-C-03': 'KB_INTL_HOUSING', 'P48-C-04': 'KB_ISRAELI_STATUTORY',
    'P48-C-05': 'KB_ERGONOMICS_INTERIOR', 'P48-CORE-01': 'KB_ISRAELI_STATUTORY', 'P48-PB-01': 'KB_ERGONOMICS_INTERIOR',
    'P48-PC-01': 'KB_INTL_HOUSING', 'P48-F7-01': 'KB_ISRAELI_STATUTORY', 'P48-ROOF-01': 'KB_ISRAELI_STATUTORY',
    'P48-GND-01': 'KB_INTL_HOUSING', 'P48-GND-02': 'KB_ISRAELI_STATUTORY', 'P48-GND-03': 'KB_ISRAELI_STATUTORY',
    'P48-BSM-01': 'KB_ISRAELI_STATUTORY',
    'KKL-PARK-01': 'KB_ISRAELI_STATUTORY', 'KKL-PARK-02': 'KB_ISRAELI_STATUTORY', 'KKL-E-01': 'KB_INTL_HOUSING',
    'KKL-E-02': 'KB_ERGONOMICS_INTERIOR', 'KKL-E-03': 'KB_DAYLIGHT_IEQ', 'KKL-B-01': 'KB_ERGONOMICS_INTERIOR',
    'KKL-B-02': 'KB_ISRAELI_STATUTORY', 'KKL-B-03': 'KB_SPACE_SYNTAX', 'KKL-D-01': 'KB_INTL_HOUSING',
    'KKL-D-02': 'KB_ERGONOMICS_INTERIOR', 'KKL-CORE-01': 'KB_ISRAELI_STATUTORY', 'KKL-PH-01': 'KB_ISRAELI_STATUTORY',
    'KKL-GND-01': 'KB_ISRAELI_STATUTORY',
    'YAT-N-01': 'KB_INTL_HOUSING', 'YAT-N-02': 'KB_ERGONOMICS_INTERIOR', 'YAT-N-03': 'KB_SPACE_SYNTAX',
    'YAT-S-01': 'KB_ERGONOMICS_INTERIOR', 'YAT-S-02': 'KB_ISRAELI_STATUTORY', 'YAT-PH-01': 'KB_INTL_HOUSING',
    'YAT-GND-01': 'KB_ISRAELI_STATUTORY', 'YAT-BSM-01': 'KB_ISRAELI_STATUTORY',
    'KIT-37-NW': 'KB_ERGONOMICS_INTERIOR', 'KIT-37-NE': 'KB_INTL_HOUSING', 'KIT-37-SE': 'KB_ERGONOMICS_INTERIOR',
    'KIT-37-SW': 'KB_ISRAELI_STATUTORY', 'KIT-39-W3': 'KB_ISRAELI_STATUTORY', 'KIT-39-SW': 'KB_DAYLIGHT_IEQ',
    'KIT-PH-01': 'KB_ERGONOMICS_INTERIOR', 'KIT-BSM-01': 'KB_ISRAELI_STATUTORY',
    'FB3-W-01': 'KB_SPACE_SYNTAX', 'FB3-W-02': 'KB_ERGONOMICS_INTERIOR', 'FB3-W-03': 'KB_ISRAELI_STATUTORY',
    'FB3-E-01': 'KB_ERGONOMICS_INTERIOR', 'FB3-E-02': 'KB_DAYLIGHT_IEQ', 'FB3-PH-01': 'KB_INTL_HOUSING',
    'FB3-BSM-01': 'KB_ISRAELI_STATUTORY',
  };

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
    if (!note) {
      const defKb = KB_META_CATALOG.KB_INTL_HOUSING;
      return {
        polarity: 'NEGATIVE',
        polarityHe: 'שלילי',
        category: 'ARCH_QUALITY',
        categoryHe: 'איכות תכנון אדריכלי',
        kbId: defKb.id,
        kbShortHe: defKb.shortHe,
        kbTitleHe: defKb.titleHe,
        kbIcon: defKb.icon,
        kbSourcesHe: defKb.sourcesHe,
        kbColor: defKb.color,
        kbBg: defKb.bg,
        kbBorder: defKb.border,
      };
    }
    if (note.is_value_eng) {
      const veKb = KB_META_CATALOG.KB_VALUE_ENG_BIM;
      return {
        polarity: 'SAVINGS',
        polarityHe: 'חיסכון',
        category: 'SAVINGS',
        categoryHe: 'חיסכון',
        kbId: veKb.id,
        kbShortHe: veKb.shortHe,
        kbTitleHe: veKb.titleHe,
        kbIcon: veKb.icon,
        kbSourcesHe: veKb.sourcesHe,
        kbColor: veKb.color,
        kbBg: veKb.bg,
        kbBorder: veKb.border,
      };
    }
    const polarity = note.audit_polarity || (note.status === 'PASS' ? 'POSITIVE' : 'NEGATIVE');
    const polarityHe = polarity === 'POSITIVE' ? 'חיובי' : 'שלילי';
    let category = note.audit_category;
    const nid = note.id || '';
    const txt = `${note.rule_id || ''} ${note.title || ''} ${note.recommendation || ''}`.toLowerCase();
    if (!category || category === 'SAVINGS') {
      if (EXPLICIT_JS_CATEGORY_MAP[nid]) {
        category = EXPLICIT_JS_CATEGORY_MAP[nid];
      } else if (note.is_design_improvement) {
        category = 'ARCH_QUALITY';
      } else {
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

    // Knowledge Base classification
    let kbId = note.kb_id || EXPLICIT_JS_KB_MAP[nid] || '';
    if (!kbId || !KB_META_CATALOG[kbId]) {
      if (note.is_design_improvement) {
        kbId = 'KB_SPACE_SYNTAX';
      } else if (['כיווני אוויר', 'אוורור', 'אור יום', 'אקוסט', 'en 17037', 'cibse', '5281', '1004', 'חלון', 'הצללה'].some((k) => txt.includes(k))) {
        kbId = 'KB_DAYLIGHT_IEQ';
      } else if (['פקע״ר', 'פיקוד העורף', 'ממ״ד', 'חניון', 'מיסעה', 'רמפה', 'ת״י', 'תקנות', 'b1.', '1918', '1142', '2481', 'הגשה', 'מכר', 'מוניציפלי'].some((k) => txt.includes(k))) {
        kbId = 'KB_ISRAELI_STATUTORY';
      } else if (['nkba', 'אי מטבח', 'ארון', 'דלת כיס', 'pocket', 'ריהוט', 'מיטה', 'מקלחון', 'boverket', 'din 18040', 'משקוף'].some((k) => txt.includes(k))) {
        kbId = 'KB_ERGONOMICS_INTERIOR';
      } else if (['מסדרון', 'מבואה', 'זרימה', 'פרטיות', 'space syntax', 'alexander', 'מדרגת מחיצה'].some((k) => txt.includes(k))) {
        kbId = 'KB_SPACE_SYNTAX';
      } else if (category === 'STANDARD') {
        kbId = 'KB_ISRAELI_STATUTORY';
      } else if (category === 'INTERIOR_TIP') {
        kbId = 'KB_ERGONOMICS_INTERIOR';
      } else {
        kbId = 'KB_INTL_HOUSING';
      }
    }
    const kbMeta = KB_META_CATALOG[kbId] || KB_META_CATALOG.KB_INTL_HOUSING;
    return {
      polarity,
      polarityHe,
      category,
      categoryHe,
      kbId: kbMeta.id,
      kbShortHe: note.kb_short_he || kbMeta.shortHe,
      kbTitleHe: note.kb_title_he || kbMeta.titleHe,
      kbIcon: note.kb_icon || kbMeta.icon,
      kbSourcesHe: note.kb_sources_he || kbMeta.sourcesHe,
      kbColor: note.kb_color || kbMeta.color,
      kbBg: note.kb_bg || kbMeta.bg,
      kbBorder: note.kb_border || kbMeta.border,
    };
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
    const userDecCount = Object.keys(decisionsMap).filter((k) => k.startsWith(prefix) && decisionsMap[k]).length;
    const pds = currentProject.project_data_summary || {};
    const pkg = (pds.summary_document && pds.summary_document.architect_action_package) || {};
    const pkgItemsCount = Array.isArray(pkg.action_items) ? pkg.action_items.length : 0;
    hdrDecisionsCount.textContent = userDecCount > 0 ? `${userDecCount}/${pkgItemsCount || userDecCount}` : String(pkgItemsCount || 0);
  }

  const DECISION_LABELS = {
    TO_CHECK: { label: 'לבדיקה', cls: 'dec-todo' },
    DECIDED_TO_FIX: { label: 'הוחלט לתקן', cls: 'dec-todo' },
    IN_DESIGN: { label: 'בתכנון', cls: 'dec-verified' },
    FIXED_PENDING_VERIFICATION: { label: 'תוקן — ממתין לאימות', cls: 'dec-verified' },
    CLOSED: { label: 'נסגר (מאומת)', cls: 'dec-approved' },
    REJECTED: { label: 'נדחה', cls: 'dec-rejected' },
    // Backwards-compatible aliases
    TODO: { label: 'הוחלט לתקן', cls: 'dec-todo' },
    VERIFIED: { label: 'תוקן — ממתין לאימות', cls: 'dec-verified' },
    APPROVED: { label: 'אושר לקדם', cls: 'dec-approved' },
  };

  function isNoteUnknownStatus(note) {
    if (!note) return false;
    return (
      note.status === 'UNKNOWN' ||
      note.verification_status === 'UNKNOWN' ||
      String(note.measured || '').includes('UNKNOWN') ||
      String(note.measured || '').includes('לא ידוע')
    );
  }

  function isNoteActionNeeded(note) {
    if (!note || note.is_value_eng) return false;
    if (isNoteUnknownStatus(note)) return false;
    const cls = classifySystemNote(note);
    return (
      note.status === 'FAIL' ||
      (cls.polarity === 'NEGATIVE' && !note.is_design_improvement && cls.category !== 'INTERIOR_TIP')
    );
  }

  function isNoteOpportunity(note) {
    if (!note || note.is_value_eng) return false;
    if (isNoteUnknownStatus(note)) return false;
    const cls = classifySystemNote(note);
    return Boolean(note.is_design_improvement) || (cls.polarity === 'NEGATIVE' && cls.category === 'INTERIOR_TIP');
  }

  function isNotePreservationConstraint(note) {
    if (!note || note.is_value_eng) return false;
    const cls = classifySystemNote(note);
    return note.status === 'PASS' || cls.polarity === 'POSITIVE' || Boolean(note.is_preservation_constraint);
  }

  // Pan & Zoom State
  let scale = 1.0;
  let panX = 0;
  let panY = 0;
  let isDragging = false;
  let dragStartX = 0;
  let dragStartY = 0;

  const STATUS_LABELS = {
    PASS: 'תקין (לשימור)',
    WARN: 'לבדיקה',
    FAIL: 'חריגה',
    UNKNOWN: 'לא ידוע (מידע חסר)',
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
      let loadedFromLiveApi = false;
      try {
        const resp = await fetch('/api/analyze_project', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: cleanQuery }),
        });
        if (resp.ok) {
          data = await resp.json();
          loadedFromLiveApi = true;
        }
      } catch (apiErr) {
        console.warn('API endpoint not reachable, trying static fallback:', apiErr);
      }

      if (!data) {
        // Fallback for Google Cloud / Firebase Hosting
        const q_low = cleanQuery.toLowerCase();
        let staticFile = 'hafetz44.json';
        if (['משה שרת', 'שרת', 'sharett', 'sharet', '26-28', '26–28', '1025'].some((k) => q_low.includes(k))) staticFile = 'sharett26.json';
        else if (['פאירברג', 'פאיירברג', 'פיארברג', 'feierberg', 'fairberg', 'feirberg', '6387'].some((k) => q_low.includes(k))) staticFile = 'feierberg3.json';
        else if (['יטקובסקי', 'yatkovski', '7א'].some((k) => q_low.includes(k))) staticFile = 'yatkovski7.json';
        else if (['קיטרוני', 'קטרוני', 'kitroni', '37', '39'].some((k) => q_low.includes(k))) staticFile = 'kitroni37.json';
        else if (['חפץ', 'חיים', 'hafetz', '44'].some((k) => q_low.includes(k))) staticFile = 'hafetz44.json';
        else if (['קקל', 'קק"ל', 'קק״ל', 'kkl', '10'].some((k) => q_low.includes(k))) staticFile = 'kkl10.json';
        else if (['פינס', 'pines', '48'].some((k) => q_low.includes(k))) staticFile = 'pines48.json';

        const staticResp = await fetch(`/api/${staticFile}?v=7.6`, { cache: 'no-store' });
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

      data._loaded_from_live_api = loadedFromLiveApi;
      currentProject = data;
      activeNoteId = null;
      userExplicitlySelectedNote = false;
      hoveredNoteId = null;
      currentFilter = 'ALL';
      currentTaskFocus = 'ACTION_NEEDED';
      currentPolarity = 'ALL';
      currentCategory = 'ALL';
      currentKnowledgeBase = 'ALL';
      currentVeCategory = 'ALL';
      if (currentWorkMode !== 'OVERVIEW' && currentWorkMode !== 'FINDINGS') {
        currentWorkMode = 'OVERVIEW';
      }
      workModeTabs.forEach((t) => t.classList.toggle('active', t.dataset.mode === currentWorkMode));
      if (docSubfilterBar) docSubfilterBar.classList.toggle('hidden', currentWorkMode !== 'FINDINGS');
      if (veSubfilterBar) veSubfilterBar.classList.add('hidden');
      taskFocusBtns.forEach((b) => b.classList.toggle('active', b.dataset.taskFocus === currentTaskFocus));
      polarityBtns.forEach((b) => b.classList.toggle('active', b.dataset.polarity === 'ALL'));
      catFilterBtns.forEach((b) => b.classList.toggle('active', b.dataset.category === 'ALL'));
      kbFilterBtns.forEach((b) => b.classList.toggle('active', b.dataset.kb === 'ALL'));
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
    const actionNotes = systemNotes.filter((n) => isNoteActionNeeded(n));
    const oppNotes = systemNotes.filter((n) => isNoteOpportunity(n));
    const preserveNotes = systemNotes.filter((n) => isNotePreservationConstraint(n));
    const unknownNotes = notes.filter((n) => isNoteUnknownStatus(n));

    if (countAllEl) countAllEl.textContent = systemNotes.length;
    if (countOptEl) countOptEl.textContent = veNotes.length;

    if (countTaskActionEl) countTaskActionEl.textContent = actionNotes.length;
    if (countTaskOppEl) countTaskOppEl.textContent = oppNotes.length;
    if (countTaskPreserveEl) countTaskPreserveEl.textContent = preserveNotes.length;
    if (countTaskUnknownEl) countTaskUnknownEl.textContent = unknownNotes.length;

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

    // Knowledge Base counts within polarity + category scope
    const catScopedNotes = currentCategory === 'ALL'
      ? polarityScopedNotes
      : polarityScopedNotes.filter((n) => classifySystemNote(n).category === currentCategory);

    if (countKbAllEl) countKbAllEl.textContent = catScopedNotes.length;
    if (countKbIsrEl) countKbIsrEl.textContent = catScopedNotes.filter((n) => classifySystemNote(n).kbId === 'KB_ISRAELI_STATUTORY').length;
    if (countKbIntlEl) countKbIntlEl.textContent = catScopedNotes.filter((n) => classifySystemNote(n).kbId === 'KB_INTL_HOUSING').length;
    if (countKbSpaceEl) countKbSpaceEl.textContent = catScopedNotes.filter((n) => classifySystemNote(n).kbId === 'KB_SPACE_SYNTAX').length;
    if (countKbErgoEl) countKbErgoEl.textContent = catScopedNotes.filter((n) => classifySystemNote(n).kbId === 'KB_ERGONOMICS_INTERIOR').length;
    if (countKbIeqEl) countKbIeqEl.textContent = catScopedNotes.filter((n) => classifySystemNote(n).kbId === 'KB_DAYLIGHT_IEQ').length;
    if (countKbAdaptEl) countKbAdaptEl.textContent = catScopedNotes.filter((n) => classifySystemNote(n).kbId === 'KB_ADAPTABILITY_FAMILY').length;
    if (countKbMepEl) countKbMepEl.textContent = catScopedNotes.filter((n) => classifySystemNote(n).kbId === 'KB_ACOUSTICS_MEP').length;
    if (countKbUrbanEl) countKbUrbanEl.textContent = catScopedNotes.filter((n) => classifySystemNote(n).kbId === 'KB_URBAN_LOCAL').length;

    // Dedicated Savings tab counts
    if (countVeAllEl) countVeAllEl.textContent = veNotes.length;
    if (countVeAgEl) countVeAgEl.textContent = veNotes.filter((n) => n.ve_category === 'AG').length;
    if (countVeUgEl) countVeUgEl.textContent = veNotes.filter((n) => n.ve_category === 'UG').length;
    if (countVeFacEl) countVeFacEl.textContent = veNotes.filter((n) => n.ve_category === 'FAC').length;
  }

  // =========================================================================
  // 2. RENDER HEADER, 4 PRIMARY OPERATIONAL METRICS (Sec 5.4) & DISCOVERED FILES
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
        btnOpen3dViewer.href = `${resolved3dUrl}${resolved3dUrl.includes('?') ? '&' : '?'}v=7.6`;
        btnOpen3dViewer.classList.remove('hidden');
      } else {
        btnOpen3dViewer.classList.add('hidden');
      }
    }
    // Summary & Quantitative Data Document Button + Unified Header Savings Badge
    const pds = data.project_data_summary || {};
    const opt = pds.design_optimization || {};
    const optKpis = opt.executive_kpis || {};
    const netBd = opt.net_avoidable_cost_breakdown || {};
    const netSavingIls = netBd.net_avoidable_saving_base_ils !== undefined
      ? netBd.net_avoidable_saving_base_ils
      : (optKpis.net_avoidable_saving_base_ils !== undefined ? optKpis.net_avoidable_saving_base_ils : (optKpis.grand_total_direct_saving_ils || 0));

    if (hdrVeTotalBadge) {
      hdrVeTotalBadge.textContent = `נטו: ${fmtNum(netSavingIls)} ₪`;
    }
    if (pds && pds.summary_doc_url && btnOpenSummaryDoc) {
      btnOpenSummaryDoc.href = pds.summary_doc_url;
      btnOpenSummaryDoc.classList.remove('hidden');
    } else if (btnOpenSummaryDoc) {
      btnOpenSummaryDoc.classList.add('hidden');
    }

    // Counts for filter & mode buttons
    const notes = data.notes || [];
    const sheets = data.sheets || [];
    const systemNotes = notes.filter((n) => !n.is_value_eng);
    const openActionCount = systemNotes.filter((n) => isNoteActionNeeded(n)).length;
    const oppCount = systemNotes.filter((n) => isNoteOpportunity(n)).length;
    const unknownNoteCount = notes.filter((n) => isNoteUnknownStatus(n)).length;
    const pkg = (pds.summary_document && pds.summary_document.architect_action_package) || {};
    const infoGaps = Array.isArray(pkg.information_gaps) ? pkg.information_gaps : [];
    const totalMissingInfoCount = unknownNoteCount + infoGaps.length;

    updateSystemFilterCounts(data);

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

    const lockSum = data.spatial_lock_summary || {};
    const lockCountTxt = lockSum.locked_notes ? `${lockSum.locked_notes}/${lockSum.total_notes}` : `${notes.length}/${notes.length}`;
    const planVer = pkg.baseline_plan_version || 'v2026.10';
    const runModeText = data._loaded_from_live_api ? 'הרצת מנוע חיה' : 'נתוני בקרה שמורים (v2026.10)';
    const matStage = opt.maturity_stage || 3;

    // Render 4 Primary Operational Metrics (Section 5.4) + Run Provenance Bar (E36)
    docMetricsGrid.innerHTML = `
      <div class="zt-provenance-bar" title="מקור ומועד התוצאה (E36)">
        <div>
          <span class="zt-prov-pill">📄 גרסה: ${planVer}</span>
          <span style="margin-right:4px;">${runModeText} · סבב #${revNum}</span>
        </div>
        <span class="zt-secondary-score-pill" title="ציון איכות משני שקוף (אינו מחליף בדיקת חריגות)">ציון איכות משני: ${overallScore}</span>
      </div>

      <div class="zt-four-metrics-grid" role="region" aria-label="4 מדדים ראשיים">
        <button type="button" class="zt-metric-card m-open" id="zt-m-btn-open" title="במה צריך לטפל? לחץ לסינון ממצאים פתוחים וחריגות">
          <span class="zt-m-lbl">1. ממצאים פתוחים</span>
          <strong class="zt-m-val">${openActionCount} לטיפול</strong>
          <span class="zt-m-sub">+${oppCount} הזדמנויות שיפור</span>
        </button>

        <button type="button" class="zt-metric-card m-coverage" id="zt-m-btn-coverage" title="מה באמת נבדק? לחץ לצפייה בכל הבדיקות שבוצעו">
          <span class="zt-m-lbl">2. כיסוי בדיקות</span>
          <strong class="zt-m-val">${notes.length - unknownNoteCount}/${notes.length} אומתו</strong>
          <span class="zt-m-sub">${sheets.length} גיליונות · 🔒 ${lockCountTxt}</span>
        </button>

        <button type="button" class="zt-metric-card m-unknown" id="zt-m-btn-unknown" title="מה מונע מסקנה? לחץ לצפייה במידע חסר או חבילת אדריכל">
          <span class="zt-m-lbl">3. מידע חסר</span>
          <strong class="zt-m-val">${totalMissingInfoCount === 0 ? '0 חוסרים' : `${totalMissingInfoCount} להשלמה`}</strong>
          <span class="zt-m-sub">${unknownNoteCount} בממצאים · ${infoGaps.length} במפרט</span>
        </button>

        <button type="button" class="zt-metric-card m-savings" id="zt-m-btn-savings" title="מהו הערך ומה מידת התקדמותו? לחץ לפתיחת תחשיב חיסכון נטו">
          <span class="zt-m-lbl">4. חיסכון לפי בשלות</span>
          <strong class="zt-m-val">${fmtNum(netSavingIls)} ₪ נטו</strong>
          <span class="zt-m-sub">שלב ${matStage}/5: נבדק גיאומטרית</span>
        </button>
      </div>

      <div id="model-3d-sync-strip" style="margin-top:4px;padding:5px 8px;border-radius:7px;border:1px solid ${wasUpdated ? '#86efac' : '#cbd5e1'};background:${wasUpdated ? '#f0fdf4' : '#f8fafc'};display:flex;align-items:center;justify-content:space-between;gap:8px;font-size:11px;">
        <div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="${syncSt.status_message_he || 'המודל התלת-ממדי הבסיסי מאומת ומסונכרן'}">
          <strong>${wasUpdated ? '🟢 מודל 3D עודכן — הורצה בדיקה מלאה' : '🧊 מודל 3D מנוטר'}</strong>
          <span style="color:#475569;margin-right:4px;">· <code>#${hashShort}</code>${total3dChecks ? ` · ${total3dChecks} בדיקות 3D` : ''} · <strong style="color:#1e40af;">🔒 2D↔3D (${lockCountTxt})</strong></span>
        </div>
        <button type="button" id="btn-inline-reaudit-3d" style="flex-shrink:0;padding:2px 7px;border-radius:5px;border:1px solid #2563eb;background:#eff6ff;color:#1d4ed8;font-family:inherit;font-size:10.5px;font-weight:700;cursor:pointer;" title="בדוק אם מודל ה-3D הבסיסי שונה או עודכן והרץ בדיקה תכנונית מלאה חדשה">
          🔄 בדוק 3D
        </button>
      </div>
    `;

    const btnMOpen = document.getElementById('zt-m-btn-open');
    if (btnMOpen) {
      btnMOpen.addEventListener('click', () => {
        setTaskFocusFilter('ACTION_NEEDED');
      });
    }
    const btnMCov = document.getElementById('zt-m-btn-coverage');
    if (btnMCov) {
      btnMCov.addEventListener('click', () => {
        setTaskFocusFilter('ALL');
      });
    }
    const btnMUnk = document.getElementById('zt-m-btn-unknown');
    if (btnMUnk) {
      btnMUnk.addEventListener('click', () => {
        if (unknownNoteCount > 0) {
          setTaskFocusFilter('UNKNOWN');
        } else {
          openDecisionsExportModal();
        }
      });
    }
    const btnMSav = document.getElementById('zt-m-btn-savings');
    if (btnMSav) {
      btnMSav.addEventListener('click', () => {
        switchWorkMode('OPTIMIZATION');
      });
    }

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
      const shortTitle = getShortSheetTitle(sh.title);
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'sheet-tab-btn';
      btn.dataset.sheetId = sh.id;
      btn.title = `${sh.title} (לחץ לבחירת קומה)`;
      btn.innerHTML = `
        <span class="sheet-tab-short">${shortTitle}</span>
        <span class="sheet-tab-full">${sh.title}</span>
        <span class="sheet-tab-count">${sheetNotesCount}</span>
      `;
      btn.addEventListener('click', () => {
        if (currentSheetId === sh.id && !isSheetsCompact) {
          toggleSheetsCompact(true);
        } else {
          selectSheet(sh.id, { keepNote: false });
        }
      });
      sheetTabsContainer.appendChild(btn);
    });
    syncSheetsCompactUi();
  }

  function syncSheetsCompactUi() {
    if (sheetTabsContainer) {
      sheetTabsContainer.classList.toggle('sheets-compact', isSheetsCompact);
      sheetTabsContainer.classList.toggle('sheets-expanded', !isSheetsCompact);
    }
    if (btnToggleSheetsCompact) {
      btnToggleSheetsCompact.classList.toggle('active', !isSheetsCompact);
      btnToggleSheetsCompact.innerHTML = isSheetsCompact ? 'פירוט קומות ▾' : 'צמצם קומות ▴';
      btnToggleSheetsCompact.title = isSheetsCompact
        ? 'פתח פירוט מלא של הקומות והתיאורים'
        : 'צמצם את רשימת הקומות לשורה קומפקטית אחת';
    }
  }

  function toggleSheetsCompact(forceCompact) {
    isSheetsCompact = forceCompact !== undefined ? Boolean(forceCompact) : !isSheetsCompact;
    syncSheetsCompactUi();
  }

  function syncCollapsedBarsRestoreUi() {
    const isTopCollapsed = document.body.classList.contains('top-bar-collapsed');
    const isDocCollapsed = splitWorkspaceEl ? splitWorkspaceEl.classList.contains('doc-collapsed') : false;
    const isToolbarCollapsed = Boolean(isPlanToolbarCollapsed);

    // Sync inline expand buttons inside visual-toolbar (visible when visual-toolbar itself is open)
    if (btnExpandTopBar) {
      btnExpandTopBar.classList.toggle('hidden', !isTopCollapsed);
    }
    if (btnExpandDocPanel) {
      btnExpandDocPanel.classList.toggle('hidden', !isDocCollapsed);
    }

    // Sync floating restore bar inside #plan-viewport (ALWAYS accessible even when visual-toolbar is closed!)
    const anyBarCollapsed = isTopCollapsed || isDocCollapsed || isToolbarCollapsed;
    if (planToolbarRestoreBar) {
      planToolbarRestoreBar.classList.toggle('hidden', !anyBarCollapsed);
    }
    if (btnRestoreTopBarFloating) {
      btnRestoreTopBarFloating.classList.toggle('hidden', !isTopCollapsed);
    }
    if (btnRestoreDocPanelFloating) {
      btnRestoreDocPanelFloating.classList.toggle('hidden', !isDocCollapsed);
    }
    if (btnRestorePlanToolbar) {
      btnRestorePlanToolbar.classList.toggle('hidden', !isToolbarCollapsed);
    }
    const collapsedCount = (isTopCollapsed ? 1 : 0) + (isDocCollapsed ? 1 : 0) + (isToolbarCollapsed ? 1 : 0);
    if (btnRestoreAllBars) {
      btnRestoreAllBars.classList.toggle('hidden', collapsedCount < 2);
    }
  }

  function restoreAllBarsAndPanels() {
    isFocusMode = false;
    if (btnFocusMode) {
      btnFocusMode.classList.remove('active');
      btnFocusMode.textContent = 'מיקוד';
    }
    document.body.classList.remove('top-bar-collapsed');
    if (topCommandBar) topCommandBar.classList.remove('hidden');
    if (splitWorkspaceEl) splitWorkspaceEl.classList.remove('doc-collapsed');
    isPlanToolbarCollapsed = false;
    if (visualPanelEl) visualPanelEl.classList.remove('plan-toolbar-collapsed');
    if (visualToolbarEl) visualToolbarEl.classList.remove('hidden');
    if (vePlanBar && currentWorkMode === 'OPTIMIZATION' && !isVePlanBarCollapsed) {
      vePlanBar.classList.remove('hidden');
    }
    syncCollapsedBarsRestoreUi();
    setTimeout(() => {
      try {
        if (model3dIframe && model3dIframe.contentWindow && currentViewMode !== '2d') {
          model3dIframe.contentWindow.dispatchEvent(new Event('resize'));
        }
      } catch (e) {}
    }, 60);
  }

  function togglePlanToolbar(forceCollapse) {
    isPlanToolbarCollapsed = forceCollapse !== undefined ? Boolean(forceCollapse) : !isPlanToolbarCollapsed;
    if (visualPanelEl) {
      visualPanelEl.classList.toggle('plan-toolbar-collapsed', isPlanToolbarCollapsed);
    }
    if (visualToolbarEl) {
      visualToolbarEl.classList.toggle('hidden', isPlanToolbarCollapsed);
    }
    if (vePlanBar) {
      if (isPlanToolbarCollapsed) {
        vePlanBar.classList.add('hidden');
      } else if (currentWorkMode === 'OPTIMIZATION' && !isVePlanBarCollapsed) {
        vePlanBar.classList.remove('hidden');
      }
    }
    syncCollapsedBarsRestoreUi();
    setTimeout(() => {
      try {
        if (model3dIframe && model3dIframe.contentWindow && currentViewMode !== '2d') {
          model3dIframe.contentWindow.dispatchEvent(new Event('resize'));
        }
      } catch (e) {}
    }, 60);
  }

  function toggleVePlanBarCollapse(forceCollapse) {
    isVePlanBarCollapsed = forceCollapse !== undefined ? Boolean(forceCollapse) : !isVePlanBarCollapsed;
    if (vePlanBar) {
      const shouldHide = isVePlanBarCollapsed || isPlanToolbarCollapsed || currentWorkMode !== 'OPTIMIZATION';
      vePlanBar.classList.toggle('hidden', shouldHide);
    }
    if (btnRestoreVePlanBar) {
      const showRestoreBtn = isVePlanBarCollapsed && currentWorkMode === 'OPTIMIZATION';
      btnRestoreVePlanBar.classList.toggle('hidden', !showRestoreBtn);
    }
  }

  function selectSheet(sheetId, options = {}) {
    if (!currentProject || !sheetId) return;
    const sheet = (currentProject.sheets || []).find((s) => s.id === sheetId);
    if (!sheet) return;

    const sheetChanged = currentSheetId !== sheetId;
    currentSheetId = sheetId;

    // E33 Zero-Trust Rule: Never leave an active finding from another floor selected when switching floors!
    if (sheetChanged && activeNoteId && !options.fromHighlightNote) {
      const activeObj = (currentProject.notes || []).find((n) => n.id === activeNoteId);
      if (activeObj && activeObj.sheet_id !== sheetId) {
        activeNoteId = null;
        document.querySelectorAll('.doc-note-card.active').forEach((card) => {
          card.classList.remove('active');
          const exp = card.querySelector('.note-inline-expanded');
          if (exp) {
            exp.classList.add('hidden');
            exp.innerHTML = '';
          }
        });
      }
    }

    // Update top header breadcrumb & collapsed restore pill
    if (hdrBreadcrumbSub) {
      hdrBreadcrumbSub.textContent = `${currentProject.project_name || ''} · ${sheet.title}`;
    }
    if (restoreBarSheetName) {
      restoreBarSheetName.textContent = getShortSheetTitle(sheet.title);
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

    if (!options.keepNote && !activeNoteId) {
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

  function setTaskFocusFilter(taskFocusVal) {
    currentTaskFocus = taskFocusVal || 'ALL';
    currentPolarity = 'ALL';
    currentCategory = 'ALL';
    currentKnowledgeBase = 'ALL';
    taskFocusBtns.forEach((b) => b.classList.toggle('active', b.dataset.taskFocus === currentTaskFocus));
    polarityBtns.forEach((b) => b.classList.toggle('active', b.dataset.polarity === 'ALL'));
    catFilterBtns.forEach((b) => b.classList.toggle('active', b.dataset.category === 'ALL'));
    kbFilterBtns.forEach((b) => b.classList.toggle('active', b.dataset.kb === 'ALL'));
    if (currentWorkMode !== 'FINDINGS') {
      switchWorkMode('FINDINGS', { preserveSubfilters: true });
    } else if (currentProject) {
      updateSystemFilterCounts(currentProject);
      renderDocumentSections(currentProject);
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

    // 2. System Findings Tab ("הערות מערכת"): Task Focus + secondary Polarity/Category/KB filters
    if (currentWorkMode === 'FINDINGS') {
      if (currentTaskFocus === 'UNKNOWN') {
        return isNoteUnknownStatus(note);
      }
      if (note.is_value_eng) return false;

      if (currentTaskFocus === 'ACTION_NEEDED' && !isNoteActionNeeded(note)) return false;
      if (currentTaskFocus === 'OPPORTUNITIES' && !isNoteOpportunity(note)) return false;
      if (currentTaskFocus === 'PRESERVE' && !isNotePreservationConstraint(note)) return false;

      const cls = classifySystemNote(note);
      if (currentPolarity !== 'ALL' && cls.polarity !== currentPolarity) return false;
      if (currentCategory !== 'ALL' && cls.category !== currentCategory) return false;
      if (currentKnowledgeBase !== 'ALL' && cls.kbId !== currentKnowledgeBase) return false;
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

      // 2. Clean Numbered Pin on Plan with Collision Avoidance & WCAG 2.2 Keyboard Support
      const pin = document.createElement('button');
      pin.type = 'button';
      pin.className = `plan-pin pin-${note.status} ${isVe ? 'pin-VE' : ''} ${isImp ? 'pin-IMP' : ''} ${isNoteActive ? 'active-pin' : ''} ${isNoteHovered ? 'hover-pin' : ''} ${isDimmed ? 'dimmed-pin' : ''}`;
      let pinX = Number(note.cx_pct || 50);
      let pinY = Number(note.cy_pct || 50);
      // Collision avoidance against already-placed pins on the same sheet
      const existingPins = planPinsLayer.querySelectorAll('.plan-pin');
      let collisionIdx = 0;
      existingPins.forEach((ep) => {
        const ex = parseFloat(ep.dataset.rawX || ep.style.left || '50');
        const ey = parseFloat(ep.dataset.rawY || ep.style.top || '50');
        if (Math.hypot(pinX - ex, pinY - ey) < 2.8) {
          collisionIdx += 1;
        }
      });
      pin.dataset.rawX = String(pinX);
      pin.dataset.rawY = String(pinY);
      if (collisionIdx > 0) {
        const angle = (collisionIdx * 135 * Math.PI) / 180;
        pinX = Math.max(2, Math.min(98, +(pinX + Math.cos(angle) * 2.1 * collisionIdx).toFixed(2)));
        pinY = Math.max(2, Math.min(98, +(pinY + Math.sin(angle) * 2.1 * collisionIdx).toFixed(2)));
      }
      pin.style.left = `${pinX}%`;
      pin.style.top = `${pinY}%`;
      pin.textContent = note.pin_num;
      pin.dataset.noteId = note.id;
      pin.setAttribute('aria-label', `סיכה #${note.pin_num}: ${note.room_name} — ${note.title}`);
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

  function build3AxisReliabilityStripHtml(note) {
    if (!note) return '';
    const vStat = note.verification_status || (note.status === 'PASS' ? 'VALID' : note.status === 'UNKNOWN' ? 'UNKNOWN' : 'DEVIATION');
    const vStatHe = note.verification_status_he || (vStat === 'VALID' ? 'תקין (לשימור)' : vStat === 'UNKNOWN' ? 'לא ידוע' : 'חריגה / הזדמנות');
    const evSrcHe = note.evidence_source_he || 'גיאומטריה מחושבת';
    const userDec = getNoteDecision(note.id);
    const wfState = userDec || note.workflow_state || 'TO_CHECK';
    const wfLabelObj = DECISION_LABELS[wfState];
    const wfStateHe = wfLabelObj ? wfLabelObj.label : (note.workflow_state_he || 'לבדיקה');

    return `
      <div class="zt-3axis-strip" aria-label="3 צירי אמינות">
        <span class="zt-axis-badge zt-axis-verif v-${vStat}" title="ציר 1: תוצאת הבדיקה">🔍 תוצאה: ${vStatHe}</span>
        <span class="zt-axis-badge zt-axis-source" title="ציר 2: מקור הראיה">📐 מקור: ${evSrcHe}</span>
        <span class="zt-axis-badge zt-axis-workflow wf-${wfState}" title="ציר 3: מצב העבודה">📋 סטטוס: ${wfStateHe}</span>
      </div>
    `;
  }

  function buildFourPillarsSideDockHtml(note) {
    const vExp = note.visual_explanation || {};
    const rec = vExp.recommendation || {};
    const sol = vExp.solution || {};
    const sav = vExp.savings || {};
    const imp = vExp.building_impact || {};
    const evRec = note.evidence_record || {};
    const cls = classifySystemNote(note);

    const isVe = Boolean(note.is_value_eng);
    const isDesignImp = Boolean(note.is_design_improvement);
    const effPct = sav.efficiency_pct !== undefined ? sav.efficiency_pct : (isVe ? 100 : 0);

    // 4 Decision Value Dimensions (Financial, Planning, Feasibility, Certainty)
    const finImpactText = isVe
      ? `חיסכון ברוטו: ${fmtNum(sav.saving_ils !== undefined ? sav.saving_ils : (note.ve_saving_ils || 0))} ₪ (-${fmtNum(sav.net_contour_sqm || note.ve_saved_sqm || 0)} מ״ר קונטור)`
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
          ? 'מאושר — אילוץ לשימור'
          : 'דורש בדיקת מתכנן ועדכון שרטוט';

    const certaintyText = note.evidence_source_he
      ? `${note.evidence_source_he} (${note.rule_id || 'כלל מערכת'})`
      : (note.rule_id ? `מדידה וקטורית מהתכנית מול תקן (${note.rule_id})` : 'חישוב הנדסי מתוך קואורדינטות התכנית');

    const currentDecision = getNoteDecision(note.id) || note.workflow_state || 'TO_CHECK';

    // Determine "מה לבדוק שוב" (Recheck & Preservation Constraints — Section 5.3)
    const recheckText = isVe
      ? (note.ve_category === 'UG'
          ? 'לוודא רדיוסי סיבוב ברמפה, גובה פנוי (H_clear ≥ 2.20m), אי-פגיעה בקירות ממ״ד יורדים (70%) ונגישות למפרץ החניה החלופי.'
          : note.ve_category === 'FAC'
            ? 'לוודא שמירת עמידות אקלימית, פרטי תפר בין חיפוי יבש לטיח, והנחיות חזית רחוב עירונית.'
            : 'לוודא אי-פגיעה בשטח פלדלת של הדירות, רוחב פרוזדור תקני ואוורור חדר המדרגות.')
      : note.status === 'PASS'
        ? 'אילוץ לשימור: כל שינוי עתידי בקומה חייב לשמר יתרון זה במלואו ללא פגיעה באוורור, בגישה או במידות החלל.'
        : 'בדיקה חוזרת לאחר תיקון: פתיחת דלתות ללא התנגשות, שמירת רוחב מעבר נקי לאחר גמרים, ואי-פגיעה בחדרים סמוכים.';

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

    // Layer 1 Short Finding Card (Section 5.3) + Layer 2 Progressive Disclosure Evidence Drawer
    return `
      <div class="zt-short-card-grid" role="region" aria-label="תקציר ממצא ופעולה">
        <div class="zt-sc-row">
          <span class="zt-sc-lbl">📏 קיים ומקורו:</span>
          <span class="zt-sc-val"><strong>${note.measured || 'לא נמדד'}</strong> <span style="color:#64748b;font-size:10.5px;">(${note.evidence_source_he || 'גיאומטריה מחושבת'})</span></span>
        </div>
        <div class="zt-sc-row">
          <span class="zt-sc-lbl">🎯 יעד ותחולה:</span>
          <span class="zt-sc-val"><strong>${note.benchmark || 'לפי תקן'}</strong> <span style="color:#64748b;font-size:10.5px;">(${cls.categoryHe})</span></span>
        </div>
        <div class="zt-sc-row">
          <span class="zt-sc-lbl">💡 משמעות:</span>
          <span class="zt-sc-val">${rec.finding || note.summary || ''}</span>
        </div>
        <div class="zt-sc-row">
          <span class="zt-sc-lbl">🛠️ אפשרות לשינוי:</span>
          <span class="zt-sc-val" style="color:#1e3a8a;font-weight:700;">${sol.how_to_execute || note.how_to_execute || note.recommendation || ''}</span>
        </div>
        <div class="zt-sc-recheck">
          <strong>🔄 מה לבדוק שוב (אילוצים לשימור):</strong> ${recheckText}
        </div>
      </div>

      <div class="l2-decision-workflow-box" style="margin-top:6px;">
        <div style="font-size:10px;font-weight:800;color:#475569;margin-bottom:3px;">מצב עבודה ומעקב אדריכל (E42 — תיקון ממתין לאימות גרסה חוזרת):</div>
        <div class="l2-dec-buttons">
          <button type="button" class="btn-dec-state ${(currentDecision === 'DECIDED_TO_FIX' || currentDecision === 'TODO') ? 'active dec-todo' : ''}" data-dec="DECIDED_TO_FIX" data-note-id="${note.id}">הוחלט לתקן</button>
          <button type="button" class="btn-dec-state ${(currentDecision === 'FIXED_PENDING_VERIFICATION' || currentDecision === 'VERIFIED') ? 'active dec-verified' : ''}" data-dec="FIXED_PENDING_VERIFICATION" data-note-id="${note.id}" title="סימון שבוצע תיקון מעביר למצב 'תוקן וממתין לאימות' עד לבדיקת תוכנית מעודכנת (E42)">תוקן — ממתין לאימות</button>
          <button type="button" class="btn-dec-state ${(currentDecision === 'CLOSED' || currentDecision === 'APPROVED') ? 'active dec-approved' : ''}" data-dec="CLOSED" data-note-id="${note.id}">נסגר (מאומת)</button>
          <button type="button" class="btn-dec-state ${currentDecision === 'REJECTED' ? 'active dec-rejected' : ''}" data-dec="REJECTED" data-note-id="${note.id}">נדחה</button>
        </div>
      </div>

      <details class="l3-evidence-drawer">
        <summary class="l3-evidence-summary">
          <span>📚 שכבה 2: רשומת ראיה, מקורות תקניים, תחשיב ודיאגרמה</span>
          <span class="l3-chevron">▾</span>
        </summary>
        <div class="l3-evidence-body">
          <div class="zt-evidence-record-box">
            <div><strong>רשומת ראיה (Evidence Record):</strong> מזהה קבוע <code>${evRec.immutable_id || note.id}</code> · גרסת תוכנית: <code>${evRec.plan_version || 'v2026.10'}</code> · כלל: <code>${evRec.rule_id || note.rule_id || '-'} (${evRec.rule_version || '2026.2'})</code></div>
            <div style="margin-top:2px;"><strong>ישויות בתוכנית:</strong> ${(evRec.element_ids || [note.sheet_id, note.room_name]).filter(Boolean).join(' · ')} · <strong>טווח אי-ודאות:</strong> <code>${evRec.uncertainty_range || '±2.0 cm'}</code></div>
            <div style="margin-top:2px;"><strong>${cls.kbIcon} בסיס ידע ומקורות:</strong> ${cls.kbTitleHe} (${cls.kbSourcesHe})</div>
          </div>

          <div class="l2-value-metrics-grid">
            <div class="l2-val-card">
              <span class="l2-val-lbl">סוג ערך והשפעה</span>
              <strong class="l2-val-txt">${note.value_category_he || finImpactText}</strong>
            </div>
            <div class="l2-val-card">
              <span class="l2-val-lbl">השפעה תכנונית</span>
              <strong class="l2-val-txt">${planImpactText}</strong>
            </div>
            <div class="l2-val-card">
              <span class="l2-val-lbl">ישימות ובשלות</span>
              <strong class="l2-val-txt">${note.maturity_stage_he || feasibilityText}</strong>
            </div>
            <div class="l2-val-card">
              <span class="l2-val-lbl">מקור הראיה</span>
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
    const netBd = opt.net_avoidable_cost_breakdown || {};
    const matStage = Number(opt.maturity_stage || 3);
    const guar = opt.zero_damage_guarantees || {};
    const contourAudit = opt.contour_audit_summary || {};
    const agOpt = opt.above_ground_optimization || {};
    const ugOpt = opt.underground_optimization || {};
    const facOpt = opt.facade_cladding_optimization || {};

    const netBaseIls = netBd.net_avoidable_saving_base_ils !== undefined
      ? netBd.net_avoidable_saving_base_ils
      : (kpis.net_avoidable_saving_base_ils !== undefined ? kpis.net_avoidable_saving_base_ils : (kpis.grand_total_direct_saving_ils || 0));
    const grossDirectIls = netBd.gross_direct_saving_ils !== undefined
      ? netBd.gross_direct_saving_ils
      : (kpis.grand_total_direct_saving_ils || 0);
    const adaptDeductionIls = netBd.less_adaptation_and_details_ils || 0;
    const redesignDeductionIls = netBd.less_redesign_and_coordination_ils || 0;
    const riskDeductionIls = netBd.less_schedule_and_risk_buffer_ils || 0;
    const consScenarioIls = netBd.conservative_scenario_ils !== undefined ? netBd.conservative_scenario_ils : Math.round(netBaseIls * 0.8);
    const optScenarioIls = netBd.optimistic_scenario_ils !== undefined ? netBd.optimistic_scenario_ils : grossDirectIls;

    valueEngModalTitle.textContent = `💰 מודל חיסכון נטו (עלויות נמנעות) ובקרת קונטור — ${data.project_name}`;

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
    const facDirItems = facOpt.by_facade || [];
    let mainFacadesSqm = Number(facOpt.main_facades_opaque_sqm || 0);
    let sideFacadesSqm = Number(facOpt.side_and_rear_facades_opaque_sqm || 0);
    if (!mainFacadesSqm && !sideFacadesSqm && facDirItems.length > 0) {
      facDirItems.forEach((f) => {
        const opq = Number(f.opaque_area_sqm || 0);
        const fn = String(f.facade_name || '');
        const isMain = fn.includes('ראשית') || (fn.includes('רחוב') && !fn.includes('עורפית') && !fn.includes('צד'));
        if (isMain) mainFacadesSqm += opq;
        else sideFacadesSqm += opq;
      });
    }
    const presetPlasterPct = Number(
      facOpt.preset_plaster_pct ||
        (totalOpaque > 0 && sideFacadesSqm > 0
          ? Math.max(1, Math.min(100, Math.round((sideFacadesSqm / totalOpaque) * 100)))
          : Math.max(1, Math.min(100, Math.round(Number(facOpt.optimized_plaster_pct || 75)))))
    );
    const presetDryPct = 100 - presetPlasterPct;
    const presetPlasterSqm = Math.round(totalOpaque * (presetPlasterPct / 100.0) * 10) / 10;
    const presetDrySqm = Math.round((totalOpaque - presetPlasterSqm) * 10) / 10;
    const presetFacSavingIls = Math.round(presetPlasterSqm * 400);
    const presetGrandTotalIls = Math.round(baseAgSaved * 6200) + Math.round(baseUgSaved * 3500) + presetFacSavingIls;
    const presetSplitText =
      facOpt.preset_split_rule_he ||
      `פריסט פרויקט: חזיתות עיקריות חיפוי יבש (${presetDryPct}% = ${fmtNum(Math.round(mainFacadesSqm || presetDrySqm))} מ״ר) · חזיתות צד טיח (${presetPlasterPct}% = ${fmtNum(Math.round(sideFacadesSqm || presetPlasterSqm))} מ״ר)`;

    const agBeforeSqm = Number(agOpt.current_total_above_ground_sqm || 1);
    const agAfterSqm = Number(agOpt.optimized_total_above_ground_sqm || agBeforeSqm);
    const agAfterPct = Math.max(60, Math.min(99, Math.round((agAfterSqm / agBeforeSqm) * 100)));

    const ugBeforeSqm = Number(ugOpt.current_total_underground_sqm || 1);
    const ugAfterSqm = Number(ugOpt.optimized_total_underground_sqm || ugBeforeSqm);
    const ugAfterPct = Math.max(60, Math.min(99, Math.round((ugAfterSqm / ugBeforeSqm) * 100)));

    valueEngModalBody.innerHTML = `
      <!-- Top 4 Construction Cost Savings KPI Boxes (Net vs Gross & Value Categories — Section 4.1–4.6) -->
      <div class="modal-kpi-strip" style="grid-template-columns: repeat(4, 1fr); margin-bottom: 10px;">
        <div class="modal-kpi-box" style="border-top-color:#059669;background:#ecfdf5;">
          <div class="k-title" style="color:#065f46;">💰 אומדן חיסכון נטו (בכפוף לבדיקות)</div>
          <div class="k-num" style="color:#047857;" id="ve-kpi-grand-total">${fmtNum(netBaseIls)} ₪</div>
          <div class="k-desc" style="color:#065f46;">ברוטו: ${fmtNum(grossDirectIls)} ₪ · טווח: ${fmtNum(consScenarioIls)}–${fmtNum(optScenarioIls)} ₪</div>
        </div>
        <div class="modal-kpi-box" style="border-top-color:#2563eb;">
          <div class="k-title">🏢 חיסכון קונטור עילי (6,200 ₪/מ״ר)</div>
          <div class="k-num" id="ve-kpi-ag-ils">${fmtNum(kpis.above_ground_saving_ils)} ₪</div>
          <div class="k-desc">נבנה פחות: ${fmtNum(kpis.above_ground_saved_sqm)} מ״ר (נוכו ${fmtNum(contourAudit.rejected_locked_ag_core_sqm)} מ״ר ליבה כלואה)</div>
        </div>
        <div class="modal-kpi-box" style="border-top-color:#0284c7;">
          <div class="k-title">🅿️ חיסכון קונטור חניון (3,500 ₪/מ״ר)</div>
          <div class="k-num" id="ve-kpi-ug-ils">${fmtNum(kpis.underground_saving_ils)} ₪</div>
          <div class="k-desc">נבנה פחות: ${fmtNum(kpis.underground_saved_sqm)} מ״ר (נוכו ${fmtNum(contourAudit.rejected_locked_ug_zone_sqm)} מ״ר רמפה ותמרון)</div>
        </div>
        <div class="modal-kpi-box" style="border-top-color:#d97706;">
          <div class="k-title">🧱 חיפוי יבש מול טיח (400 ₪/מ״ר)</div>
          <div class="k-num" id="ve-kpi-fac-ils">${fmtNum(kpis.facade_saving_ils)} ₪</div>
          <div class="k-desc">המרת <span id="ve-kpi-fac-sqm">${fmtNum(kpis.facade_converted_to_plaster_sqm)}</span> מ״ר מחיפוי יבש (700 ₪) לטיח (300 ₪)</div>
        </div>
      </div>

      <!-- 5-Stage Savings Maturity Stepper (Section 4.2) -->
      <div class="zt-maturity-stepper" role="region" aria-label="שלבי בשלות החיסכון">
        <div class="zt-mat-step ${matStage > 1 ? 'done' : matStage === 1 ? 'current' : ''}">1. הזדמנות לבדיקה</div>
        <div class="zt-mat-step ${matStage > 2 ? 'done' : matStage === 2 ? 'current' : ''}">2. חלופה מתוארת</div>
        <div class="zt-mat-step ${matStage > 3 ? 'done' : matStage === 3 ? 'current' : ''}">3. נבדקה גיאומטרית</div>
        <div class="zt-mat-step ${matStage > 4 ? 'done' : matStage === 4 ? 'current' : ''}">4. מתואמת ומתומחרת (יועצים)</div>
        <div class="zt-mat-step ${matStage === 5 ? 'current' : ''}">5. חיסכון ממומש בחוזה</div>
      </div>

      <!-- UNIFIED SAVINGS COMMAND CENTER TAB NAVIGATION BAR (Click to switch views cleanly) -->
      <div class="ve-hub-tabs-bar">
        <button type="button" class="ve-hub-tab-btn active" data-ve-tab="overview">
          📊 1. תחשיב נטו וסימולטור
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
          🛋️ 6. שיפור שימושיות (+${fmtNum(kpis.total_design_improvement_sqm)} מ״ר = 0 ₪ שלד)
        </button>
      </div>

      <!-- TAB 1: OVERVIEW, NET AVOIDABLE COST TABLE, BEFORE/AFTER BOARD & LIVE SIMULATOR -->
      <div class="ve-hub-tab-pane active" data-ve-pane="overview">
        <!-- Net Avoidable Cost Breakdown Table (Section 4.3 & 4.6) -->
        <div class="modal-section-card" style="margin-bottom:14px;border-color:#6ee7b7;background:#f8fafc;">
          <h3>🧮 פירוק עלות נמנעת נטו (Net Avoidable Cost Breakdown — לפי מתודולוגיית RICS NRM)</h3>
          <div class="sec-note">חיסכון נטו = עלויות ישירות שנמנעות − תשתיות ופרטי מעבר − תכנון מחדש ותיאום יועצים − השפעת ביצוע ולו״ז (${netBd.tax_and_unit_basis_he || 'לפני מע״מ, מחירון 2026'}).</div>
          <table class="modal-data-table">
            <thead>
              <tr>
                <th>רכיב בתחשיב</th>
                <th>הסבר הנדסי ותכולה</th>
                <th>סכום (₪)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>1. הפרש עלויות ישיר ברוטו (Gross Direct Saving)</strong></td>
                <td>כיווץ קונטור עילי (-${fmtNum(kpis.above_ground_saved_sqm)} מ״ר) + כיווץ מרתף (-${fmtNum(kpis.underground_saved_sqm)} מ״ר) + המרת חיפוי (${fmtNum(kpis.facade_converted_to_plaster_sqm)} מ״ר)</td>
                <td style="font-weight:800;color:#047857;">+${fmtNum(grossDirectIls)} ₪</td>
              </tr>
              <tr>
                <td><strong>2. בניכוי: תשתיות ופרטי מעבר נוספים</strong></td>
                <td>פרופילי קצה ואיטום בתפר חיפוי/טיח, התאמות ניקוז ופתחי אוורור בחדר משאבות תחת רמפה</td>
                <td style="font-weight:700;color:#dc2626;">−${fmtNum(adaptDeductionIls)} ₪</td>
              </tr>
              <tr>
                <td><strong>3. בניכוי: תכנון מחדש ותיאום יועצים</strong></td>
                <td>עדכון תוכניות אדריכלות, קונסטרוקציה, אינסטלציה ותנועה עבור החלופה שנבחרה</td>
                <td style="font-weight:700;color:#dc2626;">−${fmtNum(redesignDeductionIls)} ₪</td>
              </tr>
              <tr>
                <td><strong>4. בניכוי: השפעת ביצוע, לו״ז ומרווח ביטחון</strong></td>
                <td>מרווח אי-ודאות ביצועי להתאמות בשלב התכנון הנוכחי</td>
                <td style="font-weight:700;color:#dc2626;">−${fmtNum(riskDeductionIls)} ₪</td>
              </tr>
              <tr class="total-row" style="background:#dcfce7;color:#065f46;border-top:2px solid #059669;">
                <td><strong>אומדן חיסכון נטו בתרחיש הבסיס (בכפוף לבדיקות המפורטות)</strong></td>
                <td>טווח תרחישים: שמרני (${fmtNum(consScenarioIls)} ₪) עד מיטבי (${fmtNum(optScenarioIls)} ₪) · שלב בשלות ${matStage}/5</td>
                <td style="font-size:15px;font-weight:900;color:#047857;">${fmtNum(netBaseIls)} ₪</td>
              </tr>
            </tbody>
          </table>
        </div>

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
              <div class="ve-sim-title">🧮 סימולטור חיסכון אינטראקטיבי — צמצום קונטור בנייה מאומת ויחס טיח / חיפוי יבש (1%–100%)</div>
              <div style="font-size:12px;color:#94a3b8;margin-top:2px;">הזז את המחוונים (1%–100%) · ${presetSplitText}</div>
            </div>
            <div class="ve-sim-total-pill" id="ve-sim-live-total">
              סה״כ חיסכון בסימולציה: ${fmtNum(presetGrandTotalIls)} ₪
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
                <span>🧱 % טיח / חיפוי יבש (מתוך ${fmtNum(totalOpaque)} מ״ר אטום · 1%–100%):</span>
                <strong id="sim-lbl-fac-pct">${presetPlasterPct}% טיח (${fmtNum(presetPlasterSqm)} מ״ר) / ${presetDryPct}% חיפוי יבש (${fmtNum(presetDrySqm)} מ״ר)</strong>
              </label>
              <input type="range" id="sim-range-fac-pct" min="1" max="100" step="1" value="${presetPlasterPct}" />
              <div style="display:flex;align-items:center;justify-content:space-between;gap:6px;margin-top:4px;">
                <div class="sim-sub-val" id="sim-val-fac-ils">חיסכון חזיתות (400 ₪/מ״ר טיח מול יבש): ${fmtNum(presetFacSavingIls)} ₪</div>
                <button type="button" id="btn-reset-fac-preset" class="ctrl-btn" style="font-size:10.5px;padding:2px 7px;" title="${presetSplitText}">פריסט: עיקריות יבש (${presetDryPct}%) / צד טיח (${presetPlasterPct}%)</button>
              </div>
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
    const btnResetFacPreset = valueEngModalBody.querySelector('#btn-reset-fac-preset');

    function updateLiveSimulation() {
      const agSqm = Number(rangeAg ? rangeAg.value : baseAgSaved);
      const ugSqm = Number(rangeUg ? rangeUg.value : baseUgSaved);
      const facPct = Math.max(1, Math.min(100, Number(rangeFac ? rangeFac.value : presetPlasterPct)));
      const dryPct = 100 - facPct;

      const agIls = Math.round(agSqm * 6200);
      const ugIls = Math.round(ugSqm * 3500);
      const facConvSqm = Math.round(totalOpaque * (facPct / 100.0) * 10) / 10;
      const facDrySqm = Math.round((totalOpaque - facConvSqm) * 10) / 10;
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
      if (lblFac) lblFac.textContent = `${facPct}% טיח (${fmtNum(facConvSqm)} מ״ר) / ${dryPct}% חיפוי יבש (${fmtNum(facDrySqm)} מ״ר)`;
      if (valFac) valFac.textContent = `חיסכון חזיתות (400 ₪/מ״ר טיח מול יבש): ${fmtNum(facIls)} ₪`;
      if (liveTot) liveTot.textContent = `סה״כ חיסכון בסימולציה: ${fmtNum(grandTotalIls)} ₪`;
    }

    if (rangeAg) rangeAg.addEventListener('input', updateLiveSimulation);
    if (rangeUg) rangeUg.addEventListener('input', updateLiveSimulation);
    if (rangeFac) rangeFac.addEventListener('input', updateLiveSimulation);
    if (btnResetFacPreset && rangeFac) {
      btnResetFacPreset.addEventListener('click', () => {
        rangeFac.value = String(presetPlasterPct);
        updateLiveSimulation();
      });
    }

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

  function jumpToSystemFilter(polarity, category, kbId) {
    if (kbId === 'KB_VALUE_ENG_BIM') {
      currentVeCategory = 'ALL';
      veCatBtns.forEach((b) => b.classList.toggle('active', b.dataset.veCat === 'ALL'));
      switchWorkMode('OPTIMIZATION');
      return;
    }
    currentPolarity = polarity || 'ALL';
    currentCategory = category || 'ALL';
    currentKnowledgeBase = kbId || 'ALL';
    polarityBtns.forEach((b) => b.classList.toggle('active', b.dataset.polarity === currentPolarity));
    catFilterBtns.forEach((b) => b.classList.toggle('active', b.dataset.category === currentCategory));
    kbFilterBtns.forEach((b) => b.classList.toggle('active', b.dataset.kb === currentKnowledgeBase));
    if (currentProject) {
      updateSystemFilterCounts(currentProject);
    }
    switchWorkMode('FINDINGS', { preserveSubfilters: true });
  }

  function buildClientFallbackKbBreakdown(notes) {
    const order = [
      'KB_ISRAELI_STATUTORY',
      'KB_INTL_HOUSING',
      'KB_SPACE_SYNTAX',
      'KB_ERGONOMICS_INTERIOR',
      'KB_DAYLIGHT_IEQ',
      'KB_ADAPTABILITY_FAMILY',
      'KB_ACOUSTICS_MEP',
      'KB_URBAN_LOCAL',
      'KB_VALUE_ENG_BIM',
    ];
    const groups = {};
    order.forEach((k) => {
      const m = KB_META_CATALOG[k];
      groups[k] = {
        kb_id: m.id,
        kb_icon: m.icon,
        kb_short_he: m.shortHe,
        kb_title_he: m.titleHe,
        kb_sources_he: m.sourcesHe,
        kb_description_he: '',
        kb_color: m.color,
        kb_bg: m.bg,
        kb_border: m.border,
        total_count: 0,
        positive_count: 0,
        negative_count: 0,
        savings_count: 0,
        bullets: [],
      };
    });
    (notes || []).forEach((n) => {
      const cls = classifySystemNote(n);
      const g = groups[cls.kbId] || groups.KB_INTL_HOUSING;
      g.total_count += 1;
      if (cls.polarity === 'SAVINGS') g.savings_count += 1;
      else if (cls.polarity === 'POSITIVE') g.positive_count += 1;
      else g.negative_count += 1;
      g.bullets.push({
        note_id: n.id,
        pin_num: n.pin_num,
        sheet_id: n.sheet_id,
        room_name: n.room_name || '',
        title: n.title || '',
        status: n.status || 'WARN',
        polarity: cls.polarity,
        polarity_he: cls.polarity === 'SAVINGS' ? 'חיסכון והנדסת ערך' : cls.polarity === 'POSITIVE' ? 'יתרון תכנוני (תקין)' : 'לשיפור / תשומת לב',
        rule_id: n.rule_id || '',
        measured: n.measured || '',
        recommendation: n.recommendation || '',
        pleasant_text: `${n.summary || n.measured || ''}${n.recommendation ? ` — מומלץ: ${n.recommendation}` : ''}`,
      });
    });
    return order.map((k) => groups[k]).filter((g) => g.total_count > 0);
  }

  function buildOverviewModeElement(data) {
    const pds = data.project_data_summary || {};
    const opt = pds.design_optimization || {};
    const optKpis = opt.executive_kpis || {};
    const contourAudit = opt.contour_audit_summary || {};
    const sdoc = pds.summary_document || {};
    const cvr = sdoc.concise_verbal_review || {};
    const archNar = cvr.architect_narrative || {};
    const notes = data.notes || [];
    const sysNotes = notes.filter((n) => !n.is_value_eng);
    const veNotes = notes.filter((n) => Boolean(n.is_value_eng));

    const negNotes = sysNotes.filter((n) => classifySystemNote(n).polarity === 'NEGATIVE');
    const posNotes = sysNotes.filter((n) => classifySystemNote(n).polarity === 'POSITIVE');

    // Find pin/note ID helper by pin_num or note_id
    const findNoteByPinOrId = (pinNum, noteId) => {
      if (noteId) {
        const byId = notes.find((n) => n.id === noteId);
        if (byId) return byId;
      }
      if (pinNum !== undefined && pinNum !== null) {
        return notes.find((n) => Number(n.pin_num) === Number(pinNum));
      }
      return null;
    };

    // 1. General Architectural Overview Paragraphs (טקסט שוטף של אדריכל)
    const overviewParagraphs = Array.isArray(archNar.general_overview_paragraphs) && archNar.general_overview_paragraphs.length > 0
      ? archNar.general_overview_paragraphs
      : [
          cvr.executive_paragraph || sdoc.overall_verdict || data.project_subtitle ||
          `בסקירה האדריכלית של הפרויקט נבחנו תכניות הקומות, חתכי הבניין והמודל התלת-ממדי אל מול תקנות התכנון והבנייה, תקני איכות הדיור הבינלאומיים ומדדי הארגונומיה וזרימת החלל.`,
        ];

    const identityBadges = Array.isArray(archNar.identity_badges) && archNar.identity_badges.length > 0
      ? archNar.identity_badges
      : [
          `ציון איכות תכנון: ${data.overall_score || '90.0'}/100`,
          `${posNotes.length} יתרונות ונקודות חוזק`,
          `${negNotes.length} נקודות לשיפור`,
          `${veNotes.length} מוקדי הנדסת ערך וחיסכון`,
        ];

    const identityBadgesHtml = identityBadges
      .map((b) => `<span class="ov-identity-pill">${b}</span>`)
      .join('');

    const overviewProseHtml = overviewParagraphs
      .map((p) => `<p class="ov-arch-paragraph">${p}</p>`)
      .join('');

    // 2. Pros Narrative + Bullets (יתרונות הפרויקט — טקסט שוטף + בוליטים)
    const prosNarrativeText = archNar.pros_narrative ||
      `נקודות החוזק המרכזיות של הפרויקט באות לידי ביטוי ב-${posNotes.length} ממצאים חיוביים שעמדו בהצלחה מלאה בדרישות הרישוי, המיגון ואיכות החיים הדירתית:`;

    const prosBulletsList = Array.isArray(archNar.pros_bullets) && archNar.pros_bullets.length > 0
      ? archNar.pros_bullets
      : posNotes.map((n) => {
          const cls = classifySystemNote(n);
          return {
            title: `${n.room_name} — ${n.title}`,
            text: `${n.summary || n.measured}${n.recommendation ? ` (${n.recommendation})` : ''}`,
            pin_num: n.pin_num,
            note_id: n.id,
            kb_badge: `${cls.kbIcon} ${cls.kbShortHe}`,
          };
        });

    const prosBulletsHtml = prosBulletsList
      .map((b) => {
        const matchedNote = findNoteByPinOrId(b.pin_num, b.note_id);
        const nidAttr = matchedNote ? `data-note-id="${matchedNote.id}"` : '';
        const pinHtml = b.pin_num ? `<span class="ov-bullet-pin pin-pos" title="לחץ למיקוד בסיכה #${b.pin_num} על התכנית">#${b.pin_num}</span>` : `<span class="ov-bullet-pin pin-pos">✓</span>`;
        const kbBadgeHtml = b.kb_badge ? `<span class="ov-inline-kb-tag">${b.kb_badge}</span>` : '';
        return `
          <li class="ov-arch-bullet bullet-pos" ${nidAttr}>
            ${pinHtml}
            <div class="ov-arch-bullet-content">
              <div class="ov-arch-bullet-top">
                <strong class="ov-arch-bullet-title">${b.title}</strong>
                ${kbBadgeHtml}
              </div>
              <div class="ov-arch-bullet-text">${b.text}</div>
            </div>
          </li>
        `;
      })
      .join('');

    // 3. Cons Narrative + Bullets (חסרונות ונקודות לשיפור — טקסט שוטף + בוליטים אופרטיביים)
    const consNarrativeText = archNar.cons_narrative ||
      `לצד היתרונות התכנוניים, זיהתה הבקרה האדריכלית ${negNotes.length} נקודות תורפה ופשרות תכנוניות שמומלץ לטפל בהן כדי לשדרג את נוחות המגורים ולמנוע חיכוך תפקודי:`;

    const consBulletsList = Array.isArray(archNar.cons_bullets) && archNar.cons_bullets.length > 0
      ? archNar.cons_bullets
      : negNotes.map((n) => {
          const cls = classifySystemNote(n);
          return {
            title: `${n.room_name} — ${n.title}`,
            text: `${n.summary || n.measured}${n.recommendation ? ` — פתרון מומלץ: ${n.recommendation}` : ''}`,
            pin_num: n.pin_num,
            note_id: n.id,
            kb_badge: `${cls.kbIcon} ${cls.kbShortHe}`,
          };
        });

    const consBulletsHtml = consBulletsList
      .map((b) => {
        const matchedNote = findNoteByPinOrId(b.pin_num, b.note_id);
        const nidAttr = matchedNote ? `data-note-id="${matchedNote.id}"` : '';
        const pinHtml = b.pin_num ? `<span class="ov-bullet-pin pin-neg" title="לחץ למיקוד בסיכה #${b.pin_num} על התכנית">#${b.pin_num}</span>` : `<span class="ov-bullet-pin pin-neg">!</span>`;
        const kbBadgeHtml = b.kb_badge ? `<span class="ov-inline-kb-tag">${b.kb_badge}</span>` : '';
        return `
          <li class="ov-arch-bullet bullet-neg" ${nidAttr}>
            ${pinHtml}
            <div class="ov-arch-bullet-content">
              <div class="ov-arch-bullet-top">
                <strong class="ov-arch-bullet-title">${b.title}</strong>
                ${kbBadgeHtml}
              </div>
              <div class="ov-arch-bullet-text">${b.text}</div>
            </div>
          </li>
        `;
      })
      .join('');

    // 4. Value Engineering & Interior Improvement Narrative
    const veNarrativeText = archNar.ve_and_improvement_narrative ||
      `בגזרת ההשבחה התכנונית והנדסת הערך (Value Engineering), אותר פוטנציאל חיסכון ישיר של ${fmtNum(optKpis.grand_total_direct_saving_ils)} ₪ באמצעות כיווץ קונטור מאומת של ${fmtNum(contourAudit.total_verified_contour_saved_sqm)} מ״ר ואופטימיזציית תמהיל חיפוי החזיתות, לצד השבחת פנים של +${fmtNum(optKpis.total_design_improvement_sqm)} מ״ר — ללא אובדן מ״ר דירתי או חניות.`;

    // 5. Knowledge Base Breakdown (חלוקה לסוגי הערות לפי בסיס הידע שעל פיו ההערה ניתנה)
    const kbBreakdown = Array.isArray(cvr.knowledge_base_breakdown) && cvr.knowledge_base_breakdown.length > 0
      ? cvr.knowledge_base_breakdown
      : buildClientFallbackKbBreakdown(notes);

    const kbQuickPillsHtml = kbBreakdown
      .map((kb) => `
        <button type="button" class="ov-kb-summary-pill" data-jump-kb="${kb.kb_id}" style="background:${kb.kb_bg || '#f8fafc'};border-color:${kb.kb_border || '#cbd5e1'};color:${kb.kb_color || '#0f172a'};" title="לחץ לסינון הערות לפי בסיס ידע: ${kb.kb_title_he}">
          <span>${kb.kb_icon} ${kb.kb_short_he}</span>
          <strong>(${kb.total_count})</strong>
        </button>
      `)
      .join('');

    const kbCardsHtml = kbBreakdown
      .map((kb, idx) => {
        const isVeKb = kb.kb_id === 'KB_VALUE_ENG_BIM';
        const countsBadges = [];
        if (kb.positive_count > 0) {
          countsBadges.push(`<span class="ov-kb-stat-badge stat-pos">🟢 ${kb.positive_count} יתרונות</span>`);
        }
        if (kb.negative_count > 0) {
          countsBadges.push(`<span class="ov-kb-stat-badge stat-neg">🔴 ${kb.negative_count} לשיפור</span>`);
        }
        if (kb.savings_count > 0) {
          countsBadges.push(`<span class="ov-kb-stat-badge stat-ve">💰 ${kb.savings_count} מוקדי חיסכון</span>`);
        }

        const kbBulletsHtml = (kb.bullets || kb.items || [])
          .map((item) => {
            const polCls = item.polarity === 'SAVINGS' ? 'kb-item-ve' : item.polarity === 'POSITIVE' ? 'kb-item-pos' : 'kb-item-neg';
            const polTagCls = item.polarity === 'SAVINGS' ? 'tag-ve' : item.polarity === 'POSITIVE' ? 'tag-pos' : 'tag-neg';
            const nid = item.note_id || item.id || '';
            const polLabel = item.polarity_he || (item.polarity === 'SAVINGS' ? 'חיסכון והנדסת ערך' : item.polarity === 'POSITIVE' ? 'יתרון תכנוני (תקין)' : 'לשיפור / תשומת לב');
            const descTxt = item.pleasant_text || `${item.explanation_he || item.measured || ''}${item.recommendation_he ? ` · המלצה: ${item.recommendation_he}` : ''}`;
            return `
              <li class="ov-kb-bullet-item ${polCls}" data-note-id="${nid}">
                <span class="ov-bullet-pin">#${item.pin_num}</span>
                <div class="ov-kb-bullet-body">
                  <div class="ov-kb-bullet-hdr">
                    <strong>${item.room_name} — ${item.title}</strong>
                    <div class="ov-kb-bullet-meta">
                      <span class="ov-kb-pol-tag ${polTagCls}">${polLabel}</span>
                      ${item.rule_id ? `<code class="ov-kb-rule-code">${item.rule_id}</code>` : ''}
                    </div>
                  </div>
                  <div class="ov-kb-bullet-desc">${descTxt}</div>
                </div>
              </li>
            `;
          })
          .join('');

        return `
          <details class="ov-kb-group-details" ${idx < 3 ? 'open' : ''} style="border-right: 4px solid ${kb.kb_color || '#1e40af'};">
            <summary class="ov-kb-group-summary">
              <div class="ov-kb-group-title-wrap">
                <div class="ov-kb-group-title">
                  <span>${kb.kb_icon} ${kb.kb_title_he}</span>
                </div>
                <div class="ov-kb-sources-line">
                  <strong>בסיס הידע והמקורות:</strong> ${kb.kb_sources_he}
                </div>
              </div>
              <div class="ov-kb-group-right">
                <div class="ov-kb-counts-row">
                  ${countsBadges.join('')}
                </div>
                <button type="button" class="ov-filter-jump-btn" data-jump-kb="${kb.kb_id}">
                  ${isVeKb ? 'למרכז החיסכון ◂' : 'סנן ב״הערות מערכת״ ◂'}
                </button>
              </div>
            </summary>
            <div class="ov-kb-group-body">
              ${kb.kb_description_he ? `<p class="ov-kb-desc-paragraph">${kb.kb_description_he}</p>` : ''}
              <ul class="ov-kb-bullet-list">
                ${kbBulletsHtml}
              </ul>
            </div>
          </details>
        `;
      })
      .join('');

    // 6. Functional Quick Breakdown (תקן / איכות תכנון אדריכלי / טיפ עיצוב פנים)
    const groupByCat = (list) => ({
      STANDARD: list.filter((n) => classifySystemNote(n).category === 'STANDARD'),
      ARCH_QUALITY: list.filter((n) => classifySystemNote(n).category === 'ARCH_QUALITY'),
      INTERIOR_TIP: list.filter((n) => classifySystemNote(n).category === 'INTERIOR_TIP'),
    });
    const negByCat = groupByCat(negNotes);
    const posByCat = groupByCat(posNotes);

    const wrap = document.createElement('div');
    wrap.className = 'mode-overview-container';

    wrap.innerHTML = `
      <!-- 1. ARCHITECT'S NARRATIVE OVERVIEW HERO CARD -->
      <div class="ov-section-card ov-architect-hero-card">
        <div class="ov-card-header-row">
          <div>
            <div class="ov-card-title">🏛️ ${archNar.architect_title || archNar.architect_title_he || `סקירת אדריכל בודק — ${data.project_name || ''}`}</div>
            <div class="ov-architect-subtitle">${archNar.architect_subtitle || archNar.architect_subtitle_he || data.project_subtitle || 'ניתוח תכנוני שוטף, יתרונות, חסרונות וחלוקה לפי בסיסי הידע'}</div>
          </div>
          <span class="ov-score-pill">ציון תכנון: ${data.overall_score || '—'}</span>
        </div>

        <div class="ov-identity-badges-row">
          ${identityBadgesHtml}
        </div>

        <div class="ov-prose-container">
          ${overviewProseHtml}
        </div>

        <div class="ov-polarity-summary-strip">
          <button type="button" class="ov-pol-chip ov-pol-pos" data-jump-pol="POSITIVE" data-jump-cat="ALL">
            <span class="ov-pol-dot pos"></span>
            <span>יתרונות ונקודות חוזק: <strong>${posNotes.length}</strong></span>
          </button>
          <button type="button" class="ov-pol-chip ov-pol-neg" data-jump-pol="NEGATIVE" data-jump-cat="ALL">
            <span class="ov-pol-dot neg"></span>
            <span>חסרונות / לשיפור: <strong>${negNotes.length}</strong></span>
          </button>
          <button type="button" class="ov-pol-chip ov-pol-ve" id="ov-switch-ve-tab">
            <span>💰 מוקדי חיסכון והנדסת ערך: <strong>${veNotes.length}</strong></span>
          </button>
        </div>
      </div>

      <!-- 2. PROS & STRENGTHS: FLOWING PROSE + BULLETS -->
      <div class="ov-section-card ov-verbal-card ov-verbal-positive">
        <div class="ov-card-header-row">
          <span class="ov-card-title">🟢 יתרונות הפרויקט ונקודות החוזק התכנוניות (${posNotes.length})</span>
          <button type="button" class="btn-link-Action" data-jump-pol="POSITIVE" data-jump-cat="ALL">כל החיוביים ב״הערות מערכת״ ◂</button>
        </div>
        <p class="ov-narrative-intro intro-pos">${prosNarrativeText}</p>
        <ul class="ov-arch-bullets-list">
          ${prosBulletsHtml}
        </ul>
      </div>

      <!-- 3. CONS & CHALLENGES: FLOWING PROSE + OPERATIVE BULLETS -->
      <div class="ov-section-card ov-verbal-card ov-verbal-negative">
        <div class="ov-card-header-row">
          <span class="ov-card-title">🔴 חסרונות, פשרות תכנוניות ונקודות לשיפור (${negNotes.length})</span>
          <button type="button" class="btn-link-Action" data-jump-pol="NEGATIVE" data-jump-cat="ALL">כל השליליים ב״הערות מערכת״ ◂</button>
        </div>
        <p class="ov-narrative-intro intro-neg">${consNarrativeText}</p>
        <ul class="ov-arch-bullets-list">
          ${consBulletsHtml}
        </ul>
      </div>

      <!-- 4. KNOWLEDGE BASE BREAKDOWN (חלוקה לסוגי הערות לפי בסיס הידע שעל פיו ההערה ניתנה) -->
      <div class="ov-section-card ov-kb-section-card">
        <div class="ov-card-header-row">
          <div>
            <div class="ov-card-title">📚 חלוקה לסוגי הערות לפי בסיס הידע שעל פיו ההערה ניתנה (${notes.length} הערות ב-${kbBreakdown.length} בסיסי ידע)</div>
            <div class="ov-architect-subtitle">כל הערה בפרויקט משויכת למקור הידע התכנוני, החוקי או ההנדסי שעל בסיסו היא נקבעה — לחצו לסינון או למיקוד על התכנית</div>
          </div>
        </div>
        <div class="ov-kb-pills-bar">
          ${kbQuickPillsHtml}
        </div>
        <div class="ov-kb-groups-stack">
          ${kbCardsHtml}
        </div>
      </div>

      <!-- 5. VALUE ENGINEERING & INTERIOR IMPROVEMENT NARRATIVE + KPI BOXES -->
      <div class="ov-section-card ov-ve-narrative-card">
        <div class="ov-card-header-row">
          <span class="ov-card-title">💡 פוטנציאל השבחה תכנונית, נצילות שטחים והנדסת ערך (VE)</span>
        </div>
        <p class="ov-narrative-intro intro-ve">${veNarrativeText}</p>
        <div class="ov-kpi-pair">
          <div class="ov-kpi-box" id="ov-open-ve">
            <span class="ov-kpi-lbl">פוטנציאל חיסכון מאומת (בטאב חיסכון)</span>
            <strong class="ov-kpi-val">${fmtNum(optKpis.grand_total_direct_saving_ils)} ₪</strong>
            <span class="ov-kpi-sub">-${fmtNum(contourAudit.total_verified_contour_saved_sqm)} מ״ר קונטור (${veNotes.length} מוקדים) · 0 פגיעה בדירות/חניות</span>
          </div>
          <div class="ov-kpi-box" id="ov-open-areas">
            <span class="ov-kpi-lbl">מאזן שטחים והשבחת פנים</span>
            <strong class="ov-kpi-val">+${fmtNum(optKpis.total_design_improvement_sqm)} מ״ר</strong>
            <span class="ov-kpi-sub">פתיחת טבלאות שטחים מלאות והשבחת דירות</span>
          </div>
        </div>
      </div>

      <!-- 6. COMPACT FUNCTIONAL MATRIX (שלילי / חיובי × תקן / איכות תכנון / עיצוב פנים) -->
      <div class="ov-section-card">
        <div class="ov-card-header-row" style="margin-bottom:6px;">
          <span class="ov-card-title">🗂️ קיצורי דרך לסינון מהיר לפי סיווג תפקודי</span>
        </div>
        <div class="ov-func-matrix-grid">
          <button type="button" class="ov-func-chip neg" data-jump-pol="NEGATIVE" data-jump-cat="STANDARD">
            ⚖️ לשיפור בתקן (${negByCat.STANDARD.length})
          </button>
          <button type="button" class="ov-func-chip neg" data-jump-pol="NEGATIVE" data-jump-cat="ARCH_QUALITY">
            📐 לשיפור באיכות תכנון (${negByCat.ARCH_QUALITY.length})
          </button>
          <button type="button" class="ov-func-chip neg" data-jump-pol="NEGATIVE" data-jump-cat="INTERIOR_TIP">
            🛋️ טיפי עיצוב פנים (${negByCat.INTERIOR_TIP.length})
          </button>
          <button type="button" class="ov-func-chip pos" data-jump-pol="POSITIVE" data-jump-cat="STANDARD">
            ⚖️ תקין בתקן (${posByCat.STANDARD.length})
          </button>
          <button type="button" class="ov-func-chip pos" data-jump-pol="POSITIVE" data-jump-cat="ARCH_QUALITY">
            📐 חוזקות איכות תכנון (${posByCat.ARCH_QUALITY.length})
          </button>
          <button type="button" class="ov-func-chip pos" data-jump-pol="POSITIVE" data-jump-cat="INTERIOR_TIP">
            🛋️ חוזקות עיצוב פנים (${posByCat.INTERIOR_TIP.length})
          </button>
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
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        jumpToSystemFilter(btn.getAttribute('data-jump-pol'), btn.getAttribute('data-jump-cat'), 'ALL');
      });
    });

    wrap.querySelectorAll('[data-jump-kb]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        e.preventDefault();
        jumpToSystemFilter('ALL', 'ALL', btn.getAttribute('data-jump-kb'));
      });
    });

    wrap.querySelectorAll('[data-note-id]').forEach((li) => {
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
        if (currentProject) {
          updateSystemFilterCounts(currentProject);
        }
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
    card.setAttribute('tabindex', '0');
    card.setAttribute('role', 'button');

    let taxBadgesHtml = '';
    const kbPillHtml = `<span class="note-kb-pill" style="background:${clsInfo.kbBg};color:${clsInfo.kbColor};border:1px solid ${clsInfo.kbBorder};" title="בסיס הידע: ${clsInfo.kbTitleHe} (${clsInfo.kbSourcesHe})">${clsInfo.kbIcon} ${clsInfo.kbShortHe}</span>`;
    if (isVe) {
      const veLabel = note.ve_callout_badge || `חיסכון: ${fmtNum(note.ve_saving_ils)} ₪`;
      taxBadgesHtml = `${kbPillHtml}<span class="note-ve-pill">${veLabel}</span>`;
    } else {
      const polClass = clsInfo.polarity === 'NEGATIVE' ? 'pol-neg' : 'pol-pos';
      const catClass = `cat-${clsInfo.category.toLowerCase()}`;
      taxBadgesHtml = `
        ${kbPillHtml}
        <span class="note-polarity-pill ${polClass}">${clsInfo.polarityHe}</span>
        <span class="note-cat-pill ${catClass}">${clsInfo.categoryHe}</span>
      `;
    }

    const posLock = note.position_lock || (note.spatial_3d && note.spatial_3d.position_lock) || null;
    const posLockBadgeHtml = (posLock && posLock.locked)
      ? `<span class="note-cat-pill" style="background:#eff6ff;color:#1d4ed8;border:1px solid #bfdbfe;" title="מיקום דו-ממד (${note.cx_pct}%, ${note.cy_pct}%) ותלת-ממד (${(posLock.actual_3d_xz || []).join(', ')}m) מאומת ומקובע · #${posLock.lock_hash || ''}">🔒 2D↔3D</span>`
      : '';

    const axis3StripHtml = build3AxisReliabilityStripHtml(note);

    card.innerHTML = `
      <div class="note-top-row">
        <div class="note-badges-right">
          <span class="note-pin-circle">#${note.pin_num}</span>
          <span class="note-room-tag">${note.room_name}</span>
        </div>
        <div class="note-badges-left">
          ${posLockBadgeHtml}
          ${taxBadgesHtml}
          ${decObj ? `<span class="note-dec-badge ${decObj.cls}">${decObj.label}</span>` : ''}
        </div>
      </div>
      ${axis3StripHtml}
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
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        highlightNote(note.id, { scrollDoc: false, switchSheet: true, openDock: false, zoomTo: true });
      }
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
      const netBreak = opt.net_avoidable_cost_breakdown || {};
      const netBase = netBreak.net_avoidable_saving_base_ils !== undefined
        ? Number(netBreak.net_avoidable_saving_base_ils)
        : Math.round((Number(optKpis.grand_total_direct_saving_ils) || 0) * 0.72);
      const maturityLabel = opt.maturity_stage_he || 'שלב 3/5: חלופה שנבדקה גיאומטרית';

      const veBanner = document.createElement('div');
      veBanner.className = 've-tab-summary-card';
      veBanner.innerHTML = `
        <div class="ve-tab-summary-row">
          <div>
            <div class="ve-tab-summary-lbl">חיסכון נטו בר־הימנעות (לאחר התאמות ותכנון מחדש) · <span style="color:#fde68a;">${maturityLabel}</span></div>
            <div class="ve-tab-summary-val">${fmtNum(netBase)} ₪ <span style="font-size:12px;font-weight:500;opacity:0.85;">(ברוטו ישיר: ${fmtNum(optKpis.grand_total_direct_saving_ils)} ₪)</span></div>
            <div class="ve-tab-summary-sub">הקטנת קונטור מאומתת: -${fmtNum(contourAudit.total_verified_contour_saved_sqm)} מ״ר + המרת חיפוי יבש זמין בלבד</div>
          </div>
          <button type="button" class="btn-locate-on-plan" id="ve-tab-open-modal">פירוט נטו, 5 שלבי בשלות ודו״ח מלא ◂</button>
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
      currentTaskFocus !== 'ALL' ||
      currentPolarity !== 'ALL' ||
      currentCategory !== 'ALL' ||
      currentKnowledgeBase !== 'ALL';

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
      emptyEl.innerHTML = `
        <div>אין ממצאים בקטגוריה זו עבור הסינון שנבחר (${currentTaskFocus}).</div>
        <button type="button" class="ctrl-btn" style="margin-top:8px;" id="btn-empty-reset-filter">הצג את כל ההערות</button>
      `;
      const resetBtn = emptyEl.querySelector('#btn-empty-reset-filter');
      if (resetBtn) {
        resetBtn.addEventListener('click', () => setTaskFocusFilter('ALL'));
      }
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
      selectSheet(note.sheet_id, { keepNote: true, fromHighlightNote: true });
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
        currentTaskFocus = 'ALL';
        currentPolarity = 'ALL';
        currentCategory = 'ALL';
        currentKnowledgeBase = 'ALL';
        taskFocusBtns.forEach((b) => b.classList.toggle('active', b.dataset.taskFocus === 'ALL'));
        polarityBtns.forEach((b) => b.classList.toggle('active', b.dataset.polarity === 'ALL'));
        catFilterBtns.forEach((b) => b.classList.toggle('active', b.dataset.category === 'ALL'));
        kbFilterBtns.forEach((b) => b.classList.toggle('active', b.dataset.kb === 'ALL'));
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
      isVePlanBarCollapsed = false;
      if (docSubfilterBar) docSubfilterBar.classList.add('hidden');
      if (veSubfilterBar) veSubfilterBar.classList.remove('hidden');
      if (btnToggleVePlanMode) btnToggleVePlanMode.classList.add('active');
      if (vePlanBar && !isPlanToolbarCollapsed) vePlanBar.classList.remove('hidden');
      if (btnRestoreVePlanBar) btnRestoreVePlanBar.classList.add('hidden');
    } else if (currentWorkMode === 'FINDINGS') {
      currentFilter = 'ALL';
      if (!opts.preserveSubfilters) {
        taskFocusBtns.forEach((b) => b.classList.toggle('active', b.dataset.taskFocus === currentTaskFocus));
        polarityBtns.forEach((b) => b.classList.toggle('active', b.dataset.polarity === currentPolarity));
        catFilterBtns.forEach((b) => b.classList.toggle('active', b.dataset.category === currentCategory));
        kbFilterBtns.forEach((b) => b.classList.toggle('active', b.dataset.kb === currentKnowledgeBase));
      }
      if (docSubfilterBar) docSubfilterBar.classList.remove('hidden');
      if (veSubfilterBar) veSubfilterBar.classList.add('hidden');
      if (btnToggleVePlanMode) btnToggleVePlanMode.classList.remove('active');
      if (vePlanBar) vePlanBar.classList.add('hidden');
      if (btnRestoreVePlanBar) btnRestoreVePlanBar.classList.add('hidden');
    } else {
      // OVERVIEW or COMPARE
      currentFilter = 'ALL';
      if (docSubfilterBar) docSubfilterBar.classList.add('hidden');
      if (veSubfilterBar) veSubfilterBar.classList.add('hidden');
      if (btnToggleVePlanMode) btnToggleVePlanMode.classList.remove('active');
      if (vePlanBar) vePlanBar.classList.add('hidden');
      if (btnRestoreVePlanBar) btnRestoreVePlanBar.classList.add('hidden');
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

  // Primary Task-Focus Filter Buttons (נדרש טיפול / הזדמנויות / לשימור / מידע חסר / הכל)
  taskFocusBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      setTaskFocusFilter(btn.dataset.taskFocus || 'ALL');
    });
  });

  // Secondary Polarity Filter Buttons (הכל / שלילי / חיובי) in System Notes tab
  polarityBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      currentPolarity = btn.dataset.polarity || 'ALL';
      currentTaskFocus = 'ALL';
      taskFocusBtns.forEach((b) => b.classList.toggle('active', b.dataset.taskFocus === 'ALL'));
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
      currentTaskFocus = 'ALL';
      taskFocusBtns.forEach((b) => b.classList.toggle('active', b.dataset.taskFocus === 'ALL'));
      catFilterBtns.forEach((b) => b.classList.toggle('active', b === btn));
      if (currentProject) {
        updateSystemFilterCounts(currentProject);
        renderDocumentSections(currentProject);
        renderVisualPlanAnnotations();
      }
    });
  });

  // Tertiary Knowledge Base Filter Buttons (סינון לפי בסיס הידע שעל פיו ההערה ניתנה)
  kbFilterBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      currentKnowledgeBase = btn.dataset.kb || 'ALL';
      currentTaskFocus = 'ALL';
      taskFocusBtns.forEach((b) => b.classList.toggle('active', b.dataset.taskFocus === 'ALL'));
      kbFilterBtns.forEach((b) => b.classList.toggle('active', b === btn));
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
    syncCollapsedBarsRestoreUi();
  }

  if (btnCollapseTopBar) {
    btnCollapseTopBar.addEventListener('click', () => toggleTopBar(false));
  }
  if (btnExpandTopBar) {
    btnExpandTopBar.addEventListener('click', () => toggleTopBar(true));
  }
  if (btnRestoreTopBarFloating) {
    btnRestoreTopBarFloating.addEventListener('click', () => toggleTopBar(true));
  }

  // Collapsible / Compact Floor Tabs & Plan Toolbar Handlers
  if (btnToggleSheetsCompact) {
    btnToggleSheetsCompact.addEventListener('click', () => toggleSheetsCompact());
  }
  if (btnCollapsePlanToolbar) {
    btnCollapsePlanToolbar.addEventListener('click', () => togglePlanToolbar(true));
  }
  if (btnRestorePlanToolbar) {
    btnRestorePlanToolbar.addEventListener('click', () => togglePlanToolbar(false));
  }
  if (btnRestoreAllBars) {
    btnRestoreAllBars.addEventListener('click', () => restoreAllBarsAndPanels());
  }
  if (btnCollapseVePlanBar) {
    btnCollapseVePlanBar.addEventListener('click', () => toggleVePlanBarCollapse(true));
  }
  if (btnRestoreVePlanBar) {
    btnRestoreVePlanBar.addEventListener('click', () => toggleVePlanBarCollapse(false));
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
      toggleSideDock(false);
      toggleTopBar(false);
      toggleSheetsCompact(true);
      syncCollapsedBarsRestoreUi();
    } else {
      restoreAllBarsAndPanels();
    }
  }

  if (btnFocusMode) {
    btnFocusMode.addEventListener('click', () => toggleFocusMode());
  }

  // Architect Action Package & Decision Tracking Modal (Section 6.1–6.4, E38, E42)
  let currentArchPkgFilter = 'ALL';

  function openDecisionsExportModal() {
    if (!currentProject || !decisionsExportModal || !decisionsModalBody) return;
    const notes = currentProject.notes || [];
    const pds = currentProject.project_data_summary || {};
    const sdoc = pds.summary_document || {};
    const pkg = currentProject.architect_action_package || sdoc.architect_action_package || {};
    const pkgSummary = pkg.executive_decision_summary || {};
    const infoGaps = pkg.information_gaps || pkg.missing_information_requests || [];
    const pkgItems = pkg.action_items || [];

    decisionsModalTitle.textContent = `חבילת תיקונים לאדריכל ומעקב החלטות — ${currentProject.project_name}`;

    const reqTypeLabels = {
      ALL: 'הכל',
      FIX_MEASURED_DEVIATION: '🔴 תיקון חריגה מדודה',
      EVALUATE_ALTERNATIVE: '💡 בחינת חלופה תכנונית',
      COMPLETE_MISSING_INFO: '❓ השלמת מידע חסר',
      CONSULTANT_COORDINATION: '🤝 תיאום יועצים',
      CONFIRM_PRESERVATION_CONSTRAINT: '🛡️ אישור אילוץ לשימור'
    };

    // Build unified items list from architect_action_package arrays + any user-decided notes
    const unifiedItems = [];
    const seenIds = new Set();

    function pushUnifiedItem(rawItem, defaultReqType, defaultOwner) {
      const matchNote = notes.find((n) => n.id === rawItem.note_id || (n.evidence_record && n.evidence_record.immutable_id === rawItem.immutable_id));
      const noteId = matchNote ? matchNote.id : (rawItem.note_id || rawItem.immutable_id);
      if (noteId && seenIds.has(noteId)) return;
      if (noteId) seenIds.add(noteId);
      const userDec = matchNote ? getNoteDecision(matchNote.id) : null;
      const rType = rawItem.request_type || defaultReqType;
      unifiedItems.push({
        immutable_id: rawItem.immutable_id || (matchNote && matchNote.evidence_record && matchNote.evidence_record.immutable_id) || `AK-${noteId || unifiedItems.length + 1}`,
        note_id: matchNote ? matchNote.id : null,
        pin_num: matchNote ? matchNote.pin_num : (rawItem.pin_num || '—'),
        request_type: rType,
        request_type_he: rawItem.request_type_he || reqTypeLabels[rType] || 'בחינת חלופה',
        location_he: rawItem.location_he || rawItem.location || rawItem.where_on_plan || (matchNote ? `${matchNote.typology} · ${matchNote.room_name}` : ''),
        finding_he: rawItem.finding_he || rawItem.preserved_quality || rawItem.missing_item || (matchNote ? `${matchNote.title} (${matchNote.measured})` : ''),
        requested_action_he: rawItem.requested_action_he || rawItem.action_required || rawItem.proposed_change || rawItem.how_to_execute || rawItem.constraint_rule || (matchNote ? (matchNote.how_to_execute || matchNote.recommendation) : ''),
        preservation_constraints: rawItem.preservation_constraints || (rType === 'CONFIRM_PRESERVATION_CONSTRAINT'
          ? ['אין לפגוע ביתרון תכנוני זה בחלופות עתידיות ללא הצגת הפשרה']
          : ['אי־פגיעה בחניות ורדיוסי תמרון', 'שמירת רוחב פרוזדור חוקי ושטח דירה']),
        owner_he: rawItem.owner_he || defaultOwner || 'אדריכל הפרויקט',
        workflow_state: userDec || rawItem.workflow_state || 'OPEN_FOR_REVIEW',
        plan_version: pkg.plan_version || 'v2026.10'
      });
    }

    pkgItems.forEach((it) => pushUnifiedItem(it, 'EVALUATE_ALTERNATIVE', 'אדריכל הפרויקט'));
    (pkg.mandatory_statutory_fixes || []).forEach((it) => pushUnifiedItem(it, 'FIX_MEASURED_DEVIATION', 'אדריכל הפרויקט (רישוי)'));
    (pkg.quality_and_usability_improvements || []).forEach((it) => pushUnifiedItem(it, 'EVALUATE_ALTERNATIVE', 'אדריכל הפרויקט'));
    (pkg.value_engineering_alternatives || []).forEach((it) => pushUnifiedItem(it, 'CONSULTANT_COORDINATION', 'אדריכל + קונסטרוקטור / יועץ תנועה'));
    (pkg.preservation_constraints || []).forEach((it) => pushUnifiedItem(it, 'CONFIRM_PRESERVATION_CONSTRAINT', 'צוות תכנון ובקרה'));
    (pkg.missing_information_requests || []).forEach((it) => pushUnifiedItem(it, 'COMPLETE_MISSING_INFO', 'אדריכל / מנהל פרויקט'));

    notes.forEach((n) => {
      if (seenIds.has(n.id)) return;
      const userDec = getNoteDecision(n.id);
      if (userDec || n.status === 'FAIL' || isNoteUnknownStatus(n)) {
        const reqType = n.status === 'FAIL'
          ? 'FIX_MEASURED_DEVIATION'
          : (isNoteUnknownStatus(n) ? 'COMPLETE_MISSING_INFO' : (n.is_value_eng ? 'CONSULTANT_COORDINATION' : 'EVALUATE_ALTERNATIVE'));
        pushUnifiedItem({ note_id: n.id }, reqType, n.is_value_eng ? 'אדריכל + קונסטרוקטור' : 'אדריכל הפרויקט');
      }
    });

    const filteredItems = currentArchPkgFilter === 'ALL'
      ? unifiedItems
      : unifiedItems.filter((it) => it.request_type === currentArchPkgFilter);

    const filterPillsHtml = Object.keys(reqTypeLabels).map((rKey) => {
      const count = rKey === 'ALL' ? unifiedItems.length : unifiedItems.filter((i) => i.request_type === rKey).length;
      return `<button type="button" class="subfilter-pill arch-pkg-filter-btn ${currentArchPkgFilter === rKey ? 'active' : ''}" data-req-type="${rKey}">${reqTypeLabels[rKey]} <span>(${count})</span></button>`;
    }).join('');

    const infoGapsHtml = infoGaps.length > 0
      ? `
        <div class="modal-section-card" style="background:#fffbeb;border-color:#fde68a;">
          <h3 style="color:#92400e;">❓ פערי מידע להשלמה לפני אישור סופי (${infoGaps.length})</h3>
          <ul style="margin:6px 0 0 0;padding-right:18px;font-size:12px;color:#78350f;line-height:1.5;">
            ${infoGaps.map((g) => `<li><strong>${g.category_he || g.field || 'נתון חסר'}:</strong> ${g.description_he || g.impact_he || ''}</li>`).join('')}
          </ul>
        </div>
      `
      : '';

    const rowsHtml = filteredItems.map((it) => {
      const wfCode = it.workflow_state || 'OPEN_FOR_REVIEW';
      const dMeta = DECISION_LABELS[wfCode] || { label: 'לבדיקה', cls: 'dec-todo' };
      const constraintsHtml = (it.preservation_constraints || []).map((c) => `<span style="display:inline-block;background:#f1f5f9;border:1px solid #cbd5e1;border-radius:4px;padding:1px 5px;font-size:10px;margin:1px;">🛡️ ${c}</span>`).join(' ');
      return `
        <tr>
          <td>
            <div style="font-family:monospace;font-size:10.5px;font-weight:700;color:#1e293b;">${it.immutable_id}</div>
            <div style="font-size:10px;color:#64748b;">סיכה #${it.pin_num} · ${it.plan_version}</div>
          </td>
          <td><span style="font-size:11px;font-weight:700;">${it.request_type_he}</span></td>
          <td><strong>${it.location_he}</strong></td>
          <td>${it.finding_he}</td>
          <td>${it.requested_action_he}</td>
          <td>${constraintsHtml}</td>
          <td>${it.owner_he}</td>
          <td>
            <span class="note-dec-badge ${dMeta.cls}" style="display:inline-block;margin-bottom:4px;">${dMeta.label}</span>
            ${it.note_id ? `
              <select class="arch-pkg-wf-select" data-note-id="${it.note_id}" style="display:block;width:100%;font-size:11px;padding:2px 4px;border-radius:4px;border:1px solid #cbd5e1;">
                <option value="OPEN_FOR_REVIEW" ${wfCode === 'OPEN_FOR_REVIEW' ? 'selected' : ''}>לבדיקה</option>
                <option value="DECIDED_TO_FIX" ${wfCode === 'DECIDED_TO_FIX' || wfCode === 'TODO' ? 'selected' : ''}>הוחלט לתקן</option>
                <option value="FIXED_PENDING_VERIFICATION" ${wfCode === 'FIXED_PENDING_VERIFICATION' || wfCode === 'REVIEWED' ? 'selected' : ''}>תוקן — ממתין לאימות</option>
                <option value="VERIFIED_CLOSED" ${wfCode === 'VERIFIED_CLOSED' || wfCode === 'APPROVED' ? 'selected' : ''}>נסגר (מאומת)</option>
                <option value="REJECTED" ${wfCode === 'REJECTED' ? 'selected' : ''}>נדחה</option>
              </select>
            ` : ''}
          </td>
          <td>
            ${it.note_id ? `<button type="button" class="btn-locate-on-plan btn-arch-pkg-jump" data-note-id="${it.note_id}">📍 פתח במבט הנכון</button>` : '—'}
          </td>
        </tr>
      `;
    }).join('');

    decisionsModalBody.innerHTML = `
      <div class="modal-kpi-strip">
        <div class="modal-kpi-box">
          <span class="modal-kpi-lbl">פריטי עבודה בחבילה</span>
          <strong class="modal-kpi-val">${unifiedItems.length}</strong>
          <span class="modal-kpi-sub">גרסת תוכנית: ${pkg.plan_version || 'v2026.10'}</span>
        </div>
        <div class="modal-kpi-box">
          <span class="modal-kpi-lbl">ממצאים בעדיפות גבוהה</span>
          <strong class="modal-kpi-val" style="color:#dc2626;">${(pkgSummary.high_priority_findings || []).length || unifiedItems.filter((i) => i.request_type === 'FIX_MEASURED_DEVIATION').length}</strong>
          <span class="modal-kpi-sub">חריגות מדודות ואילוצי רישוי</span>
        </div>
        <div class="modal-kpi-box">
          <span class="modal-kpi-lbl">חלופות והחלטות יזם/אדריכל</span>
          <strong class="modal-kpi-val" style="color:#0284c7;">${unifiedItems.filter((i) => i.request_type === 'EVALUATE_ALTERNATIVE' || i.request_type === 'CONSULTANT_COORDINATION').length}</strong>
          <span class="modal-kpi-sub">נדרש אישור תכנוני לפני זקיפת חיסכון</span>
        </div>
        <div class="modal-kpi-box highlight">
          <span class="modal-kpi-lbl">כלל סגירה הנדסי (E42)</span>
          <strong class="modal-kpi-val" style="font-size:13px;">אימות בסבב הבא</strong>
          <span class="modal-kpi-sub">ממצא שתוקן עובר ל״ממתין לאימות״ עד לבדיקה חוזרת</span>
        </div>
      </div>

      ${infoGapsHtml}

      <div class="modal-section-card">
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:10px;">
          <h3 style="margin:0;">טבלת משימות ומעקב ביצוע לאדריכל וליועצים (${filteredItems.length} פריטים מוצגים)</h3>
          <div style="display:flex;flex-wrap:wrap;gap:4px;">${filterPillsHtml}</div>
        </div>
        <table class="modal-data-table">
          <thead>
            <tr>
              <th>מזהה קבוע (ID)</th>
              <th>סוג בקשה</th>
              <th>קומה ומיקום</th>
              <th>ממצא ומידה</th>
              <th>פעולה מבוקשת</th>
              <th>מה לבדוק שוב (אילוצים לשימור)</th>
              <th>אחראי</th>
              <th>סטטוס סבב (E42)</th>
              <th>ניווט לתוכנית</th>
            </tr>
          </thead>
          <tbody>${rowsHtml}</tbody>
        </table>
      </div>
    `;

    decisionsModalBody.querySelectorAll('.arch-pkg-filter-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        currentArchPkgFilter = btn.dataset.reqType || 'ALL';
        openDecisionsExportModal();
      });
    });

    decisionsModalBody.querySelectorAll('.arch-pkg-wf-select').forEach((sel) => {
      sel.addEventListener('change', () => {
        const nId = sel.getAttribute('data-note-id');
        const val = sel.value;
        if (nId) {
          setNoteDecision(nId, val);
          if (currentProject) {
            updateSystemFilterCounts(currentProject);
            renderDocumentSections(currentProject);
          }
          openDecisionsExportModal();
        }
      });
    });

    decisionsModalBody.querySelectorAll('.btn-arch-pkg-jump').forEach((btn) => {
      btn.addEventListener('click', () => {
        const nId = btn.getAttribute('data-note-id');
        decisionsExportModal.classList.add('hidden');
        if (nId) {
          highlightNote(nId, { scrollDoc: true, switchSheet: true, openDock: true, zoomTo: true });
        }
      });
    });

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
      if (
        isFocusMode ||
        document.body.classList.contains('top-bar-collapsed') ||
        (splitWorkspaceEl && splitWorkspaceEl.classList.contains('doc-collapsed')) ||
        isPlanToolbarCollapsed
      ) {
        restoreAllBarsAndPanels();
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
      syncCollapsedBarsRestoreUi();
    });
  }

  if (btnExpandDocPanel && splitWorkspaceEl) {
    btnExpandDocPanel.addEventListener('click', () => {
      splitWorkspaceEl.classList.remove('doc-collapsed');
      syncCollapsedBarsRestoreUi();
    });
  }

  if (btnRestoreDocPanelFloating && splitWorkspaceEl) {
    btnRestoreDocPanelFloating.addEventListener('click', () => {
      splitWorkspaceEl.classList.remove('doc-collapsed');
      syncCollapsedBarsRestoreUi();
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
    const targetSrc = `${baseUrl}${baseUrl.includes('?') ? '&' : '?'}embed=1&v=7.5`;
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
      let updatedPayload = null;
      try {
        const resp = await fetch('/api/check_3d_models', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ project: pid, force: Boolean(forceReaudit) }),
        });
        if (resp.ok) {
          const resData = await resp.json();
          updatedPayload = resData.payload || null;
        }
      } catch (apiErr) {
        console.warn('check_3d_models API not available, using static fallback:', apiErr);
      }
      if (!updatedPayload && pid) {
        const staticResp = await fetch(`/api/${pid}.json?v=7.5&t=${Date.now()}`, { cache: 'no-store' });
        if (staticResp.ok) {
          updatedPayload = await staticResp.json();
        }
      }
      updatedPayload = updatedPayload || currentProject;
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
