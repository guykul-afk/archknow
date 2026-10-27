# Central 3D Models Repository Rule (Single Source of Truth)

- **Central 3D Models Directory:** `G:\Shared drives\שליטה ובקרה\מודלים פרויקטים`
- **Catalog File:** `G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\00_models_catalog.json`
- **Never rebuild existing 3D models from scratch** when they already exist in `G:\Shared drives\שליטה ובקרה\מודלים פרויקטים\<שם_הפרויקט>`.
- **Zero-Copy Principle:** Always load/serve existing 3D models (`*_3d_model.html`, `*_3d_bim_viewer.html`, `*.glb`, `*.obj`) directly from `G:\Shared drives\שליטה ובקרה\מודלים פרויקטים` without duplicating heavy files into the workspace.
- When overlaying planning analysis, audit notes, or Value Engineering (VE) proposals on a 3D model, inject or layer the 3D annotations/volumes on top of the existing Three.js scene (`scene`, `FLOORS`, `floorGroups`, `activeCam`, `camState`, `selectFloor`, `setFloorMode`) rather than rebuilding the base model.
