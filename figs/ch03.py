"""3장 그림 — 행벡터의 등고선·정사영(f1), 노름별 단위원(f2).

실행: cd figs && python3 ch03.py
"""
from lafig import *

U = 0.62                                   # f1 두 패널 공통 축척


def _right_angle(ax, p, d1, d2, s=0.15, color=TEXT2):
    """p에서 단위벡터 d1, d2 방향으로 그린 직각 표시."""
    p, d1, d2 = (np.asarray(v, float) for v in (p, d1, d2))
    pts = np.array([p + s * d1, p + s * (d1 + d2), p + s * d2])
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=1.1, zorder=3)


def f1_rowvector_projection():
    fig = canvas(6.6, 3.0)
    ylim = (-1.3, 2.8)
    a = np.array([2., 1.])
    u = a / np.linalg.norm(a)              # 행벡터 방향
    n = np.array([-1., 2.]) / np.sqrt(5)   # 등고선 방향(행벡터에 수직)
    white = dict(fc="white", ec="none", pad=0.6)

    # ① 행벡터 [2 1]과 등고선 2x + y = c
    L = plane(fig, 0.2, 0.2, (-1.6, 3.4), ylim, unit=U)
    for c in range(-4, 9, 2):
        line(L, 2, 1, c, mix(CAT[0], .45), lw=1.3, z=2)
    y = 2.45
    for c in (0, 2, 4, 6):
        L.text((c - y) / 2 + 0.12, y, f"$c={c}$", fontsize=11, color=TEXT2,
               ha="left", va="center", bbox=white, zorder=4)
    vec(L, a, CAT[0], lw=2.6, z=5)
    L.text(1.75, 1.55, r"$[2\;\;1]$", fontsize=13, color=CAT[0], ha="center", va="center",
           bbox=white, zorder=6)
    _right_angle(L, 0.8 * a, -u, n)        # 벡터가 c=4 등고선과 만나는 점
    tag(L, r"① 행벡터 $[2\;\;1]$의 등고선", y=1.03)

    # ② 내적 = 정사영 길이 × |a|
    R = plane(fig, 3.75, 0.2, (-0.6, 3.6), ylim, unit=U)
    b = np.array([2.6, 0.6])
    p = (b @ u) * u                        # b를 a 방향으로 정사영한 벡터
    R.plot([a[0], p[0]], [a[1], p[1]], color=mix(TEXT2, .5), lw=1.2, ls=(0, (3, 2)), zorder=2)
    R.plot([b[0], p[0]], [b[1], p[1]], color=TEXT2, lw=1.2, ls=(0, (2, 2)), zorder=3)
    _right_angle(R, p, -u, -n, s=0.14)
    # 정사영 길이 — 치수 막대
    off = 0.5 * n
    ext = mix(TEXT2, .35)
    for q in (np.zeros(2), p):
        R.plot([q[0], q[0] + 0.62 * n[0]], [q[1], q[1] + 0.62 * n[1]], color=ext, lw=1.0, zorder=2)
    s0, s1 = off, p + off
    R.plot([s0[0], s1[0]], [s0[1], s1[1]], color=ACCENT, lw=4.5, solid_capstyle="butt", zorder=4)
    mid = (s0 + s1) / 2 + 0.12 * n
    R.text(mid[0], mid[1], r"정사영 길이 $|b|\cos\theta$", fontsize=12, color=ACCENT_INK,
           fontweight="bold", rotation=np.degrees(np.arctan2(a[1], a[0])), rotation_mode="anchor",
           ha="center", va="bottom", zorder=5)
    # 각 θ
    t1, t2 = np.degrees(np.arctan2(b[1], b[0])), np.degrees(np.arctan2(a[1], a[0]))
    R.add_patch(mp.Arc((0, 0), 2.4, 2.4, theta1=t1, theta2=t2, color=TEXT2, lw=1.2, zorder=3))
    tm = np.radians((t1 + t2) / 2)
    R.text(1.6 * np.cos(tm), 1.6 * np.sin(tm), r"$\theta$", fontsize=12, color=TEXT2,
           ha="center", va="center", zorder=5)
    vec(R, a, CAT[0], lw=2.6, z=5)
    vec(R, b, CAT[1], "$b$", lw=2.6, off=(6, 0), va="center", z=5)
    la = 0.5 * a + 0.2 * n
    R.text(la[0], la[1], "$a$", fontsize=13, color=CAT[0], ha="center", va="center", zorder=6)
    R.text(1.5, -0.55, r"$a^{\top}\!b = |a|\,|b|\cos\theta$", fontsize=13, color=TEXT,
           ha="center", va="center", bbox=white, zorder=5)
    R.text(1.5, -0.98, r"$=$ (정사영 길이) $\times\,|a|$", fontsize=12, color=TEXT2,
           ha="center", va="center", bbox=white, zorder=5)
    tag(R, "② 내적과 정사영", y=1.03)
    save(fig, out("ch03", "f1_rowvector_projection.png"))


def f2_norms():
    t = np.linspace(0, 2 * np.pi, 400)
    shapes = [("① $L^1$ — 마름모", np.array([[1, 0, -1, 0, 1], [0, 1, 0, -1, 0.]]),
               r"$|x|+|y|=1$"),
              ("② $L^2$ — 원", np.vstack([np.cos(t), np.sin(t)]),
               r"$\sqrt{x^2+y^2}=1$"),
              (r"③ $L^\infty$ — 정사각형", np.array([[1, 1, -1, -1, 1], [1, -1, -1, 1, 1.]]),
               r"$\max(|x|,|y|)=1$")]
    fig = canvas(7.9, 3.1)
    for i, (name, s, eq) in enumerate(shapes):
        a = plane(fig, 0.15 + i * 2.6, 0.5, (-1.6, 1.6), (-1.6, 1.6), unit=0.75)
        c = CAT[i]
        a.add_patch(mp.Polygon(s.T, closed=True, fc=mix(c, .2), ec="none", zorder=0.5))
        a.plot(s[0], s[1], color=c, lw=2.2, zorder=3)
        a.text(1.06, -0.07, "1", fontsize=11, color=TEXT2, ha="left", va="top", zorder=5)
        a.text(-0.07, 1.06, "1", fontsize=11, color=TEXT2, ha="right", va="bottom", zorder=5)
        a.text(0.5, -0.04, eq, transform=a.transAxes, fontsize=12, color=TEXT2,
               ha="center", va="top")
        tag(a, name, y=1.03)
    save(fig, out("ch03", "f2_norms.png"))


if __name__ == "__main__":
    f1_rowvector_projection()
    f2_norms()
