"""
Stage 4 — validation of the extracted plan model (adapted from the skill's
validate_bim.py checks, in 2D):
  * dimension checksum   – written dimensions vs. measured dimension lines (scale)
  * area checksum        – Σ net room areas vs. the declared apartment area
  * room count           – declared "N חדרים" vs. detected rooms
  * room dimensions      – written room dimensions vs. measured room extents
  * ממ"ד                 – present, wall thickness, blast door & window
  * topology             – every unit space reachable from the entrance
  * coverage             – labels mapped, north arrow, unlabeled spaces
Statuses: PASS / WARN / FAIL. FAIL here means *the extraction is unreliable*
(not a design violation) — design rules are judged by validation_engine.
"""
from .taxonomy import INTERIOR_TYPES, OUTDOOR_TYPES

NET_TO_GROSS_RANGE = (0.72, 0.95)   # Σ net interior / declared (gross incl. walls)


def _r(status, check, message, value=None):
    out = {"status": status, "check": check, "message": message}
    if value is not None:
        out["value"] = value
    return out


def run_checks(sheet):
    out = []
    cal = sheet.get("calibration", {})
    spaces = sheet.get("spaces", [])
    apt = sheet.get("apartment", {})
    unit = [s for s in spaces if s.get("in_unit") and s.get("area_sqm") is not None]

    # 1. scale / dimension checksum
    n, tot = cal.get("matched_dimensions", 0), cal.get("total_dimensions", 0)
    err = cal.get("median_error_pct")
    if n >= 2 and err is not None and n >= 0.5 * tot:
        st = "PASS" if err <= 2.0 else "WARN" if err <= 5.0 else "FAIL"
        msg = f"קנה מידה {cal.get('scale')} אומת מול {n}/{tot} מידות כתובות — סטייה חציונית {err:.1f}%."
        if cal.get("correction", 1.0) != 1.0:
            msg += f" הוחל תיקון {cal['correction']}."
        out.append(_r(st, "קנה מידה ומידות כתובות", msg, err))
    elif tot:
        out.append(_r("WARN", "קנה מידה ומידות כתובות",
                      f"רק {n}/{tot} מידות כתובות זוהו על קווי מידה — קנה המידה {cal.get('scale')} לא אומת במלואו."))
    else:
        out.append(_r("WARN", "קנה מידה ומידות כתובות",
                      f"לא נקראו מידות כתובות — הסתמכות על קנה מידה {cal.get('scale')} ({cal.get('scale_source')})."))

    # 2. area checksum
    net = apt.get("net_interior_area_sqm") or 0
    declared = apt.get("declared_area_sqm")
    if declared and net:
        ratio = net / float(declared)
        lo, hi = NET_TO_GROSS_RANGE
        st = "PASS" if lo <= ratio <= hi else "WARN" if 0.6 <= ratio <= 1.02 else "FAIL"
        out.append(_r(st, "התאמת שטח לשטח המוצהר",
                      f"סכום שטחי פנים נטו {net:.1f} מ\"ר = {ratio:.0%} מהשטח המוצהר {declared} מ\"ר "
                      f"(צפוי {lo:.0%}–{hi:.0%}, כי השטח המוצהר כולל קירות).", round(ratio, 3)))
    elif net:
        out.append(_r("WARN", "התאמת שטח לשטח המוצהר", f"שטח פנים נטו {net:.1f} מ\"ר; אין שטח מוצהר בגיליון להשוואה."))

    # 3. room count
    dec = apt.get("declared_rooms")
    meas = apt.get("rooms_count_measured")
    if dec:
        st = "PASS" if abs(float(dec) - meas) < 0.6 else "WARN"
        out.append(_r(st, "מספר חדרים", f"מוצהר {dec:g} חדרים; זוהו {meas} (סלון + חדרי שינה + ממ\"ד + חדר עבודה)."))

    # 4. room dimensions: written vs measured
    worst = []
    for s in unit:
        wd = s.get("written_dimensions_cm") or {}
        mbr = s.get("mbr_cm")
        if not mbr or not wd.get("horizontal") or not wd.get("vertical"):
            continue
        a, b = sorted([max(wd["horizontal"]), max(wd["vertical"])])
        dev = max(abs(a - mbr[0]) / a, abs(b - mbr[1]) / b)
        if dev > 0.08:
            worst.append(f"{s.get('name')}: כתוב {a:.0f}×{b:.0f}, נמדד {mbr[0]:.0f}×{mbr[1]:.0f}")
    checked = sum(1 for s in unit if (s.get("written_dimensions_cm") or {}).get("horizontal")
                  and (s.get("written_dimensions_cm") or {}).get("vertical"))
    if checked:
        out.append(_r("WARN" if worst else "PASS", "מידות חדרים כתובות מול נמדדות",
                      ("סטייה מעל 8%: " + "; ".join(worst) + " (חלל לא מלבני או חלוקה משוערת).") if worst
                      else f"{checked} חדרים — המידות הכתובות תואמות לגאומטריה (±8%)."))

    # 5. ממ"ד
    mamads = [s for s in unit if s.get("type") == "safe_room"]
    if not mamads:
        out.append(_r("WARN", "ממ\"ד", "לא זוהה ממ\"ד בתוויות התכנית."))
    for s in mamads:
        m = s.get("mamad") or {}
        issues = []
        t = m.get("min_wall_thickness_cm")
        if t is not None and t < 18.5:  # 20 cm with ~1.5 cm measurement tolerance
            issues.append(f"עובי קיר מינימלי שנמדד {t:.0f} ס\"מ < 20")
        if not m.get("has_door"):
            issues.append("לא זוהתה דלת")
        if not m.get("has_window"):
            issues.append("לא זוהה חלון")
        walls = ", ".join(f"{k} {v:.0f}" for k, v in (m.get("wall_thickness_cm") or {}).items())
        msg = ("; ".join(issues) + ". " if issues else "") + f"עובי קירות (ס\"מ): {walls or 'לא נמדד'}."
        out.append(_r("WARN" if issues else "PASS", f"ממ\"ד ({s.get('name')})", msg))

    # 6. topology
    ent = apt.get("entrance_space_id")
    topo = sheet.get("topology", [])
    ids = {s["id"] for s in unit if s.get("type") in INTERIOR_TYPES | OUTDOOR_TYPES}
    if not ent:
        out.append(_r("WARN", "כניסה ראשית", "דלת הכניסה לדירה לא זוהתה — מדדי עומק ופרטיות יחושבו ללא נקודת כניסה."))
    else:
        adj = {}
        for e in topo:
            adj.setdefault(e["source"], set()).add(e["target"])
            adj.setdefault(e["target"], set()).add(e["source"])
        seen, stack = {"EXT"}, ["EXT"]
        while stack:
            u = stack.pop()
            for v in adj.get(u, ()):
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        lost = [s.get("name") or s["id"] for s in unit if s["id"] in ids and s["id"] not in seen]
        out.append(_r("WARN" if lost else "PASS", "רציפות טופולוגית",
                      f"לא נמצא מסלול מהכניסה אל: {', '.join(lost)}." if lost
                      else f"כל {len(ids)} החללים נגישים מהכניסה (רוחב דלת כניסה {apt.get('main_entrance_width_cm')} ס\"מ)."))

    # 7. coverage
    unm = sheet.get("unmapped_labels") or []
    if unm:
        out.append(_r("WARN", "שיוך תוויות", f"תוויות שלא שויכו לחלל: {', '.join(unm)}."))
    inferred = [s for s in unit if s.get("name_inferred")]
    if inferred:
        out.append(_r("PASS", "חללים ללא תווית",
                      f"{len(inferred)} חללים ללא שם בתכנית סווגו גאומטרית: "
                      + ", ".join(f"{s['name']} ({s['area_sqm']} מ\"ר)" for s in inferred) + "."))
    north = sheet.get("north") or {}
    out.append(_r("PASS" if north.get("present") else "WARN", "חץ צפון",
                  f"כיוון צפון {north.get('north_direction_deg')}° — כיווניות חלונות חושבה." if north.get("present")
                  else "לא זוהה חץ צפון בגיליון — כיווניות ואוורור צולב לא חושבו."))
    return out
