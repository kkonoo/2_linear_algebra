"""9–18장 그림."""
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse
from style import *

# ── 9장 ─────────────────────────────────────────────────────────
def ch09():
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    fig = plt.figure(figsize=(4.4, 3.6))
    ax = fig.add_subplot(111, projection="3d")
    L = 1.6
    P = np.array([[-L, -L, 0], [L, -L, 0], [L, L, 0], [-L, L, 0.]])
    ax.add_collection3d(Poly3DCollection([P], color=LILAC, alpha=.22,
                                         edgecolor=LILAC, lw=.8))
    a1 = np.array([1.2, -0.5, 0.]); a2 = np.array([0.3, 1.2, 0.])
    b  = np.array([0.9, 0.5, 1.25]); bh = np.array([0.9, 0.5, 0.])

    def q(v, c, lw=2.0):
        ax.quiver(0, 0, 0, *v, color=c, lw=lw, arrow_length_ratio=.13)

    q(a1, TEAL, 1.5); q(a2, TEAL, 1.5)
    q(b, CORAL, 2.4); q(bh, PURPLE, 2.4)
    ax.plot(*zip(bh, b), color=GREY, ls=":", lw=1.8)
    ax.plot([0], [0], [0], "o", color="#333", ms=3)

    ax.text(*(a1 + [.12, -.12, 0]), "$a_1$", color=TEAL, fontsize=9)
    ax.text(*(a2 + [-.05, .16, 0]), "$a_2$", color=TEAL, fontsize=9)
    ax.text(*(b + [.05, 0, .12]), "$b$", color=CORAL, fontsize=10)
    ax.text(*(bh + [.18, .05, -.18]), r"$\hat{b}=A\hat{x}$", color=PURPLE, fontsize=9)
    ax.text(1.05, .52, .62, "$e$", color="#777", fontsize=10)
    ax.text(-1.45, 1.35, -.08, "$C(A)$", color="#8B7FA8", fontsize=9)

    ax.set_xlim(-L, L); ax.set_ylim(-L, L); ax.set_zlim(-.1, 1.5)
    ax.set_box_aspect((1, 1, .75))
    ax.set_axis_off(); ax.view_init(20, -62)
    ax.set_title("$b$ 를 열공간에 정사영 · 잔차 $e$ 는 직교", fontsize=9, y=.97)
    save(fig, "ch09", "f1_projection_colspace.png")

    rng = np.random.default_rng(3)
    x = rng.normal(size=25); y = 0.9 * x + rng.normal(scale=.55, size=25)
    x -= x.mean(); y -= y.mean()
    beta = np.sum(x * y) / np.sum(x * x)
    C = np.cov(np.vstack([x, y])); w, V = np.linalg.eigh(C); d = V[:, -1]
    t = np.linspace(-2.6, 2.6, 2)
    fig, ax = plt.subplots(1, 2, figsize=(5.6, 2.9))
    for a, (title, line, proj) in zip(ax, [
            ("회귀 — $y$ 방향 거리", beta * t, "v"),
            ("PCA — 직교 거리", d[1] / d[0] * t, "o")]):
        plane(a, 2.8); a.plot(t, line, color=PURPLE, lw=1.8)
        a.plot(x, y, "o", color=CORAL, ms=3.5)
        for xi, yi in zip(x, y):
            if proj == "v":
                a.plot([xi, xi], [yi, beta * xi], color=GREY, lw=.9)
            else:
                p = (np.array([xi, yi]) @ d) * d
                a.plot([xi, p[0]], [yi, p[1]], color=GREY, lw=.9)
        a.set_title(title, fontsize=9)
    save(fig, "ch09", "f2_regression_vs_pca.png")

    fig, ax = plt.subplots(1, 2, figsize=(5.4, 2.8))
    b0 = np.array([1.7, 1.1]); A = np.array([[1.0, .55], [.55, .8]])
    gx, gy = np.meshgrid(np.linspace(-.4, 2.4, 200), np.linspace(-.6, 2.0, 200))
    Z = (A[0, 0] * (gx - b0[0])**2 + 2 * A[0, 1] * (gx - b0[0]) * (gy - b0[1])
         + A[1, 1] * (gy - b0[1])**2)
    tt = np.linspace(0, 2 * np.pi, 300); r = .75
    shapes = [("ridge — $L^2$ 공", np.vstack([r * np.cos(tt), r * np.sin(tt)])),
              ("lasso — $L^1$ 마름모", np.array([[r, 0, -r, 0, r], [0, r, 0, -r, 0.]]))]
    for a, (title, s) in zip(ax, shapes):
        plane(a, 2.2); a.set_xlim(-1.1, 2.5); a.set_ylim(-1.1, 2.1)
        a.contour(gx, gy, Z, levels=[.35, .9, 1.7, 2.8], colors=[LILAC], linewidths=.9)
        a.add_patch(Polygon(s.T, color=TEAL, alpha=.25))
        a.plot(s[0], s[1], color=TEAL, lw=1.6)
        a.plot(*b0, "o", color=CORAL, ms=5)
        a.text(b0[0] + .1, b0[1] + .1, r"$\hat{\beta}_{OLS}$", color=CORAL, fontsize=8)
        hit = np.array([r * .70, r * .70]) if "ridge" in title else np.array([r, 0.])
        a.plot(*hit, "o", color=PURPLE, ms=5)
        a.set_title(title, fontsize=9)
    fig.suptitle("등고선이 제약 영역에 처음 닿는 곳이 해", fontsize=9, y=1.03)
    save(fig, "ch09", "f3_ridge_lasso.png")

# ── 11장 ────────────────────────────────────────────────────────
def ch11():
    A = np.array([[2., 1.], [1., 2.]])
    fig, ax = plt.subplots(1, 2, figsize=(5.6, 2.9))
    for a, (M, t) in zip(ax, [(np.eye(2), "변환 전"), (A, "변환 후 $Ax$")]):
        plane(a, 3.4)
        for ang in np.linspace(0, np.pi, 9)[:-1]:
            v = M @ np.array([np.cos(ang), np.sin(ang)]) * 1.2
            arrow(a, v, GREY, None, lw=1.0, alpha=.75)
        for vec, c in ((np.array([1, 1]) / np.sqrt(2), PURPLE),
                       (np.array([-1, 1]) / np.sqrt(2), TEAL)):
            arrow(a, M @ vec * 1.2, c, None, lw=2.4)
        a.set_title(t, fontsize=9)
    fig.suptitle("굵은 두 벡터만 방향이 유지된다 — 고유벡터 ($\\lambda=3,\\ 1$)",
                 fontsize=9, y=1.03)
    save(fig, "ch11", "f1_eigenvector.png")

    rng = np.random.default_rng(2)
    x = rng.normal(size=12); y = .75 * x + rng.normal(scale=.6, size=12)
    a_, b_ = x - x.mean(), y - y.mean()
    r = a_ @ b_ / (np.linalg.norm(a_) * np.linalg.norm(b_))
    fig, ax = plt.subplots(figsize=(3.0, 2.9))
    plane(ax, 1.25)
    u = a_ / np.linalg.norm(a_) ; v = b_ / np.linalg.norm(b_)
    th = np.arccos(r)
    arrow(ax, (1, 0), PURPLE, "$a$ (편차)", lw=2.2)
    arrow(ax, (np.cos(th), np.sin(th)), TEAL, "$b$ (편차)", lw=2.2)
    arc = np.linspace(0, th, 60)
    ax.plot(.3 * np.cos(arc), .3 * np.sin(arc), color=CORAL, lw=1.2)
    ax.text(.36 * np.cos(th / 2), .36 * np.sin(th / 2), r"$\theta$", color=CORAL)
    ax.set_title(f"$r=\\cos\\theta={r:.2f}$", fontsize=9)
    save(fig, "ch11", "f2_correlation_cosine.png")

# ── 12장 ────────────────────────────────────────────────────────
def ch12():
    A = np.array([[2., 1.], [1., 3.]])
    w, Q = np.linalg.eigh(A)
    t = np.linspace(0, 2 * np.pi, 300); circ = np.vstack([np.cos(t), np.sin(t)])
    stages = [("① 원", circ, None), ("② $Q^\\top$ 회전", Q.T @ circ, Q.T),
              ("③ $\\Lambda$ 늘이기", np.diag(w) @ Q.T @ circ, None),
              ("④ $Q$ 되돌리기", A @ circ, Q)]
    fig, ax = plt.subplots(1, 4, figsize=(9.0, 2.4))
    for a, (title, C, _) in zip(ax, stages):
        plane(a, 3.6)
        a.plot(C[0], C[1], color=PURPLE, lw=1.8)
        a.fill(C[0], C[1], color=LILAC, alpha=.3)
        for i, c in enumerate((TEAL, CORAL)):
            arrow(a, C[:, np.argmin(np.abs(t - (0 if i == 0 else np.pi / 2)))],
                  c, None, lw=1.6)
        a.set_title(title, fontsize=9)
    save(fig, "ch12", "f1_evd_steps.png")

    gx, gy = np.meshgrid(np.linspace(-2, 2, 300), np.linspace(-2, 2, 300))
    cases = [("양정치 — 타원", np.array([[2., .5], [.5, 1.]])),
             ("부정치 — 쌍곡선", np.array([[1., 0.], [0., -1.]])),
             ("준정치 — 골짜기", np.array([[1., 1.], [1., 1.]]))]
    fig, ax = plt.subplots(1, 3, figsize=(7.0, 2.5))
    for a, (title, M) in zip(ax, cases):
        Z = M[0, 0] * gx**2 + 2 * M[0, 1] * gx * gy + M[1, 1] * gy**2
        plane(a, 2.0, grid=False)
        a.contour(gx, gy, Z, levels=[-2, -1, -.3, .3, 1, 2, 4],
                  colors=[PURPLE], linewidths=.9)
        wv, V = np.linalg.eigh(M)
        for k, c in zip(range(2), (TEAL, CORAL)):
            arrow(a, V[:, k] * 1.5, c, None, lw=1.5)
        a.set_title(f"{title}\n$\\lambda=({wv[0]:.1f},\\ {wv[1]:.1f})$", fontsize=8.5)
    fig.suptitle("고유벡터가 등고선의 축", fontsize=9, y=1.06)
    save(fig, "ch12", "f2_quadratic_forms.png")

# ── 13장 ────────────────────────────────────────────────────────
def ch13():
    rng = np.random.default_rng(7)
    X = rng.normal(size=(180, 2)) @ np.array([[1.8, .0], [1.1, .6]])
    Xc = X - X.mean(0)
    C = Xc.T @ Xc / len(Xc); w, Q = np.linalg.eigh(C); w, Q = w[::-1], Q[:, ::-1]

    fig, ax = plt.subplots(1, 2, figsize=(6.2, 2.9))
    plane(ax[0], 4.5)
    ax[0].plot(Xc[:, 0], Xc[:, 1], "o", color=GREY, ms=2.5, alpha=.65)
    for k, (c, lab) in enumerate(((PURPLE, "PC1"), (TEAL, "PC2"))):
        arrow(ax[0], Q[:, k] * np.sqrt(w[k]) * 2, c, lab, lw=2.4)
    ax[0].set_title("공분산의 고유벡터 = 분산의 방향", fontsize=9)

    angs = np.linspace(0, np.pi, 180)
    var = [np.var(Xc @ np.array([np.cos(a_), np.sin(a_)])) for a_ in angs]
    ax[1].plot(np.degrees(angs), var, color=PURPLE, lw=1.8)
    best = np.degrees(np.arctan2(Q[1, 0], Q[0, 0])) % 180
    ax[1].axvline(best, color=TEAL, ls="--", lw=1.2)
    ax[1].text(best + 3, max(var) * .93, "PC1 방향", color=TEAL, fontsize=8)
    ax[1].set_xlabel("정사영 방향 (도)"); ax[1].set_ylabel("정사영 분산")
    ax[1].set_title(r"$e^\top C e$ 를 최대화하는 방향", fontsize=9)
    for s in ("top", "right"): ax[1].spines[s].set_visible(False)
    save(fig, "ch13", "f1_pca_direction.png")

    ev = np.array([9.1, 3.4, 1.6, .9, .55, .35, .25, .18, .12, .08])
    ev = ev / ev.sum()
    fig, ax = plt.subplots(1, 2, figsize=(5.6, 2.4))
    ax[0].plot(range(1, 11), ev, "o-", color=PURPLE, ms=4)
    ax[0].set_xlabel("성분"); ax[0].set_ylabel("설명 분산 비율"); ax[0].set_title("Scree plot", fontsize=9)
    ax[1].plot(range(1, 11), np.cumsum(ev), "o-", color=TEAL, ms=4)
    ax[1].axhline(.9, color=CORAL, ls="--", lw=1)
    ax[1].text(6.2, .84, "90%", color=CORAL, fontsize=8)
    ax[1].set_xlabel("성분"); ax[1].set_ylabel("누적 비율"); ax[1].set_title("누적 설명 분산", fontsize=9)
    for a in ax:
        for s in ("top", "right"): a.spines[s].set_visible(False)
    save(fig, "ch13", "f2_scree.png")

    Xr = X + np.array([6., 4.])
    Cr = Xr.T @ Xr / len(Xr); wr, Qr = np.linalg.eigh(Cr)
    fig, ax = plt.subplots(1, 2, figsize=(5.8, 2.9))
    for a, (D, Qq, t) in zip(ax, [(Xc, Q, "중심화 O — PC1이 구조를 가리킴"),
                                  (Xr, Qr[:, ::-1], "중심화 X — PC1이 평균 방향")]):
        a.set_aspect("equal")
        a.plot(D[:, 0], D[:, 1], "o", color=GREY, ms=2.5, alpha=.6)
        a.plot(0, 0, "o", color=CORAL, ms=5)
        arrow(a, Qq[:, 0] * 5, PURPLE, "PC1", lw=2.2)
        a.axhline(0, color="#BBB", lw=.8); a.axvline(0, color="#BBB", lw=.8)
        a.set_xticks([]); a.set_yticks([])
        for s in a.spines.values(): s.set_visible(False)
        a.set_title(t, fontsize=8.5)
    save(fig, "ch13", "f3_centering.png")

# ── 14장 ────────────────────────────────────────────────────────
def ch14():
    a1 = np.array([2., 1.]); a2 = np.array([1.2, 2.4])
    u1 = a1; q1 = u1 / np.linalg.norm(u1)
    p = (q1 @ a2) * q1; u2 = a2 - p; q2 = u2 / np.linalg.norm(u2)
    fig, ax = plt.subplots(1, 3, figsize=(7.2, 2.6))
    plane(ax[0], 3.0); arrow(ax[0], a1, PURPLE, "$a_1$"); arrow(ax[0], a2, TEAL, "$a_2$")
    ax[0].set_title("① 주어진 벡터", fontsize=9)
    plane(ax[1], 3.0)
    arrow(ax[1], a1, PURPLE, "$u_1$"); arrow(ax[1], a2, GREY, "$a_2$", lw=1.2, alpha=.7)
    arrow(ax[1], p, CORAL, None, lw=2.0)
    ax[1].plot([a2[0], p[0]], [a2[1], p[1]], color=GREY, ls=":", lw=1.2)
    ax[1].text(p[0] * .5, p[1] * .5 - .45, "사영", color=CORAL, fontsize=8)
    ax[1].set_title("② $a_2$ 에서 사영 성분을 뺌", fontsize=9)
    plane(ax[2], 3.0)
    arrow(ax[2], q1 * 2.2, PURPLE, "$q_1$"); arrow(ax[2], q2 * 2.2, TEAL, "$q_2$")
    ax[2].plot([0, q1[0] * .35, (q1[0] + q2[0]) * .35, q2[0] * .35],
               [0, q1[1] * .35, (q1[1] + q2[1]) * .35, q2[1] * .35], color=CORAL, lw=1.0)
    ax[2].set_title("③ 정규화 — 정규직교기저", fontsize=9)
    save(fig, "ch14", "f1_gram_schmidt.png")

# ── 15장 ────────────────────────────────────────────────────────
def ch15():
    A = np.array([[2., 1.], [.6, 1.8]])
    U, d, Vt = np.linalg.svd(A)
    t = np.linspace(0, 2 * np.pi, 300); circ = np.vstack([np.cos(t), np.sin(t)])
    fig, ax = plt.subplots(1, 2, figsize=(5.8, 2.9))
    plane(ax[0], 3.0)
    ax[0].plot(circ[0], circ[1], color=GREY, lw=1.2)
    for k, c in enumerate((PURPLE, TEAL)):
        arrow(ax[0], Vt[k], c, f"$v_{k+1}$", lw=2.2)
    ax[0].set_title("입력 — 직교하는 $v_1,v_2$", fontsize=9)
    plane(ax[1], 3.0)
    E = A @ circ
    ax[1].plot(E[0], E[1], color=LILAC, lw=1.6)
    for k, c in enumerate((PURPLE, TEAL)):
        arrow(ax[1], U[:, k] * d[k], c, f"$\\sigma_{k+1}u_{k+1}$", lw=2.2)
    ax[1].set_title("출력 — 여전히 직교, 길이만 $\\sigma$배", fontsize=9)
    save(fig, "ch15", "f1_circle_to_ellipse.png")

    rng = np.random.default_rng(11)
    N = 140
    yy, xx = np.mgrid[0:N, 0:N]
    field = rng.normal(size=(N, N))
    for _ in range(22):                      # 반복 평활 → 매끄럽지만 랭크가 높은 장
        field = (field + np.roll(field, 1, 0) + np.roll(field, -1, 0)
                 + np.roll(field, 1, 1) + np.roll(field, -1, 1)) / 5
    field /= field.std()
    img = (0.45 * field
           + 1.2 * np.sin(xx / 13.) * np.cos(yy / 20.)
           + 1.7 * ((np.abs(xx - 42) < 18) & (np.abs(yy - 98) < 18))
           + 1.7 * (((xx - 98)**2 + (yy - 42)**2) < 24**2)
           + 1.2 * (np.abs(xx - yy) < 5))

    U, d, Vt = np.linalg.svd(img); tot = np.sqrt((d**2).sum())
    fig, ax = plt.subplots(1, 5, figsize=(9.4, 2.2))
    for a, k in zip(ax, [1, 5, 20, 60, len(d)]):
        Ak = U[:, :k] @ np.diag(d[:k]) @ Vt[:k]
        a.imshow(Ak, cmap="bone"); a.axis("off")
        if k == len(d):
            a.set_title(f"원본 (rank {np.linalg.matrix_rank(img)})", fontsize=8.5)
        else:
            a.set_title(f"$k={k}$\n오차 {np.sqrt((d[k:]**2).sum())/tot:.1%}"
                        f" · 저장 {k*(2*N+1)/N**2:.0%}", fontsize=8.5)
    save(fig, "ch15", "f2_lowrank.png")

# ── 16장 ────────────────────────────────────────────────────────
def ch16():
    rng = np.random.default_rng(5)
    s = rng.uniform(-1, 1, size=(800, 2))           # 비가우시안(균등) 원본
    A = np.array([[1.0, .7], [.35, 1.0]])
    X = s @ A.T; X -= X.mean(0)
    C = np.cov(X.T); w, Q = np.linalg.eigh(C); w, Q = w[::-1], Q[:, ::-1]
    fig, ax = plt.subplots(1, 2, figsize=(5.8, 2.9))
    for a in ax:
        a.set_aspect("equal"); a.plot(X[:, 0], X[:, 1], "o", color=GREY, ms=1.8, alpha=.5)
        a.set_xticks([]); a.set_yticks([])
        for sp in a.spines.values(): sp.set_visible(False)
    for k, c in enumerate((PURPLE, TEAL)):
        arrow(ax[0], Q[:, k] * np.sqrt(w[k]) * 2.2, c, f"PC{k+1}", lw=2.4)
    ax[0].set_title("PCA — 분산이 큰 직교 축", fontsize=9)
    for k, c in enumerate((PURPLE, TEAL)):
        arrow(ax[1], A[:, k] / np.linalg.norm(A[:, k]) * 2.0, c, f"IC{k+1}", lw=2.4)
    ax[1].set_title("ICA — 데이터의 '변' 방향 (직교 아님)", fontsize=9)
    save(fig, "ch16", "f1_pca_vs_ica.png")

# ── 17장 ────────────────────────────────────────────────────────
def ch17():
    gx, gy = np.meshgrid(np.linspace(-2, 2, 300), np.linspace(-2, 2, 300))
    fig, ax = plt.subplots(1, 3, figsize=(7.2, 2.5))
    Z1 = gx**2 + 4 * gy**2
    ax[0].contour(gx, gy, Z1, levels=np.linspace(.2, 12, 8), colors=[PURPLE], linewidths=.8)
    p = np.array([1.8, 1.6]); path = [p.copy()]
    for _ in range(14):
        g = np.array([2 * p[0], 8 * p[1]]); p = p - 0.12 * g; path.append(p.copy())
    path = np.array(path)
    ax[0].plot(path[:, 0], path[:, 1], "o-", color=CORAL, ms=2.5, lw=1.2)
    ax[0].set_title("양정치 — 그릇\n경사하강이 지그재그", fontsize=8.5)
    Z2 = gx**2 - gy**2
    ax[1].contour(gx, gy, Z2, levels=[-3, -1.5, -.4, .4, 1.5, 3], colors=[PURPLE], linewidths=.8)
    ax[1].plot(0, 0, "o", color=CORAL, ms=5)
    ax[1].set_title("부정치 — 안장점", fontsize=8.5)
    Z3 = (gx + gy)**2
    ax[2].contour(gx, gy, Z3, levels=[.2, 1, 3, 6], colors=[PURPLE], linewidths=.8)
    ax[2].set_title("준정치 — 평평한 방향", fontsize=8.5)
    for a in ax:
        plane(a, 2.0, grid=False)
    save(fig, "ch17", "f1_hessian.png")

# ── 18장 ────────────────────────────────────────────────────────
def ch18():
    N = 64; n = np.arange(N)
    fig, ax = plt.subplots(1, 4, figsize=(8.6, 1.9))
    for a, k in zip(ax, [0, 1, 3, 8]):
        a.plot(n, np.cos(2 * np.pi * k * n / N), color=PURPLE, lw=1.4)
        a.plot(n, np.sin(2 * np.pi * k * n / N), color=TEAL, lw=1.0, ls="--")
        a.set_title(f"$f_{{{k}}}$", fontsize=9); a.set_xticks([]); a.set_yticks([])
        for s in a.spines.values(): s.set_visible(False)
        a.axhline(0, color="#DDD", lw=.7)
    fig.suptitle("푸리에 기저 — 실수부(보라)·허수부(청록)", fontsize=9, y=1.08)
    save(fig, "ch18", "f1_fourier_basis.png")

    rng = np.random.default_rng(0)
    N = 128; n = np.arange(N)
    x = np.sin(2 * np.pi * 3 * n / N) + .6 * np.sin(2 * np.pi * 20 * n / N) \
        + .4 * rng.normal(size=N)
    h = np.zeros(N); h[:9] = 1 / 9.
    y = np.real(np.fft.ifft(np.fft.fft(x) * np.fft.fft(h)))
    fig, ax = plt.subplots(1, 3, figsize=(8.4, 2.2))
    ax[0].plot(x, color=GREY, lw=.9); ax[0].plot(y, color=PURPLE, lw=1.6)
    ax[0].set_title("시간 영역 — 원신호와 평활", fontsize=8.5)
    ax[1].stem(np.abs(np.fft.fft(x))[:N // 2], linefmt=GREY, markerfmt=" ", basefmt=" ")
    ax[1].set_title("$|\\hat{x}|$ — 주파수 성분", fontsize=8.5)
    ax[2].plot(np.abs(np.fft.fft(h))[:N // 2], color=TEAL, lw=1.6)
    ax[2].set_title("$|\\hat{h}|$ — 저역통과 필터", fontsize=8.5)
    for a in ax:
        a.set_xticks([]); a.set_yticks([])
        for s in ("top", "right"): a.spines[s].set_visible(False)
    fig.suptitle("컨볼루션 = 주파수 영역의 원소별 곱", fontsize=9, y=1.05)
    save(fig, "ch18", "f2_convolution.png")


if __name__ == "__main__":
    for f in (ch09, ch11, ch12, ch13, ch14, ch15, ch16, ch17, ch18):
        print(f.__name__); f()
