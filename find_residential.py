import fitz

def find_residential_sections(filepath):
    print(f"Searching: {filepath}")
    doc = fitz.open(filepath)
    matches = []
    
    for page_num in range(len(doc)):
        text = doc[page_num].get_text()
        # Look for titles like "HOUSES", "RESIDENTIAL", "APARTMENTS" at the top of pages
        first_lines = text.split('\n')[:5]
        for line in first_lines:
            if "RESIDENTIAL" in line.upper() or "HOUSE" in line.upper() or "APARTMENT" in line.upper():
                matches.append((page_num + 1, line.strip()))
                break
                
    print(f"Found {len(matches)} matching pages.")
    for page, title in matches[:20]:
        print(f"Page {page}: {title}")

if __name__ == "__main__":
    find_residential_sections("03. Architect_s Data.pdf")
