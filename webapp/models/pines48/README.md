# פרויקט פינס 48 פינת הבעל שם טוב, פתח תקווה — מערכת הדמיה שיווקית 3D וניתוח מרחבי (GIS)

מערכת הדמיה אדריכלית תלת-ממדית אינטראקטיבית בקנה מידה `1:50` (חוץ + פנים מתוך תוכניות **נחומי אדריכלים**) המשולבת על גבי מפת **Google Maps** רב-רזולוציונית (`Z15 + Z17 + Z19`) עם 8 מעגלי מרחק ו-28 מוקדי עניין עירוניים מאומתים (כולל תחנת המטרו העתידית בעיריית פתח תקווה — קו M2).

---

## מבנה הפרויקט

- **[`index.html`](./index.html)** — קובץ המערכת הראשי העצמאי (`Standalone 3D Marketing & GIS Viewer`). ניתן לפתיחה ישירה בכל דפדפן ללא התקנה.
- **[`pines48_spatial_map.html`](./pines48_spatial_map.html)** — מפת ה-GIS הדו-ממדית המשלימה.
- **[`pines48_model.glb`](./pines48_model.glb) / [`pines48_model.obj`](./pines48_model.obj)** — קובצי מודל תלת-ממדי לתוכנות CAD/3D חיצוניות.
- **[`docs/PRD_SPECIFICATION.md`](./docs/PRD_SPECIFICATION.md)** — מסמך אפיון מערכת מלא (PRD & Technical Specification).
- **[`docs/DESIGN_SYSTEM.md`](./docs/DESIGN_SYSTEM.md)** — מסמך עיצוב, חוויית משתמש ושפה חזותית (UI/UX & 3D Design System).
- **[`src/build_html_viewer.py`](./src/build_html_viewer.py)** — מחולל המערכת המייצר את `index.html`.
- **[`src/build_seamless_3d_map.py`](./src/build_seamless_3d_map.py)** — סקריפט הורדת וכיול מפות הלוויין מרמות זום 15, 17 ו-19.
- **[`src/update_metro_poi.py`](./src/update_metro_poi.py)** — סקריפט עדכון מאגר מוקדי הסביבה ותחנת המטרו.
- **[`data/`](./data/)** — נתוני ה-JSON המכוילים (`extracted_interior_plans.json`, `unified_3d_map.json`, `spatial_map_data.json`).

---

## הפעלה ובנייה מחדש

### 1. צפייה במערכת
- פתחו בלחיצה כפולה את הקובץ [`index.html`](./index.html), או הריצו שרת מקומי בתיקיית הפרויקט:
  ```powershell
  python -m http.server 8080
  ```
  וגשו לכתובת: `http://localhost:8080/index.html`

### 2. בנייה מחדש לאחר שינויים בקוד או בנתונים
```powershell
python src/build_html_viewer.py
```
הסקריפט ייצר מחדש את `index.html` עם כל השינויים.
