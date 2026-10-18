"""Space taxonomy: maps a Hebrew label to a canonical space type.

Canonical types (plan model) and whether they belong to the dwelling unit:
  living, dining, kitchen, bedroom, safe_room, study, bathroom, toilet, utility,
  storage, walk_in_closet, corridor, entrance                     → interior, in unit
  balcony, service_balcony, garden                                 → private outdoor, in unit
  lobby, elevator, stairs, shaft, core, neighbour, parking         → outside the unit
"""
import re

from .hebrew import normalize_hebrew

INTERIOR_TYPES = {"living", "dining", "kitchen", "bedroom", "safe_room", "study", "bathroom", "toilet",
                  "utility", "storage", "walk_in_closet", "corridor", "entrance"}
OUTDOOR_TYPES = {"balcony", "service_balcony", "garden"}
EXCLUDED_TYPES = {"lobby", "elevator", "stairs", "shaft", "core", "neighbour", "parking"}
HABITABLE_TYPES = {"living", "dining", "kitchen", "bedroom", "safe_room", "study"}
WET_TYPES = {"bathroom", "toilet"}

# Israeli room count ("דירת N חדרים") counts living + bedrooms (+ ממ"ד, study)
ROOM_COUNT_TYPES = {"living", "bedroom", "safe_room", "study"}


def _norm(text):
    t = normalize_hebrew(text or "").strip()
    t = t.replace("״", '"').replace("'", "'").replace("׳", "'")
    t = re.sub(r"\bח\.\s*", "חדר ", t)
    t = re.sub(r"\s+", " ", t)
    return t


_RULES = [
    # order matters: first match wins
    (("מרחב מוגן", 'ממ"ד', "ממד", "מ.מ.ד"), "safe_room"),
    (("מרפסת שירות", "מסתור כביסה", "מסתור"), "service_balcony"),
    (("מרפסת", "גזוזטר", "מרפסת שמש", "לוגיה"), "balcony"),
    (("גינה", "חצר"), "garden"),
    (("לובי", "מבואה קומתית", "מבואת קומה"), "lobby"),
    (("מעלית",), "elevator"),
    (("מדרגות",), "stairs"),
    (("פיר", "פירים", "ר.ש", "ארון חשמל", "ארון מים", "שעון מים", "מונים", "תקשורת", "גז "), "shaft"),
    (("חניה", "חניון"), "parking"),
    (("חדר ארונות", "ארונות"), "walk_in_closet"),
    (("מחסן", "ארון", "אחסון"), "storage"),
    (("אמבטיה", "רחצה", "מקלחת"), "bathroom"),
    (("שירותים", "שרותים", "שירותי", "שרותי", "נוחיות", "wc"), "toilet"),
    (("שירות", "שרות", "כביסה"), "utility"),
    (("מטבח", "מטבחון"), "kitchen"),
    (("פינת אוכל", "פינת אכילה", "חדר אוכל"), "dining"),
    (("סלון", "חדר דיור", "פינת ישיבה", "חדר מגורים"), "living"),
    (("עבודה", "משרד", "ספריה"), "study"),
    (("שינה", "הורים", "ילדים", "חדר"), "bedroom"),
    (("מסדרון", "מעבר", "פרוזדור"), "corridor"),
    (("מבואה", "כניסה", "הול"), "entrance"),
]


def classify_label(label):
    """Return (space_type, normalised_label). Unknown labels → ('unknown', label)."""
    t = _norm(label)
    low = t.lower()
    if re.fullmatch(r"דירה\s*\d+.*", t) or "דירה שכנה" in t:
        return "neighbour", t
    for keys, typ in _RULES:
        if any(k in low for k in keys):
            # "חדר רחצה הורים" is a bathroom, not a bedroom — rules order handles it
            return typ, t
    return "unknown", t


def is_in_unit(space_type, vision_inside=True):
    if space_type in EXCLUDED_TYPES:
        return False
    if space_type == "unknown":
        return bool(vision_inside)
    return True
