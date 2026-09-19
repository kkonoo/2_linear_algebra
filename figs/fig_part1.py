"""1–7장 그림."""
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, FancyBboxPatch
from style import *

# ── 1장 ─────────────────────────────────────────────────────────
def ch01():
    # f1 세 가지 시각
    fig, ax = plt.subplots(1, 3, figsize=(7.5, 2.6))
    plane(ax[0], 3.2)
    arrow(ax[0], (2, 1), PURPLE, "$v$")
    arrow(ax[0], (2, 1), GREY, None, start=(-2.5, -2.0), lw=1.4, alpha=.6)
    ax[0].set_title("① 화살표 — 크기와 방향", fontsize=9)

    plane(ax[1], 3.2)
    arrow(ax[1], (2, 1), PURPLE)
    ax[1].plot([2, 2], [0, 1], color=TEAL, ls=":", lw=1.2)
    ax[1].plot([0, 2], [1, 1], color=TEAL, ls=":", lw=1.2)
    ax[1].text(2.05, -0.38, "2", color=TEAL); ax[1].text(-0.42, 1.0, "1", color=TEAL)
    ax[1].set_title("② 좌표 — 기저에 대한 계수", fontsize=9)

    g = ["g1", "g2", "g3", "g4", "g5"]
    ax[2].bar(g, [2.1, 0.4, 3.3, 1.2, 2.7], color=PURPLE, width=.6)
    ax[2].set_title("③ 데이터 — 숫자 리스트", fontsize=9)
    ax[2].set_ylabel("expression"); ax[2].set_yticks([])
    for s in ("top", "right"): ax[2].spines[s].set_visible(False)
    save(fig, "ch01", "f1_three_views.png")

    # f2 span
    fig, ax = plt.subplots(1, 2, figsize=(5.4, 2.7))
    plane(ax[0]); t = np.linspace(-3, 3, 2)
    ax[0].plot(t * 1, t * 2, color=LILAC, lw=6, alpha=.35, solid_capstyle="round")
    arrow(ax[0], (1, 2), PURPLE, "$v_1$")
    ax[0].set_title(r"span$\{v_1\}$ — 직선", fontsize=9)

    plane(ax[1])
    ax[1].add_patch(Polygon([[-3, -3], [3, -3], [3, 3], [-3, 3]], color=LILAC, alpha=.22))
    for c in np.arange(-3, 3.1, 1.0):
        ax[1].plot([-3, 3], [-3 * 2 + c * 3, 3 * 2 + c * 3], color="white", lw=.6)
    arrow(ax[1], (1, 2), PURPLE, "$v_1$"); arrow(ax[1], (3, 1), TEAL, "$v_2$")
    ax[1].set_title(r"span$\{v_1,v_2\}$ — 평면 전체", fontsize=9)
    save(fig, "ch01", "f2_span.png")

    # f3 독립/종속
    fig, ax = plt.subplots(1, 2, figsize=(5.4, 2.7))
    plane(ax[0]); arrow(ax[0], (1, 2), PURPLE, "$v_1$"); arrow(ax[0], (3, 1), TEAL, "$v_2$")
    ax[0].set_title("선형독립 — 새 방향을 준다", fontsize=9)
    plane(ax[1]); t = np.linspace(-3, 3, 2)
    ax[1].plot(t, t * 0.66, color=GREY, ls="--", lw=.9)
    arrow(ax[1], (1.2, 0.8), PURPLE, "$v_1$"); arrow(ax[1], (2.4, 1.6), TEAL, "$v_2=2v_1$")
    ax[1].set_title("선형종속 — span이 그대로", fontsize=9)
    save(fig, "ch01", "f3_independence.png")

# ── 2장 ─────────────────────────────────────────────────────────
def ch02():
    A = np.array([[2., 1.], [0., 3.]])
    fig, ax = plt.subplots(1, 2, figsize=(5.6, 2.9))
    plane(ax[0], 3.6)
    ax[0].add_patch(Polygon(SQUARE.T[:4], color=LILAC, alpha=.3))
    arrow(ax[0], (1, 0), PURPLE, "$e_1$"); arrow(ax[0], (0, 1), TEAL, "$e_2$")
    ax[0].set_title("변환 전 — 단위정사각형", fontsize=9)
    plane(ax[1], 3.6)
    out = A @ SQUARE
    ax[1].add_patch(Polygon(out.T[:4], color=LILAC, alpha=.3))
    arrow(ax[1], A[:, 0], PURPLE, "$Ae_1$"); arrow(ax[1], A[:, 1], TEAL, "$Ae_2$")
    ax[1].set_title("변환 후 — 열이 곧 행선지", fontsize=9)
    save(fig, "ch02", "f1_columns.png")

    th = np.pi / 6
    mats = [("identity", np.eye(2)), ("scale 1.5", 1.5 * np.eye(2)),
            ("shearing", np.array([[1, 1], [0, 1.]])),
            ("rotation", np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])),
            ("permutation", np.array([[0, 1], [1, 0.]])),
            ("projection", np.array([[1, 0], [0, 0.]]))]
    fig, axes = plt.subplots(2, 3, figsize=(6.6, 4.4))
    for a, (name, M) in zip(axes.ravel(), mats):
        plane(a, 2.4)
        a.add_patch(Polygon(SQUARE.T[:4], facecolor="none", edgecolor=GREY, ls="--", lw=.9))
        o = M @ SQUARE
        a.add_patch(Polygon(o.T[:4], color=LILAC, alpha=.45))
        arrow(a, M[:, 0], PURPLE, lw=1.6); arrow(a, M[:, 1], TEAL, lw=1.6)
        a.set_title(name, fontsize=8.5)
    save(fig, "ch02", "f2_gallery.png")

    R = np.array([[0, -1], [1, 0.]]); P = np.array([[1, 0], [0, 0.]])
    fig, ax = plt.subplots(1, 3, figsize=(7.2, 2.6))
    for a, (M, t) in zip(ax, [(np.eye(2), "원본"), (P @ R, "$PR$ — 돌린 뒤 사영"),
                              (R @ P, "$RP$ — 사영 뒤 회전")]):
        plane(a, 2.0)
        a.add_patch(Polygon(SQUARE.T[:4], facecolor="none", edgecolor=GREY, ls="--", lw=.9))
        o = M @ SQUARE
        a.plot(o[0], o[1], color=PURPLE, lw=2.4)
        a.add_patch(Polygon(o.T[:4], color=LILAC, alpha=.4))
        a.set_title(t, fontsize=9)
    save(fig, "ch02", "f3_noncommute.png")

# ── 3장 ─────────────────────────────────────────────────────────
def ch03():
    fig, ax = plt.subplots(1, 2, figsize=(5.6, 2.8))
    a = np.array([2., 1.])
    plane(ax[0], 3.2)
    xs = np.linspace(-3, 3, 2)
    for c in range(-4, 9, 2):
        ax[0].plot(xs, (c - a[0] * xs) / a[1], color=TEAL, lw=.9, alpha=.75)
        if c in (0, 4): ax[0].text(2.6, (c - a[0] * 2.6) / a[1] + .12, f"$={c}$", color=TEAL, fontsize=7.5)
    arrow(ax[0], a, PURPLE, r"$[2\ 1]$")
    ax[0].set_title("행벡터 = 선형함수 · 등고선 ⊥ 행벡터", fontsize=9)

    plane(ax[1], 3.2)
    b = np.array([2.6, 0.6]); u = a / np.linalg.norm(a)
    p = (b @ u) * u
    arrow(ax[1], a, PURPLE, "$a$"); arrow(ax[1], b, TEAL, "$b$")
    ax[1].plot([b[0], p[0]], [b[1], p[1]], color=GREY, ls=":", lw=1.2)
    arrow(ax[1], p, CORAL, None, lw=3.0)
    ax[1].text(p[0] * .5, p[1] * .5 - .5, "정사영 길이", color=CORAL, fontsize=8)
    ax[1].set_title(r"$a^\top b = |a|\,|b|\cos\theta$", fontsize=9)
    save(fig, "ch03", "f1_rowvector_projection.png")

    fig, ax = plt.subplots(1, 3, figsize=(6.6, 2.4))
    t = np.linspace(0, 2 * np.pi, 400)
    shapes = [("$L^1$ — 마름모", np.array([[1, 0, -1, 0, 1], [0, 1, 0, -1, 0.]])),
              ("$L^2$ — 원", np.vstack([np.cos(t), np.sin(t)])),
              (r"$L^\infty$ — 정사각형", np.array([[1, 1, -1, -1, 1], [1, -1, -1, 1, 1.]]))]
    for a_, (name, s) in zip(ax, shapes):
        plane(a_, 1.6)
        a_.add_patch(Polygon(s.T, color=LILAC, alpha=.4))
        a_.plot(s[0], s[1], color=PURPLE, lw=1.8)
        a_.set_title(name, fontsize=9)
    save(fig, "ch03", "f2_norms.png")

# ── 4장 ─────────────────────────────────────────────────────────
def ch04():
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")

    def box(x, y, w, h, fc, label, sub):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                                    fc=fc, ec="none"))
        ax.text(x + w / 2, y + h * .62, label, ha="center", fontsize=9.5, color="#333")
        ax.text(x + w / 2, y + h * .24, sub, ha="center", fontsize=7.5, color="#666")

    box(0.4, 3.2, 3.0, 1.5, LILAC + "80", "행공간 $C(A^\\top)$", "차원 $r$")
    box(0.4, 0.7, 3.0, 1.5, "#EDEBF3", "영공간 $N(A)$", "차원 $n-r$")
    box(6.6, 3.2, 3.0, 1.5, "#BFE3E1", "열공간 $C(A)$", "차원 $r$ · 치역")
    box(6.6, 0.7, 3.0, 1.5, "#EDF3F3", "좌영공간 $N(A^\\top)$", "차원 $m-r$ · 도달 불가")

    ax.annotate("", xy=(6.5, 3.95), xytext=(3.5, 3.95),
                arrowprops=dict(arrowstyle="-|>", color=PURPLE, lw=2))
    ax.text(5.0, 4.15, "$A$ — 일대일 대응", ha="center", fontsize=8.5, color=PURPLE)
    ax.annotate("", xy=(6.5, 1.45), xytext=(3.5, 1.45),
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.6, ls=":"))
    ax.text(5.0, 1.62, "$A$ → $0$", ha="center", fontsize=8.5, color=GREY)

    ax.text(1.9, 2.75, "⊥", ha="center", fontsize=11, color=CORAL)
    ax.text(8.1, 2.75, "⊥", ha="center", fontsize=11, color=CORAL)
    ax.text(1.9, 5.15, r"정의역  $\mathbb{R}^n$", ha="center", fontsize=9.5, color="#333")
    ax.text(8.1, 5.15, r"공역  $\mathbb{R}^m$", ha="center", fontsize=9.5, color="#333")
    save(fig, "ch04", "f1_four_subspaces.png")

    fig, ax = plt.subplots(1, 2, figsize=(5.4, 2.7))
    t = np.linspace(-3, 3, 2)
    plane(ax[0]); ax[0].plot(t, t * .6, color=PURPLE, lw=2.2)
    ax[0].plot(0, 0, "o", color=CORAL, ms=5)
    ax[0].set_title("부분공간 O — 원점을 지남", fontsize=9)
    plane(ax[1]); ax[1].plot(t, t * .6 + 1.2, color=GREY, lw=2.2)
    ax[1].plot(0, 0, "o", color=CORAL, ms=5)
    ax[1].text(.15, -.55, "원점 ∉", color=CORAL, fontsize=8)
    ax[1].set_title("부분공간 X — 원점을 안 지남", fontsize=9)
    save(fig, "ch04", "f2_subspace_or_not.png")

# ── 5장 ─────────────────────────────────────────────────────────
def ch05():
    B = np.array([[1.4, -0.7], [0.5, 1.2]])
    v = np.array([2.3, 1.7])
    fig, ax = plt.subplots(1, 2, figsize=(5.6, 2.9))
    plane(ax[0], 3.2)
    arrow(ax[0], v, CORAL, "$v$", lw=2.4)
    arrow(ax[0], (1, 0), PURPLE, "$e_1$", lw=1.5); arrow(ax[0], (0, 1), TEAL, "$e_2$", lw=1.5)
    ax[0].set_title("표준기저 — $v=(2.3,\\ 1.7)$", fontsize=9)

    plane(ax[1], 3.2, grid=False)
    for k in np.arange(-3, 3.1, 1):
        for vec, other in ((B[:, 0], B[:, 1]), (B[:, 1], B[:, 0])):
            p0 = other * k - vec * 4; p1 = other * k + vec * 4
            ax[1].plot([p0[0], p1[0]], [p0[1], p1[1]], color=FAINT, lw=.7, zorder=0)
    c = np.linalg.solve(B, v)
    arrow(ax[1], v, CORAL, "$v$", lw=2.4)
    arrow(ax[1], B[:, 0], PURPLE, "$b_1$", lw=1.5); arrow(ax[1], B[:, 1], TEAL, "$b_2$", lw=1.5)
    ax[1].set_title(f"새 기저 — $[v]_B=({c[0]:.1f},\\ {c[1]:.1f})$", fontsize=9)
    save(fig, "ch05", "f1_two_coordinates.png")

    fig, ax = plt.subplots(figsize=(6.2, 1.9)); ax.axis("off")
    ax.set_xlim(0, 10); ax.set_ylim(0, 3)
    steps = [("$[v]_P$", "#EDEBF3"), ("표준좌표", LILAC + "80"),
             ("변환됨", "#BFE3E1"), ("$[Av]_P$", "#EDF3F3")]
    ops = ["$P$", "$A$", "$P^{-1}$"]
    for i, (lab, fc) in enumerate(steps):
        x = 0.3 + i * 2.5
        ax.add_patch(FancyBboxPatch((x, 1.0), 1.7, 1.0, boxstyle="round,pad=0.07", fc=fc, ec="none"))
        ax.text(x + .85, 1.5, lab, ha="center", va="center", fontsize=9)
        if i < 3:
            ax.annotate("", xy=(x + 2.5, 1.5), xytext=(x + 1.75, 1.5),
                        arrowprops=dict(arrowstyle="-|>", color=PURPLE, lw=1.6))
            ax.text(x + 2.12, 1.72, ops[i], ha="center", fontsize=8.5, color=PURPLE)
    ax.text(5.0, 0.35, "$P^{-1}AP$ — 번역 → 작업 → 재번역", ha="center", fontsize=9, color="#555")
    save(fig, "ch05", "f2_similarity.png")

# ── 6장 ─────────────────────────────────────────────────────────
def ch06():
    mats = [(np.eye(2), "$\\det=1$"),
            (np.array([[2, 0], [0, 1.5]]), "$\\det=3$"),
            (np.array([[1, 1], [0, 1.]]), "$\\det=1$ · 전단"),
            (np.array([[0, 1], [1, 0.]]), "$\\det=-1$ · 반사"),
            (np.array([[1, 2], [0.5, 1.]]), "$\\det=0$ · 붕괴")]
    fig, ax = plt.subplots(1, 5, figsize=(9.5, 2.1))
    for a, (M, t) in zip(ax, mats):
        plane(a, 2.6)
        a.add_patch(Polygon(SQUARE.T[:4], facecolor="none", edgecolor=GREY, ls="--", lw=.8))
        o = M @ SQUARE
        a.add_patch(Polygon(o.T[:4], color=LILAC, alpha=.5))
        a.plot(o[0], o[1], color=PURPLE, lw=1.8)
        a.set_title(t, fontsize=8.5)
    save(fig, "ch06", "f1_determinant_area.png")

    fig, ax = plt.subplots(1, 3, figsize=(6.6, 2.4))
    for a, eps in zip(ax, [0.8, 0.25, 0.03]):
        plane(a, 2.0)
        M = np.array([[1, 1], [0, eps]])
        o = M @ SQUARE
        a.add_patch(Polygon(o.T[:4], color=CORAL, alpha=.35))
        arrow(a, M[:, 0], PURPLE, lw=1.6); arrow(a, M[:, 1], TEAL, lw=1.6)
        a.set_title(f"$\\det={eps:.2f}$ · $\\kappa$={np.linalg.cond(M):.0f}", fontsize=8.5)
    fig.suptitle("두 열이 평행해질수록 넓이 → 0, 역행렬은 폭주", fontsize=9, y=1.03)
    save(fig, "ch06", "f2_collinear.png")

# ── 7장 ─────────────────────────────────────────────────────────
def ch07():
    fig, ax = plt.subplots(1, 2, figsize=(5.6, 2.9))
    xs = np.linspace(-1, 4, 2)
    plane(ax[0], 3.4)
    ax[0].plot(xs, (5 - 1 * xs) / 2, color=PURPLE, lw=1.8)
    ax[0].plot(xs, (11 - 3 * xs) / 4, color=TEAL, lw=1.8)
    ax[0].plot(1, 2, "o", color=CORAL, ms=6)
    ax[0].text(1.15, 2.15, "교점 $(1,2)$", color=CORAL, fontsize=8)
    ax[0].set_title("행 그림 — 직선의 교차", fontsize=9)

    plane(ax[1], 3.4)
    a1 = np.array([1., 3.]); a2 = np.array([2., 4.]); b = a1 + 2 * a2
    arrow(ax[1], a1, PURPLE, "$a_1$"); arrow(ax[1], a2, TEAL, "$a_2$")
    arrow(ax[1], 2 * a2, TEAL, None, start=a1, lw=1.3, ls=":")
    arrow(ax[1], b / 3.2, CORAL, "$b$", lw=2.2)
    ax[1].set_title("열 그림 — 열벡터의 조합", fontsize=9)
    save(fig, "ch07", "f1_row_column_picture.png")

    fig, ax = plt.subplots(1, 3, figsize=(7.0, 2.5))
    systems = [([[1, 2], [3, 4.]], [5, 11], "원래 방정식"),
               ([[1, 2], [0, -2.]], [5, -4], "가우스 소거 후 (REF)"),
               ([[1, 0], [0, 1.]], [1, 2], "가우스-조던 후 (RREF)")]
    for a, (A, b, t) in zip(ax, systems):
        A = np.array(A); b = np.array(b, float)
        plane(a, 3.4)
        for row, rhs, c in zip(A, b, (PURPLE, TEAL)):
            if abs(row[1]) > 1e-9:
                a.plot(xs, (rhs - row[0] * xs) / row[1], color=c, lw=1.8)
            else:
                a.axvline(rhs / row[0], color=c, lw=1.8)
            arrow(a, row / np.linalg.norm(row) * 1.3, c, None, lw=1.1, ls="--", alpha=.7)
        a.plot(1, 2, "o", color=CORAL, ms=5)
        a.set_title(t, fontsize=8.5)
    fig.suptitle("법선벡터(점선)가 축에 평행해진다 · 교점은 보존", fontsize=9, y=1.04)
    save(fig, "ch07", "f2_elimination_geometry.png")


if __name__ == "__main__":
    for f in (ch01, ch02, ch03, ch04, ch05, ch06, ch07):
        print(f.__name__); f()
