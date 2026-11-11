"""4장 그림. 네 기본 부분공간(§3)과 부분공간 판정(§1-2).

실행: cd figs && python3 ch04.py
"""
from lafig import *


def f1_four_subspaces():
    fig, ax = new(8.2, 3.8)
    live = mix(CAT[0], 0.28)        # 행공간·열공간 — 살아남아 옮겨가는 쪽
    dead = mix(CAT[1], 0.25)        # 영공간·좌영공간
    W, H = 2.7, 1.25
    xl, xr = 0.2, 5.3
    yt, yb = 1.95, 0.3

    def cell(x, y, fc, name, sub):
        box(ax, x, y, W, H, fc=fc, ec="none", r=0.1)
        label(ax, x + W / 2, y + H * 0.63, name, fs=13, w="bold", c=on(fc))
        label(ax, x + W / 2, y + H * 0.3, sub, fs=11, c=TEXT2)

    label(ax, xl + W / 2, 3.5, "정의역  $\\mathbb{R}^n$", fs=13, w="bold")
    label(ax, xr + W / 2, 3.5, "공역  $\\mathbb{R}^m$", fs=13, w="bold")
    cell(xl, yt, live, "행공간  $C(A^{\\mathsf{T}})$", "차원 $r$")
    cell(xl, yb, dead, "영공간  $N(A)$", "차원 $n-r$")
    cell(xr, yt, live, "열공간  $C(A)$", "차원 $r$ · 치역")
    cell(xr, yb, dead, "좌영공간  $N(A^{\\mathsf{T}})$", "차원 $m-r$ · 도달 불가")

    # 직교 표시 (상자 사이 틈)
    gy = (yb + H + yt) / 2
    label(ax, xl + W / 2, gy, "$\\perp$", fs=16, c=TEXT2)
    label(ax, xr + W / 2, gy, "$\\perp$", fs=16, c=TEXT2)

    # 행공간 → 열공간 (일대일 대응)
    ym = yt + H / 2
    arrow(ax, xl + W + 0.05, ym, xr - 0.05, ym, color=CAT[0], lw=2.2, ms=14)
    label(ax, (xl + W + xr) / 2, ym + 0.13, "$A$ · 일대일 대응", fs=12, c=CAT[0], va="bottom")

    # 영공간 → 0 (공역의 원점: 열공간과 좌영공간 사이, 공역 안쪽)
    zx, zy = xr + 0.35, gy
    ax.plot(zx, zy, "o", color=TEXT, ms=7, mec="white", mew=1.2, zorder=6)
    label(ax, zx + 0.11, zy, "$0$", fs=13, ha="left")
    x0, y0 = xl + W + 0.05, yb + H * 0.64
    arrow(ax, x0, y0, zx - 0.09, zy, color=TEXT2, lw=1.6)
    label(ax, 4.15, 1.0, "$Ax = 0$", fs=12, c=TEXT2)
    save(fig, out("ch04", "f1_four_subspaces.png"))


def f2_subspace_or_not():
    U = 0.5
    fig = canvas(7.0, 3.6)
    lim = (-3, 3)

    a = plane(fig, 0.1, 0.1, lim, lim, unit=U)
    line(a, 0.6, -1, 0, CAT[0])                 # y = 0.6x
    dot(a, (0, 0), color=TEXT, s=8)
    a.annotate("원점 ∈ 직선", (0, 0), xytext=(8, -6), textcoords="offset points",
               fontsize=12, color=TEXT, ha="left", va="top")
    tag(a, "① 부분공간이다", y=1.03)

    b = plane(fig, 3.7, 0.1, lim, lim, unit=U)
    line(b, 0.6, -1, -1.2, TEXT2)               # y = 0.6x + 1.2
    dot(b, (0, 0), color=ACCENT, s=10)
    b.annotate("원점 ∉ 직선", (0, 0), xytext=(8, -6), textcoords="offset points",
               fontsize=12, color=ACCENT_INK, fontweight="bold", ha="left", va="top")
    tag(b, "② 부분공간이 아니다", y=1.03)
    save(fig, out("ch04", "f2_subspace_or_not.png"))


if __name__ == "__main__":
    f1_four_subspaces()
    f2_subspace_or_not()
