"""13장 그림. 실행: cd figs && python3 ch13.py"""
from lafig import *
from matplotlib.ticker import PercentFormatter


def _data():
    """설명용 가상 데이터(원래 스크립트의 시드 7). 중심화 데이터의 공분산 고유분해까지."""
    rng = np.random.default_rng(7)
    X = rng.normal(size=(180, 2)) @ np.array([[1.8, .0], [1.1, .6]])
    Xc = X - X.mean(0)
    C = Xc.T @ Xc / len(Xc)
    w, Q = np.linalg.eigh(C)
    w, Q = w[::-1], Q[:, ::-1].copy()
    if Q[0, 0] < 0:
        Q[:, 0] *= -1
    if Q[1, 1] < 0:
        Q[:, 1] *= -1
    return X, Xc, w, Q


def _lab(ax, text, xy, off, color, ha="left", va="center", fs=13, bold=True, bg=True):
    """라벨(bg=True면 흰 바탕을 깔아 점 위에서도 읽히게)."""
    ax.annotate(text, xy, xytext=off, textcoords="offset points", fontsize=fs, color=color,
                fontweight="bold" if bold else "regular", ha=ha, va=va, zorder=8,
                bbox=dict(fc="white", ec="none", pad=1.0) if bg else None)


def f1_pca_direction():
    X, Xc, w, Q = _data()
    PT = mix(TEXT2, 0.4)
    fig = canvas(8.2, 3.3)
    H, y0 = 2.3, 0.65
    ytag = y0 + 1.05 * H                     # 두 패널 표시의 높이(인치)

    # ① 데이터와 주성분 — 같은 축척(equal), 데이터 범위만큼만
    L = np.abs(Xc[:, 0]).max() + 0.4
    U = 3.5 / (2 * L)
    ya = np.abs(Xc[:, 1]).max() + 0.7
    ha_in = 2 * ya * U
    yb = y0 + (H - ha_in) / 2
    a = plane(fig, 0.15, yb, (-L, L), (-ya, ya), unit=U, grid=False)
    a.plot(Xc[:, 0], Xc[:, 1], "o", color=PT, ms=3.5, mec="none", zorder=2)
    p1 = Q[:, 0] * np.sqrt(w[0]) * 2
    p2 = Q[:, 1] * np.sqrt(w[1]) * 2
    vec(a, p1, CAT[0], lw=2.6)
    vec(a, p2, CAT[1], lw=2.6)
    _lab(a, "PC1", p1, (6, 0), CAT[0], ha="left", va="center")
    _lab(a, "PC2", p2, (0, 5), CAT[1], ha="center", va="bottom")
    tag(a, "① 데이터와 주성분", y=(ytag - yb) / ha_in)

    # ② 방향을 돌려 가며 잰 정사영 분산
    b = fig.add_axes([4.85 / 8.2, y0 / 3.3, 3.2 / 8.2, H / 3.3])
    deg = np.linspace(0, 180, 361)
    var = [np.var(Xc @ np.array([np.cos(t), np.sin(t)])) for t in np.radians(deg)]
    b.plot(deg, var, color=TEXT2, lw=2.2, zorder=3)
    t1 = np.degrees(np.arctan2(Q[1, 0], Q[0, 0])) % 180
    t2 = (t1 + 90) % 180
    b.plot(t1, w[0], "o", color=CAT[0], ms=9, mec="white", mew=1.2, zorder=5, clip_on=False)
    b.plot(t2, w[1], "o", color=CAT[1], ms=9, mec="white", mew=1.2, zorder=5, clip_on=False)
    b.annotate("$\\lambda_1$ (PC1)", (t1, w[0]), xytext=(8, 4), textcoords="offset points",
               fontsize=13, color=CAT[0], fontweight="bold", ha="left", va="bottom")
    b.annotate("$\\lambda_2$ (PC2)", (t2, w[1]), xytext=(0, 30), textcoords="offset points",
               fontsize=13, color=CAT[1], fontweight="bold", ha="center", va="bottom")
    b.set_xlim(0, 180); b.set_ylim(0, w[0] * 1.3)
    b.set_xticks([0, 45, 90, 135, 180])
    b.set_xticklabels([f"{v}°" for v in (0, 45, 90, 135, 180)])
    b.set_xlabel("정사영 방향 θ", fontsize=12)
    b.set_ylabel("정사영 분산", fontsize=12)
    b.tick_params(labelsize=11)
    tag(b, "② 방향별 정사영 분산", x=-0.02, y=1.05)
    save(fig, out("ch13", "f1_pca_direction.png"))


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


def f3_centering():
    X, Xc, w, Q = _data()
    PT = mix(TEXT2, 0.4)
    Xr = X + np.array([6., 4.])                     # 중심화하지 않은 데이터
    Cr = Xr.T @ Xr / len(Xr)                         # 2차 적률
    wr, Qr = np.linalg.eigh(Cr)
    r1 = Qr[:, -1].copy()
    if r1[0] < 0:
        r1 *= -1
    m = Xr.mean(0)
    s0, s1 = m - 5.5 * Q[:, 0], m + 5.5 * Q[:, 0]   # 구조 방향(중심화 PC1)을 평균에 놓은 선분
    yt = Xr[Xr[:, 0] > s1[0] - 3.5, 1].max() + 0.2  # "구조 방향" 라벨: 점들 위쪽

    # 축척 공통: 두 패널 폭의 합 7.0인치
    L1 = np.abs(Xc[:, 0]).max() + 0.5
    y1 = (Xc[:, 1].min() - 1.9, Xc[:, 1].max() + 0.6)
    x2 = (min(-1.0, Xr[:, 0].min()) - 0.6, Xr[:, 0].max() + 0.6)
    y2 = (-1.2, max(Xr[:, 1].max() + 0.8, yt + 0.8))
    U = 7.0 / (2 * L1 + (x2[1] - x2[0]))
    h1 = (y1[1] - y1[0]) * U
    h2 = (y2[1] - y2[0]) * U
    gap, yb = 0.6, 0.3
    fig = canvas(8.2, h2 + 1.0)

    # ① 중심화한 데이터 (윗변을 ②와 맞춤)
    a = plane(fig, 0.15, yb + h2 - h1, (-L1, L1), y1, unit=U, grid=False)
    a.plot(Xc[:, 0], Xc[:, 1], "o", color=PT, ms=3.5, mec="none", zorder=2)
    pc = Q[:, 0] * 5
    vec(a, pc, CAT[0], lw=2.6)
    _lab(a, "PC1", pc, (6, 0), CAT[0], ha="left", va="center")
    dot(a, (0, 0), color=TEXT, s=8)
    a.annotate("원점 = 평균", (0, 0), xytext=(0, y1[0] + 0.25), textcoords="data",
               fontsize=12, color=TEXT, ha="center", va="bottom", zorder=8,
               bbox=dict(fc="white", ec="none", pad=1.0),
               arrowprops=dict(arrowstyle="-", color=TEXT2, lw=1.0, shrinkA=0, shrinkB=5))
    tag(a, "① 중심화한 데이터", y=1.04)

    # ② 중심화하지 않은 데이터
    b = plane(fig, 0.15 + 2 * L1 * U + gap, yb, x2, y2, unit=U, grid=False)
    b.plot(Xr[:, 0], Xr[:, 1], "o", color=PT, ms=3.5, mec="none", zorder=2)
    b.plot([s0[0], s1[0]], [s0[1], s1[1]], color=TEXT2, lw=1.6, ls=(0, (4, 3)), zorder=3)
    b.text(s1[0], yt, "구조 방향", fontsize=12, fontweight="bold", color=TEXT2,
           ha="right", va="bottom", zorder=8)
    pc = r1 * 5
    vec(b, pc, CAT[0], lw=2.6)
    _lab(b, "PC1", pc / 2, (6, -6), CAT[0], ha="left", va="top")
    dot(b, (0, 0), color=TEXT, s=8)
    _lab(b, "원점", (0, 0), (-6, -6), TEXT, ha="right", va="top", fs=12, bold=False)
    dot(b, m, color=TEXT, s=8)
    _lab(b, "평균", m, (6, -6), TEXT, ha="left", va="top", fs=12, bold=False)
    tag(b, "② 중심화하지 않은 데이터", y=1.04)
    save(fig, out("ch13", "f3_centering.png"))


if __name__ == "__main__":
    f1_pca_direction()
    f2_scree()
    f3_centering()
