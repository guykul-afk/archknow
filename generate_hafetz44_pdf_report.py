# -*- coding: utf-8 -*-
"""
Generator script for Chafetz Chaim 44 Architectural Quality Audit PDF Document.
Converts the in-depth architectural audit (v2.1 including EN 17037, BR 209,
CIBSE AM10/TM59, WELL v2, Boverket Möblerbarhet, UK HQI, DIN 18040-2, EU Level(s) 2.3,
CBE POE, NDSS, ADG, NKBA & Space Syntax) into a print-ready A4 PDF report.
"""

import os
import shutil
import subprocess

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
GDRIVE_DIR = r"G:\תיקיות אחסון שיתופי\פרויקטים שוטפים\פרויקטים בביצוע\חפץ חיים 44\מודל"

HTML_PATH = os.path.join(OUTPUT_DIR, "hafetz44_architectural_quality_analysis.html")
PDF_FILENAME = "hafetz44_architectural_quality_analysis.pdf"
PRIMARY_PDF_PATH = os.path.join(OUTPUT_DIR, PDF_FILENAME)

HTML_CONTENT = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>דוח בקרת איכות תכנון ואדריכלות — חפץ חיים 44, פתח תקווה</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700;800&family=Heebo:wght@300;400;500;700;800;900&family=Rubik:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    @page {
      size: A4 portrait;
      margin: 13mm 12mm 13mm 12mm;
      @bottom-center {
        content: "עמוד " counter(page);
        font-family: 'Heebo', sans-serif;
        font-size: 8pt;
        color: #64748b;
      }
    }

    * {
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }

    body {
      font-family: 'Assistant', 'Heebo', 'Segoe UI', Arial, sans-serif;
      font-size: 9.2pt;
      line-height: 1.44;
      color: #0f172a;
      background-color: #ffffff;
      margin: 0;
      padding: 0;
    }

    h1, h2, h3, h4 {
      font-family: 'Heebo', sans-serif;
      margin-top: 0;
      color: #0f172a;
      letter-spacing: -0.2px;
    }

    h1 {
      font-size: 20pt;
      font-weight: 900;
      line-height: 1.15;
      color: #1e3a8a;
      margin-bottom: 4px;
    }

    h2 {
      font-size: 12.5pt;
      font-weight: 800;
      border-bottom: 2px solid #2563eb;
      padding-bottom: 4px;
      margin-top: 16px;
      margin-bottom: 9px;
      color: #1e293b;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    h3 {
      font-size: 10pt;
      font-weight: 700;
      margin-top: 10px;
      margin-bottom: 5px;
      color: #334155;
    }

    p {
      margin: 0 0 6px 0;
    }

    ul {
      margin: 4px 0 8px 0;
      padding-right: 18px;
    }

    li {
      margin-bottom: 3px;
    }

    .header-banner {
      background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 60%, #0284c7 100%);
      color: #ffffff;
      padding: 16px 20px;
      border-radius: 8px;
      margin-bottom: 14px;
      position: relative;
    }

    .header-banner h1 {
      color: #ffffff;
      margin: 0 0 4px 0;
      font-size: 20pt;
    }

    .header-subtitle {
      font-size: 10.5pt;
      font-weight: 600;
      color: #93c5fd;
      margin-bottom: 10px;
    }

    .header-meta {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      font-size: 8.2pt;
      background: rgba(15, 23, 42, 0.45);
      padding: 8px 12px;
      border-radius: 6px;
      border: 1px solid rgba(255, 255, 255, 0.18);
    }

    .header-meta-item strong {
      color: #fde047;
      display: block;
      font-size: 7.8pt;
      text-transform: uppercase;
    }

    .scorecard-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      margin-bottom: 12px;
    }

    .score-card {
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 9px 10px;
      text-align: center;
    }

    .score-card.primary {
      background: #eff6ff;
      border-color: #3b82f6;
    }

    .score-title {
      font-size: 8pt;
      font-weight: 700;
      color: #64748b;
      margin-bottom: 2px;
    }

    .score-val {
      font-family: 'Heebo', sans-serif;
      font-size: 21pt;
      font-weight: 900;
      color: #1e3a8a;
      line-height: 1;
    }

    .score-sub {
      font-size: 7.8pt;
      color: #059669;
      font-weight: 700;
      margin-top: 3px;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 8.2pt;
      margin-bottom: 10px;
      page-break-inside: avoid;
    }

    th, td {
      padding: 5px 7px;
      text-align: right;
      border-bottom: 1px solid #e2e8f0;
      vertical-align: middle;
    }

    th {
      background-color: #f1f5f9;
      color: #1e293b;
      font-weight: 700;
      font-family: 'Heebo', sans-serif;
      border-top: 1px solid #cbd5e1;
      border-bottom: 2px solid #94a3b8;
    }

    tr:nth-child(even) td {
      background-color: #f8fafc;
    }

    .badge {
      display: inline-block;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 7.2pt;
      font-weight: 800;
      font-family: 'Heebo', sans-serif;
      text-align: center;
    }

    .badge-pass {
      background-color: #dcfce7;
      color: #15803d;
      border: 1px solid #86efac;
    }

    .badge-warn {
      background-color: #fef3c7;
      color: #b45309;
      border: 1px solid #fde68a;
    }

    .badge-fail {
      background-color: #fee2e2;
      color: #b91c1c;
      border: 1px solid #fca5a5;
    }

    .badge-info {
      background-color: #e0f2fe;
      color: #0369a1;
      border: 1px solid #bae6fd;
    }

    .alert-box {
      border-radius: 6px;
      padding: 8px 11px;
      margin: 8px 0;
      font-size: 8.4pt;
      line-height: 1.38;
      page-break-inside: avoid;
    }

    .alert-warning {
      background-color: #fffbeb;
      border-right: 4px solid #f59e0b;
      color: #92400e;
    }

    .alert-info {
      background-color: #eff6ff;
      border-right: 4px solid #3b82f6;
      color: #1e40af;
    }

    .alert-success {
      background-color: #f0fdf4;
      border-right: 4px solid #10b981;
      color: #065f46;
    }

    .section-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 9px 12px;
      margin-bottom: 10px;
      page-break-inside: avoid;
    }

    .recommendations-list {
      counter-reset: rec-counter;
      list-style: none;
      padding: 0;
      margin: 6px 0;
    }

    .recommendations-list li {
      position: relative;
      padding-right: 30px;
      margin-bottom: 8px;
      page-break-inside: avoid;
    }

    .recommendations-list li::before {
      counter-increment: rec-counter;
      content: counter(rec-counter);
      position: absolute;
      right: 0;
      top: 1px;
      width: 21px;
      height: 21px;
      background: #1e3a8a;
      color: #fde047;
      font-weight: 800;
      font-size: 8.5pt;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Heebo', sans-serif;
    }

    .rec-title {
      font-weight: 800;
      color: #1e293b;
      margin-bottom: 2px;
      font-size: 9pt;
    }

    .rec-desc {
      color: #475569;
      font-size: 8.2pt;
      line-height: 1.34;
    }

    .footer-bar {
      margin-top: 14px;
      border-top: 1px solid #cbd5e1;
      padding-top: 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 7.5pt;
      color: #64748b;
    }

    .page-break {
      page-break-after: always;
    }
  </style>
</head>
<body>

  <!-- HEADER BANNER -->
  <div class="header-banner">
    <h1>דוח בקרת איכות תכנון ואדריכלות מלא (v2.1)</h1>
    <div class="header-subtitle">פרויקט חפץ חיים 44, פתח תקווה — ניתוח הנדסי, תאורה, אוורור ושימושיות (Zero-Trust White-Box Audit)</div>
    <div class="header-meta">
      <div class="header-meta-item">
        <strong>יזם וקבלן מבצע:</strong>
        יצחק קולסקי חברה לבניה והשקעות בע"מ
      </div>
      <div class="header-meta-item">
        <strong>אדריכלות:</strong>
        א.ב. דרגן אדריכלים / סטודיו אורכה
      </div>
      <div class="header-meta-item">
        <strong>היקף וגוש/חלקה:</strong>
        17 יח"ד · 9 קומות + מרתף · גוש 6396 חלקה 85
      </div>
      <div class="header-meta-item">
        <strong>מנוע בקרה ותקינה:</strong>
        archknow v2.1 (403 קובצי חוק ותקינה)
      </div>
    </div>
  </div>

  <!-- EXECUTIVE SCORECARDS -->
  <div class="scorecard-grid">
    <div class="score-card primary">
      <div class="score-title">ציון איכות אדריכלית משוקלל</div>
      <div class="score-val">89.8<span style="font-size:11pt;color:#64748b;">/100</span></div>
      <div class="score-sub">דירוג A · +11.8 נק' מפינס 48</div>
    </div>
    <div class="score-card">
      <div class="score-title">בדיקות מנוע דטרמיניסטי</div>
      <div class="score-val" style="color:#059669;">270<span style="font-size:11pt;color:#64748b;">/328</span></div>
      <div class="score-sub">82.3% PASS · 0 כשלים חוקיים (FAIL)</div>
    </div>
    <div class="score-card">
      <div class="score-title">כיווני אוויר ואור יום</div>
      <div class="score-val" style="color:#0284c7;">3–4</div>
      <div class="score-sub">100% מהדירות תלת/ארבע-כיווניות!</div>
    </div>
    <div class="score-card">
      <div class="score-title">צפיפות קומתית וגובה נטו</div>
      <div class="score-val" style="color:#7c3aed;">2.87m</div>
      <div class="score-sub">2 דירות בקומה בלבד (קומות 1–8)</div>
    </div>
  </div>

  <!-- TABLE 1: WEIGHTED QUALITY MATRIX -->
  <h2>📊 1. מטריצת ציוני איכות והשוואה לפרויקטי הייחוס (פינס 48 וקק״ל 10)</h2>
  <table>
    <thead>
      <tr>
        <th style="width: 28%;">קטגוריית הערכה ותקינה</th>
        <th style="width: 7%; text-align: center;">משקל</th>
        <th style="width: 11%; text-align: center;">חפץ חיים 44</th>
        <th style="width: 10%; text-align: center;">מול פינס 48</th>
        <th style="width: 10%; text-align: center;">מול קק״ל 10</th>
        <th style="width: 9%; text-align: center;">סטטוס</th>
        <th style="width: 25%;">ממצא מרכזי מבוסס BIM</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>1. חקיקה ותקנות הבנייה (ישראל 2026)</strong></td>
        <td style="text-align: center;">20%</td>
        <td style="text-align: center; font-weight: 800; color: #1e3a8a;">97 / 100</td>
        <td style="text-align: center; color: #15803d; font-weight: 700;">+3 (94)</td>
        <td style="text-align: center; color: #15803d; font-weight: 700;">+1 (96)</td>
        <td style="text-align: center;"><span class="badge badge-pass">PASS</span></td>
        <td>0 כשלי סף; גובה נטו 2.87 מ'; ממ"דים ענקיים בקומות 1–8 (11.8–13.4 מ"ר).</td>
      </tr>
      <tr>
        <td><strong>2. אור יום, מבט ואוורור (EN 17037 / CIBSE / BR 209)</strong></td>
        <td style="text-align: center;">18%</td>
        <td style="text-align: center; font-weight: 800; color: #1e3a8a;">95 / 100</td>
        <td style="text-align: center; color: #15803d; font-weight: 700;">+24 (71)</td>
        <td style="text-align: center; color: #15803d; font-weight: 700;">+8 (87)</td>
        <td style="text-align: center;"><span class="badge badge-pass">מצטיין</span></td>
        <td>3–4 כיווני אוויר לכל דירה; שצ"פ מערבי 13.95 מ'; מסלול מפולש 9.4 מ' ≤ 5×H.</td>
      </tr>
      <tr>
        <td><strong>3. מדדי רווחה ופרופורציות (NDSS / ADG / UK HQI)</strong></td>
        <td style="text-align: center;">16%</td>
        <td style="text-align: center; font-weight: 800; color: #1e3a8a;">90 / 100</td>
        <td style="text-align: center; color: #15803d; font-weight: 700;">+22 (68)</td>
        <td style="text-align: center; color: #15803d; font-weight: 700;">+6 (84)</td>
        <td style="text-align: center;"><span class="badge badge-pass">מצטיין</span></td>
        <td>עודף של +16 עד +43 מ"ר מעל NDSS; מרפסות בעומק 2.00 מ' (19 מ"ר); איזון HQI מלא.</td>
      </tr>
      <tr>
        <td><strong>4. שימושיות, ריהוט וגמישות (Boverket / DIN / Level(s))</strong></td>
        <td style="text-align: center;">14%</td>
        <td style="text-align: center; font-weight: 800; color: #1e3a8a;">84 / 100</td>
        <td style="text-align: center; color: #15803d; font-weight: 700;">+14 (70)</td>
        <td style="text-align: center; color: #15803d; font-weight: 700;">+4 (80)</td>
        <td style="text-align: center;"><span class="badge badge-info">טוב מאוד</span></td>
        <td>69%–74% מחיצות פריקות (EU Level(s) ≥ 60%); חדר ארונות בכל יחידת הורים; מעבר צד מיטה 52 ס"מ.</td>
      </tr>
      <tr>
        <td><strong>5. ארגונומיה, מטבחים ורחצה (NKBA / Neufert / POE)</strong></td>
        <td style="text-align: center;">12%</td>
        <td style="text-align: center; font-weight: 800; color: #1e3a8a;">86 / 100</td>
        <td style="text-align: center; color: #15803d; font-weight: 700;">+12 (74)</td>
        <td style="text-align: center; color: #b45309; font-weight: 700;">-2 (88)</td>
        <td style="text-align: center;"><span class="badge badge-info">טוב מאוד</span></td>
        <td>מעבר מטבח 142–164 ס"מ בקומות 1–8 (96 ס"מ בפנטהאוז); חסר שירותי אורחים בטיפוס W.</td>
      </tr>
      <tr>
        <td><strong>6. תחביר המרחב ופרטיות (Space Syntax / APL / SAGA)</strong></td>
        <td style="text-align: center;">10%</td>
        <td style="text-align: center; font-weight: 800; color: #1e3a8a;">85 / 100</td>
        <td style="text-align: center; color: #15803d; font-weight: 700;">+12 (73)</td>
        <td style="text-align: center; color: #15803d; font-weight: 700;">+3 (82)</td>
        <td style="text-align: center;"><span class="badge badge-info">טוב מאוד</span></td>
        <td>אפס קירות משותפים בין סלונים/חדרי שינה בקומה; יחס מסדרון יעיל במיוחד (6.0%–6.9%).</td>
      </tr>
      <tr>
        <td><strong>7. תשתית בניין, חניה ונגישות עירונית (GIS / TOD)</strong></td>
        <td style="text-align: center;">10%</td>
        <td style="text-align: center; font-weight: 800; color: #1e3a8a;">83 / 100</td>
        <td style="text-align: center; color: #15803d; font-weight: 700;">+7 (76)</td>
        <td style="text-align: center; color: #b45309; font-weight: 700;">-11 (94)</td>
        <td style="text-align: center;"><span class="badge badge-info">טוב מאוד</span></td>
        <td>19 חניות רגילות (1.12 לדירה, ללא מכפילים); מעלית בודדת ל-17 יח"ד; ללא מחסנים במרתף.</td>
      </tr>
      <tr style="background-color: #eff6ff; font-weight: 800;">
        <td><strong>ציון איכות כולל (משוקלל)</strong></td>
        <td style="text-align: center;">100%</td>
        <td style="text-align: center; font-size: 10.5pt; color: #1e3a8a;">89.8 / 100</td>
        <td style="text-align: center; color: #15803d;">+11.8 נק'</td>
        <td style="text-align: center; color: #15803d;">+0.2 נק'</td>
        <td style="text-align: center;"><span class="badge badge-pass">דירוג A</span></td>
        <td><strong>פרויקט בוטיק מואר, מאוורר ומרווח באופן יוצא דופן (2 דירות בקומה).</strong></td>
      </tr>
    </tbody>
  </table>

  <!-- TABLE 2: APARTMENT ARCHETYPES -->
  <h2>🏢 2. סקירת טיפוסי הדירות בפרויקט (17 יח"ד — חילוץ 1:1 ממודל ה-BIM)</h2>
  <table>
    <thead>
      <tr>
        <th>טיפוס דירה</th>
        <th>קומות ומספרי דירות</th>
        <th style="text-align: center;">חדרים</th>
        <th style="text-align: center;">שטח פלדלת</th>
        <th style="text-align: center;">מרפסת שמש/גג</th>
        <th>כיווני אוויר מלאים</th>
        <th style="text-align: center;">גובה נטו</th>
        <th style="text-align: center;">בדיקות PASS / סה"כ</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>טיפוס W (מערבית)</strong></td>
        <td>קומות 1–8 (אי-זוגיות #1..#15 — 8 יח"ד)</td>
        <td style="text-align: center;">5</td>
        <td style="text-align: center; font-weight: 700;">124 מ"ר</td>
        <td style="text-align: center;">19 מ"ר (200×940)</td>
        <td>מערב (שצ"פ), צפון, דרום (3)</td>
        <td style="text-align: center; color: #15803d; font-weight: 700;">2.87 מ'</td>
        <td style="text-align: center; font-weight: 700;">87 / 108 (0 FAIL)</td>
      </tr>
      <tr>
        <td><strong>טיפוס E (מזרחית חזיתית)</strong></td>
        <td>קומות 1–8 (זוגיות #2..#16 — 8 יח"ד)</td>
        <td style="text-align: center;">4</td>
        <td style="text-align: center; font-weight: 700;">102 מ"ר</td>
        <td style="text-align: center;">19 מ"ר (200×940)</td>
        <td>מזרח (חזית), צפון, דרום (3)</td>
        <td style="text-align: center; color: #15803d; font-weight: 700;">2.87 מ'</td>
        <td style="text-align: center; font-weight: 700;">75 / 93 (0 FAIL)</td>
      </tr>
      <tr>
        <td><strong>פנטהאוז #17 (PH)</strong></td>
        <td>קומה 9 שלמה (דירה #17 — יח"ד 1)</td>
        <td style="text-align: center;">5–6</td>
        <td style="text-align: center; font-weight: 700;">168 מ"ר</td>
        <td style="text-align: center;">112 מ"ר (2 מרפסות גג)</td>
        <td>מזרח, מערב, צפון, דרום (4)</td>
        <td style="text-align: center; color: #15803d; font-weight: 700;">2.87 מ'</td>
        <td style="text-align: center; font-weight: 700;">108 / 127 (0 FAIL)</td>
      </tr>
    </tbody>
  </table>

  <div class="alert-box alert-warning">
    <strong>⚠️ 2 ממצאי ביקורת Zero-Trust במסמכי ה-CRM והרישוי של המודל:</strong><br>
    1. <strong>כפילות בשיוך חניה #10 ואי-שיוך חניות #17–#19 במרתף:</strong> בטבלת <code>CRM_DATA.units</code>, חניה #10 במרתף משויכת בו-זמנית גם לדירה #10 (קומה 5) וגם לפנטהאוז הדגל #17 (קומה 9, מחיר ₪6.45M), בעוד חניות #17, #18 ו-#19 במרתף אינן משויכות לאף דירה. יש לשייך לפנטהאוז #17 את צמד החניות #17 + #18 הצמודות ללובי המעלית.<br>
    2. <strong>אחידות גוש/חלקה:</strong> בכותרת ה-HTML ובתבנית הצעת המחיר מופיע <code>גוש 6373 חלקה 265</code>, בעוד בתוכנית המדידה ההנדסית ובגוף המודל מופיע <code>גוש 6396 חלקה 85 (מגרשים 85-1, 85-2, 85-3)</code>. יש לאחד את הרישום בכל מסמכי השיווק.
  </div>

  <div class="page-break"></div>

  <!-- SECTION 3: DAYLIGHT, VIEW OUT & VENTILATION (NEW STANDARDS) -->
  <h2>☀️ 3. תאורה טבעית, מבט החוצה, אוורור ואיכות סביבה (EN 17037 / CIBSE / BR 209 / WELL v2)</h2>
  <div class="section-card">
    <h3>3.1 אוורור מפולש תלת-כיווני (CIBSE AM10 & NSW ADG 4B)</h3>
    <ul>
      <li><strong>100% דירות מפולשות (3–4 כיווני אוויר):</strong> בזכות תצורת 2 דירות בקומה, כל דירה נהנית מחזית צפונית מלאה, חזית דרומית מלאה, וחזית ראשית מערבית (טיפוס W) או מזרחית (טיפוס E), והפנטהאוז מ-4 חזיתות.</li>
      <li><strong>עומק מסלול אוורור מפולש (דרישת CIBSE AM10: ≤ 5 × H = 14.35 מ'):</strong> המרחק מצפון לדרום הוא <strong>9.40 מ' (3.28×H)</strong> וממזרח למערב 10.90–12.18 מ' — <strong>PASS מצטיין</strong> בכל הדירות.</li>
      <li><strong>עומק חדרים באוורור חד-צדדי (דרישת CIBSE AM10: ≤ 2.0 × H = 5.74 מ'):</strong> כל חדרי השינה בפרויקט (עומק 3.35–4.68 מ') עומדים בתקרת העומק לאוורור אפקטיבי מפתח יחיד.</li>
    </ul>

    <h3>3.2 יחס זיגוג (WFR), קו שמיים (BRE BR 209) ואיכות מבט החוצה (EN 17037)</h3>
    <ul>
      <li><strong>סלון ופינת אוכל שטופי אור:</strong> בטיפוס W ובטיפוס E שטח הזיגוג בסלון הוא <strong>12.06 מ"ר</strong> (ויטרינה 3.00×2.50 מ' + שני חלונות דרומיים גבוהים 1.20×1.90 מ'), המעניקים יחס חלון/רצפה של <strong>42.7% בטיפוס W ו-52.9% בטיפוס E</strong> (מול 8% בחוק הישראלי ו-10% ב-ADG!).</li>
      <li><strong>פתיחות נופית מערבית מובטחת סטטוטורית (EN 17037 View Out — רמת High):</strong> הפקעת מגרש 85-3 ל<strong>שצ"פ מערבי ברוחב 13.95 מ'</strong> + קו בניין מערבי 6.05 מ' יוצרים מרחק מבט פתוח של 20–45 מ' אל צמחייה, קרקע ושמיים (3 שכבות נוף וזווית הסתרה של 14° בלבד ≤ 25° לפי BR 209).</li>
      <li><strong>נגישות לאור צירקדי (WELL v2 L01):</strong> מרחק כל נקודות הישיבה והשינה מחלון מבט הוא <strong>2.80 עד 4.20 מ'</strong> (100% בתוך הטווח האופטימלי של ≤ 4.50 מ').</li>
      <li><strong>הגנה תרמית בחזית המערבית (CIBSE TM59):</strong> ויטרינת הסלון המערבית מוגנת על ידי קירוי מרפסת שמש בעומק מלא של <strong>2.00 מ'</strong> לאורך 9.40 מ'.</li>
    </ul>
  </div>

  <!-- SECTION 4: ROOM DIMENSIONS, HQI & FURNISHABILITY -->
  <h2>🛋️ 4. פרופורציות, יכולת ריהוט (Möblerbarhet), נגישות וגמישות (HQI / Boverket / DIN / Level(s))</h2>
  <div class="section-card">
    <h3>4.1 איזון פרוגרמטי (UK HQI) ורוחב חדרים (NSW ADG)</h3>
    <ul>
      <li><strong>איזון HQI מושלם בין אזור היום לאזור הלילה:</strong> בטיפוס W (6 מיטות) החלל הציבורי המשולב הוא <strong>40.76 מ"ר</strong> (מול 29.0 מ"ר נדרש ב-HQI); בטיפוס E (5 מיטות) <strong>35.32 מ"ר</strong> (מול 27.0 מ"ר); ובפנטהאוז (8 מיטות) <strong>68.52 מ"ר</strong> (מול 33.0 מ"ר).</li>
      <li><strong>רוחב חדרי שינה מהנדיבים ביותר בישראל:</strong> הממ"ד המערבי (<strong>3.35×4.00 מ' = 13.40 מ"ר!</strong>), חדר ההורים המזרחי (<strong>3.00×4.22 מ'</strong>), סוויטת ההורים בפנטהאוז (<strong>3.35×4.23 מ'</strong>) ושני חדרי השינה בפנטהאוז (<strong>3.06×3.44 מ'</strong>) חוצים כולם את רף ה-<strong>3.00 מ'</strong> של תקן המצוינות האוסטרלי ADG 4D-3! חדר ההורים המערבי וחדר שינה 1 מערבי עומדים על <strong>2.99 מ'</strong> (1 ס"מ בלבד מרף ה-ADG).</li>
    </ul>

    <h3>4.2 בדיקת יכולת ריהוט (Boverket Möblerbarhet) ומרווחי גישה (DIN 18040-2)</h3>
    <ul>
      <li><strong>חדר ארונות נפרד בכל יחידת הורים:</strong> משחרר את חדר השינה של ההורים מארון בגדים ומספק 3.00–3.20 מ' ארונות תלייה וקיפול.</li>
      <li><strong>נקודת תורפה במרווח צידי המיטה בחדרי ההורים בקומות 1–8 (52–53 ס"מ):</strong> הצבת מיטה ברוחב 1.70 מ' ושתי שידות של 46 ס"מ על הקיר החיצוני (2.99–3.00 מ') משאירה מעבר של 52–53 ס"מ מכל צד (מול 80–90 ס"מ מומלץ ב-DIN 18040-2). סיבוב המיטה לקיר הדרומי הארוך (4.22–4.68 מ') או הקטנת השידות ל-35 ס"מ יפתרו זאת במלואו.</li>
      <li><strong>דלת מקלחת הורים בקומות 1–8 (160×160 ס"מ):</strong> מרווח צד הידית הוא 15 ס"מ בלבד והכנף נפתחת פנימה; מומלץ להחליפה ל<strong>דלת הזזה לכיס (Pocket Door)</strong>.</li>
      <li><strong>גמישות מחיצות פנים (EU Level(s) 2.3):</strong> <strong>69% עד 74% ממחיצות הפנים</strong> הן מחיצות לא-נושאות פריקות (מעל רף 60% של האיחוד האירופי), והממ"ד ממוקם בקצה המסדרון מבלי לקטוע את רצף חדרי השינה.</li>
    </ul>
  </div>

  <!-- SECTION 5: KITCHENS, BATHROOMS & ACOUSTICS -->
  <h2>🍳 5. ארגונומיית מטבחים, חדרי רחצה ובידוד אקוסטי (NKBA & CBE POE)</h2>
  <div class="section-card">
    <ul>
      <li><strong>מטבחי הקומות הטיפוסיות (טיפוס W ו-E — 12.54 מ"ר):</strong> מטבח ח' עם חצי-אי (Peninsula), חלון דרומי מעל הכיור, חזית משטחים של 7.28–7.52 מ', ו<strong>מעבר עבודה רחב של 164 ס"מ ב-W ו-142 ס"מ ב-E</strong> (עובר בהצטיינות את דרישת NKBA_K01 של 122 ס"מ לשני בשלנים).</li>
      <li><strong>צוואר בקבוק במטבח השף של הפנטהאוז (מעבר 96 ס"מ):</strong> במטבח הפנטהאוז (21.42 מ"ר), המרחק בין השיש הדרומי (<code>Y=3.38</code>) לאי המרכזי (<code>Y=2.42</code>) הוא <strong>96 ס"מ בלבד</strong>. הזזת האי ב-<strong>24 ס"מ צפונה</strong> תפתח מעבר תקני ונוח של <strong>120 ס"מ</strong>.</li>
      <li><strong>אוורור טבעי כפול במקלחות ההורים:</strong> לכל מקלחות ההורים בבניין יש 2 חלונות חיצוניים פינתיים (צפון + מערב/מזרח).</li>
      <li><strong>היעדר שירותי אורחים נפרדים בדירת 5 החדרים (טיפוס W, 124 מ"ר):</strong> בניגוד לפנטהאוז (שבו יש שירותי אורחים עם חלון), בדירת 5 החדרים יש 2 חדרי רחצה בלבד ללא תא שירותי אורחים שלישי.</li>
      <li><strong>אקוסטיקה (CBE POE & ת"י 1004):</strong> הפרדה מוחלטת בין דירות הקומה (אפס קירות משותפים בין חדרי מגורים/שינה!). בתוך הדירה, יש לבודד אקוסטית את הקיר המשותף בין <code>חדר שינה 2</code> (ב-W) ו<code>חדר שינה 1</code> (ב-E) לבין חדר הרחצה הכללי ומכונת הכביסה.</li>
    </ul>
  </div>

  <!-- SECTION 6: 8 GOLDEN RECOMMENDATIONS -->
  <h2>🎯 6. שמונה המלצות זהב אופרטיביות להשבחת הפרויקט</h2>
  <div class="section-card">
    <ol class="recommendations-list">
      <li>
        <div class="rec-title">תיקון שיוך חניות ה-CRM: הצמדת חניות #17 + #18 במרתף לפנטהאוז הדגל (#17)</div>
        <div class="rec-desc">ביטול הכפילות של חניה #10 (המשויכת לדירה #10) ושיוך החניות הפנויות #17 ו-#18 הצמודות ללובי המעלית במרתף אל פנטהאוז #17 (ושימוש בחניה #19 כפרמיית שדרוג לדירת 5 חדרים).</div>
      </li>
      <li>
        <div class="rec-title">הזזת האי במטבח פנטהאוז #17 ב-24 ס"מ צפונה (תקן NKBA_K01)</div>
        <div class="rec-desc">הגדלת מעבר העבודה בין השיש הדרומי לאי מ-96 ס"מ ל-120 ס"מ תקניים לשני בשלנים ופתיחה חופשית של מדיח הכלים מול האי, ללא כל עלות ביצוע.</div>
      </li>
      <li>
        <div class="rec-title">איחוד רישום גוש/חלקה בכל תוויות ה-UI והצעות המחיר (גוש 6396 חלקה 85)</div>
        <div class="rec-desc">החלפת הכיתוב השגוי 'גוש 6373 חלקה 265' בכותרת ה-HTML ובתבנית ה-PDF לנתון המדויק ממפת המדידה ('גוש 6396 חלקה 85, מגרש 85-2').</div>
      </li>
      <li>
        <div class="rec-title">דלת הזזה לכיס (Pocket Door) במקלחת הורים וסיבוב אופציונלי של מיטת ההורים (קומות 1–8)</div>
        <div class="rec-desc">החלפת דלת הציר של מקלחת ההורים (160×160 ס"מ) בדלת כיס תשחרר את מרחב הכניסה, והצגת וריאציית העמדת מיטה על הקיר הדרומי הארוך (4.22–4.68 מ') תגדיל את מעברי הצד מ-52 ס"מ ל-110 ס"מ.</div>
      </li>
      <li>
        <div class="rec-title">הכנת חלופת שינויי דיירים (Option B) לתוספת שירותי אורחים בדירת 5 החדרים (טיפוס W)</div>
        <div class="rec-desc">תכנון מראש של תא שירותי אורחים קומפקטי (90×140 ס"מ) על בסיס חלק ממסתור הכביסה הרחב (240×75 ס"מ) או מבואת המסדרון עבור רוכשי דירות 5 חדרים הדורשים אסלה שלישית.</div>
      </li>
      <li>
        <div class="rec-title">שדרוג אקוסטי לקיר חדר הרחצה הכללי ולפיר המעלית (CBE POE / ת"י 1004)</div>
        <div class="rec-desc">שימוש בצנרת דלוחין מושתקת (Silent-db20) ובמחיצה אקוסטית רב-שכבתית בין חדר הרחצה ומכונת הכביסה לבין חדר השינה הצמוד (bed2_w ו-bed1_e).</div>
      </li>
      <li>
        <div class="rec-title">הזזת פתח הדלת ב-5–8 ס"מ בחדר שינה 2 מערבי וחדר שינה 1 מזרחי (Boverket Möblerbarhet)</div>
        <div class="rec-desc">הגדלת היסט הדלת מהפינה מ-52–55 ס"מ ל-60 ס"מ מלאים כדי לאפשר הצבת ארון בגדים בעומק 60 ס"מ גם לאורך קיר הכניסה.</div>
      </li>
      <li>
        <div class="rec-title">הכנת משקוף סמוי מגלריית המסדרון אל חדר העבודה בפנטהאוז #17 (Space Syntax SS-5)</div>
        <div class="rec-desc">יאפשר לרוכשי הפנטהאוז לבחור בין סוויטת הורים כפולה (חדר שינה + לאונג'/עבודה פרטי) לבין הפרדת החדר לחדר שינה עצמאי חמישי עם כניסה ישירה מהמסדרון.</div>
      </li>
    </ol>
  </div>

  <!-- FOOTER -->
  <div class="footer-bar">
    <div><strong>archknow v2.1</strong> · מערכת ביקורת איכות אדריכלית, תאורה, אוורור, שימושיות ותקנים בינלאומיים</div>
    <div>פרויקט חפץ חיים 44, פתח תקווה · יצחק קולסקי חברה לבניה והשקעות בע"מ · אוקטובר 2026</div>
  </div>

</body>
</html>
"""

def generate_pdf():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print(f"Wrote HTML template to: {HTML_PATH}")

    browsers = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    ]
    browser_exe = next((b for b in browsers if os.path.exists(b)), None)
    if not browser_exe:
        raise RuntimeError("No headless browser found for PDF printing.")

    print(f"Using browser: {browser_exe}")
    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={PRIMARY_PDF_PATH}",
        "--no-pdf-header-footer",
        HTML_PATH
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Browser stderr: {res.stderr}")
        raise RuntimeError(f"Browser failed with return code {res.returncode}")

    if not os.path.exists(PRIMARY_PDF_PATH):
        raise RuntimeError("PDF was not created!")

    size_kb = os.path.getsize(PRIMARY_PDF_PATH) / 1024
    print(f"Successfully generated PDF: {PRIMARY_PDF_PATH} ({size_kb:.1f} KB)")

    if os.path.exists(GDRIVE_DIR):
        gdrive_pdf = os.path.join(GDRIVE_DIR, PDF_FILENAME)
        gdrive_html = os.path.join(GDRIVE_DIR, "hafetz44_architectural_quality_analysis.html")
        try:
            shutil.copy2(PRIMARY_PDF_PATH, gdrive_pdf)
            shutil.copy2(HTML_PATH, gdrive_html)
            print(f"Copied PDF & HTML to GDrive project folder: {gdrive_pdf}")
        except Exception as e:
            print(f"Notice: GDrive copy skipped ({e})")

if __name__ == "__main__":
    generate_pdf()
