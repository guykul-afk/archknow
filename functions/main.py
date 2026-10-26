import os
import json
import tempfile
from firebase_functions import storage_fn, options
from firebase_admin import initialize_app, firestore, storage

# Import local modules from the deployed function environment
import pdf_parser
import validation_engine
from plan_analyzer import analyze_pdf_to_project

initialize_app()


@storage_fn.on_object_finalized(memory=options.MemoryOption.GB_2, timeout_sec=540)
def analyze_pdf_plan(event: storage_fn.CloudEvent[storage_fn.StorageObjectData]):
    """
    Triggers when a PDF is uploaded to Firebase Storage.
    Runs the smart plan analysis (plan_analyzer: sheet reading with Gemini vision,
    2D model of walls/openings/spaces, extraction QA), validates every apartment
    against the knowledge base and saves the result to Firestore.
    """
    bucket_name = event.data.bucket
    file_path = event.data.name
    db = firestore.client()

    if not file_path.endswith(".pdf") or not file_path.startswith("uploads/"):
        print(f"Skipping non-upload file: {file_path}")
        return

    file_name = os.path.basename(file_path)
    file_hash = file_name.replace(".pdf", "")
    print(f"Processing PDF file: {file_name} with hash: {file_hash}")
    doc_ref = db.collection("projects").document(file_hash)
    doc_ref.set({"status": "processing", "updated_at": firestore.SERVER_TIMESTAMP})

    # 1. Download PDF to a private temp dir
    work_dir = tempfile.mkdtemp(prefix=f"plan_{file_hash}_")
    temp_pdf_path = os.path.join(work_dir, file_name)
    bucket = storage.bucket(bucket_name)
    bucket.blob(file_path).download_to_filename(temp_pdf_path)

    # 2. Smart analysis → project JSON (+ plan model written to work_dir)
    try:
        project_data, _model = analyze_pdf_to_project(temp_pdf_path, work_dir, file_hash,
                                                      preview_dir=work_dir, preview_url_prefix="")
    except Exception as e:
        print(f"plan_analyzer failed: {e}; trying legacy parser")
        try:
            project_data = pdf_parser.legacy_parse_pdf_plan(
                temp_pdf_path, os.path.join(work_dir, f"{file_hash}_project.json"), file_hash)
            project_data.setdefault("warnings", []).append(f"הניתוח החכם נכשל ({e}) — הופעל המפענח הישן.")
        except Exception as e2:
            doc_ref.set({"status": "error", "error": f"שגיאה בניתוח קובץ ה-PDF: {e2}",
                         "updated_at": firestore.SERVER_TIMESTAMP})
            return

    # 3. Upload preview images and make them public for the web app
    def publish(name):
        if not name:
            return name
        local = os.path.join(work_dir, os.path.basename(name))
        if not os.path.exists(local):
            return name
        blob = bucket.blob(f"uploads/{os.path.basename(name)}")
        blob.upload_from_filename(local)
        blob.make_public()
        return blob.public_url

    project_data["bg_image_url"] = publish(project_data.get("bg_image_url"))
    for floor in project_data.get("floors", []):
        floor["bg_image_url"] = publish(floor.get("bg_image_url")) or project_data["bg_image_url"]
        for apt in floor.get("apartments", []):
            ex = apt.get("plan_extraction")
            if ex and ex.get("preview_image"):
                ex["preview_image"] = floor["bg_image_url"]

    # 4. Run the validation engine on every apartment
    rules_dir = "okf_rules" if os.path.exists("okf_rules") else "functions/okf_rules"
    rules = validation_engine.load_okf_rules(rules_dir)
    for floor in project_data.get("floors", []):
        for apt in floor.get("apartments", []):
            try:
                apt["validation_results"] = validation_engine.run_validation(apt, rules)
            except Exception as e:
                print(f"Error running validation: {e}")
                apt["validation_results"] = []

    # 5. Save to Firestore. Polygons are nested arrays (unsupported by Firestore),
    #    so the full project is stored as a JSON string; flat fields keep old clients working.
    first = (project_data.get("floors") or [{}])[0].get("apartments", [{}])[0]
    doc_ref.set({
        "status": "success",
        "project_name": project_data.get("project_name", file_name),
        "bg_image_url": project_data.get("bg_image_url"),
        "project_json": json.dumps(project_data, ensure_ascii=False),
        "validation_results": first.get("validation_results", []),
        "updated_at": firestore.SERVER_TIMESTAMP,
    })
    print(f"Successfully processed and saved project {file_hash} to Firestore!")
