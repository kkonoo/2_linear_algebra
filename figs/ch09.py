"""9장 그림 — 최소제곱의 기하(정사영), 회귀 vs PCA, ridge vs lasso.

실행: cd figs && python3 ch09.py
"""
from lafig import *
import matplotlib.patches as mp


def f1_projection_colspace():
    """b를 열공간 C(A)(평면)에 정사영. 3D 대신 사선 투영으로 직접 그린다."""
    s = 1.35                                         # 1 단위 = s 인치
    ex, ey, ez = np.array([1.0, -0.2]), np.array([0.5, 0.4]), np.array([0.0, 1.0])
    o = np.array([1.65, 1.15])                       # 원점의 화면 위치(인치)

    def P(p):
        x, y, z = p
        return o + s * (x * ex + y * ey + z * ez)

    fig, ax = new(5.9, 3.7)
    # 열공간 C(A) — 평면
    corners = [P((-0.7, -0.7, 0)), P((2.1, -0.7, 0)), P((2.1, 1.7, 0)), P((-0.7, 1.7, 0))]
    ax.add_patch(mp.Polygon(corners, closed=True, fc=mix(PRIMARY, .15),
                            ec=mix(PRIMARY, .45), lw=1.0, zorder=1))
    label(ax, 5.3, 1.45, "$C(A)$", fs=13, c=TEXT2, ha="right")

    O = P((0, 0, 0))
    a1, a2 = np.array([1.3, -0.3, 0.]), np.array([-0.3, 1.3, 0.])
    bh = np.array([1.0, 0.7, 0.]); b = np.array([1.0, 0.7, 1.4])
    A1, A2, BH, B = P(a1), P(a2), P(bh), P(b)

    # 열벡터 a1, a2
    arrow(ax, *O, *A1, color=CAT[0], lw=2.2, ms=15, z=3)
    arrow(ax, *O, *A2, color=CAT[1], lw=2.2, ms=15, z=3)
    label(ax, A1[0] + 0.08, A1[1] - 0.05, "$a_1$", fs=13, c=CAT[0], ha="left", va="top")
    label(ax, A2[0] - 0.06, A2[1] + 0.04, "$a_2$", fs=13, c=CAT[1], ha="right", va="bottom")

    # 잔차 e (점선) + 직각 표시
    ax.plot([BH[0], B[0]], [BH[1], B[1]], color=TEXT2, lw=1.8, ls=(0, (4, 3)), zorder=3)
    label(ax, B[0] + 0.1, (BH[1] + B[1]) / 2, "$e$", fs=13, c=TEXT2, ha="left")
    m = 0.14
    u = -bh / np.linalg.norm(bh)
    zt = np.array([0, 0, 1.0])
    sq = [P(bh + m * u), P(bh + m * u + m * zt), P(bh + m * zt)]
    ax.plot([q[0] for q in sq], [q[1] for q in sq], color=TEXT2, lw=1.1, zorder=3)

    # 정사영 b̂ = Ax̂ (강조)
    arrow(ax, *O, *BH, color=ACCENT, lw=2.8, ms=16, z=4)
    label(ax, BH[0] + 0.13, BH[1] - 0.06, "$\\hat{b}=A\\hat{x}$", fs=13, c=ACCENT_INK,
          ha="left", va="center", w="bold")

    # 관측 b
    arrow(ax, *O, *B, color=TEXT, lw=2.6, ms=16, z=5)
    label(ax, B[0] + 0.1, B[1] - 0.02, "$b$", fs=14, c=TEXT, ha="left", va="center")

    ax.plot(*O, "o", color=TEXT, ms=4, zorder=6)
    save(fig, out("ch09", "f1_projection_colspace.png"))


def f2_regression_vs_pca():
    """설명용 가상 데이터 25점(시드 3)."""
    rng = np.random.default_rng(3)
    x = rng.normal(size=25); y = 0.9 * x + rng.normal(scale=.55, size=25)
    x -= x.mean(); y -= y.mean()
    beta = np.sum(x * y) / np.sum(x * x)
    C = np.cov(np.vstack([x, y])); w, V = np.linalg.eigh(C); d = V[:, -1]

    R = np.ceil((np.abs(np.r_[x, y]).max() + 0.3) * 2) / 2
    S = 3.4                                          # 패널 한 변(인치)
    U = S / (2 * R)
    fig = canvas(7.8, S + 0.7)
    a = plane(fig, 0.2, 0.2, (-R, R), (-R, R), unit=U, grid=False)
    b = plane(fig, 0.2 + S + 0.55, 0.2, (-R, R), (-R, R), unit=U, grid=False)

    # ① 회귀 — y 방향 거리
    for xi, yi in zip(x, y):
        a.plot([xi, xi], [yi, beta * xi], color=mix(CAT[0], .5), lw=1.3, zorder=2)
    line(a, beta, -1, 0, CAT[0], lw=2.4)
    a.text(0.97, 0.04, "회귀직선", transform=a.transAxes, color=CAT[0], fontsize=12,
           ha="right", va="bottom")
    tag(a, "① 회귀 — $y$ 방향 거리", y=1.03)

    # ② PCA — 직교거리
    for xi, yi in zip(x, y):
        p = (np.array([xi, yi]) @ d) * d
        b.plot([xi, p[0]], [yi, p[1]], color=mix(CAT[1], .5), lw=1.3, zorder=2)
    line(b, beta, -1, 0, mix(CAT[0], .55), lw=1.6, ls=(0, (4, 3)), z=2)
    line(b, -d[1], d[0], 0, CAT[1], lw=2.4)
    b.text(0.97, 0.13, "PC1", transform=b.transAxes, color=CAT[1], fontsize=12,
           ha="right", va="bottom")
    b.text(0.97, 0.04, "회귀직선(점선)", transform=b.transAxes, color=CAT[0], fontsize=12,
           ha="right", va="bottom")
    tag(b, "② PCA — 직교거리", y=1.03)

    for ax_ in (a, b):
        for xi, yi in zip(x, y):
            dot(ax_, (xi, yi), color=TEXT2, s=6, z=5)
    save(fig, out("ch09", "f2_regression_vs_pca.png"))


def f3_ridge_lasso():
    b0 = np.array([1.7, 1.1]); A = np.array([[1.0, .55], [.55, .8]]); r = .75
    xl, yl = (-1.1, 3.0), (-1.3, 2.4)
    U = 0.85
    Wp = (xl[1] - xl[0]) * U
    gx, gy = np.meshgrid(np.linspace(*xl, 300), np.linspace(*yl, 300))
    Z = (A[0, 0] * (gx - b0[0]) ** 2 + 2 * A[0, 1] * (gx - b0[0]) * (gy - b0[1])
         + A[1, 1] * (gy - b0[1]) ** 2)

    def Q(p):                                        # p: 2 × N
        dd = p - b0[:, None]
        return (dd * (A @ dd)).sum(0)

    tt = np.linspace(0, 2 * np.pi, 3601)
    circ = np.vstack([r * np.cos(tt), r * np.sin(tt)])
    Vd = np.array([[r, 0], [0, r], [-r, 0], [0, -r], [r, 0.]])
    t = np.linspace(0, 1, 1001)
    diam = np.hstack([(Vd[i][:, None] + t * (Vd[i + 1] - Vd[i])[:, None]) for i in range(4)])

    fig = canvas(8.2, (yl[1] - yl[0]) * U + 0.9)
    panels = [("① ridge — $L^2$ 공", circ, CAT[0], 0.2, False),
              ("② lasso — $L^1$ 마름모", diam, CAT[1], 0.2 + Wp + 0.45, True)]
    for name, shape, col, x0, key in panels:
        a = plane(fig, x0, 0.2, xl, yl, unit=U, grid=False)
        q = Q(shape); k = np.argmin(q); hit, Qs = shape[:, k], q[k]
        a.contour(gx, gy, Z, levels=list(Qs * np.array([0.12, 0.4, 0.75])),
                  colors=[mix(TEXT2, .45)], linewidths=1.0, zorder=1)
        a.contour(gx, gy, Z, levels=[Qs], colors=[TEXT2], linewidths=1.5, zorder=3)
        a.add_patch(mp.Polygon(shape.T, closed=True, fc=mix(col, .25), ec=col, lw=2.0, zorder=2))
        dot(a, b0, color=TEXT, s=7)
        a.annotate("$\\hat{\\beta}_{\\mathrm{OLS}}$", b0, xytext=(0, -8), textcoords="offset points",
                   fontsize=13, color=TEXT, ha="center", va="top", zorder=7)
        if key:
            dot(a, hit, color=ACCENT, s=11, z=8)
            zero = "$\\beta_2=0$" if abs(hit[1]) < 1e-9 else "$\\beta_1=0$"
            # 마름모와 접선 등고선 사이의 빈 곳에 두고 지시선으로 잇는다
            a.annotate(zero, hit, xytext=(0.78, -0.62), textcoords="data", fontsize=13,
                       color=ACCENT_INK, fontweight="bold", ha="center", va="center", zorder=8,
                       arrowprops=dict(arrowstyle="-", color=ACCENT_INK, lw=1.0,
                                       shrinkA=3, shrinkB=7))
        else:
            dot(a, hit, color=TEXT, s=8, z=8)
        # 축 이름은 패널 밖 축 끝에(등고선과 겹치지 않게)
        a.annotate("$\\beta_1$", (xl[1], 0), xytext=(4, 0), textcoords="offset points",
                   fontsize=13, color=TEXT2, ha="left", va="center", annotation_clip=False)
        a.annotate("$\\beta_2$", (0, yl[1]), xytext=(0, 3), textcoords="offset points",
                   fontsize=13, color=TEXT2, ha="center", va="bottom", annotation_clip=False)
        tag(a, name, y=1.11)
    save(fig, out("ch09", "f3_ridge_lasso.png"))


if __name__ == "__main__":
    f1_projection_colspace()
    f2_regression_vs_pca()
    f3_ridge_lasso()
