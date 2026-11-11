"""11장 그림. 예시 행렬 A = [[2,1],[1,2]] (연습문제 1, 고유값 3·1), 상관 그림은 원본 시드 2의 설명용 데이터.

실행: cd figs && python3 ch11.py
"""
from lafig import *


def f1_eigenvector():
    U = 0.6
    A = np.array([[2., 1.], [1., 2.]])
    v1 = np.array([1., 1.]) / np.sqrt(2)          # λ = 3
    v2 = np.array([-1., 1.]) / np.sqrt(2)         # λ = 1
    angs = np.linspace(0, np.pi, 9)[:-1]
    others = [k for k in range(8) if k not in (2, 6)]   # π/4, 3π/4은 고유벡터라 굵게 따로
    grey = mix(TEXT2, 0.55)

    fig = canvas(7.5, 2.75)
    ylim = (-0.6, 3.1)
    hb = (ylim[1] - ylim[0]) * U                  # ② 높이(인치)
    xa = (-1.8, 1.8); ya = (-0.6, 1.6)
    ha_ = (ya[1] - ya[0]) * U                      # ① 높이(인치)
    a = plane(fig, 0.3, 0.2, xa, ya, unit=U)
    b = plane(fig, 0.3 + (xa[1] - xa[0]) * U + 0.5, 0.2, (-2.8, 4.7), ylim, unit=U)

    for ax, M in ((a, np.eye(2)), (b, A)):
        # 고유 방향 안내선(옅은 점선)
        line(ax, 1, -1, 0, mix(CAT[0], 0.35), lw=1.0, ls=(0, (4, 3)), z=1)
        line(ax, 1, 1, 0, mix(CAT[1], 0.35), lw=1.0, ls=(0, (4, 3)), z=1)
        for k in others:
            u = np.array([np.cos(angs[k]), np.sin(angs[k])]) * 1.2
            vec(ax, M @ u, grey, lw=1.2, z=2)

    # ① 변환 전
    vec(a, v1 * 1.2, CAT[0], "$v_1$", lw=2.6, off=(8, 0), va="center")
    vec(a, v2 * 1.2, CAT[1], "$v_2$", lw=2.6, off=(-8, 0), ha="right", va="center")
    tag(a, "① 변환 전", y=(hb * 1.04) / ha_)

    # ② 변환 후 Ax
    vec(b, A @ v1 * 1.2, CAT[0], "$Av_1 = 3v_1$", lw=2.6, off=(12, -3), va="center")
    vec(b, A @ v2 * 1.2, CAT[1], "$Av_2 = v_2$", lw=2.6, off=(-6, -4), ha="right", va="top")
    tag(b, "② 변환 후 $Ax$", y=1.04)
    save(fig, out("ch11", "f1_eigenvector.png"))


def f2_correlation_cosine():
    """설명용 가상 데이터 12쌍(원본 시드 2)."""
    rng = np.random.default_rng(2)
    x = rng.normal(size=12); y = .75 * x + rng.normal(scale=.6, size=12)
    a_, b_ = x - x.mean(), y - y.mean()
    r = a_ @ b_ / (np.linalg.norm(a_) * np.linalg.norm(b_))
    th = np.arccos(r)
    c, s = np.cos(th), np.sin(th)

    fig = canvas(4.7, 3.9)
    ax = plane(fig, 0.2, 0.2, (-0.2, 1.75), (-0.45, 1.15), unit=2.2, grid=False, axes=False)

    # b를 a 방향으로 내린 그림자
    ax.plot([c, c], [s, 0], color=mix(TEXT2, 0.5), lw=1.2, ls=(0, (2, 2)), zorder=2)
    q = 0.05
    ax.plot([c - q, c - q, c], [0, q, q], color=mix(TEXT2, 0.5), lw=1.0, zorder=2)

    vec(ax, (1, 0), CAT[0], "$a$ (편차)", lw=2.6, off=(8, 0), va="center")
    vec(ax, (c, s), CAT[1], "$b$ (편차)", lw=2.6, off=(6, 4))
    dot(ax, (0, 0), color=TEXT2, s=5)

    arc = np.linspace(0, th, 60)
    ax.plot(0.22 * np.cos(arc), 0.22 * np.sin(arc), color=TEXT2, lw=1.2, zorder=3)
    ax.text(0.3 * np.cos(th / 2), 0.3 * np.sin(th / 2), r"$\theta$", color=TEXT2, fontsize=13,
            ha="left", va="center")

    # 그림자 길이 = cosθ = r  (강조 한 곳)
    y0, t = -0.11, 0.035
    ax.plot([0, r], [y0, y0], color=ACCENT, lw=4, solid_capstyle="butt", zorder=3)
    for xx in (0, r):
        ax.plot([xx, xx], [y0 - t, y0 + t], color=ACCENT_INK, lw=1.4, zorder=4)
    ax.text(r / 2, y0 - 0.06, f"$r=\\cos\\theta={r:.2f}$", color=ACCENT_INK, fontsize=13,
            fontweight="bold", ha="center", va="top")
    save(fig, out("ch11", "f2_correlation_cosine.png"))


if __name__ == "__main__":
    f1_eigenvector()
    f2_correlation_cosine()
