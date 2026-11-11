"""14장 그림. 예제 벡터는 원래 그림 그대로 a1 = (2, 1), a2 = (1.2, 2.4).

실행: cd figs && python3 ch14.py
"""
from lafig import *


def right_angle(ax, d1, d2, s=0.2, start=(0, 0), color=TEXT2):
    """start에서 단위방향 d1, d2 사이의 직각 표시."""
    o = np.array(start, float)
    d1, d2 = np.asarray(d1, float), np.asarray(d2, float)
    pts = np.array([o + s * d1, o + s * (d1 + d2), o + s * d2])
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=1.2, zorder=3)


def f1_gram_schmidt():
    a1 = np.array([2.0, 1.0]); a2 = np.array([1.2, 2.4])
    u1 = a1; q1 = u1 / np.linalg.norm(u1)
    p = (q1 @ a2) * q1                      # proj_{u1}(a2) = (1.92, 0.96)
    u2 = a2 - p; q2 = u2 / np.linalg.norm(u2)
    n = np.array([q1[1], -q1[0]])           # u1에 수직, 오른쪽 아래 방향

    U = 0.68
    XL, YL = (-1.0, 2.7), (-0.6, 2.8)
    fig = canvas(8.4, 2.9)
    GREY = mix(TEXT2, 0.55)

    # ① 주어진 벡터
    a = plane(fig, 0.15, 0.2, XL, YL, unit=U)
    vec(a, a1, CAT[0], "$a_1$", off=(6, 0), va="center")
    vec(a, a2, CAT[1], "$a_2$", off=(6, 0), va="center")
    tag(a, "① 주어진 벡터", y=1.04)

    # ② a2에서 u1 방향 성분(사영)을 뺀다
    b = plane(fig, 2.95, 0.2, XL, YL, unit=U)
    vec(b, a2, GREY, "$a_2$", lw=1.6, off=(6, 0), va="center", z=3)
    vec(b, u1, CAT[0], "$u_1$", off=(6, 2), va="bottom")
    off = 0.22 * n                          # 사영은 u1과 겹치지 않게 평행하게 옮겨 그린다
    vec(b, p, ACCENT, start=off, lw=2.4, z=5)
    b.text(1.25, -0.12, "$\\mathrm{proj}_{u_1}a_2$", color=ACCENT_INK, fontsize=12,
           fontweight="bold", ha="center", va="top")
    b.plot([p[0], a2[0]], [p[1], a2[1]], color=CAT[1], lw=1.4, ls=(0, (3, 2)), zorder=3)
    vec(b, u2, CAT[1], "$u_2$", off=(-6, 2), ha="right", va="bottom")
    right_angle(b, q1, q2, s=0.22)
    tag(b, "② 사영 성분 빼기", y=1.04)

    # ③ 정규화 — 길이를 1로 (점선 호: q1, q2 끝이 같은 단위원 위)
    c = plane(fig, 5.75, 0.2, XL, YL, unit=U)
    t1, t2 = np.arctan2(q1[1], q1[0]), np.arctan2(q2[1], q2[0])
    th = np.linspace(t1, t2, 120)
    c.plot(np.cos(th), np.sin(th), color=mix(TEXT2, 0.45), lw=1.0, ls=(0, (2, 2)), zorder=2)
    vec(c, u1, GREY, "$u_1$", lw=1.4, off=(6, 0), va="center", z=3)
    vec(c, u2, GREY, "$u_2$", lw=1.4, off=(-6, 2), ha="right", va="bottom", z=3)
    vec(c, q1, CAT[0], "$q_1$", off=(4, -4), va="top")
    vec(c, q2, CAT[1], "$q_2$", off=(-7, -9), ha="right", va="top")
    right_angle(c, q1, q2, s=0.2)
    tag(c, "③ 정규화", y=1.04)

    save(fig, out("ch14", "f1_gram_schmidt.png"))


if __name__ == "__main__":
    f1_gram_schmidt()
