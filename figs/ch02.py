"""2장 그림. 예시 행렬 A = [[2,1],[0,3]] (본문 §2-2), 변환 갤러리(§5), 회전 R(90°)·x축 사영 P (§3-2).

실행: cd figs && python3 ch02.py
"""
from lafig import *

SQ = np.array([[0, 1, 1, 0], [0, 0, 1, 1.]])          # 단위정사각형 꼭짓점
GREY_FC = mix(TEXT2, 0.18)                             # 변환 전 도형(중립)
AFTER_FC, AFTER_EC = mix(PRIMARY, 0.15), mix(PRIMARY, 0.6)
DASH = (0, (3, 2))


def poly(ax, pts, fc="none", ec=TEXT2, lw=1.2, ls="-", z=0.5):
    """꼭짓점 2×k 배열로 닫힌 다각형(단색)."""
    ax.add_patch(mp.Polygon(np.asarray(pts).T, closed=True, fc=fc, ec=ec, lw=lw, ls=ls,
                            zorder=z, joinstyle="round"))


def overlay(fig):
    """그림 전체를 덮는 인치 좌표 축(패널 사이 화살표용)."""
    W, H = fig.get_size_inches()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    return ax


def f1_columns():
    U = 0.7
    A = np.array([[2., 1.], [0., 3.]])
    fig = canvas(6.3, 3.6)
    # ① 변환 전 — 단위정사각형과 표준기저
    a = plane(fig, 0.3, 0.3, (-0.6, 1.9), (-0.6, 3.6), unit=U)
    poly(a, SQ, fc=GREY_FC, ec=TEXT2, lw=1.0)
    vec(a, (1, 0), CAT[0], "$e_1$", off=(0, -6), ha="center", va="top")
    vec(a, (0, 1), CAT[1], "$e_2$", off=(-6, 0), ha="right", va="center")
    dot(a, (1, 1), TEXT)
    a.annotate("$(1,1)$", (1, 1), xytext=(5, 3), textcoords="offset points",
               fontsize=12, color=TEXT, ha="left", va="bottom")
    tag(a, "① 변환 전", y=1.04)

    # ② 변환 후 — 열이 곧 행선지
    b = plane(fig, 3.0, 0.3, (-0.6, 3.6), (-0.6, 3.6), unit=U)
    poly(b, A @ SQ, fc=AFTER_FC, ec=AFTER_EC, lw=1.2)
    vec(b, A[:, 0], CAT[0], "$Ae_1=(2,0)$", off=(0, -6), ha="center", va="top")
    vec(b, A[:, 1], CAT[1], "$Ae_2=(1,3)$", off=(-9, 0), ha="right", va="center")
    dot(b, (3, 3), TEXT)
    b.annotate("$(3,3)$", (3, 3), xytext=(4, 2), textcoords="offset points",
               fontsize=12, color=TEXT, ha="left", va="bottom")
    tag(b, "② 변환 후", y=1.04)

    o = overlay(fig)
    y = 0.3 + (0.5 + 0.6) * U
    arrow(o, 2.2, y, 2.85, y, color=TEXT2, lw=1.8)
    label(o, 2.525, y + 0.22, "$A$", fs=15)
    save(fig, out("ch02", "f1_columns.png"))


def f2_gallery():
    U = 0.75
    th = np.pi / 6
    mats = [("① 항등", np.eye(2)),
            ("② 확대 1.5배", 1.5 * np.eye(2)),
            ("③ 전단", np.array([[1, 1], [0, 1.]])),
            ("④ 회전 30°", np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])),
            ("⑤ 치환", np.array([[0, 1], [1, 0.]])),
            ("⑥ $x$축 사영", np.array([[1, 0], [0, 0.]]))]
    xl, yl = (-0.8, 2.2), (-0.5, 1.8)
    pw, ph = (xl[1] - xl[0]) * U, (yl[1] - yl[0]) * U
    gap, rgap = 0.45, 0.55
    fig = canvas(8.0, 0.2 + 2 * ph + rgap + 0.4)
    for i, (name, M) in enumerate(mats):
        r, c = divmod(i, 3)
        x0 = 0.25 + c * (pw + gap)
        y0 = 0.2 + (1 - r) * (ph + rgap)
        a = plane(fig, x0, y0, xl, yl, unit=U)
        poly(a, M @ SQ, fc=AFTER_FC, ec=AFTER_EC, lw=1.2, z=0.5)
        poly(a, SQ, fc="none", ec=TEXT2, lw=1.2, ls=DASH, z=2)
        if np.linalg.norm(M[:, 0]) > 1e-9:
            vec(a, M[:, 0], CAT[0], lw=2.2)
        if np.linalg.norm(M[:, 1]) > 1e-9:
            vec(a, M[:, 1], CAT[1], lw=2.2)
        else:                                   # 사영: e2가 원점으로
            dot(a, (0, 0), CAT[1], s=8)
            a.text(-0.08, -0.1, "$e_2\\to 0$", color=CAT[1], fontsize=11, ha="right", va="top")
        tag(a, name, y=1.04)
    save(fig, out("ch02", "f2_gallery.png"))


def f3_noncommute():
    U = 0.62
    R = np.array([[0, -1], [1, 0.]]); P = np.array([[1, 0], [0, 0.]])
    xl, yl = (-1.4, 1.4), (-0.3, 1.4)
    pw, ph = (xl[1] - xl[0]) * U, (yl[1] - yl[0]) * U
    gap = 0.85
    xs = [0.2 + k * (pw + gap) for k in range(3)]
    y_top = 0.2 + ph + 0.55
    rows = [(y_top, CAT[0], "① $PR$ — 돌린 뒤 사영", [(R, "$R$", "90° 회전"), (P, "$P$", "$x$축 사영")]),
            (0.2, CAT[1], "② $RP$ — 사영 뒤 회전", [(P, "$P$", "$x$축 사영"), (R, "$R$", "90° 회전")])]
    fig = canvas(7.4, y_top + ph + 0.45)
    o = overlay(fig)
    for y0, col, name, steps in rows:
        shape = SQ.copy()
        for k in range(3):
            a = plane(fig, xs[k], y0, xl, yl, unit=U)
            if k == 0:
                poly(a, SQ, fc=GREY_FC, ec=TEXT2, lw=1.0)
                tag(a, name, y=1.06)
                continue
            shape = steps[k - 1][0] @ shape
            poly(a, SQ, fc="none", ec=TEXT2, lw=1.2, ls=DASH, z=2)
            if abs(np.linalg.det(np.vstack([shape[:, 1] - shape[:, 0], shape[:, 3] - shape[:, 0]]))) > 1e-9:
                poly(a, shape, fc=mix(col, 0.2), ec=col, lw=1.6, z=1.5)   # 축선 위로
            else:                               # 선분으로 납작해짐
                p = shape.T
                lo, hi = p.min(axis=0), p.max(axis=0)
                a.plot([lo[0], hi[0]], [lo[1], hi[1]], color=col, lw=4.5,
                       solid_capstyle="butt", zorder=3)
        ym = y0 + ph / 2
        for k, (_, sym, desc) in enumerate(steps):
            x1, x2 = xs[k] + pw + 0.1, xs[k + 1] - 0.1
            arrow(o, x1, ym, x2, ym, color=TEXT2, lw=1.6)
            label(o, (x1 + x2) / 2, ym + 0.2, sym, fs=14)
            label(o, (x1 + x2) / 2, ym - 0.2, desc, fs=11, c=TEXT2)
    save(fig, out("ch02", "f3_noncommute.png"))


if __name__ == "__main__":
    f1_columns()
    f2_gallery()
    f3_noncommute()
