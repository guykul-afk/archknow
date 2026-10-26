"""Hebrew text helpers for CAD-exported PDFs (visual-order reversal, normalisation).
Ported from the `arch-2d-to-3d-bim` skill (preprocess_pdf.normalize_hebrew) and
the legacy pdf_parser.fix_hebrew_text."""
import re

_HEB = re.compile(r"[\u0590-\u05FF]")

# common words that CAD exports write in visual (reversed) order
_REVERSALS = {
    "תומוק": "קומות", "תינכת": "תכנית", "תויסופיט": "טיפוסיות", "תיסופיט": "טיפוסית",
    "תזיח": "חזית", "פתרמ": "מרתף", "עקרק": "קרקע", 'ד"ממ': 'ממ"ד', "דממ": "ממד",
    "ןולס": "סלון", "חבטמ": "מטבח", "תילעמ": "מעלית", "תקב": "בקת", "עקב": "בקע",
    "הלוגרפ": "פרגולה", "הגיסנ": "נסיגה", "ןוינח": "חניון", "המוק": "קומה",
    "הנישׁ": "שינה", "הנש": "שנה", "הנייש": "שינה", "הדיר": "דירה", "רדח": "חדר",
    "תספרמ": "מרפסת", "הצחר": "רחצה", "הטבמא": "אמבטיה", "םיתוריש": "שירותים",
    "תורש": "שרות", "תוריש": "שירות", "ןסחמ": "מחסן", "יבול": "לובי",
}
_KEYWORDS = ["ממ\"ד", "ממד", "סלון", "מטבח", "מעלית", "לובי", "חזית", "מרתף", "קרקע",
             "קומה", "קומות", "חדר", "שינה", "דירה", "מרפסת", "רחצה", "שירות", "שרות"]


def has_hebrew(text):
    return bool(text) and bool(_HEB.search(text))


def normalize_hebrew(text):
    """Return Hebrew text in logical order (fixes visual-order exports)."""
    s = (text or "").replace("\xa0", " ").replace("\xad", "-").strip()
    if not has_hebrew(s):
        return s
    words = s.split()
    fixed = [_REVERSALS.get(w, w) for w in words]
    if fixed != words:
        return " ".join(fixed)
    # whole-string reversal when the reversed form contains known words
    rev = s[::-1]
    score = sum(k in s for k in _KEYWORDS)
    rscore = sum(k in rev for k in _KEYWORDS)
    if rscore > score:
        return rev
    return s
