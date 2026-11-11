"""6장 그림. 행렬식 = 부피 배율(f1), 거의 평행한 두 열(f2) — 원본 fig_part1.py ch06()의 예시 유지.

실행: cd figs && python3 ch06.py
"""
from lafig import *

FILL = mix(CAT[0], 0.22)        # 변환 후 평행사변형 (두 그림 공통)
EDGE = mix(CAT[0], 0.6)         # 평행사변형의 나머지 두 변
SQ = TEXT2                      # 단위정사각형(변환 전, 중립)


def _frame(ax):
    """패널 전체 범위를 차지하는 보이지 않는 틀 — save()가 수평·수직 격자선(폭 0)을
    자를 범위에서 빼므로, 이것으로 패널 끝까지 저장되게 한다."""
    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    ax.add_patch(mp.Rectangle((x0, y0), x1 - x0, y1 - y0, fc="none", ec="none", zorder=0))


def _unit_square(ax):
    ax.add_patch(mp.Polygon([(0, 0), (1, 0), (1, 1), (0, 1)], closed=True, fc="none",
                            ec=SQ, lw=1.1, ls=(0, (4, 3)), zorder=3))


def _para(ax, M):
    a1, a2 = M[:, 0], M[:, 1]
    if abs(np.linalg.det(M)) < 1e-9:           # 넓이 0 — 선분으로 무너짐
        s = a1 + a2
        ax.plot([0, s[0]], [0, s[1]], color=EDGE, lw=4.5, solid_capstyle="butt", zorder=2)
    else:
        ax.add_patch(mp.Polygon([(0, 0), tuple(a1), tuple(a1 + a2), tuple(a2)], closed=True,
                                fc=FILL, ec=EDGE, lw=1.3, zorder=2))


def f1_determinant_area():
    U = 0.62
    XL, YL = (-0.4, 3.4), (-0.4, 2.0)
    pw = (XL[1] - XL[0]) * U
    gap = 0.29
    mats = [(np.eye(2), "① $\\det=1$",
             dict(o1=(2, -3), h1="left", v1="top", o2=(-4, 2), h2="right", v2="bottom")),
            (np.array([[2, 0], [0, 1.5]]), "② $\\det=3$",
             dict(o1=(2, -3), h1="left", v1="top", o2=(-4, 2), h2="right", v2="bottom")),
            (np.array([[1, 1], [0, 1.]]), "③ $\\det=1$ · 전단",
             dict(o1=(2, -3), h1="left", v1="top", o2=(-4, 4), h2="right", v2="bottom")),
            (np.array([[0, 1], [1, 0.]]), "④ $\\det=-1$ · 반사",
             dict(o1=(-4, 2), h1="right", v1="bottom", o2=(2, -3), h2="left", v2="top")),
            (np.array([[1, 2], [0.5, 1.]]), "⑤ $\\det=0$ · 붕괴",
             dict(o1=(4, -6), h1="left", v1="top", o2=(-4, 6), h2="right", v2="bottom"))]
    x_row1 = [0.2 + i * (pw + gap) for i in range(3)]
    mid = (x_row1[0] + x_row1[2] + pw) / 2
    x0 = mid - (2 * pw + gap) / 2
    pos = [(x, 2.55) for x in x_row1] + [(x0, 0.3), (x0 + pw + gap, 0.3)]

    fig = canvas(8.1, 4.5)
    for (x, y), (M, t, o) in zip(pos, mats):
        a = plane(fig, x, y, XL, YL, unit=U)
        _frame(a)
        _para(a, M)
        _unit_square(a)
        if abs(np.linalg.det(M)) < 1e-9:       # 겹치는 두 열: 긴 a2 먼저, 짧은 a1 위에
            vec(a, M[:, 1], CAT[1], "$a_2$", off=o["o2"], ha=o["h2"], va=o["v2"])
            vec(a, M[:, 0], CAT[0], "$a_1$", off=o["o1"], ha=o["h1"], va=o["v1"], z=5)
        else:
            vec(a, M[:, 0], CAT[0], "$a_1$", off=o["o1"], ha=o["h1"], va=o["v1"])
            vec(a, M[:, 1], CAT[1], "$a_2$", off=o["o2"], ha=o["h2"], va=o["v2"])
        tag(a, t, y=1.04)
    save(fig, out("ch06", "f1_determinant_area.png"))


def f2_collinear():
    U = 0.9
    XL, YL = (-0.3, 2.3), (-0.35, 1.1)
    pw = (XL[1] - XL[0]) * U
    gap = 0.29
    marks = "①②③"
    fig = canvas(8.2, 2.0)
    for i, eps in enumerate([0.8, 0.25, 0.03]):
        M = np.array([[1, 1], [0, eps]])
        k = np.linalg.cond(M)
        a = plane(fig, 0.2 + i * (pw + gap), 0.3, XL, YL, unit=U)
        _frame(a)
        _para(a, M)
        vec(a, M[:, 0], CAT[0], "$a_1$", off=(2, -3), ha="left", va="top")
        vec(a, M[:, 1], CAT[1], "$a_2$", off=(-3, 5), ha="right", va="bottom", z=5)
        tag(a, f"{marks[i]} $\\det={eps:.2f}$ · $\\kappa\\approx{k:.0f}$", y=1.04)
    save(fig, out("ch06", "f2_collinear.png"))


if __name__ == "__main__":
    f1_determinant_area()
    f2_collinear()
