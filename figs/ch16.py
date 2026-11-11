"""16장 그림. PCA와 ICA — 같은 데이터(균등분포 원본을 섞은 설명용 가상 데이터), 다른 기준.

실행: cd figs && python3 ch16.py
"""
from lafig import *


def f1_pca_vs_ica():
    rng = np.random.default_rng(5)
    s = rng.uniform(-1, 1, size=(800, 2))           # 비가우시안(균등) 원본
    A = np.array([[1.0, .7], [.35, 1.0]])
    X = s @ A.T; m = X.mean(0); X -= m
    C = np.cov(X.T); w, Q = np.linalg.eigh(C); w, Q = w[::-1], Q[:, ::-1]
    if Q[0, 0] < 0: Q[:, 0] *= -1                   # PC1은 오른쪽 위로
    if Q[1, 1] < 0: Q[:, 1] *= -1                   # PC2는 위쪽으로

    U = 0.9
    xl, yl = (-1.9, 2.1), (-1.5, 1.9)
    fig = canvas(8.2, 3.6)
    a = plane(fig, 0.2, 0.2, xl, yl, unit=U, grid=False, axes=False)
    b = plane(fig, 4.3, 0.2, xl, yl, unit=U, grid=False, axes=False)
    pts = mix(TEXT2, 0.4)
    for p in (a, b):
        p.plot(X[:, 0], X[:, 1], "o", color=pts, ms=2.2, mec="none", zorder=2)

    # ① PCA — 분산이 큰 직교 축
    v1 = Q[:, 0] * np.sqrt(w[0]) * 2.2
    v2 = Q[:, 1] * np.sqrt(w[1]) * 2.2
    r = 0.16                                        # 직각 표시
    u1, u2 = Q[:, 0] * r, Q[:, 1] * r
    a.plot([u1[0], u1[0] + u2[0], u2[0]], [u1[1], u1[1] + u2[1], u2[1]],
           color=TEXT, lw=1.1, zorder=5)
    vec(a, v1, CAT[0], "PC1", lw=2.6, off=(5, 3))
    vec(a, v2, CAT[1], "PC2", lw=2.6, off=(-4, 4), ha="right")
    tag(a, "① PCA — 직교 축", y=1.02)

    # ② ICA — 데이터를 만든 원래 축(혼합 행렬의 열) = 평행사변형의 두 변, 직교 아님
    corner = A @ np.array([-1.0, -1.0]) - m         # 왼쪽 아래 꼭짓점
    start = corner + np.array([-0.1, -0.1])         # 점구름 바로 바깥에서 출발
    i1 = A[:, 0] / np.linalg.norm(A[:, 0]) * 2.0
    i2 = A[:, 1] / np.linalg.norm(A[:, 1]) * 2.0
    vec(b, i1, CAT[0], "IC1", start=start, lw=2.6, off=(4, -6), va="top")
    vec(b, i2, CAT[1], "IC2", start=start, lw=2.6, off=(-6, 2), ha="right")
    tag(b, "② ICA — 원래 축", y=1.02)
    save(fig, out("ch16", "f1_pca_vs_ica.png"))


if __name__ == "__main__":
    f1_pca_vs_ica()
