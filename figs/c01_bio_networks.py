"""01 §2 — 네 가지 생물학 네트워크, 하나의 자료구조.

왼쪽 둘: 연결이 실재한다. 오른쪽 둘: 우리가 만들었고 파라미터가 모양을 정했다.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import *
import networkx as nx
from scipy.spatial import cKDTree

OUT = outdir("c01")

fig, axes = plt.subplots(1, 4, figsize=(16.0, 4.5), gridspec_kw={"wspace": 0.06})
rng = np.random.default_rng(11)

# --- 1. PPI: 허브가 있는 구조 ----------------------------------------------
G = nx.barabasi_albert_graph(70, 2, seed=3)
pos = nx.spring_layout(G, seed=3, k=0.42)
deg = np.array([d for _, d in G.degree()])
ax = axes[0]
nx.draw_networkx_edges(G, pos, ax=ax, edge_color=LGREY, width=0.8)
nx.draw_networkx_nodes(G, pos, ax=ax, node_color=TEAL, linewidths=0,
                       node_size=18 + 9 * deg)
ax.set_title("단백질 상호작용 (PPI)", color=NAVY)
ax.text(0.5, -0.05, "엣지가 측정되었다\n(Y2H, AP-MS, 큐레이션)",
        transform=ax.transAxes, ha="center", va="top", fontsize=10,
        color="#4A4A4A")

# --- 2. 대사·신호전달: 방향이 있다 -----------------------------------------
D = nx.DiGraph()
for ch in (list(range(0, 7)), list(range(7, 13)), list(range(13, 19))):
    D.add_edges_from(zip(ch[:-1], ch[1:]))
D.add_edges_from([(3, 8), (9, 15), (16, 5), (1, 14)])
posd = nx.kamada_kawai_layout(D)
ax = axes[1]
nx.draw_networkx_edges(D, posd, ax=ax, edge_color="#9FB6C4", width=1.1,
                       arrowsize=9, node_size=110)
nx.draw_networkx_nodes(D, posd, ax=ax, node_color=NAVY, linewidths=0,
                       node_size=110)
ax.set_title("대사 · 신호전달", color=NAVY)
ax.text(0.5, -0.05, "엣지에 방향과 부호가 있다",
        transform=ax.transAxes, ha="center", va="top", fontsize=10,
        color="#4A4A4A")

# --- 3. 공발현: 상관 임계값을 우리가 골랐다 --------------------------------
nmod, per = 4, 12
lab = np.repeat(np.arange(nmod), per)
n = nmod * per
C = np.zeros((n, n))
for i in range(n):
    for j in range(i + 1, n):
        base = 0.72 if lab[i] == lab[j] else 0.18
        C[i, j] = C[j, i] = np.clip(base + rng.normal(0, 0.13), 0, 0.99)
Gc = nx.Graph((i, j) for i in range(n) for j in range(i + 1, n) if C[i, j] > 0.60)
Gc.add_nodes_from(range(n))
posc = nx.spring_layout(Gc, seed=7, k=0.5)
cols = [[TEAL, PURPLE, OLIVE, ORANGE][l] for l in lab]
ax = axes[2]
nx.draw_networkx_edges(Gc, posc, ax=ax, edge_color=LGREY, width=0.7)
nx.draw_networkx_nodes(Gc, posc, ax=ax, node_color=cols, linewidths=0,
                       node_size=55)
ax.set_title("유전자 공발현", color=NAVY)
ax.text(0.5, -0.05, "⚠ 우리가 r > 0.60 이라고\n정했기 때문에 생긴 엣지",
        transform=ax.transAxes, ha="center", va="top", fontsize=10, color=RED)

# --- 4. 세포 kNN 그래프: k 를 우리가 골랐다 --------------------------------
pops = [(34, (-1.7, 1.5), 0.55, BLUE), (28, (1.6, 1.7), 0.50, PURPLE),
        (24, (1.1, -1.5), 0.48, TEAL), (14, (-1.9, -1.6), 0.40, ORANGE)]
X, cc = [], []
for cnt, (cx, cy), s, col in pops:
    X.append(rng.normal([cx, cy], s, size=(cnt, 2))); cc += [col] * cnt
X = np.vstack(X)
tree = cKDTree(X); k = 5
Gk = nx.Graph(); Gk.add_nodes_from(range(len(X)))
for i, nb in enumerate(tree.query(X, k + 1)[1]):
    for j in nb[1:]:
        Gk.add_edge(i, int(j))
posk = {i: tuple(X[i]) for i in range(len(X))}
ax = axes[3]
nx.draw_networkx_edges(Gk, posk, ax=ax, edge_color=LGREY, width=0.7)
nx.draw_networkx_nodes(Gk, posk, ax=ax, node_color=cc, linewidths=0, node_size=45)
ax.set_title("단일세포 kNN 그래프", color=NAVY)
ax.text(0.5, -0.05, "⚠ 우리가 k = 5 라고\n정했기 때문에 생긴 엣지",
        transform=ax.transAxes, ha="center", va="top", fontsize=10, color=RED)

for ax in axes:
    ax.set_axis_off()

fig.savefig(os.path.join(OUT, "bio_networks.png"))
print("wrote", os.path.join(OUT, "bio_networks.png"))
