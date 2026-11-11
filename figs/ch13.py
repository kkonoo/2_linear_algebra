"""13장 그림. 실행: cd figs && python3 ch13.py"""
from lafig import *
from matplotlib.ticker import PercentFormatter


def f2_scree():
    """설명용 가상 고유값 10개."""
    ev = np.array([9.1, 3.4, 1.6, .9, .55, .35, .25, .18, .12, .08]); ev = ev / ev.sum()
    k = np.arange(1, 11)
    fig = canvas(8.0, 3.0)
    a = fig.add_axes([0.08, 0.2, 0.38, 0.68]); b = fig.add_axes([0.59, 0.2, 0.38, 0.68])
    a.plot(k, ev, "-o", color=PRIMARY, lw=2, ms=6, mec="white", mew=1)
    a.annotate("elbow", (3, ev[2]), xytext=(4.6, 0.3), fontsize=12, color=TEXT2,
               arrowprops=dict(arrowstyle="-|>", color=TEXT2, lw=1.2, shrinkA=2, shrinkB=6))
    a.set_ylabel("설명 분산 비율", fontsize=12)
    b.plot(k, np.cumsum(ev), "-o", color=PRIMARY, lw=2, ms=6, mec="white", mew=1)
    b.axhline(0.9, color=ACCENT_INK, lw=1.4, ls=(0, (4, 3)))
    b.text(10.3, 0.875, "90% 기준", color=ACCENT_INK, fontsize=12, fontweight="bold", ha="right", va="top")
    b.set_ylabel("누적 비율", fontsize=12); b.set_ylim(0.5, 1.03)
    for x, t in ((a, "① 성분별"), (b, "② 누적")):
        x.set_xticks(k); x.set_xlabel("성분 번호", fontsize=12)
        x.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
        x.tick_params(labelsize=11)
        tag(x, t, x=-0.02, y=1.05)
    save(fig, out("ch13", "f2_scree.png"))


if __name__ == "__main__":
    f2_scree()
