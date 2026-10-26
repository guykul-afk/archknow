import fitz

def find_residential_metric(filepath):
    print(f"Searching: {filepath}")
    doc = fitz.open(filepath)
    matches = []
    
    for page_num in range(len(doc)):
        text = doc[page_num].get_text()
        first_lines = text.split('\n')[:5]
        for line in first_lines:
            if "RESIDENTIAL" in line.upper() or "HOUSE" in line.upper() or "APARTMENT" in line.upper() or "HOUSING" in line.upper() or "DOMESTIC" in line.upper():
                matches.append((page_num + 1, line.strip()))
                break
                
    print(f"Found {len(matches)} matching pages.")
    for page, title in matches:
        print(f"Page {page}: {title}")

if __name__ == "__main__":
    find_residential_metric("preview-9781000449549_A42256746.pdf")
