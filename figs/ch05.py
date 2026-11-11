"""5장 그림. 예제는 본문 §1-2의 B = [[3,-1],[1,2]], v = (5,4), [v]_B = (2,1).
표준기저 = CAT[0], 새 기저 = CAT[1] (장 전체에서 같은 뜻).

실행: cd figs && python3 ch05.py
"""
from lafig import *


def f1_two_coordinates():
    U = 0.48
    fig = canvas(8.0, 3.3)
    e1, e2 = np.array([1, 0]), np.array([0, 1])
    b1, b2 = np.array([3, 1]), np.array([-1, 2])
    v = np.array([5, 4])
    dash = (0, (3, 2))
    note = dict(fontsize=13, color=TEXT, ha="left", va="top", linespacing=1.6, zorder=6,
                bbox=dict(fc="white", ec="none", pad=1.5))

    # ① 표준기저 — v = 5e1 + 4e2
    a = plane(fig, 0.2, 0.25, (-1.0, 5.8), (-0.8, 4.8), unit=U)
    vec(a, 5 * e1, CAT[0], lw=1.4, ls=dash, z=2)
    vec(a, 4 * e2, CAT[1], start=5 * e1, lw=1.4, ls=dash, z=2)
    vec(a, e1, CAT[0], "$e_1$", off=(0, -5), ha="center", va="top")
    vec(a, e2, CAT[1], "$e_2$", off=(-5, 0), ha="right", va="center")
    vec(a, v, TEXT, "$v$", lw=2.6, off=(6, 0), va="center")
    a.text(3.0, -0.2, "$5e_1$", color=CAT[0], fontsize=12, ha="center", va="top")
    a.text(5.15, 2.0, "$4e_2$", color=CAT[1], fontsize=12, ha="left", va="center")
    a.text(-0.85, 4.65, "$v = 5e_1 + 4e_2$\n좌표 $(5,\\,4)$", **note)
    tag(a, "① 표준기저", y=1.04)

    # ② 새 기저 — v = 2b1 + 1b2, 기울어진 격자
    b = plane(fig, 3.85, 0.25, (-1.6, 6.6), (-0.8, 4.8), unit=U, grid=False, axes=False)
    for k in (-1, 0, 1, 2):          # b1 방향 격자선: x − 3y = −7k (k·b2를 지남)
        line(b, 1, -3, -7 * k, color=mix(CAT[1], .6 if k == 0 else .3),
             lw=1.0 if k == 0 else 0.8, z=0)
    for k in (0, 1, 2):              # b2 방향 격자선: 2x + y = 7k (k·b1을 지남)
        line(b, 2, 1, 7 * k, color=mix(CAT[1], .6 if k == 0 else .3),
             lw=1.0 if k == 0 else 0.8, z=0)
    vec(b, 2 * b1, CAT[0], lw=1.4, ls=dash, z=2)
    vec(b, b2, CAT[1], start=2 * b1, lw=1.4, ls=dash, z=2)
    vec(b, b1, CAT[0], "$b_1$", off=(2, -6), va="top")
    vec(b, b2, CAT[1], "$b_2$", off=(-2, 4), ha="right", va="bottom")
    vec(b, v, TEXT, lw=2.6)
    # v 끝점을 격자선 두 개가 지나므로 라벨에 흰 바탕을 깐다
    b.annotate("$v$", tuple(v), xytext=(7, 6), textcoords="offset points", fontsize=13,
               color=TEXT, ha="left", va="bottom", zorder=6,
               bbox=dict(fc="white", ec="none", pad=1.0))
    b.text(4.7, 1.2, "$2b_1$", color=CAT[0], fontsize=12, ha="left", va="top")
    b.text(5.35, 3.0, "$+\\,1b_2$", color=CAT[1], fontsize=12, ha="right", va="center")
    b.text(-1.45, 4.65, "$v = 2b_1 + 1b_2$\n좌표 $[v]_B=(2,\\,1)$", **note)
    tag(b, "② 새 기저", y=1.04)
    save(fig, out("ch05", "f1_two_coordinates.png"))


def f2_similarity():
    fig, ax = new(8.3, 2.5)
    std, nb = mix(CAT[0], .2), mix(CAT[1], .28)
    boxes = [("$[v]_P$", "새 기저 좌표", nb, CAT[1]),
             ("$v$", "표준좌표", std, CAT[0]),
             ("$Av$", "표준좌표", std, CAT[0]),
             ("$[Av]_P$", "새 기저 좌표", nb, CAT[1])]
    ops = [("$P$", "번역"), ("$A$", "작업"), ("$P^{-1}$", "재번역")]
    W, H, G, y0 = 1.5, 0.95, 0.7, 1.2
    for i, (m, s, fc, ec) in enumerate(boxes):
        x = 0.1 + i * (W + G)
        box(ax, x, y0, W, H, fc=fc, ec=ec, lw=1.4)
        label(ax, x + W / 2, y0 + 0.62, m, fs=15)
        label(ax, x + W / 2, y0 + 0.25, s, fs=11, c=TEXT2)
        if i < 3:
            xa, xb = x + W + 0.06, x + W + G - 0.06
            arrow(ax, xa, y0 + H / 2, xb, y0 + H / 2, color=TEXT2)
            label(ax, (xa + xb) / 2, y0 + H / 2 + 0.24, ops[i][0], fs=13)
            label(ax, (xa + xb) / 2, y0 + H / 2 - 0.24, ops[i][1], fs=11, c=TEXT2)
    # 세 단계를 한 번에 — 새 기저에서 본 같은 변환
    arrow(ax, 0.1 + W / 2, y0 - 0.06, 0.1 + 3 * (W + G) + W / 2, y0 - 0.06,
          color=TEXT, lw=1.6, rad=0.12)
    label(ax, 4.15, 0.62, "$A' = P^{-1}AP$ — 같은 변환을 새 기저에서", fs=13, va="top")
    save(fig, out("ch05", "f2_similarity.png"))


if __name__ == "__main__":
    f1_two_coordinates()
    f2_similarity()
