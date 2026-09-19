# 선형대수 — 기하학적 직관으로 읽는

Quarto 기반 선형대수 교재 사이트.

- 공개 주소: https://kkonoo.github.io/2_linear_algebra/
- 구성: 6 Part · 18장 + 부록 3
- 대상: 학부 일반 선형대수 (수식·기하학적 직관 중심, R/Python 코드는 보조)

## 구조

```
_quarto.yml          # 사이트 설정 · Part별 사이드바
index.qmd            # 홈 — 전체 목차, 표기 규칙
chapters/
  01_vector.qmd              Part I.  벡터와 행렬
  02_linear_transformation.qmd
  03_inner_product.qmd
  04_subspaces.qmd           Part II. 공간의 구조
  05_change_of_basis.qmd
  06_determinant.qmd
  07_gauss_elimination.qmd   Part III. 연립방정식 풀기
  08_lu_cholesky.qmd
  09_least_squares.qmd       Part IV. 최적해
  10_pseudo_inverse.qmd
  11_eigen.qmd               Part V.  분해
  12_evd.qmd
  13_pca.qmd
  14_qr.qmd
  15_svd.qmd
  16_ica_nmf.qmd             Part VI. 더 나아가기
  17_matrix_calculus.qmd
  18_fourier.qmd
  _template.qmd              (렌더 제외 — 형식 참고용)
appendix/
  a_numerical.qmd  b_affine.qmd  c_cheatsheet.qmd
figs/                # 그림 생성 스크립트 (style.py, fig_part1.py, fig_part2.py)
assets/              # html.css, ai-chat-init.html
images/              # 로고·파비콘 + 챕터별 그림 (ch01/ … ch18/, figs/ 스크립트가 생성)
```

## 표기 규칙

| 기호 | 뜻 |
|---|---|
| 🎯 | 학습목표 |
| 🤔 | 출발 질문 |
| ⚠️ | 흔한 오해 |
| 🧬 | 생물정보학 연결 (선택 읽기) |
| 🔗 | 다른 장과의 연결 |
| ✅ | 체크리스트 · 연습문제 |

문서 소스에서 **＋** 표시는 원자료(`S_M_1_선형대수`)에 없던 신규 보완 항목입니다.

## 장 작성 형식

```
---
title: "N. 제목"
description: "한 줄 설명"
author: "Eunji Ha"
date: today
format:
  html:
    include-in-header:
      text: |
        <meta name="ai-title" content="N. 제목">
        <meta name="ai-context" content="AI 도우미에게 줄 장 요약 2-3문단">
---

🎯 학습목표 callout → 🤔 출발 질문 → 본문(## 1. {#s1} / ### 1) {#s1-1})
→ 코드 callout(R·Python 탭) → ⚠️ 흔한 오해 → 🧬 생물정보학에서는
→ ✅ 정리와 연습 → 🔗 다음 장 → 참고 자료
```

### 서술 규칙 — 개조식

- 본문은 **문단이 아니라 항목**으로 쓴다. 줄글 서술 금지
- 관계는 들여쓰기와 기호로 표현
  - `…` 부연 · `→` 귀결 · `⟹` 결론 · `vs` 대비
- 대비·분류는 표로 뺀다
- 강조할 한 문장만 `>` 인용으로 남긴다 (장당 1–2회)
- 문장 끝맺음은 명사형으로 (`~이다`/`~합니다` 대신 `~임`, `~함`, 또는 체언 종결)

새 장을 추가하면 `_quarto.yml`의 `sidebar.contents` 해당 Part에도 등록합니다.

## 그림

```bash
cd figs && python3 fig_part1.py && python3 fig_part2.py
```

- 33장의 그림이 `images/chXX/`에 생성됩니다
- 자세한 규칙은 [figs/README.md](figs/README.md)

## 참고

- 원자료: `S_M_1_선형대수` 문서 1–5 (2021–2022)
- [공돌이의 수학정리노트](https://angeloyeo.github.io/) — 기하학적 직관 서술 참고, 각 장 말미에 해당 포스트 연결

## 로컬 미리보기

```bash
quarto preview
```

push하면 GitHub Actions가 자동으로 빌드·배포합니다 (`.github/workflows/deploy.yml`).
