"""공통 스타일 — 사이트 테마(cosmo + assets/html.css)에 맞춘 색과 크기."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT  = ROOT / "images"

PURPLE = "#5B4D80"   # h2 색
LILAC  = "#9A8DB5"
TEAL   = "#3FA3A0"
CORAL  = "#C46A5A"
GREY   = "#9AA0A6"
FAINT  = "#DCD7E8"

# 한글 폰트 (없으면 기본값 — 그림 안 라벨은 대부분 수식/영문)
for cand in ("Pretendard", "Malgun Gothic", "NanumGothic", "Noto Sans CJK KR", "Noto Sans CJK JP"):
    if any(f.name == cand for f in fm.fontManager.ttflist):
        plt.rcParams["font.family"] = cand
        break
plt.rcParams.update({
    "axes.unicode_minus": False,
    "figure.dpi": 160,
    "savefig.dpi": 160,
    "savefig.bbox": "tight",
    "savefig.facecolor": "white",
    "axes.edgecolor": "#CCCCCC",
    "axes.labelcolor": "#444444",
    "xtick.color": "#666666",
    "ytick.color": "#666666",
    "font.size": 8,
})


def save(fig, chapter, name):
    d = OUT / chapter
    d.mkdir(parents=True, exist_ok=True)
    p = d / name
    fig.savefig(p)
    plt.close(fig)
    print("  ", p.relative_to(ROOT))


def plane(ax, lim=3, grid=True, ticks=False):
    """원점을 지나는 축이 있는 깨끗한 평면."""
    ax.set_aspect("equal")
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.axhline(0, color="#BBBBBB", lw=0.8, zorder=0)
    ax.axvline(0, color="#BBBBBB", lw=0.8, zorder=0)
    if grid:
        ax.grid(True, color=FAINT, lw=0.5, zorder=0)
    for s in ax.spines.values():
        s.set_visible(False)
    if not ticks:
        ax.set_xticks([]); ax.set_yticks([])


def arrow(ax, v, color=PURPLE, label=None, start=(0, 0), lw=2.0, ls="-", alpha=1.0, dx=0.12):
    ax.annotate("", xy=(start[0] + v[0], start[1] + v[1]), xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                linestyle=ls, alpha=alpha, shrinkA=0, shrinkB=0))
    if label:
        ax.text(start[0] + v[0] + dx, start[1] + v[1] + dx, label,
                color=color, fontsize=9, ha="left", va="bottom")


SQUARE = np.array([[0, 1, 1, 0, 0],
                   [0, 0, 1, 1, 0]], float)
