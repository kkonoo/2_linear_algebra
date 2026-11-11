"""7장 그림. 예제 연립방정식은 2x + y = 5, x − y = 1 (해 (2, 1)) — 본문 6절의 2x+y=5에 맞춤.

실행: cd figs && python3 ch07.py
"""
from lafig import *


def f1_row_column_picture():
    U = 0.62
    fig = canvas(8.4, 3.6)
    # ① 행 그림 — 두 직선의 교점
    a = plane(fig, 0.2, 0.25, (-0.6, 3.6), (-1.6, 3.6), unit=U)
    line(a, 2, 1, 5, CAT[0])
    line(a, 1, -1, 1, CAT[1])
    a.text(2.85, -1.05, "$2x+y=5$", color=CAT[0], fontsize=13, ha="right", va="center")
    a.text(3.55, 3.45, "$x-y=1$", color=CAT[1], fontsize=13, ha="right", va="top")
    dot(a, (2, 1), color=ACCENT, s=11)
    a.annotate("교점 $(2,\\,1)$", (2, 1), xytext=(10, -4), textcoords="offset points",
               fontsize=12, color=ACCENT_INK, fontweight="bold", ha="left", va="top")
    tag(a, "① 행 그림 — 직선의 교차", y=1.04)

    # ② 열 그림 — 열벡터의 조합
    b = plane(fig, 3.55, 0.25, (-0.6, 6.4), (-1.6, 3.6), unit=U)
    a1, a2 = np.array([2, 1]), np.array([1, -1])
    vec(b, 2 * a1, CAT[0], lw=1.4, ls=(0, (3, 2)), z=2)
    vec(b, a2, CAT[1], start=2 * a1, lw=1.4, ls=(0, (3, 2)), z=2)
    vec(b, a1, CAT[0], "$a_1$", off=(-4, 6), ha="right")
    vec(b, a2, CAT[1], "$a_2$", off=(4, -6), va="top")
    vec(b, (5, 1), TEXT, "$b$", lw=2.6, off=(6, 0), va="center")
    b.text(2.2, 1.95, "$2a_1$", color=CAT[0], fontsize=12, ha="center")
    b.text(4.85, 1.75, "$+\\,1a_2$", color=CAT[1], fontsize=12, ha="left")
    tag(b, "② 열 그림 — 열벡터의 조합", y=1.04)
    save(fig, out("ch07", "f1_row_column_picture.png"))


if __name__ == "__main__":
    f1_row_column_picture()
