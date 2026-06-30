# LIGHT ONE Trainer Report SaaS

LIGHT ONE은 PT샵과 트레이너가 보유한 운동 기록, 체형 관찰, 통증 반응, 상담 메모를 하나의 상담 리포트로 정리하는 비의료 보조 SaaS 프로토타입입니다.

## 1. 프로젝트 목적

PT샵에서는 회원의 운동 기록, 체형 변화, 통증 반응, 상담 메모가 여러 곳에 흩어져 관리되는 경우가 많습니다. LIGHT ONE은 이 데이터를 하나의 리포트 흐름으로 정리해 트레이너가 재등록 상담과 회원 관리에 활용할 수 있도록 돕는 것을 목표로 합니다.

## 2. 핵심 개념

LIGHT ONE은 의료 진단, 치료, 처방, 질병 예측을 목적으로 하지 않습니다. 회원 데이터를 바탕으로 트레이너가 상담 전에 확인해야 할 항목을 정리하고, 최종 판단은 트레이너가 수행하는 Human-in-the-loop 구조를 따릅니다.

## 3. 주요 기능

- LIGHT ONE 사업 개요 페이지
- 서비스 구조 소개 페이지
- 회원별 샘플 상담 리포트 페이지
- MVP 적용 흐름 시각화
- AUTO / REVIEW / BLOCK 기반 상담 우선순위 분류
- PASS / CHECK / FAIL 기반 리포트 검토 상태 표시
- 샘플 데이터 생성 명령어 제공

## 4. 주요 경로

- /lightone/ : LIGHT ONE 사업 개요 및 MVP 대시보드
- /lightone/method/ : 서비스 구조 및 작동 방식 설명
- /lightone/report/<id>/ : 회원별 샘플 상담 리포트

## 5. 기술 스택

- Python
- Django
- SQLite
- HTML / CSS / JavaScript
- VS Code
- Git

## 6. 실행 방법

프로젝트 폴더에서 아래 순서로 실행합니다.

1. python -m pip install -r requirements.txt
2. python manage.py migrate
3. python manage.py seed_lightone
4. python manage.py runserver

브라우저 접속 주소는 http://127.0.0.1:8000/lightone/ 입니다.

## 7. 비의료 고지

본 프로젝트는 의료 진단, 치료, 처방, 질병 예측을 목적으로 하지 않습니다. LIGHT ONE은 PT샵 운영과 트레이너 상담을 보조하기 위한 비의료 리포트 SaaS 프로토타입입니다.

## 8. 현재 개발 상태

현재 버전은 LIGHT ONE 사업 소개와 MVP 화면 구조를 검증하기 위한 Django 프로토타입입니다. 향후 실제 회원 입력폼, 상담 리포트 자동 생성, 체형 분석 이미지 업로드, PT샵 관리자 화면을 보완할 예정입니다.
