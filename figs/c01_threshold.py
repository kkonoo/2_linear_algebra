"""01 §3 — 임계값이 네트워크를 정한다.

같은 상관 행렬, 세 개의 기준값.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *
import networkx as nx

OUT = outdir("c01")

rng = np.random.default_rng(4)
nmod, per = 4, 12
n = nmod * per
lab = np.repeat(np.arange(nmod), per)

C = np.zeros((n, n))
for i in range(n):
    for j in range(i + 1, n):
        base = 0.70 if lab[i] == lab[j] else 0.22
        C[i, j] = C[j, i] = np.clip(base + rng.normal(0, 0.15), -0.2, 0.99)

ths = np.arange(0.30, 0.951, 0.01)
counts = [(C > t).sum() // 2 for t in ths]

fig = plt.figure(figsize=(15.6, 4.8))
gs = fig.add_gridspec(1, 4, width_ratios=[1.30, 1, 1, 1], wspace=0.30)

ax = fig.add_subplot(gs[0, 0])
ax.plot(ths, counts, color=NAVY, lw=2.2)
for t, col in [(0.50, ORANGE), (0.60, TEAL), (0.75, PURPLE)]:
    ax.axvline(t, color=col, ls="--", lw=1.4)
    ax.scatter([t], [(C > t).sum() // 2], color=col, zorder=5, s=38)
ax.set_xlabel("상관 임계값  r")
ax.set_ylabel("엣지 수")
ax.set_title("임계값에 따른 엣지 수", color=NAVY, fontsize=12)
ax.set_yscale("log")

cols = [[TEAL, PURPLE, OLIVE, ORANGE][l] for l in lab]
for idx, (t, col) in enumerate([(0.50, ORANGE), (0.60, TEAL), (0.75, PURPLE)]):
    G = nx.Graph((i, j) for i in range(n) for j in range(i + 1, n) if C[i, j] > t)
    G.add_nodes_from(range(n))
    pos = nx.spring_layout(G, seed=2, k=0.55)
    ax = fig.add_subplot(gs[0, idx + 1])
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=LGREY, width=0.6)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=cols, linewidths=0,
                           node_size=48)
    ax.set_title(f"r > {t:.2f}\n엣지 {G.number_of_edges()}개", color=col,
                 fontsize=12)
    ax.set_axis_off()

fig.subplots_adjust(top=0.80)
fig.savefig(os.path.join(OUT, "threshold.png"))
print("wrote", os.path.join(OUT, "threshold.png"))
