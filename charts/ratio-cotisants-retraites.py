#!/usr/bin/env python3
"""
Bar chart: Ratio cotisants/retraites par regime (2023)
Data: COR Rapport annuel juin 2025, CNRACL, L'Assurance Retraite, AGIRC-ARRCO
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# --- Data (2023) ---
regimes = [
    "AGIRC-ARRCO\n(compl. prive)",
    "Tous regimes\nconfondus",
    "CNRACL\n(territ./hosp.)",
    "CNAV\n(base prive)",
    "Fonctionnaires\nd'Etat (CAS)",
    "Marins\n(ENIM)",
]
ratios = [2.20, 1.79, 1.58, 1.39, 0.80, 0.29]

# Colors: green above 1, orange near 1, red below 1
colors = []
for r in ratios:
    if r >= 1.5:
        colors.append("#2ca02c")  # green - healthy
    elif r >= 1.0:
        colors.append("#e6ab02")  # gold - tight
    else:
        colors.append("#d62728")  # red - deficit

# --- Plot ---
plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.barh(range(len(regimes)), ratios, color=colors, height=0.6,
               edgecolor="white", linewidth=1.5)

# Labels on bars
for i, (bar, ratio) in enumerate(zip(bars, ratios)):
    x_pos = bar.get_width() + 0.05
    label = f"{ratio:.2f}"
    if ratio < 1:
        label += "  (plus de retraites que d'actifs)"
    ax.text(x_pos, i, label, va="center", fontsize=11, fontweight="bold",
            color=colors[i])

# Reference line at 1.0
ax.axvline(x=1.0, color="#888888", linestyle="--", linewidth=1.5, alpha=0.7)
ax.text(1.02, len(regimes) - 0.3, "Seuil d'equilibre : 1 cotisant par retraite",
        fontsize=8.5, color="#888888", fontstyle="italic", va="bottom")

# Y axis
ax.set_yticks(range(len(regimes)))
ax.set_yticklabels(regimes, fontsize=10)
ax.invert_yaxis()

# X axis
ax.set_xlim(0, 2.8)
ax.set_xlabel("Nombre de cotisants par retraite", fontsize=11)

# Title
fig.suptitle("Ratio cotisants / retraites par regime (2023)",
             fontsize=15, fontweight="bold", y=0.96)
ax.set_title(
    "Moins d'un actif par retraite dans la fonction publique d'Etat depuis 2012",
    fontsize=10.5, color="#555555", pad=12)

# Source
fig.text(0.95, 0.02,
         "Sources : COR, Rapport annuel juin 2025 ; CNRACL ; "
         "L'Assurance Retraite ; AGIRC-ARRCO",
         ha="right", va="bottom", fontsize=7.5, fontstyle="italic",
         color="#888888")

plt.tight_layout(rect=[0, 0.05, 1, 0.92])

# Save
output = Path(__file__).with_suffix(".png")
fig.savefig(output, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved: {output}")
plt.close()
