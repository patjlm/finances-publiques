#!/usr/bin/env python3
"""
Line/step chart: Evolution du taux de cotisation employeur Etat (fonctionnaires civils)
Data: Legifrance, decrets n2025-61 et n2025-1341
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# --- Data ---
# Confirmed data points
years_confirmed = [2024, 2025, 2026]
rates_confirmed = [74.28, 78.28, 82.28]

# Projected trend (+4 pts/year, dashed)
years_projected = [2026, 2027, 2028, 2029, 2030]
rates_projected = [82.28, 86.28, 90.28, 94.28, 98.28]

# Reference: taux prive
taux_prive = 16.58

# --- Style ---
plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(10, 6))

# Confirmed line (solid, thick)
ax.plot(
    years_confirmed, rates_confirmed,
    color="#d62728", linewidth=2.5, marker="o", markersize=10,
    zorder=5, label="Taux confirme (decrets)",
)

# Projected line (dashed)
ax.plot(
    years_projected, rates_projected,
    color="#d62728", linewidth=2, linestyle="--", marker="o", markersize=7,
    alpha=0.5, zorder=4, label="Projection si +4 pts/an",
)

# Data labels for confirmed points
for x, y in zip(years_confirmed, rates_confirmed):
    ax.annotate(
        f"{y:.2f} %",
        xy=(x, y), xytext=(0, 14),
        textcoords="offset points",
        ha="center", va="bottom",
        fontsize=11, fontweight="bold", color="#d62728",
    )

# Data label for 2030 projection
ax.annotate(
    f"~{rates_projected[-1]:.0f} % ?",
    xy=(years_projected[-1], rates_projected[-1]),
    xytext=(0, 14),
    textcoords="offset points",
    ha="center", va="bottom",
    fontsize=10, fontweight="bold", color="#d62728", alpha=0.6,
)

# Horizontal reference line: taux prive
ax.axhline(
    y=taux_prive, color="#2ca02c", linestyle="-", linewidth=1.5, alpha=0.7,
)
ax.text(
    2030.2, taux_prive + 1.5,
    f"Taux employeur prive : {taux_prive} %",
    fontsize=9, color="#2ca02c", fontstyle="italic",
    va="bottom", ha="right",
)

# Fill between the two rates to show the gap
all_years = list(range(2024, 2031))
all_rates = [74.28, 78.28, 82.28, 86.28, 90.28, 94.28, 98.28]
ax.fill_between(
    all_years, taux_prive, all_rates,
    alpha=0.08, color="#d62728",
)

# Annotation: gap label
mid_year = 2027
mid_rate_top = 86.28
mid_rate_bot = taux_prive
ax.annotate(
    "",
    xy=(mid_year, mid_rate_bot + 2), xytext=(mid_year, mid_rate_top - 2),
    arrowprops=dict(arrowstyle="<->", color="#888888", lw=1.5),
)
ax.text(
    mid_year + 0.15, (mid_rate_top + mid_rate_bot) / 2,
    f"Ecart : x {mid_rate_top / mid_rate_bot:.0f}",
    fontsize=9, color="#888888", va="center",
)

# Axes
ax.set_xlabel("Annee", fontsize=11)
ax.set_ylabel("Taux de cotisation employeur (%)", fontsize=11)
ax.set_xlim(2023.5, 2030.5)
ax.set_ylim(0, 110)
ax.set_xticks(range(2024, 2031))
ax.set_yticks(range(0, 111, 10))

# Decree annotations
ax.annotate(
    "Decret\nn°2025-61",
    xy=(2025, 78.28), xytext=(2025.4, 60),
    fontsize=8, color="#555555",
    arrowprops=dict(arrowstyle="->", color="#555555", lw=1),
    ha="left",
)
ax.annotate(
    "Decret\nn°2025-1341",
    xy=(2026, 82.28), xytext=(2026.4, 65),
    fontsize=8, color="#555555",
    arrowprops=dict(arrowstyle="->", color="#555555", lw=1),
    ha="left",
)

# Legend
ax.legend(loc="upper left", fontsize=10, frameon=True, fancybox=True)

# Spines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Title
fig.suptitle(
    "Evolution du taux de cotisation employeur Etat",
    fontsize=14, fontweight="bold", y=0.98,
)
ax.set_title(
    "Fonctionnaires civils — +4 points par an, fixe par decret pour combler le deficit du CAS Pensions",
    fontsize=10, color="#555555", pad=12,
)

# Source
fig.text(
    0.95, 0.01,
    "Sources : Legifrance, decrets n°2025-61 et n°2025-1341",
    ha="right", va="bottom",
    fontsize=7.5, fontstyle="italic", color="#888888",
)

plt.tight_layout(rect=[0, 0.04, 1, 0.94])

# Save
output = Path(__file__).with_suffix(".png")
fig.savefig(output, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved: {output}")
plt.close()
