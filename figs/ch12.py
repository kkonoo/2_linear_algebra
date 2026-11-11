"""12장 그림. 예제 대칭행렬은 본문 §6-1의 A = [[2,1],[1,3]] (그림 1, 그림 2의 ①).

실행: cd figs && python3 ch12.py
"""
from lafig import *

A = np.array([[2., 1.], [1., 3.]])
GHOST = mix(TEXT2, 0.45)                    # 직전 단계(회색 점선)
SHAPE_FC, SHAPE_EC = mix(TEXT2, 0.14), TEXT2  # 변환되는 모양(중립 회색)
CONTOUR = TEXT2                              # 등고선


def eig_fixed(M):
    """고유값 오름차순(λ1 ≤ λ2). 고유벡터 부호는 x>0 (x=0이면 y>0)으로 고정."""
    w, V = np.linalg.eigh(M)
    for k in range(V.shape[1]):
        v = V[:, k]
        if v[0] < -1e-12 or (abs(v[0]) < 1e-12 and v[1] < 0):
            V[:, k] = -v
    return w, V


def vlab(ax, p, s, color, off, ha="left", va="bottom"):
    """벡터 끝점 옆 라벨(격자·등고선 위에서도 읽히게 흰 바탕)."""
    ax.annotate(s, p, xytext=off, textcoords="offset points", fontsize=13, color=color,
                ha=ha, va=va, zorder=7,
                bbox=dict(boxstyle="square,pad=0.08", fc="white", ec="none"))


def f1_evd_steps():
    w, Q = eig_fixed(A)
    assert np.linalg.det(Q) > 0                 # Q가 회전이 되도록 부호를 맞춤
    q1, q2 = Q[:, 0], Q[:, 1]
    e1, e2 = np.eye(2)
    t = np.linspace(0, 2 * np.pi, 361)
    S0 = np.vstack([np.cos(t), np.sin(t)])     # 단위원
    S1 = Q.T @ S0                               # ① Qᵀ 회전
    S2 = np.diag(w) @ S1                        # ② Λ 늘이기
    S3 = Q @ S2                                 # ③ Q 되돌리기 (= A·원)

    U, ylim = 0.46, (-3.9, 4.3)
    panels = [
        ("단위원", (-1.5, 1.6), S0, None, [],
         [(q1, "$q_1$", (4, -3), "top"), (q2, "$q_2$", (4, 2), "bottom")]),
        ("① $Q^{\\mathsf{T}}$ 회전", (-1.5, 1.7), S1, None, [q1, q2],
         [(e1, "$e_1$", (3, -4), "top"), (e2, "$e_2$", (4, 3), "bottom")]),
        ("② $\\Lambda$ 늘이기", (-1.7, 2.5), S2, S0, [],
         [(w[0] * e1, "$\\lambda_1 e_1$", (4, -4), "top"),
          (w[1] * e2, "$\\lambda_2 e_2$", (4, 3), "bottom")]),
        ("③ $Q$ 되돌리기", (-2.5, 3.0), S3, S2, [],
         [(w[0] * q1, "$\\lambda_1 q_1$", (15, -6), "top"),
          (w[1] * q2, "$\\lambda_2 q_2$", (3, 4), "bottom")]),
    ]
    fig = canvas(8.4, 4.3)
    x = 0.1
    for name, xlim, S, G, ghost_vecs, vecs in panels:
        a = plane(fig, x, 0.15, xlim, ylim, unit=U)
        a.fill(S[0], S[1], fc=SHAPE_FC, ec="none", zorder=0.5)
        a.plot(S[0], S[1], color=SHAPE_EC, lw=1.6, zorder=2)
        if G is not None:
            a.plot(G[0], G[1], color=GHOST, lw=1.3, ls=(0, (4, 3)), zorder=2)
        for v in ghost_vecs:
            vec(a, v, GHOST, lw=1.4, ls=(0, (3, 2)), z=3)
        for (v, s, off, va), c in zip(vecs, CAT[:2]):
            vec(a, v, c, z=5)
            vlab(a, v, s, c, off, va=va)
        tag(a, name, y=1.01)
        x += (xlim[1] - xlim[0]) * U + 0.25
    save(fig, out("ch12", "f1_evd_steps.png"))


def f2_quadratic_forms():
    cases = [
        ("① 양정치", A, [0.5, 1.5, 3, 5], "$\\lambda_1,\\ \\lambda_2>0$",
         [((4, -3), "top"), ((4, 2), "bottom")]),
        ("② 양의 준정치", np.array([[1., 1.], [1., 1.]]), [0.3, 1, 2.2, 4],
         "$\\lambda_1=0<\\lambda_2$",
         [((4, -3), "top"), ((4, 2), "bottom")]),
        ("③ 부정치", np.array([[1., 0.], [0., -1.]]), [-3, -1.5, -0.5, 0.5, 1.5, 3],
         "$\\lambda_1<0<\\lambda_2$",
         [((5, 0), "center"), ((2, 4), "bottom")]),
    ]
    U = 0.6
    fig = canvas(8.4, 3.5)
    g = np.linspace(-2, 2, 401)
    gx, gy = np.meshgrid(g, g)
    for i, (name, M, levels, cond, offs) in enumerate(cases):
        a = plane(fig, 0.15 + i * (4 * U + 0.4), 0.55, (-2, 2), (-2, 2), unit=U, grid=False)
        Z = M[0, 0] * gx**2 + 2 * M[0, 1] * gx * gy + M[1, 1] * gy**2
        pos = [l for l in levels if l > 0]
        neg = [l for l in levels if l < 0]
        a.contour(gx, gy, Z, levels=pos, colors=[CONTOUR], linewidths=1.0,
                  linestyles="solid", zorder=2)
        if neg:
            a.contour(gx, gy, Z, levels=neg, colors=[CONTOUR], linewidths=1.0,
                      linestyles="dashed", zorder=2)
        if abs(np.linalg.det(M)) < 1e-12:       # 준정치: q = 0인 골짜기 바닥(직선)
            line(a, M[0, 0], M[0, 1], 0, CONTOUR, lw=1.0, z=2)
        w, V = eig_fixed(M)
        for k, c in enumerate(CAT[:2]):
            v = V[:, k] * 1.5
            vec(a, v, c, z=5)
            off, va = offs[k]
            vlab(a, v, f"$q_{k + 1}$", c, off, va=va)
        tag(a, name, y=1.02)
        a.text(0.5, -0.05, cond, transform=a.transAxes, fontsize=12, color=TEXT2,
               ha="center", va="top")
    save(fig, out("ch12", "f2_quadratic_forms.png"))


if __name__ == "__main__":
    f1_evd_steps()
    f2_quadratic_forms()
