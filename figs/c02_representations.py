"""02 §2 — 같은 그래프, 세 가지 표현.

그림 / 인접 행렬 / 엣지 목록·인접 리스트.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *
import networkx as nx

OUT = outdir("c02")

names = ["TP53", "MDM2", "CDKN1A", "ATM", "CHEK2", "BAX", "RB1", "E2F1"]
edges = [("TP53", "MDM2"), ("TP53", "CDKN1A"), ("TP53", "BAX"), ("TP53", "ATM"),
         ("ATM", "CHEK2"), ("CHEK2", "TP53"), ("CDKN1A", "RB1"), ("RB1", "E2F1")]
G = nx.Graph(); G.add_nodes_from(names); G.add_edges_from(edges)

fig = plt.figure(figsize=(15.6, 5.1))
gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.05, 1.15], wspace=0.28)

# --- A. 그림 ---------------------------------------------------------------
ax = fig.add_subplot(gs[0, 0])
pos = nx.spring_layout(G, seed=5, k=1.1)
nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#B9C6CE", width=1.6)
nx.draw_networkx_nodes(G, pos, ax=ax, node_color=TEAL, linewidths=0,
                       node_size=1250)
nx.draw_networkx_labels(G, pos, ax=ax, font_size=7.5, font_color="white",
                        font_weight="bold")
ax.set_title("① 그림", color=NAVY)
ax.margins(0.14)
ax.set_axis_off()

# --- B. 인접 행렬 ----------------------------------------------------------
ax = fig.add_subplot(gs[0, 1])
A = nx.to_numpy_array(G, nodelist=names)
ax.imshow(A, cmap="Blues", vmin=0, vmax=1.6)
ax.set_xticks(range(len(names))); ax.set_yticks(range(len(names)))
ax.set_xticklabels(names, rotation=60, ha="right", fontsize=8)
ax.set_yticklabels(names, fontsize=8)
for i in range(len(names)):
    for j in range(len(names)):
        ax.text(j, i, int(A[i, j]), ha="center", va="center", fontsize=7.5,
                color="white" if A[i, j] else "#9AA5AC")
ax.set_xticks(np.arange(-.5, len(names), 1), minor=True)
ax.set_yticks(np.arange(-.5, len(names), 1), minor=True)
ax.grid(which="minor", color="white", lw=1.4)
ax.tick_params(which="minor", length=0)
for s in ax.spines.values():
    s.set_visible(False)
ax.set_title("② 인접 행렬 — 칸 64개 중 16개만 1", color=NAVY, fontsize=11.5)

# --- C. 목록 두 가지 -------------------------------------------------------
ax = fig.add_subplot(gs[0, 2]); ax.set_axis_off()
el = "\n".join(f"{u:<8}{v}" for u, v in sorted(G.edges()))
al = "\n".join(f"{n:<8}{', '.join(sorted(G[n]))}" for n in names[:5])
ax.text(0.0, 1.02, "③ 엣지 목록 — 8줄", transform=ax.transAxes, va="top",
        fontsize=11.5, fontweight="bold", color=NAVY)
ax.text(0.02, 0.93, el, transform=ax.transAxes, va="top", family="monospace",
        fontsize=8.6, color="#2A2A2A")
ax.text(0.0, 0.42, "④ 인접 리스트 — 앞 5개만", transform=ax.transAxes, va="top",
        fontsize=11.5, fontweight="bold", color=NAVY)
ax.text(0.02, 0.33, al, transform=ax.transAxes, va="top", family="monospace",
        fontsize=8.6, color="#2A2A2A")

fig.savefig(os.path.join(OUT, "representations.png"))
print("wrote", os.path.join(OUT, "representations.png"))
