# /// script
# dependencies = ["plotly", "kaleido"]
# ///
"""
Diagramme de Sankey : flux de financement des retraites françaises (2024-2025)

Lit les données depuis :
  - flux-financement-retraites-data.json  (montants, descriptions, sources)
  - flux-financement-retraites-sankey.json (nœuds, liens, layout)

Génère :
  - flux-financement-retraites-sankey.png  (export statique, scale=2)
  - Met à jour les blocs JSON embarqués dans flux-financement-retraites-sankey.html

Usage: uv run flux-financement-retraites-sankey.py
"""

import json
import os
from pathlib import Path

import plotly.graph_objects as go

# =============================================================================
# CHROME / KALEIDO PATH
# =============================================================================
for candidate in [
    "/usr/lib64/chromium-browser/headless_shell",
    "/usr/bin/chromium-browser",
    "/usr/bin/chromium",
]:
    if os.path.isfile(candidate):
        os.environ.setdefault("CHROME_PATH", candidate)
        os.environ.setdefault("BROWSER_PATH", candidate)
        break

# =============================================================================
# LOAD DATA
# =============================================================================
script_dir = Path(__file__).parent

data = json.loads(
    (script_dir / "flux-financement-retraites-data.json").read_text(encoding="utf-8")
)
cfg = json.loads(
    (script_dir / "flux-financement-retraites-sankey.json").read_text(encoding="utf-8")
)

# =============================================================================
# BUILD NODE LABELS
# =============================================================================
def node_label(node: dict) -> str:
    """Return the display label for a Sankey node."""
    if "label_override" in node:
        return node["label_override"]
    key = node["amount_key"]
    entry = data[key]
    return f'{entry["label"]} {entry["value_md"]} Md€'


nodes_label = [node_label(n) for n in cfg["nodes"]]
nodes_color = [n["color"] for n in cfg["nodes"]]
nodes_x = [n["x"] for n in cfg["nodes"]]
nodes_y = [n["y"] for n in cfg["nodes"]]

# =============================================================================
# BUILD LINKS
# =============================================================================
link_src = [lnk["source_node_id"] for lnk in cfg["links"]]
link_tgt = [lnk["target_node_id"] for lnk in cfg["links"]]
link_val = [data[lnk["amount_key"]]["value_md"] for lnk in cfg["links"]]
link_color = [lnk["color"] for lnk in cfg["links"]]
link_label = [data[lnk["amount_key"]]["label"] for lnk in cfg["links"]]

# =============================================================================
# ASSERT NODE BALANCE (in == out for all intermediate nodes)
# =============================================================================
_in: dict[int, float] = {}
_out: dict[int, float] = {}
for lnk in cfg["links"]:
    val = data[lnk["amount_key"]]["value_md"]
    _out[lnk["source_node_id"]] = _out.get(lnk["source_node_id"], 0) + val
    _in[lnk["target_node_id"]] = _in.get(lnk["target_node_id"], 0) + val

for idx, node in enumerate(cfg["nodes"]):
    i_sum = _in.get(idx, 0)
    o_sum = _out.get(idx, 0)
    if i_sum > 0 and o_sum > 0:
        assert i_sum + 0.05 >= o_sum, (
            f"Node {idx} underfunded: in={i_sum:.2f} < out={o_sum:.2f}, "
            f"diff={i_sum - o_sum:+.2f} — {node_label(node)}"
        )

# =============================================================================
# BUILD FIGURE
# =============================================================================
fig = go.Figure(
    data=[
        go.Sankey(
            arrangement="snap",
            node=dict(
                pad=25,
                thickness=20,
                line=dict(color="white", width=1),
                label=nodes_label,
                color=nodes_color,
                x=nodes_x,
                y=nodes_y,
                hovertemplate="%{label}<extra></extra>",
            ),
            link=dict(
                source=link_src,
                target=link_tgt,
                value=link_val,
                color=link_color,
                label=link_label,
                hovertemplate="%{label}<extra></extra>",
            ),
        )
    ]
)

# =============================================================================
# LAYOUT
# =============================================================================
lay = cfg["layout"]
budget_direct = 12 + 45 + 6 + 8 + 1.7 + 8 + 10 + 4.7  # 95.4 Md€ direct Budget → retraites
budget_indirect = 14.4  # via dotations collectivités → CNRACL FPT
part_dette = round((budget_direct + budget_indirect) * 124 / 443)

fig.update_layout(
    title=dict(
        text=(
            f"<b>{lay['title']}</b>"
            "<br><sup>"
            f"Total pensions 407 Md€ · Pensions publiques 107 Md€ · "
            f"Budget État → retraites : {budget_direct:.1f} Md€ directs + {budget_indirect} Md€ via collectivités · "
            "Déficit officiel COR : -1,7 Md€"
            "</sup>"
        ),
        font=dict(size=16),
        x=0.5,
        xanchor="center",
    ),
    font=dict(size=10, family="Liberation Sans, Arial, sans-serif"),
    width=lay["width"],
    height=lay["height"],
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(**lay["margin"]),
    annotations=[
        dict(
            text=ann["text"],
            xref=ann["xref"],
            yref=ann["yref"],
            x=ann["x"],
            y=ann["y"],
            showarrow=ann["showarrow"],
            font=dict(**ann["font"]),
            xanchor=ann["xanchor"],
        )
        for ann in lay["annotations"]
    ],
)

# =============================================================================
# SAVE PNG
# =============================================================================
output_png = script_dir / "flux-financement-retraites-sankey.png"
try:
    fig.write_image(str(output_png), scale=2)
    print(f"Saved: {output_png}")
except Exception as e:
    print(f"PNG export failed ({e.__class__.__name__}: {e}), skipping.")
