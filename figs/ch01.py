"""1장 그림 — 벡터의 세 시각, span, 선형독립·종속. 실행: cd figs && python3 ch01.py"""
from lafig import *
import matplotlib.patches as mp

V1, V2 = np.array([1, 2]), np.array([3, 1])
XL, YL, U = (-2.5, 3.5), (-2.0, 4.5), 0.5          # f2·f3 공통 범위와 축척
SPAN = mix(PRIMARY, 0.25)                            # span{v1} 직선(옅은 띠)


def inch_axes(fig, x, y, w, h, xlim, ylim):
    """(x, y) 인치에서 시작하는 w × h 인치의 축 없는 패널."""
    W, H = fig.get_size_inches()
    ax = fig.add_axes([x / W, y / H, w / W, h / H])
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")
    return ax


def frame(ax):
    """보이지 않는 패널 테두리 — 수평·수직 격자선은 save()의 잘라내기 범위에 안 들어가므로
    패널 전체가 저장되도록 범위를 잡아 준다."""
    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    ax.add_patch(mp.Rectangle((x0, y0), x1 - x0, y1 - y0, fc="none", ec="none", zorder=0))


def lattice(ax, a, b, step, color="white", lw=1.0, z=0.5):
    """a·x + b·y = k·step 꼴의 평행선 중 패널을 지나는 것만 그린다."""
    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    vals = [a * x + b * y for x in (x0, x1) for y in (y0, y1)]
    lo, hi = min(vals), max(vals)
    for k in range(math.ceil(lo / step), math.floor(hi / step) + 1):
        c = k * step
        if lo + 1e-6 < c < hi - 1e-6:
            line(ax, a, b, c, color, lw=lw, z=z)


def f1_three_views():
    fig = canvas(8.4, 2.6)
    u, xl, yl = 0.4, (-3, 3), (-2.5, 2.5)

    # ① 화살표 — 자리를 옮겨도 같은 벡터
    a = plane(fig, 0.1, 0.2, xl, yl, unit=u)
    frame(a)
    vec(a, (2, 1), TEXT2, start=(-2.5, -2), lw=2.0)
    a.annotate("$v$", (-1.5, -1.5), xytext=(-6, 6), textcoords="offset points",
               fontsize=13, color=TEXT2, ha="right", va="bottom")
    vec(a, (2, 1), PRIMARY, "$v$")
    tag(a, "① 화살표", y=1.04)

    # ② 좌표 — 기저에 대한 계수
    b = plane(fig, 2.95, 0.2, xl, yl, unit=u)
    frame(b)
    b.plot([2, 2], [0, 1], color=CAT[1], ls=":", lw=1.6, zorder=3)
    b.plot([0, 2], [1, 1], color=CAT[1], ls=":", lw=1.6, zorder=3)
    vec(b, (2, 1), PRIMARY, "$v$")
    b.annotate("2", (2, 0), xytext=(0, -4), textcoords="offset points", fontsize=13,
               color=CAT[1], ha="center", va="top")
    b.annotate("1", (0, 1), xytext=(-5, 0), textcoords="offset points", fontsize=13,
               color=CAT[1], ha="right", va="center")
    tag(b, "② 좌표", y=1.04)

    # ③ 데이터 — 숫자 리스트 (설명용 가상 발현량)
    c = inch_axes(fig, 5.8, 0.2, 2.4, 2.0, (0, 5.4), (-0.7, 3.9))
    vals = [2.1, 0.4, 3.3, 1.2, 2.7]
    c.plot([0.55, 5.35], [0, 0], color=AXIS, lw=1.0, zorder=1)
    c.plot([0.55, 0.55], [0, 3.7], color=AXIS, lw=1.0, zorder=1)
    for i, h in enumerate(vals):
        x = 1.15 + 0.95 * i
        c.add_patch(mp.Rectangle((x - 0.275, 0), 0.55, h, fc=PRIMARY, ec="none", zorder=2))
        c.text(x, h + 0.08, f"{h}", fontsize=11, color=TEXT2, ha="center", va="bottom")
        c.text(x, -0.1, f"g{i + 1}", fontsize=11, color=TEXT2, ha="center", va="top")
    c.text(0.3, 1.7, "발현량", fontsize=11, color=TEXT2, rotation=90, ha="center", va="center")
    tag(c, "③ 데이터", y=1.04)
    save(fig, out("ch01", "f1_three_views.png"))


def f2_span():
    fig = canvas(7.0, 3.85)
    # ① span{v1} — 직선
    a = plane(fig, 0.1, 0.25, XL, YL, unit=U)
    frame(a)
    line(a, 2, -1, 0, SPAN, lw=8, z=2)
    vec(a, V1, CAT[0], "$v_1$", off=(-8, 0), ha="right", va="center")
    tag(a, r"① span$\{v_1\}$ — 직선", y=1.02)

    # ② span{v1, v2} — 평면 전체
    b = plane(fig, 3.6, 0.25, XL, YL, unit=U, grid=False)
    b.add_patch(mp.Rectangle((XL[0], YL[0]), XL[1] - XL[0], YL[1] - YL[0],
                             fc=mix(PRIMARY, 0.15), ec="none", zorder=0))
    lattice(b, 2, -1, 2.5)          # v1 방향 평행선
    lattice(b, 1, -3, 2.5)          # v2 방향 평행선
    vec(b, V1, CAT[0], "$v_1$", off=(-8, 0), ha="right", va="center")
    vec(b, V2, CAT[1], "$v_2$", off=(-4, 6), ha="right", va="bottom")
    tag(b, r"② span$\{v_1,v_2\}$ — 평면 전체", y=1.02)
    save(fig, out("ch01", "f2_span.png"))


def f3_independence():
    fig = canvas(7.0, 3.85)
    # ① 선형독립 — v2가 v1의 직선을 벗어난다
    a = plane(fig, 0.1, 0.25, XL, YL, unit=U)
    frame(a)
    line(a, 2, -1, 0, SPAN, lw=8, z=2)
    vec(a, V1, CAT[0], "$v_1$", off=(-8, 0), ha="right", va="center")
    vec(a, V2, CAT[1], "$v_2$", off=(-4, 6), ha="right", va="bottom")
    tag(a, "① 선형독립 — 새 방향을 준다", y=1.02)

    # ② 선형종속 — v2 = 2v1은 같은 직선 위
    b = plane(fig, 3.6, 0.25, XL, YL, unit=U)
    frame(b)
    line(b, 2, -1, 0, SPAN, lw=8, z=2)
    vec(b, 2 * V1, CAT[1], "$v_2=2v_1$", off=(-8, 0), ha="right", va="center", z=4)
    vec(b, V1, CAT[0], "$v_1$", lw=3.0, off=(-8, 0), ha="right", va="center", z=6)
    tag(b, "② 선형종속 — span이 그대로", y=1.02)
    save(fig, out("ch01", "f3_independence.png"))


if __name__ == "__main__":
    f1_three_views()
    f2_span()
    f3_independence()
