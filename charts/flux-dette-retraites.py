#!/usr/bin/env python3
"""
Flow diagram: Dette -> Budget Etat -> Salaires fonctionnaires -> Cotisations -> CAS Pensions -> Pensions
Simplified arrow/box diagram using matplotlib patches and arrows.
Data: DGFiP (execution 2025), Legifrance, Cour des comptes (NEB Pensions 2024)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from pathlib import Path

# --- Style ---
plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis("off")
ax.set_aspect("equal")

# --- Box definitions ---
# Each box: (x_center, y_center, width, height, label, sublabel, color, text_color)
boxes = [
    (1.5, 6.5, 2.4, 1.0,
     "Emprunt / Dette",
     "300 Md€ emis\n(OAT 2025)",
     "#8b0000", "white"),

    (1.5, 4.0, 2.4, 1.2,
     "Budget de l'Etat",
     "Deficit : -124 Md€\nRecettes : 319 Md€\nDepenses : 441 Md€",
     "#d62728", "white"),

    (5.5, 4.0, 2.4, 1.2,
     "Salaires\nfonctionnaires",
     "dont cotisations\nemployeur retraite",
     "#e07020", "white"),

    (9.0, 4.0, 2.0, 1.2,
     "CAS Pensions",
     "Recettes : 65 Md€\nDepenses : 68 Md€",
     "#f0a830", "#333333"),

    (9.0, 1.5, 2.0, 1.0,
     "Pensions versees",
     "~63 Md€\n(fonctionnaires Etat)",
     "#2171b5", "white"),

    (5.5, 1.5, 2.4, 1.0,
     "Taux employeur",
     "78,28 %\n(civils, 2025)",
     "#d62728", "white"),
]

# Draw boxes
for (cx, cy, w, h, title, sub, color, tcolor) in boxes:
    box = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0.1",
        facecolor=color, edgecolor="white", linewidth=2,
        alpha=0.9,
    )
    ax.add_patch(box)
    ax.text(cx, cy + 0.15, title, ha="center", va="center",
            fontsize=10, fontweight="bold", color=tcolor)
    ax.text(cx, cy - 0.28, sub, ha="center", va="center",
            fontsize=7.5, color=tcolor, alpha=0.9)

# --- Arrows ---
arrow_style = "Simple,tail_width=6,head_width=16,head_length=8"
arrow_kwargs = dict(
    arrowstyle=arrow_style,
    color="#555555",
    lw=1.5,
    connectionstyle="arc3,rad=0",
)


def draw_arrow(ax, xy_start, xy_end, label=None, label_offset=(0, 0.2), color="#555555"):
    arrow = FancyArrowPatch(
        xy_start, xy_end,
        arrowstyle=arrow_style,
        color=color, lw=1.5,
        connectionstyle="arc3,rad=0",
        zorder=3,
    )
    ax.add_patch(arrow)
    if label:
        mid_x = (xy_start[0] + xy_end[0]) / 2 + label_offset[0]
        mid_y = (xy_start[1] + xy_end[1]) / 2 + label_offset[1]
        ax.text(mid_x, mid_y, label, ha="center", va="center",
                fontsize=8, color="#555555", fontstyle="italic",
                bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.8))


# Arrow 1: Emprunt -> Budget Etat
draw_arrow(ax, (1.5, 6.0), (1.5, 4.65),
           label="finance le deficit", label_offset=(1.1, 0))

# Arrow 2: Budget Etat -> Salaires
draw_arrow(ax, (2.7, 4.0), (4.3, 4.0),
           label="paie", label_offset=(0, 0.25))

# Arrow 3: Salaires -> CAS Pensions
draw_arrow(ax, (6.7, 4.0), (8.0, 4.0),
           label="cotise (78,28 %)", label_offset=(0, 0.3), color="#d62728")

# Arrow 4: CAS Pensions -> Pensions
draw_arrow(ax, (9.0, 3.4), (9.0, 2.05),
           label="verse", label_offset=(0.6, 0))

# Arrow 5: Rate box -> Arrow 3 (informational)
ax.annotate(
    "",
    xy=(6.7, 3.5), xytext=(6.7, 2.0),
    arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.2, linestyle="--"),
)
ax.text(
    5.5, 2.65,
    "fixe par\ndecret",
    ha="center", va="center",
    fontsize=7.5, color="#d62728", fontstyle="italic",
)

# --- Key insight box ---
insight_text = (
    "L'Etat fixe par decret un taux de cotisation (78,28 %) qui equilibre le CAS Pensions.\n"
    "Mais l'Etat est deficitaire de 124 Md€ — il emprunte pour financer ce taux.\n"
    "Resultat : la dette finance indirectement une partie des retraites."
)
insight_box = FancyBboxPatch(
    (0.5, 0.15), 7.5, 0.85,
    boxstyle="round,pad=0.15",
    facecolor="#fff3e0", edgecolor="#e07020", linewidth=1.5,
    alpha=0.9,
)
ax.add_patch(insight_box)
ax.text(
    4.25, 0.57, insight_text,
    ha="center", va="center",
    fontsize=8.5, color="#333333",
    linespacing=1.4,
)

# Title
fig.suptitle(
    "Flux de financement : de la dette aux pensions des fonctionnaires",
    fontsize=14, fontweight="bold", y=0.97,
)
fig.text(
    0.5, 0.935,
    "Comment l'emprunt public finance indirectement les retraites via le CAS Pensions",
    ha="center", va="top",
    fontsize=10, color="#555555",
)

# Source
fig.text(
    0.95, 0.01,
    "Sources : DGFiP (execution 2025) ; Legifrance ; Cour des comptes (NEB Pensions 2024)",
    ha="right", va="bottom",
    fontsize=7.5, fontstyle="italic", color="#888888",
)

plt.tight_layout(rect=[0, 0.03, 1, 0.92])

# Save
output = Path(__file__).with_suffix(".png")
fig.savefig(output, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved: {output}")
plt.close()
