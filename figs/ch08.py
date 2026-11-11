"""8장 그림 (새로 그림). LU 분해는 한 번, 대입은 b마다 — 본문 §3-1.

실행: cd figs && python3 ch08.py
"""
from lafig import *


def f1_lu_reuse():
    fig, ax = new(8.4, 3.0)
    c0, c1, c2 = ramp(3)            # 순서 있는 단계: 분해 → forward → back
    box(ax, 0.1, 0.45, 1.85, 2.1, fc=c0, ec="none", r=0.12)
    label(ax, 1.025, 2.12, "분해", fs=13, w="bold", c="white")
    label(ax, 1.025, 1.55, "$PA = LU$", fs=15, c="white")
    label(ax, 1.025, 0.95, "$O(n^3)$", fs=12, c="white")
    pill(ax, 1.025, 2.55, "한 번", fc=ACCENT, tc=ON_ACCENT, fs=12)
    arrow(ax, 2.0, 1.5, 2.7, 1.5, color=TEXT2)
    label(ax, 2.35, 1.72, "$L,\\,U$ 저장", fs=11, c=TEXT2)
    rows = [(2.25, "1"), (1.4, "2"), (0.35, "k")]
    ax.plot([2.78, 2.78], [rows[-1][0], rows[0][0]], color=TEXT2, lw=1.6, solid_capstyle="round")
    for y, k in rows:
        ax.plot([2.78, 2.9], [y, y], color=TEXT2, lw=1.6)
        label(ax, 3.12, y, f"$b_{k}$", fs=14)
        arrow(ax, 3.32, y, 3.55, y)
        box(ax, 3.58, y - 0.32, 1.95, 0.64, fc=c1, ec="none")
        label(ax, 4.555, y + 0.1, f"$Lc = Pb_{k}$", fs=13, c=on(c1))
        label(ax, 4.555, y - 0.17, "forward substitution", fs=11, c=on(c1))
        arrow(ax, 5.56, y, 5.78, y)
        box(ax, 5.81, y - 0.32, 1.95, 0.64, fc=c2, ec="none")
        label(ax, 6.785, y + 0.1, "$Ux = c$", fs=13, c=on(c2))
        label(ax, 6.785, y - 0.17, "back substitution", fs=11, c=on(c2))
        arrow(ax, 7.79, y, 8.0, y)
        label(ax, 8.2, y, f"$x_{k}$", fs=14)
    label(ax, 5.67, 0.9, "⋮", fs=14, c=TEXT2)
    label(ax, 5.67, -0.15, "$b$마다 $O(n^2)$", fs=12, c=TEXT2)
    save(fig, out("ch08", "f1_lu_reuse.png"))


if __name__ == "__main__":
    f1_lu_reuse()
