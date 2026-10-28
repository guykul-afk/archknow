import json
import matplotlib.pyplot as plt

with open(r"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\hafetz44_extracted_plans.json", encoding="utf-8") as f:
    plans = json.load(f)

for pname in ["typical", "penthouse", "ground"]:
    fig, ax = plt.subplots(figsize=(22, 10), dpi=200)
    for wp in plans[pname]["wall_polys"]:
        ext = wp["exterior"]
        xs = [p[0] for p in ext] + [ext[0][0]]
        ys = [p[1] for p in ext] + [ext[0][1]]
        ax.fill(xs, ys, color="#94a3b8", alpha=0.5)
        ax.plot(xs, ys, color="#1e293b", lw=1.0)
    for s in plans[pname]["cad_lines"]:
        ax.plot([s[0], s[2]], [s[1], s[3]], color="#0284c7", lw=0.6)
    ax.set_xlim(-16, 17)
    ax.set_ylim(5.5, -5.5) # Invert Y so North (-Y) is at top, matching CAD sheet!
    ax.set_aspect("equal")
    ax.grid(True, which="both", color="#cbd5e1", linestyle="--", lw=0.4)
    ax.set_xticks(range(-16, 18, 1))
    ax.set_yticks([round(y * 0.5, 1) for y in range(-11, 12)])
    ax.set_title(f"{pname.upper()} CAD FURNITURE & WALL GRID (Meters)")
    out_p = rf"C:\Users\User\.gemini\antigravity\brain\ef5d209e-79a1-4a68-bf81-403c83c8182e\scratch\hafetz44\crops\cad_diag\furn_grid_{pname}.png"
    plt.tight_layout()
    plt.savefig(out_p)
    plt.close()
    print("Saved", out_p)
