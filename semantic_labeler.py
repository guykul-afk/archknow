import re

def normalize_hebrew_text(text: str) -> str:
    """
    Normalizes Hebrew text for room classification:
    - Lowers casing (if any English characters exist).
    - Removes punctuation like double-quotes, single-quotes, periods, hyphens.
    - Resolves abbreviations like 'ח.' or 'ח ' to 'חדר'.
    - Collapses multiple spaces.
    """
    if not text:
        return ""
    
    # Trim and lowercase
    text = text.strip().lower()
    
    # Replace common room abbreviations
    # 'ח.' or 'ח ' at start of words to 'חדר'
    text = re.sub(r'\bח\.\s*', 'חדר ', text)
    text = re.sub(r'\bח\s+', 'חדר ', text)
    
    # Replace special forms of ממ"ד / מ.מ.ד
    text = re.sub(r'מ\.מ\.ד', 'ממד', text)
    text = re.sub(r'ממ"ד', 'ממד', text)
    text = re.sub(r'ממ\'ד', 'ממד', text)
    
    # Remove remaining punctuation except spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Computes the standard Levenshtein edit distance between two strings.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (0 if c1 == c2 else 1)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def similarity_ratio(s1: str, s2: str) -> float:
    """
    Returns a similarity ratio between 0.0 and 1.0 based on Levenshtein distance.
    """
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    dist = levenshtein_distance(s1, s2)
    return 1.0 - (dist / max_len)

# Define category rules
# We define reference phrases for fuzzy matching and strong keywords for rule-based heuristics
CATEGORIES = {
    'bedroom_master': {
        'keywords': ['הורים', 'סוויטת הורים'],
        'references': ['חדר שינה הורים', 'חדר הורים', 'הורים', 'סוויטת הורים']
    },
    'bedroom': {
        'keywords': ['שינה', 'ילדים', 'מגורים'],
        'references': ['חדר שינה', 'חדר ילדים', 'חדר שינה ילדים', 'חדר', 'חצי חדר', 'חדר עבודה']
    },
    'safe_room': {
        'keywords': ['ממד', 'מרחב מוגן', 'ממ ד'],
        'references': ['ממד', 'מרחב מוגן', 'מרחב מוגן דירתי']
    },
    'living_room': {
        'keywords': ['סלון', 'דיור', 'מגורים'],
        'references': ['סלון', 'חדר דיור', 'פינת דיור', 'חלל מגורים']
    },
    'kitchen': {
        'keywords': ['מטבח', 'בישול'],
        'references': ['מטבח', 'פינת בישול', 'מטבחון']
    },
    'bathroom': {
        'keywords': ['רחצה', 'אמבטיה', 'מקלחת', 'שירותים', 'שרותים', 'נוחיות', 'אורחים'],
        'references': ['חדר רחצה', 'אמבטיה', 'מקלחת', 'שירותים', 'שירותי אורחים', 'מקלחת הורים', 'חדר אמבטיה']
    },
    'balcony': {
        'keywords': ['מרפסת', 'גזוזטרא', 'שמש'],
        'references': ['מרפסת שמש', 'מרפסת', 'מרפסת שירות', 'גזוזטרא']
    },
    'corridor': {
        'keywords': ['מסדרון', 'מעבר', 'פרוזדור', 'מבואה'],
        'references': ['מסדרון', 'מעבר', 'פרוזדור', 'מבואה', 'פרוזדר', 'הול']
    },
    'utility': {
        'keywords': ['שירות', 'שרות', 'כביסה', 'חצי חדר'],
        'references': ['חדר שירות', 'חדר שרות', 'שירות', 'שרות', 'כביסה', 'ח. שירות', 'ח. שרות']
    }
}

def classify_room(text: str) -> str:
    """
    Classifies a Hebrew room name into one of the standard categories:
    'living_room', 'kitchen', 'bedroom', 'bedroom_master', 'safe_room', 'bathroom', 'balcony', 'unknown'
    """
    if not text:
        return 'unknown'
        
    normalized = normalize_hebrew_text(text)
    if not normalized:
        return 'unknown'
    
    # 1. First-pass rule-based routing using high-confidence keyword markers
    # Master bedroom has high priority if 'הורים' (parents) is present
    if 'הורים' in normalized:
        # Check if it's bathroom related (e.g. מקלחת הורים, שירותי הורים)
        if any(kw in normalized for kw in ['מקלחת', 'רחצה', 'אמבטיה', 'שירותים', 'שרותים']):
            return 'bathroom'
        return 'bedroom_master'
        
    # Safe room (ממד) has high priority
    if 'ממד' in normalized or 'מרחב מוגן' in normalized:
        return 'safe_room'
        
    # Living room
    if 'סלון' in normalized or 'חדר דיור' in normalized:
        return 'living_room'
        
    # Kitchen
    if 'מטבח' in normalized:
        return 'kitchen'
        
    # Balcony
    if 'מרפסת' in normalized:
        return 'balcony'
        
    # Bathroom
    if any(kw in normalized for kw in ['מקלחת', 'אמבטיה', 'רחצה', 'שירותים', 'שרותים', 'אורחים']):
        return 'bathroom'

    # Corridor / Passage
    if any(kw in normalized for kw in ['מסדרון', 'מעבר', 'פרוזדור', 'מבואה', 'פרוזדר', 'הול']):
        return 'corridor'

    # Utility Room
    if any(kw in normalized for kw in ['שירות', 'שרות', 'כביסה']):
        return 'utility'

    # 2. Fuzzy Matching fallback
    best_category = 'unknown'
    best_score = 0.0
    
    for category, config in CATEGORIES.items():
        # Avoid overriding high-confidence logic for bedroom/bedroom_master
        if category == 'bedroom_master' and 'הורים' not in normalized:
            continue
            
        for ref in config['references']:
            # Direct match
            if normalized == ref:
                return category
            
            # Fuzzy match score
            score = similarity_ratio(normalized, ref)
            if score > best_score:
                best_score = score
                best_category = category
                
    # Confidence threshold for fuzzy matching
    if best_score >= 0.6:
        return best_category
        
    return 'unknown'

if __name__ == '__main__':
    # Test suite
    test_cases = [
        ('ח. שינה', 'bedroom'),
        ('חדר שינה הורים', 'bedroom_master'),
        ('סלון', 'living_room'),
        ('מטבח', 'kitchen'),
        ('ממד', 'safe_room'),
        ('ממ"ד', 'safe_room'),
        ('מרפסת שמש', 'balcony'),
        ('אמבטיה', 'bathroom'),
        ('מקלחת', 'bathroom'),
        ('שירותי אורחים', 'bathroom'),
        ('ח. רחצה', 'bathroom'),
        ('מקלחת הורים', 'bathroom'),
        ('סתם טקסט לא קשור', 'unknown'),
        ('', 'unknown'),
    ]
    
    print("Running classification tests:")
    passed = 0
    for input_text, expected in test_cases:
        actual = classify_room(input_text)
        status = "PASSED" if actual == expected else "FAILED"
        print(f"Input: '{input_text}' -> Expected: '{expected}', Got: '{actual}' [{status}]")
        if actual == expected:
            passed += 1
            
    print(f"\nPassed {passed}/{len(test_cases)} tests.")
    assert passed == len(test_cases), "Some test cases failed!"
