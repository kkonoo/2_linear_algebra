<<<<<<< HEAD
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
=======
"""강의 그림 공통 스타일.

모든 그림 스크립트는 `from style import *` 로 시작하고 OUT 아래에 저장합니다.
한글 폰트는 실행 환경(Windows / macOS / Linux)에 따라 자동으로 고릅니다.
"""
import os
import glob
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np

# ── 팔레트 ────────────────────────────────────────────────────────────
TEAL = "#5F9EA0"; PURPLE = "#9B8EC4"; OLIVE = "#B5AE8A"; NAVY = "#2E4057"
RED = "#C1544B"; GREY = "#B8B8B8"; LGREY = "#E8E8E8"; ORANGE = "#E08A3C"
BLUE = "#4A77A8"
# 사이트 CSS의 제목 색과 맞춘 보조색
PLUM = "#5B4D80"


# ── 한글 폰트 ─────────────────────────────────────────────────────────
def _korean_font():
    """설치된 한글 폰트 이름을 반환. 없으면 None."""
    for name in ("Pretendard", "Malgun Gothic", "AppleGothic",
                 "NanumGothic", "Noto Sans CJK KR", "Noto Sans KR"):
        try:
            if fm.findfont(fm.FontProperties(family=name),
                           fallback_to_default=False):
                return name
        except Exception:
            pass
    # 리눅스: 파일 경로로 직접 등록 (Noto CJK 는 KR/JP 가 한 파일에 들어 있음)
    for pat in ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                "/usr/share/fonts/**/NanumGothic*.ttf",
                "/usr/share/fonts/**/NotoSansCJK*.ttc"):
        for path in glob.glob(pat, recursive=True):
            try:
                fm.fontManager.addfont(path)
                return fm.FontProperties(fname=path).get_name()
            except Exception:
                continue
    return None


KO = _korean_font()

plt.rcParams.update({
    "font.family": KO if KO else "DejaVu Sans",
    "font.size": 11,
    "axes.unicode_minus": False,        # 한글 폰트에서 마이너스 깨짐 방지
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#4A4A4A", "axes.labelcolor": "#2A2A2A",
    "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlepad": 12,
    "xtick.color": "#4A4A4A", "ytick.color": "#4A4A4A",
    "figure.facecolor": "white", "savefig.facecolor": "white",
    "savefig.dpi": 160, "savefig.bbox": "tight",
})

# 각 스크립트에서 chapter 폴더를 붙여 씁니다.
IMG_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")


def outdir(chapter):
    """images/<chapter>/ 를 만들고 경로를 돌려줍니다."""
    d = os.path.join(IMG_ROOT, chapter)
    os.makedirs(d, exist_ok=True)
    return d
>>>>>>> 98a8ebed3aa40d1a9ee95bedd78d6c5386c1cee4
