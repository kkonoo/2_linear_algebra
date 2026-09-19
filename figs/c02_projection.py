"""02 §1 — 이분 그래프와 사영(projection).

유전자–경로 이분 그래프를 유전자–유전자로 접으면, 큰 경로 하나가 거대한
clique 을 만든다.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *
import networkx as nx
from itertools import combinations

OUT = outdir("c02")

genes = [f"G{i}" for i in range(1, 11)]
# P3 는 유전자 6개가 붙어 있는 '큰 경로'
pathways = {"P1": ["G1", "G2"], "P2": ["G2", "G3", "G4"],
            "P3": ["G4", "G5", "G6", "G7", "G8", "G9"], "P4": ["G9", "G10"]}

B = nx.Graph()
B.add_nodes_from(genes, bipartite=0)
B.add_nodes_from(pathways, bipartite=1)
for p, gs_ in pathways.items():
    B.add_edges_from((g, p) for g in gs_)

P = nx.bipartite.weighted_projected_graph(B, genes)

fig, axes = plt.subplots(1, 2, figsize=(13.8, 5.2), gridspec_kw={"wspace": 0.10})

# ── 왼쪽: 이분 그래프 ─────────────────────────────────────────────────
ax = axes[0]
pos = {}
for i, g in enumerate(genes):
    pos[g] = (0, -i * 0.9)
for i, p in enumerate(pathways):
    pos[p] = (2.6, -(i * 2.6) - 1.4)
nx.draw_networkx_edges(B, pos, ax=ax, edge_color="#C3CED6", width=1.2)
nx.draw_networkx_nodes(B, pos, ax=ax, nodelist=genes, node_color=TEAL,
                       linewidths=0, node_size=420)
nx.draw_networkx_nodes(B, pos, ax=ax, nodelist=list(pathways),
                       node_color=PURPLE, node_shape="s", linewidths=0,
                       node_size=620)
nx.draw_networkx_labels(B, pos, ax=ax, font_size=8, font_color="white",
                        font_weight="bold")
ax.set_title("이분 그래프 — 유전자 10개 · 경로 4개", color=NAVY)
ax.text(0.5, -0.04, f"엣지 {B.number_of_edges()}개",
        transform=ax.transAxes, ha="center", va="top", fontsize=10.5,
        color="#4A4A4A")
ax.margins(0.16); ax.set_axis_off()

# ── 오른쪽: 사영 결과 ─────────────────────────────────────────────────
ax = axes[1]
big = set(pathways["P3"])
posp = nx.spring_layout(P, seed=9, k=0.9)
ecol = [RED if (u in big and v in big) else "#C3CED6" for u, v in P.edges()]
ewid = [1.9 if c == RED else 1.2 for c in ecol]
nx.draw_networkx_edges(P, posp, ax=ax, edge_color=ecol, width=ewid, alpha=0.9)
nx.draw_networkx_nodes(P, posp, ax=ax,
                       node_color=[ORANGE if g in big else TEAL for g in P.nodes()],
                       linewidths=0, node_size=420)
nx.draw_networkx_labels(P, posp, ax=ax, font_size=8, font_color="white",
                        font_weight="bold")
n_clique = len(list(combinations(big, 2)))
ax.set_title("사영 — 유전자–유전자", color=NAVY)
ax.text(0.5, -0.04,
        f"엣지 {P.number_of_edges()}개 중 {n_clique}개가 P3 하나에서 나온 clique",
        transform=ax.transAxes, ha="center", va="top", fontsize=10.5, color=RED)
ax.margins(0.16); ax.set_axis_off()

fig.savefig(os.path.join(OUT, "projection.png"))
print("wrote", os.path.join(OUT, "projection.png"))
print("  bipartite edges:", B.number_of_edges(),
      "| projected edges:", P.number_of_edges(),
      "| P3 clique edges:", n_clique)
