# LIGHTONE Visual Source Usage Guide

## 1. 목적

이 문서는 사용자가 제작한 LIGHTONE 시각 자료를 현재 Django MVP 프로젝트에 바로 적용하기 위한 사용 가이드입니다.

## 2. 권장 저장 경로

```text
lightone_v2_django/static/lightone/img/brand/
lightone_v2_django/static/lightone/css/brand_visual_assets.css
```

## 3. 포함 예정 자산

```text
studio-interior-night-blue.webp
studio-interior-day.webp
studio-interior-night-warm.webp
studio-interior-night-blue-alt.webp
trainer-feedback-dashboard.webp
ai-fitness-overlay-bg.webp
network-abstract-bg.webp
studio-exterior-day.webp
dashboard-icon-set.webp
asset_manifest.json
```

## 4. 적용 우선순위

1. `studio-interior-night-warm.webp` — 랜딩페이지 hero 또는 premium studio visual
2. `trainer-feedback-dashboard.webp` — 제품 소개/포트폴리오 대표 목업
3. `ai-fitness-overlay-bg.webp` — AI/QS/JATC 설명 섹션 배경
4. `studio-exterior-day.webp` — 브랜드 스토리 또는 PT Studio 확장 비전
5. `dashboard-icon-set.webp` — 아이콘 스타일 참고 자료

## 5. Django 템플릿 적용 예시

```django
{% load static %}
<link rel="stylesheet" href="{% static 'lightone/css/brand_visual_assets.css' %}">

<section class="lo-hero-visual lo-hero-night">
  <div class="container py-5">
    <h1>LIGHTONE</h1>
    <p>비의료 PT 상담 리포트 SaaS MVP</p>
    <p class="lo-nonmedical-caption">
      비의료 운동상담 참고용 · 트레이너 검토 필요
    </p>
  </div>
</section>
```

## 6. 비의료 안전 문구

권장 문구:

> 본 화면은 비의료 PT 상담 참고용입니다. AI 및 점수 결과는 최종 판단이 아니며 트레이너 검토가 필요합니다.

## 7. 주의

이 자산은 브랜드·제품 표현용입니다. 의료 진단, 치료, 처방, 질병 예측, 환자 모니터링 화면처럼 보이게 사용하지 않습니다.
