import fitz  # PyMuPDF
import sys

def inspect_pdf(filepath):
    print(f"Inspecting: {filepath}")
    doc = fitz.open(filepath)
    print(f"Total pages: {len(doc)}")
    
    # Print metadata
    print("Metadata:", doc.metadata)
    
    # Print TOC
    toc = doc.get_toc()
    if toc:
        print("Table of Contents:")
        for item in toc[:15]:  # show first 15 items
            print(item)
    else:
        print("No TOC found.")
        
    # Read first page content
    print("\n--- Page 1 text (first 1000 chars) ---")
    page = doc.load_page(0)
    print(page.get_text()[:1000])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        inspect_pdf(sys.argv[1])
    else:
        print("Please provide a PDF filename.")
