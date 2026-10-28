# יטקובסקי 7, פתח תקווה — פורטל תלת-ממד 3D BIM, CRM ו-GIS מרחבי

ברוכים הבאים למאגר המודל התלת-ממדי ההנדסי והשיווקי של פרויקט הבוטיק **יטקובסקי אחים 7 (7א), פתח תקווה** (גוש `6385`, חלקה `136`, מגרש `57`).

---

## הפעלה מהירה (ללא התקנה)

1. **פורטל תלת-ממד ראשי (3D BIM + CRM + סיור פנים):**
   * פתחו בדפדפן את הקובץ [`index.html`](index.html) (או [`yatkovski7_3d_model.html`](yatkovski7_3d_model.html) / [`yatkovski7_3d_bim_viewer.html`](yatkovski7_3d_bim_viewer.html)).
2. **פורטל 3D GIS ומפה מרחבית עירונית (28 נקודות עניין + תצ"א היברידית):**
   * פתחו בדפדפן את הקובץ [`yatkovski7_spatial_map.html`](yatkovski7_spatial_map.html) (ניתן לפתוח גם ישירות מתוך כפתור **"מפת 3D GIS ונקודות עניין"** בסרגל העליון של המודל הראשי).
3. **ייבוא לתוכנות שרטוט ומידול (Revit / SketchUp / Blender / Rhino):**
   * קובץ glTF 2.0 בינארי: [`yatkovski7_model.glb`](yatkovski7_model.glb)
   * קובץ Wavefront OBJ + חומרים: [`yatkovski7_model.obj`](yatkovski7_model.obj) + [`yatkovski7_model.mtl`](yatkovski7_model.mtl)

---

## מבנה התיקייה והקבצים

```text
יטקובסקי 7/מודל/
├── index.html                        # פורטל 3D BIM + CRM ראשי (Standalone HTML5)
├── yatkovski7_3d_model.html          # עותק תואם של פורטל התלת-ממד הראשי
├── yatkovski7_3d_bim_viewer.html     # עותק תואם של פורטל התלת-ממד הראשי
├── yatkovski7_spatial_map.html       # פורטל 3D GIS, תצ"א היברידית ו-28 נקודות עניין בפתח תקווה
├── compact_bim.json                  # קובץ ולידציה הנדסי (PASS בכל 5 בדיקות arch-2d-to-3d-bim)
├── yatkovski7_model.glb              # מודל 3D בינארי (glTF 2.0) לייבוא לתוכנות CAD/BIM
├── yatkovski7_model.obj              # מודל 3D בפורמט Wavefront OBJ
├── yatkovski7_model.mtl              # הגדרות חומרים וצבעים עבור קובץ ה-OBJ
├── SYSTEM_SCOPE_SPECIFICATION.md     # מסמך תחולות מערכת מלא (תואם 100% לתחולות פינס 48)
├── PRD_SPECIFICATION.md              # מסמך אפיון מוצר ודרישות מערכת (PRD)
├── DESIGN_SYSTEM.md                  # מפרט מערכת עיצוב, צבעים וחומרים (Design System)
├── yatkovski7_bim_report.md          # דו"ח בקרת איכות וולידציה הנדסית (BIM QA Report)
├── data/
│   ├── yatkovski7_extracted_plans.json   # פוליגוניזציה של 9 הקומות מתוך ה-DWG המקורי
│   ├── yatkovski7_units_crm.json         # מאגר 11 הדירות (קולסקי / בן אהרון) ו-12 החניות
│   ├── unified_yatkovski7_3d_map.json    # תצ"א היברידית אמיתית ברזולוציות Z15/Z17/Z19
│   ├── yatkovski7_spatial_map_data.json  # 28 נקודות עניין עירוניות בפתח תקווה (WGS84)
│   └── compact_bim.json                  # עותק גיבוי של קובץ הוולידציה ההנדסי
└── src/
    ├── export_yatkovski7_json.py         # חילוץ ופוליגוניזציה של קובץ ה-DWG/DXF
    ├── export_yatkovski7_3d_files.py     # הפקת קבצי OBJ, MTL ו-GLB
    ├── build_yatkovski7_gis.py           # הורדת תצ"א והפקת פורטל ה-3D GIS
    └── build_yatkovski7_viewer.py        # מחולל פורטל ה-3D BIM & CRM הראשי
```
