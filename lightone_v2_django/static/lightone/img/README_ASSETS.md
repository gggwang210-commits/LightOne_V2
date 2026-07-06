# LIGHT ONE UI Source Assets

이미지 레퍼런스를 웹페이지 구성용 소스 이미지로 분해한 파일입니다.

> 참고: 파일명에 포함된 `medical` 또는 `hospital`은 원본 소스 식별용 레거시 명칭이며, 제품 정체성은 비의료 웰니스·운동 상담 보조 자산으로만 정의합니다.

권장 위치:
`static/lightone/img/`

## 파일 목록

- `01_hero_main_dashboard.png` — 메인 히어로 배경 / dashboard hero background — 918x270
- `02_hero_sub_medical_light.png` — 서브 히어로 슬림 배경 / secondary wellness background strip — 918x180
- `03_sidebar_layout_reference.png` — 사이드바 레이아웃 참고 / sidebar reference — 172x496
- `04_card_panel_background.png` — 카드·패널 배경 / card panel background — 367x187
- `05_chart_panel_background.png` — 그래프·차트 패널 배경 / chart panel background — 367x154
- `06_kpi_card_background.png` — KPI 카드 배경 / KPI card background — 367x88
- `07_feature_importance_panel.png` — 피처 중요도 패널 배경 / feature importance panel — 470x141
- `08_content_section_background.png` — 콘텐츠 섹션 배경 / content section background — 440x164
- `09_roadmap_timeline_background.png` — 로드맵·타임라인 배경 / roadmap timeline background — 557x163
- `10_01_runner_ai_illustration.png` — 러너 AI 일러스트 / runner AI illustration — 202x126
- `10_02_hospital_corridor_blur.png` — 웰니스 공간 배경 / wellness background — 212x126
- `10_03_hand_hologram_body.png` — 컨디셔닝 안내 비주얼 / conditioning visual — 212x126
- `10_04_heartbeat_signal.png` — 운동 리듬 데이터 패턴 / conditioning data pattern — 219x126
- `10_05_dna_medical_texture.png` — 추상 데이터 패턴 / abstract data pattern — 211x126
- `10_06_smartwatch_health.png` — 스마트워치 컨디셔닝 이미지 / smartwatch conditioning visual — 210x126
- `10_07_medical_plus_icon.png` — 웰니스 지원 아이콘 / wellness support icon — 185x126
- `11_01_dotted_wave_pattern.png` — 도트 웨이브 패턴 / dotted wave pattern — 295x95
- `11_02_hexagon_pattern.png` — 헥사곤 패턴 / hexagon pattern — 309x95
- `11_03_soft_wave_gradient.png` — 소프트 웨이브 그라디언트 / soft wave gradient — 287x95
- `11_04_dark_digital_grid.png` — 다크 디지털 그리드 / dark digital grid — 291x95
- `11_05_network_node_pattern.png` — 네트워크 노드 패턴 / network node pattern — 280x95


## Django CSS 사용 예시

```css
.premium-hero {
  background-image:
    linear-gradient(90deg, rgba(5, 22, 54, 0.92), rgba(20, 89, 220, 0.58)),
    url("../img/01_hero_main_dashboard.png");
  background-size: cover;
  background-position: center;
}
```

## Django template 사용 예시

```html
{% load static %}
<img src="{% static 'lightone/img/10_01_runner_ai_illustration.png' %}" alt="AI runner">
```
