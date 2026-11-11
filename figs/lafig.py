"""선형대수 그림용 보조 도구 — 공용 스타일(medfig) 위에 좌표평면 그리기를 더한다.

각 장 스크립트는 `from lafig import *`로 시작하고 `save(fig, out("ch07", "f1_….png"))`로 저장한다.
좌표평면은 plane()으로 만든다. 단위 길이를 인치로 정하므로 여러 패널의 축척이 같아진다.
"""
import math
import os
from medfig import *            # noqa: F401,F403  (색 상수, new, save, box, arrow, label …)
import matplotlib.patches as mp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AXIS = "#B4BAC3"                # 좌표축
GRID = LINE                     # 격자
plt.rcParams["mathtext.fontset"] = "dejavusans"


def out(ch, name):
    """images/<ch>/<name> 경로."""
    return os.path.join(ROOT, "images", ch, name)


def canvas(w, h):
    """w × h 인치 빈 그림. 패널은 plane()이나 fig.add_axes로 올린다."""
    return plt.figure(figsize=(w, h))


def plane(fig, x, y, xlim, ylim, unit=0.6, grid=True, axes=True):
    """그림의 (x, y) 인치 위치를 왼쪽 아래로 하는 좌표평면. 1 = unit 인치."""
    W, H = fig.get_size_inches()
    w = (xlim[1] - xlim[0]) * unit
    h = (ylim[1] - ylim[0]) * unit
    ax = fig.add_axes([x / W, y / H, w / W, h / H])
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")
    if grid:
        for g in range(math.ceil(xlim[0]), math.floor(xlim[1]) + 1):
            ax.plot([g, g], ylim, color=GRID, lw=0.6, zorder=0)
        for g in range(math.ceil(ylim[0]), math.floor(ylim[1]) + 1):
            ax.plot(xlim, [g, g], color=GRID, lw=0.6, zorder=0)
    if axes:
        ax.plot(xlim, [0, 0], color=AXIS, lw=1.0, zorder=1)
        ax.plot([0, 0], ylim, color=AXIS, lw=1.0, zorder=1)
    return ax


def vec(ax, v, color=None, label=None, start=(0, 0), lw=2.4, ls="-", off=(6, 4),
        fs=13, ha="left", va="bottom", z=4):
    """start에서 시작하는 벡터 v. label은 끝점에서 off(포인트)만큼 떨어진 곳에."""
    color = color or PRIMARY
    x0, y0 = start
    x1, y1 = x0 + v[0], y0 + v[1]
    ax.add_patch(mp.FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=15,
                                    color=color, lw=lw, ls=ls, zorder=z, shrinkA=0, shrinkB=0))
    if label:
        ax.annotate(label, (x1, y1), xytext=off, textcoords="offset points", fontsize=fs,
                    color=color, ha=ha, va=va, zorder=z + 1)


def line(ax, a, b, c, color=None, lw=2.4, ls="-", z=3):
    """직선 a·x + b·y = c를 좌표평면 안쪽만 그린다(밖으로 나간 부분이 여백을 만들지 않게)."""
    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    if abs(b) < 1e-12:
        xs, ys = [c / a, c / a], [y0, y1]
    else:
        lo, hi = x0, x1
        if abs(a) > 1e-12:
            xa, xb = (c - b * y0) / a, (c - b * y1) / a
            lo, hi = max(x0, min(xa, xb)), min(x1, max(xa, xb))
        xs = [lo, hi]
        ys = [(c - a * lo) / b, (c - a * hi) / b]
    ax.plot(xs, ys, color=color or PRIMARY, lw=lw, ls=ls, zorder=z, solid_capstyle="butt")


def dot(ax, p, color=None, s=7, z=6, ec="white"):
    """점 하나."""
    ax.plot(*p, "o", color=color or PRIMARY, ms=s, mec=ec, mew=1.2, zorder=z)


def tag(ax, text, x=0.0, y=1.0, fs=12):
    """패널 표시(예: ① 행 그림). 축 좌표 기준 왼쪽 위."""
    ax.text(x, y, text, transform=ax.transAxes, fontsize=fs, fontweight="bold", color=TEXT,
            ha="left", va="bottom")
