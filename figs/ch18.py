"""18장 그림. 푸리에 기저(N=64)와 이동평균 필터의 컨볼루션(N=128, 9점) — 원래 fig_part2.py ch18()의 예시 유지.

실행: cd figs && python3 ch18.py
"""
from lafig import *


def _base(fig, W, H):
    """그림 전체를 덮는 인치 좌표 드로잉 축(범례·연산 기호용)."""
    b = fig.add_axes([0, 0, 1, 1])
    b.set_xlim(0, W); b.set_ylim(0, H); b.axis("off")
    return b


def _panel(fig, W, H, x, y, w, h, xlim, ylim):
    a = fig.add_axes([x / W, y / H, w / W, h / H])
    a.set_xlim(*xlim); a.set_ylim(*ylim); a.axis("off")
    return a


def f1_fourier_basis():
    N = 64; n = np.arange(N)
    W, H = 8.0, 4.0
    fig = canvas(W, H)
    base = _base(fig, W, H)
    pw, ph = 3.65, 1.25
    pos = [(0.2, 2.35), (4.15, 2.35), (0.2, 0.65), (4.15, 0.65)]
    for (x0, y0), k in zip(pos, [0, 1, 3, 8]):
        a = _panel(fig, W, H, x0, y0, pw, ph, (0, N - 1), (-1.15, 1.15))
        a.plot([0, N - 1], [0, 0], color=AXIS, lw=0.8, zorder=1)
        a.plot(n, np.sin(2 * np.pi * k * n / N), color=CAT[1], lw=1.6, ls=(0, (4, 2.5)), zorder=2)
        a.plot(n, np.cos(2 * np.pi * k * n / N), color=CAT[0], lw=2.0, zorder=3)
        tag(a, f"$f_{{{k}}}$", y=1.04, fs=13)
    # 범례 — 아래쪽 가운데
    ly = 0.25
    base.plot([1.2, 1.7], [ly, ly], color=CAT[0], lw=2.0)
    label(base, 1.8, ly, "실수부 $\\cos(2\\pi kn/N)$", fs=12, ha="left")
    base.plot([4.3, 4.8], [ly, ly], color=CAT[1], lw=1.6, ls=(0, (4, 2.5)))
    label(base, 4.9, ly, "허수부 $\\sin(2\\pi kn/N)$", fs=12, ha="left")
    save(fig, out("ch18", "f1_fourier_basis.png"))


def f2_convolution():
    """설명용 가상 신호: k=3, k=20 정현파 + 잡음, 9점 이동평균(순환 컨볼루션)."""
    rng = np.random.default_rng(0)
    N = 128; n = np.arange(N)
    x = np.sin(2 * np.pi * 3 * n / N) + .6 * np.sin(2 * np.pi * 20 * n / N) \
        + .4 * rng.normal(size=N)
    h = np.zeros(N); h[:9] = 1 / 9.
    y = np.real(np.fft.ifft(np.fft.fft(x) * np.fft.fft(h)))
    K = N // 2; k = np.arange(K)
    Xs = np.abs(np.fft.fft(x))[:K]
    Hs = np.abs(np.fft.fft(h))[:K]
    Ys = np.abs(np.fft.fft(y))[:K]

    W, H = 8.2, 4.15
    fig = canvas(W, H)
    base = _base(fig, W, H)
    raw = mix(TEXT2, .55)

    # ① 시간 영역
    lo, hi = x.min(), x.max(); pad = 0.08 * (hi - lo)
    a = _panel(fig, W, H, 0.2, 2.25, 7.8, 1.45, (0, N - 1), (lo - pad, hi + pad))
    a.plot([0, N - 1], [0, 0], color=AXIS, lw=0.8, zorder=1)
    a.plot(n, x, color=raw, lw=1.0, zorder=2)
    a.plot(n, y, color=CAT[0], lw=2.2, zorder=3)
    tag(a, "① 시간 영역", y=1.04)
    a.text(0.78, 1.04, "원신호 $x$", transform=a.transAxes, fontsize=12, color=TEXT2,
           ha="right", va="bottom")
    a.text(1.0, 1.04, "평활 $h*x$", transform=a.transAxes, fontsize=12, color=CAT[0],
           fontweight="bold", ha="right", va="bottom")

    # ②–④ 주파수 영역: 입력 × 필터 = 출력
    pw, ph, py = 2.1, 1.4, 0.3
    xs = [0.2, 3.05, 5.9]
    top = Xs.max() * 1.25
    spec = [(Xs, TEXT2, "② 입력 $|\\hat{x}|$", (0, top)),
            (None, CAT[1], "③ 필터 $|\\hat{h}|$", (0, 1.25)),
            (Ys, CAT[0], "④ 출력 $|\\widehat{h*x}|$", (0, top))]
    for x0, (S, c, t, yl) in zip(xs, spec):
        s = _panel(fig, W, H, x0, py, pw, ph, (-1, K), yl)
        s.plot([-1, K], [0, 0], color=AXIS, lw=0.8, zorder=1)
        if S is None:
            s.plot(k, Hs, color=c, lw=2.2, zorder=3)
        else:
            s.vlines(k, 0, S, color=c, lw=1.4, zorder=3)
            s.annotate("$k=3$", (3, S[3]), xytext=(6, 0), textcoords="offset points",
                       fontsize=11, color=TEXT2, ha="left", va="center")
            s.annotate("$k=20$", (20, S[20]), xytext=(0, 4), textcoords="offset points",
                       fontsize=11, color=TEXT2, ha="center", va="bottom")
        tag(s, t, y=1.04)
    cy = py + ph / 2
    label(base, (xs[0] + pw + xs[1]) / 2, cy, "×", fs=20, c=TEXT2)
    label(base, (xs[1] + pw + xs[2]) / 2, cy, "=", fs=20, c=TEXT2)
    save(fig, out("ch18", "f2_convolution.png"))


if __name__ == "__main__":
    f1_fourier_basis()
    f2_convolution()
