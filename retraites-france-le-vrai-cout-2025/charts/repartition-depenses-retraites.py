#!/usr/bin/env python3
"""
Pie/donut chart: Repartition des depenses de retraite par regime (2024)
Data: COR, Rapport annuel juin 2025
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# --- Data ---
labels = [
    "CNAV\n(regime general\n+ independants)",
    "AGIRC-ARRCO\n(complementaire\nprive)",
    "CAS Pensions / SRE\n(fonctionnaires\nEtat)",
    "CNRACL\n(fonctionnaires\nterritoriaux /\nhospitaliers)",
    "Regimes speciaux\n(SNCF, RATP,\nmarins...)",
    "FSV et\ntransferts",
    "Autres\n(IRCANTEC,\nRAFP, FSPOEIE)",
]
values = [160.9, 98.1, 62.9, 27.5, 11.0, 7.5, 6.6]
total = sum(values)  # ~374.5 displayed, but total consolide is ~406.9

# Colors: varied palette for better readability
colors = [
    "#2171b5",  # CNAV - dark blue
    "#41ab5d",  # AGIRC-ARRCO - green
    "#d94801",  # CAS Pensions - orange-red (emphasis)
    "#6a51a3",  # CNRACL - purple
    "#e6ab02",  # Regimes speciaux - gold
    "#7fcdbb",  # FSV - teal
    "#bdbdbd",  # Autres - gray
]

# Legend labels with amounts
legend_labels = [
    f"CNAV (regime general + independants) — {values[0]:.1f} Md",
    f"AGIRC-ARRCO (complementaire prive) — {values[1]:.1f} Md",
    f"CAS Pensions / SRE (fonctionnaires Etat) — {values[2]:.1f} Md",
    f"CNRACL (territoriaux / hospitaliers) — {values[3]:.1f} Md",
    f"Regimes speciaux (SNCF, RATP, marins...) — {values[4]:.1f} Md",
    f"FSV et transferts — {values[5]:.1f} Md",
    f"Autres (IRCANTEC, RAFP, FSPOEIE) — {values[6]:.1f} Md",
]

# --- Style ---
plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(9, 8))

# Donut chart
wedges, texts, autotexts = ax.pie(
    values,
    labels=None,
    autopct=lambda pct: f"{pct:.1f} %\n({pct * total / 100:.0f} Md)",
    startangle=90,
    colors=colors,
    pctdistance=0.78,
    wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2),
    textprops=dict(fontsize=9),
)

# Style autopct text
for autotext in autotexts:
    autotext.set_fontsize(8.5)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

# CAS Pensions label in darker color for readability
autotexts[2].set_color("white")

# Add legend on the right
ax.legend(
    wedges,
    legend_labels,
    title="Regimes",
    loc="center left",
    bbox_to_anchor=(1.0, 0.5),
    fontsize=9,
    title_fontsize=10,
    frameon=True,
    fancybox=True,
    shadow=False,
)

# Center circle text
ax.text(
    0, 0,
    f"~{total:.0f} Md\n13,9 % PIB",
    ha="center", va="center",
    fontsize=14, fontweight="bold",
    color="#333333",
)

# Title
fig.suptitle(
    "Repartition des depenses de retraite par regime (2024)",
    fontsize=15, fontweight="bold", y=0.96,
)
ax.set_title(
    "Total consolide : ~406,9 Md EUR (13,9 % du PIB)",
    fontsize=11, color="#555555", pad=15,
)

# Source
fig.text(
    0.95, 0.02,
    "Source : COR, Rapport annuel juin 2025 — cor-retraites.fr",
    ha="right", va="bottom",
    fontsize=7.5, fontstyle="italic", color="#888888",
)

plt.tight_layout(rect=[0, 0.04, 0.78, 0.94])

# Save
output = Path(__file__).with_suffix(".png")
fig.savefig(output, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved: {output}")
plt.close()
