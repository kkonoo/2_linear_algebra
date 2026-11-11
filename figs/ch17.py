"""17장 그림. 헤시안 세 경우 — ① x²+4y²(양정치), ② x²−y²(부정치), ③ (x+y)²(준정치). 연습문제 3·4와 같은 함수.

실행: cd figs && python3 ch17.py
"""
from lafig import *


def _note(ax, x, y, text, ha="left", va="bottom", c=TEXT2, rot=0):
    """등고선 위에 얹는 짧은 설명(흰 바탕으로 선과 겹치지 않게)."""
    ax.text(x, y, text, fontsize=11, color=c, ha=ha, va=va, rotation=rot, zorder=7,
            bbox=dict(fc="white", ec="none", pad=1.5))


def f1_hessian():
    U = 0.55
    L = (-2, 2)
    gx, gy = np.meshgrid(np.linspace(-2, 2, 300), np.linspace(-2, 2, 300))
    fig = canvas(7.9, 2.95)
    y0 = 0.3
    xs = (0.1, 2.75, 5.4)
    kw = dict(colors=[CAT[0]], linewidths=1.0, linestyles="solid", zorder=2)

    # ① 양정치 — 그릇, 경사하강이 지그재그
    a = plane(fig, xs[0], y0, L, L, unit=U, grid=False)
    a.contour(gx, gy, gx**2 + 4 * gy**2, levels=np.linspace(.2, 12, 8), **kw)
    p = np.array([1.8, 1.6]); path = [p.copy()]
    for _ in range(10):                       # 학습률 0.23: y 방향이 매 단계 부호를 바꿈
        g = np.array([2 * p[0], 8 * p[1]]); p = p - 0.23 * g; path.append(p.copy())
    path = np.array(path)
    a.plot(path[:, 0], path[:, 1], "-", color=ACCENT_INK, lw=1.6, zorder=5)
    a.plot(path[:, 0], path[:, 1], "o", color=ACCENT, ms=4.5, mec=ACCENT_INK, mew=0.8, zorder=6)
    a.plot(*path[0], "o", color=ACCENT, ms=7.5, mec=ACCENT_INK, mew=1.0, zorder=6)
    dot(a, (0, 0), color=TEXT, s=6)
    tag(a, "① 양정치 — 최솟값", y=1.04)

    # ② 부정치 — 안장점
    b = plane(fig, xs[1], y0, L, L, unit=U, grid=False)
    b.contour(gx, gy, gx**2 - gy**2, levels=[-3, -1.5, -.4, .4, 1.5, 3], **kw)
    dot(b, (0, 0), color=TEXT, s=7)
    _note(b, 0.12, 0.1, "안장점", c=TEXT)
    tag(b, "② 부정치 — 안장점", y=1.04)

    # ③ 준정치 — 평평한 방향 (x + y = 0 위에서 이차항이 0)
    c = plane(fig, xs[2], y0, L, L, unit=U, grid=False)
    c.contour(gx, gy, (gx + gy)**2, levels=[.2, 1, 3, 6], **kw)
    line(c, 1, 1, 0, color=TEXT2, lw=1.6, ls=(0, (4, 3)))
    c.text(2.0, -2.08, "평평한 방향", fontsize=11, color=TEXT2, ha="right", va="top")
    tag(c, "③ 준정치 — 판정 불가", y=1.04)

    save(fig, out("ch17", "f1_hessian.png"))


if __name__ == "__main__":
    f1_hessian()
