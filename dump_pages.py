import fitz

doc = fitz.open("architecture-05-00008-v2.pdf")
for i in range(3, 8):  # Pages 4 to 8 (0-indexed: 3 to 7)
    print(f"\n--- PAGE {i+1} ---")
    print(doc[i].get_text())
