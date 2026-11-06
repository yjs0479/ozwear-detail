# 표준 상세 틀 (로리 기준 가독성) — 11/07
- 기준: 오즈라나 로리 OZ3027 16430898234. 모든 쿠팡 상세는 이 틀로만 만든다(글씨 크기·색 고정).
- `build.py`의 `run_big(P)` 또는 `run_big({'code':..}, html_path=...)`: gen_ozw 틀 HTML을 CSS 폭 590으로 그려 780px로 확대(글씨 ×1.32) + 큰 글씨 배송·관리 블록.
- P 딕셔너리 예시: examples/prods_jade7_mellow_valen.py, examples/corin_mk.py. 사이즈표는 build.size_html (세로표).
- 올리기 전: 핸드폰 폭(390)으로 줄여 로리와 나란히 비교, 한 글자 줄바꿈 고치기. 판매중 리스팅 교체는 Jenny 확인 후 시드니 05:00~10:00.
- 글씨 측정: measure_text.js (판정 기준 파일 안에).
- 필요: python3, Pillow, numpy, playwright(chromium), Noto Sans/Serif CJK KR 폰트.
