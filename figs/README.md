# 그림 생성

본문 그림은 전부 이 폴더의 스크립트로 만듭니다. 출력은 `images/ch01/`, `images/ch02/` … 로 들어갑니다.

```bash
cd figs
python3 fig_part1.py    # 1–7장
python3 fig_part2.py    # 9–18장
```

- `style.py` … 공통 색·크기·헬퍼 (`plane`, `arrow`, `save`)
  - 색은 `assets/html.css`의 h2 색(#5B4D80)을 기준으로 맞췄습니다
  - 한글 폰트는 설치된 것 중에서 자동 선택 (Pretendard → Malgun Gothic → NanumGothic → Noto Sans CJK)
- 필요 패키지: `numpy`, `matplotlib`
- 그림 안에는 짧은 라벨만 넣고, 설명은 qmd의 캡션에 둡니다 (검색·선택 가능하도록)

본문에서 참조하는 형식:

```markdown
![캡션](../images/ch06/f1_determinant_area.png){fig-align="center" width="100%"}
```
