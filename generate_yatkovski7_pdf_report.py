# -*- coding: utf-8 -*-
"""
Generator script for Yatkovski 7 Architectural Quality Audit PDF Document.
"""

import os
import shutil
import subprocess

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
GDRIVE_DIR = r"G:\תיקיות אחסון שיתופי\פרויקטים שוטפים\פרויקטים בביצוע\יטקובסקי 7\מודל"

HTML_PATH = os.path.join(OUTPUT_DIR, "yatkovski7_architectural_quality_analysis.html")
PDF_FILENAME = "yatkovski7_architectural_quality_analysis.pdf"
PRIMARY_PDF_PATH = os.path.join(OUTPUT_DIR, PDF_FILENAME)

HTML_CONTENT = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>דוח בקרת איכות תכנון ואדריכלות — יטקובסקי אחים 7 (7א), פתח תקווה</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700;800&family=Heebo:wght@300;400;500;700;800;900&display=swap" rel="stylesheet">
  <style>
    @page {
      size: A4 portrait;
      margin: 13mm 12mm 13mm 12mm;
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
    h1, h2, h3 {
      font-family: 'Heebo', sans-serif;
      margin-top: 0;
      color: #0f172a;
    }
    h2 {
      font-size: 12pt;
      font-weight: 800;
      border-bottom: 2px solid #2563eb;
      padding-bottom: 4px;
      margin-top: 14px;
      margin-bottom: 8px;
      color: #1e293b;
    }
    .header-banner {
      background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 60%, #0284c7 100%);
      color: #ffffff;
      padding: 16px 20px;
      border-radius: 8px;
      margin-bottom: 14px;
    }
    .header-banner h1 {
      color: #ffffff;
      margin: 0 0 4px 0;
      font-size: 19pt;
      font-weight: 900;
    }
    .header-subtitle {
      font-size: 10.2pt;
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
      font-size: 20pt;
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
      font-size: 8.1pt;
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
    }
    .badge-pass { background-color: #dcfce7; color: #15803d; border: 1px solid #86efac; }
    .badge-warn { background-color: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
    .badge-info { background-color: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }
    .section-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 9px 12px;
      margin-bottom: 10px;
      page-break-inside: avoid;
    }
    .alert-box {
      border-radius: 6px;
      padding: 8px 11px;
      margin: 8px 0;
      font-size: 8.4pt;
      background-color: #f0fdf4;
      border-right: 4px solid #10b981;
      color: #065f46;
    }
    .recommendations-list {
      counter-reset: rec-counter;
      list-style: none;
      padding: 0;
      margin: 6px 0;
    }
    .recommendations-list li {
      position: relative;
      padding-right: 28px;
      margin-bottom: 7px;
    }
    .recommendations-list li::before {
      counter-increment: rec-counter;
      content: counter(rec-counter);
      position: absolute;
      right: 0;
      top: 1px;
      width: 20px;
      height: 20px;
      background: #1e3a8a;
      color: #fde047;
      font-weight: 800;
      font-size: 8pt;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .rec-title { font-weight: 800; color: #1e293b; font-size: 8.8pt; }
    .rec-desc { color: #475569; font-size: 8pt; }
    .footer-bar {
      margin-top: 12px;
      border-top: 1px solid #cbd5e1;
      padding-top: 6px;
      display: flex;
      justify-content: space-between;
      font-size: 7.5pt;
      color: #64748b;
    }
  </style>
</head>
<body>

  <div class="header-banner">
    <h1>דוח בקרת איכות תכנון ואדריכלות מלא (v2.1)</h1>
    <div class="header-subtitle">פרויקט יטקובסקי אחים 7 (7א), פתח תקווה — ניתוח הנדסי, תאורה, אוורור ושימושיות (Zero-Trust White-Box Audit)</div>
    <div class="header-meta">
      <div class="header-meta-item">
        <strong>יזם וקבלן מבצע:</strong>
        יצחק קולסקי חברה לבניה והשקעות בע"מ (52%)
      </div>
      <div class="header-meta-item">
        <strong>אדריכלות:</strong>
        א.ב. דרגן אדריכלים (רמי דרגן)
      </div>
      <div class="header-meta-item">
        <strong>היקף וגוש/חלקה:</strong>
        11 יח"ד · 7 קומות + מרתף · גוש 6385 חלקה 136
      </div>
      <div class="header-meta-item">
        <strong>מנוע בקרה ותקינה:</strong>
        archknow v2.1 (391 בדיקות דטרמיניסטיות)
      </div>
    </div>
  </div>

  <div class="scorecard-grid">
    <div class="score-card primary">
      <div class="score-title">ציון איכות אדריכלית משוקלל</div>
      <div class="score-val">91.4<span style="font-size:11pt;color:#64748b;">/100</span></div>
      <div class="score-sub">דירוג A · בוטיק מצטיין</div>
    </div>
    <div class="score-card">
      <div class="score-title">בדיקות מנוע דטרמיניסטי</div>
      <div class="score-val" style="color:#059669;">351<span style="font-size:11pt;color:#64748b;">/391</span></div>
      <div class="score-sub">89.8% PASS · 0 כשלים חוקיים (FAIL)</div>
    </div>
    <div class="score-card">
      <div class="score-title">כיווני אוויר ואור יום</div>
      <div class="score-val" style="color:#0284c7;">3–4</div>
      <div class="score-sub">100% מהדירות תלת/ארבע-כיווניות!</div>
    </div>
    <div class="score-card">
      <div class="score-title">חניה וצפיפות קומתית</div>
      <div class="score-val" style="color:#7c3aed;">1:1.09</div>
      <div class="score-sub">12 חניות רגילות (0 מכפילים!) · 2 דירות בקומה</div>
    </div>
  </div>

  <div class="alert-box">
    <strong>תמצית מנהלים:</strong> פרויקט <strong>יטקובסקי 7</strong> מציג את ציון האיכות הגבוה ביותר בפורטפוליו (<strong>91.4/100</strong>) בזכות תכנון בוטיק מוקפד של <strong>11 דירות בלבד</strong>: דירת גן יחידה בקומת הקרקע (105 מ"ר + 153 מ"ר גינה), 2 דירות בקומה בלבד בקומות א'–ד' עם <strong>3 כיווני אוויר מלאים</strong> לכל דירה, ו-2 פנטהאוזים על קומה שלמה כל אחד בקומות ה'–ו' עם <strong>4 כיווני אוויר</strong>. כל סוויטות ההורים בפרויקט ברוחב <strong>340–350 ס"מ</strong> (עוברות במלואן את תקן המצוינות האוסטרלי ADG ≥ 300 ס"מ), ומרתף החניון מספק <strong>12 חניות רגילות ב-100% ללא מכפילים</strong>.
  </div>

  <h2>📊 1. מטריצת ציוני איכות והשוואה לפרויקטי החברה</h2>
  <table>
    <thead>
      <tr>
        <th style="width: 28%;">קטגוריית הערכה ותקינה</th>
        <th style="width: 6%; text-align: center;">משקל</th>
        <th style="width: 11%; text-align: center;">יטקובסקי 7</th>
        <th style="width: 9%; text-align: center;">פינס 48</th>
        <th style="width: 9%; text-align: center;">קק״ל 10</th>
        <th style="width: 9%; text-align: center;">חפץ חיים 44</th>
        <th style="width: 8%; text-align: center;">סטטוס</th>
        <th style="width: 20%;">ממצא מרכזי מבוסס BIM</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>1. חקיקה ותקנות הבנייה (ישראל 2026)</strong></td>
        <td style="text-align: center;">20%</td>
        <td style="text-align: center; font-weight: 800; color: #1e3a8a;">98 / 100</td>
        <td style="text-align: center;">94</td>
        <td style="text-align: center;">96</td>
        <td style="text-align: center;">97</td>
        <td style="text-align: center;"><span class="badge badge-pass">PASS</span></td>
        <td>0 כשלי סף; ממ"ד 9.72 מ"ר נטו (335×290 ס"מ); גובה 2.85–3.25 מ'.</td>
      </tr>
      <tr>
        <td><strong>2. אור יום, מבט ואוורור (EN 17037 / CIBSE)</strong></td>
        <td style="text-align: center;">18%</td>
        <td style="text-align: center; font-weight: 800; color: #1e3a8a;">96 / 100</td>
        <td style="text-align: center;">71</td>
        <td style="text-align: center;">87</td>
        <td style="text-align: center;">95</td>
        <td style="text-align: center;"><span class="badge badge-pass">מצטיין</span></td>
        <td>3 כיווני אוויר בדירות 1–9; 4 כיווני אוויר בפנטהאוזים 10–11.</td>
      </tr>
      <tr>
        <td><strong>3. מדדי רווחה ופרופורציות (NDSS / ADG / HQI)</strong></td>
        <td style="text-align: center;">16%</td>
        <td style="text-align: center; font-weight: 800; color: #1e3a8a;">92 / 100</td>
        <td style="text-align: center;">68</td>
        <td style="text-align: center;">84</td>
        <td style="text-align: center;">90</td>
        <td style="text-align: center;"><span class="badge badge-pass">מצטיין</span></td>
        <td>100% מחדרי ההורים ברוחב 340–350 ס"מ (עובר ADG ≥ 300 ס"מ!).</td>
      </tr>
      <tr>
        <td><strong>4. שימושיות, ריהוט וגמישות (Boverket / DIN)</strong></td>
        <td style="text-align: center;">14%</td>
        <td style="text-align: center; font-weight: 800; color: #1e3a8a;">87 / 100</td>
        <td style="text-align: center;">70</td>
        <td style="text-align: center;">80</td>
        <td style="text-align: center;">84</td>
        <td style="text-align: center;"><span class="badge badge-info">טוב מאוד</span></td>
        <td>68%–76% מחיצות פריקות; קירות ארון רציפים; מעברי מיטה 80–85 ס"מ.</td>
      </tr>
      <tr>
        <td><strong>5. ארגונומיה, מטבחים ורחצה (NKBA / Neufert)</strong></td>
        <td style="text-align: center;">12%</td>
        <td style="text-align: center; font-weight: 800; color: #1e3a8a;">88 / 100</td>
        <td style="text-align: center;">74</td>
        <td style="text-align: center;">85</td>
        <td style="text-align: center;">86</td>
        <td style="text-align: center;"><span class="badge badge-info">טוב מאוד</span></td>
        <td>מטבחים מערביים מאווררים (340×310 עד 480×360); רחצה 260×210 ס"מ.</td>
      </tr>
      <tr>
        <td><strong>6. תחביר המרחב ופרטיות (Space Syntax / SAGA)</strong></td>
        <td style="text-align: center;">10%</td>
        <td style="text-align: center; font-weight: 800; color: #1e3a8a;">86 / 100</td>
        <td style="text-align: center;">74</td>
        <td style="text-align: center;">82</td>
        <td style="text-align: center;">85</td>
        <td style="text-align: center;"><span class="badge badge-info">טוב מאוד</span></td>
        <td>הפרדת סוויטת הורים בטיפוס הצפוני; כניסה ישירה לסלון ללא מבואה.</td>
      </tr>
      <tr>
        <td><strong>7. מיגון ובטיחות אש (פיקוד העורף / ת"י)</strong></td>
        <td style="text-align: center;">5%</td>
        <td style="text-align: center; font-weight: 800; color: #1e3a8a;">98 / 100</td>
        <td style="text-align: center;">95</td>
        <td style="text-align: center;">97</td>
        <td style="text-align: center;">98</td>
        <td style="text-align: center;"><span class="badge badge-pass">PASS</span></td>
        <td>ממ"ד 9.72 מ"ר ברוחב 2.90 מ', קירות 30 ס"מ, חלון הדף ודלת תקניים.</td>
      </tr>
      <tr>
        <td><strong>8. תנועה, חניה וממשק עירוני (קרקע ומרתף)</strong></td>
        <td style="text-align: center;">5%</td>
        <td style="text-align: center; font-weight: 800; color: #1e3a8a;">95 / 100</td>
        <td style="text-align: center;">76</td>
        <td style="text-align: center;">86</td>
        <td style="text-align: center;">93</td>
        <td style="text-align: center;"><span class="badge badge-pass">מצטיין</span></td>
        <td>12 חניות רגילות ב-100% (ללא מכפילים), מיסעה 6.00 מ', לובי דו-מפלסי.</td>
      </tr>
    </tbody>
  </table>

  <h2>🏢 2. ניתוח מפורט לפי טיפוסי הדירות (11 יח"ד · 4 טיפולוגיות)</h2>
  <table>
    <thead>
      <tr>
        <th>טיפוס דירה</th>
        <th>דירות וקומות</th>
        <th>שטח פלדלת + חוץ</th>
        <th>כיווני אוויר</th>
        <th>מידות חללים עיקריים (ס"מ)</th>
        <th>בדיקות מנוע (PASS/WARN/FAIL)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>דירת גן דרומית</strong></td>
        <td>דירה #1 (קומת קרקע · יזם)</td>
        <td>105 מ"ר + 153 מ"ר גינה</td>
        <td>S / W / E (3)</td>
        <td>סלון 420×480 · פ.אוכל 300×260 · מטבח 340×310 · הורים 340×360 · ח.שינה 290×340 · ממ"ד 335×290</td>
        <td><strong>83 PASS</strong> · 11 WARN · <span class="badge badge-pass">0 FAIL</span></td>
      </tr>
      <tr>
        <td><strong>טיפוס N צפוני חזיתי (4 חד')</strong></td>
        <td>דירות #3, #5, #7, #9 (קומות א'–ד')</td>
        <td>97 מ"ר + 12–18 מ"ר מרפסת סוכה</td>
        <td>N / W / E (3)</td>
        <td>סלון ו-פ.אוכל 410×460 · מטבח 310×290 · הורים מזרחי 340×360 · ח.שינה 295×340 · ממ"ד 335×290</td>
        <td><strong>83 PASS</strong> · 11 WARN · <span class="badge badge-pass">0 FAIL</span></td>
      </tr>
      <tr>
        <td><strong>טיפוס S דרומי עורפי (4 חד')</strong></td>
        <td>דירות #2, #4, #6, #8 (קומות א'–ד')</td>
        <td>102 מ"ר + 11–16 מ"ר מרפסת סוכה</td>
        <td>S / W / E (3)</td>
        <td>סלון 420×460 · פ.אוכל 310×260 · מטבח 340×310 · הורים 340×360 · ח.שינה 290×340 · ממ"ד 335×290</td>
        <td><strong>83 PASS</strong> · 11 WARN · <span class="badge badge-pass">0 FAIL</span></td>
      </tr>
      <tr>
        <td><strong>פנטהאוזים קומה שלמה (5 חד')</strong></td>
        <td>דירה #10 (קומה ה') ודירה #11 (קומה ו' · יזם)</td>
        <td>125–150 מ"ר + 52–64 מ"ר מרפסות גג</td>
        <td>N / S / E / W (4)</td>
        <td>סלון 560×480 / 540×460 · מטבח שף 480×360 · הורים 350×410 · חדרים 320×340 · ממ"ד 335×290</td>
        <td><strong>102 PASS</strong> · 7 WARN · <span class="badge badge-pass">0 FAIL</span></td>
      </tr>
    </tbody>
  </table>

  <h2>🔧 3. המלצות הנדסיות ותכנוניות ליישום בתוכניות העבודה והמכר</h2>
  <div class="section-card">
    <ol class="recommendations-list">
      <li>
        <div class="rec-title">שילוב מחיצת משרבייה / נגרות במבואת הכניסה לדירות הטיפוסיות (Space Syntax SS-3)</div>
        <div class="rec-desc">דלת הכניסה נפתחת ישירות אל חלל הסלון ופינת האוכל ללא מבואה סגורה. הוספת אלמנט נגרות דו-צדדי ברוחב 90 ס"מ תיצור סינון ויזואלי מלא ותגדיל את שטח האחסון הדירתי ב-0.8 מ"ק (השלמה ל-10.0 מ"ק לפי ADG 4G).</div>
      </li>
      <li>
        <div class="rec-title">דלת הזזה לכיס (Pocket Door) בחדרי רחצה הורים בדירות הטיפוסיות (165×200 ס"מ)</div>
        <div class="rec-desc">מרווח צד הידית בדלת חדר רחצה הורים עומד על 25 ס"מ (מול 30 ס"מ מומלץ ב-DIN 18040-2). התקנת כיס גבס (Pocket Door) תשחרר לחלוטין את רדיוס התמרון מול הכיור והמקלחון (90×90 ס"מ).</div>
      </li>
      <li>
        <div class="rec-title">הזזת ציר אסלה ב-4 ס"מ בחדרי הרחצה (NKBA Bathroom Ergonomics)</div>
        <div class="rec-desc">הגדלת מרחק ציר האסלה מהקיר הצדדי מ-40–42 ס"מ ל-46 ס"מ מומלצים לפי NKBA בשלב אינסטלציית השלד, ללא שינוי מיקום קירות.</div>
      </li>
      <li>
        <div class="rec-title">הצגת וריאציית העמדת מיטה על הקיר הארוך (335–340 ס"מ) בממ"ד ובחדר השינה הדרומי</div>
        <div class="rec-desc">רוחב החדרים (290–295 ס"מ) עומד בתקנות הבנייה וב-NDSS אך קרוב ל-300 ס"מ של ADG. הצגת העמדת ריהוט חלופית בתוכניות המכר תגדיל את מעבר הצד מ-85 ס"מ ל-110 ס"מ (עובר DIN 18040-2 במלואו).</div>
      </li>
    </ol>
  </div>

  <div class="footer-bar">
    <div><strong>archknow v2.1</strong> · מערכת ביקורת איכות אדריכלית, תאורה, אוורור, שימושיות ותקנים בינלאומיים</div>
    <div>פרויקט יטקובסקי אחים 7 (7א), פתח תקווה · יצחק קולסקי חברה לבניה והשקעות בע"מ · אוקטובר 2026</div>
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
        raise RuntimeError(f"Browser failed with return code {res.returncode}: {res.stderr}")

    size_kb = os.path.getsize(PRIMARY_PDF_PATH) / 1024
    print(f"Successfully generated PDF: {PRIMARY_PDF_PATH} ({size_kb:.1f} KB)")

    if os.path.exists(GDRIVE_DIR):
        try:
            shutil.copy2(PRIMARY_PDF_PATH, os.path.join(GDRIVE_DIR, PDF_FILENAME))
            shutil.copy2(HTML_PATH, os.path.join(GDRIVE_DIR, "yatkovski7_architectural_quality_analysis.html"))
            print(f"Copied PDF & HTML to GDrive project folder: {GDRIVE_DIR}")
        except Exception as e:
            print(f"Notice: GDrive copy skipped ({e})")

if __name__ == "__main__":
    generate_pdf()
