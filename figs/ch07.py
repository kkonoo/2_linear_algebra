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


def f2_elimination_geometry():
    # 첨가행렬 [A | b]에서 직접 소거
    A0 = np.array([[2., 1.], [1., -1.]]); b0 = np.array([5., 1.])
    A1, b1 = A0.copy(), b0.copy()                     # 가우스: R2 ← R2 − (1/2)R1
    m = A1[1, 0] / A1[0, 0]
    A1[1] -= m * A1[0]; b1[1] -= m * b1[0]
    A2, b2 = A1.copy(), b1.copy()                     # 조던: 피벗을 1로, 피벗 위를 0으로
    for i in range(2):
        p = A2[i, i]; A2[i] /= p; b2[i] /= p
    s = A2[0, 1]; A2[0] -= s * A2[1]; b2[0] -= s * b2[1]
    assert np.allclose(A1, [[2, 1], [0, -1.5]]) and np.allclose(b1, [5, -1.5])
    assert np.allclose(A2, np.eye(2)) and np.allclose(b2, [2, 1])
    sol = np.linalg.solve(A0, b0)
    assert np.allclose(sol, [2, 1])

    systems = [
        (A0, b0, "① 원래 방정식",
         [("$2x+y=5$", (2.98, -1.35), "right", "center"),
          ("$x-y=1$", (3.55, 3.45), "right", "top")]),
        (A1, b1, "② 가우스 소거 → REF",
         [("$2x+y=5$", (2.98, -1.35), "right", "center"),
          ("$-\\frac{3}{2}y=-\\frac{3}{2}$", (3.55, 1.12), "right", "bottom")]),
        (A2, b2, "③ 가우스-조던 → RREF",
         [("$x=2$", (2.1, 3.45), "left", "top"),
          ("$y=1$", (3.55, 1.12), "right", "bottom")]),
    ]
    U = 0.58
    xl, yl = (-0.6, 3.6), (-1.6, 3.6)
    pw = (xl[1] - xl[0]) * U
    fig = canvas(8.4, 3.7)
    for k, (A, rhs, name, labels) in enumerate(systems):
        ax = plane(fig, 0.15 + k * (pw + 0.4), 0.25, xl, yl, unit=U)
        for i, c in enumerate((CAT[0], CAT[1])):
            line(ax, A[i, 0], A[i, 1], rhs[i], c)
            n = A[i] / np.linalg.norm(A[i]) * 1.5      # 법선벡터 방향(길이는 맞춤)
            vec(ax, n, c, lw=1.6, ls=(0, (3, 2)), z=4)
            t, (x, y), ha, va = labels[i]
            ax.text(x, y, t, color=c, fontsize=13, ha=ha, va=va)
        ax.plot(*sol, "o", ms=10, mfc="white", mec=TEXT, mew=2.2, zorder=6)
        ax.annotate("$(2,\\,1)$", sol, xytext=(-16, 6), textcoords="offset points",
                    fontsize=12, color=TEXT, ha="right", va="bottom")
        tag(ax, name, y=1.04)
    save(fig, out("ch07", "f2_elimination_geometry.png"))


if __name__ == "__main__":
    f1_row_column_picture()
    f2_elimination_geometry()
