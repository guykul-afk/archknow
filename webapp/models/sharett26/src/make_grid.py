import fitz
doc = fitz.open()
p = doc.new_page(width=1024, height=1024)
p.insert_image(fitz.Rect(0, 0, 1024, 1024), filename=r"C:\Users\User\.gemini\antigravity\brain\71931cc9-7058-41f3-a9f0-80549e5c535b\scratch\closeup_z19.png")
for i in range(0, 1025, 64):
    col = (1, 0, 0) if i == 512 else (0, 1, 1)
    w = 2 if i == 512 else 0.7
    p.draw_line((i, 0), (i, 1024), color=col, width=w)
    p.draw_line((0, i), (1024, i), color=col, width=w)
    p.insert_text((i + 2, 15), str(i), color=(1, 1, 0), fontsize=10)
    p.insert_text((4, i + 12), str(i), color=(1, 1, 0), fontsize=10)
p.get_pixmap().save(r"C:\Users\User\.gemini\antigravity\brain\71931cc9-7058-41f3-a9f0-80549e5c535b\scratch\closeup_grid.png")
print("Saved closeup_grid.png")
