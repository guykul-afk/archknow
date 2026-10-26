"""
plan_analyzer — smart architectural PDF analysis for ArchKnow.

Builds the *Plan Data Model* (analysis database) from a PDF floor plan following
the "מידול אדריכלי" (arch-2d-to-3d-bim) workflow up to — but excluding — 3D
modelling, then adapts it to the validation engine's apartment schema.

    from plan_analyzer import analyze_pdf_to_project
    project, model = analyze_pdf_to_project("plan.pdf", "uploads", file_hash)
"""
import json
import os

from .pipeline import analyze_pdf, SCHEMA_VERSION  # noqa: F401
from .adapter import to_project, to_engine_apartment  # noqa: F401


def analyze_pdf_to_project(pdf_path, work_dir, file_hash, preview_dir=None, use_vision=True,
                           preview_url_prefix="/uploads/", reading_override=None, log=print):
    """Run the full pipeline; writes `<hash>_plan_model.json` to work_dir.
    Returns (project_json, plan_model)."""
    model = analyze_pdf(pdf_path, work_dir, file_hash, preview_dir=preview_dir, use_vision=use_vision,
                        reading_override=reading_override, log=log)
    if not model["sheets"]:
        raise ValueError("לא זוהתה תכנית קומה בקובץ (לא נמצאו קירות מסומנים). " + "; ".join(model["warnings"]))
    with open(os.path.join(work_dir, f"{file_hash}_plan_model.json"), "w", encoding="utf-8") as f:
        json.dump(model, f, ensure_ascii=False, indent=1)
    return to_project(model, preview_url_prefix=preview_url_prefix), model
