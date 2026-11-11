"""15장 그림 — SVD: 단위원 → 타원, 저랭크 근사.

실행: cd figs && python3 ch15.py
"""
from lafig import *
from matplotlib.colors import LinearSegmentedColormap


def _overlay(fig):
    """그림 전체를 덮는 인치 좌표 축(화살표·라벨용)."""
    W, H = fig.get_size_inches()
    ov = fig.add_axes([0, 0, 1, 1])
    ov.set_xlim(0, W); ov.set_ylim(0, H); ov.axis("off")
    return ov


def _right_angle(ax, e1, e2, s):
    """원점에서 e1, e2 사이의 직각 표시."""
    e1, e2 = np.asarray(e1), np.asarray(e2)
    pts = np.array([s * e1, s * (e1 + e2), s * e2])
    ax.plot(pts[:, 0], pts[:, 1], color=TEXT2, lw=1.1, zorder=3)


def f1_circle_to_ellipse():
    A = np.array([[2., 1.], [.6, 1.8]])
    _, d, Vt = np.linalg.svd(A)
    V = Vt.T.copy()
    if V[0, 0] < 0:
        V[:, 0] *= -1                      # v1은 오른쪽 위를 향하게
    if V[1, 1] < 0:
        V[:, 1] *= -1                      # v2는 위를 향하게
    SU = A @ V                             # 열 = σ_i u_i
    Uu = SU / d                            # 열 = u_i
    t = np.linspace(0, 2 * np.pi, 300)
    circ = np.vstack([np.cos(t), np.sin(t)])
    E = A @ circ

    U = 0.75
    fig = canvas(7.3, 3.9)

    # ① 입력 — 단위원과 직교하는 v1, v2
    a = plane(fig, 0.2, 0.75, (-1.5, 1.5), (-1.5, 1.5), unit=U)
    a.fill(circ[0], circ[1], color=FAINT, lw=0, zorder=0.5)
    a.plot(circ[0], circ[1], color=TEXT2, lw=1.4, zorder=2)
    _right_angle(a, V[:, 0], V[:, 1], 0.16)
    vec(a, V[:, 0], CAT[0], "$v_1$", off=(6, 4), ha="left", va="bottom")
    vec(a, V[:, 1], CAT[1], "$v_2$", off=(-6, 4), ha="right", va="bottom")
    tag(a, "① 입력 — 단위원", y=1.33)

    # ② 출력 — 타원, 축이 σ_i u_i
    b = plane(fig, 3.1, 0.15, (-2.6, 2.6), (-2.3, 2.3), unit=U)
    b.fill(E[0], E[1], color=FAINT, lw=0, zorder=0.5)
    b.plot(E[0], E[1], color=TEXT2, lw=1.4, zorder=2)
    _right_angle(b, Uu[:, 0], Uu[:, 1], 0.22)
    vec(b, SU[:, 0], CAT[0], "$\\sigma_1u_1$", off=(6, 4), ha="left", va="bottom")
    vec(b, SU[:, 1], CAT[1], "$\\sigma_2u_2$", off=(-6, 4), ha="right", va="bottom")
    tag(b, "② 출력 — $Av_i=\\sigma_i u_i$", y=1.04)

    # 두 패널 사이: 변환 A
    ov = _overlay(fig)
    arrow(ov, 2.55, 2.25, 3.0, 2.25, color=TEXT2)
    label(ov, 2.775, 2.45, "$A$", fs=14, c=TEXT)
    save(fig, out("ch15", "f1_circle_to_ellipse.png"))


def f2_lowrank():
    """설명용 가상 이미지 140×140."""
    rng = np.random.default_rng(11)
    N = 140
    yy, xx = np.mgrid[0:N, 0:N]
    field = rng.normal(size=(N, N))
    for _ in range(22):                      # 반복 평활 → 매끄럽지만 랭크가 높은 장
        field = (field + np.roll(field, 1, 0) + np.roll(field, -1, 0)
                 + np.roll(field, 1, 1) + np.roll(field, -1, 1)) / 5
    field /= field.std()
    img = (0.45 * field
           + 1.2 * np.sin(xx / 13.) * np.cos(yy / 20.)
           + 1.7 * ((np.abs(xx - 42) < 18) & (np.abs(yy - 98) < 18))
           + 1.7 * (((xx - 98)**2 + (yy - 42)**2) < 24**2)
           + 1.2 * (np.abs(xx - yy) < 5))

    U, d, Vt = np.linalg.svd(img)
    tot = np.sqrt((d**2).sum())
    lo, hi = img.min(), img.max()
    cmap = LinearSegmentedColormap.from_list("ink", [TEXT, "white"])

    W, H = 6.9, 5.45
    S, gap = 2.0, 0.35
    fig = canvas(W, H)
    ov = _overlay(fig)
    top, bot = 3.3, 0.6
    xs_top = [0.1, 0.1 + S + gap, 0.1 + 2 * (S + gap)]
    x0_bot = 0.1 + (3 * S + 2 * gap - (2 * S + gap)) / 2
    xs_bot = [x0_bot, x0_bot + S + gap]
    cells = [(1, xs_top[0], top), (5, xs_top[1], top), (20, xs_top[2], top),
             (60, xs_bot[0], bot), (len(d), xs_bot[1], bot)]

    for k, x, y in cells:
        ax = fig.add_axes([x / W, y / H, S / W, S / H])
        Ak = U[:, :k] @ np.diag(d[:k]) @ Vt[:k]
        ax.imshow(Ak, cmap=cmap, vmin=lo, vmax=hi)
        ax.axis("off")
        cx = x + S / 2
        if k == len(d):
            label(ov, cx, y - 0.12, "원본", fs=13, w="bold", va="top")
            label(ov, cx, y - 0.40, f"rank {np.linalg.matrix_rank(img)}",
                  fs=11, c=TEXT2, va="top")
        else:
            err = np.sqrt((d[k:]**2).sum()) / tot
            store = k * (2 * N + 1) / N**2
            label(ov, cx, y - 0.12, f"$k={k}$", fs=13, va="top")
            label(ov, cx, y - 0.40, f"오차 {err:.1%} · 저장 {store:.0%}",
                  fs=11, c=TEXT2, va="top")
    save(fig, out("ch15", "f2_lowrank.png"))


if __name__ == "__main__":
    f1_circle_to_ellipse()
    f2_lowrank()
