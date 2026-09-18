"""02 §3 — 연결성: component, bridge, articulation node, 그리고 방향 그래프의 SCC.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *
import networkx as nx

OUT = outdir("c02")

# ── 왼쪽: 무방향 그래프 ───────────────────────────────────────────────
G = nx.Graph()
G.add_edges_from([
    # 덩어리 A
    (0, 1), (0, 2), (1, 2), (2, 3), (1, 3),
    # 다리
    (3, 4),
    # 덩어리 B
    (4, 5), (4, 6), (5, 6), (6, 7), (5, 7),
    # 떨어져 있는 작은 덩어리
    (8, 9), (9, 10), (8, 10),
])
bridges = list(nx.bridges(G))
arts = list(nx.articulation_points(G))
comps = list(nx.connected_components(G))

pos = nx.spring_layout(G, seed=12, k=0.85)
fig, axes = plt.subplots(1, 2, figsize=(13.6, 5.0),
                         gridspec_kw={"wspace": 0.08})

ax = axes[0]
ecol = [RED if (u, v) in bridges or (v, u) in bridges else "#C3CED6"
        for u, v in G.edges()]
ewid = [2.6 if c == RED else 1.4 for c in ecol]
nx.draw_networkx_edges(G, pos, ax=ax, edge_color=ecol, width=ewid)
ncol = [ORANGE if n in arts else TEAL for n in G.nodes()]
nx.draw_networkx_nodes(G, pos, ax=ax, node_color=ncol, linewidths=0,
                       node_size=420)
nx.draw_networkx_labels(G, pos, ax=ax, font_size=9, font_color="white",
                        font_weight="bold")
ax.set_title(f"무방향 — 연결 요소 {len(comps)}개", color=NAVY)
ax.text(0.5, -0.04,
        f"빨간 엣지 = bridge ({len(bridges)}개)   ·   주황 노드 = 절단점 ({len(arts)}개)",
        transform=ax.transAxes, ha="center", va="top", fontsize=10.5,
        color="#4A4A4A")
ax.margins(0.12); ax.set_axis_off()

# ── 오른쪽: 방향 그래프의 SCC ─────────────────────────────────────────
D = nx.DiGraph()
D.add_edges_from([
    (0, 1), (1, 2), (2, 0),          # SCC 1
    (2, 3),
    (3, 4), (4, 5), (5, 3),          # SCC 2
    (5, 6),
    (6, 7), (7, 6),                  # SCC 3
])
sccs = sorted(nx.strongly_connected_components(D), key=lambda s: min(s))
palette = [TEAL, PURPLE, ORANGE, OLIVE]
cmap = {n: palette[i % len(palette)] for i, s in enumerate(sccs) for n in s}

ax = axes[1]
posd = nx.kamada_kawai_layout(D)
nx.draw_networkx_edges(D, posd, ax=ax, edge_color="#9FB6C4", width=1.5,
                       arrowsize=14, node_size=420)
nx.draw_networkx_nodes(D, posd, ax=ax, node_color=[cmap[n] for n in D.nodes()],
                       linewidths=0, node_size=420)
nx.draw_networkx_labels(D, posd, ax=ax, font_size=9, font_color="white",
                        font_weight="bold")
ax.set_title(f"방향 — 약하게 연결된 하나의 덩어리, SCC {len(sccs)}개", color=NAVY)
ax.text(0.5, -0.04,
        "색 = 강하게 연결된 요소(SCC). 방향을 지우면 전부 한 덩어리로 보인다",
        transform=ax.transAxes, ha="center", va="top", fontsize=10.5,
        color="#4A4A4A")
ax.margins(0.12); ax.set_axis_off()

fig.savefig(os.path.join(OUT, "connectivity.png"))
print("wrote", os.path.join(OUT, "connectivity.png"))
print("  components:", [sorted(c) for c in comps])
print("  bridges:", bridges, " articulation:", sorted(arts))
print("  SCCs:", [sorted(s) for s in sccs])
