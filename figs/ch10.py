"""10장 그림 (새로 그림). 최소노름 해 — 본문 §5-2.

실행: cd figs && python3 ch10.py
"""
from lafig import *


def f1_min_norm():
    U = 0.75
    fig = canvas(7.0, 4.1)
    a = plane(fig, 0.3, 0.2, (-1.5, 4.5), (-1.5, 3.5), unit=U)

    # 내부 예: A = [1 1], 해집합 x + y = 3 (숫자는 그림에 쓰지 않음)
    xp = np.array([3.0, 0.0])                 # 특수해 하나
    xs = np.array([1.5, 1.5])                 # A^+ b = 행공간 위의 해

    # 영공간 N(A): x + y = 0 (원점을 지남), 해집합은 이것과 평행
    line(a, 1, 1, 0, mix(TEXT2, 0.6), lw=1.4, ls=(0, (4, 3)), z=2)
    a.text(1.62, -1.5, "$N(A)$", color=TEXT2, fontsize=13, ha="left", va="center")

    # 행공간: x − y = 0 (원점을 지나고 해집합에 수직)
    line(a, 1, -1, 0, CAT[0], lw=2.0, z=3)
    a.text(3.58, 3.5, "행공간", color=CAT[0], fontsize=13, ha="left", va="center")

    # 해집합: x + y = 3
    line(a, 1, 1, 3, CAT[1], lw=2.4, z=3)
    a.text(4.58, -1.5, "해집합 $x_p+N(A)$", color=CAT[1], fontsize=13,
           ha="left", va="center")

    # 원점 중심, 반지름 ‖A^+b‖인 원호 — 해집합에 한 점에서만 닿음
    r = np.hypot(*xs)
    t = np.radians(np.linspace(-15, 105, 120))
    a.plot(r * np.cos(t), r * np.sin(t), color=TEXT2, lw=1.2, ls=(0, (1, 2.5)), zorder=2)

    # 직각 표시 (행공간 ⟂ 해집합)
    s = 0.24
    d1 = np.array([-1, -1]) / np.sqrt(2)
    d2 = np.array([1, -1]) / np.sqrt(2)
    sq = np.array([xs + s * d1, xs + s * (d1 + d2), xs + s * d2])
    a.plot(sq[:, 0], sq[:, 1], color=TEXT2, lw=1.2, zorder=4)

    # 특수해 x_p (회색)와 최소노름 해 A^+b (강조)
    vec(a, xp, TEXT2, "$x_p$", lw=2.0, off=(-4, -6), ha="right", va="top", z=5)
    vec(a, xs, ACCENT, lw=2.8, z=6)
    a.annotate("$A^+b$", xs, xytext=(-12, 0), textcoords="offset points", fontsize=13,
               color=ACCENT_INK, fontweight="bold", ha="right", va="center", zorder=7)

    dot(a, (0, 0), color=TEXT, s=5, z=7)
    save(fig, out("ch10", "f1_min_norm.png"))


if __name__ == "__main__":
    f1_min_norm()
