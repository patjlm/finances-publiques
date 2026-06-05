#!/usr/bin/env python3
"""
Grouped bar chart: Dépenses vs recettes par régime de retraite (2024)
Shows the structural gap per regime, with CAS Pensions revenue split
into "cotisations au taux privé" and "surcotisation budgétaire".

Sources:
- COR Rapport annuel juin 2025
- Cour des comptes, NEB CAS Pensions 2024
- CCSS mai 2026
- Sénat, rapport PLF 2025
- URSSAF (taux privé 16.58%)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

# --- Data (2024, Md EUR) ---
regimes = [
    "Privé\n(CNAV +\nAGIRC-ARRCO)",
    "Fonctionnaires\nd'État\n(CAS Pensions)",
    "CNRACL\n(territ. / hosp.)",
    "Régimes\nspéciaux",
]

depenses = [259.0, 68.2, 27.5, 11.0]

# Revenue breakdown:
# For each regime: [cotisations "normales", surcotisation/subvention État, gap non couvert]
# "Cotisations normales" = ce que le régime recevrait avec un taux employeur comparable au privé
cotis_normales = [255.0, 20.0, 23.8, 5.1]
surcotisation = [0.0, 44.7, 0.0, 5.9]  # CAS: 64.7 - 20 = 44.7 surcotis; Spéciaux: subvention État
gap_non_couvert = [4.0, 3.5, 3.7, 0.0]  # Déficits résiduels

# --- Plot ---
plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(12, 7))

y_pos = np.arange(len(regimes))
bar_height = 0.35

# Dépenses bars (top)
bars_dep = ax.barh(y_pos - bar_height/2, depenses, bar_height,
                   color="#2171b5", edgecolor="white", linewidth=1.5,
                   label="Dépenses (pensions versées)")

# Revenue stacked bars (bottom)
bars_cotis = ax.barh(y_pos + bar_height/2, cotis_normales, bar_height,
                     color="#41ab5d", edgecolor="white", linewidth=1.5,
                     label="Cotisations (taux comparable au privé)")

bars_surcot = ax.barh(y_pos + bar_height/2, surcotisation, bar_height,
                      left=cotis_normales, color="#e6550d", edgecolor="white",
                      linewidth=1.5,
                      label="Surcotisation État / subvention directe")

bars_gap = ax.barh(y_pos + bar_height/2, gap_non_couvert, bar_height,
                   left=[c + s for c, s in zip(cotis_normales, surcotisation)],
                   color="#d62728", edgecolor="white", linewidth=1.5,
                   hatch="///", alpha=0.7,
                   label="Déficit non couvert")

# Value labels on dépenses bars
for i, (bar, val) in enumerate(zip(bars_dep, depenses)):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
            f"{val:.0f} Md€", va="center", fontsize=10, fontweight="bold",
            color="#2171b5")

# Value labels on revenue bars
for i in range(len(regimes)):
    total_rev = cotis_normales[i] + surcotisation[i] + gap_non_couvert[i]
    y = y_pos[i] + bar_height/2

    # Label cotisations normales
    if cotis_normales[i] > 15:
        ax.text(cotis_normales[i]/2, y, f"{cotis_normales[i]:.0f}",
                va="center", ha="center", fontsize=8.5, fontweight="bold",
                color="white")

    # Label surcotisation
    if surcotisation[i] > 3:
        mid = cotis_normales[i] + surcotisation[i]/2
        ax.text(mid, y, f"{surcotisation[i]:.0f}",
                va="center", ha="center", fontsize=8.5, fontweight="bold",
                color="white")

    # Label gap
    if gap_non_couvert[i] > 2:
        mid = cotis_normales[i] + surcotisation[i] + gap_non_couvert[i]/2
        ax.text(mid, y, f"-{gap_non_couvert[i]:.1f}",
                va="center", ha="center", fontsize=8, fontweight="bold",
                color="#d62728")

# Annotations for CAS Pensions
ax.annotate("78,28 % taux employeur\n(vs 16,58 % privé)",
            xy=(cotis_normales[1] + surcotisation[1], y_pos[1] + bar_height/2),
            xytext=(cotis_normales[1] + surcotisation[1] + 25, y_pos[1] + bar_height*1.8),
            fontsize=8.5, color="#e6550d", fontstyle="italic",
            arrowprops=dict(arrowstyle="->", color="#e6550d", lw=1.2))

# Y axis
ax.set_yticks(y_pos)
ax.set_yticklabels(regimes, fontsize=10.5)
ax.invert_yaxis()

# X axis
ax.set_xlim(0, 300)
ax.set_xlabel("Milliards d'euros (2024)", fontsize=11)

# Title
fig.suptitle("Retraites : dépenses vs recettes par régime",
             fontsize=15, fontweight="bold", y=0.97)
ax.set_title(
    "Le privé s'autofinance — le CAS Pensions repose sur une surcotisation budgétaire",
    fontsize=10.5, color="#555555", pad=14)

# Legend
legend = ax.legend(loc="lower right", fontsize=9, frameon=True, fancybox=True,
                   ncol=2)

# Footnote
fig.text(0.5, 0.01,
         "Note : l'État étant déficitaire de 124 Md€, le financement budgétaire provient en partie de l'emprunt.\n"
         "Sources : COR, Rapport annuel juin 2025 ; Cour des comptes, NEB Pensions 2024 ; "
         "CCSS mai 2026 ; Sénat PLF 2025 ; URSSAF",
         ha="center", va="bottom", fontsize=7.5, fontstyle="italic",
         color="#888888")

plt.tight_layout(rect=[0, 0.06, 1, 0.93])

# Save
output = Path(__file__).with_suffix(".png")
fig.savefig(output, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved: {output}")
plt.close()
