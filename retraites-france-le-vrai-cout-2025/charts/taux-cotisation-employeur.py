#!/usr/bin/env python3
"""
Horizontal bar chart: Taux de cotisation employeur retraite — Etat vs prive
Data: URSSAF, Decret n2025-61 du 22/01/2025 (Legifrance)
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# --- Data ---
categories = [
    "Secteur prive\n(base + complementaire)",
    "CNRACL\n(territoriaux / hospitaliers)\n2024",
    "CNRACL\n(territoriaux / hospitaliers)\nd'ici 2028",
    "Fonctionnaires civils\nEtat (2025)",
    "Militaires",
]
values = [16.58, 34.65, 43.65, 78.28, 126.07]

# Color gradient: green (normal) -> orange -> red (extreme)
colors = ["#2ca02c", "#f0a830", "#e07020", "#d62728", "#8b0000"]

# --- Style ---
plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(10, 5.5))

y_pos = np.arange(len(categories))
bars = ax.barh(y_pos, values, color=colors, edgecolor="white", height=0.65)

# Add value labels
for bar, val in zip(bars, values):
    x = bar.get_width()
    ax.text(
        x + 1.5, bar.get_y() + bar.get_height() / 2,
        f"{val:.2f} %",
        va="center", ha="left",
        fontsize=12, fontweight="bold",
        color="#333333",
    )

# Multiplier annotations
ref = values[0]
for i, val in enumerate(values):
    if i == 0:
        continue
    ratio = val / ref
    ax.text(
        val + 1.5, y_pos[i] + 0.28,
        f"x {ratio:.1f}",
        va="center", ha="left",
        fontsize=9, fontstyle="italic",
        color="#888888",
    )

ax.set_yticks(y_pos)
ax.set_yticklabels(categories, fontsize=10)
ax.set_xlabel("Taux de cotisation employeur retraite (%)", fontsize=11)
ax.set_xlim(0, 145)
ax.invert_yaxis()

# Vertical reference line for prive
ax.axvline(x=ref, color="#2ca02c", linestyle="--", linewidth=1, alpha=0.5)
ax.text(
    ref + 0.5, len(categories) - 0.15,
    f"Taux prive : {ref} %",
    fontsize=8, color="#2ca02c", fontstyle="italic",
    va="top",
)

# Remove top and right spines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Title
fig.suptitle(
    "Taux de cotisation employeur retraite : Etat vs prive",
    fontsize=14, fontweight="bold", y=0.98,
)
ax.set_title(
    "L'Etat cotise jusqu'a 4,7 fois plus que le secteur prive — et le taux augmente chaque annee",
    fontsize=10, color="#555555", pad=12,
)

# Source
fig.text(
    0.95, 0.01,
    "Sources : URSSAF ; Decret n°2025-61 du 22/01/2025 (Legifrance)",
    ha="right", va="bottom",
    fontsize=7.5, fontstyle="italic", color="#888888",
)

plt.tight_layout(rect=[0, 0.04, 1, 0.94])

# Save
output = Path(__file__).with_suffix(".png")
fig.savefig(output, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved: {output}")
plt.close()
