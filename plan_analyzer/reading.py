"""
Stage 2 — reading the sheet: labels, written dimensions, title block, north arrow,
fixtures. (Skill step 1 "categorised text extraction" + step 2 "datum & rules".)

Two sources, merged by the pipeline:
  * text layer  – deterministic, free (PDFs exported with real text);
  * vision      – Gemini structured extraction for sheets whose text is
                  vectorised (common for CAD sales plans). Result is cached
                  per file hash so a sheet is read once.
Coordinates are returned as normalised boxes [x0, y0, x1, y1] in 0..1 page units.
"""
import json
import os
import re
import io

from .hebrew import normalize_hebrew, has_hebrew

DEFAULT_MODEL = os.environ.get("GEMINI_VISION_MODEL", "gemini-flash-latest")

VISION_PROMPT = """You are reading an Israeli architectural floor-plan sheet (Hebrew).
Read EVERYTHING written on the drawing and return ONE JSON object, no markdown.
All boxes use "box_2d": [ymin, xmin, ymax, xmax] normalised to 0-1000 on the full image.
Write Hebrew in normal logical reading order (as a person reads it), exactly as printed.

{
  "sheet": {
    "project_name": str|null, "city": str|null,
    "plan_type": "sales_plan"|"execution_plan"|"permit_plan"|"other",
    "sheet_kind": "apartment_plan"|"typical_floor"|"ground_floor"|"basement"|"roof"|"elevation"|"section"|"site_plan"|"other",
    "floors_text": str|null,            // as printed, e.g. "קומה 1, 5-7"
    "floors": [int],                    // expanded list, e.g. [1,5,6,7]
    "apartment_numbers": [str],
    "rooms_count": number|null,         // e.g. "דירה 5 חדרים" -> 5 (4.5 allowed)
    "apartment_area_sqm": number|null,  // "שטח דירה"
    "scale": str|null,                  // e.g. "1:50"
    "date": str|null, "sheet_number": str|null,
    "north_arrow": {"present": bool, "box_2d": [..]|null, "label_text": str|null,
                    "north_direction_deg": number|null}  // direction the arrow points to, degrees clockwise from image-up
                    // the north symbol is often SMALL (an arrow/compass with "צפון" or "N" beside it) — search the whole sheet.
                    // label_text = the text printed with the symbol. Arrows marking "כניסה"/"יציאה" are NOT north arrows.
  },
  "spaces": [ {"label": str, "box_2d": [..], "inside_unit": bool,
               "area_sqm_written": number|null} ],
      // every room/space name: סלון, מטבח, חדר שינה, ממ"ד, חדר רחצה, שירותים, מרפסת, מחסן, לובי, מעלית, חדר מדרגות...
      // one entry per label occurrence; multi-line labels ("חדר שינה" + "ממ\"ד") are ONE entry with the joined text.
      // inside_unit=false for building core / neighbours (לובי, מעלית, מדרגות, פיר, דירה שכנה).
  "dimensions": [ {"value": number, "unit": "cm"|"m", "orientation": "horizontal"|"vertical",
                   "box_2d": [..]} ],
      // every dimension number on a dimension line (e.g. 405, 380). orientation = direction of the text baseline.
  "annotations": [ {"text": str, "kind": "window_type"|"level"|"ceiling"|"equipment"|"note"|"other",
                    "box_2d": [..]} ],
      // e.g. "תריס גלילה" (window_type), "+28.73" (level), "הנמכת גבס" (ceiling), "מסתור כביסה", "מזגן" (equipment)
  "fixtures": [ {"type": "toilet"|"washbasin"|"shower"|"bathtub"|"kitchen_sink"|"cooktop"|"washing_machine"|"ac_unit"|"water_heater"|"other",
                 "box_2d": [..]} ],
  "notes": [str]   // the numbered general notes, each shortened to one line
}
Return [] for empty lists and null for unknown values. Do not invent anything that is not drawn."""


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _box_from_2d(b):
    """Gemini box_2d [ymin,xmin,ymax,xmax] (0..1000) → [x0,y0,x1,y1] (0..1)."""
    if not isinstance(b, (list, tuple)) or len(b) != 4:
        return None
    try:
        y0, x0, y1, x1 = [float(v) / 1000.0 for v in b]
    except (TypeError, ValueError):
        return None
    return [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)]


def _strip_json(text):
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```(?:json)?", "", t).rstrip("`").strip()
    s, e = t.find("{"), t.rfind("}")
    return t[s:e + 1] if s != -1 and e != -1 else t


def load_api_key():
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        return key
    # local development: functions/.env (never logged)
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for cand in (os.path.join(here, "functions", ".env"), os.path.join(here, ".env")):
        if os.path.exists(cand):
            with open(cand, encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith(("GEMINI_API_KEY", "GOOGLE_API_KEY")) and "=" in line:
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def normalise_reading(raw, source):
    """Convert a raw vision/text reading into the internal reading structure."""
    raw = raw or {}
    sheet = dict(raw.get("sheet") or {})
    na = sheet.get("north_arrow") or {}
    label = str(na.get("label_text") or "")
    confirmed = bool(na.get("present")) and (
        "צפון" in label or re.search(r"(^|[^A-Za-z])N([^A-Za-z]|$)", label) is not None
        or source == "override")
    deg = na.get("north_direction_deg")
    sheet["north_arrow"] = {
        "present": confirmed and deg is not None,
        "box": _box_from_2d(na.get("box_2d")) if na.get("box_2d") else na.get("box"),
        "label_text": label or None,
        "north_direction_deg": deg if confirmed else None,
        "rejected_reason": None if confirmed or not na.get("present") else "הסמל אינו מסומן 'צפון'/N — לא נעשה בו שימוש",
    }
    out = {"source": source, "sheet": sheet, "spaces": [], "dimensions": [],
           "annotations": [], "fixtures": [], "notes": list(raw.get("notes") or [])}
    for s in raw.get("spaces") or []:
        box = s.get("box") or _box_from_2d(s.get("box_2d"))
        if not box or not s.get("label"):
            continue
        out["spaces"].append({"label": str(s["label"]).strip(), "box": box,
                              "inside_unit": s.get("inside_unit", True),
                              "area_sqm_written": s.get("area_sqm_written"), "source": source})
    for d in raw.get("dimensions") or []:
        box = d.get("box") or _box_from_2d(d.get("box_2d"))
        try:
            val = float(d.get("value"))
        except (TypeError, ValueError):
            continue
        if not box or val <= 0:
            continue
        if str(d.get("unit") or "cm").lower() == "m":
            val *= 100.0
        out["dimensions"].append({"value_cm": val, "orientation": d.get("orientation") or "horizontal",
                                  "box": box, "source": source})
    for a in raw.get("annotations") or []:
        box = a.get("box") or _box_from_2d(a.get("box_2d"))
        if box and a.get("text"):
            out["annotations"].append({"text": a["text"], "kind": a.get("kind") or "other", "box": box, "source": source})
    for fx in raw.get("fixtures") or []:
        box = fx.get("box") or _box_from_2d(fx.get("box_2d"))
        if box and fx.get("type"):
            out["fixtures"].append({"type": fx["type"], "box": box, "source": source})
    return out


# ---------------------------------------------------------------------------
# text layer (deterministic)
# ---------------------------------------------------------------------------
_NUM = re.compile(r"^\d{2,4}(?:\.\d+)?$")
_TITLE_PATTERNS = {
    "floor": re.compile(r"קומ(?:ה|ות)\s*[:\-]?\s*([\d,\-–\s]+)"),
    "apt": re.compile(r"דיר(?:ה|ות)\s*[:\-]?\s*([\d,\s]+)"),
    "rooms": re.compile(r"(\d+(?:\.\d)?)\s*חדרים"),
    "area": re.compile(r"שטח\s*(?:ה)?דירה\s*[:\-]?\s*(\d+(?:\.\d+)?)"),
    "scale": re.compile(r"1\s*:\s*(\d+)"),
}


def _expand_floors(txt):
    out = []
    for part in re.split(r"[,\s]+", txt or ""):
        m = re.match(r"^(\d+)\s*[-–]\s*(\d+)$", part)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            if 0 <= b - a <= 60:
                out.extend(range(a, b + 1))
        elif part.isdigit():
            out.append(int(part))
    return out


def read_text_layer(page):
    """Reading from the PDF text layer. Returns None when the page has no usable text."""
    W, H = page.rect.width, page.rect.height
    words = page.get_text("words")
    if len(words) < 5:
        return None
    lines = {}
    for x0, y0, x1, y1, txt, b, l, _ in words:
        lines.setdefault((b, l), []).append((x0, y0, x1, y1, txt))
    spaces, dims, annotations, all_text = [], [], [], []
    for (b, l), ws in lines.items():
        ws.sort(key=lambda w: w[0])
        text = normalize_hebrew(" ".join(w[4] for w in ws))
        x0 = min(w[0] for w in ws); y0 = min(w[1] for w in ws)
        x1 = max(w[2] for w in ws); y1 = max(w[3] for w in ws)
        box = [x0 / W, y0 / H, x1 / W, y1 / H]
        all_text.append(text)
        if len(ws) == 1 and _NUM.match(ws[0][4]):
            orient = "horizontal" if (x1 - x0) >= (y1 - y0) else "vertical"
            dims.append({"value": float(ws[0][4]), "unit": "cm", "orientation": orient, "box": box})
        elif not has_hebrew(text) and not re.match(r"^[+\-±]\d+\.\d{2}$", text.replace(" ", "")):
            for wx0, wy0, wx1, wy1, wtxt in ws:
                wclean = wtxt.strip().strip("/\\(),;")
                if _NUM.match(wclean):
                    worient = "horizontal" if (wx1 - wx0) >= (wy1 - wy0) else "vertical"
                    dims.append({
                        "value": float(wclean),
                        "unit": "cm",
                        "orientation": worient,
                        "box": [wx0 / W, wy0 / H, wx1 / W, wy1 / H],
                    })
                elif re.match(r"^\d{2,4}[/\\]\d{2,4}$", wclean):
                    for part_num in re.split(r"[/\\]", wclean):
                        if _NUM.match(part_num):
                            worient = "horizontal" if (wx1 - wx0) >= (wy1 - wy0) else "vertical"
                            dims.append({
                                "value": float(part_num),
                                "unit": "cm",
                                "orientation": worient,
                                "box": [wx0 / W, wy0 / H, wx1 / W, wy1 / H],
                            })
        elif has_hebrew(text):
            spaces.append({"label": text, "box": box, "inside_unit": True})
        elif re.match(r"^[+\-±]\d+\.\d{2}$", text.replace(" ", "")):
            annotations.append({"text": text, "kind": "level", "box": box})
    joined = " | ".join(all_text)
    sheet = {"plan_type": "other", "sheet_kind": "other"}
    m = _TITLE_PATTERNS["floor"].search(joined)
    if m:
        sheet["floors_text"] = m.group(0)
        sheet["floors"] = _expand_floors(m.group(1))
    m = _TITLE_PATTERNS["apt"].search(joined)
    if m:
        sheet["apartment_numbers"] = [p for p in re.split(r"[,\s]+", m.group(1)) if p]
    m = _TITLE_PATTERNS["rooms"].search(joined)
    if m:
        sheet["rooms_count"] = float(m.group(1))
    m = _TITLE_PATTERNS["area"].search(joined)
    if m:
        sheet["apartment_area_sqm"] = float(m.group(1))
    m = _TITLE_PATTERNS["scale"].search(joined)
    if m:
        sheet["scale"] = f"1:{m.group(1)}"
    return normalise_reading({"sheet": sheet, "spaces": spaces, "dimensions": dims,
                              "annotations": annotations}, "text_layer")


# ---------------------------------------------------------------------------
# vision (Gemini)
# ---------------------------------------------------------------------------
def read_with_vision(png_bytes, cache_path=None, model=None, api_key=None):
    """Structured reading with Gemini. Returns (reading | None, error | None)."""
    if cache_path and os.path.exists(cache_path):
        with open(cache_path, encoding="utf-8") as f:
            return normalise_reading(json.load(f), "vision"), None
    api_key = api_key or load_api_key()
    if not api_key:
        return None, "GEMINI_API_KEY לא מוגדר — קריאת טקסט וקטורי מהתכנית לא בוצעה"
    model = model or DEFAULT_MODEL
    level = os.environ.get("GEMINI_THINKING_LEVEL", "low")
    attempts = [level, None, None]  # low thinking first, then the model's default
    raw, last_err = None, None
    for thinking in attempts:
        try:
            text = _call_gemini(png_bytes, model, api_key, thinking)
            raw = json.loads(_clean_json(_strip_json(text)))
            if not isinstance(raw, dict):
                raise ValueError("התשובה אינה אובייקט JSON")
            break
        except Exception as e:  # network, quota, malformed JSON → retry
            last_err = e
            raw = None
    if raw is None:
        return None, f"קריאת Vision נכשלה: {last_err}"
    if cache_path:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(raw, f, ensure_ascii=False, indent=1)
    return normalise_reading(raw, "vision"), None


def _clean_json(t):
    """Remove // comments and trailing commas that LLMs sometimes emit."""
    t = re.sub(r'(?m)^\s*//.*$', "", t)
    t = re.sub(r'(?<=[\]}"\d])\s*//[^\n"]*$', "", t, flags=re.M)
    t = re.sub(r",\s*([\]}])", r"\1", t)
    return t


def _call_gemini(png_bytes, model, api_key, thinking_level=None):
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        import google.generativeai as genai_old
        from PIL import Image
        genai_old.configure(api_key=api_key)
        m = genai_old.GenerativeModel(model)
        resp = m.generate_content([VISION_PROMPT, Image.open(io.BytesIO(png_bytes))],
                                  generation_config={"response_mime_type": "application/json", "temperature": 0.0})
        return resp.text
    client = genai.Client(api_key=api_key)
    parts = [types.Part.from_bytes(data=png_bytes, mime_type="image/png"), VISION_PROMPT]
    cfg = dict(response_mime_type="application/json", temperature=0.0)
    if thinking_level:
        try:
            cfg["thinking_config"] = types.ThinkingConfig(thinking_level=thinking_level)
        except Exception:
            pass
    resp = client.models.generate_content(model=model, contents=parts, config=types.GenerateContentConfig(**cfg))
    return resp.text


def merge_readings(primary, secondary):
    """Prefer `primary` (text layer is exact); fill gaps from `secondary` (vision)."""
    if not primary:
        return secondary
    if not secondary:
        return primary
    out = dict(primary)
    sheet = dict(secondary.get("sheet") or {})
    sheet.update({k: v for k, v in (primary.get("sheet") or {}).items() if v not in (None, [], "", "other")})
    out["sheet"] = sheet
    for key in ("spaces", "dimensions"):
        if len(primary.get(key) or []) < 2:
            out[key] = secondary.get(key) or []
    for key in ("annotations", "fixtures", "notes"):
        out[key] = (primary.get(key) or []) + (secondary.get(key) or [])
    out["source"] = "text_layer+vision"
    return out
