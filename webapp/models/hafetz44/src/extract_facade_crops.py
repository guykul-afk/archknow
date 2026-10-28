import fitz, os

out_dir = r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\crops\facades_detail"
os.makedirs(out_dir, exist_ok=True)

doc2 = fitz.open(r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\pdfs\hafetz44_g9_part2.pdf")
page2 = doc2[0]
W, H = page2.rect.width, page2.rect.height

crops2 = {
    "facade_west_east": (0.0, 0.02, 0.27, 0.45),
    "facade_north": (0.27, 0.02, 0.62, 0.45),
    "facade_south": (0.62, 0.02, 0.96, 0.45),
    "section_details_left": (0.0, 0.45, 0.35, 0.92),
    "section_bb": (0.35, 0.45, 0.85, 0.92),
}
for name, (x0, y0, x1, y1) in crops2.items():
    r = fitz.Rect(x0 * W, y0 * H, x1 * W, y1 * H)
    pix = page2.get_pixmap(clip=r, dpi=250)
    pix.save(os.path.join(out_dir, f"{name}.jpg"))

doc1 = fitz.open(r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\pdfs\hafetz44_g9_part1.pdf")
page1 = doc1[0]
W1, H1 = page1.rect.width, page1.rect.height

crops1 = {
    "typ_full_dims": (0.31, 0.03, 0.64, 0.48),
    "pent_full_dims": (0.14, 0.03, 0.33, 0.48),
    "roof_plans": (0.01, 0.03, 0.33, 0.92),
}
for name, (x0, y0, x1, y1) in crops1.items():
    r = fitz.Rect(x0 * W1, y0 * H1, x1 * W1, y1 * H1)
    pix = page1.get_pixmap(clip=r, dpi=250)
    pix.save(os.path.join(out_dir, f"{name}.jpg"))

print("Done!")
