import fitz, math, os
from PIL import Image, ImageDraw

PT_PER_M = 72.0 / 25.4 * 10.0  # 28.3464567 pt/m
p1_path = r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\pdfs\hafetz44_g9_part1.pdf"
out_dir = r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\crops\cad_diag"
os.makedirs(out_dir, exist_ok=True)

doc1 = fitz.open(p1_path)
page1 = doc1[0]
rot1 = page1.rotation_matrix
W1, H1 = page1.rect.width, page1.rect.height

# Let's find the exact bounding box of each of the 6 plans in Part 1 by finding the blue concrete fills (0.0, 0.32, 1.0)!
blue_pts = []
for d in page1.get_drawings():
    c = tuple(round(x, 2) for x in d['color']) if d.get('color') else None
    f = tuple(round(x, 2) for x in d['fill']) if d.get('fill') else None
    if c == (0.0, 0.32, 1.0) or f == (0.0, 0.32, 1.0):
        r = d['rect'] * rot1
        blue_pts.append((r.x0 / PT_PER_M, r.y0 / PT_PER_M, r.x1 / PT_PER_M, r.y1 / PT_PER_M))

# Cluster blue_pts into floor plan bounding boxes!
clusters = []
for x0, y0, x1, y1 in blue_pts:
    cx, cy = 0.5*(x0+x1), 0.5*(y0+y1)
    placed = False
    for cl in clusters:
        if (cl[0]-8 <= cx <= cl[2]+8) and (cl[1]-8 <= cy <= cl[3]+8):
            cl[0] = min(cl[0], x0)
            cl[1] = min(cl[1], y0)
            cl[2] = max(cl[2], x1)
            cl[3] = max(cl[3], y1)
            cl[4] += 1
            placed = True
            break
    if not placed:
        clusters.append([x0, y0, x1, y1, 1])

# Merge overlapping clusters
merged = True
while merged:
    merged = False
    for i in range(len(clusters)):
        for j in range(i+1, len(clusters)):
            a, b = clusters[i], clusters[j]
            if not (a[2]+5 < b[0] or b[2]+5 < a[0] or a[3]+5 < b[1] or b[3]+5 < a[1]):
                a[0] = min(a[0], b[0])
                a[1] = min(a[1], b[1])
                a[2] = max(a[2], b[2])
                a[3] = max(a[3], b[3])
                a[4] += b[4]
                clusters.pop(j)
                merged = True
                break
        if merged:
            break

print("Detected Floor Plan Clusters in Part 1 (in meters at 1:100):")
for i, cl in enumerate(sorted(clusters, key=lambda x: (round(x[1]/25), x[0]))):
    print(f"  Cluster {i+1}: X=[{cl[0]:.2f}..{cl[2]:.2f}m] (W={cl[2]-cl[0]:.2f}m), Y=[{cl[1]:.2f}..{cl[3]:.2f}m] (H={cl[3]-cl[1]:.2f}m), blue_draws={cl[4]}")
